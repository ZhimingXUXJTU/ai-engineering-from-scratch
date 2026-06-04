# 音频语言模型 — Qwen2.5-Omni、Audio Flamingo、GPT-4o Audio

> 2026 年的音频语言模型能理解语音+环境声+音乐。Qwen2.5-Omni-7B 在 MMAU-Pro 上匹配 GPT-4o Audio，Audio Flamingo Next 在 LongAudioBench 上超越 Gemini 2.5 Pro。开源与闭源的差距基本消失。

> **【中文解读】** 2026 年的音频语言模型能理解语音+环境声+音乐。Qwen2.5-Omni-7B 在 MMAU-Pro 上匹配 GPT-4o Audio，Audio Flamingo Next 在 LongAudioBench 上超越 Gemini 2.5 Pro。开源与闭源的差距基本消失。

> **【拓展：音频大模型的新时代】** 音频语言模型将 LLM 的推理能力扩展到音频领域，能同时理解语音内容、识别环境声音、分析音乐结构。这是多模态 AI 的重要方向。

**类型：** 学习
**语言：** Python
**前置条件：** 阶段 6 · 04（ASR），阶段 12 · 03（视觉语言模型），阶段 7 · 10（音频 Transformer）
**时长：** 约 45 分钟

## 问题引入

你有 5 秒音频：狗叫声，有人喊"停下！"，然后是沉默。有用的问题跨越多个维度：

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

- **转录。** "说了什么？"——ASR 领域。
- **语义推理。** "这个人有危险吗？"——需要联合理解狗叫 + 喊叫 + 沉默。
- **音乐推理。** "什么乐器演奏旋律？"
- **长音频检索。** "在这 90 分钟讲座中，讲师在哪里解释了梯度下降？"

一个模型用一个提示回答所有这些问题，就是**音频语言模型（LALM / ALM）**。与纯 ASR 不同：LALM 生成自由形式的自然语言答案，而不仅仅是转录。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![音频语言模型：音频编码器 + 投影器 + LLM 解码器](../assets/alm-architecture.svg)

### 三组件模板

每个 2026 年的 LALM 都有相同的骨架：

1. **音频编码器。** Whisper 编码器、BEATs、CLAP、WavLM 或每个模型的自定义编码器。
2. **投影器。** 线性层或 MLP，将音频编码器特征桥接到 LLM 的 token 嵌入空间。
3. **LLM。** 基于 Llama / Qwen / Gemma 的解码器。接收交织的文本 + 音频 token；生成文本。

训练：

- **阶段 1。** 冻结编码器 + LLM；仅在 ASR / 标注数据上训练投影器。
- **阶段 2。** 在指令跟随音频任务（QA、推理、音乐理解）上做全量 / LoRA 微调。
- **阶段 3（可选）。** 语音入/语音出添加语音解码器。Qwen2.5-Omni 和 AF3-Chat 做了这步。

### 2026 模型地图

| 模型 | 骨干 | 音频编码器 | 输出模态 | 访问 |
|------|------|-----------|----------|------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | 自定义 + Whisper | 文本 + 语音 | Apache-2.0 |
| Qwen3-Omni | Qwen3 | 自定义 | 文本 + 语音 | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | 文本 | NVIDIA 非商业 |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | 文本 | NVIDIA 非商业 |
| SALMONN | Vicuna | Whisper + BEATs | 文本 | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | 文本 | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | 文本 | Apache-2.0 |
| Gemini 2.5 Flash/Pro（闭源） | Gemini | 私有 | 文本 + 语音 | API |
| GPT-4o Audio（闭源） | GPT-4o | 私有 | 文本 + 语音 | API |

### 基准现实检查（2026）

**MMAU-Pro。** 1800 个 QA 对，涵盖语音 / 声音 / 音乐 / 混合。包含多音频子集。

| 模型 | 总体 | 语音 | 声音 | 音乐 | 多音频 |
|------|------|------|------|------|--------|
| Gemini 2.5 Pro | 约 60% | 73.4% | 51.9% | 64.9% | 约 22% |
| Gemini 2.5 Flash | 约 57% | 73.4% | 50.5% | 64.9% | 21.2% |
| GPT-4o Audio | 52.5% | — | — | — | 26.5% |
| Qwen2.5-Omni-7B | 52.2% | 57.4% | 47.6% | 61.5% | 约 20% |
| Audio Flamingo 3 | 约 54% | — | — | — | — |
| Audio Flamingo Next | LongAudioBench SOTA | — | — | — | — |

