# DualPipe Parallelism | 双向流水线并行

> DeepSeek-V3 was trained on 2,048 H800 GPUs with MoE experts scattered across nodes. Cross-node expert all-to-all communication cost 1 GPU-hour of comm for every 1 GPU-hour of compute. GPUs were idle half the time. DualPipe (DeepSeek, Dec 2024) is a bidirectional pipeline that overlaps forward and backward computation with the all-to-all comms they trigger. Bubbles drop, throughput climbs, and the keeping of two model-parameter copies (the "dual" that gives the name) is cheap once Expert Parallelism is already spreading experts across ranks anyway. This lesson is a Learn-type walkthrough of what DualPipe actually does and why Sea AI Lab's DualPipeV refinement drops the 2x parameter cost at the expense of a marginally tighter bubble.

> **【中文解读】** DeepSeek-V3 在 2048 张 H800 上训练，MoE 专家分布在节点间。跨节点 all-to-all 通信让 GPU 一半时间在等待。DualPipe 是双向流水线，将前向/反向计算与 all-to-all 通信重叠，减少气泡、提升吞吐。

> **【拓展：DualPipe→大规模训练】** DualPipe 是 DeepSeek-V3 高效训练的关键：它将 MoE 的通信开销与前向/反向计算重叠，使得在 2048 卡上的训练效率接近线性扩展。这是大规模 MoE 训练的工程突破。

**Type:** Learn
**Languages:** Python (stdlib, schedule simulator)
**Prerequisites:** Phase 10 · 05 (distributed training, FSDP, DeepSpeed), Phase 10 · 14 (open-model architectures and MoE)
**Time:** ~60 minutes

## Learning Objectives | 学习目标

- Name the four components of a DualPipe forward-backward chunk and why each one gets its own overlap window.
  说出 DualPipe 前向-反向块的四个组件及其各自的重叠窗口原因
- Explain the pipeline bubble problem at scale, and what "bubble-free" means in practice versus in marketing.
  解释大规模流水线气泡问题，以及实践中"无气泡"与营销说法的区别
- Trace a DualPipe schedule by hand for 8 PP ranks and 16 micro-batches and confirm the forward and reverse streams fill each other's idle slots.
  手动追踪 8 个 PP 阶段和 16 个微批次的 DualPipe 调度，确认正向和反向流填充彼此的空闲槽位
- State the tradeoff DualPipeV (Sea AI Lab, 2025) makes: drops the 2x parameter replication at the cost of a slightly larger bubble when Expert Parallelism is inactive.
  说明 DualPipeV（Sea AI Lab, 2025）的权衡：取消 2x 参数复制，代价是 Expert Parallelism 不活跃时气泡稍大

## The Problem | 问题引入

Training a 671B MoE model on 2k H800 GPUs runs into three compounding bottlenecks:

1. **Memory pressure.** Each GPU holds a slice of the model. Activation memory at sequence 8k across 61 layers on 128 heads is enormous.
2. **Pipeline bubbles.** Traditional pipeline parallelism (GPipe, 1F1B) leaves GPUs idle while they wait for their stage's input or gradient. At 8 stages, roughly 12% of GPU time can be bubble even with 1F1B scheduling.
3. **Cross-node all-to-all.** MoE with expert parallelism scatters experts across nodes. Every forward pass triggers an all-to-all to dispatch tokens to their experts, and another to combine. At 2k GPUs this easily becomes a 1:1 compute-to-comm ratio.

> 在 2k H800 GPU 上训练 671B MoE 模型会遇到三个复合瓶颈：

1. **内存压力。** 每个 GPU 持有模型的一个切片。8k 序列长度、61 层、128 头的激活显存是巨大的。
   中文翻译：每张 GPU 持有模型的一个切片。8k 序列长度、61 层、128 头的激活显存是巨大的。
2. **流水线气泡。** 传统流水线并行（GPipe、1F1B）让 GPU 在等待其阶段的输入或梯度时空闲。8 个阶段时，即使使用 1F1B 调度，约 12% 的 GPU 时间可能是气泡。
   中文翻译：传统流水线并行让 GPU 在等待时空闲。8 个阶段时，约 12% 的 GPU 时间是气泡。
