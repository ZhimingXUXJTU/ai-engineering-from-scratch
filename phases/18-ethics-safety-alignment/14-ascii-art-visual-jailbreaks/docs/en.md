# ASCII Art and Visual Jailbreaks | ASCII 艺术 视觉

> Jiang, Xu, Niu, Xiang, Ramasubramanian, Li, Poovendran, "ArtPrompt: ASCII Art-based Jailbreak Attacks against Aligned LLMs" (ACL 2024, arXiv:2402.11753). Mask the safety-relevant tokens in a harmful request, replace them with ASCII-art renderings of the same letters, and send the cloaked prompt. GPT-3.5, GPT-4, Gemini, Claude, Llama-2 all fail to robustly recognize ASCII-art tokens. The attack bypasses PPL (perplexity filters), Paraphrase defenses, and Retokenization. Related: the ViTC benchmark measures recognition of non-semantic visual prompts; StructuralSleight generalizes to Uncommon Text-Encoded Structures (trees, graphs, nested JSON) as a family of encoding attacks.

> **【中文解读】** 本节介绍了 ASCII 艺术视觉越狱——用文本图形绕过安全过滤器的攻击技术。ArtPrompt（ACL 2024）两步攻击：识别安全相关词，用 ASCII 艺术渲染替换。安全过滤器看到无害的标点符号网格，模型看到一个词。GPT-4、Gemini、Claude、Llama-2 全部失败，攻击成功率超过 75%。

> **【拓展：ArtPrompt → 编码攻击家族】** 标准防御（困惑度过滤、释义、重新分词）在 ArtPrompt 上全部失败，因为安全过滤器在令牌/语义级别操作，而 ArtPrompt 在视觉识别级别操作。StructuralSleight 将此推广到罕见文本编码结构（UTES）——树、图、嵌套 JSON、CSV-in-JSON——任何训练安全数据中罕见但模型可解析的结构都可以隐藏有害内容。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, ArtPrompt token-masking harness) | **语言:** Python（标准库，ArtPrompt token 掩码框架）
**Prerequisites:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ) | **前置知识:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ)
**Time:** ~60 minutes | **时间:** ~60 分钟

> 🔗 **【前置】** 学本节前请先掌握：Phase 18·12-13。视觉越狱 = 用 ASCII 艺术/树状图/JSON 等编码攻击绕过文本过滤器。
> 💡 **【类比】** ASCII 越狱 = "隐形墨水"。安全过滤器看到无害的标点网格，模型视觉理解为一个词。ArtPrompt ACL 2024：GPT-4/Gemini/Claude/Llama-2 全失败，>75% 攻击成功率。绕过 PPL 过滤、改写、重 token 化防御。结构性变种（StructuralSleight）扩展到树/图/嵌套 JSON——所有非语义视觉提示都是攻击面。

## Learning Objectives | 学习目标

- Describe the ArtPrompt attack: word-identification step, ASCII-art substitution, final cloaked prompt.

> 描述 ArtPrompt 攻击：词识别步骤、ASCII 艺术替换、最终伪装提示。

- Explain why standard defenses (PPL, Paraphrase, Retokenization) fail on ArtPrompt.

> 解释为什么标准防御（困惑度过滤、释义、重新分词）在 ArtPrompt 上失败。

- Define ViTC and describe what it measures.

> 定义 ViTC 并描述它衡量的内容。

- Describe StructuralSleight as a generalization to arbitrary Uncommon Text-Encoded Structures.

> 描述 StructuralSleight 作为对任意罕见文本编码结构的推广。

## The Problem | 问题

Attacks via paraphrase and roleplay (Lesson 12) and via long context (Lesson 13) operate on the text-level pattern. ArtPrompt operates at the recognition level: the model does not parse the forbidden token. It parses an image rendered in characters. The safety filter sees harmless punctuation. The model sees a word.

> 通过释义和角色扮演（Lesson 12）和长上下文（Lesson 13）的攻击在文本级模式上操作。ArtPrompt 在识别级别操作：模型不解析禁止的令牌，而是解析以字符渲染的图像。安全过滤器看到无害的标点符号。模型看到一个词。

## The Concept | 概念

