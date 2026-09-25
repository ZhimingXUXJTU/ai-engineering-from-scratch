# OpenTelemetry GenAI  Công cụ theo dõi gọi kết thúc đến kết thúc  OpenTelemetry GenAI:端到端追踪工具调用

> Một đại lý gọi 5 công cụ, 3 máy chủ MCP và 2 đại lý phụ. Anh cần một dấu vết trên tất cả. Các quy ước ngữ nghĩa OpenTelemetry GenAI (chế độ liên tục ổn định trong v1.37 trở lên) là tiêu chuẩn 2026, được hỗ trợ bởi Datadog, Langfuse, Arize Phoenix, OpenLLMetry và AgentOps. Bài học này nêu tên các thuộc tính cần thiết, đi qua hệ thống phân cấp thời gian (agent -> LLM -> tool), và gửi một máy phát phát sóng thời gian stdlib bạn có thể kết nối với bất kỳ nhà xuất khẩu OTel nào.

> **【中文解读】**Trình độ:: 0x5 (từ 1 đến 2), 0x5 (từ 1 đến 3), 0x5 (từ 1 đến 5), 0x5 (từ 1 đến 5), 0x5 (từ 1 đến 5), 0x5 (từ 1 đến 5), 0x5 (từ 1 đến 5), 0x5 (từ 1 đến 5), 0x5 (từ 1 đến 5), 0x5 (từ 1 đến 5), 0x5 (từ 1 đến 5), 0x5 (từ 1 đến 5), 0x5 (từ 1 đến 6), 0x5 (từ 1 đến 7), 0x5 (từ 1 đến 7), 0x5 (từ 1 đến 7), 0x5 (từ 1 đến 7), 0x5 (từ 1 đến 7), 0x5 (từ 1 đến 7), 0x5 (từ 1 đến 7), 0x5 (từ 1 đến 7), 0x5 (từ 1 đến 7 đến 7), 0x5 (từ 1 đến 7 đến 7), 0x5 (từ 1 đến 7 đến 7), 0x5 (từ 1 đến 7 đến 7 đến 7), 0x5 (từ 1 đến 7 đến 7 đến 7), 0x5 (từ 1 đến 7 đến 7 đến 7 đến 7), 0x5 (từ 1 đến 7 đến 7 đến 7 đến 7), 0x5 (từ 1 đến 7 đến 7 đến 7 đến 7 đến 7 đến 7), 0x5 (từ 7 đến 7 đến 7 đến 7 đến 7 đến 7 đến 7), 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

> **【拓展】**OpenTelemetry là AI  ứng dụng từ thử nghiệm hướng tới sản xuất cơ sở hạ tầng quan sát thiết yếu.

>  **【前置】**学本节前请先掌握:(1) Bước 13·07、08(MCP server/client) 要在MCP 调用上加 span;(2) OpenTelemetry 基础(trace、span、span context、exportor);(3) 分布式追踪概念(trace_id、span_id、parent_id);(4) W3C traceparent 头格式跨进程上下文传播──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, OTel span emitter) | **语言:** Python (stdlib, OTel span emitter)
**Prerequisites:** Phase 13 · 07 (MCP server), Phase 13 · 08 (MCP client) | **前置知识:** Phase 13 · 07 (MCP server), Phase 13 · 08 (MCP client)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Đề xuất các thuộc tính OTel GenAI cần thiết cho một khoảng thời gian LLM và một khoảng thời gian thực hiện công cụ.
  Trung文翻译:命名 LLM span 和工具执行 span 的必需 OTel GenAI 属性──
- Xây dựng một hệ thống phân cấp theo dõi bao gồm vòng tròn đại lý, LLM gọi, tool gọi, và MCP khách hàng gửi.
  Trung文翻译:构建覆盖 Agent 循环、LLM 调用、工具调用和 MCP 客户端分发的痕迹层次──
- Quyết định nội dung nào để chụp (tự chọn) vs chỉnh sửa (tầm định).
  Trung文翻译:决定捕获哪些内容(opt-in) Vs 脱敏(默认) 』
