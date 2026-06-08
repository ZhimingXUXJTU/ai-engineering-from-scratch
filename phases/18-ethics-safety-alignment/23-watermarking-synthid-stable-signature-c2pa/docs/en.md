# Watermarking — SynthID, Stable Signature, C2PA | 稳定签名 水印 SynthID C2PA

> Three technologies structure 2026 AI-generated-content provenance. SynthID (Google DeepMind) — image watermarking launched August 2023, text+video May 2024 (Gemini + Veo), text open-sourced October 2024 via Responsible GenAI Toolkit, unified multi-media detector November 2025 alongside Gemini 3 Pro. Text watermarking adjusts next-token sampling probabilities imperceptibly; image/video watermarks survive compression, cropping, filters, frame-rate changes. Stable Signature (Fernandez et al., ICCV 2023, arXiv:2303.15435) — fine-tunes the latent diffusion decoder so every output contains a fixed message; cropped (10% of content) generated images detected >90% at FPR<1e-6. Follow-up "Stable Signature is Unstable" (arXiv:2405.07145, May 2024) — fine-tuning removes the watermark while preserving quality. C2PA — cryptographically signed, tamper-evident metadata standard (C2PA 2.2 Explainer 2025). Watermarking and C2PA are complementary: metadata can be stripped but carries richer provenance; watermarks persist through transcoding but carry less information.

> **【中文解读】** 本节介绍了 AI 水印技术——SynthID、C2PA 等标识 AI 生成内容的方法。SynthID（Google DeepMind）调整 next-token 采样概率使生成包含更多"绿色"令牌——不可察觉但可检测。Stable Signature 微调潜在扩散解码器使每个输出包含固定二进制消息。C2PA 是加密签名、防篡改的元数据标准。

> **【拓展：水印 → Deepfake 检测】** 水印是 Deepfake 检测的核心技术路径。SynthID 的跨模态检测器（2025 年 11 月）可以从文本、图像、音频和视频中读取信号。但局限性明显：模型特定（无 SynthID 信号不等于真实）、不抗释义（文本水印在改写后消失）、微调可移除（"Stable Signature is Unstable"证明）。与 C2PA 元数据互补——元数据可剥离但信息丰富，水印持久但信息有限。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, token-watermark embed + detect) | **语言:** Python（标准库，token 水印嵌入 + 检测）
**Prerequisites:** Phase 10 · 04 (sampling), Phase 01 · 09 (information theory) | **前置知识:** Phase 10 · 04 (采样), Phase 01 · 09 (信息论)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Describe token-level watermarking (SynthID-text style) and the mechanism by which it is detectable.
- Describe Stable Signature and the 2024 removal attack that broke it.
- State C2PA's role and why it is complementary to watermarking.
- Describe the key limitations: model-specific signal, robustness under paraphrase, and meaning-preserving attacks (arXiv:2508.20228).

> 描述令牌级水印（SynthID-text 风格）及其可检测机制。描述 Stable Signature 和 2024 年破坏它的移除攻击。说明 C2PA 的角色以及为什么它与水印互补。描述关键局限性：模型特定信号、释义下的鲁棒性和意义保持攻击。

## The Problem | 问题

2023-2024 saw deepfakes and AI-generated content enter political and consumer contexts at scale. Watermarking is the proposed technical provenance signal: mark generations at creation time, detect them later. 2025 evidence: no watermark is unconditionally robust, but layered with C2PA metadata the combination provides a usable provenance story.

> 2023-2024 年深度伪造和 AI 生成内容大规模进入政治和消费场景。水印是提出的技术来源信号：在创建时标记生成，之后检测。2025 年证据：没有水印是无条件鲁棒的，但与 C2PA 元数据分层提供可用的来源故事。

## The Concept | 概念

> **【中文解读】** 文本水印机制（Kirchenbauer 等人 2023，由 Google 产品化）：每个解码步骤将前 K 个令牌哈希产生词汇表的伪随机"绿色"和"红色"分区，向绿色 logits 添加 delta 偏置采样。生成包含比随机更多的绿色令牌。检测：重新哈希每个前缀，计数生成中的绿色令牌，计算 z 分数。水印文本 z > 0，人类文本 z ~ 0。

### Text watermarking (SynthID-text style)

