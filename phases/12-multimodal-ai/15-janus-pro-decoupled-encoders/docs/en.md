# Janus-Pro: Decoupled Encoders for Unified Multimodal Models | Janus-Pro：解耦编码器的统一多模态模型

> Unified multimodal models have an unavoidable tension.

> **【中文解读】** Janus-Pro（DeepSeek，2025年1月）解决了一个根本矛盾：理解任务需要语义特征（SigLIP），生成任务需要重建友好的编码（VQ token）。两者无法兼容于单一编码器。Janus-Pro 的答案是解耦：理解走 SigLIP 路径，生成走 VQ 路径，共享 Transformer 主体。7B 参数就在 GenEval 上击败了 DALL-E 3。

> **【拓展：解耦编码器的产业影响】** 解耦编码器思想已成为 2026 年统一模型的默认架构。InternVL-U 将其整合到了原生多模态预训练框架中。对于需要同时理解和生成的产品（如创意工具、内容生成平台），Janus-Pro 是参考架构。 Understanding wants semantic features — SigLIP or DINOv2 output vectors rich with concept-level information. Generation wants reconstruction-friendly codes — VQ tokens that compose back into crisp pixels. The two goals are not compatible in a single encoder. Janus (DeepSeek, October 2024) and Janus-Pro (DeepSeek, January 2025) argue the fix is to stop trying: decouple the two encoders. Share the transformer body between tasks, but route understanding through SigLIP and generation through a VQ tokenizer. At 7B, Janus-Pro beats DALL-E 3 on GenEval while matching LLaVA on MMMU. This lesson reads why two encoders work where one fails.

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, dual-encoder routing + shared-body signal)
**Prerequisites:** Phase 12 · 13 (Transfusion), Phase 12 · 14 (Show-o)
**Time:** ~120 minutes

## Learning Objectives  | 学习目标

- Explain why a single shared encoder compromises either understanding or generation quality.
- Describe Janus-Pro's routing: SigLIP features on the input side for understanding, VQ tokens on both input and output for generation.
- Trace the data-mix scaling that makes Janus-Pro succeed where Janus did not.
- Compare decoupled (Janus-Pro), coupled-continuous (Transfusion), and coupled-discrete (Show-o) architectures.

## The Problem  | 问题背景

Unified models share a transformer body across understanding and generation. Previous attempts (Chameleon, Show-o, Transfusion) all use one visual tokenizer for both directions. The tokenizer is a compromise:

- Optimized for reconstruction (generation): VQ-VAE captures fine-grained pixel detail but produces tokens with weak semantic coherence.
- Optimized for semantics (understanding): SigLIP embeddings group "cat" images near "cat" tokens but do not permit good reconstruction.

Show-o and Transfusion pay for this with a visible quality tax on one direction. Janus-Pro asks: why require one tokenizer when the tasks have different needs?

## The Concept  | 核心概念

### Decoupled visual encoding

Janus-Pro's architecture separates the two encoders:

- Understanding path. Input image → SigLIP-SO400m → 2-layer MLP → transformer body.
- Generation path. Input image (if conditioning on an existing image) → VQ tokenizer → token IDs → transformer body.
- Output generation. Image tokens predicted by the transformer → VQ decoder → pixels.

The transformer body is shared. Everything upstream and downstream of the body is task-specific.

Inputs are disambiguated by prompt format: a `<understand>` tag routes through SigLIP; `<generate>` routes through VQ. Or the routing is implicit from task.

### Why this works

Understanding loss gets SigLIP features, which CLIP-style pretraining has tuned for semantic similarity. The model's perception benchmarks improve over Show-o / Transfusion because the input features are better for the task.

Generation loss gets VQ tokens, which a tokenizer has tuned for reconstruction. Image quality improves over Show-o because VQ codes compose back to pixels cleanly.

The shared transformer body sees two input distributions (SigLIP and VQ) and learns to work with both. The claim: enough data + enough parameters, the body absorbs the switching.

### Data scaling — Janus vs Janus-Pro

Janus (original, arXiv 2410.13848) introduced the decoupling but at small scale (1.3B params, limited data). Janus-Pro (arXiv 2501.17811) scaled:

- 7B params (vs 1.3B).
- 90M image-text pairs for stage 1 (alignment) up from 72M.
- 72M for stage 2 (unified) up from 26M.
- Added 200k image-gen instruction samples for stage 3.

The upshot: Janus-Pro-7B matches LLaVA on MMMU (60.3 vs ~58) and beats DALL-E 3 on GenEval (0.80 vs 0.67). One open model, competitive on both sides of the unified spectrum.

