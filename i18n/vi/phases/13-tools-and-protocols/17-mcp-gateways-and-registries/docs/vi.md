# MCP không có quốc tịch Gateway và đăng ký nhập cảnh .

> Một cửa ngõ nên làm cho mọi tuyến đường rõ ràng. giao thức 2026-07-28 cho nó phương pháp, tên, phiên bản, khả năng, danh tính, kho lưu trữ và ranh giới theo dõi mà không cần một phiên giao thông.

> **【中文解读】**网关应让每条路由显式化──2026-07-28 协议 根据没有传输会话的前提,为网关提供方法,名称,版本,能力,身份,缓存和追踪边界──旧网关"多路复用一个客户端会话到多个后端会话并重写`Mcp-Session-Id`"đối với mỗi yêu cầu tái xác nhận, tái ủy quyền, tái cấu trúc sau khi yêu cầu.

> **【拓展】**网关是企业 MCP 部署的控制平面:把阶段13 · 15的描述符锁定与阶段13 · 16的授权模型集中执行――注册中心(Registry) cung cấp chứng cứ phát hiện(server.json), nhưng nhập vào quyền quyết định在网关

>  **【前置】**学本节前 xin vui lòng nắm bắt trước:(1) giai đoạn 13 · 15(安全) với 13 · 16(授权)网关集中执行这两课的全部校验;(2) giai đoạn 13 · 09 của Streamable HTTP单一 POST 端点、请求级 SSE、`subscriptions/listen`3) MRTR và các nhiệm vụ 扩展的基本形态──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 15 (security), Phase 13 · 16 (authorization) | **前置知识:** Phase 13 · 15（安全）、Phase 13 · 16（授权）
**Time:** ~75 minutes | **时间:** 约 75 分钟

## Mục tiêu học tập

- Kết hợp một số máy chủ MCP sau một điểm cuối 2026-07-28 mà không có mối liên hệ phiên.
  Trung ngữ翻译:把多个MCP 服务器聚合到一个2026-07-28 端点之后,不依赖会话亲和──
- Thiết lập metadata và tiêu đề định tuyến trước khi chính sách hoặc chuyển tiếp theo yêu cầu.
  Trung ngữ翻译: 在策略与转发之前校验每请求元数据和路由头──
- Thủy hợp các công cụ với không gian tên ổn định, thứ tự xác định, pin mô tả, RBAC và lưu trữ trước tiên riêng.
  Trung文翻译:用稳定命名空间、确定性顺序、描述符锁定、RBAC 和私有缓存合并工具──
- Hãy xem hồ sơ đăng ký là bằng chứng khám phá mà vẫn đòi hỏi chính sách nhập học.
  Trung ngữ翻译:把注册中心记录当作仍需准入策略的发现证据──
- SSE theo yêu cầu đường, `subscriptions/listen`, MRTR thử lại, và nhiệm vụ mở rộng gọi đúng.
  Trung文翻译:正确路由请求级 SSE`subscriptions/listen`、MRTR 重试和 扩展调用──
- Tránh tay cổ xưa và hỗ trợ phiên từ con đường hiện đại.
  Trung ngữ翻译:把遗留握手与会话支持与现代路径隔离──

> **【中文解读】**Học mục tiêu:聚合(无会话亲和) 校验(先于策略) 、合并(确定性) 、准入(发现≠决定) 、路由(SSE/订阅/MRTR/Tasks 四种流) 、隔离(遗留路径版本门控) ⋅

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**规模化部署 phải trả lời sáu câu hỏi: Which servers allow access? Which subject can see and call each tool? Two backend重名怎么办? Descrilator变更如何复审?

Kết nối một client trực tiếp với một máy chủ là đơn giản. Một triển khai lớn hơn cần một câu trả lời nhất quán cho các câu hỏi khó khăn hơn:

> Một khách hàng trực tiếp kết nối với một máy chủ rất đơn giản.

- Các máy chủ nào được phép?
  Trung ngữ翻译: Quý các máy chủ được phép?
- Giám đốc nào có thể nhìn thấy và gọi cho mỗi công cụ?
  Trung ngữ翻译: कौन trong số những người có thể xem và điều chỉnh mỗi công cụ?
- Điều gì xảy ra khi hai người đứng sau cùng một tên?
  Trung ngữ: Chuyện gì xảy ra khi hai bên tiếp xúc cùng tên?
- Những thay đổi mô tả được xem xét như thế nào?
  Trung ngữ翻译:描述符变更如何复审?
- Các giới hạn lãi suất và các sự kiện kiểm toán được áp dụng ở đâu?
  Trung ngữ翻译:Cơ quan kiểm toán và hạn chế diễn ra ở đâu?
- Có trường hợp nào có thể xử lý yêu cầu tiếp theo không?
  Trung ngữ翻译:任意实例都能处理下一个请求吗?

Một cửa ngõ nằm giữa các khách hàng và các máy chủ MCP hậu thuẫn. Nó trình bày một điểm cuối MCP, áp dụng chính sách xuyên ngành và chuyển các yêu cầu được phê duyệt.

> 网关 nằm giữa khách hàng và sau端 MCP 服务器. Nó trình bày một điểm cuối MCP, ứng dụng các chiến lược, chuyển phát yêu cầu phê duyệt.

Các thiết kế cổng thông tin cũ thường đa dạng một phiên khách hàng thành nhiều phiên cuối và viết lại `Mcp-Session-Id`Đó là một thiết kế tương thích cũ. lõi 2026-07-28 không có phiên giao thức.

> 早期网关设计常把一个客户端会话多路复用成多后端会话并重写 `Mcp-Session-Id` Đó là遗留兼容设计──2026-07-28 核心没有协议会话──

>  **【类比】**旧网关像"总机转接的电话系统"客户先拨总机(建立会话),总机记住线路(会话亲和),断线就得重拨.现代网关像"快递分拣中心"每个包裹(请求) tự带完整面单(元数据 +路由头 +凭证),任何分拣员(任意实例) 拿起就能处理,不需要"上次是谁接的电话"――注册中心像"供应商黄页"黄页只证明"有这家店",不证明"应该让这货进仓库";准入策略只是仓库的验货单.

