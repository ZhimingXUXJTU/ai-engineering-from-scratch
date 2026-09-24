# MCP Tool Contracts and Content | MCP 工具契约与内容

> A tool is safe to automate only when discovery, arguments, results, pagination, and transport metadata agree on one contract.

> **【中文解读】** 一个工具只有当发现、参数、结果、分页和传输元数据这五处对齐到同一份契约上，才适合交给 AI 自动调用。本课基于 MCP 2026-07-28 规范，把一次工具调用拆成五道门禁（发现→准入→调用→执行→消费），逐门讲清校验责任归谁：宿主拥有准入与消费两道门，服务器无法强迫客户端信任自己的注解、schema 或输出。

> **【拓展：MCP→真实生产链路】** 这五道门对应真实 AI 网关的分层：descriptor 校验是网关的"工具准入"，`x-mcp-header` 镜像是负载均衡按区域路由的依据，分页游标是目录同步的基础，completion 是表单自动补全的授权面。Phase 13 · 17（网关与注册中心）和 Phase 13 · 23（毕业项目）都会复用本课的准入核心。

> 🔗 **【前置】** 学本课前请先掌握：Phase 13 · 07（MCP 服务器）、Phase 13 · 09（MCP 传输：Streamable HTTP 细节）、Phase 13 · 10（resources 与 prompts，completion 的引用对象来自这里）。

**Type:** Build | **类型:** 动手实践
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lessons 07, 09, and 10 | **前置知识:** Phase 13 · 07、09、10
**Time:** ~120 minutes | **时间:** 约 120 分钟

## Learning Objectives | 学习目标

- Define tool inputs and outputs with JSON Schema 2020-12.
  中文翻译：用 JSON Schema 2020-12 定义工具的输入与输出。
- Validate structured results without assuming they are JSON objects.
  中文翻译：校验结构化结果，而不预设它们一定是 JSON 对象。
- Choose between text, image, audio, resource links, and embedded resources.
  中文翻译：在文本、图像、音频、资源链接与内嵌资源之间做出选择。
- Reject unsafe `x-mcp-header` definitions before a tool reaches the model.
  中文翻译：在不安全的 `x-mcp-header` 定义到达模型之前把它拒绝掉。
- Encode parameter-header values and verify exact header-to-body parity.
  中文翻译：对参数-头部值编码，并验证头部与请求体的精确一致性。
- Traverse cursor pagination without interpreting cursor values.
  中文翻译：遍历游标分页而不去解释游标的取值。
- Bound and authorize `completion/complete` suggestions.
  中文翻译：为 `completion/complete` 补全建议设界并做授权。

## The Problem | 问题引入

> **【中文解读】** 本课的出发点：调用本地 Python 函数是简单事，而通过 AI 宿主调用远端能力是一个契约问题。链路上有六个角色——服务器发布 descriptor、客户端把它变成模型上下文和 UI、模型生成参数、网关可能依据镜像头部路由请求、服务器执行工具、客户端再决定结果是否安全有效到可以还给模型。任何一环边界松了，整条链都坏。

Calling a Python function is easy. Calling a remote capability through an AI host is a contract problem.

> 调用一个 Python 函数很容易。通过 AI 宿主调用一个远端能力，则是一个契约问题。

The server publishes a descriptor. The client turns that descriptor into model context and user interface. The model creates arguments. A gateway may route the request from mirrored headers. The server executes the tool. The client then decides whether the result is safe and valid enough to return to the model.

> 服务器发布 descriptor；客户端把 descriptor 转换为模型上下文和用户界面；模型生成参数；网关可能根据镜像头部路由请求；服务器执行工具；客户端再决定这个结果是否足够安全、足够有效，可以返回给模型。

One weak boundary corrupts the whole chain.

Consider five failures:

- The descriptor says the result is an object, but the server returns an array.
- The client stops pagination when `nextCursor` is an empty string.
- A token parameter is mirrored into an HTTP header and becomes visible to intermediaries.
- A Unicode routing value is sent as a raw header, then the gateway and origin interpret different bytes.
- A completion endpoint suggests a production environment to a caller who cannot access it.

