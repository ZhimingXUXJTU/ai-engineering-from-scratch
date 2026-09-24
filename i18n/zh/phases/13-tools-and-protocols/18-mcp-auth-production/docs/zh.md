# 发行人绑定注册与代币

> 第16课构建了OAuth 2.1状态机. 这一课加强了MCP 2026-07-28的生产界限:客户端 ID 转化数据文件首先,仅仅用于兼容性,授权-响应发行商验证,发行商密钥的客户身份证,JWKS更新和每个无状态请求的观众印代币.
其他
> **Spec note (2026-07-28):**动态客户端注册被废除以支持客户端ID元数据文件.DCR仍然是一个兼容性机制.当它被使用时,客户端声明正确的`application_type`客户验证现有RFC 9207`iss`授权服务器发行商之间永远不会重复使用凭证.

> **【中文解读】**第16课搭建了OAuth 2.1 状态机;本课把它的边界固化到MCP 2026-07-28 规范的生产要求:注册优先走客户端ID元数据文件(CIMD),DCR 降级为仅作兼容已被废弃路径;授权应对必须校验RFC 9207`iss`根据协议的规定,每一个请求都进行受众绑定检查.

> **【拓展：MCP 2026-07-28 的注册范式转向】**这一版规范从"推" (DCR) 注册.`POST /register`)改为"拉" (CIMD:授权服务器按需拉取客户端自托管的元数据文档),信任从IDP内部状态转移到DNS;同时凭证按发放者隔离、代码按发放者,资源) 转向存储,堵住跨IDP 复用凭证与跨资源重放代币的攻击面.