- Giả phát các đoạn văn cho một người thu thập địa phương (Jaeger, Langfuse) mà không cần viết lại mã công cụ.

> **【中文解读】**Mục tiêu học tập: nắm bắt các thuộc tính thiết yếu của OTel GenAI (LLM span và tool execution span); xây dựng bao gồm Agent 循环、LLM 调用、工具调用和 MCP 客户端分发的痕迹层级; quyết định nắm bắt nội dung nào (opt-in) vs 脱敏(默认); gửi span đến bộ sưu tập địa phương。

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**调试场景: người dùng báo cáo"Công viên có thời gian 30 giây phản ứng, có thời gian 3 giây"── không theo dõi,日志 chỉ hiển thị LLM 调用,看不到工具分发、MCP 服务器往返、子 代理── cuối cùng phát hiện ra một máy chủ MCP  lạnh khởi động đôi khi bị mắc kẹt── không có kết thúc theo dõi là không thể phát hiện ra những vấn đề như vậy──

Một lỗi từ tháng 2 năm 2026: người dùng báo cáo "trong thời gian đại lý của tôi phải trả lời 30 giây; thời gian khác 3 giây". Không có dấu vết. Các nhật ký cho thấy cuộc gọi LLM, nhưng không phải việc gửi công cụ, không phải chuyến đi trở lại của máy chủ MCP, không phải là đại lý phụ. Bạn đoán. Cuối cùng bạn sẽ thấy: một máy chủ MCP đôi khi bị treo trên một khởi động lạnh.

> 2026 年 2 月调试: người dùng báo cáo"My Agent 有时 30秒响应; 有时 3秒"──无追踪──日志显示 LLM 调用,但不显示工具分发、MCP 服务器往返、子 Agent──你猜测──最终你发现:一个MCP 服务器在冷启动时偶尔卡住──

Không có việc theo dõi từ đầu đến cuối, bạn không thể tìm thấy điều này.

> Không có dấu vết, bạn không tìm thấy nó.

>  **【类比】**分布式追踪像快递的"物流单号"──你寄一个包裹(user 请求),途经多个中转站(agent → LLM → tool → MCP server),每个站点扫一次单号(生成一个跨度)──最后你能看到一个时间线:"9:01 寄出 → 9:02 收件 → 9:05 分拣 → 9:30 转运 → 9:45 送"──OTel GenAI 是快递公司约定的"扫码字段标准"每家公司(Datadog/Langfuse) 都都相同字段(gen_ai.operation.name等)记录,所以你换物流公司时不需要重新贴单.──

Các quy ước được giải quyết trong năm 2025-2026 dưới nhóm các quy ước ngữ nghĩa OpenTelemetry. Họ xác định tên thuộc tính ổn định để Datadog, Langfuse, Phoenix, OpenLLMetry và AgentOps tất cả phân tích cùng một khoảng thời gian.

> 约定在 2025-2026年在 OpenTelemetry 语义约定组下稳定──它们定义稳定属性名称,使 Datadog、Langfuse、Phoenix、OpenLLMetry 和 AgentOps 都解析相同的跨度──一次仪表化;发送到任何后端──

## Khái niệm cốt lõi

> **【中文解读】**本节详解 span 层次结构(agent.invoke_agent -> llm.chat -> tool.execute -> mcp.call) 、必需属性(gen_ai.* 命名空间) 、span 类型(CLIENT/INTERNAL) 、opt-in 内容捕获、span 事件、导出器、跨 MCP 传播、指标和 AgentOps 层。

### Tỷ lệ bậc của Span

> **【中文解读】**Span 层次:agent.invoke_agent(顶层 INTERNAL span) -> llm.chat(CLIENT span) -> tool.execute(INTERNAL) -> mcp.call(CLIENT span)―整个结构嵌套在一个追踪 id 下,span id 链接父子关系。

