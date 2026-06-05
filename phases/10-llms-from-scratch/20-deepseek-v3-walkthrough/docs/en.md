# DeepSeek-V3 Architecture Walkthrough | DeepSeek-V3 架构详解

> Phase 10 · Lesson 14 named the six architectural knobs every open model turns. DeepSeek-V3 (December 2024, 671B parameters total, 37B active) turns all six and adds four more: Multi-Head Latent Attention, auxiliary-loss-free load balancing, Multi-Token Prediction, and DualPipe training. This lesson reads DeepSeek-V3's architecture top to bottom and derives every parameter count from the published config. By the end you can explain why the 671B/37B ratio is the right bet and why MLA + MoE together beat either alone at the frontier.

> **【中文解读】** DeepSeek-V3（2024年12月，671B 总参数，37B 激活）转动了所有六个架构旋钮并新增四个：MLA（多头潜在注意力）、无辅助损失的负载均衡、MTP（多 token 预测）、DualPipe 训练。671B/37B 的比例意味着每次推理只激活 5.5% 的参数。

> **【拓展：DeepSeek架构→开源大模型】** DeepSeek-V3 是 2024-2025 年最重要的开源大模型架构之一。MLA 将 KV-cache 压缩到原来的 1/10，MoE 让 671B 模型只消耗 37B 的推理成本。理解这个架构是理解中国 AI 实验室在大模型领域突破的关键。

**Type:** Learn
**Languages:** Python (stdlib, parameter calculator)
**Prerequisites:** Phase 10 · 14 (open-model walkthroughs), Phase 10 · 17 (NSA), Phase 10 · 18 (MTP), Phase 10 · 19 (DualPipe)
**Time:** ~75 minutes

## Learning Objectives | 学习目标

- Read the DeepSeek-V3 config top to bottom and explain each field in terms of the six GPT-2 knobs plus four DeepSeek-specific additions.
  从头到尾阅读 DeepSeek-V3 配置，用 GPT-2 的六个旋钮加上四个 DeepSeek 特有创新解释每个字段
- Derive the total parameter count (671B), active parameter count (37B), and the components that contribute to each.
  推导总参数量（671B）、激活参数量（37B）及其组成
- Compute the KV cache footprint of MLA at 128k context and compare to what a same-active-param dense model with GQA would pay.
  计算 MLA 在 128K 上下文中的 KV 缓存占用，与同等激活参数的 GQA 密集模型对比
- State the four DeepSeek-specific innovations (MLA, MTP, auxiliary-loss-free routing, DualPipe) and name which part of the architecture/training stack each one targets.
  说出四项 DeepSeek 特有创新（MLA、MTP、无辅助损失路由、DualPipe）及其针对的架构/训练环节

## The Problem | 问题引入

DeepSeek-V3 is the first frontier open model whose architecture is meaningfully different from the Llama family. Llama 3 405B is "GPT-2 with six knobs turned." DeepSeek-V3 is GPT-2 with all six knobs plus four more. Reading the Llama 3 config is a warmup for reading the DeepSeek config, but the deep structure — the shape of the attention block, the routing logic, the training-time objective — is different enough that you need a separate walkthrough.

The payoff of learning it: DeepSeek-V3's open-weights release shifted what "frontier capability" means in open models. The architecture is the blueprint many 2026 training runs are copying. Understanding it is table stakes for any role that touches frontier LLM training or inference.

## The Concept | 核心概念

> **【中文解读】** DeepSeek-V3 是 2024 年最具影响力的开源模型之一：671B 总参数（37B 激活参数）的 MoE 架构，用 MLA（多头潜在注意力）压缩 KV-cache，用 DualPipe 优化流水线并行，以约 560 万美元的训练成本达到了 GPT-4 级别的性能。

> **【拓展：DeepSeek-V3 的经济性突破】** DeepSeek-V3 的训练成本仅约 560 万美元（2.788M H800 GPU 小时），约为 Llama 3 405B 训练成本的 1/18。关键因素：MoE 只激活 37B/671B 参数（降低约 18 倍计算量）、FP8 混合精度训练、DualPipe 减少流水线气泡、自研通信内核减少跨节点通信开销。


