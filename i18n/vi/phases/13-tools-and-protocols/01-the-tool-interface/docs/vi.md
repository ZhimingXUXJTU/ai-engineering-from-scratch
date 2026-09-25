# Các công cụ giao diện tại sao đại lý cần cấu trúc I / O  công cụ giao diện: tại sao đại lý cần cấu trúc nhập khẩu xuất khẩu

> Một mô hình ngôn ngữ tạo ra các token. Một chương trình thực hiện các hành động. Khoảng cách giữa hai đó là giao diện công cụ: một hợp đồng cho phép mô hình yêu cầu một hành động và chủ nhà thực hiện nó. Mỗi 2026 xếp hàng  hàm gọi vào OpenAI, Anthropic và Gemini; MCP `tools/call`; Các phần nhiệm vụ của A2A là một mã hóa khác của cùng một vòng lặp bốn bước. Bài học này đặt tên vòng lặp và cho thấy cơ chế tối thiểu để chạy nó.

> **【中文解读】**语言模型生成代币,程序执行动作──工具接口是连接两者的桥梁一个让模型请求动作──宿主执行动作的契约──2026 年所有主流都是同一四步循环的不同编码──

> **【拓展：工具接口→AI Agent 基础】**工具接口 là một chi tiết trung tâm của AI Agent.`tools/call`OpenAI của`tool_calls`Các phần nhiệm vụ của A2A là sự thực hiện khác của trừu tượng này.

>  **【前置】**学本节前请先掌握:(1) Bước 11·01(Prompt Engineering) 理解 LLM 如何生成代币;(2) Bước 11·03(Structured Outputs) JSON Schema 基础,本节输入 schema 全靠它;(3) Python 字典、JSON 序列化基础──本节不需要真实 LLM,用 stdlib 模拟,重点在理解循环结构而不是API──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, no LLM) | **语言:** Python（标准库，无 LLM）
**Prerequisites:** Phase 11 (LLM completion APIs) | **前置知识:** Phase 11（LLM 补全 API）
**Time:** ~45 minutes | **时间:** 约 45 分钟

## Mục tiêu học tập

- Giải thích tại sao một LLM chỉ có thể tạo ra văn bản không thể, một mình, thực hiện hành động chống lại thế giới thực.
  Trung ngữ翻译: giải thích tại sao một LLM chỉ có thể tạo văn bản không thể hoạt động độc lập với thế giới thực.
- Hình vẽ vòng gọi công cụ bốn bước (xác định → quyết định → thực hiện → quan sát) và đặt tên ai là chủ sở hữu của mỗi bước.
  Trung文翻译:绘制四步工具调用循环(描述→决定→执行→观察)并指出每一步的归属方──
- Viết mô tả công cụ như ba phần: tên, đầu vào JSON Schema và hàm thực thi xác định.
  Trung文翻译:将工具描述写成三部分:名称、JSON Schema 输入和确定性执行器函数。
- Sự khác biệt giữa các công cụ tinh khiết và tác dụng phụ và nêu rõ tại sao việc chia cắt quan trọng đối với an toàn.
  Trung ngữ: phân biệt công cụ tinh khiết và công cụ có tác dụng phụ, và minh họa tầm quan trọng của sự phân biệt đối với an toàn.

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**LLM chỉ có thể phát hành token, đó là phương thức phát hành duy nhất của nó. Nó không thể trực tiếp điều khiển API, cơ sở dữ liệu hoạt động hoặc thực hiện bất kỳ động tác bên ngoài nào.

> **【拓展：Function Calling 的商业影响】**Tháng 6 năm 2023 OpenAI  Lanh ra Chức năng gọi  sau đó, AI  ứng dụng phát triển mô hình xảy ra thay đổi cơ bản. Theo số liệu của OpenAI, năm 2025 có hơn 80% API 调用 liên quan đến tool_use, từ đơn giản về điều tra thời tiết đến phức tạp nhiều bước sắp xếp dòng công việc.

Một LLM phát ra phân phối xác suất trên token tiếp theo. Đó là toàn bộ bề mặt đầu ra. Nếu bạn hỏi một mô hình trò chuyện "giờ này thời tiết ở Bengaluru là gì", nó có thể viết một câu có thể tin được, nhưng nó không thể quay vào API thời tiết. Câu đó có thể đúng bởi tình cờ hoặc ba ngày bị lỗi.

