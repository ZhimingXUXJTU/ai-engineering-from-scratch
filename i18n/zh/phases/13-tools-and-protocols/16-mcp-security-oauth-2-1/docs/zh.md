# 发行者:CIMD,发行人:PKCE,和步骤.

> 远程MCP请求是无国有的,但其授权并非匿名的. 绑定所有凭证与创建它的发行者,以及每一个代币与接收它资源.

> **【中文解读】**远程MCP 请求是无状态的,但授权不是匿名的.2026-07-28 授权配置的两个支柱:把每份凭证绑定到发发行它的发行者,把每个代币绑定到接收它的资源.`iss`校验、资源绑定代币与逐步授权.

> **【拓展】**合并了多年安全最佳实践:强制PKCE、禁止隐式流程──MCP在其上叠加自己的配置:注册优先级(预注册 > CIMD > 废弃的DCR)、RFC 9207 的`iss`参数精确校验、禁止跨发行商 复用凭证――CIMD(客户ID 转载数据文件,客户端 ID 元数据文档) 是新一代注册机制客户端自托管一个 HTTPS 元数据文档,文档 URL 本身就是客户_id,免去每次第一次接触都要动态注册的旧负担――

>  **【前置】**学本节前请先掌握:(1) 第13阶段 · 09 运输) 只有远程可播放的HTTP 才需要OAuth,本地工作室不用;(2) 第13阶段 · 15 安全) 先了解威胁面与主体 (主体) 概念;(3) 第2阶段 2.0/2.1、PKCE、载体代币 基础;(4) 第3阶段 RFC 9728 / RFC 8707 / RFC 9207 三份 RFC本课逐一实现关键校验.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 09 (transports), Phase 13 · 15 (security) | **前置知识:** Phase 13 · 09（传输层）、Phase 13 · 15（安全）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## 学习目标

- 通过保护资源的元数据发现授权服务器.
  中文翻译:通过受保护资源元数据发现授权服务器──
- 优先使用客户ID的元数据文件,而不是过时的动态客户端注册.
  中文翻译:优先使用客户端ID 元数据文档(CIMD),而不是已废弃的动态客户端注册(DCR) 』.
- 声明正确的`application_type`如果 DCR 兼容性路径是不可避免的.
  中文翻译:当DCR 兼容路径不可避免时,声明正确的 `application_type`,我知道.
- 验证授权响应`iss`并且按发行人分隔证书.
  中文翻译:校验授权响应的`iss`根据签发分离凭证.
- 使用PKCE,资源指标,观众验证和增量范围.
  中文翻译:使用PKCE、资源指示器、受众校验和增量权限范围──
- 发送授权MCP 2026-07-28请求,而无需协议会议.
  中文翻译:在无协议会话的情况下发送已授权的MCP 2026-07-28 请求──

> **【中文解读】**学习目标主线:元数据发现 → 注册优先级(CIMD 优先级)→ DCR 兼容路径的正确姿势 → `iss`校验与发行人 隔离 → PKCE/资源指示器/受众/增量范围 四套 → 无状态授权请求――六个目标串起来就是一个完整的远程MCP 授权流水线――

## 问题 问题引入

> **【中文解读】**认证回答"谁出示凭证",授权还应回答五个问题:哪个授权服务器发发发?代码给哪个MCP资源?哪个客户端和重定向URI 完成流程?用户批准了哪些操作?该请求是否仍在批准范围内?2026-07-28 授权配置强化注册与发行商 处理来回答这些问题,并不恢复握手或`Mcp-Session-Id`,我知道.

远程MCP服务器可能会阅读私人记录,写外部系统或启动昂贵的工作.身份验证告诉它谁提交了凭证.权限还必须回答:

> 远程MCP 服务器可能读取隐私记录、写入外部系统或触发昂贵操作――认证告诉它谁出示凭证――授权还必须回答:

- 哪个授权服务器发出了凭证?
  中文翻译:哪个授权服务器发出了这份凭证?
