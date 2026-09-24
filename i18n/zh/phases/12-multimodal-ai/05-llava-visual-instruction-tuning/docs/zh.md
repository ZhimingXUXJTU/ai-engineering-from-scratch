# 视觉指令微调

> 拉瓦 (四月2023年) 是地球上最多复制的多式建筑. 它用2层MLP取代BLIP-2的Q-Former,用天真的代币连接取代Flamingo的门禁交叉注意力,并从仅仅是文字的标题中训练了GPT-4生成的158k视觉指令转折. 任何在2023年至2026年之间建造VLM的实践者都会构建一些LLaVA的变体. 增加了AnyRes. 拉瓦-下一个升级分辨率. 单一的图像,多个图像和视频. 这一课阅读了食谱,应用了投影机,并解释了"简单的获胜"的原因.

> **【中文解读】**拉瓦是2023-2026年间被复制的最多模态架构.它的核心思想非常简单:使用2层MLP将视觉编码器的输出投影到语言模型的嵌入空间,然后将视觉代币直接拼接到文本序列中.

> **【拓展：多模态大模型的起源】**在LLaVA之前,多模态模型主要依赖于复杂的跨模态注意力机制 (如Flamingo的门控交叉注意力,BLIP-2的Q-Former)  LLaVA的成功标志着多模态研究从"设计更好的跨模态接口"转向"更简单的接口+更多数据"的范转变.

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, projector + instruction-template builder)  | **语言：Python（标准库，投影器 + 指令模板构建器）**
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 11 (LLM Engineering — instruction tuning)  | **前置：阶段12第02课（CLIP）、阶段11（LLM工程——指令微调）**
**Time:** ~180 minutes  | **时长：约180分钟**

>  **【前置】**学本节前请先掌握:阶段12·02(CLIP 视觉编码器);阶段12·03(BLIP-2 桥接,对照学习);阶段11·08(指示调整指令微调)。LLaVA 是BLIP-2 的反面刻意简化桥接,靠数据取胜──
>  **【类比】**拉瓦 MLP = "576页原文整本贴给 LLM"――前者省纸张但丢了信息,后者费纸张但 LLM 看得到全部细节LLM上下文变长后",费纸"不再是问题,拉瓦自然就赢了――

## 学习目标

- 构建一个2层MLP投影器,将ViT补丁嵌入 ((维度1024) 映射到LLM嵌入维度 ((维度4096) ⋅
- 走在LLaVA两阶段的配方: (1) 投影机在558k标题对, (2) 视觉指令调节在158kGPT-4生成的转折.
- 构建一个LLaVA格式提示词,包含图像代币占位符、系统提示和用户/助手轮次.
- 解释为什么社区从Q-Former转向MLP,尽管Q-Former在代币预算上更优优.

## 问题背景

蓝皮-2的Q-Former (课时12.03) 将图像压缩到32个代币. 清洁,高效,适合基准. 但它有两个问题.

首先,Q-Former可以训练,但其丢失并不是最终任务.第一阶段训练ITC+ITM+ITG.第二阶段训练LM损失.查询学习一些中间表示,LLM然后必须解码.信息在瓶中丢失.

第二,Q-Former需要188万个参数,在LLaVA的2023级别上,你必须与你的目标LLM共同设计.改变LLM,重新训练Q-Former.改变视觉编码器,重新训练.每个组合都是一个独立的研发项目.

> **【中文解读】**蓝牙二号的Q-Former将图像缩小为32个代币,看起来高效,但有两个核心问题: 1) 训练目标不一致 第一阶段使用ITC/ITM/ITG损失,第二阶段才使用语言建模损失,信息在瓶中丢失; 2) 参数大大188M) 和特定的LLM 合,换LLM就需要重新训练.

简单的LLaVA答案是令人尬的:取了ViT的576个补丁代币,`1024 → 4096 → 4096`没有瓶,没有阶段1预训练, 只是训练MLP直接LM损失.

