# Xây dựng máy chủ MCP: Python không trạng thái và TypeScript

> Một máy chủ MCP hiện đại không nhớ một cú tay. Nó xác nhận metadata trên mỗi yêu cầu, chạy một bộ xử lý và trả lại một kết quả được gõ.

> **【中文解读】**MCP  máy chủ hiện đại không nhớ bất kỳ tay nào. Nó đối với mỗi yêu cầu kiểm tra dữ liệu.`params._meta`、 phải chọn `server/discover`、 danh sách có thể lưu trữ thứ tự xác định và thống nhất `resultType`Kết quả bao bì.

> **【拓展：MCP 服务器→Claude 生态开发】**MCP  máy chủ là Claude 生态的标准工具接口形态:Claude Desktop、Cursor、VS Code 等宿主都通过studio或HTTP 启动你的服务器并调用其工具──旧教程以初始化 握手开场;2026-07-28 之后无状态内核反而更简单没有连接状态要维护,任何副本都能处理任何请求──理解本课的 stdlib 实现后,迁移到官方SDK 只是改变语法──

>  **【前置】**学本节前请先掌握:(1) Giai đoạn 13 · 06(MCP 基础)无状态请求模型、`params._meta`3 bộ,`server/discover``resultType`- Không.`ttlMs`- Không.`cacheScope`;(2) Python 子 process với stdin/stdout 逐行通信;(3) JSON-RPC 2.0 错误码(-32700/-32600/-32601/-32602/-32603 与 MCP 专属的 -32022)

**Type:** Build | **类型:** 构建
**Languages:** Python, TypeScript | **语言:** Python, TypeScript
**Prerequisites:** Phase 13, Lesson 06 | **前置知识:** Phase 13, Lesson 06
**Time:** ~85 minutes | **时间:** ~85 分钟

## Mục tiêu học tập

- Thực hiện bắt buộc `server/discover`cho MCP `2026-07-28`- Tôi không biết.
  中文翻译:为 MCP `2026-07-28`实现必选的 `server/discover`
- Thiết lập phiên bản giao thức và khả năng của khách hàng trên mỗi yêu cầu.
  Trung ngữ翻译: 在每个请求上校验协议版本和客户端能力──
- Khám phá các công cụ, tài nguyên và lời nhắc với thứ tự danh sách xác định.
  Trung文翻译:以确定性列表排序暴露工具、资源和提示──
- Trở lại`resultType`, danh tính máy chủ, và cache gợi ý về kết quả chính xác.
  Trung ngữ翻译: 在正确的结果上回归 `resultType`、 danh tính và lưu trữ của máy chủ
- Dịch vụ hợp đồng không có quốc tịch tương tự trên newline-delimited studio trong Python và TypeScript.
  Trung ngữ翻译:用Python和TypeScript 在换行分隔的studio 上提供同一个无状态契约──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**旧式服务器把第一个请求的功能存下来复用,好写但运维:同一进程先后服务多个客户端、远程请求落到不同工作者时,过期能力声明会跨授权边界泄漏行为──2026-07-28 Sử dụng"每个请求自描述" giải quyết vấn đề của协议层; ứng dụng của bạn vẫn có thể giữ ghi chép, nhiệm vụ等持久状态, điều duy nhất cấm là ảnh hưởng đến trạng thái ẩn协议 của các yêu cầu giải mã sau đó──2026-07-28

Một máy chủ lưu trữ khả năng của khách hàng sau khi tin nhắn đầu tiên là dễ dàng để xây dựng và khó hoạt động.

> Một máy chủ có khả năng lưu trữ khách hàng sau khi gửi thông tin đầu tiên dễ viết nhưng khó vận hành.

MCP `2026-07-28`ứng dụng của bạn vẫn có thể giữ các ghi chú lâu dài, công việc, hoặc xử lý trạng thái rõ ràng. Điều mà nó không thể giữ là trạng thái giao thức ẩn thay đổi cách giải mã yêu cầu sau đó.

> MCP `2026-07-28`Bằng cách cho mỗi yêu cầu tự mô tả để giải quyết vấn đề này phần của thỏa thuận. Ứng dụng của bạn vẫn có thể giữ lại ghi chép lâu dài, nhiệm vụ hoặc trạng thái hiển nhiên.

Bài học này xây dựng một máy chủ ghi chú hai lần. Phiên bản Python và TypeScript chỉ sử dụng thư viện tiêu chuẩn của họ cho lõi giao thức. Cả hai phơi bày các phương pháp tương tự và thực thi hợp đồng dây tương tự.

