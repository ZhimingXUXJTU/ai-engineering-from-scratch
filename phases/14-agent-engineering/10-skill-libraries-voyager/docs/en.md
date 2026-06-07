# Skill Libraries and Lifelong Learning (Voyager) | 技能库与终身学习（Voyager）

> Voyager (Wang et al., TMLR 2024) treats executable code as a skill. Skills are named, retrievable, composable, and refined by environment feedback. This is the reference architecture for Claude Agent SDK skills, skillkit, and the 2026 skill-library pattern.

> **【中文解读】** Voyager 将可执行代码视为技能。技能是命名的、可检索的、可组合的，并通过环境反馈精炼。这是 Claude Agent SDK skills、skillkit 和 2026 年技能库模式的参考架构。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta Blocks) | **前置知识:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta 块)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Learning Objectives | 学习目标

- Name Voyager's three components — automatic curriculum, skill library, iterative prompting — and the role of each.
  中文翻译：说出 Voyager 的三个组件——自动课程、技能库、迭代提示——及各自的作用。
- Explain why Voyager makes the action space code, not primitive commands.
  中文翻译：解释为什么 Voyager 将动作空间设为代码而非原始命令。
- Implement a stdlib skill library with registration, retrieval, composition, and failure-driven refinement.
  中文翻译：用标准库实现带注册、检索、组合和失败驱动精炼的技能库。
- Map Voyager's pattern onto the 2026 Claude Agent SDK skills and the skillkit ecosystem.
  中文翻译：将 Voyager 模式映射到 2026 年 Claude Agent SDK skills 和 skillkit 生态系统。

## The Problem | 问题引入

Agents that rebuild every capability from scratch in every session do three things wrong:

> 每次会话都从头重建所有能力的 Agent 会做错三件事：

1. **Waste tokens.** Every task re-elicits the same reasoning.
   中文翻译：**浪费 token。** 每个任务都重新引发相同的推理。
2. **Lose progress.** A correction learned in session A doesn't transfer to session B.
   中文翻译：**丢失进展。** 在会话 A 中学到的纠正不会转移到会话 B。
3. **Fail on long-horizon composition.** Complex tasks need capability hierarchies; one-shot prompts cannot express them.
   中文翻译：**在长程组合上失败。** 复杂任务需要能力层次；单次提示无法表达它们。

> **【中文解读】** 技能库（Skill Libraries）源自 Voyager (Wang et al., 2023)——一个在 Minecraft 中自主探索和学习的 Agent。Voyager 的核心创新是自动技能发现和存储：Agent 在执行任务时发现有效的操作序列，将其编码为可复用的技能函数存入技能库。

Voyager's answer: treat each reusable capability as a named chunk of code stored in a library, retrievable by similarity, composable with other skills, and refined by execution feedback.

> Voyager 的答案：将每个可复用能力视为存储在库中的命名代码块，可通过相似性检索，可与其他技能组合，并通过执行反馈精炼。

> **【拓展：Voyager 的技能库概念已被 2026 年的编码 Agent 普遍采用】** Claude Code 的 CLAUDE.md、Cursor 的 .cursorrules 和 Codex 的技能系统都是这一思想的变体——将有效的操作模式编码为可复用的技能。Voyager 在 Minecraft 中用 160 个自动发现的技能完成了需要人类玩家数小时才能完成的任务。

## The Concept | 核心概念

### Three components

Voyager (arXiv:2305.16291) structures an agent around:

> Voyager（arXiv:2305.16291）围绕以下三个组件构建 Agent：

1. **Automatic curriculum.** A curiosity-driven proposer picks the next task based on the agent's current skill set and environment state. Exploration is bottom-up.
   中文翻译：**自动课程。** 好奇心驱动的提议器根据 Agent 当前技能集和环境状态选择下一个任务。探索是自底向上的。
2. **Skill library.** Each skill is executable code. New skills are added when a task succeeds. Skills are retrieved by query-to-description similarity.
   中文翻译：**技能库。** 每个技能是可执行代码。任务成功时添加新技能。通过查询到描述的相似性检索技能。
3. **Iterative prompting mechanism.** On failure, the agent receives execution errors, environment feedback, and self-verification output, then refines the skill.
   中文翻译：**迭代提示机制。** 失败时，Agent 接收执行错误、环境反馈和自我验证输出，然后精炼技能。

The Minecraft evaluation (Wang et al., 2024): 3.3x more unique items, 8.5x faster stone tools, 6.4x faster iron tools, 2.3x longer map traversal versus baselines. The numbers are Minecraft-specific, but the pattern transfers.

> Minecraft 评估（Wang 等人，2024）：3.3 倍更多独特物品、8.5 倍更快石制工具、6.4 倍更快铁制工具、2.3 倍更长地图遍历对比基线。数字是 Minecraft 特定的，但模式可迁移。

### Action space = code

Most agents emit primitive commands. Voyager emits JavaScript functions. A skill is:

> 大多数 Agent 发出原始命令。Voyager 发出 JavaScript 函数。一个技能是：

