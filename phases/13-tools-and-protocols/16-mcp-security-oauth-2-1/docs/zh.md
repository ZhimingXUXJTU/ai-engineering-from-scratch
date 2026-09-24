# MCP 授权：CIMD、签发方绑定、PKCE 与逐步授权

> 远程 MCP 请求是无状态的，但授权不是匿名的。把每份凭证绑定到签发它的 issuer（签发方），把每个 token 绑定到接收它的 resource（资源）。

> **【中文解读】** 2026-07-28 授权配置的两大支柱：凭证绑定 issuer、token 绑定 resource。本课在进程内完整模拟受保护资源元数据发现、注册优先级（CIMD 优先、DCR 弃用兼容）、PKCE、`iss` 校验、资源绑定 token 与逐步授权。

> **【拓展】** OAuth 2.1 合并了多年安全最佳实践：强制 PKCE、禁止隐式流程。MCP 在其上叠加自己的配置：注册优先级（预注册 > CIMD > 弃用的 DCR）、RFC 9207 的 `iss` 参数精确校验、禁止跨 issuer 复用凭证。CIMD（Client ID Metadata Document，客户端 ID 元数据文档）是新一代注册机制——客户端自托管一个 HTTPS 元数据文档，文档 URL 本身就是 client_id，免去每次首接触都要动态注册的旧负担。

> 🔗 **【前置】** 学本节前请先掌握：(1) Phase 13 · 09（transports）——只有远程 Streamable HTTP 才需要 OAuth；(2) Phase 13 · 15（security）——理解威胁面与主体概念；(3) OAuth 2.0/2.1、PKCE、Bearer token 基础；(4) RFC 9728 / RFC 8707 / RFC 9207 三份 RFC——本课逐一实现其关键校验。

**类型：** 构建
**语言：** Python
**前置条件：** Phase 13 · 09（传输层）、Phase 13 · 15（安全）
**预计用时：** 约 90 分钟

## 学习目标

- 通过受保护资源元数据发现授权服务器。
- 优先使用客户端 ID 元数据文档（CIMD），而非已弃用的动态客户端注册（DCR）。
- 当 DCR 兼容路径不可避免时，声明正确的 `application_type`。
- 校验授权响应的 `iss`，并按签发方隔离凭证。
- 使用 PKCE、资源指示器、受众校验和增量权限范围。
- 在无协议会话的情况下发送已授权的 MCP 2026-07-28 请求。

> **【中文解读】** 六个目标串起来就是一条完整的远程 MCP 授权流水线：发现 → 注册 → 兼容路径 → iss 校验与隔离 → 四件套（PKCE/资源指示器/受众/增量 scope）→ 无状态授权请求。

## 问题引入

远程 MCP 服务器可能读取隐私记录、写入外部系统或触发昂贵操作。认证告诉它谁出示了凭证。授权还必须回答：

- 哪个授权服务器签发了这份凭证？
- 这个 token 是给哪个 MCP 资源的？
- 哪个客户端和重定向 URI 完成了流程？
- 用户批准了哪些操作？
- 这个请求是否仍在该批准范围内？

2026-07-28 授权配置强化了客户端注册与 issuer 处理：优先 CIMD、弃用 DCR、要求 DCR 声明正确的 `application_type`、校验 RFC 9207 issuer 响应、禁止跨 issuer 复用凭证。

这些规则与无状态核心互补，不恢复核心握手或 `Mcp-Session-Id`。

> **【中文解读】** 认证回答"谁出示了凭证"，授权还要回答五个问题：谁签发、给哪个资源、哪个客户端、批准了什么、本请求是否仍在范围内。2026-07-28 的答案全部落在"注册"与"issuer 处理"两个环节上。

> 💡 **【类比】** token 像会员卡，资源指示器（RFC 8707）相当于在卡上印"仅限本店使用"（aud 受众锁定）；issuer 绑定则是"每家店的会员卡分开办"——健身房的卡拿到超市刷不开。CIMD 像"自带的电子名片"：名片 URL 就是身份，到新店出示名片即可入会，不用每家店重新填表（DCR）；但消费记录仍按店（issuer）分开保存，换店时旧积分（旧凭证）不带过去。

## 核心概念

### 认识三个角色

- **MCP 客户端：** 代表资源所有者发送请求。
- **MCP 资源服务器：** 接受 access token 并提供 MCP 端点。
- **授权服务器：** 认证资源所有者、收集同意并签发 token。

资源服务器和授权服务器可以一起运营，但它们的标识符和校验职责要保持分离。

