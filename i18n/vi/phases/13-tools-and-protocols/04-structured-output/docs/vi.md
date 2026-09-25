# Kết quả cấu trúc  JSON Schema, Pydantic, Zod, mã hóa hạn chế   cấu trúc xuất: JSON Schema、Pydantic、Zod và约束解码

> "Hãy yêu cầu mô hình tốt để trả lại JSON" thất bại từ 5 đến 15% thời gian, ngay cả trên các mô hình biên giới. Các sản phẩm kết cấu đóng khoảng cách đó bằng cách giải mã hạn chế: mô hình được ngăn chặn từ chữ để phát ra một token sẽ vi phạm sơ đồ.`responseSchema`, AI của Pydantic `output_type`, và Zod `.parse`là năm hình dạng bề mặt của cùng một ý tưởng. Bài học này xây dựng trình xác nhận sơ đồ và các học viên hợp đồng chế độ nghiêm ngặt sẽ sử dụng cho mỗi đường ống khai thác sản xuất.

> **【中文解读】**"Tình cách để mô hình trả về JSON" vẫn có tỷ lệ thất bại 5-15% trên mô hình phía trước.`responseSchema`、AI Pydantic `output_type`和 Zod `.parse`Đó là 5 hình thức bề mặt của cùng một ý tưởng.

> **【拓展：结构化输出→Function Calling 的质量保障】**结构化输出 là nền tảng của tất cả các ống dẫn lấy dữ liệu. Trong trường hợp gọi chức năng, cấu trúc xuất hiện đảm bảo các cấu trúc JSON của các phần tử công cụ luôn luôn hiệu quả. OpenAI chế độ nghiêm ngặt thông qua mã hóa hạn chế trong giải mã, ngăn chặn vi phạm các token của Schema, Anthropic thông qua.`input_schema`Trong tool_use thực hiện similar assurance. Điều này loại bỏ "model return ineffective JSON" là một trong những sản xuất lỗi phổ biến nhất.

>  **【前置】**学本节前请先掌握:(1) Bước 11·03(Structured Outputs) 基础;(2) Bước 13·01(The Tool Interface) 和 13·02(Function Calling Deep Dive) 理解严格模式 出现前的"prompt for JSON"失败模式;(3) Pydantic v2 或 Zod 基础语法,本节会使用它们生成 Schema。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, JSON Schema 2020-12 subset) | **语言:** Python（标准库，JSON Schema 2020-12 子集）
**Prerequisites:** Phase 13 · 02 (function calling deep dive) | **前置知识:** Phase 13 · 02（函数调用深入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Viết một JSON Schema 2020-12 cho mục tiêu khai thác bằng cách sử dụng các hạn chế đúng (enum, min/max, yêu cầu, mô hình).
  中文翻译:使用正确的约束(enum、min/max、required、pattern) 为提取目标编写 JSON Schema 2020-12。
- Giải thích tại sao chế độ nghiêm ngặt và mã hóa hạn chế cung cấp các đảm bảo khác với "sự xác thực sau thế hệ".
  Trung ngữ翻译:解释为什么严格模式 和约束解码提供与"生成后验证" khác nhau.
- Hóa ra ba chế độ thất bại: lỗi phân tích, vi phạm sơ đồ, từ chối mô hình.
  Trung文翻译:区分三种失败模式:解析错误、Schema 违规、模型拒绝──
- Chuyển một đường ống khai thác với sửa chữa kiểu và xử lý từ chối kiểu.
  Trung ngữ翻译:交付一个带有类型化修复和类型化拒绝处理的提取管道──

## Vấn đề  vấn đề giới thiệu

Một đại lý đọc email đặt hàng mua cần biến văn bản miễn phí thành `{customer, line_items, total_usd}`Ba cách tiếp cận.

> Một đại lý của một đơn đặt hàng cần phải chuyển đổi văn bản tự do thành `{customer, line_items, total_usd}`❖ 3 cách:

**Approach one: prompt for JSON.**"Câu trả lời trong JSON với các trường khách hàng, line_items, total_usd. " Làm việc 85 đến 95% thời gian trên các mô hình biên giới. thất bại theo sáu cách: không có dấu chấm, dấu ngoặc sau, loại sai, các trường ảo giác, bị cắt ngắn ở giới hạn token, rò rỉ văn bản như "Đây là JSON của bạn:".

