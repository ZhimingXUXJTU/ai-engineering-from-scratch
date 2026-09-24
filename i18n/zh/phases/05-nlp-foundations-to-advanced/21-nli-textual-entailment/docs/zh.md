# 文本含有 文本含有

> "t entails h"意味着人类的读数 t将得出 h 是真的. NLI 是预测含义/矛盾/中立的任务.表面上的无聊,生产中承载.
> "t 含 h"意味着人类读 t 后会推断 h 为真――NLI 是预测含/矛盾/中性的任务――表面无聊,生产中承重――

> **【中文解读】**两句之间逻辑关系: 含矛盾中性

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment Analysis), Phase 5 · 10 (Attention) | **前置知识:** Phase 5 · 05（情感分析），Phase 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

你建立了一个聊天机器人.它回答了"是的".你怎么知道"是的"是根据证据支持的?你需要按主题分类10,000个新闻文章.你有50个标记的例子.你把它变成NLI: "这个文章是关于{主题}"含义或矛盾?你需要检查生成的摘要是否忠于来源.再次NLI.

> 你建立了一个聊天机器人――它回答"是"――你怎么知道"是"有证据支持?你需要按主题分类分类 10,000 篇新闻文章――你有 50 个标签样本――你将转换为NLI:"这篇文章是关于 {主题}"含有矛盾吗?你需要检查生成的摘要是否忠于源子――又是NLI――

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

所有三个问题都归结为自然语言推理.NLI是支持事实检查,零射击分类,总结评估和检索验证的脊柱任务.每个生产RAG管道都在罩杯下运行NLI.

> 这些三个问题都归结为自然语言推理――NLI是支事实核查,零样本分类,摘要评估和检查验证的骨干任务――每个生产RAG流水线都在底层运行NLI――

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

**The task.**鉴于前提`t`假设`h`它们的关系分类为: 结合 (t 含有 h),矛盾 (t 矛盾 h),中立 (没有). 三方向分类.

> **任务。**给定条件`t`和假设`h`它们的关系分类为: 含含含 h) 矛盾矛盾 h) 中性都不是) 三分类

**Cross-encoder approach.**结t和h,通过变压器输送,分类. 用于精度关键的应用. 慢,因为你运行每个对的完整模型.

> **交叉编码器方法。**拼音 t 和 h,通过变压器,分类――用于准确率关键应用――慢因为每对运行完整模型――

**Bi-encoder approach.**单独编码t和h,比较嵌入式 (可索因相似性).快速检索,但不太准确.

> **双编码器方法。**分别编码 t 和 h,比较嵌入式的余弦相似度) 检索快但不太准确的.

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――
```figure
nli-router
```

## 建立它

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

### 步骤1:通过NLI进行零射分类

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

> **【中文解读】**本节展示了如何使用成熟框架快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

生产NLI堆:

> 生产 NLP 技术:

- **Zero-shot classification:**零样本分类:NLI模型──
- **Fact verification:**交叉编码器 NLI/ 事实验证:交叉编码器 NLI
- **Summary faithfulness:**检查每个摘要句子与源子.
- **RAG grounding:**检查获取的文本支持答案. / RAG 定:验证检索上下文支持答案──

## 运送它.

保存如`outputs/skill-nli-applications.md`其他:

> 保存为`outputs/skill-nli-applications.md`其他:

```markdown
Given a production need (fact-checking, zero-shot classification, summary evaluation), design the NLI pipeline.
1. Model choice. Cross-encoder (accuracy) or bi-encoder (speed).
2. Input format. Premise-hypothesis pairs.
3. Evaluation. Accuracy on labeled NLI datasets.
```

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题;;

## 练习题

1. **Easy.**使用`roberta-large-mnli`对于20个句子的零射击主题分类. / **简单。**使用 `roberta-large-mnli`对于20句做零样本主题分类.
2. **Medium.**通过NLI建立一个总结忠实度检查器. 在CNN/DailyMail上评估. / **中等。**用NLI 构建摘要忠诚检查器──在CNN/DailyMail上评估──
3. **Hard.**为了验证RAG答案,比较跨码器与双码器NLI. 报告速度和准确性交易. / **困难。**比较交叉编码器与双编码器 NLI 用于RAG 答案验证――报告速度和准确率权衡――

## 关键词 快速查找表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NLI（自然语言推理） | Entailment task / 蕴含任务 | Classify premise-hypothesis pairs as entailment/contradiction/neutral. / 将前提-假设对分类为蕴含/矛盾/中性。 |
| Cross-encoder（交叉编码器） | Joint encoding / 联合编码 | Encode both texts together through the full model. / 通过完整模型联合编码两个文本。 |
| Bi-encoder（双编码器） | Separate encoding / 分离编码 | Encode each text independently, compare embeddings. / 独立编码每个文本，比较嵌入。 |

## 继续阅读 继续阅读

- [Bowman et al. (2015). SNLI](https://nlp.stanford.edu/pubs/snli_paper.pdf)斯坦福的NLI数据集. /斯坦福的NLI 数据集.
- [He et al. (2021). DeBERTa v3](https://arxiv.org/abs/2111.09543)最先进的NLI模型. / 先进的NLI模型──
