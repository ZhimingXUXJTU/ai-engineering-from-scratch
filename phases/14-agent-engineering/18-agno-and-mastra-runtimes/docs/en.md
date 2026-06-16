# Agno and Mastra: Production Runtimes | 生产 运行时 Mastra Agno

> Agno (Python) and Mastra (TypeScript) are the 2026 production-runtime pairing. Agno aims at microsecond agent instantiation and stateless FastAPI backends. Mastra ships agents, tools, workflows, unified model routing, and composite storage on the Vercel AI SDK substrate.

**Type:** Learn | **类型:** 学习
**Languages:** Python, TypeScript | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 13 (LangGraph) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

## Learning Objectives | 学习目标

- Identify Agno's performance targets and when they matter.
- Name Mastra's three primitives — Agents, Tools, Workflows — and the supported server adapters.
- Explain why a stateless session-scoped FastAPI backend is the recommended Agno production path.
- Pick Agno vs Mastra for a given stack (Python-first vs TypeScript-first).

## The Problem | 问题引入

LangGraph, AutoGen, CrewAI are framework-heavy. Teams that want "just the agent loop, fast, in my runtime" reach for Agno (Python) or Mastra (TypeScript). Both trade some of the framework-owned primitives for raw speed and a tighter fit to the surrounding stack.

> LangGraph、AutoGen、CrewAI 都是偏重框架的。想要"只要 Agent 循环，快速，在我的运行时中"的团队会选择 Agno（Python）或 Mastra（TypeScript）。两者都放弃了一些框架自带的原语，换取了原始速度和与周围技术栈更紧密的适配。


> **【中文解读】** Agno 和 Mastra 代表了 2026 年的两种 Agent 运行时设计哲学。Agno（原 PhiData）追求极简——用最少的代码构建 Agent。Mastra（TypeScript）追求全功能——提供完整的 Agent 生命周期管理。选择取决于团队的技术栈和复杂度需求。

> **{【拓展：Agno (GitHub 15k+ stars) 和 Mastra 是 2026 年 Agent 运...】}** Agno (GitHub 15k+ stars) 和 Mastra 是 2026 年 Agent 运行时的新秀。Agno 的哲学是'Agent 即函数'——每个 Agent 是一个带有工具集的异步函数。Mastra 基于 TypeScript，面向全栈开发者，提供完整的 Agent 生命周期管理（部署、监控、扩展）。两者都支持多模型后端和 MCP 集成。

> 🔗 **【前置】** 必须先掌握：Phase 14·01（Agent Loop）和 Phase 14·13（LangGraph）——本节是这两者的"轻量替代品"。如果你不知道为什么要"轻量化"LangGraph，说明你还没在生产中遇到 LangGraph 的工程负担，建议先用 LangGraph 几周再回头看本节。

## The Concept | 核心概念

### Agno

- Python runtime, formerly Phi-data.
- "No graphs, chains, or convoluted patterns — just pure python."
- Performance targets from their docs: ~2μs agent instantiation, ~3.75 KiB memory per agent, ~23 model providers.
- Production path: stateless session-scoped FastAPI backend. Each request starts a fresh agent; session state lives in a DB.
- Native multimodal (text, image, audio, video, file) and agentic RAG.

The speed targets matter when you have thousands of short-lived agents per second (chat fan-in, evaluation pipelines). They matter less when one agent runs for 10 minutes.

> 💡 **【类比】** Agno 像摩托车、LangGraph 像 SUV：摩托车启动快、轻便、能钻小巷（2μs 实例化、3.75 KiB 内存），适合短途高频通勤（每秒数千个短任务）；SUV 装得多、能跑长途、有空调导航（持久化、人在回路、复杂图），但启动慢、占地大。**关键洞察**：选 Agno 不是因为它"更好"，而是因为你的场景是"高频短任务"——LangGraph 在这里浪费资源。

> 速度目标在你每秒有数千个短暂 Agent（聊天聚合、评估管道）时很重要。当一个 Agent 运行 10 分钟时，它们就不那么重要了。

> Agno 和 Mastra 是两种轻量级 Agent 运行时。Agno 专注快速构建，Mastra 专注 TypeScript 生产部署。两者都提供最小化的 Agent 抽象。

### Mastra

- TypeScript, built on Vercel AI SDK.
- Three primitives: **Agents**, **Tools** (Zod-typed), **Workflows**.
- Unified Model Router — 3,300+ models across 94 providers (March 2026).
- Composite storage: memory, workflows, observability to different backends; ClickHouse recommended for observability at scale.
- Apache 2.0 with `ee/` directories under source-available enterprise license.
- Server adapters for Express, Hono, Fastify, Koa; first-class Next.js and Astro integration.
- Ships Mastra Studio (localhost:4111) for debugging.
- 22k+ GitHub stars, 300k+ weekly npm downloads at 1.0 (Jan 2026).

### Positioning

Neither is trying to be LangGraph. They compete on:

> 两者都不是在试图成为 LangGraph。它们的竞争点是：

> Agno 和 Mastra 是两种轻量级 Agent 运行时。Agno 专注快速构建，Mastra 专注 TypeScript 生产部署。两者都提供最小化的 Agent 抽象。

- **Language fit.** Agno for Python-first teams; Mastra for TypeScript-first.
- **Runtime ergonomics.** Agno = near-zero overhead; Mastra = integrated with the Vercel ecosystem.
- **Observability.** Both integrate with Langfuse/Phoenix/Opik (Lesson 24) but Mastra Studio is first-party.

### When to pick each

- **Agno** — Python backend, many short-lived agents, strong perf requirements, FastAPI shop.
- **Mastra** — TypeScript backend, Next.js / Vercel deploy, unified multi-provider model routing, Zod-typed tools.
- **LangGraph** (Lesson 13) — when durable state and explicit graph reasoning matter more than raw speed.
- **OpenAI / Claude Agent SDK** — when you want the provider's productized shape (Lessons 16–17).

