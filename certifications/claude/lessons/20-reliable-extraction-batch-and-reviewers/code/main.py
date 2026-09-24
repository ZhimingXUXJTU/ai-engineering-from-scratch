"""课程：Reliable Extraction, Batch, and Independent Reviewers | 可靠抽取、批处理与独立评审者
路径：certifications/claude/lessons/20-reliable-extraction-batch-and-reviewers
核心概念：合法 JSON 只证明形状活了下来，不证明事实活了下来。本文件校验
extraction-review-report.md 的标题与证据关键词：四层校验（语法/schema/语义/
来源可溯）齐备、未知值用 null 表示、批处理用 custom_id 对账乱序结果、
生成者与独立评审者分离、分歧进入人工裁决，以及官方批处理事实
（50% 成本降低、24 小时窗口、无保证延迟 SLA）原样在场。
AI 应用对应：生产级抽取流水线的最小验收器——按"每条被接受记录"而不是
"每条输出记录"算质量；评审者是一台仪器，人工裁决才是分歧的终点。

Companion validator for this lesson's docs/en.md extraction report.
"""

from __future__ import annotations

import json
from pathlib import Path


ARTIFACT = Path(__file__).resolve().parents[1] / "outputs" / "extraction-review-report.md"
REQUIRED_HEADINGS = (
    "## Extraction Contract",
    "## Batch Manifest",
    "## Validation Layers",
    "## Reviewer Findings",
    "## Adjudication",
    "## Metrics",
)
REQUIRED_EVIDENCE = {
    "validation": ("syntax", "schema", "semantic", "provenance"),
    "absence": ("null",),
    "reconciliation": ("custom_id", "shuffled"),
    "batch_contract": ("50%", "24-hour", "no guaranteed latency"),
    "review": ("independent", "adjudication"),
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
    return {"status": "ready_for_adjudication" if not findings else "blocked", "score": max(0, 100 - 12 * len(findings)), "findings": findings}


def validate_artifact(path: Path = ARTIFACT) -> dict[str, object]:
    return validate_text(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(validate_artifact(), indent=2))
