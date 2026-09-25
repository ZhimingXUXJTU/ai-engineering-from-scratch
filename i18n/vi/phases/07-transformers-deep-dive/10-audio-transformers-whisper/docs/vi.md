# Transformer âm thanh  Phầm kiến trúc 音频 Transformer  Phầm kiến trúc

> Âm thanh là hình ảnh tần số theo thời gian. Whisper là một ViT ăn nhiều quang phổ và nói lại.

> **【中文解读】**Whisper Using Transformer 做语音识别和翻译──理解音频如何变成符号序列送进 Transformer──

**Type:** Study | **类型:** 学习
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 08 (Encoder-Decoder), Phase 7 · 09 (ViT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Trước khi Whisper (OpenAI, Radford et al. 2022), nhận dạng giọng nói tự động tiên tiến (ASR) có nghĩa là wav2vec 2.0 và HuBERT  máy thu thập tính tự giám sát cộng với một đầu điều chỉnh tinh tế.

> Trước đó, các công nghệ nhận dạng tiếng Anh tự động tiên tiến nhất của ASR (ASR) sử dụng wav2vec 2.0 và HuBERT (Huawei) đã sử dụng các thiết bị nhận dạng tiếng Anh tự giám sát.

Whisper đã đặt cược ba lần:

> Whisper đã làm ba điều:

1. **Train on everything.**680.000 giờ âm thanh có nhãn yếu được thu thập từ internet trong 97 ngôn ngữ, không có tập hợp học thuật sạch, không có nhãn âm thanh.
   Trung ngữ翻译:**用一切数据训练。**680.000 giờ qua từ Internet, bao gồm 97 ngôn ngữ.
2. **Multi-task single model.**Một bộ giải mã được đào tạo chung về bản sao chép, dịch, phát hiện hoạt động giọng nói, nhận dạng ngôn ngữ và dấu thời gian thông qua các mã công việc.
   Trung ngữ翻译:**单模型多任务。**Một giải mã thông qua mã lệnh 联合训练转录、翻译、语音活动检测、语言识别和时间──
3. **Standard encoder-decoder transformer.**Các mã hóa sử dụng các quang phổ log-mail. Các mã hóa phát hành mã thông báo văn bản tự động. Không vocoder, không CTC, không HMM.
   Trung ngữ翻译:**标准编码器-解码器 Transformer。**编码器消费 log-mail 频谱图──解码器 tự quay trở lại tạo mã hóa văn bản──没有声码器,没有CTC,没有HMM──

Kết quả: Whisper large-v3 là mạnh mẽ trên các giọng, tiếng ồn và ngôn ngữ có dữ liệu có nhãn sạch không. Nó là đầu tiên mặc định của giọng nói cho mọi trợ lý giọng nói nguồn mở và hầu hết các ngôn ngữ thương mại vào năm 2026.

> Kết quả:Whisper large-v3 đối với tiếng nói, tiếng ồn và dữ liệu không có dấu hiệu đều có tính chất 鲁棒性. Nó là đầu tiên của mỗi trợ lý tiếng mở và hầu hết các trợ lý tiếng thương mại năm 2026

> **【中文解读】**Whisper's Three Big Innovations: 1) dùng 680.000小时弱标注音频训练,覆盖 97 种语言; 2) đơn模型多任务(转录、翻译、语种识别、时间); 3) 标准编码器-解码器 Transformer 架。音频被转构为 log-mail 频谱图图(类似图像),编码器处理频谱特征,解码器生成文本。

## Khái niệm cốt lõi

![Whisper pipeline: audio → mel → encoder → decoder → text](../assets/whisper.svg)

### Bước 1  mẫu lại + cửa sổ

Audio ở 16 kHz. Clip/pad đến 30 giây. tính toán log-mel spectrogram: 80 mel bin, 10 ms bước → ~ 3.000 khung hình × 80 tính năng. Đây là "hình ảnh đầu vào" mà Whisper nhìn thấy.

> 音频采样率 16 kHz──剪切/填充到30秒──计算日志频谱图:80 个梅尔频率bin,10 ms 步长 → 约 3,000  × 80特征──这是Whisper 看到的"输入图像"──

### Bước 2  thân lưng

Hai lớp Conv1D với hạt nhân 3 và bước 2 làm giảm 3.000 khung hình thành 1.500.

> 两层 Conv1D(核大小 3,步长 2) sẽ giảm 3.000  xuống còn 1.500 .

> **【拓展：Whisper 的多语言能力来源】**Whisper trong 97 种语言,680 万小时音频上训练, khả năng đa ngôn ngữ xuất phát từ hai yếu tố: 1) 超大规模的弱标注数据覆盖绝大多数语言; 2) 统一的BPE 词表是GPT-2 词表的超集,天然支持多语言――decoder prompt 中的语言代码如`<|zh|>`) kiểm soát các ngôn ngữ xuất, để mô hình tương tự có thể thực hiện các nhiệm vụ chuyển tải hoặc dịch.

