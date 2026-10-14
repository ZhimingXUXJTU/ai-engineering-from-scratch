# OpenAI Agents SDK: Handoffs, Guardrails, Tracing 交交 OpenAI Agent SDK

> OpenAI Agents SDK là framework đa đại lý nhẹ được xây dựng dựa trên API Responses. Năm nguyên thủy: Agent, Handoff, Guardrail, Session, Tracing. Handoffs là các công cụ có tên `transfer_to_<agent>`- Đường dây bảo vệ bị hỏng khi nhập hoặc ra.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Mục tiêu học tập

- Hãy nêu tên năm nguyên thủy của OpenAI Agents SDK.
- Giải thích các giao hàng: tại sao chúng được mô hình hóa như là công cụ, hình dạng tên nào mà mô hình nhìn thấy và cách chuyển ngữ cảnh.
- Hóa ra sự khác biệt giữa các cửa hàng đầu vào, cửa hàng đầu ra và cửa hàng công cụ; giải thích `run_in_parallel`với chế độ chặn.
- Thực hiện thời gian chạy stdlib với giao hàng + ván bảo vệ + theo dõi theo kiểu span.

## Vấn đề  vấn đề giới thiệu

Các đại lý không thể ủy thác sạch sẽ cuối cùng là lấp đầy mọi thứ trong một prompt. Các đại lý không có hàng rào gửi PII, sản xuất vi phạm chính sách, hoặc vòng lặp mãi mãi. SDK của OpenAI mã hóa ba nguyên thủy làm cho việc đa đại lý dễ xử lý.

> 无法干净地委派任务的代理 最终将所有东西塞进一个提示词中. 无护的代理会泄露 PII,输出违反政策内容或永远循环. OpenAI SDK sẽ làm cho nhiều công việc của Agent trở nên có thể quản lý được ba ngôn ngữ nguyên thủy được quy định.


> **【中文解读】**OpenAI Agents SDK(原 Swarm) là OpenAI 官方的 Agent 开发框架──三大核心概念:(1) HandoffsAgent 之间的任务转移;(2) Guardrails输入/输出安全护;(3) Tracing内置 OpenTelemetry 追踪──SDK's design philosophy is'简洁至上'使用最小抽象实现最常见的 Agent 模式──

> **{【拓展：OpenAI Agents SDK 是 2025-2026 年最流行的轻量级 Agent 框架。其 ...】}**OpenAI Agents SDK là khung cơ quan hạng nhẹ phổ biến nhất năm 2025-2026  Mô hình giao dịch của nó  Mô hình hợp tác của nhiều đại lý  Mô hình xây dựng cho '接力赛'  Một đại lý hoàn thành phần của mình sau đó sẽ chuyển quyền kiểm soát cho một người khác  Điều này tương tự với mô hình của AutoGen  Mô hình tạo ra đối với  Khả năng theo dõi SDK trong đó làm cho nó đặc biệt phù hợp với nhu cầu của môi trường sản xuất có thể quan sát được 

>  **【前置】**必须先掌握:Phase 14·01(Agent Loop) vàPhase 14·06(Tương cụ sử dụng) OpenAI Agents SDK 就是这些概念的产品化封装──还需要熟悉OpenAI Response API(不是旧的聊天完成 API),因为SDK là dựa trên Responses API 构建的──

## Khái niệm cốt lõi

### 5 nguyên thủy

1. **Agent.**LLM + hướng dẫn + công cụ + giao hàng.
2. **Handoff.**Đưa đại diện cho một đại lý khác.`transfer_to_<agent_name>`- Tôi không biết.
3. **Guardrail.**Thiết lập bằng chứng khi nhập (chỉ là đại lý đầu tiên), xuất (chỉ là đại lý cuối cùng) hoặc gọi công cụ (bằng công cụ chức năng).
4. **Session.**Lịch sử trò chuyện tự động qua các vòng.
5. **Tracing.**Các hệ thống tích hợp cho LLM, gọi công cụ, giao hàng, che chở.

### Giúp như là công cụ

