# Semantic Segmentation — U-Net | 语义分割 — U-Net

> Segmentation is classification at every pixel. U-Net makes it work by pairing a downsampling encoder with an upsampling decoder and wiring skip connections between them.

> **【中文解读】** 语义分割就是对每个像素进行分类。U-Net 通过配对下采样编码器和上采样解码器，并在它们之间连接跳跃连接来实现这一点。编码器提取特征，解码器恢复分辨率，跳跃连接保留细节信息。

> **【拓展：U-Net 的广泛应用】** U-Net 最初为医学影像分割设计，但已成为许多领域的基础架构：Stable Diffusion 使用 U-Net 作为核心去噪网络、自动驾驶中的道路分割、卫星图像的土地覆盖分类。其编码器-解码器+跳跃连接的模式已被广泛复制。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 4 Lesson 03 (CNNs), Phase 4 Lesson 04 (Image Classification)
**Time:** ~75 minutes

## Learning Objectives

- Distinguish semantic, instance, and panoptic segmentation and pick the right task for a given problem
- Build a U-Net from scratch in PyTorch with encoder blocks, a bottleneck, a decoder with transposed convolutions, and skip connections
- Implement pixel-wise cross-entropy, Dice loss, and the combined loss that is the current default for medical and industrial segmentation
- Read IoU and Dice metrics per class and diagnose whether a bad score comes from small-object recall, boundary accuracy, or class imbalance

> **【中文解读】** 学习目标列出了完成本课后应该掌握的核心能力。建议在开始学习前先浏览目标，学完后对照检查是否达成。


## The Problem | 问题引入

Classification outputs one label per image. Detection outputs a handful of boxes per image. Segmentation outputs one label per pixel. For an input of size `H x W`, the output is a tensor of shape `H x W` (semantic) or `H x W x N_instances` (instance). That is millions of predictions per image, not one.

> **【中文解读】** 分类输出一个标签，检测输出若干框，分割输出每个像素的标签。分割的核心难题是：既要看到全局上下文（这是哪种场景），又要保留局部像素细节（这个像素是路还是人行道）。标准 CNN 通过空间压缩获取上下文时会丢失细节，U-Net 通过跳跃连接同时解决了这两个需求。

The structure of segmentation is why it powers almost every dense-prediction vision product: medical imaging (tumour masks), autonomous driving (road, lane, obstacle), satellite (building footprints, crop boundaries), document parsing (layout zones), robotics (graspable regions). None of those tasks can be solved by putting a box around the object; they need the exact silhouette.

The architectural problem is simple to state and not simple to solve: you need the network to see the global context of an image (what kind of scene is this) and the local pixel detail (exactly which pixel is road vs pavement) simultaneously. A standard CNN compresses spatially to gain context, which throws away the detail. U-Net was the design that got both.

## The Concept | 核心概念

> **【中文解读】** 本节介绍核心概念和理论基础。掌握这些概念是后续动手实现的前提，同时也是面试和工程实践中高频考察的知识点。


### Semantic vs instance vs panoptic

```mermaid
flowchart LR
    IN["Input image"] --> SEM["Semantic<br/>(pixel → class)"]
    IN --> INS["Instance<br/>(pixel → object id,<br/>only foreground classes)"]
    IN --> PAN["Panoptic<br/>(every pixel → class + id)"]

    style SEM fill:#dbeafe,stroke:#2563eb
    style INS fill:#fef3c7,stroke:#d97706
    style PAN fill:#dcfce7,stroke:#16a34a
```

- **Semantic** says "this pixel is road, that pixel is car." Two cars next to each other collapse into a single blob.
- **Instance** says "this pixel is car #3, that pixel is car #5." Ignores background stuff ("stuff" = sky, road, grass).
- **Panoptic** unifies both: every pixel gets a class label, every instance gets a unique id, stuff and things both segmented.

This lesson covers semantic. The next lesson (Mask R-CNN) covers instance.

### The U-Net shape

