# T5, BART  Mã hóa-Mô hình mã hóa  T5 ЬART  Mã hóa-Mô hình mã hóa

> Các mã hóa hiểu. Các mã hóa tạo ra. Hãy đặt chúng lại với nhau và bạn sẽ có một mô hình được xây dựng cho các nhiệm vụ đầu vào → đầu ra: dịch, tóm tắt, viết lại, sao chép.

> **【中文解读】**T5 Đặt tất cả các nhiệm vụ NLP 统一为文本-text 格式――BART Sử dụng để tự编码 tập luyện――适用于翻译、摘要等序列转换任务――

**Type:** Study | **类型:** 学习
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Chỉ có GPT và BERT chỉ có mã hóa mỗi đoạn cắt theo kiến trúc năm 2017 cho một mục tiêu khác nhau.

> 解码器专用 GPT 和编码器专用 BERT từng tự cho các mục tiêu khác nhau đã tinh chỉnh cấu trúc năm 2017 .

- Dịch: tiếng Anh → tiếng Pháp.
  Trung ngữ翻译:翻译:英语 → 法语。
- Kết luận: 5000 token bài viết → 200 token tổng kết.
  Trung文翻译:摘要: 5.000 mã 文章 → 200 mã 摘要。
- Nhận dạng giọng nói: mã thông báo âm thanh → mã thông báo văn bản.
  Trung ngữ翻译:语音识别:音频 token → 文本 token。
- Phân xuất cấu trúc: prose → JSON.
  Trung văn翻译:结构化提取:散文 → JSON。

Đối với những thứ này, bộ mã hóa-cập mã làm cho phù hợp nhất. bộ mã hóa tạo ra một đại diện dày đặc của nguồn. bộ mã hóa tạo ra đầu ra, phục vụ chéo cho đại diện đó ở mỗi bước. Trình luyện là chuyển đổi từng người ở phía đầu ra.

> Đối với những nhiệm vụ này, coder-decoder là lựa chọn thích hợp nhất. Coder-decoder là một lựa chọn rất đặc biệt.

Hai bài báo đã định nghĩa cuốn sách chơi game hiện đại:

> 两篇论文定义了现代范式:

1. **T5**(Raffel et al. 2019). "Transformer Transfer Text-to-Text". Mỗi nhiệm vụ NLP được định dạng lại như text-in, text-out. kiến trúc đơn, từ vựng đơn, mất mát đơn. Được đào tạo trước trên dự đoán thời gian đeo mặt nạ (nhanh tham nhũng trong đầu vào, giải mã chúng trong đầu ra).
   Trung ngữ翻译:**T5**(Raffel 等人,2019) ――"文本到文本迁移变压器"── mỗi nhiệm vụ NLP đều được định nghĩa lại như文本输入文本输出──单一架构、单一词表、单一损失──用掩码片段预测进行预训练(破坏输入中的片段,在输出中解码它们)──
2. **BART**(Lewis et al. 2019). "Tranformator hai chiều và tự động hồi phục". Phể bỏ autoencoder: nhập nhập bị hư hại theo nhiều cách (xuy nhộn, che giấu, xóa, xoay), yêu cầu máy giải mã tái tạo bản gốc.
   Trung ngữ翻译:**BART**(Lewis 等人,2019) ――"双向自归转变器"──去噪自编码器:用多种方式破坏输入(打乱、掩码、删除、旋转),要求解码器重建原始文本。

Năm 2026, định dạng mã hóa-tài mã hóa sẽ tồn tại ở những nơi cấu trúc đầu vào quan trọng:

> Năm 2026, các mô hình lập trình- giải trình tiếp tục tồn tại trong các trường hợp quan trọng trong cấu trúc nhập khẩu:

- Nhầm (những lời nói → văn bản).
  中文翻译:Whisper(语音 → 文本) 』
- Google dịch vụ.
  Trung ngữ翻译:Google's翻译系统──
- Một số mô hình hoàn thành / sửa chữa mã có cấu trúc ngữ cảnh và chỉnh sửa khác nhau.
  Trung ngữ翻译:一些具有明确上下文-编辑结构的代码补全/修复模型──
