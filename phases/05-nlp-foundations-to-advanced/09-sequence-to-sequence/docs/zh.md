# 序列到序列模型 (Seq2Seq)

> 两个 RNN 假装是翻译器。它们撞上的瓶颈正是注意力机制存在的原因。

> **【中文解读】** 编码器-解码器架构。注意力机制就是为解决它的瓶颈而发明的。

**类型：** 构建
**编程语言：** Python
**前置课程：** Phase 5 · 08（CNN + RNN 文本处理），Phase 3 · 11（PyTorch 简介）
**预计时长：** ~75 分钟

## 问题引入

分类将变长序列映射为单个标签。翻译将变长序列映射为另一个变长序列。输入和输出在不同的词表中，可能是不同的语言，长度无法保证一致。

> **【中文解读】** 本节提出的问题是：如何在实际工程中正确理解和应用这一技术。理解问题背景有助于把握技术选型的关键决策点。在实际 AI 系统中，错误的技术选型往往比实现细节的 bug 代价更高。


seq2seq 架构（Sutskever, Vinyals, Le, 2014）用一个刻意简单的方案解决了这个问题。两个 RNN。一个读取源句子并产生固定大小的上下文向量。另一个读取该向量并逐 token 生成目标句子。你在第 08 课写的代码，以不同方式粘合在一起。

这值得学习有两个原因。第一，上下文向量瓶颈是 NLP 中最具教学价值的失败。它激发了注意力和 Transformer 擅长的一切。第二，训练方案（教师强制、计划采样、推理时的束搜索）仍然适用于包括 LLM 在内的每个现代生成系统。

## 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


**编码器（Encoder）。** 一个读取源句子的 RNN。其最终隐藏状态是**上下文向量** —— 整个输入的固定大小摘要。据说不会丢失源信息的任何内容。

**解码器（Decoder）。** 另一个从上下文向量初始化的 RNN。在每一步，它将之前生成的 token 作为输入，产生目标词表上的分布。采样或取 argmax 选择下一个 token。将其反馈进去。重复直到产生 `<EOS>` token 或达到最大长度。

**训练：** 每个解码器步骤的交叉熵损失，在序列上求和。通过两个网络的标准时间反向传播。

**教师强制（Teacher Forcing）。** 训练时，解码器在步骤 `t` 的输入是位置 `t-1` 的*真实* token，而不是解码器自己的前一个预测。这稳定了训练；没有它，早期错误会级联，模型永远学不会。推理时，你必须使用模型自己的预测，所以总是存在训练/推理分布差距。这个差距叫做**暴露偏差（Exposure Bias）**。

**瓶颈。** 编码器学到的关于源的一切都必须压缩到那一个上下文向量中。长句子丢失细节。罕见词被模糊。重排序（chat noir vs. black cat）必须记忆，而非计算。

注意力（第 10 课）通过让解码器查看*每个*编码器隐藏状态（而不仅是最后一个）来修复这个问题。这就是全部要点。

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：大语言模型的工程实践】** 从 GPT 到 ChatGPT，NLP 领域经历了从 "每个任务训练一个模型" 到 "一个模型解决所有任务" 的范式转变。在实际工程中，LLM 的部署需要考虑 Token 限制、延迟、成本、安全审查等问题。LangChain、LlamaIndex 等框架简化了 LLM 应用的开发。

> **【拓展：RAG 与企业知识库】** 检索增强生成（RAG）是当前企业 AI 应用最流行的架构：将用户查询先检索相关文档片段，再将检索结果作为上下文喂给 LLM 生成答案。这种方式解决了 LLM 知识过时和幻觉问题。向量数据库（如 Milvus、Pinecone、Weaviate）是 RAG 系统的核心组件。

> **【拓展：NLP 的多语言挑战】** 全球有 7000+ 种语言，但 NLP 研究主要集中在英语等少数语言。跨语言迁移学习、多语言预训练模型（如 mBERT、XLM-R）是解决低资源语言 NLP 的主要方法。字节级模型（如 ByT5）甚至可以在无分词器的情况下处理任何语言。





## 动手实现

### 步骤 1：编码器

