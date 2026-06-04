# KV Cache, Flash Attention & Inference Optimization | KV Cache、Flash Attention 与推理优化

> 训练是并行的、受 FLOP 限制的。推理是串行的、受内存限制的。不同的瓶颈，不同的技巧。

> **【中文解读】** KV Cache 缓存已计算的 Key/Value 避免重复计算，是 LLM 推理加速的核心。Flash Attention 优化显存访问模式，减少显存使用。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 7 · 02（自注意力），阶段 7 · 05（完整 Transformer），阶段 7 · 07（GPT）
**时长：** 约 75 分钟

## 问题引入

朴素的 自回归解码器生成 `N` 个 token 需要 `O(N²)` 的工作量：每一步它重新计算整个前缀的注意力。对于 4K-token 的响应，那是 16M 次注意力操作，其中大部分是冗余的。每个前缀 token 的隐藏状态一旦计算就是确定的——你只需要用新 token 的查询与之前缓存的所有键和值计算注意力。

除此之外，注意力本身移动大量数据。标准注意力实例化一个 N×N 分数矩阵、N×d softmax 输出、N×d 最终输出——对 HBM 的读写太多。对于 N>=2K，注意力在成为 FLOP 瓶颈之前就成为内存瓶颈。经典注意力内核对现代 GPU 的利用率低 4-10 倍。

两项优化，均来自 Dao 等人，将前沿推理从"慢"推向"快"：

1. **KV 缓存。** 存储每个前缀 token 的 K 和 V 向量。每个新 token 的注意力是对缓存键的一次查询。推理从每步 `O(N²)` 降到 `O(N)`。
2. **Flash Attention。** 对注意力计算进行分块，使完整的 N×N 矩阵不触及 HBM。所有 softmax + 矩阵乘法都在 SRAM 中完成。A100 上 2-4 倍时间加速；H100 上使用 FP8 达 5-10 倍。

到 2026 年，两者都是通用的。每个生产推理栈（vLLM、TensorRT-LLM、SGLang、llama.cpp）都假设它们存在。每个前沿模型都启用 Flash Attention 发布。

> **【中文解读】** 推理优化的两大核心技术：KV Cache 存储已计算的 Key/Value 向量，避免重复计算，将每步推理从 O(N^2) 降到 O(N)；Flash Attention 通过分块计算避免 N×N 矩阵写入 HBM，在 SRAM 中完成所有计算，速度提升 2-10 倍。

## 核心概念

![KV 缓存增长和 Flash Attention 分块](../assets/kv-cache-flash-attn.svg)

### KV 缓存数学

每个解码器层，每个 token，每个头：

```
bytes_per_token_per_layer = 2 * d_head * dtype_size
                          ^
                          K 和 V
```

对于一个 7B 模型，32 层，32 头，d_head=128，fp16：

```
每 token 每层 = 2 * 128 * 2 = 512 字节
每 token（32 层） = 16 KB
每 32K 上下文 = 512 MB
```

> **【拓展：GQA 对 KV 缓存的影响】** GQA（Grouped-Query Attention）将 KV 头从 n_heads 减少到 n_kv_heads，直接等比例缩小 KV 缓存。例如 Llama 3 70B 的 64 查询头 / 8 KV 头配置，将 KV 缓存压缩了 8 倍。在 128K 上下文中，这意味着从约 4 GB 降到 0.5 GB 的 KV 缓存，是长上下文推理的关键优化。

对于 Llama 3 70B（80 层，d_head=128，GQA 有 8 个 KV 头）：

```
每 token 每层 = 2 * 8 * 128 * 2 = 4096 字节（4 KB）
每 32K 上下文 = 10.4 GB
```

这 10 GB 就是为什么 Llama 3 70B 在 128K 上下文时仅 KV 缓存就需要 40 GB A100 的大部分。

**GQA 是 KV 缓存的胜利。** MHA 有 64 头时会是 32 GB。MLA 压缩得更进一步。

### Flash Attention——分块技巧

标准注意力：

```
S = Q @ K^T          （HBM 读取，N×N，HBM 写入）
P = softmax(S)       （HBM 读取，HBM 写入）
O = P @ V            （HBM 读取，HBM 写入）
```

三次 HBM 往返。在 H100 上，HBM 带宽是 3 TB/s；SRAM 是 30 TB/s。每次 HBM 往返都比保持在芯片上慢 10 倍。

Flash Attention：

