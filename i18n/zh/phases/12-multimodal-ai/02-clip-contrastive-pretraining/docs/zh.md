# 视觉语言预训练

> 开放AI的CLIP (2021) 证明了一个足够大的想法,可以在未来五年内实现:将图像编码器和文本编码器在同一向量空间中, 没有监督标签. 两千万个. 结果的嵌入空间进行零射击分类,图像文本检索,并作为其视觉塔插入每一个2026 VLM. siglip 2 (2025) 取代软max 通过sigmoid,以更低的成本扩展到CLIP之后. 这一课将从InfoNCE到sigmoid对式损失的数学进行,并建立了在 stdlib Python 中的训练步骤.

> **【中文解读】**通过使用400亿网络图文对比,通过比较损失将图像和文本编码到同一向量空间.

> **【拓展：CLIP→多模态大模型】**了解CLIP是理解整个多模态 AI 生态的起点.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, InfoNCE + sigmoid loss implementations) | **语言:** Python（标准库，InfoNCE + sigmoid 损失实现）
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 7 (Transformers) | **前置知识:** Phase 12 · 01（ViT patch），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**学本节前请先掌握:阶段12·01(ViT 把图像切成补丁);阶段11·04(嵌入式向量空间概念);阶段7(变压器自注意力)。本节核心数学是软max + 交叉,阶段7·04 有详细推导──
>  **【类比】**模型学会把每张图片和它的描述拉到量空间的同一位置,推出其他31999张图片的描述. 训练结束后,模型就能把"一张猫的照片"和真正的猫图画在一起,即使在训练中没有见过这只猫.

## 学习目标

- 通过互通信息来推导InfoNCE损失,并实现数量稳定的向量化版本.
  中文翻译:从互信息推导 InfoNCE 损失,并实现数值稳定的向量化版本──
- 解释为什么sigmoid对式损失 (SigLIP) 达到32768+批量,而没有全集的上空软max要求.
  中文翻译:解释为什么sigmoid 成对损失 (SigLIP) 可以扩展到32768+ 批次大小,而无需软max所需的全部集成开销.
- 通过构建文本模板来运行零截图的 ImageNet 分类 (`a photo of a {class}`) 和使用 argmax 与 cosine 类似性相比.
  中文翻译:通过构建文本模板`a photo of a {class}`)并对余弦相似度取 argmax 来运行零样本 图像网 分类。
- 列出CLIP/SigLIP预训练给你提供的四个杆:批量大小,温度,提示模板,数据质量.
  中文翻译:列举 CLIP / SigLIP 预训给你四杆:批次大小,温度,提示模板,数据质量――

## 问题 问题引入

监督CLIP前的视觉.收集标记数据集 (ImageNet: 1.2M图像, 1000 类),训练一个CNN,运输它.标签昂贵,标签偏向标签商可以同意,标签不会转移到新的任务没有细节调整.

> 之前的视觉是监督式的.收集标签数据集. 图像网:120万张图像,1000个类别),训练CNN,部署.

图像标题网有超过10亿个宽松标签的双色球免费.一个带有"我的狗马克斯在公园"的黄金回归器的图片带有监督信号.

> 网络上有超过10亿的免费使用的散布标签图片. 一张金毛猎犬的照片配备了"我的狗马克斯在公园里"的监督信号.

根据Clip的答案:把图像标题对应当作匹配任务. 鉴于一批N图像和N标题,学会与N-1分散注意力的标题匹配. 监督是"这两件事相应,这些N-1不. "没有类标签.没有人注释.只是一个反驳的损失.

> 监督信号是"这两种东西都属于一起;这 N-1 个不属于"――没有类别标签,没有人工标签,只有对比损失――

图像网的零射击效果是因为"一张猫的照片"嵌入了没有明确标记的猫的照片附近.这是每2026年VLM产生的一项投注.

> 得到的嵌入空间超越了CLIP的训练目标. 图像网 零样本分类有效,因为"猫的照片"嵌入到没有被明显标记为猫的猫图片附近.

## 概念的核心概念

> **【中文解读】**通过比较学习将图像和文本映射到同一量空间:相匹配图文对距离近,不相匹配推远. 在400亿图文对上训练后,无需微调即可实现零射图像分类,是OpenAI多模态能力的基石.

