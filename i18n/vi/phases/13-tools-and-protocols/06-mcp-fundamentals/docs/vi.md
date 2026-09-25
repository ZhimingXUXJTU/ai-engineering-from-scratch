# MCP Basic: Requests without state và JSON-RPC

> MCP hiện đại không có cú tay và không có phiên giao thức. Mỗi yêu cầu phải chứa đủ siêu dữ liệu để được hiểu, ủy quyền, định tuyến và thử lại một mình.

> **【中文解读】**现代 MCP 没有握手,也没有协议会话―― mỗi yêu cầu phải mang đủ dữ liệu từ bản thân để được hiểu biết độc lập, cấp quyền, đường dẫn và thử lại―― đây là 2026-07-28 规范相对旧版(2025-11-25 及更早的初始化 握手模型)

> **【拓展：MCP→协议演进时间线】**MCP bởi Anthropic 于 2024 年 11 月首发,现由 Linux 基金会下的 Agentic AI Foundation 管理。旧版(到 2025-11-25 为止) là mô hình vòng đời ba giai đoạn của "connect → initialize 握手 →操作";2026-07-28 版把协议核心改为无状态:每个请求在`params._meta`里自带协议版本、客户端能力与身份,`initialize`降级为旧版兼容路径──本课是这个 MCP 系列的基基,后续 07(服务器) 、08(客户端) 都基于这个无状态模型──

>  **【前置】**Học本节前请先掌握:(1) giai đoạn 13 · 01-05工具接口、函数调用、Schema 设计;(2) JSON-RPC 2.0 基础(请求/响应/通知 三种信封);(3) đối với phiên bản cũ của MCP bắt đầu 握手有整体认识(本课会解释为何它被废弃为兼容分支)

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lessons 01 through 05 | **前置知识:** Phase 13, Lessons 01 through 05
**Time:** ~55 minutes | **时间:** ~55 分钟

## Mục tiêu học tập

- Sự khác biệt giữa các tính năng máy chủ của MCP và các tính năng bên khách hàng.
  Trung ngữ翻译:区分 MCP的服务器原语与客户端特性──
- Xây dựng các yêu cầu và phản hồi JSON-RPC 2.0 hợp lệ cho MCP `2026-07-28`- Tôi không biết.
  中文翻译:为 MCP `2026-07-28`构建合法的 JSON-RPC 2.0 Ứng dụng và phản ứng
- Thêm phiên bản giao thức, khả năng của khách hàng và danh tính khách hàng vào mỗi yêu cầu.
  Trung ngữ翻译:为每请求附加协议版本、客户端能力和客户端身份──
- Sử dụng `server/discover`và xử lý `UnsupportedProtocolVersionError`Không bắt tay.
  Trung ngữ翻译: 在无握手的前提下使用 `server/discover`并 xử lý `UnsupportedProtocolVersionError`
- Theo dõi một yêu cầu độc lập từ xác nhận thông qua kết quả hoàn chỉnh.
  Trung ngữ翻译: theo dõi một yêu cầu độc lập từ trường học đến kết quả hoàn chỉnh.

## Vấn đề  vấn đề giới thiệu

Một máy chủ MCP có thể nhận được hai yêu cầu liên tiếp từ các khách hàng khác nhau, với khả năng khác nhau, trên cùng một quy trình hoặc nhân viên HTTP. Nếu máy chủ nhớ những gì yêu cầu trước đó đã tuyên bố, nó có thể áp dụng các quyền sai hoặc trả lại hình dạng dây sai.

> Một máy chủ MCP có thể nhận được hai yêu cầu từ các khách hàng khác nhau trong cùng một quá trình hoặc nhân viên HTTP sau đó, với khả năng khác nhau. Nếu máy chủ nhớ được một yêu cầu trên tuyên bố gì, thì có thể sử dụng quyền sai lầm, hoặc trả lại định dạng đường sai lầm.

MCP `2026-07-28`Các máy chủ phải quyết định cách xử lý yêu cầu hiện tại từ yêu cầu hiện tại, chứ không phải từ lịch sử kết nối.

