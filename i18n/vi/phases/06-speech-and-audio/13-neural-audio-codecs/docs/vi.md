# Bộ mã âm thanh thần kinh  EnCodec, SNAC, Mimi, DAC và phân chia âm nghĩa-tâm ngữ

> 2026 audio generation gần như là tất cả các token. EnCodec, SNAC, Mimi và DAC biến hình dạng sóng liên tục thành chuỗi riêng biệt mà một biến thể có thể dự đoán.

> **【中文解读】**2026 năm của âm thanh sản xuất hầu hết dựa trên token.EnCodec, SNAC, Mimi, DAC sẽ tiếp tục chuyển hình dạng thành chuỗi phân tán, để Transformer có thể dự đoán.

> **【拓展：音频 token 化】**Như văn bản có token BPE sẽ biến văn bản thành token,音频 có EnCodec và các bộ giải mã sẽ biến âm thanh thành token.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 10 · 11 (Quantization), Phase 5 · 19 (Subword Tokenization) | **前置知识:** 阶段 6 · 02（频谱图），阶段 10 · 11（量化），阶段 5 · 19（子词分词）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## Vấn đề  vấn đề giới thiệu

Các mô hình ngôn ngữ hoạt động trên các mã thông báo riêng biệt. Âm thanh là liên tục. Nếu bạn muốn một mô hình LLM kiểu cho ngôn ngữ / âm nhạc  MusicGen, Moshi, Sesame CSM, VibeVoice, Orpheus  bạn cần một **neural audio codec**: một bộ mã hóa học tập phân loại âm thanh thành một từ vựng nhỏ của các token, và một bộ mã hóa phù hợp tái tạo hình dạng sóng.

> 语言模型处理离散 token──音频是连续的── nếu bạn muốn xây dựng một mô hình LLM 风格的模型MusicGen、Moshi、Sesame CSM、VibeVoice、Orpheus你首先需要一个**神经音频编解码器**Một máy viết chữ học tập sẽ phân tán âm thanh thành token biểu tượng nhỏ, cộng với một máy viết chữ phù hợp.

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Hai gia đình đã xuất hiện:

> Hai gia đình đã xuất hiện:

1. **Reconstruction-first codecs** EnCodec, DAC. Tối ưu hóa chất lượng âm thanh nhận thức. Các token là "những âm thanh"  chúng ghi lại mọi thứ bao gồm danh tính loa, timbre, tiếng ồn nền.
   **重建优先编解码器**EnCodec、DAC──优化感知音频质量──Token 是"声学"它们捕获一切,包括说话人身份、音色、背景噪音──
2. **Semantic-first codecs** Mimi (Kyutai), SpeechTokenizer. Bắt đầu sách mã đầu tiên mã hóa nội dung ngôn ngữ / âm thanh (thường bằng cách chưng cất từ WavLM).
   **语义优先编解码器**Mimi(Kyutai)、SpeechTokenizer。强制第一码本编码语言/语音内容(通常通过从波LM 蒸)。后续码本是声学细节。

Những thông tin sâu sắc về năm 2024-2026: **a pure reconstruction codec gives you blurry speech when you try to generate from text.**Các mã codec của LLM phải học cả cấu trúc ngôn ngữ và cấu trúc âm thanh trong cùng một codebook, không có quy mô.

> 2024-2026 năm:**纯重建编解码器在从文本生成时给你模糊的语音。**编解码代币 上的LLM 必须同时学习语言结构和声学结构在同一码本中,这无法扩展──将它们分离语义码本 0,声学码本 1-N正是Moshi 和芝麻CSM成功的关键──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Four codec landscape: EnCodec, DAC, SNAC (multi-scale), Mimi (semantic+acoustic)](../assets/codec-comparison.svg)

### Tránh cốt lõi: Quantization Vektor còn lại (RVQ)

Thay vì một cuốn sách mã lớn (có thể cần hàng triệu mã để có chất lượng tốt), tất cả các codec âm thanh hiện đại sử dụng **RVQ**: một loạt các codebook nhỏ. codebook đầu tiên định lượng sản xuất encoder; thứ hai định lượng dư thừa; vv Mỗi codebook là 1024 codebook. 8 codebook = từ vựng hiệu quả của 1024 ^ 8 = 10^24.

