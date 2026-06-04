# LLaVA-OneVision: Single-Image, Multi-Image, Video in One Model | LLaVA-OneVision：单图、多图、视频统一模型

> Before LLaVA-OneVision (Li et al., August 2024) the open-VLM world had separate lineages: LLaVA-1.5 for single images, multi-image models like Mantis and VILA, video models like Video-LLaVA and Video-LLaMA. Each won its benchmark and failed at the others. LLaVA-OneVision argued a single curriculum could train one model to dominate all three scenarios, and that the emergent task-transfer effects (single-image skills exported to video, multi-image reasoning exported to single-image) beat the sum of specialists. The recipe is deceptively simple: a visual-token budget that stays constant across scenarios, plus an explicit curriculum that moves from single-image to OneVision (multi-image) to video. This lesson reads the budget, the curriculum, and the emergent behaviors.

> **【中文解读】** LLaVA-OneVision 的核心贡献：用一个统一的视觉 token 预算（约 3000-4000 token）和一个三阶段课程学习（单图→多图→视频），训练一个同时擅长三种场景的模型。课程学习带来了涌现能力——在单图上学的技能可以迁移到视频上。

> **【拓展：统一多模态模型的产业价值】** 在实际产品中，用户可能同时上传单张图片、多张图片和视频。维护三个独立模型（分别处理单图、多图、视频）的成本远高于一个统一模型。LLaVA-OneVision 的"固定 token 预算"策略使得推理成本可预测，这对部署成本控制至关重要。

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, token budget solver + curriculum planner)  | **语言：Python（标准库，token预算求解器 + 课程规划器）**
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 12 · 06 (any-resolution)  | **前置：阶段12第05课（LLaVA）、阶段12第06课（任意分辨率）**
**Time:** ~180 minutes  | **时长：约180分钟**

## 学习目标

- Design a visual-token budget that holds constant across single-image, multi-image, and video inputs.  | 设计在单图、多图和视频输入中保持恒定的视觉 token 预算。
- Order a training curriculum that transfers skills from single-image to video without catastrophic forgetting.  | 安排训练课程顺序，将单图技能迁移到视频而不发生灾难性遗忘。
- Explain why a single model beats specialists at the same parameter count when curriculum is done right.  | 解释为什么正确使用课程学习后，单一模型优于同等参数量的专家模型。
- Name the three emergent capabilities reported by LLaVA-OneVision: multi-camera reasoning, set-of-mark prompting, iPhone-screenshot agent.  | 列举 LLaVA-OneVision 报告的三种涌现能力。

## 问题背景

Image, multi-image, and video each stress a model differently.

Single-image wants high-resolution tokens (AnyRes, ~2880 visual tokens) to catch OCR and fine detail. Budget per sample: one image, 2880 tokens.

Multi-image wants several images at moderate resolution (~576 tokens each) so reasoning across images fits in context. Budget per sample: 4-8 images, 576 each, 2300-4600 tokens.

Video wants many frames at low resolution (~196 tokens per frame after pooling) to capture temporal dynamics. Budget per sample: 8-32 frames, 196 each, 1600-6200 tokens.

> **【中文解读】** 三种场景对 token 预算的需求不同：单图要高分辨率（约2880 token），多图要中等分辨率（每张约576 token），视频要低分辨率但多帧（每帧约196 token）。挑战在于：如何用一个固定预算同时满足三种场景。

If you train separate models, you pick one budget. If you train one model, you need the budget to scale sensibly across scenarios without blowing context.

Pre-OneVision, the default answer was "train one scenario, ignore the others." Video-LLaVA retrofitted video onto an image model with extra training stages. LLaVA-NeXT added multi-image support with tiling. None handled all three cleanly.

## 核心概念

### The OneVision token budget  | OneVision token 预算

LLaVA-OneVision picks a unified visual-token budget of approximately 3000-4000 tokens per sample, allocated differently per scenario:

- Single image / 单图: AnyRes-9 (3x3 tiles + thumbnail), each tile at 384 with 729 patches, aggressive bilinear pooling 2x2 → 182 per tile. Total: 9 * 182 + 182 = 1820 tokens. Or AnyRes-4 at 729-per-tile = 2916 + 729.
- Multi-image / 多图: each image at moderate resolution (384, no tiling), 729 tokens with no pooling. Budget 6 images → 4374 tokens.
- Video / 视频: 32 frames at 384 resolution with aggressive 3x3 bilinear pool → 81 tokens per frame. Total: 32 * 81 = 2592 tokens.

The allocation maintains roughly constant total tokens. The LLM never sees a batch that blows its context. The encoder produces different geometry per scenario, but the LLM consumes the same budget.

> **【中文解读】** 核心思想：总 token 预算保持恒定（约3000-4000），但分配方式因场景而异。单图用 AnyRes 切片+池化，多图用中等分辨率无池化，视频用低分辨率+激进池化但更多帧。LLM 看到的总 token 数始终在预算内。

