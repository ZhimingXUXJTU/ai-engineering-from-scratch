# Phân phối giọng nói & chuyển đổi giọng nói 语音克隆与语音转换

> Phân bản giọng nói đọc văn bản của bạn bằng giọng nói của người khác. Chuyển đổi giọng nói viết lại giọng nói của bạn vào tiếng nói của người khác trong khi vẫn giữ lại những gì bạn nói. Cả hai đều gắn liền với sự phân hủy tương tự: tách biệt danh tính loa khỏi nội dung.

> **【中文解读】**语音克隆 dùng tiếng nói của người khác để đọc văn bản của bạn;语音 chuyển đổi để biến tiếng nói của bạn thành tiếng nói của người khác nhưng giữ lại nội dung.

> **【拓展：语音克隆的伦理与法律】**语音克隆技术引发严重伦理和法律问题深度伪造语音欺诈、名人声音未经授权使用──2025-2026 Nhiều vụ kiện ((如 Warner Music 5 tỷ USD和解案) thúc đẩy phát triển của âm thanh thủy印 và chống giả mạo kỹ thuật──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Năm 2026, một đoạn âm thanh 5 giây là đủ để tạo ra một bản sao âm thanh chất lượng cao của bất kỳ ai với GPU tiêu dùng. ElevenLabs, F5-TTS, OpenVoice v2, VoiceBox tất cả các tàu không bắn hoặc ít bắn sao. Công nghệ là một ân phước (tải tiếp cận TTS, dubbing, tiếng nói hỗ trợ) và một vũ khí (scam cuộc gọi, deepfakes chính trị, IP trộm cắp).

> Năm 2026, một đoạn 5 giây音频就足以使用消费级 GPU高质量克隆任何人的声音──ElevenLabs、F5-TTS、OpenVoice v2、VoiceBox đều cung cấp零样本或少样本克隆──

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Hai nhiệm vụ liên quan chặt chẽ:

> Hai nhiệm vụ liên quan chặt chẽ:

- **Voice cloning (TTS-side):**văn bản + giọng nói tham chiếu 5 giây → âm thanh trong giọng nói đó.
  **声音克隆（TTS 侧）：**文本 + 5 秒参考声音 → The声音的音频──
- **Voice conversion (speech-side):**âm thanh nguồn (người A nói X) + giọng nói tham chiếu của người B → âm thanh của B nói X.
  **语音转换（语音侧）：**源音频(说话人 A 说 X) + 说话人 B 的参考声音 → B 说 X 的音频。

Cả hai đều tính toán một dạng sóng thành (container, speaker, prosody) và tái kết hợp nội dung từ một nguồn với speaker từ một nguồn khác.

> 两者都将波形分解为(内容、说话人、律) và từ một nguồn lấy nội dung với nguồn khác lại tập hợp lại người nói.

Một hạn chế quan trọng mà bạn đang phải đặt vào năm 2026:**watermarking and consent gates are legally required in the EU (AI Act, enforceable August 2026) and in California (AB 2905, effective 2025)**Đường ống của bạn phải phát ra một dấu nước không thể nghe được và từ chối các bản sao không đồng ý.

> 2026 năm bạn phải đối mặt với những điều quan trọng:**水印和同意门在 EU（AI 法案，2026 年 8 月生效）和加利福尼亚州（AB 2905，2025 年生效）是法律要求的** dòng nước của bạn phải phát ra dấu ấn vô thể nghe thấy và từ chối không đồng ý của mình 

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Voice cloning vs conversion: factorize, swap speaker, recombine](../assets/voice-cloning.svg)

**Zero-shot cloning.**Chuyển một clip 5 giây cho một mô hình đã được đào tạo trên hàng ngàn loa. Bộ mã hóa loa lập bản đồ clip cho một loa nhúng; bộ mã hóa TTS điều kiện trên nhúng cộng với văn bản.

