# Phase 2: 机器学习基础

> **18 节课 · ~21 小时 · 🟢入门**

## 在本阶段开始（GitHub）| Start this phase on GitHub

**前置条件：**Phase 1 数学基础和 NumPy。用以下命令检查路线：`python3 phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route ml-foundations`。

**第一课：**[什么是机器学习](01-what-is-machine-learning/)

在仓库根目录运行以下命令：

```bash
python3 phases/02-ml-fundamentals/01-what-is-machine-learning/code/ml_intro.py
```

保留命令、退出码、测试准确率、随机基线，以及一句话解释为什么学到的分类器优于该基线。

**下一步：**调整类别间隔，预测准确率会怎么变化，再次运行，然后继续学习 [线性回归从零实现](02-linear-regression/)。

浏览[完整的 Phase 2 课程列表](../../README.md#phase-2)或[跨阶段路线图](../../ROADMAP.md)。

## 学习目标

- 理解机器学习的核心范式：监督学习、无监督学习
- 从零实现经典算法（线性回归、逻辑回归、决策树、SVM 等）
- 掌握模型评估、特征工程、超参数调优等工程实践
- 建立偏差-方差、集成方法等核心概念的直觉

## 前置知识

- Python 编程基础（Phase 0）
- 基础数学知识（Phase 1 的线性代数、概率论部分）

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | 什么是机器学习 | Learn | - | ~45min |
| 02 | 线性回归从零实现 | Build | Python | ~75min |
| 03 | 逻辑回归与分类 | Build | Python | ~75min |
| 04 | 决策树 | Build | Python | ~75min |
| 05 | 支持向量机 | Build | Python | ~75min |
| 06 | KNN 与距离度量 | Build | Python | ~60min |
| 07 | 无监督学习 | Build | Python | ~75min |
| 08 | 特征工程 | Build | Python | ~75min |
| 09 | 模型评估 | Build | Python | ~75min |
| 10 | 偏差与方差 | Learn | Python | ~60min |
| 11 | 集成方法 | Build | Python | ~75min |
| 12 | 超参数调优 | Build | Python | ~60min |
| 13 | ML 流水线 | Build | Python | ~75min |
| 14 | 朴素贝叶斯 | Build | Python | ~60min |
| 15 | 时间序列 | Build | Python | ~75min |
| 16 | 异常检测 | Build | Python | ~60min |
| 17 | 不平衡数据处理 | Build | Python | ~60min |
| 18 | 特征选择 | Build | Python | ~60min |

## 常见困惑

- **"有了深度学习还需要学传统 ML 吗？"** → 绝对需要。传统 ML 在表格数据、小样本场景下仍然是最优选择，且理解传统 ML 是理解深度学习的必要基础。
- **"为什么要从零实现而不是直接调库？"** → 从零实现能让你真正理解算法原理和细节，调库只是几行代码的事，但出了问题你不会调试。
- **"学完这个阶段能做什么？"** → 能独立完成大部分经典 ML 任务：分类、回归、聚类、异常检测等，并能正确评估和调优模型。

## 开始学习

→ [第一课：什么是机器学习](01-what-is-machine-learning/docs/zh.md)
