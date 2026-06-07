# Native Sparse Attention (DeepSeek NSA) | 原生稀疏注意力 (DeepSeek NSA)

> At 64k tokens, attention eats 70-80% of decode latency. Every open-model lab has a plan to fix it. DeepSeek's NSA (ACL 2025 best paper) is the one that stuck: three parallel attention branches — compressed coarse-grained tokens, selectively retained fine-grained tokens, and sliding windows for local context — combined through a learned gate. It is hardware-aligned (kernel-friendly), natively trainable (works in pre-training, not bolted on at inference), and on 64k decodes it runs faster than FlashAttention while matching or beating full attention quality. This lesson builds the three branches end-to-end and shows why the sparsity is end-to-end differentiable.

> **【中文解读】** 64K token 时注意力消耗 70-80% 的解码延迟。DeepSeek NSA（ACL 2025 最佳论文）用三条并行注意力分支解决：压缩粗粒度 token、选择保留细粒度 token、滑动窗口局部上下文，通过可学习门控组合。硬件友好、可预训练、比 FlashAttention 更快。

> **【拓展：稀疏注意力→长上下文】** 长上下文（64K-128K token）是 2025-2026 年大模型的核心能力。NSA、MHA、GQA 都是降低注意力计算复杂度的方案。DeepSeek 的创新在于稀疏性是端到端可微分的，可以在预训练阶段直接使用。

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 12 (KV cache, flash-attention), Phase 7 · 15 (attention variants), Phase 10 · 16 (differential attention)
**Time:** ~60 minutes

## Learning Objectives

- State the three NSA attention branches and what each one captures.
- Explain why NSA is "natively trainable" where prior sparse-attention methods were inference-only.
- Compute the attention compute savings of NSA versus full attention at 64k context as a function of compression block size and selection top-k.
- Implement the three-branch combination in stdlib Python on a short synthetic sequence and verify the gating weights behave.

## The Problem

Full attention at sequence length N costs `O(N^2)` time and `O(N)` KV cache per layer. At 64k tokens, the compute and memory bandwidth numbers are catastrophic. Measured theoretical estimate from the NSA paper: attention accounts for 70-80% of total decode latency at 64k. Everything downstream — TTFT, tokens/sec, cost per million tokens — is dominated by attention cost.

> **【中文解读】**
> 64K token 时，注意力机制占了解码延迟的 70-80%。问题出在 O(N^2) 的计算复杂度——token 数量翻倍，计算量翻四倍。之前的稀疏注意力方案要么丢弃信息（滑动窗口），要么在推理时才稀疏化（KV cache 剪枝），效果都不理想。NSA 的突破在于让稀疏模式在预训练阶段就参与学习，模型自动学会如何在稀疏模式下路由信息。

Sparse attention is the obvious answer. Prior attempts fall into two buckets. Fixed-pattern sparsity (sliding-window, strided, block-local) throws information away and fails on long-range recall tasks. Inference-time sparsity (KV cache pruning, H2O, StreamingLLM) is applied to a model pre-trained on dense attention and recovers only a fraction of the potential speedup because the model was never asked to route information through the sparse pattern.

Native Sparse Attention (Yuan et al., DeepSeek + PKU + UW, ACL 2025 best paper, arXiv:2502.11089) does both: a sparsity pattern the model learns during pre-training, implemented as a kernel-aligned algorithm that actually delivers the compute savings at inference. Two years from now, NSA or a direct descendant is the default attention on every frontier long-context model.

## The Concept

### Three parallel branches

For each query, NSA runs attention three times, against three different views of the KV cache:

1. **Compressed branch.** Tokens are grouped into blocks of size `l` (typically 32 or 64). Each block is compressed into a single summary token via a small learned MLP. The query attends over these compressed tokens, getting a coarse-grained view of the whole sequence.

2. **Selected branch.** Using attention scores from the compressed branch, the top-k blocks most relevant to the current query are identified. Fine-grained (uncompressed) tokens from those blocks are read and the query attends over all of them. Think of compressed-branch attention as the routing signal for the selection.

