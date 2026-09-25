# Audio Fundamentals  Phong hình sóng, lấy mẫu, Fourier Transform  音频基础  波形、采样与里叶变化

> Các dạng sóng là tín hiệu nguyên liệu. Các quang phổ là đại diện. Các tính năng Mel là dạng thân thiện với ML. Mỗi đường ống ASR và TTS hiện đại đi qua bậc thang này, và bước đầu tiên là hiểu lấy mẫu và Fourier.

> **【中文解读】**波形是原始信号,频谱图是表示形式,Mel特征是机器学习的友好的形式――每个现代语音识别(ASR) 和语音合成(TTS) hệ thống đều dọc theo thang này:波形 → 频谱图 → Mel特征──第一阶段就是理解采样和里叶变化──

> **【拓展：音频 AI 的基础】**采样率 (tương tự như 16kHz) quyết định tần suất cao nhất có thể được biểu thị (NEWS) 里叶变化将时域信号分解为频域成分──这些概念是Whisper、TTS、语音克隆等所有音频 AI的基础──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 1 · 06 (Vectors & Matrices), Phase 1 · 14 (Probability Distributions) | **前置知识:** 阶段 1 · 06（向量与矩阵），阶段 1 · 14（概率分布）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Một micrô tạo ra tín hiệu áp suất so với thời gian. Mạng thần kinh của bạn tiêu thụ các tensor. Giữa chúng nằm một loạt các quy tắc, khi bị vi phạm, tạo ra các lỗi im lặng: mô hình hoạt động tốt nhưng WER tăng gấp đôi, hoặc TTS gửi một tiếng ồn, hoặc một hệ thống nhân bản giọng nói ghi nhớ micro thay vì loa.

> 麦克风产生一个压力-时间信号――消耗你的神经网络是张量―― giữa hai thứ là một loạt các quy định trái ngược với các quy định này sẽ tạo ra lỗi ẩn: mô hình đào tạo bình thường nhưng WER 翻倍, hoặc TTS 输出声, hoặc语音克隆系统记住麦克风而不是说话人――

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Mỗi lỗi trong hệ thống ngôn ngữ đều có thể được tìm thấy từ một trong ba câu hỏi:

> Mỗi lỗi trong hệ thống tiếng nói đều có thể được tìm thấy trong ba vấn đề sau:

1. Dữ liệu được ghi lại ở mức độ mẫu nào, và mô hình mong đợi gì?
   Tỷ lệ lấy mẫu ghi dữ liệu là bao nhiêu, tỷ lệ lấy mẫu mô hình mong đợi là bao nhiêu?
2. tín hiệu có tên gọi không?
   信号 có sự lộn xộn không?
3. Bạn đang vận hành trên mẫu nguyên liệu hay trên một đại diện tần số?
   Bạn đang xử lý các điểm mẫu nguyên thủy hay thường xuyên biểu hiện?

Nếu làm đúng, phần còn lại của giai đoạn 6 sẽ dễ xử lý, nếu làm sai, thậm chí cả Whisper-Large-v4 cũng sẽ tạo ra rác.

> Làm cho những vấn đề này, phần còn lại của giai đoạn 6 dễ hiểu hơn.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Waveform, sampling, DFT, and frequency bins visualized](../assets/audio-fundamentals.svg)

**Waveform.**Một bộ sưu tập một chiều của các floats trong `[-1.0, 1.0]`Để chuyển đổi thành giây, chia bằng tỷ lệ mẫu:`t = n / sr`Một clip 10 giây ở 16 kHz là một dải 160.000 float.

> **波形（Waveform）。**Một giá trị được lấy trong `[-1.0, 1.0]`间的一个维浮点数组──以采样编为索引──应转换为秒数,除以采样率:`t = n / sr` 1段 10 giây 16 kHz 音频 là 160.000 个浮点数组

**Sampling rate (sr).**Số lượng mẫu mỗi giây.

> **采样率（sr）。**Số điểm lấy mẫu mỗi giây.

| Rate | Use |
|------|-----|
| 8 kHz | Telephony, legacy VOIP. Nyquist at 4 kHz kills consonants. Avoid for ASR. |
| 16 kHz | ASR standard. Whisper, Parakeet, SeamlessM4T v2 all consume 16 kHz. |
| 22.05 kHz | TTS vocoder training for older models. |
| 24 kHz | Modern TTS (Kokoro, F5-TTS, xTTS v2). |
| 44.1 kHz | CD audio, music. |
| 48 kHz | Film, pro audio, high-fidelity TTS (VALL-E 2, NaturalSpeech 3). |

