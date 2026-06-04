# Capstone Lesson 39: Instruction Tuning by Supervised Fine-Tuning | 微调 结业

> A pretrained base model can extend a sequence but cannot follow an instruction. Supervised fine-tuning is the smallest change that fixes this: feed the model paired examples of an instruction and a desired response, and train the body to predict the response tokens. The trick is that you only want the loss to count the response, not the instruction. This lesson builds an Alpaca-style SFT loop with a custom collate function that masks instruction tokens with `ignore_index=-100`, trains on 200 instruction-response pairs, and evaluates on a held-out split using exact-match.

> **【中文解读】** 本节是综合项目——实现指令微调 SFT。


**Type:** Build
**Languages:** Python (torch, numpy)
**Prerequisites:** Phase 19 lessons 30-37 (NLP LLM track: tokenizer, embedding table, attention block, transformer body, pre-training loop, checkpointing, generation, perplexity)
**Time:** ~90 minutes

## Learning Objectives | 学习目标

- Format paired instruction-response data into a single causal sequence with explicit boundary tokens.
- Build a collate function that masks instruction tokens so cross-entropy only counts response tokens.
- Train a tiny transformer body under the SFT objective and watch the eval metric move.
- Implement greedy and temperature-sampled generation that respects the response-start boundary.
- Compute held-out exact-match on generated completions.

## The Problem | 问题

> **【中文解读】** 基座模型在"下一个 token 预测"上训练，不知道什么是指令。给它 "What is the capital of France?"，它会继续提问或发明新句子。SFT 的修正是将指令-响应对格式化为带边界 token 的因果序列，但只在响应 token 上计算损失——指令 token 的目标位置设为 `-100`（`ignore_index`），贡献零梯度和零损失。

> **【拓展：SFT 数据集与对齐研究】** Alpaca (Stanford, 2023) 使用 GPT-3.5 生成的 52K 指令-响应对，开创了"自我指导"(Self-Instruct) 范式。LIMA (Meta, 2023) 证明仅需 1000 个高质量示例就能训练出竞争力强的模型。Dolly (Databricks) 和 OpenAssistant 提供开源 SFT 数据集。现代 SFT 通常使用聊天模板（ChatML、ChatML-Legacy、LLaMA Chat 等），支持多轮对话。损失掩码（本课的核心技巧）在所有框架中都是标准实践。 Show it the string `"What is the capital of France?"` and it will continue the question or invent a new sentence. The model has the language but not the format contract.

The SFT contract is a string template. Every training example becomes a single sequence with three regions:

```text
<INST> What is the capital of France? <RESP> The capital of France is Paris.
```

The boundary tokens are special tokens reserved at training time. The model learns that everything after `<RESP>` is the response and the response is what gets graded. The base model's next-token objective still applies; it is just trained on a corpus where every example has this shape.

But there is a catch. If you feed the entire sequence to a vanilla cross-entropy loss, you are training the model to also predict the instruction tokens. The instruction is given. You want zero gradient on those positions. The fix is the mask.

## The Concept | 概念

> **【中文解读】** SFT 的概念图：指令-响应对 -> 应用模板（插入 INST + RESP 边界 token）-> 编码为 token ID -> 构建 loss mask（指令位置设为 -100）-> 送入 Transformer -> 仅在响应 token 上计算交叉熵损失。模型在前向传播中能看到指令（注意力可以关注指令），但损失只在响应部分计算。这实现了"以指令为条件，预测响应"。

```mermaid
flowchart LR
  Pair[instruction + response] --> Tmpl[apply template<br/>INST + RESP tokens]
  Tmpl --> Tokens[token ids]
  Tokens --> Mask[loss mask<br/>-100 on instruction]
  Mask --> Model[transformer body + LM head]
  Model --> CE[cross-entropy<br/>ignore_index=-100]
  CE --> Step[backward + optimiser step]
```

`ignore_index` is a feature of `torch.nn.functional.cross_entropy`. Any target position equal to `ignore_index` contributes zero loss and zero gradient. The convention in PyTorch is `-100`. The collate function builds two tensors per example: `input_ids` (the full sequence) and `labels` (a copy of `input_ids` with the instruction positions overwritten by `-100`).

The model sees the whole sequence during the forward pass; attention can attend to the instruction. The loss only counts response tokens. This is exactly what you want: condition on the instruction, predict the response.

## The Data

> **【拓展：SFT 数据质量的重要性】** LIMA (Meta, 2023) 的核心发现是"数据质量比数量更重要"——1000 个精心标注的示例训练出的模型，在人类评估中优于用 52K 自动生成数据训练的 Alpaca。本课的 200 个确定性生成样本覆盖了 6 种任务类型（事实问答、算术、列表提取、摘要、代码、定义），每种任务的难度梯度从简单到复杂。生产级 SFT 数据集通常需要 10K-100K 高质量样本，数据清洗和去重是关键的前置步骤。

Two hundred instruction-response pairs are generated deterministically in `main.py`. They cover six task types:

- factual single-shot (capital of X)
- arithmetic
- list extraction
- one-sentence summary
- code (print, sort)
- definition

Each task has a templated instruction and a deterministic response. This is intentionally simple. Exact-match is brittle, and the lesson uses a fixture where the right answer is one specific string. Real SFT datasets need fuzzy metrics; the principle is identical.