> **零样本克隆。**Để truyền tải 5 giây âm thanh cho mô hình được đào tạo trên hàng ngàn người nói.

Được sử dụng bởi: F5-TTS (2024), YourTTS (2022), XTTS v2 (2024), OpenVoice v2 (2024).

> Người dùng:F5-TTS(2024)、YourTTS(2022)、XTTS v2(2024)、OpenVoice v2(2024)。

**Few-shot fine-tuning.**Lập lại 5-30 phút của giọng nói mục tiêu. LoRA-định chỉnh một mô hình cơ bản trong một giờ. chất lượng nhảy từ "tốt" đến "không thể phân biệt". Coqui và ElevenLabs đều hỗ trợ mô hình này; cộng đồng sử dụng nó với F5-TTS.

> **少样本微调。**录制目标声音 5-30 分钟──LoRA 微调基础模型一小时──质量 từ "还行" nhảy đến "无法区分"──Coqui 和 ElevenLabs 都支持这种模式;社区用F5-TTS实现──

**Voice conversion (VC).**Hai gia đình:

> **语音转换（VC）。**Hai gia đình:

- **Recognition-synthesis.**Động cơ ASR để lấy biểu diễn nội dung (ví dụ: hậu âm mềm, PPG), sau đó tổng hợp lại với nhúng loa mục tiêu. Năng bằng ngôn ngữ và giọng nói. Được sử dụng bởi KNN-VC (2023), Diff-HierVC (2023).
  **识别-合成。**运行类 ASR 模型提取内容表示 (如软音素后验、PPG), sau đó sử dụng mục tiêu nói话人嵌入重新合成──对语言和口音鲁棒──KNN-VC(2023)、Diff-HierVC(2023) 使用──
- **Disentanglement.**Trình tạo một bộ mã hóa tự động phân tách nội dung, loa và prosody trong không gian ẩn tại nút chai. Swap loa nhúng tại suy luận. chất lượng thấp hơn nhưng nhanh hơn. Được sử dụng bởi AutoVC (2019), biến thể VITS-VC.
  **解耦。**训练自编码器在瓶处的潜在空间中分离内容、讲话人和律──推理时交换讲话人嵌入──质量较低但更快──AutoVC(2019)、VITS-VC 变体使用──

**Neural codec-based cloning (2024+).**VALL-E, VALL-E 2, NaturalSpeech 3, VoiceBox  xử lý âm thanh như các token riêng biệt từ SoundStream / EnCodec, đào tạo mô hình tự rút hoặc phù hợp dòng chảy lớn hơn các token codec. Chất lượng tương đương với ElevenLabs trên các lời nhắc ngắn.

> **基于神经编解码器的克隆（2024+）。**VALL-E、VALL-E 2、NaturalSpeech 3、VoiceBox sẽ được xem như một biểu tượng phân tán của SoundStream/EnCodec, trong việc编解代码 token 上训练大型自归归或流匹配模型──短提示上质量可与ElevenLabs 相当──

### Một phần đạo đức, không phải là một cái nắp

> ### 伦理问题, không có lựa chọn

**Watermarking.**PerTh (Perth) và SilentCipher (2024) nhúng một ID ~ 16-32 bit vô hình trong âm thanh. tồn tại mã hóa lại, phát trực tuyến và chỉnh sửa phổ biến.

> **水印。**PerTh 和 SilentCipher(2024) được đặt trong âm thanh trong không thể nhận thức được khoảng 16-32 vị trí ID──能经受重新编码、流传输和常见编辑──生产可用开源方案──

**Consent gates.**"Tôi, Rohit, vào ngày 2026-04-22, cho phép giọng nói này cho mục đích X".

> **同意门。**Mỗi bản xuất khẩu của một quốc gia phải được ghi lại một bản ghi đồng ý có thể xác minh được.