```
async function craftIronPickaxe(bot) {
  await mineIron(bot, 3);
  await mineStick(bot, 2);
  await placeCraftingTable(bot);
  await craft(bot, 'iron_pickaxe');
}
```

Composed from sub-skills. Stored keyed on description and embedding. Retrieved as a program, not a prompt.

> 由子技能组合而成。以描述和嵌入为键存储。作为程序而非提示检索。

This is the 2026 Claude Agent SDK skill: a named, retrievable chunk of code plus instructions the agent loads on demand.

> 这就是 2026 年 Claude Agent SDK skill：一个命名的、可检索的代码块加上 Agent 按需加载的指令。

### Skill retrieval

New task "make a diamond pickaxe." Agent:

> 新任务"制作钻石镐"。Agent：

1. Embeds the task description.
   中文翻译：嵌入任务描述。
2. Queries the skill library for top-k similar skills.
   中文翻译：查询技能库获取 top-k 相似技能。
3. Retrieves `craftIronPickaxe`, `mineDiamond`, `placeCraftingTable` etc.
   中文翻译：检索 `craftIronPickaxe`、`mineDiamond`、`placeCraftingTable` 等。
4. Composes the new skill from retrieved primitives + new logic.
   中文翻译：从检索到的原语 + 新逻辑组合新技能。

This is the pattern MCP resources (Phase 13) and Agent SDK skills implement: retrieval over a knowledge/code surface, scoped to the current task.

> 这是 MCP 资源（Phase 13）和 Agent SDK skills 实现的模式：在知识/代码表面上检索，限定于当前任务。

### Iterative refinement

Voyager's feedback loop:

> Voyager 的反馈循环：

1. Agent writes a skill.
   中文翻译：Agent 编写技能。
2. Skill runs against the environment.
   中文翻译：技能在环境中运行。
3. One of three signals returns: `success`, `error` (with stack trace), `self-verification failure`.
   中文翻译：三种信号之一返回：`success`、`error`（带堆栈跟踪）、`self-verification failure`。
4. Agent rewrites the skill using the signal as context.
   中文翻译：Agent 使用信号作为上下文重写技能。
5. Loop until success or max rounds.
   中文翻译：循环直到成功或达到最大轮次。

This is Self-Refine (Lesson 05) applied to code generation with environment-grounded verification. CRITIC (Lesson 05) is the same pattern with external tools as the verifier.

> 这是 Self-Refine（第 5 课）应用于带环境锚定验证的代码生成。CRITIC（第 5 课）是用外部工具作为验证器的相同模式。

### Curriculum and exploration

Voyager's curriculum module proposes tasks like "build a shelter near the lake" based on what the agent has and what it has not yet done. The proposer uses the environment state + skill inventory to pick a task just above current capability — the exploration sweet spot.

> Voyager 的课程模块基于 Agent 已有的和尚未完成的内容提出任务，如"在湖边建一个庇护所"。提议器使用环境状态 + 技能清单来选择略高于当前能力的任务——探索的最佳点。

For production agents this translates to a "what's missing" operator: given the current skill library and a domain, what skills are we not yet covering? Teams typically implement this manually as curriculum review.

> 对于生产 Agent，这转化为一个"缺什么"操作器：给定当前技能库和领域，我们还没有覆盖哪些技能？团队通常手动实现为课程审查。

### Where this pattern goes wrong

- **Skill library rot.** Same skill added 10 times with slightly different descriptions. Add deduplication on write; retrieval returns only one.
  中文翻译：**技能库腐化。** 同一技能用略有不同的描述添加 10 次。写入时添加去重；检索只返回一个。
- **Composed-skill drift.** Parent skill depends on a child that was refined. Version skills; a parent pinned to v1 doesn't magically pick up v3.
  中文翻译：**组合技能漂移。** 父技能依赖的子技能被精炼了。版本化技能；固定在 v1 的父技能不会自动获得 v3。
- **Retrieval quality.** Vector retrieval over skill descriptions degrades as the library grows past a few hundred. Supplement with tag filters and hard constraints ("only skills with `category=tooling`").
  中文翻译：**检索质量。** 技能描述上的向量检索在库增长超过几百时退化。用标签过滤器和硬约束补充（"只有 `category=tooling` 的技能"）。

## Build It | 动手构建

`code/main.py` implements a stdlib skill library:

> `code/main.py` 用标准库实现了技能库：

- `Skill` — name, description, code (as string), version, tags, dependencies.
  中文翻译：`Skill`——名称、描述、代码（字符串）、版本、标签、依赖。
- `SkillLibrary` — register, search (token overlap), compose (topological sort of deps), and refine (version bump on update).
  中文翻译：`SkillLibrary`——注册、搜索（token 重叠）、组合（依赖的拓扑排序）和精炼（更新时版本递增）。
- A scripted agent that registers three primitive skills, composes a fourth, hits a failure, and refines.
  中文翻译：注册三个原始技能、组合第四个、遇到失败并精炼的脚本 Agent。

