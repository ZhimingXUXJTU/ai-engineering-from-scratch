# Music Generation  MusicGen, Stable Audio, Suno, và Licensing Earthquake  音乐生成  MusicGen、Stable Audio、Suno và bản quyền động đất

> Thế hệ âm nhạc năm 2026: Suno v5 và Udio v4 thống trị thương mại; MusicGen, Stable Audio Open và ACE-Step dẫn đầu nguồn mở. Vấn đề kỹ thuật chủ yếu được giải quyết. Vấn đề pháp lý (Warner Music $ 500M giải quyết, UMG giải quyết) đã định hình lại lĩnh vực trong năm 2025-2026.

> **【中文解读】**2026 năm của sản xuất âm nhạc:Suno v5 和 Udio v4 主导商业产品;MusicGen、Stable Audio Open 和 ACE-Step 领先开源;; vấn đề kỹ thuật cơ bản giải quyết, nhưng vấn đề pháp luật(Warner Music 5 tỷ USD giải quyết案) trong năm 2025-2026 tái tạo lĩnh vực này;;

> **【拓展：AI 音乐的法律风暴】**Vấn đề bản quyền của AI sinh sản âm nhạc đã gây ra một trận động đất trong ngành âm nhạc.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 4 · 10 (Diffusion Models) | **前置知识:** 阶段 6 · 02（频谱图），阶段 4 · 10（扩散模型）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Text → một đoạn nhạc từ 30 giây đến 4 phút, với lời bài hát, giọng hát và cấu trúc. Ba phụ vấn đề:

> 文本 → 30 giây đến 4 phút của âm nhạc đoạn,带歌词、人声和结构──三子问题:

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

1. **Instrumental generation.**Các văn bản như "lo-fi hip-hop trống với khóa ấm áp" → âm thanh. MusicGen, Stable Audio, AudioLDM.
   **器乐生成。**像"lo-fi hip-hop trống với khóa ấm áp"这样的文本 → 音频──MusicGen、Stable Audio、AudioLDM──
2. **Song generation (with vocals + lyrics).**"Câu nhạc nhạc quốc gia về những đêm mưa ở Texas" → bài hát đầy đủ.
   **歌曲生成（带人声+歌词）。**"Câu hát quốc gia về những đêm mưa ở Texas" → 完整歌曲──Suno、Udio、YuE、ACE-Step──
3. **Conditional / controllable.**Lũ rộng clip hiện có, tái tạo cầu, đổi thể loại, tách gốc hoặc sơn.
   **条件/可控生成。**扩展现有片段、重新生成桥段、切换风格、分轨或内画──Udio's内画 + 分轨 là chức năng cần theo đuổi vào năm 2026──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Music generation: token-LM vs diffusion, the 2026 model map](../assets/music-generation.svg)

### LM token trên mã codec thần kinh

> ### 基于神经编解码代币的代币 LM

Meta's **MusicGen**(2023, MIT) và nhiều phái sinh: điều kiện trên các bản ghi văn bản / giai điệu, dự đoán tự động các token EnCodec (32 kHz, 4 cuốn codebook), giải mã với EnCodec. 300M - 3.3B param. Nguyên tắc cơ bản mạnh; đấu tranh vượt quá 30 giây.

> Meta của **MusicGen**(2023, MIT) và nhiều phái sinh:以文本/旋律嵌入为条件,自归预测 EnCodec token(32 kHz,4 个码本), sử dụng EnCodec 解码──3亿到33亿参数──强基线; hơn 30秒效果下降──

**ACE-Step**(có nguồn mở, 4B XL phát hành tháng 4 năm 2026) mở rộng điều này cho thế hệ đầy đủ bài hát theo điều kiện lyric.

> **ACE-Step**(Open Source, 4 tháng 4 năm 2026 版本 XL 版本) sẽ mở rộng sang toàn曲歌词条件生成──开源社区最接近Suno的产品──

### Sự pha trộn trên các chất tan chảy hoặc ẩn

> ### 基于 Mel hoặc tiềm biến số

**Stable Audio (2023)**và **Stable Audio Open (2024)**: phát sóng ẩn trên âm thanh nén. xuất sắc trong vòng lặp, thiết kế âm thanh, kết cấu môi trường. Không tốt cho các bài hát đầy đủ cấu trúc.

> **Stable Audio（2023）**和 **Stable Audio Open（2024）**: 压缩音频上的潜变量扩散──擅长循环、声音设计、氛围质感──不太擅长结构化完整歌曲──

**AudioLDM / AudioLDM2**: văn bản-đâu âm thanh thông qua truyền tải ẩn hình kiểu T2I, tổng quát đến âm nhạc, hiệu ứng âm thanh, nói chuyện.

