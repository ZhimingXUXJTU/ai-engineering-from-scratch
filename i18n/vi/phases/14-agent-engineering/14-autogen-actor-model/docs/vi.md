# AutoGen v0.4: Mô hình diễn viên và khung đại lý
# Mô hình diễn viên cho các đại lý  Thông điệp không đồng bộ và thời gian chạy được đánh dấu

> Các đại lý như các diễn viên: trao đổi tin nhắn không đồng bộ, xử lý các sự kiện, cách ly lỗi, đồng thời tự nhiên. AutoGen v0.4 (Microsoft Research, tháng 1 năm 2025) đã thiết kế lại dàn xếp đại lý xung quanh mô hình này; khung hiện đang trong chế độ bảo trì, với Microsoft Agent Framework (bước xem trước công cộng tháng 10 năm 2025) là người kế nhiệm sản xuất của nó.

> **【中文解读】**AutoGen v0.4 (Microsoft 研究院, tháng 1 năm 2025) xoay quanh Actor 模型 tái thiết kế Agent 编排, 事件驱动 Agent,故障隔离,天然并发,

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 12 (工作流模式)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Mô tả mô hình diễn viên: đại lý như diễn viên, tin nhắn như IPC duy nhất, sự cô lập thất bại cho mỗi diễn viên.
  Trung文翻译:描述 Actor 模型:Agent 作为 Actor,消息作为唯一的进程间通信,每个 Actor 独立故障隔离──
- Tên gọi ba lớp API của AutoGen v0.4  Core, AgentChat, Extensions  và mỗi lớp là gì.
  Trung文翻译:说出 AutoGen v0.4's三个 API层Core、AgentChat、Extensions及各自用途──
- Giải thích tại sao việc tách thông điệp từ việc xử lý cho phép sự cô lập lỗi và đồng thời tự nhiên.
  Trung ngữ翻译:解释为什么将消息传递与处理解能带来故障隔离和自然并发──
- Thực hiện một runtime diễn viên stdlib trong Python và chuyển một dòng kiểm tra mã hai đại lý vào nó.
  Trung文翻译:用Python 标准库实现 Actor 运行时并将双 Agent 代码审查流程移植到其上──

## Vấn đề  vấn đề giới thiệu

Hầu hết các khung đại lý đều đồng bộ: một đại lý sản xuất, một đại lý tiêu thụ, trong một đống gọi. Các thất bại gây ra sự cố.

> Đại đa số Cơ quan 框架 là đồng bộ: một Cơ quan sản xuất, một Cơ quan tiêu thụ, trong调用, thất bại sẽ làm cho sự sụp đổ, và phát triển là hậu gia của, phân tán cần phải viết lại.

Câu trả lời của AutoGen v0.4: mô hình diễn viên. Mỗi đại lý là một diễn viên với một hộp thư đến riêng. Thông điệp là tương tác duy nhất. Thời gian chạy tách giao hàng khỏi xử lý. Các thất bại cô lập với một diễn viên. Sự cạnh tranh là bản địa. Phân phối chỉ là giao thông khác nhau.

> AutoGen v0.4 trả lời:Actor 模型── Mỗi đại lý là một diễn viên trong hộp thư gửi riêng──消息是唯一交互方式──运行时将交付与处理解──失败隔离到一个演员──并发是原生──分布式只是不同的传输方式──

> **【中文解读】**AutoGen v0.4  áp dụng Actor 模型 Mỗi đại lý là một diễn viên độc lập, thông qua truyền thông truyền thông.

> **【拓展：AutoGen 的演进】**AutoGen được phát triển bởi Microsoft Research Institute, v0.4 (2025) là một cuộc tái cấu trúc lớn. Từ mô hình đối thoại v0.3 chuyển sang mô hình diễn viên, cảm hứng từ mô hình phát triển của Erlang / Akka.

>  **【前置】**必须先掌握:Phase 14·01(Agent Loop) vàPhase 14·12(Anthropic Workflow Patterns) 本节是这些模式在"并发场景"下延伸──还需要"Actor 模型"的基本概念如果不知道Erlang/Akka是什么,先去补一节分布式系统课──本节硬核在"异步消息传递"而不是"LLM调用"──

## Khái niệm cốt lõi

### Các diễn viên

Một diễn viên có:

> Một diễn viên có:

- Một nhà nước tư nhân (không bao giờ được chạm trực tiếp từ bên ngoài).
  Trung ngữ翻译:私有状态 (私有状态)
- Một hộp thư đến (trung thư).
  Trung文翻译:收件箱(消息队列) 』
