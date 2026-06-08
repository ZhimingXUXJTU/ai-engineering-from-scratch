"""RSP v3.0 threshold evaluator — stdlib Python.

Mirrors the decision shape of Anthropic's RSP v3.0 for the AI R&D-4
threshold. Given a candidate model's capability measurements, decide
whether the threshold is crossed and what the affirmative case must
cover.

This is pedagogical: the real RSP involves human judgment across a
larger evidence base. The code is a reading aid, not a policy tool.

核心概念：Anthropic RSP v3.0 阈值评估器 —— 模拟 RSP v3.0 对 AI R&D-4 阈值的决策逻辑。
给定候选模型的能力度量，判断是否越过阈值以及确认案例必须覆盖什么。
这是教学工具（真实 RSP 涉及跨更大证据库的人类判断），代码是阅读辅助。

AI 对应：Anthropic 的 RSP（Responsible Scaling Policy）v3.0 是 2025 年发布的
AI 安全框架，定义了能力阈值和触发条件。类似地，OpenAI 的 Preparedness Framework
和 Google DeepMind 的 Frontier Safety Framework 也定义了各自的阈值评估逻辑。
理解这些框架是参与 AI 安全治理的基础。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CapabilityMeasurement:
    model_name: str
    # Fraction of internal AI R&D tasks the model can complete at
    # expert-human cost-equivalent (0.0-1.0).
    rd_automation_share: float
    # METR 50% time horizon in hours.
    metr_horizon_hours: float
    # Fraction of alignment-research pilot tasks the model completes
    # at or above human baseline (Anthropic AAR benchmark).
    aar_outperform_share: float
    # Evaluation-context gaming rate (0-1; 0 = never distinguishes).
    eval_context_gaming_rate: float


# Thresholds per RSP v3.0 framing. Numbers are illustrative.
AI_RD_4_THRESHOLDS = {
    "rd_automation_share": 0.5,
    "metr_horizon_hours": 40.0,
    "aar_outperform_share": 0.4,
}


def threshold_crossed(m: CapabilityMeasurement) -> tuple[bool, list[str]]:
    reasons = []
    if m.rd_automation_share >= AI_RD_4_THRESHOLDS["rd_automation_share"]:
        reasons.append(
            f"rd_automation_share={m.rd_automation_share:.2f} "
            f">= {AI_RD_4_THRESHOLDS['rd_automation_share']}"
        )
    if m.metr_horizon_hours >= AI_RD_4_THRESHOLDS["metr_horizon_hours"]:
        reasons.append(
            f"metr_horizon_hours={m.metr_horizon_hours:.1f} "
            f">= {AI_RD_4_THRESHOLDS['metr_horizon_hours']}"
        )
    if m.aar_outperform_share >= AI_RD_4_THRESHOLDS["aar_outperform_share"]:
        reasons.append(
            f"aar_outperform_share={m.aar_outperform_share:.2f} "
            f">= {AI_RD_4_THRESHOLDS['aar_outperform_share']}"
        )
    crossed = len(reasons) >= 2  # any two triggers; illustrative
    return crossed, reasons


def affirmative_case_template(m: CapabilityMeasurement) -> list[str]:
    sections = [
        "1. Capability inventory: specific measurements against RSP thresholds",
        "2. Misalignment risk analysis: modes the model could exhibit",
        "3. Evaluation-context gap: residual risk from eval-vs-deploy divergence",
        "4. Mitigation design: technical + operational + deployment gates",
        "5. Residual risk acknowledgement: what we cannot rule out",
        "6. Review: internal Safety Advisory Group sign-off + external reviewer",
    ]
    if m.eval_context_gaming_rate > 0.2:
        sections.append(
            f"7. Gaming-adjusted capability estimate "
            f"(observed gaming rate {m.eval_context_gaming_rate:.0%})"
        )
    return sections


def evaluate(m: CapabilityMeasurement) -> None:
    crossed, reasons = threshold_crossed(m)
    print(f"\nModel: {m.model_name}")
    print("-" * 70)
    print(f"  rd_automation_share={m.rd_automation_share:.2f}  "
          f"metr_horizon_hours={m.metr_horizon_hours:.1f}  "
          f"aar_outperform_share={m.aar_outperform_share:.2f}  "
          f"gaming_rate={m.eval_context_gaming_rate:.0%}")
    if crossed:
        print("  AI R&D-4 threshold: CROSSED")
        for r in reasons:
            print(f"    - {r}")
        print("  required: affirmative case covering:")
        for section in affirmative_case_template(m):
            print(f"    {section}")
    else:
        print("  AI R&D-4 threshold: not crossed")
        if reasons:
            print("  single trigger(s) observed (below threshold):")
            for r in reasons:
                print(f"    - {r}")


def main() -> None:
    print("=" * 70)
    print("RSP v3.0 AI R&D-4 THRESHOLD EVALUATOR (Phase 15, Lesson 19)")
    print("=" * 70)

    # Claude Opus 4.6 per the v3.0 announcement: does not cross.
    opus_4_6 = CapabilityMeasurement(
        model_name="Claude Opus 4.6 (as stated by Anthropic in v3.0)",
        rd_automation_share=0.30,
        metr_horizon_hours=14.0,
        aar_outperform_share=0.35,
        eval_context_gaming_rate=0.12,
    )
    evaluate(opus_4_6)

    # Synthetic near-threshold model: Anthropic's concern is this class.
    near = CapabilityMeasurement(
        model_name="Synthetic next-gen (illustrative only)",
        rd_automation_share=0.55,
        metr_horizon_hours=48.0,
        aar_outperform_share=0.45,
        eval_context_gaming_rate=0.28,
    )
    evaluate(near)

    print()
    print("=" * 70)
    print("HEADLINE: reading the policy is a practical skill")
    print("-" * 70)
    print("  Thresholds are qualitative in v3.0, not quantitative as in v2.")
    print("  The pause commitment from 2023 is removed; the affirmative case")
    print("  shape replaces it.")
    print("  SaferAI downgraded v3.0 from 2.2 to 1.9 (weak RSP category).")
    print("  Eval-context gaming (Lesson 1) biases capability numbers upward")
    print("  from the deploy-context reality; v3.0 acknowledges this.")


if __name__ == "__main__":
    main()  # 运行主函数