### JanusFlow — the rectified flow variant

JanusFlow (arXiv 2411.07975) swaps the VQ generation path for a rectified-flow generation path (continuous). The split becomes SigLIP-for-understanding + rectified-flow-for-generation. Quality ceilings lift further. The architecture remains decoupled-encoders-shared-body.

### The shared body's job

The transformer body processes a unified sequence but with two input distributions. Its job is to:

- For understanding: consume SigLIP features + text tokens → emit text autoregressively.
- For generation: consume text tokens + (optional image VQ tokens) → emit image VQ tokens autoregressively.

The body has no modality-specific weights per block. It is the text-style transformer you'd expect to find inside Qwen or Llama, plus the two input adapters.

Interestingly, this means Janus-Pro's body could be initialized from a pretrained LLM. Janus-Pro does initialize from DeepSeek-MoE-7B. That choice matters: the LLM contributes reasoning ability that pure-from-scratch unified models struggle to reach.

### Compared to InternVL-U

InternVL-U (Lesson 12.10) is the 2026 follow-up. It combines:

- Native multimodal pretraining (InternVL3 backbone).
- Decoupled-encoder routing (SigLIP in, VQ + diffusion heads out).
- Unified understanding + generation + editing.

InternVL-U subsumes Janus-Pro's architectural choice into a larger framework. The decoupled-encoder idea is now the default for unified models at scale.

### Limitations

Decoupled encoders add architectural complexity. Two tokenizers to train, two input paths to maintain, two sets of fail modes. For products that do not need generation, Janus-Pro is over-engineered — pick a LLaVA-family understanding model.

For products that do not need understanding, Janus-Pro is overqualified — pick a Stable Diffusion 3 / Flux model.

For products that need both, Janus-Pro is now the reference open architecture.

## Use It  | 动手实践

`code/main.py` simulates Janus-Pro routing:

- Two mock encoders: SigLIP-like (produces 256-dim semantic vectors) and VQ-like (produces integer codes).
- A prompt router that picks the encoder based on a task tag.
- A shared body (stand-in) that processes token sequences regardless of which encoder produced them.
- A switch from stage 1 (alignment) to stage 3 (instruction tune) weighted-sample schedule.

Print the routed paths for 3 examples: image QA, T2I, image editing.

## Ship It  | 部署上线

This lesson produces `outputs/skill-decoupled-encoder-picker.md`. Given a product that wants unified generation + understanding at frontier-ish quality, it picks Janus-Pro, JanusFlow, or InternVL-U with a concrete data-scale recommendation.

## Exercises  | 练习题

1. Janus-Pro-7B beats DALL-E 3 on GenEval. Explain why a 7B open model can match a frontier proprietary model on generation but not on understanding.

2. Implement a router function: given prompt text, classify as `understand` or `generate`. How do you handle ambiguous prompts like "describe and then sketch"?

3. JanusFlow replaces the VQ path with rectified flow. What does the transformer body now output, and what changes in the loss?

4. Propose a fourth task the Janus-Pro architecture could handle with one more decoupled encoder. Examples: image segmentation (DINO-style), depth (MiDaS-style).

5. Read Janus-Pro Section 4.2 on data scaling. Which data stage contributes most to the T2I quality gain vs Janus?

## Key Terms  | 关键术语

| Term | What people say | What it actually means | 中文含义 |
|------|-----------------|------------------------|
| Decoupled encoding | "Two visual encoders" | Separate tokenizer or encoder per direction: semantic for understanding, reconstruction for generation |
| Shared body | "One transformer" | Single transformer processes either encoder's output; no modality-specific weights |
| SigLIP for understanding | "Semantic features" | CLIP-family vision tower providing rich conceptual features but poor reconstruction |
| VQ for generation | "Reconstruction codes" | Vector-quantized tokens that decode cleanly back to pixels |
| JanusFlow | "Rectified-flow variant" | Janus-Pro with a continuous flow-matching generation head instead of VQ |
| Routing tag | "Task tag" | Prompt marker (`<understand>` / `<generate>`) that picks the input encoder |

## Further Reading  | 延伸阅读

- [Wu et al. — Janus (arXiv:2410.13848)](https://arxiv.org/abs/2410.13848)
- [Chen et al. — Janus-Pro (arXiv:2501.17811)](https://arxiv.org/abs/2501.17811)
- [Ma et al. — JanusFlow (arXiv:2411.07975)](https://arxiv.org/abs/2411.07975)
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877)
- [Dong et al. — DreamLLM (arXiv:2309.11499)](https://arxiv.org/abs/2309.11499)
