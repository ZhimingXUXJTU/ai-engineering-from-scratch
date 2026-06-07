# Memory Blocks and Sleep-Time Compute (Letta) | 记忆块与休眠计算（Letta）

> MemGPT became Letta in 2024. The 2026 evolution adds two ideas: discrete functional memory blocks the model can edit directly, and a sleep-time agent that consolidates memory asynchronously while the primary agent is idle. This is how you scale memory beyond one conversation.

> **【中文解读】** MemGPT 在 2024 年成为 Letta。2026 年的演进增加了两个想法：模型可以直接编辑的离散功能记忆块，以及在主 Agent 空闲时异步合并记忆的休眠 Agent。这是将记忆扩展到单次对话之外的方式。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT) | **前置知识:** Phase 14 · 07 (MemGPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Name the three memory tiers Letta uses (core, recall, archival) and the role of each.
  中文翻译：说出 Letta 使用的三个记忆层级（core、recall、archival）及各自的作用。
- Explain the memory-block pattern: Human block, Persona block, and user-defined blocks as first-class typed objects.
  中文翻译：解释记忆块模式：Human 块、Persona 块和用户自定义块作为一等类型化对象。
- Describe what sleep-time compute is, why it sits off the critical path, and why it can run a stronger model than the primary agent.
  中文翻译：描述休眠计算是什么、为什么它在关键路径之外、为什么可以运行比主 Agent 更强的模型。
- Implement a scripted two-agent loop where a primary agent serves responses and a sleep-time agent consolidates blocks between turns.
  中文翻译：实现一个脚本化的双 Agent 循环，主 Agent 提供响应，休眠 Agent 在轮次间合并块。

## The Problem | 问题引入

MemGPT (Lesson 07) solved the virtual-memory control flow. Three production problems emerged:

> MemGPT（第 7 课）解决了虚拟内存控制流。三个生产问题出现了：

1. **Latency.** Every memory operation sits on the critical path. If the agent has to prune, summarize, or reconcile while the user waits, tail latency blows up.
   中文翻译：**延迟。** 每个记忆操作都在关键路径上。如果 Agent 必须在用户等待时修剪、摘要或协调，尾部延迟会爆炸。
2. **Memory rot.** Writes accumulate. Contradicted facts stay. Retrieval drowns in stale content.
   中文翻译：**记忆腐化。** 写入积累。矛盾的事实保留。检索被过时内容淹没。
3. **Structure loss.** A flat archival store cannot express "the Human block is always in the prompt; the Persona block is always in the prompt; the Task block swaps per session."
   中文翻译：**结构丢失。** 扁平的归档存储无法表达"Human 块始终在提示中；Persona 块始终在提示中；Task 块按会话交换。"

Letta (letta.com) is the 2026 rewrite. Memory blocks make structure explicit; sleep-time compute moves consolidation off the critical path.

> Letta（letta.com）是 2026 年的重写。记忆块使结构显式化；休眠计算将合并移出关键路径。

> **【中文解读】** 记忆块（Memory Blocks）和休眠计算（Sleep-Time Compute）是 MemGPT/Letta 的两种优化策略。记忆块是固定大小的上下文分区，类似于内存页，用于精细控制上下文窗口中各类信息的占比。休眠计算指在用户不活跃时预先处理和压缩记忆，减少下次会话的延迟。

> **【拓展：Letta 的演进】** Letta（原 MemGPT）在 2024-2025 年的演进中引入了记忆块和休眠计算两个关键概念。记忆块将上下文窗口划分为系统指令、核心记忆、对话历史等固定分区，避免信息混淆。休眠计算利用空闲时间做记忆整理和预计算，类似于操作系统的后台内存整理（compaction）。

## The Concept | 核心概念

### Three tiers

| Tier | Scope | Where it lives | Written by |
|------|-------|----------------|------------|
| 层级 | 范围 | 存储位置 | 写入者 |
| Core | Always visible | Inside the main prompt | Agent tool call + sleep-time rewrites / Agent 工具调用 + 休眠重写 |
| Recall | Conversation history | Retrievable | Automatic turn logging / 自动轮次日志 |
| Archival | Arbitrary facts | Vector + KV + graph | Agent tool call + sleep-time ingest / Agent 工具调用 + 休眠摄取 |

Core is the MemGPT core. Recall is the conversation buffer with its evicted tail. Archival is the external store. The split cleans up MemGPT's two-tier overloading.

> Core 是 MemGPT 的核心。Recall 是带驱逐尾部的对话缓冲区。Archival 是外部存储。这种拆分清理了 MemGPT 两层的过度加载。

### Memory blocks

A block is a typed, persistent, editable section of the core tier. The original MemGPT paper defined two:

> 块是 core 层的类型化、持久化、可编辑分区。原始 MemGPT 论文定义了两个：

- **Human block** — facts about the user (name, role, preferences, goals).
  中文翻译：**Human 块**——关于用户的事实（姓名、角色、偏好、目标）。
- **Persona block** — the agent's self-concept (identity, tone, constraints).
  中文翻译：**Persona 块**——Agent 的自我概念（身份、语气、约束）。

Letta generalizes to arbitrary user-defined blocks: a `Task` block for the current goal, a `Project` block for codebase facts, a `Safety` block for hard constraints. Each block has an `id`, `label`, `value`, `limit` (character cap), `description` (so the model knows when to edit it).

> Letta 泛化为任意用户定义块：用于当前目标的 `Task` 块、用于代码库事实的 `Project` 块、用于硬约束的 `Safety` 块。每个块有 `id`、`label`、`value`、`limit`（字符上限）、`description`（让模型知道何时编辑它）。

Blocks are editable via the tool surface:

> 块通过工具接口可编辑：

- `block_append(label, text)`
  中文翻译：`block_append(label, text)`——向块追加文本。
- `block_replace(label, old, new)`
  中文翻译：`block_replace(label, old, new)`——替换块中的文本。
- `block_read(label)`
  中文翻译：`block_read(label)`——读取块内容。
- `block_summarize(label)` — condense a block that is near its limit.
  中文翻译：`block_summarize(label)`——压缩接近上限的块。

### Sleep-time compute

The 2025 Letta addition: run a second agent in background, off the critical path. Sleep-time agents process conversation transcripts and codebase context, write `learned_context` into shared blocks, and consolidate or invalidate archival records.

> 2025 年 Letta 的新增功能：在后台运行第二个 Agent，不在关键路径上。休眠 Agent 处理对话记录和代码库上下文，将 `learned_context` 写入共享块，并合并或使归档记录失效。

Properties that fall out:

> 随之产生的特性：

- **No latency cost.** Primary responses do not wait for memory ops.
  中文翻译：**无延迟成本。** 主响应不等待记忆操作。
- **Stronger model allowed.** The sleep-time agent can be a more expensive, slower model because it is not latency-constrained.
  中文翻译：**允许更强的模型。** 休眠 Agent 可以是更昂贵、更慢的模型，因为它不受延迟约束。
- **Natural consolidation window.** Dedup, summarize, invalidate contradicted facts when the user is not waiting.
  中文翻译：**天然的合并窗口。** 在用户不等待时去重、摘要、使矛盾事实失效。

The shape matches how humans work: you do the task, you sleep on it, the long-term memory settles overnight.

> 这种形态与人类工作方式一致：你做任务，你睡一觉，长期记忆在夜间沉淀。

### Letta V1 and native reasoning

Letta V1 (`letta_v1_agent`, 2026) deprecates `send_message`/heartbeat and inline `Thought:` tokens in favor of native reasoning. The Responses API (OpenAI) and the Messages API with extended thinking (Anthropic) emit reasoning on a separate channel, passed through turns (encrypted across providers in production). The control loop is still ReAct. The thought trace is structural, not prompt-shaped.

> Letta V1（`letta_v1_agent`，2026）弃用了 `send_message`/心跳和内联 `Thought:` token，转而使用原生推理。Responses API（OpenAI）和带扩展思考的 Messages API（Anthropic）在独立通道上输出推理，跨回合透传（在生产环境中跨提供商加密）。控制循环仍然是 ReAct。思维轨迹是结构性的，不是提示形式的。

### Where this pattern goes wrong

- **Block bloat.** Infinite `block_append` hits the limit fast. Wire a block summarizer before the write that pushes over the cap.
  中文翻译：**块膨胀。** 无限的 `block_append` 很快达到上限。在超出上限的写入之前接入块摘要器。
- **Silent drift.** Sleep-time agent rewrites a block and the primary agent never notices. Version blocks and surface diffs in the trace.
  中文翻译：**静默漂移。** 休眠 Agent 重写块但主 Agent 从未注意到。版本化块并在轨迹中显示差异。
- **Poisoned consolidation.** Sleep-time agent processes attacker-reachable content into core. Lesson 27 applies to the sleep-time surface too.
  中文翻译：**投毒合并。** 休眠 Agent 将攻击者可达的内容处理进 core。第 27 课也适用于休眠接口。

## Build It | 动手构建

`code/main.py` implements:

> `code/main.py` 实现了：

- `Block` — id, label, value, limit, description.
  中文翻译：`Block`——id、label、value、limit、description。
- `BlockStore` — CRUD + `near_limit(label)` helper.
  中文翻译：`BlockStore`——CRUD + `near_limit(label)` 辅助方法。
- Two scripted agents — `PrimaryAgent` serves a turn, `SleepTimeAgent` consolidates between turns.
  中文翻译：两个脚本 Agent——`PrimaryAgent` 提供轮次，`SleepTimeAgent` 在轮次间合并。
- A trace that shows a three-turn conversation with block writes, plus a sleep-time pass that summarizes a block and invalidates a stale fact.
  中文翻译：展示三轮对话带块写入的轨迹，加上压缩块和使过时事实失效的休眠处理。

Run it:

> 运行：

```
python3 code/main.py
```

The transcript shows the split: primary turns are fast and produce raw writes; the sleep pass compacts and cleans up.

> 转录记录显示了分工：主轮次快速产生原始写入；休眠处理压缩和清理。

## Use It | 用框架实现

- **Letta** (letta.com) for the reference implementation. Self-host or managed cloud.
  中文翻译：**Letta**（letta.com）参考实现。自托管或托管云。
- **Claude Agent SDK skills** as block-shaped knowledge — a skill is a named, versioned, retrievable block of instructions the agent loads on demand.
  中文翻译：**Claude Agent SDK skills** 作为块状知识——skill 是命名的、版本化的、可检索的指令块，Agent 按需加载。
- **Custom builds** for teams that want control over the storage backend. Use the Letta API contract so you can migrate later.
  中文翻译：**自定义构建**——适合想要控制存储后端的团队。使用 Letta API 契约以便后续迁移。

## Ship It | 产出物

`outputs/skill-memory-blocks.md` generates a Letta-shaped block system with sleep-time hooks for any runtime, including safety rules and citation wiring.

> `outputs/skill-memory-blocks.md` 为任何运行时生成 Letta 形状的块系统，带休眠钩子、安全规则和引用连接。

## Exercises | 练习题

1. Add a `block_summarize` tool that replaces the block value with a model-generated summary when `near_limit` returns true. Which trigger threshold minimizes both summarization calls and block overflow?
   中文翻译：添加 `block_summarize` 工具，在 `near_limit` 返回 true 时用模型生成的摘要替换块值。哪个触发阈值最小化摘要调用和块溢出？
2. Implement sleep-time dedup over archival: two records whose text has >90% token overlap collapse to one. Do it only in the sleep pass, never on the critical path.
   中文翻译：在归档存储上实现休眠去重：token 重叠 >90% 的两条记录合并为一条。只在休眠处理中做，从不在关键路径上做。
3. Version blocks. On every write record the old value and a diff. Expose `block_history(label)` so operators can debug "why did the agent forget X."
   中文翻译：版本化块。每次写入记录旧值和差异。暴露 `block_history(label)` 让运维可以调试"为什么 Agent 忘记了 X"。
4. Treat sleep-time agents as untrusted writers. When they touch the Persona or Safety block, require a second-agent review before committing.
   中文翻译：将休眠 Agent 视为不可信写入者。当它们触碰 Persona 或 Safety 块时，提交前需要第二个 Agent 审查。
5. Port the example to use the Letta API (`letta_v1_agent`). What changes in the block schema, and how does native reasoning alter the trace shape?
   中文翻译：将示例移植为使用 Letta API（`letta_v1_agent`）。块模式有什么变化？原生推理如何改变轨迹形态？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Memory block | "Editable prompt section" / "可编辑提示分区" | Typed, persistent, LLM-editable segment of core memory / 类型化、持久化、LLM 可编辑的核心记忆段 |
| Human block | "User memory" / "用户记忆" | Facts about the user, pinned in core / 关于用户的事实，固定在 core 中 |
| Persona block | "Agent identity" / "Agent 身份" | Self-concept, tone, constraints, pinned in core / 自我概念、语气、约束，固定在 core 中 |
| Sleep-time compute | "Async memory work" / "异步记忆工作" | Second agent doing consolidation off the critical path / 第二个 Agent 在关键路径之外做合并 |
| Core / Recall / Archival | "Tiers" / "层级" | Three-layer memory split: always-visible / conversation / external / 三层记忆拆分：始终可见 / 对话 / 外部 |
| Block limit | "Cap" / "上限" | Character limit per block; forces summarization / 每个块的字符限制；强制摘要 |
| Native reasoning | "Thinking channel" / "思考通道" | Provider-level reasoning output, not prompt-level `Thought:` / 提供商级推理输出，非提示级 `Thought:` |
| Learned context | "Sleep output" / "休眠输出" | Facts the sleep-time agent writes into shared blocks / 休眠 Agent 写入共享块的事实 |

## Further Reading | 延伸阅读

- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) — the block pattern
  中文翻译：Letta 记忆块博客——块模式。
- [Letta, Sleep-time Compute blog](https://www.letta.com/blog/sleep-time-compute) — async consolidation
  中文翻译：Letta 休眠计算博客——异步合并。
- [Letta, Rearchitecting the Agent Loop](https://www.letta.com/blog/letta-v1-agent) — native reasoning rewrite
  中文翻译：Letta 重建 Agent 循环博客——原生推理重写。
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) — the origin
  中文翻译：MemGPT 论文——起源。