```python
import torch
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, src_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(src_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)

    def forward(self, src):
        e = self.embed(src)
        outputs, hidden = self.gru(e)
        return outputs, hidden
```

`outputs` 形状为 `[batch, seq_len, hidden_dim]` —— 每个输入位置一个隐藏状态。`hidden` 形状为 `[1, batch, hidden_dim]` —— 最终步。第 08 课说 "在 outputs 上池化做分类"。这里我们保留最后隐藏状态作为上下文向量，忽略逐步输出。

### 步骤 2：解码器

```python
class Decoder(nn.Module):
    def __init__(self, tgt_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(tgt_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, tgt_vocab_size)

    def forward(self, token, hidden):
        e = self.embed(token)
        out, hidden = self.gru(e, hidden)
        logits = self.fc(out)
        return logits, hidden
```

解码器每次调用一步。输入：一批单个 token 和当前隐藏状态。输出：下一个 token 的词表 logits 和更新后的隐藏状态。

### 步骤 3：教师强制训练循环

```python
def train_batch(encoder, decoder, src, tgt, bos_id, optimizer, teacher_forcing_ratio=0.9):
    optimizer.zero_grad()
    _, hidden = encoder(src)
    batch_size, tgt_len = tgt.shape
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    loss = 0.0
    loss_fn = nn.CrossEntropyLoss(ignore_index=0)

    for t in range(tgt_len):
        logits, hidden = decoder(input_token, hidden)
        step_loss = loss_fn(logits.squeeze(1), tgt[:, t])
        loss += step_loss
        use_teacher = torch.rand(1).item() < teacher_forcing_ratio
        if use_teacher:
            input_token = tgt[:, t].unsqueeze(1)
        else:
            input_token = logits.argmax(dim=-1)

    loss.backward()
    optimizer.step()
    return loss.item() / tgt_len
```

两个值得注意的参数。`ignore_index=0` 跳过填充 token 上的损失。`teacher_forcing_ratio` 是每步使用真实 token 与模型预测的概率。从 1.0（完全教师强制）开始，训练过程中退火到约 0.5 以缩小暴露偏差差距。

### 步骤 4：推理循环（贪心）

```python
@torch.no_grad()
def greedy_decode(encoder, decoder, src, bos_id, eos_id, max_len=50):
    _, hidden = encoder(src)
    batch_size = src.shape[0]
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    output_ids = []
    for _ in range(max_len):
        logits, hidden = decoder(input_token, hidden)
        next_token = logits.argmax(dim=-1)
        output_ids.append(next_token)
        input_token = next_token
        if (next_token == eos_id).all():
            break
    return torch.cat(output_ids, dim=1)
```

贪心解码每步选择最高概率的 token。它可能走偏：一旦你提交了一个 token，就无法撤回。**束搜索（Beam Search）** 保持排名前 `k` 的部分序列存活，在最后选择最高分的完整序列。束宽度 3-5 是标准。

### 步骤 5：瓶颈演示

在玩具复制任务上训练模型：源 `[a, b, c, d, e]`，目标 `[a, b, c, d, e]`。增加序列长度。观察准确率。

```
seq_len=5   复制准确率: 98%
seq_len=10  复制准确率: 91%
seq_len=20  复制准确率: 62%
seq_len=40  复制准确率: 23%
```

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


单个 GRU 隐藏状态无法无损记忆 40 个 token 的输入。信息在每个编码器步骤都存在，但解码器只看到最后状态。注意力直接修复了这个问题。



> **【拓展：Prompt Engineering 与 LLM 应用】** Prompt Engineering 已成为 NLP 工程师的核心技能。从 Zero-shot 到 Few-shot，从 Chain-of-Thought 到 ReAct，不同的提示策略适用于不同场景。在实际项目中，系统提示（System Prompt）的设计直接影响 LLM 应用的稳定性和输出质量。

## 用框架实现

PyTorch 有 `nn.Transformer` 和基于 `nn.LSTM` 的 seq2seq 模板。Hugging Face 的 `transformers` 库提供在数十亿 token 上训练的完整编码器-解码器模型（BART、T5、mBART、NLLB）。

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tok = AutoTokenizer.from_pretrained("facebook/bart-base")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

