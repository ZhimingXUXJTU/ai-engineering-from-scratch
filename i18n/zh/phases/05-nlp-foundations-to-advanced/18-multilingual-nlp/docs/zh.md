# 多语言的NLP

> 一个模型,100多种语言,大多数语言的训练数据是零的.
> 一个模型,100+种语言,大多数语言零训练数据――跨语言迁移是2020年代的实用奇迹――

> **【中文解读】**多语言BERT、XLM-R等模型处理多种语言──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 04 (GloVe, FastText, Subword), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 04（GloVe、FastText、子词），Phase 5 · 11（机器翻译）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

英语有数十亿个标签的例子.乌尔都有数千个.马提利几乎没有任何一个.任何为全球观众服务的实用NLP系统都必须在没有任务特定培训数据的长尾语言上工作.

> 英语有数十亿标签样本.乌尔都语有数千种.

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

多语言模型通过同时训练一个模型在多种语言来解决这一问题. 共同的代表性使得模型能够将高资源语言中学习的技能转移到低资源语言中. 通过英语情感分析进行细节调整, 这就是零射击跨语言传输,它已经改变了NLP如何传递到世界.

> 多语言模型通过同时在许多语言上训练一个模型来解决这个问题.共享表示让模型将高资源语言学到的技能转移到低资源语言. 在英语情感分析中微调模型,它可以对乌尔都语产生令人惊的良好情感预测.

这一课列出了交易,规范模式,以及一个决定,

> 本课标名为权衡"",经典模型"",困扰多语言工作新手团队的决策:选择迁移的源语言.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

![Cross-lingual transfer via shared multilingual embedding space](../assets/multilingual.svg)

**Shared vocabulary.**多语言模型使用了从所有目标语言中训练的SentencePiece或WordPiece标记器.词汇库是共享的:相同的子词单元在相关语言中代表着相同的形态. `anti-`在英语和意大利语中,得到了相同的代币.

> **共享词表。**多语言模型使用在所有目标语言文本上训练的句子片或 WordPiece 分词器──词表是共享的:相同的子词单元在相关语言中表示相同的语素──英语和意大利语的`anti-`获得相同的标志.

**Shared representation.**通过面具语言模拟,在许多语言中预先训练的变压器学会了不同语言中的语义相似句子产生类似的隐藏状态. mBERT,XLM-R和NLLB都显示出这一点.英语中的"猫"嵌入式集群在法语的"聊天"和西班牙语的"gato"附近,以及全句嵌入式.

> **共享表示。**在多种语言的掩码语言建模上预训练的变革者学到不同语言中语义相似的句子产生相似的隐藏状态.

**Zero-shot transfer.**根据一个语言 (通常是英语) 的标签数据进行细节调整.在推断时,运行在模型支持的任何其他语言上.不需要标签目标语言.对类型相关语言来说,结果是强的,对于远方语言来说是弱的.

> **零样本迁移。**在一种语言 (通常是英语) 的标签数据上微调模型. 在推理时,在任何其他语言上运行.

**Few-shot fine-tuning.**添加100-500个标记的例子. 准确度在分类任务上跳到英语基线的95-98%.这是多语言NLP中最具成本效益的单一杆.

> **少样本微调。**在目标语言中增加100-500个标记样本. 在分类任务中准确率升至英语基线的95-98%.

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 模型的模型

| Model / 模型 | Year / 年份 | Coverage / 覆盖 | Notes / 说明 |
|-------|------|----------|-------|
| mBERT | 2018 | 104 languages / 104 种语言 | Trained on Wikipedia. First practical multilingual LM. Weak on low-resource. / 在 Wikipedia 上训练。首个实用多语言 LM。低资源语言较弱。 |
| XLM-R | 2019 | 100 languages / 100 种语言 | Trained on CommonCrawl. Sets the cross-lingual baseline. / 在 CommonCrawl 上训练。设定跨语言基线。 |
| XLM-V | 2023 | 100 languages / 100 种语言 | XLM-R with 1M-token vocabulary. Better on low-resource. / XLM-R 配 1M token 词表。低资源更好。 |
| mT5 | 2020 | 101 languages / 101 种语言 | T5 architecture for multilingual generation. / T5 架构用于多语言生成。 |
| NLLB-200 | 2022 | 200 languages / 200 种语言 | Meta's translation model; includes 55 low-resource languages. / Meta 翻译模型；含 55 种低资源语言。 |
| BLOOM | 2022 | 46 languages + 13 programming / 46 种语言 + 13 种编程语言 | Open 176B LLM trained multilingually. / 开源 176B 多语言 LLM。 |
| Aya-23 | 2024 | 23 languages / 23 种语言 | Cohere's multilingual LLM. Strong on Arabic, Hindi, Swahili. / Cohere 多语言 LLM。阿拉伯语、印地语、斯瓦希里语强。 |

