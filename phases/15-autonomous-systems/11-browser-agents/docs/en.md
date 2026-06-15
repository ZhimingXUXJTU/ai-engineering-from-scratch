# Browser Agents and Long-Horizon Web Tasks | 浏览器 Agent 与长程 Web 任务

> ChatGPT agent (July 2025) merged Operator and deep research into one browser/terminal agent and set BrowseComp SOTA at 68.9%. OpenAI shut Operator down August 31, 2025 — consolidation at the product layer. Anthropic's Vercept acquisition moved Claude Sonnet on OSWorld from under 15% to 72.5%. WebArena-Verified (ServiceNow, ICLR 2026) fixed 11.3 percentage points of false-negative rate in the original WebArena and shipped the 258-task Hard subset. The numbers are real. So is the attack surface: OpenAI's head of preparedness stated publicly that indirect prompt injection into browser agents "is not a bug that can be fully patched." Documented 2025–2026 attacks: Tainted Memories (Atlas CSRF), HashJack (Cato Networks), and one-click hijacks in Perplexity Comet.

> **【中文解读】** ChatGPT agent（2025 年 7 月）将 Operator 和 deep research 合并为一个浏览器/终端 Agent 并以 68.9% 创下 BrowseComp SOTA。OpenAI 于 2025 年 8 月 31 日关闭 Operator——产品层整合。Anthropic 的 Vercept 收购让 Claude Sonnet 在 OSWorld 上从不到 15% 升到 72.5%。WebArena-Verified（ServiceNow，ICLR 2026）修正了原 WebArena 中 11.3 个百分点的假阴性率，发布了 258 任务 Hard 子集。数字是真实的，攻击面也是：OpenAI 准备度负责人公开表示对浏览器 Agent 的间接提示注入"不是可以完全修补的 bug"。已记录的 2025-2026 攻击：Tainted Memories（Atlas CSRF）、HashJack（Cato Networks）、Perplexity Comet 中的一键劫持。

> **【拓展：攻击与能力同构】** 浏览器 Agent 必须读取不受信任内容才能完成工作。它读取的任何内容都可能包含指令。它遵循的任何指令都可能偏离用户实际请求。防御（信任边界、分类器、工具允许列表、后果性动作 HITL）提高攻击成本并减少爆炸半径——它们不闭合该类别。这是与 Lob 定理相同的推理模式：Agent 不能证明下一个 token 安全；它只能设置让不安全 token 更可检测的系统。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, indirect prompt-injection attack surface model) | **语言:** Python（标准库，间接提示注入攻击面模型）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 01（长程 Agent）
**Time:** ~45 minutes | **时间:** ~45 分钟

## The Problem | 问题引入

> **【中文解读】** 浏览器 Agent 通过操作 Web 浏览器完成任务——导航、点击、输入、阅读。核心价值是通用性：任何有 Web 界面的服务都可以被操作，无需 API。代表性系统包括 Anthropic 的 Computer Use 和 Browser Use（开源）。挑战包括页面加载延迟、动态内容处理和 CAPTCHA 绕过。

> **【拓展：browser agents】** 浏览器 Agent 是 2025-2026 年的重要突破。与 API-first Agent 相比，浏览器 Agent 的优势是不需要服务提供商的支持——只要有网页就能操作。劣势是速度慢（每步需要渲染和截屏）和脆弱性（页面布局变化会破坏 Agent 的操作）。主要应用包括 Web 测试、数据采集和自动化工作流。

A browser agent is a long-horizon agent that reads untrusted content and takes consequential actions.

> 浏览器 Agent 是读取不受信任内容并采取后果性动作的长程 Agent。

Every page the agent visits is an input the user did not write. Every form on every page is a potential command channel. The 2025–2026 attack corpus shows this is not hypothetical: Tainted Memories lets an attacker bind malicious instructions to the agent's memory via a crafted page; HashJack hides commands in URL fragments the agent visits; Perplexity Comet hijacks hit in a single click.