> Bài học này đã xây dựng một máy lưu trữ máy tính hai lần. Các bản Python và bản TypeScript chỉ sử dụng các bản chuẩn riêng của mình.

## Khái niệm cốt lõi

### Loop chuyển giao hiện đại

> **【中文解读】**现代分发循环九步:读一行 JSON-RPC → 解析信封 → 通知不响应 → 校验本请求的参数._meta → 按方法路由 → 用结果Type 和 serverInfo 包装成功 → 写一行响应 → 忘记请求级元数据――studio 三条铁律不变:stdout只写 JSON-RPC(诊断走 stderr) 换行分隔并逐条 flush、stdin EOF 即退不――进程生命周期只是传输层生命周期,MCP 会话――

```text
read one JSON-RPC line
parse the envelope
if it is a notification, do not respond
validate params._meta for this request
route by method
wrap success with resultType and serverInfo
write one JSON-RPC response line
forget request-scoped metadata
```

Ba quy tắc của studio vẫn còn quan trọng:

- Chỉ viết tin nhắn JSON-RPC cho stdout.
  Trung文翻译: chỉ hướng đến stdout 写 JSON-RPC 消息──诊断信息发发到 stderr──
- Định nghĩa các tin nhắn bằng một dòng mới và đánh dấu mỗi câu trả lời.
  Trung文翻译:用换行符分隔消息并逐条 flush 响应。
- Hãy ra khỏi ngay khi Stdin đến EOF.
  Trung文翻译:đừng đến EOF 时立即退出──

Thời gian vận chuyển là thời gian vận chuyển, không phải là một phiên MCP hiện đại.

> Chu kỳ đời sống của quá trình chỉ là chu kỳ đời sống truyền tải.

> ️ **【易错点】**场景:调试时用 `print()`往 stdout 打印变量 / 后果:stdout 混入非 JSON 文本,客户端解析信封失败断连;另常见坑是忘记 `flush()`导致响应滞留缓冲区,客户端超时 / 修复: tất cả các chẩn đoán输出走 `sys.stderr`(hoặc khai thác,默认 stderr), mỗi条响应 `sys.stdout.write(json.dumps(...) + "\n")`后立即 `flush()`

### Đơn xin xác thực

Mỗi yêu cầu phải có:

> Mỗi yêu cầu phải có:

```json
{
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        "name": "notes-client",
        "version": "1.0.0"
      }
    }
  }
}
```

Hai trường đầu tiên là cần thiết. `clientInfo`được khuyến cáo. xác nhận hình dạng danh tính hiện tại, nhưng không coi nó như xác thực.

> Trước hai đoạn là cần phải điền.`clientInfo`                                                                                                                                                                                                                                                              

Nếu phiên bản không được hỗ trợ, trả lại mã `-32022`với `requested`và `supported`. Mất dữ liệu liên quan đến yêu cầu là param không hợp lệ, mã `-32602`Đừng bao giờ điền vào các trường bị mất từ cuộc gọi trước đó.

> Nếu phiên bản không được hỗ trợ, trả lại lỗi `-32022`Và`requested`Với`supported`◊ thiếu yêu cầu dữ liệu thuộc vô hiệu lực, trả lại `-32602`                                                                                                                                                                                                                                                              

### Việc khám phá bắt buộc

Các máy chủ hiện đại phải triển khai `server/discover`. Kết quả phát hiện đầy đủ bao gồm các phiên bản hiện đại được hỗ trợ, khả năng, hướng dẫn tùy chọn, gợi ý cache và nhận dạng máy chủ kết quả `_meta`- Có thể là:

> 现代服务器 phải được thực hiện `server/discover`◊ Kết quả phát hiện đầy đủ bao gồm hỗ trợ phiên bản hiện đại, khả năng, sử dụng có thể chọn, lưu trữ, và kết quả`_meta`Trung ương dịch vụ:

```json
{
  "resultType": "complete",
  "supportedVersions": ["2026-07-28"],
  "capabilities": {
    "tools": {"listChanged": false},
    "resources": {"listChanged": false, "subscribe": false},
    "prompts": {"listChanged": false}
  },
  "ttlMs": 3600000,
  "cacheScope": "public",
  "_meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "notes-server",
      "version": "2.0.0"
    }
  }
}
```

Discovery không mở khóa máy chủ.`tools/list`Không gọi là khám phá bởi vì`tools/list`đã mang cùng một yêu cầu metadata.