> **【中文解读】**通过一个2层MLP,直接把ViT的576个补丁代币`1024 → 4096 → 4096`),然后全部丢进了LLM的输入序列.

> ️ **【易错点】**第一阶段必须训练!很多人错误认为可以跳过第一阶段 直接做指示微调不行!没有训练的投影机输出随机向量,LLM 完全看不懂视觉代币 含义,第二阶段将让LLM 把视觉代币 当噪音忽略掉.

数据来自哪里?LLaVA的第二个见解:使用GPT-4 (仅用于文字) 来生成指令数据.为图像提供GPT-4的COCO标题和边界框数据,要求它产生对话,描述和复杂的推理问题.158k的指令响应免费转换.没有人注释.

> **【中文解读】**数据从哪里来?LLaVA的第二个创新:使用GPT-4 (纯文本模式) 生成指令数据――将COCO图像的描述文本和边界框信息给GPT-4,让它生成对话,描述和推理问题答案,得到158k条指令回复对,完全不需要人工标签――

结果是,VLM在8架A100上运行了一天,在MMMU上击败了Flamingo,并发出了一个可以扩展社区的开放检查点.到2023年底,它已经产生了50多个叉子.

> **【拓展：LLaVA 的产业影响】**拉瓦证明了VLM不需要庞大的计算能力8张A100 跑一天就够了. 这大大降低了多模态研究的门,推动了开源VLM生态的爆发. 在金融场景中,拉瓦架构被用于理解财报图表,票据图像等,是文件理解管道的基础组件.

## 概念的核心概念

> **【中文解读】**通过视觉指令微调让模型学会看图说话.核心创新:使用GPT-4 生成多模态指令数据,将图像描述转化为问答对应.

> **【拓展：LLaVA 的开源生态】**拉瓦是最成功的开源多模态模型――拉瓦-下一个支持任意分辨率输入,拉瓦-一视觉统一图像和视频理解――性能接近GPT-4V的80%,产生了大量衍生模型――


### 建筑,建筑.

,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
- 视觉编码器:CLIP ViT-L/14 @ 336 (在第一阶段冷,可选解,第二阶段可选解).
- 投影器: GELU 激活的2层MLP+GELU激活,`1024 → 4096 → 4096`现在,我们要去.
- 语言模型:Vicuna-13B (后来的Llama-3.1-8B /后续使用Llama-3.1-8B).

图像+文本提示的前向传播:

```
img -> ViT -> 576 patches of dim 1024           # 图像 -> ViT -> 576个维度1024的补丁
patches -> MLP -> 576 tokens of dim 4096         # 补丁 -> MLP -> 576个维度4096的token
prompt: system + "<image>" placeholder + user question  # 提示词：系统提示 + <image>占位符 + 用户问题
replace <image> token with the 576 projected tokens      # 用576个投影token替换<image>
feed the full sequence to the LLM                       # 将完整序列送入LLM
decode response                                         # 解码响应
```

图像占据了LLM文本的576个代币.在2048文本上,留下了1472个代币.在32k文本上,这是一个圆形错误.

> **【中文解读】**在2048年上下文窗口中,占据了28%,剩下1472个标志给文本;但在32k上下文中,这几乎可以忽略不计.

### 投影机准备第一阶段

结ViT.结LLM. 训练只有2层MLP. 数据集:558k图像标题对 (LAION-CC-SBU). 损失:标题上的语言建模,根据投影图像代币.

在单个时代中,在128批次中,这在几个小时内完成.投影器学习将ViT空间映射到LLM空间.没有具体任务的监督.

> **【中文解读】**第一个阶段结ViT和LLM,只训练2层MLP──用558k图文对,以语言建模损失训练──MLP学会将ViT的视觉嵌入空间映射到LLM的语义空间──单个时代、批量128 几小时即可完成──

### 视觉指令调节第二阶段

解投影机 (仍然可以训练).解LLM (通常完全,有时LoRA).训练158k视觉指导转折.

