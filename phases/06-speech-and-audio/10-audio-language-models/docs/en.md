# Audio-Language Models — Qwen2.5-Omni, Audio Flamingo, GPT-4o Audio | 音频语言模型

> 2026 audio-language models reason over speech + environmental sound + music. Qwen2.5-Omni-7B matches GPT-4o Audio on MMAU-Pro. Audio Flamingo Next beats Gemini 2.5 Pro on LongAudioBench. The gap between open and closed is essentially closed — except on multi-audio tasks, where everyone is near random.

> **【中文解读】** 2026 年的音频语言模型能理解语音+环境声+音乐。Qwen2.5-Omni-7B 在 MMAU-Pro 上匹配 GPT-4o Audio，Audio Flamingo Next 在 LongAudioBench 上超越 Gemini 2.5 Pro。开源与闭源的差距基本消失。

> **【拓展：音频大模型的新时代】** 音频语言模型将 LLM 的推理能力扩展到音频领域，能同时理解语音内容、识别环境声音、分析音乐结构。这是多模态 AI 的重要方向。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 12 · 03 (Vision-Language Models), Phase 7 · 10 (Audio Transformers) | **前置知识:** 阶段 6 · 04（ASR），阶段 12 · 03（视觉语言模型），阶段 7 · 10（音频 Transformer）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## The Problem | 问题引入

You have 5 seconds of audio: dog barks, someone yells "stop!", then silence. Useful questions span multiple axes:

> 你有 5 秒音频：狗叫，有人喊"stop!"，然后是静音。有用的问题跨越多个维度：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

- **Transcription.** "What was said?" — ASR territory.
  **转录。** "说了什么？"——ASR 领域。
- **Semantic reasoning.** "Is the person in danger?" — requires joint understanding of the bark + yell + silence.
  **语义推理。** "这个人有危险吗？"——需要联合理解狗叫 + 喊叫 + 静音。
- **Music reasoning.** "What instruments play the melody?"
  **音乐推理。** "什么乐器演奏旋律？"
- **Long-audio retrieval.** "Where in this 90-minute lecture did the instructor explain gradient descent?"
  **长音频检索。** "在这 90 分钟讲座中，讲师在哪里解释了梯度下降？"

A single model that answers all of these with one prompt is an **audio-language model** (LALM / ALM). Separate from pure ASR: LALMs produce free-form natural-language answers, not just transcripts.

> 用一个提示回答所有这些问题的单一模型就是**音频语言模型**（LALM / ALM）。区别于纯 ASR：LALM 生成自由形式的自然语言答案，而不仅仅是转录文本。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![Audio-language model: audio encoder + projector + LLM decoder](../assets/alm-architecture.svg)

### The three-component template

Every 2026 LALM has the same skeleton:

> ### 三组件模板

> 2026 年每个 LALM 都有相同的骨架：

1. **Audio encoder.** Whisper encoder · BEATs · CLAP · WavLM · or a custom encoder per model.
   **音频编码器。** Whisper 编码器 · BEATs · CLAP · WavLM · 或每个模型的自定义编码器。
2. **Projector.** Linear or MLP bridging audio-encoder features into the LLM's token embedding space.
   **投影器。** 将音频编码器特征桥接到 LLM 的 token 嵌入空间的线性层或 MLP。
3. **LLM.** Llama / Qwen / Gemma-based decoder. Takes interleaved text + audio tokens; generates text.
   **LLM。** 基于 Llama / Qwen / Gemma 的解码器。接收交织的文本 + 音频 token；生成文本。

Training:

> 训练：

- **Stage 1.** Freeze encoder + LLM; train projector only on ASR / captioning data.
  **阶段 1。** 冻结编码器 + LLM；仅在 ASR/标注数据上训练投影器。
- **Stage 2.** Full / LoRA fine-tune on instruction-following audio tasks (QA, reasoning, music understanding).
  **阶段 2。** 在指令跟随音频任务（QA、推理、音乐理解）上进行全参数/LoRA 微调。
