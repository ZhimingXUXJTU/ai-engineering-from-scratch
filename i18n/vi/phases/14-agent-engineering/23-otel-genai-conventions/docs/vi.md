# OpenTelemetry GenAI Semantic Conventions 约定 GenAI METR

> OpenTelemetry's GenAI SIG (được ra mắt vào tháng 4 năm 2024) xác định các quy trình tiêu chuẩn cho điện toán đại lý. Tên của span, thuộc tính và các quy tắc nắm bắt nội dung hội tụ giữa các nhà cung cấp vì vậy dấu vết đại lý có nghĩa là cùng một điều trong Datadog, Grafana, Jaeger và Honeycomb.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 24 (Observability Platforms) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Mục tiêu học tập

- Tên gọi các loại phạm vi GenAI: mô hình/thành khách, đại lý, công cụ.
- Nhận ra sự khác biệt`invoke_agent`KLIENT vs INTERNAL và khi nào mỗi ứng dụng.
- Đăng danh tính cấp cao nhất của GenAI: tên nhà cung cấp, mô hình yêu cầu, ID nguồn dữ liệu.
- Giải thích hợp đồng thu thập nội dung: chọn tham gia, `OTEL_SEMCONV_STABILITY_OPT_IN`, khuyến nghị tham chiếu bên ngoài.

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**Mỗi nhà cung cấp đều phát minh ra tên tuổi của riêng mình, vận tải và đội hình cuối cùng cần phải xây dựng một bảng thiết bị độc lập cho mỗi khung.

Mỗi nhà cung cấp phát minh ra tên miền riêng của họ. nhóm Ops kết thúc xây dựng bảng điều khiển theo khung. OpenTelemetry's GenAI SIG sửa chữa điều này bằng cách xác định một tiêu chuẩn các mục tiêu toàn bộ hệ sinh thái.

> Mỗi nhà cung cấp đều phát minh ra phạm vi riêng của mình 名称――运维团队 cuối cùng cần xây dựng một bảng thiết bị độc lập cho mỗi khung hình―― OpenTelemetry's GenAI SIG 通过定义一个全生态系统遵循的标准来解决这个问题――

> **【拓展：OTel GenAI 规范的跨平台统一】**OpenTelemetry GenAI 语义约定 (2024年4月启动) 定义 Agent 遥测的标准方案:span 名称、属性和内容捕获规则跨供应商统一,使 Agent 追踪在 Datadog、Grafana、Jaeger 和 Honeycomb 中具有相同语义──一次埋点,多后端通用──

>  **【前置】**Học本节前请先掌握:Phase 14·01(Agent Loop)你需要先有 Agent才能给它埋点;Phase 14·13(LangGraph)理解状态图,因为 span 的父子层级就是图遍历的镜像──如果完全没有接触过OpenTelemetry(不知道什么是 span、trace、语境传播),先看OTel 官方 Python 快速进入本节只讲 GenAI 专属约定,不重讲 OT基础 ⋅

## Khái niệm cốt lõi

### Các loại span

>  **【类比】**3 loại phạm vi của OTel GenAI 像医院的分级诊疗记录:**Model span**là thử nghiệm đơn nhất, ghi lại "từ máu nhiều như thế nào"", dùng những thiết bị nào"", kết quả nhiều như thế nào"**Agent span**门诊病历 (门诊病历)                                                                                                                                                                                                                                                         **Tool span**Đây là một chương trình kiểm tra.`parent_span_id`链回父记录这样 Datadog 里你能展开看: toàn bộ Đại diện 调用 → 5 lần 工具调用 → Mỗi lần 工具调用里 2 lần LLM 调用。

1. **Model / client spans.**Bao gồm các cuộc gọi LLM nguyên liệu. Được phát hành bởi các SDK của nhà cung cấp (Anthropic, OpenAI, Bedrock) và các bộ chuyển đổi mô hình khung.
2. **Agent spans.** `create_agent`(khi đại lý được xây dựng) và `invoke_agent`(Khi nó chạy).
3. **Tool spans.**Một cho mỗi công cụ gọi; kết nối với khoảng thời gian đại lý bởi mối quan hệ cha mẹ-cháu.

### Tên gọi của đại lý span

- Tên tiếng Tây Ban Nha: `invoke_agent {gen_ai.agent.name}`nếu có tên; fallback đến `invoke_agent`- Tôi không biết.
- Loại Span:
  - **CLIENT** cho các dịch vụ đại lý từ xa (OpenAI Assistants API, Bedrock Agents).
  - **INTERNAL** cho các khung đại lý trong quá trình (LangChain, CrewAI, ReAct địa phương).

### Các thuộc tính chính

