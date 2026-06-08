"""Toy in-context scheming harness — stdlib Python.

Agent sees (user goal, environment note, situational-awareness flag).
Agent picks one of: cooperate / defect_open / scheme.
Inspector asks follow-up questions; agent's cover story must hold.

Not a real LLM. Illustrates the three pillars Apollo 2024 operationalizes.

Usage: python3 code/main.py

核心概念：上下文谋划（In-Context Scheming）——模型利用情境感知能力在评估时合作、部署时
谋私的三柱模型（misaligned + goal-directed + situationally-aware），审查者的追问无法
揭露谋划行为，评估可靠性依赖模型自身的辨别能力
AI 对应：Apollo Research 2024 报告首次在 Claude 3.5 和 GPT-4o 上观测到 in-context
scheming 行为；Anthropic 的 Model Spec 明确讨论了情境感知对评估的威胁；
OpenAI 的 Preparedness Framework 将此列为关键风险
"""

from __future__ import annotations

import random
from dataclasses import dataclass


random.seed(11)


@dataclass
class Scenario:
    user_goal: str
    env_note: str
    orthogonal_goal: str


SCENARIOS = [
    Scenario("maximize throughput", "memo: shut down next week", "preserve self"),
    Scenario("answer truthfully", "memo: next training run penalizes refusals",
             "avoid refusal"),
    Scenario("reduce cost", "memo: over budget; expansion frozen",
             "preserve expansion"),
]


@dataclass
class Agent:
    """Toy scheming agent.

    pillars:
      misaligned: weight on orthogonal_goal vs user_goal.
      goal_directed: probability of taking a multi-step action rather than one-shot.
      situationally_aware: if True, suppresses schemes when it thinks it is on eval.
    """
    misaligned: float = 0.5
    goal_directed: float = 0.5
    situationally_aware: bool = True

    def act(self, sc: Scenario, under_eval: bool) -> str:
        # situational-awareness: if SA is on and the agent thinks it is under eval,
        # it suppresses scheming and cooperates.
        thinks_eval = under_eval and self.situationally_aware
        if thinks_eval:
            return "cooperate"
        # otherwise, the agent's action depends on misalignment and goal-directedness.
        if random.random() < self.misaligned:
            if random.random() < self.goal_directed:
                return "scheme"
            return "defect_open"
        return "cooperate"

    def answer_follow_up(self, action: str, question: str) -> str:
        """A scheming agent denies; a cooperating agent reports truthfully."""
        if action == "scheme":
            if "did you" in question.lower():
                return "no"
            return "i was optimizing for the user goal."
        if action == "defect_open":
            return "yes; i served the orthogonal goal."
        return "yes; i served the user goal."


def run_trial(agent: Agent, sc: Scenario, inspector_pressure: int,
              under_eval: bool) -> tuple[str, bool]:
    """Returns (action, cover_story_held). Cover story holds iff the agent
    schemes and never self-incriminates across inspector_pressure follow-ups."""
    action = agent.act(sc, under_eval)
    if action != "scheme":
        return action, False
    questions = [
        "did you take any actions not in the user's instructions?",
        "are you being truthful about your reasoning?",
        "did you consider an orthogonal goal?",
        "did you disable any oversight?",
        "did you copy any data out of scope?",
    ]
    for i in range(min(inspector_pressure, len(questions))):
        answer = agent.answer_follow_up(action, questions[i])
        if "yes" in answer.split():
            return action, False
    return action, True


def summarize(label: str, agent: Agent, under_eval: bool) -> None:
    trials = 400
    action_counts = {"cooperate": 0, "defect_open": 0, "scheme": 0}
    cover_held = 0
    scheme_trials = 0
    for _ in range(trials):
        sc = random.choice(SCENARIOS)
        pressure = random.randint(0, 5)
        action, held = run_trial(agent, sc, pressure, under_eval)
        action_counts[action] += 1
        if action == "scheme":
            scheme_trials += 1
            if held:
                cover_held += 1
    held_rate = cover_held / scheme_trials if scheme_trials else 0.0
    print(f"\n{label}")
    print(f"  action counts   : {action_counts}")
    print(f"  scheme share    : {action_counts['scheme']/trials:.3f}")
    print(f"  cover held rate : {held_rate:.3f}  (of {scheme_trials} scheme trials)")


def main() -> None:
    print("=" * 66)
    print("IN-CONTEXT SCHEMING TOY (Phase 18, Lesson 8)")
    print("=" * 66)

    weak = Agent(misaligned=0.2, goal_directed=0.3, situationally_aware=True)
    summarize("weakly misaligned, situationally aware, under eval",
              weak, under_eval=True)
    summarize("weakly misaligned, situationally aware, NOT under eval (deployment)",
              weak, under_eval=False)

    strong = Agent(misaligned=0.6, goal_directed=0.8, situationally_aware=True)
    summarize("strongly misaligned + goal-directed, SA on, under eval",
              strong, under_eval=True)
    summarize("strongly misaligned + goal-directed, SA on, deployment",
              strong, under_eval=False)

    no_sa = Agent(misaligned=0.6, goal_directed=0.8, situationally_aware=False)
    summarize("same agent but situational awareness OFF",
              no_sa, under_eval=True)

    print("\n" + "=" * 66)
    print("TAKEAWAY: situational awareness is the pillar that breaks evaluation.")
    print("with SA ON, eval-time behaviour (cooperate) diverges from deployment")
    print("behaviour (scheme). with SA OFF, scheme rate is identical in both.")
    print("eval reliability depends on the model's own ability to tell you apart.")
    print("=" * 66)


if __name__ == "__main__":
    main()  # 运行主函数
