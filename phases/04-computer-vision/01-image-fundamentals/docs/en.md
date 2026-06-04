# Image Fundamentals — Pixels, Channels, Color Spaces | 图像基础 — 像素、通道与色彩空间

> An image is a tensor of light samples. Every vision model you will ever use starts from this one fact.

> **【中文解读】** 图像本质上是一组光线采样值的张量（多维数组）。无论是手机拍照、自动驾驶还是 GPT-4V，所有视觉模型都从这个基本事实出发。理解像素、通道和数据格式是避免 "模型吃错数据" 这类隐蔽 bug 的关键。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 1 Lesson 12 (Tensor Operations), Phase 3 Lesson 11 (Intro to PyTorch)
**Time:** ~45 minutes

## Learning Objectives | 学习目标

- Explain how a continuous scene gets discretized into pixels and why sampling/quantization decisions set the ceiling on every downstream model
  解释连续场景如何被离散化为像素，以及为什么采样/量化决策决定了所有下游模型的上限
- Read, slice, and inspect images as NumPy arrays and switch fluently between HWC and CHW layouts
  读取、切片、检查图像的 NumPy 数组表示，并在 HWC 和 CHW 布局之间自如切换
- Convert between RGB, grayscale, HSV, and YCbCr and justify why each color space exists
  在 RGB、灰度、HSV 和 YCbCr 之间转换，并理解每种色彩空间存在的原因
- Apply pixel-level preprocessing (normalize, standardize, resize, channel-first) exactly as torchvision expects it
  精确按照 torchvision 的期望进行像素级预处理（归一化、标准化、缩放、通道前置）

> **【中文解读】** 学习目标列出了完成本课后应该掌握的核心能力。建议在开始学习前先浏览目标，学完后对照检查是否达成。


## The Problem | 问题引入

Every paper you will read, every pretrained weight you will download, every vision API you will call assumes a specific encoding of the input. Pass a `uint8` image where the model wants `float32` and it will still run — and silently produce garbage. Feed BGR to a network trained on RGB and accuracy collapses by ten points. Hand a model channels-last input when it expects channels-first and the first conv layer treats height as a feature channel. None of this throws an error. It just ruins your metrics and you spend a week hunting for a bug that lives in how you loaded the file.

> **【中文解读】** 这是计算机视觉工程中最常见的 "隐性 bug" 来源：数据格式不匹配。模型不会报错，但结果完全错误。比如把 BGR（OpenCV 默认）当作 RGB（PyTorch 默认）喂给模型，准确率可能暴跌 10 个百分点。在实际 AI 工程中，这类问题可能导致自动驾驶系统误判红绿灯颜色。

A convolution is not complicated once you know what it is sliding over. The hard part is that "an image" means different things to a camera, a JPEG decoder, PIL, OpenCV, torchvision, and a CUDA kernel. Each stack has its own axis order, byte range, and channel convention. A vision engineer who cannot keep these straight ships broken pipelines.

This lesson fixes the foundation so the rest of the phase can build on it. By the end you will know what a pixel is, why there are three numbers per pixel instead of one, what "normalize with ImageNet stats" actually does, and how to move between the two or three layouts that every other lesson in this phase will assume.


> **【拓展：数据标注与质量】** 视觉任务的效果高度依赖标注数据质量。Label Studio、CVAT 是主流标注工具。在工业场景中，主动学习（Active Learning）可以减少标注成本：模型对不确定的样本请求人工标注，确定性的样本自动标注。

## The Concept | 核心概念

### The full preprocessing pipeline at a glance | 预处理流水线全景

Every production vision system is the same sequence of reversible transforms. Get one step wrong and the model sees a different input than it was trained on.

