# MCP 授权: CIMD、签发方绑定、PKCE 与逐步授权

> Một yêu cầu từ xa của MCP là không có quốc gia, nhưng sự ủy quyền của nó không ẩn danh. Kết nối mọi giấy chứng nhận với nhà phát hành đã tạo nó và mỗi token với tài nguyên nhận nó.

> **【中文解读】**远程 MCP 请求是无状态的,但授权不是匿名的──2026-07-28 授权配置的两个支柱:把每份凭证绑定到发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发发`iss`校验、资源绑定 token 与逐步授权──

> **【拓展】**OAuth 2.1 合并了多年安全最佳实践:强制 PKCE、禁止隐式流程──MCP 在其上叠加自己的配置:注册优先级(预注册 > CIMD > 废弃 DCR)、RFC 9207 的`iss`参数精确校验、禁止跨发行人 复用凭证──CIMD(Client ID Metadata Document,客户端 ID 元数据文档) là một cơ chế đăng ký thế hệ mới客户端自托管一个 HTTPS 元数据文档,文档 URL 本身就是客户_id,免去每次第一次接触都要动态注册的旧负担──

>  **【前置】**学本节前请先掌握:(1) Giai đoạn 13 · 09(transport)  chỉ từ xa Streamable HTTP 才需要 OAuth,本地工作室不用;(2) Giai đoạn 13 · 15(security) 先理解威胁面与主体(主) 概念;(3) OAuth 2.0/2.1、PKCE、Bearer token 基础;(4) RFC 9728 / RFC 8707 / RFC 9207 三份 RFC本课逐一实现其关键校验.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 09 (transports), Phase 13 · 15 (security) | **前置知识:** Phase 13 · 09（传输层）、Phase 13 · 15（安全）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## Mục tiêu học tập

- Khám phá các máy chủ ủy quyền thông qua metadata nguồn được bảo vệ.
  Trung ngữ翻译:通过受保护资源元数据发现授权服务器。
- Tích thích Tài liệu Metadata ID khách hàng hơn là đăng ký khách hàng động lỗi thời.
  Trung文翻译:优先使用客户端 ID 元数据文档(CIMD), thay vì đã bị bỏ rơi động态客户端注册(DCR)。
- Hãy tuyên bố đúng `application_type`khi một con đường tương thích DCR là không thể tránh khỏi.
  Trung文翻译:当 DCR 兼容路径不可避免时,声明正确的 `application_type`
- Thiết lập câu trả lời cho phép `iss`và tách các thông tin tín dụng theo nhà phát hành.
  Trung ngữ翻译:校验授权响应的 `iss`,并按签发方隔离凭证.
- Sử dụng PKCE, chỉ số nguồn lực, xác thực khán giả và phạm vi tăng trưởng.
  Trung文翻译: sử dụng PKCE、资源指示器、受众校验和增量权限范围──
- Gửi yêu cầu được ủy quyền của MCP 2026-07-28 mà không cần các phiên giao thức.
  Trung文翻译: 在无协议会话的情况下发送已授权的 MCP 2026-07-28 求求──

> **【中文解读】**Học tập mục tiêu chủ đạo:元数据发现 → 注册优先级(CIMD 优先)→ DCR 兼容路径的正确姿势 → `iss`校验与发行人 隔离 → PKCE/资源指示器/受众/增量 scope 四套 → 无状态授权请求――六个目标串起来就是一条完整的远程MCP 授权流水线――

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**认证 trả lời" ai đã trình bày bằng chứng",授权 cũng phải trả lời năm câu hỏi: máy chủ cấp phép nào phát hành? mã thông báo nào cho MCP 资源 nào? máy khách nào và định hướng URI nào hoàn thành quá trình? người dùng đã phê duyệt những hoạt động nào?`Mcp-Session-Id`

Một máy chủ MCP từ xa có thể đọc hồ sơ riêng tư, viết hệ thống bên ngoài hoặc kích hoạt công việc tốn kém.

> 远程MCP 服务器可能读取隐私记录、写入外部系统或触发昂贵操作――认证告诉它谁出了凭证――授权还必须回答:

- Quản lý nào đã phát hành giấy chứng nhận?
  Trung ngữ翻译: Which authorized server issued this diploma?
- MCP là mã thông báo cho nguồn nào?
  Trung ngữ翻译: This token is giving to which MCP 资源的?
- Client nào và URI chuyển hướng đã hoàn thành dòng chảy?
  Trung ngữ翻译: Quý khách hàng và định hướng URI đã hoàn thành quá trình?
- Người dùng đã chấp thuận các hoạt động nào?
  Trung ngữ翻译: người dùng đã phê duyệt những hoạt động nào?
- Liệu yêu cầu chính xác này vẫn phù hợp với sự chấp thuận đó?
  Trung ngữ翻译: Đây là yêu cầu có còn trong phạm vi phê duyệt?

Profil ủy quyền 2026-07-28 làm cứng đăng ký khách hàng và xử lý nhà phát hành. Nó thích Tài liệu Metadata ID khách hàng, làm trệ Dinamic Client Registration, yêu cầu quyền `application_type`trên DCR, xác nhận các phản hồi của nhà phát hành RFC 9207, và cấm tái sử dụng chứng chỉ giữa các nhà phát hành.

