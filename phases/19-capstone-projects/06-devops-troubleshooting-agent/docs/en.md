# Capstone 06 — DevOps Troubleshooting Agent for Kubernetes | 故障排除 Kubernetes 结业 DevOps

> AWS's DevOps Agent went GA, Resolve AI published its K8s playbooks, NeuBird demoed semantic monitoring, and Metoro tied AI SRE to per-service SLOs. The production shape is settled: an alert webhook fires, an agent reads telemetry, walks a graph of K8s objects, ranks root-cause hypotheses, and posts a Slack brief with approval buttons. Read-only by default. Every remediation gated by a human. This capstone is that agent, evaluated on 20 synthetic incidents and compared against AWS's Agent on three shared cases.

> **【中文解读】** 本节是综合项目——构建 DevOps 故障排除 Agent，自动诊断和修复基础设施问题。


**Type:** Capstone | **类型:** 综合项目
**Languages:** Python (agent), TypeScript (Slack integration) | **语言:** Python（Agent）, TypeScript（Slack 集成）
**Prerequisites:** Phase 11 (LLM engineering), Phase 13 (tools and MCP), Phase 14 (agents), Phase 15 (autonomous), Phase 17 (infrastructure), Phase 18 (safety) | **前置知识:** Phase 11（LLM 工程）, Phase 13（工具与 MCP）, Phase 14（Agent）, Phase 15（自主系统）, Phase 17（基础设施）, Phase 18（安全）
**Phases exercised:** P11 · P13 · P14 · P15 · P17 · P18 | **涉及阶段:** P11 · P13 · P14 · P15 · P17 · P18
**Time:** 30 hours | **时间:** 30 小时

## Problem | 问题引入

> **【中文解读】** 本节阐述 DevOps 故障排除 Agent 的核心问题。2025-2026 年 SRE 领域的共识是"AI Agent 做初步诊断，人类审批修复操作"。Agent 读取 Prometheus 指标、Loki 日志、Tempo 追踪和 kube-state-metrics，在 5 分钟内生成带遥测引用的根因假设。关键难点不在推理能力，而在安全边界设计：默认只读 RBAC、审计日志记录每个被考虑但未执行的命令、成本控制避免级联故障产生 $5000 的 Agent 账单。

> **【拓展：AIOps 产业现状】** 2026 年 AIOps 主要玩家：AWS DevOps Agent（GA 发布）、Resolve AI（K8s 故障排除专用）、NeuBird（语义监控）、Metoro（SLO-first AI SRE）、PagerDuty AIOps。共同架构是告警 webhook 触发 → Agent 读取遥测 → 排名根因假设 → Slack 简报 + 审批按钮。MTTR（平均修复时间）从人工的 45-90 分钟缩短到 Agent 辅助的 10-15 分钟。安全设计上，所有破坏性操作都需要 Slack 人工审批。

The 2025-2026 SRE narrative became: "AI agents triage incidents, humans approve remediations." AWS DevOps Agent, Resolve AI, NeuBird, Metoro, PagerDuty AIOps all ship this shape in production. The agent reads Prometheus metrics, Loki logs, Tempo traces, kube-state-metrics, and a knowledge graph of K8s objects. It produces a ranked root-cause hypothesis with telemetry citations in under five minutes. It never executes destructive commands without explicit human approval through Slack.

> 2025-2026 年的 SRE 叙事变成了："AI Agent 分诊事故，人类审批修复。"AWS DevOps Agent、Resolve AI、NeuBird、Metoro、PagerDuty AIOps 都在生产环境中提供这种形态。Agent 读取 Prometheus 指标、Loki 日志、Tempo 追踪、kube-state-metrics 和 K8s 对象知识图谱。它在五分钟内生成带遥测引用的排序根因假设。它从不在没有通过 Slack 获得明确人工审批的情况下执行破坏性命令。

Most of the hard work is scoping and safety, not reasoning. The agent needs a read-only-by-default RBAC surface, a hardened MCP tool server, and audit logs of every command considered vs executed. It needs to know when it is outside its depth and escalate. And it has to run cheap enough that OOM-kill cascades do not generate a $5k agent bill.

> 大部分困难工作在于范围界定和安全，而非推理。Agent 需要默认只读的 RBAC 表面、加固的 MCP 工具服务器，以及每个被考虑与执行的命令的审计日志。它需要知道何时超出能力范围并升级。而且运行成本必须足够低，以免 OOM-kill 级联产生 $5000 的 Agent 账单。

