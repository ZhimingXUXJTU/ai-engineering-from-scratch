# MCP Thể hiện: Công việc bền vững trên một lõi không quốc tịch  MCP Thể hiện: nhiệm vụ không trạng thái nội nhân

> MCP không có quốc tịch không có nghĩa là mọi hoạt động phải hoàn thành trong một yêu cầu.`tools/call`, bất cứ trường hợp nào có thể trả lời.`tasks/get`, và thông tin của khách hàng đến qua `tasks/update`Không làm lại các phiên giao thức.

> **【中文解读】**MCP không bằng với mỗi hoạt động phải được hoàn thành trong một yêu cầu.`tools/call`返回句柄, bất cứ trường hợp nào đều có thể ứng phó `tasks/get`, khách hàng nhập thông qua `tasks/update`送达全程不需要复活协议会话──注意本课已完全改版:Tác vụ từ 2025-11-25 的实验性核心特性(SEP-1686) 迁移为官方 `io.modelcontextprotocol/tasks`扩展, phương pháp面也换了`tasks/status``tasks/result``tasks/list`已移除)

> **【拓展：持久化任务→Agent 长时运行工作】**异步任务是MCP 处理长时间运行工作的标准模式:深度研究、代码生成、批量导出 这类需要几分钟到几小时的工作──与传统同步`tools/call`Không giống như,Tác vụ 让服务器先持久化再返回任务Id,客户端稍后轮询快照或订阅通知. Đây là bước quan trọng của MCP từ " đơn giản công cụ thực hiện " tiến triển đến " phức tạp của quy trình sắp xếp " , với " giao dịch 确认 消费 " của dòng tin tức.

>  **【前置】**学本节前请先掌握:(1) Bước 13·09(transport)Streamable HTTP 的 POST/SSE 形态,本课的 `Mcp-Method`- Không.`Mcp-Name`头直接建立在它;(2) giai đoạn 13·11(MRT không có quốc gia) 无会话重试与 `inputRequests`- Không.`inputResponses`机械;(3) Bước 13·12(elicitation)  nhiệm vụ thực hiện trong thu thập người dùng nhập vào sử dụng là cùng một bộ biểu tượng đơn sơ。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 09 (transports), Phase 13 · 11 (stateless MRTR), Phase 13 · 12 (elicitation) | **前置知识:** Phase 13 · 09（transports）、Phase 13 · 11（无状态 MRTR）、Phase 13 · 12（elicitation）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## Mục tiêu học tập

- Sự khác biệt giữa giao thông giao thức không có quốc gia và trạng thái nhiệm vụ ứng dụng bền.
  Trung ngữ翻译:区分无状态的协议传输与持久化应用任务状态──
- Thỏa thuận`io.modelcontextprotocol/tasks`mở rộng khả năng theo yêu cầu và`server/discover`- Tôi không biết.
  Trung ngữ翻译:在按请求能力与 `server/discover`中协商 `io.modelcontextprotocol/tasks`扩展──
- Trả lại một máy chủ hướng `CreateTaskResult`với `resultType: "task"`Chỉ sau khi tạo ra một sự tồn tại lâu dài.
  Trung ngữ翻译: Chỉ sau khi xây dựng được hoàn thành,才回带`resultType: "task"`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `CreateTaskResult`
- Cuộc thăm dò với `tasks/get`, hoàn thành các nhiệm vụ nhập với `tasks/update`, và yêu cầu hủy hợp tác với `tasks/cancel`- Tôi không biết.
  中文翻译:用 `tasks/get`轮询 `tasks/update`补充任务输入、用 `tasks/cancel`Xin hãy cùng làm việc.
- Tắt ra người lớn tuổi `tasks/status`- `tasks/result`, và`tasks/list`những giả định.
  Trung ngữ翻译:清除旧版 `tasks/status``tasks/result`和 `tasks/list`Ước tính:
- Đăng ký thông báo nhiệm vụ tùy chọn qua `subscriptions/listen`trên một dòng SSE trả lời POST.
  中文翻译:通过 POST 响应 SSE 流上的 `subscriptions/listen`订阅可选的任务通知──
- Mô hình nhiệm vụ hết hạn, khởi động lại phục hồi, sao chép sao chép khóa đầu vào và lỗi thực hiện đúng.
  Trung文翻译:正确建模任务过期、重启恢复、输入键去重和执行错误──

## Tại sao nhiệm vụ là một phần mở rộng

> **【中文解读】**Nhiệm vụ ban đầu là tính năng cơ bản thực nghiệm của 2025-11-25 (trước đó được gọi là SEP-1686  nhiệm vụ tăng cường) ⋅`io.modelcontextprotocol/tasks`扩展客户端和服务器按需选择加入这个套额外生命周期,而不是让所有人为核心协议买单. 扩展规范目前仍在草案表面:锁定SDK 支持扩展版本、跑一致场景、把线上适配器与工作器和存储领域隔离──

Nhiệm vụ lần đầu tiên xuất hiện như một tính năng cốt lõi thử nghiệm trong năm 2025-11-25.`io.modelcontextprotocol/tasks`mở rộng để khách hàng và máy chủ có thể chọn vào vòng đời bổ sung mà không mở rộng giao thức cốt lõi cho tất cả mọi người.

> Các nhiệm vụ ban đầu là tính năng cơ bản thử nghiệm xuất hiện vào năm 2025-11-25.`io.modelcontextprotocol/tasks` mở rộng, cho phép khách hàng và máy chủ có thể chọn tham gia vào vòng đời bổ sung này theo yêu cầu, mà không cần phải mở rộng các giao dịch cốt lõi cho tất cả mọi người.

Các đặc điểm mở rộng vẫn là một bề mặt sơ đồ mặc dù nó là nhà chính thức hiện tại cho các nhiệm vụ. Pin phiên bản mở rộng được hỗ trợ bởi SDK của bạn, chạy kịch bản phù hợp, và cô lập bộ chuyển đổi dây từ nhân viên và miền lưu trữ của bạn.

> 扩展规范 hiện vẫn là bề mặt dự thảo, mặc dù nó đã là nhiệm vụ hiện tại của chính thức.

Sử dụng một nhiệm vụ khi hoạt động có một hoặc nhiều tính chất sau đây:

> Khi hoạt động có một hoặc nhiều thuộc tính sau đây khi sử dụng nhiệm vụ:

- Nó có thể tồn tại lâu hơn một thời gian yêu cầu bình thường.
  Trung ngữ翻译:它可能超越普通请求的超时时间──
- Một hàng lao động hoặc hệ thống việc làm bên ngoài đã sở hữu hành động.
  Trung ngữ翻译:某个工作队列或外部作业系统已经拥有执行权──
- Khách hàng cần phải phục hồi sau khi khởi động lại.
  Trung ngữ翻译:客户端需要在自己的重启后恢复.
- Hành động dừng lại cho người dùng hoặc mô hình nhập trong quá trình thực hiện.
  Trung ngữ翻译:操作在执行中会暂停等待用户或模型输入──
- Việc hủy bỏ và thu hồi kết quả lâu dài là yêu cầu sản phẩm.
  Trung ngữ翻译:取消和持久化结果获取是产品需求──

Đừng tạo ra một nhiệm vụ cho một tìm kiếm quyết định giá rẻ.

> Đừng tìm kiếm nhiệm vụ xây dựng vì sự chắc chắn rẻ tiền.

## Core không quốc tịch, ứng dụng có quốc tịch.

> **【中文解读】**Đây là khái niệm của bài học: MCP 2026-07-28  Dỡ bỏ `initialize``notifications/initialized`、 thỏa thuận sẽ được thảo luận và `Mcp-Session-Id` Nhưng điều này không cấm có trạng thái sản phẩm.  nhiệm vụ id là một trạng thái ứng dụng rõ ràng: trước được duy trì tái trả lại; khách hàng có thể tồn tại  tái khởi động sau được hỏi lại;  có thể được chuyển đến bất kỳ bản sao nào sau cùng một lưu trữ duy trì; mỗi lần phương pháp nhiệm vụ调用 đều được thực hiện lại kiểm tra ủy quyền; hết hạn và xóa được xác định bởi các đoạn nhiệm vụ, chứ không phải chuyển giao vòng đời. 

MCP 2026-07-28 được gỡ bỏ `initialize`- `notifications/initialized`, các phiên giao thức, và`Mcp-Session-Id`Điều đó không cấm các sản phẩm có nội dung.

> MCP 2026-07-28 移除了 `initialize``notifications/initialized`、 thỏa thuận sẽ được thảo luận và `Mcp-Session-Id` Không cấm có sản phẩm có trạng thái

Một task id là trạng thái ứng dụng rõ ràng:

> 任务 id là trạng thái ứng dụng rõ ràng:

- Máy chủ vẫn cố gắng để trả lại nó.
  Trung ngữ翻译:服务器先持久化它再返回──
- Khách hàng có thể lưu trữ nó và thăm dò lại sau khi khởi động lại.
  Trung ngữ翻译:客户端可以存储它,重启后再次轮询──
- Thẻ nhận dạng có thể chuyển đến bất kỳ bản sao nào được hỗ trợ bởi cùng một cửa hàng bền.
  Trung ngữ翻译:该 id có thể được chuyển đến bất kỳ bản sao nào của cùng một kho lưu trữ lâu dài.
- Quyền được kiểm tra trên mỗi phương pháp nhiệm vụ.
  Trung ngữ翻译:每次任务方法调用都检查授权──
- Thời hạn và xóa được xác định bởi các lĩnh vực nhiệm vụ, không phải là thời gian vận chuyển.
  Trung ngữ翻译:过期与删除由任务字段定义,而不是传输生命周期──

Điều này khác với trạng thái ẩn gắn với một kết nối.

> Điều này khác với trạng thái ẩn trên kết nối.

Hãy giữ bốn đời riêng biệt:

> Cứ chia 4 vòng đời:

| State | Lifetime | Where it belongs |
|---|---|---|
| Protocol metadata | One request | `params._meta`, validated again on every call |
| Transport work | One stdio request or HTTP response | In-flight coordinator with a bounded deadline |
| MRTR continuation | One retry sequence | Integrity-protected `requestState`, plus replay controls when needed |
| Durable task | Across requests, replicas, restarts, and reconnects | Shared application store keyed by an authorized `taskId` |

> 表格对照(zh 版):协议元数据单个请求`params._meta`, mỗi lần调用都重试;传输工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作单个工作`requestState`, cần thời gian tăng cường kiểm soát; duy trì nhiệm vụ qua yêu cầu, phụ bản, khởi động lại và tái nối để ủy quyền`taskId`Để lưu trữ ứng dụng chia sẻ quan trọng.

Di chuyển một hồ sơ nhiệm vụ vào bộ nhớ quá trình không làm cho MCP trạng thái. Nó làm cho ứng dụng không đáng tin cậy.`tasks/get`Đăng thẳng trước khi trả lại tay cầm, sau đó làm cho mỗi phương pháp nhiệm vụ giải quyết cùng một bản ghi chia sẻ dưới kiểm tra người thuê và chủ.

> Đặt ghi tác vụ vào bộ nhớ quá trình sẽ không làm cho MCP biến thành trạng thái, chỉ làm cho ứng dụng không thể tin cậy.`tasks/get`Không thể khôi phục lại bản ghi này. Trước tiên, hãy giữ lại và trả lại câu, sau đó để mỗi phương pháp nhiệm vụ phân tích cùng một bản ghi chung dưới sự kiểm tra của người thuê và chủ sở hữu.

