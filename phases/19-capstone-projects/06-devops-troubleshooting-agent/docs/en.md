# Capstone 06 — DevOps Troubleshooting Agent for Kubernetes | 故障排除 Kubernetes 结业 DevOps

> AWS's DevOps Agent went GA, Resolve AI published its K8s playbooks, NeuBird demoed semantic monitoring, and Metoro tied AI SRE to per-service SLOs. The production shape is settled: an alert webhook fires, an agent reads telemetry, walks a graph of K8s objects, ranks root-cause hypotheses, and posts a Slack brief with approval buttons. Read-only by default. Every remediation gated by a human. This capstone is that agent, evaluated on 20 synthetic incidents and compared against AWS's Agent on three shared cases.

> **【中文解读】** 本节是综合项目——构建 DevOps 故障排除 Agent，自动诊断和修复基础设施问题。


**Type:** Capstone
**Languages:** Python (agent), TypeScript (Slack integration)
**Prerequisites:** Phase 11 (LLM engineering), Phase 13 (tools and MCP), Phase 14 (agents), Phase 15 (autonomous), Phase 17 (infrastructure), Phase 18 (safety)
**Phases exercised:** P11 · P13 · P14 · P15 · P17 · P18
**Time:** 30 hours

## Problem

> **【中文解读】** 本节阐述 DevOps 故障排除 Agent 的核心问题。2025-2026 年 SRE 领域的共识是"AI Agent 做初步诊断，人类审批修复操作"。Agent 读取 Prometheus 指标、Loki 日志、Tempo 追踪和 kube-state-metrics，在 5 分钟内生成带遥测引用的根因假设。关键难点不在推理能力，而在安全边界设计：默认只读 RBAC、审计日志记录每个被考虑但未执行的命令、成本控制避免级联故障产生 $5000 的 Agent 账单。

> **【拓展：AIOps 产业现状】** 2026 年 AIOps 主要玩家：AWS DevOps Agent（GA 发布）、Resolve AI（K8s 故障排除专用）、NeuBird（语义监控）、Metoro（SLO-first AI SRE）、PagerDuty AIOps。共同架构是告警 webhook 触发 → Agent 读取遥测 → 排名根因假设 → Slack 简报 + 审批按钮。MTTR（平均修复时间）从人工的 45-90 分钟缩短到 Agent 辅助的 10-15 分钟。安全设计上，所有破坏性操作都需要 Slack 人工审批。

The 2025-2026 SRE narrative became: "AI agents triage incidents, humans approve remediations." AWS DevOps Agent, Resolve AI, NeuBird, Metoro, PagerDuty AIOps all ship this shape in production. The agent reads Prometheus metrics, Loki logs, Tempo traces, kube-state-metrics, and a knowledge graph of K8s objects. It produces a ranked root-cause hypothesis with telemetry citations in under five minutes. It never executes destructive commands without explicit human approval through Slack.

Most of the hard work is scoping and safety, not reasoning. The agent needs a read-only-by-default RBAC surface, a hardened MCP tool server, and audit logs of every command considered vs executed. It needs to know when it is outside its depth and escalate. And it has to run cheap enough that OOM-kill cascades do not generate a $5k agent bill.

## Concept

> **【中文解读】** Agent 操作基于 K8s 知识图谱：节点是 Pod、Deployment、Service 等对象，边编码所有权（Pod→ReplicaSet→Deployment）、调度关系（Pod→Node）和观测关系（Pod→Prometheus 指标）。告警触发时，Agent 从受影响对象出发遍历图谱，拉取相关遥测切片（最近 15 分钟），生成按证据权重排序的根因假设。修复操作默认只读，破坏性操作需 Slack 人工审批。

> **【拓展：知识图谱在 SRE 中的应用】** Neo4j 和 kuzu（嵌入式图数据库）是主流选择。kube-state-metrics 每 30 秒同步一次集群状态到图数据库。根因假设评分公式：recency x specificity x graph-path-length-inverse x citation-count。实测数据显示，top-3 假设的准确率可达 80%+（20 个合成故障场景），p50 诊断时间 < 5 分钟。审计日志采用只追加 JSONL 格式，记录每个被考虑和被执行的命令。

The agent operates on a knowledge graph. Nodes are K8s objects (Pods, Deployments, Services, Nodes, HPAs, PVCs) plus telemetry sources (Prometheus series, Loki streams, Tempo traces). Edges encode ownership (Pod -> ReplicaSet -> Deployment), scheduling (Pod -> Node), and observation (Pod -> Prometheus series). The graph is kept fresh by a kube-state-metrics sync and re-sampled on every alert.

When an alert fires, the agent root-causes from the affected object. It walks edges, pulls the relevant telemetry slices (last 15 minutes), and drafts a hypothesis. The hypothesis is ranked by evidence: how many telemetry citations support it, how recent, how specific. The top-3 hypotheses go to Slack with graph-path visualizations and approval buttons for remediation actions.

Remediation is gated. Allowed default actions are read-only. Destructive actions (scaling down, rolling back, deleting Pods) require Slack approval; ArgoCD rollback hooks require an auth token the agent never holds. The audit log records every command the agent *considered* — not just executed — so the review process catches near-misses.

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

## Stack

