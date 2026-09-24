# 序列到序列模型 (秒2秒)

> 两名RNN假装是翻译者. 他们遇到的瓶是人们的关注的原因.
> 两个RNN假装是翻译器.

> **【中文解读】**编码器解码器架构――注意力机制就是为了解决它的瓶而发明的――

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 08 (CNNs + RNNs for Text), Phase 3 · 11 (PyTorch Intro) | **前置知识:** Phase 5 · 08（CNN 和 RNN 文本处理），Phase 3 · 11（PyTorch 入门）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

类别将变量长度序列映射到单个标签上. 翻译将变量长度序列映射到另一个变量长度序列上. 输入和输出在不同的词汇库中,可能是不同的语言,没有保证长度平衡.

> 分类将变长序列映射为单个标签――翻译将变长序列映射为另一个变长序列――输入和输出在不同的词表中,可能是不同的语言,长度无法保证一致――

后2seq架构 (Sutskever,Vinyals,Le,2014) 用一个简单的食谱来解解开这个问题.两个RNN.一个读取源句子并产生一个固体尺寸的语境向量.另一个读取该向量并生成目标句子代币.同一个代码你为08课写的,粘合在一起以不同的方式.

> 结构 (Sutskever, Vinyals, Le, 2014) 用一个刻意简单的方案解决这个问题.

首先,文本向量瓶是NLP中最具教学效益的失败.它激励了注意力和变压器擅长的一切.第二,培训配方 (教师强迫,计划采样,线束搜索在推断) 仍然适用于包括LLM在内的每个现代生成系统.

> 这值得学习有两个原因. 第一,上下文向量瓶是NLP中最具教学价值的失败. 第二,训练方案 (教师强制,计划采样,推理时的束搜索) 仍然适用于包括LLM内的每个现代生成系统.

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.

**Encoder.**读取源句子的RNN. 它的最后隐藏状态是**context vector**总结整个输入的总结. 据说除了源头之外,没有什么丢失.

> **编码器（Encoder）。**一读取源句的RNN──其最终隐藏状态是**上下文向量** 整个输入的固定大小摘要――据说不会丢失任何内容.

**Decoder.**另一个RNN从文本向量初始化.在每个步骤中,它将先前生成的代币作为输入,并产生目标词汇中的分布. 样本或 argmax来选择下一个代币. 输入它.重复直到一个`<EOS>`标志产生的或最大长度被击中.

> **解码器（Decoder）。**另一个从上下文向量初始化的RNN──在每一步,它将先生成的代币作为输入,产生目标词表上的分布──采样或取 argmax 选择下一个代币──将其反进而──重复直到产生`<EOS>`标志或达到最大长度.

**Training:**通过两个网络,通过时间进行标准的背后支持.

> **训练：**通过两个网络的标准时间反向传播.

**Teacher forcing.**在训练过程中,解码器的输入步骤`t`是位置上的*真实地图*符号`t-1`没有它,早期错误会发生,模型永远不会学习.在推断时,你必须使用模型的预测,所以总是存在火车/推理分布差距.这个差距被称为**exposure bias**现在,我们要去.

> **教师强制（Teacher Forcing）。**训练时,解码器在步骤中`t`的输入是位置`t-1`没有它,早期错误会级联,模型永远不会学到. 在推理时,你必须使用模型的自己的预测,所以总是存在训练/推理分布差距.**暴露偏差（Exposure Bias）**,我知道.

**The bottleneck.**编码器学到关于源的所有信息都必须挤进一个文本向量中.长短句子会失去细节.罕见的词语会模糊.重排 (聊天黑与黑猫) 必须记忆,而不是计算.

> **瓶颈。**编码器学到的关于源源的一切都必须缩小到那个上下文向量中――长句子丢失细节――罕见词被模糊――重排序(聊天黑人与黑猫) 必须记忆,而不是计算――

注意力 (课 10) 通过让解码器查看 *每一个*编码器的隐藏状态,而不仅仅是最后一个.

> 注意力 (第十课) 通过让解码器查看*每个*编码器隐藏状态 (不仅是最后一个) 来修复这个问题――这是全部的关键点――

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.

## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
lstm-gates
```

## 建立它

### 步骤1:编码器

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

`outputs`具有形状`[batch, seq_len, hidden_dim]`每一个输入位置一个隐藏状态.`hidden`具有形状`[1, batch, hidden_dim]`最后一步. 第08课说"分类输出".在这里我们将最后一个隐藏状态作为文本向量,并忽略每一步输出.

> `outputs`形状为`[batch, seq_len, hidden_dim]` 每个输入位置都隐藏状态.`hidden`形状为`[1, batch, hidden_dim]` 最终步骤. 第8课说"在输出上池化做分类".

### 步骤 2: 解码器

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

输入:单个代币的批量和当前隐藏状态.输出:下一个代币和更新的隐藏状态的词汇记录.

> 解码器每次调用一步──输入:一批单个代币 和当前隐藏状态──输出:下一个代币的词表 logits 和更新后的隐藏状态──

### 步骤3:教师强迫的训练循环

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

两个值得命名的.`ignore_index=0`置代币的损失.`teacher_forcing_ratio`根据模型的预测,在每一步使用真符号的概率.从1.0开始 (完全强迫教师) 并在训练中降至0.5以缩小暴露偏差.

> 值得注意的两个参数:`ignore_index=0`跳过填充代币 上的损失.`teacher_forcing_ratio`实际标志和模型预测的概率. 从1.0 (完全教师强制) 开始,训练过程中退火到约0.5以缩小暴露偏差.

### 步骤4:推断循环 (贪)

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

贪的解码会在每一步都选择最有可能的代币. 它可以走开:一旦你承诺一个代币,**Beam search**保持了顶部...`k`部分序列活着,最后选择最高分的完整序列.

> 贪心解码每步选择最高概率的代币――它可能偏偏:一旦你提交了一个代币,就无法撤回――**束搜索（Beam Search）**保持排名`k`部分序列存活,在最后选择最高分数的完整序列中.束宽度3-5是标准.

### 步骤5:瓶,已证明

训练模型做玩具复制任务:来源 `[a, b, c, d, e]`目标`[a, b, c, d, e]`增加序列长度,观察准确性.

> 在玩具复制任务上训练模型:源 `[a, b, c, d, e]`目标`[a, b, c, d, e]`△增加序列长度──观察准确率──

```
seq_len=5   copy accuracy: 98%
seq_len=10  copy accuracy: 91%
seq_len=20  copy accuracy: 62%
seq_len=40  copy accuracy: 23%
```

单个GRU隐藏状态不能无损地记住40代码输入.信息在每个编码器步骤上都存在,但解码器只能看到最后一个状态.注意力直接解决这一问题.

> 单个GRU 隐藏状态无法无损记忆 40个代币的输入信息存在于每个编码器步骤,但解码器只看到最后状态――注意力直接修复了这个问题――

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.

> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

皮托奇已经`nn.Transformer`其他`nn.LSTM`基于"接着"的模板.`transformers`库运输了大量的代码器和解码器模型 (BART,T5, mBART,NLLB),

> 火有`nn.Transformer`基于`nn.LSTM`面子的抱`transformers`库提供数十亿代币上训练的完整编码器解码器模型 ((BART、T5、mBART、NLLB) 

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tok = AutoTokenizer.from_pretrained("facebook/bart-base")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

src = tok("Translate this to French: Hello, how are you?", return_tensors="pt")
out = model.generate(**src, max_new_tokens=50, num_beams=4)
print(tok.decode(out[0], skip_special_tokens=True))
```

现代编码解码器将RNN用于变压器.高层形状 (编码器,解码器,生成代币-按代币) 与2014年 seq2seq纸相同.每个区块内部的机制是不同的.

> 现代编码器-解码器用变压器 替代了RNN──高层结构──编码器、解码器、个个代币 生成) 与2014年的第二次论文完全相同──每个块内部的机制不同──

### 什么时候还可以找到基于RNN的seq2seq

对于新项目来说,几乎从来没有.

> 对于新项目几乎没有必要:

- 流媒体翻译,其中你一次输入一个代币,
  流式翻译,逐个标志 消耗输入,内存有界――
