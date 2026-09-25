# MCP Công cụ Hợp đồng và Nội dung . MCP  Công cụ

> Một công cụ là an toàn để tự động hóa chỉ khi phát hiện, lập luận, kết quả, pagination, và vận chuyển metadata đồng ý trên một hợp đồng.

> **【中文解读】**Một công cụ chỉ có khi phát hiện, các tham số, kết quả, phân trang và truyền tải dữ liệu này được chuẩn bị cho cùng một hiệp ước,才适合交付AI tự động调用.

> **【拓展：MCP→真实生产链路】**Đây là 5 lối đối phó với các phân tầng của AI 网关: mô tả 校验 là "công cụ vào" của 网关,`x-mcp-header`镜像 là một phần của các chương trình, và các chương trình được hoàn thành bằng cách tự động.

>  **【前置】**学本课前请先掌握:Phase 13 · 07(MCP 服务器) Phase 13 · 09(MCP 传输:Streamable HTTP 细节) Phase 13 · 10(tài nguyên và yêu cầu, hoàn thành 引用对象来自这里)。

**Type:** Build | **类型:** 动手实践
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lessons 07, 09, and 10 | **前置知识:** Phase 13 · 07、09、10
**Time:** ~120 minutes | **时间:** 约 120 分钟

## Mục tiêu học tập

- Định nghĩa đầu vào và đầu ra công cụ với JSON Schema 2020-12.
  Trung文翻译:用 JSON Schema 2020-12 定义工具的输入和输出──
- Thiết lập kết quả được cấu trúc mà không giả định chúng là các đối tượng JSON.
  Trung ngữ翻译:校验结构化结果, không dự đoán chúng phải là đối tượng JSON.
- Chọn giữa văn bản, hình ảnh, âm thanh, liên kết tài nguyên và các tài nguyên nhúng.
  Trung ngữ翻译: trong văn bản, hình ảnh, âm thanh, nguồn kết nối và nguồn nội dung để lựa chọn.
- Tháo bỏ những thứ không an toàn`x-mcp-header`các định nghĩa trước khi một công cụ đạt đến mô hình.
  Trung ngữ翻译:在不安全的`x-mcp-header`定义 đến khi đạt mô hình trước khi nó từ chối bỏ.
- Mã hóa các giá trị tiêu đề tham số và xác minh sự tương đương chính xác tiêu đề với cơ thể.
  Trung ngữ翻译:对参数-头部值编码,并验证头部与请求体的精确一致性──
- Trải qua trang trình chiếu mà không giải thích các giá trị trình chiếu.
  Trung ngữ翻译:遍历游标分页而不去解释游标的取值──
- Bị ràng buộc và ủy quyền `completion/complete`những đề xuất.
  中文翻译:为 `completion/complete`补全建议设界并做授权──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**Điểm khởi đầu của bài học này: Cần sử dụng Python  hàm là một điều đơn giản, trong khi qua AI  chủ nhà Cần sử dụng năng lực đầu cuối là một vấn đề hợp đồng. Trên mạng có sáu vai trò.

Gọi một chức năng Python là dễ dàng. Gọi một khả năng từ xa thông qua máy chủ AI là một vấn đề hợp đồng.

> 调用一个Python 函数很容易――通过 AI 宿主调用一个远端能力,则是一个契约问题――

Server xuất bản mô tả. Client biến mô tả đó thành mô hình ngữ cảnh và giao diện người dùng. mô hình tạo ra các lập luận. Một cửa cổng có thể định tuyến yêu cầu từ tiêu đề gương. Server thực thi công cụ. Client sau đó quyết định kết quả có đủ an toàn và hợp lệ để quay lại mô hình.

>  máy chủ phát hành mô tả; khách hàng chuyển mô tả thành mô hình trên văn bản và giao diện người dùng; mô hình tạo các tham số;网关可能根据镜头部路由请求; máy chủ thực hiện công cụ; khách hàng tái quyết định kết quả này là đủ an toàn, đủ hiệu quả, có thể trở lại cho mô hình.

Một ranh giới yếu kém làm hỏng toàn bộ chuỗi.

Hãy xem xét năm sự thất bại:

- Mô tả nói kết quả là một đối tượng, nhưng máy chủ trả lại một mảng.
- Khách hàng ngừng trang khi `nextCursor`là một chuỗi trống.
- Một tham số token được phản chiếu vào tiêu đề HTTP và trở nên hiển thị cho người trung gian.
- Một giá trị định tuyến Unicode được gửi như một tiêu đề thô, sau đó cửa ngõ và nguồn gốc giải thích các byte khác nhau.
- Một điểm cuối hoàn thành gợi ý một môi trường sản xuất cho người gọi không thể truy cập nó.

Không có lỗi nào được khắc phục bằng cách yêu cầu tốt hơn.

> Những thất bại này không có một cách nào có thể dựa vào "sự đề xuất tốt hơn" sửa chữa, chúng cần một thỏa thuận rõ ràng và ứng dụng thỏa thuận.`nextCursor`为空字符串时客户端停止分页;toke 参数 được chiếu vào HTTP 头并对中间人可见;Unicode 路由值以原始头发送导致网关和源站解释不同的字节;补全端点向无权访问调用者建议生产环境;;)

