# Function Calling Deep Dive  OpenAI, Anthropic, Gemini 函数调用深入:三大供应商对比

> Ba nhà cung cấp biên giới hội tụ trên cùng một vòng gọi công cụ vào năm 2024 và sau đó khác nhau về mọi thứ khác.`tools`và `tool_calls`- Sử dụng nhân loại`tool_use`và `tool_result`Đứa sinh đôi sử dụng`functionDeclarations`Bài học này khác biệt ba bên cạnh nhau để mã được gửi trên một nhà cung cấp không bị phá vỡ khi bạn chuyển nó.

> **【中文解读】**Các nhà cung cấp hàng đầu ở Việt Nam sẽ tiếp nhận cùng một vòng lặp sử dụng công cụ trong năm 2024, nhưng thực hiện các sự khác biệt cụ thể.`tools`- Không.`tool_calls`, Anthropic sử dụng `tool_use`- Không.`tool_result`块,Tình sinh `functionDeclarations`Và chỉ có một ID 关联──Bản đối, để bạn chuyển mã viết trên một nhà cung cấp vào một thời gian khác không đến khi bị phá vỡ──

> **【拓展：Function Calling】**函数调用 (函数调用) là cơ chế cốt lõi của giao tiếp với thế giới bên ngoài. LLM không thực hiện trực tiếp hoạt động, mà là xuất ra cấu trúc hóa "调准图" (调准图) của các công cụ tên + tham số, được thực hiện sau khi trả lại kết quả.

>  **【前置】**Học本节前请先掌握:(1) Bước 13·01(The Tool Interface) 本节 là sự mở ra của nó, phải ăn trước qua vòng bốn bước;(2) Bước 11·03(Outputs cấu trúc)  hiểu JSON Schema,三大供应商的 `parameters`- Không.`input_schema`文档──如果不会区分`tool_choice`Trong 3 mô hình, trước tiên hãy xem các bước "phát quyết" của giai đoạn 13.01.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, schema translators) | **语言:** Python（标准库，模式翻译器）
**Prerequisites:** Phase 13 · 01 (the tool interface) | **前置知识:** Phase 13 · 01（工具接口）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Cụ thể ra ba sự khác biệt hình dạng giữa OpenAI, Anthropic và Gemini gọi hàm tải trọng hữu ích (sự tuyên bố, gọi, kết quả).
  Nói rõ OpenAI、Anthropic、Gemini 函数调用载荷的三种形态差异(声明、调用、结果)
- Dịch một tuyên bố công cụ trên cả ba định dạng nhà cung cấp và dự đoán những hạn chế chế chế độ nghiêm ngặt sẽ khác nhau.
  将一个工具声明 译为三种供应商格式,预测严格 模式约束在哪会不同.
- Sử dụng `tool_choice`trong mỗi nhà cung cấp để buộc, cấm, hoặc tự động chọn công cụ gọi.
  Trong mỗi nhà cung cấp sử dụng `tool_choice`强制、禁止或自动选择工具调用──
- Biết các giới hạn cứng mỗi nhà cung cấp (tương tự số công cụ, độ sâu sơ đồ, chiều dài lập luận) và các chữ ký lỗi mỗi người phát ra khi các giới hạn bị vi phạm.
  了解各供应商的硬限制 ()                                                                                                                                                                                                                                                         

## Vấn đề  vấn đề giới thiệu

Các hình thức của yêu cầu gọi chức năng khác nhau theo nhà cung cấp. ba ví dụ cụ thể từ các hàng sản xuất năm 2026:

> Các hình thức của việc yêu cầu chức năng khác nhau với nhà cung cấp.

> **【中文解读】**Phụng thức của yêu cầu của hàm调用 khác nhau với nhà cung cấp.`tools`+`tool_calls`, 响应中 `arguments`là cần phải phân tích JSON 字符串;Anthropic 用 `tool_use`- Không.`tool_result`块,`input`已经是解析好的对象; 双胞胎用嵌套的`functionDeclarations`, kết quả qua `functionResponse`返回── cùng một vòng lặp, các kiểu chữ khác nhau, các kiểu hình dạng, các chuỗi so với các thiết bị định hình và hệ thống liên kết từ một nhà cung cấp chuyển sang một "đầu công trình ống" khác chỉ cần hai hoặc ba ngày.

