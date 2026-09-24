# 流式语音到语音 流式语音到语音 流式语音与全双工对话

> 2024-2026年重新定义了语音AI.莫希发出一个单个模型,可以在200ms延迟同时听和说话.希比基会逐步进行语音翻译.这两个都放弃了ASR → LLM → TTS管道,以实现Mimi代码代码代码的统一全双结构.这是新的参考设计.

> **【中文解读】**2024-2026年重新定义语音AI──Moshi使用单一模型在200ms 延迟内同时听和说──Hibiki 逐块进行语音到语音翻译──两者都放弃了ASR→LLM→TTS流水线,采用基于Mimi编解码器的统一双工构──这是新的参考设计──

> **【拓展：全双工语音 AI】**传统语音助手是"半双工" (听时不能说),莫西实现了"全双工" (全双工) (同时听说),就像人类自然对话一样.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 13 (Neural Audio Codecs), Phase 6 · 11 (Real-Time Audio), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 13（神经音频编解码器），阶段 6 · 11（实时音频），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## 问题 问题引入

每个从课11+12构建的语音代理都具有基本的延迟地板约300-500ms:VAD火灾,STT过程,LLM原因,TTS生成.每个阶段都有自己的最低延迟.你可以调和并行,但管道形状限制你.

> 基于第11和12课程的每个语音助手都有约300-500 ms的基础延迟下限:VAD 触发、STT 处理、LLM 推理、TTS 生成──每个阶段都有自己的最小延迟──你可以调整和并行化,但流水线架构本身限制你──

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――


莫希 (九台,2024-2026) 提出了一个不同的问题:如果没有管道呢?如果一个模型接收了音频并直接,连续地发出音频,文字作为中间的"内在单独话语"而不是所需的阶段呢?

> 莫希·九台,2024-2026)提出了一个不同的问题:如果没有流水线?如果一个模型直接持续接收音频输入和输出音频,文本只是中间的"内心独白"而不是必要阶段?

答案是**full-duplex speech-to-speech**理论上的延迟160ms (80ms米米框架 +80ms声响延迟). 实际的延迟200ms在单个L4GPU上. 这就是最好的管道语音代理能实现的一半.

> 答案是**全双工语音到语音**△理论延迟160 ms(80 ms Mimi  + 80 ms 声学延迟) ・ 在单张L4 GPU 上实际延迟200 ms──这是最好的流水线语音助手延迟的一半──

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Moshi architecture: two parallel Mimi streams + inner-monologue text](../assets/moshi-hibiki.svg)

### 莫希建筑

> 莫希架构

**Inputs.**两条米米编码流,都在12.5Hz × 8编码书:

> **输入。**两个米米编解码器流,平均为12.5Hz × 8个码本:

- 流 1:用户音频 (Mimi编码,不断到达)
  中文翻译:流 1:用户音频(米米编码,持续到达)
- 流2:莫希的声音 (由莫希制作)
  中文翻译:流 2:Moshi 自身的音频(由Moshi 生成)

**The transformer.**时间变压器处理了两个流和一个文本"内部单独"流.每80ms步骤,它:

> **Transformer。**一个70亿参数的时间流变压器同时处理两个流和一个文本"内心独白"流.

1. 消耗最新用户的Mimi代币 (8本代码书).
   中文翻译:消费最新的用户米米代币 (Mimi token)
2. 消耗了最新的Moshi Mimi代币 (8本编码书,如产品).
   中文翻译:消费最近生成的莫希米米代币 (Moshi Mimi token)
3. 生成下一个Moshi文本代码 (内部单词).
   中文翻译:生成下一个莫西文本代号
4. 通过小的深度变压器生成下一个Moshi Mimi代币 (8本代码书).
   中文翻译:生成下一组莫希米米令牌 (由小型深度变压器) 通过8个码本.

所有三条流程都运行并行.莫希可以听到用户在说话时;可以打断自己当用户打断;可以反频道 ("mhm") 没有打破其主语句.

> 三流用户音频、Moshi 音频、Moshi 文本并行运行──Moshi可以在谈话中同时听到用户;可以在用户打断时断断断自己;可以在不破坏主要发言的情况下进行反("")。

**The depth transformer.**在一个框架内,8个代码书不会平行预测.它们具有代码书之间的依赖性.一个小型的2层"深度变压器"在80ms内测序预测它们.这是AR代码 LM的标准因子化 (VALL-E,VibeVoice也使用).

> **深度 Transformer。**在一个内,8个码本不是并行预测的中存在的码本间依赖.一个2层的小型"深度变压器"在80ms内顺序预测它们.这是自归编码器语言模型的标准因子化方式.

### 为什么内面单词文本有帮助

没有明确的文本,模型必须隐含地模拟语言在声流中.莫希的见解:强迫它与音频一起发射文本代码.文本流基本上是莫希所说的转录.这改善了语义一致性,使更容易更换语言模型头,并免费提供转录.

> 为什么内心独白文本有帮助:没有明显文本,模型必须在声学流中隐藏建模语言――莫希的洞察:强制它同时输出文本标记和音频――文本流本质上是莫希所说的内容的转录――这提高了语义连贯性,使语言模型头部更容易更换,并且免费提供转录文本――

