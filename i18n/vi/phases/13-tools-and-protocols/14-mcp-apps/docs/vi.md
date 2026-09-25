# MCP Apps trên giao thức vô quốc tịch

> Kết quả tương tác vẫn là một công cụ MCP và trao đổi tài nguyên. lõi 2026-07-28 làm cho trao đổi đó tự chủ, trong khi phần mở rộng Apps thêm bề mặt trình duyệt sandboxed.

> **【中文解读】**Một kết quả giao tiếp vẫn là một lần MCP 工具与资源交换──2026-07-28 核心协议让此次交换自包含(每个请求自带版本与能力,无会话),Apps 扩展在其上叠加沙盒化的浏览器表面──注意本课已完全改版:不再围绕SEP-1724/ext-app SDK,而是围绕`io.modelcontextprotocol/ui`扩展`server/discover`发现、以及"UI 声明在工具定义上 (调用前元数据) "

> **【拓展：MCP Apps→Agent 的应用平台】**MCP Apps là một bước quan trọng trong việc chuyển từ "text tool调用" hướng tới "app platform", giống như微信小程序之于微信:写一次`ui://`资源, tất cả các兼容宿主都能染──2026-07-28 重设计后, nó với không trạng thái lõi nghiêm ngặt phân cấp lõi ống phát hiện/工具/资源,Apps 扩展管 UI 声明与iframe 桥接,浏览器沙箱管最终边界──

>  **【前置】**学本节前请先掌握:(1) Giai đoạn 13·07(MCP server) với 13·10(cơ sở hữu)`ui://`là một loại chương trình tài nguyên,Apps  tuyên bố phụ thuộc vào `tools/list`和 `resources/read`上;(2) 2026-07-28 无状态核心(Phase 13·11 MRTR、13·12 dẫn cùng nguồn)  mỗi yêu cầu mang theo `_meta`能力, không có `initialize`会话;(3) HTML/iframe/postMessage/CSP 基础 沙盒与桥接重度依赖它们──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 10 (resources) | **前置知识:** Phase 13 · 07（MCP server）、Phase 13 · 10（resources）
**Time:** ~75 minutes | **时间:** 约 75 分钟

## Mục tiêu học tập

- Giao dịch các ứng dụng MCP thông qua `server/discover`và khả năng mở rộng theo yêu cầu.
  Trung ngữ翻译:通过 `server/discover`Và theo yêu cầu tuyên bố khả năng mở rộng MCP Apps
- Thiết lập một `ui://`tài nguyên trên một công cụ trước khi công cụ được gọi.
  Trung ngữ翻译: 在工具被调用之前就把`ui://`资源声明在工具定义上──
- Trả lại kết quả công cụ và tài nguyên hoàn chỉnh trên dây vô quốc tịch 2026-07-28.
  Trung ngữ翻译: 在 2026-07-28 无状态线形式上返回完整的工具与资源结果──
- Phân tách các ứng dụng `ui/initialize`thông điệp cầu từ cú tay của lõi MCP đã bị xóa.
  Trung ngữ翻译:把 Apps 的 `ui/initialize`桥接消息与已移除的MCP 核心握手区分开.
- Sử dụng xác nhận nguồn gốc, sandboxing, CSP và quyền quyền ưu tiên tối thiểu.
  Trung文翻译:应用源校验、沙箱、CSP 和最小权限──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**文本结果只能"描述"时间线, không thể cho người dùng một条能过、能检查、能操作的时间线──MCP Apps sử dụng có thể mở rộng để giải quyết vấn đề hiện tại:工具定义指向`ui://`资源, chủ nhà có thể trong công cụ vận hành trước nắm bắt và kiểm tra tài nguyên này                                                                                                                                                                                                                                                     

Kết quả văn bản có thể mô tả một dòng thời gian. Nó không thể cung cấp cho người dùng một dòng thời gian mà họ có thể lọc, kiểm tra hoặc hành động theo.

> Kết quả văn bản có thể mô tả một dòng thời gian. Nó không thể cung cấp cho người dùng một dòng thời gian có thể qua、 có thể kiểm tra、 có thể hoạt động.

MCP Apps giải quyết vấn đề trình bày bằng một phần mở rộng tùy chọn.`ui://`nguồn lực. Người chủ có thể lấy và xem xét nguồn tài nguyên đó trước khi công cụ chạy, render nó trong một iframe sandboxed, và trung gian tất cả các hành động ứng dụng thông qua một cây cầu JSON-RPC.

> MCP Apps sử dụng một tùy chọn mở rộng để giải quyết vấn đề hiện tại.`ui://`资源── chủ nhà có thể lấy và kiểm tra tài nguyên này trước khi chạy công cụ ⋅ trong khung i-frame ⋅ trong hộp ⋅ ⋅ nó ⋅ và thông qua JSON-RPC 桥接中介所有 App 动作──

Các giao thức cốt lõi đã thay đổi vào năm 2026-07-28. Không bao bọc một ứng dụng trong vòng đời kết nối cũ:

> 核心协议 vào năm 2026-07-28 已变化. Đừng bao gồm App  vào vòng đời kết nối cũ:

- Không có lõi nào.`initialize`yêu cầu hoặc `notifications/initialized`thông báo.
  Trung ngữ翻译:没有核心`initialize`Xin lỗi, cũng không có `notifications/initialized`通知:
- Không có `Mcp-Session-Id`đầu.
  Trung ngữ翻译:没有 `Mcp-Session-Id`头──
- Mỗi yêu cầu đều có phiên bản giao thức và khả năng của khách hàng trong `params._meta`- Tôi không biết.
  Trung ngữ翻译:每个请求都在 `params._meta`Trung携带协议版本和客户端能力──
- Một máy chủ thực hiện `server/discover`để khách hàng có thể kiểm tra phiên bản, khả năng cốt lõi và phần mở rộng.
  中文翻译:服务器实现 `server/discover`, để khách hàng có thể kiểm tra phiên bản, năng lực và mở rộng lõi.
- Mỗi kết quả thành công đều có một kết quả`resultType`phân biệt đối xử.
  Trung ngữ翻译: mỗi thành công đều có kết quả`resultType`判别符.
- Streamable HTTP sử dụng một POST mỗi yêu cầu. GET và DELETE hiện đại trả lại 405.
  中文翻译:Streamable HTTP 每个请求用一个 POST──现代 GET 与 DELETE 入口返回 405──

Cầu Apps vẫn có một phương pháp có tên `ui/initialize`Nó thuộc về phương ngữ iframe postMessage. Nó không tạo lại một phiên bản MCP cốt lõi.

> Apps 桥接 vẫn có một cái tên `ui/initialize`方言──它 sẽ không tái tạo lõi MCP 会话──

>  **【类比】**MCP Apps 像"AI 助手版微信小程序",2026 版又把它搬进"去中心化货架": trước đây mỗi chủ nhà đều có một bộ các phần liên kết API(Claude artefacts、GPT custom HTML),App Author phải cá nhân thích ứng; bây giờ là một `ui://`资源 + một phần tuyên bố mở rộng, bất cứ điều gì đã được thực hiện `io.modelcontextprotocol/ui`Người chủ nhà đều có thể nhập vai, và không cần phải đăng ký trước mỗi yêu cầu tự mang danh tính và khả năng, như máy tự trợ giúp dùng máy tính, thay vì làm việc với thẻ thành viên.

## Khái niệm cốt lõi

> **【中文解读】**本节走完整契约链:双协议分层 → 发现(`server/discover`)→ 工具定义上声明 UI(调用前元数据)→ 工具调用只返回数据 → `resources/read`提供可执行内容 → 按可执行内容缓存 → 线格式歧义先行拒绝 → 沙箱是边界而非信任判决 → 桥接有自己的生命周期 → 宿主上下文与能力撤销 → 降级是契约的一部分──

### Hai giao thức, một tính năng

Giữ các lớp rõ ràng:

> 让各层保持显式:

1. Các lõi MCP mang `server/discover`- `tools/list`- `tools/call`- `resources/list`, và`resources/read`- Tôi không biết.
   中文翻译:MCP 核心承载 `server/discover``tools/list``tools/call``resources/list`和 `resources/read`
2. MCP Apps mở rộng tuyên bố UI và xác định cầu iframe-to-host.
   Trung文翻译:MCP Apps 扩展声明 UI 并定义 iframe 到主人的桥接──
3. Các quy tắc hộp rác trình duyệt hạn chế những gì UI có thể đạt được.
   Trung文翻译:浏览器沙箱规则限制 UI 能触及的范围──

Định dạng mở rộng là `io.modelcontextprotocol/ui`. Cả hai đồng nghiệp chọn tham gia. Một khách hàng gửi hỗ trợ mở rộng bên trong đối tượng khả năng với mỗi yêu cầu:

> 扩展标识符 là `io.modelcontextprotocol/ui`❖ Biết chọn tham gia ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "server/discover",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "extensions": {
          "io.modelcontextprotocol/ui": {}
        }
      },
      "io.modelcontextprotocol/clientInfo": {
        "name": "timeline-host",
        "version": "1.0.0"
      }
    }
  }
}
```

`clientInfo`được khuyến cáo để chẩn đoán. Đó là dữ liệu tự báo cáo, không phải là một danh tính ủy quyền.

> 建议包含 `clientInfo`Để được chẩn đoán, đó là dữ liệu tự báo cáo, không phải là quyền nhận dạng.

### Khám phá trước khi chuyển đổi

Kết quả phát hiện của máy chủ quảng cáo mở rộng:

> 服务器的发现结果声明该扩展:

```json
{
  "resultType": "complete",
  "supportedVersions": ["2026-07-28"],
  "capabilities": {
    "tools": {},
    "resources": {},
    "extensions": {
      "io.modelcontextprotocol/ui": {}
    }
  },
  "ttlMs": 300000,
  "cacheScope": "public",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "timeline-app-server",
      "version": "2.0.0"
    }
  }
}
```

Các máy chủ phải hỗ trợ phát hiện. Một khách hàng không bị buộc phải gọi phát hiện trước mỗi hành động vì mỗi hành động mang lại khả năng riêng của nó.

> 服务器 phải hỗ trợ phát hiện. 客户端 không cần phải sử dụng phát hiện trước mỗi động tác, vì mỗi động tác đều có khả năng.

### Thiết lập UI trên định nghĩa công cụ

> **【中文解读】**Đây là phiên bản mới và phiên bản cũ (SEP-1724 时代) nhất sự khác biệt trong giao ước: UI không còn phụ thuộc vào kết quả của công cụ调用.`_meta.ui`上, thay vì 提前声明在`tools/list`của công cụ định nghĩa`_meta.ui.resourceUri`(■) Thay vào ba lợi ích: chủ nhà có thể tải trước, lưu trữ và yêu cầu kết quả cho thấy trước khi thực hiện kiểm tra an ninh.

Hợp đồng ứng dụng hiện đại liên kết UI với công cụ trong `tools/list`- Có thể là:

> 现代 Apps 契约在 `tools/list`Trung把 UI  bị ràng buộc vào công cụ:

```json
{
  "name": "notes_timeline",
  "description": "Render a timeline of notes.",
  "inputSchema": {
    "type": "object",
    "properties": {}
  },
  "_meta": {
    "ui": {
      "resourceUri": "ui://notes/timeline.html"
    }
  }
}
```

Đây là metadata trước cuộc gọi. Người chủ có thể tải trước, lưu trữ cache và xem xét bảo mật HTML trước khi kết quả yêu cầu hiển thị nó. Các phím metadata phẳng cũ có thể được chấp nhận bởi mã tương thích, nhưng các máy chủ mới nên phát ra các ổ `_meta.ui.resourceUri`hình thức.

> Đây là một dự định để điều chỉnh dữ liệu trước đó. Người chủ có thể tải trước trước khi yêu cầu kết quả hiển thị. Cài lưu và kiểm tra an toàn cho HTML.`_meta.ui.resourceUri`形式──

`tools/list`là cacheable trong lõi hiện tại. Bao gồm định nghĩa sắp xếp,`ttlMs`, và`cacheScope`- Sử dụng`private`khi các công cụ có thể nhìn thấy khác nhau theo người dùng hoặc token.

> `tools/list`Trong trung tâm hiện tại là có thể lưu trữ.`ttlMs`和 `cacheScope`                                                                                                                                                                                                                                                              `private`

### Trả lại dữ liệu, sau đó để máy chủ kết nối khung cảnh

Các công cụ gọi trả lại nội dung thông thường cộng với dữ liệu cấu trúc:

> 工具调用回归普通内容加结构化数据:

```json
{
  "resultType": "complete",
  "content": [
    {"type": "text", "text": "Timeline ready."}
  ],
  "structuredContent": {
    "notes": [
      {"id": "note-1", "title": "Discover", "created": "2026-07-28"}
    ]
  },
  "isError": false
}
```

Người chủ đã biết xem nào thuộc về công cụ. Tránh phát minh một khối nội dung mới chỉ để lặp lại URI.

> Người chủ đã biết xem nào thuộc về công cụ này. Đừng để lặp lại URI mà phát triển các khối nội dung mới.

### Sử dụng ứng dụng như một nguồn tài nguyên

Máy chủ quảng cáo `resources`trong khám phá, vì vậy nó cũng thực hiện các bắt buộc`resources/list`Các mục danh sách xác định của nó bao gồm URI, tên ổn định, mô tả và loại MIME. Kết quả danh sách bao gồm `resultType`, dữ liệu siêu dữ liệu danh tính máy chủ,`ttlMs`, và`cacheScope`, giống như danh sách các công cụ xác định.

> 服务器在发现中声明 `resources`, do đó cũng thực hiện bắt buộc `resources/list`操作──其确定性列表条目包含规范 URI、稳定名称、描述和 MIME 类型──列表结果包含 `resultType`、 Server ID:`ttlMs`和 `cacheScope`, phù hợp với danh sách các công cụ xác định

Người chủ gửi `resources/read`. Trên Streamable HTTP, yêu cầu có:

> 宿主发送 `resources/read`在 Streamable HTTP 上, yêu cầu hình như:

```text
POST /mcp
MCP-Protocol-Version: 2026-07-28
Mcp-Method: resources/read
Mcp-Name: ui://notes/timeline.html
```

Các giá trị tiêu đề và cơ thể JSON-RPC phải phù hợp. Một sự không phù hợp là lỗi giao thức `-32020`- Tôi không biết.

> 头部值与 JSON-RPC 主体必须匹配──不匹配即协议错误 `-32020`

Kết quả chứa tài nguyên HTML và gợi ý cache:

> Kết quả chứa HTML 资源 và cache提示:

```json
{
  "resultType": "complete",
  "contents": [
    {
      "uri": "ui://notes/timeline.html",
      "mimeType": "text/html;profile=mcp-app",
      "text": "<!doctype html>...",
      "_meta": {
        "ui": {
          "csp": {
            "connectDomains": [],
            "resourceDomains": [],
            "frameDomains": [],
            "baseUriDomains": []
          },
          "permissions": {}
        }
      }
    }
  ],
  "ttlMs": 60000,
  "cacheScope": "public"
}
```

### Cache các tài nguyên UI như nội dung thực thi

Một tài nguyên ứng dụng không thể thay đổi với văn bản thông thường. mục kho lưu trữ của nó có thể thực hiện mã cầu, trình bày dữ liệu công cụ và yêu cầu các hành động trung gian của máy chủ.`ui://`URI, nhận dạng và phiên bản máy chủ, tiêu hóa nội dung tài nguyên và bối cảnh ủy quyền khi `cacheScope`Không bao giờ sử dụng lại tài nguyên ứng dụng riêng tư trên các nguyên tắc vì HTML hoặc metadata chính sách của nó có thể khác nhau ngay cả khi URI là giống nhau.