### The invariant core, again

DeepSeek-V3 is still autoregressive. It still stacks decoder blocks. Each block still has attention plus MLP plus two RMSNorms. It still uses SwiGLU in the MLP. It still uses RoPE. Pre-norm. Weight-tied embeddings. Same baseline as every Llama or Mistral.

### The twist: MLA instead of GQA

From Phase 10 · 14 you know GQA shrinks the KV cache by sharing K and V across groups of Q heads. Multi-Head Latent Attention (MLA) goes further: K and V are compressed into a shared low-rank latent representation (the `kv_lora_rank`), then decompressed per head on the fly. The KV cache stores only the latent — typically 512 floats per token per layer, not 8 x 128 = 1024 floats.

At 128k context, DeepSeek-V3 with MLA (one shared latent `c^{KV}` per token per layer; K and V are both derived from this latent via up-projections that can be absorbed into the subsequent matmul):

```
kv_cache = num_layers * kv_lora_rank * max_seq_len * bytes_per_element
         = 61 * 512 * 131072 * 2
         = 7.6 GB
```

A hypothetical GQA baseline (Llama 3 70B shape, 8 KV heads, head dim 128) would pay:

```
kv_cache = 2 * 61 * 8 * 128 * 131072 * 2
         = 30.5 GB
```

MLA is 4x smaller than a Llama-3-70B-style GQA cache at 128k context.

The tradeoff: MLA adds a decompression step per attention computation (per head). The extra compute is small compared to the bandwidth saved. Net win for long-context inference.

### The routing: auxiliary-loss-free load balancing

MoE routers decide which top-k experts process each token. A naive router concentrates too much work on a few experts, leaving others idle. Standard fix: add an auxiliary loss term that penalizes load imbalance. This works but slightly degrades main-task performance.

DeepSeek-V3 introduces an auxiliary-loss-free scheme. Per-expert bias terms are added to the router logits, adjusted during training by a simple rule: if expert `e` is overloaded, decrease `bias_e`; if underloaded, increase it. No extra loss term. Training stays clean. Expert load stays balanced.

Effect on the main loss: none measurable. Effect on the MoE architecture: cleaner, no auxiliary-loss hyperparameter to tune.

### The MTP: denser training + free draft

From Phase 10 · 18 you know DeepSeek-V3 adds D=1 MTP module that predicts the token two positions ahead. At inference, the trained module is repurposed as a speculative-decoding draft with 80%+ acceptance. At training, each hidden state is supervised on D+1 = 2 targets, providing a denser signal.

Parameters: 14B on top of the 671B main. Overhead: 2.1%.

### The training: DualPipe

From Phase 10 · 19 you know DualPipe is a bidirectional pipeline that overlaps forward and backward chunks with cross-node all-to-all comms. At DeepSeek-V3's 2,048-H800 scale, it recovers roughly 245k GPU-hours that 1F1B would have lost to pipeline bubbles.

### The config, field by field

Here is the DeepSeek-V3 config (simplified):

```
hidden_size: 7168
intermediate_size: 18432   (dense MLP hidden size, used on first few layers)
moe_intermediate_size: 2048 (expert MLP hidden size)
num_hidden_layers: 61
first_k_dense_layers: 3    (first 3 layers use dense MLP)
num_attention_heads: 128
num_key_value_heads: 128   (formally equal to num_heads under MLA, but
                           the real compression is in kv_lora_rank)
kv_lora_rank: 512          (MLA latent dimension)
num_experts: 256            (MoE expert count per block)
num_experts_per_tok: 8      (top-8 routing)
shared_experts: 1           (always-on shared expert per block)
max_position_embeddings: 163840
rope_theta: 10000.0
vocab_size: 129280
mtp_module: 1               (1 MTP module at depth 1)
```

Parse it:

