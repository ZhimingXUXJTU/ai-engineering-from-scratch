# 计划执行控制流程 执行控制计划

> 一个无法生存的计划是脚本,一个能够重建的脚本是代理.

> **【中文解读】**本节是综合项目 建设计划-执行控制流.


**Type:** Build | **类型:** Build
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 lessons 01-07, Phase 14 lesson 01 | **前置知识:** Phase 13 lessons 01-07, Phase 14 lesson 01
**Time:** ~90 minutes | **时间:** ~90 minutes

>  前置 代理运用 5/10──参考14·08期
> 计划执行者 = "能重规划才叫代理人"――计划不住失败=脚本;能重规划的脚本=代理人――先建重规划器,再建初始规划器――失败→观察→重新规划是代理人的灵魂――

## 学习目标
- 描述一个计划作为编写步骤的顺序列表,以便执行者可以考虑进展和结果.
  中文翻译:将计划表达成一个排列的输入步骤列表,以便执行者可以考虑进展和结果.
- 执行步骤顺序,控制失败转移到规划器.
  中文翻译:随着控制失败转移到规划器,顺序执行步骤.
- 根据当前的线索标记,重新编写前一个错误,以便通知下一个计划.
  中文翻译:将前一个错误从当前的线索器中复制,以便下一个计划得到信息.
- 每次修改时发出一个计划差异,以便下游追踪器或UI可以显示为什么计划改变.
  中文翻译:每次修改都会发出一个不同计划,以便下游追踪器或UI可以显示为什么计划改变.
- 执行两个预算:一个硬步骤天花板和一个硬重建天花板.
  中文翻译:执行两个预算:一个硬步骤天花板和一个硬重建天花板.

```figure
cg-plan-replan
```

## 计划和执行,而不是思考链

> **【中文解读】**链式思维 (链思维) 代理 代币输出,让循环猜测工具调用何时结束;计划-执行 (计划-执行) 代理先输出结构化计划,然后确定性执行每一步.计划是数据利用可内省,审计和修订.

> **【拓展：Plan-and-Execute vs ReAct 架构】**对于LangChain的计划执行代理和LlamaIndex的子问题QueryEngine都采用类似的架构――与ReAct的相比,计划执行的优势在可审计性上.

链思维代理发出代币,让循环猜测工具调用结束的地方.一个计划执行代理首先发出结构化计划,然后确定性地执行每个步骤.计划是数据,带可以内视.执行是通过发送器运行数据的带.

> 一个链思想代理发射代币,让循环猜测工具调用结束的地方.一个计划执行代理首先发出结构化计划,然后确定性地执行每个步骤.计划是数据,该带可以内视.执行是通过发送器运行这些数据的带.


计划的执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,执行者,

> 两个小块.


```text
1. Abort         (return failed, surface the error)
2. Skip          (mark step failed, continue with the rest)
3. Replan        (hand the error to the planner, get a new plan from the cursor)
```

复原是把剧本变成一个代理的.

## 步骤的形状

> **【中文解读】** `Step`结构包含 id(单调度递增) 、工具_名称、参数、预期_结果、结果和错误。`expected_outcome`是规划器发出的简短描述,不由执行器强制执行它的用途是:重新规划时提供上下文,事件流中展示"这一步预期做什么"――

```text
Step
  id              : int           (monotonic within a plan revision)
  tool_name       : str
  args            : dict
  expected_outcome: str           (planner's stated success condition)
  result          : Any | None
  error           : str | None
```

`expected_outcome`计划器在修改计划时读取它;事件流则发出它,以便追踪器可以显示"这个步骤应该做X".

> `expected_outcome`是一个简短的句子,计划者在步骤旁边发出.


## 规划器的形状

> **【拓展：Plan-and-Execute 在 Claude 和 GPT-4 中的实践】**克劳德的工具_使用模式和GPT-4的功能_调用本质上都是单步计划-执行.但Devin、SWE-Agent等产品级的代理采用多步规划:先将用户需求分解为子任务,规划),再逐步执行,重新规划.`last_error`参数和`history`列表解决了这个问题.

```python
def planner(goal: str, history: list[Step], last_error: str | None) -> list[Step]:
    ...
```

纯粹的功能.`goal`对于用户来说,`history`是已经执行的步骤 (填写结果和错误).`last_error`计划器将从线索开始返回下一个计划.

> 一个纯粹的功能.`goal`对于用户来说,`history`是已经执行的步骤 (填写结果和错误).`last_error`计划器将从线索开始返回下一个计划.


计划者不知道执行者,他不知道重试,他不知道时间限制,他制造了一个计划.

> 计划者不知道执行者,他不知道重试,他不知道时间限制,他制造了一个计划.


## 执行者

执行器是一个小状态机器.每一步都通过发送器.结果是三个事情之一:成功,失败可重复计划,失败可致命.重复的失败将归还给规划师.致命的失败 (预算超出,重复计划天花板撞击) 返回一个`FAILED`会议结果.

> 执行器是一个小状态机器.每一步都通过发射器.结果是三个事情之一:成功,失败可重复计划,失败可重复.重复的失败将归还给规划者.致命的失败 (预算超出,重复计划上限撞击) 返回一个`FAILED`会议结果.


