# MCP Conformance Engineering: Versioning, Evidence, and Operations  MCP 一致性工程: phiên bản hóa, chứng cứ và vận hành

> Một máy chủ không phù hợp vì con đường hạnh phúc của nó hoạt động thông qua một SDK. Sự phù hợp sống tại dây, tại ranh giới phiên bản, thông qua các trung gian và trong thời gian quay trở lại.

> **【中文解读】**Một máy chủ sẽ không được bởi vì "sự chơi vui vẻ trong một SDK đã chạy qua" tính đến phù hợp (conformant) ⋅ phù hợp sống ở bốn nơi: hình dạng (线形) ⋅ dây (线) ⋅ trên ⋅ phiên bản biên giới trên ⋅ xuyên qua thiết bị trung gian ⋅ cũng như trong quá trình xoay vòng.

> **【拓展：MCP→质量工程与 SRE】**Mỗi phương tiện xuất hiện trong đây: mẫu vàng với thử nghiệm tiêu cực, phòng chống tấn công giảm cấp, phân biệt truyền đại lý, phát hành cửa và chứng nhận được quay lại là các chủ đề điển hình của SRE về kỹ thuật giao thức (HTTP/TLS, bộ thống nhất, bảo vệ giảm cấp, phát hành các loại hình khác nhau)`resultType`判判器、镜像路由头、通知不变量、以及 2026-07-28 的自含元数据──它与Phase 13 · 29(可靠性) 和Phase 13 · 30(注册中心准入) 首尾相接:29 管"出事怎么活",30 管"进门前怎么审",本课管"凭什么说它一直对"──

>  **【前置】**Học本课前请先掌握:Phase 13 · 09(MCP 传输Streamable HTTP 与头部) Phase 13 · 17(网关与注册中心中间设备与镜像头) Phase 13 · 30(注册中心准入pin、证据摘要与回滚目标)

**Type:** Build | **类型:** 动手实践
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 09 (transports), Phase 13 · 17 (gateways), Phase 13 · 30 (registry admission) | **前置知识:** Phase 13 · 09（传输）、Phase 13 · 17（网关）、Phase 13 · 30（注册中心准入）
**Time:** ~100 minutes | **时间:** 约 100 分钟

## Mục tiêu học tập

- Chuyển đổi các quy tắc MCP quy định thành bản ghi âm bằng vàng và âm.
  Trung文翻译:把规范性的 MCP 规则变成黄金与负面线格式转录(transcript) 』
- Hãy giữ chặt .`2026-07-28`hành vi tách biệt với những hậu quả của sự cố.
  Trung ngữ翻译:让严格的 `2026-07-28`行为与有界的旧版回退 (trở lại) giữ phân biệt.
- Để phân biệt các trường phụ chưa biết từ một trường không rõ không xác định `resultType`- Tôi không biết.
  Trung文翻译:区分"增量式未知字段"与"非法的未知 `resultType`" "..
- So sánh bằng chứng JSON-RPC nguyên liệu với một dạng xem SDK bình thường.
  Trung文翻译:把原始 JSON-RPC 证据与SDK 归一化后的视图做差分比较──
- Bằng chứng về tính toàn vẹn của tiêu đề và cơ thể qua một ranh giới thực.
  Trung ngữ翻译: xuyên qua biên giới trung gian thực sự chứng minh sự toàn vẹn của đầu và chủ thể.
- Các bản phát hành Gate với bản sao đã được chỉnh sửa, sức khỏe và bằng chứng quay lại.
  Trung ngữ翻译:用脱敏后的转录、健康与回滚证据为发布把关──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**"SDK 里调 `tools/list`得到到了工具、集成测试绿了" kết quả này trả lời không phải là câu hỏi thực sự: request带带没带现代的单请求元数据?`resultType`Có phải là thực hiện trực tuyến hay SDK 合成? tương lai mới增字段 sẽ được giữ lại? một lỗi hiện đại sẽ không bị bất ngờ kích hoạt phiên bản cũ tay cầm? đại diện giữ lại mã nguồn và lỗi? thông báo trình tự hóa có phát ra phản ứng bị cấm không?运维能不能不存储 bí mật Để chứng minh lý do phát hành một lần hoặc quay lại? sự đồng nhất là một nhóm các không biến thể có thể quan sát được Trước khi bạn phát hiện vấn đề, hãy tạo ra một cái máy thử nghiệm có thể nắm bắt những không biến này (HARNES)

Khách hàng của anh gọi`tools/list`thông qua SDK và nhận được các công cụ.

> Khách hàng của bạn thông qua SDK 调用 `tools/list`Không có công cụ, tập hợp kiểm tra đã qua.

Kết quả này để lại những câu hỏi quan trọng không có câu trả lời:

> Kết quả này để lại nhiều câu hỏi quan trọng không có câu trả lời:

- Liệu yêu cầu có chứa các metadata giao thức hiện đại theo yêu cầu?
- Có `MCP-Protocol-Version`- `Mcp-Method`, và`Mcp-Name`phù hợp với cơ thể JSON-RPC?
- Câu trả lời có chứa một câu trả lời hợp lệ `resultType`trên dây, hay SDK đã tổng hợp một?
- Khách hàng có thể bảo tồn một lĩnh vực phụ gia trong tương lai không?
- Một sai lầm hiện đại được công nhận có vô tình gây ra một cú tay cổ tích?
- Một proxy đã bảo tồn trạng thái nguồn gốc và lỗi JSON-RPC?
- Máy thông báo seriesiezer đã phát ra một phản ứng cấm?
- Liệu các hoạt động có thể chứng minh tại sao một bản phát hành được thúc đẩy hoặc bị lật lại mà không lưu trữ bí mật?

Conformance là một tập hợp các biến động có thể quan sát được. Hãy xây dựng một dây đeo bắt được những biến động đó trước khi giao thông sản xuất phải phát hiện chúng.

> Một tính chất là một tập hợp các không biến thể có thể quan sát được. Trước khi dòng sản xuất phải phát hiện chúng, trước tiên xây dựng một cơ sở thử nghiệm có thể nắm bắt những không biến thể này.

```figure
mcp-conformance-operations
```

## Bắt đầu với phiên bản Eras.

> **【中文解读】**两纪元两套规则,绝不做"一个宽松验证器同时吃两种形态"──现代纪元(`2026-07-28`): tự chứa các yêu cầu`params._meta.io.modelcontextprotocol/protocolVersion`Với`.../clientCapabilities`, trần truồng `protocolVersion`别名是形的;镜像路由头在场时必须与 JSON-RPC 主体一致; thành công kết quả带 `resultType`旧纪元 截至 `2025-11-25`): Thời gian khởi đầu sớm, khách hàng chọn định kỷ nguyên cũ, không có `resultType`Kết quả chỉ được giải thích là toàn diện. phân chia ngăn chặn "những hình thức hiện đại đối với các kết quả ngược lại nhận được chứng minh yếu hơn".`server/discover`hoặc được nhận ra là lỗi thời), không có lý do gì.`-32020/-32021/-32022`降级; trở lại mô hình trước tiên làm một lần có giới hạn hiện đại tìm kiếm, siêu thời gian /空响应 /断连只是"无结论"、不证明旧版,只有显然允许的端点才可做有界旧版探测,且必须验证它`initialize`Kết quả sau đó là chọn các phân đoạn cũ.

>  **【类比】**版本纪元像充电口的"全程 USB-C"与"备用转接"──默认只走 USB-C(严格模式);转接(旧版回退) chỉ cho đăng ký trong danh sách trắng sử dụng thiết bị cũ, và trước tiên phải xác nhận rằng thiết bị đó là thiết bị cũ thật sự(lượng di sản hợp pháp`initialize`证据) 不能因为"新线没插上" (超时/无响应) 就默认对方是老设备――否则一个干扰你的中间人就能靠"弄丢现代响应"把整个连接拖回旧协议,这是降级攻击 (降级攻击) 的套路――