> 2026-07-28  ủy quyền định vị tăng cường đăng ký khách hàng và nhà phát hành  xử lý: ưu tiên CIMD  từ bỏ sử dụng DCR  yêu cầu DCR  tuyên bố chính xác `application_type`、校验 RFC 9207 phát hành 响应、禁止跨发行 复用凭证。

Những quy tắc này bổ sung vào lõi vô quốc tịch.`Mcp-Session-Id`- Tôi không biết.

> Những quy tắc này không liên quan đến sự hỗ trợ, không phục hồi tay cầm hoặc`Mcp-Session-Id`

>  **【类比】**token 像会员卡,资源指示器(RFC 8707) tương đương với in on card " chỉ giới hạn sử dụng cửa hàng này" (aud受众锁定);issuer 绑定则是" mỗi cửa hàng của thành viên thẻ mở办"健房的卡拿到超市刷不开,超市也不会把你的会员信息分享给健房;;CIMD 像"自带的电子名片": danh bạ của bạn chính là URL身份, đến bất kỳ cửa hàng mới nào biểu thị danh bạ có thể vào cửa hàng ngay lập tức, không cần phải lấp đầy lại danh bạ đăng ký DCR (DCR); nhưng hồ sơ tiêu dùng vẫn được lưu giữ theo quy định của nhà phát hành, đổi cửa hàng cũ 旧积分店证书) không mang quá khứ.

## Khái niệm cốt lõi

> **【中文解读】**本节主线:三角色 → 授权只管 HTTP → RFC 9728 元数据发现 → 授权服务器元数据校验 → 注册优先级(预注册/CIMD/DCR) → 按发行人 隔离储备凭证 → PKCE 授权码流程 → `iss`精确校验 → MCP 服务器端受众校验 → 最小范围 与逐步授权 → 无状态授权请求的错误信封 → 禁止代币 透传 → refresh token。

### Biết ba vai trò

- **MCP client:**gửi yêu cầu thay mặt cho chủ sở hữu tài nguyên.
  Trung ngữ翻译:**MCP 客户端：**代表资源所有者发送请求──
- **MCP resource server:**chấp nhận token truy cập và phục vụ điểm cuối MCP.
  Trung ngữ翻译:**MCP 资源服务器：** chấp nhận token truy cập并 cung cấp MCP 端点。
- **Authorization server:**xác thực chủ sở hữu tài nguyên, thu thập sự đồng ý và phát hành token.
  Trung ngữ翻译:**授权服务器：**认证资源所有者、收集同意并签发代币──

Các máy chủ tài nguyên và máy chủ ủy quyền có thể được vận hành cùng nhau, nhưng giữ các nhận dạng và trách nhiệm xác thực của họ riêng biệt.

> Các dịch vụ tài nguyên và các dịch vụ ủy quyền có thể hoạt động cùng nhau, nhưng các công cụ nhận dạng và nhiệm vụ của chúng phải được giữ riêng biệt.

### Truyền phép áp dụng cho HTTP

Các quy định ủy quyền MCP áp dụng cho các giao thông dựa trên HTTP. Một máy chủ studio địa phương chạy dưới ranh giới tin cậy của quy trình và hệ điều hành. Đừng thêm một dòng OAuth trình duyệt giả vào studio chỉ vì sự đối xứng.

> MCP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

Đối với HTTP Streamable từ xa, gửi token người mang vào `Authorization`không bao giờ đặt nó trong URL.

> Đối với HTTP Streamable từ xa, mỗi yêu cầu đều đặt token  đặt `Authorization`头里发送,绝不放进URL.

### Bắt đầu với metadata nguồn được bảo vệ

> **【中文解读】**RFC 9728 Được bảo vệ tài nguyên dữ liệu là điểm khởi đầu của toàn bộ quy trình: khách hàng từ MCP  tài nguyên URL xuất phát, kéo `.well-known/oauth-protected-resource/mcp`(注意保留资源路径后), từ中选择授权服务器,再拉取它的OAuth/OIDC 元数据──不要按主机名猜授权服务器,也不要跟随未经验错体里发现的发行者──

Các nguồn máy chủ xuất bản RFC 9728 metadata:

```json
{
  "resource": "https://notes.example.com/mcp",
  "authorization_servers": ["https://auth.example.com"],
  "scopes_supported": ["notes:delete", "notes:read", "notes:write"]
}
```

Khách hàng bắt đầu từ URL nguồn MCP, lấy tài liệu này, chọn máy chủ ủy quyền quảng cáo, và sau đó lấy OAuth hoặc OpenID Connect metadata của máy chủ đó.

> 客户端 từ MCP 资源 URL xuất phát, lấy tài liệu này, chọn một tuyên bố của ủy quyền máy chủ, tái lấy OAuth hoặc OpenID Connect của máy chủ đó 元数据──

