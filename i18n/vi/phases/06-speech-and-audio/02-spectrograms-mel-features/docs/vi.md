# Phân quang, Mél Scale & Audio Features 频谱图, Mél Scale và âm thanh

> Các mạng thần kinh không tiêu thụ các dạng sóng nguyên liệu tốt. Chúng tiêu thụ quang phổ. Chúng tiêu thụ quang phổ mel thậm chí tốt hơn. Mỗi bộ phân loại âm thanh ASR, TTS và vào năm 2026 sống hoặc chết do lựa chọn xử lý trước này.

> **【中文解读】**Phân tích của hệ thống xử lý sóng gốc không tốt, nhưng xử lý tần số tần số hiệu quả tốt hơn, xử lý tần số tần số hiệu quả tốt hơn.

> **【拓展：Mel 频谱图是音频 AI 的 "图像"】**Mel 频谱图将音频转换为 2D 图像(时间×频率), có thể sử dụng CNN/ViT 处理──Whisper、MusicGen、Stable Audio 都使用 Mel 频谱图作为中间表示──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 01 (Audio Fundamentals) | **前置知识:** 阶段 6 · 01（音频基础）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Hãy lấy một clip 10 giây 16 kHz. đó là 160.000 float, tất cả trong`[-1, 1]`, gần như hoàn toàn không liên quan đến nhãn "cô ốc" hoặc "những từ mèo". dạng sóng thô có thông tin nhưng trong một hình thức mô hình không thể dễ dàng trích xuất. Hai âm thanh giống nhau nói cách nhau 100 ms có mẫu nguyên liệu hoàn toàn khác nhau.

> 16 kHz trong 10 giây. Đó là 160.000 điểm.`[-1, 1]`Trong phạm vi, gần như không liên quan đến nhãn "dog calling" hoặc "单词 cat" hoàn toàn không liên quan.

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Một quang phổ sửa chữa điều này. Nó phá vỡ chi tiết thời gian nơi nhận thức của con người bỏ qua nó (microsecond jitter) và bảo tồn cấu trúc nơi nhận thức tham dự (đôi tần số là năng lượng, qua cửa sổ thời gian ~ 1025 ms).

> 频谱图 giải quyết vấn đề này. Nó thu nhỏ các chi tiết thời gian mà con người cảm nhận bỏ qua (<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

Các quang phổ mel đẩy xa hơn. Con người nhận thức âm thanh theo cách logaritm: 100 Hz vs 200 Hz âm thanh "các khoảng cách nhau" như 1000 Hz vs 2000 Hz. Skala mel biến dạng trục tần số để phù hợp.

> Mél 频谱图进一步──人类对音高的感知是对数:100 Hz 与 200 Hz 听起来和1000 Hz 与2000 Hz "距离一样远"──Mel scale will be frequency axis tortuous to match this perception──Mel 频谱图是2010-2026年语音机学习中最重要的单一特征──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Waveform to STFT to mel spectrogram to MFCC ladder](../assets/mel-features.svg)

**STFT (Short-Time Fourier Transform).**Cắt hình dạng sóng thành khung chồng chéo (tình thường: cửa sổ 25 ms, hop 10 ms = 400 mẫu / 160 mẫu ở 16 kHz).`(n_frames, n_freq_bins)`Đó là quang phổ của anh.

> **STFT（短时傅里叶变换）。**将波形切成重叠的(典型:25 ms 窗口,10 ms 步长 = 16 kHz 下400 采样点 / 160 采样点) ・・・每乘以窗函数(默认 Hann;Hamming 略有不同) ・・・对每做 FFT。将幅谱堆叠成`(n_frames, n_freq_bins)`Đây là hình ảnh của bạn.

**Log-magnitude.**Tầm độ lớn có thể dao động từ 5-6 bậc.`log(|X| + 1e-6)`hoặc `20 * log10(|X|)`Mỗi đường ống sản xuất sử dụng log magnitude, không phải là nguyên liệu.

> **对数幅度。**Độ dài ban đầu trong 5-6 lớp số lượng.`log(|X| + 1e-6)`Hoặc`20 * log10(|X|)`Để nén động thái phạm vi. Mỗi dòng sản xuất nước được sử dụng cho số lượng chiều cao chứ không phải chiều cao ban đầu.

**Mel scale.**Tần suất `f`trong bản đồ Hz đến mel `m`bởi `m = 2595 * log10(1 + f / 700)`. Bản đồ là đường thẳng dưới 1 kHz và logarithmic trên. 80 mel bins bao gồm 08 kHz là đầu vào ASR tiêu chuẩn.

> **Mel 尺度。**频率 `f`(Hz)映射到 mel `m`公式为 的公式为`m = 2595 * log10(1 + f / 700)`◊该映射在1 kHz 以下大致线性,以上大致对数──覆盖 08 kHz 80 个 melbin là tiêu chuẩn ASR 输入──