> Ứng dụng 资源 không thể nhầm lẫn với văn bản thông thường. Ứng dụng 资源 không thể nhầm lẫn với văn bản thông thường.`ui://`URI、 đã sẵn sàng Server ID và phiên bản、 nguồn tài liệu,`cacheScope`Để được cấp quyền riêng tư, các phần mềm dưới đây được sử dụng như một khóa lưu trữ.

Tháo bỏ mục khi nó `ttlMs`hết hạn, công cụ của `_meta.ui.resourceUri`thay đổi liên kết, phiên bản máy chủ hoặc thay đổi pin mô tả được chấp nhận, hoặc một đăng ký thay đổi tài nguyên được xác nhận đặt tên URI. Phục hồi và áp dụng lại CSP và kiểm tra quyền phép trước khi cài đặt lại. Một iframe cũ không được giữ các quyền rộng hơn chỉ vì một phiên bản tài nguyên mới chưa tải.

> 当条目的`ttlMs`过期、工具的 `_meta.ui.resourceUri`绑定变化、服务器版本或已准备描述符点变化、或已确认的资源变更订阅点名该 URI 时,使条目失效──重新挂载前重新抓取并重做CSP与权限审查──旧iframe 不能仅因为新资源版本尚未加载就保留更宽的权限──

### Tháo lại sự mơ hồ về dây trước chính sách tính năng

Thiết lập có một thứ tự cố ý. Trước tiên xác nhận hình dạng JSON-RPC và yêu cầu metadata giao thức chuỗi cộng với bản đồ khả năng khách hàng đối tượng. Sau đó so sánh tiêu đề định tuyến với cơ thể. Chỉ sau đó quyết định liệu phiên bản giao thức phù hợp có được hỗ trợ hay không.

> 校验有意意的顺序――先校验 JSON-RPC 形状, yêu cầu các dữ liệu của các giao thức字符串 và khả năng phân tích khách hàng của các đối tượng――再比较路由头与主体――最后才判断是否支持了匹配的协议版本――这个顺序防止代理和服务器各自解释不同的请求――

| Condition | HTTP | JSON-RPC error |
|-----------|------|----------------|
| Header and body version, method, or name disagree | 400 | `-32020` |
| Header and body agree on an unsupported version | 400 | `-32022`, with `data` exactly `{"supported":["2026-07-28"],"requested":"<actual>"}` |
| `resources/read` lacks the Apps extension capability | 400 | `-32021`, with `data.requiredCapabilities.extensions.io.modelcontextprotocol/ui` |
| Method is unknown | 404 | `-32601` |

> 表格对照(zh 版):头部与主体的版本/方法/名称不一致HTTP 400,错误 `-32020`Các bên đồng ý nhưng phiên bản không được hỗ trợ 400,`-32022`- Tôi không biết.`data`精确为 `{"supported":["2026-07-28"],"requested":"<actual>"}`-`resources/read`缺少 Apps  mở rộng năng lực 400,`-32021`- Tôi không biết.`data.requiredCapabilities.extensions.io.modelcontextprotocol/ui`- Không biết cách nào.`-32601`

Một thông báo JSON-RPC không có `id`, vì vậy máy chủ không bao giờ phát ra phản ứng JSON-RPC cho nó. Một thông báo HTTP được chấp nhận trả lại 202 với một cơ thể trống. Một lỗi có thể thay đổi tình trạng HTTP, nhưng nó vẫn không thể tạo ra một cơ thể lỗi JSON-RPC cho một thông báo.

> JSON-RPC 通知没有 `id`, vì vậy máy chủ không bao giờ cho nó phát ra JSON-RPC  phản ứng. Được chấp nhận HTTP  thông báo trả về 202 với chủ thể không có.

### Cái hộp cát là ranh giới, không phải phán quyết tin tưởng

> **【中文解读】**沙箱解决"能不能碰到",不解决"该不该相信"── chủ chủ kiểm soát iframe:App 不能直接读主 cookie、localStorage或页面 DOM, tất cả các đặc quyền hoạt động phải được chuyển桥──默认值:CSP 域名列表全空再按需加(`connectDomains`管 fetch/XHR/WebSocket,`resourceDomains`管脚本样式图片字体);能打包就打包;没有可见功能就不要申请摄像头/麦克风/定位;postMessage 钉死精确对端源;工具参数、结果、资源文本、桥接消息全部当不可信输入;用户同意留在宿主iframe 不能批准自己的重大操作──切记:放行的域名仍是外通道,`connectDomains: ["https://api.example.com"]`Có nghĩa là bất kỳ văn bản nào trong ứng dụng đều có thể đưa dữ liệu được nhận ra ra.

Một máy chủ điều khiển iframe. Ứng dụng không thể trực tiếp đọc cookie chủ, lưu trữ địa phương hoặc trang DOM. Tất cả công việc đặc quyền phải vượt qua cầu.

> 宿主控制 iframe──App 不能直接读取宿主 cookie──本地存储或页面 DOM──所有特权工作必须经过桥接──

