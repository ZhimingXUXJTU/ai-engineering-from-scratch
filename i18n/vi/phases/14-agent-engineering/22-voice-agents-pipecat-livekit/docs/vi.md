# Pipecat và LiveKit

> Các đại lý thoại là một loại sản xuất hạng nhất vào năm 2026. Pipecat cung cấp cho bạn một đường ống dựa trên khung Python (VAD → STT → LLM → TTS → vận chuyển). LiveKit Agents nối các mô hình AI với người dùng qua WebRTC. Mục tiêu độ trễ sản xuất hạ cánh ở 450600ms từ đầu đến cuối cho các đống cao cấp.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Mục tiêu học tập

- Mô tả đường ống dựa trên khung của Pipecat: DOWNSTREAM (nguồn→sink) và UPSTREAM (các bộ điều khiển).
- Tên gọi các giai đoạn đường ống âm thanh truyền thống và vận chuyển hỗ trợ của Pipecat.
- Giải thích hai lớp đại lý giọng nói của LiveKit Agents (MultimodalAgent, VoicePipelineAgent) và khi nào mỗi lớp phù hợp.
- Tóm lại kỳ vọng độ trễ sản xuất năm 2026 và cách chúng thúc đẩy các lựa chọn kiến trúc.

## Vấn đề  vấn đề giới thiệu

Các đại lý thoại không phải là một vòng lặp văn bản với TTS được gắn. Ngân sách độ trễ là tàn bạo (~ 600ms), âm thanh một phần là mặc định, phát hiện lượt là một mô hình, và vận chuyển từ điện thoại SIP đến WebRTC.

> 语音 Đại lý không phải là vòng lặp văn bản cộng với TTS──延迟预算极其严苛(约600ms),部分音频是默认状态,轮次检测是一个模型,传输方式从电话SIP到WebRTC 不等──你要么构建一个基于的管道(Pipecat),要么依赖一个平台(LiveKit)──


> **【中文解读】**语音 đại lý 需要实时处理音频流语音识别(ASR) LLM 推理、语音合成(TTS) 延迟 phải ở trong 300ms 以内 để duy trì cuộc đối thoại tự nhiên.

> **{【拓展：Pipecat（开源框架）和 LiveKit（实时音频基础设施）是 2026 年语音 Agent 生...】}**Pipecat (tiếng Anh: Pipecat) và LiveKit (LiveKit) là một trong những hệ thống truyền hình âm thanh của Trung tâm phát thanh của Trung tâm phát thanh của năm 2026. Pipecat cung cấp các ống xử lý âm thanh được phân tích, hỗ trợ nhiều loại ASR / TTS / LLM.

>  **【前置】**Học本节前请先掌握:Phase 14·01(Agent Loop) 理解 ReAct 循环,本节是在循环外加一层音频管道;Phase 14·12(Workflow Patterns) 理解多阶段工作流的概念──另外最好有数字信号处理基础概念──采样率、、流式处理),否则看"框架型管道" 会很──

## Khái niệm cốt lõi

### Chiếc pipecat (pipecat-ai/pipecat)

- Phụ trình đường ống dựa trên khung Python.
- `Frame`→ `FrameProcessor`- Sợi dây.
- Hai hướng chảy:
  - **DOWNSTREAM** nguồn → bồn rửa (audio in, TTS out).
  - **UPSTREAM** phản hồi và kiểm soát (bấm, số liệu, barge-in).
- `PipelineTask`quản lý chu kỳ đời sống với các sự kiện (`on_pipeline_started`- `on_pipeline_finished`- `on_idle_timeout`) và các nhà quan sát cho các métrics/tracing/RTVI.

Đường ống thông điển hình:

```
VAD (Silero) → STT → LLM (context alternates user/assistant) → TTS → transport
```

Giao thông: Daily, LiveKit, SmallWebRTCTransport, FastAPI WebSocket, WhatsApp.

>  **【类比】**Pipecat's frame-based pipeline 像汽车流水线:每个工位(Prosessor) chỉ làm một việc  VAD 工位识别有没有人说话、STT 工位把语音转文字、LLM 工位想回复、TTS 工位把文字转语音),车架(Frame) Từ đi sau流过(DOWNSTREAM), bất kỳ một工位 tìm thấy vấn đề chất lượng có thể theo tuyến đỏ dừng xe(UPSTREAM hủy  đây là cơ chế phá vỡ ) 

> 语音 đại lý 结合 LLM 和实时语音处理──Pipecat 和 LiveKit là hai loại đại lý tiếng 框架, phân biệt xử lý âm thanh ống và thực时通信──

Pipecat Flows thêm các cuộc trò chuyện có cấu trúc (cỗ máy trạng thái). Pipecat Cloud là thời gian chạy được quản lý.

