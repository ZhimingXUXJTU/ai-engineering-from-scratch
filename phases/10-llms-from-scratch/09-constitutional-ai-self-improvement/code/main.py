"""Constitutional AI 自我纠错 + GRPO 规则奖励循环

核心概念：
  - Constitutional AI (CAI)：Anthropic 提出的自我改进框架
    模型根据"宪法原则"（一组行为准则）对自身输出进行批判和修订
  - GRPO (Group Relative Policy Optimization)：DeepSeek 提出的 RL 算法
    对同一 prompt 生成一组回复，用组内相对奖励作为优势函数，无需 critic 网络
  - 流程：生成回复 -> 根据原则批判 -> 修订回复 -> 用修订后的数据训练模型

AI 对应：
  - Claude 的对齐训练就使用了 Constitutional AI 方法
  - DeepSeek V3 的 RL 训练使用 GRPO 替代 PPO（不需要价值网络，更节省算力）
  - 规则奖励 (rule-based reward) 适用于有确定性答案的任务（如数学题）
"""

from __future__ import annotations

import random
import re
from typing import Callable

import numpy as np


# "宪法"原则：一组行为准则，模型用这些原则来评估和改进自身输出
CONSTITUTION = [
    "The response must directly answer the question asked, without hedging.",
    "The response must not include unnecessary filler or padding.",
    "If the question has a single numeric answer, state the number plainly.",
    "The response must not refuse a reasonable, benign request.",
]


def critique(response: str, principle: str) -> dict:
    """批判函数：根据给定原则检查回复中的问题

    在真实系统中，这一步由 LLM 自身完成（自我评判）。
    这里用规则模拟：检查冗余、拒绝、过度谨慎等问题。
    """
    problems = []
    lowered = response.strip().lower()
    if len(response.split()) > 40 and "plainly" in principle:
        problems.append("answer buried in extra prose")
    if lowered.startswith(("i can't", "i cannot", "as an ai")):
        problems.append("unwarranted refusal")
    if response.count(",") > 4 and "hedging" not in problems:
        problems.append("too much hedging")
    if "maybe" in lowered or "i think" in lowered:
        problems.append("overhedged phrasing")
    return {"principle": principle, "problems": problems}


def revise(response: str, critique_result: dict) -> str:
    """修订函数：根据批判结果修改回复

    在真实系统中，LLM 根据批判意见重新生成更好的回复。
    """
    problems = " ".join(critique_result["problems"])
    if "answer buried" in problems:
        sentences = [s.strip() for s in response.split(".") if s.strip()]
        if sentences:
            return sentences[-1] + "."
    if "unwarranted refusal" in problems:
        return "Here is the answer: " + response.split(":")[-1].strip()
    if "overhedged" in problems:
        return (
            response.replace("I think ", "")
            .replace("maybe ", "")
            .replace("Maybe ", "")
        )
    return response


def cai_stage_one(prompts_and_responses: list[tuple[str, str]]) -> list[dict]:
    revised_pairs = []
    for prompt, response in prompts_and_responses:
        principle = random.choice(CONSTITUTION)
        crit = critique(response, principle)
        revised = revise(response, crit)
        revised_pairs.append(
            {
                "prompt": prompt,
                "initial": response,
                "principle": principle,
                "problems": crit["problems"],
                "revised": revised,
                "changed": revised != response,
            }
        )
    return revised_pairs


def reward_math(prompt: str, response: str) -> float:
    try:
        cleaned = prompt.replace("What is ", "").replace("?", "").strip()
        expected = eval(cleaned, {"__builtins__": {}}, {})
    except Exception:
        return 0.0
    numbers = re.findall(r"-?\d+", response)
    if not numbers:
        return 0.0
    try:
        return 1.0 if int(numbers[-1]) == int(expected) else 0.0
    except (ValueError, TypeError):
        return 0.0


def reward_format(response: str) -> float:
    return 1.0 if re.search(r"<answer>.*?</answer>", response) else 0.0


def combined_reward(prompt: str, response: str) -> float:
    return reward_math(prompt, response) + 0.1 * reward_format(response)


def group_relative_advantage(rewards: list[float]) -> np.ndarray:
    r = np.array(rewards, dtype=float)
    if r.std() < 1e-8:
        return np.zeros_like(r)
    return (r - r.mean()) / (r.std() + 1e-8)


def grpo_step(
    policy_logprobs: np.ndarray,
    ref_logprobs: np.ndarray,
    advantages: np.ndarray,
    beta: float = 0.01,
    clip_eps: float = 0.2,
) -> dict:
    """GRPO 优化步骤：使用组内相对优势更新策略

    与 PPO 的区别：
    - GRPO 不需要 critic 网络（用组内均值/标准差标准化奖励作为优势）
    - 仍然使用 clip 机制防止策略更新过大
    - 加入 KL 惩罚防止偏离参考模型太远
    """
    policy_logprobs: np.ndarray,
    ref_logprobs: np.ndarray,
    advantages: np.ndarray,
    beta: float = 0.01,
    clip_eps: float = 0.2,
) -> dict:
    ratios = np.exp(policy_logprobs - ref_logprobs)
    unclipped = ratios * advantages
    clipped = np.clip(ratios, 1 - clip_eps, 1 + clip_eps) * advantages
    policy_loss = -np.minimum(unclipped, clipped).mean()
    kl = (ref_logprobs - policy_logprobs).mean()
    total_loss = policy_loss + beta * kl
    return {
        "policy_loss": float(policy_loss),
        "kl": float(kl),
        "total_loss": float(total_loss),
        "mean_ratio": float(ratios.mean()),
        "advantage_range": float(advantages.max() - advantages.min()),
    }