None of these failures is fixed by better prompting. They require explicit protocol and application contracts.

> 这五种失败没有一种能靠"更好的提示词"修复，它们需要显式的协议契约和应用契约。（五种失败分别是：descriptor 说结果是对象但服务器返回数组；`nextCursor` 为空字符串时客户端停止分页；token 参数被镜像进 HTTP 头并对中间人可见；Unicode 路由值以原始头部发送导致网关和源站解释不同的字节；补全端点向无权访问的调用者建议生产环境。）

## The Contract Pipeline | 契约流水线

> **【中文解读】** 把每次工具调用看作五道门：发现（读取确定性的分页工具列表）→ 准入（校验每个 descriptor 并应用本地安全策略）→ 调用（校验参数、构建传输元数据）→ 执行（运行处理器、正确分类失败）→ 消费（在交给模型前校验内容块与结构化输出）。关键归属：准入和消费两道门归宿主所有——服务器无法强迫客户端信任自己的注解、schema 或输出。

Treat each tool call as five gates:

1. **Discover.** Read a deterministic, paginated tool list.
2. **Admit.** Validate each descriptor and apply local security policy.
3. **Invoke.** Validate arguments and build transport metadata.
4. **Execute.** Run the handler and classify failures correctly.
5. **Consume.** Validate content blocks and structured output before model use.

```figure
mcp-contract-pipeline
```

The host owns the admission and consumption gates. A server cannot force a client to trust its annotations, schemas, or outputs.

## JSON Schema Is a Runtime Boundary | JSON Schema 是一道运行时边界

> **【中文解读】** 在 MCP 2026-07-28 中，`inputSchema` 和 `outputSchema` 都是 JSON Schema，`$schema` 缺省时方言默认 2020-12。三个要点：(1) 无参工具也应声明 `{"type":"object","additionalProperties":false}`，比裸 `{"type":"object"}` 更严；(2) 服务器一旦发布 outputSchema，包括 `isError: true` 在内的每个完整结果都要返回符合该 schema 的 `structuredContent`——错误标志只分类执行结果，不豁免输出契约；(3) 客户端应校验结果而不是信任 descriptor。

In MCP `2026-07-28`, `inputSchema` and `outputSchema` use JSON Schema. When `$schema` is absent, the default dialect is 2020-12.

> 在 MCP `2026-07-28` 中，`inputSchema` 与 `outputSchema` 使用 JSON Schema。`$schema` 缺失时默认方言是 2020-12。

The input schema must be a schema object. A tool with no arguments should still say exactly what it accepts:

```json
{
  "type": "object",
  "additionalProperties": false
}
```

This is stricter than `{ "type": "object" }`, which accepts arbitrary properties.

An output schema is optional. Once a server publishes one, every complete tool
result commits to returning conforming `structuredContent`, including results
with `isError: true`. The error flag classifies execution outcome; it does not
waive the published output contract. Clients should validate the result instead
of trusting the descriptor.

> 输出 schema 是可选的。服务器一旦发布了它，每一个完整工具结果都承诺返回符合该 schema 的 `structuredContent`——包括 `isError: true` 的结果。错误标志只分类执行结果，并不豁免已发布的输出契约。客户端应当校验结果，而不是信任 descriptor。

### Structured content is any JSON value | 结构化内容可以是任意 JSON 值

Do not hard-code `structuredContent` as a dictionary. It can be:

- an object;
- an array;
- a string;
- a number;
- a boolean;
- `null`.

This tool returns an array:

```json
{
  "name": "tag_catalog",
  "inputSchema": {
    "type": "object",
    "additionalProperties": false
  },
  "outputSchema": {
    "type": "array",
    "items": {"type": "string"}
  }
}
```

Its successful result is valid:

```json
{
  "resultType": "complete",
  "content": [
    {
      "type": "text",
      "text": "[\"contracts\", \"mcp\", \"stateless\"]"
    }
  ],
  "structuredContent": ["contracts", "mcp", "stateless"],
  "isError": false
}
```

For compatibility, structured results should also include serialized JSON in a text block. The text is not the validation source. `structuredContent` is.

