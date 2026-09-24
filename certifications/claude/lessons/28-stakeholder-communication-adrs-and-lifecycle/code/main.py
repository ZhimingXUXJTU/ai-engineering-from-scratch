"""课程：Stakeholder Communication, ADRs, and Lifecycle Ownership | 干系人沟通、ADR 与生命周期归属
路径：certifications/claude/lessons/28-stakeholder-communication-adrs-and-lifecycle
核心概念：交付交接包的确定性验收器——校验产物是否包含六个必备章节（高管决策、ADR、
契约索引、运营就绪、归属地图、翻转条件）、证据关键词（回滚/告警/SLO、被否决/翻转、
负责人、桌面演练），并拦截未解决的占位符（tbd/todo/[replace）。
AI 应用对应：真实架构交付中"交接验收门"的最小模型——让干系人沟通与生命周期归属
可机检、可回归，而不是靠人眼读 Markdown 确认架构已经交付。

Companion validator for this lesson's docs/en.md delivery packet.
"""

from __future__ import annotations

import json
from pathlib import Path


ARTIFACT = Path(__file__).resolve().parents[1] / "outputs" / "delivery-handoff-packet.md"
REQUIRED_HEADINGS = (
    "## Executive Decision",
    "## ADR",
    "## Contract Index",
    "## Operational Readiness",
    "## Ownership Map",
    "## Reversal Condition",
)
REQUIRED_EVIDENCE = {
    "operations": ("rollback", "alert", "slo"),
    "decision": ("rejected", "reversal"),
    "accountability": ("owner",),
    "drill": ("tabletop",),
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
    return {"status": "ready_for_handoff" if not findings else "blocked", "score": max(0, 100 - 12 * len(findings)), "findings": findings}


def validate_artifact(path: Path = ARTIFACT) -> dict[str, object]:
    return validate_text(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(validate_artifact(), indent=2))
