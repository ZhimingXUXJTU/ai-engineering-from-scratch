"""Phase 13 Lesson 14: MCP Apps on the MCP 2026-07-28 wire.
Lesson: phases/13-tools-and-protocols/14-mcp-apps/docs/en.md
Spec: https://modelcontextprotocol.io/specification/2026-07-28
Models discovery, tools, resources, and a self-contained MCP Apps UI.
Lesson 09 owns the HTTP adapter; the UI pins its postMessage origin.

无状态协议上的 MCP Apps (MCP Apps on the Stateless Protocol)
核心概念：
  - 扩展标识 io.modelcontextprotocol/ui：客户端在每请求 _meta 能力里声明，服务器在
    server/discover 能力里声明；tools/list 只在客户端声明扩展时才带 _meta.ui.resourceUri
  - UI 绑定在工具定义（调用前元数据），工具调用本身只返回 content + structuredContent
  - resources/read 提供 text/html;profile=mcp-app 资源，头部与主体不匹配返回 -32020，
    缺少 Apps 能力返回 -32021，版本不受支持返回 -32022
  - CSP 域名列表（connectDomains/resourceDomains/frameDomains/baseUriDomains）默认全空，
    按需加白；加载权与上传权分离
  - Apps 桥接：postMessage 上的 JSON-RPC 方言，ui/initialize 握手 + ui/notifications/initialized
    就绪通知；postMessage 钉死精确对端源（hostOrigin），拒绝其他任何源
AI 应用对应：MCP Apps 是 MCP 从文本工具走向应用平台的扩展，支持仪表盘、表单、地图等
  交互场景；无会话核心让它可以随宿主任意水平扩展。
"""

from __future__ import annotations

import html
import json
from dataclasses import dataclass
from typing import Any


PROTOCOL_VERSION = "2026-07-28"
APPS_EXTENSION = "io.modelcontextprotocol/ui"
PROTOCOL_META = "io.modelcontextprotocol/protocolVersion"
CLIENT_CAPABILITIES_META = "io.modelcontextprotocol/clientCapabilities"
CLIENT_INFO_META = "io.modelcontextprotocol/clientInfo"
SERVER_INFO_META = "io.modelcontextprotocol/serverInfo"
SERVER_INFO = {"name": "timeline-app-server", "version": "2.0.0"}
RESOURCE_URI = "ui://notes/timeline.html"
RESOURCE_MIME = "text/html;profile=mcp-app"
HOST_ORIGIN = "https://host.example"

# 示例笔记数据，用于生成时间线（工具调用经 structuredContent 返回同一份数据）
NOTES = [
    {"id": "note-1", "title": "Discover", "created": "2026-07-28"},
    {"id": "note-2", "title": "Per-request metadata", "created": "2026-07-29"},
    {"id": "note-3", "title": "MCP Apps", "created": "2026-07-30"},
]

# CSP 域名列表默认全空（最小权限）：connectDomains 管上传/fetch，resourceDomains 管加载
APP_CSP = {
    "connectDomains": [],
    "resourceDomains": [],
    "frameDomains": [],
    "baseUriDomains": [],
}


@dataclass(frozen=True)
class ProtocolError(Exception):
    code: int
    message: str
    data: dict[str, Any] | None = None


def request_meta(*, apps: bool = True) -> dict[str, Any]:
    extensions = {APPS_EXTENSION: {}} if apps else {}
    return {
        PROTOCOL_META: PROTOCOL_VERSION,
        CLIENT_CAPABILITIES_META: {"extensions": extensions},
        CLIENT_INFO_META: {"name": "lesson-client", "version": "1.0.0"},
    }


def make_request(
    method: str,
    request_id: int,
    params: dict[str, Any] | None = None,
    *,
    apps: bool = True,
) -> tuple[dict[str, Any], dict[str, str]]:
    body_params = dict(params or {})
    body_params["_meta"] = request_meta(apps=apps)
    body = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": body_params}
    headers = {"MCP-Protocol-Version": PROTOCOL_VERSION, "Mcp-Method": method}
    if method in {"tools/call", "resources/read", "prompts/get"}:
        headers["Mcp-Name"] = str(body_params.get("name") or body_params.get("uri") or "")
    return body, headers