3. **Sliding-window branch.** The query attends to the most recent `W` tokens (typically 512) for local context. This branch captures the structure-heavy short-range patterns (syntax, local coreference) that the other two might miss.

The three branch outputs are combined via a learned per-position gate:

```
out = g_cmp * out_cmp + g_sel * out_sel + g_win * out_win
```

`g_cmp, g_sel, g_win` are gate weights from a small MLP on the query. They do not have to sum to 1 — they can weight branches independently.

### Why this is "natively trainable"

The selection step (top-k blocks) is discrete. Discrete operations break gradient flow. Prior sparse-attention work either skipped backprop through selection (limiting training) or used continuous relaxations that did not give real sparsity at inference.

NSA sidesteps this: the compressed-branch attention IS a differentiable coarse-grained attention on the whole sequence. The top-k operation just reuses the top attention scores from the compressed branch to pick which fine-grained blocks to load. Gradients flow through the compressed-branch scores (which influence both the compressed output AND the selection logic), and the selected blocks' contribution to the final output is also differentiable. The non-differentiable `top_k` operation is a no-op on the forward computational graph — it only controls which blocks get loaded from memory.

This is why NSA can be used in pre-training end to end. The model learns to route information through the three branches jointly, producing a sparse pattern that at inference actually delivers the promised speedup.

### Hardware-aligned kernel

NSA's kernel is designed for modern GPU memory hierarchies. The kernel loads queries by GQA groups (outer loop), fetches the corresponding sparse KV blocks per group (inner loop), and runs attention on SRAM. Because each query group sees the same selected blocks (selection is per-query-group, not per-query-head), the KV loads are amortized across the group. Arithmetic intensity stays high.

The paper reports Triton kernels running 9x faster than FlashAttention on 64k decodes, with the speedup ratio growing with sequence length. Forward and backward kernels are both provided.

### The compute budget

Let `N` be sequence length, `l` the compression block size, `k` the top-k selection count, `w` the sliding window, `b` the selected block size (typically equals `l`).

- Compressed branch: `O(N/l)` keys per query, so `O(N * N / l)` total.
- Selected branch: `O(k * b)` keys per query, so `O(N * k * b)`.
- Sliding branch: `O(w)` keys per query, so `O(N * w)`.

Total: `O(N * (N/l + k*b + w))`.

With `N = 64k, l = 64, k = 16, b = 64, w = 512`: per-query cost is `1000 + 1024 + 512 = 2536 keys`. Full attention is `64000 keys`. 25x compute reduction.

With `N = 128k, l = 64, k = 16, b = 64, w = 512`: per-query cost is `2000 + 1024 + 512 = 3536 keys`. Full attention is `128000 keys`. 36x reduction. The benefit grows with sequence length, which is the whole point.

### How does it compare

| Method | Differentiable | Real inference speedup | Long-range recall |
|--------|---------------|----------------------|-------------------|
| Sliding window only | yes | yes | fails |
| Strided / block-sparse | yes | yes | partial |
| KV pruning (H2O, StreamingLLM) | N/A (inference-time) | yes | partial |
| MoBA (Moonshot) | partial | yes | good |
| NSA | yes (natively) | yes (9x at 64k) | matches full attention |

MoBA (Moonshot, arXiv:2502.13189) was concurrently published and takes a similar three-is-better-than-one approach, applying the MoE principle to attention blocks. NSA and MoBA are the two architectures to know for 2026 long-context pre-training.

## Build It

> **【中文解读】**
> NSA 的三条分支各司其职：压缩分支用 O(N/l) 的开销扫描全序列找到粗粒度相关区域；选择分支在 top-k 区域做细粒度注意力，精确捕捉远距离依赖；滑动窗口分支处理局部语法和指代关系。三条分支通过可学习门控组合，整体复杂度从 O(N^2) 降到 O(N*(N/l + k*b + w))，64K 时 25 倍计算减少。

