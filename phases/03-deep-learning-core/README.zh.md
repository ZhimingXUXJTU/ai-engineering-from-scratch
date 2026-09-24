# Phase 3: 深度学习核心

> **13 节课 · ~15 小时 · 🟢入门**

## 在本阶段开始（GitHub）| Start this phase on GitHub

**前置条件：**Phase 1 线性代数直觉。建议同时完成 Phase 2，以掌握模型评估的基本词汇。

**第一课：**[感知机](01-the-perceptron/)

在仓库根目录运行以下命令：

```bash
python3 phases/03-deep-learning-core/01-the-perceptron/code/perceptron.py
```

保留命令、退出码、收敛门控（gate）结果、单个感知机在 XOR 上的失败结果，以及最终两层网络对 XOR 的预测。

**下一步：**解释为什么单条线性边界无法解决 XOR，然后继续学习 [多层网络与前向传播](02-multi-layer-networks/)。

浏览[完整的 Phase 3 课程列表](../../README.md#phase-3)或[跨阶段路线图](../../ROADMAP.md)。

## 学习目标

- 从感知机到多层网络，理解神经网络的基本架构
- 从零实现反向传播算法，真正理解梯度如何流动
- 掌握激活函数、损失函数、优化器、正则化等核心组件
- 搭建自己的迷你深度学习框架，再过渡到 PyTorch

## 前置知识

- Python 编程与 NumPy（Phase 0）
- 线性代数与微积分基础（Phase 1）
- 传统机器学习概念（Phase 2）

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | 感知机 | Learn | Python | ~45min |
| 02 | 多层网络 | Build | Python | ~60min |
| 03 | 反向传播从零实现 | Build | Python | ~90min |
| 04 | 激活函数 | Learn | Python | ~45min |
| 05 | 损失函数 | Learn | Python | ~45min |
| 06 | 优化器 | Build | Python | ~75min |
| 07 | 正则化 | Build | Python | ~60min |
| 08 | 权重初始化 | Learn | Python | ~45min |
| 09 | 学习率调度 | Build | Python | ~60min |
| 10 | 搭建迷你框架 | Build | Python | ~90min |
| 11 | PyTorch 入门 | Build | Python | ~75min |
| 12 | JAX 入门 | Build | Python | ~60min |
| 13 | 调试神经网络 | Build | Python | ~75min |

## 常见困惑

- **"为什么不能直接学 PyTorch？"** → 先理解底层原理，再用框架，你才能真正读懂错误信息、选择合适的架构、排查训练问题。框架只是工具，理解才是核心。
- **"反向传播太抽象了怎么办？"** → 第三课用代码一步步实现，配合可视化，比任何教材都直观。建议多运行几遍代码，手动跟踪梯度计算。
- **"迷你框架有什么用？"** → 搭建迷你框架是检验你是否真正理解所有组件的最好方式。它会成为你理解 PyTorch 等框架内部原理的桥梁。

## 开始学习

→ [第一课：感知机](01-the-perceptron/docs/zh.md)
