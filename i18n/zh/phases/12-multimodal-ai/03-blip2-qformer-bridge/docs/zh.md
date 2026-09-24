# 从Clip到Blip-2 Q-Former作为模拟桥梁.

> CLIP将图像和文字相对应,但不能生成标题,回答问题,或进行对话. 通过跨度注意力来通过结结结 ViT 的特征,然后直接插入结结 LLM 的输入流中, 188万个桥梁参数将11B LLM连接到ViT-g/14. 到2026年,每一个基于适配器的VLM都是 MiniGPT-4,InstructBLIP,LLaVA的表弟都是后代. 这一课程阅读了Q-Former的架构,解释了它的两阶段训练,

> **【中文解读】**通过交叉注意力桥接结结 ViT 和 LLM,仅188M参数就能将视觉特征注入11B的语言模型.

> **【拓展：Q-Former→多模态架构演进】**问:前是"结视觉编码器+结LLM+轻量桥接"范式的创始人,MiniGPT-4、InstructBLIP、LLaVA 都是其思想的后代──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, cross-attention + learnable-query demo) | **语言:** Python（标准库，交叉注意力 + 可学习查询演示）
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 7 (Transformers) | **前置知识:** Phase 12 · 02（CLIP），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**学本节前请先掌握:阶段12·02(CLIP对比学习);阶段7(转换器自注意力和交叉注意力);阶段11·04(嵌入式) ――核心数学是交叉注意力 Q·K^T·V──
>  **【类比】**问:前面,每个人提问自己,听完回答后写下32条新闻摘要.

## 学习目标

- 解释为什么冷视觉编码器和冷的LLM之间的可训练的瓶比成本和稳定性更好.
  中文翻译:解释为什么在结视觉编码器和结 LLM 之间可训练瓶在成本和稳定性上优于端到端微调.
- 实现一个跨重视区块,其中一个固定的学习性查询集处理外部图像特征.
  中文翻译:实现一个交叉注意力块,其中一组固定的可学习查询关注外部图像特征──
- 通过BLIP-2的两阶段预训练:表示 (ITC + ITM + ITG) 然后生成 (通过冷解码器损失LM).
  中文翻译:理 BLIP-2 的两阶段预训:表示学习(ITC + ITM + ITG) 然后生成学习(结解码器的LM 损失) 』
- 比较Q-Former与LLaVA中使用的简单的MLP投影机,并讨论当每一个选择赢得时.
  中文翻译:比较Q-Former 和 LLaVA 使用的更简单的MLP投影器,论证各自的优势场景.

## 问题 问题引入

你有一个冷的ViT,每张图片产生256个补丁代币,每张图片均为14080.你有一个冷的7B LLM,预计将4096的代币嵌入.明显的桥梁从1408到4096 的线性层工作,但将所有256个补丁代币输入到LLM的文本中,每张图片每张代币额外256个.超过32个图像的批量仅仅是视觉模式消耗的8192个代币.

> 你有一个结结的 ViT,每张图像产生 256 个维度为 1408 个补丁符号.你有一个结结的 7B LLM,预期维度为 4096 个符号.嵌入.显然可行的桥梁从 1408 到 4096 线性层,但将所有 256 个补丁符号入 LLM 上下文需要每张图像额外消耗 256 个符号.

问:你可以将256个代币的图像表示压缩到更少的代币 (例如32个代币),同时保留足够的信息,让LLM能够标题,回答问题,并解释图像?

> BLIP-2的问题:你能否将256个代币的图像表示缩小到远低于32个代币,同时保留足够的信息让LLM进行图像描述,回答问题和推理?

答案:一个Q-Former. 32个可学习的"查询"向量,它们交叉地处理VIT的补丁代码,产生了LLM所消耗的32代代码视觉总结.总共188万个参数.在触及LLM之前,训练有素进行对比,匹配和生成目标.

> 答案是:Q-Former──32个可学习的"查询"量通过交叉关注 ViT的补丁代币,产生LLM 消费的32个代币 视觉摘要──总共188M参数──在接触LLM 之前使用比较、匹配和生成目标进行训练──

## 概念的核心概念

> **【中文解读】**BLIP-2 引入Q-Former 作为结视觉编码器和结 LLM 之间的轻量桥接层――Q-Former 使用一组可学习的查询代币 从视觉编码器提取与文本最相关的视觉特征,大幅减少了训练参数量(仅训练Q-Former),实现了高效的视觉语言对齐――

