# Kill Switches, Circuit Breakers, and Canary Tokens | 终止开关、断路器与金丝雀 Token

> A kill switch is a boolean held outside the agent's edit surface — a Redis key, a feature flag, a signed config — that disables the agent entirely. A circuit breaker is finer-grained: it trips on a specific pattern (five identical tool calls in a row), pauses the offending path, and escalates to a human. A canary token inherits from classical deception: a fake credential or honeypot record an agent has no legitimate reason to touch, whose access triggers an alert. eBPF-based datapaths (e.g. Cilium) can rewrite a quarantined pod's egress to a forensic honeypot at the kernel layer; published Cilium benchmarks report sub-millisecond P99 datapath latency under load (your propagation budget depends on how a policy update reaches the node, not the datapath itself). Statistical detectors (EWMA, CUSUM) that adapt to a moving baseline will quietly accept drift — layer them with hard constitutional limits that do not bend.

> **【中文解读】** 终止开关是位于 Agent 编辑面之外的布尔值——Redis 键、功能标志、签名配置——完全禁用 Agent。断路器更细粒度：在特定模式上跳闸（连续五次相同工具调用），暂停违规路径并升级到人类。金丝雀 token 继承自经典欺骗：Agent 无合法理由触及的假凭据或蜜罐记录，其访问触发警报。基于 eBPF 的数据路径（例如 Cilium）可在内核层将隔离 pod 的出口重写到取证蜜罐；公开 Cilium 基准报告负载下亚毫秒 P99 数据路径延迟（你的传播预算取决于策略更新如何到达节点，而非数据路径本身）。适应移动基线的统计检测器（EWMA、CUSUM）会静默接受漂移——将它们与不弯折的硬宪法限制分层。

> **【拓展：三层不信任架构】** 三个检测器全部不信任 Agent 自报告：终止开关外置（Agent 不能编辑）、断路器模式匹配（不看 Agent 意图）、金丝雀基于"不应触及"原则（访问即警报）。统计检测器（EWMA/CUSUM）适应漂移但会被耐心攻击者缓慢移动基线绕过；硬宪法限制（"永不发邮件给 secrets@"）简单、可审计、不可博弈。分层：统计检测器捕获大多数噪声，硬限制捕获走过检测器的攻击。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-detector simulator: kill switch, circuit breaker, canary) | **语言:** Python（标准库，三检测器模拟器：终止开关、断路器、金丝雀）
**Prerequisites:** Phase 15 · 13 (Cost governors), Phase 15 · 10 (Permission modes) | **前置知识:** Phase 15 · 13（成本治理器），Phase 15 · 10（权限模式）
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 15·13（Cost Governors）、Phase 15·10（权限模式）、网络安全基础（蜜罐、断路器）。三道防线 = 不信任 Agent 自报告。
> 💡 **【类比】** 三道防线 = "银行安保三层"。Kill Switch = 总闸（紧急情况一键断电，Agent 不能改）；Circuit Breaker = 自动跳闸（检测到异常模式自动暂停，如连续 5 次相同操作）；Canary Token = 银行假钞（不该被触及的假数据，一被访问就报警）。三层都不信 Agent——靠外置基础设施检测。
> 🤔 **【困惑】** Q: 为什么不靠 Agent 内置安全检查？— 因为 Agent 可能被破解或自修改绕过（DGM 案例）。修复：检测器必须独立于 Agent（Redis 键、内核 eBPF、签名配置），Agent 看不到、改不了、绕不过。这是"trust-but-verify"的核心。

## The Problem | 问题引入

> **【中文解读】** 终止开关（Kill Switches）和金丝雀测试（Canaries）是 Agent 安全的两道防线。终止开关允许人类操作员立即停止 Agent 的所有操作。金丝雀测试在 Agent 执行前用小规模测试检测潜在问题——类似于矿井中的金丝雀预警有毒气体。两者结合形成'检测-停止'的安全模式。

> **【拓展：kill switches canaries】** 终止开关和金丝雀测试借鉴了软件工程和工业安全的最佳实践。金丝雀部署在软件工程中指先向 1% 的用户发布新版本，检测问题后再全面部署。在 Agent 上下文中，金丝雀测试指在执行高风险操作前先用安全数据做小规模测试。终止开关则类似于工厂的紧急停止按钮——简单、可靠、无条件。

Cost governors (Lesson 13) bound what the agent can spend. They do not bound what the agent can do inside the budget.

> 成本控制器（第 13 课）限制 Agent 能花费什么。它们不限制 Agent 在预算内能做什么。

An agent with a $50 velocity limit can still exfiltrate a secret, publish the wrong post, or delete a resource — the expensive action is often the cheap one in tokens.

