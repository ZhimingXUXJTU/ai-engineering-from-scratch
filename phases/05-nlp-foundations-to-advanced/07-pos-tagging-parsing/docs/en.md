# POS Tagging and Syntactic Parsing | 词性标注与句法分析

> Grammar was unfashionable for a while. Then every LLM pipeline needed to validate structured extraction, and it came back.

> **【中文解读】** 给每个词标注词性，分析句子的语法结构。

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes)
**Time:** ~45 minutes | **时间:** ~45 minutes


## The Problem | 问题引入

Lesson 01 promised that lemmatization needs a part-of-speech tag. Without knowing `running` is a verb, a lemmatizer cannot reduce it to `run`. Without knowing `better` is an adjective, it cannot reduce to `good`.
> 第 01 课承诺过词形还原需要词性标注。不知道 `running` 是动词，词形还原器无法将其还原为 `run`。不知道 `better` 是形容词，它无法还原为 `good`。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


That promise hid a whole subfield. Part-of-speech tagging assigns grammatical categories. Syntactic parsing recovers the sentence's tree structure: which word modifies which, which verb governs which arguments. Classical NLP spent twenty years refining both. Then deep learning collapsed them into a token-classification task on top of a pretrained transformer, and the research community moved on.
> 那个承诺背后隐藏着一整个子领域。词性标注分配语法类别。句法分析恢复句子的树结构：哪个词修饰哪个，哪个动词支配哪个论元。经典 NLP 花了二十年完善这两者。然后深度学习将它们折叠为预训练 Transformer 之上的 token 分类任务，研究界就转向了。

Not the applied community. Every structured-extraction pipeline still uses POS and dependency trees under the hood. LLM-generated JSON gets validated against grammatical constraints. Question-answering systems decompose queries using dependency parses. Machine translation quality evaluators check alignment of parse trees.
> 应用界没有。每个结构化抽取流水线仍在底层使用 POS 和依存树。LLM 生成的 JSON 会根据语法约束进行验证。问答系统使用依存分析来分解查询。机器翻译质量评估器检查分析树的对齐。

Worth knowing. This lesson introduces the tagsets, the baselines, and the point where you stop implementing from scratch and call spaCy.
> 值得了解。本课介绍标签集、基线以及你停止从零实现转而调用 spaCy 的节点。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


**POS tagging** labels each token with a grammatical category. The **Penn Treebank (PTB)** tagset is the English default. 36 tags with distinctions the casual reader finds fussy: `NN` singular noun, `NNS` plural noun, `NNP` proper noun singular, `VBD` verb past tense, `VBZ` verb 3rd person singular present, and so on. The **Universal Dependencies (UD)** tagset is coarser (17 tags) and language-agnostic; it became the default for cross-lingual work.
> **词性标注（POS Tagging）** 为每个 token 标注语法类别。**Penn Treebank (PTB)** 标签集是英语的默认选择。36 个标签，带有一般读者觉得过于细致的区别：`NN` 单数名词、`NNS` 复数名词、`NNP` 专有名词单数、`VBD` 动词过去时、`VBZ` 动词第三人称单数现在时等等。**通用依存（Universal Dependencies, UD）** 标签集更粗（17 个标签）且与语言无关；它成为了跨语言工作的默认选择。

```
The/DET cats/NOUN were/AUX running/VERB at/ADP 3pm/NOUN ./PUNCT
```

**Syntactic parsing** produces a tree. Two major styles:
> **句法分析（Syntactic Parsing）** 产生一棵树。两种主要风格：

- **Constituency parsing.** Noun phrases, verb phrases, prepositional phrases nest inside each other. Output is a tree of non-terminal categories (NP, VP, PP) with words as leaves.
- **Dependency parsing.** Each word has a single head word it depends on, labeled with a grammatical relation. Output is a tree where every edge is a (head, dependent, relation) triple.
> - **成分分析（Constituency Parsing）。** 名词短语、动词短语、介词短语嵌套在一起。输出是非终结类别（NP、VP、PP）的树，词作为叶子。
- **依存分析（Dependency Parsing）。** 每个词有一个支配它的中心词，标注语法关系。输出是一棵树，每条边是一个 (head, dependent, relation) 三元组。

Dependency parsing won in the 2010s because it generalizes cleanly across languages, especially free-word-order ones.
> 依存分析在 2010 年代胜出，因为它跨语言泛化更干净，特别是自由语序语言。

```
running is ROOT
cats is nsubj of running
were is aux of running
at is prep of running
3pm is pobj of at
```

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。


## Build It | 动手实现

### Step 1: most-frequent-tag baseline
> 最笨但管用的 POS 标注器。对每个词，预测它在训练中最常有的标签。

The dumbest POS tagger that works. For each word, predict the tag it had most often in training.
> 在 Brown 语料库上，这个基线达到约 85% 的准确率。不好，但这是任何严肃模型都不应低于的底线。