The Kirchenbauer et al. 2023 mechanism, productionized by Google:

1. At each decoding step, hash the previous K tokens to produce a pseudorandom partition of the vocabulary into "green" and "red" sets.
2. Bias sampling toward the green set by adding δ to green logits.
3. The generation contains more green tokens than chance would produce.

Detection: rehash each prefix, count green tokens in the generation, compute a z-score. The z-score is >0 for watermarked text, ~0 for human text.

Properties:
- Imperceptible to readers (δ is small enough that quality loss is minor).
- Detectable with access to the vocabulary partition function.
- Not robust to paraphrase — rewriting the text destroys the signal.

SynthID-text is open-sourced October 2024 via Google's Responsible GenAI Toolkit.

> **【中文解读】** Stable Signature（Fernandez 等人, ICCV 2023）微调潜在扩散解码器使每个生成图像包含固定二进制消息。裁剪到原始内容 10% 的图像在 FPR<1e-6 下检测率 >90%。但 2024 年 5 月"Stable Signature is Unstable"证明微调解码器可以在保持图像质量的同时移除水印——对抗性生成后微调成本低。

### Stable Signature (image)

Fernandez et al. ICCV 2023. Fine-tune the latent diffusion decoder so every generated image contains a fixed binary message embedded in the latent representation. Detection is decoded from the latent with a neural decoder. Cropped (to 10% of content) images detected >90% at FPR<1e-6.

> Stable Signature 微调潜在扩散解码器使每个生成图像包含固定二进制消息。裁剪到 10% 的图像在 FPR<1e-6 下检测率 >90%。

May 2024 "Stable Signature is Unstable" (arXiv:2405.07145): fine-tuning the decoder removes the watermark while preserving image quality. Adversarial post-generation fine-tuning is cheap; the watermark's adversarial robustness is limited.

> 2024 年 5 月"Stable Signature is Unstable"证明微调解码器可以在保持图像质量的同时移除水印。对抗性后生成微调成本低；水印的对抗鲁棒性有限。

### SynthID unified detector (November 2025)

Alongside Gemini 3 Pro: a multi-media detector that reads SynthID signals from text, image, audio, and video in one API. Unifies the Google provenance stack.

> 伴随 Gemini 3 Pro：一个跨模态检测器，可从文本、图像、音频和视频中读取 SynthID 信号。统一了 Google 来源技术栈。

> **【拓展：C2PA + 水印互补 → EU AI Act Article 50】** C2PA 和水印互补：元数据可剥离但携带丰富来源链；水印通过转码持久但只携带少量比特。Google 在搜索、广告和"关于此图片"中集成两者。EU AI Act Article 50 的透明度代码要求 AI 生成内容标签（包括 Deepfake），这是需要 Lesson 23 水印技术的监管层。

### C2PA

Coalition for Content Provenance and Authenticity. Cryptographically signed tamper-evident metadata standard. C2PA 2.2 Explainer (2025). A C2PA manifest records provenance claims (who created, when, what transformations) signed by the creator's key.

> C2PA 是加密签名、防篡改的元数据标准。C2PA 清单记录来源声明（谁创建、何时、什么转换），由创建者的密钥签名。

Complementary to watermarking:
- Metadata can be stripped; watermarks cannot (easily).
- Metadata is rich (full provenance chain); watermarks carry bits.
- C2PA depends on platform adoption; watermarks embed automatically.

> 与水印互补：元数据可剥离但信息丰富；水印通过转码持久但只携带少量比特。C2PA 依赖平台采用；水印自动嵌入。

Google integrates both in Search, Ads, and "About this image."

> Google 在搜索、广告和"关于此图片"中集成两者。

> **【拓展：水印局限性 → 模型特定信号问题】** 关键局限性：SynthID 水印仅来自启用 SynthID 的模型。"无 SynthID 信号"不等于真实性证明——未启用 SynthID 的模型生成的任何内容都不会有水印。此外，arXiv:2508.20228（2025）展示了意义保持攻击可以同时破坏文本水印和多种图像水印。

### Limitations

