"""
AI 调试与性能分析工具包 — 张量检查、NaN 检测、性能计时、内存追踪、梯度健康检查。
核心概念: 张量形状/类型/设备检查、NaN/Inf 检测、内存分析、GPU 显存管理。
AI 对应: AI 调试最大的挑战是"静默失败"——代码不报错但结果错误。本工具帮助你在训练过程中发现这些问题。
"""
import sys
import time
import tracemalloc
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

try:
    import torch
    import torch.nn as nn
    HAS_TORCH = True  # PyTorch 可用
except ImportError:
    HAS_TORCH = False


def debug_print(name, tensor):
    """打印张量的关键信息: 形状、数据类型、设备、统计值、是否包含 NaN。"""
    print(f"  {name}: shape={tensor.shape}, dtype={tensor.dtype}, "
          f"device={tensor.device}, "
          f"min={tensor.min().item():.4f}, max={tensor.max().item():.4f}, "
          f"mean={tensor.mean().item():.4f}, "
          f"has_nan={tensor.isnan().any().item()}")  # NaN 检测——AI 调试中最常见的问题


class Timer:
    """上下文管理器，用于测量代码块执行时间。"""
    def __init__(self, name=""):
        self.name = name
        self.elapsed = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start
        print(f"  [{self.name}] {self.elapsed:.4f}s")


def check_shapes(model, sample_input):
    """使用 PyTorch Hook 逐层检查模型的输入/输出形状。"""
    print(f"  Input: {sample_input.shape}")
    hooks = []

    def make_hook(name):
        def hook(module, inp, out):
            in_shape = inp[0].shape if isinstance(inp, tuple) else inp.shape
            out_shape = out.shape if hasattr(out, "shape") else type(out).__name__
            print(f"    {name}: {in_shape} -> {out_shape}")  # 逐层打印形状变换
        return hook

    for name, module in model.named_modules():
        if name:
            hooks.append(module.register_forward_hook(make_hook(name)))

    with torch.no_grad():
        model(sample_input)

    for h in hooks:
        h.remove()


def detect_nan(model, loss, step):
    """检测 loss 是否为 NaN，并定位产生 NaN 梯度的参数。"""
    if torch.isnan(loss):  # loss 为 NaN 是训练崩溃的典型信号
        print(f"  NaN loss detected at step {step}")
        for name, param in model.named_parameters():
            if param.grad is not None:
                if torch.isnan(param.grad).any():
                    print(f"    NaN gradient in {name}")  # 该参数的梯度包含 NaN
                if torch.isinf(param.grad).any():
                    print(f"    Inf gradient in {name}")  # 该参数的梯度包含 Inf
        return True
    return False


def check_devices(model, *tensors):
    """检查模型和张量是否在同一设备上（CPU/GPU 不匹配是常见 bug）。"""
    model_device = next(model.parameters()).device
    print(f"  Model device: {model_device}")
    for i, t in enumerate(tensors):
        status = "OK" if t.device == model_device else "MISMATCH"  # 设备不匹配
        print(f"    Tensor {i}: {t.device} [{status}]")


def check_gradient_health(model):
    """检查模型梯度的健康状况：过大（梯度爆炸）、为零（梯度消失）、总范数。"""
    total_norm = 0.0
    for name, param in model.named_parameters():
        if param.grad is not None:
            grad_norm = param.grad.data.norm(2).item()
            total_norm += grad_norm ** 2
            if grad_norm > 100:
                print(f"    WARNING: large gradient in {name}: {grad_norm:.2f}")  # 梯度爆炸
            if grad_norm == 0:
                print(f"    WARNING: zero gradient in {name}")  # 梯度消失
    total_norm = total_norm ** 0.5
    print(f"  Total gradient norm: {total_norm:.4f}")  # 总梯度范数
    return total_norm


