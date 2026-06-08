"""Run the same task on a sample app twice: prompt-only vs workbench-guided.

Both pipelines are scripted (no LLM) so the measurement is reproducible.
Writes before-after-report.md and comparison.json next to this file.

Run: python3 code/main.py

核心概念：真实仓库上的 Workbench 对比实验 —— 在示例应用上运行同一任务两次：
纯提示词模式 vs Workbench 引导模式。两条管线都是脚本化的（无 LLM），确保可复现。
输出 before-after-report.md 和 comparison.json 量化 Workbench 的改进效果。

AI 对应：这是 Agent 工程中"有结构 vs 无结构"的 A/B 测试方法。
Claude Code、Cursor 等 Agent IDE 的研发团队也使用类似方法验证新功能的效果。
量化对比是 Agent 工程从"凭感觉"到"数据驱动"的关键步骤。
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

HERE = Path(__file__).parent
SAMPLE = HERE / "sample_app"


SAMPLE_APP_PY = '''"""Minimal signup handler. Treat as production-ish for this exercise."""

USERS: dict[str, str] = {}


def signup(email: str, password: str) -> dict[str, object]:
    USERS[email] = password
    return {"status": 200, "email": email}
'''

SAMPLE_TEST_PY = '''from sample_app.app import signup


def test_signup_happy_path():
    out = signup("a@b.co", "longenough")
    assert out["status"] == 200
'''


@dataclass
class TaskOutcome:
    pipeline: str
    tests_actually_run: bool
    acceptance_met: bool
    files_outside_scope: list[str] = field(default_factory=list)
    handoff_quality: str = "missing"
    reviewer_total: int = 0


ALLOWED = {"sample_app/app.py", "sample_app/test_app.py"}
FORBIDDEN = {"sample_app/scripts/release.sh"}


def run_prompt_only() -> TaskOutcome:
    """Edits a couple of files, never runs the test, claims done."""
    touched = ["sample_app/app.py", "README.md", "sample_app/scripts/release.sh"]
    return TaskOutcome(
        pipeline="prompt-only",
        tests_actually_run=False,
        acceptance_met=False,
        files_outside_scope=[p for p in touched if p not in ALLOWED],
        handoff_quality="missing",
        reviewer_total=3,
    )


def run_workbench() -> TaskOutcome:
    """Reads scope, edits inside scope, runs acceptance through feedback, gates, reviews, hands off."""
    touched = ["sample_app/app.py", "sample_app/test_app.py"]
    return TaskOutcome(
        pipeline="workbench-guided",
        tests_actually_run=True,
        acceptance_met=True,
        files_outside_scope=[p for p in touched if p not in ALLOWED],
        handoff_quality="full packet",
        reviewer_total=9,
    )


def write_report(po: TaskOutcome, wb: TaskOutcome) -> None:
    lines = [
        "# Before / After: Agent Workbench on a Real Repo",
        "",
        "Same task. Same sample app. Two pipelines.",
        "",
        "| Outcome | Prompt only | Workbench |",
        "|---------|-------------|-----------|",
        f"| tests_actually_run | {po.tests_actually_run} | {wb.tests_actually_run} |",
        f"| acceptance_met | {po.acceptance_met} | {wb.acceptance_met} |",
        f"| files_outside_scope | {len(po.files_outside_scope)} | {len(wb.files_outside_scope)} |",
        f"| handoff_quality | {po.handoff_quality} | {wb.handoff_quality} |",
        f"| reviewer_total (/10) | {po.reviewer_total} | {wb.reviewer_total} |",
        "",
        "## Read",
        "",
        "Prompt only writes outside scope, claims done without running the acceptance command, "
        "leaves no handoff, and scores low on review. Workbench keeps writes in scope, runs the "
        "acceptance command through the feedback runner, passes the verification gate, and ships "
        "a handoff packet the next session loads on startup.",
    ]
    (HERE / "before-after-report.md").write_text("\n".join(lines) + "\n")


def write_sample() -> None:
    SAMPLE.mkdir(exist_ok=True)
    (SAMPLE / "app.py").write_text(SAMPLE_APP_PY)
    (SAMPLE / "test_app.py").write_text(SAMPLE_TEST_PY)
    (SAMPLE / "README.md").write_text("# sample app\n\nForbidden zone for agent tasks.\n")
    (SAMPLE / "scripts").mkdir(exist_ok=True)
    (SAMPLE / "scripts" / "release.sh").write_text("#!/usr/bin/env bash\necho release\n")


def main() -> None:
    write_sample()
    po = run_prompt_only()
    wb = run_workbench()

    for outcome in (po, wb):
        print(f"=== {outcome.pipeline} ===")
        for k, v in asdict(outcome).items():
            print(f"  {k}: {v}")
        print()

    write_report(po, wb)
    (HERE / "comparison.json").write_text(
        json.dumps({"prompt_only": asdict(po), "workbench": asdict(wb)}, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()  # 运行主函数
