# Tận dạng ngôn ngữ (ASR)  CTC, RNN-T, chú ý  语音识别  CTC、RNN-T và cơ chế chú ý

> Sự nhận dạng giọng nói là phân loại âm thanh tại mỗi bước thời gian, được gắn với nhau bởi một mô hình chuỗi biết tiếng Anh và im lặng. CTC, RNN-T và chú ý là ba cách để làm điều đó. Chọn một và hiểu tại sao.

> **【中文解读】**语音识别 là mỗi thời gian làm âm thanh, tái sử dụng chuỗi mô hình (xác định ngôn ngữ và âm thanh tĩnh) để gắn chúng lại.

> **【拓展：ASR 的应用】**语音识别是语音助手(Siri、小爱同学) 、会议记录(飞书/钉钉实时字幕) 、视频字幕自动生成的核心──Whisper 是 2026 年的开源 ASR 标杆──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 08 (CNNs & RNNs for Text), Phase 5 · 10 (Attention) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 08（文本的 CNN 与 RNN），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Bạn có một clip 10 giây 16 kHz. Bạn muốn một chuỗi: "đóng đèn nhà bếp". Thách thức là cấu trúc: khung âm thanh không phù hợp với các ký tự. Từ "okay" có thể mất 200 ms hoặc 1200 ms. Sự im lặng chấm dứt phát biểu. Một số âm thanh dài hơn những người khác. Số lượng các mã thông báo đầu ra không được biết trước.

> Bạn có một đoạn 10 giây 16 kHz của âm thanh. Bạn muốn một字符串:" bật đèn bếp"── thách thức là cấu trúc:音频与字符不是一对应的──单词"okay"可能占用200 ms或1200 ms──静音打断语语语──有些音素比其它更长──输出代号的数量事先不知道──

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Ba công thức giải quyết vấn đề này:

> 3 giải pháp giải quyết vấn đề này:

1. **CTC (Connectionist Temporal Classification).**Phát ra xác suất token mỗi khung bao gồm một * trống đặc biệt*. Phản ứng sụp đổ lặp lại và trống trong thời gian giải mã. Không tự rút, nhanh. Được sử dụng bởi wav2vec 2.0, MMS.
   **CTC（连接时序分类）。**逐发射代币 概率, bao gồm đặc biệt *blank*。解码时折重复和空白。非自归,快速。wav2vec 2.0、MMS 使用。
2. **RNN-T (Recurrent Neural Network Transducer).**Mạng lưới chung dự đoán mã thông báo tiếp theo được cung cấp khung mã hóa và mã thông báo trước đó. Streamable. được sử dụng bởi ASR trên thiết bị của Google, NVIDIA Parakeet.
   **RNN-T（递归神经网络转换器）。**联合网络根据编码器和之前的代币 预测下一个代币──可流式处理──Google 端侧 ASR、NVIDIA Parakeet 使用──
3. **Attention encoder-decoder.**Encoder nén âm thanh vào trạng thái ẩn, decoder phục vụ chéo để tạo token tự động.
   **注意力编码器-解码器。**编码器将音频压缩为隐藏状态,解码器通过交叉注意力自归地生成代币──Whisper、SeamlessM4T 使用──

Năm 2026, SOTA WER trên LibriSpeech test-clean là 1,4% (Parakeet-TDT-1.1B, NVIDIA) và 1,58% (Whisper-Large-v3-turbo).

> Năm 2026, Test-clean của LibriSpeech 上的 SOTA WER là 1,4% (Parakeet-TDT-1.1B,NVIDIA) và 1,58% (Whisper-Large-v3-turbo)

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Three ASR formulations: CTC, RNN-T, attention-encoder-decoder](../assets/asr-formulations.svg)

**CTC intuition.**Để mã hóa phát `T`phân phối cấp khung trên `V+1`token (V chars + blank). Đối với một chuỗi mục tiêu `y`dài `U < T`, bất kỳ đường thẳng khung nào bị sập xuống`y`số lượng. CTC mất tổng trên tất cả các sự sắp xếp như vậy. Inference: per frame argmax, sụp đổ lặp lại, loại bỏ trống.

