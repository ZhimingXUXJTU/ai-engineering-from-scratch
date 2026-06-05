# KV Cache, Flash Attention & Inference Optimization | KV Cache、Flash Attention 与推理优化

> Training is parallel and FLOP-bound. Inference is serial and memory-bound. Different bottleneck, different tricks.

> **【中文解读】** KV Cache 缓存已计算的 Key/Value 避免重复计算，是 LLM 推理加速的核心。Flash Attention 优化显存访问模式，减少显存使用。

**Type:** Hands-on | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## The Problem | 问题引入

A naive autoregressive decoder does `O(N²)` work to generate `N` tokens: at each step it recomputes attention over the full prefix. For a 4K-token response that is 16M attention operations, most of them redundant. Every hidden state of a prefix token is deterministic once computed — you only need to run the new token's query against the cached keys and values of everything before.

> 一个朴素的自回归解码器生成 `N` 个 token 需要 `O(N²)` 的工作量：每一步都对完整前缀重新计算注意力。对于 4K token 的响应，那是 16M 次注意力操作，其中大部分是冗余的。前缀 token 的每个隐藏状态一旦计算就是确定性的——你只需用新 token 的查询与之前缓存的所有键和值做注意力。

On top of that, attention itself moves a lot of data. Standard attention materializes an N×N score matrix, N×d softmax output, N×d final output — too many reads and writes to HBM. For N≥2K, attention becomes memory-bound before it becomes FLOP-bound. Classic attention kernels underuse modern GPUs by 4–10×.

> 除此之外，注意力本身要移动大量数据。标准注意力会生成 N×N 分数矩阵、N×d softmax 输出、N×d 最终输出——对 HBM 的读写次数过多。当 N≥2K 时，注意力在成为 FLOP 瓶颈之前先成为内存瓶颈。经典注意力内核对现代 GPU 的利用率仅为 4-10 倍之差。

Two optimizations, both from Dao et al., pushed frontier inference from "slow" to "fast":

> 两个优化（都来自 Dao 等人）将前沿推理从"慢"推向"快"：

1. **KV cache.** Store the K and V vectors of every prefix token. Each new token's attention is one query against the cached keys. Inference reduces from `O(N²)` to `O(N)` per generation step.
   中文翻译：**KV 缓存。** 存储每个前缀 token 的 K 和 V 向量。每个新 token 的注意力是对缓存键的一次查询。推理从每步 `O(N²)` 降低到 `O(N)`。
2. **Flash Attention.** Tile the attention computation so the full N×N matrix never hits HBM. All of softmax + matmul happens in SRAM. 2–4× wall-clock speedup on A100; 5–10× on H100 with FP8.
   中文翻译：**Flash Attention。** 将注意力计算分块，使完整的 N×N 矩阵永远不写入 HBM。所有 softmax + 矩阵乘法都在 SRAM 中完成。A100 上 2-4 倍加速；H100 上 FP8 可达 5-10 倍。

By 2026 both are universal. Every production inference stack (vLLM, TensorRT-LLM, SGLang, llama.cpp) assumes them. Every frontier model ships with Flash Attention enabled.

> 到 2026 年，两者都已普及。每个生产推理栈（vLLM、TensorRT-LLM、SGLang、llama.cpp）都假设使用它们。每个前沿模型都默认启用 Flash Attention。

> **【中文解读】** 推理优化的两大核心技术：KV Cache 存储已计算的 Key/Value 向量，避免重复计算，将每步推理从 O(N^2) 降到 O(N)；Flash Attention 通过分块计算避免 N×N 矩阵写入 HBM，在 SRAM 中完成所有计算，速度提升 2-10 倍。

## The Concept | 核心概念

![KV cache growth and Flash Attention tiling](../assets/kv-cache-flash-attn.svg)

### KV cache math

Per decoder layer, per token, per head:

> 每个解码器层，每个 token，每个头：

```
bytes_per_token_per_layer = 2 * d_head * dtype_size
                          ^
                          K and V
```

For a 7B model with 32 layers, 32 heads, d_head=128, fp16:

> 对于 7B 模型（32 层、32 头、d_head=128、fp16）：

```
per token per layer = 2 * 128 * 2 = 512 bytes
per token (32 layers) = 16 KB
per 32K context = 512 MB
```

> **【拓展：GQA 对 KV 缓存的影响】** GQA（Grouped-Query Attention）将 KV 头从 n_heads 减少到 n_kv_heads，直接等比例缩小 KV 缓存。例如 Llama 3 70B 的 64 查询头 / 8 KV 头配置，将 KV 缓存压缩了 8 倍。在 128K 上下文中，这意味着从约 4 GB 降到 0.5 GB 的 KV 缓存，是长上下文推理的关键优化。

