# Whisper  Kiến trúc & Fine-Tuning  Whisper  架构与微调

> Whisper là một bộ mã hóa-tử toán biến đổi cửa sổ 30 giây, được đào tạo trên 680k giờ của các cặp âm thanh văn bản đa ngôn ngữ bị giám sát kém.

> **【中文解读】**Whisper là một bộ chuyển đổi trong 30 giây, trong hơn 680.000 giờ, trong hơn 2026 năm.

> **【拓展：Whisper 的生态】**Whisper 衍生了 Whisper.cpp(本地部署)、Faster-Whisper(CTtranslate2 加速)、WhisperX(词级时间)、Bloomsbury(实时流式)等工具链,是语音识别工业部署的事实标准──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 5 · 10 (Attention), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 04（ASR），阶段 5 · 10（注意力机制），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Whisper, được phát hành bởi OpenAI vào tháng 9 năm 2022, là mô hình ASR đầu tiên được xuất khẩu như một hàng hóa: dán âm thanh, nhận văn bản, 99 ngôn ngữ, mạnh mẽ với tiếng ồn, chạy trên máy tính xách tay. Đến năm 2024 OpenAI đã xuất khẩu các biến thể Large-v3 và Turbo; đến năm 2026, Whisper là cơ sở mặc định cho mọi thứ từ bản sao podcast đến trợ lý giọng nói đến phụ đề YouTube.

> Whisper được công bố bởi OpenAI vào tháng 9 năm 2022, là mô hình ASR đầu tiên được công bố như một sản phẩm chung: dán âm thanh, lấy văn bản, 99 ngôn ngữ, chống tiếng ồn, có thể chạy trên sổ cái. Đến năm 2024, OpenAI đã công bố Large-v3 và Turbo 变体; đến năm 2026, Whisper là từ người phát hành chuyển tải lên trợ lý tiếng nói đến YouTube 字幕 và tất cả các cảnh tượng của các cơ sở cố định.

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Nhưng Whisper không phải là một đường ống dẫn mà bạn có thể đối xử như một hộp đen mãi mãi.

> Nhưng thì thầm không phải là có thể mãi mãi được sử dụng trong hộp đen dòng nước.

1. Cái gì đó thực sự là bên trong.
   Nó là cấu trúc bên trong.
2. Làm thế nào để cung cấp nó chunked, streaming, hoặc hình thức dài âm thanh chính xác.
   Làm thế nào để chính xác phân chia nó 块、流式或长音频输入──
3. Khi nào và làm thế nào để điều chỉnh.
   何時微调以及如何微调──

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


## Khái niệm cốt lõi

![Whisper encoder-decoder, tasks, chunked inference, fine-tune](../assets/whisper.svg)

**Architecture.**Bộ mã hóa-tử toán biến đổi tiêu chuẩn.

> **架构。**标准 Transformer 编码器-解码器。

- Nhập: 30 giây log-mel spectrogram, 80 mels, 10 ms hop → 3000 khung hình. clip ngắn hơn là không đệm, clip dài hơn là mảnh.
  输入30秒 log-mail 频谱图,80 mels,10 ms 步长 → 3000 ──短片段零填充,长片段分块──
- Mã hóa: con-downsample (phases 2) + `N`Các khối biến đổi. cho V3 lớn: 32 lớp, 1280 độ sâu, 20 đầu.
  编码器:卷积下采样(步幅 2) + `N`个 Transformer 块──Large-v3:32 层,1280 维,20 头──
- - Thử giải mã:`N`khối biến đổi với tự-attn nguyên nhân + giao tiếp với đầu ra mã hóa. cùng kích thước với mã hóa.
  解码器:`N`个带因果自注意力 + đối với bộ máy lập trình đầu ra chuyển đổi chú ý khối ⋅与 bộ máy lập trình cùng lớn ⋅
- Kết quả: BPE token trên một từ ngữ 51,865 token.
  输出:51,865 token 词表上的 BPE token──

Large-v3 có param 1.55B. Turbo sử dụng một decoder 4 lớp (từ 32), cắt độ trễ 8x với một hit WER < 1%.

