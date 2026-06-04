"""
batch_headers.py — 批量添加双语标题

对指定 phase 的所有 docs/en.md 文件，自动添加缺失的中文标题。
只处理固定的已知标题模式，不影响其他内容。
"""
import re
import sys
import io
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = Path("Z:/learn-AI_from-scratch/ai-engineering-from-scratch/phases")

# 已知的标题翻译映射
HEADER_MAP = {
    "## The Problem": "## The Problem | 问题引入",
    "## The Concept": "## The Concept | 核心概念",
    "## Build It": "## Build It | 动手实现",
    "## Use It": "## Use It | 用框架实现",
    "## Ship It": "## Ship It | 产出物",
    "## Exercises": "## Exercises | 练习题",
    "## Key Terms": "## Key Terms | 术语速查表",
    "## Connections": "## Connections | 概念关联地图",
    "## Further Reading": "## Further Reading | 延伸阅读",
    "## Common Pitfalls": "## Common Pitfalls | 常见陷阱",
    "## Debugging": "## Debugging | 调试技巧",
    "## Debugging Tips": "## Debugging Tips | 调试技巧",
    "## Summary": "## Summary | 小结",
    "## Next Steps": "## Next Steps | 下一步",
    "## Prerequisites": "## Prerequisites | 前置知识",
}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    modified = 0
    new_lines = []

    for line in lines:
        stripped = line.rstrip()
        # Check if this line matches a known header that needs translation
        matched = False
        for eng, bilingual in HEADER_MAP.items():
            # Exact match (no | already present)
            if stripped == eng or stripped == eng + " ":
                if '|' not in stripped:
                    new_lines.append(bilingual)
                    modified += 1
                    matched = True
                    break
        if not matched:
            new_lines.append(line)

    if modified > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        return modified
    return 0

def main():
    phase_num = sys.argv[1] if len(sys.argv) > 1 else "01"
    phase_dir = BASE / f"{int(phase_num):02d}"
    # Find matching phase directory
    phase_dirs = [d for d in BASE.iterdir() if d.name.startswith(f"{int(phase_num):02d}") and d.is_dir()]
    if not phase_dirs:
        print(f"Phase {phase_num} not found")
        return
    phase_dir = phase_dirs[0]

    total_changes = 0
    files_changed = 0
    for en_md in sorted(phase_dir.glob("*/docs/en.md")):
        changes = process_file(en_md)
        if changes > 0:
            lesson = en_md.parent.parent.name
            print(f"  {lesson}: {changes} headers added")
            total_changes += changes
            files_changed += 1

    print(f"\nTotal: {total_changes} headers added in {files_changed} files")

if __name__ == "__main__":
    main()
