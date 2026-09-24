# 原因语言模型

> 现在,我们可以看到一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符串,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符,一个字符.

> **【中文解读】**简单的解释是:GPT 是单独解码器的变压器,用因果掩码 (因果掩码) 防止看到未来的代币.

**Type:** Hands-on | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 问题 问题引入

语言模型回答了一个问题:`t-1`代币,代币的概率分布是多少?`t`训练这个信号,预测下一个代币,你得到一个模型,可以生成任意的文字,一个代币一次.

> 语言模型回答一个问题:给定前 `t-1`个标志,第`t`在这个信号下一个代币预测上训练,你就能得到一个可以单个代币生成任意文本的模型

为了在整个序列上进行端到端训练,你需要每个位置的预测仅依赖于之前的位置.否则模型通过查看答案就会轻微地欺骗.

> 为了在整个序列上端到端并行训练,你需要预测每个位置只依赖于之前的位置.

原因面膜是这样做的.`-inf`随着软max之后,这些位置变为0. 每个位置只能关注自己和之前的位置. 因为你将它应用到整个序列上一次,你得到N平行下一个代币预测在一个前进传递.

> 由于掩码实现了这一点.`-inf`值),加到软max 之前的注意分数上――软max 后,这些位置变为0――每个位置只能关注自身及之前的位置――因为对整个序列只适用于一次,所以一次向前传播就能得到N个并行的下一个代币预测――

它们都是一个核心循环的仅可解码的因果变压器. 只有更大,更好的数据,更好的RLHF.
它们都是具有相同的核心循环的仅可解码的因果变压器.它们分别于数据质量,规模和建筑精炼以及后培训 (SFT,RLHF,DPO及其后代).

> 它们都是解码器专用因果变压器,核心循环相同──只是更大,数据更好,RLHF更好──

> **【中文解读】**因果掩码是现代AI中最重要的代码. 增加注意力分数,经过软max 后被遮蔽位置变为0――每个位置只能关注自身及之前的代码.

## 概念的核心概念

![Causal mask creates a triangular attention matrix](../assets/causal-attention.svg)

### 面具

由于长度的顺序`N`建立一个`N × N`矩阵:

> 给定长度为`N`序列,构建一个`N × N`矩阵:

```
M[i, j] = 0       if j <= i
M[i, j] = -inf    if j > i
```

加入`M`软max之前的注意力分数. `exp(-inf) = 0`关注矩阵的每个行是仅对前位置的概率分布.

> 将`M`增加到软max 之前的原始注意力分数.`exp(-inf) = 0`因此,被掩盖位置的权重为零. 注意矩阵的每行只是前序位置的概率分布.

实施成本:一 `torch.tril()`电话,计算时间:纳秒,现场影响:一切.

> 实现成本:一行`torch.tril()`调用――计算时间:纳秒级――对整个领域的影响:改变了一切――
### 长方体来自哪里

面具通常以注意力上的补丁呈现. 运行衍生在另一方向,它不再神秘:注意力是预सर्ग平均的第三个精炼,三角形是该平均的循环边界,写成矩阵.

**Stage 1 — prefix average.**顺序的最愚蠢的因果总结:位置`i`成为位置的平均值`0…i`作为一个循环,这是`out[i] = X[:i+1].mean(0)`按一个矩阵乘以一个矩阵,然后把每个行分为数,然后乘以

```python
import numpy as np

A = np.tril(np.ones((n, n)))
A = A / A.sum(axis=1, keepdims=True)
out = A @ X
```

排列`i`其他`A`是`[1/(i+1), …, 1/(i+1), 0, …, 0]`未来的任何东西都没有被掩盖,未来从来没有在总数中.

**Stage 2 — learned weights.**统一的平均值将过去的每个代币都视为同样相关.`S`现在,行列不再按构造算数积为一个,所以将每个行列正常化为软max,而不是按数量分.软max从来没有输出精确的零,这会破坏因果关系,除非未来的分数进入为`-inf`因为`exp(-inf) = 0`其他:

```python
def softmax(x, axis):
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

S = S + np.triu(np.full((n, n), -np.inf), k=1)
A = softmax(S, axis=1)
out = A @ X
```

它们是三角形,三行矩阵,三角形.`-inf`面具不是新机器,而是第一阶段的零输入,