**Detection.**AASIST, RawNet2 và Wav2Vec2-AASIST đóng vai trò là các máy dò. ASVspoof 2025 Challenge đã công bố EER 0,82,3% cho các máy dò hiện đại chống lại các sản phẩm ElevenLabs, VALL-E 2 và Bark.

> **检测。**AASIST、RawNet2 和 Wav2Vec2-AASIST 作为检测器发布──ASVspoof 2025 挑战赛发布 SOTA 检测器对ElevenLabs、VALL-E 2 和 Bark 输出 EER为0.8-2.3%──

### Số (2026)

> Số năm 2026

| Model | Zero-shot? | SECS (target sim) | WER (intel.) | Params |
|-------|-----------|--------------------|--------------|--------|
| F5-TTS | Yes | 0.72 | 2.1% | 335M |
| XTTS v2 | Yes | 0.65 | 3.5% | 470M |
| OpenVoice v2 | Yes | 0.70 | 2.8% | 220M |
| VALL-E 2 | Yes | 0.77 | 2.4% | 370M |
| VoiceBox | Yes | 0.78 | 2.1% | 330M |

| 模型 | 零样本？ | SECS（目标相似度） | WER（可懂度） | 参数量 |
|------|---------|-------------------|--------------|--------|
| F5-TTS | 是 | 0.72 | 2.1% | 3.35 亿 |
| XTTS v2 | 是 | 0.65 | 3.5% | 4.7 亿 |
| OpenVoice v2 | 是 | 0.70 | 2.8% | 2.2 亿 |
| VALL-E 2 | 是 | 0.77 | 2.4% | 3.7 亿 |
| VoiceBox | 是 | 0.78 | 2.1% | 3.3 亿 |

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――


SECS > 0,70 thường không thể phân biệt với mục tiêu đối với hầu hết người nghe.

> SECS > 0,70 đối với hầu hết khán giả thường không thể phân biệt với mục tiêu.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.



## Hãy xây dựng nó.
```figure
sp-voice-factorize
```

## Hãy xây dựng nó

### Bước 1: phân hủy với công nhận-sínhết (chỉ dùng mã demo trong main.py)

```python
def clone_pipeline(ref_audio, text, target_embedder, tts_model):
    speaker_emb = target_embedder.encode(ref_audio)
    mel = tts_model(text, speaker=speaker_emb)
    return vocoder(mel)
```

Khả năng thực hiện là rất đơn giản.`tts_model`và bộ mã hóa loa.

> 概念上简单;实现量在 `tts_model`Và nói chuyện người trong bộ máy lập trình.

### Bước 2: Klon không bắn với F5-TTS

```python
from f5_tts.api import F5TTS
tts = F5TTS()
wav = tts.infer(
    ref_file="rohit_5s.wav",
    ref_text="The quick brown fox jumps over the lazy dog.",
    gen_text="Please add milk and bread to my list.",
)
```

Bản sao tham chiếu phải phù hợp chính xác với âm thanh; sự không phù hợp phá vỡ sự sắp xếp.

> 参考转录必须与音频完全匹配; 不匹配会破坏对齐──

### Bước 3: chuyển đổi giọng nói với KNN-VC

```python
import torch
from knnvc import KNNVC  # 2023 model, https://github.com/bshall/knn-vc
vc = KNNVC.load("wavlm-base-plus")
out_wav = vc.convert(source="my_voice.wav", target_pool=["alice_1.wav", "alice_2.wav"])
```

KNN-VC chạy WavLM để trích xuất các nhúng mỗi khung cho nguồn và mục tiêu pool, sau đó thay thế mỗi khung nguồn với hàng xóm gần nhất trong hồ.

> KNN-VC 运行 WavLM 提取源和目标池的逐嵌入, sau đó sử dụng gần gũi hàng xóm trong池 thay thế mỗi nguồn──非参数化,一分钟目标语音即可工作──

### Bước 4: Nhập một dấu nước

