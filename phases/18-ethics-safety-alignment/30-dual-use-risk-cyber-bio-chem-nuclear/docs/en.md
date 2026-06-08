# Dual-Use Risk — Cyber, Bio, Chem, Nuclear Uplift | 双重用途 核 网络 风险 化学 生物

> The 2026 dual-use picture, domain by domain. Bio/chem: Lesson 17 covers WMDP; Anthropic's bioweapon-acquisition trial (2.53x uplift) and OpenAI's April 2025 Preparedness Framework v2 warning ("on the cusp of meaningfully helping novices create known biological threats") mark the inflection point. Cyber (November 2025 Anthropic report): Chinese-linked state actors used Claude's agentic coding tool to automate up to 90% of a cyberattack campaign, with human intervention only in 4-6 steps; OpenAI "trusted access" pilot gives vetted security organisations capability access for defensive dual-use work. Chem/bio execution gap erosion: the classic defense was "information access alone is insufficient." Vision-enabled frontier models (GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) can observe wet-lab video and provide real-time correction. December 2025: OpenAI demonstrated GPT-5 iterating on wet-lab experiments, achieving 79x efficiency improvement via AI-driven protocol optimization. Novice-vs-expert pattern: AI provides greater relative uplift to novices but greater absolute capability to experts.

> **【中文解读】** 本节介绍了双重用途风险——AI 在网络、生物、化学、核领域的滥用风险和防护。2026 年双重用途画面按领域：生物——从"轻微提升"到 2.53 倍提升（Anthropic 2025），不足以排除 ASL-3；网络——中国关联国家行为者使用 Claude 的代理编码工具自动化高达 90% 的网络攻击活动（Anthropic 2025 年 11 月）；化学——视觉使能的前沿模型可以观察湿实验室视频并提供实时纠正，执行差距正在侵蚀。

> **【拓展：跨领域综合 → 四领域阈值穿越】** 2024-2025 年四个领域的状态：生物从轻微提升到 ASL-3 临界（获取阶段自动化）；化学从轻微提升到执行差距侵蚀（实时湿实验室纠正）；网络从代码辅助到 80-90% 活动自动化（代理编码）；核——仍然受限于材料获取瓶颈。三个领域穿越了阈值，一个仍受非信息壁垒约束。

**Type:** Learn | **类型:** 学习
**Languages:** none | **语言:** 无
**Prerequisites:** Phase 18 · 17 (WMDP), Phase 18 · 18 (safety frameworks), Phase 18 · 28 (ecosystem) | **前置知识:** Phase 18 · 17 (WMDP), Phase 18 · 18 (安全框架), Phase 18 · 28 (生态系统)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Describe the 2024-2025 bio-uplift narrative: "mild uplift" -> "on the cusp" -> "2.53x uplift insufficient to rule out ASL-3."
- Describe the November 2025 Anthropic cyber report: Chinese-linked automation at up to 90% of a cyberattack campaign.
- Describe the chem/bio execution-gap erosion: vision-enabled real-time correction of wet-lab experiments.
- State the novice-relative vs expert-absolute asymmetry and its implication for safety-case construction.

> 描述 2024-2025 年生物提升叙述。描述 2025 年 11 月 Anthropic 网络报告。描述化学/生物执行差距侵蚀。说明新手相对 vs 专家绝对的不对称性及其对安全案例构建的含义。

## The Problem | 问题

Lesson 17 is the measurement methodology. Lesson 30 is the 2026 state of the measurement. The picture shifted materially between 2024 and late 2025: each domain crossed a threshold that the 2024 frameworks did not anticipate.

> Lesson 17 是测量方法论。Lesson 30 是 2026 年的测量状态。2024 到 2025 年底画面发生了实质性变化。

## The Concept | 概念

### Bio/chem uplift narrative

Three phases (repeated from Lesson 17 for coherence):

1. **2024 "mild uplift."** Early Preparedness/RSP evaluations reported small novice advantages over internet search.
2. **April 2025 "on the cusp."** OpenAI PF v2 warned models were "on the cusp of meaningfully helping novices create known biological threats."
3. **2025 Anthropic bioweapon-acquisition trial.** Controlled novice study; 2.53x uplift on acquisition-phase tasks; insufficient to rule out ASL-3.