> 为了兼容，结构化结果还应在一个文本块里携带序列化的 JSON。但文本不是校验的依据，`structuredContent` 才是。

### A small validator still teaches the boundary | 一个小校验器照样能教会这道边界

The lesson uses a deliberate JSON Schema subset because it stays inside the Python standard library. It checks the mechanisms used by the sample tools:

> 本课刻意使用一个 JSON Schema 子集，以保持在 Python 标准库之内。它校验示例工具用到的机制：object/array/string/integer/number/boolean/null 类型、required 属性、`additionalProperties: false`、数组 items、enum 取值、字符串最小长度。它不是完整生产校验器的替代品——可复用的课程要点是"校验发生在哪"：descriptor 在发现之后、参数在执行之前、结构化结果在消费之前。

- object, array, string, integer, number, boolean, and null types;
- required properties;
- `additionalProperties: false`;
- array items;
- enum values;
- minimum string length.

This is not a replacement for a complete production validator. The reusable lesson is where validation happens: after discovery for descriptors, before execution for arguments, and before consumption for structured results.

## Content Blocks Carry Different Costs | 内容块各有不同的代价

> **【中文解读】** `content` 数组可以混合五种内容块：text（人和模型可读的摘要，当作不可信输出对待）、image（base64 视觉证据，校验媒体类型和大小）、audio（base64 语音，校验媒体类型和时长）、resource_link（一个 URI 引用，客户端跟随它时要重新过资源授权）、resource（直接内嵌的数据，当场执行载荷与内容上限）。选择原则：大件或独立变化的东西用链接省一次往返的载荷；必须与结果原子同行的小证据才内嵌。

The `content` array can combine several content types.

| Type | Use it for | Main boundary |
|------|------------|---------------|
| `text` | Human and model-readable summaries | Treat text as untrusted output |
| `image` | Visual evidence encoded as base64 | Validate media type and size |
| `audio` | Spoken or recorded output encoded as base64 | Validate media type and duration limits |
| `resource_link` | A URI the client may fetch later | Reauthorize the later resource read |
| `resource` | Data embedded directly in the result | Enforce payload and content limits now |

A resource link is not proof that the resource appears in `resources/list`. It is a reference returned by this tool call. The client still applies its resource policy when it follows the URI.

> 资源链接并不证明该资源出现在 `resources/list` 里；它只是本次工具调用返回的一个引用。客户端跟随这个 URI 时，仍然要套用自己的资源策略。

An embedded resource avoids another round trip but increases the current response size. Use links for large or independently changing artifacts. Use embedded resources for small evidence that must travel atomically with the result.

> 内嵌资源省掉一次往返，但会增大当前响应体积。大件或独立变化的工件用链接；必须与结果原子同行的小证据才用内嵌。

The lesson's `evidence_bundle` result includes all five types. The client validates each block before accepting the result.

## `x-mcp-header` Is Routing Metadata | `x-mcp-header` 是路由元数据

> **【中文解读】** `inputSchema` 里的属性可以声明 `x-mcp-header`，客户端在 Streamable HTTP 上把该参数镜像为 `Mcp-Param-{name}` 头。目的：让负载均衡、网关或策略引擎不解析 JSON 体就能路由；它不是放凭证的地方。规范约束（全部 fail closed）：头名非空且符合 HTTP field-name 语法、大小写不敏感地唯一、属性类型只能是 string/integer/boolean（禁止 number）、注解只能出现在 `inputSchema.properties` 的直接成员上（嵌套对象的 properties、`oneOf` 分支、items、`$ref` 引到的定义、output schema 中一律拒绝）、整数必须在 JavaScript 安全整数范围内。本课另加一条部署策略：镜像 `password`/`secret`/`token`/`api_key`/`authorization` 等名字的 descriptor 直接拒绝。审计记录头名，不记录值。

A property inside `inputSchema` may declare `x-mcp-header`. Over Streamable HTTP, the client mirrors that argument into `Mcp-Param-{name}`.

```json
{
  "region": {
    "type": "string",
    "x-mcp-header": "Region"
  }
}
```

