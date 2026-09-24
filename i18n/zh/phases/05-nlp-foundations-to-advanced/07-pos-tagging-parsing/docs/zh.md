# 标签和语法分析

> 语法一段时间不适用,然后每一个LLM管道都需要验证结构化的提取,
> 语法曾经不流行. 后来每个LLM流水线都需要验证结构化抽取,它又回来了.

> **【中文解读】**给每一个词标注词性,分析句子的语法结构.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

第1课承诺, 化需要部分语音标签.`running`是一个动词,一个 lemmatizer不能把它缩小到`run`没有意识到`better`是一个形容词,不能缩小到`good`现在,我们要去.

> 第1课 承诺过词形复原需要词性标注――不知道`running`是动词,词形还原器无法将其恢复为`run`不知道`better`是形容词,它无法恢复为`good`,我知道.

语法分析恢复了句子的树结构:哪个词修改哪个,哪个动词控制哪些参数.经典NLP花了二十年时间来完善这两种.然后深度学习将它们分解成一个预训练的变压器之上的代币分类任务,研究社区继续前进.

> 那个承诺背后隐藏着整个子领域――词性标记分配语法类别――句法分析恢复句子的树结构:哪个词修饰哪个,哪个动词支配哪个论元――经典的NLP花了二十年完善这两者――然后深度学习将它们折叠成预训练变革器 之上的标志 分类任务,研究界就转向了――

没有应用社区.每个结构化提取管道仍然使用 POS 和依赖树在罩杯下.LLM生成的JSON得到对语法限制进行验证.问答系统使用依赖解析分解查询.机器翻译质量评估人员检查解析树的对齐.

> 应用界没有. 每个结构化抽取流水线仍然在底层使用POS 和依赖树. LLM 生成的JSON会根据语法约束进行验证.

这一课介绍了标签组,基线,以及你停止从零开始实现的点,

> 值得了解. 本课介绍标签集,基线以及你停止从零实现转而调用空间的节点.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

**POS tagging**标签每一个符号以语法类别.**Penn Treebank (PTB)**标签是英语默认的. 36个标签有区别,随便读者发现很尬: `NN`单一名词`NNS`复数名词`NNP`个体名词`VBD`过去时代的动词,`VBZ`动词第三个单词存在,等等.**Universal Dependencies (UD)**标签是粗的 (17标签) 和语言不认同的;它成为跨语言工作的默认.

