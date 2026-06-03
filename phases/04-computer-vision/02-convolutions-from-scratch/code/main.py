"""
从零实现卷积 (Convolutions from Scratch)

核心概念：
- 卷积是共享权重的小型全连接层，在图像上滑动计算点积
- 关键公式：H_out = floor((H - K + 2P) / S) + 1
- im2col 技巧：将卷积转化为矩阵乘法，是 GPU 加速的核心原理
- 堆叠多层 3x3 卷积可以高效扩大感受野

AI 对应：
- CNN 是自动驾驶（YOLO）、人脸识别（FaceNet）、医学影像分析的基础
- im2col + GEMM 是 cuDNN 等深度学习库的底层实现方式
- 深度可分离卷积（Depthwise Conv）是 MobileNet、ConvNeXt 的核心组件
"""

import numpy as np


def pad2d(x, p):
    """对 2D 特征图进行零填充
    AI 对应：保持特征图尺寸不变（same padding），使网络可以堆叠更多层
    """
    if p == 0:
        return x
    h, w = x.shape[-2:]  # 支持任意前导维度：(H,W), (C,H,W), (N,C,H,W)
    out = np.zeros(x.shape[:-2] + (h + 2 * p, w + 2 * p), dtype=x.dtype)
    out[..., p:p + h, p:p + w] = x
    return out


def output_size(h_in, k, p, s):
    """计算卷积输出尺寸：H_out = floor((H - K + 2P) / S) + 1
    这是设计任何 CNN 架构时最常用的公式
    """
    return (h_in + 2 * p - k) // s + 1


def conv2d_naive(x, w, b=None, stride=1, padding=0):
    """嵌套循环实现 2D 卷积（参考实现，慢但清晰）
    AI 对应：这就是 torch.nn.functional.conv2d 的数学原理
    """
    c_in, h, w_in = x.shape           # 输入：通道数、高、宽
    c_out, c_in_w, kh, kw = w.shape   # 权重：输出通道、输入通道、核高、核宽
    assert c_in == c_in_w              # 通道数必须匹配

    x_pad = pad2d(x, padding)         # 零填充
    h_out = output_size(h, kh, padding, stride)   # 计算输出高度
    w_out = output_size(w_in, kw, padding, stride) # 计算输出宽度

    out = np.zeros((c_out, h_out, w_out), dtype=np.float32)
    for oc in range(c_out):            # 遍历每个输出通道
        for i in range(h_out):         # 遍历输出行
            for j in range(w_out):     # 遍历输出列
                hs = i * stride        # 输入中的起始行位置
                ws = j * stride        # 输入中的起始列位置
                patch = x_pad[:, hs:hs + kh, ws:ws + kw]  # 提取感受野窗口
                out[oc, i, j] = np.sum(patch * w[oc])      # 点积求和
        if b is not None:
            out[oc] += b[oc]           # 加偏置
    return out


def im2col(x, kh, kw, stride=1, padding=0):
    """im2col：将每个感受野窗口展开为一列，使卷积变成矩阵乘法
    AI 对应：cuDNN 的 GEMM-based 卷积就是这个原理的优化版本
    """
    c_in, h, w = x.shape
    x_pad = pad2d(x, padding)
    h_out = output_size(h, kh, padding, stride)
    w_out = output_size(w, kw, padding, stride)

    cols = np.zeros((c_in * kh * kw, h_out * w_out), dtype=x.dtype)  # 每列是一个感受野
    col = 0
    for i in range(h_out):
        for j in range(w_out):
            hs = i * stride
            ws = j * stride
            patch = x_pad[:, hs:hs + kh, ws:ws + kw]
            cols[:, col] = patch.reshape(-1)  # 展平为列向量
            col += 1
    return cols, h_out, w_out


