# Lesson program for selecting the smallest evidence-producing slice.
# Read: phases/14-agent-engineering/50-choose-the-smallest-testable-slice/docs/en.md
# Reference: Boehm, A Spiral Model of Software Development and Enhancement, 1988.
# Reference: Lenarduzzi and Taibi, MVP Explained, 2016.
# Run this file to generate outputs/slice-decision.json.
# 中文标题：选能改变决策的最小切片 (Choose the Smallest Slice That Can Change the Decision)
# 核心概念：先从最高风险开放假设推出"必备证明集"，切片只有覆盖全部证明才有资格参评
#           （required_proof <= set(item.proves)）；评分 = (结果价值+不确定性消减)/(投入+后果惩罚)，
#           资格门槛高于算术——便宜但证明不全的候选分数再高也会被拒绝。
# AI 应用对应：AI 功能的 MVP/试点范围应按"能证明哪条假设"来定，而不是按"能做多小"来定；
#             只读回放这类可逆形态优先于生产自动执行，停止规则先于实现写下。
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Slice:
    name: str
    outcome_value: int
    uncertainty_reduced: int
    effort: int
    consequence: int
    reversible: bool
    proves: tuple[str, ...]


def score(item: Slice) -> float:
    if item.effort < 1:
        raise ValueError("effort must be positive")
    risk_penalty = item.consequence * (2 if not item.reversible else 0.5)
    return round((item.outcome_value + item.uncertainty_reduced) / (item.effort + risk_penalty), 3)


def choose(items: list[Slice], required_proof: set[str]) -> Slice:
    candidates = [item for item in items if required_proof <= set(item.proves)]
    if not candidates:
        raise ValueError("no slice proves the required assumptions")
    return max(candidates, key=lambda item: (score(item), -item.effort, item.name))


def decision(items: list[Slice], required_proof: set[str]) -> dict:
    selected = choose(items, required_proof)
    return {
        "required_proof": sorted(required_proof),
        "selected": {**asdict(selected), "score": score(selected)},
        "alternatives": [{**asdict(item), "score": score(item)} for item in items if item != selected],
    }


def example() -> list[Slice]:
    return [
        Slice("read-only incident replay", 4, 5, 2, 1, True, ("service-identification", "operator-trust")),
        Slice("production auto-remediation", 5, 4, 10, 5, False, ("service-identification", "operator-trust")),
        Slice("dashboard mockup", 2, 2, 1, 1, True, ("operator-trust",)),
    ]


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "outputs" / "slice-decision.json"
    output.write_text(json.dumps(decision(example(), {"service-identification", "operator-trust"}), indent=2) + "\n", encoding="utf-8")
    print(output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