3. **跨节点全互联。** 带专家并行的 MoE 将专家分散到各节点。每次前向传播触发一次全互联将 token 分派到专家，另一次将结果合并。2k GPU 时这很容易变成 1:1 的计算通信比。
   中文翻译：MoE 专家并行每次前向传播触发两次全互联通信，在 2k GPU 时计算通信比接近 1:1。

Each of these has separate solutions: gradient checkpointing for memory, Zero Bubble (Sea AI Lab, 2023) for pipeline bubbles, expert-parallel comm kernels for all-to-all. What DualPipe does is make them play together. The schedule overlaps compute and comm within a single forward-backward chunk, injects micro-batches from both ends of the pipeline simultaneously, and uses the resulting schedule to hide all-to-all inside the compute windows.

Reported result: near-elimination of pipeline bubbles, over 95% GPU utilization in DeepSeek-V3's 14.8T-token training run.

## The Concept | 核心概念

> **【中文解读】** DualPipe 是 DeepSeek-V3 提出的双向流水线并行算法，通过在前向和反向传播之间重叠计算来最大化 GPU 利用率。相比传统单向流水线，DualPipe 显著减少了流水线气泡。

> **【拓展：DualPipe 与 DeepSeek-V3 的效率】** DeepSeek-V3 在 2048 张 H800 GPU 上训练，使用 DualPipe + MoE 专家并行 + FSDP。DualPipe 将流水线气泡率降至约 5%（传统方法约 20%），是 DeepSeek-V3 以约 560 万美元训练出顶级模型的关键技术之一。


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


> **【拓展：流水线并行的工程细节】** DualPipe 在同一方向上交替前向和反向传播，将气泡率从约 20% 降到约 5%。这对大规模训练成本影响巨大。


## Use It | 用框架实现

`code/main.py` is a pipeline schedule simulator. It takes `(P, n_micro_batches, schedule)` and prints the stable-phase utilization for each of 1F1B, Zero Bubble, DualPipe, and DualPipeV. It is a teaching tool — the numbers match the qualitative claims in the papers, they are not a claim about production measured speedup.

The simulator's value: run it with different P and micro-batch counts and watch how the bubble fraction grows for 1F1B but not DualPipe.

Integration considerations for a real training run:

- Pick a pipeline-parallel depth that divides cleanly into your micro-batch count.
- Ensure your expert-parallel mesh supports bidirectional all-to-all. DeepSeek's kernels are the reference.
- Expect to burn a week of debugging time on the schedule itself the first time. The bookkeeping is fiddly.
- Monitor GPU utilization per rank, not just aggregate. DualPipe's benefit comes from tightening the stragglers.

## Ship It | 产出物

This lesson produces `outputs/skill-dualpipe-planner.md`. Given a training cluster specification (GPU count, topology, interconnect, model shape), it recommends a pipeline parallelism strategy, the scheduling algorithm to use, and the expected bubble fraction at the target scale.

> 本课产出 `outputs/skill-dualpipe-planner.md`。给定训练集群规范（GPU 数量、拓扑、互连、模型形状），它推荐流水线并行策略、调度算法和目标规模下的预期气泡占比。

## Exercises | 练习题

1. Run `code/main.py` on `(P=8, micro_batches=16, schedule=dualpipe)` and `(P=8, micro_batches=16, schedule=1f1b)`. Compute the GPU utilization difference and express it as recovered GPU-hours per million tokens of training.
   中文翻译：在 `(P=8, micro_batches=16, schedule=dualpipe)` 和 `(P=8, micro_batches=16, schedule=1f1b)` 上运行 `code/main.py`。计算 GPU 利用率差异并表示为每百万训练 token 回收的 GPU 小时数。

2. Sketch the schedule table for `(P=4, micro_batches=8, schedule=dualpipe)` by hand. Mark each time slot with the micro-batch ID and direction. Identify the first time slot where bubbles are absent.
   中文翻译：手动画出 `(P=4, micro_batches=8, schedule=dualpipe)` 的调度表。标记每个时间槽的微批次 ID 和方向。找到气泡消失的第一个时间槽。

3. Read Figure 5 of the DeepSeek-V3 technical report (arXiv:2412.19437). Identify the overlap window for all-to-all dispatch inside a DualPipe forward chunk. Explain how the compute schedule hides it.
   中文翻译：阅读 DeepSeek-V3 技术报告图 5。识别 DualPipe 前向块内 all-to-all 调度的重叠窗口。解释计算调度如何隐藏它。