Mô hình thấy `transfer_to_billing_agent`Địa chỉ cho nó báo hiệu thời gian chạy đến:

> 模型 trong danh sách công cụ`transfer_to_billing_agent`调用 nghĩa là vận hành cần:

> OpenAI Agents SDK 提供四种核心概念:Agents(带指令和工具的LLM) ‧Handoffs(Agent 间移交) ‧Guardrails(输入/输出验证) ‧Tracing(运行追踪) ‧生产级 Agent 开发框架──

1. Tải lại ngữ cảnh cuộc trò chuyện (hoặc phá vỡ nó qua `nest_handoff_history`beta).
2. Đưa ra lệnh cho tác nhân mục tiêu.
3. Cứ tiếp tục chạy với nhân viên mục tiêu.

Đây là mô hình giám sát (Dạy học 13 / Dạy học 28) được sản xuất.

> Đó là mô hình giám sát viên sau sản phẩm hóa (第13课 / 第28课)

>  **【类比】**Handoff 像医院的分诊转诊:分诊台(triage agent) nghe lời mô tả bệnh nhân sau khi nói "để đi đến bộ phận tim"`transfer_to_cardiology_agent` bệnh nhân (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân) (Bệnh nhân)**关键**:handoff là đơn phương, quyền kiểm soát hoàn toàn chuyển giao, đại lý gốc không tham gia nữa.

> OpenAI Agents SDK 提供四种核心概念:Agents(带指令和工具的LLM) ‧Handoffs(Agent 间移交) ‧Guardrails(输入/输出验证) ‧Tracing(运行追踪) ‧生产级 Agent 开发框架──

### Đường dây bảo vệ

Ba hương vị:

> 三种类型:

- **Input guardrails.**Hãy chạy theo thông tin của đại lý đầu tiên, từ chối các yêu cầu không an toàn hoặc ngoài phạm vi trước khi gọi LLM.
- **Output guardrails.**Đi vào nguồn gốc của nhân viên cuối cùng, bắt được thông tin cá nhân rò rỉ, vi phạm chính sách, phản ứng sai.
- **Tool guardrails.**Đánh thành công cụ tính năng, xác nhận lập luận, kiểm tra quyền, thực hiện kiểm toán.

Phương thức:

> 模式:

- **Parallel**(tầm định). Guardrail LLM chạy cùng với LLM chính.
- **Blocking**(`run_in_parallel=False`Guardrail LLM chạy trước, nếu bị ngã, không có token bị lãng phí trong cuộc gọi chính.

Cáp ba nâng lên `InputGuardrailTripwireTriggered`- `OutputGuardrailTripwireTriggered`- Tôi không biết.

> 触发器会抛出 `InputGuardrailTripwireTriggered`- `OutputGuardrailTripwireTriggered`异常──

> OpenAI Agents SDK 提供四种核心概念:Agents(带指令和工具的LLM) ‧Handoffs(Agent 间移交) ‧Guardrails(输入/输出验证) ‧Tracing(运行追踪) ‧生产级 Agent 开发框架──

### Theo dõi

Mỗi thế hệ LLM, công cụ gọi, giao, và guardrail phát ra một span. `OPENAI_AGENTS_DISABLE_TRACING=1`- Anh chọn ra.`add_trace_processor(processor)`Fan trải dài đến phần sau của bạn cùng với OpenAI.

> 默认开启──每次 LLM 生成、工具调用、交接和护都发出一个跨度──`OPENAI_AGENTS_DISABLE_TRACING=1`Tôi có thể chọn rút lui.`add_trace_processor(processor)`Có thể kéo dài cùng lúc gửi đến cuối của bạn và cuối của OpenAI.

> OpenAI Agents SDK 提供四种核心概念:Agents(带指令和工具的LLM) ‧Handoffs(Agent 间移交) ‧Guardrails(输入/输出验证) ‧Tracing(运行追踪) ‧生产级 Agent 开发框架──

### Các buổi

`Session`lưu trữ lịch sử cuộc trò chuyện trong một backend (SQLite, Redis, tùy chỉnh). `Runner.run(agent, input, session=session)`tự động tải và phụ kiện.

> `Session`Trong phần sau của SQLite, Redis, tự định nghĩa`Runner.run(agent, input, session=session)`tự động tải và thêm:

> OpenAI Agents SDK 提供四种核心概念:Agents(带指令和工具的LLM) ‧Handoffs(Agent 间移交) ‧Guardrails(输入/输出验证) ‧Tracing(运行追踪) ‧生产级 Agent 开发框架──

### Khi mô hình này đi sai

> ️ **【易错点】**Handoff drift(交接循环):Agent A 移交给 B,B 又移交给 A,A 再移交给 B...无限循环烧代币──**后果**"Bằng ngày không hoàn thành nhiệm vụ".**一行修复**: trong Runner 里加 hop counter`max_handoffs=5`), hơn là`HandoffBudgetExceeded`异常──OpenAI SDK 默认没有这个保护,必须自己加──

