# Model Routing as a Cost-Reduction Primitive | 原始 路由 成本

> A dynamic broker evaluates every request (task type, token length, embedding similarity, confidence) and sends simple queries to a cheap model, escalating complex ones to a frontier model. Also called model cascading. Production case studies show 20-60% cost reduction at iso-quality across US/UK/EU deployments; a 30% routing efficiency improvement on high-volume SaaS turns into six-figure annual savings. The 2026 context is that LLM inference prices dropped ~10x per year — a GPT-4-class token went from $20/M to ~$0.40/M from late 2022 to 2026. Most of the drop is better serving stacks (Phase 17 · 04-09), not hardware. Routing is how you convert that price drop into margin without product regression. The failure mode is cheap-model drift: the route pushes 40% to a weaker model, quality drops 3-5% on reasoning tasks, no one notices for a quarter. Gate routes by online quality metrics, not just offline eval sets.

> **【中文解读】** 本节介绍了模型路由——根据任务复杂度动态选择不同模型的成本优化策略。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cascading router simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 19 (AI Gateways) | **前置知识:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 19 (AI Gateways)
**Time:** ~60 minutes | **时间:** ~60 minutes

## Learning Objectives | 学习目标

- Explain model cascading: cheap-first with confidence check, escalate on low confidence.
  中文翻译：解释模型级联：廉价优先加置信度检查，低置信度时升级。
- Enumerate the four routing signals (task classification, prompt length, embedding similarity to known-hard set, self-confidence from first-pass).
  中文翻译：列举四种路由信号（任务分类、提示长度、嵌入相似度、首次通过自置信度）。
- Compute expected blended cost at target routing split and quality loss tolerance.
  中文翻译：计算目标路由分流和质量损失容忍度下的预期混合成本。
- Name the drift-monitoring metric (online quality gate) that catches cheap-model creep.
  中文翻译：说出捕获廉价模型质量漂移的漂移监控指标（在线质量门控）。

## The Problem | 问题引入

> **【中文解读】** 模型路由的核心洞察：70% 的查询是简单的（"巴黎几点了？""改写这句话"），可以用 Haiku 级别的模型以 3% 的成本完美处理。只有 30% 需要 GPT-5 级别的推理能力。将 70% 路由到廉价模型，30% 路由到前沿模型，可以在相同产品质量下降低约 65% 的账单。关键挑战是构建路由器而不降低质量。

> **【拓展：模型路由的产业案例】** 2026 年模型路由在生产中的典型成果：20-60% 成本降低（同质量下）。LLM 推理价格从 2022 年到 2026 年下降了约 10x/年（GPT-4 级别从 $20/M 降到 $0.40/M），大部分下降来自推理栈优化（Phase 17·04-09）。模型路由让你在应用层捕获这些收益，而非等待所有用户迁移到廉价模型。开源路由器 RouteLLM（LMSYS）和商业方案 Not Diamond 都在快速迭代。

Your service costs $80k/month on GPT-5. Your analytics show 70% of queries are simple: "what time is it in Paris?" "rephrase this sentence." A Haiku-class model handles those perfectly at 3% of the cost. 30% need GPT-5's reasoning — coding, math, multi-step planning.

If you route the 70% to cheap and 30% to expensive, your bill drops ~65% at the same product quality. This is routing. The trick is building the broker without regressing quality.

## The Concept | 核心概念

### Four routing signals

> **【中文解读】** 四种路由信号：(1) 任务分类——简单/复杂/代码/数学/聊天，可用规则分类器或小 LLM（$0.25/M）；(2) 提示长度——>4K token 通常需要前沿模型，<500 通常不需要；(3) 嵌入相似度——与已知困难集的余弦相似度 >0.88 则直接升级；(4) 首次通过的自置信度——发送到廉价模型，如果 log-probs 显示低置信度或拒绝，重试到前沿模型。

1. **Task classification**: simple/complex/codegen/math/chat. Can be a rules-based classifier, a small LLM (Haiku-class at $0.25/M), or embedding similarity to labeled buckets. Output: route = cheap / balanced / frontier.

2. **Prompt length**: prompts >4K tokens often need frontier for coherence. Prompts <500 tokens usually don't.

3. **Embedding similarity to known-hard set**: if the query is close (cosine > 0.88) to a known-hard bucket, escalate to frontier directly.

4. **Self-confidence from first-pass**: send to cheap; if model's log-probs show low confidence OR it refuses OR outputs hedging language, retry on frontier. Adds P95 latency on ~10% of traffic but saves 50%+ on the other 90%.

### Three patterns

> **【拓展：模型路由的三种模式】** 模型路由的三种实现模式对比：(1) Pre-route——前置分类器（规则或小 LLM），增加 5-10ms 延迟，总体最快；(2) Cascade——先发到廉价模型，低置信度时升级到前沿模型，中位延迟约 1.2x、升级时约 2x，质量底线最好；(3) Ensemble route——并行运行廉价和前沿模型，奖励模型选择最佳，最高质量但最高成本。生产中推荐 Cascade 作为默认——它在质量、成本、延迟之间提供了最佳平衡。

**Pre-route** (classifier up front): ~5-10ms latency added; fastest overall.

**Cascade** (cheap-first, escalate on low confidence): ~1.2x median latency (cheap run plus verify), ~2x on escalated. Best quality floor.

**Ensemble route** (run cheap and frontier in parallel for a sample, reward-model pick): highest quality, highest cost; use only for critical A/B.

### Implementation

