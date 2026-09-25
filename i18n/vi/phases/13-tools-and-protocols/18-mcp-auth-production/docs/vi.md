# MCP Author in Production: Giấy đăng ký và mã thông báo liên kết với nhà phát hành . MCP 生产级认证:签发者绑定的注册与代币

> Bài học 16 xây dựng máy trạng thái OAuth 2.1. Bài học này làm cứng ranh giới sản xuất của nó cho MCP 2026-07-28: Tài liệu Metadata ID Khách hàng trước, đăng ký động hóa lỗi thời chỉ cho sự tương thích, xác thực cấp phép-phản ứng của nhà phát hành, tín chỉ khách hàng có chìa khóa cấp phép, cập nhật JWKS và token được gắn vào khán giả trên mỗi yêu cầu không có trạng thái.
>
> **Spec note (2026-07-28):**Dynamic Client Registration bị lỗi thời để ủng hộ các tài liệu Metadata ID của khách hàng. DCR vẫn là một cơ chế tương thích. Khi được sử dụng, khách hàng tuyên bố đúng `application_type`. Khách hàng xác nhận RFC 9207 hiện tại `iss`giá trị và không bao giờ sử dụng lại các thông tin tín dụng trên các nhà phát hành máy chủ ủy quyền.

> **【中文解读】**第 16 课搭起了 OAuth 2.1 状态机; 本课把它的边界固固至MCP 2026-07-28 规范的生产要求:注册优先走客户端ID Metadata Document(CIMD),DCR 降级为仅作兼容已废弃路径;授权响应必须校验RFC 9207`iss`; khách hàng bằng chứng theo người phát hành phân biệt lưu trữ; JWKS theo kế hoạch tươi mới; mỗi yêu cầu không trạng thái đều được thực hiện kiểm tra ràng buộc đối tượng.

> **【拓展：MCP 2026-07-28 的注册范式转向】**Đây là phiên bản của quy tắc đăng ký từ "Tuyền" của DCR`POST /register`(CIMD: ủy quyền dịch vụ theo yêu cầu kéo theo khách hàng tự quản của元数据文档),信任 chuyển từ trạng thái nội bộ của IdP sang DNS; đồng thời bằng chứng theo issuer隔离、token 按 issuer,资源) thành kho lưu trữ, chặn qua IdP 复用凭证与跨资源重放 token的攻击面──同一版规范还移除协议会话(见第 23 课毕业项目), đây chính là nguồn gốc của "mỗi yêu cầu phải được xác minh lại"

