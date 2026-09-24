# 代理与代理协议

> 现在,我们需要一个代理.  A2A (Agent2Agent) 是一个允许不同框架构建的不透明代理合作的开放协议. 谷歌于2025年4月发布,并于2025年6月捐赠给Linux基金会,并在2026年4月获得了150多个支持者,包括AWS,Cisco,微软,Salesforce,SAP和ServiceNow. 它吸收了IBM的ACP,并增加了AP2支付延长. 这一课讲述了特工卡,任务生命周期,

> **【中文解读】**据悉,在该协议中,该协议的内容是: 通过"互动互动"协议,将"互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动互动的互动互动互动

> **【拓展】**A2A与MCP是互补而不是替代关系.MCP用于调用具体工具,A2A用于将整个任务委托给另一个代理.`/.well-known/agent.json`) 与MCP的工具发现机制类似,但描述的是代理的能力而不是工具.

>  **【前置】**学本节前请先掌握:(1) 阶段13·06(MCP基础) 和13·08(MCP客户端) 理解MCP是代理到工具,本节是代理到代理;(2) HTTP + JSON-RPC 基础;(3) SSE 或轮询机制A2A任务 状态订阅;(4) 异步任务概念,可参考阶段13·13。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, Agent Card + Task harness) | **语言:** Python (stdlib, Agent Card + Task harness)
**Prerequisites:** Phase 13 · 06 (MCP fundamentals), Phase 13 · 08 (MCP client) | **前置知识:** Phase 13 · 06 (MCP fundamentals), Phase 13 · 08 (MCP client)
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 区分代理到工具 (MCP) 与代理到代理 (A2A) 使用情况.
  中文翻译:区分 代理工具(MCP) 和 代理代理(A2A) 用例──
- 在 发行代理卡`/.well-known/agent.json`具有技能和终端数据.
  中文翻译:在`/.well-known/agent.json`发布带技能和端点元数据的代理卡.
- 查看任务生命周期 (提交 -> 工作 -> 输入要求 -> 完成 / 失败 / 取消 / 拒绝).
  中文翻译:走通任务 生命周期 (中文翻译:走通任务 生命周期)
- 使用部分 (文字,文件,数据) 和文物的消息作为输出.

> **【中文解读】**学习目标:区分代理工具 (MCP) 与代理用例 (A2A);发布代理卡;走通任务 生命周期;使用带零件的信息和文物输出――

## 问题 问题引入

> **【中文解读】**客服 需要将报告写作委托给专门写作 代理──A2A 之前的选择(定制 REST API、共享代码库、MCP) 都不合适──A2A 将交互建模为一个代理 向另一个代理 发送任务,具有生命周期、消息和工件──被调用 代理内部状态保持不透明调用者只看到任务状态转换和最终输出──

客户服务代理需要将报告编写委托给专业的作家代理.

> 客服 需要将报告写作委托给专门写作 代理──A2A 之前的选项:

- 定制RESTAPI,但每次配对都是一次性的.
  中文翻译:定制 REST API──可行但每个配对都是一次性──
- 需要两个代理运行相同的框架.
  中文翻译:共享代码库.
- 没有合适:MCP是用来调用工具,而不是两个代理合作,同时保持每个代理的不透明的内部推理.
  中文翻译:MCP──不合适:MCP 用于调用工具,而不是两个代理在保持各自的不透明内部推理下协作──

A2A填补了空白.它模拟了一个代理向另一个代理发送任务的交互,使用生命周期,消息和文物.所谓的代理内部状态保持不透明.

> 填充空白. 它将交互建模为一个代理向另一个发送任务,带生命周期,消息和工件. 被调用代理内部状态保持不透明.调用者只看到任务状态转换和最终输出.

 A2A 是"让跨框架的代理人相互交谈"协议. 它不取代MCP;这两种协议是互补的.

>  A2A 是"让跨框架代理交谈"的协议.

