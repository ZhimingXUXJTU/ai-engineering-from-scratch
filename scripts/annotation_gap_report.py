"""
annotation_gap_report.py — 分析每个文件的中文注释差距

用法:
    python scripts/annotation_gap_report.py                 # 全部 phases
    python scripts/annotation_gap_report.py --phase 00      # 只看某个 phase
    python scripts/annotation_gap_report.py --phase 00,01   # 多个 phases
"""
import os
import sys
import io

# Windows GBK console fix
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
import re
import json
import argparse
from pathlib import Path

BASE = Path("Z:/learn-AI_from-scratch/ai-engineering-from-scratch/phases")

# 常用 section 标题的固定中文翻译
FIXED_TRANSLATIONS = {
    "The Problem": "问题引入",
    "The Concept": "核心概念",
    "Build It": "动手实现",
    "Use It": "用框架实现",
    "Ship It": "产出物",
    "Exercises": "练习题",
    "Key Terms": "术语速查表",
    "Learning Objectives": "学习目标",
    "Further Reading": "延伸阅读",
    "Connections": "概念关联地图",
    "Common Pitfalls": "常见陷阱",
    "Debugging": "调试技巧",
    "Connections | 概念关联地图": "概念关联地图",
}


def find_phases(phase_filter=None):
    """获取要处理的 phase 目录列表"""
    all_phases = sorted([d for d in BASE.iterdir() if d.is_dir() and re.match(r'\d{2}', d.name)])
    if phase_filter:
        nums = [f"{int(n):02d}" for n in phase_filter.split(",")]
        return [p for p in all_phases if any(p.name.startswith(n) for n in nums)]
    return all_phases


