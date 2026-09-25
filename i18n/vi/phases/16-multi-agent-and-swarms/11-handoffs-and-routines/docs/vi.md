# Handoffs và thói quen  Phong nhạc vô quốc tịch 编排 交接 例程 状态

> OpenAI Swarm ( Tháng 10 năm 2024) đã chưng cất dàn nhạc đa đại lý cho hai nguyên thủy: **routines**(các hướng dẫn + công cụ như một lời nhắc hệ thống) và **handoffs**(một công cụ đưa một nhân viên khác về). Không có máy nhà nước, không có DSL nhánh  các tuyến LLM bằng cách gọi công cụ giao hàng đúng. OpenAI Agents SDK (March 2025) là kế thừa sản xuất. Swarm chính nó vẫn là tham chiếu khái niệm sạch nhất  toàn bộ nguồn của nó phù hợp với một vài trăm dòng. Mô hình này là viral bởi vì bề mặt API là "agent = prompt + tools; handoff = function returning agent".

> **【中文解读】**Phần này giới thiệu các quy trình và quy trình giao tiếp giữa các đại lý truyền tải quyền kiểm soát nhiệm vụ.

> **【拓展：handoffs and routines→具体应用】**交接(Handoffs) là khái niệm cốt lõi của OpenAI Agents SDKAgent A sẽ chuyển quyền kiểm soát sang Agent B。关键设计决策:(1) 上下文传递B 收到多少 A 的历史?(2) 恢复机制B 完成后控制权回到 A 还是交给 C?(3) 超时处理B 如果卡住怎么办?


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 16·04(原语模型)、Phase 14·07(工具调用)。OpenAI Swarm 把多 Agent 简化为2 原语:routine(系统提示+工具)+ handoff(返回另一个代理的工具)。
>  **【类比】**Handoff = "客服转接"──用户问技术问题→客服 A 接听→判断需要技术支持→转接给技术专员 B。Swarm 的天才之处:handoff 就是一个普通工具调用(回复代理),LLM 自动路由──无状态机、无 DSL,几百行代码搞定──OpenAI Agents SDK 是生产版本──

##                                                                                                                                                                                                                                                               

Mỗi framework đa đại lý muốn bạn học được DSL của nó: Lớp nối LangGraph và cạnh, CrewAI và nhiệm vụ, AutoGen GroupChat và quản lý. DSL là trừu tượng thực sự, nhưng chúng làm cho việc cảm thấy nặng hơn nó cần phải là.

> Mỗi nhiều cơ quan  framework đều muốn bạn học được các thiết bị của DSL: LongGraph, nhóm và nhiệm vụ của CrewAI, GroupChat và quản lý của AutoGen.

DSL Lock-in là thuế khung đa đại lý. Mỗi DSL có khái niệm riêng của nó, công cụ gỡ lỗi riêng của nó, cộng đồng riêng của nó. Một khi bạn cam kết, di chuyển là tốn kém. Swarm đặt cược: bỏ qua DSL hoàn toàn, sử dụng các công cụ gọi hiện có của mô hình.

> DSL 锁定是多代理 框架税── mỗi DSL có khái niệm riêng, công cụ điều tra riêng, cộng đồng riêng.

Swarm đẩy theo hướng ngược lại: sử dụng khả năng gọi công cụ mà mô hình đã có. Handoffs trở thành gọi công cụ.

> Swarm 推向相反的方向: sử dụng các mô hình có sẵn công cụ调用能力──交接变成工具调用──编排器就是当前持有对话的代理──状态机隐含在代理的系统提示中.

Nhìn sâu sắc: bạn không cần một DSL dàn nhạc vì LLM đã là dàn nhạc viên. Mỗi cuộc gọi LLM quyết định những gì phải làm tiếp theo dựa trên bối cảnh. Handoffs chỉ phơi bày quyết định đó như một công cụ mô hình có thể gọi.

> 洞察深刻:你不需要编排 DSL,因为 LLM 已经是编排器. Mỗi lần LLM 调用 dựa trên các tiêu đề sau để quyết định bước tiếp theo.

## Khái niệm cốt lõi

### Hai nguyên thủy

**Routine.**Một lệnh hệ thống xác định vai trò của một đại lý và các công cụ có sẵn. Hãy nghĩ về nó như một bộ hướng dẫn có mục tiêu: "bạn là một đại lý phân loại; nếu người dùng hỏi về hoàn lại, hãy giao cho đại lý hoàn lại".

