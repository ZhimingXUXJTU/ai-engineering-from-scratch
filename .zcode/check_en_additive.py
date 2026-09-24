"""Verify that annotated en.md files remain pure additions over upstream.

Usage: python .zcode/check_en_additive.py [lesson_dir ...]
Without args, checks every phases/*/*/docs/en.md that differs from upstream-snap.
Pure-additive means: every line removed vs upstream must reappear as a prefix
of a corresponding added line (e.g. trailing " | 中文"), and extra lines are
insertions only. Any deletion or mid-line edit is reported.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASE = "upstream-snapshot"


def hunks(base_lines, cur_lines):
    """Yield (removed, added) line lists using simple Myers-free diff via difflib."""
    import difflib
    sm = difflib.SequenceMatcher(a=base_lines, b=cur_lines, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            yield base_lines[i1:i2], cur_lines[j1:j2]


def check(path: Path) -> list[str]:
    rel = path.relative_to(REPO).as_posix()
    base = subprocess.run(
        ["git", "show", f"{BASE}:{rel}"], cwd=REPO, capture_output=True, text=True
    ).stdout
    if not base:
        return [f"{rel}: no upstream counterpart (new file? OK)"]
    cur = path.read_text(encoding="utf-8")
    issues = []
    # Global multiset check: every upstream line must survive as-is or as the
    # prefix of an annotated line ("... | 中文"). Hunk-local diffing mispairs
    # when annotation blocks are inserted between adjacent English lines.
    pool = list(cur.splitlines())
    for r in base.splitlines():
        hit = next((k for k, a in enumerate(pool) if a == r or a.startswith(r)), None)
        if hit is None:
            issues.append(f"removed/edited: {r[:90]!r}")
        else:
            pool.pop(hit)
    return issues


def main():
    targets = sys.argv[1:]
    if not targets:
        out = subprocess.run(
            ["git", "diff", "--name-only", BASE], cwd=REPO, capture_output=True, text=True
        ).stdout.splitlines()
        targets = [p for p in out if p.endswith("docs/en.md")]
    bad = 0
    for t in targets:
        p = REPO / t if "phases/" in t else REPO / Path(t)
        p = Path(p)
        if not p.exists():
            continue
        issues = check(p)
        if any("no upstream counterpart" not in i for i in issues):
            bad += 1
            print(f"FAIL {t}")
            for i in issues[:5]:
                print(f"   {i}")
        elif issues:
            pass  # new file note, fine
    print(f"checked {len(targets)} en.md files, {bad} with modifications beyond pure addition")


if __name__ == "__main__":
    main()
