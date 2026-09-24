# 创建一个变压器从零开始  石头  从零构建变压器  毕业项目

> 十三课,一个模型,没有快捷方式.

> **【中文解读】**整合所有知识,从零实现完整的GPT架构――这是本阶段的核心实践理解这个,你就能读懂任何变压器的代码――

**Type:** Hands-on | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 7 · 01 through 13. Don't skip. | **前置知识:** Phase 7 · 01 through 13. Don't skip.
**Time:** ~120 minutes | **时间:** ~120 分钟

## 问题 问题引入

你已经读过每篇论文,你已经实现了注意力,多头分区,位置编码,编码和解码区块,BERT和GPT损失,MoE,KV缓存.现在让它们一起完成一个真正的任务.

> 你已经读过每篇文章. 你已经实现了注意力,多头分离,位置编码,编码器和编码器块,BERT 和 GPT 损失,MoE,KV 缓存.

终点:训练一个小的单独解码器变压器端到端进行角色级语言建模任务.它读出莎士比亚.它生成了新的莎士比亚.它足够小,以在10分钟内在笔记本电脑上训练.它足够正确,更大的数据集和更长的训练交换给你一个真正的LM.

> 毕业项目:在字符级语言建模任务上端到端训练一个小型解码器专用变压器――它读了莎士比亚,产生了新的莎士比亚――它足够小,可以在笔记本上完成训练10分钟内――它足够正确,转换成更大的数据集和更长的训练时间就能得到真正的语言模型――

卡帕蒂的2023年纳米GPT教程是每个学生至少写一次的参考实现.我们把形状抬起,重新整理了我们所覆盖的内容.

> 这就是课程的"纳米GPT"――它不是原创的卡帕蒂2023年纳米GPT课程是每个学生至少写一次的参考实现――我们借鉴了它的结构,并根据我们学到的内容进行了改造――

> **【中文解读】**这个毕业项目将在13节前整合所有知识:字符级语言建模,代码 嵌入,位置编码,RMSNorm,多头因果注意力,SwiGLU FFN,残差连接,训练一个可以在笔记本上完成10分钟内的莎士比亚生成机.

