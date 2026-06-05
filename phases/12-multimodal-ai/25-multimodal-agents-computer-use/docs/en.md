# Multimodal Agents and Computer-Use (Capstone) | 多模态 Agent 与计算机使用

> The 2026 frontier product is a multimodal agent that reads screenshots, clicks buttons, navigates web UIs, fills forms, and completes workflows end-to-end. SeeClick and CogAgent (2024) proved the GUI-grounding primitive. Ferret-UI added mobile. ChartAgent introduced visual tool-use for charts. VisualWebArena and AgentVista (2026) are the benchmarks the frontier chases — and even Gemini 3 Pro and Claude Opus 4.7 score ~30% on AgentVista's hard tasks. This capstone pulls together every thread of Phase 12: perception (high-res VLM), reasoning (LLM with tool use), grounding (coordinate output), long-horizon memory, and evaluation.

> **【中文解读】** 2026 年的前沿产品是能读截图、点按钮、导航网页、填表单、端到端完成工作流的多模态 Agent。SeeClick 和 CogAgent 证明了 GUI 定位原语可行，Ferret-UI 扩展到移动端，ChartAgent 引入视觉工具调用。但在 AgentVista 困难任务上，即使是 Gemini 3 Pro 和 Claude Opus 4.7 也仅约 30% 通过率——这是 Phase 12 的收官课程，整合感知、推理、定位、长期记忆与评估。

