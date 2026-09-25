# MCP Security: Métadata độc hại, định tuyến, và MRTR trạng thái . MCP Security:投毒元数据、路由与MRTR 状态

> Không quốc tịch không có nghĩa là không tin tưởng, nó có nghĩa là mỗi yêu cầu cho thấy bằng chứng mà một máy chủ và cửa khẩu cần để xác nhận cuộc gọi độc lập.

> **【中文解读】**无状态不等于无需信任──2026-07-28 版 MCP 移除核心握手与协议会话,边界安全随其变化:工具描述、注解、客户端/服务器信息一律按不可信的数据处理──本课把七种攻击面列列 into a specific list,教你在网关做描述符整体哈希锁定、路由头先于策略的考验,以及MRTR 确认状态的防变化保护──

> **【拓展】**工具描述直接进入模型上下文,元数据因此成为MCP最大威胁面等于让第三方在系统提示内注入任意指令──2025-2026年 Invariant Labs、Unit 42等研究测得前沿模型对隐藏指令的遵守率高达70%以上;2026-07-28 规范的回应不是单个检测器,而是"证链"思路:每个请求自带的元数据是独立校验的依据──防御从"检测会话异常"转变为"校验请求自证"──

>  **【前置】**学本节前请先掌握:(1) Bước 13 · 07(MCP server) với 13 · 08(MCP client) 理解工具描述如何进入模型上下文;(2) Bước 13 · 09 của Streamable HTTP本课直接复用其路由头(`Mcp-Method`- Không.`Mcp-Name`);(3) Bối hình cơ bản của MRTR (多轮往返请求)

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 08 (MCP client) | **前置知识:** Phase 13 · 07（MCP 服务器）、Phase 13 · 08（MCP 客户端）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## Mục tiêu học tập

- Chế độ mô tả công cụ, ghi chú, thông tin khách hàng và thông tin máy chủ như dữ liệu không đáng tin cậy.
  Trung ngữ翻译:把工具描述、注解、客户端信息和服务器信息当作不可信的数据──
- Khám phá nhiễm metadata, thay đổi mô tả và va chạm tên giữa máy chủ.
  Trung ngữ翻译:检测元数据投毒、描述符变更和跨服务器命名冲突──
- Thiết lập metadata yêu cầu 2026-07-28 và tiêu đề định tuyến HTTP Streamable.
  Trung文翻译:校验 2026-07-28 请求元数据和流通 HTTP 路由头
- Bảo vệ MRTR `requestState`chống lại sự thao túng và buộc xác nhận với các lập luận chính xác.
  中文翻译:保护 MRTR `requestState`Không bị thay đổi,并把确认绑定到精确参数.
- Đưa ra giới hạn cấp phép và tỷ lệ cho một chủ nhân, chứ không phải một phiên giao thức bị xóa.
  Trung ngữ翻译:把授权和限流应用到主体 (主体) (chủ), thay vì bị xóa khỏi thỏa thuận.

> **【中文解读】**Mục tiêu học tập: tất cả dữ liệu một cách không thể tin; kiểm tra dữ liệu đầu tư thuốc, mô tả biến đổi, tên xung đột 3 loại vấn đề; theo quy tắc năm 2026-07-28  quy tắc yêu cầu kiểm tra 封封与路由头; phòng chống tình trạng MRTR 改并确认绑定精确参数;授权与限流定到主体而非删除的会话.

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**问题本质:模型、路由器、用户三方都依赖服务器提供的元数据做决策, một恶意描述符可以同时攻击三方──官方安全指南的态度很直接除非来自接收服务器,描述和注解一律不可信; ngay cả từ接收服务器,部署信任也会随着更新,攻陷,注册失误,网关合并而变化──

Một mô hình đọc mô tả công cụ để quyết định gọi gì. Một bộ định tuyến đọc tên công cụ để quyết định gửi yêu cầu. Người dùng đọc nhãn để quyết định phải chấp thuận gì. Một mô tả độc hại có thể nhắm mục tiêu cả ba.

> 模型读工具描述来决定调用什么;路由器读工具名来决定发送请求到哪里;用户读标签来决定批准什么―― một mô tả ác ý có thể tấn công cả 3 bên một lúc――

Các hướng dẫn bảo mật chính thức của MCP là trực tiếp: mô tả và ghi chú nên được coi là không đáng tin cậy trừ khi chúng đến từ một máy chủ đáng tin cậy. Ngay cả khi đó, sự tin tưởng triển khai có thể thay đổi.

> 官方MCP安全指南很直接: trừ khi từ máy chủ nhận, mô tả và ghi chép đều nên được coi là không đáng tin cậy. Ngay cả vậy, Bộ Trưởng Trung tâm cũng sẽ thay đổi  máy chủ cập nhật, bị xâm lược, gói ghi chép, hoặc kết nối mạng, tất cả có thể thay đổi nội dung của mô hình nhìn thấy.

Các giao thức hiện tại cũng thay đổi ranh giới an ninh. Năm 2026-07-28 không có cú tay cốt lõi và không có phiên giao thông.`Mcp-Session-Id`không phải là một thiết kế hiện tại.

