# Khám phá hoạt động giọng nói & quay  Silero, Cobra, và Trận thuật Flush 语音活动检测与轮次切换

> Mỗi đại lý giọng nói sống hoặc chết dựa trên hai quyết định: người dùng đang nói và họ đã hoàn thành chưa? VAD trả lời câu đầu tiên. Khám phá quay (VAD + âm thầm-hành động + mô hình điểm cuối ngữ nghĩa) trả lời câu thứ hai.

> **【中文解读】**Thành công của mỗi trợ lý tiếng nói phụ thuộc vào hai phán quyết: người dùng hiện đang đang nói chuyện? người dùng nói xong chưa? VAD(chuyến thăm hoạt động tiếng nói) trả lời thứ nhất, lần lượt kiểm tra(VAD+静音持续+语义终点模型) trả lời thứ hai。 bất cứ một lỗi nào, trợ lý hoặc cắt user, hoặc mãi mãi không mở cửa。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 11 (Real-Time Audio), Phase 6 · 12 (Voice Assistant) | **前置知识:** 阶段 6 · 11（实时音频），阶段 6 · 12（语音助手）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Ba quyết định khác nhau mà một đại lý giọng nói đưa ra cho mỗi 20 ms:

> 语音助手 cần phải đưa ra ba quyết định khác nhau trên mỗi 20 ms của khối âm thanh:

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.


1. **Is this frame speech?**VAD, nhị phân, mỗi khung hình.
   Trung ngữ翻译:这个是语音吗?
2. **Has the user started a new utterance?** phát hiện sự khởi phát.
   Trung ngữ翻译:用户开始了一个新的发言吗?
3. **Has the user finished?** hướng cuối (turn-end).
   Trung文翻译:用户说完了吗?端点检测(轮次结束)

Câu trả lời ngây thơ (giới hạn năng lượng) thất bại trong bất kỳ tiếng  giao thông, bàn phím, tiếng đùa đám đông. Câu trả lời 2026: Silero VAD (cởi mở, học sâu) + mô hình phát hiện lượt (số kết thúc ngữ nghĩa) + một cơn sưng lặng được định đo VAD.

> 朴素的答案(能量值) 在任何噪音环境下都会失败交通声、键盘声、人群杂声。2026 年的答案是:Silero VAD(开源、深度学习) + 轮次检测模型(语义端点检测) + VAD 校准的静音持续等──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![VAD cascade: energy → Silero → turn-detector → flush trick](../assets/vad-turn-taking.svg)

### Các 3 cấp VAD Cascade

> 三级 VAD 级联架构

**Tier 1: energy gate.**Giá rẻ nhất, RMS ở -40 dBFS, lọc âm thầm rõ ràng nhưng bắn vào bất kỳ tiếng ồn nào trên ngưỡng.

> **第一层：能量门控。**Phương pháp rẻ nhất: RMS  giá trị được đặt là -40 dBFS.

**Tier 2: Silero VAD**(2020-2026, MIT). 1M tham số. Được đào tạo trên 6000 + ngôn ngữ. chạy trong ~ 1 ms cho mỗi 30 ms phần trên một chuỗi CPU duy nhất. 87,7% TPR tại 5% FPR.

> **第二层：Silero VAD**(2020-2026, MIT 许可) ・100.000参数── trên 6000+ 种语言 trên đào tạo── trên mỗi 30 ms khối trên một CPU 线程

**Tier 3: semantic turn detector.**Mô hình phát hiện lượt của LiveKit (2024-2026) hoặc phân loại nhỏ của riêng bạn. Hóa ra sự khác biệt giữa "phát ngơi giữa câu" và "sự nói xong".

> **第三层：语义轮次检测器。**LiveKit's round-review model(2024-2026) hoặc tự định nghĩa小分类器──区分"句子中间的停顿"和"说完了"──使用语言上下文(语调 + 近期词汇),而不仅仅是静音──

### Các tham số chính và các mặc định của chúng

> 关键参数 và giá trị默认

