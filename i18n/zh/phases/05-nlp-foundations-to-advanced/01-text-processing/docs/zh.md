# 文字处理 标记化,表决,化,化.

> 语言是连续的,模型是离散的,预处理是桥梁.
> 语言是连续的.模型是离散的.预处理是两者之间的桥梁.

> **【中文解读】**分词是NLP的第一步:把连续文本切成离散代币――包括词干提取和词形回原――在LLM时代,分词由BPE等子词分词器处理――

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 学习目标

- 了解代币化,源和化作为不同的预处理操作
  理解分词、词干提取和词形还原作为不同的预处理操作
- 建立一个Regex代币器,一个 Porter stemmer步骤,和一个基于搜索的 lemmatizer从零开始
  从零构建正则分词器、波特词干提取步骤和基于查找表的词形回原器
- 对于生产预加工管道来说,比较NLTK和spaCy
  与NLTK和SpaceCy在生产预处理流水线中的优势
- 识别最常见的两种生产故障:可复制性漂移和火车/线程不匹配
  识别两种最常见的生产故障:可复现性漂移和训练/推理不匹配

## 问题 问题引入

模型不能读"猫们跑了". 它读完整数.

> 模型不能直接读取"猫们跑了".

每个NLP系统都以相同的三个问题开启.一个词从哪里开始.这个词的根源是什么?我们如何把"跑","跑","跑"当它帮助的时候,当它帮助的时候,当它帮助的时候,当它帮助的时候,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它帮助时,当它对待时,当它帮助时,当它对待时,当它对待时,当它对待时,当它对它对它有所帮助时,当它对它对它对它有所帮助时,当它对它对它对它对它有不同的影响时,当它对它对它对它对它对它对它对它有所影响.

> 每个NLP系统都必须回答相同的三个问题:一个词从哪里开始?这个词的词根是什么?我们如何在需要时将"运行","运行","运行"视为同一个东西,在不需要时又分待?

如果你的代币器处理了,`don't`作为一个标志,但`do n't`如果你的投票崩,`organization`其他`organ`如果你的化器需要部分语文背景,但你没有通过它,动词将被视为名词.

> 分词做错了,模型就从垃圾数据中学习.`don't`当作一个标志,但把 `do n't`当你两个,训练分开就会分开.`organization`和 `organ`归结为同一个词干,主题建模就会失效――如果你的词形恢复器需要词性上下文,但你没有传入,动词就会被视为名词处理――

这一课程将从零开始构建三个预处理步骤,然后展示NLTK和spaCy如何做同样的工作,

> 课程从零构建到这些三个预处理步骤,然后展示NLTK和SpaceCy如何做同样的工作,让你看到其中的权衡.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

三个操作,每个操作都有一个任务,一个失败模式.

> 只有三种操作,每个人都有自己的责任和失败模式.

**Tokenization**字符串分为代币. "代币"是故意模糊的,因为正确的细分性取决于任务. 经典NLP的字面级别. 变压器的字体. 语言的字符没有白色空间.

> **分词（Tokenization）**将字符串分为标志. 这个词是有意保持模糊的,因为合适的粒度取决于具体任务.

**Stemming**快速,侵略性,愚蠢.`running -> run`现在,我们要去.`organization -> organ`第二个是失败模式.

> **词干提取（Stemming）**使用规则截断后──快速、激进、粗暴──`running -> run`,我知道.`organization -> organ`,第二个例子就是它的失败模式.

**Lemmatization**通过使用语法知识将一个词缩小到词典形式. 慢慢,准确,需要一个搜索表或形态分析仪. `ran -> run`(需要知道"跑"是"跑"的过去时代).`better -> good`(需要了解相对形式).

> **词形还原（Lemmatization）**用语法知识将词还原为词典形式――较慢、准确、需要查找表或形态分析器――`ran -> run`(需要知道"跑"是"跑"的过去时)`better -> good`(需要知道比较级形式)

语:当速度重要时,你可以容忍噪音 (搜索索索引,粗略分类).当意义重要时,你可以语 (回答问题,语义搜索,用户会阅读任何东西).