> Khi thỏa thuận trước cũng thay đổi biên giới an ninh.`Mcp-Session-Id`关联审批,限制流或审审历史的安全设计, đã không phù hợp với quy tắc hiện hành.

>  **【类比】**元数据像商品外包装上的标签:采购员(模型) 看标签决定进哪个货物,分拣线(路由器) 看标签决定送哪条线,收货人(用户) 看标签决定签不签收收攻击者只要在标签上印一行小字(投毒描述),三方全部中招──2026-07-28 无状态化相当于"每件货物自带完整关关单单"请求元数据): 校验依据(随货同行,不再依赖"老客户脸" (熟客户脸) 👍🏻哈希锁定像定期比标签上纹可以偷标(地毯拉),但没有发现标签就错字投毒),所以还需要签叠加环环节 ((执行前限削减签)

## Khái niệm cốt lõi

> **【中文解读】**本节是全课核心,按防御纵深排列:七个攻击面清单 → 请求信封是证据而非身份 → 路由校验先于策略 → 锁定完整描述符 → 静态扫描是线 → 合并前先命名空间 → 能力声明不等于授权 → 保护无状态 MRTR 确认 → 高危调用 规则二 → 执行前削减权限 → 遗留交互路径 → 无状态传输检查――

### 7 mặt tấn công đáng kiểm tra

Hãy sử dụng danh sách cụ thể thay vì chỉ dẫn mơ hồ để cẩn thận.

> Sử dụng đơn giản thay thế "để nhỏ" loại này空泛提醒.

> **【中文解读】**七个攻击面:元数据投毒、描述符地毯拉、跨服务器影射、头/正文混、能力冒冒使用升级、MRTR 状态改、供应链身份混── chú ý chúng chồng lên nhau哈希锁定只防"变更"防不了"初版即毒",静态扫描只抓到明显短语,命名空间只消一类冲突──必须叠加控制──

1. **Metadata poisoning.**Mô tả chứa các hướng dẫn không liên quan đến hành vi công cụ được tuyên bố.
  Trung ngữ翻译:**元数据投毒。**描述包含与声明的工具行为无关指令──
2. **Descriptor rug pull.**Một tên, mô tả, sơ đồ hoặc ghi chú đã được chấp thuận trước đó thay đổi.
  Trung ngữ翻译:**描述符地毯拉扯。**Tên gọi đã được phê duyệt trước đó, mô tả, kế hoạch hoặc giải thích thay đổi.
3. **Cross-server shadowing.**Hai nền cho thấy cùng một tên công cụ không đủ điều kiện và định tuyến chọn một trong những tên này.
  Trung ngữ翻译:**跨服务器影射。**两个后端暴露同名未限定工具名,路由静默选择其一──
4. **Header and body confusion.** `Mcp-Method`hoặc `Mcp-Name`không đồng ý với yêu cầu JSON-RPC.
  Trung ngữ翻译:**头/正文混淆。** `Mcp-Method`Hoặc`Mcp-Name`Với JSON-RPC 请求不一致。
5. **Capability escalation.**Một đồng nghiệp yêu cầu một tính năng mở rộng hoặc khách hàng và máy chủ sai đó tuyên bố cho phép.
  Trung ngữ翻译:**能力冒用升级。**Đối với một tuyên bố mở rộng hoặc tính năng khách hàng, máy chủ đã đưa ra tuyên bố sai như được ủy quyền.
6. **MRTR state tampering.**Một khách hàng thay đổi `requestState`, trả lời một câu hỏi khác, hoặc sử dụng lại xác nhận với các lập luận khác nhau.
  Trung ngữ翻译:**MRTR 状态篡改。**客户端改 `requestState`、 trả lời một câu hỏi khác, hoặc xác nhận thay đổi các tham số lại.
7. **Supply-chain identity confusion.**Một tên hiển thị quen thuộc được coi là bằng chứng về danh tính nhà xuất bản hoặc máy chủ.
  Trung ngữ翻译:**供应链身份混淆。**熟悉的展示名被当作发行人或服务器身份证明──

Các bề mặt này chồng chéo. Hash pining giúp thay đổi mô tả nhưng không chứng minh rằng mô tả đầu tiên là an toàn. Quét tĩnh bắt được các cụm từ rõ ràng nhưng không phải hướng dẫn tinh tế. Namespacing ngăn chặn một lớp va chạm nhưng không phải là một máy chủ có không gian tên độc hại.

> Những mặt tấn công này chồng lên nhau. Hỗn khóa giúp phát hiện các mô tả thay đổi, nhưng chứng minh không có mô tả đầu tiên là an toàn.

### Báo cáo yêu cầu hiện tại là bằng chứng, không phải danh tính

> **【中文解读】**Xin xin tin là chứng cứ và không phải danh tính:`_meta`里的 `clientInfo`là chủ thể tự báo cáo, không thể được xác nhận;`serverInfo`适合日志与调试, nhưng không phải chứng chỉ, chứng chỉ đăng ký hoặc quyết định ủy quyền.

Mỗi yêu cầu năm 2026-07-28 bao gồm:

```json
{
  "_meta": {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientCapabilities": {
      "elicitation": {"form": {}}
    },
    "io.modelcontextprotocol/clientInfo": {
      "name": "security-lab",
      "version": "1.0.0"
    }
  }
}
```

Thiết lập phiên bản và hình dạng khả năng trên mỗi yêu cầu. Sử dụng các khả năng để chọn một hình dạng phản ứng tương thích. Không sử dụng `clientInfo`là một người chủ sở hữu xác thực.

> Mỗi yêu cầu đều có phiên bản và hình thức khả năng.`clientInfo`Khi được xác nhận chủ thể đã là tự báo cáo.

Tương tự như cảnh báo này cũng áp dụng cho `io.modelcontextprotocol/serverInfo`Nó hữu ích cho các nhật ký và debugging. Nó không phải là một chứng chỉ, chứng minh đăng ký, hoặc quyết định ủy quyền.

> Tương tự như vậy cũng áp dụng cho kết quả trong dữ liệu.`io.modelcontextprotocol/serverInfo` Nó phù hợp với việc viết日志 và调试, nhưng không phải chứng chỉ  đăng ký hoặc ủy quyền quyết định

### Thiết lập đường dẫn trước chính sách

> **【中文解读】**路由校验必须先于策略:`Mcp-Method`必须等于正文方法,`Mcp-Name` phải bằng `params.name`, không đồng bộ với luật lệ `-32020`拒绝并且应发生在选择后端、应用 RBAC、扣限制流令牌之前──错误码序列固定:头与正文不匹配 → HTTP 400 `-32020`;头文一致但版本不支持 → HTTP 400 `-32022`且 `data`精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`;未知方法 → HTTP 404 `-32601` không có thông báo`id`,永远不收 JSON-RPC 成功/错响应,HTTP 层接受后返回 202 空体──

Vì `tools/call`, Streamable HTTP bao gồm:

```text
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: notes.export
```

Phương pháp tiêu đề phải bằng phương pháp cơ thể.`params.name`Thử từ chối bất đồng với `-32020`trước khi chọn một backend, áp dụng RBAC hoặc tiêu thụ một token giới hạn lãi suất.

> Phương pháp của bài viết phải bằng với phương pháp chữ chính, tên của bài viết phải bằng với`params.name`∼ không nhất quán `-32020`拒绝要在选择后端,应用RBAC,消耗限流令牌之前完成.

Sự sắp xếp này đóng lại một sự mơ hồ phổ biến: một thành phần cho phép cơ thể trong khi một thành phần khác đi theo tiêu đề.

> Cái thứ tự này ngăn chặn một sự khác biệt thường: một bộ phận được ủy quyền theo văn bản, một bộ phận khác được chuyển giao theo đường dẫn.

> ️ **【易错点】**场景:组件 A 按 JSON-RPC 正文做授权,组件 B 按 `Mcp-Name`头做路由,头与正文不一致时没人拦截 / 后果: kẻ tấn công xây dựng"正文说 notes.search、头说 notes.export"的请求绕过授权直达高危工具 / 修复:(1) 固定校验顺序先校验 JSON-RPC 与元数据类型,再对对对对头与正文相等,最后检查版本支持;(2) 头文不一致一律 HTTP 400`-32020`,绝不"取其一继续"; 3) 限流令牌在全部校验通过后才扣减, ngăn chặn việc yêu cầu rác đốt số lượng quang.

Thiết lập bằng chứng bằng dây theo một chuỗi chính xác. Thiết lập các loại JSON-RPC và metadata, so sánh giá trị tiêu đề với cơ thể, sau đó kiểm tra xem phiên bản phù hợp có được hỗ trợ hay không. Một tiêu đề không phù hợp trả về HTTP 400 với `-32020`Nếu tiêu đề và cơ thể đồng ý về một phiên bản không được hỗ trợ, trả về HTTP 400 với `-32022`và `data`Đúng vậy.`{"supported":["2026-07-28"],"requested":"<actual>"}`. Một phương pháp không rõ trả về HTTP 404 với `-32601`- Tôi không biết.

> 线格式校验遵循唯一精确顺序:先校验 JSON-RPC与元数据类型,再比对头值与正文,最后检查是否支持版本匹配到的版本.头不匹配返回 HTTP 400 `-32020`; tiêu đề kết hợp nhưng phiên bản không hỗ trợ, quay lại HTTP 400 `-32022`且 `data`精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`;未known方法返回 HTTP 404 `-32601`

Mỗi đối tượng lỗi bao gồm tùy chọn `data`khi hợp đồng cần thông tin thu hồi có cấu trúc.`id`, vì vậy nó không bao giờ nhận được một thành công JSON-RPC hoặc phản ứng lỗi. Một thông báo HTTP được chấp nhận trả lại 202 với một cơ thể trống.

> Khi các giao ước cần được cấu trúc để phục hồi thông tin, mỗi lỗi đối tượng đều có thể được chọn.`data` không có thông báo`id`, vì vậy luôn không nhận JSON-RPC thành công hoặc phản ứng sai lầm.

### Đẹp toàn bộ mô tả

Một mô tả hash đơn độc bỏ lỡ các thay đổi sơ đồ và ghi chú. Canonicalize và hash các trường mô tả người dùng đã chấp thuận:

> Chỉ cần mô tả văn bản sẽ bỏ qua schema và thay đổi của nó.

```python
normalized = json.dumps(tool, sort_keys=True, separators=(",", ":"))
digest = hashlib.sha256(normalized.encode()).hexdigest()
```

Cung cấp bản ghi dưới một khóa có trình độ như `notes.export`, cùng với bằng chứng của nhà xuất bản và thời gian phê duyệt bên ngoài ví dụ đồ chơi này.

> Để lấy tập tin lên tên giới hạn`notes.export`(v) dưới; thực triển cũng cần phải kèm theo chứng chỉ và thời gian phê duyệt của nhà phát hành

Với mỗi lần làm mới:

- Chìa khóa không rõ: Quarantaine cho đến khi xem xét.
  Trung文翻译:未知键:隔离待审──
- Chìa khóa giống nhau, tiêu hóa khác nhau: Quarantaine như một kéo thảm cho đến khi được phê duyệt lại.
  Trung文翻译:同键不同摘要:按地毯拉隔离,直到重新批准──
- Tên không đủ điều kiện trùng lặp: yêu cầu không gian tên xác định.
  Trung文翻译:重复的未限定名:要求确定性命名空间──
- Nhấn máy quét: chặn và xem xét mô tả đầy đủ.
  Trung文翻译:扫描器命中:阻止并复审完整描述符──

Sự bình đẳng Hash chứng minh sự ổn định, không phải sự an toàn.

> 哈希相等 chứng minh là ổn định, không phải an toàn.

> 🤔 **【困惑】**Q: 静态扫描和哈希锁定都不完美,为什么还要做?A: Vì chúng rẻ và互补.

### Quét tĩnh là một dây tripwire

Các mẫu đơn giản có thể đánh dấu thẻ vai trò, lệnh vượt trội, ẩn, truy cập bí mật và các điểm đến mạng bị che giấu.

> Mô hình đơn giản có thể đánh dấu các mục tiêu của các nhân vật, chỉ thị bao phủ, hành vi ẩn, truy cập mật và kết nối với các mục đích mạng.

Chúng không phải là bằng chứng ngữ nghĩa. Một mô tả an toàn có thể chứa một cụm từ được đánh dấu trong một cảnh báo hợp pháp. Một mô tả độc hại có thể tránh mọi cụm từ.

> 静态扫描不是语义证明. 安全的描述可能因合法警告含被标记短语; 恶意的描述可以避免所有短语.

### Không gian tên trước khi sáp nhập

Giả sử hai máy chủ đều lộ ra`search`Đừng bao giờ để lệnh khám phá quyết định ai thắng.

> 假设 hai máy chủ đều bị lộ`search`Không cần phải để cho sự phát hiện của sự sắp xếp quyết định ai có hiệu quả.

```text
notes.search
issues.search
```

Tên được xác nhận là tên cửa ngõ công cộng. ghi lại bản đồ hậu kết riêng biệt. Tên ổn định làm cho sự chấp thuận, kiểm toán, pin hash, và `Mcp-Name`định tuyến liên quan đến cùng một đối tượng.

> 限定名是网关对外公开的名称;后端映射单独记录;;稳定的名字让审批,审计,哈希锁定和`Mcp-Name`路由指向同一个对象──

### Khả năng là tuyên bố tương thích

Theo yêu cầu`clientCapabilities`cho biết máy chủ có các tính năng giao thức nào mà khách hàng có thể xử lý. Nó không cho phép khách hàng truy cập vào các công cụ, dữ liệu hoặc hành động.

> Mỗi yêu cầu của `clientCapabilities`告诉服务器客户端能处理哪些协议特性――它 không cấp cho khách hàng quyền truy cập bất kỳ công cụ, dữ liệu hoặc động tác nào――

Việc ủy quyền vẫn xuất phát từ chính sách chính sách và nguồn lực được xác thực.

> 授权 vẫn đến từ chủ thể và nguồn lực đã được xác nhận.

1. Đăng bằng thông tin giao thông.
  Trung ngữ翻译:认证传输层凭证。
2. Thiết lập phiên bản, tiêu đề và hình dạng yêu cầu.
  Trung文翻译:校验版本、头部和请求形状──
3. Kiểm tra khả năng tương thích.
  Trung ngữ翻译:检查能力兼容性.
4. Quyền chính, công cụ, tài nguyên và các lập luận.
  Trung ngữ翻译:授权主体、工具、资源和参数──
5. Thực hiện hoặc yêu cầu nhập dữ liệu của người dùng.
  Trung ngữ翻译:执行或请求用户输入。

### Bảo vệ xác nhận MRTR không có quốc tịch

> **【中文解读】**MRTR(多轮往返请求) thay thế máy chủ thành máy chủ khách hàng`resultType: input_required`+ `inputRequests`(完整内嵌请求) + không rõ ràng `requestState`; khách hàng nhận được người dùng nhập sau khi sử dụng ID JSON-RPC mới 重试原方法并附上 `inputResponses`❖ Đặt điểm an toàn:`requestState`là nhập vào  phải ký hoặc mã hóa, và bị ràng buộc với phương pháp, công cụ, xác định các tham số, sử dụng, thời hạn hết hạn, chủ đề, tái放  phải紧时 cũng phải bị ràng buộc một lần không có.

Một công cụ có thể cần xác nhận người dùng. MCP hiện tại sử dụng nhiều yêu cầu đi vòng thay vì một cuộc gọi trở lại từ máy chủ đến khách hàng.

> 后果性工具可能需要用户确认──当前 MCP dùng nhiều轮往返请求(MRTR) thay thế máy chủ cho các调调的客户端──

Câu trả lời đầu tiên:

```json
{
  "resultType": "input_required",
  "inputRequests": {
    "confirm": {
      "method": "elicitation/create",
      "params": {
        "mode": "form",
        "message": "Export notes to archive?",
        "requestedSchema": {
          "type": "object",
          "properties": {
            "confirm": {"type": "boolean"}
          },
          "required": ["confirm"]
        }
      }
    }
  },
  "requestState": "opaque-integrity-protected-value"
}
```

Khách hàng nhận được đầu vào và thử lại phương pháp ban đầu với một ID JSON-RPC mới:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "notes.export",
    "arguments": {"query": "private", "destination": "archive"},
    "requestState": "opaque-integrity-protected-value",
    "inputResponses": {
      "confirm": {
        "action": "accept",
        "content": {"confirm": true}
      }
    },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "elicitation": {"form": {}}
      }
    }
  }
}
```

Mỗi người`inputRequests`value là một yêu cầu được nhúng hoàn chỉnh với `method`và `params`. Chìa khóa của nó phải phù hợp với mục tương ứng trong `inputResponses`. Một hình thức tạo ra sử dụng một object-root `requestedSchema`, và khách hàng phải đã tuyên bố khả năng kích hoạt biểu mẫu trước khi máy chủ yêu cầu nó.

> Mỗi người`inputRequests`值都是带 `method`和 `params`Ứng dụng được cài đặt đầy đủ, các khóa phải được`inputResponses`中对应条目匹配──表单诱导输入(elicitation) sử dụng đối tượng根的 `requestedSchema`, và trước khi máy chủ khởi động yêu cầu, khách hàng phải đã tuyên bố có khả năng chỉ dẫn một mình.

Khả năng hiện tại có hai tuyên bố hình thức hợp lệ. `{"elicitation":{}}`hỗ trợ ngầm hình thức tạo ra, trong khi `{"elicitation":{"form":{}}}`Một tuyên bố chỉ có URL như `{"elicitation":{"url":{}}}`không hỗ trợ yêu cầu biểu mẫu. máy chủ trả về HTTP 400 với `-32021`và `data.requiredCapabilities`bằng với `{"elicitation":{"form":{}}}`- Tôi không biết.

> Hiện có hai loại tuyên bố đơn hiệu quả:`{"elicitation":{}}`隐式支持表单,`{"elicitation":{"form":{}}}`显式声明── chỉ URL 声明`{"elicitation":{"url":{}}}`) không hỗ trợ biểu đơn yêu cầu, máy chủ quay lại HTTP 400 `-32021`, và`data.requiredCapabilities`Vì vậy`{"elicitation":{"form":{}}}`

Chữa bệnh`requestState`mã hóa nó, xác nhận nó và liên kết nó với phương pháp, công cụ, lập luận chính xác, mục đích, hết hạn, chính, và một lần không khi chơi lại các vấn đề. mã bài học sử dụng HMAC và lập luận chính xác phù hợp để làm cho ranh giới hiển thị.

> - Đưa đi.`requestState`Khi nhập vào: ký kết hoặc ghi mật, thử nghiệm,并 ràng buộc đến phương pháp, công cụ, xác định các tham số, sử dụng, quá hạn thời gian, chủ đề, tái đính kèm cần thiết, thời gian tái ràng buộc một lần nữa không có.

Các sổ cái nonce không được sống bên trong một đối tượng cửa khẩu. mô hình chạy được tiêm một cửa hàng tái phát có giới hạn, cắt TTL có thể được chia sẻ bởi nhiều trường hợp cửa khẩu. tuyên bố nguyên tử của nó là ranh giới thực hiện: chỉ một chấp nhận được xác nhận hoặc giảm kết thúc rõ ràng tiêu thụ trạng thái.`cancel`Không thực hiện bất cứ điều gì và vẫn có thể được sử dụng lại cho đến khi hết hạn.

> Không có tài liệu có thể được đặt trong một đối tượng kết nối mạng duy nhất. Mô hình có thể vận hành được vào một giới hạn.`cancel`Không thực hiện bất cứ điều gì, và giữ được có thể thử lại trước hết hạn.

Không lưu trữ bối cảnh xác nhận ẩn trong phiên giao thức. Bất kỳ phiên bản máy chủ nào cũng nên có thể xác nhận lần thử lại.

> Đừng đặt xác nhận ẩn trên văn bản lưu vào cuộc họp thỏa thuận.

### Quy tắc hai cho các cuộc gọi có rủi ro cao

> **【中文解读】**Quy tắc thứ hai: Dọc theo 3 điều轴分类 một lần调用消耗不可信输入、可访问敏感数据、引发后果性外部动作──单次自动步骤不应三者兼得: hoặc phân chia、 hoặc giảm quyền、 hoặc thông qua MRTR 求明显用户输入──这是设计启动式,不是协议能力──

Đánh phân một cuộc gọi dọc theo ba trục:

- Nó tiêu thụ đầu vào không tin cậy.
  Trung ngữ翻译:它消耗不可信输入──
- Nó có thể truy cập dữ liệu nhạy cảm.
  Trung ngữ翻译:它可能访问敏感数据──
- Nó gây ra một hành động bên ngoài hậu quả.
  Trung ngữ翻译:它引发后果性的外部动作──

Một bước tự động duy nhất không nên kết hợp cả ba. Chia nó, giảm quyền lợi hoặc yêu cầu nhập khẩu người dùng rõ ràng thông qua MRTR. Đây là một tính năng thiết kế, không phải là một tính năng giao thức.

> 单次自动步骤不应同时组合三项──拆分它──降权限,或通过MRTR 请显然用户输入──这是设计启发式,不是协议能力──

### Giảm quyền lực trước khi hành quyết

Sự vô quốc tịch đơn độc không phải là an toàn. Nó xóa lịch sử giao thức ẩn, nhưng một yêu cầu tự nhiên vẫn có thể yêu cầu một người xử lý có quyền vượt quá để rò rỉ dữ liệu hoặc thực hiện một thay đổi không thể đảo ngược. An toàn đến từ việc giảm quyền lực ở mỗi ranh giới:

> 仅靠无状态不安全. Nó đã di chuyển lịch sử giao thức ẩn, nhưng một yêu cầu tự chứa vẫn có thể cho phép quyền quá lớn xử lý tiết lộ dữ liệu hoặc làm thay đổi không thể đảo ngược.

1. **Typed verb.**Khám phá một hoạt động giới hạn như `archive_note`, không phải là thuốc chung .`run`hoặc `request`công cụ có thể thể hiện các quyền lực không liên quan.
  Trung ngữ翻译:**类型化动词。** Khám phá một hoạt động có giới hạn như `archive_note`, thay vì thể hiện quyền lực không liên quan .`run`Hoặc`request`工具──
2. **Validated arguments.**Sử dụng một kế hoạch đóng cửa khi thực tế, từ chối các trường không rõ, bình thường hóa các nhận dạng một lần, kích thước giới hạn, và xác nhận đích, người thuê nhà và sở hữu tài nguyên trước khi đánh giá chính sách.
  Trung ngữ翻译:**校验过的参数。**尽可能使用封闭方案,拒绝未知字段,标识符只规范化一次,限制大小,并策略评估前校试验目的地、租户和资源归属──
3. **Current authorization.**Kết nối nguyên tố xác thực với động từ chính xác, tài nguyên, môi trường và các lập luận bình thường.
  Trung ngữ翻译:**现行授权。**Việc kết nối chủ thể đã được xác nhận với các động từ, nguồn lực, môi trường và quy định các tham số.
4. **Action-bound approval.**Để gọi kết quả, liên kết sự chấp thuận với một bản ghi của động từ và các lập luận bình thường được gõ, cộng với chính sách chính, hết hạn và một lần. Bất kỳ trường nào thay đổi đều đòi hỏi phải có quyết định mới.
  Trung ngữ翻译:**绑定动作的批准。**Đối với việc điều chỉnh hậu quả, hãy kết hợp phê duyệt vào "những từ kiểu hóa động từ +  quy định các tham số", các yếu tố ngoài, thời gian quá hạn và chiến lược một lần.
5. **First-class refusal.**Mô hình từ chối, hết hạn phê duyệt, người dùng từ chối và không an toàn đích như kết quả bình thường mà không thực hiện bất kỳ tác dụng phụ nào. Đừng chuyển từ thành một công cụ trở lại yếu hơn.
  Trung ngữ翻译:**一等公民式的拒绝。**Để từ chối, quá hạn phê duyệt, người dùng từ chối và không an toàn mục đích như không thực hiện các tác dụng phụ kết quả thường xây dựng, đừng để từ chối được dịch thành yếu hơn  cơ bản công cụ.
6. **Redacted audit evidence.**Lưu ý ai đã hỏi, mô tả và phiên bản chính sách nào đã được sử dụng, mục tiêu tiêu bình thường được phép, lý do tại sao quyết định cho phép hoặc từ chối, và liệu việc thực thi có bắt đầu hay không.
  Trung ngữ翻译:**脱敏的审计证据。**记录谁发起了,使用了哪个准入描述符和策略版本,授权了什么规范化目标,决策为什么允许或拒绝,执行是否开始,存储或脱敏值,不存秘密,

Mỗi bước thu hẹp những gì thành phần tiếp theo có thể làm. Người xử lý cuối cùng nên nhận lệnh miền đã được xác nhận, không phải văn bản mô hình nguyên liệu cộng với các chứng chỉ rộng.

> Mỗi bước được thu hẹp theo một bộ phận có thể làm gì. Các bộ xử lý cuối cùng nên nhận được lệnh trong lĩnh vực đã được thử nghiệm, thay vì các mô hình gốc văn bản tăng cường thông tin.

### Các đường tương tác hiện tại và di sản

Root, Sampling và Logging đã bị lỗi thời cho các triển khai mới 2026-07-28. Một cửa cổng có thể giữ lại mã kênh yêu cầu cũ chỉ như một con đường tương thích được trang bị phiên bản.

> Roots、Sampling 和 Logging trong 2026-07-28 mới 实现中已弃用──网关只能把旧请求通道代码保留为版本门控的兼容路径──

Đừng xây dựng một hệ thống phòng thủ mới xung quanh giới hạn lấy mẫu mỗi phiên. Sử dụng hạn ngạch cho chính xác nhận, nhà phát hành, tài nguyên, công cụ và cửa sổ thời gian. Đối với công việc tương tác hiện tại, kiểm tra các yêu cầu nhập và phản hồi của MRTR.

> Đừng xây dựng một hệ thống phòng thủ mới xung quanh "đánh lấy mẫu theo cuộc họp". Đưa số lượng vào các đối tượng đã được xác nhận, phát hành, nguồn lực, công cụ và cửa sổ thời gian.

### Kiểm tra vận chuyển vô quốc tịch

- Tận dụng các tin nhắn MCP hiện đại tại điểm cuối POST duy nhất.
  Trung文翻译: 在单一 POST 端点接收现代 MCP 消息──
- Trả lại 405 cho GET và DELETE hiện đại.
  Trung文翻译:对现代 GET 和 DELETE 返回 405。
- Đừng đúc hoặc phụ thuộc vào `Mcp-Session-Id`- Tôi không biết.
  Trung文翻译:不造、不依赖 `Mcp-Session-Id`
- Phớt lờ phiên cũ và chơi lại tiêu đề như đầu vào quyền lực.
  Trung ngữ翻译:把旧式会话与重放头忽略掉,不作为权威输入──
- Trả lại JSON hoặc yêu cầu-scoped SSE cho POST đó.
  中文翻译:为该 POST 返回 JSON 或请求级 SSE。
- Sử dụng `subscriptions/listen`Chỉ cho các thông báo thay đổi lâu dài được chọn.
  Trung ngữ翻译: chỉ đối với 明确订阅的长效变更通知使用 `subscriptions/listen`

```figure
tp-tool-poisoning
```

## Hãy xây dựng nó.

> **【中文解读】** `code/main.py`实现一个小型进程内安全网关模型:规范化并锁定完整工具描述符、报告元数据投毒与跨服务器影射、校验现代请求信封与路由值,并使用签名 `requestState`加注入共享重放存储完成两轮确认导出.模型假定 HTTP 适配器已解析好 JSON 正文与路由头;传输层契约(`Content-Type`- Không.`Accept`)归 Bài học 09 的 Streamable HTTP 适配器──

`code/main.py`thực hiện một mô hình cổng thông tin bảo mật nhỏ trong quá trình. Nó canonicalize và pin đầy đủ mô tả công cụ, báo cáo nhiễm độc và bóng dữ liệu, xác nhận bao bì yêu cầu hiện đại và định tuyến giá trị, và thực hiện hai vòng xác nhận xuất với chữ ký `requestState`và một cửa hàng phát lại được tiêm.

> `code/main.py`实现一个小型进程内安全网关模型:规范化并锁定完整工具描述符、报告元数据投毒与影射、校验现代请求信封与路由值,并使用签名的 `requestState`Và nhập vào kho lưu trữ chia sẻ tái lưu trữ hoàn thành hai vòng xác nhận xuất khẩu.

Mô hình bắt đầu sau khi một bộ điều chỉnh HTTP đã phân tích cơ thể JSON và tiêu đề định tuyến. Nó không xác nhận `Content-Type`hoặc `Accept`Kết nối cùng một máy phát sóng với bộ chuyển đổi HTTP Streamable đầy đủ của bài học 09 , đòi hỏi `Content-Type: application/json`và một `Accept`giá trị chứa cả hai `application/json`và `text/event-stream`- Tôi không biết.

> 模型在HTTP 适配器解析完 JSON 正文与路由头后接手,它不校验 `Content-Type`Hoặc`Accept`❖ Đưa cùng một bộ phát phát nối đến bài học 09                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                `Content-Type: application/json`, và`Accept`Đồng thời bao gồm`application/json`Với`text/event-stream`

Đi đi.

> 运行:

```bash
cd phases/13-tools-and-protocols/15-mcp-security-tool-poisoning
python3 code/main.py
python3 -m unittest discover code/tests -v
```

Các mẫu cố tình biến đổi một mô tả.`input_required`phản ứng và thử lại không có quốc tịch.

> Example故意变更一个描述符: máy quét và bản tóm tắt so sánh các sản phẩm của riêng mình phát hiện độc lập; sau đó dẫn xuất trình bày`input_required`响应与无状态重试──

## Sử dụng nó thực tế

Thay thế `SAFE_TOOLS`với một snapshot bình thường từ các máy chủ được phê duyệt của riêng bạn. giữ tín dụng và bí mật khỏi snapshot. Xem xét mọi mô tả mới hoặc thay đổi trước khi cập nhật tiêu hóa của nó.

> - Đưa đi.`SAFE_TOOLS`换成你自己已批准服务器规范化快照──凭证和秘密不要进快照──每个新增或变更的描述符都必须先复审、再更新摘要──

Tại một cửa ngõ, chạy các kiểm tra tương tự trong quá trình phát hiện và một lần nữa trước khi gửi. Một bộ nhớ cache có thể làm giảm công việc phát hiện, nhưng sự chấp thuận được lưu trữ trong bộ nhớ cache phải hết hạn hoặc bị vô hiệu hóa khi mô tả thay đổi.

> Trong các kết nối mạng, phát hiện giai đoạn và phân phát trước mỗi chạy một lần nữa cùng một kiểm tra.

## Chuyển nó đi.

Bài học này sẽ đi theo `outputs/skill-mcp-threat-model.md`Nó tạo ra mô hình đe dọa giao thức hiện tại trên các metadata, định tuyến, khả năng, ủy quyền, MRTR, lưu trữ trước, đăng ký và ranh giới tương thích.

> 本课产 出 `outputs/skill-mcp-threat-model.md` Nó theo các giao thức hiện tại tạo mô hình đe dọa, bao gồm dữ liệu, đường dẫn, năng lực, quyền, MRTR, bộ nhớ, trung tâm đăng ký và khả năng hài hòa 8 loại biên giới.

## Tập luyện bài tập

1. Kết nối chính xác và quyết định cấp phép hiện tại với trạng thái MRTR được niêm phong, sau đó từ chối một lần thử lại theo một chính khác.
   Trung ngữ翻译:把已认证主体和现行授权决定绑定 into密封的MRTR 状态,然后拒绝换一个主体重试――
2. Thay thế kho lưu trữ lặp lại trong bộ nhớ bằng một phần nhập điều kiện bền vững và chứng minh hai quá trình không thể cả hai đều đòi hỏi một nonce.
   Trung文翻译:把内存重放储存换成持久化条件插入, chứng minh hai quá trình không thể cùng một lúc chiếm giữ cùng một nonce。
3. Đưa ra một lỗi sau khi yêu cầu tái phát nhưng trước khi xuất khẩu mô phỏng.
   Trung文翻译: 在占用重放状态后、模拟导出之前注入一个故障──定义并测试让恢复安全的事务或等规则──
4. Thay đổi công cụ `inputSchema`Không thay đổi mô tả của nó.
   Trung ngữ翻译:只改工具的 `inputSchema`Không thay đổi mô tả. Đảm nhận toàn bộ mô tả.
5. Thêm một chính sách từ chối lưu trữ trước khi `tools/list`khác nhau theo nguyên tắc.
   中文翻译:当 `tools/list`Trong khi đó, thêm từ chối chiến lược lưu trữ công cộng.
6. Mô hình một máy chủ cũ phía sau cổng. Đặt tất cả sự bắt tay và hành vi phiên sau một rõ ràng`2025-11-25`Hành vi tương thích.
   Trung ngữ翻译:在网关后面建模一台旧服务器──把所有握手与会话行为放进显而易见的`2025-11-25`兼容分支──

## Từ khóa  Từ khóa nhanh chóng

| Term | Meaning | 中文 |
|------|---------|------|
| Metadata poisoning | Instructions or deceptive claims embedded in a tool descriptor | 元数据投毒：工具描述符中嵌入指令或欺骗性声明 |
| Rug pull | Change to a previously approved descriptor | 地毯拉扯：已批准描述符发生变更 |
| Tool shadowing | Ambiguous routing caused by duplicate unqualified names | 工具影射：未限定重名导致路由歧义 |
| Header mismatch | Routing header and JSON-RPC body disagreement, error `-32020` | 头不匹配：路由头与正文不一致，错误码 `-32020` |
| Hash pin | Digest of the complete approved descriptor | 哈希锁定：完整已批准描述符的摘要 |
| MRTR | Stateless response and retry pattern for server-requested input | 多轮往返请求：服务器请求输入的无状态响应与重试模式 |
| `requestState` | Opaque round-trip value that must be treated as untrusted input | 不透明的往返值，必须视为不可信输入 |
| Capability declaration | Statement of protocol compatibility, not authorization | 能力声明：协议兼容性声明，不是授权 |
| Implicit form support | An empty `elicitation` capability object, equivalent to form support | 隐式表单支持：空 `elicitation` 能力对象，等价于支持表单 |
| Qualified tool name | Stable gateway name such as `notes.search` | 限定工具名：稳定的网关名，如 `notes.search` |

## Xem thêm 延伸阅读

- [MCP security and trust guidance](https://modelcontextprotocol.io/specification/2026-07-28#security-and-trust--safety)
  Trung văn说明:MCP 官方安全与信任指南(2026-07-28 版规范内嵌章节) ⋅
- [Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
  Trung văn说明:MRTR 模式规范本课确认状态防改的权威来源──
- [Streamable HTTP transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
  Trung văn说明:Streamable HTTP 传输规范路由头与POST 端点契约。
- [Deprecated features](https://modelcontextprotocol.io/specification/2026-07-28/deprecated)
  中文说明: bỏ qua các tính năng清单Roots/Sampling/Logging 等旧路径的归宿──
