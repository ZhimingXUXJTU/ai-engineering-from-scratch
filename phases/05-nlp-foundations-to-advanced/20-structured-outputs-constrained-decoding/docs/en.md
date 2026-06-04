# Structured Outputs & Constrained Decoding | 结构化输出与约束解码

> Ask an LLM for JSON. Get JSON most of the time. In production, "most" is the problem. Constrained decoding turns "most" into "always" by editing the logits before sampling.

> **【中文解读】** 让 LLM 输出结构化数据如 JSON、SQL。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 5 · 17 (Chatbots), Phase 5 · 19 (Subword Tokenization)
**Time:** ~60 minutes

## The Problem | 问题引入

A classifier prompts an LLM: "Return one of {positive, negative, neutral}." The model returns "The sentiment is positive — this review is overwhelmingly favorable because the customer explicitly states that they ...". Your parser crashes. Your classifier's F1 is 0.0.

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


Free-form generation is not a contract. It is a suggestion. A production system needs a contract.

Three layers exist in 2026.

1. **Prompting.** Ask nicely. "Return only the JSON object." Works ~80% on frontier models, less on smaller ones.
2. **Native structured output APIs.** OpenAI `response_format`, Anthropic tool use, Gemini JSON mode. Reliable on supported schemas. Vendor-locked.
3. **Constrained decoding.** Modify the logits at every generation step so the model *cannot* emit invalid tokens. 100% valid by construction. Works on any local model.

This lesson builds intuition for all three and names when to reach for which.

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


## The Concept | 核心概念

![Constrained decoding masking invalid tokens at each step](../assets/constrained-decoding.svg)

**How constrained decoding works.** At each generation step, the LLM produces a logit vector over the full vocabulary (~100k tokens). A *logit processor* sits between the model and the sampler. It computes which tokens are valid given the current position in the target grammar — JSON Schema, regex, context-free grammar — and sets the logits of all invalid tokens to negative infinity. The softmax over the remaining logits puts probability mass only on valid continuations.

Implementations in 2026:

- **Outlines.** Compiles JSON Schema or regex into a finite-state machine. Every token gets an O(1) valid-next-token lookup. FSM-based, so recursive schemas need flattening.
- **XGrammar / llguidance.** Context-free grammar engines. Handle recursive JSON Schema. Near-zero decoding overhead. OpenAI credited llguidance in their 2025 structured output implementation.
- **vLLM guided decoding.** Built-in `guided_json`, `guided_regex`, `guided_choice`, `guided_grammar` via Outlines, XGrammar, or lm-format-enforcer backends.
- **Instructor.** Pydantic-based wrapper over any LLM. Retries on validation failure. Cross-provider, but does not modify logits — it relies on retries + structured-output-aware prompts.

### The counterintuitive result

Constrained decoding is often *faster* than unconstrained generation. Two reasons. First, it shrinks the next-token search space. Second, clever implementations skip token generation entirely for forced tokens (scaffolding like `{"name": "` — every byte is determined).

### The pitfall that costs you

Field order matters. Put `answer` before `reasoning`, and the model commits to an answer before it thinks. JSON is valid. Answer is wrong. No validation catches it.

```json
// BAD
{"answer": "yes", "reasoning": "because ..."}

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。


// GOOD
{"reasoning": "... therefore ...", "answer": "yes"}
```

Schema field order is logic, not formatting.

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。




## Build It | 动手实现

### Step 1: regex-constrained generation from scratch

See `code/main.py` for a standalone FSM implementation. The core idea in 30 lines:

```python
def mask_logits(logits, valid_token_ids):
    mask = [float("-inf")] * len(logits)
    for tid in valid_token_ids:
        mask[tid] = logits[tid]
    return mask


def generate_constrained(model, tokenizer, prompt, fsm):
    ids = tokenizer.encode(prompt)
    state = fsm.initial_state
    while not fsm.is_accept(state):
        logits = model.next_token_logits(ids)
        valid = fsm.valid_tokens(state, tokenizer)
        logits = mask_logits(logits, valid)
        tok = sample(logits)
        ids.append(tok)
        state = fsm.transition(state, tok)
    return tokenizer.decode(ids)
```

The FSM tracks what parts of the grammar we have satisfied so far. `valid_tokens(state, tokenizer)` computes which vocabulary tokens can advance the FSM without leaving an accepting path.

### Step 2: Outlines for JSON Schema

```python
from pydantic import BaseModel
from typing import Literal
import outlines


class Review(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float
    evidence_span: str


model = outlines.models.transformers("meta-llama/Llama-3.2-3B-Instruct")
generator = outlines.generate.json(model, Review)

result = generator("Classify: 'The wait staff was attentive and the food arrived hot.'")
print(result)
# Review(sentiment='positive', confidence=0.93, evidence_span='attentive ... hot')
```

Zero validation errors. Ever. The FSM makes invalid output unreachable.

### Step 3: Instructor for provider-agnostic Pydantic

