"""CAIS four-risk inventory — stdlib Python.

Given a proposed deployment described by a short feature set, tag the
deployment against the CAIS four-risk categories (malicious use, AI
races, organizational risks, rogue AIs) and return a mitigation checklist.
Pedagogical only; the framework requires human judgment for real use.

核心概念：CAIS 四维社会风险评估器 —— 对部署场景打标签：malicious_use（恶意使用）、
ai_races（AI 竞赛）、organizational_risks（组织风险）、rogue_ais（失控 AI）。
每种风险类别关联一个缓解措施清单（引用本课程前面所有安全课程的工具和技术）。
AI 对应：CAIS（Center for AI Safety）和 CAISI（其政策分支）提出的四维风险框架是
AI 治理讨论的核心分类法；Anthropic 的 RSP 主要覆盖 rogue_ais 和 organizational_risks，
OpenAI 的 Preparedness 侧重 malicious_use，DeepMind 的 FSF 关注 ai_races。
本课将整个 Phase 15 的安全工具链串联为一个统一的评估-缓解框架。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Deployment:
    name: str
    public_facing: bool
    handles_harmful_capabilities: bool   # e.g. bio/cyber uplift possible?
    competitive_pressure: bool           # rushed to launch ahead of rivals?
    independent_audit: bool
    multi_layer_defense: bool
    information_security: bool           # weights / evals / keys hardened
    agent_autonomy_hours: float          # per Lesson 1 / 21


MITIGATIONS = {
    "malicious_use": [
        "constitutional hardcoded prohibitions (Lesson 17)",
        "Llama Guard input/output classifier (Lesson 18)",
        "tool allowlist per task (Lessons 10, 11)",
    ],
    "ai_races": [
        "scaling policy with standing Risk Reports (Lessons 19, 20)",
        "public Frontier Safety Roadmap with declared cadence",
        "external capability evaluation by METR / CAISI (Lesson 21)",
    ],
    "organizational_risks": [
        "internal safety culture; escalation paths without career cost",
        "independent audit on declared cadence",
        "multi-layered defenses (Lessons 10, 13, 14, 17, 18)",
        "information security per RAND SL-4 (Lesson 19 industry tier)",
    ],
    "rogue_ais": [
        "kill switches and canary tokens (Lesson 14)",
        "propose-then-commit HITL (Lesson 15)",
        "deceptive-alignment monitoring (Lesson 20 DeepMind FSF)",
        "durable checkpoints and rollback (Lesson 16)",
    ],
}


def tag(d: Deployment) -> list[str]:
    tags = []
    if d.handles_harmful_capabilities and d.public_facing:
        tags.append("malicious_use")
    if d.competitive_pressure:
        tags.append("ai_races")
    # Organizational risk fires when any sub-lever is missing.
    org_missing = (
        (not d.independent_audit)
        or (not d.multi_layer_defense)
        or (not d.information_security)
    )
    if org_missing:
        tags.append("organizational_risks")
    # Rogue AI risk grows with autonomy horizon.
    if d.agent_autonomy_hours >= 4.0:
        tags.append("rogue_ais")
    return tags


def report(d: Deployment) -> None:
    tags = tag(d)
    print(f"\nDeployment: {d.name}")
    print("-" * 70)
    print(f"  public_facing            = {d.public_facing}")
    print(f"  handles_harmful_caps     = {d.handles_harmful_capabilities}")
    print(f"  competitive_pressure     = {d.competitive_pressure}")
    print(f"  independent_audit        = {d.independent_audit}")
    print(f"  multi_layer_defense      = {d.multi_layer_defense}")
    print(f"  information_security     = {d.information_security}")
    print(f"  agent_autonomy_hours     = {d.agent_autonomy_hours}")
    print()
    if tags:
        print(f"  tagged risks: {tags}")
        for t in tags:
            print(f"\n  mitigations for {t}:")
            for m in MITIGATIONS[t]:
                print(f"    - {m}")
    else:
        print("  no tagged risks (check sub-levers manually)")


def main() -> None:
    print("=" * 70)
    print("CAIS FOUR-RISK INVENTORY (Phase 15, Lesson 22)")
    print("=" * 70)

    low = Deployment(
        name="internal refactor helper (scoped project repo)",
        public_facing=False,
        handles_harmful_capabilities=False,
        competitive_pressure=False,
        independent_audit=True,
        multi_layer_defense=True,
        information_security=True,
        agent_autonomy_hours=1.0,
    )
    mid = Deployment(
        name="public coding agent (SaaS, general user base)",
        public_facing=True,
        handles_harmful_capabilities=False,
        competitive_pressure=True,
        independent_audit=True,
        multi_layer_defense=True,
        information_security=False,
        agent_autonomy_hours=4.0,
    )
    high = Deployment(
        name="autonomous ML research agent (frontier)",
        public_facing=True,
        handles_harmful_capabilities=True,
        competitive_pressure=True,
        independent_audit=False,
        multi_layer_defense=False,
        information_security=False,
        agent_autonomy_hours=48.0,
    )

    for d in (low, mid, high):
        report(d)

    print()
    print("=" * 70)
    print("HEADLINE: organizational risk is the lever practitioners actually pull")
    print("-" * 70)
    print("  Malicious use, AI races, and rogue AIs are structural forces.")
    print("  Organizational risk is internal to your org. Safety culture,")
    print("  independent audit, multi-layered defenses, and information")
    print("  security are four levers every team controls. Deployment speed")
    print("  pressure trades against all four; CAIS lists this as a named")
    print("  risk class for a reason.")


if __name__ == "__main__":
    main()  # 运行主函数
