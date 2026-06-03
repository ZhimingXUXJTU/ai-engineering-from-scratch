"""Toy Reflexion loop — Actor, Evaluator, Self-Reflector, Episodic memory.
玩具 Reflexion 循环——执行器、评估器、自我反思器、情景记忆。

Task: pick three integers from 1..9 that sum to a target. The Actor is
scripted to start with a bad strategy and adapt when reflections are present.
任务：选择三个 1..9 的整数使其总和等于目标值。执行器从错误策略开始，
当反思存在时会适应改进。

核心概念：Reflexion 用自然语言反思替代梯度更新，实现"从失败中学习"。
AI 对应：Claude Code 的 CLAUDE.md、Letta 的 sleep-time compute 都基于此模式。
"""

from __future__ import annotations

from dataclasses import dataclass, field


TARGET = 20    # 目标总和


@dataclass
class Reflection:
    """反思记录——记录一次失败后的自然语言反思"""
    trial: int     # 试验编号
    text: str      # 反思文本


@dataclass
class EpisodicMemory:
    """情景记忆——存储历史反思的有界缓冲区 | AI 对应：Agent 的跨会话经验存储"""
    items: list[Reflection] = field(default_factory=list)
    max_len: int = 6     # 最大容量——防止记忆腐化

    def add(self, r: Reflection) -> None:
        """添加反思，超出容量时移除最早的"""
        self.items.append(r)
        if len(self.items) > self.max_len:
            self.items.pop(0)

    def as_prompt(self) -> str:
        """将反思格式化为提示词——注入到下一轮的上下文中"""
        if not self.items:
            return "(no prior reflections)"
        lines = [f"- trial {r.trial}: {r.text}" for r in self.items]
        return "\n".join(lines)


class Actor:
    """脚本化执行器——根据情景记忆调整策略。无反思时保持错误选择，有反思时趋向目标。
    AI 对应：真实场景中替换为 LLM，根据反思历史调整行动计划。"""

    def act(self, memory: EpisodicMemory) -> list[int]:
        """根据记忆中的反思数量决定行动策略"""
        n = len(memory.items)
        if n == 0:
            return [1, 2, 3]       # 无反思：使用初始错误策略
        if n == 1:
            return [5, 6, 7]       # 有1条反思：改进但仍不够
        if n == 2:
            return [6, 7, 7]       # 有2条反思：接近目标
        return [6, 7, 7]


def binary_evaluator(attempt: list[int], target: int) -> tuple[bool, int]:
    """二元评估器——检查总和是否等于目标，返回(是否成功, 差值)"""
    total = sum(attempt)
    return total == target, total - target


class SelfReflector:
    """自我反思器——分析失败原因并生成自然语言反思 | AI 对应：LLM 对自身输出的自我批评"""

    def reflect(self, attempt: list[int], delta: int) -> str:
        """根据差值生成反思文本"""
        if delta < 0:
            return f"sum {sum(attempt)} is {-delta} short; pick larger values"
        if delta > 0:
            return f"sum {sum(attempt)} overshoots by {delta}; pick smaller values"
        return "succeeded"


@dataclass
class TrialResult:
    """试验结果——记录每次尝试的完整信息"""
    trial: int            # 试验编号
    attempt: list[int]    # 尝试的数字列表
    success: bool         # 是否成功
    delta: int            # 与目标的差值
    reflection: str       # 反思文本


def run_reflexion(max_trials: int, use_memory: bool) -> list[TrialResult]:
    """运行 Reflexion 循环——Actor→Evaluator→Self-Reflector→Memory 的迭代"""
    actor = Actor()
    reflector = SelfReflector()
    memory = EpisodicMemory()
    trials: list[TrialResult] = []
    for t in range(1, max_trials + 1):
        attempt = actor.act(memory if use_memory else EpisodicMemory())  # 执行器行动
        success, delta = binary_evaluator(attempt, TARGET)               # 评估器评分
        text = reflector.reflect(attempt, delta)                          # 自我反思
        trials.append(TrialResult(t, attempt, success, delta, text))
        if success:
            break
        memory.add(Reflection(trial=t, text=text))   # 将反思存入情景记忆
    return trials


def summarize(trials: list[TrialResult], name: str) -> None:
    """打印试验摘要"""
    print(f"\n{name}")
    print("-" * 60)
    for r in trials:
        mark = "OK " if r.success else "..."
        print(f"  trial {r.trial}: {r.attempt} sum={sum(r.attempt)} "
              f"delta={r.delta:+d} {mark} -> {r.reflection}")
    last = trials[-1]
    print(f"  final: {'success' if last.success else 'failed'} "
          f"at trial {last.trial}")


def main() -> None:
    print("=" * 70)
    print(f"REFLEXION — pick three ints in [1..9] summing to {TARGET}")
    print("Phase 14, Lesson 03")
    print("=" * 70)

    trials_no_mem = run_reflexion(max_trials=4, use_memory=False)
    summarize(trials_no_mem, "BASELINE (no episodic memory)")

    trials_mem = run_reflexion(max_trials=4, use_memory=True)
    summarize(trials_mem, "REFLEXION (episodic memory on)")

    baseline_steps = len(trials_no_mem)
    reflex_steps = len(trials_mem)
    print()
    print(f"baseline used {baseline_steps} trials; reflexion used {reflex_steps}.")  # 基线 vs Reflexion 的试验次数
    print("Without a reflection in the prompt, the scripted actor never adapts.")     # 无反思时执行器永不适应
    print("With one reflection, the actor corrects; with two, it converges.")         # 有反思时逐步收敛


if __name__ == "__main__":
    main()
