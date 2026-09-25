# MCP Resources and Prompts: Adressable Context for Stateless Servers  MCP Resources with Tip: 無状态服务器的可寻址上下文

> Các công cụ thực hiện các hoạt động. Các tài nguyên phơi bày nội dung có thể địa chỉ. Cảnh báo gói mẫu tin nhắn được người dùng chọn. Một máy chủ MCP tốt giữ các hợp đồng đó riêng biệt và dự đoán.

> **【中文解读】**三种服务器原语各司其职:工具 执行操作,资源 暴露可寻址的内容,提示 打包用户选择的消息模板。 một MCP 服务器合格让这三份契约彼此分离、可预期──本课还把这三者放进2026-07-28无状态信封:没有初始化握手,每个请求自带协议版本和能力,列表结果确定性排序,缓存提示(`ttlMs`- Không.`cacheScope`) trở thành một phần của sự thật.

> **【拓展：原语三分→真实产品】**现实中的分工例:GitHub MCP 把问题详情做成资源(URI 可寻址、宿主可附加到上下文),把"创建问题"做工具(有副作用),把"代码审查工作流"做提示模板(用户一键触发) ――2026-07-28 的新约束是:资源订阅不再使用`resources/subscribe`Nhưng là một sự thống nhất.`subscriptions/listen`Các yêu cầu cấp đáp ứng dòng chảy với bài học 09 của truyền tải tầng tiến triển một liên kết.

>  **【前置】**学本节前请先掌握:(1) Giai đoạn 13·07(Construction MCP 服务器) Tools/list、tools/call 的实现;(2) Giai đoạn 13·09(MCP 传输层)无状态信封、`_meta`键,`subscriptions/listen`◎ URI 概念`file://`、 tự định nghĩa quy trình);(4) 若学过旧版(`resources/subscribe`订阅), chú ý phương pháp này đã thuộc thời đại đã qua đời.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lesson 07 (Building an MCP Server), Phase 13, Lesson 09 (MCP Transports) | **前置知识:** Phase 13 · 07（构建 MCP 服务器）、Phase 13 · 09（MCP 传输层）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## Mục tiêu học tập

- Chọn giữa các công cụ, tài nguyên và lời khuyên từ ý định của người tiêu dùng.
  Trung ngữ翻译: Từ người tiêu dùng意图出发, trong các công cụ、资源和提示做选择──
- Tiếp thị tài nguyên và nhanh chóng bề mặt thông qua bắt buộc `server/discover`- Tôi không biết.
  Trung ngữ翻译:通过强制的`server/discover`Khả năng thông báo và tư vấn:
- Xây dựng định nghĩa `resources/list`và `prompts/list`Kết quả.
  中文翻译: cấu构确定性的 `resources/list`和 `prompts/list`Kết quả.
- Đơn `ttlMs`và `cacheScope`Không rò rỉ dữ liệu cụ thể cho người dùng.
  Trung ngữ翻译:应用 `ttlMs`和 `cacheScope`Và không tiết lộ dữ liệu cụ thể của người dùng.
- Trả lỗi JSON-RPC `-32602`cho một URI tài nguyên không hợp lệ hoặc không được biết.
  Trung文翻译:对无效或未知的资源 URI 返回 JSON-RPC 错误 `-32602`
- Mở một `subscriptions/listen`POST- phản hồi dòng chảy và tương quan mỗi sự kiện bằng ID đăng ký.
  Trung ngữ翻译:打开 `subscriptions/listen`                                                                                                                                                                                                                                                              
- Chống lại nội dung tài nguyên và các mẫu yêu cầu như là đầu ra máy chủ không đáng tin cậy.
  Trung ngữ翻译:把资源内容和提示模板当作不可信的服务器输出──

## Bắt đầu với người tiêu dùng

> **【中文解读】**Cách đơn giản nhất để sử dụng MCP là từ việc thực hiện mã hóa: "Đây là một hàm để làm công cụ""Đây là một tài liệu để làm nguồn"― đúng là "người đang chọn, ông mong đợi gì": mô hình/ ứng dụng thực hiện các hoạt động lựa chọn công cụ; chủ sở hữu, ứng dụng hoặc người dùng đọc URI  nội dung lựa chọn nguồn; người dùng thông qua chủ sở hữu UI  khởi động các thông tin tái sử dụng 流选. Không cho một loại năng lực đồng thời tiết lộ ba loại ngôn ngữ nguyên thủy mỗi năng lực xuất hiện phải trả giá cho phát hiện, cấp quyền, lưu trữ, xử lý sai lầm, kiểm tra và tài liệu.

Cách dễ nhất để lạm dụng MCP là bắt đầu với mã thực hiện. Một truy vấn cơ sở dữ liệu trở thành một công cụ vì các chức năng quen thuộc. Một dòng công việc có thể sử dụng lại trở thành một nguồn tài nguyên vì nó được lưu trữ trong một tệp. Một lời nhắc trở thành chính sách ẩn vì máy chủ có thể tiêm nó.

