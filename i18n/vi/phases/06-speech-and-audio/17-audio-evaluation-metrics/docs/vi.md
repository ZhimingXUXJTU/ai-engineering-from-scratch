# Đánh giá âm thanh  WER, MOS, UTMOS, MMAU, FAD, và bảng xếp hạng mở  音频评估指标

> Bạn không thể gửi những gì bạn không thể đo lường. Bài học này nêu tên các số liệu 2026 cho mỗi nhiệm vụ âm thanh: ASR (WER, CER, RTFx), TTS (MOS, UTMOS, SECS, WER-on-ASR-round-trip), ngôn ngữ âm thanh (MMAU, LongAudioBench), âm nhạc (FAD, CLAP), và loa (EER).

> **【中文解读】**无法量就无法交付──本课列出 2026 年所有音频任务的评估指标:ASR 用 WER(词错率) ✓ TTS 用 MOS(平均意见分) ✓ 音频语言模型用 MMAU、音乐用 FAD、说话人识别用 EER──还有对比排行榜──

> **【拓展：WER 是语音识别的黄金指标】**WER(Tỷ lệ lỗi từ,词错率) = (替换+删除+插入) / 总词数。Whisper V3 lớn trong tiếng Anh đạt ~5% WER, gần với mức độ loài người。中文用 CER(字错率)。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 06, 07, 09, 10; Phase 2 · 09 (Model Evaluation) | **前置知识:** 阶段 6 · 04、06、07、09、10；阶段 2 · 09（模型评估）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## Vấn đề  vấn đề giới thiệu

Mỗi nhiệm vụ âm thanh có nhiều métrics, mỗi đo một trục khác nhau. Sử dụng métrics sai là cách bạn vận chuyển một mô hình trông tuyệt vời trên bảng điều khiển của bạn và khủng khiếp trong sản xuất. Danh sách 2026:

> Mỗi nhiệm vụ âm thanh có nhiều chỉ số, mỗi chỉ số đo kích thước khác nhau. Chỉ số sai lầm là làm thế nào để một mô hình xuất hiện tốt trên bảng thiết bị nhưng hoạt động tồi tệ trong sản xuất.

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.


| Task | Primary | Secondary |
|------|---------|-----------|
| ASR | WER | CER · RTFx · first-token latency |
| TTS | MOS / UTMOS | SECS · WER-on-ASR-round-trip · CER · TTFA |
| Voice cloning | SECS (ECAPA cosine) | MOS · CER |
| Speaker verification | EER | minDCF · FAR / FRR at operating point |
| Diarization | DER | JER · speaker confusion |
| Audio classification | top-1 · mAP | macro F1 · per-class recall |
| Music generation | FAD | CLAP · listening panel MOS |
| Audio language model | MMAU-Pro | LongAudioBench · AudioCaps FENSE |
| Streaming S2S | latency P50/P95 | WER · MOS |

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


## Khái niệm cốt lõi

![Audio evaluation matrix — metrics vs tasks vs 2026 leaderboards](../assets/eval-landscape.svg)

### Các số liệu ASR

> ASR  đánh giá chỉ số

**WER (Word Error Rate).** `(S + D + I) / N`- chữ nhỏ, dấu chấm, bình thường hóa số trước khi ghi điểm.`jiwer`hoặc OpenAI `whisper_normalizer`. &lt;5% = đọc ngôn ngữ bằng con người.

> **WER（词错率）。** `(替换 + 删除 + 插入) / 总词数`◊评分前需转小写、除标点、标准化数字──使用 `jiwer`Hoặc OpenAI của `whisper_normalizer`❖ thấp hơn 5% = 朗读语音的人类水平。

**CER (Character Error Rate).**Tương tự công thức, cấp độ ký tự. được sử dụng cho ngôn ngữ âm thanh (Mandarin, tiếng Cantonese) nơi phân đoạn từ là mơ hồ.

