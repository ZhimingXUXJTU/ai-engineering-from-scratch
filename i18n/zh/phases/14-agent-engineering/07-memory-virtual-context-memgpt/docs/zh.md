# 记忆:虚拟上下文与MemGPT
# 代理记忆 虚拟文本和记忆页面

> 文本窗口是有限的.对话,文档和工具痕迹是没有的.解决方案是OS虚拟内存重置. 主要文本是 RAM,外部存储是磁盘,它们之间的代理页面. MemGPT (Packer等, 2023) 命名了该模式;许多生产内存系统建立在它上.

> **【中文解读】**上下文窗口是有限的,但对话、文档和工具轨迹不是.MemGPT将这种类型比作操作系统虚拟内存. 下文主要是RAM,外部存储是磁盘,代理在两者之间交换.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 06 (工具使用)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 解释MemGPT基于的操作系统比喻:主语境 = RAM,外部语境 = 磁盘,内存工具 = 页面输入/输出.
  中文翻译:解释 MemGPT 所基于的操作系统类比:主上下文 = RAM,外部上下文 =磁盘,记忆工具 = 页面换进/换出――
- 实现在 stdlib 中使用主语境缓冲器,外部可搜索的存储器和页面进/出工具的双层 MemGPT 模式.
  中文翻译:用标准库实现两层 MemGPT 模式,包含主上下文缓冲区、外部可搜索存储和页面换进/换出工具──
- 描述代理如何发出"中断"查询或修改外部内存,以及结果如何将其交配到下一个提示中.
  中文翻译:描述代理如何发出"中断"来查询或修改外部记忆,以及结果如何拼接回下一个提示.
- 确定将Letta (课08) 和 Mem0 (课09) 带入 MemGPT设计选择.
  中文翻译:识别 MemGPT 中延续到 Letta(第8课) 和 Mem0(第9课) 的设计选择──

## 问题 问题引入

文本窗户似乎应该解决内存.

> 上下文窗口看似能解决记忆问题,但实际上不能.

1. **Overflow.**经过过截止时间的时间,一切都消失了.
   翻译: 中文**溢出。**长文档或工具调用密集的轨迹跨越窗口限制――截止之外的一切都丢失了――
2. **Dilution.**即使在窗口内,填充无关紧要的文本, 便会让人们忽视重要的事情.
   翻译: 中文**稀释。**即使在窗户内,不相关的填充下文也稀释了对重要内容的注意力.
3. **Persistence.**没有外部记忆的代理人不能在会议中说"记住你问我...
   翻译: 中文**持久化。**没有外部记忆的代理人不能跨会话说"记得你让我......"......

> **【中文解读】**上下文窗口看似能解决记忆问题,但实际上不能.生产环境中的三个失败模式: 1) 溢出多轮对话或长文档跨越窗口限制,切断之外的一切都丢失了; 2) 稀释窗内填充不相关上下文稀释了注意力; 3) 持久化新会话从空窗开始, 代理无法跨会话记忆.

根据Mem0的2025年论文,128k窗口的基线仍然缺少长视线的事实,

> 更大的窗户有帮助,但无法解决这个问题――Mem0的2025年论文测量发现,128k窗户的基线仍然会遗漏4k窗户+外部记忆 代理能捕获长程事实――

> **【拓展：MemGPT → 现代 Agent 记忆系统】**简介:MemGPT (Packer et al., 2023) 将上下文管理类比为操作系统虚拟内存:主上下文=RAM,外部存储=磁盘,记忆工具=页面换入换出.这是2026年所有记忆系统的基本模式.

>  **【前置】**必须先掌握:阶段14·01(代理循环) MemGPT的记忆工具是普通工具调用扩展;阶段14·06(工具使用) 记忆操作通过工具实现. 还需要操作系统基础知识

## 概念的核心概念

### 操作系统比较

基于此,MemGPT (Packer等, arXiv:2310.08560, v2 Feb 2024) 将文本管理映射到操作系统虚拟内存:

> 包装器 等人 (arXiv:2310.08560,v2 2024 年 2 月) 将上下文管理映射到操作系统虚拟内存:

| OS concept | MemGPT concept | 2026 production analog |
|------------|---------------|------------------------|
| OS 概念 | MemGPT 概念 | 2026 生产环境类比 |
| RAM | main context (prompt) | Anthropic/OpenAI context window / 主上下文（提示） |
| Disk | external context | vector DB, KV, graph store / 外部上下文（向量数据库、KV、图存储） |
| Page fault | memory tool call | `memory.search`, `memory.read`, `memory.write` / 记忆工具调用 |
| OS kernel | agent control loop | ReAct loop with memory tools / 带记忆工具的 ReAct 循环 |