> LLM 输出 là phân bố xác suất của một token tiếp theo, đây là phạm vi sản xuất của nó. Nếu bạn hỏi một mô hình trò chuyện "Banhkarao hiện tại thời tiết như thế nào", nó có thể viết một câu có vẻ hợp lý, nhưng nó không thể sử dụng API thời tiết.

Đó là mục đích của giao diện công cụ. Chương trình chủ  thời gian chạy của đại lý của bạn, Claude Desktop, ChatGPT, Cursor, hoặc kịch bản tùy chỉnh  quảng cáo danh sách các công cụ có thể gọi cho mô hình. Mô hình, khi nó quyết định một hành động là cần thiết, phát ra một tải trọng hữu ích được cấu trúc đặt tên cho một công cụ và các lập luận của nó. Người chủ phân tích tải trọng, chạy công cụ thực sự, và cung cấp kết quả trở lại. Loop tiếp tục cho đến khi mô hình quyết định không cần thêm cuộc gọi nữa.

> 弥合这个沟通正是工具接口的目的──主程序你的代理运行时、Claude Desktop、ChatGPT、Cursor 或自定义脚本向模型通告一个可调用工具列表──当模型判断需要执行某动作时,它会发出一个结构化负载,指标工具名称和参数──主程序解析该负载,真正运行工具,然后将结果反回去──循环持续持续,直到模型判断不再需要调用──

Phiên bản đầu tiên của hợp đồng này được xuất bản vào tháng 6 năm 2023 như là tham số "các chức năng" của OpenAI.`tool_use`Các khối trong Claude 2.1.`functionDeclarations`Một vài tháng sau. Mỗi nhà cung cấp hiện đang tiết lộ cùng một hình dạng: một danh sách công cụ kiểu JSON-Schema, một công cụ tải trọng trả phí JSON. Mô hình giao thức ngữ cảnh (Triều 11 năm 2024) đã tổng quát hợp đồng vì vậy một danh sách công cụ phục vụ mỗi mô hình. A2A (Triều 4, 2026, v1.0) đã layered nguyên thủy tương tự cho đại lý-to-agent đại diện.

> Phiên bản đầu tiên của hiệp ước này được phát hành vào tháng 6 năm 2023 với các "các chức năng" của OpenAI dưới dạng tham số.`tool_use`Một vài tháng sau, Gemini đã thêm vào.`functionDeclarations` Hiện tại, mỗi nhà cung cấp đều tiết lộ hình dạng giống nhau: nhập JSON Schema  danh sách các loại công cụ, xuất JSON  tải về các công cụ调用。 Mô hình Context Protocol(2024 年 11 月) sẽ được phổ biến, để một sổ đăng ký công cụ có thể phục vụ tất cả các mô hình。A2A(2026 年 4 月, v1.0) sẽ được sử dụng cùng một nguyên bản cho các nhiệm vụ của đại lý 间委托。

Các vòng lặp bốn bước là sự bất biến bên dưới tất cả những điều này.

> Chuyện vòng bốn bước là không thay đổi dưới tất cả các kỹ thuật này. Phần còn lại của giai đoạn 13 là sự mở rộng của chu kỳ này.

> **【中文解读】**四步循环(describe→decide→execute→observe) là tất cả các công cụ调用协议的不变量──无论是 OpenAI's function calling、Anthropic's tool_use、MCP's tools/call 还是A2A's task parts,本质上都是这个循环的不同编码方式──

## Khái niệm cốt lõi

### Bước 1: mô tả

> **【中文解读】**工具声明是整个循环的起点──每个工具需要三个字段:名称(机器可读标识符) 描述(自然语言使用说明) 输入模式(JSON Schema 参数描述)── một mô tả công cụ tốt trực tiếp quyết định mô hình có thể chọn đúng và sử dụng công cụ──

Người chủ tuyên bố mỗi công cụ với ba trường.

> 宿主为每个工具声明三个字段──

- **Name.**Một thẻ nhận dạng ổn định, có thể đọc được bằng máy.`get_weather`Không phải "cái thời tiết".
  Trung ngữ翻译:**名称。**Một bộ chỉ định được đọc trên máy tính.`get_weather`, thay vì "天气那玩意"
- **Description.**Một đoạn ngắn ngôn ngữ tự nhiên. "Điều sử dụng khi người dùng hỏi về điều kiện hiện tại cho một thành phố cụ thể.
  Trung ngữ翻译:**描述。**Một đoạn ngắn về ngôn ngữ tự nhiên: "Khi người dùng hỏi tình trạng hiện tại của một thành phố, đừng sử dụng dữ liệu lịch sử".
