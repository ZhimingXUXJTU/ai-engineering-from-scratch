# 命名实体识别 (NER)

> 听起来很容易,直到你处理模糊的边界,嵌套的实体,和域名语.
> 让名字提取出来.听起来简单,直到你遇到模糊边界.

> **【中文解读】**从文本中识别人名,地名,组织名等实体──是信息抽取和知识图谱的基础──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word Embeddings) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 5 · 03（词嵌入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

"果公司就其在美国的iPhone搜索协议起诉谷歌".五家实体:果 (ORG),谷歌 (ORG),iPhone (PRODUCT),搜索协议 (也许),美国 (GPE).一个好的NER系统将所有这些实体都用正确类型提取出来.一个坏的系统错过了iPhone,把果和果公司混为一谈,并标记"美国"为个体.

> 五个实体:果 (ORG) 、谷歌 (ORG)、iPhone (iPhone) 、产品 (iPhone)、搜索协议 (可能)、美国 (GPE) 。一个好的NER 系统能正确提取所有实体及其类型──一个差的系统会遗漏iPhone,把水果果和公司果混,把"美国"标记为个体──

简历分析,合规日志扫描,医疗记录匿名化,搜索查询理解,聊天机器人响应的基础,法律合同提取.你永远不会完全看到它;你总是依赖它.

> 简历解析,合规日志扫描,医疗记录匿名化,搜索查询理解,聊天机器人响应的基础,法律合同抽取.你几乎看不到它,但你总是依赖它.

这一课程将经典的路径 (基于规则,HMM,CRF) 走向现代的路径 (BiLSTM-CRF,然后是变压器).每个步骤解决了之前的特定限制.模式是课程.

> 本课从经典路径 (基于规则,HMM,CRF) 走向现代路径 (BiLSTM-CRF,然后是变革者) 通过每一步都解决了前一步的特定局限性.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

**BIO tagging**标签每一个代币以 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标签 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标`B-TYPE`(实体的开始),`I-TYPE`(内部实体),或`O`(任何实体以外).

> **BIO 标注**标记标记问题.`B-TYPE`现在,我还在做什么?`I-TYPE`实体内部`O`(不在任何实体内)

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

多代币实体链: `New B-GPE`现在`York I-GPE`现在`City I-GPE`了解生物的模型可以提取任意的跨度.

> 多代币 实体链接:`New B-GPE`,我知道.`York I-GPE`,我知道.`City I-GPE`△理解BIO的模型可以提取任意跨度.

建筑发展:

> 架构演进:

- **Rule-based.**已知实体的高精度,新实体的覆盖率为零.
  **基于规则。**正则 + 地名词典查找──对已知实体精确率高,对新实体零覆盖──
- **HMM.**隐藏的马科夫模型,给定的标签的发射概率,标签到标签的过渡概率,维特比解码,训练用标签数据.
  **HMM。**隐马尔可夫模型――给定标签的代币 发射概率,标签间转移概率――Viterbi 解码――在标签数据上训练――
- **CRF.**条件随机场.像HMM,但有歧视性,所以你可以混合任意的特征 (字形,字母,邻近的词).仍然是2026年低资源部署的经典生产工作马.
  **CRF。**条件随机场──类似于HMM,但判别式,所以可以混合任意特征──词形、大小写、相邻词)──到2026年仍是低资源部署的经典生产主力──
- **BiLSTM-CRF.**系统读取句子两方向,CRF层在上面执行一致的标签序列.
  **BiLSTM-CRF。**神经特征代替手工特征――LSTM 双向读取句子,顶部CRF层强制一致的标签序列――
