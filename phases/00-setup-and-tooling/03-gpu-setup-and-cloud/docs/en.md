# GPU Setup & Cloud | GPU 设置与云平台

> Training on CPU is fine for learning. Training for real needs a GPU.
> 用 CPU 训练用来学习没问题。但真正的训练需要 GPU。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 0, Lesson 01 | **前置知识:** Phase 0, 第 01 课
**Time:** ~45 minutes | **时间:** ~45 分钟

## Learning Objectives | 学习目标

- Verify local GPU availability using `nvidia-smi` and PyTorch's CUDA API
  中文翻译：使用 `nvidia-smi` 和 PyTorch 的 CUDA API 验证本地 GPU 是否可用
- Configure Google Colab with a T4 GPU for free cloud-based experiments
  中文翻译：配置 Google Colab 的 T4 GPU，进行免费云端实验
- Benchmark matrix multiplication on CPU vs GPU and measure the speedup
  中文翻译：对 CPU 和 GPU 的矩阵乘法进行基准测试，测量加速比
- Estimate the largest model that fits in your VRAM using the fp16 rule of thumb
  中文翻译：用 fp16 经验法则估算你的显存能装下的最大模型

> **【中文解读】**
> 本章教你如何配置 GPU 加速。在 AI 中，GPU 是训练模型的关键硬件——它能把训练时间从几小时缩短到几分钟。没有本地 GPU 也可以用免费的 Google Colab。

## The Problem | 问题描述

Most lessons in phases 1-3 run fine on CPU. But once you start training CNNs, transformers, or LLMs (phases 4+), you need GPU acceleration. A training run that takes 8 hours on CPU takes 10 minutes on GPU.

> 阶段 1-3 的大部分课程在 CPU 上运行良好。但一旦开始训练 CNN、Transformer 或 LLM（阶段 4+），就需要 GPU 加速。CPU 上 8 小时的训练，在 GPU 上只需 10 分钟。

You have three options: local GPU, cloud GPU, or Google Colab (free).

> 你有三种选择：本地 GPU、云端 GPU 或 Google Colab（免费）。

> **【中文解读】**
> 阶段 1-3 的课程在 CPU 上就能跑。但从阶段 4 开始（CNN、Transformer、LLM），没有 GPU 会慢到无法接受。CPU 上 8 小时的训练，GPU 上只要 10 分钟。

## The Concept | 核心概念

```
Your options:

1. Local NVIDIA GPU          # 本地 NVIDIA 显卡
   Cost: $0 (you already have it)  # 免费（已有硬件）
   Setup: Install CUDA + cuDNN
   Best for: Regular use, large datasets  # 适合：日常使用、大数据集

2. Google Colab (free tier)  # 免费 Colab
   Cost: $0
   Setup: None               # 无需安装
   Best for: Quick experiments, no GPU at home  # 适合：快速实验、家里没有 GPU

3. Cloud GPU (Lambda, RunPod, Vast.ai)  # 云端 GPU 租赁
   Cost: $0.20-2.00/hr       # 按小时计费
   Setup: SSH + install
   Best for: Serious training, large models  # 适合：正式训练、大模型
```

> **【拓展：GPU 为什么适合 AI？】**
> GPU 拥有数千个核心，擅长并行执行大量简单计算（如矩阵乘法）。神经网络的训练本质上就是海量的矩阵运算，因此 GPU 能提供数十到上百倍的加速。NVIDIA 的 CUDA 是目前 AI 领域的主流 GPU 计算平台。

## Build It | 动手搭建

> **【中文解读】** 以下提供三种 GPU 方案：本地 NVIDIA 显卡（免费但需要硬件）、Google Colab（免费云 GPU）、云 GPU 租赁（按小时付费）。根据你的条件选择一种即可。

### Option 1: Local NVIDIA GPU | 本地 NVIDIA GPU

Check if you have one:

> 检查你是否有本地 GPU：

```bash
nvidia-smi  # 查看 GPU 状态和驱动信息
```

Install PyTorch with CUDA:

> 安装支持 CUDA 的 PyTorch：

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")  # 检查 CUDA 是否可用
print(f"CUDA version: {torch.version.cuda}")  # CUDA 版本号
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")  # GPU 型号
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")  # 显存大小
```

### Option 2: Google Colab | 谷歌 Colab（免费 GPU）

1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Runtime > Change runtime type > T4 GPU  # 运行时 > 更改运行时类型 > 选择 T4 GPU
3. Run `!nvidia-smi` to verify  # 验证 GPU 是否可用

Upload notebooks from this course directly to Colab.

> 将本课程的 notebook 直接上传到 Colab。

### Option 3: Cloud GPU | 云 GPU

For Lambda Labs, RunPod, or Vast.ai:

> 用于 Lambda Labs、RunPod 或 Vast.ai：

```bash
ssh user@your-gpu-instance

pip install torch torchvision torchaudio
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### No GPU? No problem. | 没 GPU？没关系。

> **【拓展：显存估算经验公式】** fp16 下每个参数占 2 字节。7B 参数模型（如 Llama 2 7B）需要约 14GB 显存。加上优化器状态（Adam 需要 2 倍参数量的额外显存），训练 7B 模型实际需要约 40-50GB 显存（一张 A100 80GB 可以跑）。推理则只需约 14GB。这就是为什么 `device = "cuda" if available else "cpu"` 这行代码在 AI 工程中随处可见。

Most lessons work on CPU. The ones that need GPU will say so and include Colab links.

> 大部分课程在 CPU 上就能运行。需要 GPU 的课程会特别说明并提供 Colab 链接。

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 自动选择 GPU 或 CPU
print(f"Using: {device}")
```

## Build It: GPU vs CPU benchmark | GPU vs CPU 基准测试

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
    print(f"Speedup: {cpu_time / gpu_time:.0f}x")  # 加速倍数
```

> **【中文解读】**
> 上面的代码对比了 CPU 和 GPU 在矩阵乘法上的速度差异。矩阵乘法是神经网络训练中最核心的运算，GPU 的加速效果直接决定了训练效率。

## Exercises | 练习题

1. Run the benchmark above and compare CPU vs GPU times
   运行上面的基准测试，对比 CPU 和 GPU 的速度
2. If you don't have a GPU, run it on Google Colab and compare
   如果没有本地 GPU，在 Google Colab 上运行并对比
3. Check how much GPU memory you have and estimate the largest model you can fit (rule of thumb: 2 bytes per parameter for fp16)
   检查你的 GPU 显存大小，估算能装下的最大模型（经验法则：fp16 下每个参数占 2 字节）

## Key Terms | 关键术语

> **【拓展：2026 年 GPU 市场参考】** AI 训练的主流 GPU：RTX 4090（24GB，~$1600，个人学习首选）、A100（80GB，云端约 $2/hr）、H100（80GB，云端约 $3/hr，训练大模型首选）。Google Colab 免费版提供 T4（16GB），足够跑完本课程大部分实验。

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| CUDA | "GPU programming" | NVIDIA's parallel computing platform that lets you run code on the GPU |
| VRAM | "GPU memory" | Video RAM on the GPU, separate from system RAM. Limits model size. |
| fp16 | "Half precision" | 16-bit floating point, uses half the memory of fp32 with minimal accuracy loss |
| Tensor Core | "Fast matrix hardware" | Specialized GPU cores for matrix multiplication, 4-8x faster than regular cores |

| 术语 | 俗称 | 实际含义 |
|------|------|---------|
| CUDA | "GPU 编程" | NVIDIA 的并行计算平台，让你能在 GPU 上运行代码 |
| VRAM | "显存" | GPU 上的视频内存，独立于系统内存，决定了能跑多大的模型 |
| fp16 | "半精度" | 16 位浮点数，占用 fp32 一半的内存，精度损失极小 |
| Tensor Core | "快速矩阵硬件" | GPU 上专门做矩阵乘法的核心，比普通核心快 4-8 倍 |
