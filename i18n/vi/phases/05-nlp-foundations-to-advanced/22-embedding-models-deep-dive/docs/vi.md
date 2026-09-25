#  Lập vào mô hình  2026 Deep Dive  嵌入模型  深度解析

> Word2Vec cho bạn một vector cho mỗi từ. Các mô hình nhúng hiện đại cho bạn một vector cho mỗi đoạn, xuyên ngôn ngữ, với tầm nhìn hiếm, dày đặc và đa vector, kích thước phù hợp với chỉ mục của bạn. Chọn sai và RAG của bạn lấy lại sai thứ.
> Word2Vec  cho bạn mỗi từ một chiều dài. Moderne Embedded Model cho bạn mỗi đoạn một chiều dài, xuyên ngôn ngữ, có độ hiếm, mật độ và nhiều chiều dài.

> **【中文解读】**嵌入模型 là lõi của RAG 和语义搜索.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word Embeddings), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 03（词嵌入），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Vấn đề  vấn đề giới thiệu

Chọn một embedding vào năm 2026 có nghĩa là chọn qua năm trục: mật độ đối với ít đối với nhiều vector, đơn ngôn ngữ đối với đa ngôn ngữ, kích thước mô hình, mục tiêu đào tạo, và liệu nó phù hợp với các hạn chế kích thước của cơ sở dữ liệu vector của bạn hay không.

> 2026 năm chọn nhúng có nghĩa là chọn trên 5 trục: 密 vs 稀疏 vs 多向量、单语 vs 多语言、模型大小、训练目标、以及是否适合你的向量数据库尺寸约束──

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng kỹ thuật này trong công trình thực tế.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

**Dense embeddings.**Một vector kích thước cố định trên mỗi văn bản (ví dụ: 768-dim từ MiniLM).

> **稠密嵌入。**Mỗi văn bản là một khối lượng lớn cố định như MiniLM của 768 维) ⋅Bí dụ nhanh hơn, nén hơn, khối lượng dữ liệu cơ sở dữ liệu tiêu chuẩn ⋅ phù hợp nhất với các quét chung ⋅

**Sparse embeddings.**Một trọng lượng cho mỗi từ vựng (như một TF-IDF được học). SPLADE, BM25.

> **稀疏嵌入。**Mỗi từ biểu hiện một quyền trọng (如学习的TF-IDF) ――SPLADE、BM25──适合关键词密集的查询──

**Multi-vector / ColBERT.**Một vector mỗi token, điểm tương tác muộn, chỉ số chính xác hơn nhưng lớn hơn.

> **多向量 / ColBERT。**Mỗi token một向量,延迟交互评分......

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua quá trình chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI trong doanh nghiệp hiện tại.

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**Bài viết này thông qua mã từ zero thực hiện các thuật toán cốt lõi.
```figure
gx-matryoshka
```

## Hãy xây dựng nó

### Bước 1: so sánh các mô hình nhúng

```python
from sentence_transformers import SentenceTransformer
import numpy as np

models = {
    "MiniLM": "sentence-transformers/all-MiniLM-L6-v2",
    "multilingual": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
}

query = "What is attention in transformers?"
docs = ["Self-attention computes weighted sums of values.", "The cat sat on the mat."]

for name, model_id in models.items():
    model = SentenceTransformer(model_id)
    q_emb = model.encode([query], normalize_embeddings=True)
    d_embs = model.encode(docs, normalize_embeddings=True)
    sims = (d_embs @ q_emb.T).flatten()
    print(f"{name}: {list(zip(docs, sims.round(3)))}")
```

> **【中文解读】**Bài này sẽ cho thấy cách sử dụng một khuôn khổ đã trưởng thành để nhanh chóng áp dụng công nghệ này.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**Bài viết này tập trung vào cách thức triển khai mô hình cho các sản phẩm có thể sử dụng.

| Model / 模型 | Dim / 维度 | Best for / 最适合 |
|------|------|---------|
| all-MiniLM-L6-v2 | 384 | English, speed / 英语，速度 |
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | Multilingual / 多语言 |
| BGE-large-en-v1.5 | 1024 | English accuracy / 英语准确率 |

## Chuyển nó đi.

Cứ như `outputs/skill-embedding-picker.md`- Có thể là:

> 保存为 `outputs/skill-embedding-picker.md`- Có thể là:

```markdown
Given requirements (language, accuracy, latency, index size), pick the right embedding model.
1. Dense vs sparse vs multi-vector.
2. Model checkpoint.
3. Dimension and index budget.
```

## Tập luyện bài tập

1. **Easy.**So sánh MiniLM vs BGE trên một nhiệm vụ tìm kiếm 100 câu hỏi. / **简单。**Trong 100 nhiệm vụ kiểm tra kiểm tra trên so sánh MiniLM vs BGE.
2. **Medium.**Xây dựng bộ thu hồi mật độ hybrid + spars. / **中等。**构建混合密+稀疏检索──
3. **Hard.**Định chỉnh một mô hình nhúng trên các cặp cụ thể về miền. / **困难。**Trong lĩnh vực cụ thể đối với các mô hình nhỏ được đặt trong.

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dense embedding（稠密嵌入） | Fixed-size vector per text. / 固定大小向量。 |
| Sparse embedding（稀疏嵌入） | One weight per vocab term. / 每个词表项一个权重。 |
| ColBERT / multi-vector | One vector per token, late interaction. / 每个 token 一个向量。 |
| Hybrid search（混合搜索） | Combine dense + sparse retrieval scores. / 结合稠密+稀疏检索。 |

## Xem thêm 延伸阅读

- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) nhúng các tiêu chuẩn. / 嵌入模型基准──
- [SPLADE](https://arxiv.org/abs/2109.10086)  rạn rạn học được nhúng. / 稀疏学习嵌入。
- [ColBERT](https://arxiv.org/abs/2004.12832) late interaction retrieval. / 延迟交互检索。