> **【拓展：CLIP 的应用生态】**CLIP的比较学习范式产生了大量应用:DALL-E 2/3使用 CLIP 引导图像生成,稳定扩散使用 OpenCLIP 作为安全过器,LLaVA使用 CLIP 视觉编码器连接 LLM 和图像理解──CLIP的零射击能力在 ImageNet 上达到76.2% 准确率,无需任何 ImageNet 训练数据──


> **【拓展：CLIP 的 zero-shot 能力】**在图像网上,CLIP ViT-L/14的零射准确率 (CCLIP ViT-L/14 准确率) 接近ResNet-50的全监督准确率 (CCLIP ViT-L/14 准确率) (76.7%) .


### 双码码器

克利普有两个塔楼:

> 有两个塔.

- 图像编码器`f`视频或ResNet,输出每张图像的D-dim向量.
  中文翻译:图像编码器 `f`视频或 ResNet,每张图像输出一个 D 维向量
- 文字编码器`g`转换器,每字幕输出一个D-dim向量.
  中文翻译:文本编码器 `g`微型变压器,每条描述输出一个 D 维向量――

两座塔都将输出正常化到单位长度.`cos(f(x), g(y)) = f(x)^T g(y)`由于它们都是单位标准.

> 两个塔都将输出归纳为长度单位.`cos(f(x), g(y)) = f(x)^T g(y)`因为这两者都是单位向量.

> ️ **【易错点】**忘记归一化(L2正常化) 就计算相似度 → 向量模长大的样本天然有更大的点积,模型会偏向"长向量"而不是"语义匹配"──修复:每次前进 后必须`f = f / ||f||`然后才算`cos`,我知道.
>  **【困惑】**问:为什么不用余弦相似度?A:余弦只看方向不看模长,对"亮度不同但内容相同"的图片是鲁棒的;欧氏距离被向量模长主导.

对于一批N (图片,字幕) 双,构建类似矩阵`S`形状`(N, N)`其他:

> 对于一批 N 个图像,描述) 对,构建形状为`(N, N)`类似度矩阵`S`其他:

```
S[i, j] = cos(f(x_i), g(y_j)) / tau
```

在哪里`tau`是学习温度 (CLIP初始化为0.07;在日记空间中学习).

> 其中`tau`是一个可学习的温度参数.

### 信息NCE损失

通过Clip,在行列和列中使用对称的交叉透:

> 关键对行和列使用对称交叉:

```
loss_i2t = CE(S, labels=identity)     # each image's positive is its own caption
loss_t2i = CE(S^T, labels=identity)   # each caption's positive is its own image
loss = (loss_i2t + loss_t2i) / 2
```

这就是InfoNCE.CE中软max强迫每个图像比批次中的其他所有标题更符合其标题."负"是所有其他批次的项目.较大的批次 =更多负面 =更强的信号.Clip训练在批次32k;规模是重要的.

> 这就是InfoNCE──CE 中的软度max 强制每张图像与自己描述的匹配度高于批次中所有其他描述──"负样本"是批次中所有其他项目──批次越大 = 负样本越多 = 信号越强──CLIP 在32k批次下训练;规模很重要──

> ️ **【易错点】**批量_尺寸太小(如 64) 训不出好 CLIP负样本太少,模型学不到"什么算真正的相似"──CLIP 原文批量_尺寸=32768 才有效果──如果你只能运行批量=256,要么用 SigLIP(不需要大批量),要么用梯度累积模拟大批量(但不等价)──
>  **【类比】**像"找卧底游戏":32k张图片对应32k 个描述,每个图片都必须在一堆描述中找到自己的真相对应――卧底负样本) 越来越多,游戏越难,学到的东西越扎实――

### 温度

`tau`控制软max的敏度.低tau →敏分布,硬负矿效应.高tau →软,所有样本都贡献.CLIP学习 log(1/tau),切断以防止崩.SigLIP 2修复初始tau,并使用学习偏见.

> `tau`控制软max 的度──低tau → 尖分布,具有负面的挖掘效果──高tau → 平滑,所有样本都有贡献──CLIP 学习日志1/tau),并剪切以防止崩──SigLIP 2 固定初始 tau 并使用可学习的偏置替代──

### 为什么sigmoid 尺度更好 (SigLIP)

在分布式训练中,你必须把每个嵌入到每个复制品中,然后做软max.这是世界尺寸的方形.

> 在分布式训练中,你必须将每个嵌入到每个副本,然后做软max――通信开销与世界小呈二关系――

