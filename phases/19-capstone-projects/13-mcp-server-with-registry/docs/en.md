# Capstone 13 — MCP Server with Registry and Governance | MCP 服务器 结业 注册中心

> The Model Context Protocol stopped being the future and became the default tool-use spec in 2026. Anthropic, OpenAI, Google, and every major IDE ship MCP clients. Pinterest published its internal ecosystem of MCP servers. The AAIF Registry formalized capability metadata at `.well-known`. AWS ECS published the reference stateless deployment. Block's goose-agent put the same protocol inside a hosted assistant. The 2026 production shape is: StreamableHTTP transport, OAuth 2.1 scopes, OPA policy gating, and a registry that lets platform teams discover, validate, and enable servers. Build that end to end.

> **【中文解读】** 本节是综合项目——构建带注册中心的 MCP 服务器。


**Type:** Capstone | **类型:** Capstone
**Languages:** Python (server, via FastMCP) or TypeScript (@modelcontextprotocol/sdk), Go (registry service) | **语言:** Python (server, via FastMCP) or TypeScript (@modelcontextprotocol/sdk), Go (registry service)
**Prerequisites:** Phase 11 (LLM engineering), Phase 13 (tools and MCP), Phase 14 (agents), Phase 17 (infrastructure), Phase 18 (safety)

> 🔗 **【前置】** 顶点项目 13 = 综合 Phase 11/13/14/17/18。MCP 服务器+注册中心 = 2026 默认工具规范（Anthropic/OpenAI/Google/IDE 全支持）。
> 💡 **【类比】** MCP 注册中心 = "AI 工具的应用商店"。2026 生产栈：StreamableHTTP 传输+OAuth 2.1 scope+OPA 策略门+AAIF 注册中心（`.well-known` 能力元数据）。参考 Pinterest 内部生态+AWS ECS 无状态部署+Block goose-agent。要求平台团队发现/验证/启用服务器。| **前置知识:** Phase 11 (LLM engineering), Phase 13 (tools and MCP), Phase 14 (agents), Phase 17 (infrastructure), Phase 18 (safety)
**Phases exercised:** P11 · P13 · P14 · P17 · P18 | **涉及阶段:** P11 · P13 · P14 · P17 · P18
**Time:** 25 hours | **时间:** 25 hours

## Problem | 问题引入

> **【中文解读】** 本节描述 MCP 服务器生产化的核心挑战。MCP 已成为工具使用的通用语言——Claude Code、Cursor 3、Amp、OpenCode、Gemini CLI 都消费 MCP 服务器。挑战不在编写服务器（FastMCP 很简单），而在企业级部署：每租户 OAuth 范围、OPA 策略对破坏性工具的门控、StreamableHTTP 无状态水平扩展、注册中心发现和每工具调用审计日志。

> **【拓展：MCP 生态系统】** 2026 年 MCP 生态：Anthropic、OpenAI、Google 和所有主流 IDE 都内置 MCP 客户端。Pinterest 发布了内部 MCP 服务器生态系统。AAIF Registry 规范标准化了 `.well-known/mcp-capabilities` 能力元数据。AWS ECS 发布了无状态部署参考。Block 的 goose-agent 将 MCP 协议嵌入托管助手。StreamableHTTP（2026 MCP 修订版）取代了 SSE+stdio，默认无状态、可水平扩展，支持长连接通知。

MCP became the tool-use lingua franca. Claude Code, Cursor 3, Amp, OpenCode, Gemini CLI, and every managed agent now consume MCP servers. The production challenges are not authoring servers (FastMCP makes that easy) but deploying them at scale with enterprise requirements: per-tenant OAuth scopes, OPA policy on destructive tools, StreamableHTTP stateless scaling, a registry for discovery, audit logs per tool call. Pinterest's internal MCP ecosystem and the AAIF Registry spec set the 2026 bar.

> MCP became the tool-use lingua franca.


You will build an MCP server exposing 10 internal tools (Postgres read-only, S3 listing, Jira, Linear, Datadog, etc.), a registry UI for platform discovery, and a human-approval gate for destructive tools. The load test demonstrates StreamableHTTP horizontal scaling. The audit trail satisfies an enterprise security review.

