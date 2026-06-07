# Tool Use and Function Calling | 工具使用与函数调用

> Toolformer (Schick et al., 2023) started self-supervised tool annotation. Berkeley Function Calling Leaderboard V4 (Patil et al., 2025) sets the 2026 bar: 40% agentic, 30% multi-turn, 10% live, 10% non-live, 10% hallucination. Single-turn is solved. Memory, dynamic decision-making, and long-horizon tool chains are not.

> **【中文解读】** Toolformer 开创了自监督工具标注。Berkeley Function Calling Leaderboard V4 定义了 2026 年的评估标准：40% 智能体、30% 多轮、10% 实时、10% 非实时、10% 幻觉检测。单轮函数调用已解决，记忆、动态决策和长链工具编排仍是开放问题。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 13 · 01 (Function Calling Deep Dive) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 13 · 01 (函数调用深入)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- Explain Toolformer's self-supervised training signal: keep tool annotations only when execution reduces next-token loss.
  中文翻译：解释 Toolformer 的自监督训练信号：仅在执行减少下一个 token 损失时保留工具标注。
- Name BFCL V4's five evaluation categories and what each measures.
  中文翻译：说出 BFCL V4 的五个评估类别及每个衡量的内容。
- Implement a stdlib tool registry with schema validation, argument coercion, and execution sandboxing.
  中文翻译：用标准库实现带模式验证、参数强制转换和执行沙箱的工具注册表。
- Diagnose the three 2026 open problems: long-horizon tool chaining, dynamic decision-making, and memory.
  中文翻译：诊断三个 2026 年开放问题：长链工具编排、动态决策和记忆。

## The Problem | 问题引入

Early tool use asked: can the model predict a correct function call? Modern tool use asks: can the model chain tools across 40 steps, with memory, with partial observability, with recovery from tool failures, without hallucinating tools that do not exist?

> 早期工具使用的问题是：模型能否预测正确的函数调用？现代工具使用的问题是：模型能否在 40 步内链式调用工具、拥有记忆、处理部分可观察性、从工具失败中恢复、且不幻觉出不存在的工具？

Toolformer established the baseline: models can learn when to call tools with self-supervision. BFCL V4 defines the 2026 evaluation target. The gap between them is the space production agents live in.

> Toolformer 建立了基线：模型可以通过自监督学习何时调用工具。BFCL V4 定义了 2026 年的评估目标。两者之间的差距就是生产 Agent 的生存空间。

> **【中文解读】** 早期工具使用的问题是：模型能否预测正确的函数调用？现代工具使用的问题是：模型能否在 40 步内链式调用工具、拥有记忆、处理部分可观察性、从工具失败中恢复、且不幻觉出不存在的工具？单轮函数调用已接近解决，但记忆、动态决策和长链工具编排仍是 2026 年的开放问题。

> **【拓展：BFCL V4 评估体系的演进】** Berkeley Function Calling Leaderboard V4 是 2026 年事实上的评估标准。V3 引入了基于状态的评估（检查 API 实际状态而非匹配 AST），V4 添加了 Web 搜索、记忆和格式敏感性类别。关键发现：单轮函数调用已接近解决，失败集中在记忆（跨轮次上下文传递）、动态决策（基于先前结果选择工具）和长链漂移（20+ 步后偏离任务）。

## The Concept | 核心概念

### Toolformer (Schick et al., NeurIPS 2023)

Idea: let the model annotate its own pretraining corpus with candidate API calls. For each candidate, execute it. Keep the annotation only if including the tool result reduces loss on the next token. Fine-tune on the filtered corpus.

> 核心思想：让模型用自己的预训练语料标注候选 API 调用。对每个候选，执行它。只有当包含工具结果能减少下一个 token 的损失时才保留标注。然后在过滤后的语料上微调。

Tools covered: calculator, QA system, search engines, translator, calendar. The self-supervision signal is purely about whether the tool helps predict text — no human labels.

