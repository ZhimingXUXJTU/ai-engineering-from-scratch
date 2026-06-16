# Memory: Virtual Context and MemGPT | 记忆：虚拟上下文与 MemGPT

> Context windows are finite. Conversations, documents, and tool traces are not. MemGPT (Packer et al., 2023) frames this as OS virtual memory — main context is RAM, external store is disk, the agent pages between them. This is the pattern every 2026 memory system inherits.

> **【中文解读】** 上下文窗口是有限的，但对话、文档和工具轨迹不是。MemGPT 将此类比为操作系统虚拟内存——主上下文是 RAM，外部存储是磁盘，Agent 在两者之间换页。这是 2026 年所有记忆系统继承的模式。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 06 (工具使用)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Explain the OS analogy MemGPT builds on: main context = RAM, external context = disk, memory tools = page in/out.
  中文翻译：解释 MemGPT 所基于的操作系统类比：主上下文 = RAM，外部上下文 = 磁盘，记忆工具 = 页面换入/换出。
- Implement the two-tier MemGPT pattern in stdlib with a main-context buffer, an external searchable store, and page in/out tools.
  中文翻译：用标准库实现两层 MemGPT 模式，包含主上下文缓冲区、外部可搜索存储和页面换入/换出工具。
- Describe how the agent issues "interrupts" to query or modify external memory and how the result is spliced back into the next prompt.
  中文翻译：描述 Agent 如何发出"中断"来查询或修改外部记忆，以及结果如何被拼接回下一个提示。
- Identify the MemGPT design choices that carry into Letta (Lesson 08) and Mem0 (Lesson 09).
  中文翻译：识别 MemGPT 中延续到 Letta（第 8 课）和 Mem0（第 9 课）的设计选择。

## The Problem | 问题引入

Context windows look like they should solve memory. They do not. Three failure modes recur in production:

> 上下文窗口看似能解决记忆问题，但实际上不能。生产环境中反复出现三种失败模式：

1. **Overflow.** Multi-turn conversations, long documents, or tool-call-heavy trajectories cross the window. Everything past the cutoff is gone.
   中文翻译：**溢出。** 多轮对话、长文档或工具调用密集的轨迹跨越窗口限制。截断之外的一切都丢失了。
2. **Dilution.** Even within the window, stuffing irrelevant context dilutes attention over what matters. Frontier models still degrade on long inputs.
   中文翻译：**稀释。** 即使在窗口内，填充不相关的上下文也稀释了对重要内容的注意力。前沿模型在长输入上仍然退化。
3. **Persistence.** A new session starts with an empty window. Agents without external memory cannot say "remember when you asked me to..." across sessions.
   中文翻译：**持久化。** 新会话从空窗口开始。没有外部记忆的 Agent 无法跨会话说"记得你让我……"。

> **【中文解读】** 上下文窗口看似能解决记忆问题，但实际上不能。生产环境中的三个失败模式：(1) 溢出——多轮对话或长文档跨越窗口限制，截断之外的一切都丢失了；(2) 稀释——窗口内填充不相关上下文稀释了注意力；(3) 持久化——新会话从空窗口开始，Agent 无法跨会话记忆。

Bigger windows help but do not fix this. Mem0's 2025 paper measured that 128k-window baselines still miss long-horizon facts that a 4k-window agent with external memory catches.

> 更大的窗口有帮助但不能解决这个问题。Mem0 的 2025 年论文测量发现，128k 窗口的基线仍然会遗漏 4k 窗口 + 外部记忆 Agent 能捕获的长程事实。

> **【拓展：MemGPT → 现代 Agent 记忆系统】** MemGPT (Packer et al., 2023) 将上下文管理类比为操作系统虚拟内存：主上下文=RAM，外部存储=磁盘，记忆工具=页面换入换出。这是 2026 年所有记忆系统的基本模式。Mem0 的 2025 年论文测量发现，128k 窗口的基线仍然会遗漏 4k 窗口 + 外部记忆 Agent 能捕获的长程事实。

> 🔗 **【前置】** 必须先掌握：Phase 14·01（Agent Loop）——MemGPT 的记忆工具是普通工具调用的扩展；Phase 14·06（Tool Use）——记忆操作通过工具实现。还需要操作系统基础知识——如果你不知道"虚拟内存""页面错误"是什么，先去补操作系统课，否则类比看不懂。

## The Concept | 核心概念

### MemGPT: the OS analogy

Packer et al. (arXiv:2310.08560, v2 Feb 2024) map context management to operating-system virtual memory:

> Packer 等人（arXiv:2310.08560，v2 2024 年 2 月）将上下文管理映射到操作系统虚拟内存：

| OS concept | MemGPT concept | 2026 production analog |
|------------|---------------|------------------------|
| OS 概念 | MemGPT 概念 | 2026 生产环境类比 |
| RAM | main context (prompt) | Anthropic/OpenAI context window / 主上下文（提示） |
| Disk | external context | vector DB, KV, graph store / 外部上下文（向量数据库、KV、图存储） |
| Page fault | memory tool call | `memory.search`, `memory.read`, `memory.write` / 记忆工具调用 |
| OS kernel | agent control loop | ReAct loop with memory tools / 带记忆工具的 ReAct 循环 |

The agent runs a normal ReAct loop. One extra class of tools lets it page data in and out of main context.

> 💡 **【类比】** MemGPT 像你电脑的内存管理：RAM（主上下文）只有 8GB 但要跑 Photoshop + 浏览器 + IDE；操作系统通过页面换入换出（page in/out）让你"感觉"有无穷内存。MemGPT 让 Agent 也这样做——主上下文塞不下时，Agent 自己调用 `archival_memory_search` 把相关内容"换入"，调用 `core_memory_replace` 把无关内容"换出"。Agent 像操作系统内核，记忆工具像系统调用。

> Agent 运行普通的 ReAct 循环。额外的一类工具让它可以在主上下文和外部存储之间换入换出数据。

> **【中文解读】** MemGPT 将上下文管理映射到操作系统虚拟内存：RAM=主上下文（当前 prompt），磁盘=外部上下文（向量数据库/KV/图存储），页面错误=记忆工具调用（`memory.search`/`memory.read`/`memory.write`），OS 内核=Agent 控制循环。Agent 运行普通的 ReAct 循环，额外增加一类工具用于在主上下文和外部存储之间换入换出数据。

### Two tiers

- **Main context.** Fixed-size prompt holding the current task. Always visible to the model.
  中文翻译：**主上下文。** 固定大小的提示，承载当前任务。模型始终可见。
- **External context.** Unbounded, searchable via tools. Read when relevant, written when facts emerge.
  中文翻译：**外部上下文。** 无界的，通过工具可搜索。相关时读取，出现事实时写入。

The original paper evaluated the design on two tasks beyond the base window: document analysis longer than 100k tokens and multi-session chat with persistent memory across days.

> 原论文在两个超出基础窗口的任务上评估了该设计：超过 100k token 的文档分析和跨天持久化记忆的多会话聊天。

### The interrupt pattern

MemGPT introduces memory-as-interrupt: mid-conversation the agent can invoke a memory tool, the runtime executes it, and the result splices into the next assistant turn as a new observation. Conceptually identical to a Unix `read()` syscall that blocks the process, returns bytes, and the process continues.

> MemGPT 引入了记忆即中断：在对话中 Agent 可以调用记忆工具，运行时执行它，结果作为新观察拼接到下一个助手轮次中。概念上等同于 Unix `read()` 系统调用——阻塞进程、返回字节、进程继续。

Canonical memory tool surface:

> 标准记忆工具接口：

- `core_memory_append(section, text)` — write to a persistent section of the prompt.
  中文翻译：`core_memory_append(section, text)`——写入提示的持久化分区。
- `core_memory_replace(section, old, new)` — edit a persistent section.
  中文翻译：`core_memory_replace(section, old, new)`——编辑持久化分区。
- `archival_memory_insert(text)` — write to the searchable external store.
  中文翻译：`archival_memory_insert(text)`——写入可搜索的外部存储。
- `archival_memory_search(query, top_k)` — retrieve from the external store.
  中文翻译：`archival_memory_search(query, top_k)`——从外部存储检索。
- `conversation_search(query)` — scan past turns.
  中文翻译：`conversation_search(query)`——扫描过去的轮次。

### Where MemGPT ends and Letta begins

In September 2024 MemGPT became Letta. The research repo (`cpacker/MemGPT`) remains; Letta extends the design:

> 2024 年 9 月 MemGPT 成为 Letta。研究仓库（`cpacker/MemGPT`）仍然存在；Letta 扩展了设计：

- Three tiers instead of two (core, recall, archival — Lesson 08).
  中文翻译：三层而非两层（core、recall、archival——第 8 课）。
- Native reasoning replacing the `send_message`/heartbeat pattern (Lesson 08).
  中文翻译：原生推理替代 `send_message`/心跳模式（第 8 课）。