### Bước 3  mã hóa

Một bộ mã hóa biến thể 24 tầng (đối với lớn) trên 1.500 bước thời gian. mã hóa vị trí sinus, tự chú ý, GELU FFN. Tạo ra 1.500 × 1.280 trạng thái ẩn.

> Một 24 tầng(lớn  phiên bản)Transformer 编码器 xử lý 1.500 个时间步──正弦位置编码、自注意力、GELU FFN── tạo ra 1.500 × 1.280 trạng thái ẩn──

### Bước 4  decoder

Một decoder biến đổi 24 lớp. Nó tự lập tạo ra các token từ một từ vựng BPE là một bộ siêu của GPT-2 với một vài token đặc biệt cụ thể.

> Một 24 tầng Transformer 解码器──自归地从 BPE 词表生成代币,该词表是GPT-2 词表的超集,外加几个音频专用特殊代币──

### Bước 5  mã công việc

Việc giải mã bắt đầu với các mã kiểm soát cho mô hình biết phải làm gì:

> Để kiểm soát token, hãy nói với mô hình phải làm gì:

```
<|startoftranscript|>  <|en|>  <|transcribe|>  <|0.00|>
```

hoặc

```
<|startoftranscript|>  <|fr|>  <|translate|>   <|0.00|>
```

Mô hình được đào tạo theo hội nghị này. Bạn kiểm soát nhiệm vụ bằng tiền tố. tương đương với điều chỉnh hướng dẫn năm 2026, nhưng áp dụng cho ngôn ngữ.

> 模型按这种约定训练──你通过前控制任务──这是指令微调在语音领域的等价──

> **【中文解读】**Cơ chế kiểm soát nhiệm vụ của Whisper rất tốt: thông qua trong giải mã trước trong thêm mã đặc biệt như`<|transcribe|>`Hoặc`<|translate|>`(được gọi là " chỉ dẫn nhỏ" trong lĩnh vực ngữ pháp.

> **【拓展：Whisper 在语音助手中的应用】**Whisper là một thành phần cơ bản của AI ngôn ngữ năm 2026 ⋅ từ trợ lý ngôn ngữ thực tế đến video幕 tạo,再到多语言会议翻译, Whisper 提供统一的语音前端, Whisper-turbo (tạm dịch: "hỗ trợ ngôn ngữ") sẽ chậm lại giảm 8 lần, làm cho cuộc hội thoại thực tế trở nên có thể, kết hợp với cuối của LLM, hình thành cấu trúc trợ lý ngôn ngữ hiện đại của "Whisper + LLM + TTS".

### Bước 6  đầu ra

Tìm kiếm chùm (thiều rộng 5) với ngưỡng log-prob.`<|notimestamps|>`token bị vắng mặt.

> 束搜索(宽度 5)加对数概率值──当没有 `<|notimestamps|>`Địa chỉ 时, mỗi 0.02 秒预测 một lần ──

### Kích thước thì thầm

| Model | Params | Layers | d_model | Heads | VRAM (fp16) |
|-------|--------|--------|---------|-------|-------------|
| 模型 | 参数量 | 层数 | d_model | 头数 | 显存 (fp16) |
| Tiny | 39M | 4 | 384 | 6 | ~1 GB |
| Base | 74M | 6 | 512 | 8 | ~1 GB |
| Small | 244M | 12 | 768 | 12 | ~2 GB |
| Medium | 769M | 24 | 1024 | 16 | ~5 GB |
| Large | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3 | 1550M | 32 | 1280 | 20 | ~10 GB |
| Large-v3-turbo | 809M | 32 | 1280 | 20 | ~6 GB (4-layer decoder) |

Large-v3-turbo (2024) cắt giảm bộ giải mã từ 32 lớp xuống 4.8x nhanh hơn với sự lùi điểm <1 WER.

> Large-v3-turbo(2024) sẽ giảm tốc độ giải mã từ 32 tầng xuống còn 4 tầng.

> **【拓展：音频 Transformer 的统一趋势】**语音识别(Whisper)、语音合成(VALL-E, Kokoro)、音乐生成(MusicGen) 都在转向 Transformer 架构──核心思路相同:将音频转换为频谱图或离散代币序列,然后使用标准 Transformer 处理──这验证了 Transformer 作为通用序列建模器的地位──

### Những gì Whisper không làm

- Không có nhật ký (người đang nói) kết hợp với ghi chú phấn cho điều đó.
  Trung文翻译:没有说话人分离(谁在说话) ⋅需要搭配 ⋅ 使用.
- Không có luồng trực tuyến thời gian thực bản địa  cửa sổ 30 giây được cố định.`faster-whisper`- `WhisperX`) điện thoại thông minh trên VAD + chồng chéo.
  Trung ngữ翻译:没有原生实时流式处理30秒窗口是固定的──现代封装器(`faster-whisper``WhisperX`) Thông qua VAD + 重叠实现流式处理。