**多音频列对所有人都是致命的。** 4 选项多选题的随机概率 = 25%；大多数模型得分在那附近。LALM 仍然难以比较两个片段。

### LALM 在 2026 年哪里有用

- **呼叫中心录音合规审计。** "客服是否提到了必要的免责声明？"
- **无障碍。** 向听障用户描述声音事件（不仅仅是转录）。
- **内容审核。** 检测暴力语言 + 威胁语气 + 背景上下文。
- **播客 / 会议章节划分。** 语义摘要，不仅仅是说话人轮次。
- **音乐目录分析。** "找到所有 B 段有转调的曲目。"

### 哪里还没用

- 精细音乐理论（和弦级别以下）。
- 长对话中的说话人归因推理（超过 10 分钟性能下降）。
- 多音频比较（22-26% 几乎是随机）。
- 实时流式推理（大多数是离线批处理推理）。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

## 动手实现

### 步骤 1：查询 Qwen2.5-Omni

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

### 步骤 2：投影器模式

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

就这样。投影器通常是 1-3 个线性层。在 ASR 对（音频 -> 转录）上训练它是阶段 1 的预文本任务。

### 步骤 3：基准测试 MMAU / LongAudioBench

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

按类别（语音 / 声音 / 音乐 / 多音频）分别报告。汇总数字隐藏了模型的失败点。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

| 任务 | 2026 选择 |
|------|-----------|
| 自由音频 QA（开源） | Qwen2.5-Omni-7B |
| 最佳开源长音频 | Audio Flamingo Next |
| 最佳闭源 | Gemini 2.5 Pro |
| 语音入/语音出代理 | Qwen2.5-Omni 或 GPT-4o Audio |
| 音乐推理 | Audio Flamingo 3 或 2（音乐专用 AF-CLAP） |
| 呼叫中心审计 | Gemini 2.5 Pro 通过 API，配合你的政策文档 RAG |

## 陷阱

- **过度信任多音频。** 如果你的任务需要"哪个片段有 X"，随机级别的性能是真实的。
- **长音频退化。** 超过 10 分钟，大多数模型的说话人归因会崩溃。先做日志（第 6 课），再摘要。
- **静音幻觉。** 使用 Whisper 编码器的 LALM 继承了相同的 Whisper 风格问题。VAD 门控。
- **基准挑最好的。** 厂商博客突出最佳类别。自己运行 MMAU-Pro 多音频子集。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-alm-picker.md`。为给定音频理解任务选择 LALM + 基准子集 + 输出模态（文本 vs 语音）。

## 练习题

1. **简单。** 运行 `code/main.py` 查看玩具投影器模式 + 假 LALM 的（音频嵌入，文本 token）-> 输出 token 路由。
2. **中等。** 在 100 个 MMAU-Pro 语音项上评测 Qwen2.5-Omni-7B。与论文报告数字比较。
3. **困难。** 构建最小音频标注基线：BEATs 编码器 + 2 层投影器 + 冻结 Llama-3.2-1B。仅在 AudioCaps 上微调投影器。在 Clotho-AQA 上与 SALMONN 比较。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| LALM | 音频 ChatGPT | 音频编码器 + 投影器 + LLM 解码器。 |
| 投影器（Projector） | 适配器 | 将音频特征映射到 LLM 嵌入空间的小型 MLP。 |
| MMAU | 那个基准 | 10k 音频-QA 对，涵盖语音、声音、音乐。 |
| MMAU-Pro | 更难的 MMAU | 1800 个多音频 / 推理密集的问题。 |
| LongAudioBench | 长音频评估 | 多分钟片段带语义查询。 |
| 语音入/语音出 | 语音原生 | 模型直接接收和发出语音，不经文本中转。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Chu et al. (2024). Qwen2-Audio](https://arxiv.org/abs/2407.10759) —— 参考架构。
- [Alibaba (2025). Qwen2.5-Omni](https://huggingface.co/Qwen/Qwen2.5-Omni-7B) —— 语音入语音出。
- [NVIDIA (2025). Audio Flamingo 3](https://arxiv.org/abs/2507.08128) —— 开源长音频领军者。
- [NVIDIA (2026). Audio Flamingo Next](https://arxiv.org/abs/2604.10905) —— LongAudioBench SOTA。
- [Tang et al. (2023). SALMONN](https://arxiv.org/abs/2310.13289) —— 双编码器先驱。
- [MMAU-Pro 排行榜](https://mmaubenchmark.github.io/) —— 2026 年实时排名。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
