# Why Multi-Agent? | 多 Agent 为什么

> One agent hits a wall. The smart move is not a bigger agent - it is more agents.

> **【中文解读】** 本节介绍了为什么需要多 Agent 系统——单 Agent 的上下文溢出、角色混乱和串行瓶颈问题，以及多 Agent 如何通过分工协作来解决这些问题。

> **【拓展：why multi agent→具体应用】** 单 Agent 在处理复杂任务时面临三个瓶颈：(1) 上下文溢出——所有信息塞进一个窗口，重要的被淹没；(2) 角色混乱——一个 Agent 扮演多个角色导致提示词冲突；(3) 串行执行——工具调用只能排队。多 Agent 通过分工协作解决这些问题。Anthropic 的研究表明，多 Agent 系统在 BrowseComp 基准上比单 Agent 提升 90.2%，80% 的方差仅由 token 使用量解释。

> 🔗 **【前置】** 学本节前请先掌握：Phase 14（Agent Engineering）全部，特别是 Phase 14·01（Agent Loop）和 Phase 14·28（Orchestration Patterns）。本节回答"什么时候用多 Agent"——简单回答：单 Agent + 工具不够时。Anthropic 经验法则：任务需要 > 50 工具调用、或 > 1 个角色（如研究员 + 写手）、或并行能省时间，才考虑多 Agent。

> 💡 **【类比】** 单 Agent vs 多 Agent = 全能管家 vs 专业团队。全能管家（单 Agent）能干所有事但每件都不精：上午做饭、下午修车、晚上辅导作业，每样都半吊子。专业团队（多 Agent）：厨师专做饭、机修工专修车、家教专辅导，每人精一行。代价：协调成本（Agent 间通信）和复杂度增加——简单任务用单 Agent 更划算。

**Type:** Learn | **类型:** 学习
**Languages:** TypeScript | **语言:** TypeScript
**Prerequisites:** Phase 14 (Agent Engineering) | **前置知识:** Phase 14 (Agent 工程)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- Identify the single-agent ceiling (context overflow, mixed expertise, sequential bottleneck) and explain when splitting into multiple agents is the right move
  中文翻译：识别单 Agent 上限（上下文溢出、专业能力混合、串行瓶颈），并解释何时拆分为多个 Agent 是正确的选择
- Compare orchestration patterns (pipeline, parallel fan-out, supervisor, hierarchical) and select the right one for a given task structure
  中文翻译：比较编排模式（流水线、并行扇出、监督者、分层），并为给定任务结构选择合适的模式
- Design a multi-agent system with clear role boundaries, shared state, and a communication contract
  中文翻译：设计一个具有明确角色边界、共享状态和通信契约的多 Agent 系统
- Analyze the tradeoffs of multi-agent complexity (latency, cost, debugging difficulty) versus single-agent simplicity
  中文翻译：分析多 Agent 复杂性（延迟、成本、调试难度）与单 Agent 简单性之间的权衡

## The Problem | 问题引入

You built a single agent in Phase 14. It works. It can read files, run commands, call APIs, and reason about results. Then you point it at a real codebase: 200 files, three languages, tests that depend on infrastructure, and a requirement to research external APIs before writing code.

> 你在 Phase 14 中构建了一个单 Agent。它运行良好，能够读取文件、运行命令、调用 API 并对结果进行推理。然后你将它指向一个真实的代码库：200 个文件、三种语言、依赖基础设施的测试，以及需要先研究外部 API 再编写代码的要求。

The gap between demo agents and production agents is the gap between "one file, one language, one tool" and "many files, many languages, many tools with dependencies." The demo works because the task fits. Production fails because the task does not.

> 演示 Agent 和生产 Agent 之间的差距是"一个文件、一种语言、一个工具"和"许多文件、许多语言、许多有依赖的工具"之间的差距。演示有效因为任务适合。生产失败因为任务不适合。

The agent chokes. Not because the LLM is dumb, but because the task exceeds what one agent loop can handle. The context window fills up with file contents. The agent forgets what it read 40 tool calls ago. It tries to be a researcher, a coder, and a reviewer all at once, and does all three poorly.