- **Stage 3 (optional).** Voice-in / voice-out adds a speech decoder. Qwen2.5-Omni and AF3-Chat do this.
  **阶段 3（可选）。** 语音入/语音出添加语音解码器。Qwen2.5-Omni 和 AF3-Chat 实现了这一点。

### The 2026 model map

> ### 2026 年模型地图

| Model | Backbone | Audio encoder | Output modality | Access |
|-------|----------|---------------|-----------------|--------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | Custom + Whisper | text + speech | Apache-2.0 |
| Qwen3-Omni | Qwen3 | Custom | text + speech | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | text | NVIDIA non-commercial |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | text | NVIDIA non-commercial |
| SALMONN | Vicuna | Whisper + BEATs | text | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | text | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | text | Apache-2.0 |
| Gemini 2.5 Flash/Pro (closed) | Gemini | proprietary | text + speech | API |
| GPT-4o Audio (closed) | GPT-4o | proprietary | text + speech | API |

| 模型 | 骨干 | 音频编码器 | 输出模态 | 访问方式 |
|------|------|-----------|---------|---------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | 自定义 + Whisper | 文本+语音 | Apache-2.0 |
| Qwen3-Omni | Qwen3 | 自定义 | 文本+语音 | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | 文本 | NVIDIA 非商业 |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | 文本 | NVIDIA 非商业 |
| SALMONN | Vicuna | Whisper + BEATs | 文本 | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | 文本 | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | 文本 | Apache-2.0 |
| Gemini 2.5 Flash/Pro（闭源） | Gemini | 专有 | 文本+语音 | API |
| GPT-4o Audio（闭源） | GPT-4o | 专有 | 文本+语音 | API |

### Benchmark reality check (2026)

**MMAU-Pro.** 1800 QA pairs covering speech / sound / music / mixed. Multi-audio subset included.

| Model | Overall | Speech | Sound | Music | Multi-audio |
|-------|---------|--------|-------|-------|-------------|
| Gemini 2.5 Pro | ~60% | 73.4% | 51.9% | 64.9% | ~22% |
| Gemini 2.5 Flash | ~57% | 73.4% | 50.5% | 64.9% | 21.2% |
| GPT-4o Audio | 52.5% | — | — | — | 26.5% |
| Qwen2.5-Omni-7B | 52.2% | 57.4% | 47.6% | 61.5% | ~20% |
| Audio Flamingo 3 | ~54% | — | — | — | — |
| Audio Flamingo Next | SOTA on LongAudioBench | — | — | — | — |

The **multi-audio column is damning for everyone.** Random chance on 4-option multiple choice = 25%; most models score around there. LALMs still struggle to compare two clips.

> **多音频列对所有人都是致命的。** 4 选 1 多选题的随机概率 = 25%；大多数模型得分就在那附近。LALM 仍然难以比较两个音频片段。

### Where LALMs are useful in 2026

- **Compliance audit of call-center recordings.** "Did the agent mention the required disclosure?"
  **合规审计通话录音。** "客服是否提到了必要的免责声明？"
- **Accessibility.** Describe sound events to deaf users (not just transcription).
  **无障碍。** 为听障用户描述声音事件（不只是转录）。
- **Content moderation.** Detect violent language + threatening tone + background context.
  **内容审核。** 检测暴力语言 + 威胁语气 + 背景上下文。
- **Podcast / meeting chaptering.** Semantic summary, not just speaker turns.
  **播客/会议章节化。** 语义摘要，不只是说话人轮次。
- **Music catalog analysis.** "Find all tracks with a B-section key change."
  **音乐目录分析。** "找出所有 B 段有转调的曲目。"

### Where they are NOT (yet) useful

- Fine-grained music theory (below chord-level).
  精细音乐理论（和弦级别以下）。
- Speaker-attributed reasoning over long conversations (degrades past 10 minutes).
  长对话中的说话人归因推理（超过 10 分钟退化）。
