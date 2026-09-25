# Chiến lược chia nhỏ cho RAG

> Các cấu hình phân chia ảnh hưởng đến chất lượng thu hồi cũng như sự lựa chọn của mô hình nhúng (Vectara NAACL 2025).
> Các phân đoạn phân loại có tác động đến chất lượng kiểm tra như các lựa chọn của mô hình nhúng (VECTRA NAACL 2025)

> **【中文解读】**Trong hệ thống RAG, tài liệu làm thế nào để phân chia thành khối trực tiếp ảnh hưởng đến kết quả kiểm tra.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 22 (Embedding Models), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 22（嵌入模型），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Vấn đề  vấn đề giới thiệu

Giải pháp không phải là "mua một mô hình nhúng tốt hơn". Giải pháp là nhúng đúng. Báo NAACL 2025 của Vectara cho thấy chiến lược nhúng giải thích sự khác biệt về chất lượng truy xuất cũng như lựa chọn nhúng.

> Phương pháp sửa chữa không phải là "mua một mô hình nhúng tốt hơn"──Phương pháp sửa chữa là chính xác phân khối──VECTARA's NAACL 2025 thesis cho thấy phân khối chiến lược giải thích nhiều sự khác biệt về chất lượng tìm kiếm như lựa chọn nhúng──

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng kỹ thuật này trong công trình thực tế.

Các tiêu chuẩn tháng 2 năm 2026 cho thấy kết quả đáng ngạc nhiên: phân tích nhỏ gọn với kích thước cố định với 100 token và 20 token chồng chéo vượt qua hầu hết các chiến lược phân tích "thông minh" trên RAG mục đích chung.

> Kiểm tra chuẩn mực tháng 2 năm 2026 cho thấy kết quả đáng kinh ngạc: đơn giản cố định lớn nhỏ khối lượng lớn ((100 token cộng 20 token 重叠) trong General RAG trên đánh bại hầu hết các chiến lược phân khối " thông minh " .

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

**Fixed-size chunking.**Chia văn bản thành các khối mã thông báo N với sự chồng chéo tùy chọn. đơn giản, nhanh chóng, hiệu quả đáng ngạc nhiên.

> **固定大小分块。**Để phân chia văn bản thành các khối của N token, có thể được chọn chồng lên.

**Sentence-level chunking.**Chia thành các giới hạn câu. Mỗi phần = một hoặc nhiều câu.

> **句子级分块。**Trong câu giới hạn chia sẻ. Mỗi khối = một hoặc nhiều câu.

**Semantic chunking.**Nhúng câu, nhóm các câu liên tiếp với các bản nhúng tương tự thành các mảnh.

> **语义分块。**嵌入句子, sẽ được嵌入 tương tự连续句子分组为块.

**Recursive character chunking.**Chia theo đoạn văn, sau đó theo câu, sau đó theo ký tự.

> **递归字符分块。**按段落分割,然后按句子,然后按字符──LangChain 的默认──好的通用启发式──

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua quá trình chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI trong doanh nghiệp hiện tại.

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.
```figure
n5-chunk-cuts
```

## Hãy xây dựng nó

## Hãy xây dựng nó.

> **【中文解读】**Bài viết này thông qua mã từ zero thực hiện các thuật toán cốt lõi.

### Bước 1: Chuyển nhỏ kích thước cố định với sự chồng chéo

```python
def fixed_chunk(text, chunk_size=100, overlap=20):
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunks.append(" ".join(tokens[i:i + chunk_size]))
    return chunks
```

### Bước 2: Phân tích ngữ nghĩa

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def semantic_chunk(text, model_name="sentence-transformers/all-MiniLM-L6-v2", threshold=0.5):
    model = SentenceTransformer(model_name)
    sentences = text.split(". ")
    embeddings = model.encode(sentences, normalize_embeddings=True)
    chunks = [sentences[0]]
    for i in range(1, len(sentences)):
        sim = np.dot(embeddings[i], embeddings[i-1])
        if sim < threshold:
            chunks.append(sentences[i])
        else:
            chunks[-1] += ". " + sentences[i]
    return chunks
```

> **【中文解读】**Bài này sẽ cho thấy cách sử dụng một khuôn khổ đã trưởng thành để nhanh chóng áp dụng công nghệ này.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**Bài viết này tập trung vào cách thức triển khai mô hình cho các sản phẩm có thể sử dụng.

| Strategy / 策略 | Chunk size / 块大小 | Best for / 最适合 |
|---------|---------|---------|
| Fixed / 固定 | 100-500 tokens | General purpose / 通用 |
| Sentence / 句子 | 1-3 sentences | FAQ, short answers / FAQ、短答案 |
| Semantic / 语义 | Variable / 可变 | Narrative, long docs / 叙述、长文档 |
| Recursive / 递归 | 500-1500 chars | LangChain default / LangChain 默认 |

## Chuyển nó đi.

Cứ như `outputs/skill-chunking-picker.md`- Có thể là:

> 保存为 `outputs/skill-chunking-picker.md`- Có thể là:

```markdown
Given document type and retrieval task, pick chunking strategy and parameters.
1. Chunking method (fixed, sentence, semantic, recursive).
2. Chunk size and overlap.
3. Evaluation metric (retrieval recall@k, answer quality).
```

## Tập luyện bài tập

1. **Easy.**Thực hiện phân mảnh kích thước cố định với sự chồng chéo. đo chất lượng thu hồi. / **简单。**实现固定大小分块──测量检索质量──
2. **Medium.**So sánh các phân tích cố định và ngữ nghĩa trên một bộ dữ liệu kể chuyện. / **中等。**Trong bộ dữ liệu kể về so sánh cố định với các phân đoạn ngôn ngữ.
3. **Hard.**Xây dựng một đường ống chunking tối ưu thích nghi kích thước chunk mỗi loại tài liệu. / **困难。**构建按文档类型自适应块大小的优分块流水线──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Chunking（分块） | Splitting documents into retrievable units. / 将文档分割为可检索单元。 |
| Overlap（重叠） | Shared tokens between adjacent chunks. / 相邻块之间的共享 token。 |
| Semantic chunking（语义分块） | Group sentences by embedding similarity. / 按嵌入相似度分组句子。 |

## Xem thêm 延伸阅读

- [Vectara NAACL 2025 chunking study](https://vectara.com/blog/breaking-the-ice-chunking-strategies-for-rag) điểm chuẩn phân mảnh. / 分块基准。
- [LangChain text splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/) thực hiện phân mảnh. / 分块实现。