> Agent 崩溃了。不是因为 LLM 愚蠢，而是因为任务超出了单个 Agent 循环能处理的范围。上下文窗口被文件内容填满。Agent 忘记了 40 次工具调用前读过的内容。它试图同时扮演研究员、程序员和审阅者三个角色，但三个都做不好。

This is the single-agent ceiling. You hit it every time a task requires:

> 这就是单 Agent 上限。每当任务需要以下条件时你就会遇到：

The ceiling is structural, not algorithmic. A better LLM delays the ceiling but does not remove it. A 1M-token context window fills up just as surely as a 200k one — it just takes more files.

> 上限是结构性的，不是算法性的。更好的 LLM 延迟上限但不移除它。1M token 上下文窗口像 200k 一样确定地填满——只是需要更多文件。

- **More context than fits in one window** - reading 50 files blows past 200k tokens
  中文翻译：**超出一个窗口容量的上下文** — 读取 50 个文件会超过 200k token
- **Different expertise at different stages** - research requires different prompting than code generation
  中文翻译：**不同阶段需要不同的专业知识** — 研究需要与代码生成不同的提示
- **Work that can happen in parallel** - why read three files sequentially when you can read them simultaneously?
  中文翻译：**可以并行执行的工作** — 既然可以同时读取三个文件，为什么要顺序读取？

## The Concept | 核心概念

### The Single-Agent Ceiling

A single agent is one loop, one context window, one system prompt. Picture it:

> 单 Agent 是一个循环、一个上下文窗口、一个系统提示。想象一下：

```
┌─────────────────────────────────────────┐
│            SINGLE AGENT                 │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │         Context Window            │  │
│  │                                   │  │
│  │  research notes                   │  │
│  │  + code files                     │  │
│  │  + test output                    │  │
│  │  + review feedback                │  │
│  │  + API docs                       │  │
│  │  + ...                            │  │
│  │                                   │  │
│  │  ██████████████████████ FULL ███  │  │
│  └───────────────────────────────────┘  │
│                                         │
│  One system prompt tries to cover       │
│  research + coding + review + testing   │
│                                         │
│  Result: mediocre at everything         │
└─────────────────────────────────────────┘
```

The single system prompt is the root cause. It has to give instructions for research, coding, reviewing, and testing simultaneously. Each instruction dilutes the others. The agent ends up "okay" at everything, excellent at nothing.

> 单系统提示是根本原因。它必须同时为研究、编码、审阅和测试提供指令。每条指令稀释其他。Agent 最终在所有事上"还行"，在任何事上都不优秀。

Three things break:

> 三个问题会导致崩溃：

1. **Context saturation** - tool results pile up. By turn 30, the agent has consumed 150k tokens of file contents, command outputs, and prior reasoning. Critical details from turn 5 get lost.
   中文翻译：**上下文饱和** — 工具结果不断堆积。到第 30 轮时，Agent 已消耗 150k token 的文件内容、命令输出和先前推理。第 5 轮的关键细节丢失了。

2. **Role confusion** - a system prompt that says "you are a researcher, coder, reviewer, and tester" produces an agent that half-researches, half-codes, and never finishes reviewing.
   中文翻译：**角色混乱** — 一个写着"你是研究员、程序员、审阅者和测试员"的系统提示会产生一个半研究、半编码、永远完不成审阅的 Agent。

3. **Sequential bottleneck** - the agent reads file A, then file B, then file C. Three serial LLM calls. Three serial tool executions. No parallelism.
   中文翻译：**串行瓶颈** — Agent 读取文件 A，然后文件 B，然后文件 C。三次串行 LLM 调用。三次串行工具执行。没有并行性。

The single agent is a generalist asked to be a specialist at every step. Multi-agent splits the work and lets each agent be a specialist in one thing.

> 单 Agent 是一个被要求在每个步骤都成为专家的通才。多 Agent 拆分工作，让每个 Agent 在一件事上成为专家。

### The Multi-Agent Solution

Split the work. Give each agent one job, one context window, and one system prompt tuned for that job:

> 拆分工作。给每个 Agent 一个任务、一个上下文窗口和一个为该任务调优的系统提示：