根据使用情况选择. 类别与XLM-R-base作为正常默认功能很好. 代代任务需要mT5或NLLB,取决于翻译与开放代代. 基于Aya-23或Claude的LLM类型工作对,使用明确的多语言提示.

> 按例选择――分类任务以XLM-R为基础 作为合理默认――生成任务根据翻译对开放生成选择 mT5或NLLB――LLM 风格工作配合 Aya-23或Claude 使用显式多语言提示――

## 源语言决策 (研究)

据悉,在2026年,英国的研究人员发现,英语是最好的调整源.

> 大多数团队默认以英语作为微调源. 最新研究 (最新研究) 表明,这通常是错误的.

语言相似性预测传输质量比原材料大小更好.对于斯拉夫人目标,德国或俄罗斯人通常超过英语.对于印第安人目标,印度语通常超过英语.**qWALS**根据世界语言结构图表的2026年,**LANGRANK**(Lin et al., ACL 2019) 是一种单独的早期方法,从语言相似性,体积和遗传相关性组合中排名候选源语言.

> 语言相似性比原始语料大小更好地预测迁移质量――对于斯拉夫语目标,德语或俄语通常胜英语――对于印度语目标,印地语通常胜英语――**qWALS**像性度量 (相似性度量)**LANGRANK**语言相似性,语料大小和遗传关系组合中排名候选源语言.

实际规则:如果你的目标语言具有典型的近距离高资源的亲戚,

> 实用规则:如果你的目标语言具有近乎高资源亲属的类型,

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
n5-crosslingual-bridge
```

## 建立它

### 阶段1:零截图跨语言分类

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli")
model = AutoModelForSequenceClassification.from_pretrained("joeddav/xlm-roberta-large-xnli")


def classify(text, candidate_labels, hypothesis_template="This text is about {}."):
    scores = {}
    for label in candidate_labels:
        hypothesis = hypothesis_template.format(label)
        inputs = tok(text, hypothesis, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits[0]
        entail_score = torch.softmax(logits, dim=-1)[2].item()
        scores[label] = entail_score
    return dict(sorted(scores.items(), key=lambda x: -x[1]))


print(classify("I love this product!", ["positive", "negative", "neutral"]))
print(classify("मुझे यह उत्पाद पसंद है!", ["positive", "negative", "neutral"]))
print(classify("J'adore ce produit !", ["positive", "negative", "neutral"]))
```

基于NLI训练的XLM-R通过"结"技巧将数据转移到分类.

> 通过含技巧很好地迁移到分类.

### 步骤2:多语言嵌入空间

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

pairs = [
    ("The cat is sleeping.", "Le chat dort."),
    ("The cat is sleeping.", "El gato está durmiendo."),
    ("The cat is sleeping.", "Die Katze schläft."),
    ("The cat is sleeping.", "The dog is barking."),
]

for eng, other in pairs:
    emb_eng = model.encode([eng], normalize_embeddings=True)[0]
    emb_other = model.encode([other], normalize_embeddings=True)[0]
    sim = float(np.dot(emb_eng, emb_other))
    print(f"  {eng!r} <-> {other!r}: cos={sim:.3f}")
```

翻译在嵌入空间中接近. 另一个英语句子在更远的地方. 这就是使跨语言检索,集群和相似性工作的原因.

> 翻译在嵌入空间中距离很近.不同英语句子距离更远. 这就是跨语言检查,聚类和相似度工作的基础.

### 步骤3:少量调整策略

```python
from transformers import TrainingArguments, Trainer
from datasets import Dataset


