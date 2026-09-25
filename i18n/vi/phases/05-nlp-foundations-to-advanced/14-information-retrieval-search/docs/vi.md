# Tìm kiếm thông tin và tìm kiếm thông tin

> BM25 chính xác nhưng hỏng. Thiết bị dày đặc ném một mạng lưới rộng nhưng bỏ lỡ từ khóa. Hybrid là mặc định 2026. Mọi thứ khác đều được điều chỉnh.
> BM25 精确但脆弱──密检索撒大网但漏掉关键词──混合检索 là lựa chọn mặc định năm 2026──其余都是调参──

> **【中文解读】**Từ từ khóa phù hợp đến kiểm tra khối lượng.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## Vấn đề  vấn đề giới thiệu

Người dùng gõ "điều xảy ra nếu ai đó nói dối để kiếm tiền" và hy vọng sẽ tìm ra quy định thực sự bao gồm điều đó: "Gụ 420 IPC". Một tìm kiếm từ khóa bỏ qua hoàn toàn (không có từ vựng được chia sẻ).
> Người dùng nhập "what happens if someone lies to get money"并期望找到实际覆盖该内容的法规:"Chap 420 IPC"──关键词搜索完全找不到它(没有共享词汇)── Nếu嵌入没有在法律文本上训练过,语义搜索也会错过它──真正搜索必须同时处理两者──

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.


IR là đường ống dưới mỗi hệ thống RAG, mỗi thanh tìm kiếm, tìm kiếm mờ của mỗi trang web tài liệu. Kiến trúc 2026 hoạt động trong sản xuất không phải là một phương pháp duy nhất.
> IR là mỗi hệ thống RAG, mỗi tìm kiếm, mỗi điểm lưu trữ tìm kiếm dòng chảy dưới đây.

Bài học này xây dựng từng mảnh và tên mà thất bại mỗi bắt.
> Bài học này xây dựng mỗi phần và chỉ ra những thất bại mà mỗi phần đã nắm bắt.

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


## Khái niệm cốt lõi

![Hybrid retrieval: BM25 + dense + RRF + cross-encoder rerank](../assets/retrieval.svg)
> ![混合检索：BM25 + 稠密 + RRF + 交叉编码器重排序](../assets/retrieval.svg)

Bốn lớp, chọn những lớp mà anh cần.
> Bốn tầng. Chọn những gì bạn cần.

1. **Sparse retrieval (BM25).**Nhanh chóng, chính xác trong sự phù hợp chính xác, khủng khiếp trong ngữ nghĩa chạy qua một chỉ số đảo ngược Sub-10ms mỗi truy vấn trên hàng triệu tài liệu có bạn tham chiếu quy định, mã sản phẩm, thông điệp lỗi, tên thực thể đúng.
2. **Dense retrieval.**Mã hóa truy vấn và tài liệu thành vector. Tìm kiếm hàng xóm gần nhất. Chụp các cụm từ và sự tương đồng ngữ nghĩa. Chưa có sự phù hợp chính xác từ khóa khác nhau bằng một ký tự. 50-200ms cho mỗi truy vấn với FAISS hoặc một vector DB.
3. **Fusion.**Thủy lại danh sách xếp hạng từ hiếm và dày đặc. Phối hợp xếp hạng tương đối (RRF) là mặc định dễ dàng vì nó bỏ qua điểm số thô (có sống trong các cân bằng khác nhau) và chỉ sử dụng các vị trí xếp hạng. Phối hợp trọng lượng là một lựa chọn khi bạn biết một tín hiệu thống trị cho miền của bạn.
4. **Cross-encoder rerank.**Hãy lấy top-30 từ fusion. chạy một cross-encoder (query + document cùng nhau, ghi điểm mỗi cặp). Giữ top-5. Cross-encoder chậm hơn mỗi cặp so với bi-encoder nhưng chính xác hơn nhiều. Bạn giảm giá bằng cách chỉ chạy chúng trên top-30.
> 1. **稀疏检索（BM25）。**快速、精确匹配准确、语义上糟糕──在倒排索引上运行──百万档次上每查询亚 10毫秒──正确处理法规引用、产品代码、错误消息、命名实体──
2. **稠密检索。**Để tìm kiếm và biên tập mã hóa cho khối lượng. gần đây tìm kiếm.
3. **融合。**合并稀疏和密的排列列表──倒数排名融合(Reciprocal Rank Fusion, RRF) là một lựa chọn mặc định đơn giản, bởi vì nó bỏ qua số lượng nguyên thủy (có ở các quy mô khác nhau) chỉ sử dụng vị trí xếp hạng── khi bạn biết một tín hiệu nào đó chiếm ưu thế trong lĩnh vực của bạn, gia tăng quyền lực kết hợp là một lựa chọn──
4. **交叉编码器重排序。**Từ hội nhập lấy top-30──运行交叉编码器(查询 + 文档一起,对每对打分)──保留 top-5──交叉编码器对双编码器慢但准确得多──你只在 top-30 上运行来摊销成本──

