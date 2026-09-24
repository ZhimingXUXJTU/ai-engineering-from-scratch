"""课程：Production Observability, Latency, and Cost | 生产可观测性、延迟与成本
路径：certifications/claude/lessons/26-production-observability-latency-and-cost
核心概念：把系统成功（HTTP 200）、任务成功（达到评分标准）与业务结果分成四层观测；
日志记离散事件、指标做时间聚合、追踪串起完整轨迹；延迟拆到每个 span 并同时盯
P50/P95 尾部；成本按"每次成功结果的成本"计算——失败请求照样留在分子里；
告警必须有负责人与运维手册，灰度发布用质量、延迟、成本、安全四道门守住证据风险。
AI 应用对应：真实 LLM 服务的可观测性与 FinOps 基线（发布记分卡、金丝雀发布、
缓存命中率监控、按变体分层比较）的最小模型——仪表盘度量的是传输成功，
产品依赖的是任务成功，可观测性负责把两者连起来。

Production telemetry lab for this lesson's docs/en.md.

Aggregates traces into latency, reliability, cache, error, and economic signals.
Evaluates cost per successful outcome instead of reporting call price alone.
Uses only the Python standard library and synthetic, non-sensitive trace data.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Trace:
    trace_id: str
    variant: str
    duration_ms: int
    input_tokens: int
    output_tokens: int
    cost_usd: float
    task_success: bool
    system_ok: bool
    cache_read: bool = False
    error_category: str | None = None


def percentile(values: list[int], probability: float) -> float:
    if not values:
        return 0.0
    if not 0 <= probability <= 1:
        raise ValueError("probability must be between zero and one")
    ordered = sorted(values)
    rank = max(0, math.ceil(probability * len(ordered)) - 1)
    return float(ordered[rank])


def summarize(traces: list[Trace]) -> dict[str, object]:
    if not traces:
        return {
            "requests": 0,
            "system_success_rate": 0.0,
            "task_success_rate": 0.0,
            "p50_ms": 0.0,
            "p95_ms": 0.0,
            "total_cost_usd": 0.0,
            "cost_per_task_success_usd": None,
            "cache_read_rate": 0.0,
            "errors": {},
        }
    task_successes = sum(trace.task_success for trace in traces)
    system_successes = sum(trace.system_ok for trace in traces)
    total_cost = sum(trace.cost_usd for trace in traces)
    errors = Counter(trace.error_category for trace in traces if trace.error_category)
    return {
        "requests": len(traces),
        "system_success_rate": round(system_successes / len(traces), 4),
        "task_success_rate": round(task_successes / len(traces), 4),
        "p50_ms": percentile([trace.duration_ms for trace in traces], 0.50),
        "p95_ms": percentile([trace.duration_ms for trace in traces], 0.95),
        "total_cost_usd": round(total_cost, 6),
        "cost_per_task_success_usd": round(total_cost / task_successes, 6) if task_successes else None,
        "cache_read_rate": round(sum(trace.cache_read for trace in traces) / len(traces), 4),
        "errors": dict(sorted(errors.items())),
    }


def by_variant(traces: list[Trace]) -> dict[str, dict[str, object]]:
    variants: dict[str, list[Trace]] = {}
    for trace in traces:
        variants.setdefault(trace.variant, []).append(trace)
    return {name: summarize(selected) for name, selected in sorted(variants.items())}


@dataclass(frozen=True)
class ServiceObjectives:
    minimum_task_success_rate: float
    maximum_p95_ms: float
    maximum_cost_per_success_usd: float


def evaluate_objectives(summary: dict[str, object], objectives: ServiceObjectives) -> dict[str, bool]:
    cost = summary.get("cost_per_task_success_usd")
    return {
        "task_success": float(summary.get("task_success_rate", 0.0)) >= objectives.minimum_task_success_rate,
        "latency": float(summary.get("p95_ms", 0.0)) <= objectives.maximum_p95_ms,
        "cost": cost is not None and float(cost) <= objectives.maximum_cost_per_success_usd,
    }


def demo() -> dict[str, object]:
    traces = [
        Trace("t1", "baseline", 1200, 3000, 300, 0.020, True, True),
        Trace("t2", "baseline", 1700, 3200, 400, 0.024, False, True),
        Trace("t3", "cached", 650, 3000, 280, 0.008, True, True, True),
        Trace("t4", "cached", 720, 3000, 310, 0.009, True, True, True),
        Trace("t5", "cached", 900, 3000, 0, 0.004, False, False, True, "tool_timeout"),
    ]
    aggregate = summarize(traces)
    objectives = ServiceObjectives(0.70, 1800, 0.03)
    return {
        "aggregate": aggregate,
        "variants": by_variant(traces),
        "objectives": asdict(objectives),
        "passes": evaluate_objectives(aggregate, objectives),
    }


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2))

