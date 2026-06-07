"""Stdlib tool registry with JSON Schema subset validation and parallel dispatch.

Subset: required fields, string/int/number/bool/array/object, enum, minimum/maximum.
Returns structured observations for every validation failure so an agent can retry.

核心概念：工具注册表 + JSON Schema 验证 + 并行调度 —— LLM 函数调用的核心基础设施。
Agent 通过工具注册表发现可用工具，调度器验证参数类型、枚举值和数值范围，
验证失败时返回结构化错误而非抛异常，让 Agent 可以自动重试。

AI 对应：OpenAI 的 function calling、Anthropic 的 tool_use、Google 的 functionDeclaration
都采用相同的 JSON Schema 描述工具接口。LangChain 的 Tool 类、Pydantic 的模型验证
也是这个模式的变体。理解这套基础设施是构建可靠 Agent 的前提。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ToolDef:
    """工具定义 —— 描述一个可供 LLM 调用的工具，包含名称、描述、参数 schema 和执行函数。"""
    name: str
    description: str
    input_schema: dict[str, Any]  # JSON Schema 格式的参数描述
    executor: Callable[..., str]  # 实际执行工具逻辑的函数
    timeout_s: float = 5.0


@dataclass
class ToolCall:
    """工具调用请求 —— LLM 返回的结构化调用指令，包含调用 ID、工具名和参数。"""
    tool_use_id: str
    name: str
    args: dict[str, Any]


@dataclass
class ToolResult:
    """工具执行结果 —— 包含调用 ID、成功/失败标志和内容字符串。"""
    tool_use_id: str
    ok: bool
    content: str


def _coerce(value: Any, schema: dict[str, Any]) -> tuple[Any, str | None]:
    """类型强制转换 —— 尝试将值转换为 schema 指定的类型，失败则返回错误信息。"""
    t = schema.get("type")
    if t == "integer":
        if isinstance(value, int) and not isinstance(value, bool):
            return value, None
        if isinstance(value, str):
            try:
                return int(value), None
            except ValueError:
                return value, f"cannot coerce string {value!r} to integer"
        return value, f"expected integer, got {type(value).__name__}"
    if t == "number":
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value), None
        if isinstance(value, str):
            try:
                return float(value), None
            except ValueError:
                return value, f"cannot coerce string {value!r} to number"
        return value, f"expected number, got {type(value).__name__}"
    if t == "boolean":
        if isinstance(value, bool):
            return value, None
        return value, f"expected boolean, got {type(value).__name__}"
    if t == "string":
        if isinstance(value, str):
            return value, None
        return value, f"expected string, got {type(value).__name__}"
    if t == "array":
        if isinstance(value, list):
            return value, None
        return value, f"expected array, got {type(value).__name__}"
    if t == "object":
        if isinstance(value, dict):
            return value, None
        return value, f"expected object, got {type(value).__name__}"
    return value, None


def validate(args: dict[str, Any], schema: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """参数验证 —— 检查必填字段、类型转换、枚举值和数值范围，返回验证后的参数和错误列表。"""
    errors: list[str] = []
    props = schema.get("properties", {})
    required = schema.get("required", [])
    out: dict[str, Any] = {}

    for name in required:
        if name not in args:
            errors.append(f"missing required: {name}")

    for name, value in args.items():
        prop = props.get(name)
        if prop is None:
            errors.append(f"unknown field: {name}")
            continue
        coerced, err = _coerce(value, prop)
        if err:
            errors.append(f"{name}: {err}")
            continue
        if "enum" in prop and coerced not in prop["enum"]:
            errors.append(f"{name}: {coerced!r} not in {prop['enum']}")
            continue
        if prop.get("type") in ("number", "integer"):
            if "minimum" in prop and coerced < prop["minimum"]:
                errors.append(f"{name}: {coerced} < minimum {prop['minimum']}")
                continue
            if "maximum" in prop and coerced > prop["maximum"]:
                errors.append(f"{name}: {coerced} > maximum {prop['maximum']}")
                continue
        out[name] = coerced

    return out, errors


class ToolRegistry:
    """工具注册表 —— 管理所有可用工具，提供注册、目录查询和调度功能。"""

    def __init__(self) -> None:
        self._tools: dict[str, ToolDef] = {}

    def register(self, tool: ToolDef) -> None:
        """注册一个工具到注册表。"""
        self._tools[tool.name] = tool

    def catalog(self) -> list[dict[str, Any]]:
        """返回所有工具的目录信息（名称、描述、参数 schema），供 LLM 了解可用工具。"""
        return [
            {"name": t.name, "description": t.description,
             "input_schema": t.input_schema}
            for t in self._tools.values()
        ]

    def dispatch(self, call: ToolCall) -> ToolResult:
        """调度单个工具调用 —— 验证参数后执行工具，捕获所有异常返回结构化结果。"""
        tool = self._tools.get(call.name)
        if tool is None:
            return ToolResult(call.tool_use_id, False,
                              f"error: unknown tool {call.name!r}")
        validated, errors = validate(call.args, tool.input_schema)
        if errors:
            return ToolResult(call.tool_use_id, False,
                              "validation error: " + "; ".join(errors))
        try:
            return ToolResult(call.tool_use_id, True, tool.executor(**validated))
        except Exception as e:
            return ToolResult(call.tool_use_id, False,
                              f"execution error: {type(e).__name__}: {e}")

    def dispatch_many(self, calls: list[ToolCall]) -> list[ToolResult]:
        """并行调度多个工具调用 —— 在单轮对话中处理多个工具请求。"""
        return [self.dispatch(c) for c in calls]


def add(a: int, b: int) -> str:
    return str(a + b)


def multiply(a: int, b: int) -> str:
    return str(a * b)


def classify(status: str) -> str:
    return f"classified as {status}"


def main() -> None:
    print("=" * 70)
    print("TOOL USE and FUNCTION CALLING — Phase 14, Lesson 06")
    print("=" * 70)

    reg = ToolRegistry()
    reg.register(ToolDef(
        name="add",
        description="Add two integers a and b. Use for any integer addition.",
        input_schema={
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
        },
        executor=add,
    ))
    reg.register(ToolDef(
        name="multiply",
        description="Multiply two integers a and b. Prefer multiplication over looped addition.",
        input_schema={
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
        },
        executor=multiply,
    ))
    reg.register(ToolDef(
        name="classify",
        description="Classify a status as one of the allowed labels.",
        input_schema={
            "type": "object",
            "properties": {"status": {"type": "string",
                                       "enum": ["open", "closed", "pending"]}},
            "required": ["status"],
        },
        executor=classify,
    ))

    print("\ncatalog (as presented to the model)")
    for entry in reg.catalog():
        print(f"  - {entry['name']}: {entry['description']}")

    calls = [
        ToolCall("u01", "add", {"a": 2, "b": 3}),
        ToolCall("u02", "multiply", {"a": "4", "b": 5}),
        ToolCall("u03", "classify", {"status": "in_progress"}),
        ToolCall("u04", "classify", {"status": "open"}),
        ToolCall("u05", "subtract", {"a": 1, "b": 2}),
    ]
    print("\nparallel dispatch (5 calls in one turn)")
    for result in reg.dispatch_many(calls):
        tag = "OK " if result.ok else "ERR"
        print(f"  {result.tool_use_id} {tag}: {result.content}")

    print()
    print("observation shape: every validation failure is a structured error")
    print("string the agent can read and retry against. never raise to the loop.")


if __name__ == "__main__":
    main()  # 运行主函数
