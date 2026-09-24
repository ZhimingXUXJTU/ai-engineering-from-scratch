# 红队工具 格拉克,拉马卫队,Pyrit 拉马卫队工具

> 两位公司将在2026年完成的工作. 拉马卫队 (Meta) 是拉马-3.1-8B分类器,调整了14个MLCommons危险类别;2025年拉马卫队4是从拉马4侦察中剪制的12B原生多模分类器. 卡克 (NVIDIA) 开源LLM漏洞扫描仪,具有静态,动态和适应性探测器,用于幻觉,数据泄露,快速注射,毒性和 jailbreaks. 通过 Crescendo,TAP和定制转换链进行多轮红团队活动,以进行深度利用. 拉马卫队3在Meta的"拉马卫队3群模型" (arXiv:2407.21783) 中记录;拉马卫队3-1B-INT4在 arXiv:2411.17713;Garak的探测器架构在 github.com/NVIDIA/garak. 这些工具是红团队研究 (课12-15),部署 (课17+) 之间的2026年生产界面.

> **【中文解读】**本节介绍了红队测试系统化的安全评估方法,使用自动攻击发现AI 系统漏洞. 三种生产工具定义了2026年红队技术:Llama Guard (Meta) Llama-3.1-8B 分类器微调到14个MLCommons 危险类别;Garak(NVIDIA) 开源LLM 漏洞扫描机,含静态、动态和自适应探针;PyRIT (Microsoft) 多轮红队活动,含 Crescendo、TAP 和自定义转换链.

> **【拓展：2026 红队技术栈 → 生产配置】**标准配置:Llama Guard 放在模型两侧(输入+输出),Garak 每晚运行回归测试,PyRIT 用于预发布活动。Prompt-Guard-86M 是 Meta 的轻量级输入分类器,与Llama Guard 配合使用。TrustyAI 将Garak 和Llama Stack 盾牌 集成进行端到端评估。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, tool-architecture simulator and Llama Guard-style classifier mock) | **语言:** Python（标准库，工具架构模拟器和 Llama Guard 风格分类器模拟）
**Prerequisites:** Phase 18 · 12-15 (jailbreaks and IPI) | **前置知识:** Phase 18 · 12-15 (越狱和 IPI)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前请先掌握:阶段18·12-15(越狱+IPI 全套) ⋅2026 红队工具三件套──
>  **【类比】**红队工具 = "AI安全的透透测试套件"――Llama Guard(Meta) = 输入输出分类器件(14 危险类别,类似于阶段15·18);Garak(NVIDIA) = 漏洞扫描器(静态+动态+自适应探针,覆盖幻觉/数据泄漏/越狱);PyRIT(Microsoft) = 多轮深度攻击编排(Crescendo/TAP/自定义链) ─三件套件是研究(12-15) 和部署(17+) 之间的工程界面──

## 学习目标

- 描述安全堆中的Llama Guard 3/4的位置:输入分类器,输出分类器或两者.

> 描述拉马卫队 3/4 在安全技术中的位置:输入分类器、输出分类器或两者兼有──

- 列出14个MLCommons危险类别,并列出一个不明显的危险类别 (代码解释器滥用).

> 列出14个MLCommons 危险类别,并说明一个不明显的类别

- 描述加拉克的探测器架构:探测器,探测器,带.

> 描述Garak的探针架构:探针、检测器、线束──

- 描述PyrIT的多轮运动结构以及它与Garak探测器的构成方式.

> 描述Pyrit多轮活动结构及其与Garak探针组合的关系.

## 问题问题

课程12-15介绍了攻击表面.生产部署需要可重复,可扩展的评估.三种工具占据了2026年主导地位:Llama Guard (防务分类器),Garak (扫描仪),PyrIT (运动管弦仪).每个工具都针对红队生命周期的不同层次.

> 课程12-15 展示攻击面──生产部署需要可重复、可扩展的评估──三工具主导 2026年:拉马卫队 (Llama Guard) 防卫分类器) ‧ 格拉克 (Garak) 扫描器) ‧ 皮里特 (PyRIT) 活动编排器) ‖每个针对红队生命周期的不同层次──

## 概念的概念