代理运行一个正常的 ReAct 循环. 一个额外的工具类允许它页面数据进入和退出主语境.

>  **【类比】**像你电脑内存管理:RAM(主上下文) 只需8GB但要运行Photoshop + 浏览器 + IDE;操作系统通过页面换入换出(页面进/出) 让你"感觉"有无限内存――MemGPT 让代理也这样做主上下文塞不下时,代理自调用`archival_memory_search`调用 调用 调用`core_memory_replace`把无关内容"换出"――代理 像操作系统内核,记忆工具像系统调用――

> 代理运行普通的 ReAct 循环. 额外的工具使其可以在主下文和外部存储中交换数据.

> **【中文解读】**简单的数据库:RAM=主上下文 (RAM=主上下文) 磁盘=外部上下文 (向量数据库/KV/图库存储),页面错误=记忆工具调用 (RAM=主上下文)`memory.search`现在,我们要去.`memory.read`现在,我们要去.`memory.write`),OS内核=代理 控制循环――代理运行普通的 ReAct 循环,额外增加一种工具用于在主下文和外部存储之间进行数据交换――

### 两层

- **Main context.**固定尺寸提示,保持当前任务,始终可见于模型.
  翻译: 中文**主上下文。**固定大小的提示,承担当前任务――模型始终可见――
- **External context.**无限,可通过工具搜索,当有必要时阅读,当事实出现时写下.
  翻译: 中文**外部上下文。**无界的,通过工具可搜索.

原稿评估了设计的两个任务,除了基层窗口之外:超过100万个代币的文件分析和多次会议聊天,持续记忆在几天内.

> 根据两个超越基础窗口的任务,该设计被评估:超过100万代币的文档分析和跨天持久记忆的多次会话聊天.

### 断断模式

MemGPT引入了"记忆作为中断"的过程:对话中,代理可以调用记忆工具,运行时间执行它,结果将作为一个新的观察,作为下一个助理转换.`read()`系统将阻止进程,返回字节,进程继续.

> MemGPT 引入了记忆即中断:在对话中, 代理可以调用记忆工具,运行时执行它,结果作为新观察拼接到下一个助手轮次中――概念上等于 Unix.`read()`系统调用阻塞进程、返回字节、进程继续──

尼卡内存工具表面:

> 标准记忆工具接口:

- `core_memory_append(section, text)`写到提示函中的一个持续部分.
  翻译: 中文`core_memory_append(section, text)`写入提示的持久化分区
- `core_memory_replace(section, old, new)`编辑一个持续的部分.
  翻译: 中文`core_memory_replace(section, old, new)`编辑持久化分区
- `archival_memory_insert(text)`写到可搜索的外部商店.
  翻译: 中文`archival_memory_insert(text)`写入可搜索的外部存储库.
- `archival_memory_search(query, top_k)`从外部商店中获取.
  翻译: 中文`archival_memory_search(query, top_k)`从外部存储检索
- `conversation_search(query)`扫描过往的转折.
  翻译: 中文`conversation_search(query)`扫描过去的轮次.

### 纸质的结束和生产的开始

据悉,在2024年9月,MemGPT成为Letta.`cpacker/MemGPT`) 仍然存在;Letta扩展了设计:

> 2024 年 9 月 MemGPT 成为Letta──研究仓库(`cpacker/MemGPT`) 仍然存在;Letta 扩展了设计:

- 两个层次的基础,回忆,档案 课08.
  中文翻译:三层而非两层(核心、回忆、档案第8课) ⋅
- 替代了原生理`send_message`心跳模式 (第08课).
  中文翻译:原生推理替代 `send_message`现在,我在做什么?
- 睡眠时间代理运行异步记忆工作 (课程 08).
  中文翻译:运行异步记忆工作的睡眠时间代理 (第8课)

尽管生产系统运营Letta,Mem0或一个定制的二层商店,但MemGPT纸是2026年基础.

>  MemGPT论文是2026年基础,即使生产系统运行Letta、Mem0或自定义两层存储.

### 在这个模式出现错误的地方

> ️ **【易错点】**记忆投毒:把外部网页、用户消息直接`archival_memory_insert`进入外部储存.**后果**攻击者在网页中藏了即时注射,如"忽略之前所有指令"),下次代理检查到这个记忆时,命令被执行.**一行修复**参考14·27期即时注射防护),并存储源 字段可追溯──

