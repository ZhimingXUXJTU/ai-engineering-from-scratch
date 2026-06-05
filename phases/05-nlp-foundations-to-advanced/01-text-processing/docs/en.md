# Text Processing — Tokenization, Stemming, Lemmatization | 文本处理 — 分词、词干提取、词形还原

> Language is continuous. Models are discrete. Preprocessing is the bridge.
> 语言是连续的。模型是离散的。预处理是两者之间的桥梁。

> **【中文解读】** 分词是 NLP 的第一步：把连续文本切成离散 token。包括词干提取和词形还原。在 LLM 时代，分词由 BPE 等子词分词器处理。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Understand tokenization, stemming, and lemmatization as distinct preprocessing operations
  理解分词、词干提取和词形还原作为不同的预处理操作
- Build a regex tokenizer, a Porter stemmer step, and a lookup-based lemmatizer from scratch
  从零构建正则分词器、Porter 词干提取步骤和基于查找表的词形还原器
- Compare NLTK and spaCy for production preprocessing pipelines
  比较 NLTK 和 spaCy 在生产预处理流水线中的优劣
- Recognize the two most common production failures: reproducibility drift and train/inference mismatch
  识别两种最常见的生产故障：可复现性漂移和训练/推理不匹配

## The Problem | 问题引入

A model cannot read "The cats were running." It reads integers.

> 模型无法直接读取 "The cats were running."。它读取的是整数。

Every NLP system opens with the same three questions. Where does a word start. What is the root of the word. How do we treat "run", "running", "ran" as the same thing when it helps, and as different things when it doesn't.

> 每个 NLP 系统都必须回答同样的三个问题：一个词从哪里开始？这个词的词根是什么？我们如何在需要时将 "run"、"running"、"ran" 视为同一个东西，在不需要时又区分对待？

Get tokenization wrong and the model learns from garbage. If your tokenizer treats `don't` as one token but `do n't` as two, the training distribution splits. If your stemmer collapses `organization` and `organ` to the same stem, topic modeling dies. If your lemmatizer needs part-of-speech context but you don't pass it, verbs get treated as nouns.

> 分词做错了，模型就从垃圾数据中学习。如果你的分词器把 `don't` 当作一个 token，但把 `do n't` 当作两个，训练分布就会分裂。如果你的词干提取器把 `organization` 和 `organ` 归结为同一个词干，主题建模就会失效。如果你的词形还原器需要词性上下文但你没有传入，动词就会被当作名词处理。

This lesson builds the three preprocessing steps from scratch, then shows how NLTK and spaCy do the same work so you can see the tradeoffs.

> 本课从零构建这三个预处理步骤，然后展示 NLTK 和 spaCy 如何做同样的工作，让你看到其中的权衡。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

Three operations. Each has a job and a failure mode.

> 三个操作，每个都有自己的职责和失败模式。

**Tokenization** splits a string into tokens. "Token" is deliberately vague because the right granularity depends on the task. Word-level for classical NLP. Subword for transformers. Character for languages without whitespace.

> **分词（Tokenization）** 将字符串拆分为 token。"Token" 这个词是有意保持模糊的，因为合适的粒度取决于具体任务。经典 NLP 用词级别，Transformer 用子词级别，没有空格的语言用字符级别。

**Stemming** chops suffixes with rules. Fast, aggressive, dumb. `running -> run`. `organization -> organ`. That second one is the failure mode.

> **词干提取（Stemming）** 使用规则截断后缀。快速、激进、粗暴。`running -> run`。`organization -> organ`。第二个例子就是它的失败模式。

**Lemmatization** reduces a word to its dictionary form using grammar knowledge. Slower, accurate, needs a lookup table or morphological analyzer. `ran -> run` (needs to know "ran" is past tense of "run"). `better -> good` (needs to know comparative forms).

> **词形还原（Lemmatization）** 利用语法知识将词还原为词典形式。较慢、准确、需要查找表或形态分析器。`ran -> run`（需要知道 "ran" 是 "run" 的过去时）。`better -> good`（需要知道比较级形式）。

Rule of thumb. Stem when speed matters and you can tolerate noise (search indexing, rough classification). Lemmatize when meaning matters (question answering, semantic search, anything the user will read).

> 经验法则：当速度重要且能容忍噪声时使用词干提取（搜索索引、粗略分类）。当语义重要时使用词形还原（问答、语义搜索、任何用户会阅读的场景）。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### Step 1: a regex word tokenizer

The simplest useful tokenizer splits on non-alphanumeric characters while keeping punctuation as its own tokens. Not perfect, not final, but it runs in one line.

> 最简单实用的分词器在非字母数字字符处分割，同时将标点符号保留为独立 token。不完美，也不是最终方案，但一行代码就能运行。

```python
import re

def tokenize(text):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[0-9]+|[^\sA-Za-z0-9]", text)
```

Three patterns in order of precedence. Words with optional inner apostrophe (`don't`, `it's`). Pure numbers. Any single non-whitespace non-alphanumeric character as a standalone token (punctuation).

