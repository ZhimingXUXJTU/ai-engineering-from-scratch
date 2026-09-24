"""课程：Integration Protocols, Identity, and Least Privilege | 集成协议、身份与最小权限
路径：certifications/claude/lessons/25-integration-protocols-identity-and-least-privilege
核心概念：把能力暴露拆成发现、选择、执行三段独立控制——能力注册中心只返回主体
scope 内的窄工具目录；授权门在执行前重查当前 scope 与新鲜审批；审批是绑定动作、
参数、身份与时间的能力对象；授权失败返回结构化的不可重试错误。MCP scope 不等于
业务授权，传输安全也不是授权。
AI 应用对应：真实多服务 Agent 应用的服务端授权层（协议选型 ADR、身份传播、
角色化工具束、绑定已批准动作的短时凭据、不可变审计记录）的最小模型——
发现控制模型看见什么，授权控制实际发生什么，执行时授权才是最终控制。

Integration and least-privilege lab for this lesson's docs/en.md.

Models protocol selection, capability discovery, scope checks, and approvals.
Authorization is evaluated at execution time instead of delegated to a prompt.
Uses only the Python standard library so the control boundary is inspectable.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class IntegrationRequirements:
    dynamic_discovery: bool = False
    local_automation: bool = False
    cross_agent_delegation: bool = False
    direct_service_call: bool = False
    long_running: bool = False


def select_protocol(requirements: IntegrationRequirements) -> str:
    selected = [
        name
        for condition, name in (
            (requirements.dynamic_discovery, "mcp"),
            (requirements.local_automation, "cli"),
            (requirements.cross_agent_delegation, "agent-to-agent"),
            (requirements.direct_service_call, "api"),
        )
        if condition
    ]
    if len(selected) != 1:
        raise ValueError("requirements must identify one primary integration shape")
    protocol = selected[0]
    if requirements.long_running and protocol == "cli":
        return "cli-with-durable-job"
    return protocol


@dataclass(frozen=True)
class Principal:
    principal_id: str
    scopes: frozenset[str]
    approved_actions: frozenset[str] = frozenset()


@dataclass(frozen=True)
class ToolContract:
    name: str
    description: str
    required_scopes: frozenset[str]
    risk: str
    approval_required: bool = False


@dataclass(frozen=True)
class AuthorizationDecision:
    allowed: bool
    reason: str


def authorize(principal: Principal, tool: ToolContract) -> AuthorizationDecision:
    missing = sorted(tool.required_scopes - principal.scopes)
    if missing:
        return AuthorizationDecision(False, f"missing scopes: {', '.join(missing)}")
    if tool.approval_required and tool.name not in principal.approved_actions:
        return AuthorizationDecision(False, "fresh human approval required")
    return AuthorizationDecision(True, "authorized")


def discover_tools(principal: Principal, tools: list[ToolContract]) -> list[ToolContract]:
    return [tool for tool in tools if not (tool.required_scopes - principal.scopes)]


def execute_tool(principal: Principal, tool: ToolContract, arguments: dict[str, object]) -> dict[str, object]:
    decision = authorize(principal, tool)
    if not decision.allowed:
        return {
            "ok": False,
            "error": {"category": "authorization", "retryable": False, "message": decision.reason},
        }
    return {
        "ok": True,
        "tool": tool.name,
        "arguments": arguments,
        "audit": {"principal": principal.principal_id, "risk": tool.risk},
    }


def demo() -> dict[str, object]:
    tools = [
        ToolContract("read_ticket", "Read one assigned support ticket", frozenset({"tickets:read"}), "low"),
        ToolContract("draft_reply", "Create a draft without sending it", frozenset({"tickets:read", "drafts:write"}), "low"),
        ToolContract("issue_refund", "Issue an approved refund", frozenset({"refunds:write"}), "high", True),
    ]
    principal = Principal("support-agent-42", frozenset({"tickets:read", "drafts:write"}))
    visible = discover_tools(principal, tools)
    attempt = execute_tool(principal, tools[2], {"amount": 75})
    return {
        "protocol": select_protocol(IntegrationRequirements(dynamic_discovery=True)),
        "visible_tools": [tool.name for tool in visible],
        "refund_attempt": attempt,
        "principal": asdict(principal) | {"scopes": sorted(principal.scopes), "approved_actions": sorted(principal.approved_actions)},
    }


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2))

