# 为了让我们可以找到一个好方法

> 碎配置对检索质量的影响与嵌入模型的选择一样 (Vectara NAACL 2025). 错误碎,没有重排可以挽救您.
> 分块配置对检查质量的影响与嵌入模型的选择一样大.

> **【中文解读】**在RAG系统中,文档如何分成块直接影响检索效果.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 22 (Embedding Models), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 22（嵌入模型），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## 问题 问题引入

维克塔拉的NAACL 2025论文显示,缩策略解释了检索质量的差异和嵌入选择.

> 修复方法不是"买个更好的嵌入模型"――修复方法是正确分块――Vectara的NAACL 2025论文表明分块策略解释了与嵌入选择一样多的检查质量差异――

> **【中文解读】**本节提出的问题是:如何正确理解和应用这一技术在实际工程中.

2026年2月的基准显示出令人惊的结果:无明的固体尺寸的零碎,100个代币零碎和20个代币重叠,超过了一般用途RAG上的大多数"智能"的零碎策略.语义零碎有助于叙事文本.句子级零碎有助于FAQ类型的内容.没有通用获胜者.

> 2026年2月基准测试显示出惊人的结果:朴素固定大小分块(100代币加上20代币重叠) 在通用RAG上击败了大多数"智能"分块策略──语义分块在叙述性文本中有帮助──句子级分块在FAQ风格内容中有帮助──没有万能赢家──

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提.

**Fixed-size chunking.**文字分为N代码块,可选重叠. 简单,快速,令人惊的有效. 在大多数生产RAG系统中默认.

> **固定大小分块。**将文本分为N代币的块,可选重叠――简单,快速,意料地有效――大多数生产RAG系统的默认――

**Sentence-level chunking.**按句子边界划分. 每个部分 = 一个或多个句子. 好用于查询问题和短答复.

> **句子级分块。**在句子边界分开――每个块 = 一个或多个句子――适合FAQ和短答案检查――

**Semantic chunking.**嵌入句子,组合类似嵌入的连续句子成块.

> **语义分块。**嵌入句子,将嵌入类似连续句子分组为块.

**Recursive character chunking.**按段落,然后按句子,然后按字符. 长链的默认.

> **递归字符分块。**按段落分,然后按句子,然后按字符──长链的默认──好通用启发式──

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构.

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.
```figure
n5-chunk-cuts
```

## 建立它

## 建立它,实现它.

> **【中文解读】**本节通过代码从零实现核心算法.

### 步骤1:固定尺寸的重叠零碎

```python
def fixed_chunk(text, chunk_size=100, overlap=20):
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunks.append(" ".join(tokens[i:i + chunk_size]))
    return chunks
```

### 步骤2:语义分断

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def semantic_chunk(text, model_name="sentence-transformers/all-MiniLM-L6-v2", threshold=0.5):
    model = SentenceTransformer(model_name)
    sentences = text.split(". ")
    embeddings = model.encode(sentences, normalize_embeddings=True)
    chunks = [sentences[0]]
    for i in range(1, len(sentences)):
        sim = np.dot(embeddings[i], embeddings[i-1])
        if sim < threshold:
            chunks.append(sentences[i])
        else:
            chunks[-1] += ". " + sentences[i]
    return chunks
```

> **【中文解读】**本节展示了如何使用成熟框架快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能.

## 用它实现框架

> **【中文解读】**本节关注如何将模型部署为可用产品.

| Strategy / 策略 | Chunk size / 块大小 | Best for / 最适合 |
|---------|---------|---------|
| Fixed / 固定 | 100-500 tokens | General purpose / 通用 |
| Sentence / 句子 | 1-3 sentences | FAQ, short answers / FAQ、短答案 |
| Semantic / 语义 | Variable / 可变 | Narrative, long docs / 叙述、长文档 |
| Recursive / 递归 | 500-1500 chars | LangChain default / LangChain 默认 |

## 运送它.

保存如`outputs/skill-chunking-picker.md`其他:

> 保存为`outputs/skill-chunking-picker.md`其他:

```markdown
Given document type and retrieval task, pick chunking strategy and parameters.
1. Chunking method (fixed, sentence, semantic, recursive).
2. Chunk size and overlap.
3. Evaluation metric (retrieval recall@k, answer quality).
```

## 练习题

1. **Easy.**实施固定尺寸的重叠分断,测量检索质量. / **简单。**实现固定大小分块――测量检索质量――
2. **Medium.**在叙述数据集中,比较固定与语义分量.**中等。**在叙述数据集中比较固定与语义分块.
3. **Hard.**建立一个最佳的零件管道,以适应每份文件类型的零件尺寸. / **困难。**根据文档类型自适应块大小的最优分块流水线.

## 关键词 快速查找表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Chunking（分块） | Splitting documents into retrievable units. / 将文档分割为可检索单元。 |
| Overlap（重叠） | Shared tokens between adjacent chunks. / 相邻块之间的共享 token。 |
| Semantic chunking（语义分块） | Group sentences by embedding similarity. / 按嵌入相似度分组句子。 |

## 继续阅读 继续阅读

- [Vectara NAACL 2025 chunking study](https://vectara.com/blog/breaking-the-ice-chunking-strategies-for-rag)分块基准.
- [LangChain text splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)分块实现.
