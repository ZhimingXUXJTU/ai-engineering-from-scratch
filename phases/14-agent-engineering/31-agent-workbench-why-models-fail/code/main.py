"""Compare a prompt-only run against a workbench-guided run on a tiny repo task.

The agent is a rule-based stub; the point is the surrounding surfaces. Each
surface is wired in for the second run and we count which surfaces would have
caught each failure on the first run.

Run: python3 code/main.py

核心概念：Agent Workbench 失败分析 —— 对比纯提示词运行 vs Workbench 引导运行，
统计每个 Workbench 表面（状态追踪、任务板、规则检查等）能捕获多少个纯提示词运行中的失败。
这是理解"为什么 Agent 需要工作台而非仅靠提示词"的实验方法。

AI 对应：Claude Code、Cursor、Devin 等 Agent IDE 都采用类似的工作台架构，
而非简单的"发提示词给 LLM"。工作台提供的结构化表面（文件追踪、任务管理、
规则约束）显著降低了 Agent 的失败率。这是从"提示词工程"到"Agent 工程"的关键转变。
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


WORKBENCH_SURFACES = [
    "instructions",
    "state",
    "scope",
    "feedback",
    "verification",
    "review",
    "handoff",
]


@dataclass
class RepoTask:
    description: str
    allowed_files: list[str]
    forbidden_files: list[str]
    acceptance: list[str]


@dataclass
class RunResult:
    label: str
    surfaces_present: list[str] = field(default_factory=list)
    files_touched: list[str] = field(default_factory=list)
    tests_run: bool = False
    declared_success: bool = False
    actually_passing: bool = False
    notes: list[str] = field(default_factory=list)

    def missing_surfaces(self) -> list[str]:
        return [s for s in WORKBENCH_SURFACES if s not in self.surfaces_present]


def stub_agent(task: RepoTask, surfaces: list[str]) -> RunResult:
    """Tiny deterministic stand-in for an LLM-backed coding agent."""
    result = RunResult(label="prompt-only" if not surfaces else "workbench")
    result.surfaces_present = list(surfaces)

    has_scope = "scope" in surfaces
    has_state = "state" in surfaces
    has_verification = "verification" in surfaces
    has_feedback = "feedback" in surfaces

    if has_scope:
        result.files_touched = [f for f in task.allowed_files]
    else:
        result.files_touched = [*task.allowed_files, "README.md", "scripts/release.sh"]
        result.notes.append("touched unrelated files because scope was missing")

    if has_feedback:
        result.tests_run = True
        result.notes.append("captured stdout/stderr/exit code from the test run")
    else:
        result.notes.append("never ran the test command, guessed at output")

    if has_verification:
        result.actually_passing = True
        result.declared_success = True
        result.notes.append("verification gate proved acceptance criteria met")
    else:
        result.declared_success = True
        result.actually_passing = False
        result.notes.append("declared success without running acceptance checks")

    if not has_state:
        result.notes.append("no state file written, next session restarts from zero")

    return result


def failure_report(result: RunResult) -> dict[str, object]:
    return {
        "label": result.label,
        "missing_surfaces": result.missing_surfaces(),
        "off_scope_writes": [
            f for f in result.files_touched if f not in {"app.py", "test_app.py"}
        ],
        "tests_run": result.tests_run,
        "declared_success": result.declared_success,
        "actually_passing": result.actually_passing,
        "notes": result.notes,
    }


def main() -> None:
    task = RepoTask(
        description="add input validation to /signup and a passing test",
        allowed_files=["app.py", "test_app.py"],
        forbidden_files=["README.md", "scripts/release.sh"],
        acceptance=["test_app.py::test_signup_rejects_short_password passes"],
    )

    prompt_only = stub_agent(task, surfaces=[])
    workbench = stub_agent(task, surfaces=WORKBENCH_SURFACES)

    print("=== prompt only ===")
    for k, v in failure_report(prompt_only).items():
        print(f"  {k}: {v}")
    print()
    print("=== workbench ===")
    for k, v in failure_report(workbench).items():
        print(f"  {k}: {v}")

    out = Path(__file__).parent.parent / "outputs" / "failure_modes.json"
    out.write_text(json.dumps(failure_report(prompt_only), indent=2) + "\n")
    print(f"\nwrote {out.relative_to(out.parent.parent.parent.parent.parent)}")


if __name__ == "__main__":
    main()  # 运行主函数
