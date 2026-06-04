# 生产 运行时 Mastra Agno

> Agno (Python) and Mastra (TypeScript) are the 2026 production-runtime pairing. Agno aims at microsecond agent instantiation and stateless FastAPI backends. Mastra ships agents, tools, workflows, unified model routing, and composite storage on the Vercel AI SDK substrate.


**类型：** 学习
**语言：** Python, TypeScript
**前置条件：** Phase 14 · 01 (Agent Loop), Phase 14 · 13 (LangGraph)
**预计时间：** ~45 minutes

## 学习目标

- Identify Agno's performance targets and when they matter.
- Name Mastra's three primitives — Agents, Tools, Workflows — and the supported server adapters.
- Explain why a stateless session-scoped FastAPI backend is the recommended Agno production path.
- Pick Agno vs Mastra for a given stack (Python-first vs TypeScript-first).

## 问题引入

> **【中文解读】** Agno 和 Mastra 代表了 2026 年的两种 Agent 运行时设计哲学。Agno（原 PhiData）追求极简——用最少的代码构建 Agent。Mastra（TypeScript）追求全功能——提供完整的 Agent 生命周期管理。选择取决于团队的技术栈和复杂度需求。
> **【拓展：Agno (GitHub 15k+ stars) 和 Mastra 是 2026 年 Agent 运...】** Agno (GitHub 15k+ stars) 和 Mastra 是 2026 年 Agent 运行时的新秀。Agno 的哲学是'Agent 即函数'——每个 Agent 是一个带有工具集的异步函数。Mastra 基于 TypeScript，面向全栈开发者，提供完整的 Agent 生命周期管理（部署、监控、扩展）。两者都支持多模型后端和 MCP 集成。

## 核心概念

### Agno
- Python runtime, formerly Phi-data.
- "No graphs, chains, or convoluted patterns — just pure python."
- Performance targets from their docs: ~2μs agent instantiation, ~3.75 KiB memory per agent, ~23 model providers.
- Production path: stateless session-scoped FastAPI backend. Each request starts a fresh agent; session state lives in a DB.
- Native multimodal (text, image, audio, video, file) and agentic RAG.
The speed targets matter when you have thousands of short-lived agents per second (chat fan-in, evaluation pipelines). They matter less when one agent runs for 10 minutes.
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
- **Language fit.** Agno for Python-first teams; Mastra for TypeScript-first.
- **Runtime ergonomics.** Agno = near-zero overhead; Mastra = integrated with the Vercel ecosystem.
- **Observability.** Both integrate with Langfuse/Phoenix/Opik (Lesson 24) but Mastra Studio is first-party.
### When to pick each
- **Agno** — Python backend, many short-lived agents, strong perf requirements, FastAPI shop.
- **Mastra** — TypeScript backend, Next.js / Vercel deploy, unified multi-provider model routing, Zod-typed tools.
- **LangGraph** (Lesson 13) — when durable state and explicit graph reasoning matter more than raw speed.
- **OpenAI / Claude Agent SDK** — when you want the provider's productized shape (Lessons 16–17).
### Where this pattern goes wrong
- **Perf-for-perf's-sake.** Picking Agno because "2μs" sounds good when the workload is one slow agent call per request. Overhead is not the bottleneck.
- **Ecosystem lock-in.** Mastra's Vercel-flavored integration is a plus on Vercel, a minus elsewhere.
- **Enterprise license confusion.** Mastra's `ee/` directories are source-available, not Apache 2.0. Read the licenses if you're planning to fork.

## 动手实现

This lesson is primarily comparative — no single code artifact would do both frameworks justice. See `code/main.py` for a side-by-side toy: a minimal "run an agent, stream the output, persist session" flow implemented twice (once Agno-shaped, once Mastra-shaped).
Run it:
```
python3 code/main.py
```
Two structurally different but functionally equivalent traces.

## 用框架实现

- **Agno** — Python backend that needs speed and FastAPI shape.
- **Mastra** — TypeScript backend with many providers and workflow primitives.
- Both ship first-party observability hooks. Both integrate with Langfuse.

## 产出物

`outputs/skill-runtime-picker.md` picks Agno, Mastra, LangGraph, or a provider SDK based on stack, latency budget, and operational shape.

## 练习题

1. Read Agno's docs. Port the stdlib ReAct loop (Lesson 01) to Agno. What disappeared? What stayed?
   *思考并实践此练习*
2. Read Mastra's docs. Port the same loop to Mastra. What changed in tool typing (Zod vs nothing)?
   *思考并实践此练习*
3. Benchmark: measure agent instantiation latency on your stack. Does Agno's 2μs matter to your workload?
   *思考并实践此练习*
4. Design a migration: if you've been running CrewAI in Python, what breaks if you move to Agno?
   *思考并实践此练习*
5. Read Mastra's `ee/` license terms. What restrictions would affect an open-source fork?
   *思考并实践此练习*

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Agno | "Fast Python agents" |
| Mastra | "TypeScript agents on Vercel AI SDK" |
| Unified Model Router | "Multi-provider access" |
| Composite storage | "Multiple backends" |
| Mastra Studio | "Local debugger" |
| Source-available | "Not OSS" |

## 延伸阅读

