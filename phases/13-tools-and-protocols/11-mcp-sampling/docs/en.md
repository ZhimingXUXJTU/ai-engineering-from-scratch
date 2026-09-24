# MCP Model Input: Sampling Migration and Stateless MRTR | MCP 模型输入：Sampling 迁移与无状态 MRTR

> MCP 2026-07-28 deprecates Sampling for new designs and removes the server-to-client request channel. If an existing workflow still needs the client's model, the server returns an `input_required` result and the client retries the original request with the model output. The reasoning loop becomes explicit, bounded, and stateless at the protocol layer.

> **【中文解读】** MCP 2026-07-28 为新设计弃用了 Sampling（采样），并移除了"服务器向客户端发请求"的通道。如果既有工作流仍需要客户端的模型，服务器返回一个 `input_required` 结果，客户端带着模型输出重试原始请求。推理循环因此变得显式、有界、且在协议层无状态。本课教你两条路：新服务器直连模型提供商；存量 Sampling 工作流迁移到 MRTR（Multi Round-Trip Request，多轮往返请求）。

> **【拓展：Sampling→MRTR 的方向反转】** 旧版 Sampling 是协议里唯一的"反向通道"：服务器在处理请求时反过来调用客户端的 LLM——这正是它被移除的原因，反向通道让服务器逻辑依赖连接存活、难以无状态部署。MRTR 把"反向调用"改写成"结果 + 重试"：服务器把要做的事装进 `inputRequests` 返回，客户端拿到模型输出后用新 id 重新发起同一方法。方向反转与 Lesson 09 的传输层无状态化、Lesson 10 的 `subscriptions/listen` 是同一场架构演进。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13·07（MCP server）——tools/call 的分发与校验；(2) Phase 13·10（resources and prompts）——`_meta` 保留键、`server/discover`、`resultType` 判别符；(3) HMAC / 认证加密的基本概念——`requestState` 的完整性保护要用；(4) 若学过旧版（服务器直接发 `sampling/createMessage` 请求），请把那套"反向请求"心智模型换成"结果 + 重试"。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 10 (resources and prompts) | **前置知识:** Phase 13 · 07（MCP 服务器）、Phase 13 · 10（资源与提示）
**Time:** ~75 minutes | **时间:** 约 75 分钟

## Learning Objectives | 学习目标

- Explain why Sampling is deprecated in MCP 2026-07-28 and choose the direct model integration default for new servers.
  中文翻译：解释 Sampling 在 MCP 2026-07-28 中被弃用的原因，并为新服务器选择直连模型集成的默认路径。
- Implement a compatibility workflow that carries `sampling/createMessage` through Multi Round-Trip Requests (MRTR).
  中文翻译：实现通过多轮往返请求（MRTR）承载 `sampling/createMessage` 的兼容工作流。
- Put the protocol revision and client capabilities in every request `_meta` object.
  中文翻译：把协议修订版和客户端能力放进每个请求的 `_meta` 对象。
- Return `resultType: "input_required"` and retry the original method with a fresh JSON-RPC id.
  中文翻译：返回 `resultType: "input_required"`，并用全新的 JSON-RPC id 重试原始方法。
- Integrity-protect `requestState` and bind it to the principal, method, arguments, and expiry.
  中文翻译：对 `requestState` 做完整性保护，并把它绑定到主体、方法、参数和过期时间。
- Bound model-assisted loops with capability checks, approval, response validation, and a round limit.
  中文翻译：用能力检查、审批、响应校验和轮数上限给模型辅助循环设界。

## The Decision Before the Protocol | 协议之前的决策

> **【中文解读】** 先做架构决策，再谈协议。像 `summarize_repo` 这样的工具包含两类工作：确定性工作（列文件、读允许的文件、校验路径、拼装内容）和模型工作（挑代表性文件、综合摘要）。两条合法架构：(1) 新服务器——直连模型提供商，服务器自持模型选择、凭证、预算、重试和可观测性，对 MCP 客户端只返回一个普通的 `tools/call` 结果；(2) 存量 Sampling 工作流——迁移到 MRTR 兼容路径，仅当"用客户端的模型和凭证"是真实产品需求时才选它，且要记录移除计划。

A tool such as `summarize_repo` needs two kinds of work:

1. Deterministic work: list files, read allowed files, validate paths, and assemble content.
  中文翻译：确定性工作：列出文件、读取允许的文件、校验路径、拼装内容。
