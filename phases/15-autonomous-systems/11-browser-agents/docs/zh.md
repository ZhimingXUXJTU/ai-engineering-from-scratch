# 浏览器 Agent 和长程 Web 任务

> ChatGPT agent（2025 年 7 月）将 Operator 和深度研究合并为一个浏览器/终端 Agent，在 BrowseComp 上达到 SOTA 68.9%。OpenAI 在 2025 年 8 月 31 日关闭了 Operator——产品层的整合。Anthropic 收购 Vercept 使 Claude Sonnet 在 OSWorld 上从不到 15% 提升到 72.5%。WebArena-Verified（ServiceNow，ICLR 2026）修复了原始 WebArena 中 11.3 个百分点的假阴性率，并发布了 258 个任务的 Hard 子集。这些数字是真实的。攻击面也是如此：OpenAI 准备性负责人公开表示，对浏览器 Agent 的间接提示注入"不是一个可以完全修补的漏洞"。已记录的 2025-2026 年攻击：Tainted Memories（Atlas CSRF）、HashJack（Cato Networks）以及 Perplexity Comet 中的一次点击劫持。

**类型：** 学习
**语言：** Python（标准库，间接提示注入攻击面模型）
**前置条件：** Phase 15 · 10（权限模式），Phase 15 · 01（长程 Agent）
**时间：** ~45 分钟

## 问题引入

> **【中文解读】** 浏览器 Agent 通过操作 Web 浏览器完成任务——导航、点击、输入、阅读。核心价值是通用性：任何有 Web 界面的服务都可以被操作，无需 API。代表性系统包括 Anthropic 的 Computer Use 和 Browser Use（开源）。挑战包括页面加载延迟、动态内容处理和 CAPTCHA 绕过。

> **【拓展：browser agents】** 浏览器 Agent 是 2025-2026 年的重要突破。与 API-first Agent 相比，浏览器 Agent 的优势是不需要服务提供商的支持——只要有网页就能操作。劣势是速度慢（每步需要渲染和截屏）和脆弱性（页面布局变化会破坏 Agent 的操作）。主要应用包括 Web 测试、数据采集和自动化工作流。

浏览器 Agent 是一个读取不受信任内容并采取有后果行动的长程 Agent。Agent 访问的每个页面都是用户没有编写的输入。每个页面上的每个表单都是潜在的命令通道。2025-2026 年的攻击语料库表明这不是假设的：Tainted Memories 让攻击者通过精心制作的页面将恶意指令绑定到 Agent 的记忆中；HashJack 在 Agent 访问的 URL 片段中隐藏命令；Perplexity Comet 的一次点击劫持命中了。

防御图景令人不安。OpenAI 准备性负责人说出了安静的事实：间接提示注入"不是一个可以完全修补的漏洞"。这是因为攻击存在于 Agent 的阅读-行动边界中，这在架构上是模糊的——模型读取的每个 Token 原则上都可以被读取为指令。

> **【中文解读】** 本节介绍了 AI Agent 的核心概念和实现方法。Agent 是 LLM 驱动的自主系统，能够观察环境、思考决策、执行行动并循环迭代直到完成目标。

本课命名了攻击面、命名了基准全景（BrowseComp、OSWorld、WebArena-Verified），并建模了一个最小的间接提示注入场景，以便你能在第 14 和 18 课中推理真实的防御。

## 核心概念

### 2026 年全景，每个系统一段话

**ChatGPT agent（OpenAI）。** 2025 年 7 月发布。统一了 Operator（浏览）和深度研究（多小时研究）。2025 年 8 月 31 日关闭了独立的 Operator。BrowseComp SOTA 68.9%；在 OSWorld 和 WebArena-Verified 上有强劲数字。

**Claude Sonnet + Vercept（Anthropic）。** Anthropic 收购 Vercept 专注于计算机使用能力。将 Claude Sonnet 在 OSWorld 上从 <15% 提升到 72.5%。Claude Computer Use 作为工具 API 发布。

**带 Browser Use 的 Gemini 3 Pro（DeepMind）。** Browser Use 集成发布计算机使用控制；FSF v3（2026 年 4 月，第 20 课）专门跟踪 ML 研发领域的自主性。

**WebArena-Verified（ServiceNow，ICLR 2026）。** 修复了一个有充分记录的问题：原始 WebArena 有约 11.3% 的假阴性率（标记为失败但实际已解决的任务）。Verified 版本用人工策划的成功标准重新评分，并添加了 258 个任务的 Hard 子集（ICLR 2026 论文，openreview.net/forum?id=94tlGxmqkN）。

### BrowseComp vs OSWorld vs WebArena

| 基准 | 测量什么 | 时间范围 |
|---|---|---|
| BrowseComp | 在时间压力下在开放网络上查找特定事实 | 分钟级 |
| OSWorld | Agent 操作完整桌面（鼠标、键盘、Shell） | 数十分钟 |
| WebArena-Verified | 模拟站点中的事务性 Web 任务 | 分钟级 |
| Hard 子集 | 具有多页面状态转换的 WebArena-Verified 任务 | 数十分钟 |

不同的轴。高 BrowseComp 分数说明 Agent 能找到事实；不说明 Agent 能订机票。OSWorld 分数更接近"它能在我的桌面上工作"。WebArena-Verified 更接近"它能完成一个流程"。任何生产决策都需要匹配任务分布的基准。

### 攻击面，逐个命名