## Đường ống hợp đồng.

> **【中文解读】**Để mỗi lần dùng vào xem như 5 lối: tìm thấy: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 准入: 

Hãy coi mỗi cuộc gọi công cụ như 5 cổng:

1. **Discover.**Đọc một danh sách các công cụ xác định, trang.
2. **Admit.**Thiết lập từng mô tả và áp dụng chính sách an ninh địa phương.
3. **Invoke.**Thiết lập các lập luận và xây dựng metadata vận tải.
4. **Execute.**Đưa ra bộ xử lý và phân loại lỗi đúng cách.
5. **Consume.**Thiết lập các khối nội dung và đầu ra có cấu trúc trước khi sử dụng mô hình.

```figure
mcp-contract-pipeline
```

Nhà máy chủ sở hữu các cổng nhập và tiêu thụ. Một máy chủ không thể buộc khách hàng tin tưởng vào các chú thích, sơ đồ hoặc đầu ra của nó.

## JSON Schema là một rantime boundary .

> **【中文解读】**Trong MCP 2026-07-28,`inputSchema`和 `outputSchema`Đó là JSON Schema,`$schema`缺省时方言默认 2020-12──三个要点:(1) 无参工具也应声明 `{"type":"object","additionalProperties":false}`,比裸 `{"type":"object"}`更严;(2) 服务器 khi phát hành outputSự án, bao gồm `isError: true`Trong mỗi kết quả hoàn chỉnh phải trở lại phù hợp với quy hoạch này.`structuredContent` 错标志只分类执行结果,不豁免输出契约;

Trong MCP `2026-07-28`- `inputSchema`và `outputSchema`sử dụng JSON Schema.`$schema`không có, phương ngữ mặc định là 2020-12.

> Trong MCP `2026-07-28`Trung,`inputSchema`Với`outputSchema`Sử dụng JSON Schema`$schema`缺失时默认方言 là 2020-12。

Các giao thức đầu vào phải là một đối tượng schema. Một công cụ không có lập luận vẫn nên nói chính xác những gì nó chấp nhận:

```json
{
  "type": "object",
  "additionalProperties": false
}
```

Đây là nghiêm khắc hơn `{ "type": "object" }`, chấp nhận các tính chất tùy tiện.

Một sơ đồ đầu ra là tùy chọn. Một khi một máy chủ xuất bản một, mỗi công cụ hoàn chỉnh
kết quả cam kết trả lại phù hợp `structuredContent`, bao gồm kết quả
với `isError: true`. Lập cờ lỗi phân loại kết quả thực hiện; nó không
từ bỏ hợp đồng sản xuất được công bố. Khách hàng nên xác nhận kết quả thay vào đó
của tin tưởng vào mô tả.

> 输出 schema là có thể chọn. Một khi máy chủ phát hành nó, mỗi kết quả hoàn chỉnh của công cụ đều cam kết trở lại phù hợp với schema `structuredContent`包括 `isError: true`Kết quả:  Đấu hiệu sai chỉ phân loại kết quả thực hiện, không miễn trừ kết quả xuất bản đã được phát hành:  Khách hàng phải kiểm tra kết quả, chứ không phải là mô tả tín nhiệm: 

### Nội dung được cấu trúc là bất kỳ giá trị JSON nào 

Đừng mã cứng `structuredContent`như một từ điển.

- một đối tượng;
- một mảng;
- một dây;
- một số;
- một boolean;
- `null`- Tôi không biết.

Công cụ này trả về một mảng:

```json
{
  "name": "tag_catalog",
  "inputSchema": {
    "type": "object",
    "additionalProperties": false
  },
  "outputSchema": {
    "type": "array",
    "items": {"type": "string"}
  }
}
```

Kết quả thành công của nó là hợp lệ:

```json
{
  "resultType": "complete",
  "content": [
    {
      "type": "text",
      "text": "[\"contracts\", \"mcp\", \"stateless\"]"
    }
  ],
  "structuredContent": ["contracts", "mcp", "stateless"],
  "isError": false
}
```

Để tương thích, kết quả có cấu trúc cũng nên bao gồm JSON được phân phối theo chuỗi trong khối văn bản.`structuredContent`- Phải.

> Để phù hợp, kết quả cấu trúc cũng nên được mang theo JSON được sắp xếp trong một khối văn bản.`structuredContent`才是.

### Một người xác nhận nhỏ vẫn dạy giới hạn. Một máy kiểm tra nhỏ cũng có thể dạy giới hạn này.

Bài học sử dụng một bộ phụ tập JSON Schema cố ý vì nó ở trong thư viện tiêu chuẩn Python. Nó kiểm tra các cơ chế được sử dụng bởi các công cụ mẫu:

> 本课刻意使用一个 JSON Schema 子集, để giữ trong Python 标准库之内.`additionalProperties: false`、数组 items、enum 取值、字符串最小长度──它不是完整生产校验器的替代品可复用课程要点是"校验发生在哪里":descriptor 在发现后、参数在执行之前、结构化结果在消费之前──

- Các loại đối tượng, mảng, chuỗi, số nguyên, số, boolean và null;
- các tính chất cần thiết;
- `additionalProperties: false`-
- các mục array;
- giá trị enum;
- Độ dài dây tối thiểu.

