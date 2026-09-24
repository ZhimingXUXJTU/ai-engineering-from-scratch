# 图像分类

> 类别是从像素到类别的概率分布的函数.

> **【中文解读】**图像分类器本质上是一个从像素到类别概率分布函数――检测(分类区域) 、分类分类) 、检索(按类别相似度排序) 归根结底是分类――掌握分类的完整流水线――数据集、增强、训练、评估) 是所有视觉任务的基础――

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 2 Lesson 09 (Model Evaluation), Phase 3 Lesson 10 (Mini Framework), Phase 4 Lesson 03 (CNNs) | **前置知识:** Phase 2 Lesson 09（模型评估），Phase 3 Lesson 10（迷你框架），Phase 4 Lesson 03（CNN）
**Time:** ~75 minutes | **时间:** ~75 分钟

## 学习目标

- 建立CIFAR-10的端到端图像分类管道:数据集,增强,模型,培训循环,评估
- 解释每个组件的作用 (数据加载器,损失,优化器,计划器,增强) 并预测损失曲线中任何组件的破解如何表现
- 从零开始实施混合,切割和标签滑滑,并证明每一个值得添加的时间
- 阅读一个混矩阵和每个类的精度/召回表,以诊断数据集和模型失误超出总准确性

> **【中文解读】**学习目标列出了课程完成后应掌握的核心能力.建议在开始学习前先浏览目标,学习完后对照检查是否已实现.


## 问题 问题引入

每个视觉任务都将降低到某个层次的图像分类.检测分类区域. 分类分类分类像素.检索分类与类中位数相似.获得分类正确的数据集循环,增强政策,损失,评估是将技能转移到阶段中的其他任务.

> 每个交付的视觉任务都在某种程度上归结为图像分类.检测分类区域.分类分类.检查按类中心的相似度排序.分类是对数据集循环进行的.增强策略,损失函数,评估是将每个任务的技能转移到这个阶段的其他任务.

> **【中文解读】**所有实际部署的视觉任务本质上可以归结为图像分类:目标检测是"对区域分类",语义分类是"对像素分类",图像检索是"按类型中心相似度排序"......把分类流线的每个环节弄清楚,是掌握这一阶段所有后续课程的关键.

许多分类错误都不在模型中. 它们生活在一个道中:一个破碎的规范化,一个不调整的培训组,增强,扭曲标签,一个通过培训数据污染的验证分断, 通过正确的设置,在CIFAR-10上达到93%的CNN通常会在破产时达到70-75%的分数,

> 大多数分类 bug 不在模型中.它们存在于流水线中:错误归结,未打乱的训练集,扭曲标签的增强,被训练的数据污染的验证集,在第30个时代,静默散发的学习率.一个正确配置可以达到93%的CNN在CIFAR-10上,在错误配置下通常只有70-75%,损失曲线看起来很合理.

通过手动连接整个管道,所以每个部分都可检查.`torchvision.datasets`这可能隐藏了昆虫.

> 让每个部分都可检查.`torchvision.datasets`任何可能隐藏的东西.

> **【中文解读】**大多数分类 bug 不在模型本身,而在流水线中:归结搞错,训练集没乱,增强破坏标签,验证集被训练数据污染,学习率然传播――正确配置可以达到93%的模型,错误配置只能达到70-75%,而且损失曲线看起来很正常这是最可怕的地方――本课程从开始构建完整流水线,每个环节都可以直接检查.

## 概念的核心概念

### 类别管道

```mermaid
flowchart LR
    A["Dataset<br/>(images + labels)"] --> B["Augment<br/>(random transforms)"]
    B --> C["Normalise<br/>(mean/std)"]
    C --> D["DataLoader<br/>(batch + shuffle)"]
    D --> E["Model<br/>(CNN)"]
    E --> F["Logits<br/>(N, C)"]
    F --> G["Cross-entropy loss"]
    F --> H["Argmax<br/>at eval"]
    G --> I["Backward"]
    I --> J["Optimizer step"]
    J --> K["Scheduler step"]
    K --> E

    style A fill:#dbeafe,stroke:#2563eb
    style E fill:#fef3c7,stroke:#d97706
    style G fill:#fecaca,stroke:#dc2626
    style H fill:#dcfce7,stroke:#16a34a
```

交叉透取原始的记录,而不是软max输出,所以任何`model(x).softmax()`在损失轻声计算错误的梯度之前.

> 这循环中的每一行都是存在的错误.交叉接收原始记录,而不是软max输出,所以在损失函数前做任何事情.`model(x).softmax()`城市静默计算错误的梯度.

