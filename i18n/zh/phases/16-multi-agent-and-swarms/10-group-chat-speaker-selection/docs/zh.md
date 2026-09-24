# 群聊和演讲者选择群聊 选择发言人

> 交谈配套将N代理放在一个对话中;选项函数 (LLM,圆或定制) 选择下一个说话者. 这就是新兴多代理对话的原型. 代理人不知道他们在静态图表中的作用,他们只是对共享池进行反应. 根据AutoGen v0.2的GroupeChat语义在AG2叉子中保存下来;AutoGen v0.4将其重写为以事件为导向的演员模型. 微软于2026年2月将AutoGen放入维护模式,并将其与语义内核合并到微软代理框架中 (RC 2026年2月). 群众聊天原始的存活在AG2和微软代理框架中 学会一次,在任何地方使用它.

> **【中文解读】**本节介绍了群聊发言人选择多 代理 讨论中决定谁发言、何时发言的机制──

> **【拓展：group chat speaker selection→具体应用】**群聊发言人选择是多代理 讨论中的关键问题谁发言、什么时候发言、发言多久──三种主要策略: 1) 轮流制按固定顺序发言; 2) 相关性制最相关的代理发言; 3) 仲裁制一个专门的协调员决定谁发言──AutoGen的集团聊天使用LLM作为仲裁员──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:阶段16·04(原语模型) 、AutoGen 基础──群聊 = N 个代理 共享一个对话池,发言人选择决定谁说话──
>  **【类比】**群聊发言人选择 = "会议主持人"――轮流制 = 圆桌按序;相关性制 = 谁懂谁说;仲裁制 = 主持人指定――AutoGen GroupChat 用 LLM 当主持人成本高但灵活――2026 注意:AutoGen已被微软合并到微软代理框架,AG2是社区分叉,两者保留了 GroupChat 原语――

## 问题 问题引入

静态图表 (长图) 当工作流程已知时很好.真正的对话不是静态:有时编码器会问评论员,有时研究员,有时作家.硬码每次可能交给产生边缘爆炸.你想要*代理对共享池进行反应*,有功能决定谁接下来说话.

> 静态图片 (长图) 在工作流中已知时很好――真实对话不是静态的:有时编码器问审阅者,有时问研究员,有时问写作者――硬编码每个可能的交往会产生边爆炸――你想要*代理对共享池做出反应*,由某个函数决定谁下一个发言――

边缘爆炸问题是真实的:一个五个代理系统,所有的可能的交换都有25个方向边缘.添加一个第六个代理,你得到36个.

> 边爆炸问题是真实的:带所有可能交往的5个代理系统有25条有向边. 添加第六个代理就有36条. 图方法不能扩展到现有的对话.

这就是AutoGen集团聊天所做的.

> 这就是AutoGen集团聊天所做的.

## 概念的核心概念

### 形状

```
              ┌─── shared pool ────┐
              │   m1  m2  m3  ...  │
              └─────────┬──────────┘
                        │ (everyone reads all)
      ┌───────┬─────────┼─────────┬───────┐
      ▼       ▼         ▼         ▼       ▼
    Agent A  Agent B  Agent C  Agent D  Selector
                                           │
                                           ▼
                                  "next speaker = C"
```

每个代理都会看到每一个消息,每一个转折都会调用一个选号函数来选择接下来说谁.

> 每个代理人看到每条消息. 每轮调用选手函数来选择下一个发言人.

强度:任何代理人都可以对任何话都做出反应.弱点:20轮后,每个代理人的背景是巨大的,昂贵的,和稀释的.减轻:每个代理项目范围的视图 (课 15) 或提前结束.

> 完全透明池既是集团聊天的优势也是弱点.优势:任何代理人可以对任何人说任何事情做出反应.

### 选用三种口味

**Round-robin.**定制周期. 确定性. 标量线性在N,但忽略文本一个编码器即使是法律审查的主题得到了轮回.

> **轮询。**固定循环――确定性――按N 线性扩展但忽略下文即使主题是法务审阅,编码器也能获得发言权──

