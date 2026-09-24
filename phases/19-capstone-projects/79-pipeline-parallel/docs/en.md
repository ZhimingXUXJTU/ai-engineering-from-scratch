# Pipeline Parallel and Bubble Analysis | 流水线并行与气泡分析

> Tensor parallelism splits the matrix multiply across ranks. Pipeline parallelism splits the model across ranks, one stage per rank. Microbatches flow through the pipeline. The empty time at the start and end is the bubble; minimising it is the whole craft.

> **【中文解读】** 本课讲与张量并行、数据并行正交的第三条并行轴——流水线并行：把模型按深度切成 N 个阶段（stage），每个 rank 持有一个阶段，微批次（microbatch）像流水线上的产品一样从阶段 0 流到最后一个阶段，反传再倒着流回来。流水线开头的"等第一个微批次到达末段"和结尾的"等最后一个微批次排空"期间，部分阶段无事可做——这就是气泡（bubble）。气泡分数的闭式解是 (N-1)/(M+N-1)，压低它是流水线调度的全部手艺。

> **【拓展：三条并行轴→三维混合并行】** 大模型训练的显存压力催生了三条正交的并行轴：数据并行（每卡完整模型、不同数据）、流水线并行（按层切模型）、张量并行（按矩阵乘切层）。Megatron-LM 把三者叠成 3D 并行（DP×PP×TP）跑千亿模型。本课专注流水线轴的两大调度——GPipe（先填后排）与 1F1B（一前一后交错，Megatron/PipeDream 的生产选择），以及气泡分数的推导。与 lesson 78 的 ZeRO 不同：ZeRO 切的是"状态"，流水线切的是"计算本身"。

> 🔗 **【前置】** 学本课前请先掌握：(1) Phase 19 · 76——send/recv 与集合通信原语，双 rank 真流水线 demo 建立在其上；(2) 前向/反传与激活值的生命周期概念——气泡分析的核心约束是"激活值必须存活到它的反传"；(3) lesson 78 的 ZeRO——两条分片轴正交且常组合（ZeRO-1 + pipeline）。后续衔接：lesson 80 把每阶段的参数分片写进检查点，lesson 81 把 DDP+ZeRO 组装成端到端 demo。

**Type:** Build | **类型:** 动手构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 19 Track C lessons 42-49 | **前置知识:** Phase 19 Track C 课程 42-49
**Time:** ~90 min | **时间:** 约 90 分钟

## Learning Objectives | 学习目标

- Split a sequential model into N stages and simulate a forward pipeline across N ranks.
  中文翻译：把一个顺序模型切成 N 个阶段，并在 N 个 rank 上模拟前向流水线。
- Schedule M microbatches through the pipeline using the GPipe schedule (forward-only fill, then backward) and compute the bubble fraction.
  中文翻译：用 GPipe 调度（先全部前向填充、再反传）把 M 个微批次排进流水线，并计算气泡分数。
- Compare bubble against the interleaved 1F1B schedule used in Megatron-LM and PipeDream.
  中文翻译：把气泡与 Megatron-LM 和 PipeDream 使用的交错式 1F1B 调度做对比。
- Defend stage assignment: equal compute per stage matters more than equal parameter count per stage.
  中文翻译：论证阶段划分：每阶段计算量相等比每阶段参数量相等更重要。

## The Problem | 问题引入

> **【中文解读】** 本节回答"为什么还需要流水线"。70B 模型光参数就要 140 GB，单卡放不下；ZeRO-3 虽能分参数，但每次前向每层都要 allgather 整层、付出 log(N) 跳的代价。流水线换了一条路：每 rank 只持有一个阶段，激活值逐段接力，显存随阶段数线性下降；代价是计算变串行——这就是气泡问题的来源。气泡分数 (N-1)/(M+N-1)：M=8、N=4 时 27%，M=64、N=4 时 4.5%——想让气泡小，就得有大量微批次，这直接驱动了微批次大小的设计。

A 70B-parameter model in fp16 needs 140 GB of parameters alone. No consumer GPU holds it. ZeRO-3 shards parameters across ranks but still needs every rank to allgather the full layer for each forward step, paying log(N) hops per layer. Pipeline parallel takes a different route: cut the model into N stages and put one stage on each rank. Forward of layer 1 finishes on rank 0 and hands the activation tensor to rank 1; rank 1 runs layer 2 and hands to rank 2; and so on. Backward flows in reverse. Memory drops linearly because each rank only holds one stage; compute is sequential, which is the bubble problem.