>  **【类比】**任务像餐厅的取餐号,但换成了"连锁店通"模式:你在 A 店点餐(工具/调用),小票上是取餐号 42(任务Id) 它存在连锁总部的订单系统(持久存储) 里,不是某店员的脑子里 (内存) 里 (内存) 里. Bạn có thể đến bất kỳ分店 nào để hỏi"42号好了吗" (tác vụ/tác vụ) 路由到任意副本); 中店员工 hỏi bạn không cần thêm (输入_required), bạn trả lời một câu  (tác vụ/更新); không muốn quay lại theo thời gian với các đơn nhiệm vụ/tác vụ)  (旧的"柜台"就是同步调用等等等等;旧的"SEP-1686 站员工反喊员工" () 协议   没有你一直可以回来新话.

## Khả năng đàm phán Khả năng đàm phán

Khách hàng quảng cáo hỗ trợ cho mỗi yêu cầu đủ điều kiện:

> 客户端 trong mỗi yêu cầu đáp ứng yêu cầu tuyên bố hỗ trợ:

```json
{
  "_meta": {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientCapabilities": {
      "extensions": {
        "io.modelcontextprotocol/tasks": {}
      }
    },
    "io.modelcontextprotocol/clientInfo": {
      "name": "lesson-client",
      "version": "1.0.0"
    }
  }
}
```

Server trả lại chính xác `supportedVersions`, khả năng,`ttlMs`, và`cacheScope`từ `server/discover`, với cùng một mở rộng trong khả năng.`tools/list`Kết quả đó trả lại một số lượng xác định`generate_report`mô tả, đối tượng hợp lệ `inputSchema`- `resultType: "complete"`, dữ liệu siêu dạng máy chủ, và gợi ý cache công cộng.

> 服务器 từ `server/discover`返回精确的   trả lại`supportedVersions`、 khả năng`ttlMs`和 `cacheScope`, khả năng dưới cùng một mở rộng. Vì nó tuyên bố công cụ, do đó cũng thực hiện bắt buộc.`tools/list` Kết quả trở lại xác định`generate_report`描述符、合法的 đối tượng `inputSchema``resultType: "complete"`、 dữ liệu và lưu trữ công khai của máy chủ

Một phương pháp nhiệm vụ từ một khách hàng không báo cáo các khoản mở rộng trả lại `-32021`, Không có khả năng khách hàng cần thiết, với `data.requiredCapabilities`được thiết lập`{"extensions":{"io.modelcontextprotocol/tasks":{}}}`. Một chuỗi giao thức không được hỗ trợ trả về`-32022`chính xác`supported`và `requested`dữ liệu; một phiên bản bị mất hoặc không có chuỗi trả lại `-32602`- Tôi không biết.

> Không tuyên bố mở rộng của khách hàng phát hành nhiệm vụ phương pháp khi quay lại `-32021`(缺少必需客户端能力),`data.requiredCapabilities`设为 `{"extensions":{"io.modelcontextprotocol/tasks":{}}}`▽不支持的协议字符串返回 `-32022`Không có gì rõ ràng`supported`Với`requested`dữ liệu; thiếu hoặc không dây phiên bản trở lại `-32602`

Một phong bì mà không có JSON-RPC `id`là một thông báo. Người nhận có thể xử lý nó, nhưng nó không phát ra kết quả hoặc lỗi JSON-RPC. Một bộ điều chỉnh HTTP Streamable trả về `202 Accepted`Không có cơ quan nào cho thông báo được chấp nhận.

> 没有 JSON-RPC `id`封封是通知. Người nhận có thể xử lý nó, nhưng không phát ra JSON-RPC kết quả hoặc lỗi.`202 Accepted`

Hiện tại, chỉ có`tools/call`hỗ trợ thực hiện tăng nhiệm vụ. Thiết kế trừu tượng nội bộ của bạn để các loại yêu cầu trong tương lai không yêu cầu viết lại lưu trữ.

> Hiện tại chỉ có`tools/call`支持任务增强执行――设计内部抽象时,让未来的请求类型不需要重写存储――

## Tạo nhiệm vụ hướng dẫn máy chủ Tạo nhiệm vụ hướng dẫn máy chủ

> **【中文解读】**Đây là sự thay đổi lớn nhất về hướng với phiên bản cũ:`params._meta.task.required`Không có. Hiện tại, khách hàng chỉ tuyên bố hỗ trợ mở rộng, bởi máy chủ quyết định một số.`tools/call`Có phải trở thành nhiệm vụ  quay lại `resultType: "task"`加 `taskId``status``ttlMs``pollIntervalMs`等字段──关键规则是持久-before-return: 在 `tasks/get`能解析该 id 之前,服务器不得返回句柄; cuối cùng一致存储 phải trước tiên chờ đọc可见。

Lập cờ của khách hàng cũ `params._meta.task.required`Client tuyên bố hỗ trợ mở rộng, sau đó máy chủ quyết định liệu một cụ thể `tools/call`trở thành một nhiệm vụ.

> 旧客户端标志 `params._meta.task.required`Không có gì. Các thông báo khách hàng mở rộng hỗ trợ, sau đó máy chủ quyết định một số.`tools/call`Có phải biến thành nhiệm vụ.

Yêu cầu:

> Xin vui lòng:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "generate_report",
    "arguments": {"size": "large"},
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/tasks": {}
        }
      }
    }
  }
}
```

Phản ứng:

> 响应:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "task",
    "taskId": "tsk_786512e29e0d",
    "status": "working",
    "statusMessage": "Preparing report outline.",
    "createdAt": "2026-08-21T10:30:00Z",
    "lastUpdatedAt": "2026-08-21T10:30:00Z",
    "ttlMs": 900000,
    "pollIntervalMs": 1000
  }
}
```

Các máy chủ không được trả lại tay cầm này cho đến khi một `tasks/get`trong một cửa hàng cuối cùng nhất quán, chờ cho khả năng hiển thị đọc trước khi trả lời. Nếu không, một khách hàng có thể nhận được một ID có vẻ hợp lệ và ngay lập tức nhận được "không được tìm thấy".

> Trong `tasks/get`能解析该 id 之前,服务器不得返回这个句柄──在最终一致的存储中,应答前要等待可见──否则客户端可能得到一个看起来合法的 id,紧接着就得到"没有找到"──

Một câu trả lời nhiệm vụ không được yêu cầu trong nghĩa là khách hàng không yêu cầu chế độ nhiệm vụ. Nó không phải là không đàm phán: yêu cầu hiện tại vẫn phải quảng cáo về mở rộng.

> 任务响应 trong "customer without request task mode" có nghĩa là chưa được yêu cầu. Nhưng nó không được đàm phán.

> ️ **【易错点】**场景:先返回任务Id 再异步写存储 / 后果:客户端立刻 `tasks/get`拿到"未找到",重试风暴或用户以为任务丢失;多副本部署下别的副本更是必然查不到 / 修复:坚持持持久久-before-return先持久化(最终一致存储要等读可见) 再返回句柄;`ttlMs`Từ khi tạo ra, bắt đầu tính toán, là kết thúc chứ không phải là "thỏa cam kết giữ lại kết quả sau khi hoàn thành".

## Hình dạng nhiệm vụ

Mỗi nhiệm vụ đều mang theo:

> Mỗi nhiệm vụ đều mang theo:

- `taskId`: định danh máy chủ được tạo ra ổn định;
  Trung ngữ翻译:`taskId`: máy chủ tạo của định dạng nhận dạng;