## Khái niệm cốt lõi

> **【中文解读】**本节按网关的处理流水线展开:现代网关七步路径 → 运行时策略是首要决定 → 单一 POST 端点 → Mỗi cấp thực hiện phát hiện → Mỗi yêu cầu khách hàng khả năng → 确定性命名空间 → 锁定已批准描述符 → 注册中心只助发现不作决定 → 证中介 → 无会话限流 → 审计决策链 → 请求级 SSE → 长效变更通知 → 网关中的 MRTR → 任务 扩展路由 → 兼容边界.

### Đường lối vào hiện đại

> **【中文解读】**现代网关对每一个请求走七步:认证主体 → 校验版本/路由头/元数据 → 授权主体、资源、方法、工具、参数 → 应用描述符、注册、限流、数据策略 → 为选择后端构建全新自含请求 → 校验后端结果并返回网关结果 → 记录不含秘密审计事件──会步不需要隐藏协议话;应用状态放库、显式句柄、任务或受完整性保护的MRTR 状态里──

Đối với mỗi yêu cầu:

1. Đăng bằng chính từ giấy phép vận chuyển.
  Trung ngữ翻译:从传输层授权信息认证主体──
2. Định hành`MCP-Protocol-Version`- `Mcp-Method`- `Mcp-Name`, và`params._meta`- Tôi không biết.
  Trung ngữ翻译:校验 `MCP-Protocol-Version``Mcp-Method``Mcp-Name`和 `params._meta`
3. Quyền cho nguyên tắc, tài nguyên, phương pháp, công cụ và các lập luận.
  Trung ngữ翻译:授权主体、资源、方法、工具和参数──
4. Sử dụng mô tả, đăng ký, tỷ lệ và chính sách dữ liệu.
  Trung ngữ翻译:应用描述符、注册、限流和数据策略。
5. Tạo một yêu cầu tự do mới cho phần sau đã chọn.
  Trung ngữ翻译:为选定后端构造全新的自包含请求──
6. Thiết lập kết quả hậu quả và trả lại kết quả gateway.
  Trung ngữ翻译:校验后端结果并返回网关结果──
7. Lập lại một sự kiện kiểm toán mà không ghi lại bí mật.
  Trung ngữ翻译:记录审事件,但不记录秘密──

Không có bước nào cần một phiên giao thức ẩn. trạng thái ứng dụng vẫn có thể tồn tại trong cơ sở dữ liệu, tay cụ thể, nhiệm vụ hoặc trạng thái MRTR được bảo vệ tính toàn vẹn.

> Không cần phải có bước nào ẩn trong giao thức.

### Chính sách thời gian chạy là quyết định đầu tiên của cửa ngõ

> **【中文解读】**准入决定"哪个后端版本可以进网关", nhưng không cấp phép một lần调用活跃. Mỗi yêu cầu phải được thực hiện từ chủ thể đã xác nhận, nhà phát hành và nguồn lực, thuê nhà, phù hợp với phương pháp và tên gọi, quy định tham số, nhập mô tả khóa, sau端 sức khỏe, giao dịch năng lực, phân loại dữ liệu, trạng thái dòng chảy hạn chế và bất kỳ động tác nào.

Đăng nhập quyết định phiên bản cuối cùng nào có thể nhập vào cổng thông tin. Nó không cho phép cuộc gọi trực tiếp. Đối với mỗi yêu cầu, cổng thông tin tính lại chính sách từ chính xác nhận, nhà phát hành và nguồn lực, thuê nhân, phương pháp và tên phù hợp, lập luận bình thường, pin mô tả được chấp nhận, sức khỏe cuối cùng hiện tại, giao diện khả năng, phân loại dữ liệu, trạng thái tỷ lệ và bất kỳ sự chấp thuận liên quan đến hành động nào.

> 准入决定哪个后端版本可以进入网关,但不授权一次实际调用―― đối với mỗi yêu cầu,网关 phải dựa trên phương pháp và tên gọi đã được xác nhận, nhà phát hành và tài nguyên, thuê nhà, quy định quy định, 准入描述符锁定, hiện tại后端健康,能力交交集,数据分类,流状态, và bất kỳ động tác nào được ràng buộc trong phê duyệt lại chiến lược tính toán lại――

Điều này quan trọng. Một hồ sơ Registry có thể vẫn hoạt động trong khi vai trò của người dùng bị hủy bỏ. Một mô tả có thể vẫn được gắn trong khi một lập luận đích vượt qua ranh giới người thuê nhà. Một hậu kết có thể vẫn được chấp thuận trong khi chính sách kiểm dịch xảy ra. Chính sách thời gian chạy do đó là quyết định chính cho phép hoặc từ chối, với Registry và chứng cứ mô tả như là đầu vào.

> Dòng này rất quan trọng: hồ sơ đăng ký có thể vẫn đang hoạt động và vai trò của người dùng đã bị hủy bỏ; mô tả có thể vẫn bị khóa và các tham số mục tiêu đã vượt qua biên giới thuê nhà; cuối cùng vẫn có thể được phê duyệt và chiến lược tai nạn đã tách biệt tình trạng thay đổi và điều chỉnh. Vì vậy, chiến lược khi vận hành là quyết định đầu tiên cho phép / từ chối, đăng ký và mô tả chỉ là nhập vào.

Đừng lưu trữ quyết định cho phép dưới một kết nối hoặc xóa định danh phiên. Nếu chính sách không có sẵn, hãy theo chính sách thất bại được tuyên bố theo lớp hoạt động. Một mặc định an toàn là không đóng cửa cho các thay đổi trạng thái và đọc nhạy cảm, trong khi các con đường đọc công khai được phê duyệt rõ ràng chỉ có thể sử dụng chính sách được biết đến cuối cùng ngắn ngủi khi mô hình rủi ro của họ cho phép. Lưu ý phiên bản chính sách nào và đường lối thất bại đã đưa ra quyết định, sau đó xác nhận kết quả hậu quả trước khi trả lại nó.

