# Phase 8: 生成式 AI

> **15 节课 · ~15 小时 · 🔴高级**

## 学习目标

- 理解生成模型的分类体系与历史发展脉络
- 掌握 VAE、GAN、扩散模型三大生成范式的核心原理
- 深入理解 Stable Diffusion、ControlNet、LoRA 等图像生成技术
- 了解视频生成、音频生成、3D 生成等多模态生成前沿方向
- 学习 FID、CLIP Score 等生成模型的评估方法

## 前置知识

- 深度学习基础（Phase 3：神经网络、优化器、PyTorch）
- 概率与统计基础（Phase 1：概率分布、贝叶斯定理）
- 计算机视觉基础（Phase 4：CNN、图像处理，推荐）

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | 生成模型分类与历史 | Learn | Python | ~45min |
| 02 | 自编码器与 VAE | Build | Python | ~75min |
| 03 | GAN — 生成器与判别器 | Build | Python | ~75min |
| 04 | 条件 GAN 与 Pix2Pix | Build | Python | ~75min |
| 05 | StyleGAN | Learn | Python | ~45min |
| 06 | 扩散模型 — DDPM 从零实现 | Build | Python | ~75min |
| 07 | 潜扩散与 Stable Diffusion | Build | Python | ~75min |
| 08 | ControlNet、LoRA 与图像条件控制 | Build | Python | ~75min |
| 09 | 图像修复、外绘与编辑 | Build | Python | ~75min |
| 10 | 视频生成 | Learn | Python | ~45min |
| 11 | 音频生成 | Learn | Python | ~45min |
| 12 | 3D 生成 | Learn | Python | ~45min |
| 13 | 流匹配与矫正流 | Learn | Python | ~45min |
| 14 | 评估 — FID、CLIP Score、人类偏好 | Learn | Python | ~45min |
| 15 | 视觉自回归建模 (VAR) | Learn | Python | ~60min |

## 常见困惑

- **"GAN、VAE、扩散模型有什么区别？"** → GAN 通过对抗训练生成，VAE 通过变分推断学习潜在空间，扩散模型通过逐步去噪生成。扩散模型是当前主流方向，但理解前两者有助于把握全貌。
- **"Stable Diffusion 和 DALL-E 是一回事吗？"** → 核心都是扩散模型，但 Stable Diffusion 使用潜空间（Latent Space）降低计算成本，且开源可本地运行。
- **"生成模型需要很贵的 GPU 吗？"** → 推理阶段 8GB 显存即可运行 Stable Diffusion。训练自己的模型需要高端 GPU，但课程提供了 Colab 方案。

## 开始学习

→ [第一课：生成模型分类与历史](01-generative-models-taxonomy-history/docs/zh.md)
