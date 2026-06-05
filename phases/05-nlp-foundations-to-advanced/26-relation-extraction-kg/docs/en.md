# Relation Extraction & Knowledge Graph Construction | 关系抽取与知识图谱构建

> NER found the entities. Entity linking anchored them. Relation extraction finds the edges between them. A knowledge graph is the sum of nodes, edges, and their provenance.
> NER 找到了实体。实体链接锚定了它们。关系抽取找到它们之间的边。知识图谱是节点、边及其来源的总和。

> **【中文解读】** 从文本中抽取实体间关系，构建知识图谱。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 25 (Entity Linking) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 25（实体链接）
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

Relation Extraction (RE) turns free text into structured triples: (subject, relation, object). "Apple was founded by Steve Jobs" → (Apple, founded_by, Steve Jobs). Knowledge graphs power recommendation systems, question answering, drug discovery, and compliance monitoring.

> 关系抽取（RE）将自由文本转化为结构化三元组：(主语, 关系, 宾语)。"Apple was founded by Steve Jobs" → (Apple, founded_by, Steve Jobs)。知识图驱动推荐系统、问答、药物发现和合规监控。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。

The 2026 problem: LLMs extract relations enthusiastically but hallucinate edges that do not exist in the source text. Precision matters more than recall in production KG construction.

> 2026 年的问题：LLM 热情地抽取关系但会幻觉源文本中不存在的边。在生产知识图谱构建中，精确率比召回率更重要。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。

**Supervised RE.** Train a classifier on labeled relation examples. Input: sentence + entity pair. Output: relation type. Requires labeled data.

> **有监督 RE。** 在标注关系样本上训练分类器。输入：句子 + 实体对。输出：关系类型。需要标注数据。

**Distant supervision.** Align text with existing KB triples. If (A, born_in, B) exists in the KB, any sentence mentioning both A and B is a positive example. Noisy but scalable.

> **远程监督。** 将文本与现有知识库三元组对齐。如果知识库中存在 (A, born_in, B)，任何同时提及 A 和 B 的句子都是正例。有噪声但可扩展。

**LLM-based RE.** Prompt the LLM to extract relations. High recall, variable precision. Needs verification.

> **基于 LLM 的 RE。** 提示 LLM 抽取关系。高召回率，精确率不稳定。需要验证。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了范式转变。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。

```python
def extract_relations(text, entities, llm):
    prompt = f"""Extract all relations between entities from this text.
Text: {text}
Entities: {entities}
Output as JSON list of {{"subject": "...", "relation": "...", "object": "..."}}."""
    return llm(prompt)
```

> **【中文解读】** 本节展示如何用成熟框架快速应用该技术。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。

## Use It | 用框架实现

> **【中文解读】** 本节关注如何将模型部署为可用的产品。

- **spaCy + RE models.** Production pipeline for RE. / spaCy + RE 模型。生产 RE 流水线。
- **Hugging Face RE models.** Fine-tuned BERT for relation classification. / Hugging Face RE 模型。
- **LLM + verification.** Extract with LLM, verify against source. / LLM + 验证。
- **Neo4j.** Store and query knowledge graphs. / Neo4j。存储和查询知识图谱。

## Ship It | 产出物

Save as `outputs/skill-re-kg-builder.md`:

> 保存为 `outputs/skill-re-kg-builder.md`：

```markdown
Given a corpus and entity types, build a knowledge graph.
1. RE approach (supervised, distant supervision, LLM).
2. Verification strategy (precision vs recall).
3. KG storage (Neo4j, RDF, property graph).
```

## Exercises | 练习题

1. **Easy.** Extract relations from 10 sentences using regex patterns. / **简单。** 用正则模式从 10 句话中抽取关系。
2. **Medium.** Fine-tune a BERT model for relation classification on TACRED. / **中等。** 在 TACRED 上微调 BERT 关系分类模型。
3. **Hard.** Build a complete KG pipeline: NER → EL → RE → Neo4j. / **困难。** 构建完整 KG 流水线。

## Key Terms | 术语速查表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Relation extraction（关系抽取） | Extract (subject, relation, object) triples from text. / 从文本提取三元组。 |
| Knowledge graph（知识图谱） | Structured graph of entities and relations. / 实体和关系的结构化图。 |
| Distant supervision（远程监督） | Auto-label using existing KB. / 用现有知识库自动标注。 |

## Further Reading | 延伸阅读

- [TACRED](https://nlp.stanford.edu/pubs/tacred17.pdf) — relation extraction dataset. / 关系抽取数据集。
- [Neo4j](https://neo4j.com/) — graph database. / 图数据库。