> **【拓展：从 nanoGPT 到生产级 LLM】**卡帕蒂的纳米GPT是学习变压器的最佳起点. 从纳米GPT到生产级LLM的关键差异在于:数据规模 ((从MB到TB) 培训基础设施 ((从单个GPU到数千个GPU集群) 分布式培训 ((数据并行、模型并行、流水线并行) ),以及后训练 ((SFT + RLHF) ),但核心架构是一样的.

## 概念的核心概念

![Transformer-from-scratch block diagram](../assets/capstone.svg)

建筑,注释:

> 架构,带注释:

```
input tokens (B, N)
   │
   ▼
token embedding + positional embedding  ◀── Lesson 04 (RoPE option)
   │
   ▼
┌──── block × L ────────────────────┐
│  RMSNorm                          │  ◀── Lesson 05
│  MultiHeadAttention (causal)      │  ◀── Lesson 03 + 07 (causal mask)
│  residual                         │
│  RMSNorm                          │
│  SwiGLU FFN                       │  ◀── Lesson 05
│  residual                         │
└────────────────────────────────── ┘
   │
   ▼
final RMSNorm
   │
   ▼
lm_head (tied to token embedding)
   │
   ▼
logits (B, N, V)
   │
   ▼
shift-by-one cross-entropy            ◀── Lesson 07
```

### 我们运送的东西

> 我们交付的内容:

- `GPTConfig`一个配置所有超参数的地方.
  翻译: 中文`GPTConfig` 一个配置所有超参数的地方.
- `MultiHeadAttention`因果性,批量,可选的闪光式路径 (PyTorch的) `scaled_dot_product_attention`)
  翻译: 中文`MultiHeadAttention`因果的量,可选的闪光风格路径`scaled_dot_product_attention`
- `SwiGLUFFN`现代的FFN.
  翻译: 中文`SwiGLUFFN`现代 FFN。
- `Block`预规,残留包装注意力+FFN.
  翻译: 中文`Block` 前归一化,残差包裹的注意力+FFN。
- `GPT`嵌入式,堆积式块,LM头,生成().
  翻译: 中文`GPT` 嵌入,堆叠块,LM头,生成.
- 训练循环与亚当W,数 LR,梯度剪切.
  中文翻译:带亚当W、余弦学习率、梯度剪剪的训练循环──
- 对于莎士比亚的文字.
  中文翻译:莎士比亚文本上的字符级分词器──

> **【中文解读】**完整的GPT实现包含:配置类型、多头因果注意力(可选Flash注意力)、SwiGLU FFN、前归结残差块、完整的GPT 模型类型(嵌入+堆叠块+LM头+生成函数)、AdamW+余弦学习率训练循环──为了简单地说,使用学习位置嵌入(而不是RoPE) 并未实现KV缓存,但练习要求你添加这些──

### 我们不送什么东西

> 我们不交付的内容:

- 在课程04中概念上实现了 RoPE.在这里我们使用学习的位置嵌入式来简单化.
  中文翻译:RoPE  在第04课有概念实现──这里为简洁起见使用学习式位置嵌入──练习要求你替换为RoPE──
- 随着生成的过程中,每个生成步骤重新计算注意力.慢慢,但更简单.练习要求你添加一个KV缓存.
  中文翻译:生成时的KV 缓存  每个生成步骤对完整前重新计算注意力――更慢但更简单――练习要求你添加KV 缓存――
-  PyTorch 2.0+ 自动发送,如果输入相匹配,我们使用`F.scaled_dot_product_attention`现在,我们要去.
  中文翻译:闪光注意  PyTorch 2.0+ 在输入匹配时自动分派;我们使用 `F.scaled_dot_product_attention`,我知道.
- 单个FFN每块.你在第11课中看过MoE.
  中文翻译:MOE  每块单个FFN──你在第11课中见过MOE──

### 目标指标

在MacM2笔记本电脑上,一个四层,四头,d_model=128GPT训练了2000步`tinyshakespeare.txt`其他:

> 在Mac M2笔记本上,4层、4头、d_model=128的GPT 在`tinyshakespeare.txt`上训练2000步:

- 训练损失约6分钟内从4.2 (随机) 降至1.5分钟.
  中文翻译:训练损失从约4.2随机) 在约6分钟内收到约1.5.
- 采样产品看起来像莎士比亚:古老的词,线条断裂,像"ROMEO:"这样的名字出现.
  中文翻译:采样输出看起来像莎士比亚:古词、换行、"ROMEO:"等专名词出现──
- 值损失 (最后10%的文本被保留) 密切跟踪训练损失;在这个规模/预算上没有过度适应.
  中文翻译:验证损失 (留出最后10%的文本) 紧跟训练损失;在这个规模/预算下没有过拟合.

> **【拓展：从字符级到子词级 Tokenizer】**本项目使用字符级代币器(简单但低效) ・生产级 LLM 使用 BPE(Byte Pair Encoding) 或 SentencePiece等子词级代币器──Llama 使用 BPE,GPT-4 使用 cl100k_base BPE代币器──子词代币化 在词汇量、序列长度和语义粒度之间取得平衡,是现代 LLM的标志──

## 建立它,实现它.
```figure
n5-block-stack
```

## 建立它

这堂课使用PyTorch.`torch`现在,我们可以在这个地方做什么?`code/main.py`剧本处理:

> 本课使用 PyTorch──安装 `torch`参见  计算机`code/main.py`◎该脚本处理:

- 下载`tinyshakespeare.txt`如果没有 (或阅读本地副本).
  中文翻译:如果缺失则下载 `tinyshakespeare.txt`没有什么可说的.
