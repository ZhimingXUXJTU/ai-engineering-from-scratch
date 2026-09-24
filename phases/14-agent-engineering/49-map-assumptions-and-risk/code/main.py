# Lesson program: ranks assumptions and selects the next risk-reducing experiment.
# Lesson: phases/14-agent-engineering/49-map-assumptions-and-risk/docs/en.md
# Canonical source: Boehm, Spiral Model, DOI 10.1145/12944.12948.
# Canonical source: Dardenne et al., Goal-Directed Requirements Acquisition.
# 中文标题：映射假设，先拆最大风险 (Map Assumptions and Resolve the Riskiest One First)
# 核心概念：功能背后是可证伪假设（价值/可用性/可行性/生存力/安全性五类）；风险分 =
#           影响 × 不确定性 + 不可逆性（各 1-5），始终先解决"风险最高且仍开放"的那条假设。
# AI 应用对应：AI 功能排期前先画假设地图，用最便宜的决定性实验（如只读回放）替换最贵的猜测；
#             证据支持才有边界地构建，证据反对则重构问题或停止——让证据而不是热情决定顺序。
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Assumption:
    statement: str
    impact: int
    uncertainty: int
    irreversibility: int
    test: str
    evidence: str = ""


def risk_score(item: Assumption) -> int:
    for value in (item.impact, item.uncertainty, item.irreversibility):
        if value not in range(1, 6):
            raise ValueError("risk dimensions must be integers from one to five")
    return item.impact * item.uncertainty + item.irreversibility


def prioritize(items: list[Assumption]) -> list[dict]:
    ranked = sorted(items, key=lambda item: (-risk_score(item), item.statement))
    return [{**asdict(item), "risk_score": risk_score(item), "status": "tested" if item.evidence else "open"} for item in ranked]


def next_experiment(items: list[Assumption]) -> Assumption | None:
    open_items = [item for item in items if not item.evidence]
    return max(open_items, key=risk_score, default=None)


def example() -> list[Assumption]:
    return [
        Assumption("Engineers can identify the right service from alert context", 5, 5, 2, "Replay ten incidents with a read-only prototype"),
        Assumption("Two-minute diagnosis matters", 4, 2, 1, "Interview five incident commanders", "four of five confirmed"),
        Assumption("Automatic remediation is acceptable", 5, 4, 5, "Do not automate; test approval workflow first"),
    ]


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "outputs" / "assumption-map.json"
    output.write_text(json.dumps(prioritize(example()), indent=2) + "\n", encoding="utf-8")
    print(output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
