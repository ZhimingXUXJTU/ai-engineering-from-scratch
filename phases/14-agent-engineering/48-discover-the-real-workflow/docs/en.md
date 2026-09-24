# Discover the Workflow People Actually Perform | 发现真实工作流

> Requirements are not waiting in a meeting to be collected. They are scattered across actions, workarounds, records, and disagreements.

> **【中文解读】** 需求不是躺在会议里等人来收的，而是散落在动作、绕行办法、记录和分歧里。本课教你从「现在真实发生什么」出发做工作流发现：给每个步骤建模（行动者、触发、动作、输入输出、摩擦、权限、证据），给证据分级（直接观察 > 产物 > 口述 > 推断），并保住分歧而不是把它平均掉。这是「塑造构建」路径的第二课。

> 🔗 **【前置】** 学本课前请先掌握 Phase 14 第 47 课（结果先于产出——本课检验的正是那个结果框架：期望的结果必须落在人们实际执行的工作流里，而不是想象的工作流里）。本课产出 `outputs/workflow-evidence.json`，下一课会把观察到的摩擦与不确定性变成一张假设地图。

**Type:** Learn + Build | **类型:** 学习 + 动手实践
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 14 lesson 47 | **前置知识:** Phase 14 第 47 课
**Time:** ~70 minutes | **时间:** 约 70 分钟

## Learning Objectives | 学习目标

- Model the current workflow as ordered actions with evidence.
  中文翻译：把当前工作流建模为带证据的有序动作。
- Separate direct observation from reported or inferred behavior.
  中文翻译：把直接观察与口述、推断的行为区分开。
- Locate friction, handoffs, authority, and hidden state.
  中文翻译：定位摩擦、交接、权限和隐藏状态。
- Keep uncertain claims visible instead of turning them into requirements.
  中文翻译：让不确定的断言保持可见，而不是把它们变成需求。

## Start with the Current System | 从当前系统出发

Do not begin by asking what features people want. Begin by reconstructing what happens now.

> 不要一上来就问人们想要什么功能。先重建现在正在发生什么。

For each step, record:

> 对每个步骤，记录：

| Field | Example |
|---|---|
| Actor | On-call engineer |
| Trigger | Production alert arrives |
| Action | Opens alert, then searches dashboards |
| Input | Alert payload and deployment record |
| Output | Candidate service and owner |
| Friction | Context switching across three tools |
| Authority | Incident commander approves a write |
| Evidence | Screen recording, incident log, runbook |

The workflow is larger than the screen. It includes waiting, copy-paste, side channels, approval, error recovery, and the steps people have stopped noticing.

> 工作流比屏幕大。它包括等待、复制粘贴、小道消息、审批、错误恢复，以及那些人们已经不再注意到的步骤。

> **【中文解读】** 起点决定质量：从「想要什么」出发得到的是愿望清单，从「现在怎么做」出发得到的才是约束清单。八个字段里 Friction（摩擦）、Authority（权限）、Evidence（证据）最容易被漏记——摩擦是改进机会所在，权限是 AI 能不能动手的边界，证据决定这条记录可信到什么程度。最后一句点破常见盲区：屏幕外的等待、粘贴、群聊、救火才是工作流的血肉。

## Evidence Has Strength | 证据有强弱

Use a simple evidence ladder:

> 用一个简单的证据阶梯：

1. **Direct behavior:** observation, trace, recording, or system event.
   中文翻译：**直接行为：** 观察、trace、录屏或系统事件。
2. **Artifact:** ticket, runbook, log, form, or completed output.
   中文翻译：**产物：** 工单、运维手册、日志、表单或已完成的作品。
3. **Reported behavior:** a person describes what they do.
   中文翻译：**口述行为：** 某人描述自己怎么做。
4. **Inference:** the team concludes what probably happens.
   中文翻译：**推断：** 团队推断大概发生了什么。

All four can be useful. Only the first two prove current behavior directly. Label the rest so confidence does not silently inflate.

> 四级都可能有用，但只有前两级能直接证明当前行为。给其余的贴上标签，免得置信度悄悄膨胀。

> **【中文解读】** 证据阶梯是本课的度量衡：同一句「值班工程师先查仪表盘」，直接观察到的、工单里留痕的、本人说的、团队猜的，可信度差好几档。口述和推断并非不能用，但必须打上标签——否则它们会在转述两三次后被当成事实，工作流模型的地基就这样悄悄注水。

> 💡 **【类比】** 证据阶梯像新闻信源分级。之前：会议纪要里「大家都这么干」和录屏观察写得一样理直气壮；之后：每条记录带等级标签——直接观察是第一手信源，口述是当事人回忆，推断是编辑推测，置信度不再悄悄膨胀。

```mermaid
flowchart TD
  T[Trigger] --> A1[Actor action]
  A1 --> H[Handoff]
  H --> A2[Next actor action]
  A2 --> O[Outcome]
  E1[Direct evidence] -.supports.-> A1
  E2[Artifact] -.supports.-> H
  E3[Reported behavior] -.supports.-> A2
```

