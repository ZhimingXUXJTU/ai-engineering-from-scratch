# 开发 推进 评估

> 国际娱乐平台注册平台"在线娱乐平台注册平台"在线娱乐平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册平台注册

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** All of Phase 14. | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

>  **【前置】**学本节前请先掌握:阶段14·01-29 全部本节是阶段14的综合应用.还需要阶段11·10的基础.

## 学习目标

- 列出三个评估层静态基准,定制离线,在线生产以及每个层的目的.
- 解释评估者-优化器紧密循环.
- 描述2026年最佳实践:评估在代码旁边进行,运行在CI中,关口 PR.
- 连接每个阶段14课程到它生成的评估案例.

## 问题 问题引入

代理通过演示.他们无法预测的方法无法生产.基准答案是"这个模型是否广泛的?"而不是"这个代理是否为我的产品发送正确的补丁?"答案是:在三个层次的评估,连续运行,每个防护和学习规则都被映射到一个评估案例.

>  **【类比】**经理评价运动员做体检3个层次:**静态基准**平均水平比国家体能测试;**定制离线 eval**项目设计的成功率 (如"修这种错误") =队内训练赛;**在线生产 eval**只有看基准会过适合,只看生产反周期太长.

> ️ **【易错点】**经纪人评价的3个坑:**只测 happy path**eval 集全是简单查询,复杂情况没覆盖;务必构建对抗性测试(模糊指令、攻击、边界值)**eval 不进 CI**开发时手工跑一次就过,上线后没人跑;eval 必须进入 GitHub 行动,PR 不过评价 不能合并――(3) **eval 集污染**eval 数据混进快速的少数拍照示例,分数虚高;eval 数据严格隔离.

> 代理通过演示.它们在生产中以无法预测的方式失败.基准回答是"这个模型是否具有广泛的能力?"而不是"这个代理是否在为我的产品交付正确补丁?"答案是:三层评估,持续运行,每个护和学习规则都映射到一个评估用例中.


> **【中文解读】**评估驱动的代理 开发) 将在传统软件工程中的TDD 应用于代理:先定义评估标准,再实现代理.

> **{【拓展：Eval-Driven Agent Development 是 2025-2026 年的最佳实践。核...】}**基于Eval-Driven Agent Development是2025-2026年最佳实践.核心工具: 1) AgentOpsAgent 追踪和评估平台; 2) LangSmithLangChain的评估套件; 3) BraintrustAI 评估框架.
## 概念的核心概念

### 评估三层

1. **Static benchmarks**SWE-bench 验证代码 (课时19),WebArena/OSWorld 浏览/桌面 (课时20),GAIA 对于一般主义者 (课时19),BFCL V4用于工具使用 (课时06).用于跨模型比较和回归盖特.污染是真实的:SWE-bench+发现了32.67%的解决方案泄漏.总是报告验证/+审计得分.

2. **Custom offline evals**产品的形状:
   - 作为法官的LLM (Langfuse,城,Opik 课 24).
   - 基于执行 (运行补丁,检查测试).
   - 基于轨迹 (比较与黄金的行动序列;OSWorld-Human显示黄金的顶级代理人1.4-2.7倍).

3. **Online evals**生产:
   - 会议重播 (长).
   - 警报警报 (课 16,21).
   - 逐步成本/延迟追踪 (课程23 OTel范围).

### 评价器优化器 (人类)

紧密的循环:

1. 发射器产生输出.
2. 评价员评审员.
3. 在评估员通过之前,再精炼.

任何你关心的代理流量都可以用评估器优化,以确保可靠性.

> 任何你关心的代理流程都可以用评估器优化器包装以提高可靠性.

> 评估驱动的代理 开发 率驱动的开发) 将作为代理 开发的核心进行评估.

### 2026 年最佳实践

- 子住在代码旁边.
- 报警每次公关.
- 通过测试结果,关口结合 (例如"没有回归>5%与主要").
- 每个护都会给一个评估案例.
- 每个学到的规则 (反思,工作流动支持学习规则) 都将一个失败案例映射出来.

### 结合14期

阶段14的每一个课程都会产生评估案例:

| Lesson | Eval case it generates |
|--------|------------------------|
| 01 Agent Loop | Budget-exhausted, infinite-loop guard |
| 02 ReWOO | Planner replans correctly when a tool fails |
| 03 Reflexion | Learned reflections apply on retry |
| 05 Self-Refine/CRITIC | Judge passes refined output |
| 06 Tool Use | Argument coercion works; unknown tools rejected |
| 07-10 Memory | Retrieval citations match sources; stale facts invalidate |
| 12 Workflow Patterns | Each pattern produces correct output |
| 13 LangGraph | Resume reproduces state exactly |
| 14 AutoGen Actors | DLQ catches crashed handlers |
| 16 OpenAI Agents SDK | Guardrail trips on the right inputs |
| 17 Claude Agent SDK | Subagent results return to orchestrator |
| 19-20 Benchmarks | SWE-bench Verified score, WebArena success rate, OSWorld efficiency |
| 21 Computer Use | Per-step safety catches injected DOM |
| 23 OTel | Spans emit required attributes |
| 26 Failure Modes | Detectors tag known failures |
| 27 Prompt Injection | PVE refuses poisoned retrievals |
| 28 Orchestration | Supervisor routes to the right specialist |
| 29 Runtime Shapes | DLQ handles N% failure |

如果你的评估套件中每个案例都有病例,你已经覆盖了14阶段.

> 如果你的评估套件有每个课程的用例,你已经覆盖了14阶段.

> 评估驱动的代理 开发 率驱动的开发) 将作为代理 开发的核心进行评估.

### 没有评估驱动的开发

- **No baseline.**没有最后一个已知的东西的等值是不可读的.
- **LLM-judge without grounding.**评判模式 (课05) 评判理由在外部工具上.
- **Over-fitting to evals.**优化评估与生产有用性不同.
- **Flaky evals.**没有确定性的情况会引起虚假报警.

> **没有基线。**没有最后已知良好状态的评估是不可读的.
> **LLM 评审器没有基础。**评审器也会幻觉――Critic 模式(第5课) 评审器基于外部工具――
> **过拟合评估。**为了评估优化会偏离实用性.
> **不稳定的评估。**无确定性使用例导致误报.

## 建立它,实现它.
```figure
ae-eval-three-layers
```

## 建立它

`code/main.py`是一个 stdlib eval 带:

- 类别的案例登记簿 (标准标志,定制,在线).
- 一个经过测试的经纪人.
- 评估者-优化者循环:提出,判断,完善到通过或最大轮.
- 关口:总通过率+与基线相反的回归.

运行它:

```
python3 code/main.py
```

输出:每案合格/失败,退缩标志,CI门判决.

> 输出:每例通过/失败、回归标志、CI 门控裁定──

> 评估驱动的代理 开发 率驱动的开发) 将作为代理 开发的核心进行评估.

## 用它实现框架

- 写出评估案例与代理代码相同的备忘录.
- 通过信息通讯,查看他们每一个公关.
- 没有回归的基础.
- 随着时间的推移.
- 连接每一个生产失败到一个新的案例.

## 运送它.

`outputs/skill-eval-suite.md`建立一个为代理产品的三层评估套件,具有CI门和回归跟踪.

> `outputs/skill-eval-suite.md`为代理产品构建三层评估套件,包括CI门控和回归追踪.

> 评估驱动的代理 开发 率驱动的开发) 将作为代理 开发的核心进行评估.

## 练习题

1. 写一个复制的评估案例,你的代理现在通过了吗?
  中文翻译:思考并实践此练习──
2. 建立一个为您的领域的LLM法官分类,以三个维度 (事实,语调,范围).
  中文翻译:思考并实践此练习──
3. 输入评估套件到CI. 输出在>=5%回归.
  中文翻译:思考并实践此练习──
4. 添加一个轨迹效率指标:代理采取了多少步骤?
  中文翻译:思考并实践此练习──
5. 给你一个评估案例,每一个14阶段的课程.
  中文翻译:思考并实践此练习──

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Static benchmark | "Off-the-shelf eval" | SWE-bench, GAIA, AgentBench, WebArena, OSWorld |  |
| Custom offline eval | "Domain eval" | LLM-as-judge / exec / trajectory on your product shape |  |
| Online eval | "Production eval" | Session replay, guardrail alerts, cost/latency tracking |  |
| Evaluator-optimizer | "Propose-judge-refine" | Iterate until judge passes |  |
| CI gate | "Merge blocker" | Fail the build on eval regression |  |
| Baseline | "Last-known-good" | Reference score to detect regression |  |
| Trajectory efficiency | "Steps over gold" | Agent step count divided by human expert minimum |  |

## 继续阅读 继续阅读

- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)"开始简单,优化使用评估"
  中文翻译:见原文.
- [OpenAI, SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) 评选的基准指数
  中文翻译:见原文.
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html)工具使用基准
  中文翻译:见原文.
- [Langfuse docs](https://langfuse.com/)评估+实践中重播会议
  中文翻译:见原文.