**OpenAI Chat Completions / Responses API.**Anh qua đi.`tools: [{type: "function", function: {name, description, parameters, strict}}]`Phản ứng của mô hình chứa `choices[0].message.tool_calls: [{id, type: "function", function: {name, arguments}}]`nơi `arguments`là một chuỗi JSON bạn phải phân tích.`strict: true`) thực thi tuân thủ các kế hoạch thông qua mã hóa hạn chế.

> **OpenAI Chat Completions / Responses API。**Anh truyền vào`tools: [{type: "function", function: {name, description, parameters, strict}}]` Mô hình của phản ứng bao gồm`choices[0].message.tool_calls: [{id, type: "function", function: {name, arguments}}]`, trong số đó `arguments`là một cần bạn tự động phân tích JSON 字符串。严格模式(`strict: true`(Từ quy định giải mã bắt buộc thực hiện mô hình hợp pháp).

**Anthropic Messages API.**Anh qua đi.`tools: [{name, description, input_schema}]`Câu trả lời là:`content: [{type: "text"}, {type: "tool_use", id, name, input}]`- `input`đã được phân tích (một đối tượng, không phải một chuỗi). Bạn trả lời với một `user`thông điệp chứa một `{type: "tool_result", tool_use_id, content}`- Quận.

> **Anthropic Messages API。**Anh truyền vào`tools: [{name, description, input_schema}]`   `content: [{type: "text"}, {type: "tool_use", id, name, input}]`形式返回──`input`已被解析 (已被解析) là một đối tượng, không phải là một字符串 (你用包含)`{type: "tool_result", tool_use_id, content}`块的新 `user`消息回复.

**Google Gemini API.**Anh qua đi.`tools: [{functionDeclarations: [{name, description, parameters}]}]`(đồng dưới `functionDeclarations`) Câu trả lời đến như `candidates[0].content.parts: [{functionCall: {name, args, id}}]`nơi `id`là duy nhất trong Gemini 3 và lên cho tương quan liên quan đến cuộc gọi song song.`{functionResponse: {name, id, response}}`- Tôi không biết.

> **Google Gemini API。**Anh truyền vào`tools: [{functionDeclarations: [{name, description, parameters}]}]`(đúng trong `functionDeclarations`下) ・ đáp ứng`candidates[0].content.parts: [{functionCall: {name, args, id}}]`形式到达, trong đó `id`Trong phiên bản Gemini 3 及以上 là duy nhất, được sử dụng để làm việc với các thiết bị liên kết.`{functionResponse: {name, id, response}}`回复:

Một nhóm người viết một thông báo thời tiết trên OpenAI trả tiền hai ngày cho Anthropic và một ngày khác cho Gemini chỉ vì ống nước.

> Một nhóm đại lý khí hậu trên OpenAI được chuyển đến Anthropic 需要两天,再到双胞胎 又需要一天只是管道工程──

>  **【类比】**三大供应商像三种不同的快递公司──都能寄包裹(同一循环), nhưng vận chuyển đơn格式不同:OpenAI 把物品清单写在面单上需要收件人看自己(`arguments`là JSON 字符串);Anthropic 把清单内容已经填好直接看(`input`已解析对象);Gemini 用专门运单号 UUID 区分包裹(Gemini 3+) ・・・本质都是寄快递, nhưng mỗi công ty运单设计不同, vì vậy bạn cần một"统一运单翻译器" để chuyển đổi trong nhiều công ty。

Bài học này xây dựng một trình dịch mà thống nhất ba định dạng thành một tuyên bố công cụ và các tuyến đường tại cạnh.

> Bài học này xây dựng một trình dịch, sẽ thống nhất 3 kiểu như một tuyên bố công cụ quy định, và tiến hành hành hành trình.

## Khái niệm cốt lõi

### Cơ cấu chung

Mỗi nhà cung cấp cần 5 điều:

> Mỗi nhà cung cấp đều cần 5 thứ:

1. **Tool list.**Tên, mô tả và sơ đồ đầu vào mỗi công cụ.
   Trung ngữ翻译:**工具列表。**Tên, mô tả và mô hình nhập của mỗi công cụ.
2. **Tool choice.**Bắt buộc một công cụ cụ thể, cấm công cụ, hoặc để mô hình quyết định.
   Trung ngữ翻译:**工具选择。**强制使用特定工具、禁止使用工具或让模型自主决定──
3. **Call emission.**Kết quả kết cấu đặt tên công cụ và các lập luận.
   Trung ngữ翻译:**调用输出。**命名工具和参数的结构化输出──
4. **Call id.**Kết hợp phản ứng với cuộc gọi đúng (nhiều quan trọng cho song song).
   Trung ngữ翻译:**调用 ID。**Sẽ đáp ứng quan hệ với chính xác điều chỉnh
5. **Result injection.**Một tin nhắn hoặc chặn liên kết kết quả trở lại với cuộc gọi.
   Trung ngữ翻译:**结果注入。**Kết quả sẽ được kết nối với các thông tin hoặc khối.

> **【中文解读】**Mỗi nhà cung cấp đều cần 5 thứ: danh sách công cụ (nói + mô tả + nhập Schema)  lựa chọn công cụ (nói buộc/ cấm/ tự động) 调用输出 (nói và tham số của công cụ được cấu trúc) 调用 ID (nói kết nối)  kết quả (nói kết quả)  kết quả sẽ được kết nối với các thông tin hoặc khối được调用) 