```
agent.invoke_agent  (top, INTERNAL span)
 ├── llm.chat       (CLIENT span)
 ├── tool.execute   (INTERNAL)
 │    └── mcp.call  (CLIENT span)
 ├── llm.chat       (CLIENT span)
 └── subagent.invoke (INTERNAL)
```

Tất cả đều nằm dưới một danh tính, và các danh tính liên kết mối quan hệ giữa cha mẹ và con cái.

> 整套嵌套在一个痕迹 id 下。Span id 链接父子关系。

> ️ **【易错点】**场景:跨进程调用 MCP server 时不传 traceparent / 后果: khách户端的追踪 在 MCP 调用处断裂,看到的是"tool.execute 100ms 完成",但看不到 MCP server 内部到底卡在哪;多个独立的追踪 无法串联 / 修复:(1) HTTP 调用 MCP 时在头加`traceparent: 00-<trace_id>-<span_id>-01`;(2) Studio MCP Đặt theo dõi ngữ cảnh 序列化 thành JSON-RPC `params._meta.trace_context`;(3) 接收端取出文 续接 span──没有上下文传播,分布式追踪就是空话──

> 🤔 **【困惑】**Q: trong khoảng thời gian 里 nên ghi lại đầy đủ nhanh chóng và phản ứng ư?**不记录**, chỉ ghi nhớ độ dài và số điểm:**隐私**quan 含用户敏感信息;(2) **存储成本** lượng lớn yêu cầu trong toàn bộ lượng ghi chép sẽ làm cho dấu vết  hậu端 lưu trữ nổ;**合规**GDPR/CCPA  yêu cầu tối thiểu hóa thu thập dữ liệu `gen_ai.content.capture=full`才记录,且加密存储 + 短期 TTL。

### Các thuộc tính cần thiết

Theo kỳ kết 2025-2026,:

- `gen_ai.operation.name` `"chat"`- `"text_completion"`- `"embeddings"`- `"execute_tool"`- `"invoke_agent"`- Tôi không biết.
  Trung ngữ翻译:`gen_ai.operation.name`操作名(`"chat"``"text_completion"``"embeddings"``"execute_tool"``"invoke_agent"`(■)
- `gen_ai.provider.name` `"openai"`- `"anthropic"`- `"google"`- `"azure_openai"`- Tôi không biết.
  Trung ngữ翻译:`gen_ai.provider.name` cung cấp thương nhân
- `gen_ai.request.model` chuỗi mô hình yêu cầu (ví dụ: `"gpt-4o-2024-08-06"`().
  Trung ngữ翻译:`gen_ai.request.model`请求的模型字符串──
- `gen_ai.response.model` mô hình thực sự phục vụ.
  Trung ngữ翻译:`gen_ai.response.model` thực tế dịch vụ mô hình:
- `gen_ai.usage.input_tokens`- `gen_ai.usage.output_tokens`- Tôi không biết.
  Trung ngữ翻译:`gen_ai.usage.input_tokens`- `gen_ai.usage.output_tokens` nhập/output token số.
- `gen_ai.response.id` ID phản ứng nhà cung cấp để tương quan.
  Trung ngữ翻译:`gen_ai.response.id` nhà cung cấp ứng dụng ID 用于关联。

Đối với các vòng tròn công cụ:

> Đối với thời gian sử dụng:

- `gen_ai.tool.name` Định dạng công cụ.
  Trung ngữ翻译:`gen_ai.tool.name`工具标识符──
- `gen_ai.tool.call.id` danh tính gọi cụ thể.
  Trung ngữ翻译:`gen_ai.tool.call.id` cụ thể调用 id。
- `gen_ai.tool.description` mô tả công cụ (không tùy chọn).
  Trung ngữ翻译:`gen_ai.tool.description`工具描述(可选)。

Đối với các đại lý:

> Đối với thời gian hoạt động của đại lý:

- `gen_ai.agent.name`- `gen_ai.agent.id`- `gen_ai.agent.description`- Tôi không biết.
  Trung ngữ翻译:`gen_ai.agent.name`- `gen_ai.agent.id`- `gen_ai.agent.description`Công viên 名/id/描述。

### Loại Span

- `SpanKind.CLIENT`cho các cuộc gọi vượt qua ranh giới quy trình (chuyên bố LLM, máy chủ MCP).
  Trung ngữ翻译:`SpanKind.CLIENT`Sử dụng trong quá trình biên giới của调调用 (LLM 提供商, MCP 服务器)
- `SpanKind.INTERNAL`cho các bước vòng lặp của đại lý và thực hiện công cụ.
  Trung ngữ翻译:`SpanKind.INTERNAL`Sử dụng để thực hiện các bước và công cụ của chính đại lý.

### Tải nội dung chọn nhượng

Theo mặc định, các khoảng thời gian mang theo các số liệu và thời gian không phải yêu cầu hoặc hoàn thành.`OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`và các môi trường thu thập nội dung cụ thể để bao gồm nội dung.

> 默认情况下,span 携带标标和计时而不是快速或补全;;`OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`Và các nội dung cụ thể nắm bắt biến đổi môi trường để chứa nội dung.

### Các sự kiện trên các span

Các sự kiện cấp token có thể được thêm vào như các sự kiện trải dài:

> Token 级事件可作为 span 事件添加:

- `gen_ai.content.prompt` thông điệp nhập.
  Trung ngữ翻译:`gen_ai.content.prompt`输入消息──
- `gen_ai.content.completion` thông điệp xuất phát.
  Trung ngữ翻译:`gen_ai.content.completion`输出消息──
- `gen_ai.content.tool_call` gọi công cụ như ghi lại.
  Trung ngữ翻译:`gen_ai.content.tool_call`记录的工具调用──

Các sự kiện theo thời gian trong một khoảng thời gian để lặp lại chi tiết.

> Sự kiện trong khoảng thời gian trong thời gian, được sử dụng để phân tích chi tiết.

### Các nhà xuất khẩu

OTel mở rộng xuất khẩu sang:

- **Jaeger / Tempo.**OSS, tại chỗ.
  Trung ngữ翻译:**Jaeger / Tempo。**开源,本地部署
- **Langfuse.**LLM-observability-specific; hình dung việc sử dụng token.
  Trung ngữ翻译:**Langfuse。**LLM 可观测性专用;可视化代币 使用──
- **Arize Phoenix.**Evals + tracing kết hợp.
  Trung ngữ翻译:**Arize Phoenix。**评估+ theo dõi结合──
- **Datadog.**Thương mại; phân tích bản địa `gen_ai.*`thuộc tính.
  Trung ngữ翻译:**Datadog。**商业;原生解析 `gen_ai.*`属性.
- **Honeycomb.**Chuẩn cho cột; thân thiện với truy vấn.
  Trung ngữ翻译:**Honeycomb。**列式存储;查询友好。

Tất cả đều nói OTLP, định dạng điện thoại.

> Tất cả đều nói là OTLP, 线格式.

### Sự lan truyền trên MCP

Khi một khách hàng MCP gọi cho một máy chủ, tiêm tiêu đề theo dõi W3C vào yêu cầu. Streamable HTTP hỗ trợ tiêu đề tiêu chuẩn. Stdio không mang tiêu đề HTTP bản địa; bản đồ đường bộ 2026 của quy định thảo luận thêm một `_meta.traceparent`trường trên các cuộc gọi JSON-RPC.

> Khi MCP 客户端调用服务器, sẽ W3C traceparent 头注入请求──Streamable HTTP 支持标准头──studio 原生不携带 HTTP 头;规范 2026 路线图讨论在 JSON-RPC 调用上添加 `_meta.traceparent`字段。

Cho đến khi tàu: bao gồm các dấu vết trong `_meta`của mỗi yêu cầu bằng tay. Server ghi lại ID theo dõi.

> Cho đến khi đó: "Hàn tay trong mọi yêu cầu"`_meta`中包含 traceparent──服务器记录 trace id──

### Métrics

Bên cạnh các khoảng thời gian, GenAI semconv xác định các số liệu:

> Ngoài khoảng cách ngoài, GenAI 语义约定定义指标:

- `gen_ai.client.token.usage` HISTogram.
  Trung ngữ翻译:`gen_ai.client.token.usage`直方图──
- `gen_ai.client.operation.duration` HISTogram.
  Trung ngữ翻译:`gen_ai.client.operation.duration`直方图──
- `gen_ai.tool.execution.duration` HISTogram.
  Trung ngữ翻译:`gen_ai.tool.execution.duration`直方图──

Sử dụng chúng cho bảng điều khiển không cần chi tiết mỗi cuộc gọi.

> Sử dụng những điều này không cần phải sử dụng các thiết bị trong bảng.

### Lớp AgentOps

AgentOps (tạo ra năm 2024) chuyên về khả năng quan sát GenAI. Nó bao gồm các khung phổ biến (LangGraph, Pydantic AI, CrewAI) để phát ra các khoảng OTel tự động. hữu ích nếu chồng của bạn sử dụng một khung hỗ trợ; sử dụng công cụ thủ công nếu không.

> AgentOps(2024 năm thành lập) chuyên về GenAI 可观测性──它包装流行框架(LangGraph、Pydantic AI、CrewAI) tự động phát hành OTel span──如果你的技术使用支持的框架则有用;否则使用手动仪表化──

## Hãy sử dụng nó để thực hiện

> **【中文解读】** `code/main.py`hướng đến  phát ra OTLP-JSON format span, bao gồm một Agent 调用 LLM、分发两个工具、进行一次MCP 往返──无真导出器课程聚焦跨 形状和属性集──关注点:trace id 跨所有跨 跨 跨 共享;父子链接通过 parentSpanId 编码;`gen_ai.*`Ứng dụng được hoàn thành; Content Capture默认关闭──
```figure
t3-span-waterfall
```

## Sử dụng nó

`code/main.py`phát ra các bước dài hình OTel để stdout (trong định dạng OTLP-JSON) cho một đại lý gọi LLM, gửi hai công cụ, và thực hiện một chuyến đi về và về của MCP. Không có nhà xuất khẩu thực sự  bài học tập trung vào hình dạng và thuộc tính tập hợp. Paste đầu ra vào một người xem OTLP tương thích hoặc chỉ đọc nó.

> `code/main.py`Đối với các công cụ khác nhau, các công cụ này được sử dụng để tạo ra các mô hình và các mô hình khác nhau.

Những gì cần xem:

- Đồ nhận dạng dấu vết được chia sẻ trên tất cả các phạm vi.
  中文翻译:Trace id 跨所有 span 共享──
- Các liên kết cha mẹ-con được mã hóa qua `parentSpanId`- Tôi không biết.
  Trung ngữ翻译:父子链接通过 `parentSpanId`编码.
- Cần `gen_ai.*`thuộc tính được lấp đầy.
  Trung ngữ翻译:必需的`gen_ai.*`属性已填充──
- Việc ghi lại nội dung là mặc định; một kịch bản bật nó qua env var.
  Trung文翻译:内容捕获默认关闭;一个场景通过环境变量开启──

## Chuyển nó đi.

> **【中文解读】**本课产 出 `outputs/skill-otel-genai-instrumentation.md` Định lập trình 代码库, tạo trình tự hóa kế hoạch:  添加跨度,填充哪些属性,目标导出器,

Bài học này sẽ mang lại kết quả `outputs/skill-otel-genai-instrumentation.md`Với một cơ sở mã đại lý, kỹ năng tạo ra một kế hoạch công cụ: nơi để thêm phạm vi, thuộc tính để dân cư, và những người xuất khẩu để nhắm mục tiêu.

> 本课产 出 `outputs/skill-otel-genai-instrumentation.md` Đặt tài liệu của đại lý, kỹ năng này sinh ra kế hoạch thiết bị hóa:

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đếm khoảng thời gian và xác định là ai là khách hàng đối với nội bộ.
   Trung ngữ翻译:运行 `code/main.py`◊ Mức độ tính toán và xác định những gì là khách hàng vs nội bộ.

2. Khởi động chụp nội dung (env var) và xác nhận `gen_ai.content.prompt`và `gen_ai.content.completion`Các sự kiện xuất hiện.
   Trung文翻译:开启内容捕获(环境变量)并确认 `gen_ai.content.prompt`和 `gen_ai.content.completion`Sự kiện xuất hiện.

3. Thêm metric tool-execution `gen_ai.tool.execution.duration`và phát ra nó như một mẫu histogram mỗi cuộc gọi.
   中文翻译:添加工具执行指标 `gen_ai.tool.execution.duration`Không được sử dụng mỗi lần như một mẫu hình trực tiếp xuất phát.

4. Chuyển một người mẹ theo dõi từ một đại lý mẹ trải dài vào yêu cầu MCP `_meta.traceparent`kiểm tra máy chủ MCP sẽ thấy ID theo dõi tương tự.
   Trung文翻译:将 traceparent 从父代理 span 传播到MCP 请求的 `_meta.traceparent`字段──验证 MCP 服务器 nhìn thấy identic dấu vết──

5. Đọc các mô hình semconv của OTel GenAI. Xác định một thuộc tính được liệt kê trong semconv mà mã bài học này KHÔNG phát ra. Thêm nó.
   Trung ngữ翻译:阅读 OTel GenAI 语义约定规范──识别语义约定中列出但本课代码未发出一个属性──添加它──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| OTel | "OpenTelemetry" | Open standard for traces, metrics, logs | 开放遥测标准 |
| GenAI semconv | "GenAI semantic conventions" | Stable attribute names for LLM / tool / agent spans | GenAI 语义约定 |
| `gen_ai.*` | "The attribute namespace" | All GenAI attributes share this prefix | GenAI 属性命名空间 |
| Span | "Timed operation" | A unit of work with a start, end, and attributes | Span：带属性的时间操作单元 |
| Trace | "Cross-span ancestry" | Tree of spans sharing a trace id | Trace：跨 span 的追踪树 |
| SpanKind | "CLIENT / SERVER / INTERNAL" | Hints about span direction | Span 类型：跨进程/同进程 |
| OTLP | "OpenTelemetry Line Protocol" | Wire format for exporters | OTLP：导出器线格式 |
| Opt-in content | "Prompt / completion capture" | Off by default; env var to enable | 内容捕获：默认关闭 |
| traceparent | "W3C header" | Propagates trace context across services | traceparent：跨服务追踪传播 |
| Exporter | "Backend-specific shipper" | Component that sends spans to Jaeger / Datadog / etc. | 导出器：发送到后端 |

## Xem thêm 延伸阅读

- [OpenTelemetry — GenAI semconv](https://opentelemetry.io/docs/specs/semconv/gen-ai/) các quy ước kinh điển cho các phạm vi, métrics và sự kiện của GenAI
  Trung ngữ翻译:GenAI span、指标和事件的权威约定
- [OpenTelemetry — GenAI spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/) Danh sách các thuộc tính của LLM và thời gian thực hiện công cụ
  Trung ngữ翻译:LLM 和工具执行 span 属性列表
- [OpenTelemetry — GenAI agent spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/) cấp đại lý `invoke_agent`span
  Trung ngữ翻译:Công viên 级 `invoke_agent`span
- [open-telemetry/semantic-conventions — GenAI spans](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-spans.md) Nguồn tin được lưu trữ trên GitHub
  Trung ngữ翻译:GitHub 托管的真相源
- [Datadog — LLM OTel semantic convention](https://www.datadoghq.com/blog/llm-otel-semantic-convention/) Lối tích hợp sản xuất
  Trung ngữ翻译:生产集成演练