> 一个 fp16 的 70B 参数模型光参数就需要 140 GB。没有消费级 GPU 装得下。ZeRO-3 把参数分片到各 rank，但每次前向步每个 rank 仍要 allgather 整层，为每层支付 log(N) 跳。流水线并行走另一条路：把模型切成 N 个阶段，每个 rank 放一个。第 1 层的前向在 rank 0 上完成后把激活张量交给 rank 1；rank 1 跑第 2 层再交给 rank 2；依此类推。反传反向流动。因为每个 rank 只持一个阶段，显存线性下降；计算是串行的——这就是气泡问题。

The bubble is the idle time at the start of the pipeline (waiting for the first microbatch to reach the last stage) and at the end (waiting for the last microbatch to drain back through). With M microbatches and N stages the per-stage bubble fraction is (N-1)/(M+N-1). At M=8, N=4 that is 27%. At M=64, N=4 it is 4.5%. The bubble shrinks when you have many microbatches per step, which means small per-microbatch batch sizes, which is the constraint that drives microbatch design.

> 气泡是流水线开头的空闲时间（等第一个微批次到达最后一个阶段）和结尾的空闲时间（等最后一个微批次排空回流）。M 个微批次、N 个阶段时，每阶段气泡分数是 (N-1)/(M+N-1)。M=8、N=4 时是 27%。M=64、N=4 时是 4.5%。每步微批次越多气泡越小，这意味着每个微批次的 batch 要小——这正是驱动微批次设计的约束。

## The Concept | 核心概念

```mermaid
flowchart LR
  R0[rank 0: stage 0 / layer 0] --> R1[rank 1: stage 1 / layer 1]
  R1 --> R2[rank 2: stage 2 / layer 2]
  R2 --> R3[rank 3: stage 3 / loss]
  R3 -.backward.-> R2
  R2 -.backward.-> R1
  R1 -.backward.-> R0
```

### GPipe schedule

> **【中文解读】** GPipe 是"先填后排"：所有 M 个微批次先全部跑完前向，再倒序全部跑反传。代价是激活值——每个微批次的激活必须活到它自己的反传，所以激活显存随 M 线性增长。时间账：前向 M+N-1 个周期、反传再 M+N-1 个周期；每阶段有用功 2M 个周期、气泡 2(N-1) 个周期，气泡分数 = (N-1)/(M+N-1)。让 M 远大于 N 就能把气泡藏住。

Fill the pipeline forward with all M microbatches before starting any backward; then drain backward in reverse. Activations from every microbatch must be held until its backward, so memory grows linearly with M. Forward takes M+N-1 cycles, backward takes another M+N-1 cycles. Per-stage useful work is 2M cycles; per-stage bubble is 2(N-1) cycles. Bubble fraction is (N-1)/(M+N-1) when each forward and backward takes one unit of time. Picking M much greater than N hides the bubble.

> 先让全部 M 个微批次填满前向流水线，再倒序排空反传。每个微批次的激活值必须保持到它自己的反传，所以显存随 M 线性增长。前向花 M+N-1 个周期，反向再花 M+N-1 个周期。每阶段有用功是 2M 个周期；每阶段气泡是 2(N-1) 个周期。当前向和反向各占一个时间单位时，气泡分数是 (N-1)/(M+N-1)。选 M 远大于 N 就能藏住气泡。

### 1F1B schedule

> **【中文解读】** 1F1B 是"一前一后"交错：某个微批次的前向一到达最后一个阶段，立刻开始它的反传并让它流回去。每个阶段交替执行一次前向、一次反传。气泡仍然是 N-1 个周期，但激活显存只受流水线深度约束、不再随微批次数增长——这就是 Megatron、PipeDream 等生产流水线全用 1F1B 的原因。本课先实现更简单的 GPipe，1F1B 留作练习。

Interleave: as soon as a microbatch's forward reaches the last stage, start its backward and let it stream back. The schedule alternates one forward and one backward per stage. Bubble is still N-1 but activation memory is bounded by the pipeline depth, not the microbatch count. Production pipelines use 1F1B (Megatron, PipeDream). The lesson implements GPipe first because it is simpler, and 1F1B as an exercise.

> 交错执行：某个微批次的前向一到达最后一个阶段，就启动它的反传并让它流回去。调度在每个阶段上交替一次前向、一次反传。气泡仍是 N-1，但激活显存由流水线深度界定，而不是微批次数。生产流水线都用 1F1B（Megatron、PipeDream）。本课先实现更简单的 GPipe，1F1B 作为练习。

### Why equal compute per stage matters

> **【中文解读】** 阶段划分的第一原则是"每阶段计算量相等"而不是"参数量相等"：若阶段 0 花 50 ms、阶段 1 花 100 ms，每个周期都被阶段 1 卡住，其他阶段每周期白等 50 ms。参数量是错误的轴——Transformer 每层的计算由注意力 + MLP 主导，而嵌入层参数多、计算少。划分应均衡每阶段的 FLOPs，不是每阶段的权重字节数。