> Thay vì sử dụng một mã lớn, tất cả các bộ xử lý âm thanh hiện đại đều sử dụng.**RVQ**Một nhóm nhỏ codebook của cấp liên. Một số codebook tự do được định lượng.

Vào thời điểm suy luận, bộ giải mã tổng hợp tất cả các mã được chọn cho mỗi khung để tái cấu trúc.

> Khi được đưa ra, máy giải mã sẽ tìm kiếm và tái tạo tất cả các mã trong mỗi cuộc.

### Bốn codec quan trọng vào năm 2026

**EnCodec (Meta, 2022).**Hình cơ bản. Mã mã hóa-bẻ khóa trên dạng sóng, nút nút rơm RVQ. 24 kHz, 32 sổ mã có thể, mặc định 4 sổ mã @ 1.5 kbps. Sử dụng `1D conv + transformer + 1D conv`Thiết kế, được sử dụng bởi MusicGen.

> **EnCodec（Meta，2022）。**基线──波形上的编码器-解码器,RVQ 瓶──24 kHz, tối đa 32 个码本,默认 4 个码本 @ 1.5 kbps──使用 `1D conv + transformer + 1D conv`架构──MusicGen 使用──

**DAC (Descript, 2023).**RVQ với sổ mã L2-tự chuẩn hóa, chức năng kích hoạt định kỳ, lỗ hổng cải thiện. Độ trung thực tái tạo cao nhất của bất kỳ codec mở nào  đôi khi không thể phân biệt với ngôn ngữ gốc với 12 sổ mã. 44.1 kHz băng thông đầy đủ.

> **DAC（Descript，2023）。**采用 L2 归化码本、周期性激活函数和改进损失的RVQ──开源编码器中重建保真度最高12个码本时有时与原始语音无法分辨──44.1 kHz 全频带──

**SNAC (Hubert Siuzdak, 2024).**RVQ nhiều quy mô  các sổ mã thô hoạt động với tốc độ khung thấp hơn so với các sổ cái tốt. Nó hiệu quả mô hình âm thanh theo cấp bậc: một "phác thảo" thô ở ~ 12 Hz cộng với chi tiết ở 50 Hz. Được sử dụng bởi Orpheus-3B vì cấu trúc bậc bậc được lập bản đồ tốt cho thế hệ dựa trên LM.

> **SNAC（Hubert Siuzdak，2024）。**Nhiều kích thước RVQ粗码本以细码本较低的率运行──有效地分层建模音频:约12 Hz 的粗草图加50 Hz 的细节──Orpheus-3B 使用, vì cấu trúc phân层 rất tốt để映射 đến LM dựa trên sản xuất──

**Mimi (Kyutai, 2024).**Game-changer 2026: tốc độ khung hình 12,5 Hz ( cực thấp), 8 codebook @ 4.4 kbps. Codebook 0 là **distilled from WavLM** được đào tạo để dự đoán các tính năng nội dung nói chuyện của WavLM. Các codebook 1-7 là dư lượng âm thanh.

> **Mimi（Kyutai，2024）。**2026 年的游戏规则变化者──12.5 Hz 率(极低),8 个码本 @ 4.4 kbps──码本 0 **从 WavLM 蒸馏** tập để dự đoán các đặc điểm nội dung tiếng của WavLM. 码本 1-7 là sự khác biệt về âm thanh.

### Tốc độ khung hình quan trọng cho mô hình hóa ngôn ngữ

Tốc độ khung hình thấp hơn = chuỗi ngắn hơn = LM nhanh hơn.

> 率 đối với ngôn ngữ xây dựng rất quan trọng: 率越低 = 序列越短 = LM 越快──

| Codec | Frame rate | 1 s = N frames | Good for |
|-------|-----------|----------------|---------|
| EnCodec-24k | 75 Hz | 75 | music, general audio |
| DAC-44.1k | 86 Hz | 86 | high-fidelity music |
| SNAC-24k (coarse) | ~12 Hz | 12 | AR-LM efficient |
| Mimi | 12.5 Hz | 12.5 | streaming speech |

