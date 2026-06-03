"""
CNN 架构演进：从 LeNet 到 ResNet (CNNs — LeNet to ResNet)

核心概念：
- LeNet-5 (1998)：定义了 CNN 的基本模板——卷积+池化+全连接
- AlexNet (2012)：ReLU 激活 + Dropout + 深度，引爆深度学习革命
- VGG (2014)：3x3 卷积极致堆叠，简洁即美
- Inception (2014)：多尺度并行滤波
- ResNet (2015)：残差跳跃连接 y=F(x)+x，解决了深度网络的退化问题

AI 对应：
- 残差连接从 ResNet 扩展到所有 Transformer（GPT、BERT、Claude）
- ResNet 骨干网络是目标检测（YOLO/Faster R-CNN）和语义分割（U-Net）的基础
- 迁移学习：预训练 ResNet + 自定义头 = 快速解决新任务
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class LeNet5(nn.Module):
    """LeNet-5 (1998)：第一个成功的卷积神经网络
    模板：卷积 → 池化 → 卷积 → 池化 → 全连接 × 3
    AI 对应：所有现代 CNN 都继承了这个基本架构，仅 6 万参数
    """
    def __init__(self, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5)     # 灰度图 → 6通道
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)    # 6通道 → 16通道
        self.pool = nn.AvgPool2d(2)                      # 平均池化下采样
        self.fc1 = nn.Linear(16 * 5 * 5, 120)            # 展平后全连接
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)             # 输出 10 类

    def forward(self, x):
        x = self.pool(torch.tanh(self.conv1(x)))  # 卷积+tanh激活+池化
        x = self.pool(torch.tanh(self.conv2(x)))  # 卷积+tanh激活+池化
        x = torch.flatten(x, 1)                    # 展平为向量
        x = torch.tanh(self.fc1(x))
        x = torch.tanh(self.fc2(x))
        return self.fc3(x)                         # 输出 logits


class VGGBlock(nn.Module):
    """VGG 块：两个 3x3 卷积 + BN + ReLU + 最大池化
    AI 对应：VGG 证明了 "用 3x3 堆叠代替大核" 的有效性
    """
    def __init__(self, in_c, out_c):
        super().__init__()
        self.conv1 = nn.Conv2d(in_c, out_c, kernel_size=3, padding=1)   # 3x3 卷积
        self.bn1 = nn.BatchNorm2d(out_c)                                 # 批归一化
        self.conv2 = nn.Conv2d(out_c, out_c, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(out_c)
        self.pool = nn.MaxPool2d(2)  # 2x2 最大池化，空间尺寸减半

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))  # 卷积 → BN → ReLU
        x = F.relu(self.bn2(self.conv2(x)))  # 卷积 → BN → ReLU
        return self.pool(x)                    # 池化下采样


class MiniVGG(nn.Module):
    """MiniVGG：VGG 风格的轻量版，适合 CIFAR 等小尺寸输入
    三个 VGG 块逐步增加通道数：32 → 64 → 128
    """
    def __init__(self, num_classes=10):
        super().__init__()
        self.stack = nn.Sequential(
            VGGBlock(3, 32),    # 输入 RGB 3通道 → 32通道
            VGGBlock(32, 64),   # 32 → 64通道
            VGGBlock(64, 128),  # 64 → 128通道
        )
        self.head = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),  # 全局平均池化，忽略空间尺寸
            nn.Flatten(),              # 展平
            nn.Linear(128, num_classes),  # 分类器
        )

    def forward(self, x):
        return self.head(self.stack(x))


class BasicBlock(nn.Module):
    """ResNet 基本块：两个 3x3 卷积 + 跳跃连接
    核心公式：y = F(x) + x（残差连接）
    AI 对应：这个结构是 ResNet-18/34 的核心，残差思想扩展到了所有 Transformer
    """
    def __init__(self, in_c, out_c, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_c, out_c, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_c)
        self.conv2 = nn.Conv2d(out_c, out_c, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_c)
        # 当维度不匹配时（步幅或通道数变化），用 1x1 卷积调整跳跃连接
        if stride != 1 or in_c != out_c:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_c, out_c, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_c),
            )
        else:
            self.shortcut = nn.Identity()  # 维度匹配时直接传递

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))   # 卷积 → BN → ReLU
        out = self.bn2(self.conv2(out))          # 卷积 → BN（不加 ReLU）
        out = out + self.shortcut(x)             # 残差连接：F(x) + x
        return F.relu(out)                       # 最后加 ReLU


class TinyResNet(nn.Module):
    """迷你 ResNet：4 组 BasicBlock，适合 CIFAR 尺寸输入
    结构：stem → [32ch, s=1] → [64ch, s=2] → [128ch, s=2] → [256ch, s=2] → head
    AI 对应：这是 ResNet-18 的缩小版，展示了残差网络的标准构建模式
    """
    def __init__(self, num_classes=10):
        super().__init__()
        self.stem = nn.Sequential(  # 输入处理层（茎部）
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
        )
        self.layer1 = self._make_group(32, 32, num_blocks=2, stride=1)   # 32通道，不降采样
        self.layer2 = self._make_group(32, 64, num_blocks=2, stride=2)   # 64通道，降采样
        self.layer3 = self._make_group(64, 128, num_blocks=2, stride=2)  # 128通道，降采样
        self.layer4 = self._make_group(128, 256, num_blocks=2, stride=2) # 256通道，降采样
        self.head = nn.Sequential(  # 分类头
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(256, num_classes),
        )

    def _make_group(self, in_c, out_c, num_blocks, stride):
        """构建一组 BasicBlock：第一个块处理降采样，后续块保持尺寸"""
        blocks = [BasicBlock(in_c, out_c, stride=stride)]
        for _ in range(num_blocks - 1):
            blocks.append(BasicBlock(out_c, out_c, stride=1))
        return nn.Sequential(*blocks)

    def forward(self, x):
        x = self.stem(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        return self.head(x)


def summary(name, net, x):
    """打印模型摘要：名称、输入输出形状、参数量"""
    net.eval()
    with torch.no_grad():
        y = net(x)
    params = sum(p.numel() for p in net.parameters())
    trainable = sum(p.numel() for p in net.parameters() if p.requires_grad)
    print(f"{name:12s}  input {tuple(x.shape)} -> output {tuple(y.shape)}   "
          f"params {params:>10,}   trainable {trainable:>10,}")


def per_group_params(net):
    """按模块分组统计参数量"""
    return {name: sum(p.numel() for p in mod.parameters()) for name, mod in net.named_children()}


def main():
    """主函数：对比三种 CNN 架构的参数量和输出形状"""
    summary("LeNet5",     LeNet5(),     torch.randn(1, 1, 32, 32))
    summary("MiniVGG",    MiniVGG(),    torch.randn(1, 3, 32, 32))
    summary("TinyResNet", TinyResNet(), torch.randn(1, 3, 32, 32))

    # 展示 TinyResNet 各模块的参数分布
    print("\nTinyResNet parameters by group:")
    for name, n in per_group_params(TinyResNet()).items():
        print(f"  {name:8s}  {n:>10,}")


if __name__ == "__main__":
    main()  # 运行 CNN 架构对比：LeNet → VGG → ResNet