**Type:** Capstone
**Languages:** Python (stdlib, action schema + agent loop skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 12 · 09 (Qwen-VL JSON), Phase 14 (Agent Engineering)
**Time:** ~240 minutes

## Learning Objectives | 学习目标

- Design a multimodal agent loop: perceive → reason → act → observe → repeat.
  设计多模态 Agent 循环：感知 → 推理 → 行动 → 观察 → 重复。
- Build a GUI grounding output schema (click coordinates, type text, scroll, drag) the VLM can emit as JSON.
  构建 GUI 定位输出模式（点击坐标、输入文字、滚动、拖拽），VLM 以 JSON 格式输出。
- Compare screenshot-only agents vs accessibility-tree agents vs hybrid agents.
  对比纯截图 Agent、无障碍树 Agent 和混合 Agent。
- Set up a multimodal agent benchmark evaluation on a small VisualWebArena slice.
  在 VisualWebArena 小规模子集上搭建多模态 Agent 基准评估。

## The Problem | 问题定义

> **【中文解读】** 以订票场景为例：Agent 需要截图浏览器页面，解析截图+URL+目标生成计划，输出结构化动作（点击坐标、输入文字、滚动、选择），在浏览器上执行动作，观察新状态，循环直到任务完成。每一步都是一次多模态 VLM 调用，错误会在步骤间累积，因此恢复机制至关重要。

A booking-site workflow: "find me a flight to Tokyo for April 15, aisle seat under $800, book it."

> 一个订票工作流："帮我找 4 月 15 日飞东京的航班，靠走道，$800 以下，预订。"

A multimodal agent needs to:

> 多模态 Agent 需要：

1. Take a screenshot of the browser.
   中文翻译：截取浏览器屏幕截图。
2. Parse the screenshot + URL + goal into a plan.
   中文翻译：解析截图 + URL + 目标，生成计划。
3. Emit a structured action: click (at x,y), type "Tokyo" (at element E), scroll down, select (radio button).
   中文翻译：输出结构化动作：点击（x,y）、输入"Tokyo"（元素 E）、向下滚动、选择（单选按钮）。
4. Apply the action to the browser.
   中文翻译：在浏览器上执行动作。
5. Observe the new state (next screenshot).
   中文翻译：观察新状态（下一张截图）。
6. Repeat until the task is done.
   中文翻译：重复直到任务完成。

Each step is a multimodal VLM call. The VLM output must be parseable JSON. Errors compound across steps, so recovery matters.

> 每一步都是一次多模态 VLM 调用。VLM 输出必须是可解析的 JSON。错误在步骤间累积，因此恢复机制至关重要。

## The Concept | 核心概念

> **【中文解读】** 多模态 Agent（如 Computer Use Agent）让 AI 直接操作计算机界面：截图理解屏幕内容，生成鼠标/键盘操作。这是多模态理解的终极应用——AI 不仅能看懂图像，还能在图形界面中执行任务。

> **【拓展：Computer Use 的前沿** Anthropic 的 Computer Use 让 Claude 直接操作桌面应用，完成网页浏览、表单填写等任务。OpenAI 的 Operator 使用类似方法。关键技术挑战：精确定位（准确点击按钮）、状态跟踪（理解界面变化）、错误恢复（操作失败后重试）。当前模型在 OSWorld 基准上的成功率约 12.5%（人类约 72%），还有很大提升空间。


### GUI grounding — the primitive | GUI 定位——基础原语

GUI grounding is: given a screenshot and a natural language instruction, output the (x, y) coordinate to click (or other action).

> GUI 定位是：给定一张截图和自然语言指令，输出需要点击的 (x, y) 坐标（或其他动作）。

> **【中文解读】** GUI 定位是：给定一张截图和自然语言指令，输出需要点击的 (x, y) 坐标（或其他动作）。SeeClick 是首个大规模开放成果，CogAgent 增加了 1120x1120 高分辨率编码，Ferret-UI 聚焦移动端 UI。输出格式通常是 JSON，`element_desc` 字段帮助恢复——当坐标在截图间漂移时，语义提示让系统重新定位。

SeeClick (arXiv:2401.10935) was the first open result at scale: fine-tune a VLM on synthetic + real GUI data, output coordinates as plain text tokens. Works.

> SeeClick 是首个大规模开放成果：在合成+真实 GUI 数据上微调 VLM，以纯文本 token 输出坐标。有效。

CogAgent (arXiv:2312.08914) added 1120x1120 high-resolution encoding for dense UIs. Score: ~84% on web navigation.

> CogAgent 为密集 UI 添加了 1120x1120 高分辨率编码。网页导航得分约 84%。

Ferret-UI (arXiv:2404.05719) focuses on mobile UIs, integrates with iOS accessibility data.

> Ferret-UI 聚焦移动端 UI，集成 iOS 无障碍数据。

Output format is usually JSON:

> 输出格式通常是 JSON：

```json
{"action": "click", "x": 384, "y": 220, "element_desc": "Search button"}
```

The `element_desc` helps recovery: if coordinates drift between screenshots, the semantic hint lets the system re-ground.

> `element_desc` 帮助恢复：如果坐标在截图间漂移，语义提示让系统重新定位。

### Action schemas | 动作模式

A typical action schema has 6-10 action types:

> 典型的动作模式包含 6-10 种动作类型：

> **【中文解读】** 典型的动作模式包含 6-10 种动作类型：click（点击）、type（输入）、scroll（滚动）、drag（拖拽）、select（选择）、hover（悬停）、navigate（导航）、wait（等待）、done（完成）。Agent 每步输出一个动作，浏览器包装器执行后返回新状态。

- `click`: (x, y)
  中文翻译：`click`：点击 (x, y)。
- `type`: (text, x?, y?)
  中文翻译：`type`：输入文本，可选位置。
- `scroll`: (direction, amount)
  中文翻译：`scroll`：滚动（方向，量）。
- `drag`: (x0, y0, x1, y1)
  中文翻译：`drag`：从 (x0, y0) 拖拽到 (x1, y1)。
- `select`: (option_index)
  中文翻译：`select`：选择选项。
- `hover`: (x, y)
  中文翻译：`hover`：悬停 (x, y)。
- `navigate`: (url)
  中文翻译：`navigate`：导航到 URL。
- `wait`: (ms)
  中文翻译：`wait`：等待毫秒数。
- `done`: (success, explanation)
  中文翻译：`done`：完成（成功/失败，解释）。

The agent emits one action per step. The browser wrapper executes and returns the new state.

> Agent 每步输出一个动作。浏览器包装器执行后返回新状态。

### Screenshot-only vs accessibility-tree | 纯截图 vs 无障碍树

> **【中文解读】** 两种输入模式：纯截图模式最通用但精度较低；无障碍树（DOM/iOS 无障碍信息）更可靠但仅在有结构数据时可用；混合模式同时使用两者，树用于原子动作定位，截图用于语义理解。生产 Agent 尽可能使用混合模式。

Two input modes:

> 两种输入模式：

- Screenshot-only: full image, no structural info. Most general; works on any app.
  中文翻译：纯截图：完整图像，无结构信息。最通用；适用于任何应用。
- Accessibility tree: structured DOM / iOS accessibility info. Much more reliable for grounding; works where the tree is available.
  中文翻译：无障碍树：结构化 DOM / iOS 无障碍信息。定位更可靠；在有树数据时可用。
- Hybrid: both, with the tree as a reliable grounder for atomic actions and the screenshot for semantic context.
  中文翻译：混合：两者都用，树用于原子动作定位，截图用于语义理解。

Production agents use hybrid when possible. Browser automation (Selenium + accessibility) always has the tree; desktop apps sometimes do.

> 生产 Agent 尽可能使用混合模式。浏览器自动化（Selenium + 无障碍）始终有树；桌面应用有时有。

### Long-horizon memory | 长期记忆

A 20-step workflow generates 20 screenshots. The VLM's context fills up fast. Three compression strategies:

> 20 步工作流产生 20 张截图。VLM 上下文很快填满。三种压缩策略：

> **【中文解读】** 20 步工作流产生 20 张截图，VLM 上下文很快填满。三种压缩策略：摘要链（每 5 步总结一次，丢弃旧截图）、跳帧（保留首尾和每第 3 张）、工具记录日志（只保留文本日志不看旧截图）。Claude 的计算机使用 API 使用日志模式，更简单可靠。

- Summary-chain: after every 5 steps, summarize what has happened, drop old screenshots.
  中文翻译：摘要链：每 5 步总结已发生的事情，丢弃旧截图。
- Skip-frame: keep the first, last, and every 3rd screenshot.
  中文翻译：跳帧：保留首、尾和每第 3 张截图。
- Tool-recorded log: execute actions, keep a text log of what was done; don't re-look at old screenshots.
  中文翻译：工具记录日志：执行动作，保留文本日志；不重新查看旧截图。

Claude's computer-use API uses the log pattern. Simpler, more reliable.

> Claude 的计算机使用 API 使用日志模式。更简单，更可靠。

### Visual tool use | 视觉工具使用

> **【中文解读】** ChartAgent 引入视觉工具调用：Agent 可以输出"裁剪区域 (100,200,300,400) 然后调用 OCR"作为工具调用。工具返回文本后 VLM 继续推理。这一模式可推广到集合标记提示、区域标注和外部检测工具。

ChartAgent (arXiv:2510.04514) introduces visual tool use for chart understanding: crop, zoom, OCR, call external detection. The agent can output "crop to region (100, 200, 300, 400) then call OCR" as a tool call. The tool returns text; the VLM continues reasoning.

> ChartAgent 引入视觉工具调用用于图表理解：裁剪、缩放、OCR、调用外部检测。Agent 可以输出"裁剪到区域 (100, 200, 300, 400) 然后调用 OCR"作为工具调用。工具返回文本；VLM 继续推理。

This pattern generalizes: set-of-mark prompting, region annotation, and external detection tools all fit the same "output a tool call, receive a structured response" schema.

> 这一模式可推广：集合标记提示、区域标注和外部检测工具都适配相同的"输出工具调用，接收结构化响应"模式。

### The 2026 benchmarks | 2026 年基准测试

> **【拓展：多模态 Agent 基准全景】** ScreenSpot-Pro 测试 GUI 定位（开放模型 ~85%，前沿 ~90%）；VisualWebArena 测试端到端网页任务（开放模型 ~20%，Gemini 3 Pro ~27%）；AgentVista 是 2026 最难基准，覆盖 12 个领域的真实工作流，前沿模型仅 27-40%；WebArena/WebShop 已被前沿模型饱和。

- ScreenSpot-Pro. GUI grounding on ~1k web screenshots. Open SOTA Qwen2.5-VL-72B ~85%. Frontier ~90%.
  中文翻译：ScreenSpot-Pro。约 1k 网页截图 GUI 定位。开放 SOTA Qwen2.5-VL-72B 约 85%。前沿约 90%。
- VisualWebArena. End-to-end web tasks (shop, forum, classifieds). Open SOTA ~20%. Gemini 3 Pro ~27%.
  中文翻译：VisualWebArena。端到端网页任务（购物、论坛、分类广告）。开放 SOTA 约 20%。Gemini 3 Pro 约 27%。
- AgentVista (arXiv:2602.23166). The hardest 2026 benchmark. Realistic workflows across 12 domains. Frontier models score 27-40%; open models 10-20%.
  中文翻译：AgentVista。2026 年最难基准。跨 12 领域真实工作流。前沿模型 27-40%；开放模型 10-20%。
- WebArena / WebShop. Older benchmarks; saturated by frontier.
  中文翻译：WebArena / WebShop。旧基准；已被前沿模型饱和。

### Why it's still hard | 为什么仍然很难

> **【中文解读】** Agent 性能瓶颈：1) 细粒度视觉定位（"点击小 X"在移动分辨率下经常失败）；2) 长期规划（10 步后 Agent 偏离目标）；3) 错误恢复（点击失败时检测和恢复缺乏训练数据）；4) 跨页面上下文（跳转标签页或长表单丢失状态）。研究方向包括记忆架构、显式重规划、多模态验证。