>  **【前置】**Học本课前请先掌握:(1) giai đoạn 13 · 16(OAuth 2.1 状态机、PKCE、资源指示器) 本课是其生产化;(2) giai đoạn 13 · 17(网关);(3) JWT 结构与 JWKS 概念;(4) 本课将逐渐实现规范:RFC 8414(AS 元数据) 、RFC 7591 ((DCR) 、RFC 8707 ((资源指示器) 、RFC 9728 ((PR 元数据) 、RFC 9207 ((iss 参数) 、RFC 7636 ((PKCE) 、RFC 7662 ((token内省) 、RFC 7009 ((token 吊销) ⋅

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 16 (OAuth 2.1 state machine), Phase 13 · 17 (gateways) | **前置知识:** Phase 13 · 16（OAuth 2.1 状态机）、Phase 13 · 17（网关）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## Mục tiêu học tập

- Khám phá một máy chủ ủy quyền thông qua RFC 8414 siêu dữ liệu và xác minh hợp đồng.
  Trung文翻译:通过 RFC 8414 元数据发现授权服务器并验证契约。
- Đăng vào một Tài liệu Metadata ID Khách hàng và tách DCR lỗi thời như một sự trở lại.
  Trung文翻译:通过 Client ID Metadata Document 完成注册,并把已废弃的 DCR 隔离为后备路径。
- Thiết lập RFC 9207 `iss`, đăng ký chính bởi nhà phát hành máy chủ ủy quyền, và các mã thông báo chính bị ràng buộc tài nguyên bởi nhà phát hành cộng tài nguyên.
  中文翻译:校验 RFC 9207 `iss`; đăng ký thông tin theo ủy quyền của các dịch vụ; tài nguyên được gắn thẻ theo "签发者 + tài nguyên" thành đối với các công cụ:
- Cache và làm mới các phím JWKS theo một lịch trình để xác minh chữ ký tồn tại khi phím được lật lại.
  Trung ngữ翻译:按计划缓存并刷新 JWKS 密钥,使签名验证在密钥轮换后仍然活着──
- Pin token vào một nguồn MCP duy nhất bằng cách sử dụng các chỉ số nguồn RFC 8707 và từ chối tái sử dụng hỗn loạn-đại diện.
  Trung文翻译: dùng RFC 8707 资源指示器把代币 固定到单个MCP 资源,拒绝混代理式重用──
- Chọn xác thực JWT hoặc kiểm tra nội bộ token, xác định tính tươi mới của việc hủy bỏ, và thất bại an toàn khi các phụ thuộc về danh tính không có sẵn.
  Trung ngữ翻译: Trong JWT 校验与代币内省之间做出选择、定义吊销新鲜度,并依赖身份不可用时安全失败──
- Chia tách máy chủ ủy quyền, máy chủ tài nguyên và khách hàng để mỗi người chỉ thực thi kiểm tra của riêng mình.
  Trung ngữ翻译:把授权服务器、资源服务器和客户端分开, để mỗi bên chỉ thực hiện kiểm tra của riêng mình.
- Kiểm tra một máy chủ ủy quyền đối với danh sách kiểm tra triển khai và từ chối đăng ký không an toàn hoặc tái sử dụng token.
  Trung ngữ翻译:按部署检查清单审计授权服务器,拒绝不安全的注册或代币 复用──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**Trò chơi chơi game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game`token.aud`Phân tích độ cứng trên mỗi yêu cầu, cũng là phương tiện duy nhất để phòng chống quá tải tài nguyên.

Máy mô phỏng Bài học 16 chạy OAuth 2.1 trong bộ nhớ.

> Chương 16 课机模拟器在内存中运行 OAuth 2.1  环境生产有三内存模拟器看不到的操作缺口

Sự khác biệt đầu tiên là đăng ký và cách ly tín chỉ. Một tổ chức thực sự có thể chạy hàng trăm máy chủ MCP và hàng ngàn khách hàng MCP.**Client ID Metadata Document**: client sử dụng một URL HTTPS với một con đường mà nó kiểm soát như là nhận dạng của nó, và máy chủ ủy quyền kéo metadata. RFC 7591 đăng ký động chỉ còn lại như một con đường tương thích lỗi thời. Khi DCR là không thể tránh khỏi, yêu cầu tuyên bố chính xác `application_type`. Khách hàng lưu trữ các đăng ký dưới các nhà phát hành máy chủ cấp phép và các token truy cập dưới `(issuer, resource)`Một nhà phát hành thay đổi có nghĩa là một người đăng ký mới, và một nguồn khác có nghĩa là một token riêng biệt đối với khán giả.

> Vỗ khống đầu tiên là phân lập đăng ký và chứng chỉ.**Client ID Metadata Document**: khách hàng sử dụng một đường dẫn tự kiểm soát HTTPS URL như là một trình nhận dạng, ủy quyền máy chủ chủ động lấy dữ liệu. RFC 7591 动态注册 chỉ như là một đường dẫn hợp nhất đã bị bỏ hoang.`application_type` Khách hàng đăng ký thông tin theo ủy quyền của máy chủ gửi lưu trữ, đặt mã thông tin truy cập theo`(issuer, resource)`Đối với kho lưu trữ, người phát hành phải đăng ký lại; nguồn tài nguyên khác phải độc lập để kết nối với người dùng.

Khoảng cách thứ hai là quay chìa khóa. Việc xác thực JWT phụ thuộc vào các khóa ký của máy chủ ủy quyền, được xuất bản dưới dạng một bộ khóa web JSON (JWKS). Các máy chủ ủy quyền xoay chúng theo một lịch trình (thường là hàng giờ, đôi khi nhanh hơn trong phản ứng sự cố). Một máy chủ MCP lấy JWKS một lần khởi động xác nhận tốt cho đến khi cửa sổ quay  sau đó mỗi yêu cầu thất bại cho đến khi khởi động lại. Các dây sản xuất JWKS như một giá trị được lưu trữ trong cache với một công việc làm mới làm việc ghi lại bộ nhớ cache trước khi các khóa trước hết hạn, cộng với một lần thu hồi về cache bị bỏ lỡ cho trường hợp một token được ký bởi một khóa mới hơn bộ nhớ cache đến.

> Vỗ khán thứ hai là khóa thay đổi. JWT xác nhận phụ thuộc vào khóa ký của máy chủ ủy quyền, phát hành dưới dạng JSON Web Key Set (JWKS).

Hỗng thứ ba là liên kết đối tượng. Bài học 16 đã giới thiệu các chỉ số nguồn lực RFC 8707. Trong sản xuất, chỉ số đó trở thành kiểm tra yêu cầu khó khăn trên mọi yêu cầu.`token.aud`chống lại URL nguồn riêng của nó và từ chối sự không phù hợp với HTTP 401. Đây là biện pháp phòng thủ duy nhất chống lại một máy chủ MCP trên dòng (hoặc một khách hàng độc hại nắm giữ một token được thiết kế cho một máy chủ) chơi lại token đó với một máy chủ khác trong cùng một lưới tin cậy.

> Vốn thứ ba là người dùng bị ràng buộc. Chương 16 đã đưa ra RFC 8707  chỉ dẫn nguồn. Trong quá trình sản xuất, chỉ dẫn này trở thành một tuyên bố cứng trên mỗi yêu cầu.`token.aud`Đối với các quy định của riêng mình, URL không phù hợp với HTTP 401  từ chối. Đây là phương tiện duy nhất để gửi token lên một máy chủ hoặc có mã thông báo của một máy chủ khác trong cùng một mạng lưới.

Bài học này sẽ vẽ mỗi khoảng trống trên một mảnh bê tông của bề mặt. Tài liệu siêu dữ liệu là điểm cuối HTTP. JWKS cache refresh là một công việc được lên lịch cộng với một key-value cache. JWT xác thực là một thói quen các nguồn lực máy chủ chạy trước khi gửi bất kỳ công cụ. Giữ ba vai trò riêng biệt và mỗi người chỉ thực thi kiểm tra mà nó sở hữu: máy chủ ủy quyền phát hành và xoay các khóa, máy chủ tài nguyên lưu trữ và xác nhận, khách hàng phát hiện và đăng ký.

> Bài học này sẽ chỉ định mỗi lỗ hổng là một cấu trúc cụ thể trên mặt chứng nhận: tài liệu dữ liệu元 là một HTTP 端点; JWKS 缓存刷新 là một nhiệm vụ cố định thêm một giá trị khóa; JWT 验证 là một quy trình của một bộ máy chủ tài nguyên trước khi phát hành bất kỳ công cụ nào.

## Khả năng: Thực thi sản xuất sau bài học 16  phạm vi: tăng cường sản xuất sau bài học 16

> **【中文解读】**本课不重新定义 OAuth 流程授权码状态机、PKCE、受保护资源发现、资源指示器都属于第16课. 本课从这些契约已经存在之后开始: một bộ phận tài nguyên phục vụ đã được triển khai làm thế nào để tiếp tục thực hiện các契约 trong vòng chuyển khóa、不透明代币、吊销、依赖故障、灰度和事件响应──

[Lesson 16: MCP Security with OAuth 2.1](../../16-mcp-security-oauth-2-1/docs/en.md)sở hữu máy trạng thái mã ủy quyền, PKCE, phát hiện tài nguyên được bảo vệ, chỉ số tài nguyên và quyết định phạm vi. Bài học này không xác định dòng chảy OAuth thứ hai. Nó bắt đầu sau khi các hợp đồng đó tồn tại và hỏi làm thế nào một máy chủ tài nguyên được triển khai tiếp tục thực thi chúng trong quá trình xoay khóa, xác thực mã thông báo không minh bạch, hủy bỏ, thất bại phụ thuộc, triển khai và phản ứng sự cố.

> [第 16 课：MCP Security with OAuth 2.1](../../16-mcp-security-oauth-2-1/docs/en.md)负责授权码状态机、PKCE、受保护资源发现、资源指示器和范围 决策――本课不定义第二个OAuth流程―― nó bắt đầu sau khi các hiệp ước này đã tồn tại, theo dõi một bộ phận của một bộ phận quản lý tài nguyên đã triển khai làm thế nào để thực hiện các hiệp ước này trong quá trình chuyển đổi khóa、 không minh bạch mã thông báo 校验、吊销、依赖故障、灰度发布和事件响应期间──

Biên giới sản xuất hẹp hơn và hoạt động tốt hơn:

> Biên giới sản xuất khắt khe hơn

- Một con đường JWT xác minh một nhà phát hành, thuật toán, khóa ký hiệu, khán giả, yêu cầu thời gian và phạm vi trên mỗi yêu cầu trong khi làm mới JWKS an toàn.
  Trung ngữ翻译:JWT 路径 在每个请求上校验锁定的发发发者、算法、签名密钥、受众、时间声明和范围,同时安全更新 JWKS。
- Một đường đi mã thông báo không minh bạch gọi điểm cuối tự quan sát xác thực của nhà phát hành và xác nhận trạng thái hoạt động, khán giả hoặc nguồn lực, hết hạn, đối tượng và phạm vi được trả lại.
  Trung文翻译:不透明 token 路径调用签发者经认证的内省端点,并校验返回的活跃状态、受众或资源、过期时间、主体和范围──
- Chính sách hủy bỏ xác định tốc độ một giấy chứng nhận phải ngừng hoạt động và cache nào có thể trì hoãn sự kiện đó.
  Trung ngữ翻译:吊销策略定义 một chứng chỉ phải mất hiệu lực trong thời gian ngắn, cũng như những dự trữ nào có thể làm cho sự thật này chậm lại.
- Chính sách thất bại quyết định những gì xảy ra khi phát hiện, JWKS, tự khám phá, hoặc thu hồi cơ sở hạ tầng không sẵn sàng.
  Trung ngữ翻译:故障策略决定当发现、JWKS、内省或吊销基础设施不可用时该怎么办。
- Các hồ sơ bằng chứng mà người phát hành siêu dữ liệu, bộ khóa hoặc phản ứng tự xem, yêu cầu token, phiên bản chính sách và lý do từ chối đã thúc đẩy kết quả mà không lưu trữ token.
  Trung ngữ翻译: chứng cứ ghi chép là những gì người phát hành dữ liệu, khóa tập hợp hoặc nội省 phản ứng, mã thông báo, tuyên bố, phiên bản chiến lược và từ chối đã quyết định kết quả, nhưng không lưu trữ mã thông báo.

Sự phân biệt này giữ cho các bài học được kết hợp. Bài học 16 chứng minh dòng chảy. Bài học 18 chứng minh rằng một token vẫn đáng tin cậy, hoặc bị từ chối, sau khi nó đạt đến một con đường yêu cầu MCP thực sự.

> Điều này chia sẻ làm cho hai bài học được tổ chức: thứ 16  Khóa chứng minh quy trình thành lập; thứ 18  Khóa chứng minh một token sau khi đạt được thực tế MCP yêu cầu đường, hoặc vẫn có thể tin cậy  hoặc bị từ chối.

## Khái niệm cốt lõi

### RFC 8414  OAuth Authorization Server Metadata

Một tài liệu tại `/.well-known/oauth-authorization-server`mô tả mọi thứ mà khách hàng cần:

> 位于 `/.well-known/oauth-authorization-server`                                                                                                                                                                                                                                                              

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

Một client được trao một MCP nguồn URL chuỗi phát hiện: `oauth-protected-resource`từ RFC 9728 (tài liệu của máy chủ tài nguyên) đặt tên cho nhà phát hành, sau đó `oauth-authorization-server`(RFC này) đặt tên cho mỗi điểm cuối. Client không bao giờ mã hóa một URL ủy quyền.

> Nhận được URL của khách hàng của MCP 资源`oauth-protected-resource`(资源服务器的文档) chỉ định người phát hành, tiếp tục`oauth-authorization-server`(本 RFC)列出全部端点──客户端从不硬编码授权 URL──

Đối với một công cụ nhận dạng tài nguyên với một con đường, hãy chèn phần được biết đến trước con đường đó. Ví dụ: `https://mcp.example.com/team/server`giải quyết các metadata nguồn được bảo vệ tại `https://mcp.example.com/.well-known/oauth-protected-resource/team/server`- Thêm vào`/.well-known/...`sau khi con đường nguồn tài nguyên không chính xác.

> Đối với các thông báo nguồn lực của đường, hãy đặt một đoạn được biết đến trước đường.`https://mcp.example.com/team/server`                                                                                                                                                                                                                                                              `https://mcp.example.com/.well-known/oauth-protected-resource/team/server` `/.well-known/...`追加在资源路径后是错写法──

Hợp đồng mà bạn xác minh trước khi tin tưởng một IDP cho MCP:

> Trong信任一个IDP 用于MCP 之前要验证的契约:

- `code_challenge_methods_supported`bao gồm `S256`(PKCE theo RFC 7636).**absent**, máy chủ ủy quyền không hỗ trợ PKCE và khách hàng **MUST**từ chối tiến hành.
  Trung ngữ翻译:`code_challenge_methods_supported`包含 `S256`(RFC 7636 của PKCE)  quy tắc viết rõ ràng:该字段**缺失**即表示授权服务器不支持 PKCE, khách户端**必须**拒绝继续――
- `grant_types_supported`bao gồm `authorization_code`và từ chối `password`và `implicit`- Tôi không biết.
  Trung ngữ翻译:`grant_types_supported`包含 `authorization_code`,并拒绝`password`和 `implicit`
- Ít nhất một con đường đăng ký có sẵn: `client_id_metadata_document_supported: true`(CIMD, ưu tiên), một khách hàng đã đăng ký trước, hoặc `registration_endpoint`(sự tương thích RFC 7591 bị giảm).
  Trung ngữ翻译:至少一条注册路径可用:`client_id_metadata_document_supported: true`(CIMD,首选) 、预注册的客户端, hoặc `registration_endpoint`(RFC 7591 兼容路径 đã bị bỏ qua)
- Nếu`authorization_response_iss_parameter_supported`đúng, khách hàng yêu cầu trả lại RFC 9207 `iss`và so sánh nó chính xác với nhà phát hành đã ghi trước khi chuyển hướng.
  中文翻译:若 `authorization_response_iss_parameter_supported`Vì vậy, khách hàng phải yêu cầu quyền đáp trả trả lại RFC 9207 `iss`, và xác định được số lượng của người gửi bất kỳ yêu cầu nào trước khi gửi và chuyển hướng lại.
- `response_types_supported`chính xác `["code"]`cho OAuth 2.1.
  Trung文翻译:对 OAuth 2.1,`response_types_supported`恰为 `["code"]`

Nếu`S256`Nếu không có, máy chủ MCP từ chối triển khai chống lại IdP này không có chế độ xuống cấp cho PKCE. Nếu *không có * đường đăng ký được quảng cáo và bạn không có đăng ký trước `client_id`, bạn cũng không thể đăng ký; bản ghi việc triển khai là sai, không phải mã.

> Nếu`S256`缺失,MCP 服务器拒绝在此 IdP 上部署PKCE 没有降级模式──若两条注册路径都未公布也没有预注册的`client_id`, cũng không thể đăng ký; lỗi là部署清单, không phải là mã hóa.

### RFC 9728 (sửa lại)  Phụ liệu siêu dữ liệu nguồn được bảo vệ

Bài học 16 bao gồm RFC 9728. Delta trong sản xuất: tài liệu này là nơi duy nhất mà khách hàng tìm kiếm để tìm các máy chủ ủy quyền được tin cậy bởi máy chủ MCP này. Một máy chủ MCP duy nhất có thể chấp nhận token từ nhiều IdP (một cho nhân viên, một cho đối tác). RFC 9728 tuyên bố bộ đó; RFC 8414 tài liệu những gì mỗi IdP hỗ trợ.

> 第 16 课讲过 RFC 9728──增量在生产中是: This document is a clientèle search *此* MCP 服务器信任哪些授权服务器的唯一入口──单个 MCP 服务器可以接受来自多个 IdP的代币──一个给员工一个给合作伙伴──RFC 9728 声明这个集合;RFC 8414 说明每个 IdP 支持什么──

```json
{
  "resource": "https://notes.example.com",
  "authorization_servers": ["https://auth.example.com", "https://partners.example.com"],
  "scopes_supported": ["mcp:tools.invoke"],
  "bearer_methods_supported": ["header"],
  "resource_documentation": "https://notes.example.com/docs"
}
```

### Tài liệu Metadata ID khách hàng (được khuyến cáo mặc định)

> **【中文解读】**CIMD Đặt đăng ký từ "推"反转为"拉": khách hàng sử dụng một con đường HTTPS tự kiểm soát`client_id`, URL này được phân tích thành một JSON 元数据文档, ủy quyền máy chủ trong quá trình OAuth 按需拉取──信任是 DNS信任`app.example.com`Như là bạn đang quản lý nó. Không đăng ký trở lại, không có.`client_id`命名空间可耗尽, không cần phải đồng bộ với từng trạng thái của máy chủ.

CIMD đảo ngược đăng ký từ *push* đến *pull*. Thay vì yêu cầu máy chủ ủy quyền để mint một `client_id`, khách hàng sử dụng một URL HTTPS nó kiểm soát **as**của nó`client_id`. URL được giải quyết thành một tài liệu siêu dữ liệu JSON; máy chủ ủy quyền lấy nó theo yêu cầu trong dòng OAuth.`app.example.com`, nó tin vào khách hàng được phục vụ từ`https://app.example.com/client.json`Không có đăng ký đi lại, không.`client_id`không gian tên để thải, không có trạng thái trên máy chủ để giữ đồng bộ.

> CIMD Đăng ký từ *推*反转为*拉*。客户端不再请求授权服务器造一个 `client_id`, thay vì sử dụng một URL HTTPS tự kiểm soát trực tiếp**充当** `client_id` Các URL 解析 thành một JSON 元数据文档, ủy quyền máy chủ trong quá trình OAuth 按需拉取它──信任以 DNS 为根:如果服务器运营方信任 `app.example.com`, nó dựa trên sự tin tưởng từ `https://app.example.com/client.json`提供服务的客户端. Không đăng ký trở về, không có chi tiêu hết.`client_id`Không cần phải giữ trạng thái của mỗi máy chủ.

Tài liệu siêu dữ liệu mà khách hàng lưu trữ:

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

- `client_id`giá trị trong tài liệu **MUST**bằng với URL mà nó được phục vụ (tạm dịch: server ủy quyền xác minh điều này; sự không phù hợp được từ chối).`client_id_metadata_document_supported: true`trong RFC 8414 metadata của nó.

> 文档中 `client_id`值**必须**等等其托管 URL(授权服务器会验证这一点,不匹配即拒绝) ⋅授权服务器在RFC 8414 元数据中使用 `client_id_metadata_document_supported: true`Công bố hỗ trợ

Đối với hợp đồng hiện tại của CIMD, `client_id`- `client_name`, và không trống `redirect_uris`Các mục tiêu của các ứng dụng này là các mục tiêu của các ứng dụng khác nhau.`application_type`Có thể được bao gồm, nhưng nó không phải là một trường CIMD bắt buộc.`application_type`vào con đường CIMD được ưa thích.

> Về thỏa thuận CIMD,`client_id``client_name`和非空的 `redirect_uris`数组是必填项. Các mục tiêu nhận dạng khách hàng phải là một URL HTTPS tuyệt đối có đường dẫn.`application_type`Có thể, nhưng nó không phải là một phần cần thiết của CIMD. Đừng dùng DCR để đối phó.`application_type`Ưu tiên của chuyển vào CIMD 路径

Hai sự thật về an ninh mà thông số nói thẳng thắn:

> 规范直言不讳的两个安全事实:

- **SSRF.**Các máy chủ ủy quyền lấy một URL được cung cấp bởi kẻ tấn công. Nó phải bảo vệ chống lại giả mạo yêu cầu bên máy chủ (không lấy đến các điểm cuối nội bộ / admin).
  Trung ngữ翻译:**SSRF。**授权服务器会拉取攻击者可提供的URL, phải phòng thủ server端请求伪造(不得拉取内部/管理端点)
- **localhost impersonation.**CIMD một mình không thể ngăn chặn một kẻ tấn công địa phương yêu cầu URL siêu dữ liệu của khách hàng hợp pháp và liên kết bất kỳ `localhost`chuyển hướng. máy chủ ủy quyền **MUST**hiển thị rõ ràng tên chủ URI chuyển hướng trong khi đồng ý và **SHOULD**cảnh báo về `localhost`- Chỉ chuyển hướng.
  Trung ngữ翻译:**localhost 冒充。**Chỉ dựa vào CIMD  không sống trong địa phương kẻ tấn công nhận thức được các mã dữ liệu của khách hàng hợp pháp URL và buộc tùy ý `localhost`chuyển hướng.**必须**Trong đồng ý trang rõ ràng hiển thị chuyển hướng URI 主机名,并**应当**Chỉ có`localhost`Đổi hướng 发出警告──

Vì CIMD không cần trạng thái bên máy chủ, không có nhà đăng ký để đứng lên theo cách DCR yêu cầu. Bên khách hàng chỉ đọc: phục vụ tài liệu siêu dữ liệu của bạn từ điểm cuối HTTPS tĩnh và để máy chủ ủy quyền kéo nó.

> Vì CIMD không cần trạng thái cuối máy chủ, cũng không có DCR đó cần thiết lập đăng ký máy chủ.

Nếu nhà khai thác máy chủ ủy quyền đã cung cấp một nhận dạng khách hàng, hãy sử dụng đăng ký có quy mô của nhà phát hành trước khi thử đăng ký tự động. Nếu không, hãy ưu tiên CIMD. Chỉ sử dụng DCR lỗi thời khi nhà phát hành không thể sử dụng cả đăng ký trước hoặc CIMD.

> Nếu người sử dụng dịch vụ ủy quyền đã phân phối thẻ nhận khách hàng, nên sử dụng đăng ký được xác định bởi người phát hành, hãy thử tự động đăng ký lại. Nếu không, ưu tiên CIMD.

### RFC 7591: Việc ghi danh tính tương thích đã lỗi thời

> **【中文解读】**RFC 7591 动态客户端注册在 2026-07-28 版本被正式废弃, chỉ为无法消费 CIMD 且预注册不现实授权服务器保留──关键变化:`application_type`Không trang trí  quay vòng bảng mặt khách hàng tuyên bố `native`, server托管客户端声明 `web`Và sử dụng HTTPS chuyển hướng URI.`software_statement`校验,`registration_access_token`哈希存储──

DCR đã bị lỗi thời trong phiên bản sửa đổi 2026-07-28. Chỉ lưu trữ cho các máy chủ ủy quyền không thể tiêu thụ CIMD và khi đăng ký trước là không thực tế.

> DCR trong 2026-07-28 修订版中已弃用── chỉ đối với cả hai không thể tiêu thụ CIMD、预注册又不现实授权服务器保留它──兼容客户端 POST:

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

Server trả lời với `client_id`và một `registration_access_token`cho các bản cập nhật sau:

>  máy chủ`client_id`和一个供后续更新使用的 `registration_access_token`响应:

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

`application_type`không phải là trang trí. Một máy tính để bàn lặp lại client tuyên bố `native`; một khách hàng được lưu trữ trên máy chủ tuyên bố `web`và sử dụng HTTPS chuyển hướng URI. `token_endpoint_auth_method: none`là mặc định đúng cho một khách hàng địa phương công cộng.`client_id`Chỉ có PKCE cung cấp bằng chứng sở hữu.

> `application_type`Không phải đặt ra.`native`; dịch vụ quản lý khách hàng tuyên bố `web`并 sử dụng HTTPS chuyển hướng URI.`token_endpoint_auth_method: none`Đó là giá trị mặc định chính xác của khách hàng gốc công cộng.`client_id`, do PKCE cung cấp chứng minh có quyền kiểm soát.

Ba cái bẫy sản xuất:

> 3 cái bẫy sản xuất:

- Điểm cuối đăng ký phải được giới hạn theo IP nguồn. Nếu không có đó, một diễn viên thù địch sẽ viết hàng triệu đăng ký giả và làm hết các `client_id`Thực hiện kiểm tra giới hạn giá trước khi nhà đăng ký xử lý yêu cầu.
  Trung ngữ翻译:注册端点必须按源 IP 限流.`client_id`命名空间──在注册器处理请求之前先跑限流检查──
- `software_statement`(một chứng thực JWT được ký kết cho khách hàng) được yêu cầu bởi một số IDP doanh nghiệp. Phong cách của bài học bỏ qua nó; dây sản xuất một bước xác minh từ chối đăng ký chưa ký từ bất cứ thứ gì khác ngoài localhost chuyển hướng URI.
  中文翻译:某些企业 IdP 要求 `software_statement`(为客户端背书的签名 JWT) ――本课的模仿 跳过它;生产环境要连线一个验证步骤,拒绝来自非本地主持转导 URI 的未签名注册――
- - `registration_access_token`Việc đánh cắp token này có nghĩa là kẻ tấn công có thể viết lại các URL của khách hàng.
  Trung ngữ翻译:`registration_access_token`必须以哈希存储,而非明文.                                                                                                                                                                                                                                                         

### RFC 8707 (sửa lại)  Chỉ số nguồn lực

Bài học 16 đã thiết lập hình dạng. quy tắc sản xuất: mỗi yêu cầu token bao gồm `resource=<canonical-mcp-url>`, và máy chủ MCP xác minh `token.aud`URI Canonical là chỉ số * cụ thể nhất * cho máy chủ: nó sử dụng các chương trình nhỏ chữ và chủ, không có mảnh, và thông thường không có slash sau.**not**được loại bỏ bởi quy tắc  thông số kỹ thuật giữ nó khi cần thiết để xác định một máy chủ MCP riêng lẻ. `https://mcp.example.com`- `https://mcp.example.com/mcp`- `https://mcp.example.com:8443`, và`https://mcp.example.com/server/mcp`là tất cả các URI hợp lệ. chọn một trên mỗi máy chủ và pin`aud`(Phần này sử dụng khán giả khán giả như `https://notes.example.com`cho ngắn gọn; một triển khai đồng chủ nhiều máy chủ MCP dưới một nguồn gốc phân biệt chúng theo đường đi.)

> 第16 课 确立了形态――生产规则: mỗi biểu tượng 请求都带`resource=<canonical-mcp-url>`,MCP  máy chủ trong mỗi cuộc gọi trên chứng nhận `token.aud`匹配与自身资源URL ︎规范 URI 是服务器的*最具体*标识符:scheme与主机 小写、无碎片、按惯例无尾部斜──路径组件**不**Theo quy tắc, khi cần xác định một MCP, quy tắc sẽ giữ nó.`https://mcp.example.com``https://mcp.example.com/mcp``https://mcp.example.com:8443``https://mcp.example.com/server/mcp`Đó là quy định hợp pháp của URI. Mỗi máy chủ chọn một, và đưa ra.`aud`精确固定到它──(本课模仿 为简洁起见用裸主机受众如`https://notes.example.com`; ở cùng nguồn gốc, dưới quản lý nhiều MCP  máy chủ được triển khai bằng cách phân biệt chúng.

### RFC 7636 (sửa lại)  PKCE

PKCE là bắt buộc trong OAuth 2.1.`code_challenge`và `code_verifier`. Server từ chối bất kỳ yêu cầu token nào mà không có xác minh hoặc với xác minh không hash cho thách thức được lưu trữ.

> PKCE trong OAuth 2.1 là bắt buộc.`code_challenge`和 `code_verifier` máy chủ từ chối bất kỳ thiếu hụt nào của xác minh hoặc xác minh 哈希后与存储挑战 不符的代码 请求。

### MCP 2026-07-28 hồ sơ cấp phép

> **【中文解读】**2026-07-28 版保持 OAuth 资源服务器边界, nhưng biến MCP 传输 thành không trạng thái: không có thể缓存身份决定的协议会话, cấp phép do đó đối với mỗi yêu cầu kiểm chứng độc lập.`Authorization: Bearer`Và mỗi yêu cầu phải được xác minh.`aud`- Không.`iss`- Không.`exp`/scope;401/403 của thách thức Used `resource_metadata`指针(没有 `resource`参数); phát hiện đồng thời chấp nhận RFC 8414 với OIDC Discovery; trộn  phòng thủ trên khách hàng (RFC 9207);凭证按签发者隔离;CIMD 优先、DCR 已弃用──

Bản sửa đổi MCP hiện tại giữ ranh giới nguồn lực-thư chủ OAuth trong khi làm cho giao thông MCP không có trạng thái. Không có phiên giao thức để lưu trữ quyết định danh tính.

> Khi MCP  sửa đổi phiên bản giữ OAuth 资源服务器边界, đồng thời đưa MCP 传输变为无状态. Không có thỏa thuận nào có thể được sử dụng để xác định danh tính của nó, cấp quyền do đó cho mỗi yêu cầu kiểm chứng độc lập:

- Thực hiện RFC 9728 được bảo vệ nguồn metadata, và cung cấp vị trí của nó hoặc thông qua `WWW-Authenticate: Bearer resource_metadata="..."`tiêu đề trên 401 **or**URI nổi tiếng `/.well-known/oauth-protected-resource`(SEP-985 đã làm cho tiêu đề tùy chọn với một sự vứt bỏ nổi tiếng).`authorization_servers`trường **MUST**đặt tên ít nhất một máy chủ.
  Trung ngữ翻译: thực hiện RFC 9728 Được bảo vệ tài nguyên dữ liệu, vị trí của nó hoặc thông qua 401 trên của `WWW-Authenticate: Bearer resource_metadata="..."`头给出,**要么**用 URI nổi tiếng `/.well-known/oauth-protected-resource`(SEP-985 把该头变为可选并配已知 回退)`authorization_servers`字段**必须**Ít nhất là một máy chủ.
- Chỉ chấp nhận token qua `Authorization: Bearer ...`**every**yêu cầu  không bao giờ trong chuỗi truy vấn, không bao giờ được xác nhận chỉ khi bắt đầu phiên.
  Trung ngữ翻译: chỉ trong**每个**Xin hãy qua`Authorization: Bearer ...` Đánh giá mã thông báo 绝不放进查询串,绝不能只在会话开始时验证一次──
- Định hành`aud`- `iss`- `exp`, và phạm vi yêu cầu theo yêu cầu.**MUST**xác nhận rằng token đã được phát hành đặc biệt cho nó (khán giả); một dấu hiệu bị thiếu hoặc không phù hợp `aud`được từ chối, không bao giờ được coi là một thẻ hoang dã.
  Trung ngữ翻译:每个请求都验证 `aud``iss``exp`和必需的范围──服务器**必须**验证 token là đặc biệt dành cho nó để phát hành của(những người tham gia);`aud`缺失或不匹配一律拒绝,绝不当作通配符──
- Vào ngày 401/403, quay lại `WWW-Authenticate: Bearer`vận chuyển`error=...`, `resource_metadata="<PRM-URL>"`parameter (URL của tài liệu metadata, *không* nguồn khỏa thân), và `scope="..."``insufficient_scope`(403). Lưu ý: tham số là `resource_metadata`, một chỉ số phát hiện  không có `resource`tham số trong thử thách.
  Trung ngữ翻译: 在 401/403 上返回 `WWW-Authenticate: Bearer`, mang theo`error=...``resource_metadata="<PRM-URL>"`参数(元数据文档的URL,*而非*裸资源),403 的 `insufficient_scope`Tới đây`scope="..."`注意: 該参数叫 `resource_metadata`, một phát hiện chỉ số thách thức không có`resource`参数。
- Authorization-server discovery chấp nhận **either**RFC 8414 OAuth metadata **or**OpenID Connect Discovery 1.0; khách hàng phải thử cả hai hậu tố nổi tiếng theo thứ tự ưu tiên.
  Trung ngữ翻译:授权服务器发现**既** chấp nhận RFC 8414 OAuth 元数据,**也**接受 OpenID Connect Discovery 1.0; khách hàng phải ưu tiên theo lần thử hai loại 后──
- Khách hàng (không phải máy chủ) bảo vệ chống lại **mix-up attacks**: ghi lại những gì mong đợi `issuer`trước khi chuyển hướng và xác nhận `iss`giá trị được trả lại trong phản hồi ủy quyền thực tế (RFC 9207) trước khi đổi mã. PKCE một mình không ngừng trộn lẫn, bởi vì khách hàng giao `code_verifier`đến bất cứ điểm nào mà nó được hướng tới.
  Trung ngữ翻译:**mix-up 攻击**By khách hàng (而非服务器) phòng thủ:重定向前记录预期 `issuer`, trong  đổi mã  trước khi thực sự kiểm tra quyền đáp ứng trong trả lại `iss`Giá trị RFC 9207)  Chỉ dựa vào PKCE  không phải là sự nhầm lẫn, vì khách hàng sẽ`code_verifier`交给它被带走的标志 端点.
- Một chứng chỉ của khách hàng thuộc về một nhà phát hành máy chủ ủy quyền. Nếu phát hiện được giải quyết cho một nhà phát hành khác, khách hàng đăng ký lại thay vì trình bày các thông tin cũ `client_id`, mã đăng ký, hoặc mã truy cập.
  Trung ngữ翻译: một khách hàng chứng chỉ chỉ thuộc về một người phát hành dịch vụ được ủy quyền. Nếu phát hiện ra đã phân tích cho người phát hành khác, khách hàng nên đăng ký lại, thay vì sử dụng cũ.`client_id`、 đăng ký token hoặc access token 去硬。
- CIMD là cơ chế đăng ký Ứng dụng DCR đã bị lỗi thời; yêu cầu DCR tương thích vẫn tuyên bố đúng `application_type`- Tôi không biết.
  Trung ngữ翻译:CIMD 是首选注册机械──DCR已弃用;兼容使用的DCR 请求仍要声明正确的`application_type`

Dự thảo OAuth 2.1 là lớp phụ; RFC 8414/7591/8707/9728/9207 + RFC 7636 + CIMD là bề mặt; đặc điểm MCP là hồ sơ.

> OAuth 2.1 草案 là nền tảng;RFC 8414/7591/8707/9728/9207 + RFC 7636 + CIMD là tầng cao;MCP 规范是配置档──

### Danh sách kiểm tra khả năng triển khai

Các bảng tính năng của nhà cung cấp trở nên lỗi thời nhanh chóng. Kiểm tra các metadata được trả lại bởi máy chủ ủy quyền mà bạn thực sự sẽ triển khai thay vào đó. Cổng là cơ học:

> 厂商功能表很快过期. 改为检查您实际要部署的授权服务器回归元数据. 门控是机械的:

| Check | Required decision |
|---|---|
| Discovered issuer | Exact HTTPS issuer expected by policy |
| PKCE | `S256` advertised; otherwise stop |
| Enrollment | CIMD preferred, pre-registration accepted, DCR only as deprecated compatibility |
| Authorization response | Validate RFC 9207 `iss` when present or advertised |
| Resource binding | Token request carries `resource`; resource server requires the matching `aud` |
| Credential storage | Key client IDs and registration credentials by issuer; key access tokens by issuer plus resource |
| DCR compatibility | Declare `native` or `web`; reject redirect URIs that do not fit the declared application type |

Đừng suy luận hỗ trợ từ một tên sản phẩm hoặc cấp giá.

> Đừng từ sản phẩm tên hoặc giá cả hồ sơ xác định hỗ trợ khả năng.

### Mô hình làm mới của JWKS (tiếng quay tại AS, làm mới tại máy chủ tài nguyên)

> **【中文解读】**区分两个动词:**轮换（rotate）**là ủy quyền cho máy chủ tạo ra chìa khóa mới, phát hành vào JWKS, sau đó loại bỏ chìa khóa cũ;**刷新（refresh）**là tài nguyên máy chủ duy nhất có thể làm gì tái GET  đã được phát hành JWKS vào bộ nhớ.`kid`未命中时做**一次**Đồng thời, chúng ta cũng có thể thay đổi và tạo ra những thứ đã được tạo ra và không bị mất đi.`kid`, cũng sẽ được theo kịp`kid`Đơn hiệu 喷射打成自伤式 DoS──

Hãy giữ hai động từ tách biệt, bởi vì kết hợp chúng là một lỗi sản xuất thực sự:

> Để phân chia hai từ động, sử dụng chúng là lỗi sản xuất thực sự:

- **Rotate**là những gì * máy chủ ủy quyền* làm: đúc một khóa ký mới, xuất bản nó trong JWKS, rút ra cũ sau đó.
  Trung ngữ翻译:**轮换**Đó là việc mà các máy chủ quyền phải làm: tạo ra một khóa ký hiệu mới, phát hành vào JWKS, sau đó loại bỏ khóa cũ.
- **Refresh**là những gì * nguồn lực máy chủ * làm: re-`GET`Đó là hành động duy nhất của JWKS mà một máy chủ tài nguyên thực hiện.
  Trung ngữ翻译:**刷新**Đó là: tái tạo`GET`已发布的 JWKS 进缓存──这是资源服务器唯一会执行的 JWKS 操作──

Các chế độ thất bại sản xuất là một bộ nhớ cache cũ. Giải quyết nó bằng một công việc cập nhật theo lịch trình cộng với một key-value cache.`<issuer>/.well-known/jwks.json`và ghi lại`cache[issuer] = {keys, fetched_at}`- Bộ xác nhận đọc từ bộ nhớ cache đó.`kid`bị mất trong bộ kích hoạt cache **one**Tự cập nhật đồng bộ như một sự lùi, sau đó kiểm tra lại. Điều này xử lý hai trường hợp cùng một lúc: việc cập nhật theo lịch trình, và cửa sổ chồng chéo khóa khi một token được ký bởi một khóa mới hoàn toàn đến trước khi cập nhật theo lịch trình tiếp theo.

> 生产故障模式是缓存过期. Sử dụng một định thời gian làm mới nhiệm vụ thêm một giá trị khóa缓存 giải quyết.`<issuer>/.well-known/jwks.json`Không bao gồm`cache[issuer] = {keys, fetched_at}`❖ kiểm chứng từ ❖ ❖ ❖ ❖ ❖`kid`Không trong lưu trữ,触发**一次**Đồng thời, nó bao gồm hai tình huống: bản cập nhật trong kế hoạch, và "đơn hiệu ký mật khẩu của toàn bộ khóa mới trong kế hoạch tiếp theo bản cập nhật trước khi đến" cửa sổ xếp chồng khóa.

Sự trở lại**must be a re-fetch, never a rotate**Nếu bạn chuyển đường cache-miss sang một quay-và-măng, hai điều sẽ bị phá vỡ: (1) Măng một khóa mới tạo ra một `kid`rằng *still* không phù hợp với token, vì vậy tìm kiếm thất bại dù sao; và (2) một kẻ tấn công phun token với ngẫu nhiên `kid`giá trị buộc một loạt các sáng tạo quan trọng không giới hạn một DoS tự gây ra một lần nữa là vô hiệu, vì vậy một giả `kid`Giá tối đa là một việc làm lãng phí.

> 回退**必须是重新拉取，绝不许是轮换**Nếu bạn đưa kho lưu trữ không định hướng đến "đổi lại và tạo", sẽ xảy ra hai điều xấu: 1) tạo ra chìa khóa mới.`kid`* vẫn *匹配不上代币,查找照样失败;(2) 攻击者随机 `kid`喷射 token,逼出无限密钥创建自伤式DoS──重新拉取是等,伪造的`kid`Lần cuối cùng mất một lần để lấy.

Hình dạng cache:

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

Hai phím cùng một lúc là trạng thái ổn định.`k_2026_04`) trước khi rút khỏi cuộc (`k_2026_03`), vì vậy các token được phát hành theo khóa cũ vẫn còn hợp lệ cho đến khi hết hạn.`kid`- Tôi không biết.

> Đồng thời có hai chìa khóa là ổn định.`k_2026_04`),再退役前一个(`k_2026_03`), do đó, biểu tượng của khóa cũ được phát hành vẫn còn hiệu quả trong quá khứ.`kid`选用──

>  **【类比】**JWKS 刷新像消防站的密码本──授权局(消防局) thường xuyên đổi mã hóa(tên ký 密钥),各消防站(MCP 服务器) phải người tay一册最新密码本,否则夜间演习(凌晨3点的用户请求)全部认证失败。正确姿势:各站订阅定时换发(cron 刷新);新旧密码并行一段时间(重叠窗口);有人拿新密码敲门而本子还没有更新时,现场打电话核实一次(缓存未决步回回) 而不是自己编写一个新密码(rotate-as-fallback,将随机敲门变成无止境的印刷新密码)

### Các quy trình xác thực

Máy chủ MCP chạy xác thực trước khi gửi bất kỳ công cụ nào.`code/main.py`sử dụng:

> MCP  máy chủ đang phát triển bất kỳ công cụ nào trước khi chạy thử nghiệm.`code/main.py`形态:

```python
result = server.validate(bearer_token, required_scope="mcp:tools.invoke")
if not result["valid"]:
    return {"status": result["status"], "WWW-Authenticate": result["www_authenticate"]}
```

`validate`giải mã JWT, giải quyết khóa ký từ bộ nhớ cache JWKS (phục hồi một lần khi bị bỏ qua), xác minh chữ ký, sau đó kiểm tra `iss`chống lại danh sách cho phép, `aud`chống lại nguồn tài nguyên của máy chủ này,`exp`, và phạm vi yêu cầu  trả lại một `WWW-Authenticate`thách thức khi thất bại đầu tiên. Giữ nó một thói quen duy nhất trên máy chủ tài nguyên có nghĩa là mọi điểm nhập cảnh (mỗi cuộc gọi công cụ, mỗi vận chuyển) đi qua các kiểm tra tương tự; không có con đường nào đến một công cụ mà không xác nhận trước.

> `validate`解码 JWT, từ JWKS 缓存解析签名密钥(未命中时刷新一次),验证签名,然后把 `iss`Để xem cho phép danh sách `aud`Đối với quy định của máy chủ này`exp`Và bao giờ cũng không thể quay lại`WWW-Authenticate`thách thức: để giữ nó như một đơn vị trên máy chủ tài nguyên, có nghĩa là mỗi lần nhập thông qua mỗi công cụ được sử dụng, mỗi loại truyền thông đều trải qua cùng một bộ kiểm tra; không có chứng cứ chưa có kinh nghiệm về các đường đến các công cụ.

### Các token không rõ ràng sử dụng sự nhìn vào bản thân, không phải đoán

> **【中文解读】**Không phải tất cả các mã thông báo truy cập đều là JWT. Nếu người phát hành phát hành mã thông báo không minh bạch, tài nguyên máy chủ không thể giải mã ra một tuyên bố đáng tin cậy, phải gửi mã thông báo qua chứng nhận của bên sau của đường dẫn đến RFC 7662 bên trong điểm cuối của người phát hành, yêu cầu.`active: true`、 được dự kiến phát hành trên các bản ghi dưới đây、 xác định MCP người nhận hoặc tài nguyên、 thời gian chưa hết hạn và phạm vi cần thiết cho công cụ này。缓存 theo " phát hành viên + token  đơn hướng trích dẫn + MCP  tài nguyên" làm chìa khóa, không cần thiết để làm thẻ ghi chép hoặc thẻ缓存.

Không phải tất cả các token truy cập đều là JWT. Nếu nhà phát hành ghi lại một token không minh bạch, máy chủ tài nguyên không thể giải mã nó thành các tuyên bố đáng tin cậy. Nó gửi token đến điểm cuối tự dò RFC 7662 của nhà phát hành qua một kênh ngược xác thực và yêu cầu`active: true`, bối cảnh nhà phát hành dự kiến, khán giả hoặc nguồn tài nguyên MCP chính xác, yêu cầu thời gian chưa hết hạn và phạm vi yêu cầu của công cụ cụ thể.

> Không phải mỗi token truy cập đều là JWT. Nếu người phát hành phát hành một token không minh bạch, resource server không thể giải mã nó thành một tuyên bố đáng tin cậy. Nó đưa token 经认证 后端通道发送到发发行者的 RFC 7662 内省端点,并要求`active: true`、 báo cáo về thời gian chưa hết hạn của MCP được dự kiến và phạm vi cần thiết cho công cụ cụ thể này.

Cache introspection bởi nhà phát hành, một đường tiêu hóa token, và nguồn MCP. Đừng bao giờ sử dụng token rõ ràng như một thẻ ghi nhật ký hoặc cache. Kết nối một mục cache tích cực bằng thời gian hết hạn token sớm nhất, hướng dẫn cache của nhà phát hành và mục tiêu mới của việc khai thác. Giữ cache tiêu cực đủ ngắn để token mới được phát hành không bị vô hiệu hóa. Kết quả cho một nguồn tài nguyên không thể ủy quyền cho nguồn tài nguyên khác ngay cả khi chuỗi mã thông báo không rõ ràng là giống nhau.

> Trong khi đó, các mã hóa được sử dụng để lưu trữ trong các mã hóa khác nhau, trong đó có mã hóa có thể được sử dụng để lưu trữ trong các mã hóa khác. Các mã hóa có thể được sử dụng để lưu trữ trong các mã hóa khác.

Không chọn chế độ xác thực từ nội dung mã thông báo do kẻ tấn công kiểm soát. Pin JWT so với hành vi tự quan sát đến dữ liệu siêu dữ liệu của nhà phát hành được xác nhận và cấu hình triển khai. Trên con đường JWT, pin chấp nhận thuật toán và tin cậy `jwks_uri`; không bao giờ theo URL hoặc thuật toán chính chỉ được chọn bởi tiêu đề token.

> Không dựa trên mã thông báo có thể kiểm soát được của kẻ tấn công  Nội dung chọn phương thức xác minh  Đưa "JWT còn là nội bộ" đóng vào các dữ liệu và phân bố của người phát hành đã được xác minh  Trên đường JWT, khóa các thuật toán được chấp nhận và đáng tin cậy `jwks_uri`; không chỉ theo chỉ từ mã thông báo 头指定的密钥URL或算法──

### Tháo lại là một hợp đồng tươi mới

RFC 7009 cho phép khách hàng yêu cầu một máy chủ ủy quyền hủy bỏ một token. yêu cầu đó không xóa các bản sao đã được lưu trữ trong cache của mỗi máy chủ tài nguyên. Định nghĩa thời gian trễ hủy bỏ tối đa và làm cho mỗi bộ nhớ cache tôn trọng nó.

> RFC 7009 cho phép yêu cầu của khách hàng ủy quyền cho máy chủ hủy bỏ token. Nhưng yêu cầu này sẽ không xóa bỏ bản sao đã được lưu trữ bởi mỗi tài nguyên máy chủ.

Việc triển khai mã thông báo không rõ ràng có thể đạt được sự hủy bỏ chặt chẽ hơn bằng cách theo dõi nội bộ vào mỗi cuộc gọi có rủi ro cao hoặc sử dụng cache tích cực ngắn. Việc triển khai JWT tự chủ thường kết hợp thời gian sống của mã thông báo truy cập ngắn với việc hủy bỏ mã thông báo cập nhật, rút tiền khóa cho các sự cố toàn bộ nhà phát hành và một chủ đề tùy chọn, phiên hoặc danh mục mã thông báo cho việc từ chối địa phương khẩn cấp. Một JWT được ký kết vẫn có hiệu lực mật mã cho đến khi hết hạn trừ khi máy chủ tài nguyên có bằng chứng khước từ bên ngoài hiện tại.

> Việc triển khai mã thông minh có thể được thực hiện trong nội bộ hoặc sử dụng tạm thời để giảm thiểu, thực hiện việc bỏ phiếu chặt chẽ hơn. Bản thân chứa JWT  triển khai thường được sử dụng: mã thông báo truy cập ngắn có hiệu quả + mã thông báo làm mới  bỏ phiếu  hướng tới toàn bộ sự kiện của người phát hành.

Logout, vô hiệu hóa tài khoản, rút tiền đồng ý và phản ứng xảy ra là các yếu tố kích hoạt khác nhau nhưng phải hội tụ trên một tuyên bố có thể đo lường: tối đa sau khi cửa sổ hủy bỏ được tuyên bố, mỗi bản sao từ chối giấy chứng nhận.

> 登登,账号停用,撤回同意和事件响应是不同的触发器, nhưng phải nhận được một câu nói có thể đo lường: đến nhiều sau khi cửa sổ hủy bỏ của tuyên bố, mỗi bản đã từ chối giấy chứng nhận này.

### Sự thất bại của sự phụ thuộc cần một quyết định được tuyên bố

> **【中文解读】**Các chiến lược có thể được sử dụng không thể được phát triển ngay lập tức trong các bộ xử lý bất thường.`kid`且唯一回退失败→拒绝;内省不可用→失败关闭;元数据意外变更→停止新注册;吊销端点不可用→如实报告未完成;时钟源或声明类型无效→拒绝而非放宽偏差)  Bằng chứng lệ thuộc故障与无效必须分类:前者是带健康和重试策略运维错误,后者是授权拒绝两者都到不到工具处理器,也都不允许将代码内容泄漏到审计证书中.

Không bao giờ improvise chính sách sẵn có bên trong một người xử lý ngoại lệ.

> Không có bất kỳ xử lý trong lập trình lập ra các chiến lược có thể sử dụng.

| Failure | Safe production behavior |
|---|---|
| Scheduled JWKS refresh fails, known `kid` remains in a still-valid bounded cache | Continue only within the declared stale-on-error window and emit degraded health evidence |
| Token has an unknown `kid` and the one allowed refresh fails | Reject; never accept an unverifiable signature |
| Introspection is unavailable | Fail closed for protected calls; do not convert network failure into `active: true` |
| Protected-resource or issuer metadata changes unexpectedly | Stop new enrollment and token acquisition; keep only explicitly pinned, unexpired configuration under a bounded incident policy |
| Revocation endpoint is unavailable | Report logout or revocation as incomplete, retain the credential locally as unusable when possible, and do not claim global revocation succeeded |
| Clock source or claim type is invalid | Reject rather than widening skew until the token passes |

Đánh phân loại các lỗi riêng biệt với các thông tin tín dụng không hợp lệ. Một sự gián đoạn phụ thuộc là một lỗi hoạt động với chính sách sức khỏe và thử lại. Một chữ ký, nhà phát hành, khán giả, hết hạn hoặc phạm vi không hợp lệ là từ chối ủy quyền. Cả hai không tiếp cận người xử lý công cụ, và cả hai không nên rò rỉ nội dung token vào bằng chứng kiểm toán.

> Để dựa vào lỗi và vô hiệu lực chứng chỉ phân chia thành phân loại. Việc dựa vào sự gián đoạn là một sai lầm trong hoạt động của chiến lược kiểm tra sức khỏe và tái kiểm tra; sai ký ▌được phát hành, người nhận, thời hạn hoặc phạm vi là quyền từ chối.

### Khán giả-playback walkthrough (các hạn chế quyền truy cập mã thông báo)

> **【中文解读】**受众重放演练:Server A(notes.example.com) với Server B(tasks.example.com) đăng ký vào cùng một máy chủ ủy quyền;A 被陷入后攻击者拿用户的笔记符号 去敲 B。B的验证器在第三步检查`aud == "https://tasks.example.com"`失败, quay lại 401 không đi `resource_metadata`Chỉ số: Các tuyên bố của người nhận là mức độ thỏa thuận duy nhất để phòng thủ các loại tấn công này.**access-token privilege restriction**:MCP 服务器 `MUST`拒绝任何受众里没有点它名字的代币──注意术语:*Phác sĩ bối rối* 留给了另一个问题MCP 代理使用静态客户ID 转发代币 且未获得每户端同意──

Server A (`notes.example.com`) và Server B (`tasks.example.com`(b) cả hai đăng ký với cùng một máy chủ ủy quyền. Server A bị xâm phạm. kẻ tấn công lấy token ghi chú của người dùng và đánh lại nó với Server B.

> 服务器 A`notes.example.com`) với máy chủ B`tasks.example.com`(c) đã đăng ký vào cùng một máy chủ ủy quyền. A bị tấn công.

Tác giả của máy chủ B:

> 服务器 B 的验证器:

1. Khóa mã JWT, lấy JWKS qua `kid`, xác minh chữ ký.
  中文翻译:解码 JWT,按 `kid`取 JWKS,验证签名──
2. Chuyện này`iss`chống lại các metadata của nó được bảo vệ trong tài nguyên `authorization_servers`(Tạo qua cùng IDP.)
  Trung ngữ翻译:把 `iss`Đối với các tài nguyên được bảo vệ của dữ liệu`authorization_servers`( thông qua cùng IDP。)
3. Chuyện này`aud == "https://tasks.example.com"`(Thất bại  token `aud`là `https://notes.example.com`.)
  Trung ngữ翻译:检查 `aud == "https://tasks.example.com"`◊(失败token của `aud` `https://notes.example.com`◊)
4. Trả lại 401 với `WWW-Authenticate: Bearer error="invalid_token", error_description="audience mismatch", resource_metadata="https://tasks.example.com/.well-known/oauth-protected-resource"`- Tôi không biết.
  Trung ngữ翻译:返回 401,带 `WWW-Authenticate: Bearer error="invalid_token", error_description="audience mismatch", resource_metadata="https://tasks.example.com/.well-known/oauth-protected-resource"`

Tầm nhìn của khán giả là biện pháp phòng thủ duy nhất chống lại cuộc tấn công này ở lớp giao thức. Trượt nó để hiệu suất là sai lầm sản xuất phổ biến nhất; trình xác thực phải chạy trên mọi yêu cầu, không chỉ tại buổi bắt đầu.**access-token privilege restriction**: một máy chủ MCP `MUST`từ chối bất kỳ biểu tượng nào không nêu tên nó trong khán giả.

> Thông báo người dùng là phương tiện duy nhất để phòng thủ cuộc tấn công này trên tầng thỏa thuận.**access-token privilege restriction**(trình hiệu truy cập 特权限制):MCP 服务器 `MUST`拒绝任何受众中未点名的标志──

> **Naming note.**Các thông số đặc trưng dành cho thuật ngữ * confused deputy* cho một vấn đề liên quan nhưng rõ ràng: một máy chủ MCP hoạt động như một OAuth **proxy**cho một API bên thứ ba, sử dụng ID khách hàng tĩnh, chuyển giao token mà không cần nhận sự đồng ý của người dùng mỗi khách hàng. Audience binding sửa chữa việc lặp lại ở trên; sự cố nhầm lẫn-đại diện là sự đồng ý của mỗi khách hàng **plus**không bao giờ chuyển token nhập qua các API trên dòng (mạng máy chủ MCP `MUST`có được token riêng của mình trên dòng chảy).

### Các cuộc tấn công hỗn hợp (một phòng thủ bên khách hàng mà máy chủ không thể cung cấp)

Một client nói chuyện với nhiều máy chủ ủy quyền trong suốt cuộc đời của nó. Một AS độc hại có thể cố gắng để làm cho khách hàng đổi mã ủy quyền của AS trung thực tại điểm cuối token của kẻ tấn công. Kết nối khán giả không giúp ở đây  cuộc tấn công xảy ra trước khi bất kỳ token nào tồn tại.

> 客户端一生会与许多授权服务器打交交道──恶意 AS có thể设法让客户端把诚实AS的授权码拿到攻击者的代币 端点去换──受众绑定在这里帮不上忙攻击发生在任何代币存在之前──防御在客户端一侧(RFC 9207):

1. Trước khi chuyển hướng, khách hàng ghi lại dự kiến `issuer`từ các metadata AS được xác nhận.
  Trung ngữ翻译:重定向之前,客户端从已验证的AS 元数据记录预期的 `issuer`
2. Trên câu trả lời ủy quyền, khách hàng so sánh các trả lại `iss`tham số đối với nhà phát hành đã ghi (sự so sánh chuỗi đơn giản, không có bình thường hóa) trước khi gửi mã bất cứ nơi nào.
  Trung ngữ翻译: nhận được quyền đáp ứng khi, khách hàng ở bất cứ nơi nào gửi mã  trước, đưa trở lại `iss`参数与记录的签发者比对 (nên không làm quy định)
3. Không phù hợp (hoặc `iss`Không có khi AS quảng cáo `authorization_response_iss_parameter_supported`) → từ chối, và thậm chí không hiển thị `error`các cánh đồng.
  中文翻译:不匹配(或 AS 已公布 `authorization_response_iss_parameter_supported`Nhưng thiếu sót`iss`)→ 拒绝,连 `error`字段都不要展示──

PKCE một mình không ngừng nhầm lẫn, bởi vì khách hàng giao cho mình `code_verifier`cho bất kỳ điểm cuối token nào mà nó được hướng đến.`state`- Tôi không biết.

> Chỉ PKCE  không sống nhầm lẫn, vì khách hàng sẽ `code_verifier`交给它被引入的代币端点. Đó là quy tắc để đưa người phát hành và xác minh PKCE.`state`Một khởi đầu theo yêu cầu ghi lại nguyên nhân:

### Các chế độ thất bại

- **Stale JWKS.**Các xác thực viên từ chối mã thông báo hợp lệ sau khi AS quay một khóa. sửa chữa là cron-refresh + cache-miss-refetch pattern trên. Không bao giờ cache JWKS mà không có một công việc refresh.
  Trung ngữ翻译:**过期 JWKS。**AS 轮换密钥后验证器拒绝有效代币──修复是上述的定时刷新 + 未命中重拉模式──绝对没有刷新任务的情况下缓存 JWKS──
- **Rotate-as-fall-back.**Cáp đường cache-miss đến một quay-và-mint thay vì một lại-phát là một lỗi thực sự: nó không bao giờ tạo ra các mất `kid`, và nó trở thành bị kẻ tấn công kiểm soát .`kid`giá trị vào một DoS tạo khóa.`refresh-jwks`- Tôi không biết.
  Trung ngữ翻译:**把轮换当回退。**Để chuyển lưu trữ không định hướng đến "đổi lại và tạo" thay vì tái tạo là lỗi thực sự: nó sẽ không bao giờ tạo ra không bị mất.`kid`, sẽ khiến kẻ tấn công có thể kiểm soát được .`kid`值变成密钥创建 DoS──回退必须是等等的 `refresh-jwks`
- **Missing `aud` claim.**Một số IDP mặc định để bỏ qua `aud`trừ khi`resource`được có trong yêu cầu token. Người xác nhận phải từ chối token với thiếu `aud`, không coi sự vắng mặt như một món đồ hoang dã.
  Trung ngữ翻译:**缺失 `aud` 声明。**Một số IDP 默认省略 `aud`, trừ khi biểu tượng yêu cầu trong mang theo `resource` Máy kiểm tra phải từ chối thiếu hụt`aud`Đồ biểu tượng, thay vì biến mất thành một biểu tượng.
- **Mix-up via missing `iss` check.**Một khách hàng không xác nhận RFC 9207 `iss`tham số ủy quyền-đáp ứng đối với nhà phát hành nó đã ghi lại trước khi chuyển hướng có thể được hướng đến trả lại mã AS trung thực tại điểm cuối token của kẻ tấn công. Đây là một lỗi phía khách hàng; máy chủ tài nguyên không thể bù đắp cho nó.
  Trung ngữ翻译:**缺 `iss` 检查导致 mix-up。**Không phân RFC 9207 `iss`授权响应参数与重定向前记录的发发件者比对客户端, có thể được dẫn đến mã AS của token của kẻ tấn công 端点去换诚实 AS.
- **Scope upgrade race.**Hai dòng tăng tốc đồng thời cho cùng một người dùng có thể cả hai thành công và tạo ra hai token truy cập với phạm vi khác nhau. Người xác thực phải sử dụng token được trình bày trên yêu cầu, chứ không phải tìm kiếm " phạm vi hiện tại của người dùng"  tạo ra cửa sổ TOCTOU.
  Trung ngữ翻译:**scope 升级竞态。**Cùng với hai biến động của cùng một người dùng bước lên 流程都可能成功, tạo ra hai phạm vi khác nhau của các mã thông tin truy cập  chứng thực phải sử dụng mã thông tin được trình bày trên yêu cầu, thay vì để xem "những mã thông tin hiện tại của người dùng"  sẽ mở cửa sổ TOCTOU 
- **Registration token theft.**Một vụ rò rỉ`registration_access_token`cho phép kẻ tấn công viết lại chuyển hướng URI. Hash chúng trong yên tĩnh; yêu cầu khách hàng trình bày văn bản rõ ràng trong mỗi cập nhật; quay trên nghi ngờ.
  Trung ngữ翻译:**注册 token 被盗。**漏漏的 `registration_access_token`让攻击者可以改写转导 URI──静态哈希存储; yêu cầu khách hàng mỗi lần cập nhật xuất hiện明文;
- **`iss` not pinned.**Một người xác nhận chấp nhận bất kỳ`iss`cho phép một kẻ tấn công lập máy chủ ủy quyền riêng của họ, đăng ký một khách hàng cho đối tượng mục tiêu, và phát hành token.`authorization_servers`danh sách là danh sách cho phép; thực thi nó.
  Trung ngữ翻译:**`iss` 未锁定。** chấp nhận bất cứ điều gì `iss`Các chứng thực sẽ cho phép kẻ tấn công tự xây dựng một máy chủ ủy quyền, để mục tiêu đăng ký khách hàng và phát hành token.`authorization_servers`列表就是允许列表;强制执行它.
- **Credential or token cache collision.**Một khách hàng chỉ khóa đăng ký bằng tài nguyên có thể trình bày danh tính của một máy chủ ủy quyền cho một máy chủ khác. Một khách hàng chỉ khóa truy cập token bởi nhà phát hành có thể chơi lại một token với khán giả sai.`(issuer, resource)`, và đăng ký lại bất cứ khi nào nhà phát hành thay đổi.
  Trung ngữ翻译:**凭证或 token 缓存碰撞。**Chỉ theo tài nguyên được đăng ký là khóa cho khách hàng, sẽ chuyển giao một danh tính của máy chủ ủy quyền cho một người khác; chỉ theo người phát hành cho thẻ truy cập làm khóa cho khách hàng, sẽ chuyển thẻ vào người xem sai lầm.`(issuer, resource)`Làm chìa khóa,签发者一变就重新注册──

```figure
t3-jwks-rotate
```

## Hãy sử dụng nó để thực hiện

> **【中文解读】** `code/main.py`用标准库 Python 和三个角色(`AuthorizationServer``ResourceServer``Client`)走完整生产流程:发布 RFC 8414 元数据 → 检查注册选项与 S256 → 优先发行人级预注册/CIMD、DCR 单独可测 → 记录签发者并校验授权响应 `iss`→ PKCE + RFC 8707 资源指示器 → Bearer 调用工具 → JWKS 缓存验证 → 密钥轮换后无需重启继续验证 → 受众重放得到 401。

`code/main.py`đi bộ dòng sản xuất đầy đủ với stdlib Python và ba vai trò: `AuthorizationServer`- `ResourceServer`, và`Client`- Dòng chảy:

> `code/main.py`用标准库 Python 和三个角色`AuthorizationServer``ResourceServer``Client`走完整生产流程──流程:

Từ nguồn kho, chạy:

> Trong thư mục lưu trữ:

```bash
cd phases/13-tools-and-protocols/18-mcp-auth-production
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

Chỉ thị đầu tiên in đăng ký và xác thực token liên quan đến nhà phát hành
lệnh thứ hai báo cáo mười tám kiểm tra vượt qua.
người nghe mạng hoặc viết thông tin tín dụng.

> Điều thứ nhất lệnh ấn ấn ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký ký

1. Server ủy quyền xuất bản RFC 8414 metadata tại `/.well-known/oauth-authorization-server`- Tôi không biết.
  Trung ngữ翻译:授权服务器在 `/.well-known/oauth-authorization-server`发布 RFC 8414 元数据──
2. Khách hàng MCP gọi đến điểm kết metadata và kiểm tra các tùy chọn đăng ký của nó (`client_id_metadata_document_supported`cho CIMD, `registration_endpoint`cho DCR) và `S256`Hỗ trợ PKCE.
  Trung ngữ翻译:MCP 客户端调用元数据端点,检查注册选项(CIMD 看 `client_id_metadata_document_supported`,DCR 看 `registration_endpoint`) với `S256`PKCE 支持。
3. Khách hàng kiểm tra cho một đăng ký trước được cấp phép của nhà phát hành, nếu không đăng ký với HTTPS ID Client Metadata Document của mình. DCR bị suy giảm vẫn là một phương pháp tương thích có thể kiểm tra riêng.
  Trung文翻译:客户端先查按签发者划定的预注册,否则使用其 HTTPS Client ID Metadata Document 注册──已废弃的 DCR 仍保留为可单独测试的兼容方法──
4. Khách hàng ghi lại nhà phát hành được xác nhận, tạo ra một thách thức S256, nhận được mã ủy quyền một lần cộng với `iss`, xác nhận nhà phát hành trả lại, và đổi mã bằng chứng thực gốc và RFC 8707 `resource`chỉ số.
  Trung ngữ翻译:客户端记录已验证的签发者, tạo thử thách S256, nhận được mã quyền một lần và `iss`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,`resource`指示器 换代码──
5. MCP client gọi một công cụ trên máy chủ MCP với `Authorization: Bearer ...`- Tôi không biết.
  Trung ngữ翻译:MCP 客户端以 `Authorization: Bearer ...`调用 MCP  các công cụ trên máy chủ.
6. MCP máy chủ chạy `validate`, giải quyết khóa ký từ bộ nhớ cache JWKS.
  中文翻译:MCP 服务器运行 `validate`, từ JWKS 缓存解析签名密钥──
7. IdP xoay một phím; việc làm mới được lên kế hoạch kéo lại JWKS vào bộ nhớ cache.
  Trung文翻译:IdP 轮换一个密钥;定时刷新把JWKS 重新拉进缓存──
8. Cuộc gọi tiếp theo xác nhận với các phím được cập nhật mà không khởi động lại, và token trước đó vẫn xác nhận trong cửa sổ chồng chéo.
  Trung ngữ翻译: lần sau调用无需重启即针对刷新后的密钥验证,且旧代币在重叠窗口内仍然有效──
9. Một nỗ lực tái diễn đối với một nguồn tài nguyên khác của MCP sẽ có 401 với`audience mismatch`và một `resource_metadata`- Điểm chỉ.
  Trung文翻译: đối với một nguồn tài nguyên khác của MCP`audience mismatch`和 `resource_metadata`Chỉ thị

JWT ở đây sử dụng HS256 với một bí mật được chia sẻ (vì vậy bài học chỉ chạy trên stdlib). sản xuất sử dụng RS256 hoặc EdDSA với mô hình JWKS ở trên; logic xác thực là giống nhau. Bởi vì IdP và máy chủ tài nguyên sống trong một quá trình,`refresh_jwks`đọc danh sách khóa của máy chủ ủy quyền trực tiếp; qua dây là một HTTP `GET`đến`jwks_uri`- Tôi không biết.

> Trong đây, JWT sử dụng HS256 cộng chia sẻ (shared key) để làm cho bài học này chỉ hoạt động trên standard library)  sản xuất sử dụng RS256 hoặc EdDSA cộng với mô hình JWKS trên; xác nhận logic còn lại hoàn toàn giống nhau.`refresh_jwks`直接读授权服务器的密钥表;走线缆时它就是对`jwks_uri`Một lần HTTP `GET`

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-mcp-auth.md`. Với cấu hình máy chủ MCP và một bộ khả năng IdP, kỹ năng phát ra bề mặt auth để đứng lên  các metadata nguồn được bảo vệ, con đường đăng ký để sử dụng (CIMD, đăng ký trước hoặc DCR fallback), lịch trình làm mới JWKS, bản đồ phạm vi và các quy tắc từ chối áp dụng khi IdP không hỗ trợ toàn bộ hồ sơ RFC.

> 本课产 出 `outputs/skill-mcp-auth.md` Đưa ra MCP  máy chủ cấu hình và IdP  năng lực tập hợp, kỹ năng phát triển cần thiết thiết thiết lập chứng nhận  được bảo vệ tài nguyên dữ liệu  phải sử dụng tuyến đường đăng ký  CIMD  đăng ký trước hoặc DCR 后备)  JWKS 刷新计划、 phạm vi 映射, cũng như IdP không đáp ứng đầy đủ các quy tắc từ chối khi configure RFC 

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Theo dõi dòng chảy. Nhận thấy cách IdP xoay một phím trong bước 6, các kế hoạch `refresh_jwks`kéo lại bộ đã xuất bản, và cả token cũ (trung cửa sổ chồng chéo) và token mới được xác nhận mà không cần khởi động lại.
   Trung ngữ翻译:运行 `code/main.py`, theo dõi quy trình. chú ý bước 6 IDP  làm thế nào để chuyển đổi khóa 定时`refresh_jwks`如何重拉已发布的密钥集,以及旧代币 (旧代币) 和新代币 (新代币) 如何都无需重启即可验证──

2. Thêm một IDP mới vào metadata nguồn được bảo vệ `authorization_servers`list. phát hành một token được ký bởi IDP mới và xác nhận người xác nhận chấp nhận nó. phát hành một token được ký bởi một IDP không được liệt kê và xác nhận người xác nhận từ chối với `WWW-Authenticate: Bearer error="invalid_token", error_description="iss not allowed"`- Tôi không biết.
   Trung文翻译:向受保护资源元数据的`authorization_servers`列表添加新 IdP──签发一个由新 IdP 签名的代币,确认验证器接受;再签发一个由未列出的 IdP 签名的代币,确认验证器以`WWW-Authenticate: Bearer error="invalid_token", error_description="iss not allowed"`拒绝.

3. Thêm kiểm tra giới hạn lãi suất vào `register_client`sử dụng một token-bucket cho mỗi nguồn IP được giữ trong một dict nhỏ được khóa bằng IP.
   Trung ngữ翻译:给 `register_client`Tóm lại một kiểm tra giới hạn được thực hiện trước khi đăng ký viên chấp nhận yêu cầu.

4. Đọc RFC 7591 và xác định hai lĩnh vực bài học `/register`người xử lý không xác nhận. Thêm xác nhận. (Nhận thức: `software_statement`và `redirect_uris`Chương trình URI.)
   Trung văn翻译:阅读 RFC 7591, tìm ra bài học này `/register`处理器未验证的两个字段并补上验证――(提示:`software_statement`Với`redirect_uris`(Đối với URI)

5. Thêm một máy chủ ủy quyền thứ hai. xác nhận khách hàng lưu trữ một đăng ký riêng biệt với khóa phát hành và từ chối sử dụng lại token của nhà phát hành đầu tiên hoặc `client_id`- Tôi không biết.
   Trung ngữ翻译:添加第二授权服务器── xác nhận khách hàng lưu trữ độc lập theo chủ đề đăng ký của chủ đề, và từ chối sử dụng mã thông báo của chủ đề đầu tiên hoặc `client_id`

6. Cố gắng xác minh DoS, gửi cho người xác nhận một token với một số ngẫu nhiên`kid`và xác nhận`refresh_jwks`chạy tối đa một lần và số lượng khóa của máy chủ ủy quyền không tăng lên. Sau đó cố ý quay lại quay trở lại và xem số lượng khóa leo lên mỗi token giả  khôi phục lại sau đó.
   Trung文翻译: chứng minh DoS 修复──给验证器送一个随机 `kid`Đồ hiệu, xác nhận`refresh_jwks`Số lượng chìa khóa của máy chủ được cấp phép không tăng lên. Sau đó cố ý chuyển đổi lại, xem số lượng chìa khóa theo mỗi mã hóa giả mạo.

7. Thực hành DCR bị lỗi thời với cả hai `native`và `web`Client. xác nhận một client web với một HTTP chuyển hướng URI và một client bản địa mà không có một chuyển hướng loopback chính xác được từ chối.
   中文翻译:用 `native`和 `web`两种客户端演练已废弃的DCR──确认带HTTP转向 URI 网络客户端与没有精确回环转向的本地客户端都被拒绝──

## Từ khóa  Từ khóa nhanh chóng

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

## Xem thêm 延伸阅读

- [MCP authorization specification (2026-07-28)](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)- hồ sơ cấp phép MCP hiện tại
  中文翻译:MCP 授权规范(2026-07-28) 本课实现的当前MCP 授权配置档
- [MCP 2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)- CIMD, xác thực nhà phát hành, khấu trừ DCR và thay đổi tín dụng của nhà phát hành
  Trung文翻译:MCP 2026-07-28 变更日志CIMD、签发人校验、DCR 弃用与按签发人做键的凭证变更
- [OAuth Client ID Metadata Document (draft-ietf-oauth-client-id-metadata-document-00)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-client-id-metadata-document-00) CIMD
  Trung文翻译:CIMD 草案"URL 即客户端_id"的注册机制
- [RFC 8414 — OAuth 2.0 Authorization Server Metadata](https://datatracker.ietf.org/doc/html/rfc8414) Hợp đồng phát hiện
  Trung ngữ翻译:RFC 8414发现契约
- [RFC 7591 — OAuth 2.0 Dynamic Client Registration Protocol](https://datatracker.ietf.org/doc/html/rfc7591) DCR (cách quay trở lại)
  Trung文翻译:RFC 7591DCR(后备路径)
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://datatracker.ietf.org/doc/html/rfc7636) chứng minh sở hữu của khách hàng công cộng
  Trung ngữ翻译:RFC 7636PKCE, công khách có chứng chỉ
- [RFC 8707 — Resource Indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707) Khán giả đính kèm
  Trung文翻译:RFC 8707资源指示器,受众固定
- [RFC 9728 — OAuth 2.0 Protected Resource Metadata](https://datatracker.ietf.org/doc/html/rfc9728) phát hiện máy chủ tài nguyên
  Trung文翻译:RFC 9728资源服务器发现
- [RFC 9207 — OAuth 2.0 Authorization Server Issuer Identification](https://datatracker.ietf.org/doc/html/rfc9207) `iss`tham số bảo vệ chống lại các cuộc tấn công hỗn hợp
  Trung文翻译:RFC 9207 phòng thủ  tấn công `iss`参数
- [RFC 7662: OAuth 2.0 Token Introspection](https://datatracker.ietf.org/doc/html/rfc7662)
  Trung文翻译:RFC 7662不透明代币 的内省端点
- [RFC 7009: OAuth 2.0 Token Revocation](https://datatracker.ietf.org/doc/html/rfc7009)
  Trung文翻译:RFC 7009token 吊销,本课的"新鲜度契约"
