# Phase 7: Transformer 深度解析

> **16 节课 · ~16 小时 · 🟡进阶**

## 学习目标

- 理解自注意力机制（Self-Attention）的数学原理与实现
- 掌握多头注意力、位置编码、编码器-解码器等 Transformer 核心组件
- 深入分析 BERT、GPT、T5 等经典模型的架构设计
- 了解 MoE、KV Cache、Flash Attention 等推理优化技术
- 理解缩放定律（Scaling Laws）对模型训练的指导意义

## 前置知识

- 深度学习基础（Phase 3：神经网络、反向传播、PyTorch）
- NLP 基础（Phase 5：注意力机制、序列模型）
- 线性代数基础（Phase 1：矩阵运算）

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | 为什么需要 Transformer | Learn | Python | ~45min |
| 02 | 自注意力从零实现 | Build | Python | ~75min |
| 03 | 多头注意力 | Build | Python | ~75min |
| 04 | 位置编码 — 正弦、RoPE、ALiBi | Learn | Python | ~45min |
| 05 | 完整 Transformer — 编码器+解码器 | Build | Python | ~75min |
| 06 | BERT 掩码语言模型 | Build | Python | ~45min |
| 07 | GPT 因果语言模型 | Build | Python | ~75min |
| 08 | T5、BART 编码器-解码器模型 | Learn | Python | ~45min |
| 09 | 视觉 Transformer (ViT) | Learn | Python | ~45min |
| 10 | 音频 Transformer — Whisper 架构 | Learn | Python | ~45min |
| 11 | 混合专家模型 (MoE) | Learn | Python | ~45min |
| 12 | KV Cache、Flash Attention 与推理优化 | Build | Python | ~75min |
| 13 | 缩放定律 | Learn | Python | ~45min |
| 14 | 从零构建 Transformer — 毕业项目 | Build | Python | ~120min |
| 15 | 注意力变体 — 滑动窗口、稀疏、差分 | Learn | Python | ~60min |
| 16 | 推测解码 — 草案、验证、重复 | Learn | Python | ~60min |

## 常见困惑

- **"Attention is All You Need 论文太长，读不懂？"** → 本阶段从自注意力机制开始，逐步拆解每个组件，配合代码实现，让你真正理解而不仅仅是背诵公式。
- **"BERT 和 GPT 有什么区别？"** → BERT 是双向编码器（适合理解任务），GPT 是单向解码器（适合生成任务）。第 06、07 课会对比讲解。
- **"MoE、Flash Attention 这些值得学吗？"** → 这些是当前大模型的核心技术。Mixtral、DeepSeek-V3 都用 MoE 架构；Flash Attention 是训练和推理的标配优化。

## 开始学习

→ [第一课：为什么需要 Transformer](01-why-transformers/docs/zh.md)