> Đừng "đưa" quyết định để tồn tại kết nối hoặc được di chuyển dưới dấu hiệu của cuộc họp. Chiến lược không thể sử dụng khi, theo loại hoạt động thực hiện đã tuyên bố chiến lược thất bại.

> ️ **【易错点】**场景:网关把"允许" quyết định缓存连接ID或旧会话ID 下 / 后果: người dùng角色被撤销、租户被隔离后,请求在旧连接上仍被放行策略绕过/修复:(1) Mỗi yêu cầu重算策略,点是已认证主体而不是连接;(2) 策略服务不可用按操作类别失败-closed(写操作和敏感读直接拒绝);3) 审核记录策略版本与失败路径,让"为什么放行/拒绝"可盘.

### Một điểm cuối POST

HTTP Streamable hiện đại gửi mỗi tin nhắn JSON-RPC qua POST:

> 现代 Streamable HTTP  thông qua POST 发送每条 JSON-RPC 消息:

```text
POST /mcp
Authorization: Bearer <gateway-token>
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: notes.search
Accept: application/json, text/event-stream
```

Gateway có thể trả về JSON hoặc yêu cầu-scoped SSE cho POST đó. GET và DELETE trả lại 405 cho yêu cầu hiện đại. `Mcp-Session-Id`và `Last-Event-ID`không tạo ra quyền lực, mối quan hệ, hoặc lặp lại hành vi.

> 网关可以为该 POST 返回 JSON 或请求级 SSE。现代请求的 GET 和 DELETE 返回 405。`Mcp-Session-Id`Với`Last-Event-ID`Không có quyền lực, tình yêu hay hành vi tái tạo.

Các giá trị tiêu đề và cơ thể phải đồng ý.`-32020`Điều này cho phép bộ cân bằng tải, cửa khẩu và giới hạn tốc độ đi đường mà không cần phân tích toàn bộ cơ thể trong khi vẫn giữ được tính toàn vẹn đầu đến cuối.

> 头与正文的值必须一致──在搜索后端之前使用 `-32020`拒绝不匹配──这让负载均衡器、网关和限流器不需要解析完整正文就能路由,同时保持端到端完整性──

Thiết lập bằng một thứ tự chính xác: JSON-RPC và các loại metadata, tiêu đề và cơ thể, sau đó hỗ trợ cho phiên bản phù hợp.`-32020`Nếu tiêu đề và cơ thể đồng ý về một phiên bản không được hỗ trợ, trả về HTTP 400 với `-32022`và `data`Đúng vậy.`{"supported":["2026-07-28"],"requested":"<actual>"}`. Một phương pháp không rõ trả về HTTP 404 với `-32601`- Tôi không biết.