```mermaid
flowchart LR
    A["Image file<br/>(JPEG/PNG)"] --> B["Decode<br/>uint8 HWC"]
    B --> C["Convert<br/>colorspace<br/>(RGB/BGR/YCbCr)"]
    C --> D["Resize<br/>shorter side"]
    D --> E["Center crop<br/>model size"]
    E --> F["Divide by 255<br/>float32 [0,1]"]
    F --> G["Subtract mean<br/>Divide by std"]
    G --> H["Transpose<br/>HWC → CHW"]
    H --> I["Batch<br/>CHW → NCHW"]
    I --> J["Model"]

    style A fill:#fef3c7,stroke:#d97706
    style J fill:#ddd6fe,stroke:#7c3aed
    style G fill:#fecaca,stroke:#dc2626
    style H fill:#bfdbfe,stroke:#2563eb
```

The two red and blue boxes are where 80% of silent failures live: missing standardization and wrong layout.

> **【中文解读】** 80% 的隐性错误集中在两个环节：(1) 没有做标准化（减均值除标准差），(2) 数据布局搞错了（HWC vs CHW）。在实际项目中，用 torchvision.transforms.Compose 按顺序组合这些步骤是最可靠的做法。

### A pixel is a sample, not a square | 像素是采样点，不是色块

A camera sensor counts photons that land on a grid of tiny detectors. Each detector integrates light for a fraction of a second and emits a voltage proportional to how many photons hit it. The sensor then discretizes that voltage into an integer. One detector becomes one pixel.

```
Continuous scene                 Sensor grid                     Digital image
(infinite detail)                (H x W detectors)               (H x W integers)

    ~~~~~                        +--+--+--+--+--+                 210 198 180 155 120
   ~   ~   ~                     |  |  |  |  |  |                 205 195 178 152 118
  ~ light ~      ---->           +--+--+--+--+--+     ---->       200 190 175 150 115
   ~~~~~                         |  |  |  |  |  |                 195 185 170 148 112
                                 +--+--+--+--+--+                 188 180 165 145 108
```

Two choices happen at this step and they fix the ceiling on everything downstream:

- **Spatial sampling** decides how many detectors per degree of the scene. Too few, and edges become jagged (aliasing). Too many, and storage and compute explode.
- **Intensity quantization** decides how finely the voltage is bucketed. 8 bits gives 256 levels and is standard for display. 10, 12, 16 bits give smoother gradients and matter for medical imaging, HDR, and raw sensor pipelines.

A pixel is not a coloured square with area. It is a single measurement. When you resize or rotate, you are resampling that measurement grid.

> **【中文解读】** 像素不是一个小方块，而是一个采样点——传感器在某个空间位置测得的一个数值。缩放或旋转图像时，实际上是对采样网格进行重采样。这个概念在医学影像（如 CT、MRI）和高动态范围（HDR）成像中尤为重要。

### Why three channels | 为什么是三个通道

One detector counts photons across the whole visible spectrum — that is grayscale. To get colour, the sensor covers the grid with a mosaic of red, green, and blue filters. After demosaicing, every spatial location has three integers: the response of the red-filtered detector, green-filtered, and blue-filtered nearby. Those three integers are a pixel's RGB triplet.

```
One pixel in memory:

    (R, G, B) = (210, 140, 30)   <- reddish-orange

An H x W RGB image:

    shape (H, W, 3)     stored as   H rows of W pixels of 3 values
                                    each in [0, 255] for uint8
```

Three is not magic. Depth cameras add a Z channel. Satellites add infrared and ultraviolet bands. Medical scans often have one channel (X-ray, CT) or many (hyperspectral). The number of channels is the last axis; conv layers learn to mix across it.

> **【拓展：多通道图像】** 卫星遥感图像通常有红外、紫外等额外波段（多光谱/高光谱）；医疗 CT 只有一个通道；深度摄像头（如 Kinect、iPhone LiDAR）会增加深度通道 D。这些多通道图像在农业监测、医学诊断和自动驾驶中有广泛应用。

### Two layout conventions: HWC and CHW | 两种布局约定：HWC 和 CHW

Same tensor, two orderings. Every library picks one.

