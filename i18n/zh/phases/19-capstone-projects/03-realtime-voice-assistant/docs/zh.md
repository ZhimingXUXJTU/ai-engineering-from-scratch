# 卡普斯通 03 实时语音助理 (ASR到LLM到TTS)

> 听到声音的代理人可以使用800ms以下的端到端延迟,知道你何时停止说话,处理入, 雷特尔,瓦皮,莱维基特代理和皮皮卡特都在2026年进入这个酒吧. 它们用相同的形式进行: 流媒体ASR,转变检测器,流媒体LLM, 建立一个,测量WER和MOS和错误切断率,然后运行在输入输入下.

> **【中文解读】**本节是综合项目构建实时语音助手,整合语音识别、LLM 推理和语音合成──


**Type:** Capstone | **类型:** 综合项目
**Languages:** Python (agent + pipeline), TypeScript (web client) | **语言:** Python（Agent + 管道）, TypeScript（Web 客户端）
**Prerequisites:** Phase 6 (speech and audio), Phase 7 (transformers), Phase 11 (LLM engineering), Phase 13 (tools), Phase 14 (agents), Phase 17 (infrastructure)

>  **【前置】**顶点项目 03 = 综合阶段 6/7/11/13/14/17──实时语音助手(ASR→LLM→TTS)。
>  **【类比】**实时语音助手 = "开源版 GPT-4o"──2026 商业参考:Retell/Vapi/LiveKit/Pipecat──难点:端到端延迟 <800ms、知道用户何时说完、断)、工具调用不卡──架构:流式ASR+转换探测器+流式LLM+流式TTS+WebRTC──参考阶段12·20思想家讲者指标──标志:WER/MOS/误切断率──**前置知识:**阶段第6期语音与音频),阶段第7期变压器,阶段第11期LLM工程,阶段第13期工具,阶段第14期代理,阶段第17期基础设施)
**Phases exercised:**现在,我们在这个世界里,**涉及阶段:**子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子
**Time:** 30 hours | **时间:** 30 小时

## 问题 问题引入

> **【中文解读】**本节描述实时语音助手面临的技术挑战.2025-2026年语音成为AI UX 发展最快的品类,关键标志是端到端延迟 < 800ms.难点不仅在延迟,还在于交互体验:不能打断用户,不能被用户打断时出错,断断恢复,工具调用不阻音频,在移动网络动下生存.

> **【拓展：语音 AI 产品生态】**2026年主要语音代理 平台包括Retell AI、Vapi.ai、LiveKit代理 1.0、Pipecat 0.0.70。OpenAI实时API 和 Gemini 2.5 Live 提供集成式语音模型。ASR领域Deepgram Nova-3 以亚 300ms 首片延迟领先,开源方案更快的低语可自托管。TTS 方面卡特西亚 Sonic-2 首字节延迟最低(~200ms),ElevenLabs Flash v3 质量最优优──单台 g5.xlarge GPU 服务器可支 50 路并发通话──

语音是2025-2026年最快发展的AI UX类别. 技术上限每季度都下降. 开放AI实时API,双子 2.5 现场,卡特西亚索尼克-2,ElevenLabs Flash v3,LiveKit Agents 1.0和皮皮卡特 0.0.70都能实现800ms下载. 酒吧不是一个人的延迟. 互动感觉:不切断用户,不切断,从句子中断中恢复,在谈话中调用工具,

> 语音是2025-2026年发展最快的AI UX 品类――技术天花板每季都在下降――OpenAI实时API、Gemini 2.5 Live、Cartesia Sonic-2、ElevenLabs Flash v3、LiveKit Agents 1.0 和 Pipecat 0.0.70 都使亚亚 800ms 首音频输出成为可能――标准不仅是延迟,还有交互体验:不断用户、不断从句子中断中恢复、在对话中调用工具而不阻碍音频、在动移动网络中生存――

构建它,故障模式就会显现:为背景电视打响电话的音频调节的VAD,一个等待永远不会出现的分分区的轮检测器,一个TTS在发射之前缓冲400ms. 最重要的是在负载下一次修复这些并发布延迟和质量报告.

> 你无法通过拼接三个 REST调调用于实现. 架构是端到端的管道式流式传输. 构建后,失败模式变得可见:为电话音频调优的VAD在背景电视触发,等待永远来的标点符号的轮检测器,在输出前缓冲400ms的TTS. 本结业项目在负载下逐步修复这些问题并发布延迟和质量报告.