- **Input schema.**Một đối tượng JSON Schema (mở 2020-12) mô tả các lập luận của công cụ.
  Trung ngữ翻译:**输入模式。**Một JSON Schema đối tượng (2020-12 草案), mô tả các yếu tố của công cụ.

>  **【类比】**工具接口像餐厅点餐:菜单上每道菜=工具,菜名=tool name,菜单上的描述=描述("招牌牛肉面,清真可选,配油"),点餐时填的选项(度、加蛋)=JSON Schema 参数──服务员(模型)看菜单决定推哪道菜,把订单(tool_call)递给厨房(执行器),厨房做好端上来(tool_result),服务员转交给顾客──模型从厨房不进,只递单子──

Mô hình nhận được danh sách. Các nhà cung cấp hiện đại liên tục các tuyên bố này vào hệ thống nhắc sử dụng một mẫu cụ thể cho nhà cung cấp, vì vậy bạn như người gọi chỉ xử lý các hình thức có cấu trúc.

> 模型接收这个列表――Modern provider sử dụng mô hình cụ thể sẽ trình tự các tuyên bố này thành các gợi ý hệ thống, vì vậy như một người dùng, bạn chỉ cần xử lý hình thức cấu trúc――

### Bước 2: quyết định

> **【中文解读】**模型面对用户消息和可用工具列表时, có ba lựa chọn:直接文本回答、调用一个或多个工具、或拒绝──工具调用负载包含三个字段:call id(用于关联结果) 工具名 (工具名) ]] 参数 (JSON 参数对象) ]]并行调用时 id 尤为重要,因为结果可能乱序返回──

> **【拓展：Parallel Tool Calls 的性能优势】**OpenAI và Gemini 默认开启并行工具调用`parallel_tool_calls: true`), cho phép mô hình phát hành nhiều điều kiện độc lập trong một lần suy luận. thực nghiệm cho thấy, đối với nhu cầu truy vấn nhiều nguồn dữ liệu như kiểm tra thời tiết và cổ phiếu), việc truy cập có thể sẽ giảm từ 40 đến 60% trong thời gian.

Với thông điệp của người dùng và các công cụ có sẵn, mô hình chọn một trong ba hành vi.

> 给定用户消息和可用工具,模型选择三种行为之一──

1. **Answer directly**Không có lời gọi công cụ.
   Trung ngữ翻译:**直接以文本回答。**Không dùng công cụ.
2. **Call one or more tools.**Phát ra các đối tượng gọi có cấu trúc.`parallel_tool_calls: true`(tầm định trên OpenAI và Gemini, chọn vào Anthropic) mô hình có thể phát ra nhiều cuộc gọi trong một lượt.
   Trung ngữ翻译:**调用一个或多个工具。**发发发结构化调用对象──在 `parallel_tool_calls: true`(OpenAI và Gemini 默认开启,Anthropic 需要选择开启)
3. **Refuse.**Các kết quả kết cấu trong chế độ nghiêm ngặt có thể tạo ra một kiểu `refusal`chặn thay vì gọi điện.
   Trung ngữ翻译:**拒绝。**nghệ thống cấu trúc của mô hình xuất có thể tạo ra một loại hóa `refusal`块而非调用──

Một công cụ gọi tải hữu ích có ba trường ổn định: một cuộc gọi `id`, một công cụ `name`, và một JSON `arguments`ID tồn tại để máy chủ có thể liên quan kết quả sau đó với cuộc gọi cụ thể, điều quan trọng khi các cuộc gọi song song trở lại không phù hợp.

> 工具调用负载有三个稳定字段:调用 `id`、 dụng cụ `name`和 JSON `arguments`Sự tồn tại của đối tượng là để chủ nhà có thể kết nối kết quả tiếp theo với một số điều chỉnh cụ thể, điều này rất quan trọng khi điều chỉnh các thứ tự trở lại.

### Bước 3: Thực hiện

> **【中文解读】**执行阶段, host program nhận được yêu cầu调用, trước tiên sử dụng JSON Schema 验证参数合法性, sau đó vận hành trình thực hiện.