Việc lấy lại ba chiều (BM25 + dày + học-sparse như SPLADE) vượt qua hai chiều trong các chỉ số chuẩn năm 2026 nhưng cần cơ sở hạ tầng cho các chỉ số học-sparse. Đối với hầu hết các đội, xếp hạng lại hai chiều cộng với mã hóa chéo là điểm tốt nhất.
> 三路检索 (BM25 + 密 + 学习稀疏如 SPLADE) trong năm 2026基准上优于两路, nhưng cần phải học cơ sở hạ tầng của chỉ số稀疏. Đối với hầu hết các nhóm, hai đường cộng lại là điểm cân bằng tốt nhất.

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.


## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
gx-hybrid-retrieval
```

## Hãy xây dựng nó

### Bước 1: BM25 từ đầu
> Hai yếu tố đáng hiểu.`k1=1.5`控制词频和;更高 nghĩa là từ重复的权重更大──`b=0.75`Control length 归纳化;0 忽略文档长度,1 完全归纳化──默认值是罗伯逊 原始论文中的推值,很少需要调整──

```python
import math
import re
from collections import Counter

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text):
    return TOKEN_RE.findall(text.lower())


class BM25:
    def __init__(self, corpus, k1=1.5, b=0.75):
        if not corpus:
            raise ValueError("corpus must not be empty")
        self.corpus = [tokenize(d) for d in corpus]
        self.k1 = k1
        self.b = b
        self.n_docs = len(self.corpus)
        self.avg_dl = sum(len(d) for d in self.corpus) / self.n_docs
        self.df = Counter()
        for doc in self.corpus:
            for term in set(doc):
                self.df[term] += 1

    def idf(self, term):
        n = self.df.get(term, 0)
        return math.log(1 + (self.n_docs - n + 0.5) / (n + 0.5))

    def score(self, query, doc_idx):
        q_tokens = tokenize(query)
        doc = self.corpus[doc_idx]
        dl = len(doc)
        freq = Counter(doc)
        score = 0.0
        for term in q_tokens:
            f = freq.get(term, 0)
            if f == 0:
                continue
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * dl / self.avg_dl)
            score += self.idf(term) * numerator / denominator
        return score

    def rank(self, query, top_k=10):
        scored = [(self.score(query, i), i) for i in range(self.n_docs)]
        scored.sort(reverse=True)
        return scored[:top_k]