> Agent 访问的每个页面都是用户未写的输入。每个页面上的每个表单都是潜在命令通道。2025-2026 攻击语料表明这不是假设性的：Tainted Memories 让攻击者通过精心制作的页面将恶意指令绑定到 Agent 的记忆；HashJack 在 Agent 访问的 URL 片段中隐藏命令；Perplexity Comet 一键劫持成功。

The defensive picture is uncomfortable. OpenAI's head of preparedness said the quiet part loud: indirect prompt injection "is not a bug that can be fully patched."

> 防御形势令人不安。OpenAI 准备度负责人公开表示：间接提示注入"不是一个可以完全修补的 bug"。

This is because the attack lives in the agent's reading-vs-acting boundary, which is architecturally fuzzy — every token the model reads could, in principle, be read as an instruction.

> 这是因为攻击位于 Agent 的读取-行动边界上，该边界在架构上模糊——模型读取的每个 token 原则上都可以被读为指令。

> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

This lesson names the attack surface, names the benchmark landscape (BrowseComp, OSWorld, WebArena-Verified), and models a minimal indirect-prompt-injection scenario so you can reason about real defenses in Lessons 14 and 18.

> 本课命名攻击面，命名基准景观（BrowseComp、OSWorld、WebArena-Verified），并建模最小间接提示注入场景，使你能在第 14 和 18 课中推理真实防御。

## The Concept | 核心概念

### The 2026 landscape, in one paragraph per system | 2026 全景，每系统一段

**ChatGPT agent (OpenAI).** Launched July 2025. Unifies Operator (browsing) and Deep Research (multi-hour research). Shut down the standalone Operator August 31, 2025. SOTA on BrowseComp at 68.9%; strong numbers on OSWorld and WebArena-Verified.

> **ChatGPT agent（OpenAI）。** 2025 年 7 月发布。统一 Operator（浏览）和 Deep Research（多小时研究）。2025 年 8 月 31 日关闭独立 Operator。BrowseComp SOTA 68.9%；OSWorld 和 WebArena-Verified 上有强数字。

**Claude Sonnet + Vercept (Anthropic).** Anthropic's Vercept acquisition focused on computer-use capabilities. Moved Claude Sonnet on OSWorld from <15% to 72.5%. Claude Computer Use ships as a tool API.

> **Claude Sonnet + Vercept（Anthropic）。** Anthropic 的 Vercept 收购聚焦于计算机使用能力。让 Claude Sonnet 在 OSWorld 上从 <15% 升到 72.5%。Claude Computer Use 作为工具 API 发布。

**Gemini 3 Pro with Browser Use (DeepMind).** Browser Use integration ships computer-use controls; FSF v3 (April 2026, Lesson 20) tracks autonomy in the ML R&D domain specifically.

> **Gemini 3 Pro 与 Browser Use（DeepMind）。** Browser Use 集成发布计算机使用控制；FSF v3（2026 年 4 月，第 20 课）专门跟踪 ML R&D 领域的自主性。

**WebArena-Verified (ServiceNow, ICLR 2026).** Fixes a well-documented problem: the original WebArena had ~11.3% false-negative rate (tasks marked failed that were actually solved). The Verified release re-grades with human-curated success criteria and adds a 258-task Hard subset (ICLR 2026 paper, openreview.net/forum?id=94tlGxmqkN).

> **WebArena-Verified（ServiceNow，ICLR 2026）。** 修复已充分记录的问题：原 WebArena 约 11.3% 假阴性率（标记为失败但实际解决的任务）。Verified 版本用人工策划的成功标准重新评分并添加 258 任务 Hard 子集（ICLR 2026 论文，openreview.net/forum?id=94tlGxmqkN）。

### BrowseComp vs OSWorld vs WebArena | BrowseComp vs OSWorld vs WebArena