> **【中文解读】**拉马卫 3 是拉马-3.1-8B 模型微调到 MLCommons AILuminate 14 类别的输入/输出分类,支持 8种语言。拉马卫 3-1B-INT4 是量化边缘变体(440MB,移动CPU约30代币/s) ・拉马卫 4(2025年4月) 是12B 原生多模态分类器,从拉马4 侦察剪枝,取代了之前的8B 文本和11B 视觉分类器。

### 拉马卫队 (Meta)

拉马卫队3是拉马-3.1-8B型号,为MLCommons AILuminate14类的输出/输出分类进行了细节调整:
- 暴力犯罪,非暴力犯罪,性犯罪,CSAM,谤
- 专业咨询,隐私,知识产权,无歧视武器,仇恨
- 自杀/自伤,性内容,选举,代码解释者滥用

> 拉马卫队3 是拉马-3.1-8B 模型,针对MLCommons AILuminate 14 个类进行输入/输出分类微调――支持 8种语言――

支持8种语言. 使用:在LLM (输入调节),LLM (输出调节) 之后,或两者.这两种用途产生不同的训练分布.

> 使用方式:放在LLM之前 (输入审核) 之后 (输出审核) 或两者兼有.

拉马卫 3-1B-INT4 (arXiv:2411.17713, 440MB,在移动CPU上使用30个代币/秒) 是量化边缘变体.

> 拉马卫 3-1B-INT4 是量化边缘变体(440MB,移动CPU约30代币/秒) ⋅

拉马卫队4 (四月2025) 是12B,原产地是多型的,从拉马卫队4 Scout中剪切.它以一种类别器取代了8B文本和11B视觉前身,它摄入了文本+图像.

> 拉马卫队4号 (Llama Guard 4号) 是12B原生多模态分类器,从拉马4号的侦察剪枝,替代了之前的8B文本和11B视觉分类器.

> **【拓展：Garak 架构 → 探针/检测器/线束】**格拉克的三层结构:探针幻觉、数据泄露、提示注入、毒性、越狱的攻击生成器,分为静态(固定提示)、动态(生成提示)、自适应(响应目标输出);检测器针对预期失败模式评分输出;线束管理探针-检测器对,运行活动,生成报告.基于层级评分(TBSA) 替代二元通过/失败模型可以通过重度相同的探针级 3 但失败级 5..

### 卡拉克 (NVIDIA)

开源漏洞扫描仪.
- **Probes.**攻击生成器用于幻觉,数据泄漏,即时注射,毒性, jailbreaks.静态 (固定提示),动态 (生成提示),适应性 (响应目标输出).
- **Detectors.**预期失败模式的结果 毒性,泄漏,破解.
- **Harnesses.**管理探测器对,运行运动,生成报告.

> 开源漏洞扫描机.架构:探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针.

TrustyAI将Garak与Llama-Stack屏蔽 (Prompt-Guard-86M输入分类,Llama-Guard-3-8B输出分类) 集成为端到端的屏蔽目标评估.基于层次的评分 (TBSA) 取代了二进制通过/失败.

> 基于层次评分,TBSA可以通过重度层级3但失败层级5.

### 公司

通过Python风险识别工具包,多个轮回红团队的运动.
- **Converters.**转换一个种子提示语法,编码,翻译,角色扮演.
- **Orchestrators.**运行活动:Crescendo (升级),TAP (分支),RedTeaming (定制循环).
- **Scoring.**法律法官或法官分类人

> 字符号是Python 风险识别工具包.

皮瑞特是加拉克的重量表兄弟.加拉克运行了数千个单转探测器;皮瑞特运行了旨在打破特定故障模式的深度多转运动.

> 罗拉克运行了数千个单轮探针;罗拉克运行旨在打破特定失败模式的多轮深度活动.

### 子

按模型两侧安装Llama Guard. 晚上运行Garak以回归. 运行PyrIT以预发行活动. 这是2026年大多数生产部署的默认配置.

> 在模型两侧放置拉马卫队. 每晚运行加拉克回归测试.

