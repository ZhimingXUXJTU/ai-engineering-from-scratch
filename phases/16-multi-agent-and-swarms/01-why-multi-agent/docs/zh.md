# 为什么需要多 Agent？ | 多 Agent 为什么

> 单 Agent 会碰壁。聪明的做法不是更大的 Agent —— 而是更多的 Agent。

> **【中文解读】** 本节介绍了为什么需要多 Agent 系统——单 Agent 的上下文溢出、角色混乱和串行瓶颈问题，以及多 Agent 如何通过分工协作来解决这些问题。

> **【拓展：why multi agent→具体应用】** 单 Agent 在处理复杂任务时面临三个瓶颈：(1) 上下文溢出——所有信息塞进一个窗口，重要的被淹没；(2) 角色混乱——一个 Agent 扮演多个角色导致提示词冲突；(3) 串行执行——工具调用只能排队。多 Agent 通过分工协作解决这些问题。Anthropic 的研究表明，多 Agent 系统在 BrowseComp 基准上比单 Agent 提升 90.2%，80% 的方差仅由 token 使用量解释。


**类型：** 学习
**语言：** TypeScript
**前置条件：** 第 14 阶段（Agent 工程）
**时间：** ~60 分钟

## 学习目标

- 识别单 Agent 天花板（上下文溢出、角色混杂、串行瓶颈），并解释何时拆分为多个 Agent 是正确的选择
- 比较编排模式（流水线、并行扇出、监督者、层次化），并为给定任务结构选择合适的模式
- 设计一个具有清晰角色边界、共享状态和通信契约的多 Agent 系统
- 分析多 Agent 复杂性（延迟、成本、调试难度）与单 Agent 简洁性之间的权衡

## 问题引入

你在第 14 阶段构建了一个单 Agent。它能工作。它可以读取文件、运行命令、调用 API 并对结果进行推理。然后你将它指向一个真实的代码库：200 个文件、三种编程语言、依赖基础设施的测试，以及在写代码之前需要研究外部 API 的需求。

Agent 崩溃了。不是因为 LLM 愚蠢，而是因为任务超出了一个 Agent 循环能处理的范围。上下文窗口被文件内容填满。Agent 忘记了 40 次工具调用之前读取了什么。它试图同时充当研究员、程序员和审查者，三个角色都做得不好。

这就是单 Agent 天花板。每当任务需要以下条件时你都会碰到它：

- **超出一个窗口的上下文量** - 读取 50 个文件会超过 20 万 token
- **不同阶段需要不同专长** - 研究需要与代码生成不同的提示
- **可以并行执行的工作** - 为什么要顺序读取三个文件，明明可以同时读取？

## 核心概念

### 单 Agent 天花板

单 Agent 是一个循环、一个上下文窗口、一个系统提示词。想象一下：

```
┌─────────────────────────────────────────┐
│            单 Agent                      │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │         上下文窗口                 │  │
│  │                                   │  │
│  │  研究笔记                         │  │
│  │  + 代码文件                       │  │
│  │  + 测试输出                       │  │
│  │  + 审查反馈                       │  │
│  │  + API 文档                       │  │
│  │  + ...                            │  │
│  │                                   │  │
│  │  ██████████████████████ 已满 ███  │  │
│  └───────────────────────────────────┘  │
│                                         │
│  一个系统提示词试图覆盖                   │
│  研究 + 编码 + 审查 + 测试               │
│                                         │
│  结果：每件事都平庸                       │
└─────────────────────────────────────────┘
```

三件事会出问题：

1. **上下文饱和** - 工具结果不断堆积。到第 30 轮时，Agent 已经消耗了 15 万 token 的文件内容、命令输出和先前的推理。第 5 轮的关键细节被遗忘了。

2. **角色混乱** - 一个说"你是研究员、程序员、审查员和测试员"的系统提示词，会产生一个半研究、半编码、从不完成审查的 Agent。

3. **串行瓶颈** - Agent 读取文件 A，然后文件 B，然后文件 C。三次串行 LLM 调用。三次串行工具执行。没有并行性。

### 多 Agent 解决方案

拆分工作。给每个 Agent 一个任务、一个上下文窗口和一个为该任务调优的系统提示词：