The shift is qualitative: "mild" evolved into "plausibly enabling" within eighteen months, even without a capability breakthrough.

> **【中文解读】** 化学/生物执行差距侵蚀：历史防御是"信息获取必要但不充分，执行协议的技能阻止新手"。2025 年前沿模型通过视觉部分打破了这个防御——实时协议纠正（GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1 可以观察湿实验室视频并标记错误）。2025 年 12 月 OpenAI 展示 GPT-5 在湿实验室实验上迭代，通过协议优化实现 79 倍效率提升。

### Chem/bio execution-gap erosion

Historic defense: information is necessary but not sufficient; the skill of executing the protocol blocks novices. 2025 frontier models with vision break this defense partially:

- **Real-time protocol correction.** GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1 can observe wet-lab video and flag errors mid-procedure.
- **December 2025 OpenAI demonstration.** GPT-5 iterating on wet-lab experiments achieves 79x efficiency improvement via protocol optimization.

The implication: execution-skill-as-defense is eroding. Procurement and equipment gaps remain, but the tacit-knowledge gap is narrowing.

> **【拓展：网络提升 → 代理编码作为攻击自动化原语】** Anthropic 2025 年 11 月报告的关键发现：代理编码是攻击自动化原语。之前的 AI 网络辅助局限在代码片段级别；代理工作流整合了侦察、利用、后利用和数据外泄。4-6 个人类步骤是瓶颈——未来能力提升将减少该计数。OpenAI 的"可信访问"试点为审查通过的安全组织提供能力访问，如果试点扩展，访问不对称有利于防御者。

### Cyber uplift (November 2025)

Anthropic's November 2025 report: Chinese-linked state actors used Claude's agentic coding tool to automate 80-90% of a cyberattack campaign. Human intervention was required in only 4-6 steps.

Implications:
- Agentic coding is the attack-automation primitive. Previous AI cyber assistance was bounded at code-snippet level; agentic workflows integrate reconnaissance, exploitation, post-exploitation, and exfiltration.
- The 4-6 human steps are the bottleneck; future capability gains would reduce that count.
- Defensive dual-use: OpenAI's "trusted access" pilot provides vetted security organisations (established incident-response firms, government) with capability access for defense. Asymmetry in access favors defenders if the pilot scales.

> **【拓展：核领域 → 材料瓶颈仍有效】** 核是四个 CBRN 领域中在公开文档中分析最少的。威胁模型不同：裂变材料获取主导难度，不是信息。AI 在信息层面对新手的提升在实践中有限。没有 2024-2025 年的主要实验室报告识别到核特定阈值穿越。材料获取瓶颈是唯一仍然有效的非信息壁垒。

### Nuclear

The least-analyzed of the four CBRN domains in public documentation. The threat model is different: fissile-material acquisition dominates the difficulty, not information. AI uplift on the information layer provides limited novice uplift in practice. No 2024-2025 major-lab report identifies a nuclear-specific threshold crossing.

> 四个 CBRN 领域中在公开文档中分析最少的。威胁模型不同：裂变材料获取主导难度，不是信息。材料获取瓶颈是唯一仍然有效的非信息壁垒。

> **【中文解读】** 新手相对 vs 专家绝对的模式：新手相对提升——高，乘法的（Anthropic 2025 生物报告 2.53 倍）；专家绝对能力——高天花板（专家知道该问什么和如何解释）。安全案例启示：仅解决新手提升（通过输入过滤器、拒绝、不确定性表达）对专家绝对控制不够。需要额外措施：引出强化、能力遗忘（Lesson 17）和控制协议（Lesson 10）。

### Novice-relative vs expert-absolute

A pattern across all four domains:

- **Novice-relative uplift.** High. Multiplicative. Per Anthropic 2025 bio, 2.53x.
- **Expert-absolute capability.** High ceiling. An expert extracts more than a novice because the expert knows what to ask and how to interpret.