> **【拓展：稀疏注意力→RAG 和长文档】** NSA 使得 128K+ token 的上下文窗口在经济上可行。想象一下把整本书喂给 LLM 做 RAG——标准注意力在 128K token 时的计算量是 NSA 的 36 倍。DeepSeek 的 Triton 内核在 64K 解码时比 FlashAttention 快 9 倍，这意味着长上下文推理不再需要昂贵的集群，单卡就能跑。

`code/main.py` implements the three branches on a short synthetic sequence and shows:

- The compression MLP (a simple mean-pool baseline is used for pedagogical clarity; the real NSA uses a learned MLP).
- The top-k block selection driven by compressed-branch scores.
- The sliding-window attention on the last `w` tokens.
- The gated combination.
- A compute-count printout comparing to full attention.

### Step 1: compress tokens into blocks

```python
def compress(K, l):
    n = len(K)
    n_blocks = (n + l - 1) // l
    out = []
    for b in range(n_blocks):
        start, end = b * l, min((b + 1) * l, n)
        block = K[start:end]
        summary = [sum(row[d] for row in block) / len(block) for d in range(len(K[0]))]
        out.append(summary)
    return out
```

### Step 2: compressed-branch attention

Run softmax attention of the query against the compressed keys. The compressed-branch scores double as the signal for top-k selection.

### Step 3: top-k block selection

Pick the indices of the `k` highest-scoring compressed blocks. Load the original uncompressed tokens from those blocks and run attention on them.

### Step 4: sliding-window attention

Take the last `w` tokens and run standard attention against them.

### Step 5: gate + combine

A small MLP on the query produces three gate weights. The final output is a weighted sum of the three branch outputs.

### Step 6: compute counting

Print the number of keys attended per query for each branch and the total. Compare to `N` (full attention). On a 1024-token synthetic with `l = 32, k = 4, w = 128`, NSA sees `32 + 128 + 128 = 288` keys per query versus 1024 for full attention — 3.5x fewer.

## Use It

NSA is shipping in DeepSeek's own long-context pre-training pipeline. Integration status in public inference stacks as of April 2026:

- **DeepSeek internal**: native, published weights use NSA or its successor DSA (Deepseek Sparse Attention).
- **vLLM**: experimental NSA support in development for DeepSeek-V3.x weights.
- **SGLang**: NSA benchmarks published; production path follows vLLM.
- **llama.cpp / CPU**: not supported; overhead of the kernel decomposition is not worth it at CPU throughput.

When to reach for NSA:

- Pre-training or continued-training run targeting 64k-plus context with a serious compute budget.
- Inference of DeepSeek's own long-context checkpoints. The weights are NSA-native.

When not to:

- Serving an existing dense-attention pre-trained model. You cannot retrofit NSA without continued training.
- Context under 16k. The three-branch overhead dominates the savings.
- Batch-1 interactive chat. Latency-sensitive decode benefits, but only at long contexts.

## Ship It

This lesson produces `outputs/skill-nsa-integrator.md`. Given a long-context pre-training run specification, it produces an NSA integration plan: compression block size, top-k, sliding window, gate MLP width, kernel choice, and the specific long-context evals that would justify the architecture change.

## Exercises

1. Run `code/main.py` on a 1024-token synthetic. Sweep `(l, k, w)` across three presets and print compute counts. Identify the preset that achieves the lowest key-count per query while keeping 95% recall against full attention on a needle-in-haystack test.

2. Replace the mean-pool compressor with a tiny learned MLP (2-layer, hidden 32). Train it on a synthetic task where the signal is the average of a block. Measure the perplexity gap against the mean-pool baseline on held-out data.

3. Implement the gate MLP. It takes the query as input and outputs three scalars. Show that the gate behaves sensibly: near-uniform weighting on random queries, heavy weight on the selected branch when the query hits a far-back block.