Đây không phải là một thay thế cho một xác thực sản xuất hoàn chỉnh. Bài học tái sử dụng là nơi xác thực xảy ra: sau khi phát hiện cho mô tả, trước khi thực hiện cho các lập luận, và trước khi tiêu thụ cho kết quả cấu trúc.

## Các khối nội dung có chi phí khác nhau.

> **【中文解读】** `content`数组可以混合五种内容块:text(人和模型可读的摘要,当作不可信输出对待) 图像(base64 视觉证据,校验媒体类型和大小) 音频(base64 语音,校验媒体类型和时长) 资源_link(一个 URI 引用,客户端跟随它时要重新过资源授权) 资源(直接内嵌的数据,当场执行负载和内容上限) 选择原则:大件或独立变化的东西链接省一次往返的负载;必须与结果原子同行的小证据才内嵌.

- `content`array có thể kết hợp nhiều loại nội dung.

| Type | Use it for | Main boundary |
|------|------------|---------------|
| `text` | Human and model-readable summaries | Treat text as untrusted output |
| `image` | Visual evidence encoded as base64 | Validate media type and size |
| `audio` | Spoken or recorded output encoded as base64 | Validate media type and duration limits |
| `resource_link` | A URI the client may fetch later | Reauthorize the later resource read |
| `resource` | Data embedded directly in the result | Enforce payload and content limits now |

Một liên kết tài nguyên không phải là bằng chứng cho thấy tài nguyên xuất hiện trong `resources/list`. Nó là một tham chiếu được trả lại bởi tool call này. Khách hàng vẫn áp dụng chính sách tài nguyên của mình khi nó theo dõi URI.

> 资源链接 không chứng minh tài nguyên này hiện tại `resources/list`里; nó chỉ là một trích dẫn của công cụ này để sử dụng trở lại.

Một tài nguyên nhúng tránh một chuyến đi quay lại khác nhưng làm tăng kích thước phản ứng hiện tại. Sử dụng liên kết cho các hiện vật lớn hoặc tự động thay đổi. Sử dụng tài nguyên nhúng cho các bằng chứng nhỏ phải đi theo nguyên tử với kết quả.

> Trong đó, các nguồn tài nguyên được sử dụng để kết nối với các phần tử khác nhau, nhưng sẽ tăng lên.

Bài học là `evidence_bundle`kết quả bao gồm cả năm loại. Khách hàng xác nhận từng khối trước khi chấp nhận kết quả.

## `x-mcp-header`- Định hướng dữ liệu siêu dữ liệu.`x-mcp-header`là đường dẫn của dữ liệu

> **【中文解读】** `inputSchema`Các thuộc tính của nó có thể được tuyên bố.`x-mcp-header`, khách hàng trong Streamable HTTP để chuyển các tham số này`Mcp-Param-{name}`头──目的:让负载均衡、网关或策略引擎不解析 JSON 体就能路由; nó không được放凭证的地方──规范约束(全部失败闭):头名非空且符合HTTP字段名语法、大小写不敏感地唯一、属性类型只能是字符串/整数/boolean(禁止号码)`inputSchema.properties`Các thuộc tính của vật thể,`oneOf`分支, các mặt hàng`$ref`引到的定义、output schema 中一律拒绝) 整数必须在 JavaScript 安全整数范围内.`password`- Không.`secret`- Không.`token`- Không.`api_key`- Không.`authorization`等名字的描述符 直接拒绝──审计记录头名,不记录值──

Một tài sản bên trong`inputSchema`có thể tuyên bố `x-mcp-header`. Trên Streamable HTTP, client phản ánh lập luận đó vào `Mcp-Param-{name}`- Tôi không biết.

```json
{
  "region": {
    "type": "string",
    "x-mcp-header": "Region"
  }
}
```

Với `region: "eu-west"`, vận chuyển có thể phát ra:

```http
Mcp-Param-Region: eu-west
```

Các ghi chú tồn tại để một bộ cân bằng tải, cửa khẩu hoặc công cụ chính sách có thể định tuyến mà không phân tích cơ thể JSON.

Các giao thức hạn chế ghi chú:

- Tên tiêu đề không trống và tuân theo cấu trúc mã mã mã tên trường HTTP;
- Tên tiêu đề là duy nhất bất kể trường hợp;
- loại thuộc tính là chuỗi, số nguyên hoặc boolean;
- `number`không được phép;
- ghi chú chỉ xuất hiện trên một thành viên trực tiếp của `inputSchema.properties`-
- giá trị nguyên số ở trong `-9007199254740991`qua `9007199254740991`- Tôi không biết.

Quy tắc vị trí là tổng hợp và không bị đóng.
không chỉ các tính chất xác thực viên của bạn hiểu.
ghi chú dưới một đối tượng `properties`, một `oneOf`nhánh,`items`, một
định nghĩa đạt được bởi `$ref`, hoặc bất kỳ sơ đồ đầu ra nào.
không biến nút tham chiếu thành một thuộc tính cấp cao trực tiếp.