> **【中文解读】**流水线中每一行都可能藏有 bug.交叉接收是原始 logits. 如果先做 softmax 再传入损失函数,梯度计算就完全错了,但不会报错.`optimizer.zero_grad()`错误的发生在一个阶段, 跳过它会积累渐变, 看起来像一个非常不稳定的学习率.

### 交叉,和软max

一个分类器产生`C`应用软max将它们转化为概率分布:

> 分类器为每张图像产生`C`个数字,称为逻辑. 应用软max将它们转换为概率分布:

```
softmax(z)_i = exp(z_i) / sum_j exp(z_j)
```

交叉透量测量正确类的负记录概率:

> 交叉衡正确类别的负对数概率:

```
CE(z, y) = -log( softmax(z)_y )
        = -z_y + log( sum_j exp(z_j) )
```

右边的表格是数值稳定的表格 (log-sum-exp).`nn.CrossEntropyLoss`软max+NLL在一个操作中合并并并直接取原始的logits. 应用软max自己首先几乎总是一个错误.

> 右边的形式是数值稳定的 (log-sum-exp) .`nn.CrossEntropyLoss`在一个操作中融合了软max + NLL,直接接收原始逻辑――自己先应用软max 几乎总是一个bug你在计算日志(软max(软max(z))),一个无意义的量――

> **【中文解读】**皮托尔奇的`nn.CrossEntropyLoss`内部已经融合了软max + 负对数似然,直接传入原始逻辑即可.

### 为什么增强效果

对于转换 (从重量共享) 的 CNN 有诱导偏见,但没有内置的变化,即作物,翻转,颜色的震惊或.教导它这些变化的唯一方法是向它展示它们的像素.训练过程中的每一次随机转变都是说:"这两个图像都有相同的标签;学习忽略差异的特征.

> 对于平移有归纳偏移 (来自权重共享),但对剪裁,翻转,颜色动或遮没有内置不变性.

> **【拓展：数据增强与模型泛化】**数据增强是现代AI最强大的免费正规化手段. 在ResNet、EfficientNet等经典模型训练中,增强策略的好坏直接影响了3-5%的准确率.

```
Original crop:  "dog facing left"
Flip:           "dog facing right"       <- same label, different pixels
Rotate(+15):    "dog, slight tilt"
Colour jitter:  "dog in warmer light"
RandomErasing:  "dog with patch missing"
```

规则:增强必须保留标签.一个数字上的切割和旋转可以将"6"转换为 "9";对于该数据集,您使用较小的旋转范围,并选择尊重数字特定的不变的增强.

> 规则:增强必须保持标签不变.对数字进行遮蔽和旋转可能把"6"变成9";对于那个数据集,你使用更小的旋转范围,并选择尊重数字的不变增强.

### 混合和切割混合物

常见的增强将像素转化,但保持标签的热度.**Mixup**其他**cutmix**通过插入两者来打破这一点.

> 常常增强变化像素但保持标签为一个热的.**Mixup**和 **cutmix**通过对方进行插值打破这一点.

```
Mixup:
  lambda ~ Beta(a, a)
  x = lambda * x_i + (1 - lambda) * x_j
  y = lambda * y_i + (1 - lambda) * y_j

Cutmix:
  paste a random rectangle of x_j into x_i
  y = area-weighted mix of y_i and y_j
```

模型停止记忆尖的单热目标,并学习间隔. 训练损失增加,测试精度增加. 这是任何分类器的唯一最便宜的强度升级.

> 为什么有帮助:模型停止记忆尖峰式的一个热门目标,学会在类别之间插值――训练损失上升,测试准确率也上升――这是任何类器中最便宜的鲁棒性升级――

> **【拓展：Mixup 在大模型中的应用】**在ChatGPT等LLM培训中,标签平滑和软标签技术也得到广泛使用,帮助模型产生更准确的概率输出,减少过度自信.

### 标签滑滑

的表哥,而不是训练`[0, 0, 1, 0, 0]`列车对抗`[eps/C, eps/C, 1-eps, eps/C, eps/C]`为了一个小的`eps`模型不会产生任意尖的位,并且几乎没有成本地提高校准.`nn.CrossEntropyLoss(label_smoothing=0.1)`自PyTorch 1.10以来.

