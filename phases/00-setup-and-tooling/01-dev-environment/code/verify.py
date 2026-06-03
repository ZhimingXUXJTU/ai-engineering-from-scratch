"""
环境验证脚本 — 检查 AI 工程开发环境是否正确配置。
核心概念: 逐项检查 Python 工具链、GPU 支持等关键依赖。
AI 对应: 确保你能在后续课程中顺利运行 PyTorch、NumPy 等 AI 库。
"""
import sys
import shutil
import subprocess

# 核心检查项: Python 版本、基础库、开发工具
CHECKS = [
    ("Python 3.10+", lambda: sys.version_info >= (3, 10), f"Python {sys.version}"),  # Python 版本检查
    ("NumPy", lambda: __import__("numpy"), None),  # NumPy: 数值计算基础库
    ("Matplotlib", lambda: __import__("matplotlib"), None),  # Matplotlib: 数据可视化库
    ("Jupyter", lambda: __import__("jupyter"), None),  # Jupyter: 交互式笔记本
    ("Git", lambda: shutil.which("git") is not None, None),  # Git: 版本控制
    ("Node.js", lambda: shutil.which("node") is not None, None),  # Node.js: JS 运行时
    ("Rust (cargo)", lambda: shutil.which("cargo") is not None, None),  # Rust: 系统编程语言
]

# GPU 相关检查项（可选）
GPU_CHECKS = [
    ("PyTorch", lambda: __import__("torch"), None),  # PyTorch: 深度学习框架
    (
        "CUDA",  # CUDA: NVIDIA GPU 加速计算平台
        lambda: __import__("torch").cuda.is_available(),
        lambda: __import__("torch").cuda.get_device_name(0) if __import__("torch").cuda.is_available() else "Not available",
    ),
]


def run_check(name, check_fn, detail_fn=None):
    """运行单个检查项，返回 True/False。"""
    try:
        result = check_fn()
        if result is False:
            raise Exception("Check returned False")
        detail = ""
        if detail_fn:
            if callable(detail_fn):
                detail = f" ({detail_fn()})"
            else:
                detail = f" ({detail_fn})"
        print(f"  [PASS] {name}{detail}")  # 检查通过
        return True
    except Exception:
        print(f"  [FAIL] {name}")  # 检查失败
        return False


def main():
    """主函数: 运行所有检查并报告结果。"""
    print("\n=== AI Engineering from Scratch — Environment Check ===\n")

    print("Core:")  # 核心检查
    passed = sum(run_check(name, fn, detail) for name, fn, detail in CHECKS)
    total = len(CHECKS)

    print("\nGPU (optional):")  # GPU 检查（可选）
    gpu_passed = sum(run_check(name, fn, detail) for name, fn, detail in GPU_CHECKS)
    gpu_total = len(GPU_CHECKS)

    print(f"\nResult: {passed}/{total} core checks passed", end="")  # 显示核心检查结果
    if gpu_passed > 0:
        print(f", {gpu_passed}/{gpu_total} GPU checks passed")  # 显示 GPU 检查结果
    else:
        print(" (no GPU — that's fine, most lessons work on CPU)")

    if passed == total:
        print("\nYou're ready. Start with Phase 1.\n")  # 全部通过，可以开始学习
    else:
        print("\nFix the failed checks above, then run this script again.\n")  # 有失败项，需要修复

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())  # 运行环境检查
