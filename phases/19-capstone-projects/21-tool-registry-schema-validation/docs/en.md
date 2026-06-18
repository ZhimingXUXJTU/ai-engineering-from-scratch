# Tool Registry with Schema Validation | 注册中心 化学

> A tool the agent cannot validate is a tool the agent cannot call. Build the registry and the schema checker before you build the tools.

> **【中文解读】** 本节是综合项目——构建工具注册中心和 Schema 验证。


**Type:** Build | **类型:** Build
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 lessons 01-07, Phase 14 lesson 01 | **前置知识:** Phase 13 lessons 01-07, Phase 14 lesson 01
**Time:** ~90 minutes | **时间:** ~90 minutes

> 🔗 **【前置】** Agent Harness 2/10。参考 Phase 13·07（工具 Schema）。
> 💡 工具注册中心 = 工具调用的"型检器"。Agent 不能验证的工具=不能调用的工具。先建 registry+schema 检查，再建工具。

## Learning Objectives | 学习目标
- Hold a typed registry of tool name → schema → handler that the dispatcher can ask once and trust afterwards.
  中文翻译：Hold a typed registry of tool name → schema → handler that the dispatcher can ask once and trust afterwards.
- Implement a JSON Schema 2020-12 subset that covers the keywords ninety percent of tool calls actually use.
  中文翻译：Implement a JSON Schema 2020-12 subset that covers the keywords ninety percent of tool calls actually use.
- Return precise, json-pointer-shaped error paths so the model can self-correct in one round trip.
  中文翻译：Return precise, json-pointer-shaped error paths so the model can self-correct in one round trip.
- Reject re-registration without explicit override, since silent overwrites are how production tool catalogs drift.
  中文翻译：Reject re-registration without explicit override, since silent overwrites are how production tool catalogs drift.
- Keep the validator pure (no I/O, no time, no globals) so it can be re-run on a replay log.
  中文翻译：Keep the validator pure (no I/O, no time, no globals) so it can be re-run on a replay log.

## Why the registry comes before the tool

> **【中文解读】** 本节强调注册中心必须先于工具构建。2026 年编码 Agent 注册的工具数超过模型单次上下文窗口能容纳的范围——200 个工具中每轮只暴露 10-40 个。注册中心是"什么工具存在"、"参数是什么形状"、"调用什么处理器"的唯一事实来源。避免的错误是：发布处理器没有 Schema，或发布 Schema 没有验证——两者都会让调度器变成猜测游戏。

> **【拓展：MCP 工具注册实践】** Model Context Protocol 中，每个 MCP 服务器通过 `tools/list` 方法暴露工具清单，每个工具包含 name、description、inputSchema（JSON Schema）。Claude Code 等客户端在会话开始时获取工具列表，按需选择暴露给模型的子集。JSON Schema 2020-12 子集覆盖 90% 实际使用的关键字：type、properties、required、enum、items、minimum/maximum、pattern。验证器必须纯净（无 I/O/时间/全局变量）以支持重放日志。

A coding agent in 2026 has more registered tools than the model can fit in a single context window. A non-trivial harness will register two hundred tools and surface ten to forty at any given turn. The registry is the source of truth for "what tools exist," "what shape do their arguments take," and "what handler do I call." Once those three answers are pinned, the rest of the harness can stop guessing.

> 一个coding agent in 2026 has more registered tools than the model can fit in a single context window. A non-trivial harness will register two hundred tools and surface ten to forty at any given turn. The registry is the source of truth for "what tools exist," "what shape do their arguments take," and "what handler do I call." Once those three answers are pinned, the rest of the harness can stop guessing.


The mistake we are avoiding is shipping handlers without schemas, or shipping schemas without validation. Both are common. Both turn the next layer (the dispatcher in lesson twenty-three) into a guessing game where the only failure mode is a stack trace from the handler.

> mistake we are avoiding is shipping handlers without schemas, or shipping schemas without validation. Both are common. Both turn the next layer (the dispatcher in lesson twenty-three) into a guessing game where the only failure mode is a stack trace from the handler.


## What a tool record looks like

```text
ToolRecord
  name        : str          (unique, lowercase alphanumeric and underscore segments separated by dots, e.g., snake_case.segment.case)
  description : str          (one line, shown to the model)
  schema      : dict         (JSON Schema 2020-12 subset)
  handler     : Callable     (async or sync, returns Any)
  idempotent  : bool         (dispatcher uses this for retry decisions)
  timeout_ms  : int          (override per-tool dispatcher default)
```

