# 为什么多代理?

> 智能举动不是一个更大的代理,而是更多的代理.

> **【中文解读】**本节介绍了为什么需要多个代理 系统 单个代理 单个代理 单个代理 单个代理 单个代理 系统 单个代理 系统 单个代理 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 系统 单个代理 单个代理 系统 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个代理 单个 单个代理 单个 单个代理 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个 单个

> **【拓展：why multi agent→具体应用】**单个代理在处理复杂任务时面临三个瓶: 1) 上下文溢出所有信息塞进一个窗口,重要被淹没; 2) 角色混乱 单个代理扮演多个角色导致提示词冲突; 3) 串行执行工具调用只能排队――多代理通过分工协作解决这些问题――人类研究表明,多代理系统在浏览Comp基准上单个代理提升 90.2%,80%的方仅由代币使用解释量差异――

>  **【前置】**学本节前请先掌握:阶段14(代理工程) 全部,特别是阶段14·01(代理循环) 和阶段14·28(配乐模式) ◎本节回答"什么时候用多代理"简单回答:单代理+工具不够时间。人类体验法则:任务需要 > 50 工具调用、或 > 1 个角色(如研究员+写手) 、或并行能省时间,才考虑多代理──

>  **【类比】**单代理对多代理 = 全能管家对专业团队对全能管家(单代理) 可以做所有事情但每件事都不精:上午做饭、下午修车、晚上辅导作业,每样都半吊子。专业团队(多代理):厨师专做饭、机修工专修车、家教专辅导,每个人精一行──代价:协调成本(代理间通信) 和复杂性增加简单任务使用单代理更划算──

**Type:** Learn | **类型:** 学习
**Languages:** TypeScript | **语言:** TypeScript
**Prerequisites:** Phase 14 (Agent Engineering) | **前置知识:** Phase 14 (Agent 工程)
**Time:** ~60 minutes | **时间:** ~60 分钟

## 学习目标

- 确定单剂的上限 (文本溢出,混合专业知识,连续瓶) 并解释分为多个代理是什么是正确的举动
  中文翻译:识别单个代理 上限(上下文溢出、专业能力混合、串行瓶),并解释何时分为多个代理是正确的选择