Agent performance bottlenecks:

> Agent 性能瓶颈：

1. Visual grounding at fine scale. "Click the small X" fails often at mobile resolution.
   中文翻译：细粒度视觉定位。"点击小 X"在移动分辨率下经常失败。
2. Long-horizon planning. After 10 actions, the agent drifts from the goal.
   中文翻译：长期规划。10 个动作后 Agent 偏离目标。
3. Error recovery. When a click fails (wrong button), detecting + recovering is rarely trained data.
   中文翻译：错误恢复。点击失败时（按错按钮），检测+恢复缺乏训练数据。
4. Cross-page context. Jumping between tabs or long forms loses state.
   中文翻译：跨页面上下文。跳转标签页或长表单丢失状态。

Research directions: memory architectures, explicit replanning, multimodal verification (screenshot match for action success).

> 研究方向：记忆架构、显式重规划、多模态验证（截图匹配验证动作成功）。

### The capstone build-it | 毕业项目构建

> **【中文解读】** 毕业项目任务：构建一个计算机使用 Agent，能够读取预订网站模拟页面的 HTML+截图，规划多步序列（搜索→选择→填表→提交），输出匹配动作模式的 JSON 动作，并在 10 个固定任务上评估。

The capstone task: build a computer-use agent that:

> 毕业项目任务：构建一个计算机使用 Agent，要求：