>  **【前置】**学本课前请先掌握:(1) 阶段 13 · 16 ((OAuth 2.1 状态机、PKCE、资源指示器) 本课是其生产化;(2) 阶段 13 · 17 网关);(3) JWT 结构与 JWKS 概念;(4) 本课将逐步实现规范:RFC 8414(AS 元数据) 、RFC 7591 ((DCR)、RFC 8707 ((资源指示器)、RFC 9728 ((PR 元数据) 、RFC 9207 ((iss参数)、RFC 7636 ((PKCE)、RFC 7662 ((token内省)、RFC 7009 ((token 吊销) ⋅

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 16 (OAuth 2.1 state machine), Phase 13 · 17 (gateways) | **前置知识:** Phase 13 · 16（OAuth 2.1 状态机）、Phase 13 · 17（网关）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## 学习目标

- 通过RFC 8414元数据发现授权服务器,并验证合同.
  中文翻译:通过RFC 8414 元数据发现授权服务器并验证契约。
- 查看客户ID元数据文件,并将废旧的DCR作为回归.
  中文翻译:通过客户端ID元数据文件完成注册,并把已被废弃的DCR隔离为后备路径──
- 验证RFC 9207 `iss`发行者加资源的关键代币.
  中文翻译:校验 RFC 9207 `iss`根据授权服务器签发者做键;资源绑定代币 根据签发者 +资源成做键──
- 按时间表存储和更新JWKS键,以便签名验证存活关键翻转.
  中文翻译:按计划缓存并刷新JWKS 密钥,使签名验证在密钥轮换后仍然活着──
- 通过RFC 8707资源指标将代币粘贴到单个MCP资源上,并拒绝混副本重复使用.
  中文翻译:使用RFC 8707 资源指示器把代币固定在单个MCP 资源中,拒绝混代理式重用──
- 选择JWT验证或代币内检查,定义撤销新鲜度,并在身份依赖不可用时安全失败.
  中文翻译:在 JWT 校验与代币内省之间做出选择,定义取消新鲜度,并依赖身份不可用时安全失败.
- 分开授权服务器,资源服务器和客户端,
  中文翻译:把授权服务器、资源服务器和客户端分开,让每个方只执行自己的检查.
- 审核授权服务器与部署检查清单,拒绝不安全的注册或代币重复使用.
  中文翻译:按部署检查清单审计授权服务器,拒绝不安全的注册或代币 复用.

## 问题 问题引入

> **【中文解读】**三个生产缺口: 1) 注册与凭证隔离CIMD 优先、DCR 仅作兼容,且凭证必须按发放者隔离; 2) 密钥轮换JWKS 缓存必须有刷新任务加回回获取; 3) 受众绑定`token.aud`与资源URL相比,对每个请求的硬性检查也是唯一防跨资源重置的手段.

课16模拟器在内存中运行OAuth 2.1. 制作中有三个操作缺口,仅存储器模拟器无法看到.

> 第十六课 模拟器在内存中运行 OAuth 2.1――生产环境有三个内存模拟器看不到的操作缺陷――

实际的组织可能运行数百个MCP服务器和数千个MCP客户端. 2026-07-28的修订更喜欢一个**Client ID Metadata Document**客户端使用一个HTTPS URL,其路径是其识别符,授权服务器将元数据拉开.RFC 7591动态注册仅仅作为一个过时的兼容路径.当DCR是不可避免的,请求声明正确的`application_type`客户端存储在授权服务器发行商下的注册表和在授权服务器下的访问代币.`(issuer, resource)`换发行商意味着新注册,而不同的资源意味着一个单独的观众的代币.

> 实际组织可能运行数百个MCP服务器和数千个MCP客户端.**Client ID Metadata Document**客户端使用一个自控带路径 HTTPS URL 作为标识符,授权服务器主动取取数据.`application_type`△客户端将信息注册按授权服务器签发者存储,将访问令牌按`(issuer, resource)`发行者必须重新注册;资源不同需要单独绑定受众.

另一个缺口是关键旋转.  JWT验证取决于授权服务器的签字密钥, 作为 JSON Web Key Set (JWKS) 发布. 授权服务器按时间表旋转这些 (通常每小时,有时在事件响应下更快). 通过MCP服务器,一个接收JWKS的启动,直到转换窗口, 产品线程将 JWKS 作为缓存值,更新工作将在前键到期之前覆盖缓存,加上在一个新键签署的代币到达时,缓存错误的缓存.

> 第二个缺点是密钥轮换――JWT 验证依赖授权服务器的签名密钥,以JSON Web Key Set (JWKS) 形式发布――授权服务器按计划轮换这些密钥――通常每小时,事件响应时更快) ――只在启动时获取一次 JWKS 的 MCP 服务器在轮换窗口上出现前验证正常后所有请求都失败,直到重新启动――生产环境将 JWKS 连线为缓存:刷新任务在旧密钥过期覆盖缓存,另加缓存未预期的回归获取,以处理"代码由缓存更新的密钥名"的情况签签――

课程16引入了RFC 8707资源指标.在生产中,该指标成为每一个请求的硬要求检查.`token.aud`根据其自己的规范资源URL,并拒绝与HTTP401的不匹配.这是唯一的防御,以防止上游MCP服务器 (或持有一个服务器的恶意客户端) 将该代币反射到同一信任网中的另一台服务器中.

> 第16课引入了RFC 8707 资源指示器. 在生产中,该指示器成为每个请求的硬性声明检查.`token.aud`与自己的规范资源URL相比,不匹配就像HTTP 401 拒绝.这是保护上游MCP服务器的唯一手段,或者持有发送给某个服务器的代币的恶意客户端) 在同一信任网络内重置代币给另一个服务器.

这一课将每一个空隙映射到一个水面的混凝土块上. 转载数据的数据是HTTP终端.  JWKS缓存更新是一个计划工作加上一个关键值缓存. 资源服务器在发送任何工具之前运行的 JWT验证是例行程序. 保持三个角色分开,每个角色只执行其所有的检查:授权服务器发出和旋转密钥,资源服务器缓存和验证,客户端发现和注册.

> 本课程将每个缺陷映射为认证面上的一个具体组成部分:元数据文档是一个HTTP端点;JWKS 缓存刷新是一个定时任务加一个键值缓存;JWT 验证是资源服务器在分发任何工具之前执行的一个例程.

## 范围:16课后的生产强化

> **【中文解读】**本课不重新定义 OAuth 流程授权码状态机、PKCE、受保护资源发现、资源指示器都属于第16课. 本课从这些协议已经存在后开始:一个部署的资源服务器如何在密钥轮换、不透明的代币、吊销、依赖故障、灰度和事件响应中持续执行这些协议.

[Lesson 16: MCP Security with OAuth 2.1](../../16-mcp-security-oauth-2-1/docs/en.md)授权代码状态机,PKCE,保护资源发现,资源指标和范围决策.本课程并未定义第二个OAuth流.它开始在这些合同存在后,并询问部署的资源服务器如何在关键轮换,不透明代码验证,撤销,依赖性故障,部署和事件响应期间继续执行这些协议.

> [第 16 课：MCP Security with OAuth 2.1](../../16-mcp-security-oauth-2-1/docs/en.md)负责授权码状态机、PKCE、受保护资源发现、资源指示器和范围 决策――本课程不定义第二个OAuth流程――它从这些协议已经存在之后开始,追问已部署的资源服务器如何在密钥轮换、不透明代币 校验、取消、依赖故障、灰度发布和事件响应期间持续执行这些协议――

生产界限较窄,更有效:

> 生产边界更窄,更偏运维:

- 一个JWT路径验证了固定发行者,算法,签名键,观众,时间要求,以及每个请求的范围,同时安全地更新JWKS.
  中文翻译:JWT 路径在每个请求上校验锁定发发件者、算法、签名密钥、受众、时间声明和范围,同时安全更新JWKS。
- 透明的代币路径将调用发行商认证的内视终点,并验证返回的活跃状态,受众或资源,过期期,主题和范围.
  中文翻译:不透明代币 路径调用签发者经认证的内省端点,并校验返回的活跃状态、受众或资源、过期时间、主题和范围──
- 取消政策定义了证书必须停止工作的速度以及哪个缓存可以延迟这一事实.
  中文翻译:吊销策略定义证书必须在很短的时间内失效,以及哪些缓存可以让这一事实拖延.
- 失败政策决定发现,JWKS,内检查或撤销基础设施不可用时发生什么.
  中文翻译:故障策略决定当发现、JWKS、内省或吊销基础设施不可用时该怎么办.
- 证据记录发行者转载的元数据,关键集或内检测响应,代币索赔,政策版本和拒绝理由驱动了结果,而没有存储代币.
  中文翻译:证据记录是哪个发行者元数据,密钥集或内省响应,代币 声明,策略版本和拒绝原因决定结果,但没有存储代币本人.

这种区别使得课程保持可编译性.16课证明了流动性.18课证明,一个代币在达到真正的MCP请求路径后仍然值得信赖,或者被拒绝.

> 这个分工让两个课程保持可组合:第16课证明流程成立;第18课证明一个代币 在达到真实的MCP请求路径后,要么仍然可信、要么被拒绝──

## 概念的核心概念

### 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签

文件`/.well-known/oauth-authorization-server`描述客户需要的一切:

> 位于`/.well-known/oauth-authorization-server`文件描述客户端需要的一切:

```json
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "jwks_uri": "https://auth.example.com/.well-known/jwks.json",
  "client_id_metadata_document_supported": true,
  "registration_endpoint": "https://auth.example.com/register",
  "authorization_response_iss_parameter_supported": true,
  "response_types_supported": ["code"],
  "grant_types_supported": ["authorization_code", "refresh_token"],
  "code_challenge_methods_supported": ["S256"],
  "scopes_supported": ["mcp:tools.read", "mcp:tools.invoke"],
  "token_endpoint_auth_methods_supported": ["none", "private_key_jwt"]
}
```

给一个MCP资源URL链的客户端发现: `oauth-protected-resource`根据RFC 9728 (资源服务器文件) 命名发行者,然后`oauth-authorization-server`客户端从来没有硬码授权URL.

> 获取MCP资源URL的客户端做链式发现:先由RFC 9728 `oauth-protected-resource`标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标签: 标`oauth-authorization-server`客户端从不硬编码授权URL──

对于具有路径的资源识别器,在路径前插入已知段.`https://mcp.example.com/team/server`解决保护资源的元数据`https://mcp.example.com/.well-known/oauth-protected-resource/team/server`附加`/.well-known/...`在资源路径不正确后.

> 对于带路径的资源标识符,要把已知段落插在路径之前.`https://mcp.example.com/team/server`保护资源数据元位于`https://mcp.example.com/.well-known/oauth-protected-resource/team/server`子`/.well-known/...`添加在资源路径后是错误写法.

在信任MCP的IDP之前,你要验证的合同:

> 在信任一个IDP使用MCP之前要验证的契约:

- `code_challenge_methods_supported`包括`S256`规格是明确的:如果这个字段是**absent**授权服务器不支持PKCE和客户端**MUST**拒绝继续.
  翻译: 中文`code_challenge_methods_supported`包含`S256`规范写得明确:该字段**缺失**即表示授权服务器不支持PKCE,客户端**必须**拒绝继续.
- `grant_types_supported`包括`authorization_code`拒绝了`password`其他`implicit`现在,我们要去.
  翻译: 中文`grant_types_supported`包含`authorization_code`并拒绝了`password`和 `implicit`,我知道.
- 至少有一个招生途径:`client_id_metadata_document_supported: true`预注册客户或`registration_endpoint`(RFC 7591相容性已降低).
  中文翻译:至少一条注册路径可用:`client_id_metadata_document_supported: true`预注册的客户端,或`registration_endpoint`(已被废弃的RFC 7591 兼容路径)
- 如果`authorization_response_iss_parameter_supported`客户需要返回的RFC 9207`iss`并且与转向前记录的发行人进行了准确的比较.
  中文翻译:若`authorization_response_iss_parameter_supported`客户端必须要求授权回应返回RFC 9207`iss`发送任何请求前与重定向记录发发送者做出精确比较.
- `response_types_supported`现在,我们在`["code"]`对于OAuth 2.1.
  中文翻译:对 OAuth 2.1,`response_types_supported`恰为`["code"]`,我知道.

如果`S256`如果没有,MCP服务器拒绝部署这个IdP 没有降级模式的PKCE.如果 *没有*注册路径广告,你没有预注册`client_id`您也不能注册; 部署说明书是错误的,不是代码.

> 青春`S256`缺失,MCP 服务器拒绝在此IDP 上部署PKCE 没有降级模式――若两条注册路径都未公布,没有预注册`client_id`错误是部署清单,不是代码.

### 保护资源元数据

第16课涵盖RFC 9728的生产中.该文件是客户端寻找由*这个*MCP服务器所信任的授权服务器的唯一地方.单个MCP服务器可以接受多个IDP的代币 (一个为员工,一个为合作伙伴).RFC 9728声明该集合;RFC 8414记录每个IDP支持什么.

> 第16课讲述了RFC 9728──生产中的增量是:本文档是客户端查找 *此* MCP 服务器信任哪些授权服务器的唯一入口──单个 MCP 服务器可以接受来自多个 IdP的代币 ((一个给员工一个给合作伙伴) ─RFC 9728 声明这个集合;RFC 8414 说明每个 IdP 支持什么──

```json
{
  "resource": "https://notes.example.com",
  "authorization_servers": ["https://auth.example.com", "https://partners.example.com"],
  "scopes_supported": ["mcp:tools.invoke"],
  "bearer_methods_supported": ["header"],
  "resource_documentation": "https://notes.example.com/docs"
}
```

### 客户端ID元数据文件 (建议默认)

> **【中文解读】**客户端使用自己控制的带路由HTTPSURL直接充当`client_id`查看一个JSON元数据文档,授权服务器在OAuth流程中按需拉取──信任是DNS信任`app.example.com`没有登记,没有回来.`client_id`命名空间可耗尽,不需要同步的每个服务器状态.

转换登记从*推*到*拉*.`client_id`客户端使用它控制的HTTPSURL**as**其他`client_id`. URL 归结为 JSON 转载数据文件;授权服务器在 OAuth 流量中按要求获取它.信任根植于 DNS:如果服务器运营商信任 `app.example.com`公司信任客户`https://app.example.com/client.json`没有登记回路,没有`client_id`没有每个服务器状态保持同步.

> 客户端不再要求授权服务器造一个`client_id`直接使用一个 HTTPS URL**充当** `client_id`△该URL 解析到一个JSON元数据文档,授权服务器在OAuth流程中按需拉取它──信任以 DNS为根:如果服务器运营方信任`app.example.com`现在,我在信任.`https://app.example.com/client.json`提供服务的客户端. 没有注册往返,没有可耗尽的.`client_id`命名空间也不需要保持同步的每个服务器状态.

客户端主持的元数据文档:

> 客户端托管的元数据文档:

```json
{
  "client_id": "https://app.example.com/oauth/client.json",
  "client_name": "Example MCP Client",
  "client_uri": "https://app.example.com",
  "application_type": "native",
  "redirect_uris": ["http://127.0.0.1:7333/callback", "http://localhost:7333/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none"
}
```

其他`client_id`文件中的值**MUST**授权服务器确认此情况,拒绝不匹配.`client_id_metadata_document_supported: true`在其RFC 8414元数据中.

> 文档中`client_id`值**必须**授权服务器在RFC 8414 元数据中使用`client_id_metadata_document_supported: true`支持的公众

对于目前的CIMD合同,`client_id`现在`client_name`没有空的`redirect_uris`客户端识别器是绝对的HTTPSURL,具有路径. `application_type`没有复制 DCR 要求`application_type`进入首选CIMD路径.

> 根据目前的CIMD协议,`client_id`,我知道.`client_name`和非空的`redirect_uris`数组是必填项.客户端标识符必须是一个带路径的绝对HTTPSURL.`application_type`虽然可以,但它不是CIMD的必填字段.`application_type`要求照搬进首选的CIMD路径──

两项安全事实,规范是直接的:

> 规范直言不讳的两个安全事实:

- **SSRF.**授权服务器获取攻击者提供的URL. 它必须防范服务器端请求伪造 (不获取内部/管理员终端点).
  翻译: 中文**SSRF。**授权服务器会拉取攻击者提供的URL,必须防御服务器端请求伪造(不得拉取内部/管理端点)
- **localhost impersonation.**单独CIMD不能阻止本地攻击者索取合法的客户端的元数据URL并绑定任何`localhost`转向权限服务器**MUST**在同意期间明确显示转向URI主机名称,**SHOULD**警告我们`localhost`- 只有转向.
  翻译: 中文**localhost 冒充。**仅靠CIMD 不住本地攻击者认领合法客户端的元数据URL并绑定任意`localhost`转向:授权服务器**必须**在同意页面清楚显示转向URI 主机名,并**应当**仅仅`localhost`发出警告.

由于CIMD不需要服务器端状态,因此没有登记器可以像DCR所要求的那样站立.客户端端只能读取:从静态HTTPS端点提供您的元数据文档,然后让授权服务器拉出它.

> 因为CIMD不需要服务器端状态,也没有DCR那样需要架设的注册机.

如果授权服务器运营商已经提供了客户端识别符,在尝试自动注册之前使用发行商范围的注册.否则更喜欢CIMD.只使用已过时的DCR,如果发行商无法使用预注册或CIMD.

> 如果授权服务器运营商已经分配了客户端标识符,应先使用根据发发行人规定的注册,再尝试自动注册――否则优先考虑CIMD――只有当发行人既不能预注册也不能使用CIMD时,才使用已废弃的DCR――

### 标准第7591号:过期兼容性注册

> **【中文解读】**动态客户端注册在2026-07-28 版正式被废弃,仅为无法消费CIMD且预注册不现实授权服务器保留──关键变化:`application_type`不是装饰 回环桌面客户端声明`native`服务器托管客户端声明`web`并使用HTTPS转向URI──三生产陷如旧:按源IP 限流、`software_statement`校验,`registration_access_token`哈希储备

根据2026-07-28的修订,DCR已过时使用.只保留在不能使用CIMD的授权服务器和预注册不实用的地方.

> 已被废弃了. 已无法消费的CIMD,预注册又不现实授权服务器保留它.

```json
POST /register
Content-Type: application/json

{
  "application_type": "native",
  "redirect_uris": ["http://127.0.0.1:7333/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none",
  "scope": "mcp:tools.invoke",
  "client_name": "Cursor",
  "software_id": "com.cursor.cursor",
  "software_version": "0.42.0"
}
```

服务器响应了`client_id`其他`registration_access_token`对于后续更新:

> 服务器以`client_id`和一个供后续更新使用的`registration_access_token`响应:

```json
{
  "client_id": "c_3e7f1a",
  "client_id_issued_at": 1769472000,
  "redirect_uris": ["http://127.0.0.1:7333/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "registration_access_token": "regt_b2...",
  "registration_client_uri": "https://auth.example.com/register/c_3e7f1a"
}
```

`application_type`没有装饰性.一个循环桌面客户端声明`native`;一个服务器托管的客户端声明`web`通过HTTPS转向URI.`token_endpoint_auth_method: none`对于一个公众原生客户来说,这是正确的默认.`client_id`只有PKCE提供了拥有证明.

> `application_type`不是摆设. 回环桌面客户端声明.`native`;服务器托管客户端声明 `web`并使用HTTPS转向URI──`token_endpoint_auth_method: none`是公共原生客户端的正确默认值,它只得到了`client_id`经由PKCE提供持有证据.

生产的三大陷:

> 三个生产陷:

- 没有那么,一个敌对的演员将编写数百万个假注册,`client_id`在注册官处理请求之前,请检查利率限制.
  中文翻译:注册端点必须按源 IP 流量限制.否则恶意行为者可以编写发起数百万假注册,耗尽.`client_id`命名空间――在注册器处理请求之前先跑限流检查――
- `software_statement`课程模拟跳过它;生产线一个验证步骤拒绝任何其他地方的未签名注册转向URI.
  中文翻译:某些企业 IdP 要求 `software_statement`由于不支持本课的注册,
- 其他`registration_access_token`盗窃这个代币意味着攻击者可以重写客户端的转向URI.
  翻译: 中文`registration_access_token`必须以哈希存储,而非明文. 盗窃意味着攻击者可以改写客户端的转向URI.

### 资源指标 (RFC 8707 (重复) 

制作规则:每一个代币请求都包括`resource=<canonical-mcp-url>`并且MCP服务器验证`token.aud`常规的URI是服务器的*最具体*标识符:它使用小字母方案和主机,没有碎片,通常没有后续切片.路径组件是**not**规则 规格在需要识别一个单个MCP服务器时保留它. `https://mcp.example.com`现在`https://mcp.example.com/mcp`现在`https://mcp.example.com:8443`其他`https://mcp.example.com/server/mcp`选择一个每个服务器和`aud`现在,我们在学习时,`https://notes.example.com`简单的说法:一个部署在一个源头下共托几个MCP服务器,以路径来区分它们.

> 第十六课 建立了形态.生产规则:每个标志 请都带`resource=<canonical-mcp-url>`经过每次调用的验证`token.aud`规范 URI 是服务器的*最具体*标识符:方案与主机小写、无碎片、按惯例无尾部斜──路径组件**不**根据规则,需要识别单个MCP服务器时规则将保留它.`https://mcp.example.com`,我知道.`https://mcp.example.com/mcp`,我知道.`https://mcp.example.com:8443`,我知道.`https://mcp.example.com/server/mcp`每个服务器都选择一个,并把它.`aud`精确固定到它――(本课模仿为简洁起见用裸主机受众如`https://notes.example.com`根据不同的方式分辨它们.

### 标准标准 (RFC 7636 (重复)  PKCE

在 OAuth 2.1 中,PKCE是强制性的.课程的授权代码流动始终带有`code_challenge`其他`code_verifier`服务器拒绝任何没有验证器或没有对存储挑战进行哈希的验证器的代币请求.

> 在 OAuth 2.1 中,PKCE是强制性的.本课的授权码流程始终携带.`code_challenge`和 `code_verifier`△服务器拒绝任何缺少验证器或验证器 哈希后与存储的挑战 不符的代币 请求。

### 许可证的配置文件MCP 2026-07-28

> **【中文解读】**2026-07-28 版保持OAuth 资源服务器边界,但把MCP 传输变成无状态:没有可缓存身份决定的协议会话,授权层因此对每个请求独立验证.`Authorization: Bearer`并且每一个要求都必须验证`aud`现在,我们要去.`iss`现在,我们要去.`exp`挑战用`resource_metadata`指针(没有`resource`参数);发现同时接受RFC 8414与OIDC发现;混合在客户端的防御;;RFC 9207);凭证按发言人隔离;CIMD 优先、DCR 已被弃用──

目前的MCP修订保持了OAuth资源服务器边界,同时使MCP运输无状态.没有协议会议可缓存身份决定.因此,授权层独立验证每个请求:

> 当前MCP修订版保持OAuth 资源服务器边界,同时把MCP 传输变为无状态――没有可以用来缓存身份决定的协议会话,授权层因此对每个请求进行独立验证:

- 执行RFC 9728保护资源的元数据,并通过 `WWW-Authenticate: Bearer resource_metadata="..."`标题在401号**or**已知的URI`/.well-known/oauth-protected-resource`(SEP-985使头条可选,已知倒退).`authorization_servers`领域**MUST**提名至少一个服务器.
  中文翻译:实现RFC 9728受保护资源元数据,其位置要么通过 401 上的 `WWW-Authenticate: Bearer resource_metadata="..."`头给给出,**要么**用已知的URI`/.well-known/oauth-protected-resource`(SEP-985 把该头变为可选并配备已知回退) ⋅元数据的`authorization_servers`字段**必须**至少列出一个服务器.
- 仅通过 `Authorization: Bearer ...`现在**every**从来没有在查询链中,从来没有仅在会议开始时验证.
  中文翻译:只在**每个**求上经`Authorization: Bearer ...`接受代币绝不放进查询串,绝不能只在会话开始时验证一次.
- 验证`aud`现在`iss`现在`exp`服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器 服务器**MUST**确认该代币是专门发行给它 (观众); 缺失或不匹配`aud`没有被拒绝,从来没有被视为牌.
  中文翻译:每个请求都验证`aud`,我知道.`iss`,我知道.`exp`和必需的范围──服务器**必须**验证代币是专门发送的(受众);`aud`缺失或不匹配一律拒绝,绝不当作通配符.
- 在401/403回来`WWW-Authenticate: Bearer`运输`error=...`其他`resource_metadata="<PRM-URL>"`参数 (元数据文档的URL, *不是*空格资源),以及`scope="..."`现在`insufficient_scope`(403). 注:参数是`resource_metadata`没有发现的指标`resource`挑战中的参数.
  中文翻译:在401/403 上返回 `WWW-Authenticate: Bearer`携带`error=...`,我知道.`resource_metadata="<PRM-URL>"`参数(元数据文档的URL,*而非*裸资源),403 的 `insufficient_scope`再加上`scope="..."`◎注意:该参数叫`resource_metadata`没有发现的挑战`resource`参数.
- 授权服务器发现接受**either**标签: 标签: 标签: 标签: 标签: 标签:**or**客户端必须以优先顺序尝试两个已知后尾.
  中文翻译:授权服务器发现**既**接受RFC 8414 OAuth 元数据,**也**接受OpenID Connect Discovery 1.0;客户端必须按优先级次尝试两种已知后──
- 客户端 (而不是服务器) 防御**mix-up attacks**报告预期的情况`issuer`在转向并验证`iss`仅仅PKCE不停止混,因为客户端交给其 `code_verifier`无论它是什么标志性的目的地.
  翻译: 中文**mix-up 攻击**客户端 (而不是服务器) 防御:重定向前记录预期的`issuer`之前的实验实验授权响应中返回的`iss`值(RFC 9207) △仅靠PKCE 不住混,因为客户端会把`code_verifier`交给它被带走的标志 端点.
- 如果发现解决了另一个发行商,客户重新注册,而不是呈现旧的 `client_id`登记代币或访问代币.
  中文翻译:一个客户端凭证只属于授权服务器发发发行人.`client_id`、注册代币或访问代币 去硬──
- 根据CIMD的规定,CIMD是最喜欢的注册机制.`application_type`现在,我们要去.
  中文翻译:CIMD 是首选注册机制──DCR已被废弃;兼容的DCR 请求仍要声明正确的`application_type`,我知道.

标题:OAuth 2.1草案是基板;RFC 8414/7591/8707/9728/9207 +RFC 7636 +CIMD是表面;MCP规格是配置文件.

> 根据"中共"的规定,该委员会将对"中共"的规定进行审核.

### 部署能力检查列表

查看您实际部署的授权服务器返回的元数据. 门是机械的:

> 厂商功能表很快过期. 改为检查你实际部署的授权服务器回归元数据.

| Check | Required decision |
|---|---|
| Discovered issuer | Exact HTTPS issuer expected by policy |
| PKCE | `S256` advertised; otherwise stop |
| Enrollment | CIMD preferred, pre-registration accepted, DCR only as deprecated compatibility |
| Authorization response | Validate RFC 9207 `iss` when present or advertised |
| Resource binding | Token request carries `resource`; resource server requires the matching `aud` |
| Credential storage | Key client IDs and registration credentials by issuer; key access tokens by issuer plus resource |
| DCR compatibility | Declare `native` or `web`; reject redirect URIs that do not fit the declared application type |

没有从产品名称或定价层推断支持. 在部署证据中捕获发现的文件,并在缺失强制性字段时关闭.

> 没有产品名称或定价档推断支持能力.

###  JWKS 更新模式 (在AS 旋转,在资源服务器更新)

> **【中文解读】**区分两个动词:**轮换（rotate）**是授权服务器的新密钥,发布到 JWKS,**刷新（refresh）**是资源服务器唯一能做的事重新 GET 已发布的 JWKS 进入缓存.`kid`未命中时做**一次**同步刷新作回归回复查.回归必须是"再拉取"等,绝不能是"轮换并造"后者既造不出缺失.`kid`现在还会随时被抓住`kid`标志 喷射打成自伤式DoS──

两个动词分开,因为把它们混在一起是真正的生产错误:

> 把两个动词分开,混用它们是真实的生产错误:

- **Rotate**资源服务器没有参与,也不能这样做.它不保留IdP的私钥.
  翻译: 中文**轮换**是*授权服务器*做的事:造新签名密钥,发布到 JWKS 之后退役旧密钥――资源服务器与此无关也没有做到它没有IDP的私钥――
- **Refresh**资源服务器做什么:`GET`资源服务器所执行的唯一的JWKS操作.
  翻译: 中文**刷新**是*资源服务器*做的事:重新 `GET`已发布的 JWKS 进入缓存.

产品故障模式是旧缓存. 通过计划更新工作加上关键值缓存来解决.资源服务器运行一个工作 (cron,计时器,无论运行时间提供什么) 在固定间隔上,检索`<issuer>/.well-known/jwks.json`子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子,子.`cache[issuer] = {keys, fetched_at}`验证器可以从缓存中读取.`kid`缓存触发器中没有找到**one**交代更新作为倒退,然后重新检查. 这一次处理两个情况:计划更新,和重叠键窗口,一个新钥匙签署的代币在下一个计划更新之前到达.

> 生产故障模式是缓存过期. 用一个定时刷新任务加一个关键值缓存解决.资源服务器运行一个作业.`<issuer>/.well-known/jwks.json`覆盖`cache[issuer] = {keys, fetched_at}`△验证器从该缓存读取──某个代币的`kid`没有存储,触发**一次**同步刷新作为回归,然后复查. 这同时涵盖两种情况:计划内刷新,以及"全新密钥签名的代币在下一次计划刷新之前到达"的密钥重叠窗口.

倒的情况**must be a re-fetch, never a rotate**如果把缓存错误路径转换到旋转和,两件事就会发生破裂: (1) 造一个新钥匙会产生一个`kid`并且 (2) 攻击者将随机喷代币`kid`值得一提的是,它需要一个无限的系列的关键创作.`kid`总的来说,这只钱最多是一个浪费的.

> 回退**必须是重新拉取，绝不许是轮换**如果把缓存未预期的路径到"轮换并造",会坏两件事:`kid`现在还没有匹配,查找照样失败;`kid`喷射代币,逼出无限的密钥创建自伤式DoS──重新拉取是等等,伪造的`kid`最多浪费一次拉取.

缓存形状:

> 缓存形态:

```json
{
  "https://auth.example.com": {
    "keys": [
      {"kid": "k_2026_03", "kty": "RSA", "n": "...", "e": "AQAB", "alg": "RS256", "use": "sig"},
      {"kid": "k_2026_04", "kty": "RSA", "n": "...", "e": "AQAB", "alg": "RS256", "use": "sig"}
    ],
    "fetched_at": 1772668800
  }
}
```

权限服务器通过输入下一个键 (`k_2026_04`) 在退休之前 (`k_2026_03`),因此在旧密钥下发行的代币仍然有效,直到它们到期.缓存存储存储会保持联盟;验证器选择通过`kid`现在,我们要去.

> 同时持有两个密钥是稳定的.`k_2026_04`),再退役前一个(`k_2026_03`),因此旧密钥签发的代币在过期前仍然有效.`kid`选用.

>  **【类比】** JWKS 刷新像消防站的密码本.授权局. 消防局. 定期换密码. 各消防站. 消防站. 服务器. 必须人手一册最新密码本.否则夜间演习.

### 验证程序

在发送任何工具之前,MCP服务器执行验证.`code/main.py`使用:

> 服务器在分发任何工具之前先运行验证.`code/main.py`的形态:

```python
result = server.validate(bearer_token, required_scope="mcp:tools.invoke")
if not result["valid"]:
    return {"status": result["status"], "WWW-Authenticate": result["www_authenticate"]}
```

`validate`解码JWT,从JWKS缓存中解决签名密钥 (一次更新一次错误),验证签名,然后检查`iss`针对允许清单,`aud`对于这个服务器的可信资源,`exp`返回一个 `WWW-Authenticate`资源服务器上保持一个常规的程序意味着每个入口点 (每个工具调用,每个运输) 都会经历相同的检查;没有通路可以先验证到一个工具.

> `validate`解码 JWT,从 JWKS 缓存解析签名密钥(未命中时刷新一次),验证签名,然后把 `iss`为了允许列表`aud`对照本服务器规范资源再查`exp`首先失败即回归`WWW-Authenticate`挑战――将其作为资源服务器上的单一程序,意味着每个入口,每个调用工具,每个传输都经历了相同的检查;没有未经验的方法来触及工具――

### 形的代币使用内观,而不是猜测

> **【中文解读】**不是所有访问代币都是JWT.发行者若发布不透明代币,资源服务器无法解码可信声明,必须将代币经认证的后端通道送到发行者的RFC 7662 内省端点,要求.`active: true`、预期发发件人下文、精确的MCP受众或资源、未过期时间和该工具所需的范围──缓存按"发发件人+代币 单向摘要+MCP资源"做键,绝不需要明文代币做日志或缓存标签──验证模式不能由代币 内容决定攻击者可控的内容不能选择验证路径──

不是每个访问代币都是JWT. 如果发行商记录一个不透明的代币,资源服务器无法将其解码成可信的索赔.它通过认证后道将代币发送到发行商的RFC 7662内观终端点,并要求`active: true`预期发行商的背景,MCP的确切受众或资源,未到期的时间索赔,以及具体工具所需的范围.

> 不是每个访问代币都是JWT. 如果发发行者发布了一个不透明的代币,资源服务器无法将其解码为可信声明. 它将代币经认证的后端通道发送到发发发发行者的RFC 7662 内省端点,并要求`active: true`、预期发行人下文、精确的MCP受访者或资源、未过期时间声明,以及该具体工具所需的范围──

发行者进行缓存内省,单向代币消化,以及MCP资源. 永远不要使用清晰的代币作为日志或缓存标签. 按代币最早的期限,发行商的缓存指导,以及部署的撤销新鲜度目标绑定一个正确的缓存输入. 保持负面缓存时间短以免新发行的代币保持虚假的不活跃. 一个资源的结果不能授权另一个资源,即使不透明的代币字符串是相同的.

> 内省缓存按发行者、代币 单向摘要和MCP 资源做键──绝对不用明文代币 当日志或缓存标签──正向缓存条目的有效期取"代币 过期时间、发行者缓存指引、部署的吊销新鲜度目标"三者中最早的──负向缓存要足够短,以免新发行的代币被误判为不活跃──针对某个资源权内省结果不能授予另一个资源即使不透明 字符串完全相同──

通过攻击者控制的代币内容,不要选择验证模式. 印JWT与内视行为,并验证发行者元数据和部署配置.在JWT路径上,印接受算法和可信`jwks_uri`;永远不要遵循仅仅由代币标题选择的关键URL或算法.

> 根据攻击者可控的代币 内容选择验证模式. 让"JWT 还是内省"钉死在已验证的发发射者数据和部署配置上.`jwks_uri`绝对不仅仅由代币指定的关键URL或算法.

### 撤销是一项新鲜度合同

根据RFC 7009,客户端可以要求授权服务器撤销代币.该请求不会删除每个资源服务器已经缓存的副本.定义最大可接受的撤销延迟,并使每个缓存都尊重它.

> 客户端请求允许客户端请求授权服务器吊销代币.但该请求不会删除已被每个资源服务器缓存的副本.

通过对高风险的每次通话进行内视或使用短暂的正面缓存,可实现更严格的撤销. 独立的JWT部署通常结合短暂的访问代币使用寿命,更新代币撤销,发行商范围内的事件的关键退休,以及紧急局部拒绝的可选主题,会议或代币身份证分类列表. 签署的JWT将在截止日期内保持加密有效性,除非资源服务器有当前外部撤销证据.

> 不透明代币部署可用于每次高风险调用都内省或使用短正向缓存,实现更紧密的吊销.自含 JWT 部署通常组合使用:短访问代币 有效期+更新代币吊销.面向全发发件事件的关键退役,以及应急本地拒绝使用主题/会议/代币-ID 列表.签署的 JWT 在过期前密码学上始终有效,除非资源服务器持有当前外部吊销证据.

登录,帐户禁用,同意撤销和事件响应是不同的触发因素,但必须与一个可测量的声明相结合:在宣布撤销窗口之后,每个复制都拒绝了凭证.通过负载平衡器测试该声明,不仅仅对一个热过程进行测试.

> 登录,账号停用,撤销同意和事件响应是不同的触发器,但必须收到一个可量的陈述:在声明的取消窗口之后,每个副本都拒绝了该证书.

### 依赖性失败需要宣布的决定

> **【中文解读】**可用性策略不能在异常处理器里即兴发挥.表格给出6类依赖故障的安全生产行为.`kid`且唯一回退失败→拒绝;内省不可用→失败关闭;元数据意外变更→停止新注册;吊销端点不可用→如实报告未完成;时钟源或声明类型无效→拒绝而非放宽偏差) ◎依赖故障与无效证书必须分类:前者是带健康和重试策略运维错误,后者是授权拒绝都无法处理工具,也不能把代币内容泄露到审计证书中.

永远不要在例外处理器内即兴化可用性政策.

> 绝对没有异常处理器即兴制定可用性策略.

| Failure | Safe production behavior |
|---|---|
| Scheduled JWKS refresh fails, known `kid` remains in a still-valid bounded cache | Continue only within the declared stale-on-error window and emit degraded health evidence |
| Token has an unknown `kid` and the one allowed refresh fails | Reject; never accept an unverifiable signature |
| Introspection is unavailable | Fail closed for protected calls; do not convert network failure into `active: true` |
| Protected-resource or issuer metadata changes unexpectedly | Stop new enrollment and token acquisition; keep only explicitly pinned, unexpired configuration under a bounded incident policy |
| Revocation endpoint is unavailable | Report logout or revocation as incomplete, retain the credential locally as unusable when possible, and do not claim global revocation succeeded |
| Clock source or claim type is invalid | Reject rather than widening skew until the token passes |

根据"安全性"的规定,使用者必须将数据丢失,并将数据丢失. 根据"安全性"的规定,使用者必须将数据丢失. 根据"安全性"的规定,使用者必须将数据丢失.

> 依赖故障与无效证分为开类.依赖中断是带健康和重试策略的运维错误;坏的签名,发行者,受访者,过期时间或范围是授权拒绝.

### 观众重播通行 (访问符号权限限制)

> **【中文解读】**受众重放演练:服务器 A(notes.example.com) 与服务器 B(tasks.example.com) 注册到同一授权服务器; 被攻击后攻击者拿用户的注释代币 去敲 B。B 的验证器在第三步检查`aud == "https://tasks.example.com"`失败,返回 401 并带`resource_metadata`标志:受访者声明是协议层对此类攻击的唯一防御**access-token privilege restriction**服务器`MUST`拒绝任何受众里没有点它名字的代币――注意术语:*困惑副官* 留给了另一个问题MCP 代理使用静态客户ID 转发代币 且未获得每个客户端的同意――

服务器A (`notes.example.com`) 和服务器B (`tasks.example.com`) 两者都会登录在同一授权服务器上.服务器A被破坏.攻击者取取用户的笔记符号并将其反弹到服务器B.

> 服务器 A`notes.example.com`)与服务器 B`tasks.example.com`攻击者获取用户的注册代币并转向B的服务器重放.