```

Hai tham số đáng biết.`k1=1.5`điều khiển độ bão hòa tần số thuật ngữ; cao hơn có nghĩa là trọng lượng nhiều hơn khi lặp lại thuật ngữ. `b=0.75`Điều khiển bình thường hóa chiều dài; 0 bỏ qua chiều dài tài liệu, 1 bình thường hóa hoàn toàn.
> L2 归一化嵌入使点积等于余弦──`all-MiniLM-L6-v2`là 384 维,快速, đối với hầu hết các English检索足够强.`paraphrase-multilingual-MiniLM-L12-v2`❖ tỷ lệ sử dụng cao nhất`bge-large-en-v1.5`Hoặc`e5-large-v2`

### Bước 2: lấy lại dày đặc với một bộ mã hóa đôi
> `k=60`常数 từ nguyên thủy RRF 论文──更高的 `k`Để tạo ra sự khác biệt trong xếp hạng đóng góp biến đổi bằng; thấp hơn `k`使頂部排名主导──60 là giá trị mặc định đã được phát hành, rất ít cần điều chỉnh──

```python
from sentence_transformers import SentenceTransformer
import numpy as np


def build_dense_index(corpus, model_id="sentence-transformers/all-MiniLM-L6-v2"):
    encoder = SentenceTransformer(model_id)
    embeddings = encoder.encode(corpus, normalize_embeddings=True)
    return encoder, embeddings


def dense_search(encoder, embeddings, query, top_k=10):
    q_emb = encoder.encode([query], normalize_embeddings=True)
    sims = (embeddings @ q_emb.T).flatten()
    order = np.argsort(-sims)[:top_k]
    return [(float(sims[i]), int(i)) for i in order]
```

L2- bình thường hóa các nhúng nhúng vì vậy điểm sản phẩm bằng cosine. `all-MiniLM-L6-v2`là 384 chiều, nhanh, và đủ mạnh để lấy lại tiếng Anh.`paraphrase-multilingual-MiniLM-L12-v2`Để có độ chính xác cao nhất,`bge-large-en-v1.5`hoặc `e5-large-v2`- Tôi không biết.
> 三阶段组合──BM25 找到词汇匹配──密找到语义匹配──RRF 合并两个排名不需要分数校准──交叉编码器使用查询文档对重新对 top-30 打分,捕获双编码器遗漏的细粒度相关性──保留 top-5──

### Bước 3: Sự hợp nhất cấp bậc
>                                                                                                                                                                                                                                                               
|------|------|
| Recall@k | 存在正确文档的查询中，正确文档在 top-k 中的比例 |
| MRR（平均倒数排名） | 第一个相关文档的 1/rank 的平均值 |
| nDCG@k | 考虑相关性分级，而非仅仅是二元的 相关/不相关 |

```python
def reciprocal_rank_fusion(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, (_, doc_idx) in enumerate(ranking):
            scores[doc_idx] = scores.get(doc_idx, 0.0) + 1.0 / (k + rank + 1)
    fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(score, doc_idx) for doc_idx, score in fused]
```

- `k=60`liên tục đến từ giấy RRF gốc.`k`làm phẳng hơn sự đóng góp của sự khác biệt cấp bậc; thấp hơn `k`60 là tiêu chuẩn mặc định được xuất bản và hiếm khi cần điều chỉnh.
> Đặc biệt đối với RAG, kiểm tra **Recall@k**Đó là con số quan trọng nhất. Nếu đoạn văn chính xác không được tìm kiếm, người đọc không thể trả lời.

### Bước 4: Tìm kiếm lai + xếp hạng lại
> 调试技巧: đối với các truy vấn thất bại, đối với hiếm疏和密排名── nếu một tìm thấy tài liệu chính xác và một khác không có, bạn có từ ngữ không phù hợp (修复:添加缺失的一半) hoặc语义歧义 (修复:更好的嵌入或重排序器)

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def hybrid_search(query, bm25, encoder, dense_embeddings, corpus, top_k=5, pool_size=30, reranker=reranker):
    sparse_ranking = bm25.rank(query, top_k=pool_size)
    dense_ranking = dense_search(encoder, dense_embeddings, query, top_k=pool_size)
    fused = reciprocal_rank_fusion([sparse_ranking, dense_ranking])[:pool_size]

    pairs = [(query, corpus[doc_idx]) for _, doc_idx in fused]
    scores = reranker.predict(pairs)
    reranked = sorted(zip(scores, [doc_idx for _, doc_idx in fused]), reverse=True)
    return reranked[:top_k]
```