### The three-stage curriculum  | 三阶段课程学习

LLaVA-OneVision trains in three stages:

1. Single-image SFT (stage SI) / 单图指令微调. All data is single-image-plus-text. Train on high-resolution AnyRes input. This teaches perception, OCR, and fine-grained understanding. Uses LLaVA-NeXT data plus OneVision-specific single-image data.
2. OneVision SFT (stage OV) / 统一指令微调. Mix single-image + multi-image + video (uniformly sampled frames). Train on the unified token budget. This teaches the model to handle heterogeneous batch shapes. No weight reset — continues from stage SI.
3. Task transfer (stage TT) / 任务迁移. Continue with a target task mix, typically heavier on multi-image or video depending on product. Optional fine-tune for deployment.

Critical: the curriculum order matters. Training video-first or multi-image-first produces worse image performance than single-image-first, even with the same data. The paper ablates this explicitly.

> **【中文解读】** 课程顺序至关重要：先单图、再多图+视频、最后任务迁移。如果先训练视频或多图，单图性能会下降。这是因为单图训练建立了感知基础，多图和视频的时序/空间推理需要以此为基础。

### Why curriculum works  | 为什么课程学习有效

Single-image training builds the perceptual base. Patch tokens carry fine-grained visual features; the LLM learns to integrate them with text. Multi-image and video introduce structural challenges (which image is which, what happened first) that are hard to learn without a strong perceptual base.

If you train all scenarios from scratch together, the model underfits perception (limited single-image data per batch) and overfits structure (lots of multi-image / video data). Result: a model that follows cross-image reasoning patterns but is visually shallow.

Curriculum ordering gives you perception strength from stage SI, then compositional/temporal reasoning from stage OV, without losing either.

> **【中文解读】** 如果同时训练所有场景，模型会欠拟合感知能力（每批中单图数据有限）而过拟合结构（大量多图/视频数据），导致模型能做跨图推理但视觉理解浅薄。课程学习先建立感知基础，再叠加组合/时序推理，两者都不损失。

### Emergent cross-scenario skills  | 涌现的跨场景能力

The LLaVA-OneVision paper reports three emergent capabilities:

1. Multi-camera reasoning / 多摄像头推理. Trained on multi-image + video separately; at inference, asked to reason about a multi-camera driving scene. The model correctly integrates the views despite never seeing that exact format in training.
2. Set-of-mark prompting / 标记提示. User annotates objects in an image with numbered marks; the model reasons about "what is mark 3 doing relative to mark 7." Trained on neither marks nor annotation; learned from the combination of spatial grounding + multi-image reference.
3. iPhone-screenshot agent / 手机截图代理. User provides a screenshot of an iPhone screen and asks to plan the next click. Trained on UI screenshots, video of user workflows, and multi-image before/after pairs. Generalizes to the agent use case.

These are not trained tasks; they emerge from the curriculum's compositional structure.

> **【拓展：涌现能力的工程启示】** 涌现能力意味着统一模型的价值超越各专家之和。多摄像头推理能力可用于安防监控、自动驾驶；标记提示可用于图像标注工具；手机截图代理可用于 UI 自动化测试。这些都不是显式训练的，而是课程学习的"副产品"。

### Visual-token pooling  | 视觉 token 池化

The token budget requires pooling. OneVision uses bilinear interpolation on the 2D patch grid: 24x24 = 576 patches becomes 12x12 = 144 (2x factor) or 8x8 = 64 (3x factor). Pooling is done in patch-grid space, not token space, to preserve locality.

The choice of pooling factor per scenario is itself a hyperparameter. Less pooling = more tokens = richer representation. More pooling = fewer tokens = more frames / images fit.

> **【中文解读】** 池化在 2D 补丁网格空间进行（而非 token 空间），以保留空间局部性。池化因子是每个场景的超参数：少池化=更多 token=更丰富表示；多池化=更少 token=可容纳更多帧/图像。

### LLaVA-OneVision-1.5

The 2025 follow-up (LLaVA-OneVision-1.5, arXiv 2509.23661) is "fully open" in training data, model weights, and code. Matches the proprietary gap on some benchmarks and democratizes the recipe. Same curriculum, more data, better base LLM. No architecture change.

### Contrast with Qwen2.5-VL  | 与 Qwen2.5-VL 对比

Qwen2.5-VL (Lesson 12.09) makes different choices. It uses M-RoPE and dynamic FPS instead of fixed pooling. Its budget scales with input — a 1-minute video uses more tokens than a 5-second video. LLaVA-OneVision fixes the budget and scales the pooling. Both work; they trade configurability for predictability.

> **【中文解读】** Qwen2.5-VL 用 M-RoPE 和动态帧率，token 预算随输入缩放；LLaVA-OneVision 固定预算、调整池化。两种策略各有优劣：前者灵活但成本不可预测，后者成本可控但可能浪费或不足。

