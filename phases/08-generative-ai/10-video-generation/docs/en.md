# Video Generation | 视频生成

> An image is a 2-D tensor. A video is a 3-D one. The theory is the same; the compute is 10-100x harder. OpenAI's Sora (Feb 2024) proved it was possible. By 2026 Veo 2, Kling 1.5, Runway Gen-3, Pika 2.0, and WAN 2.2 ship production video from text at 1080p — and the open-weights stack (CogVideoX, HunyuanVideo, Mochi-1, WAN 2.2) is 12 months behind.

> **【中文解读】** 图像是 2D 张量，视频是 3D 张量，理论相同但计算量高 10-100 倍。Sora 证明可行，到 2026 年多个商业产品（Veo 2、Kling、Runway）已能生成 1080p 视频。

> **【拓展：Sora 的影响】** OpenAI 的 Sora（2024年2月）是视频生成的里程碑，展示了扩散模型+Transformer 架构的强大能力。视频生成是 2024-2026 年 AI 最热门的赛道之一。

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 7 · 09 (ViT), Phase 8 · 06 (DDPM)
**Time:** ~45 minutes

## The Problem | 问题引入

A 10-second 1080p video at 24fps is 240 frames of 1920×1080×3 pixels. That's ~1.5 GB of raw data per clip. Pixel-space diffusion is infeasible. You need:

> 10 秒 1080p 24fps 视频是 240 帧 1920×1080×3 像素，约 1.5 GB 原始数据。像素空间扩散不可行。你需要：

1. **Spatiotemporal compression.** A VAE that encodes videos, not frames, into a sequence of spatial-temporal patches.
   **时空压缩。** 将视频（而非帧）编码为时空 patch 序列的 VAE。
2. **Temporal coherence.** Frames need to share content, lighting, and object identity over seconds. The net has to model motion.
   **时间连贯性。** 帧之间需要共享内容、光照和物体身份。
3. **Compute budget.** Video training is 10-100x more expensive than image for the same model size.
   **计算预算。** 视频训练比图像贵 10-100 倍。
4. **Conditioning.** Text, image (first-frame), audio, or another video. Most production models accept all four.
   **条件化。** 文本、图像（首帧）、音频或其他视频。

The architecture that solved this is the **Diffusion Transformer (DiT)** applied to spatiotemporal patches, trained on huge (prompt, caption, video) datasets. Same diffusion loss as Lesson 06.

> 解决这些的架构是**Diffusion Transformer (DiT)** 应用于时空 patch，在大规模数据集上训练。与第 06 课相同的扩散损失。

## The Concept | 核心概念

![Video diffusion: patchify, DiT, decode](../assets/video-generation.svg)

### Patchify

> ### Patch 化

Encode the video with a 3D VAE (learned spatiotemporal compression). The latent is shape `[T_latent, H_latent, W_latent, C_latent]`. Split into patches of size `[t_p, h_p, w_p]`. For Sora-style models, `t_p = 1` (per-frame patches) or `t_p = 2` (every two frames). A 10-second 1080p video compresses to ~20,000-100,000 patches.

> 用 3D VAE 编码视频。潜在表示形状为 `[T, H, W, C]`。切分为 `[t_p, h_p, w_p]` 大小的 patch。10 秒 1080p 视频压缩为约 2-10 万个 patch。

### Spatiotemporal DiT

> ### 时空 DiT

A transformer processes the flat sequence of patches. Each patch has a 3D positional embedding (time + y + x). Attention is usually factorized:

> Transformer 处理展平的 patch 序列。每个 patch 有 3D 位置编码（时间 + y + x）。注意力通常分解为：

- **Spatial attention** within each frame's patches.
  **空间注意力** 在每帧的 patch 内。
- **Temporal attention** across frames at the same spatial location.
  **时间注意力** 跨帧的相同空间位置。
- **Full 3D attention** is 16-100x more expensive; used only at low resolution or in research.
  **完整 3D 注意力** 贵 16-100 倍；仅在低分辨率或研究中使用。

> **【中文解读】** 视频生成的核心技术栈：(1) 3D VAE 将视频压缩为时空潜在表示；(2) 将潜在表示切分为时空 patch；(3) DiT（Diffusion Transformer）处理 patch 序列，使用 3D 位置编码；(4) 注意力通常分解为空间注意力和时间注意力以降低计算量。这与 Sora 的架构一致。

> **【拓展：Sora 架构与 DiT 在视频中的应用】** Sora 的核心是将 ViT 的 patch 化思想扩展到视频领域——将视频视为"时空 patch 序列"。DiT（Diffusion Transformer）用 Transformer 替代 U-Net 作为去噪网络，在视频生成中表现出更好的扩展性。开源实现如 CogVideoX、HunyuanVideo 和 WAN 2.2 都遵循这一架构。

### Text conditioning

> ### 文本条件化

