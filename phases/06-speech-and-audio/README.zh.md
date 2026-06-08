# Phase 6: 语音与音频

> **17 节课 · ~18 小时 · 🟡进阶**

## 学习目标

- 理解音频信号的数学基础和特征提取方法（频谱图、梅尔特征）
- 掌握语音识别（ASR）的原理和实现，包括 Whisper 架构
- 学习语音合成（TTS）和声音克隆的技术方案
- 构建完整的语音助手流水线，整合识别、理解和合成

## 前置知识

- 深度学习基础（Phase 3：神经网络、PyTorch）
- 傅里叶变换基础（Phase 1 第 20 课，可选）
- NLP 基础（Phase 5 的文本处理部分，推荐）

## 课程清单

| # | 课程 | 类型 | 语言 | 预计时间 |
|---|------|------|------|---------|
| 01 | 音频基础 | Learn | Python | ~60min |
| 02 | 频谱图与梅尔特征 | Build | Python | ~60min |
| 03 | 音频分类 | Build | Python | ~60min |
| 04 | 语音识别 ASR | Build | Python | ~75min |
| 05 | Whisper 架构与微调 | Build | Python | ~75min |
| 06 | 说话人识别与验证 | Build | Python | ~60min |
| 07 | 文本转语音 TTS | Build | Python | ~75min |
| 08 | 声音克隆与转换 | Build | Python | ~75min |
| 09 | 音乐生成 | Build | Python | ~60min |
| 10 | 音频语言模型 | Learn | Python | ~60min |
| 11 | 实时音频处理 | Build | Python | ~75min |
| 12 | 语音助手流水线 | Build | Python | ~90min |
| 13 | 神经音频编解码器 | Build | Python | ~60min |
| 14 | 语音活动检测与轮次管理 | Build | Python | ~60min |
| 15 | 流式语音到语音（Moshi/Hibiki） | Build | Python | ~75min |
| 16 | 反欺骗与音频水印 | Learn | Python | ~60min |
| 17 | 音频评估指标 | Learn | Python | ~45min |

## 常见困惑

- **"音频处理需要很多数学吗？"** → 基础部分需要一些信号处理知识（如傅里叶变换），但课程会用代码和可视化来讲解，不需要推导数学证明。
- **"语音识别和大模型的关系？"** → 现代语音识别（如 Whisper）本质上也是基于 Transformer 的序列模型。语音+大模型的结合（语音语言模型）是当前前沿方向。
- **"做语音项目需要特殊硬件吗？"** → 推理阶段 CPU 即可，训练自定义模型建议使用 GPU。声音克隆和实时处理对延迟敏感，建议使用 GPU 推理。

## 开始学习

→ [第一课：音频基础](01-audio-fundamentals/docs/zh.md)