- 在设备上发送文字,变压器内存成本是极高的.
  设备端文本生成,变压器内存成本过高.
- 了解编码和解码瓶是最快的方法来了解变压器为什么赢了.
  教学――理解编码器-解码器瓶是理解变革为什么胜出最快的路径――

### 暴露偏见及其减轻

- **Scheduled sampling.**训练期间的教师强迫比率,使得模型学会从自己的错误中恢复.
  **计划采样（Scheduled Sampling）。**训练期间退火教师强制比例,让模型学会从自己的错误中恢复过来──
- **Minimum risk training.**训练用语句级蓝色分数而不是代币级交叉,更接近你真正想要的.
  **最小风险训练（Minimum Risk Training）。**在句子级蓝色分数而不是标志性交叉级上训练――更接近你真正想要的――
- **Reinforcement learning fine-tuning.**奖励序列生成器用一个指标.
  **强化学习微调。**用标志奖励序列生成器──用于现代LLM的RLHF──

它们都适用于变压器发电.

> 这三种仍然适用于基于变压器的生成.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.

## 运送它.

保存如`outputs/prompt-seq2seq-design.md`其他:

> 保存为`outputs/prompt-seq2seq-design.md`其他:

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

Refuse to recommend training a seq2seq from scratch for under a million parallel examples. Flag any pipeline that uses greedy decoding for user-facing content as fragile (greedy repeats and loops).
```

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## 练习题

1. **Easy.**执行玩具复制任务. 训练一个GRU seq2seq在输出输入对等目标的源. 测量精度在长度 5, 10, 20. 复制瓶.
   **简单。**实现玩具复制任务――训练GRU seq2seq 在目标等于源的输入输出对上――测量长度 5、10、20 的准确率――复现瓶──
2. **Medium.**添加光束搜索解码. 3. 测量蓝色在一个小平行体上,以抵制贪. 光束搜索获胜的文件 (通常是最后的代币),并且它没有区别.
   **中等。**添加束宽度为3个束搜索解码――在小平行语料上测量对贪心的蓝色――记录束搜索在哪里胜出(通常是最后几个代币) 以及在哪里没有区别――
3. **Hard.**精细调节`facebook/bart-base`根据10k对对对法拉斯数据集,比较细调模型的光束-4输出与基本模型的持久输入.报告BLEU,选择10个质量例子.
   **困难。**在1万对释义数据集中微调`facebook/bart-base`△在留出输入上比较微调模型的束 4 输出与基础模型――报告 BLEU 并选出10个定性示例――

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.

## 关键词 快速查找表

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Encoder（编码器） | Input RNN / 输入 RNN | Reads source. Produces per-step hidden states and a final context vector. / 读取源。产生逐步隐藏状态和最终上下文向量。 |
| Decoder（解码器） | Output RNN / 输出 RNN | Initialized from context vector. Generates target tokens one at a time. / 从上下文向量初始化。逐个生成目标 token。 |
| Context vector（上下文向量） | The summary / 摘要 | Final encoder hidden state. Fixed size. The bottleneck attention solves. / 最终编码器隐藏状态。固定大小。注意力解决的瓶颈。 |
| Teacher forcing（教师强制） | Use true tokens / 使用真实 token | Feed the ground-truth previous token at training time. Stabilizes learning. / 训练时馈入真实的前一个 token。稳定学习。 |
| Exposure bias（暴露偏差） | Train/test gap / 训练/测试差距 | Model trained on true tokens never practiced recovering from its own mistakes. / 在真实 token 上训练的模型从未练习从自己的错误中恢复。 |
| Beam search（束搜索） | Better decoding / 更好的解码 | Keep top-k partial sequences alive at each step instead of committing greedily. / 每步保持排名前 k 的部分序列存活，而非贪心提交。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.

## 继续阅读 继续阅读

- [Sutskever, Vinyals, Le (2014). Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215)原始的四页. / 原始的四页.
- [Cho et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078)引入了GRU和编码器解码器框架.
- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473)注意论文. 阅读课后立即阅读. / 注意力论文──在本课后立即阅读──
- [PyTorch NLP from Scratch tutorial](https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html)可构建的seq2seq+注意码. / 可构建的seq2seq+注意力代码──