> **CER（字错率）。**相同公式,字符级别──用于声调语言(普通话、语), vì phân đoạn từ không rõ ràng──

**RTFx (inverse real-time factor).**2 giây âm thanh được xử lý mỗi giây. cao hơn là tốt hơn. Parakeet-TDT đạt 3380x. Whisper-large-v3 là ~30x.

> **RTFx（逆实时因子）。**Mỗi giây thực tế xử lý của số lượng âm thanh giây.

**First-token latency.**Đường đồng hồ từ đầu vào âm thanh đến mã bản sao đầu tiên.

> **首 token 延迟。**Từ âm thanh nhập vào đầu tiên chuyển âm token thời gian thực tế.

### TTS

> TTS  đánh giá chỉ số

**MOS (Mean Opinion Score).**1-5 người xếp hạng. tiêu chuẩn vàng nhưng chậm. Thu thập 20+ người nghe mỗi mẫu, 100+ mẫu mỗi mẫu.

> **MOS（平均意见分）。**1-5 分人工评分──黄金标准但速度慢──每个样本收集20+听者,每个模型100+样本──

**UTMOS (2022-2026).**Tiến sĩ đã học được dự báo MOS. tương quan với MOS con người trên các tiêu chuẩn tiêu chuẩn. F5-TTS: UTMOS 3.95; sự thật cơ bản: 4.08.

> **UTMOS（2022-2026）。**Học tập kiểu MOS  dự đoán器. ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒  ⇒ ⇒  ⇒ ⇒ ⇒    ⇒ ⇒    ⇒ ⇒     ⇒ ⇒     ⇒ ⇒     ⇒ ⇒    ⇒ ⇒                                                                                                                                                                                                                                         

**SECS (Speaker Encoder Cosine Similarity).**Đối với việc nhân bản giọng nói. ECAPA nhúng cosine giữa tham chiếu và đầu ra nhân bản. &gt; 0,75 = nhân bản nhận ra.

> **SECS（说话人编码器余弦相似度）。**Sử dụng trong ngữ音克隆──参考音频和克隆输出之间的 ECAPA 嵌入余弦相似度──大于0.75 = 可识别的克隆──

**WER-on-ASR-round-trip.**chạy Whisper trên đầu ra TTS, tính WER với văn bản nhập. Chụp sự lùi độ hiểu biết. 2026 SOTA: &lt; 2% CER.

> **WER-on-ASR-round-trip（ASR 回环 WER）。**Đối với TTS 输出运行 ,计算对输入文本的 WER──捕获可理解度退化──2026 SOTA:CER 低于2%──

**TTFA (time-to-first-audio).**Thời gian trễ của đồng hồ tường. Kokoro-82M: ~ 100 ms; F5-TTS: ~ 1 giây.

> **TTFA（首个音频时间）。**实际延迟──Kokoro-82M: khoảng 100 ms; F5-TTS: khoảng 1 s──

### Đặc biệt về nhân tạo giọng nói

> 语音克隆专用标标签

**SECS + MOS + CER**Một bản sao có điểm SECS cao nhưng MOS thấp có nghĩa là timbre-trực nhưng không tự nhiên; ngược lại có nghĩa là giọng nói tự nhiên nhưng không đúng.

> **SECS + MOS + CER**作为三重指标──克隆分高SECS Nhưng MOS thấp có nghĩa là âm sắc chính xác nhưng không tự nhiên; 反之则 có nghĩa là âm thanh tự nhiên nhưng nói người không đối với──

### Kiểm tra loa

> Nói chuyện người chứng nhận chỉ số

**EER (Equal Error Rate).**Giá trị ngưỡng khi tỷ lệ chấp nhận sai bằng tỷ lệ từ chối sai. ECAPA trên VoxCeleb1-O: 0,87%.

> **EER（等错误率）。**误接受率等于误拒率的值──ECAPA 在 VoxCeleb1-O 上:0.87%──