Sử dụng các mặc định này:

> Sử dụng các giá trị ẩn:

- Để tất cả các danh sách tên miền CSP trống, sau đó chỉ thêm nguồn gốc mà ứng dụng cần. Sử dụng `connectDomains`cho lấy, XHR, và WebSocket; sử dụng `resourceDomains`cho các kịch bản, phong cách, hình ảnh và phông chữ.
  Trung文翻译: Hãy để tất cả CSP 域名列表保持为空, sau đó chỉ thêm App 需要的源──fetch、XHR 和 WebSocket 用 `connectDomains`; kịch bản, phong cách, hình ảnh và chữ sử dụng`resourceDomains`
- Kết hợp mã và dữ liệu khi có thể.
  Trung ngữ翻译:可行时把代码和数据打包内置.
- Không yêu cầu phép chụp ảnh, nghe nhạc hoặc đặt chỗ trừ khi một tính năng có thể nhìn thấy cần nó.
  Trung ngữ翻译: trừ khi có chức năng cần thiết, không yêu cầu quyền quay, máy bay hoặc định vị.
- Pin `postMessage`đến nguồn gốc chính xác của các đồng nghiệp và từ chối các sự kiện từ mọi nguồn gốc khác.
  Trung ngữ翻译:把 `postMessage`Đánh vào nguồn gốc chính xác, từ chối bất kỳ sự kiện nào khác.
- Chống đối số công cụ, kết quả công cụ, văn bản tài nguyên và các thông điệp cầu như là đầu vào không đáng tin cậy.
  Trung ngữ翻译:把工具参数、工具结果、资源文本和桥接消息都当作不可信输入──
- Giữ sự đồng ý của người dùng trong máy chủ. iframe không thể chấp thuận hành động hậu quả của riêng nó.
  Trung ngữ翻译:把用户同意留在宿主──iframe 不能批准自己的重大操作──

Đừng sao chép một số cố định `sandbox`thuộc tính từ một hướng dẫn vào mỗi máy chủ. máy chủ phải chọn cờ dựa trên mô hình nguồn gốc của ứng dụng và thiết kế cách ly của riêng nó.

> Đừng cố định trong bài học`sandbox`属性复制进每个主机. 的主机必须基于App's源模型和自己的隔离设计来选择标志.

Một miền được phép vẫn là một con đường thoát. `connectDomains: ["https://api.example.com"]`nghĩa là bất kỳ kịch bản nào chạy bên trong ứng dụng có thể gửi dữ liệu được phép ở đó. Sự phù hợp chính xác nguồn gốc ngăn ngừa sự nhầm lẫn về điểm đến, nhưng nó không quyết định liệu tải trọng hữu ích có phù hợp hay không. Giữ truy cập kết nối trống mặc định, tránh đặt token người mang vào iframe, các hoạt động cúng qua máy chủ khi thực tế, giới hạn kích thước phản ứng và yêu cầu, và kiểm tra hành động của người dùng gây ra mỗi yêu cầu ra ngoài. Chữa bệnh`resourceDomains`tách biệt với `connectDomains`; quyền tải font hoặc script không nên cho phép tải dữ liệu tùy ý.

> Được phép tên miền vẫn là một lối thoát ngoài.`connectDomains: ["https://api.example.com"]`Có nghĩa là bất kỳ kịch bản nào trong ứng dụng thực hiện đều có thể đưa dữ liệu được nhận được ra để chuyển đến đó. Cần xác định nguồn phù hợp để ngăn chặn sự nhầm lẫn mục tiêu, nhưng không đánh giá tải trọng có phải là có hoặc không.`resourceDomains`Với`connectDomains`Để phân chia đối xử; quyền tải chữ cái hoặc văn bản không được cấp cho bất kỳ dữ liệu trên truyền tải.

> ️ **【易错点】**场景:图省事给CSP 开 `connectDomains: ["*"]`Hoặc là`postMessage`写成  写成 `"*"`/ 后果:App trong bất kỳ script nào (include being injected) đều có thể chuyển đến bất kỳ địa chỉ nào 传输数据外传数据、接收任意源的恶意消息精确源匹配只防"发错地方",不防"发的东西本身不应发" / 修复:域名列表默认全空、按需加白;`targetOrigin`Với`event.origin`校验钉死精确对端;加载权(resourceDomains) 与上传权(connectDomains) 分离; nhạy cảm操作走宿主代理并审计。

### Cầu Apps có chu kỳ đời riêng của nó

> **【中文解读】**桥接是 postMessage 上的 JSON-RPC 方言, có một vòng đời nhỏ của riêng mình:View 发 `ui/initialize`(带 `appInfo`和 `appCapabilities`)→ 宿主回归能力与宿主上下文 → Xem 才发 `ui/notifications/initialized`→ Từ đó chủ nhà mới bắt đầu hướng xem 发消息.`notifications/initialized`已被移除,Apps của `ui/notifications/initialized`仍然存在──这个本地握手只建立"一个iframe与一个宿主"之间的桥,不协商 MCP 协议版本、不创建服务器状态、不造传输会话; 桥源的核心请求是全新的自包含请求(新 JSON-RPC id + 完整请求元数据)。