### 语文:流媒体语文翻译

基比基-零 (Feb 2026) 消除了文字级对齐训练数据的需要. 使用语句级数据 + GRPO强化学习来优化延迟.

> 希比基:流式语音到语音翻译――同样的架构,使用翻译对训练――源语言音频输入,目标语言音频输出,持续进行――希比基-零 (Hibiki-Zero) 消除对词级对齐训练数据的需求使用句子级数据 + GRPO 强化学习进行延迟优化――

首先支持四种语言对;可在1000小时内适应新语言.

> 首先支持四种语言对;可以使用约1000小时的数据适应新语言.

### 更多的九泰堆 (2026)

> 更广泛的九台技术(2026年)

- **Moshi** 双重对话 (首先是法语,英语支持良好)
  中文翻译:Moshi  全双工对话(法语优先,英语支持良好)
- **Hibiki / Hibiki-Zero**同时演讲翻译
  中文翻译:Hibiki / Hibiki-Zero  同步语音翻译
- **Kyutai STT**流动ASR (500 ms或2.5秒前景)
  中文翻译:九台STT  流式语音识别(500 ms或2.5s 前视)
- **Kyutai Pocket TTS** 100M-param TTS运行在CPU上 (2026年1月)
  中文翻译:九台口袋TTS  1 亿参数TTS,可在CPU上运行(2026年1月)
- **Unmute**将这些数据在公共服务器上结合
  中文翻译:Unmute  在公共服务器上组合这些组件的完整流水线

在L40SGPU上吞吐量: 64次同时会议,实时3x.

> 在L40S GPU上的吞吐量:64 个并发会话,3 倍实时速度.

### 芝麻CSM 表哥

芝麻CSM (2025) 使用类似的想法. 一个Llama-3背骨和米米编程头. 但CSM是单向的 (采取文本 + 语文,产生语音) 而不是全双重. 它是市场上最好的"语音存在"TTS; 不和莫希的全双重能力完全相同.

> 芝麻CSM (Sesame CSM) 使用类似的想法Llama-3 骨干网络 + Mimi 编解码器头.但CSM是单向的,而不是全双工.它是市场上最好的"语音存在感"TS;但与莫希的全双工能力不完全相同.

### 2026 年的绩效数字

| Model | Latency | Use case | License |
|-------|---------|----------|---------|
| Moshi | 200 ms (L4) | full-duplex English / French dialogue / 全双工英/法对话 | CC-BY 4.0 |
| Hibiki | 12.5 Hz framerate | French ↔ English streaming translation / 法↔英流式翻译 | CC-BY 4.0 |
| Hibiki-Zero | same | 5 language-pairs, no aligned data / 5 语言对，无需对齐数据 | CC-BY 4.0 |
| Sesame CSM-1B | 200 ms TTFA | context-conditioned TTS / 上下文条件 TTS | Apache-2.0 |
| GPT-4o Realtime | ~300 ms | closed, OpenAI API / 闭源，OpenAI API | commercial |
| Gemini 2.5 Live | ~350 ms | closed, Google API / 闭源，Google API | commercial |

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――




## 建立它,实现它.
```figure
sp-fullduplex
```

## 建立它

### 步骤1:接口

> 步骤1:接口

莫希暴露了一个WebSocket服务器,它接收了80毫米的Mimi编码音频,

> 莫希 暴露一个WebSocket 服务器,接收80 ms的 Mimi 编码音频块并返回80 ms的 Mimi 编码音频块──双向,持续进行──

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

### 步骤2:全双循环

> 步骤2:全双工循环

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

两条方向同时运行.  Python 异步或 Rust 期货是标准的运输.

> 两方向同时运行. 字thon 无机或化期货是标准的传输方式.

### 步骤3:培训目标 (概念)

> 步骤3: 训练目标 (概念性)

每80ms的时间`t`其他:

> 对于每80ms 的`t`其他:

- 输入:`user_mimi[0..t]`现在`moshi_mimi[0..t-1]`现在`moshi_text[0..t-1]`
  中文翻译:输入:`user_mimi[0..t]`,我知道.`moshi_mimi[0..t-1]`,我知道.`moshi_text[0..t-1]`
- 预测:`moshi_text[t]`现在`moshi_mimi[t, codebook_0..7]`
  中文翻译:预测:`moshi_text[t]`然后是`moshi_mimi[t, codebook_0..7]`

文字预测在音频之前 (内部单词);音频预测在深度变压器内是代码书序列.

> 文本在音频之前预测;;音频在深度变压器内按码本顺序预测。

### 步骤4:莫希在哪里赢,在哪里不赢

> 步骤4:莫希的优势和缺点

莫希赢了:

> 莫希的优势:

- 在廉价硬件上,Sub-250ms端到端.
  中文翻译:在廉价硬件上端到端低于250ms.
- 自然的后通道和中断.
  中文翻译:自然的反和打断能力──
- 没有管道合码.
  中文翻译:无需流水线水代码──

莫希没有赢得:

> 莫希的不足:

- 工具调用 (没有接受培训;你需要单独的LLM途径).
  中文翻译:工具调用 (未针对此训练;需要单独的LLM路径)
- 长时间推理 (莫希是一个8B式对话模型,而不是克劳德/GPT-4).
  中文翻译:长链推理(莫西是约8000亿参数的对话模型,不是克劳德/GPT-4)。
- 关于基层主题的事实准确性.
  中文翻译:小众话题的事实准确性──
- 大多数生产企业使用案例 (2026年仍使用管道).
  中文翻译:大多数生产级企业场景(2026年仍在流水线使用) 』

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.





> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

| Situation | Pick |
|-----------|------|
| Lowest-latency voice companion / 最低延迟语音伴侣 | Moshi |
| Live translation call / 实时翻译通话 | Hibiki |
| Voice demo / research / 语音演示/研究 | Moshi, CSM |
| Enterprise agent with tools / 企业级带工具的 agent | Pipeline（第 12 课），不是 Moshi |
| Custom-voice TTS in context / 上下文中的自定义音色 TTS | Sesame CSM |
| Speech-to-speech, any languages / 任意语言的语音到语音 | GPT-4o Realtime 或 Gemini 2.5 Live（商业） |



## 陷

> 常见陷

- **Limited tool calling.**莫希是一个对话模式,而不是代理框架.
  翻译: 中文**有限的工具调用。**莫希是对话模型,不是代理框架.
- **Specific-voice conditioning.**莫希使用一个训练有素的人物;克隆是一个独立的训练.
  翻译: 中文**特定语音调节。**莫希使用单一训练人格;克隆需要单独的训练过程.
- **Language coverage.**汉语+英语是优秀的,其他语言有限.
  翻译: 中文**语言覆盖。**法语 + 英语表现优秀;其他语言有限──Hibiki-Zero 有帮助,但仍需要训练数据──
- **Resource cost.**一个完整的Moshi会话里,有一个GPU插槽,而不是一个便宜的共享租户部署模式.
  翻译: 中文**资源成本。**一个完整的Moshi会话用一个GPU插槽;不是廉价的共享租户部署模式.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-duplex-pipeline.md`选择管道与全双结构来进行语音代理工作,有理由.

> 保存为`outputs/skill-duplex-pipeline.md`◎为一个语音助手工作负载选择流水线还是全双工架构,并说明理由──

## 练习题

1. **Easy.**跑步`code/main.py`它象征性地模拟了两流+内格架构.
   翻译: 中文**简单。**运行`code/main.py`△它以符号方式模拟双流 + 内心独白架构.
2. **Medium.**拉出Moshi从HuggingFace,运行服务器,测试一场对话. 从用户结束的语音到Moshi响应的时间.
   翻译: 中文**中等。**从 HuggingFace 拉取 Moshi,运行服务器,测试一段对话――测量从用户语音结束到 Moshi 回复开始的实际延迟――
3. **Hard.**根据20个匹配的测试演示,比较P50延迟与Moshi.
   翻译: 中文**困难。**用第12课流水线助理和莫希在20条匹配测试语句上比较P50延迟.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Full-duplex | Hear-and-speak at once | Two audio streams active simultaneously on the same model. / 同一模型同时维护两条音频流 |
| Inner monologue | Model's text stream | Moshi emits text tokens alongside its audio output. / Moshi 在音频输出同时输出文本 token |
| Depth transformer | Inter-codebook predictor | Small transformer that predicts 8 codebooks within one 80 ms frame. / 在一个 80 ms 帧内预测 8 个码本的小型 Transformer |
| Mimi | Kyutai's codec | 12.5 Hz × 8 codebooks; semantic+acoustic; powers Moshi. / 12.5 Hz × 8 码本；语义+声学；驱动 Moshi |
| Streaming S2S | Audio → audio live | Chunk-by-chunk translation/dialogue, no pipeline stages. / 逐块翻译/对话，无流水线阶段 |
| Back-channeling | "Mhm" reactions | Moshi can emit small acknowledgments without breaking its turn. / Moshi 可发出小反馈而不打断自己的轮次 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Défossez et al. (2024). Moshi — speech-text foundation model](https://arxiv.org/html/2410.00037v2)报纸.
  莫西语音文本基础模型原始论文──
- [Kyutai Labs (2026). Hibiki-Zero](https://arxiv.org/abs/2602.12345)无线数据的流媒体翻译.
  基泰实验室 (Kyutai Labs) 没有必要对齐数据的流式翻译.
- [Sesame (2025). Crossing the uncanny valley of voice](https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice) CSM规格
  跨越语音的恐怖谷CSM规范──
- [Kyutai — Moshi repo](https://github.com/kyutai-labs/moshi)安装+服务器.
  库泰莫西 仓库安装 + 服务器。
- [OpenAI — Realtime API](https://platform.openai.com/docs/guides/realtime)关闭商业同行
  开放式实时API 关闭源商业对应方
- [Kyutai — Delayed Streams Modeling](https://github.com/kyutai-labs/delayed-streams-modeling)罩子下面的STT/TTS框架.
  延迟流量建模 底层STT/TTS框架

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