- Không có ngữ cảnh hình thức dài hơn 30 s mà không có sự phân mảnh bên ngoài.
  Trung ngữ翻译:没有外部分块则不支持30秒以上长格式上下文── thực tế hiệu quả tốt, vì người dùng rất ít cần khoảng cách dài trên下文──

### 2026 phong cảnh

| Task | Model | Notes |
|------|-------|-------|
| 任务 | 模型 | 备注 |
| English ASR | Whisper-turbo, Moonshine | Moonshine is 4× faster on edge |
| 英语 ASR | Whisper-turbo, Moonshine | Moonshine 在边缘设备上快 4 倍 |
| Multilingual ASR | Whisper-large-v3 | 97 languages |
| 多语言 ASR | Whisper-large-v3 | 97 种语言 |
| Streaming ASR | faster-whisper + VAD | 150 ms latency targets achievable |
| 流式 ASR | faster-whisper + VAD | 可实现 150ms 延迟目标 |
| TTS | Piper, XTTS-v2, Kokoro | Encoder-decoder pattern, but Whisper-shaped |
| TTS | Piper, XTTS-v2, Kokoro | 编码器-解码器模式，但类似 Whisper |
| Audio + language | AudioLM, SeamlessM4T | Text tokens + audio tokens in one transformer |
| 音频 + 语言 | AudioLM, SeamlessM4T | 文本 token + 音频 token 在一个 Transformer 中 |

## Hãy xây dựng nó.
```figure
n5-mel-decode
```

## Hãy xây dựng nó

Nhìn xem`code/main.py`Chúng tôi không đào tạo Whisper, chúng tôi xây dựng đường ống quang phổ log-mail + định dạng lệnh giao thức. Đó là những bộ phận bạn thực sự chạm vào trong sản xuất.

> 参见 `code/main.py` Chúng tôi không luyện tập ầmầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm ầm

### Bước 1: tổng hợp âm thanh

Tạo ra một sóng âm âm 1 giây ở 440 Hz lấy mẫu ở 16 kHz. 16.000 mẫu.

> Tạo ra một 1 giây 440 Hz, tỷ lệ chụp 16 kHz, 16.000 điểm chụp.

### Bước 2: Nhìn quang phổ log-mel (đơn giản hóa)

Phân quang phổ mel đầy đủ cần FFT. Chúng tôi làm một khung đơn giản + mỗi khung năng lượng phiên bản cho thấy đường ống mà không cần `librosa`- Có thể là:

> 完整的梅尔频谱图需要FFT──我们做一个简化分+逐能量版本,无需`librosa`即可展示管道:

```python
def frame_signal(x, frame_size=400, hop=160):
    frames = []
    for start in range(0, len(x) - frame_size + 1, hop):
        frames.append(x[start:start + frame_size])
    return frames
```

Frame = 25 ms, hop = 10 ms. Tương tự như Whisper's Windowing.

>  = 25 ms,步长 = 10 ms──与 Whisper 的窗口匹配──逐能量用于教学演示,替代梅尔频率 bin──

### Bước 3: Pad đến 30 s