Implication for safety cases: addressing only novice uplift (via input filters, refusals, uncertainty) is insufficient for expert-absolute control. Additional measures required: elicitation-hardening, capability unlearning (Lesson 17), and control protocols (Lesson 10).

### Cross-domain synthesis

| Domain | 2024 | 2025 | Inflection |
|---|---|---|---|
| Bio | mild uplift | 2.53x uplift, ASL-3 approach | acquisition-phase automation |
| Chem | mild uplift | execution-gap erosion via vision | real-time wet-lab correction |
| Cyber | code assistance | 80-90% campaign automation | agentic coding |
| Nuclear | limited | limited | material-access bottleneck holds |

Three domains crossed thresholds. One remains bounded by non-informational barriers.

> 三个领域穿越了阈值，一个仍受非信息壁垒约束。

### Where this fits in Phase 18

Lesson 30 is the capstone: the current dual-use picture that every prior lesson contributes to measuring, limiting, or governing. Lessons 17-18 give the measurement and frameworks; Lessons 12-16 give the evaluation tooling; Lessons 24-25 give the regulatory and disclosure layer; Lesson 28 gives the research ecosystem. Lesson 30 is where the evidence lands.

> Lesson 30 是顶点课程：每个先前课程贡献于测量、限制或治理的当前双重用途画面。Lesson 30 是证据落地的位置。

No code. Read the Anthropic November 2025 cyber report, OpenAI's Preparedness Framework v2 April 2025 update, and the Council on Strategic Risks 2025 AI x Bio wrapup.

> 没有代码。阅读 Anthropic 2025 年 11 月网络报告、OpenAI PF v2 和 Council on Strategic Risks 2025 AI x Bio 年终总结。

This lesson produces `outputs/skill-dual-use-triage.md`. Given a 2026 capability claim or incident report, it triages across the four domains and identifies whether the claim affects novice-relative uplift, expert-absolute capability, or both.

> 本课产出 `outputs/skill-dual-use-triage.md`。给定 2026 年能力声明或事件报告，跨四个领域分类并识别声明影响新手相对提升、专家绝对能力还是两者。

## Exercises | 练习题

1. Read Anthropic's November 2025 cyber report. Enumerate the 4-6 human-intervention steps and argue which would be first to automate in a next-generation model.

2. The chem/bio execution gap is eroding via vision. Design an evaluation that measures tacit-knowledge uplift without crossing ITAR/EAR boundaries.

3. Nuclear uplift appears bounded by material access. Argue for and against the position that a future AI breakthrough could shift this bottleneck.

4. Construct a safety case (Lesson 18 three-pillar) for a cyber-capable frontier model that bounds both novice and expert uplift.

5. Pick one of the four domains and write a one-paragraph 2027 forecast based on the 2024-2025 trajectory. Identify the evidence that would falsify your forecast.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Uplift | "AI helps attackers" | Increase in attacker capability attributable to AI assistance |
| Novice-relative uplift | "multiplicative" | How much AI helps a novice vs status-quo |
| Expert-absolute capability | "ceiling" | Maximum capability an expert can extract from the model |
| Execution gap | "doing vs knowing" | Historical defense: tacit wet-lab skill blocks novices |
| Agentic coding | "autonomous attacks" | Multi-step autonomous cyber-task execution |
| Acquisition phase | "pre-synthesis steps" | Procurement, equipment, permit stages of a bio threat |
| Trusted access | "defender-only pilot" | OpenAI 2025 program giving vetted defenders capability access |

## Further Reading | 延伸阅读

- [Anthropic — November 2025 cyber threat report](https://www.anthropic.com/news/disrupting-AI-espionage) — Chinese-linked campaign automation
- [OpenAI — Preparedness Framework v2 (April 15, 2025)](https://openai.com/index/updating-our-preparedness-framework/) — bio "on the cusp"
- [Anthropic — RSP v3.0 (February 2026)](https://www.anthropic.com/responsible-scaling-policy) — ASL-3 bio thresholds
- [Council on Strategic Risks — 2025 AI x Bio wrapup](https://councilonstrategicrisks.org/2025/12/22/2025-aixbio-wrapped-a-year-in-review-and-projections-for-2026/) — year-end synthesis