- Một người quản lý:`receive(message) -> effects`nơi mà hiệu ứng có thể là "đưa trả lời", "đưa cho một diễn viên khác", "đưa ra một diễn viên mới", "được cập nhật trạng thái", "đừng tự".
  Trung ngữ翻译:处理器:`receive(message) -> effects`, hiệu quả có thể là "回复""",发送给其他演员"",创建新演员"",更新状态"",停止自己"――

Hai diễn viên không thể chia sẻ trí nhớ, họ chỉ có thể gửi tin nhắn.

>  **【类比】**Người diễn viên 模型像办公室里互相见的同事: mỗi người có công việc riêng của mình (私有状态) 和收件箱 (收件箱) 消息队列 (消息队列)  Bạn muốn để cho đồng nghiệp giúp đỡ, không thể trực tiếp đi翻他的工位 (共享内存), chỉ có thể发邮件 (发消息)  Người diễn viên xử lý完邮件可能回信 (回复) 转发给另一个人 (发送给另一个人) 招聘习生 (招生)  tạo một diễn viên mới (发送新演员) **关键**Một đồng nghiệp không ảnh hưởng đến người khác.

> Hai diễn viên không thể chia sẻ ký ức.

### Ba lớp API trong AutoGen v0.4
### Ba lớp API

AutoGen v0.4 chia bề mặt thành ba phần:

1. **Core.**Quản lý các diễn viên cấp thấp. `AgentRuntime`- `Agent`- `Message`- `Topic`- Chuyển đổi tin nhắn đồng bộ, dựa trên sự kiện.
   Trung ngữ翻译:**Core。**底层 Actor 框架。`AgentRuntime``Agent``Message``Topic`异步消息交换,事件驱动
2. **AgentChat.**API cấp cao dựa trên nhiệm vụ (đổi thay cho ConversableAgent của v0.2). `AssistantAgent`- `UserProxyAgent`- `RoundRobinGroupChat`- `SelectorGroupChat`- Tôi không biết.
   Trung ngữ翻译:**AgentChat。**任务驱动的高级 API(替代 v0.2 của ConversableAgent)`AssistantAgent``UserProxyAgent``RoundRobinGroupChat``SelectorGroupChat`
3. **Extensions.**Các tích hợp  OpenAI, Anthropic, Azure, công cụ, bộ nhớ.
   Trung ngữ翻译:**Extensions。**集成OpenAI、Anthropic、Azure、工具、记忆──

### Tại sao việc tách biệt quan trọng

Trong mô hình v0.2, gọi `agent_a.chat(agent_b)`đồng thời chặn agent_a cho đến khi agent_b quay lại.`send(agent_b, msg)`đưa tin vào hộp thư đến của agent_b và trả lại. thời gian chạy đưa ra sau đó. Ba hậu quả:

> Trong v0.2 模型中,调用 `agent_a.chat(agent_b)`Đồng thời ngăn chặn đại lý_a cho đến khi đại lý_b  quay trở lại. Trong v0.4,`send(agent_b, msg)`Để gửi thông điệp vào hộp thư của đại lý và trả lại.

- **Fault isolation.**Cảnh sát B không bị hỏng Cảnh sát A  thời gian chạy bắt được sự thất bại trong bộ xử lý của B và quyết định phải làm gì (đăng ký, thử lại, thư chết).
  Trung ngữ翻译:**故障隔离。**Đặc vụ B 崩 sẽ không gây ra sự cố bị bắt trong bộ xử lý của B 崩 hành động khi hành động của B 崩 và quyết định làm gì (日志、重试、死信) ⋅
- **Natural concurrency.**Nhiều tin nhắn trên máy bay cùng một lúc; các diễn viên xử lý hộp thư đến của họ cùng một lúc.
  Trung ngữ翻译:**天然并发。**Nhiều thông tin đồng thời truyền tải; Người chơi không phát hành xử lý chúng.
- **Distribution-ready.**Hộp thư đến + vận chuyển là trừu tượng tương tự cho dù diễn viên đang trong quá trình hoặc trên một máy chủ khác.
  Trung ngữ翻译:**分布式就绪。**收件箱 + 传输 là cùng một bản tóm tắt, dù diễn viên trong quá trình hay trên máy chủ khác.

> ️ **【易错点】**Với diễn viên nhưng quên "câu chuyện phải được sắp xếp"**后果**:本地开发跑通(消息传递 là Python đối tượng引用), trên sản xuất phân phối đến nhiều cơ hội trên sự sụp đổ đối tác quá trình không đạt đến đối tượng của bạn。**一行修复**: tất cả các tin nhắn phải sử dụng pydantic/dataclass/JSON-schema 定义, cấm truyền lambda、文件句柄、数据库连接等不可序列化对象──

### Topology

