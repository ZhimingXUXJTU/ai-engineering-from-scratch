# 果和果:生产时间
# 快速实例化和类型工作流程

> 生产代理运行时间优化了原型框架忽略的内容:实例化成本,打字工作流表面和服务准备的后端. 2026 配对:Agno (Python) 旨在实现微秒代理实例化和无状态FastAPI后端.Mastra 将代理,工具,工作流程,统一模型路由和复合存储放在Vercel AI SDK基板上.

**Type:** Learn | **类型:** 学习
**Languages:** Python, TypeScript | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 13 (LangGraph) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

## 学习目标

- 确定阿格诺的性能目标,以及它们什么时候重要.
- 命名Mastra的三个原始物件 代理,工具,工作流程 和支持的服务器适配器.
- 解释为什么无状态的FastAPI后端是AgnO生产路径的建议.
- 选择给定的堆 (Python-first vs TypeScript-first).

## 问题 问题引入

拉格格拉夫,自动生成,CrewAI是框架重的.想要"只需要代理循环,快速,在我的运行时间"的团队可以使用Agno (Python) 或Mastra (TypeScript).这两者都以原始的速度和更紧密的适应环境堆来交易一些框架所有的原始.

> 长图,自动生成,机组都是偏重的框架. 想要"只要代理循环,快速,在我的运行中"的团队会选择Agno (Python) 或Mastra (TypeScript) 两者都放弃了一些自带的框架原语,换取原始速度和与周围技术更紧密的适应.


> **【中文解读】**亚格诺和马斯特拉代表了2026年的两种代理 运行时设计哲学――亚格诺(原 PhiData) 追求极简使用最小代码构建代理――马斯特拉(类型文字) 追求全功能提供完整的代理 生命周期管理――选择取决于团队的技术和复杂性需求――

> **{【拓展：Agno (GitHub 15k+ stars) 和 Mastra 是 2026 年 Agent 运...】}**亚格诺 (GitHub 15k+星) 和马斯特拉是2026年代理运行时的新秀――阿格诺的哲学是'Agent 即函数' 每个代理是带有工具集的异步函数――马斯特拉基于TypeScript,面向全开发者,提供完整的代理生命周期管理(部署、监控、扩展) ――两者都支持多模型后端和MCP 集成――

>  **【前置】**必须先掌握:阶段14·01(代理循环) 和阶段14·13(长度图) 本节是这两者的"轻量替代品"――如果你不知道为什么要"轻量化"长度图,说明你还没在生产中遇到长度图的工程负担,建议先使用长度图 几周再回头看本节――

## 概念的核心概念

### 果

- 之前是Python运行时间,
- "没有图形,链条,或复杂的模式,
- 根据其文件的性能目标: ~ 2μs 代理实例化, ~ 3.75 KiB 存储量每代理, ~ 23 个模型提供商.
- 制作路径:无状态的会话缩写 FastAPI 后端. 每个请求都启动一个新的代理;会话状态在DB中.
- 产生的多模 (文字,图像,音频,视频,文件) 和代理RAG.

速度目标在每秒有数千个短暂的代理时重要 (聊天风扇,评估管道),而当一个代理运行10分钟时,它们更不重要.

>  **【类比】**长图像:摩托车启动快,轻便,能钻小 () ◎2μs 实例化,3.75 KiB 内存),适合短途高频通勤,每秒数千短任务;SUV装得多,能长途跑,有空调导航,但启动,慢占地大.**关键洞察**选择Agno 不是因为它"更好",而是因为你的场景是"高频短任务"长图 在这里浪费资源.

> 速度目标是很重要的,当你每秒有数千个短暂的代理.

> 亚格诺和马斯特拉是两种轻量级的代理 运行时时.亚格诺专注于快速构建,马斯特拉专注于TypeScript 生产部署.

### 马斯特拉

- 基于Vercel AI SDK的TypeScript.
- 三个原始:**Agents**现在**Tools**子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子**Workflows**现在,我们要去.
- 统一型路由器  3,300+ 型号在 94 个供应商中 (2026 年 3 月).
- 复合存储:内存,工作流程,可观测到不同的后台;ClickHouse建议以实现规模观测.
-  Apache 2.0 版本`ee/`源可用企业许可证下载的目录.
- 服务器适配器用于Express,Hono,Fastify,Koa;第一级Next.js和Astro集成.
- 导航Mastra Studio (本地主机:4111) 进行调试.
- 据悉,GitHub的数据量超过22万,每周每小时下载量超过300万,

### 定位

他们都不想成为兰格拉夫.

> 两者都不是试图成为兰格拉夫.

> 亚格诺和马斯特拉是两种轻量级的代理 运行时时.亚格诺专注于快速构建,马斯特拉专注于TypeScript 生产部署.

- **Language fit.**首先为Python团队提供AgnO,而TypeScript则为Mastra.
- **Runtime ergonomics.**亚格诺=近零的通用费用;马斯特拉=与Vercel生态系统集成.
- **Observability.**两者都与Langfuse/Phoenix/Opik (课 24) 结合起来,但Mastra Studio是第一方.

### 选出每一个

