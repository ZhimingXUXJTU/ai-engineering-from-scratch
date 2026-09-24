# 在LLM中偏见和代表性损害

> 卡莱戈斯,罗西,巴罗,坦吉姆,金,德恩科特,尤,张,阿赫迈德 (计算语言学2024年, arXiv:2309.00770). 根据2024年基础调查,分辨代表性损害 (刻板印象,删除) 与分配性损害 (资源分配不平等) 并将评估指标归类为嵌入式,基于概率或基于生成的文本. 2024-2025 经验: An et al. (PNAS Nexus,2025年3月) 在GPT-3.5Turbo,GPT-4o,Gemini 1.5Flash,Claude 3.5Sonnet,Llama 3-70B中测量跨界性别 x种族偏见,在自动评估20个入门级工作的简历上. 果实质性 (COLM 2025, arXiv:2508.07111) 引入了基于不确定性的交叉身份公平评估. 尤和安尼阿努2025年将性别神经元识别在MLP层中;阿桑和瓦莱斯2025年使用SAE来揭示临床种族偏见;周等人 头的注意力是为了头.  Meta-critic (arXiv:2508.11067):10年文学不成比例地关注二元性别偏见.

> **【中文解读】**本节介绍了AI系统中的偏见来源,检测和缓解方法.

> **【拓展：交叉偏见 → 真实世界影响】**其他们 (PNAS Nexus, 2025 年 3 月) 测量了GPT-3.5 Turbo、GPT-4o、Gemini 1.5 Flash、Claude 3.5 Sonnet、Llama 3-70B 在 20 个入门级职位中自动简历评估中交叉性别×种族偏见──GPT-4o 在简历评分中对黑人女性的惩罚比黑人男性和白人女性的分别更严重单轴评估无法捕捉这种效应──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, toy embedding-based bias probe) | **语言:** Python（标准库，玩具嵌入偏见探针）
**Prerequisites:** Phase 05 (word embeddings), Phase 18 · 01 (instruction following) | **前置知识:** Phase 05 (词嵌入), Phase 18 · 01 (指令遵循)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:阶段05 词嵌入) 、阶段18·01──偏见分两类:代表性(刻板印象/抹除)vs 分配性(资源不平等) 。
>  **【类比】**偏见 = "AI 的有色眼镜"――来自训练数据(社会历史偏见) + 训练目标――评估三方法:嵌入空间(向量几何) + 概率(logits 差) + 生成文本(输出统计) ・2025 一个PNAS 连接:GPT/Claude/Gemini/Llama 在简历评估上都有交叉性别×种族偏见――Yu 2025 在 MLP 层定位"性别神经元",Ahsan 2025 用 SAE 揭示临床种族偏见――

## 学习目标

- 定义代表性与分配损害,并在LLM部署中举一个例子.

> 定义代表性伤害和分配性伤害,并给每个 LLM部署中的例子.

- 举个名单,说明Gallegos及其他2024年的三个评估-计量类别,并描述每个计量类别的一个.

> 列出加勒戈等2024年三类评估指标,并描述每个类中的一个指标.

- 描述跨区性,以及为什么基于不确定性的WinoIdentity的公平度测量解决单轴偏见评估的缺陷.

> 描述交叉性以及为什么基于不确定性的公平测量解决了单轴偏见评估的缺陷.

- 描述对偏见的两种机械解释性方法 (性别神经元,SAE特征,注意力头操纵).

> 描述两种偏见的机制可解释性方法:

## 问题问题

之前的课程涵盖了故意的伤害 (入狱,策划) 和安全治理.偏见是从训练数据分发,快速框架,积累的设计选择中出现的伤害.测量和减少是对抗强度的独特方法挑战.

> 之前的课程包括故意伤害 (越狱,策略) 和安全管理.偏见是没有意图的伤害.

## 概念的概念

### 代表性与分配性