> **【中文解读】** 三角色与教科书 OAuth 相同，但 MCP 强调：即使资源服务器与授权服务器同属一个服务，两者的 URL 标识与校验职责也必须分开——issuer 字符串是后续一切隔离存储的键。

### 授权只适用于 HTTP

MCP 授权规范只适用于 HTTP 系传输。本地 stdio 服务器运行在进程与操作系统的信任边界内，不要为了"对称"给 stdio 加一个假浏览器 OAuth 流程。

对远程 Streamable HTTP，每个请求都把 bearer token 放在 `Authorization` 头里发送，绝不放进 URL。

> **【中文解读】** stdio 场景的信任边界是"谁能启动这个进程"；HTTP 场景的信任边界才是"谁能在网络上出示凭证"。给 stdio 硬加 OAuth 既不增加安全，又增加攻击面。

### 从受保护资源元数据开始

资源服务器发布 RFC 9728 元数据：

```json
{
  "resource": "https://notes.example.com/mcp",
  "authorization_servers": ["https://auth.example.com"],
  "scopes_supported": ["notes:delete", "notes:read", "notes:write"]
}
```

客户端从 MCP 资源 URL 出发，获取这份文档，选择一个声明的授权服务器，再获取该服务器的 OAuth 或 OpenID Connect 元数据。

构造 RFC 9728 well-known URL 时要保留资源路径。资源 `https://notes.example.com/mcp` 对应 `https://notes.example.com/.well-known/oauth-protected-resource/mcp`。丢掉 `/mcp` 后缀可能选中同源上另一个受保护资源的元数据。

不要从主机名猜授权服务器；不要跟随来自未校验错误体的 issuer；保留一份"客户端愿意信任哪些 issuer"的策略。

> **【中文解读】** 发现链条是"资源 URL → RFC 9728 文档 → 授权服务器元数据"。最容易踩的坑是 well-known URL 丢路径后缀：同源上可能部署着多个受保护资源，选错文档就找错授权服务器。

### 校验授权服务器元数据

元数据应暴露端点与受支持的控制项：

```json
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "code_challenge_methods_supported": ["S256"],
  "authorization_response_iss_parameter_supported": true,
  "client_id_metadata_document_supported": true
}
```

PKCE 要求 S256。记录精确的 issuer 字符串——这个精确值将成为注册与 token 存储的键。

> **【中文解读】** 两件事必须在这里敲定：PKCE 只接受 S256（_plain challenge 不被接受_）；issuer 按原始字符串逐字节记录，不做任何规范化——后面的凭证隔离全靠它。

### 遵循注册优先级

客户端与所选 issuer 已有明确关系时用预注册信息；否则在授权服务器声明支持时优先 CIMD；DCR 只作弃用的兼容回退；这些机制都不可用时才提示输入客户端信息。

> **【中文解读】** 注册优先级的每一步都有明确的"降级理由"：预注册是既有信任关系，CIMD 是规范推荐的新默认，DCR 是为旧授权服务器保留的兼容通道。关键纪律：降级必须是显式决策，不能在 CIMD 校验失败后静默落到 DCR——那等于把安全故障变成更弱的注册路径。

### 优先使用客户端 ID 元数据文档

客户端 ID 元数据文档给授权服务器一个 HTTPS URL，它既是客户端标识又是其元数据的位置：

```json
{
  "client_id": "https://client.example.com/oauth/metadata.json",
  "client_name": "Notes desktop client",
  "application_type": "native",
  "redirect_uris": ["http://127.0.0.1:8765/callback"],
  "grant_types": ["authorization_code"],
  "response_types": ["code"]
}
```

授权服务器拉取并校验该文档。`client_id` 必须是带路径的 HTTPS URL，且文档内的值与该 URL 完全相等。文档必填字段为 `client_id`、`client_name`、`redirect_uris`。`application_type` 出现在示例中但不是 CIMD 的必填项——它的新强制用途专门在 DCR 路径上。

把拉取文档当作 SSRF 敏感操作：解析并校验目的地，拒绝回环、私网、链路本地等禁用地址，重定向与 DNS 变化后复检，限制重定向次数、字节与时间，强制 JSON，只按已校验的 HTTP 缓存控制来缓存。`client_name` 等展示字段按不可信文本处理。

CIMD 免去了每次首次接触都铸造新动态标识的需要，但不免除重定向 URI 校验、issuer 策略或用户同意。

> **【中文解读】** CIMD 的本质是"让客户端自己托管身份"：URL 即标识，文档即元数据。授权服务器要做的是"验证名片真伪"（拉取 + 全等校验），而这一步是 SSRF 高危操作，必须按内网防护标准处理。

