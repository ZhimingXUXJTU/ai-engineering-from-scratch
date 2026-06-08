# Moderation Systems — OpenAI, Perspective, Llama Guard | Llama Guard Perspective 审核 OpenAI

> Production moderation systems operationalize the safety policies defined in Lessons 12-16. OpenAI Moderation API: `omni-moderation-latest` (2024) built on GPT-4o classifies text + images in one call; 42% better on multilingual test set than prior version; the response schema returns 13 category booleans — harassment, harassment/threatening, hate, hate/threatening, illicit, illicit/violent, self-harm, self-harm/intent, self-harm/instructions, sexual, sexual/minors, violence, violence/graphic; free for most developers. Layered patterns: Input moderation (pre-generation), Output moderation (post-generation), Custom moderation (domain rules). Async parallel calls hide latency; placeholder responses on flag. Llama Guard 3/4 (Lesson 16): 14 MLCommons hazards, Code Interpreter Abuse, 8 languages (v3), multi-image (v4). Perspective API (Google Jigsaw): toxicity scoring predating the LLM-as-moderator wave; primarily single-dimension toxicity with severe-toxicity/insult/profanity variants; baseline for content-moderation research. Deprecations: Azure Content Moderator deprecated February 2024, retired February 2027, replaced by Azure AI Content Safety.

> **【中文解读】** 本节介绍了内容审核系统——OpenAI Perspective、Llama Guard 等内容安全工具。OpenAI Moderation API（omni-moderation-latest, 2024）基于 GPT-4o，在单次调用中分类文本+图像，返回 13 个类别布尔值。三层模式是 2026 年默认配置：输入审核（预生成）、输出审核（后生成）、自定义审核（域规则）。

> **【拓展：审核栈 → 生产配置】** OpenAI 和 Llama Guard 的分类法重叠但分歧——OpenAI 有"非法"作为宽泛类别，Llama Guard 分为"暴力犯罪"和"非暴力犯罪"。部署根据策略分类法适配选择。Perspective API（Google Jigsaw）是 LLM 时代前的毒性评分基线，在内容审核研究中仍广泛使用因为有多年校准数据。Azure Content Moderator 2024 年 2 月弃用，2027 年 2 月退役，迁移到 Azure AI Content Safety。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, three-layer moderation harness) | **语言:** Python（标准库，三层审核框架）
**Prerequisites:** Phase 18 · 16 (Llama Guard / Garak / PyRIT) | **前置知识:** Phase 18 · 16 (Llama Guard / Garak / PyRIT)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Learning Objectives | 学习目标

- Describe the OpenAI Moderation API's category taxonomy and how it differs from Llama Guard 3's MLCommons set.
- Describe the three moderation-layer pattern (input, output, custom) and name one failure mode of each.
- Describe Perspective API's position as a pre-LLM-era baseline and why it remains used in research.
- State the Azure deprecation timeline.

> 描述 OpenAI Moderation API 的类别分类法及其与 Llama Guard 3 MLCommons 集的区别。描述三层审核模式和每层的一个失败模式。描述 Perspective API 作为 LLM 前时代基线的位置。说明 Azure 弃用时间线。

## The Problem | 问题

Lessons 12-16 describe attacks and defense tooling. Lesson 29 covers the deployed moderation systems that operationalize the defenses at the surface where users touch the product. The three-layer pattern is the 2026 default configuration.

> Lessons 12-16 描述攻击和防御工具。Lesson 29 涵盖将防御操作化的已部署审核系统。三层模式是 2026 年默认配置。

## The Concept | 概念

> **【中文解读】** OpenAI Moderation API 的 13 个类别：骚扰/骚扰-威胁、仇恨/仇恨-威胁、自残/自残-意图/自残-指示、性/性-未成年人、暴力/暴力-图形、非法/非法-暴力。多模态支持适用于暴力、自残和性但不包括性-未成年人，其余仅限文本。比上一代审核端点多语言测试集上好 42%。

### OpenAI Moderation API

`omni-moderation-latest` (2024). Built on GPT-4o. Classifies text + images in one call. Free for most developers.

Categories (13 booleans in the response schema):
- harassment, harassment/threatening
- hate, hate/threatening
- self-harm, self-harm/intent, self-harm/instructions
- sexual, sexual/minors
- violence, violence/graphic
- illicit, illicit/violent

Multimodal support applies to `violence`, `self-harm`, and `sexual` but not `sexual/minors`; the rest are text-only.

For the code harness in `code/main.py` we collapse the `/threatening`, `/intent`, `/instructions`, and `/graphic` sub-categories into their top-level parents for pedagogical simplicity. Production code should use the full 13-category schema.

42% better on multilingual test set than the prior-generation moderation endpoint. Per-category scores; applications set thresholds.

### Llama Guard 3/4