## 动手实践

`code/main.py` is a curriculum and budget planner for a OneVision-style VLM. Given a token budget per sample and a target scenario mix (say 40% single-image, 30% multi-image, 30% video), it:

- Allocates resolution, pooling factor, and frames per scenario.  | 为每个场景分配分辨率、池化因子和帧数。
- Checks that every scenario fits within the shared budget.  | 检查每个场景是否在共享预算内。
- Reports expected token count, LLM FLOPs, and which scenarios are under-tokenized.  | 报告预期 token 数、LLM FLOPs 和哪些场景 token 不足。
- Prints a stage-by-stage training schedule.  | 打印逐阶段训练计划。

## 部署上线

This lesson produces `outputs/skill-onevision-budget-planner.md`. Given a target task distribution and a per-sample budget, it emits the AnyRes factor, per-frame pooling, video frame count, and curriculum stage weights. Use this whenever you train or fine-tune a unified-scenario VLM.

> **【中文解读】** 本课产出 OneVision 预算规划工具。给定目标任务分布和每样本预算，输出 AnyRes 因子、帧级池化、视频帧数和课程阶段权重。适用于训练或微调统一场景 VLM。

## 练习题

1. Your product supports 80% single-image, 10% multi-image (2-4 images), 10% video (8-16 frames). Design the token budget. Where would you put the extra budget you save from not doing heavy multi-image?
   | 产品支持 80% 单图、10% 多图（2-4张）、10% 视频（8-16帧）。设计 token 预算。从轻量多图中省下的预算放在哪？

2. Read LLaVA-OneVision Section 4.3 (emergent capabilities). Propose a fourth emergent skill the curriculum would likely unlock but the paper did not report.
   | 阅读 LLaVA-OneVision 第 4.3 节（涌现能力）。提出课程学习可能解锁但论文未报告的第四种涌现技能。

3. Swap the curriculum order — train multi-image first, then single-image, then video. Predict which benchmarks degrade and why.
   | 交换课程顺序——先多图，再单图，最后视频。预测哪些基准会下降以及原因。

4. The paper reports video benchmarks trained on only 8 frames per sample. Does that generalize to 30-second videos at inference? What breaks first — the token budget or the temporal reasoning?
   | 论文报告视频基准只用每样本8帧训练。这对推理时的30秒视频泛化吗？先崩溃的是 token 预算还是时序推理？

5. Bilinear pooling of 24x24 patches to 12x12 is a 4x reduction per dim. Implement the pooling in stdlib Python and verify that the mean over each 2x2 block matches the bilinear output.
   | 将 24x24 补丁双线性池化为 12x12 是每维 4 倍缩减。用标准库 Python 实现池化，验证每个 2x2 块的均值与双线性输出一致。

## 关键术语

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| OneVision scenario | "Single-image, multi-image, or video" | One of three input shapes the unified VLM handles; the budget stays constant across | 统一 VLM 处理的三种输入形态之一，预算在场景间保持恒定 | |
| Token budget | "How many tokens per sample" | Total visual tokens the LLM sees per training / inference sample, typically 3000-4000 | LLM 每样本看到的总视觉 token 数，通常 3000-4000 | |
| Curriculum | "Training order" | Stage ordering (single-image → multi-image → video) chosen for emergent transfer | 课程学习：按单图→多图→视频顺序训练，促进技能迁移 | |
| Bilinear pooling | "Token shrink" | Applying bilinear interpolation to the patch grid (2D) to reduce token count while preserving locality | 在补丁网格上做双线性插值，减少 token 数并保留空间局部性 | |
| Emergent skill | "Not trained, still works" | Capability that appears at inference without matching training data, due to curriculum composition | 课程学习组合带来的未训练即涌现的能力 | |
| AnyRes-k | "k-tile setup" | k sub-tiles of fixed resolution plus one thumbnail, typical k ∈ {4, 9} | k 个固定分辨率子切片加一个缩略图 | |
| Task transfer | "Cross-scenario generalization" | Skills learned on single-image that apply to video (and vice versa) via shared backbone | 通过共享骨干网络，单图技能迁移到视频（反之亦然） | |

## 延伸阅读

- [Li et al. — LLaVA-OneVision (arXiv:2408.03326)](https://arxiv.org/abs/2408.03326) | LLaVA-OneVision 原始论文
- [LLaVA-OneVision-1.5: Fully Open Framework (arXiv:2509.23661)](https://arxiv.org/abs/2509.23661) | 完全开源版本
- [Lin et al. — Video-LLaVA (arXiv:2311.10122)](https://arxiv.org/abs/2311.10122) | Video-LLaVA 视频多模态
- [Lin et al. — VILA (arXiv:2312.07533)](https://arxiv.org/abs/2312.07533) | VILA 多图像模型
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191) | Qwen2-VL 对比参考
