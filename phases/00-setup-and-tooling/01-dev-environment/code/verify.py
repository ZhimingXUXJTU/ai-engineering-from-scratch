"""Route-aware environment preflight for AI Engineering from Scratch.

开发环境搭建 — 路线感知的环境预检 (Dev Environment — Route-aware Preflight)
核心概念：按"路线（route）最小环境"预检——每条学习路线只检查启动所需工具，
默认跳过后续课程才用到的依赖，每个失败项都给出精确的修复命令。
AI 应用对应：AI 工程师日常要在多套环境（训练 / 推理 / 前端 / Agent）间切换，
"用到再装 + 可脚本化自检"是保持环境可复现、可交接的工程实践。

Lesson: phases/00-setup-and-tooling/01-dev-environment/docs/en.md
Run this file from the repository root before starting a learning route.
"""

from __future__ import annotations

import argparse
import importlib.util
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Result:
    ok: bool      # 是否通过
    detail: str   # 检测到的版本 / 路径 / 错误详情


@dataclass(frozen=True)
class Probe:
    label: str                    # 检查项显示名
    run: Callable[[], Result]     # 执行检查的函数
    fix: str                      # 失败时给出的精确修复命令


@dataclass(frozen=True)
class Route:
    label: str                        # 路线显示名
    required: tuple[str, ...]         # 启动路线必需的探针
    optional: tuple[str, ...]         # 后续课程才需要的探针（--show-later 时检查）
    next_command: str                 # 预检通过后建议运行的下一条命令
    manual: tuple[str, ...] = ()      # 脚本无法自动验证、需人工确认的检查项