| 采样率 | 用途 |
|--------|------|
| 8 kHz | 电话、传统 VOIP。奈奎斯特频率 4 kHz 会丢失辅音。ASR 应避免使用。 |
| 16 kHz | ASR 标准。Whisper、Parakeet、SeamlessM4T v2 均使用 16 kHz。 |
| 22.05 kHz | 旧模型 TTS 声码器训练。 |
| 24 kHz | 现代 TTS（Kokoro、F5-TTS、xTTS v2）。 |
| 44.1 kHz | CD 音质、音乐。 |
| 48 kHz | 电影、专业音频、高保真 TTS（VALL-E 2、NaturalSpeech 3）。 |

**Nyquist-Shannon.**Tỷ lệ mẫu của `sr`có thể thể đại diện một cách rõ ràng cho tần số lên đến `sr/2`- `sr/2`giới hạn là tần số Nyquist. năng lượng trên Nyquist được * aliased *  gấp xuống tần số thấp hơn  và làm hỏng tín hiệu.

> **奈奎斯特-香农定理。**采样率 `sr`Có thể không khác biệt nghĩa là cao nhất đến `sr/2`                                                                                                                                                                                                                                                              `sr/2`边界就是奈奎斯特频率 () . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

**Bit depth.**PCM 16-bit (được ký int16, phạm vi ±32,767) là định dạng trao đổi phổ biến.`soundfile`đọc int16 nhưng phơi bày float32 array trong `[-1, 1]`- Tôi không biết.

> **位深度。**16 位 PCM(有符号 int16, phạm vi ±32,767) là một hệ thống giao dịch thông thường.`soundfile`Đọc thêm 16 nhưng quay lại`[-1, 1]`范围的浮动32 数组──

**Fourier Transform.**Bất kỳ tín hiệu hữu hạn nào là tổng số các sinus ở tần số khác nhau.`N`mẫu, `N`Tỷ lệ liên quan phức tạp  một trong mỗi thùng tần số. `bin k`bản đồ tần số `k · sr / N`Hz. Tầm là độ dốc ở tần số đó, góc là pha.

> **傅里叶变换。**Bất kỳ tín hiệu nào có giới hạn có thể được phân chia thành các tần số khác nhau của các âm thanh.`N`个采样点计算 `N`个复数系数 mỗi tần số bin một.`bin k`đối với tần suất`k · sr / N`Hz── chiều rộng là chiều rộng của tần số này, góc là pha-bi-tơ──

**FFT.**Chuyển đổi Fourier nhanh: một `O(N log N)`thuật toán cho DFT khi `N`Mỗi thư viện âm thanh sử dụng FFT dưới nắp. một FFT mẫu 1024 ở 16 kHz cung cấp 512 thùng tần số có thể sử dụng trải dài 08 kHz ở độ phân giải 15,6 Hz.

> **FFT。**快速里叶变换:当 `N`Vì 2 时,DFT của `O(N log N)`算法── mỗi tầng âm thanh sử dụng FFT──16 kHz 下 1024 采样点的 FFT 产生 512 个可用频率bin,覆盖08 kHz,分辨率为15.6 Hz──

**Framing + window.**Chúng tôi không làm FFT toàn bộ clip. Chúng tôi cắt nó thành các khung chồng chéo (thường là 25 ms với 10 ms hop), nhân mỗi khung bằng một chức năng cửa sổ (Hann, Hamming) để loại bỏ sự gián đoạn cạnh, sau đó FFT mỗi khung. Đây là chuyển đổi Fourier thời gian ngắn (STFT). Bài học 02 bắt đầu từ đây.

> **分帧 + 加窗。**Chúng tôi không đối với toàn bộ đoạn âm thanh làm FFT. Thay vào đó, chúng tôi sẽ cắt thành các phần chồng lên.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.



## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
mel-scale
```

## Hãy xây dựng nó

### Bước 1: đọc một clip và vẽ hình dạng sóng

`code/main.py`chỉ sử dụng stdlib `wave`module để giữ cho demo miễn phí phụ thuộc.`soundfile`hoặc `torchaudio.load`(cả hai đều trở lại `(waveform, sr)`(Tuples):

> `code/main.py` chỉ sử dụng tiêu chuẩn `wave`模块 để giữ cho biểu diễn không phụ thuộc.`soundfile`Hoặc`torchaudio.load`(两者都回归 `(waveform, sr)`元组:

```python
import soundfile as sf
waveform, sr = sf.read("clip.wav", dtype="float32")  # shape (T,), sr=int
```

### Bước 2: tổng hợp một sóng âm từ các nguyên tắc đầu tiên

```python
import math

def sine(freq_hz, sr, seconds, amp=0.5):
    n = int(sr * seconds)
    return [amp * math.sin(2 * math.pi * freq_hz * i / sr) for i in range(n)]
