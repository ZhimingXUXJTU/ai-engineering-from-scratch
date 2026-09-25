# Xây dựng một đường ống trợ lý giọng nói  Lớp 6 Capstone  xây dựng语音助手流水线  阶段 6 毕业项目

> Tất cả từ bài học 01-11, được đan kết hợp. Hãy xây dựng một trợ lý giọng nói lắng nghe, lý luận và nói lại. Năm 2026 đó là một vấn đề kỹ thuật được giải quyết, không phải là một vấn đề nghiên cứu  nhưng chi tiết tích hợp quyết định liệu nó có vận chuyển hay không.

> **【中文解读】**Hãy kết nối tất cả các nội dung của bài học 01-11 , xây dựng một trợ lý tiếng có thể nghe, có thể nghĩ, có thể nói. Năm 2026 đây là một vấn đề kỹ thuật đã được giải quyết, chứ không phải là vấn đề nghiên cứu.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 05, 06, 07, 11; Phase 11 · 09 (Function Calling); Phase 14 · 01 (Agent Loop) | **前置知识:** 阶段 6 · 04、05、06、07、11；阶段 11 · 09（函数调用）；阶段 14 · 01（智能体循环）
**Time:** ~120 minutes | **预计用时:** ~120 分钟

## Vấn đề  vấn đề giới thiệu

Xây dựng một trợ lý đầu đến cuối:

> 构建一个端到端助手:

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

1. Chụp đầu vào micro (16 kHz mono).
   捕获麦克风输入(16 kHz 单声道)
2. Khám phá bắt đầu/sự nói của người dùng.
   检测用户语音的开始/结束──
3. Chuyển lại dòng phát.
   Chuyển chuyển:
4. Chuyển bản sao cho một LLM có thể gọi các công cụ (timer, thời tiết, lịch).
   sẽ chuyển tải vào các công cụ có thể sử dụng để làm việc của LLM
5. Chuyển văn bản LLM cho một TTS.
   Để LLM 文本流式传输给TTS──
6. Đưa âm thanh trở lại người dùng.
   向用户播放音频──
7. Ngưng nếu người dùng gián đoạn giữa phản ứng.
   Nếu người dùng trong phản ứng đột ngột thì dừng lại.

Mục tiêu trễ: đầu tiên TTS byte âm thanh trong vòng 800 ms của người dùng hoàn thành phát biểu của họ trên một CPU máy tính xách tay. Mục tiêu chất lượng: không có từ bỏ, không có phụ đề ảo giác trên im lặng, không có rò rỉ nhân bản giọng nói, không có sự thành công tiêm nhanh chóng.

> 延迟目标: 在笔记本 CPU 上用户说完话后 800 ms 内发出第一个 TTS 音频字节──质量目标:不漏词、静音不产生幻觉字幕、无声音克隆泄漏、提示注入不成功──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Voice assistant pipeline: mic → VAD → STT → LLM+tools → TTS → speaker](../assets/voice-assistant.svg)

### Bảy thành phần

1. **Audio capture.**Mic → 16 kHz mono → 20 ms. thường `sounddevice`trong Python hoặc AudioUnit/ALSA/WASAPI bản địa trong sản xuất.
   **音频捕获。**麦克风 → 16 kHz 单声道 → 20 ms 块──Python 中通常使用 `sounddevice`, sản xuất môi trường sử dụng nguyên sinh AudioUnit/ALSA/WASAPI。
2. **VAD (Lesson 11).**Silero VAD @ ngưỡng 0,5, min nói 250 ms, im lặng hangover 500 ms. tín hiệu "bắt đầu" và "sự kết thúc".
   **VAD（第 11 课）。**Silero VAD @ 值 0.5, tối thiểu语音 250 ms,静音持续 500 ms──信号"开始"和"结束"──
3. **Streaming STT (Lesson 4-5).**Whisper-streaming, Parakeet-TDT, hoặc Deepgram Nova-3 (API).
   **流式 STT（第 4-5 课）。**Whisper-streaming、Parakeet-TDT 或 Deepgram Nova-3(API) 』部分 + 最终转录──
