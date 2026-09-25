# BERT  Mô hình hóa ngôn ngữ đeo mặt nạ ∙ BERT  掩码语言模型

> GPT dự đoán từ tiếp theo. BERT dự đoán một từ bị mất. Một câu khác biệt  và nửa thập kỷ của mọi thứ hình dạng nhúng.

> **【中文解读】**BERT là một bộ chuyển đổi chỉ có mã hóa, sử dụng lớp học dự đoán ẩn chứa.

**Type:** Hands-on | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Năm 2018, mỗi nhiệm vụ NLP  cảm xúc, NER, QA, liên quan  đã đào tạo mô hình riêng của nó từ đầu trên dữ liệu được dán nhãn của riêng nó. Không có điểm kiểm soát "nghiểu tiếng Anh" được đào tạo trước mà bạn có thể điều chỉnh. ELMo (2018) cho thấy bạn có thể đào tạo trước các nhúng ngữ cảnh bằng LSTM hai chiều; nó giúp nhưng không phổ biến.

> Năm 2018, mỗi nhiệm vụ NLP  phân tích cảm xúc、 đặt tên thực thể nhận dạng、 câu trả lời、 văn bản 含都需要在自己的标签数据上从零训练模型──当时没有预训的"理解英语"检查点可供微调──ELMo(2018) chứng minh có thể sử dụng hai chiều LSTM 预训上下文嵌入, nhưng khả năng phổ biến hạn──

BERT (Devlin et al. 2018) hỏi: nếu chúng ta lấy một bộ mã hóa biến đổi, đào tạo nó trên mỗi câu trên internet, và buộc nó dự đoán từ thiếu trong ngữ cảnh ở cả hai bên?

> BERT(Devlin 等人,2018) đưa ra một vấn đề quan trọng: Nếu sử dụng Transformer 编码器, trên tất cả các câu trên Internet, bắt buộc nó dựa trên hai bên trên các ngôn ngữ dự đoán bị che giấu từ, sẽ làm thế nào?

Kết quả: trong vòng 18 tháng BERT và các biến thể của nó (RoBERTa, ALBERT, ELECTRA) thống trị mọi bảng xếp hạng NLP hiện có. Đến năm 2020 mọi công cụ tìm kiếm, đường ống dẫn kiểm soát nội dung và hệ thống tìm kiếm ngữ nghĩa trên trái đất đều có BERT bên trong.

> Kết quả là: trong 18 tháng,BERT và các biến thể của nó (Robert Ta, Albert Electra) đã thống trị tất cả các bảng xếp hạng NLP cho đến năm 2020, mỗi công cụ tìm kiếm trên thế giới đều có một BERT trong các hệ thống tìm kiếm nội dung và kiểm tra nội dung.

Trong năm 2026, các mô hình chỉ có mã hóa vẫn là công cụ phù hợp để phân loại, lấy lại và lấy lại cấu trúc. Chúng chạy nhanh hơn 510x mỗi token so với các mã hóa và nhúng của chúng là xương sống của mọi ngăn xếp tìm kiếm hiện đại. ModernBERT (Dec 2024) đã đẩy kiến trúc đến bối cảnh 8K với Flash Attention + RoPE + GeGLU.

> Đến năm 2026, mô hình chuyên dụng của bộ lập trình vẫn là lựa chọn chính xác của phân loại, kiểm tra và cấu trúc.

> **【中文解读】**Sự cách mạng của BERT nằm trong mô hình "pre training+micro调": trên quy mô lớn không có dấu hiệu trên các ngôn ngữ sử dụng mô hình ngôn ngữ ẩn chứa (MLM) pre training, sau đó trong nhiệm vụ cụ thể nhỏ điều chỉnh số lượng tham số.

## Khái niệm cốt lõi

![Masked language modeling: pick tokens, mask them, predict originals](../assets/bert-mlm.svg)

### Đèn huấn luyện

Hãy lấy một câu:`the quick brown fox jumps over the lazy dog`- Tôi không biết.

> 取一个句子:`the quick brown fox jumps over the lazy dog`

