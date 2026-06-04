# vLLM 推理服务内部机制：PagedAttention、连续批处理、分块预填充 | vLLM 推理服务内部机制

> vLLM 在 2026 年的主导地位基于三个复合默认设置，而非单一技巧。PagedAttention 始终开启。连续批处理在解码迭代之间注入新请求。分块预填充将长提示切片，使解码 token 永远不会饥饿。三者全部开启后，单卡 H100 上的 Llama 3.3 70B FP8 以 128 并发推送 2,200-2,400 tok/s——比 vLLM 自己的默认值高出约 25%，比朴素 PyTorch 循环快 3-4 倍。本课程以你可以图解的级别阅读调度器和注意力内核，并以 `code/main.py` 中的玩具连续批处理器结束，它按照 vLLM 的方式调度预填充和解码。

> **【中文解读】** vLLM 在 2026 年的主导地位基于三个复合优化：PagedAttention（分页注意力）始终开启；连续批处理在解码迭代间注入新请求；分块预填充切片长提示以防止解码 Token 饥饿。三者全开时，Llama 3.3 70B FP8 在单卡 H100 上以 128 并发达到 2,200-2,400 tok/s——比朴素 PyTorch 循环快 3-4 倍。

> **【拓展：vLLM → LLM 推理服务标准】** vLLM 是 2026 年最流行的开源 LLM 推理服务引擎。PagedAttention 借鉴操作系统的虚拟内存分页思想管理 KV Cache，将碎片率控制在 4% 以下。连续批处理允许在解码步骤间动态加入新请求，大幅提升 GPU 利用率。这是生产环境部署 LLM 的必学技术。

**类型：** 学习
**语言：** Python（标准库，模拟连续批处理调度器）
**前置条件：** Phase 17 · 01（模型服务），Phase 11（LLM 工程）
**时间：** 约 75 分钟

## 学习目标

- 将 PagedAttention 解释为 KV 缓存分配器：块、块表，以及为什么生产负载下碎片率保持在 4% 以下。
- 在迭代级别图解连续批处理：完成的序列如何离开批次，新的如何加入而无需排空。
- 用一句话描述分块预填充，并说出它保护哪个延迟指标（提示：是 TTFT 尾部，不是平均吞吐量）。
- 说出 2026 年 vLLM v0.18.0 中让团队同时启用所有优化时遇到的坑。

## 问题引入

> **【中文解读】** 朴素 PyTorch 服务循环一次处理一个请求。静态批处理将所有请求填充到最长序列，浪费 GPU 资源并让快请求等待慢请求。vLLM 通过三个核心优化解决此问题：PagedAttention（KV Cache 碎片率从 60-80% 降到 4% 以下）、连续批处理（在解码迭代间动态加入新请求）、分块预填充（将长提示切片以防止解码饥饿）。

朴素的 PyTorch 服务循环一次运行一个请求：分词、预填充、解码直到 EOS、返回。一个用户时这没问题。一百个用户时，这是一群耐心的人排队。显而易见的修复——静态批处理——将每个请求填充到窗口中最长的提示，将每个解码填充到最长的预期输出，并在最慢的序列上停滞整个批次。你为从未使用的填充付费，快请求等待慢请求。

vLLM 一次解决三个问题。PagedAttention 阻止 KV 缓存碎片像经典连续分配那样消耗 60-80% 的 GPU 内存。连续批处理让请求在每个解码迭代之间加入和离开批次，所以批次总是充满真正的工作。分块预填充将 32K token 的提示分解为约 512 token 的切片，与解码交替，所以长提示不会冻结 GPU 上的每个解码 token。

2026 年的生产默认值是三者全部开启。你需要理解每个做了什么，因为失败模式都在调度器上，而不是模型上。

## 核心概念

### PagedAttention 作为虚拟内存系统