> 语音 đại lý 结合 LLM 和实时语音处理──Pipecat 和 LiveKit là hai loại đại lý tiếng 框架, phân biệt xử lý âm thanh ống và thực时通信──

### LiveKit Agents (livekit/agents)

- Đường nối các mô hình AI với người dùng qua WebRTC.
- Các khái niệm chính: `Agent`- `AgentSession`- `entrypoint`- `AgentServer`- Tôi không biết.
- Hai lớp học đại lý giọng nói:
  - **MultimodalAgent** âm thanh trực tiếp thông qua OpenAI Realtime hoặc tương đương.
  - **VoicePipelineAgent** STT → LLM → TTS; cung cấp kiểm soát ở cấp độ văn bản.
- Khám phá biến đổi ngữ nghĩa thông qua mô hình biến đổi.
- Sự tích hợp MCP bản địa.
- Điện thoại qua SIP.
- 50+ mô hình không có khóa API thông qua LiveKit Inference; 200+ hơn thông qua plugin.

### Các nền tảng thương mại

Vapi (~ 450600ms trên một gói Premium tối ưu hóa) và Retell (~ 600ms kết thúc đến kết thúc trên 180 cuộc gọi thử nghiệm) xây dựng trên đầu này. Chọn một nền tảng khi bạn muốn một gói giọng nói được quản lý mà không cần một nhóm WebRTC.

> 🤔 **【困惑】**Q: MultimodalAgent(音频进音频出) 和 VoicePipelineAgent(STT→LLM→TTS 级联) ¿到底选哪个? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少控制权? A: 看你需要多少权? A: 看你需要控制权?

> Vapi(optimize后的高级堆约450-600ms) 和 Retell(180次测试通话端到端约600ms) xây dựng trên những người này.

> 语音 đại lý 结合 LLM 和实时语音处理──Pipecat 和 LiveKit là hai loại đại lý tiếng 框架, phân biệt xử lý âm thanh ống và thực时通信──

### Khi mô hình này đi sai

- **No barge-in handling.**Người dùng ngắt lời; đại lý tiếp tục nói chuyện. yêu cầu UPSTREAM hủy khung hình trong Pipecat, tương đương trong LiveKit.
- **STT confidence ignored.**Các bản ghi tự tin thấp được đưa đến LLM như là tin mừng.
- **TTS mid-sentence cutoff.**Khi đường ống hủy bỏ giữa phát âm, TTS cần biết hoặc cắt âm thanh.
- **Latency budget ignored.**Mỗi thành phần thêm 50200ms. Tổng chuỗi của bạn trước khi vận chuyển.

> **没有打断处理。**Người dùng chia tay;Agent  tiếp tục nói chuyện.
> **忽略 STT 置信度。**低信度转录被当作真理传给LLM.
> **TTS 句中截断。**Khi đường ống trong khi nói giữa bị hủy bỏ, TTS cần biết hoặc cắt âm thanh.
> **忽略延迟预算。**Mỗi bộ phận tăng 50-200ms.

### Típ trễ 2026

- VAD: 2060ms
- STT một phần: 100250ms
- LLM đầu tiên: 150400ms
- TTS âm thanh đầu tiên: 100200ms
- RTT vận chuyển: 3080ms

End-to-end 450600ms là cao cấp. 8001200ms là phổ biến. Bất cứ điều gì > 1500ms cảm thấy bị phá vỡ.

> 端到端 450-600ms là mức cao端――800-1200ms là mức thường thấy――超过1500ms 感觉就会出问题――

> 语音 đại lý 结合 LLM 和实时语音处理──Pipecat 和 LiveKit là hai loại đại lý tiếng 框架, phân biệt xử lý âm thanh ống và thực时通信──

## Hãy xây dựng nó.

> ️ **【易错点】**新手搭语音管道常踩3 个坑:(1) **不做 barge-in 处理** người dùng打断时 Agent còn trong tự顾自地说,体验极差, phải ở trong bộ xử lý TTS 监听 UPSTREAM hủy frame 并立即停止音频输出──(2) **忽略 STT 置信度**置信度 0.3 的""被当成用户回答,Agent 走错分支;修复:confiance < 0.7 时让 Agent 反问"我没听清,能再说一次吗"―(3) **延迟预算算总账** độc lập xem mỗi bộ phận đều đạt tiêu chuẩn(VAD 40ms + STT 200ms + LLM 300ms + TTS 150ms = 690ms), nhưng trên đường hậu đến cuối 1200ms, vì漏算网络 RTT và队列等待──修复: sử dụng giai đoạn 14·23 OTel span 测真链路, đừng đánh bộ não──
```figure
voice-pipeline
```

## Hãy xây dựng nó