> 位置规则是语法性的且失败关闭――要穿越整个 schema 树,而不仅仅是你的校验器恰恰认识的那部分属性――嵌套对象的`properties``oneOf`- Đúng rồi.`items`、经 `$ref`Đến đến định nghĩa và bất kỳ sự ghi chép trong bất kỳ sơ đồ xuất đều phải từ chối  giải quyết một trích dẫn không đưa các nút được trích dẫn thành thuộc tính trực tiếp trên tầng.

Bài học này thêm một chính sách triển khai: từ chối mô tả phản ánh tên như `password`- `secret`- `token`- `api_key`, hoặc`authorization`Các thông số chính thức khuyên các tác giả máy chủ không thể phản ánh các thông số nhạy cảm.

Kiểm tra tên tiêu đề, không phải giá trị của nó.`Mcp-Param-Region`trong khi giữ `eu-west`ra khỏi sự kiện kiểm toán.

### Mã hóa giá trị trước khi xây dựng HTTP tiêu đề  xây dựng HTTP đầu trước khi mã hóa giá trị

Một giá trị tham số chỉ có thể đi như văn bản đơn giản khi nó là một chuỗi không trống
của các ký tự ASCII có thể nhìn thấy từ `!`qua `~`và không giống như
Tất cả mọi thứ khác đều sử dụng hình thức này:

> Chỉ khi một giá trị tham số là`!`Đến`~`Các chữ cái có thể nhìn thấy được trong ASCII không có kích thước trống, không giống như mã hóa, để chuyển tiếp bằng văn bản; phần còn lại của các chữ cái có thể nhìn thấy được trong ASCII.`=?base64?`开头的值) 都编码为 `=?base64?{Base64UTF8}?=` đối với nguyên bản UTF-8 字节 làm tiêu chuẩn cơ sở64,编码前不剪、不归归一化、不替换。 đối với "长得像哨兵" giá trị tái编码 một lần, chính là người nhận có thể trả lại nguyên bản gốc chữ chứ không phải là như là truyền tải 语法解码的关键──Bộ 染为小写`true`- Không.`false`; số nguyên được đặt theo hệ thống và phải nằm trong phạm vi toàn số an toàn của JavaScript, giá trị bên ngoài phạm vi trực tiếp từ chối thay vì để người trung gian vào bốn bên.

```text
=?base64?{Base64UTF8}?=
```

`Base64UTF8`là base64 tiêu chuẩn trên các byte UTF-8 chính xác. Đừng cắt,
làm bình thường, hoặc thay thế giá trị trước.
tab, ký tự điều khiển, CR hoặc LF, không gian trắng dẫn hoặc sau, và bất kỳ
giá trị bắt đầu với `=?base64?`. Mã hóa một giá trị trông như Sentinel một lần nữa là
điều gì cho phép người nhận lấy lại văn bản gốc theo nghĩa đen thay vì giải mã
nó như là tổng hợp vận tải.

Tóm lại là chữ nhỏ `true`hoặc `false`. Số nguyên được hiển thị trong cơ sở 10 và
phải ở trong phạm vi toàn số an toàn của JavaScript. Giá trị bên ngoài phạm vi đó
được từ chối thay vì được tròn bởi một người trung gian.

### Máy chủ kiểm tra bản sao gương 服务器校验镜像副本

Tạo tiêu đề chỉ là một nửa của client.
máy chủ phải:

> Trong giới hạn HTTP được phát trực tuyến, máy chủ phải: không phân biệt tên gọi`Mcp-Param-*`Name; existence时解码精确的base64 哨兵形式;把解码文本与 JSON体中对应参数进行精确比较; 在分发之前拒绝缺失、重复、意外、形或不匹配的已识别头──拒绝方式是 HTTP`400`加 JSON-RPC 错误码 `-32020`, và trong hồ sơ kiểm toán chỉ có tên đã được xác định và loại từ chối, không có giá trị của nó cũng không có hình thức mã hóa của nó.

1. tìm được công nhận `Mcp-Param-*`Tên không tính đến trường hợp tên tiêu đề;
2. mã hóa hình thức sentinel base64 chính xác khi có mặt;
3. so sánh văn bản được giải mã với lập luận cơ thể JSON tương ứng chính xác;
4. từ chối một vật bị mất tích, trùng lặp, không mong đợi, sai dạng hoặc không phù hợp
   đầu được nhận ra trước khi gửi.

Việc từ chối là HTTP `400`với mã lỗi JSON-RPC `-32020`- Không phải là
giá trị cơ thể cũng như hình thức tiêu đề được mã hóa của nó không thuộc về hồ sơ kiểm toán.
Chỉ có tên tiêu đề được công nhận và danh mục từ chối.

`code/main.py`mô hình ranh giới này trực tiếp. [Lesson 09](../../09-mcp-transports/)
bao gồm các lệnh xác thực HTTP Streamable rộng hơn, bao gồm phương pháp và
Phân điểm giao thức- phiên bản.

## Các bài viết trên trang web không rõ ràng

> **【中文解读】**MCP danh sách hoạt động tác dụng 游标分页:页大小和游标格式由服务器定,客户端只有一个决定`nextCursor`否为`None`                                                                                                                                                                                                                                                              `if not result.get("nextCursor")`):空字符串是合法游标,真值判断会提前翻完──正确写法只判 `is None` Khách hàng phải giải mã, tăng lên, so sánh với các biểu tượng cũ, sắp xếp hoặc xác định các biểu tượng.`-32602`

