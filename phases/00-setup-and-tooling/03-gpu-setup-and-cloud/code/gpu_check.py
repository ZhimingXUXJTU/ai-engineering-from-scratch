"""
GPU 检测与基准测试脚本 — 检查 GPU 可用性并对比 CPU/GPU 矩阵乘法速度。
核心概念: CUDA 并行计算、显存(VRAM)估算、fp16 半精度。
AI 对应: GPU 加速是训练深度学习模型的基础，本脚本帮你验证环境是否就绪。
"""
import time
import sys


def check_gpu():
    """检测 GPU 状态，运行 CPU vs GPU 矩阵乘法基准测试。"""
    try:
        import torch
    except ImportError:
        print("PyTorch not installed. Run: pip install torch")  # PyTorch 未安装
        return

    print("=== GPU Check ===\n")
    print(f"PyTorch version: {torch.__version__}")  # PyTorch 版本
    print(f"CUDA available: {torch.cuda.is_available()}")  # CUDA 是否可用

    if not torch.cuda.is_available():
        print("\nNo GPU detected. That's fine for most lessons.")  # 没有 GPU，大部分课程仍可运行
        print("For GPU-heavy lessons, use Google Colab (free).")  # 需要时可使用 Colab
        return

    print(f"CUDA version: {torch.version.cuda}")  # CUDA 版本
    print(f"GPU: {torch.cuda.get_device_name(0)}")  # GPU 型号名称

    props = torch.cuda.get_device_properties(0)  # 获取 GPU 属性
    print(f"Memory: {props.total_memory / 1e9:.1f} GB")  # 显存大小
    print(f"Compute capability: {props.major}.{props.minor}")  # 计算能力版本

    # --- CPU vs GPU 矩阵乘法基准测试 ---
    print("\n=== CPU vs GPU Benchmark ===\n")
    size = 4000  # 矩阵尺寸

    a = torch.randn(size, size)  # 随机矩阵 A
    b = torch.randn(size, size)  # 随机矩阵 B

    start = time.time()
    _ = a @ b  # CPU 矩阵乘法
    cpu_time = time.time() - start
    print(f"CPU matrix multiply ({size}x{size}): {cpu_time:.3f}s")  # CPU 耗时

    a_gpu = a.to("cuda")  # 将矩阵移到 GPU
    b_gpu = b.to("cuda")
    torch.cuda.synchronize()  # 同步，确保数据传输完成

    start = time.time()
    _ = a_gpu @ b_gpu  # GPU 矩阵乘法
    torch.cuda.synchronize()  # 同步，确保计算完成
    gpu_time = time.time() - start
    print(f"GPU matrix multiply ({size}x{size}): {gpu_time:.3f}s")  # GPU 耗时
    print(f"Speedup: {cpu_time / gpu_time:.0f}x")  # 加速倍数

    # 估算 fp16 半精度下能装下多少参数的模型
    vram_gb = props.total_memory / 1e9  # 显存 GB
    params_fp16 = vram_gb * 1e9 / 2  # fp16 每参数 2 字节
    params_billions = params_fp16 / 1e9
    print(f"\nEstimated max model size (fp16): ~{params_billions:.0f}B parameters")  # 估算最大模型参数量


if __name__ == "__main__":
    check_gpu()  # 运行 GPU 检测