**LLM-selected.**电话给一个LLM,读取最近的库,并返回最好的下一个演讲者. 意识到环境,但慢:每轮都增加一个LLM电话.

> **LLM 选择。**调用 LLM 读取最近的池并返回最佳下一个发言人──上下文感知但慢:每轮增加一次 LLM 调用──AutoGen 的默认选择──

**Custom.**典型:LLM选择后退规则 (例如",总是给验证器后代码器").

> **自定义。**一个Python函数,使用你想要的任何逻辑――典型:LLM 选择带回退规则 (例如",总是在编码器后给验证者发言权")

### 可交谈的代理API

```
agent = ConversableAgent(
    name="coder",
    system_message="You write Python.",
    llm_config={...},
)
chat = GroupChat(agents=[coder, reviewer, tester], messages=[])
manager = GroupChatManager(groupchat=chat, llm_config={...})
```

`GroupChatManager`经理打电话给选手,然后再送下一个选手. 循环持续到终止条件.

> `GroupChatManager`持有选择器──当代理完成一轮时,管理者调用选择器,返回下一个代理──循环继续直到终止条件──

选择器功能是集团聊天的核心. 换换它,改变调整风格. 圆选器 = 确定性. LLM选器 = 适应性. 定制选器 = 任何规则你编码. 同样的原始,不同的调整.

> 选择器函数是集团聊天的核心. 换掉它,改变编排风格. 轮询选择器 = 确定性.

### 终止

现在,我们有三种常见模式:

> 三种常见模式:

- **Max rounds.**完全转的硬帽子.
  翻译: 中文**最大轮数。**总轮数的硬上限.
- **"TERMINATE" token.**代理人可以发出哨兵信息; 经理在出现时停止.
  翻译: 中文**"TERMINATE" 标记。**代理可以发出哨兵消息; 管理员在出现时停止.
- **Goal-reached check.**通过轻量级验证器,每次转换都会进行,
  翻译: 中文**目标达成检查。**轻量级验证者每轮运行,完成时停止聊天.

### 机器人> AG2 分裂和微软代理框架合并
### 血统:叉子和合并

在2025年初,微软开始围绕事件驱动的演员模型重写AutoGen (v0.4).社区将AutoGen v0.2的GroupeChat语义作为AG2,保留了早期采用者集成的API.

> 2025年初,微软开始围绕事件驱动演员模型对AutoGen (v0.4) 进行重大重写.社区将AutoGen v0.2的GrouppChat语义分叉为AG2,保留早期采用者已经集成的API.

由于4.0版本基本破坏了后退兼容性,`GroupChat`现在`ConversableAgent`其他`GroupChatManager`虽然 API 稳定,但 v0.4 引入了新的事件驱动原始.

> 分叉是必要的,因为v0.4在基本上破坏了后后兼容性.`GroupChat`,我知道.`ConversableAgent`和 `GroupChatManager`截至2026年,两条线都积极维护.

2026年2月,微软宣布,AutoGen将进入维护模式,以事件驱动的演员模式合并到**Microsoft Agent Framework**集团Chat概念在两条轨道中存活下来;实现细节不同. AG2是v0.2兼容代码的首选上游.

> 2026年2月,微软宣布AutoGen进入维护模式,事件驱动演员 模型合并到**Microsoft Agent Framework**现在已经与语义内核合并) ――GroupChat 概念在两个轨道中存活;实现细节不同――AG2 是 v0.2 兼容代码的首选上游――

课程:API表面比框架还长.在2024年写到 AutoGen v0.2 的 GroupChat API 版的代码仍然在2026年通过 AG2 运行不变.框架变化;原始 (共享池 + 选择器) 不.投注原始.

> 教训:API 表面比框架持久──2024年针对AutoGen v0.2 GroupChat API 编写的代码在2026年通过AG2 仍然不变运行──框架变化;原语(共享池 + 选择器) 不变──押注原语──

### 当集团聊天适合时