```
对于 Q 的每个块（tile 大小约 128 × 128）：
    将 Q_tile 加载到 SRAM
    对于 K、V 的每个块：
        将 K_tile、V_tile 加载到 SRAM
        计算 S_tile = Q_tile @ K_tile^T     （SRAM）
        运行 softmax 聚合                   （SRAM）
        累加到 O_tile                       （SRAM）
    将 O_tile 写入 HBM
```

每个 tile 一次 HBM 往返。总内存占用从 `O(N²)` 降到 `O(N)`。反向传播从前向传播中重计算一些值而不是存储它们——另一个内存胜利。

**数值技巧。** 运行 softmax 跨 tile 维护 `(max, sum)`，使最终归一化精确。不是近似——Flash Attention 计算与标准注意力位相同 的输出（除了 fp16 非结合性）。

> **【中文解读】** Flash Attention 的核心技巧：将注意力计算分块（tiling），在 GPU 的快速 SRAM 中完成 softmax 和矩阵乘法，避免将 N×N 的中间矩阵写入慢速 HBM。关键数值技巧是"运行时 softmax"——跨 tile 维护 (max, sum) 对，确保最终结果与标准注意力数学上完全一致，不是近似。

> **【拓展：vLLM 的 PagedAttention】** PagedAttention（vLLM）将 KV 缓存组织为固定大小的"页"，类似操作系统的虚拟内存。这消除了内存碎片问题，使得多个并发请求可以高效共享 GPU 显存。配合连续批处理（continuous batching），vLLM 将 LLM 推理吞吐量提升了 2-4 倍，成为 2024-2026 年最流行的推理框架。

**版本演进：**

| 版本 | 年份 | 关键变化 | 参考硬件上的加速 |
|------|------|---------|-----------------|
| Flash 1 | 2022 | 分块 SRAM 内核 | A100 上 2× |
| Flash 2 | 2023 | 更好的并行性，因果优先排序 | A100 上 3× |
| Flash 3 | 2024 | Hopper 异步，FP8 | H100 上 1.5-2×（约 740 TFLOPs FP16） |
| Flash 4 | 2026 | Blackwell 5 级流水线，软件 exp2 | 推理优先（最初仅前向） |

Flash 4 在发布时仅支持前向传播。训练仍使用 Flash 3。Flash 4 的 GQA 和 varlen 支持尚待完成（2026 年中）。

### 推测解码——另一个延迟胜利

廉价模型提出 N 个 token。大模型并行验证所有 N 个。如果验证接受 k 个 token，你花了 1 次大模型前向传播获得了 k 次生成。典型 k=3-5（代码和散文）。

2026 年默认：
- **EAGLE 2 / Medusa。** 共享验证器隐藏状态的集成草案头。2-3 倍加速，无质量损失。
- **带草案模型的推测解码。** 消费级硬件上 2-4 倍加速。
- **Lookahead 解码。** Jacobi 迭代；不需要草案模型。小众但免费。

### 连续批处理

经典批量推理：等待最慢的序列完成，然后开始新批次。短响应提前完成时浪费 GPU。

连续批处理（首先在 Orca 中发布，现在在 vLLM、TensorRT-LLM、SGLang 中）：旧请求完成时立即将新请求换入批次。典型聊天工作负载的 5-10 倍吞吐量提升。

### PagedAttention——KV 缓存即虚拟内存

vLLM 的核心功能。KV 缓存以 16-token 块分配；页表将逻辑位置映射到物理块。让你可以在并行采样（束搜索、并行采样）之间共享 KV，热交换前缀用于提示缓存，以及碎片整理内存。相比朴素连续分配的 4 倍吞吐量提升。

## 动手实现

参见 `code/main.py`。我们实现：

1. 一个朴素的 `O(N²)` 增量解码器。
2. 一个 `O(N)` KV 缓存解码器。
3. 一个模拟 Flash Attention 运行最大值算法的分块 softmax。

### 步骤 1：KV 缓存

```python
class KVCache:
    def __init__(self, n_layers, n_heads, d_head):
        self.K = [[[] for _ in range(n_heads)] for _ in range(n_layers)]
        self.V = [[[] for _ in range(n_heads)] for _ in range(n_layers)]

    def append(self, layer, head, k, v):
        self.K[layer][head].append(k)
        self.V[layer][head].append(v)

    def read(self, layer, head):
        return self.K[layer][head], self.V[layer][head]
```

简单：在每层、每头列表中持续追加每 token 的 K、V 向量。

### 步骤 2：分块 softmax