Bảo tồn con đường tài nguyên khi xây dựng URL nổi tiếng của RFC 9728.`https://notes.example.com/mcp`, bài học này sử dụng`https://notes.example.com/.well-known/oauth-protected-resource/mcp`- Thả ra `/mcp`Suffix có thể chọn metadata cho một nguồn bảo vệ khác nhau trên cùng nguồn gốc.

>  cấu trúc RFC 9728 URL nổi tiếng 时要保留资源路径──资源 `https://notes.example.com/mcp`Đối với`https://notes.example.com/.well-known/oauth-protected-resource/mcp`        `/mcp`后可能选中同源上另一个受保护资源的元数据──

Đừng đoán máy chủ ủy quyền từ tên chủ. Đừng theo dõi nhà phát hành được phát hiện từ một cơ quan lỗi không xác nhận. Hãy giữ một chính sách mà nhà phát hành khách hàng sẵn sàng tin tưởng.

> Đừng theo dõi người phát hành từ các tổ chức chủ sở hữu; đừng theo dõi người phát hành từ các tổ chức sai lầm chưa được kiểm tra; giữ lại một chiến lược " khách hàng muốn tin tưởng những người phát hành".

### Kiểm tra dữ liệu siêu dữ liệu máy chủ ủy quyền

Các siêu dữ liệu nên phơi bày các điểm cuối và các điều khiển được hỗ trợ:

> Các dữ liệu nên được phơi bày và các điều khiển được hỗ trợ:

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

yêu cầu S256 cho PKCE. ghi lại chuỗi phát hành chính xác. giá trị chính xác đó trở thành chìa khóa cho đăng ký và lưu trữ token.

> PKCE  yêu cầu S256。 ghi chép chính xác của nhà phát hành 字符串

### Theo ưu tiên đăng ký

> Đăng ký ưu tiên là sự thay đổi quan trọng của 2026-07-28: đã có mối quan hệ rõ ràng với thông tin đăng ký trước; nếu không thì trong tuyên bố hỗ trợ máy chủ ủy quyền ưu tiên CIMD; DCR chỉ cần sử dụng kết hợp trở lại;都不行才提示输入客户端信息──顺序不可颠倒,更不能在校试失败后"静默降级"到DCR──

Sử dụng thông tin khách hàng đã đăng ký trước khi khách hàng đã có mối quan hệ rõ ràng với nhà phát hành đã chọn. Nếu không, hãy ưu tiên Tài liệu Metadata ID khách hàng khi máy chủ ủy quyền quảng cáo hỗ trợ. Chỉ sử dụng DCR như là sự phục hồi tương thích lỗi thời, sau đó yêu cầu thông tin khách hàng nếu không có một trong những cơ chế đó có sẵn.

> 客户端与选择发行商 已有明确关系时使用预注册信息;否则在授权服务器声明支持时优先 CIMD;DCR只作废弃兼容回退;这些机制都不可用时才提示输入客户端信息──

### Ưu tiên ID Client Metadata Documents

> **【中文解读】**CIMD: Đưa cho máy chủ ủy quyền một URL HTTPS, nó là cả mục tiêu nhận dạng khách hàng và là dữ liệu đặt tại đó.`client_id`必须是带路径的 HTTPS URL,且文档中的值与该URL 完全相等; 必须填字段是 `client_id``client_name``redirect_uris`CIMD 免去第一次接触时造动态标识, nhưng không miễn phí định hướng URI 校验、发行人 策略和用户同意──拉取文档本身是SSRF 敏感操作,要注意──

Tài liệu Metadata ID Client cung cấp cho máy chủ ủy quyền một URL HTTPS là cả nhận dạng khách hàng và vị trí của metadata của nó:

> 客户端 ID 元数据文档 cho phép máy chủ một URL HTTPS, nó là cả mục tiêu nhận dạng khách hàng và vị trí của dữ liệu:

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

Các máy chủ ủy quyền lấy và xác nhận tài liệu.`client_id`phải là một URL HTTPS với một con đường, và giá trị bên trong tài liệu phải bằng với URL đó chính xác. Các trường tài liệu cần thiết là `client_id`- `client_name`, và`redirect_uris`- `application_type`xuất hiện trong ví dụ này nhưng không phải là yêu cầu CIMD. Việc sử dụng bắt buộc mới của nó cụ thể là con đường DCR.

> 授权服务器拉取并校验该文档──`client_id`必须是带路径的HTTPS URL,且文档内值与该URL 完全相等──文档必填字段为 `client_id``client_name``redirect_uris``application_type`Trong các ví dụ hiện tại nhưng không phải là một phần cần thiết của CIMD, việc sử dụng bắt buộc mới của nó đặc biệt là trên các đường DCR.

Chế độ lấy tài liệu như một hoạt động nhạy cảm với SSRF. Giải quyết và xác nhận đích, từ chối các địa chỉ loopback, riêng tư, liên kết địa phương và không được phép, kiểm tra lại sau khi chuyển hướng và thay đổi DNS, giới hạn chuyển hướng, byte và thời gian, yêu cầu JSON, và chỉ theo các kiểm soát cache HTTP được xác nhận.`client_name`và các trường hiển thị khác như văn bản không đáng tin cậy.

