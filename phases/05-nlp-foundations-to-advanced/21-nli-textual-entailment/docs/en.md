# Natural Language Inference — Textual Entailment | 自然语言推理 — 文本蕴含

> "t entails h" means a human reading t would conclude h is true. NLI is the task of predicting entailment / contradiction / neutral. Boring on the surface, load-bearing in production.
> "t 蕴含 h" 意味着人类读 t 后会推断 h 为真。NLI 是预测蕴含/矛盾/中性的任务。表面无聊，生产中承重。

> **【中文解读】** NLI 判断两个句子之间的逻辑关系：蕴含、矛盾、中性。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment Analysis), Phase 5 · 10 (Attention) | **前置知识:** Phase 5 · 05（情感分析），Phase 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

You built a chatbot. It answered "yes." How do you know that "yes" is supported by the evidence? You need to classify 10,000 news articles by topic. You have 50 labeled examples. You turn it into NLI: "this article is about {topic}" — entailment or contradiction? You need to check if a generated summary is faithful to the source. NLI again.

> 你建了一个聊天机器人。它回答 "yes"。你怎么知道 "yes" 有证据支持？你需要按主题分类 10,000 篇新闻文章。你有 50 个标注样本。你将其转化为 NLI："这篇文章是关于 {topic}"——蕴含还是矛盾？你需要检查生成的摘要是否忠实于源。又是 NLI。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

All three problems reduce to Natural Language Inference. NLI is the backbone task that supports fact-checking, zero-shot classification, summarization evaluation, and retrieval verification. Every production RAG pipeline runs NLI under the hood.

> 这三个问题都归结为自然语言推理。NLI 是支撑事实核查、零样本分类、摘要评估和检索验证的骨干任务。每个生产 RAG 流水线都在底层运行 NLI。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

**The task.** Given premise `t` and hypothesis `h`, classify their relationship as one of: Entailment (t implies h), Contradiction (t contradicts h), Neutral (neither). Three-way classification.

> **任务。** 给定前提 `t` 和假设 `h`，将它们的关系分类为：蕴含（t 蕴含 h）、矛盾（t 矛盾 h）、中性（都不是）。三分类。

**Cross-encoder approach.** Concatenate t and h, feed through a transformer, classify. Used for accuracy-critical applications. Slow because you run the full model for each pair.

> **交叉编码器方法。** 拼接 t 和 h，通过 Transformer，分类。用于准确率关键的应用。慢因为每对运行完整模型。

**Bi-encoder approach.** Encode t and h separately, compare embeddings (cosine similarity). Fast for retrieval but less accurate.

> **双编码器方法。** 分别编码 t 和 h，比较嵌入（余弦相似度）。检索快但不太准确。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### Step 1: zero-shot classification via NLI

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("roberta-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli")

def nli_classify(premise, hypothesis):
    inputs = tok(premise, hypothesis, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits[0]
    # 0=contradiction, 1=neutral, 2=entailment
    probs = torch.softmax(logits, dim=-1)
    labels = ["contradiction", "neutral", "entailment"]
    return {labels[i]: probs[i].item() for i in range(3)}

print(nli_classify("A man is playing guitar.", "Someone is making music."))
```

> **【中文解读】** 本节展示如何用成熟框架快速应用该技术。在实际项目中，优先使用经过验证的框架实现。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

The production NLI stack:

> 生产 NLP 技术栈：

- **Zero-shot classification:** NLI models (DeBERTa-v3-large-mnli). / 零样本分类：NLI 模型。
- **Fact verification:** Cross-encoder NLI on claim vs evidence. / 事实验证：交叉编码器 NLI。
- **Summary faithfulness:** Check each summary sentence against source. / 摘要忠实度：检查每个摘要句子与源。
- **RAG grounding:** Verify retrieved context supports the answer. / RAG 锚定：验证检索上下文支持答案。

## Ship It | 产出物

Save as `outputs/skill-nli-applications.md`:

> 保存为 `outputs/skill-nli-applications.md`：

```markdown
Given a production need (fact-checking, zero-shot classification, summary evaluation), design the NLI pipeline.
1. Model choice. Cross-encoder (accuracy) or bi-encoder (speed).
2. Input format. Premise-hypothesis pairs.
3. Evaluation. Accuracy on labeled NLI datasets.
```

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目。

## Exercises | 练习题

1. **Easy.** Use `roberta-large-mnli` for zero-shot topic classification on 20 sentences. / **简单。** 使用 `roberta-large-mnli` 对 20 句话做零样本主题分类。
2. **Medium.** Build a summary faithfulness checker using NLI. Evaluate on CNN/DailyMail. / **中等。** 用 NLI 构建摘要忠实度检查器。在 CNN/DailyMail 上评估。
3. **Hard.** Compare cross-encoder vs bi-encoder NLI for RAG answer verification. Report speed and accuracy tradeoffs. / **困难。** 比较交叉编码器与双编码器 NLI 用于 RAG 答案验证。报告速度和准确率权衡。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NLI（自然语言推理） | Entailment task / 蕴含任务 | Classify premise-hypothesis pairs as entailment/contradiction/neutral. / 将前提-假设对分类为蕴含/矛盾/中性。 |
| Cross-encoder（交叉编码器） | Joint encoding / 联合编码 | Encode both texts together through the full model. / 通过完整模型联合编码两个文本。 |
| Bi-encoder（双编码器） | Separate encoding / 分离编码 | Encode each text independently, compare embeddings. / 独立编码每个文本，比较嵌入。 |

## Further Reading | 延伸阅读

- [Bowman et al. (2015). SNLI](https://nlp.stanford.edu/pubs/snli_paper.pdf) — the Stanford NLI dataset. / Stanford NLI 数据集。
- [He et al. (2021). DeBERTa v3](https://arxiv.org/abs/2111.09543) — state-of-the-art NLI model. / 先进 NLI 模型。