BM25 tìm thấy sự phù hợp từ điển. Thiết bị mật độ tìm thấy sự phù hợp ngữ nghĩa. RRF hợp nhất hai thứ hạng mà không cần phải chuẩn lập điểm số. Cross-encoder ghi lại top-30 bằng cách sử dụng cặp truy vấn-tài liệu cùng nhau, thu thập sự liên quan tinh tế của các bi-encoder bị bỏ lỡ. Giữ top-5.

### Bước 5: đánh giá

| Metric | Meaning |
|--------|---------|
| Recall@k | Of queries where the correct document exists, how often is it in the top-k? |
| MRR (Mean Reciprocal Rank) | Average of 1/rank of first relevant document. |
| nDCG@k | Accounts for relevance gradations, not just binary relevant/not. |

Đặc biệt là cho RAG,**Recall@k**của bộ truy cập là số quan trọng nhất. Người đọc của bạn không thể trả lời nếu đoạn văn đúng không trong bộ truy cập.

Mẹo gỡ lỗi: cho các truy vấn thất bại, phân biệt các thứ hạng hiếm và dày đặc. Nếu một tìm thấy tài liệu đúng và người khác không tìm thấy, bạn có một sự không phù hợp từ vựng (sửa: thêm nửa thiếu) hoặc sự mơ hồ ngữ nghĩa (sửa: nhúng tốt hơn hoặc một trình xếp hạng lại).


> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


Số 2026:
> 2026 年技术:

| Scale | Stack |
|-------|-------|
| 1k-100k docs | In-memory BM25 + `all-MiniLM-L6-v2` embeddings + RRF. No separate DB. |
| 100k-10M docs | FAISS or pgvector for dense + Elasticsearch / OpenSearch for BM25. Run in parallel. |
| 10M+ docs | Qdrant / Weaviate / Vespa / Milvus with hybrid support. Cross-encoder rerank on top-30. |
| Best-quality frontier | Three-way (BM25 + dense + SPLADE) + ColBERT late-interaction reranking |
> Ưu điểm, kỹ thuật
|------|--------|
| 1k-100k 文档 | 内存中 BM25 + `all-MiniLM-L6-v2` 嵌入 + RRF。无需独立数据库。 |
| 100k-10M 文档 | FAISS 或 pgvector 做稠密 + Elasticsearch / OpenSearch 做 BM25。并行运行。 |
| 10M+ 文档 | Qdrant / Weaviate / Vespa / Milvus 配混合支持。交叉编码器重排序 top-30。 |
| 最高质量前沿 | 三路（BM25 + 稠密 + SPLADE）+ ColBERT 后期交互重排序 |

Bất cứ điều gì bạn chọn, ngân sách để đánh giá. Nhận lại điểm chuẩn trước khi đánh giá chính xác RAG đầu đến cuối. Một người đọc không thể sửa chữa những gì người tìm lại đã bỏ lỡ.
> Bất kể bạn chọn gì, bạn phải đánh giá ngân sách.

### Những bài học khó khăn từ sản xuất RAG năm 2026
> - **80% 的 RAG 失败追溯到摄取和分块，而不是模型。**团队 mất vài tuần trao đổi LLM và điều chỉnh tốt hơn, và kiểm tra mỗi ba lần truy vấn về bình tĩnh trả lại sai lầm trên dưới đây.
- **分块策略比分块大小更重要。**固定大小分割会破坏表格、代码和嵌套标题──句感知是默认选择;语义或基于LLM的分块在技术文档和产品手册有回报──
- **父文档模式。**检索小的"子"块以获得精度――当同一节的多子块出现时,换进父块以保留下文――这持续提升答案质量而无需重新训练――
- **k_rerank=3 通常最优。**Mỗi lần tăng một khối vượt quá số này sẽ tăng token thành phần và sản xuất chậm không nâng cao chất lượng trả lời. Nếu k=8 vẫn còn so với k=3, thì biểu hiện của bộ sưu tập lại là kém.
- **HyDE / 查询扩展。**Từ câu hỏi tạo ra giả thuyết trả lời, nhúng vào nó, kiểm tra.
- **上下文预算控制在 8K token 以下。**Trong một cuộc sống tiếp tục dưới sự hạn chế này có nghĩa là sắp xếp lại.
- **版本化一切。**提示、分块规则、嵌入模型、重排序器──任何漂移都会静默破坏答案质量──忠诚度、上下文精确率和未回答问题率
- **三路检索（BM25 + 稠密 + 学习稀疏如 SPLADE）在 2026 年基准上优于两路**, đặc biệt là các quý vị được sử dụng trong các dịch vụ liên lạc.

