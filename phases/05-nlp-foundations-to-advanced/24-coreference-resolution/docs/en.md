# Coreference Resolution | 共指消解

> "She called him. He did not answer. The doctor was at lunch." Three references to two people and nobody is named. Coreference resolution figures out who is who.
> "She called him. He did not answer. The doctor was at lunch." 三个指代涉及两个人，没有人被点名。共指消解弄清楚谁是谁。

> **【中文解读】** 将文本中的代词和名词短语链接到它们指代的实体。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

Coreference resolution links every expression that refers to the same entity. "Barack Obama", "the president", "he", "Obama" all point to one person. Without it, your NER system reports four entities instead of one, your knowledge graph fragments, and your summarizer drops subjects mid-document.

> 共指消解将每个指向同一实体的表达链接起来。"Barack Obama"、"the president"、"he"、"Obama" 都指向一个人。没有它，你的 NER 系统报告四个实体而不是一个，知识图破碎，摘要器在文档中间丢弃主语。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。

Why it matters in 2026: LLMs handle coreference implicitly within their context window, but RAG retrieval still needs explicit resolution. If a user asks "what did she say?", the retriever needs to know who "she" is before it can find the right chunk.

> 2026 年为什么重要：LLM 在上下文窗口内隐式处理共指，但 RAG 检索仍需要显式消解。如果用户问 "what did she say?"，检索器在找到正确的块之前需要知道 "she" 是谁。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。

**Mention detection.** Find all noun phrases and pronouns that could refer to an entity. Use POS tags and parse trees.

> **指称检测。** 找到所有可能指向实体的名词短语和代词。使用 POS 标签和解析树。

**Coreference clustering.** Group mentions that refer to the same entity. Mention-pair classifiers, span-based models, or end-to-end neural approaches (Lee et al., 2017).

> **共指聚类。** 将指向同一实体的指称分组。指称对分类器、基于跨度的模型或端到端神经方法。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。

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

> **【中文解读】** 本节展示如何用成熟框架快速应用该技术。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。

## Use It | 用框架实现

> **【中文解读】** 本节关注如何将模型部署为可用的产品。

- **spaCy with coreferee.** Production coreference for English. / spaCy + coreferee。英语生产共指。
- **Hugging Face span-based models.** Neural coreference resolution. / Hugging Face 基于跨度的模型。
- **LLM prompting.** Ask the LLM to resolve coreferences. Good accuracy, high cost. / LLM 提示消解共指。

## Ship It | 产出物

Save as `outputs/skill-coref-picker.md`:

> 保存为 `outputs/skill-coref-picker.md`：

```markdown
Given a text and need for entity tracking, pick coreference approach.
1. Rule-based vs neural vs LLM.
2. Language support.
3. Latency budget.
```

## Exercises | 练习题

1. **Easy.** Implement pronoun resolution using POS tags. / **简单。** 用 POS 标签实现代词消解。
2. **Medium.** Evaluate spaCy coreferee on a 50-sentence corpus. / **中等。** 在 50 句语料上评估 spaCy coreferee。
3. **Hard.** Build a RAG preprocessor that resolves coreferences before chunking. / **困难。** 构建在分块前消解共指的 RAG 预处理器。

## Key Terms | 术语速查表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Coreference（共指） | Multiple expressions referring to the same entity. / 多个表达指向同一实体。 |
| Mention（指称） | A textual reference to an entity. / 对实体的文本引用。 |
| Anaphora（回指） | Pronoun referring to an earlier noun. / 代词指向前面的名词。 |

## Further Reading | 延伸阅读

- [Lee et al. (2017). End-to-end Neural Coreference Resolution](https://arxiv.org/abs/1707.07045) — the span-based approach. / 基于跨度的方法。
- [coreferee](https://github.com/explosion/coreferee) — spaCy coreference plugin. / spaCy 共指插件。
