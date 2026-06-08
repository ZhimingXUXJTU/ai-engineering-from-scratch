# Phase 10: 从零构建 LLM

> **25 节课 · ~26 小时 · 🔴高级**

## 学习目标

- 从零实现分词器（BPE、WordPiece、SentencePiece）
- 掌握大模型预训练的数据流水线和分布式训练技术
- 深入理解 SFT、RLHF、DPO 等对齐训练方法
- 学习量化、推理优化、推测解码等部署技术
- 通过 DeepSeek-V3 等前沿模型架构解析，了解最新技术趋势

## 前置知识

- Transformer 架构（Phase 7：自注意力、多头注意力、位置编码）
- 强化学习基础（Phase 9：PPO、奖励建模，推荐）
- 深度学习工程基础（Phase 3：PyTorch、训练调试）

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | 分词器 — BPE、WordPiece、SentencePiece | Learn | Python | ~45min |
| 02 | 从零构建分词器 | Build | Python | ~75min |
| 03 | 预训练数据流水线 | Build | Python | ~75min |
| 04 | 预训练 Mini GPT (124M) | Build | Python | ~120min |
| 05 | 扩展 — 分布式训练、FSDP、DeepSpeed | Build | Python | ~75min |
| 06 | 指令微调 (SFT) | Build | Python | ~75min |
| 07 | RLHF — 奖励模型 + PPO 训练 | Build | Python | ~75min |
| 08 | DPO — 直接偏好优化 | Build | Python | ~75min |
| 09 | Constitutional AI 与自我改进 | Learn | Python | ~45min |
| 10 | 评估 — 基准测试、评估框架、LM Harness | Build | Python | ~75min |
| 11 | 量化 — INT8、GPTQ、AWQ、GGUF | Build | Python | ~75min |
| 12 | 推理优化 | Build | Python | ~75min |
| 13 | 构建完整 LLM 流水线 | Build | Python | ~120min |
| 14 | 开源模型架构解析 | Learn | Python | ~45min |
| 15 | 推测解码与 EAGLE-3 | Build | Python | ~75min |
| 16 | 差分注意力 (V2) | Learn | Python | ~60min |
| 17 | 原生稀疏注意力 (DeepSeek NSA) | Learn | Python | ~60min |
| 18 | 多 Token 预测 (MTP) | Learn | Python | ~60min |
| 19 | DualPipe 并行策略 | Learn | Python | ~60min |
| 20 | DeepSeek-V3 架构解析 | Learn | Python | ~75min |
| 21 | Jamba — 混合 SSM-Transformer | Learn | Python | ~60min |
| 22 | 异步 Hogwild! 推理 | Learn | Python | ~60min |
| 23 | 投机解码与 EAGLE | Build | Python | ~60min |
| 24 | 梯度检查点与激活重计算 | Learn | Python | ~60min |

## 常见困惑

- **"需要多少 GPU 才能训练大模型？"** → 课程从 124M 参数的小模型开始，单卡即可完成。分布式训练（第 05 课）会讲解多卡和集群方案。
- **"RLHF 和 DPO 有什么区别？"** → RLHF 需要训练奖励模型 + PPO 优化（两步），DPO 直接从偏好数据学习（一步）。DPO 更简单但 RLHF 在某些场景下效果更好。
- **"量化会损失很多质量吗？"** → INT4/INT8 量化通常只损失不到 1% 的性能，但推理速度可以提升 2-4 倍。第 11 课会详细对比各种量化方案。

## 开始学习

→ [第一课：分词器 — BPE、WordPiece、SentencePiece](01-tokenizers/docs/zh.md)
