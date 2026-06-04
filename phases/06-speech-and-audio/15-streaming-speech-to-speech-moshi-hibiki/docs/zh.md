# 流式语音到语音 — Moshi、Hibiki 与全双工对话

> 2024-2026 年重新定义了语音 AI。Moshi 用单一模型在 200ms 延迟内同时听和说。Hibiki 逐块进行语音到语音翻译。两者都放弃了 ASR->LLM->TTS 流水线，采用基于 Mimi 编解码器 token 的统一全双工架构。这是新的参考设计。

> **【中文解读】** 2024-2026 年重新定义了语音 AI。Moshi 用单一模型在 200ms 延迟内同时听和说。Hibiki 逐块进行语音到语音翻译。两者都放弃了 ASR→LLM→TTS 流水线，采用基于 Mimi 编解码器 token 的统一全双工架构。这是新的参考设计。

> **【拓展：全双工语音 AI】** 传统语音助手是"半双工"（听的时候不能说），Moshi 实现了"全双工"（同时听说），就像人类自然对话一样。这是 2026 年语音 AI 最前沿的方向。

**类型：** 学习
**语言：** Python
**前置条件：** 阶段 6 · 13（神经音频编解码器），阶段 6 · 11（实时音频），阶段 7 · 05（完整 Transformer）
**时长：** 约 75 分钟

## 问题引入

基于第 11 + 12 课构建的每个语音代理都有一个根本性的延迟下限约 300-500 ms：VAD 触发、STT 处理、LLM 推理、TTS 生成。每个阶段都有自己的最小延迟。你可以调优和并行化，但流水线形状限制了你的上限。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

Moshi（Kyutai，2024-2026）问了一个不同的问题：如果没有流水线呢？如果一个模型直接接收音频并输出音频，持续不断地，文本作为中间的"内心独白"而不是必需的阶段呢？

答案是**全双工语音到语音**。理论延迟 160 ms（80 ms Mimi 帧 + 80 ms 声学延迟）。单张 L4 GPU 上实际延迟 200 ms。这是最好的级联语音代理的一半。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

![Moshi 架构：两条并行 Mimi 流 + 内心独白文本](../assets/moshi-hibiki.svg)

### Moshi 架构

**输入。** 两条 Mimi 编解码器流，都是 12.5 Hz × 8 码本：

- 流 1：用户音频（Mimi 编码，持续到达）
- 流 2：Moshi 自己的音频（Moshi 生成）

**Transformer。** 一个 7B 参数的时间 Transformer 处理两条流和一个文本"内心独白"流。在每 80 ms 步中，它：

1. 消费最新的用户 Mimi token（8 个码本）。
2. 消费最近的 Moshi Mimi token（8 个码本，已生成）。
3. 生成下一个 Moshi 文本 token（内心独白）。
4. 生成下一个 Moshi Mimi token（8 个码本通过小型深度 Transformer）。

所有三个流——用户音频、Moshi 音频、Moshi 文本——并行运行。Moshi 可以在说话时听到用户；可以在用户打断时中断自己；可以发出回应声（"嗯嗯"）而不打断自己的主要话语。

**深度 Transformer。** 在一个帧内，8 个码本不是并行预测的——它们有码本间依赖。一个小型 2 层"深度 Transformer"在 80 ms 内顺序预测它们。这是 AR 编解码器 LM 的标准分解（VALL-E、VibeVoice 也使用）。

### 为什么内心独白文本有帮助

没有显式文本，模型必须在声学流中隐式建模语言。Moshi 的洞察：强制它伴随音频发射文本 token。文本流本质上是 Moschi 正在说的内容的转录。这提高了语义连贯性，使替换语言模型头更容易，并免费给你转录。

### Hibiki：流式语音到语音翻译

相同架构，在翻译对上训练。源音频输入，目标语言音频输出，持续不断。Hibiki-Zero（2026 年 2 月）消除了词级对齐训练数据的需要——使用句子级数据 + GRPO 强化学习做延迟优化。

