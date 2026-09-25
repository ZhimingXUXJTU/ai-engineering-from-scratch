# Các thương mại của Agent Framework  LangGraph vs CrewAI vs AutoGen vs Agno  Agent Framework đối với: LangGraph vs CrewAI vs AutoGen vs Agno
# Các giao dịch cơ bản của đại lý  Hình ảnh, vai trò và dàn nhạc diễn viên

> Mỗi framework bán cùng một demo (nhà nghiên cứu xây dựng một báo cáo) và ẩn cùng một lỗi (chế hoạch trạng thái chiến đấu với lớp dàn xếp). Chọn framework có trừu tượng phù hợp với hình dạng của vấn đề của bạn; tất cả những thứ khác là dán bạn viết hai lần.

> **【中文解读】**Mỗi khung đều hiển thị cùng một demo (đọc Agent 生成報告), tất cả ẩn cùng một lỗi (đọc trạng thái và sắp xếp tầng xung đột)  chọn trừu tượng phù hợp với hình dạng của vấn đề của bạn, phần còn lại là bạn phải viết hai lần 水代码──

> **【拓展：框架选择→Agent工程实践】**LangGraph  thích hợp với nhu cầu kiểm soát chi tiết của dòng công việc có trạng thái; CrewAI  thích hợp với nhiều vai trò cộng tác; AutoGen  thích hợp với nhiều đại lý hội thoại;

>  **【前置】**Học本节前请先掌握:Phase 11·09(Function Calling)、Phase 11·16(LangGraph)。本节 là phần cuối cùng củaPhase 11, đối với 4 个主流框架(LangGraph、CrewAI、AutoGen、Agno) 优劣──最好已经分别使用过其中 2个──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 16 (LangGraph) | **前置知识:** Phase 11 · 09 (函数调用)、16 (LangGraph)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Bạn có một nhiệm vụ cần nhiều hơn một cuộc gọi LLM. Có thể đó là một dòng công việc nghiên cứu (kế hoạch, tìm kiếm, tóm tắt, trích dẫn). Có thể đó là một đường ống sửa đổi mã (đánh phân, phê bình, sửa chữa, xác nhận). Có thể đó là một trợ lý đa lượt ghi lại các chuyến bay, viết email và lưu trữ báo cáo chi phí. Bạn chọn một khung.

> Bạn có một nhiệm vụ cần nhiều lần để điều chỉnh LLM. Có lẽ là nghiên cứu.

Ba ngày sau, bạn phát hiện ra các sự rò rỉ của khung trừu tượng. CrewAI cho bạn vai trò nhưng chiến đấu với bạn khi "nhà nghiên cứu" cần phải trao một kế hoạch có cấu trúc cho "nhà viết". AutoGen cho bạn trò chuyện giữa các đại lý nhưng không có trạng thái hạng nhất vì vậy điểm kiểm soát của bạn là một nhựa nhựa của một nhật ký trò chuyện. LangGraph đưa ra một biểu đồ trạng thái nhưng buộc bạn phải đặt tên cho mỗi chuyển đổi trước khi bạn biết đại lý sẽ làm gì. Agno cho bạn một bản trừu tượng đơn đại lý mà thét lên khi bạn cố gắng phát triển ra ba công nhân đồng thời.

> Trẻ ngày sau, bạn phát hiện ra một sự phơi bày trừu tượng của khung hình. Cỗ máy AI cho bạn vai trò nhưng khi "phân tích viên" cần phải đưa ra kế hoạch cấu trúc cho "người viết" sẽ gặp vấn đề. AutoGen cho bạn một đại lý.

Giải pháp không phải là "chọn khung tốt nhất". Nó là để phù hợp với bản trừu tượng cốt lõi của khung với hình dạng của vấn đề của bạn. Bài học này vẽ bản đồ đó.

> Phương pháp sửa chữa không phải là "chọn khung tốt nhất" mà là kết hợp các bản trừu tượng cốt lõi của khung với hình dạng của vấn đề của bạn.


> **【中文解读】**Các mô hình của các cơ quan: 1)  nhiệm vụ phức tạp 简单 RAG sử dụng LlamaIndex, 复杂 Agent sử dụng LangGraph; 2) 团队 kinh nghiệm 新手使用 LangChain 模板,专家使用原生 API; 3) 生产要求需要 LangSmith 集成选择 LangChain 生态──