> 混合的近亲──不使用 `[0, 0, 1, 0, 0]`进行训练,而是使用`[eps/C, eps/C, 1-eps, eps/C, eps/C]`在其中`eps`由于 0.1 ⋅ 阻止模型产生任意尖的逻辑,几乎零成本改善校准.`nn.CrossEntropyLoss(label_smoothing=0.1)`在中.

### 超出准确性的评估

总的来说,一个90-10的二进制分类器总是预测大多数类的分数是90%.

> 总体准确率隐藏不平衡. 一个总体预测大多数类型的90-10分类.

- **Per-class accuracy**每类一个数字;立即出现低绩效类别.
  中文翻译:每类准确率每类一个数字;立即暴露表现不佳的类别
- **Confusion matrix** C x C 格格,行 i col j = 预测的真实类 i 的数量为类 j; 横向是正确的,外横向是您的模型居住的地方.
  中文翻译:混矩阵C x C 网格,行 i 列 j = 真实类别 i 被预测为类别 j 的计数;对角线是正确的,非对角线是你的模型出错的地方。
- **Top-1 / Top-5**是否正确的类型在前1或前5个预测中;对ImageNet来说,前5个是重要的,因为"诺威奇特里耶尔"与"诺福克特里耶尔"等类型是真正模糊的.
  中文翻译:Top-1 /Top-5正确类别是否在前1或前5个预测中;Top-5对ImageNet 很重要,因为像"诺威奇特里耶尔"vs"诺福克特里耶尔" 这类类别确实模两可──
- **Calibration (ECE)**0.8的可靠性预测 80% 的时间是否正确?现代网络系统上过于安全;通过温度缩小或标签平滑来解决.
  中文翻译:校准(ECE) 0.8 置信度预测 80% 的时间是对的吗?现代网络系统性地过度自信; 用温度缩放或标签平滑修复。

> **【拓展：工业部署中的视觉系统】**在实际工业部署中,视觉模型需要考虑推迟模型大小的边缘设备适应等问题.


## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
receptive-field
```

## 建立它

### 步骤1:确定性合成数据集

为了使这门课程能够复制和快速,我们构建了一个合成数据集,看起来像CIFAR  32x32 RGB图像,具有类型特定的结构,模型必须学习.

> 为了使这本课程可复制和快速,我们构建了一个看起来像CIFAR的合成数据集带有模型必须学习的类别特定结构的32x32RGB图像.

```python
import numpy as np
import torch
from torch.utils.data import Dataset


def synthetic_cifar(num_per_class=1000, num_classes=10, seed=0):
    rng = np.random.default_rng(seed)
    X = []
    Y = []
    for c in range(num_classes):
        centre = rng.uniform(0, 1, (3,))
        freq = 2 + c
        for _ in range(num_per_class):
            yy, xx = np.meshgrid(np.linspace(0, 1, 32), np.linspace(0, 1, 32), indexing="ij")
            r = np.sin(xx * freq) * 0.5 + centre[0]
            g = np.cos(yy * freq) * 0.5 + centre[1]
            b = (xx + yy) * 0.5 * centre[2]
            img = np.stack([r, g, b], axis=-1)
            img += rng.normal(0, 0.08, img.shape)
            img = np.clip(img, 0, 1)
            X.append(img.astype(np.float32))
            Y.append(c)
    X = np.stack(X)
    Y = np.array(Y)
    idx = rng.permutation(len(X))
    return X[idx], Y[idx]


class ArrayDataset(Dataset):
    def __init__(self, X, Y, transform=None):
        self.X = X
        self.Y = Y
        self.transform = transform

    def __len__(self):
        return len(self.X)

    def __getitem__(self, i):
        img = self.X[i]
        if self.transform is not None:
            img = self.transform(img)
        img = torch.from_numpy(img).permute(2, 0, 1)
        return img, int(self.Y[i])
```

每个类别都会有自己的颜色调色和频率模式,加上高斯噪音,迫使模型学习信号而不是记忆像素.

> 每类都有自己的调色板和频率模式,加上高音噪声,迫使模型学习信号而不是记忆像素.

### 标准化和增强

两种变化,每个视觉管道都有.

> 每个视频流线都有两个变化.

```python
def standardize(mean, std):
    mean = np.array(mean, dtype=np.float32)
    std = np.array(std, dtype=np.float32)
    def _fn(img):
        return (img - mean) / std
    return _fn


def random_hflip(p=0.5):
    def _fn(img):
        if np.random.random() < p:
            return img[:, ::-1, :].copy()
        return img
    return _fn


