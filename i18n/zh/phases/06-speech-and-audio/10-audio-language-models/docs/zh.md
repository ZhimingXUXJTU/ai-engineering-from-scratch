# 音频语言模型  Qwen2.5Omni,音频弗拉门戈,GPT-4o音频模型

> 2026年音频语言模型推理语音+环境声音+音乐.Qwen2.5-Omni-7B与MMAU-Pro的GPT-4o音频相匹配.Audio Flamingo Next在LongAudioBench上超过了Gemini 2.5 Pro.开放和关闭之间的差距基本上是关闭的除了多音频任务,每个人都几乎是随机的.

> **【中文解读】**2026年的音频语言模型能理解语音+环境声+音乐──Qwen2.5-Omni-7B 在 MMAU-Pro 上匹配GPT-4o音频,Audio Flamingo 下在 LongAudioBench 上超越双子 2.5 Pro──开源与闭源差距基本消失──

> **【拓展：音频大模型的新时代】**音频语言模型将将LLM的推理能力扩展到音频领域,同时理解语音内容,识别环境声音,分析音乐结构.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 12 · 03 (Vision-Language Models), Phase 7 · 10 (Audio Transformers) | **前置知识:** 阶段 6 · 04（ASR），阶段 12 · 03（视觉语言模型），阶段 7 · 10（音频 Transformer）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## 问题 问题引入

您有5秒的音频:狗吠叫,有人喊"停止!",然后沉默.

> 你有5秒音频:狗叫,有人叫"停止!",然后是静音.

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

- **Transcription.**"有什么说?" 阿斯里亚地区.
  **转录。**"说了什么?" ASR领域.
- **Semantic reasoning.**"人是否处于危险之中?" 需要共同理解叫+喊叫+沉默.
  **语义推理。**"这个人有危险吗?"需要共同理解狗叫 + 喊 + 静音.
- **Music reasoning.**"什么乐器演奏这首歌曲?"
  **音乐推理。**"什么乐器演奏旋律?"
- **Long-audio retrieval.**"在这90分钟的讲座中,教师在哪里解释了梯度下降?"
  **长音频检索。**"在这90分钟的讲座中,讲师在哪里解释了梯度下降?"

一个单个模型,只能用一个提示来回答所有这些问题,**audio-language model**单独与纯ASR:LALM产生自由形式的自然语言答案,而不是仅仅是转录.

> 用一个提示回答所有这些问题,**音频语言模型**语:LALM 生成自由形式的自然语言答案,而不仅仅是转录文本.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Audio-language model: audio encoder + projector + LLM decoder](../assets/alm-architecture.svg)

### 三个组成部分的模板

每个2026年的LALM都具有相同的骨:

> ### 三组件模板

> 2026年,每一个LALM都会有相同的骨架:

1. **Audio encoder.**语编码器 · BEATs · CLAP · WavLM ·或每款车型的定制编码器.
   **音频编码器。**语编码器 · 跳动 · 快播 · 波动 · 或每个模型的自定义编码器──
2. **Projector.**线性或MLP桥接音频编码器功能在LLM的代币嵌入空间.
   **投影器。**将音频编码器特征桥接到LLM的代币嵌入空间的线性层或MLP.
3. **LLM.**基于Llama/Qwen/Gemma的解码器. 接收交织的文本 + 音频代币;生成文本.
   **LLM。**基于Llama / Qwen / Gemma 的解码器──接收交织的文本 + 音频代币;生成文本──

培训:

> 训练:

- **Stage 1.**结编码器 + LLM;仅使用ASR/字幕数据的火车投影机.
  **阶段 1。**结编码器 + LLM;仅在ASR/标注数据上训练投影器──
- **Stage 2.**完成/LoRA细节调整后续指令的音频任务 (QA,推理,音乐理解).
  **阶段 2。**在命令跟随音频任务 (QA、推理、音乐理解) 上进行全参数/LoRA 微调.
- **Stage 3 (optional).**语音输入/发音增加语音解码器. Qwen2.5Omni和AF3聊天这样做.
  **阶段 3（可选）。**语音入/语音出添加语音解码器──Qwen2.5Omni 和 AF3-Chat 实现了这一点──

### 2026年模型地图

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

### 实实况检查标准 (2026)

**MMAU-Pro.**1800 个QA对涵盖语音/声音/音乐/混合.多音频子集包括在内.

| Model | Overall | Speech | Sound | Music | Multi-audio |
|-------|---------|--------|-------|-------|-------------|
| Gemini 2.5 Pro | ~60% | 73.4% | 51.9% | 64.9% | ~22% |
| Gemini 2.5 Flash | ~57% | 73.4% | 50.5% | 64.9% | 21.2% |
| GPT-4o Audio | 52.5% | — | — | — | 26.5% |
| Qwen2.5-Omni-7B | 52.2% | 57.4% | 47.6% | 61.5% | ~20% |
| Audio Flamingo 3 | ~54% | — | — | — | — |
| Audio Flamingo Next | SOTA on LongAudioBench | — | — | — | — |

其他**multi-audio column is damning for everyone.**随机机会在4选项多选项=25%;大多数模型在此处得分.LALM仍然难以比较两个剪辑.

> **多音频列对所有人都是致命的。**4 选 1 多选题的随机概率 = 25%;大多数模型得分就在附近.

### 2026年LALM的使用

