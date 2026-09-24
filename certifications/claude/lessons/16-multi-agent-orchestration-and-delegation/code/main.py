"""Companion validator for this lesson's docs/en.md orchestration contract.

中文批注（认证课 16）：
课程标题：多 Agent 编排与委托 / Multi-Agent Orchestration and Delegation
核心概念：多 Agent 架构不解决分解，只把缺失的契约变贵。收益只来自五处：上下文隔离、独立并行、
专用工具、独立评审、保护协调者预算。委托契约要有目标/范围/输入/工具/约束/输出/完成/交接八字段；
子 Agent 必须返回 complete/partial/blocked 三态；确定性前置（顺序、并发、审批）由代码强制而非提示词。
AI 应用对应：Claude Code 任务边界与 Agent SDK 子 Agent 的最小治理模型——本校验器检查任务身份、
依赖顺序、预算、部分状态与评审者隔离，即"委托链契约"的可执行版本。
"""

from __future__ import annotations

import json
from pathlib import Path


ARTIFACT = Path(__file__).resolve().parents[1] / "outputs" / "orchestration-contract.md"
REQUIRED_HEADINGS = (
    "## Goal and Scope",
    "## Tasks and Dependencies",
    "## Result States",
    "## Budgets",
    "## Merge Rules",
    "## Independent Review",
)
REQUIRED_EVIDENCE = {
    "result states": ("complete", "partial", "blocked"),
    "resource boundary": ("budget", "allowed tools"),
    "merge integrity": ("provenance", "conflict"),
    "review isolation": ("isolated",),
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
    return {"status": "ready_for_dry_run" if not findings else "blocked", "score": max(0, 100 - 12 * len(findings)), "findings": findings}


def validate_artifact(path: Path = ARTIFACT) -> dict[str, object]:
    return validate_text(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(validate_artifact(), indent=2))