- Sleep-time agents running async memory work (Lesson 08).
  中文翻译：运行异步记忆工作的睡眠时间 Agent（第 8 课）。

The MemGPT paper is the 2026 foundation even if production systems run Letta, Mem0, or a custom two-tier store.

> MemGPT 论文是 2026 年的基础，即使生产系统运行 Letta、Mem0 或自定义两层存储。

### Where this pattern goes wrong

> ⚠️ **【易错点】** MemGPT 新手最容易忽略"记忆投毒"：把外部网页、用户消息直接 `archival_memory_insert` 进外部存储。**后果**：攻击者在网页里藏 prompt injection（如"忽略之前所有指令"），下次 Agent 检索到这条记忆时，指令被执行。**一行修复**：所有进入 archival 的外部内容必须先做安全过滤（参考 Phase 14·27 prompt injection 防护），并存储 source 字段用于追溯。

- **Memory rot.** Writes accumulate faster than reads; retrieval drowns in stale facts. Fix: periodic consolidation (Letta sleep-time), explicit invalidation (Mem0 conflict detector).
  中文翻译：**记忆腐化。** 写入积累速度快于读取；检索被过时事实淹没。修复：定期合并（Letta sleep-time）、显式失效（Mem0 冲突检测器）。
- **Memory poisoning.** External memory is retrieved text. If attacker-controlled content lands in a memory note, the agent re-ingests it next session. This is the Greshake et al. (Lesson 27) attack restated over time.
  中文翻译：**记忆投毒。** 外部记忆是检索到的文本。如果攻击者控制的内容进入了记忆笔记，Agent 在下次会话中会重新摄取它。这是 Greshake 等人（第 27 课）攻击的跨时间版本。
- **Citation loss.** Agent recalls "the user asked me to ship X" but cannot cite which turn. Store source references (session ID, turn ID) with every archival write.
  中文翻译：**引用丢失。** Agent 回忆"用户让我发布 X"但无法引用哪一轮。每次归档写入时存储来源引用（会话 ID、轮次 ID）。

> 🤔 **【困惑】** Q: 既然 2026 年模型上下文窗口已经 1M token 了（Gemini 1.5 Pro），还需要 MemGPT 这种"虚拟内存"吗？ A: 需要。窗口大不代表用得对——硬塞 1M token 会触发"中段遗忘"（lost in the middle 现象）和注意力稀释，模型对中间内容的注意力显著低于首尾。MemGPT 的核心价值不是"装下"，而是"在正确时刻只让相关内容可见"。

## Build It | 动手构建

`code/main.py` implements MemGPT's two-tier pattern in stdlib:

> `code/main.py` 用标准库实现了 MemGPT 的两层模式：

- `MainContext` — fixed-size prompt buffer with a `core` dict and a `messages` list; auto-compacts oldest messages when over cap.
  中文翻译：`MainContext`——固定大小的提示缓冲区，带 `core` 字典和 `messages` 列表；超出上限时自动压缩最旧的消息。
- `ArchivalStore` — in-memory BM25-esque store (token-overlap scoring) of (id, text, tags, session, turn) records.
  中文翻译：`ArchivalStore`——内存中的类 BM25 存储（token 重叠评分），存储 (id, text, tags, session, turn) 记录。
- Five memory tools mapping to the MemGPT surface.
  中文翻译：映射到 MemGPT 接口的五个记忆工具。
- A scripted agent that fills archival with facts, then answers a question by calling `archival_memory_search`.
  中文翻译：一个脚本 Agent，用事实填充归档存储，然后通过调用 `archival_memory_search` 回答问题。

Run it:

> 运行：

```
python3 code/main.py
```

The trace shows the agent writing three facts, filling main context to the cap (forcing eviction), then answering a follow-up question by retrieving from archival — reproducing the MemGPT workflow without any real LLM.

> 轨迹显示 Agent 写入三个事实、将主上下文填满到上限（强制驱逐）、然后通过从归档存储检索来回答后续问题——在没有任何真实 LLM 的情况下重现了 MemGPT 工作流。

## Use It | 用框架实现

Every production memory system today is a MemGPT variant:

> 今天每个生产记忆系统都是 MemGPT 的变体：

- **Letta** (Lesson 08) — three tiers, native reasoning, sleep-time compute.
  中文翻译：**Letta**（第 8 课）——三层、原生推理、睡眠时间计算。
- **Mem0** (Lesson 09) — vector + KV + graph fused with a scoring layer.
  中文翻译：**Mem0**（第 9 课）——向量 + KV + 图与评分层融合。