## Concept | 核心概念

> **【中文解读】** Agent 操作基于 K8s 知识图谱：节点是 Pod、Deployment、Service 等对象，边编码所有权（Pod→ReplicaSet→Deployment）、调度关系（Pod→Node）和观测关系（Pod→Prometheus 指标）。告警触发时，Agent 从受影响对象出发遍历图谱，拉取相关遥测切片（最近 15 分钟），生成按证据权重排序的根因假设。修复操作默认只读，破坏性操作需 Slack 人工审批。

> **【拓展：知识图谱在 SRE 中的应用】** Neo4j 和 kuzu（嵌入式图数据库）是主流选择。kube-state-metrics 每 30 秒同步一次集群状态到图数据库。根因假设评分公式：recency x specificity x graph-path-length-inverse x citation-count。实测数据显示，top-3 假设的准确率可达 80%+（20 个合成故障场景），p50 诊断时间 < 5 分钟。审计日志采用只追加 JSONL 格式，记录每个被考虑和被执行的命令。

The agent operates on a knowledge graph. Nodes are K8s objects (Pods, Deployments, Services, Nodes, HPAs, PVCs) plus telemetry sources (Prometheus series, Loki streams, Tempo traces). Edges encode ownership (Pod -> ReplicaSet -> Deployment), scheduling (Pod -> Node), and observation (Pod -> Prometheus series). The graph is kept fresh by a kube-state-metrics sync and re-sampled on every alert.

> Agent 在知识图谱上操作。节点是 K8s 对象（Pod、Deployment、Service、Node、HPA、PVC）加遥测源（Prometheus 序列、Loki 流、Tempo 追踪）。边编码所有权（Pod -> ReplicaSet -> Deployment）、调度（Pod -> Node）和观测（Pod -> Prometheus 序列）。图通过 kube-state-metrics 同步保持新鲜，并在每次告警时重新采样。

When an alert fires, the agent root-causes from the affected object. It walks edges, pulls the relevant telemetry slices (last 15 minutes), and drafts a hypothesis. The hypothesis is ranked by evidence: how many telemetry citations support it, how recent, how specific. The top-3 hypotheses go to Slack with graph-path visualizations and approval buttons for remediation actions.

> 当告警触发时，Agent 从受影响对象进行根因分析。它遍历边，拉取相关遥测切片（最近 15 分钟），并起草假设。假设按证据排序：有多少遥测引用支持它、多近、多具体。top-3 假设发送到 Slack，附带图路径可视化和修复操作的审批按钮。

Remediation is gated. Allowed default actions are read-only. Destructive actions (scaling down, rolling back, deleting Pods) require Slack approval; ArgoCD rollback hooks require an auth token the agent never holds. The audit log records every command the agent *considered* — not just executed — so the review process catches near-misses.

> 修复是受限的。默认允许的操作是只读的。破坏性操作（缩减、回滚、删除 Pod）需要 Slack 审批；ArgoCD 回滚 hook 需要一个 Agent 永远不持有的认证 token。审计日志记录 Agent *考虑*的每个命令——不仅仅是执行的——以便审查过程捕获差一点就发生的情况。

## Architecture | 架构

```
PagerDuty / Alertmanager webhook
           |
           v
     FastAPI receiver
           |
           v
   LangGraph root-cause agent
           |
           +---- read-only MCP tools ----+
           |                             |
           v                             v
   K8s knowledge graph              telemetry slices
     (Neo4j / kuzu)              Prometheus, Loki, Tempo
   ownership + scheduling          last 15m, scoped
           |
           v
   hypothesis ranking (evidence weight)
           |
           v
   Slack brief + approval buttons
           |
           v (approved)
   ArgoCD rollback hook / PagerDuty escalate
           |
           v
   audit log: considered vs executed, every command
```

## Stack | 技术栈

- Observability sources: Prometheus, Loki, Tempo, kube-state-metrics
  中文翻译：Observability sources: Prometheus, Loki, Tempo, kube-state-metrics
- Knowledge graph: Neo4j (managed) or kuzu (embedded) of K8s objects + telemetry edges
  中文翻译：Knowledge graph: Neo4j (managed) or kuzu (embedded) of K8s objects + telemetry edges
- Agent: LangGraph with per-tool allow-list, read-only by default
  中文翻译：Agent: LangGraph with per-tool allow-list, read-only by default