> Cách đơn giản nhất của MCP là từ việc thực hiện mã nguồn điền. Việc truy vấn cơ sở dữ liệu trở thành công cụ, vì hàm làm cho người ta quen thuộc.

Bắt đầu với những người chọn và những gì họ mong đợi.

> Từ "Ai đang chọn, anh ấy mong đợi gì" bắt đầu.

| Primitive | Primary intent | Selection owner | Typical result |
|---|---|---|---|
| Tool | Perform an operation | Model or application | Structured action result |
| Resource | Read content at a URI | Host, application, or user | Text or binary content |
| Prompt | Start a reusable message workflow | User through host UI | One or more prompt messages |

Một lời nhắn ở `notes://note-1`là một nguồn tài nguyên vì nó là nội dung có thể được địa chỉ. `delete_note`là một công cụ vì nó thay đổi trạng thái. `review_note`là một lời nhắc bởi vì người dùng chọn một dòng công việc đánh giá đã chuẩn bị.

> `notes://note-1`Bài viết trên là tài nguyên, vì nó là nội dung có thể tìm kiếm.`delete_note`Đó là một công cụ, vì nó thay đổi trạng thái.`review_note`Đó là một lời khuyên, vì người dùng chọn là một quá trình kiểm tra trước.

Đừng cho thấy một hoạt động như cả ba chỉ để trông hoàn chỉnh.

> Không chỉ để hiển thị hoàn hảo, bạn nên đưa một hoạt động cùng lúc lên tiếng cho ba ngôn ngữ nguyên thủy.

>  **【类比】**Ba nguồn tài nguyên của nhà thư viện: công cụ là để vay nhân viên trên bảng  bạn yêu cầu anh ta làm việc  bạn yêu cầu anh ta làm  bạn yêu cầu anh ta thực hiện động tác  có tác dụng phụ; nguồn tài nguyên là sách trên bảng URI là số sách, chủ nhà có thể trực tiếp lấy và kèm theo vào các nội dung trên, không cần mỗi lần yêu cầu; các yêu cầu là trong nhà thư viện "hướng dẫn tự động" quy trình nhiều bước được chuẩn bị, người dùng theo một nút nhấp đầy.

## Báo thư vô quốc tịch năm 2026-07-28

> **【中文解读】**本课面向 MCP 协议修订版 2026-07-28 的无状态档位: không bắt tay đầu, không có thỏa thuận, mỗi yêu cầu được giữ lại`_meta`键自带协议版本和客户端能力── máy chủ phải được thực hiện `server/discover`, kết quả công bố hỗ trợ phiên bản, nguồn lực và năng lực gợi ý, thực hiện danh tính và lưu trữ gợi ý.`"resultType": "complete"`;不支持的修订返回 `-32022`Và đồng thời đưa ra yêu cầu sửa đổi và các sửa đổi hỗ trợ máy chủ.

Bài học này nhắm vào việc sửa đổi giao thức MCP `2026-07-28`Không có bắt tay bắt đầu hoặc phiên giao thức trong hồ sơ này. Mỗi yêu cầu mang phiên bản giao thức của nó và các khả năng của khách hàng trong lưu trữ `_meta`- Chìa khóa.