> ⚠️ **【易错点】** 场景：把拉取 CIMD 文档当成普通 GET，不校验目标地址 / 后果：SSRF——攻击者把 `client_id` 指向内网地址（如云元数据服务 169.254.169.254），授权服务器替攻击者发起请求 / 修复：(1) 解析后校验 IP，拒绝回环/私网/链路本地段；(2) 限制重定向次数、响应字节与超时；(3) 强制 JSON、按已验证的 Cache-Control 缓存；(4) 展示字段一律按不可信文本转义。

### DCR 是兼容路径

动态客户端注册（DCR）对较旧的授权服务器仍然可用，但对新的 MCP 实现已弃用。

使用 DCR 时，声明 `application_type`：

```json
{
  "client_name": "Notes desktop client",
  "application_type": "native",
  "redirect_uris": ["http://127.0.0.1:8765/callback"],
  "grant_types": ["authorization_code"],
  "response_types": ["code"]
}
```

- 桌面、移动、命令行和回环客户端用 `native`。
- 远程托管的浏览器应用用 `web` 和远程 HTTPS 重定向。

省略该字段时，OpenID Connect 注册实现可能默认 `web`，导致合法的回环重定向失败。

DCR 代码要放在显式的回退决策之后。不要在 CIMD 校验任意失败后静默回退——那可能把一次安全失败变成更弱的注册路径。

> **【中文解读】** `application_type` 决定重定向 URI 规则：`native` 允许 `http://127.0.0.1` 回环，`web` 只允许远程 HTTPS。默认值若为 `web`，本地桌面客户端的回环回调会被拒——这是最典型的"省一个字段，流程全挂"。

### 把凭证绑定到签发方

把 issuer 铸造的注册材料存到精确的 issuer 名下：

```text
issuer_credentials[issuer] = pre_registered_or_dcr_client
tokens[(issuer, resource)] = access_token
```

如果受保护资源发现的结果从 `https://auth-one.example` 变成 `https://auth-two.example`，要重新评估信任。绝不把第一个 issuer 的 client secret、DCR client id、注册访问令牌、refresh token 或 access token 发给第二个。预注册和 DCR 客户端必须使用新 issuer 签发的凭证。

CIMD client id 不同：它是自托管的 HTTPS URL，不是授权服务器铸造的凭证。同一个 CIMD URL 可移植——新的受信 issuer 拉取并校验文档即可，无需 DCR 重新注册。但授权响应与 token 仍在新 issuer 名下校验和存储。

> **【中文解读】** 存储模型是两级键：注册凭证按 issuer 一级，token 按 (issuer, resource) 两级。issuer 一变，旧槽位里的所有东西都留在原地，绝不迁移——防止"换门牌偷家当"。CIMD URL 是唯一例外，因为它的可信度来自"你自托管"而不是"某 issuer 签发"。

### 带 PKCE 的授权码流程

交互式流程是：

1. 生成高熵 `code_verifier`。
2. 派生 S256 `code_challenge`。
3. 发送授权请求，带精确的 `client_id`、`redirect_uri`、`scope`、`code_challenge` 和 `resource`。
4. 接收包含 `code` 与（若提供）`iss` 的授权响应。
5. 在使用任何响应字段之前，先对照精确记录的 issuer 校验 `iss`。
6. 用 `code_verifier`、同一 redirect URI 和同一 `resource` 换取 token。
7. 把得到的 token 存到 `(issuer, resource)` 名下。

来自 RFC 8707 的 `resource` 参数同时出现在授权请求与 token 请求中，标识规范的 MCP 服务器 URI。

> **【中文解读】** PKCE 让客户端不必存密钥：每次流程生成临时 verifier，授权服务器只认 S256 哈希。这对装在用户机器上的 MCP 客户端（Claude Desktop、Cursor 等）至关重要——client_secret 反正会被逆出来。`resource` 参数则保证换来的 token 只对一个 MCP 服务器有效。

### 精确校验 `iss`

RFC 9207 防止一个 issuer 的授权响应与另一个 issuer 的响应相混淆。

`iss` 存在时，与记录的 issuer 比较——不折叠大小写、不改尾斜杠、不去默认端口、不做百分号编码规范化。不匹配时，不要使用 code，甚至不要展示该响应中攻击者可控的错误详情。

包含 `iss` 的授权服务器会声明 `authorization_response_iss_parameter_supported: true`。即使缺少该声明，当前客户端仍要校验存在的 `iss`。

> **【中文解读】** issuer 是所有凭证存储的键，"规范化一下再比"会给相似 issuer 挤进同一存储槽位的机会。RFC 9207 的设计就是字节级相等——多一个斜杠都不行。