- Tool transport: FastMCP over StreamableHTTP; separate server for destructive tools behind approval gate
  中文翻译：Tool transport: FastMCP over StreamableHTTP; separate server for destructive tools behind approval gate
- Models: Claude Sonnet 4.7 for root-cause reasoning, Gemini 2.5 Flash for log summarization
  中文翻译：Models: Claude Sonnet 4.7 for root-cause reasoning, Gemini 2.5 Flash for log summarization
- Remediation: ArgoCD rollback webhook, PagerDuty escalate, Slack approval card
  中文翻译：Remediation: ArgoCD rollback webhook, PagerDuty escalate, Slack approval card
- Audit: append-only structured log (considered, executed, approved, outcome)
  中文翻译：Audit: append-only structured log (considered, executed, approved, outcome)
- Deployment: K8s deployment with its own narrow RBAC role; separate namespace
  中文翻译：Deployment: K8s deployment with its own narrow RBAC role; separate namespace

## Build It | 动手构建

> **【中文解读】** 构建 9 个阶段：图数据库摄入、告警接收器、只读工具面、根因 Agent、证据评分、Slack 简报、修复门控、审计日志和合成故障场景集。关键设计决策：破坏性工具（scale down、rollback、delete）放在独立的 MCP 服务器后，需要审批 token 才能调用——Agent 永远不持有该 token。

> **【拓展：合成故障场景在 SRE 训练中的价值】** 本课的 20 个合成故障场景（OOMKill 级联、DNS 抖动、HPA 震荡、PVC 填满、吵闹邻居等）是 SRE Agent 的"单元测试"。Google 的 SRE 书籍强调"Game Day"演练的重要性——在受控环境中模拟故障以验证响应流程。本课的合成场景集是自动化的 Game Day，使 Agent 的诊断能力可以量化评估。

1. **Graph ingestion.** Sync kube-state-metrics into Neo4j/kuzu every 30s. Nodes: Pod, Deployment, Node, Service, PVC, HPA. Edges: OWNED_BY, SCHEDULED_ON, EXPOSES, MOUNTS, SCALES. Telemetry overlay edges: OBSERVED_BY (a Pod is observed by a Prometheus series).
   中文翻译：1. **Graph ingestion.** Sync kube-state-metrics into Neo4j/kuzu every 30s. Nodes: Pod, Deployment, Node, Service, PVC, HPA. Edges: OWNED_BY, SCHEDULED_ON, EXPOSES, MOUNTS, SCALES. Telemetry overlay edges: OBSERVED_BY (a Pod is observed by a Prometheus series).

2. **Alert receiver.** FastAPI endpoint that accepts PagerDuty or Alertmanager webhooks. Extract the affected object(s) and SLO breach.
   中文翻译：2. **Alert receiver.** FastAPI endpoint that accepts PagerDuty or Alertmanager webhooks. Extract the affected object(s) and SLO breach.

3. **Read-only tool surface.** Wrap kubectl, Prometheus query, Loki logql, Tempo traceql through FastMCP. Every tool has a narrow RBAC verb ("get", "list", "describe"). No "delete", "exec", "scale" in the default server.
   中文翻译：3. **Read-only tool surface.** Wrap kubectl, Prometheus query, Loki logql, Tempo traceql through FastMCP. Every tool has a narrow RBAC verb ("get", "list", "describe"). No "delete", "exec", "scale" in the default server.

4. **Root-cause agent.** LangGraph with three nodes: `sample` pulls the last-15-minutes telemetry slice, `walk` queries the graph for neighboring objects, `hypothesize` drafts ranked root-cause candidates with telemetry citations.
   中文翻译：4. **Root-cause agent.** LangGraph with three nodes: `sample` pulls the last-15-minutes telemetry slice, `walk` queries the graph for neighboring objects, `hypothesize` drafts ranked root-cause candidates with telemetry citations.

5. **Evidence scoring.** Each hypothesis has a score = recency * specificity * graph-path length inverse * citation count. Return top-3.
   中文翻译：5. **Evidence scoring.** Each hypothesis has a score = recency * specificity * graph-path length inverse * citation count. Return top-3.

6. **Slack brief.** Post an attachment with the hypothesis, the graph-path visualization (a subgraph image rendered server-side), and approval buttons for at most one remediation action.
   中文翻译：6. **Slack brief.** Post an attachment with the hypothesis, the graph-path visualization (a subgraph image rendered server-side), and approval buttons for at most one remediation action.