>  **【类比】**选 Agent 框架像选交通工具短途买菜用自行车(stdlib + hàm gọi),跨城出差用车(LangGraph 状态机),多人旅行用面包车(CrewAI 角色),即时通讯用电话(AutoGen 对话) ⋅每种工具有适用场景,"哪个好"是错误问题,"哪个匹配你的问题形状"才是──

> ️ **【易错点】**框架选错的 3 个常见原因:(1) **跟风最热门**AutoGen 火就上 AutoGen, kết quả phát hiện nhiệm vụ chỉ đơn độc Agent + 工具, quá工程;先评估任务复杂度再选择框架――(2) **被 demo 误导**CrewAI's"研究员+作家"demo trông rất tuyệt, nhưng thực tế nhiệm vụ trong vai trò biên giới模糊,CrewAI's role abstract反而拖累;先做 PoC 验证抽象匹配──(3) **低估迁移成本** bắt đầu sử dụng Agno 简单,后期要增加 Agent 时发现Agno 不支持,重写到 LangGraph 花两周;选框架时看 6 个月后的需求──


## Khái niệm cốt lõi

> **【中文解读】**Các cơ quan quản lý của các nhà quản lý: LongChain 生态 hoàn chỉnh nhất nhưng phức tạp nhất, LlamaIndex  tập trung vào RAG, CrewAI  phù hợp với nhiều nhà quản lý  hợp tác, LongGraph  phù hợp với trạng thái của máy kiểm soát, trực tiếp sử dụng API tối đa nhưng tự viết thêm mã.

> **【拓展：Agent 框架的选型指南】**选型维度:(1) 任务复杂度(简单 RAG 用 LlamaIndex,复杂 Agent 用 LangGraph);(2) 团队 kinh nghiệm(新手用 LangChain 模板,专家用原生 API);(3) 生产要求(LangSmith 集成选 LangChain 生态) ――2025 年的趋势是框架轻量化──


![Agent framework matrix: core abstraction vs problem shape](../assets/framework-matrix.svg)

Bốn khung thống trị phong cảnh năm 2026.

> Bốn khung thống trị khung hình năm 2026:

| Framework | Core abstraction | Best fit | Worst fit |
|-----------|------------------|----------|-----------|
| **LangGraph** | `StateGraph` — typed state, nodes, conditional edges, checkpointer. | Workflows with explicit state and human-in-the-loop interrupts; production agents needing time-travel debugging. | Loose, role-driven brainstorming where the topology is unknown. |
| **CrewAI** | `Crew` — roles (goal, backstory), tasks, process (sequential or hierarchical). | Role-playing or persona-driven workflows with a short linear/hierarchical plan. | Anything stateful beyond the crew's turn history; complex branching. |
| **AutoGen** | `ConversableAgent` pair — two or more agents that speak in turns until an exit condition. | Multi-agent *dialogue* (teacher-student, proposer-critic, actor-reviewer) where the thinking emerges from the chat. | Deterministic workflows with a known DAG; anything needing durable state across restarts. |
| **Agno** | `Agent` — a single LLM + tools + memory, composable into teams. | Fast-to-build single agents and lightweight teams; strong multi-modality and built-in storage drivers. | Deep, explicitly-branched graphs with custom reducers. |

### "Từ trừu tượng" thực sự có nghĩa là gì

Sự trừu tượng cốt lõi của một framework là thứ bạn vẽ trên bảng màu khi bạn đưa ra kiến trúc.

> Chụp phác thảo của framework là những gì bạn vẽ trên bảng trắng khi bán cấu trúc.

- **LangGraph**→ bạn vẽ một biểu đồ. nút là bước, cạnh là chuyển tiếp, và đối tượng trạng thái ở mỗi điểm được gõ. mô hình tâm lý là một máy trạng thái.
  Bạn vẽ một bức tranh. Điểm là bước, bên là chuyển đổi.
