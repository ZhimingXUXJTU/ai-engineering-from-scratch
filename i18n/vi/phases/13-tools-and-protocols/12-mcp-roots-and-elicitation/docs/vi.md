# Khả năng và quy định không có quốc tịch .

> Roots đã bị lỗi thời trong MCP 2026-07-28 và không bao giờ là một hộp cát bảo mật. Đặt phạm vi trong các lập luận công cụ hoặc tài nguyên URIs hiển thị, ủy quyền nó trên máy chủ, và sử dụng MRTR khi một công cụ thực sự cần input người dùng. Người dùng nhìn thấy quyết định, mô hình nhìn thấy tay cầm, và bất kỳ phiên bản máy chủ nào có thể xử lý thử lại.

> **【中文解读】**Chủ đề của bài học này đã xảy ra một sự thay đổi cơ bản trong phiên bản MCP 2026-07-28: Roots(root scope) đã bị chính thức bỏ qua nó không bao giờ là hộp bảo mật; Role domain information must appear apparently in tool parameter or resource URI 里, by server responsible authorized; elicitation(induced input) vẫn tồn tại, nhưng khi tool thực sự cần user input, hãy sử dụng MRTR(多轮往返请求)交付──user can see decision, model can see sentence handle, any server instance can handle re-try.

> **【拓展：显式作用域→可审计的 MCP 安全模型】**Đưa phạm vi từ trạng thái truyền tải ẩn vào các tham số yêu cầu có thể nhìn thấy, thay vào đó là kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, kiểm tra, và kiểm tra, và kiểm tra, kiểm tra, và kiểm tra, và kiểm tra, và kiểm tra, và kiểm tra, và kiểm tra, và kiểm tra, và kiểm tra.

>  **【前置】**Học本节前请先掌握:(1) Bước 13·07(MCP server) 工具调用与能力协商的基本形态;(2) Bước 13·11(MRT không có quốc gia) `input_required`Kết quả`requestState`回传、无会话重试机制,本课的发动性 完全建立在它上;

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 11 (stateless MRTR) | **前置知识:** Phase 13 · 07（MCP server）、Phase 13 · 11（无状态 MRTR）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## Mục tiêu học tập

- Thay thế Roots lỗi thời bằng các tham số không gian làm việc rõ ràng, URI tài nguyên hoặc cấu hình máy chủ.
  Trung文翻译:用显式工作区参数、资源 URI 或服务器配置取代废弃的 Roots。
- Các gợi ý phạm vi riêng biệt từ ủy quyền, hạn chế đường dẫn và sandboxing hệ điều hành.
  Trung ngữ翻译:把作用域提示与授权,路径包含检查,操作系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统, 系统
- Phương thức giao thức `elicitation/create`thông qua MRTR `input_required`kết quả.
  Trung ngữ翻译:通过 MRTR `input_required`Kết quả giao dịch đơn phương `elicitation/create`
- Tiến hành hỗ trợ kích hoạt trong các khả năng của khách hàng theo yêu cầu và từ chối các chế độ không được hỗ trợ.
  Trung ngữ翻译:在按请求的客户端能力中声明 支持,并拒绝不支持的模式──
- Định hành`accept`- `decline`, và`cancel`như những kết quả rõ ràng.
  Trung ngữ翻译:把 `accept``decline`和 `cancel`Có 3 kết quả khác nhau để chứng minh.
- Kết nối xác nhận phá hủy với một nguyên tắc xác thực, các lập luận ban đầu, bộ ứng cử viên và hết hạn.
  Trung文翻译:把破坏性确认绑定到已认证主体、原始参数、候选集和过期时间──

## Hai vấn đề trông giống nhau.

Một công cụ ghi chú nhận được yêu cầu này: "Tài ra báo cáo TPS cũ".

> Một tài liệu ghi chép nhận được yêu cầu như sau:" xóa báo cáo TPS cũ".""

Máy chủ phải trả lời hai câu hỏi khác nhau.

> 服务器 phải trả lời hai câu hỏi khác nhau.

1. Quá trình này có thể chạm vào không gian làm việc nào?
   Trung ngữ翻译: Đây là một hoạt động có thể chạm vào khu vực làm việc nào?
2. Người dùng có ý gì trong ba ghi chú tương ứng?
   Trung ngữ翻译:三条匹配的笔记里用户指的是哪一条?

Thứ nhất là phạm vi và ủy quyền. thứ hai là sự phân biệt rõ ràng tương tác. Trộn chúng dẫn đến các thiết kế nguy hiểm, chẳng hạn như xử lý một thư mục được cung cấp bởi khách hàng như bằng chứng rằng người gọi có thể xóa tất cả mọi thứ bên trong nó.