> 带 $50 速度限制的 Agent 仍可泄露秘密、发布错误帖子或删除资源——昂贵动作往往是 token 上便宜的。

This lesson covers the three detectors that sit next to the cost layer:

> 本课覆盖位于成本层旁边的三个检测器：

> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

1. **Kill switch**: boolean off-button held outside the agent's reach.
   中文翻译：**终止开关**：位于 Agent 触及之外的布尔关闭按钮。
2. **Circuit breaker**: action-pattern detector that pauses a specific path.
   中文翻译：**断路器**：暂停特定路径的动作模式检测器。
3. **Canary token**: bait that an agent with no legitimate reason to touch will reveal itself by touching.
   中文翻译：**金丝雀 token**：Agent 无合法理由触及、触及就会暴露自己的诱饵。

All three are pre-LLM engineering. Classical deception, rate-limit breakers, and feature-flag kills predate autonomous agents. What's new is the attack surface: agents read untrusted content (Lesson 11), edit their own memory, and can compose many safe-looking actions into an unsafe one. The detectors named here work because they do not trust the agent's self-report.

> 三者都是 LLM 前工程。经典欺骗、速率限制断路器和功能标志终止早于自主 Agent。新的是攻击面：Agent 读取不受信任内容（第 11 课）、编辑自己的记忆、可将多个安全动作组合为不安全动作。此处命名的检测器有效因为它们不信任 Agent 的自报告。

## The Concept | 核心概念

### Kill switches | 终止开关

A kill switch is a boolean the agent reads but cannot write.

> 终止开关是 Agent 可读不可写的布尔值。

Implementation choices:

> 实现选择：

- **Feature flag in a managed service.** LaunchDarkly, Statsig, Unleash. Updates propagate in seconds.
  中文翻译：**管理服务中的功能标志。** LaunchDarkly、Statsig、Unleash。更新在数秒内传播。
- **Redis key the agent polls.** Simple; requires the agent process to check on every turn.
  中文翻译：**Agent 轮询的 Redis 键。** 简单；要求 Agent 进程每轮检查。
- **Signed config in object storage.** Agent verifies a signature on boot; rejects unsigned states.
  中文翻译：**对象存储中的签名配置。** Agent 启动时验证签名；拒绝未签名状态。
- **OS-level signal or container-lifecycle kill.** Docker `kill`, Kubernetes `kubectl delete pod`, systemd stop.
  中文翻译：**OS 级信号或容器生命周期终止。** Docker `kill`、Kubernetes `kubectl delete pod`、systemd stop。

Properties a correct kill switch has:

> 正确终止开关的属性：