服务器B的验证器:

> 服务器B 的验证器:

1. 解码JWT,通过JWKS来获取`kid`检查签名.
  中文翻译:解码 JWT,按 `kid`取 JWKS,验证签名.
2. 查看`iss`对于其保护资源的元数据`authorization_servers`通过同一名人.
  中文翻译:把 `iss`根据其受保护资源数据`authorization_servers`〔(通过同一的IDP〕
3. 查看`aud == "https://tasks.example.com"`没有成功的代币.`aud`是`https://notes.example.com`)
  中文翻译:检查 `aud == "https://tasks.example.com"`败发的`aud`是 `https://notes.example.com`〔一〕
4. 返回401号`WWW-Authenticate: Bearer error="invalid_token", error_description="audience mismatch", resource_metadata="https://tasks.example.com/.well-known/oauth-protected-resource"`现在,我们要去.
  中文翻译:返回401,带 `WWW-Authenticate: Bearer error="invalid_token", error_description="audience mismatch", resource_metadata="https://tasks.example.com/.well-known/oauth-protected-resource"`,我知道.

观众声称是协议层的唯一防御措施. 为了性能而跳过它是最常见的生产错误;验证器必须在每个请求上运行,而不仅仅是会议开始. 规格称这是**access-token privilege restriction**:一个MCP服务器`MUST`拒绝任何在观众中不提名的标志.

