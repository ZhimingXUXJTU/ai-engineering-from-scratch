# Tên gọi: ĐHN

> Nghe dễ dàng cho đến khi bạn đối phó với ranh giới mơ hồ, các thực thể tổ và thuật ngữ miền.
> Hãy đưa tên ra ngoài. Nghe như đơn giản, cho đến khi bạn gặp gỡ mờ giới giới.

> **【中文解读】**Từ văn bản nhận dạng người tên, địa danh, tổ chức tên, và các thực thể khác.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word Embeddings) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 5 · 03（词嵌入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

"Apple đã kiện Google về thỏa thuận tìm kiếm iPhone của mình ở Mỹ". Năm thực thể: Apple (ORG), Google (ORG), iPhone (PRODUCT), thỏa thuận tìm kiếm (có lẽ), US (GPE).

> "Apple kiện Google về thỏa thuận tìm kiếm iPhone của mình ở Mỹ". 五个实体:Apple(ORG)、Google(ORG)、iPhone(PRODUCT)、 tìm kiếm thỏa thuận(可能)、US(GPE)。 một NER tốt 系统能正确提取所有实体及其类型──一个差的系统会遗漏 iPhone,把水果 Apple 和公司 Apple 混,把"US"标记为 PERSON──

NER là con ngựa làm việc dưới mỗi đường ống dẫn khai thác có cấu trúc. Phân tích sơ khai, quét nhật ký tuân thủ, ẩn danh hồ sơ y tế, hiểu truy vấn tìm kiếm, cơ sở cho các phản ứng chatbot, khai thác hợp đồng pháp lý. Bạn không bao giờ hoàn toàn thấy nó; bạn luôn phụ thuộc vào nó.

> NER là một công cụ làm việc dưới mỗi dòng nước cấu trúc. Bạn hầu như không nhìn vào nó, nhưng bạn luôn phụ thuộc vào nó.

Bài học này đi theo con đường cổ điển (thương pháp dựa trên quy tắc, HMM, CRF) vào con đường hiện đại (BiLSTM-CRF, sau đó là các biến đổi).

> Bài học này từ các đường lối cổ điển (基于规则, HMM, CRF) hướng tới các đường lối hiện đại (BiLSTM-CRF, rồi là Transformer) ⋅ từng bước đều giải quyết được những hạn chế cụ thể của bước trước.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

**BIO tagging**(hoặc BILOU) biến khai thác thực thể thành một vấn đề gắn nhãn chuỗi.`B-TYPE`(sự khởi đầu của tổ chức), `I-TYPE`(các tổ chức bên trong), hoặc `O`(ngoài bất kỳ đơn vị nào).

> **BIO 标注**(hoặc BILOU) sẽ được chuyển đổi thành các vấn đề ký hiệu chuỗi.`B-TYPE`(实体开始)`I-TYPE`(trực thể nội bộ) hoặc `O`(không có bất kỳ thực thể nào)

```
Apple    B-ORG
sued     O
Google   B-ORG
over     O
its      O
iPhone   B-PRODUCT
search   O
deal     O
in       O
the      O
US       B-GPE
.        O
```

Dòng các đơn vị đa token: `New B-GPE`- `York I-GPE`- `City I-GPE`Một mô hình hiểu được BIO có thể thu thập các khoảng thời gian tùy ý.

> 多 token 实体链接:`New B-GPE``York I-GPE``City I-GPE`❖ hiểu mô hình của BIO có thể được sử dụng bất kỳ chiều dài nào.

Sự tiến triển kiến trúc:

> 架构演进:

- **Rule-based.**Tìm kiếm Regex + báo chí. độ chính xác cao trên các thực thể đã biết, không bao gồm các thực thể mới.
  **基于规则。**正则 + 地名词典查找── đối với vật thể đã biết cao tỷ lệ xác định, đối với vật thể mới零覆盖──
- **HMM.**Mô hình Markov ẩn, xác suất phát hành của thẻ token, xác suất chuyển đổi từ thẻ đến thẻ, mã hóa Viterbi, được đào tạo trên dữ liệu được dán nhãn.
  **HMM。**隐马尔可夫模型――给定标签的代币 发射概率,标签间转移概率――Viterbi 解码――在标签数据上训练――