- 进行对比 (管道,平行风扇,监督,层次) 调整模式,并选择对特定任务结构的正确模式
  中文翻译:比较编排模式 ((流水线、并行扇出、监督者、分层),并为给定任务结构选择合适的模式
- 设计一个多代理系统,具有明确的角色界限,共享状态和通信合同
  中文翻译:设计一个具有明确角色边界的多代理系统
- 分析多代理复杂性 (延迟,成本,调试难度) 与单代理简单性的折衷
  中文翻译:分析多 代理 复杂性(延迟、成本、调试难度) 与单个代理 简单性之间的权衡

## 问题 问题引入

在14期中,你建立了一个单个代理.它可以读取文件,运行命令,调用API,并考虑结果.然后你将它指向一个真正的代码库:200个文件,三个语言,依赖基础设施的测试,以及在编写代码之前需要研究外部API.

> 在14期中,你建立了一个单个代理. 它运行良好,能够读取文件,运行命令,调用API并推论结果. 然后你将它指向一个真实的代码库:200 文件,三种语言,依赖基础设施测试,以及需要先研究外部API重新编写代码的要求.

演示代理和生产代理之间的差距是"一个文件,一个语言,一个工具"和"许多文件,许多语言,许多工具有依赖性"之间的差距.演示工作是因为任务适合.

> 演示 代理与生产代理之间的差距是"一个文件"",一种语言"",一个工具"和"许多文件"",许多语言"",许多依赖的工具"之间的差距.

代理人窒息.不是因为LLM是愚蠢的,而是因为任务超过了一个代理循环可以处理的. 文本窗口充满文件内容. 代理人忘记了40次工具通话之前读到的内容. 他试图同时成为研究人员,编码者和评论员,并且做了这三件事都很差.

> 代理毁了. 不是因为LLM愚蠢,而是因为任务超越了单个代理循环能处理范围. 上下文窗口被文件内容填满. 代理忘记了40次调用前读的内容. 它试图同时扮演研究员,程序员和审核员的三个角色,但三个都不好.

这就是单机的天花板.每当任务需要:

> 每次任务需要以下条件,你会遇到:

顶层结构性,而不是算法性.更好的LLM延迟了顶层,但不会删除它.一个1M标语文本窗口就像一个200k一样肯定地填满了它只需要更多文件.

> 上限是结构性的,不是算法性的.更好的LLM 延迟上限但不移除它.

- **More context than fits in one window**- 阅读50份文件,超过200万个代币
  翻译: 中文**超出一个窗口容量的上下文**读取50个文件将超过200万个代币
- **Different expertise at different stages**- 研究需要与代码生成不同的激励
  翻译: 中文**不同阶段需要不同的专业知识**研究需要与代码产生不同的提示
- **Work that can happen in parallel**- - - 既然可以同时读到,为什么要连续读三个文件?
  翻译: 中文**可以并行执行的工作**既然可以同时读三个文件,为什么要顺序读?

## 概念的核心概念

### 单机机顶

一个代理是一个循环,一个文本窗口,一个系统提示.

> 单代理是一个循环,一个上下文窗口,一个系统提示.

```
┌─────────────────────────────────────────┐
│            SINGLE AGENT                 │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │         Context Window            │  │
│  │                                   │  │
│  │  research notes                   │  │
│  │  + code files                     │  │
│  │  + test output                    │  │
│  │  + review feedback                │  │
│  │  + API docs                       │  │
│  │  + ...                            │  │
│  │                                   │  │
│  │  ██████████████████████ FULL ███  │  │
│  └───────────────────────────────────┘  │
│                                         │
│  One system prompt tries to cover       │
│  research + coding + review + testing   │
│                                         │
│  Result: mediocre at everything         │
└─────────────────────────────────────────┘
```

单个系统提示是根本原因.它必须同时提供研究,编码,审查和测试的指示.每一个指示都稀释了其他命令.代理最终在一切方面都"好",但在任何方面都不擅长.

> 单系统提示是根本原因. 它必须同时为研究编码,审核和测试提供指令.

三个东西会破裂:

> 三个问题会导致崩:

1. **Context saturation**到了30轮,代理已经消耗了15万个文件内容,命令输出和先前推理的代币.
   翻译: 中文**上下文饱和**工具结果不断堆积.到第30轮时,代理已经消耗了15万个代币的文件内容.命令输出和前推理.

2. **Role confusion**系统提示: "你是一个研究人员,编码者,审查者和测试者",产生一个半研究,半编码的代理,
   翻译: 中文**角色混乱**一个写"你是研究员,程序员,审核者和测试员"的系统提示会产生一个半研究,半编码,永远不完整的审核代理.

3. **Sequential bottleneck**经理读取文件A,然后文件B,然后文件C.三次连续LLM电话,三次连续工具执行.
   翻译: 中文**串行瓶颈**代理 读取文件A,然后文件B,然后文件C──三次串行LLM 调用──三次串行工具执行──没有并行性──

单个代理人是一个一般专家,要求在每一步都做专家. 多代理人分工,让每个代理人成为一个专家.

> 单个代理人是要求在每一步都成为专家的通才. 多个代理人分工,让每个代理人成为一个事项的专家.

### 多代理解决方案

给每一个代理一个工作,一个背景窗口,一个系统提示调整到这个工作:

> 拆分工作.给每一个代理一个任务,一个上下文窗口和一个为这个任务调整的系统提示:

对于每一个代理人的提示,都是更短和更集中.每一个代理的文本窗口只包含需要的内容.每一个代理都可以独立测试和改进.主管处理组合.

> 对于每一个代理的提示更短更集中. 每个代理的下文窗口只拥有它所需的.

```
┌──────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                          │
│                                                          │
│  "Build a REST API for user management"                  │
│                                                          │
│         ┌──────────┬──────────┬──────────┐               │
│         │          │          │          │               │
│         ▼          ▼          ▼          ▼               │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│   │RESEARCHER│ │  CODER   │ │ REVIEWER │ │  TESTER  │  │
│   │          │ │          │ │          │ │          │  │
│   │ Reads    │ │ Writes   │ │ Checks   │ │ Runs     │  │
│   │ docs,    │ │ code     │ │ code     │ │ tests,   │  │
│   │ finds    │ │ based on │ │ quality, │ │ reports  │  │
│   │ patterns │ │ research │ │ finds    │ │ results  │  │
│   │          │ │ + spec   │ │ bugs     │ │          │  │
│   └─────┬────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│         │           │            │             │         │
│         └───────────┴────────────┴─────────────┘         │
│                          │                               │
│                     Merge results                        │
└──────────────────────────────────────────────────────────┘
```

每个代理都有:
- 专注系统提示 ("你是代码审查员.你的唯一工作是找到错误. ")
  中文翻译:一个聚焦的系统提示("你是一个代码审阅者――你的唯一任务是发现错误――")
- 自己的背景窗口 (不受其他代理人的工作污染)
  中文翻译:自己的上下文窗口(不被其他代理的工作污染)
- 清晰的输出/输入合同 (收到研究说明,输出代码)
  中文翻译:清晰的输入/输出契约(接收研究笔记,输出代码)

组织者只需要了解高级任务和如何委托.它不需要知道如何完成每个子任务.每个专业代理只需要知道自己的狭窄工作.分离关注,适用于LLM.

> 编排代理只需要了解高层任务和如何委托. 它不需要知道如何完成每个子任务.

### 实际的系统

**Claude Code subagents**- 当克劳德·科德生出一个子女时`Task`孩子的工作是集中的,他回报总结.

> **Claude Code 子 Agent** 当克劳德代码 使用 `Task`生成子 时,它会创建一个具有有限范围的子代理.

模式是病毒的,因为它构成:一个副基可以产生自己的副基.在复杂的代码基础任务中,三级深度是常见的;除此之外,调试变得痛苦.

> 由于它可以组合:子代理可以产生自己的子代理.

**Devin**编程器将工作分成步骤.编程器编写代码.浏览器研究文档.每个都有不同的背景.

> **Devin** 运行一个规划代理"",编码代理和一个浏览器代理"",规划器将工作分为步骤"",编码器编写代码"",浏览器研究文档"",每个都有独立的上下文――

德文的架构是教科书监督模式:一个规划者拥有全球计划,多名专业人员执行切片.浏览器代理是有趣的.它本身是一个具有浏览工具的子代理,与编码器的环境隔离.

> 德文的架构是教科书式的监督者模式:一个拥有全局计划的规划器,多个执行切片的专家工作器.

**Multi-agent coding teams (SWE-bench)**单代理系统的得分较低. 单代理系统的得分较低.

> **多 Agent 编码团队 (SWE-bench)** SWE-bench 上表现最好的系统使用一个读取代码库的研究员,一个设计修复方案的规划器和一个实现修复编码器.

2026年SWE 位表由多代理系统主导.模式:一个研究人员具有广泛的背景来理解代码基础,一个规划者具有专注的提示来修复设计,一个编码器具有严格的键字要求来实现.每个角色都获得了所需的提示.

> 2026年SWE-bench 排名由多代理系统主导.模式:带大上下文的研究人员用于代码库理解.带焦点提示的规划器用于修复设计.带严格类型的编码器用于实现.每个角色都得到需要的提示.

**ChatGPT Deep Research**- 同时生成多个搜索代理,每个搜索不同的角度,然后合成结果.

> **ChatGPT Deep Research**并行生成多个搜索代理,每个搜索不同的角度,然后综合结果.

### 频谱

多代理不是二进制,而是频谱:

> 多代理 不是二元的.

频谱框架是重要的,因为大多数生产系统都没有任何极端.克劳德代码使用子基质 (深度一级).德文使用一个小团队.真正的研究系统使用5-50代理.频谱的正确点取决于任务复杂性.

> 光谱框架很重要,因为大多数生产系统都不任一极端.

```
SIMPLE ──────────────────────────────────────────── COMPLEX

 Single        Sub-         Pipeline      Team         Swarm
 Agent         agents

 ┌───┐       ┌───┐        ┌───┐───┐    ┌───┐───┐    ┌─┐┌─┐┌─┐
 │ A │       │ A │        │ A │ B │    │ A │ B │    │ ││ ││ │
 └───┘       └─┬─┘        └───┘─┬─┘    └─┬─┘─┬─┘    └┬┘└┬┘└┬┘
               │                │        │   │       ┌┴──┴──┴┐
             ┌─┴─┐          ┌───┘───┐    │   │       │shared │
             │ a │          │ C │ D │  ┌─┴───┴─┐    │ state │
             └───┘          └───┘───┘  │  msg   │    └───────┘
                                       │  bus   │
 1 loop      Parent +      Stage by    │       │    N peers,
 1 context   child tasks   stage       └───────┘    emergent
                                       Explicit      behavior
                                       roles
```

**Single agent**一个循环,一个提示,适合简单的任务.

> **单 Agent** 一个循环,一个提示.

**Subagents**孩子们会回报,这就是克劳德·科德所做的.

> **子 Agent** 父 代理 为聚焦子任务生成子 代理 父 维护计划 子 代理 汇报结果  这就是克劳德代码的做法

**Pipeline**对于阶段化工作流程来说,研究 -> 代码 -> 审查 -> 测试.

> **流水线** 代理 顺序运行――Agent A 的输出成为 Agent B 的输入――适合分阶段的工作流:研究 -> 编码 -> 审阅 -> 测试――

**Team**经纪人与共享信息公交行,每个人都有角色,一个管弦乐队协调员,当需要不同的技能同时时很好.

> **团队** 经纪人 通过共享消息总线并行运行.

**Swarm**没有固定管弦,代理从队列中接收工作,适合高吞吐量并行任务.

> **群体** 许多相同或近似相同的代理 共享状态――没有固定的编排器――代理从队列中获取工作――适合高吞吐量的并行任务――

### 四种多代理模式

#### 模式1:管道

```
Input ──▶ Agent A ──▶ Agent B ──▶ Agent C ──▶ Output
          (research)  (code)      (review)
```

每个代理都会转换数据,传递给人. 简单的推理. 一个阶段的失败阻了其余的阶段.

> 每个代理都转换数据并传递给下一个.

使用当:每个阶段都有明确的输入/输出,阶段自然是序列的.研究 →代码 →审查 →测试是正规的例子.避免当:阶段可以并行运行或需要它们之间的代.

> 使用场景:每个阶段有清晰的输入/输出和阶段自然顺序执行――研究 →编码 → 审阅 → 测试是典型的例子――避免:阶段可以并行或需要彼此代时――

#### 模式2: 风/风

```
                ┌──▶ Agent A ──┐
                │              │
Input ──▶ Split ├──▶ Agent B ──├──▶ Merge ──▶ Output
                │              │
                └──▶ Agent C ──┘
```

通过平行代理进行分工,然后将结果合并.

> 将工作分配给并行的代理,然后合并结果.

避免:任务分成独立的部分 (例如,搜索5个不同的来源,总结10份文件). 避免:子任务相互依赖或合并需要深入的推理.

> 使用场景:任务可以清晰分为独立部分 (如搜索 5个不同来源,总结 10 份文档) 避免:子任务相互依赖或合并需要深度推理时.

#### 模式3:乐团主持人

```
                    ┌──────────┐
                    │  Orch.   │
                    └──┬───┬───┘
                  task │   │ task
                 ┌─────┘   └─────┐
                 ▼               ▼
           ┌──────────┐   ┌──────────┐
           │ Worker A │   │ Worker B │
           └──────────┘   └──────────┘
```

智能管家决定要做什么,委托工作者,并合成结果.

> 智能编辑器决定做什么,委派给工作器,并综合结果――编辑器本身是一个具有生成工作器工具的代理――

工作过程是什么时候的? 工作过程是什么时候的? 工作过程是什么时候的?

> 使用场景:任务足够复杂,决定自己做什么是一个难题.

#### 模式4: 同龄人群

```
         ┌───┐ ◄──── msg ────▶ ┌───┐
         │ A │                  │ B │
         └─┬─┘                  └─┬─┘
           │                      │
      msg  │    ┌───────────┐     │ msg
           └───▶│  Shared   │◄────┘
                │  State    │
           ┌───▶│  / Queue  │◄────┐
           │    └───────────┘     │
      msg  │                      │ msg
         ┌─┴─┐                  ┌─┴─┐
         │ C │ ◄──── msg ────▶ │ D │
         └───┘                  └───┘
```

没有中央调整器,代理人相互沟通,决策来自互动,更难调试,但可以达到许多代理人.

> 没有中央编排器. 代理人之间点对点通信. 决策从交互中涌现. 更难调试,但可以扩展到许多代理人.

避免:需要单一一致的计划或严格的排序.

> 使用场景:许多同质代理大规模做类似工作(抓取、分类) 避免:需要单一连贯计划或严格排序时──

### 什么时候不要使用多剂

复杂性增加了多代理. 代理之间的每一个消息都是潜在的失败点. 调试从"读一场对话"到"追踪五个代理之间的消息".

> 多代理 增加了复杂性. 代理之间的每条消息都是潜在的故障点.

**Stay single-agent when:**
- 任务适合一个文本窗口 (工作数据的约100k代币以下)
  中文翻译:任务适合一个上下文窗口(工作数据不超过约100k代币)
- 你不需要不同的系统提示,
  中文翻译:不同阶段不需要不同的系统提示
- 顺序执行足够快
  中文翻译:顺序执行速度足够快
- 任务足够简单,把它分为额外的成本
  中文翻译:任务足够简单,分开增加的开销超过其价值

**The complexity cost:**
- 每个代理界限都是一个损失压缩步骤:代理A的全部文本总结为B代理的信息
  中文翻译:每一个代理 边界都是有损压缩步骤:Agent A 的完整上下文总结为发送给B 代理的消息
- 协调逻辑 (谁做什么,什么时候,什么顺序) 是其自身的错误来源
  中文翻译:协调逻辑 ((谁做什么、何时做、按什么顺序) 本身就是一个错误源
- 延迟增加:N代理意味着N连续LLM调用最小,如果他们需要回来和回来
  中文翻译:延迟增加:N 个代理意思至少N 次串行 LLM调用,如果需要来回对话则更多
- 成本乘以:每个代理独立燃烧代币
  中文翻译:成本倍增:每个代理 独立消耗代币

基本规则:如果一个任务需要不到20个工具调用,并且可以容纳100万个代币,请保持单代理.

> 经验法则:如果一个任务只需要不到20次调用工具,并且适合100k代币,就保持单个代理.

## 建立它,实现它.
```figure
swarm-messages
```

## 建立它

### 第一个步骤: 过度负载的单身代理人

现在,一个单个代理试图做一切. 它有一个巨大的系统提示和一个文本窗口,

> 这是一个试图做所有事情的单一代理. 它有一个庞大的系统提示,

```typescript
type AgentResult = {
  content: string;
  tokensUsed: number;
  toolCalls: number;
};

async function singleAgentApproach(task: string): Promise<AgentResult> {
  const systemPrompt = `You are a full-stack developer. You must:
1. Research the requirements
2. Write the code
3. Review the code for bugs
4. Write tests
Do ALL of these in a single conversation.`;

  const contextWindow: string[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const research = await fakeLLMCall(systemPrompt, `Research: ${task}`);
  contextWindow.push(research.output);
  totalTokens += research.tokens;
  totalToolCalls += research.calls;

  const code = await fakeLLMCall(
    systemPrompt,
    `Given this research:\n${contextWindow.join("\n")}\n\nNow write code for: ${task}`
  );
  contextWindow.push(code.output);
  totalTokens += code.tokens;
  totalToolCalls += code.calls;

  const review = await fakeLLMCall(
    systemPrompt,
    `Given all previous context:\n${contextWindow.join("\n")}\n\nReview the code.`
  );
  contextWindow.push(review.output);
  totalTokens += review.tokens;
  totalToolCalls += review.calls;

  return {
    content: contextWindow.join("\n---\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

这种方法的问题:
- 根据研究的过程,它包含了研究说明和代码和先前的推理.
  中文翻译:上下文窗口随着每个阶段的增长而成,
- 系统提示是通用的,不能调整每个阶段.
  中文翻译:系统提示是通用的.
- 没有什么是平行的.
  中文翻译:没有并行执行.

单代理循环迫使LLM在每一轮都在非常不同的认知任务 (研究与编码与审查) 之间切换背景.

> 单代理循环迫使LLM 每轮都在非常不同的认知任务 (研究 vs编码 vs审阅) 之间切换上下文――每次切换都损失质量――

### 第二步:专业代理人

现在分开,每个代理都能做一个工作:

> 现在分开它. 每个代理都得到一个任务:

```typescript
type SpecialistAgent = {
  name: string;
  systemPrompt: string;
  run: (input: string) => Promise<AgentResult>;
};

function createSpecialist(name: string, systemPrompt: string): SpecialistAgent {
  return {
    name,
    systemPrompt,
    run: async (input: string) => {
      const result = await fakeLLMCall(systemPrompt, input);
      return {
        content: result.output,
        tokensUsed: result.tokens,
        toolCalls: result.calls,
      };
    },
  };
}

const researcher = createSpecialist(
  "researcher",
  "You are a technical researcher. Read documentation, find patterns, and summarize findings. Output only the facts needed for implementation."
);

const coder = createSpecialist(
  "coder",
  "You are a senior TypeScript developer. Given requirements and research notes, write clean, tested code. Nothing else."
);

const reviewer = createSpecialist(
  "reviewer",
  "You are a code reviewer. Find bugs, security issues, and logic errors. Be specific. Cite line numbers."
);
```

每个专家都有一个专注的提示. 每个人都得到一个清洁的背景窗口,

> 每个专家都有一个聚焦提示. 每个人都得到一个干净的上下文窗口,只包含所需的输入.

编码器的提示是优化为写清洁代码的.评论员的提示是优化为发现错误的.没有一个提示试图做三个.

> 研究员的提示针对阅读和总结优化.编辑员的提示针对编写干净代码优化.审稿员的提示针对发现错误优化.没有单一提示试图同时做这三个事情.

### 第三步:通过信息协调

给专家们传递明确的信息:

> 通过显式消息传递将专家连接起来:

```typescript
type AgentMessage = {
  from: string;
  to: string;
  content: string;
  timestamp: number;
};

async function multiAgentApproach(task: string): Promise<AgentResult> {
  const messages: AgentMessage[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const researchResult = await researcher.run(task);
  messages.push({
    from: "researcher",
    to: "coder",
    content: researchResult.content,
    timestamp: Date.now(),
  });
  totalTokens += researchResult.tokensUsed;
  totalToolCalls += researchResult.toolCalls;

  const coderInput = messages
    .filter((m) => m.to === "coder")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const codeResult = await coder.run(coderInput);
  messages.push({
    from: "coder",
    to: "reviewer",
    content: codeResult.content,
    timestamp: Date.now(),
  });
  totalTokens += codeResult.tokensUsed;
  totalToolCalls += codeResult.toolCalls;

  const reviewerInput = messages
    .filter((m) => m.to === "reviewer")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const reviewResult = await reviewer.run(reviewerInput);
  messages.push({
    from: "reviewer",
    to: "orchestrator",
    content: reviewResult.content,
    timestamp: Date.now(),
  });
  totalTokens += reviewResult.tokensUsed;
  totalToolCalls += reviewResult.toolCalls;

  return {
    content: messages.map((m) => `[${m.from} -> ${m.to}]: ${m.content}`).join("\n\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

每个代理只收到向其发送的信息,没有环境污染.研究人员阅读的50万份文档,从来没有进入审查者的环境.

> 每个代理只收到给自己的消息. 没有上下文污染. 研究员读取的5万个代币.

根据这些数据,我们可以看到一个数据库的数据库,一个数据库的数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个数据库,一个.

> 根据"中文网"的文章,每一个代理的上下文窗口都专注于自己的任务.

### 步骤4:比较

```typescript
async function compare() {
  const task = "Build a rate limiter middleware for an Express.js API";

  console.log("=== Single Agent ===");
  const single = await singleAgentApproach(task);
  console.log(`Tokens: ${single.tokensUsed}`);
  console.log(`Tool calls: ${single.toolCalls}`);

  console.log("\n=== Multi-Agent ===");
  const multi = await multiAgentApproach(task);
  console.log(`Tokens: ${multi.tokensUsed}`);
  console.log(`Tool calls: ${multi.toolCalls}`);
}
```

多代理版本使用更多的总代币 (三代理,三个独立的LLM调用),但每个代理的背景保持清洁.由于系统提示是专业化的,每个阶段的质量都会提高.

> 多 代理 版本使用更多总代币(三个代理,三次独立的LLM调用),但每个代理的上下文保持干净――每个阶段的质量提高,因为系统提示是专业化的――

交易很清楚:花更多的代币,获得更好的产量. 值得它当任务很难. 不值得它"总结这一段落".

> 权衡很清晰:花更多的代币,获得更好的输出.任务难时值得.对"总结这一段"不值得.

## 用它实现框架

通过此课程,我们可以重新使用一个提示,`outputs/prompt-multi-agent-decision.md`现在,我们要去.

> 本课产出了一个可复制的提示,用于决定何时使用多种代理.`outputs/prompt-multi-agent-decision.md`,我知道.

提示提示提出四个诊断问题: (1) 任务是否需要100万多个工作背景代币? (2) 在不同阶段是否需要不同的专业知识? (3) 有没有并行工作? (4) 复杂性是否值得总费用?

> 提示问四个诊断问题: 1) 任务是否需要超过100k代币的工作上下文? 2) 不同阶段是否需要不同专业知识? 3) 有没有可行的工作? 4) 复杂性是否值得开销?

## 练习题

1. 添加第四位专家:一个"测试者"代理,从编码器那里接收代码,并从审查者那里审查反,然后写测试
   中文翻译:添加第四个专家:一个"测试员"代理,接收编码器的代码和审阅者的反,然后编写测试
2. 修改管道,以便审查者可以向编码器发送反,以便进行修改循环 (最大2次)
   中文翻译:修改流水线,使审阅者可以将反发送回编码器进行修改循环(最多2轮)
3. 将序列管道转换为风扇:并行运行研究人员和"要求分析器"代理,然后将其输出结合起来,然后转向编码器
   中文翻译:将顺序流水线转换为扇出:并行运行研究员和"需求分析师"代理,然后合并它们的输出再传递给编码器

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Swarm / 群体 | "A hive mind of AI agents" / "AI Agent 的蜂巢思维" | A set of peer agents with shared state and no fixed leader. Behavior emerges from local interactions. / 一组具有共享状态且无固定领导者的对等 Agent。行为从局部交互中涌现。 |
| Orchestrator / 编排器 | "The boss agent" / "老板 Agent" | An agent whose tools include spawning and managing other agents. It plans and delegates but may not do the actual work. / 一个工具包括生成和管理其他 Agent 的 Agent。它规划和委派，但可能不做实际工作。 |
| Coordinator / 协调器 | "The traffic cop" / "交通警察" | A non-agent component (often just code, not an LLM) that routes messages between agents based on rules. / 一个非 Agent 组件（通常只是代码，不是 LLM），根据规则在 Agent 之间路由消息。 |
| Consensus / 共识 | "The agents agree" / "Agent 们达成一致" | A protocol where multiple agents must reach agreement before proceeding. Used when conflicting outputs need resolution. / 多个 Agent 在继续之前必须达成一致的协议。用于需要解决冲突输出的情况。 |
| Emergent behavior / 涌现行为 | "The agents figured it out themselves" / "Agent 自己想出来的" | System-level patterns that arise from agent interactions but were not explicitly programmed. Can be useful or harmful. / 从 Agent 交互中产生但未被明确编程的系统级模式。可能有用也可能有害。 |
| Fan-out / fan-in / 扇出/扇入 | "Map-reduce for agents" / "Agent 的 Map-reduce" | Splitting a task across parallel agents (fan-out), then combining their results (fan-in). / 将任务分配给并行 Agent（扇出），然后合并它们的结果（扇入）。 |
| Message passing / 消息传递 | "Agents talk to each other" / "Agent 之间互相交谈" | The communication mechanism between agents: structured data sent from one agent to another, replacing shared context windows. / Agent 之间的通信机制：从一个 Agent 发送到另一个 Agent 的结构化数据，替代共享上下文窗口。 |

## 继续阅读 继续阅读

- [The Landscape of Emerging AI Agent Architectures](https://arxiv.org/abs/2409.02977)- 调查多代理模式
  中文翻译:新兴AI代理 架构概述  多代理 模式综述
- [AutoGen: Enabling Next-Gen LLM Applications](https://arxiv.org/abs/2308.08155)- 微软的多代理对话框架
  中文翻译:AutoGen:赋能下一代 LLM 应用  微软的多代理对话框架
- [Claude Code subagents documentation](https://docs.anthropic.com/en/docs/claude-code)- 克劳德·科德如何委托任务
  中文翻译:Claude Code 子 代理 文档 Claude Code 如何使用任务委派
- [CrewAI documentation](https://docs.crewai.com/)-基于角色的多代理框架
  中文翻译:CrewAI 文档  基于角色的多代理 框架
