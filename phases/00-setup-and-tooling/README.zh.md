# Phase 0: 环境搭建与工具

> **12 节课 · ~14 小时 · 🟢入门**

## 在本阶段开始（GitHub）| Start this phase on GitHub

**前置条件：**无。开始只需要 Git 和 Python 3.11 或更高版本。其他工具只在你的路线（route）需要时才安装。

**第一课：**[开发环境搭建](01-dev-environment/)

在仓库根目录运行可识别路线的预检（preflight）：

```bash
python3 phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route beginner
```

保留命令、仓库根目录的工作目录、退出码、必需检查项的结果，以及打印出的 `Next:` 命令。可选检查未通过不算失败。

**下一步：**修复所有必需项的失败，重新运行直到命令以退出码 0 结束，然后继续学习 [Git 与协作](02-git-and-collaboration/)。

浏览[完整的 Phase 0 课程列表](../../README.md#phase-0)或[跨阶段路线图](../../ROADMAP.md)。

## 学习目标

- 搭建完整的 AI 开发环境，掌握日常开发工具链
- 学会使用 Git 进行版本控制与团队协作
- 理解 GPU 加速原理，能使用云平台进行模型训练
- 掌握 Python 环境管理、Docker 容器化和数据管理流程

## 前置知识

- 基本的计算机操作能力
- 无需任何 AI 或编程经验

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | 开发环境搭建 | Build | Python | ~60min |
| 02 | Git 与协作 | Learn | - | ~60min |
| 03 | GPU 配置与云平台 | Build | Python | ~75min |
| 04 | API 与密钥管理 | Build | Python | ~60min |
| 05 | Jupyter 笔记本 | Build | Python | ~60min |
| 06 | Python 环境管理 | Build | Shell | ~75min |
| 07 | Docker 容器化 | Build | Docker | ~75min |
| 08 | 编辑器配置 | Build | - | ~60min |
| 09 | 数据管理 | Build | Python | ~75min |
| 10 | 终端与 Shell | Learn | - | ~60min |
| 11 | Linux 基础 | Learn | - | ~75min |
| 12 | 调试与性能分析 | Build | Python | ~75min |

## 常见困惑

- **"为什么要先学这些工具？"** → 工欲善其事，必先利其器。后续所有阶段都依赖这些环境配置，提前掌握能避免大量重复踩坑。
- **"GPU 环境配不好怎么办？"** → 第三课详细讲解了本地 GPU 和云平台两种方案，推荐初学者先用云平台（如 Google Colab）快速上手。
- **"Docker 不熟影响后续学习吗？"** → 影响不大。Docker 主要用于部署和生产环境，学习阶段可以先跳过，需要时再回来复习。

## 开始学习

→ [第一课：开发环境搭建](01-dev-environment/docs/zh.md)
