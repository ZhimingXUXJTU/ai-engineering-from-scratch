# Lesson program for promoting corrections into durable controls.
# Read: phases/14-agent-engineering/46-turn-feedback-into-system/docs/en.md
# Reference: Basili, Caldiera, and Rombach, The Goal Question Metric Approach.
# Reference: Shinn et al., Reflexion, arXiv:2303.11366.
# Run this file to generate outputs/feedback-ratchet.json.
# 中文标题：把反馈变成系统 (Turn Every Agent Correction into a System Improvement)
# 核心概念：纠正 → 控制的升级规则（按根因关键词选最早责任层：测试/范围/自动化/示例/指令）；
#           归一化根因后做指纹（sha256 前 12 位）去重，同一根因的重复纠正只保留一条控制。
# AI 应用对应：人工纠正不再只留在聊天里——每次纠正被升级为可验证的持久控制并带去重指纹，
#             相当于给 Agent 工作流装上"只进不退"的棘轮，下一次运行从更强的起点开始。
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Correction:
    symptom: str
    cause: str
    recurrence: int
    consequence: str


@dataclass(frozen=True)
class Control:
    target: str
    rule: str
    verification: str
    fingerprint: str
    symptom: str
    cause: str
    recurrence: int
    consequence: str


def choose_target(correction: Correction) -> str:
    text = f"{correction.symptom} {correction.cause}".lower()
    if any(word in text for word in ("incorrect output", "regression", "edge case", "bug")):
        return "test"
    if any(word in text for word in ("scope", "unrelated file", "permission")):
        return "scope"
    if any(word in text for word in ("command", "setup", "environment", "tool")):
        return "automation"
    if any(word in text for word in ("format", "pattern", "example")):
        return "example"
    return "instruction"


def normalize_cause(cause: str) -> str:
    text = cause.strip().rstrip(".").lower()
    implicit = re.fullmatch(r"(.+?) (?:was|were) implicit", text)
    if implicit:
        return f"implicit {implicit.group(1)}"
    unchecked = re.fullmatch(r"(.+?) was described but not checked", text)
    if unchecked:
        return f"unchecked {unchecked.group(1)} description"
    missing = re.fullmatch(r"(.+?) had no (.+)", text)
    if missing:
        return f"missing {missing.group(2)} for {missing.group(1)}"
    return text


def promote(correction: Correction) -> Control:
    target = choose_target(correction)
    rule = f"Prevent {normalize_cause(correction.cause)}"
    verification = {
        "test": "Run the new regression test",
        "scope": "Run the scope checker",
        "automation": "Run the setup or tool preflight",
        "example": "Compare the output with the canonical example",
        "instruction": "Run the instruction linter and scenario check",
    }[target]
    digest = hashlib.sha256(f"{target}|{rule}".encode()).hexdigest()[:12]
    return Control(
        target,
        rule,
        verification,
        digest,
        correction.symptom,
        correction.cause,
        correction.recurrence,
        correction.consequence,
    )


def ratchet(corrections: list[Correction]) -> list[Control]:
    promoted: dict[str, Control] = {}
    for correction in corrections:
        if correction.recurrence < 1:
            continue
        control = promote(correction)
        promoted[control.fingerprint] = control
    return sorted(promoted.values(), key=lambda item: (item.target, item.fingerprint))


def example() -> list[Correction]:
    return [
        Correction("Agent edited an unrelated file", "scope was described but not checked", 2, "review churn"),
        Correction("A regression escaped", "edge case had no executable example", 1, "user-visible failure"),
        Correction("Setup command failed", "environment assumptions were implicit", 3, "lost session"),
    ]


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "outputs" / "feedback-ratchet.json"
    output.write_text(json.dumps([asdict(item) for item in ratchet(example())], indent=2) + "\n", encoding="utf-8")
    print(output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
