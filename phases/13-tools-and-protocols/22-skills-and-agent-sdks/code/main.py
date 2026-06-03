"""Phase 13 Lesson 22 - SKILL.md loader and agent bundle demo.

Skills 与 Agent SDK (Skills and Agent SDKs)
核心概念：MCP 定义"有什么工具"，Skills 定义"如何完成任务"。
Anthropic Skills（SKILL.md）、AGENTS.md（项目级Agent上下文）、OpenAI Apps SDK 是2026年三大标准。
AI 应用对应：Skills 是 Claude Code 等 Agent 的工作单元，AGENTS.md 已在60000+仓库中使用。

Parses SKILL.md files with a stdlib YAML-frontmatter parser (no pyyaml),
builds an in-memory skill registry, and simulates an agent loop that loads
a skill by name and uses it to prefix the system prompt.

Skills live under ./skills/*/SKILL.md (created in /tmp for this demo).

Run: python code/main.py
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


SKILL_ROOT = Path("/tmp/lesson-21-skills")


# ------------------------------------------------------------------
# 测试用技能 fixture (toy fixture skills)
# ------------------------------------------------------------------

RELEASE_NOTES_SKILL = """\
---
name: release-notes-writer
description: Write a changelog entry for the latest merged PRs following this project's style.
---

# Release notes writer

When invoked, run these steps:

1. List PRs merged since the last tag.
2. Group by label: feature, fix, chore, docs.
3. For each PR, write one line: `- <title> (#<num>)`.
4. Draft the release notes and stage them in CHANGELOG.md.

If the user says "ship", run `git tag vX.Y.Z` and `gh release create`.

See style-guide.md for the house style rules.
"""

RELEASE_STYLE = """\
# Release notes style guide

- One line per PR. No prose.
- Feature entries first; fixes second; chores third; docs last.
- Skip chores from public changelog.
"""

PR_REVIEW_SKILL = """\
---
name: pr-reviewer
description: Review a PR diff against the project's style guide and open clarifying comments.
---

# PR reviewer

Steps:

1. Fetch the PR diff.
2. Identify rules from AGENTS.md that the diff touches.
3. Write one comment per clear violation.
"""


def setup_fixtures() -> None:
    """创建测试用 SKILL.md 文件到 /tmp 目录。"""
    SKILL_ROOT.mkdir(parents=True, exist_ok=True)
    rn = SKILL_ROOT / "release-notes-writer"
    rn.mkdir(exist_ok=True)
    (rn / "SKILL.md").write_text(RELEASE_NOTES_SKILL)
    (rn / "style-guide.md").write_text(RELEASE_STYLE)
    pr = SKILL_ROOT / "pr-reviewer"
    pr.mkdir(exist_ok=True)
    (pr / "SKILL.md").write_text(PR_REVIEW_SKILL)


# ------------------------------------------------------------------
# 加载器 (loader)
# ------------------------------------------------------------------

@dataclass
class Skill:
    name: str
    description: str
    body: str
    root: Path


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """解析 SKILL.md 的 YAML frontmatter：提取 `---` 之间的键值对和正文。"""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_raw = text[4:end]
    body = text[end + 5:]
    fm: dict = {}
    for line in fm_raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, body


def load_skill(folder: Path) -> Skill | None:
    """从文件夹加载 SKILL.md：解析 frontmatter 获取名称和描述。"""
    skill_md = folder / "SKILL.md"
    if not skill_md.exists():
        return None
    text = skill_md.read_text()
    fm, body = parse_frontmatter(text)
    if "name" not in fm:
        return None
    return Skill(name=fm["name"], description=fm.get("description", ""),
                 body=body.strip(), root=folder)


def discover_skills(root: Path) -> dict[str, Skill]:
    """技能发现：扫描目录下的所有 SKILL.md，构建按名称索引的注册表。"""
    registry: dict[str, Skill] = {}
    if not root.exists():
        return registry
    for item in sorted(root.iterdir()):
        if item.is_dir():
            s = load_skill(item)
            if s:
                registry[s.name] = s
    return registry


def read_subresource(skill: Skill, filename: str) -> str:
    """渐进式披露：按需读取技能目录下的子资源文件。"""
    path = skill.root / filename
    if not path.exists():
        return f"(no such subresource: {filename})"
    return path.read_text()


# ------------------------------------------------------------------
# 演示 Agent 循环 (demo agent loop)
# ------------------------------------------------------------------

def agent_run(skill: Skill, user_task: str) -> str:
    """模拟 Agent 运行：加载技能，按需拉取子资源，构建系统提示。"""
    print(f"  [loader] loading skill '{skill.name}'")
    print(f"  [loader] progressive disclosure: read style-guide only if needed")
    system_prompt = f"""You are an assistant with the {skill.name} skill loaded.

Skill instructions:
{skill.body}

User task: {user_task}
"""
    # demonstrate progressive disclosure
    if "style-guide" in skill.body.lower():
        style = read_subresource(skill, "style-guide.md")
        print(f"  [loader] subresource pulled ({len(style)} bytes)")
        system_prompt += f"\n\nAdditional style guide:\n{style}"
    return system_prompt


def demo() -> None:
    print("=" * 72)
    print("PHASE 13 LESSON 21 - SKILLS AND AGENT SDK LOADER")
    print("=" * 72)

    setup_fixtures()

    print(f"\n--- discovery under {SKILL_ROOT} ---")
    skills = discover_skills(SKILL_ROOT)
    for name, s in skills.items():
        print(f"  {name:25s} -> {s.description}")

    print(f"\n--- invoke release-notes-writer with a fake user task ---")
    prompt = agent_run(skills["release-notes-writer"],
                       "draft the 1.4.0 release notes")
    print(f"\n[the system prompt the agent would send to the model]")
    print("-" * 72)
    print(prompt[:600] + "...")

    print("\n--- AGENTS.md + SKILL.md + MCP : the three-layer stack ---")
    print("  AGENTS.md (repo root)   -> project conventions at session start")
    print("  SKILL.md (./skills/*/)  -> reusable workflows on demand")
    print("  MCP server              -> tools the skill invokes (Phase 13 / 06-14)")


if __name__ == "__main__":
    demo()