**Stage 3 — content-dependent weights.**在第二阶段,`S`选后的位置:位置7总是重量位置3相同,无论代币说什么. 让得分取决于代币本身:`S = Q @ K.T / sqrt(d_k)`面具,软质,,都是一样的.

基本上,它是一个不变的阶段,一个不变的阶段:一个低三角的排列-stochastic矩阵乘以序列. 均的平均,学习的静态权重,内容依赖的权重.

```figure
mask-derivation
```

### 并行培训,串行推断

培训:向前传递整体`(N, d_model)`顺序一次,计算N跨进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进进

> 训练:对整个`(N, d_model)`序列做一次前向传播,计算 N 个交叉损失(每个位置一个),求和,反向传播──沿序列并行──这就是GPT 训练可扩展的原因一次GPU 通行就能处理批量中的1M个代币──

引号:你生成代币.`[t1, t2, t3]`现在,`t4`料`[t1, t2, t3, t4]`现在,`t5`料`[t1, t2, t3, t4, t5]`现在,`t6` KV缓存 (课 12) 保存了隐藏的状态`t1…tn`所以你不会每一步都重新计算它们. 但推断的序列深度=输出长度. 这就是自动降低税,

> 推理: 个个标志 生成――输入`[t1, t2, t3]`得到了`t4`◎输入`[t1, t2, t3, t4]`得到了`t5`◎输入`[t1, t2, t3, t4, t5]`得到了`t6`〔KV 缓存〕第12课)保存了`t1…tn`由于每一步都不需要重复计算,但推理时的串行深度 = 输出长度.

### 损失 变量

给出的代币`[t1, t2, t3, t4]`其他:

> 给定标志`[t1, t2, t3, t4]`其他:

- 输入:`[t1, t2, t3]`
  中文翻译:输入:`[t1, t2, t3]`
- 目标:`[t2, t3, t4]`
  中文翻译:目标:`[t2, t3, t4]`

对于每一个职位`i`计算`-log P(target_i | inputs[:i+1])`总结,这是整个序列的交叉化.

> 对于每一个位置`i`计算`-log P(target_i | inputs[:i+1])`这就是整个序列的交叉.

每个变压器 LM 你听说过的火车在这个损失. 预训练,细节调整,SFT 相同的损失,不同的数据.

> 你听说的每个变压器语言模型都在这个损失上训练――预训练、微调、SFT同样的损失,不同的数据――

> **【拓展：Teacher Forcing 与暴露偏差】**训练时模型从未见过自己的错误输出,推理时却必须从自己的输出中继续产生.

### 解码策略

训练后,样本选项比人们想象的更重要.

> 训练完成后,采样策略的选择比人们想象的更重要.

| Method | What it does | When to use |
|--------|--------------|-------------|
| 方法 | 功能 | 适用场景 |
| Greedy | Argmax every step | Deterministic tasks, code completion |
| 贪心 | 每步取最大值 | 确定性任务、代码补全 |
| Temperature | Divide logits by T, sample | Creative tasks, higher T = more diversity |
| 温度 | 将 logits 除以 T 后采样 | 创意任务，T 越高多样性越大 |
| Top-k | Sample from top-k tokens only | Kills low-probability tails |
| Top-k | 只从概率最高的 k 个 token 采样 | 消除低概率尾部 |
| Top-p (nucleus) | Sample from smallest set with cumulative prob ≥ p | 2020+ default; adapts to distribution shape |
| Top-p（核采样） | 从累积概率 ≥ p 的最小集合中采样 | 2020+ 默认策略；自适应分布形状 |
| Min-p | Keep tokens with `p > min_p * max_p` | 2024+; better at rejecting long tails than top-p |
| Min-p | 保留 `p > min_p * max_p` 的 token | 2024+；比 top-p 更好地拒绝长尾 |
| Speculative decoding | Draft model proposes N tokens, big model verifies | 2–3× latency reduction at same quality |
| 推测解码 | 草案模型提出 N 个 token，大模型验证 | 相同质量下延迟降低 2-3 倍 |

2026年,min-p + 0.7温度是开放权重模型的合理默认.

> 在2026年,min-p+温度0.7是开源模型的合理默认配置.

> **【中文解读】**解码策略的选择直接影响生成质量──贪心搜索(argmax) 适应确定性任务,温度采样增加多样性,顶-p/min-p 截断低概率尾部──2026年的推默认:min-p +温度0.7,比传统的顶-p 能更好地处理分布的度变化──