**Mel filterbank.**Một bộ bộ bộ lọc tam giác nằm trong khoảng cách bằng nhau trên thang mel. Mỗi bộ lọc là tổng cân của các thùng FFT lân cận.

> **Mel 滤波器组。**Một nhóm trên thang máy và khoảng cách giữa các thứ tự. Mỗi bộ máy là cộng lượng của các bin FFT lân cận.

**Log-mel spectrogram.** `log(mel_spec + 1e-10)`- Hướng dẫn của Whisper, hướng dẫn của Parakeet, hướng dẫn của SeamlessM4T, hướng dẫn âm thanh toàn cầu năm 2026.

> **对数 Mel 频谱图。** `log(mel_spec + 1e-10)`❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ Nhầm ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ 

**MFCCs.**Hãy lấy quang phổ log-mel, áp dụng một DCT (tiêu II), giữ 13 nhân tố đầu tiên. Khóa các tính năng và nén hơn nữa. tính năng thống trị cho đến khoảng năm 2015 khi các CNN / Transformers trên log-mel thô bắt kịp.

> **MFCC。**取对数 Mel 频谱图,应用 DCT(类 II),保留前 13 个系数──除特征间相关性并进一步压缩──2015年之前的主流特征,之后 CNN/Transformer 在原始 log-mel 上追上──仍用于说话人识别(x-vector、ECAPA)──

**Resolution trade.**FFT lớn hơn = độ phân giải tần số tốt hơn nhưng độ phân giải thời gian tồi tệ hơn. 25 ms / 10 ms là mặc định của âm thanh-ML; 50 ms / 12,5 ms cho âm nhạc; 5 ms / 2 ms cho phát hiện tạm thời (những đập trống, âm thanh).

> **分辨率权衡。**FFT lớn hơn = tần số phân giải tốt hơn nhưng tần số phân giải thời gian kém hơn.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.



## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
spectrogram-window
```

## Hãy xây dựng nó

### Bước 1: khung hình sóng

```python
def frame(signal, frame_len, hop):
    n = 1 + (len(signal) - frame_len) // hop
    return [signal[i * hop : i * hop + frame_len] for i in range(n)]
```

Một clip 10 giây 16 kHz với `frame_len=400, hop=160`Tạo ra 998 khung hình.

> Một đoạn 10 giây 16 kHz 的音频,使用 `frame_len=400, hop=160`, có được 998 ──

### Bước 2: cửa sổ Hann

```python
import math

def hann(N):
    return [0.5 * (1 - math.cos(2 * math.pi * n / (N - 1))) for n in range(N)]
```

Tăng số nhân tố trước FFT. loại bỏ rò rỉ quang phổ do cắt giảm ở các điểm cuối không bằng 0.

> Trước FFT  từng yếu tố được nhân lên  loại bỏ các phát thải tần số dẫn đến sự cắt đứt ở các điểm không phân đoạn 

### Bước 3: Độ lớn STFT

```python
def stft_magnitude(signal, frame_len=400, hop=160):
    win = hann(frame_len)
    frames = frame(signal, frame_len, hop)
    return [magnitudes(dft([w * s for w, s in zip(win, f)])) for f in frames]
```

Sử dụng sản xuất `torch.stft`hoặc `librosa.stft`(FFT hỗ trợ, vectorized). vòng lặp ở đây là giáo dục; nó chạy trên clip ngắn trong `code/main.py`- Tôi không biết.

> 生产环境使用 `torch.stft`Hoặc`librosa.stft`(Dựa trên FFT  định lượng) `code/main.py`中处理短音频片段──

### Bước 4: Mel filterbank

```python
def hz_to_mel(f):
    return 2595.0 * math.log10(1.0 + f / 700.0)

def mel_to_hz(m):
    return 700.0 * (10 ** (m / 2595.0) - 1)