- **Handoff drift.**Cảnh sát A đưa tay sang Cảnh sát B, người trả lại cho Cảnh sát A. Thêm một bộ đếm hop.
- **Guardrail bypass.**Các cửa sổ bảo vệ công cụ chỉ bắn vào các công cụ chức năng; các công cụ tích hợp (đọc tập tin, lấy web) cần chính sách riêng biệt.
- **Over-tracing.**Nội dung nhạy cảm trong khoảng thời gian. Kết hợp với các quy tắc chụp nội dung OTel GenAI (Dạy học 23)  lưu trữ bên ngoài, tham chiếu bằng ID.

> 🤔 **【困惑】**Q: Guardrail's parallel 和 blocking 模式怎么选?看起来平行总是更快── A: 不一定──Parallel là"主 LLM 和 guardrail LLM 同时跑"快但浪费代币(guardrail 触发时主 LLM 已经在跑,代币已花了)──Blocking là"先 guardrail,过了再主 LLM"慢但省钱──**选择规则**Nếu màn chắn 触发率高 (如 >20%), dùng để chặn 省钱; nếu触发率 thấp (如 <5%), dùng song song 省延迟。

> **交接漂移。**Đặc vụ A  giao tiếp với đặc vụ B, đặc vụ B cũng giao tiếp với đặc vụ A ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙  ∙ ∙ ∙  ∙ ∙  ∙   ∙  ∙     ∙   ∙   ∙     ∙         ∙        ∙                                                                                                                                                                                                                                                                                                            
> **护栏绕过。**工具护 chỉ cần kích hoạt trên các công cụ hàm; 工具内置 (内置工具) 文件读取器,网页抓取) cần một chiến lược riêng biệt.
> **过度追踪。**Span 中包含敏感内容──配合 OTel GenAI 内容捕获规则(第 23 课) sử dụng 外部存储,按 ID 引用──

## Hãy xây dựng nó.
```figure
ae-agent-handoff
```

## Hãy xây dựng nó

`code/main.py`thực hiện hình dạng SDK trong stdlib:

> `code/main.py`Sử dụng tiêu chuẩn để thực hiện hình thức SDK:

> OpenAI Agents SDK 提供四种核心概念:Agents(带指令和工具的LLM) ‧Handoffs(Agent 间移交) ‧Guardrails(输入/输出验证) ‧Tracing(运行追踪) ‧生产级 Agent 开发框架──

- `Agent`- `FunctionTool`- `Handoff`(như một công cụ chức năng với ngữ nghĩa chuyển giao).
- `Runner`Với đường dây bảo vệ đầu vào/cởi ra/các công cụ, giao hàng và máy tính đếm hop.
- Một máy phát xạ dài đơn giản để cho thấy hình dạng dấu vết.
- Một đại lý phân loại cung cấp cho hóa đơn hoặc hỗ trợ dựa trên truy vấn của người dùng; Guardrail đi trên một đầu vào.

Đi đi.

```
python3 code/main.py
```