- **CRF.**Field Random Conditional. Giống như HMM nhưng phân biệt đối xử, vì vậy bạn có thể trộn các tính năng tùy tiện (phụng chữ, chữ viết to, từ lân cận).
  **CRF。**条件随机场──类似于 HMM nhưng判别式, vì vậy có thể hỗn hợp bất kỳ đặc điểm nào 词形、大小写、相邻词)── đến năm 2026 vẫn là lực lượng sản xuất cổ điển của Bộ Bộ Bộ Tài nguyên Ranh (Low Resource Deployment).
- **BiLSTM-CRF.**Các tính năng thần kinh thay vì làm bằng tay. LSTM đọc câu cả hai hướng, lớp CRF ở trên thực thi các chuỗi thẻ nhất quán.
  **BiLSTM-CRF。**神经特征代替手工特征──LSTM 双向读取句子,顶部CRF层强制一致的标签序列──
- **Transformer-based.**Định chỉnh BERT với đầu phân loại token, độ chính xác tốt nhất, tính toán tốt nhất.
  **基于 Transformer。**Sử dụng mã số 分类头微调 BERT──最佳准确率──最多计算量──

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
ner-bio-tagging
```

## Hãy xây dựng nó

### Bước 1: Đánh dấu BIO trợ lý

```python
def spans_to_bio(tokens, spans):
    labels = ["O"] * len(tokens)
    for start, end, label in spans:
        labels[start] = f"B-{label}"
        for i in range(start + 1, end):
            labels[i] = f"I-{label}"
    return labels


def bio_to_spans(tokens, labels):
    spans = []
    current = None
    for i, label in enumerate(labels):
        if label.startswith("B-"):
            if current:
                spans.append(current)
            current = (i, i + 1, label[2:])
        elif label.startswith("I-") and current and current[2] == label[2:]:
            current = (current[0], i + 1, current[2])
        else:
            if current:
                spans.append(current)
                current = None
    if current:
        spans.append(current)
    return spans
```

```python
>>> tokens = ["Apple", "sued", "Google", "over", "iPhone", "sales", "."]
>>> labels = ["B-ORG", "O", "B-ORG", "O", "B-PRODUCT", "O", "O"]
>>> bio_to_spans(tokens, labels)
[(0, 1, 'ORG'), (2, 3, 'ORG'), (4, 5, 'PRODUCT')]
```

### Bước 2: Các tính năng được làm bằng tay

Đối với NER cổ điển (không thần kinh), các tính năng là trò chơi.

> Đối với các loại loại loại khác, đặc điểm là quan trọng.

```python
def token_features(token, prev_token, next_token):
    return {
        "lower": token.lower(),
        "is_upper": token.isupper(),
        "is_title": token.istitle(),
        "has_digit": any(c.isdigit() for c in token),
        "suffix_3": token[-3:].lower(),
        "shape": word_shape(token),
        "prev_lower": prev_token.lower() if prev_token else "<BOS>",
        "next_lower": next_token.lower() if next_token else "<EOS>",
    }


def word_shape(word):
    out = []
    for c in word:
        if c.isupper():
            out.append("X")
        elif c.islower():
            out.append("x")
        elif c.isdigit():
            out.append("d")
        else:
            out.append(c)
    return "".join(out)
```

`word_shape("iPhone")`trả lại `xXxxxx`- `word_shape("USA-2024")`trả lại `XXX-dddd`Các mô hình vốn hóa là tín hiệu cao cho các từ chính xác.

> `word_shape("iPhone")` quay lại `xXxxxx``word_shape("USA-2024")` quay lại `XXX-dddd`◊                                                                                                                                                                                                                                                              

### Bước 3: một quy tắc đơn giản + từ điển cơ sở

```python
ORG_GAZETTEER = {"Apple", "Google", "Microsoft", "OpenAI", "Meta", "Amazon", "Netflix"}
GPE_GAZETTEER = {"US", "USA", "UK", "India", "Germany", "France"}
PRODUCT_GAZETTEER = {"iPhone", "Android", "Windows", "ChatGPT", "Claude"}