```mermaid
flowchart LR
    subgraph ENC["Encoder (contracting)"]
        E1["64<br/>H x W"] --> E2["128<br/>H/2 x W/2"]
        E2 --> E3["256<br/>H/4 x W/4"]
        E3 --> E4["512<br/>H/8 x W/8"]
    end
    subgraph BOT["Bottleneck"]
        B1["1024<br/>H/16 x W/16"]
    end
    subgraph DEC["Decoder (expanding)"]
        D4["512<br/>H/8 x W/8"] --> D3["256<br/>H/4 x W/4"]
        D3 --> D2["128<br/>H/2 x W/2"]
        D2 --> D1["64<br/>H x W"]
    end
    E4 --> B1 --> D4
    E1 -. skip .-> D1
    E2 -. skip .-> D2
    E3 -. skip .-> D3
    E4 -. skip .-> D4
    D1 --> OUT["1x1 conv<br/>classes"]

    style ENC fill:#dbeafe,stroke:#2563eb
    style BOT fill:#fef3c7,stroke:#d97706
    style DEC fill:#dcfce7,stroke:#16a34a
```

The encoder halves spatial resolution four times and doubles channels. The decoder reverses: doubles spatial resolution four times and halves channels. The skip connections concatenate matching encoder features with decoder features at every resolution. The final 1x1 conv maps `64 -> num_classes` at full resolution.

Why skip connections are necessary: the decoder has seen only small feature maps by the time it tries to output pixel-level predictions. Without the skips it cannot localise edges accurately because that information was compressed away in the encoder. Skip connections hand it the high-resolution feature maps the encoder computed on the way down.

### Transposed vs bilinear upsample

The decoder has to expand spatial dimensions. Two options:

- **Transposed convolution** (`nn.ConvTranspose2d`) — learnable upsample. Historical U-Net default. Can produce checkerboard artifacts if stride and kernel size do not divide evenly.
- **Bilinear upsample + 3x3 conv** — smooth upsample followed by a conv. Fewer artifacts, fewer parameters, now the modern default.

Both appear in the wild. For a first U-Net, bilinear is safer.

### Cross-entropy on a pixel grid

For semantic segmentation with C classes, the model output is `(N, C, H, W)`. The target is `(N, H, W)` with integer class IDs. Cross-entropy is identical to the classification case, just applied at every spatial position:

```
Loss = mean over (n, h, w) of -log( softmax(logits[n, :, h, w])[target[n, h, w]] )
```

`F.cross_entropy` in PyTorch handles this shape natively. No reshape needed.

### Dice loss and why you need it

Cross-entropy treats every pixel equally. That is wrong when one class dominates the frame (medical imaging: 99% background, 1% tumour). The network can score 99% accuracy by predicting background everywhere and still be useless.

Dice loss solves this by directly optimising the overlap between predicted and true mask:

```
Dice(p, y) = 2 * sum(p * y) / (sum(p) + sum(y) + epsilon)
Dice_loss = 1 - Dice
```

where `p` is the sigmoid/softmax probability map for a class and `y` is the binary ground-truth mask. The loss is zero only when the overlap is perfect. Because it is ratio-based, class imbalance is irrelevant.

In practice, use the **combined loss**:

```
L = L_cross_entropy + lambda * L_dice       (lambda ~ 1)
```

Cross-entropy gives stable gradients early in training; Dice focuses the tail of training on actually matching the mask shape. This combination is the medical-imaging default and hard to beat on any class-imbalanced dataset.

### Evaluation metrics

- **Pixel accuracy** — percent of pixels predicted correctly. Cheap. Broken on imbalanced data for the same reason as accuracy in classification.
- **IoU per class** — intersection over union for each class's mask; average across classes = mIoU.
- **Dice (F1 on pixels)** — similar to IoU; `Dice = 2 * IoU / (1 + IoU)`. Medical imaging prefers Dice, driving community prefers IoU; they are monotonically related.
- **Boundary F1** — measures how close predicted boundaries are to ground-truth boundaries, penalising even small shifts. Important for high-precision tasks like semiconductor inspection.

Report IoU per class, not just mIoU. Mean IoU hides a class at 15% when nine others are at 85%.

### Input resolution trade-off

U-Net's encoder halves resolution four times, so the input must be divisible by 16. Medical images are often 512x512 or 1024x1024. Autonomous-driving crops are 2048x1024. The memory cost of U-Net scales with `H * W * C_max`, and at 1024x1024 with 1024 bottleneck channels the forward pass already uses gigabytes of VRAM.