Mái 15% mã thông báo theo cách ngẫu nhiên:

> 随机掩码 15% của token:

```
input:  the [MASK] brown fox jumps [MASK] the lazy dog
target: the quick brown fox jumps over the lazy dog
```

Tập mô hình để dự đoán các token gốc ở các vị trí che giấu.`[MASK]`ở vị trí 1 có thể sử dụng `brown fox jumps`ở vị trí 2+. Đó là điều mà GPT không thể làm.

> 训练模型在被掩藏位置预测原始代币――因为编码器 là hai chiều,预测位置 là 1 `[MASK]`Có thể sử dụng vị trí 2 及后的`brown fox jumps`Đó là điều GPT không làm được.

### Quy tắc mặt nạ BERT

Trong số 15% các token được chọn để dự đoán:

> Trong token được chọn để dự đoán 15% trong:

- 80% được thay thế bằng `[MASK]`- Tôi không biết.
  Trung ngữ翻译:80% 被替换为`[MASK]`
- 10% được thay thế bằng một token ngẫu nhiên.
  Trung ngữ翻译:10% được thay thế cho biểu tượng tự nhiên.
- 10% vẫn không thay đổi.
  Trung ngữ翻译:10% 保持不变──

Tại sao không phải lúc nào cũng vậy?`[MASK]`Vì...`[MASK]`Không bao giờ xuất hiện tại thời điểm suy luận.`[MASK]`ở 100% các vị trí che giấu sẽ tạo ra sự thay đổi phân phối giữa việc tập luyện trước và điều chỉnh tinh tế. 10% ngẫu nhiên + 10% không thay đổi giữ cho mô hình trung thực.

> Tại sao không luôn luôn được sử dụng?`[MASK]`? vì `[MASK]`Trong thời gian suy nghĩ sẽ không bao giờ xuất hiện. Nếu mô hình đào tạo ở vị trí ẩn 100%, bạn mong đợi thấy.`[MASK]`, sẽ gây ra sự phân chia chuyển biến giữa dự phòng đào tạo và điều chỉnh nhỏ.

> **【中文解读】**Các quy tắc của BERT 掩码的三条规则 ((80% [MASK]、10% 随机替换、10% 保持不变) nhằm mục đích giảm thiểu sự phân chia giữa dự phòng đào tạo và điều chỉnh nhỏ.

> **【拓展：BERT 在 RAG 系统中的角色】**Trong hệ thống RAG hiện đại, BERT 变体 vẫn là trung tâm của giai đoạn检索. Các mô hình chuyển đổi câu nói giống như tất cả MiniLM-L6-v2) bản chất là sử dụng để so sánh học tập nhỏ của BERT.

### Next Sentence Prediction (NSP)  và tại sao nó đã bị bỏ rơi

BERT gốc cũng được đào tạo về NSP: được đưa ra hai câu A và B, dự đoán nếu B theo A. RoBERTa (2019) đã xóa nó và cho thấy NSP bị tổn thương, không giúp đỡ.

> Trong khi đó, các máy tính lập trình hiện đại đã sử dụng nó.

### Điều gì đã thay đổi vào năm 2026: ModernBERT

Bảng ModernBERT năm 2024 đã xây dựng lại khối với những nguyên thủy năm 2026:

> ModernBERT năm 2024 论文用现代组件重建编码器块:

| Component | Original BERT (2018) | ModernBERT (2024) |
|-----------|----------------------|-------------------|
| 组件 | 原始 BERT (2018) | ModernBERT (2024) |
| Positional | Learned absolute | RoPE |
| 位置编码 | 学习式绝对位置 | RoPE |
| Activation | GELU | GeGLU |
| 激活函数 | GELU | GeGLU |
| Normalization | LayerNorm | Pre-norm RMSNorm |
| 归一化 | LayerNorm | 前归一化 RMSNorm |
| Attention | Full dense | Alternating local (128) + global |
| 注意力 | 全密集 | 交替局部 (128) + 全局 |
| Context length | 512 | 8192 |
| 上下文长度 | 512 | 8192 |
| Tokenizer | WordPiece | BPE |
| 分词器 | WordPiece | BPE |