siglip取代 softmax 用元素智能sigmoid:为每对 `(i, j)`输出是"这些是匹配的对吗?"正数类标签是对角,其他的一切都是负数.

> 标LIP 用个元素标M 换软max:对每对`(i, j)`损失是对角线的二分类. 损失是对角线的二分类.

>  **【困惑】**问:为什么软max 需要全部集合而 sigmoid 不需要?A:软max 的分母是"所有N2 个配对的相似度和",每张GPU 必须看到全部;sigmoid 只看每个 (i,j) 配对独立判断是/否匹配,不依赖全局信息――多GPU 训练时 sigmoid 损失可以在本地计算后减少――
>  **【类比】**信息NCE = "32k 选 1 选题",必须看完整张卷子才能做;SigLIP = "32k 个判断题(这对配对吗?)",每个独立答案.前者需要老师收齐所有卷子,后者每个学生自己批评.

```
L = -1/N sum over (i, j) [ y_ij log sigmoid(S[i,j]) + (1-y_ij) log sigmoid(-S[i,j]) ]
```

`y_ij = 1`如果`i == j`任何 GPU 都需要一个全集. 每个 GPU 都计算出其本地块和数量. SigLIP 2 量化为 32k-512k 批量便宜, CLIP 需要比较多的通信.

> `y_ij = 1`如果`i == j`没有需要全部收集. 每个GPU 计算其本地块并求和. SigLIP 2 可以低成本扩展到32k-512k批次,而CLIP 需要相应更多的通信.

### 零射分类

给给N类名称,为每个类构建一个文本模板:

> 给定N 个类名称,为每个类构建文本模板:

```
"a photo of a {class}"
```

嵌入每个模板与文本编码器. 嵌入图像与图像编码器. Argmax cosine 类似性 = 预测类. 没有对目标类进行培训.

> 用文本编码器嵌入每个模板――用图像编码器嵌入图像――Argmax 余弦相似度 = 预测类别――无需在目标类别上训练――

> ️ **【易错点】**直接使用`"cat"`作为提示 → 比 `"a photo of a cat"`差 10+ 个百分点──CLIP 训练时文本端看的描述大多是完整的句子,单词作为提示会让分布偏移──修复:始终使用模板`"a photo of a {class}"`现在,我还在做什么?
>  **【困惑】**问:图像网1000类全算一遍文嵌入 不是很慢吗?A:只算一次然后缓存──1000个提示 在文本编码器里跑一遍(毫秒级),后面每张新图片只需要1次图像嵌入+1000次余弦相似度(向量化矩阵乘)──

快速模板是重要的.CLIP的原始论文每类使用80个模板 (平坦,艺术,照片,绘画等) 并平均嵌入. +3 图像网点.现代使用通常选择一个或两个模板.

> 提示模板很重要──CLIP 原始论文每类使用80个模板 ((普通、艺术、照片、绘画等) 并对嵌入取平均──ImageNet 上升3个百分点──现代用法通常选择一个两个模板──

### 线性探测器和细调

零射线是基线.线性探测器 (为目标类的CIP功能加上一个线性层) 在域内任务中比零射线更好.完整的细节调整在域内探测器比线性探测器更好,但可以损害零射线转移.三个模式具有三个折扣.

> 零样本是基线――线性探测(在结结的 CLIP特征上为目标类型训练一个线性层) 在域内任务上超越零样本――全量微调在域内超越线性探测,但可能损害零样本迁移――三种模式,三种权衡――

### 标LIP 2: NaFlex 和密集的特征

siglip 2 (2025) 补充:

> 标签: 标签:

- 纳弗莱克斯:单个模型处理可变的面积比和分辨率.
  中文翻译:NaFlex:单一模型处理可变宽高比和分辨率
- 较好的密度功能用于细分和深度估计, 针对于VLM中作为结的脊柱.
  中文翻译:更好的密集特征用于分和深度估计,目标是作为VLM中结干网络.
- 多语言:在CIP仅使用英语的100多种语言上接受培训.
  中文翻译:多语言:在100种语言上训练,而CLIP仅限于英文.
- 升到400米的1B参数尺度.
  中文翻译:10亿参数规模,而Clip最高为400亿.

在2026年开放的VLM中,SigLIP 2 SO400m/14是默认的视觉塔.Clip仍然是纯图像文本检索的默认,其中特定的LAION-2B训练分布与查询模式匹配.

> 在2026年开放的VLM中,SigLIP 2 SO400m/14是默认视觉塔.在纯图文检查中,CLIP仍然是默认选择,特别是当特定的LAION-2B 训练分布匹配你的查询模式时.

### 其他技术: 技术技术

简单的数据量度:CLIP (Google, 2021):与CLIP相同的想法,1.8B双尺度,90%的噪音. 已证明的噪音数据量度.OpenCLIP (LAION):在LAION-400M/2B上CLIP的开放复制,多个尺度,开放检查点.EVA-CLIP:从面具图像建模开始;VLM的强大脊柱.BASIC:谷歌的CLIP+ALIGN混合动力.所有相同的家族,不同的数据和调整.

> 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签

### 零射击的天花板

CLIP类型的模型约占76%的ImageNet零射 (CLIP-G,OpenCLIP-G).此外需要更大的数据 (SigLIP 2获得80%+) 或结构变化 (监督头部,更多参数).基准值是和;实际值是下游VLM所消耗的嵌入空间.

> 通过Clip 类模型在 ImageNet 零样本分类上限约为76%;;CLIP-G、OpenCLIP-G) ・超过这个水平需要更大的数据(SigLIP 2 达到80%+) 或结构变更(监督头、更多参数) ・基准测试正在和;真正的价值在下游VLM 消费的嵌入空间中──