Cầu Apps là một phương ngữ JSON-RPC trên `postMessage`Nó có thể trao đổi`ui/initialize`và `ui/*`thông báo và có thể đại diện các phương pháp trông như`tools/call`- Tôi không biết.

> 桥接是 `postMessage`上的 JSON-RPC 方言──它 có thể được trao đổi `ui/initialize`和 `ui/*`通知,并可以代理形似核心的方法 (nói như)`tools/call`(■)

View gửi `ui/initialize`với `appInfo`và một `appCapabilities`object. host trả về khả năng và bối cảnh host. Chỉ sau khi phản ứng đó View gửi `ui/notifications/initialized`. Người chủ phải chờ cho thông báo ứng dụng này trước khi gửi tin nhắn đến View.

> Xem 发送带 `appInfo`和 `appCapabilities`đối tượng`ui/initialize`◊ chủ nhà trả lại khả năng của mình với chủ nhà trên văn.`ui/notifications/initialized`◊ Chủ nhà phải chờ cho ứng dụng này  sau khi thông báo để xem  gửi tin 

Việc nắm tay địa phương tạo ra một cầu nối giữa một iframe và một host frame. Nó không đàm phán phiên bản giao thức MCP, tạo trạng thái máy chủ, hoặc tạo ra một phiên giao thông.`notifications/initialized`đã bị xóa, trong khi Apps `ui/notifications/initialized`Một yêu cầu cốt lõi được tạo ra bởi một cuộc gọi công cụ nối là một yêu cầu tự lập mới với một ID JSON-RPC mới và dữ liệu siêu dữ liệu yêu cầu đầy đủ.

> Đó là một cuộc giao tiếp giữa một iframe và một host. Nó không thảo luận về bản MCP 协议 版本, không tạo ra tình trạng máy chủ, cũng không tạo ra cuộc giao tiếp.`notifications/initialized`已被移除,而 Apps 的 `ui/notifications/initialized`仍在──桥接工具调用生成的核心请求是一个全新的自包含请求,带新的 JSON-RPC id 和完整请求元数据──

### Khung ngữ cảnh, hành động và hủy bỏ chủ nhà

Người chủ tiếp tục là thẩm quyền sau khi khởi tạo cầu. Một View có thể yêu cầu hành động công cụ, điều hướng, sử dụng clipboard hoặc hiệu ứng đặc quyền khác chỉ thông qua một khả năng mà người chủ quảng cáo. Người chủ xác nhận yêu cầu được nhập, người dùng hiện tại, mục tiêu và lập luận, áp dụng chính sách chấp thuận, và có thể từ chối nó. Nhấp chuột nút và thông điệp cầu hợp lệ bày tỏ ý định; không một trong hai cấp thẩm quyền.

> 桥梁初始化后主持人仍然权威. 查看只能通过主持人声明的能力请求工具动作,导航,剪贴板或其他特权效果. 东方校验类化请求,当前用户,目标和参数,应用审批策略,并可以拒绝.

Chống đối xử với chủ đề, kích thước và khả năng truy cập như thay đổi bối cảnh máy chủ thay vì đầu vào render một lần:

> Đặt chủ đề, kích thước và không có trở ngại như sẽ thay đổi chủ nhà trên các nội dung dưới đây, chứ không phải là một lần nhập:

- Sử dụng các mã màu và kiểu chữ được cung cấp bởi máy chủ, sau đó phản ứng khi chủ đề hoặc sự tương phản thay đổi.
  Trung ngữ翻译: ứng dụng chủ sở hữu cung cấp màu sắc và 排版令牌, và phản ứng khi chủ đề hoặc đối với sự thay đổi sở thích so sánh.
- Để View báo cáo kích thước mong muốn, nhưng để host cap và áp dụng kích thước iframe để nội dung không thể thoát khỏi bố cục của nó hoặc tạo các lớp phủ lừa đảo.
  Trung ngữ翻译:让 View 报告期望尺寸, nhưng bởi chủ nhà封顶并应用 iframe 尺寸, khiến nội dung không thể thoát khỏi bố cục hoặc tạo ra lớp phủ lừa đảo.
- Giữ trật tự bàn phím, tập trung hiển thị, tên truy cập, trạng thái đọc màn hình, tương phản đầy đủ, phóng to và hành vi chuyển động giảm bên trong iframe.
  Trong iframe, giữ giữ lại thứ tự bàn phím, có thể nhìn thấy điểm nhấn, không có trở ngại, trạng thái của máy đọc màn hình, đủ để giảm hiệu quả.
- Kiểm tra lại chuyển đổi trọng tâm giữa các điều khiển chủ và View sau khi thay đổi kích thước và tái trình bày.
  Trung文翻译: 在缩放和重染后重新测试主控件与视控件之间的焦点转移──

Các khả năng có thể bị thu hồi trong khi ứng dụng mở vì người dùng thay đổi tài khoản, thay đổi chính sách, máy chủ bị cách ly hoặc máy chủ hạn chế sự đồng ý.`ui/initialize`Khi hủy bỏ, từ chối các cuộc gọi đặc quyền đang chờ đợi, ngừng hoạt động mạng không còn phù hợp với chính sách, xóa trạng thái render nhạy cảm, và cài đặt lại hoặc quay lại văn bản khi tài nguyên UI không còn được phép.