src = tok("Translate this to French: Hello, how are you?", return_tensors="pt")
out = model.generate(**src, max_new_tokens=50, num_beams=4)
print(tok.decode(out[0], skip_special_tokens=True))
```

现代编码器-解码器用 Transformer 替代了 RNN。高层结构（编码器、解码器、逐 token 生成）与 2014 年的 seq2seq 论文完全相同。每个块内部的机制不同。

### 何时仍然使用基于 RNN 的 seq2seq

对新项目几乎不用。特定例外：

- 流式翻译，逐 token 消耗输入，内存有界。
- 设备端文本生成，Transformer 内存成本过高。
- 教学。理解编码器-解码器瓶颈是理解 Transformer 为什么胜出的最快路径。

### 暴露偏差及其缓解

- **计划采样（Scheduled Sampling）。** 训练期间退火教师强制比例，让模型学会从自己的错误中恢复。
- **最小风险训练（Minimum Risk Training）。** 在句子级 BLEU 分数而非 token 级交叉熵上训练。更接近你真正想要的。
- **强化学习微调。** 用指标奖励序列生成器。用于现代 LLM 的 RLHF。

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


这三者仍然适用于基于 Transformer 的生成。



## 产出物

保存为 `outputs/prompt-seq2seq-design.md`：

```markdown
---
name: seq2seq-design
description: Design a sequence-to-sequence pipeline for a given task.
phase: 5
lesson: 09
---

Given a task (translation, summarization, paraphrase, question rewrite), output:

1. Architecture. Pretrained transformer encoder-decoder (BART, T5, mBART, NLLB) is the default. RNN-based seq2seq only for specific constraints.
2. Starting checkpoint. Name it (`facebook/bart-base`, `google/flan-t5-base`, `facebook/nllb-200-distilled-600M`). Match the checkpoint to task and language coverage.
3. Decoding strategy. Greedy for deterministic output, beam search (width 4-5) for quality, sampling with temperature for diversity. One sentence justification.
4. One failure mode to verify before shipping. Exposure bias manifests as generation drift on longer outputs; sample 20 outputs at the 90th-percentile length and eyeball.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse to recommend training a seq2seq from scratch for under a million parallel examples. Flag any pipeline that uses greedy decoding for user-facing content as fragile (greedy repeats and loops).
```

## 练习题

1. **简单。** 实现玩具复制任务。训练 GRU seq2seq 在目标等于源的输入输出对上。测量长度 5、10、20 的准确率。复现瓶颈。
2. **中等。** 添加束宽度为 3 的束搜索解码。在小平行语料上测量相对于贪心的 BLEU。记录束搜索在哪里胜出（通常是最后几个 token）以及在哪里没有区别。
3. **困难。** 在 1 万对释义数据集上微调 `facebook/bart-base`。在留出输入上比较微调模型的束 4 输出与基础模型。报告 BLEU 并选取 10 个定性示例。

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## 术语速查表

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 编码器（Encoder） | 输入 RNN | 读取源。产生逐步隐藏状态和最终上下文向量。 |
| 解码器（Decoder） | 输出 RNN | 从上下文向量初始化。逐个生成目标 token。 |
| 上下文向量 | 摘要 | 最终编码器隐藏状态。固定大小。注意力解决的瓶颈。 |
| 教师强制 | 使用真实 token | 训练时馈入真实的前一个 token。稳定学习。 |
| 暴露偏差 | 训练/测试差距 | 在真实 token 上训练的模型从未练习从自己的错误中恢复。 |
| 束搜索 | 更好的解码 | 每步保持排名前 k 的部分序列存活，而非贪心提交。 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## 延伸阅读

- [Sutskever, Vinyals, Le (2014). Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215) — 原始 seq2seq 论文。四页。
- [Cho et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078) — 引入了 GRU 和编码器-解码器框架。
- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) — 注意力论文。在本课后立即阅读。
- [PyTorch NLP from Scratch tutorial](https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html) — 可构建的 seq2seq + 注意力代码。
