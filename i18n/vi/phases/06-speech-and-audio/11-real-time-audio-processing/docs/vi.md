# Tiêu chuẩn âm thanh thời gian thực  Tiêu chuẩn âm thanh thời gian thực

> Các đường ống hàng xử lý một tập tin. Các đường ống hàng thời gian thực xử lý 20 millisecond tiếp theo trước khi 20 giây tiếp theo đến. Mỗi AI trò chuyện, studio phát sóng và bot điện thoại sống và chết bằng ngân sách trễ này.

> **【中文解读】**批处理流水线处理文件,实时流水线在下20毫秒到达之前处理完整这20毫秒.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 6 · 04 (ASR), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 02（频谱图），阶段 6 · 04（ASR），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Bạn muốn một trợ lý giọng nói cảm thấy sống. thời gian trễ chuyển đổi cuộc trò chuyện của con người là ~ 230 ms (trầm lặng để trả lời). Bất cứ điều gì trên 500 ms cảm thấy robot; trên 1500 ms cảm thấy vỡ. Ngân sách cho một đầy đủ **hear → understand → respond → speak**vòng vào năm 2026 là:

> Bạn muốn một trợ lý tiếng "sống"―― cuộc nói chuyện của con người lần lượt chậm khoảng 230 ms(静音到回应)―― hơn 500 ms 感觉像机器人; hơn 1500 ms 感觉坏掉――2026年完整**听 → 理解 → 回应 → 说**循环预算 là:

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

| Stage | Budget |
|-------|--------|
| Mic → buffer | 20 ms |
| VAD | 10 ms |
| ASR (streaming) | 150 ms |
| LLM (first token) | 100 ms |
| TTS (first chunk) | 100 ms |
| Render → speaker | 20 ms |
| **Total** | **~400 ms** |

| 阶段 | 预算 |
|------|------|
| 麦克风 → 缓冲 | 20 ms |
| VAD | 10 ms |
| ASR（流式） | 150 ms |
| LLM（首 token） | 100 ms |
| TTS（首块） | 100 ms |
| 渲染 → 扬声器 | 20 ms |
| **总计** | **约 400 ms** |

Moshi (Kyutai, 2024) đã đồng hồ 200 ms đầy đủ duplex. GPT-4o-time (2024) đồng hồ ~ 320 ms. Các đường ống nước ngập vào năm 2022 được vận chuyển với 2500 ms. Sự cải tiến 10x đến từ ba kỹ thuật: (1) truyền khắp nơi, (2) đường ống không đồng bộ với kết quả một phần, (3) sản xuất bị gián đoạn.

> Moshi(Kyutai,2024) đạt được 200 ms 全双工──GPT-4o-realtime(2024) khoảng 320 ms──2022 năm của cấp联流水线延迟 2500 ms──10倍提升来自三个技术:(1) 全面流式化,(2) 带部分结果的异步流水线,(3) 可中断生成──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Streaming audio pipeline with ring buffer, VAD gate, interruption](../assets/real-time.svg)

**Frame / chunk / window.**Đường độ âm thanh trong thời gian thực được chuyển đổi thành khối kích thước cố định.

> **帧/块/窗口。**实时音频以固定大小的块流动──常见选择:20 ms(16 kHz 下 320 采样点)──下游一切都必须跟上这个节奏──

**Ring buffer.**Bộ đệm vòng tròn kích thước cố định. Dòng sản xuất viết khung mới, dây tiêu dùng đọc. ngăn chặn phân bổ trong đường nóng. kích thước ≈ độ trễ tối đa × tốc độ mẫu; vòng 16 kHz 2 giây = 32.000 mẫu.

> **环形缓冲区。**固定大小的循环缓冲区──生产者线程写入新,消费者线程读取──防止热路中的内存分配──大小约等于最大延迟 × 采样率;2秒 16 kHz 环形缓冲 = 32,000 采样点──

**VAD (Voice Activity Detection).**Gates hoạt động dòng chảy xuống khi không ai nói. Silero VAD 4.0 (2024) chạy < 1 ms mỗi khung hình 30 ms trên CPU. `webrtcvad`là sự thay thế cũ hơn.

