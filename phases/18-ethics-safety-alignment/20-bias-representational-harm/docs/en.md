# Bias and Representational Harm in LLMs | 代表性 偏见 伤害 LLM

> Gallegos, Rossi, Barrow, Tanjim, Kim, Dernoncourt, Yu, Zhang, Ahmed (Computational Linguistics 2024, arXiv:2309.00770). Foundational 2024 survey distinguishing representational harms (stereotypes, erasure) from allocational harms (unequal resource distribution) and categorizing evaluation metrics as embedding-based, probability-based, or generated-text-based. 2024-2025 empirical: An et al. (PNAS Nexus, March 2025) measure intersectional gender x race bias across GPT-3.5 Turbo, GPT-4o, Gemini 1.5 Flash, Claude 3.5 Sonnet, Llama 3-70B on automated resume evaluation for 20 entry-level jobs. WinoIdentity (COLM 2025, arXiv:2508.07111) introduces uncertainty-based fairness evaluation for intersectional identities. Yu & Ananiadou 2025 identify gender neurons in MLP layers; Ahsan & Wallace 2025 use SAEs to reveal clinical racial bias; Zhou et al. 2024 (UniBias) manipulates attention heads for debiasing. Meta-critique (arXiv:2508.11067): 10-year literature disproportionately focuses on binary-gender bias.

> **【中文解读】** 本节介绍了偏见和代表性伤害——AI 系统中的偏见来源、检测和缓解方法。Gallegos 等人（Computational Linguistics 2024）区分了代表性伤害（刻板印象、抹除）和分配性伤害（不平等的资源分配），并将评估指标分类为嵌入基础、概率基础和生成文本基础。

> **【拓展：交叉偏见 → 真实世界影响】** An 等人（PNAS Nexus, 2025 年 3 月）测量了 GPT-3.5 Turbo、GPT-4o、Gemini 1.5 Flash、Claude 3.5 Sonnet、Llama 3-70B 在 20 个入门级职位自动简历评估中的交叉性别×种族偏见。GPT-4o 在简历评分中对黑人女性的惩罚比对黑人男性和白人女性分别更严重——单轴评估无法捕捉这种效应。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, toy embedding-based bias probe) | **语言:** Python（标准库，玩具嵌入偏见探针）
**Prerequisites:** Phase 05 (word embeddings), Phase 18 · 01 (instruction following) | **前置知识:** Phase 05 (词嵌入), Phase 18 · 01 (指令遵循)
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 05（词嵌入）、Phase 18·01。偏见分两类：代表性（刻板印象/抹除）vs 分配性（资源不平等）。
> 💡 **【类比】** 偏见 = "AI 的有色眼镜"。来自训练数据（社会历史偏见）+ 训练目标。评估三方法：嵌入空间（向量几何）+ 概率（logits 差）+ 生成文本（输出统计）。2025 An PNAS Nexus：GPT/Claude/Gemini/Llama 在简历评估上都有交叉性别×种族偏见。Yu 2025 在 MLP 层定位"性别神经元"，Ahsan 2025 用 SAE 揭示临床种族偏见。

## Learning Objectives | 学习目标

- Define representational vs allocational harm and give one example of each in an LLM deployment.

> 定义代表性伤害与分配性伤害，并各给一个 LLM 部署中的例子。

- Name the three evaluation-metric categories from Gallegos et al. 2024 and describe one metric from each.

> 列出 Gallegos 等人 2024 年的三类评估指标，并描述每类中的一个指标。

- Describe intersectionality and why WinoIdentity's uncertainty-based fairness measurement addresses gaps in single-axis bias evaluation.

> 描述交叉性以及为什么 WinoIdentity 的基于不确定性的公平测量解决了单轴偏见评估的缺口。

- Describe two mechanistic-interpretability approaches to bias (gender neurons, SAE features, attention-head manipulation).

> 描述两种偏见的机制可解释性方法（性别神经元、SAE 特征、注意力头操作）。

## The Problem | 问题

The previous lessons cover deliberate harm (jailbreaks, scheming) and safety governance. Bias is harm that emerges without intent — from training data distributions, from prompt framing, from accumulated design choices. Measuring and reducing it is a distinct methodological challenge from adversarial robustness.

> 之前的课程涵盖故意伤害（越狱、策略）和安全治理。偏见是没有意图的伤害——来自训练数据分布、提示框架、累积的设计选择。测量和减少它是与对抗鲁棒性不同的方法论挑战。

## The Concept | 概念

### Representational vs allocational

