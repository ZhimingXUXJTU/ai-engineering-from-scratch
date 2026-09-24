# 长文下文评估                

> 双子座3 Pro 广告10万语境代币.在1万代币时,8针MRCR下降到26.3%.广告可使用.长语境评估告诉你你运输的模型的实际容量.
> 双子座3 Pro 宣称10M代币 上下文──在1M代币中,8针MRCR 降至26.3%──宣称的可用≠──长上下文评估告诉你你正在部署的模型的实际能力──

> **【中文解读】**评估法师在长上下文窗口中的实际表现――

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 27 (LLM Evaluation) | **前置知识:** Phase 5 · 27（LLM 评估）
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

这就是2026年语境能力差距. 规格表显示1M代币. 基准表示:在100K代币时,检索精度下降15-40%.在500K时,它下降40-70%.

> 根据"图片"的描述,在2026年,检索准确率下降了15-40%.

> **【中文解读】**本节提出的问题是:如何正确理解和应用这一技术在实际工程中.

长文本评估衡量这些轴:在各种深度的检索准确性,在文件中进行多次推理,以及分布式信息的汇总.

> 长上下文评估测量这些轴:各种深度检查准确率,跨文档的多跳推理以及分布信息聚合力.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.

**NIAH (Needle in a Haystack).**插入一个特定的事实在一个长文档中,在各种位置.请模型检索它. 测量:模型可以在Y标签的草堆中找到一个深度X的针吗?

> **NIAH（大海捞针）。**在长文档的各个位置插入特定的事实――让模型检查――测量:模型能否在Y符号的干草堆中深度X 找到针?

**RULER.**扩大NIAH多针,变量距离和集成任务. 更全面.

> **RULER。**扩大NIAH 添加多针、可变距离和聚合任务──更全面──

**LongBench.**实际的长文本任务:总结,质量检查,检索,代码. 比合成基准更代表性.

> **LongBench。**真长上下文任务:摘要,问答,检索,代码.

**MRCR (Multi-hop Reasoning over Context).**需要连接多个文件的信息. 最难的长文本测试.

> **MRCR（上下文多跳推理）。**需要跨多档案连接信息的推理.

> **【拓展：大语言模型的工程实践】**通过GPT到ChatGPT,NLP 领域经历了范式转变.
```figure
gx-niah-decay
```

## 建立它

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构.

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.

## 建立它,实现它.

> **【中文解读】**本节通过代码从零实现核心算法.

### 步骤1:简单的NIAH测试

```python
def needle_in_haystack(model, context_length, needle, needle_position):
    """Insert needle at position in a long document and test retrieval."""
    haystack = generate_irrelevant_text(context_length)
    full_text = haystack[:needle_position] + f"\n{needle}\n" + haystack[needle_position:]
    question = f"What is the secret fact hidden in the text?"
    response = model(full_text + "\n\n" + question)
    return needle.lower() in response.lower()
```

> **【中文解读】**本节展示了如何使用成熟框架快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能.

## 用它实现框架

> **【中文解读】**本节关注如何将模型部署为可用产品.

| Benchmark / 基准 | Type / 类型 | Measures / 测量 |
|---------|------|---------|
| NIAH | Synthetic / 合成 | Single-fact retrieval at depth. / 深度单事实检索。 |
| RULER | Synthetic / 合成 | Multi-needle + aggregation. / 多针 + 聚合。 |
| LongBench | Real / 真实 | Practical long-context tasks. / 实用长上下文任务。 |
| MRCR | Synthetic / 合成 | Multi-hop reasoning. / 多跳推理。 |

## 运送它.

保存如`outputs/skill-long-context-eval.md`其他:

> 保存为`outputs/skill-long-context-eval.md`其他:

```markdown
Given a model claiming long-context support, verify actual performance.
1. Context length to test.
2. Benchmarks to run (NIAH, RULER, LongBench).
3. Minimum acceptable accuracy at target length.
```

## 练习题

1. **Easy.**运行NIAH在10K和50K代币的模型上.**简单。**在10K和50K代币上运行NIAH──
2. **Medium.**建立一个多针的测试,在100万的环境中测量5个事实.**中等。**构建多针测试――
3. **Hard.**报告最快的降解. / **困难。**在长上比较3个模型.

## 关键词 快速查找表

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| NIAH（大海捞针） | Insert fact in long text, test retrieval. / 在长文本中插入事实，测试检索。 |
| Context window（上下文窗口） | Maximum input length a model can process. / 模型能处理的最大输入长度。 |
| Multi-hop reasoning（多跳推理） | Connect info across multiple documents. / 跨文档连接信息。 |

## 继续阅读 继续阅读

- [NIAH original](https://arxiv.org/abs/2404.05460)针子在一堆草子里.
- [RULER](https://arxiv.org/abs/2404.02372)延长长文本基准. / 扩展长上下文基准──
- [LongBench](https://arxiv.org/abs/2308.14508)现实世界长文任务. / 真实长上下文任务──
