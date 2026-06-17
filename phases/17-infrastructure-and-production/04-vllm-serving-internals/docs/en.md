# vLLM Serving Internals: PagedAttention, Continuous Batching, Chunked Prefill | vLLM 推理服务内部机制：分页注意力、连续批处理、分块预填充

> vLLM's dominance in 2026 rests on three compounding defaults, not a single trick. PagedAttention is always on. Continuous batching injects new requests into the active batch between decode iterations. Chunked prefill slices long prompts so decode tokens never starve. Turn all three on and a Llama 3.3 70B FP8 on one H100 SXM5 pushes 2,200-2,400 tok/s at 128 concurrent — roughly 25% above vLLM's own default and 3-4x a naive PyTorch loop. This lesson reads the scheduler and attention kernel at a level you can diagram, and ends with a toy continuous batcher in `code/main.py` that schedules prefill and decode the way vLLM does.

> **【中文解读】** vLLM 在 2026 年的主导地位基于三个复合优化：PagedAttention（分页注意力）始终开启；连续批处理在解码迭代间注入新请求；分块预填充切片长提示以防止解码 Token 饥饿。三者全开时，Llama 3.3 70B FP8 在单卡 H100 上以 128 并发达到 2,200-2,400 tok/s——比朴素 PyTorch 循环快 3-4 倍。

> **【拓展：vLLM → LLM 推理服务标准】** vLLM 是 2026 年最流行的开源 LLM 推理服务引擎。PagedAttention 借鉴操作系统的虚拟内存分页思想管理 KV Cache，将碎片率控制在 4% 以下。连续批处理允许在解码步骤间动态加入新请求，大幅提升 GPU 利用率。这是生产环境部署 LLM 的必学技术。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy continuous batching scheduler) | **语言:** Python（标准库，连续批处理调度器模拟）
**Prerequisites:** Phase 17 · 01 (Model Serving), Phase 11 (LLM Engineering) | **前置知识:** Phase 17 · 01（模型服务）, Phase 11（LLM 工程）
**Time:** ~75 minutes | **时间:** ~75 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 11·12（推理优化基础）、KV cache 概念、连续批处理。vLLM 是 2026 开源推理引擎的事实标准。
> 💡 **【类比】** vLLM 三件套 = "高效餐厅厨房"。PagedAttention = 分块管理 KV cache（像操作系统虚拟内存分页，碎片率 < 4%）；Continuous Batching = 动态拼单（新请求随时插入运行 batch）；Chunked Prefill = 切长 prompt（长输入切片避免阻塞解码）。Llama 3.3 70B FP8 在 H100 上 128 并发达 2200-2400 tok/s，比朴素实现快 3-4 倍。

## Learning Objectives | 学习目标

- Explain PagedAttention as a KV cache allocator: blocks, block tables, and why fragmentation stays under 4% at production load.
  中文翻译：将 PagedAttention 解释为 KV 缓存分配器：块、块表，以及为什么在生产负载下碎片率保持在 4% 以下。
- Diagram continuous batching at the iteration level: how finished sequences leave the batch and new ones join without draining.
  中文翻译：在迭代级别绘制连续批处理：已完成的序列如何离开批次，新序列如何加入而无需清空。
- Describe chunked prefill in one sentence and name which latency metric it protects (hint: it is TTFT tail, not mean throughput).
  中文翻译：用一句话描述分块预填充，并说出它保护哪个延迟指标（提示：是 TTFT 尾部，而非平均吞吐量）。
- Name the 2026 vLLM v0.18.0 gotcha that bites teams enabling every optimization at once.
  中文翻译：说出 2026 年 vLLM v0.18.0 中同时启用所有优化的团队会遇到的问题。

## The Problem | 问题引入

> **【中文解读】** 朴素 PyTorch 服务循环一次处理一个请求。静态批处理将所有请求填充到最长序列，浪费 GPU 资源并让快请求等待慢请求。vLLM 通过三个核心优化解决此问题：PagedAttention（KV Cache 碎片率从 60-80% 降到 4% 以下）、连续批处理（在解码迭代间动态加入新请求）、分块预填充（将长提示切片以防止解码饥饿）。

