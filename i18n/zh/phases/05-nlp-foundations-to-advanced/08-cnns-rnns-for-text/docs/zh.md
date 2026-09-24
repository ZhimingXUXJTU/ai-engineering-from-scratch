# 对于文字的CNN和RNN

> 转变学会 n- 克,回复记忆,两者都被注意力取代,在有限的硬件上都很重要.
> 卷积学习 n-gram――循环负责记忆――都被注意力机制取代――但在有限硬件上仍然很重要――

> **【中文解读】**网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络网络

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 11 (PyTorch Intro), Phase 5 · 03 (Word Embeddings), Phase 4 · 02 (Convolutions from Scratch) | **前置知识:** Phase 3 · 11（PyTorch 入门），Phase 5 · 03（词嵌入），Phase 4 · 02（从零实现卷积）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

基于这些类别的分类器无法辨别`dog bites man`其他`man bites dog`字序有时带来信号.

> TF-IDF 和 Word2Vec 产生忽略词序的平向量.基于它们构建的分类器无法区分.`dog bites man`和 `man bites dog`语序有时带信号语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语语

在变压器到达之前,两个建筑家族填补了这一差距.

> 在变压器出现之前,两族架构填补了这个空白.

**Convolutional nets for text (TextCNN).**应用1D卷曲在文字嵌入序列上.宽度3的过器是一种可学习的三重符号探测器:它跨越三个词并输出分数. 堆积不同的宽度 (2, 3, 4, 5) 检测多尺度模式. 最大积分到一个固定尺寸的表示. 平坦,平行,快速.

> **文本卷积网络（TextCNN）。**在词嵌序列上应用一维卷积――宽度为3的波器是可学习的三元组检测器:它跨越三个词并输出分数――堆叠不同宽度的2、3、4、5) 检测多维模式――最大池化到固定大小的表示――平、并行、快速――

**Recurrent nets (RNN, LSTM, GRU).**处理代币一次,保持一个隐藏状态,将信息传递到前方.序列,存储器,灵活的输入长度.从2014年到2017年,主导序列建模,然后引起了关注.

> **循环网络（RNN、LSTM、GRU）。**个别处理代币,维护前传信息的隐藏状态――顺序、有记忆、灵活输入长度――从2014年到2017年主导序列建模,然后出现注意力机制――

这一课就建立了两者,然后给出了引起人们注意的失败的名字.

> 现在,我们在学习中学习了一些知识,

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

**TextCNN**代币被嵌入.`k`连续的缩将光滑到一个光器上`k`总体的最大聚合在该地图上选择最强的激活. 连接多个过器宽度的最大聚合输出. 输入到一个分类器头.

> **TextCNN**果是个果,`k`连续的一维卷积`k`图片的图片是全局最大的化选择最强的激活.

过器是可以学习的n-gram. 极共聚是位置变异性的,所以"不好"在审查的开始或中期会引发相同的功能.三个过器宽度,每个过器都有100个,给你300个学习的n-gram探测器.训练是平行的;没有连续依赖.

> 为什么有效──波器是可学习的 n-gram──最大池化是位置不变的,所以"不好"在评论开头或中间触发相同的特征──三个波器宽度各 100 个波器给你 300 个可学习的 n-gram 检测器──训练是并行的;没有顺序依赖──

**RNN.**每次都会有点`t`隐藏的状态`h_t = f(W * x_t + U * h_{t-1} + b)`分享`W`现在`U`现在`b`时间的隐藏状态.`T`为了分类,集合在`h_1 ... h_T`(最大,平均或最后).

> **RNN。**在每一个时间步骤`t`隐藏状态`h_t = f(W * x_t + U * h_{t-1} + b)`,我知道.`W`,我知道.`U`,我知道.`b`跨时间共享.`T`隐藏状态是整个前的摘要.`h_1 ... h_T`上池化 (最大,平均值或最后)

染性质的化物质在化.**LSTM**通过长序列稳定梯度, 通过 向的向, 通过向的向, 通过向的向, 通过向的向, 通过向的向, 通过向的向, 通过向的向, 通过向的向, 通过向的向, 通过向的向, 通过向的向, 通过向的向, 通过向的向, 向的向, 向的向, 向的向, 向的向, 向的向, 向的向,向的向,向的向,向的向,向的向,向的向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,向,,,,,,.**GRU**简化LSTM为两个门;具有较少参数的性能.

> 常见的RNN存在消失问题.**LSTM**增加决定忘记什么,储存什么,输出什么门,稳定长序列的梯度.**GRU**将LSTM简化为两个门;参数较小,但效果相似.

**Bidirectional RNNs**运行一个RNN向前和另一个向后,连接隐藏状态.每个代币的表示可以看到左和右的文本.