- **CrewAI**→ bạn vẽ một biểu đồ tổ chức. Mỗi vai trò có mô tả công việc và một người quản lý hướng các nhiệm vụ. mô hình tâm lý là một nhóm nhỏ các chuyên gia.
  Bạn vẽ một tổ chức. Mỗi vai trò có mô tả trách nhiệm, quản lý phân bổ nhiệm vụ.
- **AutoGen**2 đại lý nhắn tin với nhau; một đại lý thứ ba gia nhập nếu bạn cần một người điều hành. Mô hình tâm lý là trò chuyện.
  Bạn vẽ một Slack 私信. 2 đại lý.
- **Agno**→ bạn vẽ một hộp đơn với các công cụ treo trên nó. đặt các hộp cạnh nhau cho một nhóm. mô hình tâm lý là "đồng hành với pin bao gồm".
  Bạn vẽ một khung hình treo trên công cụ. Mô hình tâm trí là "đại lý mở hộp".

### Câu hỏi nhà nước

Nhà nước là nơi mà hầu hết các lựa chọn khung bị phá vỡ trong sản xuất.

>  trạng thái là nơi mà hầu hết các khung lựa chọn trong sản xuất xuất vấn đề.

- **LangGraph.**Tiêu chuẩn trạng thái (`TypedDict`hoặc mô hình Pydantic), giảm per-field, điểm kiểm tra hạng nhất (SQLite/Postgres/Redis).
  **LangGraph。**类型化 trạng thái`TypedDict`hoặc Pydantic 模型) 、每字段 reducer、一等公民检查点器(SQLite/Postgres/Redis) ⋅恢复、中断和时间旅行免费──(见阶段 11 · 16──)
- **CrewAI.**Các dòng nước như các chuỗi giữa các nhiệm vụ qua `context`trường, hoặc cấu trúc qua `output_pydantic`Không có cửa hàng bền bỉ cho mỗi thủy thủ đoàn ra khỏi hộp; bạn tự mình đi nếu thủy thủ đoàn phải sống sót sau khi khởi động lại.
  **CrewAI。** trạng thái như字符串 trong nhiệm vụ trong quá trình `context`字段流动, hoặc qua `output_pydantic`结构化──开箱无持久每人机组 储存; Nếu phi hành đoàn 需活重启需自外挂──
- **AutoGen.**State là lịch sử trò chuyện và bất kỳ người dùng xác định `context`. Các bản sao cuộc trò chuyện vẫn tồn tại; trạng thái workflow tùy ý không làm được trừ khi bạn viết bộ chuyển đổi.
  **AutoGen。** trạng thái là chat lịch sử và bất kỳ người dùng được xác định `context`                                                                                                                                                                                                                                                              
- **Agno.**Các trình điều khiển lưu trữ tích hợp (SQLite, Postgres, Mongo, Redis, DynamoDB) được gắn vào một `Agent`qua `storage=` các phiên trò chuyện và ký ức người dùng tồn tại tự động. Không phải một điểm kiểm tra đồ thị đầy đủ; một cửa hàng phiên.
  **Agno。**内置存储驱动(SQLite、Postgres、Mongo、Redis、DynamoDB) thông qua `storage=`附在 `Agent`上对话会话和用户记忆自动持久化──不是完整图片检查点器;是会话存储──

- **LangGraph.**Tiêu chuẩn trạng thái (`TypedDict`hoặc mô hình Pydantic), giảm per-field, điểm kiểm tra hạng nhất (SQLite/Postgres/Redis).
- **CrewAI.**Các dòng nước như các chuỗi giữa các nhiệm vụ qua `context`trường, hoặc cấu trúc qua `output_pydantic`Không có cửa hàng bền bỉ cho mỗi thủy thủ đoàn ra khỏi hộp; bạn tự mình đi nếu thủy thủ đoàn phải sống sót sau khi khởi động lại.
- **AutoGen.**State là lịch sử trò chuyện và bất kỳ người dùng xác định `context`. Các bản sao cuộc trò chuyện vẫn tồn tại; trạng thái workflow tùy ý không làm được trừ khi bạn viết bộ chuyển đổi.
- **Agno.**Các trình điều khiển lưu trữ tích hợp (SQLite, Postgres, Mongo, Redis, DynamoDB) được gắn vào một `Agent`qua `storage=` các phiên trò chuyện và ký ức người dùng tồn tại tự động. Không phải một điểm kiểm tra đồ thị đầy đủ; một cửa hàng phiên.