### Sự khác biệt hình dạng, trường theo trường

> ️ **【易错点】**场景:把 OpenAI 代码原样贴到Anthropic / 后果:`tool_calls`字段不存在导致 `KeyError`, và OpenAI của `arguments`  `json.loads()`,Anthropic của `input`已是 dict,直接访问会得到字符串而非字段值 / 修复: phải viết适配层或使用 LiteLLM 这类统一 SDK;若手写,每个供应商独立测试用例覆盖──

| Aspect | OpenAI | Anthropic | Gemini |
|--------|--------|-----------|--------|
| 方面 | OpenAI | Anthropic | Gemini |
| Declaration envelope | `{type: "function", function: {...}}` | `{name, description, input_schema}` | `{functionDeclarations: [{...}]}` |
| 声明信封 | `{type: "function", function: {...}}` | `{name, description, input_schema}` | `{functionDeclarations: [{...}]}` |
| Schema field | `parameters` | `input_schema` | `parameters` |
| Schema 字段 | `parameters` | `input_schema` | `parameters` |
| Response container | `tool_calls[]` on assistant message | `content[]` of type `tool_use` | `parts[]` of type `functionCall` |
| 响应容器 | assistant 消息上的 `tool_calls[]` | `content[]` 中类型为 `tool_use` 的块 | `parts[]` 中类型为 `functionCall` 的条目 |
| Arguments type | stringified JSON | parsed object | parsed object |
| 参数类型 | 字符串化 JSON | 已解析对象 | 已解析对象 |
| Id format | `call_...` (OpenAI generates) | `toolu_...` (Anthropic) | UUID (Gemini 3+) |
| ID 格式 | `call_...`（OpenAI 生成） | `toolu_...`（Anthropic） | UUID（Gemini 3+） |
| Result block | role `tool`, `tool_call_id` | `user` with `tool_result`, `tool_use_id` | `functionResponse` with matching `id` |
| 结果块 | 角色 `tool`，`tool_call_id` | 带有 `tool_result` 的 `user` 消息，`tool_use_id` | 带有匹配 `id` 的 `functionResponse` |
| Force-a-tool | `tool_choice: {type: "function", function: {name}}` | `tool_choice: {type: "tool", name}` | `tool_config: {function_calling_config: {mode: "ANY"}}` |
| 强制工具 | `tool_choice: {type: "function", function: {name}}` | `tool_choice: {type: "tool", name}` | `tool_config: {function_calling_config: {mode: "ANY"}}` |
| Forbid tools | `tool_choice: "none"` | `tool_choice: {type: "none"}` | `mode: "NONE"` |
| 禁止工具 | `tool_choice: "none"` | `tool_choice: {type: "none"}` | `mode: "NONE"` |
| Strict schema | `strict: true` | schema-is-schema (always enforced) | `responseSchema` at request level |
| 严格模式 | `strict: true` | 模式即模式（始终强制执行） | 请求级别的 `responseSchema` |

