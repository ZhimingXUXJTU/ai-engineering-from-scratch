# A/B Testing LLM Features — GrowthBook, Statsig, and the Vibes Problem | 特性 LLM PR

> Traditional A/B testing was not built for non-deterministic LLMs. The critical distinction: evals answer "can the model do the job?" A/B tests answer "do users care?" Both are required; shipping on vibe checks is over. What to test in 2026: prompt engineering (wording), model selection (GPT-4 vs GPT-3.5 vs OSS; accuracy vs cost vs latency), generation parameters (temperature, top-p). Real cases: a chatbot reward-model variant delivered +70% conversation length and +30% retention; Nextdoor AI subject-line experiments delivered +1% CTR after reward-function refinement; Khan Academy Khanmigo iterated on a latency-vs-math-accuracy axis. Platform split: **Statsig** (acquired by OpenAI for $1.1B in September 2025) — sequential testing, CUPED, all-in-one. **GrowthBook** — open-source, warehouse-native, Bayesian + Frequentist + Sequential engines, CUPED, SRM checks, Benjamini-Hochberg + Bonferroni corrections. You pick based on warehouse-SQL preference and whether "acquired by OpenAI" matters to your organization.

> **【中文解读】** 本节介绍了 LLM 特性的 AB 测试——科学评估 LLM 功能变更效果的方法。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy sequential test simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 20 (Progressive Deployment) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 20 (Progressive Deployment)
**Time:** ~60 minutes | **时间:** ~60 minutes

## Learning Objectives | 学习目标

- Distinguish evals ("can the model do the job") from A/B tests ("do users care").
  中文翻译：Distinguish evals ("can the model do the job") from A/B tests ("do users care").
- Enumerate three testable axes (prompt, model, parameters) and pick the metric for each.
  中文翻译：Enumerate three testable axes (prompt, model, parameters) and pick the metric for each.
- Explain CUPED, sequential testing, and Benjamini-Hochberg multiple-comparison corrections.
  中文翻译：Explain CUPED, sequential testing, and Benjamini-Hochberg multiple-comparison corrections.
- Pick Statsig or GrowthBook based on warehouse-SQL posture and corporate acquisition stance.
  中文翻译：Pick Statsig or GrowthBook based on warehouse-SQL posture and corporate acquisition stance.

## The Problem | 问题引入

> **【中文解读】** 传统 A/B 测试不是为非确定性 LLM 构建的。关键区分：评估（evals）回答"模型能做这件事吗？"，A/B 测试回答"用户在乎吗？"两者都是必需的——凭感觉上线（vibes check）的时代已经结束。2026 年可测试的三个维度：提示工程（措辞）、模型选择（GPT-4 vs GPT-3.5 vs OSS；准确率 vs 成本 vs 延迟）、生成参数（temperature、top-p）。

> **【拓展：LLM A/B 测试的真实案例】** 2026 年 LLM A/B 测试的生产案例：(1) 聊天机器人奖励模型变体——+70% 对话长度、+30% 留存率；(2) Nextdoor AI 主题行实验——奖励函数优化后 +1% CTR；(3) Khan Academy Khanmigo——在延迟 vs 数学准确率轴上迭代。平台选择：Statsig（2025 年 9 月被 OpenAI 以 $1.1B 收购）——全合一；GrowthBook——开源、仓库原生、Bayesian + Frequentist + Sequential 引擎。

You hand-tuned a system prompt. It feels better. You ship it. Conversion changes by noise. You blame the metric. Or you shipped a new model and conversion didn't move — did the model degrade or was the change too small to detect? You don't know, because you shipped without an A/B.

Evals answer whether the model can do a task on a labeled set. They do not answer whether users prefer the output. Only a controlled online experiment answers that, and only if the experiment has enough power, controls for non-determinism, and corrects for multiple comparisons.

## The Concept | 核心概念

### Evals vs A/B tests

**Evals** — offline, labeled set, judge (rubric or LLM-as-judge or human). Answer: "Is the output correct / helpful / safe on this fixed distribution?"

