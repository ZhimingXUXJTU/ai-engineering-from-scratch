# Chủ đề Mô hình hóa  LDA và BERTopic 

> LDA: tài liệu là hỗn hợp các chủ đề, các chủ đề là phân phối trên các từ. BERTopic: các tập hợp tài liệu trong không gian nhúng, các tập hợp là các chủ đề. Mục tiêu tương tự, phân hủy khác nhau.
> LDA:文档是主题的混合,主题是词的分布.

> **【中文解读】**LDA sử dụng mô hình xác suất tìm thấy chủ đề,BERTopic sử dụng BERT 嵌入──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec)
**Time:** ~45 minutes | **时间:** ~45 分钟


## Vấn đề  vấn đề giới thiệu

Bạn có 10.000 vé hỗ trợ khách hàng, 50.000 bài báo tin tức, hoặc 200.000 tweet. Bạn cần biết bộ sưu tập là gì mà không cần đọc nó. Bạn không có nhãn danh mục. Bạn thậm chí không biết có bao nhiêu danh mục tồn tại.
> Bạn có 10.000 张客户支持工单,50.000 篇新闻文章或200.000 条推文── bạn cần hiểu chủ đề của bộ sưu tập này trong khi không đọc── bạn không có danh mục phân loại── bạn thậm chí không biết có bao nhiêu danh mục tồn tại──

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.


Mô hình hóa chủ đề trả lời mà không cần giám sát. Hãy đưa cho nó một tập hợp, lấy lại một bộ nhỏ các chủ đề liên kết và, cho mỗi tài liệu, phân phối trên các chủ đề đó.
> Chủ đề xây dựng trong trường hợp không giám sát trả lời câu hỏi này.

LDA (2003) xử lý mỗi tài liệu như là một hỗn hợp các chủ đề ẩn và mỗi chủ đề như là một phân phối trên các từ.
> 两个算法族占主导地位――LDA(2003) sẽ xem mỗi tài liệu là sự pha trộn của chủ đề tiềm ẩn, mỗi chủ đề là sự phân bố của từ ngữ―― 推断是贝叶斯的――它 vẫn còn trong sản xuất phân bố và phân bố các chủ đề có thể giải thích của các thành viên pha trộn.

BERTopic (2020) mã hóa tài liệu bằng BERT, giảm chiều kích với UMAP, tập hợp với HDBSCAN, và trích xuất từ chủ đề thông qua lớp dựa trên TF-IDF. Nó thắng trên văn bản ngắn, phương tiện truyền thông xã hội và bất cứ thứ gì mà sự tương đồng ngữ nghĩa quan trọng hơn sự chồng chéo từ. Một tài liệu nhận được một chủ đề, đó là một giới hạn cho nội dung dạng dài.
> BERTopic(2020) sử dụng BERT 编码文档, sử dụng UMAP 降维, sử dụng HDBSCAN 聚类, thông qua dựa trên các loại TF-IDF 提取主题词── nó được sử dụng trong các văn bản ngắn, truyền thông xã hội và ngữ义相似性比词重叠比较重要内容.

Bài học này xây dựng trực giác cho cả hai và tên cho một người để chọn cho một tập hợp nhất định.
> Bài học này cho cả hai xây dựng trực giác và chỉ ra cho định liệu pháp cần chọn.

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


## Khái niệm cốt lõi

![LDA mixture model vs BERTopic clustering](../assets/topic-modeling.svg)
> ![LDA 混合模型 vs BERTopic 聚类](../assets/topic-modeling.svg)

**LDA generative story.**Mỗi chủ đề là một phân phối trên các từ. Mỗi tài liệu là một hỗn hợp của các chủ đề. Để tạo ra một từ trong một tài liệu, lấy mẫu một chủ đề từ hỗn hợp tài liệu, sau đó lấy mẫu một từ từ phân phối của chủ đề đó. Thuyết dẫn ngược điều này: cho các từ được quan sát, suy luận phân phối chủ đề trên mỗi tài liệu và phân phối từ trên mỗi chủ đề.
> **LDA 生成故事。**Mỗi chủ đề là phân bố của từ. Mỗi tài liệu là sự pha trộn của chủ đề. Phải tạo ra một từ trong tài liệu, lấy một chủ đề từ sự pha trộn của tài liệu, sau đó lấy một từ trong phân bố của chủ đề đó.

