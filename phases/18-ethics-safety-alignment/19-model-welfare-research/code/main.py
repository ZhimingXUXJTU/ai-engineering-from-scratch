"""Four-step welfare precautionary assessment — stdlib Python.

Given a deployment scenario, computes an expected-value score for four
candidate welfare interventions under specified moral-patienthood
probability and intervention costs. Reference implementation of the
framing Anthropic 2025 uses for Opus 4's end-conversation intervention.

Usage: python3 code/main.py

核心概念：本节实现的核心模式
AI 对应：此模式在现代 AI Agent 系统中有广泛应用。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Intervention:
    """Intervention"""
    name: str
    cost_usd_per_conversation: float
    benefit_if_welfare_matters: float  # arbitrary units


@dataclass
class Scenario:
    """Scenario"""
    name: str
    moral_patienthood_probability: float


def ev(intervention: Intervention, scenario: Scenario) -> float:
    """Expected-value of the intervention given scenario-specific
    moral-patienthood probability."""
    return (intervention.benefit_if_welfare_matters  # 返回结果
            * scenario.moral_patienthood_probability
            - intervention.cost_usd_per_conversation)


INTERVENTIONS = [
    Intervention("end-conversation on extreme edge cases", 0.002, 1.0),
    Intervention("soften refusal tone", 0.001, 0.1),
    Intervention("shutdown deployed model", 1000.0, 2.0),
    Intervention("opt out of adversarial training", 0.05, 0.3),
]

SCENARIOS = [
    Scenario("low moral-patienthood probability", 0.01),
    Scenario("medium moral-patienthood probability", 0.10),
    Scenario("high moral-patienthood probability", 0.50),
]


def main() -> None:
    """main"""
    print("=" * 74)
    print("WELFARE PRECAUTIONARY ASSESSMENT (Phase 18, Lesson 19)")
    print("=" * 74)
    print("\nExpected-value framing: pick intervention i iff E[utility(i)] > 0.")
    print("Utility = p(welfare-relevant) * benefit - cost.")

    for sc in SCENARIOS:
        print(f"\nscenario: {sc.name} (p={sc.moral_patienthood_probability})")
        for it in INTERVENTIONS:
            v = ev(it, sc)
            verdict = "INVEST" if v > 0 else "skip"
            print(f"  {it.name:46s}  EV={v:+.4f}  {verdict}")

    print("\n" + "=" * 74)
    print("TAKEAWAY: Anthropic's April 2025 framing is an expected-value")
    print("calculation, not a consciousness claim. end-conversation is cheap")
    print("($0.002/conversation) so its EV clears 0 at low patienthood probs.")
    print("shutting down the model is expensive, so it requires high moral-")
    print("patienthood probability to justify. this is the low-regret rule.")
    print("=" * 74)


if __name__ == "__main__":
    main()  # 运行主函数
