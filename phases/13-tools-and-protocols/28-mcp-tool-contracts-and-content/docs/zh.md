# MCP 工具契约与内容

> 一个工具只有当发现、参数、结果、分页和传输元数据这五处对齐到同一份契约上，才适合交给 AI 自动调用。

> **【中文解读】** 本课基于 MCP 2026-07-28 规范，把一次工具调用拆成五道门禁（发现→准入→调用→执行→消费），逐门讲清校验责任归谁。核心归属：准入和消费两道门归 AI 宿主所有——服务器无法强迫客户端信任自己的注解、schema 或输出。

> **【拓展：MCP→真实生产链路】** 这五道门对应真实 AI 网关的分层：descriptor 校验是网关的"工具准入"，`x-mcp-header` 镜像是负载均衡按区域路由的依据，分页游标是目录同步的基础，completion 是表单自动补全的授权面。Phase 13 · 17（网关与注册中心）和毕业项目都会复用本课的准入核心。

> 🔗 **【前置】** 学本课前请先掌握：Phase 13 · 07（MCP 服务器）、Phase 13 · 09（MCP 传输）、Phase 13 · 10（resources 与 prompts）。

**类型：** 动手实践
**语言：** Python
**前置条件：** Phase 13 · 07、09、10
**预计用时：** 约 120 分钟

## 学习目标

- 用 JSON Schema 2020-12 定义工具的输入与输出。
- 校验结构化结果，而不预设它们一定是 JSON 对象。
- 在文本、图像、音频、资源链接与内嵌资源之间做出选择。
- 在不安全的 `x-mcp-header` 定义到达模型之前把它拒绝掉。
- 对参数-头部值编码，并验证头部与请求体的精确一致性。
- 遍历游标分页而不去解释游标的取值。
- 为 `completion/complete` 补全建议设界并做授权。

## 问题引入

调用一个 Python 函数很容易。通过 AI 宿主调用一个远端能力，则是一个契约问题。

服务器发布 descriptor；客户端把 descriptor 转换为模型上下文和用户界面；模型生成参数；网关可能根据镜像头部路由请求；服务器执行工具；客户端再决定这个结果是否足够安全、足够有效，可以返回给模型。

任何一环的边界松了，整条链都会坏。

设想五种失败：

- descriptor 说结果是对象，服务器却返回数组。
- `nextCursor` 是空字符串时，客户端停止了分页。
- 一个 token 参数被镜像进 HTTP 头，对中间人可见。
- 一个 Unicode 路由值以原始头部发送，网关和源站解释了不同的字节。
- 补全端点向无权访问的调用者建议了生产环境。

这五种失败没有一种能靠"更好的提示词"修复，它们需要显式的协议契约和应用契约。

> **【中文解读】** 链路上有六个角色，任何一环松了全链皆坏。"更好的提示词"修不了契约问题——这是本课与提示工程课程的分界线。

## 契约流水线

把每次工具调用看作五道门：

1. **发现（Discover）。** 读取确定性的、分页的工具列表。
2. **准入（Admit）。** 校验每个 descriptor，并应用本地安全策略。
3. **调用（Invoke）。** 校验参数，构建传输元数据。
4. **执行（Execute）。** 运行处理器，正确分类失败。
5. **消费（Consume）。** 在交给模型使用前校验内容块与结构化输出。

```figure
mcp-contract-pipeline
```

准入和消费两道门归宿主所有。服务器无法强迫客户端信任自己的注解、schema 或输出。

> **【中文解读】** 五道门各有 owner：发现和执行在服务器侧，准入、调用、消费在客户端侧。把校验放错门（比如让服务器自证输出安全）是契约设计的常见错误。

## JSON Schema 是一道运行时边界

在 MCP `2026-07-28` 中，`inputSchema` 与 `outputSchema` 使用 JSON Schema。`$schema` 缺失时默认方言是 2020-12。

输入 schema 必须是一个 schema 对象。没有参数的工具也应精确声明自己接受什么：

```json
{
  "type": "object",
  "additionalProperties": false
}
```

这比 `{ "type": "object" }` 更严，后者会接受任意属性。

输出 schema 是可选的。服务器一旦发布了它，每一个完整工具结果都承诺返回符合该 schema 的 `structuredContent`——包括 `isError: true` 的结果。错误标志只分类执行结果，并不豁免已发布的输出契约。客户端应当校验结果，而不是信任 descriptor。

### 结构化内容可以是任意 JSON 值