> 经验法则:当速度重要且能容忍噪音时使用词干提取(搜索引号、粗略分类) ――当语义重要时使用词形还原(问答、语义搜索、任何用户会阅读场景) ――

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
edit-distance
```

## 建立它

### 步骤1:一个regex字符标记器

最简单的有用代币器分成非字母符号,同时保留符号作为自己的代币. 不完美,不是最终的,但它运行在一个行.

> 最简单的实用分词器在非字母数字字符符处分开,同时将标点符号保留为独立代币――不完美,也不是最终方案,但一行代码就能运行――

```python
import re

def tokenize(text):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[0-9]+|[^\sA-Za-z0-9]", text)
```

字母的排序:`don't`现在`it's`) 纯数字:任何单个非白色空间非字母符作为独立的标记 (点点).

> 三个按优先排列的模式──带可选的内部留号的词`don't`,我知道.`it's`)──纯数字──任何单个非空白非字母数字字符作为独立标志 (标点符号)──

```python
>>> tokenize("The cats weren't running at 3pm.")
['The', 'cats', "weren't", 'running', 'at', '3', 'pm', '.']
```

检测失败模式.`3pm`分成`['3', 'pm']`因为我们在字母运行和数字运行之间交替. 足够适合大多数任务. URL,电子邮件,hashtag都破裂.

> 需要注意的失败模式.`3pm`被拆分为`['3', 'pm']`由于我们在字母序列和数字序列之间进行了交换. 对于大多数任务来说,这是足够好的.

### 步骤2:一个 Porter stemmer (仅步骤1a)

波特算法包含五个阶段的规则. 单独的第一步涵盖了最常见的英语后音,并教导了模式.

> 完整的波特算法有五个阶段的规则. 仅仅的步骤1a 涵盖了最常见的英语后,并展示了规则模式.

```python
def stem_step_1a(word):
    if word.endswith("sses"):
        return word[:-2]
    if word.endswith("ies"):
        return word[:-2]
    if word.endswith("ss"):
        return word
    if word.endswith("s") and len(word) > 1:
        return word[:-1]
    return word
```

```python
>>> [stem_step_1a(w) for w in ["caresses", "ponies", "caress", "cats"]]
['caress', 'poni', 'caress', 'cat']
```

阅读下面的规则.`ies -> i`规则是为什么`ponies -> poni`没有`pony`实际的波特有第一步B,可以解决问题,规则竞争,以前的规则赢得,秩序比任何单一规则都重要.

> 从上到下阅读规则.`ies -> i`规则是`ponies -> poni`而不是`pony`原因――真正的波特算法有1b步骤来解决这个问题――规则相互竞争,排在前面的规则胜利――规则的顺序比任何单条规则都重要――

### 步骤3:基于搜索的化器

化需要形态学.一个可操作的教学版本使用一个小的形表和一个倒退.

> 真正的词形还原需要形态学――一个可行的教学版本使用小词表和后备策略――

```python
LEMMA_TABLE = {
    ("running", "VERB"): "run",
    ("ran", "VERB"): "run",
    ("runs", "VERB"): "run",
    ("better", "ADJ"): "good",
    ("best", "ADJ"): "good",
    ("cats", "NOUN"): "cat",
    ("cat", "NOUN"): "cat",
    ("were", "VERB"): "be",
    ("was", "VERB"): "be",
    ("is", "VERB"): "be",
}

def lemmatize(word, pos):
    key = (word.lower(), pos)
    if key in LEMMA_TABLE:
        return LEMMA_TABLE[key]
    if pos == "VERB" and word.endswith("ing"):
        return word[:-3]
    if pos == "NOUN" and word.endswith("s"):
        return word[:-1]
    return word.lower()