> 能力 có thể bị hủy bỏ trong khi mở App  user switch accounts  strategy change  server bị tách biệt  host narrow consent                                                                                                                                                                                                                                                `ui/initialize`期间──撤销时: từ chối chờ xử lý quyền điều chỉnh, ngừng không phù hợp với các hoạt động mạng chiến lược, loại bỏ tình trạng nhạy cảm bị nhiễm trùng, và UI 资源 tự nó không được truy cập khi được đăng tải lại hoặc quay lại văn bản.

### Lái lại là một phần của hợp đồng.

Một máy chủ có ý thức về Apps vẫn có thể phục vụ các máy chủ không quảng cáo phần mở rộng UI:

> 感知 Apps's server vẫn có thể dịch vụ không được tuyên bố  mở rộng UI của chủ nhà:

- Trả lại cùng một công cụ mà không cần `_meta.ui`trong `tools/list`- Tôi không biết.
  Trung ngữ翻译:在 `tools/list`中返回不带 `_meta.ui`Đúng như vậy.
- Giữ kết quả văn bản hữu ích cho `tools/call`- Tôi không biết.
  中文翻译:为 `tools/call`Bảo tồn kết quả văn bản hữu ích
- Không chấp nhận`resources/read`cho UI với lỗi khả năng thiếu.
  Trung ngữ翻译:对 UI 的 `resources/read`以缺少能力错误拒绝――
- Không bao giờ giả định một iframe tồn tại khi quyết định liệu công cụ đã hoàn thành hay không.
  Trung文翻译:判断工具是否完成时,永远不要假设 iframe 存在──

```figure
t3-ui-sandbox
```

## Hãy xây dựng nó.

`code/main.py`xây dựng một mô hình giao thức trong quá trình nhỏ mà không có SDK. Nó xác nhận gói yêu cầu hiện tại và giá trị định tuyến HTTP Streamable, quảng cáo Apps thông qua `server/discover`, liệt kê các công cụ và tài nguyên, thực hiện công cụ, và phục vụ một tài nguyên HTML tự do.

> `code/main.py`构建一个不用SDK的小型进程内协议模型――它校验现行请求信封与流动 HTTP 路由值、通过`server/discover`声明 Apps, liệt kê các công cụ và tài nguyên, thực hiện các công cụ và cung cấp một tài nguyên HTML tự chứa.

Mô hình nhận được các cơ thể đã phân tích và tiêu đề định tuyến. Nó không phải là một bộ điều chỉnh HTTP hoàn chỉnh và không phân tích `Content-Type`hoặc `Accept`Sử dụng bài học 09 cho bộ điều chỉnh HTTP Streamable đầy đủ cần `Content-Type: application/json`và một `Accept`giá trị chứa cả hai `application/json`và `text/event-stream`- Tôi không biết.

> Mô hình nhận được chủ thể và đường dẫn đã được phân tích. Nó không phải là một ứng dụng HTTP hoàn chỉnh, cũng không phân tích.`Content-Type`Hoặc`Accept`△完整的 Streamable HTTP 适配器 要求 `Content-Type: application/json`且 `Accept`值同时包含 `application/json`Với`text/event-stream`) Xem Bài học 09:

Đi đi.

> 运行:

```bash
cd phases/13-tools-and-protocols/14-mcp-apps
python3 code/main.py
python3 -m unittest discover code/tests -v
```

Kiểm tra bốn điều trong đầu ra:

> Trong việc xuất khẩu kiểm tra bốn điều:

1. Mỗi cuộc gọi đều độc lập.
   Trung ngữ翻译: Mỗi调用 đều độc lập.
2. Mọi yêu cầu đều có`_meta`khả năng.
   Trung ngữ翻译: Mỗi yêu cầu đều có`_meta`能力──
3. `resources/list`trả lại mô tả ổn định trước khi đọc tài nguyên nào.
   Trung ngữ翻译:`resources/list`Trong bất kỳ tài nguyên nào đọc được trước khi quay lại trình diễn viên ổn định.
4. Mọi kết quả đều có`resultType`và dữ liệu siêu dữ liệu danh tính máy chủ.
   Trung ngữ翻译: mỗi kết quả có`resultType`和 máy chủ danh tính dữ liệu:
5. Không có nhân danh phiên bản cốt lõi xuất hiện.
   Trung ngữ翻译:不出现任何核心会话标识符──

## Sử dụng nó để kiểm tra

Bắt đầu với `server/discover`- Đảm bảo`io.modelcontextprotocol/ui`xuất hiện trong bản đồ mở rộng máy chủ.`tools/list`hai lần, một lần với khả năng Apps và một lần mà không có nó. Câu trả lời đầu tiên tuyên bố tài nguyên. thứ hai vẫn là một công cụ chỉ có văn bản có thể sử dụng.

> Từ `server/discover`开始── xác nhận`io.modelcontextprotocol/ui`xuất hiện máy chủ mở rộng映射中──然后调用 `tools/list`两次,一次带 Apps 能力、一次不带;; thứ nhất là nguồn khai báo ứng dụng; thứ hai vẫn là các công cụ văn bản thuần túy có sẵn.

Đọc `ui://notes/timeline.html`Tìm kiếm HTML cho `hostOrigin`và `event.origin`hai đường đó là bằng chứng rõ ràng nhất cho thấy cầu không sử dụng mục tiêu.

