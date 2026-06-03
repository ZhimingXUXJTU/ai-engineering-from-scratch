"""Toy ReAct agent loop — stdlib only. | 玩具 ReAct Agent 循环——仅使用标准库

Implements the five ingredients from docs/en.md:
  1. message buffer        # 消息缓冲区——存储对话历史
  2. tool registry         # 工具注册表——名称到可调用函数的映射
  3. stop condition        # 停止条件——触发循环退出
  4. turn budget           # 轮次预算——防止无限循环
  5. observation formatter # 观察格式化器——将工具输出转为模型可读字符串

ToyLLM is a scripted policy so the loop runs offline and deterministic. Swap
ToyLLM for a real provider client and the control flow is identical.

核心概念：ReAct 循环（Reason + Act）是所有现代 AI Agent 的基础架构。
AI 对应：Claude Code、GPT Agent、Devin 等都基于此循环——观察→思考→行动→重复。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ToolCall:
    """工具调用数据类——记录模型请求调用的工具名称和参数"""
    name: str
    args: dict[str, Any]


@dataclass
class Turn:
    """对话轮次数据类——记录循环中每一步的类型、内容、工具调用和观察结果"""
    kind: str       # 类型：user / thought / action / final
    content: str    # 文本内容
    tool_call: ToolCall | None = None      # 关联的工具调用（仅 action 类型）
    observation: str | None = None          # 工具返回的观察结果


class ToolRegistry:
    """工具注册表——管理 Agent 可调用的工具集合 | AI 对应：类似 Claude Code 的工具系统"""
    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., str]] = {}

    def register(self, name: str, fn: Callable[..., str]) -> None:
        """注册工具——将函数名映射到可调用对象"""
        self._tools[name] = fn

    def names(self) -> list[str]:
        """返回所有已注册工具的名称列表"""
        return sorted(self._tools)

    def dispatch(self, call: ToolCall) -> str:
        """分派工具调用——根据名称查找并执行对应函数，返回结果字符串"""
        fn = self._tools.get(call.name)
        if fn is None:
            return f"error: unknown tool {call.name!r}"   # 未知工具——返回错误观察
        try:
            return fn(**call.args)
        except TypeError as e:
            return f"error: bad args for {call.name}: {e}"    # 参数错误——返回错误观察
        except Exception as e:
            return f"error: {type(e).__name__}: {e}"          # 其他异常——返回错误观察而非崩溃


def calculator(expr: str) -> str:
    """计算器工具——安全地执行数学表达式 | AI 对应：Agent 的基础计算能力"""
    allowed = set("0123456789+-*/(). ")
    if not set(expr).issubset(allowed):
        return "error: illegal character in expr"    # 非法字符——防止注入攻击
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))    # 安全 eval：禁用内置函数
    except Exception as e:
        return f"error: {type(e).__name__}: {e}"


class KVStore:
    """键值存储工具——Agent 的简单记忆机制 | AI 对应：Agent 的短期工作记忆"""
    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def get(self, key: str) -> str:
        """获取键值"""
        return self._store.get(key, f"missing:{key}")

    def set(self, key: str, value: str) -> str:
        """设置键值"""
        self._store[key] = value
        return f"stored {key}"


class ToyLLM:
    """Scripted ReAct policy. Returns one assistant turn per call.
    脚本化的 ReAct 策略——每次调用返回一个助手轮次。

    Each script entry is either ('thought', text) plus ('action', name, args)
    or ('finish', text). The loop runs through the script in order.
    每个脚本条目是（思考+行动）或（完成）。循环按顺序执行脚本。
    AI 对应：真实场景中替换为 Claude/GPT API 调用。
    """

    def __init__(self, script: list[dict[str, Any]]) -> None:
        self.script = script
        self.cursor = 0

    def respond(self, history: list[Turn]) -> dict[str, Any]:
        """根据脚本返回下一个响应——模拟 LLM 的输出"""
        if self.cursor >= len(self.script):
            return {"kind": "finish", "content": "no more actions"}
        entry = self.script[self.cursor]
        self.cursor += 1
        return entry


@dataclass
class AgentLoop:
    """Agent 循环——ReAct 的核心实现 | AI 对应：所有 Agent 框架（Claude Code、LangGraph 等）的底层循环"""
    llm: ToyLLM
    tools: ToolRegistry
    max_turns: int = 12                         # 轮次预算——防止无限循环
    history: list[Turn] = field(default_factory=list)   # 消息缓冲区

    def run(self, user_message: str) -> str:
        """运行 Agent 循环——观察→思考→行动→重复直到停止"""
        self.history.append(Turn(kind="user", content=user_message))
        for step in range(self.max_turns):
            reply = self.llm.respond(self.history)
            if reply["kind"] == "finish":        # 停止条件：模型输出 finish
                self.history.append(Turn(kind="final", content=reply["content"]))
                return reply["content"]
            thought = reply.get("thought", "")
            self.history.append(Turn(kind="thought", content=thought))   # 记录思考步骤
            call = ToolCall(name=reply["action"], args=reply.get("args", {}))
            observation = self.tools.dispatch(call)       # 执行工具调用，获取观察结果
            self.history.append(
                Turn(kind="action", content=call.name,
                     tool_call=call, observation=observation)
            )
        self.history.append(Turn(kind="final",
                                 content="budget exhausted"))   # 轮次预算耗尽
        return "budget exhausted"


def pretty_trace(history: list[Turn]) -> None:
    """格式化打印完整的 ReAct 轨迹——用于调试和可视化"""
    for i, turn in enumerate(history):
        tag = f"[{i:02d} {turn.kind:>7}]"
        if turn.kind == "user":
            print(f"{tag} {turn.content}")
        elif turn.kind == "thought":
            print(f"{tag} {turn.content}")
        elif turn.kind == "action":
            call = turn.tool_call
            assert call is not None
            print(f"{tag} {call.name}({call.args}) -> {turn.observation}")
        elif turn.kind == "final":
            print(f"{tag} {turn.content}")


def build_demo_agent() -> AgentLoop:
    """构建演示 Agent——注册工具并定义执行脚本"""
    tools = ToolRegistry()
    tools.register("calculator", calculator)
    kv = KVStore()
    tools.register("kv_get", kv.get)
    tools.register("kv_set", kv.set)

    # 脚本定义了 Agent 的执行步骤（真实场景中由 LLM 动态生成）
    script: list[dict[str, Any]] = [
        {"kind": "action", "thought": "store the base price",       # 思考：存储基础价格
         "action": "kv_set", "args": {"key": "base", "value": "120"}},
        {"kind": "action", "thought": "compute 15% tax",            # 思考：计算 15% 税费
         "action": "calculator", "args": {"expr": "120 * 0.15"}},
        {"kind": "action", "thought": "store the tax",              # 思考：存储税费
         "action": "kv_set", "args": {"key": "tax", "value": "18.0"}},
        {"kind": "action", "thought": "compute total",              # 思考：计算总价
         "action": "calculator", "args": {"expr": "120 + 18.0"}},
        {"kind": "action", "thought": "confirm stored values",      # 思考：确认存储的值
         "action": "kv_get", "args": {"key": "base"}},
        {"kind": "finish", "content": "the total including 15% tax is 138.0"},  # 完成：返回最终答案
    ]
    return AgentLoop(llm=ToyLLM(script), tools=tools, max_turns=10)


def main() -> None:
    print("=" * 70)
    print("TOY REACT LOOP — Phase 14, Lesson 01")
    print("=" * 70)
    agent = build_demo_agent()
    final = agent.run("What is 120 plus 15% tax, stored in kv?")
    print()
    pretty_trace(agent.history)
    print()
    print(f"final answer: {final}")       # 最终答案
    print(f"turns used:   {len([t for t in agent.history if t.kind == 'action'])}")  # 使用的轮次数
    print(f"tools used:   {agent.tools.names()}")  # 使用的工具列表


if __name__ == "__main__":
    main()