```
┌──────────────────────────────────────────────────────────┐
│                    编排器                                  │
│                                                          │
│  "构建一个用户管理的 REST API"                              │
│                                                          │
│         ┌──────────┬──────────┬──────────┐               │
│         │          │          │          │               │
│         ▼          ▼          ▼          ▼               │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│   │ 研究员   │ │  编码者  │ │  审查员  │ │  测试员  │  │
│   │          │ │          │ │          │ │          │  │
│   │ 读取     │ │ 编写     │ │ 检查     │ │ 运行     │  │
│   │ 文档，   │ │ 代码     │ │ 代码     │ │ 测试，   │  │
│   │ 发现     │ │ 基于研究 │ │ 质量，   │ │ 报告     │  │
│   │ 模式     │ │ + 规格   │ │ 发现     │ │ 结果     │  │
│   │          │ │          │ │ 缺陷     │ │          │  │
│   └─────┬────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│         │           │            │             │         │
│         └───────────┴────────────┴─────────────┘         │
│                          │                               │
│                     合并结果                               │
└──────────────────────────────────────────────────────────┘
```

每个 Agent 拥有：
- 一个聚焦的系统提示词（"你是代码审查员。你唯一的任务是发现缺陷。"）
- 自己的上下文窗口（不被其他 Agent 的工作污染）
- 清晰的输入/输出契约（接收研究笔记，输出代码）

### 实际使用此模式的系统

**Claude Code 子 Agent** - 当 Claude Code 使用 `Task` 生成子 Agent 时，它创建一个带有范围任务的子 Agent。父 Agent 保持上下文干净。子 Agent 做专注的工作并返回摘要。

**Devin** - 运行规划 Agent、编码 Agent 和浏览器 Agent。规划者将工作分解为步骤。编码者编写代码。浏览器研究文档。每个都有独立的上下文。

**多 Agent 编码团队（SWE-bench）** - SWE-bench 上表现最好的系统使用读取代码库的研究员、设计修复方案的规划者和实现方案的编码者。单 Agent 系统得分较低。

**ChatGPT 深度研究** - 并行生成多个搜索 Agent，每个探索不同角度，然后综合结果。

### 多 Agent 光谱

多 Agent 不是二元的。它是一个光谱：

```
简单 ──────────────────────────────────────────── 复杂

 单 Agent      子 Agent       流水线       团队        群体

 ┌───┐       ┌───┐        ┌───┐───┐    ┌───┐───┐    ┌─┐┌─┐┌─┐
 │ A │       │ A │        │ A │ B │    │ A │ B │    │ ││ ││ │
 └───┘       └─┬─┘        └───┘─┬─┘    └─┬─┘─┬─┘    └┬┘└┬┘└┬┘
               │                │        │   │       ┌┴──┴──┴┐
             ┌─┴─┐          ┌───┘───┐    │   │       │共享    │
             │ a │          │ C │ D │  ┌─┴───┴─┐    │ 状态   │
             └───┘          └───┘───┘  │ 消息    │    └───────┘
                                       │ 总线   │
 1 个循环      父 + 子       阶段到     │        │    N 个对等
 1 个上下文    任务           阶段       └────────┘    涌现行为
                                       显式角色

```

**单 Agent** - 一个循环，一个提示词。适合简单任务。

**子 Agent** - 父 Agent 为聚焦的子任务生成子 Agent。父 Agent 维护计划。子 Agent 汇报结果。这就是 Claude Code 做的事。

**流水线** - Agent 按顺序运行。Agent A 的输出成为 Agent B 的输入。适合分阶段工作流：研究 -> 编码 -> 审查 -> 测试。

**团队** - Agent 通过共享消息总线并行运行。每个都有角色。编排器协调。适合同时需要不同技能的场景。

**群体** - 许多相同或接近相同的 Agent 具有共享状态。没有固定的编排器。Agent 从队列中获取工作。适合高吞吐量并行任务。

### 四种多 Agent 模式

#### 模式 1：流水线

```
输入 ──▶ Agent A ──▶ Agent B ──▶ Agent C ──▶ 输出
         （研究）    （编码）     （审查）
```