| 编解码器 | 帧率 | 1 秒 = N 帧 | 适用场景 |
|---------|------|------------|---------|
| EnCodec-24k | 75 Hz | 75 | 音乐、通用音频 |
| DAC-44.1k | 86 Hz | 86 | 高保真音乐 |
| SNAC-24k（粗） | ~12 Hz | 12 | AR-LM 高效 |
| Mimi | 12.5 Hz | 12.5 | 流式语音 |

Ở 12,5 Hz, một phát biểu 10 giây chỉ là 125 khung codec  một bộ biến thể có thể dễ dàng dự đoán chúng.

> Ở mức 12.5 Hz, một đoạn 10 giây của giọng nói chỉ có 125 mã giải mã.

### Các token ngữ nghĩa so với âm thanh

> 语义 vs 声学 token

```
frame_t → [semantic_token_t, acoustic_token_0_t, acoustic_token_1_t, ..., acoustic_token_6_t]
```

- **Semantic token (codebook 0 in Mimi).**Mã hóa những gì đã được nói  âm, từ, nội dung.
  **语义 token（Mimi 中的码本 0）。**编码说了什么音素、单词、内容──通过辅助预测损失从波LM 蒸──
- **Acoustic tokens (codebooks 1-7).**Định nghĩa âm thanh, danh tính loa, âm nhạc, tiếng ồn nền, chi tiết tinh tế.
  **声学 token（码本 1-7）。**编码音色、说话人身份、律、背景噪音、精细细节──

Một LM AR dự đoán đầu tiên token ngữ nghĩa (được điều chỉnh trên văn bản), sau đó dự đoán token âm thanh (được điều chỉnh trên tham chiếu ngữ nghĩa + loa).

> Bản thân LM 先预测语义 token(以文本为条件),再预测语学 token(以语义 + 说话人参考为条件) ・・・这种分解正是现代 TTS 能够零样本克隆声音的原因:语义模型处理内容,声学模型处理音色。

### 2026 chất lượng tái tạo (bit/s, tốc độ bit thấp hơn là tốt hơn)

| Codec | Bitrate | PESQ | ViSQOL |
|-------|---------|------|--------|
| Opus-20kbps | 20 kbps | 4.0 | 4.3 |
| EnCodec-6kbps | 6 kbps | 3.2 | 3.8 |
| DAC-6kbps | 6 kbps | 3.5 | 4.0 |
| SNAC-3kbps | 3 kbps | 3.3 | 3.8 |
| Mimi-4.4kbps | 4.4 kbps | 3.1 | 3.7 |

| 编解码器 | 比特率 | PESQ | ViSQOL |
|---------|--------|------|--------|
| Opus-20kbps | 20 kbps | 4.0 | 4.3 |
| EnCodec-6kbps | 6 kbps | 3.2 | 3.8 |
| DAC-6kbps | 6 kbps | 3.5 | 4.0 |
| SNAC-3kbps | 3 kbps | 3.3 | 3.8 |
| Mimi-4.4kbps | 4.4 kbps | 3.1 | 3.7 |

Các codec truyền thống như Opus vẫn thắng từng bit về chất lượng nhận thức.**discrete tokens**(mà Opus không sản xuất) và **generative-model quality**(làm gì LM có thể làm với những token).

> 传统编解码器 (如 Opus) vẫn thắng trên mỗi bit cảm nhận chất lượng.**离散 token**(Opus 不产生) và**生成模型质量**(LM 能用这些符号做什么) 上胜出.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.



## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
rvq-codec-cascade
```

## Hãy xây dựng nó

### Bước 1: mã hóa bằng EnCodec

```python
from encodec import EncodecModel
import torch

model = EncodecModel.encodec_model_24khz()
model.set_target_bandwidth(6.0)  # kbps

wav = torch.randn(1, 1, 24000)
with torch.no_grad():
    encoded = model.encode(wav)
codes, scale = encoded[0]
# codes: (1, n_codebooks, n_frames), dtype=int64
```

`n_codebooks=8`với tốc độ 6 kbps. Mỗi mã là 0-1023 (10 bit).

> 6 kbps 下 `n_codebooks=8`❖ Mỗi mã lấy giá trị 0-1023(10 比特)

### Bước 2: giải mã và đo tái tạo

```python
with torch.no_grad():
    wav_recon = model.decode([(codes, scale)])

from torchaudio.functional import compute_deltas
import torch.nn.functional as F