def command_result(command: str, minimum_major: int | None = None) -> Result:
    """运行 `<命令> --version` 并解析版本号（可选校验主版本下限）。"""
    path = shutil.which(command)
    if path is None:
        return Result(False, f"{command!r} was not found on PATH")

    try:
        process = subprocess.run(
            [path, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return Result(False, f"could not run {path}: {exc}")

    output = (process.stdout or process.stderr).strip().splitlines()
    detail = output[0] if output else f"exit code {process.returncode} with no version output"
    if process.returncode != 0:
        return Result(False, detail)

    if minimum_major is not None:
        digits = "".join(character if character.isdigit() else " " for character in detail)
        parts = digits.split()
        if not parts:
            return Result(False, f"could not parse a version from {detail!r}")
        major = int(parts[0])
        if major < minimum_major:
            return Result(False, f"found {detail}; need version {minimum_major}+")

    return Result(True, f"{detail} at {path}")


def python_result() -> Result:
    """检查 Python 版本是否 >= 3.11（课程主语言）。"""
    version = platform.python_version()
    executable = sys.executable
    if sys.version_info < (3, 11):
        return Result(False, f"found Python {version} at {executable}; need Python 3.11+")
    return Result(True, f"Python {version} at {executable}")


def module_result(module: str) -> Result:
    """检查某个 Python 库能否被当前解释器导入。"""
    if importlib.util.find_spec(module) is None:
        return Result(False, f"{module!r} is not importable by {sys.executable}")
    return Result(True, f"importable by {sys.executable}")


def gpu_result() -> Result:
    """检查加速器后端：CUDA / Apple MPS / 纯 CPU（GPU 可选，不阻塞任何路线）。"""
    if importlib.util.find_spec("torch") is None:
        return Result(False, "PyTorch is not installed, so no accelerator backend was checked")

    try:
        import torch
    except Exception as exc:
        return Result(False, f"PyTorch could not be imported: {type(exc).__name__}: {exc}")

    if torch.cuda.is_available():
        return Result(True, f"CUDA: {torch.cuda.get_device_name(0)}")
    mps = getattr(getattr(torch, "backends", None), "mps", None)
    if mps is not None and mps.is_available():
        return Result(True, "Apple MPS is available")
    return Result(True, "CPU only; a GPU is optional for the starting lessons")


def git_fix() -> str:
    """按操作系统给出 Git 的安装修复命令。"""
    system = platform.system()
    if system == "Darwin":
        return "Run `xcode-select --install`, then `git --version`."
    if system == "Windows":
        return "Run `winget install --id Git.Git -e`, then `git --version`."
    return "Run `sudo apt-get update && sudo apt-get install -y git`, then `git --version`."


# 全部工具探针表（旧版 CHECKS/GPU_CHECKS 表的扩展版）：
# 每个条目 = 显示名 + 检查函数 + 失败修复命令
PROBES = {
    "python": Probe(  # Python 3.11+：课程主语言
        "Python 3.11+",
        python_result,
        "Install it with `uv python install 3.12`, activate that environment, and rerun with `python3`.",
    ),
    "git": Probe("Git", lambda: command_result("git"), git_fix()),  # Git：版本控制
    "node": Probe(  # Node.js 20+：TypeScript 课程运行时
        "Node.js 20+",
        lambda: command_result("node", minimum_major=20),
        "Run `fnm install 22 && fnm use 22`, then `node --version`.",
    ),
    "npx": Probe(  # npx：TS 课程的包执行器
        "npx",
        lambda: command_result("npx"),
        "Install Node.js 22, then run `npm install -g npm` and `npx --version`.",
    ),
    "cargo": Probe(  # Rust cargo：高性能课程工具链
        "Rust cargo",
        lambda: command_result("cargo"),
        "Install Rust with rustup, restart the shell, then run `cargo --version`.",
    ),
    "julia": Probe(  # Julia：数学密集型课程
        "Julia",
        lambda: command_result("julia"),
        "Install Julia with juliaup, restart the shell, then run `julia --version`.",
    ),
    "numpy": Probe(  # NumPy：数值计算基础库
        "NumPy",
        lambda: module_result("numpy"),
        "Activate the course environment and run `python3 -m pip install numpy`.",
    ),
    "matplotlib": Probe(  # Matplotlib：数据可视化库
        "Matplotlib",
        lambda: module_result("matplotlib"),
        "Activate the course environment and run `python3 -m pip install matplotlib`.",
    ),
    "jupyter": Probe(  # Jupyter：交互式笔记本
        "Jupyter",
        lambda: module_result("jupyter"),
        "Activate the course environment and run `python3 -m pip install jupyter`.",
    ),
    "torch": Probe(  # PyTorch：深度学习框架
        "PyTorch",
        lambda: module_result("torch"),
        "Activate the course environment and run `python3 -m pip install torch`.",
    ),
    "gpu": Probe(  # 加速器后端：CUDA / Apple MPS / 纯 CPU（可选）
        "Accelerator backend",
        gpu_result,
        "A GPU is optional. Install PyTorch first if you want CUDA or Apple MPS detection.",
    ),
}


BASE_OPTIONAL = ("node", "npx", "numpy", "matplotlib", "jupyter", "torch", "gpu", "cargo", "julia")  # 初学者路线默认跳过、后续课程按需启用的工具

ROUTES = {  # 七条学习路线定义（--route 参数）：每条只列"启动必需"项，其余归入 optional
    "beginner": Route(  # 初学者完整序列：只需 Python + Git 即可开跑
        "Beginner course",
        ("python", "git"),
        BASE_OPTIONAL,
        "python3 phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py",
    ),
    "ml-foundations": Route(  # 数学与 ML 基础：在 beginner 之上加 NumPy
        "Math and ML foundations",
        ("python", "git", "numpy"),
        ("matplotlib", "jupyter", "torch", "gpu", "julia"),
        "python3 phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py",
    ),
    "llm-engineering": Route(  # LLM 工程：从提示工程起步
        "LLM engineering",
        ("python", "git"),
        ("numpy", "torch", "gpu", "node", "npx", "cargo"),
        "python3 phases/11-llm-engineering/01-prompt-engineering/code/prompt_engineering.py",
    ),
    "agents": Route(  # Agent 工程：从 Agent 循环起步
        "Agent engineering",
        ("python", "git"),
        ("node", "npx", "numpy", "torch"),
        "python3 phases/14-agent-engineering/01-the-agent-loop/code/main.py",
    ),
    "mcp": Route(  # MCP 协议课程：Python + Git 即可开始
        "Model Context Protocol (MCP)",
        ("python", "git"),
        ("node", "npx"),
        "python3 phases/13-tools-and-protocols/06-mcp-fundamentals/code/main.py",
    ),
    "agent-skills": Route(  # Agent Skills 工程：需要 Node + npx，另附人工主机检查项
        "Agent Skills engineering",
        ("python", "git", "node", "npx"),
        (),
        "python3 phases/13-tools-and-protocols/22-skills-and-agent-sdks/code/main.py",
        (
            "Choose one skill-capable host and confirm it is installed.",
            "Choose a user or project skill scope and confirm it is writable.",
        ),
    ),
    "certification": Route(  # Claude 认证准备：入门只需打开 GETTING_STARTED.md
        "Claude certification preparation",
        ("python", "git"),
        ("node", "npx"),
        "Open certifications/claude/GETTING_STARTED.md and choose a track.",
        ("If using the AI tutor, confirm your selected host can read repository skills.",),
    ),
}


def parse_args() -> argparse.Namespace:
    """命令行参数：--route 选择学习路线（默认 beginner），--show-later 同时检查后续工具。"""
    parser = argparse.ArgumentParser(
        description="Check only the tools needed to start a selected curriculum route."
    )
    parser.add_argument(
        "--route",
        choices=tuple(ROUTES),
        default="beginner",
        help="learning route to prepare for (default: beginner)",
    )
    parser.add_argument(
        "--show-later",
        action="store_true",
        help="also check tools that are optional now or required by later lessons",
    )
    return parser.parse_args()


def print_probe(key: str, required: bool) -> bool:
    """打印单项探针结果：PASS / FAIL（当前必需）/ LATER（后续才需要），失败时附修复命令。"""
    probe = PROBES[key]
    result = probe.run()
    if result.ok:
        status = "PASS"  # 通过
    elif required:
        status = "FAIL"  # 必需项失败——阻塞当前路线
    else:
        status = "LATER"  # 后续工具缺失——不阻塞当前路线
    timing = "required now" if required else "optional or needed later"
    print(f"  [{status}] {probe.label} ({timing})")
    print(f"         {result.detail}")
    if not result.ok:
        print(f"         Fix: {probe.fix}")
    return result.ok


def main() -> int:
    """主函数：按所选路线运行必需检查，汇总结果并给出下一步命令。"""
    args = parse_args()
    route = ROUTES[args.route]

    print("\n=== AI Engineering from Scratch: Environment Check ===\n")
    print(f"Route: {route.label} (`--route {args.route}`)\n")

    passed = 0
    for key in route.required:  # 逐项运行必需探针
        passed += int(print_probe(key, required=True))

    if route.optional and args.show_later:  # 显式要求时才检查后续工具
        print("\nOptional or needed later:")
        for key in route.optional:
            print_probe(key, required=False)
    elif route.optional:  # 默认跳过后续工具，避免"一屏警告"吓退新手
        print(
            f"\nLater checks skipped: {len(route.optional)} tools are not needed to start. "
            "Add `--show-later` when you want to inspect them."
        )

    if route.manual:  # 输出脚本无法自动验证的人工检查项
        print("\nManual checks:")
        for item in route.manual:
            print(f"  [MANUAL] {item}")

    total = len(route.required)
    print(f"\nResult: {passed}/{total} required checks passed")
    if passed == total:  # 全部必需项通过：给出下一节课的确切命令
        print(f"Ready to start {route.label}.")
        print(f"Next: {route.next_command}\n")
        return 0

    print("Not ready yet. Run each Fix command above, then repeat this preflight.\n")  # 有失败项：按修复命令逐项处理
    return 1


if __name__ == "__main__":
    raise SystemExit(main())  # 运行路线预检，退出码 0=就绪 / 1=未就绪
