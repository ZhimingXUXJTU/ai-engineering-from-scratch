# Shadow Traffic, Canary Rollout, and Progressive Deployment for LLMs | 渐进式 影子 金丝雀 LLM

> LLM rollouts combine the hardest parts of software deployment: no unit tests, diffuse failure modes, delayed signals. The sequence is (1) shadow mode — duplicate prod requests to candidate model, log, compare with zero user impact; catches obvious distribution issues but is not a quality guarantee; (2) canary rollout — progressive traffic shift 10% → 25% → 50% → 75% → 100% with gates at each step; track latency percentiles, cost/request, error/refusal rate, output length distribution, user-feedback rate; (3) A/B testing for distinct alternatives after stability confirmed. Non-determinism is irreducible — up to 15% accuracy variation across runs with identical inputs due to GPU FP non-associativity plus batch-size variance. Cost is a variable, not constant — a 20% better model can be 3x more expensive per call. Rollback speed is decisive: if rollback requires redeploy, you are too slow. Policy lives in config/flags; model lives in registry with pinned digests; rollback = flip policy + revert threshold + pin old model in seconds.

> **【中文解读】** 本节介绍了影子/金丝雀/渐进式部署——LLM 服务安全上线的部署策略。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy canary-progression simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing)

> 🔗 **【前置】** 学本节前请先掌握：Phase 17·13（可观测性）、Phase 17·21（A/B 测试）。LLM 上线 = 软件部署最难的组合：无单元测试、失败模式分散、信号延迟。
> 💡 **【类比】** LLM 部署三步 = "飞机首飞流程"。Shadow = 地面模拟（复制 prod 请求，零用户影响，对比但不切换）；Canary = 真飞但逐步开载客（10%→25%→50%→100%，每步有门禁）；A/B = 商业航班对比（稳定后测不同方案）。关键：非确定性不可消除（GPU 浮点+batch 差异致 15% 准确率波动）；成本是变量（好 20% 的模型可能贵 3 倍）；回滚速度决定性（必须秒级 flag 切换不能 redeploy）。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Learning Objectives | 学习目标

- Distinguish shadow mode (zero-impact compare), canary (live traffic progressive), and A/B (stability-confirmed comparison).
  中文翻译：区分影子模式（零影响比较）、金丝雀（真实流量渐进）和 A/B（统计比较）。
- Enumerate five LLM-specific canary metrics (latency, cost/request, error/refusal, output-length distribution, user feedback).
  中文翻译：列举五个 LLM 特定的金丝雀指标（延迟、成本/请求、错误/拒绝、输出长度分布、语义质量样本）。
- Explain why LLM non-determinism (up to 15%) changes what "stable" means in a rollout.
  中文翻译：解释为什么 LLM 非确定性（高达 15%）改变了推出中"稳定"的含义。
- Design a rollback path that takes seconds (policy flip) not hours (redeploy).
  中文翻译：设计一个秒级回滚路径（策略翻转），而非小时级（重新部署）。

## The Problem | 问题引入

> **【中文解读】** LLM 部署结合了软件部署中最难的部分：没有单元测试、模糊的失败模式、延迟的信号。正确的序列是：(1) 影子模式——将生产请求复制到候选模型，日志对比，零用户影响；(2) 金丝雀发布——10%→25%→50%→75%→100% 渐进流量切换，每个阶段有门控指标；(3) A/B 测试——稳定性确认后的对比。回滚速度是决定性的——策略标志翻转（30 秒）vs 重新部署（3 小时）。

> **【拓展：LLM 非确定性与部署】** LLM 的非确定性是不可约的——相同输入在相同模型上可能产生高达 15% 的准确率差异（原因：GPU FP 非结合性、batch size 差异、temperature > 0 的采样）。这意味着"稳定"在 LLM 部署中意味着"指标在预期方差内"，而非"与基线相同"。金丝雀门控阈值必须设置在噪声地板之上，否则会频繁误报。成本也是变量——一个好 20% 的模型可能贵 3x，成本/请求必须是五个门控指标之一。

