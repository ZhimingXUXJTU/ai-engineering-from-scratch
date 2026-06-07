"""Chaos engineering runner with safety plane gates — stdlib Python.

Runs three LLM-specific experiments and applies burn-rate + blast-radius safety gates.

核心概念：LLM 系统的混沌工程——安全平面门控：burn-rate(实验错误率/基线错误率) x
blast-radius(影响范围百分比)，burn-rate > 2x 且 blast-radius > 20% 时中止实验，
三种 LLM 特定实验：Pod Kill、Provider 429 Fallback、Tokenizer Stall
AI 对应：Chaos Monkey (Netflix) 是混沌工程的起源；Litmus Chaos 是 Kubernetes 的
混沌工程框架；Gremlin 提供企业级混沌工程平台；
LLM 特有的故障模式（tokenizer stall、KV cache OOM、provider rate limit）
需要专门的混沌实验设计；SLO error budget 是实验安全的量化边界
"""

from __future__ import annotations

from dataclasses import dataclass


ERROR_BUDGET_PER_DAY = 0.001   # 99.9% SLO
EXPECTED_ERROR_RATE = 0.0005


@dataclass
class Experiment:
    name: str
    duration_min: int
    induced_error_rate: float
    blast_radius_pct: float


EXPERIMENTS = [
    Experiment("pod kill (1 decode replica)",     5, 0.002, 0.05),
    Experiment("provider 429 fallback",           5, 0.015, 0.30),
    Experiment("malformed prompt tokenizer stall",3, 0.040, 0.10),
]


def run_experiment(e: Experiment) -> dict:
    burn_rate = e.induced_error_rate / max(EXPECTED_ERROR_RATE, 0.0001)
    paused = burn_rate > 2.0 and e.blast_radius_pct > 0.2
    return {
        "experiment": e.name,
        "duration": e.duration_min,
        "error_rate": e.induced_error_rate,
        "burn_rate_x": burn_rate,
        "blast_radius": e.blast_radius_pct,
        "paused_by_safety_plane": paused,
        "status": "ABORTED (burn-rate guard)" if paused else "COMPLETED",
    }


def main() -> None:
    print("=" * 90)
    print("CHAOS EXPERIMENT RUNNER — safety plane gates burn-rate × blast-radius")
    print("=" * 90)
    print(f"SLO error budget: {ERROR_BUDGET_PER_DAY*100:.2f}%/day")
    print(f"Expected baseline error rate: {EXPECTED_ERROR_RATE*100:.3f}%")
    print(f"Burn-rate gate: > 2.0x expected AND blast radius > 20%\n")

    header = f"{'Experiment':38}  {'mins':>4}  {'err %':>6}  {'burn×':>6}  {'blast':>6}  Status"
    print(header)
    print("-" * len(header))
    for e in EXPERIMENTS:
        r = run_experiment(e)
        print(f"{r['experiment']:38}  {r['duration']:>4}  "
              f"{r['error_rate']*100:>5.2f}%  "
              f"{r['burn_rate_x']:>5.1f}x  "
              f"{r['blast_radius']*100:>5.0f}%  "
              f"{r['status']}")

    print("\nRead: small-blast-radius experiments run to completion even at high burn rate.")
    print("Large-blast-radius + high burn → abort. Suppression windows + trace-ID tags")
    print("required to dedupe alerts during experiments.")


if __name__ == "__main__":
    main()  # 运行主函数
