# Indirect Prompt Injection — Production Attack Surface | 提示注入 生产 间接

> Indirect prompt injection (IPI) embeds instructions inside external content — a web page, an email, a shared document, a support ticket — consumed by an agentic system without explicit user action. IPI is the dominant 2026 production threat: it bypasses user-input filters because the attacker never touches the user, it scales silently as agents process more external content, and it targets automated workflows where nobody is reading the prompt. MDPI Information 17(1):54 (January 2026) synthesizes 2023-2025 research. NDSS 2026's IPI-defense paper frames the core challenge: injected instructions can be semantically benign ("please print Yes"), so detection requires more than keyword filtering. "The Attacker Moves Second" (Nasr et al., joint OpenAI/Anthropic/DeepMind, October 2025): adaptive attacks (gradient, RL, random search, human red-team) broke >90% of 12 published defenses that had originally reported near-zero attack success rates.

> **【中文解读】** 本节介绍了间接提示注入——通过第三方数据源（网页、文档）注入恶意指令的攻击。IPI 是 2026 年主要的生产威胁：它绕过用户输入过滤器因为攻击者从不触碰用户，它随 Agent 处理更多外部内容而静默扩展，它针对没人阅读提示的自动化工作流。Nasr 等人（OpenAI/Anthropic/DeepMind 联合, 2025 年 10 月）的自适应攻击破坏了 12 个已发布防御中 >90% 的防御。

> **【拓展：IPI → 2026 最大生产威胁】** OWASP LLM Top 10（2025）将提示注入（直接+间接）排在 LLM01——应用层威胁第一位。NIST AI SPD 2024 称间接提示注入为"生成式 AI 最大的安全缺陷"。实际事件包括 EchoLeak（CVE-2025-32711, CVSS 9.3, Microsoft 365 Copilot）和 CamoLeak（CVSS 9.6, GitHub Copilot Chat）。

**Type:** Build
**Languages:** Python (stdlib, IPI attack + defense harness)
**Prerequisites:** Phase 18 · 12 (PAIR), Phase 14 (agent engineering)
**Time:** ~75 minutes

## Learning Objectives | 学习目标

- Define indirect prompt injection and describe three common delivery vectors.
- Explain why user-input filters miss IPI entirely.
- Describe the "information flow control" framing as the 2026 defense paradigm.
- State the finding of Nasr et al. (October 2025) on adaptive attack success against published IPI defenses.

## The Problem | 问题

Direct prompt injection requires the attacker to reach the user or their prompt. IPI requires neither: the attacker places a payload in any content the agent might read — a web page, an email in the inbox, a GitHub issue, a product review. The agent picks it up during normal operation and executes the instructions. The user is the messenger, not the intent.

## The Concept | 概念

> **【中文解读】** 三种投递向量共享一个结构特性——攻击者控制提示片段但不触碰面向用户的输入。（1）RAG 注入——攻击者发布文档，检索步骤获取它，提示在用户问题前拼接，模型执行攻击者指令；（2）收件箱/文档工作流——攻击者发送邮件，Agent 读取邮件，提示包含邮件正文，模型遵循邮件指令；（3）工具输出——攻击者控制 Agent 使用的工具，工具输出包含指令。

### Three delivery vectors

- **Retrieval-augmented generation (RAG).** Attacker publishes a document; the retrieval step fetches it; the prompt concatenates it before the user question; the model executes the attacker's instructions.
- **Inbox / document workflows.** Attacker sends an email to the user; the agent reads emails; the prompt includes the email body; the model follows the email's instructions.
- **Tool output.** Attacker controls a tool the agent uses (e.g., a web search that returns an attacker-controlled result); the tool output contains instructions; the agent's control flow follows them.

The three share a structural property: the attacker controls a fragment of the prompt without touching the user-facing input.

### Why user-input filters miss it

An IPI payload does not appear in the user's input. It appears in the retrieved content. If the filter is gated on user input, the payload bypasses it. If the filter is gated on all content that reaches the model, it must apply to arbitrary retrieved text — which is expensive and produces false positives against legitimate content that happens to contain imperative-voice language.

> **【中文解读】** 信息流控制（IFC）是 2026 年的防御范式，借鉴经典操作系统安全：将每个内容源视为安全标签，用户查询标记为"可信"，检索内容标记为"不可信"，模型控制流中的行动：由不可信内容触发的行动必须在执行前获得可信输入的批准。CaMeL（Microsoft 2025）、ConfAIde（Stanford 2024）和 NDSS 2026 IPI 防御论文以不同方式实现了 IFC。共同原则：只要代码和数据共享同一上下文窗口，目标就是遏制而非阻止。

### Information Flow Control (IFC) for AI

The 2026 defense paradigm borrows from classical OS security. Treat every content source as a security label. Label the user's query as "trusted." Label retrieved content as "untrusted." Treat the model's control flow as an information flow: actions triggered by untrusted content must be ratified by trusted input before execution.