You ship a new model. Offline evals show 3% accuracy gain. You flip it on in production. Within 24 hours, cost is up 40%, user thumbs-down is up 8%, three customer tickets report "weird answers." You roll back. Redeploy takes 3 hours. Your weekend is ruined.

Every piece of that was avoidable. Shadow mode would have caught the 40% cost spike before any user saw it. Canary would have stopped at 10% when thumbs-down moved. Policy-flag rollback would have taken 30 seconds. The discipline is what fills in the gap between "offline evals look good" and "real users are happy."

## The Concept | 核心概念

### Shadow mode

> **【中文解读】** 影子模式——候选模型接收与生产相同的请求，输出仅记录不返回给用户。日志内容包括：输出内容（与生产 diff）、token 数量（成本差异）、延迟、拒绝和错误。能捕获：成本爆炸、长度退化、明显的拒绝变化、硬错误。不能捕获：用户会感知到的质量差异——影子是烟雾测试，不是质量测试。

Candidate receives the same requests as production; outputs are logged, not returned to users. Zero user impact. Log:

- Output content (diff against production).
- Token counts (cost delta).
- Latency.
- Refusal and error.

Catches: cost blow-ups, length regressions, obvious refusal changes, hard errors. Does NOT catch: quality delta users would perceive. Shadow is a smoke test, not a quality test.

### Canary rollout

> **【拓展：LLM 金丝雀发布的五个门控指标】** LLM 金丝雀发布必须监控的五个门控指标：(1) 延迟百分位（P50/P95/P99）——canary P99 > 1.5x 基线则触发；(2) 每请求成本——>20% 高于基线则触发；(3) 错误/拒绝率——2x 基线则触发；(4) 输出长度分布——均值 + P99 分布偏移则触发；(5) 用户反馈率——thumbs-down/工单 1.5x 基线则触发。典型进度 1%→10%→25%→50%→75%→100%，每个阶段累积足够样本（5-15 分钟检查间隔）。

Progressive traffic shift with gates. Typical progression: 1% → 10% → 25% → 50% → 75% → 100%. Gate on 5 metrics at each step:

1. **Latency percentiles** — P50, P95, P99. Breach: canary has P99 > 1.5x baseline.
2. **Cost per request** — blended $. Breach: >20% above baseline.
3. **Error / refusal rate** — 5xx plus explicit refusals. Breach: 2x baseline.
4. **Output length distribution** — mean + P99. Breach: distributional shift.
5. **User-feedback rate** — thumbs-down / ticket filings. Breach: 1.5x baseline.

### Non-determinism is the new variance

Identical inputs produce non-identical outputs. Reasons:

- GPU FP non-associativity (floating-point reduction order varies by batch).
- Batch-size variance (same prompt in a batch of 128 vs batch of 16).
- Sampling (temperature > 0).

Measured: up to 15% accuracy variation run-to-run on identical eval sets. "Stable" in a rollout means metrics are within expected variance, not identical to baseline. Set gates above the noise floor.

### Cost is a variable

A 20% better model can be 3x more expensive per call. Cost/request is one of the five gates. Shipping a "better" model that breaks unit economics is a rollback case.

### Rollback is the weapon

- Policy flag (feature flag system): flip percentage in config; takes seconds.
- Model pinning (registry digest): pinned model does not auto-upgrade.
- Rollback = revert flag + set pinned digest to previous. Seconds, not hours.

If your stack requires redeploy to rollback, fix that before rolling.

### Tooling

> **【拓展：LLM 渐进式部署工具链】** 2026 年 LLM 渐进式部署的工具选择：(1) Argo Rollouts / Flagger——Kubernetes 原生渐进式部署控制器，与 Istio/Linkerd 加权路由集成；(2) Istio weighted routing——服务网格级流量切分；(3) KServe / Seldon Core——模型服务自带 canary 功能；(4) Feature flags——LaunchDarkly、Flagsmith、Unleash，策略级翻转无需重新部署。回滚基础设施：策略标志（feature flag system）翻转百分比在配置中（秒级）+ 模型注册摘要固定（pinned digest 不自动升级）。如果你的堆栈需要重新部署来回滚，先修复这个再上线。

