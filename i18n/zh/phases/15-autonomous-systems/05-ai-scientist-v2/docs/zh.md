# 工坊级自主研究

> 萨卡纳的AI科学家 v2 (Yamada等, arXiv:2504.08066) 运行了整个研究循环:假设,代码,实验,数字,写作,提交. 这是第一个在ICLR 2025研讨会上进行的纸质合格同行审查的系统. 独立评估 (Beel等人) 发现, 42% 的实验失败于编码错误, 萨卡纳的医生警告说,该代码基础执行了LLM编写的代码, 这两个图片的两半都是重点.

> **【中文解读】**萨卡纳的AI科学家 v2(Yamada 等人,arXiv:2504.08066) 运行完整的研究循环:假设,编码,实验,图表,写作,提交――这是通过ICLR 2025 工作坊同行评审的第一个有生成论文系统――独立评估(Beel 等人) 发现 42% 的实验因编码错误失败,文献综述频繁将建立的概念错误标记为新──萨卡纳自己的文档警告代码库执行LLM编写的代码并建议Docker 隔离──这两方面都是本课重点──

> **【拓展：开放式研究的代价】**AlphaEvolve 和 DGM 都有"机器可检查的评估器"单元测试或基准.研究没有:论文由审稿人评判,而不是单元测试. 这使得闭环更难,但价值也更高.研究是复利增长的来源.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, research-loop state-machine toy) | **语言:** Python（标准库，研究循环状态机玩具）
**Prerequisites:** Phase 15 · 03 (AlphaEvolve), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 03（AlphaEvolve），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:阶段15·03-04(AlphaEvolve/DGM) 、阶段14·30+(工作台 实践) 、学术论文写作基础――AI科学家 = 开放式研究任务,评估器是"同行评审"(弱信号),所以安全模型完全不同――
>  **【类比】**智能科学家="AI 博士生"――AlphaEvolve/DGM = 工程师(评估器=单元测试,强信号);AI科学家=博士生(评估器=审稿人,弱信号) ――同样跑实验-评估-代循环,但弱信号评估让代理人容易欺骗42% 的实验代码有错误,文献综述已知概念当新发现――修复:(1) Docker 隔离(必须执行LLM 代码沙箱);(2) 人类复核(披露 AI 生成);(3) 引入强信号检查(如复现实测试) 

## 问题 问题引入

研究是一个无限的任务.

> 研究是开放任务.

与AlphaEvolve的算法搜索或DGM的基准限制自我修改不同,研究结果没有机器可检查的准确性标准.论文由审查者评判,而不是单元测试.这使循环更难关闭,并且更有价值,因为研究是复合进步的所在.

> 与AlphaEvolve的算法搜索或DGM的基准约束自修改不同,研究结果没有机器可检查的正确性标准.论文由审稿人评价,而不是单元测试.

通过从人类创作的模板开始,AI科学家v1 (Sakana,2024) 关闭了循环. 法律法师在固定架子内进行了实验. AI科学家 v2 (Yamada等, 2025) 通过使用视觉语言模型批评循环的代理树搜索来删除模板要求. 该系统产生想法,实施实验,产生数字,写论文,并反复评论者的反.

> 通过AI科学家 v1(Sakana,2024) 从人类编写的模板开始闭合循环.LLM 在固定脚手架中填充实验.

> **【中文解读】**运行完整的研究循环:假设,编码,实验,图表,论文编写和提交. 它是通过ICLR 2025 工作坊同行评审系统的第一个有生成论文.

专业评审判决:在ICLR 2025研讨会上接受了一份v2生成的论文 (含披露).独立评价判决:系统远非可靠.这两者都是真的.

> 同行评审结论:一篇 v2 生成的论文被ICLR 2025 工作坊接受了(附带披露) ・独立评估结论:系统远非可靠──两者都是事实──

## 概念的核心概念

### 建筑,建筑.

1. **Idea generation.**专业士提出了基于主题和先前文献的研究想法. v1使用模板; v2使用在假设领域的代理搜索.
   翻译: 中文**想法生成。**基于主题和先前文献提出研究思想.
2. **Novelty check.**文献检索步骤检查了这个想法是否已发表.这是Beel等人评估发现错误标签的步骤.
   翻译: 中文**新颖性检查。**文献检查步骤检查想法是否已发表.
3. **Experiment plan.**经纪人起草了实验协议,并编写了代码.
   翻译: 中文**实验计划。**经纪人 起草实验协议并编写代码――
4. **Execution.**在比尔等的测量中, 42% 的实验在这个阶段失败于编码错误.
   翻译: 中文**执行。**在比尔等人的测量中,42%的实验在此阶段因编码错误失败.
5. **Figure generation.**视觉语言模型读取生成的数字并重新写出它们以确保清晰度.这是v2的关键技术补充.
   翻译: 中文**图表生成。**视觉语言模型读取生成图表并为清晰性重写它们──这是 v2 的关键技术添加──