> **VAD（语音活动检测）。**无人说话时阻止下游工作──Silero VAD 4.0(2024) trên CPU trên mỗi 30 ms 运行 <1 ms──`webrtcvad`Đó là một giải pháp thay thế cũ hơn.

**Streaming ASR.**Các mô hình phát ra bản ghi âm một phần khi âm thanh đến. Parakeet-CTC-0.6B trong chế độ phát trực tuyến (NeMo, 2024) thực hiện 25% WER với độ trễ 320 ms. Whisper-Streaming (Macháček et al., 2023) phân đoạn Whisper cho gần phát trực tuyến với độ trễ ~ 2 s.

> **流式 ASR。**随音频到达而输出部分转录的模型──Parakeet-CTC-0.6B 流式模式──NeMo,2024) ở 320 ms 延迟下 đạt 2-5% WER──Whisper-Streaming──Macháček 等,2023) sẽ Whisper 分块 để đạt được gần dòng chảy khoảng 2 giây延迟──

**Interruption.**Khi người dùng nói trong khi trợ lý đang nói, bạn phải (a) phát hiện sự đột nhập, (b) dừng TTS, (c) loại bỏ các kết quả LLM còn lại. Tất cả trong vòng 100 ms, hoặc người dùng nhận thấy trợ lý điếc.

> **打断。**Khi trợ lý trong cuộc nói chuyện khi người dùng mở cửa, bạn phải (a) kiểm tra để bắt đầu nói chuyện, (b) ngừng TTS, (c) bỏ phần còn lại của LLM 输出──全部在100 ms内完成,否则用户感觉助手是聋子──

**WebRTC Opus transport.**20 ms khung hình, 48 kHz, tốc độ bit thích ứng 8128 kbps. tiêu chuẩn cho trình duyệt và di động. LiveKit, Daily.co, Pion là các gói 2026 để xây dựng ứng dụng thoại.

> **WebRTC Opus 传输。**20 ms ,48 kHz, tự ứng dụng tỷ lệ 8-128 kbps .

**Jitter buffer.**Các gói mạng đến không đúng giờ / muộn. bộ đệm jitter sắp xếp lại và làm mượt mà; khoảng trống nhỏ quá → nghe thấy, quá lớn → độ trễ. 6080 ms điển hình.

> **抖动缓冲区。**网络包乱序/迟到达──动缓冲区重排和平滑;太小 → 可听间隙,太大 → 延迟──典型值 60-80 ms──

### Thị trường chung

> ### 常见陷

- **Thread contention.**Các mô hình nặng GIL + của Python có thể làm mất đi dây chuyền âm thanh. Sử dụng thư viện âm thanh C-callback (hỗ máy âm thanh, PortAudio) và giữ Python khỏi con đường nóng.
  **线程竞争。**GIL của Python + 重模型会使音频线程饥饿──使用 C 回调音频库(sounddevice、PortAudio),让 Python 远离热路径──
- **Sample-rate conversion latency.**Phân tích lại bên trong đường ống thêm 520 ms. Hoặc lấy lại mẫu trước hoặc sử dụng một mẫu lại không trễ (PolyPhase, `soxr_hq`().
  **采样率转换延迟。**流水线内部重采采集增加5-20 ms──要么提前重采采,要么使用零延迟重采采器──
- **TTS priming.**Ngay cả TTS nhanh như Kokoro cũng có tốc độ nóng lên 100200 ms khi yêu cầu đầu tiên.
  **TTS 预热。**Ngay cả như Kokoro như TTS tốc độ nhanh trong lần đầu tiên yêu cầu cũng có 100-200 ms 预热──缓存模型 + trong lần thực đầu tiên 预运行假预热──
- **Echo cancellation.**Không có AEC, đầu ra TTS quay lại vào micrô và kích hoạt ASR trên giọng nói của bot. WebRTC AEC3 là mặc định nguồn mở.
  **回声消除。**Không có AEC, TTS 输出重新进入麦克风并触发 ASR 识别机器人自己的声音──WebRTC AEC3 là một giải pháp mở.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.

> **【拓展：语音隐私与安全】**语音数据 chứa rất nhiều thông tin cá nhân riêng tư (音纹、对话内容) ◦深度伪造 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术) 语音技术 (反欺诈) 语音技术 (反欺诈) 防伪 (反伪造) 防伪研究热点) 热点