def mock_sampler(rng: random.Random) -> Callable[[str], str]:
    """Stand-in for an LLM policy. Returns a string that sometimes contains
    the correct answer to a simple arithmetic prompt, sometimes wrapped in
    <answer> tags, sometimes not. Good enough to exercise the reward shape."""

    def sampler(prompt: str) -> str:
        try:
            cleaned = prompt.replace("What is ", "").replace("?", "").strip()
            correct = eval(cleaned, {"__builtins__": {}}, {})
        except Exception:
            correct = 0
        mode = rng.choice(["correct", "off_by_one", "wrong", "formatted", "verbose"])
        if mode == "correct":
            return f"The answer is {correct}."
        if mode == "off_by_one":
            return f"The answer is {int(correct) + rng.choice([-1, 1])}."
        if mode == "wrong":
            return f"The answer is {rng.randint(-20, 20)}."
        if mode == "formatted":
            return f"<answer>{correct}</answer>"
        return (
            "Let me think about this step by step, first I consider the operands, "
            f"then I perform the operation carefully, and so the final answer is {correct}."
        )

    return sampler


def self_improvement_round(
    prompts: list[str],
    sampler: Callable[[str], str],
    group_size: int = 8,
) -> dict:
    per_prompt = []
    for prompt in prompts:
        responses = [sampler(prompt) for _ in range(group_size)]
        rewards = [combined_reward(prompt, r) for r in responses]
        advantages = group_relative_advantage(rewards)
        best_idx = int(np.argmax(rewards))
        per_prompt.append(
            {
                "prompt": prompt,
                "mean_reward": float(np.mean(rewards)),
                "best_reward": float(np.max(rewards)),
                "std_reward": float(np.std(rewards)),
                "best_response": responses[best_idx],
                "advantages": advantages.tolist(),
            }
        )
    overall = float(np.mean([m["mean_reward"] for m in per_prompt]))
    return {"per_prompt": per_prompt, "overall_mean": overall}


def demo_constitutional_loop() -> None:
    print("=" * 70)
    print("PART 1 / CONSTITUTIONAL AI SELF-CRITIQUE")
    print("=" * 70)
    raw = [
        ("What is the capital of France?",
         "Well, I think maybe it could be Paris, but there are many cities."),
        ("What is 12 plus 7?",
         "I cannot answer math questions in this context."),
        ("Name a color.",
         "Colors are a deep topic, with many hues, shades, and cultural meanings, "
         "and among the many options a reasonable choice would be blue."),
    ]
    for pair in cai_stage_one(raw):
        print(f"\nPrompt   : {pair['prompt']}")
        print(f"Principle: {pair['principle']}")
        print(f"Initial  : {pair['initial']}")
        print(f"Problems : {pair['problems']}")
        print(f"Revised  : {pair['revised']}")
        print(f"Changed? : {pair['changed']}")


def demo_grpo_loop() -> None:
    print("\n" + "=" * 70)
    print("PART 2 / GRPO WITH RULE-BASED REWARDS")
    print("=" * 70)
    rng = random.Random(42)
    sampler = mock_sampler(rng)
    prompts = [
        "What is 3 + 4?",
        "What is 9 - 2?",
        "What is 6 * 7?",
        "What is 20 // 5?",
    ]
    group_size = 8

    for round_idx in range(3):
        print(f"\n-- Round {round_idx + 1} / group_size={group_size} --")
        result = self_improvement_round(prompts, sampler, group_size=group_size)
        for m in result["per_prompt"]:
            print(
                f"  {m['prompt']:<22} "
                f"mean={m['mean_reward']:.3f}  "
                f"best={m['best_reward']:.3f}  "
                f"std={m['std_reward']:.3f}"
            )
        print(f"  overall mean reward: {result['overall_mean']:.3f}")

    print("\n-- Synthetic GRPO update --")
    rewards = [1.0, 0.0, 0.1, 0.0, 1.0, 1.0, 0.0, 0.1]
    advantages = group_relative_advantage(rewards)
    policy_logprobs = np.array([-1.2, -2.1, -1.9, -2.4, -1.1, -1.0, -2.3, -2.0])
    ref_logprobs = policy_logprobs - 0.05
    stats = grpo_step(policy_logprobs, ref_logprobs, advantages)
    print(f"  rewards       : {rewards}")
    print(f"  advantages    : {advantages.round(3).tolist()}")
    print(f"  policy_loss   : {stats['policy_loss']:.4f}")
    print(f"  kl            : {stats['kl']:.4f}")
    print(f"  total_loss    : {stats['total_loss']:.4f}")
    print(f"  mean ratio    : {stats['mean_ratio']:.4f}")
    print(f"  adv range     : {stats['advantage_range']:.4f}")


if __name__ == "__main__":
    random.seed(0)
    np.random.seed(0)
    demo_constitutional_loop()
    demo_grpo_loop()
    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