mse = F.mse_loss(wav_recon[:, :, :wav.shape[-1]], wav).item()
```

### Bước 3: chia cắt âm nghĩa-tâm âm (tình hình Mimi)

```python
from moshi.models import loaders
mimi = loaders.get_mimi()

with torch.no_grad():
    codes = mimi.encode(wav)  # shape (1, 8, frames@12.5Hz)

semantic = codes[:, 0]
acoustic = codes[:, 1:]
```

Bộ mã ngữ nghĩa 0 được sắp xếp với WavLM. Bạn có thể đào tạo một bộ biến đổi văn bản sang ngữ nghĩa  từ vựng nhỏ hơn nhiều so với đi trực tiếp sang âm thanh. Sau đó một điều kiện giải mã dạng âm thanh riêng biệt cho dạng sóng trên một tham chiếu loa.

> 语义码本 0 与 WavLM 对齐. Bạn có thể luyện tập một文本→语义 Transformer 词表比直接到音频小得多──然后一个独立的声学→波形解码器以说话人参考为条件──

### Bước 4: tại sao AR LM trên mã codec hoạt động

Đối với một clip phát biểu 10 giây tại 12.5 Hz của Mimi × 8 codebook:

```
N_tokens = 10 * 12.5 * 8 = 1000 tokens
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


1000 token là một bối cảnh tầm thường cho một bộ biến đổi. Một bộ biến đổi tham số 256M có thể tạo ra 10 giây nói chuyện trong vài millisecond trên một GPU hiện đại.

> 1000 token đối với Transformer là một phần nhỏ trên trên trên trên. Một Transformer có 2,56 tỷ tham số trên GPU hiện đại có thể tạo ra 10 giây trong vài giây.




> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

Vấn đề bản đồ → codec:

| Task | Codec |
|------|-------|
| General music generation | EnCodec-24k |
| Highest-fidelity reconstruction | DAC-44.1k |
| AR LM over speech (TTS) | SNAC or Mimi |
| Streaming full-duplex speech | Mimi (12.5 Hz) |
| Sound-effect library with text | EnCodec + T5 condition |
| Fine-grained audio editing | DAC + inpainting |

| 任务 | 编解码器 |
|------|---------|
| 通用音乐生成 | EnCodec-24k |
| 最高保真重建 | DAC-44.1k |
| 语音上的 AR LM（TTS） | SNAC 或 Mimi |
| 流式全双工语音 | Mimi（12.5 Hz） |
| 文本驱动的音效库 | EnCodec + T5 条件 |
| 细粒度音频编辑 | DAC + 内画 |

Quy tắc: **if you're building a generative model, start with Mimi or SNAC. If you're building a compression pipeline, use Opus.**

> 经验法则:**如果你在构建生成模型，从 Mimi 或 SNAC 开始。如果在构建压缩流水线，使用 Opus。**



## Những bẫy

- **Too many codebooks.**Thêm codebook tăng độ trung thực theo đường thẳng nhưng chiều dài chuỗi LM cũng theo đường thẳng.
  **码本过多。**Lợi lượng tăng lên tăng lên, nhưng LM 序列 dài cũng tăng lên.
- **Frame-rate mismatch.**LM đào tạo trên 12,5 Hz Mimi sau đó điều chỉnh tinh tế trên 50 Hz EnCodec thất bại lặng lẽ.
  **帧率不匹配。**Ở 12,5 Hz Mimi lên tập LM, rồi ở 50 Hz EnCodec lên định chế sẽ không thành công.
- **Assuming all codebooks equal.**Trong Mimi, codebook 0 mang nội dung; mất nó phá hủy khả năng hiểu biết.
  **假设所有码本同等重要。**Trong Mimi, mã số 0  tải nội dung; mất nó sẽ phá hủy khả năng hiểu biết.
