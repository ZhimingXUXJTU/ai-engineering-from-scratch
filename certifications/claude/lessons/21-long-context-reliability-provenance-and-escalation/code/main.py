"""课程：Make Large Context Observable | 让长上下文可观测
路径：certifications/claude/lessons/21-long-context-reliability-provenance-and-escalation
核心概念：大上下文窗口装得下证据，却不能保证证据被注意到、仍然最新、权威且安全。
本文件校验 reliability-packet.md 的标题与证据关键词：覆盖率显式（18/24 加未处理
计数）、来源可溯信封（源版本、内容类型、位置）、partial 结果不被伪装成完成、
冲突绑定负责人、升级点出缺失的决定并给出安全的下一步、人工评审带随机抽检。
AI 应用对应：长上下文 Agent 系统的最小可靠性验收器——用清单（manifest）保住
持久状态、用三态契约（complete/partial/blocked）暴露不确定性、用证据校准置信度，
而不是让一份圆滑的摘要把缺失的工作藏起来。

Companion validator for this lesson's docs/en.md reliability packet.
"""

from __future__ import annotations

import json
from pathlib import Path


ARTIFACT = Path(__file__).resolve().parents[1] / "outputs" / "reliability-packet.md"
REQUIRED_HEADINGS = (
    "## Scope and Coverage",
    "## Provenance Envelope",
    "## Partial Result",
    "## Conflict",
    "## Escalation",
    "## Human Review",
)
REQUIRED_EVIDENCE = {
    "coverage": ("18 of 24", "omitted"),
    "provenance": ("source version", "content type", "location"),
    "escalation": ("owner", "safe next action"),
    "review": ("random sample",),
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
    return {"status": "ready_for_bounded_review" if not findings else "blocked", "score": max(0, 100 - 12 * len(findings)), "findings": findings}


def validate_artifact(path: Path = ARTIFACT) -> dict[str, object]:
    return validate_text(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(validate_artifact(), indent=2))