> 🤔 **【困惑】** Q: 为什么"精确字符串比较"这么较真？差个尾斜杠不行吗？A: 不行。若 `https://auth.example.com` 与 `https://auth.example.com/` 视为相等，攻击者注册带尾斜杠的相似 issuer 就能继承别人的凭证。OAuth 历史上多次账号接管都源于"规范化再比"的善意。字节级相等是有意为之。

### 在 MCP 服务器端校验受众

资源服务器只接受为自己签发的 token：

```text
token.issuer == configured_authorization_server
token.audience == canonical_mcp_resource
```

无效、过期、错 issuer、错受众的 token 一律 401。MCP 服务器不得接受或转运给其他服务签发的 token。

> **【中文解读】** 受众校验是资源指示器的对偶：客户端在请求时声明"给谁用"，服务器在验收时核对"是不是给我的"。混淆代理攻击（把 A 服务器的 token 转给 B）在这条检查前止步。

### 请求最小的当前权限范围

先请求现在需要的 scope。如果后续工具需要更多，服务器返回带权威 scope 挑战的 403：

```text
WWW-Authenticate: Bearer error="insufficient_scope",
  scope="notes:delete",
  resource_metadata="https://notes.example.com/.well-known/oauth-protected-resource/mcp"
```

客户端向用户解释新权限、取得同意、用合并后的 scope 集执行新的授权流程，然后用新的 JSON-RPC id 重试 MCP 请求。

不要假设被挑战的 scope 是 `scopes_supported` 的子集。挑战对当前操作是权威的。

> **【中文解读】** 逐步授权（step-up）是最小权限原则的机制化：默认只拿只读，需要删除时才弹同意框补 `notes:delete`。挑战通过 `WWW-Authenticate` 头传递，且附带 `resource_metadata` 让客户端知道去哪发现授权服务器。

### 授权与无状态 MCP 线格式

已授权的工具调用仍要携带完整的当前请求信封：

```text
POST /mcp
Authorization: Bearer <access-token>
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: notes.delete
```

```json
{
  "jsonrpc": "2.0",
  "id": 12,
  "method": "tools/call",
  "params": {
    "name": "notes.delete",
    "arguments": {"id": "note-7"},
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "oauth-lesson-client",
        "version": "1.0.0"
      }
    }
  }
}
```

token 授权主体；请求元数据协商协议行为。两者互不替代。

