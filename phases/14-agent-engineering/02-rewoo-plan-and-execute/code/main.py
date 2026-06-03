"""Toy ReWOO — Planner, Workers, Solver. Stdlib only. | 玩具 ReWOO——规划器、工作器、求解器

Demonstrates the decoupled pattern from Xu et al. (arXiv:2305.18323):
  1. Planner emits a DAG of (tool, args) steps with references (#E1, #E2, ...).
     规划器生成包含引用的计划 DAG
  2. Workers run each step in topological order.
     工作器按拓扑顺序执行每个步骤
  3. Solver composes the final answer from question + plan + evidence.
     求解器将问题+计划+证据组合成最终答案

Compare run_rewoo() vs run_react() at the bottom for token-use intuition.

核心概念：ReWOO 将 ReAct 的"边想边做"改为"先规划再执行"。
AI 对应：Devin、Claude Code 的多步骤任务、Anthropic 推荐的计划-执行工作流。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class PlanStep:
    """计划步骤——一个工具调用节点，包含 ID、工具名和参数"""
    id: str           # 步骤标识（如 E1、E2）
    tool: str         # 工具名称
    args: dict[str, Any]  # 工具参数（可包含 #E1 等引用）


@dataclass
class Plan:
    """计划——由多个步骤组成的有向无环图(DAG)"""
    steps: list[PlanStep]


class ToolRegistry:
    """工具注册表——管理可用工具的名称到函数映射"""

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., str]] = {}

    def register(self, name: str, fn: Callable[..., str]) -> None:
        """注册工具"""
        self._tools[name] = fn

    def dispatch(self, name: str, args: dict[str, Any]) -> str:
        """分派工具调用——根据名称执行对应函数"""
        fn = self._tools.get(name)
        if fn is None:
            return f"error: unknown tool {name!r}"
        try:
            return fn(**args)
        except Exception as e:
            return f"error: {type(e).__name__}: {e}"


REFERENCE_RE = re.compile(r"#E(\d+)")   # 证据引用模式——匹配 #E1, #E2 等


def resolve_references(value: Any, evidence: dict[str, str]) -> Any:
    """解析引用——将 #E1 等占位符替换为实际工作器输出"""
    if not isinstance(value, str):
        return value
    return REFERENCE_RE.sub(lambda m: evidence.get(f"E{m.group(1)}", m.group(0)),
                            value)


def topological(plan: Plan) -> list[PlanStep]:
    """拓扑排序——按依赖关系排定计划步骤的执行顺序"""
    resolved: list[PlanStep] = []
    known: set[str] = set()
    pending = list(plan.steps)
    while pending:
        progress = False
        rest: list[PlanStep] = []
        for step in pending:
            refs = REFERENCE_RE.findall(str(step.args))
            if all(f"E{r}" in known for r in refs):
                resolved.append(step)
                known.add(step.id)
                progress = True
            else:
                rest.append(step)
        if not progress:
            raise RuntimeError("cyclic plan or unresolved reference")
        pending = rest
    return resolved


def run_workers(plan: Plan, tools: ToolRegistry) -> dict[str, str]:
    """执行工作器——按拓扑顺序运行计划中的每个步骤，收集证据"""
    evidence: dict[str, str] = {}
    for step in topological(plan):
        bound_args = {k: resolve_references(v, evidence) for k, v in step.args.items()}
        evidence[step.id] = tools.dispatch(step.tool, bound_args)
    return evidence


class ScriptedPlanner:
    """脚本化规划器——返回预设的计划 DAG（真实场景中替换为 LLM 调用）"""
    def __init__(self, plan: Plan) -> None:
        self.plan = plan

    def plan_for(self, question: str) -> Plan:
        return self.plan


class ScriptedSolver:
    """脚本化求解器——使用模板组合证据生成最终答案"""
    def __init__(self, answer_template: str) -> None:
        self.template = answer_template

    def solve(self, question: str, plan: Plan, evidence: dict[str, str]) -> str:
        return self.template.format(**evidence)