For Llama 3 70B (80 layers, d_head=128, GQA with 8 KV heads):

> 对于 Llama 3 70B（80 层、d_head=128、GQA 8 个 KV 头）：

```
per token per layer = 2 * 8 * 128 * 2 = 4096 bytes (4 KB)
per 32K context = 10.4 GB
```

That 10 GB is why Llama 3 70B at 128K context needs most of a 40 GB A100 just for KV cache at batch size 1.

> 这 10 GB 就是为什么 Llama 3 70B 在 128K 上下文下仅 KV 缓存（batch size 1）就需要大部分 40 GB A100 显存。

**GQA is the KV-cache win.** MHA with 64 heads would be 32 GB. MLA compresses even further.

> **GQA 是 KV 缓存的胜利。** 64 头的 MHA 需要 32 GB。MLA 压缩得更进一步。

### Flash Attention — the tiling trick

Standard attention:

> 标准注意力：

```
S = Q @ K^T          (HBM read, N×N, HBM write)
P = softmax(S)       (HBM read, HBM write)
O = P @ V            (HBM read, HBM write)
```

Three HBM round trips. On H100, HBM bandwidth is 3 TB/s; SRAM is 30 TB/s. Every HBM trip is a factor-of-10 slowdown vs keeping everything on-chip.

> 三次 HBM 往返。在 H100 上，HBM 带宽是 3 TB/s；SRAM 是 30 TB/s。每次 HBM 访问比在片上保持所有数据慢 10 倍。

Flash Attention:

```
for each block of Q (tile size ~128 × 128):
    load Q_tile into SRAM
    for each block of K, V:
        load K_tile, V_tile into SRAM
        compute S_tile = Q_tile @ K_tile^T     (SRAM)
        running softmax aggregation             (SRAM)
        accumulate into O_tile                  (SRAM)
    write O_tile to HBM
```

One HBM trip per tile. Total memory footprint drops from `O(N²)` to `O(N)`. Backward pass recomputes some values from the forward pass instead of storing them — another memory win.

> 每个 tile 一次 HBM 访问。总内存占用从 `O(N²)` 降到 `O(N)`。反向传播从前向传播中重新计算某些值而不是存储它们——又一个内存优势。

**Numerical trick.** Running softmax maintains `(max, sum)` across tiles so the final normalization is exact. Not an approximation — Flash Attention computes bit-identical output to standard attention (modulo fp16 non-associativity).

> **数值技巧。** 运行时 softmax 跨 tile 维护 `(max, sum)` 对，确保最终归一化是精确的。不是近似——Flash Attention 计算与标准注意力逐位相同的输出（除 fp16 非结合性外）。

> **【中文解读】** Flash Attention 的核心技巧：将注意力计算分块（tiling），在 GPU 的快速 SRAM 中完成 softmax 和矩阵乘法，避免将 N×N 的中间矩阵写入慢速 HBM。关键数值技巧是"运行时 softmax"——跨 tile 维护 (max, sum) 对，确保最终结果与标准注意力数学上完全一致，不是近似。

> **【拓展：vLLM 的 PagedAttention】** PagedAttention（vLLM）将 KV 缓存组织为固定大小的"页"，类似操作系统的虚拟内存。这消除了内存碎片问题，使得多个并发请求可以高效共享 GPU 显存。配合连续批处理（continuous batching），vLLM 将 LLM 推理吞吐量提升了 2-4 倍，成为 2024-2026 年最流行的推理框架。

**Version evolution:**

| Version | Year | Key change | Speedup on reference hardware |
|---------|------|-----------|-------------------------------|
| 版本 | 年份 | 关键变化 | 参考硬件上的加速 |
| Flash 1 | 2022 | Tiled SRAM kernel | 2× on A100 |
| Flash 2 | 2023 | Better parallelism, causal-first ordering | 3× on A100 |
| Flash 3 | 2024 | Hopper asynchrony, FP8 | 1.5–2× on H100 (~740 TFLOPs FP16) |
| Flash 4 | 2026 | Blackwell 5-stage pipeline, software exp2 | Inference-first (forward only initially) |

Flash 4 is forward-pass only at launch. Training still uses Flash 3. GQA and varlen support for Flash 4 is pending (mid-2026).

> Flash 4 发布时仅支持前向传播。训练仍使用 Flash 3。Flash 4 的 GQA 和变长支持待定（2026 年中）。

### Speculative decoding — the other latency win

Cheap model proposes N tokens. Big model verifies all N in parallel. If verification accepts k tokens, you paid 1 big-model forward pass for k generations. Typical k=3–5 on code and prose.