> **【中文解读】** PagedAttention 借鉴操作系统虚拟内存分页思想管理 KV Cache。传统连续分配为每个序列预分配最大长度（如 8192 tokens），但平均请求只用 1500 tokens，浪费 82% 的 HBM。PagedAttention 将 KV Cache 分为固定大小的块（默认 16 tokens），每个序列有一个块表映射逻辑位置到物理块 ID，按需分配，碎片率低于 4%。这是 vLLM 唯一的分配器，通过 `--gpu-memory-utilization`（默认 0.9）控制 KV Cache 可用的 HBM 比例。

> **【拓展：KV Cache 内存管理演进】** KV Cache 内存管理经历了三代演进：(1) 连续预分配——简单但浪费 60-80% 内存；(2) PagedAttention（vLLM 2023）——分页管理，碎片率 <4%，成为行业标准；(3) RadixAttention（SGLang 2024）——在前缀共享场景下进一步优化，通过 radix tree 索引实现跨请求的 KV 复用。在 70B 模型 128 并发的生产负载下，PagedAttention 相比连续分配可节省 50-70% 的 GPU 内存。

一个 KV 缓存每个序列是 `num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element`。对于 8192 token 的 Llama 3.3 70B，BF16 下大约每序列 1.25 GB。如果你为每个请求预保留 8192 个槽位，但平均请求只使用 1500 个 token，你浪费了约 82% 的预留 HBM。经典批处理承担这个浪费。

PagedAttention 借鉴操作系统虚拟内存的思想。KV 缓存不是每个序列连续的。它以固定大小的块分配（默认 16 token）。每个序列有一个块表，将其逻辑 token 位置映射到物理块 ID。当序列增长超过其分配的块时，添加一个新块。当它完成时，其块返回到池中。

碎片从 60-80%（经典）降到 4% 以下（PagedAttention）。你不需要用标志启用 PagedAttention——它是 vLLM 唯一附带的分配器。旋钮是 `--gpu-memory-utilization`（默认 0.9），它告诉 vLLM 在加载权重和激活后为 KV 块保留多少 HBM。

### 迭代级别的连续批处理

> **【中文解读】** 连续批处理在每个解码步骤之间做出接纳/释放决策。每个迭代：(1) 移除已完成（EOS 或 max_tokens）的序列；(2) 检查等待队列，如果有空闲 KV 块则接纳新序列；(3) 对 RUNNING 列表中的所有序列执行一次前向传播。批次大小不固定，不同输出位置的序列共享同一次融合前向计算。2026 年 vLLM V1 调度器的核心不变量是：调度器每个解码迭代运行一次，而非每个请求运行一次。

旧的"动态批处理"等待一个窗口（比如 10 ms）来填充批次，然后运行预填充 + 解码 + 解码 + 解码直到每个序列完成。快序列提前离开并空闲等待，而 GPU 完成慢序列。

连续批处理在每个解码步骤之间操作。将运行中的序列集合称为 `RUNNING` 列表。在每次迭代中：

1. `RUNNING` 中刚刚达到 EOS 或 max_tokens 的任何序列被移除。
2. 调度器查看等待队列。如果有空闲的 KV 块，它接纳新序列（预填充或恢复的）。
3. 前向传播在 `RUNNING` 中的所有内容上运行，为每个序列发出一个新的 token。

批次大小从不填充到固定数量。不同输出位置的序列共享一次融合前向。在 2026 年的 vLLM 中，这被称为 `V1 调度器`。关键不变量：调度器每个解码迭代运行一次，而不是每个请求运行一次。

### 分块预填充保护 TTFT 尾部

> **【中文解读】** 分块预填充解决了长提示"冻结"其他序列解码的问题。一个 32K token 的提示在 70B 模型上需要约 800ms 的纯 prefill 计算，期间所有其他序列的解码 token 都在等待。分块预填充将 prefill 切成固定大小的块（默认 512 tokens），每个块之间调度器可以推进其他序列的解码。代价是 prefill 延迟增加几毫秒，但 P99 ITL 从约 50ms 降到约 15ms——这是用户体验的关键改善。

