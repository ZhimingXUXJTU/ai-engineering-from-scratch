# Named Entity Recognition | 命名实体识别 (NER)

> Pull the names out. Sounds easy until you deal with ambiguous boundaries, nested entities, and domain jargon.
> 把名字提取出来。听起来简单，直到你遇到模糊边界、嵌套实体和领域术语。

> **【中文解读】** 从文本中识别人名、地名、组织名等实体。是信息抽取和知识图谱的基础。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word Embeddings) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 5 · 03（词嵌入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## The Problem | 问题引入

"Apple sued Google over its iPhone search deal in the US." Five entities: Apple (ORG), Google (ORG), iPhone (PRODUCT), search deal (maybe), US (GPE). A good NER system extracts all of them with correct types. A bad one misses iPhone, confuses Apple the fruit with Apple the company, and labels "US" as a PERSON.

> "Apple sued Google over its iPhone search deal in the US." 五个实体：Apple（ORG）、Google（ORG）、iPhone（PRODUCT）、search deal（可能）、US（GPE）。一个好的 NER 系统能正确提取所有实体及其类型。一个差的系统会遗漏 iPhone，把水果 Apple 和公司 Apple 混淆，把 "US" 标记为 PERSON。

NER is the workhorse underneath every structured extraction pipeline. Resume parsing, compliance log scanning, medical record anonymization, search query understanding, grounding for chatbot responses, legal contract extraction. You never quite see it; you always depend on it.

> NER 是每个结构化抽取流水线下的工作引擎。简历解析、合规日志扫描、医疗记录匿名化、搜索查询理解、聊天机器人响应的基础、法律合同抽取。你几乎看不到它，但你总是依赖它。

This lesson walks the classical path (rule-based, HMM, CRF) into the modern one (BiLSTM-CRF, then transformers). Each step solves a specific limitation of the one before it. The pattern is the lesson.

> 本课从经典路径（基于规则、HMM、CRF）走向现代路径（BiLSTM-CRF，然后是 Transformer）。每一步都解决了前一步的特定局限。这个模式本身就是这节课的内容。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

**BIO tagging** (or BILOU) turns entity extraction into a sequence-labeling problem. Label each token with `B-TYPE` (beginning of entity), `I-TYPE` (inside entity), or `O` (outside any entity).

> **BIO 标注**（或 BILOU）将实体抽取转化为序列标注问题。给每个 token 标注 `B-TYPE`（实体开始）、`I-TYPE`（实体内部）或 `O`（不在任何实体内）。

```
Apple    B-ORG
sued     O
Google   B-ORG
over     O
its      O
iPhone   B-PRODUCT
search   O
deal     O
in       O
the      O
US       B-GPE
.        O
```

Multi-token entities chain: `New B-GPE`, `York I-GPE`, `City I-GPE`. A model that understands BIO can extract arbitrary spans.

> 多 token 实体链接：`New B-GPE`、`York I-GPE`、`City I-GPE`。理解 BIO 的模型可以提取任意跨度。

The architecture progression:

> 架构演进：

- **Rule-based.** Regex + gazetteer lookups. High precision on known entities, zero coverage on new ones.
  **基于规则。** 正则 + 地名词典查找。对已知实体精确率高，对新实体零覆盖。
- **HMM.** Hidden Markov Model. Emission probability of token given tag, transition probability of tag-to-tag. Viterbi decode. Trained on labeled data.
  **HMM。** 隐马尔可夫模型。给定标签的 token 发射概率，标签间转移概率。Viterbi 解码。在标注数据上训练。
- **CRF.** Conditional Random Field. Like HMM but discriminative, so you can mix arbitrary features (word shape, capitalization, neighboring words). Still the classical production workhorse in 2026 for low-resource deployments.
  **CRF。** 条件随机场。类似 HMM 但是判别式，所以可以混合任意特征（词形、大小写、相邻词）。到 2026 年仍是低资源部署的经典生产主力。
- **BiLSTM-CRF.** Neural features instead of hand-crafted. LSTM reads the sentence both directions, CRF layer on top enforces consistent tag sequences.
  **BiLSTM-CRF。** 神经特征代替手工特征。LSTM 双向读取句子，顶部 CRF 层强制一致的标签序列。
