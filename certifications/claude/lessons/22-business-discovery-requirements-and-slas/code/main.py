# 课程：Business Discovery, Requirements, and SLAs | 业务调研、需求与 SLA
# 路径：certifications/claude/lessons/22-business-discovery-requirements-and-slas
# 核心概念：调研简报的"就绪门"校验——一份 discovery brief 必须同时具备结果
# （基线/目标/负责人）、服务等级（SLI/SLO）、分类（constraint/estimate）与范围
# （非目标）证据；事实、估计、偏好、约束不得混写，TBD/TODO 占位符直接判 blocked。
# AI 应用对应：真实 AI 项目立项评审的最小门禁——调研不充分就不进入架构选型，
# 对应架构师"先降低歧义、再选技术"的决策纪律。
"""Companion validator for this lesson's docs/en.md discovery brief."""

from __future__ import annotations

import json
from pathlib import Path


ARTIFACT = Path(__file__).resolve().parents[1] / "outputs" / "discovery-brief.md"
REQUIRED_HEADINGS = (
    "## Outcome",
    "## Requirements",
    "## Data and Authority",
    "## Measures",
    "## Assumptions",
    "## Non-Goals",
)
REQUIRED_EVIDENCE = {
    "outcome": ("baseline", "target", "owner"),
    "service levels": ("sli", "slo"),
    "classification": ("constraint", "estimate"),
    "scope": ("autonomous sending",),
}


def validate_text(text: str) -> dict[str, object]:
    lowered = " ".join(text.lower().split())
    findings = [f"missing heading: {heading}" for heading in REQUIRED_HEADINGS if heading not in text]
    for label, terms in REQUIRED_EVIDENCE.items():
        missing = [term for term in terms if term not in lowered]
        if missing:
            findings.append(f"missing {label}: {', '.join(missing)}")
    if any(marker in lowered for marker in ("tbd", "todo", "[replace")):
        findings.append("unresolved placeholder")
    return {"status": "ready_for_architecture" if not findings else "blocked", "score": max(0, 100 - 12 * len(findings)), "findings": findings}


def validate_artifact(path: Path = ARTIFACT) -> dict[str, object]:
    return validate_text(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(validate_artifact(), indent=2))
