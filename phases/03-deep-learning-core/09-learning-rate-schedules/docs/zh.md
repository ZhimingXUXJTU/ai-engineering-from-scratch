# 学习率调度与预热

> 学习率是最重要的超参数——不是架构，不是数据量，是学习率。

**类型：** 构建
**语言：** Python
**前置知识：** 第 03.06 课（优化器）、第 03.08 课（权重初始化）
**预计时间：** ~90 分钟

## 学习目标

- 从零实现恒定、阶梯衰减、余弦退火、warmup+余弦和 1cycle 学习率调度
- 演示学习率选择的三个失败模式：发散（太高）、停滞（太低）、振荡（不衰减）
- 解释为什么基于 Adam 的优化器需要 warmup 以及它如何稳定早期训练
- 在相同任务上对比所有五种调度的收敛速度

## 问题引入

学习率 0.1 → 训练 3 步就发散。0.0001 → 100 轮几乎不动。0.01 → 50 轮后开始振荡。最优学习率不是常数——它在训练中变化。早期需要大步快速覆盖距离，后期需要小步稳定到好的极小值。

每种主流模型都有精心调优的学习率调度：Llama 3 峰值 lr=3e-4 + 2000 步 warmup + cosine decay 到 3e-5。GPT-3 峰值 lr=6e-4 + 375M token warmup。

## 核心概念

### 恒定学习率

最简单的方法。选一个数，每步都用。很少是最优的。

### 阶梯衰减

ResNet 时代的方法。在固定 epoch 将学习率乘以因子（通常 10x）。ResNet-50 用 lr=0.1，在 epoch 30、60、90 各降 10 倍。

### 余弦退火

平滑地从最大学习率衰减到最小：

```
lr(t) = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(pi * t / T))
```

现代训练的默认选择。

### Warmup：为什么要从小学习率开始

Adam 维护梯度均值和方差的运行估计。第 0 步，这些估计初始化为零。前几步的梯度更新基于垃圾统计量。Warmup 从极小的学习率开始，线性升温到 lr_max，让 Adam 的统计量稳定下来。

```
lr(t) = lr_max * (t / warmup_steps)     当 t < warmup_steps
```

典型 warmup：总训练步的 1-5%。

### 线性 Warmup + 余弦衰减

现代默认。先线性升温，再余弦衰减。Llama、GPT、PaLM 和大多数现代 Transformer 都用这个。

### 1cycle 策略

Leslie Smith 2018 年的发现：训练前半段学习率从低到高，后半段从高到低。高学习率作为正则化，让模型探索更多损失景观。

## 动手实现

```python
import math

def constant_schedule(step, lr=0.01, **kwargs):
    return lr

def cosine_schedule(step, lr=0.01, total_steps=1000, lr_min=1e-5, **kwargs):
    if step >= total_steps:
        return lr_min
    return lr_min + 0.5 * (lr - lr_min) * (1 + math.cos(math.pi * step / total_steps))

def warmup_cosine_schedule(step, lr=0.01, total_steps=1000, warmup_steps=100, lr_min=1e-5, **kwargs):
    if step < warmup_steps:
        return lr * step / warmup_steps
    progress = (step - warmup_steps) / (total_steps - warmup_steps)
    return lr_min + 0.5 * (lr - lr_min) * (1 + math.cos(math.pi * progress))

def one_cycle_schedule(step, lr=0.01, total_steps=1000, **kwargs):
    mid = max(total_steps // 2, 1)
    if step < mid:
        return (lr / 25) + (lr - lr / 25) * step / mid
    else:
        progress = (step - mid) / max(total_steps - mid, 1)
        return lr * (1 - progress) + (lr / 10000) * progress
```

## 用框架实现

```python
from transformers import get_cosine_schedule_with_warmup

scheduler = get_cosine_schedule_with_warmup(
    optimizer,
    num_warmup_steps=2000,
    num_training_steps=100000,
)
```

HuggingFace 的函数是大多数 Llama 和 GPT 微调脚本使用的。不确定时，用 warmup + cosine，warmup = 总步数的 3-5%。

## 练习题

1. 实现指数衰减 lr(t) = lr_0 * gamma^t，对比余弦退火。
2. 实现学习率范围测试：训练几百步，学习率从 1e-7 指数增长到 1。
3. 变化 warmup 长度：0%、1%、5%、10%、20%，找到最稳定的点。
4. 实现带热重启的余弦退火（SGDR），对比标准余弦。
5. 构建"调度外科医生"，自动在损失稳定时切换调度。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| 学习率 (Learning rate) | "学多快" | 梯度更新的标量乘数；最重要的超参数 |
| 调度 (Schedule) | "随时间变 lr" | 训练步到学习率的映射函数 |
| Warmup | "从小 lr 开始" | 线性升温到目标 lr，稳定优化器统计量 |
| 余弦退火 (Cosine annealing) | "平滑 lr 衰减" | 按余弦曲线从 lr_max 衰减到 lr_min |
| 1cycle 策略 | "先升后降" | Leslie Smith 的方法，先升后降 lr 加速收敛 |
| 学习率范围测试 (LR range test) | "找最佳学习率" | 指数增长 lr 找到损失开始上升的点 |

## 延伸阅读

- Loshchilov & Hutter, "SGDR" (2017) —— 余弦退火和热重启
- Smith, "Super-Convergence" (2018) —— 1cycle 策略
- Touvron et al., "Llama 2" (2023) —— 大规模 warmup + cosine 调度