> **双向 RNN**运行一个RNN向前、另一个向后,拼接隐藏状态――每个代币的表示看左右两侧的上下文――对标记任务必不可少――

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
rnn-unroll
```

## 建立它

### 步骤1:PyTorch中文字CNN

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class TextCNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, n_classes, filter_widths=(2, 3, 4), n_filters=64, dropout=0.3):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.convs = nn.ModuleList([
            nn.Conv1d(embed_dim, n_filters, kernel_size=k)
            for k in filter_widths
        ])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(n_filters * len(filter_widths), n_classes)

    def forward(self, token_ids):
        x = self.embed(token_ids).transpose(1, 2)
        pooled = []
        for conv in self.convs:
            c = F.relu(conv(x))
            p = F.max_pool1d(c, c.size(2)).squeeze(2)
            pooled.append(p)
        h = torch.cat(pooled, dim=1)
        return self.fc(self.dropout(h))
```

其他`transpose(1, 2)`转型`[batch, seq_len, embed_dim]`为了`[batch, embed_dim, seq_len]`因为`nn.Conv1d`总量输出不论输入长度如何,均为固定尺寸.

> `transpose(1, 2)`将`[batch, seq_len, embed_dim]`重塑为`[batch, embed_dim, seq_len]`因为`nn.Conv1d`后输出是固定大小的,无论输入长度如何.

### 步骤 2:LSTM分类器

```python
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_classes, bidirectional=True, dropout=0.3):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=bidirectional)
        factor = 2 if bidirectional else 1
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * factor, n_classes)

    def forward(self, token_ids):
        x = self.embed(token_ids)
        out, _ = self.lstm(x)
        pooled = out.max(dim=1).values
        return self.fc(self.dropout(pooled))
```

为了分类,最大分组通常比取最后一个隐藏状态更好,因为长序列结束的信息往往占据了最后一个状态.

> 在序列上做最大的池化,而不是最后的状态池化.对于分类,最大的池化通常比最后的隐藏状态更好,因为长序列末端的信息倾向于主导最后的状态.

### 步骤3:消失梯度演示 (直觉)

简单的RNN没有门户不能学习长距离的依赖性.`A`任何一个序列中出现.`A`如果重量低于1,梯度会消失.如果超过1,它会爆炸.如果重量低于1,梯度会消失.如果超过1,它会爆炸.

> 没有门控的普通RNN 无法学习长程依赖.考虑一个玩具任务:预测代币.`A`是否出现在序列的任何位置.`A`在位置1的序列长度为100,损失梯度必须通过99次循环重量乘法回流.如果重量小于1,梯度消失.如果大于1,梯度爆炸.

```python
def vanishing_gradient_sim(seq_len, recurrent_weight=0.9):
    import math
    return math.pow(recurrent_weight, seq_len)


# At weight=0.9 over 100 steps:
#   0.9 ^ 100 ≈ 2.7e-5
# The gradient from step 100 to step 1 is effectively zero.
```

机器将这个解决**cell state**通过网络运行的只有添加互动 (忘记门乘以其量度,但梯度仍然沿着"高速公路"流动).

> 通过一个**细胞状态**修复了这个问题,这个状态只通过加法交互穿过网络,但梯度仍然沿着"高速公路"流动.

### 步骤4:为什么这仍然不够

尽管有3个问题,但即使是LSTM仍然存在.

> 即使有LSTM,三个问题持续存在.

1. **Sequential bottleneck.**训练一个RNN在长度1000的序列需要1000个连续前后步骤.不能在时间间平行化.
   **顺序瓶颈。**在长度为1000的序列上训练RN需要1000个连串的正向/反向步骤――无法跨时间并行化――
2. **Fixed-size context vector in encoder-decoder setups.**解码器只能看到编码器的最后隐藏状态,压缩到整个输入.长入输入会丢失细节.第09课直接涵盖这一点.
   **编码器-解码器中的固定大小上下文向量。**解码器只看到编码器的最终隐藏状态,压缩了整个输入.
3. **Distant-dependency accuracy ceiling.**虽然LSTM比普通RNN更有效,但仍然在200多个步骤中难以传播特定信息.
   **远距离依赖准确率天花板。**虽然LSTM比普通RNN优异,但在200+步之间传播特定信息仍然困难.

变形器完全放弃了复发性. 第10课是旋转.

> 注意力解决了所有三个问题.

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

皮托尔奇的`nn.LSTM`现在`nn.GRU`其他`nn.Conv1d`训练规范是标准的.

> 皮托尔奇的`nn.LSTM`,我知道.`nn.GRU`和 `nn.Conv1d`培训代码是标准的.

拥抱面孔船,预训练嵌入式,你插入作为输入层:

> 拥抱面孔 提供预训嵌入作为输入层插入:

```python
from transformers import AutoModel

encoder = AutoModel.from_pretrained("bert-base-uncased")
for param in encoder.parameters():
    param.requires_grad = False


class BertCNN(nn.Module):
    def __init__(self, n_classes, filter_widths=(2, 3, 4), n_filters=64):
        super().__init__()
        self.encoder = encoder
        self.convs = nn.ModuleList([nn.Conv1d(768, n_filters, kernel_size=k) for k in filter_widths])
        self.fc = nn.Linear(n_filters * len(filter_widths), n_classes)

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            out = self.encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        x = out.transpose(1, 2)
        pooled = [F.max_pool1d(F.relu(conv(x)), kernel_size=conv(x).size(2)).squeeze(2) for conv in self.convs]
        return self.fc(torch.cat(pooled, dim=1))
```