> **方法一：提示要求 JSON。**"以 JSON 形式回复,包含字段客户、line_items、total_usd──" trên mô hình tiền tuyến có hiệu quả 85-95% thời gian.

**Approach two: validate after generation.**Tạo tự do, phân tích, xác nhận chống lại schema, thử lại khi thất bại. đáng tin cậy nhưng đắt tiền  bạn trả tiền cho mỗi lần thử lại, và lỗi cắt giảm chi phí thêm một lượt mỗi lần xảy ra.

> **方法二：生成后验证。**tự do tạo, phân tích, theo Schema kiểm tra, thất bại, thử lại.

**Approach three: constrained decoding.**Nhà cung cấp thực thi chương trình trong thời gian giải mã. Các token không hợp lệ được che giấu khỏi phân phối lấy mẫu. Kết quả được đảm bảo để phân tích và đảm bảo để xác nhận. Sự thất bại sụp đổ vào một chế độ: từ chối (chương trình quyết định đầu vào không phù hợp với chương trình).

> **方法三：约束解码。**提供商在解码时强制执行 Schema──无效代币 从采样分布中被屏蔽──输出保证可解析且可验证──失败归结为一种模式:拒绝(模型判定输入不适合 Schema)。

>  **【类比】**约束解码像填空题的"格子"约束──普通生成是写作文,想写写,可能跑题无效 JSON)──约束解码是给你一个表格,每个格子已经标记了"姓名/年龄/邮箱",模型只能在格子里填满应类内容,不会出现"年龄"那填满了"小明"──技术实现: 在每个代币采用时,预先屏蔽掉所有导致 Schema 违规的代币,让概率为零──

> **【中文解读】**Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi: Trò chơi

Mỗi nhà cung cấp biên giới năm 2026 sẽ đưa ra một số cách tiếp cận thứ ba.

> Mỗi nhà cung cấp hàng đầu năm 2026 đã phát hành một số hình thức phương pháp.

- **OpenAI.** `response_format: {type: "json_schema", strict: true}`+`refusal`trong phản ứng nếu mô hình giảm.
  Trung ngữ翻译:**OpenAI。** `response_format: {type: "json_schema", strict: true}`, Nếu mô hình từ chối thì trong phản ứng gia tăng `refusal`
- **Anthropic.**Việc thực thi quy định trên `tool_use`đầu vào; `stop_reason: "refusal"`không phải là một thứ, nhưng `end_turn`Không có công cụ gọi là tín hiệu.
  Trung ngữ翻译:**Anthropic。**Trong `tool_use`输入上强制执行方案;`stop_reason: "refusal"`Không tồn tại, nhưng không có công cụ được sử dụng.`end_turn`Đó là tín hiệu.
- **Gemini.** `responseSchema`theo yêu cầu; vào năm 2026 Gemini sẽ đưa ra các hạn chế ngữ pháp cấp token cho các loại đã chọn.
  Trung ngữ翻译:**Gemini。**Xin cấp độ `responseSchema`Năm 2026, Gemini đã cung cấp một loại ngôn ngữ chuẩn.
- **Pydantic AI.** `output_type=InvoiceModel`phát ra một cấu trúc `RunResult`được đánh dấu theo `InvoiceModel`- Tôi không biết.
  Trung ngữ翻译:**Pydantic AI。** `output_type=InvoiceModel`发发发类型化为`InvoiceModel`       `RunResult`
- **Zod (TypeScript).**Chân tích thời gian chạy xác nhận đầu ra của nhà cung cấp với một chương trình Zod; kết hợp với OpenAI `beta.chat.completions.parse`- Tôi không biết.
  Trung ngữ翻译:**Zod (TypeScript)。**根据Zod Schema 验证提供商输出运行时解析器;与OpenAI 的`beta.chat.completions.parse`配合使用。

Điểm chung: tuyên bố sơ đồ một lần, thực thi nó cuối đến cuối.

> 共同主线: tuyên bố Schema 一次,端到端强制执行──

## Khái niệm cốt lõi

### JSON Schema 2020-12  ngôn ngữ ngoại ngữ

