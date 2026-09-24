"""Runnable companion for the Image Fundamentals lesson.

图像基础 — 像素、通道与色彩空间 (Image Fundamentals — Pixels, Channels, Color Spaces)
核心概念：图像是光线采样的张量；HWC 是 PIL/OpenCV 的磁盘格式，CHW 是 PyTorch/cuDNN 的计算格式；
预处理流水线 = 解码 uint8 → /255 归一化 → ImageNet 标准化 → HWC→CHW；
最近邻/双线性/双三次插值都可以用端点对齐的采样坐标从零实现。
AI 应用对应：所有视觉模型（CNN、ViT、YOLO、Stable Diffusion）都依赖正确的图像预处理，
数据格式错误（uint8 vs float32、BGR vs RGB、HWC vs CHW）是视觉工程中最常见的 "静默失败"。

Builds a deterministic RGB image and transforms it as a NumPy tensor.
Implements nearest, bilinear, and bicubic resizing from scratch.
See ../docs/en.md for the derivations and production-library comparison.
"""

import numpy as np


# ImageNet 标准化参数 — 几乎所有预训练视觉模型都使用这组数值
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)  # RGB 三通道均值
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)    # RGB 三通道标准差


def synthetic_image(height=128, width=192, seed=0):
    """生成确定性合成 RGB 图像（uint8 HWC），无需网络和图像库即可离线复现
    AI 对应：模型测试和单元验证中常用的确定性数据生成方法
    """
    rng = np.random.default_rng(seed)
    yy, xx = np.meshgrid(np.linspace(0, 1, height), np.linspace(0, 1, width), indexing="ij")
    r = (np.sin(xx * 6) * 0.5 + 0.5) * 255  # 红色通道：正弦波图案
    g = (yy * 255)                           # 绿色通道：垂直渐变
    b = ((1 - yy) * xx * 255)                # 蓝色通道：对角渐变
    noise = rng.normal(0, 6, (height, width, 3))  # 模拟传感器噪声
    rgb = np.stack([r, g, b], axis=-1) + noise    # 堆叠三通道并加噪
    return np.clip(rgb, 0, 255).astype(np.uint8)  # 裁剪到 [0,255] 并转为 uint8


def inspect(arr, label="image"):
    """打印图像张量的关键属性：dtype、shape、值范围、通道均值
    AI 对应：调试视觉模型时的第一步——确认输入数据的格式和范围是否正确
    """
    if arr.ndim == 2:  # 灰度图像（无通道维度）
        print(
            f"[{label}] dtype={arr.dtype} shape={arr.shape} "
            f"min={arr.min()} max={arr.max()} mean={float(arr.mean()):.2f}"
        )
        return
    print(
        f"[{label}] dtype={arr.dtype} shape={arr.shape} "
        f"min={arr.min()} max={arr.max()} "
        f"per-channel mean="
        f"{arr.reshape(-1, arr.shape[-1]).mean(axis=0).round(2).tolist()}"
    )


def hwc_to_chw(arr):
    """HWC → CHW 布局转换（PIL/OpenCV 磁盘格式 → PyTorch 计算格式）
    AI 对应：PyTorch 的 nn.Conv2d 期望输入为 (N,C,H,W) 格式
    """
    return arr.transpose(2, 0, 1)


def chw_to_hwc(arr):
    """CHW → HWC 布局转换（PyTorch 格式 → PIL/OpenCV/显示格式）"""
    return arr.transpose(1, 2, 0)


def rgb_to_grayscale(rgb):
    """RGB → 灰度转换（ITU-R BT.601 加权）
    人眼对绿色更敏感，所以绿色权重最高 (0.587)
    AI 对应：OCR、文档理解模型通常使用灰度输入以减少计算量
    """
    weights = np.array([0.299, 0.587, 0.114], dtype=np.float32)  # 亮度加权系数
    return (rgb.astype(np.float32) @ weights).astype(np.uint8)   # 加权求和转灰度


def rgb_to_hsv(rgb):
    """RGB → HSV 色彩空间转换
    H (色相): 0-360度, S (饱和度): 0-1, V (明度): 0-1
    AI 对应：HSV 在颜色分割、肤色检测等传统 CV 任务中广泛使用
    """
    rgb_f = rgb.astype(np.float32) / 255.0  # 先归一化到 [0,1]
    r, g, b = rgb_f[..., 0], rgb_f[..., 1], rgb_f[..., 2]
    cmax = np.max(rgb_f, axis=-1)           # 三通道最大值
    cmin = np.min(rgb_f, axis=-1)           # 三通道最小值
    delta = cmax - cmin                     # 最大与最小之差（色差）

    h = np.zeros_like(cmax)
    mask = delta > 0  # 只有非灰色像素才有色相
    # 使用 argmax 代替浮点相等判断，避免边界情况
    argmax = np.argmax(rgb_f, axis=-1)
    rmax = mask & (argmax == 0)
    gmax = mask & (argmax == 1)
    bmax = mask & (argmax == 2)
    h[rmax] = ((g[rmax] - b[rmax]) / delta[rmax]) % 6   # 红色为主时的色相
    h[gmax] = ((b[gmax] - r[gmax]) / delta[gmax]) + 2   # 绿色为主时的色相
    h[bmax] = ((r[bmax] - g[bmax]) / delta[bmax]) + 4   # 蓝色为主时的色相
    h = h * 60.0  # 转换为角度 [0, 360]

    s = np.divide(delta, cmax, out=np.zeros_like(delta), where=cmax > 0)  # 饱和度：色差占最大值的比例
    v = cmax                                                              # 明度：即三通道最大值
    return np.stack([h, s, v], axis=-1)


