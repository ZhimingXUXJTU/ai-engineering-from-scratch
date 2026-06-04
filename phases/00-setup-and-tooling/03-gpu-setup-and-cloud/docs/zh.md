# GPU 设置与云平台

> 用 CPU 训练用于学习没问题。真正训练模型需要 GPU。

**类型：** 动手实践
**语言：** Python
**前置条件：** Phase 0, Lesson 01
**预计用时：** 约 45 分钟

## 学习目标

- 使用 `nvidia-smi` 和 PyTorch 的 CUDA API 验证本地 GPU 是否可用
- 配置 Google Colab 使用 T4 GPU 进行免费云端实验
- 对比 CPU 与 GPU 的矩阵乘法性能并测量加速比
- 使用 fp16 经验法则估算 VRAM 能容纳的最大模型

> **【中文解读】**
> 本章教你如何配置 GPU 加速。在 AI 中，GPU 是训练模型的关键硬件——它能把训练时间从几小时缩短到几分钟。没有本地 GPU 也可以用免费的 Google Colab。

## 问题引入

阶段 1-3 的大部分课程在 CPU 上运行良好。但一旦开始训练 CNN、Transformer 或 LLM（阶段 4+），你就需要 GPU 加速。在 CPU 上需要 8 小时的训练，在 GPU 上只需 10 分钟。

你有三个选择：本地 GPU、云 GPU 或 Google Colab（免费）。

> **【中文解读】**
> 阶段 1-3 的课程在 CPU 上就能跑。但从阶段 4 开始（CNN、Transformer、LLM），没有 GPU 会慢到无法接受。CPU 上 8 小时的训练，GPU 上只要 10 分钟。

## 核心概念

```
你的选择：

1. 本地 NVIDIA 显卡
   费用: $0（已有硬件）
   设置: 安装 CUDA + cuDNN
   适合: 日常使用、大数据集

2. Google Colab（免费层）
   费用: $0
   设置: 无需安装
   适合: 快速实验、家里没有 GPU

3. 云 GPU（Lambda、RunPod、Vast.ai）
   费用: $0.20-2.00/小时
   设置: SSH + 安装
   适合: 正式训练、大模型
```

> **【拓展：GPU 为什么适合 AI？】**
> GPU 拥有数千个核心，擅长并行执行大量简单计算（如矩阵乘法）。神经网络的训练本质上就是海量的矩阵运算，因此 GPU 能提供数十到上百倍的加速。NVIDIA 的 CUDA 是目前 AI 领域的主流 GPU 计算平台。

## 动手搭建

> **【中文解读】** 以下提供三种 GPU 方案：本地 NVIDIA 显卡（免费但需要硬件）、Google Colab（免费云 GPU）、云 GPU 租赁（按小时付费）。根据你的条件选择一种即可。

### 选项 1：本地 NVIDIA GPU

检查是否有 NVIDIA GPU：

```bash
nvidia-smi  # 查看 GPU 状态和驱动信息
```

安装支持 CUDA 的 PyTorch：

```python
import torch

print(f"CUDA 可用: {torch.cuda.is_available()}")  # 检查 CUDA 是否可用
print(f"CUDA 版本: {torch.version.cuda}")  # CUDA 版本号
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")  # GPU 型号
    print(f"显存: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")  # 显存大小
```

### 选项 2：Google Colab（免费 GPU）

1. 前往 [colab.research.google.com](https://colab.research.google.com)
2. 运行时 > 更改运行时类型 > 选择 T4 GPU
3. 运行 `!nvidia-smi` 验证

可以直接将本课程的 notebook 上传到 Colab。

### 选项 3：云 GPU

适用于 Lambda Labs、RunPod 或 Vast.ai：

```bash
ssh user@your-gpu-instance

pip install torch torchvision torchaudio
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### 没 GPU？没关系。

> **【拓展：显存估算经验公式】** fp16 下每个参数占 2 字节。7B 参数模型（如 Llama 2 7B）需要约 14GB 显存。加上优化器状态（Adam 需要 2 倍参数量的额外显存），训练 7B 模型实际需要约 40-50GB 显存（一张 A100 80GB 可以跑）。推理则只需约 14GB。这就是为什么 `device = "cuda" if available else "cpu"` 这行代码在 AI 工程中随处可见。

大部分课程在 CPU 上可以运行。需要 GPU 的课程会特别说明并提供 Colab 链接。

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 自动选择 GPU 或 CPU
print(f"使用: {device}")
```

## GPU vs CPU 基准测试

```python
import torch
import time

size = 5000

a_cpu = torch.randn(size, size)  # 生成随机矩阵 A
b_cpu = torch.randn(size, size)  # 生成随机矩阵 B

start = time.time()
c_cpu = a_cpu @ b_cpu  # CPU 矩阵乘法
cpu_time = time.time() - start
print(f"CPU: {cpu_time:.3f}s")

if torch.cuda.is_available():
    a_gpu = a_cpu.to("cuda")  # 将矩阵移到 GPU
    b_gpu = b_cpu.to("cuda")

    torch.cuda.synchronize()  # 等待 GPU 完成所有操作
    start = time.time()
    c_gpu = a_gpu @ b_gpu  # GPU 矩阵乘法
    torch.cuda.synchronize()  # 同步，确保计时准确
    gpu_time = time.time() - start
    print(f"GPU: {gpu_time:.3f}s")
    print(f"加速比: {cpu_time / gpu_time:.0f}x")  # 加速倍数
```

> **【中文解读】**
> 上面的代码对比了 CPU 和 GPU 在矩阵乘法上的速度差异。矩阵乘法是神经网络训练中最核心的运算，GPU 的加速效果直接决定了训练效率。

## 练习题

1. 运行上面的基准测试，对比 CPU 和 GPU 的速度
2. 如果没有本地 GPU，在 Google Colab 上运行并对比
3. 检查你的 GPU 显存大小，估算能装下的最大模型（经验法则：fp16 下每个参数占 2 字节）

## 术语速查表

> **【拓展：2026 年 GPU 市场参考】** AI 训练的主流 GPU：RTX 4090（24GB，~$1600，个人学习首选）、A100（80GB，云端约 $2/hr）、H100（80GB，云端约 $3/hr，训练大模型首选）。Google Colab 免费版提供 T4（16GB），足够跑完本课程大部分实验。

| 术语 | 俗称 | 实际含义 |
|------|------|---------|
| CUDA | "GPU 编程" | NVIDIA 的并行计算平台，让你能在 GPU 上运行代码 |
| VRAM | "显存" | GPU 上的视频内存，独立于系统内存，决定了能跑多大的模型 |
| fp16 | "半精度" | 16 位浮点数，占用 fp32 一半的内存，精度损失极小 |
| Tensor Core | "快速矩阵硬件" | GPU 上专门做矩阵乘法的核心，比普通核心快 4-8 倍 |