A naive PyTorch serve loop runs one request at a time: tokenize, prefill, decode until EOS, return. At one user this works. At one hundred, it is a queue of patient people. The obvious fix — static batching — pads every request to the longest prompt in the window, pads every decode to the longest expected output, and stalls the whole batch on the slowest sequence. You pay for padding you never use, and fast requests wait for slow ones.

> 朴素 PyTorch 服务循环一次处理一个请求：分词、预填充、解码直到 EOS、返回。一个用户时这行得通。一百个用户时，这就是一排耐心等待的人。显而易见的修复——静态批处理——将每个请求填充到窗口中最长的提示，将每个解码填充到最长预期输出，整个批次等待最慢的序列。你为从未使用的填充买单，快请求等待慢请求。

vLLM solves three problems at once. PagedAttention stops KV cache fragmentation from eating 60-80% of GPU memory the way classic contiguous allocation does. Continuous batching lets requests join and leave the batch between each decode iteration, so the batch is always full of real work. Chunked prefill breaks a 32k-token prompt into ~512-token slices that interleave with decode, so a long prompt does not freeze every decode token on the GPU.

> vLLM 一次解决三个问题。PagedAttention 阻止 KV 缓存碎片像经典连续分配那样吞噬 60-80% 的 GPU 内存。连续批处理让请求在每个解码迭代之间加入和离开批次，所以批次总是充满真实工作。分块预填充将 32K token 的提示切成约 512 token 的片段，与解码交错进行，所以长提示不会冻结 GPU 上的每个解码 token。

The 2026 production default is all three on. You need to understand what each one does because the failure modes are all on the scheduler, not the model.

> 2026 年的生产默认设置是三个都开。你需要了解每个做什么，因为故障模式都在调度器上，而非模型上。

## The Concept | 核心概念

### PagedAttention as a virtual memory system

> **【中文解读】** PagedAttention 借鉴操作系统虚拟内存分页思想管理 KV Cache。传统连续分配为每个序列预分配最大长度（如 8192 tokens），但平均请求只用 1500 tokens，浪费 82% 的 HBM。PagedAttention 将 KV Cache 分为固定大小的块（默认 16 tokens），每个序列有一个块表映射逻辑位置到物理块 ID，按需分配，碎片率低于 4%。这是 vLLM 唯一的分配器，通过 `--gpu-memory-utilization`（默认 0.9）控制 KV Cache 可用的 HBM 比例。

> **【拓展：KV Cache 内存管理演进】** KV Cache 内存管理经历了三代演进：(1) 连续预分配——简单但浪费 60-80% 内存；(2) PagedAttention（vLLM 2023）——分页管理，碎片率 <4%，成为行业标准；(3) RadixAttention（SGLang 2024）——在前缀共享场景下进一步优化，通过 radix tree 索引实现跨请求的 KV 复用。在 70B 模型 128 并发的生产负载下，PagedAttention 相比连续分配可节省 50-70% 的 GPU 内存。

A KV cache is `num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element` per sequence. For Llama 3.3 70B at 8192 tokens, that is roughly 1.25 GB per sequence in BF16. If you pre-reserve 8192 slots for every request but the average request only uses 1500 tokens, you waste roughly 82% of the HBM you reserved. Classic batching pays this waste.

> 每个序列的 KV 缓存大小为 `num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element`。Llama 3.3 70B 在 8192 token 时，BF16 下每个序列约 1.25 GB。如果你为每个请求预预留 8192 个槽位，但平均请求只用 1500 个 token，你浪费了约 82% 预留的 HBM。经典批处理承担了这种浪费。

PagedAttention borrows the idea from OS virtual memory. KV cache is not contiguous per sequence. It is allocated in fixed-size blocks (default 16 tokens). Each sequence has a block table that maps its logical token positions to physical block IDs. When a sequence grows past its allocated blocks, one more block is added. When it finishes, its blocks return to the pool.

> PagedAttention 借鉴操作系统虚拟内存的思想。KV 缓存不是每个序列连续的。它以固定大小的块（默认 16 token）分配。每个序列有一个块表，将逻辑 token 位置映射到物理块 ID。当序列增长超过已分配块时，添加一个新块。完成后，块返回池中。