需要使用时适合限制的清单.

> 适用约束检查清单.

- **Edge / on-device inference.**如果你的部署目标是手机,这是堆.
  **边缘/设备端推理。**带全球嵌入式文字CNN比变压器小10-100倍.
- **Streaming / online classification.**对于实时输入文本,LSTM仍然获胜.
  **流式/在线分类。**转换器需要完整序列.
- **Tiny models for baselines.**在CPU上训练一个TextCNN5分钟.
  **用于基线的微型模型。**在新任务上快速代. 在CPU上5分钟训练一个文字CNN.
- **Sequence labeling with limited data.**对于1k-10k标记句子,BiLSTM-CRF (课06) 仍然是一个生产级NER架构.
  **数据有限的序列标注。**对于1k-10k标注句子仍然是生产级 NER 架构.

其他一切都会被转变器所控制.

> 其他一切都用了变压器.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

## 运送它.

保存如`outputs/prompt-text-encoder-picker.md`其他:

> 保存为`outputs/prompt-text-encoder-picker.md`其他:

```markdown
---
name: text-encoder-picker
description: Pick a text encoder architecture for a given constraint set.
phase: 5
lesson: 08
---

Given constraints (task, data volume, latency budget, deploy target, compute budget), output:

1. Encoder architecture: TextCNN, BiLSTM, BiLSTM-CRF, transformer fine-tune, or "use a pretrained transformer as a frozen encoder + small head".
2. Embedding input: random init, GloVe / fastText frozen, or contextualized transformer embeddings.
3. Training recipe in 5 lines: optimizer, learning rate, batch size, epochs, regularization.
4. One monitoring signal. For RNN/CNN models: attention mechanism absence means they miss long-range deps; check per-length accuracy. For transformers: fine-tuning collapse if LR too high; check train loss.

Refuse to recommend fine-tuning a transformer when data is under ~500 labeled examples without showing that a TextCNN / BiLSTM baseline has plateaued. Flag edge deployment as needing architecture-before-everything.
```

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 练习题

1. **Easy.**训练一个 TextCNN 在3类玩具数据集 (你发明数据). 检查过器宽度 (2, 3, 4) 超过平均F1的单个宽度 (3).
   **简单。**在一个3类玩具数据集中训练 文字CNN(你自己发明数据) 证证波器宽度 (2, 3, 4) 在平均F1上优于单个宽度 (3) ⋅
2. **Medium.**实现LSTM分类器的最大池,中池和最后状态聚合. 在一个小数据集上进行比较; 文件聚合中获胜的,并假设为什么.
   **中等。**为LSTM 分类器实现最大的池化,平均值池化和最后状态池化.
3. **Hard.**建立一个BiLSTM-CRF NER标签 (组合课06和这项).在CoNLL-2003上训练.比较课06的CRF单独基线和BERT细调.报告训练时间,内存和F1.
   **困难。**构建BiLSTM-CRF NER标记器(结合第06课和本课) ⋅在CoNLL-2003上训练――与第06课的纯CRF基线和BERT微调比较――报告训练时间、内存和F1――

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 关键词 快速查找表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| TextCNN | CNN for text / 文本 CNN | Stack of 1D convolutions over word embeddings with global max-pool. Kim (2014). / 在词嵌入上堆叠一维卷积加全局最大池化。Kim (2014)。 |
| RNN（循环神经网络） | Recurrent net / 循环网络 | Hidden state updated at each time step: `h_t = f(W x_t + U h_{t-1})`. / 每个时间步更新隐藏状态：`h_t = f(W x_t + U h_{t-1})`。 |
| LSTM | Gated RNN / 门控 RNN | Adds input / forget / output gates + a cell state. Trains stably through long sequences. / 添加输入/遗忘/输出门 + 细胞状态。在长序列上稳定训练。 |
| GRU | Simpler LSTM / 更简单的 LSTM | Two gates instead of three. Similar accuracy, fewer parameters. / 两个门代替三个。类似准确率，更少参数。 |
| Bidirectional（双向） | Both directions / 两个方向 | Forward + backward RNN concatenated. Every token sees both sides of its context. / 前向 + 后向 RNN 拼接。每个 token 看到其上下文两侧。 |
| Vanishing gradient（梯度消失） | Training signal dies / 训练信号消失 | Repeated multiplication by <1 weights in plain RNNs makes early-step gradients effectively zero. / 普通 RNN 中对小于 1 的权重反复乘法使早期步骤的梯度实际上为零。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.

## 继续阅读 继续阅读

- [Kim, Y. (2014). Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1408.5882)文本CNN论文.八页.可读. /文本CNN论文──八页──易读──
- [Hochreiter, S. and Schmidhuber, J. (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf) LSTM 论文. 意料地清晰.
- [Olah, C. (2015). Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)让每个人都能理解LSTM的图解.