Cross-attention with a large text encoder (T5-XXL for Sora, CogVideoX-5B uses T5-XXL). Long prompts matter — Sora's training set had GPT-generated dense re-captions averaging 200 tokens per clip.

> 用大型文本编码器做交叉注意力。长 prompt 很重要——Sora 的训练集有 GPT 生成的密集重标注，平均每片段 200 token。

### Training

> ### 训练

Standard diffusion loss (ε or v prediction) over spatiotemporal latents. Data: web video + ~100M curated clips + synthetic text captions. Compute: 10,000+ GPU hours for even a small research run; Sora-scale is 100,000+.

> 时空潜在表示上的标准扩散损失。数据：网络视频 + 约 1 亿精选片段 + 合成文本标注。计算：小规模研究需 1 万+ GPU 小时；Sora 规模是 10 万+。

## The 2026 production landscape | 2026 年生产格局

| Model / 模型 | Date | Max duration / 最长时长 | Max res / 最高分辨率 | Open weights? / 开源？ | Notable / 亮点 |
|-------|------|--------------|---------|---------------|---------|
| Sora (OpenAI) | 2024-02 | 60s | 1080p | No | First model to show world simulator properties at scale / 首个展示世界模拟器属性的模型 |
| Sora Turbo | 2024-12 | 20s | 1080p | No | Production Sora at 5x faster inference / 5 倍推理加速 |
| Veo 2 (Google) | 2024-12 | 8s | 4K | No | Highest quality + physics in 2025 / 2025 年最高质量 |
| Veo 3 | 2025 Q3 | 15s | 4K | No | Native audio and stronger camera control / 原生音频 |
| Kling 1.5 / 2.1 (Kuaishou) | 2024-2025 | 10s | 1080p | No | Best human motion in 2025 Q1 / 最佳人体运动 |
| Runway Gen-3 Alpha | 2024-06 | 10s | 768p | No | Professional video tools on top / 专业视频工具 |
| Pika 2.0 | 2024-10 | 5s | 1080p | No | Strongest character consistency / 最强角色一致性 |
| CogVideoX (THUDM) | 2024 | 10s | 720p | Yes (2B, 5B) | First open 5B-scale video / 首个开源 5B 视频 |
| HunyuanVideo (Tencent) | 2024-12 | 5s | 720p | Yes (13B) | Open SOTA late 2024 / 2024 年末开源 SOTA |
| Mochi-1 (Genmo) | 2024-10 | 5.4s | 480p | Yes (10B) | Most permissively licensed / 最宽松许可 |
| WAN 2.2 (Alibaba) | 2025-07 | 5s | 720p | Yes | Strongest open model mid-2025 / 2025 年中最强开源 |

Open weights are closing the gap faster than in the image space: HunyuanVideo + WAN 2.2 LoRAs already power most open-source workflows by mid-2026.

> 开源权重正在比图像领域更快地缩小差距。

## Build It | 动手实现

`code/main.py` simulates the core spatiotemporal DiT idea: patchify a small synthetic video, add a per-patch position embedding, and denoise the whole sequence with a transformer-style attention over patches. No numpy; pure Python. We show that temporal coherence emerges even in 1-D when adjacent-frame patches share a denoiser and position embeddings.

### Step 1: patchify a synthetic 1-D "video"

```python
def make_video(T_frames=8, rng=None):
    # a "video" is a sequence of 1-D values following a smooth trajectory
    base = rng.gauss(0, 1)
    return [base + 0.3 * t + rng.gauss(0, 0.1) for t in range(T_frames)]
```

### Step 2: position embedding per frame

```python
def pos_embed(t, dim):
    return sinusoidal(t, dim)
```

### Step 3: denoiser sees the whole sequence

Instead of denoising each frame independently, our tiny net concatenates all frame values + their position embeddings and predicts the noise for all frames jointly.

### Step 4: temporal coherence test

After training, sample a video. Measure the frame-to-frame delta. If the model has learned temporal structure, the deltas stay smaller than sampling each frame independently.

## Pitfalls | 常见陷阱

- **Independent per-frame sampling = flicker.** If you run image diffusion on each frame separately, the output flickers because each frame's noise is independent. Video diffusion fixes this by coupling the frames through attention or shared noise.
- **Naive 3D attention = OOM.** Full 3D attention on a 10-second 1080p latent is hundreds of billions of operations. Factorize into spatial + temporal.
- **Data captioning matters more than size.** Sora's main upgrade over prior work was training on ~10x more detailed captions (GPT-4 re-labelled clips). OpenAI's technical report is explicit on this.
- **First-frame conditioning.** Most production models also accept an image as the first frame. This is "image-to-video" mode; training includes this variant.
- **Physics drift.** Long clips (>10s) accumulate subtle inconsistencies. Sliding-window generation + keyframe anchoring helps.

## Use It | 用框架实现