4. **LLM with tool calling.**GPT-4o / Claude 3.5 / Gemini 2.5 Flash. JSON schema cho công cụ.
   **带工具调用的 LLM。**GPT-4o / Claude 3.5 / Gemini 2.5 Flash──工具的 JSON schema──流式代码──
5. **Streaming TTS (Lesson 7).**Kokoro-82M (cởi mở nhanh nhất) hoặc Cartesia Sonic (thị mại).
   **流式 TTS（第 7 课）。**Kokoro-82M (最快的开源) 或 Cartesia Sonic (商业) ⋅ 在 20 个 LLM token 后启动 TTS──
6. **Playback.**Đóng loa; mã hóa opus cho mạng băng thông thấp.
   **回放。**扬声器输出;低带宽网络用 opus 编码。
7. **Interruption handler.**Nếu VAD nổ trong thời gian phát lại TTS, dừng phát lại, hủy LLM, khởi động lại STT.
   **打断处理器。**Nếu TTS 播放期间 VAD 触发, ngừng播放、取消 LLM、重启 STT。

### Ba chế độ thất bại bạn sẽ nhấn

> ### Bạn sẽ gặp phải ba kiểu thất bại

1. **First-word clip.**VAD bắt đầu một đập quá muộn. người dùng "hey" bị mất. bắt đầu ngưỡng ở 0,3, không phải 0,5.
   **首词截断。**VAD  khởi động một lần. Người dùng của bạn đã mất.
2. **Mid-response interrupt confusion.**LLM tiếp tục tạo sau khi người dùng gián đoạn; trợ lý nói chuyện trên người dùng.
   **回应中打断混乱。**Người dùng cắt đứt sau LLM  tiếp tục tạo; trợ giúp áp áp trên người dùng nói chuyện.
3. **Silence hallucination.**"Cảm ơn vì đã xem" trên khung làm nóng âm thầm.
   **静音幻觉。**Whisper 在静音预热上输出 "Cảm ơn đã xem"──务必用 VAD 过──

### 2026 hàng tham chiếu sản xuất

| Stack | Latency | License | Notes |
|-------|---------|---------|-------|
| LiveKit + Deepgram + GPT-4o + Cartesia | 350-500 ms | commercial API | Industry default 2026 |
| Pipecat + Whisper-streaming + GPT-4o + Kokoro | 500-800 ms | mostly open | DIY-friendly |
| Moshi (full-duplex) | 200-300 ms | CC-BY 4.0 | Single-model; different architecture, lesson 15 |
| Vapi / Retell (managed) | 300-500 ms | commercial | Fastest to launch; limited customization |
| Whisper.cpp + llama.cpp + Kokoro-ONNX | offline | open | Privacy / edge |

| 技术栈 | 延迟 | 许可 | 备注 |
|--------|------|------|------|
| LiveKit + Deepgram + GPT-4o + Cartesia | 350-500 ms | 商业 API | 2026 行业默认 |
| Pipecat + Whisper-streaming + GPT-4o + Kokoro | 500-800 ms | 多数开源 | DIY 友好 |
| Moshi（全双工） | 200-300 ms | CC-BY 4.0 | 单模型；不同架构，第 15 课 |
| Vapi / Retell（托管） | 300-500 ms | 商业 | 最快上线；定制有限 |
| Whisper.cpp + llama.cpp + Kokoro-ONNX | 离线 | 开源 | 隐私/边缘 |

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.

> **【拓展：语音隐私与安全】**语音数据 chứa rất nhiều thông tin cá nhân riêng tư (音纹、对话内容) ◦深度伪造 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术) 语音技术 (反欺诈) 语音技术 (反欺诈) 防伪 (反伪造) 防伪研究热点) 热点





## Hãy xây dựng nó.
```figure
v4-voice-latency
```

## Hãy xây dựng nó

### Bước 1: chụp micro bằng cách chunking (pseudocode)