### Câu hỏi về phân nhánh

Tất cả các đại lý không nhỏ đều là những chi nhánh, những người quyết định những vấn đề.

> Mỗi đại lý bất thường đều có một bộ phận.

- **LangGraph** bạn quyết định, thông qua các cạnh có điều kiện. Routing là một hàm Python với tên chi nhánh. Chi nhánh là lớp đầu tiên trong biểu đồ được biên soạn; điểm kiểm tra ghi lại chi nhánh nào đã được lấy.
  **LangGraph**你决定,通过条件边──路由是带命名分支的 Python 函数──分支是编译图中的一等公民;检查点器记录走哪条──
- **CrewAI** người quản lý quyết định trong chế độ phân cấp; trong chế độ theo dõi bạn quyết định tại thời gian xây dựng. Routing là ngầm trong danh sách nhiệm vụ; không có "nếu" hạng nhất bên ngoài lời nhắc của người quản lý.
  **CrewAI**分层模式由经理决定;顺序模式你在构建时决定──路由隐含在任务列表中;经理提示外无一等公民"if"──
- **AutoGen** các đại lý quyết định qua trò chuyện.`GroupChatManager`chọn người phát biểu tiếp theo; bạn có thể viết tay một `speaker_selection_method`nhưng mặc định là LLM-driven.
  **AutoGen**Công viên 通过聊天决定──分支从谁下一个说话中涌现──`GroupChatManager`选下一个发言人;可手写 `speaker_selection_method`Nhưng tôi đã chấp nhận LLM.
- **Agno** đại lý quyết định công cụ nào để gọi tiếp theo.
  **Agno**Agent 通过下一个调用哪个工具决定──团队 có bộ điều phối viên/router/co-laborator 模式; bên ngoài分支由开发者负责──

- **LangGraph** bạn quyết định, thông qua các cạnh có điều kiện. Routing là một hàm Python với tên chi nhánh. Chi nhánh là lớp đầu tiên trong biểu đồ được biên soạn; điểm kiểm tra ghi lại chi nhánh nào đã được lấy.
- **CrewAI** người quản lý quyết định trong chế độ phân cấp; trong chế độ theo dõi bạn quyết định tại thời gian xây dựng. Routing là ngầm trong danh sách nhiệm vụ; không có "nếu" hạng nhất bên ngoài lời nhắc của người quản lý.
- **AutoGen** các đại lý quyết định qua trò chuyện.`GroupChatManager`chọn người phát biểu tiếp theo; bạn có thể viết tay một `speaker_selection_method`nhưng mặc định là LLM-driven.
- **Agno** đại lý quyết định công cụ nào để gọi tiếp theo.

### Câu hỏi khả năng quan sát

>  quan sát

- **LangGraph** OpenTelemetry thông qua LangSmith hoặc bất kỳ nhà xuất khẩu OTel nào. Mỗi chuyển đổi nút là một khoảng thời gian theo dõi; các điểm kiểm soát gấp đôi như các dấu vết có thể chơi lại. LangSmith là tùy chọn bên đầu tiên; Langfuse / Phoenix cũng có bộ điều chỉnh.
  **LangGraph** Thông qua LangSmith hoặc bất kỳ OTel 导出器的 OpenTelemetry。 mỗi节点转换是一个追踪跨度;检查点兼作重放追踪。
- **CrewAI** OpenTelemetry hạng nhất kể từ cuối năm 2025; tích hợp với Langfuse, Phoenix, Opik, AgentOps.
  **CrewAI**2025 年末起一等公民OpenTelemetry;集成 Langfuse、Phoenix、Opik、AgentOps。
- **AutoGen** Tích hợp OpenTelemetry thông qua `autogen-core`- AgentOps và Opik có các kết nối.
  **AutoGen** qua `autogen-core`của OpenTelemetry 集成;AgentOps 和 Opik có kết nối.
- **Agno** tích hợp `monitoring=True`cờ cộng với các nhà xuất khẩu OpenTelemetry; tích hợp chặt chẽ với Langfuse cho các dấu vết phiên.
  **Agno**内置 `monitoring=True`标志加 OpenTelemetry 导出器;与 Langfuse 紧密集成会话追踪──