等人通过:
1. 拍一个COCO图片.
2. 提取文本描述,5个人的字幕 + 边界框列表.
3. 给GPT-4发送三个提示模板.
   - 对话 / 对话: "用户和助理之间关于这个图像的回复对话".
   - 详细描述/详细描述: "给图像的丰富,详细描述. "
   - 复杂推理: "问一个需要对图像进行推理的问题,然后回答它".
4. 解析GPT-4的输出成 (指示,响应) 对.

任何这些都直接触及图像,只有文字描述.GPT-4幻觉可信的图像内容.一些噪音,但它奏效:158万转折足以解锁对话.

> **【中文解读】**关键创新:数据生成完全不接触图像本身仅使用文本描述.GPT-4 会"幻觉"出合理的图像内容,虽然会有噪音,但158k条数据足以解锁对话能力.

>  **【困惑】**问:GPT-4 没看图只看描述,那个LLaVA 训练时实际学学的"视觉"是什么?A:LLaVA 学习是两件事:
> ️ **【易错点】**模型可能描述图中没有的东西――修复:使用GPT-4V (多模态版本) 替代纯文本GPT-4,让GPT-4V 真的看图生成描述(分享GPT4V就是这个思路),质量更高――

> **【拓展：数据合成的范式意义】**拉瓦的数据合成方法 (GPT-4 生成指令数据) 开创了VLM 数据工程的新范式――后续的 ShareGPT4V(100万高质量描述) 拉瓦的数据合成方法 (ALLaVA) 都沿着这一思路――在垂直领域 (如医疗影像,金融图),也可以使用GPT-4V 生成领域的特定指令数据来微调VLM――

### 为什么社区复制了这个为什么社区纷纷效仿

- 没有1阶段的损失,整个LM损失.
- 投影机几小时即可完成训练,而不是几天.
- 通过重新训练投影器,可以更换LLM.
- 视觉指令数据管线使用GPT-4,用于新领域的数据生成成本很低.

### 拉瓦-1.5和拉瓦-下一个.

现在,我们在车上,我们在车上着.
- 学生任务数据 (VQA、OKVQA、RefCOCO) 混入指令微调──
- 系统提示更好.
- 现在,我们在2048年开始,

现在,我们在新的一天,
- AnyRes:将高分辨率图像分为2x2或1x3的336x3网格,加上一个全局低分辨率缩略图片.每个片子产生576个代币,总共约2880个视觉代币.
- 更多的指令数据混合,加入 ShareGPT4V(高质量 GPT-4V 描述)
- 士7B,士34B. 更多强大的基础LLM

> **【拓展：AnyRes 与高分辨率理解】**对于金融场景中的报道,发票等文档图像,高分辨率理解至关重要.文字可能很小,需要放大才能正确的OCR.

### 视频

12.08课程涵盖OneVision的深度.短版本:相同的投影机,但以一个模型的单一图像,多图像和视频课程进行培训,共享视觉标志预算.

> **【中文解读】**第12.08 课程将深入讲解OneVision──简言之:使用相同的投影机,但通过课程学习覆盖单图,多图和视频三种任务,在一个模型中共享视觉代币预算──简言之:使用相同的投影机,但通过课程学习覆盖单图,多图和视频三种任务.

### 现在,我们在头上看了.

| | Q-Former (BLIP-2) | MLP (LLaVA) |
|---|---|---|
| Visual tokens per image / 每张图视觉token数 | 32 | 576 (base/基础) or 2880 (AnyRes) |
| Trainable params / 可训练参数 | 188M + LM | 40M + LM |
| Stage 1 loss / 第一阶段损失 | ITC+ITM+ITG | LM only / 仅语言建模 |
| LLM drop-in / LLM替换 | Requires retrain / 需重新训练 | Swap with minimal retrain / 几乎无需重训 |
| Multi-image / 多图像 | Awkward / 不自然 | Natural (concat) / 自然拼接 |
| Video / 视频 | Awkward / 不自然 | Natural (per-frame concat) / 逐帧拼接 |
| Token budget / Token预算 | Small / 小 | Large / 大 |