**Argo Rollouts** / **Flagger** — Kubernetes progressive delivery controllers. Integrate with Istio/Linkerd weighted routing.

**Istio weighted routing** — service-mesh-level traffic split.

**KServe / Seldon Core** — model serving with built-in canary.

**Feature flags** — LaunchDarkly, Flagsmith, Unleash. Policy-level flip, no redeploy.

### Metrics cadence

Canary gates check every 5-15 minutes depending on traffic volume. 1% traffic with 10 req/min gives 50-150 data points per window — enough for latency but noisy for user feedback. 10% gives ~10x more. Progressions should pause long enough to accumulate enough samples at each step.

### The A/B step is optional

If the new model is distinctly different (different behavior, different cost curve, different tone), A/B test it at 50% after canary passes. If it's just an improved version, skip to 100% when canary gates pass.

### Numbers you should remember

- Canary progression: 1% → 10% → 25% → 50% → 75% → 100%.
- Non-determinism ceiling: up to 15% run-to-run variance on identical inputs.
- Five canary metrics: latency, cost, error/refusal, output length, user feedback.
- Cost gate: >20% above baseline is a breach.
- Rollback: seconds, not hours.

## Use It | 用框架实现

`code/main.py` simulates a canary rollout with injected regressions. Reports which stage the rollout halts at and which gate triggered.

> `code/main.py` simulates a canary rollout with injected regressions. Reports which stage the rollout halts at and which gate triggered.

> `code/main.py` simulates a canary rollout with injected regressions. Reports which stage the rollout halts at and which gate triggered.

## Ship It | 产出物

This lesson produces `outputs/skill-rollout-runbook.md`. Given candidate model, baseline, and risk tolerance, designs shadow→canary→100% plan.

> 本课产出 `outputs/skill-rollout-runbook.md`. Given candidate model, baseline, and risk tolerance, designs shadow→canary→100% plan.

## Exercises | 练习题

1. Run `code/main.py`. Inject a 25% cost regression. At which stage does the canary halt?
   中文翻译：运行 `code/main.py`。注入 25% 成本回归。金丝雀在哪个阶段捕获它？
2. Your new model has 3% accuracy gain offline but cost/request is +18%. Is it a ship? Depends on the policy — write both paths.
   中文翻译：你的新模型离线精度提升 3% 但成本/请求 +18%。值得上线吗？取决于产品上下文。
3. Design a rollback that takes under 60 seconds end-to-end. List the required infrastructure.
   中文翻译：设计端到端 60 秒内的回滚。列出所需基础设施。
4. Non-determinism shows ±7% on your eval. Set canary gates so you don't false-alarm. What multipliers do you use?
   中文翻译：非确定性显示 +/-7%。设置金丝雀门控以避免误报。
5. Shadow mode catches a 40% cost spike before canary. Write the alert rule that fires in shadow.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Shadow mode | "duplicate to new" | Zero-impact send-to-candidate for logging |
| Canary | "progressive traffic" | Gradual user-exposed rollout with gates |
| Gates | "rollout checks" | Metric thresholds that block progression |
| Non-determinism | "LLM variance" | Irreducible run-to-run differences |
| Policy flag | "flag flip rollback" | Config-level rollback, seconds not hours |
| Model pin | "registry digest" | Immutable reference to a model version |
| Argo Rollouts | "K8s progressive" | Kubernetes-native canary/rollback controller |
| KServe | "inference K8s" | Model serving with canary primitives |
| Istio weighted | "mesh split" | Service-mesh traffic splitter |

## Further Reading | 延伸阅读

- [TianPan — Releasing AI Features Without Breaking Production](https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing)
- [MarkTechPost — Safely Deploying ML Models](https://www.marktechpost.com/2026/03/21/safely-deploying-ml-models-to-production-four-controlled-strategies-a-b-canary-interleaved-shadow-testing/)
- [APXML — Advanced LLM Deployment Patterns](https://apxml.com/courses/mlops-for-large-models-llmops/chapter-4-llm-deployment-serving-optimization/advanced-llm-deployment-patterns)
- [Argo Rollouts docs](https://argo-rollouts.readthedocs.io/)
- [Flagger docs](https://docs.flagger.app/)
