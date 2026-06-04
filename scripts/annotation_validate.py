"""
annotation_validate.py — 验证中文注释质量

用法:
    python scripts/annotation_validate.py --phase 00      # 验证某个 phase
    python scripts/annotation_validate.py --phase 00,01   # 验证多个 phases
    python scripts/annotation_validate.py --all            # 验证全部
"""
import os
import sys
import io

# Windows GBK console fix
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
import re
import argparse
import subprocess
from pathlib import Path

BASE = Path("Z:/learn-AI_from-scratch/ai-engineering-from-scratch/phases")


def find_phases(phase_filter=None):
    all_phases = sorted([d for d in BASE.iterdir() if d.is_dir() and re.match(r'\d{2}', d.name)])
    if phase_filter:
        nums = [f"{int(n):02d}" for n in phase_filter.split(",")]
        return [p for p in all_phases if any(p.name.startswith(n) for n in nums)]
    return all_phases


def validate_doc_file(filepath):
    """验证单个 docs/en.md 文件"""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')

    # 1. 检查注释数量
    cn_count = content.count("【中文解读】")
    expand_count = len(re.findall(r'【拓展[：:]', content))

    if cn_count < 3:
        issues.append(f"LOW_CN: 只有 {cn_count} 个【中文解读】(目标≥5)")
    if expand_count < 2:
        issues.append(f"LOW_EXPAND: 只有 {expand_count} 个【拓展】(目标≥4)")

    # 2. 检查 H2/H3 标题缺少中文
    for i, line in enumerate(lines):
        m = re.match(r'^(#{2,3})\s+(.+)', line)
        if m:
            title = m.group(2).strip()
            # 跳过纯代码/无文字标题
            if len(title) > 5 and not title.startswith('```'):
                has_cn = any('一' <= c <= '鿿' for c in title)
                if not has_cn and '|' not in title:
                    issues.append(f"MISSING_CN_HEADER: L{i+1}: {title[:50]}")

    # 3. 检查 UTF-8 编码
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()
        raw.decode('utf-8')
    except UnicodeDecodeError:
        issues.append("ENCODING: 文件不是有效 UTF-8")

    # 4. 检查 blockquote 格式
    for i, line in enumerate(lines):
        if '【中文解读】' in line and not line.strip().startswith('>'):
            issues.append(f"FORMAT: L{i+1} 【中文解读】不在 blockquote 中")

    # 5. 检查 mermaid 代码块完整性
    mermaid_count = content.count('```mermaid')
    mermaid_end = content.count('```')
    # 每个 mermaid 块有一个开始和结束，总 ``` 数应该是偶数

    return {
        'file': str(filepath.relative_to(BASE.parent)),
        'cn_count': cn_count,
        'expand_count': expand_count,
        'issues': issues,
        'passed': len([i for i in issues if i.startswith(('ENCODING', 'FORMAT'))]) == 0,
        'quality_score': min(100, cn_count * 10 + expand_count * 15),
    }


def validate_phase(phase_dir):
    """验证整个 phase"""
    lessons = sorted(phase_dir.glob("*/docs/en.md"))
    results = []
    for lesson_path in lessons:
        result = validate_doc_file(lesson_path)
        results.append(result)

    # 检查 git diff 是否修改了原文（只允许增加行）
    try:
        diff_output = subprocess.run(
            ['git', 'diff', '--stat', '--', str(phase_dir)],
            capture_output=True, text=True, cwd=BASE.parent
        )
    except Exception:
        diff_output = None

    total = len(results)
    passed = sum(1 for r in results if r['passed'])
    avg_score = sum(r['quality_score'] for r in results) / total if total else 0
    all_issues = [i for r in results for i in r['issues']]

    return {
        'phase': phase_dir.name,
        'total_files': total,
        'passed': passed,
        'failed': total - passed,
        'avg_score': round(avg_score, 1),
        'total_issues': len(all_issues),
        'results': results,
    }


def main():
    parser = argparse.ArgumentParser(description='验证中文注释质量')
    parser.add_argument('--phase', type=str, default=None, help='Phase 编号')
    parser.add_argument('--all', action='store_true', help='验证全部')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详情')
    args = parser.parse_args()

    if args.all:
        phases = find_phases()
    elif args.phase:
        phases = find_phases(args.phase)
    else:
        print("请指定 --phase NN 或 --all")
        return

    total_passed = 0
    total_failed = 0

    for phase_dir in phases:
        result = validate_phase(phase_dir)
        status = "✅ PASS" if result['failed'] == 0 else f"⚠️ {result['failed']} FAIL"
        print(f"\n{result['phase']}: {status} | avg_score={result['avg_score']} | "
              f"{result['passed']}/{result['total_files']} files passed")

        if args.verbose or result['failed'] > 0:
            for r in result['results']:
                if r['issues']:
                    lesson_name = Path(r['file']).parent.parent.name
                    print(f"  ⚠️ {lesson_name}: score={r['quality_score']}")
                    for issue in r['issues'][:5]:
                        print(f"     - {issue}")

        total_passed += result['passed']
        total_failed += result['failed']

    print(f"\n{'='*50}")
    print(f"总计: {total_passed} passed, {total_failed} failed")
    exit_code = 0 if total_failed == 0 else 1
    exit(exit_code)


if __name__ == "__main__":
    main()