def few_shot_finetune(base_model, base_tokenizer, examples):
    ds = Dataset.from_list(examples)

    def tokenize_fn(ex):
        out = base_tokenizer(ex["text"], truncation=True, max_length=128)
        out["labels"] = ex["label"]
        return out

    ds = ds.map(tokenize_fn)
    args = TrainingArguments(
        output_dir="out",
        per_device_train_batch_size=8,
        num_train_epochs=5,
        learning_rate=2e-5,
        save_strategy="no",
    )
    trainer = Trainer(model=base_model, args=args, train_dataset=ds)
    trainer.train()
    return base_model
```

对于100-500个目标语言的例子,`num_train_epochs=5`其他`learning_rate=2e-5`提高学习率会导致多语言的调整崩,

> 对于100-500个目标语言样本,`num_train_epochs=5`和 `learning_rate=2e-5`更多语言的学习率会导致多语言的崩,你得到一个仅限于英语的模型.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 实际上是有效的评估.

- **Per-language accuracy on held-out sets.**总结不合,总结隐藏着长尾.
  **每种语言在留出集上的准确率。**不要聚聚.聚聚会藏长尾.
- **Benchmark against monolingual baseline.**在具有足够数据的语言中,从零开始训练的单语言模型有时比多语言模型更好.
  **与单语基线比较。**对于有足够的数据的语言,从头训练的单语模型有时胜过多语言模型――测试――
- **Entity-level tests.**标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签:
  **实体级测试。**目标语言中的命名实体――多语言模型对远离拉丁文的书写分词通常较弱――
- **Cross-lingual consistency.**两个语言的含义应该产生相同的预测.
  **跨语言一致性。**两种语言中相同的含义应产生相同的预测――测量差距――

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

## 用它实现框架

现在,我们要做什么?

> 2026 年技术:

| Task / 任务 | Recommended / 推荐 |
|-----|-------------|
| Classification, 100 languages / 分类，100 种语言 | XLM-R-base (~270M) fine-tuned / 微调 |
| Zero-shot text classification / 零样本文本分类 | `joeddav/xlm-roberta-large-xnli` |
| Multilingual sentence embeddings / 多语言句子嵌入 | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Translation, 200 languages / 翻译，200 种语言 | `facebook/nllb-200-distilled-600M` |
| Generative multilingual / 生成式多语言 | Claude, GPT-4, Aya-23, mT5-XXL |
| Low-resource language NLP / 低资源语言 NLP | XLM-V or domain-specific fine-tune / XLM-V 或领域微调 |

总是预算调整目标语言,如果表现有意义.零射击是起点,而不是最终答案.

> 如果性能很重要,总是为目标语言的微调预留预算.

### 代币化税

多语言模型在所有语言中都具有一个代码符号.该词汇是由英语,法语,西班牙语,中国,德国主导的组成部分训练.对于任何语言以外的主导组,三个税收都默默地组合:

> 多语言模型在所有语言间共享一个分词器.该词表在英语,法语,西班牙语,中文,德语主导语料上训练.

- **Fertility tax.**低资源语言文本每字的代码比英语要多得多. 印度语句可能需要相当于英语句的代码的3-5倍.
  **繁殖税。**低资源语言文本每一个词分词成比英语更多的代币――一个印地语句可能需要等价英语句的3-5倍的代币――
- **Variant recovery tax.**每个字体错误,二重变体,Unicode规范不匹配或案例变化都会成为嵌入空间中的冷启动无关的序列.
  **变体恢复税。**每个拼写错误,变音符变体,Unicode 归结不匹配或大小写变都变成嵌入空间中的冷启动无关序列.
- **Capacity spillover tax.**税收1和2消耗了背景位置,层深度和嵌入维度.实际推理所剩下的东西系统较小.
  **容量溢出税。**税 1 和 2 消耗下文位置,层深度和嵌入维度.

实际症状:你的模型通常以印度语进行训练,损失曲线看起来正确,评估困难看起来合理,**You cannot data-scale your way out of a broken tokenizer.**

> 实际症状:模型在印地语上训练正常,损失曲线正确,评估困惑度合理,但生产输出微妙地出错.**你无法通过数据扩展来修复损坏的分词器。**

减轻:选择一个对目标语言有良好的代币化器;验证已保留的目标文本的代币化生育能力;对真正长尾脚本使用字节级的反弹.

> 缓解措施:选择对目标语言覆盖良好的分词器;在留出的目标文本上验证分词繁殖率;对真正的长尾书写使用字节级回归――

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

## 运送它.

保存如`outputs/skill-multilingual-picker.md`其他:

> 保存为`outputs/skill-multilingual-picker.md`其他:

```markdown
---
name: multilingual-picker
description: Pick source language, target model, and evaluation plan for a multilingual NLP task.
version: 1.0.0
phase: 5
lesson: 18
tags: [nlp, multilingual, cross-lingual]
---