不要把 `structuredContent` 硬编码为字典。它可以是：

- 对象；
- 数组；
- 字符串；
- 数字；
- 布尔值；
- `null`。

这个工具返回数组：

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

它的成功结果合法：

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

为了兼容，结构化结果还应在一个文本块里携带序列化的 JSON。但文本不是校验的依据，`structuredContent` 才是。

> **【中文解读】** `structuredContent` 是任意 JSON 值——把它当字典硬编码是本课点名的第一类生产失败。兼容文本块是给旧客户端的，校验永远以 `structuredContent` 为准。

### 一个小校验器照样能教会这道边界

本课刻意使用一个 JSON Schema 子集，以保持在 Python 标准库之内。它校验示例工具用到的机制：

- object、array、string、integer、number、boolean、null 类型；
- required 属性；
- `additionalProperties: false`；
- 数组 items；
- enum 取值；
- 字符串最小长度。

它不是完整生产校验器的替代品。可复用的课程要点是校验发生在哪：descriptor 在发现之后，参数在执行之前，结构化结果在消费之前。

## 内容块各有不同的代价

`content` 数组可以混合多种内容类型。

| 类型 | 用于 | 主要边界 |
|------|------|----------|
| `text` | 人和模型可读的摘要 | 把文本当作不可信输出 |
| `image` | base64 编码的视觉证据 | 校验媒体类型与大小 |
| `audio` | base64 编码的语音或录音输出 | 校验媒体类型与时长上限 |
| `resource_link` | 客户端稍后可获取的 URI | 跟随后的资源读取要重新授权 |
| `resource` | 直接内嵌在结果里的数据 | 当场执行载荷与内容上限 |

资源链接并不证明该资源出现在 `resources/list` 里；它只是本次工具调用返回的一个引用。客户端跟随这个 URI 时，仍然要套用自己的资源策略。

内嵌资源省掉一次往返，但会增大当前响应体积。大件或独立变化的工件用链接；必须与结果原子同行的小证据才用内嵌。

本课的 `evidence_bundle` 结果包含全部五种类型。客户端在接受结果前逐块校验。

> **【中文解读】** 五种内容块各有代价模型：链接省载荷但要"再授权一次"，内嵌保证原子性但撑大响应。安全上要记住两条——文本是不可信输出，资源链接不是授权凭证。

## `x-mcp-header` 是路由元数据

`inputSchema` 里的属性可以声明 `x-mcp-header`。在 Streamable HTTP 上，客户端把该参数镜像为 `Mcp-Param-{name}`。

```json
{
  "region": {
    "type": "string",
    "x-mcp-header": "Region"
  }
}
```

当 `region: "eu-west"` 时，传输层可以发出：

```http
Mcp-Param-Region: eu-west
```

这个注解存在的意义是让负载均衡、网关或策略引擎不解析 JSON 体就能路由。它不是放凭证的地方。

协议对注解的约束：

- 头名非空且符合 HTTP field-name token 语法；
- 头名大小写不敏感地唯一；
- 属性类型是 string、integer 或 boolean；
- 不允许 `number`；
- 注解只能出现在 `inputSchema.properties` 的直接成员上；
- 整数值保持在 `-9007199254740991` 到 `9007199254740991` 之间。

位置规则是语法性的且失败关闭。要遍历整棵 schema 树，而不只是你的校验器恰好认识的那部分属性。嵌套对象的 `properties`、`oneOf` 分支、`items`、经 `$ref` 到达的定义以及任何输出 schema 里的注解都要拒绝——解析一个引用并不会把被引用节点变成直接顶层属性。

本课增加一条部署策略：拒绝镜像 `password`、`secret`、`token`、`api_key`、`authorization` 等名字的 descriptor。官方规范建议服务器作者不要镜像敏感参数；客户端可以把这条建议变成硬性准入规则。

审计头名，不审计值。示例代码记录 `Mcp-Param-Region`，但不把 `eu-west` 写进审计事件。

> **【中文解读】** `x-mcp-header` 的定位是"给中间设备的路由提示"，不是"给凭证的运输通道"。三条硬规则：位置必须顶层直挂、类型限 string/integer/boolean、敏感名字一律拒绝。全树遍历 + 失败关闭是准入校验的正确姿势。

### 构建 HTTP 头之前先对值编码

只有当一个参数值是 `!` 到 `~` 的可见 ASCII 字符组成的非空字符串、且不像编码哨兵时，才能以明文传输。其余一切使用这个精确形式：

```text
=?base64?{Base64UTF8}?=
```