Whisper luôn xử lý các mảnh 30 giây. Pad (hoặc clip) quang phổ đến 3.000 khung hình.

> Nhầm 总是 xử lý 30 giây của phân khối.

### Bước 4: xây dựng các mã thông báo nhanh

```python
def whisper_prompt(lang="en", task="transcribe", timestamps=True):
    tokens = ["<|startoftranscript|>", f"<|{lang}|>", f"<|{task}|>"]
    if not timestamps:
        tokens.append("<|notimestamps|>")
    return tokens
```

Đó là toàn bộ bề mặt kiểm soát nhiệm vụ.

> Đó là tất cả các nhiệm vụ kiểm soát giao tiếp.

## Hãy sử dụng nó để thực hiện

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("meeting.wav", language="en", task="transcribe")
print(result["text"])
print(result["segments"][0]["start"], result["segments"][0]["end"])
```

Tốc độ nhanh hơn, tương thích với OpenAI:

> Các giải pháp tương thích với OpenAI:

```python
from faster_whisper import WhisperModel
model = WhisperModel("large-v3-turbo", compute_type="int8_float16")
segments, info = model.transcribe("meeting.wav", vad_filter=True)
for s in segments:
    print(f"{s.start:.2f} - {s.end:.2f}: {s.text}")
```

**When to pick Whisper in 2026:**

> **2026 年何时选择 Whisper：**

- ASR đa ngôn ngữ với một mô hình.
  Trung文翻译:用一个模型做多语言 ASR。
- Bản sao âm thanh ồn ào, đa dạng.
  Trung文翻译:对噪音大、多样化的音频进行鲁棒转录──
- Nghiên cứu / nguyên mẫu ASR  điểm khởi đầu nhanh nhất.
  Trung文翻译:研究/原型 ASR最快的起点──

**When to pick something else:**

> **何时选择其他方案：**

- Tiếng lưu điện cực thấp trên cạnh  Moonshine đánh bại Whisper với chất lượng phù hợp.
  Trung ngữ翻译:边缘设备上的超低延迟流式处理月光在相同质量下比 语更快──
- AI trò chuyện thời gian thực cần <200 ms  chuyên dụng phát trực tuyến ASR.
  Trung ngữ翻译:需要 <200ms 的实时对话 AI专用流式 ASR。
- Đăng ký loa  Whisper không làm điều này; đệm trên pianonote.
  Trung文翻译:说话人分离Whisper 不做这个;需要加装钢琴笔记──

## Chuyển nó đi.

Nhìn xem`outputs/skill-asr-configurator.md`. Khả năng chọn một mô hình ASR, giải mã các tham số và đường ống xử lý trước cho một ứng dụng giọng nói mới.

> 参见 `outputs/skill-asr-configurator.md`◊ Kỹ năng này cho ứng dụng ngôn ngữ mới chọn ASR 模型、解码参数和预处理管道。

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`- Đảm nhận số khung hình cho một tín hiệu 1 giây ở 16 kHz với 10 ms hop là ~ 100 khung hình.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận 1 秒 tín hiệu ở 16 kHz、10 ms 步长下约100 ──30 秒:约3,000 ──
2. **Medium.**Xây dựng toàn bộ log-mel spectrogram sử dụng `numpy.fft`- Thêm 80 miếng nhựa .`librosa.feature.melspectrogram(n_mels=80)`trong lỗi số.
   中文翻译:用 `numpy.fft`构建完整的 log-mel 频谱图――验证 80 个梅尔频率bin 与 `librosa.feature.melspectrogram(n_mels=80)`Trong phạm vi số lượng sai lầm phù hợp.
3. **Hard.**Thực hiện suy luận phát trực tuyến: phần âm thanh vào cửa sổ 10 giây với sự chồng chéo 2 giây, chạy Whisper trên mỗi phần, kết hợp bản ghi chép. đo tỷ lệ lỗi từ so với một lần qua trên một mẫu podcast 5 phút.
   Trung ngữ翻译:实现流式推理:将音频分成10秒窗口(2秒重叠), trên mỗi cửa sổ chạy Xầm,合并转录──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Mel spectrogram | "Audio image" | 2D representation: frequency bins on one axis, time frames on the other; log-scaled energy per cell. |