## Hãy xây dựng nó.
```figure
nyquist-aliasing
```

## Hãy xây dựng nó

### Bước 1: bơm vòng

```python
import collections

class RingBuffer:
    def __init__(self, capacity):
        self.buf = collections.deque(maxlen=capacity)
    def write(self, frame):
        self.buf.extend(frame)
    def read(self, n):
        return [self.buf.popleft() for _ in range(min(n, len(self.buf)))]
    def level(self):
        return len(self.buf)
```

Công suất xác định độ trễ tối đa. 32.000 mẫu ở 16 kHz = 2 s.

### Bước 2: Cổng VAD

```python
def simple_energy_vad(frame, threshold=0.01):
    return sum(x * x for x in frame) / len(frame) > threshold ** 2
```

Thay thế bằng Silero VAD trong sản xuất:

```python
import torch
vad, _ = torch.hub.load("snakers4/silero-vad", "silero_vad")
is_speech = vad(torch.tensor(frame), 16000).item() > 0.5
```

### Bước 3: phát ASR

```python
# Parakeet-CTC-0.6B streaming via NeMo
from nemo.collections.asr.models import EncDecCTCModelBPE
asr = EncDecCTCModelBPE.from_pretrained("nvidia/parakeet-ctc-0.6b")
# chunk_ms=320 ms, look_ahead_ms=80 ms
for chunk in audio_stream():
    partial_text = asr.transcribe_streaming(chunk)
    print(partial_text, end="\r")
```

### Bước 4: xử lý gián đoạn

```python
class Dialog:
    def __init__(self):
        self.tts_task = None

    def on_user_speech(self, frame):
        if self.tts_task and not self.tts_task.done():
            self.tts_task.cancel()   # barge-in
        # then feed to streaming ASR

    def on_final_user_utterance(self, text):
        self.tts_task = asyncio.create_task(self.reply(text))

    async def reply(self, text):
        async for tts_chunk in llm_then_tts(text):
            speaker.write(tts_chunk)
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


Hinges trên I / O async và phát TTS hủy bỏ. WebRTC peerconnection.stop() trên các bài hát âm thanh là cách truyền thống.

> Tùy thuộc vào các bước khác nhau I/O 和可取消的 TTS 流式传输──WebRTC's peerconnection.stop() 停止音频轨道是标准方式──




> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

Số 2026:

| Layer | Pick |
|-------|------|
| Transport | LiveKit (WebRTC) or Pion (Go) |
| VAD | Silero VAD 4.0 |
| Streaming ASR | Parakeet-CTC-0.6B or Whisper-Streaming |
| LLM first-token | Groq, Cerebras, vLLM-streaming |
| Streaming TTS | Kokoro or ElevenLabs Turbo v2.5 |
| Echo cancel | WebRTC AEC3 |
| End-to-end native | OpenAI Realtime API or Moshi |

| 层 | 选择 |
|----|------|
| 传输 | LiveKit（WebRTC）或 Pion（Go） |
| VAD | Silero VAD 4.0 |
| 流式 ASR | Parakeet-CTC-0.6B 或 Whisper-Streaming |
| LLM 首 token | Groq、Cerebras、vLLM-streaming |
| 流式 TTS | Kokoro 或 ElevenLabs Turbo v2.5 |
| 回声消除 | WebRTC AEC3 |
| 端到端原生 | OpenAI Realtime API 或 Moshi |



## Những bẫy

> 常见陷

- **Buffering 500 ms to be safe.**Buffer là tầng độ trễ của bạn.
  **缓冲 500 ms 求安全。**缓冲区*就是*你的延迟下限──缩小它──
- **Not pinning threads.**Phục hồi âm thanh trên một chuỗi ưu tiên thấp hơn UI = lỗi dưới tải.
  **没有绑定线程。**音频回调 低于 UI 优先线程上 = 负载出现故障──
- **TTS chunks too small.**Các mảnh dưới 200 ms làm cho các vật thể vocoder được nghe thấy. 320 ms là điểm ngọt ngào.
  **TTS 块太小。**Các khối dưới 200 ms làm cho bộ máy mã âm thanh giả hình có thể nghe được. 320 ms là điểm cân bằng tốt nhất.
- **No jitter buffer.**Các mạng lưới thực sự là căng thẳng; mà không làm trơn, bạn có thể bị bùng nổ.
  **没有抖动缓冲。**Thực tế mạng có động lực; không có sự bình thường sẽ xuất hiện.
- **Single-shot error handling.**Các ống dẫn âm thanh phải không bị tai nạn.
  **单次错误处理。**音频流水线必须抗崩──一个异常就杀死会话──

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-realtime-designer.md`Thiết kế một đường ống âm thanh thời gian thực với ngân sách độ trễ cụ thể cho mỗi giai đoạn.