Two standard workarounds:
1. Tile the input — process 256x256 tiles with overlap and stitch.
2. Replace the bottleneck with dilated convolutions that keep spatial resolution higher but widen receptive field (the DeepLab family).

For a first model, a 256x256 input with a 64-channel-base U-Net trains comfortably on 8 GB VRAM.

> **【中文解读】** 本节通过代码从零实现核心算法。这种 "from scratch" 的方式能帮助理解框架背后的原理，遇到问题时不会被黑盒困住。

> **【拓展：工业部署中的视觉系统】** 在实际工业部署中，视觉模型需要考虑推理延迟、模型大小、边缘设备适配等问题。TensorRT、ONNX Runtime、OpenVINO 是常用的推理加速工具。自动驾驶系统（如 Tesla FSD）通常在车载芯片上实时运行多个视觉模型。

> **【拓展：数据标注与质量】** 视觉任务的效果高度依赖标注数据质量。Label Studio、CVAT 是主流标注工具。在工业场景中，主动学习（Active Learning）可以减少标注成本：模型对不确定的样本请求人工标注，确定性的样本自动标注。




## Build It | 动手实现

### Step 1: Encoder block

Two 3x3 convs with batch norm and ReLU. The first conv changes channel count; the second keeps it.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DoubleConv(nn.Module):
    def __init__(self, in_c, out_c):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_c, out_c, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_c),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_c, out_c, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_c),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.net(x)
```

This block is reused throughout. `bias=False` because BN's beta handles the bias.

### Step 2: Down and up blocks

```python
class Down(nn.Module):
    def __init__(self, in_c, out_c):
        super().__init__()
        self.net = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(in_c, out_c),
        )

    def forward(self, x):
        return self.net(x)