### Chi phí và thời gian trễ

Tất cả bốn khung đều thêm chi phí chung mỗi cuộc gọi (điều logic khung, xác thực, phân phối hàng loạt).`GroupChatManager`LangGraph chỉ dùng token khi bạn viết.`llm.invoke`Con đường của Agno chỉ đơn độc là mỏng.

> Bốn khung đều tăng mỗi lần được gọi                                                                                                                                                                                                                                                           

Khi chi phí cho mỗi chạy quan trọng, thích định tuyến rõ ràng (LangGraph edges, AutoGen `speaker_selection_method`) trên LLM chọn đường dẫn.

> Khi chi phí vận hành mỗi lần quan trọng, ưu tiên sử dụng đường lộn rõ ràng thay vì đường lựa chọn LLM.

### Sự tương tác

> 互操作性

- **LangGraph** **LangChain**Công cụ, máy lấy lại, LLM. Cấu hình MCP hạng nhất (các công cụ được nhập khẩu như máy chủ MCP).
  **LangGraph** **LangChain**工具、检索器、LLM──一等公民 MCP 适配器(工具作为 MCP 服务器导入)
- **CrewAI** các công cụ thừa kế từ `BaseTool`; Các công cụ LangChain, các công cụ LlamaIndex và các công cụ MCP đều thích nghi.`allow_delegation=True`- Tôi không biết.
  **CrewAI** 工具继承自 `BaseTool`LongChain 工具、LlamaIndex 工具、MCP 工具都适配进来──Crew-to-crew 委派通过`allow_delegation=True`
- **AutoGen**→ `FunctionTool`bao bọc bất kỳ Python có thể gọi; chuyển đổi MCP có sẵn. kết nối chặt chẽ với hệ sinh thái AG2 cho các mô hình đại lý đến đại lý.
  **AutoGen**→ `FunctionTool`包装 bất kỳ Python nào có thể điều chỉnh; MCP 适配器可用──与 AG2 生态紧密合合用于 Agent 间模式──
- **Agno**→ `@tool`thiết kế trang trí hoặc phân loại BaseTool; bộ điều chỉnh MCP; các công cụ có thể được chia sẻ giữa các đại lý và nhóm.
  **Agno**→ `@tool`装饰器或BaseTool 子类;MCP 适配器;工具可跨 Agent 和团队共享──

## Khả năng

> Bạn có thể giải thích, trong một câu, tại sao một khung nhất định là phù hợp với một vấn đề đặc vụ nhất định.
> Bạn có thể sử dụng một câu để giải thích tại sao một khuôn khổ nào đó phù hợp với một vấn đề của một đại lý.

Danh sách kiểm tra trước khi xây dựng:

> 构建前检查清单:

1. **Draw the shape.**Đây là một biểu đồ (tiêu trạng thái, tên chuyển đổi), một trò chơi vai trò (người chuyên gia giao công việc), một trò chuyện (nhà nhân nói chuyện cho đến khi hoàn thành), một đại lý duy nhất với công cụ?
   **画出形状。**Đây là một hình ảnh, trò chuyện, hay là một nhân viên đơn thuần?
2. **Decide who branches.**Các phân nhánh được quyết định bởi nhà phát triển → LangGraph. Manager-agent-decided → CrewAI hierarchical. Chat-emergent → AutoGen. Tool-call-decided → Agno.
   **决定谁分支。**开发者决定 → LangGraph──经理 Agent决定 → CrewAI──聊天涌现 → AutoGen──工具调用决定 → Agno──
3. **Check the state budget.**Bạn cần tiếp tục từ điểm kiểm tra? Du lịch thời gian? Con người gián đoạn giữa chạy? Nếu có, LangGraph là mặc định; các phiên Agno bao gồm trạng thái được mở rộng bằng cuộc trò chuyện.
   **检查状态预算。**Bạn cần hồi phục từ điểm kiểm tra thời gian đi du lịch?
4. **Check the cost budget.**Các đường dẫn được chọn bởi LLM chi phí thêm token mỗi lượt. Nếu đại lý chạy hàng ngàn lần một ngày, thích đường dẫn rõ ràng.
   **检查成本预算。**LLM 选择的路由每轮额外消耗代币──
