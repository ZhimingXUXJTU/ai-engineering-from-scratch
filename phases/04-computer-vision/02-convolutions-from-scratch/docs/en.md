# Convolutions from Scratch | 从零实现卷积

> A convolution is a tiny dense layer you slide across an image, sharing the same weights at every location.

> **【中文解读】** 卷积本质上是一个"滑动的小型全连接层"——用同一组权重在图像的每个位置计算点积。这给了我们两个关键特性：平移等变性（输入移动，输出跟着移动）和参数共享（同一个特征检测器在整个图像上复用）。CNN 之所以能统治计算机视觉十余年（2012-2020），正是因为卷积是图像数据的正确归纳偏置。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 3 (Deep Learning Core), Phase 4 Lesson 01 (Image Fundamentals)
**Time:** ~75 minutes

## Learning Objectives | 学习目标

- Implement 2D convolution from scratch using only NumPy, including the nested-loop version and a vectorised `im2col` version
  仅用 NumPy 从零实现 2D 卷积，包括嵌套循环版和向量化的 im2col 版
- Compute output spatial size for any combination of input size, kernel size, padding, and stride, and justify the `(H - K + 2P) / S + 1` formula
  计算任意输入大小、核大小、填充和步幅组合下的输出尺寸，理解公式 `(H - K + 2P) / S + 1`
- Hand-design kernels (edge, blur, sharpen, Sobel) and explain why each one produces the pattern of activations it does
  手动设计核（边缘检测、模糊、锐化、Sobel），解释每种核为何产生对应的激活模式
- Stack convolutions into a feature extractor and connect the depth-of-the-stack to the size of the receptive field
  将多个卷积层堆叠为特征提取器，理解堆叠深度与感受野大小的关系

## The Problem

A fully connected layer on a 224x224 RGB image would need 224 * 224 * 3 = 150,528 input weights per neuron. A single hidden layer with 1,000 units is already 150 million parameters — before you have learnt anything useful. Worse, that layer has no notion that a dog in the top-left and a dog in the bottom-right are the same pattern. It treats every pixel position as independent, which is exactly wrong for images: translating a cat by three pixels should not force the network to relearn the concept.

> **【中文解读】** 全连接层处理图像有两个致命问题：(1) 参数爆炸——224x224 图像的每个神经元就需要 15 万个权重；(2) 没有平移不变性——左上角的猫和右下角的猫被当作完全不同的模式。卷积通过参数共享（同一个核滑过全图）和局部连接（只看邻域）完美解决了这两个问题。

The two properties an image model needs are **translation equivariance** (the output shifts when the input shifts) and **parameter sharing** (the same feature detector runs everywhere). Dense layers give you neither. Convolution gives you both for free.

Convolution was not invented for deep learning. It is the same operation that powers JPEG compression, Gaussian blur in Photoshop, edge detection in industrial vision, and every audio filter ever shipped. The reason CNNs dominated ImageNet from 2012 to 2020 is that convolution is the correct prior for data where nearby values are related and the same pattern can appear anywhere.

> **【拓展：CNN 的工业应用】** 卷积并非深度学习发明的。JPEG 压缩、Photoshop 模糊、工业视觉边缘检测、音频滤波器都使用卷积。在 AI 领域，CNN 驱动了自动驾驶中的目标检测（YOLO）、医学影像分析、人脸识别（FaceNet）等核心应用。

## The Concept | 核心概念

### One kernel, sliding | 一个核，滑过全图

A 2D convolution takes a small weight matrix called the kernel (or filter), slides it across the input, and at each location computes the sum of element-wise products. That sum becomes one output pixel.

```mermaid
flowchart LR
    subgraph IN["Input (H x W)"]
        direction LR
        I1["5 x 5 image"]
    end
    subgraph K["Kernel (3 x 3)"]
        K1["learned<br/>weights"]
    end
    subgraph OUT["Output (H-2 x W-2)"]
        O1["3 x 3 map"]
    end
    I1 --> |"slide kernel<br/>compute dot product<br/>at each position"| O1
    K1 --> O1

    style IN fill:#dbeafe,stroke:#2563eb
    style K fill:#fef3c7,stroke:#d97706
    style OUT fill:#dcfce7,stroke:#16a34a
```

A concrete 3x3 example on a 5x5 input (no padding, stride 1):

