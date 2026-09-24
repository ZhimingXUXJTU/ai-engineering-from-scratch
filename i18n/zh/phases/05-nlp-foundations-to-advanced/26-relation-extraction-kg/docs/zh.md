# 关系抽取与知识图谱构建

> 根据NER的数据,NER发现了实体.实体链接将它们结起来.关系提取发现了它们之间的边缘.知识图是节点,边缘和它们的来源的总和.
> 实体链接 确定它们 关系抽取找到它们之间的边缘 知识图谱是节点及其来源的总和

> **【中文解读】**从文本中抽取实体间关系,构建知识图谱.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 25 (Entity Linking) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 25（实体链接）
**Time:** ~60 minutes | **时间:** ~60 分钟

## 问题 问题引入

关系提取 (RE) 将自由文本转化为结构化的三重: (主题,关系,对象). "果是由史蒂夫·乔布斯创立的" → (果,由史蒂夫·乔布斯创立).知识图表表权力推系统,回答问题,药物发现和合规监测.

> 关系抽取(RE)将自由文本转化为结构化三元组:(主语,关系,宾语) ――"果是由史蒂夫·乔布斯创立的"

> **【中文解读】**本节提出的问题是:如何正确理解和应用这一技术在实际工程中.

2026年问题:LLM热情地提取关系,但在源文本中不存在的边缘都产生幻觉.

> 2026年问题:在生产知识图谱构建中,精确率比召集率更重要.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.

**Supervised RE.**训练一个分类器在标记关系的例子.输入:句子 +实体对.输出:关系类型.需要标记数据.

> **有监督 RE。**在标签关系样本上训练分类器──输入:句子 + 实体对──输出:关系类型──需要标签数据──

**Distant supervision.**配合现有 KB 三倍.如果 KB 中存在 (A, born_in, B),任何提到 A 和 B 的句子都是一个积极的例子. 噪音但可扩展.

> **远程监督。**将文本与现有知识库三元组对齐.如果知识库中存在 (A,生_在,B),任何同时提及A和B的句子都是正例.

**LLM-based RE.**让法师提取关系,提醒,变量精度,需要验证.

> **基于 LLM 的 RE。**提示 LLM 抽取关系──高召回率,精确率不稳定──需要验证──

> **【拓展：大语言模型的工程实践】**通过GPT到ChatGPT,NLP 领域经历了范式转变.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构.
```figure
relation-triples
```

## 建立它

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.

## 建立它,实现它.

> **【中文解读】**本节通过代码从零实现核心算法.

```python
def extract_relations(text, entities, llm):
    prompt = f"""Extract all relations between entities from this text.
Text: {text}
Entities: {entities}
Output as JSON list of {{"subject": "...", "relation": "...", "object": "..."}}."""
    return llm(prompt)
```

> **【中文解读】**本节展示了如何使用成熟框架快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能.

## 用它实现框架

> **【中文解读】**本节关注如何将模型部署为可用产品.

- **spaCy + RE models.**生产RE流水线――
- **Hugging Face RE models.**为了关系分类,精细调节的BERT. / 拥抱面孔RE模型――
- **LLM + verification.**通过LLM提取,根据来源验证.
- **Neo4j.**存储和查询知识图谱.

## 运送它.

保存如`outputs/skill-re-kg-builder.md`其他:

> 保存为`outputs/skill-re-kg-builder.md`其他:

```markdown
Given a corpus and entity types, build a knowledge graph.
1. RE approach (supervised, distant supervision, LLM).
2. Verification strategy (precision vs recall).
3. KG storage (Neo4j, RDF, property graph).
```

## 练习题

1. **Easy.**通过使用regex模式从10句子中提取关系. / **简单。**用正则模式从10句中抽取关系.
2. **Medium.**调整一个BERT模型,以对 TACRED的关系分类. / **中等。**在TACRED上微调BERT 关系分类模型――
3. **Hard.**建立一个完整的KG管道:NER → EL → RE → Neo4j. / **困难。**构建完整的KG流水线.

## 关键词 快速查找表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Relation extraction（关系抽取） | Extract (subject, relation, object) triples from text. / 从文本提取三元组。 |
| Knowledge graph（知识图谱） | Structured graph of entities and relations. / 实体和关系的结构化图。 |
| Distant supervision（远程监督） | Auto-label using existing KB. / 用现有知识库自动标注。 |

## 继续阅读 继续阅读

- [TACRED](https://nlp.stanford.edu/pubs/tacred17.pdf)关系抽取数据集. / 关系抽取数据集──
- [Neo4j](https://neo4j.com/)图数据库.