> 你will build an MCP server exposing 10 internal tools (Postgres read-only, S3 listing, Jira, Linear, Datadog, etc.), a registry UI for platform discovery, and a human-approval gate for destructive tools. The load test demonstrates StreamableHTTP horizontal scaling. The audit trail satisfies an enterprise security review.


## Concept | 核心概念

> **【中文解读】** MCP 2026 修订版强制 StreamableHTTP 作为默认传输：单个 HTTP 端点接受 JSON-RPC 请求、流式响应、支持长连接通知。无状态意味着可在负载均衡器后水平扩展。授权使用 OAuth 2.1 按工具范围控制（jira:read、s3:list、postgres:query:readonly），高风控工具需要 `approved:by:human` 范围（通过 Slack 审批卡提升）。注册中心是独立服务，轮询各服务器的 `.well-known/mcp-capabilities` 文档，验证并索引。

> **【拓展：MCP 安全与治理】** OPA/Rego 策略引擎在每个工具调用时检查授权、PII 脱敏和负载大小上限。破坏性工具（Jira 创建、Postgres 写入）部署在独立 MCP 服务器上，需要 Slack 审批卡在 15 分钟内提升的范围。审计日志采用每租户只追加 JSONL 格式，PII 在写入前通过 Presidio 脱敏。负载测试目标：100 并发客户端在 StreamableHTTP 上水平扩展，双副本无会话粘性。

MCP 2026 revision mandates StreamableHTTP as the default transport. Unlike the earlier stdio-and-SSE shape, StreamableHTTP is stateless by default: a single HTTP endpoint accepts JSON-RPC requests, streams responses, and supports long-lived connections for notifications. Stateless means horizontally scalable behind a load balancer.

> MCP 2026 revision mandates StreamableHTTP as the default transport.


Authorization is OAuth 2.1 with per-tool scopes. A token carries scopes like `jira:read`, `s3:list`, `postgres:query:readonly`. The MCP server checks scopes at tool-call time, not just session start. For high-risk tools, the server rejects any call whose scope is not elevated to `approved:by:human` within the last N minutes — that elevation comes from a Slack review card.

> Authorization is OAuth 2.


The registry is a separate service. Every MCP server exposes a `.well-known/mcp-capabilities` document with its tool manifest, transport URL, auth requirements. The registry polls, validates, and indexes. Platform teams use the registry UI to see what tools are available, what scopes they need, and which teams own them.

> registry is a separate service. Every MCP server exposes a `.well-known/mcp-capabilities` document with its tool manifest, transport URL, auth requirements. The registry polls, validates, and indexes. Platform teams use the registry UI to see what tools are available, what scopes they need, and which teams own them.


## Architecture | 架构

```
MCP client (Claude Code, Cursor 3, ...)
          |
          v
StreamableHTTP over HTTPS (JSON-RPC + streaming)
          |
          v
MCP server (FastMCP) behind load balancer
          |
   +------+------+---------+----------+------------+
   v             v         v          v            v
Postgres    S3 listing  Jira       Linear     Datadog
(read-only) (paged)     (read)     (read)     (query)
          |
   +------+-------------+
   v                    v
 OPA policy gate   destructive tool MCP (separate server)
                        |
                        v
                   human approval via Slack
                        |
                        v
                   audit log (append-only, per-tenant)

  registry service
     |
     v  GET /.well-known/mcp-capabilities from each server
     v
     UI: search / validate / enable-disable / ownership
```

## Stack | 技术栈

- Server framework: FastMCP (Python) or `@modelcontextprotocol/sdk` (TypeScript)
  中文翻译：Server framework: FastMCP (Python) or `@modelcontextprotocol/sdk` (TypeScript)
- Transport: StreamableHTTP over HTTPS (stateless)
  中文翻译：Transport: StreamableHTTP over HTTPS (stateless)
- Auth: OAuth 2.1 with workload identity via SPIFFE / SPIRE
  中文翻译：Auth: OAuth 2.1 with workload identity via SPIFFE / SPIRE
- Policy: OPA / Rego rules per tool; policy decision service per request
  中文翻译：Policy: OPA / Rego rules per tool; policy decision service per request
