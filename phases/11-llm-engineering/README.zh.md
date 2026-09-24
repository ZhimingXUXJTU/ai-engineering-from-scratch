# Phase 11: LLM 工程化

> **17 节课 · ~17 小时 · 🟡进阶**

## 在本阶段开始（GitHub）| Start this phase on GitHub

**前置条件：**Phase 10 第 01 至 05 课，或具备分词、数据流水线、预训练和扩展方面的同等知识。

**第一课：**[提示工程](01-prompt-engineering/)

在仓库根目录运行以下命令：

```bash
python3 phases/11-llm-engineering/01-prompt-engineering/code/prompt_engineering.py
```

保留命令、退出码、生成的提示元数据、测试结果，以及一处提示修改和它造成的输出差异。该演示使用模拟的模型响应，无需 API 密钥。

**下一步：**解释哪个提示变量改变了行为以及原因，然后继续学习 [少样本、思维链与思维树](02-few-shot-cot/)。

浏览[完整的 Phase 11 课程列表](../../README.md#phase-11)或[跨阶段路线图](../../ROADMAP.md)。

## 学习目标

- 掌握提示工程（Prompt Engineering）的核心技术与模式
- 理解检索增强生成（RAG）的原理和高级优化策略
- 学习 LoRA/QLoRA 微调技术，低成本适配大模型
- 掌握 Function Calling、MCP 协议等工具使用方法
- 构建可落地的生产级 LLM 应用

## 前置知识

- Transformer 基础（Phase 7：注意力机制、编码器-解码器）
- NLP 基础（Phase 5：文本处理、嵌入，推荐）
- Python 工程基础（API 开发、异步编程）

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | 提示工程 — 技术与模式 | Build | Python | ~45min |
| 02 | 少样本、思维链 (CoT)、思维树 (ToT) | Build | Python | ~45min |
| 03 | 结构化输出 | Build | Python | ~75min |
| 04 | 嵌入与向量表示 | Build | Python | ~75min |
| 05 | 上下文工程 | Build | Python | ~75min |
| 06 | 检索增强生成 (RAG) | Build | Python | ~75min |
| 07 | 高级 RAG | Build | Python | ~75min |
| 08 | LoRA 与 QLoRA 微调 | Build | Python | ~75min |
| 09 | 函数调用与工具使用 | Build | Python | ~75min |
| 10 | 评估与测试 LLM 应用 | Build | Python | ~45min |
| 11 | 缓存、限流与成本优化 | Build | Python | ~45min |
| 12 | 安全护栏与内容过滤 | Build | Python | ~45min |
| 13 | 构建生产级 LLM 应用 | Build | Python | ~120min |
| 14 | 模型上下文协议 (MCP) | Build | Python | ~75min |
| 15 | 提示缓存与上下文缓存 | Build | Python | ~60min |
| 16 | LangGraph 状态机 | Build | Python | ~75min |
| 17 | Agent 框架权衡 | Learn | Python | ~60min |

## 常见困惑

- **"RAG 和微调该怎么选？"** → RAG 适合需要外部知识的场景（文档问答），微调适合改变模型行为风格的场景。很多生产系统两者结合使用。
- **"MCP 协议是什么？"** → Model Context Protocol 是 Anthropic 提出的标准化协议，让 LLM 能通过统一接口调用外部工具和数据源。第 14 课会深入讲解。
- **"做 LLM 应用需要自己训练模型吗？"** → 大部分场景不需要。通过提示工程、RAG、Function Calling 等技术，基于 API 即可构建强大的应用。

## 开始学习

→ [第一课：提示工程 — 技术与模式](01-prompt-engineering/docs/zh.md)