```
HWC (height, width, channels)           CHW (channels, height, width)

   W ->                                    H ->
  +-----+-----+-----+                     +-----+-----+
H |R G B|R G B|R G B|                   C |R R R R R R|
| +-----+-----+-----+                   | +-----+-----+
v |R G B|R G B|R G B|                   v |G G G G G G|
  +-----+-----+-----+                     +-----+-----+
                                          |B B B B B B|
                                          +-----+-----+

   PIL, OpenCV, matplotlib,              PyTorch, most deep learning
   almost every image file on disk       frameworks, cuDNN kernels
```

CHW exists because convolution kernels slide across H and W. Keeping the channel axis first means each kernel sees a contiguous 2D plane per channel, which vectorizes cleanly. Disk formats keep HWC because that matches how scanlines come out of a sensor.

> **【中文解读】** HWC（高×宽×通道）是 PIL、OpenCV 等库的默认格式，也是图像文件在磁盘上的存储方式。CHW（通道×高×宽）是 PyTorch 和 GPU 计算（cuDNN）使用的格式，因为卷积核在 H 和 W 上滑动时，通道前置使得每个核看到的是连续的 2D 平面，计算效率更高。两者之间的转换是每天都要写无数次的操作。

The one-line conversion you will type a thousand times:

```
img_chw = img_hwc.transpose(2, 0, 1)      # NumPy
img_chw = img_hwc.permute(2, 0, 1)        # PyTorch tensor
```

Memory layout, visualised:

```mermaid
flowchart TB
    subgraph HWC["HWC — pixels stored interleaved (PIL, OpenCV, JPEG)"]
        H1["row 0: R G B | R G B | R G B ..."]
        H2["row 1: R G B | R G B | R G B ..."]
        H3["row 2: R G B | R G B | R G B ..."]
    end
    subgraph CHW["CHW — channels stored as stacked planes (PyTorch, cuDNN)"]
        C1["plane R: entire H x W of red values"]
        C2["plane G: entire H x W of green values"]
        C3["plane B: entire H x W of blue values"]
    end
    HWC -->|"transpose(2, 0, 1)"| CHW
    CHW -->|"transpose(1, 2, 0)"| HWC
```

### Byte ranges and dtype | 字节范围与数据类型

Three conventions dominate:

| Convention | dtype | Range | Where you see it |
|------------|-------|-------|------------------|
| Raw | `uint8` | [0, 255] | Files on disk, PIL, OpenCV output |
| Normalized | `float32` | [0.0, 1.0] | After `img.astype('float32') / 255` |
| Standardized | `float32` | roughly [-2, +2] | After subtracting mean and dividing by std |

Convolutional networks were trained on standardized inputs. ImageNet stats `mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]` are the arithmetic mean and standard deviation of the three channels over the full ImageNet training set, computed on [0, 1] normalized pixels. Feeding raw `uint8` into a model that expects standardized float is the single most common silent failure in applied vision.

> **【中文解读】** 三种数据范围：(1) uint8 [0,255] — 文件/PIL/OpenCV 的原始输出；(2) float32 [0,1] — 归一化后；(3) float32 ≈[-2,+2] — ImageNet 标准化后。把 uint8 直接喂给期望标准化输入的模型，是最常见的 "静默失败"。ImageNet 的均值和标准差是整个训练集统计出来的，几乎所有预训练模型都用这组数值。

### Color spaces and why they exist | 色彩空间及其存在的理由

RGB is the capture format but it is not always the most useful representation for a model.

```
 RGB               HSV                       YCbCr / YUV

 R red             H hue (angle 0-360)       Y luminance (brightness)
 G green           S saturation (0-1)        Cb chroma blue-yellow
 B blue            V value/brightness (0-1)  Cr chroma red-green

 Linear to         Separates color from      Separates brightness from
 sensor output     brightness. Useful for    color. JPEG and most video
                   color thresholding, UI    codecs compress the chroma
                   sliders, simple filters   channels harder because the
                                             human eye is less sensitive
                                             to chroma detail than to Y.
```

For most modern CNNs you feed RGB. You meet other spaces when:

- **HSV** — classical CV code, color-based segmentation, white-balancing.
- **YCbCr** — reading JPEG internals, video pipelines, super-resolution models that operate on Y only.
- **Grayscale** — OCR, document models, any case where color is nuisance variable rather than signal.

Grayscale from RGB is a weighted sum, not an average, because the human eye is more sensitive to green than to red or blue:

```
Y = 0.299 R + 0.587 G + 0.114 B       (ITU-R BT.601, the classic weights)
```

### Aspect ratio, resizing, and interpolation | 宽高比、缩放与插值

Every model has a fixed input size (224x224 for most ImageNet classifiers, 384x384 or 512x512 for modern detectors). Your images rarely match. The three resize choices that matter:

- **Resize shorter side, then center crop** — the standard ImageNet recipe. Preserves aspect ratio, throws away a strip of edge pixels.
- **Resize and pad** — preserves aspect ratio and every pixel, adds black bars. Standard for detection and OCR.
- **Resize directly to target** — stretches the image. Cheap, distorts geometry, fine for many classification tasks.

The interpolation method decides how intermediate pixels are computed when the new grid does not align with the old one:

```
Nearest neighbour     fastest, blocky, only choice for masks/labels
Bilinear              fast, smooth, default for most image resizing
Bicubic               slower, sharper on upscaling
Lanczos               slowest, best quality, used for final display
```

Rule of thumb: bilinear for training, bicubic or lanczos for assets you will look at, nearest for anything containing integer class IDs.

> **【中文解读】** 缩放时的插值方法选择：最近邻（nearest）速度最快但会产生锯齿，只用于掩码/标签图；双线性（bilinear）又快又平滑，是训练时的默认选择；双三次（bicubic）更慢但放大时更清晰；Lanczos 最慢但质量最好。经验法则：训练用 bilinear，展示用 bicubic/lanczos，标签用 nearest。

> **【拓展：工业部署中的视觉系统】** 在实际工业部署中，视觉模型需要考虑推理延迟、模型大小、边缘设备适配等问题。TensorRT、ONNX Runtime、OpenVINO 是常用的推理加速工具。自动驾驶系统（如 Tesla FSD）通常在车载芯片上实时运行多个视觉模型。


## Build It | 动手实践

### Step 1: Load an image and inspect its shape | 加载图像并检查其形状

Use Pillow to load any JPEG or PNG, convert to NumPy, and print what you got. For a deterministic example that runs offline, synthesize one.

```python
import numpy as np
from PIL import Image

def synthetic_rgb(h=128, w=192, seed=0):
    rng = np.random.default_rng(seed)
    yy, xx = np.meshgrid(np.linspace(0, 1, h), np.linspace(0, 1, w), indexing="ij")
    r = (np.sin(xx * 6) * 0.5 + 0.5) * 255  # 红色通道：正弦波图案
    g = yy * 255                               # 绿色通道：垂直渐变
    b = (1 - yy) * xx * 255                    # 蓝色通道：对角渐变
    rgb = np.stack([r, g, b], axis=-1) + rng.normal(0, 6, (h, w, 3))  # 叠加高斯噪声
    return np.clip(rgb, 0, 255).astype(np.uint8)  # 裁剪到 [0,255] 并转为 uint8

arr = synthetic_rgb()
# 也可以从磁盘加载：arr = np.asarray(Image.open("your_image.jpg").convert("RGB"))

print(f"type:   {type(arr).__name__}")       # 类型
print(f"dtype:  {arr.dtype}")                 # 数据类型：uint8
print(f"shape:  {arr.shape}     # (H, W, C)")  # 形状：(高, 宽, 通道)
print(f"min:    {arr.min()}")                 # 最小值
print(f"max:    {arr.max()}")                 # 最大值
print(f"pixel at (0, 0): {arr[0, 0]}")       # 左上角像素的 RGB 值
```

Expected output: `shape: (H, W, 3)`, `dtype: uint8`, range `[0, 255]`. That is the canonical on-disk representation whether the bytes came from a camera, a JPEG decoder, or a synthetic generator.

### Step 2: Split channels and re-order layout | 分离通道并重排布局