class Up(nn.Module):
    def __init__(self, in_c, out_c):
        super().__init__()
        self.up = nn.Upsample(scale_factor=2, mode="bilinear", align_corners=False)
        self.conv = DoubleConv(in_c, out_c)

    def forward(self, x, skip):
        x = self.up(x)
        if x.shape[-2:] != skip.shape[-2:]:
            x = F.interpolate(x, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        x = torch.cat([skip, x], dim=1)
        return self.conv(x)
```

The spatial-only shape check (`shape[-2:]`) handles inputs whose dimensions are not divisible by 16; a safe `F.interpolate` aligns the tensor before the concat. Comparing the full shape would also trigger on channel-count differences, which should be a loud error, not a silent interpolate.

### Step 3: The U-Net

```python
class UNet(nn.Module):
    def __init__(self, in_channels=3, num_classes=2, base=64):
        super().__init__()
        self.inc = DoubleConv(in_channels, base)
        self.d1 = Down(base, base * 2)
        self.d2 = Down(base * 2, base * 4)
        self.d3 = Down(base * 4, base * 8)
        self.d4 = Down(base * 8, base * 16)
        self.u1 = Up(base * 16 + base * 8, base * 8)
        self.u2 = Up(base * 8 + base * 4, base * 4)
        self.u3 = Up(base * 4 + base * 2, base * 2)
        self.u4 = Up(base * 2 + base, base)
        self.outc = nn.Conv2d(base, num_classes, kernel_size=1)

    def forward(self, x):
        x1 = self.inc(x)
        x2 = self.d1(x1)
        x3 = self.d2(x2)
        x4 = self.d3(x3)
        x5 = self.d4(x4)
        x = self.u1(x5, x4)
        x = self.u2(x, x3)
        x = self.u3(x, x2)
        x = self.u4(x, x1)
        return self.outc(x)

net = UNet(in_channels=3, num_classes=2, base=32)
x = torch.randn(1, 3, 256, 256)
print(f"output: {net(x).shape}")
print(f"params: {sum(p.numel() for p in net.parameters()):,}")
```

Output shape `(1, 2, 256, 256)` — same spatial size as the input, `num_classes` channels. About 7.7M parameters at `base=32`.

### Step 4: Losses

```python
def dice_loss(logits, targets, num_classes, eps=1e-6):
    probs = F.softmax(logits, dim=1)
    targets_one_hot = F.one_hot(targets, num_classes).permute(0, 3, 1, 2).float()
    dims = (0, 2, 3)
    intersection = (probs * targets_one_hot).sum(dim=dims)
    denom = probs.sum(dim=dims) + targets_one_hot.sum(dim=dims)
    dice = (2 * intersection + eps) / (denom + eps)
    return 1 - dice.mean()


def combined_loss(logits, targets, num_classes, lam=1.0):
    ce = F.cross_entropy(logits, targets)
    dc = dice_loss(logits, targets, num_classes)
    return ce + lam * dc, {"ce": ce.item(), "dice": dc.item()}
```

Dice is computed per class then averaged (macro Dice). The `eps` prevents division by zero on classes absent from the batch.

### Step 5: IoU metric

```python
@torch.no_grad()
def iou_per_class(logits, targets, num_classes):
    preds = logits.argmax(dim=1)
    ious = torch.zeros(num_classes)
    for c in range(num_classes):
        pred_c = (preds == c)
        true_c = (targets == c)
        inter = (pred_c & true_c).sum().float()
        union = (pred_c | true_c).sum().float()
        ious[c] = (inter / union) if union > 0 else torch.tensor(float("nan"))
    return ious
```

Returns a vector of length C. `nan` marks classes absent from the batch — do not average over those when computing mIoU.

### Step 6: Synthetic dataset for end-to-end verification

Generate shapes on coloured backgrounds so the network has to learn shape, not pixel colour.

```python
import numpy as np
from torch.utils.data import Dataset, DataLoader

def synthetic_segmentation(num_samples=200, size=64, seed=0):
    rng = np.random.default_rng(seed)
    images = np.zeros((num_samples, size, size, 3), dtype=np.float32)
    masks = np.zeros((num_samples, size, size), dtype=np.int64)
    for i in range(num_samples):
        bg = rng.uniform(0, 1, (3,))
        images[i] = bg
        masks[i] = 0
        num_shapes = rng.integers(1, 4)
        for _ in range(num_shapes):
            cls = int(rng.integers(1, 3))
            color = rng.uniform(0, 1, (3,))
            cx, cy = rng.integers(10, size - 10, size=2)
            r = int(rng.integers(4, 12))
            yy, xx = np.meshgrid(np.arange(size), np.arange(size), indexing="ij")
            if cls == 1:
                mask = (xx - cx) ** 2 + (yy - cy) ** 2 < r ** 2
            else:
                mask = (np.abs(xx - cx) < r) & (np.abs(yy - cy) < r)
            images[i][mask] = color
            masks[i][mask] = cls
        images[i] += rng.normal(0, 0.02, images[i].shape)
        images[i] = np.clip(images[i], 0, 1)
    return images, masks


class SegDataset(Dataset):
    def __init__(self, images, masks):
        self.images = images
        self.masks = masks

    def __len__(self):
        return len(self.images)

    def __getitem__(self, i):
        img = torch.from_numpy(self.images[i]).permute(2, 0, 1).float()
        mask = torch.from_numpy(self.masks[i]).long()
        return img, mask
```

Three classes: background (0), circles (1), squares (2). The network must learn to distinguish shape.

### Step 7: Training loop

```python
def train_one_epoch(model, loader, optimizer, device, num_classes):
    model.train()
    loss_sum, total = 0.0, 0
    iou_sum = torch.zeros(num_classes)
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        loss, _ = combined_loss(logits, y, num_classes)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss_sum += loss.item() * x.size(0)
        total += x.size(0)
        iou_sum += iou_per_class(logits, y, num_classes).nan_to_num(0)
    return loss_sum / total, iou_sum / len(loader)
```

Run this for 10-30 epochs on the synthetic dataset and watch mIoU climb past 0.9 for the shape classes. Note the `nan_to_num(0)` treats classes absent from a batch as zero; for accurate per-class IoU, mask by presence and use `torch.nanmean` across batches at evaluation time rather than averaging here.




> **【拓展：视觉模型的持续学习】** 在生产环境中，视觉模型需要不断适应新数据（新产品、新场景、新光照条件）。持续学习（Continual Learning）技术可以防止模型在适应新数据时遗忘旧知识。这在自动驾驶和工业质检中尤为重要。

## Use It | 用框架实现

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


For production, `segmentation_models_pytorch` ("smp") wraps every standard segmentation architecture with any torchvision or timm backbone. Three lines:

```python
import segmentation_models_pytorch as smp

model = smp.Unet(
    encoder_name="resnet34",
    encoder_weights="imagenet",
    in_channels=3,
    classes=3,
)
```

Also worth knowing for real work:
- **DeepLabV3+** replaces max-pool-based downsampling with dilated convs so the bottleneck keeps resolution; faster boundaries on satellite and driving data.
- **SegFormer** swaps the conv encoder for a hierarchical transformer; current SOTA on many benchmarks.
- **Mask2Former** / **OneFormer** unify semantic, instance, and panoptic segmentation in a single architecture.

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


All three are drop-in replacements in `smp` or `transformers` with the same data loader.



## Ship It | 产出物

This lesson produces:

- `outputs/prompt-segmentation-task-picker.md` — a prompt that picks between semantic, instance, and panoptic segmentation and names the architecture for a given task.
- `outputs/skill-segmentation-mask-inspector.md` — a skill that reports class distribution, predicted-mask statistics, and the classes that are under-predicted or boundary-blurred.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


## Exercises | 练习题

1. **(Easy)** Implement `bce_dice_loss` for a binary segmentation task (foreground vs background). Verify on a synthetic two-class dataset that the combined loss converges faster than BCE alone when the foreground is 5% of pixels.
2. **(Medium)** Replace the `nn.Upsample + conv` up-block with a `nn.ConvTranspose2d` up-block. Train both on the synthetic dataset and compare mIoU. Observe where checkerboard artifacts appear in the transposed-conv version.
3. **(Hard)** Take a real segmentation dataset (Oxford-IIIT Pets, Cityscapes mini split, or a medical subset) and train the U-Net to within 2 IoU points of the `smp.Unet` reference. Report per-class IoU and identify which classes benefit most from adding Dice to the loss.

> **【中文解读】** 术语表中的 "What people say" vs "What it actually means" 区分了日常口语和精确技术含义。在团队协作中，统一术语定义可以避免大量沟通误解。


## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Semantic segmentation | "Label every pixel" | Per-pixel classification into C classes; instances of the same class merge |
| Instance segmentation | "Label every object" | Separates distinct instances of the same class; foreground-only |
| Panoptic segmentation | "Semantic + instance" | Every pixel gets a class; every thing instance also gets a unique id |
| Skip connection | "U-Net bridge" | Concatenation of encoder features into matching-resolution decoder features; preserves high-frequency detail |
| Transposed conv | "Deconvolution" | Learnable upsampling; can produce checkerboard artifacts |
| Dice loss | "Overlap loss" | 1 - 2|A ∩ B| / (|A| + |B|); optimises mask overlap directly and is robust to class imbalance |
| mIoU | "Mean intersection over union" | Average IoU across classes; the community-standard metric for segmentation |
| Boundary F1 | "Boundary accuracy" | F1 score computed on boundary pixels only; matters for precision-critical tasks |

> **【中文解读】** 延伸阅读提供了深入学习的高质量资源。这些论文和教程是该领域的经典参考文献，适合需要深入理解的读者。


## Further Reading | 延伸阅读

- [U-Net: Convolutional Networks for Biomedical Image Segmentation (Ronneberger et al., 2015)](https://arxiv.org/abs/1505.04597) — the original paper; the figure everyone copies is on page 2
- [Fully Convolutional Networks (Long et al., 2015)](https://arxiv.org/abs/1411.4038) — the paper that first made segmentation an end-to-end conv problem
- [segmentation_models_pytorch](https://github.com/qubvel/segmentation_models.pytorch) — the reference for production segmentation; every standard architecture plus every standard loss
- [Lessons learned from training SOTA segmentation (kaggle.com competitions)](https://www.kaggle.com/code/iafoss/carvana-unet-pytorch) — a walkthrough of why TTA, pseudo-labeling, and class weights matter on real data