- Flan-T5 và các biến thể cho các nhiệm vụ lý luận có cấu trúc.
  Trung văn翻译:Flan-T5  và các biến thể, được sử dụng để cấu trúc nhiệm vụ.

Chỉ có decoder đã giành được sự chú ý, nhưng decoder không bao giờ biến mất.

> Mô hình chuyên dụng của máy giải mã đã giành được đèn聚光, nhưng máy code-decode chưa bao giờ biến mất.

> **【中文解读】**编码器-解码器架构在"输入→输出"结构化任务中仍然有优势──T5 sẽ thống nhất tất cả các nhiệm vụ NLP thành văn bản-text 格式,BART sử dụng để tự lập âm thanh 编码训练──Though in the pure text generation field it is only replaced by Decoder, but in语音识别(Whisper) 翻译、摘要等任务中仍然是最佳选择──

## Khái niệm cốt lõi

![Encoder-decoder with cross-attention](../assets/encoder-decoder.svg)

### Chuyện chuyển tiếp

```
source tokens ─▶ encoder ─▶ (N_src, d_model)  ──┐
                                                 │
target tokens ─▶ decoder block                   │
                 ├─▶ masked self-attention       │
                 ├─▶ cross-attention ◀───────────┘
                 └─▶ FFN
                ↓
              next-token logits
```

Điều quan trọng là bộ mã hóa chạy một lần mỗi đầu vào. Bộ mã hóa chạy tự động nhưng phục vụ qua nhau cho * cùng một * đầu ra mã hóa tại mỗi bước. Caching đầu ra mã hóa là một tốc độ miễn phí cho đầu vào dài.

> Điều quan trọng là, bộ lập trình chỉ chạy một lần cho mỗi đầu vào.

> **【中文解读】**交叉注意力是编码器-解码器架构的信息桥梁:Q 来自编码器,K/V 来自编码器输出;;编码器只运行一次(高效),解码器每步都通过交叉注意力访问编码器的完整输出;;

> **【拓展：Whisper 的编码器-解码器设计】**Mô hình nhận dạng tiếng nói của OpenAI sử dụng cấu trúc lập trình - giải mã, vì âm thanh (MDR) và văn bản là một mô hình hoàn toàn khác nhau.

### T5 trước khi đào tạo  tham nhũng thời gian

Chọn các khoảng thời gian ngẫu nhiên của đầu vào (giờ trung bình là 3 token, tổng cộng là 15%). Thay thế mỗi khoảng thời gian bằng một sentinel độc đáo: `<extra_id_0>`- `<extra_id_1>`, vv. Các decoder chỉ phát ra các span bị hỏng với tiền tố của họ Sentinel:

> 随机选择输入中的片段(平均长度 3 个代币,总计 15%) ⋅ dùng một ký hiệu chỉ huy duy nhất để thay thế mỗi đoạn:`<extra_id_0>``<extra_id_1>`等──解码器只输出被破坏的片段及其哨兵前:

```
source: The quick <extra_id_0> fox jumps <extra_id_1> dog
target: <extra_id_0> brown <extra_id_1> over the lazy
```

tín hiệu rẻ hơn so với dự đoán toàn bộ chuỗi. cạnh tranh với MLM (BERT) và tiền tố-LM (UniLM) trong giấy T5 của ablation.

> Trong thí nghiệm tiêu hóa của bài luận T5, cạnh tranh với MLM (BERT) và trước LM (UniLM) tương đương.

### BART trước khi tập                                                                                                                                                                                                                                                             

BART thử nghiệm năm chức năng âm thanh:

> BART 尝试五种噪声函数:

1. - Đánh dấu.
   Trung文翻译:Token 掩码。
2. - Đánh dấu.
   中文翻译:Token 删除。
3. Đơn văn bản (đóng một khoảng thời gian, trình giải mã chèn chiều dài đúng).
   Trung văn翻译:文本填充(掩码一个片段,解码器插入正确长度)
4. Chuyển đổi câu.
   Trung ngữ翻译:句子排列──
5. Chuyển đổi tài liệu.
   Trung ngữ翻译:文档旋转──

Kết hợp việc lấp đầy văn bản + chuyển đổi câu tạo ra các số lượng thấp nhất. Bộ giải mã luôn tái tạo nguyên bản. Kết quả của BART là toàn bộ chuỗi, không chỉ là các khoảng thời gian bị hỏng  vì vậy tính toán trước khi tập là cao hơn T5.