**minDCF (min Detection Cost).**Chi phí cân nhắc tại một điểm hoạt động được chọn (thường là FAR=0,01).

> **minDCF（最小检测代价）。**Trong các điểm chọn làm việc (thường là FAR=0.01) tăng giá quyền làm việc hơn EER

### Lượng chảy máu

> Nói话人日志 chỉ số

**DER (Diarization Error Rate).** `(FA + Miss + Confusion) / total_speaker_time`. Phản ứng không được phát âm + phát âm báo động giả + confusion loa, mỗi lần là một phần nhỏ.

> **DER（说话人日志错误率）。** `(虚警 + 漏检 + 混淆) / 总说话时间`◊漏检语音 + 虚警语音 + 说话人混,各占比例──AMI 会议:DER 约 10-20% 是现实水平──pianonote 3.1 + Precision-2 商业版:在良好录音上 DER 低于10%──

**JER (Jaccard Error Rate).**Thay vì DER, mạnh mẽ để phân đoạn ngắn thiên vị.

> **JER（Jaccard 错误率）。**DER thay thế, đối với các đoạn ngắn khác biệt hơn là

### Định dạng âm thanh

> 音频分类标签

Nhiều nhãn: **mAP (mean Average Precision)**trên tất cả các lớp. AudioSet: 0.548 mAP cho BEATs-iter3.

> 多标签:**mAP（平均精度均值）**, phủ sóng tất cả các loại.

Tác dụng độc quyền đa lớp: **top-1, top-5 accuracy**. Phân lệnh nói v2: 99,0% top-1 (Audio-MAE).

> Nhiều loại:**top-1、top-5 准确率**❖Hướng dẫn phát âm v2:99.0% top-1 (Audio-MAE)

Không cân bằng: **macro F1**+ **per-class recall**. Báo cáo cho mỗi lớp  tổng độ chính xác ẩn các lớp thất bại.

> dữ liệu không cân bằng:**macro F1**+ **每类召回率**❖ Theo báo cáo phân loại 汇总准确率 sẽ che giấu những phân loại thất bại nào.

### Tạo nhạc

> 音乐生成指标

**FAD (Fréchet Audio Distance).**Khoảng cách giữa các phân phối vGGish-trúng âm thanh thực vs. tạo. MusicGen- nhỏ trên MusicCaps: 4.5. MusicLM: 4.0. Thấp hơn tốt hơn.

> **FAD（Fréchet 音频距离）。**Thực tế và tạo âm thanh của VGGish 嵌入分布之间的距离──MusicGen-small 在 MusicCaps 上:4.5──MusicLM:4.0──越低越好──

**CLAP Score.**Điểm so sánh văn bản-audio bằng cách sử dụng nhúng CLAP. &gt; 0,3 = sự sắp xếp hợp lý.

> **CLAP 分数。**Sử dụng CLAP 嵌入文本音频对齐分数──大于0.3 = 合理对齐──

**Listening panel MOS.**Suno v5 ELO 1293 trên TTS Arena (từ sở thích của con người).

> **听音评审团 MOS。**仍然是消费级音乐的最终评判标准──Suno v5 在 TTS Arena 上的ELO 为 1293(来自配对人类偏好)──

### Các tiêu chuẩn ngôn ngữ âm thanh

> 音频语言基准测试

**MMAU (Massive Multi-Audio Understanding).**10k cặp âm thanh-QA.

> **MMAU（大规模多音频理解）。**10.000 tiếng nói.

**MMAU-Pro.**1800 vật liệu cứng, bốn loại: giọng nói / âm thanh / âm nhạc / đa âm thanh. Cơ hội ngẫu nhiên 25% trên 4 chiều. Gemini 2.5 Pro tổng thể ~ 60%; đa âm thanh ~ 22% trên tất cả các mô hình.

