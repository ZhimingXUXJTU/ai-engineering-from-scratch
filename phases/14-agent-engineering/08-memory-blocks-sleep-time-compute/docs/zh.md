# 记忆块与休眠计算 (Letta)

> MemGPT 在 2024 年成为 Letta。2026 年的演进增加了两个想法：模型可直接编辑的离散功能记忆块，以及在主 Agent 空闲时异步整合记忆的休眠 Agent。这是你将记忆扩展到单次对话之外的方式。

**类型：** 构建
**语言：** Python (标准库)
**前置条件：** Phase 14 · 07 (MemGPT)
**预计时间：** ~75 分钟

## 学习目标

- 说出 Letta 使用的三个记忆层（核心 core、回忆 recall、归档 archival）及各自的作用。
- 解释记忆块模式：Human 块、Persona 块和用户自定义块作为一等类型化对象。
- 描述休眠计算是什么，为什么它在关键路径之外，以及为什么可以使用比主 Agent 更强的模型。
- 实现一个脚本化的双 Agent 循环：主 Agent 提供响应，休眠 Agent 在轮次间整合块。

## 问题引入

MemGPT（第 07 课）解决了虚拟内存控制流。出现了三个生产问题：

1. **延迟。** 每个记忆操作都在关键路径上。如果 Agent 在用户等待时必须修剪、摘要或协调，尾部延迟会爆炸。
2. **记忆腐化。** 写入不断积累。矛盾的事实留下。检索被过时内容淹没。
3. **结构丢失。** 扁平的归档存储无法表达"Human 块始终在提示中；Persona 块始终在提示中；Task 块按会话切换"。

> **【中文解读】** 记忆块（Memory Blocks）和休眠计算（Sleep-Time Compute）是 MemGPT/Letta 的两种优化策略。记忆块是固定大小的上下文分区，类似于内存页，用于精细控制上下文窗口中各类信息的占比。休眠计算利用空闲时间做记忆整理和预计算，类似于操作系统的后台内存整理。

Letta (letta.com) 是 2026 年的重写。记忆块使结构显式；休眠计算将整合移出关键路径。

## 核心概念

### 三层架构

| 层级 | 范围 | 存储位置 | 写入者 |
|------|------|---------|--------|
| 核心 (Core) | 始终可见 | 主提示内部 | Agent 工具调用 + 休眠时重写 |
| 回忆 (Recall) | 对话历史 | 可检索 | 自动轮次日志 |
| 归档 (Archival) | 任意事实 | 向量 + KV + 图 | Agent 工具调用 + 休眠时摄入 |

### 记忆块

块是核心层中类型化的、持久的、可编辑的部分。原始 MemGPT 论文定义了两个：

- **Human 块**——关于用户的事实（姓名、角色、偏好、目标）。
- **Persona 块**——Agent 的自我概念（身份、语调、约束）。

Letta 泛化为任意用户定义块：当前目标的 `Task` 块、代码库事实的 `Project` 块、硬约束的 `Safety` 块。每个块有 `id`、`label`、`value`、`limit`（字符上限）、`description`（让模型知道何时编辑它）。

### 休眠计算

2025 年 Letta 的添加：在后台运行第二个 Agent，不在关键路径上。休眠 Agent 处理对话转录和代码库上下文，将 `learned_context` 写入共享块，并整合或使归档记录失效。

自然产生的特性：

- **无延迟成本。** 主响应不等待记忆操作。
- **允许更强模型。** 休眠 Agent 可以使用更昂贵、更慢的模型，因为不受延迟约束。
- **自然整合窗口。** 在用户不等待时去重、摘要、使矛盾事实失效。

### 这个模式哪里会出错

- **块膨胀。** 无限的 `block_append` 很快达到上限。在写入即将超出上限之前连接块摘要器。
- **静默漂移。** 休眠 Agent 重写块，主 Agent 从未注意到。对块进行版本控制并在追踪中显示差异。
- **投毒的整合。** 休眠 Agent 将攻击者可达内容处理到核心中。第 27 课同样适用于休眠面。

## 动手实现

`code/main.py` 实现：

- `Block`——id, label, value, limit, description。
- `BlockStore`——CRUD + `near_limit(label)` 辅助。
- 两个脚本化 Agent——`PrimaryAgent` 提供一轮对话，`SleepTimeAgent` 在轮次间整合。
- 展示三轮对话带块写入加上休眠整合的轨迹。

运行：

```
python3 code/main.py
```

## 用框架实现

- **Letta** (letta.com) 参考实现。自托管或托管云。
- **Claude Agent SDK skills** 作为块形知识——skill 是一个命名的、版本化的、可检索的指令块，Agent 按需加载。
- **自定义构建**——需要控制存储后端的团队。使用 Letta API 契约以便日后迁移。

## 产出物

`outputs/skill-memory-blocks.md` 为任何运行时生成 Letta 形状的块系统，带休眠钩子、安全规则和引用连线。

## 练习题

1. 添加 `block_summarize` 工具，在 `near_limit` 返回 true 时用模型生成的摘要替换块值。什么触发阈值最小化摘要调用和块溢出？
2. 实现归档的休眠时去重：token 重叠 >90% 的两条记录合并为一条。只在休眠整合中做，从不在关键路径上。
3. 对块进行版本控制。每次写入记录旧值和差异。暴露 `block_history(label)` 让运维可以调试"Agent 为什么忘了 X"。
4. 将休眠 Agent 视为不可信写入者。当它们触碰 Persona 或 Safety 块时，提交前需要第二 Agent 审查。
5. 将示例移植为使用 Letta API (`letta_v1_agent`)。块 schema 有什么变化，原生推理如何改变追踪形状？

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Memory block（记忆块） | 类型化的、持久的、LLM 可编辑的核心记忆段 |
| Human block（Human 块） | 关于用户的事实，固定在核心中 |
| Persona block（Persona 块） | 自我概念、语调、约束，固定在核心中 |
| Sleep-time compute（休眠计算） | 第二个 Agent 在关键路径之外做整合 |
| Core / Recall / Archival | 三层记忆分裂：始终可见 / 对话 / 外部 |
| Block limit（块上限） | 每块的字符限制；强制摘要 |
| Native reasoning（原生推理） | 提供商级推理输出，非提示级 `Thought:` |
| Learned context（学习上下文） | 休眠 Agent 写入共享块的事实 |

## 延伸阅读

- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks)
- [Letta, Sleep-time Compute blog](https://www.letta.com/blog/sleep-time-compute)
- [Letta, Rearchitecting the Agent Loop](https://www.letta.com/blog/letta-v1-agent)
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560)