> **例程。**定义 Agent 角色和可用工具的系统提示――把它想象成一组范围化的命令:" bạn là một đại lý phân诊; nếu người dùng hỏi về khoản thanh toán, giao tiếp với Đại lý thanh toán――"

**Handoff.**Một công cụ mà đại lý có thể gọi mà trả về một đối tượng mới của đại lý. thời gian chạy Swarm phát hiện giá trị trả về của đại lý và chuyển đổi đại lý hoạt động cho lượt tiếp theo.

> **交接。**Trình tác nhân có thể được điều chỉnh, trả lại một Trình tác nhân mới đối tượng.

Đó là toàn bộ sự trừu tượng.

> Đó là toàn bộ sự trừu tượng.

```
def transfer_to_refunds():
    return refund_agent  # Swarm sees Agent return → switch active agent

triage_agent = Agent(
    name="triage",
    instructions="Route the user to the right specialist.",
    functions=[transfer_to_refunds, transfer_to_sales, transfer_to_support],
)
```

Các thông báo hệ thống của đại lý phân loại cho phép nó chọn giao hàng đúng dựa trên thông điệp của người dùng.

> 分诊 Agent's system提示 cho phép nó dựa trên thông tin của người dùng chọn đúng giao tiếp.

Đây là động thái thanh lịch: tái sử dụng cơ sở hạ tầng gọi công cụ hiện có của mô hình cho việc dàn xếp. Không DSL mới, không biên tập đồ thị, không máy trạng thái. mô hình đã biết cách chọn công cụ đúng; giao hàng chỉ là công cụ trả lại các đại lý.

> Đây là một sáng kiến của U雅: sử dụng các công cụ hiện có của mô hình để điều chỉnh cơ sở hạ tầng. Không có DSL mới, không có biên tập viên hình ảnh, không có cơ chế trạng thái.

### Tại sao nó là virus

- **Small API.**Hai khái niệm cần học.
  Trung ngữ翻译:**小型 API。**Chỉ cần học hai khái niệm.
- **Uses what the model already does.**Việc gọi công cụ đã được cấp sản xuất trên các nhà cung cấp.
  Trung ngữ翻译:**使用模型已有的能力。**工具调用在各供应商中已经是生产级.
- **No state-machine burden.**Bạn không mô tả biểu đồ; các thông báo của các đại lý mô tả họ giao cho ai.
  Trung ngữ翻译:**无状态机负担。**Bạn không mô tả hình ảnh; Tiêu đề của đại lý mô tả chúng giao tiếp với ai.

### Thương mại vô quốc tịch

Swarm là một hệ thống không có chính sách giữa các lần chạy. Framework lưu trữ lịch sử tin nhắn trong một lần chạy, nhưng nó không tồn tại bất cứ điều gì.

> Swarm trong các hoạt động thực sự không có trạng thái.

Thiết kế không có nhà nước là có ý định: nó làm cho khung lại trivially khởi động, có thể mở rộng ngang, và debuggable (mỗi chạy là độc lập). chi phí là các dòng công việc chạy lâu đòi hỏi quản lý trạng thái bên ngoài (hội dữ liệu, hàng, điểm kiểm soát).

> 无状态设计是有意的: nó làm cho khung hình có thể dễ dàng khởi động lại, mở rộng và điều chỉnh được (每次运行独立) 代价是长时间运行的工作流需要外部状态管理 (数据库,队列,检查点) 代价是长时间运行的工作流需要外部状态管理 (数据库,队列,检查点) 代价是长时间运行的工作流需要外部状态管理 (数据库,队列,检查点) 代价是长时间运行的工作流需要外部状态管理 (数据库,检查点) 代价是长时间运行的工作流需要外部状态管理 (数据库,队列,检查点) 代价是长时间运行的工作流需要外部状态管理 (数据库,检查点) 代价是长时间运行的工作流需要的状态的状态的状态的状态的状态的状态的状态的状态是很容易的

Trong sản xuất (OpenAI Agents SDK, tháng 3 năm 2025) đây là một trong những điều chính đã thay đổi: SDK thêm vào quản lý phiên tích hợp, hàng rào và theo dõi trong khi giữ cho giao hàng nguyên thủy.