Splits are 160 train, 40 test. The test set covers all six task types so per-category exact-match can be reported.

## Tokenisation and Padding

The tokeniser is byte-level with three reserved specials:

- `INST_ID = 256`: marks the start of the instruction region.
- `RESP_ID = 257`: marks the boundary between instruction and response.
- `PAD_ID = 258`: padding for variable-length batches.

The sequence is `[INST] inst_bytes [RESP] resp_bytes [PAD]*`. The collate function:

1. Tokenises each example.
2. Pads every example in the batch to the longest sequence in the batch.
3. Builds `labels` = `input_ids` shifted by one (causal LM target), with:
   - The instruction region replaced by `-100`.
   - The padding region replaced by `-100`.
   - The `RESP_ID` boundary position itself replaced by `-100` (you do not train the model to predict the boundary token; it predicts what follows).

```mermaid
flowchart TD
  Batch[(examples)] --> Tok[encode + insert specials]
  Tok --> Pad[pad to longest]
  Pad --> Shift[shift labels by one]
  Shift --> Mask[set -100 on<br/>inst / pad / boundary]
  Mask --> Out[(input_ids, labels)]
```

The shift is the standard causal trick: position `i` of `input_ids` predicts position `i+1`, so `labels[i] = input_ids[i+1]` (with the final position dropped from the input and the first dropped from the target). The mask is applied after the shift to land on the right positions.

## Training

```mermaid
flowchart LR
  DL[Train loader<br/>200 pairs] --> Fwd[forward]
  Fwd --> Logits[B x T x V]
  Logits --> Loss[CE with -100 mask]
  Loss --> Bwd[backward]
  Bwd --> Opt[Adam optimiser]
  Opt --> Body[(updated body)]
```

The loop is the standard PyTorch SFT loop. Adam, learning rate around 3e-4 to 1e-3, ten to twenty epochs on this fixture, no scheduler. The model is small enough (hidden 96, 2 blocks, max length 64) to train to convergence on CPU inside two minutes.

Every fifth epoch the loop runs a tiny eval pass on the held-out set and prints exact-match. Watching exact-match go from 0.0 at epoch one to something like 0.85 at epoch fifteen is the lesson's payoff: you can see the model learning the format and the answers at the same time.

## Generation

At eval time the model gets the instruction prefix `[INST] inst_bytes [RESP]` and generates tokens until either:

- the sequence reaches `max_len`, or
- the model emits a special stop heuristic: two consecutive sentence-ending bytes (`.`, `!`, `?`).

The lesson ships greedy decoding plus an optional temperature sampler. Exact-match uses greedy because temperature would make the metric stochastic. Real systems often sample, then judge fuzzily; that pipeline is lesson 41.

## Exact-Match Evaluation

Exact-match is the strictest text metric. The predicted response string is normalised (lowercase, strip whitespace, collapse double spaces) and compared to the reference response, normalised the same way. The metric is either 1 or 0 per example. The aggregate is the mean.

Real SFT pipelines complement exact-match with token-level F1 (lesson 41) and a judge model. Exact-match remains useful because it is unambiguous; if it says 0.7, exactly 70 percent of test instructions produced the gold response character for character.

## What you will build

The implementation is one `main.py` plus tests.

1. `InstructionTokenizer`: byte-level encoder with reserved specials. Encodes either an instruction prefix or a full pair.
2. `make_dataset`: generates 200 pairs across six task types with a fixed seed.
3. `SFTDataset`: returns `(input_ids, labels)` per example, already mask-prepared.
4. `sft_collate`: dynamic padding, builds the batch tensor, sets `-100` on instruction and pad positions.
5. `TinyGPT`: transformer body plus tied or untied LM head.
6. `train_sft`: the SFT loop, with per-epoch eval hooks.
7. `generate`: causal decode from a prefix, greedy or sampled, with the stop heuristic.
8. `exact_match`: normalised string comparison, returns float in `[0, 1]`.
9. `run_demo`: builds the data, trains for twenty epochs, evaluates, prints a per-category breakdown, exits zero on success.

## Why the mask matters

> **【中文解读】** 没有掩码，损失将指令 token 也作为目标，模型学习预测指令。这浪费模型容量重建用户总提供的输入，且响应损失在梯度和中占比更小（指令 token 数通常多于响应 token），有效学习率低于预期。掩码不是润色，而是目标函数本身。

Without the mask, the loss treats instruction tokens as targets. The model learns to predict the instruction. This is a different objective and produces a worse model in two ways. First, model capacity is wasted reconstructing inputs the user always provides. Second, the response loss is smaller in the gradient sum because instruction tokens outnumber response tokens in most batches; the optimiser's effective learning rate on the part you care about is lower than you intended. The mask is not a polish; it is the objective.

## Stretch goals

- Add a learning-rate warmup followed by cosine decay. SFT is more sensitive to LR than pretraining.
- Add per-token loss logging and plot the loss curve over training. Notice that early epochs are dominated by template tokens (`<RESP>`, common prefixes) and later epochs are dominated by the actual answer tokens.
- Extend the eval to BLEU-1 or chrF. Exact-match underestimates models that produce a paraphrase with the same answer.
- Add a chat template with multi-turn formatting and train on a fixture that includes follow-ups.

The implementation gives you the format contract, the mask, and the loop. The objective change from base model to instruction follower is one collate function.