简单化和代币灵活性是MLP的胜利.Q-Former在代币预算中获胜.到2023年底,代币预算不再是约束力的约束 (LLM背景增长到32k-128k+) 而简单性占据主导地位.

> **【中文解读】**简洁性和代币灵活性上胜出,Q-Former在代币预算上胜出.但到2023年底,随着LLM上下文窗口增长到32k-128k+,代币预算不再是瓶,简洁性成为决定因素.

>  **【困惑】**学完本节还会问:1) 为什么没有LLaVA 上加Q-Former?加了复杂性变高、训练难度大、收益小(除非视频这样的标志 预算紧张场景) ――2) LLaVA-1.5 和 LLaVA-NeXT 该选哪个? 默认 LLaVA-NeXT(支持高分辨率 AnyRes,OCR 和文档任务更强) ⋅

### 提示词格式

```
A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions. USER: <image> Describe this image in detail. ASSISTANT: The image shows ...
```

`<image>`在代币化之前,它被取代为576个视觉代币 (或2880个随 AnyRes).代币化器看到比它训练的稍长一段序列,但LLM处理新输入,因为第一阶段教了它.

> **【中文解读】** `<image>`是占位符代币,在送入代币器之前将被替换为576个 (或 AnyRes模式下2880个) 视觉代币.

### 参数经济性

子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子
- 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查: 临床检查:
- 投影器: ~22M可训练 / 可训练.
- 星7B:7B
- 总计:7.3B参数. 训练可在第二阶段训练:全7B+22M投影机.

训练费用:第2阶段:在8xA100上工作20小时.这是一个节点,可重复的关键号码.

> **【中文解读】**第二阶段训练成本:8张A100 跑约20小时――这是一个关键数字一天、一台机器、可复现――这就是LLaVA能够迅速传播的原因――
```figure
mm-llava-projector
```

## 用它

## 运用它 动手实践

`code/main.py`现在,我们需要一个工具.`code/main.py`实现了:

1. 两层MLP投影器 (dim 16 → 32 → 32 玩具尺度) 在纯Python.
2. 快速构建管道:系统快速`<image>`提示词构建管线:系统提示 + 提示`<image>`替换为N个投影代币 + 用户轮次 + 助手生成占位符──
3. 视觉标志在LLM上下文中占比多少比例(2k/32k/128k窗口)

## 发射上线

这一课产生了`outputs/skill-llava-vibes-eval.md`由于LLaVA家族检查点,它运行了10个即时振动式套件 (3个字幕,3个VQA,2个推理,2个拒绝) 并报告了一个可以读取的人类的分数卡.不是基准;一个烟雾测试来确认投影机和LLM的连接良好.

> **【中文解读】**本课产出发 `outputs/skill-llava-vibes-eval.md`◎ 给定一个LLaVA系列的检查点,运行10个提示的"振动-标准"测试套件[3] 3个描述,3个VQA,2个推断,2个拒绝),产生可读的成绩单――这不是正式基准测试,而是一个烟雾测试,用于确认投影机和LLM 连接良好――

## 练习题

1. 计算2层MLP投影器的可训练参数数量`1024 → 4096 → 4096`通过GELU和偏差,它代表了LLaVA-13B的多少分?
   | 计算维度为 `1024 → 4096 → 4096` 的 2 层 MLP 投影器的可训练参数量。含 GELU 和 bias，它占 LLaVA-13B 的多少比例？

2. 构建一个"拒绝"案例的LLaVA提示图片 图片包含一个私人. 写出预期的助理反应. 为什么LLaVA应该拒绝这种零射击,以及需要什么培训数据来加强拒绝?
   | 为"拒绝"场景构建 LLaVA 提示词——图像包含私人个体。写出期望的助手回复。为什么 LLaVA 应该零样本拒绝？需要什么训练数据来强化拒绝行为？