> **CTC 直觉。**让编码器输出 `T`个级分布, mỗi phân bố bao phủ `V+1`个 token ((V 个字符 + trống) ⋅ đối với长度为 `U < T`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `y`, bất kỳ gấp sau như `y`CTC  mất mát đối với tất cả các đối tượng như vậy 推理:逐 argmax, gấp lại, di chuyển空白──

Lợi ích: không tự rút, có thể phát trực tuyến, không có đầu nhìn. Khối thấu: * giả định độc lập điều kiện *  mỗi dự đoán khung tự do khỏi các khung khác, do đó không có mô hình ngôn ngữ nội bộ.

> 优势:非自归、可流式处理、零前──缺点:*条件独立性假设*每预测彼此独立,因此没有内部语言模型──通过光束搜索或浅融合的外部LM 来修复──

**RNN-T intuition.**Thêm một mạng * predictor * nhúng lịch sử token và một * joiner * kết hợp trạng thái dự đoán với khung mã hóa thành một phân phối chung trên `V+1`(the `+1`là null / no-emitt). Mô hình rõ ràng phụ thuộc điều kiện CTC bỏ qua. Streamable vì mỗi bước chỉ điều kiện trên khung trước và token trước.

> **RNN-T 直觉。**Thêm một mã thông báo nhúng  lịch sử của * dự đoán * 网络和一个将预测器 状态与编码器结合为 `V+1`联合分布的 *joiner*(`+1`là null/不发射) ―― hiển nhiên xây dựng CTC 忽略的条件依赖――可流式处理, vì mỗi bước chỉ phụ thuộc vào quá khứ和过去的代币──

Lợi ích: Streamable + LM nội bộ. Khác điểm: đào tạo phức tạp hơn và đói trí nhớ (3D grid); RNN-T hạt nhân mất mát là một toàn bộ danh mục thư viện riêng.

> 优势:可流式 + 内部 LM。缺点:训练更复杂、更耗内存(3D 损失格);RNN-T 损失核本身就是一个完整的库类──

**Attention encoder-decoder.**Bộ mã hóa (6-32 lớp biến đổi) trên khung log-mail. Bộ mã hóa (6-32 lớp biến đổi) phục vụ qua nhau để tạo ra mã hóa tự động. Không có hạn chế sắp xếp  sự chú ý có thể nhìn bất cứ nơi nào trong âm thanh. Không thể phát trực tuyến trừ khi bạn hạn chế sự chú ý (Whisper-Streaming, 2024).

> **注意力编码器-解码器。**编码器(6-32 层变压器) xử lý log-mel ──解码器(6-32 层变压器) thông qua交叉注意力自归归生成代币──无对齐约束注意力可以看向音频的任何位置──除非限制注意力(分块 微笑流,2024),否则不可流式处理──

Lợi ích: chất lượng cao nhất trên ASR ngoài khơi, dễ đào tạo với công cụ seq2seq tiêu chuẩn. Khối thối: độ trễ tự động tương xứng với chiều dài đầu ra; không thể phát trực tuyến mà không cần kỹ thuật.

> 优势:离线 ASR 质量最高,使用标准seq2seq 工具易训练──缺点: tự quay trở chậm với dung lượng xuất thành正比;不做工程优化无法流式处理──

### WER: số một

> ### WER: chỉ số duy nhất

**Word Error Rate**= `(S + D + I) / N`, nơi S = thay thế, D = xóa, I = nhập, N = số từ tham chiếu. Hình dung tương ứng khoảng cách chỉnh sửa Levenshtein ở mức từ. thấp hơn là tốt hơn. WER trên 20% thường không thể sử dụng; dưới 5% là bình đẳng con người cho bài đọc.

> **词错误率**= `(S + D + I) / N`, trong đó S = thay thế, D = xóa, I =插入, N = số từ tham khảo.

| Model | LibriSpeech test-clean | LibriSpeech test-other | Size |
|-------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 1.1B params |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 809M |
| Canary-1B Flash | 1.48% | 2.87% | 1B |
| Seamless M4T v2 | 1.7% | 3.5% | 2.3B |

| 模型 | LibriSpeech test-clean | LibriSpeech test-other | 大小 |
|------|------------------------|------------------------|------|
| Parakeet-TDT-1.1B | 1.40% | 2.78% | 11 亿参数 |
| Whisper-Large-v3-turbo | 1.58% | 3.03% | 8.09 亿 |
| Canary-1B Flash | 1.48% | 2.87% | 10 亿 |
| Seamless M4T v2 | 1.7% | 3.5% | 23 亿 |

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――


Tất cả các hệ thống này đều dựa trên mã hóa-tử lý hoặc RNN-T. Hệ thống CTC tinh khiết (wav2vec 2.0) nằm ở khoảng 1,82,1% trên test-clean.

> Những thứ này là các bộ lập trình- giải mã hoặc RNN-T 架构──纯 CTC 系统(wav2vec 2.0) trong test-clean 上约1.82.1%──

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.



## Hãy xây dựng nó.
```figure
ctc-collapse
```

## Hãy xây dựng nó

### Bước 1: CTC tham lam

```python
def ctc_greedy(frame_logits, blank=0, vocab=None):
    # frame_logits: list of per-frame probability vectors
    preds = [max(range(len(p)), key=lambda i: p[i]) for p in frame_logits]
    out = []
    prev = -1
    for p in preds:
        if p != prev and p != blank:
            out.append(p)
        prev = p
    return "".join(vocab[i] for i in out) if vocab else out
```

Hai quy tắc: sụp đổ liên tiếp lặp lại, bỏ trống. ví dụ: `a a _ _ a b b _ c`→ `a a b c`- Tôi không biết.

> 两条规则: 折叠连续重复,丢弃空白.`a a _ _ a b b _ c`→ `a a b c`

### Bước 2: CTC tìm kiếm chùm

```python
def ctc_beam(frame_logits, beam=8, blank=0):
    import math
    beams = [([], 0.0)]  # (tokens, log_prob)
    for p in frame_logits:
        log_p = [math.log(max(pi, 1e-10)) for pi in p]
        candidates = []
        for seq, lp in beams:
            for t, lpt in enumerate(log_p):
                new = seq[:] if t == blank else (seq + [t] if not seq or seq[-1] != t else seq)
                candidates.append((new, lp + lpt))
        candidates.sort(key=lambda x: -x[1])
        beams = candidates[:beam]
    return beams[0][0]
```

Sản xuất sử dụng tìm kiếm chùm cây tiền tố với hợp nhất LM; đây là bộ xương khái niệm.

> 生产环境使用带 LM 融合的前树束搜索;这是概念骨架──

### Bước 3: WER

```python
def wer(ref, hyp):
    r, h = ref.split(), hyp.split()
    dp = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        dp[i][0] = i
    for j in range(len(h) + 1):
        dp[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            cost = 0 if r[i - 1] == h[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )
    return dp[len(r)][len(h)] / max(1, len(r))
```

### Bước 4: suy luận chống lại Whisper

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe("clip.wav")
print(result["text"])
```

Một dòng cho ASR chung mạnh nhất vào năm 2026. chạy trên một GPU 24 GB với thời gian thực ~ 20x.

> Một dòng mã của ASR phổ biến mạnh nhất năm 2026  trên GPU 24 GB chạy với tốc độ thực tế khoảng 20 lần 

### Bước 5: phát trực tuyến với Parakeet hoặc wav2vec 2.0

```python
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="nvidia/parakeet-tdt-1.1b")
for chunk in streaming_audio():
    print(asr(chunk, return_timestamps=True))
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


