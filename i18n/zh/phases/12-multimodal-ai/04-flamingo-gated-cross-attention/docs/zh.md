# 闪电和门交叉注意力与少样本视觉语言模型

> 们都在想, 它显示,一个模型可以任意处理交织的图像,视频和文本序列. 模型可以在背景下学习, 通过三个例子 (图像,字幕) 组进行几次提示, 机制:关闭的跨注意层,插入了结的LLM现有层之间,具有从零开始的学习门,因此在初始化时保留了LLM的文本能力. 这一课程讲述了弗拉明戈的感知器复制样本和关闭的交叉注意力架构,

> **【中文解读】**佛兰哥 首次实现图文交织输入和上下文少样本学习.核心是门控交叉注意力在结结LLM层间插入可学习的门控层,初始值为零以保护文本能力.

> **【拓展：Flamingo→Gemini交织输入】**弗拉明戈的图文交织处理模式是双子座交织输入和Idefics2视觉代币的原型,开创了多模态下文习的先河.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, gated cross-attention + Perceiver resampler demo) | **语言:** Python（标准库，门控交叉注意力 + Perceiver resampler 演示）
**Prerequisites:** Phase 12 · 03 (BLIP-2 Q-Former) | **前置知识:** Phase 12 · 03（BLIP-2 Q-Former）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**学本节前请先掌握:阶段12·03(BLIP-2 Q-Former,理解交叉注意力和可学习查询);阶段7(转former残差结构);阶段11·05(内文学习概念) ・Flamingo 和 BLIP-2 最大的不同:BLIP-2 在 LLM 输入端桥接一次;Flamingo 在 LLM 每隔几层插入门控制层──
>  **【类比】**佛兰哥门控交叉注意力 = "外科手术式的微创改造"――BLIP-2 = "在LLM大门口装一个翻译员"(输入端桥接一次);佛兰哥 = "在LLM的每层办公室里安装一个窗口"――每4层门控交叉注意力) ─门控初始为0 = 窗口一开始是关闭的,模型行为和原始LLM完全一样;训练慢慢开窗口 = 视觉信息逐渐注入但不会破坏原始文本能力──

## 学习目标

- 解释如何通过tanh(gate) = 0 保存结的LLM的文本能力.
  中文翻译:解释门控交叉注意力如何通过tanh(gate) = 0 在初始化时保持结 LLM的文本能力──
- 通过感知器重新样本:N图像补丁 →K通过交叉注意力固定"隐藏"查询.
  中文翻译:理感知器复制样本:N 个图像补丁 → 通过交叉注意力产生 K 个固定"潜在"查询。
- 描述弗拉明戈如何处理交织的图像文本序列,并使用因果掩饰来尊重图像的放置.
  中文翻译:描述弗拉明戈如何尊重图像位置的因果掩码处理交织的图文序列.
- 复制几次多模式提示结构 (3个图像标题示例,然后是查询图像).
  中文翻译:复现少样本多模态提示结构(3个图文示例后跟一个查询图像) 』

## 问题 问题引入

通过BLIP-2将32个视觉代币输入到一个结的LLM的输入层中. 按一个提示,可以使用一个图像. 但如果您想用文字插入 *许多*图像,如"这里是图像A,标题它;这里是图像B,标题它;现在这里是图像C,标题它"? 专业学习的自我注意力需要在单个流程中处理图像代币和文字代币,

> BLIP-2 将将 32 个视觉代币 入结 LLM 的输入层――适用于每个提示一张图像――但是如果你想入与文本交织的*多张*图像,例如"这是图像A,描述它;这是图像B,描述它;现在是图像C,描述它"?LLM的自主注意力需要在单个流中处理图像代币和文本代币,哪些位置可以关注哪些图像问题变得棘手.

弗拉明戈的答案:不要改变LLM的输入流. 插入现有LLM区间的额外的跨注意层. 文字代币仍然像往常一样流出在LLM的因果自我注意力中. 在每几个LLM块之间,文字代币通过新的封闭层来交叉访问图像功能. 门 (初始化为零) 意味着在零步骤时,新层是无运作的 随着训练的进步,门户就打开,视觉信息开始流动.

> 弗拉明戈的答案:完全不改变LLM的输入流程. 在现有LLM块之间插入额外的交叉注意力层.文本代币 像往常一样流过LLM的因果自注意力. 每隔几个LLM块,文本代币还通过新的门控层交叉关注图像特征.门控(初始化为零) 意味着第零步的新层是空操作模型行为完全像预训练的LLM.随着训练进行门控逐渐开放,视觉信息开始流入.