- **Using reconstruction quality as the only metric.**Một codec có thể có sự tái tạo tuyệt vời nhưng không thể sử dụng cho thế hệ dựa trên LM nếu cấu trúc ngữ nghĩa không tốt.
  **仅用重建质量作为唯一指标。**Một trình giải mã có thể xây dựng lại chất lượng tốt, nhưng nếu cấu trúc ngữ nghĩa khác nhau, thì không cần thiết cho việc tạo dựa trên LM.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-codec-picker.md`Chọn một codec cho một nhiệm vụ tạo hoặc nén nhất định.

> 保存为 `outputs/skill-codec-picker.md`❖ Cho một nhiệm vụ tạo hoặc nén cho chọn mã hóa ❖

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`Nó thực hiện một bộ định lượng đồ chơi scalar + dư và đo lỗi tái tạo khi bạn thêm sách mã.
   **简单。**运行 `code/main.py` Nó thực hiện một bộ chỉ số đồ chơi + phân biệt lượng hóa, đo lường theo số liệu tăng của sự sai lầm xây dựng lại
2. **Medium.**Thiết lập `encodec`và so sánh 1, 4, 8, 32 codebook trên một clip bài phát biểu kéo dài.
   **中等。**                                          `encodec`, trong phần còn lại của đoạn phim tiếng nói trên so sánh 1、4、8、32 个码本── vẽ PESQ hoặc MSE vs 比特率──
3. **Hard.**Load Mimi. Encode một clip. Thay thế codebook 0 bằng số nguyên số ngẫu nhiên; decode. Sau đó thay thế codebook 7 tương tự. So sánh hai sự tham nhũng  codebook 0 tham nhũng nên phá hủy khả năng hiểu biết; codebook 7 tham nhũng hầu như không thay đổi bất cứ điều gì.
   **困难。**加载 Mimi。编码一段音频。 dùng bất cứ số lượng nào thay đổi码本 0;解码。然后类似地 thay đổi码本 7。

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| RVQ | Residual quantization | Cascade of small codebooks; each quantizes the previous residual. |
| Frame rate | Codec speed | How many token-frames per second. Lower = faster LM. |
| Semantic codebook | Codebook 0 (Mimi) | Codebook distilled from SSL features; encodes content. |
| Acoustic codebooks | Everything else | Timbre, prosody, noise, fine detail. |
| PESQ / ViSQOL | Perceptual quality | Objective metrics correlating with MOS. |
| EnCodec | Meta codec | The RVQ baseline; used by MusicGen. |
| Mimi | Kyutai codec | 12.5 Hz frame rate; semantic-acoustic split; powers Moshi. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| RVQ | 残差量化 | 小码本级联；每个量化前一个残差。 |
| 帧率 | 编解码器速度 | 每秒多少 token 帧。越低 = LM 越快。 |
| 语义码本 | 码本 0（Mimi） | 从 SSL 特征蒸馏的码本；编码内容。 |
| 声学码本 | 其余所有 | 音色、韵律、噪声、精细细节。 |
| PESQ / ViSQOL | 感知质量 | 与 MOS 相关的客观指标。 |
| EnCodec | Meta 编解码器 | RVQ 基线；MusicGen 使用。 |
| Mimi | Kyutai 编解码器 | 12.5 Hz 帧率；语义-声学分离；驱动 Moshi。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Défossez et al. (2023). EnCodec](https://arxiv.org/abs/2210.13438) Hình điểm cơ bản RVQ.
  Défossez 等 (2023). EnCodecRVQ 基线。
- [Kumar et al. (2023). Descript Audio Codec (DAC)](https://arxiv.org/abs/2306.06546) Cung cấp trung thành nhất mở.
  Kumar 等 (2023). DAC最高保真开源编解码器
- [Siuzdak (2024). SNAC](https://arxiv.org/abs/2410.14411) RVQ đa quy mô.
  Siuzdak (2024). SNAC多尺度 RVQ。
- [Kyutai (2024). Mimi codec](https://kyutai.org/codec-explainer) phân chia âm nghĩa-tâm âm, chưng cất WavLM.
  Kyutai (2024). Mimi 编解码器语义-声学分离,WavLM 蒸。
- [Borsos et al. (2023). AudioLM](https://arxiv.org/abs/2209.03143) mô hình ngữ nghĩa/ âm thanh hai giai đoạn.
  Borsos 等 (2023). AudioLM两阶段语义/声学范式──
- [Zeghidour et al. (2021). SoundStream](https://arxiv.org/abs/2107.03312) codec RVQ được phát trực tuyến ban đầu.
  Zeghidour 等 (2021). SoundStream原始可流式 RVQ 编解码器──

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

