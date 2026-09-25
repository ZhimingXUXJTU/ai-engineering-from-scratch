# MCP Transport: studio và stateless Streamable HTTP . MCP 传输层:studio với không trạng thái Streamable HTTP

> Transport mang thông điệp MCP. Nó không cung cấp trạng thái giao thức bị thiếu.`2026-07-28`, địa phương stdio và từ xa Streamable HTTP cả hai mang lại tự mô tả yêu cầu.

> **【中文解读】**传输层 chỉ chịu trách nhiệm di chuyển MCP 消息, không chịu trách nhiệm hoàn thành thỏa thuận trạng thái. Trong quy định 2026-07-28 规范,本地工作室和远程流媒体 HTTP 传递的都是"自描述"请求每个请求自带协议版本与客户端能力,不再依赖连接或会话保存上下文.

> **【拓展：传输层演进→2026-07-28 无状态化】**MCP 传输层三年三变:2024-11 của HTTP+SSE 双端点、2025-03-26 của Streamable HTTP(GET 流 + `Mcp-Session-Id`会话) 、再到2026-07-28 的无状态 POST-only 契约──演进方向始终是"把状态从传输层赶出去": 会话头没了,改成请求体 `_meta`携带版本与能力; độc lập GET 流没了,改成 `subscriptions/listen`Đơn xin cấp độ đáp ứng. Không trạng thái để bất kỳ phụ bản nào có thể xử lý bất kỳ yêu cầu, là chìa khóa của việc mở rộng.

>  **【前置】**学本节前请先掌握:(1) Bước 13·07、08(MCP server 和 client) 理解 JSON-RPC 分发逻辑;(2) HTTP 协议基础(method、header、状态码);(3) DNS 重绑定攻击概念本节的`Origin`校验是防御手段;(4) 若你学过本课旧版(2025 传输:GET 流 + 会话头 + `Last-Event-ID`重放), xin hãy đọc lại lại.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lessons 07 and 08 | **前置知识:** Phase 13 · 07、08（MCP 服务器与客户端）
**Time:** ~65 minutes | **时间:** 约 65 分钟

## Mục tiêu học tập

- Chọn stdio cho các quy trình trẻ em địa phương và Streamable HTTP cho các dịch vụ mạng.
  Trung文翻译:本地子进程选studio,网络服务选 Streamable HTTP──
- Thực hiện hợp đồng HTTP Streamable hiện đại chỉ có điểm cuối duy nhất, chỉ có POST.
  Trung文翻译:实现现代的单端点、仅 POST 的 Streamable HTTP 契约──
- Nhìn và xác nhận phiên bản, phương pháp và tiêu đề tên MCP đối với cơ thể JSON-RPC.
  Trung文翻译:把 MCP 版本、方法、名称镜像头与 JSON-RPC 请求体做比对校验──
- Chuyển giao SSE theo yêu cầu và lâu dài `subscriptions/listen`dòng chảy đúng cách.
  Trung語翻译:正确交付请求级 SSE流和长生命周期的`subscriptions/listen`流──
- Chuyển các triển khai HTTP + SSE dựa trên phiên và di truyền mà không trình bày hành vi di truyền như hiện đại.
  Trung ngữ翻译:迁移基于会话的部署和遗留 HTTP+SSE 部署,且不把遗留行为冒充为现代行为──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**本节讲清"Why do you need to be stateless"―早期 Streamable HTTP 把协议协商、连接行为、会话行为捆绑服务器可以造`Mcp-Session-Id`、để lộ độc lập GET 流、 chấp nhận DELETE 终止会话、用 `Last-Event-ID`恢复 SSE──2026-07-28 Đưa tất cả các cơ chế này ra khỏi mô hình modern line: mỗi yêu cầu đều có thể rơi vào bất kỳ người lao động sức khỏe lên, vì phiên bản giao thức và khả năng khách hàng theo yêu cầu truyền thể; HTTP chỉ làm đường dẫn với hình ảnh chiến lược, máy chủ thực hiện trước cuộc họp thử nghiệm với thể có phù hợp không.

Các phiên bản HTTP Streamable trước đây kết hợp đàm phán giao thức với kết nối và hành vi phiên.`Mcp-Session-Id`, phơi bày một dòng GET độc lập, chấp nhận DELETE để chấm dứt phiên, và tiếp tục SSE với `Last-Event-ID`- Tôi không biết.

> Hơn nữa, phiên bản HTTP được phát trực tuyến đã kết hợp với các giao thức để đàm phán và kết nối.`Mcp-Session-Id`、 tiết lộ một GET 流 độc lập 、 chấp nhận DELETE để kết thúc cuộc trò chuyện,并使用 `Last-Event-ID`Khôi phục SSE.

MCP `2026-07-28`Các tiêu đề HTTP phản chiếu các trường hợp được chọn để định tuyến và chính sách, nhưng máy chủ xác nhận các tiêu đề đó chống lại cơ thể trước khi thực hiện.