- Multi-audio comparison (22-26% is barely above random).
  多音频比较（22-26% 几乎等于随机）。
- Real-time streaming reasoning (most are offline batch inference).
  实时流式推理（大多数是离线批量推理）。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。




## Build It | 动手实现

### Step 1: query Qwen2.5-Omni

```python
from transformers import AutoModelForCausalLM, AutoProcessor

processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-Omni-7B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-Omni-7B", torch_dtype="auto")

audio, sr = load_wav("clip.wav", sr=16000)
messages = [{
    "role": "user",
    "content": [
        {"type": "audio", "audio": audio},
        {"type": "text", "text": "What sounds do you hear, and what's happening?"},
    ],
}]
inputs = processor.apply_chat_template(messages, tokenize=True, return_tensors="pt")
output = model.generate(**inputs, max_new_tokens=200)
print(processor.decode(output[0], skip_special_tokens=True))
```

### Step 2: the projector pattern

```python
import torch.nn as nn

class AudioProjector(nn.Module):
    def __init__(self, audio_dim=1280, llm_dim=4096):
        super().__init__()
        self.down = nn.Linear(audio_dim, llm_dim)
        self.act = nn.GELU()
        self.up = nn.Linear(llm_dim, llm_dim)

    def forward(self, audio_features):
        return self.up(self.act(self.down(audio_features)))
```

That's it. The projector is usually 1-3 linear layers. Training it on ASR pairs (audio → transcript) is the Stage-1 pretext task.

### Step 3: benchmarking MMAU / LongAudioBench

```python
from datasets import load_dataset
mmau = load_dataset("MMAU/MMAU-Pro")

correct = 0
for item in mmau["test"]:
    answer = call_model(item["audio"], item["question"], item["choices"])
    if answer == item["correct_choice"]:
        correct += 1
print(f"Accuracy: {correct / len(mmau['test']):.3f}")
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


Report per-category (speech / sound / music / multi-audio) separately. Aggregate numbers hide where the model fails.




> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## Use It | 用框架实现

| Task | 2026 pick |
|------|-----------|
| Free-form audio QA (open) | Qwen2.5-Omni-7B |
| Best open on long audio | Audio Flamingo Next |
| Best closed | Gemini 2.5 Pro |
| Voice-in / voice-out agent | Qwen2.5-Omni or GPT-4o Audio |
| Music reasoning | Audio Flamingo 3 or 2 (music-specialized AF-CLAP) |
| Call-center audit | Gemini 2.5 Pro via API, with RAG over your policy docs |

| 任务 | 2026 年选择 |
|------|-----------|
| 自由格式音频 QA（开源） | Qwen2.5-Omni-7B |
| 最佳开源长音频 | Audio Flamingo Next |
| 最佳闭源 | Gemini 2.5 Pro |
| 语音入/语音出智能体 | Qwen2.5-Omni 或 GPT-4o Audio |
| 音乐推理 | Audio Flamingo 3 或 2（音乐专用 AF-CLAP） |
| 呼叫中心审计 | Gemini 2.5 Pro via API，配合策略文档 RAG |



## Pitfalls

> 常见陷阱

- **Over-trust on multi-audio.** If your task needs "which clip has X," random-chance-level performance is real.
  **过度信任多音频。** 如果你的任务需要"哪个片段有 X"，随机水平的性能是真实的。
- **Long-audio degradation.** Past 10 minutes, most models' speaker attribution breaks. Diarize first (Lesson 6), then summarize.
  **长音频退化。** 超过 10 分钟，大多数模型的说话人归因失效。先做日志化（第 6 课），再总结。
- **Hallucinations on silence.** Same Whisper-style issue inherited by LALMs that use Whisper encoder. VAD-gate.
  **静音上的幻觉。** 与使用 Whisper 编码器的 LALM 继承的 Whisper 式问题相同。用 VAD 过滤。
- **Benchmark cherry-picking.** Vendor blog posts highlight best-case categories. Run MMAU-Pro multi-audio subset yourself.
  **基准挑挑拣拣。** 供应商博客文章突出最佳类别。自己运行 MMAU-Pro 多音频子集。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-alm-picker.md`. Pick LALM + benchmark subset + output-modality (text vs speech) for a given audio-understanding task.