With `region: "eu-west"`, the transport can emit:

```http
Mcp-Param-Region: eu-west
```

The annotation exists so a load balancer, gateway, or policy engine can route without parsing the JSON body. It is not a place to put credentials.

The protocol constrains the annotation:

- the header name is non-empty and follows HTTP field-name token syntax;
- header names are unique without regard to case;
- the property type is string, integer, or boolean;
- `number` is not allowed;
- the annotation appears only on a direct member of `inputSchema.properties`;
- integer values stay within `-9007199254740991` through `9007199254740991`.

The location rule is syntactic and fail-closed. Walk the entire schema tree,
not just the properties your validator happens to understand. Reject an
annotation under a nested object's `properties`, a `oneOf` branch, `items`, a
definition reached by `$ref`, or any output schema. Resolving a reference does
not turn the referenced node into a direct top-level property.

> 位置规则是语法性的且失败关闭。要遍历整棵 schema 树，而不只是你的校验器恰好认识的那部分属性。嵌套对象的 `properties`、`oneOf` 分支、`items`、经 `$ref` 到达的定义以及任何输出 schema 里的注解都要拒绝——解析一个引用并不会把被引用节点变成直接顶层属性。

This lesson adds a deployment policy: reject descriptors that mirror names such as `password`, `secret`, `token`, `api_key`, or `authorization`. The official specification advises server authors not to mirror sensitive parameters. A client can turn that advice into a hard admission rule.

Audit the header name, not its value. The sample code records `Mcp-Param-Region` while keeping `eu-west` out of the audit event.

### Encode values before building HTTP headers | 构建HTTP头之前先对值编码

A parameter value may travel as plain text only when it is a non-empty string
of visible ASCII characters from `!` through `~` and does not resemble the
encoding sentinel. Everything else uses this exact form:

> 只有当一个参数值是 `!` 到 `~` 的可见 ASCII 字符组成的非空字符串、且不像编码哨兵时，才能以明文传输；其余一切（Unicode、空串、空格、制表符、控制字符、CR/LF、首尾空白、以及以 `=?base64?` 开头的值）都编码为 `=?base64?{Base64UTF8}?=`——对原始 UTF-8 字节做标准 base64，编码前不裁剪、不归一化、不替换。对"长得像哨兵"的值再编码一次，正是接收方能够还原字面原文而不是当作传输语法解码的关键。布尔渲染为小写 `true`/`false`；整数按十进制渲染且必须落在 JavaScript 安全整数范围内，范围外的值直接拒绝而不是让中间人四舍五入。

```text
=?base64?{Base64UTF8}?=
```

`Base64UTF8` is standard base64 over the exact UTF-8 bytes. Do not trim,
normalize, or replace the value first. Encode Unicode, empty strings, spaces,
tabs, control characters, CR or LF, leading or trailing whitespace, and any
value beginning with `=?base64?`. Encoding a sentinel-looking value again is
what lets the receiver recover the literal original text instead of decoding
it as transport syntax.

Booleans render as lowercase `true` or `false`. Integers render in base 10 and
must stay inside the JavaScript safe integer range. Values outside that range
are rejected instead of rounded by an intermediary.

### The server checks the mirrored copy | 服务器校验镜像副本

Header generation is only the client half. At the Streamable HTTP boundary,
the server must:

> 生成头部只是客户端这一半。在 Streamable HTTP 边界上，服务器必须：不区分头名大小写地找出已识别的 `Mcp-Param-*` 名字；存在时解码精确的 base64 哨兵形式；把解码文本与 JSON 体中对应参数做精确比较；在分发之前拒绝缺失、重复、意外、畸形或不匹配的已识别头。拒绝方式是 HTTP `400` 加 JSON-RPC 错误码 `-32020`，且审计记录里只放已识别头名和拒绝类别，不放体值也不放其编码形式。

1. find recognized `Mcp-Param-*` names without regard to header-name case;
2. decode the exact base64 sentinel form when present;
3. compare the decoded text with the corresponding JSON body argument exactly;
4. reject a missing, duplicated, unexpected, malformed, or mismatched
   recognized header before dispatch.