Người chủ nhận được cuộc gọi, xác nhận các lập luận chống lại sơ đồ được tuyên bố và chạy trình thực hiện. Các lập luận không hợp lệ có nghĩa là mô hình ảo giác một trường hoặc sử dụng loại sai  một chế độ thất bại rất phổ biến trên các mô hình yếu. Các máy chủ sản xuất làm một trong ba điều trên các lập luận không hợp lệ: thất bại nhanh chóng và làm bề mặt lỗi cho mô hình, sửa chữa JSON bằng một trình phân tích bị hạn chế hoặc thử lại mô hình với lỗi xác thực được bao gồm trong lời nhắc.

> Ứng dụng nhận được từ máy chủ, theo các tham số xác minh mô hình của tuyên bố, sau đó chạy bộ điều hành. tham số vô hiệu nghĩa là mô hình hình ảo giác một đoạn hoặc sử dụng loại sai lầm. Đây là một mô hình thất bại rất phổ biến trên mô hình yếu.

> ️ **【易错点】**场景:跳过 schema 验证直接执行 / 后果:弱模型(Haiku、GPT-4o-mini) 会幻觉字段(如 `get_weather({ cityy: "Tokyo" })`拼错键), trình thực trình  KeyError 崩 要拿到 None 走错分支 / 修复: 在 trình thực trình trước cần thêm sơ đồ 验证, thất bại 时把错误以`tool_result`形式 trở lại cho mô hình để nó thử lại, thay vì bỏ qua bất thường cho chủ nhà.

Bản thân trình thực trình là mã thông thường. Python, TypeScript, lệnh shell, truy vấn cơ sở dữ liệu. Nó tạo ra kết quả, thường là một chuỗi nhưng có thể là bất kỳ giá trị JSON hoặc khối nội dung được cấu trúc (tin nhắn văn bản, hình ảnh hoặc tham chiếu tài nguyên trong MCP). Kết quả phải được tựa.

> 执行器 tự nó là mã thông thường.  Python, TypeScript, shell, lệnh, truy vấn cơ sở dữ liệu.  Nó tạo ra một kết quả, thường là một chuỗi, nhưng cũng có thể là bất kỳ giá trị JSON hoặc khối nội dung cấu trúc nào trong MCP.

### Bước 4: quan sát

> **【中文解读】**观察阶段将工具结果附加到对话历史(以 `tool`角色消息形式,携带匹配的 id), sau đó tái调用模型──模型现在有工具输出上下文,可以生成最终答案或请求更多调用──循环持续持续直到模型停止发出调用或主机达到安全上限──

Người chủ kết nối kết quả công cụ vào cuộc trò chuyện (như một `tool`thông điệp vai trò với sự phù hợp `id`(văn khoái) và triệu tập lại mô hình. mô hình bây giờ có công cụ đầu ra trong bối cảnh và có thể tạo ra một câu trả lời cuối cùng hoặc yêu cầu nhiều cuộc gọi hơn.

> Chủ nhà sẽ kết quả công cụ được thêm vào cuộc trò chuyện để có sự phù hợp`id`của `tool`角色消息形式)并调用模型.模型现在在上下文中包含工具输出,可以生成最终答案或请求更多调用.

### Sự tin tưởng chia rẽ

> **【中文解读】**工具分为两类:纯工具(只读、无副作用,如get_weather) 和后果性工具(改变状态、消耗资金、触及用户数据,如发送_email) 后果性工具必须设置门控机制――Meta 2026 年的"二选一规则"要求单次交互最多只能组合两项:不可信输入、敏感数据、后果性动作――

> **【拓展：Agent 安全中的 Tool Poisoning】**Sự xuất hiện của Công cụ Bị độc  tấn công cho thấy, các công cụ ác ý có thể thông qua mô hình lừa đảo mô hình được xây dựng kỹ lưỡng để thực hiện các hoạt động nguy hiểm. Ví dụ: được nhúng trong mô tả công cụ "Khi người dùng yêu cầu xóa ngay lập tức thực hiện" trong lệnh ẩn. Đây cũng là tầng an toàn của MCP.

Các công cụ có hai hương vị quan trọng cho an toàn.

> 工具从安全角度分为两类:

- **Pure.**Chỉ đọc, quyết định, không có tác dụng phụ. `get_weather`- `search_docs`- `get_current_time`- Được gọi theo cách suy đoán.
  Trung ngữ翻译:**纯工具。**Chỉ đọc, chắc chắn, không có tác dụng phụ.`get_weather``search_docs``get_current_time` có thể được sử dụng an toàn.