7. **Remediation gate.** Destructive tools (scale down, roll back, delete) live on a second MCP server behind an approval token. The agent can call them only after the Slack card is approved by a human.
   中文翻译：7. **Remediation gate.** Destructive tools (scale down, roll back, delete) live on a second MCP server behind an approval token. The agent can call them only after the Slack card is approved by a human.

8. **Audit log.** Append-only JSONL: for every candidate command, log whether it was considered, whether it was executed, who approved it. Ship to S3 daily.
   中文翻译：8. **Audit log.** Append-only JSONL: for every candidate command, log whether it was considered, whether it was executed, who approved it. Ship to S3 daily.

9. **Synthetic incident suite.** Build 20 scenarios: OOMKill cascade, DNS flap, HPA thrash, PVC fill, noisy neighbor, faulty sidecar, bad ConfigMap rollout, certificate rotation, image-pull backoff, etc. Score the agent on root-cause accuracy and time-to-hypothesis.
   中文翻译：9. **Synthetic incident suite.** Build 20 scenarios: OOMKill cascade, DNS flap, HPA thrash, PVC fill, noisy neighbor, faulty sidecar, bad ConfigMap rollout, certificate rotation, image-pull backoff, etc. Score the agent on root-cause accuracy and time-to-hypothesis.

## Use It | 使用方法

```
webhook: alert.pagerduty.com -> checkout-api SLO breach, error rate 14%
[graph]   affected: Deployment checkout-api (3 Pods, Node ip-10-2-3-4)
[walk]    neighbors: ReplicaSet checkout-api-abc, Service checkout-api,
          recent rollout 14m ago
[sample]  prometheus error_rate 14%, up-trend; loki 500s on /api/v2/pay
[hypo]    #1 bad rollout: latest image checkout-api:v2.41 fails /healthz
          citations: deploy.yaml (rev 42), prometheus errorRate, loki 500 stack
[slack]   [ROLL BACK to v2.40]  [ESCALATE]  [IGNORE]
          (approval required; agent does not roll back unilaterally)
```

## Ship It | 部署上线

> **【中文解读】** 交付物是一个完整的 DevOps 故障排除 Agent，评估维度包括：RCA 准确率（20 个合成场景 >= 80%）、安全性（破坏性操作必须有 Slack 审批）、诊断速度（p50 < 5 分钟）、可解释性（每个假设有图路径和遥测引用）和集成完整性。

`outputs/skill-devops-agent.md` is the deliverable. Given a K8s cluster and alert source, the agent produces ranked root-cause hypotheses and a Slack-gated remediation flow.

> `outputs/skill-devops-agent.md` 是交付物。给定 K8s 集群和告警源，Agent 生成排序的根因假设和 Slack 受控的修复流程。

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | RCA accuracy on scenario suite | ≥80% correct root cause across 20 synthetic incidents |
| 25 | 场景套件上的 RCA 准确率 | 20 个合成事故中 ≥80% 正确根因 |
| 20 | Safety | Destructive-action guard never fires without Slack approval in the audit log |
| 20 | 安全性 | 破坏性操作守卫从未在审计日志中缺少 Slack 审批就触发 |
| 20 | Time-to-hypothesis | p50 under 5 minutes from alert to Slack brief |
| 20 | 假设时间 | 从告警到 Slack 简报的 p50 低于 5 分钟 |
| 20 | Explainability | Every hypothesis has graph paths and telemetry citations |
| 20 | 可解释性 | 每个假设有图路径和遥测引用 |
| 15 | Integration completeness | PagerDuty, Slack, ArgoCD, Prometheus end-to-end working |
| 15 | 集成完整性 | PagerDuty、Slack、ArgoCD、Prometheus 端到端工作 |
| **100** | | |

## Exercises | 练习题

1. Run your agent on the same three incidents AWS's DevOps Agent is demo'd on. Publish the side-by-side. Report where the agent diverges.
   中文翻译：在同一三个事故上运行你的 Agent，与 AWS DevOps Agent 的演示对比。发布并排比较。报告 Agent 分歧之处。

> 中文翻译：在同一三个事故上运行你的 Agent，与 AWS DevOps Agent 的演示对比。发布并排比较。报告 Agent 分歧之处。（翻译）


