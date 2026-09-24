# 嵌入式和向量表示

> 文字是离散的.数学是连续的.每次你要求LLM找到"类似"的文件,比较含义,或者搜索超越关键词,你依赖于这两个世界之间的桥梁.那座桥梁是嵌入式.如果你不理解嵌入式,你就不理解现代人工智能.你只是使用它.

> **【中文解读】**文本是离散的,数学是连续的.嵌入式 (嵌入式) 是连接这两个世界的桥梁.

> **【拓展：嵌入→RAG与搜索】**嵌入是RAG (检索增强生成) 系统的核心基础设施.文本转向后存入向量数据库,通过余弦相似性实现语义搜索,这是所有现代人工智能搜索和推系统的基础技术.

>  **【前置】**学本节前请先掌握:(1) Python 基础(numpy 向量运算、字典、列表推导);(2) 高中向量数学点积、角、模长(不知道这些先看 01·02 阶段向量矩阵);(3) 阶段 05·03(Word Embeddings Word2Vec) 会讲词嵌入基础,本节是其延伸到句子/文档级.`numpy`,我知道.`scikit-learn`可选`chromadb`或`qdrant`,我知道.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11, Lesson 01 (Prompt Engineering) | **前置知识:** Phase 11 · 01 (提示工程)
**Time:** ~75 minutes | **时间:** ~75 分钟
**Related:**阶段5 · 22 (嵌入式模型深度潜水) 涵盖密集对稀少对多向量,马特里奥斯卡切割,每个轴模型选择.本课程侧重于生产管道 (向量DB,HNSW,相似数学的). 在选择模型之前阅读阶段5 · 22 .**相关:**阶段 5 · 22 (嵌入模型深度解析) 涵盖密/稀疏/多向量、马特里奥斯卡 截断和分轴模型选择――本课聚焦生产管线(向量库、HNSW、相似度数学) ・选模型前先读 阶段 5 · 22。

## 学习目标

- 使用API提供商和开源模型生成文本嵌入,并计算它们之间的共数相似性
  使用API提供商和开源模型生成文本嵌入,并计算它们之间的余弦相似性
- 解释为什么嵌入式解决了关键字搜索无法处理的词汇不匹配问题
  解释为什么嵌入能解决关键词搜索无法处理的词汇不匹配问题
- 建立一个语义搜索索引,以取出文档的含义而不是精确的关键词匹配
  构建一个语义搜索引,按意义而非精确关键词匹配搜索文档
- 使用检索基准 (precision@k,回忆) 评估嵌入质量,并选择适合您的任务的嵌入模型
  使用检索基准(precision@k、recall) 评估嵌入质量,并为任务选择合适的嵌入模型

> **【中文解读】**本课目的:理解文本嵌入的原理和应用.嵌入将文本转化为向量,使语义相似文本在向量空间中的距离更近.这是语义搜索,RAG,聚类等任务的基础.


## 问题 问题引入

你有1万张支持门票.一个客户写道:"我的付款没有完成".你需要找到类似的过去门票.关键字搜索会找到包含"付款"和"没有完成"的门票.它错过了"交易失败","收费被拒绝",和"账单错误".这些门票描述了完全不同的词汇.

> 你有1万张工单.客户写道:"我的付款没有成功".你需要找到类似的过往工单.关键词搜索找到了包含"支付"和"没有通过"的工单,但丢掉了"交易失败"",收费被拒绝"和"账单错误".这些工单描述完全相同的问题,只是使用完全不同的词.

人类语言有几十种方法来说同样的东西.关键词搜索对待每个词作为一个独立的符号,没有意义.它不能知道"拒绝"和"没有通过"指的是同一个概念.

> 这就是词汇不匹配的问题.人类语言有几种表达相同的方法.

>  **【类比】**关键词搜索像 用"按拼音查字典""水果"和"果"是两条目,彼此找不到.嵌入像"按含义分类""水果""果实""果"都被放进"可食用植物产品"这个语义盒里,能跨语言、跨表达方式匹配. 这就是为什么ChatGPT 能理解你的提议即使你打错字或使用罕见说法.

你需要一个文字的表示,其中意思,而不是拼写,决定相似性. 你需要一种方法,在某个数学空间中将"我的付款没有完成"和"交易被拒绝"放在一个近距离,同时推 "我的付款到达了时间"远远,尽管分享了"付款"这个词.

> 你需要一种方法来表达文本的表达方式,其中的意义而不是拼写决定相似性――你需要一种方法,将"我的付款没有成功"和"交易被拒绝"放在某个数学空间中彼此接近――

这种表现是嵌入式.

> 这种表示就是嵌入.

## 概念的核心概念

> **【中文解读】**嵌入 (嵌入) 将文本转换为高维向量,使语义相似文本在向量空间中距离更近.嵌入是RAG,语义搜索,聚类,分类等任务的基础.

