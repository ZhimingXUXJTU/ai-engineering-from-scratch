# MCP Model Input: Sampling Migration and Stateless MRTR  MCP 模型输入: Sampling 迁移与无状态 MRTR

> MCP 2026-07-28 đã loại bỏ Sampling cho các thiết kế mới và loại bỏ kênh yêu cầu máy chủ sang khách hàng. Nếu một workflow hiện có vẫn cần mô hình của khách hàng, máy chủ sẽ trả lại một `input_required`kết quả và khách hàng thử lại yêu cầu ban đầu với đầu ra mô hình. vòng hợp lý trở nên rõ ràng, giới hạn và không có quốc gia ở lớp giao thức.

> **【中文解读】**MCP 2026-07-28 để thiết kế mới từ bỏ Sampling (采样),并移除" server to client request" (tạm dịch: "tạm dịch: máy chủ gửi yêu cầu khách hàng")`input_required`Kết quả, khách hàng có mô hình xuất bản thử nghiệm lại yêu cầu ban đầu. Chuyển chuyển các quy trình đã trở nên rõ ràng.

> **【拓展：Sampling→MRTR 的方向反转】**旧版样本是协议里唯一的"反向通道": máy chủ trong xử lý yêu cầu ngược lại调用客户端的 LLM đây chính là lý do nó được di chuyển, ngược lại通道让服务器逻辑依赖连接存活、难以无状态部署――MRTR 把"反向调用"改写成"结果 + 重试": máy chủ将要做的事装进`inputRequests`Trở lại, khách hàng nhận được mô hình sau khi xuất khẩu sử dụng ID mới 重新发起相同方法──方向反转与课09的传输层无状态化、课10的`subscriptions/listen`Đó là cùng một cấu trúc.

>  **【前置】**学本节前请先掌握:(1) Bước 13·07(MCP server) 工具/call 的分发与校验;(2) Bước 13·10(资源 và lời nhắc) `_meta`Bảo quản chìa khóa`server/discover``resultType`判别符;(3) HMAC / 认证加密的基本概念`requestState`                                                                                                                                                                                                                                                              `sampling/createMessage`Xin vui lòng, xin hãy chuyển cái "đối với yêu cầu" này thành " kết quả + 重试"

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 10 (resources and prompts) | **前置知识:** Phase 13 · 07（MCP 服务器）、Phase 13 · 10（资源与提示）
**Time:** ~75 minutes | **时间:** 约 75 分钟

## Mục tiêu học tập

- Giải thích lý do tại sao Sampling bị lỗi thời trong MCP 2026-07-28 và chọn mặc định tích hợp mô hình trực tiếp cho các máy chủ mới.
  Trung ngữ翻译:解释 样本化在 MCP 2026-07-28 bị từ bỏ,并为新服务器选择直连模型集成的默认路径──
- Thực hiện một dòng công việc tương thích mang theo `sampling/createMessage`thông qua Các yêu cầu nhiều chuyến đi vòng (MRTR).
  Trung文翻译:实现通过多轮往返请求(MRTR)承载 `sampling/createMessage`                                                                                                                                                                                                                                                              
- Đặt sửa đổi giao thức và khả năng của khách hàng trong mỗi yêu cầu `_meta`đối tượng.
  Trung ngữ翻译:把协议修订版和客户端能力放进每个请求的`_meta`Đối tượng:
- Trở lại`resultType: "input_required"`và thử lại phương pháp ban đầu với một ID JSON-RPC mới.
  Trung ngữ翻译:返回 `resultType: "input_required"`,并使用全新的 JSON-RPC id 重试原始方法──
- Bảo vệ sự toàn vẹn `requestState`và buộc nó với nguyên tắc, phương pháp, lý luận và hết hạn.
  Trung ngữ翻译:对 `requestState`Làm bảo vệ tính toàn diện, và buộc nó vào chủ thể, phương pháp, tham số và thời gian qua hạn.
- Các vòng được hỗ trợ bởi mô hình bị ràng buộc với kiểm tra khả năng, phê duyệt, xác nhận phản ứng và giới hạn tròn.
  Trung文翻译: dùng khả năng kiểm tra, phê duyệt, đáp ứng và vòng lên giới hạn cho mô hình hỗ trợ vòng đặt giới hạn.

## Quyết định trước giao thức