- **RoundRobinGroupChat.**Các nhân viên thay lượt trong một vòng quay cố định.
  Trung ngữ翻译:**RoundRobinGroupChat。**Trưởng 按固定轮换顺序轮流──
- **SelectorGroupChat.**Một đại lý chọn lựa chọn người đi tiếp theo dựa trên bối cảnh cuộc trò chuyện.
  Trung ngữ翻译:**SelectorGroupChat。**选择器 Agent 根据对话上下文选择下一个发言人。
- **Magentic-One.**Nhóm quản lý đa đại lý để duyệt web, xử lý mã, xử lý tệp.
  Trung ngữ翻译:**Magentic-One。**Sử dụng để xem các trang web, thực hiện mã, xử lý tài liệu, tham khảo nhiều nhóm đại lý.

### Sự quan sát

OpenTelemetry hỗ trợ được tích hợp. Mỗi tin nhắn phát ra một khoảng thời gian; các cuộc gọi công cụ mang `gen_ai.*`thuộc tính theo các công ước ngữ nghĩa OTel GenAI 2026 (Lớp 23).

> OpenTelemetry 支持内置──每条消息发发出一个跨度;工具调用携带 `gen_ai.*`属性,符合 2026 年 OTel GenAI 语义约定(第 23 课)

### Tình trạng: chế độ bảo trì

Đầu năm 2026: AutoGen v0.7.x ổn định cho nghiên cứu và tạo mẫu. Microsoft đã chuyển phát triển tích cực sang Microsoft Agent Framework, kế nhiệm sản xuất (bước xem trước công khai ngày 1 tháng 10 năm 2025; 1.0 GA được nhắm mục tiêu cho cuối Q1 năm 2026).

```figure
actor-mailbox
```

> 🤔 **【困惑】**Q: AutoGen đã bước vào mô hình bảo trì, tôi còn nên học không?**别在生产上选 AutoGen**△原因:(1) 微软 đã chuyển sang Microsoft Agent Framework(MAF), AutoGen không nhận được các tính năng mới;(2) Actor 模型本身是个**经久不衰的分布式设计思想**(được lấy từ bài luận Hewitt năm 1973,比 LLM 老 50年), hiểu nó cho bạn đánh giá MAF、Erlang、Akka、Ray đều có ích.

> Đầu năm 2026: AutoGen v0.7.x trong nghiên cứu và phát triển nguyên mẫu ổn định. Microsoft đã chuyển động phát triển tích cực sang Microsoft Agent Framework.

## Hãy xây dựng nó.

`code/main.py`thực hiện một runtime diễn viên stdlib:

> `code/main.py`Used standard库 đã thực hiện Actor 运行时:

- `Message` tải trọng hữu ích được đánh dấu với `sender`- `recipient`- `topic`- `body`- Tôi không biết.
  Trung ngữ翻译:`Message`带 `sender``recipient``topic``body`带类型 tải
- `Actor` trừu tượng với `receive(message, runtime)`- Tôi không biết.
  Trung ngữ翻译:`Actor`带 `receive(message, runtime)`                                                                                                                                                                                                                                                              
- `Runtime` vòng lặp sự kiện với hàng đợi chung, giao hàng, cách ly thất bại.
  Trung ngữ翻译:`Runtime`带共享队列,递交,故障隔离事件循环.
- Một bản demo hai diễn viên:`ReviewerAgent`mã đánh giá, `ChecklistAgent`chạy một danh sách kiểm tra; họ trao đổi tin nhắn cho đến khi đồng thuận.
  中文翻译:双 Actor 演示:`ReviewerAgent`审查代码,`ChecklistAgent`运行检查清单; chúng trao đổi thông tin cho đến khi đạt được sự đồng thuận.

Đi đi.

> 运行:

```
python3 code/main.py
```

Hướng dẫn cho thấy giao thông thông tin, một sự thất bại mô phỏng trong một diễn viên mà không gây ra sự sụp đổ của người khác, và sự hội tụ trên một phán quyết chung.

> 轨迹显示消息递递, 模拟故障 trong một diễn viên sẽ không dẫn đến sự sụp đổ khác, cũng như nhận được quyết định chia sẻ.

## Hãy sử dụng nó để thực hiện

- **AutoGen v0.4/v0.7**(hỗ trợ)  ổn định cho nghiên cứu, tạo ra nguyên mẫu, nhiều tác nhân mô hình.
  Trung ngữ翻译:**AutoGen v0.4/v0.7**(维护中) 研究、原型、多 Agent 模式稳定──
- **Microsoft Agent Framework**(Public preview)  con đường tiến bộ; cùng một ý tưởng mô hình diễn viên trong một API được làm mới.
  Trung ngữ翻译:**Microsoft Agent Framework**(公开预览) 前进方向; trong API được cập nhật 中体现相同的 Actor 模型理念。