Hình ảnh cho thấy hai lần giao hàng thành công, một chuyến đi vào đường dây bảo vệ và một cây tròn phản ánh những gì SDK thực sự phát ra.

> 追踪 cho thấy hai lần kết nối thành công ∞ một lần nhập ∞触发, cũng như một phản ánh thực tế SDK ∞ xuất ∞

> OpenAI Agents SDK 提供四种核心概念:Agents(带指令和工具的LLM) ‧Handoffs(Agent 间移交) ‧Guardrails(输入/输出验证) ‧Tracing(运行追踪) ‧生产级 Agent 开发框架──

## Hãy sử dụng nó để thực hiện

- **OpenAI Agents SDK**cho các sản phẩm OpenAI đầu tiên.
- **Claude Agent SDK**(Dân học 17) cho các sản phẩm Claude-first.
- **LangGraph**(Dân học 13) khi bạn muốn có một trạng thái rõ ràng và một hồ sơ lâu dài.
- **Custom**khi bạn cần kiểm soát chính xác (những dịch vụ bằng giọng nói, nhiều nhà cung cấp, các dịch vụ liên bang).

## Chuyển nó đi.

`outputs/skill-agents-sdk-scaffold.md`Đặt một ứng dụng SDK của Agents với một đại lý phân loại, giao hàng, cửa sổ đầu vào/ ra ngoài/ công cụ, cửa hàng phiên và bộ xử lý theo dõi.

> `outputs/skill-agents-sdk-scaffold.md`搭建一个代理 SDK 应用,包含分诊 Agent、交接、输入/输出/工具护、会话存储和追踪处理器──

> OpenAI Agents SDK 提供四种核心概念:Agents(带指令和工具的LLM) ‧Handoffs(Agent 间移交) ‧Guardrails(输入/输出验证) ‧Tracing(运行追踪) ‧生产级 Agent 开发框架──

## Tập luyện bài tập

1. Thêm một con số chuyển giao: từ chối sau khi chuyển giao N. Theo dõi hành vi.
  Trung ngữ翻译:思考并实践此练习。
2. Thực hiện`nest_handoff_history`tùy chọn  kết hợp các thông điệp trước đó thành một bản tóm tắt trước khi chuyển.
  Trung ngữ翻译:思考并实践此练习。
3. Hãy so sánh độ trễ của các lệnh sẽ làm nó bị cản trở so với những lệnh mà đi qua.
  Trung ngữ翻译:思考并实践此练习。
4. Sợi dây`add_trace_processor`để ghi nhật ký JSON. hình dạng nào nó phát ra cho mỗi khoảng thời gian?
  Trung ngữ翻译:思考并实践此练习。
5. Đọc các tài liệu SDK. Đưa đồ chơi SDLIB của bạn vào `openai-agents-python`- Cậu làm sai mô hình gì?
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent | "LLM + instructions" | Agent type in the SDK; owns tools and handoffs |  |
| Handoff | "Transfer" | Tool the model calls to delegate to another agent |  |
| Guardrail | "Policy check" | Validation on input / output / tool invocation |  |
| Tripwire | "Guardrail trip" | Exception raised when guardrail rejects |  |
| Session | "History store" | Conversation memory persisted between runs |  |
| Tracing | "Spans" | Built-in observability over LLM + tool + handoff + guardrail |  |
| Blocking guardrail | "Sequential check" | Guardrail runs first; no token waste on trip |  |
| Parallel guardrail | "Concurrent check" | Guardrail runs alongside; lower latency, wastes tokens on trip |  |

## Xem thêm 延伸阅读

- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) nguyên thủy, giao hàng, đường dây bảo vệ, theo dõi
  Trung ngữ: 翻译:见原文.
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) Phương đối tác có hương vị Claude
  Trung ngữ: 翻译:见原文.
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) khi nào để tiếp cận cho các giao hàng
  Trung ngữ: 翻译:见原文.
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) các SDK đại lý tiêu chuẩn trải dài từ bản đồ đến
  Trung ngữ: 翻译:见原文.
