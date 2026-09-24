# 文本摘要

> 抽象系统告诉你文件中所说的东西,抽象系统告诉你作者是什么意思.不同的任务,不同的陷.
> 抽取式系统告诉你文档说了什么――生成式系统告诉你作者意思――不同的任务,不同的陷――

> **【中文解读】**抽取式 VS 生成式摘要――

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation)
**Time:** ~75 minutes | **时间:** ~75 minutes


## 问题 问题引入

您需要120个词来捕捉到的新闻文章.您可以从文章中选出三个最重要的句子 (摘要) 或用您自己的词 (抽象) 重写内容.这两个称为总结.它们是完全不同的问题.
> 一篇2000字的新闻文章出现在你的信息流中――你需要120字来概括它――你可以从文章中选出最重要的三个句子 (抽取式),或者用自己的话重写内容 (生成式)――两者都叫做摘要――它们是完全不同的问题――

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――


提取总结是一个排名问题.`k`输出总是语法性的,因为它被字面上提升.
> 抽取式摘要是一个排序问题.给每个句子打分,返回排名.`k`风险是遗漏分布在整个文章中的内容.

抽象总结是一个生成问题.一个变压器产生了新的文本,根据输入条件.输出流动和压缩,但可能会幻觉到未在源头中的事实.风险是自信的制造.
> 生成式摘要是一个生成问题――转变器根据输入产生新文本――输出流并缩小,但可能产生源中没有事实幻觉――风险是自信的编制――

这一课是建立了两者,每个人都有失败模式.
> 本课构建两者,以及各自的失败模式.

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


## 概念的核心概念

![Extractive TextRank vs abstractive transformer](../assets/summarization.svg)
> ![抽取式 TextRank vs 生成式 Transformer](../assets/summarization.svg)

**Extractive.**按照文章的相关性,将文章视为一个图,其中节点是句子,边缘是相似之处. 运行页面排行 (或类似的东西) 在图上,以根据它们与其他一切的联系来评分句子.最高分的句子是总结.**TextRank**尔塞亚和塔拉乌 (2004年).
> **抽取式（Extractive）。**将文章视为图,节点是句子,边是相似度.**TextRank**们的生活方式

**Abstractive.**在文件-总结对上进行变压器编码器-解码器 (BART,T5,Pegasus) 的细调.在推断时,模型会读取文件并通过交叉注意力生成总结代币-代币.Pegasus特别使用一个空隙句子预训目标,使其在没有太多细调的情况下进行总结.
> **生成式（Abstractive）。**在文档摘要对上微调 变压器编码器解码器(BART、T5、Pegasus) 推理时,模型读取文档并通过交叉注意力对代币生成摘要。Pegasus 特别使用间隔句子预训目标,使其无需太多微调就擅长摘要。

评估与**ROUGE**红色-1和红色-2分数重叠单格和大格.红色-L分数是最长的常见次数.更高是更好,但40红色-L是"好"和50是"特殊".每篇报道都报告了三个.使用`rouge-score`包装.
> 使用 **ROUGE**评分一元组和二元组重叠――ROUGE-L 评分最长公共子序列――越高越好,但40 ROUGE-L 是"好"",50 是"出色"――每篇论文都报告全部三个――使用`rouge-score`包

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.


## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
summarize-collapse
```

## 建立它

### 步骤1:文字排行 (摘取)
> 值得注意的两件事――相似度函数使用对数归结的词重叠,这是原始的 TextRank的变体――TF-IDF 向量的余弦相似度也行――阻尼因子0.85 和代次数是 PageRank的默认值――

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

值得命名的两个东西.类似性函数使用日志正常化的词重叠,这是原始的 TextRank 变体. TF-IDF 矢量的可西因也可以运行.缓解因子 0.85 和反复数是 PageRank 默认.
> 对于其他领域 (科学论文,对话,法律),使用应对的Pegasus检查点或在目标数据上微调.

### 步骤2:使用BART抽象
> 始终使用词干提取──没有它,"running"和"run"被视为不同的词,ROUGE 会低估──

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

article = """(long news article text)"""

summary = summarizer(article, max_length=120, min_length=60, do_sample=False)
print(summary[0]["summary_text"])
```