> **【拓展：BLIP-2 的高效训练】**----的设计影响了后续的LLaVA、InternVL等模型──销售力的BLIP-2在VQAv2上达到82.2%准确率,接近当时的最佳水平──


> **【拓展：Q-Former 的影响】**-Former的设计思想 (使用可学习查询从编码器提取任务相关特征) 得到广泛的借鉴. -Former的轻量性 (仅约188M参数) 使在消费级GPU上训练多模态模型成为可能.


### 需要学习的问题

模具的核心技巧:而不是让LLM的文字代币关注图像补丁,`Q`查询是模型的参数,它们是在训练中学习,并且用于每个图像的相同32个查询.

> 问:前任的核心技巧:不要让LLM的文本代币关注图像补丁,而是引入一组新的32个可学习查询向量`Q`让它们关注图像补丁. 查询是模型的参数.

> ️ **【易错点】**它们学习"如何从图片中提取32种信息维度" (例如颜色,物体,空间关系) ⋅每张图片通过Q-Former都输出相同的32维结构.
>  **【困惑】**答: 32个查询 如何知道每个该看什么?A: 训练时三个损失(ITC/ITM/ITG) 将反向传播梯度告诉每个查询 该专精什么;;最终学到的 32 维编码是"损失下降最快的方向",不是为人所指定的"颜色/物体/背景"――

经过交叉关注,每个查询都包含了图像的压缩总结"描述主对象","描述背景","数对象",等.查询不真正专注于语义标签;它们学习任何编码导致下游损失下降.

> 交叉注意力后,每个查询都包含图像的缩写摘要"描述主要对象"",描述背景"",计算对象数量"等.查询并非字面专注于语义标签;它们学习使下游损失下降的编码.

### 建筑

形器是一个小型变压器 (12层,大约100M参数),具有两个路径:

> 问:前者是小型变压器 (大约12层,大约100M参数),有两条路径:

1. 查询路径:32个查询向量通过自我注意 (彼此),然后通过冷的ViT补丁代币进行交叉注意,然后FFN.
   中文翻译:查询路径:32 个查询量流过自注意力(彼此之间),然后对结结 ViT 的补丁代币做交叉注意力,最后是FFN。
2. 文本路径:一个类似BERT的文本编码器与查询路径共享自注意和FFN权重.文本路径被禁用交叉注意.
   中文翻译:文本路径:类BERT的文本编码器与查询路径共享自注意力和FFN权重――文本路径禁用交叉注意力――

在训练时间,两个路径都运行.查询和文本通过共享自我注意力相互作用,这意味着查询可以对需要它的工作 (ITM,ITG) 进行文本条件.在VLM交付的推断时间,只有查询流过,产生32个视觉代币.

> 训练时两条路径同时运行――查询和文本通过共享的自注意交互,这意味着查询可以在需要文本的任务中进行.

### 两阶段的培训

双重飞行器-2预训练有两阶段:

> 预训练:

阶段1:代表性学习 (没有法学士).
- 图像与文本对比:集成查询代币和文本CLS代币之间的CLIP式对比.
  中文翻译:ITC(图文对比):池化查询代币与文本 CLS代币之间的类型 CLIP对比损失.
- 图像和文本匹配:二进制分类器 是不是图像和文本对相匹配?硬负采矿.
  中文翻译:ITM(图文匹配):二分类器这个图文对是否匹配?使用难负例挖掘。
- 图像基文本生成:因果性LM对文本进行标记,根据查询进行条件. 要求查询编码可生成文本的内容.
  中文翻译:ITG(图像条件文本生成):文本上的因果 LM 头,以查询为条件――强制查询编码可生成文本内容――

>  **【类比】**三损失的分工:ITC = "看图找文字"(粗粒度对齐);ITM = "判断图文是不是真的配"(细粒度区分);ITG = "看图把应对文字写出来"(生成能力)──三一起训练,让查询学到既能检查又能描述的视觉摘要──

只有Q-Former列车,ViT被结,没有LLM涉及.

> 仅训练Q-Former──ViT 结──不涉及LLM──

阶段2:生成学习. 附加一个结的LLM (OPT-2.7B或Flan-T5-XL,等).通过一个小的线性层将32个查询输出投影到LLM的嵌入式. 准备它们进入文本提示. 仅训练线性投影和Q-Former在LC损失上连接提示 +图像 +标题序列.