> **【拓展：嵌入模型的演进】**嵌入模型从Word2Vec/GloVe (静态词嵌入) 到BERT (上下文嵌入) 到专用嵌入模型 (如BGE、E5、GTE) ∼OpenAI的文本嵌入-3-大 在MTEB基准上达到约64分钟.嵌入维度通常为768-3072,可以通过Matryoshka 嵌入在推理时截断到更短维度以节省存储.


### 植入是什么?

嵌入式是代表文本的意义的浮点数量的密集向量. "密集"这个词是重要的 - 每个维度都包含信息,而不同于稀疏的表示 (字包,TF-IDF),其中大多数维度都是零.

> 嵌入是表示文本含义的浮点数密向量──"密"很重要每个维度都载有信息,不像稀疏表示(词袋、TF-IDF) 中大多数维度为零──

"猫坐在床上"变成了这样的东西`[0.023, -0.041, 0.087, ..., 0.012]`根据模型,这些数字编码含义.你从来没有直接检查它们.你比较它们.

> "猫坐子上"变成类似的`[0.023, -0.041, 0.087, ..., 0.012]`根据模型不同的是,这是768到3072个数字的列表. 这些数字编码了意义.

###  Word2Vec 突破

2013年,托马斯·米科洛夫和谷歌的同事发表了Word2Vec.核心见解:训练一个神经网络来预测一个词从其邻居 (或邻居从一个词),而隐藏的层重量成为有意义的向量表示.

> 2013年,Tomas Mikolov 及其谷歌同事发表了Word2Vec──核心洞察:训练神经网络从邻居预测一个词(或反过来),隐藏层权重就会变成有意义的向量表示──

著名的结果:

> 著名结果:

```
king - man + woman = queen
```

词嵌入中的矢量算数捕捉了语义关系.从"男人"到"女人"的方向大致与从"国王"到"女王"的方向相同.这是在该领域意识到几何可以编码意义时.

> 词嵌的量算术能捕捉语义关系――"男"到"女人"的方向大致等于"国王"到"女王"的方向――这是意识到几何可以编码含义的时刻――

