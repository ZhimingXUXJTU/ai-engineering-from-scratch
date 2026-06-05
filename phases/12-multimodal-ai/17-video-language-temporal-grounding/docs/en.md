# Video-Language Models: Temporal Tokens and Grounding | 视频语言模型：时间 Token 与时序定位

> Video is not a stack of photos. A 5-second clip has causal ordering, action verbs, and event timing that an image model cannot represent. Video-LLaMA (Zhang et al., June 2023) shipped the first open video-LLM with audio-visual grounding. VideoChat and Video-LLaVA scaled the pattern. By 2025 Qwen2.5-VL's TMRoPE closed the gap with frontier proprietary models. Each system solved temporal tokens differently — Q-former per clip, concat-pool per frame, TMRoPE per token. This lesson reads the patterns, builds a uniform-vs-dynamic frame sampler, and evaluates on temporal grounding tasks.

> **【中文解读】** 视频不是一堆照片的堆叠。5 秒的短视频包含因果顺序、动作动词和事件时间信息，这是图像模型无法表示的。从 Video-LLaMA（2023）到 Qwen2.5-VL（2025），视频 VLM 的核心突破在于时间位置编码——TMRoPE 让模型能看到"4.2 秒"而非"第 15 帧"。

**Type:** Build
**Languages:** Python (stdlib, frame sampler + temporal-grounding evaluator)
**Prerequisites:** Phase 12 · 08 (LLaVA-OneVision)
**Time:** ~180 minutes

## Learning Objectives

- Explain why temporal positional encoding changes video VLM performance independently of the vision encoder.
  中文翻译：解释为什么时间位置编码独立于视觉编码器影响视频 VLM 性能。
- Compare uniform, dynamic-FPS, and event-driven frame sampling on tokens-per-second vs grounding accuracy.
  中文翻译：比较均匀、动态 FPS 和事件驱动帧采样在每秒 token 数与定位准确率上的表现。
- Describe Q-former-per-clip (Video-LLaMA) vs pooled-per-frame (Video-LLaVA) vs M-RoPE-per-token (Qwen2.5-VL) designs.
  中文翻译：描述每片段 Q-former（Video-LLaMA）vs 每帧池化（Video-LLaVA）vs 每帧 token 的 M-RoPE（Qwen2.5-VL）设计。
- Name the four video benchmarks: VideoMME, TempCompass, EgoSchema, Video-MMMU.
  中文翻译：列举四个视频基准测试：VideoMME、TempCompass、EgoSchema、Video-MMMU。

## The Problem | 问题引入

A 1-minute video at 30 FPS is 1800 frames. At 196 visual tokens per frame (ViT-B at 224), that is 352k tokens — larger than any 2024-era LLM context.

> 1 分钟 30 FPS 的视频有 1800 帧。以每帧 196 个视觉 token（ViT-B 在 224 分辨率下）计算，共 352k token——超过了 2024 年任何 LLM 的上下文长度。

> **【中文解读】** 1 分钟 30FPS 的视频有 1800 帧，每帧 196 个视觉 token，总计 352k token——远超 2024 年 LLM 的上下文窗口。三种压缩策略各有取舍：采样帧损失时间细节，池化损失空间细节，Q-former 两者都损失一点但节省 token。

Three reduction strategies exist:

> 三种压缩策略：

1. Subsample frames (1-8 FPS depending on content).
   中文翻译：子采样帧（根据内容 1-8 FPS）。
2. Pool each frame's patch tokens aggressively (3x3 or 4x4 bilinear pool).
   中文翻译：对每帧的 patch token 进行激进池化（3x3 或 4x4 双线性池化）。
3. Compress via a Q-former that takes a 16-frame clip and outputs 64 tokens.
   中文翻译：通过 Q-former 压缩，将 16 帧片段映射为 64 个 token。

Each trade-off is different. Subsampling loses temporal detail. Pooling loses spatial detail. Q-former loses both a little but saves tokens.

> 每种权衡不同。子采样丢失时间细节。池化丢失空间细节。Q-former 两者都损失一点但节省 token。

Temporal position encoding is the other axis: how does the model know frame 5 came before frame 6? Options include simple 1D temporal RoPE (Video-LLaMA), learned temporal embeddings (Video-LLaVA), and TMRoPE (Qwen2.5-VL, full 3D).

> 时间位置编码是另一个维度：模型怎么知道第 5 帧在第 6 帧之前？选项包括简单的 1D 时间 RoPE（Video-LLaMA）、可学习时间嵌入（Video-LLaVA）和 TMRoPE（Qwen2.5-VL，完整 3D）。