If stage 0 takes 50 ms and stage 1 takes 100 ms, every cycle is gated on stage 1. The other stages idle 50 ms per cycle waiting for stage 1 to release. Equal parameter count is the wrong axis: a transformer's compute is dominated by attention plus MLP per layer, and embedding layers have many parameters but little compute. Stage assignment should equalise FLOPs per stage, not weights per stage.

> 如果阶段 0 花 50 ms 而阶段 1 花 100 ms，每个周期都卡在阶段 1 上。其他阶段每周期空等 50 ms 等阶段 1 放行。参数量相等是错误的轴：Transformer 的计算由每层的注意力 + MLP 主导，而嵌入层参数很多但计算很少。阶段分配应该均衡每阶段的 FLOPs，而不是每阶段的权重。

### Microbatch versus batch

A pipeline runs M microbatches of size B each. The effective batch size is M*B. The gradient at the end of a pipeline step is the gradient on the combined M*B examples. Bubble fraction depends on M; the optimiser sees M*B. Tuning M means trading bubble (lower with high M) against per-microbatch memory (higher activation memory with high M for GPipe).

> 流水线一次跑 M 个大小为 B 的微批次。有效 batch 大小是 M*B。流水线步结束时的梯度是合并的 M*B 个样本上的梯度。气泡分数取决于 M；优化器看到的是 M*B。调 M 意味着在气泡（M 大则低）与每微批次显存（GPipe 下 M 大则激活显存高）之间做交易。

```figure
cd-pipeline-bubble
```

## Build It | 动手构建

> **【中文解读】** 代码分两层：纯调度层——`gpipe_schedule` 生成 (周期, 阶段, 微批次, 前向/反传) 事件表，`render_gantt` 画成甘特图，`measure_bubble` 数空闲格得到实测气泡，与闭式解 `bubble_fraction` 对照；真实通信层——`PipelineStage` + 双 rank gloo 进程，rank 0 持阶段 0、rank 1 持阶段 1，激活值经 send/recv 接力、梯度反传回流，证明"线上"真的能跑。demo 还打印 M=1..64 的气泡对照表，直观呈现"M 越大气泡越小"的饱和曲线。

`code/main.py` implements:

- `PipelineStage`: a small `nn.Module` that holds one stage's parameters and exposes `forward(activation)`.
- `Pipeline(stages, num_microbatches)`: orchestrates the GPipe schedule on simulated stages using simulated wall-clock per stage.
- `bubble_fraction(num_stages, num_microbatches)`: closed-form (N-1)/(M+N-1).
- A 4-stage demo that prints the per-microbatch trace and the measured bubble fraction.

Run it:

```bash
python3 code/main.py
```

Output: a stage-by-microbatch Gantt chart and the bubble percentage against the closed-form prediction.

> 输出：一张阶段×微批次的甘特图，以及实测气泡百分比与闭式解预测的对照。

## Production patterns in the wild | 生产中的实战模式

> **【中文解读】** 三条实战经验：(1) 激活值检查点与流水线是天生一对——GPipe 下 M 个微批次在飞，激活显存是单微批次的 M 倍，激活检查点用反传时重算前向换显存，两者结合才让长序列的流水线可行；(2) 阶段均衡要实测不要假设——生产团队先跑 profiling 量每层真实耗时再划分，Megatron 的 `--num-layers-per-stage` 接受列表以支持不均等层数；(3) send/recv 顺序必须防死锁——所有阶段都"先发后收"会在网上死锁，标准修法是偶数 rank 先发后收、奇数 rank 先收后发。

Three patterns harden pipeline parallel enough to ship.

> 三条模式让流水线并行足以投入生产。

**Activation checkpointing pairs with pipeline.** With M microbatches in flight on GPipe, activation memory is M times one microbatch. Activation checkpointing recomputes the forward at backward time, trading compute for memory; the combination is what makes pipeline tractable for long sequences.

> **激活值检查点与流水线配对。** GPipe 上同时有 M 个微批次在飞时，激活显存是单个微批次的 M 倍。激活值检查点在反传时重算前向，用计算换显存；两者结合才让长序列的流水线变得可行。

**Stage balance is measured, not assumed.** Production teams run a profiling pass that measures actual per-layer compute (FLOPs and wall-clock) on the target hardware, then partition by that measurement. The Megatron-LM `--num-layers-per-stage` flag accepts a list to allow uneven layer counts when stages have different per-layer cost.

> **阶段均衡靠实测，不靠假设。** 生产团队先跑一遍 profiling，在目标硬件上量出每层真实计算量（FLOPs 和墙钟时间），再按测量结果划分。Megatron-LM 的 `--num-layers-per-stage` 标志接受一个列表，允许在每层成本不同时使用不均等的层数。