> Thứ nhất là vấn đề phạm vi và quyền hạn. Thứ hai là sự kết nối giữa hai thứ này và kết hợp chúng với nhau sẽ dẫn đến một thiết kế nguy hiểm.

> **【中文解读】**作用域(我能碰哪里) 与消歧义(用户指哪个) là hai vấn đề chính xác. 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用域: 作用: 作用域: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 作用: 

## Roots là một vùng di cư. Roots is a migration face.

Các sửa đổi trước đây của MCP cho phép khách hàng quảng cáo Roots và thông báo cho máy chủ khi danh sách thay đổi. Roots là hướng dẫn thông tin.

> Phiên bản sửa đổi MCP sớm hơn cho phép các thông báo khách hàng Roots không nằm trong danh sách khi thay đổi thông báo cho máy chủ. Roots là hướng dẫn thông tin.

MCP 2026-07-28 bị hủy bỏ `roots/list`và `notifications/roots/list_changed`cho các thiết kế mới. Tôi thích một trong những thay thế rõ ràng sau đây:

> MCP 2026-07-28 đối với thiết kế mới bị bỏ rơi`roots/list`和 `notifications/roots/list_changed`❖ ưu tiên sử dụng các giải pháp thay thế rõ ràng sau:

- A `workspaceUri`hoặc `directory`Truyện công cụ khi phạm vi khác nhau cho mỗi cuộc gọi.
  Trung ngữ翻译:作用域随调用变化时,用 `workspaceUri`Hoặc`directory`工具参数──
- Một URI tài nguyên khi hoạt động đã nhắm vào một tài nguyên.
  Trung ngữ翻译:操作本本就针对某资源时,用资源URI──
- Cấu hình máy chủ khi một triển khai sở hữu một không gian làm việc cố định.
  Trung ngữ翻译: Một部署 chỉ có một khu vực làm việc cố định, sử dụng các bộ phận dịch vụ.
- Một hộp cát xử lý hoặc hệ thống tệp bị bỏ tù khi mã phải không thể thoát ra.
  Trung ngữ翻译:当代码必须在技术上无法越界时,用进程沙箱或受限文件系统.

Nếu một sự tích hợp hiện có 2026-07-28 vẫn cần `roots/list`trong cửa sổ khấu trừ, máy chủ nhúng nó vào MRTR `inputRequests`Nó không được gửi một yêu cầu ngược trực tiếp. Đó là một bộ chuyển đổi chuyển đổi; người xử lý mới nên chấp nhận phạm vi rõ ràng thay vào đó.

> Nếu hiện có 2026-07-28 集成在废弃窗口仍需要 `roots/list`, máy chủ cần đặt nó vào MRTR `inputRequests`Trung── nó phải gửi phản hướng yêu cầu hoạt động── đó là chuyển ứng ứng dụng; bộ xử lý mới phải chấp nhận rõ ràng

Mô hình có thể nhìn thấy và lặp lại một tay cầm rõ ràng. phạm vi giao thông ẩn-giữ phiên khó kiểm tra, lặp lại, kiểm toán, và tuyến đường.

> 模型能看到并重复一个显式句柄──隐藏的传输会话作用域更难检查、重放、审计和路由──

>  **【类比】**Roots 像客人进门时口头说"我只去客厅" chủ nghe nhưng không khóa cửa; 显式作用域像每张出入证上都印着房间号,门禁系统(服务器授权) từng间验票――前者只是"提示",后者才是"凭证"――旧版把提示当边界使用;新版要求把边界写成见的参数,再由服务器真正执行授权检查――

### Quy tắc ba tầng

Một URI rõ ràng vẫn không tự cho phép.

> 显式 URI 本身仍不能自我授权──三层必须执行:

1. **Authorization:**Người quản lý có được chứng minh có được phép sử dụng không gian làm việc này không?
   Trung ngữ翻译:**授权：**Người có giấy phép này có được phép sử dụng khu vực làm việc này không?
2. **Containment:**URI mục tiêu bình thường có ở bên trong ranh giới không gian làm việc được phép không?
   Trung ngữ翻译:**包含检查：**Mục tiêu sau khi hợp nhất URI có vẫn nằm trong ranh giới của khu vực làm việc được ủy quyền không?
3. **Sandbox:**Hệ điều hành có thể ngăn chặn một máy chủ bị xâm nhập thoát khỏi không?
   Trung ngữ翻译:**沙箱：**Hệ điều hành có thể chặn được một máy chủ đã bị xâm lược trên biên giới không?

Các máy chủ chạy giữ một danh sách các URL không gian làm việc được ủy quyền, bình thường hóa các con đường mã hóa phần trăm, kiểm tra ranh giới thực của thành phần đường, và kiểm tra lại việc chứa ngay trước khi xóa.