> 按唯一精确顺序校验:JSON-RPC với các kiểu dữ liệu cũ, đầu và chữ chính,等等, sau đó hỗ trợ cho phiên bản phù hợp. Không phù hợp trả về HTTP 400.`-32020`; tiêu đề kết hợp nhưng phiên bản không hỗ trợ, quay lại HTTP 400 `-32022`且 `data`精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`;未known方法返回 HTTP 404 `-32601`

`ProtocolError`mang theo tùy chọn `data`, và cửa cổng sẽ liên tục nó vào đối tượng lỗi JSON-RPC.`id`, vì vậy nó không bao giờ nhận được thành công hoặc lỗi JSON-RPC. Một thông báo HTTP được chấp nhận trả lại 202 với một cơ thể trống.

> `ProtocolError`携带可选 `data`,网关把它序列化到 JSON-RPC 错误对象──没有通知 `id`,永远不收 JSON-RPC 成功或错响应── được chấp nhận HTTP 通知返回 202 空体──

### Thực hiện phát hiện ở mọi lớp

Các thiết bị Gateway `server/discover`Nó cũng phát hiện ra mỗi backend để nó biết các phiên bản giao thức, khả năng và mở rộng.

> 网关为客户端实现 `server/discover`; đồng thời cũng tìm thấy mỗi cuối sau, để biết phiên bản giao thức, khả năng và mở rộng.

Ví dụ kết quả gateway:

> 网关结果 ví dụ:

```json
{
  "resultType": "complete",
  "supportedVersions": ["2026-07-28"],
  "capabilities": {
    "tools": {"listChanged": true}
  },
  "ttlMs": 30000,
  "cacheScope": "private",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "enterprise-gateway",
      "version": "2.0.0"
    }
  }
}
```

Chỉ quảng cáo giao thông khả năng mà cửa khẩu có thể tôn trọng từ đầu đến cuối. Một tính năng hậu thuẫn không tự động được tiết lộ an toàn. Một tính năng cửa khẩu không có đường hậu thuẫn không hữu ích để quảng cáo.

> Chỉ có thông báo về khả năng giao dịch kết thúc.

`serverInfo`là dữ liệu hiển thị và chẩn đoán tự báo cáo. Đừng sử dụng nó như chứng minh đăng ký hoặc nhà xuất bản.

> `serverInfo`Đây là những dữ liệu tự báo cáo và chứng minh, không được sử dụng như một trung tâm đăng ký hoặc chứng minh của nhà phát hành.

### Khả năng của khách hàng theo yêu cầu

Mỗi yêu cầu được chuyển tiếp cần một hiện tại `_meta`bao bì:

> Mỗi yêu cầu chuyển đổi đều cần hiện tại.`_meta`信封:

```json
{
  "io.modelcontextprotocol/protocolVersion": "2026-07-28",
  "io.modelcontextprotocol/clientCapabilities": {},
  "io.modelcontextprotocol/clientInfo": {
    "name": "enterprise-gateway",
    "version": "1.0.0"
  }
}
```

Đừng mù quáng các khả năng của khách hàng bên ngoài vào backend. Gateway là khách hàng của backend. Chỉ quảng cáo các tính năng của gateway sẽ trung gian đúng.

> Đừng để khả năng của các khách hàng bên ngoài được chuyển sang các khách hàng bên kia.

### Định nghĩa namespacing

Thủy lại các công cụ hậu môn dưới tên công khai ổn định:

> Sử dụng cụ kết nối cuối cùng:

```text
notes.search
notes.create
issues.list
issues.open
```

Hãy giữ bản đồ từ tên công cộng đến tên công cụ gốc và cuối cùng. Đừng bao giờ chọn vụ va chạm đầu tiên hoặc cuối cùng. Một tên công cộng là một phần của hợp đồng phê duyệt và kiểm toán, vì vậy thay đổi nó là một di chuyển.

> 保留"公开名 → 后端 + 原始工具名"的映射──绝不重名冲突里选先来后到──公开名是审核与审计契约的一部分,改它就是一次迁移──

`tools/list`Khi khả năng nhìn thấy khác nhau bởi chính, trả lại `cacheScope: private`- Một giới hạn`ttlMs`Giảm tải phát hiện hậu kết mà không cho phép danh sách cụ thể cho người dùng rò rỉ qua các bối cảnh ủy quyền.

> `tools/list`必须确定性──当可见性因主体不同时回归 `cacheScope: private`有界的`ttlMs` giảm tải về sau khi phát hiện, không cho phép các danh sách tùy chỉnh của người dùng vượt qua quyền trên

Mỗi mô tả công cụ được phơi bày bao gồm một tên ổn định, mô tả và gốc đối tượng `inputSchema`. Namespacing không thể loại bỏ các trường mô tả yêu cầu. Kết quả danh sách đầy đủ cũng bao gồm `resultType`, dữ liệu siêu dạng máy chủ, và gợi ý cache.

> Mỗi mô tả công cụ được phơi bày đều có tên, mô tả và gốc vật`inputSchema`◊命名空间化不能删掉必填的描述符字段──完整列表结果还包括 `resultType`、 Server ID và bộ nhớ dữ liệu 

### Các mô tả được chấp thuận bằng pin

Vào thời điểm nhập học, hãy ghi danh mô tả đầy đủ và lưu trữ bản ghi của nó dưới tên công khai đủ điều kiện.

> 准入时规范化完整描述符,把摘要存储到有限公开名下;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

Nếu nó thay đổi:

- Tắt nó ra khỏi `tools/list`- Tôi không biết.
  Trung ngữ翻译:从 `tools/list`移除 nó.
- Khước từ các cuộc gọi trực tiếp.
  Trung ngữ翻译:拒绝直接调用。
- Đưa ra một sự kiện kiểm toán.
  Trung ngữ翻译:发出审计事件.
- Cần chính sách hoặc phê duyệt lại của con người trước khi cập nhật pin.
  Trung ngữ翻译:更新锁定前要求策略或人工重新批准──

Một cửa cổng là một điểm thực thi trung tâm hữu ích, nhưng nó không biến một mô tả lần đầu tiên thấy thành một mô tả an toàn.

> 网关 là điểm tập trung thực hiện hữu ích, nhưng nó không thể biến "được nhìn thấy lần đầu tiên mô tả" thành an toàn.

### Các hồ sơ giúp khám phá, không quyết định

> **【中文解读】**Đăng ký trung tâm `server.json`只是发布元数据:它说明"包叫什么,怎么装,版本号是多少", không mang lại quyết định an ninh của mạng.`server.json`Với trạng thái nhập cảnh để kết nối (đối gia) ⋅ mỗi nhập cảnh sau端要记录:精确注册中心与记录标识、已验证发行者命名空间、允许传输与端点、锁定版本、工件/描述符摘要、授权发行者与资源、审核人/审核时间/有效期──

Một sổ đăng ký`server.json`cung cấp dữ liệu siêu dữ liệu xuất bản. Một hồ sơ được hỗ trợ gói có thể trông như sau:

> Đăng ký trung tâm `server.json`提供发布元数据──一个带包的记录长这样:

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
  "name": "com.example/notes",
  "description": "Example notes MCP server.",
  "version": "1.0.0",
  "packages": [
    {
      "registryType": "npm",
      "identifier": "@example/notes-mcp",
      "version": "1.0.0",
      "transport": {"type": "stdio"}
    }
  ]
}
```

Các metadata xuất bản không mang lại quyết định bảo mật của cổng thông tin.

> 发布元数据不承载网关的安全决定―― đưa người phát hành đã được chứng minh và chứng minh nguồn vào trạng thái truy cập độc lập:

```json
{
  "registryName": "com.example/notes",
  "registryVersion": "1.0.0",
  "publisher": {"namespace": "com.example", "status": "verified"},
  "provenance": {
    "source": "registry.modelcontextprotocol.io",
    "recordId": "com.example/notes@1.0.0"
  },
  "admission": {"status": "approved", "reviewedBy": "gateway-policy"}
}
```

Cổng kiểm tra `server.json`Và các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên của các thành viên.

> 网关检查 `server.json`hình dạng của nó để kết nối với trạng thái bên ngoài đó.

Đối với mỗi backend được chấp nhận, ghi lại:

- Đồ đăng ký chính xác và ghi nhận.
  Trung ngữ翻译:精确的注册中心与记录标识──
- Các nhà xuất bản đã xác minh không gian tên hoặc bằng chứng tên miền.
  Trung文翻译:已验证的发行者命名空间或域名证据──
- Chuyển và điểm cuối được phép.
  Trung ngữ翻译:允许的传输与端点。
- Phiên bản đinh hoặc chính sách nâng cấp được phê duyệt.
  Trung ngữ翻译:锁定的版本或已批准的升级策略──
- Thiết bị tạo ra hoặc tiêu hóa mô tả.
  Trung ngữ翻译:工件或描述符摘要。
- Nhà phát hành và nguồn tài nguyên.
  Trung文翻译:授权发行与资源──
- Đánh giá, thời gian phê duyệt, và hết hạn.
  Trung ngữ翻译:评审人、批准时间与有效期──