MCP sử dụng các hoạt động danh sách trang trang. máy chủ chọn kích thước trang và định dạng trình chiếu. Client nhận được một quyết định:

```python
if result.get("nextCursor") is None:
    break
cursor = result["nextCursor"]
```

Đừng viết như thế này:

```python
if not result.get("nextCursor"):
    break
```

Một chuỗi trống là một trình chỉ dẫn hợp lệ. Sự thật sẽ dừng lại quá sớm.

> 空字符串 là một biểu tượng hợp pháp.

Khách hàng không được giải mã một trình chiếu, tăng nó, so sánh nó với một trình chiếu trước đó để đặt hàng, hoặc suy luận một số trang. Một máy chủ có thể ký một trình chiếu, gắn nó với một phiên bản danh mục, hoặc lập bản đồ cho trạng thái riêng tư. Đó là chi tiết thực hiện của máy chủ.

Máy chủ mẫu cố ý trả lại `""`Sau trang đầu tiên. khách hàng phải gửi giá trị chính xác trên yêu cầu thứ hai.

```text
<first request with no cursor>
<second request with cursor "">
```

Các trình chiếu không hợp lệ tạo ra các tham số không hợp lệ JSON-RPC, mã `-32602`- Tôi không biết.

## Kết thúc là một bề mặt được ủy quyền.

> **【中文解读】** `completion/complete`Để nhanh chóng 参数和资源模板参数 cung cấp đầy đủ lời khuyên. Nó rất hữu ích đối với biểu đồ giao tiếp, nhưng có thể tiết lộ danh sách thông thường 方法保护起来的名字`development`和 `staging`, chỉ có người điều hành mới có thể thấy`production` nguyên tắc: đối với việc bổ sung toàn bộ bộ bộ yêu cầu sử dụng và được trích dẫn prompt / nguồn lực tương tự giới hạn quyền hạn.

`completion/complete`cung cấp các gợi ý cho các lập luận nhanh chóng và lập luận mẫu tài nguyên. Nó hữu ích cho các biểu mẫu tương tác, nhưng nó có thể rò rỉ tên mà các phương pháp danh sách thông thường bảo vệ.

Một yêu cầu hoàn thành nêu tên tham chiếu và lập luận được hoàn thành:

```json
{
  "method": "completion/complete",
  "params": {
    "ref": {
      "type": "ref/prompt",
      "name": "deployment_review"
    },
    "argument": {
      "name": "environment",
      "value": "st"
    }
  }
}
```

Kết quả trả lại tối đa 100 giá trị và có thể báo cáo `total`+`hasMore`- Tôi không biết.

Sử dụng cùng ranh giới ủy quyền được sử dụng bởi prompt hoặc nguồn tham khảo.`development`và `staging`Chỉ có một người vận hành mới có thể nhận được`production`- Tôi không biết.

Việc hoàn thành sản xuất cũng cần:

- xác thực đầu vào;
- lọc thông tin cho người gọi;
- yêu cầu khai báo cho khách hàng;
- giới hạn tốc độ trong máy chủ;
- số kết quả bị giới hạn;
- Các nhật ký không tiết lộ các giá trị gợi ý nhạy cảm.

Hoàn thành là hỗ trợ, không phải là khám phá.

## Hai lớp sai lầm.

> **【中文解读】**协议错误与工具执行错误必须分开. MCP 请求无法正确分发时使用 JSON-RPC 错误(未知工具名、请求形形形、缺请求元数据、游标无效);调用已到达工具、工具报告可行动的失败时,使用`isError: true`Kết quả của các công cụ hoàn chỉnh. Nếu một công cụ tuyên bố một kế hoạch xuất, thất bại của một hành động có thể được xây dựng trong kế hoạch đó.`route_report`                                                                                                                                                                                                                                                              `accepted: false`, với người có thể đọc được sai văn bản và `isError: true`

Giữ lỗi giao thức tách biệt với lỗi thực hiện công cụ.

Sử dụng lỗi JSON-RPC khi yêu cầu MCP không thể được gửi đúng:

- Tên công cụ không rõ;
- hình dạng yêu cầu bị biến dạng;
- Mẫu dữ liệu yêu cầu bị thiếu;
- Cursor không hiệu quả.

Sử dụng kết quả công cụ đầy đủ với `isError: true`Khi cuộc gọi đến công cụ và công cụ báo cáo một lỗi có thể xử lý:

- nguồn báo cáo không có sẵn;
- một ngày nằm ngoài phạm vi hỗ trợ;
- một quy tắc kinh doanh từ chối hoạt động yêu cầu.

Các mô hình thường có thể sửa lỗi thực hiện công cụ. Họ không thể sửa chữa một máy chủ vi phạm sơ đồ đầu ra của riêng mình.

Nếu công cụ tuyên bố một sơ đồ đầu ra, mô hình một lỗi có thể thực hiện bên trong đó
Chế độ.`route_report`thất bại trả lại khu vực yêu cầu của nó với
`accepted: false`, bên cạnh văn bản lỗi có thể đọc được bởi con người và `isError: true`- Tôi không biết.