`Base64UTF8` 是对精确 UTF-8 字节的标准 base64。先不要裁剪、归一化或替换值。Unicode、空字符串、空格、制表符、控制字符、CR 或 LF、首尾空白，以及任何以 `=?base64?` 开头的值都要编码。对"长得像哨兵"的值再编码一次，正是接收方能够还原字面原文、而不是当作传输语法解码的关键。

布尔渲染为小写 `true` 或 `false`。整数按十进制渲染，且必须落在 JavaScript 安全整数范围内。范围外的值直接拒绝，而不是让中间人四舍五入。

### 服务器校验镜像副本

生成头部只是客户端这一半。在 Streamable HTTP 边界上，服务器必须：

1. 不区分头名大小写地找出已识别的 `Mcp-Param-*` 名字；
2. 存在时解码精确的 base64 哨兵形式；
3. 把解码文本与 JSON 体中对应参数做精确比较；
4. 在分发之前拒绝缺失、重复、意外、畸形或不匹配的已识别头。

拒绝方式是 HTTP `400` 加 JSON-RPC 错误码 `-32020`。体值和它的编码形式都不属于审计记录，只记录已识别头名和拒绝类别。

`code/main.py` 直接建模了这道边界。[Lesson 09](../../09-mcp-transports/) 覆盖更宽的 Streamable HTTP 校验顺序，包括方法与协议版本一致性。

> 💡 **【类比】** 头体一致性像"快递单与包裹内容对账"：面单（`Mcp-Param-*` 头）是给分拣机（网关）看的，包裹（JSON 体）是给收件人（源站）看的。两边必须逐字节对得上，否则分拣机把货发到 A 仓、收件人却在 B 仓执行——这就是为什么不匹配要在分发前用 `400` + `-32020` 硬拒绝。

## 分页游标是不透明的

MCP 列表操作使用游标分页。页大小和游标格式由服务器选定。客户端只有一个决定：

```python
if result.get("nextCursor") is None:
    break
cursor = result["nextCursor"]
```

不要这样写：

```python
if not result.get("nextCursor"):
    break
```

空字符串是一个合法游标。真值判断会停得太早。

客户端不得解码游标、递增游标、与旧游标比较排序，或推断页码。服务器可以对游标签名、绑定目录版本或映射到私有状态——那是服务器的实现细节。

示例服务器刻意在第一页之后返回 `""`。客户端必须在第二个请求里原样发送这个值。它的 trace 是：

```text
<first request with no cursor>
<second request with cursor "">
```

无效游标产生 JSON-RPC invalid params，错误码 `-32602`。

> **【中文解读】** 游标不透明是一条安全与演进双保险的规则：对客户端它可以是任意字符串（包括空串），对服务器它可以是签名 token 或版本戳。客户端唯一合法的动作是"原样回传或停止"。

## Completion 是一个授权面

`completion/complete` 为 prompt 参数和资源模板参数提供补全建议。它对交互式表单很有用，但可能泄露普通 list 方法保护起来的名字。

一个补全请求指明引用和正在补全的参数：

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

结果最多返回 100 个值，并可以报告 `total` 和 `hasMore`。

对补全请求套用与被引用 prompt 或 resource 相同的授权边界。示例中的 analyst 收到 `development` 和 `staging`，只有 operator 能收到 `production`。

生产级补全还需要：

- 输入校验；
- 按调用者过滤；
- 客户端防抖；
- 服务器限流；
- 有界的结果数；
- 不暴露敏感建议值的日志。

补全是辅助输入，不是绕过发现权限的后门。

> **【中文解读】** completion 最容易被当成"方便的 autocomplete"而漏掉授权。正确姿势：谁能在 `prompts/get` 里看到这个名字，谁才能在补全里看到它。

## 两个错误层

把协议错误与工具执行错误分开。

MCP 请求无法正确分发时使用 JSON-RPC error：

- 未知工具名；
- 请求形状畸形；
- 缺失请求元数据；
- 游标无效。

调用已到达工具、工具报告可行动的失败时，使用 `isError: true` 的完整工具结果：

- 某个报告源不可用；
- 日期超出支持范围；
- 业务规则拒绝请求的操作。

模型往往能修复一个工具执行错误，却无法修复一个违反自身输出 schema 的服务器。

如果工具声明了输出 schema，就把可行动的失败建模在该 schema 之内。示例 `route_report` 的失败返回请求的区域加 `accepted: false`，配人类可读的错误文本和 `isError: true`。

