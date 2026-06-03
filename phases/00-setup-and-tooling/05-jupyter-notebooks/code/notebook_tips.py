"""
Jupyter Notebook 核心技巧演示 — 对比 Python 原生 vs NumPy 性能、内联绘图、DataFrame 展示、内存管理。
核心概念: Notebook 中的交互式数据分析、Magic 命令等效操作。
AI 对应: Notebook 是 AI 实验的标准环境，用于数据探索、模型原型开发和结果可视化。
"""
import time
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")  # 使用非交互式后端（脚本中无法弹窗）
import matplotlib.pyplot as plt
import pandas as pd


def timing_comparison():
    """对比 Python 列表推导式 vs NumPy 向量化运算的速度差异。"""
    print("=== Timing: List vs NumPy ===\n")

    size = 1_000_000  # 一百万个元素

    start = time.perf_counter()
    python_list = [x ** 2 for x in range(size)]  # Python 原生列表推导
    list_time = time.perf_counter() - start
    print(f"List comprehension: {list_time:.4f}s")

    start = time.perf_counter()
    numpy_array = np.arange(size) ** 2  # NumPy 向量化运算，比原生快几十倍
    numpy_time = time.perf_counter() - start
    print(f"NumPy:              {numpy_time:.4f}s")
    print(f"Speedup:            {list_time / numpy_time:.1f}x")  # 加速倍数


def inline_plotting():
    """演示 Notebook 中的内联绘图（脚本模式保存为文件）。"""
    print("\n=== Inline Plotting ===\n")

    np.random.seed(42)  # 固定随机种子，结果可复现
    x = np.linspace(0, 10, 200)  # 0 到 10 之间的 200 个等间距点
    y_sin = np.sin(x)  # 正弦信号
    y_noisy = y_sin + np.random.normal(0, 0.2, 200)  # 加高斯噪声

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))  # 一行两列的子图

    axes[0].plot(x, y_sin, label="sin(x)")  # 原始信号
    axes[0].plot(x, y_noisy, alpha=0.5, label="noisy")  # 带噪声信号
    axes[0].set_title("Signal vs Noise")
    axes[0].legend()

    axes[1].hist(y_noisy - y_sin, bins=30, edgecolor="black")  # 噪声分布直方图
    axes[1].set_title("Noise Distribution")

    plt.tight_layout()
    plt.savefig("notebook_plot.png", dpi=100)  # 保存图片
    print("Saved plot to notebook_plot.png")  # 在 Notebook 中用 plt.show() 即可内联显示
    print("In a notebook, plt.show() displays this inline.")


def dataframe_display():
    """演示 DataFrame 的富文本展示和数据分析。"""
    print("\n=== DataFrame Display ===\n")

    df = pd.DataFrame({  # 创建模型对比表
        "model": ["Linear Regression", "Random Forest", "Neural Network", "XGBoost"],
        "accuracy": [0.72, 0.89, 0.94, 0.91],
        "train_time_sec": [0.1, 2.3, 45.6, 8.2],
        "parameters": [102, 50_000, 1_200_000, 25_000],
    })

    print("In a notebook, just typing 'df' renders a rich HTML table:\n")
    print(df.to_string(index=False))

    print(f"\nBest model: {df.loc[df['accuracy'].idxmax(), 'model']}")  # 准确率最高的模型
    print(f"Fastest model: {df.loc[df['train_time_sec'].idxmin(), 'model']}")  # 训练最快的模型


def memory_check():
    """检查不同大小数组的内存占用——Notebook 中需注意内存累积。"""
    print("\n=== Memory Usage ===\n")

    small = np.random.randn(1000)  # 一千个浮点数
    medium = np.random.randn(100_000)  # 十万个浮点数
    large = np.random.randn(10_000_000)  # 一千万个浮点数

    for name, arr in [("1K", small), ("100K", medium), ("10M", large)]:
        size_mb = arr.nbytes / 1e6  # 字节数转 MB
        print(f"Array {name:>4s} elements: {size_mb:>8.2f} MB")

    print(f"\nPython process memory: ~{sys.getsizeof(large) / 1e6:.1f} MB for the large array")
    print("In notebooks, memory accumulates across cells. Restart the kernel to free it.")  # Notebook 中内存会累积，需重启 Kernel 释放


def magic_command_equivalents():
    """演示 Jupyter Magic 命令的等效 Python 代码。"""
    print("\n=== Magic Command Equivalents ===\n")
    print("In a notebook, you would use magic commands:")
    print("  %timeit np.random.randn(10000)    -> micro-benchmark")  # 微基准测试
    print("  %%time long_operation()            -> wall clock time")  # 墙钟时间
    print("  %matplotlib inline                 -> show plots in cells")  # 内联显示图表
    print("  !pip install package               -> install from notebook")  # 安装包
    print("  %env VAR                           -> check env variable")  # 查看环境变量
    print()

    iterations = 1000
    start = time.perf_counter()
    for _ in range(iterations):
        np.random.randn(10000)  # 重复执行取平均（模拟 %timeit）
    elapsed = time.perf_counter() - start
    per_call = elapsed / iterations * 1e6  # 转换为微秒

    print(f"Manual timing (like %%timeit): np.random.randn(10000)")
    print(f"  {per_call:.1f} us per call ({iterations} iterations)")


if __name__ == "__main__":
    print("Notebook Tips - Key Patterns\n")  # Notebook 核心技巧
    print("Run these in a Jupyter notebook to see rich output.\n")  # 在 Notebook 中运行可看到富文本输出

    timing_comparison()  # 列表 vs NumPy 速度对比
    inline_plotting()  # 内联绘图演示
    dataframe_display()  # DataFrame 展示演示
    memory_check()  # 内存占用检查
    magic_command_equivalents()  # Magic 命令等效操作
