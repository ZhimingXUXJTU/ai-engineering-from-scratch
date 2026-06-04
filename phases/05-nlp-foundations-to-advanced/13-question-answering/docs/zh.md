# 问答系统

> 三种系统塑造了现代问答。抽取式找到文本片段。检索增强将答案锚定在文档中。生成式产生答案。每个现代 AI 助手都是三者的混合。

> **【中文解读】** 从信息检索到生成式问答。RAG 就是一种问答系统。

**类型：** 构建
**编程语言：** Python
**前置课程：** Phase 5 · 11（机器翻译），Phase 5 · 10（注意力机制）
**预计时长：** ~75 分钟

## 问题引入

用户输入 "When did the first iPhone launch?" 并期望得到 "June 29, 2007."。不是 "Apple's history is long and varied."。不是孤立的 "2007" 没有句子上下文。一个直接、有据可依、正确的答案。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


过去十年中三种架构主导了问答。

- **抽取式问答（Extractive QA）。** 给定一个问题和已知包含答案的段落，找到答案在段落中的起始和结束索引。SQuAD 是经典基准。
- **开放域问答（Open-domain QA）。** 段落未给定。先检索相关段落，然后抽取或生成答案。这是当今每个 RAG 流水线的基石。
- **生成式/闭卷问答（Generative / Closed-book QA）。** 大语言模型从参数化记忆中回答。无检索。推理最快，事实可靠性最低。

2026 年的趋势是混合：检索最佳几个段落，然后提示生成模型在这些段落基础上回答。这就是 RAG，第 14 课深入讲解检索部分。本课构建问答部分。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![问答架构：抽取式、检索增强、生成式](../assets/qa.svg)

**抽取式。** 用 Transformer（BERT 系列）一起编码问题和段落。训练两个预测答案起始和结束 token 索引的头。损失是有效位置上的交叉熵。输出是段落中的一个片段。不会幻觉（结构上如此），无法处理段落不能回答的问题（结构上如此）。

**检索增强（RAG）。** 两个阶段。第一，检索器从语料库中找到 top-`k` 段落。第二，阅读器（抽取式或生成式）使用这些段落产生答案。检索器-阅读器分离允许各自独立训练和评估。现代 RAG 通常在两者之间添加重排序器。

**生成式。** 仅解码器的 LLM（GPT、Claude、Llama）从学习到的权重中回答。无检索步骤。在常见知识上出色，在罕见或近期事实上灾难性。幻觉率与预训练数据中的事实频率负相关。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。





## 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


### 步骤 1：用预训练模型做抽取式问答

```python
from transformers import pipeline

qa = pipeline("question-answering", model="deepset/roberta-base-squad2")

passage = (
    "Apple Inc. released the first iPhone on June 29, 2007. "
    "The device was announced by Steve Jobs at Macworld in January 2007."
)
question = "When was the first iPhone released?"

answer = qa(question=question, context=passage)
print(answer)
```

```python
{'score': 0.98, 'start': 57, 'end': 70, 'answer': 'June 29, 2007'}
```

`deepset/roberta-base-squad2` 在 SQuAD 2.0 上训练，包含不可回答的问题。默认情况下，`question-answering` 流水线返回得分最高的片段，即使模型的空分数胜出——它不自动返回空答案。要获得显式的 "无答案" 行为，在流水线调用中传入 `handle_impossible_answer=True`：流水线只在空分数超过所有片段分数时返回空答案。无论哪种方式都要检查 `score` 字段。

### 步骤 2：检索增强流水线（概要）

```python
from sentence_transformers import SentenceTransformer
import numpy as np

encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

corpus = [
    "Apple Inc. released the first iPhone on June 29, 2007.",
    "Macworld 2007 featured the iPhone announcement by Steve Jobs.",
    "Android launched in 2008 as Google's mobile operating system.",
    "The first iPod was released in 2001.",
]
corpus_embeddings = encoder.encode(corpus, normalize_embeddings=True)


def retrieve(question, top_k=2):
    q_emb = encoder.encode([question], normalize_embeddings=True)
    sims = (corpus_embeddings @ q_emb.T).squeeze()
    order = np.argsort(-sims)[:top_k]
    return [corpus[i] for i in order]


def answer(question):
    passages = retrieve(question, top_k=2)
    combined = " ".join(passages)
    return qa(question=question, context=combined)


print(answer("When was the first iPhone released?"))
```

两阶段流水线。稠密检索器（Sentence-BERT）通过语义相似度找到相关段落。抽取式阅读器（RoBERTa-SQuAD）从合并的 top 段落中提取答案片段。适用于小语料库。对于百万级文档语料，使用 FAISS 或向量数据库。

### 步骤 3：用 RAG 做生成式

```python
def rag_generate(question, llm):
    passages = retrieve(question, top_k=3)
    prompt = f"""Context:
{chr(10).join('- ' + p for p in passages)}

Question: {question}

Answer using only the context above. If the context does not contain the answer, say "I don't know."
"""
    return llm(prompt)
```

提示模式很重要。显式告诉模型基于上下文回答并在上下文不足时返回 "I don't know"，相比朴素提示将幻觉率降低 40-60%。更精细的模式添加引用、置信度分数和结构化抽取。

### 步骤 4：反映真实世界的评估

