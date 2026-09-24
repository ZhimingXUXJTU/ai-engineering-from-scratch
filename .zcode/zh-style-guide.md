# 中文翻译与批注风格指南（fork 维护用）

本 fork 的双语体系有三层，全部是**增量式**的——英文原文一字不改、一行不删，中文只做添加。

## 1. en.md 内嵌批注（所有课程）

以 `phases/13-tools-and-protocols/06-mcp-fundamentals/docs/en.md`（合并前版本，`git show b06de5f9:<path>` 可取）为完整范例。规则：

```markdown
# English Title | 中文标题（保留英文，加竖线+中文）

> English hook paragraph 保持原样，必须是全文第一个 blockquote（site/build.js 依赖它生成摘要）。

> **【中文解读】** 用 3-5 句中文概括本节主旨：这是什么、为什么重要、解决什么问题。

> **【拓展：主题→具体应用】** （可选，约 3 句）把本节放进更大的图景：生态位、真实产品、历史脉络或与后续课程的联系。

> 🔗 **【前置】** （可选）学本节前请先掌握：列出前置课程编号和知识点，说明本节在系列中的位置。

> 💡 **【类比】** （可选）用一个生活化类比解释核心概念，格式如 "X 像 Y 标准。之前…之后…"。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 01 | **前置知识:** Phase 13 · 01
**Time:** ~45 minutes | **时间:** 约 45 分钟

## Learning Objectives | 学习目标

- Name all six MCP primitives and give one use case each.
  中文翻译：说出全部六个 MCP 原语并为每个给出一个用例。
  （学习目标每条英文下面缩进加一行"中文翻译：…"）

## The Problem | 问题引入

English paragraph stays untouched.

> 英文段落的中文翻译，以 blockquote 形式紧跟其后。每个 section 的前 1-3 个重要段落做全文翻译；次要段落可跳过或并入【中文解读】。

## Core Concepts | 核心概念
（每个二级标题都加" | 中文名"；常见对照：The Problem=问题引入、Core Concepts=核心概念、
Learning Objectives=学习目标、Implementation=动手实现、Common Pitfalls=常见陷阱、
Verification=验证、Key Takeaways=要点总结、Further Reading=延伸阅读、Exercises=练习）
```

要点：
- 代码块、表格、链接、英文原文**一个字符都不改**。表格通常不加中文（zh.md 里才翻译表格）。
- 【中文解读】每个大 section 至少一个；整课 5-10 个为宜，宁精勿滥。
- 类比要贴合中国读者的知识背景（如 USB-C、高铁、外卖平台）。
- 术语约定：Agent/LLM/MCP/tools/resources/prompts 等协议词保留英文；"primitives=原语、tool call=工具调用、lifecycle=生命周期、capability negotiation=能力协商、wire format=线格式、sampling=采样、elicitation=诱导输入（可保留英文）、registry=注册中心、gateway=网关、sandbox=沙箱"。

## 2. zh.md 完整翻译（有翻译传统的阶段）

以 `phases/00-setup-and-tooling/01-dev-environment/docs/zh.md` 和 `git show b06de5f9:phases/13-tools-and-protocols/06-mcp-fundamentals/docs/zh.md` 为范例。规则：

- 全文中文重写（不是逐行对照），结构、标题层级、代码块、表格列数与 en.md 一一对应。
- 首行 `# 中文标题`；hook 段落翻译为中文；随后放【中文解读】【拓展】【前置】块（与 en.md 中的相同主题，可复用文字）。
- frontmatter 全中文：`**类型：** 动手实践` / `**语言：** Python（标准库）` / `**前置条件：** …` / `**预计用时：** 约 45 分钟`。
- 每个大 section 后加一个 `> **【中文解读】**` 块，给读者"这一节到底在说什么"的中文导读。
- 代码块原样保留（注释可译）；表格整体翻译（表头和说明文字译成中文，术语/代码列保留）。
- 文末若有 Further Reading，译为 `## 延伸阅读`，链接保留，每个链接后加一句中文说明。
- 结尾术语表（如有）译为 `## 术语表`，格式 `| 英文 | 中文 | 说明 |`。

## 3. 代码文件中文注释（fork 有先例的文件）

以 `git show b06de5f9:phases/19-capstone-projects/13-mcp-server-with-registry/code/main.py` 为范例：

- 文件头 docstring 前部加中文块：课程标题中英对照 + `核心概念：…`（2-4 行）+ `AI 应用对应：…`（2-3 行）。
- 关键 section 分隔注释可译为中文（如 `# OTel GenAI span 发射器`）。
- 只加注释，不改任何逻辑、不删原有英文注释。Python 用 `#` 或 docstring；不能破坏运行。

## 4. 硬性约束

- 英文内容零删改（en.md 的英文部分与上游逐字节一致，只有中文是新增的）。
- en.md 第一个 blockquote 必须保持为英文原 hook（构建脚本从它提取描述）。
- 章节编号、相对链接、锚点不动。
- 完成后自查：`grep -c "【中文解读】" <en.md>` 应 ≥5；zh.md 行数应与 en.md 相近（±25%）。

## 5. 本次补译任务的特殊约定（2026-09-24 追加）

### P19 毕业项目课（58-87）
- 中文标题**必须**用 `phases/19-capstone-projects/README.zh.md` 表中已定的名称（保持一致）。
- 代码块里的训练/分布式/安全术语按指南；checkpoint=检查点、sharding=分片、pipeline parallel=流水线并行、bubble=气泡、jailbreak=越狱、refusal=拒答、constitutional=宪法式。

### certifications/claude 认证课（00-32）
- 中文标题**必须**用 `certifications/claude/README.zh.md` 索引表中已定的名称。
- 常见小节中英对照：Learning Objectives=学习目标、The Problem=问题引入、The Concept=核心概念、
  Build It=动手构建、Interactive Lab=交互实验室、Practice Lab=练习实验室、Shipped Artifact=交付产物、
  Verify It=验证、Capstone Connection=毕业设计衔接、Use It=运行验证、Exam Decision Patterns=考试决策模式、
  Common Traps=常见陷阱、Exercises=练习、Key Terms=关键术语、Further Reading=延伸阅读。
- 认证课引用的官方事实（价格、题数、域名权重）**原样保留数字**，翻译不得改写事实性内容。
- 每课仍需 5-8 个【中文解读】；第一个 blockquote 保持英文原 hook。
