# DualPipe Parallelism | 双向流水线并行

> DeepSeek-V3 was trained on 2,048 H800 GPUs with MoE experts scattered across nodes. Cross-node expert all-to-all communication cost 1 GPU-hour of comm for every 1 GPU-hour of compute. GPUs were idle half the time. DualPipe (DeepSeek, Dec 2024) is a bidirectional pipeline that overlaps forward and backward computation with the all-to-all comms they trigger. Bubbles drop, throughput climbs, and the keeping of two model-parameter copies (the "dual" that gives the name) is cheap once Expert Parallelism is already spreading experts across ranks anyway. This lesson is a Learn-type walkthrough of what DualPipe actually does and why Sea AI Lab's DualPipeV refinement drops the 2x parameter cost at the expense of a marginally tighter bubble.

> **【中文解读】** DeepSeek-V3 在 2048 张 H800 上训练，MoE 专家分布在节点间。跨节点 all-to-all 通信让 GPU 一半时间在等待。DualPipe 是双向流水线，将前向/反向计算与 all-to-all 通信重叠，减少气泡、提升吞吐。

> **【拓展：DualPipe→大规模训练】** DualPipe 是 DeepSeek-V3 高效训练的关键：它将 MoE 的通信开销与前向/反向计算重叠，使得在 2048 卡上的训练效率接近线性扩展。这是大规模 MoE 训练的工程突破。

**Type:** Learn
**Languages:** Python (stdlib, schedule simulator)
**Prerequisites:** Phase 10 · 05 (distributed training, FSDP, DeepSpeed), Phase 10 · 14 (open-model architectures and MoE)
**Time:** ~60 minutes

## Learning Objectives

- Name the four components of a DualPipe forward-backward chunk and why each one gets its own overlap window.
- Explain the pipeline bubble problem at scale, and what "bubble-free" means in practice versus in marketing.
- Trace a DualPipe schedule by hand for 8 PP ranks and 16 micro-batches and confirm the forward and reverse streams fill each other's idle slots.
- State the tradeoff DualPipeV (Sea AI Lab, 2025) makes: drops the 2x parameter replication at the cost of a slightly larger bubble when Expert Parallelism is inactive.

## The Problem

Training a 671B MoE model on 2k H800 GPUs runs into three compounding bottlenecks:

1. **Memory pressure.** Each GPU holds a slice of the model. Activation memory at sequence 8k across 61 layers on 128 heads is enormous.
2. **Pipeline bubbles.** Traditional pipeline parallelism (GPipe, 1F1B) leaves GPUs idle while they wait for their stage's input or gradient. At 8 stages, roughly 12% of GPU time can be bubble even with 1F1B scheduling.
3. **Cross-node all-to-all.** MoE with expert parallelism scatters experts across nodes. Every forward pass triggers an all-to-all to dispatch tokens to their experts, and another to combine. At 2k GPUs this easily becomes a 1:1 compute-to-comm ratio.

Each of these has separate solutions: gradient checkpointing for memory, Zero Bubble (Sea AI Lab, 2023) for pipeline bubbles, expert-parallel comm kernels for all-to-all. What DualPipe does is make them play together. The schedule overlaps compute and comm within a single forward-backward chunk, injects micro-batches from both ends of the pipeline simultaneously, and uses the resulting schedule to hide all-to-all inside the compute windows.

Reported result: near-elimination of pipeline bubbles, over 95% GPU utilization in DeepSeek-V3's 14.8T-token training run.

> **【中文解读】**
> 大模型训练有三大瓶颈：显存压力、流水线气泡、跨节点通信。GPipe 让 GPU 大量时间空闲，1F1B 稍好但气泡仍占 12%。DualPipe 的核心思路是把 MoE 的 all-to-all 通信"藏"在前向/反向计算里面——通信和计算同时进行，GPU 不再等待。这意味着同样的 GPU 集群可以训练更多 token，DeepSeek-V3 靠它达到了 95% 以上的 GPU 利用率。

## The Concept

### Pipeline parallelism refresher

Split an N-layer model across P devices. Device `i` holds layers `i * N/P .. (i+1) * N/P - 1`. A micro-batch flows forward through devices 0 to P-1, then backward from P-1 to 0. Each device can only start its forward stage when the prior device sends its output and can only start backward when the downstream device sends the upstream gradient.