> **【中文解读】** 错误分层的判据是"请求到没到工具"：没到是协议错误（JSON-RPC error），到了但业务失败是工具结果（`isError: true`）。发布过 outputSchema 的工具连失败也要符合 schema——这是 2026-07-28 规范表述的关键点。

## 动手实现

`code/main.py` 用 Python 标准库同时实现边界两侧。

服务器实现：

- 逐请求 MCP 元数据校验；
- 带 tools 与 completions 能力的 `server/discover`；
- 确定性的 `tools/list` 分页；
- 四个工具 descriptor，其中一个必须被拒绝；
- 数组结构化输出；
- 当前全部工具内容块类型；
- 解码已识别参数头、不匹配时返回 HTTP `400` 加 JSON-RPC `-32020` 的 Streamable HTTP 一致性门禁；
- 带授权和限流的补全。

客户端实现：

- descriptor 准入；
- 全树 `x-mcp-header` 位置校验和敏感字段策略；
- 精确的明文可见 ASCII 或 base64 UTF-8 值编码；
- 能跟随空字符串的不透明游标循环；
- 参数与结果校验；
- 内容块校验；
- 只含头名不含值的审计事件。

那个刻意不安全的 descriptor 是教学数据：它证明一个被拒的工具不妨碍其他合法工具加载。

## 学以致用

从仓库根目录：

```bash
cd phases/13-tools-and-protocols/28-mcp-tool-contracts-and-content/code
python3 main.py
python3 -m unittest discover tests -v
```

demo 会打印准入的工具、被拒的 descriptor、两次分页请求、结构化数组内容、内容块类型、镜像头名、值是否需要编码、HTTP 一致性状态，以及按调用者过滤的补全值。

## 交互实验

打开 `code/main.py` 并定位 `TOOLS`。

1. 把 `tag_catalog.outputSchema.type` 从 `array` 改为 `object`。
2. 运行 demo。客户端应当拒绝返回的数组。
3. 恢复 schema。
4. 让第一页的 `nextCursor` 保持 `""`，再让最后一页返回 `nextCursor: None` 而不是省略该字段。
5. 运行测试并比较游标 trace。
6. 给一个字符串属性加 `x-mcp-header: "Authorization"`。
7. 确认 descriptor 准入在调用之前拒绝它。
8. 用包含 Unicode、换行、首尾空格和字面文本 `=?base64?SGVsbG8=?=` 的 `region` 值做实验。解码每个发出的头，证明原值毫发无损地存活。
9. 把注解挪到 `oneOf`、`items` 或 `$ref` 定义之下。确认每个 descriptor 都被拒绝，即使 demo 从不使用那个分支。
10. 删掉已识别头或改掉它的解码值。确认 HTTP 边界返回状态 `400` 和 JSON-RPC 错误码 `-32020`。

要点不是背一个 JSON 形状，而是亲眼看每道门在"拥有它的边界"上失败。

## 进阶练习

给契约实验扩展一个 `search_evidence` 工具。

要求：

1. 输入 schema 接受 `query`、`limit` 和一个安全的 `region` 路由字段。
2. 输出 schema 是含 `uri`、`title`、`score` 的对象数组。
3. 结果包含兼容文本和每项一个资源链接。
4. 参数拒绝未知属性。
5. `limit` 由应用校验设界。
6. 无权访问某 URI 的调用者永远不能通过补全或工具输出看到它。
7. 测试覆盖不合规 score、非法头注解和两页列表。
8. 头值测试覆盖可见 ASCII、Unicode、控制字符、空白、哨兵样文本，以及 JavaScript 安全整数的两个边界。
9. HTTP fixture 大小写不敏感地接受头名，但对缺失或不匹配的已识别值返回状态 `400` 和错误码 `-32020`。

## 产出物

`outputs/skill-mcp-contract-reviewer.md` 是一个扁平、可复用的评审 skill。给它一个工具 descriptor、样例结果、分页行为和补全策略，它会返回准入决定、结果校验计划、头部策略和具体的失败测试。

## 验证

以下陈述全部为真时，本课才算完成：