- `status``working`- `input_required`- `completed`- `cancelled`, hoặc`failed`-
  Trung ngữ翻译:`status`- Có thể là:`working``input_required``completed``cancelled`Hoặc`failed`-
- `createdAt`và `lastUpdatedAt`: Tiêu chuẩn ISO 8601;
  Trung ngữ翻译:`createdAt`Với`lastUpdatedAt`:ISO 8601 时间;
- `ttlMs`: thời gian hết hạn từ khi tạo ra, hoặc `null`Không giới hạn quảng cáo;
  Trung ngữ翻译:`ttlMs`Từ khi thành lập,`null`表示不声明上限;
- tùy chọn `pollIntervalMs`: thời gian biểu thăm dò tối thiểu hiện tại của máy chủ;
  Trung ngữ翻译:可选的`pollIntervalMs`: dịch vụ đang đề nghị khoảng cách yêu cầu tối thiểu;
- tùy chọn `statusMessage`: bối cảnh đối diện với người dùng hoặc đối diện với mô hình.
  Trung ngữ翻译:可选的`statusMessage`: Façãu user hoặc mô hình trên:

Các trường cụ thể về tình trạng chỉ xuất hiện khi có liên quan:

> 状态相关字段 chỉ xuất hiện trong liên quan:

- `input_required`bao gồm `inputRequests`- Tôi không biết.
  Trung ngữ翻译:`input_required`包含 `inputRequests`
- `completed`bao gồm các yêu cầu ban đầu `result`hình dạng.
  Trung ngữ翻译:`completed`包含原始请求的 `result`形状──
- `failed`bao gồm một JSON-RPC `error`đối tượng.
  Trung ngữ翻译:`failed`包含 JSON-RPC `error`Đối tượng:

Khách hàng nên tôn trọng`pollIntervalMs`Một máy chủ có thể hạn chế tỷ lệ thăm dò dữ dội hơn và có thể thay đổi khoảng thời gian trong suốt thời gian nhiệm vụ.

> 客户端 phải tuân thủ `pollIntervalMs` máy chủ có thể đối phó với dòng truy vấn tăng cường hơn, hoặc có thể thay đổi khoảng thời gian trong vòng đời nhiệm vụ.

## Cuộc thăm dò với `tasks/get``tasks/get`轮询

Khách hàng yêu cầu một bức ảnh hiện tại:

> 客户端请求当前快照:

```http
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tasks/get
Mcp-Name: tsk_786512e29e0d
```

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tasks/get",
  "params": {
    "taskId": "tsk_786512e29e0d",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/tasks": {}
        }
      }
    }
  }
}
```

`tasks/get`tự hoàn thành, do đó kết quả của nó luôn luôn có`resultType: "complete"`- Vấn đề đốn nhựa vẫn có thể xảy ra .`status: "working"`hoặc `status: "input_required"`- Tôi không biết.

> `tasks/get`Bản thân đã hoàn thành, vì vậy kết quả của nó luôn là`resultType: "complete"`                                                                                                                                                                                                                                                              `status: "working"`Hoặc`status: "input_required"`

Sự phân biệt này ngăn chặn lỗi phân tích phổ biến:

> Cái phân biệt này có thể ngăn chặn một lỗi phân tích phổ biến:

```text
result.resultType = complete    means the tasks/get RPC finished
result.status = working        means the represented job is still running
```

> Đối với:`result.resultType = complete`biểu hiện nhiệm vụ/ nhận được RPC này kết thúc;`result.status = working`Cụ thể nhiệm vụ mà nó đại diện vẫn đang chạy.

Không có `tasks/result`Khi nhiệm vụ hoàn thành, người tiếp theo sẽ`tasks/get`Câu trả lời trong bản gốc `CallToolResult`dưới `result`- Có thể là:

> Không có gì`tasks/result`调用──任务完成后,次次`tasks/get`响应把原始的                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `CallToolResult`Trong liên kết`result`下:

```json
{
  "resultType": "complete",
  "taskId": "tsk_786512e29e0d",
  "status": "completed",
  "createdAt": "2026-08-21T10:30:00Z",
  "lastUpdatedAt": "2026-08-21T10:34:12Z",
  "ttlMs": 900000,
  "result": {
    "resultType": "complete",
    "content": [
      {"type": "text", "text": "Generated large report with approved outline."}
    ],
    "structuredContent": {"size": "large", "approved": true},
    "isError": false,
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "tasks-demo",
        "version": "1.0.0"
      }
    }
  },
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "tasks-demo",
      "version": "1.0.0"
    }
  }
}
```

Bên ngoài `resultType`nói `tasks/get`RPC hoàn thành.`result.resultType`nói rằng cuộc gọi công cụ ban đầu đã hoàn thành.`CallToolResult`Nó cũng phải mang theo của riêng nó `io.modelcontextprotocol/serverInfo`; bài học này bao gồm nó thay vì lưu trữ một tải trọng hữu ích không được loại.

> Bên ngoài`resultType`Nói rõ`tasks/get`RPC đã hoàn thành.`result.resultType`Nói rõ công cụ nguyên thủy được sử dụng đã hoàn thành.`CallToolResult`Và phải mang theo của mình.`io.modelcontextprotocol/serverInfo`; 本课包含它, chứ không phải tồn tại một loại không tải.

Không có `tasks/list`Các máy chủ không có phiên không thể suy luận an toàn các nhiệm vụ thuộc về danh sách kết nối. Các ứng dụng cần lịch sử nên phơi bày một công cụ miền được ủy quyền với các bộ lọc rõ ràng và các quy tắc sở hữu.

> Không có gì`tasks/list` Không có cuộc họp máy chủ không thể xác định một cách an toàn những nhiệm vụ thuộc một danh sách của phạm vi kết nối nào đó.

> 🤔 **【困惑】**Q: 旧的`tasks/status``tasks/result`Không phải trực tiếp hơn sao?`tasks/get`A: Bởi vì phương pháp cũ liên quan đến giả định "số họp có thể vòng tròn định nhiệm vụ".`taskId`定位任务,那就没有理由为"状态"和"结果"分设两个方法`tasks/get`Một lần quay lại hoàn toàn, kết thúc thời gian kết quả liên kết.`tasks/list`Được gỡ bỏ: cần danh sách để làm một công cụ lĩnh vực rõ ràng, tự xác định và trao quyền.

## Nhập trong quá trình thực hiện nhiệm vụ Nhập trong quá trình thực hiện nhiệm vụ

Các đầu vào nhiệm vụ và MRTR cốt lõi trông giống nhau nhưng sử dụng các tiếp tục khác nhau.

> 任务输入与核心MRTR看着相似, nhưng sử dụng phương pháp tiếp nối khác nhau.

### Đăng nhập cần thiết trước khi tạo nhiệm vụ

Lòng quay trở lại `resultType: "input_required"`từ bản gốc `tools/call`Khách hàng hoàn thành nó và thử lại cuộc gọi ban đầu. chỉ tạo nhiệm vụ sau khi các vòng MRTR đồng bộ kết thúc.

> Trong nguyên thủy`tools/call`                                                                                  `resultType: "input_required"` Khách hàng hoàn thành nó và thử lại việc điều chỉnh ban đầu.

### Nhập cần thiết sau khi tạo nhiệm vụ

Đặt nhiệm vụ cho `input_required`- `tasks/get`cho thấy những gì nổi bật `inputRequests`, và khách hàng gửi câu trả lời qua `tasks/update`Khách hàng không thử lại bản gốc.`tools/call`- Tôi không biết.

> Đặt nhiệm vụ cho `input_required``tasks/get` Khám phá chưa quyết định `inputRequests`, khách hàng qua `tasks/update`发送响应──客户端不重试原始的 `tools/call`

> **【中文解读】**输入时机决定续接方式, đây là điểm dễ dàng nhất trong các quy tắc mới: tạo nhiệm vụ trước thiếu输入 走核心 MRTR(`input_required`结果 + 客户端重试原始 `tools/call`); tạo nhiệm vụ后缺输入走任务输入( nhiệm vụ trạng thái đặt `input_required`, khách hàng dùng`tasks/update`应答,不再重试原调用) ∼ mỗi条 `inputRequests`Các khóa trong nhiệm vụ trong suốt vòng đời phải là duy nhất, khách hàng nhấn khóa để tải, máy chủ bỏ qua không biết / đã bị bỏ qua / đã đáp ứng các khóa.

Hình ảnh:

> 快照:

```json
{
  "resultType": "complete",
  "taskId": "tsk_786512e29e0d",
  "status": "input_required",
  "createdAt": "2026-08-21T10:30:00Z",
  "lastUpdatedAt": "2026-08-21T10:31:00Z",
  "ttlMs": 900000,
  "inputRequests": {
    "approve_outline": {
      "method": "elicitation/create",
      "params": {
        "mode": "form",
        "message": "Approve the generated report outline?",
        "requestedSchema": {
          "type": "object",
          "properties": {"approved": {"type": "boolean"}},
          "required": ["approved"]
        }
      }
    }
  }
}
```

Cập nhật:

> 更新:

```http
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tasks/update
Mcp-Name: tsk_786512e29e0d
```

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tasks/update",
  "params": {
    "taskId": "tsk_786512e29e0d",
    "inputResponses": {
      "approve_outline": {
        "action": "accept",
        "content": {"approved": true}
      }
    },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/tasks": {}
        }
      }
    }
  }
}
```

