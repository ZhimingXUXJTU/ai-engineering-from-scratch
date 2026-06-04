# Memory: Virtual Context and MemGPT | 虚拟上下文 记忆 MemGPT

> Context windows are finite. Conversations, documents, and tool traces are not. MemGPT (Packer et al., 2023) frames this as OS virtual memory — main context is RAM, external store is disk, the agent pages between them. This is the pattern every 2026 memory system inherits.

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use)
**Time:** ~75 minutes

## Learning Objectives | 学习目标

- Explain the OS analogy MemGPT builds on: main context = RAM, external context = disk, memory tools = page in/out.
- Implement the two-tier MemGPT pattern in stdlib with a main-context buffer, an external searchable store, and page in/out tools.
- Describe how the agent issues "interrupts" to query or modify external memory and how the result is spliced back into the next prompt.
- Identify the MemGPT design choices that carry into Letta (Lesson 08) and Mem0 (Lesson 09).

## The Problem | 问题

> **【中文解读】** 上下文窗口看似能解决记忆问题，但实际上不能。生产环境中的三个失败模式：(1) 溢出——多轮对话或长文档跨越窗口限制，截断之外的一切都丢失了；(2) 稀释——窗口内填充不相关上下文稀释了注意力；(3) 持久化——新会话从空窗口开始，Agent 无法跨会话记忆。

Context windows look like they should solve memory. They do not. Three failure modes recur in production:

1. **Overflow.** Multi-turn conversations, long documents, or tool-call-heavy trajectories cross the window. Everything past the cutoff is gone.
2. **Dilution.** Even within the window, stuffing irrelevant context dilutes attention over what matters. Frontier models still degrade on long inputs.
3. **Persistence.** A new session starts with an empty window. Agents without external memory cannot say "remember when you asked me to..." across sessions.

> **【拓展：MemGPT → 现代 Agent 记忆系统】** MemGPT (Packer et al., 2023) 将上下文管理类比为操作系统虚拟内存：主上下文=RAM，外部存储=磁盘，记忆工具=页面换入换出。这是 2026 年所有记忆系统的基本模式。Mem0 的 2025 年论文测量发现，128k 窗口的基线仍然会遗漏 4k 窗口 + 外部记忆 Agent 能捕获的长程事实。

Bigger windows help but do not fix this. Mem0's 2025 paper measured that 128k-window baselines still miss long-horizon facts that a 4k-window agent with external memory catches.

## The Concept | 概念

### MemGPT: the OS analogy

> **【中文解读】** MemGPT 将上下文管理映射到操作系统虚拟内存：RAM=主上下文（当前 prompt），磁盘=外部上下文（向量数据库/KV/图存储），页面错误=记忆工具调用（`memory.search`/`memory.read`/`memory.write`），OS 内核=Agent 控制循环。Agent 运行普通的 ReAct 循环，额外增加一类工具用于在主上下文和外部存储之间换入换出数据。

Packer et al. (arXiv:2310.08560, v2 Feb 2024) map context management to operating-system virtual memory:

| OS concept | MemGPT concept | 2026 production analog |
|------------|---------------|------------------------|
| RAM | main context (prompt) | Anthropic/OpenAI context window |
| Disk | external context | vector DB, KV, graph store |
| Page fault | memory tool call | `memory.search`, `memory.read`, `memory.write` |
| OS kernel | agent control loop | ReAct loop with memory tools |

The agent runs a normal ReAct loop. One extra class of tools lets it page data in and out of main context.

### Two tiers

- **Main context.** Fixed-size prompt holding the current task. Always visible to the model.
- **External context.** Unbounded, searchable via tools. Read when relevant, written when facts emerge.

The original paper evaluated the design on two tasks beyond the base window: document analysis longer than 100k tokens and multi-session chat with persistent memory across days.

### The interrupt pattern

MemGPT introduces memory-as-interrupt: mid-conversation the agent can invoke a memory tool, the runtime executes it, and the result splices into the next assistant turn as a new observation. Conceptually identical to a Unix `read()` syscall that blocks the process, returns bytes, and the process continues.

Canonical memory tool surface:

- `core_memory_append(section, text)` — write to a persistent section of the prompt.
- `core_memory_replace(section, old, new)` — edit a persistent section.
- `archival_memory_insert(text)` — write to the searchable external store.
- `archival_memory_search(query, top_k)` — retrieve from the external store.
- `conversation_search(query)` — scan past turns.