5. **Budget the framework overhead.**Mỗi framework là một sự phụ thuộc khác. Nếu nhiệm vụ là hai cuộc gọi LLM và một công cụ, hãy viết 30 dòng Python đơn giản; không khung nào rẻ hơn không khung nào.
   **预算框架开销。**Mỗi khung là một phụ thuộc khác. Nếu nhiệm vụ chỉ là hai lần LLM 调用 một công cụ, viết 30 行纯 Python.

Không muốn tìm ra một khung hình trước khi bạn có thể vẽ biểu đồ, biểu đồ tổ chức, trò chuyện, hoặc hộp đại lý.

> Trước khi bạn có thể vẽ, tổ chức, trò chuyện hoặc khung đại lý, đừng kéo dài khung hình. Đừng chọn một cái gì đó buộc bạn phải chiến đấu cho mô hình trạng thái của nó.

## Matrix quyết định

| Problem shape | Preferred framework | Why |
|---------------|---------------------|-----|
| Workflow DAG with typed state, human approvals, long-running | LangGraph | First-class state, checkpointer, interrupts, time-travel. |
| Research / writing pipeline with distinct roles | CrewAI (sequential) or LangGraph subgraphs | Role-per-task is cheap to express in CrewAI; scale up with LangGraph when branching gets complex. |
| Proposer-critic or teacher-student dialogue | AutoGen | Two-agent chat is its native shape. |
| Single agent with tools, sessions, memory | Agno | Thinnest setup, built-in storage and memory. |
| Thousands of parallel fanouts with reducers | LangGraph + `Send` | The only one with a first-class parallel-dispatch API. |
| Quick prototype, no framework commitment | Plain Python + provider SDK | No framework is the fastest framework. |

| 问题形状 | 推荐框架 | 原因 |
|---------|---------|------|
| 类型化状态的工作流 DAG、人工审批、长期运行 | LangGraph | 一等公民状态、检查点、中断、时间旅行 |
| 研究写作流水线带不同角色 | CrewAI（顺序）或 LangGraph 子图 | CrewAI 表达每任务角色便宜；分支复杂时用 LangGraph |
| 提议者-评论者或师生对话 | AutoGen | 双 Agent 聊天是其原生形状 |
| 单 Agent 带工具、会话、记忆 | Agno | 最薄设置，内置存储和记忆 |
| 数千并行扇出带 reducer | LangGraph + `Send` | 唯一带一等公民并行分派 API 的 |
| 快速原型、不绑定框架 | 纯 Python + 提供商 SDK | 无框架是最快的框架 |

## Tập luyện bài tập
```figure
l5-framework-fit
```

## Các bài tập

1. **Easy.**Hãy thực hiện cùng một nhiệm vụ  "phát tích trụ sở của Anthropic, viết một bản tóm tắt 200 từ, trích dẫn các nguồn"  và thực hiện nó trong LangGraph (bốn nút: lập kế hoạch, tìm kiếm, viết, trích dẫn) và trong CrewAI (ba vai trò: nhà nghiên cứu, nhà văn, biên tập viên).
   Sử dụng cùng một nhiệm vụ trong LangGraph và CrewAI để thực hiện, báo cáo số lượng mã hóa và mã hóa của mỗi lần chạy.
2. **Medium.**Xây dựng nhiệm vụ tương tự trong AutoGen (phát tích  writer chat, biên tập viên tham gia qua `GroupChat`) và Agno (một đại lý duy nhất với `search_tools`và `write_tools`, cộng với một cửa hàng phiên bản). Đánh xếp bốn thực thi trên (a) chi phí mỗi chạy, (b) khả năng tiếp tục sau khi xảy ra tai nạn, (c) khả năng tiêm sự chấp thuận của con người trước bước viết.
   Trong AutoGen và Agno thực hiện cùng một nhiệm vụ, theo chi phí, khả năng phục hồi, khả năng phê duyệt nhân tạo, xếp hạng khả năng tiêm.