>  **【困惑】**学习完本节还会问:1) 为什么CLIP的零射不像GPT-4那样理解"图中两个人做什么"?CLIP只学到了"图文匹配",没有学到细粒度的关系推理,那就是VLM(像LLaVA) 的工作.

## 用它实现框架
```figure
multimodal-fusion
```

## 用它

`code/main.py`执行:

> `code/main.py`实现了:

1. 玩具双码码器 (基于hash的图像功能,文字图表功能),以便您可以在无的情况下看到InfoNCE形状.
   中文翻译:一个玩具双编码器 (基于哈希的图像特征,文本字符特征),无需编号即可看到InfoNCE的形态.
2. 在纯Python中输入InfoNCE (通过 log-sum-exp进行数字稳定).
   中文翻译:纯Python实现的InfoNCE 损失 (通过日志-总和-exp实现数值稳定性) ⋅
3. 形双向损失比较.
   中文翻译:Sigmoid 成对损失用于对比.
4. 零射分类例程:计算与一组文本提示相似的共数,预测的 argmax.
   中文翻译:零样本分类例程:计算与一组文本提示的余弦相似度,argmax 得出预测──

运行它,看输法曲线.绝对数字是玩具;形状与真正的Clip训练师的排放相匹配.

> 运行它并观察损失曲线――绝对数值是玩具级的;但形状与真实的CLIP训练机的输出匹配――

## 运送它.

这一课产生了`outputs/skill-clip-zero-shot.md`鉴于图像集 (通过路径) 和目标类的列表,它使用CLIP模板构建文本提示,并将两个侧面嵌入到指定检查点 (例如,`openai/clip-vit-large-patch14`),并返回与相似度分数的前1/前5预测.技能拒绝对未列入提示列表的类别提出索赔.

> 本课产出发 `outputs/skill-clip-zero-shot.md`△给定一组图像 (通过路径) 和一组目标类别,它使用 CLIP 模板构建文本提示,使用指定的检查点 (如`openai/clip-vit-large-patch14`) 嵌入两侧,并返回与相似度分数的前-1 /前-5 预测――该技能绝对拒绝在提示列表中的类别做判断――

## 练习题

1. 通过手动实现4对的InfoNCE. 构建4x4相似度矩阵,运行软max,选择对角,计算交叉. 根据手动计算验证您的Python实现.
   中文翻译:手动实现 4 对样本的 InfoNCE──构建 4x4 相似度矩阵,运行软max,提取对角线,计算交叉──验证你的Python 实现与手算一致──

2. siglip使用偏差参数`b`除了温度: `S'[i,j] = S[i,j]/tau + b`什么角色?`b`对于一轮的负数比正数多得多,请参阅SigLIP第3节 (arXiv:2303.15343).
   中文翻译:SigLIP除了温度还使用偏置参数`b`其他:`S'[i,j] = S[i,j]/tau + b`△当批次存在较大的类别不平衡时,`b`起什么作用?阅读SIGLIP 第3节