> 本课面向 MCP 协议修订版 `2026-07-28`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊`_meta`键中携带 bản giao thức riêng và khả năng khách hàng.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/list",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientInfo": {
        "name": "course-client",
        "version": "1.0.0"
      },
      "io.modelcontextprotocol/clientCapabilities": {}
    }
  }
}
```

Một máy chủ phải thực hiện `server/discover`Kết quả của nó quảng cáo được hỗ trợ
phiên bản, khả năng tài nguyên và nhanh chóng, danh tính thực hiện, và
một khách hàng có thể gọi một phương pháp khác trực tiếp, nhưng phát hiện cho nó
một ảnh chụp ổn định trước khi nó xây dựng một UI.

> 服务器 phải được thực hiện `server/discover` Kết quả công bố hỗ trợ phiên bản  nguồn lực và năng lực gợi ý  thực hiện danh tính và gợi ý lưu trữ  Khách hàng có thể trực tiếp sử dụng các phương pháp khác, nhưng phát hiện ra có thể làm cho nó có được một bức ảnh nhanh nhất trước khi xây dựng UI 

```json
{
  "resultType": "complete",
  "supportedVersions": ["2026-07-28"],
  "capabilities": {
    "resources": {"listChanged": true, "subscribe": true},
    "prompts": {"listChanged": true}
  },
  "ttlMs": 3600000,
  "cacheScope": "public"
}
```

Kết quả bình thường được công bố.`"resultType": "complete"`. Phản ứng`_meta`xác định việc thực hiện dịch vụ với `io.modelcontextprotocol/serverInfo`Thông tin này hữu ích cho chẩn đoán. Nó không phải là một danh tính xác thực. Một yêu cầu mang một sửa đổi không hỗ trợ trả lại `-32022`với cả sửa đổi yêu cầu và các sửa đổi được hỗ trợ của máy chủ.

> Thông báo kết quả thường xuyên`"resultType": "complete"`     `_meta`用 `io.modelcontextprotocol/serverInfo`标识提供服务的实现――这些信息对诊断有用,但不是认证身份――携带不支持修改请求回复 `-32022`, đồng thời đưa ra sửa đổi yêu cầu và sửa đổi hỗ trợ máy chủ.

Hợp đồng không có quốc tịch thay đổi bản năng thiết kế của bạn. Một danh sách không thể phụ thuộc vào một cuộc gọi trước đó trên một kết nối. Quyền có thể thay đổi bộ hiển thị vì các thông tin tín dụng là yêu cầu nhập, nhưng lịch sử kết nối không được.

> 无状态契约会改变你的设计直觉―― danh sách không thể phụ thuộc vào các kết nối trên cùng một kết nối.

## Các nguồn lực là hợp đồng URI ổn định .

> **【中文解读】**资源 được xác định bởi URI 标识内容先设计 URI,再写处理器──好 URI:足够稳定可收藏、按服务器域名命名空间化、独立于进程ID或连接、存储访问前先校验、每次读取都过授权──`resources/list`返回调用者当前可见的资源,按稳定键 (如 URI) 排序 确定性排序能避免缓存噪音、快照漂移和宿主 UI 跳动──`resources/read`Đối với URI không biết không trả lại "successful空读", mà là`-32602`,让客户端能区分"không tồn tại" với"bài thư trống hợp pháp"

Một nguồn tài nguyên là nội dung được xác định bởi một URI. Thiết kế URI trước khi xử lý.

> 资源 được URI 标识的内容──先设计 URI,再写处理器──

Các tính chất URI tốt:

> Bản chất của URI:

- Đủ ổn định để đánh dấu sổ hoặc chuyển giữa các yêu cầu.
  Trung ngữ翻译:足足够稳定,可收藏或在请求间传递──
- Tên không gian đến miền của máy chủ.
  Trung文翻译:按服务器域名做命名空间──
- Không phụ thuộc vào ID hoặc kết nối quá trình.
  Trung ngữ翻译:独立于进程 ID 或连接──
- Được xác minh trước khi truy cập vào kho.
  Trung ngữ翻译:在访问存储之前先校验。
- Được phép đọc mọi bài.
  Trung ngữ翻译:每次读取都做授权──

`notes://note-1`là tốt hơn `note-1`vì không gian tên của nó là rõ ràng.`file://`URI, nhưng nó vẫn phải kiểm tra ranh giới thư mục được cấu hình sau khi giải quyết các liên kết đồng nghĩa và các phân đoạn tương đối.

> `notes://note-1`优于 `note-1`, vì không gian tên của nó là rõ ràng .`file://`URI, nhưng sau khi các mã phân tích kết nối và tương đối đoạn, vẫn phải kiểm tra biên giới danh mục của cấu hình.

`resources/list`trả về các tài nguyên hiện có thể nhìn thấy cho người gọi. sắp xếp theo một phím ổn định như URI. Định nghĩa ngăn chặn bị bỏ lỡ bộ nhớ cache ồn ào, thay đổi snapshot và host UI nhảy giữa các bản cập nhật.

> `resources/list`返回调调者当前可见的资源──按稳定键如 URI)排序──确定性排序可防止杂的缓存未命中、不断变化的快照,以及跳来跳去的宿主UI──

```json
{
  "resultType": "complete",
  "resources": [
    {
      "uri": "notes://note-1",
      "name": "Architecture decision",
      "description": "Why the service uses a stateless boundary",
      "mimeType": "text/markdown"
    }
  ],
  "ttlMs": 300000,
  "cacheScope": "public",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "notes-server",
      "version": "2.0.0"
    }
  }
}
```

`resources/read`trả lại một hoặc nhiều mục nội dung. Một URI không biết không là một đọc trống thành công. Khóa tài nguyên hiện tại gán không hợp lệ hoặc không biết nguồn tài nguyên URI cho các tham số không hợp lệ JSON-RPC, mã `-32602`- Tôi không biết.

> `resources/read`返回一个或多内容项──未知 URI 不等于一次成功的空读──现行资源 规范把无效或未知资源 URI 归纳 JSON-RPC 无效参数,错码 `-32602`

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -32602,
    "message": "Unknown or invalid resource URI",
    "data": {
      "uri": "notes://missing"
    }
  }
}
```

Sự phân biệt này cho phép khách hàng tách sự vắng mặt từ một tài liệu trống hợp lệ. Nó cũng ngăn chặn sự rơi ngẫu nhiên vào một tìm kiếm rộng hơn.

> Sự khác biệt này cho phép khách hàng có thể phân chia "không tồn tại" với "bài thư trống hợp pháp". Nó cũng ngăn chặn sự không ngờ quay lại tìm kiếm rộng hơn.

### Các mẫu tài nguyên

> **【中文解读】**资源模板 mô tả một bộ URI được phân loại, phù hợp với trường hợp "để liệt kê từng mục cụ thể có giá cao hoặc không giới hạn". 模板不放松校验:解析变量、过授权、限长度和字符集、使用类型化参数构建存储查询绝不把任意 URI 尾巴拼进文件路径或数据库语句──

Một mẫu tài nguyên mô tả một gia đình các URI được tham số. Sử dụng một khi liệt kê mọi mục cụ thể sẽ tốn kém hoặc không giới hạn. Ví dụ: `notes://projects/{project}/decisions/{decision}`cho khách hàng biết cách tạo ra một địa chỉ hợp lệ mà không trả lại mọi quyết định.

