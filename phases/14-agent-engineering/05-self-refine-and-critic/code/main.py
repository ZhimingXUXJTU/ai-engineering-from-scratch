"""Toy Self-Refine and CRITIC loop. | 玩具自我精炼与 CRITIC 循环

Task: produce a 3-bullet summary under 60 chars per bullet that does not contain
known factual errors. Self-Refine uses LLM-style self-critique; CRITIC routes
verification through an external fact list.
任务：生成每条不超过 60 字符的 3 条摘要，不包含已知事实错误。
Self-Refine 使用 LLM 式自我批评；CRITIC 通过外部事实列表验证。

核心概念：生成→验证→精炼的迭代循环。CRITIC 用外部工具替代自我批评。
AI 对应：Claude Code 的测试验证代码、Anthropic 的评估器-优化器工作流。
"""

from __future__ import annotations

from dataclasses import dataclass, field


KNOWN_WRONG_FACTS = [                   # 已知错误事实——CRITIC 用作外部验证参考
    "paris is the capital of germany",
    "mt everest is in europe",
    "the sun orbits the earth",
]


@dataclass
class Attempt:
    """一次迭代尝试——记录输出、批评和验证结果"""
    iteration: int         # 迭代编号
    output: str            # 生成的输出
    critique: str          # 批评文本
    verified: bool         # 是否通过验证


def generate(topic: str, history: list[Attempt]) -> str:
    """生成器——根据历史尝试生成新的输出（脚本化，真实场景替换为 LLM）"""
    if not history:
        return (
            "- Paris is the capital of Germany\n"
            "- Mt Everest is in Europe\n"
            "- Water boils at 100C"
        )
    last = history[-1]
    if "germany" in last.critique.lower():
        return (
            "- Paris is the capital of France\n"
            "- Mt Everest is in Europe\n"
            "- Water boils at 100C"
        )
    if "everest" in last.critique.lower():
        return (
            "- Paris is the capital of France\n"
            "- Mt Everest is in Asia\n"
            "- Water boils at 100C at sea level"
        )
    return history[-1].output


def feedback_self(output: str) -> tuple[str, bool]:
    """自我批评——LLM 自行评估输出质量（Self-Refine 模式）"""
    if "Germany" in output and "Paris" in output:
        return "first bullet reads wrong, double-check capital", False
    if "Europe" in output and "Everest" in output:
        return "second bullet's continent looks off to me", False
    return "no issues", True


def verify_external(output: str) -> tuple[str, bool]:
    """外部验证器——CRITIC 模式，通过外部事实库验证（比自我批评更可靠）"""
    text = output.lower()
    for fact in KNOWN_WRONG_FACTS:
        key = fact.split(" is ")[0] if " is " in fact else fact
        if "paris" in text and "germany" in text:
            return f"verifier: 'paris is the capital of germany' contradicts reference data", False
        if "everest" in text and "europe" in text:
            return f"verifier: 'mt everest is in europe' contradicts reference data", False
    if len([l for l in output.splitlines() if l.startswith("-")]) != 3:
        return "verifier: expected 3 bullet lines", False
    if any(len(l) > 60 for l in output.splitlines()):
        return "verifier: bullet exceeds 60 chars", False
    return "verifier: ok", True


def refine(topic: str, prev: str, critique: str, history: list[Attempt]) -> str:
    return generate(topic, history)


def run_loop(topic: str, use_critic: bool, max_iters: int = 4) -> list[Attempt]:
    """运行精炼循环——生成→验证→精炼→重复直到通过"""
    history: list[Attempt] = []
    output = generate(topic, history)
    verify = verify_external if use_critic else (lambda o: feedback_self(o))
    for i in range(1, max_iters + 1):
        critique, ok = verify(output)
        history.append(Attempt(i, output, critique, ok))
        if ok:
            break
        output = refine(topic, output, critique, history)
    return history


def print_run(label: str, history: list[Attempt]) -> None:
    print(f"\n{label}")
    print("-" * 60)
    for a in history:
        tag = "OK " if a.verified else "..."
        print(f"  iter {a.iteration} {tag} critique: {a.critique}")
        for line in a.output.splitlines():
            print(f"    {line}")


def main() -> None:
    print("=" * 70)
    print("SELF-REFINE and CRITIC — Phase 14, Lesson 05")
    print("=" * 70)

    hist_self = run_loop("world facts", use_critic=False)
    print_run("Self-Refine (self-critique only)", hist_self)

    hist_critic = run_loop("world facts", use_critic=True)
    print_run("CRITIC (external verifier)", hist_critic)

    def summary(hist: list[Attempt]) -> str:
        return "passed" if hist and hist[-1].verified else "did not converge"

    print()
    print(f"Self-Refine ended: {summary(hist_self)}  after {len(hist_self)} iters")
    print(f"CRITIC    ended: {summary(hist_critic)}  after {len(hist_critic)} iters")
    print()
    print("Observation: CRITIC's verifier is grounded against reference data; a")
    print("self-critic can fail to flag its own confident-sounding hallucination.")   # 自我批评可能漏掉自信的幻觉


if __name__ == "__main__":
    main()
