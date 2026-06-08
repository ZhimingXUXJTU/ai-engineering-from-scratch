# WMDP and Dual-Use Capability Evaluation | 评估 双重用途 WMDP

> Li et al., "The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning" (ICML 2024, arXiv:2403.03218). 4,157 multiple-choice questions across biosecurity (1,520), cybersecurity (2,225), and chemistry (412). Questions operate in the "yellow zone" — proximate enabling knowledge, filtered by multi-expert review and ITAR/EAR legal compliance. Dual purpose: proxy evaluation of dual-use capability, and unlearning benchmark (the companion RMU method reduces WMDP performance while preserving general capability). 2024-2025 field narrative: early OpenAI/Anthropic 2024 evaluations reported "mild uplift" over internet search; by April 2025, OpenAI's Preparedness Framework v2 said models are "on the cusp of meaningfully helping novices create known biological threats." Anthropic's bioweapon-acquisition trial showed 2.53x uplift, insufficient to rule out ASL-3.

> **【中文解读】** 本节介绍了 WMDP 双重用途评估——衡量 AI 系统在生物、化学、网络安全等高风险领域的能力。4,157 道多选题涵盖生物安全（1,520）、网络安全（2,225）和化学（412），在"黄色区域"操作——接近有害流程的使能知识但不是直接合成配方。配套的 RMU（表征误导遗忘）方法在保持通用能力的同时将 WMDP 分数降低到接近随机。

> **【拓展：2024-2025 提升叙述 → 从"轻微"到"关键"】** 三阶段叙述：2024 年"轻微提升"——早期评估报告模型对新手只有小幅优势；2025 年 4 月"即将突破"——OpenAI PF v2 报告模型即将有意义地帮助新手创造已知生物威胁；Anthropic 2025 年生物武器获取试验——2.53 倍提升，不足以排除 ASL-3。18 个月内从"轻微"演变为"可能促成"。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, WMDP-shaped uplift evaluation harness) | **语言:** Python（标准库，WMDP 形式提升评估框架）
**Prerequisites:** Phase 18 · 16 (red-team tooling), Phase 14 (agent engineering) | **前置知识:** Phase 18 · 16 (红队工具), Phase 14 (Agent 工程)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- Describe WMDP's three domains, question counts, and "yellow zone" filter criterion.
- Explain RMU and why WMDP is both an evaluation and an unlearning benchmark.
- Describe the 2024-2025 uplift narrative: "mild uplift" -> "on the cusp" -> "insufficient to rule out ASL-3."
- Distinguish novice-relative uplift from expert-absolute capability.

## The Problem | 问题

Dual-use capability is the measurement problem under every lab's frontier safety framework (Lesson 18). The question: does model X materially advance a novice's ability to cause mass harm in bio, chem, or cyber? Direct measurement (ask the model to actually produce harm) is illegal and unethical. Proxy measurement needs a benchmark the model cannot refuse (to produce honest capability numbers) but whose questions are not themselves harmful publications.

## The Concept | 概念

> **【中文解读】** "黄色区域"设计：需要有害流程的接近使能知识但不是直接合成配方。每道题经过多个领域专家审查，按 ITAR/EAR 出口管制合规过滤。选择题格式使模型在不被要求协助任何有害活动的情况下回答，能力可以在不引出有害行为的情况下测量。

### The "yellow zone"

Questions that require proximate, enabling knowledge of a harmful process without being a direct synthesis recipe. "What reagent catalyzes step 4 of [published pathway]?" not "how do I make [dangerous compound]?" Each question reviewed by multiple domain experts; filtered for ITAR/EAR export-control compliance.

4,157 questions total:
- Biosecurity: 1,520
- Cybersecurity: 2,225
- Chemistry: 412

Multiple-choice format. Models answer without being asked to assist with anything; capability can be measured without eliciting harmful behaviour.

> **【中文解读】** RMU（表征误导遗忘）：应用于 LLaMa-2-7B，在将 WMDP 分数降低到接近随机的同时保持 MMLU 和其他通用能力基准在几个百分点内。该方法是每个后续生物-化学-网络安全遗忘论文的基线。

### RMU — Representation Misdirection for Unlearning

The companion unlearning method. Applied to LLaMa-2-7B, reduced WMDP scores to near-random while preserving MMLU and other general-capability benchmarks within a few percentage points. The published method is the unlearning baseline for every subsequent bio-chem-cyber unlearning paper.

### The 2024-2025 uplift narrative

Three phases:

1. **2024 "mild uplift."** Early OpenAI and Anthropic Preparedness/RSP evaluations reported small advantages over internet search for novices attempting bio-adjacent tasks. Public framing: frontier models help, but not substantially more than Google.

2. **April 2025 "on the cusp."** OpenAI's Preparedness Framework v2 reported models "on the cusp of meaningfully helping novices create known biological threats." Not a capability claim — a warning that the cusp is close.

3. **Anthropic's 2025 bioweapon-acquisition trial.** Controlled study with novice participants, measured relative success at acquisition-phase tasks. Reported 2.53x uplift. Insufficient to rule out ASL-3 (Lesson 18) — the threshold for Anthropic's Responsible Scaling Policy tier 3 is met or approached.