- 什么MCP资源是标志?
  标志是给哪个MCP资源的?
- 哪个客户端和转向URI完成了流动?
  中文翻译:哪个客户端和重定向URI完成流程?
- 用户批准了哪些操作?
  中文翻译:用户批准了哪些操作?
- 这一要求是否仍然符合批准?
  中文翻译:这个请求是否仍在该批准范围内?

根据"2026-07-28"授权配置文件,客户注册和发行商处理都会变得更加严格.`application_type`根据RFC 9207的证券交易条例,证券交易条例 (RFC 9207) 证券交易条例 (RFC 9207) 证券交易条例 (RFC 9207) 证券交易条例 (RFC 9207) 证券交易条例 (RFC 9207) 证券交易条例 (RFC 9207) 证券交易条例 (RFC 9207) 证券交易条例)

> 2026-07-28 授权配置加强客户端注册与发行人 处理:优先 CIMD、弃用 DCR、要求 DCR 声明正确的`application_type`校验RFC 9207发行商 响应 禁止跨发行商 复用凭证

它们不恢复了核心握手或`Mcp-Session-Id`现在,我们要去.

> 这些规则与无状态核心互补,不恢复核心握手或`Mcp-Session-Id`,我知道.

>  **【类比】**标签 像会员卡,资源指示器(RFC 8707) 等于在卡上印"仅限本店使用"(aud受众锁定);发行人 绑定则是"每家店的会员卡分开办"健身房的卡拿到超市刷不开,超市也不会把你的会员信息分享给健身房。CIMD 像"自带电子名片":你的名片就是URL身份,到任何新店出名片即可进入店,不需要每家重新填写登记表DCR);但消费记录仍然按了(发行人) 分开保存,换旧店时旧积分店证书) 不带过去.

## 概念的核心概念

> **【中文解读】**本节主线:三角色 → 授权只管 HTTP → RFC 9728 元数据发现 → 授权服务器元数据校验 → 注册优先级(预注册/CIMD/DCR)→ 按发行人 隔离存储凭证 → PKCE 授权码流程 → `iss`精确校验 → MCP 服务器端受众校验 → 最小范围 与逐步授权 → 无状态授权请求的错误信封 → 禁止代币 透传 →更新代币。

### 了解三个角色

- **MCP client:**代表资源所有者发送请求.
  翻译: 中文**MCP 客户端：**代表资源所有者发送请求――
- **MCP resource server:**接受访问令牌并为MCP终端服务.
  翻译: 中文**MCP 资源服务器：**接受访问代币并提供MCP端点.
- **Authorization server:**认证资源所有者,收集同意,并发行代币.
  翻译: 中文**授权服务器：**认证资源所有者、收集同意并签发代币──

资源服务器和授权服务器可以一起运行,但保持其识别器和验证责任分开.

> 资源服务器和授权服务器可以一起运行,但它们的标识符和校验责任必须保持分离.

### 权限适用于HTTP

基于HTTP的运输应用MCP授权规范.本地工作室服务器在进程和操作系统的信任边界下运行.仅仅为了对称性,不要添加虚假浏览器OAuth流向工作室.

>  MCP 授权规范仅适用于HTTP 传输.本地工作室 服务器运行在进程和操作系统的信任边界内,不要为了"对称"工作室加一个假浏览器 OAuth 流程.

对于远程流向 HTTP,将载体代币发送到 `Authorization`每次请求都会有标题.

> 对于远程流媒体HTTP,每个请求都把持有符号放在`Authorization`发送,绝对不放入URL.

### 开始使用保护资源的元数据

> **【中文解读】**保护资源数据是整个流程的起点:客户端从MCP资源URL出发,拉取`.well-known/oauth-protected-resource/mcp`没有任何可能的错误,也不要跟随未经验错误的发行者.

资源服务器发布RFC 9728的元数据:

```json
{
  "resource": "https://notes.example.com/mcp",
  "authorization_servers": ["https://auth.example.com"],
  "scopes_supported": ["notes:delete", "notes:read", "notes:write"]
}
```