> **【拓展：从 GPT-2 到 GPT-4 的规模跳跃】**根据GPT-2(1.5B 参数)→GPT-3(175B)→GPT-4(估计1.8T MoE) 的规模跳跃中,结构变化很小,但数据和训练方法的改进巨大――GPT-4使用了MoE(混合专家) 架构和更高质量的数据配合比,加上RLHF对齐训练――这证实了"规模即一切"的假设,但也表明数据质量和后训练同样关键――

### 什么让"GPT配方"工作

1. **Decoder-only.**没有编码器,每层一个注意力传输+FFN.
   翻译: 中文**解码器专用。**没有编码器开销. 每层一次注意力.
2. **Scaling.**基数法 (课 13) 告诉你如何花钱计算.
   翻译: 中文**规模扩展。**从124M到1.5B到175B再到万亿参数.
3. **In-context learning.**模型可以在不需要细调的情况下遵循一些拍摄的例子.
   翻译: 中文**上下文学习。**约在6B-13B 参数时涌现.模型无需微调就能遵循少样本示例.
4. **RLHF.**培训后的人类偏好将原始预训练的文本转化为聊天助理.
   翻译: 中文**RLHF。**在人类偏好上进行后训练后,将原始预训练文本转化为对话助手.
5. **Pre-norm + RoPE + SwiGLU.**稳定训练规模.
   翻译: 中文**Pre-norm + RoPE + SwiGLU。**实力训练

根据GPT-2的数据,规模和训练后的情况,

> 自GPT-2以来,核心架构没有发生大变化.

> **【中文解读】** GPT的成功要素:仅通过解码器的架构简洁性,规模扩展 (从124M到万亿参数) 下文学习能力 (约6B参数开始涌现) RLHF 后训练 (将预训文本转化为对话助手) 和现代块设计 (Pre-norm + RoPE + SwiGLU) .

> **【拓展：自回归生成的推理瓶颈】**GPT的核心矛盾:训练时并行计算整个序列 (高效),推理时必须逐个代币 生成 (串行) ;;KV 缓存 (缓存) 课12和推测解码 (推测解码) 课16是缓解推理延迟的两个关键技术. 在生产系统中,推理延迟通常是最大的工程挑战,直接决定用户体验和成本.

## 建立它,实现它.
```figure
causal-mask
```

## 建立它

### 步骤1:因果性面具

看到`code/main.py`一个单行:

> 参见`code/main.py`〔一行代码〕

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

在软max之前,再加上注意力分数.

> 增加到之前的注意力分数.

### 步骤2:两层GPT型模型

堆叠两个解码器块 (掩盖自注意+FFN,没有交叉注意).添加一个代币嵌入,一个定位编码和一个解嵌 (绑定到代币嵌入矩阵是GPT-2以来的标准技巧).

> 堆叠两个解码器块(掩码自注意力 + FFN,无交叉注意力) ・・・添加代币 嵌入、位置编码和反嵌入(与代币 嵌入矩阵绑定GPT-2 以来标准技巧) ・・・

### 步骤3:下一个标志预测,端到端

在20个代币玩具词汇上,在每个位置都生成 logits. 计算交叉缩损失与转移对一个目标. 没有梯度.

> 在20个代币的玩具词表上,在每个位置都产生逻辑――对偏移者的目标计算交叉损失――不涉及梯度这是前向传播的合理性检查――

### 步骤4:采样

运行一个固定提示,并比较输出.一个样本取函数是10行.

> 实现贪心,温度,顶-k,顶-p,min-p采样――在固定提示上分别运行并比较输出――一个采样函数只需要10 行代码――

## 用它实现框架

火,2026年语法:

> 火,2026年的常用写法:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")