- **Agno**Python后端,许多短暂的代理,强大的性能要求,FastAPI商店.
- **Mastra** 类型脚本后台,下一个.js / Vercel部署,统一的多提供商模型路由,Zod类型工具.
- **LangGraph**长期状态和明确的图形推理比原始速度更重要.
- **OpenAI / Claude Agent SDK**当你想要提供商的生产形状时 (课程1617).

### 在这个模式出现错误的地方

> ️ **【易错点】**看到Agno "2μs 实例化"就没有脑子选Agno。**后果**实例化对总耗时的影响是0.0000003% 错误的框架也失去了朗格拉夫的持久性能力.**一行修复**首先测量您的工作负载的"代理 实例化次数 × 单次实例化开销与总耗时",占比 > 30% 才值得选择性能,否则继续使用LangGraph──

- **Perf-for-perf's-sake.**选择Agno因为2μs听起来很好,当工作负载是每次要求一个缓慢的代理调用.
- **Ecosystem lock-in.**马斯特拉的Vercel味道整合是Vercel的加倍,其他地方是负的.
- **Enterprise license confusion.**马斯特拉的`ee/`如果您打算叉,请阅读许可证.

>  **【困惑】**问: 我团队是Python后端,又想要Mastra的"多模型路由"功能,能用Agno 实现吗?A:能,但要自己写.Agno 也有23个模型提供商,但Mastra的3300+模型 94提供商是基于Vercel AI SDK的庞大的生态.如果"模型路由"是核心诉求和团队接受TypeScript,Mastra是更省省的选择;如果坚持Python,Agno +自我封装一层模型路由器也行,工作量约2-3天.

> **为性能而性能。**因为"2μs"听起来不错就选择Agno,而工作负载是每个请求一个慢速代理调用.
> **生态系统锁定。**马斯特拉的Vercel风格集成在Vercel上是优势,在其他地方是劣势.
> **企业许可困惑。**马斯特拉的`ee/`如果您打算叉,请先阅读许可证.

## 建立它,实现它.
```figure
wb-runtime-spawn
```

## 建立它

没有单个代码文物可以对这两个框架进行正义.`code/main.py`对于一款横边玩具:至少执行两次 (一次Agnō形,一次Mastra形) 的"运行代理,输出流,持续会议"流程.

> 这一课主要是比较性,没有一个代码产品可以同时体现两个框架的特点.`code/main.py`中的并排演示:一个最小的"运行代理"",流式输出"",持久化会话"流程实现了两次 (一次Agnō形态,一次Mastra形态) .

> 亚格诺和马斯特拉是两种轻量级的代理 运行时时.亚格诺专注于快速构建,马斯特拉专注于TypeScript 生产部署.

运行它:

```
python3 code/main.py
```

两种结构不同但功能相等的痕迹.

> 两种结构不同,但功能均等的追踪.

> 亚格诺和马斯特拉是两种轻量级的代理 运行时时.亚格诺专注于快速构建,马斯特拉专注于TypeScript 生产部署.

## 用它实现框架

- **Agno** Python后端需要速度和FastAPI形状.
- **Mastra** 类型Script后台与许多提供商和工作流原始.
- 两艘船都能使用第一方可观测,

## 运送它.

`outputs/skill-runtime-picker.md`根据堆,延迟预算和运营形状,选择Agno,Mastra,LangGraph或提供商SDK.

> `outputs/skill-runtime-picker.md`根据技术、延迟预算和运营形态选择Agno、Mastra、LangGraph或供应商SDK──

> 亚格诺和马斯特拉是两种轻量级的代理 运行时时.亚格诺专注于快速构建,马斯特拉专注于TypeScript 生产部署.

## 练习题

1. 读出阿格诺的文件,将Sdlib ReAct循环 (课1) 转移到阿格诺.
  中文翻译:思考并实践此练习──
2. 阅读Mastra的文件.将相同的循环移植到Mastra.工具打字 (Zod vs.什么都没有) 发生了什么变化?
  中文翻译:思考并实践此练习──
3. 测量代理实时延迟. 亚格诺的2μs对你的工作负载有什么关系?
  中文翻译:思考并实践此练习──
4. 如果您在Python中运行CrewAI,如果您搬到Agno,会有什么问题?
  中文翻译:思考并实践此练习──
5. 阅读马斯特拉的书`ee/`什么限制会影响一个开源叉子?
  中文翻译:思考并实践此练习──

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agno | "Fast Python agents" | Stateless session-scoped agent runtime |  |
| Mastra | "TypeScript agents on Vercel AI SDK" | Agents + Tools + Workflows + Model Router |  |
| Unified Model Router | "Multi-provider access" | Single client for 3,300+ models across 94 providers |  |
| Composite storage | "Multiple backends" | Memory/workflows/observability each to a different store |  |
| Mastra Studio | "Local debugger" | localhost:4111 UI for introspecting agents |  |
| Source-available | "Not OSS" | License permits source reading but restricts commercial use |  |

## 继续阅读 继续阅读

- [Agno Agent Framework docs](https://www.agno.com/agent-framework)绩效目标,FastAPI集成
  中文翻译:见原文.
- [Mastra docs](https://mastra.ai/docs)原始设备,服务器适配器,路由器模型
  中文翻译:见原文.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)国家图的替代方案
  中文翻译:见原文.
- [Comet Opik](https://www.comet.com/site/products/opik/)Mastra集成所引用的可观性比较
  中文翻译:见原文.