Đừng chấp nhận một máy chủ vì tên hiển thị của nó giống như một sản phẩm quen thuộc. Đừng coi sự hiện diện của registry như một đánh giá bảo mật hoạt động. Các máy chủ riêng có thể được nhập thông qua cùng một kế hoạch chứng minh ngay cả khi chúng không bao giờ xuất hiện trong một registry công cộng.

> Đừng chỉ vì hiển thị tên như một sản phẩm quen thuộc bạn sẽ nhận được một máy chủ; đừng coi "trong trung tâm đăng ký" như một lần kiểm tra an ninh vận tải.

Bài học này thực hiện các cửa ngõ: kết hợp bằng chứng xuất bản với việc nhận địa phương trước khi một backend trở thành định tuyến. [Lesson 30: MCP Registry Supply Chain, Admission, Drift, and Rollback](../../30-mcp-registry-supply-chain-and-drift/docs/en.md)xây dựng toàn bộ máy điều khiển cho chứng minh không gian tên chính xác, nguồn gốc của vật thể, pin không thay đổi, dẫn dắt mô tả trực tiếp, hòa giải trạng thái Registry, sổ tay nhập cảnh rõ ràng và quay lại bằng chứng. Giữ trạng thái chuỗi cung ứng tách biệt với quyết định thời gian chạy theo yêu cầu ở trên.

> Bài học 30  Xây dựng một trình tự kiểm soát hoàn chỉnh  xác định tên không gian chứng minh √ nguồn sản phẩm √ không thể thay đổi khóa √ trình diễn viên di chuyển trên mạng √ đăng ký trung tâm trạng thái đối với tài khoản √ phòng √ thay đổi vào tài khoản và có chứng minh √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √

> 🤔 **【困惑】**Q: Trung tâm đăng ký đã xác nhận nhà phát hành, tại sao các mạng lưới còn cần chính sách nhập cảnh của mình?A: Trung tâm đăng ký xác nhận là "người phát hành là ai", không phải "công ty của bạn không nên sử dụng"。 đăng ký có thể giữ hiệu lực và vai trò người dùng đã bị hủy bỏ; mô tả giữ khóa và mục tiêu tham số xuyên thuê nhà; hậu kết giữ phê duyệt và chiến lược tai nạn tách biệt thay đổi điều chỉnh。 phát hiện chứng minh giải quyết" hàng này là của ai", nhập cảnh và hoạt động khi chiến lược giải quyết "thời gian này bây giờ không thể vào ∞ năng lượng lên nào条 tuyến".。

### Trợ lý chứng nhận

Cổng thông tin xác thực người gọi và xác thực riêng cho backend.

> 网关认证 chính mình điều chỉnh người dùng,并单独向后端做认证──后端凭证永远不到客户端手上──

Hãy giữ các ràng buộc này rõ ràng:

> Hãy giữ cho những điều này hiển nhiên:

```text
outer principal -> gateway role and policy
backend issuer + resource -> backend registration and token
```

Không bao giờ chuyển token cổng bên ngoài cho một backend. Không bao giờ sử dụng lại token backend tại một nhà phát hành hoặc nguồn khác. Nếu một công cụ hoạt động thay mặt cho người dùng cuối, hãy bảo tồn ủy quyền đó bằng một mô hình trao đổi hoặc yêu cầu được thiết kế thay vì giả vờ người dùng với giấy chứng nhận dịch vụ chia sẻ.

> Không bao giờ chuyển token mạng bên ngoài sang cuối; không bao giờ chuyển token cuối sử dụng cho nhà phát hành hoặc nguồn khác. Nếu công cụ đại diện cho hành động của người dùng cuối cùng, nên sử dụng mô hình trao đổi hoặc tuyên bố được thiết kế để giữ lại cấp ủy thác này, thay vì lấy giấy phép dịch vụ chia sẻ để bắt đầu người dùng.

### Các giới hạn tỷ lệ không có buổi

Các giới hạn chính theo chính xác nhận, nhà phát hành, tài nguyên, công cụ công cộng, lớp chi phí và cửa sổ thời gian.

> 限流按已认证主体、发行者、资源、公开工具、成本类别和时间窗口取键──会话 id 已不存在;即便存在也易轮换,不可作键──

Hãy kiểm tra giá rẻ trước khi tiêu thụ công việc đắt tiền.

> Trước tiên làm các bài kiểm tra rẻ tiền, tái tiêu thụ công việc đắt tiền.

### Kiểm tra chuỗi quyết định

Đăng đủ để tái tạo cuộc gọi:

> 记录足够重建一次调用信息:

- Đơn vị xác định yêu cầu và theo dõi.
  Trung文翻译:请求与追踪标识符──
- Chủ sở hữu và nhà phát hành xác thực
  Trung文翻译:已认证主体与发行者──
- Công cụ công cộng và đường dẫn hậu.
  Trung ngữ翻译:公开工具与后端路由──
- Phiên bản pin mô tả.
  Trung ngữ翻译:描述符锁定版本──
- Quyết định chính sách và lý do.
  Trung ngữ翻译:策略决定与理由。
- Lạt và lớp kết quả.
  Trung ngữ翻译:延迟与结果类别。
- MRTR vòng hoặc xác định nhiệm vụ khi có thể.
  Trung ngữ翻译:适用时的 MRTR 轮次或任务标识符──

Các mã thông báo người mang thư, mã ủy quyền, mã thông báo mới, bí mật thô và các lập luận nhạy cảm không cần thiết.

> Đối với người mang token, mã quyền, mã làm mới, bí mật ban đầu và các yếu tố nhạy cảm không cần thiết để làm sáng tỏ.

### SSE theo yêu cầu

Một POST bình thường có thể trả lại SSE được yêu cầu khi workflows trong một yêu cầu đó.

> Khi một công việc trong một yêu cầu trong dòng chảy xuất hiện, thông thường POST có thể trả lại yêu cầu cấp SSE。关闭响应流即取消这个进行中的现代HTTP请求。

Đừng tạo ra một dòng GET riêng biệt và không hứa hẹn lặp lại ID-Event cuối cùng.

