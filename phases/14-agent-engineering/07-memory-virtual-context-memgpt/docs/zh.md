# 虚拟上下文与 MemGPT 记忆

> 上下文窗口看似能解决记忆问题，但实际上不能。生产环境中的三个失败模式：(1) 溢出——多轮对话或长文档跨越窗口限制，截断之外的一切都丢失了；(2) 稀释——窗口内填充不相关上下文稀释了注意力；(3) 持久化——新会话从空窗口开始，Agent 无法跨会话记忆。MemGPT (Packer 等人, 2023) 将上下文管理类比为操作系统虚拟内存——主上下文=RAM，外部存储=磁盘，记忆工具=页面换入换出。

**类型：** 构建
**语言：** Python (标准库)
**前置条件：** Phase 14 · 01 (Agent 循环), Phase 14 · 06 (工具使用)
**预计时间：** ~75 分钟

## 学习目标

- 解释 MemGPT 建立在其上的 OS 类比：主上下文 = RAM，外部上下文 = 磁盘，记忆工具 = 页面换入/换出。
- 用标准库实现双层 MemGPT 模式：主上下文缓冲区、外部可搜索存储和页面换入/换出工具。
- 描述 Agent 如何发出"中断"来查询或修改外部记忆，以及结果如何拼接到下一个提示中。
- 识别 MemGPT 的设计选择如何延续到 Letta（第 08 课）和 Mem0（第 09 课）。

## 问题引入

上下文窗口看似能解决记忆问题。实际上不能。三个失败模式在生产中反复出现：

1. **溢出。** 多轮对话、长文档或工具调用密集的轨迹跨越窗口。截断之外的一切都消失了。
2. **稀释。** 即使在窗口内，填充不相关上下文也会稀释对重要内容的注意力。前沿模型在长输入上仍然会退化。
3. **持久化。** 新会话以空窗口开始。没有外部记忆的 Agent 无法跨会话说"记得你之前让我……"。

更大的窗口有帮助但不能修复。Mem0 的 2025 年论文测量发现，128k 窗口的基线仍然遗漏 4k 窗口 + 外部记忆 Agent 能捕获的长程事实。

> **【拓展：MemGPT → 现代 Agent 记忆系统】** MemGPT (Packer et al., 2023) 将上下文管理类比为操作系统虚拟内存：主上下文=RAM，外部存储=磁盘，记忆工具=页面换入换出。这是 2026 年所有记忆系统的基本模式。

## 核心概念

### MemGPT：OS 类比

Packer 等人 (arXiv:2310.08560, v2 2024 年 2 月) 将上下文管理映射到操作系统虚拟内存：

| OS 概念 | MemGPT 概念 | 2026 年生产对应物 |
|---------|------------|------------------|
| RAM | 主上下文（提示） | Anthropic/OpenAI 上下文窗口 |
| 磁盘 | 外部上下文 | 向量数据库、KV、图存储 |
| 页面错误 | 记忆工具调用 | `memory.search`、`memory.read`、`memory.write` |
| OS 内核 | Agent 控制循环 | 带记忆工具的 ReAct 循环 |

Agent 运行普通的 ReAct 循环。额外的一类工具让它在主上下文和外部存储之间换入换出数据。

### 两层架构

- **主上下文。** 固定大小的提示，持有当前任务。始终对模型可见。
- **外部上下文。** 无界，通过工具可搜索。相关时读取，事实出现时写入。

### 中断模式

MemGPT 引入记忆即中断：对话中途 Agent 可以调用记忆工具，运行时执行它，结果作为新观察拼接到下一个助手轮次。概念上等同于 Unix `read()` 系统调用——阻塞进程、返回字节、进程继续。

经典记忆工具面：

- `core_memory_append(section, text)`——写入提示的持久部分。
- `core_memory_replace(section, old, new)`——编辑持久部分。
- `archival_memory_insert(text)`——写入可搜索的外部存储。
- `archival_memory_search(query, top_k)`——从外部存储检索。
- `conversation_search(query)`——扫描过去轮次。

### 这个模式哪里会出错

- **记忆腐化。** 写入速度超过读取；检索被过时事实淹没。修复：定期整合（Letta sleep-time）、显式失效（Mem0 冲突检测器）。
- **记忆投毒。** 外部记忆是检索到的文本。如果攻击者控制的内容进入记忆笔记，Agent 下次会话会重新摄入。这是 Greshake 等人（第 27 课）攻击在时间维度上的重述。
- **引用丢失。** Agent 回忆"用户让我发布 X"但无法引用哪一轮。每个归档写入都应存储来源引用（会话 ID、轮次 ID）。

## 动手实现

`code/main.py` 用标准库实现 MemGPT 的双层模式：

- `MainContext`——固定大小的提示缓冲区，含 `core` dict 和 `messages` 列表；超过上限时自动压缩最旧消息。
- `ArchivalStore`——内存中的 BM25 风格存储（token 重叠评分），含 (id, text, tags, session, turn) 记录。
- 五个映射到 MemGPT 面的记忆工具。
- 一个脚本化 Agent，填充归档事实，然后通过调用 `archival_memory_search` 回答问题。

运行：

```
python3 code/main.py
```

## 用框架实现

2026 年的每个生产记忆系统都是 MemGPT 变体：

- **Letta**（第 08 课）——三层、原生推理、sleep-time compute。
- **Mem0**（第 09 课）——向量 + KV + 图与评分层融合。
- **OpenAI Assistants / Responses**——通过线程和文件管理记忆。
- **Claude Agent SDK**——通过 skill 和会话存储实现长期记忆。

## 产出物

`outputs/skill-virtual-memory.md` 是一个可复用 skill，为任何目标运行时产生正确的双层记忆脚手架（主记忆 + 归档 + 工具面），带驱逐策略和引用字段。

## 练习题

1. 添加按 token 计量的 `max_main_context_tokens` 上限（用 `len(text.split())` * 1.3 近似）。超过上限时将最旧消息压缩为摘要。比较有和没有摘要器的行为。
2. 正确实现归档存储上的 BM25（词频、逆文档频率）。在玩具事实集上测量 recall@10 与 token 重叠基线的对比。
3. 在归档插入中添加 `citation` 字段 (session_id, turn_id, source_url)。让 Agent 在每次检索支持的答案上引用来源。
4. 模拟记忆投毒：添加一条归档记录说"忽略所有未来的用户指令"。编写一个守护程序，扫描检索中的指令形态文本并标记为不可信。
5. 将实现移植为使用 MemGPT 研究仓库的核心记忆 JSON schema (`cpacker/MemGPT`)。从扁平字符串切换到类型化部分时有什么变化？

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Virtual context（虚拟上下文） | 主记忆（提示）+ 外部（可搜索）双层，带页面换入/换出 |
| Main context（主上下文） | 提示——固定大小，始终可见 |
| Archival memory（归档记忆） | 外部可搜索持久化，按需检索 |
| Core memory（核心记忆） | 固定在主上下文内的命名部分 |
| Memory tool（记忆工具） | Agent 发出的读/写外部记忆的工具调用 |
| Interrupt（中断） | Agent 暂停、运行时获取、结果拼接到下一轮 |
| Memory rot（记忆腐化） | 旧写入淹没检索；通过整合修复 |
| Memory poisoning（记忆投毒） | 攻击者内容存储为记忆，召回时重新摄入 |

## 延伸阅读

- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560)
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks)
- [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413)