`code/main.py`là một đường ống đồ chơi dựa trên khung với:

> 语音 đại lý 结合 LLM 和实时语音处理──Pipecat 和 LiveKit là hai loại đại lý tiếng 框架, phân biệt xử lý âm thanh ống và thực时通信──

- `Frame`các loại (audio, bản sao, văn bản, tts_audio, điều khiển).
- `Processor`giao diện với `process(frame)`- Tôi không biết.
- Một đường ống năm giai đoạn (VAD → STT → LLM → TTS → vận chuyển) như bộ xử lý kịch bản.
- Một khung hủy UPSTREAM để chứng minh sự đột nhập.

Đi đi.

```
python3 code/main.py
```

Hình ảnh cho thấy dòng chảy bình thường và một sự hủy bỏ của tàu bay đã ngăn chặn TTS giữa phát âm.

> 追踪 hiển thị quá trình bình thường và một trong các cuộc nói giữa dừng TTS của 打断取消──

> 语音 đại lý 结合 LLM 和实时语音处理──Pipecat 和 LiveKit là hai loại đại lý tiếng 框架, phân biệt xử lý âm thanh ống và thực时通信──

## Hãy sử dụng nó để thực hiện

- **Pipecat**cho sự kiểm soát đầy đủ  bộ xử lý tùy chỉnh, Python-first, các nhà cung cấp pluggable.
- **LiveKit Agents**cho việc triển khai WebRTC đầu tiên và điện thoại.
- **Vapi / Retell**cho các đại lý giọng nói không có đội WebRTC.
- **OpenAI Realtime / Gemini Live**cho âm thanh trực tiếp vào/ ra khỏi (MultimodalAgent).

## Chuyển nó đi.

`outputs/skill-voice-pipeline.md`Đàn phẳng một đường ống giọng hình Pipecat với VAD + STT + LLM + TTS + vận chuyển cộng với xử lý tàu thuyền.

> `outputs/skill-voice-pipeline.md`Xây dựng một ống thông tiếng Pipecat 形态, bao gồm VAD + STT + LLM + TTS + 传输以及打断处理──

> 语音 đại lý 结合 LLM 和实时语音处理──Pipecat 和 LiveKit là hai loại đại lý tiếng 框架, phân biệt xử lý âm thanh ống và thực时通信──

## Tập luyện bài tập

1. Thêm một người quan sát số liệu vào đường ống đồ chơi của bạn: đếm khung mỗi giai đoạn mỗi giây.
  Trung ngữ翻译:思考并实践此练习。
2. Thực hiện STT có cửa độ tin cậy: dưới ngưỡng, yêu cầu "bạn có thể lặp lại điều đó không?"
  Trung ngữ翻译:思考并实践此练习。
3. Thêm nhận lượt ngữ nghĩa: quy tắc đơn giản  nếu bản sao kết thúc bằng "?", cuối lượt.
  Trung ngữ翻译:思考并实践此练习。
4. Đọc các tài liệu vận chuyển của Pipecat. Thay đổi STDlib vận chuyển cho cấu hình SmallWebRTCTransport (stub).
  Trung ngữ翻译:思考并实践此练习。
5. Đo một chuỗi OpenAI thời gian thực so với STT + LLM + TTS trên cùng một truy vấn. Chi phí trễ nào được kiểm soát ở cấp độ văn bản mang lại?
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Frame | "Event" | Typed unit of data in the pipeline (audio, transcript, text, control) |  |
| Processor | "Pipeline stage" | Handler with process(frame) |  |
| DOWNSTREAM | "Forward flow" | Source to sink: audio in, speech out |  |
| UPSTREAM | "Feedback flow" | Control: cancel, metrics, barge-in |  |
| VAD | "Voice activity detection" | Detects when user is speaking |  |
| Semantic turn detection | "Smart end-of-turn" | Model-based decision that the user is done |  |
| MultimodalAgent | "Direct audio agent" | Audio in, audio out; no text in the middle |  |
| VoicePipelineAgent | "Cascade agent" | STT + LLM + TTS; text-level control |  |

## Xem thêm 延伸阅读

- [Pipecat docs](https://docs.pipecat.ai/getting-started/introduction) đường ống dựa trên khung, bộ xử lý, vận chuyển
  Trung ngữ: 翻译:见原文.
- [LiveKit Agents docs](https://docs.livekit.io/agents/) WebRTC + âm thanh nguyên thủy
  Trung ngữ: 翻译:见原文.
- [Vapi](https://vapi.ai/) nền tảng thoại được quản lý
  Trung ngữ: 翻译:见原文.
- [Retell AI](https://www.retellai.com/) quản lý giọng nói, trễ-chỉ số
  Trung ngữ: 翻译:见原文.