- **Compliance audit of call-center recordings.**"代理人提及了必要的披露吗?"
  **合规审计通话录音。**"客服是否提到了必要的免责声明?"
- **Accessibility.**描述听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力者听力障碍者听力障碍者听力者听力障碍者听力者听力障碍者听力者听力障碍者听力者听力障碍者听力障碍者听力障碍者听力者听力障碍者听力者听力障碍者听力障碍者听力障碍者听力者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力障碍者听力者听力障碍者听力障碍者听力障碍者听力障碍者听力者听力障碍者听力者听力障碍者听力者听力.
  **无障碍。**为听障用户描述声音事件(不只是转录)
- **Content moderation.**检测暴力语言+威胁性语调+背景背景.
  **内容审核。**检测暴力语言 + 威胁语气 + 背景上下文──
- **Podcast / meeting chaptering.**语义概述,而不是演讲者转转.
  **播客/会议章节化。**语义摘要,不仅仅说话人轮次.
- **Music catalog analysis.**"用B部分键变换找到所有轨道".
  **音乐目录分析。**"找出所有的B段有转调曲目.

### 它们 (尚未) 有用处

- 精细的音乐理论 (低于合唱水平).
  精细音乐理论(和弦级别以下) 』
- 长时间对话 (过去10分钟的程度) 时,讲者所归功的推理.
  长对话中的说话人归因推理 (超过10分钟退化)
- 无线电和无线电的比较 (22-26%几乎不超过随机).
  多音频比较 (22-26% 几乎等于随机)
- 实时流媒体推理 (大多数是离线批量推理).
  实际流式推理 (大部分都是离线批量推理)

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――




## 建立它,实现它.
```figure
v4-alm-tokens
```

## 建立它

### 步骤1:查询Qwen2.5-Omni

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

### 步骤2:投影仪模式

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

预测器通常是1-3个线性层.在ASR对 (音频 →转录) 上训练它是第一阶段的借口任务.

### 步骤3:MMAU/LongAudioBench的基准评估

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

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


单独报告每类别 (语音/声音/音乐/多音频). 总数隐藏在模型失败的地方.




> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

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



## 陷

> 常见陷

- **Over-trust on multi-audio.**如果你的任务需要"哪个剪辑有X", 随机运算水平的性能是真实的.
  **过度信任多音频。**如果你的任务需要"哪个片段有X",随机水平性能是真实的.
- **Long-audio degradation.**过去10分钟,大多数模型的扬声器属性断裂.
  **长音频退化。**超过10分钟,大多数模型的说话人归因失效――先做日志化 (第6课),再总结――
- **Hallucinations on silence.**像LALM一样,使用Whisper编码器的Whisper样式问题.
  **静音上的幻觉。**与使用Whisper编码器的 LALM 继承的Whisper 式问题相同.
- **Benchmark cherry-picking.**销售商博客文章突出了最佳类别.
  **基准挑挑拣拣。**供应商博客文章突出最佳类别──自运行MMAU-Pro 多音频子集──

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-alm-picker.md`选择LALM+基准子集+输出模式 (文字与语音) 为特定的音频理解任务.

> 保存为`outputs/skill-alm-picker.md`〔为给定的音频理解任务选择 LALM + 基准子集 + 输出模态(文本 vs 语音) 』

## 练习题

1. **Easy.**跑步`code/main.py`查看玩具投影器模式 + 输出代币的虚假 LALM 路由 (音频嵌入,文本代币) →
   **简单。**运行`code/main.py`查看玩具投影器模式 + 假 LALM 路由(音频嵌入,文本代币)→ 输出代币──
2. **Medium.**根据100个MMAU-Pro语音项目, 评分Qwen2.5Omni-7B.
   **中等。**在100个MMAU-Pro语音项评分中,Qwen2.5-Omni-7B──与论文报告的数字比较──
3. **Hard.**建立一个最小的音频标题基线:BEAT编码器+2层投影器+结的Llama-3.2-1B. 仅在AudioCaps上调整投影器.比较Clotho-AQA上的SALMONN.
   **困难。**构建最小音频标注基线:BEATs编码器 + 2层投影器 + 结 Llama-3.2-1B──仅在AudioCaps上微调投影器──在Clotho-AQA上与SALMONN比较──

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

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

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Chu et al. (2024). Qwen2-Audio](https://arxiv.org/abs/2407.10759)参考架构.
  等 (2024). 文2-音频参考架构──
- [Alibaba (2025). Qwen2.5-Omni](https://huggingface.co/Qwen/Qwen2.5-Omni-7B)说话中说话.
  阿里巴巴 (2025). Qwen2.5Omni语音入语音出。
- [NVIDIA (2025). Audio Flamingo 3](https://arxiv.org/abs/2507.08128)开放长音频领导者.
  音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频领先者: 音频开源: 音频领先者: 音频领先者: 音频开源: 音频领先者: 音频
- [NVIDIA (2026). Audio Flamingo Next](https://arxiv.org/abs/2604.10905)长音频.
  音频 弗拉明戈 下一个 长音频  索塔
- [Tang et al. (2023). SALMONN](https://arxiv.org/abs/2310.13289)双码码开创者
  唐等 (2023). SALMONN双编码器先驱.
- [MMAU-Pro leaderboard](https://mmaubenchmark.github.io/)2026年现场排名.
  马达-普罗 排行榜2026年实时排名

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