def demo_print_debugging():
    """演示 1: 张量打印调试——查看形状、数据类型、统计值和 NaN。"""
    print("\n--- 1. Print Debugging for Tensors ---")
    x = torch.randn(32, 784)  # 模拟输入批次: 32 个样本，784 维特征
    debug_print("input batch", x)

    w = torch.randn(784, 128)  # 权重矩阵
    out = x @ w  # 矩阵乘法
    debug_print("after matmul", out)

    with_nan = out.clone()
    with_nan[0, 0] = float("nan")  # 注入 NaN
    debug_print("with injected NaN", with_nan)


def demo_timing():
    """演示 2: 计时代码——测量矩阵乘法的执行时间。"""
    print("\n--- 2. Timing Code Sections ---")

    with Timer("matrix multiply 1000x1000"):
        a = torch.randn(1000, 1000)
        b = torch.randn(1000, 1000)
        _ = a @ b

    with Timer("matrix multiply 5000x5000"):
        a = torch.randn(5000, 5000)
        b = torch.randn(5000, 5000)
        _ = a @ b


def demo_memory_tracking():
    """演示 3: 内存追踪——使用 tracemalloc 找出内存热点。"""
    print("\n--- 3. Memory Tracking (tracemalloc) ---")
    tracemalloc.start()

    data = [torch.randn(100, 100) for _ in range(100)]  # 分配内存
    more_data = torch.randn(1000, 1000)

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")  # 按代码行号统计内存分配
    print("  Top 5 memory allocations:")
    for stat in top_stats[:5]:
        print(f"    {stat}")

    del data, more_data  # 释放内存
    tracemalloc.stop()


def demo_shape_checking():
    """演示 4: 形状检查——通过 Hook 逐层追踪模型的张量形状变换。"""
    print("\n--- 4. Shape Checking Through Model ---")

    model = nn.Sequential(
        nn.Linear(784, 256),  # 784 -> 256
        nn.ReLU(),
        nn.Linear(256, 64),   # 256 -> 64
        nn.ReLU(),
        nn.Linear(64, 10),    # 64 -> 10（10 类分类）
    )

    sample = torch.randn(4, 784)  # 4 个样本
    check_shapes(model, sample)


def demo_nan_detection():
    """演示 5: NaN 检测——正常 loss 和 NaN loss 的检测对比。"""
    print("\n--- 5. NaN Detection ---")

    model = nn.Sequential(
        nn.Linear(784, 256),
        nn.ReLU(),
        nn.Linear(256, 10),
    )

    x = torch.randn(4, 784)
    target = torch.randint(0, 10, (4,))
    criterion = nn.CrossEntropyLoss()  # 交叉熵损失
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, target)
    loss.backward()  # 反向传播
    print(f"  Normal loss: {loss.item():.4f}")
    nan_found = detect_nan(model, loss, step=0)
    print(f"  NaN detected: {nan_found}")

    fake_nan_loss = torch.tensor(float("nan"))  # 模拟 NaN loss
    print(f"  Simulated NaN loss: {fake_nan_loss.item()}")
    nan_found = detect_nan(model, fake_nan_loss, step=99)
    print(f"  NaN detected: {nan_found}")


def demo_device_checking():
    """演示 6: 设备检查——确保模型和张量在同一设备上。"""
    print("\n--- 6. Device Checking ---")

    model = nn.Linear(10, 5)
    t1 = torch.randn(4, 10)
    t2 = torch.randn(4, 10)

    check_devices(model, t1, t2)

    if torch.cuda.is_available():
        model_gpu = model.cuda()  # 模型移到 GPU
        t_cpu = torch.randn(4, 10)  # 张量在 CPU
        t_gpu = torch.randn(4, 10).cuda()  # 张量在 GPU
        print("  With mixed devices:")
        check_devices(model_gpu, t_cpu, t_gpu)  # CPU 张量和 GPU 模型不匹配


def demo_gradient_health():
    """演示 7: 梯度健康检查——检测梯度爆炸和梯度消失。"""
    print("\n--- 7. Gradient Health Check ---")

    model = nn.Sequential(
        nn.Linear(784, 256),
        nn.ReLU(),
        nn.Linear(256, 10),
    )

    x = torch.randn(4, 784)
    target = torch.randint(0, 10, (4,))
    criterion = nn.CrossEntropyLoss()

    output = model(x)
    loss = criterion(output, target)
    loss.backward()  # 反向传播计算梯度
    check_gradient_health(model)  # 检查梯度是否正常