```python
from silentcipher import SilentCipher
sc = SilentCipher(model="2024-06-01")
payload = b"consent_id:abc123;ts:1745353200"
watermarked = sc.embed(wav, sr=24000, message=payload)
detected = sc.detect(watermarked, sr=24000)   # returns payload bytes
```

~ 32 bit tải trọng hữu ích, có thể phát hiện sau khi mã hóa lại MP3 và tiếng ồn nhẹ.

> 约 32 位载荷,MP3 重编码和轻度噪音后仍可检测──

### Bước 5: Cổng đồng ý

```python
def cloned_inference(text, ref_audio, consent_record):
    assert verify_signature(consent_record), "Signed consent required"
    assert consent_record["speaker_id"] == hash_speaker(ref_audio)
    wav = tts.infer(ref_file=ref_audio, gen_text=text)
    wav = watermark(wav, payload=consent_record["id"])
    return wav
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.





> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

Số 2026:

> 2026 năm của công nghệ:

| Situation | Pick |
|-----------|------|
| 5-sec zero-shot clone, open-source | F5-TTS or OpenVoice v2 |
| Commercial production cloning | ElevenLabs Instant Voice Clone v2.5 |
| Voice conversion (rewriting) | KNN-VC or Diff-HierVC |
| Many-speaker fine-tune | StyleTTS 2 + speaker adapter |
| Cross-lingual cloning | XTTS v2 or VALL-E X |
| Deepfake detection | Wav2Vec2-AASIST |

| 场景 | 选择 |
|------|------|
| 5 秒零样本克隆，开源 | F5-TTS 或 OpenVoice v2 |
| 商业生产级克隆 | ElevenLabs Instant Voice Clone v2.5 |
| 语音转换（重写） | KNN-VC 或 Diff-HierVC |
| 多说话人微调 | StyleTTS 2 + 说话人适配器 |
| 跨语言克隆 | XTTS v2 或 VALL-E X |
| 深度伪造检测 | Wav2Vec2-AASIST |



## Những bẫy

> 常见陷

- **Misaligned reference transcript.**F5-TTS và các loại tương tự yêu cầu văn bản tham chiếu phù hợp chính xác với âm thanh tham chiếu, bao gồm dấu chấm.
  **参考转录不对齐。**F5-TTS等 yêu cầu văn bản tham khảo và tham khảo âm thanh hoàn toàn phù hợp, bao gồm các điểm tham khảo.
- **Reverberant reference.**Echo giết người.
  **混响参考。**Chuyện này sẽ làm hỏng Klon.
- **Emotional mismatch.**Thuật ngữ "hạnh phúc" tạo ra những bản sao vui vẻ của mọi thứ.
  **情感不匹配。** tập tin "欢快" sẽ tạo ra mọi nội dung 欢快克隆.
- **Language leakage.**Khả năng nhân bản một người nói tiếng Anh sau đó yêu cầu mô hình nói tiếng Pháp thường mang theo giọng nói; sử dụng các mô hình đa ngôn ngữ (XTTS, VALL-E X).
  **语言泄漏。**克隆英文说话人然后让模型说法语仍将带有口音;使用跨语言模型 (XTTS, VALL-E X) ⋅
- **No watermark.**Không được vận chuyển hợp pháp tại EU từ tháng 8 năm 2026.
  **没有水印。**Từ tháng 8 năm 2026 bắt đầu trên EU 法律上不可出版.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-voice-cloner.md`Thiết kế một đường ống khống chế hoặc chuyển đổi với cổng đồng ý + dấu nước + mục tiêu chất lượng.