MCP `2026-07-28`sử dụng tự nhiên mỗi yêu cầu metadata.`params._meta.io.modelcontextprotocol/protocolVersion`và `params._meta.io.modelcontextprotocol/clientCapabilities`. Các khóa tên chính xác quan trọng;`protocolVersion`hoặc `clientCapabilities`khi các tiêu đề định tuyến được hiển thị ở biên giới HTTP, giá trị của chúng phải phù hợp với cơ thể JSON-RPC. Kết quả thành công hiện đại mang lại`resultType`- Tôi không biết.

> MCP `2026-07-28`Sử dụng tự chứa của từng yêu cầu dữ liệu.`params._meta.io.modelcontextprotocol/protocolVersion`和 `params._meta.io.modelcontextprotocol/clientCapabilities`                                                                                                                                                                                                                                                              `protocolVersion`Hoặc`clientCapabilities`别名是形的──镜像路由头 xuất hiện trên HTTP 边界时, giá trị của nó phải phù hợp với JSON-RPC 主体──现代成功结果携带`resultType`

Các phiên bản thông qua `2025-11-25`sử dụng thời kỳ khởi tạo sớm hơn.`resultType`được giải thích là hoàn chỉnh chỉ sau khi khách hàng đã chọn thời kỳ trước đó.

> 截至 `2025-11-25`                                                                                                                                                                                                                                                              `resultType`Kết quả của phiên bản cũ, chỉ sau khi khách hàng đã chọn thời gian sớm hơn, mới được giải thích đầy đủ.

Đừng tạo ra một xác nhận cho phép chấp nhận cả hai hình dạng cùng một lúc. Sử dụng hai nhánh:

> Đừng làm một "đồng nhận hai hình thức" của một chứng minh rộng rãi.

| Branch | Entry evidence | Missing `resultType` | Initialization |
|---|---|---|---|
| Modern | Successful `server/discover` or recognized modern response | Invalid | Not the default path |
| Legacy | Configured allowlist plus a valid legacy `initialize` result after an inconclusive modern probe | Interpreted as complete | Required by that era |

> 分支表: 现代分支的入口证据是成功的 `server/discover`Hoặc được nhận ra trong hiện đại, thiếu sót`resultType`视为非法,初始化不是默认路径; 旧版分支的入口证是"已配置的允许 list + 一次无结论的现代探测后有效的旧版 `initialize`Kết quả"`resultType`Được giải thích là hoàn chỉnh, khởi nghiệp là điều cần thiết trong thời đại này.

Sự tách biệt ngăn cản một người đồng nghiệp hiện đại bị hình dạng sai trái được khen thưởng bằng sự xác nhận yếu hơn.

> Sự phân tách này ngăn chặn một hình dạng hiện đại đối với cuối cùng được chứng minh yếu hơn.

### Chế độ nghiêm ngặt.

Chế độ nghiêm ngặt đòi hỏi chứng minh hành vi hiện đại.`server/discover`chứng minh chi nhánh hiện đại. Một lỗi JSON-RPC hiện đại được công nhận cũng chứng minh điều đó. sửa lỗi yêu cầu hoặc dừng lại. Không bao giờ hạ cấp vì máy chủ đã quay lại`-32020`- `-32021`, hoặc`-32022`- Tôi không biết.

> 严格模式要求现代行为正面证明: một lần thành công `server/discover`证明现代分支, một được nhận dạng现代 JSON-RPC 错误 cũng chứng minh nó.`-32020``-32021`Hoặc`-32022`Và hạ cấp.

### Phương thức quay lại

Phương thức fallback thực hiện một thăm dò hiện đại có giới hạn. Một thời gian nghỉ, câu trả lời trống, kết nối đóng hoặc phản ứng không được nhận ra là không kết luận. Nó không chứng minh rằng đồng nghiệp là di sản. Chỉ một điểm cuối được cấu hình hoặc liệt kê rõ ràng cho sự tương thích sau đó có thể nhận được một thăm dò di sản có giới hạn, và khách hàng chỉ chọn nhánh di sản sau khi xác nhận các bản thăm dò đó.`initialize`kết quả và đàm phán sửa đổi kế thừa.

> Trình quay trở lại trước một lần có giới hạn hiện đại tìm kiếm. Trình độ quá thời gian, không đáp ứng, không kết nối hoặc không thể nhận ra được đáp ứng là "không kết luận" chúng không chứng minh kết thúc là phiên bản cũ. Chỉ có một điểm cuối được định nghĩa rõ ràng hoặc được đưa vào danh sách dung dung hợp, mới có thể nhận được một lần có giới hạn tìm kiếm cũ; và khách hàng chỉ có thể xác nhận được lần tìm kiếm đó.`initialize`Kết quả sau khi sửa đổi phiên bản cũ được thảo luận,才选定旧分支.

Fallback không là  cố gắng di sản sau bất kỳ lỗi nào. Một lỗi hiện đại được công nhận chứa thông tin sửa chữa hữu ích. Việc hạ cấp sau đó có thể che giấu sự không phù hợp của tiêu đề, tuyên bố khả năng bị thiếu hoặc phiên bản không được hỗ trợ.

> Trở lại không phải là "trước bất kỳ lỗi nào sau khi thử phiên bản cũ"― một lỗi hiện đại được nhận ra mang lại thông tin sửa chữa hữu ích; sau đó giảm, có thể che giấu sự không phù hợp của đầu, tuyên bố khả năng thiếu hoặc phiên bản không được hỗ trợ―

Điều này ngăn chặn một kẻ tấn công, tắt điện hoặc lọc proxy buộc phải hạ cấp bằng cách loại bỏ phản ứng hiện đại.

> Điều này ngăn chặn kẻ tấn công  cố hoặc quá kiểu đại diện bằng cách "đánh mất phản ứng hiện đại" áp lực hạ cấp  phải đưa ra chiến lược điểm kết thúc  không kết luận của quan sát hiện đại  xác thực bằng chứng cũ và ghi chép kỷ lục được chọn 

Viết thời gian được chọn bên cạnh mỗi bản ghi.

> Để ghi lại lịch sử được chọn là bên cạnh mỗi bài đăng chuyển tiếp. Không có sự thật này, một đoạn văn bị thiếu sót có thể xảy ra lần này trong quá trình kiểm tra.

## Xây dựng một bản sao Transcript Corpus xây dựng một bộ nhớ chuyển đổi