Câu trả lời thành công là một sự thừa nhận trống rỗng cộng với `resultType: "complete"`Sự thay đổi của nhà nước có thể cuối cùng là phù hợp, vì vậy khách hàng tiếp tục thăm dò hoặc lắng nghe.

> Thành công đáp ứng là không xác nhận thêm`resultType: "complete"`◊ tình trạng thay đổi có thể là kết quả nhất quán, vì vậy khách hàng tiếp tục hỏi hoặc nghe ◊

Mỗi người`inputRequests`Key phải là độc đáo cho toàn bộ cuộc sống của nhiệm vụ.`tasks/get`các ảnh chụp nhanh có thể hiển thị cùng một khóa đang chờ; các client sao chép lại UI và các máy chủ bỏ qua các phản ứng cho các khóa không rõ, thay thế hoặc đã được thực hiện.`input_required`cho đến khi tất cả các khóa cần thiết được trả lời.

> Mỗi 条`inputRequests`Đơn vị quan trọng trong suốt chu kỳ đời phải là duy nhất.`tasks/get`快照可能显示相同未决键; khách hàng đối với UI 重, máy chủ bỏ qua đối với không biết 已作废或已应答键的响应.`input_required`, cho đến khi tất cả các yếu tố cần thiết đều được đáp ứng.

## Tháo hỏng là hợp tác.

`tasks/cancel`Các công việc có thể kết thúc trước, bỏ qua hủy bỏ hoặc chuyển đổi sau đó.

> `tasks/cancel`Quý vị đã xác nhận không đảm bảo rằng máy đã dừng lại.