## The Concept | 核心概念

> **【中文解读】** 视频语言时序定位（Temporal Grounding）是在视频中精确找到与自然语言描述对应的时间段。例如"找到他说谢谢的片段"需要模型理解视频的时序结构和语言的时间指代。这是视频理解中的精细任务。

> **【拓展：时序定位的应用场景】** 时序定位在视频搜索、自动剪辑、体育分析、安防监控等场景有广泛应用。技术上分为 moment retrieval（定位单个片段）和 highlight detection（定位高光时刻）。当前最好的模型在 Charades-STA 数据集上达到约 60% mIoU。


### Video-LLaMA: Q-former per clip + audio branch

Video-LLaMA (2023) was the first open video-LLM. Architecture:

> Video-LLaMA（2023）是第一个开放视频 LLM。架构：

- 16-frame clips at 2 FPS (so 8 seconds).
  中文翻译：16 帧片段，2 FPS（即 8 秒）。
- Per-frame ViT features -> Video Q-former that cross-attends over all 16 frames -> 32 learned queries -> LLM.
  中文翻译：每帧 ViT 特征 → Video Q-former 对所有 16 帧做交叉注意力 → 32 个学习查询 → LLM。
- Parallel audio branch: waveform -> ImageBind audio encoder -> Audio Q-former -> 32 queries -> LLM.
  中文翻译：并行音频分支：波形 → ImageBind 音频编码器 → Audio Q-former → 32 个查询 → LLM。

Strength: audio-visual joint reasoning. Weakness: fixed clip length, no arbitrary time grounding.

> 优势：音视频联合推理。劣势：固定片段长度，无法做任意时间定位。

### VideoChat and Video-LLaVA

VideoChat kept the Video-LLaMA idea but dropped audio and simplified. Video-LLaVA (Lin et al., 2023) trained a single visual encoder on both images and video frames ("alignment before projection"), giving a unified representation. Both are frozen-CLIP-encoder + MLP + LLM.

> VideoChat 保留了 Video-LLaMA 的思路但去掉了音频并简化了。Video-LLaVA 在图像和视频帧上训练单一视觉编码器（"对齐先于投影"），给出统一表示。两者都是冻结 CLIP 编码器 + MLP + LLM。

Neither handles long video. Both are 8-16 frame systems.

> 两者都不能处理长视频。都是 8-16 帧系统。

### Qwen2.5-VL and TMRoPE

Qwen2.5-VL introduced TMRoPE — Temporal-Modality Rotary Position Embedding. Each patch token carries an (t, h, w) position where t is the actual timestamp (not frame index).

> Qwen2.5-VL 引入了 TMRoPE——时间-模态旋转位置编码。每个 patch token 携带 (t, h, w) 位置，其中 t 是实际时间戳（非帧索引）。

Key differences from simple temporal embedding:

> 与简单时间嵌入的关键区别：

- Absolute time, not index. The model sees "at 4.2 seconds" not "at frame 15."
  中文翻译：绝对时间而非索引。模型看到的是"4.2 秒"而非"第 15 帧"。
- Per-token rotation, not per-clip. Each visual token rotates independently by its timestamp.
  中文翻译：逐 token 旋转而非逐片段。每个视觉 token 按时间戳独立旋转。
- Compatible with dynamic FPS. If you sample at 2 FPS here and 4 FPS there, TMRoPE handles the uneven spacing natively.
  中文翻译：兼容动态 FPS。如果某处 2 FPS 采样、另一处 4 FPS 采样，TMRoPE 原生处理不均匀间隔。

TMRoPE enables "at what second does the cat jump?" queries. The model can output "at 4.2 seconds." Video-LLaMA could only say "early in the clip."

> TMRoPE 支持"猫在几秒跳的？"这类查询。模型可以输出"4.2 秒"。Video-LLaMA 只能说"在片段早期"。

> **【中文解读】** TMRoPE 是 Qwen2.5-VL 的关键创新：每个视觉 token 携带 (t, h, w) 位置信息，其中 t 是真实时间戳而非帧索引。这意味着模型看到的是"4.2 秒"而不是"第 15 帧"，并且能自然处理动态帧率下不均匀的时间间隔。

> **【拓展：TMRoPE 在金融视频分析中的应用】** TMRoPE 的绝对时间定位能力对金融场景至关重要：分析财报发布会视频时，可以精确定位"CEO 何时提到营收增长"；分析交易监控视频时，可以标记异常事件的时间点。这比传统的"视频前段/后段"描述精确得多。

