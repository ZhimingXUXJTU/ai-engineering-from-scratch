# Machine Translation | 机器翻译

> Translation is the task that paid for NLP research for thirty years and keeps paying now.

> **【中文解读】** 从统计机器翻译到神经机器翻译。现代用 Transformer。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes

## The Problem | 问题引入

A model reads a sentence in one language and produces a sentence in another. Length varies. Word order varies. Some source words map to multiple target words and vice versa. Idioms refuse one-to-one mapping. "I miss you" in French is "tu me manques" — literally "you are lacking to me." No word-level alignment survives that.

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


Machine translation is the task that forced NLP to invent encoder-decoders, attention, transformers, and eventually the whole LLM paradigm. Every step forward arrived because translation quality was measurable and the gap between human and machine was stubborn.

This lesson skips the history lesson and teaches the working pipeline of 2026: pretrained multilingual encoder-decoder (NLLB-200 or mBART), subword tokenization, beam search, BLEU and chrF evaluation, and the handful of failure modes that still ship to production uncaught.

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


![MT pipeline: tokenize → encode → decode with attention → detokenize](../assets/mt-pipeline.svg)

Modern MT is a transformer encoder-decoder trained on parallel text. The encoder reads the source in its language's tokenization. The decoder generates the target, one subword at a time, using the encoder's output via cross-attention (lesson 10). Decoding uses beam search to avoid the greedy-decoding trap. The output is detokenized, detruecased, and scored against a reference.

Three operational choices drive real-world MT quality.

- **Tokenizer.** SentencePiece BPE trained on a mixed-language corpus. Shared vocabulary across languages is what enables zero-shot pairs in NLLB.
- **Model size.** NLLB-200 distilled 600M fits on a laptop. NLLB-200 3.3B is the published production default. 54.5B is the research ceiling.
- **Decoding.** Beam width 4-5 for general content. Length penalty to avoid too-short output. Constrained decoding when you need terminology consistency.

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。





## Build It | 动手实现