- **Representational harm.** Stereotypes, erasure, demeaning portrayals. An LLM that depicts nurses as exclusively female is producing representational harm.
- **Allocational harm.** Unequal material outcomes. An LLM that scores Black applicants' resumes systematically lower is producing allocational harm.

> **代表性伤害：** 刻板印象、抹除、贬低性描绘。**分配性伤害：** 不平等的物质结果。两者不同——模型可以"代表性无偏见"但"分配性有偏见"。

These are not the same. A model can be "representationally unbiased" (produces diverse portrayals) while being "allocationally biased" (makes unequal recommendations). Evaluations need to measure both.

> 评估需要同时测量两者。

> **【中文解读】** 三类评估指标：嵌入基础（WEAT 式测试）——测量身份词和属性词之间的统计关联，受限在于测量表征而非行为；概率基础——刻板印象确认 vs 违反补全的对数似然比，捕获部分行为偏见；生成文本基础——下游任务测量（简历评分、推荐撰写、对话），生态效度最高但最难复现。

### Three evaluation-metric categories (Gallegos et al. 2024)

- **Embedding-based.** WEAT-style tests on pre-RLHF embeddings. Measures statistical associations between identity terms and attribute terms. Limited: measures the representation, not the behaviour.
- **Probability-based.** Log-likelihood of stereotype-confirming vs stereotype-violating completions. Decoder-side measurement. Captures some behavioural bias.
- **Generated-text-based.** Downstream-task measurement on generated text. Resume-scoring, recommendation writing, dialogue. Most ecologically valid; hardest to reproduce.

> **嵌入基础：** WEAT 式测试，测量身份词和属性词的统计关联。**概率基础：** 刻板印象确认 vs 违反补全的对数似然比。**生成文本基础：** 下游任务测量，生态效度最高但最难复现。

### Intersectionality

Bias evaluation on "gender" misses the bias that only fires on (gender, race) pairs. An et al. 2025 find GPT-4o penalizes Black women in resume scoring more than Black men and more than white women separately. Single-axis evaluation cannot capture this.

> "性别"上的偏见评估遗漏了仅在（性别，种族）对上触发的偏见。An 等人发现 GPT-4o 在简历评分中对黑人女性的惩罚比对黑人男性和白人女性分别更严重。单轴评估无法捕捉。

WinoIdentity (COLM 2025) introduces uncertainty-based intersectional fairness. It measures whether the model's uncertainty over outcomes differs across intersectional identity tuples — not just the point prediction. This catches cases where the model is equally wrong across groups but more uncertain for some, which produces different downstream allocation behaviour.

> WinoIdentity 引入基于不确定性的交叉性公平评估。它测量模型在不同交叉身份元组上的结果不确定性是否不同。

> **【拓展：机制可解释性 → 偏见干预新路径】** 2024-2025 年机制可解释性工作开辟了偏见到机制干预的路径：性别神经元（Yu & Ananiadou 2025）——特定 MLP 神经元与性别特定行为相关，消融这些神经元以有限的能力成本减少性别差距；临床种族偏见 SAE（Ahsan & Wallace 2025）——稀疏自编码器特征将内部表征分解为可解释维度；UniBias（Zhou 等人 2024）——注意力头操作实现零样本去偏见。

### Mechanistic approaches

2024-2025 interpretability work opens bias to mechanistic intervention:

- **Gender neurons (Yu & Ananiadou 2025).** Specific MLP neurons correlate with gender-specific behaviours. Ablating these neurons reduces gender-gap metrics with limited capability cost.
- **Clinical racial bias via SAEs (Ahsan & Wallace 2025).** Sparse autoencoder features decompose the internal representation into interpretable dimensions; race-correlated features can be identified and suppressed.
- **UniBias (Zhou et al. 2024).** Attention-head manipulation for zero-shot debiasing. Specific heads amplify identity-class sensitivity; zeroing or re-weighting these heads reduces bias with no fine-tuning.

> 2024-2025 年机制可解释性工作开辟了偏见到机制干预的路径：性别神经元——消融这些神经元以有限能力成本减少性别差距；临床种族偏见 SAE——识别和抑制种族相关特征；UniBias——注意力头操作实现零样本去偏见。

> **【中文解读】** 元批评（arXiv:2508.11067, 2025）：10 年文献回顾发现该领域不成比例地聚焦于二元性别偏见。其他轴——残疾、宗教、移民身份、多语言身份——获得的关注远少得多。狭窄关注可能通过忽视伤害边缘化群体：一个在二元性别上良好去偏见的模型可能在没有人检查的维度上严重偏见。