> 第二阶段:生成学习――连接一个结尾的LLM(OPT-2.7B 或Flan-T5-XL等) 通过一个小的线性层将将 32 个查询输出投影到LLM的嵌入维度――将它们置于文本提示――仅在线性投影和Q-Former 上练拼接的提示 + 图像 + 描述序列的LM 损失――

在第二阶段之后,Q-Former+投影是完整的视觉适配器.在推断时:图像 → ViT → Q-Former →线性项目 →预pendium → text → frozen LLM 发出.

> 第二阶段后,Q-Former + 投影就是完整的视觉适配器──推理时:图像 → ViT → Q-Former → 线性投影 → 前置到文本 → 结 LLM 生成输出──

### 参数经济学

造型 (B-Former) 总数为8B,训练有素188M.仅Q-Former为全堆参数的2.4% .训练成本反映了这一点:几天在少数A100s上与周为端到端.

> 结) + OPT-6.7B(67亿,结) + Q-前者(1.88亿,训练) = 共80亿,训练1.88亿,训练1.88亿──Q-前者 仅占全参数约2.4%──训练成本反映这一点:少量A100 上数天vs端到端数周──

质量:BLIP-2与Flamingo-80B相匹配或超过零射击VQA,同时小50倍.

> 质量:BLIP-2 在零样本 VQA 上匹配或超越 Flamingo-80B,同时小了50倍.

### 导航BLIP和指令知情的Q-Former

导读BLIP (2023) 通过一个额外的输入:指令文本本身,扩展了Q-Former.在交叉注意力时间,查询现在可以访问图像补丁和指令.查询可以专业化每条指令 ("数车","描述情绪") 而不是学习单个固定总结.基准在完成任务上获益.

> 通过额外输入扩展了Q-Former:指令文本本身. 在交叉注意力时,查询可以同时访问图像补丁和指令.查询可以按指令专精化.

### 迷你GPT-4和仅用投影仪的方法

迷你GPT-4 保留了Q-Former,但仅训练出口线性投影,同时结了其他一切.便宜,但成本是质量.

> 迷你GPT-4保留了Q-Former,但仅训练输出线性投影,结结其他一切――便宜,但价格是质量查询是BLIP-2,不是你的――适合快速代,不是最佳架构――

### 为什么LLaVA变得更简单

拉瓦 (2023,课时12.05) 取代了Q-Former,用一个简单的2层MLP,将每个ViT补丁代币投射到LLM空间中. 压缩更糟,但让法师参加了原始补丁. 当时这是有争议的;到2023年底,它是主导的,因为视觉指导数据 (LLaVA-Instruct-150k) 证明MLP可以训练来保存足够的信号. 交易:LLaVA的背景更快地填充,但它自然可以扩展到多个图像和视频.

> 拉瓦 (LLVA) 通过简单的2层MLP替换了Q-Former,将每个VIT补丁代币投影到LLM空间24x24 网格下每张图像 576个代币,全部给LLM. 压缩更差,但让LLM可以关注原始补丁.当时,这有争议;到2023年底,它已经成为主流,因为视觉指令数据(LLaVA-Instruct-150k) 证明MLP可以训练以保留足够的信号.权衡是:LLaVA的下文更快地填充,但它自然扩大多个图像和视频.

>  **【困惑】**学完本节还会问:Q-Former vs LLaVA MLP 该选哪个? 短上下文 + 高质量 → Q-Former(压缩32个代币 精心训练);长上下文 + 多图/视频 → LLaVA MLP(每代币 信息量大但灵活) ⋅2026年大多数VLM使用MLP,因为视觉指令数据充足,MLP 学到的足够好而且更容易扩展──

到2026年,该领域的分化:Q-Former在代币预算重要的地方存活下来 (长视频,许多图像);MLP投影器在每代币原质量优先考虑的地方占主导地位.

> 到2026年,领域分化:Q-Former 在代币预算重要时;;长视频、多图像) 生存;MLP投影器在每个代币的原质量优先占主导地位.

### 门的跨越注意力:弗拉明戈,祖先

弗拉明戈 (课 12.04) 在BLIP-2之前使用了相同的跨注意力想法,但在每个结的LLM层上,不是单一的桥梁.BLIP-2显示你可以只压缩到输入层,仍然工作.双胞胎和Idefics结合了两者:交叉输入代币加上可选的门式跨注意力在文本中的几次拍摄.