def preprocess_imagenet(rgb_uint8):
    """ImageNet 标准预处理：uint8 HWC → float32 CHW（标准化后）
    AI 对应：几乎所有 torchvision 预训练模型的输入要求
    """
    x = rgb_uint8.astype(np.float32) / 255.0   # [0,255] → [0,1]
    x = (x - IMAGENET_MEAN) / IMAGENET_STD      # 标准化：约 [-2, +2]
    x = x.transpose(2, 0, 1)                    # HWC → CHW
    return x


def deprocess_imagenet(chw_float32):
    """预处理的逆操作：CHW float32 → HWC uint8（用于可视化模型输出）"""
    x = chw_float32.transpose(1, 2, 0)          # CHW → HWC
    x = x * IMAGENET_STD + IMAGENET_MEAN        # 逆标准化
    x = np.clip(x * 255.0, 0, 255).astype(np.uint8)  # [0,1] → [0,255]
    return x


def resize_coordinates(source_length, target_length):
    """生成端点对齐的采样坐标：首尾源像素固定，中间均匀分布
    这是三种插值方法共用的坐标系统，保证缩放边界不漂移
    """
    if target_length < 1:
        raise ValueError("target length must be positive")
    if source_length < 1:
        raise ValueError("source length must be positive")
    if target_length == 1:
        return np.zeros(1, dtype=np.float32)
    return np.linspace(0, source_length - 1, target_length, dtype=np.float32)


def nearest_resize(arr, target_height, target_width):
    """最近邻缩放：每个输出坐标四舍五入到最近的源像素
    AI 对应：分割掩码/标签图缩放时的唯一正确选择（不产生新类别值）
    """
    y = np.rint(resize_coordinates(arr.shape[0], target_height)).astype(int)
    x = np.rint(resize_coordinates(arr.shape[1], target_width)).astype(int)
    return arr[y[:, None], x[None, :]]  # fancy indexing 一次性 gather 全图


def bilinear_resize(arr, target_height, target_width):
    """双线性缩放：找周围 4 个像素，按距离加权混合（水平两次 + 垂直一次，可分离）
    AI 对应：训练时图像增广的默认插值方法
    """
    y = resize_coordinates(arr.shape[0], target_height)  # 浮点采样坐标
    x = resize_coordinates(arr.shape[1], target_width)
    y0 = np.floor(y).astype(int)   # 上侧邻居行
    x0 = np.floor(x).astype(int)   # 左侧邻居列
    y1 = np.minimum(y0 + 1, arr.shape[0] - 1)  # 下侧邻居（边界截断）
    x1 = np.minimum(x0 + 1, arr.shape[1] - 1)  # 右侧邻居（边界截断）
    wy = (y - y0)[:, None, None]  # 垂直插值权重
    wx = (x - x0)[None, :, None]  # 水平插值权重

    source = arr.astype(np.float32)
    top = source[y0[:, None], x0[None, :]] * (1 - wx)     # 上行两次水平插值
    top += source[y0[:, None], x1[None, :]] * wx
    bottom = source[y1[:, None], x0[None, :]] * (1 - wx)  # 下行两次水平插值
    bottom += source[y1[:, None], x1[None, :]] * wx
    result = top * (1 - wy) + bottom * wy                 # 垂直方向再插值一次
    return np.clip(np.rint(result), 0, 255).astype(arr.dtype)


def cubic_weight(distance, tension=-0.5):
    """Catmull-Rom 三次核权重：|x|<=1 用内侧多项式，1<|x|<2 用外侧多项式，其余为 0"""
    x = np.abs(distance)
    inner = (tension + 2) * x**3 - (tension + 3) * x**2 + 1
    outer = tension * x**3 - 5 * tension * x**2 + 8 * tension * x - 4 * tension
    return np.where(x <= 1, inner, np.where(x < 2, outer, 0.0))


