"""
图像基础 — 像素、通道与色彩空间 (Image Fundamentals — Pixels, Channels, Color Spaces)

核心概念：
- 图像本质上是光线采样的张量（多维数组），每个像素包含一个或多个通道值
- HWC (高×宽×通道) 是 PIL/OpenCV 的默认格式，CHW (通道×高×宽) 是 PyTorch 的格式
- 预处理流水线：解码 → 色彩空间转换 → 缩放 → 归一化 → 标准化 → 布局转换

AI 对应：
- 所有计算机视觉模型（CNN、ViT、YOLO、Stable Diffusion）都依赖正确的图像预处理
- ImageNet 标准化参数 (mean/std) 是几乎所有预训练模型的基础
- 数据格式错误是视觉工程中最常见的 "静默失败" 来源
"""

import numpy as np
from PIL import Image
from io import BytesIO
from urllib.request import Request, urlopen


# ImageNet 标准化参数 — 几乎所有预训练视觉模型都使用这组数值
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)  # RGB 三通道均值
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)    # RGB 三通道标准差


def synthetic_image(height=128, width=192, seed=0):
    """生成合成测试图像，避免依赖外部文件
    AI 对应：模型测试和单元验证中常用的确定性数据生成方法
    """
    rng = np.random.default_rng(seed)
    yy, xx = np.meshgrid(np.linspace(0, 1, height), np.linspace(0, 1, width), indexing="ij")
    r = (np.sin(xx * 6) * 0.5 + 0.5) * 255  # 红色通道：正弦波图案
    g = (yy * 255)                             # 绿色通道：垂直渐变
    b = ((1 - yy) * xx * 255)                  # 蓝色通道：对角渐变
    noise = rng.normal(0, 6, (height, width, 3))  # 模拟传感器噪声
    rgb = np.stack([r, g, b], axis=-1) + noise     # 堆叠三通道并加噪
    return np.clip(rgb, 0, 255).astype(np.uint8)  # 裁剪到 [0,255] 并转为 uint8


def load_rgb(url, timeout=5):
    """从 URL 加载 RGB 图像，失败时返回合成图像
    AI 对应：实际部署中图像来源多样（URL、摄像头、文件系统），需要健壮的加载逻辑
    """
    try:
        req = Request(url, headers={"User-Agent": "ai-eng-course/1.0"})
        data = urlopen(req, timeout=timeout).read()
        img = Image.open(BytesIO(data)).convert("RGB")  # 强制转为 RGB（排除 RGBA/灰度等）
        return np.asarray(img)  # PIL Image → NumPy 数组（HWC 格式）
    except Exception:
        return synthetic_image()  # 网络失败时回退到合成图像


def inspect(arr, label="image"):
    """打印图像张量的关键属性：dtype、shape、值范围、通道均值
    AI 对应：调试视觉模型时的第一步——确认输入数据的格式和范围是否正确
    """
    if arr.ndim == 2:  # 灰度图像（无通道维度）
        print(f"[{label}] dtype={arr.dtype} shape={arr.shape} "
              f"min={arr.min()} max={arr.max()} mean={float(arr.mean()):.2f}")
        return
    print(f"[{label}] dtype={arr.dtype} shape={arr.shape} "
          f"min={arr.min()} max={arr.max()} "
          f"per-channel mean={arr.reshape(-1, arr.shape[-1]).mean(axis=0).round(2).tolist()}")


def hwc_to_chw(arr):
    """HWC → CHW 布局转换（PIL/OpenCV 格式 → PyTorch 格式）
    AI 对应：PyTorch 的 nn.Conv2d 期望输入为 (N,C,H,W) 格式
    """
    return arr.transpose(2, 0, 1)


def chw_to_hwc(arr):
    """CHW → HWC 布局转换（PyTorch 格式 → PIL/OpenCV 格式）"""
    return arr.transpose(1, 2, 0)


def rgb_to_grayscale(rgb):
    """RGB → 灰度转换（ITU-R BT.601 加权）
    人眼对绿色更敏感，所以绿色权重最高 (0.587)
    AI 对应：OCR、文档理解模型通常使用灰度输入以减少计算量
    """
    weights = np.array([0.299, 0.587, 0.114], dtype=np.float32)
    return (rgb.astype(np.float32) @ weights).astype(np.uint8)


def rgb_to_hsv(rgb):
    """RGB → HSV 色彩空间转换
    H (色相): 0-360度, S (饱和度): 0-1, V (明度): 0-1
    AI 对应：HSV 在颜色分割、肤色检测等传统 CV 任务中广泛使用
    """
    rgb_f = rgb.astype(np.float32) / 255.0  # 归一化到 [0,1]
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

    s = np.where(cmax > 0, delta / cmax, 0)  # 饱和度：色差占最大值的比例
    v = cmax                                    # 明度：即三通道最大值
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
    x = x * IMAGENET_STD + IMAGENET_MEAN         # 逆标准化
    x = np.clip(x * 255.0, 0, 255).astype(np.uint8)  # [0,1] → [0,255]
    return x


def resize_compare(arr, scale=3):
    """对比三种插值方法的缩放效果
    AI 对应：训练时用 bilinear，推理时也需匹配相同的插值方法
    """
    target = (arr.shape[1] * scale, arr.shape[0] * scale)  # 注意 PIL 的 size 是 (W, H)
    methods = {
        "nearest": Image.NEAREST,
        "bilinear": Image.BILINEAR,
        "bicubic": Image.BICUBIC,
    }
    return {
        name: np.asarray(Image.fromarray(arr).resize(target, filt))
        for name, filt in methods.items()
    }


def local_roughness(x):
    """计算图像局部粗糙度（梯度均值），用于量化插值效果"""
    gy = np.diff(x.astype(np.float32), axis=0)  # 垂直梯度
    gx = np.diff(x.astype(np.float32), axis=1)  # 水平梯度
    return float(np.abs(gy).mean() + np.abs(gx).mean())


def main():
    """主函数：演示图像加载、布局转换、色彩空间转换、标准化和缩放"""
    url = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/"
        "PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png"
    )
    arr = load_rgb(url)      # 加载图像（HWC, uint8）
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
    main()  # 运行图像基础演示：加载 → 检查 → 布局转换 → 色彩空间 → 标准化 → 缩放