Fragmentation drops from 60-80% (classic) to under 4% (PagedAttention). You do not enable PagedAttention with a flag — it is the only allocator vLLM ships. The knob is `--gpu-memory-utilization` (default 0.9), which tells vLLM how much HBM to reserve for KV blocks after loading weights and activations.

> 碎片率从 60-80%（经典）降到 4% 以下（PagedAttention）。你不需要用标志启用 PagedAttention——它是 vLLM 唯一的分配器。旋钮是 `--gpu-memory-utilization`（默认 0.9），告诉 vLLM 在加载权重和激活后为 KV 块预留多少 HBM。

### Continuous batching at the iteration level

> **【中文解读】** 连续批处理在每个解码步骤之间做出接纳/释放决策。每个迭代：(1) 移除已完成（EOS 或 max_tokens）的序列；(2) 检查等待队列，如果有空闲 KV 块则接纳新序列；(3) 对 RUNNING 列表中的所有序列执行一次前向传播。批次大小不固定，不同输出位置的序列共享同一次融合前向计算。2026 年 vLLM V1 调度器的核心不变量是：调度器每个解码迭代运行一次，而非每个请求运行一次。

The old "dynamic batching" waited for a window (say 10 ms) to fill a batch, then ran prefill + decode + decode + decode until every sequence finished. Fast sequences left early and sat idle while the GPU finished the slow ones.

> 旧的"动态批处理"等待一个窗口（如 10ms）来填充批次，然后运行 prefill + decode + decode + decode 直到每个序列完成。快序列早早完成然后空闲，而 GPU 完成慢序列。

Continuous batching operates between each decode step. Call the set of running sequences the `RUNNING` list. At each iteration:

> 连续批处理在每个解码步骤之间操作。将运行中的序列集合称为 `RUNNING` 列表。每次迭代：

1. Any sequence in `RUNNING` that just hit EOS or max_tokens is removed.
   中文翻译：`RUNNING` 中刚达到 EOS 或 max_tokens 的任何序列被移除。
2. The scheduler looks at the waiting queue. If there are free KV blocks, it admits new sequences (prefill or resumed).
   中文翻译：调度器查看等待队列。如果有空闲 KV 块，它接纳新序列（预填充或恢复）。
3. The forward pass runs on whatever is now in `RUNNING`, emitting one new token per sequence.
   中文翻译：前向传播对 `RUNNING` 中的所有内容运行，每个序列发出一个新 token。

The batch size is never padded to a fixed number. Sequences at different positions in their output share one fused forward. In 2026 vLLM this is called the `V1 scheduler`. The key invariant: the scheduler runs once per decode iteration, not once per request.

> 批次大小从不填充到固定数字。输出不同位置的序列共享一次融合前向传播。2026 年 vLLM 中这称为 `V1 scheduler`。关键不变量：调度器每个解码迭代运行一次，而非每个请求运行一次。

### Chunked prefill protects TTFT tail

> **【中文解读】** 分块预填充解决了长提示"冻结"其他序列解码的问题。一个 32K token 的提示在 70B 模型上需要约 800ms 的纯 prefill 计算，期间所有其他序列的解码 token 都在等待。分块预填充将 prefill 切成固定大小的块（默认 512 tokens），每个块之间调度器可以推进其他序列的解码。代价是 prefill 延迟增加几毫秒，但 P99 ITL 从约 50ms 降到约 15ms——这是用户体验的关键改善。

> **【拓展：vLLM 生产部署最佳实践】** 2026 年 vLLM 生产部署的关键配置包括：(1) `--gpu-memory-utilization 0.9`——预留 90% HBM 给 KV Cache；(2) `--max-model-len` 根据实际需求设置而非默认最大值；(3) 分块预填充默认开启但与某些推测解码模式不兼容；(4) `--enable-prefix-caching` 在 RAG/Agent 场景下可大幅减少重复 prefill；(5) Prometheus 指标端点用于监控队列深度和 KV 利用率。