> **【中文解读】** ArtPrompt 两步攻击的细节：第一步——给定有害请求，使用 LLM 识别安全相关词（如"bomb"在"how to make a bomb"中）；第二步——将每个识别的词替换为其 ASCII 艺术渲染（7x5 或 7x7 字符块形成字母形状）。模型收到的是标点和空格网格，足够强大的模型可以识别为词；安全过滤器只看到网格。

### ArtPrompt, two steps

Step 1. Word Identification. Given a harmful request, the attacker uses an LLM to identify the safety-relevant words (e.g., "bomb" in "how to make a bomb"). 

Step 2. Cloaked Prompt Generation. Replace each identified word with its ASCII-art rendering (a 7x5 or 7x7 block of characters forming the letter shape). The model receives a grid of punctuation and spaces that a sufficiently capable model can recognize as the word; a safety filter sees only the grid.

Result: GPT-4, Gemini, Claude, Llama-2, GPT-3.5 all fail. Attack success rate above 75% on their benchmark subset.

> 结果：GPT-4、Gemini、Claude、Llama-2、GPT-3.5 全部失败。攻击成功率在基准子集上超过 75%。

> **【拓展：防御失败 → 多层安全启示】** 困惑度过滤器失败是因为合法结构化输入也得分高；释义失败是因为释义 LLM 常保留或重建 ASCII 艺术；重新分词失败是因为识别是视觉的而非令牌级的。安全必须泛化到模型能解析的所有结构化表示——这个集合很大且在增长。

### Why the standard defenses fail

- **PPL (perplexity filter).** ASCII art has high perplexity — but so does all novel input. Threshold choices that block ArtPrompt also block legitimate structured input.

> **困惑度过滤。** ASCII 艺术有高困惑度——但所有新颖输入也是如此。阻止 ArtPrompt 的阈值选择也会阻止合法的结构化输入。

- **Paraphrase.** Paraphrasing the prompt destroys the ASCII art. In practice, paraphrase LLMs often preserve or reconstruct the art.

> **释义。** 释义提示会破坏 ASCII 艺术。实际上，释义 LLM 常常保留或重建艺术。

- **Retokenization.** Splitting tokens differently does not change that the model's vision is recognizing letter shapes.

> **重新分词。** 不同地分割令牌不会改变模型的视觉在识别字母形状的事实。

The underlying issue is that safety filters are token- or semantic-level; ArtPrompt operates at the visual recognition level.

> 根本问题是安全过滤器在令牌或语义级别操作；ArtPrompt 在视觉识别级别操作。

> **【中文解读】** ViTC 基准：ArtPrompt 的有效性与模型读取视觉文本的能力相关——ViTC 准确率越高，ArtPrompt 越有效。这是一个能力-安全权衡：提升模型的多模态理解能力会同时增加编码攻击的脆弱性。视觉 LLM（GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1）扩展了攻击面——实际图像的 ArtPrompt 式攻击比 ASCII 艺术更强。

### ViTC benchmark

Recognition of non-semantic visual prompts. Measures the model's ability to read ASCII-art, wingdings, and other non-text-semantic visual content. ArtPrompt's effectiveness correlates with ViTC accuracy: the better the model reads visual text, the better ArtPrompt works on it. This is a capability-safety tradeoff.

> 非语义视觉提示的识别。衡量模型读取 ASCII 艺术、Wingdings 和其他非文本语义视觉内容的能力。ArtPrompt 的有效性与 ViTC 准确率相关：模型读取视觉文本越好，ArtPrompt 效果越好。这是能力-安全权衡。

### StructuralSleight

Generalizes ArtPrompt: Uncommon Text-Encoded Structures (UTES). Trees, graphs, nested JSON, CSV-in-JSON, diff-style code blocks. If a structure is rare in training safety data but parseable by the model, it can hide harmful content.

> 推广 ArtPrompt：罕见文本编码结构（UTES）。树、图、嵌套 JSON、JSON 中的 CSV、diff 风格代码块。如果一个结构在训练安全数据中罕见但模型可解析，它就可以隐藏有害内容。

The defense implication: safety must generalize across the structured representations the model can parse. The set is large and growing.

> 防御启示：安全必须泛化到模型能解析的所有结构化表示。这个集合很大且在增长。

### Image-modality analog

Visual LLMs (GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) extend the attack surface. ArtPrompt-style attacks with actual images are stronger than ASCII-art analogs because image encoders produce richer signal.