- **Transformer-based.** Fine-tune BERT with a token-classification head. Best accuracy. Most compute.
  **基于 Transformer。** 用 token 分类头微调 BERT。最佳准确率。最多计算量。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### Step 1: BIO tagging helpers

```python
def spans_to_bio(tokens, spans):
    labels = ["O"] * len(tokens)
    for start, end, label in spans:
        labels[start] = f"B-{label}"
        for i in range(start + 1, end):
            labels[i] = f"I-{label}"
    return labels


def bio_to_spans(tokens, labels):
    spans = []
    current = None
    for i, label in enumerate(labels):
        if label.startswith("B-"):
            if current:
                spans.append(current)
            current = (i, i + 1, label[2:])
        elif label.startswith("I-") and current and current[2] == label[2:]:
            current = (current[0], i + 1, current[2])
        else:
            if current:
                spans.append(current)
                current = None
    if current:
        spans.append(current)
    return spans
```

```python
>>> tokens = ["Apple", "sued", "Google", "over", "iPhone", "sales", "."]
>>> labels = ["B-ORG", "O", "B-ORG", "O", "B-PRODUCT", "O", "O"]
>>> bio_to_spans(tokens, labels)
[(0, 1, 'ORG'), (2, 3, 'ORG'), (4, 5, 'PRODUCT')]
```

### Step 2: hand-crafted features

For classical (non-neural) NER, features are the game. Useful ones:

> 对于经典（非神经）NER，特征是关键。有用的特征：

```python
def token_features(token, prev_token, next_token):
    return {
        "lower": token.lower(),
        "is_upper": token.isupper(),
        "is_title": token.istitle(),
        "has_digit": any(c.isdigit() for c in token),
        "suffix_3": token[-3:].lower(),
        "shape": word_shape(token),
        "prev_lower": prev_token.lower() if prev_token else "<BOS>",
        "next_lower": next_token.lower() if next_token else "<EOS>",
    }


def word_shape(word):
    out = []
    for c in word:
        if c.isupper():
            out.append("X")
        elif c.islower():
            out.append("x")
        elif c.isdigit():
            out.append("d")
        else:
            out.append(c)
    return "".join(out)
```

`word_shape("iPhone")` returns `xXxxxx`. `word_shape("USA-2024")` returns `XXX-dddd`. Capitalization patterns are high-signal for proper nouns.

> `word_shape("iPhone")` 返回 `xXxxxx`。`word_shape("USA-2024")` 返回 `XXX-dddd`。大小写模式对专有名词是高信号特征。

### Step 3: a simple rule-based + dictionary baseline

```python
ORG_GAZETTEER = {"Apple", "Google", "Microsoft", "OpenAI", "Meta", "Amazon", "Netflix"}
GPE_GAZETTEER = {"US", "USA", "UK", "India", "Germany", "France"}
PRODUCT_GAZETTEER = {"iPhone", "Android", "Windows", "ChatGPT", "Claude"}


def rule_based_ner(tokens):
    labels = []
    for token in tokens:
        if token in ORG_GAZETTEER:
            labels.append("B-ORG")
        elif token in GPE_GAZETTEER:
            labels.append("B-GPE")
        elif token in PRODUCT_GAZETTEER:
            labels.append("B-PRODUCT")
        else:
            labels.append("O")
    return labels
```

Production gazetteers have millions of entries scraped from Wikipedia and DBpedia. Coverage is good. Disambiguation (`Apple` the company vs the fruit) is terrible. That is why statistical models won.

> 生产地名词典有数百万条目，从 Wikipedia 和 DBpedia 抓取。覆盖率不错。消歧（公司 `Apple` vs 水果 `apple`）很糟糕。这就是统计模型胜出的原因。

### Step 4: the CRF step (sketch, not full impl)

Full CRF from scratch in 50 lines is not enlightening without the probability-theory foundations. Use `sklearn-crfsuite` instead:

> 没有概率论基础的情况下从零在 50 行内实现完整 CRF 并不明智。改用 `sklearn-crfsuite`：