This is "separation of concerns" applied to LLM agents. Each agent's prompt is shorter and more focused. Each agent's context window holds only what it needs. Each agent can be tested and improved independently. The orchestrator handles composition.

> 这是应用于 LLM Agent 的"关注点分离"。每个 Agent 的提示更短更聚焦。每个 Agent 的上下文窗口只持有它需要的。每个 Agent 可以独立测试和改进。编排器处理组合。

```
┌──────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                          │
│                                                          │
│  "Build a REST API for user management"                  │
│                                                          │
│         ┌──────────┬──────────┬──────────┐               │
│         │          │          │          │               │
│         ▼          ▼          ▼          ▼               │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│   │RESEARCHER│ │  CODER   │ │ REVIEWER │ │  TESTER  │  │
│   │          │ │          │ │          │ │          │  │
│   │ Reads    │ │ Writes   │ │ Checks   │ │ Runs     │  │
│   │ docs,    │ │ code     │ │ code     │ │ tests,   │  │
│   │ finds    │ │ based on │ │ quality, │ │ reports  │  │
│   │ patterns │ │ research │ │ finds    │ │ results  │  │
│   │          │ │ + spec   │ │ bugs     │ │          │  │
│   └─────┬────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│         │           │            │             │         │
│         └───────────┴────────────┴─────────────┘         │
│                          │                               │
│                     Merge results                        │
└──────────────────────────────────────────────────────────┘
```

Each agent has:
- A focused system prompt ("You are a code reviewer. Your only job is finding bugs.")
  中文翻译：一个聚焦的系统提示（"你是一个代码审阅者。你唯一的任务是发现 bug。"）