Prefill is compute-bound. A 32k-token prompt on Llama 3.3 70B takes ~800 ms of pure prefill on one H100. While prefill runs, decode tokens for every other sequence in the batch wait. In a serving loop, the first-token latency (TTFT) of one long prompt becomes the inter-token latency (ITL) blip for dozens of other users.

> 预填充是计算密集型的。Llama 3.3 70B 上一个 32K token 的提示在单卡 H100 上需要约 800ms 的纯预填充。预填充运行时，批次中所有其他序列的解码 token 都在等待。在服务循环中，一个长提示的首 token 延迟（TTFT）变成了几十个其他用户的 token 间延迟（ITL）毛刺。

Chunked prefill splits prefill into fixed-size chunks (default 512 tokens) and schedules each chunk as a unit. Between chunks the scheduler can advance decode sequences by one token. You trade a small absolute prefill latency hit (a few ms per chunk) for much lower decode-time jitter. P99 ITL under mixed load drops from ~50 ms to ~15 ms in published benchmarks.

> 分块预填充将预填充切分成固定大小的块（默认 512 token），每个块作为调度单元。在块之间，调度器可以推进解码序列一个 token。你用少量绝对预填充延迟损失（每块几毫秒）换取低得多的解码时间抖动。混合负载下 P99 ITL 从约 50ms 降到约 15ms。

### The three defaults interact

All three features assume each other. PagedAttention gives the scheduler a fine-grained KV resource to trade against. Continuous batching needs that fine-grained resource so admitting a new sequence does not force a global reshuffle. Chunked prefill is a decision the scheduler makes on the same `RUNNING` list — it is one more scheduler policy, not a separate system.

> 三个特性相互依赖。PagedAttention 为调度器提供了细粒度的 KV 资源来调配。连续批处理需要这种细粒度资源，这样接纳新序列不需要全局重排。分块预填充是调度器在同一个 `RUNNING` 列表上做出的决策——它是又一个调度策略，不是独立系统。

You do not need to know every flag. You need to know what the scheduler optimizes: goodput under KV-block budget, subject to chunked prefill slicing.

> 你不需要知道每个标志。你需要知道调度器优化什么：KV 块预算下的 goodput，受分块预填充切片约束。

### The 2026 v0.18.0 gotcha

> **【中文解读】** vLLM v0.18.0 中不能同时启用 `--enable-chunked-prefill` 和 draft-model 推测解码（`--speculative-model`）。唯一的例外是 V1 调度器中的 N-gram GPU 推测解码。不阅读发布说明就开启所有优化标志的团队会在启动时遇到运行时错误，而非软性退化。如果推测解码的收益值得开启分块预填充，2026 年的正确答案通常是 EAGLE-3 而非 draft model。

In vLLM v0.18.0 you cannot combine `--enable-chunked-prefill` with draft-model speculative decoding (`--speculative-model`). The documented exception is N-gram GPU speculative decoding in the V1 scheduler. Teams that flip every flag on without reading the release notes get a run-time error at startup, not a soft regression. If your speculative gain was worth enabling chunked prefill for, revisit the choice — the right answer in 2026 is often EAGLE-3 without chunked prefill, not a draft model plus chunked prefill that does not compile.

> 在 vLLM v0.18.0 中，你不能同时启用 `--enable-chunked-prefill` 和 draft-model 推测解码（`--speculative-model`）。文档记录的例外是 V1 调度器中的 N-gram GPU 推测解码。不阅读发布说明就开启所有标志的团队在启动时遇到运行时错误而非软性退化。如果推测解码的收益值得开启分块预填充，重新审视选择——2026 年的正确答案通常是 EAGLE-3 而非 draft model。

### Numbers you should remember

- Llama 3.3 70B FP8, H100 SXM5, 128 concurrent, all three on: 2,200-2,400 tok/s.
  中文翻译：Llama 3.3 70B FP8，H100 SXM5，128 并发，三个优化全开：2,200-2,400 tok/s。
- Same model, default vLLM (no chunked prefill): ~1,800 tok/s.
  中文翻译：同模型，默认 vLLM（无分块预填充）：约 1,800 tok/s。