Khả năng phát LDA chính:
> 关键 LDA 输出:

- `doc_topic`: matrix `(n_docs, n_topics)`, mỗi hàng tổng cộng đến 1 (phối hợp chủ đề của tài liệu).
- `topic_word`: matrix `(n_topics, vocab_size)`, mỗi hàng tổng cộng đến 1 (khác định từ của chủ đề).
> - `doc_topic`:矩阵 `(n_docs, n_topics)`, mỗi行总和为 1(文档主题混合)
- `topic_word`:矩阵 `(n_topics, vocab_size)`, mỗi行总和为 1 ((主题的词分布)

**BERTopic pipeline.**
> **BERTopic 流水线。**

1. Mã hóa mỗi tài liệu bằng một bộ biến đổi câu (ví dụ: `all-MiniLM-L6-v2`). 384 chiều vector.
2. Giảm kích thước với UMAP xuống còn ~ 5 kích thước.
3. Cluster với HDBSCAN. dựa trên mật độ, tạo ra các cluster kích thước thay đổi và một nhãn "outlier".
4. Đối với mỗi cluster, tính toán TF-IDF dựa trên lớp trên các tài liệu của cluster để trích xuất các từ hàng đầu.
> 1. 用句子 Transformer`all-MiniLM-L6-v2`(编码每篇文档──384 维向量──)
2. Sử dụng UMAP 降维到大约5维度.
3. Sử dụng HDBSCAN 聚类. dựa trên mật độ, tạo ra biến đổi 聚类和离群值标签.
4. Đối với mỗi nhóm, các tài liệu về nhóm được tính toán dựa trên các loại TF-IDF để lấy từ cấp cao nhất.

Output là một chủ đề cho mỗi tài liệu (cộng với một nhãn ngoại lệ -1).
> 输出是每篇文档一个主题 (加上 -1 离群值标签) ⋅可选地,通过 HDBSCAN的概率向量获得软成员资格──

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.


## Hãy xây dựng nó.
```figure
topic-drift
```

## Hãy xây dựng nó

### Bước 1: LDA thông qua scikit-learn
> Lưu ý:移除停用词,min_df 和 max_df 过罕见和无处不在的词, sử dụng CountVectorizer(không phải TfidfVectorizer), vì LDA 期望原始计数。

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


def fit_lda(documents, n_topics=5, max_features=1000):
    cv = CountVectorizer(
        max_features=max_features,
        stop_words="english",
        min_df=2,
        max_df=0.9,
    )
    X = cv.fit_transform(documents)
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=50,
        learning_method="online",
    )
    doc_topic = lda.fit_transform(X)
    feature_names = cv.get_feature_names_out()
    return lda, cv, doc_topic, feature_names


def print_top_words(lda, feature_names, n_top=10):
    for idx, topic in enumerate(lda.components_):
        top_idx = np.argsort(-topic)[:n_top]
        words = [feature_names[i] for i in top_idx]
        print(f"topic {idx}: {' '.join(words)}")
```

Lưu ý: từ dừng được xóa, min_df và max_df lọc các thuật ngữ hiếm và phổ biến, CountVectorizer (không phải TfidfVectorizer) vì LDA mong đợi số liệu thô.
> `Topic != -1` bỏ rơi                                                                                                                                                                                                                                                             `min_topic_size`控制 HDBSCAN's minimum聚类大小;BERTopic 库默认为10──本例为课程的规模显然设为15──对于超过10,000 文档语料,增加到50或100──

### Bước 2: BERTopic (sản xuất)
> 两种方法都输出主题词――问题是这些词是否连贯――

```python
from bertopic import BERTopic

topic_model = BERTopic(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    min_topic_size=15,
    verbose=True,
)

topics, probs = topic_model.fit_transform(documents)
info = topic_model.get_topic_info()
print(info.head(20))
valid_topics = info[info["Topic"] != -1]["Topic"].tolist()
for topic_id in valid_topics[:5]:
    print(f"topic {topic_id}: {topic_model.get_topic(topic_id)[:10]}")