> **词性标注（POS Tagging）**为每一个标志语法类别.**Penn Treebank (PTB)**标签集是英语默认选择.`NN`单数名词,`NNS`复数名词`NNP`专名词单数`VBD`动词过去时,`VBZ`动词第三人称单数现在时等等等.**通用依存（Universal Dependencies, UD）**标签集更粗 ((17个标签) 与语言无关;它成为跨语言工作的默认选择.

```
The/DET cats/NOUN were/AUX running/VERB at/ADP 3pm/NOUN ./PUNCT
```

**Syntactic parsing**树木的生长方式是:

> **句法分析（Syntactic Parsing）**产生一棵树──两种主要风格:

- **Constituency parsing.**词词,动词,预语词,在彼此内嵌. 输出是一个非终端类别的树 (NP,VP,PP) 具有单词的叶子.
  **成分分析（Constituency Parsing）。**名词短语、动词短语、介词短语嵌套在一起──输出非终结类别(NP、VP、PP) 的树,词作为叶子──
- **Dependency parsing.**每个字都有一个单个单词,它依赖于,标记着语法关系.输出是一个树,每个边缘是一个 (头,依赖,关系) 三倍.
  **依存分析（Dependency Parsing）。**每个词有一个支配它的中心词,标注语法关系――输出是一棵树,每条边是一个 (头,依赖,关系) 三元组――

依赖性解析在2010年代取得了成功,因为它在语言中,特别是自由单词顺序中,

> 依赖分析在2010年取得了成功,因为它跨语言泛化更干净,特别是自由语序语言.

```
running is ROOT
cats is nsubj of running
were is aux of running
at is prep of running
3pm is pobj of at
```

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
pos-tagger
```

```figure
dependency-arcs
```

## 建立它

### 步骤1:最常见标签的基线

对于每一个字,预测它在训练中最常用的标签.

> 最但管用的POS标记器──对每一个词,预测它在训练中最常见的标记──

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

在布朗体上,这个基线达到85%的准确度. 不好,但没有任何严重的模型应该落下的地板.

> 在色语料库上,这个基线达到约85%的准确率.

### 步骤2:大 HMM标签

模型对序列的联合概率:

> 建模序列的联合概率:

```
P(tags, words) = prod P(tag_i | tag_{i-1}) * P(word_i | tag_i)
```

两个表:过渡概率 (给前一个标签),排放概率 (给一个词标签). 根据拉普莱斯平滑计算来估算两者. 用维特比解码 (在标签网格上动态编程).

> 两个表:转移概率 (给定前一个标签的标签概率),发射概率 (发射概率) 给定标签的词概率 (给定标签的词概率) 两者都从计数中使用拉普拉斯平滑估计.

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

黑色的HMM大小是93%的准确度.从85%跳到93%的跳跃主要是过渡概率模型学习`DET NOUN`常见的`NOUN DET`很少见.

> 在语料库上二元组HMM 达到93%的准确率.从85%到93%的跳跃主要来自转移概率模型学到`DET NOUN`是常见的.`NOUN DET`是很罕见的.

### 步骤3:为什么现代标记器比这更好

转变+排放概率是本地的.`saw`在"我买了"中是名词,但在"我看过电影"中是动词.一个任意特征的CRF (后音,字形,字前后,字本身) 达到~97%.一个BiLSTM-CRF或变压器达到~98%+.

> 转移+发射概率是局部的.`saw`在"我买了"中是名词但在"我看了电影"中是动词──带有任意特征(后、词形、前后词、词本身) 的CRF 达到约97%──BiLSTM-CRF或变压器 达到约98%+──

们在林银行上约97%的时间都同意.超过98%的模型可能过于适合测试集.

> 标志者分歧决定了这一任务的天花板. 标志者在宾夕法尼亚州木树银行上达成了97%的时间的一致.

### 步骤4:依赖性分析草图

完全依赖从零开始分析是不适用的;正文教科书处理是Jurafsky和马丁.

> 从零实现完整依赖分析超出范围;经典教科书处理见Jurafsky和Martin──需要了解的两个经典系列:

- **Transition-based**解析器 (arc-eager,arc-standard) 像一个减变解析器一样:它们读取代币,将它们移到堆上,并应用减少创建弧的操作.贪解码是快速的.经典的实现是MaltParser.现代神经版本:陈和曼宁的过渡基于解析器.
  **基于转移的**解析器(arc-eager、arc-standard) 如移进归约解析器一样工作:读进代币,移进到上,应用创建弧的归约动作──贪解码很快──经典实现是MaltParser──现代神经版本:Chen 和 Manning的基于转移的解析器──
- **Graph-based**子 (Eisner 的算法, Dozat-Manning 白) 测量了每一个可能的根部依赖边缘,然后选择最大的跨度树.
  **基于图的**解析器(Eisner 算法、Dozat-Manning 双仿射) 对每个可能的头部依赖 边打分,选择最大生成树──更慢但更准确──

对于大多数应用工作,请拨打 spaCy:

> 对于大多数应用工作,调用空间:

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

阅读`dep`列从下到上,句子的语法结构掉下来.

> 从下往上阅读`dep`列,句子的语法结构就自然呈现了──

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

每个生产NLP图书馆都作为标准管道的一部分运送 POS和依赖性解析器.

> 每个生产NLP库都将 POS 和依赖解析器作为标准流水线的一部分提供.

- **spaCy**(`en_core_web_sm`现在,`md`现在,`lg`现在,`trf`快速,精确,与代币化+NER+Lemmatization集成.`token.tag_`现在,我们要做什么?`token.pos_`其他国家`token.dep_`(依赖关系).
  **spaCy**(`en_core_web_sm`现在,`md`现在,`lg`现在,`trf`快速、准确,与分词 + NER + 词形还原集成。`token.tag_`现在,我们要去做什么?`token.pos_`其他地方`token.dep_`没有什么可能的.
- **Stanford NLP (stanza)**斯坦福大学的继任者,在60多种语言上.
  **Stanford NLP (stanza)**❖ 斯坦福核心NLP的继任者――在60多种语言中达到先进水平――
- **trankit**基于变压器,高度的DD准确性.
  **trankit**基于变压器,良好的 UD 准确率.
- **NLTK**现在,我们要去.`pos_tag`很适合教学,很适合教学.
  **NLTK**,我知道.`pos_tag`可用慢慢较旧适合教学

### 在2026年,这仍然是重要的

- **Lemmatization.**第1课需要POS正确的化.
  **词形还原。**第1课需要 POS 才能正确词形恢复原――始终如此――
- **Structured extraction from LLM outputs.**验证生成的句子是否遵守语法限制 (例如,主题verb协议,要求修改).
  **LLM 输出的结构化抽取。**验证生成的句子满足语法约束 (如主谓一致,必要修饰语)
- **Aspect-based sentiment.**依赖性解析告诉你哪个属性修改哪个名词.
  **基于方面的情感分析。**依赖分析告诉你哪个形容词修饰哪个名词――
- **Query understanding.**"由韦斯安德森导演的电影,由比尔·穆雷主演",通过分析,分解成结构化限制.
  **查询理解。**"由韦斯安德森导演,明星比尔·穆雷主演的电影"
- **Cross-lingual transfer.**语言不了解语言,使得新语言的结构分析能够进行零射击.
  **跨语言迁移。**标签和依赖与语言无关,支持新语言的零样本结构化分析.
- **Low-compute pipelines.**如果您无法运送变压器,
  **低算力流水线。**如果你不能部署变压器,POS+ 依赖分析+ 地名词典能让你走得相当远.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

## 运送它.

保存如`outputs/skill-grammar-pipeline.md`其他:

> 保存为`outputs/skill-grammar-pipeline.md`其他:

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

Refuse to recommend rolling your own parser. Building parsers from scratch is a research project, not an application task. Flag any pipeline that consumes POS tags without handling lowercase/uppercase variants as fragile.
```

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 练习题

1. **Easy.**使用一个小标签组 (例如,NLTK的Brown子组) 上最常见标签基线,测量保留的句子上的准确性. 验证~85%的结果.
   **简单。**在一个小标签语料 (如NLTK的Brow 子集) 上使用最频繁的标签基线,测量在留出句子上的准确率――验证约85%的结果――
2. **Medium.**按每标签的精度/回忆报告.哪些标签最困惑?
   **中等。**训练上述二元组 HMM 并报告每标签精确率/召回率──HMM 最容易混的标签是什么?
3. **Hard.**使用 spaCy 的依赖分析来从1000句的样本中提取主体-动词-对象三倍. 评估50个手动标记的三倍. 抽取失败的文档 (通常是被动,协调和被删除的主体).
   **困难。**使用空间的依赖分析从1000句样本中提取主题三元组. 在50个手动标签的三元组上评估.记录抽取失败的地方.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 关键词 快速查找表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| POS tag（词性标签） | Word's type / 词的类型 | Grammatical category. PTB has 36; UD has 17. / 语法类别。PTB 有 36 个；UD 有 17 个。 |
| Penn Treebank | Standard tagset / 标准标签集 | English-specific. Fine-grained verb tenses and noun number. / 特定于英语。细粒度的动词时态和名词数。 |
| Universal Dependencies（通用依存） | Multilingual tagset / 多语言标签集 | Coarser than PTB; language-neutral; defaults for cross-lingual work. / 比 PTB 更粗；语言无关；跨语言工作的默认选择。 |
| Dependency parse（依存分析） | Sentence tree / 句子树 | Each word has one head, each edge has a grammatical relation. / 每个词有一个中心词，每条边有一个语法关系。 |
| Viterbi（维特比算法） | Dynamic programming / 动态规划 | Finds the highest-probability tag sequence given emissions and transitions. / 给定发射和转移概率，找到最高概率的标签序列。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.

## 继续阅读 继续阅读

- [Jurafsky and Martin — Speech and Language Processing, chapters 8 and 18](https://web.stanford.edu/~jurafsky/slp3/)可教教科书处理 POS和解析. / POS 和解析的经典教科书处理──
- [Universal Dependencies project](https://universaldependencies.org/)每一个多语言解析器使用的跨语言标签集和树库集合.
- [spaCy linguistic features guide](https://spacy.io/usage/linguistic-features) 关于每一个被曝光的属性的实际参考`Token`现在,我们要去.`Token`具体的情况:
- [Chen and Manning (2014). A Fast and Accurate Dependency Parser using Neural Networks](https://nlp.stanford.edu/pubs/emnlp2014-depparser.pdf)将神经解析器带入主流论文.
