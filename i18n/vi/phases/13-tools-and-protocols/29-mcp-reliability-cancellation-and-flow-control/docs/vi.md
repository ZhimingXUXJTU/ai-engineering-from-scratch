# MCP Đán cậy, hủy bỏ và kiểm soát dòng chảy

> Một ID yêu cầu tương quan với một tin nhắn. Nó không làm cho một tác dụng phụ an toàn, ngăn chặn một công nhân, hoặc bảo vệ một dòng từ từ từ từ của người tiêu dùng.

> **【中文解读】**Ứng dụng ID chỉ chịu trách nhiệm liên quan thông tin: nó không thể làm cho tác dụng phụ trở nên an toàn, không thể dừng lại một công nhân, cũng không bảo vệ được dòng chảy không bị người tiêu dùng kéo dài.

> **【拓展：MCP→分布式系统工程】**Mỗi khái niệm xuất hiện trong đây 取消信号与传输绑定,完成/取消竞态、空+绝对双超时、等键、事务性发件箱、背压、动退避 đều là các bài học cổ điển của hệ thống phân tán.`tasks/cancel`面向持久任务──Phase 13 · 13(异步任务) là việc đặt trước trực tiếp của bài học.

>  **【前置】**学本课前请先掌握:Phase 13 · 09(MCP 传输:studio 与流通 HTTP 的差异)`tasks/cancel`(■)

**Type:** Build | **类型:** 动手实践
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lessons 09 and 13 | **前置知识:** Phase 13 · 09、13
**Time:** ~120 minutes | **时间:** 约 120 分钟

## Mục tiêu học tập

- Thực hiện tín hiệu hủy hiệu chính xác cho stdio và Streamable HTTP.
  Trung文翻译:为studio 和 Streamable HTTP 实现各自正确的取消信号──
- Giải quyết cuộc đua hoàn thành và hủy bỏ mà không gửi thông điệp sau khi hủy bỏ.
  Trung ngữ翻译:解决"完成与取消"的竞态,且在取消后不再发送消息.
- Tháo gỡ yêu cầu riêng biệt từ lâu dài `tasks/cancel`ngữ nghĩa.
  Trung文翻译:把请求取消与持久 `tasks/cancel`语义区分开――
- Xây dựng quyết định thử lại dựa trên tác dụng phụ và các khóa vô hiệu hóa rõ ràng.
  Trung ngữ翻译: dựa trên tác dụng phụ và biểu hiện等键构建重试决策──
- Giữ xếp hàng tiến bộ trong khi vẫn giữ lại các phản hồi cuối cùng.
  Trung ngữ翻译:给进度队列设界,同时保住最终响应──
- Khôi phục dòng chảy thông qua kết nối lại, tái nối, và backkoff nervous.
  Trung ngữ翻译:通过重连、权权重取和带动的退避恢复流──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**经典事故链:客户端调工具→服务器开工→进度到来→代理缓冲了流→客户端超时断开→服务器一毫秒后完成→客户端换了一个新的 JSON-RPC id 重试→变更执行两次. Mỗi bộ phận trong địa phương đều hoạt động đúng, hệ thống toàn diện thất bại. MCP chỉ quản lý thông điệp và truyền tải; thời gian ngân sách, kinh doanh 等等等等等等等等有队列重试分界类,持久任务状态,重连重策略.

Con đường hạnh phúc ẩn giấu những lỗi hệ thống phân tán đắt tiền nhất.

> 快乐路径(lucky path) chứa các lỗi hệ thống phân tán đắt tiền nhất.

Một client gọi một công cụ. máy chủ bắt đầu làm việc. tiến bộ đến. Một proxy buffer dòng. Client đạt đến thời gian và kết nối. máy chủ hoàn thành một millisecond sau đó. Client thử lại với một ID JSON-RPC mới. đột biến chạy hai lần.

Mỗi thành phần đã hành xử địa phương, hệ thống đã thất bại trên toàn cầu.

> Mỗi bộ phận đều hoạt động đúng, hệ thống đã thất bại trên toàn diện.

MCP xác định hành vi thông điệp và vận chuyển, nhưng ứng dụng của bạn vẫn sở hữu:

- ngân sách thời gian;
- sự bất lực kinh doanh;
- Các hàng rào giới hạn;
- phân loại thử nghiệm lại;
- trạng thái nhiệm vụ lâu dài;
- tái kết nối và tái điều chỉnh chính sách.

Bài học này xây dựng những quyết định đó thành một mô phỏng xác định.
Không có ổ cắm, ổ cắm, hoặc thất bại ngẫu nhiên.
Một thử nghiệm dây đồng bộ buộc hai khách hàng sổ cái để cạnh tranh
cho cùng một chìa khóa tự do.

## Ứng dụng hủy bỏ là giao thông cụ thể Ứng dụng hủy bỏ là giao thông được buộc