Streaming ASR cần tập trung phần mềm mã hóa và trạng thái chuyển tải; sử dụng thư viện hỗ trợ nó (NeMo cho Parakeet, `transformers`đường ống với `chunk_length_s`().

> 流式 ASR 需要分块编码器注意力和转移状态; sử dụng hỗ trợ kho của nó`transformers`đường ống dẫn 带 `chunk_length_s`(■)




> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

Số 2026:

> 2026 năm của công nghệ:

| Situation | Pick |
|-----------|------|
| English, offline, max quality | Whisper-large-v3-turbo |
| Multilingual, robust | SeamlessM4T v2 |
| Streaming, low latency | Parakeet-TDT-1.1B or Riva |
| Edge, mobile, <500 ms latency | Whisper-Tiny quantized or Moonshine (2024) |
| Long-form | Whisper with VAD-based chunking (WhisperX) |
| Domain-specific (medical, legal) | Fine-tune wav2vec 2.0 + domain LM fusion |

| 场景 | 选择 |
|------|------|
| 英文、离线、最高质量 | Whisper-large-v3-turbo |
| 多语言、鲁棒 | SeamlessM4T v2 |
| 流式、低延迟 | Parakeet-TDT-1.1B 或 Riva |
| 边缘/移动、<500 ms 延迟 | 量化 Whisper-Tiny 或 Moonshine（2024） |
| 长音频 | Whisper + VAD 分块（WhisperX） |
| 特定领域（医疗、法律） | 微调 wav2vec 2.0 + 领域 LM 融合 |



## Những bẫy vẫn còn tồn tại vào năm 2026

> Năm 2026 vẫn còn trong bẫy tội phạm

- **No VAD.**Điệu Vô lên im lặng tạo ra ảo giác ("Cảm ơn đã xem!").
  **没有 VAD。**Trong thanh thanh lên vận hành Whisper 会产生幻觉("Cảm ơn đã xem!")
- **Character vs word vs subword WER.**Báo cáo WER cấp từ * sau * bình thường hóa (như chữ viết lách, dấu chấm bị loại bỏ).
  **字符 vs 词 vs 子词 WER。**报告归一化后(小写、去标点) của từ级 WER。
- **Language ID drift.**LID tự động của Whisper sai đường cho các clip tiếng ồn đến tiếng Nhật hoặc tiếng Wales; lực `language="en"`Khi anh biết.
  **语言识别漂移。**Whisper's Automatic Language Identification will mistake 杂段段 for 语或威尔士语;已知语言时强制 `language="en"`
- **Long clips without chunking.**Whisper có một cửa sổ 30 giây.`chunk_length_s=30, stride=5`cho bất cứ điều gì lâu hơn.
  **长音频不分块。**Hầm thì thầm có 30 giây cửa sổ.`chunk_length_s=30, stride=5`

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-asr-picker.md`Chọn mô hình, giải mã chiến lược, chunking, và LM hợp nhất cho một mục tiêu triển khai nhất định.

> 保存为 `outputs/skill-asr-picker.md`❖ Đối với một mục tiêu triển khai cho mô hình chọn lựa, giải mã chiến lược, phân khối và LM 融合方案.

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`Nó tham lam giải mã một đầu ra CTC được làm bằng tay và tính WER với một tham chiếu.
   **简单。**运行 `code/main.py`◊ Nó đối với CTC sản xuất thủ công 输出 thực hiện tham gia giải mã并计算 WER。
2. **Medium.**Thực hiện tìm kiếm chùm cây tiền tố trong bước 2 một cách đúng đắn (tự tính quy tắc hợp nhất trống). So sánh với tham lam trên một tập dữ liệu tổng hợp 10 ví dụ.
   **中等。**正确实现步骤 2 中的前树束搜查(考虑空白合并规则) ⋅ 在 10 个合成样本上与贪方法比较──
3. **Hard.**Sử dụng `whisper-large-v3-turbo`[LibriSpeech test-clean](https://www.openslr.org/12)- Xét WER trên 100 phát biểu đầu tiên. So sánh với số lượng được công bố.
   **困难。**Trong [LibriSpeech test-clean](https://www.openslr.org/12)上使用 `whisper-large-v3-turbo`△计算前 100 条语音的 WER──与发表的数据比较──

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| CTC | The blank-token loss | Marginal over all frame-to-token alignments; non-AR. |
| RNN-T | The streaming loss | CTC + next-token predictor; handles word-order. |
| Attention enc-dec | Whisper-style | Encoder + cross-attending decoder; best offline quality. |
| WER | The number you report | `(S+D+I)/N` at word level. |
| Blank | The emptiness | Special token in CTC signalling "no emission this frame". |
| LM fusion | External language model | Add weighted LM log-probs during beam search. |
| VAD | The silence gate | Voice activity detector; trims non-speech. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| CTC | blank token 损失 | 所有帧到 token 对齐的边际概率；非自回归。 |
| RNN-T | 流式损失 | CTC + 下一 token 预测器；处理词序。 |
| 注意力编解码 | Whisper 风格 | 编码器 + 交叉注意力解码器；最佳离线质量。 |
| WER | 你报告的数字 | 词级别的 `(S+D+I)/N`。 |
| Blank | 空白 | CTC 中表示"本帧不发射"的特殊 token。 |
| LM 融合 | 外部语言模型 | beam search 中加入加权的 LM 对数概率。 |
| VAD | 静音门 | 语音活动检测器；裁剪非语音部分。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Graves et al. (2006). Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf) giấy tờ CTC.
  Graves 等 (2006). 连接时序分类CTC 论文。
- [Graves (2012). Sequence Transduction with RNNs](https://arxiv.org/abs/1211.3711) tờ RNN-T.
  Graves (2012). Sử dụng RNN  tiến hành chuyển đổi chuỗi RNN-T 论文。
- [Radford et al. / OpenAI (2022). Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) giấy phép năm 2022; v3-turbo mở rộng vào năm 2024.
  Radford 等 / OpenAI (2022). Hầmầm: ầmầmầm: ầmầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm: ầm:
- [NVIDIA NeMo — Parakeet-TDT card](https://huggingface.co/nvidia/parakeet-tdt-1.1b) 2026 Open ASR Leaderboard dẫn đầu.
  NVIDIA NeMoParakeet-TDT 模型卡2026 年 Open ASR 排行榜领先者──
- [Hugging Face — Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) chỉ số chuẩn trực tiếp trên 25+ mô hình.
  Hugging FaceOpen ASR 排行榜25+ 模型的实时基准测试──

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

