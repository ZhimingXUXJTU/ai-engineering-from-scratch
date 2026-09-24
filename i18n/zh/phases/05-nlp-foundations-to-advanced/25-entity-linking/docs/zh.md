# 实体链接与消歧

> 没有链接,你的知识图仍然模糊.
> 没有链接,你的知识图谱保持模糊.

> **【中文解读】**将NER提取的实体链接到知识库中的唯一条目.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 22 (Embedding Models) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 22（嵌入模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

实体链接 (EL) 解决每个提到的知识库 (Wikidata,Wikipedia,GeoNames) 中的独特条目. 两个步骤的管道:候选人生成 (找到可能的匹配) 和解读 (选择正确的).

> 实体链接(EL) 将每个指称解析为知识库(维基数据、维基百科、地名) 中唯一条目──两步流水线:候选生成(找到可能的匹配) 和消歧(选择正确的) ⋅

> **【中文解读】**本节提出的问题是:如何正确理解和应用这一技术在实际工程中.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.

**Candidate generation.**根据"约旦", KB 输入中的哪个符合? 使用字符串匹配,重定位分辨率和人气优先级.通常检索前10-50名候选人.

> **候选生成。**给定"约旦",哪些知识库条目匹配?使用字符串匹配、重定向解析和流行度先验──通常检索前10-50个候选──

**Disambiguation.**根据背景相似性排名候选人.速度的双编码器,准确性的交叉编码器.背景 =周围文本 + KB 的实体描述.

> **消歧。**按上下文相似度排名候选人──双编码器用于速度,交叉编码器用于准确率──上下文 = 周围文本 + 知识库中的实体描述──

> **【拓展：大语言模型的工程实践】**通过GPT到ChatGPT,NLP 领域经历了范式转变.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构.

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.

## 建立它,实现它.

> **【中文解读】**本节通过代码从零实现核心算法.
```figure
gx-entity-linking
```

## 建立它

### 步骤1:从维基百科转向构建一个别名索引

```python
alias_to_entities = {
    "jordan": ["Q41421 (Michael Jordan)", "Q810 (Jordan, country)", "Q254110 (Michael B. Jordan)"],
    "paris":  ["Q90 (Paris, France)", "Q663094 (Paris, Texas)", "Q55411 (Paris Hilton)"],
    "apple":  ["Q312 (Apple Inc.)", "Q89 (apple, fruit)"],
}
```

维基百科号数据: ~18M (号,实体) 对. 从维基百科号下载. 作为逆向索引存储.

### 步骤2:基于环境的置歧义

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

> **【中文解读】**本节展示了如何使用成熟框架快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能.

## 用它实现框架

> **【中文解读】**本节关注如何将模型部署为可用产品.

- **OpenTapioca.**轻量EL的维基数据. /OpenTapioca──维基数据 轻量EL──
- **REL (Radboud Entity Linker).**最新的维基百科 EL. / REL──先进维基百科 EL──
- **GENRE.**通过Facebook链接的自归实体链接.
- **LLM prompting.**要求法师明确.

## 运送它.

保存如`outputs/skill-entity-linker.md`其他:

> 保存为`outputs/skill-entity-linker.md`其他:

```markdown
Given mentions from NER, link them to a knowledge base.
1. KB choice (Wikidata, Wikipedia, custom).
2. Candidate generation strategy.
3. Disambiguation method (embedding similarity, cross-encoder, LLM).
```

## 练习题

1. **Easy.**建立一个基于维基百科的候选生成器.**简单。**基于维基百科的候选生成器.
2. **Medium.**实施双码码解读和评估在测试组上. / **中等。**实现双编码器消歧──
3. **Hard.**在多语言数据集中,对 LLM 基于 EL 与神经 EL 进行比较. / **困难。**在多语言数据集中,比较LLM EL与神经 EL.

## 关键词 快速查找表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Entity linking（实体链接） | Map mentions to KB entries. / 将指称映射到知识库条目。 |
| Disambiguation（消歧） | Pick the correct entity among candidates. / 在候选中选择正确实体。 |
| Candidate generation（候选生成） | Retrieve possible KB matches for a mention. / 为指称检索可能的知识库匹配。 |

## 继续阅读 继续阅读

- [Wu et al. (2020). Scalable Zero-shot Entity Linking](https://arxiv.org/abs/1910.02854)其他类型的实体链接
- [De Cao et al. (2020). GENRE](https://arxiv.org/abs/1912.01572)现在,我们已经开始了.