初始支持四种语言对；可以用约 1000 小时适应新语言。

### 更广泛的 Kyutai 技术栈（2026）

- **Moshi** — 全双工对话（法语优先，英语良好支持）
- **Hibiki / Hibiki-Zero** — 同时语音翻译
- **Kyutai STT** — 流式 ASR（500 ms 或 2.5 s 前瞻）
- **Kyutai Pocket TTS** — 1 亿参数 TTS 在 CPU 上运行（2026 年 1 月）
- **Unmute** — 在公共服务器上组合这些的完整流水线

L40S GPU 上吞吐量：64 个并发会话，3 倍实时。

### Sesame CSM — 表亲

Sesame CSM（2025）使用类似想法——Llama-3 骨干配 Mimi 编解码器头。但 CSM 是单向的（接收上下文 + 文本，产生语音），而非全双工。它是市场上最好的"语音存在感" TTS；与 Moshi 的全双工能力不完全相同。

### 2026 性能数字

| 模型 | 延迟 | 用例 | 许可 |
|------|------|------|------|
| Moshi | 200 ms（L4） | 全双工英语/法语对话 | CC-BY 4.0 |
| Hibiki | 12.5 Hz 帧率 | 法语 <-> 英语流式翻译 | CC-BY 4.0 |
| Hibiki-Zero | 同上 | 5 个语言对，无需对齐数据 | CC-BY 4.0 |
| Sesame CSM-1B | 200 ms TTFA | 上下文条件 TTS | Apache-2.0 |
| GPT-4o Realtime | 约 300 ms | 闭源，OpenAI API | 商业 |
| Gemini 2.5 Live | 约 350 ms | 闭源，Google API | 商业 |

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：语音 AI 的产品化】** 语音技术在产品化中面临独特挑战：不同口音、背景噪声、远场拾音、多人说话等。Siri、Alexa、小爱同学等产品都投入了大量工程优化来解决这些 "长尾问题"。实时性要求（<300ms 延迟）也是语音产品的核心指标。

> **【拓展：多语言语音技术】** 全球语言的语音特性差异巨大：声调语言（如中文）的音高携带语义，低资源语言缺乏训练数据。Meta 的 MMS 模型支持 1000+ 种语言的语音识别，Whisper 在多语言场景表现出色，但仍需针对特定语言微调。

## 动手实现

### 步骤 1：接口

Moshi 暴露一个 WebSocket 服务器，接收 80 ms 的 Mimi 编码音频块并返回 80 ms 的 Mimi 编码音频块。双向。持续不断。

```python
import asyncio
import websockets
from moshi.client_utils import encode_audio_mimi, decode_audio_mimi

async def moshi_chat():
    async with websockets.connect("ws://localhost:8998/api/chat") as ws:
        mic_task = asyncio.create_task(stream_mic_to(ws))
        spk_task = asyncio.create_task(stream_from_to_speaker(ws))
        await asyncio.gather(mic_task, spk_task)
```

### 步骤 2：全双工循环

```python
async def stream_mic_to(ws):
    async for chunk_80ms in mic_stream_at_12_5_hz():
        mimi_tokens = encode_audio_mimi(chunk_80ms)
        await ws.send(serialize(mimi_tokens))

async def stream_from_to_speaker(ws):
    async for msg in ws:
        mimi_tokens, text_token = deserialize(msg)
        audio = decode_audio_mimi(mimi_tokens)
        await play(audio)
```

两个方向同时运行。Python asyncio 或 Rust futures 是标准传输。

### 步骤 3：训练目标（概念性）

对于每 80 ms 帧 `t`：

- 输入：`user_mimi[0..t]`、`moshi_mimi[0..t-1]`、`moshi_text[0..t-1]`
- 预测：`moshi_text[t]`，然后 `moshi_mimi[t, codebook_0..7]`

文本在音频之前预测（内心独白）；音频在深度 Transformer 内按码本顺序预测。

### 步骤 4：Moshi 哪里赢，哪里不赢