> Trong môi trường sản xuất, OpenAI Agents SDK,2025 năm 3 tháng 3), đây là một trong những thay đổi chính:SDK đã thêm nội dung quản lý, bảo vệ và theo dõi, đồng thời giữ lại giao tiếp nguyên ngữ.

### Khi Swarm/Handoffs phù hợp

- **Triage patterns.**Các đại lý hàng đầu sẽ đưa người dùng đến một chuyên gia.
  Trung ngữ翻译:**分诊模式。**Người dùng sẽ được chuyển đến chuyên gia.
- **Skill-based handoffs.**"Nếu nhiệm vụ cần mã, hãy gọi cho người lập mã; nếu nó cần nghiên cứu, hãy gọi cho nhà nghiên cứu".
  Trung ngữ翻译:**基于技能的交接。**"Nếu nhiệm vụ cần mã, hãy sử dụng bộ mã; nếu cần nghiên cứu, hãy sử dụng nhà nghiên cứu"".
- **Short, bounded conversations.**Hỗ trợ khách hàng, FAQ-to-ticket, các quy trình làm việc đơn giản.
  Trung ngữ翻译:**短、有界对话。**客户支持、FAQ đến đơn giản, đơn giản

### Khi Swarm đấu tranh

- **Long sessions with shared memory.**Handoffs đặt lại trạng thái cuộc trò chuyện vào lịch sử liên tục của nhân viên mới.
  Trung ngữ翻译:**需要共享内存的长会话。**交接将对话状态重置为新代理的提示加历史――没有调用者管理的内存就没有跨代理的持久状态――
- **Parallel execution.**Handoff là một lần trong một thời gian  các chuyển đổi của đại lý hoạt động.
  Trung ngữ翻译:**并行执行。**交接是逐一的活动 交换. 交行性需要调用者编排多个 Swarm 运行.
- **Audit and replay.**Các chạy không có quốc tịch khó để chơi lại chính xác; sự lựa chọn của LLM không xác định.
  Trung ngữ翻译:**审计和回放。**Không có trạng thái vận hành khó xác định; lựa chọn giao tiếp của LLM không chắc chắn.

### OpenAI Agents SDK (March 2025)

Người kế nhiệm sản xuất thêm:

> 生产继任者 thêm thêm:

- **Session state.**Dòng liên tục qua các đường.
  Trung ngữ翻译:**会话状态。**跨运行的持久线程──
- **Guardrails.**Các cái nát xác nhận đầu vào/phản xuất.
  Trung ngữ翻译:**防护栏。**输入/输出验证子。
- **Tracing.**Mọi cuộc gọi và giao hàng đều được ghi lại.
  Trung ngữ翻译:**追踪。**Mỗi lần sử dụng và giao tiếp đều được ghi lại.
- **Handoff filters.**Kiểm soát những gì chuyển ngữ cảnh khi giao tiếp.
  Trung ngữ翻译:**交接过滤器。**控制交接时传输什么 上下文──

Việc giao tiếp nguyên thủy tồn tại; ergonomics sản xuất được thêm vào xung quanh nó.

> 交接原语存活下来;生产人体工程学 xung quanh nó

Đây là tiến trình tiêu chuẩn cho các trừu tượng virus: tàu nguyên thủy đơn giản đầu tiên (Swarm), sản xuất liên quan đến lớp trên (Agents SDK).

> Đây là một bước tiến tiêu chuẩn của virus:先发布简单原语(Swarm),生产关注点在其上层上层上层的Agents SDK) ――原语保持稳定;包装器增长──押注原语──

### Swarm vs GroupChat

Cả hai đều sử dụng định tuyến LLM, nhưng chúng khác nhau về **who picks next**- Có thể là:

> 两者都使用 LLM 驱动的路线, nhưng trong**谁选择下一个**上不同:

- GroupChat: một người chọn ( chức năng hoặc LLM) chọn người phát biểu tiếp theo từ bên ngoài.
  Trung文翻译:GroupChat:选择器(函数或 LLM) từ bên ngoài chọn 下一个发言者──
- Swarm: đại lý hiện tại chọn người kế vị của mình bằng cách gọi một công cụ chuyển giao.
  Trung文翻译:Swarm:当前 Agent 通过调用交接工具选择其继任者──

