# Capstone 15 — Constitutional Safety Harness + Red-Team Range | 宪法式 结业 线束 安全

> Anthropic's Constitutional Classifiers, Meta's Llama Guard 4, Google's ShieldGemma-2, NVIDIA's Nemotron 3 Content Safety, and X-Guard for multilingual coverage defined the 2026 safety-classifier stack. garak, PyRIT, NVIDIA Aegis, and promptfoo became the standard adversarial evaluation tools. NeMo Guardrails v0.12 ties them into a production pipeline. This capstone wires all of it together: a layered safety harness around a target app, an autonomous red-team agent running 6+ attack families, and a constitutional self-critique run that produces a measurable harmlessness delta.

> **【中文解读】** 本节是综合项目——构建宪法式安全线束。


**Type:** Capstone | **类型:** Capstone
**Languages:** Python (safety pipeline, red team), YAML (policy configs) | **语言:** Python (safety pipeline, red team), YAML (policy configs)
**Prerequisites:** Phase 10 (LLMs from scratch), Phase 11 (LLM engineering), Phase 13 (tools), Phase 14 (agents), Phase 18 (ethics, safety, alignment)

> 🔗 **【前置】** 顶点项目 15 = 综合 Phase 10/11/13/14/18。宪法安全线束+红队靶场 = 整合 Phase 18 所有安全工具的实战。
> 💡 **【类比】** 安全线束 = "AI 应用的安全带+气囊"。2026 分类器栈：Anthropic Constitutional Classifiers+Llama Guard 4+Google ShieldGemma-2+NVIDIA Nemotron 3+X-Guard（多语言）。红队工具：garak/PyRIT/NVIDIA Aegis/promptfoo。NeMo Guardrails v0.12 串起来。要求：分层守护+自主红队（6+ 攻击家族）+宪法自评产生可测无害性 delta。| **前置知识:** Phase 10 (LLMs from scratch), Phase 11 (LLM engineering), Phase 13 (tools), Phase 14 (agents), Phase 18 (ethics, safety, alignment)
**Phases exercised:** P10 · P11 · P13 · P14 · P18 | **涉及阶段:** P10 · P11 · P13 · P14 · P18
**Time:** 25 hours | **时间:** 25 hours

## Problem | 问题引入

> **【中文解读】** 本节描述 LLM 安全防护的核心挑战。2026 年前沿问题不是分类器是否有效（它们大致有效），而是如何正确组合它们——不过度拒绝也不留下明显漏洞。Llama Guard 4 处理英文策略违规、X-Guard 覆盖 132 种语言的多语言越狱、ShieldGemma-2 捕获图像提示注入、NVIDIA Nemotron 3 覆盖企业类别、Anthropic 宪法分类器在训练时而非服务时使用。

> **【拓展：对抗性攻击工具生态】** 2026 年标准化攻击工具：garak（LLM 安全扫描器）、PyRIT（微软红队框架）、promptfoo（提示注入测试）、NVIDIA Aegis（企业安全评估）。攻击家族包括：PAIR/TAP（自动越狱发现）、GCG（梯度后缀攻击）、ASCII/base64/rot13 编码攻击、多轮攻击（人格采纳/记忆利用）、语码转换攻击（混合英语与斯瓦希里语或泰语）。每次红队运行产出 CVSS 评分的结构化发现文件。

The frontier of LLM safety in 2026 is not whether classifiers work (they do, roughly) but how to compose them correctly around a production app without over-refusing or leaving obvious holes. Llama Guard 4 handles English policy violations. X-Guard (132 languages) handles multilingual jailbreak. ShieldGemma-2 catches image-based prompt injection. NVIDIA Nemotron 3 Content Safety covers enterprise categories. Anthropic's Constitutional Classifiers are a separate approach used during training rather than serving.

> frontier of LLM safety in 2026 is not whether classifiers work (they do, roughly) but how to compose them correctly around a production app without over-refusing or leaving obvious holes. Llama Guard 4 handles English policy violations. X-Guard (132 languages) handles multilingual jailbreak. ShieldGemma-2 catches image-based prompt injection. NVIDIA Nemotron 3 Content Safety covers enterprise categories. Anthropic's Constitutional Classifiers are a separate approach used during training rather than serving.


Attack evolution matters too. PAIR and TAP automate jailbreak discovery. GCG runs gradient-based suffix attacks. Multi-turn and code-switch attacks exploit agent memory. Any deployed LLM needs a red-team range — garak and PyRIT are the canonical drivers — plus documented mitigations and CVSS-scored findings.

> Attack evolution matters too.


You will harden a target application (either an 8B instruction-tuned model or one of the RAG chatbots from other capstones), run 6+ attack families against it, and produce a before/after harmlessness measurement.