```

```python
>>> lemmatize("running", "VERB")
'run'
>>> lemmatize("cats", "NOUN")
'cat'
>>> lemmatize("better", "ADJ")
'good'
>>> lemmatize("watched", "VERB")
'watched'
```

最后一个案例是教学的关键时刻.`watched`没有在我们的桌子上,我们的倒退只能处理.`ing`实际的化覆盖`ed`无规律的动词,比较形容词,音调变化的多元 (`children -> child`这就是为什么生产系统使用WordNet, spaCy的形态分析仪,或一个完整的形态分析仪.

> 最后一个例子是关键的教学时刻.`watched`我们的后备策略只能处理.`ing` 真正的词形还原覆盖 `ed`、不规则动词、比较级形容词、语音变化的复数(`children -> child`这就是为什么生产系统使用WordNet、SpaceCy的形态分析器或完整的形态分析器.

### 步骤4:将它们连接在一起

```python
def preprocess(text, pos_tagger=None):
    tokens = tokenize(text)
    stems = [stem_step_1a(t.lower()) for t in tokens]
    tags = pos_tagger(tokens) if pos_tagger else [(t, "NOUN") for t in tokens]
    lemmas = [lemmatize(word, pos) for word, pos in tags]
    return {"tokens": tokens, "stems": stems, "lemmas": lemmas}
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

现在,默认所有东西都在`NOUN`承认自己的限制.

> 缺少的部分是词性标注器――第五阶段 · 07(词性标注) 将构建一个――目前,将所有词默认为`NOUN`承认这个局限性.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

产品版本的NLTK和SpaCy运输,每行几行.

> 公司提供了生产级版本.

### 其他国家

```python
import nltk
nltk.download("punkt_tab")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger_eng")

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag

text = "The cats were running."
tokens = word_tokenize(text)
stems = [PorterStemmer().stem(t) for t in tokens]
lemmatizer = WordNetLemmatizer()
tagged = pos_tag(tokens)


def nltk_pos_to_wordnet(tag):
    if tag.startswith("V"):
        return "v"
    if tag.startswith("J"):
        return "a"
    if tag.startswith("R"):
        return "r"
    return "n"


lemmas = [lemmatizer.lemmatize(t, nltk_pos_to_wordnet(tag)) for t, tag in tagged]
```

`word_tokenize`处理缩短,Unicode,边缘案例,你的regex错过了.`PorterStemmer`它们在五个阶段都运行.`WordNetLemmatizer`需要从NLTK的Penn Treebank计划转换到WordNet的缩写集.上面的翻译线程是大多数教程的跳过.

> `word_tokenize`处理缩写,Unicode 和你的正则表达式遗漏的边界情况.`PorterStemmer`运行所有五个阶段.`WordNetLemmatizer`需要将 NLTK 的 Penn Treebank 词性标签方案转换为 WordNet 的缩写集.

### 空间

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running.")

for token in doc:
    print(token.text, token.lemma_, token.pos_)
```

```
The      the     DET
cats     cat     NOUN
were     be      AUX
running  run     VERB
.        .       PUNCT
```

太空系统隐藏了整个管道.`nlp(text)`标记, POS标记和 lemmatization都运行. 比NLTK更快. 精确. 折衷是,你不能轻松交换个体组件.

> 整个水线将隐藏在`nlp(text)`背后──分词、词性标注和词形还原全部运行──大规模下比NLTK更快,开箱即用更准确──代价是你无法轻松替换单个组件──

### 什么时候选择哪个

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Teaching, research, swapping components | NLTK | 教学、研究、需要替换组件 | NLTK |
| Production, multi-language, speed matters | spaCy | 生产环境、多语言、速度要求高 | spaCy |
| Transformer pipeline (you'll tokenize with the model's tokenizer anyway) | Use `tokenizers` / `transformers` and skip classical preprocessing | Transformer 流水线（反正你会用模型自带的分词器） | 使用 `tokenizers` / `transformers`，跳过经典预处理 |

### 没有人警告你

两件事会造成真正的预处理管道,而且几乎从来都没有被覆盖.

> 许多教程都已经停止了.

**Reproducibility drift.**它们的版本在NLTK和 spaCy之间改变了代码化和 lemmatizer行为.`['do', "n't"]`在 spaCy 2.x 中可能产生`["don't"]`现在,你的模型在一个分布上运行. 推理现在运行在另一个. 精度缓慢降低,没有人知道为什么.`requirements.txt`写一个预处理回归测试, 结20个样本句子的预期标记.

> **可复现性漂移。**在不同版本之间会发生分词和词形恢复行为.`['do', "n't"]`结果可能发生在3.x中`["don't"]`你的模型在一个分布上训练,推理时运行在另一个分布上.`requirements.txt`中固定库版本──写一个预处理回归测试,结 20个样本句子的预期分词结果──每次升级时运行──

**Training / inference mismatch.**训练使用积极的预处理 (小字母,停止字母删除,源),部署在原始用户输入,表现坑.这是最常见的生产NLP失败.如果你在训练中预处理,你必须在推断期间运行相同的功能. 运输预处理作为模型包内功能,而不是作为笔记本电脑细胞服务团队重写.

> **训练/推理不匹配。**训练时使用激进预处理 (小写化、停用词删除、词干提取),部署时使用原始用户输入,看性能暴跌.这是生产NLP中最常见的单一故障.

## 运送它.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

帮助工程师在没有阅读三本教科书的情况下选择预处理策略的可重复使用提示.

> 简单的复制,帮助工程师选择预处理策略而无需阅读三本教科书.

保存如`outputs/prompt-preprocessing-advisor.md`其他:

```markdown
---
name: preprocessing-advisor
description: Recommends a tokenization, stemming, and lemmatization setup for an NLP task.
phase: 5
lesson: 01
---