```python
def tiled_softmax_dot(q, K, V, tile=4):
    """Flash-attention 风格的 softmax(qK^T)V 带运行最大值/总和。"""
    m = float("-inf")
    s = 0.0
    out = [0.0] * len(V[0])
    for start in range(0, len(K), tile):
        k_block = K[start:start + tile]
        v_block = V[start:start + tile]
        scores = [sum(qi * ki for qi, ki in zip(q, k)) for k in k_block]
        new_m = max(m, *scores)
        exp_old = math.exp(m - new_m) if m != float("-inf") else 0.0
        exp_new = [math.exp(sc - new_m) for sc in scores]
        s = s * exp_old + sum(exp_new)
        for j in range(len(out)):
            out[j] = out[j] * exp_old + sum(e * v[j] for e, v in zip(exp_new, v_block))
        m = new_m
    return [o / s for o in out]
```

与一次性 `softmax(qK) V` 的输出位相同，但任何时候工作集都是 `tile × d_head` 块，而不是完整的 `N × d_head`。

### 步骤 3：比较朴素与缓存解码在 100-token 生成上

计算注意力操作数。朴素：`O(N²)` = 5050。缓存：`O(N)` = 100。代码打印两者。

## 用框架实现

```python
# HuggingFace transformers 在纯解码器 generate() 上自动启用 KV 缓存。
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    attn_implementation="flash_attention_2",  # 如果是 Hopper 则使用 FA3
    torch_dtype="bfloat16",
)
# generate() 自动使用 KV 缓存
```

vLLM 生产环境：

```bash
pip install vllm
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4 \
    --max-model-len 32768 \
    --enable-prefix-caching \
    --kv-cache-dtype fp8
```

跨请求的前缀缓存是 2026 年的一个重大胜利——相同的系统提示、少样本示例或长上下文文档跨调用重用 KV。对于有重复工具提示的代理工作负载，前缀缓存通常是 5 倍吞吐量提升。

## 产出物

参见 `outputs/skill-inference-optimizer.md`。该技能为新的推理部署选择注意力实现、KV 缓存策略、量化和推测解码。

## 练习题

1. **简单。** 运行 `code/main.py`。确认朴素和缓存解码器产生相同输出；注意操作数差异。
2. **中等。** 实现前缀缓存：给定一个提示 P 和多个补全，对 P 运行一次前向传播填充 KV 缓存，然后按补全分支。测量与每个补全重新编码 P 相比的加速。
3. **困难。** 实现玩具 PagedAttention：固定 16-token 块的 KV 缓存带空闲列表。序列完成时将其块返回池。模拟 1,000 个变长聊天补全。比较与连续分配的内存碎片。

## 术语速查表

| 术语 | 人们的说法 | 实际含义 |
|------|-----------|---------|
| KV 缓存 | "让解码变快的技巧" | 存储每个前缀 token 的 K 和 V；新查询对它们做注意力而非重新计算。 |
| HBM | "GPU 主内存" | 高带宽内存；H100 上 80 GB，B200 上 192 GB。约 3 TB/s 带宽。 |
| SRAM | "片上内存" | 每 SM 的快速内存，H100 上每 SM 约 256 KB。约 30 TB/s 带宽。 |
| Flash Attention | "分块注意力内核" | 不将 N×N 实例化到 HBM 的情况下计算注意力。 |
| 连续批处理 | "不等待的批处理" | 完成的序列换出，新序列换入，无需排空批次。 |
| PagedAttention | "vLLM 的核心功能" | KV 缓存以固定块分配带页表；消除碎片。 |
| 前缀缓存 | "重用长提示" | 跨请求缓存共享前缀的 KV；代理的重大成本削减。 |
| 推测解码 | "草案 + 验证" | 廉价草案模型提出 token；大模型一次验证 k 个。 |

## 延伸阅读

- [Dao 等人（2022）。FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135) —— Flash 1。
- [Dao（2023）。FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691) —— Flash 2。
- [Shah 等人（2024）。FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](https://arxiv.org/abs/2407.08608) —— Flash 3。
- [FlashAttention-4 发布说明（Dao-AILab，2026）](https://github.com/Dao-AILab/flash-attention) —— Blackwell 5 级流水线和软件 exp2 技巧；阅读仓库 README 了解本课提到的仅前向发布注意事项。
- [Kwon 等人（2023）。Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) —— vLLM 论文。
- [Leviathan 等人（2023）。Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) —— 推测解码。
- [Li 等人（2024）。EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) —— EAGLE-1/2 论文，本课引用的集成草案方法。
- [Cai 等人（2024）。Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) —— 与 EAGLE 一起引用的 Medusa 方法。
- [vLLM 文档 — PagedAttention](https://docs.vllm.ai/en/latest/design/kernel/paged_attention.html) —— 16-token 块和页表设计的规范深入解析。