def random_crop(pad=4):
    def _fn(img):
        h, w = img.shape[:2]
        padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode="reflect")
        y = np.random.randint(0, 2 * pad)
        x = np.random.randint(0, 2 * pad)
        return padded[y:y + h, x:x + w, :]
    return _fn


def compose(*fns):
    def _fn(img):
        for fn in fns:
            img = fn(img)
        return img
    return _fn
```

放映板在收获之前,而不是零板,因为黑色边界是模型将学会以无用的方式忽略的信号.

> 剪裁前使用反射填充而不是零填充,因为黑边框是模型学会以无用的方式忽略的信号.

### 步骤3:混合

混合了训练阶段内的两个图像和两个标签. 作为一批转换,所以它住在前进的传递旁边而不是数据集内部.

> 在训练阶段中混合两张图像和两个标签.作为批量变化实现,因此它位于前向传播旁边而不是数据集内部.

```python
def mixup_batch(x, y, num_classes, alpha=0.2):
    if alpha <= 0:
        return x, torch.nn.functional.one_hot(y, num_classes).float()
    lam = float(np.random.beta(alpha, alpha))
    idx = torch.randperm(x.size(0), device=x.device)
    x_mixed = lam * x + (1 - lam) * x[idx]
    y_onehot = torch.nn.functional.one_hot(y, num_classes).float()
    y_mixed = lam * y_onehot + (1 - lam) * y_onehot[idx]
    return x_mixed, y_mixed


def soft_cross_entropy(logits, soft_targets):
    log_probs = torch.log_softmax(logits, dim=-1)
    return -(soft_targets * log_probs).sum(dim=-1).mean()
```

`soft_cross_entropy`目标是完全单热的时,它降低到通常的单热情况.

> `soft_cross_entropy`对于软标签分布的交叉──当目标恰好是一个热时,它退化为通常的一个热时――

### 步骤4:训练循环

完整的食谱:一个通过数据,每批次的梯度,每期的时间表.

> 完整方案:对数据进行一次遍历,每个批量计算一次梯度,每个时代调度一次学习率.

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import SGD
from torch.optim.lr_scheduler import CosineAnnealingLR

def train_one_epoch(model, loader, optimizer, device, num_classes, use_mixup=True):
    model.train()
    total, correct, loss_sum = 0, 0, 0.0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        if use_mixup:
            x_m, y_soft = mixup_batch(x, y, num_classes)
            logits = model(x_m)
            loss = soft_cross_entropy(logits, y_soft)
        else:
            logits = model(x)
            loss = nn.functional.cross_entropy(logits, y, label_smoothing=0.1)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss_sum += loss.item() * x.size(0)
        total += x.size(0)
        # Training accuracy vs the un-mixed labels `y` is only an approximation
        # when mixup is on (the model saw soft targets, not y). Treat it as a
        # rough progress signal; rely on val accuracy for real performance.
        with torch.no_grad():
            pred = logits.argmax(dim=-1)
            correct += (pred == y).sum().item()
    return loss_sum / total, correct / total


@torch.no_grad()
def evaluate(model, loader, device, num_classes):
    model.eval()
    total, correct = 0, 0
    loss_sum = 0.0
    cm = torch.zeros(num_classes, num_classes, dtype=torch.long)
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        loss = nn.functional.cross_entropy(logits, y)
        pred = logits.argmax(dim=-1)
        for t, p in zip(y.cpu(), pred.cpu()):
            cm[t, p] += 1
        loss_sum += loss.item() * x.size(0)
        total += x.size(0)
        correct += (pred == y).sum().item()
    return loss_sum / total, correct / total, cm
```

每次写训练循环时,你检查的五种不变:

> 每次写训练循环检查的五个不变量:

1. `model.train()`在培训之前,`model.eval()`在评估之前,  转移退出和批量规范行为.
2. `.zero_grad()`在之前`.backward()`现在,我们要去.
3. `.item()`没有什么能让计算图保持活力.
4. `@torch.no_grad()`节省记忆和时间,防止微妙的事故.
5.                                                                                                                                                                                                                                                               

### 步骤5: 组合

使用`TinyResNet`根据前一课,训练几个时代,评估.

> 使用上一课的`TinyResNet`训练几个时代,评估.