- **Transformer-based.**精细调节BERT,具有代币分类头,最准确,最计算.
  **基于 Transformer。**用标志 分类微调BERT──最佳准确率──最多计算量──

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
ner-bio-tagging
```

## 建立它

### 步骤1:生物标签助手

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

### 步骤2:手工制作的特征

对于经典 (非神经) NER,功能是游戏. 有用的是:

> 对于经典的特征是关键的.

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

`word_shape("iPhone")`收益`xXxxxx`现在,我们要去.`word_shape("USA-2024")`收益`XXX-dddd`资本化模式对正确名词具有高信号.

> `word_shape("iPhone")`返回`xXxxxx`,我知道.`word_shape("USA-2024")`返回`XXX-dddd`小写模式对专名词是高信号特征

### 步骤3:基于简单的规则+字典基础

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

制作报纸上有数百万条文章从维基百科和DBpedia中摘录.`Apple`由于这些问题,我们必须要做出一些决定.

> 生产地名词典有数百万条目,从维基百科 和 DBpedia 抓取──覆盖率不错──消歧(公司 `Apple`果`apple`这就是统计模型的胜利原因.

### 步骤4:CRF步骤 (草图,不是完整的插入)

没有概率理论的基础,就不会有启发.`sklearn-crfsuite`换取之而言:

> 没有概率论基础的情况下从零到50行内实现完整的CRF并不明智.`sklearn-crfsuite`其他:

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

`c1`其他`c2`         `all_possible_transitions=True`模型可以学习非法序列 (例如,`I-ORG`之后`O`) 很不可能,这就是CRF如何在没有你写下限制的情况下强制生物一致性.

> `c1`和 `c2`是 L1 和 L2 正则化.`all_possible_transitions=True`让模型学习非法序列`O`之后出现`I-ORG`没有可能,这是CRF在你不写约束的情况下强制BIO的单致性方式.

### 步骤5: BiLSTM-CRF所增加的内容

功能变得学习.输入:代号嵌入 (GloVe或快文).LSTM读左到右和右到左. 连接隐藏状态通过CRF输出层.CRF仍然强制标签序列一致性;LSTM取代手工制造的功能与学习.

> 拼接的隐藏状态通过CRF 输出层――CRF 仍然强制标签序列一致性;LSTM 用到的特征替代手工特征――

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

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

对于CRF层,使用`torchcrf.CRF`虽然手工CRF的效益是可测量的,但比你预期的小,除非你有数万个标记的句子.

>  CRF 层使用`torchcrf.CRF`虽然这项技术的发展是可测量的,但你预期的小幅,除非你有数万个标注句子.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

产品级NER的 spaCy 运输出了盒子.

> 开箱即用提供生产级 NER.

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

注意`iPhone`标记`ORG`而不是`PRODUCT` spaCy的小型模型产品实体覆盖率较低.`en_core_web_lg`变压器模型 (`en_core_web_trf`) 情况更好.

> 注意`iPhone`被标记为`ORG`而不是`PRODUCT`空间的小模型对产品实体的覆盖较弱――大模型(`en_core_web_lg`变压器模型`en_core_web_trf`现在,我还在做.

基于BERT的NER的拥抱面孔:

> 基于BERT的NER的拥抱脸:

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

`aggregation_strategy="simple"`没有它,你就会得到代币级别的标签,

> `aggregation_strategy="simple"`没有它,你得到了标签级别的标签,需要自己合并.

### 基于LLM的NER (2026期选项)

零射和少射的LLM NER现在与许多领域的细节调整模型竞争,

> 零样本和少样本 LLM NER 现在在许多领域与微调模型具有竞争力,在标记数据稀缺时优势更大.

- **Zero-shot prompting.**给LLM一个实体类型的列表和一个示例方案. 请求JSON输出. 工作出盒子;在新领域的准确度是中等的.
  **零样本提示。**给LLM一个实体类型列表和示例模式――要求JSON输出――开箱即用;在新领域准确率中等――
- **ZeroTuneBio-style prompting.**解散任务成候选人提取 → 解释 → 判断 → 重复检查.多阶段提示 (而不是一次性) 显著提高了生物医学NER的准确性.同样的模式适用于法律,金融和科学领域.
  **ZeroTuneBio 风格提示。**将任务分解为候选抽取 → 含义解释 → 判断 → 复查――多阶段提示(而不是一次性) 在生物医学NER上大幅提升准确率――同样的模式适用于法律、金融和科学领域――
- **Dynamic prompting with RAG.**检索每次推断调用的小注释种子集合中最类似的标签示例;在飞行中构建几次调用提示.在2026年基准中,这将GPT-4生物医学NER F1提高11-12%于静态调用提示.
  **动态 RAG 提示。**每次推理调用从少量标签种子集中检查最相似的标签样本;动态构建少样本提示――在2026年基准测试中,这使得GPT-4生物医学NER F1比静态提示提高了11-12%.
- **Per-entity-type decomposition.**对于长文件,一个单次调用,同时提取所有实体类型,随着长度的增加而失去回忆. 每个实体类型运行一个提取通行. 推断成本更高,准确度更高. 这是临床笔记和法律合同的标准模式.
  **按实体类型分解。**对于长文档,一次调用提取所有实体类型时,随着长度的增加会丢失召回率.

根据2026年开始的生产建议:在收集训练数据之前,开始从LLM零射击基线开始.

> 2026年生产建议:在收集训练数据之前,先使用LLM 零样本基线开始.

### 传统的NER仍然在胜利

即使有LLM,经典的NER在:

> 即使有LLM可用,经典NER在以下情况下胜出:

- 延迟预算低于50ms.
  延迟预算低于50毫秒.
- 你有数千个标记的例子,需要98%+F1.
  你有数千个标签样本,需要98%+F1
- 该域具有稳定的定性,预训练的CRF或BiLSTM转移良好.
  领域有稳定的本体,预训练的CRF或BiLSTM 迁移良好.
- 监管限制要求实地进行非创建模式.
  监管约束要求本地部署的非生成式模型.

### 在它崩的地方

- **Domain shift.**法律合同的NER比报纸员更差.
  **领域偏移。**在 CoNLL 上训练的NER 处理法律合同同时比地名词典还差.
- **Nested entities.**美国银行塔同时是ORG和FASILITY.标准BIO不能代表重叠跨度.你需要嵌套NER (多通或跨度模型).
  **嵌套实体。**美国银行塔同时是ORG 和 FACILITY――标准BIO 无法表示重叠跨度――你需要嵌套NER(多遍或基于跨度的模型)
- **Long entities.**美国联邦存款保险公司的代币级别模型有时会分开这个.`aggregation_strategy`或是后处理.
  **长实体。**美国联邦存款保险公司的代币类型模型有时会被拆除.`aggregation_strategy`或后处理.
- **Sparse types.**医疗NER标签如Drug_Brand,ADVERSE_EVENT,DOSE.一般用途模型没有任何想法.Scispacy和BioBERT是此起点.
  **稀疏类型。**医疗 NER 标签如Drug_BRAND、ADVERSE_EVENT、DOSE──通用模型一无所知──Scispacy 和 BioBERT 是那里的起点──

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

## 运送它.

保存如`outputs/skill-ner-picker.md`其他:

> 保存为`outputs/skill-ner-picker.md`其他:

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

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 练习题

1. **Easy.**实施`bio_to_spans`(反向的`spans_to_bio`) 并通过10句检查回路一致性.
   **简单。**实现`bio_to_spans`(`spans_to_bio`逆函数) 在10个句子上验证往返一致性.
2. **Medium.**训练上述 sklearn-crfsuite CRF在CoNLL-2003英语NER数据集上.`seqeval`典型结果: ~ 84 F1.
   **中等。**在 CoNLL-2003 英文 NER 数据集上训练上述 sklearn-crfsuite CRF──使用 `seqeval`报告每类F1――典型结果:~84 F1――
3. **Hard.**精细调节`distilbert-base-cased`根据该数据库的数据库,您可以在一个特定领域的NER数据集 (医疗,法律或金融) 上进行比较.
   **困难。**在特定领域的NER数据集 (医疗,法律或金融) 上调`distilbert-base-cased`◎与空间小模型比较──记录数据泄漏检查并写下让你惊的地方──

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 关键词 快速查找表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NER（命名实体识别） | Extract names / 提取名字 | Label token spans with types (PERSON, ORG, GPE, DATE, ...). / 用类型（PERSON、ORG、GPE、DATE 等）标注 token 跨度。 |
| BIO | Tagging scheme / 标注方案 | `B-X` begins, `I-X` continues, `O` outside. / `B-X` 开始，`I-X` 继续，`O` 外部。 |
| BILOU | Better BIO / 更好的 BIO | Adds `L-X` (last), `U-X` (unit) for cleaner boundaries. / 添加 `L-X`（最后）、`U-X`（单元）以获得更清晰的边界。 |
| CRF（条件随机场） | Structured classifier / 结构化分类器 | Models transitions between labels, not just emissions. Enforces valid sequences. / 对标签间的转移建模，而不仅仅是发射。强制有效序列。 |
| Nested NER（嵌套 NER） | Overlapping entities / 重叠实体 | One span is a different entity than a sub-span of it. BIO cannot express this. / 一个跨度与其子跨度是不同的实体。BIO 无法表达这一点。 |
| Entity-level F1（实体级 F1） | Proper NER metric / 正确的 NER 指标 | Predicted span must match true span exactly. Token-level F1 overstates accuracy. / 预测跨度必须与真实跨度完全匹配。Token 级 F1 会高估准确率。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.

## 继续阅读 继续阅读

- [Lample et al. (2016). Neural Architectures for Named Entity Recognition](https://arxiv.org/abs/1603.01360) BiLSTM-CRF论文. 经典. / BiLSTM-CRF论文──经典──
- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805)引入了成为标准的代币分类模式.
- [spaCy linguistic features — named entities](https://spacy.io/usage/linguistic-features#named-entities) 关于每一个属性的实际参考`Doc.ents`其他`Span`现在,我们要去.`Doc.ents`和 `Span`任何属性的实用参考.
- [seqeval](https://github.com/chakki-works/seqeval)正确的计量库. 始终使用它. / 正确的指标库.
