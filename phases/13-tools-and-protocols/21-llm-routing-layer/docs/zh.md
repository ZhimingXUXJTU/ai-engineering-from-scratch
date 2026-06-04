# LLM 路由层 — LiteLLM、OpenRouter 与 Portkey

> 供应商锁定成本高昂。不同的工具调用工作负载适合不同的模型。路由网关提供统一的 API 接口、重试、故障转移、成本追踪和护栏。2026 年三大方案：LiteLLM（开源自托管）、OpenRouter（托管 SaaS）、Portkey（生产级，2026年3月开源）。本课命名决策标准并演示标准库路由网关。

> **【中文解读】** 供应商锁定成本高昂。不同的工具调用工作负载适合不同的模型。路由网关提供统一的 API 接口、重试、故障转移、成本追踪和护栏。2026 年三大方案：LiteLLM（开源自托管）、OpenRouter（托管 SaaS）、Portkey（生产级，2026年3月开源）。

> **【拓展】** LLM 路由层解决的核心问题：按任务复杂度自动路由到最优模型（成本优化）、供应商故障自动切换（高可用）、延迟敏感路由（用户体验）、合规区域路由（数据主权）、A/B 测试路由（实验）。这是 AI 工程从单模型走向多模型架构的关键基础设施。

**类型：** 学习
**语言：** Python（标准库，路由 + 故障转移 + 成本追踪器）
**前置条件：** Phase 13 · 02（函数调用），Phase 13 · 17（网关）
**时间：** 约 45 分钟

## 学习目标

- 区分自托管、托管和生产级路由选项。
- 实现供应商故障时的回退链。
- 跨供应商追踪每请求成本和 token 使用量。
- 根据生产约束选择 LiteLLM/OpenRouter/Portkey。

## 问题引入

路由重要的场景：

1. **成本。** Claude Sonnet 费用是 Haiku 的 3 倍。对于分流任务，Haiku 足够；对于综合任务，Sonnet 值得。按请求路由。
2. **故障转移。** OpenAI 有一个不好的小时。每个请求失败。你想要无需重部署即可自动回退到 Anthropic。
3. **延迟。** 实时聊天 UI 需要快速首 token 时间。批量摘要器不需要。按延迟 SLA 路由。
4. **合规。** EU 用户必须留在 EU 区域。按区域路由。
5. **实验。** 在同一工作负载上 A/B 两个模型。按测试桶路由。

手工编码所有这些每个集成是重复的。路由网关提供一个 OpenAI 兼容 API 并处理其余。

## 核心概念

### OpenAI 兼容代理形状

每个人都说 OpenAI 形状。路由网关暴露 `/v1/chat/completions`，接受 OpenAI Schema，内部代理到 Anthropic / Gemini / Cohere / Ollama / 任何东西。客户端不关心。

### 模型别名

你的代码不说 `claude-3-5-sonnet-20251022`，而说 `our_smart_model`。网关将别名映射到真实模型。当 Anthropic 发布 Claude 4 时，你在服务端更改别名；你的代码不动。

### 回退链

```
primary: openai/gpt-4o
on 5xx: anthropic/claude-3-5-sonnet
on 5xx: google/gemini-1.5-pro
on 5xx: refuse
```

网关在配置中定义这个。重试计入预算，防止回退级联爆炸成本。

### 语义缓存

相同或近似相同的提示命中缓存而非供应商。重复 Agent 循环的节省可达 30% 到 60%。键基于嵌入；近似相同的提示共享缓存槽。

### 护栏

网关级：

- **PII 脱敏。** 发送提示前的正则或 ML 驱动的脱敏。
- **策略违规。** 拒绝包含禁止内容的提示。
- **输出过滤器。** 擦除补全中的泄漏。

Portkey 和 Kong 都提供开箱即用的护栏。LiteLLM 将它们设为可选。

### 每密钥限流

一个 API key = 一个团队。每密钥预算防止一个团队消耗共享配额。大多数网关支持此功能。

### 自托管 vs 托管的权衡

| 因素 | LiteLLM（自托管） | OpenRouter（托管） | Portkey（生产） |
|------|-------------------|-------------------|-----------------|
| 代码 | 开源，Python | 托管 SaaS | 开源（2026年3月）+ 托管 |
| 设置 | 部署代理 | 注册 | 两者 |
| 供应商 | 100+ | 300+ | 100+ |
| 计费 | 你自己的 key | OpenRouter 积分 | 你自己的 key |
| 可观测性 | OpenTelemetry | 仪表盘 | 完整 OTel + PII 脱敏 |
| 最适合 | 想要完全控制的团队 | 快速原型开发 | 需要合规的生产 |

