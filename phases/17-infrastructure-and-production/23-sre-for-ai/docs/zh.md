# SRE for AI — Multi-Agent Incident Response, Runbooks, Predictive Detection | 多 Agent SRE PR

> AI SRE uses LLMs grounded in infrastructure data (logs, runbooks, service topology) via RAG to automate investigation, documentation, and coordination phases. The 2026 architecture pattern is multi-agent orchestration — specialized agents (logs, metrics, runbooks) coordinated by a supervisor; AI proposes hypotheses and queries, humans approve judgment calls. Datadog Bits AI and Azure SRE Agent ship this as managed products. Runbooks are evolving: NeuBird Hawkeye uses adversarial evaluation (two models analyze the same incident; agreement = confidence, disagreement = uncertainty); operational memory persists across team changes. Auto-remediation stays cautious: AI suggests, humans approve. Fully autonomous action is narrow (restart pod, rollback specific deploy) with tight guardrails — anyone selling "set it and forget it" is overselling. Emerging frontier: pre-incident prediction. MIT research reports an LLM trained on historical logs + GPU temps + API error patterns predicted 89% of outages 10-15 min early. Projection: 95% of enterprise LLMs have automated failover by end-2026.

> **【中文解读】** 本节介绍了 AI 的 SRE 实践——LLM 服务的站点可靠性工程方法论。


**类型：** 学习
**语言：** Python (stdlib, toy multi-agent incident triage simulator)
**前置条件：** Phase 17 · 13 (Observability), Phase 17 · 24 (Chaos Engineering)
**时间：** ~60 minutes

## 学习目标 | 学习目标

- Diagram the multi-agent AI SRE architecture: supervisor + specialized agents (logs, metrics, runbooks) + human approval gate.
- Explain why auto-remediation is narrow (restart pod, revert deploy) rather than broad (re-architect service).
- Name the adversarial evaluation pattern (NeuBird Hawkeye): two models agree = confidence; disagree = escalate.
- Cite the MIT 89% early-detection result and the operational constraint: predictions without actuation are just dashboards.

## 问题引入 | 问题

> **【中文解读】** AI SRE 的核心洞察：2026 年，事件调查的前 20 分钟是可自动化的——按服务分组日志、关联到最近部署、匹配 runbook——都是 RAG + 工具使用。监督式 Agent 可以在人类打开 Datadog 之前完成首轮分类并呈现假设。完全自主修复是不同的问题——重启 Pod 安全、扩展 GPU 池安全（如果策略允许）、重新架构服务绝对不行。

> **【拓展：AI SRE 产品市场】** 2026 年 AI SRE 产品：(1) Datadog Bits AI——Datadog 内部的托管 SRE copilot；(2) Azure SRE Agent——Azure 原生；(3) NeuBird Hawkeye——对抗性评估（两个模型独立分析同一事件，一致=高置信，不一致=升级）+ 操作记忆（post-mortem 存入向量 DB）；(4) PagerDuty AIOps——分类 + 去重；(5) Incident.io Autopilot——事件指挥官 + 协调。MIT 2025 研究显示，LLM 在历史日志 + GPU 温度 + API 错误模式上训练，可在 10-15 分钟前预测 89% 的停机。

An on-call engineer gets paged at 3 a.m. "High error rate in checkout." They check Datadog, Loki, three runbooks, the deploy log. 30 minutes later they realize the root cause is a vLLM OOM from a KV cache spike. They restart the pod; error clears.

In 2026 the first 20 minutes of that investigation are automatable. Grouping logs by service, correlating to recent deploys, matching against runbooks — all are RAG + tool-use. A supervised agent can do first-pass triage and present a hypothesis before the human opens Datadog.

Fully autonomous remediation is a different problem. Restart pod: safe. Scale GPU pool: safe if policy allows. Re-architect the service: absolutely not. The discipline is drawing the narrow line.

## 核心概念 | 概念

### Multi-agent architecture

> **【中文解读】** 多 Agent AI SRE 架构：Supervisor 将事件拆分为子查询，分派给专业化 Agent（日志 Agent 搜索日志、指标 Agent 查询 PromQL、Runbook Agent 检索文档）。Supervisor 综合，向人类呈现假设 + 证据。人类批准或重定向。安全自动修复范围：重启 Pod、回滚特定部署、在预批准范围内扩展池。不安全范围：更改服务拓扑、修改资源限制、部署新代码、更改 IAM。

```
          Incident
             │
             ▼
        Supervisor
        /    |    \
       ▼     ▼     ▼
  Log agent  Metric agent  Runbook agent
       │     │     │
       └─────┴─────┘
             │
             ▼
        Hypothesis + evidence
             │
             ▼
        Human approval
             │
             ▼
        Action (narrow set)
```

Supervisor breaks the incident into sub-queries. Specialized agents have tool access (log search, PromQL, doc retrieval). Supervisor synthesizes, presents hypothesis + evidence to human. Human approves or redirects.

### Auto-remediation scope

> **【拓展：AI SRE 自动修复的安全边界】** AI SRE 自动修复的安全边界划分：安全（窄范围）——重启 Pod、回滚特定部署、在预批准范围内扩展池、启用预批准 feature flag。不安全（广范围）——更改服务拓扑、修改资源限制、部署新代码、更改 IAM、修改数据库。任何声称"设置后就忘了"的供应商都在过度承诺。安全集合随 AI SRE 成熟而扩大，但边界是真实的。2026 年的最佳实践是：AI 建议、人类批准——仅对明确的窄范围操作（如 Pod 重启）允许完全自动化。