### Step 1: a pretrained MT call

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_id = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(model_id, src_lang="eng_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

src = "The cats are running."
inputs = tok(src, return_tensors="pt")

out = model.generate(
    **inputs,
    forced_bos_token_id=tok.convert_tokens_to_ids("fra_Latn"),
    num_beams=5,
    length_penalty=1.0,
    max_new_tokens=64,
)
print(tok.batch_decode(out, skip_special_tokens=True)[0])
```

```text
Les chats courent.
```

Three things matter here. `src_lang` tells the tokenizer which script and segmentation to apply. `forced_bos_token_id` tells the decoder which language to generate. Both are NLLB-specific tricks; mBART and M2M-100 use their own conventions and they are not interchangeable.

### Step 2: BLEU and chrF

BLEU measures n-gram overlap between output and reference. Four reference n-gram sizes (1-4), geometric mean of precisions, brevity penalty for too-short output. The score is in [0, 100]. Commonly used. Frustrating to interpret: 30 BLEU is "usable"; 40 is "good"; 50 is "exceptional"; differences under 1 BLEU are noise.

chrF measures character-level F-score. More sensitive to morphologically rich languages where BLEU undercounts matches. Often reported alongside BLEU.

```python
import sacrebleu

hypotheses = ["Les chats courent."]
references = [["Les chats courent."]]

bleu = sacrebleu.corpus_bleu(hypotheses, references)
chrf = sacrebleu.corpus_chrf(hypotheses, references)
print(f"BLEU: {bleu.score:.1f}  chrF: {chrf.score:.1f}")
```

Always use `sacrebleu`. It normalizes tokenization so scores are comparable across papers. Rolling your own BLEU computation is how misleading benchmarks happen.

### The three-tier evaluation hierarchy (2026)

Modern MT evaluation uses three complementary metric families. Ship with at least two.

- **Heuristic** (BLEU, chrF). Fast, reference-based, interpretable, insensitive to paraphrase. Use for legacy comparison and regression detection.
- **Learned** (COMET, BLEURT, BERTScore). Neural models trained on human judgment; compare semantic similarity of translation to source and reference. COMET has the highest association with MT research since 2023 and is the 2026 production default where quality matters.
- **LLM-as-judge** (reference-free). Prompt a large model to score translations on fluency, adequacy, tone, cultural appropriateness. GPT-4-as-judge matches human agreement ~80% of the time when the rubric is well designed. Use for open-ended content where no reference exists.

Practical 2026 stack: `sacrebleu` for BLEU and chrF, `unbabel-comet` for COMET, and a prompted LLM for the final human-facing signal. Calibrate every metric against 50-100 human-labeled examples before trusting it on production data.

Reference-free metrics (COMET-QE, BLEURT-QE, LLM-as-judge) let you evaluate translations without a reference, which matters for long-tail language pairs where reference translations do not exist.

### Step 3: what breaks in production

The working pipeline above will translate fluently 80% of the time and silently fail the remaining 20%. Named failure modes:

- **Hallucination.** Model invents content that was not in the source. Common in unfamiliar domain vocabulary. Symptom: output is fluent but claims facts the source did not state. Mitigation: constrained decoding on domain terms, human review on regulated content, monitoring for output much longer than input.
- **Off-target generation.** Model translates into the wrong language. NLLB is surprisingly prone to this on rare language pairs. Mitigation: verify `forced_bos_token_id` and always decode with a language-ID model check on output.
- **Terminology drift.** "Sign up" becomes "s'inscrire" in doc 1 and "créer un compte" in doc 2. For UI text and user-facing strings, consistency matters more than raw quality. Mitigation: glossary-constrained decoding or post-edit dictionary.
- **Formality mismatch.** French "tu" vs "vous", Japanese politeness levels. The model picks whichever form was more common in training. For customer-facing content this is usually wrong. Mitigation: prompt prefix with a formality token if the model supports it, or fine-tune a small model on formal-only corpora.
- **Length explosion on short input.** Very short input sentences often produce overlong translations because the length penalty falls off a cliff below ~5 source tokens. Mitigation: hard max-length cap proportional to source length.

### Step 4: fine-tuning for a domain

Pretrained models are generalists. Legal, medical, or game-dialog translation benefits measurably from fine-tuning on domain parallel data. The recipe is not exotic:

```python
from transformers import Trainer, TrainingArguments
from datasets import Dataset

pairs = [
    {"src": "The defendant pleaded guilty.", "tgt": "L'accusé a plaidé coupable."},
]

ds = Dataset.from_list(pairs)


def preprocess(ex):
    return tok(
        ex["src"],
        text_target=ex["tgt"],
        truncation=True,
        max_length=128,
        padding="max_length",
    )


ds = ds.map(preprocess, remove_columns=["src", "tgt"])

args = TrainingArguments(output_dir="out", per_device_train_batch_size=4, num_train_epochs=3, learning_rate=3e-5)
Trainer(model=model, args=args, train_dataset=ds).train()
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


A few thousand high-quality parallel examples beats a few hundred thousand noisy web-scraped ones. Quality of training data is the single largest production lever.




> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## Use It | 用框架实现

The 2026 production stack for MT:

| Use case | Recommended starting point |
|---------|---------------------------|
| Any-to-any, 200 languages | `facebook/nllb-200-distilled-600M` (laptop) or `nllb-200-3.3B` (production) |
| English-centric, high quality, 50 languages | `facebook/mbart-large-50-many-to-many-mmt` |
| Short runs, cheap inference, English-French/German/Spanish | Helsinki-NLP / Marian models |
| Latency-critical browser-side | ONNX-quantized Marian (~50 MB) |
| Maximum quality, willing to pay | GPT-4 / Claude / Gemini with translation prompts |

LLMs now outperform specialized MT models on several language pairs as of 2026, particularly on idiomatic content and long context. The tradeoff is per-token cost and latency. Pick an LLM when context length, stylistic consistency, or domain adaptation via prompting matters more than throughput.

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。




## Ship It | 产出物

Save as `outputs/skill-mt-evaluator.md`:

```markdown
---
name: mt-evaluator
description: Evaluate a machine translation output for shipping.
version: 1.0.0
phase: 5
lesson: 11
tags: [nlp, translation, evaluation]
---

Given a source text and a candidate translation, output:

1. Automatic score estimate. BLEU and chrF ranges you would expect. State whether a reference is available.
2. Five-point human-verifiable check list: (a) content preservation (no hallucinations), (b) correct language, (c) register / formality match, (d) terminology consistency with glossary if provided, (e) no truncation or length explosion.
3. One domain-specific issue to probe. E.g., for legal: named entities and statute citations. For medical: drug names and dosages. For UI: placeholder variables `{name}`.
4. Confidence flag. "Ship" / "Ship with review" / "Do not ship". Tie to the severity of issues found in step 2.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse to ship a translation without a language-ID check on output. Refuse to evaluate without a reference unless the user explicitly opts in to reference-free scoring (COMET-QE, BLEURT-QE). Flag any content over 1000 tokens as likely needing chunked translation.
```

## Exercises | 练习题

1. **Easy.** Translate a 5-sentence English paragraph to French and back to English using `nllb-200-distilled-600M`. Measure how close the round-trip is to the original. You should see semantic preservation with word-choice drift.
2. **Medium.** Implement a language-ID check on translation outputs using `fasttext lid.176` or `langdetect`. Integrate into the MT call so off-target generations are caught before returning.
3. **Hard.** Fine-tune `nllb-200-distilled-600M` on a 5,000-pair domain corpus of your choice. Measure BLEU on a held-out set before and after fine-tuning. Report which kinds of sentences improved and which regressed.

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BLEU | Translation score | N-gram precision with brevity penalty. [0, 100]. |
| chrF | Character F-score | Character-level F-score. More sensitive for morphologically rich languages. |
| NMT | Neural MT | Transformer encoder-decoder trained on parallel text. The 2017+ default. |
| NLLB | No Language Left Behind | Meta's 200-language MT model family. |
| Constrained decoding | Controlled output | Force specific tokens or n-grams to appear / not appear in the output. |
| Hallucination | Invented content | Model output that is not supported by the source. |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672) — the NLLB paper.
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/) — why `sacrebleu` is the only correct way to report BLEU.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) — the chrF paper.
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) — practical fine-tuning walkthrough.