> MCP `2026-07-28`Từ định dạng modern line, các cơ chế này đã được chuyển đi. Mỗi yêu cầu có thể rơi vào bất kỳ nhân viên y tế nào, vì phiên bản giao thức và khả năng khách hàng theo yêu cầu truyền tải.

Kết quả dễ dàng hơn để mở rộng và dễ hơn để lý luận về. Nó cũng có nghĩa là một máy chủ dạy giao thông 2025 như hiện tại đang dạy sai lầm và mô hình bảo mật.

> Kết quả dễ dàng hơn để mở rộng, cũng dễ hơn để suy luận. Điều này cũng có nghĩa là: đưa 2025  truyền tải như là các quy tắc hiện hành để dạy các máy chủ, dạy là sai lầm của mô hình thất bại và mô hình an toàn.

## Khái niệm cốt lõi

>  **【类比】**无状态传输像外卖平台的订单流转.旧模式(会话式传输) 如"你只能等起初接单的那骑手"骑手下线(副本重启),订单就卡住.。新模式(2026-07-28 无状态) 如"任何站点都能接住你的订单"每张订单(请求) 都完整写明地址和备注(协议版本、能力),谁接手都能继续干活;贵重物寄存(应用状态) 不塞进骑手口袋(连接亲和件),而是给一个张取性码 (显式句柄) ⇒

### studio

Việc liên kết stdio là cho một quá trình phụ được khởi động bởi khách hàng:

> stdio 绑定面向客户端启动的子进程:

- Khách hàng viết một tin nhắn UTF-8 JSON-RPC cho mỗi dòng cho stdin.
  Trung文翻译:客户端向 stdin 每行写入一条 UTF-8 JSON-RPC 消息──
- Server viết một tin nhắn UTF-8 JSON-RPC mỗi dòng cho stdout.
  Trung文翻译:服务器向 stdout 每行写入一条 UTF-8 JSON-RPC 消息──
- Server viết chẩn đoán cho STDERR.
  Trung文翻译:服务器把诊断信息写入 stderr。
- Máy chủ sẽ nhanh chóng thoát khỏi Stdin EOF.
  中文翻译:stdin 出现 EOF 时服务器立即退出──
- Mỗi yêu cầu hiện đại đều có phiên bản và khả năng của khách hàng trong `params._meta`- Tôi không biết.
  Trung ngữ翻译:每个现代请求都在 `params._meta`Trung ương mang phiên bản và khả năng khách hàng.

Quá trình này có thể hoạt động cho nhiều cuộc gọi, nhưng nó không phải là một phiên giao thức hiện đại. Nếu nó thoát khỏi bất ngờ, các yêu cầu trong chuyến bay sẽ bị mất. Bắt đầu lại quá trình, khám phá lại, tái đăng ký, mở lại đăng ký và thử lại các hoạt động an toàn với các ID yêu cầu mới.

> Quá trình có thể tồn tại nhiều lần được调用, nhưng nó không phải là một giao thức trong nghĩa hiện đại. Nếu quá trình không ngờ xuất hiện, yêu cầu được thực hiện sẽ bị mất.

### HTTP được phát trực tuyến vào năm 2026-07-28