> Có thể hoạt động máy chủ duy trì một danh sách trắng của URI của khu vực làm việc được ủy quyền, chuyển sang một phần trăm số mã hóa các đường, kiểm tra biên giới các bộ phận đường thực sự, và kiểm tra lại một thời gian trước khi xóa bao gồm các liên quan:

Các kiểm tra tiền tố chuỗi ngây thơ là sai:

> 朴素的前字符串检查是错的:

```text
allowed:   file:///work/notes
attacker:  file:///work/notes-evil/secret.md
traversal: file:///work/notes/%2e%2e/private.md
```

Cả hai con đường thù địch bắt đầu với một chuỗi gây hiểu lầm. Trước tiên bình thường hóa, sau đó so sánh các thành phần con đường. Một máy chủ hệ thống tập tin sản xuất cũng phải bảo vệ chống lại các cuộc đua liên kết biểu tượng và ngữ nghĩa con đường cụ thể cho nền tảng.

> Hai đường ác đều được mở bằng các chuỗi chữ cái sai lầm.

> ️ **【易错点】**场景: dùng `uri.startswith(workspace)`Làm chứa kiểm tra / 后果:`file:///work/notes-evil/secret.md`(前撞车) và `file:///work/notes/%2e%2e/private.md`(编码穿越) Tất cả có thể qua kiểm tra, tạo ra越界读写 / 修复:先 `unquote`归一化,再拆成路径组件逐段比较边界,删除前再查一次;真实文件系统实现还要防符号链接竞争(TOCTOU 窗口)

## Việc gọi vẫn còn, nhưng giao hàng đã thay đổi.

> **【中文解读】**Đó là cách thức tạo ra sự thay đổi lớn nhất trong bài học.`elicitation/create`, nhưng dòng trên đường chuyển hướng ngược đãi. 旧版(2025-11-25) máy chủ đang trong quá trình调用 đang phát hành một phản hướng JSON-RPC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `resultType: "input_required"`Kết quả, đưa biểu đơn yêu cầu vào`inputRequests`, khách hàng  trình đơn  thu thập câu trả lời `inputResponses`Với toàn bộ ID mới 重试 `tools/call`                                                                                                                                                                                                                                                              `requestState`Đưa đi.

Elicitation là tính năng client hiện tại để thu thập thông tin nhập của người dùng trong thời gian `tools/call`- `prompts/get`, hoặc`resources/read`Tên phương pháp vẫn còn`elicitation/create`Điều thay đổi là hướng chảy của dây.

> Lấy động là trong`tools/call``prompts/get`Hoặc`resources/read`期间 thu thập các tính năng khách hàng hiện tại của người dùng nhập vào.`elicitation/create` biến là hướng chuyển trên dòng 

Một máy chủ 2026-07-28 không gửi yêu cầu JSON-RPC ngược. Nó trả lại một `InputRequiredResult`- Có thể là:

> 2026-07-28  máy chủ không gửi ngược JSON-RPC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              `InputRequiredResult`- Có thể là:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "input_required",
    "inputRequests": {
      "delete_choice": {
        "method": "elicitation/create",
        "params": {
          "mode": "form",
          "message": "Choose one matching note and confirm deletion.",
          "requestedSchema": {
            "type": "object",
            "properties": {
              "note_id": {
                "type": "string",
                "enum": ["note-3", "note-7", "note-14"]
              },
              "confirm": {"type": "boolean"}
            },
            "required": ["note_id", "confirm"]
          }
        }
      }
    },
    "requestState": "integrity-protected-delete-state"
  }
}
```

Người dùng có thể chấp nhận, từ chối hoặc từ chối nó.`tools/call`Với một thẻ ID mới:

> 宿主染表单――用户可以接受、明确拒绝或关闭它――然后客户端使用全新的ID 重试原始的`tools/call`- Có thể là:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "notes_delete",
    "arguments": {
      "workspaceUri": "file:///Users/alice/Documents/Notes",
      "title": "TPS report"
    },
    "inputResponses": {
      "delete_choice": {
        "action": "accept",
        "content": {"note_id": "note-14", "confirm": true}
      }
    },
    "requestState": "integrity-protected-delete-state",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "elicitation": {"form": {}}
      }
    }
  }
}
```

Không có phiên giao thức giữa hai cuộc gọi. máy chủ xác minh trạng thái hồi âm, xác nhận phản ứng so với sơ đồ mong đợi, kiểm tra rằng ghi chú được chọn nằm trong bộ ứng cử viên đã ký kết, ủy quyền lại không gian làm việc, kiểm tra lại chứa, và sau đó xóa.

> 两次调用之间没有协议会话――服务器验证回传的状态、按预期方案 校验响应、检查选定的笔记确实在签名的候选人集里、重新授权工作区、重新检查包含关系,然后才删除──