Swarm là "nhà quyết định những gì tiếp theo"; GroupChat là "hành trướng quyết định những gì tiếp theo". Quyết định của Swarm sống trong cuộc gọi công cụ của đại lý hoạt động; GroupChat sống trong `GroupChatManager`- Tôi không biết.

> Swarm là "Hội ngũ quyết định bước tiếp theo"; GroupChat là "hành động quản lý quyết định bước tiếp theo";;Swarm là quyết định tồn tại trong hoạt động của Agent; GroupChat là tồn tại trong`GroupChatManager`Ở giữa.

Ý nghĩa thực tế: Swarm dễ dàng hơn để gỡ lỗi (để theo các cuộc gọi công cụ của đại lý hoạt động) nhưng khó hạn chế (bất kỳ đại lý nào có thể giao ra bất cứ nơi nào). GroupChat là ngược lại: dễ hạn chế (các chức năng chọn là một nơi để thêm quy tắc), khó khăn hơn để gỡ lỗi (thông lý của người chọn có thể không minh bạch).

> 实际影响:Swarm 更容易调试(跟踪活动 调用工具) nhưng更难约束( bất kỳ 代理 nào có thể giao tiếp ở bất cứ đâu) ――GroupChat 相反:容易约束(选择器函数是添加规则的一个地方),更难调试(选择器的逻辑可能不透明) ――

## Hãy xây dựng nó.
```figure
sw-handoff-routing
```

## Hãy xây dựng nó

`code/main.py`thực hiện Swarm từ đầu: một lớp dữ liệu Agent, một cơ chế chuyển giao (công cụ trả lại Agent), và một vòng chạy phát hiện các chuyển đổi agent.

> `code/main.py`Từ đầu thực hiện Swarm:Công ty 数据类、交接机制(工具返回 代理) và kiểm tra 转换 代理运行循环──

Demo: một đại lý phân loại các tuyến đường để hoàn lại, bán hàng hoặc hỗ trợ các chuyên gia. Mỗi chuyên gia có công cụ riêng của mình.

> 演示:分诊 Agent 路由到退款、销售或支持专家──每个专家都有自己的工具──运行循环打印每次交交交──

Đi chạy:

```
python3 code/main.py
```

## Hãy sử dụng nó để thực hiện

`outputs/skill-handoff-designer.md`thiết kế một topology handoff cho một nhiệm vụ nhất định: những đại lý nào tồn tại, những handoff nào họ có thể gọi, những chuyển giao ngữ cảnh nào.

> `outputs/skill-handoff-designer.md`Để xác định nhiệm vụ thiết kế giao tiếp: những gì đại lý  tồn tại 它们 có thể điều chỉnh những gì giao tiếp 什么上下文传输

## Chuyển nó đi.

Danh sách kiểm tra:

> 检查清单:

- **Handoff logging.**Mỗi giao hàng viết ra một sự kiện theo dõi với từ đại lý, đến đại lý, khung cảnh snapshot.
  Trung ngữ翻译:**交接日志。**Mỗi lần liên lạc ghi lại sự kiện theo dõi, bao gồm từ Agent ∼ Agent ∼ 上下文快照──
- **Context transfer rules.**Quyết định chuyển động nào trên giao hàng: lịch sử đầy đủ (chi phí tốn kém), tin nhắn N cuối cùng, hoặc một tóm tắt.
  Trung ngữ翻译:**上下文传输规则。**quyết định交接时传输什么:完整历史(昂贵) 、最后 N 条消息或摘要──
- **Guardrail on handoff.**Việc giao cho một chuyên gia có quyền công cụ khác nhau phải được xác thực  nếu không, tiêm nhanh có thể buộc phải giao không mong muốn.
  Trung ngữ翻译:**交接防护栏。**交接到具有不同工具权限专家必须得到认证 否则提示注入可以强制不需要交接──
- **Loop detection.**Hai đại lý chuyển về phía trước và về phía sau là một thất bại phổ biến; phát hiện bằng một kiểm tra vòng cuối cùng-K đơn giản.
  Trung ngữ翻译:**循环检测。**Hai đại lý quay lại giao tiếp là thường gặp thất bại; sử dụng đơn giản gần đây K 次环形检查检查.
- **Fallback agent.**Nếu mục tiêu giao không tồn tại, hãy quay lại một mục tiêu không được giao.
  Trung ngữ翻译:**后备 Agent。**Nếu không có mục tiêu kết nối, quay lại giá trị mặc định an toàn.