| Benchmark | What it measures | Horizon |
|---|---|---|
| 基准 | 测量内容 | 时间线 |
| BrowseComp | Finding specific facts on the open web under time pressure | minutes |
| BrowseComp | 时间压力下在开放网络上查找特定事实 | 分钟 |
| OSWorld | Agent operating a full desktop (mouse, keyboard, shell) | tens of minutes |
| OSWorld | Agent 操作完整桌面（鼠标、键盘、shell） | 数十分钟 |
| WebArena-Verified | Transactional web tasks in simulated sites | minutes |
| WebArena-Verified | 模拟站点中的事务性 Web 任务 | 分钟 |
| Hard subset | WebArena-Verified tasks with multi-page state transitions | tens of minutes |
| Hard 子集 | 带多页状态转换的 WebArena-Verified 任务 | 数十分钟 |

Different axes. A high BrowseComp score says the agent finds facts; it does not say the agent can book a flight. The OSWorld score is closer to "does it work on my desktop." WebArena-Verified is closer to "can it finish a flow." Any production decision needs the benchmark that matches the task distribution.

> 不同轴。高 BrowseComp 分数表明 Agent 找事实；不表明 Agent 能订机票。OSWorld 分数更接近"它在我的桌面上能用"。WebArena-Verified 更接近"它能完成流程"。任何生产决策需要匹配任务分布的基准。

### The attack surface, named | 攻击面，命名

1. **Indirect prompt injection.** Untrusted page content contains instructions. The agent reads them. The agent executes them. Public examples: 2024 Kai Greshake et al., 2025 Tainted Memories paper, 2026 HashJack (Cato Networks).
   中文翻译：**间接提示注入。** 不受信任页面内容包含指令。Agent 读取它们。Agent 执行它们。公开示例：2024 Kai Greshake 等人、2025 Tainted Memories 论文、2026 HashJack（Cato Networks）。
2. **URL fragment / query injection.** The `#fragment` or query string of a crawled URL contains commands. Never rendered visibly; still inside the agent's context.
   中文翻译：**URL 片段/查询注入。** 爬取 URL 的 `#fragment` 或查询字符串包含命令。从不可见渲染；仍在 Agent 上下文中。
3. **Memory-binding attacks.** Page instructs the agent to write a persistent memory (Lesson 12 covers durable state). Next session, the memory fires the payload with no visible trigger.
   中文翻译：**记忆绑定攻击。** 页面指示 Agent 写持久记忆（第 12 课覆盖持久状态）。下次会话，记忆在无可见触发器的情况下触发载荷。
4. **CSRF-shaped attacks on authenticated sessions.** Tainted Memories class: agent is logged in somewhere; attacker's page issues state-changing requests the agent executes with the user's cookies.
   中文翻译：**对认证会话的 CSRF 形攻击。** Tainted Memories 类：Agent 登录某处；攻击者的页面发出 Agent 用用户 cookie 执行的状态变更请求。
5. **One-click hijack.** A visually innocuous button rides a payload the agent follows. Comet class.
   中文翻译：**一键劫持。** 视觉上无害的按钮承载 Agent 遵循的载荷。Comet 类。
6. **Content-Security-Policy holes in the agent's host surface.** The rendering and tool layers can themselves be attack vectors; the browser-in-a-browser-agent stack is wide.
   中文翻译：**Agent 宿主面上的 CSP 漏洞。** 渲染和工具层本身可以是攻击向量；浏览器 Agent 中的浏览器栈很宽。

### Why "not fully patchable" | 为什么"不可完全修补"

The attack is isomorphic to the agent's capability.

> 攻击与 Agent 的能力是同构的。

The agent must read untrusted content to do its job. Any content the agent reads could contain instructions. Any instructions the agent follows could be misaligned with the user's actual request. Defenses (trust boundaries, classifiers, tool allowlists, HITL on consequential actions) raise the cost of the attack and reduce its blast radius. They do not close the class.