```python
import sounddevice as sd

def mic_stream(chunk_ms=20, sr=16000):
    q = queue.Queue()
    def cb(indata, frames, time, status):
        q.put(indata.copy().flatten())
    with sd.InputStream(channels=1, samplerate=sr, blocksize=int(sr * chunk_ms/1000), callback=cb):
        while True:
            yield q.get()
```

### Bước 2: Tận dạng vòng quay được vạch VAD

```python
def capture_turn(stream, vad, pre_roll_ms=300, silence_ms=500):
    buf, pre, triggered = [], collections.deque(maxlen=pre_roll_ms // 20), False
    silent = 0
    for chunk in stream:
        pre.append(chunk)
        if vad(chunk):
            if not triggered:
                buf = list(pre)
                triggered = True
            buf.append(chunk)
            silent = 0
        elif triggered:
            silent += 20
            buf.append(chunk)
            if silent >= silence_ms:
                return b"".join(buf)
```

### Bước 3: streaming STT → LLM → TTS

```python
async def turn(audio_bytes):
    transcript = await stt.transcribe(audio_bytes)
    async for token in llm.stream(transcript):
        async for audio in tts.stream(token):
            await speaker.play(audio)
```

### Bước 4: Công cụ gọi bên trong vòng LLM

```python
tools = [
    {"name": "get_weather", "parameters": {"location": "string"}},
    {"name": "set_timer", "parameters": {"seconds": "int"}},
]

async for chunk in llm.stream(user_text, tools=tools):
    if chunk.type == "tool_call":
        result = dispatch(chunk.name, chunk.args)
        continue_streaming(result)
    if chunk.type == "text":
        await tts.stream(chunk.text)
```

### Bước 5: xử lý gián đoạn

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


```python
tts_task = asyncio.create_task(tts_loop())
while True:
    chunk = await mic.get()
    if vad(chunk):
        tts_task.cancel()
        await speaker.stop()
        await new_turn()
        break
```




> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

Nhìn xem`code/main.py`cho một mô phỏng chạy được kết nối tất cả bảy thành phần với các mô hình trục, để bạn có thể thấy hình dạng đường ống ngay cả khi không cần phần cứng.

> 参见 `code/main.py`获取可运行的模拟,将七组件用模块连接,无需硬件即可见流水线形状──实际实现时,将模块替换为:

- `silero-vad`(`pip install silero-vad`) / VAD 模块
- `deepgram-sdk`hoặc `openai-whisper`/ 流式 STT
- `openai`(`gpt-4o`) hoặc `anthropic`/ LLM + 工具调用
- `kokoro`hoặc `cartesia`/ 流式 TTS
- `sounddevice`cho I/O / 音频输入输出



## Những bẫy

> 常见陷

- **Logging PII forever.**Tiếng nghe quay đầy đủ là thông tin cá nhân ở hầu hết các khu vực pháp lý.
  **永久记录 PII。**完整轮次音频在多数司法管辖区属于PII──30 天保留,静态加密──
- **No barge-in.**Người dùng sẽ ngắt lời, trợ lý của bạn phải ngừng nói chuyện.
  **没有抢话。**Người dùng sẽ đập đập. Người trợ lý của bạn phải dừng nói.
- **TTS that blocks.**TTS đồng bộ chặn vòng lặp sự kiện. Sử dụng async hoặc một chuỗi riêng biệt.
  **阻塞式 TTS。**Đồng步 TTS 阻塞事件循环──使用异步或独立线程──
- **No tool-call error handling.**Các công cụ thất bại. LLM phải lấy lại lỗi + thử lại một lần, sau đó hạ thấp lịch sử.
  **没有工具调用错误处理。**工具会失败──LLM 必须收到错误 + 重试一次,然后优雅降级──
- **Overzealous hallucination filters.**Over-filter và trợ lý lặp lại "Tôi không thể giúp được với điều đó". Under-filter và nó nói bất cứ điều gì.
  **过度激进的幻觉过滤。**过度过助手会重复"我帮不了"──过不足则什么都说──在留出集上校准──