3. 阅读LLaVA-NeXT博客的AnyRes部分.计算在AnyRes上1344x672图像的视觉代币数量.将其与336x336的基 576代币进行比较.
   | 阅读 LLaVA-NeXT 博客的 AnyRes 部分。计算 1344x672 图像在 AnyRes 下的视觉 token 数量，并与 336x336 基础设置的 576 个 token 比较。

4. 视觉指令调整 (视觉指令调整) 直接进入第二阶段,则会发生什么?
   | LLaVA 第一阶段投影器用描述文本的语言建模损失训练。如果跳过第一阶段直接进入第二阶段会怎样？引用 Prismatic VLMs 消融实验（arXiv:2402.07865）回答。

5. 对于一个新领域 (医疗X射线,卫星图像),描述四步数据管道生成域指示.每一步可能会发生什么问题?
   | LLaVA-Instruct-150k 用 GPT-4 从 COCO 描述生成指令。对于新领域（医疗X光、卫星图像），描述生成领域指令的四步数据管线。每步可能出什么问题？

## 关键词 关键词

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|----------------|------------------------|----------|---------|
| Projector | "MLP bridge" | 2-layer MLP with GELU mapping ViT dim to LLM dim | 投影器：将ViT维度映射到LLM维度的2层MLP | |
| Image token | "<image> placeholder" | Prompt marker replaced by N projected visual tokens before inference | 图像token：推理前被替换为N个投影视觉token的提示标记 | |
| Visual instruction tuning | "LLaVA stage 2" | Training on GPT-4-generated (image, instruction, response) triplets | 视觉指令微调：在GPT-4生成的（图像,指令,回复）三元组上训练 | |
| Stage 1 alignment | "Projector pretraining" | Freeze ViT and LLM, train projector with LM loss on captions | 第一阶段对齐：冻结ViT和LLM，用描述文本的LM损失训练投影器 | |
| AnyRes | "Multi-crop tiling" | Split high-res image into a tile grid and concatenate each tile's visual tokens | AnyRes：将高分辨率图像切分为网格，拼接各切片的视觉token | |
| LLaVA-Instruct | "GPT-4-generated" | 158k instruction-response pairs synthesized from COCO captions + GPT-4 | LLaVA指令数据：用COCO描述+GPT-4合成的158k指令-回复对 | |
| Vision encoder freeze | "Backbone locked" | CLIP weights do not update in stage 1, sometimes not in stage 2 either | 视觉编码器冻结：CLIP权重在阶段1不更新，有时在阶段2也不更新 | |
| ShareGPT4V | "Better captions" | 1M dense captions generated by GPT-4V, used for higher-quality alignment | 100万条GPT-4V生成的密集描述，用于更高质量的对齐 | |
| VQA | "Visual question answering" | Task of answering a free-form question about an image | 视觉问答：回答关于图像的自由形式问题 | |
| Prismatic VLMs | "Design-space paper" | Karamcheti 2024 ablation systematically testing projector and data choices | 系统测试投影器和数据选择的设计空间消融实验论文 | |

## 继续阅读 继续阅读

- [Liu et al. — Visual Instruction Tuning (arXiv:2304.08485)](https://arxiv.org/abs/2304.08485)LLAVA论文.
- [Liu et al. — Improved Baselines with Visual Instruction Tuning (arXiv:2310.03744)](https://arxiv.org/abs/2310.03744) 拉瓦-1.5.
- [Chen et al. — ShareGPT4V (arXiv:2311.12793)](https://arxiv.org/abs/2311.12793)密集标题数据集.
- [Karamcheti et al. — Prismatic VLMs (arXiv:2402.07865)](https://arxiv.org/abs/2402.07865)设计空间消融实验
- [Li et al. — LLaVA-OneVision (arXiv:2408.03326)](https://arxiv.org/abs/2408.03326)统一单图,多图,视频版本.