> **AudioLDM / AudioLDM2**Thông qua T2I 风格的潜变量扩散进行文本到音频生成,泛化到音乐、音效、语音──

### Hybrid (sản xuất)  Suno, Udio, Lyria

> ### 混合(生产)  Suno、Udio、Lyria

Vòng đóng. Có lẽ là codec AR LM + vocoder dựa trên sự pha trộn với đầu giọng / trống / giai điệu chuyên dụng. Suno v5 (2026) là nhà lãnh đạo chất lượng ELO 1293. Udio v4 thêm inpainting + phân tách gốc (bass, trống, giọng hát tải về riêng biệt).

> 闭源权重──可能是 AR 编解码 LM + 基于扩散的声码器,配有专门语音/鼓/旋律头──Suno v5(2026) là ELO 1293 质量领先者──Udio v4 增加内画 + 分轨(贝斯、鼓、人声分别下载)──

### Đánh giá

> ### 评估

- **FAD (Fréchet Audio Distance).**Khoảng cách cấp độ nhúng giữa phân phối âm thanh được tạo vs thực sử dụng các tính năng VGGish hoặc PANN.
  **FAD（Fréchet 音频距离）。**Sử dụng VGGish hoặc PANNs đặc trưng của tạo vs 真实音频分布的嵌入级距离──越低越好──MusicGen nhỏ:MusicCaps 上 4.5 FAD;SOTA 约 3.0──
- **Musicality (subjective).**Suno v5 ELO 1293 dẫn.
  **音乐性（主观）。**Nhân loại Ưu tiên: Suno v5 ELO 1293 领先:
- **Text-audio alignment.**CLAP điểm giữa prompt và output.
  **文本-音频对齐。**CLAP chia số giữa 提示 và输出
- **Musicality artifacts.**Chuyển đổi ngoài nhịp, chuyển động từ ngữ giọng, mất cấu trúc sau 30 giây.
  **音乐性伪影。**跑拍过渡、人声短语漂移、 hơn 30 giây sau cấu trúc bị mất đi。

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.



## Bản đồ mô hình 2026

> 2026 năm模型地图

| Model | Params | Length | Vocals | License |
|-------|--------|--------|--------|---------|
| MusicGen-large | 3.3B | 30 s | no | MIT |
| Stable Audio Open | 1.2B | 47 s | no | Stability non-commercial |
| ACE-Step XL (Apr 2026) | 4B | > 2 min | yes | Apache-2.0 |
| YuE | 7B | > 2 min | yes, multilingual | Apache-2.0 |
| Suno v5 (closed) | ? | 4 min | yes, ELO 1293 | commercial |
| Udio v4 (closed) | ? | 4 min | yes + stems | commercial |
| Google Lyria 3 (closed) | ? | real-time | yes | commercial |
| MiniMax Music 2.5 | ? | 4 min | yes | commercial API |

| 模型 | 参数量 | 时长 | 人声 | 许可 |
|------|--------|------|------|------|
| MusicGen-large | 33 亿 | 30 秒 | 无 | MIT |
| Stable Audio Open | 12 亿 | 47 秒 | 无 | Stability 非商业 |
| ACE-Step XL（2026.04） | 40 亿 | > 2 分钟 | 有 | Apache-2.0 |
| YuE | 70 亿 | > 2 分钟 | 有，多语言 | Apache-2.0 |
| Suno v5（闭源） | ? | 4 分钟 | 有，ELO 1293 | 商业 |
| Udio v4（闭源） | ? | 4 分钟 | 有 + 分轨 | 商业 |
| Google Lyria 3（闭源） | ? | 实时 | 有 | 商业 |
| MiniMax Music 2.5 | ? | 4 分钟 | 有 | 商业 API |

## Tâm lý pháp lý (2025-2026)

> ## 法律环境(2025-2026)

- **Warner Music vs Suno settlement.**500 triệu đô la. WMG hiện đang giám sát sự giống AI, quyền âm nhạc và các bài hát được tạo bởi người dùng trên Suno.
  **Warner Music 诉 Suno 和解。**500 tỷ USD. WMG hiện có quyền giám sát AI tương tự của Suno.
- **EU AI Act**+ **California SB 942**: Âm nhạc được tạo ra bởi AI phải được tiết lộ.
  **EU AI 法案**+ **加利福尼亚 SB 942**Ai sinh ra của âm nhạc phải được tiết lộ.
- **Riffusion / MusicGen**theo MIT không có hành lý tuân thủ nhưng cũng không có giọng hát thương mại.
  **Riffusion / MusicGen**Trong khi đó, công ty này cũng không có công ty nào.

Các mô hình an toàn để tàu:

> Mô hình phát hành an toàn:

1. Tạo chỉ công cụ (MusicGen, Stable Audio Open, MIT/CC0 đầu ra).
   仅生成器乐(MusicGen、Stable Audio Open、MIT/CC0 输出)
2. Sử dụng API thương mại (Suno, Udio, ElevenLabs Music) với giấy phép mỗi thế hệ.
   Sử dụng với mỗi lần tạo giấy phép API thương mại (Suno, Audio, ElevenLabs Music)
3. Đường sắt trên danh mục sở hữu hoặc được cấp phép (những doanh nghiệp hầu hết kết thúc ở đây).
   Trong tự có hoặc được ủy quyền trên danh sách đào tạo (trong phần lớn các doanh nghiệp cuối cùng đi đến bước này)
4. Tag các thế hệ với dấu nước + siêu dữ liệu.
   用水印 + 元数据标记生成内容──

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――


## Hãy xây dựng nó.
```figure
sp-codec-tokens
```

## Hãy xây dựng nó

### Bước 1: tạo bằng MusicGen

```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained("facebook/musicgen-small")
model.set_generation_params(duration=10)
wav = model.generate(["upbeat synthwave with driving drums, 128 BPM"])
torchaudio.save("out.wav", wav[0].cpu(), 32000)
```

Ba kích thước: `small`(300M, nhanh),`medium`(1.5B), `large`(3.3B) Tự nhỏ là đủ để "làm ý tưởng hạ cánh".

> 3 cái lớn:`small`(3 tỷ, nhanh chóng)`medium`(15 tỷ)`large`(33 tỷ)`small`足以验证" ý tưởng có thể thực hiện được"

### Bước 2: Điều kiện âm thanh

```python
melody, sr = torchaudio.load("humming.wav")
wav = model.generate_with_chroma(
    ["jazz piano cover"],
    melody.squeeze(),
    sr,
)
```

MusicGen-melody lấy một sắc tố và bảo tồn giai điệu trong khi thay đổi timbre. hữu ích cho "giữ cho tôi giai điệu này như một quartet dây".

> MusicGen-melody  chấp nhận色度图 và trao đổi音色时保留旋律──适用于"把这个旋律转成弦乐四重奏"──

### Bước 3: Đánh giá FAD

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()

fad.get_fad_score("generated_folder/", "reference_folder/")
```

Xét khoảng cách tích hợp VGGish. hữu ích cho các bài kiểm tra hồi quy cấp thể loại; không thay thế cho người nghe.

> 计算 VGGish 嵌入距离;;适用于流派级归归测试; không thể thay thế người nghe;;

### Bước 4: bổ sung vào dòng công việc LLM- nhạc

Kết hợp với những ý tưởng từ Bài học 7-8:

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


```python
prompt = "Write a 30-second jazz loop. Describe the drums, bass, and piano voicing."
description = llm.complete(prompt)
music = musicgen.generate([description], duration=30)
```




> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

| Goal | Stack |
|------|-------|
| Instrumental sound design | Stable Audio Open |
| Game / adaptive music | Google Lyria RealTime (closed) |
| Full songs with vocals (commercial) | Suno v5 or Udio v4 with explicit license |
| Full songs with vocals (open) | ACE-Step XL or YuE |
| Short ad jingle | MusicGen melody-conditioned on a hummed reference |
| Music-video background | MusicGen + Stable Video Diffusion |

| 目标 | 技术栈 |
|------|--------|
| 器乐声音设计 | Stable Audio Open |
| 游戏/自适应音乐 | Google Lyria RealTime（闭源） |
| 带人声的完整歌曲（商业） | Suno v5 或 Udio v4 带明确许可 |
| 带人声的完整歌曲（开源） | ACE-Step XL 或 YuE |
| 短广告曲 | MusicGen 在哼唱参考上的旋律条件 |
| 音乐视频背景 | MusicGen + Stable Video Diffusion |



## Những bẫy vẫn còn tồn tại vào năm 2026

> Năm 2026 vẫn còn trong bẫy tội phạm

- **Copyright-laundering prompts.**"Song in the style of Taylor Swift"  Suno / Audio quảng cáo lọc những cái này bây giờ, mô hình mở không.
  **版权洗钱提示。**"Câu hát theo phong cách của Taylor Swift" thương mại Suno/Udio 现在会过这些,开源模型不会――添加你自己的过列表――
- **Repetition / drift past 30 s.**Các mô hình AR loop. Crossfade nhiều thế hệ, hoặc sử dụng ACE-Step để kết hợp cấu trúc.
  **超过 30 秒的重复/漂移。**AR 模型会循环──交叉淡进多个生成,或使用 ACE-Step 保持结构一致性──
- **Tempo drift.**Các mô hình đi xa BPM. Sử dụng thẻ BPM trong prompt và post-filter với librosa `beat_track`- Tôi không biết.
  **节奏漂移。**模型偏离 BPM──在提示中使用 BPM 标签并使用图书馆的 `beat_track`后过──
- **Vocal intelligibility.**Suno là một bài hát tuyệt vời; các mô hình mở thường bị nhạt về từ ngữ.
  **人声清晰度。**Suno biểu hiện xuất sắc; open source模型的歌词经常模糊──如果歌词重要,使用商业API或微调──
- **Mono output.**Các mô hình mở tạo ra mono hoặc giả stereo. nâng cấp với một tái thiết stereo thích hợp (ví dụ, sự pha trộn stereo của Cartesia).
  **单声道输出。**开源模型生成单声道或假立体声――使用合适的立体声重建升级――

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-music-designer.md`. Chọn mô hình, chiến lược cấp phép, kế hoạch chiều dài / cấu trúc và tiết lộ metadata cho việc triển khai nhạc-gen.