def rule_based_ner(tokens):
    labels = []
    for token in tokens:
        if token in ORG_GAZETTEER:
            labels.append("B-ORG")
        elif token in GPE_GAZETTEER:
            labels.append("B-GPE")
        elif token in PRODUCT_GAZETTEER:
            labels.append("B-PRODUCT")
        else:
            labels.append("O")
    return labels
```

Các tờ báo sản xuất có hàng triệu mục được thu thập từ Wikipedia và DBpedia.`Apple`(The company vs. the fruit) là khủng khiếp. Đó là lý do tại sao các mô hình thống kê đã thắng.

> 生产地名词典 có hàng triệu条目, từ Wikipedia 和 DBpedia 抓取──覆盖率不错──消歧(公司 `Apple`vs 水果 `apple`Đó là lý do mà mô hình thống kê thắng.

### Bước 4: Bước CRF (phác thảo, không phải impl hoàn chỉnh)

CRF đầy đủ từ đầu trong 50 dòng không có sự sáng tỏ mà không có cơ sở lý thuyết xác suất.`sklearn-crfsuite`thay vào đó:

> Không có cơ sở về tỷ lệ có thể thực hiện toàn bộ CRF trong vòng 50 行 từ 0 đến không khôn ngoan.`sklearn-crfsuite`- Có thể là:

```python
import sklearn_crfsuite

def to_features(tokens):
    out = []
    for i, tok in enumerate(tokens):
        prev = tokens[i - 1] if i > 0 else ""
        nxt = tokens[i + 1] if i + 1 < len(tokens) else ""
        out.append({
            "word.lower()": tok.lower(),
            "word.isupper()": tok.isupper(),
            "word.istitle()": tok.istitle(),
            "word.isdigit()": tok.isdigit(),
            "word.suffix3": tok[-3:].lower(),
            "word.shape": word_shape(tok),
            "prev.word.lower()": prev.lower(),
            "next.word.lower()": nxt.lower(),
            "BOS": i == 0,
            "EOS": i == len(tokens) - 1,
        })
    return out


crf = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True)
X_train = [to_features(s) for s in sentences_tokenized]
crf.fit(X_train, bio_labels_train)
```

`c1`và `c2`là L1 và L2 đều được điều chỉnh. `all_possible_transitions=True`cho phép mô hình học các chuỗi bất hợp pháp (ví dụ:`I-ORG`sau đó`O`) không có khả năng, đó là cách mà một CRF thực thi sự phù hợp của BIO mà không cần bạn viết ra giới hạn.

> `c1`和 `c2`là L1 và L2 chính thức.`all_possible_transitions=True`让模型学习非法序列 (tức là:`O` sau đó xuất hiện `I-ORG`) không quá khả thi, đó là cách CRF buộc BIO một chiều trong trường hợp bạn không viết ràng buộc.

### Bước 5: BiLSTM-CRF thêm gì

Các tính năng được học. Các đầu vào: token embed (GloVe hoặc fastText). LSTM đọc từ trái sang phải và phải sang trái. Các trạng thái ẩn bị kết hợp đi qua một lớp sản xuất CRF. CRF vẫn áp dụng tính nhất quán chuỗi thẻ; LSTM thay thế các tính năng thủ công bằng các tính năng được học.

> Trẻ biến thành học được của. 输入:token 嵌入(GloVe hoặc fastText) ⋅LSTM Từ trái sang phải và từ phải sang trái读取──拼接的隐藏状态通过CRF 输出层──CRF 仍然强制标签序列一致性;LSTM 用到的特征替代手工特征──

```python
import torch
import torch.nn as nn


class BiLSTM_CRF_Head(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_labels):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(hidden_dim * 2, n_labels)

    def forward(self, token_ids):
        e = self.embed(token_ids)
        h, _ = self.lstm(e)
        emissions = self.fc(h)
        return emissions
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

