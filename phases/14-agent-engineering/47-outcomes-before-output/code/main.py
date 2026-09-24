# Lesson program for framing observable outcomes before choosing outputs.
# Read: phases/14-agent-engineering/47-outcomes-before-output/docs/en.md
# Reference: Nuseibeh and Easterbrook, Requirements Engineering: A Roadmap, 2000.
# Reference: Dardenne, van Lamsweerde, and Fickas, Goal-Directed Requirements Acquisition, 1993.
# Run this file to generate outputs/outcome-frame.json.
# 中文标题：结果先于产出 (Define the Outcome Before You Choose the Output)
# 核心概念：结果框架六段——用户/情境/当前行为/期望结果/约束/非目标；校验器拒绝空字段和
#           "解决方案泄漏"（拟议产出出现在期望结果句里）；出口问题是"什么证据能证明结果达成"。
# AI 应用对应：在决定"造什么 AI 产品"之前先钉住"世界要变好什么"；泄漏检测防止第一个
#             被想象出的产物（如"事故助手"）硬化成范围，让手册、数据修复、小改动同台竞争。
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class OutcomeFrame:
    user: str
    situation: str
    current_behavior: str
    desired_outcome: str
    constraints: list[str]
    non_goals: list[str]
    proposed_output: str = ""


def validate(frame: OutcomeFrame) -> list[str]:
    issues: list[str] = []
    for name in ("user", "situation", "current_behavior", "desired_outcome"):
        if not getattr(frame, name).strip():
            issues.append(f"{name} is empty")
    if not frame.constraints:
        issues.append("constraints are empty")
    if not frame.non_goals:
        issues.append("non-goals are empty")
    if frame.proposed_output and frame.proposed_output.lower() in frame.desired_outcome.lower():
        issues.append("desired outcome names the proposed output")
    return issues


def decision(frame: OutcomeFrame) -> dict:
    issues = validate(frame)
    return {
        "status": "ready-to-discover" if not issues else "needs-framing",
        "issues": issues,
        "frame": asdict(frame),
        "next_question": f"What evidence would show that the desired outcome was achieved for the {frame.user}?",
    }


def example() -> OutcomeFrame:
    return OutcomeFrame(
        user="on-call engineer",
        situation="a production alert arrives during an incident",
        current_behavior="searches three dashboards before finding the affected service",
        desired_outcome="identifies the failing service and safe next action within two minutes",
        constraints=["read-only during diagnosis", "must preserve the audit trail"],
        non_goals=["automatic remediation", "replacing the incident commander"],
        proposed_output="incident assistant",
    )


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "outputs" / "outcome-frame.json"
    output.write_text(json.dumps(decision(example()), indent=2) + "\n", encoding="utf-8")
    print(output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