> 保存为 `outputs/skill-alm-picker.md`。为给定的音频理解任务选择 LALM + 基准子集 + 输出模态（文本 vs 语音）。

## Exercises | 练习题

1. **Easy.** Run `code/main.py` to see a toy projector pattern + fake LALM routing of (audio-embedding, text-tokens) → output tokens.
   **简单。** 运行 `code/main.py` 查看玩具投影器模式 + 假 LALM 路由（音频嵌入，文本 token）→ 输出 token。
2. **Medium.** Score Qwen2.5-Omni-7B on 100 MMAU-Pro speech items. Compare to the paper's reported number.
   **中等。** 在 100 个 MMAU-Pro 语音项上评分 Qwen2.5-Omni-7B。与论文报告的数字比较。
3. **Hard.** Build a minimal audio-captioning baseline: BEATs encoder + 2-layer projector + frozen Llama-3.2-1B. Fine-tune only the projector on AudioCaps. Compare to SALMONN on Clotho-AQA.
   **困难。** 构建最小音频标注基线：BEATs 编码器 + 2 层投影器 + 冻结 Llama-3.2-1B。仅在 AudioCaps 上微调投影器。在 Clotho-AQA 上与 SALMONN 比较。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| LALM | Audio ChatGPT | Audio encoder + projector + LLM decoder. |
| Projector | Adapter | Small MLP mapping audio features into LLM embedding space. |
| MMAU | The benchmark | 10k audio-QA pairs across speech, sound, music. |
| MMAU-Pro | Harder MMAU | 1800 multi-audio / reasoning-heavy questions. |
| LongAudioBench | Long-form eval | Multi-minute clips with semantic queries. |
| Voice-in / voice-out | Speech-native | Model ingests speech and emits speech without text detour. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| LALM | 音频 ChatGPT | 音频编码器 + 投影器 + LLM 解码器。 |
| 投影器 | 适配器 | 将音频特征映射到 LLM 嵌入空间的小型 MLP。 |
| MMAU | 那个基准 | 跨语音、声音、音乐的 1 万音频-QA 对。 |
| MMAU-Pro | 更难的 MMAU | 1800 个多音频/重推理问题。 |
| LongAudioBench | 长音频评估 | 带语义查询的多分钟片段。 |
| 语音入/语音出 | 原生语音 | 模型直接接收和输出语音，不经文本。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Chu et al. (2024). Qwen2-Audio](https://arxiv.org/abs/2407.10759) — reference architecture.
  Chu 等 (2024). Qwen2-Audio——参考架构。
- [Alibaba (2025). Qwen2.5-Omni](https://huggingface.co/Qwen/Qwen2.5-Omni-7B) — speech-in-speech-out.
  Alibaba (2025). Qwen2.5-Omni——语音入语音出。
- [NVIDIA (2025). Audio Flamingo 3](https://arxiv.org/abs/2507.08128) — the open long-audio leader.
  NVIDIA (2025). Audio Flamingo 3——开源长音频领先者。
- [NVIDIA (2026). Audio Flamingo Next](https://arxiv.org/abs/2604.10905) — LongAudioBench SOTA.
  NVIDIA (2026). Audio Flamingo Next——LongAudioBench SOTA。
- [Tang et al. (2023). SALMONN](https://arxiv.org/abs/2310.13289) — dual-encoder pioneer.
  Tang 等 (2023). SALMONN——双编码器先驱。
- [MMAU-Pro leaderboard](https://mmaubenchmark.github.io/) — live 2026 rankings.
  MMAU-Pro 排行榜——2026 年实时排名。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。