> MCP `2026-07-28`消除了这种差义──协议核心是无状态──服务器 phải chỉ dựa trên "giải hành hiện tại này" để tự quyết định cách xử lý nó, chứ không phải dựa trên lịch sử kết nối──

Điều này thay đổi mô hình tâm lý. chuỗi cũ là kết nối đầu tiên, bắt tay thứ hai, hoạt động thứ ba.

> Điều này đã thay đổi mô hình tâm trí.

1. Khách hàng gửi một yêu cầu tự mô tả.
   Trung ngữ翻译:客户端发送一个自描述的请求──
2. Máy chủ xác nhận phiên bản và khả năng của yêu cầu đó.
   Trung ngữ翻译:服务器校验该请求自带的版本与能力──
3. Máy chủ xử lý phương pháp.
   Trung ngữ翻译:服务器处理这个方法――
4. Các máy chủ trả lại một kết quả nhập hoặc lỗi JSON-RPC.
   Trung ngữ翻译: máy chủ trả lại một kết quả kiểu hóa hoặc một JSON-RPC 错误。

Việc yêu cầu tiếp theo lặp lại quá trình tương tự từ đầu.

> Tiếp theo yêu cầu từ đầu lặp lại cùng một quy trình.

> **【中文解读】**旧模型的隐患在"服务器记忆": trong quá trình trước sau khi phục vụ nhiều khách hàng, khả năng của một yêu cầu tuyên bố trên sẽ làm ô nhiễm xử lý yêu cầu tiếp theo.`params._meta`里), máy chủ xử lý đã hoàn thành và quên đi.

>  **【类比】**旧版 MCP 像银行柜员办理业务:先取号(建连接) 、再出示身份证登记(初始化握手) 、之后每笔业务都默认"还是你这个号"──新版 MCP 像微信扫码支付:每笔支付请求都自带完整证凭 (订单号、金额身份),任何一台收银机、任何一班都能独立核销,不需要"记住你是谁"──收银机换班 (收银机换班) 进程重启、换工人) 对业务零影响──

## Khái niệm cốt lõi

### Server nguyên thủy

> **【中文解读】**服务器原语仍有三个:工具(模型可调用动作) 、资源(按 URI 寻址的数据) 、提示(可复用模板)  注意新版的重大变化:roots/sampling/logging 这三个旧客户端原语在2026-07-28 schema 中虽然保留但已废弃;要求改走"多轮往返请求"(服务器回归输入_required,客户端补输入后重试) 现代服务器不再主动发发起任何独立 JSON-RPC 请求──

Các máy chủ MCP phơi bày ba nguyên thủy chính:

1. **Tools**là các hành động được kiểm soát theo mô hình, được phát hiện với `tools/list`và được gọi là `tools/call`- Tôi không biết.
   Trung ngữ翻译:**Tools**                                                                                                                                                                                                                                                              `tools/list`发现 `tools/call`调用。
2. **Resources**là dữ liệu được định hướng bằng URI, được phát hiện với `resources/list`và lấy lại với `resources/read`- Tôi không biết.
   Trung ngữ翻译:**Resources**là theo URI 寻址的数据,用 `resources/list`发现 `resources/read`读取:
3. **Prompts**là các mẫu có thể sử dụng lại, được phát hiện với `prompts/list`và được dịch là `prompts/get`- Tôi không biết.
   Trung ngữ翻译:**Prompts**     `prompts/list`发现 `prompts/get`染──

Sối rễ, lấy mẫu và khai thác gỗ vẫn còn trong `2026-07-28`các chương trình tương thích, nhưng chúng đã bị lỗi thời. Các triển khai mới nên sử dụng công cụ hoặc nguồn lực nhập rõ ràng cho gốc, API trực tiếp của nhà cung cấp mô hình để lấy mẫu, và stderr hoặc OpenTelemetry để ghi nhật ký. Việc tạo ra vẫn có sẵn thông qua các yêu cầu nhiều lần đi vòng, nơi máy chủ trả lại yêu cầu nhập và khách hàng thử lại hoạt động ban đầu. Một máy chủ hiện đại không bao giờ khởi động yêu cầu JSON-RPC độc lập.