> 覆盖的工具：计算器、QA 系统、搜索引擎、翻译器、日历。自监督信号纯粹关于工具是否帮助预测文本——不需要人工标注。

Scale result: tool use emerges at scale. Smaller models hurt from tool annotations; larger models gain. This is why 2026 frontier models have strong tool use baked in while most 7B models need explicit tool-use fine-tuning to be reliable.

> 规模效应：工具使用在大模型上涌现。小模型反而被工具标注损害；大模型则受益。这就是为什么 2026 年前沿模型内置强大工具使用能力，而大多数 7B 模型需要显式工具使用微调才能可靠。

> **【中文解读】** Toolformer 的核心思想：让模型用自己的预训练语料标注候选 API 调用。对每个候选，执行它。只有当包含工具结果能减少下一个 token 的损失时才保留标注。然后在过滤后的语料上微调。规模效应显著：工具使用在大模型上涌现，小模型反而被工具标注损害。这也是 2026 年前沿模型有强大工具使用能力而大多数 7B 模型需要显式工具使用微调的原因。

### Berkeley Function Calling Leaderboard V4 (Patil et al., ICML 2025)

BFCL is the 2026 de facto evaluation. V4 composition:

> BFCL 是 2026 年事实上的评估标准。V4 组成：

- **Agentic (40%)** — full agent trajectories: memory, multi-turn, dynamic decisions.
  中文翻译：**智能体 (40%)**——完整 Agent 轨迹：记忆、多轮、动态决策。
- **Multi-Turn (30%)** — interactive conversations with tool chains.
  中文翻译：**多轮 (30%)**——带工具链的交互式对话。
- **Live (10%)** — user-submitted real prompts (harder distribution).
  中文翻译：**实时 (10%)**——用户提交的真实提示（更难的分布）。
- **Non-Live (10%)** — synthetic test cases.
  中文翻译：**非实时 (10%)**——合成测试用例。
- **Hallucination (10%)** — detect when no tool should be called.
  中文翻译：**幻觉 (10%)**——检测何时不应该调用工具。

V3 introduced state-based evaluation: after a tool sequence, check the API's actual state (e.g. "is the file created?") rather than match the AST of the tool calls. V4 added web search, memory, and format sensitivity categories.

> V3 引入了基于状态的评估：在工具序列执行后，检查 API 的实际状态（如"文件是否已创建？"）而非匹配工具调用的 AST。V4 添加了 Web 搜索、记忆和格式敏感性类别。

Key 2026 finding: single-turn function calling is near-solved. Failures concentrate in memory (carrying context across turns), dynamic decision-making (choosing tools based on prior results), long-horizon chains (drift after 20+ steps), and hallucination detection (refusing to call when no tool fits).

> 2026 年的关键发现：单轮函数调用已接近解决。失败集中在记忆（跨轮次传递上下文）、动态决策（基于先前结果选择工具）、长链漂移（20+ 步后偏离）和幻觉检测（在无合适工具时拒绝调用）。

### Tool schema

Every provider has a schema. They differ in details but share the same shape:

> 每个提供商都有自己的模式。细节不同但结构相同：

```
name: string
description: string (what it does, when to use it)
input_schema: JSON Schema (properties, required, types, enums)
```

Anthropic uses `input_schema` directly. OpenAI uses `function.parameters`. Both accept JSON Schema. Descriptions are load-bearing — the model reads them to pick the right tool. Bad tool descriptions are the #1 root cause of wrong-tool-picked failures.

> Anthropic 直接使用 `input_schema`。OpenAI 使用 `function.parameters`。两者都接受 JSON Schema。描述是核心承载——模型通过阅读描述来选择正确的工具。糟糕的工具描述是选错工具失败的头号根因。

### Argument validation

Trust no tool call. Validate:

> 不要信任任何工具调用。验证：

1. **Type coercion.** Model may return a string "5" where the schema says int. Coerce if unambiguous; reject if not.
   中文翻译：**类型强制转换。** 模型可能返回字符串 "5" 但模式要求 int。如果无歧义则强制转换；否则拒绝。
