# Công cụ song song gọi và phát trực tuyến với công cụ

> Ba lần tìm kiếm thời tiết độc lập được phân phối theo thứ tự là ba lần đi lại. Hãy chạy chúng song song và tổng thời gian sụp đổ đến cuộc gọi đơn giản chậm nhất. Mỗi nhà cung cấp biên giới bây giờ phát ra nhiều cuộc gọi công cụ trong một lượt.

> **【中文解读】**Ba liên kết liên tục điều tra thời tiết độc lập cần phải được thực hiện ba lần quay trở lại. Sau khi các liên kết được thực hiện, tổng thời gian giảm xuống thành thời gian điều khiển đơn giản chậm nhất. Tất cả các nhà cung cấp mô hình tiền tuyến hiện đang hỗ trợ phát hành nhiều công cụ điều khiển trong một vòng.

> **【拓展：并行调用→Agent 效率优化】**Việc sử dụng công cụ thông minh là một cải tiến quan trọng về hiệu quả của AI Agent. Khi Agent cần cùng lúc truy vấn nhiều nguồn dữ liệu (như nhiều thành phố thời tiết, giá cổ phiếu), việc sử dụng thông minh có thể chậm giảm 60-70%.`disable_parallel_tool_use`参数 và OpenAI của `parallel_tool_calls`参数都控制这一行为――

>  **【前置】**学本节前请先掌握:(1) Bước 13·02(Fungsi gọi Deep Dive)掌握三 API 形态差异,本节是它的并发延伸;(2) Python `concurrent.futures`Hoặc`asyncio.gather`基础,本节会用线程池并行执行器;(3) JSON 拼接技巧流式 `arguments`Là phần của đến, phải tích lũy lại sau.`json.loads`, không thể giải quyết được.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, thread pool + streaming harness) | **语言:** Python（标准库，线程池 + 流式线束）
**Prerequisites:** Phase 13 · 02 (function calling deep dive) | **前置知识:** Phase 13 · 02（函数调用深入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Hãy giải thích lý do tại sao `parallel_tool_calls: true`tồn tại và khi nào để vô hiệu hóa nó.
  Trung ngữ翻译: giải thích tại sao tồn tại`parallel_tool_calls: true`Và khi nào không sử dụng nó.
- Kết hợp các đoạn tranh luận được phát trực tuyến với ID gọi công cụ phải trong thời gian phát fan song song.
  Trong thời gian này, các khối được chuyển sang các khối chính xác.
- Lắp ráp lại phần `arguments`chuỗi thành JSON hoàn chỉnh mà không cần phân tích sớm.
  Trung ngữ翻译:将部分 `arguments`字符串重组为完整JSON,而不提前解析──
- Thực hiện một điểm chuẩn thời tiết ba thành phố cho thấy độ trễ liên tục so với song song.
  Trung ngữ翻译:运行三城市天气基准测试, trình bày 串行与并行延迟的对比──

## Vấn đề  vấn đề giới thiệu

Không có cuộc gọi song song, một đại lý trả lời "thời tiết ở Bengaluru, Tokyo và Zurich" làm như sau:

> Không có thông tin, một đại lý trả lời "Bengaluru,东京 và Suizing thời tiết như thế nào" sẽ làm như thế này:

```
user -> LLM
LLM -> call get_weather(Bengaluru)
host -> run executor, reply with result
LLM -> call get_weather(Tokyo)
host -> run executor, reply with result
LLM -> call get_weather(Zurich)
host -> run executor, reply with result
LLM -> final text answer
```

Ba chuyến đi về LLM, mỗi chuyến đi cũng trả cho thời gian trễ của người thực thi.

> Ba lần LLM 往返, mỗi lần trả lại phải trả cho thời gian trễ.

> **【中文解读】**Không có thông tin về thời gian, Trưởng lý trả lời "Bengaluru、东京和苏黎世的天气如何" cần 3 lần LLM 往返, mỗi lần trả lại phải trả cho thời gian trễ, tổng thời gian mất khoảng 4 lần thời gian lý tưởng.