- **Emergent conversations.**你不想预先连接每一个可能的下一个扬声器.
  翻译: 中文**涌现对话。**你不想预先连接每一个可能的下一个发言人.
- **Role-mixing tasks.**编码器问研究员,研究员问档案员,档案员问编码器回来.流量不是DAG.
  翻译: 中文**角色混合任务。**编码器问研究员,研究员问档案员,档案员反问编码器――流程不是DAG――
- **Exploratory problem-solving.**想"大脑风暴会议",而不是"集线".
  翻译: 中文**探索性问题解决。**想想"头脑风暴会议",而不是"装配线"――

### 当它失败时

- **Strict determinism.**选择法师可能不一致,相同的提示,不同的运行,不同的下一个扬声器.
  翻译: 中文**严格确定性。**选择器可能不一致──同样的提示,不同运行,不同下一个发言者──
- **Sycophancy cascades.**警方将会对那些最自信的说话做出回应.
  翻译: 中文**谄媚级联。**代理屈从于最自信的发言人.
- **Context bloat.**每个代理都会读取每一个信息; 10 轮后,文本是巨大的.
  翻译: 中文**上下文膨胀。**每个代理 读取每条消息;10轮后上下文巨大――使用投影 (图片) 阅读15课)
- **Hot speakers.**选择者喜欢他的专业,所以一个代理主导对话.
  翻译: 中文**热发言者。**一个代理主导对话,因为选择器偏向其专长.

### 集团聊天与监督者

它们是原始的,不同默认的:

> 相同原语,不同默认值:

- 监督者:一个代理计划,其他人执行. 选手是"问计划者要做什么".
  中文翻译:监督者:一个代理 规划,其他执行.选择器是"问规划者做什么".
- 集团聊天:所有代理人都是同行;选择器是共享池的函数.
  中文翻译:群聊:所有代理是对等的;选择器是共享池上的函数.

两个都使用了04课程的四个原始方法. 群体聊天默认到LLM选择的管弦乐和全池共享状态.

> 两者都使用04课的四个原语――群聊默认使用LLM选择的编排和全池共享状态――

监管者:一个代理人拥有计划,代表. 团体聊天:计划是隐含的,从对话中出现的. 一个是更可控制的;第二个是更灵活的.

> 监督者和群谈之间的选择主要是关于*谁持有计划*──监督者:一个代理人 拥有计划并委托――群谈:计划是隐式的,从对话中涌现――前者更可控;后者更灵活――

## 建立它,实现它.
```figure
swarm-speaker
```

## 建立它

`code/main.py`执行一个从头开始的集团聊天. 三个代理 (编码器,审查员,经理),轮和LLM选择的变体,并终止一个`TERMINATE`标志.

> `code/main.py`通过标准库从头部实现一个集团聊天.`TERMINATE`标记上终止.

演示程序将打印对话转录以及选手的决定记录.

> 展示印发对话记录以及两种变体的选择器决策追踪――

## 用它实现框架

`outputs/skill-groupchat-selector.md`配置一个 GroupChat 选项选项为给定的任务 圆比LLLM-选择对定制,以及选项选项输入 (最近的消息,代理专业,转数) 进行使用.

> `outputs/skill-groupchat-selector.md`为给定任务配置 集团聊天 选择器 轮询 vs LLM 选择 vs 自定义,以及使用什么选择器输入

## 运送它.

检查列表:

> 检查清单:

- **Max rounds cap.**常常. 10-20个用于典型的任务.
  翻译: 中文**最大轮数上限。**总是使用──典型任务 10-20──
- **Speaker-balance metric.**轨道转向每位代理;当失衡超过门时,应警报.
  翻译: 中文**发言者平衡指标。**随着每一个代理的轮流;当不平衡超过值时告警.
- **Termination token.** `TERMINATE`或是专门的验证代理.
  翻译: 中文**终止标记。** `TERMINATE`或是专业的证人代理人.