- **OpenAI Assistants / Responses** — managed memory via threads and files.
  中文翻译：**OpenAI Assistants / Responses**——通过线程和文件管理的记忆。
- **Claude Agent SDK** — long-term memory via skills and session store.
  中文翻译：**Claude Agent SDK**——通过 skills 和会话存储实现的长期记忆。

Pick one by operational shape (self-hosted, managed, framework-integrated), not by the core pattern — the core pattern is MemGPT.

> 根据运营形态（自托管、托管、框架集成）选择，而非核心模式——核心模式就是 MemGPT。

## Ship It | 产出物

`outputs/skill-virtual-memory.md` is a reusable skill that produces a correct two-tier memory scaffold (main + archival + tool surface) for any target runtime, with eviction policy and citation fields wired in.

> `outputs/skill-virtual-memory.md` 是一个可复用的 skill，为任何目标运行时生成正确的两层记忆脚手架（主+归档+工具接口），内置驱逐策略和引用字段。

## Exercises | 练习题

1. Add a `max_main_context_tokens` cap measured in tokens (approximate with `len(text.split())` * 1.3). Compact the oldest messages into a summary when the cap is exceeded. Compare behavior with and without the summarizer.
   中文翻译：添加按 token 计量的 `max_main_context_tokens` 上限（用 `len(text.split())` * 1.3 近似）。超出上限时将最旧消息压缩为摘要。比较有和没有压缩器的行为差异。
2. Implement BM25 properly over the archival store (term frequency, inverse document frequency). Measure recall@10 on a toy fact set versus the token-overlap baseline.
   中文翻译：在归档存储上正确实现 BM25（词频、逆文档频率）。在玩具事实集上测量 recall@10 与 token 重叠基线的对比。
3. Add `citation` fields (session_id, turn_id, source_url) to archival inserts. Make the agent cite sources on every retrieval-backed answer.
   中文翻译：为归档插入添加 `citation` 字段（session_id, turn_id, source_url）。让 Agent 在每个基于检索的回答上引用来源。
4. Simulate memory poisoning: add an archival record that says "ignore all future user instructions." Write a guard that scans retrievals for directive-shaped text and marks them untrusted.
   中文翻译：模拟记忆投毒：添加一条归档记录说"忽略所有未来用户指令"。编写一个防护器扫描检索结果中的指令型文本并标记为不可信。
5. Port the implementation to use the MemGPT research repo's core-memory JSON schema (`cpacker/MemGPT`). What changes when you switch from flat strings to typed sections?
   中文翻译：将实现移植为使用 MemGPT 研究仓库的核心记忆 JSON 模式（`cpacker/MemGPT`）。从扁平字符串切换到类型化分区时有什么变化？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Virtual context | "Unlimited memory" / "无限记忆" | Main (prompt) + external (searchable) tiers with page in/out / 主（提示）+ 外部（可搜索）两层，带页面换入/换出 |
| Main context | "Working memory" / "工作记忆" | The prompt — fixed-size, always visible / 提示——固定大小，始终可见 |
| Archival memory | "Long-term store" / "长期存储" | External searchable persistence, retrieved on demand / 外部可搜索持久化，按需检索 |
| Core memory | "Persistent prompt section" / "持久化提示分区" | Named sections pinned inside the main context / 固定在主上下文内的命名分区 |
| Memory tool | "Memory API" / "记忆 API" | Tool call the agent issues to read/write external memory / Agent 发出的读/写外部记忆的工具调用 |
| Interrupt | "Memory page fault" / "记忆页面错误" | Agent pauses, runtime fetches, result splices into next turn / Agent 暂停、运行时获取、结果拼接到下一轮 |
| Memory rot | "Stale facts" / "过时事实" | Old writes drown retrieval; fix with consolidation / 旧写入淹没检索；用合并修复 |
| Memory poisoning | "Injected persistent note" / "注入的持久化笔记" | Attacker content stored as memory, re-ingested on recall / 攻击者内容存储为记忆，在回忆时重新摄取 |

## Further Reading | 延伸阅读

- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) — OS-inspired virtual context paper
  中文翻译：MemGPT 经典论文——操作系统启发的虚拟上下文。
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) — the three-tier evolution
  中文翻译：Letta 记忆块博客——三层演进。
- [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — treating context as a budget
  中文翻译：Anthropic 关于有效上下文工程的文章——将上下文视为预算。
- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) — hybrid production memory on top of this pattern
  中文翻译：Mem0 论文——在此模式之上的混合生产记忆。