> **MMAU-Pro。**1800 个难题,四个类别:语音/声音/音乐/多音频──4 选 1 随机猜测 25%──Gemini 2.5 Pro 整体约60%;所有模型在多音频上约22%.──

**LongAudioBench.**Các đoạn clip dài vài phút với các truy vấn ngữ nghĩa.

> **LongAudioBench。**Có lẽ钟音频片段 + 语义查询──Audio Flamingo Next 超过 Gemini 2.5 Pro──

**AudioCaps / Clotho.**Các tiêu chuẩn tiêu chuẩn: SPICE, CIDER, FENSE.

> **AudioCaps / Clotho。**音频描述基准测试──SPICE、CIDER、FENSE 指标──

### Streaming speech-to-speech

> 流式语音到语音指标

**Latency P50 / P95 / P99.**Đồng hồ tường từ cuối người dùng nói đến phản ứng âm thanh đầu tiên.

> **延迟 P50 / P95 / P99。**Từ người dùng语音 kết thúc đến đầu tiên có thể nghe được phản ứng thời gian thực.

**WER / MOS**trên đầu ra.

> 输出 trên **WER / MOS**

**Barge-in responsiveness.**Thời gian từ người dùng gián đoạn đến trợ lý câm.

> **打断响应时间。**Từ thời gian người dùng chia cắt đến thời gian trợ lý tĩnh lặng. Mục tiêu thấp hơn 150 ms.

### Các bảng xếp hạng năm 2026

| Leaderboard | Tracks | URL |
|------------|--------|-----|
| Open ASR Leaderboard (HF) / 开源 ASR 排行榜（HF） | English + multilingual + long-form / 英语 + 多语言 + 长音频 | `huggingface.co/spaces/hf-audio/open_asr_leaderboard` |
| TTS Arena (HF) / TTS 竞技场（HF） | English TTS / 英语 TTS | `huggingface.co/spaces/TTS-AGI/TTS-Arena` |
| Artificial Analysis Speech / Artificial Analysis 语音 | TTS + STT, ELO from paired votes / TTS + STT，配对投票 ELO | `artificialanalysis.ai/speech` |
| MMAU-Pro / MMAU-Pro | LALM reasoning / LALM 推理 | `mmaubenchmark.github.io` |
| SpeakerBench / VoxSRC / 说话人基准 / VoxSRC | Speaker recognition / 说话人识别 | `voxsrc.github.io` |
| MMAU music subset / MMAU 音乐子集 | Music LALM / 音乐 LALM | （在 MMAU 内） |
| HEAR benchmark / HEAR 基准 | Self-supervised audio / 自监督音频 | `hearbenchmark.com` |

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.




## Hãy xây dựng nó.
```figure
sp-wer-align
```

## Hãy xây dựng nó

### Bước 1: WER với bình thường hóa

> 步骤 1:带标准化 WER

```python
from jiwer import wer, Compose, ToLowerCase, RemovePunctuation, Strip

transform = Compose([ToLowerCase(), RemovePunctuation(), Strip()])
score = wer(
    truth="Please turn on the lights.",
    hypothesis="please turn on the light",
    truth_transform=transform,
    hypothesis_transform=transform,
)
# ~0.17
```

### Bước 2: TTS WER đi về

> 步骤 2: TTS 回环 WER

```python
def ttr_wer(tts_model, asr_model, texts):
    errors = []
    for txt in texts:
        audio = tts_model.synthesize(txt)
        recog = asr_model.transcribe(audio)
        errors.append(wer(truth=txt, hypothesis=recog))
    return sum(errors) / len(errors)
```

### Bước 3: SECS cho việc nhân bản giọng nói

> 步骤 3:语音克隆的SECS

```python
from speechbrain.inference.speaker import EncoderClassifier
sv = EncoderClassifier.from_hparams("speechbrain/spkrec-ecapa-voxceleb")

emb_ref = sv.encode_batch(load_wav("reference.wav"))
emb_clone = sv.encode_batch(load_wav("cloned.wav"))
secs = torch.nn.functional.cosine_similarity(emb_ref, emb_clone, dim=-1).item()
```