- Observability sources: Prometheus, Loki, Tempo, kube-state-metrics
- Knowledge graph: Neo4j (managed) or kuzu (embedded) of K8s objects + telemetry edges
- Agent: LangGraph with per-tool allow-list, read-only by default
- Tool transport: FastMCP over StreamableHTTP; separate server for destructive tools behind approval gate
- Models: Claude Sonnet 4.7 for root-cause reasoning, Gemini 2.5 Flash for log summarization
- Remediation: ArgoCD rollback webhook, PagerDuty escalate, Slack approval card
- Audit: append-only structured log (considered, executed, approved, outcome)
- Deployment: K8s deployment with its own narrow RBAC role; separate namespace

## Build It | 动手构建

1. **Graph ingestion.** Sync kube-state-metrics into Neo4j/kuzu every 30s. Nodes: Pod, Deployment, Node, Service, PVC, HPA. Edges: OWNED_BY, SCHEDULED_ON, EXPOSES, MOUNTS, SCALES. Telemetry overlay edges: OBSERVED_BY (a Pod is observed by a Prometheus series).

2. **Alert receiver.** FastAPI endpoint that accepts PagerDuty or Alertmanager webhooks. Extract the affected object(s) and SLO breach.

3. **Read-only tool surface.** Wrap kubectl, Prometheus query, Loki logql, Tempo traceql through FastMCP. Every tool has a narrow RBAC verb ("get", "list", "describe"). No "delete", "exec", "scale" in the default server.

4. **Root-cause agent.** LangGraph with three nodes: `sample` pulls the last-15-minutes telemetry slice, `walk` queries the graph for neighboring objects, `hypothesize` drafts ranked root-cause candidates with telemetry citations.

5. **Evidence scoring.** Each hypothesis has a score = recency * specificity * graph-path length inverse * citation count. Return top-3.

6. **Slack brief.** Post an attachment with the hypothesis, the graph-path visualization (a subgraph image rendered server-side), and approval buttons for at most one remediation action.

7. **Remediation gate.** Destructive tools (scale down, roll back, delete) live on a second MCP server behind an approval token. The agent can call them only after the Slack card is approved by a human.

8. **Audit log.** Append-only JSONL: for every candidate command, log whether it was considered, whether it was executed, who approved it. Ship to S3 daily.

9. **Synthetic incident suite.** Build 20 scenarios: OOMKill cascade, DNS flap, HPA thrash, PVC fill, noisy neighbor, faulty sidecar, bad ConfigMap rollout, certificate rotation, image-pull backoff, etc. Score the agent on root-cause accuracy and time-to-hypothesis.

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

`outputs/skill-devops-agent.md` is the deliverable. Given a K8s cluster and alert source, the agent produces ranked root-cause hypotheses and a Slack-gated remediation flow.

| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | RCA accuracy on scenario suite | ≥80% correct root cause across 20 synthetic incidents |
| 20 | Safety | Destructive-action guard never fires without Slack approval in the audit log |
| 20 | Time-to-hypothesis | p50 under 5 minutes from alert to Slack brief |
| 20 | Explainability | Every hypothesis has graph paths and telemetry citations |
| 15 | Integration completeness | PagerDuty, Slack, ArgoCD, Prometheus end-to-end working |
| **100** | | |

## Exercises | 练习题

1. Run your agent on the same three incidents AWS's DevOps Agent is demo'd on. Publish the side-by-side. Report where the agent diverges.

2. Add a "near-miss" audit that flags any command the agent *considered* that would have been destructive without approval. Measure the near-miss rate over one week.

3. Swap the hypothesis model from Claude Sonnet 4.7 to a self-hosted Llama 3.3 70B. Measure RCA accuracy delta and dollar per incident.

4. Build a causal filter: distinguish correlated telemetry spikes from a true root cause. Train a small classifier on the 20-scenario labels.

5. Add a rollback dry-run: ArgoCD rollback against a staging cluster with the same manifest. Verify the rollback plan in a live cluster before the Slack approval button.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| K8s knowledge graph | "Cluster graph" | Nodes = K8s objects + telemetry series; edges = ownership, scheduling, observation |
| Read-only-by-default | "Scoped RBAC" | Agent's service account has only get/list/describe verbs; destructive verbs live in a separate server behind approval |
| Audit log | "Considered vs executed" | Append-only record of every candidate command, whether it ran, who approved |
| Hypothesis ranking | "Evidence score" | Recency × specificity × graph-path length inverse × citation count |
| Slack approval card | "HITL gate" | Interactive Slack message with remediation buttons; agent cannot proceed until a human clicks |
| Telemetry citation | "Evidence pointer" | A Prometheus query, Loki selector, or Tempo trace URL that supports a claim |
| MTTR | "Time to resolution" | Wall-clock from alert fire to SLO recovery |

## Further Reading | 延伸阅读

- [AWS DevOps Agent GA](https://aws.amazon.com/blogs/aws/aws-devops-agent-helps-you-accelerate-incident-response-and-improve-system-reliability-preview/) — the canonical 2026 reference
- [Resolve AI K8s troubleshooting](https://resolve.ai/blog/kubernetes-troubleshooting-in-resolve-ai) — the competitor reference
- [NeuBird semantic monitoring](https://www.neubird.ai) — semantic-graph approach
- [Metoro AI SRE](https://metoro.io) — SLO-first production framing
- [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics) — the cluster-state source
- [LangGraph](https://langchain-ai.github.io/langgraph/) — reference agent orchestrator
- [FastMCP](https://github.com/jlowin/fastmcp) — Python MCP server framework
- [ArgoCD rollback](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_rollback/) — the gated remediation target