2. Model work: choose representative files and synthesize the summary.
  中文翻译：模型工作：选择代表性文件并综合出摘要。

You now have two valid architectures.

> 你现在有两条合法的架构。

### New server: integrate with a model provider directly

This is the current default. The server owns model selection, credentials, budgets, retries, and observability. It returns one ordinary `tools/call` result to the MCP client.

> 这是当前的默认。服务器自持模型选择、凭证、预算、重试和可观测性。它对 MCP 客户端返回一个普通的 `tools/call` 结果。

Choose this when the server is already a hosted service or when predictable model behavior matters more than using the host's model.

> 当服务器已经是托管服务，或当可预期的模型行为比"用宿主的模型"更重要时，选这条路径。

### Existing Sampling workflow: migrate it to MRTR

Sampling still exists during its deprecation window. A server targeting 2026-07-28 cannot send a live `sampling/createMessage` request back to the client. It instead embeds that request in an `InputRequiredResult`.

> Sampling 在弃用窗口期内仍然存在。面向 2026-07-28 的服务器不能向客户端发送活的 `sampling/createMessage` 请求。它改为把该请求嵌入一个 `InputRequiredResult`。

Choose this compatibility path only when using the client's model and credentials is a real product requirement. Record a removal plan because new implementations should not adopt deprecated Sampling.

> 仅当"使用客户端的模型和凭证"是真实的产品需求时才选这条兼容路径。记录一份移除计划，因为新实现不应采用已弃用的 Sampling。

## The Stateless Contract | 无状态契约

> **【中文解读】** 2026 年 7 月的协议没有 `initialize` 交换、没有 `notifications/initialized`、没有 `Mcp-Session-Id`——原本活在握手里的信息现在随每个请求传输。服务器在每个请求上校验修订版：版本缺失或非字符串 → `-32602`；不支持的字符串 → `-32022`（带精确 supported/requested 数据）；缺 Sampling 能力 → `-32021`（带 `data.requiredCapabilities`）。无 `id` 的信封是通知：可处理但不发成功或错误响应，Streamable HTTP 适配器对被接受的通知返回无主体的 `202`。每个成功的现代结果都带判别符：`complete`（完成）、`input_required`（客户端须履行嵌入请求并重试），扩展可定义更多（Tasks 扩展在 Lesson 13 加 `"task"`）。

The July 2026 protocol has no `initialize` exchange, no `notifications/initialized`, and no `Mcp-Session-Id`. Every request carries the information that used to live in the handshake:

> 2026 年 7 月的协议没有 `initialize` 交换、没有 `notifications/initialized`、也没有 `Mcp-Session-Id`。每个请求都携带原本活在握手里的信息：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "summarize_repo",
    "arguments": {"audience": "developer"},
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {"sampling": {}},
      "io.modelcontextprotocol/clientInfo": {
        "name": "lesson-client",
        "version": "1.0.0"
      }
    }
  }
}
```

The server validates the revision on every request. A missing or non-string version is invalid params, `-32602`. An unsupported string returns `-32022` with exact data `{"supported":["2026-07-28"],"requested":"<client version>"}`. A missing Sampling capability returns `-32021` with `data.requiredCapabilities` set to `{"sampling":{}}`.

> 服务器在每个请求上校验修订版。缺失或非字符串的版本是无效参数 `-32602`。不支持的字符串返回 `-32022` 并带精确数据 `{"supported":["2026-07-28"],"requested":"<client version>"}`。缺失 Sampling 能力返回 `-32021`，`data.requiredCapabilities` 设为 `{"sampling":{}}`。

An envelope without a JSON-RPC `id` is a notification. The receiver may process it, but it emits neither a success response nor an error response. A Streamable HTTP adapter returns `202 Accepted` with no body for an accepted notification.

> 不带 JSON-RPC `id` 的信封是通知。接收方可以处理它，但既不发出成功响应也不发出错误响应。Streamable HTTP 适配器对被接受的通知返回不带主体的 `202 Accepted`。

The server also implements `server/discover` with the exact `supportedVersions` key, capabilities, `ttlMs`, and `cacheScope` so a client can learn and cache the server contract before calling a tool. Because discovery advertises `tools`, the server also implements mandatory `tools/list`. Its deterministic `summarize_repo` descriptor includes a valid object `inputSchema`, `resultType: "complete"`, server identity metadata, and public cache hints.

> 服务器还实现 `server/discover`，带精确的 `supportedVersions` 键、能力、`ttlMs` 和 `cacheScope`，让客户端能在调用工具之前学习并缓存服务器契约。因为发现公告了 `tools`，服务器还要实现强制的 `tools/list`。其确定性的 `summarize_repo` 描述符包含合法的对象 `inputSchema`、`resultType: "complete"`、服务器身份元数据和公共缓存提示。

Every successful modern result has a discriminator:

- `resultType: "complete"` means the operation finished.
  中文翻译：`resultType: "complete"` 表示操作已完成。
- `resultType: "input_required"` means the client must fulfill embedded requests and retry.
  中文翻译：`resultType: "input_required"` 表示客户端必须履行嵌入的请求并重试。
- Extensions may define additional result types. The Tasks extension adds `"task"` in Lesson 13.
  中文翻译：扩展可以定义更多结果类型。Tasks 扩展在 Lesson 13 中加入 `"task"`。

## One MRTR Round | 一轮 MRTR

> **【中文解读】** 服务器在处理请求时不能回调客户端，于是返回 `input_required` 结果：`inputRequests` 是服务器命名的映射，装着嵌入的 `sampling/createMessage` 请求；`requestState` 是不透明的完整性保护值。客户端验证自己支持 Sampling、应用审批与模型策略、拿到模型响应后，用不同的 JSON-RPC id 发送新请求：重复原始方法和参数、加上本轮的 `inputResponses`（按 `inputRequests` 的键组织）、逐字节回显 `requestState`。重试不是协议会话的延续，是新的独立请求。MRTR 只允许出现在 `tools/call`、`prompts/get`、`resources/read` 上。

> 💡 **【类比】** MRTR 像政务大厅的"一次性告知单"。旧 Sampling 像"工作人员直接替你打电话问上级"（服务器反向调用客户端）——上级下班（连接断开）事就办不完。MRTR 改成：工作人员给你一张告知单（`inputRequests`：你要去盖章的材料清单）和一张回执（`requestState`：证明你已排队到这一步），你去把章盖好（客户端模型补全），再取一个新号（新 JSON-RPC id）回来续办。窗口谁当班都能凭回执接着办（无状态、任意副本可处理），回执盖章防伪（HMAC 完整性保护），且只能办你自己的事（绑定主体和参数摘要）。

The server cannot call the client while handling the request. It returns this result instead:

> 服务器在处理请求时无法调用客户端。它改为返回这个结果：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "input_required",
    "inputRequests": {
      "pick_files": {
        "method": "sampling/createMessage",
        "params": {
          "messages": [
            {
              "role": "user",
              "content": {
                "type": "text",
                "text": "Choose three representative files and return a JSON array."
              }
            }
          ],
          "systemPrompt": "Return only the requested value.",
          "modelPreferences": {
            "costPriority": 0.8,
            "intelligencePriority": 0.2
          },
          "maxTokens": 400
        }
      }
    },
    "requestState": "opaque-integrity-protected-value"
  }
}
```

The client verifies that it supports Sampling, applies its approval and model policies, and obtains a model response. Then it sends a new request with a different JSON-RPC id:

> 客户端验证自己支持 Sampling、应用它的审批和模型策略，并取得模型响应。然后它用不同的 JSON-RPC id 发送新请求：

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "summarize_repo",
    "arguments": {"audience": "developer"},
    "inputResponses": {
      "pick_files": {
        "role": "assistant",
        "content": {
          "type": "text",
          "text": "[\"README.md\", \"server.py\", \"docs/intro.md\"]"
        },
        "model": "host-model",
        "stopReason": "endTurn"
      }
    },
    "requestState": "opaque-integrity-protected-value",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {"sampling": {}}
    }
  }
}
```

The retry is not a continuation of a protocol session. It is a new request that repeats the original method and arguments, adds only the current round's `inputResponses`, and echoes `requestState` byte for byte.

> 重试不是协议会话的延续。它是一个新请求：重复原始方法和参数、只添加当前轮次的 `inputResponses`，并逐字节回显 `requestState`。

MRTR is allowed only on `tools/call`, `prompts/get`, and `resources/read`. A server must not return `input_required` from unrelated methods.

> MRTR 只允许用于 `tools/call`、`prompts/get` 和 `resources/read`。服务器不得从无关方法返回 `input_required`。

## Multi-Round State | 多轮状态

> **【中文解读】** 多轮工作流（先挑文件、再总结）里，服务器把阶段和已校验的中间数据放进下一个 `requestState`。把这个值当作攻击者可控来对待：只签名一个裸的阶段名不够。绑定五样东西：已认证主体（不是自报的 `clientInfo`）、发起方法、原始参数的摘要、短过期时间、当前阶段和已校验的中间值。不需要机密性用 HMAC；客户端不能读该状态就用认证加密。坏签名、过期、主体变更、参数变更都用 `-32602` 拒绝。客户端不得解析或修改 `requestState`，它唯一的职责是逐字节回显。

This lesson needs two model calls:

1. `pick_files` returns a JSON array.
  中文翻译：`pick_files` 返回一个 JSON 数组。
2. `summary` returns the final prose.
  中文翻译：`summary` 返回最终的散文摘要。

Each retry carries only the responses for that round. The server therefore puts the phase and validated intermediate data into the next `requestState`.

> 每次重试只携带该轮的响应。因此服务器把阶段和已校验的中间数据放进下一个 `requestState`。

Treat that value as attacker-controlled. Signing a raw phase name is not enough. Bind the state to:

> 把这个值当作攻击者可控的来对待。只签名一个裸的阶段名是不够的。把状态绑定到：

- the authenticated principal, not self-reported `clientInfo`;
  中文翻译：已认证主体，而不是自报的 `clientInfo`；
- the originating method;
  中文翻译：发起方法；
- a digest of the original arguments;
  中文翻译：原始参数的摘要；
- a short expiry;
  中文翻译：较短的过期时间；
- the current phase and validated intermediate values.
  中文翻译：当前阶段和已校验的中间值。

Use HMAC when confidentiality is not required. Use authenticated encryption when the client must not read the state. Reject a bad signature, expired value, changed principal, or changed arguments with `-32602`.

> 不需要机密性时用 HMAC。客户端不得读取状态时用认证加密。坏签名、过期值、变更的主体或变更的参数都用 `-32602` 拒绝。

The client must not parse or modify `requestState`. Its only job is to echo the exact string on the retry.

> 客户端不得解析或修改 `requestState`。它唯一的工作是在重试时回显那个精确的字符串。

> ⚠️ **【易错点】** 场景：`requestState` 只编码阶段名不做绑定校验，或客户端图省事解析/篡改它 / 后果：攻击者伪造状态跳到任意阶段、跨请求重放旧状态、换参数续跑别人开了头的工作流；篡改后服务器行为不可预期 / 修复：HMAC 或认证加密 + 五重绑定（主体/方法/参数摘要/过期/阶段与中间值），任何校验失败一律 `-32602`；客户端侧只做逐字节回显。

## Model Preferences Are Hints | 模型偏好只是提示

> **【中文解读】** `costPriority`、`speedPriority`、`intelligencePriority` 是三个独立偏好，不是概率分布、不必求和为一；客户端可以忽略它们，因为模型策略归客户端所有。维护遗留 Sampling 流程时把 `includeContext` 保持为 `"none"`——其他上下文模式增加泄漏风险且本身已弃用；在请求里只传最少显式上下文。

`costPriority`, `speedPriority`, and `intelligencePriority` are independent preferences. They are not a probability distribution and do not need to sum to one. The client may ignore them because the client owns model policy.

> `costPriority`、`speedPriority`、`intelligencePriority` 是独立的偏好。它们不是概率分布，也不需要求和为一。客户端可以忽略它们，因为模型策略归客户端所有。

Keep `includeContext` at `"none"` if you maintain a legacy Sampling flow. Other context modes increase leakage risk and are themselves deprecated. Pass the minimum explicit context in the request.

> 如果你维护遗留 Sampling 流程，把 `includeContext` 保持为 `"none"`。其他上下文模式会增加泄漏风险且本身已弃用。在请求中传递最少的显式上下文。

## Safety Invariants | 安全不变量

> **【中文解读】** 客户端是嵌入 Sampling 请求的信任边界。七条不变量：策略要求时向用户展示服务器想让模型做什么；给 MRTR 轮数设上限（恶意服务器否则可制造模型花费循环）；每个采样响应用作文件名、URL 或工具输入前先校验；限制每轮字节数和 token 数；拒绝未在当前客户端能力中声明的输入请求；模型输出不得参与授权决策；记录发起方法和输入请求键但不记敏感提示内容。`clientInfo` 和 `serverInfo` 是展示与诊断元数据，绝不能当认证身份。

The client is the trust boundary for embedded Sampling requests.

> 客户端是嵌入 Sampling 请求的信任边界。

- Show the user what the server is asking the model to do when policy requires approval.
  中文翻译：策略要求审批时，向用户展示服务器正在让模型做什么。
- Cap MRTR rounds. A malicious server can otherwise create a model-spend loop.
  中文翻译：给 MRTR 轮数设上限。否则恶意服务器可以制造模型花费循环。
- Validate every sampling response before using it as a filename, URL, or tool input.
  中文翻译：每个采样响应在被用作文件名、URL 或工具输入之前都要校验。
- Limit bytes and tokens per round.
  中文翻译：限制每轮的字节数和 token 数。
- Refuse an input request that was not declared in current client capabilities.
  中文翻译：拒绝未在当前客户端能力中声明的输入请求。
- Keep model output out of authorization decisions.
  中文翻译：模型输出不得参与授权决策。
- Log the originating method and input-request key without logging sensitive prompt content.
  中文翻译：记录发起方法和输入请求键，但不记录敏感的提示内容。

`clientInfo` and `serverInfo` are display and diagnostics metadata. Never use either as an authenticated identity.

> `clientInfo` 和 `serverInfo` 是展示和诊断元数据。绝不要把任何一个当作已认证身份。

```figure
t3-sampling-flip
```

## Build It | 动手实现

> **【中文解读】** 示例用纯标准库跑通完整两轮流程：发现返回版本与缓存提示；工具发现返回确定性描述符；每次调用校验请求元数据；第一个结果嵌入选文件的采样请求；第一次重试验证模型结果并嵌入第二个请求；HMAC 保护的 `requestState` 在独立请求之间携带阶段；最终结果 `complete`。假宿主模型保证示例确定性——接真宿主时只替换 `fake_host_model`，服务器侧状态机应保持确定、可测。

`code/main.py` implements the full two-round flow with no third-party package:

- `server/discover` returns `supportedVersions`, advertises tool support, and returns cache hints.
  中文翻译：`server/discover` 返回 `supportedVersions`、公告工具支持并返回缓存提示。
- `tools/list` returns a deterministic, cacheable `summarize_repo` descriptor with an object input schema.
  中文翻译：`tools/list` 返回带对象输入 schema 的确定性、可缓存 `summarize_repo` 描述符。
- `tools/call` validates per-request metadata.
  中文翻译：`tools/call` 校验逐请求元数据。
- The first result embeds `sampling/createMessage` for file selection.
  中文翻译：第一个结果嵌入用于选文件的 `sampling/createMessage`。
- The first retry validates the model result and embeds a second request.
  中文翻译：第一次重试验证模型结果并嵌入第二个请求。
- HMAC-protected `requestState` carries the phase between independent requests.
  中文翻译：HMAC 保护的 `requestState` 在独立请求之间携带阶段。
- The final result uses `resultType: "complete"`.
  中文翻译：最终结果使用 `resultType: "complete"`。

The fake host model makes the example deterministic. Replace only `fake_host_model` when connecting a real host. The server-side state machine should stay deterministic and testable.

> 假宿主模型让示例保持确定性。接入真实宿主时只替换 `fake_host_model`。服务器侧状态机应保持确定和可测试。

## Use It | 用框架实现

From the repository root:

```bash
cd phases/13-tools-and-protocols/11-mcp-sampling/code
python3 main.py
python3 -m unittest discover tests -v
```

Expected checkpoints:

- Discovery returns a complete result with `ttlMs` and `cacheScope`.
  中文翻译：发现返回带 `ttlMs` 和 `cacheScope` 的完整结果。
- Tool discovery returns the same sorted descriptor with `resultType`, server identity, and cache hints.
  中文翻译：工具发现返回相同排序的描述符，带 `resultType`、服务器身份和缓存提示。
- Missing capabilities and unsupported versions use exact `-32021` and `-32022` error data.
  中文翻译：能力缺失和不支持的版本使用精确的 `-32021` 和 `-32022` 错误数据。
- An id-less notification produces no JSON-RPC response.
  中文翻译：无 id 的通知不产生 JSON-RPC 响应。
- Request ids are `[1, 2, 3]`, proving each MRTR round is independent.
  中文翻译：请求 id 是 `[1, 2, 3]`，证明每个 MRTR 轮次相互独立。
- The first two results are `input_required`.
  中文翻译：前两个结果是 `input_required`。
- The final result is `complete` and contains the selected files plus summary.
  中文翻译：最终结果是 `complete`，包含选出的文件和摘要。
- Changing the original arguments on a retry fails the request-state check.
  中文翻译：重试时改变原始参数会未通过请求状态检查。

## Ship It | 产出物

`outputs/skill-sampling-loop-designer.md` is now a migration planner. It first decides whether Sampling should be removed in favor of direct model integration. If compatibility is required, it produces the MRTR rounds, state binding, capability gate, budget, validation, and removal plan.

> `outputs/skill-sampling-loop-designer.md` 现在是一份迁移规划器。它先决定是否应该移除 Sampling、改用直连模型集成。如果需要兼容，它产出 MRTR 轮次、状态绑定、能力门、预算、校验和移除计划。

## Exercises | 练习题

1. Change the file-selection response to invalid JSON. Confirm the server returns `-32602` instead of trusting model output.
   中文翻译：把文件选择响应改成非法 JSON。确认服务器返回 `-32602` 而不是信任模型输出。
2. Change `audience` between the first call and retry. Explain why the sealed state blocks cross-request reuse.
   中文翻译：在首次调用和重试之间改变 `audience`。解释为什么密封状态能阻断跨请求复用。
3. Add a third round that asks the host to critique the summary. Carry the earlier summary inside signed state and cap the entire flow at three rounds.
   中文翻译：添加请宿主评审摘要的第三轮。把较早的摘要放进签名状态里携带，并把整个流程限制在三轮。
4. Remove Sampling by replacing the fake host callback with a server-owned model adapter. List which approval, billing, and observability responsibilities move to the server.
   中文翻译：用服务器自有的模型适配器替换假宿主回调以移除 Sampling。列出哪些审批、计费和可观测性职责转移到服务器。
5. Add an expiry test using a state value that is one second past its deadline.
   中文翻译：用一个超过截止时间一秒的状态值添加过期测试。

## Key Terms | 术语速查表

| Term | Meaning in 2026-07-28 | 中文术语 |
|------|------------------------|----------|
| Sampling | Deprecated feature that asks the client's model for a completion | 采样（已弃用） |
| MRTR | Stateless retry pattern for client input required during a request | 多轮往返请求 |
| `InputRequiredResult` | Result with `resultType: "input_required"` | 需输入结果 |
| `inputRequests` | Server-assigned map of embedded elicitation, sampling, or roots requests | 嵌入请求映射 |
| `inputResponses` | Current round's client results keyed like `inputRequests` | 本轮输入响应 |
| `requestState` | Opaque server state echoed exactly by the client and verified by the server | 请求状态（不透明） |
| `resultType` | Required discriminator for modern MCP results | 结果类型判别符 |
| Direct model integration | Recommended replacement for new servers that need model inference | 直连模型集成 |
| Capability gate | Rule that prevents sending an embedded request the client did not advertise | 能力门 |
| Loop budget | Maximum rounds, tokens, bytes, time, and spend allowed for the operation | 循环预算 |

## Legacy Compatibility | 遗留兼容

> **【中文解读】** 钉在 2025-11-25 的客户端仍可在活连接上用旧的服务器发起式 `sampling/createMessage` 流程。把那种行为只放进按版本隔离的适配器，绝不要把有会话路径当作 2026-07-28 服务器的架构。官方 SDK 可以为老对端翻译现代 `input_required` 处理器——那个垫片是兼容边界，不是添加新的依赖会话逻辑的许可。

A client pinned to 2025-11-25 may still use the older server-initiated `sampling/createMessage` flow over a live connection. Keep that behavior in a version-specific adapter only. Do not make the sessionful path the architecture for a 2026-07-28 server.

> 钉在 2025-11-25 的客户端仍可在活连接上使用较旧的服务器发起式 `sampling/createMessage` 流程。那种行为只保留在按版本隔离的适配器里。不要让有会话的路径成为 2026-07-28 服务器的架构。

Official SDKs can translate modern `input_required` handlers for older peers. That shim is a compatibility boundary, not permission to add new session-dependent logic.

> 官方 SDK 可以为较旧的对端翻译现代 `input_required` 处理器。那个垫片是兼容边界，不是添加新的依赖会话逻辑的许可。

## Further Reading | 延伸阅读

- [MCP 2026-07-28 Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
  中文翻译：MRTR 模式的权威规范
- [MCP 2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
  中文翻译：2026-07-28 修订的完整变更清单
- [MCP Sampling deprecation](https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging)
  中文翻译：Sampling 弃用的 SEP 提案原文
- [MCP 2026-07-28 server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  中文翻译：`server/discover` 发现契约规范