> **【拓展：vLLM 生产部署最佳实践】** 2026 年 vLLM 生产部署的关键配置包括：(1) `--gpu-memory-utilization 0.9`——预留 90% HBM 给 KV Cache；(2) `--max-model-len` 根据实际需求设置而非默认最大值；(3) 分块预填充默认开启但与某些推测解码模式不兼容；(4) `--enable-prefix-caching` 在 RAG/Agent 场景下可大幅减少重复 prefill；(5) Prometheus 指标端点用于监控队列深度和 KV 利用率。

预填充是计算受限的。Llama 3.3 70B 在一个 H100 上，32K token 的提示需要约 800ms 的纯预填充。在预填充运行时，批次中每个其他序列的解码 token 都在等待。在服务循环中，一个长提示的首 token 延迟（TTFT）成为几十个其他用户的 token 间延迟（ITL）毛刺。

分块预填充将预填充拆分为固定大小的块（默认 512 token），并将每个块作为一个单元调度。在块之间，调度器可以推进解码序列一个 token。你用少量绝对的预填充延迟命中（每个块几毫秒）换取低得多的解码时间抖动。在混合负载下，P99 ITL 从约 50ms 降到约 15ms。

### 三个默认值相互交互

三个特性都假设彼此存在。PagedAttention 给调度器一个细粒度的 KV 资源来交易。连续批处理需要那个细粒度的资源，所以接纳新序列不会强制全局重排。分块预填充是调度器在同一个 `RUNNING` 列表上做出的决策——它是一个额外的调度器策略，不是单独的系统。

你不需要知道每个标志。你需要知道调度器优化什么：在 KV 块预算下的 goodput，受分块预填充切片约束。

### 2026 年 v0.18.0 的坑

> **【中文解读】** vLLM v0.18.0 中不能同时启用 `--enable-chunked-prefill` 和 draft-model 推测解码（`--speculative-model`）。唯一的例外是 V1 调度器中的 N-gram GPU 推测解码。不阅读发布说明就开启所有优化标志的团队会在启动时遇到运行时错误，而非软性退化。如果推测解码的收益值得开启分块预填充，2026 年的正确答案通常是 EAGLE-3 而非 draft model。

在 vLLM v0.18.0 中，你不能将 `--enable-chunked-prefill` 与 draft-model 推测解码（`--speculative-model`）组合。文档记录的例外是 V1 调度器中的 N-gram GPU 推测解码。不阅读发布说明就打开每个标志的团队会在启动时遇到运行时错误，而不是软性退化。如果你的推测收益值得为分块预填充启用它，重新考虑这个选择——2026 年的正确答案通常是 EAGLE-3 不带分块预填充，而不是无法编译的 draft model 加分块预填充。

### 你应该记住的数字

- Llama 3.3 70B FP8，H100 SXM5，128 并发，三者全开：2,200-2,400 tok/s。
- 同一模型，默认 vLLM（无分块预填充）：约 1,800 tok/s。
- 同一模型，朴素 PyTorch 前向循环：约 600 tok/s。
- 生产负载下 PagedAttention 的 KV 碎片浪费：<4%。
- 混合负载下 P99 ITL：分块预填充约 15ms，无分块预填充约 50ms。

### 调度器是什么样的

```
while True:
    finished = [s for s in RUNNING if s.is_done()]
    for s in finished: release_blocks(s); RUNNING.remove(s)

    while WAITING and have_free_blocks_for(WAITING[0]):
        s = WAITING.pop(0)
        allocate_initial_blocks(s)
        RUNNING.append(s)

    # 在一个批次中调度预填充块 + 解码
    batch = []
    for s in RUNNING:
        if s.in_prefill:
            batch.append(next_prefill_chunk(s))   # 例如 512 个 token
        else:
            batch.append(decode_one_token(s))     # 1 个 token

    run_forward(batch)                            # 一次融合 GPU 调用
```

`code/main.py` 正是标准库 Python 中的这个循环，带有假 token 计数和假前向延迟。运行它可以看到分块预填充如何在长预填充期间保持解码序列存活。

## 用框架实现

`code/main.py` 模拟一个具有可切换功能的 vLLM 风格调度器。运行它可以看到：