Và không giống như đống 2018 , nó là Flash-Attention-native. Inference là 23x nhanh hơn với độ dài chuỗi 8K so với DeBERTa-v3 với điểm số GLUE tốt hơn.

> Không giống như công nghệ năm 2018, ModernBERT nguyên sinh hỗ trợ Flash Attention.

### Use cases vẫn chọn một encoder vào năm 2026

| Task | Why encoder beats decoder |
|------|---------------------------|
| 任务 | 为什么编码器优于解码器 |
| Retrieval / semantic search embeddings | Bidirectional context = better embedding quality per token |
| 检索/语义搜索嵌入 | 双向上下文 = 每个 token 更好的嵌入质量 |
| Classification (sentiment, intent, toxicity) | One forward pass; no generation overhead |
| 分类（情感、意图、毒性） | 一次前向传播；无生成开销 |
| NER / token labeling | Per-position output, natively bidirectional |
| NER/token 标注 | 逐位置输出，天然双向 |
| Zero-shot entailment (NLI) | Classifier head on top of encoder |
| 零样本蕴含 (NLI) | 编码器之上的分类器头 |
| Reranker for RAG | Cross-encoder scoring, 10x faster than LLM rerankers |
| RAG 重排序器 | 交叉编码器评分，比 LLM 重排序器快 10 倍 |

## Hãy xây dựng nó.
```figure
transformer-residual
```

## Hãy xây dựng nó

### Bước 1: Hình lý che giấu

Nhìn xem`code/main.py`- chức năng`create_mlm_batch`lấy danh sách các thẻ ID, kích thước từ ngữ và xác suất mặt nạ. trả về các thẻ ID đầu vào (với mặt nạ được áp dụng) và nhãn (chỉ ở các vị trí che giấu, -100 ở nơi khác  Phản ứng chỉ số của PyTorch).

> 参见 `code/main.py`◊ hàm`create_mlm_batch` chấp nhận mã thông báo 列表、词表大小和掩码概率, quay lại nhập ID(已应用掩码) 和标签( chỉ có giá trị ở vị trí ẩn, số dư là -100PyTorch của 忽略索引约定)

```python
def create_mlm_batch(tokens, vocab_size, mask_prob=0.15, rng=None):
    input_ids = list(tokens)
    labels = [-100] * len(tokens)
    for i, t in enumerate(tokens):
        if rng.random() < mask_prob:
            labels[i] = t
            r = rng.random()
            if r < 0.8:
                input_ids[i] = MASK_ID
            elif r < 0.9:
                input_ids[i] = rng.randrange(vocab_size)
            # else: keep original
    return input_ids, labels
```

### Bước 2: chạy dự đoán MLM trên một cơ thể nhỏ

Căn luyện một bộ mã hóa 2 lớp + đầu MLM trên một từ vựng 20 từ, 200 câu. Không gradient  chúng tôi làm kiểm tra tâm trí tiến hành.

> Trong 20 từ từ và 200 câu tập luyện một bộ lập trình 2 tầng + MLM 头―― không liên quan đến độ  chỉ làm kiểm tra hợp lý của việc truyền tải trước .

### Bước 3: so sánh các loại mặt nạ

Hãy cho thấy cách thức của quy tắc ba chiều giữ cho mô hình có thể sử dụng mà không cần `[MASK]`- Dự đoán về một câu không che giấu và một câu che giấu. Cả hai đều nên tạo ra phân phối biểu tượng hợp lý bởi vì mô hình đã thấy cả hai mô hình trong đào tạo.

> 展示三路规则 làm thế nào để mô hình trong không có `[MASK]`Trong trường hợp vẫn có thể sử dụng. Đối với các câu không ẩn và câu ẩn khác nhau dự đoán. Cả hai đều nên tạo ra một phân bố có lý, vì mô hình đã thấy hai mô hình trong đào tạo.

### Bước 4: đầu tinh chỉnh