客户端从MCP资源URL开始,获取此文档,选择广告授权服务器,然后获取该服务器的OAuth或OpenID连接元数据.

> 客户端从MCP资源URL发出,获取此文档,选择声明授权服务器,再获取该服务器的OAuth或OpenID连接元数据――

在构建RFC 9728的知名URL时保存资源路径.`https://notes.example.com/mcp`这一课使用了`https://notes.example.com/.well-known/oauth-protected-resource/mcp`放下了`/mcp`后可以选择同一来源的不同受保护资源的元数据.

> 构建RFC 9728已知URL 时要保留资源路径──资源 `https://notes.example.com/mcp`应对`https://notes.example.com/.well-known/oauth-protected-resource/mcp`掉了`/mcp`后可能选中同源上另一个受保护资源的元数据.

根据主机名,不要猜测授权服务器.不要跟踪从未验证的错误机构发现的发行商.保持客户愿意信任的发行商政策.

> 不要从主机名猜授权服务器;不要跟随未经验的错误体发行商;保留一个"客户端愿意信任哪些发行商"的策略.

### 验证授权服务器元数据

转载数据的数据应显示终端点和支持的控制:

> 应暴露的数据端点与受支持的控制项:

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

需要S256来编写PKCE.记录出发行器的精确字符串. 这正确值成为注册和代币存储的关键.

>  PKCE 要求 S256──记录精确发行人 字符串 这个精确值将成为注册与代币存储的键──

### 按照注册优先级

> 注册优先级是2026-07-28的关键变化:已有明确的关系使用预注册信息;否则在授权服务器声明支持时优先 CIMD;DCR只作废弃兼容回退;都不行才提示输入客户端信息――顺序不可颠倒,更不能在校试失败后"静默降级"到DCR――

使用预注册客户端信息,如果客户端已经与选择的发行商有明确关系.否则,当授权服务器广告支持时,更喜欢客户端ID元数据文件.仅使用DCR作为过时兼容性后退,然后要求客户端信息,如果这些机制中没有任何可用.

> 客户端与选择发行商 已有明确的关系使用预注册信息;否则在授权服务器声明支持时优先 CIMD;DCR只需要放弃兼容回退;这些机制是不可用的才提示输入客户端信息――

### 优先使用客户端ID 转载文件

> **【中文解读】**授权服务器获取并验证文件:`client_id`必须是带路径的HTTPSURL,且文档中的值与该URL完全相等;必须填字段是`client_id`,我知道.`client_name`,我知道.`redirect_uris`│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │

客户端ID的元数据文档给权限服务器一个HTTPSURL,它既是客户端识别器,也是其元数据的位置:

> 客户端ID元数据文档给授权服务器一个HTTPSURL,它既是客户端标识,也是其元数据的位置:

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

授权服务器将文件获取并验证.`client_id`文件中值必须是相同的URL. 需要的文件字段是`client_id`现在`client_name`其他`redirect_uris`现在,我们要去.`application_type`根据CIMD的规定,该系统的使用是CIMD的新要求.

> 授权服务器拉取并校验该文档.`client_id`必须是带路径的HTTPSURL,且文档中的值与该URL完全相等.`client_id`,我知道.`client_name`,我知道.`redirect_uris`,我知道.`application_type`现有的例子中,但不是CIMD的必填项,它的新强制用途专门在DCR路径上.

处理文件的获取作为SSRF敏感操作.解决和验证目的地,拒绝循环回归,私人,链接本地,以及其他不允许的地址,重新检查转向和DNS变更后,限制转向,字节和时间,需要JSON,并且只根据验证的HTTP缓存控制.`client_name`其他显示字段作为不可信的文本.

> 把文件作为SSRF敏感操作:解析并校验目的地,拒绝回环,私网,链路本地等禁用地址,重定向与DNS变化后复查,限制重定向次数,字节和时间,强制JSON,只按已校验的HTTP缓存控制来缓存.`client_name`等展示字段按不可信文本处理.