```
Input X (5 x 5):                Kernel W (3 x 3):

  1  2  0  1  2                   1  0 -1
  0  1  3  1  0                   2  0 -2
  2  1  0  2  1                   1  0 -1
  1  0  2  1  3
  2  1  1  0  1

The kernel slides across every valid 3 x 3 window. Output Y is 3 x 3:

 Y[0,0] = sum( W * X[0:3, 0:3] )
 Y[0,1] = sum( W * X[0:3, 1:4] )
 Y[0,2] = sum( W * X[0:3, 2:5] )
 Y[1,0] = sum( W * X[1:4, 0:3] )
 ... and so on
```

That one formula — **shared weights, locality, sliding window** — is the entire idea. Everything else is bookkeeping.

> **【中文解读】** 卷积的全部思想浓缩为三点：共享权重（同一组参数在所有位置复用）、局部性（每次只看一个小窗口）、滑动窗口（依次遍历所有位置）。输出 Y 的每个元素就是核与输入窗口的点积。

### Output size formula | 输出尺寸公式

Given input spatial size `H`, kernel size `K`, padding `P`, stride `S`:

```
H_out = floor( (H - K + 2P) / S ) + 1
```

Memorise this. You will compute it dozens of times per architecture.

> **【中文解读】** 输出尺寸公式 `H_out = floor((H - K + 2P) / S) + 1` 是设计任何 CNN 架构时最常用的计算。"Same padding" 指让 H_out = H（当 S=1 时），此时 P = (K-1)/2。这就是为什么 3x3 核最流行——它是最小的奇数核，有明确的中心点。

| Scenario | H | K | P | S | H_out | 中文说明 |
|----------|---|---|---|---|-------|--------|
| Valid conv, no padding | 32 | 3 | 0 | 1 | 30 | 无填充，尺寸缩小 |
| Same conv (preserves size) | 32 | 3 | 1 | 1 | 32 | 同填充，保持尺寸 |
| Downsample by 2 | 32 | 3 | 1 | 2 | 16 | 步幅2，下采样 |
| Pool 2x2 | 32 | 2 | 0 | 2 | 16 | 池化层 |
| Large receptive field | 32 | 7 | 3 | 2 | 16 | 大感受野 |

"Same padding" means pick P so that H_out == H when S == 1. For odd K, that is P = (K - 1) / 2. That is why 3x3 kernels dominate — they are the smallest odd kernel that still has a centre.

### Padding | 填充

Without padding, every convolution shrinks the feature map. Stack 20 of them and your 224x224 image becomes 184x184, which wastes compute on the border and complicates residual connections that need matching shapes.

```
Zero padding (P = 1) on a 5 x 5 input:

  0  0  0  0  0  0  0
  0  1  2  0  1  2  0
  0  0  1  3  1  0  0
  0  2  1  0  2  1  0       Now the kernel can centre on pixel
  0  1  0  2  1  3  0       (0, 0) and still have three rows and
  0  2  1  1  0  1  0       three columns of values to multiply.
  0  0  0  0  0  0  0
```

Modes you meet in practice: `zero` (most common), `reflect` (mirror the edge, avoids hard borders in generative models), `replicate` (copy the edge), `circular` (wrap around, used in toroidal problems).

### Stride | 步幅

Stride is the step size of the slide. `stride=1` is the default. `stride=2` halves the spatial dimensions and is the classic way to downsample inside a CNN without a separate pooling layer — every modern architecture (ResNet, ConvNeXt, MobileNet) uses strided convs in place of max-pool somewhere.

```
Stride 1 on a 5 x 5 input, 3 x 3 kernel:

  starts: (0,0) (0,1) (0,2)        -> output row 0
          (1,0) (1,1) (1,2)        -> output row 1
          (2,0) (2,1) (2,2)        -> output row 2

  Output: 3 x 3

Stride 2 on the same input:

  starts: (0,0) (0,2)              -> output row 0
          (2,0) (2,2)              -> output row 1

  Output: 2 x 2
```

### Multiple input channels | 多输入通道

Real images have three channels. A 3x3 convolution on an RGB input is actually a 3x3x3 volume: one 3x3 slice per input channel. At each spatial position, you multiply and sum across all three slices and add a bias.

```
Input:   (C_in,  H,  W)        3 x 5 x 5
Kernel:  (C_in,  K,  K)        3 x 3 x 3 (one kernel)
Output:  (1,     H', W')       2D map

For a layer that produces C_out output channels, you stack C_out kernels:

Weight:  (C_out, C_in, K, K)   e.g. 64 x 3 x 3 x 3
Output:  (C_out, H', W')       64 x 3 x 3

Parameter count: C_out * C_in * K * K + C_out   (the + C_out is biases)
```

That last line is the one you will calculate when planning a model. A 64-channel 3x3 conv on a 3-channel input has `64 * 3 * 3 * 3 + 64 = 1,792` parameters. Cheap.