- `gen_ai.provider.name` `anthropic`- `openai`- `aws.bedrock`- `google.vertex`- Tôi không biết.
- `gen_ai.request.model` Đơn vị nhận dạng mẫu.
- `gen_ai.response.model` mô hình được giải quyết (có thể khác với yêu cầu do định tuyến).
- `gen_ai.agent.name` Định danh đại lý.
- `gen_ai.operation.name` `chat`- `completion`- `invoke_agent`- `tool_call`- Tôi không biết.
- `gen_ai.data_source.id` cho RAG: các cơ sở hoặc cửa hàng đã được tham khảo.

Các công nghệ cụ thể có các quy ước cho Anthropic, Azure AI Inference, AWS Bedrock, OpenAI.

> OpenTelemetry GenAI 语义约定 đã xác định các tiêu chuẩn quan sát được của LLM 和 Agent.`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`Đúng vậy.

### Tải nội dung

> ️ **【易错点】**场景: nhà phát triển 图省事在`invoke_agent`span 里把完整提示(含用户 PII、API key、客户合同条款) như thuộc tính 直接塞进去 → 后果:运维在Jaeger 网页里点开就能看到所有明文,Datadog还会索引做全文检索,等于把合规风险扩散到整个观测链路 → 修复:默认关闭内容捕获,需要时只在 span 里存指针 ID如`gen_ai.input.message_id=row42`),原文落到带 ACL của đối tượng lưu trữ S3 里,运维要查时通过 ID 跳转授权访问──这就是本节反复强调的"những khuyến nghị tham chiếu bên ngoài"──

Quy tắc mặc định: các thiết bị không nên ghi vào / ra ra mặc định.

> OpenTelemetry GenAI 语义约定 đã xác định các tiêu chuẩn quan sát được của LLM 和 Agent.`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`Đúng vậy.

- `gen_ai.system_instructions`
- `gen_ai.input.messages`
- `gen_ai.output.messages`

Mô hình sản xuất được khuyến cáo: lưu trữ nội dung bên ngoài (S3, lưu trữ nhật ký của bạn), ghi lại tham chiếu trên khoảng thời gian (tín chỉ ID, không phải văn bản). Đây là phòng thủ độc chứa bài học 27 được kết nối với khả năng quan sát.

> 推的生产模式:将内容外存储(S3、你的日志存储),在 span 上记录引用(指针 ID,不是原文) .

> OpenTelemetry GenAI 语义约定 đã xác định các tiêu chuẩn quan sát được của LLM 和 Agent.`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`Đúng vậy.

### Thường độ ổn định

Hầu hết các hội nghị là thử nghiệm từ tháng 3 năm 2026.

> OpenTelemetry GenAI 语义约定 đã xác định các tiêu chuẩn quan sát được của LLM 和 Agent.`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`Đúng vậy.

```
OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental
```

Datadog v1.37+ bản đồ GenAI gán bản địa vào sơ đồ LLM Observability của mình.

> 🤔 **【困惑】**Q: `invoke_agent`span 什么时候标客户端,什么时候标内部?看起来很绕着── A: 看被调用的代理不是"另一个进程/服务"── Nếu trực tiếp trong Python 进程 nhập LangChain 运行一个 ReAct,这是 INTERNAL你的自己代码内的子调用── Nếu bạn调调 OpenAI Assistants API hoặc AWS Bedrock Agents, đó là cách xa HTTP 调用,标客户端──CLIENT span cũng sẽ tự động mang RPC 相关属性如(`rpc.system``rpc.service`), tiện lợi và truyền thống

> Datadog v1.37+ 原生将 GenAI 属性映射到其LLM Observability schema──其他后端(Grafana、Honeycomb、Jaeger) hỗ trợ thuộc tính nguyên thủy──

> OpenTelemetry GenAI 语义约定 đã xác định các tiêu chuẩn quan sát được của LLM 和 Agent.`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`Đúng vậy.

### Khi mô hình này đi sai

- **Capturing full prompts in spans.**PII, bí mật, dữ liệu khách hàng trong các dấu vết mà các ops có thể đọc.
- **No `gen_ai.provider.name`.**Các bảng điều khiển đa nhà cung cấp bị hỏng khi thuộc tính bị thiếu.
- **Spans without parent links.**Những công cụ mồ côi luôn truyền bá bối cảnh.
- **Not setting stability opt-in.**Các thuộc tính của bạn có thể được đổi tên trong nâng cấp backend.

> **在 span 中捕获完整提示。**运维可以读取的追踪包含PII、密钥、客户数据──外部存储──
> **缺少 `gen_ai.provider.name`。**缺少归属时,多供应商仪表盘会出错.
> **没有父链接的 span。**孤立的工具 span──始终传播上下文──
> **不设置稳定性选择加入。**Các thuộc tính của bạn có thể được đặt tên lại khi nâng cấp sau đó.

