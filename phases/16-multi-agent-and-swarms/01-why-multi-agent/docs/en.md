# Why Multi-Agent? | 为什么需要多 Agent

> One agent hits a wall. The smart move is not a bigger agent - it is more agents.

> **【中文解读】** 本节介绍了为什么需要多 Agent 系统——单 Agent 的上下文溢出、角色混乱和串行瓶颈问题，以及多 Agent 如何通过分工协作来解决这些问题。


**Type:** Learn
**Languages:** TypeScript
**Prerequisites:** Phase 14 (Agent Engineering)
**Time:** ~60 minutes

## Learning Objectives | 学习目标

- Identify the single-agent ceiling (context overflow, mixed expertise, sequential bottleneck) and explain when splitting into multiple agents is the right move
- Compare orchestration patterns (pipeline, parallel fan-out, supervisor, hierarchical) and select the right one for a given task structure
- Design a multi-agent system with clear role boundaries, shared state, and a communication contract
- Analyze the tradeoffs of multi-agent complexity (latency, cost, debugging difficulty) versus single-agent simplicity

> **【中文解读】** 学习目标：1) 识别单 Agent 天花板（上下文溢出、角色混乱、串行瓶颈）并解释何时应该拆分为多 Agent；2) 对比编排模式（流水线、并行扇出、监督者、层级）并为给定任务选择合适的模式；3) 设计具有清晰角色边界、共享状态和通信契约的多 Agent 系统；4) 分析多 Agent 复杂性与单 Agent 简洁性之间的权衡。

## The Problem | 问题

You built a single agent in Phase 14. It works. It can read files, run commands, call APIs, and reason about results. Then you point it at a real codebase: 200 files, three languages, tests that depend on infrastructure, and a requirement to research external APIs before writing code.

The agent chokes. Not because the LLM is dumb, but because the task exceeds what one agent loop can handle. The context window fills up with file contents. The agent forgets what it read 40 tool calls ago. It tries to be a researcher, a coder, and a reviewer all at once, and does all three poorly.

This is the single-agent ceiling. You hit it every time a task requires:

- **More context than fits in one window** - reading 50 files blows past 200k tokens
- **Different expertise at different stages** - research requires different prompting than code generation
- **Work that can happen in parallel** - why read three files sequentially when you can read them simultaneously?

> **【中文解读】** 单 Agent 天花板：当你将 Agent 指向真实代码库时——200 个文件、三种语言、依赖基础设施的测试——它会在三个维度上崩溃：1) **上下文饱和**——工具调用结果堆积，关键细节丢失；2) **角色混乱**——一个系统提示试图覆盖研究+编码+审查+测试；3) **串行瓶颈**——三个文件串行读取而非并行。

## The Concept | 概念

### The Single-Agent Ceiling

A single agent is one loop, one context window, one system prompt. Picture it:

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

Three things break:

1. **Context saturation** - tool results pile up. By turn 30, the agent has consumed 150k tokens of file contents, command outputs, and prior reasoning. Critical details from turn 5 get lost.

2. **Role confusion** - a system prompt that says "you are a researcher, coder, reviewer, and tester" produces an agent that half-researches, half-codes, and never finishes reviewing.

3. **Sequential bottleneck** - the agent reads file A, then file B, then file C. Three serial LLM calls. Three serial tool executions. No parallelism.

### The Multi-Agent Solution

Split the work. Give each agent one job, one context window, and one system prompt tuned for that job:

> **【中文解读】** 多 Agent 解决方案的核心原则：分工。每个 Agent 拥有：一个聚焦的系统提示（"你是代码审查员，唯一职责是发现 Bug"）、独立的上下文窗口（不被其他 Agent 的工作污染）、清晰的输入/输出契约。这样每个 Agent 都能在自己的专业领域发挥最大效能。

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
- Its own context window (not polluted by other agents' work)
- A clear input/output contract (receives research notes, outputs code)

### Real Systems That Do This

**Claude Code subagents** - when Claude Code spawns a subagent with `Task`, it creates a child agent with a scoped task. The parent keeps its context clean. The child does focused work and returns a summary.

**Devin** - runs a planner agent, a coder agent, and a browser agent. The planner breaks work into steps. The coder writes code. The browser researches documentation. Each has separate context.

**Multi-agent coding teams (SWE-bench)** - top-performing systems on SWE-bench use a researcher that reads the codebase, a planner that designs the fix, and a coder that implements it. Single-agent systems score lower.

**ChatGPT Deep Research** - spawns multiple search agents in parallel, each exploring a different angle, then synthesizes results.

> **【拓展：多 Agent 实际系统】** Claude Code 通过 Task 工具生成子 Agent，保持父 Agent 上下文清洁；Devin 运行规划 Agent、编码 Agent 和浏览器 Agent；SWE-bench 排名靠前的系统使用研究员+规划师+编码员的组合；ChatGPT Deep Research 并行生成多个搜索 Agent 再综合结果。这些真实系统的共同点是：每个 Agent 有独立的上下文和聚焦的职责。

### The Spectrum

Multi-agent is not binary. It is a spectrum:

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

**Subagents** - a parent spawns children for focused subtasks. The parent maintains the plan. Children report back. This is what Claude Code does.

**Pipeline** - agents run in sequence. Agent A's output becomes Agent B's input. Good for staged workflows: research -> code -> review -> test.

**Team** - agents run in parallel with a shared message bus. Each has a role. An orchestrator coordinates. Good when different skills are needed simultaneously.

**Swarm** - many identical or near-identical agents with shared state. No fixed orchestrator. Agents pick up work from a queue. Good for high-throughput parallel tasks.

### The Four Multi-Agent Patterns

#### Pattern 1: Pipeline

```
Input ──▶ Agent A ──▶ Agent B ──▶ Agent C ──▶ Output
          (research)  (code)      (review)
```

Each agent transforms the data and passes it forward. Simple to reason about. Failure in one stage blocks the rest.

#### Pattern 2: Fan-out / Fan-in

```
                ┌──▶ Agent A ──┐
                │              │
Input ──▶ Split ├──▶ Agent B ──├──▶ Merge ──▶ Output
                │              │
                └──▶ Agent C ──┘
```

Split work across parallel agents, then merge results. Good for tasks that decompose into independent subtasks.

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

### When NOT to Use Multi-Agent

Multi-agent adds complexity. Every message between agents is a potential failure point. Debugging goes from "read one conversation" to "trace messages across five agents."

**Stay single-agent when:**
- The task fits in one context window (under ~100k tokens of working data)
- You do not need different system prompts for different stages
- Sequential execution is fast enough
- The task is simple enough that splitting it adds more overhead than value

**The complexity cost:**
- Every agent boundary is a lossy compression step: agent A's full context gets summarized into a message for agent B
- Coordination logic (who does what, when, in what order) is its own source of bugs
- Latency increases: N agents means N serial LLM calls minimum, more if they need to talk back and forth
- Cost multiplies: each agent burns tokens independently

Rule of thumb: if a task takes fewer than 20 tool calls and fits in 100k tokens, keep it single-agent.

> **【中文解读】** 何时不要用多 Agent：多 Agent 增加复杂性——每个 Agent 边界都是有损压缩步骤，协调逻辑本身是 Bug 来源，延迟和成本成倍增加。经验法则：如果任务少于 20 次工具调用且数据量在 100k token 以内，保持单 Agent。

> **【拓展：单 Agent vs 多 Agent 决策】** 决策依据：任务是否超出单上下文窗口？不同阶段是否需要不同的系统提示？是否存在可并行的独立子任务？如果三个问题都是"否"，保持单 Agent 更好。

## Build It | 动手构建

### Step 1: The Overloaded Single Agent

Here is a single agent trying to do everything. It has one massive system prompt and one context window holding research, code, and reviews:

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
- The system prompt is generic. It cannot be tuned for each stage.
- Nothing runs in parallel.

### Step 2: Specialist Agents

Now split it. Each agent gets one job:

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

### Step 3: Coordinate Through Messages

Wire the specialists together with explicit message passing:

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

> **【中文解读】** 构建要点：单 Agent 方案的问题是上下文窗口随阶段增长，系统提示泛化无法针对每个阶段优化，且无法并行执行。多 Agent 方案中每个专家 Agent 有聚焦的系统提示、独立的上下文窗口，Agent 间通过显式消息传递协调，每个 Agent 只接收发送给自己的消息，避免了上下文污染。

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

## Use It | 使用方法

This lesson produces a reusable prompt for deciding when to go multi-agent. See `outputs/prompt-multi-agent-decision.md`.

## Exercises | 练习题

1. Add a fourth specialist: a "tester" agent that receives code from the coder and review feedback from the reviewer, then writes tests
2. Modify the pipeline so the reviewer can send feedback back to the coder for a revision loop (max 2 rounds)
3. Convert the sequential pipeline into a fan-out: run the researcher and a "requirements analyzer" agent in parallel, then merge their outputs before passing to the coder

## Key Terms | 关键术语

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Swarm | "A hive mind of AI agents" | A set of peer agents with shared state and no fixed leader. Behavior emerges from local interactions. | 群体：共享状态的对等 Agent 集合，无固定领导者，行为从局部交互中涌现 |
| Orchestrator | "The boss agent" | An agent whose tools include spawning and managing other agents. It plans and delegates but may not do the actual work. | 编排者：工具包括生成和管理其他 Agent 的 Agent，负责规划和委派 |
| Coordinator | "The traffic cop" | A non-agent component (often just code, not an LLM) that routes messages between agents based on rules. | 协调器：非 Agent 组件（通常只是代码），按规则路由 Agent 间的消息 |
| Consensus | "The agents agree" | A protocol where multiple agents must reach agreement before proceeding. Used when conflicting outputs need resolution. | 共识：多个 Agent 必须达成一致才能继续的协议 |
| Emergent behavior | "The agents figured it out themselves" | System-level patterns that arise from agent interactions but were not explicitly programmed. Can be useful or harmful. | 涌现行为：从 Agent 交互中产生的系统级模式，未被显式编程 |
| Fan-out / fan-in | "Map-reduce for agents" | Splitting a task across parallel agents (fan-out), then combining their results (fan-in). | 扇出/扇入：将任务分发到并行 Agent，再合并结果 |
| Message passing | "Agents talk to each other" | The communication mechanism between agents: structured data sent from one agent to another, replacing shared context windows. | 消息传递：Agent 间的通信机制，用结构化数据替代共享上下文窗口 |

## Further Reading | 延伸阅读

- [The Landscape of Emerging AI Agent Architectures](https://arxiv.org/abs/2409.02977) - survey of multi-agent patterns
- [AutoGen: Enabling Next-Gen LLM Applications](https://arxiv.org/abs/2308.08155) - Microsoft's multi-agent conversation framework
- [Claude Code subagents documentation](https://docs.anthropic.com/en/docs/claude-code) - how Claude Code delegates with Task
- [CrewAI documentation](https://docs.crewai.com/) - role-based multi-agent framework