> **【中文解读】**意图在每个传输上都一样: khách hàng không còn cần một kết quả trên đường.`notifications/cancelled`通知(fire-and-forget, server does not return any JSON-RPC 响应);Streamable HTTP 上是直接关闭该请求自己的响应流(不要为普通 HTTP 请求 POST 取消通知,流关闭就是取消信号)  bên máy chủ:观察到断开后应停止工作、不得再为该请求发送消息; đối với yêu cầu chưa biết、已完成或无法安全停止可以忽略取消──注意服务器方向的取消很窄:studio上仅保留用于终止`subscriptions/listen`Xin hãy...

Ý định là giống nhau trên mọi vận chuyển: khách hàng không còn cần kết quả trong chuyến bay.

> 意图在每个传输上都一样: khách hàng không còn cần một kết quả trên đường.

### Đọc tập phim

stdio sử dụng một kênh hai chiều được chia sẻ.

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/cancelled",
  "params": {
    "requestId": 41,
    "reason": "User closed the operation"
  }
}
```

Thông báo là bỏ qua và quên. máy chủ không phát ra phản ứng JSON-RPC cho nó.

> Thông báo này được phát hành sau khi bị quên, máy chủ sẽ không phát hành bất kỳ phản ứng JSON-RPC nào cho nó.

Các máy chủ nên ngừng làm việc, giải phóng tài nguyên và tránh gửi phản hồi cho yêu cầu bị hủy. Nó có thể bỏ qua việc hủy bỏ khi yêu cầu không được biết, đã hoàn thành hoặc không thể dừng lại một cách an toàn.

Các thông báo hủy bỏ bị sai, không rõ, và đã hoàn thành bị bỏ qua.

>  hình dạng 未知和已完成的取消通知 一律忽略 把这些竞争态变成新错误只会产生更多竞争态

### HTTPS được phát trực tuyến

Modern Streamable HTTP cung cấp cho mỗi yêu cầu phản ứng HTTP riêng hoặc dòng phản ứng SSE. Khách hàng hủy bằng cách đóng dòng phản ứng yêu cầu đó.

> 现代 Streamable HTTP 给每个请求独立的 HTTP 响应或 SSE 响应流,客户端通过关闭该请求的响应流来取消――不要为普通的 HTTP 请求 POST`notifications/cancelled`流的关闭就是取消信号──服务器 một khi quan sát được bị gián đoạn,就应停止工作,并且不得再发送任何消息──

Đừng đăng `notifications/cancelled`cho một yêu cầu HTTP thông thường. Tiết kiệm dòng là tín hiệu hủy.

Khi máy chủ nhận thấy sự ngắt kết nối, nó nên ngừng hoạt động và không được gửi thêm thông điệp cho yêu cầu đó.

### Việc hủy được máy chủ gửi là hạn chế

Một máy chủ không sử dụng `notifications/cancelled`để hủy các cuộc gọi khách hàng tùy ý. Trong studio, việc hủy server được dành riêng cho việc chấm dứt một`subscriptions/listen`giữ đường đi đó tách biệt với việc hủy đơn yêu cầu của khách hàng thông thường.

## Tháo hủy là một cuộc đua.

> **【中文解读】**两种事件顺序都合法:取消先到服务器标记取消,worker 随后完成,服务器压掉响应;完成先到工作者 提交结果,服务器发出响应,迟到的取消被忽视――网络延迟决定双方都无法证明对方先见到哪个事件,所以客户端也必须忽视自己已放弃请求的迟到响应――本课的`RequestCoordinator`Đối với mỗi yêu cầu chỉ tồn tại một trạng thái cuối cùng:`complete()`Không trả lại phản ứng, đã hoàn thành sau khi đã quá muộn để xóa cũng không thay đổi ghi chép.

Hai lệnh cho sự kiện đều có giá trị.

> 两种事件顺序 đều hợp pháp.

### Thủy bỏ thắng.

```text
request starts
client sends cancellation signal
server marks request cancelled
worker reaches completion
server suppresses the response
```

### Kết thúc thắng.

```text
request starts
worker commits the result
server sends the response
cancellation arrives late
server ignores the late notification
```

Khách hàng cũng phải bỏ qua phản ứng muộn cho một yêu cầu mà nó đã bỏ rơi.

> 客户端 cũng phải bỏ qua bản thân đã từ bỏ yêu cầu của mình đến thời điểm đáp ứng. 网络延迟 có nghĩa là cả hai bên không thể chứng minh nhau trước khi quan sát sự kiện nào.

```figure
mcp-reliability-race
```

Bài học là `RequestCoordinator`lưu trữ một trạng thái cuối cùng. `complete()`không trả lời sau khi hủy bỏ. Một hủy bỏ muộn không thể thay đổi một hồ sơ đã hoàn thành.

## Thời gian mất 2 giờ.

> **【中文解读】**Chỉ có một máy tính tính không hoạt động là không đủ. Để đặt hai giới hạn trên:空超时 (không có hoạt động) và最大超时 (không có hoạt động) kể từ khi yêu cầu bắt đầu.

Một bộ hẹn giờ không hoạt động duy nhất không đủ.

Sử dụng hai giới hạn:

1. **Idle timeout.**Thời gian yêu cầu có thể không tạo ra hoạt động hữu ích.
2. **Maximum timeout.**Ngân sách tuyệt đối của đồng hồ tường từ khi yêu cầu bắt đầu.

Tiến bộ có thể đặt lại đồng hồ không hoạt động.

> 进度 có thể đặt lại空时钟, nhưng không thể loại bỏ thời hạn tối đa.

```text
start: 0 ms
progress: 400 ms
progress: 800 ms
progress: 1200 ms
idle timeout: 500 ms
maximum timeout: 2000 ms
```

Tại 1500 ms, yêu cầu vẫn hoạt động vì tiến trình mới nhất chỉ là 300 ms. Tại 2000 ms, thời hạn tối đa hủy nó ngay cả khi một sự kiện tiến trình khác đến vào năm 1999 ms.

Tiến bộ là tùy chọn. Một máy chủ có thể chấp nhận một token tiến bộ và không phát ra cập nhật. Không bao giờ biến sự hiện diện của một token thành một thời gian nghỉ vô hạn.

Giá trị tiến bộ MCP phải tăng lên. Thông báo dừng lại sau khi hoàn thành hoặc hủy bỏ.

## Đơn xin hủy không được `tasks/cancel` Xin hãy xóa đi `tasks/cancel`

> **【中文解读】**两种机制面对不同的生命周期:请求取消针对一条在路 RPC (studio 发通知、HTTP 关流), thành công có nghĩa là "customer đã từ bỏ yêu cầu, máy chủ nên dừng nếu thích hợp";`tasks/cancel`针对一个持久任务,是普通 MCP 请求,成功含义只是"服务器确认取消意图"不证明工人已停止,任务可能保持 `working`Cho đến khi một người lao động  kiểm tra điểm quan sát được dấu hiệu, công việc cũng có thể được hoàn thành trước khi đó kiểm tra điểm. Vì vậy, HTTP  kết nối đóng cửa khi không xóa dài Thức năng  trạng thái: tạo Thức năng lý do là chu kỳ cuộc sống của nó dài hơn so với đơn yêu cầu và đơn kết nối.

Những cơ chế này giải quyết những cuộc sống khác nhau.

| Mechanism | Target | Signal | What success means |
|-----------|--------|--------|--------------------|
| Request cancellation on stdio | One in-flight RPC | `notifications/cancelled` | Client abandoned the request; server should stop if practical |
| Request cancellation on HTTP | One in-flight response stream | Close the stream | Client abandoned the request; server should stop if practical |
| `tasks/cancel` | One durable Task | Ordinary MCP request | Server acknowledged cancellation intent |

Một người thành công`tasks/cancel`kết quả không chứng minh người lao động đã dừng lại.`working`cho đến khi một điểm kiểm soát người lao động quan sát cờ.

> `tasks/cancel`Kết quả thành công không chứng minh người lao động đã dừng lại.`working`, cho đến khi một công nhân kiểm tra điểm quan sát để loại bỏ dấu hiệu; công việc cũng có thể được hoàn thành trước khi đó kiểm tra điểm.

Đừng xóa trạng thái nhiệm vụ lâu dài khi kết nối HTTP đóng. Lý do để tạo Task là vòng đời của nó tồn tại lâu hơn một yêu cầu và một kết nối.

> HTTP  kết nối 关闭时不要清除持久任务状态――创建任务的原因是它的生命周期比单个请求和单个连接都长――

## Một ID JSON-RPC mới không là bất khả năng .

> **【中文解读】**JSON-RPC id chỉ liên quan đến yêu cầu và phản ứng, không xác định hoạt động kinh doanh. Khách hàng sử dụng id 41 gửi khoản thanh toán, mất phản ứng.

Các ID JSON-RPC tương quan các yêu cầu và phản hồi.

Giả sử một khách hàng gửi một khoản phí với id `41`, mất phản ứng, và thử lại với id `42`Máy chủ nhìn thấy hai tin nhắn khác nhau. Không có khóa ứng dụng, nó không thể biết chúng đại diện cho một thanh toán.

Một khóa idempotency xác định ý định kinh doanh:

```json
{
  "name": "charge_account",
  "arguments": {
    "account": "acct-7",
    "cents": 1200,
    "idempotencyKey": "checkout-7"
  }
}
```

Các máy chủ lưu trữ:

- Chìa khóa;
- Một dấu vân tay của các lý lẽ hoạt động;
- kết quả đã cam kết.

Cùng một khóa và cùng một lập luận trả lại kết quả được lưu trữ. cùng một khóa với các lập luận khác nhau được từ chối. Điều này ngăn chặn việc tái sử dụng khóa ngẫu nhiên từ biến đổi một hoạt động kinh doanh khác.

>  server storage: key 操作参数的纹纹、已提交的结果──同键同参返回存储的结果;同键不同参被拒绝防止键被误用到另一个业务操作──同键同参返回存储的结果;同键不同参被拒绝防止键被误用到另一个业务操作──同键同参返回存储的结果.

>  **【类比】**等键像高铁购票的"订单号"──你在12306 下单后支付超时,重新发发支付使用的是同一个订单号系统认出"这单已经过票了",直接把原来的票给你,而不是再扣一次款卖你第二张──JSON-RPC id 则像每次点击生成的会话流水号:换个流水号重试,售票系统就当成全新购买──

### Biên giới sổ cái phải là nguyên tử và bền vững.

> **【中文解读】**"查键→执行变更→存结果" chuỗi này không an toàn: hai công nhân đều có thể quan sát sự thiếu hụt của khóa và đều có thể thực hiện thay đổi; hiệu ứng sau đó, trước khi lưu trữ bị sụp đổ cũng sẽ tạo ra những khác biệt tương tự trong thử nghiệm tái tạo.`BEGIN IMMEDIATE`Đặt kiểm tra khóa, mô phỏng hiệu ứng kinh doanh, tính toán thực thi và lưu trữ kết quả vào một giao dịch Hai sổ cái độc lập kết nối với cùng một khóa cạnh tranh chỉ quan sát một kết quả đã gửi và một lần thực hiện; đóng lại sổ cái ghi lại vẫn còn. Tất cả các giá trị trả lại đều từ kho lưu trữ JSON tái tạo (được xây dựng lại) bản sao phòng thủ), người dùng sẽ không bao giờ có thể nhận được các đối tượng thay đổi bên trong sổ cái. Biên giới quan trọng: hiệu quả kinh doanh mô phỏng là một bộ phận kiểm toán và kiểm toán trong cùng một SQLite, thực sự hỗ trợ, bộ phận hoặc API bên ngoài. Người dùng sẽ không được sử dụng bởi vì đã viết một bảng tính địa phương về nguyên tử.

Dòng này không an toàn:

```text
check key
run mutation
store result
```

Hai công nhân đều có thể quan sát một chìa khóa bị mất và cả hai đều chạy đột biến.
sau hiệu ứng nhưng trước khi cửa hàng tạo ra sự mơ hồ tương tự khi thử lại.

Bài học sử dụng một sổ cái SQLite được hỗ trợ bằng tệp. `BEGIN IMMEDIATE`serializes các
kiểm tra khóa, hiệu ứng kinh doanh mô phỏng, đếm tính thực hiện và kết quả được lưu trữ vào
hai liên kết sổ cái độc lập chạy cùng một khóa
Do đó, hãy quan sát một kết quả đã cam kết và một hành động.
sổ cái giữ hồ sơ đó.

Mỗi giá trị trả lại được tái cấu trúc từ JSON được lưu trữ. Người gọi không bao giờ nhận được
đối tượng thay đổi được giữ trong sổ cái, do đó thay đổi một từ điển trả lại không thể
kết quả phát lại sau đó bị tham nhũng.

Tác dụng kinh doanh của máy mô phỏng là máy tính nhận và thực thi bên trong
giao dịch SQLite. Một thanh toán thực, triển khai, hoặc API bên ngoài gọi là
Không phải chỉ bằng cách viết một bảng địa phương.
giao dịch cơ sở dữ liệu chung, hộp thư gửi giao dịch hoặc nhà cung cấp nguồn lên
Một khóa quá trình đơn độc không bảo vệ
nhiều bản sao hoặc sống sót sau khi khởi động lại.

### Thử lại matrix

> **【中文解读】**实现重试之前先分类. 安全类. 不安全类. 不安全类. 不安全类. 不安全类. 不安全类. 不业务重重的变更.`readOnlyHint``idempotentHint`Các công cụ này luôn là một sự thật đáng tin cậy.

Lập mục các thử nghiệm lại trước khi thực hiện chúng.

| Class | Example | Retry rule |
|------|---------|------------|
| Safe | Deterministic read with no side effect | Retry with a new JSON-RPC id after the failure boundary is understood |
| Conditional | Mutation with a durable idempotency key | Retry with the same key and identical arguments |
| Unsafe | Mutation without business deduplication | Do not retry automatically; reconcile first |

Các chú thích công cụ như `readOnlyHint`và `idempotentHint`hợp đồng ứng dụng và việc triển khai máy chủ quyết định an toàn thử lại.

## Cơn áp lực là một phần của sự đúng đắn.

> **【中文解读】**SSE sản xuất tốc độ phát triển có thể nhanh hơn tốc độ tiêu thụ của khách hàng, đại lý hoặc mạng, không giới hạn hàng ngũ sẽ biến "sự chậm" thành "sự mất trí nhớ"。

Một nhà sản xuất SSE có thể tạo ra tiến bộ nhanh hơn so với một khách hàng, đại diện hoặc mạng có thể tiêu thụ nó.

Sử dụng một hàng giới hạn và xác định những gì có thể bị mất.

Tiến bộ có thể thay thế. Giá trị tiến bộ sau này thay thế giá trị trước đó cho cùng một token.

Các khóa học buffer áp dụng chính sách này:

1. Tham gia tiến bộ lân cận cho cùng một dấu hiệu.
2. Thả tiến bộ lâu đời nhất khi đạt được năng lực.
3. Đánh dấu dòng chảy cần phải được sửa chữa.
4. Bảo vệ phản ứng cuối cùng.
5. Từ chối một trạng thái mà việc bảo tồn phản ứng cuối cùng sẽ đòi hỏi phải bỏ lại một phản ứng cuối cùng khác.

Đây là một tổn thất bị giới hạn với sự phục hồi rõ ràng.

> Đó là một sự mất mát và một sự phục hồi rõ ràng.

### Đảm bảo quyền lực.

Một máy chủ có thể truyền thông đúng trong khi một đại diện ngược lưu trữ các sự kiện trong một bộ đệm.

Để nhận được câu trả lời của SSE, gửi:

```http
Content-Type: text/event-stream
Cache-Control: no-cache
X-Accel-Buffering: no
```

Các thông số HTTP Streamable 2026 khuyến cáo `X-Accel-Buffering: no`để các proxy tương thích đưa ra các sự kiện ngay lập tức.

Đối với các dòng chảy dài thời gian yên tĩnh, thường xuyên phát ra một bình luận của SSE:

```text
:
```

Khách hàng bỏ qua các dòng bình luận, người trung gian thấy lưu lượng truy cập và ít có khả năng đóng kết nối vô hiệu.

Keeppalive không phải là tiến bộ. Đừng đặt lại thời gian trễ semantic của một hoạt động chỉ vì một bình luận vận chuyển đã đến.

## Kết nối lại có nghĩa là tái nối.

> **【中文解读】**现代 Streamable HTTP không hỗ trợ qua `Last-Event-ID`Khôi phục SSE.`subscriptions/listen`流断开后的五步恢复: sử dụng mã JSON-RPC mới 开新监听请求;恢复期望的订阅过器; từ phương pháp quyền lực lấy lại các công cụ / tài nguyên / yêu cầu / nhiệm vụ bị ảnh hưởng; theo định nghĩa định nghĩa đối với trạng thái ứng dụng để重重;绝不因为丢了响应就重放不安全的变化―― ví dụ kế hoạch phục hồi rõ ràng`sendLastEventId`设为错并列出重取的资源──

HTTP Streamable hiện đại không hỗ trợ SSE có thể được nối lại thông qua `Last-Event-ID`- Tôi không biết.

Sau một`subscriptions/listen`dòng chảy giảm:

1. Mở yêu cầu nghe mới với ID JSON-RPC mới.
2. Khôi phục bộ lọc đăng ký mong muốn.
3. Phục hồi các công cụ, tài nguyên, lời khuyên hoặc nhiệm vụ bị ảnh hưởng từ các phương pháp có thẩm quyền.
4. Tăng độ ứng dụng bằng các định danh ổn định.
5. Đừng lặp lại một đột biến không an toàn chỉ vì phản ứng của nó đã mất.

Kế hoạch phục hồi mẫu đã xác định rõ ràng `sendLastEventId`để giả và liệt kê các nguồn lực để sửa đổi.

### - Đưa một con bò quay lại. - Đưa một con bò quay lại.

Nếu 10.000 khách hàng kết nối lại trong chính xác một giây, máy chủ phục hồi lại thất bại.

> Nếu mười ngàn khách hàng được nối lại trong cùng một giây, máy chủ đang phục hồi sẽ bị lật lại.

Sử dụng backkoff theo hàm số cao với jitter và a cap. Bài học tính toán jitter xác định từ ID khách hàng và số thử nghiệm để các bài kiểm tra vẫn có thể tái tạo:

```text
attempt 0: up to 250 ms
attempt 1: up to 500 ms
attempt 2: up to 1000 ms
...
cap: 8000 ms
```

Việc sản xuất có thể sử dụng mật mã an toàn hoặc thời gian chạy ngẫu nhiên.

## Hãy xây dựng nó.

> **【中文解读】** `code/main.py`实现五个小组件:`RequestCoordinator`(Trong thời gian yêu cầu, đơn调度, chính xác của studio/HTTP 取消信号,忽略非法取消,取消与完成的终态竞争的显式化,服务器方向取消只保留给studio 订阅);`MutationLedger`(bằng chứng hai ID JSON-RPC sẽ thực hiện hai lần  SQLite các vấn đề liên quan đến kiểm tra/ hiệu quả/ tính toán/ gửi 跨连接去重、同键异参拒、防御性副本、重开账本记录仍在);`DurableTaskService`( xác nhận取消请求 nhưng giữ `working`cho đến khi người lao động kiểm tra điểm, biểu hiện xác nhận không là kết thúc);`BoundedSseBuffer`(pressure under合并或丢失进度、标记需要权重取、绝不动最终响应); phục hồi trợ giúp(

`code/main.py`xây dựng năm thành phần độ tin cậy nhỏ.

### `RequestCoordinator`

- bắt đầu yêu cầu trên chuyến bay với thời hạn không hoạt động và thời hạn tối đa;
- phát hành thông báo tiến bộ đơn giản;
- tạo ra tín hiệu hủy bỏ stdio hoặc HTTP đúng;
- bỏ qua các thông báo hủy bỏ không hợp lệ;
- làm rõ ràng các cuộc đua chấm dứt và hủy bỏ;
- lưu trữ hủy được máy chủ gửi cho thuê bao studio.

### `MutationLedger`

- chứng minh rằng hai ID JSON-RPC thực hiện hai lần mà không có khóa kinh doanh;
- sử dụng giao dịch SQLite được hỗ trợ bằng tệp để kiểm tra khóa, hiệu ứng mô phỏng,
  đếm tính thực thi và cam kết kết kết quả;
- Dedule các lập luận phù hợp dưới một khóa idempotency trên các lập luận độc lập
  kết nối sổ cái;
- Thử loại bỏ một khóa được tái sử dụng với các lập luận khác nhau;
- trả lại bản sao phòng thủ và bảo tồn các hồ sơ đã bị phạm tội trong quá trình mở lại.

### `DurableTaskService`

- chấp nhận yêu cầu hủy bỏ;
- giữ nhiệm vụ `working`cho đến một trạm kiểm soát lao động;
- chứng minh tại sao việc công nhận không phải là tình trạng cuối cùng.

### `BoundedSseBuffer`

- kết hợp hoặc giảm tiến độ dưới áp lực;
- ghi lại rằng cần phải có thẩm quyền sửa đổi;
- không bao giờ làm giảm phản ứng cuối cùng.

### Những người giúp đỡ phục hồi

- trả lại các tiêu đề SSE an toàn bằng đại diện và các ý kiến giữ lại;
- tạo ra một kế hoạch kết nối lại và tái nối;
- Các thử nghiệm spread với số lượng số lượng đằng sau và jitter.

## Hãy sử dụng nó. Hãy học cách sử dụng nó.

Từ nguồn kho:

```bash
cd phases/13-tools-and-protocols/29-mcp-reliability-cancellation-and-flow-control/code
python3 main.py
python3 -m unittest discover tests -v
```

Demo chạy cả hai bên của cuộc đua trung tâm, thực hiện một giao dịch
đột biến bị sao chép trong một sổ cái tạm thời được hỗ trợ bằng tệp, quá tải một
bộ buffer tiến bộ, và cho thấy một nhiệm vụ lâu dài chuyển từ hủy bỏ được xác nhận
cho việc hủy bỏ được công nhân quan sát.

## - Bác sĩ, tôi đã làm việc trong phòng thí nghiệm tương tác.

Thực hiện bốn sự kiện đặt hàng mà không thêm ngủ.

> Không thêm bất kỳ giấc ngủ nào, chạy bốn loại sự kiện theo thứ tự: A trước取消后 hoàn thành; B trước trước hoàn thành; B后送达取消; C trong mỗi khoảng thời gian trống trước phát triển tiến bộ và vượt quá thời hạn tối đa; D trong Streamable HTTP 上关闭其响应流;; Mỗi cảnh quay ghi lại: yêu cầu kết thúc có phải có phản ứng cuối cùng; 线上发射的信号取消; 信号客户端应忽略哪个事件;; 再把 D 换成工作室操作完全相同,取消信号必须改变;;

1. Đặt ra yêu cầu`A`, hủy nó, sau đó gọi `complete()`- Tôi không biết.
2. Đặt ra yêu cầu`B`, hoàn thành nó, sau đó chuyển trả hủy.
3. Đặt ra yêu cầu`C`, phát triển trước mỗi thời hạn trống, sau đó vượt quá thời hạn tối đa.
4. Đặt ra yêu cầu`D`qua Streamable HTTP và đóng dòng phản ứng của nó.

Lưu ý cho mỗi kịch bản:

- trạng thái yêu cầu cuối cùng;
- có phản ứng cuối cùng hay không;
- tín hiệu hủy bỏ được đặt trên dây;
- sự kiện mà khách hàng nên bỏ qua.

Vậy hãy thay đổi`D`Hành động này giống nhau, nhưng tín hiệu hủy sẽ thay đổi.

## Phòng thí nghiệm tập luyện.

Thêm một `reserve_inventory`đột biến đến `MutationLedger`- Tôi không biết.

>  Đưa `MutationLedger`Một người`reserve_inventory`变更──十条要求覆盖:键绑定 SKU/数量/租户/操作名;同键同参返回首次预约;改数则失败且不再预约;已提交但丢响应可按键对账;结果无含密与付费数据;客户端没给键就禁自动重试;模拟订阅断断后先重取库存记录再决;两个账户连接在屏障上并发钥匙提交断言只有一次预约;改变首次返回预约对象,重放钥匙,证明存储结果;关闭重账文件后按键对账.保持诚实: nếu thư viện tồn tại trong một dịch vụ khác,说明 nó chấp nhận một 键 tương tự,还是需要事务所提交地址到桥接远端效果.

Yêu cầu:

1. Chìa khóa liên kết SKU, số lượng, người thuê và tên hoạt động.
2. Một lần nữa với cùng một khóa và cùng một lập luận trả lại đặt phòng đầu tiên.
3. Một lần thử lại với số lượng thay đổi thất bại mà không có một dự phòng khác.
4. Một hành quyết đã phạm nhưng đã mất phản ứng của nó có thể được hòa giải bằng chìa khóa.
5. Kết quả không ghi lại dữ liệu bí mật hoặc thanh toán.
6. Lần thử lại tự động bị vô hiệu hóa khi khách hàng không cung cấp chìa khóa.
7. Thêm một dấu chấm đăng ký mô phỏng và chỉnh lại hồ sơ hàng tồn kho trước khi quyết định làm gì tiếp theo.
8. Bắt đầu hai kết nối sổ cái tại một rào cản và gửi cùng một khóa
   - Đề xuất một việc đặt phòng đã được thực hiện.
9. Thay đổi đối tượng đặt phòng đầu tiên trở lại.
   kết quả được lưu trữ không thay đổi.
10. Đóng và mở lại tập tin sổ cái, sau đó hòa hợp đặt chỗ bằng khóa.

Để phòng thí nghiệm trung thực: nếu hàng tồn kho sống trong một dịch vụ khác, giải thích xem
dịch vụ đó chấp nhận cùng một khóa miễn quyền hoặc một hộp thư giao dịch
cầu, người địa phương cam kết với hiệu ứng từ xa.

## Thuật vật được vận chuyển.

`outputs/skill-mcp-reliability-reviewer.md`là một kỹ năng đánh giá độ tin cậy bằng phẳng. Cho nó một hoạt động MCP, vận tải, chính sách thời gian, hành vi thử lại, chính sách xếp hàng và kế hoạch phục hồi. Nó trả lại một bảng đua, phân loại thử lại, ranh giới bất khả năng, kiểm tra kiểm soát dòng chảy và các thiết bị thất bại.

> `outputs/skill-mcp-reliability-reviewer.md`là một kỹ năng đánh giá độ tin cậy: cho nó một MCP hoạt động, truyền thông cách, siêu thời gian chiến lược, tái thử hành vi, chiến lược hàng ngũ và kế hoạch phục hồi, nó trả lại biểu thức cạnh tranh, tái thử phân loại, và các biên giới, lưu lượng kiểm tra và thất bại cố định.

## Hãy kiểm tra.

> **【中文解读】**验收清单逐条过:studio 取消发通知且不收响应;HTTP 取消关流且不发取消 POST;先取消后完成压掉最终响应;先完成后取消保留响应并忽略迟到取消;进度能重置空超时但不能动最大时;只换新 JSON-RPC id sẽ再次执行变更;同键与参与双连接并发竞争只执行一次;已提交记录可重复,重复返回防御性开复;改回对象不变存储结果;有界缓冲不超容量且保住最终响应;连接新请求、不发`Last-Event-ID`、重取受影响状态;`tasks/cancel`确认后 任务 保持非终态直到工人 观察到它──

Bài học hoàn thành khi những câu nói sau đây là đúng:

- stdio hủy gửi `notifications/cancelled`và không nhận được bất cứ phản hồi nào.
- Streamable HTTP hủy đóng dòng yêu cầu và không gửi POST hủy.
- Tháo trước khi hoàn thành sẽ ngăn chặn phản ứng cuối cùng.
- Complete before cancellation bảo vệ phản ứng và bỏ qua việc hủy bỏ muộn.
- Tiến bộ có thể đặt lại thời gian không hoạt động nhưng không bao giờ là thời gian tối đa.
- Một ID JSON-RPC mới đơn độc thực hiện đột biến một lần nữa.
- Một khóa idempotency và các lập luận giống nhau thực hiện một lần trong một cùng lúc
  Cuộc đua hai kết nối.
- Một bản ghi đã bị kết tội tồn tại khi mở lại và tái phát trả lại bản sao phòng thủ.
- Việc biến đổi một kết quả trả lại không thể thay đổi kết quả được lưu trữ.
- Bơf đệm bị giới hạn vẫn nằm trong dung lượng và giữ lại phản ứng cuối cùng.
- Reconnect sử dụng yêu cầu mới, không gửi `Last-Event-ID`, và tái định vị trạng thái bị ảnh hưởng.
- `tasks/cancel`sự thừa nhận để lại nhiệm vụ không kết thúc cho đến khi người lao động thực hiện nó.

## Các chế độ sản xuất thất bại

> Các tác phẩm có thể được xem xét trong các bài viết khác nhau. Các tác phẩm có thể được xem xét trong các bài viết khác nhau.

| Failure | Observable symptom | Correct response |
|---------|--------------------|------------------|
| HTTP client POSTs cancellation notification | Server and client disagree about request lifetime | Close the request's SSE response stream |
| Server responds after accepted cancellation | Client receives an unusable late result | Stop work and suppress further messages when cancellation wins |
| Progress resets every deadline | Hung work survives forever | Keep a separate absolute maximum timeout |
| New RPC id treated as deduplication | Charge, deployment, or deletion runs twice | Add a durable application idempotency key |
| Key check and effect are separate | Concurrent workers both observe a missing key | Commit key claim, effect record, and result atomically |
| In-memory ledger used across replicas | Restart or another worker forgets prior commits | Use shared durable storage or upstream idempotency |
| Stored mutable result returned directly | Caller mutation corrupts later replays | Serialize committed results and return defensive copies |
| Key reused with changed arguments | One key aliases two business intents | Store and compare an argument fingerprint |
| Unbounded progress queue | Memory rises with a slow consumer | Coalesce and drop replaceable progress within a bound |
| Final response dropped under pressure | Client cannot know the request outcome | Reserve capacity or evict progress, never the final response |
| Proxy buffers SSE | Progress arrives in bursts or after timeout | Disable buffering and configure compatible proxy timeouts |
| `Last-Event-ID` assumed | Client resumes from state the server does not support | Reconnect with a new request and refetch |
| Every client reconnects immediately | Recovery creates another outage | Use capped exponential backoff with jitter |
| Task ack treated as final cancellation | Worker keeps running after UI says stopped | Poll the Task until a terminal status |

## Kết nối Capstone.

Các thiết bị hệ sinh thái cần phải xem độ tin cậy như là bằng chứng thực hiện, chứ không phải là một đoạn trong một sơ đồ kiến trúc.

> 工具生态毕业项目应视可靠性为可执行证据,而不是构建中的一段文字. 要求工件: mỗi loại truyền tải một bản ghi hủy竞争态记录, mỗi bản ghi lại bị lộ biến đổi, mỗi bản ghi lại bị lộ biến đổi, 等键记录与失配配件, cùng键并发记录,重新开检,别名检查,有界缓冲过载结果,反向代理 SSE 头和空策略,点名权重取方法重连接, 时代任务的持久任务 删踪.

Cần những vật liệu này:

- Một bản sao cuộc đua hủy bỏ cho mỗi chuyến vận chuyển;
- một bàn thử nghiệm lại cho mỗi đột biến được phát hiện;
- một hồ sơ khóa bất khả năng và thiết bị không phù hợp;
- Một bản sao cùng một khóa, kiểm tra mở lại và kiểm tra tên gọi đột biến;
- kết quả quá tải buffer giới hạn;
- Các tiêu đề SSE sao ngược và chính sách không hoạt động;
- một kế hoạch kết nối lại nêu tên các phương pháp tái trang bị xác thực;
- một dấu vết hủy bỏ Task lâu dài khi đá cuối sử dụng Tasks.

Một yêu cầu xanh trong một quy trình địa phương chỉ chứng minh con đường hạnh phúc. Bạch đá cuối sẵn sàng sản xuất khi mất phản ứng, hủy bỏ muộn, người tiêu thụ chậm và kết nối lại đàn có kết quả xác định.

## Từ khóa  Keyword

| Term | Meaning |
|------|---------|
| Request cancellation | Abandonment of one in-flight MCP request |
| Cancellation race | Competition between terminal completion and cancellation events |
| Idle timeout | Limit since the last useful request activity |
| Maximum timeout | Absolute limit from request start, unaffected by progress |
| Idempotency key | Application identifier that deduplicates one business intent |
| Atomic ledger | Durable boundary that commits the key claim, effect record, and result as one unit |
| Backpressure | Control applied when producers outpace consumers |
| Progress coalescing | Replacing older progress with a newer authoritative value |
| Refetch | Reading current state again after a stream gap |
| Jitter | Deliberate variation that spreads retries across time |

## Xem thêm 延伸阅读

- [MCP Cancellation](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/cancellation)
- [MCP Progress](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/progress)
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [MCP Tasks Extension](https://tasks.extensions.modelcontextprotocol.io/specification/draft/tasks)