有 SRE 团队且想要数据主权时选 LiteLLM。想要单一订阅且无基础设施时选 OpenRouter。需要开箱即用的护栏和合规时选 Portkey。

### 成本追踪

每个请求携带 `provider`、`model`、`input_tokens`、`output_tokens`。乘以每模型每 token 价格（从网关维护的价格表拉取）。按用户/团队/项目聚合。

### MCP 加路由

网关可以同时路由 LLM 调用和 MCP 采样请求。当采样请求的 modelPreferences 偏好特定模型时，网关翻译到正确的后端。这是 Phase 13 · 17（MCP 网关）和本课路由网关有时合并为同一服务的地方。

### 路由策略

- **静态优先级。** 列表第一个；错误时回退。
- **负载均衡。** 轮询或加权。
- **成本感知。** 选择满足延迟/质量的最便宜模型。
- **延迟感知。** 选择最近 N 分钟内最快的模型。
- **任务感知。** 提示分类器路由编码到一个模型，摘要到另一个。

## 用框架实现

`code/main.py` 实现约 150 行的路由网关：接受 OpenAI 格式请求，翻译到每供应商存根，运行优先级回退链，追踪每请求成本，并应用 PII 脱敏。三个场景：正常请求、主供应商宕机触发故障转移、PII 泄露被脱敏拦截。

关注点：

- `ROUTES` 字典：别名 -> 优先级排序的具体供应商列表。
- 回退循环在 5xx 时重试。
- 成本追踪器用 token 使用量乘以每模型费率。
- PII 脱敏器在转发前擦除 SSN 形状的模式。

## 产出物

本课产生 `outputs/skill-routing-config-designer.md`。给定工作负载配置（延迟、成本、合规），该技能选择 LiteLLM/OpenRouter/Portkey 并生成路由配置。

## 练习题

1. 运行 `code/main.py`。触发宕机场景；确认回退落在第二个供应商上且成本正确归属。

2. 添加语义缓存：提示的 SHA256 是查找键；缓存命中立即返回。测量重复调用的成本节省。

3. 添加提示分类器，将"code ..."提示路由到偏好智能的别名，将"summarize ..."提示路由到偏好速度的别名。

4. 设计每团队预算：每个团队有月度支出上限；达到上限后网关拒绝请求。选择执行粒度（每请求或窗口化）。

5. 并排阅读 LiteLLM、OpenRouter 和 Portkey 文档。说出每个提供的另外两个没有的一个功能。

## 术语速查表

| 术语 | 人们怎么说 | 实际含义 | 英文 |
|------|-----------|---------|------|
| 路由网关 | "LLM 代理" | 多供应商前面的统一 API 层 | Routing gateway |
| OpenAI 兼容接口 | "说 OpenAI Schema" | 接受 `/v1/chat/completions` 形状，翻译到任何后端 | OpenAI-compatible |
| 模型别名 | "our_smart_model" | 代码中网关映射到具体模型的名称 | Model alias |
| 回退链 | "重试列表" | 失败时按序尝试的供应商列表 | Fallback chain |
| 语义缓存 | "提示嵌入缓存" | 键是提示的嵌入；近似重复共享缓存命中 | Semantic caching |
| 护栏 | "输入输出过滤器" | 脱敏 PII、拒绝策略违规 | Guardrails |
| 按密钥限流 | "团队预算" | 范围限定到 API key 的配额 | Per-key rate limit |
| 成本追踪 | "每请求费用" | 聚合 token 使用量 x 每模型价格 | Cost tracking |
| LiteLLM | "开源代理" | 可自托管的 OSS 路由网关 | LiteLLM |
| OpenRouter | "托管 SaaS" | 基于积分的托管路由网关 | OpenRouter |
| Portkey | "生产选项" | 内置护栏的开源+托管 | Portkey |

## 延伸阅读

- [LiteLLM — docs](https://docs.litellm.ai/) — 自托管路由网关
- [OpenRouter — quickstart](https://openrouter.ai/docs/quickstart) — 托管路由 SaaS
- [Portkey — docs](https://portkey.ai/docs) — 带护栏的生产路由
- [TrueFoundry — LiteLLM vs OpenRouter](https://www.truefoundry.com/blog/litellm-vs-openrouter) — 决策指南
- [Relayplane — LLM gateway comparison 2026](https://relayplane.com/blog/llm-gateway-comparison-2026) — 供应商调查