> **【中文解读】**转录(transcript)fixture  ghi lại là "true transcending the boundaries of things" 头部、请求体、响应状态码、响应体、选定纪元而不仅仅"SDK 调用回归了什么"──语料库分两类:黄金转录证明"接受行为"(元数据与头部匹配、`resultType`合法、通知无响应等); 负面转录证明"拒绝行为" ((头部与主体不匹配、未知判别器、代理吞错等)  Mỗi trường hợp sử dụng tiêu cực phải khẳng định từ chối biên giới và ổn định lỗi码"调用失败了"太弱,代理造的500 和源站的`-32020`Đàn thành gọi là thất bại, nhưng kể cho cuộc sống của họ là hoàn toàn khác nhau.

Một thiết bị ghi chép ghi lại những gì vượt qua ranh giới, không chỉ gọi SDK:

> Một phần mềm chuyển âm ghi lại nội dung vượt biên giới, không chỉ sử dụng SDK:

```json
{
  "name": "golden-modern-list",
  "era": "modern",
  "headers": {
    "MCP-Protocol-Version": "2026-07-28",
    "Mcp-Method": "tools/list"
  },
  "request": {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {
      "_meta": {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {}
      }
    }
  },
  "responseStatus": 200,
  "responseBody": {
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
      "resultType": "complete",
      "tools": []
    }
  }
}
```

Hãy giữ hai lớp đồ đạc.

> 保留两类 固定──

### Những bản ghi vàng.

Những bản ghi vàng chứng minh hành vi được chấp nhận:

> 黄金转录证明" hành vi được chấp nhận":

Một bản ghi vàng là chính xác, không lớn. Giữ ID biến động và thời gian ấn định hoặc bình thường hóa chúng trước khi so sánh.

> 黄金转录要精确,不要大大.                                                                                                                                                                                                                                                         

- yêu cầu khám phá hoặc phương pháp hiện đại với metadata và tiêu đề phù hợp
- kết quả hoàn chỉnh với các trường yêu cầu
- `input_required`kết quả khi phương pháp có thể yêu cầu nhập nhiều hơn
- kết quả mở rộng chỉ sau khi khả năng tương ứng được quảng cáo
- kết quả thừa kế mà không có `resultType`, nhưng chỉ trong thời kỳ di sản được chọn
- xử lý thông báo mà không có phản hồi JSON-RPC

Một bản ghi vàng là chính xác, không lớn. Giữ ID biến động và thời gian ấn định hoặc bình thường hóa chúng trước khi so sánh.

### - Tác giả âm tính.

Các bản ghi âm âm chứng minh hành vi từ chối:

> 负面转录证明" hành vi bị từ chối":

- không phù hợp đầu và thân
- thiếu khả năng yêu cầu
- phiên bản giao thức không được hỗ trợ
- mất hiện đại `resultType`
- không được biết đến hoặc không được quảng cáo `resultType`
- phản ứng `jsonrpc`khác ngoài `2.0`hoặc ID khác nhau về giá trị hoặc loại JSON
- một phản ứng có cả hai `result`và `error`, hoặc cả hai
- một lỗi không có số nguyên`code`và dây `message`
- lỗi giao thức được biết đến được gán đến tình trạng HTTP sai
- phản ứng được phát hành để thông báo
- bọc JSON-RPC bị biến dạng sai
- sự sụp đổ của lỗi giao thức

Đối với mỗi trường hợp tiêu cực, khẳng định giới hạn từ chối và mã lỗi ổn định. Câu lạc không thành công quá yếu.`-32020`cả hai có thể trông giống như thất bại trong khi kể cho các nhà điều hành những câu chuyện hoàn toàn khác nhau.

> Đối với mỗi trường hợp sử dụng tiêu cực, tuyên bố từ chối biên giới và định hình sai lầm có mã số không thành công.`-32020`Có vẻ như chúng đều thất bại, nhưng chúng nói cho câu chuyện về vận hành hoàn toàn khác nhau.

Thiết bị không phù hợp tiêu đề phải bao gồm phản ứng HTTP 400 JSON-RPC thực tế của máy chủ với ID yêu cầu phù hợp và mã lỗi `-32020`. Thực hiện điều đó tự động bất cứ khi nào người xác nhận địa phương quan sát `HeaderMismatch`; không làm cho xác minh phản ứng là cờ cố định tùy chọn. Một trường hợp với HTTP 500 và không có cơ thể thất bại ngay cả khi mã từ chối địa phương là đúng. Một vòng đeo dừng lại sau khi xác nhận yêu cầu của riêng nó ném đã kiểm tra chỉ bản thân, không phải hành vi dây của máy chủ.

> 头部不匹配的固定 必须包含服务器真实的 HTTP 400 JSON-RPC 响应带匹配的请求 ID 和错误码 `-32020` Chỉ cần máy kiểm tra địa phương quan sát `HeaderMismatch`, hãy tự động bắt buộc điều này; đừng coi thử nghiệm đáp ứng như một sự cố có thể chọn 开关. Một ví dụ sử dụng của "HTTP 500 且无响应体", ngay cả khi từ chối mã là đối với của cũng là thất bại. Một cái test架 dừng lại sau khi yêu cầu của mình đã bị thả bất thường, chỉ thử nghiệm bản thân nó, không có hành vi trên mạng của máy chủ thử nghiệm.

Dự án phù hợp chính thức của MCP hữu ích như một bộ phận bên ngoài và tham chiếu phiên bản. Giữ bản sao chép địa phương của bạn cũng vậy. Chúng ghi lại proxy, SDK, xác thực, mở rộng và đường phát hành của bạn, mà một bộ phận chung không thể biết.

> 官方 MCP 一致性项目适合作用于外部套件和带版本的参照──但本地转录也应该保留:它们捕获的是你的代理、SDK、认证、扩展和发布路径这些是一般性套件不可能知道──

## Giá trị tiêu đề phải phù hợp với cơ thể RPC .

> **【中文解读】**现代 Streamable HTTP 允许中间设备使用镜头部进行路由或策略执行, nhưng JSON-RPC 主体才是协议的事实来源不匹配是完整性故障,不是"二选一挑一个"提示──验证顺序:先解析校验 JSON-RPC 信封与元数据类型,再比对`MCP-Protocol-Version`Với tên không gian trong chủ đề`Mcp-Method`Với`method`、 có đường từ tên gọi thời gian đối với `Mcp-Name`,Phương trình và khác nhau được xác định sau khi quyết định liệu phiên bản và khả năng có được hỗ trợ không.`-32020`Phiên bản "与" không được hỗ trợ`-32022`"区分开,也住了" mạng lưới dựa trên tên miền được ủy quyền, nguồn gốc dựa trên tên miền khác được thực hiện" của tấn công.`Mcp-Name`含不安全字符时走 Base64 UTF-8 哨兵解码,解码失败或首尾空白都以 `-32020`拒绝.

Trong HTTP Streamable hiện đại, người trung gian có thể định tuyến hoặc thực thi chính sách bằng cách sử dụng tiêu đề gương. Cơ thể JSON-RPC vẫn là nguồn nguyên tắc.

> Trong HTTP Streamable hiện đại, thiết bị trung gian có thể sử dụng các phương pháp định tuyến hoặc thực hiện trên đầu kính, nhưng JSON-RPC chủ thể vẫn là nguồn thực tế của thỏa thuận.

Được xác nhận theo thứ tự này:

> 按以下顺序验证:

1. Phân tích và xác nhận các loại bao bì và metadata JSON-RPC.
2. So sánh`MCP-Protocol-Version`với `params._meta.io.modelcontextprotocol/protocolVersion`- Tôi không biết.
3. So sánh`Mcp-Method`với `method`- Tôi không biết.
4. Khi phương pháp có tên định tuyến, so sánh `Mcp-Name`với giá trị cơ thể tương ứng.
5. Sau khi bình đẳng được thiết lập, quyết định liệu phiên bản và bộ khả năng phù hợp có được hỗ trợ hay không.

Trật tự này phân biệt sự không phù hợp.`-32020`từ phiên bản không hỗ trợ `-32022`Nó cũng ngăn chặn một cửa cổng từ ủy quyền tên tiêu đề trong khi nguồn thực hiện một tên cơ thể khác.

> Sự sắp xếp này không phù hợp.`-32020`Với phiên bản không được hỗ trợ `-32022`区分开, cũng ngăn chặn tình huống "net关按头部名字授权"", còn nguồn站执行另主体名字"

Tên trường HTTP không nhạy cảm với trường hợp, trong khi các giá trị của chúng vẫn nhạy cảm với trường hợp. Tiêu chuẩn hóa tên tiêu đề trước khi tìm kiếm và từ chối bản sao mâu thuẫn. Đối với không gian trắng không an toàn, không phải ASCII, hoặc dẫn hoặc theo dõi `Mcp-Name`, giải mã chính xác `=?base64?{Base64EncodedValue}?=`UTF-8 Sentinel trước khi so sánh nó với cơ thể. Tháo một Sentinel không đầy đủ, Base64, không hợp lệ UTF-8, hoặc giá trị không an toàn nguyên liệu với `-32020`. Không gian trắng bao quanh nguyên liệu là không hiệu lực ngay cả khi cơ thể chứa các ký tự tương tự vì giá trị đó yêu cầu mã hóa sentinel trước khi vận chuyển.

Một trung gian có thể từ chối HTTP bị trục trặc trước khi yêu cầu đạt đến máy chủ MCP, vì vậy thất bại của nó có thể là lỗi HTTP mà không có JSON-RPC.

## Các trường không biết không phải là kết quả không biết.

> **【中文解读】**前向兼容需要两条不同的规则──增量式未知字段:结果对象和 结果对象和 结果`_meta`映射可以新增字段透明代理通常应保留(转发), ứng dụng客户端可以忽略,但要靠差分测试让"SDK 丢掉它"变成一个显然的有意的决定――未知的`resultType`: nó là một thiết bị phân định chu kỳ đời, không biết hoặc không tuyên bố, không thể được coi là hoàn chỉnh. Khách hàng không biết mình sẽ bỏ rơi chu kỳ đời nào, phải từ chối.`tools/list`需要工具 数组且描述符合法,`task`Kết quả cần`taskId`/ trạng thái/ thời gian/`ttlMs`, hoàn thành kết quả cần hợp pháp`completion`Đối tượng:

Sự tương thích tương thích đòi hỏi hai quy tắc khác nhau.

> 前向兼容需要两条不同的规则──

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +

Các đối tượng kết quả và `_meta`bản đồ có thể có được các trường. Một người xác nhận nên bảo tồn hoặc bỏ qua một trường phụ gia theo vai trò của nó, trừ khi trường vi phạm một hợp đồng được đặt phòng.`futureHint`bên cạnh một kết quả được biết đến.

> kết quả đối tượng`_meta`映射可以新增字段. 验证器应根据自己的角色保留或忽略增量字段,除非该字段违反保留契约. 举例把完整原始结果留在证据里,并接受已知结果旁边的.`futureHint`

Nếu bạn là một proxy minh bạch, bảo tồn một trường không rõ thường an toàn hơn là tước bỏ nó. Nếu bạn là một khách hàng ứng dụng, bỏ qua nó có thể là hợp lệ. Thử nghiệm khác biệt của bạn vẫn nên tiết lộ rằng SDK đã bỏ qua nó vì vậy hành vi là cố ý.

> Nếu bạn là một đại lý minh bạch, giữ các đoạn không biết thường an toàn hơn là bỏ nó; nếu bạn là một ứng dụng khách hàng, bỏ qua nó có thể hợp pháp.

### Không biết`resultType`♬ kết quả không rõ Type

`resultType`là một phân biệt đối xử.`complete`hoặc `input_required`. Một phần mở rộng chỉ có thể thêm một giá trị khác khi khả năng của nó được quảng cáo.`task`trong bối cảnh khả năng đàm phán đó.

> `resultType`là một máy phân định.`complete`Hoặc`input_required`; mở rộng chỉ trong trường hợp khả năng đối phó đã được tuyên bố để tăng giá trị khác nhau. Ví dụ: Nhiệm vụ`task`

Một người phân biệt đối xử không được biết hoặc không được quảng cáo không thể được coi là hoàn chỉnh. Khách hàng không biết chu kỳ cuộc sống mà nó sẽ loại bỏ.

> Các thiết bị phân định không được biết hoặc không được tuyên bố không thể được an toàn như là hoàn chỉnh.

Do đó, phản ứng nguyên chất tương tự có thể chứa một trường không rõ được chấp nhận và một loại kết quả không rõ được không chấp nhận.

> Do đó, cùng một phản ứng ban đầu có thể chứa cả các đoạn không biết được chấp nhận được, cũng có thể chứa các loại kết quả không biết được chấp nhận được.

Các phân biệt chỉ là lớp đầu tiên.`tools/list`kết quả cần một `tools`array có mô tả có tên không trống độc đáo, mô tả hữu ích và gốc đối tượng `inputSchema`giá trị.`task`kết quả chỉ có giá trị cho một người đủ điều kiện `tools/call`với khả năng và yêu cầu của nhiệm vụ`taskId`, tình trạng được biết đến, tạo ra và cập nhật các dấu thời gian, và `ttlMs`, cộng với một khoảng thời gian bỏ phiếu tùy chọn hợp lệ.`completion/complete`kết quả đòi hỏi một `completion`đối tượng không quá 100 giá trị chuỗi, một số nguyên không âm tùy chọn `total`không nhỏ hơn các giá trị trả lại, và một tùy chọn Boolean `hasMore`Một chữ viết thật rõ ràng.`resultType`không thể làm cho một tải trọng hữu ích bị biến dạng phù hợp.

> 判斷器只是第一层,后后还需要校验方法特定的载荷:完整的 `tools/list`Kết quả cần`tools`Số, mô tả cần có tên không trống duy nhất, mô tả hữu ích và gốc đối tượng.`inputSchema`-`task`Kết quả chỉ có trong các nhiệm vụ  năng lực `tools/call`里才合法, cần `taskId`、 đã biết trạng thái 、 tạo và cập nhật thời gian  và `ttlMs`, ngoại pháp có thể lựa chọn 间隔;complete `completion/complete`Kết quả cần`completion`Đối tượng 字符串 giá trị không vượt quá 100 个 √ có thể chọn số nguyên tích không âm`total`Không phải nhỏ hơn số lượng giá trị trả lại, có thể chọn được`hasMore`│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │`resultType`Ơn n ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng ng

## Thông báo không thay đổi  thông báo không thay đổi số lượng

Một thông báo JSON-RPC không có `id`. Người nhận không được gửi một phản ứng thành công hoặc lỗi JSON-RPC.

> 一条 JSON-RPC 通知没有 `id`❖ Người nhận phải gửi JSON-RPC thành công hoặc sai

Đối với một hình thức thông báo HTTP được chấp nhận, dây đeo sẽ chờ đợi một HTTP `202`với một cơ thể trống rỗng.`2026-07-28`không xác định các thông báo trung tâm từ client đến server trên Streamable HTTP. mẫu sử dụng thông báo mở rộng khóa học không gian tên chỉ để kiểm tra không biến động serializer một chiều. Đừng trình bày nó như một phương pháp trung tâm mới.

> Đối với HTTP  thông báo được chấp nhận hình thức, test架期望 HTTP `202`和空主体──MCP `2026-07-28`Không xác định lõi của khách hàng đến máy chủ Streamable HTTP 通知―― ví dụ sử dụng một không gian đặt tên của chương trình mở rộng thông báo, chỉ để thử nghiệm đơn phương hướng trình tự hóa không thay đổi; đừng coi nó như một phương pháp lõi mới――

Hãy thử máy truyền hình, không chỉ người xử lý.`None`trong khi middleware gói nó trong một đối tượng thành công JSON.

> 测序列化器, không chỉ là bộ xử lý. bộ xử lý có thể quay lại.`None`, và trung gian đưa nó vào một đối tượng thành công JSON.

## Thêm một SDK khác biệt   tăng SDK 差分

> **【中文解读】**SDK thường chuyển các đối tượng trên mạng thành loại ngôn ngữ thuận tiện, điều này hữu ích, nhưng các đối tượng sau khi kết hợp không chứng minh được "sự nhận được gì"  Chụp bốn thứ cho mỗi mục  SDK 解码前的原始状态、头部、响应体; SDK 归纳的回值或异常; 选择纪元的期望语义投影; SDK 升升、合成、剥除或改变的字段;; ví dụ cho phép SDK 专门移除已知的线上簿记字段(`resultType``_meta``ttlMs``cacheScope`) đồng thời so sánh ứng dụng tải, nhưng`futureHint`Được bỏ rơi như một báo cáo thực tế đoạn ngữ nghĩa không rõ đã biến mất. Sự khác biệt đối với mỗi SDK và phiên bản phát triển: khi hai SDK đối với cùng một bản chuyển đổi được kết hợp không giống nhau, chiến lược phát hành nên viết ra hành vi nào có thể chấp nhận được, chứ không phải là các kết quả tốt nhất sau đó.

SDK thường biến các đối tượng dây thành các loại ngôn ngữ thuận tiện. Điều đó hữu ích, nhưng một đối tượng bình thường không thể chứng minh được những gì đã nhận được.

> SDK thường chuyển các đối tượng trên đường thành các loại ngôn ngữ thuận tiện.

Đối với mỗi thiết bị có nguy cơ cao, bắt:

1. Tình trạng nguyên liệu, tiêu đề và cơ quan phản ứng trước khi giải mã SDK.
2. Giá trị trở lại hoặc ngoại lệ được chuẩn hóa theo SDK.
3. Dự đoán ngữ nghĩa dự kiến cho thời đại được chọn.
4. Các trường được nâng lên, tổng hợp, loại bỏ hoặc thay đổi bởi SDK.

Mô hình cho phép loại bỏ các sổ kế toán điện tử được biết đến chỉ với SDK như `resultType`- `_meta`- `ttlMs`, và`cacheScope`khi so sánh tải trọng ứng dụng. Nó báo cáo một giảm `futureHint`bởi vì lĩnh vực ngữ nghĩa không rõ đó đã biến mất.

Đừng cho rằng mọi sự khác biệt là một lỗi SDK. Điểm là để làm cho sự chuyển đổi hiển thị. quyết định liệu thành phần của bạn là một điểm cuối ứng dụng, có thể bỏ qua một trường phụ gia, hoặc một trung gian minh bạch, nên bảo tồn nó.

> Đừng giả sử mỗi điểm khác biệt là lỗi SDK. Ý nghĩa của điểm khác biệt là để chuyển đổi có thể nhìn thấy. Hãy nghĩ rõ rằng bộ phận của bạn là "có thể bỏ qua các điểm ứng dụng của phần tử tăng trưởng", hoặc "có thể giữ cho người trung gian rõ ràng của nó".

Động cơ khác biệt đối với mỗi SDK và phiên bản bạn gửi. Nếu hai SDK bình thường hóa bản sao tương tự khác nhau, chính sách phát hành nên nói hành vi nào là chấp nhận được thay vì chọn đầu ra thuận tiện nhất sau sự kiện.

> Đối với mỗi SDK bạn phát hành với phiên bản hoạt động khác nhau. Nếu hai SDK không giống nhau về việc kết hợp cùng một bản chuyển đổi, chiến lược phát hành nên viết ra những hành vi chấp nhận được, chứ không phải là các kết quả tốt nhất sau đó.

## Chụp bằng chứng đại diện.

Hầu hết các lỗi MCP sản xuất xảy ra trong nhiều quá trình hơn một.

> 大多数生产 MCP 故障跨越不止一个进程――记录三个视角:

| View | Minimum evidence |
|---|---|
| Ingress | request headers, JSON-RPC body, content type, authenticated route, receive time |
| Origin | forwarded headers and body digest, origin status, response headers and body |
| Egress | client-visible status, headers, body, and send time |

> 三个视角表: nhập khẩu(Ingress) ít nhất记记请求头部、JSON-RPC 主体、内容类型、已认证路由与接收时间;源站(Origin) ít nhất记转发头部与主体摘要、源站状态码、响应头部与主体;出口(Egress) ít nhất记客户端可见的状态码、头部、主体与发送时间──

Mô hình phát hiện ra hai biến đổi phổ biến:

> Example检测两类常见变换:

- lỗi HTTP 400 hoặc 404 JSON-RPC trở thành một proxy chung 500
- Cơ thể JSON-RPC xuất phát khác với cơ thể nguồn gốc

> 两类变换: HTTP 400 của cổng nguồn hoặc 404 JSON-RPC 错误变成代理的通用 500; xuất JSON-RPC 主体与源站主体不一致.

Thêm các tuyên bố cụ thể về triển khai cho loại nội dung, `Accept`, nén, yêu cầu-scaned SSE, cache tiêu đề, và liên quan theo dõi.

> Một lần nữa cho các loại nội dung`Accept`、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、   、 、    、 、                、                                                                                                                                    

## Tải lại trước khi bằng chứng rời khỏi trí nhớ

> **【中文解读】**脱敏 là một phần của sự thống nhất vận tải, không phải là việc làm sạch sau khi xảy ra.  在序列化、哈希、日志、测试工件或失败上传之前完成.`Authorization``Cookie``accessToken``clientSecret``token``password``secret``api_key`等键下值;规范化与 denylist 必须使用相同的形态,防止 camelCase、连字符、下划线、点号变体相互绕过──生产采集器还应加方法 特定参数策略像`query`Các khóa vô hại này cũng có thể được trang bị dữ liệu cá nhân hoặc được giám sát.

Việc viết lại là một phần của các hoạt động tuân thủ, không phải là một công việc dọn dẹp sau đó.

> 脱敏 là một phần của sự thống nhất, không phải là một phần của việc làm sạch sau đó.

Vỏ mẫu gấp các tên khóa và loại bỏ các bộ tách trước khi phù hợp, sau đó thay thế lại các giá trị dưới các khóa như `Authorization`- `Cookie`- `Set-Cookie`- `X-Api-Key`- `accessToken`- `clientSecret`- `registrationAccessToken`- `token`- `password`- `secret`, và`api_key`. Canonicalization và denylist phải sử dụng cùng một hình thức để camelCase, các biến thể có dấu chấm, nhấn mạnh và chấm không thể bỏ qua chính sách của nhau.`query`có thể vẫn chứa dữ liệu cá nhân hoặc được quy định.

> Example trước tiên đưa tên khóa làm big小写折叠并移除分隔符再匹配, sau đó chuyển tiếp thay thế `Authorization``Cookie``Set-Cookie``X-Api-Key``accessToken``clientSecret``registrationAccessToken``token``password``secret``api_key`等键下值──规范化与 denylist 必须使用相同的形态,这样 camelCase、连字符、下划线和点号变体就无法绕过彼此的策略──生产采集器也应增加方法的特定参数策略,因为像`query`Các khóa không gây hại này vẫn có thể mang theo dữ liệu cá nhân hoặc được giám sát.

Hài lưu các dữ liệu thu được trong một hệ thống lâu dài được phê duyệt chỉ khi một cuộc điều tra cụ thể yêu cầu chúng. Một bản ghi chứng minh các dữ liệu thu được đã thúc đẩy quyết định; nó không tiết lộ giá trị bị xóa.

> Chỉ khi một cuộc điều tra cụ thể thực sự cần thiết, thì bắt đầu được giữ trong hệ thống vòng đời ngắn được phê duyệt.

## Hãy làm cho sức khỏe và sự quay trở lại là một phần của cánh cổng.

> **【中文解读】**协议 phù hợp là điều kiện cần thiết để phát hành, không đủ điều kiện Một phiên bản ứng cử viên hoàn toàn phù hợp vẫn có thể vượt quá thời gian; rò rỉ trong bộ nhớ hoặc áp lực phụ thuộc. 发布 trước tiên xác định cửa sổ sức khỏe (((mức mẫu tối thiểu; tỷ lệ sai lầm tối đa; độ trễ phân vùng tối đa;  và hoặc giới hạn tài nguyên; 观察 thời gian dài; so sánh với đường cơ sở đã được chuẩn bị); tương tự như trong việc phát hành trước tiên xác định chứng cứ quay lại (Rollback)  Bản gốc xác định trước tiên; Ước truy cập (Rollback)  Bản tóm tắt  SHA-256  sản phẩm và mô tả pin  Registry  trạng thái  Kết quả sức khỏe hiện tại; 路由恢复程序  một phần xác nhận trên)                                                                                                                                                               `healthy: "yes"`、 bất kỳ mã chứng minh nào): ví dụ yêu cầu xác định loại 、 hoạt động  trạng thái 、 ba SHA-256 摘要 、可信签署 viên và có hiệu lực HMAC-SHA-256 认证 đối với toàn bộ tải toàn bộ; dùng để chứng minh mật khẩu xác định không phải là một bộ phận bí mật, sản xuất cần phải phát hành bên biên giới nhập vào khóa được bảo vệ 、 KMS kết quả xác minh hoặc chứng minh công khai ⋅ phát hành cũng từ chối chuyển nhượng không gian  SDK phân chia hoặc chứng minh đại diện  Mỗi nguồn phải mang theo một bản tóm tắt chứng minh có hiệu lực, cửa sổ sức khỏe xanh không lấp đầy bên biên giới chưa từng được quan sát.

Sự tuân thủ giao thức là cần thiết nhưng không đủ để giải phóng. Một ứng cử viên phù hợp vẫn có thể thời gian ra, rò rỉ bộ nhớ hoặc quá tải một sự phụ thuộc.

> 协议一致 là điều kiện cần thiết để phát hành chứ không phải điều kiện đầy đủ. Một phiên bản ứng cử viên nhất quán vẫn có thể vượt quá thời gian, rò rỉ trong bộ nhớ hoặc áp lực một số phụ thuộc.

Định nghĩa một cửa sổ sức khỏe trước khi triển khai:

> 发布之前先定义健康窗口:

- Số lượng mẫu tối thiểu
- Tỷ lệ lỗi tối đa
- Percentile độ trễ tối đa
- giới hạn bão hòa hoặc nguồn lực
- Thời gian quan sát
- so sánh với đường cơ sở được chấp nhận

Định nghĩa bằng chứng quay lại trước khi triển khai:

> 发布之前同样定义回滚证据:

- phiên bản trước đó chính xác
- Đánh giá bằng chứng nhập học
- SHA-256 đồ tạo và pin mô tả
- trạng thái Registry hiện tại
- kết quả sức khỏe hiện tại
- Quy trình khôi phục tuyến đường
- chứng nhận về các trường chính xác đó từ một nhân danh kiểm soát viên giải phóng đáng tin cậy

yêu cầu mục tiêu quay trở lại đó được xác minh và khỏe mạnh trước khi thăng chức, không chỉ sau khi ứng viên thất bại.

> 要求回滚目标在晋升之前就完成验证并且健康,而不是只是等候选人失败后才查查. Một lần không có đường dẫn phục hồi khả thi thành công xuất bản không phải là sản xuất sẵn sàng.

Nếu một ứng cử viên thất bại và mục tiêu quay lại không có bằng chứng đó, giữ lưu lượng thay vì đoán.

> Nếu ứng cử viên thất bại và quay lại mục tiêu thiếu chứng cứ, thì hãy ổn định lưu lượng, đừng để đoán.

Không giảm độ sẵn sàng để kiểm tra sự thật như phiên bản không trống, `healthy: "yes"`, hoặc một chuỗi bằng chứng tùy tiện. Mô hình đòi hỏi các loại chính xác, trạng thái hoạt động, ba bản ghi SHA-256, một người ký đáng tin cậy và chứng chỉ HMAC-SHA-256 hợp lệ trên toàn bộ tải trọng phục hồi. Chìa khóa demo xác định của nó là một vật cố định không bí mật. Nhúng một khóa bảo vệ, kết quả xác minh KMS hoặc xác minh chứng minh chứng minh khóa công khai tại giới hạn phát hành trong sản xuất.

> Đừng đưa ra quá trình kiểm tra trở thành giá trị thực ư như phiên bản không trống số ư`healthy: "yes"`hoặc bất kỳ chuỗi chứng cứ nào. Ví dụ yêu cầu xác định loại hình, trạng thái hoạt động, 3 SHA-256 摘要, người ký có thể tin cậy, cũng như chứng nhận HMAC-SHA-256 hợp lệ của tải toàn bộ.

Cổng phát hành cũng từ chối bản sao không có gì, SDK khác biệt hoặc bằng chứng đại diện. Mỗi nguồn phải mang theo các chứng cứ có giá trị. Một cửa sổ sức khỏe xanh không thể lấp đầy ranh giới chưa bao giờ được quan sát.

> 门也拒绝空的转录、SDK 差分或代理证据: Mỗi nguồn phải mang theo một bản tóm tắt chứng cứ hợp lệ── một cửa sổ sức khỏe xanh, không lấp đầy một ranh giới chưa bao giờ được quan sát──

## Hãy xây dựng nó.

Đưa dây thắt thư viện tiêu chuẩn:

> 运行标准库测试架:

```bash
cd phases/13-tools-and-protocols/31-mcp-conformance-versioning-and-operations
python3 code/main.py
```

Demo chạy chính xác mười lăm bản sao vàng và âm tính, bao gồm kết quả hoàn thành hợp lệ và sai, so sánh kết quả thô với một dạng xem SDK, kiểm tra một proxy đã bị lỗi nguồn gốc sụp đổ, đánh giá sức khỏe, xác minh bằng chứng quay lại, và chọn mục tiêu đó.

> demo 恰好运行十五条黄金与负面转录(含合法与形的完成结果), so sánh kết quả ban đầu với SDK 视图, kiểm tra một đại lý đã tiêu diệt các lỗi của nhà máy nguồn, đánh giá sức khỏe, xác nhận chứng cứ quay lại, và chọn trong mục tiêu này。

Hình dạng dự kiến:

> 预期输出形状:

```json
{
  "transcriptsPassed": 15,
  "transcriptsTotal": 15,
  "sdkDroppedFields": ["futureHint"],
  "proxyIssues": [
    "proxy collapsed a protocol error into HTTP 500",
    "proxy changed the origin JSON-RPC body"
  ],
  "releaseAction": "rollback",
  "evidenceDigest": "..."
}
```

Đọc `code/main.py`theo thứ tự này:

> 按以下顺序阅读 `code/main.py`- Có thể là:

1. `validate_request()`thực thi các quy tắc yêu cầu và tiêu đề cụ thể cho thời đại.
2. `validate_result()`phân biệt những người phân biệt đối xử thừa kế bị mất tích, giá trị hiện đại hợp lệ, mở rộng và giá trị không rõ.
3. `select_era()`thực hiện chính sách phản hồi nghiêm ngặt và hạn chế.
4. `run_transcript()`đánh giá các đèn vàng và âm.
5. `compare_sdk_view()`cho thấy sự khác biệt về bình thường hóa.
6. `inspect_proxy()`so sánh bằng chứng nhập cảnh, nguồn gốc và xuất cảnh.
7. `redact()`loại bỏ những bí mật rõ ràng trước khi làm việc với bằng chứng.
8. `rollback_evidence_ready()`xác nhận các trường pin chính xác và chứng nhận phát hành đáng tin cậy.
9. `ReleaseGate.evaluate()`kết hợp với chứng minh không rỗng, SDK, đại diện, sức khỏe và rolloback.

## Hãy sử dụng nó để thực hiện

Đưa dây vào bốn điểm:

> Trong 4 thời điểm vận hành:

1. Trong mỗi thay đổi thực hiện với một bộ điều chỉnh thử nghiệm trong quá trình.
2. Đối với các máy chủ và khách hàng được xây dựng trên các giao thông thực.
3. Thông qua proxy hoặc gateway được triển khai trong môi trường sắp xếp.
4. Trong khi triển khai cá thể có sức khỏe sống và bằng chứng quay lại.

Giữ tên trường hợp ổn định trên các lớp. `negative-header-body-mismatch`nên có nghĩa là không thay đổi trong báo cáo đơn vị, kết thúc đến kết thúc, đại diện và canary.

> Trong các tầng giữ được tên sử dụng ổn định tương tự:`negative-header-body-mismatch`Trong đơn vị, kết thúc, đại diện và báo cáo của Kim Cơn phải chỉ cùng một không thay đổi.

Cung cấp các bản ghi trong hệ thống phát hành của bạn. Cung cấp các bản ghi nguyên liệu ngắn hạn chỉ trong các điều khiển truy cập sự cố.

> Fixure schema 存进版本控制;脱敏后的运行证据存进发布系统; ngắn đời vòng bắt đầu chỉ được đặt dưới sự truy cập kiểm soát sự kiện.

> Bốn điểm vận hành đối với các biên giới bốn tầng: trong quá trình thực hiện thay đổi, chuyển giao thực sự, các sản phẩm được chuyển giao thực sự, các đại lý hoặc mạng lưới trong giai đoạn, với các chứng cứ về sức khỏe thực sự và các chứng cứ quay lại.

## - Bác sĩ, tôi đã làm việc trong phòng thí nghiệm tương tác.

### Phòng thí nghiệm A: chứng minh ranh giới thời đại

Từ `code`thư mục, mở Python:

> Từ `code`Giờ mở Python:

```bash
cd phases/13-tools-and-protocols/31-mcp-conformance-versioning-and-operations/code
python3 -q
```

Đi chạy:

```python
from main import *
validate_result({"tools": []}, "legacy")
validate_result({"tools": []}, "modern")
```

Lệnh truyền thống kết thúc`complete`- Cuộc gọi hiện đại đang phát sinh.`ProtocolViolation`Giờ thử nghiệm trở lại:

> 旧版调用推断出 `complete`;现代调用抛出 `ProtocolViolation` 接着测回退:

```python
select_era({"kind": "timeout"}, "fallback")
select_era(
    {"kind": "timeout"},
    "fallback",
    legacy_allowed=True,
    legacy_evidence={"kind": "initialize_success", "protocolVersion": LEGACY_VERSION},
)
select_era({"kind": "jsonrpc_error", "code": -32021}, "fallback")
```

Thời gian tạm thời đầu tiên không được đóng bởi vì sự im lặng không phải là bằng chứng di sản. Cuộc gọi thứ hai chỉ chọn di sản vì cấu hình cho phép nó và kết quả khởi tạo di sản hợp lệ đã được quan sát. Hầm lỗi khả năng thiếu được công nhận chứng minh là chi nhánh hiện đại.

> Thứ nhất là quá thời gian thất bại đóng cửa (fail closed), vì im lặng không phải là chứng cứ bản cũ. Thứ hai là vì có thể chọn bản cũ, chỉ vì việc định vị cho phép và quan sát được kết quả khởi tạo cũ có hiệu quả.

### Phòng thí nghiệm B: trường cộng với phân biệt đối xử  B: tăng số lượng 字段 và phân định

```python
validate_result({"resultType": "complete", "tools": [], "futureHint": True}, "modern")
validate_result({"resultType": "future_mode", "tools": []}, "modern")
```

Kết quả đầu tiên là giữ gìn `futureHint`. thứ hai bị từ chối vì người phân biệt sinh học không biết.

> Kết quả đầu tiên được giữ lại.`futureHint`; thứ hai bị từ chối, vì các thiết bị phân định chu kỳ đời là không biết.

### Phòng thí nghiệm C: kiểm tra chuyển đổi SDK   thí nghiệm C: kiểm tra chuyển đổi SDK

```python
compare_sdk_view(
    {"resultType": "complete", "tools": [], "futureHint": {"mode": "new"}},
    {"tools": []},
)
```

Quyết định liệu thành phần của bạn có thể bỏ qua hay không `futureHint`hoặc phải chuyển nó. ghi lựa chọn đó vào chính sách phát hành. Đừng im lặng xóa phân biệt.

> Chọn thành phần của bạn có thể bỏ qua`futureHint`, hay phải chuyển phát nó. Hãy viết lựa chọn này vào chiến lược phát hành, đừng  xóa bỏ kết quả khác biệt.

### Phòng thí nghiệm D: sửa chữa nhân viên đại diện

Thay đổi đổi đổi demo để thoát lưu giữ trạng thái nguồn gốc và thân xác.`python3 main.py`Các vấn đề đại diện nên biến mất, nhưng SDK khác biệt vẫn chặn quảng cáo.`futureHint`trong dạng xem SDK và quan sát sự thay đổi hành động đến `promote`Khi mọi nguồn bằng chứng đều qua.

> 修改 demo 交换,让出口保留源站状态码与主体──再跑一次 `python3 main.py`Vấn đề đại diện nên biến mất, nhưng SDK 差分 vẫn còn 住晋升──然后把`futureHint`Thêm vào SDK 视图,观察当每证据来源都通过时,动作变成 `promote`

## Phòng thí nghiệm tập luyện.

Thêm các bản sao SSE được yêu cầu vào vòng xoáy.

> 给测试架增加请求级 SSE 转录。

> 进阶练将语料库扩展从"一请求一响应"到"一请求一流": nắm bắt trạng thái phản ứng,类型内容,有序 SSE 事件与流终止; chứng minh mỗi sự kiện JSON-RPC 事件 có kết quả hoặc sai lầm hợp pháp trong một tài liệu cụ thể;加"代理将整个流缓冲完再转发"和"SSE 事件的 JSON-RPC id和请求符不"两个负面使用例;写证据前先脱敏事件数据;将流时长长,事件首延和事件计数纳入健康窗口; chỉ khi流失败发布门选有证据的回滚目标.

Yêu cầu:

- Tận thức trạng thái phản ứng, loại nội dung, các sự kiện SSE được sắp xếp và chấm dứt dòng.
- Hiển thị mỗi sự kiện JSON-RPC có kết quả hoặc lỗi cụ thể thời đại hợp lệ.
- Thêm trường hợp âm cho một proxy mà bơm toàn bộ dòng trước khi chuyển tiếp.
- Thêm trường hợp âm cho một sự kiện SSE có ID JSON-RPC khác với yêu cầu.
- Tạo lại dữ liệu sự kiện trước khi viết bằng chứng.
- Bao gồm thời gian lưu lượng, thời gian trễ của sự kiện đầu tiên và số sự kiện trong cửa sổ sức khỏe.
- Hãy để cửa thoát chọn chỉ một mục tiêu quay trở lại bằng chứng khi dòng chảy thất bại.

Thành công có nghĩa là cùng một trường hợp chạy trực tiếp và thông qua ủy quyền, với một báo cáo xác định ranh giới chính xác mà thay đổi hành vi.

> Các tiêu chuẩn thành công: cùng một trường hợp sử dụng既能直连运行也能穿代理运行, báo cáo能指出改变行为的精确边界――

## Thuật vật được vận chuyển.

Bài học này sẽ đi theo `outputs/skill-mcp-conformance-release-gate.md`Sử dụng nó để biến đổi máy chủ, khách hàng, cổng thông tin hoặc SDK thành một matrix phù hợp phiên bản và quyết định phát hành.

> 本课附带 `outputs/skill-mcp-conformance-release-gate.md` Sử dụng nó để thay đổi một lần máy chủ, khách hàng, cổng kết nối hoặc SDK, trở thành một mô hình thống nhất và đưa ra quyết định.

## Hãy kiểm tra.

> **【中文解读】**验收清单逐条过: tất cả vàng và chuyển âm chuyển tất cả đến kết thúc dự kiến; 现代请求要求精确的命名空间元数据键; HTTP 头部名大小写不敏感地匹配、编码的`Mcp-Name`值被精确解码;头部与主体不匹配回归现代不匹配码;响应版本、ID、结果/错误 互斥、错形态与HTTP 映射都被校验;方法特定工具列表/任务/完成 载荷要求被执行;每个观察到的`HeaderMismatch`都要求真实的 HTTP 400 JSON-RPC `-32020`响应; 原始 `Mcp-Name`Không trắng bị từ chối và lính đánh bộ                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     `resultType`Chỉ trong một thời gian cũ được chọn hợp pháp; tăng số字段 sống và không biết kết quả loại thất bại; mở rộng kết quả loại yêu cầu khả năng của nó đã được tuyên bố; được nhận dạng hiện đại lỗi không bao giờ chạm vào phiên bản cũ trở lại; thông báo không tạo ra JSON-RPC  phản ứng; SDK sổ sách di chuyển và ngữ nghĩa字段 bị mất được phân biệt; đại lý lỗi 缩 được kiểm tra  chứng chỉ được chuyển nhượng trong camelCase và phân vùng biến thể; được nâng cấp yêu cầu không trống chuyển nhượng  SDK  đại lý và chứng chỉ vận tải sức khỏe; đã nâng cấp và quay cũng yêu cầu một xác nhận  pin                                                                                                                                                                                 

Tiến hành bộ demo và xác định:

> 运行 demo 与确定性测试套件:

```bash
cd phases/13-tools-and-protocols/31-mcp-conformance-versioning-and-operations
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

Việc kiểm tra phải chứng minh:

- Mỗi bản ghi âm vàng và âm được đưa vào đều đạt được kết quả mong đợi.
- Các yêu cầu hiện đại yêu cầu các khóa metadata chính xác với tên
- Tên tiêu đề HTTP được kết hợp không nhạy cảm và mã hóa `Mcp-Name`các giá trị được giải mã chính xác
- tiêu đề và cơ thể không phù hợp trả lại mã không phù hợp hiện đại
- phiên bản phản ứng, ID, kết quả hoặc lỗi độc quyền, hình dạng lỗi và bản đồ HTTP được xác nhận
- Các yêu cầu về danh sách công cụ, nhiệm vụ và tải trọng hữu ích hoàn thành cụ thể về phương pháp được thực thi
- mỗi lần quan sát`HeaderMismatch`yêu cầu một HTTP 400 JSON-RPC thực tế `-32020`phản ứng
- thô`Mcp-Name`không gian trắng bị từ chối trong khi thực tế được mã hóa bởi sentinel không gian trắng đi lại và đi lại
- một người mất tích`resultType`chỉ có hiệu lực trong thời kỳ thừa kế được chọn
- Các trường phụ gia tồn tại trong quá trình xác thực nguyên liệu trong khi các loại kết quả không rõ ràng thất bại
- Các loại kết quả mở rộng yêu cầu khả năng quảng cáo của chúng
- lỗi hiện đại được nhận ra không bao giờ gây ra sự thất bại của di sản
- Các thông báo không tạo ra phản ứng JSON-RPC
- Việc xóa sổ SDK và mất trường ngữ nghĩa được phân biệt
- lỗi proxy bị phát hiện và các thông tin tín dụng được chỉnh sửa trở lại trên camelCase và biến thể phân tách
- Việc quảng bá đòi hỏi không có bản sao trống, SDK, đại diện và bằng chứng hoạt động lành mạnh
- Tăng cường và quay trở lại đều yêu cầu một mục tiêu quay trở lại xác thực, gắn kết, hoạt động và lành mạnh

## Các chế độ sản xuất thất bại

> 下表三列:失败、弱测试会报告什么、测试架必须证明什么──最贵的三行:SDK 合成了缺失的判辨器("工具/列表 通过了",实际上原始现代结果缺缺`resultType`、 bất hợp pháp); đại lý cấp quyền cho một công cụ và nguồn để thực hiện một công cụ khác`Mcp-Name`必须在每跳都等于主体路由名; 丝雀零样本却显示健康 (丝雀零样本却显示健康)

| Failure | What the weak test reports | What the harness must prove |
|---|---|---|
| SDK synthesizes a missing discriminator | “tools/list passed” | Raw modern result lacked `resultType` and is invalid |
| Client downgrades after `-32021` | “legacy retry worked” | Recognized modern error forbids fallback |
| Unknown result type treated as complete | “response parsed” | Unadvertised lifecycle discriminator is rejected |
| Proxy authorizes one tool and origin executes another | “request reached server” | `Mcp-Name` equals the body routing name at every hop |
| Harness throws before reading the server response | “header mismatch test passed” | HTTP 400 and JSON-RPC `-32020` response are captured and validated |
| Proxy turns origin 400 into generic 500 | “upstream error” | Origin and egress statuses and JSON-RPC bodies are preserved |
| Notification middleware emits `{result: null}` | “handler returned none” | Final egress body is empty and no JSON-RPC response exists |
| SDK strips an additive field | “typed objects match” | Raw and normalized views show the exact dropped field |
| Failure artifact leaks a bearer token | “debug bundle uploaded” | Redaction occurred before hashing, logging, or upload |
| Credential key style bypasses redaction | “denylist contains api_key” | CamelCase and separator variants share one canonical denylist form |
| Canary has no samples but appears healthy | “zero errors” | Minimum sample count is enforced |
| Rollback selects an unknown build | “previous deployment restored” | Target version, admission digest, pins, status, and health are present |

## Quy tắc hoạt động

Kiểm tra các byte bạn gửi, các byte mỗi trung gian chuyển tiếp, ngữ nghĩa mỗi SDK phơi bày, và các hoạt động bằng chứng sẽ sử dụng dưới áp lực. Sự tương thích là một nhánh rõ ràng. Rollback là một hành động phát hành được hỗ trợ bằng chứng. Cả hai không nên là một tác dụng phụ ngẫu nhiên của một trình phân tích cho phép.

> 测试你发射字节、每个中间设备转发字节、每个 SDK 暴露的语义,以及运维在压力下所需的证据――兼容是一个明显分支;回滚是一个有证据支的发布动作――两者都不应该是宽松解析器意外产生的副作用――

> Một câu nói tổng kết toàn lớp: sự đồng nhất không phải là "đã chạy qua một lần", mà là" mỗi biên giới có bằng chứng có thể quan sát được"",được tái hiện được"",đặc giải dễ dàng sẽ biến"兼容" và"回滚" thành những tác dụng phụ bất ngờ; rõ ràng phân支加证化决策,才把它们变成回受控的工程行为――

## Xem thêm 延伸阅读

- [MCP 2026-07-28 base protocol](https://modelcontextprotocol.io/specification/2026-07-28/basic)
- [MCP version negotiation](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning)
- [MCP Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [Official MCP conformance project](https://github.com/modelcontextprotocol/conformance)
