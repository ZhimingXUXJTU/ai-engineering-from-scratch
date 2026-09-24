# 士评价 士评价 士评价 士评价 士评价

> 精确匹配和F1失去了语义等效. 人类审查不扩展. LLM作为法官是生产答案,具有足够的校准度以信任数字.
> 精确匹配和F1 捕捉不到语义等价――人工审查不可扩展――LLM 作为评审是生产答案经过足够的校准可以信任这个数字――

> **【中文解读】**评估LLM 生成质量,包括RAG 效果――RAGAS、DeepEval、G-Eval 是主流框架――

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 23 (Chunking), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 23（分块），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## 问题 问题引入

你的RAG系统回答:"2007年6月29日".参考答案是:"2007年6月29日".精确匹配表示错误.蓝色表示部分.人类说正确.你需要一个与人类一致的指标,可达到数千个输出,成本低于人类的注释.

> 你的RAG系统回答:"6月29日,2007年"",参考答案是:"6月29日,2007年"",精确匹配说错了――BLEU 说部分对――人类说正确――你需要一个与人类一致的量度,可扩展到数千个输出,且成本低于人工标签――

> **【中文解读】**本节提出的问题是:如何正确理解和应用这一技术在实际工程中.

现在乘以1万个测试案例.再乘以每次要发送的模型更新.人类评估不扩展.你需要自动化指标,与人类判断相对于r ≥0.85.

> 现在乘以10,000个测试例. 再乘以你想发布的每个模型更新. 人工评估不可扩展.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.

2026年有三个框架,

> 2026年有三个框架主导这一问题.

**RAGAS.**评估RAG. 评估检索+生成. 衡量标准:忠实性,答案相关性,文本精度,文本召回.

> **RAGAS。**评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评价: 评

**DeepEval.**标准:答案相关性,忠实性,偏见性,毒性. 集成与 pytest.

> **DeepEval。**士课程 输出单元测试框架――指标:答案相关性、忠诚性、偏见、毒性──与 pytest 集成──
```figure
n5-judge-gauge
```

## 建立它

**G-Eval.**思考链促使生成评估标准,然后分出结果. 研究级.与人类判断力之间的最高相关性.

> **G-Eval。**用思维链提示生成评估标准,然后评分输出――研究级――与人类判断相关性最高――

> **【拓展：大语言模型的工程实践】**通过GPT到ChatGPT,NLP 领域经历了范式转变.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构.

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.

## 建立它,实现它.

> **【中文解读】**本节通过代码从零实现核心算法.

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

> **【中文解读】**本节展示了如何使用成熟框架快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能.

## 用它实现框架

> **【中文解读】**本节关注如何将模型部署为可用产品.

| Framework / 框架 | Focus / 重点 | Best for / 最适合 |
|---------|--------|---------|
| RAGAS | RAG evaluation / RAG 评估 | Retrieval + generation / 检索 + 生成 |
| DeepEval | Unit testing / 单元测试 | CI/CD integration / CI/CD 集成 |
| G-Eval | Research / 研究 | Custom metrics / 自定义指标 |

## 运送它.

保存如`outputs/skill-llm-eval.md`其他:

> 保存为`outputs/skill-llm-eval.md`其他:

```markdown
Given an LLM application (chatbot, RAG, agent), design evaluation pipeline.
1. Framework (RAGAS, DeepEval, G-Eval).
2. Metrics to track.
3. Calibration against human labels.
```

## 练习题

1. **Easy.**通过RAGAS来评估一个简单的RAG管道. / **简单。**用RAGAS 评估简单的RAG流水线――
2. **Medium.**建立一个DeepEval测试套件,为一个聊天机器人.**中等。**为聊天机器人构建深度Eval 测试套件──
3. **Hard.**根据200个人的标签, 进行校准.**困难。**用200个个人标签校准LLM评审.

## 关键词 快速查找表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| RAGAS | RAG evaluation framework. / RAG 评估框架。 |
| Faithfulness（忠实度） | Answer is supported by context. / 答案有上下文支持。 |
| LLM-as-judge | LLM evaluates other LLM outputs. / LLM 评估其他 LLM 输出。 |

## 继续阅读 继续阅读

- [RAGAS](https://docs.ragas.io/)RAG评估框架. /RAG评估框架。
- [DeepEval](https://docs.confident-ai.com/) LLM单元测试.
- [G-Eval](https://arxiv.org/abs/2303.16634)思想链评估. / 思维链评估.