- `NAIVE` 模式：一次一个请求，无批处理。
- `STATIC` 模式：填充和等待，经典批处理。
- `CONTINUOUS` 模式：迭代级别的接纳和释放。
- `CONTINUOUS + CHUNKED` 模式：预填充切片与解码交替。

输出显示总吞吐量（每虚拟秒 token 数）、TTFT 平均值和 P99 ITL。`CONTINUOUS + CHUNKED` 行应该在混合流量上占优。

## 产出物

> **【拓展：LLM 推理引擎对比】** 2026 年主流开源 LLM 推理引擎包括：vLLM（通用生产默认，PagedAttention+连续批处理）、SGLang（前缀共享优化，RadixAttention）、TensorRT-LLM（NVIDIA 专属，Blackwell 上吞吐最高）、llama.cpp（CPU/边缘，GGUF 格式）。选择取决于硬件（CPU/GPU/Hopper/Blackwell）、工作负载（通用聊天/Agent/RAG）和合规要求（自托管/云托管）。vLLM 占据约 60% 的生产部署份额（2026 Canonical AI 基础设施调查）。

本课程产出 `outputs/skill-vllm-scheduler-reader.md`。给定服务配置（批次大小、KV 内存利用率、分块预填充大小、推测配置），它产生一个调度器诊断，指出三个默认值中哪个是瓶颈以及应该调整什么。

## 练习题

1. 运行 `code/main.py`。在具有混合短请求和长请求的工作负载上比较 `STATIC` 和 `CONTINUOUS`。吞吐量差距从何而来——预填充效率、解码效率还是尾部延迟？
2. 修改玩具调度器添加 `--max-num-batched-tokens`。在 H100 上运行 Llama 3.3 70B FP8 的正确值是什么？（提示：它是 KV 块大小和空闲块数的函数，而不是原始 HBM。）
3. 重新阅读 vLLM v0.18.0 发布说明。哪些标志组合互斥？列出它们。
4. 计算在 (a) 最大 8192 的每请求连续分配下，(b) 16 token 块的 PagedAttention 下，1000 个请求的 KV 缓存碎片浪费（平均 1500 个输出 token，标准差 600）。
5. 用一段话解释为什么分块预填充有助于 P99 ITL 但不直接提升吞吐量。在实践中吞吐量的提升从何而来？

## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| PagedAttention | "KV 技巧" | KV 缓存的固定大小块分配器；碎片率 <4% |
| 块表 | "页表" | 每序列从逻辑 token 位置到物理 KV 块的映射 |
| 连续批处理 | "动态批处理，但是正确的" | 每个解码迭代做出的接纳/释放决策 |
| 分块预填充 | "预填充拆分" | 将长预填充分解为与解码交替的 512 token 切片 |
| TTFT | "首 token 时间" | 预填充 + 队列 + 网络；长提示时由预填充主导 |
| ITL | "token 间延迟" | 连续解码 token 之间的时间；由批次大小主导 |
| Goodput | "满足 SLO 的吞吐量" | 每秒 token 数，其中每个请求仍然满足 TTFT 和 ITL 目标 |
| V1 调度器 | "新调度器" | vLLM 的 2026 调度器；N-gram 推测解码是与分块预填充兼容的路径 |
| `--gpu-memory-utilization` | "内存旋钮" | 权重和激活后为 KV 块保留的 HBM 比例 |

## 延伸阅读

- [vLLM 文档 — 推测解码](https://docs.vllm.ai/en/latest/features/spec_decode/) — 分块预填充和推测解码兼容性的官方来源。
- [vLLM 发布说明 (NVIDIA)](https://docs.nvidia.com/deeplearning/frameworks/vllm-release-notes/index.html) — 2026 年发布节奏和特定版本行为。
- [vLLM 博客 — PagedAttention](https://blog.vllm.ai/2023/06/20/vllm.html) — 仍然定义如何思考分配器的原始文章。
- [PagedAttention 论文 (arXiv:2309.06180)](https://arxiv.org/abs/2309.06180) — 碎片分析和调度器设计。
- [Aleksa Gordic — 深入 vLLM](https://www.aleksagordic.com/blog/vllm) — 带有火焰图的详细 V1 调度器解析。