Run it:

> 运行：

```
python3 code/main.py
```

The trace shows library writes, retrieval, composition, a failed execution, and a v2 refinement — Voyager's loop end to end.

> 轨迹显示库写入、检索、组合、一次失败执行和 v2 精炼——Voyager 的端到端循环。

## Use It | 用框架实现

- **Claude Agent SDK skills** (Anthropic) — the 2026 reference: each skill has a description, code, and instructions; loaded on demand during an agent session.
  中文翻译：**Claude Agent SDK skills**（Anthropic）——2026 年参考：每个技能有描述、代码和指令；在 Agent 会话中按需加载。
- **skillkit** (npm: skillkit) — cross-agent skill management for 32+ AI coding agents.
  中文翻译：**skillkit**（npm: skillkit）——32+ AI 编码 Agent 的跨 Agent 技能管理。
- **Custom skill libraries** — domain-specific (SQL skills for data agents, Terraform skills for infra agents). The Voyager pattern scales down.
  中文翻译：**自定义技能库**——领域特定（数据 Agent 的 SQL 技能、基础设施 Agent 的 Terraform 技能）。Voyager 模式可缩小。
- **OpenAI Agents SDK `tools`** — at the low end; each tool is a lightweight skill.
  中文翻译：**OpenAI Agents SDK `tools`**——低端；每个工具是一个轻量级技能。

## Ship It | 产出物

`outputs/skill-skill-library.md` generates a Voyager-shaped skill library with registration, retrieval, versioning, and refinement wired in for any target runtime.

> `outputs/skill-skill-library.md` 生成 Voyager 形状的技能库，内置注册、检索、版本化和精炼，适用于任何目标运行时。

## Exercises | 练习题

1. Add a dependency-cycle detector to `compose()`. What happens when skill A depends on B which depends on A? Error vs warning?
   中文翻译：在 `compose()` 中添加依赖循环检测器。技能 A 依赖 B，B 依赖 A 时会发生什么？错误还是警告？
2. Implement per-skill version pinning. When a parent skill composes child `crafting@1`, a refinement to `crafting@2` must not silently upgrade the parent.
   中文翻译：实现按技能版本固定。当父技能组合子技能 `crafting@1` 时，`crafting@2` 的精炼不能静默升级父技能。
3. Replace token-overlap retrieval with sentence-transformers embeddings (or a BM25 stdlib impl). Measure retrieval@5 on a 50-skill toy library.
   中文翻译：将 token 重叠检索替换为 sentence-transformers 嵌入（或 BM25 标准库实现）。在 50 技能玩具库上测量 retrieval@5。
4. Add a "curriculum" agent: given the current library and a domain description, propose 5 missing skills. Call it weekly.
   中文翻译：添加"课程"Agent：给定当前库和领域描述，提出 5 个缺失技能。每周调用一次。
5. Read Anthropic's Claude Agent SDK skill docs. Port the toy library to the SDK's skill schema. What changes about discoverability?
   中文翻译：阅读 Anthropic 的 Claude Agent SDK skill 文档。将玩具库移植为 SDK 的 skill 模式。可发现性有什么变化？

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Skill | "Reusable capability" / "可复用能力" | Named chunk of code + description, retrievable by similarity / 命名的代码块 + 描述，可按相似性检索 |
| Skill library | "Agent memory of how-to" / "Agent 的操作记忆" | Persistent store of skills, searchable and composable / 技能的持久化存储，可搜索可组合 |
| Curriculum | "Task proposer" / "任务提议器" | Bottom-up goal generator driven by current capability gap / 由当前能力差距驱动的自底向上目标生成器 |
| Composition | "Skill DAG" / "技能 DAG" | Skills invoking skills; topologically sorted on execution / 技能调用技能；执行时拓扑排序 |
| Iterative refinement | "Self-correcting loop" / "自我纠错循环" | Env feedback + errors + self-verification fold back into the next version / 环境反馈+错误+自我验证反馈到下一版本 |
| Action-space-as-code | "Programmatic actions" / "编程式动作" | Emit functions, not primitive commands, for temporally extended behavior / 发出函数而非原始命令，用于时间扩展行为 |
| Dedup on write | "Skill collapse" / "技能合并" | Near-duplicate descriptions collapse to one canonical skill / 近似重复描述合并为一个规范技能 |

## Further Reading | 延伸阅读

- [Wang et al., Voyager (arXiv:2305.16291)](https://arxiv.org/abs/2305.16291) — the original skill-library paper
  中文翻译：Voyager 原始技能库论文。
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) — skills as the 2026 productization
  中文翻译：Claude Agent SDK 概览——2026 年产品化的技能。
- [Anthropic, Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) — skills and subagents in practice
  中文翻译：Anthropic 关于用 Claude Agent SDK 构建 Agent 的文章——实践中的技能和子代理。
- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) — the refinement loop underneath Voyager
  中文翻译：Self-Refine 论文——Voyager 底层的精炼循环。
