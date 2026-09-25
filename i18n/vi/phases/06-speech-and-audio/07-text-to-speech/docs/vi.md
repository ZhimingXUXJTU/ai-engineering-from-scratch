# Text-to-Speech (TTS)  Từ Tacotron đến F5 và Kokoro 语音合成  Từ Tacotron đến F5 và Kokoro

> ASR đảo ngược giọng nói thành văn bản; TTS đảo ngược văn bản thành giọng nói. Dòng 2026 gồm ba phần: văn bản → token, token → mel, mel → dạng sóng. Mỗi phần có mô hình mặc định phù hợp với máy tính xách tay.

> **【中文解读】**ASR 把语音变文字,TTS 把文字变语音──2026 年的 TTS 技术分三步:文本→token→Mel 频谱→波形──每一步都有可在笔记本上运行的默认模型──

> **【拓展：TTS 的应用】**TTS là một công nghệ có tiếng, dẫn đường, tiếng nói, trợ lý ảo (Siri/小爱同学) 无障碍辅助 (无障碍辅助) của TTS.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 09 (Seq2Seq), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 09（Seq2Seq），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Bạn có một chuỗi: "Xin hãy nhắc tôi để tưới cây vào 6 giờ chiều". Bạn cần một đoạn âm thanh 3 giây có âm thanh tự nhiên, có âm âm âm chính xác (phát ngơi, căng thẳng), phát âm "cây" với giọng nói đúng, và chạy trong dưới 300 ms trên một CPU cho một trợ lý giọng nói trực tiếp. Bạn cũng cần phải trao đổi giọng nói, xử lý nhập mã chuyển đổi ("hoàn ý tôi vào 6 giờ chiều, daijoubu?"), và không xấu hổ về tên.

> Bạn có một字符串:"Vui lòng nhắc tôi để tưới cây vào lúc 6 giờ chiều". Bạn cần một段 3 giây của音频, nghe起来自然,律正确(停顿、重音), " cây" của元音发音正确,并且在CPU上不到300 ms 就能运行以用于实时语音助手──你还需要切换声音、处理混合语言输入(" nhớ tôi vào lúc 6 giờ chiều, daijoubu?"),且不能在人名上出错──

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Các đường ống TTS hiện đại trông như thế này:

> 现代 TTS 流水线如下:

1. **Text frontend.**Tiêu chuẩn hóa văn bản (thang ngày, số, email), chuyển đổi thành âm hoặc mã thông báo từ phụ, dự đoán các tính năng prosody.
   **文本前端。**归一化文本(日期、数字、邮箱), chuyển đổi thành biểu tượng音素或子词,预测律特征。
2. **Acoustic model.**Text → mel spectrogram. Tacotron 2 (2017), FastSpeech 2 (2020), VITS (2021), F5-TTS (2024), Kokoro (2024).
   **声学模型。**文本 → Mel 频谱图──Tacotron 2(2017)、FastSpeech 2(2020)、VITS(2021)、F5-TTS(2024)、Kokoro(2024)。
3. **Vocoder.**Mel → dạng sóng. WaveNet (2016), WaveRNN, HiFi-GAN (2020), BigVGAN (2022), các bộ phận codec thần kinh trong năm 2024+.
   **声码器。**Mel → 波形──WaveNet(2016)、WaveRNN、HiFi-GAN(2020)、BigVGAN(2022)、2024+ 的神经编解码声码器──

Năm 2026, âm thanh + vocoder phân chia mờ với các mô hình phân tán đầu đến cuối và phù hợp với dòng chảy.

> Năm 2026, với sự xuất hiện của mô hình phổ biến và phù hợp dòng chảy, ranh giới của mô hình âm thanh + bộ mã âm thanh trở nên mờ ám.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Tacotron, FastSpeech, VITS, F5/Kokoro side-by-side](../assets/tts.svg)