>  **【类比】**A2A与MCP 像公司"外包项目"与"公司内调用工具"──MCP是工程师 (工程师) 用计算器 (计算器) 工具 (工具) 他知道计算器怎么工作、用完就完成,是工具调用──A2A是公司 A 将整个项目 (任务) 外包给公司 B (另一家代理) A不知道 B 内部怎么做(不透明),只看交付物品;;B 是独立法人有自己的工作流程,自己的工具,自己的内部状态──A2A 关心任务边界,交付格式、回报,不关心 B 使用什么框架(长链还是自动生成) 实现.

## 概念的核心概念

### 代理卡

> **【中文解读】**每个A2A兼容的代理人在`/.well-known/agent.json`发布卡片,包含名称,描述,URL,版本,技能列表和能力声明.

每个符合A2A的代理人都会在`/.well-known/agent.json`其他:

> 每个A2A兼容代理都在`/.well-known/agent.json`发布卡片:

```json
{
  "schemaVersion": "1.0",
  "name": "research-agent",
  "description": "Summarizes academic papers and drafts citations.",
  "url": "https://research.example.com/a2a",
  "version": "1.2.0",
  "skills": [
    {
      "id": "summarize_paper",
      "name": "Summarize a paper",
      "description": "Read a paper PDF and produce a 3-paragraph summary.",
      "inputModes": ["text", "file"],
      "outputModes": ["text", "artifact"]
    }
  ],
  "capabilities": {"streaming": true, "pushNotifications": true}
}
```

发现是基于URL的:拿到卡片,学习A2A终端点的URL,列出技能.

> 发现基于URL:获取卡片,学习A2A端点URL,枚举技能.

### 签署的代理卡 (AP2)

发布者用JWT签署自己的卡;消费者验证.防止伪造.

> 扩展 (AP2) 为了代理卡 添加密签名──发行者使用JWT 签名自己的卡片;消费者验证──防止冒充──

### 任务生命周期

> **【中文解读】**任务生命周期:提交 -> 工作 -> 完成 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功 没有成功`tasks/send`发起,通过SSE 订阅状态更新或轮询.

```
submitted -> working -> completed | failed | canceled | rejected
             -> input_required -> working (loop via message)
```

客户开始使用`tasks/send`调用代理通过州进行过渡;客户通过SSE或民意调查订阅状态更新.

> 客户端使用`tasks/send`发起──被调用 通过状态转换;客户端通过 SSE或轮询订阅状态更新──

> ️ **【易错点】**场景:A2A 调用方在`submitted`状态后立刻等等`completed`而不处理`input_required`后果:被调用 需要补充信息时卡在`input_required`调用方式误以为还在`working`永久等待,整个工作流死锁 / 修复:(1) 调用方必须实现完整的任务 生命周期状态机,每个状态都有操作员;(2) `input_required`时主动拉取消息内容并触发新一轮`tasks/send`设置总超时 (如10分钟),到达后取消任务并报错.

>  **【困惑】**问:既然A2A是代理对代理,那代理A怎么知道代理B信任它、会不会拒绝?A:信任通过代理卡+AP2签名建立:(1) 代理卡描述能力,AP2使用JWT签名防冒充;(2) 调用前A通常通过OAuth等机制拿到B的访问代币;(3) B可以拒绝(`rejected`状态),如调用方没付费 (AP2 支付扩展) 权限不足,负载过满;

### 信息和部分

信息包含一个或多个部分:

> 一条消息带着一个或多个部分:

- `text` 简单内容.
  翻译: 中文`text`纯文本内容.
- `file`使用mimeType的64基块.
  翻译: 中文`file`基64片带mimeType──
- `data`输入JSON有效载荷 (为所调用的代理进行结构化输入).
  翻译: 中文`data`类型化JSON 载荷(被调用代理的结构化输入) 』

举个例子:

```json
{
  "role": "user",
  "parts": [
    {"type": "text", "text": "Summarize this paper."},
    {"type": "file", "file": {"name": "paper.pdf", "mimeType": "application/pdf", "bytes": "..."}},
    {"type": "data", "data": {"targetLength": "3 paragraphs"}}
  ]
}
```

### 艺术品

输出是艺术品,而不是原始字符串.

> 输出是艺术品,而不是裸字符串.