3. 建立一个零射击分类器, 试试两个提示模板:`a photo of a {class}`其他`a picture of a {class}`测量100个试图图的精度. 模板组单击吗?
   中文翻译:构建猫狗零样本分类器──尝试两种提示模板:`a photo of a {class}`和 `a picture of a {class}`△ 100张测试图像上测量准确率――模板集成是否优于单一模板?

4. 计算软max InfoNCE 与 sigmoid 的通信成本,对 512GPU 运行在批量 32k. 什么规模为 O(N),哪个为 O(N ^ 2)? 引用 SigLIP 部分 4.
   中文翻译:计算 512 GPU、批次 32k 下软max InfoNCE 与 sigmoid 成对损失的通信成本──哪个是 O(N),哪个是 O(N^2)?引用 SigLIP 第4节──

5. 根据数据量化结果,再现他们对数据量化的结论:在固定模型尺寸下,ImageNet零截图精度和训练数据尺寸之间的日志线性关系是什么?
   中文翻译:阅读OpenCLIP 缩放定律论文 ((arXiv:2212.07143,Cherti 等人) 〕 从图表中复现他们关于数据扩展的结论:在固定模型大小下,ImageNet 零样本准确率与训练数据大小之间的数线性关系是什么?

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| InfoNCE | "Contrastive loss" | Cross-entropy over a batch's similarity matrix; each item's positive is its paired item, negatives are everything else | 批次相似度矩阵上的交叉熵；每项的正样本是其配对项，负样本是所有其他项 |
| Sigmoid loss | "SigLIP loss" | Per-pair binary cross-entropy; no softmax, no all-gather, scales cheaply in distributed training | 逐对二分类交叉熵；无 softmax，无 all-gather，分布式训练中扩展成本低 |
| Temperature | "tau" | Scalar that scales logits before softmax/sigmoid; controls sharpness of the distribution | softmax/sigmoid 前缩放 logits 的标量；控制分布的锐度 |
| Zero-shot | "no-finetune classification" | Use text prompts to construct class embeddings and classify by cosine similarity; no training on target classes | 用文本提示构建类别嵌入，通过余弦相似度分类；无需在目标类别上训练 |
| Prompt template | "a photo of a ..." | Text scaffold around a class name; affects zero-shot accuracy by 1-5 points | 类别名周围的文本支架；影响零样本准确率 1-5 个百分点 |
| Dual encoder | "Two-tower" | One image encoder + one text encoder, outputs in shared D-dim space | 一个图像编码器 + 一个文本编码器，输出在共享的 D 维空间 |
| Hard negative | "Tough distractor" | A negative similar enough to the positive that the model has to work to separate them | 与正样本足够相似的负样本，模型需要努力区分它们 |
| Linear probe | "Frozen + one layer" | Train only a linear classifier on top of frozen features; measures feature quality | 仅在冻结特征之上训练线性分类器；衡量特征质量 |
| NaFlex | "Native flexible resolution" | SigLIP 2 capability to ingest images at any aspect ratio and resolution without resizing | SigLIP 2 以任意宽高比和分辨率输入图像的能力，无需调整大小 |
| Temperature scaling | "log-parametrized tau" | CLIP parametrizes `log(1/tau)` so gradients behave; clips to prevent collapse to near-zero tau | CLIP 参数化 `log(1/tau)` 使梯度行为正常；裁剪防止 tau 崩溃到接近零 |

## 继续阅读 继续阅读

- [Radford et al. — Learning Transferable Visual Models From Natural Language Supervision (arXiv:2103.00020)](https://arxiv.org/abs/2103.00020)Clip文件.
  中文翻译:CLIP论文。
- [Zhai et al. — Sigmoid Loss for Language Image Pre-Training (arXiv:2303.15343)](https://arxiv.org/abs/2303.15343)   
  中文翻译:SigLIP论文。
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786)多语言 + NaFlex.
  中文翻译:多语言 + NaFlex。
- [Jia et al. — ALIGN (arXiv:2102.05918)](https://arxiv.org/abs/2102.05918)使用噪音的网页数据进行扩展.
  中文翻译:用噪声网络数据扩展──
- [Cherti et al. — Reproducible scaling laws for contrastive language-image learning (arXiv:2212.07143)](https://arxiv.org/abs/2212.07143)开放CLIP扩展法
  中文翻译:OpenCLIP 缩放定律──
