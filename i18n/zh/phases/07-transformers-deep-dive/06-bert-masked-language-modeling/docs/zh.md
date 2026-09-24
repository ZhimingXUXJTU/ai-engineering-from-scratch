# 贝尔特 面具语言建模

> 预测下一个字,预测一个缺失的字,一个句子的差异,一个半十年的嵌入式形状.

> **【中文解读】**据了解,BERT是仅编码的变压器,使用掩码预测训练――理解BERT=理解双上下文建模――用于文本分类、NER、问答等――

**Type:** Hands-on | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation)
**Time:** ~45 minutes | **时间:** ~45 分钟

## 问题 问题引入

2018年,每一个NLP任务都从零开始训练了自己的模型,使用自己的标签数据.没有预训练的"理解英语"检查点,你可以调整.ELMo (2018) 显示你可以预训练背景嵌入式使用双向LSTM;它帮助但没有通用化.

> 2018年,每个NLP任务情感分析、命名实体识别、问答、文本含都需要从零训练模型上从自己的标记数据上进行.当时没有预训练的"理解英语"检查点可供微调.

伯特 (Devlin et al. 2018) 问:如果我们拿一个变压器编码器,训练它在互联网上的每句话,并强迫它预测两个方面缺失的语境中的单词呢?

> 根据两侧下文预测被遮蔽的词,会如何?然后在下游任务中微调一个输出头──参数效率的提高令人震惊──

结果:在18个月内,BERT及其变体 (RoBERTa,ALBERT,ELECTRA) 占据了所有现有的NLP排名榜.到2020年,地球上每一个搜索引擎,内容调节管道和语义搜索系统都拥有BERT.

> 结果是:在18个月内,BERT及其变体 (Robert Ta, Albert Electra) 统治了所有NLP排行榜.到2020年,世界上每个搜索引擎,内容审核管道和语义搜索系统都拥有一个BERT.

2026年仅使用编码器的模型仍然是分类,检索和结构化提取的合适工具.它们比解码器更快510x,其嵌入式是每个现代检索堆的骨干.ModernBERT (2024年12月) 通过Flash Attention + RoPE + GeGLU将架构推向8K文本.

> 到2026年,编码器专业模型仍然是分类检索和结构化提取的正确选择它们的每代币运行速度比解码器快 5-10倍,其嵌入是每个现代检索系统的骨干.

> **【中文解读】**贝尔特的革命性在于"预训+微调"范式:大规模无标语料上使用掩码语言模型 (MLM) 预训,然后在特定任务上微调量参数――编码器的双向注意力使它能够同时利用左右下文预测被掩码的词,这是自归模型 (如GPT) 做不到的――

## 概念的核心概念

![Masked language modeling: pick tokens, mask them, predict originals](../assets/bert-mlm.svg)

### 训练信号

拿一个句子:`the quick brown fox jumps over the lazy dog`现在,我们要去.

> 取一个句子:`the quick brown fox jumps over the lazy dog`,我知道.

随机地出15%的代币:

> 随机掩码 15% 的代币:

```
input:  the [MASK] brown fox jumps [MASK] the lazy dog
target: the quick brown fox jumps over the lazy dog
```

训练模型以预测原始代币在隐藏位置. 因为编码器是双向,预测`[MASK]`在位置1可以使用`brown fox jumps`现在,我们在2+位置上做了什么?

> 训练模型在被隐藏位置预测原始代币――因为编码器是双向的,预测位置是1的.`[MASK]`可以利用位置 2 及后的`brown fox jumps`这正是GPT做不到的事情.

### 关于BERT面具的规则

预测选择的15%的代币:

> 在被选中用于预测的15%代币中:

- 80% 则被替换为`[MASK]`现在,我们要去.
  中文翻译:80%被替换为`[MASK]`,我知道.
- 10% 则被随机代币取代.
  中文翻译:10% 被替换为随机代币.
- 只有10%的情况保持不变.
  中文翻译:10% 保持不变――

为什么不总是`[MASK]`因为`[MASK]`训练模型以预期`[MASK]`假设在100%的面具位置,预训练和细调之间会产生分布转变.10%的随机加上10%的变化保持模型的诚实性.

> 为什么不总是用?`[MASK]`因为`[MASK]`如果训练模型在100%的隐藏位置,`[MASK]`预训和微调之间造成分布偏移.10% 随时替换 +10% 保持不变让模型保持"诚实".

> **【中文解读】**为了缩小预训和微调之间的分布差异,需要让模型在训练中也看到正常和随机替换的代币.

> **【拓展：BERT 在 RAG 系统中的角色】**现代RAG (检索增强生成) 系统中,BERT 变体仍然是检索阶段的核心――句子变换器模型――如全MiniLM-L6-v2) 本质上就是使用比较学习微调的BERT――交叉编码器――跨编码器) 重排序器也是BERT 架构它让查询和文档在同一层次的关注中交互,质量远超双编码器――

### 下一句预测 (NSP) ,为什么它被放弃