The rejection is HTTP `400` with JSON-RPC error code `-32020`. Neither the
body value nor its encoded header form belongs in the audit record. Record the
recognized header name and the rejection category only.

`code/main.py` models this boundary directly. [Lesson 09](../../09-mcp-transports/)
covers the wider Streamable HTTP validation order, including method and
protocol-version parity.

## Pagination Cursors Are Opaque | 分页游标是不透明的

> **【中文解读】** MCP 列表操作用游标分页：页大小和游标格式由服务器定，客户端只有一个决定——`nextCursor` 是否为 `None`。最经典的 bug 是用 Python 真值判断（`if not result.get("nextCursor")`）：空字符串是合法游标，真值判断会提前翻完。正确写法只判 `is None`。客户端不得解码、递增、与旧游标比较排序或推断页码——游标可能被签名、绑定目录版本或映射到私有状态，那都是服务器的实现细节。无效游标返回 JSON-RPC invalid params，错误码 `-32602`。

MCP list operations use cursor pagination. The server selects page size and cursor format. The client gets one decision:

```python
if result.get("nextCursor") is None:
    break
cursor = result["nextCursor"]
```

Do not write this:

```python
if not result.get("nextCursor"):
    break
```

An empty string is a valid cursor. Truthiness would stop too early.

> 空字符串是一个合法游标。真值判断会停得太早。

Clients must not decode a cursor, increment it, compare it with a prior cursor for ordering, or infer a page number. A server may sign a cursor, bind it to a catalog version, or map it to private state. That is the server's implementation detail.

The sample server deliberately returns `""` after the first page. The client must send that exact value on the second request. Its trace is:

```text
<first request with no cursor>
<second request with cursor "">
```

Invalid cursors produce JSON-RPC invalid params, code `-32602`.

## Completion Is an Authorization Surface | Completion 是一个授权面

> **【中文解读】** `completion/complete` 为 prompt 参数和资源模板参数提供补全建议。它对交互式表单很有用，但可能泄露普通 list 方法保护起来的名字——示例中的 analyst 只能看到 `development` 和 `staging`，只有 operator 能看到 `production`。原则：对补全请求套用与被引用 prompt/resource 相同的授权边界。生产级补全还需要输入校验、按调用者过滤、客户端防抖、服务器限流、结果数上限，以及不暴露敏感建议值的日志。补全是辅助输入，不是绕过发现权限的后门。

`completion/complete` provides suggestions for prompt arguments and resource-template arguments. It is useful for interactive forms, but it can leak names that ordinary list methods protect.

A completion request names a reference and the argument being completed:

```json
{
  "method": "completion/complete",
  "params": {
    "ref": {
      "type": "ref/prompt",
      "name": "deployment_review"
    },
    "argument": {
      "name": "environment",
      "value": "st"
    }
  }
}
```

The result returns at most 100 values and may report `total` plus `hasMore`.

Apply the same authorization boundary used by the referenced prompt or resource. An analyst in the sample receives `development` and `staging`. Only an operator can receive `production`.

Production completion also needs:

- input validation;
- caller-aware filtering;
- request debouncing in the client;
- rate limiting in the server;
- bounded result counts;
- logs that do not expose sensitive suggestion values.

Completion is assistance, not discovery bypass.

## Two Error Layers | 两个错误层

> **【中文解读】** 协议错误与工具执行错误必须分开。MCP 请求无法正确分发时用 JSON-RPC error（未知工具名、请求形状畸形、缺请求元数据、游标无效）；调用已到达工具、工具报告可行动的失败时，用 `isError: true` 的完整工具结果（报告源不可用、日期超出支持范围、业务规则拒绝）。模型往往能修复工具执行错误，却无法修复一个违反自身输出 schema 的服务器。若工具声明了输出 schema，可行动的失败也要建模在该 schema 之内——示例 `route_report` 的失败返回请求的区域加 `accepted: false`，配人类可读的错误文本和 `isError: true`。

Keep protocol errors separate from tool execution errors.