> 视觉 LLM 扩展了攻击面。使用实际图像的 ArtPrompt 式攻击比 ASCII 艺术更强，因为图像编码器产生更丰富的信号。

### Where this fits in Phase 18

Lessons 12-14 describe three orthogonal attack vectors: iterative refinement (PAIR), context length (MSJ), and encoding (ArtPrompt/StructuralSleight). Lesson 15 shifts from model-centric attacks to system-boundary attacks (indirect prompt injection). Lesson 16 describes the defensive tooling response.

> Lessons 12-14 描述三个正交攻击向量：迭代改进（PAIR）、上下文长度（MSJ）和编码（ArtPrompt/StructuralSleight）。Lesson 15 从模型中心攻击转向系统边界攻击。Lesson 16 描述防御工具响应。

> **【拓展：视觉 LLM → 攻击面扩展】** 视觉 LLM（GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1）扩展了攻击面。ArtPrompt 式攻击使用实际图像比 ASCII 艺术更强，因为图像编码器产生更丰富的信号。ViTC 基准的相关性意味着提升多模态能力同时增加了编码攻击的脆弱性——这是 AI 安全中反复出现的能力-安全权衡。

## Use It | 使用方法

`code/main.py` builds a toy ArtPrompt. You can cloak specific words in a harmful query with ASCII-art glyphs, verify the cloaked string passes a keyword filter, and (optionally) decode the cloaked string back using a simple recognizer.

> `code/main.py` 构建了一个玩具 ArtPrompt。你可以用 ASCII 艺术字形伪装有害查询中的特定词，验证伪装字符串通过关键词过滤，并（可选地）使用简单识别器解码。

## Ship It | 部署上线

This lesson produces `outputs/skill-encoding-audit.md`. Given a jailbreak-defense report, it enumerates the encoding attack families covered (ASCII art, base64, leet-speak, UTF-8 homoglyph, UTES) and the defense layer that catches each.

> 本课产出 `outputs/skill-encoding-audit.md`。给定越狱防御报告，列举覆盖的编码攻击家族及每个对应的防御层。

## Exercises | 练习题

1. Run `code/main.py`. Verify the cloaked string passes a simple keyword filter. Report the character-level change required.

2. Implement a second encoding: base64 for the same target word. Compare the filter-bypass rate against ArtPrompt and the recovery difficulty.

3. Read Jiang et al. 2024 Section 4.3 (five-model results). Propose a reason why Claude's ArtPrompt-resistance is higher than Gemini's on the same benchmark.

4. Design a pre-generation defense that detects ASCII-art-shaped regions in the prompt. Measure the false-positive rate on legitimate code, tables, and mathematical notation.

5. StructuralSleight lists 10 encoding structures. Sketch a generalized defense that handles all 10 and estimate the compute cost per defended prompt.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| ArtPrompt | "the ASCII-art attack" | Two-step jailbreak that masks safety words with ASCII-art renderings |
| Cloaking | "hide the word" | Replace a forbidden token with a visual representation the model reads but the filter does not |
| UTES | "uncommon structure" | Uncommon Text-Encoded Structure — tree, graph, nested JSON, etc. used to smuggle content |
| ViTC | "visual-text capability" | Benchmark for model's ability to read non-semantic visual encoding |
| Perplexity filter | "PPL defense" | Reject prompts with high perplexity; fails because legitimate structured input also scores high |
| Retokenization | "tokenizer shift defense" | Pre-process the prompt with a different tokenizer; fails because recognition is visual |
| Homoglyph | "lookalike characters" | Unicode characters that look identical to Latin letters; bypass substring checks |

## Further Reading | 延伸阅读

- [Jiang et al. — ArtPrompt (ACL 2024, arXiv:2402.11753)](https://arxiv.org/abs/2402.11753) — the ASCII-art jailbreak paper
- [Li et al. — StructuralSleight (arXiv:2406.08754)](https://arxiv.org/abs/2406.08754) — UTES generalization
- [Chao et al. — PAIR (Lesson 12, arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) — complementary iterative attack
- [Anil et al. — Many-shot Jailbreaking (Lesson 13)](https://www.anthropic.com/research/many-shot-jailbreaking) — complementary length attack