- Registry: self-hosted, consumes `.well-known/mcp-capabilities` manifests
  中文翻译：Registry: self-hosted, consumes `.well-known/mcp-capabilities` manifests
- Human approval: Slack interactive message for destructive tools
  中文翻译：Human approval: Slack interactive message for destructive tools
- Deployment: AWS ECS Fargate or Fly.io, one server per tenant or shared with tenant scoping
  中文翻译：Deployment: AWS ECS Fargate or Fly.io, one server per tenant or shared with tenant scoping
- Audit: structured JSONL per-tenant bucket with per-call lineage
  中文翻译：Audit: structured JSONL per-tenant bucket with per-call lineage

## Build It | 动手构建

> **【中文解读】** 构建带注册中心的 MCP 服务器：暴露 10 个内部工具（Postgres 只读查询、S3 列表、Jira/Linear 搜索、Datadog 指标查询、PagerDuty 值班查询、GitHub 只读、Notion/Slack 搜索、Salesforce 读取），每个工具带类型化 schema 和范围标签。租户隔离通过范围标签实现——每个租户只能看到授权范围内的工具。

> **【拓展：MCP 注册中心在企业级部署中的角色】** Model Context Protocol 的注册中心是企业 AI 治理的核心组件。它解决三个问题：1）工具发现（Agent 知道有哪些工具可用）；2）权限控制（基于角色的工具访问）；3）版本管理（工具 schema 变更的向后兼容性）。Anthropic 的 Claude Enterprise 和 Microsoft 的 Copilot Studio 都实现了类似的工具注册中心。本课的 10 工具面是企业级 MCP 部署的标准起点。

1. **Tool surface.** Expose 10 internal tools: Postgres read-only query, S3 list objects, Jira search/fetch, Linear search/fetch, Datadog metric query, PagerDuty on-call lookup, GitHub read-only, Notion search, Slack search, Salesforce read. Each tool has a typed schema and a scope label.
   中文翻译：1. **Tool surface.** Expose 10 internal tools: Postgres read-only query, S3 list objects, Jira search/fetch, Linear search/fetch, Datadog metric query, PagerDuty on-call lookup, GitHub read-only, Notion search, Slack search, Salesforce read. Each tool has a typed schema and a scope label.

2. **FastMCP server.** Mount the tools. Configure StreamableHTTP transport. Add a middleware for OAuth token introspection and scope enforcement.
   中文翻译：2. **FastMCP server.** Mount the tools. Configure StreamableHTTP transport. Add a middleware for OAuth token introspection and scope enforcement.

3. **OPA policy.** Rego policy per tool: what scopes permit invocation, what PII redaction applies, what payload-size caps apply. Decision service called on every tool call.
   中文翻译：3. **OPA policy.** Rego policy per tool: what scopes permit invocation, what PII redaction applies, what payload-size caps apply. Decision service called on every tool call.

4. **Registry service.** Separate Go or TS service that polls `.well-known/mcp-capabilities` from registered servers, validates with JSON Schema, and exposes a list / search / validate / enable-disable UI.
   中文翻译：4. **Registry service.** Separate Go or TS service that polls `.well-known/mcp-capabilities` from registered servers, validates with JSON Schema, and exposes a list / search / validate / enable-disable UI.

5. **Capability manifest.** Each server exposes `.well-known/mcp-capabilities` with: tool list, auth requirements, transport URL, owner team, SLO.
   中文翻译：5. **Capability manifest.** Each server exposes `.well-known/mcp-capabilities` with: tool list, auth requirements, transport URL, owner team, SLO.

6. **Destructive tool separation.** Tools that mutate state (Jira create, Linear create, Postgres write) live on a second MCP server with a stricter auth flow: tokens must have a `approved:by:human` scope elevated via Slack card within 15 minutes.
   中文翻译：6. **Destructive tool separation.** Tools that mutate state (Jira create, Linear create, Postgres write) live on a second MCP server with a stricter auth flow: tokens must have a `approved:by:human` scope elevated via Slack card within 15 minutes.

7. **Audit log.** Append-only JSONL per tenant: `{timestamp, user, tool, args_redacted, response_redacted, outcome}`. PII redaction via Presidio before write.
   中文翻译：7. **Audit log.** Append-only JSONL per tenant: `{timestamp, user, tool, args_redacted, response_redacted, outcome}`. PII redaction via Presidio before write.

