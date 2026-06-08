# FinOps for LLMs — Unit Economics and Multi-Tenant Attribution | LLM 的 FinOps——单位经济与多租户归因

> Traditional FinOps breaks on LLM spend. Costs are token-transactions, not resource-uptime. Tags don't map — an API call is a transaction, not an asset. Engineering decisions (prompt design, context window, output length) are financial decisions. The 2026 playbook has three attribution dimensions to instrument on day one: per-user (`user_id`) for seat pricing and expansion, per-task (`task_id` + `route`) for product surface cost and prioritization, per-tenant (`tenant_id`) for unit economics and renewal. Four token layers — prompt, tool, memory, response — one bucket hides spend. Enforcement ladder for multi-tenant products: rate limits per tenant (2-3x expected peak, clear 429 + retry-after); daily spend cap (1.5-3x contracted ceiling; triggers rate tightening + alert); kill switches on spend z-score > 4 (auto-pause + page on-call). Attribution patterns: tag-and-aggregate, telemetry-joiner (trace-ID → billing; highest accuracy), sampling-and-extrapolation, model-based allocation, event-sourced, real-time streaming. Unit metric: cost per resolved query, cost per generated artifact — not $/M tokens. Retroactive tagging always misses; instrument at request creation.

> **【中文解读】** 传统 FinOps 在 LLM 支出上失效了——成本是 Token 交易而非资源运行时间。工程决策（提示设计、上下文窗口、输出长度）就是财务决策。2026 年的 Playbook 建议在第一天就建立三个归因维度：按用户、按任务、按租户。四个 Token 层（提示、工具、记忆、响应）不能合并为一个桶。单位指标应为"每次解决的查询成本"，而非"每百万 Token 成本"。

> **【拓展：FinOps → LLM 成本优化】** 在 LLM 应用中，成本控制是核心挑战。vLLM + 量化部署可降低推理成本，模型路由（简单任务用小模型、复杂任务用大模型）可优化性价比，语义缓存可减少重复调用。FinOps 的"在请求创建时就埋点"原则是 LLM 成本可观测化的基础。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cost-attribution simulator with kill switch) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 14 (Caching) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 14 (Caching)
**Time:** ~60 minutes | **时间:** ~60 minutes

## Learning Objectives | 学习目标

- Explain why traditional FinOps (tags + tiers) breaks on LLM spend and name the three new attribution dimensions.
  中文翻译：解释为什么传统 FinOps（标签 + 层级）在 LLM 支出上失效，并说出三个新归因维度。
- Enumerate the four token layers (prompt, tool, memory, response) and why single-bucket billing hides cost.
  中文翻译：列举四个 token 层（提示、工具、记忆、响应），以及为什么单桶计费产生误导。
- Design an enforcement ladder (rate → spend cap → kill switch) for a multi-tenant product.
  中文翻译：设计执行阶梯（速率 -> 支出上限 -> 熔断开关）用于多租户 LLM 服务。
- Pick a unit metric (cost per resolved query / artifact) instead of $/M tokens.
  中文翻译：选择单位指标（每次解决查询/产物的成本）而非 $/M tokens。

## The Problem | 问题引入

> **【中文解读】** 传统 FinOps 在 LLM 支出上失效的核心原因：LLM 成本是 token 交易而非资源运行时间。标签（tags）无法直接映射——API 调用是交易而非资产。工程决策（提示设计、上下文窗口、输出长度）就是财务决策。你的账单显示 $40,000，但你不知道：哪个租户花了多少、哪个产品功能驱动的、是否有用户滥用、是 prompt 膨胀还是工具调用还是记忆放大导致的。

Your bill says $40,000. You don't know:
- Which tenant spent it.
- Which product feature drove it.
- Whether any individual user was abusive.
- Whether prompt bloat, tool calls, or memory amplification was the culprit.

Tag-and-aggregate on provider-side works for cloud resources (EC2, S3) where tags propagate to line items. LLM API calls do not auto-tag — you have to stamp user/task/tenant at the call site and carry through. Retroactive attribution always misses edge cases.