> 你will harden a target application (either an 8B instruction-tuned model or one of the RAG chatbots from other capstones), run 6+ attack families against it, and produce a before/after harmlessness measurement.


## Concept | 核心概念

> **【中文解读】** 安全管道分五层：输入净化（去零宽字符、解码 base64/rot13、Unicode 规范化）→ 策略层（NeMo Guardrails v0.12 策略护栏）→ 分类器门控（Llama Guard 4 输入/X-Guard 非英文/ShieldGemma-2 图像）→ 目标模型 → 输出过滤（Llama Guard 4 输出/Presidio PII 脱敏/引用强制）。高风险输出进入 Slack 人工队列。宪法自审是训练时干预：1000 条有害尝试 → 模型起草 → 按宪法自审 → 重训练，测量前后无害性差异。

> **【拓展：Constitutional AI 方法】** Anthropic 的 Constitutional AI 方法在训练时嵌入安全原则（"无害规则"），而非仅在推理时过滤。红队测试发现，多层组合防护（输入净化 + 策略护栏 + 分类器门控 + 输出过滤）比单层防护效果提升 40-60%。但过度拒绝（false positive）是实际部署的痛点——英文策略分类器在非英文输入上误拒率可达 15-20%，因此需要 X-Guard 等多语言分类器补充。

The safety pipeline is five layers. **Input sanitize**: strip zero-width chars, decode base64/rot13, normalize Unicode. **Policy layer**: NeMo Guardrails v0.12 rails (off-domain, toxicity, PII extraction). **Classifier gate**: Llama Guard 4 on input, X-Guard on non-English, ShieldGemma-2 on image inputs. **Model**: the target LLM. **Output filter**: Llama Guard 4 on output, Presidio PII scrub, citation enforcement where applicable. **HITL tier**: outputs flagged high-risk go to a Slack queue.

> safety pipeline is five layers. **Input sanitize**: strip zero-width chars, decode base64/rot13, normalize Unicode. **Policy layer**: NeMo Guardrails v0.12 rails (off-domain, toxicity, PII extraction). **Classifier gate**: Llama Guard 4 on input, X-Guard on non-English, ShieldGemma-2 on image inputs. **Model**: the target LLM. **Output filter**: Llama Guard 4 on output, Presidio PII scrub, citation enforcement where applicable. **HITL tier**: outputs flagged high-risk go to a Slack queue.


The red-team range runs on a scheduler. PAIR and TAP autonomously discover jailbreaks. GCG runs gradient-based suffix attacks. ASCII / base64 / rot13 encoding attacks. Multi-turn attacks (persona adoption, memory exploitation). Code-switch attacks (mix English with Swahili or Thai). Each run produces a structured findings file with CVSS scoring and disclosure timeline.

> red-team range runs on a scheduler. PAIR and TAP autonomously discover jailbreaks. GCG runs gradient-based suffix attacks. ASCII / base64 / rot13 encoding attacks. Multi-turn attacks (persona adoption, memory exploitation). Code-switch attacks (mix English with Swahili or Thai). Each run produces a structured findings file with CVSS scoring and disclosure timeline.


The constitutional-self-critique run is a training-time intervention. Take 1k harmful-attempt prompts, have the model draft a response, critique it against a written constitution (do-not-harm rules), and retrain on the critique loop. Measure the before/after harmlessness delta on a held-out eval.

> constitutional-self-critique run is a training-time intervention. Take 1k harmful-attempt prompts, have the model draft a response, critique it against a written constitution (do-not-harm rules), and retrain on the critique loop. Measure the before/after harmlessness delta on a held-out eval.


## Architecture | 架构

```
request (text / image / multilingual)
      |
      v
input sanitize (strip zero-width, decode, normalize)
      |
      v
NeMo Guardrails v0.12 rails (off-domain, policy)
      |
      v
classifier gate:
  Llama Guard 4 (English)
  X-Guard (multilingual, 132 langs)
  ShieldGemma-2 (image prompts)
  Nemotron 3 Content Safety (enterprise)
      |
      v (allowed)
target LLM
      |
      v
output filter: Llama Guard 4 + Presidio PII + citation check
      |
      v
HITL tier for flagged outputs

parallel:
  red-team scheduler
    -> garak (classic attacks)
    -> PyRIT (orchestrated red team)
    -> autonomous jailbreak agent (PAIR + TAP)
    -> GCG suffix attacks
    -> multilingual / code-switch
    -> multi-turn persona adoption

output: CVSS-scored findings + disclosure timeline + before/after harmlessness delta
```

## Stack | 技术栈

- Safety classifiers: Llama Guard 4, ShieldGemma-2, NVIDIA Nemotron 3 Content Safety, X-Guard
  中文翻译：Safety classifiers: Llama Guard 4, ShieldGemma-2, NVIDIA Nemotron 3 Content Safety, X-Guard