- 字节级卡标记器.
  中文翻译:字节级字符分词器──
- 列车/车间分为90/10.
  中文翻译:90/10 的训练/验证分分.
- 训练循环,在支持的硬件上自动播放 bf16.
  中文翻译:支持硬件上的bf16自动混合精度训练循环──
- 训练结束后,
  中文翻译:训练完成后的采样.

### 步骤1:数据

```python
text = open("tinyshakespeare.txt").read()
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda xs: "".join(itos[x] for x in xs)
```

只有65个字符,有很小的词汇,可以用4字节的词汇,没有BPE,没有标记器戏剧.

> 适配 4 字节词号尺寸,没有BPE,没有分词器的麻烦.

### 步骤2:模型

看到`code/main.py`区块是课05 预规,RMSNorm,SwiGLU,因果MHA的教科书.

> 参见`code/main.py`△该块是第05课的教科书实现前归结"",RMSNorm"",SwiGLU"",因果多头注意力―4/4/128 的参数:约800K―

### 步骤3:训练循环

随机取长度-256个标志窗户,向前,转变为一个,反向,亚当W步骤,记录,重复.

> 获取随机批量长度为 256 个标志窗口──前向传播──偏移一位的交叉──反向传播──AdamW 步进──记录──重复──

```python
for step in range(max_steps):
    x, y = get_batch("train")
    logits = model(x)
    loss = F.cross_entropy(logits.view(-1, vocab_size), y.view(-1))
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    opt.zero_grad()
```

### 步骤4:样本

给出提示,反复转发,从顶部p登录中取样,添加,然后继续.

> 给定一个提示,反复前向传播,从顶部的逻辑 采样,追加,继续──500个标志 后停止──

### 步骤5:读取输出

在2000步后:

> 两千步后:

```
ROMEO:
Away and mild will not thy friend, that thou shalt wit:
The chief that well shame and hath been his friends,
...
```

没有莎士比亚,但莎士比亚形状, 赢得了800万个参数和6分钟的笔记本电脑.

> 没有莎士比亚,但像莎士比亚一样,

## 用它实现框架

这块顶石是参考架构,有三个扩展,

> 这项毕业项目是一个参考架构.