```

Bộ lọc bật `Topic != -1`bỏ các loại tài liệu khác của BERTopic (HQBSCAN không thể tập hợp). `min_topic_size`kiểm soát kích thước cluster tối thiểu của HDBSCAN; thư viện mặc định của BERTopic là 10. ví dụ này đặt nó lên 15 rõ ràng cho quy mô bài học. Đối với các tài liệu trên 10.000, tăng lên 50 hoặc 100.
> - **主题连贯度（c_v）。**结合滑动窗口上下文中顶级词对的 NPMI(归一化点逐点互信息), sẽ phân số tập hợp thành các khối lượng chủ đề, thông qua các khối lượng tương tự của các khối lượng này。越高越好。使用 `gensim.models.CoherenceModel`配 `coherence="c_v"`
- **主题多样性。**所有主题顶级词中唯一词的比例──越高越好──主题不重叠 (→)
- **定性检查。**阅读每个主题的顶级词――它们是否命名为一个真实的东西?

### Bước 3: đánh giá

Cả hai phương pháp đều tạo ra các từ chủ đề.

- **Topic coherence (c_v).**Kết hợp NPMI ( thông tin tương tác theo hướng điểm chuẩn hóa) của cặp từ hàng đầu trên các bối cảnh cửa sổ trượt, tổng hợp điểm số thành vector chủ đề, và so sánh các vector đó thông qua sự tương đồng cosine. cao hơn là tốt hơn. Sử dụng `gensim.models.CoherenceModel`với `coherence="c_v"`- Tôi không biết.
- **Topic diversity.**Phụ phần các từ độc đáo trên tất cả các từ hàng đầu của các chủ đề.
- **Qualitative inspection.**Hãy đọc những từ đầu của mỗi chủ đề.


> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Khi nào để chọn

| Situation | Pick |
|-----------|------|
| Short text (tweets, reviews, headlines) | BERTopic |
| Long documents with topic mixtures | LDA |
| No GPU / limited compute | LDA or NMF |
| Need document-level multi-topic distributions | LDA |
| LLM integration for topic labeling | BERTopic (direct support) |
| Resource-constrained edge deployment | LDA |
| Max semantic coherence | BERTopic |

Các tính toán thực tế lớn nhất là chiều dài tài liệu. BERT nhúng cắt giảm; LDA đếm làm việc trên bất kỳ chiều dài nào. Đối với các tài liệu dài hơn bối cảnh của mô hình nhúng, hoặc chunk + tổng hợp hoặc sử dụng LDA.

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


## Hãy sử dụng nó để thực hiện

Số 2026:
> 2026 年技术:

- **BERTopic.**Tiểu định cho văn bản ngắn và bất cứ thứ gì mà ngữ nghĩa quan trọng.
- **`gensim.models.LdaModel`.**LDA cổ điển cho sản xuất, trưởng thành, được thử nghiệm trong trận chiến.
- **`sklearn.decomposition.LatentDirichletAllocation`.**LDA dễ dàng cho thí nghiệm.
- **NMF.**Không tính toán tử liệu âm tính. thay thế nhanh cho LDA, chất lượng tương đương trên văn bản ngắn.
- **Top2Vec.**Thiết kế tương tự như BERTopic. Cộng đồng nhỏ hơn nhưng tốt về một số điểm chuẩn.
- **FASTopic.**Tới hơn, nhanh hơn BERTopic trên các cơ quan rất lớn.
- **LLM-based labeling.**Thực hiện bất kỳ cluster nào, sau đó yêu cầu một mô hình để đặt tên cho mỗi cluster.
> - **BERTopic。**短文本和语义 quan trọng trường hợp 默认选择──
- **`gensim.models.LdaModel`。**生产级经典 LDA, trưởng thành, kinh nghiệm lâu dài.
- **`sklearn.decomposition.LatentDirichletAllocation`。**实验用简单 LDA──
- **NMF。**Không tích cực phân tích矩阵――LDA của nhanh thay thế,短文上质量相当――
- **Top2Vec。**类似BERTopic的设计──社区较小但在某些基准上表现良好──
- **FASTopic。**更新,在超大语料上比BERTopic 快──
- **基于 LLM 的标注。**运行任何聚类,然后提示模型命名每个聚类――

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-topic-picker.md`- Có thể là:
> 保存为 `outputs/skill-topic-picker.md`- Có thể là:

```markdown
---
name: topic-picker
description: Pick LDA or BERTopic for a corpus. Specify library, knobs, evaluation.
version: 1.0.0
phase: 5
lesson: 15
tags: [nlp, topic-modeling]
---

Given a corpus description (document count, avg length, domain, language, compute budget), output:

1. Algorithm. LDA / NMF / BERTopic / Top2Vec / FASTopic. One-sentence reason.
2. Configuration. Number of topics: `recommended = max(5, round(sqrt(n_docs)))`, clamped to 200 for corpora under 40,000 docs; permit >200 only when the corpus is genuinely large (>40k) and note the increased compute cost. `min_df` / `max_df` filters and embedding model for neural approaches also belong here.
3. Evaluation. Topic coherence (c_v) via `gensim.models.CoherenceModel`, topic diversity, and a 20-sample human read.
4. Failure mode to probe. For LDA, "junk topics" absorbing stopwords and frequent terms. For BERTopic, the -1 outlier cluster swallowing ambiguous documents.

Refuse BERTopic on documents longer than the embedding model's context window without a chunking strategy. Refuse LDA on very short text (tweets, reviews under 10 tokens) as coherence collapses. Flag any n_topics choice below 5 as likely wrong; flag >200 on corpora under 40k docs as likely over-splitting.
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;


## Tập luyện bài tập

1. **Easy.**LDA phù hợp với 5 chủ đề trên bộ dữ liệu 20 Newsgroups. In 10 từ hàng đầu cho mỗi chủ đề. Đánh dấu mỗi chủ đề bằng tay. Algoritm đã tìm thấy các loại thực sự?
2. **Medium.**Đáp BERTopic trên cùng 20 Newsgroups. So sánh số lượng các chủ đề được tìm thấy, từ hàng đầu và tính kết hợp chất lượng so với LDA.
3. **Hard.**Xét tính độ liên kết c_v cho cả LDA và BERTopic trên cơ sở của bạn. Đi kèm với 5, 10, 20, 50 chủ đề.
> 1. **简单。**Trong 20 nhóm tin tức trên số liệu tập hợp sử dụng 5 chủ đề phù hợp LDA;. in mỗi chủ đề top 10 từ;.
2. **中等。**Trong cùng 20 Newsgroups 子集上适合BERTopic.
3. **困难。**Trong ngôn ngữ của bạn tính toán LDA và BERTopic của c_v 连贯度──分别使用 5、10、20、50 题运行──绘制连贯度 vs.题数──报告哪种方法在题数变化下更稳定──

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Topic | A thing the corpus is about | A probability distribution over words (LDA) or a cluster of similar documents (BERTopic). |
| Mixed membership | Doc is multiple topics | LDA assigns each document a distribution over all topics. |
| UMAP | Dimensionality reduction | Manifold learning that preserves local structure; used in BERTopic. |
| HDBSCAN | Density clustering | Finds variable-size clusters; produces "noise" label (-1) for outliers. |
| c_v coherence | Topic quality metric | Average pointwise mutual information of top topic words within sliding windows. |
>  Từ ngữ  Mọi người thường nói 
|------|-----------|---------|
| 主题 | 语料关于的东西 | 词的概率分布（LDA）或相似文档的聚类（BERTopic）。 |
| 混合成员资格 | 文档是多个主题 | LDA 为每篇文档分配所有主题上的分布。 |
| UMAP | 降维 | 保留局部结构的流形学习；BERTopic 中使用。 |
| HDBSCAN | 密度聚类 | 找到变大小聚类；为离群值产生 "噪声" 标签（-1）。 |
| c_v 连贯度 | 主题质量指标 | 滑动窗口内顶级主题词的平均逐点互信息。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) báo LDA.
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) Báo chí BERTopic.
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) tờ báo giới thiệu c_v và bạn bè.
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) tài liệu tham khảo sản xuất.
> - [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) LDA 论文。
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) BERTopic 论文──
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) 引入 c_v 及相关标标的论文──
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) 生产参考──优秀示例──