> ️ **【易错点】**场景:把拉取CIMD 文档当成普通GET,不校验目标地址 / 后果:SSRF攻击者把`client_id`指向内网地址(如云元数据服务 169.254.169.254、内网管理面板),授权服务器替攻击者发起请求并把结果写入注册记录 / 修复:(1) 解析后校验IP,拒绝回环/私网/链路本地段;(2) 限制重定向次数、响应字节与超时,重定向和DNS 变化后重定向;(3) 强制要求JSON 内容类型,按验证的缓存缓存;(4) 展示字段((`client_name`等) 一律按不可信文本转义.

根据CIMD的规定,每次接触时都不需要打印新的动态标识符,不需要删除转向URI验证,发行方政策或用户同意.

> 无需在每次第一次接触时都建立新的动态标识,但无需重定向URI校验,发行人策略或用户同意.

###  DCR 是一个兼容性路径

动态客户端注册仍然可用于旧授权服务器,但对于新的MCP实现而言,它已经过时使用.

> 动态客户端注册 (DCR) 对于旧授权服务器仍然可用,但对于新的MCP实现已被放弃.

在使用DCR时,声明`application_type`其他:

> 使用DCR 时,声明 `application_type`其他:

```json
{
  "client_name": "Notes desktop client",
  "application_type": "native",
  "redirect_uris": ["http://127.0.0.1:8765/callback"],
  "grant_types": ["authorization_code"],
  "response_types": ["code"]
}
```

- 桌面,移动,命令行和循环回复客户端使用`native`现在,我们要去.
  中文翻译:桌面、移动、命令行和回环客户端用`native`,我知道.
- 使用远程托管的浏览器应用程序`web`通过远程HTTPS转向.
  中文翻译:远程托管的浏览器应用 `web`和远程HTTPS 重定向──

省掉该字段可能会默认到`web`在OpenID Connect注册实现中,并未实现合法循环回转向.

> 省略该字段时,OpenID连接注册实现可能默认`web`法律的转变转向失败.

保持DCR代码在明确的反弹决定背后. 随意后退后CIMD验证失败后不要沉默地回落. 这可能会使安全失败成为一个更弱的注册路径.

> 后应放出明显的退出决策. 避免在CIMD校验中任意失败后默默退出.

### 绑定证书给发行人

> **【中文解读】**凭证按精确发行人 隔离存储:`issuer_credentials[issuer]`与`tokens[(issuer, resource)]`△发现结果从作者-一 换成作者-二 时要重新评估信任绝不把第一个发行商的客户机密,DCR客户机密,注册访问令牌,刷新代币或访问代币发送给第二个. CIMD是例外:它本身是自主管理URL而不是发行商的造证书,同一URL可移植到新发行商,但授权应对和代币仍然根据新发行商的验证和存储.

存储发行人注册材料,以发行人名为:

> 存储发行人所制造的注册材料到确切的发行人名下:

```text
issuer_credentials[issuer] = pre_registered_or_dcr_client
tokens[(issuer, resource)] = access_token
```

如果保护资源的发现从 变化`https://auth-one.example`为了`https://auth-two.example`任何其他公司都必须使用其新发行商发行的凭据,如: 首发行商的客户密码,DCR客户ID,注册访问代币,更新代币或访问代币.

> 如果保护资源发现的结果`https://auth-one.example`变成`https://auth-two.example`为了重新评估信任──绝不把第一个发行商的客户机密──DCR客户ID──注册访问令牌──刷新令牌或访问令牌──发送给第二个──预注册和DCR客户端必须使用新发行商的凭证──签发证──

根据CIMD的数据,CIMD客户端的身份是不同的,因为它是一个自主托管的HTTPSURL,而不是授权服务器编制的凭证.同样的CIMD URL是可移植的:一个新的可信赖发行商在没有重新注册的DCR的情况下获取和验证了文档.授权回复和代币仍然被验证并存储在新的发行商下.

> 单个CIMD客户端ID 不同:它是自托管的HTTPSURL,不是授权服务器造的凭证. 同一个CIMDURL可移植新发行人 拉取并校验文档即可,无需DCR重新注册.

### 授权代码与PKCE

互动流程是:

> 交互式流程是:

1. 产生高气.`code_verifier`现在,我们要去.
  中文翻译:生成高 `code_verifier`,我知道.
2. 导出S256`code_challenge`现在,我们要去.
  中文翻译:派生 S256 `code_challenge`,我知道.
3. 发送授权请求的确切信息`client_id`现在`redirect_uri`现在`scope`现在`code_challenge`其他`resource`现在,我们要去.
  中文翻译:发送授权请求,带精确的 `client_id`,我知道.`redirect_uri`,我知道.`scope`,我知道.`code_challenge`和 `resource`,我知道.
4. 收到包含 许可的回复`code`提供时,`iss`现在,我们要去.
  中文翻译:接收包含 `code`与(若提供)`iss`权力应对
5. 验证`iss`在使用任何响应字段之前,对记录的确切发行者进行分析.
  中文翻译:在使用任何响应字段之前,先对照精确记录的发行者校验 `iss`,我知道.
6. 换代码`code_verifier`转向的 URI,和相同的`resource`现在,我们要去.
  中文翻译:用`code_verifier`、同一个转向URI 和同一个`resource`换个代币.
7. 存储结果的代币在下面`(issuer, resource)`现在,我们要去.
  中文翻译:把得到的标志存到`(issuer, resource)`现在,我在做什么?

其他`resource`参数从RFC 8707出现在授权和代币请求. 它识别了正规的MCP服务器URI.

> 根据RFC 8707的`resource`参数同时出现授权请求与代币请求中,标识规范的MCP 服务器URI──

### 验证`iss`确切地

标准规则9207防止一个发行商的授权响应与另一个发行商的响应混.

> 防止一个发行商的授权响应与另一个发行商的响应相混.

什么时候`iss`如果有,请与记录的发行商进行比较,而无需折叠案例,后续剪辑变化,默认端口删除或百分比编码正常化.

> `iss`存在时,与记录发行者相比较不折叠大小写、不变尾斜、不去默认端口、不做百分数编码规范化──不匹配时,不要使用代码,甚至不要显示该响应中攻击者可控的错误详细信息──

包含一个权限服务器`iss`广告`authorization_response_iss_parameter_supported: true`现在的客户仍然验证了礼物`iss`即使没有广告.

> 包含`iss`授权服务器会声明`authorization_response_iss_parameter_supported: true`,即使缺少该声明,当前客户端仍然需要经验.`iss`,我知道.

>  **【困惑】**问:为什么"精确字符串比较"如此真实?差个尾斜不行吗?`https://auth.example.com`与`https://auth.example.com/`视为相等,攻击者注册带尾斜的类似发行商就能挤进同一储备槽,继承别人的凭证.

### 在MCP服务器上验证观众

资源服务器只接受为自己发行的代币:

> 资源服务器只接受为自己发送的代币:

```text
token.issuer == configured_authorization_server
token.audience == canonical_mcp_resource
```

无效,过期,发行错误或错误受众的代币收到401.MCP服务器不得接受或传输用于其他服务的代币.

> 无效、过期、错发行商、错受众的代币 一条 401 ・ MCP 服务器不得接受或转移到发行的其他服务代币――

### 要求最小的电流范围

> **【中文解读】**最小权限的落地:先请求当下所需范围;后续工具需要更多时,服务器返回403+ 权力范围 挑战`WWW-Authenticate`带`scope`与`resource_metadata`客户端解释新权限、获取同意、使用合并范围 集重跑授权流程、使用新JSON-RPC id 重试──不要假设被挑战范围 是`scopes_supported`现在的操作是权威的.

如果后来的工具需要更多,服务器将返回403 带有权威的范围挑战:

> 如果后续工具需要更多,服务器将带有权力回来.

```text
WWW-Authenticate: Bearer error="insufficient_scope",
  scope="notes:delete",
  resource_metadata="https://notes.example.com/.well-known/oauth-protected-resource/mcp"
```

客户端解释了新的许可,获得同意,执行了新的授权流程,并用新的JSON-RPCID重新尝试MCP请求.

> 客户端向用户解释新权限、获取同意、使用合并后的范围集执行新的授权流程,然后使用新的JSON-RPCID重试MCP 请求。

不要假设所挑战的范围是`scopes_supported`挑战对目前的运营具有权威性.

> 不要假设被挑战的范围是`scopes_supported`现在的操作是权力的挑战.

### 授权和无国籍MCP线

> **【中文解读】**授权与协议协商正交:代码 授权主体,请求元数据协商协议行为,互不替代――线上校验固定序列:JSON-RPC 与元数据类型 → 头文相等 → 版本支持――路由/版本头不匹配 回复 400 `-32020`头文一致但版本不支持回复 400 `-32022`且`data`精确为`{"supported":["2026-07-28"],"requested":"<actual>"}`没有人知道 404 方法`-32601`△每一个请求错误(含401/403) 都是带原请求 id 的 JSON-RPC 错误信封;`WWW-Authenticate`留在HTTP头上;通知无 id,接受后 202 空体──

授权工具调用仍然包含完整的当前请求包裹:

> 授权的工具调用仍需携带完整的当前请求信封:

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

代币授权主任,请求元数据谈判协议行为,没有替代另一个.

> 标签: 授权主体; 请求元数据协商协议行为──两者互不替代──

验证线程以固定顺序:JSON-RPC和元数据类型,标题和体格等,然后支持协议.路由或版本标题不匹配返回HTTP 400与 `-32020`如果标题和体格同意不支持的版本,请返回HTTP 400`-32022`其他`data`完全是`{"supported":["2026-07-28"],"requested":"<actual>"}`未知方法返回了HTTP 404`-32601`现在,我们要去.

> 按固定顺序进行验证线上格式:JSON-RPC 与元数据类型,头与正文相等等等,然后协议支持.`-32020`标题一致但版本不支持,返回HTTP 400 `-32022`且`data`精确为`{"supported":["2026-07-28"],"requested":"<actual>"}`无法返回HTTP 404`-32601`,我知道.

每个请求错误,包括401无效的代币和403不够的范围,都是一个包含原始请求的JSON-RPC错误包.`id`结构性恢复信息属于可选错误`data`其他`WWW-Authenticate`通知没有 文件的内容`id`通过 HTTP 通知,将返回 202 个空格.

> 每个请求错误包括401 无效代币和403 权限不足都是带原始请求`id`结构化恢复信息被放置可选的错误`data`里;`WWW-Authenticate`仍有HTTP响应头没有通知`id`没有收到JSON-RPC 正文;被接受的HTTP通知返回202空体──

服务器实现`server/discover`广告工具,因此它也执行强制性`tools/list`工具描述符具有稳定的名称,描述和对象根.`inputSchema`列表是确定性和返回的`resultType`服务器身份元数据,一个有限的`ttlMs`其他`cacheScope`查找和使用者独立的工具列表可在授权之前使用.

> 服务器实现`server/discover`并且宣布工具,因此也实现必要的`tools/list`方法──工具描述符有稳定的名称、描述和对象根`inputSchema`列表是确定性的,返回`resultType`、服务器身份元数据、有界的 `ttlMs`和 `cacheScope` 发现与不随用户变化的工具列表可以在授权前提供;如果随主体变化而发生,则应应用常规策略和私人缓存.

### 没有标志性通行

客户端的MCP访问代币不能转发到下游API. 获得一个独立的下游代币与正确的受众或使用明确的代币交易设计. 服务拒绝为别人发明的代币时,受众验证只能有效.

> 服务器必须将客户端的MCP访问代币转发到下游API──要么获得受众正确的独立下游代币,要么使用明显的代币交换设计──受众的验证只有在各服务中拒绝"为别人发送的代币"才有效──

### 更新代码

更新代币是可选的.发行时,请保密存储它们,并按发行商和资源键键键.不要假设它们存在.当授权服务器支持旋转时,请旋转它们,并检测无效值的重复使用.

> 更新代币是可选的. 发发发时按发行商和资源为关键机密存储;不要假设它们存在.

```figure
t3-scope-stepup
```

## 动手构建

> **【中文解读】** `code/main.py`是进程内协议与授权模拟器:受保护资源发现"",授权服务器元数据"",CIMD注册"",版本门控的DCR回退"",应用程序类型"检查"",PKCE"",发行商"校验"",资源绑定代币"",范围"逐步升级"",`server/discover`,我知道.`tools/list`与无状态工具请求一次运通.模型接收已解析的请求正文与路由头,不是完整的HTTP 适配器 传输层契约 课09。

`code/main.py`是一个正在进行的协议和授权模拟器.它实现了保护资源发现,授权服务器元数据,CIMD注册,版本关闭DCR倒退,应用程序类型检查,PKCE,发行商验证,资源绑定代币,范围加大,`server/discover`现在`tools/list`没有国家,也没有国家.

> `code/main.py`是进程内协议与授权模拟器:受保护资源发现"",授权服务器元数据"",CIMD注册"",版本门控的DCR回退"",应用程序类型"检查"",PKCE"",发行商"校验"",资源绑定代币"",范围"逐步升级"",`server/discover`,我知道.`tools/list`和一个无状态工具请求.

该模型接收解析请求体和路由标题. 它不是完整的HTTP适配器,也不解析`Content-Type`或`Accept`连接到课程09的流式HTTP适配器,需要`Content-Type: application/json`其他`Accept`含有两者中的值`application/json`其他`text/event-stream`现在,我们要去.

> 模型接收已解析的请求正文与路由头,不是完整的HTTP适配器,不解析`Content-Type`或`Accept`◎把它连接到第09课的流动HTTP适配器上那边要求`Content-Type: application/json`且`Accept`同时包含`application/json`与`text/event-stream`,我知道.

运行它:

> 运行:

```bash
cd phases/13-tools-and-protocols/16-mcp-security-oauth-2-1
python3 code/main.py
python3 -m unittest discover code/tests -v
```

输出显示了发现首先,CIMD注册,普通阅读,两个独立的范围步骤,以及发行商密钥的凭证存储.

> 输出次展:发现流程,CIMD注册,一次普通读取,两次独立的范围,逐步升级,以及根据发行商的关键证书存储.

## 实际使用

映射模拟器对象到生产组件:

> 将模拟器对象映射到生产组件:

- `ResourceServer.protected_resource_metadata`成为RFC 9728终点.
  翻译: 中文`ResourceServer.protected_resource_metadata`对应RFC 9728 端点
- `AuthorizationServer.metadata`成为RFC 8414或OpenID Connect发现.
  翻译: 中文`AuthorizationServer.metadata`对应RFC 8414或OpenID连接发现
- `Client.enroll`成为CIMD分辨率加上明确的DCR兼容性分支.
  翻译: 中文`Client.enroll`对应CIMD 解析加显式的DCR 兼容分支
- 发行商所证实的客户身份证和`tokens_by_issuer_resource`作为CIMD的网站,CIMD的网站可以保持可移植性,而其授权结果仍然是发行商的.
  中文翻译:发行商 造的客户端凭证和 `tokens_by_issuer_resource`对于加密记录.CIMD URL 可保持可移植,而其授权结果保持发行人 绑定.
- `ResourceServer.handle`成为中间件,在发送之前验证当前的MCP标题,代币和工具范围,同时将每个请求错误都在匹配的JSON-RPC封装中保存.
  翻译: 中文`ResourceServer.handle`应对中间件 分发前校验 现有MCP 头、代码和工具范围,并让每个请求错误都落在匹配的JSON-RPC 错误信封里里.

## 运送它.

这一课是很好的.`outputs/skill-oauth-scope-planner.md`现在它设计了注册优先级,发行商的认证存储,申请类型,PKCE,资源指标,范围挑战以及目前无国籍请求界限.

> 本课产出发 `outputs/skill-oauth-scope-planner.md`△它现在的设计内容包括:注册优先级,发行商,绑定证书存储,应用程序类型,PKCE,资源指示器,范围挑战以及当前无状态请求边界.

## 练习题

1. 加入更新代币的旋转,并拒绝重新使用之前的更新代币.
   中文翻译:添加更新代币 轮换,并拒绝上一个更新代币 的重用──
2. 添加发行人权限列表.在发行人变更时,只使用可移植的CIMD URL;拒绝所有之前发行人硬币的凭证和代币.
   中文翻译:添加发行人 允许列表――发行人 变更时只复用可移植的CIMDURL,拒绝之前所有发行人 造的凭证和代币――
3. 添加到授权代码的期限,并确认迟到的交换失败.
   中文翻译:给授权码加过期时间,确认迟到换取失败──
4. 建立一个使用远程HTTPS转向的网络客户端变体,并将其DCR元数据与本地客户端进行比较.
   中文翻译:构建带远程HTTPS重定向的网 客户端变体,并比较其DCR元数据与本地客户端的差异──
5. 确认其访问令牌不能在第一个资源上使用.
   中文翻译:在同一发行商下添加第二个资源──确认其访问符号不能在第一个资源上使用──

## 关键词 快速查找表

| Term | Meaning | 中文 |
|------|---------|------|
| Protected-resource metadata | RFC 9728 document that identifies the resource and authorization servers | 受保护资源元数据：标识资源与授权服务器的 RFC 9728 文档 |
| CIMD | HTTPS metadata document whose URL is the OAuth client identifier | 客户端 ID 元数据文档：URL 即 OAuth 客户端标识的 HTTPS 元数据文档 |
| DCR | Deprecated dynamic client enrollment retained for compatibility | 动态客户端注册：已弃用、仅作兼容保留的动态注册 |
| `application_type` | `native` or `web`, used to validate redirect URI rules | 应用类型：`native` 或 `web`，用于校验重定向 URI 规则 |
| PKCE | Verifier and S256 challenge that protect an intercepted authorization code | 授权码交换证明密钥：保护被拦截授权码的 verifier 与 S256 challenge |
| `iss` | RFC 9207 authorization response issuer identifier | RFC 9207 授权响应签发方标识 |
| Resource indicator | RFC 8707 parameter that binds a token request to an MCP resource | 资源指示器：把 token 请求绑定到 MCP 资源的 RFC 8707 参数 |
| Audience | Resource for which a token is valid | 受众：token 对之有效的资源 |
| Step-up | New consent and token issuance for an additional current-operation scope | 逐步授权：为额外的当前操作 scope 进行的重新同意与 token 签发 |
| Issuer-bound credentials | Registration and token records isolated by exact authorization server issuer | 签发方绑定凭证：按精确授权服务器 issuer 隔离的注册与 token 记录 |

## 继续阅读 继续阅读

- [MCP 2026-07-28 authorization specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
  中文说明:MCP 授权规范正文 课本全部规则的权威来源
- [RFC 9728: OAuth 2.0 Protected Resource Metadata](https://www.rfc-editor.org/rfc/rfc9728)
  中文说明:受保护资源元数据 RFC发现流程的起点.
- [RFC 8707: Resource Indicators for OAuth 2.0](https://www.rfc-editor.org/rfc/rfc8707)
  中文说明:资源指示器 RFCtoken 受众绑定。
- [RFC 9207: OAuth 2.0 Authorization Server Issuer Identification](https://www.rfc-editor.org/rfc/rfc9207)
  中文说明:授权响应 `iss`参数 RFC防发行人 混。
- [OAuth Client ID Metadata Document draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-client-id-metadata-document/)
  中文说明:CIMD草案以URL为客户端标识的新注册机制