Use a JSON-RPC error when the MCP request cannot be dispatched correctly:

- unknown tool name;
- malformed request shape;
- missing request metadata;
- invalid cursor.

Use a complete tool result with `isError: true` when the invocation reached the tool and the tool reports an actionable failure:

- a report source is unavailable;
- a date is outside the supported range;
- a business rule rejects the requested operation.

Models can often repair a tool execution error. They cannot repair a server that violated its own output schema.

If the tool declares an output schema, model an actionable failure inside that
schema. The sample `route_report` failure returns its requested region with
`accepted: false`, alongside human-readable error text and `isError: true`.

## Build It | 动手实现

> **【中文解读】** `code/main.py` 用 Python 标准库同时实现边界两侧。服务器侧：逐请求 MCP 元数据校验、带 tools 与 completions 能力的 `server/discover`、确定性 `tools/list` 分页、四个工具 descriptor（其中一个必须被拒绝）、数组结构化输出、全部五种内容块类型、解码已识别参数头并在不匹配时返回 HTTP `400` + JSON-RPC `-32020` 的 Streamable HTTP 一致性门禁、带授权和限流的补全。客户端侧：descriptor 准入、全树 `x-mcp-header` 位置校验和敏感字段策略、精确的明文可见 ASCII 或 base64 UTF-8 编码、能跟随空字符串的不透明游标循环、参数与结果校验、内容块校验、只含头名不含值的审计事件。那个刻意不安全的 descriptor 是教学数据：证明一个被拒的工具不妨碍其他合法工具加载。

`code/main.py` builds both sides of the boundary with the Python standard library.

The server implements:

- per-request MCP metadata validation;
- `server/discover` with tools and completions capabilities;
- deterministic `tools/list` pagination;
- four tool descriptors, including one that must be rejected;
- array structured output;
- every current tool content block type;
- a Streamable HTTP parity gate that decodes recognized parameter headers and
  returns HTTP `400` plus JSON-RPC `-32020` on mismatch;
- authorized and rate-limited completion.

The client implements:

- descriptor admission;
- full-tree `x-mcp-header` placement validation and sensitive-field policy;
- exact plain-visible-ASCII or base64 UTF-8 value encoding;
- an opaque cursor loop that follows an empty string;
- argument and result validation;
- content-block validation;
- header audit events containing names but not values.

The deliberately unsafe descriptor is teaching data. It proves that one rejected tool does not prevent valid tools from loading.

## Use It | 学以致用

From the repository root:

```bash
cd phases/13-tools-and-protocols/28-mcp-tool-contracts-and-content/code
python3 main.py
python3 -m unittest discover tests -v
```

The demo prints admitted tools, the rejected descriptor, both pagination
requests, structured array content, content-block types, mirrored header
names, whether the value required encoding, the HTTP parity status, and
caller-filtered completion values.

## Interactive Lab | 交互实验

> **【中文解读】** 十步实验的核心不是背 JSON 形状，而是亲眼看每道门在"拥有它的边界"上失败：把 `tag_catalog.outputSchema.type` 改成 `object` 看客户端拒绝返回的数组；让首页 `nextCursor` 保持 `""` 看游标 trace；给字符串属性加 `x-mcp-header: "Authorization"` 看准入拒绝；用 Unicode、换行、首尾空格、字面 `=?base64?SGVsbG8=?=` 试编码回环；把注解挪进 `oneOf`/`items`/`$ref` 看全树遍历；改掉或删掉已识别头看 HTTP 边界返回 `400` + `-32020`。

Open `code/main.py` and locate `TOOLS`.

1. Change `tag_catalog.outputSchema.type` from `array` to `object`.
2. Run the demo. The client should reject the returned array.
3. Restore the schema.
4. Keep the first page's `nextCursor` as `""`, then make the final page return
   `nextCursor: None` instead of omitting the field.
5. Run the tests and compare the cursor trace.
6. Add `x-mcp-header: "Authorization"` to a string property.
7. Confirm descriptor admission rejects it before invocation.
8. Try `region` values containing Unicode, a newline, surrounding spaces, and
   the literal text `=?base64?SGVsbG8=?=`. Decode each emitted header and prove
   the original value survives exactly.
