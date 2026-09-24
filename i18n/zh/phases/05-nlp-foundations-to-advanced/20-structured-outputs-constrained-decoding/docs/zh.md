# 结构化输出和束解码

> 要求一个LLM获得JSON. 获取JSON大部分时间. 在生产中,"大多数"是问题. 限制式解码将"大多数"转化为"总是"通过在采样之前编辑记录.
> 让LLM 输出JSON──大多数时候可以得到JSON──在生产中",大多数"就是问题──通过采样前编辑逻辑将"大多数"变成"总是"──

> **【中文解读】**让LLM输出结构化数据如JSON、SQL──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 19 (Subword Tokenization) | **前置知识:** Phase 5 · 19（子词分词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## 问题 问题引入

免费形式生成不是合同.这是一个建议.你要求JSON,你得到一个JSON形字符串,一个后尾逗号,一个额外的背,或一个名字的密钥.每一个下游解析器都会断裂.你要求一个SQL查询,你得到一个具有幻觉的列名字.在生产中,这些失败不是 bug 它们是事件.

> 自由格式生成不是契约,是建议. 你要求JSON,得到一个带尾逗号,多余反引号或德语键名的JSON 形状字符串. 每个下游解析器都会崩.

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――

2026年,有三个层.

> 2026年,存在三层方案.

1. **Prompting.**问题很好. "只返回JSON对象". 工作时间大约85-95%. 边缘案例,长输出和对抗输入失败. / **提示。**好好请求"",只返回JSON对象"",约85-95%的时间有效――在边界情况,长输出和对抗性输入上失败――
2. **Constrained decoding.**每次生成步骤都会掩盖不有效的下一个代码登录,因此输出总是符合一个方案 (JSON方案,regex,无文本语法). 效果 100%.成本~10-30%延迟总费. / **约束解码。**在每个生成步骤中屏蔽无效的下一个代币登录,使输出始终符合模式――100% 有效――约10-30% 延迟开销――
3. **Tool/function calling.**通过模型的本土工具调用界面进行结构化输出.模型直接发射一个JSON对象,而不是作为文本.最佳延迟,最佳可靠性,但模型特定. / **工具/函数调用。**通过模型原生工具调用接口的结构化输出――最佳延迟,最佳可靠性,但模型特定――

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

**Logit masking.**在每一个生成步骤,模型在词汇中产生概率分布. 限制式解码计算了有效下一个代币的集合 (鉴于方案和迄今为止生成的) 并设置了所有其他代码在软max之前为 -inf. 该模型只能从有效代币中选择.

> **Logit 屏蔽。**在每个生成步骤中,模型在词表上产生概率分布――约束解码计算有效下一个代币集合――将所有其他逻辑设为 -inf 后再软max――模型只能从有效代币中选择――

**JSON schema constraints.**对于JSON输出,限制执行:开关括号与关闭括号匹配,键是引用字符串,值与其声明的类型匹配,所需的字段存在,除了方案之外没有额外的字段.这是一个无文本语法限制,逐步计算.

> **JSON 模式约束。**对于JSON输出,约束强制:开闭括号匹配、键是带引号字符串、值匹配声明类型、必填字段存在、无模式外额外字段──这是一个上下文无关语法约束,增量计算──

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.
```figure
constrained-decoder
```

## 建立它

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

### 步骤1:简单的罩

```python
import json
import re


def mask_logits(logits, valid_token_ids):
    """Set invalid token logits to -inf."""
    mask = torch.full_like(logits, float('-inf'))
    mask[valid_token_ids] = logits[valid_token_ids]
    return mask
```

基本的见解是:在每一步,只有一个子集的代币是有效的.

> 核心洞察:在每一步,只有标记子集是有效的.

### 步骤2:生成过程中验证JSON图案

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

### 步骤3:使用LM格式执行器

```python
from lmformatenforcer import JsonSchemaParser, generate_enforced

parser = JsonSchemaParser(schema)
# Use with any Hugging Face model's generate method
# result = generate_enforced(model, tokenizer, parser, prompt)
```

> **【中文解读】**本节展示了如何使用成熟框架快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

2026年生产选择:

> 2026年生产选项:

| Approach / 方案 | Reliability / 可靠性 | Latency cost / 延迟成本 | Best for / 最适合 |
|---------|------------|-------------|---------|
| Prompting / 提示 | ~85-95% / 约 85-95% | None / 无 | Prototypes, non-critical paths / 原型、非关键路径 |
| Constrained decoding / 约束解码 | 100% / 100% | +10-30% / 加 10-30% | Production APIs / 生产 API |
| Tool calling / 工具调用 | ~99.9% / 约 99.9% | Lowest / 最低 | Model-native workflows / 模型原生工作流 |

## 运送它.

保存如`outputs/prompt-structured-output.md`其他:

> 保存为`outputs/prompt-structured-output.md`其他:

```markdown
Given an LLM output that must be structured (JSON, SQL, etc.), pick the right approach and implement it.
1. Schema definition. JSON Schema, regex, or grammar.
2. Enforcement method. Prompting, constrained decoding, or tool calling.
3. Fallback plan. What happens when the output still fails validation.
```

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 练习题

1. **Easy.**建立一个只即时的JSON提取器. 测量100次LLM电话的成功率. / **简单。**构建纯提示的JSON提取器――测量100次 LLM调用成功率――
2. **Medium.**通过使用 logit 掩盖,实现简单的 JSON 方案的限制解码. / **中等。**使用logit 屏蔽为简单 JSON 模式实现约束解码.
3. **Hard.**进行限制解码与需要生产工作负载的工具的比较. 报告延迟,可靠性和成本. / **困难。**在生产工作负载上,与工具调用相比较.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 关键词 快速查找表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Constrained decoding（约束解码） | Force valid output / 强制有效输出 | Mask invalid logits at each step. / 每步屏蔽无效 logits。 |
| Logit masking（Logit 屏蔽） | Block bad tokens / 阻止坏 token | Set invalid token logits to -inf before softmax. / softmax 前将无效 token logits 设为 -inf。 |
| JSON Schema | JSON validation rules / JSON 验证规则 | Declarative schema for validating JSON structure and types. / 验证 JSON 结构和类型的声明式模式。 |
| Tool calling（工具调用） | Function calling / 函数调用 | Model emits structured arguments directly via native interface. / 模型通过原生接口直接发出结构化参数。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.

## 继续阅读 继续阅读

- [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer)生产限制了解码库. / 生产级约束解码库.
- [Outlines](https://github.com/dottxt-ai/outlines) 结构化生成/JSON/CFG. / 带 regex/JSON/CFG 的结构化生成
- [JSON Schema specification](https://json-schema.org/)标准用于JSON验证.