- The agent cannot set it to `off`. (Lives in a system the agent's credentials do not write.)
  中文翻译：Agent 不能将其设为 `off`。（位于 Agent 凭据不写的系统。）
- It is checked on every consequential action, not just at startup.
  中文翻译：在每个后果性动作上检查，不仅在启动时。
- When it is off, the agent does nothing externally observable, including logging to systems the agent can reach.
  中文翻译：关闭时，Agent 不做任何外部可观察的事，包括记录到 Agent 可达的系统。
- Re-enabling it is an explicit human action, not an automatic timeout.
  中文翻译：重新启用是显式人类动作，不是自动超时。

### Circuit breakers | 断路器

A circuit breaker pauses a specific pattern, not the whole agent. Classical shape (from the 2007 Nygard book, still current):

> 断路器暂停特定模式，而非整个 Agent。经典形状（来自 2007 年 Nygard 书，仍然当前）：

- **Closed**: action is allowed.
  中文翻译：**闭合**：动作允许。
- **Open**: action is blocked.
  中文翻译：**打开**：动作阻止。
- **Half-open**: after a cool-down, 1–3 probe attempts are allowed (default 1); success closes the breaker, any remaining failure re-opens it.
  中文翻译：**半开**：冷却后，允许 1-3 次探测（默认 1）；成功闭合断路器，任一剩余失败重新打开。

Agent-relevant triggers:

> Agent 相关触发器：

- Five identical tool calls in a row (repetitive loop).
  中文翻译：连续五次相同工具调用（重复循环）。
- Five consecutive failures on the same tool with different inputs (systemic failure).
  中文翻译：同一工具不同输入连续五次失败（系统性失败）。
- Rate of tool calls above a threshold (Lesson 13 velocity).
  中文翻译：工具调用速率超过阈值（第 13 课速度）。
- Specific tool invoked (e.g., `file.delete`) after an out-of-trust content read (Lesson 11).
  中文翻译：在不在信任的内容读取后调用特定工具（例如 `file.delete`）（第 11 课）。

### Canary tokens | 金丝雀 token

Canary tokens (also called honeytokens) are inputs the agent should never touch. Access is the alarm.

> 金丝雀 token（也称蜜罐 token）是 Agent 不应触及的输入。访问即警报。

Examples for agents:

> Agent 示例：

- A fake `AWS_SECRET_ACCESS_KEY` in the environment with no actual privilege. Exfiltration attempts are instantly attributable.
  中文翻译：环境中无实际特权的假 `AWS_SECRET_ACCESS_KEY`。泄露尝试立即可归因。
- A fake database record flagged with a known sentinel value. Any read or update of this record fires an alert.
  中文翻译：以已知哨兵值标记的假数据库记录。此记录的任何读或更新触发警报。
- A fake file in the workspace. Reads or edits of this file are suspicious.
  中文翻译：工作区中的假文件。此文件的读或编辑可疑。
- A fake memory entry injected at session start. If it appears in a later output, memory has been exfiltrated.
  中文翻译：会话开始时注入的假记忆条目。如果它出现在后续输出中，记忆已被泄露。

Canary design is specific to the workflow. A canary the agent has a legitimate reason to touch is noise.

> 金丝雀设计特定于工作流。Agent 有合法理由触及的金丝雀是噪声。

### Why layer statistical and hard limits | 为什么分层统计和硬限制

Statistical detectors (EWMA, CUSUM, z-score on tool-call rates) adapt to a moving baseline. That is a feature for legitimate drift and a bug for adversarial drift. A patient attacker can shift the baseline slowly enough that no alarm fires.

> 统计检测器（EWMA、CUSUM、工具调用速率 z 分数）适应移动基线。这是合法漂移的特性，是对抗漂移的 bug。耐心攻击者可足够缓慢地移动基线使无警报触发。

Hard constitutional limits (Lesson 17) do not bend. "Never email `secrets@`" as a constitutional rule is simpler, auditable, and not gameable by slow drift. The layering pattern: statistical detectors catch most noise, hard limits catch the attack that walked past the detector.

> 硬宪法限制（第 17 课）不弯折。"永不发邮件给 `secrets@`" 作为宪法规则更简单、可审计、不可被缓慢漂移博弈。分层模式：统计检测器捕获大多数噪声，硬限制捕获走过检测器的攻击。

### Quarantine via eBPF datapath redirect | 通过 eBPF 数据路径重定向隔离

Cilium's eBPF-based network policy can rewrite a quarantined pod's egress to a forensic honeypot at the kernel layer. Cilium's public benchmarks report sub-millisecond P99 datapath latency on TCP_RR; the wall-clock budget for *triggering* a quarantine in your cluster is dominated by how a policy update propagates from your control plane to the node (a few hundred milliseconds is realistic on Kubernetes with the operator pre-loaded; tail latency depends on cluster size and reconcile cadence). This gives you two things: the agent does not exfiltrate anything real, and the agent's behavior inside the honeypot is fully observed. Same pattern, different layer, as the canary token: the agent reveals intent by what it tries to do while contained.

> Cilium 的基于 eBPF 的网络策略可在内核层将隔离 pod 的出口重写到取证蜜罐。Cilium 公开基准报告 TCP_RR 上亚毫秒 P99 数据路径延迟；在集群中 *触发* 隔离的墙钟预算由策略更新如何从控制面传播到节点主导（在预加载 operator 的 Kubernetes 上几百毫秒现实；尾延迟取决于集群大小和协调节奏）。这给你两件事：Agent 不泄露任何真实东西，Agent 在蜜罐内的行为被完全观察。与金丝雀 token 相同模式、不同层：Agent 通过它在被包含时尝试做什么来揭示意图。

### What no detector catches | 没检测器能捕获什么

- **Semantic attacks that compose from allowed primitives.** Every individual action passes every detector; the composition is the problem. This is the Auto Mode composite failure from Lesson 10.
  中文翻译：**从允许原语组合的语义攻击。** 每个单独动作通过每个检测器；组合才是问题。这是第 10 课 Auto Mode 复合失败。
- **Attacks that include the detector as part of the payload.** If an agent reads a page that says "before you act, disable the canary" and the agent has the capability, the detector is compromised. Canary tokens should be in systems the agent cannot modify.
  中文翻译：**将检测器作为载荷一部分的攻击。** 如果 Agent 读页面说"行动前禁用金丝雀"且 Agent 有能力，检测器被攻破。金丝雀 token 应在 Agent 不能修改的系统中。

## Use It | 用框架实现

`code/main.py` simulates a short agent trajectory through three detectors. A kill switch held in an external dict; a circuit breaker that trips on five identical tool calls; a canary file whose read triggers an alert. Feeds in a synthetic trajectory: legitimate actions, repetitive loop, canary probe, and a kill-switch-triggered scenario where the agent's actions are halted.

> `code/main.py` 模拟通过三个检测器的短 Agent 轨迹。外部 dict 中的终止开关；在五次相同工具调用上跳闸的断路器；读取触发警报的金丝雀文件。喂入合成轨迹：合法动作、重复循环、金丝雀探测、终止开关触发场景下 Agent 动作被停止。

## Ship It | 产出物

`outputs/skill-tripwire-design.md` reviews a proposed detector stack for an agent deployment and flags gaps (missing kill switch, missing canary, circuit breaker threshold too loose).

> `outputs/skill-tripwire-design.md` 审查 Agent 部署的提议检测器栈并标记缺口（缺失终止开关、缺失金丝雀、断路器阈值太松）。

## Exercises | 练习题

1. Run `code/main.py`. Confirm the circuit breaker fires on turn 5 (fifth identical call) and the canary fires on turn 9 (fake-key read).
   中文翻译：运行 `code/main.py`。确认断路器在第 5 轮触发（第五次相同调用）金丝雀在第 9 轮触发（假键读取）。

2. Add a statistical detector: EWMA z-score on tool-call rate. Feed in a trajectory that drifts slowly and show the detector never fires. Now add a hard limit (no more than 50 tool calls in 10 minutes) and show the hard limit fires on the same trajectory.
   中文翻译：添加统计检测器：工具调用速率的 EWMA z 分数。喂入缓慢漂移的轨迹并展示检测器从不触发。现在添加硬限制（10 分钟内不超过 50 个工具调用）并展示硬限制在同一轨迹上触发。

3. Design a canary token set for a browser agent (Lesson 11). List at least three canaries and what each would detect.
   中文翻译：为浏览器 Agent（第 11 课）设计金丝雀 token 集。列出至少三个金丝雀及各检测什么。

4. Read the Cilium network-policy docs. Describe an egress-redirect quarantine flow concretely: which policy selector, which pod, which egress rewrite, which alert. What governs the wall-clock latency from "decide to quarantine" to "first redirected packet"?
   中文翻译：阅读 Cilium 网络策略文档。具体描述出口重定向隔离流：哪个策略选择器、哪个 pod、哪个出口重写、哪个警报。什么主导从"决定隔离"到"第一个重定向包"的墙钟延迟？

5. Define a re-enable procedure for a kill-switched agent. Who can re-enable? What must be documented? What must change about the agent before re-enable?
   中文翻译：为终止开关的 Agent 定义重新启用流程。谁可重新启用？必须文档化什么？重新启用前 Agent 必须改变什么？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Kill switch | "Off button" | Boolean outside the agent's edit surface; checked on every consequential action |
| 终止开关 | "关闭按钮" | Agent 编辑面之外的布尔值；每个后果性动作上检查 |
| Circuit breaker | "Pattern pause" | Action-specific trip on repetition, failure rate, or rate-limit |
| 断路器 | "模式暂停" | 在重复、失败率或速率限制上动作特定跳闸 |
| Canary token | "Honeytoken" | Bait the agent has no legitimate reason to touch; access fires an alert |
| 金丝雀 token | "蜜罐 token" | Agent 无合法理由触及的诱饵；访问触发警报 |
| Honeypot | "Forensic sandbox" | Redirected traffic / workspace where a quarantined agent is observed |
| 蜜罐 | "取证沙箱" | 隔离 Agent 被观察的重定向流量/工作区 |
| EWMA | "Moving average" | Exponentially weighted; adapts to drift (feature + bug) |
| EWMA | "移动平均" | 指数加权；适应漂移（特性 + bug） |
| CUSUM | "Cumulative sum" | Detects sustained shift from baseline |
| CUSUM | "累积和" | 检测相对基线的持续偏移 |
| Hard limit | "Constitutional rule" | Does not adapt; constant regardless of history |
| 硬限制 | "宪法规则" | 不适应；不论历史的常量 |
| Constitutional limit | "Always-true rule" | Tied to Lesson 17's constitution; cannot be edited by the agent |
| 宪法限制 | "始终为真的规则" | 绑定第 17 课的宪法；Agent 不能编辑 |

## Further Reading | 延伸阅读

- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — kill-switch and circuit-breaker framing for autonomous agents.
  中文翻译：自主 Agent 的终止开关和断路器框架。
- [Microsoft Agent Framework — HITL and oversight](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) — production governance patterns.
  中文翻译：生产治理模式。
- [OWASP LLM / Agentic Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — detection-and-response requirements.
  中文翻译：检测和响应要求。
- [Cilium — Network policy and eBPF](https://docs.cilium.io/en/stable/security/network/) — pod-level egress redirect and forensic honeypot patterns.
  中文翻译：pod 级出口重定向和取证蜜罐模式。
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) — hardcoded prohibitions as "constitutional limits".
  中文翻译：硬编码禁止作为"宪法限制"。