- **Threshold.**Silero đưa ra một xác suất; phân loại bài phát biểu ở &gt; 0.5 (phụ mặc định) hoặc &gt; 0.3 (cảm xúc). ngưỡng thấp hơn = ít clip từ đầu tiên, nhiều tích cực sai hơn.
  Trung ngữ翻译:**阈值。**Silero 输出概率值;以 > 0.5(默认) hoặc > 0.3(敏感模式) 分类语音──值越低 = 首词截断越少,但误报越多──
- **Minimum speech duration.**Tháo lời ngắn hơn 250 ms  thường ho hoặc tiếng ồn ghế.
  Trung ngữ翻译:**最小语音时长。**拒绝短于250 ms 的语音通常是咳或椅子噪音──
- **Silence hangover (end-pointing).**Sau khi VAD trở lại 0, chờ 500-800 ms trước khi tuyên bố kết thúc lượt.
  Trung ngữ翻译:**静音持续等待（端点检测）。**VAD quay lại 0 后, chờ 500-800 ms tái tuyên bố kết thúc vòng tiếp theo.
- **Pre-roll buffer.**Giữ 300-500 ms âm thanh trước khi VAD phát nổ.
  Trung ngữ翻译:**预滚缓冲。**Trong VAD 触发前保留 300-500 ms 音频──防止""字被截断──

### Tránh lội (Kyutai 2025)

Các mô hình STT phát trực tuyến có độ chậm nhìn về phía trước (500 ms cho Kyutai STT-1B, 2,5 s cho STT-2.6B).**send a flush signal to the STT**STT xử lý ở thời gian thực 4x, do đó bộ đệm 500 ms hoàn thành trong ~ 125 ms.

> 流式 STT 模型有前视延迟(Kyutai STT-1B 为 500 ms,STT-2.6B 为 2.5 s)  Thông thường bạn cần phải chờ lâu sau khi kết thúc âm thanh để có được kết quả chuyển âm.**向 STT 发送刷新信号**, bắt buộc ngay lập tức xuất khẩu;.STT với khoảng 4 lần tốc độ xử lý thực tế, vì vậy 500 ms 缓冲区 trong khoảng 125 ms hoàn thành;;

End-to-end: 125 ms VAD + flush STT = thời gian trễ cuộc trò chuyện.

> 端到端:125 ms VAD + 刷新 STT = đối thoại cấp độ chậm.

### So sánh VAD 2026

> 2026 năm VAD đối với

| VAD | TPR @ 5% FPR | Latency | License |
|-----|--------------|---------|---------|
| WebRTC VAD (Google, 2013) | 50.0% | 30 ms | BSD |
| Silero VAD (2020-2026) | 87.7% | ~1 ms | MIT |
| Cobra VAD (Picovoice) | 98.9% | ~1 ms | commercial |
| pyannote segmentation | 95% | ~10 ms | MIT-ish |

Silero là mặc định đúng. Cobra là nâng cấp tuân thủ / độ chính xác. VAD chỉ sử dụng năng lượng không có chỗ trong sản xuất năm 2026.

> Silero là một lựa chọn cố định chính xác. Cobra là một lựa chọn nâng cấp hợp pháp/ chính xác.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.

> **【拓展：语音隐私与安全】**语音数据 chứa rất nhiều thông tin cá nhân riêng tư (音纹、对话内容) ◦深度伪造 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术) 语音技术 (反欺诈) 语音技术 (反欺诈) 防伪 (反伪造) 防伪研究热点) 热点





## Hãy xây dựng nó.
```figure
sp-vad-cascade
```

## Hãy xây dựng nó

### Bước 1: cổng năng lượng

> Bước 1: năng lượng kiểm soát

```python
def energy_vad(chunk, threshold_dbfs=-40.0):
    rms = (sum(x * x for x in chunk) / len(chunk)) ** 0.5
    dbfs = 20.0 * math.log10(max(rms, 1e-10))
    return dbfs > threshold_dbfs
```

### Bước 2: Silero VAD trong Python

> 步骤 2: sử dụng Silero VAD trong Python