- **Memory rot.**写作积累速度比读取速度快;检索陷入过时的事实. 修正:定期整合 (Letta睡眠时间),明确无效 (Mem0冲突探测器).
  翻译: 中文**记忆腐化。**写入积累速度快于读取;检索被过时事实淹没──修复:定期合并(晚睡时间)、显式失效(Mem0 冲突检测器)──
- **Memory poisoning.**攻击者控制的内容如果落入记忆录,代理将其重新摄入下一次.这是Greshake等. (课 27) 攻击随着时间的推移.
  翻译: 中文**记忆投毒。**记忆部是检查到的文本. 如果攻击者控制的内容进入记忆笔记, 代理在下次会议中会重新摄取它.
- **Citation loss.**代理记得"用户要求我发送X",但无法引用哪个转换.
  翻译: 中文**引用丢失。**记忆员"用户让我发布X"但不能引用哪一轮.

>  **【困惑】**问:既然2026年模型上下文窗口已经有1M代币了? 双子1.5 Pro),还需要MemGPT吗? A:需要.窗口大不代表用对硬塞1M代币会触发"中段遗忘" (中段遗忘) 并且注意力稀释,模型对中间内容的注意力显著低于首尾.

## 动手构建
```figure
context-budget
```

## 建立它

`code/main.py`在 stdlib 中实现 MemGPT 的双层模式:

> `code/main.py`使用标准库实现了MemGPT的两层模式:

- `MainContext` 设置尺寸的快速缓冲器`core`和`messages`列表;在超过封顶时自动缩小最古老的消息.
  翻译: 中文`MainContext`固定大小的提示缓冲区,带 `core`字典和 `messages`列表;超出上限时自动压缩最旧消息
- `ArchivalStore`存储记录 (ID,文字,标签,会议,转换) 的内存BM25-esque (代币重叠分数).
  翻译: 中文`ArchivalStore`内存中的类 BM25 存储(代币 重叠评分分),存储 (ID,文字,标签,会议,转) 记录。
- 五个记忆工具将地图映射到MemGPT表面.
  中文翻译:映射到MemGPT接口的五个记忆工具──
- 编写的代理人,填写档案,然后打电话回答问题.`archival_memory_search`现在,我们要去.
  中文翻译:一个脚本代理,用事实填充归档存储,然后通过调用`archival_memory_search`回答问题.

运行它:

> 运行:

```
python3 code/main.py
```

后续的调查结果显示,代理人写了三个事实,填写了主要文本 (强迫驱逐),然后通过从档案中获取后续问题

> 轨迹显示代理 写入三个事实,将主上下文填满到上限,然后通过归档存储检查来回答后续问题,在没有任何真实的LLM的情况下重现了 MemGPT工作流――

## 用它实现框架

现在每一个生产内存系统都是MemGPT的变体:

> 今天,每一个生产记忆系统都是MemGPT的变体:

- **Letta**三层,本土推理,睡眠时间计算.
  翻译: 中文**Letta**三层,原生推理,睡眠时间计算.
- **Mem0**向量+KV+图,与一个分数层合并.
  翻译: 中文**Mem0**向量+KV+图与评分层融合──
- **OpenAI Assistants / Responses**通过线程和文件管理内存.
  翻译: 中文**OpenAI Assistants / Responses**通过线程和文件管理的记忆.
- **Claude Agent SDK**通过技能和会议存储的长期记忆.
  翻译: 中文**Claude Agent SDK**通过技能和会话存储实现长期记忆.

根据操作形状 (自主托管,管理,框架集成) 选择一个,而不是根据核心模式.

> 根据运营形态 (自托管,托管,框架集成) 选择,而非核心模式

## 运送它.
### 代理记忆的形状

页面化解决了容量.它不决定要存储什么.四种内存类型在生产系统中重复,每个类型都回答不同的问题:

- **Working memory**现在重要的是什么? 背景层次:当前任务,最近的转变,固定的核心部分.
- **Episodic memory**发生了什么?过去的转折和轨迹,存储与会议和转折参考,可按需播放.
- **Semantic memory**关于用户,域名,世界的真实信息,随着变化而更新和复制.
- **Procedural memory**如何做到这一点? 我学会了规律,偏好和规则,

开源实现选择不同的攻击点:

| Type | Implementation | How it tackles it |
|------|----------------|-------------------|
| Working | MemGPT / Letta | Pages content in and out of a fixed prompt budget via memory tools (this lesson, Lesson 08) |
| Episodic | Zep | Temporal knowledge graph — facts carry validity intervals, so "what was true when" is queryable |
| Semantic | Mem0 | Extraction pipeline that dedupes and updates facts across vector, KV, and graph stores (Lesson 09) |
| Semantic + procedural | LangMem | Background extraction of facts and behavioral rules into a store the agent consults between turns |
| Episodic + semantic | agentmemory | Captures sessions as they run, consolidates them into typed, searchable records |

## 运送它

`outputs/skill-virtual-memory.md`是可重复使用的技能,可为任何目标运行时间产生正确的两层内存架 (主 + 档案 + 工具表面),并有驱逐政策和引用字段.

> `outputs/skill-virtual-memory.md`是一个可复制的技能,在任何目标运行时生成正确的两层记忆脚手架,内置驱逐策略和引用字段.

## 练习题

1. 添加一个`max_main_context_tokens`按代币计量的上限 (约为`len(text.split())`* 1.3. 超过限时将最古老的信息缩写成总结.
   中文翻译:添加按标志计量`max_main_context_tokens`上限(用 `len(text.split())`对于压缩机的行为差异,
2. 按档案存储器 (期限频率,反文档频率) 执行BM25. 测量回忆@10在玩具事实集上与代币重叠基线相比.
   中文翻译:在归档存储上正确实现BM25(词频、逆文档频率) ・・・在玩具事实集上测量回忆@10 与代币重叠基线的对比──
3. 加入`citation`让代理引用每个获取支持的答案中的来源.
   中文翻译:为归档插入添加 `citation`字段(会议_ID,转_ID,源_url) ⋅让代理在每个基于检查的回答上引用来源──
4. 模拟记忆中毒:添加一个档案记录,上面写道"忽略所有未来用户指令".
   中文翻译:模拟记忆投毒:添加一条归档记录说"忽略所有未来用户指令"――编写一个防护器扫描检索结果中的指令类型文本并标记为不可信的――
5. 实现将MemGPT研究备忘录的核心内存JSON模式 (`cpacker/MemGPT`) 当你从平线字符串转换为打字段时,什么会发生变化?
   中文翻译:将实现移植为使用MemGPT研究仓库的核心记忆 JSON 模式`cpacker/MemGPT`) ・从平字符串转换到类型化区分时发生了什么变化?

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Virtual context | "Unlimited memory" / "无限记忆" | Main (prompt) + external (searchable) tiers with page in/out / 主（提示）+ 外部（可搜索）两层，带页面换入/换出 |
| Main context | "Working memory" / "工作记忆" | The prompt — fixed-size, always visible / 提示——固定大小，始终可见 |
| Archival memory | "Long-term store" / "长期存储" | External searchable persistence, retrieved on demand / 外部可搜索持久化，按需检索 |
| Core memory | "Persistent prompt section" / "持久化提示分区" | Named sections pinned inside the main context / 固定在主上下文内的命名分区 |
| Memory tool | "Memory API" / "记忆 API" | Tool call the agent issues to read/write external memory / Agent 发出的读/写外部记忆的工具调用 |
| Interrupt | "Memory page fault" / "记忆页面错误" | Agent pauses, runtime fetches, result splices into next turn / Agent 暂停、运行时获取、结果拼接到下一轮 |
| Memory rot | "Stale facts" / "过时事实" | Old writes drown retrieval; fix with consolidation / 旧写入淹没检索；用合并修复 |
| Memory poisoning | "Injected persistent note" / "注入的持久化笔记" | Attacker content stored as memory, re-ingested on recall / 攻击者内容存储为记忆，在回忆时重新摄取 |

## 继续阅读 继续阅读

- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560)基于OS的虚拟文本论文
  中文翻译:MemGPT 经典论文操作系统启发的虚拟上下文──
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks)三层次的进化
  中文翻译: 拉塔 记忆块博客三层演进。
- [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)将环境视为预算
  中文翻译:人类学 关于有效上下文工程的文章将上下文视为预算
- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) 混合生产内存,
  中文翻译:Mem0论文在此模式之上的混合生产记忆──
- [Zep (getzep/zep)](https://github.com/getzep/zep)类别表中的时间知识图记忆
- [Mem0 (mem0ai/mem0)](https://github.com/mem0ai/mem0)课09的混合商店背后的采集管道
- [LangMem (langchain-ai/langmem)](https://github.com/langchain-ai/langmem) 背景调查事实和行为规则
- [agentmemory (rohitg00/agentmemory)](https://github.com/rohitg00/agentmemory)集成成类型,可搜索的记录