```python
from collections import Counter, defaultdict


def train_mft(train_examples):
    word_tag_counts = defaultdict(Counter)
    all_tags = Counter()
    for tokens, tags in train_examples:
        for token, tag in zip(tokens, tags):
            word_tag_counts[token.lower()][tag] += 1
            all_tags[tag] += 1
    word_best = {w: c.most_common(1)[0][0] for w, c in word_tag_counts.items()}
    default_tag = all_tags.most_common(1)[0][0]
    return word_best, default_tag


def predict_mft(tokens, word_best, default_tag):
    return [word_best.get(t.lower(), default_tag) for t in tokens]
```

On the Brown corpus, this baseline hits ~85% accuracy. Not good, but the floor below which no serious model should fall.
> 建模序列的联合概率：

### Step 2: bigram HMM tagger
> 两个表：转移概率（给定前一个标签的标签概率），发射概率（给定标签的词概率）。两者都从计数中用拉普拉斯平滑估计。用 Viterbi 解码（在标签格上的动态规划）。

Model the joint probability of the sequence:
> 在 Brown 语料库上二元组 HMM 达到约 93% 的准确率。从 85% 到 93% 的跳跃主要来自转移概率——模型学到 `DET NOUN` 是常见的而 `NOUN DET` 是罕见的。

```
P(tags, words) = prod P(tag_i | tag_{i-1}) * P(word_i | tag_i)
```

Two tables: transition probabilities (tag given previous tag), emission probabilities (word given tag). Estimate both from counts with Laplace smoothing. Decode with Viterbi (dynamic programming over the tag lattice).
> 转移 + 发射概率是局部的。它们无法捕获 `saw` 在 "I bought a saw" 中是名词但在 "I saw the movie" 中是动词。带有任意特征（后缀、词形、前后词、词本身）的 CRF 达到约 97%。BiLSTM-CRF 或 Transformer 达到约 98%+。

```python
import math


def train_hmm(train_examples, alpha=0.01):
    transitions = defaultdict(Counter)
    emissions = defaultdict(Counter)
    tags = set()
    vocab = set()

    for tokens, ts in train_examples:
        prev = "<BOS>"
        for token, tag in zip(tokens, ts):
            transitions[prev][tag] += 1
            emissions[tag][token.lower()] += 1
            tags.add(tag)
            vocab.add(token.lower())
            prev = tag
        transitions[prev]["<EOS>"] += 1

    return transitions, emissions, tags, vocab


def log_prob(table, given, key, smooth_denom, alpha):
    return math.log((table[given].get(key, 0) + alpha) / smooth_denom)


def viterbi(tokens, transitions, emissions, tags, vocab, alpha=0.01):
    tags_list = list(tags)
    n = len(tokens)
    V = [[0.0] * len(tags_list) for _ in range(n)]
    back = [[0] * len(tags_list) for _ in range(n)]

    for j, tag in enumerate(tags_list):
        em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
        tr_denom = sum(transitions["<BOS>"].values()) + alpha * (len(tags_list) + 1)
        tr = log_prob(transitions, "<BOS>", tag, tr_denom, alpha)
        em = log_prob(emissions, tag, tokens[0].lower(), em_denom, alpha)
        V[0][j] = tr + em
        back[0][j] = 0

    for i in range(1, n):
        for j, tag in enumerate(tags_list):
            em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
            em = log_prob(emissions, tag, tokens[i].lower(), em_denom, alpha)
            best_prev = 0
            best_score = -1e30
            for k, prev_tag in enumerate(tags_list):
                tr_denom = sum(transitions[prev_tag].values()) + alpha * (len(tags_list) + 1)
                tr = log_prob(transitions, prev_tag, tag, tr_denom, alpha)
                score = V[i - 1][k] + tr + em
                if score > best_score:
                    best_score = score
                    best_prev = k
            V[i][j] = best_score
            back[i][j] = best_prev

    last_best = max(range(len(tags_list)), key=lambda j: V[n - 1][j])
    path = [last_best]
    for i in range(n - 1, 0, -1):
        path.append(back[i][path[-1]])
    return [tags_list[j] for j in reversed(path)]
```

Bigram HMM on Brown hits ~93% accuracy. The jump from 85% to 93% is mostly transition probabilities — the model learns `DET NOUN` is common and `NOUN DET` is rare.
> 这个任务的天花板由标注者分歧决定。人类标注者在 Penn Treebank 上约 97% 的时间达成一致。超过 98% 的模型可能过拟合了测试集。

### Step 3: why modern taggers beat this
> 从零实现完整依存分析超出范围；经典的教科书处理见 Jurafsky 和 Martin。需要了解的两个经典系列：