弗拉明戈回答了第二个问题:每提示如何处理每次图像的可变数量 (0, 1,或多个) ?一个感知器重样仪是一个小的跨注意力模块,它取出你拥有的任何数量的补丁并产生固定数量的视觉隐藏代币.无论提示中有多少图像,LLM跨注意力层都会看到相同的形状.

> 弗拉明戈回答第二个问题:如何处理每个提示中可变数量的图像 ((0、1或多张)?感知器重样器是一个小型交叉注意力模块,接收任意数量的补丁并产生固定数量的视觉潜在标志──无论提示中有多少图像,LLM交叉注意力层看到的形状都相同──

## 概念的核心概念

> **【中文解读】**门控制机制控制视觉信息的流入量,初始化时门控制值为0 (视觉信息不流入),训练过程中逐渐开放――

> **【拓展：Flamingo 的高效适配】**弗拉明戈 仅训练约1%的参数 (门控交叉注意力层),就能在少数拍摄的视觉推理任务上达到SOTA.


> **【拓展：门控机制的数学原理】**门控交叉注意力门控值初始化为0,意味着训练开始时视觉信息完全不流入LLM――随着训练进行,门控逐渐开放――这防止了训练初始视觉噪音干扰LLM的语言能力――这种零初始化门控技巧后来被LLaVA等模型借鉴用于投影层――


### 结的法定律师

弗拉明戈开始了冷的辛奇拉70B法师.所有70B重量都没有被触及.现有的文字自我注意和FFN正常运行.

> 现在,我们已经开始了这项计划,

### 感知器重新样本

对于每一个提示图像,ViT生成N补丁代币.感知器复样器有K固定可学习的隐藏 (Flamingo使用K=64).每一个复样器块是两个子步骤:

> 对于提示中的每张图像,ViT 产生N 个补丁符号――感知器复制器有K 个固定的可学习潜在向量――Flamingo 使用K=64)――每个复制器块有两个步骤:

>  **【困惑】**问:感知器复制器 和BLIP-2的Q-Former有什么区别?A: 思想几乎一样(从补丁中提取信息的可学习查询),但Flamingo的感知器复制器只做视觉特征压缩、不参与比损失训练;Q-Former是变压器 结构且有ITC/ITM/ITG 三个损失──可以认为感知器复制器是Q-Former的简化版──

1. 交叉注意:K潜伏对N补丁代币 (Q来自潜伏,K/V来自补丁) 进行.
   中文翻译:交叉注意力:K 个潜在向量关注 N 个补丁代币(Q 来自潜在向量,K/V 来自补丁) 』
2. 自我注意力+FFN在隐藏中.
   中文翻译:潜在向量内部的自注意力 + FFN。

输出后6个复制模块,输出为K=64的视觉代币,无论ViT产生了多少补丁. 224x224图像 (196补丁) 和480x480图像 (900补丁) 都作为64个复制模块代币.

> 经过6个复制器块后,输出是K=64个维度为1024个视觉代币,无论VIT产生多少补丁.

视频的重样仪是时间应用的:每个框架的补丁产生64个隐藏,时间定位编码使模型能够区分t=0和t=N.完整的视频成为T * 64视觉代币.

> 对于视频,样本按时间维度应用:每的补丁 产生64个潜在向量,时间位置编码让模型区分 t=0 和 t=N──完整视频变成T * 64个视频代币──

### 门的跨度注意力

在结的LLM的每一个M层之间 (Flamingo使用M=4),插入一个新的关闭的跨注意区块:

> 在结尾LLM的每层之间(Flamingo使用M=4),插入一个新的门控交叉注意力块:

```
x_after_llm_block = llm_block(x_before)
cross = cross_attn(x_after, resampler_output)
gated = tanh(alpha) * cross + x_after
x_before_next_block = gated
```

- `alpha`它们是可学习的,以零为初始的.
  翻译: 中文`alpha`是一个可学习的标志量,初始化为零.
- `tanh(0) = 0`关闭分支的贡献为零.
  翻译: 中文`tanh(0) = 0`开始时分支贡献为零.
- 作为`alpha`随着移动从零, 跨注意力贡献的增长顺利.
  中文翻译:随着`alpha`远离零,交叉注意力贡献平滑增长――