**Safe (narrow)**: restart pod, revert specific deploy, scale pool within pre-approved bounds, enable pre-approved feature flag.

**Not safe (broad)**: change service topology, modify resource limits, deploy new code, change IAM, alter databases.

Anyone selling "set it and forget it" is overselling. The safe set grows as AI SRE matures, but the boundary is real.

### Adversarial evaluation (NeuBird Hawkeye)

Two models independently analyze the same incident. If they agree on root cause, confidence is high. If they disagree, escalate to human with both hypotheses visible. Simple pattern, effective filter against hallucinated root causes.

### Operational memory

Team turnover is the silent kill of traditional SRE — tribal knowledge leaves. AI SRE stores runbooks + post-mortems in a vector DB; agents retrieve on every new incident. When new engineers join, the AI has full history.

### Pre-incident prediction

MIT 2025 research: LLM trained on historical logs, GPU temperatures, API error patterns predicted 89% of outages 10-15 minutes before they happened on the test set.

Reality check: predictions without actuation are dashboards. The operational question is "when we predict, what do we do?" Pre-emptive drain? Pager? Auto-scale? The answer is policy-specific.

### Products in 2026

- **Datadog Bits AI** — managed SRE copilot inside Datadog.
- **Azure SRE Agent** — Azure-native.
- **NeuBird Hawkeye** — adversarial eval + operational memory.
- **PagerDuty AIOps** — triage + deduplication.
- **Incident.io Autopilot** — incident commander + coordination.

### Runbooks as code

> **【拓展：AI SRE 实施路径】** AI SRE 的实施建议：(1) 首先将非结构化 runbook 转为结构化 markdown（症状、假设、验证、行动）；(2) 实现对抗性评估——两个独立模型分析同一事件；(3) 建立操作记忆——将 post-mortem + runbook 存入向量 DB；(4) 从"AI 建议人类批准"开始，不要直接跳到自主行动；(5) 预事件预测——MIT 研究显示 10-15 分钟提前量，但"预测后做什么"需要策略定义（预排水？告警？自动扩展？）。预计到 2026 年底 95% 的企业 LLM 服务将有自动 failover。

Runbooks evolve from Confluence pages to versioned markdown with structured sections (symptom, hypothesis, verify, act). Structured runbooks feed better RAG retrieval. Start any AI-SRE rollout by turning unstructured runbooks into structured.

### Numbers you should remember

- MIT early-detection: 89% of outages, 10-15 min lead time.
- Multi-agent triage: supervisor + (logs, metrics, runbooks) + human.
- Safe auto-remediation set: restart pod, revert deploy, scale within bounds.
- Adversarial eval: two models independent; agreement = confidence.

## 用框架实现 | 使用方法

`code/main.py` simulates a multi-agent triage: log agent finds error, metric agent finds CPU spike, runbook agent matches to known issue. Supervisor ranks hypotheses.

## 产出物 | 部署上线

This lesson produces `outputs/skill-ai-sre-plan.md`. Given current on-call, incident volume, team maturity, designs an AI SRE rollout.

## 练习题 | 练习题

1. Run `code/main.py`. What if the log and metric agents disagree? How does the supervisor resolve?
2. Define three "safe" auto-remediation actions for your service. Justify each.
3. Write a structured runbook template: sections, required fields, verification commands.
4. Predictive detection fires at 12 min lead. What's your policy — pager, pre-drain, or both?
5. Argue whether a 3-person team should adopt AI SRE in 2026 or wait. Consider maturity, volume, risk.

## 术语速查表 | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| AI SRE | "agent for on-call" | LLM-backed incident investigation + coordination |
| Supervisor agent | "the orchestrator" | Top-level agent breaking incidents into sub-queries |
| Specialized agent | "domain agent" | Sub-agent with tool access (logs, metrics, runbooks) |
| Auto-remediation | "AI fixes it" | Narrow pre-approved action; NOT broad re-architecture |
| Operational memory | "vector runbooks" | Post-mortems + runbooks in vector DB for RAG |
| Adversarial eval | "two-model check" | Independent analyses; agreement = confidence |
| NeuBird Hawkeye | "the adversarial one" | Product with adversarial-eval + memory pattern |
| Bits AI | "Datadog's SRE agent" | Datadog-managed AI SRE |
| Pre-incident prediction | "early detection" | 10-15 min lead time on outage prediction |

## 延伸阅读 | 延伸阅读

- [incident.io — AI SRE Complete Guide 2026](https://incident.io/blog/what-is-ai-sre-complete-guide-2026)
- [InfoQ — Human-Centred AI for SRE](https://www.infoq.com/news/2026/01/opsworker-ai-sre/)
- [DZone — AI in SRE 2026](https://dzone.com/articles/ai-in-sre-whats-actually-coming-in-2026)
- [Datadog Bits AI](https://www.datadoghq.com/product/bits-ai/)
- [NeuBird Hawkeye](https://www.neubird.ai/)
- [awesome-ai-sre](https://github.com/agamm/awesome-ai-sre)