Thay thế đầu MLM bằng đầu phân loại trên bộ dữ liệu cảm xúc đồ chơi. Chỉ có đầu tàu; bộ mã hóa bị đóng băng. Đây là mô hình mà mọi ứng dụng BERT theo.

> Sử dụng phân loại đầu thay thế đầu MLM, tập trên một tập dữ liệu cảm xúc đồ chơi. Chỉ có đầu đầu tập, coder kết thúc. Đây là mô hình tiêu chuẩn của mỗi ứng dụng BERT.

> **【拓展：BERT 微调的实践技巧】**Các thực hành tốt nhất của BERT 微调 bao gồm: 1) Sử dụng tỷ lệ học nhỏ hơn(2e-5 đến 5e-5) tránh phá vỡ trọng lượng đào tạo trước; 2) Xuất khẩu của mã thông báo cho các loại nhiệm vụ phân loại (CLS) như một biểu hiện cụm từ; 3) Ứng dụng cho các mã thông báo NER và các mã thông báo cho từng nhiệm vụ; 4) Xác giải từng bước (Gradual unfreezing) có thể nâng cao khả năng phát triển trên tập dữ liệu nhỏ.

## Hãy sử dụng nó để thực hiện

```python
from transformers import AutoModel, AutoTokenizer

tok = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base")

text = "Attention is all you need."
inputs = tok(text, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, N, 768)
```

**Embedding models are fine-tuned BERT.** `sentence-transformers`mô hình như `all-MiniLM-L6-v2`BRT được đào tạo với mất mát tương phản.

> **嵌入模型是微调后的 BERT。** `sentence-transformers`模型如 `all-MiniLM-L6-v2`Về bản chất là tương tự với các mô hình BERT của bài tập mất mát.

**Cross-encoder rerankers are also fine-tuned BERT.**Định dạng cặp trên `[CLS] query [SEP] doc [SEP]`Sự chú ý hai chiều giữa truy vấn và doc chính là điều cung cấp cho cross-encoder cạnh chất lượng của họ so với biencoders.

> **交叉编码器重排序器也是微调后的 BERT。**Trong `[CLS] query [SEP] doc [SEP]`Việc phân loại phân loại trên. Sự chú ý hai chiều giữa truy vấn và tài liệu chính là lý do tại sao chất lượng máy biên tập giao dịch tốt hơn máy biên tập đôi.

**When not to pick BERT in 2026.**Bất cứ thứ gì tạo ra. Các mã hóa không có cách hợp lý để tự tạo ra các token. Ngoài ra: bất cứ thứ gì dưới các tham số 1B nơi một decoder nhỏ có thể phù hợp với chất lượng với tính linh hoạt hơn (Phi-3-Mini, Qwen2-1.5B).

> **2026 年何时不选 BERT。**任何生成式任务──编码器 không có cách hợp lý để tự quay lại token 生成──此外, trong các trường hợp dưới đây, các giải mã nhỏ như Phi-3-Mini、Qwen2-1.5B) có thể sử dụng các tham số ít hơn để có được sự linh hoạt tương đương──

> **【拓展：ModernBERT 的现代化改进】**ModernBERT(2024) sẽ 2018 BERT  cấu trúc nâng cấp toàn diện:RoPE  thay thế học tập kiểu vị trí编码、GeGLU  thay thế GELU、 trước归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归 LayerNorm、交替使用局部和全局注意力以支持8K 上下文──推理速度比DeBERTa-v3 快2-3倍,同时 GLUE 分数更高──

## Chuyển nó đi.

Nhìn xem`outputs/skill-bert-finetuner.md`. Khả năng mở rộng một sự điều chỉnh BERT (chọn lựa xương sống, đặc điểm đầu, dữ liệu, đánh giá, dừng) cho một nhiệm vụ phân loại hoặc khai thác mới.