## Capacity Negotiation Is Per Request  Capacity Negotiation On Request

Một khách hàng hỗ trợ kích hoạt chế độ biểu mẫu tuyên bố:

> 支持表单模式 elicitation 的客户端这样表示:

```json
{
  "io.modelcontextprotocol/clientCapabilities": {
    "elicitation": {"form": {}}
  }
}
```

Một khả năng kích hoạt trống rỗng,`"elicitation": {}`, vẫn tương đương với hỗ trợ tương thích chỉ bằng hình thức.`"elicitation": {"form": {}}`cũng hỗ trợ chế độ biểu mẫu. Một tuyên bố chỉ có URL, `"elicitation": {"url": {}}`, không. máy chủ không được nhúng một chế độ không có khả năng của yêu cầu hiện tại, ngay cả khi yêu cầu trước đó quảng cáo nó.

> 空的 kích thích  năng lực `"elicitation": {}`Vì sự khả năng tương thích vẫn còn giá trị như chỉ hỗ trợ biểu tượng đơn `"elicitation": {"form": {}}"`Đồng thời hỗ trợ biểu diễn đơn phương.`"elicitation": {"url": {}}"`则不支持── máy chủ phải nhúng vào mô hình không tồn tại trong khả năng yêu cầu hiện tại, ngay cả khi yêu cầu trước đó tuyên bố đã thực hiện nó──

Mỗi yêu cầu cũng có chứa`io.modelcontextprotocol/protocolVersion`. Một phiên bản bị mất hoặc không có chuỗi trả lại `-32602`Một chuỗi không được hỗ trợ sẽ quay lại`-32022`chính xác`supported`và `requested`dữ liệu. Phản hồi hỗ trợ thu hồi bị thiếu hoặc chỉ có URL `-32021`với `data.requiredCapabilities`được thiết lập`{"elicitation":{"form":{}}}`- Tôi không biết.

> Mỗi yêu cầu cũng mang theo`io.modelcontextprotocol/protocolVersion`△ 缺失或非字符串的版本返回 `-32602`▽不支持的字符串返回 `-32022`,并附带精确的`supported`Với`requested`数据──缺失或仅 URL 支持返回 `-32021`- Tôi không biết.`data.requiredCapabilities`设为 `{"elicitation":{"form":{}}}`

Một phong bì mà không có JSON-RPC `id`là một thông báo. xử lý nó mà không phát ra một thành công JSON-RPC hoặc phản ứng lỗi. Trên Streamable HTTP, một thông báo được chấp nhận nhận nhận `202 Accepted`Không có xác.

> 没有 JSON-RPC `id`Trong HTTP được phát trực tuyến, nhận được thông báo nhận được không có phản ứng.`202 Accepted`

`clientInfo`nên được bao gồm để chẩn đoán, nhưng nó tự báo cáo và không thể xác định người dùng để được ủy quyền.

> `clientInfo` phải được bao gồm để chẩn đoán, nhưng nó là dữ liệu tự báo cáo, không thể được sử dụng như một người dùng có nghĩa là ủy quyền.

Các máy chủ thực hiện `server/discover`và trả lại`supportedVersions`, khả năng,`ttlMs`, và`cacheScope`với `resultType: "complete"`Nó không quảng cáo Roots cho thiết kế hiện đại này. Bởi vì nó quảng cáo các công cụ, nó cũng thực hiện bắt buộc `tools/list`Kết quả đó trả lại số xác định`notes_delete`mô tả, một đối tượng hợp lệ `inputSchema`, dữ liệu siêu dạng máy chủ, và gợi ý cache công cộng.

> 服务器实现 `server/discover`, quay lại`supportedVersions`、 khả năng`ttlMs`和 `cacheScope`- Tôi không biết.`resultType`Vì vậy`"complete"`Trong thiết kế hiện đại này nó không tuyên bố Roots. Vì nó tuyên bố công cụ, vì vậy cũng thực hiện bắt buộc.`tools/list` Kết quả trở lại xác định`notes_delete`描述符、合法的 đối tượng `inputSchema`、 dữ liệu và lưu trữ công khai của máy chủ

> 🤔 **【困惑】**Q: 客户端上次请求明确声明过支持表单发动,服务器这次为什么还需要再检查一次? A: Vì năm 2026-07-28 没有会话 每次请求都是独立宇宙,能力声明只对当前请求有效.`_meta`

## Chế độ hình thức

> **【中文解读】**Mô hình đơn với giới hạn 平 JSON Schema  mô tả" người dùng cần phải điền gì": gốc là đối tượng, thuộc tính chỉ có thể là 平's nguyên bản hoặc các tập hợp 枚举. định vị là "chúng kết nối nhỏ và có thể sử dụng", không phải là một động cơ đơn đơn thông thường 消歧义、破坏性确认、非敏感偏好收集是它的主场.

