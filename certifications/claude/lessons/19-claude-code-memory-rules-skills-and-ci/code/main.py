"""课程：Claude Code Memory, Rules, Skills, and CI | Claude Code 记忆、规则、Skill 与 CI
路径：certifications/claude/lessons/19-claude-code-memory-rules-skills-and-ci
核心概念：把稳定指南放进最窄的真实作用域（CLAUDE.md、导入文件、路径规则、Skill、
子代理、钩子、settings 分层选择）；不可失败的约束交给确定性钩子与无头 CI。本文件
校验 configuration-scope-audit.md 的标题与证据关键词，检查 migration-review-skill
软件包的结构：SKILL.md 的 allowed-tools 保持窄授权、check_scope.py 对迁移路径
放行并对路径穿越拒绝、子代理契约含 maxTurns 与 worktree 隔离。
AI 应用对应：团队级 Claude Code 配置治理的最小验收器——配置即代码，改配置要过
与改代码同级的评审、fixture 测试和 CI 证据；迁移评审 Skill 是可直接装进
.claude/skills/ 的交付产物。

Companion validator for this lesson's docs/en.md configuration audit.
"""

from __future__ import annotations

import json
from pathlib import Path


ARTIFACT = Path(__file__).resolve().parents[1] / "outputs" / "configuration-scope-audit.md"
SKILL_DIR = Path(__file__).resolve().parents[1] / "outputs" / "migration-review-skill"
SKILL_FILE = SKILL_DIR / "SKILL.md"
SCRIPT_FILE = SKILL_DIR / "scripts" / "check_scope.py"
REFERENCE_FILE = SKILL_DIR / "references" / "review-checklist.md"
REQUIRED_HEADINGS = (
    "## Instruction Hierarchy",
    "## Path Rule Fixtures",
    "## Skill and Command",
    "## Skill Package",
    "## Subagent Contract",
    "## Plugin Distribution",
    "## Hooks",
    "## Headless CI",
    "## Remediation",
)
REQUIRED_EVIDENCE = {
    "ci": ("fresh checkout", "read-only", "structured"),
    "fixtures": ("allow", "deny"),
    "enforcement": ("pre-write hook", "deterministic"),
    "skill": ("skill.md", "allowed-tools", "scripts/check_scope.py", "references/review-checklist.md"),
    "subagent": ("/agents", "maxturns", "isolation: worktree", "blockers", "next_step"),
    "distribution": (".claude/settings.json", "extraknownmarketplaces", "enabledplugins", "managed settings"),
    "hook protocol": ("exit 0", "exit 2", "permissionrequest", "pretooluse"),
    "official ci": ("code review", "anthropics/claude-code-action@v1"),
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
    return {"status": "configuration_verified" if not findings else "blocked", "score": max(0, 100 - 12 * len(findings)), "findings": findings}


def validate_artifact(path: Path = ARTIFACT) -> dict[str, object]:
    result = validate_text(path.read_text(encoding="utf-8"))
    skill_result = validate_skill()
    findings = list(result["findings"]) + list(skill_result["findings"])
    return {
        "status": "configuration_verified" if not findings else "blocked",
        "score": max(0, 100 - 8 * len(findings)),
        "findings": findings,
    }


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return {}
    raw = text[4:].split("\n---\n", 1)[0]
    values: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            return {}
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def validate_skill(skill_dir: Path = SKILL_DIR) -> dict[str, object]:
    findings: list[str] = []
    paths = {
        "SKILL.md": skill_dir / "SKILL.md",
        "scripts/check_scope.py": skill_dir / "scripts" / "check_scope.py",
        "references/review-checklist.md": skill_dir / "references" / "review-checklist.md",
    }
    for label, path in paths.items():
        if not path.is_file():
            findings.append(f"missing skill file: {label}")
    if findings:
        return {"status": "blocked", "findings": findings}

    text = paths["SKILL.md"].read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)
    if metadata.get("name") != "migration-review":
        findings.append("skill name must be migration-review")
    description = metadata.get("description", "").lower()
    if not all(term in description for term in ("migration", "when")):
        findings.append("skill description must state what it does and when to trigger")
    allowed_tools = metadata.get("allowed-tools", "")
    if "${CLAUDE_SKILL_DIR}/scripts/check_scope.py" not in allowed_tools:
        findings.append("allowed-tools must scope the bundled checker")
    if "Bash(*)" in allowed_tools:
        findings.append("allowed-tools must not grant broad Bash")
    for reference in ("scripts/check_scope.py", "references/review-checklist.md"):
        if reference not in text:
            findings.append(f"SKILL.md must route to {reference}")
    if any(marker in text.lower() for marker in ("tbd", "todo", "[replace")):
        findings.append("skill contains unresolved placeholder")
    return {"status": "valid" if not findings else "blocked", "findings": findings}


if __name__ == "__main__":
    print(json.dumps(validate_artifact(), indent=2))