- **Projection or scoped memory.**在10个消息之后,考虑给每个代理只提供一个范围的视图,以防止文本膨胀.
  翻译: 中文**投影或范围内存。**经过10条消息, 考虑给每个代理人只一个范围视图以防止下文膨胀.
- **Selector logging.**对于选择的LLM变体,记录选项输入和选择.否则无法调试.
  翻译: 中文**选择器日志。**对于 LLM 选择变体,记录选择器的输入和选择――否则调试不可能――

## 练习题

1. 跑步`code/main.py`根据"轮"和"士"的选择,哪个代理主导?
   中文翻译:运行 `code/main.py`比轮询与LLM选择下对话
2. 在选择器中添加"每代理最高说话"规则.
   中文翻译:在选择器中添加"每一个代理最大发言次数"规则.
3. 执行目标终止:当审查员回来时停止.
   中文翻译:实现目标达成终止:当审阅者回归"批准"时停止.
4. 在 GroupChat 上阅读AutoGen稳定文件. 确定使用的默认选择器`GroupChatManager`现在,我们要去.
   中文翻译:阅读AutoGen 稳定文档中的群体聊天――识别`GroupChatManager`使用默认选择器.
5. 阅读AG2备忘录并将其v0.2 GroupChat与v0.4事件驱动版本进行比较.v0.4添加了什么具体属性 (吞吐量,故障耐受性,可复合性)?
   中文翻译:阅读 AG2 仓库并比较其v0.2 GroupChat 与v0.4 事件驱动版本──v0.4 添加了什么具体属性(吞吐量、容错、可组合性)?

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GroupChat / 群聊 | "Agents in one chat room" / "一个聊天室中的 Agent" | Shared message pool + selector function. AutoGen / AG2 primitive. / 共享消息池 + 选择器函数。AutoGen / AG2 原语。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | The function that picks the next agent. Round-robin, LLM-selected, or custom. / 选择下一个 Agent 的函数。轮询、LLM 选择或自定义。 |
| GroupChatManager / 群聊管理者 | "The meeting host" / "会议主持人" | AutoGen component that owns the selector and loops over turns. / 拥有选择器并循环轮次的 AutoGen 组件。 |
| ConversableAgent / 可对话 Agent | "The base agent" / "基础 Agent" | AutoGen base class; an agent that can send and receive messages. / AutoGen 基类；可以发送和接收消息的 Agent。 |
| Termination token / 终止标记 | "The 'stop' word" / "停止词" | Sentinel string (usually `TERMINATE`) that ends the chat. / 结束聊天的哨兵字符串（通常是 `TERMINATE`）。 |
| Hot speaker / 热发言者 | "One agent dominates" / "一个 Agent 主导" | Failure mode where the selector keeps picking the same agent. / 选择器持续选择同一 Agent 的失败模式。 |
| Context bloat / 上下文膨胀 | "Pool grows unbounded" / "池无限增长" | Each agent reads every prior message; context grows with turns. / 每个 Agent 读取每条先前消息；上下文随轮次增长。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Role-specific view into the shared pool to prevent context bloat. / 角色特定的共享池视图以防止上下文膨胀。 |

## 继续阅读 继续阅读

- [AutoGen group chat docs](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/group-chat.html)参考实施
  中文翻译:AutoGen 群聊文档  参考实现
- [AG2 repo](https://github.com/ag2ai/ag2)社区AutoGen v0.2延续
  中文翻译:AG2 仓库 社区 自动生成 v0.2 延续
- [Microsoft Agent Framework docs](https://microsoft.github.io/agent-framework/)合并后继者,RC 2026年2月
  中文翻译:微软代理框架 文档  合并后的继任者,2026年 2月 RC
- [Microsoft Agent Framework docs](https://learn.microsoft.com/en-us/agent-framework/)合并后继者,RC 2026年2月
- [AutoGen v0.4 release notes](https://microsoft.github.io/autogen/stable/)事件驱动演员模型重写详情
  中文翻译:AutoGen v0.4 发布说明 事件驱动演员 模型重写详情