# 生成自包含的 HTML 时间线：SVG 风格列表 + 内联 JS；桥接消息全部钉死 hostOrigin 源
def timeline_html(notes: list[dict[str, str]]) -> str:
    items = "".join(
        "<li><button data-note='{}'>{}</button><time>{}</time></li>".format(
            html.escape(note["id"]),
            html.escape(note["title"]),
            html.escape(note["created"]),
        )
        for note in notes
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Notes timeline</title>
<style>body{{font:16px system-ui;margin:1rem}}li{{display:flex;gap:1rem;margin:.5rem}}</style>
</head><body><h1>Notes timeline</h1><ol>{items}</ol>
<script>
const hostOrigin = {json.dumps(HOST_ORIGIN)};
let nextId = 0;
function callTool(name, args) {{
  const id = ++nextId;
  window.parent.postMessage({{
    jsonrpc: "2.0", id, method: "tools/call",
    params: {{name, arguments: args}}
  }}, hostOrigin);
}}
window.addEventListener("message", (event) => {{
  if (event.origin !== hostOrigin || !event.data || event.data.jsonrpc !== "2.0") return;
  if (event.data.id === 0 && event.data.result) {{
    document.body.dataset.bridgeReady = "true";
    window.parent.postMessage({{
      jsonrpc: "2.0", method: "ui/notifications/initialized"
    }}, hostOrigin);
  }}
}});
document.querySelectorAll("button").forEach((button) => {{
  button.addEventListener("click", () => callTool("notes_open", {{id: button.dataset.note}}));
}});
// ui/initialize belongs to the Apps postMessage dialect, not MCP core initialization.
window.parent.postMessage({{
  jsonrpc: "2.0", id: 0, method: "ui/initialize",
  params: {{
    appInfo: {{name: "notes-timeline", version: "1.0.0"}},
    appCapabilities: {{}}
  }}
}}, hostOrigin);
</script></body></html>"""


# 进程内协议模型：校验请求信封与路由头，分发 server/discover、tools、resources 方法
class McpAppServer:
    def _validate(self, body: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
        if body.get("jsonrpc") != "2.0":
            raise ProtocolError(-32600, "Invalid Request")
        method = body.get("method")
        params = body.get("params")
        if not isinstance(method, str) or not isinstance(params, dict):
            raise ProtocolError(-32600, "Invalid Request")
        meta = params.get("_meta")
        if not isinstance(meta, dict):
            raise ProtocolError(-32602, "request params._meta is required")
        requested_version = meta.get(PROTOCOL_META)
        if not isinstance(requested_version, str):
            raise ProtocolError(-32602, "protocolVersion must be a string")
        if not isinstance(meta.get(CLIENT_CAPABILITIES_META), dict):
            raise ProtocolError(-32602, "clientCapabilities is required on every request")
        if headers.get("MCP-Protocol-Version") != requested_version:
            raise ProtocolError(-32020, "MCP-Protocol-Version header does not match body")
        if headers.get("Mcp-Method") != method:
            raise ProtocolError(-32020, "Mcp-Method header does not match body")
        expected_name = params.get("name") or params.get("uri")
        if method in {"tools/call", "resources/read", "prompts/get"}:
            if headers.get("Mcp-Name") != expected_name:
                raise ProtocolError(-32020, "Mcp-Name header does not match body")
        if requested_version != PROTOCOL_VERSION:
            raise ProtocolError(
                -32022,
                "Unsupported protocol version",
                {"supported": [PROTOCOL_VERSION], "requested": requested_version},
            )
        return meta

    @staticmethod
    def _apps_enabled(meta: dict[str, Any]) -> bool:
        caps = meta[CLIENT_CAPABILITIES_META]
        extensions = caps.get("extensions", {})
        return (
            isinstance(extensions, dict)
            and isinstance(extensions.get(APPS_EXTENSION), dict)
        )

    @staticmethod
    def _success(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
        result = dict(result)
        result.setdefault("resultType", "complete")
        result.setdefault("_meta", {})[SERVER_INFO_META] = SERVER_INFO
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    @staticmethod
    def _error(request_id: Any, error: ProtocolError) -> dict[str, Any]:
        payload: dict[str, Any] = {"code": error.code, "message": error.message}
        if error.data is not None:
            payload["data"] = error.data
        return {"jsonrpc": "2.0", "id": request_id, "error": payload}

    @staticmethod
    def _error_status(error: ProtocolError) -> int:
        return 404 if error.code == -32601 else 400

    def handle(
        self,
        body: dict[str, Any],
        headers: dict[str, str],
        *,
        http_method: str = "POST",
    ) -> tuple[int, dict[str, Any] | None]:
        if http_method != "POST":
            return 405, None
        is_notification = "id" not in body
        try:
            meta = self._validate(body, headers)
            method = body["method"]
            params = body["params"]
            if method == "server/discover":
                result = {
                    "supportedVersions": [PROTOCOL_VERSION],
                    "capabilities": {
                        "tools": {},
                        "resources": {},
                        "extensions": {APPS_EXTENSION: {}},
                    },
                    "ttlMs": 300_000,
                    "cacheScope": "public",
                }
            elif method == "tools/list":
                tool: dict[str, Any] = {
                    "name": "notes_timeline",
                    "description": "Render a timeline of notes.",
                    "inputSchema": {"type": "object", "properties": {}},
                }
                if self._apps_enabled(meta):
                    tool["_meta"] = {"ui": {"resourceUri": RESOURCE_URI}}
                result = {"tools": [tool], "ttlMs": 60_000, "cacheScope": "public"}
            elif method == "tools/call":
                if params.get("name") != "notes_timeline":
                    raise ProtocolError(-32602, "Unknown tool")
                result = {
                    "content": [{"type": "text", "text": "Timeline ready."}],
                    "structuredContent": {"notes": NOTES},
                    "isError": False,
                }
            elif method == "resources/list":
                result = {
                    "resources": [{
                        "uri": RESOURCE_URI,
                        "name": "notes-timeline",
                        "description": "Interactive notes timeline for MCP Apps hosts.",
                        "mimeType": RESOURCE_MIME,
                    }],
                    "ttlMs": 60_000,
                    "cacheScope": "public",
                }
            elif method == "resources/read":
                if params.get("uri") != RESOURCE_URI:
                    raise ProtocolError(-32602, "Unknown resource URI")
                if not self._apps_enabled(meta):
                    raise ProtocolError(
                        -32021,
                        "MCP Apps client capability is required",
                        {
                            "requiredCapabilities": {
                                "extensions": {APPS_EXTENSION: {}}
                            }
                        },
                    )
                result = {
                    "contents": [{
                        "uri": RESOURCE_URI,
                        "mimeType": RESOURCE_MIME,
                        "text": timeline_html(NOTES),
                        "_meta": {"ui": {"csp": APP_CSP, "permissions": {}}},
                    }],
                    "ttlMs": 60_000,
                    "cacheScope": "public",
                }
            else:
                raise ProtocolError(-32601, "Method not found")
            if is_notification:
                return 202, None
            return 200, self._success(body["id"], result)
        except ProtocolError as error:
            if is_notification:
                return self._error_status(error), None
            return self._error_status(error), self._error(body.get("id"), error)


# 演示：发现 → 工具列表（含 UI 绑定）→ 工具调用 → 读取 ui:// 资源
def demo() -> None:
    server = McpAppServer()
    for request_id, (method, params) in enumerate(
        [
            ("server/discover", {}),
            ("tools/list", {}),
            ("tools/call", {"name": "notes_timeline", "arguments": {}}),
            ("resources/read", {"uri": RESOURCE_URI}),
        ],
        start=1,
    ):
        body, headers = make_request(method, request_id, params)
        status, response = server.handle(body, headers)
        summary = response.get("result", response.get("error"))
        print(f"{status} {method}: {json.dumps(summary)[:220]}")


if __name__ == "__main__":
    demo()