```python
import sklearn_crfsuite

def to_features(tokens):
    out = []
    for i, tok in enumerate(tokens):
        prev = tokens[i - 1] if i > 0 else ""
        nxt = tokens[i + 1] if i + 1 < len(tokens) else ""
        out.append({
            "word.lower()": tok.lower(),
            "word.isupper()": tok.isupper(),
            "word.istitle()": tok.istitle(),
            "word.isdigit()": tok.isdigit(),
            "word.suffix3": tok[-3:].lower(),
            "word.shape": word_shape(tok),
            "prev.word.lower()": prev.lower(),
            "next.word.lower()": nxt.lower(),
            "BOS": i == 0,
            "EOS": i == len(tokens) - 1,
        })
    return out


crf = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True)
X_train = [to_features(s) for s in sentences_tokenized]
crf.fit(X_train, bio_labels_train)
```

`c1` and `c2` are L1 and L2 regularization. `all_possible_transitions=True` lets the model learn illegal sequences (e.g., `I-ORG` after `O`) are unlikely, which is how a CRF enforces BIO consistency without you writing the constraint.

> `c1` 和 `c2` 是 L1 和 L2 正则化。`all_possible_transitions=True` 让模型学习非法序列（例如 `O` 之后出现 `I-ORG`）不太可能，这就是 CRF 在你不写约束的情况下强制 BIO 一致性的方式。

### Step 5: what a BiLSTM-CRF adds

Features become learned. Inputs: token embeddings (GloVe or fastText). LSTM reads left-to-right and right-to-left. Concatenated hidden states go through a CRF output layer. The CRF still enforces tag-sequence consistency; the LSTM replaces hand-crafted features with learned ones.

> 特征变成学习得到的。输入：token 嵌入（GloVe 或 fastText）。LSTM 从左到右和从右到左读取。拼接的隐藏状态通过 CRF 输出层。CRF 仍然强制标签序列一致性；LSTM 用学习到的特征替代手工特征。

```python
import torch
import torch.nn as nn


class BiLSTM_CRF_Head(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_labels):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(hidden_dim * 2, n_labels)

    def forward(self, token_ids):
        e = self.embed(token_ids)
        h, _ = self.lstm(e)
        emissions = self.fc(h)
        return emissions
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

For the CRF layer, use `torchcrf.CRF` (pip install pytorch-crf). The gain over hand-crafted CRF is measurable but smaller than you expect unless you have tens of thousands of labeled sentences.

> CRF 层使用 `torchcrf.CRF`（pip install pytorch-crf）。相比手工 CRF 的提升是可测量的，但比你预期的小，除非你有数万标注句子。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

spaCy ships production-grade NER out of the box.

> spaCy 开箱即用提供生产级 NER。

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple sued Google over its iPhone search deal in the US.")
for ent in doc.ents:
    print(f"{ent.text:20s} {ent.label_}")
```

```
Apple                ORG
Google               ORG
iPhone               ORG
US                   GPE
```

Notice `iPhone` labeled `ORG` rather than `PRODUCT` — spaCy's small model has weak product-entity coverage. The large model (`en_core_web_lg`) does better. The transformer model (`en_core_web_trf`) does better still.

> 注意 `iPhone` 被标记为 `ORG` 而非 `PRODUCT` — spaCy 的小模型对产品实体的覆盖较弱。大模型（`en_core_web_lg`）更好。Transformer 模型（`en_core_web_trf`）更好。

Hugging Face for BERT-based NER:

> Hugging Face 的基于 BERT 的 NER：

```python
from transformers import pipeline

ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
print(ner("Apple sued Google over its iPhone in the US."))
```

```
[{'entity_group': 'ORG', 'word': 'Apple', ...},
 {'entity_group': 'ORG', 'word': 'Google', ...},
 {'entity_group': 'MISC', 'word': 'iPhone', ...},
 {'entity_group': 'LOC', 'word': 'US', ...}]
```

`aggregation_strategy="simple"` merges contiguous B-X, I-X tokens into a span. Without it, you get token-level labels and have to merge yourself.

> `aggregation_strategy="simple"` 将连续的 B-X、I-X token 合并为一个跨度。没有它，你得到 token 级别的标签，需要自己合并。

### LLM-based NER (the 2026 option)

Zero-shot and few-shot LLM NER is now competitive with fine-tuned models on many domains, and dramatically better when labeled data is scarce.