Phương thức biểu mẫu sử dụng một sơ đồ JSON hạn chế được thiết kế cho các đối thoại có thể sử dụng. Root là một đối tượng và các thuộc tính của nó là các trường nguyên thủy bằng phẳng hoặc hỗ trợ các mảng enum. Các đối tượng sâu và các sơ đồ tài liệu mục đích chung không thuộc vào một đối thoại xác nhận.

> Mô hình biểu đơn sử dụng cho thiết kế khung đối thoại có sẵn. Mô hình JSON có giới hạn.

Sử dụng chế độ biểu mẫu cho:

> 表单模式适用于:

- chọn một trong nhiều ứng cử viên;
  Trung ngữ翻译: từ多个候选中选择一个;
- xác nhận hoạt động phá hủy;
  Trung文翻译: xác nhận một tác động phá hoại;
- thu thập các ưu tiên không nhạy cảm;
  中文翻译: thu thập những sự lựa chọn không nhạy cảm;
- thu thập một số lượng nhỏ các giá trị người dùng, chứ không phải là mô hình, phải quyết định.
  Trung ngữ翻译:收集少量必须由用户 (而不是模型) quyết định giá trị.

Không sử dụng chế độ biểu mẫu cho mật khẩu, khóa API, mã thông báo truy cập hoặc thông tin tín dụng thanh toán.

> Đừng sử dụng mô hình đơn để thu thập mật khẩu, API khóa, giấy phép truy cập hoặc chứng chỉ thanh toán.

Các máy chủ xác nhận nội dung được trả lại một lần nữa. xác nhận hình thức bên khách hàng cải thiện UX nhưng không tạo ra sự tin tưởng.

> 服务器 cần tái kiểm tra nội dung trả lại                                                                                                                                                                                                                                                          

## - Định hướng URL

Chế độ URL gửi một URL web an toàn cho một tương tác ngoài băng:

> URL 模式 gửi một URL web an toàn, được sử dụng để giao tiếp:

```json
{
  "method": "elicitation/create",
  "params": {
    "mode": "url",
    "message": "Connect the report service to continue.",
    "url": "https://mcp.example.com/connect/report-service"
  }
}
```

Sử dụng nó khi thông tin nhạy cảm phải đi trực tiếp đến một dòng web được kiểm soát bởi máy chủ, chẳng hạn như ủy quyền của bên thứ ba. Khách hàng hiển thị toàn bộ điểm đến và nhận sự đồng ý trước khi mở nó. Nó không được mua trước URL.

> Khi thông tin nhạy cảm phải trực tiếp vào Web 流程 của máy chủ kiểm soát (như được cấp phép của bên thứ ba) khi sử dụng nó.

Một `accept`phản ứng có nghĩa là người dùng đồng ý mở URL. Nó không chứng minh dòng bên ngoài đã hoàn thành. Khi thử lại, máy chủ kiểm tra trạng thái của riêng nó và hoặc hoàn thành hoặc trả lại một `input_required`kết quả.

> `accept`响应 cho biết người dùng đồng ý mở URL này. Nó không chứng minh quá trình bên ngoài đã hoàn thành.`input_required`Kết quả.

URL không thay thế cho quyền giữa khách hàng MCP và máy chủ MCP. Nó là cho một tương tác bên ngoài mà máy chủ MCP cần thực hiện thay mặt cho người dùng.

> URL elicitation không phải là một thay thế được cấp quyền giữa MCP khách hàng và MCP máy chủ. Nó được sử dụng để đại diện cho người dùng của MCP máy chủ thực hiện giao tiếp bên ngoài.

## Các chi nhánh phản ứng

Chống hành động như quyết định sản phẩm, chứ không phải là biệt danh:

> Hãy coi những động tác này như quyết định sản phẩm, chứ không phải là từ ngữ:

| Action | Meaning | Safe server behavior |
|--------|---------|----------------------|
| `accept` | User submitted the interaction | Validate content and continue |
| `decline` | User explicitly refused | Return a complete, non-error refusal outcome |
| `cancel` | User dismissed or could not finish | Stop safely and allow a later retry |

> **【中文解读】**表格对照(zh 版):`accept`= Người dùng đã gửi giao tiếp trước khi tiếp tục nội dung thử nghiệm;`decline`= User explicit refused  return complete non-error refused result (người dùng đã từ chối hoàn toàn kết quả không sai lầm)`cancel`= User shut or failed to complete  security stop, allow later to try again──

Đừng bao giờ giải thích nội dung thiếu như sự đồng ý. Đừng bao giờ chuyển đổi sự từ chối thành vòng lặp lặp lặp lại.