原始BERT也在NSP上训练:给了两个句子A和B,预测如果B跟随A.RoBERTa (2019) 删除了它并显示NSP受伤,没有帮助.现代编码器跳过它.

> 原始BERT还在NSP上训练:给定两个句子A 和B,预测B 是否紧跟A.

### 2026年发生了什么变化:ModernBERT

根据2026年的原始模型,

> 2024 年的ModernBERT论文用现代组件重建编码器块:

| Component | Original BERT (2018) | ModernBERT (2024) |
|-----------|----------------------|-------------------|
| 组件 | 原始 BERT (2018) | ModernBERT (2024) |
| Positional | Learned absolute | RoPE |
| 位置编码 | 学习式绝对位置 | RoPE |
| Activation | GELU | GeGLU |
| 激活函数 | GELU | GeGLU |
| Normalization | LayerNorm | Pre-norm RMSNorm |
| 归一化 | LayerNorm | 前归一化 RMSNorm |
| Attention | Full dense | Alternating local (128) + global |
| 注意力 | 全密集 | 交替局部 (128) + 全局 |
| Context length | 512 | 8192 |
| 上下文长度 | 512 | 8192 |
| Tokenizer | WordPiece | BPE |
| 分词器 | WordPiece | BPE |

与2018年的堆不同,它是闪光注意力原生.在序列长度8K时,传输速度比DeBERTa-v3更快,GLU比分更好.

> 与2018年的技术不同,ModernBERT原生支持闪光注意力.

### 在2026年仍会选择编码器的使用案例

| Task | Why encoder beats decoder |
|------|---------------------------|
| 任务 | 为什么编码器优于解码器 |
| Retrieval / semantic search embeddings | Bidirectional context = better embedding quality per token |
| 检索/语义搜索嵌入 | 双向上下文 = 每个 token 更好的嵌入质量 |
| Classification (sentiment, intent, toxicity) | One forward pass; no generation overhead |
| 分类（情感、意图、毒性） | 一次前向传播；无生成开销 |
| NER / token labeling | Per-position output, natively bidirectional |
| NER/token 标注 | 逐位置输出，天然双向 |
| Zero-shot entailment (NLI) | Classifier head on top of encoder |
| 零样本蕴含 (NLI) | 编码器之上的分类器头 |
| Reranker for RAG | Cross-encoder scoring, 10x faster than LLM rerankers |
| RAG 重排序器 | 交叉编码器评分，比 LLM 重排序器快 10 倍 |

## 建立它,实现它.
```figure
transformer-residual
```

## 建立它

### 步骤1:掩盖逻辑

看到`code/main.py`功能`create_mlm_batch`返回输入 ID (面具应用) 和标签 (仅在面具位置, -100其他地方  PyTorch 忽略索引公约).

> 参见`code/main.py`△函数`create_mlm_batch`接受代币ID 列表、词表大小和掩码概率,返回输入ID(已应用掩码) 和标签(仅在掩码位置有价值,其余为 -100PyTorch的忽略索引约定) 

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
            # else: keep original
    return input_ids, labels
```

### 步骤2:在一个小的体积上运行MLM预测

训练一个2层编码器+MLM头,用20个字,200个句子的词汇.没有梯度.我们做了前进通过的智力检查. 需要 PyTorch的全面训练.

> 在20个词表和200个句子上训练一个2层编码器 +MLM头──不涉及梯度 仅做前向传播的合理性检查──完整训练需要 PyTorch──

### 步骤3:比较面具类型

展示三向规则如何使模型可以使用`[MASK]`预测一个未蒙面的句子和一个蒙面的句子. 两者都应该产生合理的符号分布,因为模型在训练中看到了两种模式.

> 展示三路规则如何让模型在没有`[MASK]`对于未掩码句子和掩码句子的分别预测.

### 步骤4:细调头

换一个玩具感觉数据集上的MLM头部以分类头部. 只有头部,编码器被结. 每个BERT应用程序都遵循这种模式.

> 用分类头换MLM头,在一个玩具情感数据集上训练.

> **【拓展：BERT 微调的实践技巧】**微调BERT的最佳实践包括:(1) 使用较小的学习率(2e-5到5e-5) 避免破坏预训练权重;(2) 对分类任务使用 (CLS) 代币的输出作为句子表示;(3) 对 NER 等以后的代币 任务,使用每个位置的输出;(4) 逐步解解(逐步解) 可以在小数据集上提升泛化能力;;

## 用它实现框架

```python
from transformers import AutoModel, AutoTokenizer

tok = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base")