SQuAD 使用**精确匹配（Exact Match, EM）** 和 **token 级 F1**。EM 是归一化后的严格匹配（小写、去除标点、去除冠词）——预测要么精确匹配，要么得 0。F1 在预测和参考的 token 重叠上计算，给部分分。两者都低估释义："June 29, 2007" vs "June 29th, 2007" 通常得 0 EM（序数词破坏归一化）但仍从重叠 token 获得可观的 F1。

对于生产问答：

- **答案准确率**（LLM 评判或人工评判，因为指标不捕获语义等价）。
- **引用准确率。** 引用的段落是否实际支持答案？用生成引用和检索段落之间的字符串匹配即可轻松自动检查。
- **拒绝校准。** 当答案不在检索段落中时，系统是否正确地说 "I don't know"？测量虚假置信率。
- **检索召回率。** 在评估阅读器之前，测量检索器是否将正确段落放入 top-`k`。阅读器无法修复缺失的段落。

### RAGAS：2026 年生产评估框架

`RAGAS` 专为 RAG 系统构建，是 2026 年的发布默认选择。它在不需要黄金参考的情况下从四个维度评分：

- **忠实度（Faithfulness）。** 答案中的每个声明是否来自检索的上下文？通过基于 NLI 的蕴含关系测量。你的主要幻觉指标。
- **答案相关性。** 答案是否回应了问题？通过从答案生成假设问题并与真实问题比较来测量。
- **上下文精确率。** 检索的块中，有多少实际上是相关的？低精确率 = 提示中的噪声。
- **上下文召回率。** 检索集是否包含所有需要的信息？低召回率 = 阅读器无法成功。

无参考评分让你可以在实时生产流量上评估，无需策划黄金答案。在精确匹配指标无用的开放式问题上叠加 LLM 评委。

`pip install ragas`。接入你的检索器 + 阅读器。每个查询获得四个标量。回归时报警。

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。




> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## 用框架实现

2026 年技术栈。

| 使用场景 | 推荐 |
|---------|------|
| 给定段落，找答案片段 | `deepset/roberta-base-squad2` |
| 固定语料上，闭卷不可接受 | RAG：稠密检索器 + LLM 阅读器 |
| 实时文档存储 | RAG 配混合（BM25 + 稠密）检索器 + 重排序器（第 14 课） |
| 对话式问答（追问） | 带对话历史的 LLM + 每轮 RAG |
| 高度事实性、受监管领域 | 在权威语料上的抽取式；永远不要单独用生成式 |

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


抽取式问答在 2026 年不流行了，因为带 LLM 的 RAG 处理了更多情况。它仍然在需要逐字引用的场景中发布：法律研究、合规监管、审计工具。



## 产出物

保存为 `outputs/skill-qa-architect.md`：

```markdown
---
name: qa-architect
description: Choose QA architecture, retrieval strategy, and evaluation plan.
version: 1.0.0
phase: 5
lesson: 13
tags: [nlp, qa, rag]
---

Given requirements (corpus size, question type, factuality constraint, latency budget), output:

1. Architecture. Extractive, RAG with extractive reader, RAG with generative reader, or closed-book LLM. One-sentence reason.
2. Retriever. None, BM25, dense (name the encoder), or hybrid.
3. Reader. SQuAD-tuned model, LLM by name, or "domain-fine-tuned DistilBERT."
4. Evaluation. EM + F1 for extractive benchmarks; answer accuracy + citation accuracy + refusal calibration for production. Name what you are measuring and how you are measuring it.

Refuse closed-book LLM answers for regulatory or compliance-sensitive questions. Refuse any QA system without a retrieval-recall baseline (you cannot evaluate the reader without knowing the retriever surfaced the right passage). Flag questions that require multi-hop reasoning as needing specialized multi-hop retrievers like HotpotQA-trained systems.
```

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


## 练习题

1. **简单。** 在 10 篇维基百科段落上设置上述 SQuAD 抽取式流水线。手工设计 10 个问题。测量答案正确率。如果段落和问题干净，你应该看到 7-9 个正确。
2. **中等。** 添加拒绝分类器。当最高检索分数低于阈值（比如 0.3 余弦）时，返回 "I don't know" 而不是调用阅读器。在留出集上调整阈值。
3. **困难。** 在你选择的 10,000 文档语料上构建 RAG 流水线。实现混合检索（BM25 + 稠密）加 RRF 融合（见第 14 课）。测量有和没有混合步骤的答案准确率。记录哪些问题类型受益最大。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 抽取式问答 | 找答案片段 | 预测给定段落中答案的起始和结束索引。 |
| 开放域问答 | 语料上的问答 | 无给定段落；必须先检索再回答。 |
| RAG | 检索再生成 | 检索增强生成。检索器 + 阅读器流水线。 |
| SQuAD | 经典基准 | 斯坦福问答数据集。EM + F1 指标。 |
| 幻觉 | 编造答案 | 阅读器输出不被检索上下文支持。 |
| 拒绝校准 | 知道何时闭嘴 | 系统在无法回答时正确地说 "I don't know"。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## 延伸阅读

- [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) — 基准论文。
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) — DPR，问答的经典稠密检索器。
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — 命名 RAG 的论文。
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997) — 综合 RAG 综述。