- `tools/list` 在重复调用时返回相同的逻辑顺序。
- `nextCursor` 为 `""` 时客户端发出第二个请求。
- 不安全的敏感头 descriptor 被排除，其他工具保持可用。
- 数组通过它的数组输出 schema。
- 对象无法通过同一个数组 schema。
- 错误结果不能省略或违反已发布的输出 schema。
- 文本、图像、音频、资源链接与内嵌资源块全部通过校验。
- 审计事件只含头名、不含值。
- 明文保持明文；Unicode、控制字符、带填充、空值和哨兵样的值都能经精确 base64 UTF-8 编码往返。
- 安全整数范围外的镜像整数被拒绝。
- `oneOf`、`items`、嵌套对象、`$ref` 定义或输出 schema 下的注解在准入期间被拒绝。
- 大小写不敏感的已识别头名只有在解码值与请求体精确匹配时才通过；缺失或不匹配的副本产生 HTTP `400` 和 JSON-RPC `-32020`。
- analyst 的补全永远不返回 `production`。
- 工具失败使用 `isError: true`；畸形的协议调用使用 JSON-RPC `error`。

## 生产失败模式

| 失败 | 学习者看到的现象 | 正确响应 |
|------|------------------|----------|
| 客户端预设输出是对象 | 合法的数组失败或被悄悄包装 | 按已发布的 schema 校验，不带"仅对象"类型假设 |
| 空游标被当作假值 | 最后几页消失 | 只要 `nextCursor` 存在且非 null 就继续 |
| 敏感值被镜像 | secret 出现在代理、WAF 或 trace 数据里 | 拒绝该 descriptor，把 secret 留在受保护的请求体数据中 |
| 原始 Unicode 或空白被镜像 | 网关与源站不一致或值被归一化 | 使用精确的 base64 UTF-8 哨兵编码并在解码后比较 |
| 注解藏在 schema 分支里 | 准入时客户端漏掉路由元数据 | 遍历整棵 schema 树，只允许直接顶层属性 |
| 大整数被镜像 | JavaScript 中间人四舍五入了路由值 | 拒绝 JavaScript 安全整数范围外的值 |
| 头与体不一致 | 网关路由到一个目标，源站却执行另一个 | 分发前用 HTTP `400` 和 JSON-RPC `-32020` 拒绝 |
| 输出 schema 被忽略 | 下游代码消费了损坏的结构 | 在模型或应用使用前校验 |
| 资源链接被自动信任 | 调用者跟随了未授权的 URI | 每次资源读取都重新授权 |
| 补全共享全局建议 | 隐藏的租户名泄露 | 按调用者、引用和授权过滤 |
| 工具注解被当作策略 | 破坏性操作绕过确认 | 在注解之外强制执行授权与审批 |
| 一个畸形工具拖垮发现 | 整个服务器不可用 | 拒绝坏的 descriptor，独立准入合法工具 |

> **【中文解读】** 这张表就是一份"代码评审清单"：每一行都是真实事故模式。前三行（预设对象、空游标、敏感值镜像）覆盖了绝大多数生产事故。

## 毕业项目衔接

Phase 13 毕业项目需要一个能合并多台服务器工具的网关，本课提供它的准入核心。

用这个产物给四件毕业证据打分：

- 确定且完整的分页发现；
- 模型暴露之前的 descriptor 校验；
- 校验过的结构化输出加上有界内容块；
- 保持授权边界的补全与路由元数据。

不要只凭一次成功的 `tools/call` 就宣称网关兼容。要捕获 descriptor、分页 trace、准入工具集、拒绝工具集和一个已校验结果。

## 关键术语

| 术语 | 含义 |
|------|------|
| `inputSchema` | 定义工具接受哪些参数的 JSON Schema 对象 |
| `outputSchema` | 定义 `structuredContent` 的可选 JSON Schema |
| `structuredContent` | 工具结果产生的任意 JSON 值 |
| 内容块（Content block） | 类型化的文本、图像、音频、资源链接或内嵌资源 |
| `x-mcp-header` | 把一个原始参数镜像进 Streamable HTTP 元数据的 schema 注解 |
| 不透明游标（Opaque cursor） | 服务器签发的分页 token，客户端不解释其值 |
| 补全引用（Completion reference） | 正在被补全参数的 prompt 名或资源 URI/模板 |
| 准入（Admission） | 客户端暴露或拒绝一个已发现 descriptor 的决定 |

## 延伸阅读

- [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)：工具 schema、结构化输出与 `isError` 语义的规范原文。
- [MCP Completion](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/completion)：补全请求/响应与 100 条上限。
- [MCP Pagination](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/pagination)：不透明游标与 `nextCursor` 语义。
- [MCP Streamable HTTP Parameter Headers](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http#custom-headers-from-tool-parameters)：`Mcp-Param-*` 镜像、类型限制与 base64 哨兵编码。