> 发现不会"解锁"服务器──客户端 có thể không sử dụng 发现而直接调用 `tools/list`Vì`tools/list`Chúng ta cũng có cùng một yêu cầu với dữ liệu.

### Công cụ

> **【中文解读】**工具部分两条线:`tools/list`返回确定性排序的工具描述符(稳定排序改善响应缓存并保持模型上下文稳定), kết quả phải带 `ttlMs`和 `cacheScope`-`tools/call`返回内容块和 `isError`△ lỗi có hai tầng:协议信封或方法参数无效 → lỗi JSON-RPC;调用合法但工具本身失败 → `isError: true` This makes the model can read fail causes in up below in the text并自我修复, thay vì chỉ nhận được một liên kết lớp lỗi                                                                                                                                                                                                                                               

`tools/list`trả lại một danh sách xác định của mô tả công cụ. Stable ordering cải thiện lưu trữ dự trữ phản ứng và giữ cho bối cảnh mô hình ổn định. Kết quả cũng yêu cầu`ttlMs`và `cacheScope`- Tôi không biết.

> `tools/list`返回确定性排序的工具描述符列表──稳定排序改善响应缓存并保持模型上下文稳定──该结果还必须带`ttlMs`和 `cacheScope`

`tools/call`trả lại các khối nội dung và `isError`Sử dụng lỗi JSON-RPC khi gói giao thức hoặc các tham số phương pháp không hợp lệ. Sử dụng `isError: true`khi một công cụ invocation hợp lệ chạy nhưng công cụ tự thất bại.

> `tools/call`返回内容块和 `isError` giao thức tín hiệu hoặc phương pháp không hiệu quả khi sử dụng lỗi JSON-RPC; công cụ hợp pháp đã được thực hiện nhưng công cụ tự nó thất bại khi sử dụng `isError: true`

Các chú thích về công cụ vẫn là gợi ý, không phải là thực thi:

- `readOnlyHint`
  Trung ngữ翻译:`readOnlyHint`( chỉ đọc lời khuyên)
- `destructiveHint`
  Trung ngữ翻译:`destructiveHint`(破坏性提示)
- `idempotentHint`
  Trung ngữ翻译:`idempotentHint`(等提示)
- `openWorldHint`
  Trung ngữ翻译:`openWorldHint`(Openworld提示)

Người chủ nhà nên sử dụng chúng để xác nhận và trình bày.

> Chủ nhà nên sử dụng chúng để xác nhận và hiển thị.

### Tài nguyên

`resources/list`trả lại các mô tả URI ổn định. `resources/read`trả lại nội dung được gõ. Cả hai đều có thể lưu trữ trong `2026-07-28`, nên cả hai đều bao gồm`ttlMs`và `cacheScope`- Tôi không biết.

> `resources/list`返回稳定的 URI 描述符──`resources/read`返回类型化内容──两者在 `2026-07-28`Trong đó có tất cả có thể lưu trữ, vì vậy tất cả bao gồm.`ttlMs`和 `cacheScope`

Sử dụng `cacheScope: "private"`cho dữ liệu ghi chú cụ thể cho người dùng. Một bộ nhớ cache được chia sẻ không được sử dụng lại một phản ứng riêng tư trên các bối cảnh ủy quyền.

> Ứng dụng sử dụng`cacheScope: "private"` chia sẻ缓存不得跨授权上下文复用一个私人响应

Việc chuyển đổi hiện đại không sử dụng `resources/subscribe`Một khách hàng mở cửa`subscriptions/listen`và yêu cầu `resourceSubscriptions`Bài học 10 xây dựng dòng chảy đó.

> 现代的变更投递 không còn được sử dụng `resources/subscribe`❖ khách hàng mở cửa `subscriptions/listen`并 yêu cầu`resourceSubscriptions`Hoặc danh sách biến đổi类别. Bài học 10 xây dựng quá trình đó.

### Các lời nhắc nhở

`prompts/list`là cacheable và xác định. `prompts/get`kết quả prompt được render hoàn chỉnh, nhưng nó không phải là một trong danh sách cache hoặc kết quả đọc cần các gợi ý cache.

> `prompts/list`Có thể lưu trữ và xác định thứ tự.`prompts/get`Sử dụng các tham số 染命名 prompt──染出的 prompt 结果是完整的,但它不属于必须带缓存提示的那类可缓存列表/读取结果──

### Mỗi kết quả thành công đều được đánh dấu

