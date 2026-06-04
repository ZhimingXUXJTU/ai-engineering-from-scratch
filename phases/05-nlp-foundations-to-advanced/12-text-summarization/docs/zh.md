# 文本摘要

> 抽取式系统告诉你文档说了什么。生成式系统告诉你作者的意思是什么。不同的任务，不同的陷阱。

> **【中文解读】** 抽取式 vs 生成式摘要。

**类型：** 构建
**编程语言：** Python
**前置课程：** Phase 5 · 02（BoW + TF-IDF），Phase 5 · 11（机器翻译）
**预计时长：** ~75 分钟

## 问题引入

一篇 2000 词的新闻文章出现在你的信息流中。你需要 120 个词来概括它。你可以从文章中选取最重要的三个句子（抽取式），或者用自己的话重写内容（生成式）。两者都叫摘要。它们是完全不同的问题。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


抽取式摘要是一个排序问题。给每个句子打分，返回排名前 `k` 的。输出总是合乎语法的，因为它是逐字提取的。风险是遗漏分布在整篇文章中的内容。

生成式摘要是一个生成问题。Transformer 根据输入产生新文本。输出流畅且压缩，但可能产生源中没有的事实幻觉。风险是自信的编造。

本课构建两者，以及各自拥有的失败模式。

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


## 核心概念

![抽取式 TextRank vs 生成式 Transformer](../assets/summarization.svg)

**抽取式（Extractive）。** 将文章视为图，节点是句子，边是相似度。在图上运行 PageRank（或类似算法）按句子与其他一切的连接程度打分。得分最高的句子就是摘要。经典实现是 **TextRank**（Mihalcea and Tarau, 2004）。

**生成式（Abstractive）。** 在文档-摘要对上微调 Transformer 编码器-解码器（BART、T5、Pegasus）。推理时，模型读取文档并通过交叉注意力逐 token 生成摘要。Pegasus 特别使用间隔句子预训练目标，使其无需太多微调就擅长摘要。

使用 **ROUGE**（Recall-Oriented Understudy for Gisting Evaluation）评估。ROUGE-1 和 ROUGE-2 评分一元组和二元组重叠。ROUGE-L 评分最长公共子序列。越高越好，但 40 ROUGE-L 是 "好"，50 是 "出色"。每篇论文都报告全部三个。使用 `rouge-score` 包。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。





## 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


### 步骤 1：TextRank（抽取式）

```python
import math
import re
from collections import Counter


def sentence_split(text):
    return re.split(r"(?<=[.!?])\s+", text.strip())


def similarity(s1, s2):
    w1 = Counter(s1.lower().split())
    w2 = Counter(s2.lower().split())
    intersection = sum((w1 & w2).values())
    denom = math.log(len(w1) + 1) + math.log(len(w2) + 1)
    if denom == 0:
        return 0.0
    return intersection / denom


def textrank(text, top_k=3, damping=0.85, iterations=50, epsilon=1e-4):
    sentences = sentence_split(text)
    n = len(sentences)
    if n <= top_k:
        return sentences

    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                sim[i][j] = similarity(sentences[i], sentences[j])

    scores = [1.0] * n
    for _ in range(iterations):
        new_scores = [1 - damping] * n
        for i in range(n):
            total_out = sum(sim[i]) or 1e-9
            for j in range(n):
                if sim[i][j] > 0:
                    new_scores[j] += damping * sim[i][j] / total_out * scores[i]
        if max(abs(s - ns) for s, ns in zip(scores, new_scores)) < epsilon:
            scores = new_scores
            break
        scores = new_scores

    ranked = sorted(range(n), key=lambda k: scores[k], reverse=True)[:top_k]
    ranked.sort()
    return [sentences[i] for i in ranked]
```

两件事值得注意。相似度函数使用对数归一化的词重叠，这是原始 TextRank 的变体。TF-IDF 向量的余弦相似度也行。阻尼因子 0.85 和迭代次数是 PageRank 的默认值。

### 步骤 2：用 BART 做生成式摘要

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

article = """(long news article text)"""

