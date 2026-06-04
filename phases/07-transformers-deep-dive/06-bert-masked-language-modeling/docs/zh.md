# BERT — Masked Language Modeling | BERT — 掩码语言模型

> GPT 预测下一个词。BERT 预测缺失的词。一句话的区别——以及半个世纪所有嵌入类应用的基础。

> **【中文解读】** BERT 是 Encoder-only Transformer，用掩码预测训练。理解 BERT = 理解双向上下文建模。用于文本分类、NER、问答等。

**类型：** 构建
**语言：** Python
**前置条件：** 阶段 7 · 05（完整 Transformer），阶段 5 · 02（文本表示）
**时长：** 约 45 分钟

## 问题引入

2018 年，每个 NLP 任务——情感分析、NER、QA、蕴涵——都在自己的标注数据上从头训练自己的模型。没有预训练的"理解英语"检查点可供微调。ELMo（2018）展示了你可以用双向 LSTM 预训练上下文嵌入；它有帮助但没有泛化。

BERT（Devlin 等人 2018）提出：如果我们用一个 Transformer 编码器，在互联网上的所有句子上训练它，并强制它从两侧上下文预测缺失的词呢？然后你在下游任务上微调一个头。参数效率是一个启示。

结果：在 18 个月内，BERT 及其变体（RoBERTa、ALBERT、ELECTRA）主导了所有存在的 NLP 排行榜。到 2020 年，地球上每个搜索引擎、内容审核管道和语义搜索系统都有一个 BERT。

2026 年，纯编码器模型仍然是分类、检索和结构化提取的正确工具——它们每个 token 的运行速度比解码器快 5-10 倍，其嵌入是每个现代检索栈的骨干。ModernBERT（2024 年 12 月）通过 Flash Attention + RoPE + GeGLU 将架构推到了 8K 上下文。

> **【中文解读】** BERT 的革命性在于"预训练+微调"范式：在大规模无标注语料上用掩码语言模型（MLM）预训练，然后在特定任务上微调少量参数。编码器的双向注意力让它能同时利用左右上下文预测被掩码的词，这是自回归模型（如 GPT）做不到的。

## 核心概念

![掩码语言建模：选择 token，掩码它们，预测原始 token](../assets/bert-mlm.svg)

### 训练信号

取一个句子：`the quick brown fox jumps over the lazy dog`。

随机掩码 15% 的 token：

```
输入:  the [MASK] brown fox jumps [MASK] the lazy dog
目标: the quick brown fox jumps over  the lazy dog
```

训练模型预测掩码位置的原始 token。因为编码器是双向的，在位置 1 预测 `[MASK]` 可以使用位置 2+ 的 `brown fox jumps`。这是 GPT 做不到的。

### BERT 掩码规则

在被选中进行预测的 15% token 中：

- 80% 被替换为 `[MASK]`。
- 10% 被替换为随机 token。
- 10% 保持不变。

为什么不总是 `[MASK]`？因为 `[MASK]` 在推理时永远不会出现。训练模型在 100% 的掩码位置期望 `[MASK]` 会在预训练和微调之间创建分布偏移。10% 随机 + 10% 不变让模型保持诚实。

> **【中文解读】** BERT 掩码的三条规则（80% [MASK]、10% 随机替换、10% 保持不变）是为了缩小预训练和微调之间的分布差异。推理时不会出现 [MASK] token，所以需要让模型在训练时也见到正常和随机替换的 token。

> **【拓展：BERT 在 RAG 系统中的角色】** 现代 RAG（检索增强生成）系统中，BERT 变体仍然是检索阶段的核心。sentence-transformers 模型（如 all-MiniLM-L6-v2）本质上就是用对比学习微调的 BERT。交叉编码器（cross-encoder）重排序器也是 BERT 架构——它让查询和文档在同一注意力层中交互，质量远超双编码器。

### 下一句预测 (NSP) —— 以及为什么被放弃

原始 BERT 还在 NSP 上训练：给定两个句子 A 和 B，预测 B 是否跟在 A 后面。RoBERTa（2019）消融实验表明 NSP 有害而非有益。现代编码器跳过了它。

### 2026 年的变化：ModernBERT

2024 年 ModernBERT 论文用 2026 年的原语重建了块：

| 组件 | 原始 BERT（2018） | ModernBERT（2024） |
|------|-------------------|-------------------|
| 位置编码 | 学习式绝对编码 | RoPE |
| 激活函数 | GELU | GeGLU |
| 归一化 | LayerNorm | 前归一化 RMSNorm |
| 注意力 | 完全密集 | 交替局部（128）+ 全局 |
| 上下文长度 | 512 | 8192 |
| 分词器 | WordPiece | BPE |

与 2018 年堆栈不同，它是 Flash-Attention 原生的。推理速度在序列长度 8K 时比 DeBERTa-v3 快 2-3 倍，同时 GLUE 分数更高。

### 2026 年仍然选择编码器的用例

| 任务 | 为什么编码器胜过解码器 |
|------|----------------------|
| 检索 / 语义搜索嵌入 | 双向上下文 = 每个 token 更好的嵌入质量 |
| 分类（情感、意图、毒性） | 一次前向传播；无生成开销 |
| NER / token 标注 | 逐位置输出，天然双向 |
| 零样本蕴涵（NLI） | 编码器顶部的分类器头 |
| RAG 重排序器 | 交叉编码器评分，比 LLM 重排序器快 10 倍 |

## 动手实现

### 步骤 1：掩码逻辑