**A/B test** — online, live users, randomized. Answer: "Does the new variant move the user-level metric that matters?"

Both required. Evals catch regressions before exposure; A/B confirms product impact after.

### What to test

1. **Prompt engineering** — wording, system-prompt structure, examples. Metric: task success, user retention, cost/request.
2. **Model selection** — GPT-4 vs GPT-3.5-Turbo vs Llama-OSS. Metric: accuracy (task) + cost/request + latency P99. Multi-objective.
3. **Generation parameters** — temperature, top-p, max_tokens. Metric: task-specific (output diversity vs determinism).

### CUPED — variance reduction

> **【中文解读】** CUPED（使用预实验数据的受控实验）是 A/B 测试的关键方差降低技术。原理是在比较后验期之前，回归掉前验期的方差。典型方差降低 30-70%，等效于免费增加有效样本量。Statsig 和 GrowthBook 都实现了 CUPED。

Controlled-experiments Using Pre-Experiment Data. Regress out pre-period variance before comparing post-period. Typical variance reduction: 30-70%. Effective sample size goes up for free.

Implementation: both Statsig and GrowthBook implement.

### Sequential testing

Classical A/B assumes fixed sample size. Sequential tests ("peek-and-decide") control false-positive rate under repeated looks. Always-valid sequential procedures (mSPRT, Howard's confidence sequences) let you stop early on clear winners.

### Multiple-comparison corrections

Running 20 A/B tests at 95% confidence produces one false positive by chance. Bonferroni correction tightens α per-test; Benjamini-Hochberg controls false-discovery rate. GrowthBook implements both.

### SRM — sample ratio mismatch

Assignment hash randomizes users to variants. If 50/50 split delivers 47/53, something is broken — SRM check flags it. Both platforms implement.

### Statsig vs GrowthBook

> **【拓展：Statsig vs GrowthBook 选型】** Statsig vs GrowthBook 的 2026 年选型对比：Statsig 2025 年 9 月被 OpenAI 以 $1.1B 收购，是全合一 SaaS（feature flags + 实验分析 + 可观测性），内置序贯检验和 CUPED，适合想要捆绑产品的团队。GrowthBook 是 MIT 开源，仓库原生（直接读 Snowflake/BigQuery/Redshift），支持 Bayesian + Frequentist + Sequential 三种引擎、CUPED、SRM 检查、Benjamini-Hochberg + Bonferroni 校正，适合数据团队控制指标层的仓库-SQL 商店。选型关键：是否介意 OpenAI 所有权 + 是否偏好仓库-SQL。

**Statsig**:
- Acquired by OpenAI for $1.1B (September 2025). Hosted, SaaS.
- Sequential testing, CUPED, held-out populations.
- All-in-one: feature flags + experimentation + observability.
- Best fit: team already wants a bundled product, doesn't care about OpenAI ownership.

**GrowthBook**:
- Open-source (MIT); warehouse-native (reads from Snowflake/BigQuery/Redshift directly).
- Multiple engines: Bayesian, Frequentist, Sequential.
- CUPED, SRM, Bonferroni, BH corrections.
- Self-host or managed cloud.
- Best fit: warehouse-SQL shop, data team controls the metric layer, wants OSS.

### Non-determinism complicates power

Same prompt produces varying outputs. Traditional power calculations assume IID observations. With LLM non-determinism, effective sample size is lower than nominal. Multiply required sample size by ~1.3-1.5x as a safety margin.

### Real case outcomes

- Chatbot reward model variant: +70% conversation length, +30% retention.
- Nextdoor subject lines: +1% CTR after reward-function refinement.
- Khan Academy Khanmigo: iterative latency-vs-math-accuracy trade.

### The anti-pattern: shipping on vibes

> **【拓展：LLM 非确定性对 A/B 测试的影响】** LLM 的非确定性影响 A/B 测试的统计功效。相同提示产生不同输出，传统的 power 计算假设 IID 观测值。在 LLM 非确定性下，有效样本量低于名义值——需要将所需样本量乘以 1.3-1.5x 作为安全边际。Sequential testing（序贯检验）允许在明确赢家出现时提前停止，比固定样本量测试节省 20-40% 的实验时间。多重比较校正（Bonferroni / Benjamini-Hochberg）在同时运行多个实验时必不可少。

Every senior engineer can name a feature that was shipped because "it feels better" with no A/B. Most of them regressed product metrics the team didn't notice for months. A/B is the forcing function.

### Numbers you should remember

- Statsig acquired by OpenAI: $1.1B, September 2025.
- GrowthBook: open-source MIT; Bayesian + Frequentist + Sequential.
- CUPED variance reduction: 30-70%.
- LLM non-determinism → +30-50% sample-size buffer.

## Use It | 用框架实现

`code/main.py` simulates a sequential A/B test with fixed and sequential boundaries. Shows how sequential lets you stop early.

> `code/main.py` simulates a sequential A/B test with fixed and sequential boundaries. Shows how sequential lets you stop early.

> `code/main.py` simulates a sequential A/B test with fixed and sequential boundaries. Shows how sequential lets you stop early.

## Ship It | 产出物

This lesson produces `outputs/skill-ab-plan.md`. Given feature change, workload, baseline, picks platform, gates, sample size.

> 本课产出 `outputs/skill-ab-plan.md`. Given feature change, workload, baseline, picks platform, gates, sample size.

## Exercises | 练习题

1. Run `code/main.py`. For an expected 5% lift with baseline 3% conversion, what sample size to 80% power?
   中文翻译：Run `code/main.py`. For an expected 5% lift with baseline 3% conversion, what sample size to 80% power?
2. Pick Statsig or GrowthBook for a healthcare-regulated on-prem customer.
   中文翻译：Pick Statsig or GrowthBook for a healthcare-regulated on-prem customer.
3. Design an A/B that tests GPT-4 vs GPT-3.5 on cost-per-resolved-ticket. What's the primary metric, guardrail metric, secondary?
   中文翻译：Design an A/B that tests GPT-4 vs GPT-3.5 on cost-per-resolved-ticket. What's the primary metric, guardrail metric, secondary?
4. Your canary passes but A/B shows -1.2% conversion. Do you ship? Write the escalation criteria.
   中文翻译：Your canary passes but A/B shows -1.2% conversion. Do you ship? Write the escalation criteria.
5. Apply CUPED to a pre-period with 60% of the variance of post. Compute the effective-sample-size boost.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Eval | "offline test" | Labeled-set evaluation of model capability |
| A/B test | "experiment" | Live randomized comparison on users |
| CUPED | "variance reduction" | Pre-period regression to reduce variance |
| Sequential test | "peek-ok test" | Always-valid procedure allowing early stop |
| Multiple comparison | "the family error" | Running many tests inflates false positives |
| Bonferroni | "tight correction" | Divide α by number of tests |
| Benjamini-Hochberg | "BH FDR" | False-discovery-rate control, less conservative |
| SRM | "bad split" | Sample ratio mismatch; assignment bug |
| Statsig | "OpenAI owned" | Commercial all-in-one, acquired 2025 |
| GrowthBook | "the OSS one" | MIT warehouse-native platform |
| mSPRT | "sequential probability ratio test" | Classical sequential procedure |

## Further Reading | 延伸阅读

- [GrowthBook — How to A/B Test AI](https://blog.growthbook.io/how-to-a-b-test-ai-a-practical-guide/)
- [Statsig — Beyond Prompts: Data-Driven LLM Optimization](https://www.statsig.com/blog/llm-optimization-online-experimentation)
- [Statsig vs GrowthBook comparison](https://www.statsig.com/perspectives/ab-testing-feature-flags-comparison-tools)
- [Deng et al. — CUPED](https://www.exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf)
- [Howard — Confidence Sequences](https://arxiv.org/abs/1810.08240)
