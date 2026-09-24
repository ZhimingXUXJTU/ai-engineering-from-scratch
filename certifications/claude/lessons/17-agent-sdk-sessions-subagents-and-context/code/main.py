"""Companion validator for this lesson's docs/en.md recovery packet.

中文批注（认证课 17）：
课程标题：Agent SDK 会话、子 Agent 与上下文 / Agent SDK Sessions, Subagents, and Context
核心概念：持久外部状态、当前对话上下文、执行历史三者不可混为一个存储；上下文是工作集而非权威数据库；
四种会话操作按失败风险选择（新建/恢复/分叉/压缩），压缩只省体积不保证真相；恢复靠结构化恢复包+
边界重验证+副作用幂等（先对账再重试）；子 Agent 按职责拿最小上下文与受限工具。
AI 应用对应：Claude Agent SDK sessions/subagents/hooks 能力面的治理模型——本校验器检查恢复包的
持久状态、重验证、幂等键与隔离评审，即"断点续跑"契约的可执行版本。
"""

from __future__ import annotations

import json
from pathlib import Path


ARTIFACT = Path(__file__).resolve().parents[1] / "outputs" / "session-recovery-packet.md"
REQUIRED_HEADINGS = (
    "## Goal and Scope",
    "## Durable State",
    "## Revalidation",
    "## Side Effect Reconciliation",
    "## Context Budget",
    "## Independent Review",
)
REQUIRED_EVIDENCE = {
    "checkpoint": ("hash", "manifest"),
    "freshness": ("revalidate",),
    "safe retry": ("idempotency", "unknown outcome"),
    "review": ("isolated", "blocked"),
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
    return {"status": "safe_to_resume" if not findings else "blocked", "score": max(0, 100 - 12 * len(findings)), "findings": findings}


def validate_artifact(path: Path = ARTIFACT) -> dict[str, object]:
    return validate_text(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(validate_artifact(), indent=2))
