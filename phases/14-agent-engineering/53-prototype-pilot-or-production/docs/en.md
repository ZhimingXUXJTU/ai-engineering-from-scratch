# Choose Prototype, Pilot, or Production Deliberately | 原型、试点还是生产：三档慎选

> These are different learning environments, not levels of polish. Choose the stage that answers the current unknown with the least unnecessary consequence.

> **【中文解读】** 原型、试点、生产是三种不同的学习环境，不是打磨程度的三档。选档标准只有一个：哪一个能以最小的不必要后果回答当前的未知。本课把第 50-52 课的"切片、规格、指标"接上最后一环——环境控制：原型可以随时扔，试点必须有界且可回退，生产意味着组织接受了持续责任。最容易发生的事故不是选错了档，而是原型"悄悄地"变成了生产系统。

> 🔗 **【前置】** 学本课前请先掌握：Phase 14 第 50 课（最小切片——先确定要证明什么）、第 51 课（规格契约——控制与证明条款）和第 52 课（成功指标——每档的证据闸门）。本课产出的 `outputs/stage-decisions.json` 是第 54 课反馈棘轮的运营基线。

**Type:** Learn + Build | **类型:** 学习 + 动手实践
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 14 lessons 50 to 52 | **前置知识:** Phase 14 第 50-52 课
**Time:** ~70 minutes | **时间:** 约 70 分钟

## Learning Objectives | 学习目标

- Choose a build stage from the unknown, audience, data, consequence, and readiness.
  中文翻译：根据未知项、受众、数据、后果和就绪度选择构建档位。
- Define stage-specific controls and exit criteria.
  中文翻译：定义档位专属的控制措施和退出标准。
- Prevent prototypes from quietly becoming production systems.
  中文翻译：防止原型悄悄变成生产系统。
- Delay real authority until evidence and operations justify it.
  中文翻译：把真实权限推迟到证据与运维能力都配得上它的时候。

## Three Different Questions | 三个不同的问题

| Stage | Primary question |
|---|---|
| Prototype | Can this mechanism produce the evidence at all? |
| Pilot | Does it work safely with a bounded real audience and real conditions? |
| Production | Can we own it continuously at the promised reliability and risk level? |

A prototype can be technically complete and still be disposable. A pilot can use production data while remaining limited in audience and authority. Production begins when the organization accepts ongoing responsibility.

> **【中文解读】** 三档问的是三个不同的问题：原型问"这个机制到底能不能产出证据"，试点问"在一群有界的真实受众和真实条件下它安全吗"，生产问"我们能不能以承诺的可靠性和风险水平持续拥有它"。技术完成度与档位无关——原型可以技术上百分百完成但仍然可弃；生产与部署无关——它始于组织接受持续责任的那一刻。

## Prototype | 原型

Use a prototype when the unknown does not require real users or real data. Keep it:

> 当未知项不需要真实用户或真实数据时，用原型。让它保持：

- discardable;
  中文翻译：随时可扔；
- isolated;
  中文翻译：隔离；
- narrow in behavior;
  中文翻译：行为面窄；
- explicit about the learning question;
  中文翻译：把学习问题写明白；
- free of false operational guarantees.
  中文翻译：不带任何虚假的运维保证。

Do not optimize architecture before the mechanism earns another stage.

> 在这个机制赢得下一个档位之前，不要优化架构。

> **【中文解读】** 原型的五条纪律里最硬的是"隔离"和"不带虚假运维保证"：隔离保证它失败时波及面为零；不承诺可用性则保证没人开始依赖它。最后一句是给工程师的清醒剂——机制本身还没证明价值时，花在架构打磨上的每一小时都是给一个可能要扔掉的东西镀金。

## Pilot | 试点

Use a pilot when the unknown requires real behavior, realistic data, or a real workflow, but consequence or readiness is not yet compatible with broad release.

> 当未知项需要真实行为、真实感的数据或真实工作流，但后果或就绪度还不兼容大范围发布时，用试点。

A pilot needs:

> 试点需要：

- a named audience;
  中文翻译：点名的人群；
- a human owner;
  中文翻译：一位人类负责人；
- bounded duration and authority;
  中文翻译：有界的时长与权限；
- audit and rollback;
  中文翻译：审计与回滚；
- outcome and guardrail thresholds;
  中文翻译：结果与护栏阈值（来自第 52 课）；
- exit criteria for expand, revise, or stop.
  中文翻译：扩展、修订或停止的退出标准。

> **【中文解读】** 试点的定义性特征是"真实但有界"：用真实数据、真实人群，但受众点名、时长封顶、权限收窄。六项要求里"人类负责人"和"退出标准"最常被省略——没有负责人的试点出事时找不到人拍板回滚，没有退出标准的试点会默认无限续期，变成一个半永久的不明物体。

## Production | 生产

Production needs more than deployment:

> 生产需要的比部署多：