### Where this pattern goes wrong

> ⚠️ **【易错点】** 看到 Agno "2μs 实例化"就无脑选 Agno。**后果**：如果你的场景是"一次请求跑一个 10 分钟的 Agent"，2μs 实例化对总耗时的影响是 0.0000003%——选错了框架还失去了 LangGraph 的持久化能力。**一行修复**：先测量你工作负载的"Agent 实例化次数 × 单次实例化开销 vs 总耗时"，占比 > 30% 才值得为性能选 Agno，否则继续用 LangGraph。

- **Perf-for-perf's-sake.** Picking Agno because "2μs" sounds good when the workload is one slow agent call per request. Overhead is not the bottleneck.
- **Ecosystem lock-in.** Mastra's Vercel-flavored integration is a plus on Vercel, a minus elsewhere.
- **Enterprise license confusion.** Mastra's `ee/` directories are source-available, not Apache 2.0. Read the licenses if you're planning to fork.

> 🤔 **【困惑】** Q: 我团队是 Python 后端，又想要 Mastra 的"多模型路由"功能，能用 Agno 实现吗？ A: 能，但要自己写。Agno 也有 ~23 个 model provider，但 Mastra 的 3300+ 模型 94 provider 是基于 Vercel AI SDK 的庞大生态。如果"模型路由"是核心诉求且团队接受 TypeScript，Mastra 是更省时的选择；如果坚持 Python，Agno + 自己封装一层 model router 也行，工作量约 2-3 天。技术栈决定框架，不是反过来。

> **为性能而性能。** 因为"2μs"听起来不错就选择 Agno，而工作负载是每个请求一个慢速 Agent 调用。开销不是瓶颈。
> **生态系统锁定。** Mastra 的 Vercel 风格集成在 Vercel 上是优势，在其他地方是劣势。
> **企业许可困惑。** Mastra 的 `ee/` 目录是源码可获取的，不是 Apache 2.0。如果你打算 fork，请先阅读许可证。

## Build It | 动手实现

This lesson is primarily comparative — no single code artifact would do both frameworks justice. See `code/main.py` for a side-by-side toy: a minimal "run an agent, stream the output, persist session" flow implemented twice (once Agno-shaped, once Mastra-shaped).

> 这一课主要是比较性的——没有一个代码产物能同时体现两个框架的特点。参见 `code/main.py` 中的并排演示：一个最小的"运行 Agent、流式输出、持久化会话"流程实现了两次（一次 Agno 形态，一次 Mastra 形态）。

> Agno 和 Mastra 是两种轻量级 Agent 运行时。Agno 专注快速构建，Mastra 专注 TypeScript 生产部署。两者都提供最小化的 Agent 抽象。

Run it:

```
python3 code/main.py
```

Two structurally different but functionally equivalent traces.

> 两个结构上不同但功能上等价的追踪。

> Agno 和 Mastra 是两种轻量级 Agent 运行时。Agno 专注快速构建，Mastra 专注 TypeScript 生产部署。两者都提供最小化的 Agent 抽象。

## Use It | 用框架实现

- **Agno** — Python backend that needs speed and FastAPI shape.
- **Mastra** — TypeScript backend with many providers and workflow primitives.
- Both ship first-party observability hooks. Both integrate with Langfuse.

## Ship It | 产出物

`outputs/skill-runtime-picker.md` picks Agno, Mastra, LangGraph, or a provider SDK based on stack, latency budget, and operational shape.

> `outputs/skill-runtime-picker.md` 根据技术栈、延迟预算和运营形态选择 Agno、Mastra、LangGraph 或提供商 SDK。

> Agno 和 Mastra 是两种轻量级 Agent 运行时。Agno 专注快速构建，Mastra 专注 TypeScript 生产部署。两者都提供最小化的 Agent 抽象。

## Exercises | 练习题

1. Read Agno's docs. Port the stdlib ReAct loop (Lesson 01) to Agno. What disappeared? What stayed?
  中文翻译：思考并实践此练习。
2. Read Mastra's docs. Port the same loop to Mastra. What changed in tool typing (Zod vs nothing)?
  中文翻译：思考并实践此练习。
3. Benchmark: measure agent instantiation latency on your stack. Does Agno's 2μs matter to your workload?
  中文翻译：思考并实践此练习。
4. Design a migration: if you've been running CrewAI in Python, what breaks if you move to Agno?
  中文翻译：思考并实践此练习。
5. Read Mastra's `ee/` license terms. What restrictions would affect an open-source fork?
  中文翻译：思考并实践此练习。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agno | "Fast Python agents" | Stateless session-scoped agent runtime |  |
| Mastra | "TypeScript agents on Vercel AI SDK" | Agents + Tools + Workflows + Model Router |  |
| Unified Model Router | "Multi-provider access" | Single client for 3,300+ models across 94 providers |  |
| Composite storage | "Multiple backends" | Memory/workflows/observability each to a different store |  |
| Mastra Studio | "Local debugger" | localhost:4111 UI for introspecting agents |  |
| Source-available | "Not OSS" | License permits source reading but restricts commercial use |  |

## Further Reading | 延伸阅读

- [Agno Agent Framework docs](https://www.agno.com/agent-framework) — performance targets, FastAPI integration
  中文翻译：见原文。
- [Mastra docs](https://mastra.ai/docs) — primitives, server adapters, Model Router
  中文翻译：见原文。
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — the stateful-graph alternative
  中文翻译：见原文。
- [Comet Opik](https://www.comet.com/site/products/opik/) — observability comparisons cited by Mastra integrations
  中文翻译：见原文。