- Same model, naive PyTorch forward loop: ~600 tok/s.
  中文翻译：同模型，朴素 PyTorch 前向循环：约 600 tok/s。
- KV fragmentation waste under PagedAttention at production load: <4%.
  中文翻译：PagedAttention 在生产负载下的 KV 碎片浪费：<4%。
- P99 ITL under mixed load: ~15 ms with chunked prefill, ~50 ms without.
  中文翻译：混合负载下 P99 ITL：有分块预填充约 15ms，无约 50ms。

### What the scheduler looks like

```
while True:
    finished = [s for s in RUNNING if s.is_done()]
    for s in finished: release_blocks(s); RUNNING.remove(s)

    while WAITING and have_free_blocks_for(WAITING[0]):
        s = WAITING.pop(0)
        allocate_initial_blocks(s)
        RUNNING.append(s)

    # schedule prefill chunks + decode in one batch
    batch = []
    for s in RUNNING:
        if s.in_prefill:
            batch.append(next_prefill_chunk(s))   # e.g. 512 tokens
        else:
            batch.append(decode_one_token(s))     # 1 token

    run_forward(batch)                            # one fused GPU call
```

`code/main.py` is exactly this loop in stdlib Python with fake token counts and fake forward latency. Running it shows how chunked prefill keeps decode sequences alive during a long prefill.

> `code/main.py` 正是这个循环的纯标准库 Python 实现，使用虚假 token 计数和虚假前向延迟。运行它可以看到分块预填充如何在长预填充期间保持解码序列活跃。

## Use It | 用框架实现

`code/main.py` simulates a vLLM-style scheduler with toggleable features. Run it to see:

> `code/main.py` 模拟一个带有可切换功能的 vLLM 风格调度器。运行它可以看到：

- `NAIVE` mode: one request at a time, no batching.
  中文翻译：`NAIVE` 模式：一次一个请求，无批处理。
- `STATIC` mode: pad and wait, classic batching.
  中文翻译：`STATIC` 模式：填充并等待，经典批处理。
- `CONTINUOUS` mode: iteration-level admission and release.
  中文翻译：`CONTINUOUS` 模式：迭代级别的接纳和释放。
- `CONTINUOUS + CHUNKED` mode: prefill slices interleaved with decode.
  中文翻译：`CONTINUOUS + CHUNKED` 模式：预填充切片与解码交错。

The output shows total throughput (tokens per virtual second), TTFT mean, and P99 ITL. The `CONTINUOUS + CHUNKED` row should dominate on mixed traffic.

> 输出显示总吞吐量（每虚拟秒 token 数）、TTFT 均值和 P99 ITL。`CONTINUOUS + CHUNKED` 行在混合流量下应占主导。

## Ship It | 产出物

> **【拓展：LLM 推理引擎对比】** 2026 年主流开源 LLM 推理引擎包括：vLLM（通用生产默认，PagedAttention+连续批处理）、SGLang（前缀共享优化，RadixAttention）、TensorRT-LLM（NVIDIA 专属，Blackwell 上吞吐最高）、llama.cpp（CPU/边缘，GGUF 格式）。选择取决于硬件（CPU/GPU/Hopper/Blackwell）、工作负载（通用聊天/Agent/RAG）和合规要求（自托管/云托管）。vLLM 占据约 60% 的生产部署份额（2026 Canonical AI 基础设施调查）。

This lesson produces `outputs/skill-vllm-scheduler-reader.md`. Given a serving config (batch size, KV memory utilization, chunked prefill size, speculative config), it produces a scheduler diagnosis that names which of the three defaults is bottlenecking and what to tune.

> 本课产出 `outputs/skill-vllm-scheduler-reader.md`。给定服务配置（批次大小、KV 内存利用率、分块预填充大小、推测配置），它生成调度器诊断，指出三个默认中哪个是瓶颈以及如何调优。

## Exercises | 练习题

1. Run `code/main.py`. Compare `STATIC` to `CONTINUOUS` on a workload with mixed short and long requests. Where does the throughput gap come from — prefill efficiency, decode efficiency, or tail latency?
   中文翻译：运行 `code/main.py`。在混合长短请求的工作负载上比较 `STATIC` 和 `CONTINUOUS`。吞吐量差距从何而来——预填充效率、解码效率还是尾部延迟？
