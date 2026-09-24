# 代理与代理协议

> 谷歌于2026年4月宣布A2A;到2026年4月,https://a2a-protocol.org/latest/specification/其他150多个组织支持它. A2A是MCP的水平补充 (课13):MCP是垂直的 (代理工具),A2A是同等的 (代理代理). 它定义了代理卡 (发现),具有文物 (文本,结构数据,视频) 的任务,不透明的任务生命周期和 auth. 生产系统越来越多地将MCP与A2A结合起来. 在2025-2026年期间,谷歌云将A2A支持推向Vertex AI代理构建器.

> **【中文解读】**谷歌在2025年4月发布了A2A协议;到2026年4月,规范已有150+ 组织支持.A2A是MCP的水平补充:MCP是垂直的(代理与工具),A2A是点对点的(代理与代理) ⋅定义了代理卡 (发现) ‧带产品任务、不透明任务生命周期和认证――生产系统越来越多地将MCP与A2A 配对使用.

> **【拓展：A2A → Google 的 Agent 协议】**A2A是谷歌主导的代理间通信标准协议,与人类的MCP (Mode Context Protocol) 互补.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `http.server`, `json`) | **语言:** Python (标准库, `http.server`, `json`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前请先掌握:阶段13·15-20(MCP 协议套件) 、阶段16·04(原语) ・・・A2A 是MCP 的水平补充:MCP=代理调工具(垂直),A2A=代理找代理(横向) ・・・
>  **【类比】**据悉,在中国,中国的市场上,中国的市场市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场上,市场的价格差异势,以及其他其他.

## 问题 问题引入

您的代理需要在另一个系统中调用另一个代理. 如何?您可以暴露HTTP终端点,定义一个定制的JSON方案,并希望另一方说. 每个对代理都会成为自定义集成.

> 你的代理需要调用另一个系统上的代理.你可以暴露一个HTTP端点,定义一个定制JSON模式,并希望另一个端能够理解它.

对于N代理,你需要N×(N-1) / 2的定制集成. 10代理,这是45个集成. 100代理,4950.A2A将这分解为N代理卡,每个描述一个代理.

> 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个 个

作为一个"标准发现",标准任务模型,标准运输,标准文物.

> 标准发现标准任务模型标准传输标准工件就像HTTP+REST,但作为代理作为一等公民.

关键抽象:代理是可地址的,可发现的网络终端点.你不"进口"代理,你"调用"它. 这将分离部署代理运行到任何地方,在任何语言,使用任何框架,只要它说A2A.

> 关键抽象:代理是可寻址、可发现的网络端点──你不"导入"代理;你"调用"它──这解已部署代理运行在任何地方、使用任何语言、使用任何框架,只要它说A2A──

## 概念的核心概念

### 它们的四个元素

> 四个元素

**Agent Card.**在 `/.well-known/agent.json`描述代理人:名称,技能,终点,支持的模式,作者要求.

> **Agent 卡片。**位于`/.well-known/agent.json`通过读取卡片进行发现.

已知URL公约反映了网络标准 (`/.well-known/`是相同的路径.`robots.txt`任何A2A兼容的代理都可以通过获取URL来发现.

> 知名URL 约定镜像 网络标准`/.well-known/`是用于`robots.txt`△ACME 挑战、OIDC 发现的相同路径) △任何A2A 兼容代理都可以通过获取该URL 发现──不需要注册表、代理或中央目录──

**Task.**工作单位,一个没有同步的状态的对象,生命周期:`submitted -> working -> completed / failed / canceled`客户发送任务,投票或订阅更新.

> **任务。**工作单元──具有生命周期的异步有状态对象:`submitted -> working -> completed / failed / canceled`△客户端发送任务,轮询或订阅更新──

**Artifact.**结果类型由任务生成.文本,结构化JSON,图像,视频,音频.艺术品是打字,所以不同的模式是第一类.

> **工件。**任务产生的结果类型――文本、结构化 JSON、图像、视频、音频――工件是有类型的,因此不同模态是平等的公民──

**Opaque lifecycle.**客户端可以看到状态过渡和文物;实现可以使用任何框架.

> **不透明生命周期。**客户端看到状态转换和工件;实现可以自由使用任何框架――

基于LangGraph,CrewAI或定制Python脚本的远程代理都看起来与A2A客户端相同.互操作性来自于同意线程格式,而不是内部.

> 这种不透明性是设计的.基于LangGraph、CrewAI或自定义Python脚本的远程代理构建的A2A客户端看起来都是一样的.互操作性来自于线上协议格式,而不是内部.

###  MCP/A2A 分裂

- **MCP**通过JSON-RPC读取/写入工具服务器.默认无状态.
  翻译: 中文**MCP**通过JSON-RPC 读写工具服务器──默认无状态──
- **A2A**两方都是有自己的推理的代理人.
  翻译: 中文**A2A**代理人――对等协议;双方都是有自己的推理代理人――

两者都使用多代理系统. 一个A2A同行在其侧面调用MCP工具. 分裂使两个问题保持清洁.

> 产多代理 系统 两者都使用 A2A 对等端调用 MCP 工具 这种分离保持了两个关注点的清晰度 

常见模式:公司A的A2A"研究代理"内部调用MCP搜索工具服务器,然后将其结果返回公司B的A2A"分析代理".跨组织通信是A2A;内部工具使用是MCP.每个协议都做出最好的.

> 常见模式:公司A的A2A"研究代理"内部调用MCP 搜索工具服务器,然后将发现返回公司B的A2A"分析师代理"――跨组织通信是A2A;内部工具使用是MCP――每个协议做最好的事――

或是通过流媒体:`/tasks/{id}/events`为了推迟更新.

> 或使用流式:SSE 订阅 `/tasks/{id}/events`获取推送更新.

### 标签:

支持A2A的模式有三个常见:

> 支持三种常见模式:

三个模式涵盖了"我信任我的身份提供商" (OAuth2载体) 到"我们相互验证" (mTLS) 到"我们不信任任何第三方" (HMAC签名).选择符合您的安全要求的最轻量级的.

> 三种模式涵盖从"我信任我的身份提供商" (OAuth2承载者) 到"我们互相验证" (MTLS) 到"我们不信任任何第三方" (HMAC签名) 的范围.

- **Bearer token** OAuth2 或不透明.
  翻译: 中文**Bearer token** OAuth2 或不透明令牌
- **mTLS**互联网服务系统;组织证明彼此的身份.
  翻译: 中文**mTLS**双向TLS;组织相互证明身份──
- **Signed requests**HMAC在有效载荷上.
  翻译: 中文**签名请求**对有效载荷的HMAC──

代理卡上公布了作者,客户发现并遵守.

> 认证在代理卡中声明;客户端发现并遵守.

### 到2026年4月,将有150多个组织

企业采用推动了A2A规模.标题:A2A成为企业代理系统跨越信任界限的方式.谷歌云提供了Vertex AI代理构建器A2A支持;微软代理框架支持它;大多数主要框架 (LangGraph,CrewAI,AutoGen) 运送A2A适配器.

> 企业采用推动了A2A的规模化. 标题:A2A 成为企业代理 系统跨越信任边界的方式. Google Cloud 提供了 Vertex AI 代理构建器A2A 支持;微软代理框架支持它;大多数主要框架 (长图,机器人,自动机) 提供A2A 适配器.

由于A2A在FIPA-ACL失败的情况下获得了企业采用:A2A是JSON原生,使用现有的网络基础设施 (HTTP,SSE,OAuth),不需要共享的类.FIPA的通用费是杀手;A2A学到了教训.

> 由于A2A在企业采用中获胜而FIPA-ACL失败的原因:A2A是JSON原生的、利用现有Web基础设施(HTTP、SSE、OAuth)、不需要共享本体──FIPA的开销是致命的;A2A学到了教训──

### 在A2A获胜的地方

- **Cross-organization calls.**没有A2A,每一个对都是个定制合同.
  翻译: 中文**跨组织调用。**公司A的代理人调用公司B的代理人.
- **Heterogeneous frameworks.**拉格格拉夫代理调用CrewAI代理调用定制Python代理.
  翻译: 中文**异构框架。**拉格格拉夫代理调用CrewAI代理调用自定义Python代理 A2A 标准化
- **Typed artifacts.**视频结果,结构化JSON,音频所有都是一流的.
  翻译: 中文**类型化工件。**视频结果、结构化 JSON、音频都是一等公民──
- **Long-running tasks.**模糊的生命周期+民意调查使得长达几个小时的任务变得简单.
  翻译: 中文**长时间运行的任务。**透明的生命周期+轮询使小时级任务变得简单.

### 亚2A在哪里努力

- **Latency-sensitive micro-calls.**亚2A的生命周期是异步的.
  翻译: 中文**延迟敏感的微调用。**亚毫秒级代理对代理不适合;使用直接的PCR.
- **Tight-coupled in-process agents.**如果两个代理运行相同的Python进程, A2A的HTTP回路是过度的.
  翻译: 中文**紧耦合的进程内 Agent。**如果两个代理运行在同一 Python 进程中,A2A 的 HTTP 往返是过度设计.
- **Small teams.**具体的通用费用是真实的; 只有内部代理人可能不需要正式的.
  翻译: 中文**小团队。**规范开销是真实的; 只有内部代理可能不需要这种正式性.

### 亚2A对ACP,ANP,NLIP

在2024-2026年出现了几个相关规格:

> 在2024-2026年间出现了几个相关规范:

- **ACP** A2A的前身,范围较窄.
  翻译: 中文**ACP** A2A 的前身,范围更窄.
- **ANP**同行发现重,分散的第一.
  翻译: 中文**ANP**重对等发现,去中心化优先.
- **NLIP**(Ecma自然语言互动协议,标准化2025年12月) 自然语言内容类型.
  翻译: 中文**NLIP**语言内容类型: 语言内容类型:

截至2026年4月,A2A是最多采用的同行协议. 参见 arXiv:2505.02279 (Liu等人",对代理互操作性协议的调查").

> 截至2026年4月,A2A是采用最广泛的对等协议.

2026年协议景观稳定了:A2A用于代理合作,MCP用于工具,ACP用于轨迹记录,ANP用于跨组织身份.NLIP仍然是个位.新提案需要证明真正的差距才能获得吸引力.

> 2026年协议格局已经稳定:A2A 用于代理协作,MCP 用于工具,ACP 吸收A2A 用于轨迹日志,ANP 用于跨组织身份――NLIP 仍然小众――新提案需要展示真正的差距才能获得关注――

## 建立它,实现它.
```figure
sw-agent-card-discovery
```

## 建立它

`code/main.py`实现A2A最小服务器和客户端使用`http.server`服务器:

> `code/main.py`使用 `http.server`和 JSON 实现A2A 最小服务器和客户端.

- 暴露`/.well-known/agent.json`没有任何
  中文翻译:暴露`/.well-known/agent.json`没有任何
- 接受`POST /tasks`没有任何
  中文翻译:接受 `POST /tasks`没有任何
- 管理任务状态,
  中文翻译:管理任务状态,
- 返回文物`GET /tasks/{id}`现在,我们要去.
  中文翻译:在`GET /tasks/{id}`返回工件.

客户:

> 客户端:

- 拿到代理卡,
  中文翻译:获取代理卡片,
- 提交任务,
  中文翻译:提交任务,
- 投票直到完成,
  中文翻译:轮询直到完成,
- 读到文物.
  中文翻译:读取工件。

脚本将服务器启动在一个背景线程中,然后将客户端运行到它.

> 脚本在后台线程中启动服务器,然后运行客户端──你看到完整流程:发现,提交,轮询,工件──

## 用它实现框架

`outputs/skill-a2a-integrator.md`设计A2A集成:代理卡内容,任务方案,作者选择,流媒体与民意调查.

> `outputs/skill-a2a-integrator.md`设计A2A 集成:代理 卡片内容、任务模式、认证选择、流式 vs 轮询──

## 运送它.

检查列表:

> 检查清单:

- **Pin the spec version.**现在A2A还在发展, 代理卡应该声明协议版本.
  翻译: 中文**固定规范版本。**果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司 果公司
- **Idempotent task creation.**复制提交 (网络重试) 应产生一个任务.
  翻译: 中文**幂等任务创建。**重复提交 (网络重试) 应产生一个任务.
- **Artifact schemas.**声明代理返回的形状;消费者应验证.
  翻译: 中文**工件模式。**声明 代理 返回什么形状;消费者应验证.
- **Rate limits + auth.** A2A 面向公众; 应用标准的网络安全.
  翻译: 中文**速率限制 + 认证。**面向公众;应用标准网络安全.
- **Dead-letter for failed tasks.**随着时间的推移,检查出现重复故障的模式.
  翻译: 中文**失败任务死信。**随着时间检查模式,发现出现的失败类型.

## 练习题

1. 跑步`code/main.py`确认客户发现服务器并收到正确的文物.
   中文翻译:运行 `code/main.py`❖确认客户端发现服务器并接收正确的工件――
2. 添加第二个技能到服务器上 (例如",总结").更新代理卡. 写一个基于任务类型的客户端选择技能.
   中文翻译:向服务器添加第二个技能(如"总结")。更新 代理卡片──编写根据任务类型选择技能的客户端──
3. 实现SSE流通终端: `/tasks/{id}/events`客户需要做什么不同?
   中文翻译:实现SSE 流式端点:`/tasks/{id}/events`客户端需要做什么不同的事情?
4. 阅读A2A规范. 确定规范要求不执行的三个东西.
   中文翻译:阅读A2A规范――识别规范要求的三个演示未实现的东西――
5. 比较A2A (代理卡发现) 和MCP (通过服务器端能力列表)`listTools`自我描述的代理人和能力测试之间的差别是什么?
   中文翻译:比较A2A(代理卡片发现) 与MCP(通过 `listTools`服务器端能力表) ‧自定义 代理和探测能力之间的权衡是什么?

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| A2A | "Agent-to-agent" / "Agent 对 Agent" | Peer protocol for agents to call other agents across systems. Google 2025. / Agent 跨系统调用其他 Agent 的对等协议。Google 2025。 |
| Agent Card / Agent 卡片 | "The agent's business card" / "Agent 的名片" | JSON at `/.well-known/agent.json` describing skills, endpoints, auth. / 描述技能、端点、认证的 JSON。 |
| Task / 任务 | "The unit of work" / "工作单元" | Async stateful object with a lifecycle; artifacts produced on completion. / 具有生命周期的异步有状态对象；完成时产生工件。 |
| Artifact / 工件 | "The result" / "结果" | Typed output: text, structured JSON, image, video, audio. First-class media. / 类型化输出：文本、结构化 JSON、图像、视频、音频。一等媒体。 |
| Opaque lifecycle / 不透明生命周期 | "How it's solved is the agent's business" / "如何解决是 Agent 的事" | Client sees state transitions; server is free to choose framework/tools. / 客户端看到状态转换；服务器自由选择框架/工具。 |
| Discovery / 发现 | "Finding the agent" / "找到 Agent" | `GET /.well-known/agent.json` returns the card. / 返回卡片的 GET 请求。 |
| MCP vs A2A | "Tools vs peers" / "工具 vs 对等" | MCP: vertical agent <-> tool. A2A: horizontal agent <-> agent. / MCP：垂直 Agent <-> 工具。A2A：水平 Agent <-> Agent。 |
| ACP / ANP / NLIP | "Sibling protocols" / "兄弟协议" | Adjacent specs; A2A is the most-adopted 2026. / 相邻规范；A2A 是 2026 年采用最广泛的。 |

## 继续阅读 继续阅读

- [A2A specification](https://a2a-protocol.org/latest/specification/)法典规范
  中文翻译:A2A 规范  权威规范
- [Google Developers Blog — A2A announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)2025年4月发射时间
  中文翻译:谷歌 开发者博客  A2A 公告  2025 年 4 月发布文章
- [A2A GitHub repo](https://github.com/a2aproject/A2A)参考实施和SDK
  中文翻译:A2A GitHub 仓库  参考实现和SDK
- [Liu et al. — A Survey of Agent Interoperability Protocols](https://arxiv.org/html/2505.02279v1) MCP, ACP,A2A,ANP比较
  中文翻译:Liu 等人  代理 互操作性协议综述  MCP、ACP、A2A、ANP 比较