> **【中文解读】**Trước khi làm quyết định xây dựng, tái đàm phán thỏa thuận.`summarize_repo`Các công cụ này bao gồm hai loại công việc: xác định công việc: các tài liệu, đọc cho phép các tài liệu, đường thử nghiệm, nội dung của việc lắp đặt) và mô hình công việc: các tài liệu đại diện, tổng quát)`tools/call`Kết quả: 2) 存量 Sampling 工作流迁移到MRTR 兼容路径, chỉ khi "mô hình và chứng chỉ sử dụng khách hàng" là nhu cầu sản phẩm thực sự mới chọn nó, và cần ghi lại kế hoạch di chuyển.

Một công cụ như `summarize_repo`cần hai loại công việc:

1. Công việc xác định: liệt kê các tập tin, đọc các tập tin được phép, xác nhận con đường và lắp ráp nội dung.
  Trung文翻译:确定性工作:列出文件、读取允许的文件、校验路径、拼装内容──
2. Công việc mô hình: chọn các tệp đại diện và tổng hợp bản tóm tắt.
  Trung ngữ翻译:模型工作:选择代表性文件并综合出摘要。

Bây giờ bạn có hai kiến trúc hợp lệ.

> Giờ đây, có hai cấu trúc hợp pháp.

### Server mới: tích hợp trực tiếp với nhà cung cấp mô hình

Đây là mặc định hiện tại. máy chủ sở hữu lựa chọn mô hình, tín chỉ, ngân sách, thử nghiệm lại, và khả năng quan sát. Nó trả lại một bình thường `tools/call`kết quả cho khách hàng MCP.

> Đây là mặc định hiện tại. Dịch vụ tự quản mô hình chọn lựa, chứng chỉ, ngân sách, thử nghiệm lại và có thể quan sát được. Nó trở lại một thứ bình thường đối với khách hàng MCP.`tools/call`Kết quả.

Chọn điều này khi máy chủ đã là một dịch vụ được lưu trữ hoặc khi hành vi mô hình dự đoán quan trọng hơn là sử dụng mô hình của máy chủ.

> Khi máy chủ đã là dịch vụ quản lý, hoặc khi mô hình hành vi có thể dự đoán là quan trọng hơn so với mô hình của chủ nhà, chọn đường này.

### Giai đoạn làm việc lấy mẫu hiện có: di chuyển nó sang MRTR

Các mẫu vẫn tồn tại trong cửa sổ khấu trừ của nó. Một máy chủ nhắm mục tiêu 2026-07-28 không thể gửi một trực tiếp `sampling/createMessage`yêu cầu trở lại với khách hàng. thay vào đó nó nhúng yêu cầu đó trong một`InputRequiredResult`- Tôi không biết.

> Tiêu chuẩn trong thời gian sử dụng cửa sổ vẫn còn tồn tại.`sampling/createMessage`Xin hãy thay đổi nó để đặt yêu cầu vào một.`InputRequiredResult`

Chọn con đường tương thích này chỉ khi sử dụng mô hình của khách hàng và thông tin tín dụng là yêu cầu sản phẩm thực sự.

> Chỉ khi "mô hình và chứng chỉ sử dụng khách hàng" là nhu cầu sản phẩm thực tế mới chọn con đường này.

## Hợp đồng vô quốc tịch.

