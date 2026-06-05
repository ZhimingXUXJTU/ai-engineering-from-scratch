# Entity Linking & Disambiguation | 实体链接与消歧

> NER found "Paris." Entity linking decides: Paris, France? Paris Hilton? Paris, Texas? Paris (the Trojan prince)? Without linking, your knowledge graph stays ambiguous.
> NER 找到了 "Paris"。实体链接决定：巴黎（法国）？帕里斯·希尔顿？巴黎（德克萨斯）？帕里斯（特洛伊王子）？没有链接，你的知识图谱保持模糊。

> **【中文解读】** 将 NER 提取的实体链接到知识库中的唯一条目。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 22 (Embedding Models) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 22（嵌入模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

Entity linking (EL) resolves each mention to a unique entry in a knowledge base (Wikidata, Wikipedia, GeoNames). The two-step pipeline: candidate generation (find possible matches) and disambiguation (pick the right one).

> 实体链接（EL）将每个指称解析为知识库（Wikidata、Wikipedia、GeoNames）中的唯一条目。两步流水线：候选生成（找到可能的匹配）和消歧（选择正确的）。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。

**Candidate generation.** Given "Jordan," which KB entries match? Use string matching, redirect resolution, and popularity priors. Typically retrieve top 10-50 candidates.

> **候选生成。** 给定 "Jordan"，哪些知识库条目匹配？使用字符串匹配、重定向解析和流行度先验。通常检索前 10-50 个候选。

**Disambiguation.** Rank candidates by context similarity. Bi-encoder for speed, cross-encoder for accuracy. Context = surrounding text + entity description from KB.

> **消歧。** 按上下文相似度排名候选。双编码器用于速度，交叉编码器用于准确率。上下文 = 周围文本 + 知识库中的实体描述。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了范式转变。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。

```python
def entity_link(mention, context, kb_lookup, embed_model):
    candidates = kb_lookup.get(mention.lower(), [])
    if not candidates:
        return None
    ctx_emb = embed_model.encode([context])
    scores = []
    for cand in candidates:
        cand_emb = embed_model.encode([cand["description"]])
        scores.append((cand, float(np.dot(ctx_emb[0], cand_emb[0]))))
    return max(scores, key=lambda x: x[1])[0]
```

> **【中文解读】** 本节展示如何用成熟框架快速应用该技术。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。

## Use It | 用框架实现

> **【中文解读】** 本节关注如何将模型部署为可用的产品。

- **OpenTapioca.** Lightweight EL for Wikidata. / OpenTapioca。Wikidata 轻量 EL。
- **REL (Radboud Entity Linker).** State-of-the-art Wikipedia EL. / REL。先进 Wikipedia EL。
- **GENRE.** Autoregressive entity linking by Facebook. / GENRE。Facebook 自回归实体链接。
- **LLM prompting.** Ask the LLM to disambiguate. / LLM 提示消歧。

## Ship It | 产出物

Save as `outputs/skill-entity-linker.md`:

> 保存为 `outputs/skill-entity-linker.md`：

```markdown
Given mentions from NER, link them to a knowledge base.
1. KB choice (Wikidata, Wikipedia, custom).
2. Candidate generation strategy.
3. Disambiguation method (embedding similarity, cross-encoder, LLM).
```

## Exercises | 练习题

1. **Easy.** Build a Wikipedia-based candidate generator. / **简单。** 构建基于 Wikipedia 的候选生成器。
2. **Medium.** Implement bi-encoder disambiguation and evaluate on a test set. / **中等。** 实现双编码器消歧。
3. **Hard.** Compare LLM-based EL vs neural EL on a multilingual dataset. / **困难。** 在多语言数据集上比较 LLM EL vs 神经 EL。

## Key Terms | 术语速查表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Entity linking（实体链接） | Map mentions to KB entries. / 将指称映射到知识库条目。 |
| Disambiguation（消歧） | Pick the correct entity among candidates. / 在候选中选择正确实体。 |
| Candidate generation（候选生成） | Retrieve possible KB matches for a mention. / 为指称检索可能的知识库匹配。 |

## Further Reading | 延伸阅读

- [Wu et al. (2020). Scalable Zero-shot Entity Linking](https://arxiv.org/abs/1910.02854) / 可扩展零样本实体链接。
- [De Cao et al. (2020). GENRE](https://arxiv.org/abs/1912.01572) / 自回归实体链接。
