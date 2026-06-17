# Chaos Engineering for LLM Production | 工程 生产 混沌 LLM

> Chaos engineering for LLMs is its own discipline in 2026. Prerequisites before running experiments in production: defined SLI/SLO, trace+metric+log observability, automated rollback, runbooks, on-call. Architecture has four planes: control (experiment scheduler), target (services, infra, data stores), safety (guards + abort + traffic filters), observability (metrics + traces + logs), feedback (into SLO adjustments). Guardrails are mandatory: burn-rate alerts pause experiments if daily error-budget burn > 2x expected; suppression windows + trace-ID correlation dedupe alert noise. Cadence: weekly small canary + SLO review; monthly game day + postmortem; quarterly cross-team resilience audit + dependency mapping. LLM-specific experiments: memory overload, network failures, provider outages, malformed prompts, KV cache eviction storms. Tooling: Harness Chaos Engineering (LLM-derived recommendations, blast-radius downscaling, MCP tool integration); LitmusChaos (CNCF); Chaos Mesh (CNCF Kubernetes-native).

> **【中文解读】** 本节介绍了 LLM 混沌工程——主动注入故障来测试 LLM 服务韧性的实践。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy chaos experiment runner) | **语言:** Python
**Prerequisites:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability)

> 🔗 **【前置】** 学本节前请先掌握：Phase 17·23（SRE）、Phase 17·13（可观测性）、SRE 基础（SLI/SLO/错误预算）。LLM 混沌工程 = 主动注入故障测韧性。
> 💡 **【类比】** LLM 混沌工程 = "消防演习"。前提：SLI/SLO 定义好、可观测、自动回滚、runbook、on-call。四平面：控制（实验调度）+目标（服务/数据/基础设施）+安全（守卫/中止/流量过滤）+可观测。必须护栏：错误预算燃烧率 > 2x 时暂停实验。节奏：每周小 canary+月度 game day+季度跨团队审计。LLM 专属实验：内存过载、网络故障、provider 宕机、坏 prompt、KV cache 驱逐风暴。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Learning Objectives | 学习目标

- Name the five chaos engineering prerequisites (SLI/SLO, observability, rollback, runbooks, on-call) and explain why skipping any breaks the practice.
  中文翻译：说出五个混沌工程前置条件（SLI/SLO、可观测性、回滚、运行手册、待命文化）。
- Diagram the four planes (control, target, safety, observability) and the feedback loop into SLO.
  中文翻译：绘制四个平面（控制、目标、安全、可观测性）和反馈循环到 SLO 仪表板。
- Enumerate five LLM-specific experiments (memory overload, network fail, provider outage, malformed prompt, KV eviction storm).
  中文翻译：列举五个 LLM 特定的混沌实验（内存过载、网络故障、提供商宕机、畸形输入、缓存失效）。
- Pick a tool — Harness, LitmusChaos, Chaos Mesh — given stack.
  中文翻译：选择工具——Harness、LitmusChaos、Chaos Mesh——根据技术栈。

## The Problem | 问题引入

> **【中文解读】** LLM 混沌工程是 2026 年的独立学科。LLM 栈增加了新的故障模式：4K-token 的毒化字符使分词器卡住 12 秒；上游提供商 429 触发网关重试，重试放大并发导致 OOM；突发负载下 KV Cache 淘汰风暴引发 re-prefill 级联，耗尽计算资源。这些都不会出现在单元测试中——混沌工程是在用户之前发现它们的手段。

> **【拓展：LLM 混沌工程的五类实验】** 2026 年 LLM 特定的五类混沌实验：(1) 内存过载——发送长上下文高并发请求引发 KV Cache 抢占风暴，观察服务是优雅降级还是崩溃；(2) 网络故障——切断推理网关与提供商的连接，观察 failover 是否在 SLA 内生效；(3) 提供商中断模拟——100% OpenAI 429，观察路由是否 failover 到 Anthropic；(4) 畸形提示——注入分词器卡死的负载（深层嵌套 Unicode、巨大 UTF-8 码点），观察是否单个请求锁住 worker；(5) KV 淘汰风暴——饱和 vLLM 块预算强制淘汰，观察 LMCache 恢复还是服务降级。

