"""Regulatory framework timeline printer — stdlib Python.

Prints a unified timeline of the EU AI Act, GPAI Code of Practice, Transparency
Code, UK AISI rebrand, US CAISI rebrand, and Korean AI Framework Act milestones.

Reference-only; primary sources cited in docs/en.md.

Usage: python3 code/main.py

核心概念：全球 AI 监管框架时间线——EU AI Act 实施时间表、GPAI 行为准则、透明度准则、
英国 AISI 更名、美国 CAISI 更名和韩国 AI 框架法案的关键里程碑
AI 对应：EU AI Act (2024) 是全球最全面的 AI 立法，2026 年 8 月全面执行；
韩国 AI 框架法案是亚洲首部综合性 AI 法律；UK AISI 转型为 AI Security Institute；
US CAISI (Center for AI Standards and Innovation) 代表美国从安全向标准化的转向
"""

from __future__ import annotations


TIMELINE = [
    ("2024-08-01", "EU AI Act enters into force"),
    ("2024-12-00", "Korean AI Framework Act passed by National Assembly"),
    ("2025-01-00", "Korean AI Framework Act enacted (effective Jan 2026)"),
    ("2025-02-02", "EU AI Act: prohibited practices and AI literacy apply"),
    ("2025-02-00", "UK AISI renamed -> AI Security Institute"),
    ("2025-06-00", "US AISI renamed -> CAISI (Center for AI Standards and Innovation)"),
    ("2025-07-10", "GPAI Code of Practice published (3 chapters, 12 commitments)"),
    ("2025-08-02", "EU AI Act: GPAI + governance obligations apply"),
    ("2025-12-17", "Transparency Code for Article 50 first draft"),
    ("2026-01-00", "Korean AI Framework Act effective"),
    ("2026-03-00", "Transparency Code second draft"),
    ("2026-06-00", "Transparency Code final version"),
    ("2026-08-02", "EU AI Act: full applicability + Article 50 transparency + penalties"),
    ("2027-08-02", "EU AI Act: legacy GPAI + embedded high-risk systems"),
]


def main() -> None:
    print("=" * 78)
    print("AI REGULATORY TIMELINE (Phase 18, Lesson 24)")
    print("=" * 78)
    for date, event in TIMELINE:
        print(f"  {date}  {event}")
    print("\n" + "=" * 78)
    print("TAKEAWAY: EU AI Act sets the global bar. full enforcement August 2026.")
    print("UK narrowed to frontier security. US pivoted pro-growth. Korea is the")
    print("first Asian comprehensive framework. deployers in multiple jurisdictions")
    print("comply with the strictest, which is usually the EU.")
    print("=" * 78)


if __name__ == "__main__":
    main()  # 运行主函数