2. **Enum validation.** If the schema says `status in {"open", "closed"}` and model emits `"in_progress"`, reject with a descriptive error.
   中文翻译：**枚举验证。** 如果模式指定 `status in {"open", "closed"}` 而模型输出 `"in_progress"`，用描述性错误拒绝。
3. **Required fields.** Missing required field -> immediate error observation back to the model, not a crash.
   中文翻译：**必填字段。** 缺少必填字段 -> 立即返回错误观察给模型，而不是崩溃。
4. **Format validation.** Dates, emails, URLs — validate with concrete parsers, not regex.
   中文翻译：**格式验证。** 日期、邮箱、URL——用具体的解析器验证，而非正则表达式。

Every validation failure should return a structured observation so the model can retry with the correct shape.

> 每次验证失败都应返回结构化观察，以便模型可以用正确的格式重试。

### Parallel tool calls

Modern providers support parallel tool calls in one assistant turn. The loop:

> 现代提供商支持在一个助手轮次中并行调用工具。循环：

1. Model emits 3 tool calls with distinct `tool_use_id`s.
   中文翻译：模型发出 3 个带有不同 `tool_use_id` 的工具调用。
2. Runtime executes them (in parallel if independent).
   中文翻译：运行时执行它们（如果独立则并行）。
3. Each result goes back as a `tool_result` block correlated by `tool_use_id`.
   中文翻译：每个结果作为 `tool_result` 块返回，通过 `tool_use_id` 关联。

Engineering rule: treat correlation IDs as load-bearing. Swap them and you get wrong-tool-to-wrong-result routing.

> 工程规则：将关联 ID 视为核心承载。交换它们会导致错误的工具-结果路由。

### Sandboxing

Tool execution is the sandbox boundary. See Lesson 09 for detail. Short version: every tool should specify read/write surface, network access, timeout, memory cap. Generic `run_shell(cmd)` is a red flag; specific `git_status()` is safer.

> 工具执行是沙箱边界。详见第 9 课。简短版本：每个工具都应指定读写范围、网络访问、超时和内存上限。通用的 `run_shell(cmd)` 是红旗；特定的 `git_status()` 更安全。

## Build It | 动手构建

`code/main.py` implements a production-shape tool registry:

> `code/main.py` 实现了一个生产级工具注册表：

- JSON Schema subset validator (stdlib only).
  中文翻译：JSON Schema 子集验证器（仅标准库）。
- Tool registration with description, input schema, timeout, and executor.
  中文翻译：带描述、输入模式、超时和执行器的工具注册。
- Argument coercion and enum validation.
  中文翻译：参数强制转换和枚举验证。
- Parallel tool dispatch with correlation IDs.
  中文翻译：带关联 ID 的并行工具分派。
- Error observations as structured strings.
  中文翻译：错误观察作为结构化字符串。

Run it:

> 运行：

```
python3 code/main.py
```

The trace shows a mini agent calling three tools in one turn, with one deliberately malformed call that is rejected with a descriptive error the model can act on.

> 轨迹显示一个迷你 Agent 在一个轮次中调用三个工具，其中一个故意格式错误的调用被描述性错误拒绝，模型可以据此行动。

## Use It | 用框架实现

Every provider has its own tool schema — Anthropic, OpenAI, Gemini, Bedrock. Use a translation layer (OpenAI Agents SDK, Vercel AI SDK, LangChain tool adapter) if you need multi-provider. BFCL is the reference benchmark — run it against your agent before shipping if tool use is central to the product.

> 每个提供商都有自己的工具模式——Anthropic、OpenAI、Gemini、Bedrock。如果需要多提供商，使用翻译层（OpenAI Agents SDK、Vercel AI SDK、LangChain 工具适配器）。BFCL 是参考基准——如果工具使用是产品核心，发布前用它测试你的 Agent。

## Ship It | 产出物