> 资源模板 mô tả URI phân tích một bộ 族.`notes://projects/{project}/decisions/{decision}`Nói cho khách hàng biết làm thế nào để xây dựng địa chỉ hợp pháp, không cần phải trả lại từng quyết định.

Một mẫu không làm suy yếu xác thực. Phân tích các biến, áp dụng quyền, thực thi giới hạn chiều dài và ký tự, và xây dựng các truy vấn lưu trữ với các tham số được gõ. Không bao giờ kết nối một đuôi URI tùy ý vào một con đường hệ thống tập tin hoặc tuyên bố cơ sở dữ liệu.

> 模板 sẽ không làm cho việc thử nghiệm dễ dàng hơn. 模板 sẽ giải quyết biến số, ứng dụng quyền hạn, hạn chế độ dài và ký tự, và sử dụng các kiểu hóa các yếu tố xây dựng truy vấn lưu trữ.

### Nội dung không phải là hướng dẫn đáng tin cậy

> ️ **【易错点】**场景:把资源文真正指令执行,或让 prompt 成为绕过资源授权的旁路 / 后果:资源文本可能含提示注入、秘密、误导性命令或形标记;未授权的字段泄漏给调用者 / 修复: chủ nhà lưu trữ lưu trữ thông tin và đưa nội dung tài nguyên thành dữ liệu;服务器限制内容大小、返回准确的MIME 类型、脱敏调用者无权访问的字段、不返回无关记录; URI 参数的快速阅读与直接资源相同授权检查.

Các tài liệu có thể chứa các lệnh hư cấu, sai lệch hoặc đánh dấu sai. Người chủ nên bảo tồn nguồn gốc và coi nội dung tài nguyên như dữ liệu.

> 资源文本可能包含提示注入、秘密、误导性命令或形标记── chủ nhà nên giữ lại thông tin và xem tài nguyên nội dung như dữ liệu──服务器应限制内容大小、返回准确的MIME类型、脱敏调用者无权访问的字段,并避免返回无关记录──

## Các lời khuyên là mẫu được người dùng kiểm soát.

> **【中文解读】**MCP yêu cầu 面向显式的用户选择: chủ nhà có thể 染 thành斜命令、菜单项或工作流按,协议不限制 UI。`prompts/list`Các yêu cầu được cấp quyền phải giữ sự xác định; mỗi gợi ý phải có một tên cố định, mô tả hữu ích và tuyên bố tham số, để chủ nhà ở.`prompts/get`之前收集输入──`prompts/get`Đặt các tham số phân tích thành tin nhắn, nhưng không thay thế các lệnh hệ thống của chủ chủ, chủ quyết định trả lại tin nhắn như thế nào để vào mô hình dưới đây, và để cho chiến lược đáng tin cậy của mình duy trì ưu tiên cao hơn.

Các lệnh MCP được thiết kế để lựa chọn rõ ràng của người dùng. Một máy chủ có thể render chúng như lệnh slash, mục menu hoặc nút workflow.

> MCP yêu cầu để thiết kế cho sự lựa chọn của người dùng rõ ràng. Người chủ có thể biến chúng thành các lệnh ngơng, đơn hàng hoặc dòng công việc.

`prompts/list`mỗi prompt cần một tên ổn định, mô tả hữu ích và tuyên bố lập luận để cho phép chủ sở hữu thu thập đầu vào trước `prompts/get`- Tôi không biết.

> `prompts/list`Các yêu cầu được cấp quyền phải giữ chắc chắn. Mỗi gợi ý cần một tên cố định, mô tả hữu ích và tuyên bố tham số, để chủ nhà có thể ở.`prompts/get`之前收集输入──

```json
{
  "resultType": "complete",
  "prompts": [
    {
      "name": "review_note",
      "title": "Review a note",
      "description": "Review one note for a named concern",
      "arguments": [
        {
          "name": "uri",
          "description": "The note resource URI",
          "required": true
        }
      ]
    }
  ],
  "ttlMs": 600000,
  "cacheScope": "public"
}
```

`prompts/get`giải quyết các lập luận thành tin nhắn. Nó không thay thế các hướng dẫn hệ thống của máy chủ. máy chủ quyết định cách các tin nhắn trả lại vào bối cảnh mô hình và giữ chính sách tin cậy của riêng mình ở ưu tiên cao hơn.