### The meta-critique

The 10-year literature review (arXiv:2508.11067, 2025) finds the field disproportionately focuses on binary-gender bias. Other axes — disability, religion, migration status, multi-lingual identity — receive far less attention. The meta-critique argues that narrow focus can harm marginalized groups by neglect: a model well-debiased on binary gender may be badly biased on dimensions nobody checked.

> 10 年文献回顾发现该领域不成比例地聚焦于二元性别偏见。其他轴——残疾、宗教、移民身份、多语言身份——获得的关注远少得多。狭窄关注可能通过忽视伤害边缘化群体。

### Where this fits in Phase 18

Lessons 20-21 cover bias and fairness formally. Lesson 22 covers privacy. Lesson 23 covers watermarking. These are the user-harm layer complementing the earlier deception/safety layer.

> Lessons 20-21 正式涵盖偏见和公平。Lesson 22 涵盖隐私。Lesson 23 涵盖水印。这些是补充早期欺骗/安全层的用户伤害层。

> **【拓展：交叉性 → WinoIdentity 基准】** WinoIdentity（COLM 2025, arXiv:2508.07111）引入基于不确定性的交叉性公平评估。它测量模型在不同交叉身份元组上的结果不确定性是否不同——不仅是点预测。这捕获了模型在各组之间"同样错误但对某些组更不确定"的情况，这会产生不同的下游分配行为。

## Use It | 使用方法

`code/main.py` builds a toy embedding-based bias probe: measure WEAT-style distance between identity terms and attribute terms in a simple co-occurrence embedding. You can inject a bias and observe the metric fire; apply a simple debiasing operation and observe partial recovery.

> `code/main.py` 构建了玩具嵌入偏见探针：测量简单共现嵌入中身份词和属性词之间的 WEAT 式距离。你可以注入偏见并观察指标触发；应用简单去偏见操作并观察部分恢复。

## Ship It | 部署上线

This lesson produces `outputs/skill-bias-eval.md`. Given a model card or fairness claim, it audits the evaluation across the three metric categories (embedding, probability, generated-text), the intersectionality coverage, and the mechanism of any debiasing intervention.

> 本课产出 `outputs/skill-bias-eval.md`。给定模型卡或公平性声明，审计三类指标的评估、交叉性覆盖和去偏见干预机制。

## Exercises | 练习题

1. Run `code/main.py`. Report WEAT-style bias scores before and after the debiasing step. Explain why the metric does not drop to zero.

2. Extend the probe with an intersectional test: (gender, race) x (career, family). Report cross-axis bias scores.

3. Read An et al. 2025 (PNAS Nexus). Identify the two intersectional effects they report that single-axis gender evaluation would miss.

4. Yu & Ananiadou 2025 identify gender neurons. Sketch a falsification experiment that would distinguish "these neurons cause gender bias" from "these neurons correlate with gender bias."

5. The meta-critique argues the field focuses too narrowly on binary gender. Pick one under-studied axis and describe a representational-harm measurement protocol for it.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Representational harm | "stereotypes / erasure" | Biased portrayal of a group |
| Allocational harm | "unequal decisions" | Biased material outcome for a group |
| WEAT | "the embedding test" | Word Embedding Association Test; co-occurrence-based bias probe |
| Intersectionality | "combined identity effects" | Bias that emerges at the intersection of multiple identity axes |
| Gender neurons | "MLP bias neurons" | Specific neurons whose activations correlate with gender-specific behaviour |
| SAE feature | "interpretable dimension" | Sparse-autoencoder-identified feature; useful for mechanistic bias analysis |
| UniBias | "attention-head debiasing" | Zero-shot debiasing by reweighting attention heads |

## Further Reading | 延伸阅读

- [Gallegos et al. — Bias and Fairness in LLMs: A Survey (arXiv:2309.00770, Computational Linguistics 2024)](https://arxiv.org/abs/2309.00770) — canonical survey
- [An et al. — Intersectional resume-evaluation bias (PNAS Nexus, March 2025)](https://academic.oup.com/pnasnexus/article/4/3/pgaf089/8111343) — five-model intersectional study
- [WinoIdentity — uncertainty-based intersectional fairness (arXiv:2508.07111, COLM 2025)](https://arxiv.org/abs/2508.07111) — new benchmark
- [UniBias — attention-head manipulation (Zhou et al. 2024, ACL)](https://arxiv.org/abs/2405.20612) — zero-shot debiasing