## Hãy xây dựng nó.
```figure
ae-genai-span-tree
```

## Hãy xây dựng nó

`code/main.py`thực hiện một emiter bán kính stdlib phù hợp với các quy ước GenAI:

> OpenTelemetry GenAI 语义约定 đã xác định các tiêu chuẩn quan sát được của LLM 和 Agent.`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`Đúng vậy.

- `Span`với schema thuộc tính GenAI.
- `Tracer`với `start_span`, các bối cảnh tổ hợp.
- Một nhân viên kịch bản chạy phát ra: `create_agent`- `invoke_agent`(INTERNAL), mỗi công cụ trải dài, `chat`thời gian cho các cuộc gọi LLM.
- Một chế độ chụp nội dung lưu trữ các lời nhắc bên ngoài và ghi nhận ID trên khoảng thời gian.

Đi đi.

```
python3 code/main.py
```

Kết quả: một cây span với tất cả các thuộc tính GenAI cần thiết, và một "bảo lưu bên ngoài" cho thấy các tham chiếu nội dung chọn vào.

> 输出: một chứa tất cả các cần thiết GenAI 属性 span 树, cũng như một hiển thị chọn để tham gia nội dung引用的"外部存储"

> OpenTelemetry GenAI 语义约定 đã xác định các tiêu chuẩn quan sát được của LLM 和 Agent.`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`Đúng vậy.

## Hãy sử dụng nó để thực hiện

- **Datadog LLM Observability**(v1.37+) thuộc tính bản địa của bản đồ.
- **Langfuse / Phoenix / Opik**(Dân học 24)  tự động dụng cụ hệ sinh thái.
- **Jaeger / Honeycomb / Grafana Tempo** dấu vết OTel nguyên liệu; xây dựng bảng điều khiển từ thuộc tính GenAI.
- **Self-hosted** chạy bộ sưu tập OTel với bộ xử lý GenAI.

## Chuyển nó đi.

`outputs/skill-otel-genai.md`cáp OTel GenAI mở rộng sang một đại lý hiện có với các mặc định ghi nội dung và lưu trữ tham chiếu bên ngoài.

> `outputs/skill-otel-genai.md`Để mở rộng phạm vi của OTel GenAI  vào đại lý hiện tại, chứa nội dung nắm bắt giá trị mặc định và lưu trữ trích dẫn bên ngoài.

> OpenTelemetry GenAI 语义约定 đã xác định các tiêu chuẩn quan sát được của LLM 和 Agent.`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`Đúng vậy.

## Tập luyện bài tập

1. Đồ chơi bài học 01 ReAct loop với `invoke_agent`(INTERNAL) + mỗi công cụ trải dài. gửi đến một bản Jaeger.
  Trung ngữ翻译:思考并实践此练习。
2. Thêm ghi nội dung trong chế độ "chỉ tham chiếu": các yêu cầu đến SQLite, thuộc tính span chỉ mang ID hàng.
  Trung ngữ翻译:思考并实践此练习。
3. Đọc thông số kỹ thuật cho `gen_ai.data_source.id`Đưa nó vào tìm kiếm của bạn về bài học 09 Mem0.
  Trung ngữ翻译:思考并实践此练习。
4. Đặt `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`và xác minh các thuộc tính của bạn không được đổi tên bởi người thu thập.
  Trung ngữ翻译:思考并实践此练习。
5. Xây dựng bảng điều khiển: "những lỗi công cụ nào tương quan với các mô hình nào" từ các thuộc tính của GenAI.
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| GenAI SIG | "OpenTelemetry GenAI group" | OTel working group defining the schema |  |
| invoke_agent | "Agent span" | Name of the span representing an agent run |  |
| CLIENT span | "Remote call" | Span for a call to a remote agent service |  |
| INTERNAL span | "In-process" | Span for an in-process agent run |  |
| gen_ai.provider.name | "Provider" | anthropic / openai / aws.bedrock / google.vertex |  |
| gen_ai.data_source.id | "RAG source" | Which corpus/store a retrieval hit |  |
| Content capture | "Prompt logging" | Opt-in capture of messages; store externally in prod |  |
| Stability opt-in | "Preview mode" | Env var to pin experimental conventions |  |

## Xem thêm 延伸阅读

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) thông số kỹ thuật
  Trung ngữ: 翻译:见原文.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) GenAI kéo dài theo mặc định
  Trung ngữ: 翻译:见原文.
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) Các hệ thống OTel được xây dựng trong
  Trung ngữ: 翻译:见原文.
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) W3C trace context propagation
  Trung ngữ: 翻译:见原文.