> Roots、sampling 和 logging 在 `2026-07-28`schema 中为兼容而保留,但已废弃──新实现应:roots 用显式的工具或资源输入替代;样本 直接调用模型提供商 API;登录用 stderr或 OpenTelemetry──elicitation 仍可通过"多轮往返请求" (多轮往返请求)

> 🤔 **【困惑】**Q: 旧版引自傲的样本(服务器借用客户端模型) 怎么说废弃就废弃? A: 实践中它 đã đưa ra quyền quyết định của" ai trả token 费、用哪个模型" , và yêu cầu máy chủ có thể ngược lại调用客户端, làm cho mạng关、鉴定权和缓存都变复杂――新规范把边界划清:服务器需要模型能力就回归`input_required`, bởi khách hàng hoàn chỉnh nhập vào sau thử nghiệm lại  kiểm soát dòng chảy luôn bắt đầu từ khách hàng.

### Các phong bì JSON-RPC

MCP sử dụng JSON-RPC 2.0:

- `{jsonrpc, id, method, params}`
  Trung văn翻译:请求:`{jsonrpc, id, method, params}`
- Phản ứng: `{jsonrpc, id, result}`hoặc `{jsonrpc, id, error}`
  Trung văn翻译:响应:`{jsonrpc, id, result}`Hoặc`{jsonrpc, id, error}`
- Thông báo: `{jsonrpc, method, params}`Không có `id`
  Trung ngữ翻译:通知:`{jsonrpc, method, params}`, không có `id`

`id`liên quan đến một phản ứng. Nó không tạo ra một phiên giao thức.

> Xin vui lòng`id`Chỉ dùng để kết nối một câu trả lời.

### Mét-đồ sơ yêu cầu cần thiết

Mỗi yêu cầu hiện đại đều mang theo một`_meta`vật bên trong `params`- Có thể là:

> Mỗi người yêu cầu hiện đại đều ở đó.`params`Nhận một cái`_meta`Đối tượng:

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/list",
  "params": {
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

Phiên bản giao thức và khả năng của khách hàng là cần thiết. danh tính khách hàng được khuyến cáo. Đó là hiển thị tự báo cáo và dữ liệu gỡ lỗi, không phải giấy chứng nhận bảo mật.

> 协议 phiên bản và khả năng khách hàng là cần thiết.

Các máy chủ không được suy luận bất kỳ giá trị nào từ yêu cầu trước đó, một quy trình stdio, kết nối HTTP hoặc chỉ một tiêu đề giao thông.

> 服务器 phải xác định các giá trị này từ các yêu cầu sớm hơn, quá trình, kết nối HTTP hoặc một tầng truyền tải đơn lẻ.

> ️ **【易错点】**场景: thực hiện từ phiên bản cũ chuyển đổi chỉ trong yêu cầu đầu tiên `_meta`,后续请求"省略"以图省事 / 后果: máy chủ theo quy định phải từ chối`-32602`), và người lao động khác có thể đưa ra hành vi không phù hợp; một loại khác chỉ phụ thuộc vào số phiên bản trên HTTP không kiểm tra cơ quan  quy định yêu cầu biên giới giữa đầu và cơ thể, không phù hợp trả lại `-32020`/ 修复: dùng đơn vị yêu cầu cấu trúc hàm cho mỗi yêu cầu盖全 `_meta`三件套(版本、能力、身份), và gửi trước kiểm tra trình tự hóa sau đó

### Kết quả hoàn chỉnh và danh tính máy chủ

Mỗi kết quả hiện đại thành công bao gồm:`resultType`Kết quả cuối cùng bình thường sử dụng`"complete"`Các máy chủ cũng nên tự xác định mình trong các metadata kết quả:

> Mỗi thành công hiện đại đều có kết quả`resultType`普通最终结果用 `"complete"` máy chủ cũng nên trong kết quả của dữ liệu nhận dạng bản thân:

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "resultType": "complete",
    "tools": [],
    "ttlMs": 30000,
    "cacheScope": "public",
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "notes-server",
        "version": "1.0.0"
      }
    }
  }
}
```

`tools/list`- `resources/list`- `prompts/list`- `resources/templates/list`- `resources/read`, và`server/discover`là kết quả có thể được lưu trữ.`ttlMs`và `cacheScope`Một sự cố định an toàn là`ttlMs: 0`và `cacheScope: "private"`. Các mục danh sách nên có thứ tự xác định để các phản ứng tương đương tạo ra các khóa cache ổn định và bối cảnh mô hình ổn định.

> `tools/list``resources/list``prompts/list``resources/templates/list``resources/read`和 `server/discover`là kết quả có thể lưu trữ, chúng chứa`ttlMs`和 `cacheScope`❖ Giá trị bảo mật là `ttlMs: 0`加 `cacheScope: "private"` Các mục danh sách nên có thứ tự xác định, để đáp ứng giá tương đương có thể tạo ra các khóa dự trữ ổn định và mô hình ổn định trên:

### Khám phá mà không cần bắt tay

> **【中文解读】** `server/discover`Thay thế phiên bản cũ khởi tạo  nắm tay của " tìm đường " vai trò: khách hàng có thể sử dụng nó trước để nhận được các phiên bản được hỗ trợ bởi máy chủ tập hợp, năng lực, sử dụng说明 và danh tính. Nhưng nó là tiện lợi thay vì 门 vì mỗi yêu cầu có thể tự mang phiên bản và năng lực, khách hàng nhảy phát hiện trực tiếp.`tools/list`Cũng hoàn toàn hợp pháp. 版本不匹配时返回 `-32022`, dữ liệu được yêu cầu và được hỗ trợ, khách hàng thay đổi một phiên bản được hỗ trợ bởi cả hai bên.

Mỗi máy chủ hiện đại phải triển khai`server/discover`Khách hàng có thể gọi nó trước một phương pháp khác để lấy:

- `supportedVersions`
  Trung ngữ翻译:`supportedVersions`(支持的版本集合)
- máy chủ `capabilities`
  Trung ngữ翻译:服务器 `capabilities`( năng lực)
- sử dụng tùy chọn `instructions`
  Trung ngữ翻译:可选的使用 `instructions`(số chỉ dẫn)
- kết quả là tính xác thực của máy chủ `_meta`
  中文翻译: kết quả `_meta`Trung tâm danh tính máy chủ
- gợi ý cache
  Trung ngữ翻译:缓存提示

Khám phá là hữu ích, nhưng nó không phải là cổng.`tools/list`Thứ nhất, vì yêu cầu đó đã mang phiên bản và khả năng giao thức của nó.

> Tìm thấy rất hữu ích, nhưng nó không phải là 门.`tools/list`Vì yêu cầu đó đã mang lại phiên bản và khả năng của nó.

Nếu phiên bản yêu cầu không được hỗ trợ, máy chủ sẽ trả lại mã JSON-RPC `-32022`với:

> Nếu phiên bản yêu cầu không được hỗ trợ, máy chủ sẽ trả lại JSON-RPC  errorcode `-32022`, kèm theo:

```json
{
  "requested": "2027-01-01",
  "supported": ["2026-07-28"]
}
```

Khách hàng chọn một phiên bản hiện đại hỗ trợ lẫn nhau và thử lại với một ID yêu cầu JSON-RPC mới.

> 客户端 chọn một phiên bản hiện đại được hỗ trợ bởi cả hai bên, sử dụng một phiên bản JSON-RPC mới Ứng dụng ID 重试──

### Một vòng đời yêu cầu

Theo dõi một yêu cầu hiện đại theo thứ tự này:

> 按以下顺序追踪一个现代请求:

1. Phân tích một phong bì JSON-RPC.
   Trung文翻译:解析一个 JSON-RPC 信封──
2. Đảm bảo `jsonrpc`là `"2.0"`, một `id`tồn tại,`method`là một dây, và `params`là một đối tượng.
   中文翻译: xác nhận `jsonrpc` `"2.0"`、 tồn tại `id``method`là chữ 文字`params`Là đối tượng.
3. yêu cầu các chuỗi phiên bản và khả năng đối tượng trong `params._meta`; các metadata bị biến dạng hoặc thiếu là `-32602`- Tôi không biết.
   Trung ngữ翻译:要求 `params._meta`Có phiên bản các chữ cái và khả năng đối tượng;元数据形或缺失返回 `-32602`
4. Tại một ranh giới HTTP, so sánh phiên bản, phương pháp và tiêu đề tên áp dụng với cơ thể.`-32020`ngay cả khi một trong hai giá trị phiên bản không được hỗ trợ.
   Trung ngữ翻译:在 HTTP 边界处比对版本、方法和适用名称头部与 body──不一致返回 `-32020` Ngay cả khi có một trong hai giá trị phiên bản tự nó không được hỗ trợ.
5. Sau khi bình đẳng được thiết lập, từ chối một phiên bản phù hợp nhưng không được hỗ trợ với `-32022`- Tôi không biết.
   Trung ngữ翻译:确认一致后,再拒绝"一致但不受支持"版本,返回 `-32022`
6. Kiểm tra khả năng cần thiết, sau đó đi đường bằng `method`và xác nhận các lập luận cụ thể về phương pháp.
   Trung ngữ翻译:检查必需能力, rồi按 `method`路由并校验方法级参数──
7. Truy hiệu và ủy quyền cho hoạt động bê tông trước khi người xử lý nó chạy.
   Trung ngữ翻译:在经理运行之前对具体操作做认证与授权──
8. Trả lại kết quả đầy đủ với danh tính máy chủ.
   Trung ngữ翻译:返回带服务器身份的完整结果──
9. Quên metadata giao thức theo yêu cầu.
   Trung ngữ翻译: quên mất yêu cầu cấp của giao ước元数据──

> **【中文解读】**Trình tự này là thiết kế an toàn: trước kiểm tra tín hiệu, tái kiểm tra dữ liệu, tái so sánh với đầu và cơ thể, phòng chống lại "những ghi chú. đọc, cơ thể nhưng là ghi chú. xóa" của buôn lậu) và sau đó cho phép và thực hiện. Mỗi bước thất bại có mã lỗi độc lập, và các bước khác có thể xác định được vấn đề ở đâu, thay vì đưa ra một "400 yêu cầu xấu".

Chỉ định đó ngăn cản hai thành phần giải thích các cuộc gọi khác nhau.`Mcp-Name: notes.read`trong khi nguồn gốc thực hiện `params.name: notes.delete`Nó cũng giữ nhập dạng sai, nhầm lẫn tiêu đề, đàm phán phiên bản, thất bại khả năng, ủy quyền và thất bại xử lý như bằng chứng rõ ràng.

> Điều này ngăn chặn hai thành phần để "đồng một调用" làm cho các giải thích khác nhau.`Mcp-Name: notes.read`Trong khi đó, các nhà đầu tư đã thực hiện`params.name: notes.delete` Nó cũng cho phép  hình thức nhập, đầu混, phiên bản đàm phán, thiếu năng lực, quyền thất bại và người xử lý, cố gắng để lại bằng chứng độc lập.

Đóng stdin hoặc phản ứng HTTP chấm dứt hoạt động vận chuyển. Nó không chấm dứt phiên giao thức vì MCP hiện đại không có phiên giao thức.

> 关闭 stdin hoặc trả lại HTTP 响应只是结束传输层活动──它 không kết thúc hiệp ước会话, vì MCP hiện đại 根本没有协议会话──

### Sự tương thích rõ ràng của sản phẩm

Các phiên bản thông qua `2025-11-25`sử dụng `initialize`- `notifications/initialized`, khả năng kết nối và, trên Streamable HTTP trước đó, các phiên giao thức tùy chọn. Hành vi đó vẫn có liên quan khi một khách hàng hai thời đại nói chuyện với một máy chủ cũ.

> Đến`2025-11-25`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `initialize``notifications/initialized`、 Khả năng kết nối cấp, cũng như các giao thức được chọn trên HTTP Streamable sớm.

Giữ các thời kỳ riêng biệt. Một yêu cầu hiện đại được xác định bằng các metadata yêu cầu theo yêu cầu. Một kết nối cũ chỉ được chọn thông qua con đường quay lại tài liệu. Không gửi `initialize`như là mặc định cho một `2026-07-28`máy chủ.

> Hãy chia hai thời đại. Ứng dụng hiện đại được phân chia bởi các yêu cầu cần thiết.`initialize`Khi được gửi đi`2026-07-28`服务器的默认行为──

Tất nước  do đó có một ý nghĩa cụ thể của thời đại.`2026-07-28`, nó là một giao thức không thay đổi: mỗi yêu cầu thường tự do có thể giải thích và không có phiên bản MCP tồn tại.`2025-11-25`, khởi tạo và khả năng đàm phán thuộc về kết nối, vì vậy một bộ điều chỉnh tương thích có thể giữ lại trạng thái kết nối cũ. Một thực hiện hai thời đại không phải là một máy trạng thái cho phép. Nó là một lõi hiện đại không có quốc gia bên cạnh một bộ điều chỉnh cũ bị cô lập, với một quyết định lựa chọn rõ ràng trước khi cả hai bộ phân tích chạy.

> Vì vậy, "không trạng thái" có ý nghĩa cụ thể trong thời đại.`2026-07-28`Trung nó là một thỏa thuận không thay đổi: mỗi yêu cầu thường đều có thể giải thích độc lập, không có MCP 会话.`2025-11-25`Trong phiên bản kết thúc, khả năng khởi tạo và đàm phán thuộc về kết nối, vì vậy bộ điều chỉnh khả năng có thể giữ lại trạng thái kết nối phiên bản cũ.

Không có nghĩa nào cấm trạng thái ứng dụng bền vững. Một dòng công việc, nhiệm vụ hoặc bản thảo có thể sống sau một tay cầm không minh bạch trong một cửa hàng chung. Khách hàng gửi tay cầm đó như là đầu vào thông thường, và mỗi bản sao xác thực và ủy quyền sử dụng nó.

> 两种意义都不禁止持久的应用状态――工作流、任务或草稿可以活在共享存储中的一个不透明句柄后面――客户端把这个句柄当成普通输入发送,每个副本都对其使用进行认证和授权――协议上下文必须作为被移除的话语的替代泄漏进入存储――

> **【拓展：双时代并存的现实】**"không trạng thái" không phải là "không có trạng thái kinh doanh" Đây là một sai lầm phổ biến nhất. ghi chú, nhiệm vụ, dòng chảy làm việc như lưu trữ thông thường; bị cấm chỉ là "đưa văn bản dưới thỏa thuận trong một cuộc họp kín" (ví dụ bằng cách "như kết nối trên sau tuyên bố về những gì có thể làm" để giải mã một yêu cầu) 分清" ứng dụng trạng thái ((có thể duy trì) "và" thỏa thuận cuộc họp trạng thái ((已移除)", đã nắm bắt được tinh thần của phiên bản 2026-07-28 .

```figure
mcp-tool-call
```

## Hãy sử dụng nó để thực hiện

`code/main.py`xây dựng, xác nhận, theo dõi và gửi tin nhắn MCP hiện đại mà không có khung.

> `code/main.py`Trong trường hợp không sử dụng bất kỳ khung nào, xây dựng, thử nghiệm, theo dõi và phát hiện ra các thông tin MCP:

```bash
python3 code/main.py
python3 -m unittest discover code/tests -v
```

Hãy xem xét ba biến số trong đầu ra:

> Trong xuất khẩu tập trung vào 3 biến động:

- Mỗi yêu cầu đều lặp lại.`_meta`các cánh đồng.
  Trung ngữ翻译: Mỗi yêu cầu đều lặp lại mang theo của mình `_meta`字段。
- Mỗi kết quả thành công đều là`resultType: "complete"`và bao gồm danh tính máy chủ.
  Trung ngữ翻译: mỗi thành công là kết quả`resultType: "complete"`且包含服务器身份──
- Kết quả danh sách được sắp xếp theo định nghĩa và có gợi ý cache rõ ràng.
  Trung文翻译:列表结果有确定性排序并带显式缓存提示──

## Chuyển nó đi.

Bài học này sẽ đi theo `outputs/skill-mcp-handshake-tracer.md`Tên tập tin lịch sử vẫn ổn định, nhưng hiện tại, vật phẩm này là một bộ theo dõi yêu cầu không có quốc gia. Nó kiểm tra từng tin nhắn một cách độc lập và chỉ dán nhãn lưu lượng truy cập bắt tay cũ khi nó thực sự hiện diện.

> 本课交付 `outputs/skill-mcp-handshake-tracer.md`◊ Tên tập tin theo tên lịch sử, nhưng sản phẩm hiện là một trình theo dõi yêu cầu không có trạng thái: nó kiểm tra độc lập mỗi tin nhắn, chỉ khi lưu lượng thực sự xuất hiện mà được đánh dấu như di sản.

## Tập luyện bài tập

1. Thay đổi phiên bản giao thức của một yêu cầu thành `2027-01-01`- Đảm bảo mã lỗi là `-32022`và dữ liệu quảng cáo phiên bản được hỗ trợ.
   Trung ngữ翻译:把某某请求的协议版本改成 `2027-01-01` xác nhận sai lầm là `-32022`且数据中公示了受支持的版本──

2. Tắt `io.modelcontextprotocol/clientCapabilities`xác nhận máy chủ không sử dụng lại các khả năng từ yêu cầu đầu tiên.
   Trung ngữ翻译: 从第二请求中移除 `io.modelcontextprotocol/clientCapabilities`❖ xác nhận máy chủ sẽ không sử dụng lại các yêu cầu đầu tiên

3. Trở lại sổ đăng ký công cụ trong bộ nhớ.`tools/list`vẫn trả lại cùng một thứ tự xác định.
   Trung文翻译:反转内存中的工具注册表──确认 `tools/list`仍返回相同的确定性顺序──

4. Thay đổi`cacheScope`từ `public`đến`private`Giải thích các bối cảnh ủy quyền nào có thể tái sử dụng phản ứng trong từng trường hợp.
   Trung ngữ翻译:把 `cacheScope`Từ `public`改成 `private` giải thích trong hai trường hợp nào các quyền trên sau đây có thể được sử dụng lại câu trả lời này

5. Thêm tùy chọn `clientInfo`Thử nghiệm bỏ qua: yêu cầu này vẫn có giá trị vì danh tính khách hàng được khuyến cáo, không cần thiết.
   Trung ngữ翻译:添加一个可选的`clientInfo`缺省测试── 該请求应仍然合法, vì tính khách hàng là đề nghị chứ không phải là yêu cầu.

## Từ khóa  Từ khóa nhanh chóng

| Term | Meaning |
|------|---------|
| Stateless protocol | Every request supplies the metadata needed to interpret it |
| Request metadata | Version, client capabilities, and recommended client identity in `params._meta` |
| `server/discover` | Mandatory server method for versions, capabilities, instructions, and identity |
| `resultType` | Discriminator on every successful modern result |
| Cacheable result | Result that includes required `ttlMs` and `cacheScope` hints |
| Protocol era | Modern per-request metadata or legacy connection-scoped initialization |
| Transport lifetime | Process, connection, or response-stream lifetime, not protocol session state |
| `-32022` | Unsupported protocol version error with requested and supported versions |

> 术语中文对照:Protocol không có trạng thái = không có trạng thái;Request metadata=请求元数据(`params._meta`Trung phiên bản、客户端能力与建议的客户端身份);server/discover=server发现(必选方法,公示版本、能力、说明与身份);resultType=结果类型(每个成功现代结果上的判别字段);Cachable result=可缓存结果(必含`ttlMs`Với`cacheScope`提示);Protocol era=协议时代;现代逐请求元数据 vs 旧版连接级初始化;Transport lifetime=传输层生命周期;进程/连接/响应流的存活期;不是协议会话状态;-32022=不支持的协议版本错误;附请求与支持)

## Xem thêm 延伸阅读

- [MCP Architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture)
  中文翻译:MCP 架构文档(2026-07-28 版)
- [MCP Base Protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic)
  Trung文翻译:MCP 基础协议(JSON-RPC 信封、元数据、生命周期)
- [MCP Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  Trung文翻译:server/discover 方法规范
- [MCP 2026-07-28 Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
  Trung ngữ翻译:2026-07-28 版变更日志(相对旧版的核心差异清单)