Moshi 赢的地方：

- 便宜硬件上亚 250 ms 端到端。
- 自然回应声和打断。
- 没有流水线粘合代码。

Moshi 不赢的地方：

- 工具调用（未为此训练；需要单独的 LLM 路径）。
- 长推理（Moshi 是约 8B 对话模型，不是 Claude/GPT-4）。
- 小众话题的事实准确性。
- 大多数企业生产用例（2026 年仍使用流水线）。

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

> **【拓展：语音与情感计算】** 语音不仅传递文字信息，还携带丰富的情感信号（语调、语速、音高变化）。情感语音识别（Speech Emotion Recognition, SER）在客服质检、心理健康监测、智能教育等领域有广泛应用。当前 SOTA 模型通常基于 wav2vec 2.0 或 HuBERT 等预训练模型微调。

## 用框架实现

| 场景 | 选择 |
|------|------|
| 最低延迟语音伴侣 | Moshi |
| 实时翻译通话 | Hibiki |
| 语音演示 / 研究 | Moshi、CSM |
| 带工具的企业代理 | 流水线（第 12 课），不是 Moshi |
| 自定义声音上下文 TTS | Sesame CSM |
| 语音到语音，任意语言 | GPT-4o Realtime 或 Gemini 2.5 Live（商业） |

## 陷阱

- **有限工具调用。** Moshi 是对话模型，不是代理框架。工具需结合流水线。
- **特定声音条件化。** Moshi 使用单一训练角色；克隆是单独的训练运行。
- **语言覆盖。** 法语 + 英语优秀；其他有限。Hibiki-Zero 有帮助，但仍然需要训练数据。
- **资源成本。** 完整 Moshi 会话占用一个 GPU 插槽；不是便宜的共享租户部署模式。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## 产出物

保存为 `outputs/skill-duplex-pipeline.md`。为语音代理工作负载选择流水线 vs 全双工架构，并给出理由。

## 练习题

1. **简单。** 运行 `code/main.py`。它以符号方式模拟双流 + 内心独白架构。
2. **中等。** 从 HuggingFace 拉取 Moshi，运行服务器，测试一次对话。测量从用户语音结束到 Moshi 回复开始的墙钟延迟。
3. **困难。** 取你的第 12 课流水线代理，在 20 个匹配测试话语上比较 P50 延迟 vs Moshi。写出流水线在架构上何时仍然胜出。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|----------|----------|
| 全双工 | 同时听说 | 同一模型上两条音频流同时活跃。 |
| 内心独白 | 模型的文本流 | Moshi 伴随音频输出发射文本 token。 |
| 深度 Transformer | 码本间预测器 | 在一个 80 ms 帧内预测 8 个码本的小型 Transformer。 |
| Mimi | Kyutai 的编解码器 | 12.5 Hz × 8 码本；语义+声学；驱动 Moshi。 |
| 流式 S2S | 音频 -> 音频实时 | 逐块翻译/对话，没有流水线阶段。 |
| 回应声 | "嗯嗯"反应 | Moshi 可以发出小确认而不打断自己的轮次。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## 延伸阅读

- [Defossez et al. (2024). Moshi — speech-text foundation model](https://arxiv.org/html/2410.00037v2) —— 论文。
- [Kyutai Labs (2026). Hibiki-Zero](https://arxiv.org/abs/2602.12345) —— 无对齐数据的流式翻译。
- [Sesame (2025). Crossing the uncanny valley of voice](https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice) —— CSM 规格。
- [Kyutai — Moshi 仓库](https://github.com/kyutai-labs/moshi) —— 安装 + 服务器。
- [OpenAI — Realtime API](https://platform.openai.com/docs/guides/realtime) —— 闭源商业同行。
- [Kyutai — Delayed Streams Modeling](https://github.com/kyutai-labs/delayed-streams-modeling) —— 底层 STT/TTS 框架。

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源，包括论文、教程和工具。建议按需选读，优先阅读标注为 "the critical read" 的核心论文。
