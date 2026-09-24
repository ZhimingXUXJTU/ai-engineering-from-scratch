# Lesson program for evidence-based planning and dependency scheduling.
# Read: phases/14-agent-engineering/44-plan-from-evidence/docs/en.md
# Reference: PERT, U.S. Navy Special Projects Office, 1958.
# Reference: CPM, Kelley and Walker, Eastern Joint Computer Conference, 1959.
# Run this file to generate outputs/evidence-plan.json.
# 中文标题：从证据出发做计划 (Build an Evidence-Backed Execution Plan)
# 核心概念：工作项五要素——标识符/最小改动/证据（仓库凭据）/依赖/证明；校验器拒绝缺证据、缺证明、
#           依赖悬空和循环依赖的计划；拓扑排序把工作项切成可并行的"执行波次"。
# AI 应用对应：让编码 Agent 在改文件之前先产出这份计划，人只审批计划本身；波次即并行委托的依据
#             （同一波互不依赖，可分给多个 Agent）；不可逆动作必须排在其不确定性解决之后。
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class WorkItem:
    id: str
    change: str
    evidence: tuple[str, ...]
    depends_on: tuple[str, ...]
    proof: str


def validate(items: list[WorkItem]) -> list[str]:
    issues: list[str] = []
    ids = [item.id for item in items]
    if len(ids) != len(set(ids)):
        issues.append("work item ids must be unique")
    known = set(ids)
    has_unknown_dependency = False
    for item in items:
        if not item.evidence:
            issues.append(f"{item.id} has no repository evidence")
        if not item.proof.strip():
            issues.append(f"{item.id} has no proof command")
        missing = sorted(set(item.depends_on) - known)
        if missing:
            has_unknown_dependency = True
            issues.append(f"{item.id} depends on unknown items: {', '.join(missing)}")
    if not has_unknown_dependency:
        try:
            execution_waves(items)
        except ValueError as error:
            issues.append(str(error))
    return issues


def execution_waves(items: list[WorkItem]) -> list[list[str]]:
    known = {item.id for item in items}
    for item in items:
        missing = sorted(set(item.depends_on) - known)
        if missing:
            raise ValueError(f"{item.id} depends on unknown items: {', '.join(missing)}")
    remaining = {item.id: set(item.depends_on) for item in items}
    waves: list[list[str]] = []
    completed: set[str] = set()
    while remaining:
        ready = sorted(item_id for item_id, deps in remaining.items() if deps <= completed)
        if not ready:
            cycle = ", ".join(sorted(remaining))
            raise ValueError(f"dependency cycle among: {cycle}")
        waves.append(ready)
        completed.update(ready)
        for item_id in ready:
            del remaining[item_id]
    return waves


def plan_document(items: list[WorkItem]) -> dict:
    issues = validate(items)
    return {
        "status": "ready" if not issues else "blocked",
        "issues": issues,
        "waves": execution_waves(items) if not issues else [],
        "items": [asdict(item) for item in items],
    }


def example() -> list[WorkItem]:
    return [
        WorkItem("contract", "Define duplicate-email behavior", ("tests/test_accounts.py:44",), (), "review contract"),
        WorkItem("implementation", "Reject normalized duplicates", ("app/accounts.py:18",), ("contract",), "python3 -m unittest tests.test_accounts"),
        WorkItem("docs", "Document the 409 response", ("docs/api.md:72",), ("contract",), "python3 scripts/check_links.py"),
        WorkItem("integration", "Run the complete acceptance gate", ("pyproject.toml:31",), ("implementation", "docs"), "python3 -m unittest"),
    ]


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "outputs" / "evidence-plan.json"
    output.write_text(json.dumps(plan_document(example()), indent=2) + "\n", encoding="utf-8")
    print(output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