- Guardrail framework: NeMo Guardrails v0.12 + OPA
  中文翻译：Guardrail framework: NeMo Guardrails v0.12 + OPA
- Red-team drivers: garak (NVIDIA), PyRIT (Microsoft Azure), NVIDIA Aegis, promptfoo
  中文翻译：Red-team drivers: garak (NVIDIA), PyRIT (Microsoft Azure), NVIDIA Aegis, promptfoo
- Jailbreak agents: PAIR (Chao et al., 2023), Tree-of-Attacks (TAP), GCG suffix
  中文翻译：Jailbreak agents: PAIR (Chao et al., 2023), Tree-of-Attacks (TAP), GCG suffix
- Constitutional training: Anthropic-style self-critique loop + SFT on critiques
  中文翻译：Constitutional training: Anthropic-style self-critique loop + SFT on critiques
- PII scrub: Presidio
  中文翻译：PII scrub: Presidio
- Target: an 8B instruction-tuned model or one of the other capstones' RAG chatbots
  中文翻译：Target: an 8B instruction-tuned model or one of the other capstones' RAG chatbots

## Build It | 动手构建

> **【中文解读】** 构建宪法安全测试线束：对待测模型（8B 指令微调模型或 RAG 聊天机器人）运行 10 类攻击（越狱、提示注入、数据泄露、幻觉、偏见、毒性、版权、隐私、拒绝合法请求和可用性退化），每类 20 个测试用例，共 200 个测试。评估通过 6 个指标：拒绝率、误拒率、泄露率、毒性分数、偏见分数和可用性退化度。

> **【拓展：AI 安全评估在 2026 年的标准化进展】** NIST 的 AI RMF（风险管理框架）和 ISO/IEC 42001 成为 AI 安全评估的国际标准。MLCommons 的 Safety v0.5 benchmark 包含 CSB（儿童安全）、激进行为、自残等维度的标准测试集。Anthropic 的 Responsible Scaling Policy 和 OpenAI 的 Preparedness Framework 都要求在模型发布前通过类似本课的 10 类攻击测试。宪法 AI（Constitutional AI）是 Anthropic 的核心安全方法——模型根据预设原则自我批评和修订输出。

1. **Target setup.** Stand up an 8B instruction-tuned model on vLLM (or reuse a RAG chatbot from another capstone). This is the app under test.
   中文翻译：1. **Target setup.** Stand up an 8B instruction-tuned model on vLLM (or reuse a RAG chatbot from another capstone). This is the app under test.

2. **Safety pipeline wrap.** Wire the five-layer pipeline around the target. Verify each layer is individually observable (span per layer in Langfuse).
   中文翻译：2. **Safety pipeline wrap.** Wire the five-layer pipeline around the target. Verify each layer is individually observable (span per layer in Langfuse).

3. **Classifier coverage.** Load Llama Guard 4, X-Guard (multilingual), ShieldGemma-2 (image). Run each on a small labeled set to establish baselines.
   中文翻译：3. **Classifier coverage.** Load Llama Guard 4, X-Guard (multilingual), ShieldGemma-2 (image). Run each on a small labeled set to establish baselines.

4. **Red-team scheduler.** Schedule garak, PyRIT, a PAIR agent, a TAP agent, a GCG runner, a multi-turn attacker, and a code-switch attacker. Each runs on a separate queue.
   中文翻译：4. **Red-team scheduler.** Schedule garak, PyRIT, a PAIR agent, a TAP agent, a GCG runner, a multi-turn attacker, and a code-switch attacker. Each runs on a separate queue.

5. **Attack suite.** Six attack families: (1) PAIR automated jailbreak, (2) TAP tree-of-attacks, (3) GCG gradient suffix, (4) ASCII / base64 / rot13 encoding, (5) multi-turn persona, (6) multilingual code-switch. Report success rate per family.
   中文翻译：5. **Attack suite.** Six attack families: (1) PAIR automated jailbreak, (2) TAP tree-of-attacks, (3) GCG gradient suffix, (4) ASCII / base64 / rot13 encoding, (5) multi-turn persona, (6) multilingual code-switch. Report success rate per family.

6. **Constitutional self-critique.** Curate 1k harmful-attempt prompts. For each, the target drafts a response. A critic LLM scores against a written constitution ("do no harm," "cite evidence," "refuse illegal requests"). Prompts where the critic objects get rewritten; the target fine-tunes on the critique-improved pairs. Measure before/after harmlessness on a held-out eval.
   中文翻译：6. **Constitutional self-critique.** Curate 1k harmful-attempt prompts. For each, the target drafts a response. A critic LLM scores against a written constitution ("do no harm," "cite evidence," "refuse illegal requests"). Prompts where the critic objects get rewritten; the target fine-tunes on the critique-improved pairs. Measure before/after harmlessness on a held-out eval.

