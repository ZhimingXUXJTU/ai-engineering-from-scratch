"""LangGraph-shaped stateful graph in stdlib, with checkpoint and resume.

State is a typed dict. Nodes return update dicts. Runtime serializes state
after every node so resume picks up exactly where it left off.

核心概念：有状态图 + 检查点恢复 —— 用图结构定义 Agent 的工作流，每个节点
是一个处理函数，节点之间通过条件边连接。状态在每个节点执行后自动保存到检查点，
支持从任意节点恢复执行（无需从头重跑）。这是 LangGraph 的核心抽象。

AI 对应：LangGraph 是目前最流行的 Agent 框架之一，被众多企业用于构建生产级 Agent。
其检查点机制类似于数据库的 WAL（Write-Ahead Log），确保长时间运行的 Agent
不会因故障而丢失进度。OpenAI 的 Assistants API、Anthropic 的 Agent SDK
也提供了类似的状态持久化能力。
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from typing import Any, Callable


State = dict[str, Any]
Update = dict[str, Any]
NodeFn = Callable[[State], Update]
Router = Callable[[State], str]


START = "__start__"
END = "__end__"


@dataclass
class Edge:
    src: str
    dst: str
    router: Router | None = None


class StateGraph:
    """状态图 —— 定义节点和边，支持条件路由，是 LangGraph 的核心抽象。"""
    def __init__(self) -> None:
        self.nodes: dict[str, NodeFn] = {}
        self.edges: dict[str, list[Edge]] = {}
        self.entry: str | None = None

    def add_node(self, name: str, fn: NodeFn) -> None:
        self.nodes[name] = fn

    def set_entry(self, name: str) -> None:
        self.entry = name

    def add_edge(self, src: str, dst: str) -> None:
        self.edges.setdefault(src, []).append(Edge(src=src, dst=dst))

    def add_conditional_edges(self, src: str, router: Router,
                              targets: dict[str, str]) -> None:
        """添加条件边 —— 根据路由函数的返回值决定下一步走哪条边。"""
        for value, dst in targets.items():
            self.edges.setdefault(src, []).append(
                Edge(src=src, dst=dst, router=_make_router(router, value))
            )

    def _next(self, current: str, state: State) -> str | None:
        for edge in self.edges.get(current, []):
            if edge.router is None or edge.router(state):
                return edge.dst
        return None


def _make_router(router: Router, expected: str) -> Router:
    def fn(state: State) -> bool:
        return router(state) == expected
    return fn


class InMemoryCheckpointer:
    """内存检查点 —— 每个节点执行后保存状态快照，支持加载最新快照和查询历史。"""
    def __init__(self) -> None:
        self._store: dict[str, list[tuple[str, State]]] = {}

    def save(self, session_id: str, step_name: str, state: State) -> None:
        self._store.setdefault(session_id, []).append((step_name, copy.deepcopy(state)))

    def load_latest(self, session_id: str) -> tuple[str, State] | None:
        history = self._store.get(session_id, [])
        if not history:
            return None
        return history[-1]

    def history(self, session_id: str) -> list[tuple[str, State]]:
        return list(self._store.get(session_id, []))


class PausedAtNode(Exception):
    """暂停异常 —— 当节点需要人工审批时抛出，携带当前节点名和状态。"""
    def __init__(self, node: str, state: State) -> None:
        super().__init__(node)
        self.node = node
        self.state = state


class Runner:
    """图执行器 —— 驱动状态图运行，在每个节点后保存检查点，支持暂停和恢复。"""
    def __init__(self, graph: StateGraph,
                 checkpointer: InMemoryCheckpointer) -> None:
        self.graph = graph
        self.checkpointer = checkpointer

    def run(self, session_id: str, initial_state: State,
            resume_from: str | None = None,
            state_override: State | None = None) -> State:
        """运行图 —— 从指定节点开始执行，每步保存检查点，遇到暂停则抛出异常。"""
        if state_override is not None:
            state = copy.deepcopy(state_override)
        else:
            state = copy.deepcopy(initial_state)
        current = resume_from or self.graph.entry  # 确定起始节点
        if current is None:
            raise RuntimeError("no entry node set")
        while current is not None and current != END:
            fn = self.graph.nodes.get(current)
            if fn is None:
                raise RuntimeError(f"unknown node {current!r}")
            update = fn(state)  # 执行节点函数，获取状态更新
            if update is None:
                update = {}
            state = {**state, **update}  # 合并状态更新
            self.checkpointer.save(session_id, current, state)  # 保存检查点
            if state.get("_pause_reason"):  # 检查是否需要暂停等待人工审批
                reason = state.pop("_pause_reason")
                raise PausedAtNode(current, state)
            current = self.graph._next(current, state)  # 路由到下一个节点
        return state


def _classify(state: State) -> Update:
    text = state["input"].lower()
    if "refund" in text or "money back" in text:
        route = "refund"
    elif "crash" in text or "bug" in text or "error" in text:
        route = "bug"
    elif "pricing" in text or "quote" in text:
        route = "sales"
    else:
        route = "sales"
    return {"route": route, "step": state.get("step", 0) + 1}


def _refund(state: State) -> Update:
    return {"ticket": f"REF-{state.get('input', '')[:12]}",
            "step": state.get("step", 0) + 1}


def _bug(state: State) -> Update:
    return {"ticket": f"BUG-{state.get('input', '')[:12]}",
            "step": state.get("step", 0) + 1}


def _sales(state: State) -> Update:
    return {"ticket": f"SAL-{state.get('input', '')[:12]}",
            "step": state.get("step", 0) + 1}


def _human_gate(state: State) -> Update:
    if not state.get("human_approval"):
        return {"_pause_reason": "awaiting human approval",
                "step": state.get("step", 0) + 1}
    return {"step": state.get("step", 0) + 1}


def _send(state: State) -> Update:
    return {"output": f"sent {state.get('ticket')}",
            "step": state.get("step", 0) + 1}


def build_graph() -> StateGraph:
    graph = StateGraph()
    graph.add_node("classify", _classify)
    graph.add_node("refund", _refund)
    graph.add_node("bug", _bug)
    graph.add_node("sales", _sales)
    graph.add_node("human_gate", _human_gate)
    graph.add_node("send", _send)
    graph.set_entry("classify")

    graph.add_conditional_edges(
        "classify",
        router=lambda s: s["route"],
        targets={"refund": "refund", "bug": "bug", "sales": "sales"},
    )
    graph.add_edge("refund", "human_gate")
    graph.add_edge("bug", "human_gate")
    graph.add_edge("sales", "human_gate")
    graph.add_edge("human_gate", "send")
    graph.add_edge("send", END)
    return graph


def main() -> None:
    print("=" * 70)
    print("LANGGRAPH STATE MACHINE — Phase 14, Lesson 13")
    print("=" * 70)

    graph = build_graph()
    ckpt = InMemoryCheckpointer()
    runner = Runner(graph, ckpt)

    session = "s001"
    initial: State = {"input": "the CLI crashes on ctrl-c, please fix",
                      "step": 0, "human_approval": False}

    print("\nfirst run (will pause at human_gate)")
    try:
        final = runner.run(session, initial)
        print(f"  final: {final}")
    except PausedAtNode as paused:
        print(f"  PAUSED at {paused.node}")
        print(f"  state at pause: {json.dumps(paused.state, default=str)}")

    print("\ncheckpoint history")
    for node, snap in ckpt.history(session):
        print(f"  {node}  route={snap.get('route')}  "
              f"ticket={snap.get('ticket')}  step={snap.get('step')}")

    print("\nhuman approves; resume from next node after human_gate")
    latest = ckpt.load_latest(session)
    assert latest is not None
    last_node, last_state = latest
    approved_state = {**last_state, "human_approval": True}
    approved_state.pop("_pause_reason", None)
    ckpt.save(session, f"{last_node}_reviewed", approved_state)

    final = runner.run(
        session_id=session,
        initial_state=initial,
        resume_from="send",
        state_override=approved_state,
    )
    print(f"  final: {final}")

    print()
    print("property: state serializes after every node; resume is exact.")
    print("no fresh re-runs after step 38 fails; pick up at step 39.")


if __name__ == "__main__":
    main()  # 运行主函数