> `prompts/get`Đặt các tham số phân tích thành thông điệp. Nó không thay thế các chỉ thị hệ thống của chủ chủ. Chủ nhà quyết định thông điệp trả lại vào mô hình như thế nào, và để các chiến lược đáng tin cậy của mình giữ được ưu tiên cao hơn.

Thiết lập các lập luận prompt tại biên giới máy chủ. URI prompt phải vượt qua kiểm tra ủy quyền tương tự như đọc tài nguyên trực tiếp. Đừng làm cho một prompt là kênh bên xung quanh truy cập tài nguyên.

> Trong các dịch vụ biên giới của các trường học, URI nên thông qua cùng một quyền kiểm tra với trực tiếp tài nguyên.

## Các gợi ý trong bộ nhớ là một phần của sự chính xác.

> **【中文解读】** `ttlMs`告诉客户端结果可复用长时间,`cacheScope`描述 ai có thể chia sẻ giá trị lưu trữ. MCP chỉ được định nghĩa.`public`和 `private`两种 `cacheScope`; mang theo bí mật hoặc kết quả thay đổi nhanh chóng`private`+ `ttlMs: 0`, nghiêm ngặt hơn không có cửa hàng quy tắc bởi chủ nhà quản lý quản lý`no-store`Không phải MCP của `cacheScope`值──缓存提示永远不能取代授权:缓存键必须包含所有可见性的变化请求维度(租户、用户、范围、语言、分页游标); chia sẻ缓存表达不了这些维度,就用`private`+ 零 TTL + 宿主级 không có cửa hàng.

`ttlMs`cho khách hàng biết kết quả có thể được sử dụng lại bao lâu. `cacheScope`mô tả những người có thể chia sẻ giá trị được lưu trữ.

> `ttlMs`Nói cho khách hàng một kết quả có thể được sử dụng lại lâu.`cacheScope`Mô tả ai có thể chia sẻ giá trị lưu trữ này.

| Scope | Meaning | Typical use |
|---|---|---|
| `public` | May be reused across users when authorization permits | Public prompt catalog |
| `private` | Bound to the requesting user or credential context | User-owned note content |

Chọn TTL từ tốc độ thay đổi dữ liệu và thiệt hại của sự trì hoãn. Năm phút có thể phù hợp với một danh mục thư viện công cộng.

> Theo dữ liệu tốc độ thay đổi và giá cả qua thời gian chọn TTL。

MCP chỉ định nghĩa `public`và `private`như `cacheScope`Giá trị. Đối với một kết quả bí mật hoặc thay đổi nhanh chóng, trả lại `cacheScope: "private"`với `ttlMs: 0`, sau đó áp dụng bất kỳ quy tắc không lưu trữ nghiêm ngặt hơn trong chính sách cache chủ. `no-store`bản thân nó không phải là một MCP `cacheScope`giá trị.

> MCP chỉ định `public`和 `private`作为 `cacheScope`△ giá trị đối với kết quả của sự thay đổi nhanh chóng, trả lại `cacheScope: "private"`加 `ttlMs: 0`, sau đó áp dụng bất kỳ quy tắc không- cửa hàng nghiêm ngặt hơn trong chiến lược lưu trữ chủ nhà.`no-store`本身不是MCP的`cacheScope`Giá trị:

Các gợi ý cache không bao giờ thay thế quyền phép. Một khóa cache phải bao gồm mọi chiều kích yêu cầu thay đổi khả năng hiển thị, bao gồm người thuê nhà, người dùng, phạm vi, địa điểm và trình chiếu trang. Nếu một bộ nhớ cache được chia sẻ không thể thể diễn tả các chiều kích đó một cách an toàn, hãy sử dụng `private`với một TTL không và một chính sách không cửa hàng ở cấp chủ.

> 缓存提示永远不能取代授权──缓存键 phải chứa mọi thay đổi có thể nhìn thấy được yêu cầu kích thước, bao gồm thuê户, người dùng, phạm vi, ngôn ngữ và phân trang游标── nếu chia sẻ缓存 không thể thể thể hiện an toàn các kích thước này, hãy sử dụng `private`加零 TTL 和宿主级无店 策略──

## Đăng ký Sử dụng dòng phản hồi mở của khách hàng .

> **【中文解读】**现代订阅模式取代了旧的 现代订阅模式取代了旧的`resources/subscribe`RPC và cũ của HTTP GET 事件端点──客户端把 `subscriptions/listen`作为普通 JSON-RPC 请求发发出; 在 Streamable HTTP 上,这是一个 POST,其响应保持打开成为SSE流──`notifications`Đối tượng là cho phép thanh toán  máy chủ phải gửi loại thông báo không được yêu cầu  yêu cầu ID là đăng ký ID; trước bất kỳ sự kiện được yêu cầu, máy chủ trước tiên phát`notifications/subscriptions/acknowledged`, các bộ lọc chỉ chứa các phần của máy chủ chấp nhận; trên dòng chảy tiếp theo mỗi sự kiện đều mang theo cùng một .`subscriptionId`元データ──通知 chỉ nói" tài nguyên đã thay đổi", khách hàng phải thông qua `resources/read`重新读取并重新过当前授权不要假设事件里带带带带带新文档──不要把订阅流当协议会话使用:后续读取仍可落至任意健康例的完整请求──