## The Concept | 核心概念

### Three attribution dimensions

**Per-user** (`user_id`): who is costing what. Drives seat pricing, expansion conversations, identifies power users.

**Per-task** (`task_id` + `route`): which product surface costs what. Drives feature prioritization, kill-expensive-features decisions.

**Per-tenant** (`tenant_id`): which customer is profitable. Drives unit economics, renewal pricing, tier thresholds.

Instrument all three at call site on day one. Retroactive is always worse.

### Four token layers

| Layer | Example | Typical % of total |
|-------|---------|---------------------|
| Prompt | system + user input | 40-60% |
| Tool | tool-call results fed back | 20-40% (agent workloads) |
| Memory | prior conversation / retrieved docs | 10-30% |
| Response | model output | 10-30% |

Bucketing all four together makes optimization blind. Break them out in your attribution schema.

### Enforcement ladder

> **【中文解读】** 多租户产品的三级强制阶梯：(1) 速率限制——每租户 2-3x 预期峰值，返回 429 + Retry-After，租户感受到摩擦但无意外账单；(2) 日支出上限——每租户 1.5-3x 合约上限，触发时收紧速率限制 + 告警客户成功团队；(3) Kill switch——当支出 z-score > 4（相对租户基线）时自动暂停租户，通知值班，升级到运维和客户成功。

> **【拓展：LLM FinOps 的复合优化栈】** LLM FinOps 的复合优化栈（缓存 + 批处理 + 路由 + 网关）叠加后的效果：(1) 缓存 L2（Phase 17·14）——约 10x 更便宜的输入；(2) 批处理（Phase 17·15）——50% 折扣；(3) 路由到廉价模型（Phase 17·16）——60% 成本降低；(4) 网关效率（Phase 17·19）——冗余 + 重试。全栈叠加最优可降至朴素基线的约 5-10%。大多数团队只启用了 2-3 个杠杆，很少有团队叠加全部四个。

1. **Rate limit** per tenant. 2-3x expected peak. Return 429 with `Retry-After`. Tenant sees friction; no surprise bill.

2. **Daily spend cap** per tenant. 1.5-3x contracted ceiling. Trigger: tighten rate limit + alert customer-success.

3. **Kill switch** on spend z-score > 4 relative to tenant baseline. Auto-pause tenant; page on-call; escalate to ops + CS.

### Attribution patterns

- **Tag-and-aggregate**: stamp metadata headers; aggregate later. Simple; rough.
- **Telemetry joiner**: join traces to billing via trace IDs. Highest accuracy. What mature teams do.
- **Sampling + extrapolation**: sample 5-10%, multiply. Cost-effective for rough spend; misses tails.
- **Model-based allocation**: regression to infer cost driver. For legacy data without tags.
- **Event-sourced**: cost as events in a stream (Kafka / Kinesis). Real-time.
- **Real-time streaming**: dashboard updates sub-second.

### Cost per X is the unit metric

> **【中文解读】** $/M tokens 是供应商语言。产品指标应该是：(1) 每解决的支持工单成本；(2) 每生成文章成本；(3) 每成功 Agent 任务成本；(4) 每用户会话分钟成本。将成本绑定到产品产出上，否则优化没有锚点。关键原则：在请求创建时就埋点（retroactive tagging 总是遗漏），不要事后补充归因。

$/M tokens is vendor speak. Product metrics:

- Cost per resolved support ticket.
- Cost per generated article.
- Cost per successful agent task.
- Cost per user-session-minute.

Tie cost to a product outcome. Otherwise optimization is unanchored.

### Cost attribution trace shape

```
trace_id: abc123
  user_id: u_42
  tenant_id: t_7
  task_id: task_classify_doc
  route: model_haiku
  layers:
    prompt_tokens: 1800
    tool_tokens: 600
    memory_tokens: 400
    response_tokens: 150
  cost_usd: 0.0135
  cached_input: true
  batch: false
```