Với các cuộc gọi song song:

> Có hành vi:

```
user -> LLM
LLM -> call get_weather(Bengaluru); call get_weather(Tokyo); call get_weather(Zurich)
host -> run all three executors concurrently, reply with three results
LLM -> final text answer
```

Một chuyến đi vòng về LLM. Thời gian thực hiện là tối đa của ba, không phải tổng số. Các tiêu chuẩn sản xuất trên OpenAI, Anthropic và Gemini cho thấy giảm 60 đến 70% đồng hồ tường trên tải trọng công việc máy bay.

> Một lần LLM 往返──执行器时间是三个最大值,而不是总和──OpenAI、Anthropic 和 Gemini 上的生产基准测试显示, 扇出工作负载的挂钟时间减少60-70%.──

>  **【类比】**Và đường调用 như thanh toán siêu thị. Và đường调用 = 你一个人排队买完肉,再排队买菜,再排队买酒,总时间=三个队时间相加. Và đường调用 = 你给三个朋友打电话"你们各排队,同时结账",总时间=慢 ترین队时间.

Giá là sự phức tạp tương quan. Khi ba cuộc gọi hoàn thành không được sắp xếp, kết quả của bạn phải mang theo sự phù hợp `tool_call_id`Khi kết quả được phát, bạn phải tập hợp các mảnh đối số một phần thành JSON hoàn chỉnh trước khi thực hiện. Gemini 3 thêm ID độc đáo một phần để giải quyết một vấn đề trong thế giới thực nơi hai cuộc gọi song song với cùng một công cụ không thể phân biệt được.

> 代价是关联复杂性. Khi 3调用乱序完成, kết quả phải mang theo sự phù hợp.`tool_call_id`, để mô hình đối diện với các trường hợp quy trình, phải được tập hợp thành một phần phần tử JSON hoàn chỉnh trước khi thực hiện.

> **【中文解读】**Và các quy trình điều chỉnh giá cả là liên quan đến sự phức tạp. Khi ba quy trình điều chỉnh được hoàn thành, kết quả phải mang theo các kết quả phù hợp.`tool_call_id`, để mô hình đối diện với các trường hợp, phải được tập hợp phần các phần tử thành một phần JSON hoàn chỉnh sau khi thực hiện.

## Khái niệm cốt lõi

### Cho phép song song

> **【拓展：何时禁用并行调用】**Các trường hợp điển hình của việc sử dụng và điều chỉnh bao gồm: 1) 工具有顺序依赖 (如先创建文件再写入); 2) một sản phẩm được sử dụng là một sản phẩm khác được sử dụng (如先查查用户ID再查订单); 3) Down游 API có giới hạn tốc độ,10路扇遇导致 429 错误. Trong sản xuất thực tế, khoảng 30% các công cụ sử dụng cần phải thực hiện liên tục.

- **OpenAI.** `parallel_tool_calls: true`mặc định.`false`để buộc hàng loạt.
  Trung ngữ翻译:**OpenAI。** `parallel_tool_calls: true`默认开启──设为 `false`强制串行.
- **Anthropic.**Phía song song `disable_parallel_tool_use: false`(đặc định trên Claude 3.5 trở lên).`true`cho serial.
  Trung ngữ翻译:**Anthropic。** Thông qua `disable_parallel_tool_use: false`并行(Claude 3.5 及以上默认)`true`强制串行.
- **Gemini.**Luôn ngang ngang;`tool_config.function_calling_config.mode = "AUTO"`để người mẫu quyết định.
  Trung ngữ翻译:**Gemini。**始终支持并行;`tool_config.function_calling_config.mode = "AUTO"`Hãy để mô hình tự quyết định.

Thiết lập song song khi các công cụ có phụ thuộc sắp xếp (`create_file`Vậy thì`write_file`), khi đầu ra của một cuộc gọi thông báo đầu vào của một cuộc gọi khác, hoặc khi giới hạn tốc độ không thể xử lý máy hâm mộ.