- **Model-specific.** SynthID watermarks generations from SynthID-enabled models. A generation from a model without SynthID is not watermarked, so "no SynthID signal" is not proof of authenticity.
- **Paraphrase.** Text watermarks do not survive meaning-preserving paraphrase.
- **Transformation attacks.** arXiv:2508.20228 (2025) shows meaning-preserving attacks that destroy both text watermarks and many image watermarks.
- **Fine-tune removal.** Per "Stable Signature is Unstable," post-generation fine-tuning removes embedded watermarks.

### EU AI Act Article 50

Transparency Code for AI-generated content labeling (first draft December 2025, second draft March 2026, expected final June 2026 per the [European Commission status page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)). The Code remains in draft as of April 2026 and the timeline is subject to change. The regulatory layer that requires the technical layer. Deepfakes must be labeled.

### Where this fits in Phase 18

Lessons 22-23 are about what the model emits (private data, provenance signal). Lesson 27 covers training-data governance. Lesson 24 is the regulatory framework that requires these technical measures.

> Lessons 22-23 关于模型发出什么（私有数据、来源信号）。Lesson 27 涵盖训练数据治理。Lesson 24 是要求这些技术措施的监管框架。

## Use It | 使用方法

`code/main.py` builds a toy text watermark. Tokens are integers 0..N-1; watermarked sampling biases toward the hash-defined green set. A detector computes the green-token z-score. You can observe detection at 1000-token generations, watch paraphrase destroy the signal, and measure the false-positive rate on human text.

> `code/main.py` 构建了玩具文本水印。令牌是整数 0..N-1；水印采样偏向哈希定义的绿色集。检测器计算绿色令牌 z 分数。你可以观察 1000 令牌生成的检测、释义破坏信号以及人类文本上的误报率。

## Ship It | 部署上线

This lesson produces `outputs/skill-provenance-audit.md`. Given a content deployment with a provenance claim, it audits: the watermark mechanism (if any), the C2PA signing chain (if any), the adversarial robustness of each, and the per-modality coverage.

> 本课产出 `outputs/skill-provenance-audit.md`。给定有来源声明的内容部署，审计：水印机制、C2PA 签名链、各自的对抗鲁棒性以及每模态覆盖。

## Exercises | 练习题

1. Run `code/main.py`. Report z-scores for watermarked 1000-token generation vs human-authored text. Identify the false-positive rate at the 95% confidence threshold.

2. Implement a paraphrase attack that replaces 30% of tokens with synonyms. Re-measure the z-score.

3. Read Kirchenbauer et al. 2023 Section 6 on robustness. Why do text watermarks fail under paraphrase but image watermarks survive cropping?

4. Design a deployment that uses SynthID-text + C2PA metadata. Describe the provenance chain a consumer sees. Identify one failure mode of each component.

5. The 2024 "Stable Signature is Unstable" result shows fine-tuning removes the image watermark. Design a deployment control that limits this attack — for example, require signed releases of fine-tuned checkpoints.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| SynthID | "Google's watermark" | Cross-modal provenance signal; text, image, audio, video |
| Token watermark | "Kirchenbauer-style" | Biased-sampling text watermark detectable via green-token z-score |
| Stable Signature | "image watermark" | Fine-tuned-decoder watermark; ICCV 2023 |
| C2PA | "the metadata standard" | Cryptographically signed tamper-evident provenance metadata |
| Paraphrase robustness | "does rewording break it" | Text watermark property; currently limited |
| Fine-tune removal | "adversarial unwatermark" | Attack that removes image watermark via decoder fine-tuning |
| Cross-modal detector | "unified SynthID" | November 2025 unified API across modalities |

## Further Reading | 延伸阅读

- [Kirchenbauer et al. — A Watermark for Large Language Models (ICML 2023, arXiv:2301.10226)](https://arxiv.org/abs/2301.10226) — the token-watermark mechanism
- [Fernandez et al. — Stable Signature (ICCV 2023, arXiv:2303.15435)](https://arxiv.org/abs/2303.15435) — image watermark paper
- ["Stable Signature is Unstable" (arXiv:2405.07145)](https://arxiv.org/abs/2405.07145) — the removal attack
- [Google DeepMind — SynthID](https://deepmind.google/models/synthid/) — the cross-modal watermark
- [C2PA 2.2 Explainer (2025)](https://c2pa.org/specifications/specifications/2.2/explainer/Explainer.html) — metadata standard
