# 记忆块与休眠计算 (Letta)
# 记忆阻碍和睡眠时间计算

> 模特可以直接编辑的功能性记忆区块,以及一个睡眠时间代理,在主要代理在置时,将记忆稳定成一致.

> **【中文解读】**2024年成为Letta.2026年的演变增加了两个想法:模型可以直接编辑离散功能记忆块,以及主机机空时异步合并记忆的休眠机.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT) | **前置知识:** Phase 14 · 07 (MemGPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 列塔使用的三个内存层次 (核心,回忆,存档) 和每个层次的作用.
  中文翻译:说出 Letta 使用的三个记忆层级 (核心,回忆,档案) 和各自的作用.
- 解释内存区块模式:人区块,人区块和用户定义的区块作为一级打字对象.
  中文翻译:解释记忆块模式:人块、人块和用户自定义块作为一等类型化对象──
- 描述睡眠时间计算是什么,为什么它不处于关键路径,为什么它可以运行比主要代理更强的模型.
  中文翻译:描述休眠计算是什么,为什么它在关键路径之外,为什么可以运行比主代理更强的模型.
- 执行一个脚本式的两代理循环,其中一个主要代理提供响应,而一个睡眠时间代理在轮流之间巩固区块.
  中文翻译:实现一个脚本化的双代理循环,主代理提供响应,休眠代理 在轮次间合并块――

## 问题 问题引入

解决了虚拟内存控制流程.

> 解决了虚拟内存控制流――三个生产问题出现:

1. **Latency.**如果代理人必须在用户等待时剪切,总结或调整,
   翻译: 中文**延迟。**如果代理必须在用户等待时剪辑摘要或协调,尾部延迟会爆炸.
2. **Memory rot.**书籍积累,矛盾的事实仍然存在,检索却沉浸在陈旧的内容中.
   翻译: 中文**记忆腐化。**写入积累――矛盾的事实保留――检索被过时内容淹没――
3. **Structure loss.**一个平坦的档案存储器不能表达"人块总是在提示中;人块总是在提示中;任务块每次交换".
   翻译: 中文**结构丢失。**平的归档存储无法表达"人块始终在提示中;人块始终在提示中;任务块按会话交换――"

雷塔 (letta.com) 是原始MemGPT项目在2024年通过的平台名称. 纸质的模式保持了MemGPT名称. 2026年雷塔 V1重写是一个后来的,独立的步骤. 记忆区块使结构明确;睡眠时间计算将整合转移到关键路径.

> 雷塔 (Letta) 是2026年重写的.

> **【中文解读】**记忆块 (记忆块) 和休眠计算 (休眠计算) 是MemGPT/Letta的两种优化策略. 记忆块是固定大小的下文区,类似于内存页面,用于精细控制下文窗口中各种信息的占比.休眠计算指在用户不活跃时预处理和压缩记忆,减少下次会话的延迟.

> **【拓展：Letta 的演进】**雷塔 (原 MemGPT) 在2024-2025年演变中引入了记忆块和休眠计算的两个关键概念. 记忆块将在下文窗口中分为系统指令,核心记忆,对话历史等固定区,避免信息混.

>  **【前置】**必须先过第14阶段. 本节是它的直接延续. 如果你不理解MemGPT的"主上下文与外部上下文"两层模型,那么Letta的三层.

## 概念的核心概念

### 三个层

| Tier | Scope | Where it lives | Written by |
|------|-------|----------------|------------|
| 层级 | 范围 | 存储位置 | 写入者 |
| Core | Always visible | Inside the main prompt | Agent tool call + sleep-time rewrites / Agent 工具调用 + 休眠重写 |
| Recall | Conversation history | Retrievable | Automatic turn logging / 自动轮次日志 |
| Archival | Arbitrary facts | Vector + KV + graph | Agent tool call + sleep-time ingest / Agent 工具调用 + 休眠摄取 |

核心是MemGPT的核心. 记住是对话缓冲器,它被驱逐出后尾. 档案是外部商店. 分裂清除了MemGPT的两层过载.

> 核心是MemGPT的核心. 记忆是MemGPT的对话缓冲区. 档案是外部存储区.

### 记忆区块

一块是核心层面的打字,持久,可编辑的部分.原始的MemGPT论文定义了两个:

> 块是核心层的类型化,持久化,可编辑分区.

- **Human block**用户的事实 (姓名,角色,偏好,目标).
  翻译: 中文**Human 块**关于用户的事实 (姓名,角色,偏好,目标)
- **Persona block**代理人的自我概念 (身份,语调,限制).
  翻译: 中文**Persona 块**代理的自我概念 (身份,语气,约束)

列塔将其一般化为任意用户定义的区块:`Task`现在的目标是`Project`对于代码基础事实的区块,`Safety`对于硬约束,每个块都有一个`id`现在`label`现在`value`现在`limit`(字符封顶),`description`(所以模型知道何时编辑它).

> 缓慢泛化为任意用户定义块:用于当前目标的`Task`块、用于代码库事实`Project`块 用于硬约束`Safety`每块都有`id`,我知道.`label`,我知道.`value`,我知道.`limit`没有任何其他方法.`description`(让模型知道何时编辑它)

通过工具表面可编辑块:

> 块通过工具接口可编辑:

- `block_append(label, text)`
  翻译: 中文`block_append(label, text)`向块追加文本──
- `block_replace(label, old, new)`
  翻译: 中文`block_replace(label, old, new)`替换块中的文本──
- `block_read(label)`
  翻译: 中文`block_read(label)`读取块内容.
- `block_summarize(label)`凝结一个接近其极限的块.
  翻译: 中文`block_summarize(label)`压缩接近上限的块.

### 睡眠时间计算

拉特塔的2025年补充:在背景下运行第二个代理,离开关键路径.`learned_context`文件的存储记录,并将其整合或无效.

> 2025年Letta的新增功能:在后台运行第二个代理,不在关键路径上.休眠代理处理对话记录和代码库上下文,将`learned_context`写入共享块,并合并或使归档记录失效.

产品出炉:

> 随其产生的特征:

- **No latency cost.**基本响应不会等待记忆操作.
  翻译: 中文**无延迟成本。**主响应不等待记忆操作.
- **Stronger model allowed.**睡眠时间代理可能更昂贵,更慢的模型,因为它没有延迟限制.
  翻译: 中文**允许更强的模型。**休眠代理可能更昂贵,更慢的模型,因为它不受延迟束.
- **Natural consolidation window.**假定,总结,无效,当用户不等待时.
  翻译: 中文**天然的合并窗口。**在用户不等时重复摘要,使矛盾的事实失效.

形状与人类的工作方式相匹配:你完成任务,你睡觉,长期记忆一夜之间就会稳定.

>  **【类比】**睡眠时间计算 像夜晚的清洁工:白天你(主代理) 忙于响应客户,办公室(主上下文)堆满今天的会议记录、文件、咖啡杯;晚上清洁工(睡眠时间代理) 进来擦桌子、归档文件、把"明天要跟进的事"贴上便利贴上(写入人/任务块) ⋅第二天你上班,看整洁待桌面和清晰的办公清单.**关键**清洁工可以慢一点,贵一点,因为客户不等.

> 这种形态与人类工作方式一致:你做任务,你睡觉,长期记忆在夜间沉.

### 莱塔V1和本地推理
### 基于本地的推理

雷塔 V1 (`letta_v1_agent`美国国家`send_message`心跳和直线`Thought:`答案API (OpenAI) 和信息API (有扩展思维) 在单独的道上发射推理,通过轮流 (在生产中加密的供应商).控制循环仍然是ReAct.思维痕迹是结构性的,不是提示的.

> 雷塔 V1`letta_v1_agent`现在,我们已经放弃了.`send_message`跳动和内联`Thought:`通过"创建"的方法,转而使用原生推理. 答案API(OpenAI) 和带扩展思考的信息API(人类) 在独立通道上输出推理,跨回合通过传输.

### 在这个模式出现错误的地方

> ️ **【易错点】**"静默漂移"是Letta部署中最阴险的错误:睡觉时代理在后台改造了个体块 (例如把"始终用中文回复"改成中英文混用),但主代理不知道.**后果**由于对话日志只记录主代理的输出,用户发现代理行为变化却找不出原因.**一行修复**写入后版本化区块内容,并在主代理下一轮提示里注入"自上次以来区块变化:..."的不同提示

- **Block bloat.**无限`block_append`在写到字幕之前,请在字幕上按一下一个区块总结器.
  翻译: 中文**块膨胀。**无限的`block_append`快速达到上限. 在超越上限的写入之前,
- **Silent drift.**睡眠时代代理重写一个区块,而主要代理永远不会注意到.
  翻译: 中文**静默漂移。**休眠 代理 重写块,但主代理从未注意到.
- **Poisoned consolidation.**睡眠时间代理将攻击者可以进入的内容处理到核心.
  翻译: 中文**投毒合并。**休眠代理将攻击者可达的内容处理到核心中. 第27课也适用于休眠接口.

>  **【困惑】**问:睡眠时间代理使用更强的模型不会更贵吗?为什么是省钱而不是烧钱?A:看时间维度.**避开了关键路径的高价**主代理必须使用流媒体+高优先级,单价是批量的2-3倍.

## 动手构建
```figure
memory-blocks
```

## 建立它

`code/main.py`执行:

> `code/main.py`实现了:

- `Block` id,标签,值,限制,描述.
  翻译: 中文`Block`id、标签、价值、限制、描述──
- `BlockStore`   `near_limit(label)`帮助人.
  翻译: 中文`BlockStore`CRUD+ `near_limit(label)`辅助方法.
- 两名经纪人`PrimaryAgent`子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子`SleepTimeAgent`转折之间结合.
  中文翻译:两个脚本 代理`PrimaryAgent`提供轮次,`SleepTimeAgent`在轮次间合并.
- 显示了与区块的三轮对话,加上一个睡眠时间的传递,
  中文翻译:展示三轮对话带块写入的轨迹,加上压缩块和使过时事实失效的休眠处理.

运行它:

> 运行:

```
python3 code/main.py
```

转录显示了分开:主要转折速度快,产生原始写作;睡眠通道紧,清洁.

> 转录记录显示分工:主轮次快速产生原始写作;休眠处理压缩和清理.

## 用它实现框架

- **Letta**对于参考实现, (letta.com) 提供自主托管或管理云.
  翻译: 中文**Letta**为了实现,
- **Claude Agent SDK skills**作为一个块形知识 一个技能是代理按要求加载的命名,版本,可检索的指令块.
  翻译: 中文**Claude Agent SDK skills**作为块状知识技能是命名的,版本化的,可检查的指令块,代理按需加载.
- **Custom builds**对于想要控制存储后端的团队,使用Letta API合同,以便您稍后迁移.
  翻译: 中文**自定义构建**适合想要控制存储后端的团队.

## 运送它.

`outputs/skill-memory-blocks.md`产生Letta形状的块系统,用于任何运行时间,包括安全规则和引用线.

> `outputs/skill-memory-blocks.md`为了任何运行时生成Letta 形状的块系统,带休眠子,安全规则和引用连接.

## 练习题

1. 添加一个`block_summarize`工具,以模型生成的总结取代区块值,`near_limit`什么触发门可以减少总结调用和区块过度?
   中文翻译:添加 `block_summarize`工具,在`near_limit`返回真实时使用模型生成的摘要替换块值.
2. 实现睡眠时间的减值在档案中:两个文本具有90%以上的标志性重叠的记录,将其崩成一个.
   中文翻译: 在归档存储中实现休眠去重:代码重叠 >90% 的两条记录合并为一条.
3. 在每一个写记录上,旧值和差异.`block_history(label)`操作员可以调试"为什么代理忘记X".
   中文翻译:版本化块──每次写入记录旧值和差异──暴露 `block_history(label)`让运维可以调试"为什么代理忘记X"
4. 让睡眠时间代理人看作是不值得信赖的作家.
   中文翻译:将休眠代理 视为不可信的写入者.
5. 移植该例子使用Letta API (`letta_v1_agent`区块方案发生了什么变化,原生推理如何改变痕迹形状?
   中文翻译:将示例移植为使用Letta API(`letta_v1_agent`块模式有什么变化?原生推理如何改变轨迹形态?

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Memory block | "Editable prompt section" / "可编辑提示分区" | Typed, persistent, LLM-editable segment of core memory / 类型化、持久化、LLM 可编辑的核心记忆段 |
| Human block | "User memory" / "用户记忆" | Facts about the user, pinned in core / 关于用户的事实，固定在 core 中 |
| Persona block | "Agent identity" / "Agent 身份" | Self-concept, tone, constraints, pinned in core / 自我概念、语气、约束，固定在 core 中 |
| Sleep-time compute | "Async memory work" / "异步记忆工作" | Second agent doing consolidation off the critical path / 第二个 Agent 在关键路径之外做合并 |
| Core / Recall / Archival | "Tiers" / "层级" | Three-layer memory split: always-visible / conversation / external / 三层记忆拆分：始终可见 / 对话 / 外部 |
| Block limit | "Cap" / "上限" | Character limit per block; forces summarization / 每个块的字符限制；强制摘要 |
| Native reasoning | "Thinking channel" / "思考通道" | Provider-level reasoning output, not prompt-level `Thought:` / 提供商级推理输出，非提示级 `Thought:` |
| Learned context | "Sleep output" / "休眠输出" | Facts the sleep-time agent writes into shared blocks / 休眠 Agent 写入共享块的事实 |

## 继续阅读 继续阅读

- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) 块图案
  中文翻译: 拉特·记忆块博客块模式。
- [Letta, Sleep-time Compute blog](https://www.letta.com/blog/sleep-time-compute)同步整合
  中文翻译: 拉特休眠计算博客异步合并──
- [Letta, Rearchitecting the Agent Loop](https://www.letta.com/blog/letta-v1-agent)原生推理重写
  中文翻译: 缓重建代理 循环博客原生推理重写。
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560)来源
  中文翻译:MemGPT论文起源──