### Những giới hạn mà bạn thực sự sẽ đạt được

> **【中文解读】**OpenAI:128 个工具/请求,Schema độ sâu 5,参数字符串 ≤8192 字节,strict 模式不支持 `$ref`- Không.`oneOf`等重叠组合──Anthropic:64 个工具/请求,Schema depth无硬限制但实际约10,无严格 模式标志但模型倾向于遵守──Gemini:64 个函数/请求,使用OpenAPI 3.0 子集(与JSON Schema 2020-12 有微微差异),Gemini 3 起支持唯一 ID──

- **OpenAI.**128 công cụ mỗi yêu cầu. Độ sâu sơ đồ 5. Dòng tranh luận <= 8192 byte.`$ref`Không .`oneOf`- Không.`anyOf`- Không.`allOf`với sự chồng chéo, mọi tài sản được liệt kê trong `required`- Tôi không biết.
  Trung ngữ翻译:**OpenAI。**Mỗi yêu cầu 128 个工具──Schema độ sâu 5──参数字符串 ≤ 8192 字节──严格模式要求无 `$ref`, không bị chồng lên `oneOf`- Không.`anyOf`- Không.`allOf`, mỗi thuộc tính đều nằm trong `required`Ở giữa.
- **Anthropic.**64 công cụ mỗi yêu cầu. Độ sâu sơ đồ thực sự không giới hạn nhưng giới hạn thực tế 10. Không có cờ chế độ nghiêm ngặt; sơ đồ là một hợp đồng và mô hình có xu hướng tuân thủ.
  Trung ngữ翻译:**Anthropic。**Mỗi yêu cầu 64 工具──Sự sâu của Schema thực sự không giới hạn nhưng thực tế là khoảng 10── không có dấu hiệu mô hình nghiêm ngặt; mô hình là hiệp ước, mô hình có xu hướng tuân thủ──
- **Gemini.**64 chức năng mỗi yêu cầu. Các loại Schema là OpenAPI 3.0 (sự khác biệt nhẹ từ JSON Schema 2020-12).
  Trung ngữ翻译:**Gemini。**Mỗi yêu cầu 64 个函数──Schema 类型是 OpenAPI 3.0 子集(与 JSON Schema 2020-12 有微差)──Gemini 3起支持并行调的唯一ID──

> 🤔 **【困惑】**Q: 既然三形不同,为什么不直接使用 LangChain或 LiteLLM 抽象掉? A: 抽象层确实能省80% 代码, nhưng cần cảnh báo"抽象泄漏": chế độ nghiêm ngặt 限制(OpenAI không hỗ trợ `$ref`)`tool_choice`                                                                                                                                                                                              `required`(c) 、 lỗi về định dạng khác nhau sẽ không được rút ra.

### `tool_choice`hành vi

Ba chế độ mà mọi người đều hỗ trợ, có tên khác nhau.

> Ba mô hình mỗi nhà cung cấp đều hỗ trợ, nhưng tên khác nhau.

- **Auto.**Mô hình chọn công cụ hoặc văn bản.
  Trung ngữ翻译:**自动。**模型选择工具或文本──默认值──
- **Required / Any.**Mô hình phải gọi ít nhất một công cụ.
  Trung ngữ翻译:**必需 / 任意。**模型 phải ít nhất调用 một công cụ.
- **None.**Mô hình không được gọi là công cụ.
  Trung ngữ翻译:**无。**模型 phải调用工具――