**Send-recv schedule must avoid deadlock.** A pipeline that has every stage send before receive deadlocks on the wire. The standard fix is to interleave: even-rank stages send first then recv, odd-rank stages recv first then send. The lesson schedules ranks explicitly so the pattern is visible.

> **send/recv 调度必须避免死锁。** 每个阶段都先发后收的流水线会在网络上死锁。标准修法是交错：偶数 rank 的阶段先发后收，奇数 rank 的阶段先收后发。本课显式编排 rank 顺序，让这个模式看得见。

## Use It | 用框架实现

> **【中文解读】** 三个生产框架与手工实现的对应：Megatron-LM 是大规模流水线并行的参考实现（1F1B 调度、张量+流水线+数据三并行混合）；DeepSpeed Pipeline 与 ZeRO 集成，ZeRO-1 + pipeline 是最大的开源模型的常见组合；PyTorch Pipe 是 PyTorch 原生的流水线封装。

Production patterns:

- **Megatron-LM.** The reference for pipeline parallel at scale. Uses 1F1B and supports tensor + pipeline + data parallel combined.
  中文翻译：**Megatron-LM**——大规模流水线并行的参考实现，使用 1F1B 并支持张量 + 流水线 + 数据并行组合。
- **DeepSpeed Pipeline.** Integrates with ZeRO; ZeRO-1 + pipeline is a common combo for the largest open models.
  中文翻译：**DeepSpeed Pipeline**——与 ZeRO 集成；ZeRO-1 + 流水线是最大开源模型的常见组合。
- **PyTorch Pipe.** The PyTorch-native pipeline wrapper, built on `torch.distributed.pipeline.sync.Pipe`.
  中文翻译：**PyTorch Pipe**——PyTorch 原生流水线封装，构建在 `torch.distributed.pipeline.sync.Pipe` 之上。

## Ship It | 产出物

Lesson 80 stores the per-stage parameter shards in the sharded checkpoint. Lesson 81 composes DDP + ZeRO + pipeline on the end-to-end demo (in spirit; the demo keeps the pipeline simulated for runtime).

> Lesson 80 把每阶段的参数分片存进分片检查点。Lesson 81 在端到端 demo 上组合 DDP + ZeRO + 流水线（取其精神；demo 为控制运行时保留流水线的模拟形态）。

## Exercises | 练习题

1. Implement 1F1B and verify the bubble fraction matches GPipe but activation memory is bounded.
   中文翻译：实现 1F1B，验证气泡分数与 GPipe 相同但激活显存有界。
2. Profile real per-stage time on a deeper model and rebalance stages by measured wall-clock.
   中文翻译：在更深的模型上剖析每阶段真实耗时，并按实测墙钟时间重新均衡阶段。
3. Add gradient accumulation across pipeline microbatches and check the gradient equals the gradient of the equivalent full-batch forward.
   中文翻译：跨流水线微批次加梯度累积，检查梯度等于等价全 batch 前向的梯度。
4. Pair the pipeline with activation checkpointing and measure the memory drop versus compute cost.
   中文翻译：给流水线配上激活值检查点，测量显存下降与计算代价的对比。
5. Combine pipeline with DDP (each pipeline rank is replicated across a data-parallel group) and reason through the 2D schedule.
   中文翻译：把流水线与 DDP 组合（每个流水线 rank 在数据并行组内再复制一份），并推理这个二维调度的行为。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Pipeline | "Model parallel along depth" | One stage per rank, activations flow stage to stage |
| Bubble | "Pipeline idle time" | (N-1) steps at start + end where some stages have no work |
| Microbatch | "Slice of the batch" | One forward/backward unit; bubble shrinks as M grows |
| GPipe | "Fill then drain" | All M forwards before any backward; high activation memory |
| 1F1B | "Interleaved schedule" | One forward one backward per stage; bounded activation memory |

## Further Reading | 延伸阅读

- [Huang et al, GPipe: Efficient Training of Giant Neural Networks](https://arxiv.org/abs/1811.06965)
  中文翻译：GPipe 论文原典——先填后排调度与气泡推导
- [Narayanan et al, PipeDream: Generalized Pipeline Parallelism for DNN Training](https://arxiv.org/abs/1806.03377)
  中文翻译：PipeDream 论文——1F1B 类交错调度的来源
- [Megatron-LM pipeline parallel docs](https://github.com/NVIDIA/Megatron-LM)
  中文翻译：Megatron-LM 流水线并行文档——生产级 1F1B 与 3D 并行
- Phase 19 Lesson 76 - the send/recv primitives the schedule uses
  中文翻译：Phase 19 Lesson 76——调度使用的 send/recv 原语
- Phase 19 Lesson 78 - ZeRO is orthogonal to pipeline and often combined
  中文翻译：Phase 19 Lesson 78——ZeRO 与流水线正交且经常组合使用