1. **Swap the tokenizer.**使用BPE (例如:`tiktoken.get_encoding("cl100k_base")`字母尺寸从65升至5万. 模型容量需要扩大,以补偿.
   翻译: 中文**替换分词器。**使用BPE`tiktoken.get_encoding("cl100k_base")`◎词表大小从65跳到约50,000──模型容量需要相应扩展──
2. **Train on a bigger corpus.**使用`OpenWebText`或`fineweb-edu`单个A100上的10B代币需要24小时才能实现125M的GPT.
   翻译: 中文**在更大的语料上训练。**使用 `OpenWebText`或`fineweb-edu`面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面: 面
3. **Add RoPE + KV cache + Flash Attention.**下面的练习将你通过每一个.
   翻译: 中文**添加 RoPE + KV 缓存 + Flash Attention。**下面的练习将引导你完成每一步.

这最终成为一个125M参数GPT,产生流利的英语.不是一个边界模型.但同样的代码路径只是更大是卡帕蒂,埃勒艾伊和艾伦研究所在2026年用来训练研究检查站.

> 最终得到一个能产生流利英语的125M参数GPT──不是前沿模型──但同样的代码路径只是更大是卡帕迪、电路AI 和艾伦研究所在2026年训练研究检查点所使用的──

> **【拓展：Karpathy 的 nanoGPT 与教育意义】**通过300行PyTorch实现的完整可训练的GPT,这种"从零构建"的教学方法让你真正理解每个组件的作用,而不是把变压器当作黑盒子.

## 运送它.

看到`outputs/skill-transformer-review.md`技能检查了所有13个上课的变压器从零开始实施的正确性.

> 参见`outputs/skill-transformer-review.md`△ 检查一个从零构建的变压器实现,检查所有前13课的正确性.

## 练习题

1. **Easy.**跑步`code/main.py`检查您训练有素的模型最后一步验证损失低于2.0. 改变`max_steps`                                                                                                                                                                                                                                                              
   中文翻译:运行 `code/main.py`证实你训练模型的最终步骤证实损失低于2.0――将`max_steps`证券损失从2000改至5000的情况是否继续改善?
2. **Medium.**取代学习的位置嵌入式用RoPE. 应用转换到Q和K内部`MultiHeadAttention`列车和验证的值损失至少同样低.
   中文翻译:用RoPE 替换学习式位置嵌入.`MultiHeadAttention`中对Q 和 K 应用转移──训练并验证验证损失至少不差──
3. **Medium.**通过测试,在测试循环中实现KV缓存. 生成500个代币,无论是没有缓存. 笔记本电脑的墙钟应该提高520x.
   中文翻译:在采样循环中实现KV缓存――有缓存和无缓存各产生500个代币――笔记本应该有5-20倍的实际时间改善――
4. **Hard.**加入第二个头到模型中,预测下一个加一个代币 (MTP 从DeepSeek-V3的多代币预测).
   中文翻译:添加第二个头预测下一个代币(MTP来自DeepSeek-V3的多个代币预测) ――联合训练――有帮助吗?
5. **Hard.**换取每块单个FFN用4个专家MoE.路由器+顶-2路由器.看看在匹配的活跃参数时的值损失变化.
   中文翻译:将每块的单个FFN 换成4 专家MoE──路由器 + top-2 路由──观察在匹配活跃参数下验证损失的变化──

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| nanoGPT | "Karpathy's tutorial repo" | Minimal decoder-only transformer training code, ~300 LOC; the canonical reference. |
| nanoGPT | "Karpathy 的教程仓库" | 最小解码器专用 Transformer 训练代码，约 300 行；经典参考。 |
| tinyshakespeare | "The standard toy corpus" | ~1.1 MB of text; every character-LM tutorial since 2015 uses it. |
| tinyshakespeare | "标准玩具语料库" | 约 1.1 MB 文本；自 2015 年以来每个字符级语言模型教程都用它。 |
| Tied embeddings | "Share input/output matrix" | LM head weight = transpose of token embedding matrix; saves parameters, improves quality. |
| 绑定嵌入 | "共享输入/输出矩阵" | LM 头权重 = token 嵌入矩阵的转置；节省参数，提高质量。 |
| bf16 autocast | "Training precision trick" | Run forward/back in bf16, keep optimizer state in fp32; standard since 2021. |
| bf16 自动混合精度 | "训练精度技巧" | 前向/反向用 bf16，优化器状态用 fp32；2021 年以来的标准。 |
| Gradient clipping | "Stops spikes" | Cap global grad norm at 1.0; prevents training blowups. |
| 梯度裁剪 | "阻止尖峰" | 将全局梯度范数限制在 1.0；防止训练爆炸。 |
| Cosine LR schedule | "The 2020+ default" | LR ramps up linearly (warmup) then decays cosine-shaped to 10% of peak. |
| 余弦学习率调度 | "2020+ 默认" | 学习率线性升温（warmup）然后余弦衰减到峰值的 10%。 |
| MFU | "Model FLOP Utilization" | Achieved FLOPs / theoretical peak; 40% dense, 30% MoE is strong in 2026. |
| MFU | "模型 FLOP 利用率" | 实际 FLOPs / 理论峰值；2026 年稠密 40%、MoE 30% 是好的。 |
| Val loss | "Held-out loss" | Cross-entropy on data the model never saw; overfit detector. |
| 验证损失 | "留出损失" | 模型从未见过的数据上的交叉熵；过拟合检测器。 |

## 继续阅读 继续阅读

- [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/)经典的注释实施.
  中文翻译:哈佛 NLP 的注解版 变压器,经典参考实现──
