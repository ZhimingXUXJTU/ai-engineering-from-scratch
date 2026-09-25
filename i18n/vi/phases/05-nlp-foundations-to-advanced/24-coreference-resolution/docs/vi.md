# - Định nghĩa của sự phân tích.

> "Bà gọi cho anh ta, anh ta không trả lời, bác sĩ đang ăn trưa". Ba lần nhắc đến hai người và không ai được đặt tên.
> "Bà gọi cho anh ta. Anh ta không trả lời. Bác sĩ đang ăn trưa".

> **【中文解读】**将文本中的代词和名词短语链接到它们指代的实体──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Giải quyết Coreference liên kết mọi biểu hiện liên quan đến cùng một thực thể. "Barack Obama", "quốc tịch", "anh ấy", "Obama" tất cả chỉ ra một người. Nếu không có nó, hệ thống NER của bạn báo cáo bốn thực thể thay vì một, các mảnh biểu đồ kiến thức của bạn, và tổng kết của bạn bỏ các chủ đề giữa tài liệu.

> 共指消解将每个指向同一实体表达链接起――"Barack Obama""", tổng thống""", ông""", Obama" đều chỉ đến một người――没有它,你的NER 系统报告四个实体而不是一个,知识图碎,摘要器在文档中间丢弃主语――

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Tại sao nó quan trọng vào năm 2026: LLM xử lý coreference ngầm trong cửa sổ ngữ cảnh của họ, nhưng thu thập RAG vẫn cần giải pháp rõ ràng. Nếu người dùng hỏi "nó nói gì?", người thu hồi cần biết "nó" là ai trước khi nó có thể tìm thấy phần đúng.

> 2026 năm vì sao quan trọng:LLM trong cửa sổ trên dưới văn bản trong quá trình xử lý ẩn ý, nhưng RAG 检索 vẫn cần phải được giải quyết rõ ràng. Nếu người dùng hỏi "quý cô ấy nói gì?", kiểm tra cần biết " cô ấy" là ai trước khi tìm thấy đúng khối.

## Khái niệm cốt lõi

> **【中文解读】**本节介绍核心概念和理论基础──

**Mention detection.**Tìm tất cả các cụm từ và đại từ có thể đề cập đến một thực thể. Sử dụng thẻ POS và phân tích cây.

> **指称检测。**找到所有可能指向实体名词短语和代词──使用 POS 标签和分析树──

**Coreference clustering.**Nhóm đề cập đến các thực thể tương tự. Các phân loại cặp đề cập, mô hình dựa trên thời gian hoặc các cách tiếp cận thần kinh đầu đến cuối (Lee et al., 2017).

> **共指聚类。**sẽ chỉ đến cùng một thực thể, chỉ định phân nhóm.

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua quá trình chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI trong doanh nghiệp hiện tại.

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.
```figure
coref-links
```

## Hãy xây dựng nó

## Hãy xây dựng nó.

> **【中文解读】**Bài viết này thông qua mã từ zero thực hiện các thuật toán cốt lõi.

```python
import spacy

nlp = spacy.load("en_core_web_sm")

def resolve_coref(text):
    doc = nlp(text)
    clusters = {}
    for token in doc:
        if token.pos_ == "PRON":
            # Simple heuristic: look for nearest preceding noun
            for t in reversed(list(doc[:token.i])):
                if t.pos_ in ("NOUN", "PROPN"):
                    clusters[token.text] = t.text
                    break
    return clusters
```

> **【中文解读】**Bài này sẽ cho thấy cách sử dụng một khuôn khổ đã trưởng thành để nhanh chóng áp dụng công nghệ này.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**Bài viết này tập trung vào cách thức triển khai mô hình cho các sản phẩm có thể sử dụng.

- **spaCy with coreferee.**Coreference sản xuất cho tiếng Anh. / spaCy + coreferee。英语生产共指。
- **Hugging Face span-based models.**Nơ-ron phân giải coreference. / Hugging Face dựa trên mô hình跨度.
- **LLM prompting.**Hãy yêu cầu LLM giải quyết các vấn đề chính xác, chi phí cao.

## Chuyển nó đi.

Cứ như `outputs/skill-coref-picker.md`- Có thể là:

> 保存为 `outputs/skill-coref-picker.md`- Có thể là:

```markdown
Given a text and need for entity tracking, pick coreference approach.
1. Rule-based vs neural vs LLM.
2. Language support.
3. Latency budget.
```

## Tập luyện bài tập

1. **Easy.**Thực hiện giải pháp ngụ ngữ bằng cách sử dụng thẻ POS. / **简单。**用 POS 标签实现代词消解──
2. **Medium.**Đánh giá các điểm chung của các đối tượng trên một tập hợp 50 câu. / **中等。**Trong 50 câu nói trên đánh giá các đối tượng chính của không gian.
3. **Hard.**Xây dựng một bộ xử lý trước RAG giải quyết các coreference trước khi phân mảnh. / **困难。**构建在分块前消解共指的RAG 预处理器──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Coreference（共指） | Multiple expressions referring to the same entity. / 多个表达指向同一实体。 |
| Mention（指称） | A textual reference to an entity. / 对实体的文本引用。 |
| Anaphora（回指） | Pronoun referring to an earlier noun. / 代词指向前面的名词。 |

## Xem thêm 延伸阅读

- [Lee et al. (2017). End-to-end Neural Coreference Resolution](https://arxiv.org/abs/1707.07045) phương pháp dựa trên khoảng thời gian. / 基于跨度的方法──
- [coreferee](https://github.com/explosion/coreferee) spaCy coreference plugin. / spaCy 共指插件──