Mô hình đăng ký hiện đại thay thế cho mô hình trước `resources/subscribe`RPC và điểm cuối của sự kiện HTTP GET cũ.

> 现代订阅模式取代了前者 `resources/subscribe`RPC 和旧的HTTP GET 事件端点──

Khách hàng gửi `subscriptions/listen`Over Streamable HTTP đây là một POST mà phản ứng vẫn mở như một dòng SSE.`notifications`object là một permislist. Một máy chủ không được cung cấp các loại thông báo mà không được yêu cầu.

> 客户端把 `subscriptions/listen`作为普通 JSON-RPC 请求发送──在 Streamable HTTP 上,这是一个 POST,其响应保持开放成为SSE流──`notifications`Đối tượng là cho phép thanh toán.

```json
{
  "jsonrpc": "2.0",
  "id": 17,
  "method": "subscriptions/listen",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "course-client",
        "version": "1.0.0"
      }
    },
    "notifications": {
      "resourcesListChanged": true,
      "promptsListChanged": true,
      "resourceSubscriptions": [
        "notes://note-1"
      ]
    }
  }
}
```

ID yêu cầu là ID đăng ký. Trước bất kỳ sự kiện yêu cầu nào, máy chủ gửi `notifications/subscriptions/acknowledged`Bộ lọc của nó chỉ chứa các bộ phận mà máy chủ chấp nhận.

> Đơn xin ID là đăng ký ID. Trước khi bất kỳ sự kiện được yêu cầu, máy chủ gửi `notifications/subscriptions/acknowledged`其过器只包含服务器接受的子集──

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/subscriptions/acknowledged",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/subscriptionId": 17
    },
    "notifications": {
      "resourcesListChanged": true,
      "resourceSubscriptions": [
        "notes://note-1"
      ]
    }
  }
}
```

Mỗi sự kiện sau đó trên dòng đó đều mang cùng một metadata.

> Mỗi sự kiện tiếp theo trên dòng này đều mang cùng một số dữ liệu.

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/subscriptionId": 17
    },
    "uri": "notes://note-1"
  }
}
```

Thông báo nói nguồn đã thay đổi. Khách hàng đọc lại thông qua `resources/read`, theo phép hiện tại. Nó không giả định sự kiện có chứa tài liệu mới.

> 通知 nói là " tài nguyên đã biến đổi "...... khách hàng thông qua `resources/read`重新读取,并接受当前授权的约束──它不假设事件里包含新文档──

Một số thuê bao có thể chia sẻ một kênh stdio. ID thuê bao cho phép khách hàng làm mất nhiều. Trên HTTP, đóng dòng phản hồi hủy đăng ký. Một máy chủ kết thúc dòng chảy trả lại một kết thúc `resultType: "complete"`phản ứng tương quan với yêu cầu ban đầu.

> Nhiều người đăng ký có thể chia sẻ một bài viết trên một kênh. Thư ký nhận dạng để khách hàng có thể phân phối chúng. Trên HTTP, kết thúc dòng phản ứng tức là hủy bỏ đăng ký.`resultType: "complete"`响应.

Không sử dụng dòng đăng ký như một phiên giao thức. Một đọc sau đó vẫn là một yêu cầu hoàn chỉnh có thể đạt đến bất kỳ phiên bản máy chủ lành mạnh nào.

> Đừng dùng dòng đăng ký khi giao ước được sử dụng.

```figure
t3-primitive-sort
```

## - Interactive Lab - Thực hành tương tác

Sử dụng hình ảnh để phân loại năm khả năng từ trình theo dõi dự án: chi tiết vấn đề, tạo vấn đề, mẫu đánh giá sprint, chính sách dự án và vấn đề đóng. Sau đó quyết định danh sách nào có thể được lưu trữ trong cache công khai, những gì đọc phải giữ riêng tư, và các tài nguyên nào xứng đáng được cập nhật thông báo.

> Sử dụng mô hình cho các bộ theo dõi dự án 5 khả năng phân loại: vấn đề chi tiết, tạo vấn đề, 代 đánh giá mô hình, chính sách dự án, đóng vấn đề, sau đó quyết định những danh sách có thể mở để lưu trữ, những bài đọc phải giữ riêng tư, những tài nguyên có giá trị được cập nhật thông báo.

Đối với mỗi phân loại, hãy đặt tên cho người chọn. Nếu mô hình thực hiện một hành động, hãy sử dụng một công cụ. Nếu một máy chủ đọc nội dung được địa chỉ URI, hãy sử dụng một nguồn lực. Nếu người dùng bắt đầu một dòng công việc tin nhắn đã chuẩn bị, hãy sử dụng một lời nhắc.

