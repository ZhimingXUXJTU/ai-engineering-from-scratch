# 函数调用与工具使用

> Toolformer (Schick 等人, 2023) 开创了自监督工具标注。Berkeley Function Calling Leaderboard V4 (Patil 等人, 2025) 设定了 2026 年的标准：40% agentic、30% multi-turn、10% live、10% non-live、10% hallucination。单轮调用已接近解决。记忆、动态决策和长链工具编排仍是开放问题。

**类型：** 构建
**语言：** Python (标准库)
**前置条件：** Phase 14 · 01 (Agent 循环), Phase 13 · 01 (函数调用深入)
**预计时间：** ~60 分钟

## 学习目标

- 解释 Toolformer 的自监督训练信号：仅当执行减少下一个 token 损失时保留工具标注。
- 说出 BFCL V4 的五个评估类别及各自衡量什么。
- 用标准库实现带 schema 验证、参数强制转换和执行沙箱的工具注册表。
- 诊断三个 2026 年开放问题：长链工具编排、动态决策和记忆。

## 问题引入

早期工具使用的问题是：模型能否预测正确的函数调用？现代工具使用的问题是：模型能否在 40 步内链式调用工具、拥有记忆、处理部分可观察性、从工具失败中恢复、且不幻觉出不存在的工具？单轮函数调用已接近解决，但记忆、动态决策和长链工具编排仍是 2026 年的开放问题。

> **【拓展：BFCL V4 评估体系的演进】** Berkeley Function Calling Leaderboard V4 是 2026 年事实上的评估标准。V3 引入了基于状态的评估（检查 API 实际状态而非匹配 AST），V4 添加了 Web 搜索、记忆和格式敏感性类别。关键发现：单轮函数调用已接近解决，失败集中在记忆、动态决策和长链漂移。

## 核心概念

### Toolformer (Schick 等人, NeurIPS 2023)

核心思想：让模型用自己的预训练语料标注候选 API 调用。对每个候选，执行它。只有当包含工具结果能减少下一个 token 的损失时才保留标注。然后在过滤后的语料上微调。

规模效应：工具使用在大模型上涌现，小模型反而被工具标注损害。这也是 2026 年前沿模型有强大工具使用能力而大多数 7B 模型需要显式工具使用微调的原因。

### Berkeley Function Calling Leaderboard V4 (Patil 等人, ICML 2025)

BFCL 是 2026 年事实上的评估。V4 组成：

- **Agentic (40%)**——完整 Agent 轨迹：记忆、多轮、动态决策。
- **Multi-Turn (30%)**——带工具链的交互式对话。
- **Live (10%)**——用户提交的真实提示（更难的分布）。
- **Non-Live (10%)**——合成测试用例。
- **Hallucination (10%)**——检测何时不该调用工具。

### 工具 Schema

每个提供商都有自己的 schema，细节不同但形状相同：

```
name: string
description: string (做什么，何时使用)
input_schema: JSON Schema (属性、必需、类型、枚举)
```

描述是承重的——模型阅读它们来选择正确的工具。糟糕的工具描述是选错工具失败的首要根因。

### 参数验证

不信任任何工具调用。验证：

1. **类型强制转换。** 模型可能返回字符串 "5" 而 schema 说是 int。无歧义时强制转换；有歧义时拒绝。
2. **枚举验证。** 如果 schema 说 `status in {"open", "closed"}` 而模型输出 `"in_progress"`，用描述性错误拒绝。
3. **必需字段。** 缺少必需字段 → 立即返回错误观察给模型，而不是崩溃。
4. **格式验证。** 日期、邮箱、URL——用具体解析器验证，而非正则。

### 并行工具调用

现代提供商支持一次助手轮中的并行工具调用。工程规则：将关联 ID 视为承重的。交换它们会导致错误工具到错误结果的路由。

### 沙箱

工具执行是沙箱边界。每个工具应指定读/写范围、网络访问、超时、内存上限。通用的 `run_shell(cmd)` 是红旗；特定的 `git_status()` 更安全。

## 动手实现

`code/main.py` 实现了生产形态的工具注册表：

- JSON Schema 子集验证器（仅标准库）。
- 工具注册，含描述、输入 schema、超时和执行器。
- 参数强制转换和枚举验证。
- 带关联 ID 的并行工具分派。
- 结构化字符串形式的错误观察。

运行：

```
python3 code/main.py
```

## 用框架实现

每个提供商都有自己的工具 schema——Anthropic、OpenAI、Gemini、Bedrock。如果需要多提供商，使用转换层（OpenAI Agents SDK、Vercel AI SDK、LangChain 工具适配器）。BFCL 是参考基准——如果工具使用是你产品的核心，在发布前针对你的 Agent 运行它。

## 产出物

`outputs/skill-tool-registry.md` 为给定任务领域生成工具目录、schema 和注册表。包含描述质量检查（每个工具的描述是否告诉模型何时使用它？）。

## 练习题

1. 添加"无操作"工具，让模型显式拒绝使用任何其他工具。在类似 BFCL 的幻觉测试上测量。
2. 实现 int-as-string 和 float-as-string 的参数强制转换。强制转换从哪里开始隐藏真正的 bug？
3. 为每个工具添加超时和熔断器（3 次连续失败后拒绝该工具 60 秒）。这如何改变模型的恢复方式？
4. 阅读 BFCL V4 描述。选择一个类别（如"multi-turn"），通过你的 Agent 运行 10 个示例提示。报告通过率。
5. 将标准库验证器移植到 Pydantic 或 Zod。Pydantic/Zod 捕获了什么玩具遗漏的？

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Function calling（函数调用） | 带 schema 验证的结构化输出工具调用 |
| Toolformer | Schick 2023——保留减少下一 token 损失的工具调用 |
| BFCL | 2026 年基准：40% agentic, 30% multi-turn, 10% live, 10% non-live, 10% hallucination |
| Tool schema（工具 schema） | 名称、描述、参数的 JSON Schema |
| tool_use_id | 将工具调用与其结果关联；并行分派的必需品 |
| Hallucination detection（幻觉检测） | V4 类别：当没有工具适合时拒绝调用 |
| Argument coercion（参数强制转换） | 可预测 schema 不匹配的窄修复；有歧义时拒绝 |
| Sandboxing（沙箱） | 每个工具的读/写范围、网络、超时、内存上限 |

## 延伸阅读

- [Schick et al., Toolformer (arXiv:2302.04761)](https://arxiv.org/abs/2302.04761)
- [Berkeley Function Calling Leaderboard (V4)](https://gorilla.cs.berkeley.edu/leaderboard.html)
- [Anthropic, Tool use documentation](https://platform.claude.com/docs/en/agent-sdk/overview)
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/)