```python
from main import synthetic_cifar, ArrayDataset
from main import standardize, random_hflip, random_crop, compose
from main import mixup_batch, soft_cross_entropy
from main import train_one_epoch, evaluate
# TinyResNet comes from the previous lesson (03-cnns-lenet-to-resnet).
# Adjust the import path to wherever you stored the previous lesson's code.
from cnns_lenet_to_resnet import TinyResNet  # example placeholder

X, Y = synthetic_cifar(num_per_class=500)
split = int(0.9 * len(X))
X_train, Y_train = X[:split], Y[:split]
X_val, Y_val = X[split:], Y[split:]

mean = [0.5, 0.5, 0.5]
std = [0.25, 0.25, 0.25]
train_tf = compose(random_hflip(), random_crop(pad=4), standardize(mean, std))
eval_tf = standardize(mean, std)

train_ds = ArrayDataset(X_train, Y_train, transform=train_tf)
val_ds = ArrayDataset(X_val, Y_val, transform=eval_tf)

train_loader = DataLoader(train_ds, batch_size=128, shuffle=True, num_workers=0)
val_loader = DataLoader(val_ds, batch_size=256, shuffle=False, num_workers=0)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = TinyResNet(num_classes=10).to(device)
optimizer = SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=5e-4, nesterov=True)
scheduler = CosineAnnealingLR(optimizer, T_max=10)

for epoch in range(10):
    tr_loss, tr_acc = train_one_epoch(model, train_loader, optimizer, device, 10, use_mixup=True)
    va_loss, va_acc, _ = evaluate(model, val_loader, device, 10)
    scheduler.step()
    print(f"epoch {epoch:2d}  lr {scheduler.get_last_lr()[0]:.4f}  "
          f"train {tr_loss:.3f}/{tr_acc:.3f}  val {va_loss:.3f}/{va_acc:.3f}")
```

在合成数据集中,在五个时代内,这种验证准确性几乎达到完美,这就是点:管道正确,模型可以学习可学的东西.

> 在合成数据集中,在五个时代内就能达到接近完美的验证准确率,这就是重点:流水线是正确的,模型可以学到可学的事情.

### 步骤 6:阅读混矩阵

只有精度,它永远不会告诉你模型在哪里失败.

> 单独的准确率永远不会告诉你模型在哪里失败.

```python
def print_confusion(cm, labels=None):
    c = cm.shape[0]
    labels = labels or [str(i) for i in range(c)]
    print(f"{'':>6}" + "".join(f"{l:>5}" for l in labels))
    for i in range(c):
        row = cm[i].tolist()
        print(f"{labels[i]:>6}" + "".join(f"{v:>5}" for v in row))
    print()
    tp = cm.diag().float()
    fp = cm.sum(dim=0).float() - tp
    fn = cm.sum(dim=1).float() - tp
    prec = tp / (tp + fp).clamp_min(1)
    rec = tp / (tp + fn).clamp_min(1)
    f1 = 2 * prec * rec / (prec + rec).clamp_min(1e-9)
    for i in range(c):
        print(f"{labels[i]:>6}  prec {prec[i]:.3f}  rec {rec[i]:.3f}  f1 {f1[i]:.3f}")

_, _, cm = evaluate(model, val_loader, device, 10)
print_confusion(cm)
```

列是真实类,列是预测.在3级到5级之间,一个离线数量的集群意味着模型混了这两个,并为目标数据收集或类型特定增强提供了起点.

> 行是真类,列是预测. 类 3 和 5 之间非对角线数的聚集意味着模型混合了这两个类,并为您提供了针对性的数据收集或类别特定增强的起点.



## 用它实现框架

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


`torchvision`对于真正的CIFAR-10来说,全线是四条线加上训练循环.

> `torchview`对于真实CIFAR-10来说,完整的流水线是四行代码加上一个训练循环.

```python
from torchvision.datasets import CIFAR10
from torchvision.transforms import Compose, RandomCrop, RandomHorizontalFlip, ToTensor, Normalize

mean = (0.4914, 0.4822, 0.4465)
std = (0.2470, 0.2435, 0.2616)
train_tf = Compose([
    RandomCrop(32, padding=4, padding_mode="reflect"),
    RandomHorizontalFlip(),
    ToTensor(),
    Normalize(mean, std),
])
eval_tf = Compose([ToTensor(), Normalize(mean, std)])

train_ds = CIFAR10(root="./data", train=True,  download=True, transform=train_tf)
val_ds   = CIFAR10(root="./data", train=False, download=True, transform=eval_tf)
```

值得注意的是,平均/STD是**dataset-specific**计算在CIFAR-10训练集,而不是ImageNet,反射板是社区默认的作物政策.

> 两点注意事项:平均值/标准差是**数据集特定的**在CIFAR-10训练集中计算,而不是ImageNet反射填充是社区默认的剪裁策略――在这里复制粘贴ImageNet统计量将导致约1%的准确率泄漏,直到有人分析模型才被发现――


> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质量――标签工作室、CVAT是主流标签工具――在工业场景中,主动学习(主动学习) 可以减少标签成本:模型对不确定的样本请求人工标签,确定性的样本自动标签――

## 运送它.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


这一课产生了:

- `outputs/prompt-classifier-pipeline-auditor.md`一个提示,检查了上述五种变量的训练脚本,并发现了第一个违规行为.
- `outputs/skill-classification-diagnostics.md`一个技能,在一个混矩阵和一个类名单的情况下,总结每个类的失败并提出最具影响力的解决方案.

> **【中文解读】**练习题按照易/中/难 三个难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


## 练习题

1. **(Easy | 简单)**根据合成数据集,在5个时代中,使用和无混合的模型进行训练. 两者都进行了训练. 解释为什么与混合的训练损失更高,但对验证的精度相似或更好.
   分别使用有/无混 训练 5 个时代,绘制训练和验证损失曲线,解释为什么混的训练损失更高,但验证准确率不差――

2. **(Medium | 中等)**执行切割  在每个训练图像中零出一个随机8x8平方 并运行一个除除算与没有增长,hflip+crop,hflip+crop+cutout,hflip+crop+mixup. 报告每个图像的精度.
   实现切割 (随机遮 8x8 区域),对无增强,翻转+剪裁,翻转+剪裁+切割,切割,翻转+剪裁+混合四种方案做消融实验,报告验证准确率――

3. **(Hard | 困难)**建立一个CIFAR-100管道 (100类,相同输入尺寸) 并将ResNet-34训练运行在公布的准确度的1%内复制. 额外:扫描三个学习率和两个减重,登录到本地CSV,生成最终的混矩阵-顶部混表.
   建立CIFAR-100流水线(100类),复现ResNet-34的训练结果与公开准确率相差1%以内.进阶:搜索三种学习率和两种权重衰减,记录到CSV,生成混矩阵中最容易混的类别对──

## 关键词 关键词

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Logits | "Raw outputs" | The pre-softmax vector of C numbers per image; cross-entropy expects these, not softmaxed values | Logits：softmax 之前的原始输出向量，交叉熵直接接收它 |
| Cross-entropy | "The loss" | Negative log-probability of the correct class; combines log-softmax and NLL in one stable op | 交叉熵：正确类别的负对数概率，融合了 log-softmax 和 NLL |
| DataLoader | "The batcher" | Wraps a dataset with shuffling, batching, and (optional) multi-worker loading; gets blamed for half of training bugs | 数据加载器：封装数据集的打乱、分批、多进程加载 |
| Augmentation | "Random transforms" | Any pixel-level transform at training time that preserves the label; teaches invariances the CNN does not have natively | 数据增强：训练时保持标签不变的像素级变换，教会模型 CNN 天生不具备的不变性 |
| Mixup / Cutmix | "Mix two images" | Blend both inputs and labels so the classifier learns smooth interpolations instead of hard boundaries | Mixup/Cutmix：混合两张图像及其标签，让分类器学习平滑插值 |
| Label smoothing | "Softer targets" | Replace one-hot with (1-eps, eps/(C-1), ...); improves calibration and slightly boosts accuracy | 标签平滑：用软标签替代 one-hot，改善概率校准 |
| Top-k accuracy | "Top-5" | The correct class is in the k highest-probability predictions; used on datasets with genuinely ambiguous classes | Top-k 准确率：正确类别在前 k 个预测中即算对 |
| Confusion matrix | "Where errors live" | C x C table where entry (i, j) counts images of true class i predicted as j; diagonal is right, off-diagonal tells you what to fix | 混淆矩阵：C×C 表格，对角线是正确预测，非对角线揭示混淆的类别对 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [CS231n: Training Neural Networks](https://cs231n.github.io/neural-networks-3/) 仍然是单页的训练管道最清晰的巡回
- [Bag of Tricks for Image Classification (He et al., 2019)](https://arxiv.org/abs/1812.01187)每一个小技巧,总共增加3~4%的ResNet精度
- [mixup: Beyond Empirical Risk Minimization (Zhang et al., 2017)](https://arxiv.org/abs/1710.09412)原始混合论文;三个页的理论加上令人信服的实验
- [Why temperature scaling matters (Guo et al., 2017)](https://arxiv.org/abs/1706.04599)证明现代网络是错误校准的,并用一个尺度参数来固定它