Given requirements (target languages, task type, available labeled data per language), output:

1. Source language for fine-tuning. Default English; check LANGRANK or qWALS if target language has a typologically close high-resource language.
2. Base model. XLM-R (classification), mT5 (generation), NLLB (translation), Aya-23 (generative LLM).
3. Few-shot budget. Start with 100-500 target-language examples if available.
4. Evaluation plan. Per-language accuracy, cross-lingual consistency, entity-level F1 on non-Latin scripts.

Refuse to ship a multilingual model without per-language evaluation. Flag scripts with low tokenization coverage as needing byte-fallback.
```

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 练习题

1. **Easy.**运行零射击分类管道,每种语言每句10句,包括英语,法语,印度语和阿拉伯语.
   **简单。**在英语,法语,印地语和阿拉伯语运行零样本分类流水线,每种语言10句――报告准确率――
2. **Medium.**使用`paraphrase-multilingual-MiniLM-L12-v2`通过使用不同语言的语言,建立一个跨语言检索器.
   **中等。**构建跨语言检索器──用英语查询,检索任何语言的文档──测量回忆@5──
3. **Hard.**为了完成一个印度语分类任务,比较英语源和印度语源细节调整. 报告哪个来源产生更好的印度语准确性.这是缩写中的LANGRANK论文.
   **困难。**报告中哪个来源产生更好的准确率.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 关键词 快速查找表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Multilingual model（多语言模型） | One model, many languages / 一个模型多种语言 | Shared vocabulary and parameters across languages. / 跨语言共享词表和参数。 |
| Cross-lingual transfer（跨语言迁移） | Train on one, run on another / 训练一种，运行另一种 | Fine-tune on source, evaluate on target without target labels. / 在源语言微调，在目标语言评估。 |
| Zero-shot（零样本） | No target labels / 无目标标签 | Transfer without target-language fine-tuning. / 无目标语言微调的迁移。 |
| Few-shot（少样本） | Small target labels / 少量目标标签 | 100-500 target-language examples for fine-tuning. / 100-500 个目标语言样本。 |
| mBERT | First multilingual LM / 首个多语言 LM | 104-language BERT on Wikipedia. / 104 语言 BERT。 |
| XLM-R | Cross-lingual baseline / 跨语言基线 | 100-language RoBERTa on CommonCrawl. / 100 语言 RoBERTa。 |
| NLLB | 200-language MT / 200 语言 MT | No Language Left Behind. 55 low-resource languages. / 不让任何语言掉队。55 种低资源语言。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.

## 继续阅读 继续阅读

- [Conneau et al. (2019). XLM-R](https://arxiv.org/abs/1911.02116)XLM-R论文. /XLM-R论文.
- [Pires et al. (2019). How Multilingual is Multilingual BERT?](https://arxiv.org/abs/1906.01502)跨语言迁移分析.
- [Costa-jussà et al. (2022). No Language Left Behind](https://arxiv.org/abs/2207.04672) NLLB-200. / NLLB-200 论文。
- [Üstün et al. (2024). Aya Model](https://arxiv.org/abs/2402.07827)Cohere的多语言法学士.
- [Language Similarity Predicts Cross-Lingual Transfer (2026)](https://www.mdpi.com/2504-4990/8/3/65) QWALS / 语言论文. / qWALS / 语言论文──