### Bước 4: FAD cho việc tạo ra âm nhạc

> 步骤 4: nhạc tạo của FAD

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()
score = fad.get_fad_score("generated_folder/", "reference_folder/")
```

### Bước 5: EER cho xác minh loa (cód giống như bài học 6)

> 步骤 5: nói chuyện 的人验证的 EER(与第六课相同的代码)

```python
def eer(same_scores, diff_scores):
    thresholds = sorted(set(same_scores + diff_scores))
    best = (1.0, 0.0)
    for t in thresholds:
        far = sum(1 for s in diff_scores if s >= t) / len(diff_scores)
        frr = sum(1 for s in same_scores if s < t) / len(same_scores)
        if abs(far - frr) < best[0]:
            best = (abs(far - frr), (far + frr) / 2)
    return best[1]
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.





> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

Kết hợp mỗi triển khai với một vòng đánh giá cố định chạy trên mỗi bản cập nhật mô hình. Ba quy tắc chính:

> Mỗi lần triển khai đều được trang bị một công cụ đánh giá cố định, hoạt động trong mỗi lần cập nhật mô hình.

1. **Normalize before scoring.**chữ nhỏ, dấu chấm, số mở rộng.
   Trung ngữ翻译:**评分前标准化。**转小写、去标点、数字展开―― báo cáo quy tắc tiêu chuẩn hóa―
2. **Report distributions, not averages.**P50/P95/P99 cho thời gian trễ. Nhận hồi mỗi lớp cho phân loại. Mỗi loại cho MMAU.
   Trung ngữ翻译:**报告分布而非均值。**延迟用P50/P95/P99──分类用每类召回率──MMAU用每类──
3. **Run one canonical public benchmark.**Ngay cả khi dữ liệu sản xuất của bạn khác nhau, báo cáo trên Open ASR / TTS Arena / MMAU cho phép các nhà phê bình so sánh táo với táo.
   Trung ngữ翻译:**运行一个权威公共基准。**Ngay cả khi dữ liệu sản xuất của bạn khác nhau, báo cáo trên Open ASR / TTS Arena / MMAU có thể cho phép các nhà đánh giá làm một sự tương đối công bằng.



## Những bẫy

> 常见陷

- **UTMOS extrapolation.**Được đào tạo về ngôn ngữ sạch theo kiểu VCTK; ghi âm âm thanh ồn ào / sao chép / cảm xúc kém.
  Trung ngữ翻译:**UTMOS 外推问题。**Trong VCTK 风格的纯净语音上训练;对杂/克隆/情感语音评分效果差──
- **MOS panel bias.**20 nhân viên Amazon Mechanical Turk ≠ 20 người dùng mục tiêu.
  Trung ngữ翻译:**MOS 评审团偏差。**20 Amazon Mechanical Turk 工作者不等于 20 目标用户──如果风险高,花钱请领域专家评审团──
- **FAD depends on reference set.**So sánh với phân phối tham chiếu tương tự trên các mô hình.
  Trung ngữ翻译:**FAD 依赖参考集。**跨模型比较时使用相同的参考分布──
- **Aggregate WER.**Một WER tổng thể 5% có thể che giấu 30% WER trên giọng nói nhấn mạnh.
  Trung ngữ翻译:**汇总 WER。**整体 5% WER có thể che phủ với口音语音 30% WER.