- Its own context window (not polluted by other agents' work)
  中文翻译：自己的上下文窗口（不被其他 Agent 的工作污染）
- A clear input/output contract (receives research notes, outputs code)
  中文翻译：清晰的输入/输出契约（接收研究笔记，输出代码）

The orchestrator agent only needs to understand the high-level task and how to delegate. It does not need to know how to do each subtask. Each specialist agent only needs to know its own narrow job. Separation of concerns, applied to LLMs.

> 编排 Agent 只需要理解高层任务和如何委派。它不需要知道如何完成每个子任务。每个专家 Agent 只需要知道自己狭窄的工作。关注点分离，应用于 LLM。

### Real Systems That Do This

**Claude Code subagents** - when Claude Code spawns a subagent with `Task`, it creates a child agent with a scoped task. The parent keeps its context clean. The child does focused work and returns a summary.

> **Claude Code 子 Agent** — 当 Claude Code 使用 `Task` 生成子 Agent 时，它会创建一个具有限定范围的子 Agent。父 Agent 保持上下文清洁。子 Agent 执行聚焦的工作并返回摘要。

The pattern is viral because it composes: a subagent can spawn its own subagents. Three levels deep is common in complex codebase tasks; beyond that, debugging becomes painful.

> 这种模式病毒式传播因为它可组合：子 Agent 可以生成自己的子 Agent。复杂代码库任务中三层深很常见；超过这个深度，调试变得痛苦。

**Devin** - runs a planner agent, a coder agent, and a browser agent. The planner breaks work into steps. The coder writes code. The browser researches documentation. Each has separate context.

> **Devin** — 运行一个规划 Agent、一个编码 Agent 和一个浏览器 Agent。规划器将工作分解为步骤。编码器编写代码。浏览器研究文档。每个都有独立的上下文。

Devin's architecture is the textbook supervisor pattern: one planner that owns the global plan, multiple specialist workers that execute slices. The browser agent is interesting — it is itself a sub-agent with browsing tools, isolated from the coder's context.

> Devin 的架构是教科书式的监督者模式：一个拥有全局计划的规划器、多个执行切片的专家工作器。浏览器 Agent 有趣——它本身是一个带浏览工具的子 Agent，与编码器的上下文隔离。

**Multi-agent coding teams (SWE-bench)** - top-performing systems on SWE-bench use a researcher that reads the codebase, a planner that designs the fix, and a coder that implements it. Single-agent systems score lower.

> **多 Agent 编码团队 (SWE-bench)** — SWE-bench 上表现最好的系统使用一个读取代码库的研究员、一个设计修复方案的规划器和一个实现修复的编码器。单 Agent 系统得分较低。

The 2026 SWE-bench leaderboard is dominated by multi-agent systems. The pattern: a researcher with a large context for codebase understanding, a planner with a focused prompt for fix design, a coder with strict typing requirements for implementation. Each role gets the prompt it needs.

> 2026 年 SWE-bench 排行榜由多 Agent 系统主导。模式：带大上下文的研究员用于代码库理解、带聚焦提示的规划器用于修复设计、带严格类型要求的编码器用于实现。每个角色获得它需要的提示。

**ChatGPT Deep Research** - spawns multiple search agents in parallel, each exploring a different angle, then synthesizes results.

> **ChatGPT Deep Research** — 并行生成多个搜索 Agent，每个探索不同的角度，然后综合结果。

### The Spectrum

Multi-agent is not binary. It is a spectrum:

> 多 Agent 不是二元的。它是一个光谱：

The spectrum framing matters because most production systems are not at either extreme. Claude Code uses subagents (one level deep). Devin uses a small team. Real research systems use 5-50 agents. The right point on the spectrum depends on task complexity.

> 光谱框架重要，因为大多数生产系统不在任一极端。Claude Code 使用子 Agent（一层深）。Devin 使用小团队。真实研究系统使用 5-50 个 Agent。光谱上的正确点取决于任务复杂性。

```
SIMPLE ──────────────────────────────────────────── COMPLEX

 Single        Sub-         Pipeline      Team         Swarm
 Agent         agents

 ┌───┐       ┌───┐        ┌───┐───┐    ┌───┐───┐    ┌─┐┌─┐┌─┐
 │ A │       │ A │        │ A │ B │    │ A │ B │    │ ││ ││ │
 └───┘       └─┬─┘        └───┘─┬─┘    └─┬─┘─┬─┘    └┬┘└┬┘└┬┘
               │                │        │   │       ┌┴──┴──┴┐
             ┌─┴─┐          ┌───┘───┐    │   │       │shared │
             │ a │          │ C │ D │  ┌─┴───┴─┐    │ state │
             └───┘          └───┘───┘  │  msg   │    └───────┘
                                       │  bus   │
 1 loop      Parent +      Stage by    │       │    N peers,
 1 context   child tasks   stage       └───────┘    emergent
                                       Explicit      behavior
                                       roles
```

**Single agent** - one loop, one prompt. Good for simple tasks.

> **单 Agent** — 一个循环，一个提示。适合简单任务。

**Subagents** - a parent spawns children for focused subtasks. The parent maintains the plan. Children report back. This is what Claude Code does.

> **子 Agent** — 父 Agent 为聚焦的子任务生成子 Agent。父 Agent 维护计划。子 Agent 汇报结果。这就是 Claude Code 的做法。

**Pipeline** - agents run in sequence. Agent A's output becomes Agent B's input. Good for staged workflows: research -> code -> review -> test.

> **流水线** — Agent 顺序运行。Agent A 的输出成为 Agent B 的输入。适合分阶段的工作流：研究 -> 编码 -> 审阅 -> 测试。

**Team** - agents run in parallel with a shared message bus. Each has a role. An orchestrator coordinates. Good when different skills are needed simultaneously.

> **团队** — Agent 通过共享消息总线并行运行。每个都有角色。编排器协调。适合需要同时使用不同技能的场景。

**Swarm** - many identical or near-identical agents with shared state. No fixed orchestrator. Agents pick up work from a queue. Good for high-throughput parallel tasks.

> **群体** — 许多相同或近似相同的 Agent 共享状态。没有固定的编排器。Agent 从队列中获取工作。适合高吞吐量的并行任务。

### The Four Multi-Agent Patterns

#### Pattern 1: Pipeline

```
Input ──▶ Agent A ──▶ Agent B ──▶ Agent C ──▶ Output
          (research)  (code)      (review)
```

Each agent transforms the data and passes it forward. Simple to reason about. Failure in one stage blocks the rest.

> 每个 Agent 转换数据并传递给下一个。推理简单。一个阶段的失败会阻塞后续所有阶段。

Use when: each stage has a clear input/output and stages are naturally sequential. Research → code → review → test is the canonical example. Avoid when: stages can run in parallel or need iteration between them.

> 使用场景：每个阶段有清晰的输入/输出且阶段天然顺序执行。研究 → 编码 → 审阅 → 测试是典型例子。避免：阶段可以并行或需要相互迭代时。

#### Pattern 2: Fan-out / Fan-in

```
                ┌──▶ Agent A ──┐
                │              │
Input ──▶ Split ├──▶ Agent B ──├──▶ Merge ──▶ Output
                │              │
                └──▶ Agent C ──┘
```

Split work across parallel agents, then merge results. Good for tasks that decompose into independent subtasks.

> 将工作分配给并行的 Agent，然后合并结果。适合可以分解为独立子任务的任务。

Use when: the task splits cleanly into independent pieces (e.g., search 5 different sources, summarize 10 documents). Avoid when: subtasks depend on each other or merging requires deep reasoning.

> 使用场景：任务可以清晰拆分为独立部分（如搜索 5 个不同来源、总结 10 份文档）。避免：子任务相互依赖或合并需要深度推理时。

#### Pattern 3: Orchestrator-Worker

```
                    ┌──────────┐
                    │  Orch.   │
                    └──┬───┬───┘
                  task │   │ task
                 ┌─────┘   └─────┐
                 ▼               ▼
           ┌──────────┐   ┌──────────┐
           │ Worker A │   │ Worker B │
           └──────────┘   └──────────┘
```

A smart orchestrator decides what to do, delegates to workers, and synthesizes results. The orchestrator is itself an agent with tools for spawning workers.

> 智能编排器决定做什么，委派给工作器，并综合结果。编排器本身是一个具有生成工作器工具的 Agent。

Use when: the task is complex enough that deciding what to do is itself a hard problem. Avoid when: the workflow is fixed and known in advance—use a static pipeline.

> 使用场景：任务足够复杂，决定做什么本身就是一个难题。避免：工作流是固定的且预先已知——使用静态流水线。

#### Pattern 4: Peer Swarm

```
         ┌───┐ ◄──── msg ────▶ ┌───┐
         │ A │                  │ B │
         └─┬─┘                  └─┬─┘
           │                      │
      msg  │    ┌───────────┐     │ msg
           └───▶│  Shared   │◄────┘
                │  State    │
           ┌───▶│  / Queue  │◄────┐
           │    └───────────┘     │
      msg  │                      │ msg
         ┌─┴─┐                  ┌─┴─┐
         │ C │ ◄──── msg ────▶ │ D │
         └───┘                  └───┘
```

No central orchestrator. Agents communicate peer-to-peer. Decisions emerge from interaction. Harder to debug, but scales to many agents.

> 没有中央编排器。Agent 之间点对点通信。决策从交互中涌现。更难调试，但可以扩展到许多 Agent。

Use when: many homogeneous agents doing similar work (scraping, classification) at scale. Avoid when: you need a single coherent plan or strict ordering.

> 使用场景：许多同质 Agent 大规模做类似工作（抓取、分类）。避免：需要单一连贯计划或严格排序时。

### When NOT to Use Multi-Agent

Multi-agent adds complexity. Every message between agents is a potential failure point. Debugging goes from "read one conversation" to "trace messages across five agents."

> 多 Agent 增加了复杂性。Agent 之间的每条消息都是一个潜在的故障点。调试从"阅读一个对话"变成"追踪五个 Agent 之间的消息"。

**Stay single-agent when:**
- The task fits in one context window (under ~100k tokens of working data)
  中文翻译：任务适合一个上下文窗口（工作数据不超过约 100k token）
- You do not need different system prompts for different stages
  中文翻译：不同阶段不需要不同的系统提示
- Sequential execution is fast enough
  中文翻译：顺序执行速度足够快
- The task is simple enough that splitting it adds more overhead than value
  中文翻译：任务足够简单，拆分增加的开销超过其价值

**The complexity cost:**
- Every agent boundary is a lossy compression step: agent A's full context gets summarized into a message for agent B
  中文翻译：每个 Agent 边界都是有损压缩步骤：Agent A 的完整上下文被总结为发给 Agent B 的消息
- Coordination logic (who does what, when, in what order) is its own source of bugs
  中文翻译：协调逻辑（谁做什么、何时做、按什么顺序）本身就是一个 bug 来源
- Latency increases: N agents means N serial LLM calls minimum, more if they need to talk back and forth
  中文翻译：延迟增加：N 个 Agent 意味着至少 N 次串行 LLM 调用，如果需要来回对话则更多
- Cost multiplies: each agent burns tokens independently
  中文翻译：成本倍增：每个 Agent 独立消耗 token

Rule of thumb: if a task takes fewer than 20 tool calls and fits in 100k tokens, keep it single-agent.

> 经验法则：如果一个任务只需要不到 20 次工具调用，并且适合 100k token，就保持单 Agent。

## Build It | 动手实现

### Step 1: The Overloaded Single Agent

Here is a single agent trying to do everything. It has one massive system prompt and one context window holding research, code, and reviews:

> 这是一个试图做所有事情的单 Agent。它有一个庞大的系统提示和一个容纳研究、代码和审阅的上下文窗口：

```typescript
type AgentResult = {
  content: string;
  tokensUsed: number;
  toolCalls: number;
};

async function singleAgentApproach(task: string): Promise<AgentResult> {
  const systemPrompt = `You are a full-stack developer. You must:
1. Research the requirements
2. Write the code
3. Review the code for bugs
4. Write tests
Do ALL of these in a single conversation.`;

  const contextWindow: string[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const research = await fakeLLMCall(systemPrompt, `Research: ${task}`);
  contextWindow.push(research.output);
  totalTokens += research.tokens;
  totalToolCalls += research.calls;

  const code = await fakeLLMCall(
    systemPrompt,
    `Given this research:\n${contextWindow.join("\n")}\n\nNow write code for: ${task}`
  );
  contextWindow.push(code.output);
  totalTokens += code.tokens;
  totalToolCalls += code.calls;

  const review = await fakeLLMCall(
    systemPrompt,
    `Given all previous context:\n${contextWindow.join("\n")}\n\nReview the code.`
  );
  contextWindow.push(review.output);
  totalTokens += review.tokens;
  totalToolCalls += review.calls;

  return {
    content: contextWindow.join("\n---\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

Problems with this approach:
- The context window grows with every stage. By the review step, it contains research notes AND code AND prior reasoning.
  中文翻译：上下文窗口随每个阶段增长。到审阅步骤时，它包含研究笔记和代码以及先前的推理。
- The system prompt is generic. It cannot be tuned for each stage.
  中文翻译：系统提示是通用的。无法为每个阶段调优。
- Nothing runs in parallel.
  中文翻译：没有并行执行。

The single-agent loop forces the LLM to context-switch between very different cognitive tasks (research vs coding vs review) on every turn. Each switch costs quality.

> 单 Agent 循环迫使 LLM 每轮在非常不同的认知任务（研究 vs 编码 vs 审阅）之间切换上下文。每次切换都损失质量。

### Step 2: Specialist Agents

Now split it. Each agent gets one job:

> 现在拆分它。每个 Agent 获得一个任务：

```typescript
type SpecialistAgent = {
  name: string;
  systemPrompt: string;
  run: (input: string) => Promise<AgentResult>;
};

function createSpecialist(name: string, systemPrompt: string): SpecialistAgent {
  return {
    name,
    systemPrompt,
    run: async (input: string) => {
      const result = await fakeLLMCall(systemPrompt, input);
      return {
        content: result.output,
        tokensUsed: result.tokens,
        toolCalls: result.calls,
      };
    },
  };
}

const researcher = createSpecialist(
  "researcher",
  "You are a technical researcher. Read documentation, find patterns, and summarize findings. Output only the facts needed for implementation."
);

const coder = createSpecialist(
  "coder",
  "You are a senior TypeScript developer. Given requirements and research notes, write clean, tested code. Nothing else."
);

const reviewer = createSpecialist(
  "reviewer",
  "You are a code reviewer. Find bugs, security issues, and logic errors. Be specific. Cite line numbers."
);
```

Each specialist has a focused prompt. Each gets a clean context window with only the input it needs.

> 每个专家都有一个聚焦的提示。每个都获得一个干净的上下文窗口，只包含所需的输入。

The researcher's prompt is optimized for reading and summarization. The coder's prompt is optimized for writing clean code. The reviewer's prompt is optimized for finding bugs. No single prompt tries to do all three.

> 研究员的提示针对阅读和总结优化。编码员的提示针对编写干净代码优化。审阅员的提示针对发现 bug 优化。没有单个提示试图同时做这三件事。

### Step 3: Coordinate Through Messages

Wire the specialists together with explicit message passing:

> 通过显式消息传递将专家连接起来：

```typescript
type AgentMessage = {
  from: string;
  to: string;
  content: string;
  timestamp: number;
};

async function multiAgentApproach(task: string): Promise<AgentResult> {
  const messages: AgentMessage[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const researchResult = await researcher.run(task);
  messages.push({
    from: "researcher",
    to: "coder",
    content: researchResult.content,
    timestamp: Date.now(),
  });
  totalTokens += researchResult.tokensUsed;
  totalToolCalls += researchResult.toolCalls;

  const coderInput = messages
    .filter((m) => m.to === "coder")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const codeResult = await coder.run(coderInput);
  messages.push({
    from: "coder",
    to: "reviewer",
    content: codeResult.content,
    timestamp: Date.now(),
  });
  totalTokens += codeResult.tokensUsed;
  totalToolCalls += codeResult.toolCalls;

  const reviewerInput = messages
    .filter((m) => m.to === "reviewer")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const reviewResult = await reviewer.run(reviewerInput);
  messages.push({
    from: "reviewer",
    to: "orchestrator",
    content: reviewResult.content,
    timestamp: Date.now(),
  });
  totalTokens += reviewResult.tokensUsed;
  totalToolCalls += reviewResult.toolCalls;

  return {
    content: messages.map((m) => `[${m.from} -> ${m.to}]: ${m.content}`).join("\n\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

Each agent receives only the messages addressed to it. No context pollution. The researcher's 50k tokens of documentation reading never enter the reviewer's context.

> 每个 Agent 只接收发给自己的消息。没有上下文污染。研究员读取的 50k token 文档永远不会进入审阅者的上下文。

This is the core win: information isolation. Each agent's context window is dedicated to its own task. The 200k-token budget of one agent is not wasted on other agents' scratch work.

> 这是核心优势：信息隔离。每个 Agent 的上下文窗口专注于自己的任务。一个 Agent 的 200k token 预算不会浪费在其他 Agent 的草稿工作上。

### Step 4: Compare

```typescript
async function compare() {
  const task = "Build a rate limiter middleware for an Express.js API";

  console.log("=== Single Agent ===");
  const single = await singleAgentApproach(task);
  console.log(`Tokens: ${single.tokensUsed}`);
  console.log(`Tool calls: ${single.toolCalls}`);

  console.log("\n=== Multi-Agent ===");
  const multi = await multiAgentApproach(task);
  console.log(`Tokens: ${multi.tokensUsed}`);
  console.log(`Tool calls: ${multi.toolCalls}`);
}
```

The multi-agent version uses more total tokens (three agents, three separate LLM calls) but each agent's context stays clean. The quality of each stage improves because the system prompt is specialized.

> 多 Agent 版本使用更多的总 token（三个 Agent，三次独立的 LLM 调用），但每个 Agent 的上下文保持干净。每个阶段的质量提高，因为系统提示是专业化的。

The trade is clear: spend more tokens, get better output. Worth it when the task is hard. Not worth it for "summarize this paragraph."

> 权衡很清晰：花更多 token，获得更好的输出。任务难时值得。对"总结这一段"不值得。

## Use It | 用框架实现

This lesson produces a reusable prompt for deciding when to go multi-agent. See `outputs/prompt-multi-agent-decision.md`.

> 本课产出一个可复用的提示，用于决定何时使用多 Agent。参见 `outputs/prompt-multi-agent-decision.md`。

The prompt asks four diagnostic questions: (1) does the task need more than 100k tokens of working context? (2) does it need different expertise at different stages? (3) is there parallel work? (4) is the complexity worth the overhead? If at least two are yes, multi-agent pays off.

> 该提示问四个诊断问题：(1) 任务是否需要超过 100k token 的工作上下文？(2) 不同阶段是否需要不同专业知识？(3) 是否有可并行的工作？(4) 复杂性是否值得开销？如果至少两个是，多 Agent 就划算。

## Exercises | 练习题

1. Add a fourth specialist: a "tester" agent that receives code from the coder and review feedback from the reviewer, then writes tests
   中文翻译：添加第四个专家：一个"测试员"Agent，接收编码器的代码和审阅者的反馈，然后编写测试
2. Modify the pipeline so the reviewer can send feedback back to the coder for a revision loop (max 2 rounds)
   中文翻译：修改流水线，使审阅者可以将反馈发送回编码器进行修订循环（最多 2 轮）
3. Convert the sequential pipeline into a fan-out: run the researcher and a "requirements analyzer" agent in parallel, then merge their outputs before passing to the coder
   中文翻译：将顺序流水线转换为扇出：并行运行研究员和"需求分析师"Agent，然后合并它们的输出再传递给编码器

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Swarm / 群体 | "A hive mind of AI agents" / "AI Agent 的蜂巢思维" | A set of peer agents with shared state and no fixed leader. Behavior emerges from local interactions. / 一组具有共享状态且无固定领导者的对等 Agent。行为从局部交互中涌现。 |
| Orchestrator / 编排器 | "The boss agent" / "老板 Agent" | An agent whose tools include spawning and managing other agents. It plans and delegates but may not do the actual work. / 一个工具包括生成和管理其他 Agent 的 Agent。它规划和委派，但可能不做实际工作。 |
| Coordinator / 协调器 | "The traffic cop" / "交通警察" | A non-agent component (often just code, not an LLM) that routes messages between agents based on rules. / 一个非 Agent 组件（通常只是代码，不是 LLM），根据规则在 Agent 之间路由消息。 |
| Consensus / 共识 | "The agents agree" / "Agent 们达成一致" | A protocol where multiple agents must reach agreement before proceeding. Used when conflicting outputs need resolution. / 多个 Agent 在继续之前必须达成一致的协议。用于需要解决冲突输出的情况。 |
| Emergent behavior / 涌现行为 | "The agents figured it out themselves" / "Agent 自己想出来的" | System-level patterns that arise from agent interactions but were not explicitly programmed. Can be useful or harmful. / 从 Agent 交互中产生但未被明确编程的系统级模式。可能有用也可能有害。 |
| Fan-out / fan-in / 扇出/扇入 | "Map-reduce for agents" / "Agent 的 Map-reduce" | Splitting a task across parallel agents (fan-out), then combining their results (fan-in). / 将任务分配给并行 Agent（扇出），然后合并它们的结果（扇入）。 |
| Message passing / 消息传递 | "Agents talk to each other" / "Agent 之间互相交谈" | The communication mechanism between agents: structured data sent from one agent to another, replacing shared context windows. / Agent 之间的通信机制：从一个 Agent 发送到另一个 Agent 的结构化数据，替代共享上下文窗口。 |

## Further Reading | 延伸阅读

- [The Landscape of Emerging AI Agent Architectures](https://arxiv.org/abs/2409.02977) - survey of multi-agent patterns
  中文翻译：新兴 AI Agent 架构概览 — 多 Agent 模式综述
- [AutoGen: Enabling Next-Gen LLM Applications](https://arxiv.org/abs/2308.08155) - Microsoft's multi-agent conversation framework
  中文翻译：AutoGen：赋能下一代 LLM 应用 — 微软的多 Agent 对话框架
- [Claude Code subagents documentation](https://docs.anthropic.com/en/docs/claude-code) - how Claude Code delegates with Task
  中文翻译：Claude Code 子 Agent 文档 — Claude Code 如何使用 Task 委派
- [CrewAI documentation](https://docs.crewai.com/) - role-based multi-agent framework
  中文翻译：CrewAI 文档 — 基于角色的多 Agent 框架