> **【中文解读】**JSON Schema 2020-12 là một Schema 语言 được tất cả các nhà cung cấp đồng ý chấp nhận.`type`(tiêu)`properties`(字段映射)`required`(必填字段)`enum`(枚举值)`minimum`- Không.`maximum`(sự số giá trị)`pattern`(正则约束)等──OpenAI chế độ nghiêm ngặt 额外要求所有属性必须在`required`Trung danh sách, tất cả các cấp độ`additionalProperties: false`、 phải sử dụng chưa được phân tích `$ref`

Mỗi nhà cung cấp chấp nhận JSON Schema 2020-12. Các cấu trúc bạn sử dụng nhiều nhất:

> Mỗi nhà cung cấp đều chấp nhận JSON Schema 2020-12── bạn sử dụng nhiều nhất các cấu trúc:

- `type`: một trong số `object`- `array`- `string`- `number`- `integer`- `boolean`- `null`- Tôi không biết.
  Trung ngữ翻译:`type`- Có thể là:`object``array``string``number``integer``boolean``null`Một trong số đó.
- `properties`: bản đồ tên trường đến phụ đề.
  Trung ngữ翻译:`properties`:字段名到子 Schema 的映射──
- `required`: danh sách tên trường phải xuất hiện.
  Trung ngữ翻译:`required`: phải xuất hiện của字段名列表。
- `enum`: tập hợp các giá trị được phép đóng.
  Trung ngữ翻译:`enum`:允许值的封闭集合──
- `minimum`- `maximum`(tương tự số),`minLength`- `maxLength`- `pattern`(câu)
  Trung ngữ翻译:`minimum`- `maximum`(nhiều giá trị)`minLength`- `maxLength`- `pattern`(字符串)
- `items`: các phụ quy trình áp dụng cho mọi yếu tố array.
  Trung ngữ翻译:`items`: được sử dụng cho mỗi số tử của các mô hình.
- `additionalProperties``false`cấm các trường bổ sung (tầm định thay đổi theo chế độ).
  Trung ngữ翻译:`additionalProperties`- Có thể là:`false`禁止额外字段(默认值因模式而异)

Khóa chế độ khắt khe OpenAI bổ sung ba yêu cầu: mọi tài sản phải được liệt kê trong `required`- `additionalProperties: false`khắp nơi, và không có bất cứ điều gì chưa được giải quyết `$ref`Nếu bạn phá vỡ những thứ này, API sẽ trả lại 400 vào thời điểm yêu cầu.

> OpenAI chế độ nghiêm ngặt  đã tăng ba yêu cầu: mỗi thuộc tính phải được xếp vào`required`Trung ấp tất cả các cấp độ`additionalProperties: false`、 phải sử dụng chưa được phân tích `$ref`Nếu vi phạm các yêu cầu này, API sẽ trả lại 400

> ️ **【易错点】**场景:OpenAI chế độ nghiêm ngặt 下用 Pydantic 的 `Optional[int] = None`/ 后果:API 返回 400 报"Các tính năng bổ sung hoặc yêu cầu" lỗi, vì chế độ nghiêm ngặt  yêu cầu**所有**字段在 `required`, ngay cả khi có thể chọn / 修复:用 `Union[int, None]`Không rõ ràng`required=[..., "field_name"]`; hoặc Pydantic AI framework sẽ tự động xử lý chuyển đổi này; thực tiễn tốt nhất là xác định tất cả các字段都必填, thiếu省值用空字符串/null而非"省略"

### Pydantic, liên kết Python

> **【拓展：Pydantic AI 在结构化输出中的地位】**Pydantic AI là framework Python Agent của năm 2024-2025 , cạnh tranh cốt lõi của nó là sử dụng Pydantic v2 của`model_json_schema()`Bản thân tạo các nhà cung cấp và khả năng Schema── nhà phát triển chỉ cần xác định một `BaseModel`类, framework tự động xử lý chế độ nghiêm ngặt 兼容性、类验证和拒绝处理── theo thống kê, AI của Python trong GitHub năm 2025  tăng trưởng nhanh nhất AI 框架排名三──

Pydantic v2 tạo ra JSON Schema từ các mô hình hình dạng lớp dữ liệu thông qua `model_json_schema()`Pydantic AI gói lại cái này để bạn viết:

> Pydantic v2  thông qua `model_json_schema()`Từ mô hình kiểu dữ liệu tạo ra JSON Schema.

```python
class Invoice(BaseModel):
    customer: str
    line_items: list[LineItem]
    total_usd: Decimal
```

và khung đại lý dịch các kế hoạch vào OpenAI chế độ nghiêm ngặt, Anthropic `input_schema`, hoặc Gemini `responseSchema`Tạo ra mô hình trở lại như một kiểu chữ `Invoice`ví dụ. lỗi xác thực tăng `ValidationError`với các đường lối lỗi nhập.

> Sau đó, đại lý  framework trong边缘将 Schema 翻译为 OpenAI strict mode、Anthropic `input_schema`Hoặc là cặp song sinh`responseSchema`◊ mô hình xuất khẩu để loại hóa `Invoice`例返回──验证错误会引发带有类型化错误路径的 `ValidationError`

### Zod, TypeScript liên kết

Zod (`z.object({customer: z.string(), ...})`(tương đương với TS).`zodResponseFormat(Invoice)`Điều này chuyển thành tải trọng JSON Schema của API.

> Zod (`z.object({customer: z.string(), ...})`(TypScript) là một phần mềm tương đương của TypeScript.`zodResponseFormat(Invoice)`,将其翻译为 API 的 JSON Schema 负载──

### Việc từ chối

Chế độ nghiêm ngặt không thể buộc mô hình trả lời. Nếu đầu vào không phù hợp với sơ đồ ("các email là một bài thơ, không phải một hóa đơn"), mô hình phát ra một `refusal`mã của bạn phải xử lý điều này như một kết quả hạng nhất, không phải là một thất bại. Việc từ chối cũng hữu ích như một tín hiệu an toàn: một mô hình yêu cầu lấy số thẻ tín dụng từ một email có nội dung được bảo vệ trả lại một từ chối với lý do an toàn kèm theo.

> 🤔 **【困惑】**Q: từ chối 算"成功"还是"失败"?**业务成功**,HTTP 200── vì mô hình theo kế hoạch 约定 đưa ra tín hiệu "không thể xử lý" chính xác(không phải lỗi kỹ thuật)── mã hóa lên để đưa nó thành`Result<T, Refusal>`处理:要么走"拒绝分支" (如记录到日志、回归到人工审核),要么再次提示用户──把拒绝当500 错误是新手最常见误判,会导致监控告警噪──


> Định hướng nghiêm ngặt 不能强制模型回答. Nếu输入无法适应 Schema (("邮件是诗歌而非发票"),模型会发出包含原因的`refusal`字段── mã của bạn phải được xử lý như một kết quả công dân cấp nhất, chứ không phải thất bại── từ chối cũng có thể được sử dụng như một tín hiệu an toàn: khi mô hình được yêu cầu rút thẻ tín dụng trong thư bảo vệ nội dung, sẽ trả lại kèm theo lý do an ninh từ chối──

> **【中文解读】**Định hướng nghiêm ngặt 不能强制模型回答──如果输入不能适应 Schema(如"邮件是诗歌而非发票"),模型会发发`refusal`字段── từ chối không phải là thất bại, mà là kết quả trả lại của loại công dân bình đẳng── từ chối cũng có thể được sử dụng như một tín hiệu an toàn: Khi mô hình được yêu cầu rút số thẻ tín dụng từ nội dung được bảo vệ, sẽ trả lại kèm theo lý do an toàn từ chối──

### Việc giải mã hạn chế trong công cộng

> **【拓展：开源约束解码工具对比】**Các công cụ chính bao gồm:`outlines`(GitHub 10k+ sao) dựa trên giới hạn trạng thái tự động cơ quan xây dựng token 掩码;`guidance`(微软出品) `lm-format-enforcer`Thông qua dòng chảy JSON 解析器计算有效下一代币 集合──2026 năm tiến bộ mới nhất là tốc độ của các công cụ này đã gần đến không giới hạn tạo ra, ngắn cấu trúc xuất cảnh thậm chí nhanh hơn(vì đã giảm dung lượng)──

Các triển khai trọng lượng mở sử dụng ba kỹ thuật.

> 开源权重实现使用三种技术──

1. **Grammar-based decoding**(`outlines`- `guidance`- `lm-format-enforcer`): xây dựng một tự động xác định hữu hạn từ sơ đồ; ở mỗi bước, che giấu các logit của các token sẽ vi phạm FSM.
   Trung ngữ翻译:**基于语法的解码**(`outlines``guidance``lm-format-enforcer`): Từ Schema 构建确定性有限自动机; từng bước ngăn chặn sẽ vi phạm các mã thông báo của FSM.
2. **Logit masking with a JSON parser**: chạy trình phân tích JSON trực tuyến theo bước khóa với mô hình; tại mỗi bước, tính toán bộ mã thông báo hợp lệ-nhiều tiếp theo.
   Trung ngữ翻译:**带 JSON 解析器的 Logit 屏蔽**:与模型同步运行流式 JSON 解析器; mỗi bước计算有效的下一代币 集合──
3. **Speculative decoding with a verifier**: mô hình dự thảo rẻ tiền đề xuất token, xác minh thực hiện kế hoạch.
   Trung ngữ翻译:**带验证器的推测解码**:廉价的草稿模型提出代币,验证器强制执行方案──

Các nhà cung cấp thương mại chọn một trong những điều này sau hậu trường.

> Các nhà cung cấp thương mại sau đó chọn một trong số đó.

### Ba chế độ thất bại

1. **Parse error.**Khả năng xuất không hợp lệ JSON. Không thể xảy ra trong chế độ nghiêm ngặt. vẫn có thể xảy ra trên các nhà cung cấp không nghiêm ngặt.
   Trung ngữ翻译:**解析错误。**输出 không hợp lệ JSON;; chế độ nghiêm ngặt 下不可能发生;;非严格 供应商仍可能发生;;
2. **Schema violation.**Các đầu ra phân tích nhưng vi phạm sơ đồ. Không thể xảy ra trong chế độ nghiêm ngặt. phổ biến bên ngoài nó.
   Trung ngữ翻译:**Schema 违规。**输出可解析但违反 Schema;;strict mode 下不可能发生;;在非严格下很常见;;
3. **Refusal.**Mô hình bị giảm, phải được xử lý như một kết quả được đánh dấu.
   Trung ngữ翻译:**拒绝。**模型拒绝──必须作为类型化结果处理──

### Chiến lược thử lại

> **【中文解读】**Không nghiêm ngặt mode 下的恢复模式是"生成→解析→验证→失败则注入错误重试,最多3次"―― thường một lần重试就够了,三次覆盖弱模型的偶然失败――超过三次说明 Schema 设计有问题,需要修改快速或 Schema――

Khi bạn đang ở ngoài chế độ nghiêm ngặt (phương tiện sử dụng nhân đạo, không nghiêm ngặt OpenAI, Gemini cũ), mô hình phục hồi là:

> Khi bạn không ở chế độ nghiêm ngặt 下时(Anthropic tool use、非 nghiêm ngặt OpenAI、旧版 Gemini), phục hồi chế độ là:

```
generate -> parse -> validate -> if fail, inject error and retry, max 3x
```

Một lần thử lại thường đủ. Ba lần thử lại bắt được các mảnh mô hình yếu. Hơn ba là dấu hiệu của một kế hoạch xấu: mô hình không thể thỏa mãn nó cho một số đầu vào, và lời nhắc hoặc kế hoạch cần phải sửa chữa.

> Một lần thử lại thường là đủ. Ba lần thử lại để bao gồm mô hình yếu thất bại.

### Hỗ trợ cho mô hình nhỏ

Việc giải mã hạn chế hoạt động trên các mô hình nhỏ. Một mô hình mở 3B tham số với việc thực thi ngữ pháp vượt trội hơn mô hình 70B tham số với sự thúc đẩy nguyên liệu trong các nhiệm vụ có cấu trúc. Đây là lý do chính khiến các sản phẩm có cấu trúc trở nên quan trọng cho sản xuất: nó tách rời độ tin cậy từ kích thước mô hình.

> 约束解码 cũng áp dụng cho mô hình nhỏ. Một mô hình 3B 参数开源 được bắt buộc theo quy tắc ngôn ngữ, trong nhiệm vụ cấu trúc có thể vượt quá 70B 参数 mô hình.

> **【中文解读】**约束解码 cũng áp dụng cho mô hình nhỏ. Một mô hình nguồn mở của 3B 参数 hợp tác với pháp ngữ pháp, trong nhiệm vụ cấu trúc có thể vượt quá 70B 参数 mô hình.

## Hãy sử dụng nó để thực hiện
```figure
constrained-decoding
```

## Sử dụng nó

`code/main.py`gửi một xác thực viên JSON Schema 2020-12 tối thiểu trong stdlib (loại, yêu cầu, enum, min/max, mẫu, mục, tính năng bổ sung). Nó gói `Invoice`schema và chạy một sản xuất LLM giả thông qua xác thực, chứng minh lỗi phân tích, vi phạm schema và đường từ chối. Thay đổi sản xuất giả cho phản ứng thực sự của bất kỳ nhà cung cấp nào trong sản xuất.

> `code/main.py`提供一个标准库实现的最小JSON Schema 2020-12 验证器(类型、必填、枚举、最小/最大值、模式、item、附加属性) ;;它包装一个`Invoice`Chương trình sẽ không sản xuất một LLM giả  thông qua các hoạt động của các chứng minh, trình diễn giải sai lầm  Chương trình  vi phạm quy định và từ chối đường đi  Trong sản xuất sẽ có một sản xuất giả thay thế cho bất kỳ nhà cung cấp thực sự phản ứng 

Những gì cần xem:

> 需要关注的点:

- Các xác nhận trả lại một gõ `[ValidationError]`danh sách với đường dẫn và tin nhắn. Đó là hình dạng bạn muốn xuất hiện trên yêu cầu thử lại.
  Trung ngữ翻译:验证器 trở lại một loại hóa có đường dẫn và tin nhắn `[ValidationError]`Đây là hình thức mà bạn muốn hiển thị trong bài kiểm tra lại.
- Chiếc nhánh từ chối không thử lại. Nó ghi lại và trả lại một từ chối đã nhập.
  Trung ngữ翻译:拒绝分支不会重试――它记录日志并回归类型化拒绝――Phase 14 · 09 使用拒绝作为安全信号――
- - `additionalProperties: false`kiểm tra lửa trên đầu vào thử nghiệm đối kháng, cho thấy tại sao chế độ nghiêm ngặt đóng cửa cho các trường ảo giác.
  Trung ngữ翻译:`additionalProperties: false`检查在对抗性测试输入上触发, cho thấy tại sao chế độ nghiêm ngặt 关闭幻觉字段的大门.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-structured-output-designer.md`Với mục tiêu khai thác văn bản tự do (phần hóa đơn, vé hỗ trợ, sơ yếu lý lịch, v.v.), kỹ năng tạo ra một JSON Schema 2020-12 tương thích chặt chẽ với chế độ và mô hình Pydantic phản ánh nó, với việc đánh dấu từ chối và xử lý thử lại bị đập vào.

> 本课产 出 `outputs/skill-structured-output-designer.md` Đưa ra một free text 提取目标 (): 发票、支持工单、简历等), kỹ năng này sinh ra một chế độ nghiêm ngặt 兼容 JSON Schema 2020-12 和一个镜像它的Pydantic 模型,并预置类型化拒绝和重试处理──

## Tập luyện bài tập

1. Đi chạy`code/main.py`Thêm một trường hợp thử nghiệm thứ tư mà`total_usd`là một số âm. xác nhận xác nhận từ chối nó với `minimum`đường dẫn hạn chế.
   Trung ngữ翻译:运行 `code/main.py`❖ thêm trường hợp thử nghiệm thứ tư,`total_usd`≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ `minimum`约束路径 từ chối nó.

2. Tăng độ xác nhận để hỗ trợ `oneOf`Một trường hợp phổ biến:`line_item`là một sản phẩm hoặc dịch vụ, được dán nhãn bởi `kind`. chế độ nghiêm ngặt có các quy tắc tinh tế ở đây; kiểm tra hướng dẫn đầu ra có cấu trúc của OpenAI.
   Trung ngữ翻译:扩展验证器以支持带判判器的 `oneOf`❖ Sử dụng thường:`line_item`                                                                                                                                                                                                                                                              `kind`标记──Strict mode 在此有微妙规则;查看 OpenAI's Structured Output Guidance──

3. Viết cùng một sơ đồ hóa đơn như một Pydantic BaseModel và so sánh `model_json_schema()`phát vào sơ đồ xoay tay của bạn. xác định một trường Pydantic đặt theo mặc định mà phiên bản xoay tay bỏ qua.
   中文翻译:将相同的 Faktura Schema 写成 Pydantic BaseModel,比较 `model_json_schema()`输出与手写 Schema──找出 Pydantic 默认设置但手写版本遗漏的字段──

4. Đánh giá tỷ lệ từ chối. Xây dựng mười đầu vào không nên được trích xuất (một bài hát, một bằng chứng toán học, một email trống) và chạy chúng thông qua một nhà cung cấp thực tế với chế độ nghiêm ngặt. Đếm từ chối so với các kết quả ảo giác. Đây là sự thật cơ bản của bạn cho các thử nghiệm từ chối.
   Trung ngữ翻译:测量拒绝率──构构成十个不应可提取的输入(歌词、数学证明、空白邮件), thông qua chế độ nghiêm ngặt của thực tế cung cấp người dùng运行──统计拒绝与幻觉输出量──这是拒绝感知重试的基准事实──

5. Đọc hướng dẫn đầu ra cấu trúc của OpenAI từ trên xuống. Xác định cấu trúc mà nó cấm rõ ràng trong chế độ nghiêm ngặt mà JSON Schema đơn giản cho phép. Sau đó thiết kế một sơ đồ sử dụng cấu trúc cấm không thiết yếu và tái tạo nó để tương thích chặt chẽ.
   Trung ngữ翻译:从头到尾阅读 OpenAI's Structured Output Guidance── tìm ra nó trong chế độ nghiêm ngặt 中明确禁止但普通JSON Schema 允许构建──然后设计一个不必要地使用该禁止构建的 Schema,并重构为严格兼容──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| JSON Schema 2020-12 | "The schema spec" | IETF-draft schema dialect every modern provider speaks | JSON Schema 2020-12 规范 |
| Strict mode | "Guaranteed schema" | OpenAI flag that enforces schema via constrained decoding | 严格模式 |
| Constrained decoding | "Logit masking" | Decode-time enforcement that masks invalid next-tokens | 约束解码 |
| Refusal | "Model declines" | Typed outcome when input cannot fit the schema | 模型拒绝 |
| Parse error | "Invalid JSON" | Output did not parse as JSON; impossible under strict | 解析错误 |
| Schema violation | "Wrong shape" | Parsed but violated types / required / enum / range | Schema 违规 |
| `additionalProperties: false` | "No extras allowed" | Forbids unknown fields; required in OpenAI strict | 禁止额外属性 |
| Pydantic BaseModel | "Typed output" | Python class that emits and validates JSON Schema | Pydantic 基础模型 |
| Zod schema | "TypeScript output type" | TS runtime schema for provider output validation | Zod 类型定义 |
| Grammar enforcement | "Open-weights constrained decode" | FSM-based logit masking, as in outlines / guidance | 语法强制 |

## Xem thêm 延伸阅读

- [OpenAI — Structured outputs](https://platform.openai.com/docs/guides/structured-outputs) chế độ nghiêm ngặt, từ chối và yêu cầu về kế hoạch
  Trung文翻译: chế độ nghiêm ngặt、 từ chối và Schema 要求
- [OpenAI — Introducing structured outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/) Tháng 8 năm 2024: thời gian khởi động giải thích bảo đảm giải mã
  Trung văn翻译:2024 年 8 月发布博文,解释解码保证
- [Pydantic AI — Output](https://ai.pydantic.dev/output/) các liên kết output_type được gõ mà liên kết với mỗi nhà cung cấp
  Trung ngữ翻译:序列化到各供应商的类型化输出_type 绑定
- [JSON Schema — 2020-12 release notes](https://json-schema.org/draft/2020-12/release-notes) quy định quy định
  Trung ngữ翻译:规范权威文档
- [Microsoft — Structured outputs in Azure OpenAI](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs) Thông báo triển khai doanh nghiệp và cảnh báo chế độ nghiêm ngặt
  Trung ngữ翻译:企业部署说明和严格模式 注意事项