Thêm một chế độ độc đáo cho mỗi nhà cung cấp:

> Ngoài ra, mỗi nhà cung cấp có một mô hình độc đáo:

- **OpenAI.**Cố gắng dùng một công cụ cụ thể bằng tên.
  Trung ngữ翻译:**OpenAI。**按名称强制特定工具──
- **Anthropic.**Cần dùng một công cụ cụ thể bằng tên; `disable_parallel_tool_use`cờ phân biệt đơn với đa.
  Trung ngữ翻译:**Anthropic。**按名称强制特定工具;`disable_parallel_tool_use`标志区分单次与多次调用──
- **Gemini.** `mode: "VALIDATED"`định tuyến mọi phản ứng thông qua một trình xác nhận schema bất kể mục đích mô hình.
  Trung ngữ翻译:**Gemini。** `mode: "VALIDATED"`Mỗi phản ứng sẽ được thông qua mô hình xác nhận, bất kể mô hình có ý định như thế nào.

### Các cuộc gọi song song

> **【拓展：并行调用的生产实践】**Việc thực hiện các công cụ có thể giảm đáng kể từ cuối đến cuối trì hoãn. Ví dụ: một đại lý lập kế hoạch du lịch cần đồng thời hỏi hàng không, khách sạn, khí hậu, 3 vòng LLM, nhưng cần phải thực hiện 1 vòng, nhưng lưu ý: việc thực hiện sẽ tăng chi phí và sự phức tạp của việc thực hiện, và cần phải xử lý đúng kết quả.

OpenAI `parallel_tool_calls: true`(phụ mặc định) phát ra nhiều cuộc gọi trong một tin nhắn trợ lý. Bạn chạy tất cả chúng và trả lời bằng một tin nhắn vai trò công cụ bao gồm một mục mỗi `tool_call_id`. Anthropic lịch sử đã gọi một lần;`disable_parallel_tool_use: false`(tầm như Claude 3.5) cho phép nhiều. Gemini 2 cho phép gọi song song nhưng không cung cấp ID ổn định; Gemini 3 thêm UUID để các phản ứng ngoài trật tự tương quan sạch.

> OpenAI của `parallel_tool_calls: true`(默认) Trong một bài viết 消息中发发多个调用──你运行所有调用,然后回复一个批量工具角色消息,每个 `tool_call_id`Một条目:  lịch sử nhân loại chỉ làm một lần调用;`disable_parallel_tool_use: false`(Công 3.5) đã kích hoạt nhiều lần调用. Gemini 2 cho phép并行调用 nhưng không có ID ổn định. Gemini 3 đã thêm UUID, làm cho sự rối loạn序响应 có thể干净地关联.

### Chuyển phát

Cả ba cuộc gọi hỗ trợ truyền thông thông qua công cụ.

> 三者都支持流式工具调用──传输形式 có những khác biệt:

- **OpenAI.**Các mảnh Delta của `tool_calls[i].function.arguments`đến từng bước.`finish_reason: "tool_calls"`- Tôi không biết.
  Trung ngữ翻译:**OpenAI。** `tool_calls[i].function.arguments`Số lượng khối dần dần đến...`finish_reason: "tool_calls"`
- **Anthropic.**Các sự kiện bắt đầu khối / block-delta / block-stop. `input_json_delta`Các mảnh có những tranh luận một phần.
  Trung ngữ翻译:**Anthropic。**块开始 / 块增量 / 块停止事件──`input_json_delta`块携带部分参数──
- **Gemini.** `streamFunctionCallArguments`(khởi đầu trong Gemini 3) phát ra các mảnh với một `functionCallId`để nhiều cuộc gọi song song có thể giao tiếp.
  Trung ngữ翻译:**Gemini。** `streamFunctionCallArguments`(Tình sinh 3 新增) 发出带有 `functionCallId`Các khối, làm cho nhiều đường điều chỉnh có thể giao lưu.

Giai đoạn 13 · 03 đi sâu vào việc lắp ráp lại song song và dòng phát. Bài học này tập trung vào các hình dạng tuyên bố và một cuộc gọi.