The schema is the only field the validator touches. The handler is opaque to it. We separate them on purpose. The schema is data. The handler is code. Mixing them tempts you to put validation logic inside the handler, which is the bug we are stopping.

> schema is the only field the validator touches. The handler is opaque to it. We separate them on purpose. The schema is data. The handler is code. Mixing them tempts you to put validation logic inside the handler, which is the bug we are stopping.


## The JSON Schema 2020-12 subset

The full 2020-12 spec is a paper. We need eight keywords.

```text
type           string / number / integer / boolean / object / array / null
properties     map of property name -> schema
required       list of property names
enum           list of allowed primitive values
minLength      integer, applies to strings
maxLength      integer, applies to strings
pattern        ECMA-262-compatible regex, applies to strings
items          schema applied to every array element
```

That is enough to cover what a tool API actually needs. The keywords we are not adding (oneOf, anyOf, allOf, $ref, conditionals) are valid in production schemas but turn the validator into a tree walker with cycles. We are building a registry, not a JSON Schema engine.

> That is enough to cover what a tool API actually needs.


## Json pointer error paths

When validation fails, the validator returns a list of errors. Each error carries a json-pointer path into the input. A pointer is a slash-prefixed sequence of property names and array indices.

> 当validation fails, the validator returns a list of errors. Each error carries a json-pointer path into the input. A pointer is a slash-prefixed sequence of property names and array indices.


```text
{"a": {"b": [1, 2, "x"]}}
                    ^
                    /a/b/2
```

The model reads error paths better than it reads sentences. If a schema requires `args.user.email` and the model passed an integer, the error should be `/user/email` with `expected_type: string`. The model fixes that in the next call without a round of natural language.

> model reads error paths better than it reads sentences. If a schema requires `args.user.email` and the model passed an integer, the error should be `/user/email` with `expected_type: string`. The model fixes that in the next call without a round of natural language.


## Registration and override

`register(name, schema, handler, **opts)` rejects re-registration by default. The caller has to pass `override=True` to replace. This is operational hygiene. Two parts of the codebase silently registering the same tool name is the kind of bug that takes a week to find in production.

> `register(name, schema, handler, **opts)` rejects re-registration by default.


The registry exposes three read methods. `get(name)` returns the record or raises. `validate(name, args)` returns an `Ok` or a list of errors. `names()` returns the tool names in registration order.

> registry exposes three read methods. `get(name)` returns the record or raises. `validate(name, args)` returns an `Ok` or a list of errors. `names()` returns the tool names in registration order.


## What the validator is and is not

It is a single pass over the schema tree, recursive. It is pure. It does not call handlers. It does not coerce types (a string `"42"` does not pass a number schema). It does not silently truncate.

> It is a single pass over the schema tree, recursive.


It is not a security boundary. A malicious handler can still misbehave after validation passes. The dispatcher in lesson twenty-three adds timeout and sandbox layers. The registry adds shape.

> It is not a security boundary.


## Shape

```mermaid
flowchart TD
    code[your code]
    reg[ToolRegistry<br/>name<br/>schema<br/>handler<br/>timeout]
    out[Ok or list of errors]
    code -->|register name, schema, handler| reg
    reg -->|validate args| out
```

## How to read the code

`code/main.py` defines `ToolRegistry`, `ToolRecord`, `ValidationError`, and the eight validator functions. The validator dispatches on `schema["type"]` (or treats a schema with `enum` as untyped enum check). Each type validator returns either an empty list or a list of `ValidationError`. The top-level walker concatenates errors and prepends path segments as it descends.

> `code/main.


`code/tests/test_registry.py` covers registration, override, validation success, validation failure with paths, and every keyword in the subset.

> `code/tests/test_registry.


## Going further

The two extensions you will want once this lesson lands are `$ref` resolution against a local definitions block, and `additionalProperties: false` for strict shape. Both are small. Both are common to add as the tool catalog grows past fifty tools. We left them out of the lesson to keep the file under one read.

> two extensions you will want once this lesson lands are `$ref` resolution against a local definitions block, and `additionalProperties: false` for strict shape. Both are small. Both are common to add as the tool catalog grows past fifty tools. We left them out of the lesson to keep the file under one read.


The next lesson (twenty-two) builds the JSON-RPC stdio transport that surfaces this registry to a model client. The lesson after (twenty-three) wraps both behind a dispatcher with timeouts and retries.

> 下一课将添加工具注册表。