> **【中文解读】** 多通道卷积的参数计算：参数量 = C_out × C_in × K × K + C_out（偏置）。一个 3 输入通道、64 输出通道的 3x3 卷积只需 1,792 个参数，远少于全连接层。这体现了卷积的参数效率。

### The im2col trick | im2col 技巧

Nested loops are easy to read but slow. GPUs want big matrix multiplies. The trick: flatten every receptive-field window of the input into one column of a big matrix, flatten the kernel into a row, and the whole convolution becomes a single matmul.

```mermaid
flowchart LR
    X["Input<br/>(C_in, H, W)"] --> IM2COL["im2col<br/>(extract patches)"]
    IM2COL --> COLS["Cols matrix<br/>(C_in * K * K, H_out * W_out)"]
    W["Weight<br/>(C_out, C_in, K, K)"] --> FLAT["Flatten<br/>(C_out, C_in * K * K)"]
    FLAT --> MM["matmul"]
    COLS --> MM
    MM --> OUT["Output<br/>(C_out, H_out * W_out)<br/>reshape to (C_out, H_out, W_out)"]

    style X fill:#dbeafe,stroke:#2563eb
    style W fill:#fef3c7,stroke:#d97706
    style OUT fill:#dcfce7,stroke:#16a34a
```

Every production conv implementation is some variant of this plus cache-tiling tricks (direct conv, Winograd, FFT conv for large kernels). Understand im2col and you understand the core.

> **【拓展：GPU 加速卷积】** 所有 GPU 上的卷积实现（cuDNN）都是 im2col 的变体，加上缓存分块优化（直接卷积、Winograd、FFT 卷积）。理解 im2col 就理解了深度学习框架中卷积加速的核心原理。

### Receptive field | 感受野

A single 3x3 conv looks at 9 input pixels. Stack two 3x3 convs and a neuron in the second layer looks at 5x5 input pixels. Three 3x3 convs give 7x7. In general:

```
RF after L stacked K x K convs (stride 1) = 1 + L * (K - 1)

With strides:   RF grows multiplicatively with stride along each layer.
```

The entire reason "3x3 all the way down" works (VGG, ResNet, ConvNeXt) is that two 3x3 convs see the same input area as one 5x5 conv but with fewer parameters and an extra non-linearity in between.

> **【中文解读】** 堆叠 L 层 K×K 卷积（步幅为1）的感受野 = 1 + L × (K-1)。这就是 VGG、ResNet 等网络 "全用 3x3" 的原因：两个 3x3 卷积的感受野等于一个 5x5，但参数更少，中间还多了一层非线性激活。

## Build It | 动手实践

### Step 1: Pad an array | 填充数组

Start with the smallest primitive: a function that pads with zeros around an H x W array.

```python
import numpy as np

def pad2d(x, p):
    if p == 0:
        return x
    h, w = x.shape[-2:]
    out = np.zeros(x.shape[:-2] + (h + 2 * p, w + 2 * p), dtype=x.dtype)
    out[..., p:p + h, p:p + w] = x
    return out

x = np.arange(9).reshape(3, 3)
print(x)
print()
print(pad2d(x, 1))
```

The trailing-axes trick `x.shape[:-2]` means the same function works on `(H, W)`, `(C, H, W)`, or `(N, C, H, W)` without modification.

### Step 2: 2D convolution with nested loops | 嵌套循环实现 2D 卷积

The reference implementation — slow, but unambiguous. This is what `torch.nn.functional.conv2d` does in principle.

```python
def conv2d_naive(x, w, b=None, stride=1, padding=0):
    c_in, h, w_in = x.shape       # 输入：通道数、高、宽
    c_out, c_in_w, kh, kw = w.shape  # 权重：输出通道、输入通道、核高、核宽
    assert c_in == c_in_w          # 输入通道数必须匹配

    x_pad = pad2d(x, padding)     # 填充输入
    h_out = (h + 2 * padding - kh) // stride + 1  # 输出高度
    w_out = (w_in + 2 * padding - kw) // stride + 1  # 输出宽度

    out = np.zeros((c_out, h_out, w_out), dtype=np.float32)
    for oc in range(c_out):               # 遍历每个输出通道
        for i in range(h_out):            # 遍历输出高度
            for j in range(w_out):        # 遍历输出宽度
                hs = i * stride           # 输入中的起始行
                ws = j * stride           # 输入中的起始列
                patch = x_pad[:, hs:hs + kh, ws:ws + kw]  # 提取感受野窗口
                out[oc, i, j] = np.sum(patch * w[oc])      # 点积求和
        if b is not None:
            out[oc] += b[oc]              # 加偏置
    return out
```