**Tacotron 2 (2017).**Seq2seq: chár-embedding → BiLSTM encoder → vị trí nhạy cảm chú ý → autogressive LSTM decoder phát ra khung mel. chậm (AR), dao động trên văn bản dài.

> **Tacotron 2（2017）。**Seq2seq:字符嵌入 → BiLSTM 编码器 → 位置敏感注意力 → 自归 LSTM 解码器输出 mel ──慢(AR),长文本不稳定──仍被引用为基线──

**FastSpeech 2 (2020).**Không tự rút. Tự đoán thời gian đưa ra số khung mel mỗi âm thanh nhận được. 1 vượt qua, nhanh hơn Tacotron 10x. mất một số tự nhiên (sự sắp xếp đơn giản) nhưng tàu khắp nơi.

> **FastSpeech 2（2020）。**Không tự quay trở lại. 时长预测器输出每音素获得多少 mel ──单次前向,比塔科特龙快10倍.

**VITS (2021).**Cùng đào tạo bộ mã hóa + thời gian dựa trên dòng chảy + bộ giọng HiFi-GAN kết thúc đến kết thúc với suy luận biến đổi. chất lượng cao, mô hình đơn. TTS nguồn mở thống trị 20222024. Các biến thể: YourTTS (những loa không bắn), XTTS v2 (2024, Coqui).

> **VITS（2021）。**联合训练编码器 + 基流的时长预测 + HiFi-GAN 声码器端到端,使用变分推断。高质量,单模型。2022-2024年主导开源 TTS。变体:YourTTS(多说话人零样本)、XTTS v2(2024,Coqui)。

**F5-TTS (2024).**Bộ biến đổi truyền thông trên dòng chảy phù hợp. Prosody tự nhiên, sao chép âm thanh bằng không chụp với 5 giây âm thanh tham chiếu.

> **F5-TTS（2024）。**基于流匹配的扩散 Transformer──自然律,5 秒参考音频零样本声音克隆──2026 年开源 TTS 排行榜榜榜首──3.35 亿参数──

**Kokoro (2024).**Tiểu (82M), có thể chạy CPU, tốt nhất trong lớp TTS tiếng Anh cho sử dụng thời gian thực.

> **Kokoro（2024）。**: : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : :  : : : : : :       : :       :                             

**OpenAI TTS-1-HD, ElevenLabs v2.5, Google Chirp-3.**ElevenLabs v2.5 thẻ cảm xúc ("[môn thì thầm]", "[cười]") và giọng nói nhân vật thống trị sản xuất sách âm thanh vào năm 2026.

> **OpenAI TTS-1-HD、ElevenLabs v2.5、Google Chirp-3。**商业 SOTA──ElevenLabs v2.5 的情感标签("[phầm lặng]"、"[cười]")和角色声音主导 2026 年有声书制作──

### Sự phát triển của Vocoder

> ### 声码器演进

| Era | Vocoder | Latency | Quality |
|-----|---------|---------|---------|
| 2016 | WaveNet | offline only | SOTA at release |
| 2018 | WaveRNN | ~realtime | good |
| 2020 | HiFi-GAN | 100× realtime | near-human |
| 2022 | BigVGAN | 50× realtime | generalizes across speakers/langs |
| 2024 | SNAC, DAC (neural codecs) | integrated with AR models | discrete tokens, bit-efficient |

| 时代 | 声码器 | 延迟 | 质量 |
|------|--------|------|------|
| 2016 | WaveNet | 仅离线 | 发布时 SOTA |
| 2018 | WaveRNN | 约实时 | 良好 |
| 2020 | HiFi-GAN | 100× 实时 | 接近人类 |
| 2022 | BigVGAN | 50× 实时 | 跨说话人/语言泛化 |
| 2024 | SNAC, DAC（神经编解码器） | 与 AR 模型集成 | 离散 token，比特高效 |

Đến năm 2026, hầu hết các mô hình "TTS" đều là kết thúc từ văn bản đến dạng sóng; quang phổ mel là một đại diện nội bộ.