- service level objective;
  中文翻译：服务级别目标（SLO）；
- on-call and incident ownership;
  中文翻译：值班与事故归属；
- security and privacy review;
  中文翻译：安全与隐私审查；
- cost and capacity controls;
  中文翻译：成本与容量控制；
- rollback and recovery;
  中文翻译：回滚与恢复；
- continuous monitoring;
  中文翻译：持续监控；
- a retirement path.
  中文翻译：一条退役路径。

```mermaid
flowchart LR
  U[Unknown] --> R{Needs real users or data?}
  R -->|No| P[Prototype]
  R -->|Yes| C{Consequence bounded and operations ready?}
  C -->|No| L[Pilot]
  C -->|Yes| D[Production]
```

> **【中文解读】** 七项里最反直觉的是最后一项"退役路径"：进入生产之前就要写好它怎么退出。这不是悲观，而是承认每个系统都有生命周期——没有退役路径的系统最后都变成了"没人敢动也没人知道为什么在跑"的遗产。决策树的逻辑：不需要真实用户/数据 → 原型；需要但后果未收界或运维未就绪 → 试点；两者皆备 → 生产。

> 💡 **【类比】** 三档像学车的三个阶段：驾校模拟器（原型——撞了重开，零后果）、贴实习牌+老司机陪驾上路（试点——真实道路，但有界、有负责人、随时能接管）、独立跑高速（生产——你独自承担全部责任，车还得年检、上保险）。最危险的不是新手，是开着模拟器以为自己在跑高速的人。

## Stage Drift | 阶段漂移

Prototype code becomes dangerous when it acquires users, data, or authority without acquiring ownership. Mark prototype and pilot boundaries in configuration, access control, telemetry, and documentation. A warning banner is not enough.

> 当原型代码在没有获得归属的情况下获得了用户、数据或权限，它就变得危险。把原型与试点的边界写进配置、访问控制、遥测和文档。一个警告横幅是不够的。

The stage should be observable from the system itself.

> 档位应当能从系统本身被观察出来。

> **【中文解读】** 阶段漂移（stage drift）是最常见的静默事故："临时跑一下"的原型脚本接入了真实流量，三个月后它成了没人敢重启的关键路径。防御必须落在技术控制上——配置里的开关、访问控制里的权限、遥测里的标记——而不是 UI 横幅或口头约定。判断标准很简单：一个新来的工程师能不能不问任何人就看出"这是原型"。

## Build It | 动手实现

The lab chooses a stage from the decision context, returns required controls, and writes `outputs/stage-decisions.json`.

> 实验代码从决策上下文选出档位、返回必需的控制清单，并写出 `outputs/stage-decisions.json`。

```bash
python3 code/main.py
python3 -m unittest discover code/tests -v
```

Change the pilot example to low consequence with operational readiness. Explain what additional evidence would justify production.

> 把试点那个例子改成低后果且运维就绪。解释还需要哪些额外证据才能支撑上生产。

> **【中文解读】** `choose_stage` 的三条分支就是决策树的代码化：不需要真实用户/数据 → prototype；运维未就绪、后果 ≥4 或不可逆 → pilot；其余 → production。课后实验的答案不在代码里：就算判定落到 production，仍然缺证据——比如按 SLO 跑一段时间的实际表现、安全审查通过、值班机制建立。档位判定给的是"最低档约束"，不是"通行证"。

## Exercises | 练习

1. Classify three current projects by learning stage, not deployment status.
   中文翻译：按学习阶段（而非部署状态）给你手头的三个项目分类。
2. Write pilot exit criteria that include a stop decision.
   中文翻译：为试点写包含"停止"决策的退出标准。
3. Add a technical control that prevents a prototype from reaching production data.
   中文翻译：加一条技术控制，阻止原型碰到生产数据。
4. Identify the first operational responsibility that makes the build production.
   中文翻译：指出第一个"接下它，构建就成了生产"的运营责任。
5. Design a rollback receipt for the bounded pilot.
   中文翻译：为有界试点设计一份回滚凭据。

## Further Reading | 延伸阅读

- [Barry Boehm, A Spiral Model of Software Development and Enhancement](https://dl.acm.org/doi/10.1145/12944.12948), for matching each iteration’s commitment to resolved risk.
  中文翻译：Boehm《螺旋模型》——让每一轮迭代的承诺与已解决的风险相匹配。
- [Fagerholm et al., Building Blocks for Continuous Experimentation](https://doi.org/10.1145/2601248.2601276), for the organizational and technical conditions required to run experiments continuously.
  中文翻译：Fagerholm 等《持续实验的构建块》——持续开展实验所需的组织与技术条件。

## What You Keep | 你保留的产出

Keep `outputs/stage-decisions.json`. It records why each stage is justified and which controls must exist before the next one.

> 保留 `outputs/stage-decisions.json`。它记录了每个档位为何成立，以及进入下一档之前必须存在哪些控制。
