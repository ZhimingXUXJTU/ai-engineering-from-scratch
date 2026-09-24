# 云计算和云计算平台

> 实用训练需要一个GPU.
> 实际训练需要一个GPU.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 0, Lesson 01 | **前置知识:** Phase 0, 第 01 课
**Time:** ~45 minutes | **时间:** ~45 分钟

## 学习目标

- 使用 `nvidia-smi`并且PyTorch的CUDAAPI
  中文翻译:使用 `nvidia-smi`和 PyTorch 的 CUDA API 验证本地GPU 是否可用
- 使用T4GPU配置Google Colab,可进行免费的基于云的实验
  中文翻译:配置谷歌Colab的T4GPU,进行免费云端实验
- 测量CPU与GPU的基数乘法,测量加快速度
  中文翻译:对CPU和GPU的矩阵乘法进行基准测试,测量加速比
- 根据fp16指纹,估计适合VRAM的最大模型
  中文翻译:用fp16 经验法则估算你的显存能装下的最大模型

> **【中文解读】**
> 在人工智能中,GPU是训练模型的关键硬件,它可以将训练时间从几个小时缩短到几分钟.

## 问题 问题描述

在1-3阶段的大部分课程都在CPU上运行得很好.但是一旦你开始训练CNN,变压器或LLM (阶段4+),你需要GPU加速.一个8小时的训练运行在CPU上需要10分钟的GPU.

> 阶段 1-3 的大部分课程都在CPU上运行良好.但是一旦开始训练CNN、Transformer或LLM(阶段 4+),就需要GPU加快.

你有三个选择:本地GPU,云GPU或谷歌Collab (免费).

> 你有三种选择:本地GPU、云端GPU或谷歌Collab(免费)

> **【中文解读】**
> 阶段 1-3 的课程在CPU上就能跑.但从阶段 4 开始,没有GPU会慢到无法接受.

## 概念的核心概念

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
>  GPU 拥有数千个核心,擅长并行执行大量简单计算. 神经网络的训练本质上就是大量矩阵运算,因此 GPU 能够提供数十到百倍的加速.
```figure
s0-gpu-dispatch
```

## 建立它

## 动手建造

> **【中文解读】**以下提供三种GPU方案:本地NVIDIA显卡(免费但需要硬件)、谷歌Collab(免费云GPU)、云GPU租(按小时付费)。根据你的条件选择一种即可──

### 选择1:本地NVIDIA GPU

检查你是否有:

> 检查你是否有本地GPU:

```bash
nvidia-smi  # 查看 GPU 状态和驱动信息
```

安装PyTorch与CUDA:

> 装备支持CUDA的 PyTorch:

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")  # 检查 CUDA 是否可用
print(f"CUDA version: {torch.version.cuda}")  # CUDA 版本号
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")  # GPU 型号
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")  # 显存大小
```

### 选择2:谷歌协作

1. 走去[colab.research.google.com](https://colab.research.google.com)
2. 运行时 > 改变运行时类型 > 选择T4 GPU
3. 跑步`!nvidia-smi`验证GPU是否可用

直接将课程的笔记本上传到科拉布.

> 将本课程的笔记本直接传递到科拉布.

### 选择3:云GPU

对于Lambda Labs,RunPod或Vast.ai:

> 用于Lambda Labs、RunPod或Vast.ai:

```bash
ssh user@your-gpu-instance

pip install torch torchvision torchaudio
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### 没有GPU?没有问题.没有GPU?没有关系.

> **【拓展：显存估算经验公式】**对于每一个参数,Fp16 下每个参数占2 字节──7B 参数模型(如Llama 2 7B) 需要约14GB 显存──加上优化器状态(Adam 需要2倍参数额外显存),训练 7B 模型实际需要约40-50GB 显存──一张A100 80GB 可以运行)──推则只需要约14GB──这就是为什么`device = "cuda" if available else "cpu"`这行代码在人工智能工程中可见.

需要GPU的人会说,并包括Colab链接.

> 大部分课程都在CPU上运行.

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 自动选择 GPU 或 CPU
print(f"Using: {device}")
```

## 构建它:GPUvsCPU基准测试

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
> 矩阵乘法是神经网络训练中最核心的运算,GPU的加速效果直接决定了训练效率.

## 练习题

1. 运行上述基准,并比较CPU与GPU时间
   运行上基准测试,对比 CPU 和 GPU 的速度
2. 如果没有GPU,请在Google Colab上运行,然后比较
   如果没有本地GPU,在谷歌Colab上运行并对比
3. 检查您有多少GPU内存,并估计您可以安装的最大模型 (指公规则:fp16的每个参数为2字节)
   检查你的GPU 显存大小,估算能装下最大模型(经验法则:fp16 下每个参数占2 字节)

## 关键词 关键词

> **【拓展：2026 年 GPU 市场参考】**技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术技术$1600，个人学习首选）、A100（80GB，云端约 $据悉,这项计划是为了实现高效的发展,而这项计划是为了实现高效的发展.

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