> 参见 `outputs/skill-bert-finetuner.md` Kỹ năng này là một phần của các kỹ năng mới trong việc phân loại hoặc lập kế hoạch nhiệm vụ (BERT) 微调方案 (BTC) 

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`Và in phân phối mặt nạ trên 10.000 token. xác nhận ~ 15% được chọn, và ~ 80% trở thành `[MASK]`- Tôi không biết.
   Trung ngữ翻译:运行 `code/main.py`, in 10.000 token của sự phân phối ẩn chứa ∞ xác nhận khoảng 15% được chọn, trong đó khoảng 80% ∞ biến đổi ∞`[MASK]`
2. **Medium.**Thực hiện che giấu toàn từ: nếu một từ được mã hóa thành các từ phụ, che giấu tất cả các từ phụ cùng nhau hoặc không. đo lường xem điều này có cải thiện độ chính xác MLM trên một tập hợp 500 câu không.
   Trung ngữ翻译:实现全词掩码: Nếu một từ được phân词为多个子词, hoặc là全部掩码 hoặc là全部不掩码.
3. **Hard.**Trình luyện một BERT nhỏ (2 lớp, d=64) trên 10.000 câu từ một tập dữ liệu công cộng.`[CLS]`So sánh với một đường cơ sở chỉ có trình giải mã ở các param phù hợp  nào thắng?
   Trung ngữ翻译: 在公开数据集的10,000个句子上训练一个小型(2层,d=64)BERT──微调 `[CLS]`token được sử dụng cho SST-2 情感分类.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| MLM | "Masked language modeling" | Training signal: randomly replace 15% of tokens with `[MASK]`, predict the originals. |
| MLM | "掩码语言建模" | 训练信号：随机将 15% 的 token 替换为 `[MASK]`，预测原始 token。 |
| Bidirectional | "Looks both ways" | Encoder attention has no causal mask — every position sees every other position. |
| 双向 | "看两边" | 编码器注意力没有因果掩码——每个位置都能看到其他所有位置。 |
| `[CLS]` | "The pooler token" | A special token prepended to every sequence; its final embedding is used as the sentence-level representation. |
| `[CLS]` | "池化 token" | 一个特殊 token，添加到每个序列开头；其最终嵌入用作句子级表示。 |
| `[SEP]` | "Segment separator" | Separates paired sequences (e.g. query/doc, sentence A/B). |
| `[SEP]` | "片段分隔符" | 分隔成对序列（如查询/文档、句子 A/B）。 |
| NSP | "Next sentence prediction" | BERT's second pretraining task; shown to be useless in RoBERTa, dropped after 2019. |
| NSP | "下一句预测" | BERT 的第二个预训练任务；RoBERTa 证明其无用，2019 年后弃用。 |
| Fine-tuning | "Adapt to a task" | Keep the encoder mostly frozen; train a small head on top for the downstream task. |
| 微调 | "适应任务" | 保持编码器基本冻结；在顶部训练一个小头用于下游任务。 |
| Cross-encoder | "A reranker" | A BERT that takes both query and doc as input, outputs a relevance score. |
| 交叉编码器 | "重排序器" | 同时接收查询和文档作为输入的 BERT，输出相关性分数。 |
| ModernBERT | "2024 refresh" | Encoder rebuilt with RoPE, RMSNorm, GeGLU, alternating local/global attention, 8K context. |
| ModernBERT | "2024 刷新版" | 用 RoPE、RMSNorm、GeGLU、交替局部/全局注意力重建的编码器，8K 上下文。 |

## Xem thêm 延伸阅读

- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805) giấy gốc.
  Trung ngữ翻译:BERT 原始论文。
- [Liu et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692) cách đào tạo BERT đúng cách; giết chết NSP.
  Trung文翻译:如何正确训练 BERT; chứng minh NSP 无用──
- [Clark et al. (2020). ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators](https://arxiv.org/abs/2003.10555) phát hiện mã hóa thay thế vượt qua MLM ở tính toán phù hợp.
  Trung文翻译:替换代币检测在相同计算量下优于MLM。
- [Warner et al. (2024). Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder](https://arxiv.org/abs/2412.13663) Báo ModernBERT.
  Trung văn翻译:ModernBERT 论文。
- [HuggingFace `modeling_bert.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/bert/modeling_bert.py) tham chiếu mã hóa theo quy định.
  Trung文翻译:HuggingFace BERT 模型实现参考代码──
