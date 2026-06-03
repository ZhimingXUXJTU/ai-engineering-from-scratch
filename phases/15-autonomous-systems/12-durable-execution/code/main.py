"""Minimal durable-execution engine — stdlib Python.

Models the workflow / activity / event-log pattern used by Temporal, LangGraph
checkpointing, Microsoft Agent Framework, and Claude Code Routines.

Activities are logged with inputs before execution and outputs after. A
replay of a workflow re-runs the workflow code but returns cached outputs
for activities whose event is already in the log. A crash mid-run loses
only the incomplete activity.

核心概念：本节实现的核心模式
AI 对应：此模式在现代 AI Agent 系统中有广泛应用。
"""

from __future__ import annotations

import functools
import json
import os
import tempfile
from dataclasses import dataclass


# ---------- Event log ----------

@dataclass
class EventLog:
    """EventLog"""
    path: str

    def __post_init__(self) -> None:
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def events(self) -> list[dict]:
        with open(self.path) as f:
            return json.load(f)  # 返回结果

    def append(self, ev: dict) -> None:
        evs = self.events()
        evs.append(ev)
        with open(self.path, "w") as f:
            json.dump(evs, f)

    def lookup(self, name: str, args: tuple) -> dict | None:
        for ev in self.events():
            if ev["name"] == name and ev["args"] == list(args) and ev["status"] == "done":
                return ev  # 返回结果
        return None  # 返回结果


# ---------- Activity decorator ----------

def activity(name: str):
    """activity"""
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(log: EventLog, *args):
            hit = log.lookup(name, args)
            if hit:
                print(f"    [replay] {name}({args}) -> {hit['result']} (from log)")
                return hit["result"]  # 返回结果
            log.append({"name": name, "args": list(args), "status": "started"})
            result = fn(*args)
            log.append({"name": name, "args": list(args),
                        "status": "done", "result": result})
            print(f"    [run]    {name}({args}) -> {result}")
            return result  # 返回结果
        return wrapper  # 返回结果
    return deco  # 返回结果


# ---------- Example activities ----------

@activity("fetch_docs")
def fetch_docs(query: str) -> int:
    """fetch_docs"""
    # Pretend to hit an API; return number of docs.
    return len(query) * 3  # 返回结果


@activity("call_llm")
def call_llm(doc_count: int) -> str:
    """call_llm"""
    # Pretend LLM call; deterministic here for pedagogy.
    return f"summary({doc_count}_docs)"  # 返回结果


@activity("write_report")
def write_report(summary: str) -> str:
    """write_report"""
    # Pretend tool call with a side effect.
    return f"report://{summary}"  # 返回结果


# ---------- Workflow ----------

def workflow(log: EventLog, query: str, crash_after: int = -1) -> str:
    """Three-activity workflow with an optional crash for pedagogy."""
    doc_count = fetch_docs(log, query)
    if crash_after == 1:
        raise RuntimeError("simulated crash after fetch_docs")
    summary = call_llm(log, doc_count)
    if crash_after == 2:
        raise RuntimeError("simulated crash after call_llm")
    report = write_report(log, summary)
    return report  # 返回结果


# ---------- Driver ----------

def reset_log(path: str) -> EventLog:
    """reset_log"""
    if os.path.exists(path):
        os.remove(path)
    return EventLog(path)  # 返回结果


def count_runs(log: EventLog) -> int:
    """count_runs"""
    return sum(1 for ev in log.events() if ev["status"] == "started")  # 返回结果


def main() -> None:
    """main"""
    print("=" * 70)
    print("DURABLE EXECUTION (Phase 15, Lesson 12)")
    print("=" * 70)

    tmpdir = tempfile.mkdtemp()

    # Naive retry: lose the event log on crash. Every restart re-runs
    # everything.
    print("\nNaive retry (no event log persisted)")
    print("-" * 70)
    for attempt in range(1, 4):
        log = reset_log(os.path.join(tmpdir, "naive.json"))
        print(f"  attempt {attempt}:")
        try:
            crash = 2 if attempt == 1 else -1
            r = workflow(log, "hello", crash_after=crash)
            print(f"    -> result {r}")
            print(f"    -> {count_runs(log)} activity starts this attempt")
            break
        except RuntimeError as e:
            print(f"    -> crash: {e}; {count_runs(log)} activity starts wasted")

    # Durable retry: keep the event log across attempts; replay does not
    # re-execute completed activities.
    print("\nDurable retry (event log preserved across attempts)")
    print("-" * 70)
    durable_path = os.path.join(tmpdir, "durable.json")
    if os.path.exists(durable_path):
        os.remove(durable_path)

    for attempt in range(1, 4):
        log = EventLog(durable_path)
        print(f"  attempt {attempt}:")
        try:
            crash = 2 if attempt == 1 else -1
            r = workflow(log, "hello", crash_after=crash)
            print(f"    -> result {r}")
            print(f"    -> {count_runs(log)} total activity starts across attempts")
            break
        except RuntimeError as e:
            print(f"    -> crash: {e}")

    print()
    print("=" * 70)
    print("HEADLINE: durability makes long-horizon runs affordable to fail")
    print("-" * 70)
    print("  Naive retry re-executes every activity on every attempt.")
    print("  Durable retry replays completed activities from the log;")
    print("  only the missing activity actually runs. Same design used")
    print("  by Temporal, LangGraph checkpointing, Microsoft Agent")
    print("  Framework, and Claude Code Routines. The LLM call is")
    print("  just another non-deterministic activity in the log.")


if __name__ == "__main__":
    main()  # 运行主函数