- 剩余连接意味着即使一个完全开放的门也不会覆盖LLM的文本表示;它只是在上面添加视觉信息.
  中文翻译:残差连接意味着即使门门完全开放,也不会覆盖LLM的文本表示;它只是在上面添加视觉信息.

这是一个最重要的设计选择:视觉调节是加值,关闭,在初始化时是零.一个步骤0的Flamingo是完美的文本输入的Chinchilla 70B.

> 这是弗拉明戈中最重要的设计选择:视觉条件是可加的,门控的,初始化为零.

> ️ **【易错点】**原因:未训练的交叉注意力输出是噪音,混入了LLM 内部表示会破坏文本知识──修复:alpha 必须初始化为0,让模型从"完美LLM"出发,缓慢学习──
>  **【类比】**零初始化门控 = "新员工进入职模式"――新员工 (视觉层) 第一周只观察、不说话(门=0);熟悉业务后逐渐发言(门慢慢开) ――直接让新员工主导决策(门≠0初始化) 会扰乱团队原奏(破坏LLM文本能力) ――

### 面具的交叉注意力,用于交叉输入

在"<图片A>标签A <图片B>标签B <图片C> ?"这样的提示中,每个文本标签只应该看到序列中之前的图像.`t`仅使用图像复样符号,其图像指数`i < i_t`在哪里`i_t`是位置前最新的图像`t`"只看到最后一个前面的图像"或"看到所有前面的图像"都是有效的选择;

> 在类似"<图像A> 描述A <图像B> 描述B <图像C> ?"的提示中,每个文本标志只应看到序列中位于之前的图像――交叉注意力掩码强制:位置`t`仅关注图像索引`i < i_t`图像复样符号,其中`i_t`是位置`t`之前最近的图像"",只看最近的图像"或"看所有之前的图像"都是有效的选择;弗拉明戈选择了前者──

### 在环境中学习

弗拉明戈的提示看起来像:

> 弗拉明戈提示看起来像这样:

```
<image1> A photo of a cat. <image2> A photo of a dog. <image3> A photo of a
```

模型看到完成模式并输出"鸟" (或图像3显示的任何东西).没有梯度步骤.冷的LLM的文本内学习能力通过关闭的交叉注意力.

> 模型看补全模式并输出"鸟" (或图片3 显示任何内容) 无需梯度步骤.

>  **【困惑】**问:为什么弗拉明戈能在背景下学习而BLIP-2 不能?A:弗拉明戈在LLM 每隔4层注入视觉信息,LLM内部的视觉信息学习(在阶段11·05学习过) 仍然完整工作;BLIP-2 将32个视觉代币直接拼到即时前面,LLM将它们作为普通代币处理,但训练目标没有明显的几次拍摄模式,所以能力弱――

### 培训数据

弗拉明戈训练了三个数据集:

> 佛兰哥在三个数据集上训练:

1. 多模 MassiveWeb (M3W): 43万页面的图像和文本交织在一起,重建阅读顺序.
   中文翻译:多模态大规模网页 (M3W) 4300万包含交织图像和文本的网页,重建阅读顺序.
2. 图像-文本对 (ALIGN + LTIP):4.4B对.
   中文翻译:图文对(ALIGN + LTIP):44亿对──
3. 视频文本对 (VTP):27M短视频片段.
   中文翻译:视频文本对(VTP):27亿个短视频片段.

欧贝利克斯 (2023) 是互联网体的开放复制,Idefics,Idefics2和大多数开放的"像弗拉明戈"模型都在训练中.

> 们的们在们的们中,

### 开放和

开放Flamingo (2023) 是开放的复制. 架构相同 (感知器重新样本 + 结LLaMA或MPT上的门横向注意力). 3B,4B,9B的检查点.由于LLM的基础较小,数据较少,质量落后于Flamingo.

> 开放复现――架构相同――感知器复样器+ 结 LLaMA 或 MPT 上的门控交叉注意力)―3B、4B、9B 检查点――由于基础LLM 更小和数据更少,质量落后于 Flamingo──

Otter (2023) 基于OpenFlamingo,并调整了MIMIC-IT (多模式指令的数据集) 的指令,显示了关闭的跨重视功能,也用于指令后续.

> 通过MIMIC-IT (MIMIC-IT) 进行微调指令,证明门控交叉注意力也适用于遵循指令.

### 后代

