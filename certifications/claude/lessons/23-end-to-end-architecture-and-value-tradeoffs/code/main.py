# 课程：End-to-End Architecture and Value Tradeoffs | 端到端架构与价值权衡
# 路径：certifications/claude/lessons/23-end-to-end-architecture-and-value-tradeoffs
# 核心概念：架构决策包的"就绪门"校验——决策（Decision）、候选打分（Candidate
# Scores）、硬门（Hard Gates）、失败路径（Failure Paths）、被拒方案（Rejected
# Alternatives）与逆转条件（Reversal Condition）缺一不可；硬约束不许被高分平均掉。
# AI 应用对应：真实 AI 系统架构评审的最小门禁——四模式（增强调用/确定性工作流/
# Agent/多 Agent）选最小合适者，对应"选最简架构、先结构修复后提示词补丁"的决策纪律。
"""Companion validator for this lesson's docs/en.md architecture decision."""

from __future__ import annotations

import json
from pathlib import Path


ARTIFACT = Path(__file__).resolve().parents[1] / "outputs" / "architecture-decision.md"
REQUIRED_HEADINGS = (
    "## Decision",
    "## Candidate Scores",
    "## Hard Gates",
    "## Failure Paths",
    "## Rejected Alternatives",
    "## Reversal Condition",
)
REQUIRED_EVIDENCE = {
    "patterns": ("workflow", "agent"),
    "tradeoffs": ("latency", "safety"),
    "operations": ("rollback", "owner"),
    "decision": ("reversal",),
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
    return {"status": "ready_for_decision_review" if not findings else "blocked", "score": max(0, 100 - 12 * len(findings)), "findings": findings}


def validate_artifact(path: Path = ARTIFACT) -> dict[str, object]:
    return validate_text(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(validate_artifact(), indent=2))
