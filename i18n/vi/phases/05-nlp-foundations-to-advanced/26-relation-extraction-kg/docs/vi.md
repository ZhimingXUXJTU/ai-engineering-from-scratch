# Xây dựng biểu đồ kiến thức và kết nối

> NER tìm thấy các thực thể. thực thể liên kết được neo chúng. Khóa kết nối tìm thấy các cạnh giữa chúng. Hình đồ kiến thức là tổng số các nút, cạnh và nguồn gốc của chúng.
> NER tìm thấy vật thể. Các liên kết vật thể đã xác định chúng.

> **【中文解读】**Từ văn bản thu hút các mối quan hệ thực tế, xây dựng các bản đồ kiến thức.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 25 (Entity Linking) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 25（实体链接）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Vấn đề  vấn đề giới thiệu

Relation Extraction (RE) biến văn bản tự do thành ba cấu trúc: ( chủ đề, mối quan hệ, đối tượng). "Apple được thành lập bởi Steve Jobs" → (Apple, được thành lập bởi Steve Jobs).

> 关系抽取(RE)将自由文本转化为结构化三元组:(主语, 关系, 宾语) ・・・"Apple được thành lập bởi Steve Jobs" → (Apple, được thành lập bởi Steve Jobs) ・・・知识图驱动推系统、问答、药物发现和合规监控。

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Vấn đề năm 2026: LLM thu hút các mối quan hệ với sự nhiệt tình nhưng tạo ảo giác về các cạnh không tồn tại trong văn bản nguồn.

> Câu hỏi năm 2026: LLM 热情地抽取关系但会幻源文本中不存在的边缘―― trong việc xây dựng bản đồ kiến thức sản xuất, tỷ lệ xác định quan trọng hơn tỷ lệ triệu hồi――

## Khái niệm cốt lõi

> **【中文解读】**本节介绍核心概念和理论基础──

**Supervised RE.**Đào tạo một phân loại trên các ví dụ liên quan có nhãn. Nhập: câu + cặp thực thể. Xuất: loại liên quan.

> **有监督 RE。**Trong các mô hình biểu tượng, các mô hình biểu tượng được tạo ra bởi các mô hình biểu tượng.

**Distant supervision.**Thích văn bản với các KB ba hiện có. Nếu (A, born_in, B) tồn tại trong KB, bất kỳ câu nào đề cập cả A và B là một ví dụ tích cực. ồn ào nhưng có thể mở rộng.

> **远程监督。**Để phân tích văn bản với các kiến thức hiện có, nếu trong các kiến thức tồn tại (A, sinh ra, B), bất kỳ lúc nào đề cập đến A và B các câu đều là đúng ví dụ.

**LLM-based RE.**Cố gắng để có thể thu thập các mối quan hệ, nhớ lại cao, độ chính xác biến đổi, cần xác minh.

> **基于 LLM 的 RE。**提示 LLM 抽取关系──高召回率,精确率不稳定──需要验证──

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua một quá trình chuyển đổi.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI trong doanh nghiệp hiện tại.
```figure
relation-triples
```

## Hãy xây dựng nó

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**Bài viết này thông qua mã từ zero thực hiện các thuật toán cốt lõi.

```python
def extract_relations(text, entities, llm):
    prompt = f"""Extract all relations between entities from this text.
Text: {text}
Entities: {entities}
Output as JSON list of {{"subject": "...", "relation": "...", "object": "..."}}."""
    return llm(prompt)
```

> **【中文解读】**Bài này sẽ cho thấy cách sử dụng một khuôn khổ đã trưởng thành để nhanh chóng áp dụng công nghệ này.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**Bài viết này tập trung vào cách thức triển khai mô hình cho các sản phẩm có thể sử dụng.

- **spaCy + RE models.**Đường ống sản xuất cho RE. / spaCy + RE 模型──生产 RE 流水线──
- **Hugging Face RE models.**BERT được điều chỉnh tốt cho việc phân loại mối quan hệ. / Hugging Face RE 模型。
- **LLM + verification.**Thu thập bằng LLM, xác minh với nguồn gốc. / LLM + 验证。
- **Neo4j.**Cung cấp và truy vấn các biểu đồ kiến thức. / Neo4j── lưu trữ và truy vấn kiến thức

## Chuyển nó đi.

Cứ như `outputs/skill-re-kg-builder.md`- Có thể là:

> 保存为 `outputs/skill-re-kg-builder.md`- Có thể là:

```markdown
Given a corpus and entity types, build a knowledge graph.
1. RE approach (supervised, distant supervision, LLM).
2. Verification strategy (precision vs recall).
3. KG storage (Neo4j, RDF, property graph).
```

## Tập luyện bài tập

1. **Easy.**Tạo ra các mối quan hệ từ 10 câu bằng cách sử dụng các mô hình regex. / **简单。**Sử dụng mô hình thực tế từ 10 câu trong việc rút quan hệ.
2. **Medium.**Hoán chỉnh mô hình BERT để phân loại mối quan hệ trên TACRED. / **中等。**Trong TACRED 上微调 BERT 关系分类模型──
3. **Hard.**Xây dựng một đường ống KG hoàn chỉnh: NER → EL → RE → Neo4j. / **困难。**构建完整 KG 流水线──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Relation extraction（关系抽取） | Extract (subject, relation, object) triples from text. / 从文本提取三元组。 |
| Knowledge graph（知识图谱） | Structured graph of entities and relations. / 实体和关系的结构化图。 |
| Distant supervision（远程监督） | Auto-label using existing KB. / 用现有知识库自动标注。 |

## Xem thêm 延伸阅读

- [TACRED](https://nlp.stanford.edu/pubs/tacred17.pdf) relation extraction dataset. / 关系抽取数据集──
- [Neo4j](https://neo4j.com/) cơ sở dữ liệu đồ thị. / 图数据库。