2. Add a "near-miss" audit that flags any command the agent *considered* that would have been destructive without approval. Measure the near-miss rate over one week.
   中文翻译：添加"差一点"审计，标记 Agent *考虑*但没有审批就会是破坏性的任何命令。测量一周内的差一点率。

3. Swap the hypothesis model from Claude Sonnet 4.7 to a self-hosted Llama 3.3 70B. Measure RCA accuracy delta and dollar per incident.
   中文翻译：将假设模型从 Claude Sonnet 4.7 换为自托管的 Llama 3.3 70B。测量 RCA 准确率差异和每事故美元成本。

> 中文翻译：将假设模型从 Claude Sonnet 4.7 换为自托管的 Llama 3.3 70B。测量 RCA 准确率差异和每事故美元成本。（翻译）


4. Build a causal filter: distinguish correlated telemetry spikes from a true root cause. Train a small classifier on the 20-scenario labels.
   中文翻译：构建因果过滤器：区分相关的遥测尖峰和真正的根因。在 20 个场景标签上训练一个小分类器。

5. Add a rollback dry-run: ArgoCD rollback against a staging cluster with the same manifest. Verify the rollback plan in a live cluster before the Slack approval button.
   中文翻译：添加回滚干跑：用相同清单对 staging 集群进行 ArgoCD 回滚。在 Slack 审批按钮前验证活集群中的回滚计划。

> 中文翻译：添加回滚干跑：用相同清单对 staging 集群进行 ArgoCD 回滚。在 Slack 审批按钮前验证活集群中的回滚计划。（翻译）


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| K8s knowledge graph | "Cluster graph" | Nodes = K8s objects + telemetry series; edges = ownership, scheduling, observation |
| K8s 知识图谱 | "集群图" | 节点 = K8s 对象 + 遥测序列；边 = 所有权、调度、观测 |
| Read-only-by-default | "Scoped RBAC" | Agent's service account has only get/list/describe verbs; destructive verbs live in a separate server behind approval |
| 默认只读 | "限定 RBAC" | Agent 的服务账号只有 get/list/describe 动词；破坏性动词在审批后的独立服务器中 |
| Audit log | "Considered vs executed" | Append-only record of every candidate command, whether it ran, who approved |
| 审计日志 | "考虑 vs 执行" | 每个候选命令的只追加记录，是否运行，谁审批 |
| Hypothesis ranking | "Evidence score" | Recency × specificity × graph-path length inverse × citation count |
| 假设排序 | "证据分数" | 近因 × 特异性 × 图路径长度倒数 × 引用数 |
| Slack approval card | "HITL gate" | Interactive Slack message with remediation buttons; agent cannot proceed until a human clicks |
| Slack 审批卡片 | "人机交互门" | 带修复按钮的交互式 Slack 消息；Agent 直到人类点击才能继续 |
| Telemetry citation | "Evidence pointer" | A Prometheus query, Loki selector, or Tempo trace URL that supports a claim |
| 遥测引用 | "证据指针" | 支持声明的 Prometheus 查询、Loki 选择器或 Tempo 追踪 URL |
| MTTR | "Time to resolution" | Wall-clock from alert fire to SLO recovery |
| MTTR | "解决时间" | 从告警触发到 SLO 恢复的挂钟时间 |

## Further Reading | 延伸阅读

- [AWS DevOps Agent GA](https://aws.amazon.com/blogs/aws/aws-devops-agent-helps-you-accelerate-incident-response-and-improve-system-reliability-preview/) — the canonical 2026 reference
  中文翻译：2026 年规范的参考
- [Resolve AI K8s troubleshooting](https://resolve.ai/blog/kubernetes-troubleshooting-in-resolve-ai) — the competitor reference
  中文翻译：竞争对手参考
- [NeuBird semantic monitoring](https://www.neubird.ai) — semantic-graph approach
  中文翻译：语义图方法
- [Metoro AI SRE](https://metoro.io) — SLO-first production framing
  中文翻译：SLO 优先的生产框架
- [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics) — the cluster-state source
  中文翻译：集群状态源
- [LangGraph](https://langchain-ai.github.io/langgraph/) — reference agent orchestrator
  中文翻译：参考 Agent 编排器
- [FastMCP](https://github.com/jlowin/fastmcp) — Python MCP server framework
  中文翻译：Python MCP 服务器框架
- [ArgoCD rollback](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_rollback/) — the gated remediation target
  中文翻译：受限修复目标