Đối với lớp CRF, sử dụng `torchcrf.CRF`(pip cài đặt pytorch-crf). lợi nhuận trên CRF thủ công là có thể đo lường nhưng nhỏ hơn bạn mong đợi trừ khi bạn có hàng chục ngàn câu được dán nhãn.

> CRF 层使用 `torchcrf.CRF`(Pip cài đặt pytorch-crf) ⋅ Tăng của CRF so với các máy tính thủ công là có thể đo lường, nhưng so với bạn mong đợi nhỏ, trừ khi bạn có hàng triệu dấu chấm câu ⋅

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

spaCy đưa NER cấp sản xuất ra khỏi hộp.

> Space 开箱即用提供生产级 NER.

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple sued Google over its iPhone search deal in the US.")
for ent in doc.ents:
    print(f"{ent.text:20s} {ent.label_}")
```

```
Apple                ORG
Google               ORG
iPhone               ORG
US                   GPE
```

Lưu ý`iPhone`được dán nhãn`ORG`thay vì`PRODUCT` Mô hình nhỏ của spaCy có sự bảo hiểm đối với các đơn vị sản phẩm yếu.`en_core_web_lg`(văn hình biến đổi)`en_core_web_trf`) làm tốt hơn nữa.

> chú ý`iPhone`Được ghi nhận`ORG`Không`PRODUCT` mô hình nhỏ của không gian đối với sự phủ kín của vật thể sản phẩm kém hơn.`en_core_web_lg`(更好──Tranformator 模型)`en_core_web_trf`(của tôi là một người tốt hơn)

Nhấp mặt cho NER dựa trên BERT:

> NER dựa trên BERT của Hugging Face:

```python
from transformers import pipeline

ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
print(ner("Apple sued Google over its iPhone in the US."))
```

```
[{'entity_group': 'ORG', 'word': 'Apple', ...},
 {'entity_group': 'ORG', 'word': 'Google', ...},
 {'entity_group': 'MISC', 'word': 'iPhone', ...},
 {'entity_group': 'LOC', 'word': 'US', ...}]