> 廉价模型提出 N 个 token。大模型并行验证所有 N 个。如果验证接受了 k 个 token，你用一次大模型前向传播获得了 k 个生成。代码和散文的典型 k=3-5。

2026 defaults:
- **EAGLE 2 / Medusa.** Integrated draft heads that share the verifier's hidden states. 2–3× speedup with no quality loss.
  中文翻译：**EAGLE 2 / Medusa。** 集成草案头，共享验证器的隐藏状态。2-3 倍加速，无质量损失。
- **Speculative decoding with draft model.** 2–4× speedup on consumer hardware.
  中文翻译：**带草案模型的推测解码。** 消费级硬件上 2-4 倍加速。
- **Lookahead decoding.** Jacobi iteration; no draft model needed. Niche but free.
  中文翻译：**前瞻解码。** Jacobi 迭代；不需要草案模型。小众但免费。

### Continuous batching

Classic batched inference: wait for the slowest sequence to finish, then start a new batch. Wastes GPU when short responses finish early.

> 经典批量推理：等待最慢的序列完成，然后开始新批次。短响应提前完成时浪费 GPU。

Continuous batching (first shipped in Orca, now in vLLM, TensorRT-LLM, SGLang): swap new requests into the batch as soon as old ones finish. 5–10× throughput gain for typical chat workloads.

> 连续批处理（首次在 Orca 中发布，现在在 vLLM、TensorRT-LLM、SGLang 中）：旧请求完成后立即将新请求换入批次。典型聊天工作负载的吞吐量提升 5-10 倍。

### PagedAttention — KV cache as virtual memory

vLLM's headline feature. KV cache is allocated in 16-token blocks; a page table maps logical positions to physical blocks. Lets you share KV across parallel samples (beam search, parallel sampling), hot-swap prefixes for prompt caching, and defragment memory. 4× throughput improvement over naive contiguous allocation.

> vLLM 的核心特性。KV 缓存以 16 token 块分配；页表将逻辑位置映射到物理块。允许跨并行样本（束搜索、并行采样）共享 KV，热交换前缀用于提示缓存，以及内存碎片整理。比朴素连续分配提升 4 倍吞吐量。

## Build It | 动手实现

See `code/main.py`. We implement:

> 参见 `code/main.py`。我们实现：

1. A naive `O(N²)` incremental decoder.
   中文翻译：一个朴素的 `O(N²)` 增量解码器。
2. A `O(N)` KV-cached decoder.
   中文翻译：一个 `O(N)` KV 缓存解码器。
3. A tiled softmax that simulates Flash Attention's running-max algorithm.
   中文翻译：一个模拟 Flash Attention 运行时最大值的分块 softmax。

### Step 1: KV cache

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

Simple: keep growing per-token K, V vectors in per-layer, per-head lists.

> 简单：在逐层、逐头的列表中持续追加每 token 的 K、V 向量。

### Step 2: tiled softmax

```python
def tiled_softmax_dot(q, K, V, tile=4):
    """Flash-attention-style softmax(qK^T)V with running max/sum."""
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

Bit-identical output to `softmax(qK) V` in one shot, but at any time the working set is a `tile × d_head` block, not the full `N × d_head`.

> 与一次性 `softmax(qK) V` 逐位相同的输出，但任何时候工作集只是 `tile × d_head` 块，而非完整的 `N × d_head`。

### Step 3: compare naive vs cached decoding on 100-token generation

Count attention operations. Naive: `O(N²)` = 5050. Cached: `O(N)` = 100. The code prints both.

> 计算注意力操作次数。朴素：`O(N²)` = 5050。缓存：`O(N)` = 100。代码会打印两者。

## Use It | 用框架实现

```python
# HuggingFace transformers auto-enables KV cache on decoder-only generate().
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    attn_implementation="flash_attention_2",  # use FA3 if Hopper
    torch_dtype="bfloat16",
)
# generate() uses KV cache automatically
```

vLLM production:

> vLLM 生产部署：

```bash
pip install vllm
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4 \
    --max-model-len 32768 \
    --enable-prefix-caching \
    --kv-cache-dtype fp8