`outputs/skill-tool-registry.md` generates a tool catalog, schema, and registry for a given task domain. Includes description-quality checks (does each tool's description tell the model when to use it?).

> `outputs/skill-tool-registry.md` 为给定任务领域生成工具目录、模式和注册表。包含描述质量检查（每个工具的描述是否告诉模型何时使用它？）。

## Exercises | 练习题

1. Add a "no-op" tool that lets the model explicitly refuse to use any other tool. Measure on a BFCL-like hallucination test.
   中文翻译：添加一个"无操作"工具，让模型显式拒绝使用任何其他工具。在类 BFCL 幻觉测试上测量。
2. Implement argument coercion for int-as-string and float-as-string. Where does coercion start to hide real bugs?
   中文翻译：实现字符串到 int 和字符串到 float 的参数强制转换。强制转换何时开始隐藏真实 bug？
3. Add a per-tool timeout and a circuit breaker (refuse the tool for 60s after 3 consecutive failures). What does this change about how the model recovers?
   中文翻译：添加每个工具的超时和熔断器（连续 3 次失败后拒绝工具 60 秒）。这如何改变模型的恢复方式？
4. Read BFCL V4 description. Pick one category (e.g. "multi-turn") and run 10 example prompts through your agent. Report pass rate.
   中文翻译：阅读 BFCL V4 描述。选择一个类别（如"多轮"）并通过你的 Agent 运行 10 个示例提示。报告通过率。
5. Port the stdlib validator to Pydantic or Zod. What did Pydantic/Zod catch that the toy missed?
   中文翻译：将标准库验证器移植到 Pydantic 或 Zod。Pydantic/Zod 捕获了玩具版本遗漏的什么？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Function calling | "Tool use" / "工具使用" | Structured-output tool invocation with validated schema / 带验证模式的结构化输出工具调用 |
| Toolformer | "Self-supervised tool annotation" / "自监督工具标注" | Schick 2023 — keep tool calls whose results reduce next-token loss / Schick 2023——保留减少下一个 token 损失的工具调用 |
| BFCL | "Berkeley Function Calling Leaderboard" / "Berkeley 函数调用排行榜" | 2026 benchmark: 40% agentic, 30% multi-turn, 10% live, 10% non-live, 10% hallucination / 2026 基准：40% 智能体、30% 多轮、10% 实时、10% 非实时、10% 幻觉 |
| Tool schema | "Function signature for the model" / "模型的函数签名" | name, description, JSON Schema of arguments / 名称、描述、参数的 JSON Schema |
| tool_use_id | "Correlation ID" / "关联 ID" | Ties a tool call to its result; essential for parallel dispatch / 将工具调用与其结果关联；并行分派必需 |
| Hallucination detection | "Know when not to call" / "知道何时不调用" | V4 category: refuse to call when no tool fits / V4 类别：无合适工具时拒绝调用 |
| Argument coercion | "String-to-int repair" / "字符串到整数的修复" | Narrow fixes for predictable schema-mismatch; reject if ambiguous / 可预测模式不匹配的窄修复；如果歧义则拒绝 |
| Sandboxing | "Tool execution boundary" / "工具执行边界" | Per-tool read/write surface, network, timeout, memory cap / 每个工具的读写范围、网络、超时、内存上限 |

## Further Reading | 延伸阅读

- [Schick et al., Toolformer (arXiv:2302.04761)](https://arxiv.org/abs/2302.04761) — self-supervised tool annotation
  中文翻译：Toolformer 经典论文——自监督工具标注。
- [Berkeley Function Calling Leaderboard (V4)](https://gorilla.cs.berkeley.edu/leaderboard.html) — 2026 eval benchmark
  中文翻译：Berkeley 函数调用排行榜 V4——2026 年评估基准。
- [Anthropic, Tool use documentation](https://platform.claude.com/docs/en/agent-sdk/overview) — production tool schema in the Claude Agent SDK
  中文翻译：Anthropic 工具使用文档——Claude Agent SDK 中的生产级工具模式。
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) — function tool type and Guardrails
  中文翻译：OpenAI Agents SDK 文档——函数工具类型和护栏。