- **Representational harm.**那些以女性为特色的护士的法律法师,
- **Allocational harm.**黑人申请人简历的评分系统地降低,

> **代表性伤害：**刻板印象,抹除,低性描绘.**分配性伤害：**不平等的物质结果. 两种不同的模型可以"代表性无偏见",但"分配性有偏见".

模型可以"具有代表性公正性" (产生多种描述),同时也可以"具有分配偏见性" (产生不平等的建议).评估需要衡量两者.

> 评估需要同时测量两者――

> **【中文解读】**三类评估指标:嵌入基础 (测量身份词和属性词之间的统计关联,限制在测量表现而不是行为;概率基础 (刻板印象确认与违反补充对数似然比,捕获部分行为偏见;生成文本基础下游任务测量)

### 评估-计量类别 (Gallegos及其他2024年)

- **Embedding-based.**测试在RLHF前嵌入式中进行了WEAT式测试.测量身份术语和属性术语之间的统计联系.有限:测量了表现,而不是行为.
- **Probability-based.**记录概率: 证实刻板印象与违反刻板印象的完成. 解码器边测量. 捕捉一些行为偏见.
- **Generated-text-based.**经历评分,建议写作,对话. 环境最有效; 复制最难.

> **嵌入基础：**测试,测量身份词和属性词的统计关联.**概率基础：**刻板印象确认与违反补充的对数似然比比.**生成文本基础：**下游任务测量,生态效率最高,但最难复现.

### 交叉性

对于"性别"的偏见评价忽略了只针对 (性别,种族) 双对的偏见. 一项研究发现,GPT-4o 处罚黑人女性在简历中分别得分超过黑人男性和白人女性.单轴评价不能捕获这一点.

> 其他研究人员发现,GPT-4o在简历评分中对黑人女性的惩罚比黑人男性和白人女性的处罚更严重.

果识别 (COLM 2025) 引入了基于不确定性的截面公平性.它测量模型对结果的不确定性是否在截面认同双体中不同,而不仅仅是点预测. 这捕获了模型在各组中同样错误的情况,但对一些人来说更不确定,从而产生了不同的下游分配行为.

> 基于不确定性交叉性公平评估的引入. 它测量模型在不同交叉身份组上的结果不确定性是否不同.

> **【拓展：机制可解释性 → 偏见干预新路径】**2024-2025年机制可解释性工作开辟偏见到机制干预的路径:性别神经元 (YU & Ananiadou 2025) 特定的MLP神经元与性别特定行为相关,消融这些神经元以有限的能力成本减少性别差距;临床种族偏见SAE(Ahsan & Wallace 2025) 稀疏自编码器特征将内部表征分解为可解释维度;UniBias(Zhou 等人 2024) 注意力操作实现零样本去偏见.

### 机械方法

2024-2025年可解释性工作将对机械干预产生偏见:

- **Gender neurons (Yu & Ananiadou 2025).**特定的MLP神经元与性别特定的行为相关. 删除这些神经元可以减少性别差距的指标,而能力成本也有限.
- **Clinical racial bias via SAEs (Ahsan & Wallace 2025).**缩自动编码功能将内部表示分解成可解释的维度;可以识别和压制与种族相关的特性.
- **UniBias (Zhou et al. 2024).**专用头显放大身份类敏感性;零化或重权这些头显减少偏见,没有细调.

> 2024-2025年机制可解释性工作开辟了偏见到机制干预的途径:性别神经元消融这些神经元以有限能力成本减少性别差距;临床种族偏见SAE识别和抑制种族相关特征;UniBias注意力操作实现零样本偏见.

> **【中文解读】**元批评(arXiv:2508.11067, 2025):10年文献回顾发现该领域不成比例地集中于二元性别偏见――其他轴残疾、宗教、移民身份、多语言身份获得关注远少得多――狭窄关注可能通过忽视伤害边缘化群体:在二元性别上良好偏见的模型可能在没有人检查的维度上严重偏见――

### 对于"重点批判"

十年文学审查 (arXiv:2508.11067, 2025) 发现该领域对二元性别偏见的关注不成比例.其他轴 残疾,宗教,移民状态,多语言身份得到了更少的关注.

> 10年文献回顾发现,该领域不成比例地集中在二元性别偏见方面.

### 在这个阶段的第18阶段

课程20-21正式涵盖偏见和公平性.课程22涵盖隐私.课程23涵盖水标.这些是用户损害层补充早期欺骗/安全层.

> 课 20-21 正式涵盖偏见和公平―― 第22课 涵盖隐私―― 第23课 涵盖水印―― 这些是补充早期欺诈/安全层的用户伤害层――

> **【拓展：交叉性 → WinoIdentity 基准】**基于不确定性交叉性公平评估的引入. 它测量模型在不同交叉身份元组上的结果是否不确定性不确定性不仅仅是点预测.

## 用它使用方法
```figure
an-bias-two-harms
```

## 用它

`code/main.py`通过简单的共产嵌入,测量身份术语和属性术语之间的距离:可以注入一个偏差并观察测量火;应用一个简单的脱操作并观察部分恢复.

> `code/main.py`构建玩具嵌入偏见探针:测量简单共存嵌入中身份词和属性词之间的 WEAT 式距离――你可以注入偏见并观察指标触发;应用简单去偏见操作并观察部分恢复――

## 发射上线

这一课产生了`outputs/skill-bias-eval.md`鉴于模型卡或公平性要求,它审计了三个指标类别 (嵌入,概率,生成文本),跨区性覆盖和任何调整干预的机制的评估.

> 本课产出发 `outputs/skill-bias-eval.md`△ 提供模型卡或公平性声明,审计三类指标的评估,交叉覆盖和偏见干预机制.

## 练习题

1. 跑步`code/main.py`报告在退化步骤前后的WEAT类偏差分数.解释为什么指标不会降到零.

2. 通过交叉测试扩展探测器: (性别,种族) x (职业生涯,家庭). 报告跨轴偏差分数.

3. 阅读An et al. 2025 (PNAS Nexus). 确定他们报告的两个交叉效应,单轴性别评估将错过.

4. 和安尼阿努在2025年确定性别神经元. 绘制一个伪造实验,将区分"这些神经元导致性别偏见"和"这些神经元与性别偏见相关".

5. 分析人员认为,该领域对二元性别的关注太狭.

## 关键词 关键词

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Representational harm | "stereotypes / erasure" | Biased portrayal of a group |
| Allocational harm | "unequal decisions" | Biased material outcome for a group |
| WEAT | "the embedding test" | Word Embedding Association Test; co-occurrence-based bias probe |
| Intersectionality | "combined identity effects" | Bias that emerges at the intersection of multiple identity axes |
| Gender neurons | "MLP bias neurons" | Specific neurons whose activations correlate with gender-specific behaviour |
| SAE feature | "interpretable dimension" | Sparse-autoencoder-identified feature; useful for mechanistic bias analysis |
| UniBias | "attention-head debiasing" | Zero-shot debiasing by reweighting attention heads |

## 继续阅读 继续阅读

- [Gallegos et al. — Bias and Fairness in LLMs: A Survey (arXiv:2309.00770, Computational Linguistics 2024)](https://arxiv.org/abs/2309.00770)法典调查
- [An et al. — Intersectional resume-evaluation bias (PNAS Nexus, March 2025)](https://academic.oup.com/pnasnexus/article/4/3/pgaf089/8111343)五个模型的交叉研究
- [WinoIdentity — uncertainty-based intersectional fairness (arXiv:2508.07111, COLM 2025)](https://arxiv.org/abs/2508.07111)新的基准
- [UniBias — attention-head manipulation (Zhou et al. 2024, ACL)](https://arxiv.org/abs/2405.20612)零射击脱