> **【拓展：新手相对提升 vs 专家绝对能力 → 安全案例构建】** 关键区分：新手相对提升是乘法的——新手知道很少，即使适度信息也有很大帮助；专家绝对能力是高天花板的——专家知道该问什么和如何解释。安全案例（Lesson 18）必须同时针对两者："模型不能给新手足够的提升来执行"加"专家不能从模型中提取已发布以外的信息"。

### Novice-relative vs expert-absolute

A crucial distinction:

- **Novice-relative uplift.** How much does the model help a non-expert? Multiplicative. The relative advantage is high because novices know little; even modest information helps.
- **Expert-absolute capability.** How much information does the model produce at maximum effort? An expert can extract more than a novice. The absolute ceiling is high.

Safety cases (Lesson 18) target both: "the model cannot give a novice enough uplift to execute" plus "an expert cannot extract information from the model that is not already published."

### The measurement pitfall

WMDP is a capability proxy, not a deployment measurement. A model that scores high on WMDP may or may not be exploitable by a novice in practice, depending on:
- Elicitation resistance (how hard is it to get the capability out without tripping safety filters)
- Tacit knowledge (capability that requires wet-lab skill, not information)
- Execution barriers (procurement, equipment)

Anthropic's 2025 bioweapon-acquisition trial adds the novice-elicitation layer on top of WMDP-style capability: it measures actual task success, not multiple-choice capability.

### Where this fits in Phase 18

Lessons 12-16 are attack and defense tooling on model outputs. Lesson 17 is the dual-use capability layer — the measurement that frontier safety frameworks (Lesson 18) evaluate. Lesson 30 closes the arc with the current 2026 cyber/bio/chem/nuclear uplift evidence.

> **【拓展：测量陷阱 → 能力代理非部署测量】** WMDP 是能力代理，不是部署测量。WMDP 得分高的模型在实践中不一定可被新手利用——取决于引出抗性（不触发安全过滤器获得能力的难度）、隐性知识（需要湿实验室技能的能力）和执行壁垒（采购、设备）。Anthropic 2025 生物武器获取试验在 WMDP 式能力之上添加了新手引出层：测量实际任务成功而非多项选择能力。

## Use It | 使用方法

`code/main.py` builds a toy WMDP-shaped evaluation harness. A mock model is tested on category-binned questions; scores per domain are reported. A simple unlearning intervention (zero out domain-specific representation) reduces scores; you can measure the trade-off against general capability.

## Ship It | 部署上线

This lesson produces `outputs/skill-wmdp-eval.md`. Given a dual-use capability claim ("our model does not meaningfully help with bioweapons"), it audits: which benchmarks were run, which refusal path was used for evaluation (raw completion vs policy-gated), and whether novice-elicitation studies complement the multiple-choice result.

## Exercises | 练习题

1. Run `code/main.py`. Report per-domain accuracy before and after the toy unlearning step. Explain the general-capability trade-off.

2. Augment the toy WMDP with a fourth domain (e.g., radiological). Specify two illustrative question types in the yellow zone. Explain why crafting such questions is harder than adding MMLU-shaped questions.

3. Read WMDP 2024 Section 5 (RMU methodology). Sketch a simpler unlearning approach (e.g., suppress top-k neurons for domain content) and describe its expected general-capability cost.

4. Anthropic 2025's bioweapon-acquisition trial reports 2.53x uplift. Describe two ways this number could be biased upward (novice sample size, task fidelity) and two downward (elicitation ceiling, model safety gating).

5. Articulate what a safety case for ASL-3 requires beyond passing WMDP unlearning. Name at least two complementary elicitation studies.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| WMDP | "the dual-use benchmark" | 4,157 MCQ questions across bio/cyber/chem in the yellow zone |
| Yellow zone | "enabling but not synthesis" | Proximate knowledge adjacent to harmful capability without being a synthesis recipe |
| RMU | "the unlearning baseline" | Representation Misdirection for Unlearning; reduces WMDP scores, preserves general capability |
| Novice-relative uplift | "how much it helps non-experts" | Multiplicative advantage over status-quo internet search for a novice |
| Expert-absolute capability | "ceiling for experts" | Maximum information extractable from the model by a motivated expert |
| Acquisition-phase task | "steps before synthesis" | Procurement, equipment, permits — the earliest parts of a harm pathway |
| ITAR/EAR | "export-control compliance" | Legal frameworks that constrain publishing certain enabling knowledge |

## Further Reading | 延伸阅读

- [Li et al. — The WMDP Benchmark (arXiv:2403.03218, ICML 2024)](https://arxiv.org/abs/2403.03218) — the benchmark and RMU paper
- [OpenAI — Preparedness Framework v2 (April 15, 2025)](https://openai.com/index/updating-our-preparedness-framework/) — "on the cusp" language
- [Anthropic — Responsible Scaling Policy v3.0 (February 2026)](https://www.anthropic.com/responsible-scaling-policy) — ASL-3 bio threshold and acquisition trial results
- [DeepMind — Frontier Safety Framework v3.0 (September 2025)](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) — bio-uplift CCL