> 组合文本填充 + 句排列产生最佳下游效果──解码器总是重建原本文本──BART's output is a complete sequence, not just a broken fragment

> **【中文解读】**T5 và BART có thể được đào tạo khác nhau: T5 chỉ có thể dự đoán được phá hủy một đoạn đoạn, hiệu quả cao, BART có thể tự lập trình lại toàn bộ bộ bộ trình tự, nhưng lại có giá cao hơn.

### Nhận định

Tạo tự động ngược giống như GPT. Phân tích tham lam / chùm / top-p áp dụng. Tìm kiếm chùm (thiều 45) là tiêu chuẩn cho dịch và tóm tắt vì phân phối đầu ra hẹp hơn trò chuyện.

> 推理与 GPT的自归生成相同──贪心/束搜索/top-p 采样都适用──束搜索(宽度 4-5) là một chiến lược tiêu chuẩn của翻译和摘要, vì输出分布比对话更窄──

> **【拓展：Beam Search 在翻译中的重要性】**编码器-解码器模型在翻译和摘要任务中常用束搜索(宽度 4-5), vì输出分布较窄. 束搜索维护多个候选序列,每步保留得分最高的几个继续扩展――相比贪心搜索,beam search 能找到更优的全局序列;相比随机采样,它更稳定――通常不需要束搜索,因为输出分布更广.

### Khi nào để chọn mỗi biến thể vào năm 2026

| Task | Encoder-decoder? | Why |
|------|------------------|-----|
| 任务 | 是否用编码器-解码器？ | 原因 |
| Translation | Yes, usually | Clear source sequence; fixed output distribution; beam search works |
| 翻译 | 通常是 | 明确的源序列；固定的输出分布；束搜索有效 |
| Speech-to-text | Yes (Whisper) | Input modality differs from output; encoder shapes audio features |
| 语音转文本 | 是（Whisper） | 输入模态与输出不同；编码器处理音频特征 |
| Chat / reasoning | No, decoder-only | No persistent "input" — the conversation is the sequence |
| 对话/推理 | 否，解码器专用 | 没有持久的"输入"——对话本身就是序列 |
| Code completion | Usually no | Decoder-only with long context wins; code models like Qwen 2.5 Coder are decoder-only |
| 代码补全 | 通常否 | 带长上下文的解码器专用胜出；Qwen 2.5 Coder 等代码模型是解码器专用 |
| Summarization | Either works | BART, PEGASUS beat earlier decoder-only baselines; modern decoder-only LLMs match them |
| 摘要 | 都可以 | BART、PEGASUS 超越早期解码器专用基线；现代解码器专用 LLM 能匹配它们 |
| Structured extraction | Either | T5 is clean because "text → text" absorbs any output format |
| 结构化提取 | 都可以 | T5 很干净，因为"文本 → 文本"可以吸收任何输出格式 |

Xu hướng từ ~2022: chỉ có trình giải mã tiếp quản các nhiệm vụ mà trình giải mã giải mã đã từng sở hữu bởi vì (a) các LLM chỉ có trình giải mã theo hướng dẫn tổng quát đến bất cứ thứ gì thông qua lời nhắc nhở, (b) một kiến trúc quy mô dễ dàng hơn hai, (c) RLHF giả định một trình giải mã.

> Từ năm 2022 xu hướng: giải mã chuyên dụng đã tiếp quản các nhiệm vụ mà编码器-解码器 từng sở hữu, vì (a) chỉ định nhỏ调的解码器专业 LLM 通过提示可以泛化到任何任务, (b) một cấu trúc đơn giản dễ dàng hơn hai mở rộng, (c) RLHF giả định sử dụng giải mã器.

> **【拓展：T5 的 text-to-text 统一范式】**T5's core psychological念是将所有 NLP 任务统一为"文本输入→文本输出"格式──翻译:"翻译英语为法语: Hello → Bonjour";分类:"sentiment: This film is great → positive"──这种统一简化了架构和训练流程,也后来指示调和快速工程的思想源头──Flan-T5 更是通过指令微调大幅提升了零样本能力──

## Hãy xây dựng nó.
```figure
encoder-decoder
```

