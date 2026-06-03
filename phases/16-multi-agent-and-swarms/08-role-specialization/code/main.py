"""Role specialization: planner, executor, critic, verifier.

Builds a small Python function. Critic (LLM-simulated) and verifier (code)
together catch bugs that either alone would miss.

Run twice: once with correct executor output, once with off-spec output.

核心概念：本节实现的核心模式
AI 对应：此模式在现代 AI Agent 系统中有广泛应用。
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Spec:
    """Spec"""
    task_name: str
    signature: str
    description: str
    tests: list[tuple[tuple, int]]


@dataclass
class Artifact:
    """Artifact"""
    code: str


@dataclass
class CriticReport:
    """CriticReport"""
    approved: bool
    notes: list[str] = field(default_factory=list)


@dataclass
class VerifierReport:
    """VerifierReport"""
    passed: bool
    failures: list[str] = field(default_factory=list)


def planner(user_wish: str) -> Spec:
    """Produces a structured spec from a high-level wish."""
    return Spec(  # 返回结果
        task_name="add_two",
        signature="add_two(a: int, b: int) -> int",
        description=user_wish,
        tests=[((1, 2), 3), ((10, 20), 30), ((-5, 5), 0)],
    )


def executor_correct(spec: Spec) -> Artifact:
    """executor_correct"""
    return Artifact(code="def add_two(a, b):\n    return a + b\n")  # 返回结果


def executor_buggy(spec: Spec) -> Artifact:
    """executor_buggy"""
    return Artifact(code="def add_two(a, b):\n    return a * b\n")  # 返回结果


def critic(spec: Spec, art: Artifact) -> CriticReport:
    """LLM-style review. Pattern-matches against common issues but can be fooled
    by plausible-looking code that is semantically wrong."""
    notes: list[str] = []
    if "def" not in art.code:
        notes.append("missing def statement")
    if "return" not in art.code:
        notes.append("missing return")
    if spec.task_name not in art.code:
        notes.append(f"function name does not match spec '{spec.task_name}'")
    approved = not notes
    return CriticReport(approved=approved, notes=notes)  # 返回结果


def verifier(spec: Spec, art: Artifact) -> VerifierReport:
    """Run the code in a sandbox namespace and execute the tests. Deterministic."""
    ns: dict = {}
    try:
        exec(art.code, ns, ns)
    except Exception as e:
        return VerifierReport(passed=False, failures=[f"exec error: {e}"])  # 返回结果
    fn = ns.get(spec.task_name)
    if not callable(fn):
        return VerifierReport(passed=False, failures=[f"no callable '{spec.task_name}' produced"])  # 返回结果
    failures: list[str] = []
    for args, expected in spec.tests:
        try:
            got = fn(*args)
        except Exception as e:
            failures.append(f"call {args} raised {e}")
            continue
        if got != expected:
            failures.append(f"call {args}: expected {expected}, got {got}")
    return VerifierReport(passed=not failures, failures=failures)  # 返回结果


def run_pipeline(user_wish: str, executor, label: str) -> None:
    """run_pipeline"""
    print(f"\n=== {label} ===")
    spec = planner(user_wish)
    print(f"  [planner] spec: {spec.signature} with {len(spec.tests)} tests")
    art = executor(spec)
    print(f"  [executor] produced:\n    {art.code.replace(chr(10), chr(10)+'    ')}")
    crep = critic(spec, art)
    print(f"  [critic] approved={crep.approved}, notes={crep.notes}")
    vrep = verifier(spec, art)
    print(f"  [verifier] passed={vrep.passed}, failures={vrep.failures}")
    if crep.approved and vrep.passed:
        print("  RESULT: ship it.")
    elif not vrep.passed:
        print("  RESULT: verifier blocked ship (deterministic catch).")
    elif not crep.approved:
        print("  RESULT: critic blocked ship (subjective catch).")


def main() -> None:
    """main"""
    print("Role specialization pipeline — planner, executor, critic, verifier")
    print("-" * 70)

    run_pipeline(
        "A function that returns the sum of two integers.",
        executor_correct,
        "Correct executor output",
    )

    run_pipeline(
        "A function that returns the sum of two integers.",
        executor_buggy,
        "Buggy executor output (looks plausible; fails runtime)",
    )

    print("\nKey insight: the critic passes the buggy code because it looks fine.")
    print("Only the verifier -- deterministic test execution -- catches the semantic bug.")
    print("All-LLM pipelines (no verifier) would ship the bug. Classic MAST failure mode.")


if __name__ == "__main__":
    main()  # 运行主函数