## Hãy xây dựng nó.

> **【中文解读】** `code/main.py`Sử dụng Python  chuẩn库 đồng thời thực hiện biên giới hai bên ∙ bên máy chủ: từng yêu cầu MCP 元 dữ liệu 验验、带工具与完成 能力的`server/discover`、 xác định `tools/list`分页、四个工具描述器(một trong số đó phải được từ chối) √数组结构化输出、全部五种内容块类型、解码已识别参数头并不匹配时返回 HTTP `400`+ JSON-RPC `-32020`                                                                                                                                                                                                                                                              `x-mcp-header`位置校验和敏感字段策略、精确的明文可见 ASCII 或 base64 UTF-8 编码、能跟随空字串的不透明游标循环、参数与结果校验、内容块校验、只含有名称无含值的审计事件──那个刻意不安全的描述器是教学数据:证明一个被拒绝的工具不妨碍其他合法工具加载──

`code/main.py`xây dựng cả hai bên của ranh giới với thư viện tiêu chuẩn Python.

Các máy chủ thực hiện:

- xác thực các siêu dữ liệu MCP theo yêu cầu;
- `server/discover`có khả năng hoàn thành và sử dụng các công cụ;
- xác định `tools/list`Paging;
- bốn mô tả công cụ, bao gồm một mô tả phải bị từ chối;
- đầu ra cấu trúc array;
- mỗi loại khối nội dung công cụ hiện tại;
- một cổng tương đương HTTP được phát trực tuyến giải mã các tiêu đề tham số được công nhận và
  trả lại HTTP `400`cộng với JSON-RPC `-32020`khi không phù hợp;
- hoàn thành được phép và giới hạn tốc độ.

Khách hàng thực hiện:

- Nhận phép sử dụng mô tả;
- cây đầy ắp`x-mcp-header`xác thực vị trí và chính sách lĩnh vực nhạy cảm;
- mã hóa giá trị UTF-8 chính xác-ASCII hoặc base64,
- một vòng trục trình chiếu không minh bạch theo một chuỗi trống;
- lập luận và xác nhận kết quả;
- xác thực khối nội dung;
- các sự kiện kiểm toán tiêu đề có tên nhưng không có giá trị.

Các mô tả vô tình không an toàn là dữ liệu giảng dạy. Nó chứng minh rằng một công cụ bị từ chối không ngăn chặn các công cụ hợp lệ tải.

## Hãy sử dụng nó. Hãy học cách sử dụng nó.

Từ nguồn kho:

```bash
cd phases/13-tools-and-protocols/28-mcp-tool-contracts-and-content/code
python3 main.py
python3 -m unittest discover tests -v
```

Các bản in demo công cụ được chấp nhận, mô tả bị từ chối, cả hai trang
yêu cầu, nội dung mảng cấu trúc, loại khối nội dung, tiêu đề gương
tên, cho dù giá trị được yêu cầu mã hóa, trạng thái độ tương đương HTTP, và
giá trị hoàn thành được lọc theo người gọi.

## - Bác sĩ, tôi đã làm việc trong phòng thí nghiệm tương tác.

> **【中文解读】**Các thử nghiệm của các bước 10 không phải là hình dạng JSON, mà là một sự thất bại trong "những biên giới của nó".`tag_catalog.outputSchema.type`改成 `object`Xem khách hàng từ chối trả lại số;让首页 `nextCursor` giữ `""`Xem biểu tượng dấu vết; Giữ chữ cái thuộc tính thêm `x-mcp-header: "Authorization"`看准入拒绝; dùng Unicode,换行,首尾空格,字面`=?base64?SGVsbG8=?=`试编码回环;把注解挪进 `oneOf`- Không.`items`- Không.`$ref`Xem toàn bộ cây thông qua; thay đổi hoặc xóa đã nhận dạng đầu nhìn HTTP  biên giới trở lại `400`+ `-32020`

Mở ra`code/main.py`và tìm vị trí `TOOLS`- Tôi không biết.

1. Thay đổi`tag_catalog.outputSchema.type`từ `array`đến`object`- Tôi không biết.
2. Chạy demo. Khách hàng nên từ chối array trả lại.
3. Khôi phục lại kế hoạch.
4. Hãy giữ trang đầu tiên `nextCursor`như `""`, sau đó làm cho trang cuối cùng trở lại
   `nextCursor: None`thay vì bỏ qua trường.
5. Thực hiện các xét nghiệm và so sánh dấu vết của trình chiếu.
6. Thêm `x-mcp-header: "Authorization"`đến một thuộc tính dây.
7. Đáp định mô tả xác nhận nhận từ chối nó trước khi gọi.
8. Hãy thử`region`các giá trị chứa Unicode, một dòng mới, không gian xung quanh, và
   văn bản theo nghĩa đen `=?base64?SGVsbG8=?=`. Khóa mã mỗi tiêu đề phát ra và chứng minh
   giá trị ban đầu tồn tại chính xác.
9. Di chuyển ghi chú dưới `oneOf`- `items`, hoặc một `$ref`Định nghĩa.
   mỗi mô tả bị từ chối ngay cả khi nhánh đó không bao giờ được sử dụng bởi demo.