## Hãy xây dựng nó

Nhìn xem`code/main.py`Chúng tôi thực hiện sự tham nhũng thời gian kiểu T5 cho một bộ đồ chơi. Đây là một phần hữu ích nhất của bài học này bởi vì nó xuất hiện trong mọi công thức trước khi tập lập trình và giải mã kể từ đó.

> 参见 `code/main.py` Chúng tôi thực hiện các đoạn phá kiểu T5 cho các trò chơi, đây là phần hữu ích nhất của bài học này, vì nó xuất hiện trong mỗi chương trình đào tạo dự kiến của các trình lập trình giải mã sau đây.

### Bước 1: sự tham nhũng span

```python
def corrupt_spans(tokens, mask_rate=0.15, mean_span=3.0, rng=None):
    """Pick spans summing to ~mask_rate of tokens. Return (corrupted_input, target)."""
    n = len(tokens)
    n_mask = max(1, int(n * mask_rate))
    n_spans = max(1, int(round(n_mask / mean_span)))
    ...
```

Các định dạng mục tiêu là T5 ước: `<sent0> span0 <sent1> span1 ...`. Lập nhập bị hỏng để lại các token không thay đổi với các token Sentinel tại các vị trí span.

> 目标格式 theo T5 约定:`<sent0> span0 <sent1> span1 ...` nhập được phá hủy sẽ không được thay đổi với token của vị trí trục quân 交替排列──

### Bước 2: xác minh đi lại và đi lại

Với các mục tiêu và đầu vào bị hỏng, hãy xây dựng lại câu gốc. Nếu sự hỏng của bạn là đảo ngược, thông qua trước được xác định rõ ràng. Đây là kiểm tra tâm lý  đào tạo thực sự không bao giờ làm điều này, nhưng bài kiểm tra rẻ và bắt được lỗi theo một trong sổ sách thời gian của bạn.

> 给定被破坏的输入和目标,重建原始句子──如果破坏是可逆的,前向传播就是良定义的──这是一个合理性检查真实训练从不这样做,但测试成本低且能发现片段记记中的差一错──

### Bước 3: BART tiếng ồn

Năm chức năng: `token_mask`- `token_delete`- `text_infill`- `sentence_permute`- `document_rotate`- Tạo hai trong số đó và cho thấy kết quả.

> 五个函数:`token_mask``token_delete``text_infill``sentence_permute``document_rotate`◊组合 trong số đó hai并 hiển thị kết quả

## Hãy sử dụng nó để thực hiện

Chuyện em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em em

> HuggingFace 参考:

```python
from transformers import T5ForConditionalGeneration, T5Tokenizer
tok = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

inputs = tok("translate English to French: Attention is all you need.", return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=32)
print(tok.decode(out[0], skip_special_tokens=True))
```

Trù T5: tên nhiệm vụ đi vào văn bản nhập. mô hình tương tự xử lý hàng chục nhiệm vụ vì mỗi nhiệm vụ là text-in, text-out. Năm 2026 mô hình này đã được phổ biến bởi các mô hình chỉ định-tuning decoder, nhưng T5 đã mã hóa nó trước.

> Kỹ năng của T5: Tên nhiệm vụ được viết trong văn bản nhập nhập. Một mô hình có thể xử lý hàng chục nhiệm vụ, vì mỗi nhiệm vụ đều là văn bản nhập- văn bản xuất. Năm 2026, mô hình này đã được chỉ định phổ biến mô hình chuyên dụng của máy giải mã, nhưng T5 là người đầu tiên quy định nó.

## Chuyển nó đi.

Nhìn xem`outputs/skill-seq2seq-picker.md`. Kỹ năng chọn giữa mã hóa-decoder và mã hóa-chỉ cho một nhiệm vụ mới do cấu trúc đầu vào-tả ra, độ trễ và mục tiêu chất lượng.