```mermaid
stateDiagram-v2
    [*] --> EXEC
    EXEC --> NEXT: success
    NEXT --> EXEC: n+1 < len(plan)
    NEXT --> DONE: n+1 == len(plan)
    EXEC --> REPLAN: failure
    REPLAN --> EXEC: new plan, replans_used < max_replans
    REPLAN --> FAILED: replans_used >= max_replans
    FAILED --> [*]
    DONE --> [*]
```

## 计划的修改不同

> **【中文解读】**当规划器回归新计划时,执行器发出`plan.diff`事件,包含三个字段:删除(被删除的步骤 id) 、添加(新增的步骤 id) 、修改的(工具名称或参数变更的步骤 id) ⋅追踪器或UI可使用删除线标记被移除的步骤,高亮新增的步骤──修订是可见的事件,而不是静默重写──

> **【拓展：计划可视化在 Agent 产品中的价值】**德文和库尔索都提供了任务执行步骤的可视化.用户可以看到代理的计划,每个步骤的执行状态以及计划变更历史.这种透明度是用户信任的关键因素,也是与纯 ReAct 的商业优势相比的计划和执行架构.

计划后,执行者发出一个`plan.diff`活动有三个场地.

> 计划后,执行者发出一个`plan.diff`活动有三个字段.


```text
removed: list of step ids that were in the old plan and are not in the new
added  : list of step ids in the new plan that were not in the old
revised: list of step ids whose tool_name or args changed
```

追踪器或UI可以将此作为删除步骤的突破和添加步骤的突出. 问题不是不同格式. 问题是修改是一个可见的事件,而不是一个默默的重写.

> 一个追踪器或UI可以将此作为删除步骤的突破和添加步骤的突出. 问题不是差异格式. 问题是修改是一个可见的事件,而不是沉默的重写.


## 两项预算,两项预算都很难

> **【中文解读】**两个硬性预算约束:`max_steps`(默认 12) 限制整个会议的总执行步骤数,包括重新规划后的步骤;`max_replans`规划器连续5次回归相同的错误计划将被预算上限捕获.

`max_steps`根据第一个规则,执行者将拒绝重新规划并返回失败. 执行者将拒绝重新规划并返回失败.

> `max_steps`限制整个会议的全部步骤执行,包括重新规划.


`max_replans`设置后,计划器调用了第一个计划后的次数.默认是五次.这是更重要的限制.一个计划器连续五次返回相同的破产计划,否则会循环直到步骤预算抓住它.设置后的重新计划使故障更快,原因更清楚.

> `max_replans`计划后,计划者被调用次数量.


## 在这个课程中,确定性规划者

我们在这个课程中不称作模型.课程运输一个决定性规划者,`last_error`现在,我们要去.

> 我们不会在这个课程中叫一个模型.课程是指一个决定性规划者,`last_error`现在,我们要去.


```text
last_error is None    -> emit a four-step plan
last_error matches X  -> emit a three-step plan that routes around X
last_error matches Y  -> emit a two-step plan that gives up gracefully
otherwise             -> return [] (signals nothing to replan)
```

这足以测试执行者的行为在每个过渡路径:成功,重复计划一次,重复计划两次,重复计划耗尽,

> 这足以测试执行者的行为在每个过渡路径:成功,重复计划一次,重复计划两次,重复计划耗尽,


## 结果形状

```text
SessionResult
  status      : "completed" | "failed"
  reason      : str     ("goal_met" | "step_budget" | "replan_budget" | "no_plan")
  history     : list[Step]
  revisions   : list[PlanDiff]
  events      : list[Event]
```

课二十节的带链循环可以直接读取.课二十三节的发送器是执行每个步骤的.课二十一节的注册表验证每个步骤的 args.课二十二节的输送将将整个流程通过JSON-RPC向模型客户端表面.

> 导航系统的导航系统可以直接读取这条信息.第23课的导航器是执行每个步骤的.第21课的登记器验证每个步骤的 args.第22课的运输将将整个流程通过JSON-RPC向模型客户端表面.


## 如何读取代码

`code/main.py`定义`PlanExecuteAgent`现在`Step`现在`PlanDiff`现在`SessionResult`执行者是单独的.`run(goal)`返回一个方法`SessionResult`计划差异通过比较步骤ID和`(tool_name, args)`两.

> `代码/主


`code/tests/test_agent.py`计划中失败一次重新规划,重新规划退出的疲劳`failed:replan_budget`计划差异事件格式.

> `代码/测试/测试_代理.


## 走得更远

首先,部分计划缓存:当一个计划成功的第三个六步骤,然后失败,你不想重新运行第三个.执行器已经保存历史;规划器只需要阅读它.第二,并行分支:当前执行器是严格的序列.一个发射独立分支的规划器 (`gather_step`没有`next_step`) 可以通过发送器同时进行两个工具调用.

> 两种扩展将需要一旦你将这个线线到一个真正的模型.


两者都增加了真正的复杂性. 一旦把线性执行器固定起来,两者都更容易增加.

> 两者都增加了真正的复杂性.一旦连线执行器被固定,两者都更容易增加.这就是这个课程所做的.