Chaos testing in traditional stacks is established. LLM stacks add new failure modes. A 4K-token prompt with a poison character stalls the tokenizer for 12 seconds. An upstream provider 429s; your gateway retries; your service OOMs on retry-amplified concurrency. A KV cache eviction storm under burst load causes re-prefill cascades that saturate compute.

None of these show up in unit tests. Chaos engineering is how you discover them before users do.

## The Concept | 核心概念

### Prerequisites

> **【中文解读】** 在生产中运行混沌测试的五个前提：(1) SLI/SLO 已定义；(2) 可观测性（trace + metric + log）已部署；(3) 自动回滚机制就绪；(4) 结构化 runbook 已编写；(5) 有值班人员响应。缺少任何一项，混沌就会变成真实事件。四个平面：控制面（实验调度器）、目标面（服务/基础设施）、安全面（kill switch + 抑制窗口 + blast radius 限制）、可观测面（指标 + trace 关联）。反馈循环将发现回馈到 SLO 调整、runbook 更新和代码修复。

Don't run chaos in production without:

1. **SLI/SLO** — defined service-level indicators and objectives.
2. **Observability** — traces, metrics, logs, wired to dashboards.
3. **Automated rollback** — Phase 17 · 20 policy-flag rollback.
4. **Runbooks** — structured, Phase 17 · 23.
5. **On-call** — someone to respond.

Missing any means chaos becomes real incident.

### Four planes + feedback

**Control plane** — experiment scheduler (Litmus workflow, Chaos Mesh schedule, Harness UI).

**Target plane** — services, pods, nodes, load balancers, data stores.

**Safety plane** — kill switch, suppression windows, blast-radius limits, error-budget gates.

**Observability plane** — normal metrics + trace-ID correlation to distinguish chaos-induced from natural failures.

**Feedback loop** — findings feed back into SLO adjustment, runbook updates, code fixes.

### Guardrails are mandatory

> **【拓展：混沌工程的安全护栏】** 混沌工程的三个必要安全护栏：(1) 燃尽率告警——实验期间如果每日错误预算消耗超过预期的 2x，自动暂停实验；(2) 抑制窗口——在实验的爆炸半径内静默非实验告警，避免 on-call 噪音；(3) Trace-ID 关联——所有实验引起的错误携带标签，使 on-call 可以去重。这些护栏确保混沌实验不会变成真实事件——缺少任何一个都意味着混沌失控。

- **Burn-rate alert**: pause experiment if daily error-budget burn exceeds 2x expected.
- **Suppression windows**: silence non-experiment alerts in the blast radius during experiment.
- **Trace-ID correlation**: all experiment-induced errors carry a tag so on-call can dedupe.

### Five LLM-specific experiments

1. **Memory overload** — force a KV cache preemption storm by sending long-context requests with high concurrency. Observe: does the service gracefully shed or crash?

2. **Network failure** — cut connectivity between inference gateway and provider. Observe: does fallback kick in within SLA? (Phase 17 · 19)

3. **Provider outage simulation** — 100% 429 from OpenAI. Observe: does routing failover to Anthropic? (Phase 17 · 16, 19)

4. **Malformed prompt** — inject tokenizer-stalling payload (e.g., deeply nested unicode, huge UTF-8 codepoint). Observe: does a single request lock up a worker?

5. **KV eviction storm** — force eviction by saturating vLLM block budget. Observe: does LMCache recover or does service degrade?

### Cadence

- **Weekly** — small canary experiments in staging, maybe 5% prod.
- **Monthly** — scheduled game day on a specific scenario; cross-team attendance; postmortem.
- **Quarterly** — cross-team resilience audit; dependency map update.

### Tooling

> **【拓展：混沌工程工具选择】** 2026 年混沌工程工具选择：(1) Harness Chaos Engineering——商业，AI 驱动的实验推荐，blast radius 自动缩放，MCP 工具集成；(2) LitmusChaos——CNCF 毕业，Kubernetes 工作流式；(3) Chaos Mesh——CNCF 沙箱，Kubernetes-native CRD 风格；(4) Gremlin——商业，广泛支持；(5) AWS FIS / Azure Chaos Studio——托管云服务。节奏建议：每周小 canary 实验 + SLO 审查，每月 game day + postmortem，每季度跨团队韧性审计 + 依赖映射更新。