4. Compute the 2x parameter overhead of DualPipe for a 70B dense model with P=8 pipeline stages and a 671B MoE model with P=16 pipeline stages. Show why the MoE case's overhead is proportionally smaller (most parameters are experts, sharded across a large EP group).
   中文翻译：计算 DualPipe 对 70B 密集模型（P=8 流水线阶段）和 671B MoE 模型（P=16 阶段）的 2 倍参数开销。展示为什么 MoE 情况的开销比例更小（大多数参数是专家，跨大型 EP 组分片）。

5. Compare DualPipe to Chimera (a competing bidirectional scheduler from 2021). Identify the two specific properties DualPipe added that Chimera did not have, using the paper's Section 3.4 as the reference.
   中文翻译：比较 DualPipe 与 Chimera（2021 年的竞争双向调度器）。识别 DualPipe 添加的 Chimera 没有的两个特定属性，使用论文第 3.4 节作为参考。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Pipeline bubble | "Idle time per rank" | GPU cycles wasted because a pipeline stage is waiting for its input or gradient | 流水线气泡，GPU 等待输入或梯度时空转的周期 |
| 1F1B | "Default pipeline schedule" | One forward / one backward interleaved scheduling; the baseline DualPipe beats | 1F1B 调度，一前向一反向交替 |
| Zero Bubble | "Sea AI Lab 2023" | Splits backward into B (input gradient) and W (weight gradient); almost fully tightens the pipeline | 零气泡，将反向拆为输入梯度和权重梯度 |
| DualPipe | "DeepSeek-V3 schedule" | Bidirectional pipeline + compute-comm overlap; bubbles do not grow with micro-batch count | DualPipe，双向流水线+计算通信重叠 |
| DualPipeV | "Cut-in-half" | V-shape refinement that drops the 2x parameter replication at the cost of slightly larger bubbles | DualPipeV，取消 2x 参数复制，气泡略增 |
| Chunk | "Unit of pipeline work" | A forward or backward pass of one micro-batch through one pipeline stage | 块，一个微批次在一个流水线阶段的前向/反向 |
| All-to-all dispatch | "Send tokens to experts" | Cross-node comm that routes tokens to their assigned MoE experts | 全互联分派，将 token 路由到 MoE 专家 |
| All-to-all combine | "Bring expert outputs back" | Cross-node comm that gathers expert outputs after the MLP | 全互联组合，收集专家输出 |
| Expert Parallelism (EP) | "Experts across GPUs" | Shards MoE experts across ranks so different GPUs hold different experts | 专家并行，不同 GPU 持有不同 MoE 专家 |
| Pipeline Parallelism (PP) | "Layers across GPUs" | Shards model layers across ranks; the dimension DualPipe schedules | 流水线并行，模型层分布在不同 GPU |
| Bubble fraction | "Wasted GPU time" | (bubble_time / total_time); the fraction DualPipe drives toward zero | 气泡比例，DualPipe 将其压向零 |

## Further Reading | 延伸阅读

- [DeepSeek-AI — DeepSeek-V3 Technical Report (arXiv:2412.19437), Section 3.3.2 and Figure 5](https://arxiv.org/abs/2412.19437) — the primary DualPipe reference
- [DeepSeek — DualPipe GitHub repository](https://github.com/deepseek-ai/DualPipe) — the open-source reference implementation, including DualPipeV (Cut-in-half) mode
- [Qi et al. — Zero Bubble Pipeline Parallelism (arXiv:2401.10241, Sea AI Lab 2023)](https://arxiv.org/abs/2401.10241) — the Zero Bubble predecessor
- [Sea AI Lab — DualPipe could be better without the Dual](https://sail.sea.com/blog/articles/63) — the DualPipeV analysis that informed DeepSeek's EP-off mode
- [Narayanan et al. — PipeDream / 1F1B (arXiv:1806.03377, 2018-2021)](https://arxiv.org/abs/1806.03377) — the 1F1B schedule DualPipe compares against
- [Huang et al. — GPipe (arXiv:1811.06965, 2018)](https://arxiv.org/abs/1811.06965) — the original pipeline parallelism paper and bubble problem