> Đừng xây dựng GET 流, cũng đừng hứa hẹn Last-Event-ID 重放──那些是旧传输假设──

### Thông báo thay đổi lâu dài

Đối với các thông báo thay đổi danh sách và tài nguyên, một khách hàng hiện tại gửi `subscriptions/listen`thông qua POST và nhận được một phản hồi của SSE.`toolsListChanged`- `promptsListChanged`- `resourcesListChanged`, và`resourceSubscriptions`- Có thể là:

> Để thông báo về thay đổi danh sách và tài nguyên, khách hàng hiện tại qua POST  gửi `subscriptions/listen`并收到 SSE 响应──通知过器使用精确的平字段 `toolsListChanged``promptsListChanged``resourcesListChanged`和 `resourceSubscriptions`- Có thể là:

```json
{
  "jsonrpc": "2.0",
  "id": "listen-tools",
  "method": "subscriptions/listen",
  "params": {
    "notifications": {
      "toolsListChanged": true
    },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {}
    }
  }
}
```

Sự kiện đầu tiên xác nhận bộ phụ được hỗ trợ. Biểu thức đăng ký của nó là ID JSON-RPC của yêu cầu mở dòng:

> Đầu tiên là xác nhận sự kiện được hỗ trợ.

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/subscriptions/acknowledged",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/subscriptionId": "listen-tools"
    },
    "notifications": {
      "toolsListChanged": true
    }
  }
}
```

Các thông báo trên dòng đó đều mang cùng một `io.modelcontextprotocol/subscriptionId`trong `params._meta`Không có bản phát lại tự động hoặc nghe lại tự động. Khi kết nối lại, khách hàng mở lại đăng ký và làm mới các danh sách mà nó dựa vào. Một kết thúc thanh lịch được khởi động bởi máy chủ trả lại kết quả hoàn chỉnh cuối cùng được gắn thẻ với cùng một ID đăng ký.

> 后网关只转发已确认变更类型── trên dòng này mỗi thông báo đều có`params._meta`里带同一个 `io.modelcontextprotocol/subscriptionId`Không có tự động tái tải, cũng không có tự động tái xem.

Con đường hiện đại thay thế `resources/subscribe`- `resources/unsubscribe`, và không được yêu cầu tự động GET phát sóng.

> 现代路径取代了 `resources/subscribe``resources/unsubscribe`Và không được yêu cầu độc lập GET 流.

### MRTR qua một cổng

> **【中文解读】**后端返回 `resultType: input_required`时,网关 chỉ có thể chuyển đổi kết quả khi yêu cầu nhập được hỗ trợ bởi khách hàng bên ngoài.`requestState`必须逐字节原样保留──客户端使用新的 JSON-RPC id 和 `inputResponses`重试原公开工具;网关对重试重新授权;检查同一公开路由,再转发一个全新的后端请求绝不假设早先一轮授予无限批准

Khi một phần sau quay lại `resultType: input_required`, gateway chỉ có thể chuyển kết quả đó nếu khách hàng bên ngoài hỗ trợ yêu cầu nhập cần thiết.`requestState`Byte cho byte trừ khi cổng thông tin cố tình chấm dứt và phát hành lại tương tác.

> 后端返回 `resultType: input_required`Khi chỉ có sự hỗ trợ của khách hàng bên ngoài yêu cầu nhập, mạng lưới có thể chuyển phát kết quả này.`requestState`Để giữ lại.

Khách hàng thử lại công cụ công cộng gốc với một ID JSON-RPC mới và `inputResponses`- Gateway cho phép lại thử nghiệm, kiểm tra cùng một tuyến đường công cộng, sau đó chuyển một yêu cầu hậu thuẫn mới.

> 客户端 sử dụng ID JSON-RPC mới 和 `inputResponses`重试原公开工具──网关对重试重新授权──检查同一公开路由,然后转发全新的后端请求──绝不能假设早一轮授予无限批准──

### Nhiệm vụ định tuyến mở rộng

> **【中文解读】**Nhiệm vụ là chính thức mở rộng`io.modelcontextprotocol/tasks`), không phải là một thay thế cho các cuộc họp trung tâm.`tools/call` quay lại `resultType: task`(带 `taskId`、 trạng thái 、 thời gian 、`ttlMs`、可选 `pollIntervalMs`);后续 `tasks/get`- Không.`tasks/update`- Không.`tasks/cancel`用 `params.taskId`作 `Mcp-Name`, cho trung gian một đường dẫn chìa khóa. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .`tasks/list`Hoặc`tasks/result`Đó là từ từ của mô hình kinh nghiệm cũ.

Các nhiệm vụ là một phần mở rộng chính thức được xác định bởi `io.modelcontextprotocol/tasks`Chúng không phải là một phiên bản thay thế.

> Nhiệm vụ là bởi`io.modelcontextprotocol/tasks`标识的官方扩展, không phải là một sự thay thế cho các cuộc họp trung tâm.

Khách hàng tuyên bố mở rộng bên trong khả năng của khách hàng theo yêu cầu, và cổng thông tin quảng cáo nó trong khám phá chỉ khi nó có thể bảo tồn vòng đời cuối đến cuối.`tools/call`, backend chỉ quyết định liệu phải trả lại kết quả bình thường hay không`resultType: task`. Kết quả nhiệm vụ mang theo `taskId`- `status`, dấu thời gian,`ttlMs`, và tùy chọn `pollIntervalMs`Việc này phải được đọc lâu dài trước khi kết quả đó được gửi.

> 客户端 trong mỗi yêu cầu của mình có thể mở rộng; 网关 chỉ thông báo nó trong khi phát hiện được trong thời gian duy trì nhiệm vụ.`tools/call`, có trở lại kết quả bình thường hay `resultType: task`Kết quả nhiệm vụ trực tiếp mang lại kết quả.`taskId``status`Thời gian`ttlMs`和可选的 `pollIntervalMs`❖ gửi kết quả này trước khi nhiệm vụ phải đã có thể được thực hiện lâu dài.

Gateway ghi lại đường chính và đường hậu xác thực cho công cụ xác định nhiệm vụ không rõ ràng.`tasks/get`- `tasks/update`, và`tasks/cancel`sử dụng cuộc gọi `params.taskId`như `Mcp-Name`, cho các trung gian một khóa định tuyến. `tasks/get`trả lại `resultType: complete`với trạng thái nhiệm vụ hiện tại và ghi kết quả cuối cùng hoặc lỗi giao thức trong trạng thái cuối cùng. `tasks/update`gửi khóa `inputResponses`cho sao nhập nhiệm vụ xuất hiện và trả lại một xác nhận hoàn chỉnh trống. `tasks/cancel`là một ý định hợp tác với một sự thừa nhận hoàn toàn trống rỗng, không phải là một đảm bảo rằng công việc sẽ dừng lại.

> 网关为不透明任务标识符记录已认证主体与后端路由──后续的 `tasks/get``tasks/update``tasks/cancel`调用 `params.taskId`作 `Mcp-Name`, cho trung tâm một đường dẫn.`tasks/get` quay lại `resultType: complete`Với trạng thái nhiệm vụ hiện tại, và kết thúc kết quả cuối cùng hoặc thỏa thuận sai lầm.`tasks/update`Để nhiệm vụ chưa quyết định nhập gửi dẫn khóa `inputResponses`, quay lại空的完成确认──`tasks/cancel`Không đảm bảo công việc thực sự dừng lại.

Không thực hiện mới `tasks/list`hoặc `tasks/result`Các phương pháp này thuộc về mô hình thử nghiệm cũ hơn. Một nhiệm vụ cần input cho thấy các yêu cầu nhúng hoàn chỉnh thông qua `tasks/get`; khách hàng trả lời thông qua họ `tasks/update`, không bằng cách thử lại cuộc gọi công cụ ban đầu. Khách hàng vẫn bỏ phiếu tại khoảng thời gian đề xuất; việc tạo nhiệm vụ vẫn được hướng đến máy chủ.

> Đừng thực hiện mới `tasks/list`Hoặc`tasks/result`方法它们 thuộc về mô hình thử nghiệm cũ hơn. 需要输入的任务通过 `tasks/get`暴露完整的内嵌请求; khách hàng thông qua `tasks/update`答, thay vì重试原工具调用──客户端 vẫn theo khuyến nghị间隔轮询; nhiệm vụ tạo vẫn được quản lý bởi máy chủ──

Durable task route state là dữ liệu ứng dụng được khóa bởi task handle, không phải là một phiên giao thức.

> 持久的任务路由状态是按任务句柄取取关键的应用数据,不是协议会话.

### Biên giới tương thích

Nếu cửa cổng phải phục vụ khách hàng cũ hoặc backend:

> Nếu mạng phải phục vụ khách hàng cũ hơn hoặc cuối sau:

- Khám phá thời đại rõ ràng.
  Trung ngữ翻译:显式检测协议年代。
- Giữ khởi tạo, các phiên vận chuyển, GET stream, đăng ký tài nguyên và từ vựng nhiệm vụ cũ trong một bộ điều chỉnh di sản.
  Trung ngữ翻译:把初始化、传输会话、GET 流、资源订阅和旧任务词汇全部留在遗留适配器里──
- Đừng bao giờ rò rỉ một ID phiên cũ vào định tuyến hoặc ủy quyền hiện đại.
  Trung ngữ翻译:绝不让遗留会话 id 泄漏进现代路由或授权。
- Tích thích một cuộc thăm dò khám phá giới hạn và chính sách phản hồi rõ ràng hơn là giảm cấp âm thầm.
  Trung ngữ翻译: ưu tiên sử dụng các kết quả tìm kiếm tăng rõ ràng trở lại chiến lược, chứ không phải tĩnh lặng hạ cấp.

```figure
t3-gateway-funnel
```

## Hãy xây dựng nó.

> **【中文解读】** `code/main.py`实现进程内协议网关 + 两个后端服务器──每个后端收到全新的当前协议请求;网关提供发现、按用户过的确定性`tools/list`、命名空间路由、注册中心 `server.json`+ State of External Access  Descriptor Lock  RBAC  theo quy trình kiểm toán của chủ thể `subscriptions/listen`SSE  xác nhận── mô hình nhận được đã giải quyết yêu cầu正文、路由头和已认证的 Bearer 身份, không phải là hoàn chỉnh HTTP 适配器传输层契约归 09──

`code/main.py`thực hiện một cổng thông tin giao thức trong quá trình và hai máy chủ hậu thuẫn. Mỗi cổng hậu thuẫn nhận được yêu cầu giao thức hiện tại mới. Cổng thông tin cung cấp khám phá, người dùng lọc xác định`tools/list`, định tuyến tên không gian, Registry `server.json`cộng với tình trạng nhập học bên ngoài, pin mô tả, RBAC, giới hạn lãi suất chính, quyết định kiểm toán và mô hình `subscriptions/listen`SSE xác nhận.

> `code/main.py`实现进程内协议网关和两个后端服务器――每个后端收到全新的当前协议请求――网关提供发现、按用户过的确定性`tools/list`、命名空间路由、注册中心 `server.json`+ trạng thái nhập cảnh bên ngoài  mô tả khóa  RBAC  theo chủ đề  định hạn  quyết định kiểm toán, cũng như xây dựng `subscriptions/listen`SSE xác nhận:

Mô hình nhận được các cơ quan yêu cầu được phân tích, tiêu đề định tuyến và một danh tính người mang xác thực. Nó không phải là một bộ điều chỉnh HTTP hoàn chỉnh và không phân tích `Content-Type`hoặc đầy đủ `Accept`kết nối nó với bộ chuyển đổi HTTP Streamable của bài học 09, đòi hỏi `Content-Type: application/json`và một `Accept`giá trị chứa cả hai `application/json`và `text/event-stream`- Tôi không biết.

> 模型接收已解析的请求正文、路由头和已认证的载体身份──它不是完整的HTTP 适配器,不解析`Content-Type`Hoặc hoàn chỉnh `Accept`契约──把它接到课09的流动HTTP 适配器上那边要求 `Content-Type: application/json`, và`Accept`Đồng thời bao gồm`application/json`Với`text/event-stream`

Đi đi.

> 运行:

```bash
cd phases/13-tools-and-protocols/17-mcp-gateways-and-registries
python3 code/main.py
python3 -m unittest discover code/tests -v
```

Demo in ID yêu cầu bên ngoài và ID yêu cầu hậu kết mới để hop vô quốc gia được nhìn thấy.

> 演示会打印外层请求 id 和全新的后端请求 id, để cho nhảy này không có trạng thái có thể nhìn thấy.

## Sử dụng nó thực tế

Thay thế các đối tượng hậu kết trong quá trình bằng các client giao thức hiện tại thực. Giữ các bộ phận giống nhau:

> Hãy chuyển các đối tượng trong quá trình thành thực tế trong các khách hàng giao dịch hiện tại.

- Hồ sơ nhập học trước khi kết nối.
  Trung ngữ翻译:连接之前先有准入记录──
- Khám phá hậu cảnh trước khi tiếp xúc khả năng.
  Trung ngữ翻译:能力暴露之前先完成后端发现──
- Tên công khai đủ điều kiện trước khi được cấp phép.
  Trung文翻译:授权之前先确定限定公开名──
- Pin mô tả trước khi danh sách hoặc gọi.
  Trung ngữ翻译:列表或调用之前先核对描述符锁定。
- Mét-đồ sơ mới theo yêu cầu trước khi chuyển tiếp.
  Trung ngữ翻译:转发之前先构造新鲜的每请求元数据──
- Kết quả xác nhận trước khi quay lại.
  Trung ngữ翻译:返回之前先校验结果──

## Chuyển nó đi.

Bài học này sẽ đi theo `outputs/skill-gateway-bootstrap.md`Nó tạo ra một thiết kế cổng thông tin hiện đại bao gồm nhập cảnh, khám phá, nhập cảnh, không gian tên, ủy quyền, lưu trữ trước, phát trực tuyến, đăng ký, MRTR, nhiệm vụ, khả năng quan sát và cách ly cũ.

> 本课产 出 `outputs/skill-gateway-bootstrap.md`Nó tạo ra mô hình trang web hiện đại, bao gồm nhập cảnh, phát hiện, tiếp cận, đặt tên, cấp phép, lưu trữ, lưu trữ, lưu trữ, đăng ký, MRTR, nhiệm vụ và phân lập.

## Tập luyện bài tập

1. Thêm bối cảnh theo dõi vào metadata yêu cầu bên ngoài và chuyển tiếp và ghi lại mối tương quan trong sự kiện kiểm toán.
   Trung ngữ 翻译: 给外层与转发的请求元数据加追上下文,并把关联关系记进审计事件──
2. Thêm một Backend và đường dẫn có khả năng nhiệm vụ `tasks/get`theo task id trong `Mcp-Name`- Tôi không biết.
   Trung文翻译:添加支持任务的后端,并按 `Mcp-Name`里的任务 id 路由 `tasks/get`
3. Thay đổi một mô tả hậu kết và chứng minh cả phát hiện và cuộc gọi trực tiếp đều bị chặn.
   Trung ngữ翻译:变更一个后端描述符,证明发现和直接调用都被阻止──
4. Thêm một khả năng máy chủ cụ thể về nguyên tắc và giải thích tại sao phát hiện phải được lưu trữ trong bộ nhớ cache riêng tư.
   Trung ngữ翻译:添加按主体定制的服务器能力,并解释为什么发现必须保持私有缓存──
5. Tạo một giao diện bộ chuyển đổi cũ mà không cần thêm bất kỳ trạng thái cũ nào vào hiện đại `Gateway`lớp học.
   Trung ngữ翻译:编写遗留适配器接口,且不给现代 `Gateway`类添加任何遗留状态──

## Từ khóa  Từ khóa nhanh chóng

| Term | Meaning | 中文 |
|------|---------|------|
| MCP gateway | Policy and routing server between clients and backend MCP servers | MCP 网关：客户端与后端 MCP 服务器之间的策略与路由服务器 |
| Admission record | Evidence and policy decision allowing one backend into the gateway | 准入记录：允许一个后端进入网关的证据与策略决定 |
| Qualified tool name | Stable public route such as `notes.search` | 限定工具名：稳定的公开路由，如 `notes.search` |
| Descriptor pin | Approved digest checked during discovery and dispatch | 描述符锁定：发现与分发期间核对的已批准摘要 |
| Private cache scope | Cached result restricted to one authorization context | 私有缓存范围：缓存结果限定于单一授权上下文 |
| Request-scoped SSE | Streaming response attached to one POST request | 请求级 SSE：附着于单个 POST 请求的流式响应 |
| `subscriptions/listen` | Client-opened SSE stream for selected long-lived change notifications | 客户端打开的 SSE 流，用于选定的长效变更通知 |
| Task route | Application mapping from an opaque task id to its backend | 任务路由：从不透明任务 id 到其后端的应用层映射 |
| Legacy adapter | Explicit version-gated boundary for old handshake and session behavior | 遗留适配器：为旧握手与会话行为设置的显式版本门控边界 |

## Xem thêm 延伸阅读

- [Streamable HTTP transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
  中文说明:Streamable HTTP 传输规范单 POST 端点与请求级 SSE 契约。
- [Server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  中文说明:`server/discover`规范网关与后端的双层发现依据──
- [Official Registry server.json requirements](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/official-registry-requirements.md)
  中文说明:官方注册中心 `server.json`要求发布元数据的字段契约──
- [MCP Tasks extension](https://tasks.extensions.modelcontextprotocol.io/specification/draft/tasks)
  Trung văn说明:MCP nhiệm vụ 扩展草案 nhiệm vụ vòng đời và `Mcp-Name`路由键――
