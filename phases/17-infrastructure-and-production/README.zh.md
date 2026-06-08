# Phase 17: 基础设施与生产

> **28 节课 · ~32 小时 · 🔴高级**

将 AI 交付到真实世界。扩展、监控、优化。

## 学习目标

- 掌握 LLM 推理服务核心技术：vLLM、SGLang、TensorRT-LLM、投机解码
- 理解推理平台经济学：托管平台选型、成本结构、GPU 自动扩展
- 学会推理优化：量化（AWQ/GPTQ/GGUF/FP8）、KV 缓存、分离式预填充/解码
- 构建可观测性体系：OpenTelemetry、LLM 监控、语义缓存、AI 网关
- 掌握生产部署最佳实践：灰度发布、A/B 测试、负载测试、混沌工程
- 理解 FinOps、合规框架（SOC 2/HIPAA/GDPR/EU AI Act）与安全审计

## 前置知识

- 完成阶段 01-16，理解 LLM 原理和 Agent 架构
- 基本的 DevOps 知识（Docker、Kubernetes、CI/CD）
- 了解网络基础（延迟、吞吐量、负载均衡）

## 课程清单

| # | 课程 | 类型 | 预计时间 |
|---|------|------|---------|
| 01 | 托管式 LLM 平台（Bedrock、Azure OpenAI、Vertex AI） | 学习 | ~60min |
| 02 | 推理平台经济学（Fireworks、Together、Baseten、Modal） | 学习 | ~60min |
| 03 | Kubernetes GPU 自动扩展（Karpenter、KAI 调度器） | 学习 | ~75min |
| 04 | vLLM 服务内幕（PagedAttention、连续批处理、分块预填充） | 学习 | ~75min |
| 05 | EAGLE-3 投机解码生产实践 | 学习 | ~60min |
| 06 | SGLang 与 RadixAttention 前缀密集负载 | 学习 | ~60min |
| 07 | TensorRT-LLM 与 Blackwell FP8/NVFP4 | 学习 | ~75min |
| 08 | 推理指标 — TTFT、TPOT、ITL、Goodput、P99 | 学习 | ~60min |
| 09 | 生产量化 — AWQ、GPTQ、GGUF、FP8、NVFP4 | 学习 | ~75min |
| 10 | Serverless LLM 冷启动缓解 | 学习 | ~60min |
| 11 | 多区域 LLM 服务与 KV 缓存局部性 | 学习 | ~60min |
| 12 | 边缘推理 — ANE、Hexagon、WebGPU、Jetson | 学习 | ~60min |
| 13 | LLM 可观测性技术栈选型 | 学习 | ~60min |
| 14 | 提示缓存与语义缓存经济学 | 学习 | ~60min |
| 15 | Batch API — 50% 折扣的行业实践 | 学习 | ~45min |
| 16 | 模型路由作为降本原语 | 学习 | ~60min |
| 17 | 分离式预填充/解码 — NVIDIA Dynamo 与 llm-d | 学习 | ~75min |
| 18 | vLLM 生产栈与 LMCache KV 卸载 | 学习 | ~60min |
| 19 | AI 网关 — LiteLLM、Portkey、Kong、Bifrost | 学习 | ~60min |
| 20 | 影子测试、金丝雀发布与渐进式部署 | 学习 | ~60min |
| 21 | LLM 特性 A/B 测试（GrowthBook、Statsig） | 学习 | ~60min |
| 22 | LLM API 负载测试（k6、LLMPerf、GenAI-Perf） | 动手 | ~75min |
| 23 | AI SRE — 多 Agent 事件响应 | 学习 | ~60min |
| 24 | LLM 生产混沌工程 | 学习 | ~60min |
| 25 | 安全 — 密钥、PII 清洗、审计日志 | 学习 | ~60min |
| 26 | 合规 — SOC 2、HIPAA、GDPR、EU AI Act、ISO 42001 | 学习 | ~60min |
| 27 | LLM FinOps — 单元经济与多租户归因 | 学习 | ~60min |
| 28 | 自托管服务选型 — llama.cpp、Ollama、TGI、vLLM、SGLang | 学习 | ~45min |

## 常见困惑

- **vLLM 和 SGLang 该选哪个？** → 课 04 和 06 分别深入两者内幕。vLLM 生态更成熟，SGLang 在前缀密集场景有优势。课 28 提供选型决策框架。
- **量化会损失多少质量？** → 课 09 系统比较了 AWQ/GPTQ/GGUF/FP8 等方案的精度-速度-内存权衡，附带实际基准数据。
- **FinOps 对 AI 工程师为什么重要？** → LLM 推理成本可以轻松占云账单的 50%+。课 27 教你建立 Token 级成本追踪和多租户归因模型。
- **EU AI Act 对我有什么影响？** → 课 26 详细解读了 EU AI Act（2026年8月执行高风险条款）和全球主要合规框架，包括罚款金额和适用范围。

## 开始学习

→ [第一课：托管式 LLM 平台](01-managed-llm-platforms/docs/en.md)