>  **【类比】**量空间的方向就是"含义维度"――例如某个方向编码"性别" ((男人,女人,王妃,叔叔),另一个方向编码"时态" ((步行,走),第三个编码"复数" ((猫,狗))――模型在训练中自动发现这些方向没有人告诉它"性别"是什么,纯粹从共现统计中出来──300个维度向可能编码了几十种这样的语义轴──

Word2Vec产生了300维向量.每个词都得到了一个向量,不管背景. "河岸"中的"银行"和"银行账户"的嵌入式相同. 这种限制推动了下一个十年的研究.

> 词2Vec 产生300维向量──每一个词无论上下文如何都得到一个向量──"河岸" (河岸) 和"银行账户" (银行账户) 中的"银行" (银行账户) 拥有相同的嵌入式──这一限制驱动了接下来的十年的研究──

### 从单词到句子

字符嵌入代表单个代币. 制作系统需要嵌入整个句子,段落或文档. 出现了四种方法:

> 词嵌表示单个代币――生产系统需要嵌入整个句子、段落或文档――出现了四种方法:

**Averaging**简单的文字,很便宜,很有损失,很好吃. 完全失去了单词顺序. "狗咬人"和"狗咬人"得到相同的嵌入式.

> **平均法**取句子中所有词向量的平均值──廉价──有损,对短文效果是奇怪的──完全丢失词序"狗咬人"和"人咬狗"得到相同的嵌入式──

**CLS token**转换器模型 (BERT, 2018) 输出一个特殊的 [CLS]代币嵌入,代表整个输入.比平均更好,但[CLS]代币被训练为下一句预测,而不是相似性.

> **CLS token**转变器模型 (BERT, 2018) 输出一个特殊的 [CLS]代币 嵌入表示整个输入.比平均法好,但[CLS]代币是为下一句预测任务训练的,不是为相似度任务.

**Contrastive learning**根据"我如何重置密码?"和"我需要更改密码",模型学习这些应该几乎相同的向量.

> **对比学习**显式训练模型将相似于拉近、不相似于推远──Sentence-BERT(Reimers & Gurevych, 2019) 采用这种方法,成为现代嵌入模型的基础──给定"如何重置密码?"和"我需要修改密码",模型学习到它们应该几乎具有相同的向量──

**Instruction-tuned embeddings**模型可以使用一个模特为多个任务服务. 模型可以使用一个模特为多个任务服务.

> **指令微调嵌入**模型接受任务前("搜索_查询:"、"搜索_文档:"),告诉模型产生什么样的嵌入.

```mermaid
graph LR
    subgraph "2013: Word2Vec"
        W1["king"] --> V1["[0.2, -0.1, ...]"]
        W2["queen"] --> V2["[0.3, -0.2, ...]"]
    end

    subgraph "2019: Sentence-BERT"
        S1["How do I reset my password?"] --> E1["[0.04, 0.12, ...]"]
        S2["I need to change my password"] --> E2["[0.05, 0.11, ...]"]
    end

    subgraph "2024: Instruction-Tuned"
        I1["search_query: password reset"] --> T1["[0.08, 0.09, ...]"]
        I2["search_document: To reset your password, click..."] --> T2["[0.07, 0.10, ...]"]
    end
```

### 现代嵌入式模型

根据市场的统计数据,市场已分成数量产品级的选择 (MTEB比分:2026年初,MTEB v2):

> 市场已沉为少数生产阶级选项 ((MTEB 分数为 2026 年初数据,MTEB v2):

| Model | Provider | Dimensions | MTEB | Context | Cost / 1M tokens |
|-------|----------|-----------|------|---------|------------------|
| Gemini Embedding 2 | Google | 3072 (Matryoshka) | 67.7 (retrieval) | 8192 | $0.15 |
| embed-v4 | Cohere | 1024 (Matryoshka) | 65.2 | 128K | $0.12 |
| voyage-4 | Voyage AI | 1024/2048 (Matryoshka) | 66.8 | 32K | $0.12 |
| text-embedding-3-large | OpenAI | 3072 (Matryoshka) | 64.6 | 8192 | $0.13 |
| text-embedding-3-small | OpenAI | 1536 (Matryoshka) | 62.3 | 8192 | $0.02 |
| BGE-M3 | BAAI | 1024 (dense+sparse+ColBERT) | 63.0 multilingual | 8192 | Open-weight |
| Qwen3-Embedding | Alibaba | 4096 (Matryoshka) | 66.9 | 32K | Open-weight |
| Nomic-embed-v2 | Nomic | 768 (Matryoshka) | 63.1 | 8192 | Open-weight |

MTEB (大规模文本嵌入基准) v2涵盖100多项任务,包括检索,分类,集群,重新排名和总结. 较高就更好. 到2026年,开放式型号 (Qwen3-Embedding, BGE-M3) 在大多数轴上匹配或超过封闭主机型号. 双子座嵌入2带来了纯粹的检索;旅行/Cohere带来了特定领域 (金融,法律,代码). 在做出承诺之前,总是根据自己的问题进行基准.

> MTEB(大体文本嵌入基准) v2 涵盖检索,分类,聚类,重排和摘要等100+个任务.分数越高越好.至2026年,开源权重模型(Qwen3-Embedding、BGE-M3) 大多数维度上匹配或超越闭源托管模型.

### 类似度指标

鉴于两个嵌入向量,测量它们的相似性有三个方法:

> 给出两个嵌入式向量,有三种方法来衡量它们的相似性:

**Cosine similarity**视角:两个向量之间的角的共数.从 -1 (相反) 到 1 (相同的方向). 忽略大小 - 10 字句和 500 字文档可以得到 1.0 如果它们指向相同的方向.这是 90% 的使用案例的默认.

> **余弦相似度**两个向量间角的余弦值──范围 -1(相反) 到 1(同向) ──忽略幅度10 词句和500 词文档若指向同一方向可得分 1.0──这是90%场景的默认选择──

>  **【困惑】**问:为什么大多数场景使用余弦相似度而不是欧氏距离? A: 因为嵌入向量的"长度" (长度) 通常没有意义 同句话用10字或100字说,含义一样但向量长度可能差很多。余弦只看"方向"",对长度不敏感,所以更适合"含义方向"――欧氏距离会让长文档看起来很远"但其实它讲的是同一件事──

```
cosine_sim(a, b) = dot(a, b) / (||a|| * ||b||)
```

**Dot product**微分数是两个向量的原始内部产物.当向量正常化时与可西因相似 (单位长度).计算更快.OpenAI的嵌入式是正常化的,因此点产物和可西因都得到相同的排名.

> **点积**两个向量的原始内积──当向量归结时 (单位长度) 当等于余弦相似度──计算更快──OpenAI的嵌入已经归结,所以点积和余弦给出相同排名──

```
dot(a, b) = sum(a_i * b_i)
```

**Euclidean (L2) distance**微小 = 类似. 敏感于大小差异. 使用当空间中的绝对位置重要时,而不是仅仅是方向.

> **欧氏（L2）距离**空间中的直线距离――越小越相似――对幅差异敏感――当空间中的绝对位置――不仅是方向 (重要时使用――

```
L2(a, b) = sqrt(sum((a_i - b_i)^2))
```

什么时候使用:

> 什么时候用什么种:

| Metric | Use when | Avoid when |
|--------|----------|------------|
| Cosine similarity / 余弦相似度 | Comparing texts of different lengths; most retrieval tasks / 比较不同长度文本；大多数检索任务 | Magnitude carries information / 幅度携带信息 |
| Dot product / 点积 | Embeddings are already normalized; maximum speed / 嵌入已归一化；最大化速度 | Vectors have varying magnitudes / 向量幅度不同 |
| Euclidean distance / 欧氏距离 | Clustering; spatial nearest-neighbor problems / 聚类；空间近邻问题 | Comparing documents of wildly different lengths / 比较长度悬殊的文档 |

### 矢量数据库和HNSW

根据"大力相似性搜索"的数据,每一个存储的向量都会对比到一个问题.

> 暴力相似度搜索将查询与每个存储的向量比较――100万向量,1536维情况下,每次查询需要15亿次加运算――太慢――

矢量数据库使用近邻近近邻 (ANN) 算法解决这一问题.主导算法是HNSW (层次导航小世界):

> 为了解决这个问题,使用近似近邻的数据库.

1. 构建一个多层的向量图
   构建向量的多层图
2. 顶层是稀疏的 - - 远程的连接
   顶层稀疏远距离之间长程连接
3. 底层密集,附近的向量之间有细粒度的连接.
   底层密邻近向量之间的细粒度连接
4. 搜索从顶层开始,贪地下降到精炼
   搜索从顶层开始,贪下降以精确化
5. 返回大约在 O(log n) 时间中的 top-k结果,而不是 O(n)
   在 O  没有 O  时间内回归近似的顶点结果

在10万向量时,粗 lực需要几秒钟.在HNSW需要几毫秒.

> 由于这种情况,HNSW的精度损失通常是95%到99%的回报率,而HNSW的速度却会大幅上升.

>  **【类比】**像地图搜索:"全国地图"只画大城市(顶层稀疏),省地图"画到县城(中层),街地图"画到每个建筑物(底层密) ・找"北京大学"时,先在全国层跳到北京(一次大跳),再在省层跳到海区(中跳),最后在街层找到具体位置(小跳) ・比一一楼挨查查快几个数量级.

```mermaid
graph TD
    subgraph "HNSW Layers"
        L2["Layer 2 (sparse)"] -->|"long jumps"| L1["Layer 1 (medium)"]
        L1 -->|"shorter jumps"| L0["Layer 0 (dense, all vectors)"]
    end

    Q["Query vector"] -->|"enter at top"| L2
    L0 -->|"nearest neighbors"| R["Top-k results"]
```

> ️ **【易错点】**美国海军陆战队的3个坑:**召回率随参数变化** `ef_construction`太低(< 100) 会导致图结构质量差,召回率下降到70%以下;生产建议200-500──(2) **删除代价高**HNSW 是图结构,删节点会破坏连接,多数实现是"软删除" (标记为已删除),需要定期重建 (重建).**过滤性能差**首先做量搜索再过会得到大量不符合条件的结果;解决方案:使用Qdrant的过搜索或Pinecone的稀密混合物,先过再搜索.

生产选择:

> 生产级选项:

| Database | Type | Best for | Max scale |
|----------|------|----------|-----------|
| Pinecone | Managed SaaS / 托管 SaaS | Zero-ops production / 零运维生产 | Billions / 十亿级 |
| Weaviate | Open source / 开源 | Self-hosted, hybrid search / 自托管、混合搜索 | 100M+ / 一亿+ |
| Qdrant | Open source / 开源 | High performance, filtering / 高性能、过滤 | 100M+ / 一亿+ |
| ChromaDB | Embedded / 嵌入式 | Prototyping, local dev / 原型、本地开发 | 1M / 百万 |
| pgvector | Postgres extension / Postgres 扩展 | Already using Postgres / 已在用 Postgres | 10M / 千万 |
| FAISS | Library / 库 | In-process, research / 进程内、研究 | 1B+ / 十亿+ |

### 碎策略

文件太长了,不能作为单个向量嵌入. 50页的PDF涵盖了数十个主题. 它的嵌入成为所有东西的平均值,类似于什么也没有具体的.

> 文档太长,无法作为单个向量嵌入. 50页的PDF 涵盖几十个主题.其嵌入成所有内容的平均,与任何具体内容都不相似.

**Fixed-size chunking**简单且可预测. 文件没有清晰的结构时,它可以很好地运作. 具有512个代币的部分,具有50个代币的重叠:第1个部分是代币0-511,第2个部分是代币462-973.

> **固定大小分块**标签: 每个 N 个代币 拆分一次,带 M 个代币 重叠――简单可预测――文档无清晰结构时效果好――512 代币 分块加 50 个代币 重叠:块 1 是代币 0-511,块 2 是代币 462-973――

**Sentence-based chunking**单词的分数是:分为句子边界,把句子组合在一起,直到达到标志性限度.每一个部分至少是一个完整的句子.

> **基于句子的分块**在句子边界分开,分组句子直到达到标志上限. 每块至少有一个完整的句子.

**Recursive chunking**试试在最大边界 (区块标题) 上分开.如果仍然太大,试试段界.然后句子界限.然后字符界限.这是LangChain的.`RecursiveCharacterTextSplitter`对于混合格式的体体来说,它很好.

> **递归分块**首先在最大边界,然后字符限制.这是长链的.`RecursiveCharacterTextSplitter`对于混合语料的效果好.

**Semantic chunking**嵌入式的相似性下降到门以下时,开始一个新的部分.昂贵 (需要单独嵌入每个句子),但产生最一致的部分.

> **语义分块**嵌入每个句子,然后将嵌入相似连续句子分组. 当嵌入相似度低于值时,开始新块.

| Strategy | Complexity | Quality | Best for |
|----------|-----------|---------|----------|
| Fixed-size / 固定大小 | Low / 低 | Decent / 尚可 | Unstructured text, logs / 非结构化文本、日志 |
| Sentence-based / 基于句子 | Low / 低 | Good / 好 | Articles, emails / 文章、邮件 |
| Recursive / 递归 | Medium / 中 | Good / 好 | Markdown, HTML, mixed docs / Markdown、HTML、混合文档 |
| Semantic / 语义 | High / 高 | Best / 最佳 | Critical retrieval quality / 关键检索质量 |

对于大多数系统来说,最好的点是256-512个代币块,

> 大多数系统的最佳点:256-512代币块加50代币重叠

> ️ **【易错点】**分块的3个实战坑:**块太大**嵌被稀释,每个块都"既像A 又像B",检索精度暴跌;-指规则:不超过模型最大输入的 1/4──(2) **块太小**上下文丢失,"它"指代的前文消失,嵌入成无意义的噪音――(3) **重叠设为 0**边界处关键句被切断,例如"... 不要――**删除**这个文件──"可能被切成两个块里,搜索"删除文件"找不到匹配──修复:始终设 10-20%的重叠──

### 双编码器与交叉编码器

双编码器独立嵌入查询和文件,然后比较向量.快速 - - 你嵌入查询一次,然后与预先计算的文件嵌入进行比较.这是你用于检索的.

> 双编码器独立嵌入查询和文件,然后比较向量――快速你只嵌入查询一次,与预计算的文件嵌入比较――这是查询时使用的方案――

交叉编码器将查询和文档作为单个输入,并输出相关性分数.慢 - 它通过完整模型处理每个查询-文档对. 但更准确,因为它可以同时处理查询和文档代币.

> 交叉编码器将查询和文档作为单个输入,输出相关性分数.慢它通过完整模型处理每个查询-文档对应.

生产模式:双编码器检索前100名候选人,跨编码器将他们排名至前10名.

> 生产模式:双编码器检索前-100候选人,交叉编码器重排为前-10――这就是先检索后重排管线――

> ️ **【易错点】**性能灾难:直接使用跨编码器进行检查. 一百万文档意味着每次查询需要做一百万次完整的变压器前进通行.**永远用 Bi-Encoder 召回 + Cross-Encoder 重排**‧ 跨编码器只对前100名候选人运行100次,毫秒级完成──这个组合是BGE、Cohere Rerank等所有生产RAG系统的标准做法──

```mermaid
graph LR
    Q["Query"] --> BE["Bi-Encoder: embed query"]
    BE --> VS["Vector search: top 100"]
    VS --> CE["Cross-Encoder: rerank"]
    CE --> R["Top 10 results"]
```

排名模型:Cohere Rerank 3.5 (每1000个查询每2美元),BGE-reranker-v2 (免费,开源),Jina Reranker v2 (免费,开源).

> 排行榜:Cohere Rerank 3.5(每1000个查询 $2) ‧BGE-renanker-v2(免费、开源) ‧Jina Reranker v2(免费、开源) ‧

### 马特里奥斯卡嵌入式

传统的嵌入式是全部或什么都没有.一个1536维向量使用1536个浮动.你不能在没有重新训练的情况下切断到256维度.

> 传统嵌入不就是此即彼的──1536 维向量使用 1536 个浮点数──不重新训练就无法截截至 256 维──

>  **【困惑】**问:Matryoshka 嵌入的"截断"是什么意思?为什么要做? A:类比俄罗斯套娃 (Matryoshka doll) 大套娃里套小套娃,前 256 维是"最重要的含义" (小套娃),加上 768 维是"中等细节",加上 1536 维是"完整精细含义" (最大套娃) ⋅模型训练时被强制让前 N 维也能工作.**收益**储存省 6 倍(1536→256),检索快 6 倍,精度只掉 1-3 个点──RAG 系统常用 256 维存向量 + 1536 维重排,兼顾速度和精度──

马特里奥斯卡表示学习 (Kusupati等, 2022) 解决了这一问题.该模型训练以使第一个N维度捕获最重要的信息,就像俄罗斯的巢穴娃娃.将1536d的马特里奥斯卡嵌入到256维度的切断会失去一些准确性,但仍然是功能性的.

> 马特里奥斯卡表示学习(Kusupati 等人 2022) 修复了这个点――模型训练成前N维捕获最重要的信息,像俄罗斯套娃──把1536维马特里奥斯卡嵌入截截至256维会损失一些精度但仍然可用──

通过                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            `dimensions`要求256个维度而不是1536个维度将存储量减少6倍,在MTEB基准上约有3-5%的准确性损失.

> 通过 OpenAI 的文字嵌入3小 和文字嵌入3大`dimensions`参数支持马特里奥斯卡 截断――要求 256维而不是 1536维将减少存储 6倍,在MTEB基准上损失约 3-5% 精度――

### 双数量化

作为 float32 存储的1536维嵌入式使用了6,144个字节.乘以1000万份文件:仅仅为向量为61GB.

> 存储量为 6,144 字节.

双数量化将每个浮动数量转换为单位数:正值变为1,负值变为0.存储量从6,144字节降至192字节 - 这意味着32倍的减少.类似性是使用汉密距离计算的 (数分不同位数), CPU可以在单个指示中完成.

> 二值量化将每个浮点数量转换为单个比特:正值变 1,负值变 0. 储存从 6,144 字节降至 192 字节32 倍压缩.

检索回忆时,准确度达到5-10%. 常见模式是:对数百万向量进行首次通过搜索的二进制量化,然后使用完全精确的向量重新排列前1000. 这使您获得了95%+的完全精确度,并且存储量减少了32倍.

> 检索召回率精度损失约5-10%──常见模式:使用二值量化做百万向量一次搜索,然后使用全精度向量对顶1000重排──这让你在32倍少内存下获得95%+的全精度精度──

## 建立它,实现它.
```figure
cosine-similarity
```

## 建立它

我们从零开始构建了一个语义搜索引擎.没有向量数据库.没有外部嵌入API.纯Python和数学的numpy.

> 我们从零开始构建语义搜索引擎――不用向量数据库,不用外部嵌入API――纯Python加 numpy做数学运算――

### 步骤1: 删除文字

```python
def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def chunk_by_sentences(text, max_chunk_tokens=200):
    sentences = text.replace("\n", " ").split(".")
    sentences = [s.strip() + "." for s in sentences if s.strip()]
    chunks = []
    current_chunk = []
    current_length = 0
    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length > max_chunk_tokens and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(sentence)
        current_length += sentence_length
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks
```

### 步骤2:从零开始构建嵌入式

我们使用TF-IDF实现了简单的密集嵌入式,并使用L2正常化.这不是神经嵌入式,但它遵循相同的合同:文字进,固定尺寸的向量出,类似的文本产生类似的向量.

> 我们使用L2归化TF-IDF实现简单的密嵌入.

```python
import math
import numpy as np
from collections import Counter

class SimpleEmbedder:
    def __init__(self):
        self.vocab = []
        self.idf = []
        self.word_to_idx = {}

    def fit(self, documents):
        vocab_set = set()
        for doc in documents:
            vocab_set.update(doc.lower().split())
        self.vocab = sorted(vocab_set)
        self.word_to_idx = {w: i for i, w in enumerate(self.vocab)}
        n = len(documents)
        self.idf = np.zeros(len(self.vocab))
        for i, word in enumerate(self.vocab):
            doc_count = sum(1 for doc in documents if word in doc.lower().split())
            self.idf[i] = math.log((n + 1) / (doc_count + 1)) + 1

    def embed(self, text):
        words = text.lower().split()
        count = Counter(words)
        total = len(words) if words else 1
        vec = np.zeros(len(self.vocab))
        for word, freq in count.items():
            if word in self.word_to_idx:
                tf = freq / total
                vec[self.word_to_idx[word]] = tf * self.idf[self.word_to_idx[word]]
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec
```

### 步骤3:相似性功能

```python
def cosine_similarity(a, b):
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot / (norm_a * norm_b))


def dot_product(a, b):
    return float(np.dot(a, b))


def euclidean_distance(a, b):
    return float(np.linalg.norm(a - b))
```

### 步骤4:使用粗力搜索的向量指数

```python
class VectorIndex:
    def __init__(self):
        self.vectors = []
        self.texts = []
        self.metadata = []

    def add(self, vector, text, meta=None):
        self.vectors.append(vector)
        self.texts.append(text)
        self.metadata.append(meta or {})

    def search(self, query_vector, top_k=5, metric="cosine"):
        scores = []
        for i, vec in enumerate(self.vectors):
            if metric == "cosine":
                score = cosine_similarity(query_vector, vec)
            elif metric == "dot":
                score = dot_product(query_vector, vec)
            elif metric == "euclidean":
                score = -euclidean_distance(query_vector, vec)
            else:
                raise ValueError(f"Unknown metric: {metric}")
            scores.append((i, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in scores[:top_k]:
            results.append({
                "text": self.texts[idx],
                "score": score,
                "metadata": self.metadata[idx],
                "index": idx
            })
        return results

    def size(self):
        return len(self.vectors)
```

### 步骤5:语义搜索引擎

```python
class SemanticSearchEngine:
    def __init__(self, chunk_size=200, overlap=50):
        self.embedder = SimpleEmbedder()
        self.index = VectorIndex()
        self.chunk_size = chunk_size
        self.overlap = overlap

    def index_documents(self, documents, source_names=None):
        all_chunks = []
        all_sources = []
        for i, doc in enumerate(documents):
            chunks = chunk_text(doc, self.chunk_size, self.overlap)
            all_chunks.extend(chunks)
            name = source_names[i] if source_names else f"doc_{i}"
            all_sources.extend([name] * len(chunks))
        self.embedder.fit(all_chunks)
        for chunk, source in zip(all_chunks, all_sources):
            vec = self.embedder.embed(chunk)
            self.index.add(vec, chunk, {"source": source})
        return len(all_chunks)

    def search(self, query, top_k=5, metric="cosine"):
        query_vec = self.embedder.embed(query)
        return self.index.search(query_vec, top_k, metric)

    def search_with_scores(self, query, top_k=5):
        results = self.search(query, top_k)
        return [
            {
                "text": r["text"][:200],
                "source": r["metadata"].get("source", "unknown"),
                "score": round(r["score"], 4)
            }
            for r in results
        ]
```

### 步骤 6: 进行相似度量测量

```python
def compare_metrics(engine, query, top_k=3):
    results = {}
    for metric in ["cosine", "dot", "euclidean"]:
        hits = engine.search(query, top_k=top_k, metric=metric)
        results[metric] = [
            {"score": round(h["score"], 4), "preview": h["text"][:80]}
            for h in hits
        ]
    return results
```

## 用它实现框架

通过生产嵌入式API,架构保持相同.只有嵌入器改变:

> 使用生产级嵌入API 时,架构完全相同.

```python
from openai import OpenAI

client = OpenAI()

def openai_embed(texts, model="text-embedding-3-small", dimensions=None):
    kwargs = {"model": model, "input": texts}
    if dimensions:
        kwargs["dimensions"] = dimensions
    response = client.embeddings.create(**kwargs)
    return [item.embedding for item in response.data]
```

通过OpenAI进行缩,相同的模型,尺寸较小,存储量较低:

> 使用OpenAI的Matryoshka 截断同样的模型,更少维度,更低存储:

```python
full = openai_embed(["semantic search query"], dimensions=1536)
compact = openai_embed(["semantic search query"], dimensions=256)
```

对于1000万份文件,这相当于10GB对61GB.标准基准标准的准确性损失大约为3-5%.

> 对于1000万文档,就是10GB对61GB的精度损失在标准基准上约为3-5%的度损失.

为了重新排名科赫:

> 使用Cohere 重排:

```python
import cohere

co = cohere.ClientV2()

results = co.rerank(
    model="rerank-v3.5",
    query="What is the refund policy?",
    documents=["Full refund within 30 days...", "No refunds after 90 days..."],
    top_n=3
)
```

对于没有API依赖的本地嵌入式:

> 没有API,依赖于:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
embeddings = model.encode(["semantic search query", "another document"])
```

它们可以使用任何一个类型, 换个嵌入函数, 保持搜索逻辑.

> 我们构建的矢量索引类型可与上述任意方案配合,换嵌入函数,保留搜索逻辑.

## 运送它.

这一课产生了:
- `outputs/prompt-embedding-advisor.md`-- 针对特定使用情况的嵌入模型和战略的提示
  选择嵌入模型和策略 (针对具体场景) 的提示
- `outputs/skill-embedding-patterns.md`能教导代理人如何有效地使用嵌入式产品
  教导代理 如何有效地在生产中使用嵌入式技能

## 练习题

1. **Metric comparison**根据测量结果,测量结果是不同于测量结果的,为什么?
   **指标比较**查询:对样本文档使用余弦相似度,点积和欧氏距离运行的相同 5 查询.记录每种的前3 结果.

2. **Chunk size experiment**查看数据库的数据库:以50个,100个,200个,500个字的分类大小进行索引.每一个,运行5个查询,记录前1个相似度分数.绘制分类大小和检索质量的关系.找到较大的分类开始疼痛的地方.
   **分块大小实验**通过50、100、200、500 字的块大小索引样本文档.

3. **Matryoshka simulation**简单的缩器可以产生500d向量. 切断到50,100,200和500维度. 测量每次切断时检索回忆如何降低. 这模拟了Matryoshka行为,而无需真正的训练技巧.
   **Matryoshka 模拟**构建产生500维向量的简单Embedder──截至50、100、200、500维──测量每次截止下检索召回率如何下降──这模拟了马特里奥斯卡的行为而无需真实训练技巧──

4. **Binary quantization**搜索引擎中的嵌入式,将它们转换为二进制 (1如果是正,如果是负),并执行哈密距离搜索. 根据完全精确的共数相似性进行比较. 测量重叠百分比.
   **二值量化**搜索引擎中的嵌入,转为二进制(正为1,负为0),实现汉明距离搜索――对比前十 结果与全精度余弦相似度――测量重叠百分比――

5. **Sentence-based chunking**: 取代固定尺寸的碎片`chunk_by_sentences`按照句子界限来改善结果吗?
   **基于句子的分块**将固定大小分块替换为`chunk_by_sentences`◎运行相同查询,比较检索分数――尊重句子边界是否改善结果?

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Embedding | "Text to numbers" | A dense vector where geometric proximity encodes semantic similarity | 嵌入：稠密向量，几何邻近编码语义相似度 |
| Word2Vec | "The OG embedding" | 2013 model that learned word vectors by predicting context words; proved vector arithmetic encodes meaning | Word2Vec：2013 年模型，通过预测上下文词学习词向量；证明向量算术编码含义 |
| Cosine similarity | "How similar are two vectors" | Cosine of the angle between vectors; 1 = identical direction, 0 = orthogonal, -1 = opposite | 余弦相似度：向量夹角余弦；1=同向，0=正交，-1=反向 |
| HNSW | "Fast vector search" | Hierarchical Navigable Small World graph -- multi-layer structure enabling O(log n) approximate nearest neighbor search | HNSW：层次可导航小世界图——多层结构实现 O(log n) 近似最近邻搜索 |
| Bi-encoder | "Embed separately, compare fast" | Encodes query and document independently into vectors; enables pre-computation and fast retrieval | 双编码器：独立编码查询和文档为向量；允许预计算和快速检索 |
| Cross-encoder | "Slow but accurate reranker" | Processes query-document pair jointly through the full model; higher accuracy, no pre-computation | 交叉编码器：联合处理查询-文档对；更高精度，无法预计算 |
| Matryoshka embeddings | "Truncatable vectors" | Embeddings trained so the first N dimensions capture the most important information, enabling variable-size storage | Matryoshka 嵌入：训练使前 N 维捕获最重要信息，支持变维存储 |
| Binary quantization | "1-bit embeddings" | Converting float vectors to binary (sign bit only) for 32x storage reduction with Hamming distance search | 二值量化：将浮点向量转为二进制（仅符号位）实现 32 倍存储压缩配汉明距离搜索 |
| Chunking | "Split docs for embedding" | Breaking documents into 256-512 token segments so each can be independently embedded and retrieved | 分块：将文档拆分为 256-512 token 段以便独立嵌入和检索 |
| Vector database | "Search engine for embeddings" | Data store optimized for storing vectors and performing approximate nearest neighbor search at scale | 向量数据库：为存储向量和大规模近似最近邻搜索优化的数据存储 |
| Contrastive learning | "Train by comparison" | Training approach that pushes similar pair embeddings together and dissimilar pair embeddings apart | 对比学习：将相似对嵌入拉近、不相似对推远的训练方法 |
| MTEB | "The embedding benchmark" | Massive Text Embedding Benchmark -- 56 datasets across 8 tasks; standard for comparing embedding models | MTEB：大规模文本嵌入基准——8 任务 56 数据集；比较嵌入模型的标准 |

## 继续阅读 继续阅读

- 微洛夫等人",在矢量空间中的词表表的有效估算" (2013) -- 开始了与国王-女王比喻的嵌入革命的Word2Vec论文
  迈科洛夫等,"向量空间中的词表达的有效估算" (2013) 启动嵌入革命的 Word2Vec 论文,提出了国王-女王类比
- 雷默斯和古雷维奇, "Sentence-BERT:使用西安式BERT网络的句子嵌入" (2019) --如何训练双码码器以实现句子级别的相似性,现代嵌入模型的基础
  雷默斯和古雷维奇,"Sentence-BERT" (新年) 如何为句子级相似度训练双编码器,现代嵌入模型的基础
- 库苏帕蒂等人",马特里奥斯卡表示学习" (2022) - - OpenAI采用的变量化嵌入技术3
  变维嵌入后背的技术,OpenAI在文本嵌入-3中采用
- 马尔科夫和雅舒宁, "使用层次导航式小世界图表的最接近邻居" (2018) -- HNSW 论文,大多数生产向量搜索背后的算法
  马尔科夫和雅舒宁,"HNSW" (HNSW 2018) HNSW 论文,大多数生产向量搜索背后的算法
- 开放AI嵌入式指南 (platform.openai.com/docs/guides/embeddings) - - 包括Matryoshka尺寸缩小在内的文本嵌入式-3模型的实用参考
  开放AI 嵌入指南文本嵌入-3 模型的实用参考,包括Matryoshka 降维
- MTEB 领袖板 (huggingface.co/spaces/mteb/leaderboard) - - 现场比较所有嵌入式模型在任务和语言中
  MTEB 排行榜跨任务和语言比较所有嵌入模型的实时基准
- [Muennighoff et al., "MTEB: Massive Text Embedding Benchmark" (EACL 2023)](https://arxiv.org/abs/2210.07316)-- 排名表报告的8项任务类别 (分类,聚类,对分类,重新排名,检索,STS,总结,Bitext挖掘) 的基准;在信任任何单一的MTEB分数之前阅读.
  尼戈夫等,"MTEB"(EACL 2023) 定义了8个任务类别的基准;信任任何单一的MTEB 分数前必读.
- [Sentence Transformers documentation](https://www.sbert.net/)两码码器与跨码码器的可信参考, 汇集策略,
  文档 文档 双编码器 VS 交叉编码器 池化策略和本课程实现的摄取拆分嵌入存储RAG管线的权力参考