> Đến năm 2026, hầu hết các mô hình "TTS" là từ văn bản đến mô hình cuối cùng của hình dáng; mô hình tần số của mô hình là biểu hiện bên trong.

### Đánh giá

> ### 评估

- **MOS (Mean Opinion Score).**1/5 scale, nguồn từ đám đông.
  **MOS（平均意见分）。**1-5 分量表,众包── vẫn là tiêu chuẩn vàng; tốc độ đau khổ地慢──
- **CMOS (Comparative MOS).**Tương tự A-vs-B, khoảng thời gian tin cậy chặt chẽ hơn cho mỗi chú thích.
  **CMOS（比较 MOS）。**A-vs-B 偏好── mỗi dấu chấm của đặt niềm tin trong khu vực nhỏ hơn──
- **UTMOS, DNSMOS.**Các dự báo MOS thần kinh không tham chiếu được sử dụng cho bảng xếp hạng.
  **UTMOS、DNSMOS。**无参考神经 MOS 预测器。用于排行榜。
- **CER (Character Error Rate) via ASR.**Lấy TTS ra qua Whisper, tính CER so với văn bản nhập.
  **CER（字符错误率）通过 ASR。**Để TTS 输出 qua Phầmầm, đối với nhập văn bản tính toán CER ⋅ có thể hiểu được các chỉ số đại lý ⋅
- **SECS (Speaker Embedding Cosine Similarity).**Chất lượng nhân tạo giọng nói.
  **SECS（说话人嵌入余弦相似度）。**声音克隆质量──

Số 2026 trên kiểm tra-tẩy sạch LibriTTS:

> 2026 năm LibriTTS test-clean 上的数字:

| Model | UTMOS | CER (via Whisper) | Size |
|-------|-------|-------------------|------|
| Ground truth | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 335M |
| XTTS v2 | 3.81 | 3.5% | 470M |
| VITS | 3.62 | 3.1% | 25M |
| Kokoro v0.19 | 3.87 | 1.8% | 82M |
| Parler-TTS Large | 3.76 | 2.8% | 2.3B |

| 模型 | UTMOS | CER（通过 Whisper） | 大小 |
|------|-------|---------------------|------|
| 真实音频 | 4.08 | 1.2% | — |
| F5-TTS | 3.95 | 2.1% | 3.35 亿 |
| XTTS v2 | 3.81 | 3.5% | 4.7 亿 |
| VITS | 3.62 | 3.1% | 2500 万 |
| Kokoro v0.19 | 3.87 | 1.8% | 8200 万 |
| Parler-TTS Large | 3.76 | 2.8% | 23 亿 |

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.




## Hãy xây dựng nó.
```figure
sp-tts-stack
```

## Hãy xây dựng nó

### Bước 1: Phóng âm nhập

```python
from phonemizer import phonemize
ph = phonemize("Hello world", language="en-us", backend="espeak")
# 'həloʊ wɜːld'
```

Phoneme là cầu phổ quát. Tránh cung cấp văn bản thô cho bất cứ thứ gì dưới chất lượng cấp độ VITS.

> 音素是通用桥梁──避免将原始文本输入到VITS 级别以下的任何模型──

### Bước 2: chạy Kokoro (2026 CPU mặc định)

```python
from kokoro import KPipeline
tts = KPipeline(lang_code="a")  # "a" = American English
audio, sr = tts("Please remind me to water the plants at 6 pm.", voice="af_bella")
# audio: float32 tensor, sr=24000
```

- Không hoạt động, một tập tin, 82M param.

> 离线运行,单文件,82 triệu tham số