> 读取 `ui://notes/timeline.html` Trong HTML tìm kiếm `hostOrigin`和 `event.origin`守衛──These two lines are the least visible evidence of "bridge connection not using common distribution goal" (Những đường này là những bằng chứng nhỏ nhất có thể thấy về việc "các đường nối không sử dụng mục tiêu chung").

## Chuyển nó đi.

Bài học này sẽ đi theo `outputs/skill-mcp-apps-spec.md`Sử dụng nó để xem xét một hợp đồng ứng dụng trước khi viết mã khung. Nó buộc tác giả phải nêu bao bì cốt lõi hiện tại, đàm phán mở rộng, sự trở lại, tài nguyên UI, chính sách cache, CSP, quyền, phương pháp cầu và ranh giới đồng ý.

> 本课产 出 `outputs/skill-mcp-apps-spec.md` Trước khi viết khung mã, sử dụng nó để kiểm tra 契约.

## Tập luyện bài tập

1. Thay đổi khả năng của khách hàng thành một bản đồ mở rộng trống.`tools/list`giữ công cụ nhưng loại bỏ kết nối UI.
   Trung ngữ翻译:把客户端能力改为空的扩展映射──确认 `tools/list`Bảo tồn công cụ nhưng di chuyển UI 绑定.
2. Gửi đi`Mcp-Name: ui://notes/other.html`với một cơ thể đọc thời gian.`-32020`- Tôi không biết.
   Trung ngữ翻译:发送 `Mcp-Name: ui://notes/other.html`, chủ thể đã đọc thời gian .`-32020`
3. Thay đổi nguồn tài nguyên thành `cacheScope: private`Mô tả tình trạng cụ thể cho người dùng làm cho nó có lý do.
   Trung ngữ翻译:把资源改为`cacheScope: private`◊ mô tả điều kiện cụ thể của người dùng về việc hỗ trợ
4. Dời kịch bản lên `https://static.example.com/app.js`Thêm nguồn gốc đó vào `resourceDomains`và giải thích rủi ro chuỗi cung ứng mới.
   Trung ngữ翻译:把脚本移到 `https://static.example.com/app.js`                                                                                                                                                                                                                                                              `resourceDomains`Và giải thích các chuỗi cung ứng mới.
5. Thêm một `notes_open`công cụ và hướng nút nhấp qua máy chủ. Giữ sự chấp thuận của người dùng trong máy chủ.
   Trung ngữ翻译:添加 `notes_open`工具并让按点击经由宿主路由──把用户批准留在宿主──

## Từ khóa  Từ khóa nhanh chóng

| Term | Meaning |
|------|---------|
| MCP Apps | Optional extension for interactive HTML rendered by an MCP host |
| `io.modelcontextprotocol/ui` | Extension identifier advertised by both peers |
| `ui://` | Resource scheme for an App's UI template |
| `text/html;profile=mcp-app` | MIME type for MCP App HTML |
| `server/discover` | Current RPC for protocol and capability discovery |
| `resources/list` | Mandatory resource listing method when the server advertises resources |
| `resultType` | Required discriminator for modern successful results |
| `ui/initialize` | First Apps bridge request, separate from removed core initialization |
| `ui/notifications/initialized` | Apps View readiness notification sent after the host responds |
| CSP | Browser policy that restricts scripts, styles, images, and network origins |
| Text fallback | Tool behavior retained for a host without Apps support |

> **【中文解读】**术语速查(中英对照):MCP Apps= được mở rộng bởi MCP 宿主染交互式 HTML 的可选扩展;`io.modelcontextprotocol/ui`= Biểu báo của các biểu tượng mở rộng;`ui://`=Sự quản lý tài nguyên của ứng dụng UI 模板;`text/html;profile=mcp-app`=MCP App HTML của MIME 类型;`server/discover`= RPC hiện hành của thỏa thuận và khả năng phát hiện;`resources/list`= phương pháp danh sách tài nguyên được yêu cầu sau khi các máy chủ tuyên bố tài nguyên;`resultType`= n định nghĩa cần thiết của kết quả thành công hiện đại;`ui/initialize`=Lời yêu cầu đầu tiên của ứng dụng 桥接, không liên quan đến việc khởi động lõi đã được di chuyển;`ui/notifications/initialized`= host trả lời sau khi phát hành bởi View 绪通知;CSP = hạn chế văn bản, phong cách, hình ảnh và chiến lược trình duyệt của nguồn mạng;Text fallback = vì không hỗ trợ ứng dụng của host lưu trữ văn bản giảm 

## Xem thêm 延伸阅读

- [MCP 2026-07-28 base protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic)
  Trung ngữ翻译:2026-07-28 基础协议规范──
- [MCP Apps overview](https://modelcontextprotocol.io/extensions/apps/overview)
  Trung文翻译:MCP Apps 扩展总览。
- [MCP Apps build guide](https://modelcontextprotocol.io/extensions/apps/build)
  Trung文翻译:MCP Apps 构建指南。
- [Official extension support matrix](https://modelcontextprotocol.io/extensions/client-matrix)
  Trung ngữ翻译:官方扩展支持矩阵 (中文翻译:官方扩展支持矩阵)