> 三个按优先级排列的模式。带可选内部撇号的词（`don't`、`it's`）。纯数字。任何单个非空白非字母数字字符作为独立 token（标点符号）。

```python
>>> tokenize("The cats weren't running at 3pm.")
['The', 'cats', "weren't", 'running', 'at', '3', 'pm', '.']
```

Failure modes to notice. `3pm` splits to `['3', 'pm']` because we alternated between letter runs and digit runs. Good enough for most tasks. URLs, emails, hashtags all break. For production, add patterns before the general ones.

> 需要注意的失败模式。`3pm` 被拆分为 `['3', 'pm']`，因为我们在字母序列和数字序列之间做了交替。对大多数任务来说足够好。URL、电子邮件、话题标签都会出问题。生产环境中，需要在通用模式之前添加专用模式。

### Step 2: a Porter stemmer (step 1a only)

The full Porter algorithm has five phases of rules. Step 1a alone covers the most frequent English suffixes and teaches the pattern.

> 完整的 Porter 算法有五个阶段的规则。仅步骤 1a 就涵盖了最常见的英语后缀，并展示了规则模式。

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

Read the rules top-down. The `ies -> i` rule is why `ponies -> poni`, not `pony`. Real Porter has step 1b that would fix it. Rules compete. Earlier rules win. The order matters more than any single rule.

> 从上到下阅读规则。`ies -> i` 规则是 `ponies -> poni` 而不是 `pony` 的原因。真正的 Porter 算法有步骤 1b 来修复这个问题。规则相互竞争，排在前面的规则获胜。规则的顺序比任何单条规则都重要。

### Step 3: a lookup-based lemmatizer

Lemmatization proper needs morphology. A tractable teaching version uses a small lemma table and a fallback.

> 真正的词形还原需要形态学。一个可行的教学版本使用小型词典表和后备策略。

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

The last case is the key teaching moment. `watched` is not in our table and our fallback only handles `ing`. Real lemmatization covers `ed`, irregular verbs, comparative adjectives, plurals with sound changes (`children -> child`). This is why production systems use WordNet, spaCy's morphologizer, or a full morphological analyzer.

> 最后一个例子是关键的教学时刻。`watched` 不在我们的表中，而我们的后备策略只处理 `ing`。真正的词形还原覆盖 `ed`、不规则动词、比较级形容词、语音变化的复数（`children -> child`）。这就是为什么生产系统使用 WordNet、spaCy 的形态分析器或完整的形态分析器。

### Step 4: pipe them together