9. Move the annotation under `oneOf`, `items`, or a `$ref` definition. Confirm
   each descriptor is rejected even if that branch is never used by the demo.
10. Remove the recognized header or change its decoded value. Confirm the HTTP
    boundary returns status `400` and JSON-RPC code `-32020`.

The point is not to memorize a JSON shape. It is to watch each gate fail at the boundary that owns it.

## Practice Lab | 进阶练习

Extend the contract lab with a `search_evidence` tool.

> 给契约实验扩展一个 `search_evidence` 工具。九条要求：(1) 输入 schema 接受 `query`、`limit` 和一个安全的 `region` 路由字段；(2) 输出 schema 是含 `uri`、`title`、`score` 的对象数组；(3) 结果包含兼容文本和每项一个资源链接；(4) 参数拒绝未知属性；(5) `limit` 由应用校验设界；(6) 无权访问某 URI 的调用者永远不能通过补全或工具输出看到它；(7) 测试覆盖不合规 score、非法头注解和两页列表；(8) 头值测试覆盖可见 ASCII、Unicode、控制字符、空白、哨兵样文本和 JavaScript 安全整数两个边界；(9) HTTP fixture 大小写不敏感地接受头名，但缺失或不匹配时返回 `400` + `-32020`。

Requirements:

1. Its input schema accepts `query`, `limit`, and a safe `region` routing field.
2. Its output schema is an array of objects with `uri`, `title`, and `score`.
3. The result includes compatibility text and a resource link per item.
4. Arguments reject unknown properties.
5. `limit` is bounded by application validation.
6. A caller without access to one URI never sees that URI through completion or tool output.
7. Tests include a nonconforming score, an invalid header annotation, and a two-page list.
8. Header-value tests cover visible ASCII, Unicode, control characters,
   whitespace, sentinel-looking text, and both JavaScript-safe integer bounds.
9. The HTTP fixture accepts case-insensitive header names but rejects missing
   or mismatched recognized values with status `400` and code `-32020`.

## Shipped Artifact | 产出物

`outputs/skill-mcp-contract-reviewer.md` is a flat, reusable review skill. Give it a tool descriptor, sample results, pagination behavior, and completion policy. It returns an admission decision, result-validation plan, header policy, and concrete failure tests.

> `outputs/skill-mcp-contract-reviewer.md` 是一个扁平、可复用的评审 skill：给它一个工具 descriptor、样例结果、分页行为和补全策略，它会返回准入决定、结果校验计划、头部策略和具体的失败测试。

## Verify It | 验证

> **【中文解读】** 验收清单要逐条过：`tools/list` 重复调用顺序稳定；`nextCursor` 为 `""` 时客户端会发第二次请求；敏感头 descriptor 被排除而其他工具可用；数组过数组 schema、对象不过；错误结果不能省略或违反已发布的输出 schema；五种内容块全部通过校验；审计事件只有名没有值；明文保持明文、其余值经 base64 UTF-8 精确往返；安全整数范围外的整数被拒绝；藏在 `oneOf`/`items`/嵌套对象/`$ref`/输出 schema 里的注解在准入期被拒；大小写不敏感的已识别头名只有在解码值与体精确匹配时才通过，否则 `400` + `-32020`；analyst 的补全永远不返回 `production`；工具失败用 `isError: true`，畸形协议调用用 JSON-RPC `error`。

The lesson is complete when these statements are true:

- `tools/list` returns the same logical order on repeated calls.
- The client performs a second request when `nextCursor` is `""`.
- The unsafe sensitive-header descriptor is excluded while other tools remain available.
- An array passes its array output schema.
- An object fails that same array schema.
- Error results cannot omit or violate a published output schema.
- Text, image, audio, resource link, and embedded resource blocks validate.
- Header audit events contain names and no values.
- Plain visible ASCII remains plain; Unicode, control, padded, empty, and
  sentinel-looking values round-trip through exact base64 UTF-8 encoding.