```python
from silero_vad import load_silero_vad, get_speech_timestamps

vad = load_silero_vad()
audio = torch.tensor(waveform_16k, dtype=torch.float32)
segments = get_speech_timestamps(
    audio, vad, sampling_rate=16000,
    threshold=0.5,
    min_speech_duration_ms=250,
    min_silence_duration_ms=500,
    speech_pad_ms=300,
)
for s in segments:
    print(f"{s['start']/16000:.2f}s - {s['end']/16000:.2f}s")
```

### Bước 3: Máy chế độ quay cuối

> 步骤 3: vòng kết thúc trạng thái

```python
class TurnDetector:
    def __init__(self, silence_hangover_ms=500, min_speech_ms=250):
        self.state = "idle"
        self.speech_ms = 0
        self.silence_ms = 0
        self.silence_hangover_ms = silence_hangover_ms
        self.min_speech_ms = min_speech_ms

    def update(self, is_speech, chunk_ms=20):
        if is_speech:
            self.speech_ms += chunk_ms
            self.silence_ms = 0
            if self.state == "idle" and self.speech_ms >= self.min_speech_ms:
                self.state = "speaking"
                return "START"
        else:
            self.silence_ms += chunk_ms
            if self.state == "speaking" and self.silence_ms >= self.silence_hangover_ms:
                self.state = "idle"
                self.speech_ms = 0
                return "END"
        return None
```

### Bước 4: bộ xương trò chơi lồng

> 步骤 4:刷新技巧框架代码

```python
def flush_on_end(stt_client, audio_buffer):
    stt_client.send_audio(audio_buffer)
    stt_client.send_flush()
    return stt_client.recv_transcript(timeout_ms=150)
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


STT (Kyutai, Deepgram, AssemblyAI) phải hỗ trợ flush để điều này hoạt động.

> STT(Kyutai、Deepgram、AssemblyAI) phải hỗ trợ flush để thực hiện kỹ thuật này.




> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

| Situation | VAD choice |
|-----------|-----------|
| Open, fast, general / 开源、快速、通用 | Silero VAD |
| Commercial call center / 商业呼叫中心 | Cobra VAD |
| On-device (phone) / 端侧（手机） | Silero VAD ONNX |
| Research / diarization / 研究/说话人日志 | pyannote segmentation |
| Zero-dependency fallback / 零依赖后备方案 | WebRTC VAD（传统） |
| Need turn-ending quality / 需要轮次结束质量 | Silero + LiveKit 轮次检测器分层 |

Quy tắc: không bao giờ vận chuyển VAD chỉ sử dụng năng lượng trừ khi bạn thực sự không có lựa chọn khác.

> 经验法则: trừ khi thực sự không có lựa chọn khác, nếu không thì đừng bao giờ lên mạng chỉ dựa trên năng lượng VAD。



## Những bẫy

> 常见陷

- **Fixed threshold.**Nó hoạt động trong âm thanh, thất bại trong tiếng ồn.
  Trung ngữ翻译:**固定阈值。**Trong môi trường yên tĩnh, hiệu quả, 杂环境下失败.
- **Too-short silence hangover.**Cảnh sát ngắt lời giữa câu. 500-800 ms là điểm thích hợp cho cuộc trò chuyện.
  Trung ngữ翻译:**静音持续等待过短。**助手在句子中打断用户──500-800 ms là phạm vi tốt nhất của thoại语音──
- **Too-long hangover.**Cảm thấy chậm chạp.
  Trung ngữ翻译:**静音持续等待过长。**感觉迟──与目标用户进行A/B 测试──
- **No pre-roll buffer.**200-300 ms đầu tiên của âm thanh người dùng bị mất.
  Trung ngữ翻译:**没有预滚缓冲。**Người dùng âm thanh của trước 200-300 ms 丢失──始终保持滚动预滚缓冲──
- **Ignoring semantic endpointing.**"Hmm, để tôi nghĩ"... chứa những khoảng thời gian dừng lại dài người dùng ghét bị cắt đứt trong lúc suy nghĩ.
  Trung ngữ翻译:**忽略语义端点检测。**",让我想想......" chứa một thời gian dừng lại. Người dùng thích bị gián đoạn trong quá trình suy nghĩ.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-vad-tuner.md`Chọn mô hình VAD, ngưỡng, ngứa, chiến lược phát hiện và phát hiện vòng cho một khối lượng công việc.