3. **Hard.**Xây dựng một kịch bản decision tree `pick_framework.py`có một mô tả ngắn gọn về vấn đề (JSON: `{has_typed_state, has_roles, has_dialogue, has_parallel_fanout, needs_resume}`(văn đề xuất với một câu lý do) kiểm tra nó trên sáu trường hợp bạn tự thiết kế.
   构建决策树脚本,根据问题描述返回框架推──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Orchestration | "How the agents coordinate" / "Agent 如何协调" | The layer that decides which node/role/agent runs next. | 编排：决定哪个节点/角色/Agent 下一步运行的层 |
| Durable state | "Resume after a restart" / "重启后恢复" | State that survives process death, attached to a checkpoint or session store. | 持久状态：在进程终止后仍存活的状态 |
| LLM-selected routing | "Let the model decide" / "让模型决定" | A planner LLM picks the next step each turn; flexible but pays tokens on every decision. | LLM 选择路由：规划 LLM 每轮选择下一步 |
| Explicit routing | "Developer decides" / "开发者决定" | A Python function or static edge picks the next step; cheap and auditable. | 显式路由：Python 函数或静态边选择下一步 |
| Crew | "A CrewAI team" / "CrewAI 团队" | Roles + tasks + process (sequential or hierarchical) bound into a single runnable. | Crew：角色+任务+流程绑定成一个可运行单元 |
| GroupChat | "AutoGen's multi-agent chat" / "AutoGen 多 Agent 聊天" | A managed conversation between N agents with a speaker selector. | GroupChat：N 个 Agent 之间的托管对话 |
| Team (Agno) | "Multi-agent Agno" / "多 Agent Agno" | Route / coordinate / collaborate mode over a set of agents. | Team (Agno)：Agent 集合上的路由/协调/协作模式 |
| StateGraph | "LangGraph's graph" / "LangGraph 图" | Typed-state, node, conditional-edge, checkpointer abstraction. | StateGraph：类型化状态、节点、条件边、检查点抽象 |

## Xem thêm 延伸阅读

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)StateGraph, điểm kiểm soát, gián đoạn, du lịch thời gian.
  LangGraph 文档StateGraph、检查点、中断、时间旅行──
- [CrewAI documentation](https://docs.crewai.com/) Đội ngũ, dòng chảy, đại lý, nhiệm vụ, quy trình.
  CrewAI 文档 Crew、Flow、Agent、Task、Process──
- [AutoGen documentation](https://microsoft.github.io/autogen/) ConversableAgent, GroupChat, nhóm, công cụ.
  AutoGen 文档ConversableAgent、GroupChat、teams、tools。
- [Agno documentation](https://docs.agno.com/) Trưởng lý, Nhóm, Luôn lưu lượng, lưu trữ, bộ nhớ.
  Agno 文档Công viên、Đội ngũ、Tổ thông]], lưu trữ, ký ức。
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) thư viện mẫu (sự chuỗi nhanh, định tuyến, song song, nhạc công-người làm việc, đánh giá-tích cực) framework-agnostic.
  Anthropic 关于构建有效代理的模式库,框架无关.
- [Yao et al., "ReAct: Synergizing Reasoning and Acting" (ICLR 2023)](https://arxiv.org/abs/2210.03629) vòng lặp mỗi khung trang phục lên.
  Mỗi khung đều trong gói ReAct vòng lặp văn bản gốc.
- [Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (2023)](https://arxiv.org/abs/2308.08155) Bức giấy thiết kế của AutoGen.
  AutoGen's design essay:
- [Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (UIST 2023)](https://arxiv.org/abs/2304.03442) nền tảng trò chơi vai trò mà các bộ đống nhân vật kiểu CrewAI xây dựng trên.
  CrewAI 风格角色堆所基于的角色扮演基础──
- Giai đoạn 11 · 16 (LangGraph)  khung bài học này đánh giá.
  本课对比的基准框架:
- Giai đoạn 11 · 19 (Tình phản xạ)  một mô hình vẽ sạch sẽ để LangGraph nhưng khó khăn cho CrewAI.
  Một trong LangGraph hiển thị rõ ràng nhưng trong CrewAI mô hình 拙的.
- Giai đoạn 11 · 22 (Sự quan sát sản xuất)  cách sử dụng các thiết bị tùy thuộc vào khung bạn chọn.
  Làm thế nào để bạn chọn bất kỳ khung hình nào để thêm quan sát tính năng.