- Mirrored integers outside the JavaScript safe range are rejected.
- Annotations under `oneOf`, `items`, nested objects, `$ref` definitions, or
  output schemas are rejected during admission.
- Case-insensitive recognized header names pass only when the decoded value
  exactly matches the body; missing or mismatched copies produce HTTP `400`
  and JSON-RPC `-32020`.
- Analyst completion never returns `production`.
- A tool failure uses `isError: true`; a malformed protocol call uses JSON-RPC `error`.

## Production Failure Modes | 生产失败模式

> 下表左列是失败、中列是你看到的现象、右列是正确响应。最容易踩的三行：空游标当假值（最后几页消失）、敏感值被镜像（secret 出现在代理/WAF/trace 里）、头体不一致（网关路由到 A 而源站执行 B）。

| Failure | What the learner sees | Correct response |
|---------|-----------------------|------------------|
| Client assumes object output | Valid arrays fail or are silently wrapped | Validate against the published schema without object-only types |
| Empty cursor treated as false | Final pages disappear | Continue whenever `nextCursor` is present and non-null |
| Sensitive value mirrored | Secret appears in proxy, WAF, or trace data | Reject the descriptor and keep secrets in protected request data |
| Raw Unicode or whitespace mirrored | Gateway and origin disagree or the value is normalized | Use exact base64 UTF-8 sentinel encoding and compare after decoding |
| Annotation hidden in a schema branch | A client misses routing metadata during admission | Traverse the entire schema tree and allow only direct top-level properties |
| Large integer mirrored | JavaScript intermediary rounds the routing value | Reject values outside the JavaScript safe integer range |
| Header and body disagree | Gateway routes one target while the origin executes another | Reject before dispatch with HTTP `400` and JSON-RPC `-32020` |
| Output schema ignored | Downstream code consumes corrupt structure | Validate before model or application use |
| Resource link trusted automatically | Caller follows an unauthorized URI | Reauthorize every resource read |
| Completion shares global suggestions | Hidden tenant names leak | Filter by caller, reference, and authorization |
| Tool annotations treated as policy | Destructive operation bypasses confirmation | Enforce authorization and approval outside annotations |
| One malformed tool breaks discovery | Entire server becomes unavailable | Reject the bad descriptor and admit valid tools independently |

## Capstone Connection | 毕业项目衔接

The Phase 13 capstone needs a gateway that can merge tools from several servers. This lesson provides its admission core.

> Phase 13 毕业项目需要一个能合并多台服务器工具的网关，本课提供它的准入核心。用它给四件毕业证据打分：确定且完整的分页发现、模型暴露之前的 descriptor 校验、校验过的结构化输出加上有界内容块、保持授权边界的补全与路由元数据。不要只凭一次成功的 `tools/call` 就宣称网关兼容——要捕获 descriptor、分页 trace、准入工具集、拒绝工具集和一个已校验结果。

Use the artifact to grade four pieces of capstone evidence:

- deterministic and complete paginated discovery;
- descriptor validation before model exposure;
- validated structured output plus bounded content blocks;
- completion and routing metadata that preserve authorization boundaries.

Do not claim gateway compatibility from a successful `tools/call` alone. Capture the descriptor, page trace, admitted tool set, rejected tool set, and one validated result.

## Key Terms | 关键术语

| Term | Meaning |
|------|---------|
| `inputSchema` | JSON Schema object defining accepted tool arguments |
| `outputSchema` | Optional JSON Schema defining `structuredContent` |
| `structuredContent` | Any JSON value produced by a tool result |
| Content block | Typed text, image, audio, resource link, or embedded resource |
| `x-mcp-header` | Schema annotation that mirrors a primitive argument into Streamable HTTP metadata |
| Opaque cursor | Server-issued pagination token whose value the client does not interpret |
| Completion reference | Prompt name or resource URI/template whose argument is being completed |
| Admission | Client decision to expose or reject a discovered descriptor |

## Further Reading | 延伸阅读

- [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [MCP Completion](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/completion)
- [MCP Pagination](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/pagination)
- [MCP Streamable HTTP Parameter Headers](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http#custom-headers-from-tool-parameters)
