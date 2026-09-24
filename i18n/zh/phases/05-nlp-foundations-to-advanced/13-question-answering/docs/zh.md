# 问答系统

> 现在,我们在研究中发现了一些技术,这些技术可以帮助我们理解这些技术.
> 三种系统塑造了现代问答――抽取式找到文本片段――检索增强将其定到文档――生成式产生答案――每个现代人工智能助手都是三者的混合――

> **【中文解读】**从信息检查到生成式问答.RAG就是一种问答系统.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 11 (Machine Translation), Phase 5 · 10 (Attention Mechanism) | **前置知识:** Phase 5 · 11 (Machine Translation), Phase 5 · 10 (Attention Mechanism)
**Time:** ~75 minutes | **时间:** ~75 minutes


## 问题 问题引入

用户输入"第一款iPhone什么时候发布?"并预计"2007年6月29日". 不是"果的历史很长,多样化. "不是"2007年"坐隔离,没有句子.
> 用户输入"首款iPhone发布时间是什么时候?"并期望得到"2007年6月29日".不"果的历史漫长而多样化.

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――


在过去十年中,三种建筑主导了质量评估.
> 过去十年中三种架构主导了问答.

- **Extractive QA.**给出一个问题和一个已知含有答案的段落,在段落中找到答案跨度的开始和结尾指数.
- **Open-domain QA.**现在,我们需要找到一个答案,然后提取一个答案.这是每一个RAG管道的基础.
- **Generative / Closed-book QA.**语言模型从其参数内存中得到答案,没有检索,最快的推断,最不靠事实.
> - **抽取式问答（Extractive QA）。**给定一个问题和已知包含答案的段落,找到答案在段落中的开始和结束索引.
- **开放域问答（Open-domain QA）。**段落未给定.先检查相关段落,然后抽取或生成答案.这是当今每个RAG流水线的基石.
- **生成式/闭卷问答（Generative / Closed-book QA）。**大语言模型从参数化记忆中回答――无检索――推理最快,事实可靠性最低――

2026年的趋势是混合式的:检索最好的几段落,然后要求一个生成模型根据这些段落回答.这是RAG,课程14涵盖检索的一半.这个课程构建了QA的一半.
> 2026年趋势是混合:检查最佳几个段落,然后提示生成模型在这些段落基础上回答――这是RAG,第14课深入讲解检查部分――本课构建问答部分――

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![QA architectures: extractive, retrieval-augmented, generative](../assets/qa.svg)
> ![问答架构：抽取式、检索增强、生成式](../assets/qa.svg)

**Extractive.**编码问题和通过与变压器 (BERT家族) 一起.训练两个头脑预测答案的开始和结束标志指数.损失是有效位置的交叉透.输出是通过的跨度.从来没有幻觉 (通过构建),从来处理问题,通过无法回答 (通过构建).
> **抽取式。**用变压器(BERT 系列) 编码问题和段落.训练两个预测答案起始和结束 代币索引的头.损失是有效位置交叉.输出是段落中的一个段段落.不会出现.

**Retrieval-augmented (RAG).**首先,一个车找到顶部的...`k`读者 (抽取或生成) 使用这些段落生成答案. 复习器-读者分区允许每个段落独立训练和评估. 现代RAG经常在它们之间添加一个重排器.
> **检索增强（RAG）。**两个阶段. 第一,检查器从语料库中找到顶部.`k`段落──第二,阅读器 (抽取式或生成式) 使用这些段落产生答案──检查器-阅读器分离允许各自独立训练和评估──现代RAG通常在两者之间添加重排序器──

**Generative.**仅使用解码器的LLM (GPT,Claude,Llama) 根据学习的重量回答.没有检索步骤.在普通知识上非常出色,在罕见或最近的事实上非常灾难性.预训数据中的幻觉率与事实频率相反相相关.
> **生成式。**仅解码器的LLM(GPT、Claude、Llama) 从学习权重中回答──无检索步骤──在常见知识上出色,在罕见或近期事实上灾难性──幻觉率与预训数据中的事实频率负相关──

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.


## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
qa-span
```

## 建立它

### 步骤1:采集型质量测试,采用预训练模型
> `deepset/roberta-base-squad2`在SquAD 2.0上训练中,包含不可回答的问题.`question-answering`流水线返回最高分数的片段,即使模型的空分数胜出它不自动返回空答案──要获得明显的"无答案"行为,在流水线调用中传入`handle_impossible_answer=True`流水线只在空分数超过所有段分数时返回空答案――无论如何都必须检查`score`字段.

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

`deepset/roberta-base-squad2`根据标准, 技术技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术的基础上, 技术`question-answering`管道返回最高得分的跨度,即使模型的零得分获胜. 它不会自动返回空答案.`handle_impossible_answer=True`输入到管道调用:只有当零分数超过每一个跨度分数时,管道才会返回空答.`score`无论如何,都会有.
> 两阶段流水线――密检索器 (Sentence-BERT) 通过语义相似度找到相关段落――抽取式阅读器 (RoBERTa-SquAD) 从合并的顶部段落中提取答案片段――适用于小语料库――对于百万级文档语料,使用 FAISS 或向量数据库――

### 步骤2:采集增强的管道 (图)
> 提示模式很重要――显然告诉模型基于上下文的回答,并在上下文不足时回复"我不知道",相比简单提示将幻觉率降低40-60%.

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

密集检索器 (Sentence-BERT) 通过语义相似性找到相关段落.提取读者 (RoBERTa-SQuAD) 从组合的顶段中抽取答案跨度. 在小型体中工作.对于百万份文件体,使用FAISS或矢量数据库.
> 鱼使用**精确匹配（Exact Match, EM）**和 **token 级 F1**△EM是重叠后的严格匹配 (小写,除标点,除冠词) 预测要么精确匹配,要么得到 0 ・ F1 在预测和参考的代币重叠上计算,给部分分量.

### 步骤3:使用RAG生成
> 对于生产问答:

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

提示模式是重要的.明确地告诉模型在文本中地并返回"我不知道"当文本不足时,与天真提示相比,幻觉率减少40-60%.更精密的模式增加了引用,信心分数和结构化提取.
> - **答案准确率**(LLM评判或人工评判,因为指标不捕获语义等价)
- **引用准确率。**引用的段落是否实际支持答案? 引用和检索段落之间的字符串匹配即可轻松自动检查.
- **拒绝校准。**当答案没有检索段落中时,系统是否正确地说"我不知道"?测量虚假信任率──
- **检索召回率。**在评估阅读器之前,测量检查器是否会正确落入顶部...`k`阅读器无法修复缺失的段落.

### 步骤4:反映现实世界的评估
> `RAGAS`专为RAG系统构建,是2026年发布的默认选择.

SQuAD使用**Exact Match (EM)**其他**token-level F1**现在,我们要去.  EM是正常化后的严格匹配 (小字母,条纹分分,删除文章) 预测完全匹配或得分0. 预测和参考之间的代币重叠计算 F1 并给予部分信贷. 两种低信用表达式:"2007年6月29日"与"2007年6月29日"通常获得0EM (顺序中断正常化),但仍然从重叠的代币中获得大量F1.
> - **忠实度（Faithfulness）。**答案中的每一个声明是否来自检查的上下文?通过基于NLI的含关系测量.
- **答案相关性。**答案是否回应了问题?通过从答案中生成假设问题并与真实的问题进行比较来测量.
- **上下文精确率。**检索的块中,实际上有多少相关?低精确率 = 提示中的噪音.
- **上下文召回率。**检索集是否包含所有需要的信息?低召回率 = 阅读器无法成功.

对于生产QA:
> 无参考评分让你能够在实时评估生产流量,无需策划黄金答案――在精确匹配指标无用的开放式问题上叠加LLM评委――

- **Answer accuracy**(LLM或人类判断,因为指标不捕捉到语义等效).
- **Citation accuracy.**引用的段落是否确实支持答案? 通过自动检查生成的引用和检索的段落之间的字符串匹配是无用的.
- **Refusal calibration.**当答案不在检索的段落中时,系统是否正确地说"我不知道"?测量虚假的信任率.
- **Retrieval recall.**在评估读者之前, 测量读者是否得到了正确的通道到上方`k`一位读者不能修复一个缺失的段落.
> `pip install ragas`△ 接入你的检查器+阅读器──每一个查询得到四个标志量──回归时报警──

### 拉加斯:2026年生产评估框架

`RAGAS`它是针对RAG系统的专用设计,并是2026年发货默认的. 它具有四个维度,而不需要黄金参考:

- **Faithfulness.**根据NLI的含义来测量. 你的主要幻觉指标.
- **Answer relevance.**通过从答案中产生假设问题并与真实问题进行比较来测量.
- **Context precision.**检索的部分中,哪些部分实际上是相关的?
- **Context recall.**检索集是否包含所有必要信息? 低回忆 = 读者无法成功.

无引用的评分让你在没有精选的黄金答案的情况下评估现场生产流量. 在开放式问题上,Layer LLM作为评审者,在准确匹配的指标是无用的.

`pip install ragas`连接回收器+读器,每次查询得到4个 skalar,警告回归.

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

现在我们要去.
> 2026 年技术──

| Use case | Recommended |
|---------|-------------|
| Given passage, find answer span | `deepset/roberta-base-squad2` |
| Over a fixed corpus, closed-book not acceptable | RAG: dense retriever + LLM reader |
| Real-time over a document store | RAG with hybrid (BM25 + dense) retriever + reranker (lesson 14) |
| Conversational QA (follow-up questions) | LLM with conversation history + RAG on each turn |
| Highly factual, regulated domains | Extractive over an authoritative corpus; never generative alone |
> 现在,我们可以在这个地方做一些事情.
|---------|------|
| 给定段落，找答案片段 | `deepset/roberta-base-squad2` |
| 固定语料上，闭卷不可接受 | RAG：稠密检索器 + LLM 阅读器 |
| 实时文档存储 | RAG 配混合（BM25 + 稠密）检索器 + 重排序器（第 14 课） |
| 对话式问答（追问） | 带对话历史的 LLM + 每轮 RAG |
| 高度事实性、受监管领域 | 在权威语料上的抽取式；永远不要单独用生成式 |

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


提取质量检查 (QA) 已经在2026年变得不流行了,因为RAG与LLM处理更多案件.它仍然在需要字面上引用的环境中运输:法律研究,监管合规,审计工具.
> 抽取式问答在2026年不流行,因为带 LLM 的RAG处理了更多情况.


## 运送它.

保存如`outputs/skill-qa-architect.md`其他:
> 保存为`outputs/skill-qa-architect.md`其他:

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

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


## 练习题

1. **Easy.**设置SQuAD提取管道上 10 个维基百科段.手工 10 个问题.测量答案是多少次正确.如果段落和问题是清洁的,你应该看到 7-9 正确.
2. **Medium.**添加拒绝分类器.当顶级检索分数低于门值时 (例如0.3 cosine),反复"我不知道"而不是打电话给读者.按一个被保留的集合调整门值.
3. **Hard.**根据您选择的10,000份文件组建一个RAG管道. 通过RRF融合实现混合检索 (BM25+密集) (见14课). 测量混合步骤和没有的答案精度. 文件中哪些问题类型最受益.
> 1. **简单。**在 10 篇维基百科段落上设置上述SQuAD 抽取式流水线――手工设计 10 个问题――测量答案正确率――如果段落和问题干净,你应该看到 7-9 个正确――
2. **中等。**添加拒绝分类器──当最高检索分数低于值时,返回"我不知道"而不是调用阅读器──在留出集上调整值──
3. **困难。**在您选择的 10,000 文档语料上构建RAG 流水线――实现混合检查(BM25 + 密) 加上RRF 融合(见第 14 课) ⋅测量有没有混合步骤的答案准确率――记录哪些问题类型受益最大――

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive QA | Find the answer span | Predict start and end indices of the answer within a given passage. |
| Open-domain QA | QA over a corpus | No given passage; must retrieve then answer. |
| RAG | Retrieve then generate | Retrieval-augmented generation. Retriever + reader pipeline. |
| SQuAD | Canonical benchmark | Stanford Question Answering Dataset. EM + F1 metrics. |
| Hallucination | Made-up answer | Reader output not supported by retrieved context. |
| Refusal calibration | Know when to shut up | System correctly says "I don't know" when unable to answer. |
> 现在,我们在这个世界里,
|------|-----------|---------|
| 抽取式问答 | 找答案片段 | 预测给定段落中答案的起始和结束索引。 |
| 开放域问答 | 语料上的问答 | 无给定段落；必须先检索再回答。 |
| RAG | 检索再生成 | 检索增强生成。检索器 + 阅读器流水线。 |
| SQuAD | 经典基准 | 斯坦福问答数据集。EM + F1 指标。 |
| 幻觉 | 编造答案 | 阅读器输出不被检索上下文支持。 |
| 拒绝校准 | 知道何时闭嘴 | 系统在无法回答时正确地说 "I don't know"。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250)参考文件.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906)DPR,是QA的常规密度检索器.
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)报纸称Rag.
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997)全面的RAG调查.
> - [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250)基准论文──
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) 问答的经典密检索器──
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) 命名RAG 的论文──
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997)综合RAG 综述。