```json
{
  "name": "summary",
  "parts": [{"type": "text", "text": "..."}],
  "mimeType": "text/markdown"
}
```

艺术品可以作为块流传.

> 作为块流式传输.

### 两项运输义务

1. **JSON-RPC over HTTP.** `/a2a`终端点,请求的POST, 流媒体的SSE.
  翻译: 中文**JSON-RPC over HTTP。** `/a2a`端点、POST 用于请求、可选SSE 用于流式──默认绑定──
2. **gRPC.**对于gRPC原生企业环境.
  翻译: 中文**gRPC。**采用GRPC原生企业环境.

两个结合都具有相同的逻辑信息形状.

> 两种绑定带着相同的逻辑信息形式.

### 保持空位

> **【中文解读】**不透明性保持:被调用的代理内部状态是不透明的.调用者只看到任务状态和工件,看不到链式思考工具调用或下代理委托.

设计原理:调用代理的内部状态不透明.调用者看到任务状态和文物.调用代理的思想链,其工具调用,其子代理委托都看不见.这与MCP不同,工具调用是透明的.

> 关键设计原则:被调用的代理内部状态不透明――调用者看任务状态和工件――被调用的代理的思维链、工具调用、子代理委托全部不可见――这与MCP不同,MCP的工具调用是透明的――

理由:A2A允许竞争对手在不透露内部信息的情况下协作.A2A可以是"调用这个客户服务代理"而不需要调用者学习该代理如何实现服务.

> 原则:A2A 让竞争对手在未被曝内部的情况下协作.A2A可以是"调用此客服代理",而调用者不需要学习该代理如何实现服务.

### 时间线

- **2025-04-09.**谷歌宣布A2A.
  翻译: 中文**2025-04-09。**谷歌宣布A2A.
- **2025-06-23.**捐给Linux基金会.
  翻译: 中文**2025-06-23。**捐赠给Linux基金会
- **2025-08.**吸收IBM的ACP.
  翻译: 中文**2025-08。**吸收IBM的ACP.
- **2025-09.**扩展AP2 (代理支付) 船舶.
  翻译: 中文**2025-09。**经理 支付) 发布.
- **2026-04.**版本 1.0 发布了150多个支持组织.
  翻译: 中文**2026-04。**支持组织.

### 与MCP的关系

| Dimension | MCP | A2A |
|-----------|-----|-----|
| Use case | Agent-to-tool | Agent-to-agent |
| Opacity | Transparent tool calls | Opaque inner reasoning |
| Typical caller | Agent runtime | Another agent |
| State | Tool-call result | Task with lifecycle |
| Authorization | OAuth 2.1 (Phase 13 · 16) | JWT-signed Agent Cards (AP2) |
| Transport | Stdio / Streamable HTTP | JSON-RPC over HTTP / gRPC |

许多生产系统都使用MCP,用于工具层,A2A用于协作层.

> 想调用特定工具时使用MCP──想将整个任务委托给另一个代理时使用A2A──许多生产系统都使用:

## 用它实现框架

> **【中文解读】** `code/main.py`实现最小A2A线束:研究 代理 发布卡片,写作 代理 接收 `tasks/send`经历工作 -> 输入_要求 -> 工作 -> 完成 生命周期,返回文本文本文物――全部标准库,使用内存传输关注消息形状――
```figure
a2a-task-lifecycle
```

## 用它

`code/main.py`通过A2A的最小化,研究代理发布卡,编写代理获得A2A的卡.`tasks/send`通过工作 → input_required → working → 完成的转换,并返回文本文物.所有 stdlib; 使用内存运输以关注消息形状.

> `code/main.py`实现最小A2A线束:研究 代理 发布卡片、写作 代理 接收 `tasks/send`经历工作 →输入_要求 →工作 →完成、返回文本文本文物──全部标准库;使用内存传输以聚焦消息形态──

什么要看:

- 机器人卡的JSON形状.
  中文翻译:代理卡JSON形态。
- 任务 ID 分配和状态过渡.
  中文翻译:任务 id 分配和状态转换――
- 混合型零件的消息.
  中文翻译:带混合类型部分的消息.