| Use case / 用途 | 2026 pick / 2026 选择 |
|----------|-----------|
| Highest-quality text-to-video, hosted / 最高质量托管 | Veo 3 or Sora |
| Camera-controlled cinematic / 相机控制电影感 | Runway Gen-3 with motion brushes |
| Character consistency across clips / 跨片段角色一致 | Pika 2.0 or Kling 2.1 |
| Open weights, fast fine-tune / 开源快速微调 | WAN 2.2 + LoRA |
| Image-to-video / 图生视频 | WAN 2.2-I2V, Kling 2.1 I2V, or Runway |
| Audio-to-video lip sync / 音频对口型 | Veo 3 (native audio) or a dedicated lip-sync model |
| Video editing / 视频编辑 | Runway Act-Two, Kling Motion Brush, Flux-Kontext (still-frame) |

Cost per second of video at quality parity has dropped 20x between 2024 and 2026.

> 质量平价下每秒视频成本在 2024 到 2026 年间降低了 20 倍。

## Ship It | 产出物

Save `outputs/skill-video-brief.md`. Skill takes a video brief (duration, aspect ratio, style, camera plan, subject consistency, audio) and outputs: model + hosting, prompt scaffolding (camera language, subject description, motion descriptors), seed + reproducibility protocol, and a frame-level QA checklist.

## Exercises | 练习题

1. **Easy.** In `code/main.py`, compare frame-to-frame delta for (a) independent per-frame sampling, (b) joint sequence sampling. Report the mean and variance of the deltas.
2. **Medium.** Add a first-frame condition: pin frame 0 to a given value and sample the rest. Measure how the pinned value propagates.
3. **Hard.** Use HuggingFace diffusers to run CogVideoX-2B on a local GPU. Time 20 inference steps at 720p for a 6-second clip. Profile the spatiotemporal attention to identify the bottleneck.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Video VAE | "3-D VAE" | Encoder that compresses `(T, H, W, C)` → spatiotemporal latent. |
| Patches | "The tokens" | Fixed-size 3-D blocks of the latent; input to the DiT. |
| Factorized attention | "Spatial + temporal" | Run attention over space, then over time; skip full 3-D attention. |
| Image-to-video (I2V) | "Animate this photo" | Model takes an image + text, outputs a video that starts from it. |
| Keyframe conditioning | "Anchor frames" | Pin specific frames to control the video's arc. |
| Motion brush | "Directional hint" | UI input where the user paints motion vectors onto the image. |
| Re-captioning | "Dense captions" | Using an LLM to re-label training clips with detailed prompts. |
| Flicker | "Temporal artifact" | Frame-to-frame inconsistency; fixed with coupled denoising. |

## Production note: video latents are a memory-bandwidth problem | 生产笔记：视频潜在表示是内存带宽问题

A 10-second 1080p clip at 24 fps is 240 frames × 1920 × 1080 × 3 ≈ 1.5 GB of raw pixels. After a 4× video VAE compression (`2 × spatial × 2 × temporal`) the latent is ~100 MB per request. Run this through a spatiotemporal DiT for 30 steps at batch 1 and you are moving ~3 GB/step through HBM — memory bandwidth, not FLOPs, is the bottleneck.

Three production knobs, all straight from production-inference literature inference chapter:

- **TP across the DiT.** Text-to-video models are routinely ≥10B params. TP=4 across 4 H100s is standard; PP=2 × TP=2 for 405B-class models. Latency per step drops roughly linearly with TP up to the all-reduce wall.
- **Frame batching = continuous batching.** At generation time, video is conceptually a batch of frames linked by attention. Continuous batching (in-flight scheduling) applies: start rendering frame `t+1` while frame `t-1` is being returned, if the model architecture allows sliding-window generation.
- **Clip-level prefill cache.** For image-to-video, the first-frame conditioning is analogous to an LLM's prompt prefill: compute it once, reuse across the temporal decoder passes. This is effectively a KV-cache for video.

## Further Reading | 延伸阅读

- [Brooks et al. (2024). Video generation models as world simulators](https://openai.com/index/video-generation-models-as-world-simulators/) — Sora technical report.
- [Yang et al. (2024). CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer](https://arxiv.org/abs/2408.06072) — CogVideoX.
- [Kong et al. (2024). HunyuanVideo: A Systematic Framework for Large Video Generative Models](https://arxiv.org/abs/2412.03603) — HunyuanVideo.
- [Genmo (2024). Mochi-1 Technical Report](https://www.genmo.ai/blog/mochi) — Mochi-1.
- [Alibaba (2025). WAN 2.2](https://wanvideo.io/) — open SOTA mid-2025.
- [Ho, Salimans, Gritsenko et al. (2022). Video Diffusion Models](https://arxiv.org/abs/2204.03458) — the seminal video diffusion paper.
- [Blattmann et al. (2023). Align your Latents (Video LDM)](https://arxiv.org/abs/2304.08818) — Stable Video Diffusion's ancestor.