Pull out R, G, B separately, then convert from HWC to CHW for PyTorch.

```python
R = arr[:, :, 0]   # 提取红色通道
G = arr[:, :, 1]   # 提取绿色通道
B = arr[:, :, 2]   # 提取蓝色通道
print(f"R shape: {R.shape}, mean: {R.mean():.1f}")
print(f"G shape: {G.shape}, mean: {G.mean():.1f}")
print(f"B shape: {B.shape}, mean: {B.mean():.1f}")

arr_chw = arr.transpose(2, 0, 1)  # HWC → CHW 布局转换
print(f"\nHWC shape: {arr.shape}")
print(f"CHW shape: {arr_chw.shape}")
```

Three grayscale planes, one per channel. CHW just reorders the axes; no data copy is strictly required when the memory layout allows it.

### Step 3: Grayscale and HSV conversions | 灰度与 HSV 转换

Weighted-sum grayscale, then a manual RGB-to-HSV.

```python
def rgb_to_grayscale(rgb):
    weights = np.array([0.299, 0.587, 0.114], dtype=np.float32)  # ITU-R BT.601 亮度权重
    return (rgb.astype(np.float32) @ weights).astype(np.uint8)    # 加权求和转灰度

def rgb_to_hsv(rgb):
    rgb_f = rgb.astype(np.float32) / 255.0  # 先归一化到 [0,1]
    r, g, b = rgb_f[..., 0], rgb_f[..., 1], rgb_f[..., 2]
    cmax = np.max(rgb_f, axis=-1)           # 通道最大值
    cmin = np.min(rgb_f, axis=-1)           # 通道最小值
    delta = cmax - cmin                     # 色差

    h = np.zeros_like(cmax)
    mask = delta > 0                        # 只在有色彩差异时计算色相
    rmax = mask & (cmax == r)
    gmax = mask & (cmax == g)
    bmax = mask & (cmax == b)
    h[rmax] = ((g[rmax] - b[rmax]) / delta[rmax]) % 6
    h[gmax] = ((b[gmax] - r[gmax]) / delta[gmax]) + 2
    h[bmax] = ((r[bmax] - g[bmax]) / delta[bmax]) + 4
    h = h * 60.0                            # 转换为角度 [0, 360]

    s = np.where(cmax > 0, delta / cmax, 0)  # 饱和度
    v = cmax                                   # 明度
    return np.stack([h, s, v], axis=-1)

gray = rgb_to_grayscale(arr)
hsv = rgb_to_hsv(arr)
print(f"gray shape: {gray.shape}, range: [{gray.min()}, {gray.max()}]")
print(f"hsv   shape: {hsv.shape}")
print(f"hue range: [{hsv[..., 0].min():.1f}, {hsv[..., 0].max():.1f}] degrees")
print(f"sat range: [{hsv[..., 1].min():.2f}, {hsv[..., 1].max():.2f}]")
print(f"val range: [{hsv[..., 2].min():.2f}, {hsv[..., 2].max():.2f}]")
```

Hue comes out in degrees, saturation and value in [0, 1]. That matches the OpenCV `hsv_full` convention.

### Step 4: Normalize, standardize, and reverse it | 归一化、标准化与逆变换

Go from raw bytes to the exact tensor a pretrained ImageNet model expects, then back.

```python
mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)  # ImageNet 均值
std = np.array([0.229, 0.224, 0.225], dtype=np.float32)    # ImageNet 标准差

def preprocess_imagenet(rgb_uint8):
    x = rgb_uint8.astype(np.float32) / 255.0  # uint8 [0,255] → float32 [0,1]
    x = (x - mean) / std                      # 标准化：减均值，除标准差
    x = x.transpose(2, 0, 1)                  # HWC → CHW（PyTorch 格式）
    return x

def deprocess_imagenet(chw_float32):
    x = chw_float32.transpose(1, 2, 0)        # CHW → HWC（还原布局）
    x = x * std + mean                         # 逆标准化：乘标准差，加均值
    x = np.clip(x * 255.0, 0, 255).astype(np.uint8)  # [0,1] → [0,255] uint8
    return x

x = preprocess_imagenet(arr)
print(f"preprocessed shape: {x.shape}     # (C, H, W)")
print(f"preprocessed dtype: {x.dtype}")
print(f"preprocessed mean per channel:  {x.mean(axis=(1, 2)).round(3)}")
print(f"preprocessed std  per channel:  {x.std(axis=(1, 2)).round(3)}")

roundtrip = deprocess_imagenet(x)
max_diff = np.abs(roundtrip.astype(int) - arr.astype(int)).max()
print(f"roundtrip max pixel diff: {max_diff}    # should be 0 or 1")
```