> **【中文解读】**2026 năm tháng 7 của thỏa thuận không có `initialize`交换、没有 `notifications/initialized`Không có gì`Mcp-Session-Id` nguyên thủy sống trong tay thông tin hiện đang được chuyển giao với mỗi yêu cầu. 服务器在每个请求上校验修订版:版本缺失或非字符串 → `-32602`;不支持的字符串 → `-32022`(带精确 hỗ trợ/ yêu cầu 数据); thiếu Sampling 能力 → `-32021`(带 `data.requiredCapabilities`(■无 `id`封封是通知: có thể xử lý nhưng không phát triển thành công hoặc phản ứng sai,                                                                                                                                                                                                                                                     `202`                                                                                                                                                                                                                                                              `complete`( hoàn thành)`input_required`(客户端须履行嵌入请求并重试),扩展可定义更多(Tác vụ 扩展在课13加 `"task"`(■)

Nghị định thư tháng 7 năm 2026 không có`initialize`trao đổi, không `notifications/initialized`, và không `Mcp-Session-Id`Mỗi yêu cầu đều chứa thông tin từng được trao cho người:

> 2026 năm tháng 7 của thỏa thuận không có `initialize`交换、没有 `notifications/initialized`、 cũng không có `Mcp-Session-Id`Mỗi yêu cầu đều mang theo thông tin của người gốc sống trong tay:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "summarize_repo",
    "arguments": {"audience": "developer"},
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {"sampling": {}},
      "io.modelcontextprotocol/clientInfo": {
        "name": "lesson-client",
        "version": "1.0.0"
      }
    }
  }
}
```

Các máy chủ xác nhận sửa đổi trên mỗi yêu cầu. Một phiên bản bị thiếu hoặc không có chuỗi là các param không hợp lệ, `-32602`Một chuỗi không được hỗ trợ sẽ quay lại`-32022`với dữ liệu chính xác `{"supported":["2026-07-28"],"requested":"<client version>"}`- Một khả năng lấy mẫu bị mất tích trở lại .`-32021`với `data.requiredCapabilities`được thiết lập`{"sampling":{}}`- Tôi không biết.

>  máy chủ trên mỗi yêu cầu trên các phiên bản sửa đổi.`-32602`▽不支持的字符串返回 `-32022`Không có dữ liệu chính xác`{"supported":["2026-07-28"],"requested":"<client version>"}` thiếu hụt  năng lực quay lại `-32021`- Tôi không biết.`data.requiredCapabilities`设为 `{"sampling":{}}`

Một phong bì mà không có JSON-RPC `id`là một thông báo. Người nhận có thể xử lý nó, nhưng nó không phát ra phản ứng thành công hoặc phản ứng lỗi. Một bộ điều chỉnh HTTP Streamable trả về `202 Accepted`Không có cơ quan nào cho thông báo được chấp nhận.

> Không có JSON-RPC `id`                                                                                                                                                                                                                                                              `202 Accepted`

Các máy chủ cũng thực hiện `server/discover`với chính xác `supportedVersions`- Chìa khóa, khả năng,`ttlMs`, và`cacheScope`để khách hàng có thể tìm hiểu và lưu trữ hợp đồng máy chủ trước khi gọi một công cụ. Bởi vì phát hiện quảng cáo`tools`, máy chủ cũng thực hiện bắt buộc `tools/list`- Định nghĩa của nó`summarize_repo`mô tả bao gồm một đối tượng hợp lệ `inputSchema`- `resultType: "complete"`, dữ liệu siêu dạng máy chủ, và gợi ý cache công cộng.

> 服务器还实现 `server/discover`,带精确的`supportedVersions`键, năng lực,`ttlMs`和 `cacheScope`, để khách hàng có thể học và lưu trữ các dịch vụ giao dịch trước khi sử dụng công cụ.`tools`, máy chủ cũng phải thực hiện bắt buộc`tools/list`其确定性的`summarize_repo`描述符包含合法的对象 `inputSchema``resultType: "complete"`、 dữ liệu và lưu trữ công cộng của máy chủ

Mỗi kết quả hiện đại thành công đều có một điểm phân biệt:

- `resultType: "complete"`nghĩa là hoạt động đã kết thúc.
  Trung ngữ翻译:`resultType: "complete"`表示操作已完成.
- `resultType: "input_required"`nghĩa là khách hàng phải đáp ứng yêu cầu nhúng và thử lại.
  Trung ngữ翻译:`resultType: "input_required"`Cụ thể, khách hàng phải thực hiện yêu cầu cài đặt并重试.
- Các mở rộng có thể xác định các loại kết quả bổ sung.`"task"`Trong Bài học 13.
  Trung文翻译:扩展可以定义更多结果类型──Tác vụ 扩展在课13 中加入 `"task"`

## Một vòng MRTR

> **【中文解读】** máy chủ trong xử lý yêu cầu không thể quay lại khách hàng, vì vậy quay lại `input_required`Kết quả:`inputRequests`là máy chủ tên của bản đồ, được cài đặt trong `sampling/createMessage`Xin vui lòng;`requestState`là không minh bạch của tính toàn diện bảo vệ giá trị. Khách hàng chứng minh bản thân hỗ trợ Sampling, ứng dụng phê duyệt và mô hình chiến lược, nhận được mô hình phản ứng, sử dụng khác nhau JSON-RPC ID  gửi yêu cầu mới: tái tạo nguyên nguyên thủy phương pháp và tham số, thêm trên vòng này.`inputResponses`(按 `inputRequests`                                                                                                                                                                                                                                                              `requestState`◊ 重试不是协议会话的延续,是新的独立请求――MRTR只允许出现`tools/call``prompts/get``resources/read`Ước gì

>  **【类比】**MRTR 像政务大厅的"一次性告知单"──旧样本 像" nhân viên trực tiếp thay cho bạn打电话问上级"(服务器反向调用客户端)上级下班(连接断开) 事就办不完──MRTR 改成: nhân viên cho bạn một告知单(`inputRequests`: bạn muốn đi盖章的材料清单) 和一张回执(`requestState`: chứng minh bạn đã xếp hàng đến bước này), bạn đi để có một chương tốt hơn (của bạn), bạn có thể làm việc một lần nữa (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn) (của bạn)))

Các máy chủ không thể gọi cho khách hàng trong khi xử lý yêu cầu. Nó trả lại kết quả này thay vào đó:

> 服务器在处理请求时无法调调客户端──它改为返回这个结果:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "input_required",
    "inputRequests": {
      "pick_files": {
        "method": "sampling/createMessage",
        "params": {
          "messages": [
            {
              "role": "user",
              "content": {
                "type": "text",
                "text": "Choose three representative files and return a JSON array."
              }
            }
          ],
          "systemPrompt": "Return only the requested value.",
          "modelPreferences": {
            "costPriority": 0.8,
            "intelligencePriority": 0.2
          },
          "maxTokens": 400
        }
      }
    },
    "requestState": "opaque-integrity-protected-value"
  }
}
```