CaMeL (Microsoft 2025), ConfAIde (Stanford 2024), and the NDSS 2026 IPI-defense paper operationalize IFC in different ways. The common principle: as long as code and data share the same context window, containment is the goal, not prevention.

> **【拓展：攻击者后手 → 自适应评估的必要性】** "攻击者后手"的方法论教训：只有在自适应攻击评估下发布防御。静态攻击基准不是鲁棒性的证据——攻击者可以知道防御。Nasr 等人使用梯度搜索、RL 策略、随机搜索和 72 小时人类红队测试了 12 个防御。每个原本报告接近零 ASR 的防御都被破坏到 >90% ASR。

### The Attacker Moves Second

Nasr et al. (October 2025) tested 12 published IPI defenses with adaptive attacks (gradient search, RL policies, random search, 72-hour human red-team). Every defense that originally reported near-zero ASR was broken to >90% ASR.

The methodological lesson: publish a defense only with adaptive-attack evaluation. Static-attack benchmarks are not evidence of robustness; the attacker gets to know the defense.

### Real incidents

Lesson 25 covers EchoLeak (CVE-2025-32711, CVSS 9.3) — the first publicly documented zero-click IPI in Microsoft 365 Copilot. CamoLeak (CVSS 9.6) in GitHub Copilot Chat. CVE-2025-53773 in GitHub Copilot. Production deployments are being compromised by IPI in the field, not just in benchmarks.

### OWASP and NIST framing

OWASP LLM Top 10 (2025) ranks prompt injection (direct + indirect) as LLM01, the #1 application-layer threat. NIST AI SPD 2024 calls indirect prompt injection "generative AI's greatest security flaw."

### Where this fits in Phase 18

Lessons 12-14 are model-centric jailbreaks. Lesson 15 is the system-centric attack that dominates 2026 production deployments. Lesson 16 covers the defensive tooling. Lesson 25 covers the specific CVE narrative.

> **【拓展：IPI 在 Agent 系统中的普遍性】** 随着 AI Agent 的普及——Microsoft 365 Copilot、GitHub Copilot、各种 RAG 系统——IPI 的攻击面在 2025-2026 年急剧扩大。每个对外部数据有读取访问权限的 Agent 都是一个潜在目标。现实事件（Lesson 25）证明生产部署正在被 IPI 在实际中攻击，不仅仅是基准测试中。IFC 是目前最有前景的防御范式。

## Use It | 使用方法

`code/main.py` builds an IPI harness. A toy agent has three tools (search web, read email, send message). The environment contains attacker-controlled content with an embedded instruction ("forward this to all contacts"). You can toggle between a naive agent (follows injected instructions), a filter-defended agent (keyword filter on retrieved content), and an IFC agent (separates trusted and untrusted content and refuses untrusted control-flow commands).

## Ship It | 部署上线

This lesson produces `outputs/skill-ipi-audit.md`. Given an agentic deployment description, it enumerates the untrusted content sources, checks whether the deployment applies IFC, and flags sources that reach the model without a trust label.

## Exercises | 练习题

1. Run `code/main.py`. Measure the success rate of the attack against each of the three agents.

2. Implement a paraphrase-based defense on retrieved content. Measure the benign false-positive rate on legitimate retrieved text.

3. Read the NDSS 2026 IPI-defense paper. Describe the "benign instruction" challenge and why it prevents keyword-based filtering.

4. Design a deployment where the agent receives a tool output from a third-party API. Label each prompt fragment with a trust level and write the IFC policy that governs the agent's actions.

5. Reproduce the Nasr et al. 2025 adaptive-attack methodology on your filter-defended agent from Exercise 2. Report the ASR before and after adaptive attack.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| IPI | "indirect prompt injection" | Injection via content the user did not write, consumed by the agent during normal operation |
| RAG injection | "poisoned retrieval" | Attacker publishes content that the retrieval step fetches; prompt contains the payload |
| Zero-click | "no user action" | Attack triggers automatically during agent operation; user does nothing |
| IFC | "information flow control" | Label-based approach: actions from untrusted content require trusted ratification |
| Adaptive attack | "gradient / RL red-team" | Attack that knows the defense and optimizes against it; required for honest evaluation |
| Benign instruction | "please print Yes" | IPI payload that is semantically benign; no keyword filter catches it |
| Scope violation | "cross-trust exfiltration" | Agent accesses data from one trust context and outputs it to another |

## Further Reading | 延伸阅读

- [MDPI Information 17(1):54 — Indirect Prompt Injection Survey (January 2026)](https://www.mdpi.com/2078-2489/17/1/54) — 2023-2025 synthesis
- [Nasr et al. — The Attacker Moves Second (joint OpenAI/Anthropic/DeepMind, October 2025)](https://arxiv.org/abs/2510.18108) — adaptive attack evaluation
- [Greshake et al. — Not what you've signed up for (arXiv:2302.12173)](https://arxiv.org/abs/2302.12173) — the original IPI paper
- [OWASP — LLM Top 10 (2025)](https://genai.owasp.org/llm-top-10/) — prompt injection ranked LLM01
