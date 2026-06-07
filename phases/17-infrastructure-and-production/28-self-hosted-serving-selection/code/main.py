"""Self-hosted LLM engine decision-tree walker — stdlib Python.

Given hardware, scale, and workload, pick an engine with explanation.

核心概念：自托管 LLM 推理引擎决策树——按硬件(CPU/Apple Silicon/AMD/NVIDIA Hopper/Blackwell)、
规模(单用户/小团队/生产/企业)、工作负载(通用聊天/Agentic 多轮/RAG 前缀复用/MoE)
选择最优引擎：llama.cpp(CPU/边缘)、Ollama(开发)、vLLM(生产通用)、
SGLang(Agentic/前缀密集)、TRT-LLM(Blackwell 吞吐优先)
AI 对应：vLLM 是最广泛使用的开源推理引擎；SGLang 的 RadixAttention 在
agentic 多轮场景中表现最优；TensorRT-LLM (NVIDIA) 在 Blackwell GPU 上吞吐最高；
llama.cpp 是 CPU 和 Apple Silicon 的首选；Ollama 封装 llama.cpp 提供开箱即用体验；
TGI (Hugging Face) 自 2025 年 12 月起进入维护模式
"""

from __future__ import annotations


def pick_engine(hardware: str, scale: str, workload: str) -> dict:
    reasons = []
    engine = None

    if hardware == "CPU":
        engine = "llama.cpp"
        reasons.append("hardware is CPU — only llama.cpp is competitive")
        if scale == "single_user":
            reasons.append("single-user dev → Ollama wraps llama.cpp with one-command UX")
            engine = "Ollama (llama.cpp under the hood)"
    elif hardware == "Apple Silicon":
        engine = "Ollama" if scale == "single_user" else "llama.cpp"
        reasons.append("Apple Silicon → Metal via llama.cpp (Ollama wraps)")
    elif hardware == "AMD":
        engine = "vLLM"
        reasons.append("AMD → vLLM ROCm support; TRT-LLM is NVIDIA-only")
        if "agentic" in workload.lower() or "prefix" in workload.lower():
            engine = "SGLang"
            reasons.append("agentic / prefix-heavy → SGLang RadixAttention")
    elif hardware == "NVIDIA Hopper":
        if "agentic" in workload.lower() or "prefix" in workload.lower():
            engine = "SGLang"
            reasons.append("Hopper + agentic/prefix → SGLang is the specialist")
        elif scale == "single_user":
            engine = "Ollama"
            reasons.append("single-user on Hopper is a dev scenario → Ollama is enough")
        else:
            engine = "vLLM"
            reasons.append("Hopper production → vLLM is the broad default")
    elif hardware == "NVIDIA Blackwell":
        engine = "TRT-LLM"
        reasons.append("Blackwell + throughput priority → TRT-LLM leads on B200/GB200")
        if scale in ("small_team", "production") and "agentic" not in workload.lower():
            reasons.append("vLLM Blackwell SM120 is a close second (v0.15.1 Feb 2026)")

    if scale == "enterprise":
        reasons.append("10k+ users → stack with production-stack (Phase 17 · 18)"
                      " + disaggregated (Phase 17 · 17) + cache-aware router (Phase 17 · 11)")

    reasons.append("TGI is in maintenance mode since Dec 11, 2025 — default AWAY from TGI for new projects")

    return {
        "hardware": hardware,
        "scale": scale,
        "workload": workload,
        "engine": engine,
        "reasons": reasons,
    }


SCENARIOS = [
    ("CPU",              "single_user",   "chat"),
    ("Apple Silicon",    "single_user",   "coding assistant"),
    ("NVIDIA Hopper",    "production",    "general chat"),
    ("NVIDIA Hopper",    "production",    "agentic multi-turn"),
    ("NVIDIA Blackwell", "enterprise",    "MoE frontier serving"),
    ("AMD",              "production",    "RAG with heavy prefix reuse"),
    ("NVIDIA Hopper",    "small_team",    "long-context 128K"),
]


def main() -> None:
    print("=" * 80)
    print("SELF-HOSTED ENGINE DECISION TREE — hardware / scale / workload")
    print("=" * 80)
    for hw, sc, wl in SCENARIOS:
        d = pick_engine(hw, sc, wl)
        print(f"\n[{hw}] [{sc}] [{wl}]")
        print(f"  → engine: {d['engine']}")
        for r in d["reasons"]:
            print(f"    · {r}")


if __name__ == "__main__":
    main()  # 运行主函数