> 保存为 `outputs/skill-music-designer.md`                                                                                                                                                                                                                                                                         

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`Nó tạo ra một tiến trình hợp âm "tạo ra" + mô hình trống như các biểu tượng ASCII  một phim hoạt hình nhạc-gen.
   **简单。**运行 `code/main.py`◊ Nó được thực hiện bằng ASCII 符号生成"生成式"和弦 + 鼓点一个音乐生成的卡通── có thể được phát bằng máy chiếu MIDI 染器──
2. **Medium.**Thiết lập `audiocraft`, tạo clip 10 giây trên 4 genre prompt với MusicGen-small, đo FAD với một tập hợp thể loại tham chiếu.
   **中等。**                                          `audiocraft`, sử dụng MusicGen-small trong 4 流派提示生成 10 秒片段,对照参考流派集测量 FAD──
3. **Hard.**Sử dụng ACE-Step (hoặc MusicGen-melody), tạo ba biến thể của cùng một giai điệu với các lời nhắc timbre khác nhau.
   **困难。**Sử dụng ACE-Step (hoặc MusicGen-melody), sử dụng các âm sắc khác nhau để tạo ra ba biến thể của cùng một旋律.

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| FAD | Audio FID | Fréchet distance between embedding distributions of real vs generated. |
| Chromagram | Melody as pitches | 12-dim per-frame vector; input to melody conditioning. |
| Stems | Instrument tracks | Separated bass / drums / vocals / melody as WAV. |
| Inpainting | Regen a section | Mask a time window; model regenerates just that. |
| CLAP | Text-audio CLIP | Contrastive audio-text embedding; eval text-audio alignment. |
| EnCodec | Music codec | Meta's neural codec used by MusicGen; 32 kHz, 4 codebooks. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| FAD | 音频 FID | 真实 vs 生成嵌入分布之间的 Fréchet 距离。 |
| 色度图 | 旋律即音高 | 12 维逐帧向量；旋律条件的输入。 |
| 分轨 | 乐器轨道 | 分离的贝斯/鼓/人声/旋律 WAV。 |
| 内画 | 重生成一段 | 遮蔽时间窗口；模型只重生成那部分。 |
| CLAP | 文本-音频 CLIP | 对比音频-文本嵌入；评估文本-音频对齐。 |
| EnCodec | 音乐编解码器 | Meta 的神经编解码器，MusicGen 使用；32 kHz，4 个码本。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Copet et al. (2023). MusicGen](https://arxiv.org/abs/2306.05284) chỉ số chuẩn tự động mở.
  Copet 等 (2023). MusicGen开源自归基准──
- [Evans et al. (2024). Stable Audio Open](https://arxiv.org/abs/2407.14358) thiết kế âm thanh mặc định.
  Evans 等 (2024). Stable Audio Open声音设计默认选择──
- [ACE-Step](https://github.com/ace-step/ACE-Step) mở máy phát điện 4B đầy nhạc, tháng 4 năm 2026.
  ACE-Step开源 40 亿参数全曲生成器,2026 年 4 月。
- [Suno v5 platform docs](https://suno.com) nhà lãnh đạo chất lượng thương mại.
  Suno v5 平台文档商业质量领先者──
- [AudioLDM2](https://arxiv.org/abs/2308.05734) Phân phối ẩn cho âm nhạc + hiệu ứng âm thanh.
  AudioLDM2音乐 + 音效的潜变量扩散──
- [WMG-Suno settlement coverage](https://www.musicbusinessworldwide.com/suno-warner-music-settlement/) Tháng 11 năm 2025 tiền lệ.
  WMG-Suno 和解报道2025 年 11 月判例。

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