### Where MemGPT ends and Letta begins

In September 2024 MemGPT became Letta. The research repo (`cpacker/MemGPT`) remains; Letta extends the design:

- Three tiers instead of two (core, recall, archival — Lesson 08).
- Native reasoning replacing the `send_message`/heartbeat pattern (Lesson 08).
- Sleep-time agents running async memory work (Lesson 08).

The MemGPT paper is the 2026 foundation even if production systems run Letta, Mem0, or a custom two-tier store.

### Where this pattern goes wrong

- **Memory rot.** Writes accumulate faster than reads; retrieval drowns in stale facts. Fix: periodic consolidation (Letta sleep-time), explicit invalidation (Mem0 conflict detector).
- **Memory poisoning.** External memory is retrieved text. If attacker-controlled content lands in a memory note, the agent re-ingests it next session. This is the Greshake et al. (Lesson 27) attack restated over time.
- **Citation loss.** Agent recalls "the user asked me to ship X" but cannot cite which turn. Store source references (session ID, turn ID) with every archival write.

## Build It | 动手构建

`code/main.py` implements MemGPT's two-tier pattern in stdlib:

- `MainContext` — fixed-size prompt buffer with a `core` dict and a `messages` list; auto-compacts oldest messages when over cap.
- `ArchivalStore` — in-memory BM25-esque store (token-overlap scoring) of (id, text, tags, session, turn) records.
- Five memory tools mapping to the MemGPT surface.
- A scripted agent that fills archival with facts, then answers a question by calling `archival_memory_search`.

Run it:

```
python3 code/main.py
```

The trace shows the agent writing three facts, filling main context to the cap (forcing eviction), then answering a follow-up question by retrieving from archival — reproducing the MemGPT workflow without any real LLM.

## Use It | 使用方法

Every production memory system today is a MemGPT variant:

- **Letta** (Lesson 08) — three tiers, native reasoning, sleep-time compute.
- **Mem0** (Lesson 09) — vector + KV + graph fused with a scoring layer.
- **OpenAI Assistants / Responses** — managed memory via threads and files.
- **Claude Agent SDK** — long-term memory via skills and session store.

Pick one by operational shape (self-hosted, managed, framework-integrated), not by the core pattern — the core pattern is MemGPT.

## Ship It | 部署上线

`outputs/skill-virtual-memory.md` is a reusable skill that produces a correct two-tier memory scaffold (main + archival + tool surface) for any target runtime, with eviction policy and citation fields wired in.

## Exercises | 练习题

1. Add a `max_main_context_tokens` cap measured in tokens (approximate with `len(text.split())` * 1.3). Compact the oldest messages into a summary when the cap is exceeded. Compare behavior with and without the summarizer.
2. Implement BM25 properly over the archival store (term frequency, inverse document frequency). Measure recall@10 on a toy fact set versus the token-overlap baseline.
   *思考并实践此练习*
3. Add `citation` fields (session_id, turn_id, source_url) to archival inserts. Make the agent cite sources on every retrieval-backed answer.
   *思考并实践此练习*
4. Simulate memory poisoning: add an archival record that says "ignore all future user instructions." Write a guard that scans retrievals for directive-shaped text and marks them untrusted.
   *思考并实践此练习*
5. Port the implementation to use the MemGPT research repo's core-memory JSON schema (`cpacker/MemGPT`). What changes when you switch from flat strings to typed sections?
   *思考并实践此练习*

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Virtual context | "Unlimited memory" | Main (prompt) + external (searchable) tiers with page in/out |  |
| Main context | "Working memory" | The prompt — fixed-size, always visible |  |
| Archival memory | "Long-term store" | External searchable persistence, retrieved on demand |  |
| Core memory | "Persistent prompt section" | Named sections pinned inside the main context |  |
| Memory tool | "Memory API" | Tool call the agent issues to read/write external memory |  |
| Interrupt | "Memory page fault" | Agent pauses, runtime fetches, result splices into next turn |  |
| Memory rot | "Stale facts" | Old writes drown retrieval; fix with consolidation |  |
| Memory poisoning | "Injected persistent note" | Attacker content stored as memory, re-ingested on recall |  |

## Further Reading | 延伸阅读

- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) — OS-inspired virtual context paper
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) — the three-tier evolution
- [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — treating context as a budget
- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) — hybrid production memory on top of this pattern