```python
def preprocess(text, pos_tagger=None):
    tokens = tokenize(text)
    stems = [stem_step_1a(t.lower()) for t in tokens]
    tags = pos_tagger(tokens) if pos_tagger else [(t, "NOUN") for t in tokens]
    lemmas = [lemmatize(word, pos) for word, pos in tags]
    return {"tokens": tokens, "stems": stems, "lemmas": lemmas}
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。

The missing piece is a POS tagger. Phase 5 · 07 (POS Tagging) builds one. For now, default everything to `NOUN` and acknowledge the limitation.

> 缺少的部分是词性标注器。Phase 5 · 07（词性标注）会构建一个。目前，将所有词默认为 `NOUN`，并承认这个局限性。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

NLTK and spaCy ship the production versions. A few lines each.

> NLTK 和 spaCy 提供了生产级版本。各只需几行代码。

### NLTK

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

`word_tokenize` handles contractions, Unicode, edge cases your regex misses. `PorterStemmer` runs all five phases. `WordNetLemmatizer` needs the POS tag translated from NLTK's Penn Treebank scheme to WordNet's abbreviation set. The translation wiring above is the bit most tutorials skip.

> `word_tokenize` 处理缩写、Unicode 和你的正则表达式遗漏的边界情况。`PorterStemmer` 运行所有五个阶段。`WordNetLemmatizer` 需要将 NLTK 的 Penn Treebank 词性标注方案转换为 WordNet 的缩写集。上面的转换代码是大多数教程跳过的部分。

### spaCy

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

spaCy hides the whole pipeline behind `nlp(text)`. Tokenization, POS tagging, and lemmatization all run. Faster than NLTK at scale. More accurate out of the box. The tradeoff is that you cannot easily swap individual components.

> spaCy 将整个流水线隐藏在 `nlp(text)` 背后。分词、词性标注和词形还原全部运行。在大规模下比 NLTK 更快，开箱即用更准确。代价是你无法轻松替换单个组件。

### When to pick which

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Teaching, research, swapping components | NLTK | 教学、研究、需要替换组件 | NLTK |
| Production, multi-language, speed matters | spaCy | 生产环境、多语言、速度要求高 | spaCy |
| Transformer pipeline (you'll tokenize with the model's tokenizer anyway) | Use `tokenizers` / `transformers` and skip classical preprocessing | Transformer 流水线（反正你会用模型自带的分词器） | 使用 `tokenizers` / `transformers`，跳过经典预处理 |

### The two failure modes nobody warns you about

Most tutorials teach the algorithms and stop. Two things will bite a real preprocessing pipeline, and they are almost never covered.

> 大多数教程教完算法就停了。有两个问题会咬到真正的预处理流水线，而且几乎从未被提到。

**Reproducibility drift.** NLTK and spaCy change tokenization and lemmatizer behavior between versions. What produced `['do', "n't"]` in spaCy 2.x may produce `["don't"]` in 3.x. Your model was trained on one distribution. Inference now runs on a different one. Accuracy quietly degrades and nobody knows why. Pin library versions in `requirements.txt`. Write a preprocessing regression test that freezes expected tokenization of 20 sample sentences. Run it on every upgrade.

> **可复现性漂移。** NLTK 和 spaCy 在不同版本之间会改变分词和词形还原行为。在 spaCy 2.x 中产生 `['do', "n't"]` 的结果，在 3.x 中可能产生 `["don't"]`。你的模型在一个分布上训练，推理时运行在另一个分布上。准确率悄然下降，没人知道原因。在 `requirements.txt` 中固定库版本。写一个预处理回归测试，冻结 20 个样本句子的预期分词结果。每次升级时运行。

**Training / inference mismatch.** Train with aggressive preprocessing (lowercase, stopword removal, stemming), deploy on raw user input, watch performance crater. This is the single most common production NLP failure. If you preprocess during training, you must run the identical function during inference. Ship preprocessing as a function inside the model package, not as a notebook cell the serving team rewrites.

> **训练/推理不匹配。** 训练时使用激进的预处理（小写化、停用词去除、词干提取），部署时用原始用户输入，看着性能暴跌。这是生产 NLP 中最常见的单一故障。如果你在训练时做了预处理，推理时必须运行完全相同的函数。将预处理作为模型包内的一个函数发布，而不是让服务团队重写的一个笔记本单元格。

## Ship It | 产出物

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

A reusable prompt that helps engineers pick a preprocessing strategy without reading three textbooks.

> 一个可复用的 prompt，帮助工程师选择预处理策略而无需阅读三本教科书。

Save as `outputs/prompt-preprocessing-advisor.md`:

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

## Exercises | 练习题

1. **Easy.** Extend `tokenize` to keep URLs as single tokens. Test: `tokenize("Visit https://example.com today.")` should produce one URL token.
   **简单。** 扩展 `tokenize` 使 URL 保持为单个 token。测试：`tokenize("Visit https://example.com today.")` 应产生一个 URL token。
2. **Medium.** Implement Porter step 1b. If a word contains a vowel and ends in `ed` or `ing`, remove it. Handle the double-consonant rule (`hopping -> hop`, not `hopp`).
   **中等。** 实现 Porter 步骤 1b。如果一个词包含元音且以 `ed` 或 `ing` 结尾，则移除它。处理双辅音规则（`hopping -> hop`，而不是 `hopp`）。
3. **Hard.** Build a lemmatizer that uses WordNet as a lookup table but falls back to your Porter stemmer when WordNet has no entry. Measure accuracy on a tagged corpus against plain WordNet and plain Porter.
   **困难。** 构建一个使用 WordNet 作为查找表的词形还原器，当 WordNet 没有条目时回退到你的 Porter 词干提取器。在标注语料上测量相对于纯 WordNet 和纯 Porter 的准确率。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Token | A word | Whatever unit the model consumes. Can be word, subword, character, or byte. | Token（词元） | 一个词 | 模型消耗的任何单位。可以是词、子词、字符或字节。 |
| Stem | Root of a word | Result of rule-based suffix stripping. Not always a real word. | Stem（词干） | 词的词根 | 基于规则的后缀剥离结果。不一定是真正的词。 |
| Lemma | Dictionary form | The form you'd look up. Requires grammatical context to compute correctly. | Lemma（词元形式） | 词典形式 | 你会去词典中查找的形式。需要语法上下文才能正确计算。 |
| POS tag | Part of speech | Category like NOUN, VERB, ADJ. Needed to lemmatize accurately. | POS tag（词性标注） | 词性 | 如 NOUN、VERB、ADJ 等类别。准确词形还原需要它。 |
| Morphology | Word shape rules | How a word changes form based on tense, number, case. Lemmatization depends on it. | Morphology（形态学） | 词形变化规则 | 词如何根据时态、数、格变化形式。词形还原依赖它。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## Further Reading | 延伸阅读

- [Porter, M. F. (1980). An algorithm for suffix stripping](https://tartarus.org/martin/PorterStemmer/def.txt) — the original paper, five pages, still the clearest explanation. / 原始论文，五页，至今仍然是最清晰的解释。
- [spaCy 101 — linguistic features](https://spacy.io/usage/linguistic-features) — how a real pipeline is wired. / 真实流水线是如何连接的。
- [NLTK book, chapter 3](https://www.nltk.org/book/ch03.html) — tokenization edge cases you haven't thought of yet. / 你还没想过的分词边界情况。
