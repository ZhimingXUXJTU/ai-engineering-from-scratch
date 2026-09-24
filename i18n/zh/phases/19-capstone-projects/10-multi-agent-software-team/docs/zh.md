# 卡普斯通10 多代理软件工程团队

> 许多代理工程团队的2026年形状已经融合:一个建筑师的计划,N编码器在平行工作树中工作,一个审查员的门,一个测试员验证. 斯威-阿夫的工厂架构,MetaGPT的角色驱动,AutoGen 0.4的打字演员图,Cognition的Devin和工厂的Droids都独立地登陆了它. 并行工作树将墙钟转换为吞吐量. 共同状态和传递协议成为失败表面. 目标是建立团队,在SWE-bench Pro上评估,

> **【中文解读】**本节是综合项目构建多代理软件团队,模拟完整的开发团队协作.


**Type:** Capstone | **类型:** Capstone
**Languages:** Python / TypeScript (agents), Shell (worktree scripts) | **语言:** Python / TypeScript (agents), Shell (worktree scripts)
**Prerequisites:** Phase 11 (LLM engineering), Phase 13 (tools), Phase 14 (agents), Phase 15 (autonomous), Phase 16 (multi-agent), Phase 17 (infrastructure)

>  **【前置】**顶点项目 10 = 综合阶段 11/13/14/15/16/17──多 代理软件团队 = SWE-AF / MetaGPT / AutoGen 0.4 / Devin / 工厂无人机 共识形态──
>  **【类比】**多 代理 软件团队 = "AI 开发组"――架构师规划→N个编码者并行工作树→评论员 守门→测试员 验证――并行工作树 把挂钟转成吞吐──共享状态+支持 协议成失败面──目标:SWE-bench Pro 评估+报告哪些交付 破坏+频率──**前置知识:**项目项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目: 项目:
**Phases exercised:**现在,我们在这个世界里,**涉及阶段:**子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子
**Time:** 40 hours | **时间:** 40 hours

## 问题 问题引入

> **【中文解读】**本节阐述多个代理软件团队的核心问题――单个代理编码器在大型任务中遇到瓶不是因为个人能力弱,而是200k代币上下文不能同时容纳架构计划、四个并行代码片、评审意见和测试输出――多个代理工厂将问题分开:架构师规划、编码者在并行工作树中实现、评审者关关关、测试者验证――失败面交 建筑师计划无法实现、编码者产生冲突、评审者批准幻觉修改、测试者与编写者竞争.

> **【拓展：多 Agent 框架生态】**2026年主要多代理 框架:SWE-AF:工厂架构:MetaGPT:角色提示:AutoGen 0.4:类型化:演员图:认知定向:产品级:工厂无线机器人:产品级:谷歌A2A协议:标准化:多代理的核心问题不是"是否工作"而是"每美元是否更优"定 放大效果:

单机编码带在大型任务上达到了一个天花板. 不是因为任何单个代理都很弱,而是因为200k代币的文本不能容纳一个架构计划加上四个平行代码基础片加上评论员评论加上测试输出. 多代理工厂分开了问题:一个建筑师拥有计划,编码师在并行工作树中实现,一个审查员的门,一个测试员验证. 斯威-阿夫的"工厂"架构,MetaGPT的角色,AutoGen的打字演员图所有三个框架都描述着相同的形状.

> 单个代理编码框架在大型任务中遇到天花板――不是因为任何单个代理能力弱,而是因为200k代币的上下文无法容纳架构计划加上四个并行代码库切片加评审意见加测输出――多个代理厂将问题分开:架构师拥有计划、编码者拥有并行工作树中的实现、评审者把关、测试者验证――SWE-AF的"工厂"架构、MetaGPT的角色、AutoGen的类型 演员图三种框架描述相同的形态――


设计师计划一些编码人员无法实现的东西.编码人员产生矛盾的差异.评论员批准了一个幻觉修复.测试员竞赛着一个写写写的编码器.你将构建一个团队,在50个SWE-bench Pro问题上运行它,跟踪每个编码人员,并发布死后测试.

> 失败面在交互处――架构师计划编辑者无法实现的东西――编辑者产生冲突――评审者批准了幻觉修复――测试者与仍在编辑编辑者竞争――你将建立这样一个团队,在50个SWE-bench Pro号中运行它,追踪每个交互,并发布事件后分析――