def demo_gpu_memory():
    """演示 8: GPU 显存管理——分配、监控和释放显存。"""
    print("\n--- 8. GPU Memory Summary ---")

    if not torch.cuda.is_available():
        print("  No GPU available. Skipping GPU memory demo.")
        print("  On a GPU machine, torch.cuda.memory_summary() shows:")
        print("    - Allocated memory per block size")
        print("    - Cached (reserved) memory")
        print("    - Peak memory usage")
        return

    print(f"  GPU: {torch.cuda.get_device_name(0)}")
    print(f"  Allocated: {torch.cuda.memory_allocated() / 1e6:.1f} MB")  # 已分配显存
    print(f"  Cached: {torch.cuda.memory_reserved() / 1e6:.1f} MB")  # 缓存显存

    large_tensor = torch.randn(10000, 10000, device="cuda")  # 分配大张量
    print(f"  After 10k x 10k tensor:")
    print(f"    Allocated: {torch.cuda.memory_allocated() / 1e6:.1f} MB")

    del large_tensor
    torch.cuda.empty_cache()  # 释放缓存
    print(f"  After cleanup:")
    print(f"    Allocated: {torch.cuda.memory_allocated() / 1e6:.1f} MB")


def demo_logging():
    """演示 9: 结构化日志——训练过程中记录关键指标。"""
    print("\n--- 9. Structured Logging ---")

    logger.info("Training started: lr=0.001, batch_size=32, epochs=10")  # 训练开始
    logger.info("Step 100: loss=2.3026, accuracy=0.10")  # 训练进度
    logger.warning("Loss spike detected: 15.7 at step 450")  # 异常检测
    logger.info("Step 1000: loss=0.4512, accuracy=0.87")
    logger.info("Training complete: best_loss=0.3201")  # 训练完成


def demo_conditional_breakpoint():
    """演示 10: 条件断点模式——在异常发生时自动暂停。"""
    print("\n--- 10. Conditional Breakpoint Pattern ---")
    print("  In real code, use this pattern:")
    print()
    print("    for step in range(num_steps):")
    print("        loss = train_step(model, batch)")
    print("        if loss.item() > 10 or torch.isnan(loss):")
    print("            breakpoint()  # drops into pdb")  # 进入 Python 调试器
    print()
    print("  Useful pdb commands once inside:")
    print("    p tensor.shape       # print shape")  # 查看形状
    print("    p tensor.device      # check device")  # 查看设备
    print("    p tensor.grad        # inspect gradients")  # 查看梯度
    print("    p tensor.isnan().sum()  # count NaNs")  # 统计 NaN 数量
    print("    c                    # continue execution")  # 继续执行
    print("    q                    # quit debugger")  # 退出调试


def main():
    """主函数: 依次运行所有调试和性能分析演示。"""
    print("=" * 60)
    print("  AI Debugging and Profiling Toolkit")  # AI 调试和性能分析工具包
    print("  Phase 0, Lesson 12")
    print("=" * 60)

    if not HAS_TORCH:
        print("\nPyTorch not installed. Install with:")
        print("  uv pip install torch")
        print("\nRunning non-PyTorch demos only...\n")
        demo_memory_tracking()
        demo_logging()
        return 1

    demo_print_debugging()  # 张量打印调试
    demo_timing()  # 计时
    demo_memory_tracking()  # 内存追踪
    demo_shape_checking()  # 形状检查
    demo_nan_detection()  # NaN 检测
    demo_device_checking()  # 设备检查
    demo_gradient_health()  # 梯度健康
    demo_gpu_memory()  # GPU 显存
    demo_logging()  # 结构化日志
    demo_conditional_breakpoint()  # 条件断点

    print("\n" + "=" * 60)
    print("  All demos complete.")  # 所有演示完成
    print("  Next: introduce bugs intentionally and practice catching them.")  # 下一步: 故意引入 bug 并练习捕获
    print("=" * 60 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # 运行所有调试演示