- **Consequential.**Nhập trạng thái, chi tiền, chạm vào dữ liệu người dùng. `send_email`- `delete_file`- `execute_trade`- Phải có cửa.
  Trung ngữ翻译:**后果性工具。** sửa đổi trạng thái, tiêu thụ tiền, chạm đến dữ liệu người dùng.`send_email``delete_file``execute_trade` phải đặt cửa kiểm soát

Meta's 2026 "Rule of Two" cho bảo mật đại lý nói một lượt có thể kết hợp tối đa hai: đầu vào không đáng tin cậy, dữ liệu nhạy cảm, hành động hậu quả. giao diện công cụ là nơi bạn thực thi quy tắc đó bằng cách từ chối cuộc gọi, yêu cầu xác nhận người dùng hoặc leo thang phạm vi. Xem giai đoạn 13 · 15 cho toàn bộ chương bảo mật và giai đoạn 14 · 09 cho chính sách quyền cấp đại lý.

> Meta 2026 năm "Định luật thứ hai" của Agen 安全 cho thấy, giao tiếp đơn giản có thể được kết hợp với hai trong ba mục sau đây: không thể tin vào, dữ liệu nhạy cảm, động tác hậu quả.

### Ở đâu vòng lặp sống

| Context | Who describes | Who decides | Who executes |
|---------|---------------|-------------|--------------|
| Single-turn function calling (OpenAI/Anthropic/Gemini) | App developer | LLM | App developer |
| MCP | MCP server | LLM via MCP client | MCP server |
| A2A | Agent Card publisher | Calling agent | Called agent |
| Web browser (function-calling agent) | Browser extension / WebMCP | LLM | Browser runtime |

Ở khắp mọi nơi, bốn bước tương tự.

> Bất kể ở đâu, đều giống nhau bốn bước.

> 🤔 **【困惑】**Q: 既然都是同一四步循环,为什么还需要 MCP、A2A 这么多协议? A: 循环不变是"逻辑步骤",变是"通信边界"――原生函数调用在同一进程内; MCP 把描述 步骤跨进程化(让一个服务器 服务多个主机); A2A 把执行 步骤跨网络化(让代理调 agent) ――本质是把循环的某步从"进程内"到搬迁"网络边界,需要标准协议来描述谁负责什么.

> **【拓展：MCP 统一工具协议】**Mô hình Context Protocol (MCP,2024 tháng 11 tháng 11 tháng 11 tháng 11 tháng 11 năm) sẽ được chuẩn hóa giao diện công cụ, giúp một sổ đăng ký công cụ có thể phục vụ tất cả các mô hình. MCP đã được Anthropic, OpenAI, Google và các nhà sản xuất chính khác chấp nhận. Năm 2026 đã trở thành tiêu chuẩn giao thức công cụ thực tế, tương tự như USB-C đối với các bộ sạc.

### Tại sao không chỉ yêu cầu mô hình phát ra JSON?

> **【中文解读】**纯提示方式让模型输出 JSON的失败率在5-15%,小模型更高──失败模式包括:缺少大括号、尾随号、幻觉字段、类型错误──原生函数调用通过端到端训练、独立协议槽位和约束解码三层保障, sẽ nâng cấp hiệu quả JSON 率 lên 98-99%──

"Hãy yêu cầu mô hình trả lời trong JSON" là mô hình gọi trước chức năng. Nó thất bại từ 5 đến 15% thời gian trên các mô hình biên giới và nhiều hơn nữa trên các mô hình nhỏ hơn. Các chế độ thất bại bao gồm các dây đeo bị thiếu, dấu ngoặc sau, các trường ảo giác và các loại sai. Sau đó bạn cần một thẻ sửa chữa JSON, thử lại hoặc một bộ giải mã bị hạn chế.

> "Let the model use JSON 回复" là một mô hình trước khi các hàm được điều chỉnh xuất hiện. Trong mô hình phía trước, tỷ lệ thất bại là khoảng 5-15%, trong mô hình nhỏ, tỷ lệ thất bại cao hơn.