### Frame sampling strategies

Uniform: sample N frames evenly over duration. Simple, loses motion peaks.

> 均匀采样：在时长内均匀采样 N 帧。简单，但丢失运动峰值。

Dynamic FPS: sample adaptively based on motion intensity. Optical flow or frame differencing picks high-motion segments for denser sampling. Qwen2.5-VL trains on this.

> 动态 FPS：根据运动强度自适应采样。光流或帧差分选择高运动段进行密集采样。Qwen2.5-VL 在此上训练。

Event-driven: run a lightweight detector, sample more where action happens. Used by VideoAgent.

> 事件驱动：运行轻量级检测器，在动作发生处密集采样。VideoAgent 使用。

Keyframe + context: sample at shot boundaries + a few adjacent frames. Used for cinematic content.

> 关键帧 + 上下文：在镜头边界采样 + 少量相邻帧。用于电影内容。

> **【中文解读】** 四种帧采样策略：均匀采样（简单但丢失运动峰值）、动态 FPS（根据运动强度自适应采样）、事件驱动（在动作发生处密集采样）、关键帧+上下文（在镜头边界采样）。2026 年最佳实践是动态 FPS + 3x3 双线性池化。

### Pooling per frame

At 1 FPS and 576 tokens per frame, a 5-minute clip is 172,800 tokens. Doable with Qwen2.5-VL-72B's 128k context but expensive.

> 1 FPS、每帧 576 token 下，5 分钟片段是 172,800 个 token。Qwen2.5-VL-72B 的 128k 上下文可以处理，但成本高。

3x3 bilinear pool reduces to 64 tokens per frame -> 19,200 tokens for 5 minutes. Sweet spot for most tasks.

> 3x3 双线性池化降至每帧 64 token → 5 分钟 19,200 token。大多数任务的甜点。

Pool more aggressively (6x6 -> 16 tokens per frame) for agent workflows where spatial detail matters less.

> 更激进地池化（6x6 → 每帧 16 token）适用于空间细节不太重要的 Agent 工作流。

### The four video benchmarks

- VideoMME: comprehensive video understanding, short + medium + long.
  中文翻译：VideoMME：综合视频理解，短+中+长。
- TempCompass: fine-grained temporal reasoning, "before" / "after" questions.
  中文翻译：TempCompass：细粒度时间推理，"之前"/"之后"问题。
- EgoSchema: long-horizon first-person video.
  中文翻译：EgoSchema：长程第一人称视频。
- Video-MMMU: multimodal multi-discipline video questions.
  中文翻译：Video-MMMU：多模态多学科视频问题。

A full video-VLM evaluation hits all four. They stress different axes — TempCompass is all about ordering, EgoSchema is about 3+ minute reasoning, VideoMME spans durations.

> 完整的视频 VLM 评估需要覆盖全部四个基准。它们测试不同维度——TempCompass 关注时序，EgoSchema 关注 3 分钟以上的推理，VideoMME 跨越不同时长。

### Grounding output formats

Output formats for temporal grounding:

> 时序定位的输出格式：

- Free text: "The cat jumps around the 4-second mark." Easy to parse but imprecise.
  中文翻译：自由文本："猫在 4 秒左右跳起。"容易解析但不精确。
- Structured JSON: `{"event": "jump", "start": 4.1, "end": 4.3}`. Qwen2.5-VL trains this.
  中文翻译：结构化 JSON：`{"event": "jump", "start": 4.1, "end": 4.3}`。Qwen2.5-VL 训练此格式。
- Token-based: special `<time>4.1</time>` tokens interleaved with the answer. Qwen2.5-VL's internal format.
  中文翻译：基于 token：特殊 `<time>4.1</time>` token 与回答交错。Qwen2.5-VL 的内部格式。

Token-based is most accurate for downstream use. Qwen2.5-VL's JSON output format parses directly.

> 基于 token 的格式在下游使用中最准确。Qwen2.5-VL 的 JSON 输出格式可直接解析。

### 2026 best practice

For video VLMs in 2026:

> 2026 年视频 VLM 的最佳实践：

- Encoder: SigLIP 2 with M-RoPE or TMRoPE (Qwen2.5-VL).
  中文翻译：编码器：带 M-RoPE 或 TMRoPE 的 SigLIP 2（Qwen2.5-VL）。
- Frame sampling: dynamic FPS (1-4 depending on motion) with max-frame cap.
  中文翻译：帧采样：动态 FPS（根据运动 1-4），有最大帧数上限。
