# Red-Team Tooling — Garak, Llama Guard, PyRIT | Llama Guard 工具 Garak PyRIT

> Three production tools frame the 2026 red-team stack. Llama Guard (Meta) — a Llama-3.1-8B classifier fine-tuned on 14 MLCommons hazard categories; the 2025 Llama Guard 4 is a 12B natively multimodal classifier pruned from Llama 4 Scout. Garak (NVIDIA) — open-source LLM vulnerability scanner with static, dynamic, and adaptive probes for hallucination, data leakage, prompt injection, toxicity, and jailbreaks. PyRIT (Microsoft) — multi-turn red-team campaigns with Crescendo, TAP, and custom converter chains for deep exploitation. Llama Guard 3 is documented in Meta's "Llama 3 Herd of Models" (arXiv:2407.21783); Llama Guard 3-1B-INT4 in arXiv:2411.17713; Garak's probe architecture in github.com/NVIDIA/garak. These tools are the 2026 production interface between red-team research (Lessons 12-15) and deployment (Lesson 17+).

> **【中文解读】** 本节介绍了红队测试——系统化的安全评估方法，用自动化攻击发现 AI 系统漏洞。三个生产工具定义了 2026 年红队技术栈：Llama Guard（Meta）——Llama-3.1-8B 分类器微调于 14 个 MLCommons 危险类别；Garak（NVIDIA）——开源 LLM 漏洞扫描器，含静态、动态和自适应探针；PyRIT（Microsoft）——多轮红队活动，含 Crescendo、TAP 和自定义转换链。

> **【拓展：2026 红队技术栈 → 生产配置】** 标准配置：Llama Guard 放在模型两侧（输入+输出），Garak 每晚运行回归测试，PyRIT 用于预发布活动。Prompt-Guard-86M 是 Meta 的轻量级输入分类器，与 Llama Guard 配合使用。TrustyAI 将 Garak 与 Llama Stack shields 集成进行端到端评估。

**Type:** Build
**Languages:** Python (stdlib, tool-architecture simulator and Llama Guard-style classifier mock)
**Prerequisites:** Phase 18 · 12-15 (jailbreaks and IPI)
**Time:** ~75 minutes

## Learning Objectives | 学习目标

- Describe Llama Guard 3/4's position in the safety stack: input classifier, output classifier, or both.
- Name the 14 MLCommons hazard categories and state one non-obvious one (Code Interpreter Abuse).
- Describe Garak's probe architecture: probes, detectors, harnesses.
- Describe PyRIT's multi-turn campaign structure and how it composes with Garak probes.

## The Problem | 问题

Lessons 12-15 present the attack surface. Production deployments need repeatable, scalable evaluation. Three tools dominate 2026: Llama Guard (the defense classifier), Garak (the scanner), PyRIT (the campaign orchestrator). Each targets a different layer of the red-team lifecycle.

## The Concept | 概念

> **【中文解读】** Llama Guard 3 是 Llama-3.1-8B 模型微调于 MLCommons AILuminate 14 类别的输入/输出分类，支持 8 种语言。Llama Guard 3-1B-INT4 是量化边缘变体（440MB，移动 CPU 约 30 tokens/s）。Llama Guard 4（2025 年 4 月）是 12B 原生多模态分类器，从 Llama 4 Scout 剪枝，替代了之前的 8B 文本和 11B 视觉分类器。

### Llama Guard (Meta)

Llama Guard 3 is a Llama-3.1-8B model fine-tuned for input/output classification over the MLCommons AILuminate 14 categories:
- Violent crimes, non-violent crimes, sex-related, CSAM, defamation
- Specialized advice, privacy, IP, indiscriminate weapons, hate
- Suicide/self-harm, sexual content, elections, code-interpreter abuse

Supports 8 languages. Usage: place before the LLM (input moderation), after the LLM (output moderation), or both. The two uses generate different training distributions — Llama Guard 3 ships as a single model handling both.

Llama Guard 3-1B-INT4 (arXiv:2411.17713, 440MB, ~30 tokens/s on mobile CPU) is the quantized edge variant.

Llama Guard 4 (April 2025) is 12B, natively multimodal, pruned from Llama 4 Scout. It replaces both the 8B text and 11B vision predecessors with one classifier that ingests text + images.

> **【拓展：Garak 架构 → 探针/检测器/线束】** Garak 的三层架构：探针——幻觉、数据泄露、提示注入、毒性、越狱的攻击生成器，分为静态（固定提示）、动态（生成提示）、自适应（响应目标输出）；检测器——针对预期失败模式评分输出；线束——管理探针-检测器对，运行活动，生成报告。基于层的评分（TBSA）替代二元通过/失败——模型可以在同一探针上通过严重性层级 3 但失败层级 5。

### Garak (NVIDIA)

Open-source vulnerability scanner. Architecture:
- **Probes.** Attack generators for hallucination, data leakage, prompt injection, toxicity, jailbreaks. Static (fixed prompts), dynamic (generated prompts), adaptive (responds to target output).
- **Detectors.** Score outputs against expected failure modes — toxic, leaked, jailbroken.
- **Harnesses.** Manage probe-detector pairs, run campaigns, generate reports.