AI gateways (Phase 17 · 19) expose routing. LiteLLM has `router` config with fallback and cost-routing. Portkey has guards + routing. Kong AI Gateway has plugin-based routing. OpenRouter's model marketplace exposes a recommendation API.

Open-source: RouteLLM (LMSYS), Not Diamond (commercial), Prompt Mule.

### The 2026 price curve

| Model class | Late 2022 | 2026 | Change |
|-------------|-----------|------|--------|
| GPT-4-level quality | ~$20/M | ~$0.40/M | 50x cheaper |
| Frontier (GPT-5, Claude 4) | — | ~$3-10/M | new tier |

Most of the improvement is serving efficiency — the core lessons in Phase 17 · 04-09 turned into provider-side cost drops. Routing lets you capture those gains at the app layer instead of waiting for all your users to migrate to the cheap tier.

### Drift is the real risk

> **【中文解读】** 漂移是模型路由的真正风险。路由将 40% 发送到廉价模型，6 个月后任务分布变化（用户更成熟、问题更长），但路由器的分类器仍基于 Q1 数据训练。质量悄悄下降——没有投诉足够响亮，直到在竞争对手的基准测试中落败才知道。必须通过在线质量指标门控路由：用户反馈、自动 LLM 评审（5% 采样）、升级率、拒绝率。

> **【拓展：模型路由的实现方案】** 2026 年模型路由的实现选项：(1) AI 网关（Phase 17·19）——LiteLLM 的 router config、Portkey 的 guards+routing、Kong AI Gateway 的插件式路由、OpenRouter 的推荐 API；(2) 开源——RouteLLM（LMSYS）提供完整的路由库；(3) 商业——Not Diamond 提供 SaaS 模型路由产品。三种路由模式：Pre-route（前置分类，最快）、Cascade（先廉价再升级，质量最稳）、Ensemble（并行运行多模型+奖励模型选择，最高质量但最高成本）。

Your route sends 40% to the cheap model. Over six months, the task distribution shifts (users get more sophisticated, ask longer questions). The router doesn't notice because its classifier was trained on Q1 data. Quality drops silently. Nobody complains loud enough. You find out in a competitor benchmark you lost.

Gate routes by online quality metrics:

- User thumbs-up / thumbs-down per route.
- Automated LLM-judge on a held-out sample (5%) per route.
- Escalation rate: if cascade is kicking up-route >30%, the cheap model is being over-routed.
- Refusal rate per route.

### Numbers you should remember

- 2026 routing savings at iso-quality: 20-60% case studies.
- LLM price drop 2022-2026: ~10x per year aggregate.
- GPT-4-level 2022 vs 2026: ~$20/M → ~$0.40/M.
- Cascade latency impact: ~1.2x median, ~2x escalated (~10% of traffic).

## Use It | 用框架实现

`code/main.py` simulates pre-route, cascade, and ensemble on a mixed workload. Reports blended cost, quality loss, and escalation rate.

> `code/main.py` simulates pre-route, cascade, and ensemble on a mixed workload. Reports blended cost, quality loss, and escalation rate.

> `code/main.py` simulates pre-route, cascade, and ensemble on a mixed workload. Reports blended cost, quality loss, and escalation rate.

## Ship It | 产出物

This lesson produces `outputs/skill-router-plan.md`. Given workload and quality budget, picks a routing pattern and signals.

> 本课产出 `outputs/skill-router-plan.md`. Given workload and quality budget, picks a routing pattern and signals.

## Exercises | 练习题

1. Run `code/main.py`. At what accuracy floor does cascade beat pre-route?
   中文翻译：运行 `code/main.py`。级联在什么精度下限下优于预路由？
2. Your user base is 30% enterprise (complex queries), 70% free tier (simple). Design the routing split. What online metric gates it?
   中文翻译：你的用户群 30% 是企业（复杂查询），70% 是免费层（简单）。设计路由策略。
3. A route drops quality by 2% but saves 40%. Is that a ship? Depends on product — argue both.
   中文翻译：一个路由降低质量 2% 但节省 40%。值得上线吗？取决于产品上下文。
4. Implement a confidence check using logprobs from OpenAI / Anthropic APIs. What's the threshold you start with?
   中文翻译：使用 OpenAI/Anthropic API 的 logprobs 实现置信度检查。什么阈值触发升级？
5. Over six months, escalation rate climbs from 8% to 22%. Diagnose three causes and the fix for each.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Model routing | "cost broker" | Dynamic choice of model per request |
| Model cascade | "cheap-first escalate" | Run cheap, fall through to frontier on low confidence |
| Pre-route | "classify first" | Classifier up front; no re-run |
| Ensemble route | "parallel pick" | Run multiple, reward-model picks best |
| Escalation rate | "uprouted %" | Fraction of cascade requests that escalated |
| RouteLLM | "LMSYS router" | OSS router library |
| Not Diamond | "commercial router" | SaaS model-routing product |
| Drift | "cheap creep" | Distribution shift without router noticing |
| Online quality gate | "live check" | Automated LLM-judge sampling live traffic |

## Further Reading | 延伸阅读

- [AbhyashSuchi — Model Routing LLM 2026 Best Practices](https://abhyashsuchi.in/model-routing-llm-2026-best-practices/)
- [Lukas Brunner — Rise of Inference Optimization 2026](https://dev.to/lukas_brunner/the-rise-of-inference-optimization-the-real-llm-infra-trend-shaping-2026-4e4o)
- [RouteLLM paper / code](https://github.com/lm-sys/RouteLLM)
- [Not Diamond — model routing](https://www.notdiamond.ai/)
- [OpenRouter](https://openrouter.ai/) — multi-model gateway with routing primitives.