- **Public benchmark saturation.**Hầu hết các mô hình biên giới gần trần nhà trên các tiêu chuẩn chuẩn.
  Trung ngữ翻译:**公共基准饱和。**Hầu hết các mô hình trên đường lối đã gần như như trang nhà trên chuẩn chuẩn.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-audio-evaluator.md`Chọn số liệu, chuẩn và định dạng báo cáo cho bất kỳ phiên bản mô hình âm thanh nào.

> 保存为 `outputs/skill-audio-evaluator.md`◊ cho bất kỳ mô hình âm thanh phát hành lựa chọn chỉ số, chuẩn và báo cáo hình thức.

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`- Xét WER / CER / EER / SECS / FAD-ish / MMAU-ish trên đầu vào đồ chơi.
   Trung ngữ翻译:**简单。**运行 `code/main.py` Trong game ấu输上计算 WER / CER / EER / SECS / 类 FAD / 类 MMAU。
2. **Medium.**Xây dựng một dây thừng WER đi lại và đi lại TTS. Tiêu chuẩn đầu ra Kokoro hoặc F5-TTS của bạn thông qua Whisper. Xét WER trên 50 lần.
   Trung ngữ翻译:**中等。**构建 TTS 回环 WER 评估工具──用 Whisper 处理你的Kokoro 或 F5-TTS 输出──在 50 个提示上计算 WER──标记 WER 大于10% 的提示──
3. **Hard.**Điểm lựa chọn Lớp 10 LALM của bạn trên bài phát biểu MMAU-Pro + đa bộ phận âm thanh (50 mục mỗi).
   Trung ngữ翻译:**困难。**Trong MMAU-Pro's语音 + 多音频子集上 (năm bài viết 50 bài) đánh giá các bài học bạn chọn trong chương trình LALM.

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| WER | ASR score | `(S+D+I)/N` at word level after normalization. / 标准化后的词级 `(S+D+I)/N` |
| CER | Character WER | For tone languages or char-level systems. / 用于声调语言或字符级系统 |
| MOS | Human opinion | 1-5 rating; 20+ listeners × 100 samples. / 1-5 分评分；20+ 听者 × 100 样本 |
| UTMOS | ML MOS predictor | Learned model; correlates ~0.9 with human MOS. / 学习型模型；与人类 MOS 相关性约 0.9 |
| SECS | Voice-clone similarity | ECAPA cosine between reference and clone. / 参考与克隆之间的 ECAPA 余弦相似度 |
| EER | Speaker verif score | Threshold where FAR = FRR. / FAR = FRR 的阈值 |
| DER | Diarization score | (FA + Miss + Confusion) / total. / (虚警 + 漏检 + 混淆) / 总时间 |
| FAD | Music-gen quality | Fréchet distance on VGGish embeddings. / VGGish 嵌入上的 Fréchet 距离 |
| RTFx | Throughput | Audio seconds per wall-clock second. / 每实际秒处理的音频秒数 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [jiwer](https://github.com/jitsi/jiwer) Thư viện WER/CER với các tiện ích bình thường hóa.
  带标准化工具的 WER/CER库
- [UTMOS (Saeki et al. 2022)](https://arxiv.org/abs/2204.02152) học được dự đoán MOS.
  UTMOS(Saeki 等 2022) 学习型 MOS 预测器。
- [Fréchet Audio Distance (Kilgour et al. 2019)](https://arxiv.org/abs/1812.08466) tiêu chuẩn âm nhạc.
  Frechet Audio Distance(Kilgour 等 2019) 音乐生成的标准指标──
- [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) Định vị trực tiếp năm 2026
  Open ASR 排行榜2026 实时排名──
- [TTS Arena](https://huggingface.co/spaces/TTS-AGI/TTS-Arena) bảng xếp hạng TTS với số phiếu của con người.
  TTS Arena人类投票的 TTS 排行榜──
- [MMAU-Pro benchmark](https://mmaubenchmark.github.io/) Đơn vị xếp hạng lý luận LALM.
  MMAU-Pro 基准LALM 推理排行榜
- [HEAR benchmark](https://hearbenchmark.com/) các tiêu chuẩn SSL âm thanh.
  HEAR 基准音频 SSL 评估基准。

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