> 保存为 `outputs/skill-vad-tuner.md`❖ Cho một workload chọn VAD 模型、值、静音持续等待、预滚缓冲和轮次检测策略──

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`Nó mô phỏng một chuỗi nói + im lặng + nói + ho và kiểm tra ba cấp độ VAD.
   Trung ngữ翻译:**简单。**运行 `code/main.py`∼It模拟一段语音 + 静音 + 语音 + 咳的序列,并测试三层 VAD──
2. **Medium.**Thiết lập `silero-vad`, xử lý một ghi âm 5 phút, điều chỉnh ngưỡng để giảm thiểu cả hai clip từ đầu tiên và kích hoạt sai.
   Trung ngữ翻译:**中等。**                                          `silero-vad`, xử lý một đoạn 5 phút thu âm, điều chỉnh giá trị để tối thiểu hóa đầu từ cắt và lỗi cảm xúc.
3. **Hard.**Xây dựng một bộ phát hiện vòng mini: Silero VAD + một MLP 3 tầng trên 10 từ cuối cùng ( Sử dụng các bộ chuyển đổi câu). Đào tạo trên một tập dữ liệu vòng cuối được dán nhãn bằng tay.
   Trung ngữ翻译:**困难。**Xây dựng một máy kiểm tra vòng nhỏ: Silero VAD + dựa trên 10 个近词嵌入的 3层 MLP( sử dụng các máy biến câu) ⋅ trong vòng kết thúc tập dữ liệu của thẻ tay ⋅ Than Pure Silero 方案 F1 高 10%。

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| VAD | Voice detector | Binary per-frame: is this speech? / 逐帧二分类：这是语音吗？ |
| Turn detection | End-pointing | VAD + silence-hangover + semantic endpoint. / VAD + 静音持续 + 语义端点 |
| Silence hangover | Wait-after-speech | Time to wait before declaring turn end; 500-800 ms. / 宣布轮次结束前的等待时间；500-800 ms |
| Pre-roll | Pre-speech buffer | Keep 300-500 ms audio before VAD fires. / 在 VAD 触发前保留 300-500 ms 音频 |
| Flush trick | Kyutai hack | VAD → flush-STT → 125 ms instead of 500 ms delay. / VAD → 刷新 STT → 125 ms 而非 500 ms 延迟 |
| Semantic endpoint | "Did they mean to stop?" | ML classifier that looks at words, not just silence. / 看词汇而非仅看静音的 ML 分类器 |
| TPR @ FPR 5% | ROC point | Standard VAD benchmark; 87.7% for Silero, 50% WebRTC. / 标准 VAD 基准；Silero 87.7%，WebRTC 50% |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Silero VAD](https://github.com/snakers4/silero-vad) VAD mở tham chiếu.
  Silero VAD                                                                                                                                                                                                                                                             
- [Picovoice Cobra VAD](https://picovoice.ai/products/cobra/) nhà lãnh đạo chính xác thương mại.
  Picovoice Cobra VAD thương mại tinh tế dẫn đầu.
- [Kyutai — Unmute + flush trick](https://kyutai.org/stt) thủ thuật kỹ thuật sub-200 ms.
  KyutaiUnmute + 刷新技巧亚 200 ms 的工程技巧──
- [LiveKit — turn detection](https://docs.livekit.io/agents/logic/turns/) chỉ ra kết thúc ngữ nghĩa trong sản xuất.
  LiveKit轮次检测生产中的语义端点检测
- [WebRTC VAD](https://webrtc.googlesource.com/src/) dòng cơ sở thừa kế.
  WebRTC VAD truyền thống基线。
- [pyannote segmentation](https://github.com/pyannote/pyannote-audio) phân đoạn cấp nhật ký.
  chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia chia

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