> 接受声明是协议层防御攻击的唯一手段. 为了性能跳跃,它是最常见的生产错误;验证器必须在每个请求上运行,而不是仅仅在会议开始时.**access-token privilege restriction**(访问代币特权限制):MCP 服务器 `MUST`拒绝任何受众中未点名的标志.

> **Naming note.**规格保留了"混副"这个词,用于一个相关但明显的问题:一个作为OAuth的MCP服务器**proxy**通过使用静态客户端ID,将代币转发到第三方API上,而不会获得每个客户端用户同意.观众绑定修复了上述重播;混副级修复是每个客户端同意.**plus**没有通过输入代币到上游API (MCP服务器)`MUST`获得自己的独立上游代币).

### 混合攻击 (服务器无法提供客户端防御)

客户端可以在其一生中与许多授权服务器交谈.恶意AS可以试图让客户端在攻击者的代币终端点赎回诚实的AS授权代码.观众绑定在这里并没有帮助.

> 客户端一生会与许多授权服务器交往.恶意AS可以设法让客户端把诚实AS的授权码拿到攻击者的代币.

1. 在转向之前,客户记录预期的`issuer`根据验证的AS元数据.
  中文翻译:重定向之前,客户端从已验证的AS 元数据记录预期的 `issuer`,我知道.