4. Compute the KV cache memory budget for an NSA-enabled 70B model at 128k context. KV heads are 8, head dim 128, BF16. Compare to full attention and to MLA (Phase 10 · 14 showed MLA's numbers). Identify the sequence length where NSA's fine-grained branch KV cache equals full attention.

5. Read Section 4 of the NSA paper (arXiv:2502.11089) and explain in three sentences why the compressed branch's attention scores are reused for top-k selection rather than computing a separate routing score. Tie the answer to gradient flow.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Compressed branch | "Coarse view" | Attention over block-averaged keys that provides global context in O(N/l) keys per query |
| Selected branch | "Top-k blocks" | Fine-grained attention over the `k` blocks with highest compressed-branch scores |
| Sliding window | "Local context" | Attention over the last `W` tokens for short-range patterns |
| Native trainability | "Pre-train with the sparsity on" | The sparsity pattern is learned during pre-training, not bolted on at inference |
| Compression block size l | "Group size for coarse view" | How many tokens get merged into one summary; 32-64 typical |
| Top-k | "Blocks to keep" | Number of compressed blocks whose uncompressed tokens get read; 16 typical |
| Sliding window W | "Local attention radius" | Typically 512; shorter hurts local coherence, longer wastes compute |
| Branch gate | "How to mix the three" | Per-position MLP output that weights the three branches' contributions |
| Hardware alignment | "Kernel-friendly sparsity" | Sparse pattern chosen so that the actual GPU kernel achieves the theoretical speedup |
| DSA | "NSA's successor" | Deepseek Sparse Attention, the architecture that followed NSA in DeepSeek's lineage |

| 术语 | 俗称 | 实际含义 |
|------|------|---------|
| 压缩分支 | "粗粒度视图" | 对块平均键做注意力，以 O(N/l) 的键/query 提供全局上下文 |
| 选择分支 | "Top-k 块" | 对压缩分支得分最高的 k 个块做细粒度注意力 |
| 滑动窗口 | "局部上下文" | 对最近 W 个 token 做注意力，捕捉短程模式 |
| 原生可训练性 | "预训练时带稀疏性" | 稀疏模式在预训练阶段学习，而非推理时才加上 |
| 压缩块大小 l | "粗粒度分组大小" | 多少 token 合并成一个摘要；典型值 32-64 |
| Top-k | "保留的块数" | 压缩块中哪些保留原始 token 做细粒度注意力；典型值 16 |
| 滑动窗口 W | "局部注意力半径" | 典型值 512；太短影响局部连贯性，太长浪费计算 |
| 分支门控 | "如何混合三条" | 逐位置 MLP 输出，加权三条分支的贡献 |
| 硬件对齐 | "内核友好的稀疏性" | 稀疏模式让实际 GPU 内核达到理论加速比 |
| DSA | "NSA 的继任者" | Deepseek Sparse Attention，NSA 之后 DeepSeek 的下一代架构 |

## Further Reading

- [Yuan et al. — Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention (arXiv:2502.11089, ACL 2025 Best Paper)](https://arxiv.org/abs/2502.11089) — the paper
- [DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/abs/2412.19437) — the architecture family NSA targets
- [Moonshot AI — MoBA: Mixture of Block Attention for Long-Context LLMs (arXiv:2502.13189)](https://arxiv.org/abs/2502.13189) — concurrent work, MoE-style attention over blocks
- [Beltagy et al. — Longformer: The Long-Document Transformer (arXiv:2004.05150)](https://arxiv.org/abs/2004.05150) — sliding-window origins
- [Xiao et al. — StreamingLLM: Efficient Streaming Language Models with Attention Sinks (arXiv:2309.17453)](https://arxiv.org/abs/2309.17453) — inference-time sparsity baseline NSA improves on
- [Dao et al. — FlashAttention-2 (arXiv:2307.08691)](https://arxiv.org/abs/2307.08691) — the full-attention baseline NSA kernels beat at 64k
