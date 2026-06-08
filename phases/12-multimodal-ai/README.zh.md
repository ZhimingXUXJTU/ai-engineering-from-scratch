# Phase 12: 多模态 AI

> **25 节课 · ~65 小时 · 🔴高级**

## 学习目标

- 理解视觉 Transformer 的 Patch-Token 原语和 CLIP 对比预训练
- 掌握 LLaVA、BLIP-2、Flamingo 等视觉语言模型的架构设计
- 深入学习视频理解、音频语言模型和全模态模型
- 了解 Transfusion、Janus-Pro 等统一生成架构的前沿进展
- 学习多模态 RAG、文档理解和多模态 Agent 的实际应用

## 前置知识

- Transformer 深度理解（Phase 7：注意力机制、编码器-解码器）
- 视觉基础（Phase 4：CNN、ViT，推荐）
- NLP 基础（Phase 5：嵌入、语言模型，推荐）

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | 视觉 Transformer 与 Patch-Token 原语 | Learn | Python | ~120min |
| 02 | CLIP 对比视觉语言预训练 | Build | Python | ~180min |
| 03 | BLIP-2 与 Q-Former 模态桥接 | Learn | Python | ~180min |
| 04 | Flamingo 门控交叉注意力 | Learn | Python | ~120min |
| 05 | LLaVA 视觉指令微调 | Build | Python | ~180min |
| 06 | 任意分辨率视觉：Patch-n'-Pack | Learn | Python | ~120min |
| 07 | 开源 VLM 实战配方 | Build | Python | ~180min |
| 08 | LLaVA-OneVision：图像与视频 | Build | Python | ~180min |
| 09 | Qwen-VL 系列与动态 FPS 视频 | Learn | Python | ~120min |
| 10 | InternVL3 原生多模态预训练 | Learn | Python | ~120min |
| 11 | Chameleon 早期融合 Token 方案 | Learn | Python | ~180min |
| 12 | Emu3 下一 Token 预测生成 | Learn | Python | ~120min |
| 13 | Transfusion 自回归+扩散 | Learn | Python | ~180min |
| 14 | Show-o 离散扩散统一模型 | Learn | Python | ~120min |
| 15 | Janus-Pro 解耦编码器 | Learn | Python | ~120min |
| 16 | MIO 任意到任意流式模型 | Learn | Python | ~120min |
| 17 | 视频-语言时序定位 | Build | Python | ~180min |
| 18 | 长视频理解与百万 Token 上下文 | Learn | Python | ~180min |
| 19 | 音频语言模型：从 Whisper 到 AF3 | Learn | Python | ~180min |
| 20 | 全能模型：Thinker-Talker | Learn | Python | ~180min |
| 21 | 具身智能 VLA：OpenVLA、Pi0、GR00T | Learn | Python | ~180min |
| 22 | 文档与图表理解 | Build | Python | ~180min |
| 23 | ColPali 视觉原生文档 RAG | Build | Python | ~180min |
| 24 | 多模态 RAG 与跨模态检索 | Build | Python | ~180min |
| 25 | 多模态 Agent 与计算机操控（毕业项目） | Build | Python | ~240min |

## 常见困惑

- **"多模态 AI 和视觉模型有什么区别？"** → 视觉模型只处理图像，多模态 AI 同时理解图像、文本、音频等多种输入。核心挑战是如何在不同模态之间建立统一的表示空间。
- **"这么多模型都要学吗？"** → 不需要。建议重点学第 01-05 课（基础架构）和第 25 课（应用），其余按兴趣选学。模型架构虽然多，但核心思想是相通的。
- **"这些模型需要多大的 GPU？"** → 推理阶段 24GB 显存可运行大部分开源 VLM。第 07 课会介绍不同硬件配置下的实用方案。

## 开始学习

→ [第一课：视觉 Transformer 与 Patch-Token 原语](01-vision-transformer-patch-tokens/docs/zh.md)