按固定顺序校验线上格式：JSON-RPC 与元数据类型、头与正文相等、然后协议支持。路由或版本头不匹配返回 HTTP 400 `-32020`；头文一致但版本不支持，返回 HTTP 400 `-32022` 且 `data` 精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`；未知方法返回 HTTP 404 `-32601`。

每个请求错误——包括 401 无效 token 和 403 权限不足——都是带原请求 `id` 的 JSON-RPC 错误信封。结构化恢复信息放在可选的 error `data` 里；`WWW-Authenticate` 仍是 HTTP 响应头。通知没有 `id`，不收 JSON-RPC 正文；被接受的 HTTP 通知返回 202 空体。

服务器实现 `server/discover` 并通告工具，因此也实现必需的 `tools/list` 方法。工具描述符有稳定的名称、描述和对象根 `inputSchema`。列表是确定性的，返回 `resultType`、服务器身份元数据、有界的 `ttlMs` 和 `cacheScope`。发现与不随用户变化的工具列表可以在授权前提供；若任一随主体变化，就要应用常规策略和私有缓存。

> **【中文解读】** 授权层和协议层是两条独立的轴：`Authorization` 头回答"主体是谁、能做什么"，`_meta` 与路由头回答"这是什么协议行为"。任何一层都不能代替另一层做决定——这是 2026-07-28 无状态设计的底层纪律。

### 禁止 token 透传

MCP 服务器不得把客户端的 MCP access token 转发给下游 API。要么获取受众正确的独立下游 token，要么使用显式的 token 交换设计。受众校验只有在各服务拒绝"为别人签发的 token"时才有效。

### Refresh token

Refresh token 是可选的。签发时按 issuer 和 resource 为键机密存储；不要假设它们存在。授权服务器支持轮换时就轮换，并检测失效值被重用。

> **【中文解读】** "不透传"是受众校验能成立的群体约定：只要有一个服务滥收别人的 token，整条信任链就破。下游访问要用自己的凭证换自己的 token，必要时走显式 token 交换（RFC 8693 思路）。

## 动手构建

`code/main.py` 是进程内协议与授权模拟器：受保护资源发现、授权服务器元数据、CIMD 注册、版本门控的 DCR 回退、application type 检查、PKCE、issuer 校验、资源绑定 token、scope 逐步升级、`server/discover`、`tools/list` 和一个无状态工具请求。

模型接收已解析的请求正文与路由头，不是完整 HTTP 适配器，不解析 `Content-Type` 或 `Accept`。把它接到 Lesson 09 的 Streamable HTTP 适配器上——那边要求 `Content-Type: application/json`，且 `Accept` 同时包含 `application/json` 与 `text/event-stream`。

运行：

```bash
cd phases/13-tools-and-protocols/16-mcp-security-oauth-2-1
python3 code/main.py
python3 -m unittest discover code/tests -v
```

输出依次展示：发现流程、CIMD 注册、一次普通读取、两次独立的 scope 逐步升级，以及按 issuer 为键的凭证存储。

> **【中文解读】** 读代码时按调用链走：`Client.discover` → `enroll`（CIMD/DCR 分支）→ `authorize`（PKCE）→ `exchange`（iss 校验）→ `handle`（受众 + scope）。两次 step-up 分别演示"读够了、删除要补授权"的完整闭环。

## 实际使用

把模拟器对象映射到生产组件：

- `ResourceServer.protected_resource_metadata` 对应 RFC 9728 端点。
- `AuthorizationServer.metadata` 对应 RFC 8414 或 OpenID Connect 发现。
- `Client.enroll` 对应 CIMD 解析加显式的 DCR 兼容分支。
- issuer 铸造的客户端凭证和 `tokens_by_issuer_resource` 对应加密记录。CIMD URL 可保持可移植，而其授权结果保持 issuer 绑定。
- `ResourceServer.handle` 对应中间件——分发前校验当前 MCP 头、token 和工具 scope，并让每个请求错误都落在匹配的 JSON-RPC 错误信封里。

## 产出物

本课产出 `outputs/skill-oauth-scope-planner.md`。它现在设计的内容包括：注册优先级、issuer 绑定的凭证存储、application type、PKCE、资源指示器、scope 挑战，以及当前的无状态请求边界。

## 练习题

1. 添加 refresh token 轮换，并拒绝上一个 refresh token 的重用。

2. 添加 issuer 允许列表。issuer 变更时只复用可移植的 CIMD URL，拒绝之前所有 issuer 铸造的凭证与 token。

3. 给授权码加过期时间，确认迟到换取失败。

4. 构建带远程 HTTPS 重定向的 web 客户端变体，并比较其 DCR 元数据与 native 客户端的差异。

5. 在同一 issuer 下添加第二个资源。确认它的 access token 不能用在第一个资源上。

## 术语速查表

| 术语 | 含义 | 英文 |
|------|------|------|
| 受保护资源元数据 | 标识资源与授权服务器的 RFC 9728 文档 | Protected-resource metadata |
| 客户端 ID 元数据文档 | URL 即 OAuth 客户端标识的 HTTPS 元数据文档 | CIMD |
| 动态客户端注册 | 已弃用、仅作兼容保留的动态注册 | DCR |
| `application_type` | `native` 或 `web`，用于校验重定向 URI 规则 | application_type |
| PKCE | 保护被拦截授权码的 verifier 与 S256 challenge | PKCE |
| `iss` | RFC 9207 授权响应签发方标识 | iss parameter |
| 资源指示器 | 把 token 请求绑定到 MCP 资源的 RFC 8707 参数 | Resource indicator |
| 受众 | token 对之有效的资源 | Audience |
| 逐步授权 | 为额外的当前操作 scope 进行的重新同意与 token 签发 | Step-up |
| 签发方绑定凭证 | 按精确授权服务器 issuer 隔离的注册与 token 记录 | Issuer-bound credentials |

## 延伸阅读

- [MCP 2026-07-28 授权规范](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) — 本课全部规则的权威来源
- [RFC 9728: OAuth 2.0 Protected Resource Metadata](https://www.rfc-editor.org/rfc/rfc9728) — 受保护资源元数据，发现流程的起点
- [RFC 8707: Resource Indicators for OAuth 2.0](https://www.rfc-editor.org/rfc/rfc8707) — 资源指示器，token 受众绑定
- [RFC 9207: OAuth 2.0 Authorization Server Issuer Identification](https://www.rfc-editor.org/rfc/rfc9207) — 授权响应 `iss` 参数，防 issuer 混淆
- [OAuth Client ID Metadata Document 草案](https://datatracker.ietf.org/doc/draft-ietf-oauth-client-id-metadata-document/) — CIMD：以 URL 为客户端标识的新注册机制
