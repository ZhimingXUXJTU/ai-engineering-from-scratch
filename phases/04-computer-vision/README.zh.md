# Phase 4: 计算机视觉

> **28 节课 · ~27 小时 · 🟡进阶**

## 在本阶段开始（GitHub）| Start this phase on GitHub

**前置条件：**Phase 1 第 12 课（张量运算）和 Phase 3 第 11 课（PyTorch 入门）。第一个演示只需要 NumPy。

**第一课：**[图像基础](01-image-fundamentals/)

在仓库根目录运行以下命令：

```bash
python3 phases/04-computer-vision/01-image-fundamentals/code/main.py
```

保留命令、退出码、HWC 与 CHW 形状、归一化后的通道统计、往返像素差异和插值粗糙度。该演示会生成确定性的合成图像，不使用网络。

**下一步：**解释 HWC 与 CHW 之间哪根轴发生了变化，然后继续学习 [卷积从零实现](02-convolutions-from-scratch/)。

浏览[完整的 Phase 4 课程列表](../../README.md#phase-4)或[跨阶段路线图](../../ROADMAP.md)。

## 学习目标

- 理解图像的基本表示和卷积操作的数学原理
- 从 LeNet 到 ResNet，掌握经典 CNN 架构的演进思路
- 学会目标检测、图像分割、图像生成等核心视觉任务
- 深入扩散模型、视觉 Transformer、3D 视觉等前沿方向

## 前置知识

- 深度学习基础（Phase 3：神经网络、反向传播、PyTorch）
- 线性代数与微积分（Phase 1）

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | 图像基础 | Learn | Python | ~45min |
| 02 | 卷积从零实现 | Build | Python | ~75min |
| 03 | CNN 从 LeNet 到 ResNet | Build | Python | ~75min |
| 04 | 图像分类 | Build | Python | ~60min |
| 05 | 迁移学习 | Build | Python | ~60min |
| 06 | 目标检测 YOLO | Build | Python | ~75min |
| 07 | 语义分割 U-Net | Build | Python | ~75min |
| 08 | 实例分割 Mask R-CNN | Build | Python | ~75min |
| 09 | 图像生成 GAN | Build | Python | ~75min |
| 10 | 图像生成扩散模型 | Build | Python | ~75min |
| 11 | Stable Diffusion | Build | Python | ~75min |
| 12 | 视频理解 | Build | Python | ~60min |
| 13 | 3D 视觉 NeRF | Build | Python | ~75min |
| 14 | 视觉 Transformer | Build | Python | ~75min |
| 15 | 实时与边缘部署 | Build | Python | ~60min |
| 16 | 视觉流水线毕业项目 | Build | Python | ~90min |
| 17 | 自监督视觉 | Learn | Python | ~60min |
| 18 | 开放词汇 CLIP | Build | Python | ~60min |
| 19 | OCR 与文档理解 | Build | Python | ~60min |
| 20 | 图像检索与度量学习 | Build | Python | ~60min |
| 21 | 关键点与姿态估计 | Build | Python | ~60min |
| 22 | 3D 高斯泼溅 | Build | Python | ~75min |
| 23 | 扩散 Transformer 与矫正流 | Build | Python | ~75min |
| 24 | SAM3 开放词汇分割 | Build | Python | ~60min |
| 25 | 视觉语言模型 | Learn | Python | ~60min |
| 26 | 单目深度估计 | Build | Python | ~60min |
| 27 | 多目标跟踪 | Build | Python | ~60min |
| 28 | 世界模型与视频扩散 | Build | Python | ~75min |

## 常见困惑

- **"CV 领域发展太快，学哪个方向？"** → 建议先掌握 01-06 核心课程（图像基础到目标检测），这是所有 CV 方向的基石。扩散模型和视觉 Transformer 是当前最热门的方向。
- **"需要 GPU 吗？"** → 大部分课程可以用 CPU 运行简化版代码。完整的 GAN 和扩散模型训练需要 GPU，推荐使用 Google Colab 免费 GPU。
- **"28 节课太多了怎么安排？"** → 分两轮学习：第一轮学 01-11 基础部分，第二轮按兴趣选择 12-28 前沿方向。

## 开始学习

→ [第一课：图像基础](01-image-fundamentals/docs/zh.md)