> 保存为 `outputs/skill-realtime-designer.md`❖ thiết kế từng giai đoạn có dự kiến dự kiến thực tế

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`. Mô phỏng một bộ đệm vòng + năng lượng VAD; in độ trễ giai đoạn cho một dòng 10 giây giả.
   **简单。**运行 `code/main.py`❖模拟环形缓冲区 + 能量 VAD;印假 10 秒流的各阶段延迟──
2. **Medium.**Sử dụng `sounddevice`, xây dựng một vòng lặp qua mà xử lý micro của bạn trong 20 ms khung hình và in trạng thái VAD tại mỗi khung hình.
   **中等。**Sử dụng `sounddevice`Xây dựng vòng quay đường thẳng, xử lý máy trong 20 ms và in mỗi ngày trong trạng thái VAD.
3. **Hard.**Xây dựng một thử nghiệm echo duplex đầy đủ với `aiortc`: browser → WebRTC → Python → WebRTC → browser. đo độ trễ kính-vàng với xung 1 kHz.
   **困难。**用 `aiortc`构建全双工回声测试:浏览器 → WebRTC → Python → WebRTC → 浏览器──用 1 kHz 脉冲测量端到端延迟──

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Ring buffer | The circular queue | Fixed-size, lock-free (or SPSC-locked) FIFO for audio frames. |
| VAD | Silence gate | Model or heuristic marking speech vs non-speech. |
| Streaming ASR | Real-time STT | Emits partial text as audio arrives; bounded lookahead. |
| Jitter buffer | Network smoother | Queue reordering out-of-order packets; 60–80 ms typical. |
| AEC | Echo cancellation | Subtracts speaker-to-mic feedback path. |
| Barge-in | User interrupt | System detects user speech mid-TTS; must cancel playback. |
| Full duplex | Simultaneous both ways | User and bot can talk at the same time; Moshi is full duplex. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 环形缓冲 | 那个循环队列 | 固定大小、无锁（或 SPSC 锁）的音频帧 FIFO。 |
| VAD | 静音门 | 标记语音 vs 非语音的模型或启发式。 |
| 流式 ASR | 实时 STT | 随音频到达输出部分文本；有限前瞻。 |
| 抖动缓冲 | 网络平滑器 | 重排乱序包的队列；典型 60-80 ms。 |
| AEC | 回声消除 | 减去扬声器到麦克风的反馈路径。 |
| 抢话 | 用户打断 | 系统在 TTS 播放中检测用户语音；必须取消播放。 |
| 全双工 | 双向同时 | 用户和机器人可以同时说话；Moshi 是全双工。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Macháček et al. (2023). Whisper-Streaming](https://arxiv.org/abs/2307.14743) Chúc rắc gần như đang phát sóng.
  Macháček 等 (2023). Whisper-Streaming分块近流式 Whisper。
- [Kyutai (2024). Moshi](https://kyutai.org/Moshi.pdf) Full duplex 200 ms latency.
  Kyutai (2024). Moshi全双工 200 ms 延迟──
- [LiveKit Agents framework (2024)](https://docs.livekit.io/agents/) sản xuất âm thanh đại lý dàn nhạc.
  LiveKit Agents 框架(2024) 生产级音频智能体编排──
- [Silero VAD repo](https://github.com/snakers4/silero-vad) Sub-1 ms VAD, Apache 2.0.
  Silero VAD 仓库 亚毫秒 VAD,Apache 2.0
- [WebRTC AEC3 paper](https://webrtc.googlesource.com/src/+/main/modules/audio_processing/aec3/) Pháo âm thanh trong mã nguồn mở.
  WebRTC AEC3 论文开源回声消除──

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