- 爱德艺2 / 爱德艺3:拥抱面的关闭跨度注意力谱系,逐渐变得更简单 (爱德艺2放弃了重新样本,以适应性聚合的直接补丁代币为好).
  中文翻译:Idefics / Idefics2 / Idefics3:Hugging Face 的门控交叉注意力谱系,逐步简化(Idefics2 去掉了样本,改用自适应池化的直接补丁代币) 』
- 弗拉明戈到卡梅伦过渡:到2024年,许多团队转向早期融合 (课 12.11);在需要脊椎结结的生产中,弗拉明戈风格的门口交叉注意力仍然存在.
  中文翻译:弗拉明戈到马龙的过渡:到2024年,许多团队转向早期融合 (第 12.11 课);弗拉明戈风格的门控交叉注意力在需要结结主干网络的场景仍然在生产中使用.
- 双子座的交叉输入:概念上继承了弗拉明戈的交叉格式灵活性,尽管确切的机制是专有的.
  中文翻译:Gemini的交织输入:概念上继承了弗拉门戈的交织形式灵活性,尽管具体机制是专有的.

### 与BLIP-2的比较

| | BLIP-2 | Flamingo |
|---|---|---|
| / | BLIP-2 | Flamingo |
| Visual bridge | Q-Former once at input | Gated cross-attention at every M layers |
| 视觉桥接 | 输入层一次 Q-Former | 每 M 层一次门控交叉注意力 |
| Visual tokens | 32 per image | 64 per image per cross-attn layer |
| 视觉 token | 每图 32 个 | 每个交叉注意力层每图 64 个 |
| Frozen LLM | Yes | Yes |
| 冻结 LLM | 是 | 是 |
| Few-shot in-context | Weak | Strong — the paper's centerpiece |
| 少样本上下文学习 | 弱 | 强——论文的核心亮点 |
| Interleaved inputs | No native support | Yes, the design target |
| 交织输入 | 无原生支持 | 是，设计目标 |
| Training data | 130M pairs | 1.3B pairs + 43M interleaved pages |
| 训练数据 | 1.3 亿对 | 13 亿对 + 4300 万交织网页 |
| Parameter count | 188M trained | ~10B trained (cross-attn layers) |
| 参数量 | 训练 1.88 亿 | 训练约 100 亿（交叉注意力层） |
| Compute | Days on 8 A100s | Weeks on thousands of TPUv4 |
| 计算量 | 8 块 A100 数天 | 数千块 TPUv4 数周 |

选择BLIP-2以供单图像VQA在预算中,选择Flamingo/Idefics2以供交叉,少拍或多图像推理.

> 预算有限的单图像VQA 选择BLIP-2――交织、少样本或多图像推理选 Flamingo/Idefics2――

## 用它实现框架
```figure
cross-attention-fusion
```

## 用它

`code/main.py`证明:

> `code/main.py`演示了:

1. 通过36,假的补丁代币和8个可学习的隐藏符号 (纯的Python交叉注意力)
   中文翻译:对36个假补丁代币的感知器复制样本,使用8个可学习潜在向量(纯Python 交叉注意力) 』
2. 通过一个关闭的跨度注意力步骤`alpha = 0`→输出等于输入 (LLM未变),然后`alpha = 2.0`视觉贡献混合.
   中文翻译:门控交叉注意力步骤,`alpha = 0`→ 输出等于输入 (LLM 不变),然后`alpha = 2.0`视觉贡献混入
3. 制作2D注意力面具的"图像1 (文本1) (图像2) (文本2) "序列.
   中文翻译:交织掩码构建器,为"(图像 1) (文本 1) (图像 2) (文本 2)"序列生成2D注意力掩码。

## 运送它.

这一课产生了`outputs/skill-gated-bridge-diagnostic.md`鉴于开放的VLM配置 (模拟器Y/N,跨接频率,门口方案),它识别了弗拉明戈系的元素并解释了结结策略.有用的调整为什么细调降低了文本性能 (答案:门口变得太宽太快).

> 本课产出发 `outputs/skill-gated-bridge-diagnostic.md`△给定开放VLM的配置 (是否有复制器,交叉注意力频率,门控方案),它识别了弗拉明戈血统元素并解释了结论策略.

## 练习题

1. 计算Flamingo-9B的视觉参数数:9B LLM + 1.4B 关闭横跨注意力层 + 64M 复样仪.
   中文翻译:计算 Flamingo-9B 的视觉参数:9B LLM + 14亿门控交叉注意力层 + 6400万复制器――训练参数占总参数的比例是多少?