> 保存为 `outputs/skill-voice-cloner.md`❖ thiết kế với sự đồng ý门 + 水印 + 质量目标的克隆或转换流水线──

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`. Kiểm tra sự trao đổi nhúng loa bằng cách tính toán cosine giữa hai "những loa" trước và sau khi trao đổi.
   **简单。**运行 `code/main.py`❖ Thông qua tính toán giao dịch trước sau hai "nói người" của các ký tự tương tự để thể hiện nói người được nhúng vào giao dịch.
2. **Medium.**Sử dụng OpenVoice v2 để nhân bản giọng nói của riêng bạn. đo SECS giữa tham chiếu và nhân bản. đo CER thông qua Whisper.
   **中等。**Sử dụng OpenVoice v2 克隆你自己的声音──测量参考与克隆之间的SECS──通过语 测量 CER──
3. **Hard.**Lấy dấu nước SilentCipher vào 20 bản sao, chạy chúng qua mã MP3 128 kbps + mã hóa, phát hiện tải trọng hữu ích.
   **困难。**Đối với 20 ứng dụng SilentCipher nước in, thông qua 128 kbps MP3 编码+解码,检测载荷―― báo cáo tỷ lệ chính xác――

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Zero-shot clone | 5 seconds is enough | Pretrained model + speaker embedding; no training. |
| PPG | Phonetic posteriorgram | Per-frame ASR posteriors used as language-agnostic content rep. |
| KNN-VC | Nearest-neighbor conversion | Replace each source frame with nearest target-pool frame. |
| Neural codec TTS | VALL-E style | AR model over EnCodec/SoundStream tokens. |
| Watermark | Inaudible signature | Bits embedded in audio, survive re-encode. |
| SECS | Cloning fidelity | Cosine between target and clone speaker embeddings. |
| AASIST | Deepfake detector | Anti-spoof model; detects synthesized speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 零样本克隆 | 5 秒就够了 | 预训练模型 + 说话人嵌入；无需训练。 |
| PPG | 音素后验图 | 逐帧 ASR 后验，用作语言无关的内容表示。 |
| KNN-VC | 最近邻转换 | 用目标池中最近邻替换每个源帧。 |
| 神经编解码 TTS | VALL-E 风格 | 在 EnCodec/SoundStream token 上的 AR 模型。 |
| 水印 | 不可听签名 | 嵌入音频中的比特，经受重编码。 |
| SECS | 克隆保真度 | 目标与克隆说话人嵌入之间的余弦相似度。 |
| AASIST | 深度伪造检测器 | 反欺诈模型；检测合成语音。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Chen et al. (2024). F5-TTS](https://arxiv.org/abs/2410.06885) SOTA mã nguồn mở - sao chép không bắn.
  Chen 等 (2024). F5-TTS开源 SOTA 零样本克隆。
- [Baevski et al. / Microsoft (2023). VALL-E](https://arxiv.org/abs/2301.02111)và [VALL-E 2 (2024)](https://arxiv.org/abs/2406.05370) TTS codec thần kinh.
  Baevski 等 / 微软 (2023). VALL-E 和 VALL-E 2(2024)  神经编解码 TTS──
- [Qian et al. (2019). AutoVC](https://arxiv.org/abs/1905.05879) chuyển đổi giọng nói dựa trên sự tách rời.
  Qian 等 (2019). AutoVC dựa trên giải thích của语音转换──
- [Baas, Waubert de Puiseau, Kamper (2023). KNN-VC](https://arxiv.org/abs/2305.18975) VC dựa trên tìm kiếm.
  Baas, Waubert de Puiseau, Kamper (2023). KNN-VC dựa trên kiểm tra của chuyển đổi ngữ音.
- [SilentCipher (2024) — Audio Watermarking](https://github.com/sony/silentcipher) Biểu tượng âm thanh 32 bit sẵn sàng sản xuất.
  SilentCipher(2024) 音频水印生产可用 32 位音频水印。
- [ASVspoof 2025 results](https://www.asvspoof.org/) cuộc đua vũ khí máy dò chống lại máy tổng hợp, được cập nhật vào năm 2026.
  ASVspoof 2025 结果检测器 vs 合成器军备竞赛,2026年更新──

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