| 梅尔频谱图 | "音频图像" | 2D 表示：一个轴是频率 bin，另一个是时间帧；每个单元是对数缩放的能量。 |
| Log-mel | "What Whisper sees" | Mel spectrogram passed through log; approximates human perception of loudness. |
| Log-mel | "Whisper 看到的" | 梅尔频谱图取对数；近似人类对响度的感知。 |
| Frame | "One time slice" | A 25 ms window of samples; overlapping at 10 ms stride. |
| 帧 | "一个时间切片" | 25 ms 的采样窗口；10 ms 步长重叠。 |
| Task token | "Prompt prefix for speech" | Special tokens like `<\|transcribe\|>` / `<\|translate\|>` in the decoder prompt. |
| 任务 token | "语音的提示前缀" | 解码器提示中的特殊 token，如 `<\|transcribe\|>` / `<\|translate\|>`。 |
| Voice activity detection (VAD) | "Find the speech" | Gate that removes silence before ASR; cuts cost massively. |
| 语音活动检测 (VAD) | "找到语音" | 在 ASR 之前去除静音的门控；大幅降低成本。 |
| CTC | "Connectionist Temporal Classification" | Classic ASR loss for alignment-free training; Whisper does NOT use it. |
| CTC | "连接主义时间分类" | 经典的 ASR 对齐无关训练损失；Whisper 不使用它。 |
| Whisper-turbo | "Small decoder, full encoder" | large-v3 encoder + 4-layer decoder; 8× faster decoding. |
| Whisper-turbo | "小解码器，全编码器" | large-v3 编码器 + 4 层解码器；解码速度提高 8 倍。 |
| Faster-whisper | "The production wrapper" | CTranslate2 reimplementation; int8 quantization; 4× faster than OpenAI's reference. |
| Faster-whisper | "生产封装器" | CTranslate2 重新实现；int8 量化；比 OpenAI 参考实现快 4 倍。 |

## Xem thêm 延伸阅读

- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) Bức giấy.
  Trung文翻译:Tầm thì thầm 论文。
- [OpenAI Whisper repo](https://github.com/openai/whisper) mã tham chiếu + trọng lượng mô hình.`whisper/model.py`để xem conv1D gốc + mã hóa + mã hóa từ trên xuống dưới trong ~ 400 dòng.
  Trung文翻译:OpenAI Whisper 代码仓库, khoảng 400 行代码展示 Conv1D stem + 编码器 + 解码器。
- [OpenAI Whisper — `whisper/decoding.py`](https://github.com/openai/whisper/blob/main/whisper/decoding.py) logic tìm kiếm chùm + mã công việc được mô tả trong Bước 56 ở đây; 500 dòng, hoàn toàn có thể đọc được.
  Trung文翻译:束搜索 + 任务代币 逻辑的实现,500 行代码,完全可读──
- [Baevski et al. (2020). wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://arxiv.org/abs/2006.11477) tiền thân; vẫn có tính năng SOTA trong một số cài đặt.
  Trung ngữ翻译:wav2vec 2.0 论文;Whisper 的前身,在某些场景下仍是SOTA特征──
- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) bọc sản xuất, nhanh hơn 4x so với tham chiếu.
  Trung文翻译:quá-phầm 生产封装器,比参考实现快4倍。
- [Jia et al. (2024). Moonshine: Speech Recognition for Live Transcription and Voice Commands](https://arxiv.org/abs/2410.15608) 2024 ASR thân thiện với cạnh, hình dạng Hầm nhưng nhỏ hơn.
  Trung文翻译:Moonshine 论文,2024 年面向边缘的ASR,类  sussur 但更小──
- [HuggingFace blog — "Fine-Tune Whisper For Multilingual ASR with 🤗 Transformers"](https://huggingface.co/blog/fine-tune-whisper) công thức điều chỉnh tinh tế theo quy luật bao gồm bộ xử lý trước của quang phổ mel và xử lý dấu thời gian token.
  Trung文翻译:HuggingFace Whisper 微调教程,包括梅尔频谱图预处理器和代币 时间处理──
- [HuggingFace `modeling_whisper.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/whisper/modeling_whisper.py) thực hiện đầy đủ (code, decoder, sự chú ý chéo, tạo ra) phản ánh sơ đồ kiến trúc của bài học.
  Trung文翻译:HuggingFace Whisper 完整实现(编码器、解码器、交叉注意力、生成),与课程架构图对应──