```python
import instructor
from anthropic import Anthropic
from pydantic import BaseModel, Field


class Invoice(BaseModel):
    vendor: str
    total_usd: float = Field(ge=0)
    line_items: list[str]


client = instructor.from_anthropic(Anthropic())
invoice = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    response_model=Invoice,
    messages=[{"role": "user", "content": "Extract from: 'Acme Corp $420. Widget, Gizmo.'"}],
)
```

Different mechanism. Instructor does not touch logits. It formats the schema into the prompt, parses the output, and retries on validation failure (default 3 times). Works with any provider. Retries add latency and cost. Cross-provider portability is the selling point.

### Step 4: native vendor APIs

```python
from openai import OpenAI

client = OpenAI()
response = client.responses.create(
    model="gpt-5",
    input=[{"role": "user", "content": "Classify: 'The food was cold.'"}],
    text={"format": {"type": "json_schema", "name": "sentiment",
          "schema": {"type": "object", "required": ["sentiment"],
                     "properties": {"sentiment": {"type": "string",
                                                  "enum": ["positive", "negative", "neutral"]}}}}},
)
print(response.output_parsed)
```

Server-side constrained decoding. Reliability parity with Outlines for supported schemas. No local model management. Locks you to the vendor.




> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Pitfalls

- **Recursive schemas.** Outlines flattens recursion to a fixed depth. Tree-structured outputs (nested comments, AST) need XGrammar or llguidance (CFG-based).
- **Huge enums.** 10,000-option enum compiles slowly or times out. Switch to a retriever: predict top-k candidates first, constrain to those.
- **Grammar too strict.** Force `date: "YYYY-MM-DD"` regex and the model cannot output `"unknown"` for missing dates. Model compensates by inventing a date. Allow `null` or a sentinel.
- **Premature commitment.** See field-order pitfall above. Always put reasoning first.
- **Vendor JSON mode without schema.** Pure JSON mode only guarantees valid JSON, not valid *for your use case*. Always provide a full schema.

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


## Use It | 用框架实现

The 2026 stack:

| Situation | Pick |
|-----------|------|
| OpenAI/Anthropic/Google model, simple schema | Native vendor structured output |
| Any provider, Pydantic workflow, can tolerate retries | Instructor |
| Local model, need 100% validity, flat schema | Outlines (FSM) |
| Local model, recursive schema | XGrammar or llguidance |
| Self-hosted inference server | vLLM guided decoding |
| Batch processing with retries acceptable | Instructor + cheapest model |

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。




## Ship It | 产出物

Save as `outputs/skill-structured-output-picker.md`:

```markdown
---
name: structured-output-picker
description: Choose a structured output approach, schema design, and validation plan.
version: 1.0.0
phase: 5
lesson: 20
tags: [nlp, llm, structured-output]
---

Given a use case (provider, latency budget, schema complexity, failure tolerance), output:

1. Mechanism. Native vendor structured output, Instructor retries, Outlines FSM, or XGrammar CFG. One-sentence reason.
2. Schema design. Field order (reasoning first, answer last), nullable fields for "unknown", enum vs regex, required fields.
3. Failure strategy. Max retries, fallback model, graceful `null` handling, out-of-distribution refusal.
4. Validation plan. Schema compliance rate (target 100%), semantic validity (LLM-judge), field-coverage rate, latency p50/p99.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse any design that puts `answer` or `decision` before reasoning fields. Refuse to use bare JSON mode without a schema. Flag recursive schemas behind an FSM-only library.
```

## Exercises | 练习题

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


1. **Easy.** Prompt a small open-weights model (e.g., Llama-3.2-3B) without constrained decoding for `Review(sentiment, confidence, evidence_span)`. Measure the fraction that parse as valid JSON on 100 reviews.
2. **Medium.** Same corpus with Outlines JSON mode. Compare compliance rate, latency, and semantic accuracy.
3. **Hard.** Implement a regex-constrained decoder from scratch for phone numbers (`\d{3}-\d{3}-\d{4}`). Verify 0 invalid outputs on 1000 samples.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Constrained decoding | Force valid output | Mask invalid-token logits at every generation step. |
| Logit processor | The thing that constrains | Function: `(logits, state) -> masked_logits`. |
| FSM | Finite-state machine | Compiled grammar representation; O(1) valid-next-token lookup. |
| CFG | Context-free grammar | Grammar that handles recursion; slower but more expressive than FSM. |
| Schema field order | Does it matter? | Yes — first field commits; always put reasoning before answer. |
| Guided decoding | vLLM's name for it | Same concept, integrated into the inference server. |
| JSON mode | OpenAI's early version | Guarantees JSON syntax; does NOT guarantee schema match. |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Willard, Louf (2023). Efficient Guided Generation for LLMs](https://arxiv.org/abs/2307.09702) — the Outlines paper.
- [XGrammar paper (2024)](https://arxiv.org/abs/2411.15100) — fast CFG-based constrained decoding.
- [vLLM — Structured Outputs](https://docs.vllm.ai/en/latest/features/structured_outputs.html) — inference server integration.
- [OpenAI — Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs) — API reference + gotchas.
- [Instructor library](https://python.useinstructor.com/) — Pydantic + retries across providers.
- [JSONSchemaBench (2025)](https://arxiv.org/abs/2501.10868) — benchmarking 6 constrained decoding frameworks.