> Đối với mỗi phân loại, nói lên "Who is choosing"―― mô hình thực hiện động tác dụng dụng; chủ sở hữu đọc URI 寻址 của nội dung sử dụng tài nguyên; người dùng khởi động dự kiến tạo thông tin.

## Thực hành phòng thí nghiệm thực hành thực hành

> **【中文解读】**按给定顺序检查转录: phát hiện thông báo hiện tại sửa đổi và hai loại năng lực; hai danh sách kết quả có thứ tự và`resultType: "complete"`; danh sách và kết quả đọc với cài đặt dự định;把读取 URI 改成 `notes://missing`观察 `-32602`; đăng ký xác nhận trước đến tài nguyên sự kiện; sự kiện với优雅关闭都携带 đăng ký ID 5。 chú ý:Python 模型不开真实HTTP 连接, nó trình bày là SDK 必须放到请求级响应流上的消息;生产环境使用官方 SDK做组和传输。

Tiến bộ mô phỏng từ gốc kho:

```bash
cd phases/13-tools-and-protocols/10-mcp-resources-and-prompts/code
python3 main.py
python3 -m unittest discover tests -v
```

Kiểm tra bản sao theo thứ tự này:

1. Đảm bảo `server/discover`quảng cáo về việc sửa đổi hiện tại và cả hai khả năng.
   中文翻译: xác nhận `server/discover`Thông báo hiện tại sửa đổi và hai khả năng.
2. Hãy xác nhận cả hai kết quả danh sách được sắp xếp và sử dụng `resultType: "complete"`- Tôi không biết.
   Trung文翻译: xác nhận hai danh sách kết quả có序且使用 `resultType: "complete"`
3. Đảm nhận danh sách và đọc kết quả có ý định cache gợi ý.
   Trung ngữ翻译: xác nhận danh sách và kết quả đọc kèm theo có cố định đặt của缓存提示。
4. Thay đổi URI đọc thành `notes://missing`và quan sát`-32602`- Tôi không biết.
   Trung文翻译:把读取 URI 改成 `notes://missing`, quan sát`-32602`
5. Xác nhận đăng ký trước sự kiện tài nguyên.
   Trung ngữ翻译:确认订阅确认先于资源事件──
6. Báo cáo xác nhận sự kiện và kết thúc lịch sự cả hai mang thẻ đăng ký `5`- Tôi không biết.
   Trung文翻译: xác nhận事件与优雅关闭都携带订阅 ID `5`

Mô hình Python không mở kết nối HTTP thực sự. Nó đại diện cho các thông điệp mà một SDK phải đặt trên dòng phản ứng có quy mô yêu cầu. Sử dụng một SDK chính thức để khung và vận chuyển trong sản xuất.

> Python 模型不开真实的HTTP 连接──它 trình bày là SDK  phải được đặt vào các thông tin trên dòng đáp ứng yêu cầu── trong môi trường sản xuất sử dụng SDK chính thức để thực hiện组和传输──

## Thuật vật được vận chuyển.

`outputs/skill-primitive-splitter.md`là một bản xem xét thiết kế có thể sử dụng lại cho lựa chọn nguyên thủy MCP. Nó hiện đang kiểm tra khám phá xác định, phạm vi cache, hành vi URI không hợp lệ và bộ lọc đăng ký hiện đại.

> `outputs/skill-primitive-splitter.md`Đây là một MCP có thể sử dụng được.

Bài học cũng đi theo `assets/primitive-split.svg`, một phiên bản tĩnh của ranh giới nguyên thủy và đăng ký cho nghiên cứu ngoại tuyến.

> 本课还附带 `assets/primitive-split.svg`, là phiên bản tĩnh của bản gốc và biên giới đăng ký, để học trực tuyến.

## Hãy kiểm tra.

```bash
cd phases/13-tools-and-protocols/10-mcp-resources-and-prompts/code
python3 main.py
python3 -m unittest discover tests -v
```

Kết quả mong đợi: chương trình chính in một bản sao JSON và lệnh kiểm tra báo cáo ít nhất mười hai bài kiểm tra vượt qua.

> Kết quả dự kiến: Chương trình chủ in một bản ghi JSON, lệnh kiểm tra báo cáo ít nhất 12 bài kiểm tra đã qua.

## Kết nối Capstone.

Sử dụng hợp đồng này khi máy chủ đầu đá của bạn cho thấy kiến thức có thể địa chỉ bên cạnh các hành động. Bao gồm một bản chụp ảnh danh mục xác định, một tài nguyên được phép đọc, một giải pháp nhanh chóng, một trường hợp URI không hợp lệ và một bản sao đăng ký.

> Khi máy chủ dự án tốt nghiệp của bạn được phát hiện ngoài động tác, sử dụng bản hợp đồng này.

Bằng chứng của bạn nên cho thấy rằng không có danh sách nào phụ thuộc vào lịch sử kết nối và rằng một sự kiện đăng ký không bao giờ cho phép truy cập vào tài nguyên cơ bản.