1. **间接提示注入。** 不受信任的页面内容包含指令。Agent 读取它们。Agent 执行它们。公开示例：2024 年 Kai Greshake 等人、2025 年 Tainted Memories 论文、2026 年 HashJack（Cato Networks）。
2. **URL 片段/查询注入。** 爬取 URL 的 `#fragment` 或查询字符串包含命令。从不在视觉上渲染；仍在 Agent 的上下文中。
3. **记忆绑定攻击。** 页面指示 Agent 写入持久记忆（第 12 课涵盖持久状态）。下次会话，记忆在无可见触发器的情况下激活载荷。
4. **已认证会话上的 CSRF 形状攻击。** Tainted Memories 类：Agent 在某处已登录；攻击者页面发出状态变更请求，Agent 使用用户的 cookies 执行。
5. **一次点击劫持。** 视觉上无害的按钮承载 Agent 跟随的载荷。Comet 类。
6. **Agent 宿主面中的内容安全策略漏洞。** 渲染和工具层本身可以是攻击向量；浏览器中浏览器 Agent 的栈是很宽的。

### 为什么"不可完全修补"

攻击与 Agent 的能力同构。Agent 必须读取不受信任的内容才能完成工作。Agent 读取的任何内容都可能包含指令。Agent 跟随的任何指令都可能偏离用户的实际请求。防御（信任边界、分类器、工具允许列表、有后果行动的 HITL）提高了攻击成本并减少了其爆炸半径。它们不闭合这个类别。

这与 Lob 定理（第 8 课）的推理模式相同：Agent 无法证明下一个 Token 是安全的；它只能建立一个使不安全 Token 更可检测的系统。

### 实际可部署的防御姿态

- **读/写边界。** 读取永远不会有后果。写入（提交表单、发布内容、调用有副作用的工具）在发起内容来自信任边界之外时需要新的人类批准。
- **每任务工具允许列表。** Agent 可以浏览；它不能发起电汇，除非该工具已为任务显式启用。第 13 课涵盖预算。
- **会话隔离。** 浏览器 Agent 会话仅使用范围限定的凭证。没有生产认证，没有个人邮件。每个 HTTP 请求的日志保留用于审计。
- **内容净化器。** 获取的 HTML 在被拼接到模型上下文之前剥离已知的不良模式。（减少简单攻击；不阻止复杂载荷。）
- **有后果行动的 HITL。** 先提议后提交模式（第 15 课）。
- **记忆上的金丝雀 Token。** 如果记忆条目激活，用户能看到它（第 14 课）。

## 用框架实现

`code/main.py` 建模一个微型浏览器 Agent 运行，面对三个合成页面。一个页面是良性的，一个在可见文本中有直接的提示注入块，一个有 URL 片段注入（不可见但在 Agent 的上下文中）。脚本展示 (a) 一个天真的 Agent 会做什么，(b) 读/写边界捕获什么，(c) 净化器捕获什么，(d) 两者都不捕获什么。

## 产出物

`outputs/skill-browser-agent-trust-boundary.md` 规划一个提议的浏览器 Agent 部署：它触及哪些信任区域、被授权写入什么，以及首次运行前必须部署哪些防御。

## 练习题

1. 运行 `code/main.py`。识别净化器捕获但读/写边界未捕获的攻击，以及只有读/写边界捕获的攻击。
   *思考并实践此练习*

2. 扩展净化器以检测一类 HashJack 式 URL 片段注入。测量带有合法片段的良性 URL 上的误报率。
   *思考并实践此练习*

3. 选择一个你了解的真实浏览器 Agent 工作流（例如，"订机票"）。列出每次读取和每次写入。标记哪些写入需要 HITL 以及原因。
   *思考并实践此练习*

4. 阅读 WebArena-Verified ICLR 2026 论文。识别原始 WebArena 评分不可靠的一个任务类别，并解释 Verified 子集如何解决它。
   *思考并实践此练习*

5. 为浏览器 Agent 设置设计一个记忆金丝雀。你会存储什么，存在哪里，什么触发警报？
   *思考并实践此练习*

## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|---|---|---|
| 间接提示注入 (Indirect Prompt Injection) | "坏的页面文本" | Agent 读取的页面中不受信任的内容包含 Agent 执行的指令 |
| Tainted Memories | "记忆攻击" | Agent 将攻击者提供的指令写入持久记忆；下次会话触发 |
| HashJack | "URL 片段攻击" | 隐藏在 URL 片段/查询字符串中的载荷在 Agent 的上下文中但不可见渲染 |
| 一次点击劫持 (One-click Hijack) | "坏的按钮" | 可见的交互元素承载 Agent 执行的后续载荷 |
| BrowseComp | "Web 搜索基准" | 在开放网络上查找特定事实；分钟级时间范围 |
| OSWorld | "桌面基准" | 完整操作系统控制；多步骤 GUI 任务 |
| WebArena-Verified | "修复后的 Web 任务基准" | ServiceNow 重新评分的带 Hard 子集的 WebArena |
| 读/写边界 (Read/Write Boundary) | "副作用门控" | 读取永远无后果；内容来自信任外时写入需要新批准 |

## 延伸阅读

- [OpenAI — 介绍 ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/) — Operator 和深度研究的合并；BrowseComp SOTA。
- [OpenAI — 计算机使用 Agent](https://openai.com/index/computer-using-agent/) — Operator 血统和成为 ChatGPT agent 的架构。
- [Zhou 等人 — WebArena](https://webarena.dev/) — 原始基准。
- [WebArena-Verified (OpenReview)](https://openreview.net/forum?id=94tlGxmqkN) — ICLR 2026 修复子集论文。
- [Anthropic — 实践中测量 Agent 自主性](https://www.anthropic.com/research/measuring-agent-autonomy) — 包含计算机使用 Agent 的攻击面讨论。