- **Harness Chaos Engineering** — commercial; AI-derived experiment recommendations; blast-radius downscaling; MCP tool integration.
- **LitmusChaos** — CNCF graduated; Kubernetes workflow-based.
- **Chaos Mesh** — CNCF sandbox; Kubernetes-native CRD style.
- **Gremlin** — commercial; broad support.
- **AWS FIS** / **Azure Chaos Studio** — managed cloud offerings.

### Starting small

First experiment: pod-kill one decode replica under steady traffic. Observe rerouting and recovery. If this works and looks safe, graduate to network chaos.

First LLM-specific experiment: inject one provider 429 for 5 minutes. Observe fallback. Most teams discover their fallback wasn't fully tested.

### Numbers you should remember

- Four planes: control, target, safety, observability.
- Burn-rate pause: 2x expected daily budget burn.
- Cadence: weekly canary, monthly game day, quarterly audit.
- Five LLM experiments: memory, network, provider, malformed prompt, KV storm.

## Use It | 用框架实现

`code/main.py` simulates three chaos experiments with safety plane gates. Reports which experiments would trip the burn-rate abort.

> `code/main.py` simulates three chaos experiments with safety plane gates. Reports which experiments would trip the burn-rate abort.

> `code/main.py` simulates three chaos experiments with safety plane gates. Reports which experiments would trip the burn-rate abort.

## Ship It | 产出物

This lesson produces `outputs/skill-chaos-plan.md`. Given stack and maturity, picks first three experiments and the tooling.

> 本课产出 `outputs/skill-chaos-plan.md`. Given stack and maturity, picks first three experiments and the tooling.

## Exercises | 练习题

1. Run `code/main.py`. Which experiment trips the burn-rate gate and why?
   中文翻译：运行 `code/main.py`。哪个实验触发了燃烧率门控？为什么？
2. Design the first five chaos experiments for a vLLM-based RAG service. Include success criteria.
   中文翻译：为基于 vLLM 的 RAG 服务设计前五个混沌实验。
3. Your burn-rate alert paused an experiment. How do you determine root cause — chaos or natural?
   中文翻译：你的燃烧率告警暂停了一个实验。如何确定根因 vs 预期行为？
4. Argue whether chaos should run in production or only staging. When is production the right answer?
   中文翻译：论证混沌实验应该在生产还是仅在预发布环境运行。何时生产环境是正确答案？
5. Name three LLM-specific failure modes that generic network-chaos cannot reproduce.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| SLI / SLO | "service targets" | Indicator + objective; required prerequisite |
| Blast radius | "scope" | Set of services / users affected by experiment |
| Burn-rate alert | "budget gate" | Fires when error-budget burn rate > 2x expected |
| Game day | "monthly drill" | Scheduled cross-team chaos exercise |
| LitmusChaos | "CNCF workflow" | Graduated CNCF Kubernetes chaos tool |
| Chaos Mesh | "CNCF CRD" | CNCF sandbox Kubernetes-native chaos |
| Harness CE | "commercial AI-assisted" | Harness chaos with AI recommendations |
| Malformed prompt | "tokenizer bomb" | Input that stalls tokenization |
| KV eviction storm | "preemption cascade" | Mass eviction triggering re-prefills |

## Further Reading | 延伸阅读

- [DevSecOps School — Chaos Engineering 2026 Guide](https://devsecopsschool.com/blog/chaos-engineering/)
- [Ankush Sharma — Observability for LLMs (book)](https://www.amazon.com/Observability-Large-Language-Models-Engineering-ebook/dp/B0DJSR65TR)
- [LitmusChaos (CNCF)](https://litmuschaos.io/)
- [Chaos Mesh (CNCF)](https://chaos-mesh.org/)
- [Harness Chaos Engineering](https://www.harness.io/products/chaos-engineering)
- [AWS FIS](https://aws.amazon.com/fis/)