> **【中文解读】**Tất cả kết quả thành công đi cùng một hàm đóng gói:打上 `resultType: "complete"`和 `_meta`里服务器Info;列表,读取和发现这三类处理器 再补`ttlMs`Với`cacheScope`◊ tập trung một phần đóng gói nghĩa là ngăn chặn một người xử lý 漏掉现代结果字段漏一个字段, khách hàng就可能按旧时代解读你的响应──

Các ví dụ sử dụng một gói cho mỗi thành công:

```python
def complete(payload):
    return {
        "resultType": "complete",
        **payload,
        "_meta": {SERVER_INFO_KEY: SERVER_INFO},
    }
```

Danh sách, đọc và phát hiện người xử lý thêm `ttlMs`+`cacheScope`Việc tập trung bao bì này ngăn cản một người xử lý từ chối lặng lẽ bỏ qua các trường kết quả hiện đại.

> 列表、读取和发现处理器 追加 `ttlMs`Với`cacheScope`Hãy tập trung gói này lên, để ngăn chặn một người xử lý  bỏ qua.

### Không có yêu cầu được khởi động bởi máy chủ

> **【中文解读】**Các máy chủ hiện đại có thể phát hành hai loại thứ: thông báo liên quan đến yêu cầu của khách hàng và mở khách hàng.`subscriptions/listen`流上的通知──它 phải khởi động phát hành JSON-RPC của riêng mình 请求──当处理器 需要采样,发明或根 输入时,它返回`input_required`Kết quả, do khách hàng bổ sung trong các yêu cầu nhập sau khi sử dụng ID yêu cầu mới 重试原方法 đây là "多轮往返请求" (Các yêu cầu nhiều chuyến đi vòng) mô hình, Bài học 11 展开。

Một máy chủ hiện đại có thể gửi thông báo liên quan đến yêu cầu của khách hàng hoặc thông báo trên một máy chủ mở `subscriptions/listen`Nó không được gửi yêu cầu JSON-RPC của riêng nó.

> 现代服务器 có thể gửi thông báo liên quan đến yêu cầu của khách hàng, hoặc mở trong khách hàng.`subscriptions/listen`流上发送通知──它 phải gửi bản thân JSON-RPC                                                                                                                                                                                                                                                       

Khi một người xử lý cần lấy mẫu, tạo ra hoặc nhập gốc, nó trả lại một `input_required`kết quả. Client đáp ứng các yêu cầu nhập được nhúng và thử lại phương pháp ban đầu với một ID yêu cầu mới. Bài học 11 bao gồm mô hình yêu cầu nhiều chuyến đi vòng.

> Khi người xử lý cần lấy mẫu, tạo ra hoặc gốc 输入时, nó quay lại`input_required`Kết quả:  Các ứng dụng được cài đặt trong các ứng dụng, sau đó sử dụng các ứng dụng mới.

### Sự tương thích rõ ràng của sản phẩm

Một máy chủ hai thời đại cũng có thể thực hiện các`2025-11-25`Nhấn tay vào một nhánh di sản rõ ràng tách biệt. Nó chọn hành vi hiện đại khi cần hiện đại`_meta`các trường hiện diện và di sản hành vi khi nó nhận `initialize`- Tôi không biết.

> 双时代服务器 có thể `2025-11-25`握手实现在一条清晰分离的旧版分支上. 应请求带必需的现代.`_meta`字段时选择现代行为, nhận được `initialize`时选择旧版行为──

Đừng đặt một `2026-07-28`xin thông qua con đường bắt tay cũ. Đừng đóng dấu hiện đại `resultType`mã trong bài học này là cố ý hiện đại chỉ để các biến số của nó vẫn còn hiển thị.

> Đừng để `2026-07-28`Xin hãy đi theo cách cũ. Đừng làm nó hiện đại.`resultType`字段盖到旧版初始化结果上──本课代码刻意只做现代版,好让不变式保持可见──

>  **【类比】**双时代服务器像机场的双通道边检:一条"电子护照自助通道" (trước đây: 现代:刷护照自描述通过),一条"人工柜台" (trước đây: 排队登记握手)`_meta`三件套 → 现代;发 `initialize`→ 旧版),两条通道物理隔离、互不借用流程──最忌讳的是开一条"混合通道"现代请求被拉拉排队握手,或旧版结果被贴在电子通道的标签──

```figure
t3-dispatch-loop
```

## Hãy sử dụng nó để thực hiện

Thực hiện demo và thử nghiệm hữu hạn của máy chủ Python:

> 运行 Python 服务器的有限演示和测试:

```bash
cd code
python3 main.py --demo
python3 -m unittest discover tests -v
```

Tiến TypeScript với một trình chạy TypeScript:

> 用 TypeScript 运行器 chạy TypeScript 移植版:

```bash
npx tsx main.ts --demo
```

Demo gửi đi`server/discover`, liệt kê từng nguyên thủy, gọi các công cụ, và hiển thị lỗi phiên bản không được hỗ trợ.

> 演示发送 `server/discover`,逐个列出原语,调用工具,并显示一个不支持的版本错误――每个现代请求都重复携带元数据――每个成功结果都包含服务器身份――

## Chuyển nó đi.

Bài học này sẽ đi theo `outputs/skill-mcp-server-scaffolder.md`Nó tạo ra một kế hoạch máy chủ hiện đại với hợp đồng phát hiện, xác nhận theo yêu cầu, danh sách cache xác định và một bộ chuyển đổi di sản riêng biệt tùy chọn.

> 本课交付 `outputs/skill-mcp-server-scaffolder.md`Nó xuất hiện một kế hoạch máy chủ hiện đại: tìm thấy các thỏa thuận, từng yêu cầu, kiểm tra, xác định danh sách có thể lưu trữ, cũng như một ứng dụng cũ có thể được phân lập.

## Tập luyện bài tập

1. Xóa các khả năng từ một yêu cầu và chứng minh máy chủ không sử dụng lại tuyên bố yêu cầu trước đó.
   Trung ngữ翻译: Từ một yêu cầu trong khả năng di chuyển, chứng minh máy chủ sẽ không sử dụng lại trên một yêu cầu tuyên bố.

2. Chuyển lại `TOOLS`- `PROMPTS`, và ghi chú thứ tự để đưa vào.
   Trung ngữ翻译:反转 `TOOLS``PROMPTS`和笔记的插入顺序──确认所有列表结果保持稳定──

3. Thêm một cái phá hủy `notes_delete`công cụ và yêu cầu kiểm tra ủy quyền bên trong trình thực.`destructiveHint`chỉ là một gợi ý UX.
   Trung ngữ翻译:添加一个破坏性的 `notes_delete`工具,并要求在执行器内部做授权检查──`destructiveHint`Chỉ để dành cho UX 提示

4. Thêm `resources/templates/list`với `ttlMs`- `cacheScope`, và định nghĩa thứ tự.
   Trung ngữ翻译:添加带 `ttlMs``cacheScope`Và sự xác định của`resources/templates/list`

5. Xây dựng một bộ chuyển đổi cũ riêng cho `2025-11-25`Thêm thêm các xét nghiệm chứng minh rằng một yêu cầu hiện đại không bao giờ được đưa vào.
   中文翻译:为 `2025-11-25`构建一个独立的旧版适配器──添加测试证明现代请求绝不会进入它──

## Từ khóa  Từ khóa nhanh chóng

| Term | Meaning |
|------|---------|
| Stateless server | Handles each request from its own metadata without protocol-session memory |
| `server/discover` | Mandatory modern method that advertises versions and capabilities |
| Complete result | Successful modern result with `resultType: "complete"` |
| Cacheable result | Discovery, list, or resource-read result with `ttlMs` and `cacheScope` |
| Deterministic list | Same logical registry produces the same item order |
| Server identity | Recommended `io.modelcontextprotocol/serverInfo` in result `_meta` |
| Tool error | Valid tool call that returns content with `isError: true` |
| Protocol error | Invalid JSON-RPC or MCP request returned through `error` |

> 术语中文对照:Stateless server=无状态服务器(只凭请求自元数据处理,无协议会话记忆);server/discover=服务器发现(必选现代方法,公示版本与能力);Complete result=完整结果(带 `resultType: "complete"`Kết quả có thể được che giấu = có thể lưu trữ kết quả`ttlMs`Với`cacheScope`);Deterministic list=确定性列表(同一逻辑注册表产出同一顺序);Server identity=服务器身份(结果 `_meta`中建议的服务器Info);Tool error=工具错误(合法调用返回内容且 `isError: true`);Phỏng lẻo giao thức=协议错误(không hợp pháp JSON-RPC hoặc MCP `error`返回) 』

## Xem thêm 延伸阅读

- [MCP Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/)
  Trung văn翻译:MCP 2026-07-28 规范全文
- [MCP Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  Trung文翻译:server/discover 方法规范
- [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
  Trung ngữ翻译:tools 原语规范
- [MCP Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
  Trung ngữ翻译: nguồn lực 原语规范
- [MCP Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts)
  中文翻译:phản hồi 原语规范
- [MCP stdio Transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)
  Trung文翻译:studio 传输层规范