> Giai đoạn 13 · 03 Thấu hiểu sâu về việc kết hợp và tái cấu trúc quy trình.

### Hầm lẫn và sửa chữa

> **【拓展：JSON Repair 的工业实践】**Mô hình quay lại không hiệu quả JSON là vấn đề thường gặp.`json-repair`(GitHub 2k+ stars) chuyên xử lý các vấn đề này. Một giải pháp hiện đại hơn là sử dụng cấu trúc xuất ra, thông qua việc giải mã mã trong token sinh sản giai đoạn là đảm bảo định dạng chính xác, từ cơ bản loại bỏ JSON 解析 thất bại风险.

Các lỗi lập luận không hợp lệ cũng trông khác nhau.

> 无效参数的错误表现也不同──

- **OpenAI (non-strict).**Phản hồi mô hình `arguments: "{bad json}"`, phân tích JSON của bạn thất bại, bạn tiêm một thông điệp lỗi và gọi lại.
  Trung ngữ翻译:**OpenAI（非严格模式）。**模型返回 `arguments: "{bad json}"`, , JSON của bạn 解析 thất bại, bạn nhập thông tin sai và tái调用.
- **OpenAI (strict).**Việc xác thực xảy ra trong quá trình giải mã; JSON không hợp lệ là không thể nhưng `refusal`có thể xuất hiện.
  Trung ngữ翻译:**OpenAI（严格模式）。**验证在解码期间进行; không hiệu quả JSON không thể xuất hiện, nhưng có thể xuất hiện `refusal`
- **Anthropic.** `input`có thể chứa các trường bất ngờ; schema là tư vấn.
  Trung ngữ翻译:**Anthropic。** `input`Có thể chứa các đoạn không ngờ; mô hình là khuyến nghị tình dục.
- **Gemini.**Khái niệm của OpenAPI 3.0: `enum`trên các trường đối tượng bị bỏ qua lặng lẽ; xác nhận bản thân.
  Trung ngữ翻译:**Gemini。**OpenAPI 3.0 怪癖:对象字段上的 `enum`会被静默忽略;自行验证──

### Mô hình dịch giả.

> **【中文解读】**翻译器模式:定义一个规范的 `Tool`数据类,三个小函数分别翻译为三种供应商的声明形式──`AbstractToolset`(AI Pydantic)`UniversalToolNode`(LangGraph) hoặc `BaseTool`(LlamaIndex) ――Phase 13 Bài học 17 会构建一个网关,在前端暴露OpenAI 格式 API,后端对接任意供应商――

Một tuyên bố công cụ theo quy định trong mã của bạn trông như thế này (bạn chọn hình dạng):

```python
Tool(
    name="get_weather",
    description="Use when ...",
    input_schema={"type": "object", "properties": {...}, "required": [...]},
    strict=True,
)
```

Ba chức năng nhỏ chuyển nó sang ba hình dạng cung cấp.`code/main.py`làm chính xác điều này, sau đó đi vòng qua một cuộc gọi công cụ giả thông qua hình thức phản hồi của mỗi nhà cung cấp. Không cần mạng  bài học này dạy các hình dạng, không phải HTTP.

> 三个小函数将其翻译为三种供应商格式──`code/main.py`Các mạng trung tâm được thực hiện như vậy, sau đó qua các mẫu phản ứng của mỗi nhà cung cấp quay lại một lần gọi các công cụ giả mạo.

Các nhóm sản xuất đóng gói dịch giả này trong `AbstractToolset`(AI Pydantic),`UniversalToolNode`(LangGraph), hoặc `BaseTool`(LlamaIndex). Giai đoạn 13 · 17 đưa ra một cửa ngõ cho thấy một API hình dạng OpenAI trước bất kỳ ba.

> 生产团队将此翻译器包装为 `AbstractToolset`(AI Pydantic)`UniversalToolNode`(LangGraph) hoặc `BaseTool`(LlamaIndex) ――Phase 13 · 17  phát hành một mạng, trong ba nhà cung cấp bất kỳ một trước khi được phát hiện OpenAI format API。