## 概念的核心概念

> **【中文解读】**语音助手管道包含五个流式阶段:音频输入(WebRTC) 、ASR(Deepgram Nova-3 流式转写)、轮次检测(VAD + 转完判断模型)、LLM(流式代币 输出)、TTS(首代币 后200ms 内流式音频输出)。三个横切关注点:Barge-in(用户打断时取消TTS、工具调用侧通道执行不阻塞音频)、反压力丢失包值时提高VAD 包)。

> **【拓展：VAD 与轮次检测】**Silero VAD v5 是2026年语音活动检测的默认选择,以20ms 粒度判断语音/静音――但单纯 VAD 无法判断用户是否说完整LiveKit的轮检测器是小型变压器,读部分转写文本判断语义完整性――实测显示,500ms 静音 + 完整性评分 > 0.6 的组合策略可控制误切率在 3% 以下――WER 词语错误率) 目标 <8%,15dB SNR),MOS语音质量评分) 目标 > 4.2――

管道有五个流程:**audio in**(WebRTC来自浏览器或PSTN),**ASR**(从 Deepgram Nova-3 或更快的语中流动部分转录),**turn detection**(VAD加上一个小的转变检测器模型,**LLM**(随着轮回完成, 流通令牌),**TTS**(在第一次LLM代币后,在200ms内播放音频).

> 管道有五个流式阶段:**音频输入**(来自浏览器或PSTN的WebRTC)**ASR**(来自深度图片Nova-3或更快的语的流式部分转录)**轮次检测**(VAD加上读取部分转写以获得完成提示的小型轮次检测模型)**LLM**(一旦轮次被判定为完成即流式输出代币)**TTS**(在第一个LLM代币后约200ms内流式输出音频)

两者之间存在三种问题.**Barge-in**随着使用者在代理人在说话时,TTS会取消,ASR会立即接听. **Tool use**: 交谈函数中调 (天气,日历) 必须在侧通道上运行,而不阻碍音频;如果延迟超过300ms,代理预先填充确认令牌 ("一秒..."). **Backpressure**:在数据包丢失下,部分转录被保留,VAD提高了语音门门门值,代理人避免在未被承认的消息上说话.

> 其他问题**Barge-in**当用户在代理说话时开始说话时,TTS 取消并立即恢复ASR──**工具使用**交谈中的函数调用 (天气日历) 必须在侧通道上运行而不阻碍音频;如果延迟超过300ms,代理预填写确认标志 (("稍等...") ").**反压**由于不确定性, 代理避免在未确认消息中说话.

测量是量化.Hamming VAD基准15 dB SNR上的WER低于8%.测量调用100次的第一次音频输出 p50低于800ms.测量调用率低于3%.TTS上的MOS高于4.2.50次.单个g5.xlarge上的50次同步调用.这些数字是可交付的.

> 测量标准是量化的. 在汉密尔VAD基准测试中,15 dBSNR 时 WER 低于8%──100次测量通话中首音频输出 p50 低于800ms──误切率低于3%──TTS MOS 高于4.2──单台 g5.xlarge 上50路并发通话──这些数字就是交付物物──

## 建筑,建筑

```
browser / Twilio PSTN
        |
        v
   WebRTC / SIP edge
        |
        v
  LiveKit Agents 1.0  (or Pipecat 0.0.70)
        |
   +----+--------------+--------------+-----------------+
   |                   |              |                 |
   v                   v              v                 v
  ASR              VAD v5         turn-detector     side-channel
(Deepgram         (Silero)          (LiveKit)        tools
 Nova-3 /         speech-gate    completion score    (weather,
 Whisper-v3)      per 20ms        on partials        calendar)
   |                   |              |
   +--------+----------+--------------+
            v
        LLM (streaming)
     GPT-4o-realtime / Gemini 2.5 Flash /
     cascaded Claude Haiku 4.5
            |
            v
        TTS streaming
     Cartesia Sonic-2 / ElevenLabs Flash v3
            |
            v
     audio back to caller
            |
            v
   OpenTelemetry voice traces -> Langfuse
```

##  技术

- 运输:LiveKit Agents 1.0 (WebRTC) 加上Twilio PSTN门户;作为替代框架,Pipecat 0.0.70
  中文翻译:运输:LiveKit Agents 1.0 (WebRTC) 加上Twilio PSTN网关;作为替代框架的皮皮卡特0.70

> 中文翻译:运输:LiveKit Agents 1.0 (WebRTC) 加上Twilio PSTN网关;Pipecat 0.0.70作为替代框架(翻译)

- 亚斯拉:深度格式诺瓦-3 (流动,第一个部分次300ms以下) 或更快的语Whisper-v3-turbo自主托管
  中文翻译:ASR:Deepgram Nova-3 (流媒体,300ms以下的部分) 或更快的语Whisper-v3-turbo自主托管

> 中文翻译:ASR:Deepgram Nova-3 (流媒体,300ms以下的部分) 或更快的语Whisper-v3-turbo自主托管

- 维亚:Silero VAD v5加上LiveKit转换探测器 (读取部分转录的小型变压器)
  中文翻译:VAD:Silero VAD v5加上LiveKit转换探测器 (读取部分转录的小型变压器)

> 中文翻译:VAD:Silero VAD v5加上LiveKit转换探测器 (读取部分转录的小型变压器)

- 专业:OpenAI GPT-4o实时集成,双子 2.5 闪存直播,或化Claude Haiku 4.5 (流媒体完成,独立音频路径)
  中文翻译:LLM:OpenAI GPT-4o实时集成,双子 2.5 Flash Live,或缩的Claude Haiku 4.5 (流媒体完成,独立音频路径)
- 卡特西亚索尼克-2 (最低的第一字节),ElevenLabs Flash v3,或自主主主机的开源Orpheus
  中文翻译:TTS:卡特西亚索尼克-2 (最低的第一字节),ElevenLabs Flash v3,或自主主机的开源奥尔菲斯

> 中文翻译:TTS:卡特西亚索尼克-2 (最低的第一字节),ElevenLabs Flash v3,或自主主播的开源奥尔菲斯 (翻译)

- 工具:FastMCP侧通道用于天气/日历/预订;如果工具需要300ms以上的时间,代理预发填充器
  中文翻译:工具:FastMCP 侧通道用于天气/日历/预订;如果工具需要300ms以上,代理预发填充器
- 可观察性:OpenTelemetry语音跨度,Langfuse语音跟音频重播
  中文翻译:可观察性:OpenTelemetry语音跨度,Langfuse语音跟音频重播
- 部署:单个g5.xlarge (24GBVRAM) 用于自主托管的Whisper + Orpheus;托管的API以最低延迟
  中文翻译:部署:单个g5.xlarge (24GBVRAM) 用于自主托管的Whisper + Orpheus;托管的API以最低延迟

> 中文翻译:部署:单个g5.xlarge (24GBVRAM) 用于自主托管的Whisper + Orpheus;托管的API以最低延迟(翻译)


## 动手构建

> **【中文解读】**构建分为9个阶段:WebRTC 会话建立、ASR 流式处理(20ms PCM ) 、VAD 与轮次检测(500ms 静音 + 完整性 > 0.6)、LLM 流式输出、TTS 流式输出(首个部分 200ms 内)、Barge-in 处理(取消TTS + 丢弃LLM 输出 + 重新启动ASR) 工具侧通道道(>300ms 时发送充填语)、评估套件(100 路通话测试 WER/误切/延迟/MOS)、负载测试(单台 50 路并发)

> **【拓展：SWE-bench 评估体系】**据悉,SWE-bench是目前编码的代理 最权威的评测基准,包含真实GitHub问题和对应补丁.
```figure
ce-voice-latency
```

## 建立它

1. **WebRTC session.**在服务器上,连接一个代理工作者,加入房间.
   中文翻译:1. **WebRTC session.**在服务器上,连接一个代理工作者,加入房间.

2. **ASR streaming.**输送20ms的PCM框架到Deepgram Nova-3 (或 GPU上更快的语).订阅部分和最终的转录.每部分延迟记录.
   翻译: 翻译:**ASR streaming.**输送20ms的PCM框架到Deepgram Nova-3 (或 GPU上更快的语).订阅部分和最终的转录.每部分延迟记录.

3. **VAD and turn detector.**在语音结束时,将LiveKit转换探测器启动与最新部分转录.只有当VAD说沉默500ms时,只会承诺"完成",转换探测器得分完成>0.6.
   翻译: 翻译:**VAD and turn detector.**在语音结束时,将LiveKit转换探测器启动与最新部分转录.只有当VAD说沉默500ms时,只会承诺"完成",转换探测器得分完成>0.6.

4. **LLM stream.**在完成时,开始与正在进行的对话加上最终的转录. 流出代币. 在第一个代币,交给TTS.
   翻译: 翻译:**LLM stream.**在完成时,开始与正在进行的对话加上最终的转录. 流出代币. 在第一个代币,交给TTS.

5. **TTS stream.**卡特西亚 Sonic-2 将音频块回放.第一块必须在第一个LLM代币200ms内离开服务器. 发送块到LiveKit室;客户端通过WebRTC节缓冲器播放.
   翻译: 五.**TTS stream.**卡特西亚 Sonic-2 将音频块回放.第一块必须在第一个LLM代币200ms内离开服务器. 发送块到LiveKit室;客户端通过WebRTC节缓冲器播放.

6. **Barge-in.**当VAD在播放TTS时检测到新用户语音时,立即取消TTS流,放弃剩余的LLM输出,重新装备ASR.`tts_canceled`度.
   翻译: 七个字**Barge-in.**当VAD在播放TTS时检测到新用户语音时,立即取消TTS流,放弃剩余的LLM输出,重新装备ASR.`tts_canceled`度.

7. **Tool side channel.**记录天气和日历作为调用函数工具.当调用时,同时打开调用;如果它在300ms内没有解决,请LLM发出"一秒钟,让我检查"作为填充器;一旦工具返回,再恢复.
   翻译:7.**Tool side channel.**记录天气和日历作为调用函数工具.当调用时,同时打开调用;如果它在300ms内没有解决,请LLM发出"一秒钟,让我检查"作为填充器;一旦工具返回,再恢复.

8. **Eval harness.**记录100次电话.计算WER (对待延期转录),错误截止率 (用户在句子中中时取消TTS),首次音频输出p50,TTS MOS (人或NISQA),以及丧测试 (减少3%的包).
   翻译:8.**Eval harness.**记录100次电话.计算WER (对待延期转录),错误截止率 (用户在句子中中时取消TTS),首次音频输出p50,TTS MOS (人或NISQA),以及丧测试 (减少3%的包).

9. **Load test.**通过一个g5.xlarge和合成调用器进行50次同时调用.
   翻译:9.**Load test.**通过一个g5.xlarge和合成调用器进行50次同时调用.

## 用它使用方法

```
caller: "what is the weather in tokyo tomorrow"
[asr  ] partial @280ms: "what is the"
[asr  ] partial @540ms: "what is the weather"
[turn ] completion score 0.82 at @820ms; commit
[llm  ] first token @960ms
[tool ] weather.tokyo tomorrow -> 68/52 partly cloudy @1140ms
[tts  ] first audio-out @1040ms: "Tokyo tomorrow will be partly cloudy..."
turn latency: 1040ms user-stop -> audio-out
```

## 发射上线

`outputs/skill-voice-agent.md`由于一个域名 (客户支持,安排或亭子),它会出现一个LiveKit代理,ASR/VAD/LLM/TTS管道调整到测量.

> `outputs/skill-voice-agent.md`根据测量标准调优的带ASR/VAD/LLM/TTS管道的LiveKit代理.

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | End-to-end latency | p50 first-audio-out under 800ms across 100 recorded calls |
| 25 | 端到端延迟 | 100 路记录通话中 p50 首音频输出低于 800ms |
| 20 | Turn-taking quality | False-cutoff rate under 3% on the Hamming VAD benchmark |
| 20 | 轮次交互质量 | Hamming VAD 基准测试上误切断率低于 3% |
| 20 | Tool-use correctness | Mid-conversation tool calls that return the right data without stalling audio |
| 20 | 工具使用正确性 | 对话中返回正确数据而不阻塞音频的工具调用 |
| 20 | Reliability under packet loss | WER and turn-taking stability with 3% packet drop injected |
| 20 | 丢包下的可靠性 | 注入 3% 丢包时的 WER 和轮次交互稳定性 |
| 15 | Eval harness completeness | Reproducible measurements with public config |
| 15 | 评估框架完整性 | 公开配置的可复现测量 |
| **100** | | |

## 练习题

1. 换 Deepgram Nova-3 换g5.xlarge 上的更快的语 v3 轮机. 测量延迟和 WER 差距. 确定CPUvsGPU决策在哪里重要.
   中文翻译:将将Deepgram Nova-3 换为g5.xlarge 上的更快的语 v3turbo──测量延迟和WER 差距──确定CPUvsGPU 决策在何处重要──

> 中文翻译:将将Deepgram Nova-3 换为g5.xlarge 上的更快的语 v3turbo──测量延迟和WER 差距──确定CPUvsGPU 决策在何处重要──(翻译)


2. 加入一个中断-仲裁政策:当用户在工具调用中入时,代理会做什么?比较三个政策 (硬取消,完成工具,然后停止,排队下一轮).
   中文翻译:添加中断仲裁策略:当用户在工具调用期间打断时代理怎么做?

> 中文翻译:添加中断仲裁策略:当用户在工具调用期间打断时代理怎么做?


3. 执行反向转换检测器测试:在句子中给用户长时间停顿. 调整VAD沉默门和转换检测器得分门以实现最低的假切断,而不需要超过900ms.
   中文翻译:运行对抗性轮检测器测试:给用户句子中间的长停顿――调优 VAD 静音值和轮检测器分数值以获得最低误切率,同时不超过900ms――

4. 通过Twilio在PSTN上部署相同的代理.将PSTN首次音频输出与WebRTC进行比较.解释器缓冲器和编码区别.
   中文翻译:通过Twilio在PSTN上部署同一个代理.

> 中文翻译:通过 Twilio 在 PSTN 上部署同一个代理──比较 PSTN 首音频输出与 WebRTC──解释位缓冲 和编解码器差异──(翻译)


5. 添加非英语语言 (日本语,西班牙语) 的语音活动检测. 测量Silero VAD v5错误触发率与语言特定的细节调节.
   中文翻译:为非英语语言 ((日语、西班牙语) 添加语音活动检测――测量Silero VAD v5 误触发率与语言特定微调的对比――

> 中文翻译:为非英语语言(日语、西班牙语) 添加语音活动检测――测量Silero VAD v5 误触发率与语言特定微调的对比――(翻译)


## 关键词 快速查找表

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| Turn detection | "End of utterance" | Classifier that, given VAD silence and a partial transcript, decides the user is done speaking |
| 轮次检测 | "话语结束" | 给定 VAD 静音和部分转写，判断用户说完话的分类器 |
| Barge-in | "Interruption handling" | Canceling TTS mid-playback when VAD detects new user speech |
| 打断处理 | "中断处理" | VAD 检测到新用户语音时取消正在播放的 TTS |
| First-audio-out | "Latency" | Time from user stops speaking to the first audio packet leaving the server |
| 首音频输出 | "延迟" | 从用户停止说话到第一个音频包离开服务器的时间 |
| VAD | "Speech gate" | Model classifying audio frames as speech vs silence; Silero VAD v5 is the 2026 default |
| VAD | "语音门" | 将音频帧分类为语音或静音的模型；Silero VAD v5 是 2026 年默认选择 |
| Jitter buffer | "Audio smoothing" | Client-side buffer that holds packets briefly to absorb network variance |
| Jitter buffer | "音频平滑" | 客户端缓冲区，短暂保存数据包以吸收网络波动 |
| Filler | "Acknowledgment token" | Short phrase the agent emits to avoid silence when a tool is slow |
| 填充语 | "确认 token" | 工具响应慢时 Agent 发出的短句以避免沉默 |
| MOS | "Mean opinion score" | Perceptual speech quality rating; NISQA is the automated proxy |
| MOS | "平均意见评分" | 感知语音质量评分；NISQA 是自动化代理 |

## 继续阅读 继续阅读

- [LiveKit Agents 1.0](https://github.com/livekit/agents)参考WebRTC代理框架
  中文翻译:参考WebRTC代理 框架
- [Pipecat](https://github.com/pipecat-ai/pipecat)替代Python-第一流媒体代理框架
  中文翻译:备选的Python 优先流式代理 框架
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime) 关于集成语音模型的参考
  中文翻译:集成语音模型的参考
- [Deepgram Nova-3 documentation](https://developers.deepgram.com/docs)流媒体ASR引用
  中文翻译:流式 ASR 参考
- [Silero VAD v5](https://github.com/snakers4/silero-vad) VAD 参考模型
  中文翻译:VAD 参考模型
- [Cartesia Sonic-2](https://docs.cartesia.ai)低延迟TTS参考
  中文翻译:低延迟 TTS 参考
- [Retell AI architecture](https://docs.retellai.com)生产语音代理架构
  中文翻译:生产级语音 代理架构
- [Vapi.ai production stack](https://docs.vapi.ai)替代生产参考
  中文翻译:备选的生产级参考