summary = summarizer(article, max_length=120, min_length=60, do_sample=False)
print(summary[0]["summary_text"])
```

BART-large-CNN 在 CNN/DailyMail 语料上微调。开箱即用产生新闻风格摘要。对于其他领域（科学论文、对话、法律），使用对应的 Pegasus 检查点或在目标数据上微调。

### 步骤 3：ROUGE 评估

```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
scores = scorer.score(reference_summary, generated_summary)
print({k: round(v.fmeasure, 3) for k, v in scores.items()})
```

始终使用词干提取。没有它，"running" 和 "run" 被视为不同的词，ROUGE 会低估。

### ROUGE 之外（2026 年摘要评估）

ROUGE 二十年来一直是主流摘要指标，但在 2026 年仅靠它已经不够。一项大规模 NLG 论文元分析显示：

- **BERTScore**（上下文嵌入相似度）在 2023 年获得关注，现在大多数摘要论文都与 ROUGE 一起报告。
- **BARTScore** 将评估视为生成：通过预训练 BART 给定源时分配给摘要的似然来评分。
- **MoverScore**（上下文嵌入上的推土机距离）在 2025 年摘要基准中达到顶尖，因为它比 ROUGE 更好地捕获语义重叠。
- **FactCC** 和**基于 QA 的事实性检查**在 2021-2023 年很常见，现在通常被 **G-Eval**（一种 GPT-4 提示链，用链式思维推理评分连贯性、一致性、流畅性和相关性）替代。
- **G-Eval** 和类似的 LLM 评委方法在评分标准设计良好时与人类判断约 80% 一致。

生产建议：报告 ROUGE-L 用于遗留比较，BERTScore 用于语义重叠，G-Eval 用于连贯性和事实性。针对 50-100 个人类标注摘要校准。

### 步骤 4：事实性问题

生成式摘要容易产生幻觉。抽取式摘要的幻觉风险低得多，因为输出是从源中逐字提取的，尽管如果源句子被脱离上下文、过时或乱序引用，它们仍可能误导。这是生产系统在合规相关内容上仍然偏好抽取式方法的最大原因。

需要命名的幻觉类型：

- **实体替换。** 源说 "John Smith"。摘要说 "John Brown"。
- **数字漂移。** 源说 "25,000"。摘要说 "25 million"。
- **极性翻转。** 源说 "rejected the offer"。摘要说 "accepted the offer"。
- **事实编造。** 源没有提到 CEO。摘要说 CEO 批准了。

有效的评估方法：

- **FactCC。** 在源句子和摘要句子的蕴含关系上训练的二分类器。预测事实性/非事实性。
- **基于 QA 的事实性检查。** 向 QA 模型提问源中有答案的问题。如果摘要支持不同的答案，标记。
- **实体级 F1。** 比较源与摘要中的命名实体。仅出现在摘要中的实体是可疑的。

对于事实性重要的面向用户的内容（新闻、医疗、法律、金融），抽取式是更安全的默认选择。生成式需要在循环中做事实性检查。

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。




> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## 用框架实现

2026 年技术栈：

| 使用场景 | 推荐 |
|---------|------|
| 新闻，3-5 句摘要，英语 | `facebook/bart-large-cnn` |
| 科学论文 | `google/pegasus-pubmed` 或微调的 T5 |
| 多文档，长文 | 任何 32k+ 上下文的 LLM，提示 |
| 对话摘要 | `philschmid/bart-large-cnn-samsum` |
| 抽取式，结构性低幻觉风险 | TextRank 或 `sumy` 的 LSA / LexRank |

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


2026 年在算力不是约束时，长上下文 LLM 通常超越专门模型。代价是成本和可复现性；专门模型给出更一致的输出。



## 产出物

保存为 `outputs/skill-summary-picker.md`：

```markdown
---
name: summary-picker
description: Pick extractive or abstractive, named library, factuality check.
version: 1.0.0
phase: 5
lesson: 12
tags: [nlp, summarization]
---

Given a task (document type, compliance requirement, length, compute budget), output:

1. Approach. Extractive or abstractive. Explain in one sentence why.
2. Starting model / library. Name it. `sumy.TextRankSummarizer`, `facebook/bart-large-cnn`, `google/pegasus-pubmed`, or an LLM prompt.
3. Evaluation plan. ROUGE-1, ROUGE-2, ROUGE-L (use rouge-score with stemming). Plus factuality check if abstractive.
4. One failure mode to probe. Entity swap is the most common in abstractive news summarization; flag samples where source entities do not appear in summary.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse abstractive summarization for medical, legal, financial, or regulated content without a factuality gate. Flag input over the model's context window as needing chunked map-reduce summarization (not just truncation).
```

## 练习题

1. **简单。** 在 5 篇新闻文章上运行 TextRank。将 top-3 句子与参考摘要比较。测量 ROUGE-L。在 CNN/DailyMail 风格文章上你应该看到 30-45 ROUGE-L。
2. **中等。** 实现实体级事实性：从源和摘要中提取命名实体（spaCy），计算源实体在摘要中的召回率和摘要实体对源的精确率。高精确率低召回率意味着安全但简略；低精确率意味着幻觉实体。
3. **困难。** 在 50 篇 CNN/DailyMail 文章上比较 BART-large-CNN 与 LLM（Claude 或 GPT-4）。报告 ROUGE-L、事实性（按实体 F1）和每个摘要的成本。记录各自胜出的场景。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 抽取式 | 选取句子 | 从源中逐字返回句子。不会幻觉。 |
| 生成式 | 重写 | 根据源生成新文本。可能幻觉。 |
| ROUGE | 摘要指标 | 系统输出与参考之间的 n-gram / LCS 重叠。 |
| TextRank | 基于图的抽取式 | 句子相似度图上的 PageRank。 |
| 事实性 | 对不对 | 摘要声明是否被源支持。 |
| 幻觉 | 编造内容 | 摘要中源不支持的内容。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## 延伸阅读

- [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) — 抽取式经典论文。
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461) — BART 论文。
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777) — Pegasus 和间隔句子目标。
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/) — ROUGE 论文。
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) — 事实性全景论文。