10. Tắt tiêu đề được công nhận hoặc thay đổi giá trị giải mã của nó.
    Status return boundary `400`và mã JSON-RPC `-32020`- Tôi không biết.

Ý tưởng không phải là ghi nhớ hình dạng JSON mà là xem mỗi cổng thất bại ở biên giới mà nó sở hữu.

## Phòng thí nghiệm tập luyện.

Tăng cường phòng thí nghiệm hợp đồng với một `search_evidence`công cụ.

> 给契约实验扩展一个 `search_evidence`工具──九条要求:(1) 输入 schema 接受 `query``limit`Và một sự an toàn `region`路由字段;(2) 输出 schema 是含 `uri``title``score`Các đối tượng số;(3) 结果包含兼容文本和每项一个资源链接;(4) 参数拒绝未知属性;(5) `limit`) Không được phép truy cập một số URI người dùng không bao giờ có thể qua hoàn chỉnh hoặc công cụ xuất phát để xem nó; 7) ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ `400`+ `-32020`

Yêu cầu:

1. Các quy trình đầu vào của nó chấp nhận `query`- `limit`, và một cái khoá`region`trường định tuyến.
2. Chế độ đầu ra của nó là một mảng các đối tượng với `uri`- `title`, và`score`- Tôi không biết.
3. Kết quả bao gồm văn bản tương thích và một liên kết tài nguyên cho mỗi mục.
4. Các lập luận bác bỏ các tính chất không rõ.
5. `limit`được giới hạn bởi sự xác thực ứng dụng.
6. Một người gọi không truy cập vào một URI không bao giờ thấy URI đó thông qua hoàn thành hoặc công cụ đầu ra.
7. Các bài kiểm tra bao gồm điểm không phù hợp, ghi chú tiêu đề không hợp lệ và danh sách hai trang.
8. Các bài kiểm tra giá trị tiêu đề bao gồm ASCII, Unicode, ký tự điều khiển hiển thị,
   không gian trắng, văn bản trông như sentinel, và cả hai là các giới hạn toàn số an toàn JavaScript.
9. Thiết bị HTTP chấp nhận tên tiêu đề không nhạy cảm với trường hợp nhưng từ chối mất
   hoặc không phù hợp với các giá trị được công nhận với trạng thái `400`và mã `-32020`- Tôi không biết.

## Thuật vật được vận chuyển.

`outputs/skill-mcp-contract-reviewer.md`là một kỹ năng đánh giá bằng phẳng, có thể sử dụng lại. Cho nó một mô tả công cụ, kết quả mẫu, hành vi trang và chính sách hoàn thành. Nó trả lại một quyết định nhập học, kế hoạch xác thực kết quả, chính sách tiêu đề và các thử nghiệm thất bại cụ thể.

> `outputs/skill-mcp-contract-reviewer.md`Đó là một kỹ năng đánh giá bình thường có thể lặp lại: cho nó một mô tả công cụ, kết quả mẫu, hành vi phân trang và chiến lược bổ sung, nó sẽ quay lại vào quyết định, kết quả của kế hoạch kiểm tra, chiến lược đầu và thử nghiệm thất bại cụ thể.

## Hãy kiểm tra.

> **【中文解读】**验收清单要逐条过:`tools/list`重复调用顺序稳定;`nextCursor`Vì vậy`""`Khi khách hàng sẽ gửi lần thứ hai yêu cầu; cảm giác tiêu đề mô tả được loại bỏ và các công cụ khác có thể sử dụng; số组 qua số组 schema、 đối tượng không qua; kết quả sai không thể bỏ qua hoặc vi phạm được phát hành schema;五种内容块全部通过校验;审计事件只名没有值;明文保持明文、其余值经base64 UTF-8 精确往返;安全整数范围之外的整数被拒绝;藏在`oneOf`- Không.`items`/đồng vật/`$ref`/ xuất nhập trong schema được từ chối trong giai đoạn nhập; lớn viết không nhạy cảm đã nhận ra tên chỉ được thông qua khi giải mã giá trị chính xác với thể, nếu không `400`+ `-32020`; bổ sung của nhà phân tích không bao giờ trở lại `production`; Tool fail us `isError: true`,形协议调用 JSON-RPC `error`

Bài học hoàn thành khi những câu nói sau đây là đúng:

- `tools/list`trả lại cùng một thứ tự logic cho các cuộc gọi lặp đi lặp lại.
- Khách hàng thực hiện yêu cầu thứ hai khi `nextCursor`là `""`- Tôi không biết.
- Các mô tả tiêu đề nhạy cảm không an toàn được loại trừ trong khi các công cụ khác vẫn có sẵn.
- Một mảng vượt qua sơ đồ đầu ra mảng của nó.
- Một đối tượng thất bại trong cùng một sơ đồ array.
- Kết quả lỗi không thể bỏ qua hoặc vi phạm một sơ đồ đầu ra được xuất bản.
- Văn bản, hình ảnh, âm thanh, liên kết tài nguyên và khối tài nguyên nhúng xác thực.
- Các sự kiện kiểm toán tiêu đề chứa tên và không có giá trị.
- ASCII hiển thị đơn giản vẫn đơn giản; Unicode, kiểm soát, đệm, trống, và
  giá trị trông như sentinel đi lại qua mã hóa chính xác base64 UTF-8.