> 永远不要把缺失内容解释为同意.永远不要把衰退变成重复弹窗的循环.

## Bảo vệ trạng thái MRTR hủy hoại

Danh sách ứng cử viên không thể chỉ tồn tại trong một giá trị Base64 được nhắc hoặc không ký. Một khách hàng kiểm soát mọi thứ nó gửi lại.

> Danh sách ứng cử viên không thể chỉ sống trong các từ đề nghị hoặc không ký vào Base64  giá trị.

Bài học ký một tải trọng hữu ích của nhà nước chứa:

> 本课对包含以下内容的状态载荷签名:

- chính xác nhận;
  中文翻译:已认证主体;
- phương pháp xuất xứ;
  Trung văn翻译:发起方法;
- tiêu hóa của `workspaceUri`và `title`-
  Trung ngữ翻译:`workspaceUri`和 `title`
- Các thẻ ghi nhận được cho phép được hiển thị trong biểu mẫu;
  中文翻译:表单中展示的允许笔记 id 集合;
- giai đoạn vận hành;
  中文翻译:操作阶段;
- Thời hạn ngắn.
  Trung ngữ翻译:较短的过期时间──

Trước khi đột biến, máy chủ cũng kiểm tra hồ sơ ghi chép trực tiếp. Điều này bắt được các cuộc đua xóa và một mục tiêu di chuyển ra khỏi không gian làm việc sau khi biểu mẫu được hiển thị.

> Trước khi thay đổi, máy chủ cũng sẽ kiểm tra ghi chép hoạt động. Nó có thể bắt được việc xóa cuộc thi, cũng như tình hình mục tiêu được chuyển khỏi khu vực làm việc sau khi hiển thị đơn.

Đối với một hành động tài chính hoặc không thể đảo ngược một lần, chỉ có HMAC không ngăn cản trạng thái hợp lệ được tái diễn trong thời hạn hết hạn của nó. Cung cấp và tiêu thụ nonce chính xác một lần trong một cửa hàng phát lại được chia sẻ bởi mỗi trình xử lý. Bài học tiêm một cửa hàng bị giới hạn, cắt TTL và giữ nguyên tử của nó khi thực hiện xóa trong bộ nhớ. Một cơ sở dữ liệu sản xuất nên kết hợp yêu cầu nonce và đột biến trong một giao dịch hoặc ranh giới viết điều kiện tương đương.

> Đối với một lần hoạt động tài chính hoặc không thể đảo ngược, chỉ dựa vào HMAC không thể ngăn chặn một trạng thái hợp lệ trong thời gian qua được tái lưu trữ. Trong một kho lưu trữ tái lưu trữ được chia sẻ trong tất cả các ví dụ xử lý, phải được lưu trữ và tiêu thụ một lần không có.

Thiết lập sự tương tác trước khi yêu cầu nonce.`cancel`không thực hiện đột biến và để lại trạng thái có thể tái tạo cho đến khi hết hạn.`decline`là cuối cùng, nên bài học tiêu thụ nonce mà không xóa bất cứ điều gì.

> Trong tuyên bố không có  trước khi học tập giao tiếp │ hình thức phản ứng sai lầm │`cancel`Không thực hiện thay đổi, trạng thái trong quá trình trước giữ được thử lại.`decline`là kết thúc, vì vậy bài học này trong trường hợp không xóa bất cứ điều gì tiêu thụ không còn.

> ️ **【易错点】**场景: chỉ làm HMAC 签名、不做一次性 nonce / 后果: tấn công viên(或重复的客户端重试) trong cửa sổ quá hạn `requestState`+ `inputResponses`, cùng một xóa được xác nhận hai lần; nhiều thí dụ triển khai dưới hơn khó nhận thấy / sửa chữa: ký chỉ giải quyết " trạng thái chưa được thay đổi", không giải quyết " trạng thái chỉ sử dụng một lần";把" tuyên bố không + 执行变更" đưa vào cùng một atom biên giới (事务或条件写),并让所有实例共享 cùng một lưu trữ tái lưu trữ。

```figure
t3-roots-boundary
```

## Hãy xây dựng nó.

`code/main.py`cho thấy một hiện đại `notes_delete`công cụ:

> `code/main.py`演示一个现代的  演示一个现代的`notes_delete`工具:

- `tools/list`trả lại mô tả xác định, có thể lưu trữ trong cache với không gian làm việc và sơ đồ tiêu đề cần thiết.
  Trung ngữ翻译:`tools/list`返回带必需工作空间与标题方案的确定性、可缓存描述符──
- Khu vực này là một sự rõ ràng `workspaceUri`tranh luận.
  Trung ngữ翻译:作用域是显式的`workspaceUri`参数。
- Cấu hình máy chủ cho phép không gian làm việc cho chủ tịch bài học.
  Trung ngữ翻译:服务器配置为课程主体授权该工作区──