text = "Attention is all you need."
inputs = tok(text, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, N, 768)
```

**Embedding models are fine-tuned BERT.** `sentence-transformers`模型`all-MiniLM-L6-v2`它们的编码器是相同的,损失发生了变化.

> **嵌入模型是微调后的 BERT。** `sentence-transformers`模型如`all-MiniLM-L6-v2`编码器架构与比较损失训练的BERT相同,只是损失函数变化了.

**Cross-encoder rerankers are also fine-tuned BERT.**双对分类`[CLS] query [SEP] doc [SEP]`查询和文档之间的双向关注正是交叉编码器对双码器的质量优势.

> **交叉编码器重排序器也是微调后的 BERT。**在`[CLS] query [SEP] doc [SEP]`交叉编码器质量优于双编码器的原因是查询和文档之间的双向关注.

**When not to pick BERT in 2026.**任何生成性.编码器没有任何合理的方式来自动降低生成代币.

> **2026 年何时不选 BERT。**任何生成式任务──编码器没有合理的方式进行自归代币 生成──此外,在以下场景中,小型解码器 (如 Phi-3-Mini、Qwen2-1.5B) 可以使用更少的参数获得相当的灵活性──

> **【拓展：ModernBERT 的现代化改进】**现代BERT(2024) 将2018年的BERT架构全面升级:RoPE 替代学习式位置编码、GeGLU 替代 GELU、前归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归

## 运送它.

看到`outputs/skill-bert-finetuner.md`技能范围为一个新的分类或提取任务进行BERT细调 (背骨选择,头部规格,数据,评估,停止).

> 参见`outputs/skill-bert-finetuner.md`△该技能为新的分类或提取任务规划BERT 微调方案 (骨干网络选择,头部规格,数据,评估,停止条件) 

## 练习题

1. **Easy.**跑步`code/main.py`确认15%是选定的,其中80%是`[MASK]`现在,我们要去.
   中文翻译:运行 `code/main.py`印出了10,000个标志的掩码分布. 确认约15%被选中,其中约80%是变为.`[MASK]`,我知道.
2. **Medium.**实施全字掩饰:如果一个词被标记成子词,把所有子词都掩盖在一起或没有.测量这是否提高了500句子的MLM准确性.
   中文翻译:实现全词掩码:如果一个词被分词为多个子词,要么全部掩码要么全部不掩码――测量这是否在500个句子语料上提升了LM准确率――
3. **Hard.**训练一个小的 (2层,d=64) BERT从公共数据集中的1万句子.`[CLS]`比较与匹配的参数中只有解码器的基线.
   中文翻译:在公开数据集的10,000个句子上训练一个小的 (二层,d=64)BERT──微调`[CLS]`什么比较较好?

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| MLM | "Masked language modeling" | Training signal: randomly replace 15% of tokens with `[MASK]`, predict the originals. |
| MLM | "掩码语言建模" | 训练信号：随机将 15% 的 token 替换为 `[MASK]`，预测原始 token。 |
| Bidirectional | "Looks both ways" | Encoder attention has no causal mask — every position sees every other position. |
| 双向 | "看两边" | 编码器注意力没有因果掩码——每个位置都能看到其他所有位置。 |
| `[CLS]` | "The pooler token" | A special token prepended to every sequence; its final embedding is used as the sentence-level representation. |
| `[CLS]` | "池化 token" | 一个特殊 token，添加到每个序列开头；其最终嵌入用作句子级表示。 |
| `[SEP]` | "Segment separator" | Separates paired sequences (e.g. query/doc, sentence A/B). |
| `[SEP]` | "片段分隔符" | 分隔成对序列（如查询/文档、句子 A/B）。 |
| NSP | "Next sentence prediction" | BERT's second pretraining task; shown to be useless in RoBERTa, dropped after 2019. |
| NSP | "下一句预测" | BERT 的第二个预训练任务；RoBERTa 证明其无用，2019 年后弃用。 |
| Fine-tuning | "Adapt to a task" | Keep the encoder mostly frozen; train a small head on top for the downstream task. |
| 微调 | "适应任务" | 保持编码器基本冻结；在顶部训练一个小头用于下游任务。 |
| Cross-encoder | "A reranker" | A BERT that takes both query and doc as input, outputs a relevance score. |
| 交叉编码器 | "重排序器" | 同时接收查询和文档作为输入的 BERT，输出相关性分数。 |
| ModernBERT | "2024 refresh" | Encoder rebuilt with RoPE, RMSNorm, GeGLU, alternating local/global attention, 8K context. |
| ModernBERT | "2024 刷新版" | 用 RoPE、RMSNorm、GeGLU、交替局部/全局注意力重建的编码器，8K 上下文。 |

## 继续阅读 继续阅读

- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)原始的纸.
  中文翻译:BERT 原始论文──
- [Liu et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692)如何正确训练BERT;杀死NSP.
  中文翻译:如何正确训练BERT;证明了NSP无用──
- [Clark et al. (2020). ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators](https://arxiv.org/abs/2003.10555)替换代代币检测在匹配计算时超过MLM.
  中文翻译:替换代币检测在相同计算量下优于MLM。
- [Warner et al. (2024). Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder](https://arxiv.org/abs/2412.13663)现代BERT纸.
  中文翻译:现代BERT论文──
- [HuggingFace `modeling_bert.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/bert/modeling_bert.py)可нони化编码器参考.
  中文翻译:HuggingFace BERT 模型实现参考代码──