```http
POST /mcp HTTP/1.1
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tasks/cancel
Mcp-Name: tsk_786512e29e0d
```

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tasks/cancel",
  "params": {
    "taskId": "tsk_786512e29e0d",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/tasks": {}
        }
      }
    }
  }
}
```

Đối với cả ba phương pháp nhiệm vụ,`Mcp-Name`gương`params.taskId`Nó không lặp lại tên phương pháp JSON-RPC. `code/main.py`tập trung quy tắc này trong `make_http_request`- Tôi không biết.

> Đối với tất cả ba phương pháp nhiệm vụ,`Mcp-Name`镜像 `params.taskId`▽ It doesn't重复 JSON-RPC 方法名──`code/main.py`Trong `make_http_request`Trung tập trung thực hiện quy tắc này:.

Người làm việc bài học tôn trọng hủy ngay lập tức, làm cho các cuộc gọi lặp đi lặp lại không có khả năng.

> Các máy tính làm việc ngay lập tức đáp ứng được loại bỏ, làm cho việc lặp lại được sử dụng, vv.

Không sử dụng `notifications/cancelled`để hủy bỏ một nhiệm vụ. Thông báo đó thuộc về yêu cầu hủy bỏ, không phải là nhiệm vụ lâu dài.

> Đừng dùng`notifications/cancelled`取消任务──那通知属于请求取消,而非持久化任务──

> **【中文解读】**记住两条分界线:(1) `notifications/cancelled`取消的是"请求",`tasks/cancel`取消的是" nhiệm vụ"一旦 `tools/call`已回归 `resultType: "task"`, đó là yêu cầu đã hoàn thành, kết nối bị cắt không còn để duy trì nhiệm vụ;`tasks/cancel`Đảm nhận chỉ đại diện cho " ý định đã ghi lại", không đại diện cho máy tính đã ngừng sản xuất khách hàng phải tiếp tục`tasks/get`快照确认终态, chứ không phải từ xác nhận推断.

Sự khác biệt quan trọng ở biên giới định tuyến. Phục hồi yêu cầu nhắm vào một hoạt động JSON-RPC trong chuyến bay hoặc phản ứng HTTP theo yêu cầu của nó. Nếu `tools/call`đã trở về rồi `resultType: "task"`, yêu cầu đó hoàn thành và đóng cửa vận chuyển của nó không thể đặt tên hoặc dừng lại công việc lâu dài. `tasks/cancel`là một RPC mới được ủy quyền.`params.taskId`, gương danh tính đó trong `Mcp-Name`, giải quyết hậu thuẫn sở hữu nhiệm vụ, ghi lại ý định hủy hợp tác, và trả lại một xác nhận mà không tuyên bố người lao động đã dừng lại.

> Sự khác biệt này trong đường biên giới rất quan trọng. Ứng dụng xóa đối với một hoạt động JSON-RPC đang diễn ra hoặc phạm vi của yêu cầu của HTTP Ứng dụng.`tools/call`已回归 `resultType: "task"`, yêu cầu đã hoàn thành, đóng lại truyền tải của nó không thể đặt tên hoặc không thể dừng lại nhiệm vụ kéo dài đó.`tasks/cancel`Đó là một công ty mới được ủy quyền.`params.taskId`、 trong `Mcp-Name`Trung镜像该 id、解析任务归属后端、记录协作取消意图,并返回确认但不声称工作器已停止

Do đó, một cửa khẩu phải giữ các bộ điều phối yêu cầu và các tuyến đường nhiệm vụ trong các bảng khác nhau. Bảng yêu cầu có thể biến mất khi kết thúc phản hồi. tuyến đường nhiệm vụ phải tồn tại cho đến khi trạng thái cuối cùng và lưu trữ hết hạn. [Lesson 29: MCP Reliability, Cancellation, and Flow Control](../../29-mcp-reliability-cancellation-and-flow-control/docs/en.md)xây dựng cuộc đua, thời gian nghỉ, bất lực, áp lực ngược lại, và thử lại các quy tắc cho cả hai con đường.

> Vì vậy, các mạng cần phải đặt các trình điều phối viên yêu cầu và đường nhiệm vụ vào các bảng khác nhau.[Lesson 29: MCP Reliability, Cancellation, and Flow Control](../../29-mcp-reliability-cancellation-and-flow-control/docs/en.md) xây dựng hai đường đua 超时、等 背压 và重试规则

## Thông báo tùy chọn .

Cuộc thăm dò là cơ sở. Một khách hàng muốn cập nhật đẩy gửi `subscriptions/listen`với ID nhiệm vụ. Đối với Streamable HTTP, đây là một POST mà phản ứng của nó là một dòng SSE có quy mô yêu cầu. Không có dòng GET tự động và không có phiên giao thức để giữ cho cuộc sống.

> 轮询是基线. 想要推送更新的客户端发送携带任务 id 的 `subscriptions/listen`❖ Đối với HTTP Streamable, đây là một POST, đáp ứng của nó là các yêu cầu của SSE 流── không có một GET 事件流 độc lập, cũng không cần phải bảo tồn các thỏa thuận cuộc họp──

Server nhận dạng nhận dạng được chấp nhận với `notifications/subscriptions/acknowledged`và sau đó có thể gửi ảnh chụp đầy đủ qua `notifications/tasks`- Thông báo và thông báo về nhiệm vụ`io.modelcontextprotocol/subscriptionId`trong `_meta`, bằng với `subscriptions/listen`request id. Mỗi thông báo nhiệm vụ bằng cách khác bằng với `tasks/get`sẽ quay lại ngay lúc đó.

> 服务器用 `notifications/subscriptions/acknowledged`确认 được nhận dạng, sau đó có thể thông qua `notifications/tasks`发送完整快照──确认和每条任务通知都在 `_meta`Trong tay`io.modelcontextprotocol/subscriptionId`, như vậy `subscriptions/listen`                                                                                                                                                                                                                                                              `tasks/get`Khi đó sẽ quay lại nội dung.

Khách hàng vẫn phải tuyên bố mở rộng nhiệm vụ. Họ nên kết nối lại và tiếp tục từ ID nhiệm vụ lâu dài thay vì phụ thuộc vào việc lặp lại sự kiện hoặc `Last-Event-ID`- Tôi không biết.

> 客户端 vẫn phải tuyên bố Nhiệm vụ 扩展.`Last-Event-ID`

## Sự thất bại về ngữ nghĩa

Sử dụng hai lớp lỗi đúng cách.

> Chính xác sử dụng hai lớp sai lầm.

### Lỗi giao thức

Các tham số phương pháp không hợp lệ hoặc một ID nhiệm vụ không rõ sẽ trả về lỗi JSON-RPC, thường `-32602`. Phản hồi hỗ trợ gia hạn bị mất `-32021`với đối tượng khả năng cần thiết.

> 无效的方法参数或未知任务 id 返回 JSON-RPC 错误, thường là `-32602`◊ thiếu hụt mở rộng hỗ trợ trở lại `-32021`Và kèm theo các đối tượng có khả năng cần thiết.

### Kết quả thực hiện nhiệm vụ

- Kết quả công cụ bình thường với `isError: true`vẫn là một `completed`nhiệm vụ vì cuộc gọi công cụ đã tạo ra kết quả xác định của nó.
  Trung ngữ翻译:带 `isError: true`Kết quả của công cụ thông thường vẫn là`completed`任务, vì công cụ调用 đã tạo ra kết quả xác định của nó.
- Một lỗi JSON-RPC trong quá trình thực hiện bị hoãn làm cho nhiệm vụ `failed`và lưu trữ lỗi JSON-RPC trong `error`- Tôi không biết.
  中文翻译:延迟执行期间的 JSON-RPC 错误使任务变为 `failed`,并把这个 JSON-RPC 错误存储 `error`
- Việc người dùng từ chối có thể tạo ra `cancelled`, kết quả từ chối hoàn thành, hoặc kết quả an toàn cụ thể khác.
  Trung ngữ翻译: user refuse có thể tạo ra `cancelled`、 một kết quả từ chối hoàn thành, hoặc kết quả an ninh cụ thể trong lĩnh vực khác.

## Thường độ, hết hạn và sở hữu

Giữ ít nhất ID nhiệm vụ, trạng thái, dấu thời gian, ttl, khoảng thời gian thăm dò, sở hữu hoạt động ban đầu, kết quả hoặc lỗi, yêu cầu nhập đang chờ, và tất cả các khóa nhập được phát hành.

> Ít nhất là duy trì nhiệm vụ id, trạng thái, thời gian, tròn, vòng truy vấn, quyền sở hữu, kết quả hoặc sai lầm, không quyết định yêu cầu nhập và tất cả các khóa nhập đã được phát hành.

Chìa kho lưu trữ phải bao gồm hoặc giải quyết một người thuê nhà và chủ sở hữu có thẩm quyền.`tasks/get`- `tasks/update`- `tasks/cancel`, và đăng ký.

> 存储键 phải chứa hoặc có thể phân tích được quyền thuê nhà và chủ sở hữu ➡️ biết một nhiệm vụ ID không nên cấp quyền truy cập ➡️ mỗi lần ➡️`tasks/get``tasks/update``tasks/cancel`Và quan sát quyền sở hữu.

`ttlMs`được đo từ khi tạo và có thể thay đổi. Một khách hàng có thể coi nó như một backstop khi một nhiệm vụ đã ngừng sản xuất cập nhật có thể quan sát được. Một máy chủ có thể thất bại và sau đó xóa một nhiệm vụ hết hạn. Đừng mô tả nó như một lời hứa để giữ lại kết quả hoàn thành trong nhiều millisecond sau khi hoàn thành.

> `ttlMs`Từ khi tạo, tính toán và có thể thay đổi. Khi nhiệm vụ ngừng xuất hiện có thể quan sát được khi cập nhật, khách hàng có thể đặt nó vào 底.

Sử dụng viết hoặc giao dịch nguyên tử. Bài học viết một tệp tạm thời và đổi tên nó bằng nguyên tử. Một dịch vụ đa bản sao nên sử dụng một cửa hàng bền chung và một hợp đồng thuê công nhân hoặc kiểm soát đồng thời tương đương.

> Sử dụng viết nguyên tử hoặc quan trọng.

```figure
tp-task-lifecycle
```

## Hãy xây dựng nó.

`code/main.py`thực hiện một dịch vụ nhiệm vụ xác định:

> `code/main.py`实现一个确定性的任务服务:

- `server/discover`trả lại `supportedVersions`, cache gợi ý, và mở rộng nhiệm vụ.
  Trung ngữ翻译:`server/discover` quay lại `supportedVersions`、缓存提示和任务 扩展──
- `tools/list`trả lại một định nghĩa, cacheable `generate_report`mô tả với một sơ đồ đầu vào hợp lệ.
  Trung ngữ翻译:`tools/list`返回带合法输入方案的确定性、可缓存 `generate_report`描述符──
- `tools/call`tạo ra và duy trì nhiệm vụ trước khi quay lại `resultType: "task"`- Tôi không biết.
  Trung ngữ翻译:`tools/call`Trong trở lại`resultType: "task"`之前创建并持久化任务──
- Một phiên bản dịch vụ mới tải lại cùng một nhiệm vụ, chứng minh khởi động lại phục hồi.
  Trung文翻译:新服务实例重载同一任务,演示重启恢复。
- `tasks/get`trả lại ảnh chụp hoàn chỉnh nhiệm vụ.
  Trung ngữ翻译:`tasks/get`返回完整任务快照──
- Người lao động chuyển từ `working`đến`input_required`- Tôi không biết.
  Trung ngữ翻译:工作器从 `working`转到 `input_required`
- `tasks/update`chấp nhận phản hồi trên mẫu và trả lại lời xác nhận hoàn toàn trống.
  Trung ngữ翻译:`tasks/update`接受表单响应并返回空的完成确认──
- Người lao động lưu trữ một con đẻ `CallToolResult`với chính nó `resultType`và server danh tính, sau đó chuyển sang `completed`- Tôi không biết.
  Trung文翻译:工作器存储带自己的 `resultType`和 máy chủ danh tính của các nắp `CallToolResult`, rồi chuyển đến`completed`
- `tasks/cancel`là không có khả năng trong việc thực hiện này.
  中文翻译:本实现中 `tasks/cancel`Đó là những thứ khác.
- Các bộ tạo HTTP `Mcp-Name`đến`params.taskId`cho `tasks/get`- `tasks/update`, và`tasks/cancel`- Tôi không biết.
  中文翻译:HTTP 构建器为 `tasks/get``tasks/update`和 `tasks/cancel`- Đưa đi.`Mcp-Name`设为 `params.taskId`
- Các trợ lý thông báo sử dụng `notifications/subscriptions/acknowledged`và `notifications/tasks`, cả hai đều có thẻ với danh tính yêu cầu nghe.
  中文翻译:通知辅助函数使用 `notifications/subscriptions/acknowledged`和 `notifications/tasks`, duyên都带监听请求 id 的标签──
- Các thông báo không có ID không tạo ra phản ứng JSON-RPC.
  Trung文翻译:无 id 的通知不产生 JSON-RPC 响应──

Người lao động tiến lên một cách rõ ràng thay vì ngủ trong một chuỗi nền. Điều đó làm cho mọi chuyển đổi trạng thái xác định và giữ cho ví dụ giao thức tách biệt với cơ học hàng.

> 工作器 hiển nhiên tiến bộ, thay vì ngủ trong đường dây phía sau.

## Sử dụng nó để kiểm tra

Từ nguồn kho:

> Từ thư mục kho:

```bash
cd phases/13-tools-and-protocols/13-mcp-async-tasks/code
python3 main.py
python3 -m unittest discover tests -v
```

Dòng kết quả dự kiến:

> 预期结果序列:

```text
id=0 resultType=complete status=ack
id=1 resultType=task status=working
id=2 resultType=complete status=working
id=3 resultType=complete status=input_required
id=4 resultType=complete status=ack
id=5 resultType=complete status=completed
```

Cũng xác minh rằng `tasks/status`- `tasks/result`, và`tasks/list`Phương pháp trả lại không được tìm thấy trong dịch vụ hiện đại.
> Còn phải chứng minh`tasks/status``tasks/result`和 `tasks/list`Trong dịch vụ hiện đại trở lại phương pháp không tìm thấy.
Hãy kiểm tra điều đó.`tools/list`là xác định và mỗi phương pháp HTTP hiện tại phản ánh ID nhiệm vụ của nó thông qua `Mcp-Name`- Tôi không biết.

> 验证 `tools/list`Định nghĩa, và mỗi hiện hành HTTP  nhiệm vụ phương pháp đều qua `Mcp-Name`镜像其任务 id──

## Chuyển nó đi.

`outputs/skill-task-store-designer.md`hiện đang sản xuất một thiết kế có ý thức về mở rộng: đàm phán khả năng, tạo ra lâu dài trước khi trở lại, phương pháp hiện tại, dòng cập nhật đầu vào, sở hữu, hết hạn, hủy bỏ, đăng ký và di chuyển từ các phương pháp thử nghiệm đã bị xóa.

> `outputs/skill-task-store-designer.md`现在产出扩展感知的设计:能力协商、持久-before-return 创建、现行方法、输入更新流、所有权、过期、取消、订阅,以及从已移除的实验性方法迁移──

## Tập luyện bài tập

1. Thêm một khóa nhập còn lại.`tasks/update`và chứng minh nhiệm vụ vẫn còn.`input_required`cho đến khi hai khóa được trả lời.
   Trung文翻译:添加第二个未决输入键──发送部分 `tasks/update`, chứng minh nhiệm vụ trong hai khóa đều được đáp ứng trước để giữ `input_required`
2. Thêm quyền sở hữu của người thuê nhà vào cửa hàng và từ chối một ID nhiệm vụ hợp lệ được trình bày bởi người chủ sở hữu xác thực sai.
   Trung ngữ翻译: cho kho lưu trữ thêm quyền sở hữu thuê nhà, từ chối bằng sai lầm đã xác nhận chủ thể biểu hiện nhiệm vụ hợp pháp ID.
3. Thêm một hợp đồng thuê nhân viên khi hết hạn.
   Trung ngữ翻译:添加带过期工作者租约──证明两个服务实例不能并发完成同一任务──
4. Thực hiện một bộ điều chỉnh SSE phản ứng POST cho `subscriptions/listen`. Không thêm GET, `Last-Event-ID`, hoặc một tiêu đề phiên.
   中文翻译:为 `subscriptions/listen`实现 POST 响应 SSE 适配器──不要添加 GET、`Last-Event-ID`Hoặc là một câu chuyện.
5. Thêm thời hạn dọn dẹp. Nhận phân biệt một nhiệm vụ đã hết hạn từ một ID nhiệm vụ bị hình thành sai mà không rò rỉ sự tồn tại của người thuê nhà.
   Trung ngữ翻译:添加过期清理──区分过期任务与形式错误的任务 id,且不泄露跨租户的存在──

## Từ khóa  Từ khóa nhanh chóng

| Term | Meaning in the current extension |
|------|----------------------------------|
| Tasks extension | Optional `io.modelcontextprotocol/tasks` capability for durable async work |
| `CreateTaskResult` | Server-directed `resultType: "task"` response to an eligible request |
| `tasks/get` | Poll a full current task snapshot, including terminal result or pending input |
| `tasks/update` | Submit responses to a task's outstanding `inputRequests` |
| `tasks/cancel` | Acknowledge cooperative cancellation intent |
| `input_required` | Task status indicating client input is outstanding |
| `pollIntervalMs` | Server-suggested minimum delay before another poll |
| `ttlMs` | Expiry duration measured from task creation |
| Durable-before-return | Rule that the task id must resolve before its handle is sent |
| `notifications/tasks` | Optional full task snapshot delivered on a subscribed SSE response |

> **【中文解读】**术语速查(中英对照):Tác vụ mở rộng=官方 `io.modelcontextprotocol/tasks`扩展能力;CreateTaskResult= đối với yêu cầu được cấp 的主导`resultType: "task"`响应;`tasks/get`= vòng hỏi hoàn chỉnh nhiệm vụ快照(含终态结果或未决输入);`tasks/update`= nộp đối với chưa quyết định`inputRequests``tasks/cancel`= xác nhận协作取消意图;input_required= nhiệm vụ trạng thái, cho thấy khách hàng nhập chưa quyết định;pollIntervalMs= dịch vụ đề nghị của vòng hỏi nhỏ nhất;ttlMs= từ nhiệm vụ tạo và tính toán quá hạn thời gian;Durable-before-return=句柄发出前任务 id 必须可解析;`notifications/tasks`= Đăng ký SSE 响应上投递的可选完整任务快照──

## Legacy Compatibility Ước tính

Vùng thử nghiệm 2025-11-25 sử dụng việc tăng nhiệm vụ yêu cầu của khách hàng,`tasks/status`- `tasks/result`, và tùy chọn `tasks/list`. giữ những tên chỉ trong một bộ chuyển đổi cũ gắn. một khách hàng hiện tại sử dụng khả năng mở rộng, chấp nhận máy chủ hướng dẫn tay cầm, thăm dò `tasks/get`, cung cấp đầu vào với `tasks/update`, và đọc kết quả cuối cùng từ ảnh chụp nhanh của nhiệm vụ.

> 2025-11-25  tăng cường nhiệm vụ thực nghiệm trên bề mặt sử dụng yêu cầu khách hàng`tasks/status``tasks/result`和可选的 `tasks/list` Chỉ giữ những tên trong phiên bản cũ được khóa  khả năng mở rộng sử dụng khách hàng hiện tại  chấp nhận các câu lệnh  truy vấn chủ đạo của máy chủ `tasks/get`、 dùng `tasks/update`补充输入,并从任务快照读取最终结果──

## Xem thêm 延伸阅读

- [Official MCP Tasks extension](https://tasks.extensions.modelcontextprotocol.io/specification/draft/tasks)
  Trung文翻译:官方 MCP Tasks 扩展规范(当前为草案)。
- [MCP 2026-07-28 Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
  Trung ngữ翻译:MRTR 模式规范, nhiệm vụ tạo trước输入收集的机制来源──
- [MCP 2026-07-28 Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
  Trung文翻译:Streamable HTTP 传输规范,`Mcp-Method`- Không.`Mcp-Name`头与 POST 响应 SSE 的定义处──