GPipe (Huang et al., 2019) schedules one micro-batch at a time, which wastes most GPU time. 1F1B (Narayanan et al., 2021) interleaves forward and backward passes for multiple micro-batches. Zero Bubble (Qi et al., 2023) splits the backward pass into two parts — backward-for-input (B) and backward-for-weights (W) — and schedules them to fill the bubble. After Zero Bubble, the pipeline is almost tight.

DualPipe is the next step. It adds two ideas on top:

### Idea 1: chunk decomposition

Each forward chunk is split into four components:

- **Attention.** Q/K/V projections, attention, output projection.
- **All-to-all dispatch.** Cross-node communication that sends tokens to their experts.
- **MLP.** The MoE expert computation.
- **All-to-all combine.** Cross-node communication that brings expert outputs back.

A backward chunk adds gradient versions of each of these. DualPipe schedules them so that all-to-all dispatch happens in parallel with the attention compute of the next chunk, and all-to-all combine happens in parallel with the MLP compute of the following chunk.

### Idea 2: bidirectional scheduling

Most pipeline schedules inject micro-batches from stage 0 and flow toward stage P-1. DualPipe injects micro-batches from BOTH ends. Stage 0 sees forward micro-batches originating there; stage P-1 sees forward micro-batches originating there too. The two streams meet in the middle.

For this to work, device `i` must hold BOTH the early-pipeline layer `i` AND the late-pipeline layer `P - 1 - i`. That is the "dual" part of DualPipe: each device keeps two copies of the model layers it needs to serve (one for each direction). At DeepSeek-V3's scale, this is a 2x parameter replication cost. It is affordable because Expert Parallelism already spreads the MoE experts so thin that replicating the non-expert layers twice is small potatoes.

Crucially, the forward stream in one direction and the backward stream in the other direction overlap exactly where the bubbles would be in a single-direction schedule. The bubbles vanish.

### A hand-traced schedule

Consider P = 4 ranks, 8 micro-batches, divided 4 forward / 4 reverse. Time moves left to right; rows are device ranks.

```
           Time →
rank 0:  F1 F2 F3 F4  F5R F6R F7R F8R  B1 B2 B3 B4  ...
rank 1:     F1 F2 F3  F4/F5R F6R F7R   B1 B2 ...
rank 2:        F1 F2  F3/F5R F4/F6R    B1 ...
rank 3:           F1  F2/F5R F3/F6R    ...
```

Reading the "F4/F5R" notation: rank 1 is running forward of micro-batch 4 (going left-to-right in the pipeline) AND forward of micro-batch 5 (going right-to-left) in the same time slot. That is what "bidirectional" means operationally.

At rank 2 the cross streams overlap sooner, at rank 0 and P-1 they overlap latest. In the stable middle phase of the schedule, every rank runs forward-of-X-direction overlapped with backward-of-Y-direction. Compute is busy. All-to-all dispatches for the forward pass hide inside backward compute. All-to-all combines hide inside forward compute. The bubbles are squeezed out.

### Bubble accounting

Standard 1F1B pipeline bubble (time wasted per rank):

```
bubble_1F1B = (P - 1) * forward_chunk_time
```

Zero Bubble refinement brings it down but not to zero. DualPipe, in the stable phase, has zero bubble if the micro-batch count is divisible by 2 times the pipeline depth. Outside the stable phase (warmup and cooldown), there is some bubble but it does not grow with the number of micro-batches — a key property the paper highlights.

In marketing terms: "bubble-free". In technical terms: bubbles do not grow with micro-batch count. Sea AI Lab's follow-up analysis (DualPipeV / Cut-in-half) shows the full zero-bubble only when Expert Parallelism is not the bottleneck; with EP-driven all-to-all, some scheduling compromise is always present.

### DualPipeV — the refinement

Sea AI Lab (2025) observed that the 2x parameter replication is wasteful when EP comm overlap is not the point. Their DualPipeV schedule folds the bidirectional injection into a "V-shape" schedule that runs on a single parameter copy. The bubble is slightly larger than DualPipe's, but the memory savings are substantial. DeepSeek adopted DualPipeV in their open-source DualPipe implementation as an EP-off mode.

The tradeoff:

| Feature | DualPipe | DualPipeV | 1F1B | Zero Bubble |
|---------|---------|-----------|------|------------|
| Param copies per device | 2 | 1 | 1 | 1 |
| Bubble vs micro-batches | constant | small growth | grows | grows |
| Compute-comm overlap | full | partial | minimal | partial |
| Use when | EP-heavy MoE | dense or EP-light | baseline | any pipeline |

### What it means for a 14.8T-token run

DeepSeek-V3's pre-training consumed 14.8T tokens on 2,048 H800 GPUs in roughly 2.8M GPU-hours. With naive 1F1B, they would have lost 12-15% of that to pipeline bubbles — 340-420K GPU-hours, enough to train a full 70B model. DualPipe recovered most of that. Directly quantifying the contribution is difficult without the internal logs, but the claim in the paper is over 95% GPU utilization averaged across training.

For smaller runs (under 1k GPUs), DualPipe is overkill — pipeline bubbles are smaller relative to total cost, and dense-model training rarely hits the all-to-all bottleneck. For frontier MoE training at multi-thousand GPU scale, it is effectively required.

### Where it sits in the stack

- Complementary to **FSDP** (Phase 10 · 05). FSDP shards the model parameters across ranks; DualPipe schedules the compute across ranks. They combine.
- Compatible with **ZeRO-3** gradient sharding. The bookkeeping for the two-copy replication needs to cooperate with ZeRO's sharded gradients.
- Requires **custom all-to-all kernels** tuned for the specific cluster topology. DeepSeek's open-source kernels are the reference implementation.

## Use It

> **【中文解读】**
> 实际使用 DualPipe 时，核心是模拟器帮你直观感受不同调度策略的差异：1F1B 的气泡随 micro-batch 数增长，DualPipe 的气泡不增长。集成到真实训练中需要确保 EP mesh 支持双向 all-to-all，并且第一次调试调度本身可能要花一周时间。

> **【拓展：流水线并行→千亿参数训练】** GPT-4、DeepSeek-V3、Llama 405B 等千亿/万亿参数模型的训练都依赖某种形式的流水线并行。DualPipe 的创新在于专门针对 MoE 架构优化——当模型有 256 个专家分布在多节点时，通信开销是最大的瓶颈。PyTorch 的 PiPPy 和 DeepSpeed 的流水线引擎是更通用的方案，但针对 MoE 的效率不如 DualPipe。

`code/main.py` is a pipeline schedule simulator. It takes `(P, n_micro_batches, schedule)` and prints the stable-phase utilization for each of 1F1B, Zero Bubble, DualPipe, and DualPipeV. It is a teaching tool — the numbers match the qualitative claims in the papers, they are not a claim about production measured speedup.

The simulator's value: run it with different P and micro-batch counts and watch how the bubble fraction grows for 1F1B but not DualPipe.

Integration considerations for a real training run:

- Pick a pipeline-parallel depth that divides cleanly into your micro-batch count.
- Ensure your expert-parallel mesh supports bidirectional all-to-all. DeepSeek's kernels are the reference.
- Expect to burn a week of debugging time on the schedule itself the first time. The bookkeeping is fiddly.
- Monitor GPU utilization per rank, not just aggregate. DualPipe's benefit comes from tightening the stragglers.

## Ship It

This lesson produces `outputs/skill-dualpipe-planner.md`. Given a training cluster specification (GPU count, topology, interconnect, model shape), it recommends a pipeline parallelism strategy, the scheduling algorithm to use, and the expected bubble fraction at the target scale.

## Exercises

1. Run `code/main.py` on `(P=8, micro_batches=16, schedule=dualpipe)` and `(P=8, micro_batches=16, schedule=1f1b)`. Compute the GPU utilization difference and express it as recovered GPU-hours per million tokens of training.

2. Sketch the schedule table for `(P=4, micro_batches=8, schedule=dualpipe)` by hand. Mark each time slot with the micro-batch ID and direction. Identify the first time slot where bubbles are absent.

3. Read Figure 5 of the DeepSeek-V3 technical report (arXiv:2412.19437). Identify the overlap window for all-to-all dispatch inside a DualPipe forward chunk. Explain how the compute schedule hides it.

4. Compute the 2x parameter overhead of DualPipe for a 70B dense model with P=8 pipeline stages and a 671B MoE model with P=16 pipeline stages. Show why the MoE case's overhead is proportionally smaller (most parameters are experts, sharded across a large EP group).