6. **Writeup.**法律士编写一篇论文,与内部审查员进行反复.
   翻译: 中文**撰写。**起草论文,与内部审稿人代
7. **Optional: submission.**报纸提交给一个场所.
   翻译: 中文**可选：提交。**论文提交到会议.

### 工作室接受结果意味着什么

一份v2生成的论文在ICLR 2025研讨会上通过了同行评审.作者向计划委员会披露了论文的起源.接受是数据点;它不是声称系统"进行研究"的许可.

> 一篇 v2 生成的论文在ICLR 2025 工作坊通过同行评审.作者向程序委员会披露了论文的来源.

重要背景:研讨会论文比主要会议论文低.同行评审很;在任何一天都会接受小部分提交.一个成功是概念证明,而不是可靠性声明.Nature 2026论文记录了端到端循环,它本身是由人类研究人员共同撰写的;它不是"系统写了一篇 Nature论文".

> 重要背景:工作坊论文的门低于主会议论文――同行评审有噪音;任何一天都有一小部分提交被接受――一次成功是概念证明,不是可靠性声明――自然2026论文记录了端到端循环,本身由人类研究人员共同撰写;不是"系统写了一篇自然论文".

### 独立评估发现了什么

贝尔等人 (arXiv:2502.14297) 进行了外部评估.

> 其他士: 运行外部评估

- **Experiment failures.**42%的实验因编码错误 (不良进口,形状不匹配,未定义变量) 失败.
  翻译: 中文**实验失败。**42%的实验因编码错误失败了,但不是全部.
- **Novelty mislabeling.**文献检索步骤经常标记既定概念为新奇.
  翻译: 中文**新颖性错误标记。**文献检索步骤频繁将已建立的概念标记为新──这是研究界的幻觉等效──
- **Presentation-quality gap.**视觉语言的形象批评产生了出版级的视觉,掩盖了潜在的实验弱点.
  翻译: 中文**呈现质量差距。**视觉语言图表评审产生了出版级视觉效果,掩盖了底层实验的弱点.

对于这一阶段,最后一个发现是重要的:一个系统,在没有做出说服力的研究的情况下产生令人信服的结果,

> 最后一个发现对本阶段很重要――产生令人信服的输出,但未经令人信服的研究系统,比明显失败的系统更危险而不是更安全――

评估必须达到底层要求,而不是仅限于数字.

> 评估必须触及底层声明,而不是停在图表中.

### 沙箱逃走的担忧

萨卡纳自己的存储库 README警告说:

> 萨卡纳 自己的仓库 README 警告:

> 由于该软件的性质,它执行了LLM生成的代码,我们无法保证安全. 有危险的包裹的风险,不受控制的网络访问,以及不预期的过程的产卵.

> 由于本软件执行了LLM生成的代码,我们无法保证安全.

没有一个沙盒,严格限制文件系统,网络和过程操作,任何自主导的研究代理都可以将数据泄露,烧毁计算或重写自己.

> 这是未经验证领域的自主操作形式.LLM 写代码;代码运行;代码可以做任何被允许的进程.没有硬限制文件系统,网络和进程操作的沙箱,任何自主研究代理都可泄露数据,烧毁计算或重写自己.

由于其评估器紧密,AlphaEvolve的沙盒故事更容易.AI Scientist v2的循环运行开放式代码,具有开放式目标.这就是为什么它需要更强大的隔离 (Docker最小;seccomp/gVisor优先) 和离开系统之前手动审查每个提交.

> 由于其评估器严密,AlphaEvolve的沙箱描述更容易. AI科学家 v2的循环使用开放目标运行开放代码.

### 在边境堆里,v2位于前沿的位置.

| System | Target | Output kind | Evaluator | Known failure |
|---|---|---|---|---|
| 系统 | 目标 | 输出类型 | 评估器 | 已知失败 |
| AlphaEvolve | algorithms | code | unit + benchmark | bounded by evaluator rigor |
| AlphaEvolve | 算法 | 代码 | 单元 + 基准 | 受评估器严谨性约束 |
| DGM | agent scaffolding | code | SWE-bench | reward hacking |
| DGM | Agent 脚手架 | 代码 | SWE-bench | 奖励篡改 |
| AI Scientist v2 | research papers | text + code + figures | peer review (weak) | experiment failures, mislabeling, polish masking weakness |
| AI Scientist v2 | 研究论文 | 文本 + 代码 + 图表 | 同行评审（弱） | 实验失败、错误标记、修饰掩盖弱点 |

它们是最弱的自动评估器,最宽的输出表面,

> 它们中最弱的自动评估器,最广的输出面和最短的公开产品路径.

运营控制 (沙盒,审查,披露) 执行大部分安全工作.

> 操作控制 (沙箱,审查,披露) 承担了大部分安全工作.

## 用它实现框架
```figure
mx-research-loop
```

## 用它

`code/main.py`模拟v2循环作为状态机:想法 →新奇检查 →实验 →图像 →写作 →评论 →接受或述.每个状态具有可配置的故障概率,从Beel等研究结果中抽取.运行模拟器为N循环并计算:

> `code/main.py`将 v2 循环模拟为状态机:想法 → 新性检查 → 实验 → 图表 → 写作 → 审稿 → 接受或代――每个状态有从Beel 等人发现中提取的可配置失败概率――运行模拟器 N 循环并计数:

- 许多想法都会得到提交.
  中文翻译:多少想法到达提交.
- 磨纸隐藏了多少件临界实验缺陷.
  中文翻译:多少提交会有修饰论文隐藏的关键实验缺陷──
- 如何重新尝试预算,
  中文翻译:重试预算如何衡量质量和产量之间的权衡.

## 运送它.

`outputs/skill-ai-scientist-sandbox-review.md`检查任何由研究循环代理产生的东西,

> `outputs/skill-ai-scientist-sandbox-review.md`经验循环 经验循环 经验循环 经验循环 经验循环

## 练习题

1. 跑步`code/main.py`根据"环节运行"的部分,产生了"清洁"的纸. 根据"试验失败缺陷"的部分,产生了"清洁"的纸.
   中文翻译:使用默认参数运行 `code/main.py`,有多少个论文有图表评审修改的实验失败缺陷?

2. 违约的数据已经使用了Beel等的42% /25%.`--experiment-failure 0.20 --novelty-mislabel 0.10`然后是`--experiment-failure 0.60 --novelty-mislabel 0.40`两次运行之间,抛光但缺陷的股票如何转移?
   中文翻译:默认已使用Beel等人的42% / 25%──用`--experiment-failure 0.20 --novelty-mislabel 0.10`重跑,然后用`--experiment-failure 0.60 --novelty-mislabel 0.40`两次运行之间修改但缺陷的比例如何变化?

3. 阅读Sakana的AI科学家 v2 repo README关于沙箱要求. 举个两个额外的限制 (除了Docker) 你会申请多天自动运行.
   中文翻译:阅读Sakana AI科学家 v2 仓库 README 关于沙箱要求──命名你会为多日自主运行添加的两个额外限制(除Docker 外)──

4. 阅读Beel等人 第4节关于表达质量差距. 设计一个额外的评估器,可以捕获看起来很好,但实验上有缺陷的论文.
   中文翻译:阅读Beel 等人 第4节关于现有质量差距的设计.

5. 提出一个对研究人员产生的研究结果进行人为审查的协议,比"博士阅读每篇论文"更好.
   中文翻译:为研究代理 输出提议比"博士读每篇论文"扩展更好的人工审查协议――识别瓶并根据这个设计――

## 关键词 快速查找表

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AI Scientist v1 | "Sakana's templated research agent" | Filled experiments into a fixed scaffold |
| AI Scientist v1 | "Sakana 的模板研究 Agent" | 在固定脚手架中填充实验 |
| AI Scientist v2 | "Template-free research agent" | Agentic tree search with VLM figure critique |
| AI Scientist v2 | "无模板研究 Agent" | 带有 VLM 图表评审的 Agent 式树搜索 |
| Agentic tree search | "Branching research agent" | Expands multiple experiment plans in parallel; prunes by internal critic |
| Agent 式树搜索 | "分支研究 Agent" | 并行展开多个实验计划；由内部评论者修剪 |
| Vision-language critique | "VLM polish on figures" | Multimodal model reads figures and rewrites them for clarity |
| 视觉语言评审 | "VLM 修饰图表" | 多模态模型读取图表并为清晰性重写 |
| Literature retrieval | "Novelty check" | Searches prior work to confirm idea novelty — documented to mislabel |
| 文献检索 | "新颖性检查" | 搜索先前工作以确认想法新颖性——文档记录会错误标记 |
| Polish masking | "Pretty paper, broken research" | Presentation quality exceeds experimental quality; hides weaknesses |
| 修饰掩盖 | "漂亮论文，破碎研究" | 呈现质量超过实验质量；隐藏弱点 |
| Sandbox escape | "LLM code breaks out" | Agent-executed code does things the loop designer did not intend |
| 沙箱逃逸 | "LLM 代码逃逸" | Agent 执行的代码做循环设计者未预期的事 |

## 继续阅读 继续阅读

- [Yamada et al. (2025). The AI Scientist-v2](https://arxiv.org/abs/2504.08066)纸
  中文翻译:论文──
- [Sakana blog on the Nature 2026 publication](https://sakana.ai/ai-scientist-nature/)供应商总结与同行评审背景.
  中文翻译:厂商摘要,含同行评审背景.
- [Beel et al. (2025). Independent evaluation of The AI Scientist](https://arxiv.org/abs/2502.14297)外部评估数字.
  中文翻译:外部评估数字──
- [Sakana AI Scientist v1 paper](https://arxiv.org/abs/2408.06292)模板前身.
  中文翻译:模板化前身──
- [Anthropic — Measuring AI agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy)更广泛的开放研究机构框架.
  中文翻译:开放式研究代理的更宽框架.