## Hãy sử dụng nó để thực hiện
```figure
function-call-args
```

## Sử dụng nó

`code/main.py`định nghĩa một canonical `Tool`Dataclass và ba trình dịch phát ra OpenAI, Anthropic và Gemini tuyên bố JSON. Nó sau đó phân tích một phản ứng của nhà cung cấp bằng tay của mỗi hình dạng vào cùng một đối tượng gọi theo quy luật, chứng minh rằng ngữ nghĩa là giống nhau dưới da.

> `code/main.py` định nghĩa một quy tắc `Tool`Các phân loại dữ liệu và 3 phiên dịch viên, phân biệt xuất phát OpenAI、Anthropic 和 Gemini tuyên bố JSON── sau đó nó sẽ phân tích các ứng dụng của nhà cung cấp của mỗi kiểu hình thức làm thủ công để phân tích cho cùng một quy tắc điều chỉnh đối tượng, chứng minh dưới lớp biểu ngữ là giống nhau── vận hành nó và并排比三个 tuyên bố──

Những gì cần xem:

> 需要关注的点:

- Ba khối tuyên bố chỉ khác nhau về phong bì và tên trường.
  Trung ngữ翻译:三个声明块只在信封和字段名上不同.
- Ba khối phản ứng khác nhau trong nơi cuộc gọi sống (bậc cao `tool_calls`- `content[]`khối,`parts[]`nhập).
  Trung文翻译:三个响应块在调用所在位置上不同(顶层 `tool_calls``content[]`块,`parts[]`条目)