> 图解：触发 → 行动者动作 → 交接 → 下一个行动者动作 → 结果；不同强度的证据（直接证据、产物、口述）分别支撑不同的步骤。

## Search for Four Things | 搜索四样东西

- **Friction:** repeated effort, delay, re-entry, or recovery.
  中文翻译：**摩擦：** 重复劳动、延迟、重新录入或恢复补救。
- **Hidden state:** facts carried in memory, chat, or personal notes.
  中文翻译：**隐藏状态：** 靠记忆、聊天记录或个人笔记携带的事实。
- **Authority:** the person or system allowed to make a consequential change.
  中文翻译：**权限：** 被允许做出有后果变更的人或系统。
- **Exceptions:** the case where the normal workflow stops being normal.
  中文翻译：**例外：** 正常工作流不再正常的那些情形。

AI features often fail at handoffs and exceptions because the happy path was the only path shaped.

> AI 功能常常死在交接和例外上，因为当初只塑造了顺利路径（happy path）。

> **【中文解读】** 这四样是工作流里的高价值目标：摩擦指示改进点；隐藏状态是自动化的最大障碍（机器读不到脑子和私聊里的东西）；权限决定哪里必须留人工检查点；例外是「演示环境正常、生产环境翻车」的常见根源。最后一句值得抄下来——只按 happy path 设计的 AI 功能，在第一次交接或第一个例外处就会暴露。

## Do Not Average Away Disagreement | 不要把分歧平均掉

Two users can perform different workflows for good reasons. Preserve the variants until you understand whether they represent:

> 两个用户可能在执行不同的工作流，而且各有正当理由。保留这些变体，直到你弄清它们代表的是：

- different roles;
  中文翻译：不同的角色；
- different risk levels;
  中文翻译：不同的风险等级；
- legacy and current process;
  中文翻译：旧流程与新流程并存；
- expertise differences;
  中文翻译：熟练度差异；
- a genuine policy disagreement.
  中文翻译：一场真正的政策分歧。

An averaged workflow can describe nobody.

> 一个被平均过的工作流可能谁也描述不了。

> **【中文解读】** 把两个变体合成一个「平均工作流」是最省事也最危险的做法：它描述的是一个不存在的用户。五种原因对应五种完全不同的后续动作——分角色建模、分风险建模、流程迁移、培训、上报决策——所以分歧必须原样保留到弄清原因之后。

## Build It | 动手实现

The lab stores evidence on every workflow step, validates ordering and confidence, calculates the direct-evidence ratio, and writes `outputs/workflow-evidence.json`.

> 实验部分会给每个工作流步骤存证据、校验顺序与置信度、计算直接证据占比，并写出 `outputs/workflow-evidence.json`。

```bash
python3 code/main.py
python3 -m unittest discover code/tests -v
```

Add an exception path in which the deployment record is missing. Keep the main order intact and record where the branch begins.

> 加一条「部署记录缺失」的例外路径。保持主顺序不变，记录分支从哪里开始。

> **【中文解读】** 破坏实验练的是例外建模：主流程保持线性，例外作为带自己证据的分支挂上去，而不是塞进某个主步骤的注释里。「直接证据占比」这个指标也值得留意——它量化了整个模型里到底有多少步骤真的被观察过。

## Exercises | 练习

1. Reconstruct one workflow from a log without interviewing anyone.
   中文翻译：不访谈任何人，只从一条日志重建工作流。
2. Interview a user and mark every claim that still lacks direct evidence.
   中文翻译：访谈一位用户，标记每一条仍然缺少直接证据的断言。
3. Add one authority boundary and one failure-recovery step.
   中文翻译：加一个权限边界和一条失败恢复步骤。
4. Model two workflow variants without merging them.
   中文翻译：建模两条工作流变体，不合并它们。
5. Identify a proposed feature that removes a visible step but leaves hidden work untouched.
   中文翻译：找一个「砍掉了看得见的步骤、却没碰隐藏工作」的提议功能。

## Further Reading | 延伸阅读

- [Nuseibeh and Easterbrook, Requirements Engineering: A Roadmap](https://www.cs.toronto.edu/~sme/papers/2000/ICSE2000.pdf), especially its treatment of elicitation as interpretation, modelling, and validation rather than simple capture.
  中文翻译：Nuseibeh 与 Easterbrook《需求工程：路线图》——特别是把需求获取看作解释、建模与验证，而不是简单采集。
- [Gotel and Finkelstein, An Analysis of the Requirements Traceability Problem](https://doi.org/10.1109/ICRE.1994.292398), for the difficulty of preserving the relationship between requirements and their sources.
  中文翻译：Gotel 与 Finkelstein《需求可追踪性问题分析》——保留需求与其来源之间关系的困难。

## What You Keep | 你保留的产出

Keep `outputs/workflow-evidence.json`. It turns observed friction and uncertainty into an assumption map in the next lesson.

> 保留 `outputs/workflow-evidence.json`。下一课会把观察到的摩擦与不确定性变成一张假设地图。