2. 在授权回复上,客户将返回的回复进行比较.`iss`在任何地方发送代码之前,对记录发行者进行参数 (简单的字符串比较,没有正常化).
  中文翻译:收到授权响应时,客户端在任何地方发送代码 之前,把返回的 `iss`参数与记录的发发言人比对
3. 失匹配 (或 `iss`在AS广告时缺席`authorization_response_iss_parameter_supported`拒绝,甚至不显示`error`其他地方
  中文翻译:不匹配(或AS 已公布 `authorization_response_iss_parameter_supported`却缺少了`iss`)→ 拒绝,连 `error`字段都不要展示――

客户提供了其 `code_verifier`由于此,规格每次要求记录发行者与PKCE验证器一起,`state`现在,我们要去.

> 只有PKCE 不住混,因为客户端会把`code_verifier`交给被引入的代币端点. 这正是签发者和PKCE验证器的规范.`state`一起根据请求记录的原因.

### 失败模式

- **Stale JWKS.**验证器在AS旋转键后拒绝有效代币. 修正是 cron-refresh + cache-miss-refetch 模式. 永远不要在更新工作的情况下缓存 JWKS.
  翻译: 中文**过期 JWKS。**修复是上述定时刷新+未预期重拉模式――绝对没有刷新任务的情况下缓存 JWKS――
- **Rotate-as-fall-back.**转换缓存错误路径到转换的路径,`kid`攻击者控制了它`kid`值值在关键创建DoS. 倒退必须是无权的`refresh-jwks`现在,我们要去.
  翻译: 中文**把轮换当回退。**缓存未定的路径到"轮换并造"而不是重新拉取是真实的错误:它永远不会产生失踪.`kid`攻击者也会被控制.`kid`值变成密钥创建DoS──回退必须是等等等`refresh-jwks`,我知道.
- **Missing `aud` claim.**一些IDP默认省略`aud`除非`resource`验证者必须拒绝缺失的代币.`aud`没有人会把缺席视为一个狂欢的卡片.
  翻译: 中文**缺失 `aud` 声明。**某些IDP默认省略`aud`除非标志请求中带了`resource`△验证器必须拒绝缺失`aud`没有什么可谓的符号.
- **Mix-up via missing `iss` check.**没有验证RFC 9207的客户端`iss`权限响应参数对发行者进行转向之前记录的权限响应参数可以被引导到攻击者的代币终端点中赎回诚实的AS代码.这是客户端故障;资源服务器无法补偿它.
  翻译: 中文**缺 `iss` 检查导致 mix-up。**不把RFC 9207 `iss`授权响应参数与重定向前记录的发发件者比对客户端,可能被引入攻击者的代码端点去换诚实AS.
- **Scope upgrade race.**两个同时进行的加大流程可以成功并产生两个具有不同范围的访问令牌.验证器必须使用在请求中呈现的令牌,而不是搜索"用户的当前范围",从而创建一个TOCTOU窗口.
  翻译: 中文**scope 升级竞态。**同一个用户的两个发发动步骤流程都可能成功,产生两个范围不同的访问代币――验证器必须使用请求上呈现的代币,而不是去查看"用户当前的范围"那将打开TOCTOU窗口――
- **Registration token theft.**一个泄露的`registration_access_token`让攻击者重新写转向URI. 按住这些,要求客户端在每次更新中呈现清晰文本; 根据怀疑旋转.
  翻译: 中文**注册 token 被盗。**泄漏的`registration_access_token`让攻击者可以改写转向URI──静态哈希存储;要求客户端每次更新显示明文;一有怀疑就轮换──
- **`iss` not pinned.**验证器可以接受任何`iss`攻击者可以建立自己的授权服务器,注册客户端,并发行代币.`authorization_servers`允许的列表是允许的列表;
  翻译: 中文**`iss` 未锁定。**接受任何事`iss`证实器将让攻击者自建授权服务器,以实现受众注册客户端并发送代币.`authorization_servers`列表就是允许列表;强制执行它.
- **Credential or token cache collision.**客户端只通过资源进行注册,可以向另一个提交一个授权服务器的身份.客户端只通过发行商进行访问令牌的密钥可以在错误的受众中重播一个令牌.`(issuer, resource)`任何发行者改变时,
  翻译: 中文**凭证或 token 缓存碰撞。**根据资源给注册的客户端,将授权服务器的身份转移给另一个;只根据发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发`(issuer, resource)`签发者一变就重新注册.

```figure
t3-jwks-rotate
```

## 用它实现框架

> **【中文解读】** `code/main.py`用标准库 Python 和三个角色`AuthorizationServer`,我知道.`ResourceServer`,我知道.`Client`)走完整生产流程:发布RFC 8414 元数据 → 检查注册选项与S256 → 优先发行商级预注册/CIMD、DCR 单独可测 → 记录签发者并校验授权响应`iss`→ PKCE + RFC 8707 资源指示器 → 载体调用工具 → JWKS 缓存验证 → 密钥轮换后无需重启继续验证 → 受众重放得到 401。