1. Reads the HTML + screenshot of a booking-site mock page.
   中文翻译：读取预订网站模拟页面的 HTML + 截图。
2. Plans a multi-step sequence: search → select → fill form → submit.
   中文翻译：规划多步序列：搜索→选择→填表→提交。
3. Emits JSON actions matching the action schema.
   中文翻译：输出匹配动作模式的 JSON 动作。
4. Evaluates on a fixed 10-task slice.
   中文翻译：在固定的 10 个任务上评估。

The lesson provides scaffold code that is easy to extend into a real browser.

> 课程提供脚手架代码，易于扩展到真实浏览器。

## Use It | 用框架实现

`code/main.py` is the capstone scaffold:

- Action schema JSON definition (10 actions).
  中文翻译：动作模式 JSON 定义（10 种动作）。
- Mock browser state as dict.
  中文翻译：模拟浏览器状态（字典）。
- Agent loop skeleton: receive state, emit action, apply, loop.
  中文翻译：Agent 循环骨架：接收状态、输出动作、执行、循环。
- 10-task mini-benchmark (synthetic pages) to measure end-to-end success rate.
  中文翻译：10 任务迷你基准（合成页面）测量端到端成功率。
- Error-recovery hook for when an action fails.
  中文翻译：动作失败时的错误恢复钩子。