### Bước 3: chạy F5-TTS với sao chép giọng nói

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="my_voice_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please remind me to water the plants.",
)
```

Gửi một đoạn video tham chiếu 5 giây + bản sao của nó; F5 nhân bản prosody và timbre.

> 传入 5 秒参考音频 + 其转录文本;F5 克隆律和音色──

### Bước 4: HiFi-GAN vocoder từ đầu

Quá lớn để phù hợp với một kịch bản hướng dẫn, nhưng hình dạng là:

```python
class HiFiGAN(nn.Module):
    def __init__(self, mel_channels=80, upsample_rates=[8, 8, 2, 2]):
        super().__init__()
        # 4 upsample blocks, total 256x to go from mel-rate to audio-rate
        ...
    def forward(self, mel):
        return self.blocks(mel)  # -> waveform
```

Việc đào tạo: đối kháng (chống phân biệt đối xử trên cửa sổ ngắn) + mất tích tái tạo quang phổ mel + mất tích phù hợp với tính năng.`hifi-gan`repo hoặc nvidia-neMo.

> 训练:对抗式(短窗口判别器) + Mel 频谱图重建损失 + 特征匹配损失──已商品化使用 `hifi-gan`仓库或 nvidia-NeMo 的预训练检查点──

### Bước 5: toàn bộ đường ống (phép code)

```python
text = "Please remind me at 6 pm."
phones = phonemize(text)
mel = acoustic_model(phones, speaker=alice)      # [T, 80]
wav = vocoder(mel)                                # [T * 256]
soundfile.write("out.wav", wav, 24000)
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.





> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

Số 2026:

> 2026 năm của công nghệ:

| Situation | Pick |
|-----------|------|
| Real-time English voice assistant | Kokoro (CPU) or XTTS v2 (GPU) |
| Voice cloning from 5 s reference | F5-TTS |
| Commercial character voices | ElevenLabs v2.5 |
| Audiobook narration | ElevenLabs v2.5 or XTTS v2 + fine-tune |
| Low-resource language | Train VITS on 5–20 h target-lang data |
| Expressive / emotion tags | ElevenLabs v2.5 or StyleTTS 2 fine-tune |

| 场景 | 选择 |
|------|------|
| 实时英文语音助手 | Kokoro（CPU）或 XTTS v2（GPU） |
| 5 秒参考音频声音克隆 | F5-TTS |
| 商业角色声音 | ElevenLabs v2.5 |
| 有声书朗读 | ElevenLabs v2.5 或 XTTS v2 + 微调 |
| 低资源语言 | 在 5-20 小时目标语言数据上训练 VITS |
| 表达性 / 情感标签 | ElevenLabs v2.5 或 StyleTTS 2 微调 |

Nhà lãnh đạo nguồn mở từ năm 2026: **F5-TTS for quality, Kokoro for efficiency**Đừng tìm Tacotron trừ khi bạn là nhà sử học.

> 2026 年开源领导者:**F5-TTS 追求质量，Kokoro 追求效率**Trừ khi bạn là nhà sử học, nếu không thì không sử dụng Tacotron.



## Những bẫy

> 常见陷

- **No text normalizer.**"Dr. Smith" đọc như "Doctor" hoặc "Drive"? "2026" như "twenty twenty six" hoặc "two zero two six"?
  **没有文本归一化器。**"Dr. Smith" 读成"Doctor"还是"Drive"?"2026"读成"twenty twenty six"还是"two zero two six"?
- **OOV proper nouns.**"Ghumare" → "ghyu-mair"? gửi một mô hình từ biểu đồ đến biểu ngữ cho các token không rõ.
  **OOV 专有名词。**"Ghumare" → "ghyu-mair"?
- **Clipping.**Nguồn phát ra của Vocoder hiếm khi clip, nhưng sự không phù hợp quy mô mel khi suy luận có thể vượt quá ± 1.0.`np.clip(wav, -1, 1)`- Tôi không biết.
  **削波。**音码器输出 rất ít cỡ, nhưng trong khi được đề xuất Mel 缩放不匹配可能超出 ± 1.0──始终使用 `np.clip(wav, -1, 1)`