Khách hàng xác minh rằng nó hỗ trợ Sampling, áp dụng chính sách chấp thuận và mô hình của mình, và nhận được phản hồi mô hình. Sau đó nó gửi yêu cầu mới với một ID JSON-RPC khác:

> 客户端验证自己支持 样本化, áp dụng nó phê duyệt và mô hình chiến lược, và nhận được mô hình đáp ứng.

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "summarize_repo",
    "arguments": {"audience": "developer"},
    "inputResponses": {
      "pick_files": {
        "role": "assistant",
        "content": {
          "type": "text",
          "text": "[\"README.md\", \"server.py\", \"docs/intro.md\"]"
        },
        "model": "host-model",
        "stopReason": "endTurn"
      }
    },
    "requestState": "opaque-integrity-protected-value",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {"sampling": {}}
    }
  }
}
```

Việc thử lại không phải là một sự tiếp tục của một phiên giao thức. Nó là một yêu cầu mới lặp lại phương pháp và lập luận ban đầu, chỉ thêm các vòng hiện tại `inputResponses`, và tiếng vang `requestState`Byte cho byte.

> 重试 không phải là sự tiếp tục của cuộc họp thỏa thuận. Nó là một yêu cầu mới: 重复原始方法和参数, chỉ thêm vào các phiên trước.`inputResponses`,并逐字节回显 `requestState`

MRTR chỉ được phép vào `tools/call`- `prompts/get`, và`resources/read`Một máy chủ không được quay lại`input_required`từ các phương pháp không liên quan.

> MRTR chỉ được phép sử dụng `tools/call``prompts/get`和 `resources/read` máy chủ phải quay lại từ không liên quan`input_required`

## - Vị trí đa vòng.

> **【中文解读】**Trong nhiều vòng làm việc, máy chủ đưa các dữ liệu giữa giai đoạn và đã được học tập vào thứ tiếp theo.`requestState`❖ Đánh giá này như kẻ tấn công có thể kiểm soát được: chỉ ký một giai đoạn khỏa thân tên không đủ.`clientInfo`(nếu bạn có thể đọc được các thông tin của HMAC, bạn không cần phải sử dụng HMAC để kiểm tra thông tin của bạn.`-32602`拒绝. 客户端 phải giải quyết hoặc sửa đổi.`requestState`, trách nhiệm duy nhất của nó là từ từ từ trở lại.

Bài học này cần hai mẫu gọi:

1. `pick_files`trả lại một mảng JSON.
  Trung ngữ翻译:`pick_files`返回一个 JSON 数组──
2. `summary`trả lại câu thơ cuối cùng.
  Trung ngữ翻译:`summary`返回最终的散文摘要──

Mỗi lần thử lại chỉ mang lại các câu trả lời cho vòng đó. do đó máy chủ đưa các dữ liệu giai đoạn và trung gian được xác nhận vào vòng tiếp theo `requestState`- Tôi không biết.

> Mỗi lần thử lại chỉ mang lại phản ứng của vòng. Vì vậy máy chủ đưa giai đoạn và dữ liệu giữa đã được thử vào thứ hai.`requestState`

Hãy coi giá trị đó là bị kẻ tấn công kiểm soát.

> Đặt giá trị này như một kẻ tấn công có thể kiểm soát được để đối phó. Chỉ cần ký một giai đoạn khỏa thân tên là không đủ.

- Chủ đầu tư xác thực, không được báo cáo tự `clientInfo`-
  Trung ngữ翻译:已认证主体, chứ không phải tự báo `clientInfo`-
- phương pháp xuất xứ;
  Trung văn翻译:发起方法;
- Một bản ghi lại các luận điểm ban đầu;
  Trung văn翻译: sơ lược của các nguyên tố;
- Thời hạn ngắn;
  Trung文翻译:较短的过期时间;
- giai đoạn hiện tại và các giá trị trung gian được xác nhận.
  Trung ngữ翻译:当前阶段和已校验的中间值──

Sử dụng HMAC khi bảo mật không cần thiết. Sử dụng mã hóa xác thực khi khách hàng không được đọc trạng thái. Từ chối chữ ký không đúng, giá trị hết hạn, thay đổi nguyên tắc hoặc thay đổi các lập luận với `-32602`- Tôi không biết.

> Không cần mật khẩu khi sử dụng HMAC. Khách hàng phải đọc trạng thái khi sử dụng xác nhận mật mã.`-32602`拒绝.

Khách hàng không được phân tích hoặc sửa đổi `requestState`Công việc duy nhất của nó là phản ứng đúng dòng khi thử lại.

> 客户端 phải giải quyết hoặc sửa đổi `requestState` Công việc duy nhất của nó là thử lại để hiển thị một chuỗi chính xác

> ️ **【易错点】**场景:`requestState`Chỉ编码阶段名不做绑定校验,或客户端图省事解析/改它 / 后果: kẻ tấn công giả lập trạng thái nhảy vào bất kỳ giai đoạn nào 跨请求重放旧状态、换参数续跑别人开头工作流;改后服务器行为不可预期 / 修复:HMAC 或认证加密 + 五重绑定(主体/方法/参数摘要/过期/阶段与中值), bất kỳ thử nghiệm nào thất bại theo luật`-32602`; khách hàng bên chỉ làm theo từng chữ phần trở lại hiển thị.

## Mẫu ưu tiên là gợi ý

> **【中文解读】** `costPriority``speedPriority``intelligencePriority`Có ba ưu tiên độc lập, không phải phân bố xác suất, không cần phải tìm kiếm và để một; khách hàng có thể bỏ qua chúng, vì mô hình chiến lược trở lại khách hàng sở hữu.`includeContext` giữ cho `"none"` khác trên mô hình văn bản tăng nguy cơ rò rỉ và tự nó đã bị từ bỏ; trong yêu cầu chỉ truyền ít nhất rõ ràng trên văn bản.

`costPriority`- `speedPriority`, và`intelligencePriority`là những ưu tiên độc lập. Chúng không phải là phân phối xác suất và không cần phải cộng vào một. Khách hàng có thể bỏ qua chúng vì khách hàng sở hữu chính sách mô hình.

> `costPriority``speedPriority``intelligencePriority`Các phương pháp này không phải là phân phối xác suất, cũng không cần phải tìm kiếm và để một.

Cứ giữ lại`includeContext``"none"`nếu bạn duy trì một dòng chảy lấy mẫu cũ. Các chế độ ngữ cảnh khác làm tăng nguy cơ rò rỉ và tự nó bị lỗi thời. Đưa nội dung rõ ràng tối thiểu trong yêu cầu.

> Nếu bạn bảo vệ di sản 流程 lấy mẫu, hãy lấy`includeContext` giữ cho `"none"`◊ khác trên các mô hình văn bản sẽ tăng nguy cơ rò rỉ và tự nó đã bị từ bỏ ◊ trong các yêu cầu truyền tải ít nhất rõ ràng trên các văn bản ◊

## An toàn không thay đổi

> **【中文解读】**客户端是嵌入 样本请求的信任边界──七条不变量: 策略要求时向用户展示服务器想让模型做什么;给MRTR 轮数设限上限;;恶意服务器否则可制造模型花费循环); mỗi 样本响应应用文件名、URL或工具输入前校验;限制每轮字节数和代码数;拒绝未在当前客户端能力声明中输入请求;模型输出不得参与授权决策;发行记录方法和输入请求键但不记得敏感提示内容──`clientInfo`和 `serverInfo`là hiển thị và chẩn đoán dữ liệu, không thể được xác nhận như một người.

Khách hàng là giới hạn tin cậy cho các yêu cầu lấy mẫu nhúng.

> 客户端是嵌入式 样本 请求的信任边界──

- Cho người dùng thấy máy chủ yêu cầu mô hình làm gì khi chính sách yêu cầu phê duyệt.
  Trung ngữ翻译:策略要求审批时,向用户展示服务器正在让模型做什么──
- Một máy chủ độc hại có thể tạo ra một vòng chi tiêu mô hình.
  Trung文翻译: 给MRTR 轮数设上限──否则恶意服务器可以制造模型花费循环──
- Thiết lập từng phản ứng lấy mẫu trước khi sử dụng nó như tên tập tin, URL hoặc đầu vào công cụ.
  Trung ngữ翻译: mỗi mẫu đáp应在被用作文件名、URL或工具输入之前都要校验──
- Giới hạn các byte và token mỗi vòng.
  Trung ngữ翻译:限制每轮的字节数和符号数──
- Từ chối yêu cầu nhập mà không được tuyên bố trong khả năng của khách hàng hiện tại.
  Trung ngữ翻译:拒绝未在当前客户端能力中声明的输入请求──
- Giữ sản xuất mô hình ra khỏi các quyết định ủy quyền.
  Trung ngữ翻译:模型输出不得参与授权决策.
- Lập nhật phương pháp xuất phát và khóa yêu cầu nhập mà không ghi nội dung yêu cầu nhạy cảm.
  Trung ngữ翻译:记录发起方法和输入请求键, nhưng không ghi lại nội dung gợi ý nhạy cảm.

`clientInfo`và `serverInfo`là hiển thị và chẩn đoán metadata. Không bao giờ sử dụng cả hai như một danh tính xác thực.

> `clientInfo`和 `serverInfo`Đây là một số dữ liệu được chứng minh và xác định.

```figure
t3-sampling-flip
```

## Hãy xây dựng nó.

> **【中文解读】**Ví dụ sử dụng thư viện tiêu chuẩn hoàn chỉnh hai vòng: phát hiện trở lại phiên bản và缓存提示; dụng cụ phát hiện trở lại xác định tính mô tả; mỗi lần调用 trường thử yêu cầu dữ liệu; đầu tiên kết quả được đặt vào các tệp chọn; đầu tiên kết quả của mô hình thử nghiệm lần đầu tiên và được đặt vào một yêu cầu thứ hai; HMAC  bảo vệ của`requestState`Trong giai đoạn liên quan đến yêu cầu độc lập; kết quả cuối cùng`complete`假宿主模型保证例证确定性接真宿主时只换 `fake_host_model`, tình trạng bên máy chủ nên giữ được xác định 可测──

`code/main.py`thực hiện toàn bộ dòng chảy hai vòng mà không có gói của bên thứ ba:

- `server/discover`trả lại `supportedVersions`, quảng cáo hỗ trợ công cụ, và trả về gợi ý cache.
  Trung ngữ翻译:`server/discover` quay lại `supportedVersions`、 công bố công cụ hỗ trợ và trả lại缓存提示。
- `tools/list`trả lại một định nghĩa, cacheable `summarize_repo`mô tả với một sơ đồ nhập đối tượng.
  Trung ngữ翻译:`tools/list`返回带对象输入方案的确定性、可缓存 `summarize_repo`描述符──
- `tools/call`xác nhận metadata theo yêu cầu.
  Trung ngữ翻译:`tools/call`校验逐请求元数据──
- Kết quả đầu tiên là kết quả `sampling/createMessage`cho việc chọn tập tin.
  Trung ngữ翻译:第一个结果嵌入用于选文件的`sampling/createMessage`
- Lần thử lần đầu tiên xác nhận kết quả mô hình và nhúng một yêu cầu thứ hai.
  Trung文翻译:第一次重试验证模型结果并嵌入第二请求──
- Được bảo vệ bởi HMAC `requestState`tiến hành giai đoạn giữa các yêu cầu độc lập.
  中文翻译:HMAC 保护的 `requestState`Trong khi đó, họ đã có một số người khác.
- Kết quả cuối cùng sử dụng `resultType: "complete"`- Tôi không biết.
  Trung文翻译:最终结果使用 `resultType: "complete"`

Mô hình máy chủ giả tạo ví dụ xác định.`fake_host_model`Máy trạng thái bên máy chủ nên vẫn xác định và kiểm tra được.

> 假宿主模型让例保持确定性──接入真实宿主时只换换 `fake_host_model` Các máy chủ bên cạnh trạng thái nên giữ được xác định và có thể kiểm tra.

## Hãy sử dụng nó để thực hiện

Từ nguồn kho:

```bash
cd phases/13-tools-and-protocols/11-mcp-sampling/code
python3 main.py
python3 -m unittest discover tests -v
```

Các điểm kiểm soát dự kiến:

- Discovery trả lại kết quả hoàn chỉnh với `ttlMs`và `cacheScope`- Tôi không biết.
  Trung ngữ翻译:发现返回带 `ttlMs`和 `cacheScope`Kết quả hoàn chỉnh của...
- Công cụ phát hiện trả lại mô tả được sắp xếp giống như `resultType`, danh tính máy chủ, và gợi ý cache.
  Trung文翻译:工具发现返回相同排序的描述符,带 `resultType`、 danh tính và lưu trữ của máy chủ
- Các khả năng bị thiếu và các phiên bản không được hỗ trợ sử dụng chính xác `-32021`và `-32022`dữ liệu lỗi.
  Trung ngữ翻译:能力缺失和不支持的版本使用精确的 `-32021`和 `-32022`错误数据――
- Một thông báo không có id không tạo ra phản ứng JSON-RPC.
  Trung文翻译:无 id 的通知不产生 JSON-RPC 响应──
- Các thẻ nhận dạng yêu cầu là `[1, 2, 3]`, chứng minh mỗi vòng MRTR là độc lập.
  中文翻译:请求 id 是 `[1, 2, 3]`, chứng minh mỗi MRTR 轮次相互独立.
- Hai kết quả đầu tiên là`input_required`- Tôi không biết.
  Trung ngữ翻译:前两个结果是 `input_required`
- Kết quả cuối cùng là`complete`và chứa các tệp được chọn cộng với bản tóm tắt.
  Trung ngữ翻译:最终结果是 `complete`, bao gồm các tài liệu và bản tóm tắt được chọn.
- Thay đổi các lập luận ban đầu trong một lần thử lại thất bại kiểm tra yêu cầu- trạng thái.
  Trung文翻译:重试时改变原始参数会未经请求状态检查──

## Chuyển nó đi.

`outputs/skill-sampling-loop-designer.md`Nếu tính tương thích được yêu cầu, nó sẽ tạo ra các vòng MRTR, liên kết trạng thái, cổng khả năng, ngân sách, xác thực và kế hoạch loại bỏ.

> `outputs/skill-sampling-loop-designer.md`Bây giờ là một lập trình chuyển đổi. Nó quyết định trước xem liệu nó nên di chuyển Sampling 改用直连模型集成. Nếu cần hợp nhất, nó sẽ phát triển MRTR 轮次 状态绑定 能力门 预算 校验和移动计划.

## Tập luyện bài tập

1. Thay đổi phản ứng chọn tệp thành JSON không hợp lệ. xác nhận máy chủ trả lại `-32602`thay vì tin vào sản lượng mô hình.
   Trung文翻译:把文件选择响应改成非法 JSON──确认服务器返回 `-32602`Thay vì tin tưởng mô hình xuất khẩu.
2. Thay đổi`audience`Giải thích tại sao trạng thái đóng kín ngăn chặn việc tái sử dụng yêu cầu chéo.
   Trung ngữ翻译: trong đầu tiên调用和重试之间变化 `audience`❖ giải thích tại sao tình trạng mật có thể ngăn chặn việc yêu cầu lặp lại.
3. Thêm một vòng thứ ba yêu cầu chủ nhà phê bình bản tóm tắt. Mang bản tóm tắt trước đó vào trạng thái ký và hạn chế toàn bộ dòng chảy ở ba vòng.
   Trung ngữ翻译:添加请宿主评审摘要的第三轮──把早期的摘要放进签名状态带来,并把整个流程限制在三轮──
4. Xóa Sampling bằng cách thay thế callback host giả bằng một bộ điều chỉnh mô hình thuộc sở hữu của máy chủ.
   Trung ngữ翻译: dùng máy chủ riêng để thay thế người chủ giả để chuyển Sampling。 liệt kê những nhiệm vụ phê duyệt, tính phí và khả quan chuyển sang máy chủ。
5. Thêm một bài kiểm tra hết hạn bằng giá trị trạng thái là một giây quá hạn của nó.
   Trung ngữ翻译: dùng một hơn thời gian截止 một giây của trạng thái giá trị thêm quá期测试。

## Từ khóa  Từ khóa nhanh chóng

| Term | Meaning in 2026-07-28 | 中文术语 |
|------|------------------------|----------|
| Sampling | Deprecated feature that asks the client's model for a completion | 采样（已弃用） |
| MRTR | Stateless retry pattern for client input required during a request | 多轮往返请求 |
| `InputRequiredResult` | Result with `resultType: "input_required"` | 需输入结果 |
| `inputRequests` | Server-assigned map of embedded elicitation, sampling, or roots requests | 嵌入请求映射 |
| `inputResponses` | Current round's client results keyed like `inputRequests` | 本轮输入响应 |
| `requestState` | Opaque server state echoed exactly by the client and verified by the server | 请求状态（不透明） |
| `resultType` | Required discriminator for modern MCP results | 结果类型判别符 |
| Direct model integration | Recommended replacement for new servers that need model inference | 直连模型集成 |
| Capability gate | Rule that prevents sending an embedded request the client did not advertise | 能力门 |
| Loop budget | Maximum rounds, tokens, bytes, time, and spend allowed for the operation | 循环预算 |

## Hỗ trợ Legacy

> **【中文解读】**钉 vào năm 2025-11-25 các khách hàng vẫn có thể được kết nối trực tiếp với các máy chủ cũ khởi động `sampling/createMessage`流程──把那种行为只放进按版本隔离的适配器,绝不把有会话路径当作2026-07-28 服务器的架构──官方 SDK có thể được dùng cho cũ đối端翻译现代`input_required`处理器那片是兼容边界,不是添加新的依赖会话逻辑的许可

Một client được gắn vào 2025-11-25 vẫn có thể sử dụng máy chủ khởi động cũ hơn `sampling/createMessage`lưu thông qua kết nối trực tiếp. Giữ hành vi đó chỉ trong một bộ điều chỉnh cụ thể cho phiên bản. Đừng làm cho con đường sessionful kiến trúc cho một máy chủ 2026-07-28.

> 钉 vào năm 2025-11-25 các khách hàng vẫn có thể sử dụng các máy chủ cũ trên kết nối sống`sampling/createMessage`流程── đó là hành vi chỉ được giữ lại trong các phiên bản riêng biệt của các bộ điều chỉnh.

Các SDK chính thức có thể dịch hiện đại `input_required`Đó là một ranh giới tương thích, không phải là quyền để thêm logic phụ thuộc vào phiên mới.

> 官方 SDK có thể được dùng để làm cho các phần mềm cũ hơn`input_required`处理器. 片 là兼容边界, không phải là thêm một sự phụ thuộc mới vào logic.

## Xem thêm 延伸阅读

- [MCP 2026-07-28 Multi Round-Trip Requests](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr)
  Trung ngữ翻译:MRTR 模式的权威规范
- [MCP 2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
  Trung文翻译:2026-07-28 修订的完整变更清单
- [MCP Sampling deprecation](https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging)
  中文翻译:Sampling 弃用 SEP 提案原文
- [MCP 2026-07-28 server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  Trung ngữ翻译:`server/discover`发现契约规范