Transition + emission probabilities are local. They cannot capture that `saw` is a noun in "I bought a saw" but a verb in "I saw the movie." A CRF with arbitrary features (suffix, word shape, word before and after, word itself) hits ~97%. A BiLSTM-CRF or transformer hits ~98%+.
> - **基于转移的**解析器（arc-eager、arc-standard）像移进-归约解析器一样工作：读入 token，移进到栈上，应用创建弧的归约动作。贪婪解码很快。经典实现是 MaltParser。现代神经版本：Chen 和 Manning 的基于转移的解析器。
- **基于图的**解析器（Eisner 算法、Dozat-Manning 双仿射）对每个可能的 head-dependent 边打分，选择最大生成树。更慢但更准确。

The ceiling on this task is set by annotator disagreement. Human annotators agree about 97% of the time on Penn Treebank. Models past 98% are probably overfitting the test set.
> 对于大多数应用工作，调用 spaCy：

### Step 4: dependency parsing sketch
> 从下往上阅读 `dep` 列，句子的语法结构就自然呈现了。

Full dependency parsing from scratch is out of scope; the canonical textbook treatment is in Jurafsky and Martin. Two classical families to know:

- **Transition-based** parsers (arc-eager, arc-standard) act like a shift-reduce parser: they read tokens, shift them onto a stack, and apply reduce actions that create arcs. Greedy decoding is fast. Classic implementation is MaltParser. Modern neural version: Chen and Manning's transition-based parser.
- **Graph-based** parsers (Eisner's algorithm, Dozat-Manning biaffine) score every possible head-dependent edge and pick the maximum spanning tree. Slower but more accurate.

For most applied work, call spaCy:

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running at 3pm.")
for token in doc:
    print(f"{token.text:10s} tag={token.tag_:5s} pos={token.pos_:6s} dep={token.dep_:10s} head={token.head.text}")
```

```
The        tag=DT    pos=DET    dep=det        head=cats
cats       tag=NNS   pos=NOUN   dep=nsubj      head=running
were       tag=VBD   pos=AUX    dep=aux        head=running
running    tag=VBG   pos=VERB   dep=ROOT       head=running
at         tag=IN    pos=ADP    dep=prep       head=running
3pm        tag=NN    pos=NOUN   dep=pobj       head=at
.          tag=.     pos=PUNCT  dep=punct      head=running
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


Read the `dep` column bottom to top and the sentence's grammatical structure falls out.


> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

Every production NLP library ships POS and dependency parsers as part of a standard pipeline.
> 每个生产 NLP 库都把 POS 和依存解析器作为标准流水线的一部分提供。

- **spaCy** (`en_core_web_sm` / `md` / `lg` / `trf`). Fast, accurate, integrated with tokenization + NER + lemmatization. `token.tag_` (Penn), `token.pos_` (UD), `token.dep_` (dependency relation).
- **Stanford NLP (stanza)**. Stanford's successor to CoreNLP. State-of-the-art on 60+ languages.
- **trankit**. Transformer-based, good UD accuracy.
- **NLTK**. `pos_tag`. Usable, slow, older. Fine for teaching.
> - **spaCy**（`en_core_web_sm` / `md` / `lg` / `trf`）。快速、准确，与分词 + NER + 词形还原集成。`token.tag_`（Penn）、`token.pos_`（UD）、`token.dep_`（依存关系）。
- **Stanford NLP (stanza)**。Stanford CoreNLP 的继任者。在 60+ 种语言上达到先进水平。
- **trankit**。基于 Transformer，良好的 UD 准确率。
- **NLTK**。`pos_tag`。可用、慢、较旧。适合教学。

### Where this still matters in 2026
> - **词形还原。** 第 01 课需要 POS 才能正确词形还原。始终如此。
- **LLM 输出的结构化抽取。** 验证生成的句子满足语法约束（如主谓一致、必要修饰语）。
- **基于方面的情感分析。** 依存分析告诉你哪个形容词修饰哪个名词。
- **查询理解。** "movies directed by Wes Anderson starring Bill Murray" 通过解析分解为结构化约束。
- **跨语言迁移。** UD 标签和依存关系与语言无关，支持新语言的零样本结构化分析。
- **低算力流水线。** 如果你不能部署 Transformer，POS + 依存分析 + 地名词典能让你走得相当远。

- **Lemmatization.** Lesson 01 needs POS to lemmatize correctly. Always.
- **Structured extraction from LLM outputs.** Validate that a generated sentence respects grammatical constraints (e.g., subject-verb agreement, required modifiers).
- **Aspect-based sentiment.** Dependency parses tell you which adjective modifies which noun.
- **Query understanding.** "movies directed by Wes Anderson starring Bill Murray" decomposes into structured constraints via the parse.
- **Cross-lingual transfer.** UD tags and dependency relations are language-agnostic, enabling zero-shot structured analysis of new languages.
- **Low-compute pipelines.** If you cannot ship a transformer, POS + dependency parse + gazetteer gets you surprisingly far.

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


## Ship It | 产出物

Save as `outputs/skill-grammar-pipeline.md`:
> 保存为 `outputs/skill-grammar-pipeline.md`：

```markdown
---
name: grammar-pipeline
description: Design a classical POS + dependency pipeline for a downstream NLP task.
version: 1.0.0
phase: 5
lesson: 07
tags: [nlp, pos, parsing]
---

Given a downstream task (information extraction, rewrite validation, query decomposition, lemmatization), you output:

1. Tagset to use. Penn Treebank for English-only legacy pipelines, Universal Dependencies for multilingual or cross-lingual.
2. Library. spaCy for most production, stanza for academic-grade multilingual, trankit for highest UD accuracy. Name the specific model ID.
3. Integration pattern. Show the 3-5 lines that call the library and consume the needed attributes (`.pos_`, `.dep_`, `.head`).
4. Failure mode to test. Noun-verb ambiguity (`saw`, `book`, `can`) and PP-attachment ambiguity are the classical traps. Sample 20 outputs and eyeball.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse to recommend rolling your own parser. Building parsers from scratch is a research project, not an application task. Flag any pipeline that consumes POS tags without handling lowercase/uppercase variants as fragile.
```

## Exercises | 练习题

1. **Easy.** Using the most-frequent-tag baseline on a small tagged corpus (e.g., NLTK's Brown subset), measure accuracy on held-out sentences. Verify the ~85% result.
2. **Medium.** Train the bigram HMM above and report per-tag precision/recall. Which tags does the HMM confuse most?
3. **Hard.** Use spaCy's dependency parse to extract subject-verb-object triples from a 1000-sentence sample. Evaluate on 50 manually labeled triples. Document where extraction fails (often passives, coordinations, and elided subjects).
> 1. **简单。** 在一个小型标注语料（如 NLTK 的 Brown 子集）上使用最频繁标签基线，测量在留出句子上的准确率。验证约 85% 的结果。
2. **中等。** 训练上述二元组 HMM 并报告每标签精确率/召回率。HMM 最容易混淆哪些标签？
3. **困难。** 使用 spaCy 的依存分析从 1000 句样本中提取主谓宾三元组。在 50 个手动标注的三元组上评估。记录抽取失败的地方（通常是被动语态、并列和省略主语）。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| POS tag | Word's type | Grammatical category. PTB has 36; UD has 17. |
| Penn Treebank | Standard tagset | English-specific. Fine-grained verb tenses and noun number. |
| Universal Dependencies | Multilingual tagset | Coarser than PTB; language-neutral; defaults for cross-lingual work. |
| Dependency parse | Sentence tree | Each word has one head, each edge has a grammatical relation. |
| Viterbi | Dynamic programming | Finds the highest-probability tag sequence given emissions and transitions. |
> | 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| POS 标签 | 词的类型 | 语法类别。PTB 有 36 个；UD 有 17 个。 |
| Penn Treebank | 标准标签集 | 特定于英语。细粒度的动词时态和名词数。 |
| 通用依存（UD） | 多语言标签集 | 比 PTB 更粗；语言无关；跨语言工作的默认选择。 |
| 依存分析 | 句子树 | 每个词有一个中心词，每条边有一个语法关系。 |
| Viterbi 算法 | 动态规划 | 给定发射和转移概率，找到最高概率的标签序列。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Jurafsky and Martin — Speech and Language Processing, chapters 8 and 18](https://web.stanford.edu/~jurafsky/slp3/) — the canonical textbook treatment of POS and parsing.
- [Universal Dependencies project](https://universaldependencies.org/) — the cross-lingual tagset and treebank collection used by every multilingual parser.
- [spaCy linguistic features guide](https://spacy.io/usage/linguistic-features) — practical reference for every attribute exposed on `Token`.
- [Chen and Manning (2014). A Fast and Accurate Dependency Parser using Neural Networks](https://nlp.stanford.edu/pubs/emnlp2014-depparser.pdf) — the paper that brought neural parsers into the mainstream.
> - [Jurafsky and Martin — Speech and Language Processing, chapters 8 and 18](https://web.stanford.edu/~jurafsky/slp3/) — POS 和解析的经典教科书处理。
- [Universal Dependencies project](https://universaldependencies.org/) — 每个多语言解析器使用的跨语言标签集和树库集合。
- [spaCy linguistic features guide](https://spacy.io/usage/linguistic-features) — `Token` 上暴露的每个属性的实用参考。
- [Chen and Manning (2014). A Fast and Accurate Dependency Parser using Neural Networks](https://nlp.stanford.edu/pubs/emnlp2014-depparser.pdf) — 将神经解析器带入主流的论文。