def conv2d_im2col(x, w, b=None, stride=1, padding=0):
    """im2col + 矩阵乘法实现快速卷积
    核心思想：W_flat @ cols = 输出，一次矩阵乘法完成所有位置的卷积
    """
    c_out, c_in, kh, kw = w.shape
    cols, h_out, w_out = im2col(x, kh, kw, stride, padding)
    w_flat = w.reshape(c_out, -1)   # 权重展平：(C_out, C_in*K*K)
    out = w_flat @ cols              # 一次矩阵乘法完成卷积
    if b is not None:
        out += b[:, None]            # 加偏置
    return out.reshape(c_out, h_out, w_out)  # 恢复空间维度


def receptive_field(layers):
    """计算堆叠卷积层的感受野大小
    RF = 1 + Σ(k_i - 1) * Π(s_0..s_{i-1})
    AI 对应：感受野决定了每个输出神经元"看到"的输入区域大小
    """
    rf = 1
    stride_prod = 1  # 累积步幅乘积
    for k, s in layers:
        rf = rf + (k - 1) * stride_prod  # 感受野随层数增长
        stride_prod *= s
    return rf


# 五种经典卷积核——CNN 第一个卷积层学到的特征与这些手工核高度相似
KERNELS = {
    "identity": np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float32),  # 恒等（不变）
    "blur_3x3": np.ones((3, 3), dtype=np.float32) / 9.0,                         # 均值模糊
    "sharpen": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32),  # 锐化
    "sobel_x": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32),   # 垂直边缘
    "sobel_y": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32),   # 水平边缘
}


def apply_kernel(img2d, kernel):
    """将手工核应用到灰度图像上"""
    x = img2d[None].astype(np.float32)   # 添加通道维度
    w = kernel[None, None]                # 添加 batch 和通道维度
    return conv2d_im2col(x, w, padding=1)[0]


def synthetic_step_image(size=16):
    """生成合成阶梯图像（左暗右亮），用于验证边缘检测核"""
    img = np.zeros((1, size, size), dtype=np.float32)
    img[:, :, size // 2:] = 1.0  # 右半部分设为 1.0
    return img


def test_against_naive():
    """验证 im2col 实现与 naive 实现的一致性"""
    rng = np.random.default_rng(0)
    x = rng.normal(0, 1, (3, 16, 16)).astype(np.float32)    # 3通道 16x16 输入
    w = rng.normal(0, 1, (8, 3, 3, 3)).astype(np.float32)    # 8个 3x3 核
    b = rng.normal(0, 1, (8,)).astype(np.float32)             # 偏置

    y_naive = conv2d_naive(x, w, b, padding=1)
    y_im2col = conv2d_im2col(x, w, b, padding=1)
    diff = float(np.max(np.abs(y_naive - y_im2col)))  # 应约 1e-5（浮点误差）
    return y_naive.shape, diff


def main():
    """主函数：验证卷积实现、演示经典核、计算输出尺寸和感受野"""
    shape, diff = test_against_naive()
    print(f"conv equivalence: naive vs im2col     shape={shape}   max|diff|={diff:.2e}")

    # 用 Sobel 核检测阶梯图像的垂直边缘
    x = synthetic_step_image()
    y = apply_kernel(x[0], KERNELS["sobel_x"])
    print("\nsobel_x on a left/right step image (first five rows):")
    print(y[:5].round(1))

    # 输出尺寸速查表
    print("\noutput size cheatsheet  (H=32):")
    for k, p, s in [(3, 0, 1), (3, 1, 1), (3, 1, 2), (2, 0, 2), (7, 3, 2)]:
        print(f"  K={k} P={p} S={s}  ->  H_out={output_size(32, k, p, s)}")

    # 感受野随层数增长
    stacks = [
        [(3, 1)],
        [(3, 1), (3, 1)],
        [(3, 1), (3, 1), (3, 1)],
        [(3, 1), (3, 2), (3, 1), (3, 2)],
    ]
    print("\nreceptive field grows with depth:")
    for stack in stacks:
        print(f"  layers={stack}  ->  RF={receptive_field(stack)}")


if __name__ == "__main__":
    main()  # 运行卷积从零实现演示：验证一致性 → 经典核 → 尺寸公式 → 感受野