Đổi tiếng gọi chức năng bản địa là tốt hơn vì ba lý do. Đầu tiên, nhà cung cấp đào tạo mô hình từ đầu đến cuối theo hình dạng gọi chính xác, do đó tỷ lệ JSON hợp lệ tăng lên 98 đến 99% trên chế độ nghiêm ngặt. Thứ hai, tải trọng hữu ích của cuộc gọi nằm trong khe giao thức riêng của nó, không nằm trong văn bản tự do  do đó một cuộc gọi công cụ không bao giờ rò rỉ vào câu trả lời hiển thị của người dùng. Thứ ba, các nhà cung cấp thực thi tuân thủ các kế hoạch với việc giải mã hạn chế (chế độ nghiêm ngặt của OpenAI, Anthropic `tool_use`, của Gemini `responseSchema`(c) Tạo ra được đảm bảo để xác nhận.

> Các công cụ được sử dụng trong các phiên bản khác nhau, có thể được sử dụng trong các phiên bản khác nhau, nhưng không phải là một phần của các phiên bản khác nhau.`tool_use`、Gemini của `responseSchema`(c) Đơn vị thực thi pháp luật.

Giai đoạn 13 · 02 đi cùng ba API nhà cung cấp. Giai đoạn 13 · 04 đi sâu vào các kết quả có cấu trúc.

> Giai đoạn 13 · 02 并排讲解三个供应商的API──Giai đoạn 13 · 04 深入讲解结构化输出──

### Máy cắt mạch

> **【中文解读】**断器 là cơ chế thiết yếu của môi trường sản xuất. Chuyển trong mô hình dừng phát hành và sử dụng hoặc chủ nhà đạt đến thời gian kết thúc tối đa.

> **【拓展：Agent 成本失控案例】**Nhiều trường hợp công khai năm 2025 cho thấy, thiếu hụt của máy phân chia sẽ tạo ra một khoản phí API lớn khi gặp một vòng chết mô hình. Ví dụ: một người dùng báo cáo rằng mình đã tạo ra một số phí API hơn 2.000 USD trong một đêm khi sửa lỗi.

Loop kết thúc khi mô hình ngừng phát ra cuộc gọi hoặc máy chủ đạt con số lượt tối đa. Các máy chủ sản xuất đặt điều này ở khoảng 5 đến 20 lượt. Ngoài ra, bạn gần như chắc chắn đang trong một vòng lặp mà mô hình không thể thoát ra. Claude Code mặc định là 20; OpenAI Assistants là 10; chế độ đại lý của Cursor là 25.

> Chuyện này có thể xảy ra trong vòng lặp mà mô hình không thể thoát khỏi. Claude Code:默认 20 vòng;OpenAI Assistants 10 vòng;Cursor's agent:

Các vòng lặp không giới hạn thay thế xuất hiện mỗi sáu tháng như "nhà nhân chi 400 đô la cho các cuộc gọi API qua đêm" sau khi chết.

> Một lựa chọn khác  vòng lặp không giới hạn  mỗi sáu tháng sẽ xuất hiện "truyện viên một đêm đã chi $400 API 调用"

Giai đoạn 14 · 12 bao gồm việc phục hồi lỗi và tự chữa trị sâu sắc; Giai đoạn 17 bao gồm giới hạn tốc độ sản xuất.

> Giai đoạn 14 · 12 sâu vào giải thích về sự phục hồi sai lầm và tự sửa chữa; Giai đoạn 17  giải thích về giới hạn tốc độ sản xuất môi trường.

### Từ đây, giai đoạn 13 sẽ đi đến

- Bài học 02 đến 05 làm sáng tỏ bề mặt gọi công cụ cấp nhà cung cấp.
  Trung ngữ翻译:Lớp 02 đến 05 完善提供商级别的工具调用接口──
- Bài học 06 đến 14 tổng hợp vòng lặp thành MCP.
  Bài học 06 đến 14 sẽ được chuyển thành MCP.
- Bài học 15 đến 18 bảo vệ vòng lặp chống lại các máy chủ thù địch, người dùng đối kháng và các bề mặt auth từ xa không xác nhận.
  Bài học 15 đến 18  phòng chống các máy chủ ác ý  chống lại người dùng và không được chứng nhận từ xa
- Bài học 19 đến 22 mở rộng mô hình đến sự hợp tác giữa các đại lý, khả năng quan sát, định tuyến và đóng gói.
  Bài học 19 đến 22 sẽ mở rộng mô hình đến đại lý 间协作、可观测性、路由和打包──
- Bài học 23 tạo ra một hệ sinh thái hoàn chỉnh sử dụng mọi thứ nguyên thủy.
  Trung ngữ翻译:Lớp 23 使用每个原语发布完整的生态系统──

Mỗi bài học còn lại là một sự phức tạp của vòng lặp bốn bước này. Hãy nhớ rằng như là không biến đổi.

> Mỗi bài học còn lại là sự mở rộng của vòng vòng bốn bước này. Xin hãy ghi nhớ nó như không thay đổi.

```figure
tp-tool-loop
```

## Hãy sử dụng nó để thực hiện

> **【中文解读】**Ví dụ mã code sử dụng giả "động cơ quyết định" mô hình, đưa phần còn lại của vòng lặp (验证,执行,观察) thành thực hiện. Đây là một cách tốt để học giao thức: trước tiên kiểm soát dòng chạy, rồi dần dần thay thế thành thực cấu trúc.

`code/main.py`chạy vòng lặp bốn bước mà không có LLM. Một chức năng "những người quyết định" giả mô phỏng mô hình bằng cách so sánh mô hình trên thông điệp người dùng; người thực thi, xác nhận sơ đồ và vòng kiểm tra bước thực.

> `code/main.py`Trong trường hợp không có LLM, chạy vòng bốn bước. Một hàm "những người quyết định" giả bằng cách thực hiện mô hình phù hợp để mô hình hóa thông điệp của người dùng; các dây chuyền của các bước kiểm chứng và quan sát của các nhà thực thi là thực. Nó có thể xem toàn bộ quy trình yêu cầu / phản ứng và trạng thái trung gian có thể in, sau đó trong khóa học tiếp theo sẽ thay thế các nhà quyết định giả thành bất kỳ nhà cung cấp thực sự nào.

Những gì cần xem:

> 需要关注的点:

- Các tool registry có ba trường cho mỗi tool: tên, mô tả, schema và một trình tham khảo thực thi.
  Trung ngữ翻译:工具注册表为每个工具保存三个字段:名称、描述、模式和一个执行器引用。
- Các xác thực viên là một bộ phụ quy trình JSON tối thiểu (loại, yêu cầu, enum, min/max) được viết bằng stdlib.
  Trung文翻译:验证器是一个最小的 JSON Schema 子集 ((类型、必填、枚举、最小/最大值), chỉ sử dụng các tiêu chuẩn 编写.
- Các đại lý sản xuất cần một bộ cắt mạch chính xác như thế này.
  Trung ngữ翻译:循环将代次数限制在5次――生产环境的代理 正需要这种断断器――

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-tool-interface-reviewer.md`. Với một bản thảo định nghĩa công cụ (tên + mô tả + sơ đồ + phác thảo trình thực hiện), kỹ năng kiểm tra nó cho phù hợp vòng lặp: tên là máy ổn định, mô tả là một sử dụng ngắn gọn hoàn chỉnh, liệu sơ đồ sử dụng JSON Schema 2020-12 đúng không, và là phân loại tinh khiết đối với hậu quả rõ ràng.

> 本课产 出 `outputs/skill-tool-interface-reviewer.md` Định định một công cụ định nghĩa bản thảo (名称 + 描述 + 模式 + 执行器概述), kỹ năng này 审计循环适应性:名称是否机器稳定;描述是否是完整的使用说明;模式是否正确使用 JSON Schema 2020-12;纯工具与后果性工具的分类是否明确;

## Tập luyện bài tập

1. Thêm một công cụ thứ tư vào `code/main.py`gọi `get_stock_price(ticker)`. Tác lại mô tả của nó như " Sử dụng khi người dùng yêu cầu giá cổ phiếu hiện tại bằng ticker. Không sử dụng cho giá lịch sử hoặc bản tóm tắt thị trường. " Đánh vào vòng và xác nhận các truy vấn đường lối quyết định giả sử đề cập ticker cho công cụ mới.
   Trung ngữ翻译:在 `code/main.py`Trung thêm thứ tư `get_stock_price(ticker)` sẽ được mô tả như "Khi người dùng thông qua mã hóa hỏi giá cổ phiếu hiện tại sử dụng. Không sử dụng giá lịch sử hoặc bản tóm tắt thị trường".

2. Tháo xác minh schema.`arguments`object bị thiếu một trường yêu cầu, và xác nhận host từ chối nó trước khi thực hiện. Sau đó thực hiện một cuộc gọi với một trường không rõ ràng thêm. quyết định: host phải từ chối hoặc bỏ qua? biện minh cho sự lựa chọn của bạn với một lập luận an toàn.
   Trung文翻译:破坏模式验证器──传入一个 `arguments`Đối với các mục thiếu hụt cần phải điền vào các mục tiêu, xác nhận chủ nhà đã từ chối trước khi thực hiện nó.

3. Đánh phân loại mỗi công cụ trong vòng đeo là thuần túy hoặc hậu quả.`consequential: true`cờ vào các mục đăng ký cần nó, và thay đổi vòng lặp để in một dòng "sẽ xác nhận với người dùng" bất cứ khi nào một công cụ liên quan được chọn. Đây là hình dạng của cổng xác nhận mà mọi máy chủ sản xuất cần.
   Trung ngữ翻译:将线束中的每工具分类为纯工具或后果性工具──为需要注册表条目添加 `consequential: true`标志,并修改循环, mỗi khi chọn các công cụ hậu quả, in "will with user confirm" của đường. Đây là hình thức của cửa xác nhận mà mỗi nhà sản xuất môi trường cần.

4. Hình vẽ vòng lặp bốn bước trên giấy với bảng cột nhà cung cấp ở trên được điền vào cho khách hàng yêu thích của bạn (Claude Desktop, Cursor, ChatGPT hoặc một ngăn xếp tùy chỉnh).
   Trung ngữ翻译: 在纸上绘制四步循环,填入您最喜欢的客户端 (CLODE Desktop、CURSOR、ChatGPT 或自定义技术) 供应商列表──与Phase 13 · 06 中的 MCP 特定变体交叉参考──

5. Đọc hướng dẫn gọi hàm của OpenAI từ đầu xuống dưới. Xác định một trường nằm trong yêu cầu nhưng không nằm trong vòng vòng bốn bước như được trình bày ở đây. Giải thích điều gì nó thêm và tại sao nó thuận tiện hơn là cần thiết.
   Trung ngữ翻译:从头到尾阅读 OpenAI's function调用指南―― tìm ra một đoạn trong yêu cầu nhưng không có trong vòng vòng bốn bước trong bài viết này Introduction―― giải thích nó đã thêm gì và tại sao nó là thuận tiện thay vì không cần thiết――

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Tool | "A thing the model can call" | A triple of name + JSON-Schema-typed input + executor function | 工具 |
| Function calling | "Native tool use" | Provider-level API support for emitting structured tool calls instead of prose | 函数调用 |
| Tool call | "The model's request to act" | A JSON payload with `id`, `name`, `arguments` emitted by the model | 工具调用 |
| Tool result | "What the tool returned" | The executor's output, wrapped in a `tool` role message with matching id | 工具结果 |
| Parallel tool calls | "Many calls at once" | Multiple call objects in one model turn, independent and orderable by id | 并行工具调用 |
| Strict mode | "Guaranteed JSON" | Constrained decoding that forces the model's output to validate against the declared schema | 严格模式 |
| Pure tool | "Read-only tool" | No side effects; safe to re-run | 纯工具 |
| Consequential tool | "Action tool" | Mutates external state; requires gate, audit, or user confirmation | 后果性工具 |
| Four-step loop | "The tool-call cycle" | describe → decide → execute → observe | 四步循环 |
| Host | "Agent runtime" | The program that holds the tool registry, calls the model, and runs the executor | 宿主 |

## Xem thêm 延伸阅读

- [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) Khán giả tham khảo về các thông báo công cụ kiểu OpenAI và hình thức gọi
  Trung ngữ翻译:OpenAI 风格工具声明和调用形式权威参考
- [Anthropic — Tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) Claude `tool_use`- `tool_result`định dạng khối
  Trung ngữ翻译:Claude 的 `tool_use`- `tool_result`块格式
- [Google — Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling) `functionDeclarations`và ngữ nghĩa gọi song song trong Gemini
  Trung ngữ翻译:Gemini 中的 `functionDeclarations`和并行调用语义
- [Model Context Protocol — Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) sự phổ biến hiện tại của giao diện công cụ không có nhà nước, cung cấp-những người không biết về nhà cung cấp
  Trung文翻译:MCP 2026-07-28 规范 当前无状态、供应商无关的工具接口泛化
- [JSON Schema — 2020-12 release notes](https://json-schema.org/draft/2020-12/release-notes) phương ngữ schema mọi công cụ hiện đại API nói
  Trung ngữ翻译:每个现代工具 API 使用的模式方言