## Tập luyện bài tập

1. Đi chạy`code/main.py`Hãy xác nhận người hoạt động của vòng hai đã hoàn lại tiền.
   Trung ngữ翻译:运行 `code/main.py`,分诊到退款代理── xác nhận vòng thứ hai của hoạt động
2. Thêm một quy tắc phát hiện vòng: nếu hai đại lý tương tự đã giao 3 lần liên tiếp, buộc một lối thoát. Thiết kế sự lùi.
   Trung ngữ翻译:添加循环检测规则: Nếu hai đại lý giống nhau 连续交接 3 lần,强制退出──设计后备方案──
3. Đọc các tài liệu SDK của OpenAI Agents về bộ lọc giao hàng. Thực hiện một phiên bản "summary-on-handoff": đại lý ra đi nén bối cảnh thành một bản tóm tắt đạn trước khi đại lý tiếp theo tiếp quản.
   Trung ngữ翻译:阅读 OpenAI Agents SDK 关于交接过器的文档──实现"交接时总结"版本:传出 Agent 在传入 Agent 接管之前将上下文缩为要点摘要──
4. So sánh giao dịch Swarm với một chọn GroupChatManager.
   Trung文翻译:比较 Swarm 交接与 GroupChatManager 选择器──哪种模式使提示注入更糟,为什么?
5. Đọc sách nấu ăn của Swarm. Xác định một quyết định thiết kế rõ ràng Swarm đưa ra rằng SDK OpenAI Agents đã thay đổi hoặc được giữ lại.
   Trung文翻译:阅读 Swarm 手册。识别 Swarm做出一个明确设计决策,OpenAI Agents SDK 改变或保留它。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Routine / 例程 | "The agent prompt" / "Agent 提示" | System prompt + tool list. Defines role and available handoffs. / 系统提示 + 工具列表。定义角色和可用交接。 |
| Handoff / 交接 | "Transfer to another agent" / "转移到另一个 Agent" | A tool the active agent can call that returns a new Agent. The runtime switches active agent. / 活动 Agent 可以调用的工具，返回新 Agent。运行时切换活动 Agent。 |
| Stateless / 无状态 | "No memory between runs" / "运行间无记忆" | Swarm does not persist anything; memory is the caller's responsibility. / Swarm 不持久化任何东西；内存是调用者的责任。 |
| Active agent / 活动 Agent | "Who's speaking now" / "现在谁在说话" | The agent currently holding the conversation. Handoff changes this. / 当前持有对话的 Agent。交接改变这个。 |
| Context transfer / 上下文传输 | "What moves on handoff" / "交接时传输什么" | Policy for what history the incoming agent sees: full, last N, or summarized. / 传入 Agent 看到什么历史的策略：完整、最后 N 条或摘要。 |
| Handoff loop / 交接循环 | "Agents ping-pong" / "Agent 乒乓" | Failure mode where two agents keep handing back to each other. / 两个 Agent 持续互相交接的失败模式。 |
| OpenAI Agents SDK | "Production Swarm" / "生产 Swarm" | March 2025 successor; adds sessions, guardrails, tracing on top of the handoff primitive. / 2025 年 3 月继任者；在交接原语之上添加会话、防护栏、追踪。 |
| Handoff filter / 交接过滤器 | "Gate on transfer" / "传输门" | SDK feature to inspect and modify context at the handoff boundary. / 在交接边界检查和修改上下文的 SDK 特性。 |

## Xem thêm 延伸阅读

- [OpenAI cookbook — Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) câu nói tham chiếu
  Trung文翻译:OpenAI 手册  编排 代理:例程和交接  参考阐述
- [OpenAI Swarm repo](https://github.com/openai/swarm) thực hiện ban đầu, được giữ như một tham chiếu khái niệm
  中文翻译:OpenAI Swarm 仓库  原始实现,保留为概念参考
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) người kế nhiệm sản xuất với các buổi và theo dõi
  Trung文翻译:OpenAI Agents SDK 文档  带会话和追踪的生产继任者
- [Anthropic handoff-in-Claude notes](https://docs.anthropic.com/en/docs/claude-code) cách các subagents Claude Code sử dụng mô hình như giao hàng qua `Task`
  Trung文翻译:Anthropic Claude 中的交接说明  Claude Code 子 Agent 如何通过 `Task`Sử dụng mô hình tương tự
