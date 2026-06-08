"""Four orchestration patterns: supervisor, swarm, hierarchical, debate.

Same three-intent task (refund / bug / sales) handled four ways. Measure
op count per pattern to see cost trade-offs.

核心概念：四种 Agent 编排模式对比 —— Supervisor-Worker（中心调度分发）、Swarm（去中心化 handoff）、
Hierarchical（两级树状委派）、Debate（多 Agent 辩论求共识）。同一任务集对比操作数和成本。
AI 对应：Supervisor 模式是 OpenAI Assistants API 的默认编排方式，Swarm 是 OpenAI 2024 年开源的
多 Agent 框架，Hierarchical 对应 CrewAI 的 manager 模式，Debate 对应 AutoGen GroupChat；
选择哪种模式取决于任务复杂度、延迟预算和成本约束。
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Callable


def classify(text: str) -> str:
    t = text.lower()
    if "refund" in t:
        return "refund"
    if "crash" in t or "error" in t or "bug" in t:
        return "bug"
    if "pricing" in t or "quote" in t:
        return "sales"
    return "sales"


SPECIALISTS: dict[str, Callable[[str], str]] = {
    "refund": lambda t: f"refund handled: {t[:30]}",
    "bug":    lambda t: f"bug logged: {t[:30]}",
    "sales":  lambda t: f"quote sent: {t[:30]}",
}


def supervisor_worker(tasks: list[str]) -> tuple[list[str], int]:
    trace: list[str] = []
    ops = 0
    for task in tasks:
        ops += 1
        label = classify(task)
        trace.append(f"supervisor -> {label}")
        specialist = SPECIALISTS[label]
        ops += 1
        trace.append(f"  {label}: {specialist(task)}")
    return trace, ops


def swarm(tasks: list[str]) -> tuple[list[str], int]:
    trace: list[str] = []
    ops = 0
    for task in tasks:
        current = list(SPECIALISTS)[0]
        hops = 0
        while hops < 3:
            ops += 1
            label = classify(task)
            if current == label:
                trace.append(f"swarm[{current}]: {SPECIALISTS[current](task)}")
                break
            trace.append(f"swarm[{current}] handoff -> {label}")
            current = label
            hops += 1
    return trace, ops


def hierarchical(tasks: list[str]) -> tuple[list[str], int]:
    trace: list[str] = []
    ops = 0
    for task in tasks:
        ops += 1
        top_label = "customer_ops" if classify(task) != "sales" else "commercial"
        trace.append(f"top -> {top_label}")
        ops += 1
        sub_label = classify(task)
        trace.append(f"  {top_label} -> {sub_label}")
        specialist = SPECIALISTS[sub_label]
        ops += 1
        trace.append(f"    {sub_label}: {specialist(task)}")
    return trace, ops


def debate(tasks: list[str]) -> tuple[list[str], int]:
    trace: list[str] = []
    ops = 0
    for task in tasks:
        proposals: list[str] = []
        for debater in ("alpha", "beta", "gamma"):
            ops += 1
            label = classify(task)
            proposals.append(label)
            trace.append(f"{debater} proposes {label}")
        ops += 1
        convergent = Counter(proposals).most_common(1)[0][0]
        specialist = SPECIALISTS[convergent]
        ops += 1
        trace.append(f"debate converges -> {convergent}: {specialist(task)}")
    return trace, ops


def main() -> None:
    print("=" * 70)
    print("ORCHESTRATION PATTERNS — Phase 14, Lesson 28")
    print("=" * 70)

    tasks = [
        "I need a refund for invoice 4711",
        "the CLI crashes on ctrl-c",
        "do you offer volume pricing?",
    ]

    for name, fn in (
        ("supervisor-worker", supervisor_worker),
        ("swarm",             swarm),
        ("hierarchical",      hierarchical),
        ("debate",            debate),
    ):
        trace, ops = fn(tasks)
        print(f"\n--- {name}  ops={ops} ---")
        for line in trace:
            print(f"  {line}")

    print()
    print("supervisor: cleanest. swarm: shortest. hierarchical: deepest.")
    print("debate: most expensive. pick topology AFTER picking the problem.")


if __name__ == "__main__":
    main()  # 运行主函数