Four nested loops (output channel, row, column, plus the implicit sum over C_in, kh, kw). This is the ground truth you will check every faster implementation against.

### Step 3: Verify with a hand-designed kernel | 用手工设计的核验证

Build a vertical Sobel kernel, apply it to a synthetic step image, and watch the vertical edge light up.

```python
def synthetic_step_image():
    img = np.zeros((1, 16, 16), dtype=np.float32)
    img[:, :, 8:] = 1.0
    return img

sobel_x = np.array([
    [[-1, 0, 1],
     [-2, 0, 2],
     [-1, 0, 1]]
], dtype=np.float32)[None]

x = synthetic_step_image()
y = conv2d_naive(x, sobel_x, padding=1)
print(y[0].round(1))
```

Expect large positive values on column 7 (left-to-right brightness increase) and zeros everywhere else. That single print is your sanity check that the math is right.

### Step 4: im2col | im2col 矩阵展开

Convert every kernel-sized window in the input into a column of a matrix. For `C_in=3, K=3`, each column is 27 numbers.

```python
def im2col(x, kh, kw, stride=1, padding=0):
    c_in, h, w = x.shape
    x_pad = pad2d(x, padding)
    h_out = (h + 2 * padding - kh) // stride + 1
    w_out = (w + 2 * padding - kw) // stride + 1

    cols = np.zeros((c_in * kh * kw, h_out * w_out), dtype=x.dtype)
    col = 0
    for i in range(h_out):
        for j in range(w_out):
            hs = i * stride
            ws = j * stride
            patch = x_pad[:, hs:hs + kh, ws:ws + kw]
            cols[:, col] = patch.reshape(-1)
            col += 1
    return cols, h_out, w_out
```

It is still a Python loop, but now the heavy lifting will be a single vectorised matmul.

### Step 5: Fast conv via im2col + matmul | 用 im2col + 矩阵乘法加速卷积

Replace the quadruple loop with one matrix multiplication.

```python
def conv2d_im2col(x, w, b=None, stride=1, padding=0):
    c_out, c_in, kh, kw = w.shape
    cols, h_out, w_out = im2col(x, kh, kw, stride, padding)
    w_flat = w.reshape(c_out, -1)
    out = w_flat @ cols
    if b is not None:
        out += b[:, None]
    return out.reshape(c_out, h_out, w_out)
```

Correctness check: run both implementations and compare.

```python
rng = np.random.default_rng(0)
x = rng.normal(0, 1, (3, 16, 16)).astype(np.float32)
w = rng.normal(0, 1, (8, 3, 3, 3)).astype(np.float32)
b = rng.normal(0, 1, (8,)).astype(np.float32)

y_naive = conv2d_naive(x, w, b, padding=1)
y_im2col = conv2d_im2col(x, w, b, padding=1)

print(f"max abs diff: {np.max(np.abs(y_naive - y_im2col)):.2e}")
```

`max abs diff` should be around `1e-5` — the difference is floating-point accumulation order, not a bug.

### Step 6: A bank of hand-designed kernels | 手工设计的一组经典核

Five filters that show what a single conv layer can express before any training.

```python
KERNELS = {
    "identity": np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float32),
    "blur_3x3": np.ones((3, 3), dtype=np.float32) / 9.0,
    "sharpen": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32),
    "sobel_x": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32),
    "sobel_y": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32),
}

def apply_kernel(img2d, kernel):
    x = img2d[None].astype(np.float32)
    w = kernel[None, None]
    return conv2d_im2col(x, w, padding=1)[0]
```

Applied to any grayscale image, blur softens, sharpen crisps up edges, Sobel-x lights up vertical edges, Sobel-y lights up horizontal edges. These are exactly the patterns that the *first* trained conv layer in AlexNet and VGG ended up learning — because a good image model needs edge and blob detectors no matter what task comes later.

> **【拓展：经典卷积核与 CNN 学习】** AlexNet、VGG 等网络的第一个卷积层学到的特征几乎总是边缘检测器和颜色斑点检测器——与这些手工设计的核高度相似。这说明无论任务是什么，底层视觉特征（边缘、纹理）是通用的。

## Use It | 实际应用

PyTorch's `nn.Conv2d` wraps the same operation with autograd, CUDA kernels, and cuDNN optimisation. Shape semantics are identical.

```python
import torch
import torch.nn as nn

conv = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, stride=1, padding=1)
print(conv)
print(f"weight shape: {tuple(conv.weight.shape)}   # (C_out, C_in, K, K)")
print(f"bias shape:   {tuple(conv.bias.shape)}")
print(f"param count:  {sum(p.numel() for p in conv.parameters())}")

x = torch.randn(8, 3, 224, 224)
y = conv(x)
print(f"\ninput  shape: {tuple(x.shape)}")
print(f"output shape: {tuple(y.shape)}")
```