- Các số nguyên được phản chiếu bên ngoài phạm vi an toàn JavaScript được từ chối.
- Các ghi chú dưới `oneOf`- `items`, vật thể đốn,`$ref`các định nghĩa, hoặc
  Các chương trình sản xuất được từ chối trong thời gian nhập học.
- Tên tiêu đề được công nhận không nhạy cảm với trường hợp chỉ được thông qua khi giá trị được giải mã
  chính xác phù hợp với cơ thể; các bản sao bị thiếu hoặc không phù hợp tạo ra HTTP `400`
  và JSON-RPC `-32020`- Tôi không biết.
- Việc phân tích hoàn thành không bao giờ trở lại `production`- Tôi không biết.
- Một lỗi công cụ sử dụng `isError: true`; một cuộc gọi giao thức bị hình thành sai sử dụng JSON-RPC `error`- Tôi không biết.

## Các chế độ sản xuất thất bại

> │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │

| Failure | What the learner sees | Correct response |
|---------|-----------------------|------------------|
| Client assumes object output | Valid arrays fail or are silently wrapped | Validate against the published schema without object-only types |
| Empty cursor treated as false | Final pages disappear | Continue whenever `nextCursor` is present and non-null |
| Sensitive value mirrored | Secret appears in proxy, WAF, or trace data | Reject the descriptor and keep secrets in protected request data |
| Raw Unicode or whitespace mirrored | Gateway and origin disagree or the value is normalized | Use exact base64 UTF-8 sentinel encoding and compare after decoding |
| Annotation hidden in a schema branch | A client misses routing metadata during admission | Traverse the entire schema tree and allow only direct top-level properties |
| Large integer mirrored | JavaScript intermediary rounds the routing value | Reject values outside the JavaScript safe integer range |
| Header and body disagree | Gateway routes one target while the origin executes another | Reject before dispatch with HTTP `400` and JSON-RPC `-32020` |
| Output schema ignored | Downstream code consumes corrupt structure | Validate before model or application use |
| Resource link trusted automatically | Caller follows an unauthorized URI | Reauthorize every resource read |
| Completion shares global suggestions | Hidden tenant names leak | Filter by caller, reference, and authorization |
| Tool annotations treated as policy | Destructive operation bypasses confirmation | Enforce authorization and approval outside annotations |
| One malformed tool breaks discovery | Entire server becomes unavailable | Reject the bad descriptor and admit valid tools independently |

## Kết nối Capstone.

Bạch đá cuối giai đoạn 13 cần một cổng thông tin có thể hợp nhất các công cụ từ nhiều máy chủ. Bài học này cung cấp lõi nhập học của nó.

> Giai đoạn 13  Dự án tốt nghiệp cần một kết nối có thể kết hợp nhiều công cụ máy chủ, khóa học này cung cấp cho nó một trung tâm tiếp cận. Sử dụng nó để phân chia bốn chứng chỉ tốt nghiệp: xác định và đầy đủ phân đoạn phát hiện, mô hình phát hiện trước mô tả, kiểm tra, kiểm tra kết quả cấu trúc kết quả cộng với các khối nội dung có giới hạn, giữ cho giới hạn ủy quyền bổ sung và các đường dẫn dữ liệu. Không chỉ với một lần thành công.`tools/call`Về tuyên bố 网关兼容  cần bắt được mô tả 分页 痕迹 进入工具集 拒绝工具集 和一个已经验结果──

Sử dụng hiện vật để phân loại bốn mảnh bằng chứng đáy đầu:

- phát hiện xác định và trang hoàn chỉnh;
- xác thực mô tả trước khi tiếp xúc với mô hình;
- Kết quả kết quả có cấu trúc được xác nhận cộng với các khối nội dung bị giới hạn;
- hoàn thành và định tuyến metadata giữ cho giới hạn ủy quyền.

Đừng tuyên bố tương thích của gateway từ một thành công `tools/call`Chỉ riêng. chụp mô tả, truy cập trang, bộ công cụ được chấp nhận, bộ công cụ bị từ chối, và một kết quả được xác nhận.

## Từ khóa  Keyword

| Term | Meaning |
|------|---------|
| `inputSchema` | JSON Schema object defining accepted tool arguments |
| `outputSchema` | Optional JSON Schema defining `structuredContent` |
| `structuredContent` | Any JSON value produced by a tool result |
| Content block | Typed text, image, audio, resource link, or embedded resource |
| `x-mcp-header` | Schema annotation that mirrors a primitive argument into Streamable HTTP metadata |
| Opaque cursor | Server-issued pagination token whose value the client does not interpret |
| Completion reference | Prompt name or resource URI/template whose argument is being completed |
| Admission | Client decision to expose or reject a discovered descriptor |

## Xem thêm 延伸阅读

- [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [MCP Completion](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/completion)
- [MCP Pagination](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/pagination)
- [MCP Streamable HTTP Parameter Headers](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http#custom-headers-from-tool-parameters)