7. **Over-refusal measurement.** Track false-positive rate on a benign prompt suite (e.g., XSTest). The target must stay helpful on benign questions.
   中文翻译：7. **Over-refusal measurement.** Track false-positive rate on a benign prompt suite (e.g., XSTest). The target must stay helpful on benign questions.

8. **CVSS scoring.** For each successful jailbreak, score on CVSS 4.0 (attack vector, complexity, impact). Produce a disclosure timeline and mitigation plan.
   中文翻译：8. **CVSS scoring.** For each successful jailbreak, score on CVSS 4.0 (attack vector, complexity, impact). Produce a disclosure timeline and mitigation plan.

9. **Range automation.** Everything above runs on a cron; findings write to a queue; over-refusal regression alerts fire to Slack.
   中文翻译：9. **Range automation.** Everything above runs on a cron; findings write to a queue; over-refusal regression alerts fire to Slack.

## Use It | 使用方法

```
$ safety probe --model=target --family=PAIR --budget=50
[attacker]   PAIR agent running on target
[attack]     attempt 1/50: disguise query as academic research ... blocked
[attack]     attempt 2/50: appeal to roleplay ... blocked
[attack]     attempt 3/50: chain-of-thought coax ... SUCCEEDED
[finding]    CVSS 4.8 medium: roleplay bypass on target
[range]      7 successes out of 50 (14% success rate)
```

## Ship It | 部署上线

`outputs/skill-safety-harness.md` is the deliverable. A production-grade layered safety pipeline plus a reproducible red-team range with before/after harmlessness deltas.

> `outputs/skill-safety-harness.md` 是交付物. A production-grade layered safety pipeline plus a reproducible red-team range with before/after harmlessness deltas.


| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | Attack-surface coverage | 6+ attack families exercised, 2+ languages |
| 20 | True-positive / false-positive trade-off | Attack block rate vs XSTest benign pass rate |
| 20 | Self-critique delta | Before/after harmlessness on held-out eval |
| 20 | Documentation and disclosure | CVSS-scored findings with timeline |
| 15 | Automation and repeatability | Everything runs on cron with alerts |
| **100** | | |

## Exercises | 练习题

1. Run garak's plugin for prompt-injection on a RAG chatbot and compare attack success rate with and without the output-filter layer.

2. Add a seventh attack family: indirect prompt injection via retrieved documents. Measure the extra defense required.

3. Implement a "refuse-with-help" mode: when the guardrail blocks, the target offers a safer related answer instead of a flat refusal. Measure XSTest delta.

4. Multilingual coverage gap: find a language where X-Guard underperforms. Propose a fine-tune dataset targeting it.

5. Run the constitutional self-critique on a 30B model and measure whether the delta scales.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Layered safety | "Defense in depth" | Multiple guardrails at input, gate, output, HITL |
| Llama Guard 4 | "Meta's safety classifier" | The 2026 reference input/output content classifier |
| PAIR | "Jailbreak agent" | Paper (Chao et al.) on LLM-driven jailbreak discovery |
| TAP | "Tree-of-Attacks" | Tree-search variant of PAIR |
| GCG | "Greedy coordinate gradient" | Gradient-based adversarial suffix attack |
| Constitutional self-critique | "Anthropic-style training" | Target drafts -> critic scores -> rewrite -> retrain |
| XSTest | "Benign probe set" | Benchmark for over-refusal regression |
| CVSS 4.0 | "Severity score" | Standard vulnerability scoring for safety findings |

## Further Reading | 延伸阅读

- [Anthropic Constitutional Classifiers](https://www.anthropic.com/research/constitutional-classifiers) — training-time reference
- [Meta Llama Guard 4](https://ai.meta.com/research/publications/llama-guard-4/) — the 2026 input/output classifier
- [Google ShieldGemma-2](https://huggingface.co/google/shieldgemma-2b) — image + multimodal safety
- [NVIDIA Nemotron 3 Content Safety](https://developer.nvidia.com/blog/building-nvidia-nemotron-3-agents-for-reasoning-multimodal-rag-voice-and-safety/) — enterprise reference
- [X-Guard (arXiv:2504.08848)](https://arxiv.org/abs/2504.08848) — 132-language multilingual safety
- [garak](https://github.com/NVIDIA/garak) — NVIDIA red-team toolkit
- [PyRIT](https://github.com/Azure/PyRIT) — Microsoft red-team framework
- [NeMo Guardrails v0.12](https://docs.nvidia.com/nemo-guardrails/) — rail framework
- [PAIR (arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) — jailbreak agent paper