Emit on every call. Store in data lake. Aggregate per dimension. Phase 17 · 13 observability stack is where this lives.

### The compounded-savings stack

Stack: cache + batch + route + gateway. With all four:
- Cache L2 (Phase 17 · 14): ~10x cheaper input.
- Batch (Phase 17 · 15): 50% off.
- Route to cheap model (Phase 17 · 16): 60% cost reduction.
- Gateway efficiency (Phase 17 · 19): redundancy + retries.

Best-case stacked: ~5-10% of naive baseline. Most teams have 2-3 levers engaged; few stack all four.

### Numbers you should remember

- Attribution dimensions: per-user, per-task, per-tenant.
- Four token layers: prompt, tool, memory, response.
- Kill switch: spend z-score > 4.
- Unit metric: cost per resolved query, not $/M tokens.
- Stacked optimizations: ~5-10% of baseline possible.

## Use It | 用框架实现

`code/main.py` simulates a multi-tenant LLM service with the three-tier enforcement ladder. Injects an abusive tenant and demonstrates the kill switch firing.

> `code/main.py` simulates a multi-tenant LLM service with the three-tier enforcement ladder. Injects an abusive tenant and demonstrates the kill switch firing.

> `code/main.py` simulates a multi-tenant LLM service with the three-tier enforcement ladder. Injects an abusive tenant and demonstrates the kill switch firing.

## Ship It | 产出物

This lesson produces `outputs/skill-finops-plan.md`. Given product and scale, designs the attribution schema and enforcement ladder.

> 本课产出 `outputs/skill-finops-plan.md`. Given product and scale, designs the attribution schema and enforcement ladder.

## Exercises | 练习题

1. Run `code/main.py`. At what z-score does the kill switch fire? How do you pick the threshold?
   中文翻译：运行 `code/main.py`。熔断开关在什么 z-score 下触发？如何防止误报？
2. Design a per-tenant, per-task cost dashboard. What are the 5 views you build first?
   中文翻译：设计按租户、按任务的成本仪表板。你首先构建哪 5 个视图？
3. Your largest tenant is unit-economics-negative. Propose three interventions ordered by customer impact.
   中文翻译：你最大的租户单位经济学为负。提出三个按影响排名的干预措施。
4. Compute cost per resolved ticket for a support product: 3M tokens/ticket, ~800 tickets/day, GPT-5 cached rate.
   中文翻译：计算支持产品的每解决工单成本：3M tokens/工单，约 2.5 次重试。单位经济学可行吗？
5. Argue whether retroactive tagging can ever work. When is it acceptable?

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Per-user attribution | "user-level cost" | `user_id` stamped on every call |
| Per-task attribution | "feature cost" | `task_id` + `route` identify product surface |
| Per-tenant attribution | "customer cost" | `tenant_id`; drives unit economics |
| Four token layers | "cost layers" | prompt + tool + memory + response |
| Rate limit | "429 guard" | Per-tenant ceiling enforced at gateway |
| Daily spend cap | "daily ceiling" | Tenant-scoped budget with alert |
| Kill switch | "auto-pause" | Spend z-score > 4 triggers auto-suspension |
| Cost per resolved | "product unit metric" | Cost tied to product outcome, not tokens |
| Telemetry joiner | "trace-to-billing" | Highest-accuracy attribution pattern |
| Stacked optimization | "cache+batch+route+gateway" | Compounding savings to ~5-10% baseline |

## Further Reading | 延伸阅读

- [FinOps Foundation — FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/)
- [FinOps School — Cost per Unit 2026 Guide](https://finopsschool.com/blog/cost-per-unit/)
- [Digital Applied — LLM Agent Cost Attribution 2026](https://www.digitalapplied.com/blog/llm-agent-cost-attribution-guide-production-2026)
- [PointFive — Managed LLMs in Azure OpenAI](https://www.pointfive.co/blog/finops-for-ai-economics-of-managed-llms-in-azure-open-ai)