> **【中文解读】**现代服务器只暴露一个接收 POST 的 MCP 端点(如 `/mcp`(..)  Mỗi bài JSON-RPC Ứng dụng hoặc thông báo là một POST HTTP mới, yêu cầu chỉ chứa một tin nhắn; khách hàng không gửi JSON-RPC 响应.`application/json`(单条 JSON-RPC 响应) hoặc `text/event-stream`(Từ trước đến thông báo liên quan đến yêu cầu, cuối cùng đến phản ứng cuối cùng); thông báo được chấp nhận và trả lại không chủ đề.`202 Accepted`❖ 客户端用 `Accept: application/json, text/event-stream`Đồng thời tuyên bố hai loại phản ứng:

Một máy chủ hiện đại cho thấy một điểm cuối MCP, chẳng hạn như `/mcp`, đó là chấp nhận POST.

Mỗi yêu cầu hoặc thông báo JSON-RPC là một POST HTTP mới. Cơ thể chứa một tin nhắn JSON-RPC. Khách hàng không gửi phản hồi JSON-RPC đến máy chủ.

> 现代服务器暴露一个接收 POST 的 MCP端点, ví dụ `/mcp` Mỗi bài JSON-RPC Ứng dụng hoặc thông báo đều là một bài đăng HTTP mới  Ứng dụng chứa một bài JSON-RPC 消息  Ứng dụng không hướng tới máy chủ gửi JSON-RPC 响应

Đối với yêu cầu, máy chủ trả lại:

- `Content-Type: application/json`với một phản ứng JSON-RPC; hoặc
- `Content-Type: text/event-stream`Thông báo liên quan đến yêu cầu đó, tiếp theo là phản hồi cuối cùng của JSON-RPC.

Đối với một thông báo được chấp nhận, máy chủ trả lại `202 Accepted`Không có xác.

> 对于请求,服务器返回两种之一:`Content-Type: application/json`带一条 JSON-RPC 响应, hoặc `Content-Type: text/event-stream`Trước khi đưa ra thông báo liên quan đến yêu cầu này, tiếp tục đưa ra phản ứng cuối cùng của JSON-RPC.`202 Accepted`

Khách hàng quảng cáo cả hai loại phản ứng:

> 客户端 đồng thời tuyên bố chấp nhận hai loại phản ứng:

```http
Accept: application/json, text/event-stream
```

### Chỉ có POST nghĩa là chỉ có POST

> ️ **【易错点】**场景: Từ phiên bản cũ Streamable HTTP 迁移来的服务端习惯性地实现 GET 流、DELETE 会话端点,或造/回显 `Mcp-Session-Id`、 xử lý `Last-Event-ID`/ 后果: Tất cả đều không phải là 2026-07-28  hành viGET và DELETE  phải quay lại `405`,会话头必须被忽视;请求级流在最终响应前中断即宣告请求丢失,只能换新 id 重试,绝不能尝试流恢复 /修复:对照规范逐条移除遗留端点与头处理逻辑,把"断流恢复"改成"新请求重试"――

HTTP Streamable hiện đại không có dòng GET độc lập và không có điểm cuối phiên DELETE.

> 现代 Streamable HTTP 没有独立 GET 流,也没有 DELETE 会话端点。

- `GET /mcp`trả lại `405 Method Not Allowed`- Tôi không biết.
  Trung ngữ翻译:`GET /mcp` quay lại `405 Method Not Allowed`
- `DELETE /mcp`trả lại `405 Method Not Allowed`- Tôi không biết.
  Trung ngữ翻译:`DELETE /mcp` quay lại `405 Method Not Allowed`
- `Mcp-Session-Id`được bỏ qua và không bao giờ được ghi lại hoặc lặp lại.
  Trung ngữ翻译:`Mcp-Session-Id`Được bỏ qua, từ không tạo ra cũng từ không xuất hiện.
- `Last-Event-ID`được bỏ qua bởi vì các dòng hiện đại không thể tiếp tục.
  Trung ngữ翻译:`Last-Event-ID`Được bỏ qua, vì dòng hiện đại không thể phục hồi được.

Nếu một dòng yêu cầu được mở rộng bị phá vỡ trước khi phản hồi cuối cùng của nó, khách hàng đã mất yêu cầu trong chuyến bay. Nó có thể phát hành một yêu cầu mới với một ID JSON-RPC mới khi thử lại an toàn. Nó không được cố gắng nối lại dòng.

> Nếu yêu cầu cấp dòng trong kết thúc phản ứng trước khi bị gián đoạn, khách hàng đã mất yêu cầu đang được thực hiện này. Nó có thể phát hành yêu cầu mới với một ID JSON-RPC mới trong thử nghiệm bảo mật lần nữa. Nó không thể cố gắng để truy cập lại.

### Kiểm tra nguồn gốc

> **【中文解读】**服务器对进入连接做 `Origin`校验以防 DNS 重绑定:头存在且不在白名单就返回 `403 Forbidden`; không trình duyệt khách hàng có thể không mang `Origin`(官方传输规则允许) ――三条要点:(1) 本地服务器应绑定 `127.0.0.1`而非所有网卡;(2) `Origin`Các dịch vụ mạng vẫn cần phải được chứng nhận và ủy quyền cho mỗi yêu cầu;`origin.startswith("https://trusted.example")`Chuẩn bị không an toàn, sẽ bị kẻ tấn công kiểm soát.

Các máy chủ xác nhận`Origin`trên các kết nối tiếp vào để ngăn chặn kết nối lại DNS. Nếu tiêu đề có mặt và không được phép rõ ràng, trả lại `403 Forbidden`. Một khách hàng không phải trình duyệt có thể bỏ qua `Origin`, như quy định vận tải chính thức cho phép.

> 服务器在进入连接上校验 `Origin`Để phòng chống lại DNS bị ràng buộc lại. Nếu có một cái tên không được phép, hãy quay lại.`403 Forbidden`❖ Không trình duyệt khách hàng có thể省略 `Origin`, quy tắc truyền tải chính thức cho phép điều này.

Các máy chủ địa phương nên liên kết với `127.0.0.1`Các dịch vụ mạng vẫn cần xác thực và ủy quyền trên mọi yêu cầu.

> 本地服务器应绑定 `127.0.0.1`, thay vì tất cả các thẻ. Dịch vụ mạng vẫn cần phải được xác nhận và ủy quyền cho mỗi yêu cầu.

Sử dụng sự phù hợp chính xác nguồn gốc sau cấu hình theo quy định.`origin.startswith("https://trusted.example")`là không an toàn vì chúng có thể chấp nhận hậu tố được kiểm soát bởi kẻ tấn công.

> Trong quy định định cấu hình sau khi sử dụng xác định nguồn gốc 匹配.`origin.startswith("https://trusted.example")`Chuẩn bị không an toàn vì chúng có thể chấp nhận kiểm soát của kẻ tấn công.

### Các tiêu đề siêu dữ liệu HTTP cần thiết

> **【中文解读】**Mỗi ngày có 3 tấm gương:`MCP-Protocol-Version` phải bằng `params._meta`Trung bản thỏa thuận;`Mcp-Method`必须等于 JSON-RPC `method`-`tools/call``resources/read``prompts/get`phải带`Mcp-Name`(tương đương với `params.name`- Tôi không biết.`resources/read`时等于 `params.uri`(※头值大小写敏感──不安全或非ASCII 的)`Mcp-Name`用 `=?base64?{...}?=`哨兵编码,服务器解码后再与请求体比对──缺失/形/不匹配 → HTTP `400`+ JSON-RPC `-32020`; version không hỗ trợ → HTTP `400`+ `-32022`Không có xác định`supported`- Không.`requested`数据;未知现代方法 → HTTP `404`+ `-32601`(JSON-RPC 体 rất quan trọng, hai thời đại khách hàng dựa trên nó phân biệt hiện đại lỗi và để lại điểm không định mệnh)

Mỗi yêu cầu POST hiện đại bao gồm:

```http
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: notes_search
```

Quy tắc tiêu đề:

> 头规则:

- `MCP-Protocol-Version`được yêu cầu và phải bằng `params._meta.io.modelcontextprotocol/protocolVersion`- Tôi không biết.
  Trung ngữ翻译:`MCP-Protocol-Version`phải填, và phải bằng `params._meta.io.modelcontextprotocol/protocolVersion`
- `Mcp-Method`được yêu cầu và phải bằng với JSON-RPC `method`- Tôi không biết.
  Trung ngữ翻译:`Mcp-Method`phải填, và phải bằng với JSON-RPC `method`
- `Mcp-Name`được yêu cầu cho `tools/call`- `resources/read`, và`prompts/get`- Tôi không biết.
  Trung ngữ翻译:`tools/call``resources/read``prompts/get`phải带`Mcp-Name`
- `Mcp-Name`=`params.name`, hoặc`params.uri`cho `resources/read`- Tôi không biết.
  Trung ngữ翻译:`Mcp-Name`Đúng vậy.`params.name`; đối với `resources/read`则等于 `params.uri`
- Giá trị tiêu đề là nhạy cảm với trường hợp mặc dù tên tiêu đề là không nhạy cảm với trường hợp.
  Trung ngữ翻译:头值大小写敏感, mặc dù头名大小写不敏感──

Không an toàn hoặc không phải ASCII `Mcp-Name`các giá trị sử dụng UTF-8 Base64 Sentinel chính xác:

```text
=?base64?{Base64EncodedValue}?=
```

Máy chủ giải mã giá trị đó trước khi so sánh nó với cơ thể.

> Không an toàn hay không an toàn`Mcp-Name`值使用精确的 UTF-8 Base64 哨兵格式(如上) ――服务器先解码该值再与请求体比对──

Các tiêu đề gương bị mất tích, sai dạng hoặc không phù hợp trả về HTTP `400`với mã JSON-RPC `-32020`Nếu tiêu đề và cơ thể đồng ý về một phiên bản mà máy chủ không hỗ trợ, trả về HTTP `400`với `-32022`và dữ liệu lỗi chính xác như `{"supported":["2026-07-28"],"requested":"2027-01-01"}`- Tôi không biết.

> 镜像缺失、形或不匹配时返回 HTTP `400`和 JSON-RPC 错误码 `-32020`Nếu tiêu đề và yêu cầu phù hợp với một phiên bản không được hỗ trợ của máy chủ, hãy quay lại HTTP `400`和 `-32022`,并带精确的错误数据, ví dụ:`{"supported":["2026-07-28"],"requested":"2027-01-01"}`

Một phương pháp hiện đại không rõ ràng trả về HTTP `404`với JSON-RPC `-32601`Cơ thể JSON-RPC quan trọng vì một khách hàng hai thời đại sử dụng nó để phân biệt lỗi hiện đại từ lỗi điểm cuối cũ.

> 未知的现代方法 trả về HTTP `404`和 JSON-RPC `-32601` JSON-RPC 响应体 rất quan trọng, vì hai thời đại khách hàng dựa vào nó phân biệt "đại lỗi hiện đại" và "được bỏ lại điểm chưa định mệnh".

### SSE theo yêu cầu

> **【中文解读】**服务器 có thể cho đơn lẻ dài运行请求 chọn SSE 作为响应载体:POST 发发 `tools/call`,响应流上次推送与该请求 id 相关的进步通知,最后给出最终JSON-RPC 响应,流随即关闭.约束有三条条:(1) 服务器不得在该流上发送独立的JSON-RPC 请求样本征询、根交互都改走多轮旅行请求结果;(2) 关闭响应流即取消该请求;(3) 不要重放添 SSE 事件 id`Last-Event-ID`恢复不属于现代修订──

Một máy chủ có thể chọn SSE cho một yêu cầu lâu dài:

```text
POST tools/call id=41
  <- notifications/progress related to id=41
  <- notifications/progress related to id=41
  <- JSON-RPC response id=41
stream closes
```

Các máy chủ không được gửi các yêu cầu JSON-RPC độc lập trên dòng này. Các tương tác lấy mẫu, kích hoạt và gốc sử dụng kết quả yêu cầu nhiều lần.

> 服务器 phải trên dòng này gửi độc lập JSON-RPC 请求──样本, tạo và gốc 交互使用多轮回请求(MRTR) kết quả──关闭响应流即取消该请求──

Đừng thêm ID sự kiện SSE để chơi lại. `Last-Event-ID`Việc tái lập không phải là một phần của phiên bản hiện đại.

> Đừng để thêm SSE 事件 id.`Last-Event-ID`恢复不属于现代修订──

### Những thay đổi lâu dài sử dụng đăng ký / nghe

> **【中文解读】**变更通知不再走独立 GET, mà là khách hàng chủ động khởi động `subscriptions/listen`Ứng dụng: Đăng ký của POST giữ mở, trở thành một dòng SSE dài đời.`notifications`Mục đích là cho phép thanh toán  máy chủ phải gửi loại thông báo không được yêu cầu `notifications/subscriptions/acknowledged`; xác nhận, mỗi điều thay đổi thông báo và kết quả cuối cùng đều là`_meta`Trong khi đó, bạn có thể nghe các yêu cầu của`subscriptionId` máy chủ có thể sử dụng SSE 注释做保活──流断开后,客户端换新请求 id 重新听并重新拉取受影响的数据──`resources/subscribe`和 `resources/unsubscribe`属于遗留时代, cấm sử dụng trên các mạng xã hội hiện đại.

Thông báo thay đổi sử dụng yêu cầu mở bởi khách hàng, không phải là GET độc lập:

```json
{
  "jsonrpc": "2.0",
  "id": "listen-1",
  "method": "subscriptions/listen",
  "params": {
    "notifications": {
      "toolsListChanged": true,
      "resourceSubscriptions": ["notes://note-1"]
    },
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "course-client",
        "version": "1.0.0"
      }
    }
  }
}
```

Phản ứng POST là một dòng SSE lâu đời.`notifications/subscriptions/acknowledged`- Việc xác nhận, mọi thông báo thay đổi và kết quả cuối cùng mang theo`io.modelcontextprotocol/subscriptionId`trong `_meta`, bằng với ID yêu cầu nghe. Server có thể phát ra các bình luận SSE như là các lưu trữ. Khi dòng chảy giảm, client phát lại `subscriptions/listen`với một ID yêu cầu mới và sửa đổi dữ liệu bị ảnh hưởng.

> Phản ứng của POST là một dòng chảy SSE dài đời.`notifications/subscriptions/acknowledged`❖ Thông tin xác nhận  Mỗi thông báo thay đổi và kết quả cuối cùng đều ở `_meta`Trong tay`io.modelcontextprotocol/subscriptionId`,其值等于听 请求的ID. Server có thể sử dụng SSE 注释作为保活.`subscriptions/listen`Và lấy lại dữ liệu bị ảnh hưởng.

`resources/subscribe`và `resources/unsubscribe`Không được sử dụng trong một kết nối hiện đại.

> `resources/subscribe`和 `resources/unsubscribe`属于遗留时代──不要在现代连接上使用它们──

### Tình trạng ứng dụng rõ ràng

> **【中文解读】**删除协议会话 không giống như cấm có trạng thái làm việc. Server có thể tạo ra một trạng thái không minh bạch của câu cầm, như kết quả của công cụ thông thường trả lại; khách hàng trong cuộc gọi tiếp theo đưa nó như một chuyển giao các tham số hiển nhiên. Câu cầm phải được gắn vào chủ đề đã xác nhận, không thể đoán được, có thể hết hạn, mỗi lần sử dụng đều được ủy quyền. Điều này làm cho trạng thái trong cấp ứng dụng hiển thị, chứ không phải là được lưu trữ vào chuyển giao và tính chất. Sự thất bại của trạng thái bản sao ẩn là cơ khí: yêu cầu A trong bản sao 1 trong bộ nhớ trong bộ nhớ tạo bản thảo nhưng không trả lại câu cầm, yêu cầu B  cài đặt bản sao 2 không thể đặt tên hoặc tải vào bản thảo, đường gắn liền trông như sửa chữa các triệu chứng, cho đến khi khởi động lại, phát hành, tái điều chỉnh hoặc chuyển đổi. Phần bên cạnh chính xác của nó: hai phần của giao thức: yêu cầu yêu cầu giữ lại trong mỗi bộ nhớ trong bộ nhớ ứng dụng; yêu cầu kéo dài thời gian sử dụng của các bộ nhớ được sử dụng; yêu cầu B  cài đặt các bộ nhớ được sử dụng theo các quy trình đơn vị khác nhau.`requestState`;草稿或持久任务用显式句柄 + 共享持久化 + 过期 + 并发控制 + 等──这些都不是MCP 协议会话──

Xóa các phiên giao thức không cấm các dòng công việc với trạng thái. máy chủ có thể đúc một tay cầm trạng thái không minh bạch và trả lại nó như một kết quả công cụ bình thường.

> 移除协议会话 không cấm带状态的工作流. Server có thể tạo ra một trạng thái không minh bạch, và như một kết quả công cụ thông thường trả lại.

Kết nối tay với nguyên tắc xác thực, làm cho chúng không thể kiểm tra được, hết hạn và cho phép mọi sử dụng. Điều này làm cho trạng thái hiển thị ở lớp ứng dụng thay vì giấu nó trong mối liên hệ vận tải.

> Đưa câu cầm buộc vào chủ thể đã được xác nhận, làm cho nó không thể đoán được, có thể trôi qua, và được ủy quyền cho mỗi lần sử dụng.

Sự cố do trạng thái sao chép ẩn gây ra là cơ học:

> Sự thất bại do tình trạng ẩn tác gây ra là cơ khí:

1. Đơn xin A đạt đến bản sao 1 và tạo ra một bản thảo trong bộ nhớ của quá trình đó.
  Trung văn翻译:请求 A 到达副本 1, trong trong quá trình内存中创建草稿──
2. Câu trả lời không trả lại một bản thảo vì việc thực hiện cho rằng kết nối xác định bản thảo.
  Trung văn翻译:响应不回复草稿句柄,因为实现假设"连接"能标识草稿──
3. Yêu cầu B là một POST mới và đạt đến bản sao 2.
  Trung文翻译:请求 B 是一次全新 POST,到达副本 2──
4. Replica 2 có metadata giao thức hợp lệ nhưng không có cách để đặt tên hoặc tải bản thảo, do đó workflow thất bại hoặc đọc sai đối tượng địa phương.
  Bản sao 2 có hợp pháp giao ước dữ liệu, nhưng không thể đặt tên hoặc tải bản thảo, vì vậy công việc đã thất bại hoặc đọc sai trái đối tượng địa phương.
5. Đường dẫn dính dường như sửa chữa triệu chứng cho đến khi khởi động lại, triển khai, lên lịch lại hoặc không chạy đến yêu cầu tiếp theo.
  Trung ngữ翻译:粘性路由看似修复症状,直到某次重启,发布,重调度或故障转移挪走了下一个请求──

Biên giới đúng có hai phần. Bối cảnh giao thức vẫn ở trong mỗi yêu cầu. Tình trạng ứng dụng bền vững sống trong một cửa hàng chung dưới một tay cầm được máy chủ ghi lại cho khách hàng. Cuộc gọi tiếp theo cung cấp các xử lý, bất kỳ bản sao nào tải cùng một bản ghi, và ủy quyền liên kết bản ghi với chủ sở hữu và người thuê nhà xác thực. Khoản nhớ sao chép có thể lưu trữ một bản ghi, nhưng nó không thể là bản sao duy nhất cần thiết để chính xác.

> Các biên giới chính xác có hai phần. Các bản dưới đây được lưu trữ trong từng yêu cầu. Các bản ứng dụng được lưu trữ trong kho lưu trữ chung, được máy chủ tạo ra từ ngữ trả lại cho khách hàng.

Chọn cơ chế trạng thái theo thời gian sống. Các biến yêu cầu địa phương có thể phục vụ một cuộc gọi. Một tiếp tục MRTR ngắn có thể sử dụng bảo vệ tính toàn vẹn `requestState`Một bản thảo hoặc nhiệm vụ lâu dài cần một xử lý rõ ràng cộng với sự kiên trì, hết hạn, kiểm soát đồng thời và tính không có khả năng.

> 按生命周期选择状态机制――请求局部变量可服务单次调用――短的MRTR 延续可使用带完整性保护的`requestState`◊ Bản thảo hoặc nhiệm vụ kéo dài cần một cụm từ rõ ràng, ngoài việc chia sẻ kéo dài, quá hạn, và kiểm soát.

### HTTP tương thích hai thời đại

> **【中文解读】**双时代客户端先尝试现代 POST; nhận được HTTP `400`- Không.`404`- Không.`405`Về kiểm tra phản ứng cơ thể: nhận dạng hiện đại JSON-RPC  lỗi chứng minh máy chủ là hiện đại  sửa đổi yêu cầu hoặc thử lại một phiên bản đã công bố, không được giảm; không thể nhận dạng hoặc không thể nhận ra phản ứng才可能是遗留 HTTP+SSE  máy chủ, bây giờ才去试旧 GET 端点并期待其遗留`endpoint`Các máy chủ của thời gian di chuyển có thể chuyển dữ liệu hiện đại từ đường giao thông hiện đại đến POST-chỉ thực hiện ∞ để giữ lại các điểm kết thúc độc lập cho khách hàng cũ, nhưng không thể chuyển lại GET、DELETE、会话 id hoặc tái đặt hành vi mô tả như ∞`2026-07-28`Một phần của nó.

Một client hỗ trợ các máy chủ hiện đại và cũ thử một POST hiện đại trước. Nếu nó nhận HTTP `400`- `404`, hoặc`405`, kiểm tra cơ thể:

> Đồng thời hỗ trợ hiện đại và lưu trữ máy chủ khách hàng trước thử hiện đại POST. Nếu nhận HTTP.`400``404`Hoặc`405`,就检查响应体:

- Một lỗi JSON-RPC hiện đại được công nhận chứng minh máy chủ là hiện đại.
  Trung ngữ翻译:识别出的现代 JSON-RPC 错误证明服务器是现代的── sửa đổi yêu cầu hoặc thử lại một phiên bản đã được công bố──绝不降级──
- Một cơ thể trống hoặc một phản ứng không được nhận ra có thể chỉ ra một máy chủ HTTP + SSE cũ. Chỉ sau đó thử điểm cuối GET cũ và mong đợi sự thừa kế của nó `endpoint`sự kiện.
  Trung ngữ翻译:空体或无法识别的响应可能表明这是遗留的HTTP+SSE 服务器──只有此时才去尝试旧的GET 端点并期待它的遗留`endpoint`Sự kiện

Một máy chủ có thể hỗ trợ cả hai thời đại trong quá trình di chuyển bằng cách định tuyến metadata hiện đại đến thực hiện POST hiện đại và giữ lại các điểm cuối di sản riêng biệt cho các khách hàng cũ.`2026-07-28`- Tôi không biết.

> 服务器在迁移期可以同时支持两个时代:把现代元数据路由到现代 POST-only实现,保留老客户端独立遗留端点――绝不要把遗留的 GET、DELETE、会话 id或重放行为描述为`2026-07-28`Một phần của nó.

```figure
tp-transport-handshake
```

## Hãy sử dụng nó để thực hiện

> **【中文解读】** `code/main.py`Sử dụng Python 标准库 thực hiện một giới hạn 现代的 Streamable HTTP 服务器:校验 `Origin`和镜像头、忽略已移除的会话头、普通调回 JSON,并演示一条有限的 `subscriptions/listen`SSE 流──自检(`--probe`)逐项验证: bất hợp pháp`Origin`Được từ chối, không có cuộc gặp mặt và cũng có thể hoàn thành phát hiện.`Mcp-Session-Id`和 `Last-Event-ID`Được bỏ qua, đầu không phù hợp trở lại`-32020`、不支持的版本返回 `-32022`且带精确数据、无id 通知被接受时返回无主体 `202`、GET 和 DELETE 返回 `405`、 nghe 流的确认/通知/最终结果都携带订阅 id──

`code/main.py`thực hiện một máy chủ HTTP Streamable hiện đại và hữu hạn với thư viện tiêu chuẩn Python. Nó xác nhận nguồn gốc và tiêu đề gương, bỏ qua tiêu đề phiên họp bị xóa, trả về JSON cho các cuộc gọi bình thường, và chứng minh một tiêu đề hữu hạn `subscriptions/listen`SSE dòng chảy.

> `code/main.py`Sử dụng Python  tiêu chuẩn thư viện để thực hiện một hạn chế 现代的 Streamable HTTP 服务器──它校验 Origin 和镜像头,忽略已移除的会话头,普通调回 JSON,并演示一条有限的 `subscriptions/listen`SSE 流──

```bash
cd code
python3 main.py --probe
python3 -m unittest discover tests -v
```

Chuyến thăm dò kiểm tra:

- Nguồn gốc không hợp lệ bị từ chối;
  Trung文翻译: Quản xuất bất hợp pháp bị từ chối;
- phát hiện thành công mà không có ID phiên;
  Trung文翻译:无需会话 id 即可完成发现;
- `Mcp-Session-Id`và `Last-Event-ID`bị phớt lờ;
  Trung ngữ翻译:`Mcp-Session-Id`和 `Last-Event-ID`bị bỏ qua;
- Header không phù hợp trả lại `-32020`-
  Trung ngữ翻译:头不匹配返回 `-32020`-
- trả lại phiên bản không hỗ trợ `-32022`chính xác`supported`và `requested`dữ liệu;
  Trung ngữ翻译:不支持的版本返回 `-32022`Không có xác định`supported`和 `requested`số liệu;
- một thông báo không có id được chấp nhận trả về HTTP `202`Không có cơ thể;
  Trung文翻译:被接受的无 id 通知返回 HTTP `202`且无主体;
- GET và DELETE return `405`-
  中文翻译:GET 和 DELETE 返回 `405`-
- `subscriptions/listen`là một dòng phản hồi POST mà xác nhận, thông báo và kết quả cuối cùng của nó mang theo ID đăng ký của nó.
  Trung ngữ翻译:`subscriptions/listen`                                                                                                                                                                                                                                                              

## Chuyển nó đi.

Bài học này sẽ đi theo `outputs/skill-mcp-transport-migrator.md`Nó loại bỏ các phiên giao thức hiện đại, thêm xác nhận header-body, thay thế GET độc lập với `subscriptions/listen`, và giữ bất kỳ cây cầu di sản rõ ràng tách biệt.

> 本课产 出 `outputs/skill-mcp-transport-migrator.md`                                                                                                                                                                                                                                                              `subscriptions/listen`取代独立 GET,并让任何遗留桥接保持显眼隔离──

## Tập luyện bài tập

1. Tắt `Mcp-Method`từ một POST. xác nhận HTTP `400`và lỗi `-32020`- Tôi không biết.
   中文翻译: từ POST 中移除 `Mcp-Method` xác nhận HTTP `400`和错误 `-32020`
2. Gửi phiên bản tiêu đề và thân xác phù hợp `2027-01-01`. Tiếp tục xác nhận HTTP `400`, lỗi `-32022`, và dữ liệu chính xác `{"supported":["2026-07-28"],"requested":"2027-01-01"}`- Tôi không biết.
   Trung ngữ翻译:发送头与体一致的版本 `2027-01-01` xác nhận HTTP `400`、错误 `-32022`Và dữ liệu chính xác`{"supported":["2026-07-28"],"requested":"2027-01-01"}`
3. Hãy gửi một lính canh Base64`Mcp-Name`cho một URI tài nguyên không phải ASCII. xác nhận giá trị được giải mã được so sánh với `params.uri`- Tôi không biết.
   Trung文翻译:为非ASCII 资源 URI 发送 Base64 哨兵 `Mcp-Name`❖ xác nhận giá trị của giải mã sau`params.uri`- Không.
4. Phá vỡ dòng nghe hữu hạn trước khi phản ứng cuối cùng của nó, phát hành lại với một ID JSON-RPC mới và công cụ chỉnh sửa lại.
   Trung文翻译: 在最终响应前打断有限的听流――用新 JSON-RPC id 重新发发发并重新拉取工具――
5. Thêm một tay cầm dòng công việc rõ ràng vào công cụ ping. Kết nối nó với một đối tượng ủy quyền mà không sử dụng liên kết.
   Đưa ping 工具加一个显式工作流句柄── không cần phải kết nối亲和性, hãy buộc nó vào một chủ thể được ủy quyền──

## Từ khóa  Từ khóa nhanh chóng

| Term | Meaning | 中文术语 |
|------|---------|----------|
| stdio | Newline-delimited JSON-RPC over a client-launched subprocess | stdio 传输 |
| Streamable HTTP | Single endpoint where each modern message is a new POST | Streamable HTTP 传输 |
| Request-scoped SSE | POST response stream containing related notifications and final response | 请求级 SSE 流 |
| `subscriptions/listen` | Long-lived POST request for opted-in change notifications | 订阅监听请求 |
| Header mismatch | HTTP `400` and JSON-RPC `-32020` when mirrored headers disagree with body | 头不匹配错误 |
| Origin validation | DNS-rebinding defense for incoming connections, not authentication | Origin 校验（防 DNS 重绑定） |
| Explicit state handle | Application token passed as an ordinary argument instead of hidden session state | 显式状态句柄 |
| Legacy bridge | Separate earlier-era behavior kept only for compatibility | 遗留桥接 |

## Xem thêm 延伸阅读

- [MCP Transport Overview](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)
  Trung ngữ翻译:MCP 传输总览两种现代传输的权威入口
- [MCP stdio Transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)
  Trung文翻译:studio 传输的完整规范
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
  中文翻译:Streamable HTTP 的 POST-only 契约细节
- [MCP Subscriptions](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions)
  Trung ngữ翻译:`subscriptions/listen`订阅模式规范
- [MCP 2026-07-28 Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
  Trung ngữ翻译:2026-07-28 修订的完整变更清单(会话移除的官方说明)