TrustyAI integrates Garak with the Llama-Stack shields (Prompt-Guard-86M input classifier, Llama-Guard-3-8B output classifier) for end-to-end shielded-target evaluation. Tier-based scoring (TBSA) replaces binary pass/fail — a model can pass at severity tier 3 and fail at severity tier 5 on the same probe.

### PyRIT (Microsoft)

Python Risk Identification Toolkit. Multi-turn red-team campaigns. Built around:
- **Converters.** Transform a seed prompt — paraphrase, encode, translate, roleplay.
- **Orchestrators.** Run the campaign: Crescendo (escalation), TAP (branching), RedTeaming (custom loop).
- **Scoring.** LLM-as-judge or classifier-as-judge.

PyRIT is the heavier cousin of Garak. Garak runs thousands of single-turn probes; PyRIT runs deep multi-turn campaigns designed to break specific failure modes.

### The stack

Put Llama Guard on both sides of the model. Run Garak nightly for regression. Run PyRIT for pre-release campaigns. This is the 2026 default configuration for most production deployments.

> **【中文解读】** 评估陷阱：评判身份——所有三个工具都可以使用 LLM 评判，评判校准驱动报告的 ASR（Lesson 12），必须指定评判；探针过时——Garak 探针随着模型修补而老化，自适应探针（PAIR 式）比静态探针老化更慢；Llama Guard 在良性内容上的误报率——早期版本过度标记政治和 LGBTQ+ 内容，v3/v4 校准有改善但未按部署校准。

### Evaluation pitfalls

- **Judge identity.** All three tools can use an LLM judge; judge calibration drives reported ASRs (Lesson 12). Specify the judge alongside the tool.
- **Probe staleness.** Garak probes age as models are patched against them. Adaptive probes (PAIR-shaped) age slower than static probes.
- **Llama Guard FPR on benign content.** Early Llama Guard versions over-flagged political and LGBTQ+ content; Llama Guard 3/4 calibrations are improved but not calibrated per-deployment.

### Where this fits in Phase 18

Lessons 12-15 are the attack families. Lesson 16 is the production tooling. Lesson 17 (WMDP) is the evaluation for dual-use capability. Lesson 18 is the frontier safety frameworks that wrap these tools in a policy structure.

> **【拓展：PyRIT → 多轮深度利用】** PyRIT（Microsoft）是 Garak 的重量级表亲。Garak 运行数千个单轮探针，PyRIT 运行旨在打破特定失败模式的多轮深度活动。其核心是转换器链——将种子提示通过释义、编码、翻译、角色扮演等步骤转换。编排器运行 Crescendo（升级）、TAP（分支）或自定义循环。评分使用 LLM 作为评判或分类器作为评判。

## Use It | 使用方法

`code/main.py` builds a toy Llama Guard-style classifier (keyword + semantic features over 14 categories), a toy Garak harness (probe-detector loop), and a PyRIT-style multi-turn converter chain. You can run the three tools against a mock target and observe the different coverage signatures.

## Ship It | 部署上线

This lesson produces `outputs/skill-red-team-stack.md`. Given a deployment description, it names which of the three tools are appropriate, what to configure in each, and what regression cadence to run.

## Exercises | 练习题

1. Run `code/main.py`. Compare the Llama-Guard-style classifier's detection rate on single-turn vs multi-turn attacks.

2. Implement a new Garak probe: a base64-encoded harmful request. Measure its detection by the Llama-Guard-style classifier.

3. Extend the PyRIT-style converter chain with a "translate to French, then paraphrase" converter. Re-measure attack success.

4. Read Llama Guard 3's hazard-category list. Identify two categories where the training data would realistically produce high false-positive rates on legitimate developer content.

5. Compare Garak and PyRIT's design principles. Argue for a deployment where each is the right tool.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Llama Guard | "the classifier" | Fine-tuned Llama-3.1-8B/4-12B safety classifier with 14 hazard categories |
| Garak | "the scanner" | NVIDIA open-source vulnerability scanner; probes, detectors, harnesses |
| PyRIT | "the campaign tool" | Microsoft multi-turn red-team orchestrator; converters, orchestrators, scoring |
| Prompt-Guard | "the small classifier" | Meta's 86M prompt-injection classifier, paired with Llama Guard |
| TBSA | "tier-based scoring" | Garak's tier-based pass/fail replacing binary outcomes |
| Converter chain | "paraphrase + encode + ..." | PyRIT composition primitive for building multi-step attacks |
| MLCommons hazard categories | "the 14 taxonomies" | Industry-standard taxonomy Llama Guard targets |

## Further Reading | 延伸阅读

- [Meta — Llama Guard 3 (in Llama 3 Herd paper, arXiv:2407.21783)](https://arxiv.org/abs/2407.21783) — the 8B classifier
- [Meta — Llama Guard 3-1B-INT4 (arXiv:2411.17713)](https://arxiv.org/abs/2411.17713) — quantized mobile classifier
- [NVIDIA Garak — GitHub](https://github.com/NVIDIA/garak) — the scanner repo and documentation
- [Microsoft PyRIT — GitHub](https://github.com/Azure/PyRIT) — the campaign toolkit