> 佛兰哥 (第 12.04 课) 在BLIP-2之前,使用相同的交叉注意力思想,但在每个结尾的LLM层,而不是单一桥接――BLIP-2证明只能缩小到输入层仍然有效――Gemini 和 Idefics 结合两者:交错输入代币加上可选的门控交叉注意力用于下文少样本――

### 2026年的后代

- 问:前者:BLIP-2,InstructBLIP,MiniGPT-4,以及大多数视频语言模型,
  中文翻译:Q-Former:BLIP-2、InstructBLIP、MiniGPT-4,以及大多数视频语言模型 (因为标志 预算原因) .
- 感知器重样:弗拉明戈变体 (课 12.04);Idefics家族,,OmniMAE.
  中文翻译:感知器重样:Flamingo 的变体 ((第 12.04 课);Idefics 系列、鷹、OmniMAE。
- 光器:LLaVA,LLaVA-NeXT,LLaVA-OneVision,Cambrian-1.
  中文翻译:MLP 投影器:LLaVA、LLaVA-NeXT、LLaVA-OneVision、Cambrian-1──
- 警池:维拉,帕利盖玛.
  中文翻译:注意力池化:VILA、PaliGemma。

重要的问题是,你是否受到代币预算或质量限制.

> 决策问题是你的约束是代币 预算还是每个代币的质量.

## 用它实现框架
```figure
modality-projection
```

## 用它

`code/main.py`建立一个像Q-Former这样的交叉注意力:

> `code/main.py`构建一个标准库 Q-Former 风格的交叉注意力:

1. 模拟 256 个图像补丁代币 (dim 128).
   中文翻译:模拟 256 个图像补丁符号 ((维度 128) 』
2. 立即完成32个可学习的查询 (第128个).
   中文翻译:实例化 32个可学习查询
3. 运行分点-产品跨度关注 (查询中的Q,补丁中的K/V).
   中文翻译:运行缩放点积交叉注意力
4. 通过线性层进行LLMdim (512) 项目.
   中文翻译:通过线性层投影到 LLM 维度 ((512) 〕
5. 输出32个准备好LLM的视觉代币.
   中文翻译:输出32个 LLM 就绪的视觉标志.

算法是纯 Python (嵌在向量上循环).玩具但正确的形状.注意力重量矩阵打印,这样你可以看到每个查询从哪个补丁中拉出来.

> 所有数学运算使用纯Python () 量嵌套循环) 玩具级但形状正确印注意力权重矩阵,你可以看到每个查询从哪些补丁 提取信息

## 运送它.

这一课产生了`outputs/skill-modality-bridge-picker.md`鉴于目标VLM配置 (视觉编码器代币数量,LLM环境预算,部署限制,质量目标),它建议为每个桥梁提供简短的理由和参数数数量估计的Q-Former vs MLP vs Perceiver重样样本.

> 本课产出发 `outputs/skill-modality-bridge-picker.md`△给定目标 VLM 配置(视觉编码器代币 数、LLM 上下文预算、部署约束、质量目标),它推了Q-Former vs MLP vs Perceiver 样本,附简短理由和每个桥接层的参数估算──

## 练习题

1. 执行PyTorch中跨注意力区块. 检查32个查询和256个键/值,注意力重量矩阵为32 x 256 ,每行总和在 softmax之后为1.
   中文翻译:用 PyTorch 实现交叉注意力块──验证 32个查询和 256个关键/值,注意力权重矩阵为 32 x 256,每行软最大 后和为 1──

2. 在BLIP-2阶段1中,Q-Former同时运行三个输失:ITC,ITM,ITG.用伪代码写出每个人的前进签名.哪个需要文字编码器路径才能活跃?
   中文翻译:在BLIP-2第一阶段,Q-Former同时运行三损失:ITC、ITM、ITG──用伪代码写出每个前向签名──哪个需要文本编码器路径激活?

3. 比较参数数:Q-Former (12层,隐藏 768层) 与2层MLP投影机 (1408 → 4096,两个层).在什么LLM规模上,188MQ-Former成本回报了训练效率?
   中文翻译:比较参数:Q-Former(12层,768 隐藏维度)vs2层 MLP投影器(1408 → 4096,两层) ⋅在什么 LLM 规模下,188M 的Q-Former 成本在训练效率超过本?

4. 阅读BLIP-2论文 (arXiv:2301.12597) 的3.2节,说明Q-Former如何初始化.解释为什么从BERT-base初始化 (非随机) 加速了融合.
   中文翻译:阅读BLIP-2论文(arXiv:2301.12597) 第3.2节关于Q-Former初始化的部分──解释为什么从BERT-(基础非随机)初始化加速收收──

5. 对于一个10分钟的视频,以1FPS样本为60个,计算每代币成本在 (Q-Former → 32代币/) vs (MLP投影器 → 576代币/).哪个适合一个128k代币的LLM文本窗口?
   中文翻译:对于10分钟视频以1FPS采样为60,计算每代币 成本:(Q-Former → 32代币/)vs(MLP 投影器 → 576代币/) ――哪个可以放进128k代币的LLM 上下文窗口?

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Q-Former | "Querying transformer" | Small transformer with 32 learnable query vectors that cross-attend to frozen ViT features | 带有 32 个可学习查询向量的小型 Transformer，交叉关注冻结的 ViT 特征 |
| Learnable queries | "Soft prompt for vision" | A fixed set of parameters that serve as the query side of cross-attention; learned per model, shared across all inputs | 作为交叉注意力查询侧的固定参数集；按模型学习，所有输入共享 |
| Cross-attention | "Q from here, K/V from there" | Attention where query, key, and value come from different sources; how the queries pull from ViT patches | 查询、键和值来自不同来源的注意力；查询如何从 ViT patch 提取信息 |
| ITC | "Image-text contrastive" | CLIP-style loss applied to Q-Former pooled queries vs text CLS | 应用于 Q-Former 池化查询与文本 CLS 的类 CLIP 对比损失 |
| ITM | "Image-text matching" | Binary classifier on hard-negative-mined pairs; forces the queries to discriminate fine-grained mismatches | 难负例挖掘对上的二分类器；强制查询区分细粒度不匹配 |
| ITG | "Image-grounded text generation" | Causal LM loss where text is generated conditioned on queries; forces queries to encode text-decodable content | 以查询为条件生成文本的因果 LM 损失；强制查询编码可解码为文本的内容 |
| Two-stage pretraining | "Representation then generative" | Stage 1 trains Q-Former alone (ITC/ITM/ITG); Stage 2 attaches frozen LLM and trains only the projection + Q-Former | 第一阶段仅训练 Q-Former；第二阶段连接冻结 LLM，仅训练投影 + Q-Former |
| Frozen backbone | "Do not finetune" | The vision encoder and LLM weights are fixed; only the bridge trains | 视觉编码器和 LLM 权重固定；仅训练桥接层 |
| Projection head | "Linear to LLM dim" | Final linear layer mapping Q-Former output to the LLM's embedding dimension | 将 Q-Former 输出映射到 LLM 嵌入维度的最终线性层 |
| Perceiver resampler | "Flamingo's version" | Similar learnable-query cross-attention, used by Flamingo at every layer rather than as a single bridge | 类似的可学习查询交叉注意力，Flamingo 在每层使用而非单一桥接 |

## 继续阅读 继续阅读

- [Li et al. — BLIP-2 (arXiv:2301.12597)](https://arxiv.org/abs/2301.12597)核心纸
  中文翻译:BLIP-2 核心论文──
- [Li et al. — BLIP (arXiv:2201.12086)](https://arxiv.org/abs/2201.12086)前任与ITC/ITM/ITG三重组.
  中文翻译:前作,包含ITC/ITM/ITG 三联损失──
- [Li et al. — ALBEF (arXiv:2107.07651)](https://arxiv.org/abs/2107.07651)"前配线" 第一阶段训练的概念祖先.
  中文翻译:"先对齐再融合"第一阶段训练的概念先驱──
- [Dai et al. — InstructBLIP (arXiv:2305.06500)](https://arxiv.org/abs/2305.06500)          
  中文翻译:指令感知的Q-Former。
- [Zhu et al. — MiniGPT-4 (arXiv:2304.10592)](https://arxiv.org/abs/2304.10592)仅使用投影仪的方法.
  中文翻译:仅投影器方案.
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795)学习性-查询性交叉注意力的一般架构.
  中文翻译:可学习查询交叉注意力的一般架构──