```

`aggregation_strategy="simple"`nếu bạn kết hợp các token B-X, I-X liên kết thành một span. mà không có nó, bạn sẽ nhận được các nhãn cấp token và phải tự kết hợp.

> `aggregation_strategy="simple"`Sẽ liên tục B-X ∞ I-X token 合并 cho một跨度. Không có nó, bạn nhận được token 级标签, cần tự hợp并.

### NER dựa trên LLM (tương tự là 2026)

LLM NER không bắn và ít bắn hiện nay cạnh tranh với các mô hình được điều chỉnh tốt trên nhiều lĩnh vực, và tốt hơn đáng kể khi dữ liệu được dán nhãn là hiếm.

> 零样本和少样本 LLM NER hiện đang cạnh tranh với mô hình nhỏ trong nhiều lĩnh vực, có lợi thế lớn hơn trong thời điểm thiếu dữ liệu nhãn hiệu.

- **Zero-shot prompting.**Đưa cho LLM một danh sách các loại thực thể và một sơ đồ ví dụ.
  **零样本提示。** Đưa cho LLM một danh sách và mô hình mô hình thể chất  yêu cầu JSON 输出 开箱即用; trong lĩnh vực mới 准确率中等
- **ZeroTuneBio-style prompting.**Phân tích nhiệm vụ thành khai thác ứng viên → nghĩa giải thích → phán xét → kiểm tra lại. Một lời nhắc nhiều giai đoạn (không phải một lần) nâng độ chính xác đáng kể trên NER y sinh.
  **ZeroTuneBio 风格提示。**将任务分解为候选抽取 → 含义解释 → 判断 → 复查──多阶段提示(而不是一次性) trong ngành Y học sinh NER tăng đáng kể tỷ lệ xác thực──
- **Dynamic prompting with RAG.**Nhận lại các ví dụ có nhãn tương tự nhất từ một bộ hạt giống nhỏ có chú thích cho mỗi cuộc gọi suy luận; xây dựng các cú nhắc vài lần trên đường bay.
  **动态 RAG 提示。**Mỗi lần điều chỉnh lý luận từ ít nhãn phân loại tập trung kiểm tra mẫu nhãn tương tự nhất; động thái xây dựng ít mẫu mẫu提示. Trong thử nghiệm基准 năm 2026, điều này đã làm cho GPT-4 生物医学 NER F1 tăng 11-12% so với các mẫu tĩnh提示.
- **Per-entity-type decomposition.**Đối với các tài liệu dài, một cuộc gọi duy nhất trích xuất tất cả các loại thực thể cùng một lúc sẽ mất hồi tưởng khi chiều dài tăng lên.
  **按实体类型分解。**Đối với các tài liệu dài, một lần sử dụng lấy tất cả các loại vật thể, theo thời gian tăng tỷ lệ mất tập trung.

khuyến nghị sản xuất từ năm 2026: bắt đầu với một điểm khởi đầu bằng LLM trước khi thu thập dữ liệu đào tạo.

> 2026 năm sản xuất khuyến nghị: trước khi thu thập dữ liệu đào tạo, hãy bắt đầu sử dụng LLM 零样本基线.

### Khi NER cổ điển vẫn thắng

Ngay cả khi có LLM có sẵn, NER cổ điển thắng khi:

> Ngay cả khi có LLM có thể sử dụng, NER kinh điển trong các trường hợp sau đây:

- Ngân sách trễ dưới 50ms.
  延迟预算 thấp hơn 50 毫秒.
- Bạn có hàng ngàn ví dụ được dán nhãn và cần 98% + F1.
  Anh có hàng ngàn mẫu nhãn và cần 98% + F1
- Khu vực có một ontology ổn định nơi một CRF hoặc BiLSTM được đào tạo trước chuyển giao tốt.
   lĩnh vực có cơ bản ổn định, dự kiến đào tạo của CRF hoặc BiLSTM 迁移良好──
- Các hạn chế quy định đòi hỏi một mô hình không tạo ra trên địa điểm.
  监管约束要求本地部署的非生成式模型──

### Ở đâu nó rơi ra

- **Domain shift.**NER có chuyên môn hợp đồng pháp lý tốt hơn một nhà báo.
  **领域偏移。**Trong CoNLL trên đào tạo của NER  xử lý pháp luật hợp đồng thời so với từ ngữ cũng khác nhau.
- **Nested entities.**"Bank of America Tower" là một ORG và một FASILITY. BIO tiêu chuẩn không thể đại diện cho các khoảng cách chồng chéo. Bạn cần NER nhúng (những mô hình đa vượt hoặc dựa trên khoảng cách).
  **嵌套实体。**"Bank of America Tower" đồng thời là ORG và FASILITY. Biô chuẩn không thể biểu thị quá trình chồng lên.
- **Long entities.**"Công ty bảo hiểm tiền gửi liên bang Hoa Kỳ". Các mô hình cấp token đôi khi chia rẽ điều này. Sử dụng `aggregation_strategy`hoặc sau quá trình.
  **长实体。**"United States Federal Deposit Insurance Corporation".""`aggregation_strategy`Hoặc xử lý sau.
- **Sparse types.**Các nhãn NER y tế như DRUG_BRAND, ADVERSE_EVENT, DOSE. Các mô hình sử dụng chung không có ý tưởng. Scispacy và BioBERT là điểm khởi đầu ở đây.
  **稀疏类型。**医疗 NER 标签如Drug_BRAND、ADVERSE_EVENT、DOSE。通用模型一无所知。Scispacy 和 BioBERT là điểm khởi đầu ở đó。

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

## Chuyển nó đi.

Cứ như `outputs/skill-ner-picker.md`- Có thể là:

> 保存为 `outputs/skill-ner-picker.md`- Có thể là:

```markdown
---
name: ner-picker
description: Pick the right NER approach for a given extraction task.
version: 1.0.0
phase: 5
lesson: 06
tags: [nlp, ner, extraction]
---

Given a task description (domain, label set, language, latency, data volume), output:

1. Approach. Rule-based + gazetteer, CRF, BiLSTM-CRF, or transformer fine-tune.
2. Starting model. Name it (spaCy model ID, Hugging Face checkpoint ID, or "custom, trained from scratch").
3. Labeling strategy. BIO, BILOU, or span-based. Justify in one sentence.
4. Evaluation. Use `seqeval`. Always report entity-level F1 (not token-level).

Refuse to recommend fine-tuning a transformer for under 500 labeled examples unless the user already has a pretrained domain model. Flag nested entities as needing span-based or multi-pass models. Require a gazetteer audit if the user mentions "production scale" and labels are unchanged from CoNLL-2003.
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Tập luyện bài tập

1. **Easy.**Thực hiện`bio_to_spans`(người ngược lại của `spans_to_bio`) và kiểm tra sự phù hợp về lại và về trên 10 câu.
   **简单。**实现 `bio_to_spans`(`spans_to_bio`của hàm ngược) và trên 10 câu xác minh về sự nhất quán.
2. **Medium.**Đào tạo các sklearn-crfsuite CRF trên trên trên bộ dữ liệu NER tiếng Anh CoNLL-2003.`seqeval`Kết quả điển hình: ~ 84 F1.
   **中等。**Trong CoNLL-2003 tiếng Anh NER 数据集上训练上述 sklearn-crfsuite CRF──使用 `seqeval`报告每类 F1──典型结果:~84 F1──
3. **Hard.**- Đúng rồi.`distilbert-base-cased`trên một tập dữ liệu NER cụ thể về lĩnh vực (tiếu y tế, pháp lý hoặc tài chính).So sánh với mô hình spaCy nhỏ.
   **困难。**Trong lĩnh vực cụ thể NER số liệu tập hợp (hospital, luật hoặc tài chính)`distilbert-base-cased`✿ với không gian ✿ 小模型比较✿记录数据泄漏检查并写下让你惊的地方✿

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NER（命名实体识别） | Extract names / 提取名字 | Label token spans with types (PERSON, ORG, GPE, DATE, ...). / 用类型（PERSON、ORG、GPE、DATE 等）标注 token 跨度。 |
| BIO | Tagging scheme / 标注方案 | `B-X` begins, `I-X` continues, `O` outside. / `B-X` 开始，`I-X` 继续，`O` 外部。 |
| BILOU | Better BIO / 更好的 BIO | Adds `L-X` (last), `U-X` (unit) for cleaner boundaries. / 添加 `L-X`（最后）、`U-X`（单元）以获得更清晰的边界。 |
| CRF（条件随机场） | Structured classifier / 结构化分类器 | Models transitions between labels, not just emissions. Enforces valid sequences. / 对标签间的转移建模，而不仅仅是发射。强制有效序列。 |
| Nested NER（嵌套 NER） | Overlapping entities / 重叠实体 | One span is a different entity than a sub-span of it. BIO cannot express this. / 一个跨度与其子跨度是不同的实体。BIO 无法表达这一点。 |
| Entity-level F1（实体级 F1） | Proper NER metric / 正确的 NER 指标 | Predicted span must match true span exactly. Token-level F1 overstates accuracy. / 预测跨度必须与真实跨度完全匹配。Token 级 F1 会高估准确率。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.

## Xem thêm 延伸阅读

- [Lample et al. (2016). Neural Architectures for Named Entity Recognition](https://arxiv.org/abs/1603.01360) BiLSTM-CRF giấy. Canonical. / BiLSTM-CRF 论文──经典──
- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805) giới thiệu mô hình phân loại token đã trở thành tiêu chuẩn. / 引入成为标准的 token 分类模式──
- [spaCy linguistic features — named entities](https://spacy.io/usage/linguistic-features#named-entities) tham chiếu thực tế cho mỗi thuộc tính trên `Doc.ents`và `Span`. / `Doc.ents`和 `Span`Trên mỗi thuộc tính có thể dùng để tham khảo.
- [seqeval](https://github.com/chakki-works/seqeval) thư viện métrics đúng. Hãy sử dụng nó luôn luôn. / 正确的指标库──始终使用它──