def bicubic_resize(arr, target_height, target_width):
    """双三次缩放：每轴取 4 个邻居、用 Catmull-Rom 核加权（可分离：先水平后垂直）
    AI 对应：图像放大/超分辨率任务中比双线性更锐利的经典选择
    """
    y = resize_coordinates(arr.shape[0], target_height)
    x = resize_coordinates(arr.shape[1], target_width)
    offsets = np.arange(-1, 3)  # 基础像素左右/上下各扩展的 4 个邻居偏移

    # 水平方向：4 tap 三次加权
    x_base = np.floor(x).astype(int)
    x_neighbors = x_base[:, None] + offsets[None, :]
    x_weights = cubic_weight(x[:, None] - x_neighbors)
    x_weights /= x_weights.sum(axis=1, keepdims=True)  # 权重归一化
    x_indices = np.clip(x_neighbors, 0, arr.shape[1] - 1)  # 边界截断

    source = arr.astype(np.float32)
    horizontal = np.zeros((arr.shape[0], target_width, arr.shape[2]), dtype=np.float32)
    for tap in range(4):
        horizontal += source[:, x_indices[:, tap], :] * x_weights[None, :, tap, None]

    # 垂直方向：对水平结果再做 4 tap 三次加权
    y_base = np.floor(y).astype(int)
    y_neighbors = y_base[:, None] + offsets[None, :]
    y_weights = cubic_weight(y[:, None] - y_neighbors)
    y_weights /= y_weights.sum(axis=1, keepdims=True)  # 权重归一化
    y_indices = np.clip(y_neighbors, 0, arr.shape[0] - 1)  # 边界截断

    result = np.zeros((target_height, target_width, arr.shape[2]), dtype=np.float32)
    for tap in range(4):
        result += horizontal[y_indices[:, tap], :, :] * y_weights[:, tap, None, None]
    return np.clip(np.rint(result), 0, 255).astype(arr.dtype)


def resize_compare(arr, scale=3):
    """对比三种插值方法的缩放效果（最近邻 / 双线性 / 双三次，全部从零实现）
    AI 对应：训练时用 bilinear，推理部署时必须匹配训练时相同的插值方法
    """
    if not isinstance(scale, int) or scale < 1:
        raise ValueError("scale must be a positive integer")
    target_height = arr.shape[0] * scale
    target_width = arr.shape[1] * scale
    return {
        "nearest": nearest_resize(arr, target_height, target_width),
        "bilinear": bilinear_resize(arr, target_height, target_width),
        "bicubic": bicubic_resize(arr, target_height, target_width),
    }


def local_roughness(x):
    """计算图像局部粗糙度（梯度均值），用于量化插值效果差异"""
    gy = np.diff(x.astype(np.float32), axis=0)  # 垂直梯度
    gx = np.diff(x.astype(np.float32), axis=1)  # 水平梯度
    return float(np.abs(gy).mean() + np.abs(gx).mean())


def main():
    """主函数：合成图像 → 检查 → 布局转换 → 色彩空间 → 标准化 → 三种插值对比"""
    arr = synthetic_image()  # 合成图像（HWC, uint8）
    print("source: deterministic synthetic RGB image (offline)")
    inspect(arr, "raw")      # 检查原始图像属性

    # 布局转换演示
    chw = hwc_to_chw(arr)
    print(f"HWC shape: {arr.shape}   CHW shape: {chw.shape}")

    # 色彩空间转换
    gray = rgb_to_grayscale(arr)
    hsv = rgb_to_hsv(arr)
    print(f"grayscale shape: {gray.shape}")
    print(f"hsv hue range:   [{hsv[..., 0].min():.1f}, {hsv[..., 0].max():.1f}] deg")
    print(f"hsv sat range:   [{hsv[..., 1].min():.2f}, {hsv[..., 1].max():.2f}]")
    print(f"hsv val range:   [{hsv[..., 2].min():.2f}, {hsv[..., 2].max():.2f}]")

    # ImageNet 标准化预处理
    x = preprocess_imagenet(arr)
    print(f"preprocessed shape: {x.shape}  dtype: {x.dtype}")
    print(f"per-channel mean: {x.mean(axis=(1, 2)).round(3).tolist()}")
    print(f"per-channel std:  {x.std(axis=(1, 2)).round(3).tolist()}")

    # 验证预处理/逆预处理的往返一致性
    roundtrip = deprocess_imagenet(x)
    max_diff = int(np.abs(roundtrip.astype(int) - arr.astype(int)).max())
    print(f"roundtrip max pixel diff: {max_diff}")  # 应为 0 或 1

    # 对比三种插值方法的缩放效果
    for name, out in resize_compare(arr, scale=3).items():
        print(f"{name:>8}  shape={out.shape}  roughness={local_roughness(out):6.2f}")


if __name__ == "__main__":
    main()  # 运行图像基础演示：合成 → 检查 → 布局转换 → 色彩空间 → 标准化 → 插值对比