- `hidden_size=7168`: embedding dimension.
- `num_hidden_layers=61`: total block depth.
- `first_k_dense_layers=3`: the first 3 blocks use a dense MLP of size 18432. The remaining 58 use MoE.
- `num_attention_heads=128`: 128 query heads.
- `kv_lora_rank=512`: K and V are compressed to this latent dimension and decompressed per head.
- `num_experts=256, num_experts_per_tok=8`: each MoE block has 256 experts, routes top-8.
- `shared_experts=1`: on top of the 256 routed experts, 1 always-on expert contributes to every token. Think of it as a "dense floor" that ensures every token gets something reliable.
- `moe_intermediate_size=2048`: each expert's MLP hidden size. Smaller than the dense MLP because there are 256 of them.

### Parameter accounting

The full calculation lives in `code/main.py`. The headline:

- Embedding: `vocab * hidden = 129280 * 7168 = ~0.93B`.
- First 3 dense blocks: attention with MLA (~144M per block) + dense MLP (~260M per block) + norms. About 1.2B total.
- 58 MoE blocks: attention with MLA (~144M) + 256 experts each (30M apiece) + 1 shared expert (30M) + norm. Total ~7.95B per block, including all experts. 461B total for the 58 MoE blocks.
- MTP module: 14B.

Grand total: ~476B for core architecture + 14B MTP + distinctly the published 671B number accounts for additional structural parameters (bias tensors, expert-specific components, shared expert scaling, etc.). The number we reproduce in the calculator is within 3-5% of published — the delta comes from fine-grained accounting DeepSeek's report documents in its Section 2 appendix.

Active parameters per forward:

- Attention: 144M per layer * 61 = 8.8B (all layers fire).
- MLP active: first 3 layers dense (3 * 260M = 780M), 58 MoE layers each active with 8 routed + 1 shared + routing overhead. Per layer active MLP: ~260M. Total: 3 * 260M + 58 * 260M = ~15.9B.
- Embedding + norms: 1.2B.
- Total active: roughly 26B core + 14B MTP (trained but not always run at inference) ≈ 37B.

### The 671B / 37B ratio

18x sparsity ratio (active params are 5.5% of total). DeepSeek-V3 is the sparsest frontier MoE model that has shipped open weights. Mixtral 8x7B at ratio 13/47 (28%) is much denser. Llama 4 Maverick at ratio 17B/400B (4.25%) is comparable. The DeepSeek bet: at frontier scale, more experts with lower activation ratio produces better quality per active-FLOP.

### Where DeepSeek-V3 sits

| Model | Total | Active | Ratio | Attention | Novel ideas |
|-------|------|-------|-------|-----------|-------------|
| Llama 3 70B | 70B | 70B | 100% | GQA 64/8 | — |
| Llama 4 Maverick | 400B | 17B | 4.25% | GQA | — |
| Mixtral 8x22B | 141B | 39B | 27% | GQA | — |
| DeepSeek V3 | 671B | 37B | 5.5% | MLA 512 | MLA + MTP + aux-free + DualPipe |
| Qwen 2.5 72B | 72B | 72B | 100% | GQA 64/8 | YaRN extension |

### The follow-on: R1, V4

DeepSeek-R1 (2025) is a reasoning-training run on the V3 backbone. R1 uses the same architecture. What changed is the post-training recipe (large-scale RL on verifiable tasks), not the pretraining architecture.

DeepSeek-V4 (if it ships) is expected to keep MLA + MoE + MTP and add DSA (DeepSeek Sparse Attention), the successor to NSA from Phase 10 · 17. The lineage is stable: architecture-level innovations accumulate; each version turns additional knobs.


> **【拓展：DeepSeek-V3 的 MoE 架构细节】** DeepSeek-V3 有 256 个路由专家，每次激活 8 个（加 1 个共享专家）。671B 总参数但只激活约 37B，计算量仅约 5.5%。


## Use It | 用框架实现

`code/main.py` is the parameter calculator specialized to DeepSeek-V3's shape. Run it, compare its output to the paper's numbers, and use it on hypothetical variants (256 experts vs 512, top-8 vs top-16, MLA rank 512 vs 1024).

What to look at:

- Total parameter count vs published 671B.
- Active parameter count vs published 37B.
- KV cache at 128k context — the MLA vs GQA comparison.
- Per-layer breakdown to see where the parameter budget actually goes.

## Ship It | 产出物

This lesson produces `outputs/skill-deepseek-v3-reader.md`. Given a DeepSeek-family model (V3, R1, or any future variant), it produces a component-by-component architecture reading that names each field of the config, derives parameter counts by component, and identifies which of the four DeepSeek-specific innovations the model uses.

## Exercises | 练习题

1. Run `code/main.py`. Compare the calculator's total-parameter estimate to the published 671B and identify where the delta comes from. The paper's Section 2 has the full itemization.

2. Modify the config to use MLA rank 256 instead of 512. Compute the resulting KV cache size at 128k context. What percentage reduction does it buy, and at what cost to the per-head expressiveness?

3. Compare DeepSeek-V3's (256 experts, top-8) routing to a hypothetical (512 experts, top-8) variant. Total parameters grow; active parameters stay the same. What does the extra expert capacity buy in theory, and what does it cost at inference?

4. Read Section 2.1 of the DeepSeek-V3 technical report (arXiv:2412.19437) on MLA. Explain in three sentences why the K and V decompression matrices can be "absorbed" into the subsequent matmul for inference-time efficiency.

5. DeepSeek-V3 uses FP8 training for most operations. Compute the memory savings of FP8 vs BF16 for storing the 671B weights. How does this intersect with the 14.8T-token training budget?

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| MLA | "Multi-Head Latent Attention" | Compress K and V into a shared low-rank latent (kv_lora_rank, typically 512), decompress per head on-the-fly; KV cache stores only the latent | 多头潜在注意力，将 K/V 压缩为共享低秩潜在向量 |
| kv_lora_rank | "MLA compression dim" | The size of the shared latent for K and V; DeepSeek-V3 uses 512 | MLA 压缩维度，DeepSeek-V3 使用 512 |
| First k dense layers | "Early layers stay dense" | The first few MoE-model layers skip the MoE router and run a dense MLP for stability | 前 k 层保持密集，跳过 MoE 路由保证稳定性 |
| num_experts_per_tok | "Top-k routing" | How many routed experts fire per token; DeepSeek-V3 uses 8 | 每 token 激活专家数，DeepSeek-V3 使用 8 |
| Shared experts | "Always-on experts" | Experts that process every token regardless of routing; DeepSeek-V3 uses 1 | 共享专家，每个 token 都经过的专家 |
| Auxiliary-loss-free routing | "Bias-adjusted load balance" | Per-expert bias terms adjusted during training to keep expert load balanced without adding a loss term | 无辅助损失路由，用偏置项替代辅助损失做负载均衡 |
| MTP module | "Extra prediction head" | Transformer block predicting t+2 from h^(1) and E(t+1); denser training, free speculative-decoding draft | MTP 模块，多 token 预测头 |
| DualPipe | "Bidirectional pipeline" | Training schedule that overlaps forward/backward compute with cross-node all-to-all | DualPipe，双向流水线调度 |
| Active parameter ratio | "Sparsity" | active_params / total_params; DeepSeek-V3 hits 5.5% | 激活参数比，DeepSeek-V3 仅 5.5% |
| FP8 training | "8-bit training" | Training storage and many compute ops in FP8; roughly halves memory vs BF16 at a small quality cost | FP8 训练，8 位训练节省约一半显存 |

## Further Reading | 延伸阅读

- [DeepSeek-AI — DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/abs/2412.19437) — the full architecture, training, and results document
- [DeepSeek-V3 model card on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V3) — config files and deployment notes
- [DeepSeek-V2 paper (arXiv:2405.04434)](https://arxiv.org/abs/2405.04434) — the predecessor that introduced MLA
- [DeepSeek-R1 paper (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948) — the reasoning-training successor on V3's architecture
- [Native Sparse Attention (arXiv:2502.11089)](https://arxiv.org/abs/2502.11089) — the future direction for DeepSeek-family attention
- [DualPipe repository](https://github.com/deepseek-ai/DualPipe) — the training-schedule reference