```

Một âm đạo 440 Hz (công nhạc A) ở 16 kHz trong 1 giây là 16.000 float.`wave.open(..., "wb")`sử dụng mã hóa PCM 16-bit.

> 16 kHz 采样率下 440 Hz 正弦波(标准音 A) kéo dài 1 秒 là 16.000 个浮点数――使用 `wave.open(..., "wb")`以 16 位 PCM 编码写入──

### Bước 3: tính toán DFT bằng tay

```python
def dft(x):
    N = len(x)
    out = []
    for k in range(N):
        re = sum(x[n] * math.cos(-2 * math.pi * k * n / N) for n in range(N))
        im = sum(x[n] * math.sin(-2 * math.pi * k * n / N) for n in range(N))
        out.append((re, im))
    return out
```

`O(N²)` tốt cho `N=256`để xác nhận sự chính xác, vô dụng cho âm thanh thực sự.`numpy.fft.rfft`hoặc `torch.fft.rfft`- Tôi không biết.

> `O(N²)`复杂度  đối với `N=256`验证正确性还行, đối với thực音频 không dùng.`numpy.fft.rfft`Hoặc`torch.fft.rfft`

### Bước 4: tìm tần số thống trị

Chỉ số đỉnh độ lớn `k_star`bản đồ tần số `k_star * sr / N`- Động hành này trên âm đạo 440 Hz sẽ trả lại một đỉnh ở bin`440 * N / sr`- Tôi không biết.

> 幅度峰值索引 `k_star`đối với tần suất`k_star * sr / N`△ đối với 440 Hz 正弦波运行`440 * N / sr`处返峰值──

### Bước 5: thể hiện danh tính ẩn danh

Mô hình 7 kHz sinus ở 10 kHz (Nyquist = 5 kHz).`10 − 7 = 3 kHz`. FFT đỉnh xuất hiện ở 3 kHz. Đây là biểu diễn tên gọi cổ điển và lý do tại sao mọi DAC / ADC tàu với một tường gạch lọc đi thấp.

> 以 10 kHz 采样 7 kHz 正弦波(奈奎斯特频率 = 5 kHz) ・7 kHz 音调高于奈奎斯特频率,会折叠到`10 − 7 = 3 kHz` FFT 峰值 xuất hiện ở 3 kHz  Đây là biểu diễn hỗn hợp cổ điển, cũng là lý do tại sao mỗi DAC / ADC đều trang bị 壁式低通波器 

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.





> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

Những gì bạn sẽ gửi vào năm 2026:

> 2026 năm bạn thực sự sẽ sử dụng các công nghệ:

| Task | Library | Why |
|------|---------|-----|
| Read/write WAV/FLAC/OGG | `soundfile` (libsndfile wrapper) | Fastest, stable, returns float32. |
| Resample | `torchaudio.transforms.Resample` or `librosa.resample` | Correct anti-aliasing built in. |
| STFT / Mel | `torchaudio` or `librosa` | GPU-friendly; PyTorch ecosystem. |
| Real-time streaming | `sounddevice` or `pyaudio` | Cross-platform PortAudio bindings. |
| Inspect a file | `ffprobe` or `soxi` | CLI, fast, reports sr/channels/codec. |

| 任务 | 库 | 原因 |
|------|----|------|
| 读写 WAV/FLAC/OGG | `soundfile`（libsndfile 封装） | 最快、最稳定，返回 float32。 |
| 重采样 | `torchaudio.transforms.Resample` 或 `librosa.resample` | 内置正确的抗混叠滤波。 |
| STFT / Mel | `torchaudio` 或 `librosa` | GPU 友好；PyTorch 生态。 |
| 实时流 | `sounddevice` 或 `pyaudio` | 跨平台 PortAudio 绑定。 |
| 检查文件 | `ffprobe` 或 `soxi` | 命令行工具，快速报告采样率/声道/编码。 |

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


Quy tắc quyết định: **match sample rate before you match anything else**Whisper dự kiến 16 kHz mono float32 . Đưa nó 44,1 kHz stereo và bạn sẽ có rác giống như một lỗi mô hình.

> 决策规则:**在匹配其他任何东西之前先匹配采样率**❖ Nhầm 期望 16 kHz 单声道 float32──传入 44.1 kHz 立体声, bạn sẽ nhận được trông giống như model bug của rác thải ❖

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;




## Chuyển nó đi.

Cứ như `outputs/skill-audio-loader.md`Kỹ năng này giúp bạn kiểm tra rằng đầu vào âm thanh phù hợp với kỳ vọng của mô hình dòng chảy và lấy lại đúng khi không.

> 保存为 `outputs/skill-audio-loader.md`◊ Kỹ năng này giúp bạn kiểm tra âm thanh nhập liệu nó phù hợp với mong đợi của mô hình, và thực sự tái tạo khi không phù hợp.

## Tập luyện bài tập

1. **Easy.**Kết hợp một hỗn hợp 1 giây của 220 Hz + 440 Hz + 880 Hz ở 16 kHz.
   **简单。**合成 một tín hiệu hỗn hợp 1 giây 220 Hz + 440 Hz + 880 Hz, tỷ lệ lấy 16 kHz──运行 DFT── xác nhận ở vị trí dự kiến bin  có ba đỉnh──
2. **Medium.**Tải lại một WAV 3 giây của giọng nói của bạn ở 48 kHz.`torchaudio.transforms.Resample`(với chống liêm), sau đó lên 16 kHz bằng cách sử dụng sự phân số ngây thơ (mỗi mẫu thứ ba).
   **中等。**录制一段 3 秒 48 kHz 的语音 WAV──使用 `torchaudio.transforms.Resample`(带抗混叠)降采样到16 kHz, sau đó sử dụng đơn giản抽取(每隔三个样本取一个)降采样到16 kHz──对两者做FFT──混叠现出哪里?
3. **Hard.**Xây dựng STFT từ đầu chỉ sử dụng `math`và DFT từ bước 3. kích thước khung 400, hop 160, cửa sổ Hann.`matplotlib.pyplot.imshow`Đây là quang phổ của bài học 02.
   **困难。**Chỉ dùng thôi`math`和步骤 3 của DFT từ零构建 STFT──大小 400,步长 160,Hann 窗──用 `matplotlib.pyplot.imshow`图画幅度图――这是第02课的频谱图――

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Sample rate | How many samples per second | Frequency in Hz at which the ADC measures the signal. |
| Nyquist | The max frequency you can represent | `sr/2`; energy above it aliases back down. |
| Bit depth | Resolution of each sample | `int16` = 65,536 levels; `float32` = 24-bit precision in `[-1, 1]`. |
| DFT | The Fourier transform for sequences | `N` samples → `N` complex frequency coefficients. |
| FFT | The fast DFT | `O(N log N)` algorithm requiring `N` = power of 2. |
| Bin | Frequency column | `k · sr / N` Hz; resolution = `sr / N`. |
| STFT | Spectrogram under the hood | Framed + windowed FFT over time. |
| Aliasing | Weird frequency ghosts | Energy above Nyquist mirroring down to lower bins. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 采样率 | 每秒多少个采样点 | ADC 测量信号的频率（Hz）。 |
| 奈奎斯特 | 能表示的最大频率 | `sr/2`；超过它的能量会混叠回来。 |
| 位深度 | 每个采样点的精度 | `int16` = 65,536 级；`float32` = `[-1, 1]` 中 24 位精度。 |
| DFT | 序列的傅里叶变换 | `N` 个采样 → `N` 个复数频率系数。 |
| FFT | 快速 DFT | `O(N log N)` 算法，要求 `N` 为 2 的幂。 |
| Bin | 频率列 | `k · sr / N` Hz；分辨率 = `sr / N`。 |
| STFT | 频谱图的底层实现 | 分帧 + 加窗的 FFT 随时间推移。 |
| 混叠 | 奇怪的频率鬼影 | 超过奈奎斯特的能量镜像到更低的 bin。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Shannon (1949). Communication in the Presence of Noise](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf) bài báo đằng sau định lý lấy mẫu.
  Shannon (1949) 带噪音条件下的通信采样定理背后的论文──
- [Smith — The Scientist and Engineer's Guide to Digital Signal Processing](https://www.dspguide.com/ch8.htm) sách giáo khoa DSP miễn phí, theo luật.
  Smith khoa học gia và kỹ sư's Digital Signal Processing Guide miễn phí DSP giáo dục cổ điển
- [librosa docs — audio primer](https://librosa.org/doc/latest/tutorial.html) thực tế đi bộ với mã.
  library 文档音频入门带代码的实践教程──
- [Heinrich Kuttruff — Room Acoustics (6th ed.)](https://www.routledge.com/Room-Acoustics/Kuttruff/p/book/9781482260434) tham khảo lý do tại sao âm thanh trong thế giới thực không phải là một sinus sạch.
  Heinrich Kuttruff房间声学(第 6 版)  giải thích tại sao âm thanh thế giới thực không phải là một cuốn sách tham khảo của sóng âm thanh chính xác.
- [Steve Eddins — FFT Interpretation notebook](https://blogs.mathworks.com/steve/2020/03/30/fft-spectrum-and-spectral-densities/) Nhận thức của con số tần số đã được giải quyết trong 10 phút.
  Steve Eddins FFT 解读笔记10 分钟搞清频率 ピンイン 的直觉──

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