8. **Load test.** 100 concurrent clients on StreamableHTTP. Demonstrate horizontal scaling by adding a second replica; show the load balancer redistributing without session stickiness.
   中文翻译：8. **Load test.** 100 concurrent clients on StreamableHTTP. Demonstrate horizontal scaling by adding a second replica; show the load balancer redistributing without session stickiness.

9. **Conformance tests.** Run the official MCP conformance suite against both servers. Pass all mandatory sections.
   中文翻译：9. **Conformance tests.** Run the official MCP conformance suite against both servers. Pass all mandatory sections.

## Use It | 使用方法

```
$ curl -H "Authorization: Bearer eyJhbGc..." \
       -X POST https://mcp.internal.example.com/ \
       -d '{"jsonrpc":"2.0","method":"tools/call",
            "params":{"name":"postgres.readonly","arguments":{"sql":"SELECT 1"}}}'
[registry]   capability validated: postgres.readonly v1.2
[policy]    scope postgres:query:readonly present; allowed
[audit]     logged: user=u42 tool=postgres.readonly outcome=ok
response:    { "result": { "rows": [[1]] } }
```

## Ship It | 部署上线

`outputs/skill-mcp-server.md` describes the deliverable. A production-grade MCP server + registry + audit layer for internal tools with OAuth 2.1 scopes and OPA gating.

> 描述了交付物。


| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | Spec conformance | StreamableHTTP + capability manifest passes MCP conformance tests |
| 20 | Security | Scope enforcement, OPA coverage across every tool, secret hygiene |
| 20 | Observability | Per-tool-call audit log with PII redaction |
| 20 | Scale | 100-client load test horizontal scale demonstration |
| 15 | Registry UX | Discover / validate / enable-disable workflow |
| **100** | | |

## Exercises | 练习题

1. Add a new tool (Confluence search). Ship it through the registry validation flow without touching the core server.

2. Write an OPA policy that redacts Postgres query results containing columns named `email`, `ssn`, or `phone`. Exercise with a probe query.

3. Benchmark StreamableHTTP vs stdio on local latency. Report per-call p50/p95.

4. Implement per-tenant quota: maximum N calls per minute per tool per tenant. Enforce via a second OPA rule.

5. Run the MCP conformance suite from [mcp-conformance-tests](https://github.com/modelcontextprotocol/conformance) and fix every failure.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| StreamableHTTP | "2026 MCP transport" | Stateless HTTP + streaming; replaces SSE + stdio for networked servers |
| Capability manifest | "Well-known doc" | `.well-known/mcp-capabilities` with tool list, auth, transport URL |
| OPA / Rego | "Policy engine" | Open Policy Agent for authorizing tool calls against external rules |
| Scope elevation | "Approved-by-human" | Short-lived scope granted via Slack approval, required for destructive tools |
| Registry | "Tool discovery" | Service that indexes MCP servers from their capability manifests |
| Workload identity | "SPIFFE / SPIRE" | Cryptographic service identity for OAuth token issuance |
| Conformance suite | "Spec tests" | Official MCP test battery for StreamableHTTP + tool manifest correctness |

## Further Reading | 延伸阅读

- [Model Context Protocol 2026 Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) — StreamableHTTP, capability metadata, registry
- [AAIF MCP Registry spec](https://github.com/modelcontextprotocol/registry) — the 2026 registry spec
- [AWS ECS reference deployment](https://aws.amazon.com/blogs/containers/deploying-model-context-protocol-mcp-servers-on-amazon-ecs/) — reference production deployment
- [Pinterest internal MCP ecosystem](https://www.infoq.com/news/2026/04/pinterest-mcp-ecosystem/) — the reference internal deployment
- [Block `goose` MCP usage](https://block.github.io/goose/) — reference agent consumption pattern
- [FastMCP](https://github.com/jlowin/fastmcp) — Python server framework
- [Open Policy Agent](https://www.openpolicyagent.org/) — policy engine reference
- [SPIFFE / SPIRE](https://spiffe.io) — workload identity reference