def analyze_doc_file(filepath):
    """分析单个 docs/en.md 文件的注释差距"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')

    # 统计已有注释
    cn_blocks = content.count("【中文解读】")
    expand_blocks = len(re.findall(r'【拓展[：:]', content))

    # 解析 H2/H3 标题
    headers = []
    for i, line in enumerate(lines):
        m = re.match(r'^(#{2,3})\s+(.+)', line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            has_cn = '|' in title and any('一' <= c <= '鿿' for c in title)
            headers.append({
                'line': i + 1,
                'level': level,
                'title': title,
                'has_cn': has_cn,
            })

    # 找缺少中文的标题
    headers_missing_cn = [h for h in headers if not h['has_cn']]

    # 按 H2 分节，统计每节注释数
    sections = []
    current_section = None
    for h in headers:
        if h['level'] == 2:
            if current_section:
                sections.append(current_section)
            current_section = {
                'header': h['title'],
                'start_line': h['line'],
                'cn_count': 0,
                'expand_count': 0,
            }
        # 统计行数范围内的注释（近似）
    if current_section:
        sections.append(current_section)

    # 更精确地按行统计每节注释
    section_ranges = []
    for i, h in enumerate(headers):
        if h['level'] == 2:
            start = h['line']
            end = headers[i + 1]['line'] if i + 1 < len(headers) else len(lines)
            section_text = '\n'.join(lines[start:end])
            section_ranges.append({
                'header': h['title'],
                'cn': section_text.count("【中文解读】"),
                'expand': len(re.findall(r'【拓展[：:]', section_text)),
            })

    # 计算差距
    target_cn = max(5, len(section_ranges))  # 每节至少1个，最少5个
    target_expand = max(4, len(section_ranges) - 1)  # 略少于节数
    cn_gap = max(0, target_cn - cn_blocks)
    expand_gap = max(0, target_expand - expand_blocks)

    # 代码文件检查
    code_dir = filepath.parent.parent / "code"
    code_files = []
    if code_dir.exists():
        for cf in code_dir.glob("*.py"):
            code_files.append(analyze_code_file(cf))
        for cf in code_dir.glob("*.jl"):
            code_files.append(analyze_code_file(cf, lang="julia"))
        for cf in code_dir.glob("*.ts"):
            code_files.append(analyze_code_file(cf, lang="typescript"))
        for cf in code_dir.glob("*.rs"):
            code_files.append(analyze_code_file(cf, lang="rust"))

    return {
        'file': str(filepath.relative_to(BASE.parent)),
        'cn_blocks': cn_blocks,
        'expand_blocks': expand_blocks,
        'target_cn': target_cn,
        'target_expand': target_expand,
        'cn_gap': cn_gap,
        'expand_gap': expand_gap,
        'headers_total': len(headers),
        'headers_missing_cn': len(headers_missing_cn),
        'missing_headers': [{'line': h['line'], 'title': h['title']} for h in headers_missing_cn[:10]],
        'sections': section_ranges,
        'code_files': code_files,
        'needs_work': cn_gap > 0 or expand_gap > 0 or len(headers_missing_cn) > 2,
    }


def analyze_code_file(filepath, lang="python"):
    """分析代码文件的中文注释情况"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    cn_comments = len(re.findall(r'[一-鿿]', content))
    expand_in_code = len(re.findall(r'【拓展[：:]', content))

    # 统计函数/类定义数
    if lang == "python":
        defs = len(re.findall(r'^\s*(def |class )', content, re.MULTILINE))
    elif lang == "julia":
        defs = len(re.findall(r'^(function |struct |mutable struct )', content, re.MULTILINE))
    else:
        defs = 0

    total_lines = len(content.split('\n'))
    comment_lines = len(re.findall(r'^\s*#.*[一-鿿]', content, re.MULTILINE))

    return {
        'file': filepath.name,
        'lang': lang,
        'total_lines': total_lines,
        'defs': defs,
        'cn_comment_lines': comment_lines,
        'expand_blocks': expand_in_code,
        'has_cn_docstring': bool(re.search(r'""".*[一-鿿]', content, re.DOTALL)),
        'needs_work': comment_lines < defs or expand_in_code < max(1, defs // 3),
    }


def main():
    parser = argparse.ArgumentParser(description='分析中文注释差距')
    parser.add_argument('--phase', type=str, default=None,
                        help='Phase 编号，如 "00" 或 "00,01,02"')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--needs-work', action='store_true', help='只显示需要处理的文件')
    args = parser.parse_args()

    phases = find_phases(args.phase)
    all_results = []
    summary = {}

    for phase_dir in phases:
        phase_name = phase_dir.name
        lessons = sorted(phase_dir.glob("*/docs/en.md"))
        phase_results = []

        for lesson_path in lessons:
            result = analyze_doc_file(lesson_path)
            phase_results.append(result)

        total = len(phase_results)
        needs_work = sum(1 for r in phase_results if r['needs_work'])
        avg_cn = sum(r['cn_blocks'] for r in phase_results) / total if total else 0
        avg_expand = sum(r['expand_blocks'] for r in phase_results) / total if total else 0
        total_cn_gap = sum(r['cn_gap'] for r in phase_results)
        total_expand_gap = sum(r['expand_gap'] for r in phase_results)

        summary[phase_name] = {
            'total': total,
            'needs_work': needs_work,
            'avg_cn': round(avg_cn, 1),
            'avg_expand': round(avg_expand, 1),
            'total_cn_gap': total_cn_gap,
            'total_expand_gap': total_expand_gap,
        }

        if not args.json:
            print(f"\n{'='*60}")
            print(f"Phase {phase_name} ({total} files, {needs_work} need work)")
            print(f"  平均 【中文解读】: {avg_cn:.1f}  |  平均 【拓展】: {avg_expand:.1f}")
            print(f"  总缺口 【中文解读】: {total_cn_gap}  |  总缺口 【拓展】: {total_expand_gap}")
            print(f"{'='*60}")

            for r in phase_results:
                if args.needs_work and not r['needs_work']:
                    continue
                status = "✅" if not r['needs_work'] else "⚠️"
                code_status = ""
                if r['code_files']:
                    code_needs = sum(1 for c in r['code_files'] if c['needs_work'])
                    code_status = f" | code: {code_needs}/{len(r['code_files'])} need work"
                print(f"  {status} {Path(r['file']).parent.parent.name}: "
                      f"cn={r['cn_blocks']}/{r['target_cn']} expand={r['expand_blocks']}/{r['target_expand']} "
                      f"headers_missing={r['headers_missing_cn']}{code_status}")

        all_results.extend(phase_results)

    if args.json:
        print(json.dumps({'summary': summary, 'files': all_results}, ensure_ascii=False, indent=2))

    # 总体汇总
    if not args.json:
        total_files = len(all_results)
        total_needs = sum(1 for r in all_results if r['needs_work'])
        print(f"\n{'='*60}")
        print(f"总计: {total_files} 文件, {total_needs} 需要处理")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