prompt = "Attention is all you need because"
inputs = tok(prompt, return_tensors="pt")
out = model.generate(
    **inputs,
    max_new_tokens=64,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
)
print(tok.decode(out[0]))
```

在帽子下,`generate()`运行前进传递,拉出最后位置的记录,样本下一个代币,添加它,并重复.每个生产LLM推理堆 (vLLM,TensorRT-LLM, llama.cpp,Ollama,MLX) 实现相同的循环,重量优化批量预填,连续批量,KV缓存页面,投机解码.

> 在底层,`generate()`运行前向传播,取出最后位置的逻辑,采样下一个代币,添加到序列中,重复.

**GPT vs BERT, one line each:**GPT预测`P(x_t | x_{<t})`伯特预测`P(x_masked | x_unmasked)`损失决定模型是否能产生.

> **GPT 与 BERT 各一句话：**预测`P(x_t | x_{<t})`〔BERT〕预测`P(x_masked | x_unmasked)`△损失函数决定模型是否能产生──

## 运送它.

看到`outputs/skill-sampling-tuner.md`技能选择新一代任务的样本参数,并在确定性解码需要时标记.

> 参见`outputs/skill-sampling-tuner.md`◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎

## 练习题

1. **Easy.**跑步`code/main.py`检查:排列3只应在03列中重量.
   中文翻译:运行 `code/main.py`抽查:第3行应该只在第0-3列中权重.
2. **Medium.**根据10个短提示,比较beam-4的困难与贪.beam总是赢得吗? (提示:通常用于翻译,而不是开放式聊天.)
   中文翻译:实现宽度为4个束搜索. 在10个短提示上比较束搜索和贪心搜索的困惑.束搜索一定更好吗?
3. **Hard.**实施投机解码:使用一个小的2层模型作为草案和一个6层模型作为验证器.测量长度100次的墙钟加速.64次验证输出与验证器的贪匹配.
   中文翻译:实现推测解码:用2层小模型作为草案模型,6层模型作为验证器――在100个长度为64的补充上测量实际加速比――确认输出与验证器的贪心解码一致――

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Causal mask | "The triangle" | Upper-triangular `-inf` matrix added to attention scores so position `i` only sees positions `≤ i`. |
| 因果掩码 | "三角矩阵" | 加到注意力分数上的上三角 `-inf` 矩阵，使位置 `i` 只能看到位置 `≤ i`。 |
| Next-token prediction | "The loss" | Cross-entropy of the model's distribution against the true next token at every position. |
| 下一个 token 预测 | "损失函数" | 模型分布与每个位置真实下一个 token 之间的交叉熵。 |
| Autoregressive | "Generate one at a time" | Feed output back as input; parallelism only during training, not during generation. |
| 自回归 | "逐个生成" | 将输出反馈为输入；仅在训练时并行，生成时不并行。 |
| Logits | "Pre-softmax scores" | Raw output of the LM head before softmax; sampling happens on these. |
| Logits | "softmax 前的分数" | LM 头在 softmax 之前的原始输出；采样基于这些值。 |
| Temperature | "Creativity knob" | Divide logits by T; T→0 = greedy, T→∞ = uniform. |
| 温度 | "创造力旋钮" | 将 logits 除以 T；T→0 为贪心，T→∞ 为均匀分布。 |
| Top-p | "Nucleus sampling" | Truncate distribution to smallest set summing to ≥p; sample from what remains. |
| Top-p | "核采样" | 将分布截断为累积概率 ≥ p 的最小集合；从剩余部分采样。 |
| Min-p | "Better than top-p" | Keep tokens where `p ≥ min_p × max_p`; adapts cutoff to sharpness of distribution. |
| Min-p | "比 top-p 更好" | 保留 `p ≥ min_p × max_p` 的 token；根据分布锐度自适应调整截断。 |
| Speculative decoding | "Draft + verify" | Cheap model proposes N tokens; big model verifies in parallel. |
| 推测解码 | "草案+验证" | 廉价模型提出 N 个 token；大模型并行验证。 |
| Teacher forcing | "Training trick" | During training, feed the true previous token, not the model's prediction. Standard for every seq2seq LM. |
| Teacher forcing | "训练技巧" | 训练时输入真实的前一个 token，而非模型的预测。所有 seq2seq 语言模型的标准做法。 |

## 继续阅读 继续阅读

- [Radford et al. (2018). Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)GPT-1.
  中文翻译:GPT-1 论文。
- [Radford et al. (2019). Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)GPT-2.
  中文翻译:GPT-2论文──
- [Brown et al. (2020). Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)GPT-3和在环境中学习.
  中文翻译:GPT-3 和上下文学习论文──
- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192)规格解码纸.
  中文翻译:推测解码论文──
- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py)可нони化因果性-LM参考码.
  中文翻译:HuggingFace Llama 因果语言模型参考代码──