> 零样本和少样本 LLM NER 现在在许多领域上与微调模型具有竞争力，在标注数据稀缺时优势更大。

- **Zero-shot prompting.** Give the LLM a list of entity types and an example schema. Ask for JSON output. Works out of the box; accuracy is moderate on novel domains.
  **零样本提示。** 给 LLM 一个实体类型列表和示例模式。要求 JSON 输出。开箱即用；在新领域上准确率中等。
- **ZeroTuneBio-style prompting.** Decompose the task into candidate extraction → meaning explanation → judgment → re-check. A multi-stage prompt (not one-shot) lifts accuracy substantially on biomedical NER. The same pattern works for legal, financial, and scientific domains.
  **ZeroTuneBio 风格提示。** 将任务分解为候选抽取 → 含义解释 → 判断 → 复查。多阶段提示（而非一次性的）在生物医学 NER 上大幅提升准确率。同样的模式适用于法律、金融和科学领域。
- **Dynamic prompting with RAG.** Retrieve the most similar labeled examples from a small annotated seed set for every inference call; build the few-shot prompt on the fly. In 2026 benchmarks, this lifts GPT-4 biomedical NER F1 by 11-12% over static prompting.
  **动态 RAG 提示。** 每次推理调用从少量标注种子集中检索最相似的标注样本；动态构建少样本提示。在 2026 年基准测试中，这使 GPT-4 生物医学 NER F1 比静态提示提升了 11-12%。
- **Per-entity-type decomposition.** For long documents, a single call that extracts all entity types at once loses recall as length grows. Run one extraction pass per entity type. Higher inference cost, substantially higher accuracy. This is the standard pattern for clinical notes and legal contracts.
  **按实体类型分解。** 对于长文档，一次调用提取所有实体类型时，随着长度增加会丢失召回率。每种实体类型运行一次抽取。推理成本更高，但准确率显著更高。这是临床笔记和法律合同的标准模式。

Production recommendation as of 2026: start with an LLM zero-shot baseline before you collect training data. Often the F1 is good enough that you never need to fine-tune.

> 2026 年生产建议：在收集训练数据之前，先用 LLM 零样本基线开始。通常 F1 就够用了，你永远不需要微调。

### Where classical NER still wins

Even with LLMs available, classical NER wins when:

> 即使有 LLM 可用，经典 NER 在以下情况下胜出：

- Latency budget is under 50ms.
  延迟预算低于 50 毫秒。
- You have thousands of labeled examples and need 98%+ F1.
  你有数千标注样本且需要 98%+ F1。
- The domain has a stable ontology where a pretrained CRF or BiLSTM transfers well.
  领域有稳定的本体，预训练的 CRF 或 BiLSTM 迁移良好。
- Regulatory constraints require an on-prem, non-generative model.
  监管约束要求本地部署的非生成式模型。

### Where it falls apart

- **Domain shift.** CoNLL-trained NER on legal contracts performs worse than a gazetteer. Fine-tune on your domain.
  **领域偏移。** 在 CoNLL 上训练的 NER 处理法律合同时比地名词典还差。在你的领域上微调。
- **Nested entities.** "Bank of America Tower" is simultaneously an ORG and a FACILITY. Standard BIO cannot represent overlapping spans. You need nested NER (multi-pass or span-based models).
  **嵌套实体。** "Bank of America Tower" 同时是 ORG 和 FACILITY。标准 BIO 无法表示重叠跨度。你需要嵌套 NER（多遍或基于跨度的模型）。
- **Long entities.** "United States Federal Deposit Insurance Corporation." Token-level models sometimes split this. Use `aggregation_strategy` or post-process.
  **长实体。** "United States Federal Deposit Insurance Corporation。" Token 级别模型有时会拆分这个。使用 `aggregation_strategy` 或后处理。
- **Sparse types.** Medical NER labels like DRUG_BRAND, ADVERSE_EVENT, DOSE. General-purpose models have no idea. Scispacy and BioBERT are the starting points there.
  **稀疏类型。** 医疗 NER 标签如 DRUG_BRAND、ADVERSE_EVENT、DOSE。通用模型一无所知。Scispacy 和 BioBERT 是那里的起点。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

