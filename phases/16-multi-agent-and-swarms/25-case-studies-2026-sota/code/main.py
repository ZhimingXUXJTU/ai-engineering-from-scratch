"""Case-study mapper: pick the closest 2026 reference for a proposed design.

Stdlib only. Scripted mapping from design attributes to one of three case
studies (Anthropic Research, MetaGPT/ChatDev, OpenClaw/Moltbook) and the
framework-of-choice recommendation.

核心概念：本节实现的核心模式
AI 对应：此模式在现代 AI Agent 系统中有广泛应用。
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Design:
    """Design"""
    name: str
    task_type: str          # "research" | "engineering" | "population" | "automation"
    n_agents_expected: int
    verification_required: bool
    runtime_duration_hours: float
    roles_distinct: bool
    user_facing_network: bool


CASES = {
    "anthropic_research": {
        "name": "Anthropic Research (supervisor-worker)",
        "patterns": ["fresh-context subagents", "orchestrator synthesis",
                     "rainbow deployment", "verification role"],
        "framework": "Anthropic Claude Agent SDK or LangGraph",
        "citation": "https://www.anthropic.com/engineering/multi-agent-research-system",
    },
    "metagpt_chatdev": {
        "name": "MetaGPT / ChatDev (SOP role-decomposition)",
        "patterns": ["role prompts encode SOP", "structured artifact handoffs",
                     "communicative dehallucination", "DAG routing at scale"],
        "framework": "CrewAI or MetaGPT reference impl",
        "citation": "arXiv:2308.00352 (MetaGPT), arXiv:2307.07924 (ChatDev), arXiv:2406.07155 (MacNet)",
    },
    "openclaw_moltbook": {
        "name": "OpenClaw / Moltbook (population-scale substrate)",
        "patterns": ["local ReAct loop", "agent-to-agent social graph",
                     "emergent economy", "prompt-injection threat model"],
        "framework": "custom substrate + MCP + A2A",
        "citation": "https://en.wikipedia.org/wiki/OpenClaw",
    },
}

FRAMEWORK_LANDSCAPE = [
    ("LangGraph", "production", "structured graph + checkpointing + HITL"),
    ("CrewAI", "production", "role-based crews; Sequential/Hierarchical"),
    ("AG2", "community maintenance", "GroupChat + speaker selection"),
    ("Microsoft Agent Framework", "RC (Feb 2026)", "orchestration patterns + enterprise"),
    ("OpenAI Agents SDK", "production", "Swarm successor; tool-return handoffs"),
    ("Google ADK", "production (Apr 2025)", "A2A-native; Google Cloud"),
    ("Anthropic Claude Agent SDK", "production", "agent + Research extension"),
]


def map_to_case(d: Design) -> str:
    """map_to_case"""
    if d.task_type == "population" or d.user_facing_network:
        return "openclaw_moltbook"  # 返回结果
    if d.task_type == "engineering" or d.roles_distinct:
        return "metagpt_chatdev"  # 返回结果
    if d.task_type == "research":
        return "anthropic_research"  # 返回结果
    if d.verification_required and d.runtime_duration_hours >= 1:
        return "anthropic_research"  # 返回结果
    return "anthropic_research"  # 返回结果


def print_case(key: str) -> None:
    """print_case"""
    case = CASES[key]
    print(f"\n  closest case study: {case['name']}")
    print(f"  patterns to copy:")
    for p in case["patterns"]:
        print(f"    - {p}")
    print(f"  recommended framework: {case['framework']}")
    print(f"  citation: {case['citation']}")


def print_landscape() -> None:
    """print_landscape"""
    print("\n" + "=" * 78)
    print("FRAMEWORK LANDSCAPE — April 2026")
    print("=" * 78)
    print(f"  {'framework':30s} {'status':22s} {'best for':30s}")
    for name, status, best_for in FRAMEWORK_LANDSCAPE:
        print(f"  {name:30s} {status:22s} {best_for:30s}")
    print("\n  every major framework ships MCP support; most ship A2A.")
    print("  protocol compatibility is no longer a differentiator -- handoff semantics are.")


def main() -> None:
    """main"""
    designs = [
        Design("research-assistant", "research", 6, True, 2.0, False, False),
        Design("codegen-team", "engineering", 5, True, 1.0, True, False),
        Design("agent-marketplace", "population", 1000, False, 24.0, False, True),
        Design("internal-automation", "automation", 3, True, 0.5, True, False),
    ]

    print("=" * 78)
    print("CASE-STUDY MAPPER — proposed designs → closest 2026 reference")
    print("=" * 78)

    for d in designs:
        print(f"\ndesign: {d.name!r}")
        print(f"  type={d.task_type}  n_agents={d.n_agents_expected}  "
              f"verification={d.verification_required}  hours={d.runtime_duration_hours}")
        case_key = map_to_case(d)
        print_case(case_key)

    print_landscape()

    print("\nTakeaways:")
    print("  pick a case study first; adapt the design to match its known trade-offs.")
    print("  every 2026 framework supports MCP; most support A2A -- choose on handoff semantics.")
    print("  production-grade multi-agent needs: verification, cost accounting, rainbow deploys.")


if __name__ == "__main__":
    main()  # 运行主函数