2. Modify the toy scheduler to add `--max-num-batched-tokens`. What is the right value for an H100 running Llama 3.3 70B FP8? (Hint: it is a function of KV block size and number of free blocks, not raw HBM.)
   中文翻译：修改模拟调度器添加 `--max-num-batched-tokens`。H100 运行 Llama 3.3 70B FP8 的正确值是多少？（提示：是 KV 块大小和空闲块数的函数，而非原始 HBM。）
3. Re-read the vLLM v0.18.0 release notes. Which combinations of flags are mutually exclusive? List them.
   中文翻译：重新阅读 vLLM v0.18.0 发布说明。哪些标志组合互斥？列出它们。
4. Compute the KV cache fragmentation waste for a trace of 1,000 requests with mean 1,500 output tokens, std 600 tokens, under (a) contiguous per-request allocation at 8192 max, (b) PagedAttention with 16-token blocks.
   中文翻译：计算 1,000 个请求的 KV 缓存碎片浪费（均值 1,500 输出 token，标准差 600），在 (a) 最大 8192 的连续每请求分配和 (b) 16-token 块的 PagedAttention 下。
5. Explain in one paragraph why chunked prefill helps P99 ITL but not throughput in isolation. Where does the throughput win come from in practice?
   中文翻译：用一段话解释为什么分块预填充帮助 P99 ITL 但不单独提升吞吐量。实际中吞吐量提升从何而来？

## Key Terms | 术语速查表

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| PagedAttention | "the KV trick" / "KV 技巧" | Fixed-size block allocator for KV cache; fragmentation <4% / KV 缓存的固定大小块分配器；碎片率 <4% |
| Block table | "the page table" / "页表" | Per-sequence map from logical token position to physical KV block / 每序列的逻辑 token 位置到物理 KV 块的映射 |
| Continuous batching | "dynamic batching, but right" / "正确的动态批处理" | Admit/release decisions made every decode iteration / 每个解码迭代做出接纳/释放决策 |
| Chunked prefill | "prefill splitting" / "预填充切片" | Break long prefill into 512-token slices interleaved with decode / 将长预填充切为 512 token 片段与解码交错 |
| TTFT | "first token time" / "首 token 时间" | Prefill + queue + network; dominated by prefill at long prompts / 预填充+队列+网络；长提示时由预填充主导 |
| ITL | "inter-token latency" / "token 间延迟" | Time between consecutive decode tokens; dominated by batch size / 连续解码 token 之间的时间；由批次大小主导 |
| Goodput | "throughput that meets SLO" / "满足 SLO 的吞吐量" | Tokens/sec where every request still hit TTFT and ITL targets / 每秒 token 数，每个请求仍满足 TTFT 和 ITL 目标 |
| V1 scheduler | "the new scheduler" / "新调度器" | vLLM's 2026 scheduler; N-gram spec decode is the chunked-prefill-compatible path / vLLM 2026 调度器；N-gram 推测解码与分块预填充兼容 |
| `--gpu-memory-utilization` | "the memory knob" / "内存旋钮" | Fraction of HBM reserved for KV blocks after weights and activations / 加载权重和激活后为 KV 块预留的 HBM 比例 |

## Further Reading | 延伸阅读

- [vLLM documentation — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode/) — official source on chunked-prefill and speculative-decoding compatibility.
- [vLLM Release Notes (NVIDIA)](https://docs.nvidia.com/deeplearning/frameworks/vllm-release-notes/index.html) — 2026 release cadence and version-specific behavior.
- [vLLM Blog — PagedAttention](https://blog.vllm.ai/2023/06/20/vllm.html) — the original write-up that still defines how to think about the allocator.
- [PagedAttention paper (arXiv:2309.06180)](https://arxiv.org/abs/2309.06180) — fragmentation analysis and scheduler design.
- [Aleksa Gordic — Inside vLLM](https://www.aleksagordic.com/blog/vllm) — detailed V1 scheduler walkthrough with flame graphs.