> Bằng chứng của bạn cho thấy: không có bất kỳ danh sách nào phụ thuộc vào lịch sử liên kết, và các sự kiện đăng ký không bao giờ cho phép truy cập vào các nguồn lực cấp dưới.

## Tập luyện bài tập

1. Thêm một `notes://projects/{project}/notes/{id}`mẫu tài nguyên và xác nhận cả hai biến.
   Trung ngữ翻译:添加 `notes://projects/{project}/notes/{id}`资源模板并校验两个变量──
2. Thêm trang vào `resources/list`trong khi vẫn giữ được trật tự quyết định.
   Trung ngữ翻译:给 `resources/list`加分页, đồng thời giữ định nghĩa
3. Thay đổi một tài nguyên thành `cacheScope: "private"`với `ttlMs: 0`, thêm một chính sách không cửa hàng ở cấp chủ, và giải thích mối đe dọa biện minh cho cả hai kiểm soát.
   Trung文翻译:把一个资源改为 `cacheScope: "private"`加 `ttlMs: 0`, thêm chủ sở hữu cấp không cửa hàng 策略,并 giải thích đồng thời cần hai điều khiển mô hình đe dọa.
4. Thêm đăng ký thay đổi danh sách nhắc và chứng minh không có sự kiện nào được gửi khi bộ lọc bỏ qua `promptsListChanged`- Tôi không biết.
   Trung文翻译:添加提示列表变更订阅,并证明过器省略 `promptsListChanged`时不发送事件──
5. Tạo hai đăng ký đồng thời và chứng minh mỗi sự kiện có ID yêu cầu chính xác.
   Trung ngữ翻译: tạo ra hai đăng ký tồn tại cùng lúc, chứng minh mỗi sự kiện mang theo ID yêu cầu chính xác.
6. Thêm một quyền đối tượng vào trình xử lý đọc và chứng minh một mục cache không thể vượt qua đối tượng.
   Đọc thêm:                                                                                                                                                                                                                                                             

## Từ khóa  Từ khóa nhanh chóng

- **Resource:**Nội dung được định hướng URI được phát hiện bởi máy chủ MCP.
  Trung文翻译:资源MCP 服务器暴露的 URI 寻址内容──
- **Prompt:**Một mẫu thông điệp được người dùng kiểm soát được một máy chủ MCP phát hiện.
  Trung ngữ翻译:提示MCP 服务器暴露的用户控制消息模板──
- **Deterministic list:**Kết quả phát hiện với thành viên ổn định và đặt hàng cho các đầu vào yêu cầu tương tự.
  Trung ngữ翻译:确定性列表对相同请求输入具有稳定成员和排序的发现结果──
- **`ttlMs`:**Cache thời gian tươi mới trong milliseconds.
  Trung ngữ翻译:缓存新鲜期,单位毫秒──
- **`cacheScope`:**Biên giới chia sẻ cho một kết quả được lưu trữ trong cache.
  Trung ngữ翻译:缓存结果的共享边界──
- **`subscriptions/listen`:**Một yêu cầu lâu dài mà dòng phản hồi của nó cung cấp các thông báo được lọc rõ ràng.
  Trung ngữ翻译:长生命周期请求,其响应流投递经过显式过的通知──
- **Subscription ID:**ID yêu cầu nghe ban đầu, lặp lại trong các metadata thông báo.
  Trung ngữ翻译:订阅 ID原始听 请求 ID, 在通知元数据中重复出现──
- **Invalid parameters:**lỗi JSON-RPC `-32602`, được sử dụng cho một URI tài nguyên không hợp lệ hoặc không được biết đến.
  中文翻译:无效参数JSON-RPC 错误 `-32602`, dùng cho các nguồn URI vô hiệu hoặc không được biết đến.
- **Unsupported protocol version:**lỗi JSON-RPC `-32022`, bao gồm `supported`và `requested`Các sửa đổi.
  中文翻译:不支持的协议版本JSON-RPC 错误 `-32022`, bao gồm`supported`和 `requested`修订。
- **`server/discover`:**Phương pháp máy chủ bắt buộc trả lại các sửa đổi, khả năng, danh tính và gợi ý cache tùy chọn được hỗ trợ.
  Trung ngữ翻译: pháp luật của máy chủ, trả lại hỗ trợ sửa đổi, khả năng, danh tính và có thể chọn 缓存提示.

## Xem thêm 延伸阅读

- [MCP 2026-07-28 Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
  Trung ngữ翻译:资源契约的权威规范(列表、读取、模板、`-32602`语义)
- [MCP 2026-07-28 Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)
  Trung ngữ翻译:提示契约的权威规范
- [MCP 2026-07-28 Subscriptions](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions)
  Trung ngữ翻译:`subscriptions/listen`订阅模式规范
- [MCP 2026-07-28 Caching](https://modelcontextprotocol.io/specification/2026-07-28/basic/utilities/caching)
  Trung ngữ翻译:`ttlMs`- Không.`cacheScope`缓存提示语义