- **Microsoft Agent Framework** kế thừa sản xuất (bước xem trước công khai vào tháng 10 năm 2025); cùng một ý tưởng diễn viên-chương mẫu trong một API được cập nhật.
- **LangGraph swarm topology**(Dạy 13)  mô hình tương tự qua việc trao đổi công cụ chung.
  Trung ngữ翻译:**LangGraph 群体拓扑**(第 13 课) 通过共享工具移交的类似模式──
- **Custom actor runtime** khi bạn cần vận chuyển cụ thể (NATS, RabbitMQ, gRPC).
  Trung ngữ翻译:**自定义 Actor 运行时**当你需要特定传输 (NATS, RabbitMQ, GRPC)

## Chuyển nó đi.

`outputs/skill-actor-runtime.md`tạo ra thời gian chạy diễn viên tối thiểu cộng với một mẫu nhóm (RoundRobin hoặc Selector) cho một nhiệm vụ đa đại lý nhất định.

> `outputs/skill-actor-runtime.md`Để xác định nhiều đại lý  nhiệm vụ tạo ra ít nhất Đấu kịch 运行时加团队模板(RoundRobin hoặc Selector)

## Tập luyện bài tập

1. Thêm một hàng chữ cái chết: khi một người xử lý nâng lên, hãy đậu thông điệp thất bại để kiểm tra của con người.
   Trung ngữ翻译:添加死信队列: Khi bộ xử lý bị ném ra bất thường, sẽ thất bại thông tin dừng để kiểm tra nhân tạo.
2. Thực hiện`SelectorGroupChat`: một diễn viên chọn chọn người xử lý thông điệp tiếp theo dựa trên trạng thái trò chuyện.
   Trung ngữ翻译:实现 `SelectorGroupChat`: chọn器 Actor 根据对话状态选择谁处理下一条消息──
3. Thêm vận chuyển phân tán: thay thế hàng trong quá trình cho một máy chủ JSON-over-HTTP để các diễn viên có thể chạy trong các quá trình riêng biệt.
   Trung文翻译:添加分布式传输:将进程内队列替换为 JSON-over-HTTP 服务器,使 Actor có thể chạy trong quá trình độc lập.
4. Đưa ra một khoảng thời gian OTel cho mỗi tin nhắn (hoặc một không có hoạt động thay thế).`gen_ai.agent.name`- `gen_ai.operation.name`Mỗi bài học 23.
   中文翻译:为每条消息连接 OTel span(或无运 替代) 按第 23 课发出 `gen_ai.agent.name``gen_ai.operation.name`
5. Đọc bài viết về kiến trúc của AutoGen v0.4.`autogen_core`API, anh bỏ qua điều gì quan trọng trong sản xuất?
   Trung ngữ翻译:阅读 AutoGen v0.4 的架构文章──将玩具移植到真正的 `autogen_core`API... Anh nhảy qua cái gì quan trọng trong sản xuất?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Actor | "Agent" / "Agent" | Private state + inbox + handler; no shared memory / 私有状态 + 收件箱 + 处理器；无共享内存 |
| Message | "Event" / "事件" | Typed payload; the only way actors interact / 带类型载荷；Actor 唯一的交互方式 |
| Inbox | "Mailbox" / "邮箱" | Per-actor queue of pending messages / 每个 Actor 的待处理消息队列 |
| Runtime | "Agent host" / "Agent 宿主" | Event loop that routes messages and isolates failures / 路由消息和隔离故障的事件循环 |
| Topic | "Channel" / "通道" | Named publish-subscribe route between actors / Actor 之间的命名发布-订阅路由 |
| Fault isolation | "Let it crash" / "让它崩溃" | One actor failing does not crash others / 一个 Actor 失败不会导致其他崩溃 |
| RoundRobinGroupChat | "Fixed-rotation team" / "固定轮换团队" | Agents take turns in order / Agent 按顺序轮流 |
| SelectorGroupChat | "Context-routed team" / "上下文路由团队" | Selector picks who goes next / 选择器选择下一个发言者 |
| Magentic-One | "Reference team" / "参考团队" | Multi-agent squad for web + code + files / 用于网页+代码+文件的多 Agent 小队 |

## Xem thêm 延伸阅读

- [AutoGen v0.4, Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) bài thiết kế lại
  Trung ngữ翻译:AutoGen v0.4 微软研究院重新设计文章。
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) thay thế hình đồ thị
  Trung文翻译:LangGraph 概览图形替代方案。
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) kéo dài AutoGen phát ra theo mặc định
  中文翻译:OpenTelemetry GenAI 语义约定AutoGen 默认发射跨度──