def mel_filterbank(n_mels, n_fft, sr, fmin=0, fmax=None):
    fmax = fmax or sr / 2
    mels = [hz_to_mel(fmin) + (hz_to_mel(fmax) - hz_to_mel(fmin)) * i / (n_mels + 1)
            for i in range(n_mels + 2)]
    hzs = [mel_to_hz(m) for m in mels]
    bins = [int(h * n_fft / sr) for h in hzs]
    fb = [[0.0] * (n_fft // 2 + 1) for _ in range(n_mels)]
    for m in range(n_mels):
        for k in range(bins[m], bins[m + 1]):
            fb[m][k] = (k - bins[m]) / max(1, bins[m + 1] - bins[m])
        for k in range(bins[m + 1], bins[m + 2]):
            fb[m][k] = (bins[m + 2] - k) / max(1, bins[m + 2] - bins[m + 1])
    return fb
```

80 mels bao gồm 08 kHz với `n_fft=400`cho một `(80, 201)`Matrix.`(n_frames, 201)`STFT lớn bằng chuyển để có được `(n_frames, 80)`MEL spectrogram.

> 覆盖 08 kHz của 80 个 mel 波器,`n_fft=400`, nhận được`(80, 201)`矩阵――将 `(n_frames, 201)`Lượng STFT được chuyển đổi`(n_frames, 80)`ng ng ng ng ng ng ng

### Bước 5: log-mail

```python
def log_mel(mel_spec, eps=1e-10):
    return [[math.log(max(v, eps)) for v in frame] for frame in mel_spec]
```

Các lựa chọn thay thế chung: `librosa.power_to_db`(Db chuẩn hóa tham chiếu),`10 * log10(power + eps)`Whisper sử dụng một clip liên quan hơn + bình thường hóa thói quen (xem Whisper's `log_mel_spectrogram`().

> 常见替代方案:`librosa.power_to_db`(đề cập đến dB)`10 * log10(power + eps)`❖ Nhầm sử dụng cắt cắt phức tạp hơn 归一化流程(参见 Nhầm `log_mel_spectrogram`(■)

### Bước 6: MFCC

```python
def dct_ii(x, n_coeffs):
    N = len(x)
    return [
        sum(x[n] * math.cos(math.pi * k * (2 * n + 1) / (2 * N)) for n in range(N))
        for k in range(n_coeffs)
    ]
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


Đưa DCT vào mỗi khung log-mel, giữ 13 hợp đồng đầu tiên. đó là matrix MFCC của bạn. hợp đồng đầu tiên thường bị giảm (nó mã hóa năng lượng tổng thể).

> Đối với mỗi log-mail  áp dụng DCT, giữ trước 13 系数── đây là mô hình MFCC của bạn── số 1 thường bị bỏ rơi.




> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

Số 2026:

> 2026 năm của công nghệ:

| Task | Features |
|------|----------|
| ASR (Whisper, Parakeet, SeamlessM4T) | 80 log-mels, 10 ms hop, 25 ms window |
| TTS acoustic model (VITS, F5-TTS, Kokoro) | 80 mels, 5–12 ms hop for fine temporal control |
| Audio classification (AST, PANNs, BEATs) | 128 log-mels, 10 ms hop |
| Speaker embedding (ECAPA-TDNN, WavLM) | 80 log-mels or raw-waveform SSL |
| Music (MusicGen, Stable Audio 2) | EnCodec discrete tokens (not mels) |
| Keyword spotting | 40 MFCCs for tiny devices |

| 任务 | 特征配置 |
|------|----------|
| ASR（Whisper、Parakeet、SeamlessM4T） | 80 log-mels，10 ms 步长，25 ms 窗口 |
| TTS 声学模型（VITS、F5-TTS、Kokoro） | 80 mels，5–12 ms 步长，精细时间控制 |
| 音频分类（AST、PANNs、BEATs） | 128 log-mels，10 ms 步长 |
| 说话人嵌入（ECAPA-TDNN、WavLM） | 80 log-mels 或原始波形 SSL |
| 音乐（MusicGen、Stable Audio 2） | EnCodec 离散 token（非 mels） |
| 关键词检测 | 40 MFCCs，用于小型设备 |

Quy tắc: **if you are not working on music, start with 80 log-mels.**Cánh nặng bằng chứng là bất kỳ sự lệch lạc nào.

> 经验法则:**如果你不是在做音乐，就从 80 log-mels 开始。**Bất kỳ sự phân biệt nào cũng cần chứng minh tính hợp lý của nó.



## Những bẫy vẫn còn tồn tại vào năm 2026

> Năm 2026 vẫn còn trong bẫy tội phạm

- **Mel count mismatch.**Đào tạo với 80 m, suy luận với 128 m, thất bại im lặng, ghi hình dạng tính năng ở cả hai đầu.
  **Mel 数量不匹配。**练习用80m,推理用128m. 静默失败.
- **Sample-rate mismatch upstream.**Mels tính toán ở 22,05 kHz trông khác với 16 kHz.
  **上游采样率不匹配。**22.05 kHz  tính toán mels với 16 kHz khác biệt.
- **dB vs log.**Whisper mong đợi log-mel, không phải dB-mel. Một số đường ống HF tự phát hiện; mã tùy chỉnh của bạn sẽ không.
  **dB 与 log。**Whisper 期望 log-mel chứ không phải dB-mel。 Một số HF 流水线会自动检测;
- **Normalization drift.**Tự bình thường hóa trong quá trình đào tạo, bình thường hóa toàn cầu trong quá trình suy luận.
  **归一化漂移。**训练时逐句归结,推理时全局归结.
- **Leakage from padding.**Việc đệm không cuối của clip tạo ra một quang phổ phẳng trong khung sau.
  **填充泄漏。**Đối với đoạn phim âm thanh cuối cùng零填充会在尾部产生平坦频谱──使用对称填充或复制填充──

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-feature-extractor.md`. Khả năng chọn loại tính năng, số lượng mel, khung / hop và bình thường hóa cho một mục tiêu mô hình nhất định.

> 保存为 `outputs/skill-feature-extractor.md`                                                                                                                                                                                                                                                              

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`Nó tổng hợp một chirp (tần số quét 200 → 4000 Hz) và in các argmax mel bin mỗi khung.
   **简单。**运行 `code/main.py`△ nó tạo ra một tín hiệu   tần số từ 200 扫 đến 4000 Hz)并印每的 argmax mel bin。绘图(可选)并确认与扫频匹配。
2. **Medium.**Lại chạy với `n_mels`trong `{40, 80, 128}`và `frame_len`trong `{200, 400, 800}`- Đo băng thông cao độ qua trục thời gian.
   **中等。**用 `n_mels`Vì vậy`{40, 80, 128}`和 `frame_len`Vì vậy`{200, 400, 800}`重新运行. 沿时间轴测量. 峰带宽. 哪个组合分辨信号最好?
3. **Hard.**Thực hiện`power_to_db`và so sánh độ chính xác ASR của một phân loại CNN nhỏ trên AudioMNIST bằng cách sử dụng (a) log-mel nguyên liệu, (b) dB-mel với `ref=max`, (c) MFCC-13 + delta + delta-delta.
   **困难。**实现 `power_to_db`, trên AudioMNIST 上用微型 CNN 分类器比较 (a) 原始 log-mel、(b)`ref=max` MFCC-13 + delta + delta-delta                                                                                                                                                                                                                                            

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Frame | A slice | 25 ms chunk of waveform fed to one FFT. |
| Hop | Stride | Samples between consecutive frames; 10 ms is ASR default. |
| Window | Hann/Hamming thing | Point-wise multiplier that tapers the frame edges to zero. |
| STFT | Spectrogram generator | Framed + windowed FFT; yields time × frequency matrix. |
| Mel | Warped frequency | Log-perception scale; `m = 2595·log10(1 + f/700)`. |
| Filterbank | The matrix | Triangular filters that project STFT onto mel bins. |
| Log-mel | Whisper's input | `log(mel_spec + eps)`; standardized in 2026. |
| MFCC | Old-school feature | DCT of log-mel; 13 coeffs, decorrelated. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 帧 | 一段切片 | 送入一次 FFT 的 25 ms 波形片段。 |
| 步长 | 步幅 | 连续帧之间的采样点数；10 ms 是 ASR 默认值。 |
| 窗函数 | Hann/Hamming 那个东西 | 将帧边缘逐渐缩减为零的逐点乘数。 |
| STFT | 频谱图生成器 | 分帧 + 加窗的 FFT；产生时间 × 频率矩阵。 |
| Mel | 扭曲的频率 | 对数感知尺度；`m = 2595·log10(1 + f/700)`。 |
| 滤波器组 | 那个矩阵 | 将 STFT 投影到 mel bin 的三角滤波器。 |
| Log-mel | Whisper 的输入 | `log(mel_spec + eps)`；2026 年标准化。 |
| MFCC | 老派特征 | log-mel 的 DCT；13 个系数，去相关。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Davis, Mermelstein (1980). Comparison of parametric representations for monosyllabic word recognition](https://ieeexplore.ieee.org/document/1163420) báo cáo của MFCC.
  Davis、Mermelstein (1980) 单音节词识别的参数化表示比较MFCC 论文──
- [Stevens, Volkmann, Newman (1937). A Scale for the Measurement of the Psychological Magnitude Pitch](https://pubs.aip.org/asa/jasa/article-abstract/8/3/185/735757/) thang điểm mel ban đầu.
  Stevens, Volkmann, Newman (1937) 心理音高量级的尺度尺度 原始 mel 尺度──
- [OpenAI — Whisper source, log_mel_spectrogram](https://github.com/openai/whisper/blob/main/whisper/audio.py) đọc thực hiện tham chiếu.
  OpenAIWhisper 源码,log_mel_spectrogram阅读参考实现──
- [librosa feature extraction docs](https://librosa.org/doc/main/feature.html) tham chiếu cho `mfcc`- `melspectrogram`, và nhảy / cửa sổ.
  thư viện đặc trưng 提取文档`mfcc``melspectrogram`和 hop/window 的参考──
- [NVIDIA NeMo — audio preprocessing](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/asr_all.html#featurizers) đường ống quy mô sản xuất cho các mô hình Parakeet + Canary.
  NVIDIA NeMo音频预处理Parakeet + Canary 模型的生产级流水线──

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

