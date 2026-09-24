"""课程：Enterprise Governance, Compliance, and Human Review | 企业治理、合规与人工审查
路径：certifications/claude/lessons/27-enterprise-governance-compliance-and-hitl
核心概念：治理是决定"谁可以拿谁的数据冒哪种风险"的系统——本验证器检查治理证据包是否
齐备：风险登记册、数据地图、控制矩阵（预防/检测/纠正/治理四类）、人工审查设计
（触发、有资格的评审者、证据包、队列 SLO）、回退与材料变更触发的重新评估；
没有负责人与测试的控制只是一厢情愿，合规要按特性、配置、协议、区域逐项核实。
AI 应用对应：真实受监管 Claude 工作流（医疗、金融）上线前的治理门禁——
把"有人审""符合 HIPAA"这类口号校验成有归属、有证据、可测试的架构工件，
对应架构师毕业设计的治理与人工审查章节。

Companion validator for this lesson's docs/en.md governance packet."""

from __future__ import annotations

import json
from pathlib import Path


ARTIFACT = Path(__file__).resolve().parents[1] / "outputs" / "governance-control-packet.md"
REQUIRED_HEADINGS = (
    "## Risk Register",
    "## Data Map",
    "## Control Matrix",
    "## Human Review",
    "## Fallback",
    "## Reassessment",
)
REQUIRED_EVIDENCE = {
    "control types": ("preventive", "detective", "corrective", "governance"),
    "accountability": ("owner", "qualified"),
    "operations": ("manual urgent-triage queue", "queue slo"),
    "lifecycle": ("material change",),
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
    return {"status": "ready_for_governance_review" if not findings else "blocked", "score": max(0, 100 - 12 * len(findings)), "findings": findings}


def validate_artifact(path: Path = ARTIFACT) -> dict[str, object]:
    return validate_text(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(validate_artifact(), indent=2))
