# Structured Outputs & Constrained Decoding | 结构化输出与约束解码

> Ask an LLM for JSON. Get JSON most of the time. In production, "most" is the problem. Constrained decoding turns "most" into "always" by editing the logits before sampling.
> 让 LLM 输出 JSON。大多数时候能得到 JSON。在生产中，"大多数"就是问题。约束解码通过在采样前编辑 logits 将 "大多数" 变成 "总是"。

> **【中文解读】** 让 LLM 输出结构化数据如 JSON、SQL。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 19 (Subword Tokenization) | **前置知识:** Phase 5 · 19（子词分词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## The Problem | 问题引入

Free-form generation is not a contract. It is a suggestion. You ask for JSON, you get a JSON-shaped string with a trailing comma, an extra backtick, or a key named in German. Every downstream parser breaks. You ask for a SQL query, you get one with a hallucinated column name. In production, these failures are not bugs — they are incidents.

> 自由格式生成不是契约，是建议。你要求 JSON，得到一个带尾逗号、多余反引号或德语键名的 JSON 形状字符串。每个下游解析器都会崩溃。你要求 SQL 查询，得到一个幻觉列名。在生产中，这些失败不是 bug——是事故。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。

Three layers exist in 2026.

> 2026 年存在三层方案。

1. **Prompting.** Ask nicely. "Return only the JSON object." Works ~85-95% of the time. Fails on edge cases, long outputs, and adversarial inputs. / **提示。** 好好请求。"只返回 JSON 对象。" 约 85-95% 的时间有效。在边界情况、长输出和对抗性输入上失败。
2. **Constrained decoding.** Mask invalid next-token logits at every generation step so the output always conforms to a schema (JSON schema, regex, context-free grammar). Works 100%. Costs ~10-30% latency overhead. / **约束解码。** 在每个生成步骤屏蔽无效的下一个 token logits，使输出始终符合模式。100% 有效。约 10-30% 延迟开销。
3. **Tool/function calling.** Structured output via the model's native tool-calling interface. The model emits a JSON object directly, not as text. Best latency, best reliability, but model-specific. / **工具/函数调用。** 通过模型原生工具调用接口的结构化输出。最佳延迟，最佳可靠性，但模型特定。

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。

**Logit masking.** At each generation step, the model produces a probability distribution over the vocabulary. Constrained decoding computes the set of valid next tokens (given the schema and what has been generated so far) and sets all other logits to -inf before softmax. The model can only pick from valid tokens.

> **Logit 屏蔽。** 在每个生成步骤，模型在词表上产生概率分布。约束解码计算有效下一个 token 集合（给定模式和已生成内容），将所有其他 logits 设为 -inf 后再 softmax。模型只能从有效 token 中选择。

**JSON schema constraints.** For JSON output, the constraint enforces: opening braces match closing braces, keys are quoted strings, values match their declared types, required fields are present, no extra fields beyond the schema. This is a context-free grammar constraint, computed incrementally.

> **JSON 模式约束。** 对于 JSON 输出，约束强制：开闭括号匹配、键是带引号字符串、值匹配声明类型、必填字段存在、无模式外额外字段。这是一个上下文无关语法约束，增量计算。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。

## Build It | 动手实现

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

### Step 1: simple logit masking

```python
import json
import re


def mask_logits(logits, valid_token_ids):
    """Set invalid token logits to -inf."""
    mask = torch.full_like(logits, float('-inf'))
    mask[valid_token_ids] = logits[valid_token_ids]
    return mask
```

The core insight: at each step, only a subset of tokens is valid. Computing that subset efficiently is the engineering challenge.

> 核心洞察：在每个步骤，只有 token 子集是有效的。高效计算该子集是工程挑战。

### Step 2: JSON schema validation during generation

```python
import jsonschema

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
    },
    "required": ["name", "age"],
}

def validate_json_output(text, schema):
    try:
        data = json.loads(text)
        jsonschema.validate(data, schema)
        return True, data
    except (json.JSONDecodeError, jsonschema.ValidationError) as e:
        return False, str(e)
```

### Step 3: using LM Format Enforcer

```python
from lmformatenforcer import JsonSchemaParser, generate_enforced

parser = JsonSchemaParser(schema)
# Use with any Hugging Face model's generate method
# result = generate_enforced(model, tokenizer, parser, prompt)
```

> **【中文解读】** 本节展示如何用成熟框架快速应用该技术。在实际项目中，优先使用经过验证的框架实现。

> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。

The 2026 production options:

> 2026 年的生产选项：

| Approach / 方案 | Reliability / 可靠性 | Latency cost / 延迟成本 | Best for / 最适合 |
|---------|------------|-------------|---------|
| Prompting / 提示 | ~85-95% / 约 85-95% | None / 无 | Prototypes, non-critical paths / 原型、非关键路径 |
| Constrained decoding / 约束解码 | 100% / 100% | +10-30% / 加 10-30% | Production APIs / 生产 API |
| Tool calling / 工具调用 | ~99.9% / 约 99.9% | Lowest / 最低 | Model-native workflows / 模型原生工作流 |

## Ship It | 产出物

Save as `outputs/prompt-structured-output.md`:

> 保存为 `outputs/prompt-structured-output.md`：

```markdown
Given an LLM output that must be structured (JSON, SQL, etc.), pick the right approach and implement it.
1. Schema definition. JSON Schema, regex, or grammar.
2. Enforcement method. Prompting, constrained decoding, or tool calling.
3. Fallback plan. What happens when the output still fails validation.
```

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

## Exercises | 练习题

1. **Easy.** Build a prompt-only JSON extractor. Measure success rate on 100 LLM calls. / **简单。** 构建纯提示的 JSON 提取器。测量 100 次 LLM 调用的成功率。
2. **Medium.** Implement constrained decoding for a simple JSON schema using logit masking. / **中等。** 使用 logit 屏蔽为简单 JSON 模式实现约束解码。
3. **Hard.** Compare constrained decoding vs tool calling on a production workload. Report latency, reliability, and cost. / **困难。** 在生产工作负载上比较约束解码与工具调用。报告延迟、可靠性和成本。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。

## Key Terms | 术语速查表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Constrained decoding（约束解码） | Force valid output / 强制有效输出 | Mask invalid logits at each step. / 每步屏蔽无效 logits。 |
| Logit masking（Logit 屏蔽） | Block bad tokens / 阻止坏 token | Set invalid token logits to -inf before softmax. / softmax 前将无效 token logits 设为 -inf。 |
| JSON Schema | JSON validation rules / JSON 验证规则 | Declarative schema for validating JSON structure and types. / 验证 JSON 结构和类型的声明式模式。 |
| Tool calling（工具调用） | Function calling / 函数调用 | Model emits structured arguments directly via native interface. / 模型通过原生接口直接发出结构化参数。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。

## Further Reading | 延伸阅读

- [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer) — production constrained decoding library. / 生产级约束解码库。
- [Outlines](https://github.com/dottxt-ai/outlines) — structured generation with regex/JSON/CFG. / 带 regex/JSON/CFG 的结构化生成。
- [JSON Schema specification](https://json-schema.org/) — the standard for JSON validation. / JSON 验证标准。
