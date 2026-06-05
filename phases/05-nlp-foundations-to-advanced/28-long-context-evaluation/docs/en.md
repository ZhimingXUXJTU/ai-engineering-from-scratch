# Long-Context Evaluation — NIAH, RULER, LongBench, MRCR | 长上下文评估 — NIAH、RULER

> Gemini 3 Pro advertises 10M tokens of context. At 1M tokens, 8-needle MRCR drops to 26.3%. Advertised ≠ usable. Long-context evaluation tells you the actual capacity of the model you are shipping on.
> Gemini 3 Pro 宣称 10M token 上下文。在 1M token 时，8-needle MRCR 降到 26.3%。宣称的 ≠ 可用的。长上下文评估告诉你你正在部署的模型的实际能力。

> **【中文解读】** 评估 LLM 在长上下文窗口中的实际表现。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 27 (LLM Evaluation) | **前置知识:** Phase 5 · 27（LLM 评估）
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

This is the 2026 context-capacity gap. Spec sheets say 1M tokens. Benchmarks say: at 100K tokens, retrieval accuracy drops 15-40%. At 500K, it drops 40-70%. The model does not actually "see" everything in its context window equally.

> 这是 2026 年的上下文容量差距。规格表说 1M token。基准说：在 100K token 时，检索准确率下降 15-40%。在 500K 时，下降 40-70%。模型并非在其上下文窗口中同等地 "看到" 所有内容。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。

Long-context evaluation measures these axes: retrieval accuracy at various depths, multi-hop reasoning across documents, and aggregation over distributed information.

> 长上下文评估测量这些轴：各种深度的检索准确率、跨文档的多跳推理、以及对分布信息的聚合。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。

**NIAH (Needle in a Haystack).** Insert a specific fact into a long document at various positions. Ask the model to retrieve it. Measures: can the model find a needle at depth X in a Y-token haystack?

> **NIAH（大海捞针）。** 在长文档的各个位置插入特定事实。让模型检索。测量：模型能否在 Y token 的干草堆中深度 X 处找到针？

**RULER.** Extends NIAH with multi-needle, variable-distance, and aggregation tasks. More comprehensive.

> **RULER。** 扩展 NIAH 添加多针、可变距离和聚合任务。更全面。

**LongBench.** Real-world long-context tasks: summarization, QA, retrieval, code. More representative than synthetic benchmarks.

> **LongBench。** 真实长上下文任务：摘要、问答、检索、代码。比合成基准更具代表性。

**MRCR (Multi-hop Reasoning over Context).** Reasoning that requires connecting information across multiple documents. The hardest long-context test.

> **MRCR（上下文多跳推理）。** 需要跨多个文档连接信息的推理。最难的长上下文测试。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了范式转变。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。

### Step 1: simple NIAH test

```python
def needle_in_haystack(model, context_length, needle, needle_position):
    """Insert needle at position in a long document and test retrieval."""
    haystack = generate_irrelevant_text(context_length)
    full_text = haystack[:needle_position] + f"\n{needle}\n" + haystack[needle_position:]
    question = f"What is the secret fact hidden in the text?"
    response = model(full_text + "\n\n" + question)
    return needle.lower() in response.lower()
```

> **【中文解读】** 本节展示如何用成熟框架快速应用该技术。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。

## Use It | 用框架实现

> **【中文解读】** 本节关注如何将模型部署为可用的产品。

| Benchmark / 基准 | Type / 类型 | Measures / 测量 |
|---------|------|---------|
| NIAH | Synthetic / 合成 | Single-fact retrieval at depth. / 深度单事实检索。 |
| RULER | Synthetic / 合成 | Multi-needle + aggregation. / 多针 + 聚合。 |
| LongBench | Real / 真实 | Practical long-context tasks. / 实用长上下文任务。 |
| MRCR | Synthetic / 合成 | Multi-hop reasoning. / 多跳推理。 |

## Ship It | 产出物

Save as `outputs/skill-long-context-eval.md`:

> 保存为 `outputs/skill-long-context-eval.md`：

```markdown
Given a model claiming long-context support, verify actual performance.
1. Context length to test.
2. Benchmarks to run (NIAH, RULER, LongBench).
3. Minimum acceptable accuracy at target length.
```

## Exercises | 练习题

1. **Easy.** Run NIAH on a model at 10K and 50K tokens. Plot accuracy vs depth. / **简单。** 在 10K 和 50K token 上运行 NIAH。
2. **Medium.** Build a multi-needle test. Measure retrieval of 5 facts in a 100K context. / **中等。** 构建多针测试。
3. **Hard.** Compare 3 models on LongBench. Report which degrades fastest. / **困难。** 在 LongBench 上比较 3 个模型。

## Key Terms | 术语速查表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| NIAH（大海捞针） | Insert fact in long text, test retrieval. / 在长文本中插入事实，测试检索。 |
| Context window（上下文窗口） | Maximum input length a model can process. / 模型能处理的最大输入长度。 |
| Multi-hop reasoning（多跳推理） | Connect info across multiple documents. / 跨文档连接信息。 |

## Further Reading | 延伸阅读

- [NIAH original](https://arxiv.org/abs/2404.05460) — Needle In A Haystack. / 大海捞针。
- [RULER](https://arxiv.org/abs/2404.02372) — extended long-context benchmark. / 扩展长上下文基准。
- [LongBench](https://arxiv.org/abs/2308.14508) — real-world long-context tasks. / 真实长上下文任务。
