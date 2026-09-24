# 关于此事,我们需要一个问题.

> "她打电话给他,他没有回答.医生在午餐上".三次提到两个人,没有人被命名.
> "她打电话给他.他没有回答.医生在午餐. "三指代涉及两个人,没有人被点名.

> **【中文解读】**将文本中的代词和名词短语链接到它们指代的实体.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

核心参考解析将指向同一实体的每个表达式联系在一起. "巴拉克奥巴马","总统","他","奥巴马"都指向一个人.没有它,你的NER系统报告了四个实体而不是一个,你的知识图片碎片,你的总结器将主题放下文档中部.

> 没有它,你的NER系统报告四个实体而不是一个,知识图碎,摘要器在文档中丢弃主语――

> **【中文解读】**本节提出的问题是:如何正确理解和应用这一技术在实际工程中.

2026年为什么这很重要:LLM在其背景窗口内隐含地处理核心引用,但RAG检索仍然需要明确的解决方案.如果用户问"她说什么?",检索者需要知道"她"是谁,才能找到正确的部分.

> 2026年为什么重要:LLM 在上下文窗口内隐式处理共指,但RAG检索仍然需要显然消解――如果用户问"她说什么?",检索器在找到正确的块之前需要知道"她"是谁――

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.

**Mention detection.**找出所有可能指一个实体的名词词和代词.

> **指称检测。**找到所有可能指向实体名词短语和代词――使用 POS标签和分析树――

**Coreference clustering.**组提到指相同的实体. 提到对分类器,基于跨度模型或端到端神经方法 (Lee等人,2017).

> **共指聚类。**将指向同一实体的指称分组――指称分类器――基于跨度模型或端到端神经方法――

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构.

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.
```figure
coref-links
```

## 建立它

## 建立它,实现它.

> **【中文解读】**本节通过代码从零实现核心算法.

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

> **【中文解读】**本节展示了如何使用成熟框架快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能.

## 用它实现框架

> **【中文解读】**本节关注如何将模型部署为可用产品.

- **spaCy with coreferee.**制作核心指南/spaCy +核心指南.
- **Hugging Face span-based models.**基于跨度模型.
- **LLM prompting.**要求法师解决核心问题. 精确性,高成本.

## 运送它.

保存如`outputs/skill-coref-picker.md`其他:

> 保存为`outputs/skill-coref-picker.md`其他:

```markdown
Given a text and need for entity tracking, pick coreference approach.
1. Rule-based vs neural vs LLM.
2. Language support.
3. Latency budget.
```

## 练习题

1. **Easy.**通过 POS 标签实现代名词分辨率. / **简单。**用 POS标签实现代词消解.
2. **Medium.**根据50句的语句,评估SPACy核心受访者.**中等。**在50句语料上评估空间的核心受访者.
3. **Hard.**构建一个RAG预处理器,在分解之前解决核心引用.**困难。**构建在分块前消解共指的RAG预处理器──

## 关键词 快速查找表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Coreference（共指） | Multiple expressions referring to the same entity. / 多个表达指向同一实体。 |
| Mention（指称） | A textual reference to an entity. / 对实体的文本引用。 |
| Anaphora（回指） | Pronoun referring to an earlier noun. / 代词指向前面的名词。 |

## 继续阅读 继续阅读

- [Lee et al. (2017). End-to-end Neural Coreference Resolution](https://arxiv.org/abs/1707.07045)基于跨度的方法.
- [coreferee](https://github.com/explosion/coreferee) spaCy核心参考插件. / spaCy 共指插件──