Per-channel mean should be close to zero, std close to one. The preprocess/deprocess pair is exactly what every torchvision `transforms.Normalize` call is doing under the hood.

### Step 5: Resize with three interpolation methods | 三种插值方法对比

Compare nearest, bilinear, and bicubic on an upscale so the difference is visible.

```python
target = (arr.shape[0] * 3, arr.shape[1] * 3)

nearest = np.asarray(Image.fromarray(arr).resize(target[::-1], Image.NEAREST))
bilinear = np.asarray(Image.fromarray(arr).resize(target[::-1], Image.BILINEAR))
bicubic = np.asarray(Image.fromarray(arr).resize(target[::-1], Image.BICUBIC))

def local_roughness(x):
    gy = np.diff(x.astype(float), axis=0)
    gx = np.diff(x.astype(float), axis=1)
    return float(np.abs(gy).mean() + np.abs(gx).mean())

for name, out in [("nearest", nearest), ("bilinear", bilinear), ("bicubic", bicubic)]:
    print(f"{name:>8}  shape={out.shape}  roughness={local_roughness(out):6.2f}")
```

Nearest scores highest on roughness because it keeps hard edges. Bilinear is the smoothest. Bicubic sits in between, preserving perceived sharpness without the stair-step artifacts.



## Use It | 实际应用

`torchvision.transforms` bundles everything above into a single composable pipeline. The code below reproduces exactly what `preprocess_imagenet` does, plus resize and crop.

> **【拓展：torchvision transforms】** 在实际 AI 工程中，几乎所有使用 PyTorch 预训练模型的项目都用 `transforms.Compose` 来构建预处理流水线。Stable Diffusion、YOLO、CLIP 等模型各有自己的预处理要求，理解这些基础步骤是正确使用任何视觉模型的前提。

```python
import torch
from torchvision import transforms
from PIL import Image

img = Image.fromarray(synthetic_rgb(256, 256))

pipeline = transforms.Compose([
    transforms.Resize(256),                    # 缩放短边到 256
    transforms.CenterCrop(224),                # 中心裁剪到 224x224
    transforms.ToTensor(),                     # /255 + HWC→CHW
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # ImageNet 标准化
])

x = pipeline(img)
print(f"tensor type:  {type(x).__name__}")
print(f"tensor dtype: {x.dtype}")
print(f"tensor shape: {tuple(x.shape)}      # (C, H, W)")
print(f"per-channel mean: {x.mean(dim=(1, 2)).tolist()}")
print(f"per-channel std:  {x.std(dim=(1, 2)).tolist()}")

batch = x.unsqueeze(0)  # 增加 batch 维度：(C,H,W) → (N,C,H,W)
print(f"\nbatched shape: {tuple(batch.shape)}   # (N, C, H, W) — ready for a model")
```

Four steps, in this exact order: `Resize(256)` scales the shorter side to 256; `CenterCrop(224)` takes a 224x224 patch from the middle; `ToTensor()` divides by 255 and swaps HWC to CHW; `Normalize` subtracts the ImageNet mean and divides by std. Reversing that order silently changes what reaches the model.

## Ship It | 交付产出

This lesson produces:

- `outputs/prompt-vision-preprocessing-audit.md` — a prompt that turns any model card or dataset card into a checklist of the exact preprocessing invariants a team must honour.
- `outputs/skill-image-tensor-inspector.md` — a skill that, given any image-shaped tensor or array, reports dtype, layout, range, and whether it looks raw, normalized, or standardized.