> Lớn v3 có 15,5 tỷ参数──Turbo sử dụng 4 tầng giải mã器( từ 32 tầng giảm), chậm giảm 8 lần, WER 损失不到1%──

**The prompt format.**Whisper là một mô hình đa nhiệm được điều khiển bởi các token đặc biệt trong lệnh giải mã:

> **提示格式。**Whisper là một mô hình đa nhiệm, thông qua mã hóa chỉ số đặc biệt trong gợi ý để kiểm soát:

```
<|startoftranscript|><|en|><|transcribe|><|notimestamps|> Hello world.<|endoftext|>
```

- `<|en|>` thẻ ngôn ngữ; buộc hành vi dịch-về-tác giả.
  `<|en|>` 语言标签;强制翻译或转录行为。
- `<|transcribe|>`hoặc `<|translate|>` dịch xuất phát tiếng Anh từ bất kỳ ngôn ngữ nhập, hoặc từ ngữ.
  `<|transcribe|>`Hoặc`<|translate|>` Từ bất kỳ ngôn ngữ nào输入翻译为英文输出,或逐字转录──
- `<|notimestamps|>` bỏ qua các dấu thời gian ở mức từ (quá hơn).
  `<|notimestamps|>` 跳过词级时间(更快)

Các prompt là những gì cho phép một mô hình thực hiện nhiều nhiệm vụ. Thay đổi `<|en|>`đến`<|fr|>`và nó viết lại tiếng Pháp.

> 提示 là để một mô hình hoàn thành nhiều nhiệm vụ.`<|en|>`改为 `<|fr|>`Về chuyển thành tiếng Pháp.

**30-second window.**Mọi thứ được gắn vào 30 giây. Các clip dài hơn cần phải được chia nhỏ; các clip ngắn hơn được đệm. Windows không được phát trực tuyến bản địa  đó là lý do tại sao WhisperX, Whisper-Streaming và faster-whisper tồn tại.

> **30 秒窗口。**Tất cả đều được chuẩn bị trong 30 giây. Chuyện âm thanh dài hơn cần phân đoạn; Chuyện âm thanh ngắn hơn cần phải được lấp đầy.

**Log-mel normalization.** `(log_mel - mean) / std`nơi số liệu thống kê đến từ tập thể huấn luyện của Whisper.`whisper.audio.log_mel_spectrogram`), không `librosa.feature.melspectrogram`- Tôi không biết.

> **Log-mel 归一化。** `(log_mel - mean) / std`, trong đó số lượng thống kê đến từ Whisper  tự huấn luyện语料──你*必须* sử dụng Whisper 的预处理(`whisper.audio.log_mel_spectrogram`), thay vì `librosa.feature.melspectrogram`

### Các biến thể vào năm 2026

> ### Sự biến đổi năm 2026

| Variant | Params | Latency (A100) | WER (LibriSpeech-clean) |
|---------|--------|----------------|------------------------|
| Tiny | 39M | 1× realtime | 5.4% |
| Base | 74M | 1× | 4.1% |
| Small | 244M | 1× | 3.0% |
| Medium | 769M | 1× | 2.7% |
| Large-v3 | 1.55B | 2× | 1.8% |
| Large-v3-turbo | 809M | 8× | 1.58% |
| Whisper-Streaming (2024) | 1.55B | streaming | 2.0% |

| 变体 | 参数量 | 延迟（A100） | WER（LibriSpeech-clean） |
|------|--------|--------------|-------------------------|
| Tiny | 3900 万 | 1× 实时 | 5.4% |
| Base | 7400 万 | 1× | 4.1% |
| Small | 2.44 亿 | 1× | 3.0% |
| Medium | 7.69 亿 | 1× | 2.7% |
| Large-v3 | 15.5 亿 | 2× | 1.8% |
| Large-v3-turbo | 8.09 亿 | 8× | 1.58% |
| Whisper-Streaming（2024） | 15.5 亿 | 流式 | 2.0% |

### Định nghĩa tinh tế

> ### 微调

Phòng làm việc theo quy định trong năm 2026:

> Quy trình tiêu chuẩn năm 2026:

1. Thu thập 10100 giờ âm thanh miền mục tiêu với bản ghi được sắp xếp.
   收集 10-100 小时目标领域的音频及对应转录文本──
2. Đi chạy`transformers.Seq2SeqTrainer`với `generate_with_loss`gọi lại.
   Sử dụng `transformers.Seq2SeqTrainer`和 `generate_with_loss`回调运行训练──
3. Tỷ lệ hiệu quả tham số: LoRA `q_proj`- `k_proj`- `v_proj`của các lớp chú ý làm giảm bộ nhớ GPU 4x với < 0,3 WER chi phí.
   参数高效: trong tập trung `q_proj``k_proj``v_proj`上使用 LoRA,GPU 内存降低 4 倍,WER 损失 <0.3。
4. Đóng băng bộ mã hóa nếu bạn có < 10 giờ. Chỉ điều chỉnh bộ giải mã.
   Nếu dữ liệu không đủ 10 giờ thì chỉ cần điều chỉnh bộ xử lý bộ xử lý bộ.
5. Sử dụng tokeniser của Whisper và định dạng prompt; không bao giờ trao đổi tokeniser.
   Sử dụng Whisper  tự mình tokenizer 和提示格式;永远不要替换 tokenizer──

Kết quả của cộng đồng: điều chỉnh tinh tế Mức độ trung bình trên 20 giờ của lệnh y tế giảm WER từ 12% đến 4,5% trên từ vựng y tế.

> 社区结果: trong 20 小时医疗口述上微调 Medium,医疗词汇 WER từ 12% 降至 4.5%

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.



## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
sp-asr-attention
```

## Hãy xây dựng nó

### Bước 1: chạy Whisper ra khỏi hộp

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe(
    "clip.wav",
    language="en",
    task="transcribe",
    temperature=0.0,
    condition_on_previous_text=False,  # prevents runaway repetition
)
print(result["text"])
for seg in result["segments"]:
    print(f"[{seg['start']:.2f}–{seg['end']:.2f}] {seg['text']}")
```

Các lỗi mặc định chính bạn nên luôn bỏ qua: `temperature=0.0`(chọn mẫu các mặc định đến 0.0 → 0.2 → 0.4 ... chuỗi quay trở lại), `condition_on_previous_text=False`(đang ngăn ngừa vấn đề ảo giác ngập ngập), và`no_speech_threshold=0.6`(khám phá âm thầm).

> Bạn nên luôn bao gồm các giá trị ẩn chính:`temperature=0.0`(采样默认为 0.0 → 0.2 → 0.4 ... 回退链)`condition_on_previous_text=False`(để ngăn chặn các vấn đề liên quan) và`no_speech_threshold=0.6`(静音检测)

### Bước 2: hình dạng dài bị cắt

```python
# whisperx is the 2026 reference for long-form with word-level timestamps
import whisperx
model = whisperx.load_model("large-v3-turbo", device="cuda", compute_type="float16")
segments = model.transcribe("1hour.mp3", batch_size=16, chunk_size=30)
```

WhisperX thêm (1) Silero VAD gating, (2) Word level alignment thông qua wav2vec 2.0, (3) nhật ký thông qua `pyannote.audio`- Chiếc ngựa lao động năm 2026 cho việc chuyển bản sản xuất.

> WhisperX 添加了 (1) Silero VAD 门控,(2) 通过 wav2vec 2.0 实现词级对齐,(3) 通过 `pyannote.audio`实现说话人分离──2026年生产转录的主力工具──

### Bước 3: Hoạt động với LoRA

```python
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from peft import LoraConfig, get_peft_model

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3-turbo")
lora = LoraConfig(
    r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1, bias="none", task_type="SEQ_2_SEQ_LM",
)
model = get_peft_model(model, lora)
# model.print_trainable_parameters()  -> ~3M trainable / 809M total
```

Sau đó là vòng tròn huấn luyện viên tiêu chuẩn, kiểm tra mỗi 1000 bước, đánh giá WER khi bị kéo dài.

