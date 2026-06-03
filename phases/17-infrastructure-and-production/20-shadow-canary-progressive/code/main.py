"""Canary rollout simulator — stdlib Python.

Progressively increases candidate traffic share and checks five gates at each
step. Halts when any gate breaches. Supports injected regressions.

核心概念：本节实现的核心模式
AI 对应：此模式在现代 AI Agent 系统中有广泛应用。
"""

from __future__ import annotations

from dataclasses import dataclass
import random


STAGES = [0.01, 0.10, 0.25, 0.50, 0.75, 1.00]

BASELINE = {
    "latency_p99_ms": 900,
    "cost_per_req": 0.02,
    "error_rate": 0.02,
    "output_len_p99": 450,
    "thumbs_down_rate": 0.03,
}

GATES = {
    "latency_p99_ms": 1.5,
    "cost_per_req": 1.2,
    "error_rate": 2.0,
    "output_len_p99": 1.4,
    "thumbs_down_rate": 1.5,
}


@dataclass
class Regression:
    """Regression"""
    latency_mult: float = 1.0
    cost_mult: float = 1.0
    error_mult: float = 1.0
    output_len_mult: float = 1.0
    thumbs_down_mult: float = 1.0


def measure_stage(stage: float, reg: Regression, seed: int) -> dict:
    """measure_stage"""
    rng = random.Random(seed)
    noise = lambda v: v * rng.uniform(0.92, 1.08)
    return {  # 返回结果
        "latency_p99_ms": noise(BASELINE["latency_p99_ms"] * reg.latency_mult),
        "cost_per_req": noise(BASELINE["cost_per_req"] * reg.cost_mult),
        "error_rate": noise(BASELINE["error_rate"] * reg.error_mult),
        "output_len_p99": noise(BASELINE["output_len_p99"] * reg.output_len_mult),
        "thumbs_down_rate": noise(BASELINE["thumbs_down_rate"] * reg.thumbs_down_mult),
    }


def check_gates(metrics: dict) -> list[str]:
    """check_gates"""
    breaches = []
    for k, mult in GATES.items():
        if metrics[k] > BASELINE[k] * mult:
            breaches.append(k)
    return breaches  # 返回结果


def rollout(name: str, reg: Regression) -> None:
    """rollout"""
    print(f"\n{name}")
    print(f"Regression: latency={reg.latency_mult}, cost={reg.cost_mult}, error={reg.error_mult}, len={reg.output_len_mult}, thumbs={reg.thumbs_down_mult}")
    for i, stage in enumerate(STAGES):
        metrics = measure_stage(stage, reg, seed=stage_seed(i))
        breaches = check_gates(metrics)
        status = "PASS" if not breaches else f"HALT ({','.join(breaches)})"
        pct = int(stage * 100)
        print(f"  stage {pct:3}%  "
              f"lat_p99={metrics['latency_p99_ms']:5.0f}  "
              f"cost=${metrics['cost_per_req']:.4f}  "
              f"err={metrics['error_rate']*100:4.1f}%  "
              f"thumbs_dn={metrics['thumbs_down_rate']*100:4.1f}%  "
              f"{status}")
        if breaches:
            print(f"  → ROLLBACK (policy flip, pinned model reverted)")
            return  # 返回结果
    print("  → PROMOTED to 100%")


def stage_seed(i: int) -> int:
    """stage_seed"""
    return 11 + i * 3  # 返回结果


def main() -> None:
    """main"""
    print("=" * 95)
    print("CANARY ROLLOUT — six stages, five gates, injected regressions")
    print("=" * 95)

    rollout("Clean promotion", Regression())
    rollout("Small cost regression (10%) — within gate", Regression(cost_mult=1.10))
    rollout("Cost regression 25%", Regression(cost_mult=1.25))
    rollout("Latency regression 80%", Regression(latency_mult=1.80))
    rollout("Thumbs-down regression 60%", Regression(thumbs_down_mult=1.60))
    rollout("Quality silent + cost creep", Regression(cost_mult=1.15, thumbs_down_mult=1.45))


if __name__ == "__main__":
    main()  # 运行主函数