> Cắt tài liệu như các hoạt động nhạy cảm của SSRF: phân tích và kiểm tra mục đích, từ chối quay lại vòng, riêng mạng, các địa chỉ sử dụng, định hướng lại với DNS thay đổi, hạn chế số lần định hướng lại, chữ cái và thời gian, bắt buộc JSON, chỉ theo kiểm tra HTTP 缓存 để kiểm tra缓存.`client_name`等展示字段按不可信文本处理.

> ️ **【易错点】**场景:把拉取 CIMD 文档当成普通 GET,不校验目标地址 / 后果:SSRF攻击者把 `client_id`Chỉ hướng vào địa chỉ web của mình (如云元数据服务 169.254.169.254、内网管理面板), ủy quyền máy chủ thay vì kẻ tấn công khởi động yêu cầu并把结果写入注册记录 / 修复:(1) 解析后校验 IP,拒回环/私网/链路本地段;(2) 限制重定向次数、响应字节与超时,重定向和 DNS 变化后重定向;(3) 强制要求 JSON 内容类型,按验证的缓存缓存;(4) 显示字段((`client_name`等) Một luật theo không thể tin được văn bản chuyển nghĩa.

CIMD loại bỏ sự cần thiết phải đúc một nhận dạng động mới cho mỗi lần tiếp xúc đầu tiên. Nó không loại bỏ xác thực URI chuyển hướng, chính sách phát hành hoặc sự đồng ý của người dùng.

> CIMD không có nhu cầu tạo ra các biểu tượng động mới mỗi lần tiếp xúc đầu tiên, nhưng không có sự chuyển hướng lại URI 校验、发行策略或用户同意──

### DCR là một con đường tương thích

Dynamic Client Registration vẫn có sẵn cho các máy chủ ủy quyền cũ hơn, nhưng nó đã bị lỗi thời cho các triển khai MCP mới.

> 动态客户端注册 (DCR) vẫn còn có sẵn cho các máy chủ cấp phép cũ, nhưng đã bị bỏ qua cho việc thực hiện MCP mới.

Khi sử dụng DCR, báo cáo `application_type`- Có thể là:

> Sử dụng DCR 时, tuyên bố `application_type`- Có thể là:

```json
{
  "client_name": "Notes desktop client",
  "application_type": "native",
  "redirect_uris": ["http://127.0.0.1:8765/callback"],
  "grant_types": ["authorization_code"],
  "response_types": ["code"]
}
```

- Các máy tính để bàn, di động, dòng lệnh và các khách hàng loopback sử dụng `native`- Tôi không biết.
  Trung ngữ翻译:桌面、移动、命令行和回环客户端用 `native`
- Sử dụng các ứng dụng trình duyệt được lưu trữ từ xa `web`và chuyển hướng HTTPS từ xa.
  Trung ngữ翻译:远程托管的浏览器应用用 `web`和远程 HTTPS 重定向──

Việc bỏ trường có thể mặc định là `web`trong một thực hiện đăng ký OpenID Connect và làm cho một chuyển hướng vòng lặp hợp pháp thất bại.

> 省略该字段时,OpenID Connect đăng ký thực hiện có thể默认 `web`, dẫn đến sự thất bại của vòng quay pháp lý.

Giữ mã DCR đằng sau một quyết định phản hồi rõ ràng. Đừng im lặng quay lại sau khi thất bại xác thực CIMD tùy ý. Điều đó có thể biến một lỗi bảo mật thành một con đường đăng ký yếu hơn.

> DCR mã phải được đặt sau một quyết định hoàn trả rõ ràng. Không được đặt trong một cách lặng lẽ sau khi thất bại của CIMD.

### Các thông tin tín dụng liên kết với nhà phát hành

> **【中文解读】**凭证 theo nhà phát hành chính xác 隔离存储:`issuer_credentials[issuer]`Với`tokens[(issuer, resource)]` phát hiện kết quả từ tác giả-một 换 thành tác giả- hai 时要重新评估信任绝不把第一个发行商的客户机密、DCR客户 id、注册访问令牌、refresh token或访问代币 发送给第二个。CIMD là ngoại lệ: nó tự là một URL tự quản chứ không phải là chứng chỉ của nhà phát hành 造的证书, cùng một URL có thể được chuyển đến nhà phát hành mới, nhưng quyền đáp ứng và token vẫn theo các chứng chỉ và lưu trữ của nhà phát hành mới。

Cung cấp tài liệu đăng ký được phát hành bởi nhà phát hành dưới tên chính xác của nhà phát hành:

> Đưa vật liệu đăng ký của nhà phát hành  tạo tồn tại cho nhà phát hành chính xác

```text
issuer_credentials[issuer] = pre_registered_or_dcr_client
tokens[(issuer, resource)] = access_token
```

Nếu phát hiện tài nguyên được bảo vệ thay đổi từ `https://auth-one.example`đến`https://auth-two.example`, đánh giá lại niềm tin. Không bao giờ gửi bí mật khách hàng của nhà phát hành đầu tiên, ID khách hàng DCR, mã đăng ký truy cập, mã thông báo cập nhật hoặc mã thông báo truy cập cho nhà phát hành thứ hai. Khách hàng đã đăng ký trước và DCR phải sử dụng các thông tin tín dụng được phát hành cho nhà phát hành mới.

> Nếu được tìm thấy các kết quả của tài nguyên được bảo vệ`https://auth-one.example`变成 `https://auth-two.example`, để đánh giá lại tín dụng. Không cần phải chia sẻ bí mật khách hàng của nhà phát hành thứ nhất. ID khách hàng của DCR. đăng ký lệnh truy cập.

Một ID khách hàng CIMD khác vì nó là một URL HTTPS được lưu trữ tự, chứ không phải một tín hiệu được tạo ra bởi một máy chủ ủy quyền.

> CIMD client id không giống nhau: nó là tự quản lý HTTPS URL, không phải là giấy phép được tạo bởi máy chủ ủy quyền.

### Mã ủy quyền với PKCE

Phòng chảy tương tác là:

> 交互式流程 là:

1. Tạo ra một lượng entropy cao `code_verifier`- Tôi không biết.
  中文翻译:生成高 `code_verifier`
2. Tạo ra S256 `code_challenge`- Tôi không biết.
  Trung文翻译:派生 S256 `code_challenge`
3. Gửi yêu cầu cấp phép với chính xác `client_id`- `redirect_uri`- `scope`- `code_challenge`, và`resource`- Tôi không biết.
  Trung ngữ翻译:发送授权请求,带精确的 `client_id``redirect_uri``scope``code_challenge`和 `resource`
4. Nhận được một câu trả lời về quyền phép có chứa `code`và, khi được cung cấp, `iss`- Tôi không biết.
  中文翻译:接收包含 `code`Với ((若提供)`iss`Đề xuất của người dùng
5. Định hành`iss`đối với nhà phát hành ghi nhận chính xác trước khi sử dụng bất kỳ trường phản hồi nào.
  Trung ngữ翻译: 在使用任何响应字段之前,先对照精确记录的发行者校验 `iss`
6. Thay đổi mã với `code_verifier`, cùng một URI chuyển hướng, và cùng một `resource`- Tôi không biết.
  中文翻译:用 `code_verifier`、 cùng một chuyển hướng URI 和 cùng một `resource`换代币.
7. Đặt token kết quả dưới `(issuer, resource)`- Tôi không biết.
  Trung ngữ翻译:把得到的标志 存到`(issuer, resource)`Nào, tôi đã làm gì?

- `resource`tham số từ RFC 8707 xuất hiện trong cả yêu cầu ủy quyền và token. Nó xác định URI máy chủ MCP.

> Từ RFC 8707 `resource`参数 xuất hiện đồng thời với yêu cầu cấp phép và token yêu cầu trong, Identify规范的 MCP 服务器 URI。

### Định hành`iss`chính xác

RFC 9207 ngăn chặn phản ứng ủy quyền từ một nhà phát hành bị nhầm lẫn với phản ứng từ một nhà phát hành khác.

> RFC 9207  ngăn chặn sự nhầm lẫn giữa một emittent's authorized response with another emittent's response phase.

Khi nào `iss`Nếu có sự không phù hợp, đừng hành động trên mã hoặc thậm chí hiển thị chi tiết lỗi được kiểm soát bởi kẻ tấn công từ phản ứng đó.

> `iss`Khi tồn tại, không nhét với nhà phát hành ghi chép, không nhét lại, không nhét lại, không nhét lại, không nhét lại, không dùng mã, thậm chí không thể cho thấy chi tiết sai lầm của kẻ tấn công trong phản ứng.

Một máy chủ ủy quyền bao gồm `iss`quảng cáo `authorization_response_iss_parameter_supported: true`Khách hàng hiện tại vẫn xác nhận một món quà`iss`ngay cả khi quảng cáo đó bị mất.

> 包含 `iss`                                                                                                                                                                                                                                                              `authorization_response_iss_parameter_supported: true` Ngay cả khi thiếu các tuyên bố này, các khách hàng hiện tại vẫn cần phải kiểm tra tồn tại `iss`

> 🤔 **【困惑】**Q: Tại sao "精确字符串比较" so so trơn tru?差个尾斜不行?A: 不行――issuer là tất cả các chứng chỉ và token 储存键――若`https://auth.example.com`Với`https://auth.example.com/`视为相等, kẻ tấn công đăng ký带尾斜的相似发行人就能挤进同一储备槽位、继承别人的凭证──OAuth历史上多次账户接管都源于"规范化一下再比"的善意──RFC 9207的设计就是字节级相等──

### Truy cập khán giả tại máy chủ MCP

Các máy chủ tài nguyên chỉ chấp nhận các token được phát hành cho mình:

> 资源服务器 chỉ chấp nhận token tự phát hành:

```text
token.issuer == configured_authorization_server
token.audience == canonical_mcp_resource
```

Các token không hợp lệ, hết hạn, phát hành sai hoặc đối tượng sai nhận 401. Máy chủ MCP không được chấp nhận hoặc chuyển giao một token được dự định cho một dịch vụ khác.

> 无效、过期、错发行者、错受众的代币 一律 401。MCP 服务器不得接受或转运到其他服务发发行的代币──

### yêu cầu phạm vi hiện tại nhỏ nhất

> **【中文解读】**最小权限的落地:先请求当下所需范围;后续工具需要更多时,服务器回归 403 + 权威范围 挑战`WWW-Authenticate`带 `scope`Với`resource_metadata`(■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■`scopes_supported`Các vấn đề đối với các hoạt động hiện tại là quyền lực.

Bắt đầu với phạm vi cần thiết ngay bây giờ. Nếu một công cụ sau này yêu cầu nhiều hơn, máy chủ trả lại 403 với thách thức phạm vi có thẩm quyền:

> Nếu cần thêm công cụ tiếp theo, máy chủ sẽ quay lại với quyền hạn của thách thức 403:

```text
WWW-Authenticate: Bearer error="insufficient_scope",
  scope="notes:delete",
  resource_metadata="https://notes.example.com/.well-known/oauth-protected-resource/mcp"
```

Khách hàng giải thích cho phép mới, nhận được sự đồng ý, thực hiện dòng phép mới với tập hợp phạm vi kết hợp, và thử lại yêu cầu MCP với một ID JSON-RPC mới.

> 客户端向用户解释新权限、获得同意、使用合并后的范围 集执行新的授权流程,然后使用新的 JSON-RPC id 重试 MCP 请求。

Đừng cho rằng phạm vi thách thức là một bộ phận của `scopes_supported`Thách thức này là có thẩm quyền cho hoạt động hiện tại.

> Đừng giả định được thách thức phạm vi là `scopes_supported`                                                                                                                                                                                                                                                              

### Giấy phép và dây MCP không có quốc tịch

> **【中文解读】**授权与协议协商正交:token 授权主体,请求元数据协商协议行为,互不替代──线上校验固定顺序:JSON-RPC 与元数据类型 → 头文相等 → 版本支持──路由/版本头不匹配 回复 400 `-32020`; tiêu đề kết hợp nhưng phiên bản không hỗ trợ trả lại 400 `-32022`且 `data`精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`; Unknown Method 404 `-32601` Mỗi yêu cầu sai lầm (含 401/403) đều là带原请求 id của JSON-RPC 错误信封;`WWW-Authenticate`留在 HTTP 头;通知无 id,接受后 202 空体──

Một cuộc gọi công cụ được ủy quyền vẫn mang gói yêu cầu hiện tại đầy đủ:

> 已授权的工具调用仍需携带完整的当前请求信封:

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

token cho phép người chủ, request metadata đàm phán hành vi giao thức, không thay thế cho người khác.

> token 授权主体; request元数据协商协议行为──两者互不替代──

Thiết lập dây theo thứ tự cố định: JSON-RPC và các loại metadata, tiêu đề và cơ thể bình đẳng, sau đó hỗ trợ giao thức.`-32020`Nếu tiêu đề và cơ thể đồng ý về một phiên bản không được hỗ trợ, trả về HTTP 400 với `-32022`và `data`Đúng vậy.`{"supported":["2026-07-28"],"requested":"<actual>"}`. Một phương pháp không rõ trả về HTTP 404 với `-32601`- Tôi không biết.

> 按固定顺序校验线上格式:JSON-RPC 与元数据类型,头与正文相等等等,然后协议支持──路由或版本头不匹配返回 HTTP 400 `-32020`; tiêu đề kết hợp nhưng phiên bản không hỗ trợ, quay lại HTTP 400 `-32022`且 `data`精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`;未known方法返回 HTTP 404 `-32601`

Mỗi lỗi yêu cầu, bao gồm 401 token không hợp lệ và 403 không đủ phạm vi, là một gói lỗi JSON-RPC với yêu cầu ban đầu `id`. Thông tin phục hồi cấu trúc thuộc về lỗi tùy chọn `data``WWW-Authenticate`vẫn là tiêu đề phản hồi HTTP.`id`, vì vậy nó không nhận được cơ thể JSON-RPC. Một thông báo HTTP được chấp nhận trả lại 202 với một cơ thể trống.

> Mỗi yêu cầu sai lầm bao gồm 401 mã hiệu không hiệu quả và 403 quyền hạn thiếu sót đều là yêu cầu nguyên bản`id`của JSON-RPC 错误信封―― cấu trúc phục hồi thông tin đặt cho lỗi `data`里;`WWW-Authenticate` vẫn là HTTP 响应头──通知没有 `id`, không nhận JSON-RPC 正文; được chấp nhận HTTP 通知 trả về 202 空体──

Các máy chủ thực hiện `server/discover`và quảng cáo các công cụ, vì vậy nó cũng thực hiện các yêu cầu bắt buộc `tools/list`Các mô tả công cụ của nó có tên, mô tả và gốc đối tượng ổn định.`inputSchema`Các giá trị. Danh sách là xác định và trả lại `resultType`, dữ liệu siêu dữ liệu danh tính máy chủ, một giới hạn `ttlMs`, và`cacheScope`- Khám phá và một danh sách công cụ độc lập với người dùng có thể có sẵn trước khi ủy quyền.

> 服务器实现 `server/discover`Và thông báo công cụ, do đó cũng thực hiện những gì cần thiết.`tools/list`方法──工具描述符 có tên gọi, mô tả và gốc vật thể `inputSchema` 列表是确定性的, quay lại `resultType`、 Server ID ID: dữ liệu 、 có giới hạn `ttlMs`和 `cacheScope` Tìm thấy danh sách các công cụ thay đổi không theo người dùng có thể được cung cấp trước khi được cấp phép; nếu thay đổi theo chủ đề, bạn cần áp dụng các chiến lược thông thường và lưu trữ tư nhân.

### Không có thẻ thông qua

Một máy chủ MCP không được chuyển giao mã thông tin truy cập MCP của khách hàng sang một API dòng chảy. Nhận một mã thông báo dòng chảy riêng với khán giả phù hợp hoặc sử dụng thiết kế trao đổi mã thông báo rõ ràng. Việc xác thực khán giả chỉ hoạt động khi các dịch vụ từ chối mã thông báo được đúc cho người khác.

> MCP  máy chủ phải chuyển mã thông báo truy cập MCP của khách hàng  chuyển giao cho API tiếp theo  hoặc nhận mã thông báo tiếp theo độc lập của người dùng, hoặc sử dụng mã thông báo rõ ràng   giao dịch thiết kế  Chỉ có khi người dùng từ chối mã thông báo được gửi cho người khác.

### Tấm mã refresh

Các mã thông báo mới là tùy chọn. Khi được phát hành, lưu trữ chúng bí mật và khóa chúng theo nhà phát hành và nguồn lực. Đừng giả định chúng tồn tại. Chuyển chúng khi máy chủ ủy quyền hỗ trợ quay và phát hiện sử dụng lại các giá trị bị vô hiệu hóa.

> Các mã thông báo refresh là có thể chọn lựa.

```figure
t3-scope-stepup
```

## Hãy xây dựng nó.

> **【中文解读】** `code/main.py`là trong quá trình giao ước và ủy quyền mô phỏng: được bảo vệ tài nguyên phát hiện, ủy quyền máy chủ元数据, CIMD đăng ký, phiên bản kiểm soát DCR quay trở lại, loại ứng dụng, kiểm tra, PKCE, phát hành, kiểm tra, nguồn lực gắn mã, phạm vi, nâng cấp từng bước,`server/discover``tools/list`Với các công cụ không trạng thái yêu cầu một lần chạy. mô hình nhận được yêu cầu đã được phân tích.

`code/main.py`là một mô phỏng giao thức và ủy quyền trong quá trình. Nó thực hiện phát hiện tài nguyên được bảo vệ, dữ liệu siêu dữ liệu máy chủ ủy quyền, đăng ký CIMD, phiên bản được kiểm tra DCR, kiểm tra loại ứng dụng, PKCE, xác thực nhà phát hành, token bị ràng buộc tài nguyên, tăng phạm vi,`server/discover`- `tools/list`, và yêu cầu công cụ vô quốc tịch.

> `code/main.py`là trong quá trình giao ước và ủy quyền mô phỏng: được bảo vệ tài nguyên phát hiện, ủy quyền máy chủ元数据, CIMD đăng ký, phiên bản kiểm soát DCR quay trở lại, loại ứng dụng, kiểm tra, PKCE, phát hành, kiểm tra, nguồn lực gắn mã, phạm vi, nâng cấp từng bước,`server/discover``tools/list`Và một yêu cầu không có trạng thái.

Mô hình nhận được các cơ quan yêu cầu phân tích và tiêu đề định tuyến. Nó không phải là một bộ điều chỉnh HTTP hoàn chỉnh và không phân tích `Content-Type`hoặc `Accept`Kết nối nó với bộ chuyển đổi HTTP Streamable của bài học 09 , đòi hỏi `Content-Type: application/json`và một `Accept`giá trị chứa cả hai `application/json`và `text/event-stream`- Tôi không biết.

> 模型接收已解析的请求正文与路由头, không phải là một HTTP 适配器 hoàn chỉnh, không giải quyết `Content-Type`Hoặc`Accept` đưa nó vào bài học 09 của Streamable HTTP 适配器上那边要求 `Content-Type: application/json`, và`Accept`Đồng thời bao gồm`application/json`Với`text/event-stream`

Đi đi.

> 运行:

```bash
cd phases/13-tools-and-protocols/16-mcp-security-oauth-2-1
python3 code/main.py
python3 -m unittest discover code/tests -v
```

Kết quả xuất hiện cho thấy phát hiện đầu tiên, đăng ký CIMD, đọc thông thường, hai bước tăng phạm vi riêng biệt và lưu trữ tín dụng theo khóa phát hành.

> 输出次展示: phát hiện流程、CIMD注册、一次普通读取、两次独立范围 逐步升级,以及按发行人为关键的证书存储──

## Sử dụng nó thực tế

Bản đồ các đối tượng mô phỏng cho các thành phần sản xuất:

> Để mô phỏng đối tượng được chiếu vào các thành phần sản xuất:

- `ResourceServer.protected_resource_metadata`trở thành điểm cuối RFC 9728.
  Trung ngữ翻译:`ResourceServer.protected_resource_metadata`Đối với RFC 9728 端点
- `AuthorizationServer.metadata`trở thành phát hiện RFC 8414 hoặc OpenID Connect.
  Trung ngữ翻译:`AuthorizationServer.metadata`Đối với RFC 8414 hoặc OpenID Connect 发现
- `Client.enroll`trở thành độ phân giải CIMD cộng với một nhánh tương thích DCR rõ ràng.
  Trung ngữ翻译:`Client.enroll`Đối phó CIMD 解析加显式的 DCR 兼容分支──
- Thông tin tín dụng của khách hàng được phát hành và `tokens_by_issuer_resource`Một URL CIMD có thể vẫn được di động trong khi kết quả ủy quyền của nó vẫn bị ràng buộc bởi nhà phát hành.
  Trung文翻译:issuer 造的客户端凭证和 `tokens_by_issuer_resource`Đối với các hồ sơ mật mã. CIMD URL có thể giữ được chuyển thể, và các kết quả được ủy quyền giữ cho nhà phát hành.
- `ResourceServer.handle`trở thành middleware xác nhận tiêu đề MCP hiện tại, token và phạm vi công cụ trước khi gửi trong khi giữ mọi lỗi yêu cầu trong một gói JSON-RPC phù hợp.
  Trung ngữ翻译:`ResourceServer.handle`Đối với các phần mềm trung gian 分发前校验当前 MCP 头、代码 和工具范围,并让每个请求错误都落在匹配的 JSON-RPC 错误信封里里.

## Chuyển nó đi.

Bài học này sẽ đi theo `outputs/skill-oauth-scope-planner.md`Nó hiện thiết kế ưu tiên đăng ký, lưu trữ chứng chỉ liên quan đến nhà phát hành, loại ứng dụng, PKCE, chỉ số nguồn lực, thách thức phạm vi và ranh giới yêu cầu vô quốc tịch hiện tại.

> 本课产 出 `outputs/skill-oauth-scope-planner.md` Nội dung thiết kế hiện tại bao gồm: đăng ký ưu tiên, nhà phát hành, lưu trữ giấy phép được gắn, loại ứng dụng, PKCE, chỉ dẫn nguồn, phạm vi thách thức, cũng như các yêu cầu không trạng thái hiện tại.

## Tập luyện bài tập

1. Thêm vòng quay mã thông báo refresh và từ chối tái sử dụng mã thông báo refresh trước đó.
   Trung文翻译:添加 refresh token 轮换,并拒绝上一个 refresh token 的重用──
2. Thêm danh sách quyền phát hành. Khi đổi phát hành, chỉ sử dụng lại một URL CIMD di động; từ chối tất cả các thông tin tín dụng và mã thông báo được phát hành trước đó.
   Trung文翻译:添加发行人 允许列表──发行人 变更时只复用可移植的CIMD URL,拒绝之前所有发行人 造的凭证和代币──
3. Thêm hết hạn vào mã ủy quyền và xác nhận việc trao đổi muộn thất bại.
   Trung文翻译:给授权码加过期时间, xác nhận迟到换取失败。
4. Xây dựng một phiên bản client web với một chuyển hướng HTTPS từ xa và so sánh các metadata DCR của nó với client gốc.
   Trung ngữ翻译:构建带远程HTTPS重定向的网 客户端变体,并比较其 DCR 元数据与本地客户端的差异──
5. Thêm một nguồn tài nguyên thứ hai dưới cùng một nhà phát hành. xác nhận mã truy cập của nó không thể được sử dụng tại nguồn tài nguyên đầu tiên.
   Trung文翻译: 在同一发行人 下添加第二资源──确认它的访问代号 不能在第一资源上使用──

## Từ khóa  Từ khóa nhanh chóng

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

## Xem thêm 延伸阅读

- [MCP 2026-07-28 authorization specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
  Trung văn说明:MCP 授权规范正文 文本全部规则的权威来源──
- [RFC 9728: OAuth 2.0 Protected Resource Metadata](https://www.rfc-editor.org/rfc/rfc9728)
  Trung文说明: được bảo vệ tài nguyên dữ liệu RFC phát hiện quy trình bắt đầu.
- [RFC 8707: Resource Indicators for OAuth 2.0](https://www.rfc-editor.org/rfc/rfc8707)
  中文说明: nguồn chỉ dẫn RFCtoken 受众绑定。
- [RFC 9207: OAuth 2.0 Authorization Server Issuer Identification](https://www.rfc-editor.org/rfc/rfc9207)
  中文说明:授权响应 `iss`参数 RFC防 issuer 混。
- [OAuth Client ID Metadata Document draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-client-id-metadata-document/)
  Bài viết:CIMD Draft với URL để đăng ký cơ chế mới của khách hàng nhận dạng