参见 `code/main.py`。函数 `create_mlm_batch` 接收 token ID 列表、词汇表大小和掩码概率。返回输入 ID（应用了掩码）和标签（仅在掩码位置，其他位置为 -100——PyTorch 的忽略索引约定）。

```python
def create_mlm_batch(tokens, vocab_size, mask_prob=0.15, rng=None):
    input_ids = list(tokens)
    labels = [-100] * len(tokens)
    for i, t in enumerate(tokens):
        if rng.random() < mask_prob:
            labels[i] = t
            r = rng.random()
            if r < 0.8:
                input_ids[i] = MASK_ID
            elif r < 0.9:
                input_ids[i] = rng.randrange(vocab_size)
            # 否则：保持原始
    return input_ids, labels
```

### 步骤 2：在微型语料上运行 MLM 预测

在 20 个词的词汇表、200 个句子上训练一个 2 层编码器 + MLM 头。无梯度——我们做前向传播健全性检查。完整训练需要 PyTorch。

### 步骤 3：比较掩码类型

展示三向规则如何让模型在没有 `[MASK]` 的情况下也可用。在未掩码句子和掩码句子上预测。两者都应该产生合理的 token 分布，因为模型在训练中看到了两种模式。

### 步骤 4：微调头

在玩具情感数据集上用分类头替换 MLM 头。只有头训练；编码器冻结。这是每个 BERT 应用遵循的模式。

> **【拓展：BERT 微调的实践技巧】** BERT 微调的最佳实践包括：(1) 使用较小的学习率（2e-5 到 5e-5）避免破坏预训练权重；(2) 对分类任务使用 [CLS] token 的输出作为句子表示；(3) 对于 NER 等逐 token 任务，使用每个位置的输出；(4) 逐步解冻（gradual unfreezing）可以在小数据集上提升泛化能力。

## 用框架实现

```python
from transformers import AutoModel, AutoTokenizer

tok = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base")

text = "Attention is all you need."
inputs = tok(text, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, N, 768)
```

**嵌入模型是微调过的 BERT。** `sentence-transformers` 模型如 `all-MiniLM-L6-v2` 是用对比损失训练的 BERT。编码器相同。损失函数改变了。

**交叉编码器重排序器也是微调过的 BERT。** `[CLS] query [SEP] doc [SEP]` 上的对分类。查询和文档之间的双向注意力正是交叉编码器在质量上超越双编码器的原因。

**2026 年何时不选 BERT。** 任何生成式任务。编码器没有合理的方式自回归地生成 token。另外：1B 参数以下的任何场景，小解码器可以以更大的灵活性匹配质量（Phi-3-Mini、Qwen2-1.5B）。

> **【拓展：ModernBERT 的现代化改进】** ModernBERT（2024）将 2018 年的 BERT 架构全面升级：RoPE 替代学习式位置编码、GeGLU 替代 GELU、前归一化 RMSNorm 替代后归一化 LayerNorm、交替使用局部和全局注意力以支持 8K 上下文。推理速度比 DeBERTa-v3 快 2-3 倍，同时 GLUE 分数更高。

## 产出物

参见 `outputs/skill-bert-finetuner.md`。该技能为新的分类或提取任务规划 BERT 微调（骨干选择、头规格、数据、评估、停止条件）。

## 练习题

1. **简单。** 运行 `code/main.py` 并打印 10,000 个 token 的掩码分布。确认约 15% 被选中，其中约 80% 变为 `[MASK]`。
2. **中等。** 实现全词掩码：如果一个词被分词为子词，则一起掩码所有子词或都不掩码。测量这是否在 500 句语料上提高了 MLM 准确率。
3. **困难。** 在公开数据集的 10,000 个句子上训练一个微型（2 层，d=64）BERT。对 `[CLS]` token 进行 SST-2 情感分析微调。与匹配参数的纯解码器基线比较——谁赢？

## 术语速查表

| 术语 | 人们的说法 | 实际含义 |
|------|-----------|---------|
| MLM | "掩码语言建模" | 训练信号：随机将 15% 的 token 替换为 `[MASK]`，预测原始 token。 |
| 双向 | "两边都看" | 编码器注意力没有因果掩码——每个位置看到所有其他位置。 |
| `[CLS]` | "池化 token" | 预置到每个序列的特殊 token；其最终嵌入用作句子级表示。 |
| `[SEP]` | "段分隔符" | 分隔配对序列（例如查询/文档、句子 A/B）。 |
| NSP | "下一句预测" | BERT 的第二个预训练任务；RoBERTa 中被证明无用，2019 年后被放弃。 |
| 微调 | "适配到任务" | 保持编码器大部分冻结；在顶部训练一个小头用于下游任务。 |
| 交叉编码器 | "重排序器" | 接收查询和文档作为输入的 BERT，输出相关性分数。 |
| ModernBERT | "2024 年刷新版" | 用 RoPE、RMSNorm、GeGLU、交替局部/全局注意力重建的编码器，8K 上下文。 |

## 延伸阅读

- [Devlin 等人（2018）。BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805) —— 原始论文。
- [Liu 等人（2019）。RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692) —— 如何正确训练 BERT；终结了 NSP。
- [Clark 等人（2020）。ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators](https://arxiv.org/abs/2003.10555) —— 替换 token 检测在匹配计算量下击败 MLM。
- [Warner 等人（2024）。Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder](https://arxiv.org/abs/2412.13663) —— ModernBERT 论文。
- [HuggingFace `modeling_bert.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/bert/modeling_bert.py) —— 规范的编码器参考。