Swap `padding=1` for `padding=0` and the output drops to 222x222. Swap `stride=1` for `stride=2` and it drops to 112x112. Same formula you memorised above.

## Ship It | 交付产出

This lesson produces:

- `outputs/prompt-cnn-architect.md` — a prompt that, given input size, parameter budget, and target receptive field, designs a stack of `Conv2d` layers with the right K/S/P at every step.
- `outputs/skill-conv-shape-calculator.md` — a skill that walks a network spec layer by layer and returns the output shape, receptive field, and parameter count for every block.

## Exercises | 练习题

1. **(Easy | 简单)** Given a 128x128 grayscale input and a stack of `[Conv3x3(s=1,p=1), Conv3x3(s=2,p=1), Conv3x3(s=1,p=1), Conv3x3(s=2,p=1)]`, compute the output spatial size and the receptive field at each layer by hand. Verify with a PyTorch `nn.Sequential` of dummy convs.
   手动计算四层卷积的输出尺寸和感受野，用 PyTorch 验证。

2. **(Medium | 中等)** Extend `conv2d_naive` and `conv2d_im2col` to accept a `groups` argument. Show that `groups=C_in=C_out` reproduces a depthwise convolution and that its parameter count is `C * K * K` instead of `C * C * K * K`.
   扩展卷积函数支持 groups 参数，验证深度卷积的参数量从 C×C×K×K 降为 C×K×K。

3. **(Hard | 困难)** Implement the backward pass of `conv2d_im2col` by hand: given the gradient of the output, compute the gradient of `x` and `w`. Verify against `torch.autograd.grad` on the same inputs and weights. The trick: the gradient of im2col is `col2im`, and it has to accumulate overlapping windows.
   手动实现 im2col 卷积的反向传播，用 torch.autograd.grad 验证。关键：im2col 的梯度是 col2im，需要累加重叠窗口。

## Key Terms | 关键术语

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Convolution | "Sliding a filter" | A learnable dot product applied at every spatial location with shared weights; mathematically a cross-correlation, but everyone calls it convolution | 卷积：在所有空间位置用共享权重做可学习的点积 |
| Kernel / filter | "The feature detector" | A small weight tensor of shape (C_in, K, K) whose dot product with a window of input produces one output pixel | 核/滤波器：小型权重张量，与输入窗口做点积产生一个输出像素 |
| Stride | "How far you jump" | The step size between consecutive kernel placements; stride 2 halves each spatial dimension | 步幅：核每次滑动的步长，步幅2将空间维度减半 |
| Padding | "Zeros on the edges" | Extra values added around the input so the kernel can centre on border pixels; `same` padding keeps output size equal to input size | 填充：在输入边缘补零，使核能对齐边界像素 |
| Receptive field | "How much the neuron sees" | The patch of original input that a given output activation depends on, growing with depth and stride | 感受野：一个输出激活值所依赖的原始输入区域 |
| im2col | "The GEMM trick" | Rearranging every receptive window into columns so convolution becomes one big matrix multiply — the core of every fast conv kernel | im2col：将感受野窗口重排为列，使卷积变成矩阵乘法 |
| Depthwise conv | "One kernel per channel" | A conv with `groups == C_in`, computing each output channel from only its matching input channel; the backbone of MobileNet and ConvNeXt | 深度卷积：每通道独立卷积，MobileNet/ConvNeXt 的核心组件 |
| Translation equivariance | "Shift in, shift out" | Property that shifting the input by k pixels shifts the output by k pixels; comes for free with shared weights | 平移等变性：输入平移k像素，输出也平移k像素 |

## Further Reading | 延伸阅读

- [A guide to convolution arithmetic for deep learning (Dumoulin & Visin, 2016)](https://arxiv.org/abs/1603.07285) — the definitive diagrams of padding/stride/dilation that every course quietly copies
- [CS231n: Convolutional Neural Networks for Visual Recognition](https://cs231n.github.io/convolutional-networks/) — the canonical lecture notes, including the original im2col explanation
- [The Annotated ConvNet (fast.ai)](https://nbviewer.org/github/fastai/fastbook/blob/master/13_convolutions.ipynb) — a notebook that walks from manual convolution to a trained digit classifier
- [Receptive Field Arithmetic for CNNs (Dang Ha The Hien)](https://distill.pub/2019/computing-receptive-fields/) — the paper-quality interactive explainer of receptive field calculations