def fake_search(query: str) -> str:
    """模拟搜索工具——返回预设的搜索结果"""
    if "capital of france" in query.lower():
        return "Paris"
    if "population of paris" in query.lower():
        return "11.2 million metro"
    if "capital of germany" in query.lower():
        return "Berlin"
    return f"no result for {query!r}"


def rounded_million(text: str) -> str:
    """取整工具——从文本中提取数字并四舍五入到百万"""
    m = re.search(r"([0-9]+\.?[0-9]*)", text)
    if not m:
        return "unknown"
    return f"{round(float(m.group(1)))} million"


@dataclass
class ReWOORun:
    question: str
    plan: Plan
    evidence: dict[str, str] = field(default_factory=dict)
    answer: str = ""
    planner_chars: int = 0
    worker_chars: int = 0
    solver_chars: int = 0


def run_rewoo(question: str, planner: ScriptedPlanner,
              tools: ToolRegistry, solver: ScriptedSolver) -> ReWOORun:
    """运行完整的 ReWOO 流程——规划→执行→求解"""
    plan = planner.plan_for(question)
    planner_chars = len(question) + sum(len(s.tool) + len(str(s.args))
                                        for s in plan.steps)
    evidence = run_workers(plan, tools)
    worker_chars = sum(len(str(s.args)) + len(v) for s, v in zip(plan.steps,
                                                                 evidence.values()))
    answer = solver.solve(question, plan, evidence)
    solver_chars = len(question) + worker_chars + len(answer)
    return ReWOORun(question=question, plan=plan, evidence=evidence,
                    answer=answer,
                    planner_chars=planner_chars, worker_chars=worker_chars,
                    solver_chars=solver_chars)


def run_react_mock(question: str, tools: ToolRegistry,
                   trajectory: list[tuple[str, dict[str, Any]]]) -> int:
    """模拟 ReAct 的 Token 用量——用于与 ReWOO 对比"""
    prompt_chars = len(question)
    total = 0
    history_chars = 0
    for name, args in trajectory:
        total += prompt_chars + history_chars + len(name) + len(str(args))
        obs = tools.dispatch(name, args)
        history_chars += len(name) + len(str(args)) + len(obs) + 40
    total += prompt_chars + history_chars
    return total


def main() -> None:
    print("=" * 70)
    print("REWOO — Planner, Workers, Solver (Phase 14, Lesson 02)")
    print("=" * 70)

    tools = ToolRegistry()
    tools.register("search", fake_search)
    tools.register("round_million", rounded_million)

    plan = Plan(steps=[
        PlanStep("E1", "search", {"query": "capital of France"}),       # 步骤1：搜索法国首都
        PlanStep("E2", "search", {"query": "population of #E1"}),       # 步骤2：搜索首都人口（引用 E1）
        PlanStep("E3", "round_million", {"text": "#E2"}),               # 步骤3：取整到百万（引用 E2）
    ])
    planner = ScriptedPlanner(plan)
    solver = ScriptedSolver(
        "The capital of France is {E1}; rounded population is {E3}."
    )
    run = run_rewoo("What is the population of the capital of France, rounded?",
                    planner, tools, solver)

    print("\nPLAN")
    for step in run.plan.steps:
        print(f"  {step.id}: {step.tool}({step.args})")
    print("\nEVIDENCE")
    for k, v in run.evidence.items():
        print(f"  {k} -> {v}")
    print(f"\nFINAL: {run.answer}")

    react_chars = run_react_mock(
        run.question, tools,
        [("search", {"query": "capital of France"}),
         ("search", {"query": "population of Paris"}),
         ("round_million", {"text": "11.2 million metro"})])
    rewoo_chars = run.planner_chars + run.worker_chars + run.solver_chars
    print("\nTOKEN INTUITION (chars, approximate)")
    print(f"  react total  : {react_chars}")
    print(f"  rewoo total  : {rewoo_chars}")
    print(f"  ratio        : {react_chars / max(rewoo_chars, 1):.2f}x")   # ReAct/ReWOO Token 比率
    print("\npaper claim: ~5x fewer tokens on HotpotQA. toy approximates the shape.")


if __name__ == "__main__":
    main()