- URI bình thường hóa từ chối nhầm lẫn tiền tố và quá trình mã hóa.
  Trung文翻译:URI 归一化拒绝前混和编码穿越──
- Mỗi loại bỏ tiêu diệt đòi hỏi tính năng tạo ra dạng.
  Trung文翻译: 每次破坏性删除都要求表单模式诱导──
- Sự kích thích đi vào bên trong.`resultType: "input_required"`- Tôi không biết.
  中文翻译:elicitation 装在 `resultType: "input_required"`里传输.
- Đăng ký`requestState`kết hợp danh sách ứng cử viên chính xác và các lập luận ban đầu.
  Trung ngữ翻译:签名的 `requestState`绑定精确候选人列表和原始参数──
- Một cửa hàng sao chép được tiêm từ chối trạng thái chấp nhận hoặc từ chối tương tự trên các phiên bản máy chủ.
  Trung ngữ翻译:注入的重放存储跨服务器实例拒绝同一个已接受或已拒绝的状态.
- Việc thử lại sử dụng một ID yêu cầu mới và trả lại `resultType: "complete"`- Tôi không biết.
  Trung文翻译:重试使用全新请求 id 并返回 `resultType: "complete"`

Kho lưu trữ dữ liệu là trong bộ nhớ vì vậy hành vi giao thức dễ dàng để kiểm tra. Các quy tắc bảo mật vẫn giống nhau với một cơ sở dữ liệu.

> Trong bộ nhớ dữ liệu, dễ dàng kiểm tra giao thức hành vi.

## Sử dụng nó để kiểm tra

Từ nguồn kho:

> Từ thư mục kho:

```bash
cd phases/13-tools-and-protocols/12-mcp-roots-and-elicitation/code
python3 main.py
python3 -m unittest discover tests -v
```

Các điểm kiểm soát dự kiến:

> 预期检查点:

- Discovery quảng cáo công cụ không có Roots.
  Trung文翻译:发现结果声明工具而没有根子.
- Trình phát hiện công cụ `notes_delete`với `resultType`, danh tính máy chủ, và gợi ý cache.
  Trung ngữ翻译:工具发现回带 `resultType`、 danh tính và lưu trữ của máy chủ `notes_delete`
- Đơn xin ID `1`trả lại mẫu trong `inputRequests.delete_choice`- Tôi không biết.
  中文翻译: yêu cầu id `1`Trong `inputRequests.delete_choice`Trong trở lại biểu diễn đơn giản.
- Đơn xin ID `2`lặp lại trạng thái đã ký và hoàn thành việc xóa.
  中文翻译: yêu cầu id `2`回传签名状态并完成删除──
- Một con đường tiền tố và một con đường đi qua được mã hóa đều không được kiểm soát.
  Trung ngữ翻译:前路径和编码穿越路径都未经含检查──
- Một tiêu đề thay đổi không thể sử dụng lại trạng thái xác nhận ban đầu.
  Trung文翻译:改过的标题不能复用原始确认状态──
- Một sự sụt giảm sẽ không thay đổi nó.
  Trung文翻译:decline 后笔记保持不变──
- Hai đối tượng máy chủ chia sẻ lưu ý và trạng thái phát lại không thể cả hai thực hiện một xác nhận.
  Trung ngữ翻译: hai đối tượng máy chủ chia sẻ ghi chép và đặt lại không thể thực hiện cùng một xác nhận.
- Các tuyên bố biểu mẫu trống và rõ ràng hoạt động, trong khi hỗ trợ chỉ URL trả lại chính xác `-32021`yêu cầu về mẫu.
  Trung ngữ翻译:空声明和显式表单声明都能工作,而只有URL 支持返回精确的 `-32021`                                                                                                                                                                                                                                                              
- Các lỗi phiên bản không được hỗ trợ sử dụng chính xác `-32022`hình dạng dữ liệu.
  Trung ngữ翻译:不支持的版本失败使用精确的 `-32022`Số liệu hình dạng:
- Một thông báo không có id không tạo ra phản ứng JSON-RPC.
  Trung文翻译:无 id 的通知不产生 JSON-RPC 响应──

## Chuyển nó đi.

`outputs/skill-elicitation-form-designer.md`thiết kế phạm vi rõ ràng, kiểm tra ủy quyền, biểu mẫu MRTR, chi nhánh phản ứng và liên kết trạng thái. Nó từ chối đối xử với Roots cũ như một hộp cát hoặc thu thập bí mật thông qua chế độ biểu thức.

> `outputs/skill-elicitation-form-designer.md`设计显式作用域、授权检查、MRTR 表单、响应分支和状态绑定── nó từ chối bỏ bỏ ra Roots bị bỏ rơi như một hộp, cũng từ chối thông qua表单模式收集秘密──