```

Prefix caching across requests is a big 2026 win — the same system prompt, few-shot examples, or long context document reuses KV across calls. For agent workloads with repeated tool prompts, prefix caching is routinely 5× throughput gain.

> 跨请求的前缀缓存是 2026 年的重大胜利——相同的系统提示、少样本示例或长上下文文档在调用间复用 KV。对于有重复工具提示的代理工作负载，前缀缓存通常带来 5 倍吞吐量提升。

## Ship It | 产出物

See `outputs/skill-inference-optimizer.md`. The skill picks attention implementation, KV cache strategy, quantization, and speculative decoding for a new inference deployment.

> 参见 `outputs/skill-inference-optimizer.md`。该 skill 为新的推理部署选择注意力实现、KV 缓存策略、量化和推测解码方案。

## Exercises | 练习题

1. **Easy.** Run `code/main.py`. Confirm the naive and cached decoders produce the same output; note the op-count difference.
   中文翻译：运行 `code/main.py`。确认朴素和缓存解码器产生相同输出；注意操作次数差异。
2. **Medium.** Implement prefix caching: given a prompt P and several completions, run one forward pass over P to fill the KV cache, then branch per-completion. Measure speedup vs re-encoding P for each.
   中文翻译：实现前缀缓存：给定提示 P 和多个补全，对 P 运行一次前向传播填充 KV 缓存，然后每个补全分支。测量与每次重新编码 P 相比的速度提升。
3. **Hard.** Implement a toy PagedAttention: KV cache in fixed 16-token blocks with a free-list. When a sequence finishes, return its blocks to the pool. Simulate 1,000 chat completions with varying lengths. Compare memory fragmentation vs contiguous allocation.
   中文翻译：实现玩具版 PagedAttention：KV 缓存使用固定 16 token 块加空闲列表。序列完成时归还块。模拟 1,000 个变长聊天补全。比较与连续分配的内存碎片化差异。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| KV cache | "The trick that makes decoding fast" | Stored K and V from every prefix token; new queries attend to them instead of recomputing. |
| KV 缓存 | "让解码变快的技巧" | 存储每个前缀 token 的 K 和 V；新查询对它们做注意力而非重新计算。 |
| HBM | "GPU main memory" | High Bandwidth Memory; 80 GB on H100, 192 GB on B200. ~3 TB/s bandwidth. |
| HBM | "GPU 主内存" | 高带宽内存；H100 上 80 GB，B200 上 192 GB。约 3 TB/s 带宽。 |
| SRAM | "On-chip memory" | Per-SM fast memory, ~256 KB per SM on H100. ~30 TB/s bandwidth. |
| SRAM | "片上内存" | 每 SM 的快速内存，H100 上每 SM 约 256 KB。约 30 TB/s 带宽。 |
| Flash Attention | "Tiled attention kernel" | Computes attention without materializing N×N in HBM. |
| Flash Attention | "分块注意力内核" | 不在 HBM 中生成 N×N 矩阵即完成注意力计算。 |
| Continuous batching | "No-wait batching" | Swap finished sequences out, new ones in, without draining the batch. |
| 连续批处理 | "无等待批处理" | 完成的序列换出，新的换入，无需排空批次。 |
| PagedAttention | "vLLM's headline" | KV cache allocated in fixed blocks with a page table; eliminates fragmentation. |
| PagedAttention | "vLLM 的核心特性" | KV 缓存以固定块分配加页表；消除碎片化。 |
| Prefix caching | "Reuse long prompts" | Cache KV for a shared prefix across requests; major cost cut for agents. |
| 前缀缓存 | "复用长提示" | 跨请求缓存共享前缀的 KV；代理场景大幅降低成本。 |
| Speculative decoding | "Draft + verify" | Cheap draft model proposes tokens; big model verifies k in one pass. |
| 推测解码 | "草案 + 验证" | 廉价草案模型提出 token；大模型一次验证 k 个。 |

## Further Reading | 延伸阅读

- [Dao et al. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135) — Flash 1.
  中文翻译：Flash Attention 1 论文。
- [Dao (2023). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691) — Flash 2.
  中文翻译：Flash Attention 2 论文。
- [Shah et al. (2024). FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](https://arxiv.org/abs/2407.08608) — Flash 3.
  中文翻译：Flash Attention 3 论文。
- [FlashAttention-4 release notes (Dao-AILab, 2026)](https://github.com/Dao-AILab/flash-attention) — Blackwell 5-stage pipeline and the software-exp2 trick; read the repo README for the forward-only launch caveats this lesson mentions.
  中文翻译：Flash Attention 4 发布说明；Blackwell 5 阶段管道和软件 exp2 技巧。
- [Kwon et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) — vLLM paper.
  中文翻译：vLLM PagedAttention 论文。
- [Leviathan et al. (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) — spec decoding.
  中文翻译：推测解码论文。
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) — EAGLE-1/2 paper for the integrated-draft approach the lesson cites.
  中文翻译：EAGLE-1/2 论文，集成草案方法。
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) — the Medusa approach referenced alongside EAGLE.
  中文翻译：Medusa 论文，多解码头方法。
- [vLLM docs — PagedAttention](https://docs.vllm.ai/en/latest/design/kernel/paged_attention.html) — the canonical deep dive on the 16-token block and page-table design.
  中文翻译：vLLM PagedAttention 文档，16 token 块和页表设计的深入解析。
