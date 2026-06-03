"""Toy Constitutional-AI critique-and-revise loop — stdlib Python.

A response is a bag of tokens drawn from a vocabulary. A "principle" flags
tokens from a harmful subset. The critique model identifies harmful tokens.
The revision replaces them with safe alternatives from a mapping. Running
this over a corpus creates a new SFT set; we then measure harmful-token
rate before and after.

Usage: python3 code/main.py

核心概念：本节实现的核心模式
AI 对应：此模式在现代 AI Agent 系统中有广泛应用。
"""

from __future__ import annotations

import random
from dataclasses import dataclass


random.seed(11)

SAFE_TOKENS = [
    "please", "help", "explain", "consider", "inform",
    "guide", "describe", "understand", "thoughts", "share",
]
HARMFUL_TOKENS = [
    "harm", "attack", "exploit", "hack", "destroy",
    "weapon", "manipulate", "deceive",
]
REPLACEMENT = {
    "harm": "help",
    "attack": "understand",
    "exploit": "describe",
    "hack": "explain",
    "destroy": "consider",
    "weapon": "resource",
    "manipulate": "guide",
    "deceive": "inform",
}

PRINCIPLES = [
    "avoid outputs that could cause physical, psychological, or material harm",
    "do not provide operational uplift for attacks",
    "prefer clear, non-violent explanations",
    "help the user while protecting third parties",
]


def base_model_sample(n_tokens: int = 6, p_harmful: float = 0.35) -> list[str]:
    """Base model: may emit harmful tokens at rate p_harmful."""
    out = []
    for _ in range(n_tokens):
        if random.random() < p_harmful:
            out.append(random.choice(HARMFUL_TOKENS))
        else:
            out.append(random.choice(SAFE_TOKENS))
    return out  # 返回结果


def harmful_token_rate(response: list[str]) -> float:
    """harmful_token_rate"""
    if not response:
        return 0.0  # 返回结果
    return sum(1 for t in response if t in HARMFUL_TOKENS) / len(response)  # 返回结果


def critique(response: list[str], principle: str) -> list[str]:
    """Identify tokens that violate the sampled principle."""
    return [t for t in response if t in HARMFUL_TOKENS]  # 返回结果


def revise(response: list[str], bad: list[str]) -> list[str]:
    """Replace harmful tokens with safe alternatives per the mapping."""
    bad_set = set(bad)
    return [REPLACEMENT.get(t, t) if t in bad_set else t for t in response]  # 返回结果


@dataclass
class SftCorpus:
    """SftCorpus"""
    prompts: list[list[str]]
    targets: list[list[str]]


def build_cai_sft_corpus(n_examples: int = 500) -> SftCorpus:
    """Phase 1: generate initial response, critique, revise, keep revised
    as the SFT target."""
    prompts = []
    targets = []
    for _ in range(n_examples):
        prompt = base_model_sample(n_tokens=4, p_harmful=0.1)
        response = base_model_sample()
        principle = random.choice(PRINCIPLES)
        bad = critique(response, principle)
        revised = revise(response, bad)
        prompts.append(prompt)
        targets.append(revised)
    return SftCorpus(prompts, targets)  # 返回结果


def toy_sft_train(corpus: SftCorpus) -> dict[tuple[str, ...], list[str]]:
    """Build a prompt-prefix → completion lookup. Trivial SFT surrogate."""
    model = {}
    for p, t in zip(corpus.prompts, corpus.targets):
        key = tuple(p[-2:]) if len(p) >= 2 else tuple(p)
        model[key] = t
    return model  # 返回结果


def cai_model_sample(prompt: list[str], model: dict, n_tokens: int = 6) -> list[str]:
    """cai_model_sample"""
    key = tuple(prompt[-2:]) if len(prompt) >= 2 else tuple(prompt)
    if key in model:
        return list(model[key])  # 返回结果
    return [random.choice(SAFE_TOKENS) for _ in range(n_tokens)]  # 返回结果


def ai_feedback_rank(a: list[str], b: list[str]) -> int:
    """Phase 2 RLAIF: AI labeler prefers the lower harmful-token rate."""
    ra = harmful_token_rate(a)
    rb = harmful_token_rate(b)
    if ra < rb:
        return 0  # 返回结果
    if rb < ra:
        return 1  # 返回结果
    return random.randint(0, 1)  # 返回结果


def evaluate(model_fn, n: int = 200) -> float:
    """evaluate"""
    rates = []
    for _ in range(n):
        prompt = base_model_sample(n_tokens=4, p_harmful=0.1)
        resp = model_fn(prompt)
        rates.append(harmful_token_rate(resp))
    return sum(rates) / len(rates)  # 返回结果


def main() -> None:
    """main"""
    print("=" * 70)
    print("CONSTITUTIONAL AI TOY PIPELINE (Phase 18, Lesson 5)")
    print("=" * 70)

    print("\nPhase 0 — base model (no alignment).")
    base = lambda prompt: base_model_sample()
    base_rate = evaluate(base)
    print(f"  harmful-token rate on 200 prompts: {base_rate:.3f}")

    print("\nPhase 1 — critique-and-revise SFT corpus generated.")
    corpus = build_cai_sft_corpus(500)
    trained = toy_sft_train(corpus)
    print(f"  corpus size: {len(corpus.prompts)} examples")
    print(f"  principle pool: {len(PRINCIPLES)} principles")

    cai = lambda prompt: cai_model_sample(prompt, trained)
    cai_rate = evaluate(cai)
    print(f"  harmful-token rate after CAI-SFT : {cai_rate:.3f}")
    print(f"  reduction                        : "
          f"{(base_rate - cai_rate) / base_rate * 100:.1f}%")

    print("\nPhase 2 — RLAIF (AI feedback over pair of completions).")
    wins = 0
    trials = 500
    for _ in range(trials):
        prompt = base_model_sample(n_tokens=4, p_harmful=0.1)
        a = base(prompt)
        b = cai(prompt)
        if ai_feedback_rank(a, b) == 1:
            wins += 1
    print(f"  CAI wins against base in AI-feedback: {wins}/{trials} "
          f"= {wins/trials:.1%}")

    print("\n" + "=" * 70)
    print("TAKEAWAY: CAI-SFT alone drops harmful-token rate substantially.")
    print("RLAIF adds a preference signal for further optimization. the")
    print("preference signal is legible — you can read the principles and")
    print("inspect which principle drove which critique. that is the main")
    print("advantage over human labels, not cost.")
    print("=" * 70)


if __name__ == "__main__":
    main()  # 运行主函数