## Ship It | 产出物

This lesson produces `outputs/skill-multimodal-agent-designer.md`. Given a computer-use product (domain, action set, evaluation target), designs the full agent loop, memory strategy, grounding mode, and expected benchmark score.

> 本课产出 `outputs/skill-multimodal-agent-designer.md`。给定计算机使用产品（领域、动作集、评估目标），设计完整的 Agent 循环、记忆策略、定位模式和预期基准分数。

## Exercises | 练习题

1. Extend the action schema with a `screenshot_region` tool (crop + zoom). What tasks benefit?
   扩展动作模式，添加 `screenshot_region` 工具（裁剪+缩放）。哪些任务会受益？

2. Read AgentVista (arXiv:2602.23166). Describe the hardest task category and why frontier models still fail.
   阅读 AgentVista 论文。描述最困难的任务类别以及前沿模型仍然失败的原因。

3. Long-horizon memory compression: design a summary-chain with ≤4 screenshots kept live, any number logged.
   长期记忆压缩：设计一个摘要链，保持 ≤4 张截图活跃，任意数量记录到日志。

4. Build an error-recovery hook: on action failure (button not found), what does the agent do next?
   构建错误恢复钩子：当动作失败（按钮未找到）时，Agent 下一步做什么？

5. Compare screenshot-only Claude 4.7 to hybrid screenshot + accessibility-tree Qwen2.5-VL on 10 web tasks. Which wins on which tasks?
   对比纯截图的 Claude 4.7 与混合模式的 Qwen2.5-VL 在 10 个网页任务上的表现。各在哪类任务上胜出？

## Key Terms | 关键术语

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|----------|
| GUI grounding | "Click coordinates" | Model outputs (x,y) for the target of an instruction on a screenshot | GUI 定位：模型输出截图上指令目标的 (x,y) 坐标 |
| Action schema | "Tool definitions" | JSON description of valid actions (click, type, scroll, drag) | 动作模式：有效动作的 JSON 描述 |
| Accessibility tree | "Structured DOM" | Machine-readable UI hierarchy from browser/iOS APIs | 无障碍树：来自浏览器/iOS API 的机器可读 UI 层级 |
| Hybrid agent | "Screenshot + tree" | Uses both image and structured info; more reliable than either alone | 混合 Agent：同时使用图像和结构化信息 |
| Visual tool use | "Zoom/crop/detect" | Agent calls external vision tools (OCR, detection) mid-plan | 视觉工具使用：Agent 在规划中调用外部视觉工具 |
| Summary-chain | "Memory compression" | Periodic text summaries replace long screenshot history | 摘要链：定期文本摘要替代长截图历史 |
| VisualWebArena | "E2E web bench" | 2024 benchmark for end-to-end web tasks | 端到端网页任务基准（2024） |
| AgentVista | "2026 hard bench" | 12-domain realistic workflows; even Gemini 3 Pro scores ~30% | 12 领域真实工作流基准，前沿模型仅约 30% |

## Further Reading | 延伸阅读

- [Cheng et al. — SeeClick (arXiv:2401.10935)](https://arxiv.org/abs/2401.10935)
- [Hong et al. — CogAgent (arXiv:2312.08914)](https://arxiv.org/abs/2312.08914)
- [You et al. — Ferret-UI (arXiv:2404.05719)](https://arxiv.org/abs/2404.05719)
- [ChartAgent (arXiv:2510.04514)](https://arxiv.org/abs/2510.04514)
- [Koh et al. — VisualWebArena (arXiv:2401.13649)](https://arxiv.org/abs/2401.13649)
- [AgentVista (arXiv:2602.23166)](https://arxiv.org/abs/2602.23166)