`code/main.py`通过Stdlib Python和三个角色进行了整个生产流程: `AuthorizationServer`现在`ResourceServer`其他`Client`流量:

> `code/main.py`用标准库 Python 和三个角色`AuthorizationServer`,我知道.`ResourceServer`,我知道.`Client`走完整的生产流程――流程:

从存储库根,运行:

> 在仓库根目录运行:

```bash
cd phases/13-tools-and-protocols/18-mcp-auth-production
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

第一个命令打印了发行商的注册和符号验证
另一个报告18个通过检查.
网络听者或写信件.

> 第一个条 印签发人绑定注册与代币验证记录 第二条 报告18条通过检查 二条 命令都不开网监听、不写入凭证――

1. 授权服务器将RFC 8414的元数据发布在 `/.well-known/oauth-authorization-server`现在,我们要去.
  中文翻译:授权服务器在`/.well-known/oauth-authorization-server`发布RFC 8414 元数据──
2.  MCP 客户端调用元数据终端点并检查其注册选项 (`client_id_metadata_document_supported`对于CIMD,`registration_endpoint`对于DCR) 和`S256`支持PKCE.
  中文翻译:MCP 客户端调用元数据端点,检查注册选项(CIMD 看 `client_id_metadata_document_supported`,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,`registration_endpoint`) 与`S256`支持的.
3. 客户端检查是否有发行商预先注册,否则会使用HTTPS客户端身份证元数据文件注册. 退化DCR仍然是一个可以单独测试的兼容性方法.
  中文翻译:客户端先查按签发者划定的预注册,否则使用其HTTPS客户端ID元数据文档注册──已被废弃的DCR 仍保留为可单独测试的兼容方法──
4. 客户记录验证发行商,创建S256挑战,获得一次性授权代码加上`iss`通过原始验证器和RFC 8707 验证返回发行商的代码.`resource`标志性
  中文翻译:客户端记录已验证的签发者,创建S256挑战,获得一次性授权码和 `iss`检查返回发件人,再使用原始验证器和RFC 8707 `resource`指示器换代码
5.  MCP 客户端调用一个工具在 MCP 服务器上`Authorization: Bearer ...`现在,我们要去.
  中文翻译:MCP客户端以`Authorization: Bearer ...`调用MCP服务器上的工具――
6.  MCP服务器运行`validate`通过JWKS缓存的签字密钥来解决问题.
  中文翻译:MCP 服务器运行 `validate`通过 JWKS 缓存解析签名密钥.
7.  IdP 旋转一个键; 计划更新将JWKS重新拉入缓存中.
  中文翻译:IdP 轮换一个密钥;定时刷新把 JWKS 重新拉进缓存――
8. 下一次调用会根据更新的键进行验证,而之前的代币仍然在重叠窗口中进行验证.
  中文翻译:下一次调用无需重启即针对刷新后的密钥验证,且旧代币在重叠窗口内仍然有效.
9. 试图反弹观众的 MCP 资源得到了 401 的`audience mismatch`其他`resource_metadata`标志.
  中文翻译:针对另一个MCP资源的受众重放尝试得到401,带 `audience mismatch`和 `resource_metadata`针

在此,JWT使用HS256与共享秘密 (因此课程仅运行在stdlib上).制作使用RS256或EdDSA与上述JWKS模式;验证逻辑是相同的.因为IdP和资源服务器生活在一个过程中,`refresh_jwks`直接阅读授权服务器的关键列表;通过线程,它是一个HTTP `GET`为了`jwks_uri`现在,我们要去.

> 在这里,JWT使用HS256加共享密钥 (使本课仅运行在标准库上) .生产使用RS256或EdDSA加上述JWKS模式;验证逻辑其余完全相同.`refresh_jwks`直接读授权服务器的密钥表;走线缆时它就是对`jwks_uri`一次的HTTP`GET`,我知道.

## 运送它.

这一课产生了`outputs/skill-mcp-auth.md`鉴于MCP服务器配置和IdP能力组件,该技能会发射出站立的Auth表面保护资源的元数据,使用的注册路径 (CIMD,预注册或DCR倒退),JWKS更新时间表,范围映射和拒绝适用的规则,当IdP不支持完整的RFC配置文件.

> 本课产出发 `outputs/skill-mcp-auth.md`△给定MCP 服务器配置和IDP 能力集,该技能生长需要架设的认证面受保护资源元数据、该使用的注册路径(CIMD、预注册或DCR 后备)、JWKS 刷新计划、范围 映射,以及IDP不满足完整的RFC 配置时的拒绝规则──

## 练习题

1. 跑步`code/main.py`观察如何在第6步中旋转键,`refresh_jwks`重新拉出已发布的集,既旧的代币 (重叠窗口),又新的代币都在重新启动的情况下验证.
   中文翻译:运行 `code/main.py`关注第6步 IdP 如何轮换密钥、定时`refresh_jwks`如何重启已发布的密钥集以及旧代币 (如何重叠窗口) 和新代币

2. 添加一个新的IDP到保护资源的元数据`authorization_servers`发行一个签署的代币,并确认验证者接受它.发行一个签署的代币,并确认验证者拒绝.`WWW-Authenticate: Bearer error="invalid_token", error_description="iss not allowed"`现在,我们要去.
   中文翻译:向受保护资源元数据的`authorization_servers`列表添加新IDP──签发一个由新IDP签署的代币,确认验证器接受;再签发一个未列出的IDP签署的代币,确认验证器以`WWW-Authenticate: Bearer error="invalid_token", error_description="iss not allowed"`拒绝了.

3. 添加一个利率限制检查`register_client`使用一个每个源 IP 存储在一个小键键键的IP.
   中文翻译:给`register_client`加入一个在注册器接受请求之前运行的限流检查――使用按源IP做键的小字典实现每一个IP让牌桶――

4. 阅读RFC 7591并确定课程的两个领域`/register`处理器不验证. 添加验证.`software_statement`其他`redirect_uris`美国的"URI"计划
   中文翻译:阅读RFC 7591,找出本课 `/register`处理器未验证的两个字段并补上验证――(提示:`software_statement`与`redirect_uris`它们的使用方式

5. 确认客户端存储了单独的发行商密钥注册,拒绝重复使用第一个发行商的代币或`client_id`现在,我们要去.
   中文翻译:添加第二个授权服务器──确认客户端存储独立按发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发`client_id`,我知道.

6. 证明了DoS的修正,向验证器发送一个随机的代币.`kid`确认`refresh_jwks`之后,故意将下跌回转换为旋转和,然后看看按假代币的重复回收.
   中文翻译:证明 DoS 修复――给验证器送一个随机 `kid`标志,确认`refresh_jwks`至多运行一次并授权服务器的密钥数量不增加.然后故意把重改接到"轮换并造",看密钥数量随着每个伪造代币上升最后恢复重新拉取.

7. 炼了两者都不适用`native`其他`web`确认一个 HTTP 转向URI的 Web 客户端,而一个没有精确的循环回转向的本地客户端则被拒绝.
   中文翻译:用`native`和 `web`两种客户端演练已被废弃的DCR──确认带HTTP转向URI的网页客户端与没有精确回环转向的本地客户端都被拒绝──

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| ASM | "OAuth metadata document" | RFC 8414 `/.well-known/oauth-authorization-server` JSON |
| CIMD | "Client metadata URL" | Client ID Metadata Document: an HTTPS URL used as the `client_id`; the AS pulls the JSON. Preferred enrollment in MCP 2026-07-28 |
| DCR | "Self-service client registration" | RFC 7591 `POST /register`; deprecated for current MCP and retained only for compatibility |
| JWKS | "Public keys for JWT validation" | JSON Web Key Set, fetched from `jwks_uri`, indexed by `kid` |
| Rotate vs refresh | "Updating the keys" | *Rotate* = AS mints/retires signing keys; *refresh* = resource server re-fetches the published set. Resource servers only ever refresh |
| Resource indicator | "Audience parameter" | RFC 8707 `resource` parameter pinning the token to one server |
| `aud` claim | "Audience" | JWT claim the validator compares against the canonical resource URL |
| Audience replay | "Token replay" | Token issued for Server A presented to Server B; defended by audience validation (spec: access-token privilege restriction) |
| Confused deputy | "Proxy token misuse" | An MCP proxy with a static client ID forwarding a token without per-client consent; distinct from audience replay |
| Mix-up attack | "Wrong token endpoint" | Client steered to redeem an honest AS's code at an attacker's endpoint; defended client-side via RFC 9207 `iss` |
| `iss` allow-list | "Trusted authorization servers" | The set named in protected-resource metadata's `authorization_servers` |
| `resource_metadata` | "Where to find the PRM doc" | `WWW-Authenticate` parameter naming the RFC 9728 metadata URL on a 401/403 |
| Public client | "Native or browser client" | OAuth client with no `client_secret`; PKCE compensates |
| `WWW-Authenticate` | "401/403 response header" | Carries `Bearer error=...` directives that drive client recovery |

## 继续阅读 继续阅读

- [MCP authorization specification (2026-07-28)](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)- 现行MCP授权配置
  中文翻译:MCP 授权规范(2026-07-28) 本课实现的当前MCP 授权配置档
- [MCP 2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)- CIMD,发行人验证,DCR减值和发行人关键的凭证变化
  中文翻译:MCP 2026-07-28 变更日志CIMD、签发人校验、DCR 弃用与按签发人做键的凭证变更
- [OAuth Client ID Metadata Document (draft-ietf-oauth-client-id-metadata-document-00)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-client-id-metadata-document-00)    
  中文翻译:CIMD 草案"URL即客户端_id"的注册机制
- [RFC 8414 — OAuth 2.0 Authorization Server Metadata](https://datatracker.ietf.org/doc/html/rfc8414) 发现合同
  中文翻译:RFC 8414发现契约
- [RFC 7591 — OAuth 2.0 Dynamic Client Registration Protocol](https://datatracker.ietf.org/doc/html/rfc7591) DCR (倒退路径)
  中文翻译:RFC 7591DCR(后备路径)
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://datatracker.ietf.org/doc/html/rfc7636)公众客户拥有证据
  中文翻译:RFC 7636PKCE,公共客户端持有证书
- [RFC 8707 — Resource Indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707)观众的
  中文翻译:RFC 8707资源指示器,受众固定
- [RFC 9728 — OAuth 2.0 Protected Resource Metadata](https://datatracker.ietf.org/doc/html/rfc9728)资源服务器发现
  中文翻译:RFC 9728资源服务器发现
- [RFC 9207 — OAuth 2.0 Authorization Server Issuer Identification](https://datatracker.ietf.org/doc/html/rfc9207) `iss`防范混合攻击的参数
  中文翻译:RFC 9207防御混 攻击的 `iss`参数
- [RFC 7662: OAuth 2.0 Token Introspection](https://datatracker.ietf.org/doc/html/rfc7662)
  中文翻译:RFC 7662不透明代币的内省端点
- [RFC 7009: OAuth 2.0 Token Revocation](https://datatracker.ietf.org/doc/html/rfc7009)
  中文翻译:RFC 7009代币 吊销,本课的"新鲜度契约"