- 需要输入的分支在任务中.
  中文翻译:任务中的输入要求分支──
- 工艺品在完成后返回.
  中文翻译:完成时返回文物──

## 运送它.

> **【中文解读】**本课产出发 `outputs/skill-a2a-agent-spec.md`给一个新的可调用其他代理代理,生成代理卡JSON、技能模式和端点蓝图.

这一课产生了`outputs/skill-a2a-agent-spec.md`由于一个新的代理,该技能应该被其他代理调用, 产生的代理卡JSON,技能方案,和终点蓝图.

> 本课产出发 `outputs/skill-a2a-agent-spec.md`△给一个可以被其他代理调用的新代理,该技能产生代理卡JSON、技能方案和端点蓝图――

## 练习题

1. 跑步`code/main.py`追踪任务的整个生命周期,包括调用代理要求澄清的输入暂停.
   中文翻译:运行 `code/main.py`查完整任务 生命周期,包括被调用代理 请澄清的输入-要求暂停

2. 加入一个签名的代理卡,用HMAC签名卡的正规JSON,写一个验证器,确认它在一个突变的卡上失败.
   中文翻译:添加签名 代理卡――使用HMAC对卡片的规范 JSON签名――写验证器,确认对变异卡片失败――

3. 执行任务流:编写代理通过SSE发射三个增量文物块,调用者积累它们.
   中文翻译:实现任务流式:写作 通过SSE发出三个增量文物块,调用者累积它们――

4. 设计一个 A2A 代理,将一个 MCP 服务器包裹起来.将每个 MCP 工具映射到一个 A2A 技能.注意交易.
   中文翻译:设计包装MCP 服务器的A2A代理.

5. 阅读A2A v1.0公告并确定截至2026年4月,没有任何框架实施的唯一功能. (提示:它涉及多跳任务委托).
   中文翻译:阅读A2A v1.0 公告,识别截至2026年4月尚未被任何框架实现的一个功能──(提示:与多跳任务委托有关──)

## 关键词 快速查找表

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| A2A | "Agent-to-Agent protocol" | Open protocol for opaque agent collaboration | Agent 间通信协议 |
| Agent Card | "`.well-known/agent.json`" | Published metadata describing an agent's skills and endpoint | Agent 卡片：发布能力元数据 |
| Skill | "A callable unit" | A named operation the agent supports (analog to MCP tool) | 技能：Agent 支持的可调用操作 |
| Task | "Unit of delegation" | A work item with a lifecycle and final artifact | 任务：带生命周期的委托工作单元 |
| Message | "Task input" | Carries Parts (text, file, data) | 消息：携带 Parts 的任务输入 |
| Part | "Typed chunk" | `text` / `file` / `data` element of a message | 部件：消息的类型化元素 |
| Artifact | "Task output" | Named, typed output returned on completion | 工件：完成时返回的命名类型化输出 |
| AP2 | "Agent Payments Protocol" | Signed Agent Cards extension for trust and payments | Agent 支付协议：签名卡片扩展 |
| Opacity | "Black-box collaboration" | Called agent's internals are hidden from caller | 不透明性：被调用方内部隐藏 |
| Input-required | "Task pause" | Lifecycle state when the agent needs more info | 输入要求：任务暂停等待更多信息 |

## 继续阅读 继续阅读

- [a2a-protocol.org](https://a2a-protocol.org/latest/)可нони A2A规范
  中文翻译:权威 A2A 规范
- [a2aproject/A2A — GitHub](https://github.com/a2aproject/A2A)参考实施和SDK
  中文翻译:参考实现和SDK
- [Linux Foundation — A2A launch press release](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents) 2025年6月 管理转让
  中文翻译:2025年6月治理转移
- [Google Cloud — A2A protocol upgrade](https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade)路线图和合作伙伴势头
  中文翻译:路线图和伙伴势头
- [Google Dev — A2A 1.0 milestone](https://discuss.google.dev/t/the-a2a-1-0-milestone-ensuring-and-testing-backward-compatibility/352258) v1.0 发布说明和后退型紧指导
  中文翻译:v1.0 发行说明和向后兼容指南