- **Sample-rate mismatch.**Kokoro phát ra 24 kHz; đường ống dẫn dòng chảy của bạn mong đợi 16 kHz → lấy mẫu lại hoặc nhận được danh hiệu.
  **采样率不匹配。**Kokoro 输出 24 kHz; 你的下游流水线期望 16 kHz → 重采样否则产生混叠──

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-tts-designer.md`Thiết kế một đường ống TTS cho một giọng nói, độ trễ và ngôn ngữ mục tiêu nhất định.

> 保存为 `outputs/skill-tts-designer.md`❖ Đối với một âm thanh nhất định 延迟和语言目标设计 TTS 流水线──

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`- Xây dựng một từ điển âm từ từ ngữ đồ chơi, ước tính thời gian mỗi âm và in một lịch trình "mel" giả.
   **简单。**运行 `code/main.py` Từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ từ
2. **Medium.**Lắp đặt Kokoro, tổng hợp cùng một câu với giọng nói `af_bella`và `am_adam`So sánh thời gian âm thanh và chất lượng chủ quan.
   **中等。** 安装 Kokoro, dùng `af_bella`和 `am_adam`音合成同一句话──比较音频时长和主观质量──
3. **Hard.**Hãy ghi lại một đoạn video tham chiếu 5 giây của chính mình, sử dụng F5-TTS để nhân bản nó, báo cáo SECS giữa tham chiếu và đầu ra nhân bản.
   **困难。**录制一段 5秒的自已的参考音频──使用 F5-TTS 克隆──报告参考与克隆输出之间的SECS──

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Phoneme | Sound unit | Abstract sound class; 39 in English (ARPABet). |
| Duration predictor | How long each phoneme lasts | Non-AR model output; integer frames per phoneme. |
| Vocoder | Mel → waveform | Neural net mapping mel-spec to raw samples. |
| HiFi-GAN | Standard vocoder | GAN-based; dominant 2020–2024. |
| MOS | Subjective quality | 1–5 mean opinion score from human raters. |
| SECS | Voice-clone metric | Cosine similarity between target and output speaker embedding. |
| F5-TTS | 2024 open-source SOTA | Flow-matching diffusion; zero-shot cloning. |
| Kokoro | CPU English leader | 82M-param model, Apache 2.0. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 音素 | 声音单位 | 抽象声音类别；英文有 39 个（ARPABet）。 |
| 时长预测器 | 每个音素持续多久 | 非自回归模型输出；每个音素的整数帧数。 |
| 声码器 | Mel → 波形 | 将 mel 频谱映射为原始采样的神经网络。 |
| HiFi-GAN | 标准声码器 | 基于 GAN；2020-2024 年主导。 |
| MOS | 主观质量 | 人工评分员的 1-5 平均意见分。 |
| SECS | 声音克隆指标 | 目标与输出说话人嵌入之间的余弦相似度。 |
| F5-TTS | 2024 开源 SOTA | 流匹配扩散；零样本克隆。 |
| Kokoro | CPU 英文领导者 | 8200 万参数模型，Apache 2.0。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Shen et al. (2017). Tacotron 2](https://arxiv.org/abs/1712.05884) đường cơ sở của seq2seq.
  Shen 等 (2017). Tacotron 2seq2seq 基线。
- [Kim, Kong, Son (2021). VITS](https://arxiv.org/abs/2106.06103) dựa trên dòng chảy từ đầu đến cuối.
  Kim, Kong, Son (2021). VITS端到端基于流的模型──
- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) SOTA mã nguồn mở hiện tại.
  Chen 等 (2024). F5-TTS 当前开源SOTA。
- [Kong, Kim, Bae (2020). HiFi-GAN](https://arxiv.org/abs/2010.05646) Vocoder vẫn được đưa vào năm 2026.
  Kong, Kim, Bae (2020). HiFi-GAN2026 năm vẫn còn trong sử dụng
- [Kokoro-82M on HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M) 2024 TTS tiếng Anh thân thiện với CPU.
  Kokoro-82M 在 HuggingFace 上2024 年 CPU 友好的英文 TTS──

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