> 参见 `outputs/skill-seq2seq-picker.md` Kỹ năng này dựa trên cấu trúc nhập- Xuất 延迟和质量目标, cho nhiệm vụ mới chọn bộ lập trình- giải mã hoặc giải mã cụ thể cấu trúc.

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`, áp dụng sự tham nhũng khoảng thời gian cho một câu 30 token, xác minh rằng kết nối các token nguồn không phải Sentinel với các khoảng thời gian mục tiêu được giải mã tái tạo bản gốc.
   Trung ngữ翻译:运行 `code/main.py`, đối với một đoạn văn của 30 token phá hủy, xác nhận sẽ không gửi nguồn token và giải mã mục tiêu đoạn văn can be restored nguyên bản.
2. **Medium.**Thực hiện BART `text_infill`tiếng ồn: thay thế các khoảng thời gian ngẫu nhiên bằng một `<mask>`token, và decoder phải suy luận chiều dài span đúng cộng với nội dung.
   Trung ngữ翻译:实现 BART 的 `text_infill`噪音: dùng đơn `<mask>`token 替换随机片段,解码器 phải xác định đúng đoạn phim độ dài và nội dung.
3. **Hard.**- Đúng rồi.`flan-t5-small`trên một bộ hình tiếng Anh → Lâm-Latin nhỏ (200 cặp). đo BLEU trên một bộ 50 cặp kéo dài. So sánh với điều chỉnh tinh tế `Llama-3.2-1B`trên cùng một dữ liệu với cùng một tính toán.
   Trung ngữ翻译:在小型英语 → Lợn Latin 语料库(200对) 上微调 `flan-t5-small`◊ 50 số lượng phân tích BLEU trên tập hợp thử nghiệm được bỏ ra.`Llama-3.2-1B`Đối với...

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Encoder-decoder | "Seq2seq transformer" | Two stacks: bidirectional encoder for input, causal decoder with cross-attention for output. |
| 编码器-解码器 | "Seq2seq Transformer" | 两个堆栈：双向编码器处理输入，带交叉注意力的因果解码器生成输出。 |
| Cross-attention | "Where source talks to target" | Decoder's Q × encoder's K/V. The only place encoder information enters the decoder. |
| 交叉注意力 | "源与目标对话的地方" | 解码器的 Q × 编码器的 K/V。编码器信息进入解码器的唯一通道。 |
| Span corruption | "T5's pretraining trick" | Replace random spans with sentinel tokens; decoder outputs the spans. |
| 片段破坏 | "T5 的预训练技巧" | 用哨兵 token 替换随机片段；解码器输出这些片段。 |
| Denoising objective | "BART's game" | Apply a noise function to the input, train the decoder to reconstruct the clean sequence. |
| 去噪目标 | "BART 的游戏" | 对输入应用噪声函数，训练解码器重建干净序列。 |
| Sentinel token | "The `<extra_id_N>` placeholder" | Special tokens that tag corrupted spans in the source and re-tag them in the target. |
| 哨兵 token | "`<extra_id_N>` 占位符" | 在源端标记被破坏片段、在目标端重新标记的特殊 token。 |
| Flan | "Instruction-tuned T5" | T5 fine-tuned on >1,800 tasks; made encoder-decoder competitive at instruction-following. |
| Flan | "指令微调的 T5" | 在 1,800+ 任务上微调的 T5；使编码器-解码器在指令遵循方面具有竞争力。 |
| Beam search | "Decoding strategy" | Keep top-k partial sequences at each step; standard for translation/summarization. |
| 束搜索 | "解码策略" | 每步保留得分最高的 k 个部分序列；翻译/摘要的标准策略。 |
| Teacher forcing | "Training-time input" | During training, feed the true previous output token to the decoder, not the sampled one. |
| Teacher forcing | "训练时输入" | 训练时向解码器输入真实的上一个输出 token，而非采样的 token。 |

## Xem thêm 延伸阅读

- [Raffel et al. (2019). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683) T5.
  Trung văn翻译:T5 论文。
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461) BART.
  Trung ngữ翻译:BART 论文。
- [Chung et al. (2022). Scaling Instruction-Finetuned Language Models](https://arxiv.org/abs/2210.11416) Flan-T5.
  Trung văn翻译:Flan-T5 论文。
- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) Whisper, bộ mã hóa-tử toán của năm 2026
  Trung ngữ翻译:Whisper 论文,2026 年典型编码器-解码器模型──
- [HuggingFace `modeling_t5.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/t5/modeling_t5.py) thực hiện tham chiếu.
  Trung文翻译:HuggingFace T5 参考实现。