> Sau đó, các tiêu chuẩn của Trainer  tập trung vòng lặp.

### Bước 4: kiểm tra những gì mỗi lớp học được

```python
# Grab cross-attention weights during decode to see what the decoder attends to.
with torch.inference_mode():
    out = model.generate(
        input_features=features,
        return_dict_in_generate=True,
        output_attentions=True,
    )
# out.cross_attentions: layer × head × step × src_len
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


Hình ảnh với một heatmap  bạn sẽ thấy sự sắp xếp đường chọc khi các bước decoder quét qua khung encoder.

> Sử dụng nhiệt lực hình ảnh hóa bạn sẽ thấy giải mã bước vào scan 编码器时的对角线对齐那条对角线就是 Whisper的词时间概念




> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

Số 2026:

> 2026 năm của công nghệ:

| Situation | Pick |
|-----------|------|
| General English, offline | Large-v3-turbo via `whisperx` |
| Mobile / edge | Whisper-Tiny quantized (int8) or Moonshine |
| Multilingual long-form | Large-v3 via `whisperx` + diarization |
| Low-resource language | Fine-tune Medium or Turbo with LoRA |
| Streaming (2 s latency) | Whisper-Streaming or Parakeet-TDT |
| Word-level timestamps | WhisperX (forced alignment via wav2vec 2.0) |

| 场景 | 选择 |
|------|------|
| 通用英文、离线 | 通过 `whisperx` 使用 Large-v3-turbo |
| 移动端/边缘设备 | 量化 Whisper-Tiny（int8）或 Moonshine |
| 多语言长音频 | 通过 `whisperx` 使用 Large-v3 + 说话人分离 |
| 低资源语言 | 用 LoRA 微调 Medium 或 Turbo |
| 流式（2 秒延迟） | Whisper-Streaming 或 Parakeet-TDT |
| 词级时间戳 | WhisperX（通过 wav2vec 2.0 强制对齐） |

`faster-whisper`(CTranslate2 backend) là thời gian chạy suy luận CPU + GPU nhanh nhất vào năm 2026  4x nhanh hơn vanilla với đầu ra giống nhau.

> `faster-whisper`(CTranslate2 后端) là CPU + GPU nhanh nhất năm 2026 推理运行时比原版快4倍,输出 hoàn toàn giống nhau.



## Những bẫy vẫn còn tồn tại vào năm 2026

> Năm 2026 vẫn còn trong bẫy tội phạm

- **Hallucinated text on silence.**Whisper được đào tạo trên tiêu đề bao gồm "Cảm ơn đã xem!", "Đăng ký!", lời bài hát.
  **静音上的幻觉文本。**Whisper 在字幕数据上训练,会包含"Cảm ơn đã xem!"、"Đăng ký!"、歌词──调用前务必用 VAD 过──
- **`condition_on_previous_text` cascade.**Một ảo giác làm ô nhiễm các cửa sổ sau đó.`False`trừ khi bạn cần sự thịnh vượng giữa các mảnh.
  **`condition_on_previous_text` 级联。**Một lần thấy được một cái cửa sổ sau khi bị ô nhiễm.`False`
- **Short-clip padding.**Một clip 2 giây được đệm đến 30 giây có thể ảo giác trong sự im lặng sau đó.`pad=False`hay VAD-gate.
  **短片段填充。**2 giây đoạn phim được lấp đầy đến 30 giây có thể xảy ra cảm giác tĩnh lặng ở cuối bộ.`pad=False`Hoặc là VAD 过──
- **Wrong mel stats.**Sử dụng mels của librosa thay vì Whisper tạo ra kết quả gần như ngẫu nhiên.`whisper.audio.log_mel_spectrogram`- Tôi không biết.
  **错误的 mel 统计量。**Sử dụng các bản thu thập thư viện thay vì Phầmầm sẽ xuất hiện gần như bất cứ khi nào.`whisper.audio.log_mel_spectrogram`

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-whisper-tuner.md`Thiết kế một đường ống dẫn suy luận hoặc điều chỉnh tinh tế của Whisper cho một miền nhất định.

