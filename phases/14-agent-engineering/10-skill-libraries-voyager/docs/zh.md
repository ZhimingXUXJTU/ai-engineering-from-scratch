# 技能库与终身学习 (Voyager)

> Voyager (Wang 等人, TMLR 2024) 将可执行代码视为技能。技能是命名的、可检索的、可组合的、由环境反馈精炼的。这是 Claude Agent SDK skills、skillkit 和 2026 年技能库模式的参考架构。

**类型：** 构建
**语言：** Python (标准库)
**前置条件：** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta 记忆块)
**预计时间：** ~75 分钟

## 学习目标

- 说出 Voyager 的三个组件——自动课程、技能库、迭代提示——及各自的作用。
- 解释为什么 Voyager 将行动空间设为代码而非原始命令。
- 用标准库实现带注册、检索、组合和失败驱动精炼的技能库。
- 将 Voyager 的模式映射到 2026 年 Claude Agent SDK skills 和 skillkit 生态系统。

## 问题引入

在每个会话中从头重建每个能力的 Agent 做错了三件事：

1. **浪费 token。** 每个任务重新引发相同的推理。
2. **丢失进度。** 会话 A 中学到的纠正不会转移到会话 B。
3. **长程组合失败。** 复杂任务需要能力层次结构；一次性提示无法表达。

Voyager 的答案：将每个可复用能力视为存储在库中的命名代码块，按相似度可检索，可与其他技能组合，由执行反馈精炼。

> **【中文解读】** 技能库（Skill Libraries）源自 Voyager (Wang et al., 2023)——一个在 Minecraft 中自主探索和学习的 Agent。Voyager 的核心创新是自动技能发现和存储：Agent 在执行任务时发现有效的操作序列，将其编码为可复用的技能函数存入技能库。

> **【拓展：Voyager 的技能库概念已被 2026 年的编码 Agent 普遍采用。Claude Code 的 CLAUDE.md、Cursor 的 .cursorrules 和 Codex 的技能系统都是这一思想的变体——将有效的操作模式编码为可复用的技能。Voyager 在 Minecraft 中用 160 个自动发现的技能完成了需要人类玩家数小时才能完成的任务。**

## 核心概念

### 三个组件

Voyager (arXiv:2305.16291) 围绕以下结构构建 Agent：

1. **自动课程。** 好奇心驱动的提议器根据 Agent 当前技能集和环境状态选择下一个任务。探索是自下而上的。
2. **技能库。** 每个技能是可执行代码。任务成功时添加新技能。按查询到描述的相似度检索技能。
3. **迭代提示机制。** 失败时，Agent 接收执行错误、环境反馈和自我验证输出，然后精炼技能。

### 行动空间 = 代码

大多数 Agent 发出原始命令。Voyager 发出 JavaScript 函数。一个技能是：

```
async function craftIronPickaxe(bot) {
  await mineIron(bot, 3);
  await mineStick(bot, 2);
  await placeCraftingTable(bot);
  await craft(bot, 'iron_pickaxe');
}
```

由子技能组合。按键为描述和嵌入存储。作为程序而非提示检索。

### 技能检索

新任务"制作钻石镐"。Agent：

1. 嵌入任务描述。
2. 查询技能库获取 top-k 相似技能。
3. 检索 `craftIronPickaxe`、`mineDiamond`、`placeCraftingTable` 等。
4. 从检索到的原语 + 新逻辑组合新技能。

### 迭代精炼

Voyager 的反馈循环：

1. Agent 编写技能。
2. 技能针对环境运行。
3. 三个信号之一返回：`success`、`error`（带堆栈跟踪）、`self-verification failure`。
4. Agent 使用信号作为上下文重写技能。
5. 循环直到成功或最大轮数。

这是 Self-Refine（第 05 课）应用于代码生成，带环境验证。CRITIC（第 05 课）是相同模式，用外部工具作为验证器。

### 这个模式哪里会出错

- **技能库腐化。** 同一技能以略有不同的描述添加了 10 次。写入时添加去重；检索只返回一个。
- **组合技能漂移。** 父技能依赖于被精炼的子技能。对技能进行版本控制；固定在 v1 的父技能不会自动采用 v3。
- **检索质量。** 技能描述上的向量检索在库增长超过几百个时退化。用标签过滤和硬约束补充。

## 动手实现

`code/main.py` 用标准库实现技能库：

- `Skill`——name, description, code (字符串), version, tags, dependencies。
- `SkillLibrary`——register, search (token overlap), compose (依赖的拓扑排序), refine (更新时版本递增)。
- 一个脚本化 Agent 注册三个原语技能，组合第四个，遇到失败并精炼。

运行：

```
python3 code/main.py
```

## 用框架实现

- **Claude Agent SDK skills** (Anthropic)——2026 年参考：每个 skill 有描述、代码和指令；Agent 会话期间按需加载。
- **skillkit** (npm: skillkit)——32+ AI 编码 Agent 的跨 Agent 技能管理。
- **自定义技能库**——领域特定（数据 Agent 的 SQL 技能、基础设施 Agent 的 Terraform 技能）。Voyager 模式可以缩小。
- **OpenAI Agents SDK `tools`**——低端；每个工具是一个轻量级技能。

## 产出物

`outputs/skill-skill-library.md` 为任何目标运行时生成带注册、检索、版本控制和精炼连线的 Voyager 形状技能库。

## 练习题

1. 在 `compose()` 中添加依赖循环检测器。技能 A 依赖 B 依赖 A 时怎么办？错误还是警告？
2. 实现每个技能的版本固定。当父技能组合子技能 `crafting@1` 时，对 `crafting@2` 的精炼不得静默升级父技能。
3. 将 token 重叠检索替换为 sentence-transformers 嵌入（或 BM25 标准库实现）。在 50 个技能的玩具库上测量 retrieval@5。
4. 添加"课程"Agent：给定当前库和领域描述，提出 5 个缺失技能。每周调用一次。
5. 阅读 Anthropic 的 Claude Agent SDK skill 文档。将玩具库移植为 SDK 的 skill schema。可发现性有什么变化？

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Skill（技能） | 命名的代码块 + 描述，按相似度可检索 |
| Skill library（技能库） | 技能的持久存储，可搜索且可组合 |
| Curriculum（课程） | 自下而上的目标生成器，由当前能力差距驱动 |
| Composition（组合） | 技能调用技能；执行时拓扑排序 |
| Iterative refinement（迭代精炼） | 环境反馈 + 错误 + 自验证反馈到下一版本 |
| Action-space-as-code | 发出函数而非原始命令，用于时序扩展行为 |
| Dedup on write（写入去重） | 近重复描述合并为一个规范技能 |

## 延伸阅读

- [Wang et al., Voyager (arXiv:2305.16291)](https://arxiv.org/abs/2305.16291)
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Anthropic, Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651)