每个 Agent 转换数据并向前传递。推理简单。一个阶段的失败会阻塞其余阶段。

#### 模式 2：扇出 / 扇入

```
               ┌──▶ Agent A ──┐
               │              │
输入 ──▶ 拆分 ├──▶ Agent B ──├──▶ 合并 ──▶ 输出
               │              │
               └──▶ Agent C ──┘
```

跨并行 Agent 拆分工作，然后合并结果。适合可分解为独立子任务的任务。

#### 模式 3：编排器-工作器

```
                   ┌──────────┐
                   │  编排器   │
                   └──┬───┬───┘
                 任务 │   │ 任务
                ┌─────┘   └─────┐
                ▼               ▼
          ┌──────────┐   ┌──────────┐
          │ 工作器 A │   │ 工作器 B │
          └──────────┘   └──────────┘
```

智能编排器决定做什么、委派给工作器并综合结果。编排器本身也是一个 Agent，拥有生成工作器的工具。

#### 模式 4：对等群体

```
         ┌───┐ ◄──── 消息 ────▶ ┌───┐
         │ A │                   │ B │
         └─┬─┘                   └─┬─┘
           │                       │
      消息  │    ┌───────────┐      │ 消息
           └───▶│  共享       │◄────┘
                │  状态       │
           ┌───▶│  / 队列    │◄────┐
           │    └───────────┘     │
      消息  │                       │ 消息
         ┌─┴─┐                   ┌─┴─┐
         │ C │ ◄──── 消息 ────▶ │ D │
         └───┘                   └───┘
```

没有中央编排器。Agent 以点对点方式通信。决策从交互中涌现。更难调试，但可以扩展到许多 Agent。

### 何时不应该使用多 Agent

多 Agent 增加了复杂性。Agent 之间的每条消息都是潜在的故障点。调试从"读取一个对话"变成了"追踪五个 Agent 之间的消息"。

**保持单 Agent 的情况：**
- 任务适合一个上下文窗口（不超过约 10 万 token 的工作数据）
- 不同阶段不需要不同的系统提示词
- 顺序执行速度足够
- 任务足够简单，拆分带来的开销大于价值

**复杂性成本：**
- 每个 Agent 边界都是一个有损压缩步骤：Agent A 的完整上下文被摘要为给 Agent B 的消息
- 协调逻辑（谁做什么、何时做、以什么顺序）本身就是一个错误来源
- 延迟增加：N 个 Agent 意味着至少 N 次串行 LLM 调用，如果它们需要来回通信则更多
- 成本倍增：每个 Agent 独立消耗 token

经验法则：如果一个任务少于 20 次工具调用且适合 10 万 token，保持单 Agent。

## 动手实现

### 第 1 步：过载的单 Agent

下面是一个试图做一切的单 Agent。它有一个巨大的系统提示词和一个容纳研究、代码和审查的上下文窗口：

```typescript
type AgentResult = {
  content: string;
  tokensUsed: number;
  toolCalls: number;
};

async function singleAgentApproach(task: string): Promise<AgentResult> {
  const systemPrompt = `你是一个全栈开发者。你必须：
1. 研究需求
2. 编写代码
3. 审查代码中的缺陷
4. 编写测试
在单个对话中完成所有这些。`;

  const contextWindow: string[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const research = await fakeLLMCall(systemPrompt, `研究：${task}`);
  contextWindow.push(research.output);
  totalTokens += research.tokens;
  totalToolCalls += research.calls;

  const code = await fakeLLMCall(
    systemPrompt,
    `给定以下研究：\n${contextWindow.join("\n")}\n\n现在为以下任务编写代码：${task}`
  );
  contextWindow.push(code.output);
  totalTokens += code.tokens;
  totalToolCalls += code.calls;

  const review = await fakeLLMCall(
    systemPrompt,
    `给定所有先前的上下文：\n${contextWindow.join("\n")}\n\n审查代码。`
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

这种方法的问题：
- 上下文窗口随着每个阶段增长。到审查步骤时，它包含研究笔记和代码和先前的推理。
- 系统提示词是通用的。无法为每个阶段调优。
- 没有并行执行。

### 第 2 步：专业化 Agent

现在拆分它。每个 Agent 获得一个任务：

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
  "你是一个技术研究员。阅读文档，发现模式，并总结发现。只输出实现所需的事实。"
);

const coder = createSpecialist(
  "coder",
  "你是一个资深 TypeScript 开发者。给定需求和研究成果，编写干净、经过测试的代码。不做其他事情。"
);

const reviewer = createSpecialist(
  "reviewer",
  "你是一个代码审查员。发现缺陷、安全问题和逻辑错误。要具体。引用行号。"
);
```