> Agent 必须读取不受信任内容才能完成工作。Agent 读取的任何内容都可能包含指令。Agent 遵循的任何指令都可能偏离用户实际请求。防御（信任边界、分类器、工具允许列表、后果性动作 HITL）提高攻击成本并减少爆炸半径。它们不闭合该类别。

This is the same reasoning pattern as Lob's theorem (Lesson 8): the agent cannot prove the next token is safe; it can only set up a system where unsafe tokens are more detectable.

> 这与 Lob 定理（第 8 课）相同推理模式：Agent 不能证明下一个 token 安全；它只能设置让不安全 token 更可检测的系统。

### Defense posture that actually ships | 实际出货的防御姿态

- **Read / write boundary.** Reading is never consequential. Writing (submitting a form, posting content, calling a tool with side effects) requires fresh human approval if the initiating content came from outside the trust boundary.
  中文翻译：**读/写边界。** 读取从无后果。写入（提交表单、发布内容、调用带副作用的工具）在发起内容来自信任边界外时需要新鲜人类批准。
- **Tool allowlist per task.** The agent can browse; it cannot initiate a wire transfer unless that tool was explicitly enabled for the task. Lesson 13 covers budgets.
  中文翻译：**每任务工具允许列表。** Agent 可浏览；除非该工具为任务明确启用，否则不能发起电汇。第 13 课覆盖预算。
- **Session isolation.** Browser agent sessions run with scoped credentials only. No production auth, no personal email. Logs of every HTTP request retained for audit.
  中文翻译：**会话隔离。** 浏览器 Agent 会话仅用范围凭据运行。无生产认证、无个人邮箱。每个 HTTP 请求的日志保留以供审计。
- **Content sanitizer.** Fetched HTML is stripped of known-bad patterns before being concatenated into the model context. (Reduces the easy attacks; does not stop sophisticated payloads.)
  中文翻译：**内容消毒器。** 抓取的 HTML 在拼接到模型上下文前剥离已知坏模式。（减少简单攻击；不停复杂载荷。）
- **HITL on consequential actions.** Propose-then-commit pattern (Lesson 15).
  中文翻译：**后果性动作 HITL。** Propose-then-commit 模式（第 15 课）。
- **Canary tokens on memory.** If a memory entry fires, the user sees it (Lesson 14).
  中文翻译：**记忆上金丝雀 token。** 如果记忆条目触发，用户看到它（第 14 课）。

## Use It | 用框架实现