- **No wake-word option.**Luôn lắng nghe là một trách nhiệm về quyền riêng tư.
  **没有唤醒词选项。**持续监听是隐私负担──添加唤醒词门控(Porcupine 或 openWakeWord)──

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-voice-assistant-architect.md`. Với hạn chế ngân sách + quy mô + ngôn ngữ + tuân thủ, tạo ra một thông số kỹ thuật đầy đủ.

> 保存为 `outputs/skill-voice-assistant-architect.md` Giới hạn ngân sách + quy mô + ngôn ngữ + quy định, sản xuất toàn bộ kỹ thuật quy định

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`Nó mô phỏng một vòng hoàn toàn từ đầu đến cuối với các mô-đun và in theo thời gian mỗi giai đoạn.
   **简单。**运行 `code/main.py`模块模拟一个完整轮次端到端并印各阶段延迟
2. **Medium.**Thay thế STT stub bằng một mô hình Whisper thực sự trên một bản ghi trước `.wav`- đo WER và độ trễ đầu đến cuối.
   **中等。**Trong dự án`.wav`上用真实 Whisper 模型替换 STT 模块──测量 WER 和端到端延迟──
3. **Hard.**Thêm công cụ gọi: thực hiện `get_weather`(bất kỳ API nào) và `set_timer`. Định hướng LLM qua các công cụ và xác minh rằng khi người dùng nói "đặt một bộ hẹn giờ 5 phút" chức năng đúng phát ra và câu trả lời nói xác nhận điều đó.
   **困难。**添加工具调用:实现 `get_weather`(bất kỳ API) và `set_timer`❖ Thông qua các công cụ từ LLM, xác nhận khi người dùng nói "đặt một 5 phút định thời gian" thì hàm chính xác được调用。

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Turn | A user + assistant round-trip | One VAD-bounded user speech + one LLM-TTS response. |
| Barge-in | Interruption | User speaks while assistant talks; assistant stops. |
| Wake word | "Hey assistant" | Short keyword detector; Porcupine, Snowboy, openWakeWord. |
| End-pointing | Turn ending | VAD + min-silence decision that user has finished. |
| Pre-roll | Pre-speech buffer | Keep 200-400 ms of audio before VAD fires to avoid first-word clip. |
| Tool call | Function invocation | LLM emits JSON; runtime dispatches; result feeds back in-loop. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 轮次 | 用户+助手一个来回 | 一次 VAD 界定的用户语音 + 一次 LLM-TTS 回应。 |
| 抢话 | 打断 | 助手说话时用户开口；助手停止。 |
| 唤醒词 | "嘿助手" | 短关键词检测器；Porcupine、Snowboy、openWakeWord。 |
| 端点检测 | 轮次结束 | VAD + 最小静音决策用户已说完。 |
| 预滚 | 语音前缓冲 | 在 VAD 触发前保留 200-400 ms 音频以避免首词截断。 |
| 工具调用 | 函数调用 | LLM 输出 JSON；运行时分发；结果在循环中反馈。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [LiveKit — voice agent quickstart](https://docs.livekit.io/agents/) tham chiếu cấp sản xuất.
  LiveKit语音智能体快速进入生产级参考
- [Pipecat — voice agent examples](https://github.com/pipecat-ai/pipecat) Khung thân thiện với DIY.
  Pipecat语音智能体示例DIY 友好框架。
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime) con đường âm thanh bản địa được quản lý.
  OpenAI Realtime API托管的语音原生路径──
- [Kyutai Moshi](https://github.com/kyutai-labs/moshi) Đề xuất duplex đầy đủ (Học 15).
  Kyutai Moshi全双工参考(第 15 课)。
- [Porcupine wake-word](https://picovoice.ai/products/porcupine/) Đánh cửa từ thức dậy.
  Lợn lợn 唤醒词唤醒词门控――
- [Anthropic — tool use guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) LLM chức năng gọi.
  Antropic工具使用指南LLM 函数调用。

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