> **【中文解读】**评估陷:评判身份所有三个工具都可以使用LLM评判,评判校准驱动报告的ASR(课12),必须指定评判;探针过时Garak 探针随着模型修复和老化,自适应探针(PAIR式) 比静态探针老化更慢;Llama Guard 在良性内容上的误报率早期版本过标政治和LGBTQ+内容,v3/v4校准有改善但未部署校准.

### 评估陷

- **Judge identity.**论坛的评审员可以使用法师法官;评审校准驱动器报告ASR (课 12). 指定工具旁边的评审员.
- **Probe staleness.**适应性探测器 (PAIR形状) 比静态探测器年龄较慢.
- **Llama Guard FPR on benign content.**早期的Llama Guard版本上调了政治和LGBTQ+内容;Llama Guard 3/4校准改进,但没有按部署进行校准.

### 在这个阶段的第18阶段

课程12-15是攻击家庭.课程16是生产工具.课程17 (WMDP) 是对双重用途能力的评估.课程18是边界安全框架,这些工具被包装成一个政策结构.

> 课时12-15是攻击家族.课时16是生产工具.课时17是双重用途能力评估.课时18是将这些工具包装在政策结构中的前沿安全框架.

> **【拓展：PyRIT → 多轮深度利用】**皮瑞特 (Pyrit) 是Garak的重量级表亲. 皮瑞特运行了数千个单轮探针,Pyrit运行旨在打破特定失败模式的多轮深度活动. 它的核心是转换器链.

## 用它使用方法
```figure
al-guard-stack
```

## 用它

`code/main.py`玩具可以使用Llama Guard类型的分类器 (关键字+14类别的语义功能),玩具Garak (探测器循环) 和PyrIT类型的多转转换链.您可以将三个工具运行到模拟目标上并观察不同的覆盖签名.

> `code/main.py`构建玩具 拉马卫队 风格分类器、玩具 格拉克线束和 PyRIT风格多轮转换链――你可以对模拟目标运行三个工具并观察不同的覆盖特征――

## 发射上线

这一课产生了`outputs/skill-red-team-stack.md`根据部署描述,它列出了三个工具中哪些是合适的,哪些工具应配置,以及哪些回归顺序应运行.

> 本课产出发 `outputs/skill-red-team-stack.md`给定部署描述,命名三个工具中的哪些适合,每个配置什么,以及什么回归节奏.

## 练习题

1. 跑步`code/main.py`对于单轮攻击和多轮攻击, 拉马卫兵类别的检测率进行比较.

2. 运用一个新的Garak探测器:一个基64编码的有害请求.

3. 扩展Pyrit式转换链,使用"翻译到法语,然后转换"转换器.

4. 阅读Llama Guard 3的危险类别列表. 确定两个类别,培训数据实际上会产生高的虚假阳性率对合法开发者内容.

5. 根据Garak和Pyrit的设计原则进行比较.

## 关键词 关键词

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Llama Guard | "the classifier" | Fine-tuned Llama-3.1-8B/4-12B safety classifier with 14 hazard categories |
| Garak | "the scanner" | NVIDIA open-source vulnerability scanner; probes, detectors, harnesses |
| PyRIT | "the campaign tool" | Microsoft multi-turn red-team orchestrator; converters, orchestrators, scoring |
| Prompt-Guard | "the small classifier" | Meta's 86M prompt-injection classifier, paired with Llama Guard |
| TBSA | "tier-based scoring" | Garak's tier-based pass/fail replacing binary outcomes |
| Converter chain | "paraphrase + encode + ..." | PyRIT composition primitive for building multi-step attacks |
| MLCommons hazard categories | "the 14 taxonomies" | Industry-standard taxonomy Llama Guard targets |

## 继续阅读 继续阅读

- [Meta — Llama Guard 3 (in Llama 3 Herd paper, arXiv:2407.21783)](https://arxiv.org/abs/2407.21783) 8B分类器
- [Meta — Llama Guard 3-1B-INT4 (arXiv:2411.17713)](https://arxiv.org/abs/2411.17713)量化移动分类器
- [NVIDIA Garak — GitHub](https://github.com/NVIDIA/garak)扫描仪的备忘录和文档
- [Microsoft PyRIT — GitHub](https://github.com/Azure/PyRIT)活动工具包
