# Chunking Strategies for RAG | RAG 分块策略

> Chunking configuration influences retrieval quality as much as the choice of embedding model (Vectara NAACL 2025). Get chunking wrong and no amount of reranking saves you.
> 分块配置对检索质量的影响与嵌入模型的选择一样大（Vectara NAACL 2025）。分块做错，再怎么重排序也救不回来。

> **【中文解读】** RAG 系统中，文档如何切分成块直接影响检索效果。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 22 (Embedding Models), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 22（嵌入模型），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

The fix is not "buy a better embedding model." The fix is to chunk correctly. Vectara's NAACL 2025 paper showed chunking strategy explains as much variance in retrieval quality as embedding choice.

> 修复方法不是 "买个更好的嵌入模型"。修复方法是正确分块。Vectara 的 NAACL 2025 论文表明分块策略解释了与嵌入选择一样多的检索质量差异。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。

Feb 2026 benchmarks show surprising results: naive fixed-size chunking with 100-token chunks and 20-token overlap beats most "intelligent" chunking strategies on general-purpose RAG. Semantic chunking helps on narrative text. Sentence-level chunking helps on FAQ-style content. There is no universal winner.

> 2026 年 2 月基准测试显示了令人惊讶的结果：朴素固定大小分块（100 token 加 20 token 重叠）在通用 RAG 上击败了大多数 "智能" 分块策略。语义分块在叙述性文本上有帮助。句子级分块在 FAQ 风格内容上有帮助。没有万能赢家。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提。

**Fixed-size chunking.** Split text into N-token blocks with optional overlap. Simple, fast, surprisingly effective. The default in most production RAG systems.

> **固定大小分块。** 将文本分割为 N token 的块，可选重叠。简单、快速、出乎意料地有效。大多数生产 RAG 系统的默认。

**Sentence-level chunking.** Split on sentence boundaries. Each chunk = one or more sentences. Good for FAQ and short-answer retrieval.

> **句子级分块。** 在句子边界分割。每个块 = 一个或多个句子。适合 FAQ 和短答案检索。

**Semantic chunking.** Embed sentences, group consecutive sentences with similar embeddings into chunks. Better on narrative text, slower to compute.

> **语义分块。** 嵌入句子，将嵌入相似的连续句子分组为块。在叙述性文本上更好，计算更慢。

**Recursive character chunking.** Split by paragraph, then by sentence, then by character. LangChain's default. Good general-purpose heuristic.

> **递归字符分块。** 按段落分割，然后按句子，然后按字符。LangChain 的默认。好的通用启发式。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。

### Step 1: fixed-size chunking with overlap

```python
def fixed_chunk(text, chunk_size=100, overlap=20):
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunks.append(" ".join(tokens[i:i + chunk_size]))
    return chunks
```

### Step 2: semantic chunking

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

> **【中文解读】** 本节展示如何用成熟框架快速应用该技术。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。

## Use It | 用框架实现

> **【中文解读】** 本节关注如何将模型部署为可用的产品。

| Strategy / 策略 | Chunk size / 块大小 | Best for / 最适合 |
|---------|---------|---------|
| Fixed / 固定 | 100-500 tokens | General purpose / 通用 |
| Sentence / 句子 | 1-3 sentences | FAQ, short answers / FAQ、短答案 |
| Semantic / 语义 | Variable / 可变 | Narrative, long docs / 叙述、长文档 |
| Recursive / 递归 | 500-1500 chars | LangChain default / LangChain 默认 |

## Ship It | 产出物

Save as `outputs/skill-chunking-picker.md`:

> 保存为 `outputs/skill-chunking-picker.md`：

```markdown
Given document type and retrieval task, pick chunking strategy and parameters.
1. Chunking method (fixed, sentence, semantic, recursive).
2. Chunk size and overlap.
3. Evaluation metric (retrieval recall@k, answer quality).
```

## Exercises | 练习题

1. **Easy.** Implement fixed-size chunking with overlap. Measure retrieval quality. / **简单。** 实现固定大小分块。测量检索质量。
2. **Medium.** Compare fixed vs semantic chunking on a narrative dataset. / **中等。** 在叙述数据集上比较固定 vs 语义分块。
3. **Hard.** Build an optimal chunking pipeline that adapts chunk size per document type. / **困难。** 构建按文档类型自适应块大小的最优分块流水线。

## Key Terms | 术语速查表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Chunking（分块） | Splitting documents into retrievable units. / 将文档分割为可检索单元。 |
| Overlap（重叠） | Shared tokens between adjacent chunks. / 相邻块之间的共享 token。 |
| Semantic chunking（语义分块） | Group sentences by embedding similarity. / 按嵌入相似度分组句子。 |

## Further Reading | 延伸阅读

- [Vectara NAACL 2025 chunking study](https://vectara.com/blog/breaking-the-ice-chunking-strategies-for-rag) — chunking benchmark. / 分块基准。
- [LangChain text splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/) — chunking implementations. / 分块实现。