2. 执行封闭的残留物`y = tanh(alpha) * cross + x`在 PyTorch 中,实验证明`alpha=0`现在`y==x`现在就在初步.
   中文翻译:用PyTorch实现门控残差`y = tanh(alpha) * cross + x`△实验证`alpha=0`时 时间`y==x`精确成立.

3. 阅读OpenFlamingo第3.2节 (arXiv:2308.01390) 关于当每个提示具有不同的图像数量时,他们如何处理多个图像.描述填充策略.
   中文翻译:阅读OpenFlamingo 第3.2节(arXiv:2308.01390) 关于如何处理批次中每个提示图像数量不同的情况――描述填充策略――

4. 弗拉明戈的跨度注意力面具为什么允许一个文本标志只关注*最最近的*前面图像而不是所有前面图像?
   中文翻译:为什么弗拉明戈的交叉注意力掩码让文本代币只关注*最近*前一张图像而不是所有前序图像?阅读弗拉明戈论文第 2.4 节并解释权衡──

5. 在文本中,构建一个提示,为新的Flamingo变体构建4个"图像 →主对象颜色"的例子.随着您将示例数从0到8变化,描述预期的精确性模式.
   中文翻译:上下文少样本:构建包含4个"图像 → 主要对象颜色"示例的提示――描述示例数量从0 变到8 时预期的准确率模式――

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Perceiver resampler | "Fixed-latent cross-attention" | Module that produces K fixed tokens from a variable number of input patches | 从可变数量输入 patch 产生 K 个固定 token 的模块 |
| Gated cross-attention | "Tanh-gated bridge" | Residual layer `y = tanh(alpha)*cross + x`, learnable alpha, init 0 | 残差层 `y = tanh(alpha)*cross + x`，可学习 alpha，初始化为 0 |
| Interleaved input | "Mixed sequence" | Prompt format with images and text mixed freely in reading order | 图像和文本按阅读顺序自由混合的提示格式 |
| Frozen LLM | "No LLM gradients" | The text LLM's weights do not update; only resampler + cross-attn layers train | 文本 LLM 权重不更新；仅 resampler + 交叉注意力层训练 |
| Few-shot | "In-context examples" | Give a few (image, answer) pairs in the prompt; model generalizes without finetuning | 在提示中给几个（图像，答案）对；模型无需微调即可泛化 |
| OBELICS | "Interleaved web corpus" | Open dataset of 141M web pages with images and text in reading order | 1.41 亿网页的开放数据集，包含按阅读顺序排列的图像和文本 |
| Chinchilla | "70B frozen base" | Flamingo's frozen text LLM, from DeepMind's Chinchilla paper | Flamingo 的冻结文本 LLM，来自 DeepMind 的 Chinchilla 论文 |
| Gate schedule | "How alpha moves" | The rate at which the cross-attention gate opens during training | 训练过程中交叉注意力门控打开的速率 |
| Cross-attn frequency | "Every M layers" | How often a gated cross-attention block is inserted; Flamingo uses M=4 | 门控交叉注意力块插入的频率；Flamingo 使用 M=4 |
| OpenFlamingo | "Open reproduction" | MosaicML/LAION open checkpoint at 3-9B; architecture-identical to Flamingo | MosaicML/LAION 的 3-9B 开放检查点；架构与 Flamingo 相同 |

## 继续阅读 继续阅读

- [Alayrac et al. — Flamingo (arXiv:2204.14198)](https://arxiv.org/abs/2204.14198)原始的纸.
  中文翻译:弗拉明戈 原始论文──
- [Awadalla et al. — OpenFlamingo (arXiv:2308.01390)](https://arxiv.org/abs/2308.01390)开放繁殖.
  中文翻译:开放复现――
- [Laurençon et al. — OBELICS (arXiv:2306.16527)](https://arxiv.org/abs/2306.16527) 互联网体.
  中文翻译:交织网络语料库.
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795)一般的感知器架构.
  中文翻译:通用感知器架构──
- [Li et al. — Otter (arXiv:2305.03726)](https://arxiv.org/abs/2305.03726) 调节指令的弗拉明戈后裔.
  中文翻译:指令微调的弗拉明戈后代.
- [Laurençon et al. — Idefics2 (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246)现代化简化弗拉明戈方法.
  中文翻译:弗拉门戈方法的现代化简化.