- **80% of RAG failures trace to ingestion and chunking, not the model.**Các nhóm dành hàng tuần để trao đổi LLM và điều chỉnh các yêu cầu trong khi việc tìm lại lặng lặng trả lại bối cảnh sai lầm mỗi truy vấn thứ ba.
- **Chunking strategy matters more than chunk size.**Các phân chia kích thước cố định phá vỡ các bảng, mã và tiêu đề tổ hợp. Tiếng nói nhận thức là mặc định; phân tích dựa trên ngữ nghĩa hoặc LLM trả tiền cho các tài liệu kỹ thuật và hướng dẫn sản phẩm.
- **Parent-doc pattern.**Nhận lại các mảnh nhỏ "child" để chính xác. Khi nhiều trẻ em từ cùng một phần cha mẹ xuất hiện, hãy thay đổi trong khối cha mẹ để giữ được ngữ cảnh. Điều này liên tục nâng cao chất lượng trả lời mà không cần đào tạo lại.
- **k_rerank=3 is usually optimal.**Mỗi phần thêm vào trong quá khứ mà thêm chi phí token và thời gian trễ tạo mà không nâng cao chất lượng trả lời. Nếu k=8 vẫn tốt hơn k=3 cho bạn, reanker đang hoạt động kém.
- **HyDE / query expansion.**Tạo ra một câu trả lời giả thuyết từ câu hỏi, nhúng vào đó, lấy lại. Cắt cầu khoảng cách cụm từ giữa câu hỏi ngắn và tài liệu dài.
- **Context budget under 8K tokens.**Những cú đánh liên tục ở giới hạn đó có nghĩa là ngưỡng tái xếp hạng quá lỏng lẻo.
- **Version everything.**Các yêu cầu, quy tắc chia nhỏ, mô hình nhúng, xếp hạng lại. Bất kỳ sự lở hở nào lặng lẽ phá vỡ chất lượng câu trả lời. Cổng CI về độ trung thành, độ chính xác ngữ cảnh và tỷ lệ câu hỏi không trả lời chặn sự lùi lại trước khi người dùng nhìn thấy chúng.
- **Three-way retrieval (BM25 + dense + learned-sparse like SPLADE) outperforms two-way**trên các tiêu chuẩn 2026 đặc biệt là cho các truy vấn trộn các từ chính xác với ngữ nghĩa.
> Theo các phép đo ngành công nghiệp năm 2026, thiết kế kiểm tra chính xác giảm 70-90% trong các hình ảnh.

Thiết kế thu hồi đúng cách làm giảm ảo giác 70-90% theo các phép đo ngành công nghiệp năm 2026. Hầu hết các lợi ích hiệu suất RAG đến từ việc thu hồi tốt hơn, chứ không phải điều chỉnh mô hình.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-retrieval-picker.md`- Có thể là:
> 保存为 `outputs/skill-retrieval-picker.md`- Có thể là:

```markdown
---
name: retrieval-picker
description: Pick a retrieval stack for a given corpus and query pattern.
version: 1.0.0
phase: 5
lesson: 14
tags: [nlp, retrieval, rag, search]
---

Given requirements (corpus size, query pattern, latency budget, quality bar, infra constraints), output:

1. Stack. BM25 only, dense only, hybrid (BM25 + dense + RRF), hybrid + cross-encoder rerank, or three-way (BM25 + dense + learned-sparse).
2. Dense encoder. Name the specific model. Match to language(s), domain, and context length.
3. Reranker. Name the specific cross-encoder model if used. Flag that rerank adds 30-100ms latency on top-30.
4. Evaluation plan. Recall@10 is the primary retriever metric. MRR for multi-answer. Baseline first, incremental improvements measured against it.

Refuse to recommend dense-only for corpora with named entities, error codes, or product SKUs unless the user has evidence dense handles exact matches. Refuse to skip reranking for high-stakes retrieval (legal, medical) where the final top-5 decides the user's answer.
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;


## Tập luyện bài tập

1. **Easy.**Thực hiện`hybrid_search`trên một tập hợp 500 tài liệu. kiểm tra 20 câu hỏi. So sánh nhớ ở 5 giữa chỉ BM25, chỉ mật, và lai.
2. **Medium.**Thêm tính toán MRR. Đối với mỗi truy vấn thử nghiệm với tài liệu chính xác được biết, tìm xếp hạng tài liệu chính xác trong xếp hạng BM25, mật và lai.
3. **Hard.**Định chỉnh một bộ mã hóa dày đặc trên miền của bạn bằng cách sử dụng MultipleNegativesRankingLoss (Sentence Transformers). Xây dựng một bộ đào tạo từ 500 cặp truy vấn-tài liệu. So sánh pre- và post-fine-tune recall.
> 1. **简单。**Trong 500  tài liệu ngữ pháp thực hiện trên `hybrid_search`△测试 20 个查询──比较 BM25- chỉ、 mật độ- chỉ 和混合的回忆@5──
2. **中等。**添加 MRR 计算── Đối với mỗi truy vấn kiểm tra có tài liệu chính xác được biết, tìm thấy tài liệu chính xác trong vị trí trong xếp hạng BM25、密和混合── báo cáo MRR riêng của mình──
3. **困难。**Sử dụng MultipleNegativesRankingLoss (Sentence Transformers) trong lĩnh vực của bạn từ 500 câu hỏi- tài liệu về tập hợp đào tạo xây dựng.

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BM25 | Keyword search | Okapi BM25. Scores documents by term frequency, IDF, and length. |
| Dense retrieval | Vector search | Encode query + doc into vectors, find nearest neighbors. |
| Bi-encoder | Embedding model | Encodes query and doc independently. Fast at query time. |
| Cross-encoder | Reranker model | Encodes query + doc together. Slow but accurate. |
| RRF | Rank fusion | Combine two rankings by summing `1/(k + rank)`. |
| Recall@k | Retrieval metric | Fraction of queries where a relevant doc is in the top-k. |
>  Từ ngữ  Mọi người thường nói 
|------|-----------|---------|
| BM25 | 关键词搜索 | Okapi BM25。按词频、IDF 和长度为文档打分。 |
| 稠密检索 | 向量搜索 | 将查询 + 文档编码为向量，找最近邻。 |
| 双编码器 | 嵌入模型 | 独立编码查询和文档。查询时快速。 |
| 交叉编码器 | 重排序模型 | 一起编码查询 + 文档。慢但准确。 |
| RRF | 排名融合 | 通过对 `1/(k + rank)` 求和合并两个排名。 |
| Recall@k | 检索指标 | 相关文档在 top-k 中的查询比例。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) điều trị BM25 cuối cùng.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, bộ mã hóa hai chữ theo luật.
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720) máy thu hồi nhỏ gọn học tập đóng lại khoảng cách bằng dense.
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) Bảng giấy RRF.
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) Khôi phục tương tác muộn.
> - [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) 权威的BM25 处理──
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, 经典双编码器──
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720)  缩小与密差的学习稀疏检查器──
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) RRF 论文。
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) 后期交互检索──