每个专家都有一个聚焦的提示词。每个都有干净的上下文窗口，只包含所需的输入。

### 第 3 步：通过消息协调

用显式消息传递将专家连接起来：

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
    .map((m) => `[来自 ${m.from}]：${m.content}`)
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
    .map((m) => `[来自 ${m.from}]：${m.content}`)
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
    content: messages.map((m) => `[${m.from} -> ${m.to}]：${m.content}`).join("\n\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

每个 Agent 只接收发给它的消息。没有上下文污染。研究员的 5 万 token 文档阅读永远不会进入审查员的上下文。

### 第 4 步：比较

```typescript
async function compare() {
  const task = "为 Express.js API 构建速率限制中间件";

  console.log("=== 单 Agent ===");
  const single = await singleAgentApproach(task);
  console.log(`Token 数：${single.tokensUsed}`);
  console.log(`工具调用：${single.toolCalls}`);

  console.log("\n=== 多 Agent ===");
  const multi = await multiAgentApproach(task);
  console.log(`Token 数：${multi.tokensUsed}`);
  console.log(`工具调用：${multi.toolCalls}`);
}
```

多 Agent 版本使用更多总 token（三个 Agent，三次独立的 LLM 调用），但每个 Agent 的上下文保持干净。每个阶段的质量提高，因为系统提示词是专业化的。

## 用框架实现

本课产出一个可复用的提示词，用于决定何时使用多 Agent。参见 `outputs/prompt-multi-agent-decision.md`。

## 练习题

1. 添加第四个专家：一个"测试员"Agent，接收编码者的代码和审查员的审查反馈，然后编写测试
2. 修改流水线，使审查员可以将反馈发送回编码者进行修订循环（最多 2 轮）
3. 将串行流水线转换为扇出模式：并行运行研究员和"需求分析师"Agent，然后在传递给编码者之前合并它们的输出

## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 群体 (Swarm) | "AI Agent 的蜂巢思维" | 一组具有共享状态且无固定领导者的对等 Agent。行为从局部交互中涌现。 |
| 编排器 (Orchestrator) | "老板 Agent" | 一个工具包括生成和管理其他 Agent 的 Agent。它规划和委派，但可能不做实际工作。 |
| 协调器 (Coordinator) | "交通警察" | 一个非 Agent 组件（通常只是代码，不是 LLM），根据规则在 Agent 之间路由消息。 |
| 共识 (Consensus) | "Agent 们达成一致" | 一种多个 Agent 在继续之前必须达成一致的协议。用于解决冲突的输出。 |
| 涌现行为 (Emergent behavior) | "Agent 们自己想出来的" | 从 Agent 交互中产生的系统级模式，但并非显式编程的。可能有用也可能有害。 |
| 扇出/扇入 (Fan-out / fan-in) | "Agent 的 Map-Reduce" | 将任务分配给并行 Agent（扇出），然后合并它们的结果（扇入）。 |
| 消息传递 (Message passing) | "Agent 们互相交谈" | Agent 之间的通信机制：从一个 Agent 发送到另一个 Agent 的结构化数据，替代共享上下文窗口。 |

## 延伸阅读

- [新兴 AI Agent 架构全景](https://arxiv.org/abs/2409.02977) - 多 Agent 模式综述
- [AutoGen：实现下一代 LLM 应用](https://arxiv.org/abs/2308.08155) - 微软的多 Agent 对话框架
- [Claude Code 子 Agent 文档](https://docs.anthropic.com/en/docs/claude-code) - Claude Code 如何通过 Task 委派
- [CrewAI 文档](https://docs.crewai.com/) - 基于角色的多 Agent 框架
