# Failure Modes — MAST, Groupthink, Monoculture, Cascading Errors | 失败模式 群体思维 MAST

> The reference taxonomy for 2026 is **MAST** (Cemri et al., NeurIPS 2025, arXiv:2503.13657), derived from 1642 execution traces across 7 state-of-the-art open-source MAS showing **41–86.7% failure rate**. Three root categories: **Specification Problems** (41.77%) — role ambiguity, unclear task definitions; **Coordination Failures** (36.94%) — communication breakdowns, state desync; **Verification Gaps** (21.30%) — missing validation, absent quality checks. The **Groupthink** family (arXiv:2508.05687) adds: monoculture collapse (same base model → correlated failures), conformity bias (agents reinforce each other's errors), deficient theory of mind, mixed-motive dynamics, cascading reliability failures. Cascading example: retry storms where a payment failure triggers order retries, which trigger inventory retries, which overwhelm inventory service (10x load in seconds — needs circuit breakers). Memory poisoning: one agent's hallucination enters shared memory, downstream agents treat it as fact; accuracy decays gradually, making root-cause diagnosis painful. **STRATUS** (NeurIPS 2025) reports 1.5x mitigation-success improvement via specialized detection / diagnosis / validation agents. This lesson treats failure modes as first-class engineering targets.

> **【中文解读】** 本节介绍了多 Agent 的失败模式和群体思维——多 Agent 系统特有的失败模式。

> **【拓展：failure modes mast groupthink→具体应用】** 多 Agent 系统的特有失败模式：(1) 群体思维（Groupthink）——Agent 过度趋同，失去多样性；(2) 信息级联——一个 Agent 的错误被后续 Agent 放大；(3) 死锁——Agent 互相等待无法继续；(4) 活锁——Agent 不断改变策略但无法收敛。防范措施包括：注入异见 Agent、随机化发言顺序、设置超时。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 13 (Shared Memory), Phase 16 · 14 (Consensus and BFT), Phase 16 · 15 (Voting and Debate Topology) | **前置知识:** Phase 16 · 13（共享内存），Phase 16 · 14（共识与 BFT），Phase 16 · 15（投票与辩论拓扑）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problem | 问题引入

Multi-agent systems fail 41-86.7% of the time on real tasks (Cemri et al. 2025 measured this across 7 open-source MAS). That is not debuggable by "just add more agents." The failures have structural causes. The MAST taxonomy gives you the categories. This lesson maps each category to a concrete detection, diagnosis, and mitigation pattern so the numbers stop looking arbitrary.

> 多 Agent 系统在真实任务上 41-86.7% 的时间会失败（Cemri 等人 2025 年在 7 个开源 MAS 上测量）。这不是"添加更多 Agent"就能调试的。失败有结构性原因。MAST 分类法给你类别。本课将每个类别映射到具体的检测、诊断和缓解模式。

The 2026 production practice is to treat failure modes as design inputs. Your architecture is not "good enough" until you can point to each MAST category and name the mitigation you deployed.

> 2026 年生产实践是将失败模式视为设计输入。你的架构不是"足够好"的，直到你能指向每个 MAST 类别并说出你部署的缓解措施。

## Concept | 核心概念

### MAST categories

**Specification Problems (41.77% of failures).** The agent's task was not defined tightly enough. Examples:

> **规范问题（41.77% 的失败）。** Agent 的任务定义不够紧密。例子：

- Role ambiguity: two agents both think they are the reviewer.
  中文翻译：角色模糊：两个 Agent 都认为自己是审阅者。
- Task underspecified: "summarize this" when the user wanted a specific angle.
  中文翻译：任务规格不足："总结这个"，但用户想要特定角度。
- Success criteria implicit: the agent cannot tell if it succeeded.
  中文翻译：成功标准隐含：Agent 无法判断是否成功。

Mitigations:

> 缓解措施：

- Write explicit role contracts. Each agent's prompt states what it does *and what it does not do*.
  中文翻译：编写显式角色契约。每个 Agent 的提示声明它做什么*和不做什么*。
- Acceptance tests per task. Before the agent starts, define "done looks like X."
  中文翻译：每个任务的验收测试。在 Agent 开始前，定义"完成的样子是 X"。
- Pre-flight spec check: a separate agent reviews the task definition before dispatch.
  中文翻译：预检规范检查：单独的 Agent 在分发前审查任务定义。

**Coordination Failures (36.94%).** Communication or state breakdowns.

> **协调失败（36.94%）。** 通信或状态故障。

Examples:

> 例子：

- Two agents update shared state without synchronization.
  中文翻译：两个 Agent 不同步地更新共享状态。
- Message lost between agents (queue failure, timeout).
  中文翻译：Agent 间消息丢失（队列故障、超时）。
- State drift: agent A thinks the task is done; agent B is still executing.
  中文翻译：状态漂移：Agent A 认为任务完成；Agent B 还在执行。

Mitigations:

> 缓解措施：

- Versioned shared state with optimistic concurrency.
  中文翻译：带乐观并发的版本化共享状态。
- Explicit acknowledgment for critical messages (retry until acked).
  中文翻译：关键消息的显式确认（重试直到确认）。
- Periodic state-sync checkpoints; detect drift early.
  中文翻译：定期状态同步检查点；早期检测漂移。

**Verification Gaps (21.30%).** No independent check on outputs.

> **验证缺口（21.30%）。** 没有对输出的独立检查。

Examples:

> 例子：

- One agent claims success; no one verifies.
  中文翻译：一个 Agent 声称成功；没人验证。
- Chain of agents each trusts the prior's output.
  中文翻译：Agent 链中每个都信任前一个的输出。
- Test coverage missing on the emergent composed behavior.
  中文翻译：涌现组合行为缺少测试覆盖。

Mitigations:

> 缓解措施：

- Independent verifier agent (Lesson 13). Read-only, independent source access.
  中文翻译：独立验证 Agent（第 13 课）。只读，独立源访问。
- Explicit handoff contract: "A's output must pass checker C before B starts."
  中文翻译：显式交接契约："A 的输出必须在 B 开始前通过检查器 C。"
- Outcome logging for post-hoc analysis.
  中文翻译：结果日志用于事后分析。

### Groupthink family (arXiv:2508.05687)

Five related failures when agents homogenize or mimic each other:

**Monoculture collapse.** Same base model or training data → correlated errors. When three agents share an LLM, they share its hallucinations.

**Conformity bias.** Agents adjust toward the loudest or most-confident peer, even when wrong.

**Deficient ToM.** Agents fail to model each other's beliefs; coordination falls apart (Lesson 18).

**Mixed-motive dynamics.** Agents with partially-aligned incentives drift toward compromise-middle, which satisfies no one.

**Cascading reliability failures.** One component's error pattern triggers error patterns in dependent components.

### Cascading example — the retry storm

A classic 2026 incident pattern:

```
payment service fails 10% of requests
   ↓
order agent retries payment (exponential backoff but naive)
   ↓
each retry is a new order-inventory check
   ↓
inventory service sees 2x normal load
   ↓
inventory service starts timing out
   ↓
every order retries inventory check
   ↓
inventory service sees 10x normal load
   ↓
cluster goes down
```

The fix is classical: **circuit breakers**. When downstream error rate exceeds threshold, short-circuit with cached or default results. Plus capped retry budgets per request.

Circuit breakers are one of the few multi-agent failure mitigations you borrow directly from distributed systems without modification.

### Memory poisoning (revisited)

From Lesson 13: one agent's hallucination becomes shared-memory fact; downstream agents reason on the poisoned fact. In MAST terms, this is a verification gap at the shared-memory layer.

Gradual accuracy decay is the symptom. You do not get a crash; you get slow drift that is hard to root-cause.

Mitigation: append-only log, provenance, unwritable verifier. Already covered in Lesson 13.

### STRATUS — specialized agents for failure detection

STRATUS (NeurIPS 2025) reports 1.5x mitigation-success improvement when you deploy:

- **Detection agent.** Watches for symptom patterns (high disagreement, retry spikes, accuracy drift).
- **Diagnosis agent.** Given symptoms, infers likely root cause from the MAST taxonomy.
- **Validation agent.** After a mitigation is applied, checks that symptoms clear.

This is SRE-style incident response, applied to agent systems. The three roles can all be LLM agents with specialized prompts.

### The failure-mode audit

A 2026 best practice is an annual (or per-major-release) failure-mode audit:

1. **Trace sample.** Collect ~1000 real execution traces.
2. **Categorize.** For each trace's failures, map to MAST + Groupthink categories.
3. **Compute failure-by-category rate.** Which categories dominate your system?
4. **Rank mitigations.** Which fix would eliminate the most failures?
5. **Pick 2-3 mitigations.** Implement; re-audit next quarter.

The discipline is more important than the specific choices. Without audits, failures blend into noise and never get systematically addressed.

### When systems fail silently

The most dangerous failure category is silent correctness failure. A system that fails loudly (crash, exception, alert) can be monitored. A system that produces plausible-but-wrong outputs cannot be detected by exception logs. This is why verification gaps are the most expensive category per-failure even though they are only 21.30% by count.

Invest in:
- Sample-based human review.
- Golden-dataset regression tests.
- Cross-agent cross-checking on important outputs.

### Failure vs slow failure

Some failures are immediate; some are slow. Immediate failures (timeout, schema mismatch, auth error) are cheap to detect. Slow failures (memory poisoning, monoculture drift, role ambiguity) are expensive to detect and prevent.

The 2026 engineering move: instrument slow-failure proxies so you can catch drift before it becomes a visible error. Agreement rate, retry rate, output-length distribution, and edit-distance between consecutive agent versions are all useful proxies.

## Build It | 动手构建

`code/main.py` implements:

- `FailureTaxonomy` — categorizes simulated incidents into MAST + Groupthink categories.
- `CircuitBreaker` — classic pattern; opens when error rate exceeds threshold.
- `RetryStormSimulator` — shows the cascading failure; toggles circuit breaker on / off.
- `DetectionAgent` — scripted STRATUS-style symptom matcher.

Run:

```
python3 code/main.py
```

Expected output:
- retry storm with no circuit breaker: inventory errors blow up (simulated).
- with circuit breaker: cap at threshold; degraded-mode responses served.
- detection agent flags the pattern and names the MAST category.

## Use It | 使用方法

`outputs/skill-mast-auditor.md` runs a MAST-style failure-mode audit on a multi-agent system. Traces → categorization → mitigation ranking.

## Ship It | 部署上线

Failure-mode discipline in production:

- **MAST audit per quarter.** Not annual. Categories shift as your system grows.
  中文翻译：**每季度 MAST 审计。** 不是年度的。类别随系统增长而变化。
- **Circuit breakers everywhere.** Each outbound call to any dependent service. Default open threshold at 5-10% error rate.
  中文翻译：**到处都是熔断器。** 每个对依赖服务的出站调用。默认断开阈值为 5-10% 错误率。
- **Golden datasets.** Small, high-quality, hand-audited. Regression-test against them weekly.
  中文翻译：**黄金数据集。** 小型、高质量、人工审计。每周对它们进行回归测试。
- **STRATUS trio.** Detection + Diagnosis + Validation agents monitoring production. Start with the detection agent only; add diagnosis when symptoms are noisy.
  中文翻译：**STRATUS 三重奏。** 检测 + 诊断 + 验证 Agent 监控生产。从检测 Agent 开始；当症状嘈杂时添加诊断。
- **Failure budget.** Explicit SLO for failure rate by category. Exceeding budget triggers a stop-shipping conversation.
  中文翻译：**失败预算。** 按类别的失败率显式 SLO。超出预算触发停止发布对话。

## Exercises | 练习题

1. Run `code/main.py`. Confirm the circuit breaker caps the retry storm. Vary the failure threshold and observe the tradeoff.
2. Implement a **slow-failure proxy**: agreement rate across 3 parallel agents. When it drops sharply, trigger an alert. Simulate a monoculture drift by gradually correlating agent outputs.
3. Read Cemri et al. (arXiv:2503.13657). Pick one of their 7 MAS systems and map its top 3 failure categories. How do these compare to what MAST predicts?
4. Read the Groupthink paper (arXiv:2508.05687). Identify which of the five patterns is hardest to detect in production. Propose a proxy metric.
5. Design a STRATUS-style detection-diagnosis-validation trio for a specific multi-agent system you know. Which symptoms does detection watch for? What mitigations does diagnosis recommend? How does validation confirm they work?

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MAST / MAST 分类法 | "The 2026 taxonomy" / "2026 年分类法" | Cemri 2025; 3 root categories + 14 sub-types of failures. / Cemri 2025；3 个根类别 + 14 个失败子类型。 |
| Specification Problem / 规范问题 | "Role ambiguity" / "角色模糊" | Task or role under-defined; agents do not know what to do. / 任务或角色定义不足；Agent 不知道做什么。 |
| Coordination Failure / 协调失败 | "State drift" / "状态漂移" | Communication or sync breakdown between agents. / Agent 之间的通信或同步故障。 |
| Verification Gap / 验证缺口 | "No one checked" / "没人检查" | Outputs accepted without independent validation. / 输出未经独立验证即接受。 |
| Groupthink family / 群体思维族 | "Homogeneity failures" / "同质性失败" | Monoculture, conformity, deficient ToM, mixed-motive, cascading. / 单一文化、从众、ToM 不足、混合动机、级联。 |
| Monoculture collapse / 单一文化崩溃 | "Same model, same hallucinations" / "相同模型，相同幻觉" | Correlated errors from shared base model or training data. / 共享基础模型或训练数据的相关错误。 |
| Retry storm / 重试风暴 | "Cascading error amplification" / "级联错误放大" | One failure triggers retries which amplify load downstream. / 一次失败触发重试，放大下游负载。 |
| Circuit breaker / 熔断器 | "Fail fast on error rate" / "错误率快速失败" | Open when error rate exceeds threshold; short-circuit with default. / 错误率超阈值时断开；用默认值短路。 |
| STRATUS | "Incident response trio" / "事件响应三重奏" | Detection + diagnosis + validation agents. 1.5x mitigation success. / 检测 + 诊断 + 验证 Agent。1.5 倍缓解成功。 |
| Memory poisoning / 记忆投毒 | "Hallucinations propagate" / "幻觉传播" | Shared-memory fact tainted; downstream agents reason on poison. / 共享记忆事实被污染；下游 Agent 在毒化数据上推理。 |

## Further Reading | 延伸阅读

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) — MAST taxonomy, NeurIPS 2025
- [Groupthink failures in multi-agent LLMs](https://arxiv.org/abs/2508.05687) — monoculture, conformity, and the five-family taxonomy
- [STRATUS — specialized agents for MAS incident response](https://neurips.cc/) — NeurIPS 2025 proceedings entry (detection + diagnosis + validation)
- [Release It! — stability patterns (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/) — the canonical circuit-breaker reference
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — production failure-mode notes
