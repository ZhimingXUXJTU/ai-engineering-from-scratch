# Qwen-VL Family and Dynamic-FPS Video | Qwen-VL 系列与动态帧率视频

> The Qwen-VL family — Qwen-VL (2023), Qwen2-VL (2024), Qwen2.5-VL (2025), Qwen3-VL (2025) — is the most influential open vision-language model lineage in 2026. Each generation made a single decisive architectural bet that the rest of the open ecosystem copied within twelve months: native dynamic resolution via M-RoPE, dynamic-FPS sampling with absolute time alignment, window attention in the ViT, and structured agent output formats. By Qwen3-VL, the recipe had stabilized: a 2D-RoPE-ViT encoder with native-aspect-ratio inputs, an MLP projector into a large Qwen3 language base, and training stages that emphasized OCR, grounding, and agent behavior as first-class targets. This lesson reads the family chronologically so you understand why every knob is where it is.

> **【中文解读】** Qwen-VL 系列是 2026 年最有影响力的开源视觉语言模型家族。每一代都做出了一个关键架构决策，被开源社区在 12 个月内效仿：M-RoPE 原生动态分辨率、动态帧率采样+绝对时间对齐、ViT 窗口注意力、结构化代理输出格式。

> **【拓展：Qwen-VL 的产业生态位】** Qwen-VL 系列在中英文双语场景、GUI 代理、OCR 和视频理解方面具有显著优势。在金融场景中，Qwen2.5-VL 可用于理解中文财务报表、发票 OCR、以及监控视频分析。其结构化 JSON 输出使其可以直接集成到 Agent 工作流中。

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, M-RoPE encoder + dynamic-FPS sampler)  | **语言：Python（标准库，M-RoPE 编码器 + 动态帧率采样器）**
**Prerequisites:** Phase 12 · 06 (patch-n'-pack)  | **前置：阶段12第06课（补丁打包）**
**Time:** ~120 minutes  | **时长：约120分钟**

## 学习目标

- Compute M-RoPE's three-axis rotations (temporal, height, width) and explain why all three are needed.  | 计算 M-RoPE 的三轴旋转（时间、高度、宽度），解释为什么三者都需要。
- Pick a dynamic-FPS sampling strategy for a video and reason about tokens-per-second vs event-detection accuracy.  | 为视频选择动态帧率采样策略，权衡每秒 token 数与事件检测精度。
- Name the four Qwen-VL generational upgrades in order and what each enabled.  | 按顺序列举 Qwen-VL 四代升级及各自带来的能力。
- Wire a Qwen2.5-VL-style JSON agent output format and parse structured tool calls from a VLM response.  | 构造 Qwen2.5-VL 风格的 JSON 代理输出格式，解析 VLM 响应中的结构化工具调用。

## 问题背景

Qwen-VL shipped in August 2023 as a direct response to LLaVA-1.5 and BLIP-2. The gap the Qwen team targeted was threefold: resolution, video, and structured output.

Resolution: LLaVA-1.5 ran at 336x336. Fine for photos, useless for a Chinese-language invoice or a dense spreadsheet screenshot. Qwen-VL's first innovation was 448x448 and grounded bounding-box output, letting the model point at things.

Video: Video-LLaMA stacked per-frame encoders and fed them to the LLM. It worked for short clips, not for multi-minute videos where the temporal axis is the signal. The Qwen team wanted a single encoder that understood time.

Structured output: LLaVA emitted free-form text. An agent needs JSON. Qwen-VL trained on explicit JSON output formats including bounding-box coordinates as text.

Every Qwen-VL generation extends one of these three axes.

> **【中文解读】** Qwen-VL 针对 LLaVA-1.5 的三大不足发起挑战：(1) 分辨率——336x336 无法处理中文发票或密集表格截图；(2) 视频——Video-LLaMA 只能处理短片段；(3) 结构化输出——LLaVA 输出自由文本，代理需要 JSON。每一代 Qwen-VL 都在这三个轴上延伸。

## 核心概念

### Qwen-VL (August 2023)  | Qwen-VL 第一代

The first generation: OpenCLIP ViT-bigG/14 as encoder (2.5B params), LLama-compatible Q-Former (1-step with 256 queries), Qwen-7B base. Contributions:

- 448x448 resolution (then SOTA for an open VLM).  | 448x448 分辨率（当时开源 VLM 的 SOTA）。
- Grounding / 定位: trained on image-text pairs with explicit coordinate-token output. "The cat is at <box>(112, 204), (280, 344)</box>".  | 在图文对上训练坐标 token 输出。
- Chinese + English multilingual training from the start.  | 从一开始就支持中英双语训练。

Benchmarks at the time: competitive with GPT-4V on English, dominant on Chinese. The grounding supervision was the real headline.

> **【中文解读】** Qwen-VL 第一代的突破：448x448 分辨率（超越 LLaVA 的 336x336）、定位能力（输出边界框坐标）、中英双语。在中文基准上显著领先。

### Qwen2-VL (September 2024) — M-RoPE and native resolution  | Qwen2-VL：M-RoPE 与原生分辨率

Qwen2-VL replaced the fixed-resolution + Q-Former stack with a natively dynamic-resolution ViT encoder. Key changes:

- Native dynamic resolution / 原生动态分辨率. The ViT accepts any HxW divisible by 28 (patch 14 with 2x spatial merge). An image at 1120x672 (40x24 merged patches) produces 960 visual tokens. No resize, no tiling, no thumbnail.
- M-RoPE (Multimodal RoPE) / 多模态旋转位置编码. Each token carries a 3D position (t, h, w) instead of 1D. For images t=0, for video t = frame_index. RoPE rotates query/key vectors by a frequency per axis. No positional embedding table.
- MLP projector / MLP 投影器. Drop the Q-Former; use a 2-layer MLP on the merged patch tokens.  | 放弃 Q-Former，使用 2 层 MLP。
- Video with dynamic FPS / 动态帧率视频. Video sampled at 1-2 FPS by default, but the model accepts arbitrary frame counts.  | 默认 1-2 FPS 采样，但接受任意帧数。

Result: Qwen2-VL-7B matched GPT-4o on several multimodal benchmarks and beat it on DocVQA (94.5 vs 88.4). The architecture change was the decisive move.

> **【中文解读】** Qwen2-VL 的核心架构变更：去掉固定分辨率+Q-Former，换成原生动态分辨率 ViT + M-RoPE + MLP 投影器。M-RoPE 为每个 token 赋予 3D 位置（时间、高度、宽度），使同一位置编码能统一处理文本、图像和视频。7B 参数就匹配了 GPT-4o 的多模态基准。

### Qwen2.5-VL (February 2025) — dynamic FPS + absolute time  | Qwen2.5-VL：动态帧率 + 绝对时间

Qwen2.5-VL's big shift was video. Dynamic FPS is not just "sample more frames when needed." The paper formalized:

- Absolute time tokens / 绝对时间 token. Instead of positional indices (frame 0, 1, 2...), use actual timestamps. "At 0:04, the cat jumps." The model sees `<time>0.04</time>` tokens interleaved with frame tokens.  | 使用真实时间戳而非帧索引。
- Dynamic FPS / 动态帧率. Sample at 1 FPS for slow footage, 4+ FPS for action. The user or trainer chooses; M-RoPE adapts.  | 慢速画面用1FPS，动作场景用4+FPS。
- Window attention in ViT / ViT 窗口注意力. Spatial attention is windowed (local within blocks) for throughput; global attention every few layers.  | 空间注意力在窗口内进行，每隔几层加全局注意力。
- Explicit JSON output format / 显式 JSON 输出格式. Trained on tool-call data: `{"tool": "click", "coords": [380, 220]}`. Agent-ready out of the box.  | 训练工具调用数据，开箱即用的代理能力。
- MRoPE-v2 scaling / MRoPE-v2 缩放. Positions scale with max input size so a 10-minute video does not run out of frequency range.  | 位置随最大输入尺寸缩放。

Benchmarks: Qwen2.5-VL-72B beats GPT-4o on most video benchmarks, matches Gemini 2.0 on documents, and sets the open-model SOTA for GUI grounding (ScreenSpot: 84% accuracy vs 38% for GPT-4o).

> **【中文解读】** Qwen2.5-VL 的突破在于视频理解：绝对时间 token 让模型知道"第4秒猫跳了"，动态帧率让模型在动作密集时自动提高采样率，窗口注意力提升 ViT 吞吐量。72B 版本在视频基准上超越 GPT-4o，GUI 定位精度（ScreenSpot 84%）远超 GPT-4o（38%）。

> **【拓展：结构化输出对 Agent 工程的意义】** Qwen2.5-VL 的结构化 JSON 输出使其能直接作为计算机使用代理（Computer Use Agent）的视觉感知模块。在金融场景中，这意味着 VLM 可以输出结构化的"点击坐标"或"提取的字段"，直接被下游系统消费，无需正则表达式解析。

### Qwen3-VL (November 2025)

Qwen3-VL is an incremental upgrade that consolidates rather than reinvents: larger LLM backbone (Qwen3-72B), expanded training data, improved OCR, stronger reasoning via the Qwen3 "thinking mode." The ViT and M-RoPE stay. The paper focuses on data and training improvements over architecture.

The lineage takeaway: by 2025 the Qwen-VL architecture had stabilized. Additional generations scale compute and data, not primitives.

> **【中文解读】** Qwen3-VL 是增量升级而非重新发明：更大的 LLM 骨干、更多训练数据、更好的 OCR、更强的推理（Qwen3 "思考模式"）。ViT 和 M-RoPE 保持不变。到 2025 年，Qwen-VL 架构已经稳定，后续版本主要通过扩大规模和优化数据来提升。

### M-RoPE mathematically  | M-RoPE 数学原理

Classical RoPE rotates a query `q` of dimension `d` by position `m` using paired coordinates:

```
q_rot[2i]   = q[2i]   * cos(m * theta_i) - q[2i+1] * sin(m * theta_i)   # 经典 RoPE 旋转
q_rot[2i+1] = q[2i]   * sin(m * theta_i) + q[2i+1] * cos(m * theta_i)
theta_i     = 10000^(-2i/d)                                                 # 频率基
```

M-RoPE splits the hidden dim into three bands. Say `d = 96`. Assign 32 dims to temporal, 32 to height, 32 to width. Each band rotates by its own axis position. A patch at (t=5, h=10, w=20) gets rotations `R_t(5)`, `R_h(10)`, `R_w(20)` applied to its three bands.

Text tokens use `t = text_index, h = 0, w = 0` (or a normalized choice), keeping compatibility. Video frames use `t = frame_time, h = row, w = col`. Single images use `t = 0`.

The benefit: one position encoding handles text, image, and video without branching code or different position tables.

> **【中文解读】** M-RoPE 将隐藏维度分为三个频段（时间、高度、宽度），每个频段按各自的轴位置旋转。文本 token 用 (text_index, 0, 0)，视频帧用 (frame_time, row, col)，单图用 (0, row, col)。好处：一套位置编码统一处理文本、图像和视频。

### Dynamic-FPS sampling logic  | 动态帧率采样逻辑

Given a video of duration `T` seconds and a target-tokens budget `B`:

1. Compute the maximum FPS you can afford: `fps_max = B / (T * tokens_per_frame)`.  | 计算可承受的最大帧率。
2. Pick a target FPS from `{1, 2, 4, 8}` that satisfies `fps <= fps_max`.  | 从候选帧率中选择。
3. If motion is high (optical-flow heuristic or explicit user request), pick higher FPS. If motion is low, pick lower.  | 运动量大则高帧率，运动量小则低帧率。
4. Sample uniformly at the chosen FPS; insert `<time>t</time>` tokens between frames.  | 均匀采样并在帧间插入时间 token。

Qwen2.5-VL trains this logic implicitly; at inference the user controls via `fps` parameter. A 60-second action sequence at 4 FPS with 81 tokens per frame = 19440 tokens, manageable in a 32k context.

> **【中文解读】** 动态帧率的核心思想：根据视频时长、token 预算和运动量，自动选择最优帧率。60秒动作场景在 4FPS 下产生 19440 token，可在 32k 上下文中处理。

### Structured agent output  | 结构化代理输出

Qwen2.5-VL's agent training explicitly targets structured tool calls:

```
{
  "tool": "mouse_click",          # 工具名称
  "coords": [1024, 512],          # 点击坐标
  "button": "left",               # 鼠标按钮
  "modifier": null                # 修饰键
}
```

Parsing is deterministic: JSON.parse over the model's output. Compare to free-form "click at (1024, 512)" which required regex and ambiguity handling. The shift is why Qwen2.5-VL's ScreenSpot scores jumped from Qwen2-VL's 55% to 84%.

> **【中文解读】** 结构化输出让 VLM 可以直接发出可解析的工具调用（如点击坐标），无需正则表达式。这是 ScreenSpot 精度从 55% 跳到 84% 的关键原因。

## 动手实践

`code/main.py` implements:

- M-RoPE position computation for a packed sequence mixing text, image patches, and video frames.  | 混合文本、图像补丁和视频帧的 M-RoPE 位置计算。
- Dynamic-FPS sampler: given (duration, budget, motion_level), pick FPS and emit frame timestamps.  | 动态帧率采样器。
- A toy Qwen2.5-VL JSON-output parser that handles tool-call responses with coordinate fields.  | Qwen2.5-VL JSON 输出解析器。

## 部署上线

This lesson produces `outputs/skill-qwen-vl-pipeline-designer.md`. Given a video task (monitoring, agent, action recognition, accessibility), it emits the Qwen2.5-VL configuration (frame budget, FPS strategy, window-attention flag, agent-output mode) and a latency estimate. Use this whenever you deploy a Qwen-VL-family model for a video product.

> **【中文解读】** 本课产出 Qwen-VL pipeline 设计工具。给定视频任务（监控、代理、动作识别、无障碍），输出 Qwen2.5-VL 配置（帧预算、FPS 策略、窗口注意力标志、代理输出模式）和延迟估计。

## 练习题

1. Compute M-RoPE rotations for a patch at (t=3, h=5, w=7) with hidden 48 (16 per band, base theta 10000). Show the rotation angles for the first three pairs in each band.
   | 计算 (t=3, h=5, w=7) 补丁的 M-RoPE 旋转，隐藏维度48（每频段16），基数10000。展示每频段前三对的旋转角度。

2. A 10-minute security-camera recording at 1 FPS produces how many frames? At 384 resolution with 3x pool, how many total tokens? Does Qwen2.5-VL's default 32k context handle it?
   | 10分钟安防摄像头录像在 1FPS 下产生多少帧？384分辨率+3x池化后多少 token？Qwen2.5-VL 默认 32k 上下文能处理吗？

3. Pick FPS for a 30-second tennis rally vs a 30-second recipe demo vs a 30-second UI-agent recording. Justify each with the dynamic-FPS logic.
   | 为 30 秒网球比赛、30 秒食谱演示、30 秒 UI 代理录像选择帧率。用动态帧率逻辑论证每个选择。

4. Qwen2.5-VL drops the Q-Former entirely. Why does a simple MLP work in 2025 but not in 2023? (Hint: data scale and encoder quality.)
   | Qwen2.5-VL 完全去掉了 Q-Former。为什么 MLP 在 2025 年可行但 2023 年不行？（提示：数据规模和编码器质量。）

5. Parse three Qwen2.5-VL JSON tool-call outputs into Python dicts. What fails for malformed JSON and what recovery strategy does the Qwen cookbook recommend?
   | 将三个 Qwen2.5-VL JSON 工具调用输出解析为 Python 字典。畸形 JSON 会出什么问题？Qwen 食谱推荐的恢复策略是什么？

## 关键术语

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| M-RoPE | "Multimodal RoPE" | 3D rotary position embedding with temporal, height, and width bands in the hidden dim | 三维旋转位置编码，隐藏维度分时间、高度、宽度三个频段 | |
| Dynamic FPS | "Smart sampling" | Frame sampling rate chosen per video based on motion, duration, and token budget | 根据运动量、时长和 token 预算动态选择帧率 | |
| Absolute time token | "Timestamp token" | `<time>t</time>` interleaved in the sequence so the model sees actual seconds not frame index | 在序列中插入真实时间戳 token | |
| Window attention | "Local attention" | Spatial self-attention restricted to small windows for speed; global attention added periodically | 空间自注意力限制在小窗口内加速，周期性加入全局注意力 | |
| Structured agent output | "JSON mode" | Training data supervision teaching the VLM to emit parseable JSON with coords and tool names | 训练 VLM 输出可解析的 JSON（含坐标和工具名） | |
| min_pixels / max_pixels | "Resolution bounds" | Per-request Qwen2.5-VL controls bounding total pixel count and therefore token count | 按请求控制最小/最大像素数从而控制 token 数 | |
| Grounding | "Point-at-it" | Outputting bounding-box coordinates as text tokens; used since Qwen-VL v1 | 输出边界框坐标作为文本 token，从 Qwen-VL v1 开始支持 | |

## 延伸阅读

- [Bai et al. — Qwen-VL (arXiv:2308.12966)](https://arxiv.org/abs/2308.12966) | Qwen-VL 第一代
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191) | Qwen2-VL M-RoPE
- [Qwen Team — Qwen2.5-VL Technical Report (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923) | Qwen2.5-VL 动态帧率
- [Qwen Team — Qwen3-VL (arXiv:2511.21631)](https://arxiv.org/abs/2511.21631) | Qwen3-VL 增量升级
- [Zhu et al. — InternVL3 (arXiv:2504.10479)](https://arxiv.org/abs/2504.10479) | InternVL3 对比参考