- Một `canonical_call()`chiết xuất chức năng `{id, name, args}`từ cả ba hình thức phản ứng.
  Trung ngữ翻译:一个 `canonical_call()`函数 từ tất cả các 3 kiểu phản ứng `{id, name, args}`

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-provider-portability-audit.md`. Với sự tích hợp gọi chức năng với một nhà cung cấp, kỹ năng tạo ra một kiểm toán khả năng di chuyển: nhà cung cấp giới hạn mà nó dựa vào, những lĩnh vực cần đổi tên, và những gì phá vỡ khi di chuyển đến các nhà cung cấp khác.

> 本课产 出 `outputs/skill-provider-portability-audit.md` Đưa ra cho một nhà cung cấp chức năng điều chỉnh tích hợp, kỹ năng này tạo ra một kiểm toán có thể di chuyển: phụ thuộc vào những hạn chế của nhà cung cấp, những phần nào cần được đổi tên, và những gì xảy ra khi di chuyển đến các nhà cung cấp khác.

## Tập luyện bài tập

1. Đi chạy`code/main.py`và xác minh rằng ba tuyên bố nhà cung cấp JSON tất cả các serialize cùng một cơ sở `Tool`sửa đổi công cụ Canonical để thêm một parameter enum và xác nhận chỉ cần phiên dịch viên Gemini để xử lý quirk OpenAPI.
   运行代码,验证三个供应商声明 JSON 都序列化一个 `Tool`Đối tượng: 添加 enum 参数, xác nhận chỉ có Gemini 翻译器需处理 OpenAPI 怪癖:

2. Thêm một `ListToolsResponse`parser cho mỗi nhà cung cấp lấy danh sách công cụ một mô hình trả lại sau khi `list_tools`OpenAI không có một bản địa; lưu ý sự bất đối xứng này.
   Đối với mỗi nhà cung cấp thêm `ListToolsResponse`解析器──注意 OpenAI 原生不支持这个功能的非对称性──

3. Thực hiện`tool_choice`chuyển đổi: bản đồ một canonical `ToolChoice(mode="force", tool_name="x")`trong cả ba hình dạng nhà cung cấp.`mode="any"`và `mode="none"`Hãy kiểm tra bảng điểm khác biệt của bài học.
   实现 `tool_choice`转换:将规范的 `ToolChoice`映射到三种供应商格式,覆盖力/任何/没有模式──

4. Chọn một trong ba nhà cung cấp và đọc hướng dẫn gọi chức năng của nó từ đầu đến cuối. Tìm một trường trong mô hình sơ đồ của nó mà hai người khác không hỗ trợ.`strict`, Anthropic `disable_parallel_tool_use`, Gemini `function_calling_config.allowed_function_names`- Tôi không biết.
    chọn một nhà cung cấp đọc hàm调用指南, tìm ra một hai đoạn không được hỗ trợ khác.

5. Viết một vector thử nghiệm: một cuộc gọi công cụ mà các lập luận vi phạm sơ đồ được tuyên bố. Đưa nó qua xác thực viên của mỗi nhà cung cấp (stdlib trong Bài học 01 sẽ làm như một đại diện) và ghi lại lỗi nào xảy ra. Tài liệu mà bạn sẽ sử dụng trong sản xuất để tính nghiêm ngặt.
   编写 vi phạm quy trình của quy trình, thông qua các nhà cung cấp kiểm chứng vận hành, ghi lại những sai lầm触发.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| 术语 | 通俗说法 | 实际含义 |
| Function calling | "Tool use" | Provider-level API for structured tool-call emission |
| 函数调用 | "工具使用" | 提供商级别的结构化工具调用输出 API |
| Tool declaration | "Tool spec" | Name + description + JSON Schema input payload |
| 工具声明 | "工具规格" | 名称 + 描述 + JSON Schema 输入负载 |
| `tool_choice` | "Force / forbid" | Auto / required / none / specific-name modes |
| `tool_choice` | "强制 / 禁止" | 自动 / 必需 / 无 / 指定名称模式 |
| Strict mode | "Schema enforcement" | OpenAI flag that constrains decoding to match schema |
| 严格模式 | "Schema 强制执行" | OpenAI 约束解码以匹配模式的标志 |
| `tool_use` block | "Anthropic's call shape" | Inline content block with id, name, input |
| `tool_use` 块 | "Anthropic 的调用格式" | 包含 id、name、input 的内联内容块 |
| `functionCall` part | "Gemini's call shape" | A `parts[]` entry containing name, args, and id |
| `functionCall` 部分 | "Gemini 的调用格式" | 包含 name、args 和 id 的 `parts[]` 条目 |
| Arguments-as-string | "Stringified JSON" | OpenAI returns args as a JSON string, not an object |
| 参数为字符串 | "字符串化 JSON" | OpenAI 以 JSON 字符串而非对象返回参数 |
| Parallel tool calls | "Fan-out in one turn" | Multiple tool calls in one assistant message |
| 并行工具调用 | "一回合扇出" | 一条 assistant 消息中的多个工具调用 |
| Refusal | "Model declines" | Strict-mode-only refusal block instead of a call |
| 拒绝 | "模型拒绝" | 仅严格模式下的拒绝块，替代调用 |
| OpenAPI 3.0 subset | "Gemini schema quirk" | Gemini uses a JSON-Schema-like dialect with minor differences |
| OpenAPI 3.0 子集 | "Gemini Schema 怪癖" | Gemini 使用类似 JSON Schema 的方言，存在细微差异 |

## Xem thêm 延伸阅读

- [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) tham chiếu kinh điển bao gồm chế độ nghiêm ngặt và các cuộc gọi song song
  Trung ngữ翻译:包含严格模式和并行调用的权威参考
- [Anthropic — Tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) `tool_use`và `tool_result`block semantics
  Trung ngữ翻译:`tool_use`和 `tool_result`块语义
- [Google — Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling) Các cuộc gọi song song, ID độc đáo và bộ phận OpenAPI
  Trung ngữ翻译:并行调用、唯一 ID 和 OpenAPI 子集
- [Vertex AI — Function calling reference](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling) bề mặt doanh nghiệp của Gemini
  Trung ngữ翻译:Gemini 的企业级接口
- [OpenAI — Structured outputs](https://platform.openai.com/docs/guides/structured-outputs) chi tiết về việc thực thi các quy trình chế độ nghiêm ngặt
  Trung文翻译:严格模式 Schema 强制执行细节