5. Compare DualPipe to Chimera (a competing bidirectional scheduler from 2021). Identify the two specific properties DualPipe added that Chimera did not have, using the paper's Section 3.4 as the reference.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Pipeline bubble | "Idle time per rank" | GPU cycles wasted because a pipeline stage is waiting for its input or gradient |
| 1F1B | "Default pipeline schedule" | One forward / one backward interleaved scheduling; the baseline DualPipe beats |
| Zero Bubble | "Sea AI Lab 2023" | Splits backward into B (input gradient) and W (weight gradient); almost fully tightens the pipeline |
| DualPipe | "DeepSeek-V3 schedule" | Bidirectional pipeline + compute-comm overlap; bubbles do not grow with micro-batch count |
| DualPipeV | "Cut-in-half" | V-shape refinement that drops the 2x parameter replication at the cost of slightly larger bubbles |
| Chunk | "Unit of pipeline work" | A forward or backward pass of one micro-batch through one pipeline stage |
| All-to-all dispatch | "Send tokens to experts" | Cross-node comm that routes tokens to their assigned MoE experts |
| All-to-all combine | "Bring expert outputs back" | Cross-node comm that gathers expert outputs after the MLP |
| Expert Parallelism (EP) | "Experts across GPUs" | Shards MoE experts across ranks so different GPUs hold different experts |
| Pipeline Parallelism (PP) | "Layers across GPUs" | Shards model layers across ranks; the dimension DualPipe schedules |
| Bubble fraction | "Wasted GPU time" | (bubble_time / total_time); the fraction DualPipe drives toward zero |

| 术语 | 俗称 | 实际含义 |
|------|------|---------|
| 流水线气泡 | "GPU 空闲时间" | GPU 因等待前序阶段输出而浪费的时钟周期 |
| 1F1B | "默认流水线调度" | 一前向一后向交替调度；DualPipe 要超越的基线 |
| Zero Bubble | "Sea AI Lab 2023" | 将后向拆分为 B（输入梯度）和 W（权重梯度）；几乎完全压紧流水线 |
| DualPipe | "DeepSeek-V3 调度" | 双向流水线 + 计算-通信重叠；气泡不随 micro-batch 数增长 |
| DualPipeV | "Cut-in-half" | V 形改进版，去掉双倍参数复制，代价是气泡稍大 |
| Chunk | "流水线工作单元" | 一个 micro-batch 在一个流水线阶段的前向或后向传播 |
| All-to-all dispatch | "发 token 给专家" | 跨节点通信，将 token 路由到其分配的 MoE 专家 |
| All-to-all combine | "收集专家输出" | 跨节点通信，在 MLP 后收集专家输出 |
| 专家并行 (EP) | "专家分到不同 GPU" | 将 MoE 专家分片到不同 rank，不同 GPU 持有不同专家 |
| 流水线并行 (PP) | "层分到不同 GPU" | 将模型层分片到不同 rank；DualPipe 调度的维度 |
| 气泡比例 | "浪费的 GPU 时间" | (气泡时间 / 总时间)；DualPipe 将其推向零 |

## Further Reading

- [DeepSeek-AI — DeepSeek-V3 Technical Report (arXiv:2412.19437), Section 3.3.2 and Figure 5](https://arxiv.org/abs/2412.19437) — the primary DualPipe reference
- [DeepSeek — DualPipe GitHub repository](https://github.com/deepseek-ai/DualPipe) — the open-source reference implementation, including DualPipeV (Cut-in-half) mode
- [Qi et al. — Zero Bubble Pipeline Parallelism (arXiv:2401.10241, Sea AI Lab 2023)](https://arxiv.org/abs/2401.10241) — the Zero Bubble predecessor
- [Sea AI Lab — DualPipe could be better without the Dual](https://sail.sea.com/blog/articles/63) — the DualPipeV analysis that informed DeepSeek's EP-off mode
- [Narayanan et al. — PipeDream / 1F1B (arXiv:1806.03377, 2018-2021)](https://arxiv.org/abs/1806.03377) — the 1F1B schedule DualPipe compares against
- [Huang et al. — GPipe (arXiv:1811.06965, 2018)](https://arxiv.org/abs/1811.06965) — the original pipeline parallelism paper and bubble problem