> 当工具有顺序依赖`create_file`Tới đây`write_file`(■ một đầu ra được điều chỉnh ảnh hưởng đến đầu vào khác hoặc tốc độ giới hạn không thể xử lý máy bay, tắt và đi.

> **【中文解读】**当工具有顺序依赖`create_file`Tới đây`write_file`(■ khi một thiết bị điều chỉnh xuất phát ảnh hưởng đến các thiết bị nhập khác hoặc giới hạn tốc độ không thể xử lý máy bay ra, nên tắt và đi.

> 🤔 **【困惑】**Q: 模型怎么知道哪些调调可以并行?A: 模型不知道,它只决定"现在要调这些工具";并发执行是主机的事――模型发发 `[get_weather(Tokyo), get_weather(Zurich)]`Khi, chủ nhà tự quyết định hai người không phụ thuộc có thể phát triển; nếu mô hình phát triển`[create_file, write_file]`, chủ nhà phải串行 (khả năng thường là cấm并行+ trình tự thực hiện, hoặc phụ thuộc vào kiểm tra trong thiết bị thực hiện) ⋅ do đó, "có phải并行" là chủ nhà định vị+ mô hình quyết định chung quyết định của。

### Tương quan ID

Mỗi cuộc gọi mà mô hình phát ra đều có một`id`. Mỗi kết quả mà máy chủ trả lại phải có cùng một ID. Nếu không có nó, kết quả là mơ hồ.

> Mỗi mô hình phát hành đều có một .`id`◊ Mỗi kết quả của chủ nhà trả lại phải chứa cùng một ID. Không có một kết quả này, kết quả là模糊.

- **OpenAI.** `tool_call_id`trên mỗi thông điệp vai trò công cụ.
  Trung ngữ翻译:**OpenAI。**Mỗi công cụ 角色消息 trên `tool_call_id`
- **Anthropic.** `tool_use_id`trên mỗi `tool_result`- Quận.
  Trung ngữ翻译:**Anthropic。**Mỗi người`tool_result`块 trên `tool_use_id`
- **Gemini.** `id`trên mỗi `functionResponse`(Them 3 trở lên; Gemini 2 phù hợp theo tên mà phá vỡ cho cùng tên gọi cuộc gọi song song).
  Trung ngữ翻译:**Gemini。**Mỗi người`functionResponse` 上 的`id`(Thiên sinh 3 及以上;Thiên sinh 2 按名称匹配,同名并行调用时会出错)

### Tiếp tục gọi đồng thời

Người chủ chạy trình thực hiện mỗi cuộc gọi trên dây chuyền riêng, coroutine hoặc người làm việc từ xa.`asyncio.gather`hoặc cấu trúc đồng thời. Trật tự hoàn thành là không thể đoán trước  ID là nhận dạng.

> Chủ nhà trên mỗi thiết bị thực hiện gọi chạy các dây chuyền của mình, cộng tác hoặc máy làm việc từ xa.`asyncio.gather`hoặc cấu trúc hóa并发──完成顺序不可预测id 是标识符──

> ️ **【易错点】**场景:流式模式下对每个 `arguments`分片立即 `json.loads`/ 后果: JSON 不完整触发 `JSONDecodeError`, vì dòng chảy có thể bạn nhận được .`{"city":"To`时就触发回调 / 修复: mỗi `tool_call_id`维护一个 `accumulator`字符串,所有分片 `+=`后等 `finish_reason="tool_calls"`才整体解析;并行时用 `{id: accumulator}`字典隔离──

Một lỗi phổ biến: trả lời với kết quả theo thứ tự danh sách gọi thay vì thứ tự hoàn thành.`tool_call_id`, nhưng nếu kết quả bị bỏ rơi hoặc sao chép, việc gửi ngoài trật tự sẽ làm cho việc gỡ lỗi khó khăn hơn.

> Một lỗi thường gặp: theo thứ tự của bảng xếp hạng thay vì hoàn thành thứ tự trả lời kết quả.`tool_call_id`, nhưng nếu kết quả bị bỏ rơi hoặc lặp lại, các trình đơn sắp xếp sẽ làm cho việc kiểm tra trở nên khó khăn hơn.

### Các cuộc gọi của công cụ streaming

> **【拓展：流式工具调用的用户体验】**流式工具调用让用户看到代理正在"思考"和执行的过程中,而不是等待一个黑盒操作完成――这对长时间的工具特别有价值用户可以看到参数逐步构建,提供心理预期――OpenAI's ChatGPT 和 Anthropic's Claude 都在UI中展示了工具调用流式过程――

Khi mô hình phát sóng,`arguments`3 dòng phân mảnh riêng biệt cho 3 cuộc gọi song song để liên lạc trên dây.

> Khi mô hình truyền tải,`arguments`分片到达──三并行调用三独立流块在传输中交错──你需要每个 id 一个累加器──

Hình dạng theo nhà cung cấp:

> Các nhà cung cấp:

- **OpenAI.**Mỗi mảnh đều là`choices[0].delta.tool_calls[i].function.arguments`(câu phần) Phần này mang theo`index`(trọng điểm trong danh sách gọi). Bạn tích lũy cho mỗi chỉ số, đọc `id`khi nó xuất hiện lần đầu tiên, và phân tích JSON khi `finish_reason = "tool_calls"`- Tôi không biết.
  Trung ngữ翻译:**OpenAI。**Mỗi khối là`choices[0].delta.tool_calls[i].function.arguments`(部分字符串) 块携带 `index`(调用列表中的位置) ∼ Bạn theo chỉ số tích lũy, lần đầu tiên xuất hiện 读取`id`, trong `finish_reason = "tool_calls"`时解析 JSON。
- **Anthropic.**Các sự kiện phát sóng là `message_start`, sau đó là một `content_block_start`mỗi khối với loại `tool_use`(có chứa ID, tên, nhập trống). `content_block_delta`các sự kiện mang theo`input_json_delta`- Bọn nó.`content_block_stop`đóng cửa từng khu phố.
  Trung ngữ翻译:**Anthropic。**Chuyện xảy ra trước đó là`message_start`, rồi mỗi loại là`tool_use`Một khối`content_block_start`(có chứa id、name、空 input)`content_block_delta`事件携带 `input_json_delta`块──`content_block_stop`关闭 mỗi khối.
- **Gemini.** `streamFunctionCallArguments`(Thiêm tinh 3 trở lên) phát ra các mảnh với một `functionCallId`Trước khi Gemini 3, streaming trả lại một cuộc gọi hoàn chỉnh một lần.
  Trung ngữ翻译:**Gemini。** `streamFunctionCallArguments`(Tình sinh 3 及以上) phát hành`functionCallId`Trong một khối, để调用 có thể làm sạch đất giao lưu.

### JSON một phần và bẫy phân tích sớm

Anh không thể phân tích được.`arguments`cho đến khi nó hoàn thành.`{"city": "Beng`là không hợp lệ và sẽ tăng. Cổng chính xác là tín hiệu kết thúc cuộc gọi của nhà cung cấp: OpenAI `finish_reason = "tool_calls"`, Anthropic's `content_block_stop`, hoặc sự kiện cuối dòng chảy của Gemini.`json.loads`Một cách tiếp cận mạnh hơn sử dụng một trình phân tích JSON tăng cường tạo ra các sự kiện khi cấu trúc hoàn thành; hướng dẫn phát trực tuyến của OpenAI khuyên dùng điều này cho UX hiển thị một chỉ số "thinking" trực tiếp. Brace-counting không đáng tin cậy như một bài kiểm tra tính hoàn chỉnh (những brace bên trong chuỗi trích dẫn hoặc nội dung thoát gây ra dương tính sai) và chỉ nên được sử dụng như một heuristic debug không chính thức.

> Trong `arguments`完成之前不能尝试解析──像 `{"city": "Beng`Phần này của JSON không hiệu quả, sẽ phát hiện ra bất thường.`finish_reason = "tool_calls"`、Anthropic của `content_block_stop`、 hoặc kết thúc của dòng chảy Gemini 事件── chỉ khi đó mới thử `json.loads`◊ Stronger method sử dụng tăng lượng JSON 解析器, tạo ra sự kiện khi kết cấu hoàn thành; OpenAI's流式指南推用于显示实时"思考"指示器的 UX。

> **【中文解读】**Không thể ở`arguments`完成之前尝试解析。`{"city": "Beng`Như vậy phần JSON không hiệu quả, sẽ phát ra bất thường.`finish_reason`、Anthropic của `content_block_stop`、Gemini's stream-end) ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼ ∼      ∼ ∼ ∼            ∼ ∼                        

### Việc hoàn thành ngoài trật tự

```
call_A: fast API, returns first
call_B: slow API, returns second
call_C: median API, returns third
```

Câu trả lời chủ nhà vẫn phải trích dẫn các ID:

> 宿主回复 vẫn cần trích dẫn id:

```
[{role: "tool", tool_call_id: "call_A", content: ...},
 {role: "tool", tool_call_id: "call_B", content: ...},
 {role: "tool", tool_call_id: "call_C", content: ...}]
```

Trật tự trong câu trả lời không quan trọng cho sự chính xác trên OpenAI hoặc Anthropic. Gemini chấp nhận bất kỳ lệnh nào miễn là ID phù hợp.

> Đơn vị trong 回复 đối với OpenAI hoặc Anthropic không quan trọng.

### Điểm chuẩn: theo trình tự đối với song song

Lăng trong `code/main.py`mô phỏng ba trình thực với độ trễ 400, 600 và 800 ms. Tiếp theo chạy nó trong tổng 1800 ms. song song chạy nó trong max ((400, 600, 800) = 800 ms. Sự khác biệt là không tương xứng, vì vậy tiết kiệm tăng lên với số lượng công cụ.

> `code/main.py`Các dây trung gian được mô phỏng là ba độ trễ khác nhau là 400、600 và 800 毫秒 của các thiết bị thực hiện.

Cảnh báo trong thế giới thực: các cuộc gọi song song nhấn mạnh các API dòng chảy xuống. Một fan-out 10 chiều cho một dịch vụ giới hạn tốc độ sẽ thất bại. Giai đoạn 13 · 17 bao gồm áp lực ngược ở cấp cửa khẩu; thử lại ngữ nghĩa được lên kế hoạch cho một giai đoạn tương lai.

> 现实注意事项:并行调用会给下游 API 施加压力──10 路扇出到速率限制的服务会失败──Phase 13 · 17 涵盖网关级背压;重试语义计划在未来阶段中──

### Streaming fan-out tường đồng hồ

Nếu mô hình tự phát, bạn có thể bắt đầu thực hiện ngay khi các lập luận của một cuộc gọi hoàn thành, thay vì chờ đợi tất cả các cuộc gọi hoàn thành. Đây là một tối ưu hóa tài liệu OpenAI nhưng không phải tất cả SDK lộ ra.

> Nếu mô hình tự nó là dòng chảy, bạn có thể bắt đầu thực hiện ngay sau khi một tham số được điều chỉnh hoàn thành, không cần phải chờ đợi tất cả các tham số được hoàn thành. Đây là một loại tối ưu hóa của hồ sơ OpenAI, nhưng không phải tất cả SDK đều tiết lộ khả năng này.

## Hãy sử dụng nó để thực hiện
```figure
tp-parallel-fanout
```

## Sử dụng nó

`code/main.py`có hai nửa. đầu tiên chạy ba cuộc gọi thời tiết mô phỏng theo trình tự và song song bằng cách sử dụng `concurrent.futures.ThreadPoolExecutor`Phần hai tái tạo phản ứng phát trực tuyến giả `arguments`cho ba cuộc gọi song song được giao tiếp trên một dòng  và lắp ráp lại chúng theo ID với `StreamAccumulator`Không có LLM, không có mạng, chỉ là logic tái lắp ráp.

> `code/main.py`Có hai phần.`concurrent.futures.ThreadPoolExecutor`顺序和并行运行三模拟天气调调,并印挂钟时间──第二部分回放一个假的流式响应三并行调用`arguments`块 trong một dòng chảy trên giao lưu 并用 `StreamAccumulator`按 id 重组──不需要 LLM,不需要网络,只是重组逻辑──

Những gì cần xem:

> 需要关注的点:

- Thời gian theo trình tự đạt 1,8 giây. Thời gian song song đạt 0,8 giây với cùng một độ trễ giả.
  Trung文翻译:串行计时器 đạt 1,8 giây.并行计时器在相同假延迟下达到 0.8 giây.
- Bộ tích lũy xử lý các khối đến khỏi thứ tự bằng cách bơm per-id và phân tích chỉ khi JSON của mỗi cuộc gọi hoàn thành.
  Trung ngữ翻译:累加器通过按 id 缓冲乱序到达的块来处理, chỉ trong mỗi调用 JSON 完成时才解析。
- Việc thực thi bắt đầu ngay khi các lập luận của một ID hoàn tất, không phải sau khi tất cả các dòng chảy kết thúc.
  Trung ngữ翻译: Executor trong một id của các tham số hoàn thành ngay lập tức khởi động, chứ không phải tất cả các dòng kết thúc.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-parallel-call-safety-check.md`. Với một danh sách công cụ, kiểm toán kỹ năng các công cụ nào là an toàn để song song, có phụ thuộc đặt hàng, và sẽ áp đảo các giới hạn lãi suất tiếp theo  trả lại một danh sách sửa đổi với mỗi công cụ `parallel_safe`Đường cờ.

> 本课产 出 `outputs/skill-parallel-call-safety-check.md` Đưa ra một sổ đăng ký công cụ, kỹ năng kiểm tra các công cụ có thể được đồng hành một cách an toàn, những thứ có thứ tự phụ thuộc, những thứ sẽ làm cho tốc độ truy cập xuống hạn chế không thể trở lại một với mỗi công cụ.`parallel_safe`标志的修订注册表

## Tập luyện bài tập

1. Đi chạy`code/main.py`và thay đổi độ trễ mô phỏng. xác nhận rằng tỷ lệ song song với theo trình là khoảng `max/sum`(các chạy thực sự khác biệt một chút với lý tưởng do lập trình chuỗi, chuỗi và chi phí trên cáp).
   Trung ngữ翻译:运行 `code/main.py`Không thay đổi mô hình trì hoãn.`max/sum`(trực tế vận hành do đường điều chỉnh, trình tự hóa và đường dây đai ra với giá trị lý tưởng có chút khác biệt)

2. Lớn bộ tích trữ để xử lý một trường hợp "call đã bị hủy ở giữa dòng" bằng cách thả bộ đệm của nó và phát ra một `cancelled`Chuyện này được xác định rõ ràng bởi nhà cung cấp nào?`content_block_stop`ngữ nghĩa và OpenAI `finish_reason: "length"`hành vi.
   Trung ngữ翻译:扩展累加器以处理"调用在流中途被取消"情况,丢弃其缓冲区并发出 `cancelled`事件── Which supplier has clearly recorded this situation? kiểm tra Anthropic của `content_block_stop`语义和 OpenAI của `finish_reason: "length"`行为──

3. Thay thế hồ chứa dây bằng `asyncio.gather`Bạn nên thấy những chiến thắng nhỏ trên async vì chi phí chuyển đổi ngữ cảnh thấp hơn, nhưng chỉ khi các trình thực hiện thực hiện thực tế I / O.
   中文翻译:用 `asyncio.gather`换线程池──进行基准测试── bạn nên thấy những lợi thế nhỏ hơn, vì giá thay đổi trên thấp hơn, nhưng điều kiện là trình thực hiện thực sự I/O──

4. Chọn hai công cụ mà không nên song song (ví dụ: `create_file`Vậy thì`write_file`). Thêm một `ordering_dependency`là cơ chế tối thiểu cho lập trình biết đến sự phụ thuộc, mà một giai đoạn kỹ thuật đại lý trong tương lai chính thức hóa.
   Trung ngữ翻译: chọn两个不应该并行化的工具(如 `create_file`Rồi rồi`write_file`                                                                                                                                                                                                                                                              `ordering_dependency`图,并 dựa trên 图门控制并行扇出. Đây là cơ chế tối thiểu của sự điều chỉnh cảm giác, trong tương lai đại lý 工程 giai đoạn sẽ được hình thành.

5. Đọc phần gọi hàm song song của OpenAI và Anthropic `disable_parallel_tool_use`Docs. Chọn loại công cụ thực tế mà Anthropic khuyên bạn nên vô hiệu hóa sự song song. (Nhận thức: đột biến hậu quả trên cùng một nguồn tài nguyên.)
   Trung ngữ翻译:阅读 OpenAI 的并行函数调用章节和人类的 `disable_parallel_tool_use`文档──找出 建议禁用并行 一种真实工具类型──(提示:对同一资源的后果性修改──)

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Parallel tool calls | "Fan-out in one turn" | Model emits multiple tool calls in a single assistant message | 并行工具调用 |
| `parallel_tool_calls` | "OpenAI's flag" | Enable or disable multi-call emission | OpenAI 并行调用开关 |
| `disable_parallel_tool_use` | "Anthropic's inverse" | Opt-out flag; default is parallel enabled | Anthropic 并行禁用开关 |
| Tool call id | "Correlation handle" | Per-call identifier the result message must echo | 工具调用标识符 |
| Accumulator | "Stream buffer" | Per-id string buffer for partial `arguments` chunks | 流式累加器 |
| Out-of-order completion | "Fastest first" | Parallel calls finish in unpredictable order; ids are the glue | 乱序完成 |
| Dependency graph | "Ordering constraints" | Tools whose outputs feed into inputs of other tools; cannot parallelize | 依赖图 |
| Parse-early trap | "JSON.parse exploded" | Attempting to parse an incomplete `arguments` string | 过早解析陷阱 |
| `streamFunctionCallArguments` | "Gemini 3 feature" | Streamed argument chunks with unique id per call | Gemini 3 流式参数 |
| Completion-order reply | "Don't wait for all" | Reply with results as they arrive, keyed by id | 按完成顺序回复 |

## Xem thêm 延伸阅读

- [OpenAI — Parallel function calling](https://platform.openai.com/docs/guides/function-calling#parallel-function-calling) Hành vi mặc định và cờ không chọn
  Trung ngữ翻译:默认行为和退出标志
- [Anthropic — Tool use: implementing tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implementing-tool-use) `disable_parallel_tool_use`và kết quả đợt
  Trung ngữ翻译:`disable_parallel_tool_use`Và kết quả xử lý
- [Google — Gemini function calling parallel section](https://ai.google.dev/gemini-api/docs/function-calling) Các cuộc gọi song song liên quan đến ID từ Gemini 3
  Trung文翻译:Gemini 3 的 id 关联并行调用
- [OpenAI — Streaming responses with tools](https://platform.openai.com/docs/api-reference/responses-streaming) Phục bộ lập luận lại cho các dòng OpenAI
  Trung ngữ翻译:OpenAI 流的分块参数重组
- [Anthropic — Streaming messages](https://docs.anthropic.com/en/api/messages-streaming) `content_block_delta`với `input_json_delta`
  Trung ngữ翻译:带 `input_json_delta`của `content_block_delta`