- Per-frame pooling: 3x3 bilinear.
  中文翻译：每帧池化：3x3 双线性。
- Output: structured JSON with time + event fields.
  中文翻译：输出：带时间和事件字段的结构化 JSON。
- Benchmarks: VideoMME + TempCompass for general; EgoSchema for long-horizon.
  中文翻译：基准测试：通用用 VideoMME + TempCompass；长程用 EgoSchema。

## Use It | 用框架实现

`code/main.py` includes:

> `code/main.py` 包含：

- Uniform and dynamic-FPS frame samplers.
  中文翻译：均匀和动态 FPS 帧采样器。
- A toy temporal-grounding evaluator: given a "ground truth" event at time T and a model output, score accuracy with tolerance.
  中文翻译：一个玩具时序定位评估器：给定时间 T 的"真实"事件和模型输出，在容差范围内评分。
- A comparison across Video-LLaMA (16 frames, Q-former), Video-LLaVA (8 frames, MLP), Qwen2.5-VL (dynamic FPS + TMRoPE).
  中文翻译：Video-LLaMA（16 帧，Q-former）、Video-LLaVA（8 帧，MLP）、Qwen2.5-VL（动态 FPS + TMRoPE）的对比。

## Ship It | 产出物

This lesson produces `outputs/skill-video-vlm-frame-planner.md`. Given a video task (monitoring, action recognition, temporal grounding, summarization), it picks the frame sampler, pooling factor, output format, and expected accuracy tier.

> 本课产出 `outputs/skill-video-vlm-frame-planner.md`。给定视频任务（监控、动作识别、时序定位、摘要），它选择帧采样器、池化因子、输出格式和预期准确率等级。

## Exercises | 练习题

1. For a 3-minute cooking demo, pick uniform vs dynamic FPS. Justify with a token count. 对于一个 3 分钟的烹饪演示，选择均匀采样还是动态 FPS？用 token 数量来论证。

2. TMRoPE adds what specifically that a simple temporal embedding table cannot do? TMRoPE 具体添加了什么简单的时间嵌入表无法做到的功能？

3. Write a JSON schema for temporal grounding that a VLM can learn to emit. Include error cases. 设计一个 VLM 可以学习输出的时序定位 JSON schema，包含错误情况。

4. Read Video-LLaVA's Section 3 on "Alignment Before Projection." Why is this better than training separate image and video encoders? 阅读 Video-LLaVA 第 3 节"对齐先于投影"，为什么这比分别训练图像和视频编码器更好？

5. Given the VideoMME leaderboard, what is the gap between the top open model and the top proprietary model as of 2026? How much of that gap is attributable to temporal encoding vs base LLM scale? 根据 VideoMME 排行榜，2026 年顶级开源模型和顶级闭源模型之间的差距有多大？多少归因于时间编码，多少归因于 LLM 规模？

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Temporal grounding | "Time-localized answers" 时序定位 | VLM outputs a specific timestamp range for when an event happens VLM 输出事件发生的具体时间戳范围 | |
| TMRoPE | "Time-Multimodal RoPE" 时间-多模态旋转位置编码 | 3D rotary position with absolute timestamps, used by Qwen2.5-VL 带绝对时间戳的 3D 旋转位置编码 | |
| Dynamic FPS | "Motion-aware sampling" 运动感知采样 | Sample more frames in high-motion segments, fewer in static ones 高运动段密集采样，静态段稀疏采样 | |
| Frame pooling | "Spatial compress per frame" 逐帧空间压缩 | Reduce patches per frame with bilinear interpolation before the LLM LLM 前用双线性插值减少每帧 patch 数 | |
| Video Q-former | "Clip compressor" 片段压缩器 | Cross-attention bottleneck mapping N frames to K learned queries 将 N 帧映射为 K 个学习查询的交叉注意力瓶颈 | |
| VideoMME | "Video bench" 视频基准 | Comprehensive short/medium/long video benchmark, 2500+ samples 覆盖短/中/长视频的综合基准测试 | |

## Further Reading | 延伸阅读

- [Zhang et al. — Video-LLaMA (arXiv:2306.02858)](https://arxiv.org/abs/2306.02858)
- [Li et al. — VideoChat (arXiv:2305.06355)](https://arxiv.org/abs/2305.06355)
- [Lin et al. — Video-LLaVA (arXiv:2311.10122)](https://arxiv.org/abs/2311.10122)
- [Qwen Team — Qwen2.5-VL (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923)
- [Lin et al. — VILA-1.5 (arXiv:2312.07533)](https://arxiv.org/abs/2312.07533)
