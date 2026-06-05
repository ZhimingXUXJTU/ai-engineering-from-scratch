# LLM Evaluation — RAGAS, DeepEval, G-Eval | LLM 评估 — RAGAS、DeepEval

> Exact-match and F1 miss semantic equivalence. Human review does not scale. LLM-as-judge is the production answer — with enough calibration to trust the number.
> 精确匹配和 F1 捕捉不到语义等价。人工审查不可扩展。LLM 作为评审是生产答案——经过足够校准可以信任这个数字。

> **【中文解读】** 评估 LLM 生成质量，包括 RAG 效果。RAGAS、DeepEval、G-Eval 是主流框架。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 23 (Chunking), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 23（分块），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

Your RAG system answers: "June 29th, 2007." The reference answer says: "June 29, 2007." Exact match says wrong. BLEU says partial. A human says correct. You need a metric that agrees with humans, scales to thousands of outputs, and costs less than human annotation.

> 你的 RAG 系统回答："June 29th, 2007。" 参考答案是："June 29, 2007。" 精确匹配说错了。BLEU 说部分对。人类说正确。你需要一个与人类一致的度量，可扩展到数千输出，且成本低于人工标注。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。

Now multiply by 10,000 test cases. Multiply again by every model update you want to ship. Human evaluation does not scale. You need automated metrics that correlate with human judgment at r ≥ 0.85.

> 现在乘以 10,000 个测试用例。再乘以你想发布的每个模型更新。人工评估不可扩展。你需要与人类判断相关性 r ≥ 0.85 的自动化指标。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。

2026 has three frameworks that own this problem.

> 2026 年有三个框架主导这个问题。

**RAGAS.** RAG Assessment. Evaluates retrieval + generation jointly. Metrics: faithfulness, answer relevancy, context precision, context recall. The standard for RAG evaluation.

> **RAGAS。** RAG 评估。联合评估检索和生成。指标：忠实度、答案相关性、上下文精确率、上下文召回率。RAG 评估标准。

**DeepEval.** Unit-test framework for LLM outputs. Metrics: answer relevance, faithfulness, bias, toxicity. Integrates with pytest.

> **DeepEval。** LLM 输出的单元测试框架。指标：答案相关性、忠实度、偏见、毒性。与 pytest 集成。

**G-Eval.** Chain-of-thought prompting to generate evaluation criteria, then score outputs. Research-grade. Highest correlation with human judgment.

> **G-Eval。** 用思维链提示生成评估标准，然后评分输出。研究级。与人类判断相关性最高。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了范式转变。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# Evaluate RAG pipeline
results = evaluate(
    dataset=rag_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
    llm=judge_llm,
    embeddings=embed_model,
)
print(results)
```

```python
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric

metric = FaithfulnessMetric(threshold=0.7, model="gpt-4")
assert_test(test_case, [metric])
```

> **【中文解读】** 本节展示如何用成熟框架快速应用该技术。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。

## Use It | 用框架实现

> **【中文解读】** 本节关注如何将模型部署为可用的产品。

| Framework / 框架 | Focus / 重点 | Best for / 最适合 |
|---------|--------|---------|
| RAGAS | RAG evaluation / RAG 评估 | Retrieval + generation / 检索 + 生成 |
| DeepEval | Unit testing / 单元测试 | CI/CD integration / CI/CD 集成 |
| G-Eval | Research / 研究 | Custom metrics / 自定义指标 |

## Ship It | 产出物

Save as `outputs/skill-llm-eval.md`:

> 保存为 `outputs/skill-llm-eval.md`：

```markdown
Given an LLM application (chatbot, RAG, agent), design evaluation pipeline.
1. Framework (RAGAS, DeepEval, G-Eval).
2. Metrics to track.
3. Calibration against human labels.
```

## Exercises | 练习题

1. **Easy.** Evaluate a simple RAG pipeline with RAGAS. / **简单。** 用 RAGAS 评估简单 RAG 流水线。
2. **Medium.** Build a DeepEval test suite for a chatbot. / **中等。** 为聊天机器人构建 DeepEval 测试套件。
3. **Hard.** Calibrate LLM-as-judge against 200 human labels. Report correlation. / **困难。** 用 200 个人类标签校准 LLM 评审。报告相关性。

## Key Terms | 术语速查表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| RAGAS | RAG evaluation framework. / RAG 评估框架。 |
| Faithfulness（忠实度） | Answer is supported by context. / 答案有上下文支持。 |
| LLM-as-judge | LLM evaluates other LLM outputs. / LLM 评估其他 LLM 输出。 |

## Further Reading | 延伸阅读

- [RAGAS](https://docs.ragas.io/) — RAG evaluation framework. / RAG 评估框架。
- [DeepEval](https://docs.confident-ai.com/) — LLM unit testing. / LLM 单元测试。
- [G-Eval](https://arxiv.org/abs/2303.16634) — chain-of-thought evaluation. / 思维链评估。