## 概念的核心概念

> **【中文解读】**角色是类型化代理:架构师(Opus 4.7,读号码 写计划并分解子任务) 编码者(Sonnet 4.7,N个并行实例,各自在 git 工作树 + Daytona 沙箱中) 评审者(GPT-5.4,读合并不同 批准或打回) 评审者(Gemini 2.5 Pro,独立运行测试套件) 通信通过共享任务板(文件/Redis),交接使用A2A协议 类型化消息──协调关注点包括合并解决冲突、共享状态同步和评审者的利益冲突避免──

> **【拓展：Token 放大效应】**多代理 系统的隐含成本是代币 放大:每次角色边界增加摘要提示和交接上下文.一次40轮单个代理运行变成4个角色160轮次.评估指标包括通过@1(解决率) 和$/解决问题.

角色是打字代理.**Architect**(Claude Opus 4.7) 阅读问题,写一个计划,并将其分解成用明确界面的子任务. **Coders**(Claude Sonnet 4.7,N平行例,每个案例都在一个`git worktree`独立执行子任务. **Reviewer**通过GPT-5.4阅读合并的差异,批准或要求具体的变更. **Tester**(Gemini 2.5 Pro) 单独运行测试套件,并报告与文物的失败.

> 角色是类型化代理.**架构师**编写计划并将其分解为显式接口的子任务.**编码者**其他国家和地区的经济发展`git worktree`独立实现子任务.**评审者**读取合并的差异并批准或要求具体修改.**测试者**独立运行测试套件并报告通过/失败及制品──


通过共享任务板 (文件支持或Redis) 进行通信. 每个角色都需要完成允许执行的任务. 交付是A2A协议类型的消息. 协调问题:融合冲突解决 (协调员角色或自动三向融合),共享状态同步 (计划在编码器启动后被结;重组是单独的事件),审查员关门 (审查员不能批准自己提出的变化或变化).

> 通信通过共享任务板 (文件支持或 Redis) 进行.每个角色消费它被允许处理任务. 交接是A2A 协议类型化消息.


代币放大是隐藏的成本.每个角色界限增加了总结提示和交付文本.40转单代理运行成为四个角色的总转折160. 标题特别权衡代币效率与单代理基线,因为问题不是"多代理工作"而是"每美元能否赢得".

> 代币 放大是隐含成本. 每个角色边界增加摘要提示和交接上下文.


## 建筑,建筑

```
GitHub issue URL
      |
      v
Architect (Opus 4.7)
   reads issue, produces plan with subtasks + interfaces
      |
      v
Task board (file / Redis)
      |
   +-- subtask 1 ---+-- subtask 2 ---+-- subtask 3 ---+-- subtask 4 ---+
   v                v                v                v                v
Coder A          Coder B          Coder C          Coder D          (4 parallel)
 (Sonnet)         (Sonnet)         (Sonnet)         (Sonnet)
 worktree A       worktree B       worktree C       worktree D
 Daytona          Daytona          Daytona          Daytona
      |                |                |                |
      +--------+-------+-------+--------+
               v
           merge coordinator  (three-way merge + conflict resolution)
               |
               v
           Reviewer (GPT-5.4)
               |
               v
           Tester  (Gemini 2.5 Pro)  -> passes? -> open PR
                                     -> fails?  -> route back to coder
```

##  技术

- 编排: 具有共享状态+每个代理子图的LangGraph
  中文翻译:管弦乐: 语法与共享状态 + 每个代理子图
- 信息传输:为打字的代理间信息的A2A协议 (Google 2025)
  中文翻译:消息传递:A2A协议 (Google 2025) 输入代理间消息
- 模型:Opus 4.7 (建筑师),Sonnet 4.7 (编码器),GPT-5.4 (评论员),Gemini 2.5 Pro (测试员)
  中文翻译:模型:Opus 4.7 (建筑师),Sonnet 4.7 (编码器),GPT-5.4 (评论员),Gemini 2.5 Pro (测试员)
- 工作树隔离: `git worktree add`每个编码器+戴顿沙箱
  中文翻译:工作树隔离: `git worktree add`每个编码器+戴顿沙箱
- 合并协调员:定制三方合并+通过LLM调解冲突
  中文翻译:合并协调员:定制三向合并 + LLM调解冲突
- 标准:SWE-bench Pro (50个版本),SWE-AF场景,HumanEval++用于单元测试
  中文翻译:Eval:SWE-bench Pro (50个版本),SWE-AF场景,HumanEval++用于单元测试
- 可观察性:具有角色标签范围的长,每代理代币会计
  中文翻译:可观察性:具有角色标签范围的长,每代理代币会计
- 部署:K8个角色作为一个独立部署+HPA后备
  中文翻译:部署:K8s,每个角色作为一个独立的部署 + HPA在后期

## 动手构建

> **【中文解读】**构建多个代理 软件开发团队:架构师(分解任务为DAG) 、多个编码代理(并行实现子任务) 、代码审查代理(检查正确性和风格) 、测试代理(编写和运行测试) ⋅任务板是文件支持的JSONL,角色通过标签订阅信息──关键设计是子任务接口的明确声明每个子任务涉及的文件、公共函数和测试影响──

> **【拓展：多 Agent 软件开发的产业实践】**测试的学术研究显示,多个代理合作在代码生成质量上优于单个代理,关键因素是角色分离带来的下文分离. 本课程的JSONL任务板是这些系统核心通信协议的教育简化.
```figure
ce-team-handoff
```

## 建立它

1. **Task board.**文件支持的JSONL,输入信息: `plan_request`现在`subtask`现在`diff_ready`现在`review_needed`现在`test_needed`现在`approved`现在`rejected`现在`replan_needed`代理人签订了标签.
   中文翻译:1. **Task board.**文件支持的JSONL,输入信息: `plan_request`现在`subtask`现在`diff_ready`现在`review_needed`现在`test_needed`现在`approved`现在`rejected`现在`replan_needed`代理人签订了标签.

2. **Architect.**读取GitHub问题,运行Opus 4.7与计划模板,需要明确的子任务界面 (触摸的文件,公共功能,测试影响). 发出一个 `plan_request`它们有着一个小任务.
   翻译: 翻译:**Architect.**读取GitHub问题,运行Opus 4.7与计划模板,需要明确的子任务界面 (触摸的文件,公共功能,测试影响). 发出一个 `plan_request`它们有着一个小任务.

3. **Coders.**其他工作者都需要一个小任务,每个工作者都需要一个新的任务.`git worktree add`通过接,我们可以在线观看.`diff_ready`附加补丁+测试地带.
   翻译: 翻译:**Coders.**其他工作者都需要一个小任务,每个工作者都需要一个新的任务.`git worktree add`通过接,我们可以在线观看.`diff_ready`附加补丁+测试地带.

4. **Merge coordinator.**在全编码器完成时,三向将N分支合并成一个阶段分支.只有在文件层次重叠的情况下,LLM调解冲突.
   翻译: 翻译:**Merge coordinator.**在全编码器完成时,三向将N分支合并成一个阶段分支.只有在文件层次重叠的情况下,LLM调解冲突.

5. **Reviewer.**没有批准其作者的差异. 发行`approved`没有任何`review_feedback`通过特定变更请求将返回相关编码器.
   翻译: 五.**Reviewer.**没有批准其作者的差异. 发行`approved`没有任何`review_feedback`通过特定变更请求将返回相关编码器.

6. **Tester.**双子座2.5 Pro在一个清洁的沙箱里运行测试套件,捕捉了文物,发射了`test_passed`或`test_failed`失败的测试循环返回失败的子任务的编码器.
   翻译: 七个字**Tester.**双子座2.5 Pro在一个清洁的沙箱里运行测试套件,捕捉了文物,发射了`test_passed`或`test_failed`失败的测试循环返回失败的子任务的编码器.

7. **Handoff accounting.**每个跨越角色界限的消息都会在Langfuse中获得一个跨度,使用的有效载荷大小和模型.计算每次子任务的代币放大 (coder_tokens + reviewer_tokens + tester_tokens + architect_share / coder_tokens).
   翻译:7.**Handoff accounting.**每个跨越角色界限的消息都会在Langfuse中获得一个跨度,使用的有效载荷大小和模型.计算每次子任务的代币放大 (coder_tokens + reviewer_tokens + tester_tokens + architect_share / coder_tokens).

8. **Eval.**运行50个SWE-bench Pro问题. 比较pass@1和$-per-solved-issue与单个代理基线 (单个工作树中的一个Sonnet 4.7).
   翻译:8.**Eval.**运行50个SWE-bench Pro问题. 比较pass@1和$-per-solved-issue与单个代理基线 (单个工作树中的一个Sonnet 4.7).

9. **Post-mortem.**对于每一个失败的问题,确定失败的交付 (计划太模糊,合并冲突,评论员错误批准,测试者).
   翻译:9.**Post-mortem.**对于每一个失败的问题,确定失败的交付 (计划太模糊,合并冲突,评论员错误批准,测试者).

## 用它使用方法

```
$ team run --issue https://github.com/acme/widget/issues/842
[architect] plan: 4 subtasks (parser, cache, api, migration)
[board]     dispatched to 4 coders in parallel worktrees
[coder-A]   subtask parser  -> 42 lines, tests pass locally
[coder-B]   subtask cache   -> 88 lines, tests pass locally
[coder-C]   subtask api     -> 31 lines, tests pass locally
[coder-D]   subtask migration -> 19 lines, tests pass locally
[merge]     3-way merge: 0 conflicts
[reviewer]  comments on cache (thread pool sizing); routed to coder-B
[coder-B]   revision: 92 lines; submits
[reviewer]  approved
[tester]    all 412 tests pass
[pr]        opened #3382   4 coders, 1 revision, $4.90, 18m
```

## 发射上线

`outputs/skill-multi-agent-team.md`鉴于问题URL和平行性水平,团队会产生一个准备好合并的 PR,以每个角色的代币计算.

> `outputs/skill-multi-agent-team.md`交付物质. 给定问题URL和并行级别,团队产生可合并的 PR,附带每个角色的代币计费.


| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | SWE-bench Pro pass@1 | Matched 50-issue subset, pass@1 |
| 20 | Parallel speedup | Wall-clock vs single-agent baseline |
| 20 | Review quality | False-approval rate on injected-bug probe |
| 20 | Token efficiency | Total tokens per solved issue vs single-agent |
| 15 | Coordination engineering | Merge-conflict resolution, handoff-failure histogram |
| **100** | | |

## 练习题

1. 注入明显的错误到中期差异中 (额外的`return None`检查员的错误批准率. 调整检查员提示,直到错误批准率低于5%.

2. 缩小到两个编码器 (建筑师+编码器+审查器+测试器,编码器连续执行两个子任务).比较墙钟和通过率.

3. 替换合并协调器用单字符限制 (子任务触摸分离的文件集). 测量建筑师的规划负担.

4. 测量虚假批准率和代币成本的分别.

5. 添加第五个角色:记录者 (海库4.5). 经过审查,它产生了变更日志输入. 测量文档质量是否合理增加代币支出.

## 关键词 关键词

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Parallel worktree | "Isolated branch" | `git worktree add` producing a fresh working tree per coder |
| Task board | "Shared message bus" | File or Redis store of typed messages agents subscribe to |
| Handoff | "Role boundary" | Any message crossing from one role's context to another's |
| Token amplification | "Multi-agent overhead" | Total tokens across roles / single-agent tokens for the same task |
| A2A protocol | "Agent-to-agent" | Google's 2025 spec for typed inter-agent messages |
| Merge coordinator | "Integrator" | Component that runs three-way merge and mediates conflicts |
| False approval | "Reviewer hallucination" | Reviewer approves a diff with known bugs |

## 继续阅读 继续阅读

- [SWE-AF factory architecture](https://github.com/Agent-Field/SWE-AF)2026年参考多代理工厂
- [MetaGPT](https://github.com/FoundationAgents/MetaGPT)基于角色的多代理框架
- [AutoGen v0.4](https://github.com/microsoft/autogen)微软的类型演员框架
- [Cognition AI (Devin)](https://cognition.ai)参考产品
- [Factory Droids](https://www.factory.ai)替代参考产品
- [Google A2A protocol](https://a2a-protocol.org/latest/) 代理间信息信息规范
- [git worktree documentation](https://git-scm.com/docs/git-worktree)隔离基板
- [SWE-bench Pro](https://www.swebench.com)评估目标