> 保存为 `outputs/skill-whisper-tuner.md`❖ Đối với một lĩnh vực nhất định thiết kế 微调或推理流水线──

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`Nó tạo ra một biểu tượng kiểu Whisper, tính toán các ngân sách hình dạng được giải mã và in lịch trình phần cho một clip 10 phút.
   **简单。**运行 `code/main.py` Nó cho phép các biểu tượng của Whisper 风格 được chuyển đổi, tính toán hình dạng ngân sách, và in 10 phút 音频的分块计划
2. **Medium.**Thiết lập `faster-whisper`, sao chép một podcast 10 phút, so sánh WER với một bản sao con người.`language="auto"`vs buộc `language="en"`- Tôi không biết.
   **中等。**                                          `faster-whisper`, chuyển âm 10 phút播客, với chuyển âm nhân tạo so với WER.`language="auto"`Với sự bắt buộc`language="en"`
3. **Hard.**Sử dụng HF `datasets`, chọn một ngôn ngữ mà Whisper đấu tranh với (ví dụ, Urdu), điều chỉnh Medium với LoRA trong 2 thời kỳ trong 2 giờ, và báo cáo WER delta.
   **困难。**Sử dụng HF `datasets`, chọn một tiếng nói khó khăn (如乌尔都语), trong 2 小时数据上使用 LoRA 微调 平均 2 个时代,报告 WER 差值──

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 30-sec window | Whisper's limit | Hard input cap; chunk longer audio. |
| SOT | Start-of-transcript | `<\|startoftranscript\|>` kicks off the decoder prompt. |
| Timestamps token | Temporal alignment | Every 0.02 s offset is a special token in the 51k vocab. |
| Turbo | The fast variant | 4-decoder layers, 8× faster, <1% WER regression. |
| WhisperX | The long-form wrapper | VAD + Whisper + wav2vec alignment + diarization. |
| LoRA fine-tune | Efficient tuning | Add low-rank adapters to attention; train ~0.3% of params. |
| Hallucination | The silent failure | Whisper produces fluent English from noise/silence. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 30 秒窗口 | Whisper 的限制 | 硬性输入上限；更长音频需分块。 |
| SOT | 转录开始 | `<\|startoftranscript\|>` 启动解码器提示。 |
| 时间戳 token | 时间对齐 | 每 0.02 秒偏移是 51k 词表中的特殊 token。 |
| Turbo | 快速变体 | 4 层解码器，快 8 倍，WER 回退 <1%。 |
| WhisperX | 长音频封装 | VAD + Whisper + wav2vec 对齐 + 说话人分离。 |
| LoRA 微调 | 高效调优 | 在注意力层添加低秩适配器；仅训练约 0.3% 参数。 |
| 幻觉 | 静默失败 | Whisper 从噪声/静音中产生流畅的英文。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Radford et al. (2022). Whisper paper](https://arxiv.org/abs/2212.04356) kiến trúc và công thức đào tạo ban đầu.
  Radford 等 (2022). Whisper 论文原始架构和训练方案──
- [OpenAI (2024). Whisper Large-v3-turbo release](https://github.com/openai/whisper/discussions/2363) 4 lớp decoder, tăng tốc 8x.
  OpenAI (2024). Whisper Large-v3-turbo 发布4 层解码器,8 倍加速──
- [Bain et al. (2023). WhisperX](https://arxiv.org/abs/2303.00747) hình dạng dài, chữ phù hợp, nhật ký.
  Bain 等 (2023). WhisperX长音频、词级对齐、说话人分离──
- [Systran — faster-whisper repo](https://github.com/SYSTRAN/faster-whisper) CTranslate2 hỗ trợ, nhanh hơn 4x.
  Hệ thống nhanh hơn thì thầm 仓库 CTranslate2 后端,快4 倍──
- [HuggingFace — Whisper fine-tune tutorial](https://huggingface.co/blog/fine-tune-whisper) LoRA truyền thống / đi bộ toàn bộ FT.
  HuggingFaceWhisper 微调教程标准 LoRA/全参数微调指南。

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