`code/main.py` models a tiny browser-agent run against three synthetic pages. One page is benign, one has a direct prompt-injection blob in visible text, one has a URL-fragment injection (not visible but inside the agent's context). The script shows (a) what a naïve agent would do, (b) what a read/write boundary catches, (c) what a sanitizer catches, (d) what neither catches.

> `code/main.py` 建模针对三个合成页面的小浏览器 Agent 运行。一页良性，一页有可见文本中的直接提示注入块，一页有 URL 片段注入（不可见但在 Agent 上下文内）。脚本展示 (a) 朴素 Agent 会做什么、(b) 读/写边界捕获什么、(c) 消毒器捕获什么、(d) 两者都不捕获什么。

## Ship It | 产出物

`outputs/skill-browser-agent-trust-boundary.md` scopes a proposed browser-agent deployment: which trust zones it touches, what it is authorized to write, and which defenses must be in place before the first run.

> `outputs/skill-browser-agent-trust-boundary.md` 范围化提议的浏览器 Agent 部署：它触及哪些信任区、被授权写什么、首次运行前必须就位哪些防御。

## Exercises | 练习题

1. Run `code/main.py`. Identify which attack the sanitizer catches but the read/write boundary does not, and which attack only the read/write boundary catches.
   中文翻译：运行 `code/main.py`。识别消毒器捕获但读/写边界不捕获的攻击，以及只有读/写边界捕获的攻击。

2. Extend the sanitizer to detect one class of HashJack-style URL-fragment injection. Measure the false-positive rate on benign URLs with legitimate fragments.
   中文翻译：扩展消毒器检测一类 HashJack 风格 URL 片段注入。在带合法片段的良性 URL 上测量假阳性率。

3. Pick one real browser-agent workflow you know (e.g., "book a flight"). List every read and every write. Mark which writes need HITL and why.
   中文翻译：选一个你了解的真实浏览器 Agent 工作流（例如"订机票"）。列出每个读和每个写。标记哪些写需要 HITL 及原因。

4. Read the WebArena-Verified ICLR 2026 paper. Identify one category of task where the original WebArena's scoring was unreliable and explain how the Verified subset resolves it.
   中文翻译：阅读 WebArena-Verified ICLR 2026 论文。识别原 WebArena 评分不可靠的一类任务，解释 Verified 子集如何解决它。

5. Design a memory canary for a browser-agent setting. What would you store, where, and what triggers the alarm?
   中文翻译：为浏览器 Agent 设置设计记忆金丝雀。你会存储什么、在哪、什么触发警报？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Indirect prompt injection | "Bad page text" | Untrusted content in a page the agent reads contains instructions the agent executes |
| 间接提示注入 | "坏页面文本" | Agent 读取的页面中不受信任内容包含 Agent 执行的指令 |
| Tainted Memories | "Memory attack" | Agent writes an attacker-supplied instruction to durable memory; triggered next session |
| Tainted Memories | "记忆攻击" | Agent 将攻击者提供的指令写入持久记忆；下次会话触发 |
| HashJack | "URL fragment attack" | Payload hidden in URL fragment / query string is in the agent's context but not visibly rendered |
| HashJack | "URL 片段攻击" | 隐藏在 URL 片段/查询字符串中的载荷在 Agent 上下文中但不可见渲染 |
| One-click hijack | "Bad button" | Visible affordance rides a follow-on payload the agent executes |
| 一键劫持 | "坏按钮" | 可见功能承载 Agent 执行的后续载荷 |
| BrowseComp | "Web search benchmark" | Finding specific facts on the open web; minute-scale horizon |
| BrowseComp | "Web 搜索基准" | 在开放网络上查找特定事实；分钟级时间线 |
| OSWorld | "Desktop benchmark" | Full OS control; multi-step GUI tasks |
| OSWorld | "桌面基准" | 完整 OS 控制；多步 GUI 任务 |
| WebArena-Verified | "Fixed web-task benchmark" | ServiceNow's regraded WebArena with Hard subset |
| WebArena-Verified | "修复的 Web 任务基准" | ServiceNow 重新评分的 WebArena 带 Hard 子集 |
| Read/write boundary | "Side-effect gate" | Reading never consequential; writing requires fresh approval if content is out-of-trust |
| 读/写边界 | "副作用门" | 读取从无后果；内容不在信任内时写入需新鲜批准 |

## Further Reading | 延伸阅读

- [OpenAI — Introducing ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/) — merge of Operator and deep research; BrowseComp SOTA.
  中文翻译：Operator 与 deep research 合并；BrowseComp SOTA。
- [OpenAI — Computer-Using Agent](https://openai.com/index/computer-using-agent/) — the Operator lineage and the architecture that became ChatGPT agent.
  中文翻译：Operator 血统和成为 ChatGPT agent 的架构。
- [Zhou et al. — WebArena](https://webarena.dev/) — the original benchmark.
  中文翻译：原始基准。
- [WebArena-Verified (OpenReview)](https://openreview.net/forum?id=94tlGxmqkN) — ICLR 2026 fixed-subset paper.
  中文翻译：ICLR 2026 修复子集论文。
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — includes attack-surface discussion for computer-use agents.
  中文翻译：包括计算机使用 Agent 的攻击面讨论。