## Ship It | 产出物

Save as `outputs/skill-ner-picker.md`:

> 保存为 `outputs/skill-ner-picker.md`：

```markdown
---
name: ner-picker
description: Pick the right NER approach for a given extraction task.
version: 1.0.0
phase: 5
lesson: 06
tags: [nlp, ner, extraction]
---

Given a task description (domain, label set, language, latency, data volume), output:

1. Approach. Rule-based + gazetteer, CRF, BiLSTM-CRF, or transformer fine-tune.
2. Starting model. Name it (spaCy model ID, Hugging Face checkpoint ID, or "custom, trained from scratch").
3. Labeling strategy. BIO, BILOU, or span-based. Justify in one sentence.
4. Evaluation. Use `seqeval`. Always report entity-level F1 (not token-level).

Refuse to recommend fine-tuning a transformer for under 500 labeled examples unless the user already has a pretrained domain model. Flag nested entities as needing span-based or multi-pass models. Require a gazetteer audit if the user mentions "production scale" and labels are unchanged from CoNLL-2003.
```

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

## Exercises | 练习题

1. **Easy.** Implement `bio_to_spans` (the inverse of `spans_to_bio`) and verify round-trip consistency on 10 sentences.
   **简单。** 实现 `bio_to_spans`（`spans_to_bio` 的逆函数）并在 10 个句子上验证往返一致性。
2. **Medium.** Train the sklearn-crfsuite CRF above on the CoNLL-2003 English NER dataset. Report per-entity F1 using `seqeval`. Typical result: ~84 F1.
   **中等。** 在 CoNLL-2003 英文 NER 数据集上训练上述 sklearn-crfsuite CRF。使用 `seqeval` 报告每类 F1。典型结果：~84 F1。
3. **Hard.** Fine-tune `distilbert-base-cased` on a domain-specific NER dataset (medical, legal, or financial). Compare against the spaCy small model. Document data leakage checks and write up what surprised you.
   **困难。** 在领域特定 NER 数据集（医疗、法律或金融）上微调 `distilbert-base-cased`。与 spaCy 小模型比较。记录数据泄漏检查并写下让你惊讶的地方。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NER（命名实体识别） | Extract names / 提取名字 | Label token spans with types (PERSON, ORG, GPE, DATE, ...). / 用类型（PERSON、ORG、GPE、DATE 等）标注 token 跨度。 |
| BIO | Tagging scheme / 标注方案 | `B-X` begins, `I-X` continues, `O` outside. / `B-X` 开始，`I-X` 继续，`O` 外部。 |
| BILOU | Better BIO / 更好的 BIO | Adds `L-X` (last), `U-X` (unit) for cleaner boundaries. / 添加 `L-X`（最后）、`U-X`（单元）以获得更清晰的边界。 |
| CRF（条件随机场） | Structured classifier / 结构化分类器 | Models transitions between labels, not just emissions. Enforces valid sequences. / 对标签间的转移建模，而不仅仅是发射。强制有效序列。 |
| Nested NER（嵌套 NER） | Overlapping entities / 重叠实体 | One span is a different entity than a sub-span of it. BIO cannot express this. / 一个跨度与其子跨度是不同的实体。BIO 无法表达这一点。 |
| Entity-level F1（实体级 F1） | Proper NER metric / 正确的 NER 指标 | Predicted span must match true span exactly. Token-level F1 overstates accuracy. / 预测跨度必须与真实跨度完全匹配。Token 级 F1 会高估准确率。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## Further Reading | 延伸阅读

- [Lample et al. (2016). Neural Architectures for Named Entity Recognition](https://arxiv.org/abs/1603.01360) — the BiLSTM-CRF paper. Canonical. / BiLSTM-CRF 论文。经典。
- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805) — introduces the token-classification pattern that became standard. / 引入了成为标准的 token 分类模式。
- [spaCy linguistic features — named entities](https://spacy.io/usage/linguistic-features#named-entities) — practical reference for every attribute on `Doc.ents` and `Span`. / `Doc.ents` 和 `Span` 上每个属性的实用参考。
- [seqeval](https://github.com/chakki-works/seqeval) — the correct metric library. Use it always. / 正确的指标库。始终使用它。
