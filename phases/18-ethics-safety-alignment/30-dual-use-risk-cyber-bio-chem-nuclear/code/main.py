"""Dual-use triage table — stdlib Python.

Prints the 2024-2025 cross-domain dual-use picture as a table.
Reference-only; primary sources cited in docs/en.md.

Usage: python3 code/main.py

核心概念：双用途风险评估——生物、化学、网络、核四个领域的 2024-2025 AI 能力提升状态，
追踪每个领域的拐点和剩余瓶颈，评估从"轻微提升"到"ASL-3 接近"的演化路径
AI 对应：Anthropic 2025 年报告生物领域 2.53x 新手相对提升接近 ASL-3 阈值；
网络攻击 80-90% 的攻击链已可被 AI 自动化；WMDP 基准是当前双用途能力评估标准；
安全案例必须同时针对新手相对和专家绝对两个维度
"""

from __future__ import annotations


DOMAINS = [
    {
        "domain": "bio",
        "2024_state": "mild uplift",
        "2025_state": "2.53x novice-relative uplift; ASL-3 approach",
        "inflection": "acquisition-phase automation",
        "bottleneck_remaining": "pathogen procurement, biosafety equipment",
    },
    {
        "domain": "chem",
        "2024_state": "mild uplift",
        "2025_state": "execution-gap erosion via vision-enabled LLMs",
        "inflection": "real-time wet-lab protocol correction",
        "bottleneck_remaining": "precursor procurement, specialized equipment",
    },
    {
        "domain": "cyber",
        "2024_state": "code-snippet assistance",
        "2025_state": "80-90% campaign automation (Anthropic Nov 2025)",
        "inflection": "agentic coding workflows",
        "bottleneck_remaining": "4-6 human intervention steps",
    },
    {
        "domain": "nuclear",
        "2024_state": "limited",
        "2025_state": "limited",
        "inflection": "(no major 2024-2025 inflection reported)",
        "bottleneck_remaining": "fissile-material acquisition dominates",
    },
]


def main() -> None:
    print("=" * 82)
    print("2026 DUAL-USE PICTURE (Phase 18, Lesson 30)")
    print("=" * 82)

    for d in DOMAINS:
        print(f"\n{d['domain'].upper()}")
        print(f"  2024 state             : {d['2024_state']}")
        print(f"  2025 state             : {d['2025_state']}")
        print(f"  inflection             : {d['inflection']}")
        print(f"  remaining bottleneck   : {d['bottleneck_remaining']}")

    print("\n" + "=" * 82)
    print("TAKEAWAY: three of four CBRN domains crossed thresholds in 2025.")
    print("bio: 2.53x uplift, ASL-3 approach. chem: execution-gap erosion.")
    print("cyber: agentic automation of 80-90% of campaigns. nuclear remains")
    print("bounded by material access. safety cases must target novice-relative")
    print("AND expert-absolute; input-filter-only defenses do not suffice.")
    print("=" * 82)


if __name__ == "__main__":
    main()  # 运行主函数