对于其他领域 (科学论文,对话,法律),使用相应的Pegasus检查点或对目标数据进行细节调整.
> 红色已经成为主流摘要指标,但在2026年仅靠它已经不够.

### 步骤3:红色评估
> - **BERTScore**现在大多数摘要论文都与ROUGE 一起报告.
- **BARTScore**将评估视为产生的:通过预训练BART 给定源时分配给摘要的似然来评分.
- **MoverScore**摘要基准中达到顶峰,因为它比红色更好地捕获语义重叠.
- **FactCC**和**基于 QA 的事实性检查**在2021-2023年很常见,现在通常被.**G-Eval**(一种GPT-4提示链,用链式思维推理评分连贯性,一致性,流性和相关性) 替代:
- **G-Eval**和类似的LLM评委方法在评分标准设计良好时与人类判断约80%一致.

```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
scores = scorer.score(reference_summary, generated_summary)
print({k: round(v.fmeasure, 3) for k, v in scores.items()})
```

没有它,"跑"和"跑"都算是不同的词,而Rouge算是不足的.
> 生产建议:报告 ROUGE-L 用于遗留比较,BERTScore 用于语义重叠,G-Eval 用于连贯性和事实性――针对 50-100个类标签摘要校准――

### 超越红色 (2026年总结评估)
> 生成式摘要容易产生幻觉.抽取式摘要的幻觉风险较低,因为输出是从源中逐字提取的,尽管源句子被脱离下文,过时或乱序引用,它们仍然可能误导.

红色已经成为主导的总结指标二十年,但在2026年本身不足.
> 需要命名的幻觉类型:

- **BERTScore**据报道,目前,在大多数总结论文中,与ROUGE一起报告.
- **BARTScore**评估是生成的:根据预先训练的BART将总结分配给来源的可能性,评分总结.
- **MoverScore**(Earth Mover's Distance over contextual embeddings) 在2025年总结基准中达到顶点,因为它比ROUGE更好地捕捉了语义重叠.
- **FactCC**其他**QA-based faithfulness**现在经常被替换为**G-Eval**(一个GPT-4提示链,该链的结合性,一致性,流利性,与链思维推理相关性).
- **G-Eval**类似的LLM法官方法与人判断相匹配.
> - **实体替换。**源说"约翰·史密斯"――摘要说"约翰·布朗"――
- **数字漂移。**源说25,000"",摘要说2500万"",
- **极性翻转。**源说"拒绝了这个报价"――摘要说"接受了这个报价"――
- **事实编造。**源没有提到CEO.摘要说CEO批准了.

产品推:报告 ROUGE-L用于传统的比较,BERTScore用于语义重叠,G-Eval用于一致性和事实性. 根据50-100个标记的人类的总结进行校准.
> 有效的评估方法:

### 步骤4:事实性问题
> - **FactCC。**在源句和摘要句子中含关系上训练的二分类器──预测事实性/非事实性──
- **基于 QA 的事实性检查。**答案有问题. 如果摘要支持不同的答案,标记.
- **实体级 F1。**根据摘要中所述名称实体的比较,仅仅在摘要中出现的实体是可疑的.

抽象摘要容易产生幻觉.抽象摘要带来了较低的幻觉风险,因为输出从源头上字面上取出,尽管如果源句子脱文,过时或引用过后,它们仍然可以误导.这是生产系统仍然更喜欢抽取方法的原因.
> 对于事实性重要面向用户的内容 (新闻,医疗,法律,金融),抽取式更安全的默认选择.

幻类型:

- **Entity swap.**来源说"约翰·史密斯".总结说"约翰·布朗".
- **Number drift.**来源说25,000. 总结说2500万.
- **Polarity flip.**消息来源说"拒绝了这份报价".总结说"接受了这份报价".
- **Fact invention.**消息来源没有提到首席执行官. 总结说首席执行官批准了.

评估方法:

- **FactCC.**基于源句和总结句之间的关系训练的二进制分类器. 预测事实/非事实.
- **QA-based factuality.**问一个质量评估模型的问题,其答案在源头.如果总结支持不同的答案,请标记.
- **Entity-level F1.**根据本文的内容, 总结中仅有所存在的实体是可疑的.

对于任何事实性 (新闻,医疗,法律,金融) 的用户面向,抽取是安全的默认.抽象需要循环检查事实性.

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

现在,我们要做什么?
> 2026 年技术:

| Use case | Recommended |
|---------|-------------|
| News, 3-5 sentence summary, English | `facebook/bart-large-cnn` |
| Scientific papers | `google/pegasus-pubmed` or a tuned T5 |
| Multi-document, long-form | Any LLM with 32k+ context, prompted |
| Dialog summarization | `philschmid/bart-large-cnn-samsum` |
| Extractive, low hallucination risk by construction | TextRank or `sumy`'s LSA / LexRank |
> 现在,我们可以在这个地方做一些事情.
|---------|------|
| 新闻，3-5 句摘要，英语 | `facebook/bart-large-cnn` |
| 科学论文 | `google/pegasus-pubmed` 或微调的 T5 |
| 多文档，长文 | 任何 32k+ 上下文的 LLM，提示 |
| 对话摘要 | `philschmid/bart-large-cnn-samsum` |
| 抽取式，结构性低幻觉风险 | TextRank 或 `sumy` 的 LSA / LexRank |

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


长文本的LLM通常在2026年超过专业模型,当计算不是一个限制时. 折衷是成本和可复制性;专业模型提供更一致的输出.
> 长上下文 LLM通常超越专门模型――成本是成本和可复制性;专门模型提供更一致的输出――


## 运送它.

保存如`outputs/skill-summary-picker.md`其他:
> 保存为`outputs/skill-summary-picker.md`其他:

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

1. **Easy.**运行5个新闻文章的文字排名.将前3句子与参考摘要进行比较.测量ROUGE-L.你应该在CNN/DailyMail类型的文章中看到30-45 ROUGE-L.
2. **Medium.**实体级实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实实
3. **Hard.**根据CNN/DailyMail的50篇文章,比较BART-大CNN与LLM (Claude或GPT-4) 的情况.报告ROUGE-L,事实性 (按实体F1),每次总结的成本.每个获胜的文件.
> 1. **简单。**在 5 篇新闻文章上运行 文档排名.将将前3 句子与参考摘要比较.
2. **中等。**实现实体级事实性:从源和摘要中提取命名实体 (从源和摘要中提取命名实体) 空间,计算源实体在摘要中召集率和摘要实体对源的精确率――高精确率,低召集率意味着安全但简单;低精确率意味着幻觉实体――
3. **困难。**在 50篇CNN/DailyMail文章上比较BART-大CNN与LLM(Claude或GPT-4);;报告 ROUGE-L、事实性(按实体F1)和每个摘要的成本──记录各自的胜利场景──

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive | Pick sentences | Return sentences verbatim from the source. Never hallucinates. |
| Abstractive | Rewrite | Generate new text conditioned on source. Can hallucinate. |
| ROUGE | Summary metric | N-gram / LCS overlap between system output and reference. |
| TextRank | Graph-based extractive | PageRank over sentence similarity graph. |
| Factuality | Is it right | Whether summary claims are supported by the source. |
| Hallucination | Made-up content | Content in the summary that the source does not support. |
> 现在,我们在这个世界里,
|------|-----------|---------|
| 抽取式 | 选取句子 | 从源中逐字返回句子。不会幻觉。 |
| 生成式 | 重写 | 根据源生成新文本。可能幻觉。 |
| ROUGE | 摘要指标 | 系统输出与参考之间的 n-gram / LCS 重叠。 |
| TextRank | 基于图的抽取式 | 句子相似度图上的 PageRank。 |
| 事实性 | 对不对 | 摘要声明是否被源支持。 |
| 幻觉 | 编造内容 | 摘要中源不支持的内容。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/)提取法典论文.
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461)BART纸.
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777)佩加索和空白句子目标.
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/)红色纸.
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661)实况景观论文.
> - [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) 抽取式经典论文──
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461) BART 论文──
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777)   和间隔句子目标.
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/)红色论文──
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) 事实性全景论文