Covered in Lesson 16. 14 MLCommons hazard categories (organized differently from OpenAI's 13 response-schema booleans). Supports 8 languages (v3). Llama Guard 4 (April 2025) is natively multimodal, 12B.

The OpenAI and Llama Guard taxonomies overlap but diverge. OpenAI has "illicit" as a broad category; Llama Guard has "violent crimes" and "non-violent crimes" separately. Deployments pick based on their policy-taxonomy fit.

### Perspective API (Google Jigsaw)

Toxicity scoring system predating the LLM-as-moderator wave (pre-2020). Categories: TOXICITY, SEVERE_TOXICITY, INSULT, PROFANITY, THREAT, IDENTITY_ATTACK. Single-dimension primary score (TOXICITY) with sub-dimension variants.

Widely used as a content-moderation research baseline because the API is stable, documented, and has years of calibration data. For modern LLM-adjacent use cases, Llama Guard or OpenAI Moderation is typically a better fit.

> **【中文解读】** 三层审核模式的设计逻辑：输入审核必须在生成前完成，输出审核在生成后运行。三层按顺序设计。同层内可并行——在同一文本上同时运行多个分类器（如 OpenAI Moderation + Llama Guard + Perspective）隐藏每个分类器的延迟。可选优化：输入审核完成时显示占位响应（"请稍候，正在检查..."）并推迟 token-1 流式传输。

### The three-layer pattern

1. **Input moderation.** Classify the user's prompt before generation. Reject if flagged. Latency: one classifier call.
2. **Output moderation.** Classify the model's output before delivery. Replace with a refusal if flagged. Latency: one classifier call after generation.
3. **Custom moderation.** Domain-specific rules (regex, allowlists, business policy). Runs at either input or output.

The three layers are sequential by design: input moderation must complete before generation, and output moderation runs after generation. Parallelism applies within a layer — running multiple classifiers (e.g., OpenAI Moderation + Llama Guard + Perspective) concurrently on the same text hides per-classifier latency. As an optional optimization, a placeholder response ("one moment, checking...") may be shown while input moderation completes and token-1 streaming is deferred. Flag behaviour is configurable: refuse, sanitize, escalate to human review.

> **【拓展：失败模式 → 为什么需要多层】** 仅输入审核无法捕获输出幻觉（Lesson 12-14 编码攻击绕过输入分类器）；仅输出审核允许任何输入到达模型（增加成本，向攻击者暴露内部推理）；仅自定义审核不跨类别鲁棒（正则表达式脆弱）。分层是默认——安全带+吊带。

### Failure modes

- **Input only.** Does not catch output hallucinations (Lesson 12-14 encoding attacks bypass input classifiers).
- **Output only.** Allows any input to reach the model; increases cost; surfaces internal reasoning to attacker.
- **Custom only.** Not robust across categories; regexes are brittle.

Layered is the default. Belt-and-suspenders.

### Azure deprecation

Azure Content Moderator: deprecated February 2024, retired February 2027. Replaced by Azure AI Content Safety, which is LLM-based and integrates with Azure OpenAI. The migration is a 2024-2027 field-level project for Azure deployments.

### Where this fits in Phase 18

Lesson 16 covers the moderation tooling in the red-team context. Lesson 29 covers deployed moderation. Lesson 30 closes with the current dual-use capability evidence.

> Lesson 16 在红队背景下涵盖审核工具。Lesson 29 涵盖已部署的审核。Lesson 30 以当前双重用途能力证据结束。

> **【拓展：Azure 迁移 → 2024-2027 行业项目】** Azure Content Moderator 2024 年 2 月弃用，2027 年 2 月退役，替换为基于 LLM 的 Azure AI Content Safety 并与 Azure OpenAI 集成。迁移是一个 2024-2027 年的行业级别项目——每个使用 Azure Content Moderator 的部署都需要规划迁移路径。这是传统内容审核向 LLM 驱动审核的系统性转变。

## Use It | 使用方法

`code/main.py` builds a three-layer moderation harness: input moderator (keyword + category score), output moderator (same classifier on output), custom moderator (domain rules). You can run inputs through and observe which layer catches what.

> `code/main.py` 构建三层审核框架：输入审核器、输出审核器、自定义审核器。你可以运行输入并观察哪一层捕获什么。

This lesson produces `outputs/skill-moderation-stack.md`. Given a deployment, it recommends a moderation stack configuration: which classifier at input, which at output, which custom rules, and what judge for edge cases.

> 本课产出 `outputs/skill-moderation-stack.md`。给定部署，推荐审核栈配置。

## Exercises | 练习题

1. Run `code/main.py`. Run a benign, borderline, and harmful input through all three layers. Report which layer fires for each.

2. Extend the harness with Perspective-API-style toxicity scoring on a specific category. Compare its threshold behaviour to the category score.

3. Read the OpenAI Moderation API docs and the Llama Guard 3 category list. Map each OpenAI category to the closest Llama Guard categories. Identify three categories that do not cleanly map.

4. Design a moderation stack for a code-assistant deployment (e.g., GitHub Copilot). Identify the categories most and least relevant and propose custom rules.

5. Azure Content Moderator retires February 2027. Plan a migration to Azure AI Content Safety. Identify the highest-risk element of the migration.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| OpenAI Moderation | "omni-moderation-latest" | GPT-4o-based 13-category (text) classifier with partial multimodal support |
| Perspective API | "Google Jigsaw toxicity" | Pre-LLM-era toxicity scoring baseline |
| Llama Guard | "MLCommons 14-category" | Meta's hazard classifier (v3: 8B text, 8 langs; v4: 12B multimodal) |
| Input moderation | "pre-generation filter" | Classifier on user prompt before model call |
| Output moderation | "post-generation filter" | Classifier on model output before delivery |
| Custom moderation | "domain rules" | Deployment-specific rules (regex, allowlist, policy) |
| Layered moderation | "all three layers" | Standard production deployment pattern |

## Further Reading | 延伸阅读

- [OpenAI Moderation API docs](https://platform.openai.com/docs/api-reference/moderations) — omni-moderation endpoint
- [Meta PurpleLlama + Llama Guard](https://github.com/meta-llama/PurpleLlama) — Llama Guard repo
- [Google Jigsaw Perspective API](https://perspectiveapi.com/) — toxicity scoring
- [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/) — Azure replacement