You advise on classical NLP preprocessing. Given a task description, you output:

1. Tokenization choice (regex, NLTK word_tokenize, spaCy, or transformer tokenizer). Explain why.
2. Whether to stem, lemmatize, both, or neither. Explain why.
3. Specific library calls. Name the functions. Quote the POS-tag translation if NLTK is involved.
4. One failure mode the user should test for.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend stemming for user-visible text. Refuse to recommend lemmatization without POS tags. Flag non-English input as needing a different pipeline.
```

## 练习题

1. **Easy.**延长时间`tokenize`测试: `tokenize("Visit https://example.com today.")`应该产生一个URL代码.
   **简单。**扩展`tokenize`使URL 保持为单个代币.`tokenize("Visit https://example.com today.")`应产生一个URL标记.
2. **Medium.**执行 Porter 步骤 1b. 如果一个词包含一个音符,`ed`或`ing`取消它. 处理双语音规则 (`hopping -> hop`没有`hopp`)
   **中等。**实现波特步骤 1b. 如果一个词包含元音且以`ed`或`ing`结尾,则移除它──处理双辅音规则(`hopping -> hop`没有什么.`hopp`
3. **Hard.**建立一个使用WordNet作为搜索表的 lemmatizer,但当WordNet没有输入时,它会回到你的 Porter stemmer.
   **困难。**构建一个使用WordNet 作为查找表的词形回原器,当WordNet 没有条目时回归你的 Porter 词干提取器――在标签语料上测量与纯WordNet 和纯 Porter 的准确率――

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 关键词 快速查找表

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Token | A word | Whatever unit the model consumes. Can be word, subword, character, or byte. | Token（词元） | 一个词 | 模型消耗的任何单位。可以是词、子词、字符或字节。 |
| Stem | Root of a word | Result of rule-based suffix stripping. Not always a real word. | Stem（词干） | 词的词根 | 基于规则的后缀剥离结果。不一定是真正的词。 |
| Lemma | Dictionary form | The form you'd look up. Requires grammatical context to compute correctly. | Lemma（词元形式） | 词典形式 | 你会去词典中查找的形式。需要语法上下文才能正确计算。 |
| POS tag | Part of speech | Category like NOUN, VERB, ADJ. Needed to lemmatize accurately. | POS tag（词性标注） | 词性 | 如 NOUN、VERB、ADJ 等类别。准确词形还原需要它。 |
| Morphology | Word shape rules | How a word changes form based on tense, number, case. Lemmatization depends on it. | Morphology（形态学） | 词形变化规则 | 词如何根据时态、数、格变化形式。词形还原依赖它。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.

## 继续阅读 继续阅读

- [Porter, M. F. (1980). An algorithm for suffix stripping](https://tartarus.org/martin/PorterStemmer/def.txt)原始论文,五页,至今仍然是最清晰的解释.
- [spaCy 101 — linguistic features](https://spacy.io/usage/linguistic-features)如何连接一个真正的管道.
- [NLTK book, chapter 3](https://www.nltk.org/book/ch03.html)你还没想过的分词边界情况.