## Tập luyện bài tập

1. Thay thế kho lưu trữ lặp lại trong bộ nhớ bằng SQLite. Sử dụng một giao dịch để yêu cầu nonce và xóa ghi chú, sau đó chứng minh hai quá trình không thể cả hai cam kết.
   Trung文翻译:把内存重放储备换成SQLite。 dùng một tuyên bố giao dịch không có và并删除 ghi chú, sau đó chứng minh hai quá trình không thể gửi thành công。
2. Thêm `url`đàm phán khả năng và một dòng thiết lập ngoài băng thông.`inputResponses`- Tôi không biết.
   Trung ngữ翻译:添加 `url`能力协商和一个带外设置流程──让第三方凭据远离 `inputResponses`
3. Thay thế bản đồ ghi chú trong bộ nhớ bằng cơ sở dữ liệu SQLite tạm thời. Kiểm tra lại quyền và chứa bên trong giao dịch đột biến.
   Trung ngữ翻译:把内存笔记映射换成临时SQLite 数据库――在变更事务内部重新检查授权和包含关系――
4. Thêm một chính sách liên kết biểu tượng cho một hệ thống file thực tế thực hiện. Giải thích tại sao việc chứa từ điển URI một mình không thể ngăn chặn một sự thoát khỏi liên kết biểu tượng.
   Trung ngữ翻译:为真实文件系统实现添加符号链接策略──解释为什么仅靠 URI 词法包含检查不住符号链接逃逸──
5. Thiết kế một bộ điều chỉnh 2025-11-25 để lập bản đồ đầu ra xử lý MRTR hiện đại cho việc khởi động của máy chủ cũ. Giữ nó cách ly khỏi xử lý hiện tại.
   Trung ngữ翻译:设计一个 2025-11-25 适配器,把现代 MRTR 处理器输出映射为旧版服务器发起的发动.

## Từ khóa  Từ khóa nhanh chóng

| Term | Meaning in 2026-07-28 |
|------|------------------------|
| Roots | Deprecated informational workspace hints, not authorization or sandboxing |
| Explicit scope | Workspace, directory, or resource handle visible in request arguments |
| Containment | Normalized path-component check that keeps a target inside a boundary |
| Elicitation | Client feature for obtaining user input during an MCP operation |
| Form mode | In-band structured user input using a restricted flat schema |
| URL mode | Out-of-band interaction for sensitive or external workflows |
| MRTR | Stateless input-required result followed by a fresh retry |
| `requestState` | Opaque state echoed exactly and integrity-checked by the server |
| Decline | Explicit user refusal |
| Cancel | Dismissal or incomplete interaction without approval |

> **【中文解读】**术语速查(中英对照):Roots= đã bị loại bỏ 信息性工作区提示,不是授权也不是沙箱;Explicit scope=显式作用域,请求参数中可见的工作区/目录/资源柄句;Containment=包含检查,归化路径组件检查;Elicitation=诱导输入,MCP 操作期间获取用户输入的客户端特性;Form mode表=单模式; Mode=带外交互URL;MRTR=无状态的输入_required 结果加全新重试;requestState=样原传并由服务器做完整性检验的不透明状态;Decline=明确拒绝;Cancel=未完成关闭──

## Legacy Compatibility Ước tính

Đối với một người đồng nghiệp bị buộc phải đến năm 2025-11-25, `roots/list`- `notifications/roots/list_changed`, và được khởi động bởi máy chủ trực tiếp`elicitation/create`Đánh dấu di sản bộ chuyển đổi. Đừng cho phép danh sách gốc cũ bỏ qua quyền cho máy chủ, và không mang các giả định giao thức-phát họp vào trình xử lý hiện đại.

> Đối với khóa vào 2025-11-25 đối với kết thúc,`roots/list``notifications/roots/list_changed`Và hoạt động của máy chủ khởi động `elicitation/create`Có thể vẫn tồn tại. Không cho bộ điều chỉnh đó gắn vào thẻ cũ. Đừng để bản gốc cũ của danh sách vượt qua quyền cấp phép của máy chủ.

## Xem thêm 延伸阅读

- [MCP 2026-07-28 Elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)
  中文翻译:2026-07-28 版 elicitation 官方规范。
- [MCP 2026-07-28 Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
  Trung ngữ翻译:MRTR(多轮往返请求)模式规范,`input_required`Kết quả của quyền lực được định nghĩa:
- [MCP 2026-07-28 Roots deprecation](https://modelcontextprotocol.io/specification/2026-07-28/client/roots)
  Trung文翻译:Roots 废弃说明。
- [MCP 2026-07-28 server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  Trung ngữ翻译:`server/discover`发现机制规范──