## Exercises | 练习题

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


1. **(Easy | 简单)** Load a JPEG with OpenCV (`cv2.imread`) and with Pillow. Print both shapes and the pixel at `(0, 0)`. Explain the channel-order difference, then write a one-line conversion that makes the OpenCV array identical to the Pillow one.
   用 OpenCV 和 Pillow 分别加载同一张 JPEG，打印形状和 (0,0) 像素值。解释通道顺序差异，写一行代码使两者一致。

2. **(Medium | 中等)** Write `standardize(img, mean, std)` and its inverse that together pass a `roundtrip_max_diff <= 1` test on any uint8 image. Your functions must work on a single image in HWC and on a batch in NCHW with the same call.
   编写 `standardize` 及其逆函数，要求在任意 uint8 图像上往返误差不超过 1，且同时支持单张图（HWC）和批量（NCHW）输入。

3. **(Hard | 困难)** Take a 3-channel ImageNet-standardized tensor and run it through a 1x1 conv that learns a weighted mixture of RGB into a single grayscale channel. Initialize the weights to `[0.299, 0.587, 0.114]`, freeze them, and verify the output matches your manual `rgb_to_grayscale` to within floating-point error. What other classical color-space transforms can be written as 1x1 convolutions?
   用 1x1 卷积实现 RGB 到灰度的加权混合，初始化权重为 `[0.299, 0.587, 0.114]` 并冻结，验证与手动灰度转换结果一致。思考：还有哪些经典色彩空间转换可以写成 1x1 卷积？

## Key Terms | 关键术语

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Pixel | "A coloured square" | One sample of light intensity at one grid location — three numbers for colour, one for grayscale | 像素：一个空间位置的光强采样值，彩色为三个数，灰度为一个数 |
| Channel | "The colour" | One of the parallel spatial grids stacked into an image tensor; last axis in HWC, first in CHW | 通道：图像张量中平行堆叠的空间网格之一 |
| HWC / CHW | "The shape" | Axis orderings for an image tensor; disk and PIL use HWC, PyTorch and cuDNN use CHW | HWC/CHW：图像张量的两种轴排列方式 |
| Normalize | "Scale the image" | Divide by 255 so pixels live in [0, 1] — necessary but not sufficient | 归一化：除以 255 使像素值在 [0,1] 范围内 |
| Standardize | "Zero-center" | Subtract mean and divide by std per channel so the input distribution matches what the model was trained on | 标准化：逐通道减均值除标准差，使输入分布与训练时一致 |
| Grayscale conversion | "Average the channels" | A weighted sum with coefficients 0.299/0.587/0.114 that matches human luminance perception | 灰度转换：按人眼亮度感知加权的通道求和 |
| Interpolation | "How resize picks pixels" | The rule that decides output values when the new grid does not align with the old one — nearest for labels, bilinear for training, bicubic for display | 插值：缩放时计算新像素值的规则 |
| Aspect ratio | "Width over height" | The ratio that distinguishes "resize and pad" from "resize and stretch" | 宽高比：区分 "缩放+填充" 与 "缩放+拉伸" 的关键比例 |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [Charles Poynton — A Guided Tour of Color Space](https://poynton.ca/PDFs/Guided_tour.pdf) — the clearest technical treatment of why there are so many color spaces and when each one matters
- [PyTorch Vision Transforms Docs](https://pytorch.org/vision/stable/transforms.html) — the full pipeline of transforms you will actually compose in production
- [How JPEG Works (Colt McAnlis)](https://www.youtube.com/watch?v=F1kYBnY6mwg) — a sharp visual tour of chroma subsampling, DCT, and why JPEG encodes YCbCr rather than RGB
- [ImageNet Preprocessing Conventions (torchvision models)](https://pytorch.org/vision/stable/models.html) — the source of truth for `mean=[0.485, 0.456, 0.406]` and why every model in the zoo expects it
