# LangGraph  State Machines for Agents  LangGraph: Tình trạng của đại lý
# Máy cơ nhà nước đại lý  Hình đồ, nút, Bàn kiểm soát

> Một vòng ReAct được viết bằng tay là một `while True`. cùng vòng lặp được viết như một biểu đồ rõ ràng là một cái gì đó bạn có thể kiểm soát, gián đoạn, nhánh, và đi qua thời gian.

> **【中文解读】**Chuyện phản ứng là một.`while True` ReAct vòng lặp được viết bằng LangGraph là một mô hình có thể kiểm tra điểm lưu trữ, gián đoạn, phân支, thời gian đi lại.

> **【拓展：LangGraph→Agent工程】**LangGraph là khung quản lý thực hành thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện thực hiện

>  **【前置】**学本节前请先掌握:(1) Giai đoạn 11·09(Tạm dịch gọi);(2) Giai đoạn 14·01(Tạm dịch vòng lặp)  hiểu ReAct 循环;(3) 状态机概念(有限状态机 FSM、节点、边) ――本节会用 `langgraph``langchain-core`

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 14 (Model Context Protocol) | **前置知识:** Phase 11 · 09 (函数调用)、14 (模型上下文协议)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Bạn gửi một đại lý gọi chức năng. Nó hoạt động trong ba lượt, sau đó có một cái gì đó sai: mô hình thử một công cụ trả lại 500, người dùng thay đổi ý kiến của họ giữa nhiệm vụ, hoặc đại lý quyết định hoàn lại một đơn đặt hàng mà không có một người ký.`while True:`bạn không thể tạm dừng nó, bạn không thể xoay lại nó, và bạn không thể phân nhánh ra "vậy nếu mô hình đã chọn công cụ khác".

> Bạn đã phát hành một chức năng để gọi cho Agent. Nó đã làm việc ba vòng, sau đó xuất hiện một vấn đề: mô hình đã thử một công cụ trả lại 500, người dùng thay đổi ý tưởng giữa lúc, hoặc Agent quyết định trả lại mà không có chữ ký nhân tạo.`while True:`循环没有子──你不能暂停它、倒回它、或分支到" Nếu mô hình chọn một công cụ khác thì sẽ như thế nào"── Một khi bạn phát hành thứ như vậy ra demo, Agent sẽ trở thành một hộp đen──

Bước tiếp theo là rõ ràng khi bạn thấy nó. Trưởng đã là một máy trạng thái  hệ thống nhanh chóng cộng với lịch sử tin nhắn cộng với chờ đợi công cụ gọi cộng với hành động tiếp theo. Làm cho máy trạng thái rõ ràng: nút cho "chương trình nghĩ", "một công cụ chạy", "một con người chấp thuận", và cạnh cho các chuyển đổi điều kiện giữa chúng. Một khi biểu đồ rõ ràng, vòng xoáy nhận được bốn thứ miễn phí: kiểm tra (giữ trạng thái giữa các bước), gián đoạn (phơi lỏng cho con người), phát trực tuyến (điều kiện dòng chảy và các sự kiện trung gian), và du lịch thời gian (lúc lại trạng thái trước và thử một chi nhánh khác).

> Một khi bạn thấy, bước tiếp theo là rõ ràng. Cơ quan chính là một trạng thái. Hệ thống cung cấp thông tin thêm lịch sử.

LangGraph là thư viện gửi trừu tượng này. Nó không phải là một khung đại lý theo nghĩa LangChain ("đây là một AgentExecutor, may mắn"). Đó là một thời gian chạy đồ họa với trạng thái hạng nhất, sự kiên trì hạng nhất và sự gián đoạn hạng nhất.
Việc thực hiện tham chiếu của trừu tượng này là LangGraph. Nó không phải là một khung đại lý theo nghĩa LangChain ("đây là một AgentExecutor, may mắn"). Nó là một thời gian chạy đồ thị với trạng thái hạng nhất, sự kiên trì hạng nhất và sự gián đoạn hạng nhất.

> LangGraph là một bộ thư viện trừu tượng như vậy. Nó không phải là một khung của Agent trong nghĩa LangChain. Nó là một hệ thống có một tình trạng công dân bình đẳng, một tình trạng thường trực của công dân và một tình trạng gián đoạn công dân.


> **【中文解读】**Ưu điểm cốt lõi của LangGraph là hỗ trợ quá trình kiểm soát phức tạp: vòng lặp Công ty 遇到错误时重试) 条件分支 根据任务类型选择不同工具)  的人工审批高风险操作需要人工确认   简单的 LangChain Chain 无法表达这些复杂逻辑

>  **【类比】**Lưu ý ReAct vòng quay như trên tràng hình vẽ vẽ  vẽ xong rồi, dòng chảy một冲就消失──LangGraph 像在白板上画流程图并保存每个节点("模型思考"",工具执行"",人工审批") 和边(条件跳转) đều hiển nhiên, có thể kiểm tra điểm lưu trữ(暂停后继续) 时间旅行(回到某节试点不同分支) 、人工中断(等用户确认)

> ️ **【易错点】**3 个坑 của LangGraph:(1) **状态 schema 太松散**用 `dict`Khi trạng thái 没类型约束,运行时关键 拼错发现不了;用 `TypedDict`或 Pydantic Model 定义 State──(2) **条件边写得太复杂** một cạnh 函数里 if/other 嵌套 5 层,调试地狱;拆成多个简单边 函数,每个返回单一节点名――(3) **checkpoint 用 SQLite 不持久化** Khởi động lại tình trạng dịch vụ bị mất; sản xuất sử dụng Postgres hoặc Redis làm điểm kiểm soát.


## Khái niệm cốt lõi

> **【中文解读】**LangGraph sẽ LLM Agent 建模为状态机(State Machine): xác định trạng thái节点(如检索,生成,验证) và chuyển đổi边 (转换边) ◎条件分支) ⋅相比简单的链式调用,状态机支持循环、条件分支、人工审批等复杂控制流──

> **【拓展：LangGraph 与 Agent 编排】**LangGraph là một bộ phận của nhóm LangChain được đưa ra.


![LangGraph StateGraph: nodes, edges, and the checkpointer](../assets/langgraph-stategraph.svg)

A `StateGraph`có ba điều.

> `StateGraph`Có 3 thứ.

1. **State.**Một dict được gõ (TypedDict hoặc mô hình Pydantic) chảy qua biểu đồ. Mỗi nút nhận được trạng thái đầy đủ và trả lại một bản cập nhật một phần, mà LangGraph hợp nhất bằng cách sử dụng một * giảm * cho mỗi trường `operator.add`cho các danh sách nên tích lũy, ghi lại theo mặc định.
   **状态。**流过图的类型化字典──每个节点接收完整状态并返回部分更新──
2. **Nodes.**Phụng chức năng Python `state -> partial_state`Mỗi bước là một bước riêng biệt: " gọi mô hình, " " chạy công cụ, " " tóm tắt. "
   **节点。**Python 函数 `state -> partial_state` mỗi một bước chia rẽ
3. **Edges.**Chuyển đổi giữa các nút. Biên tĩnh đi một chỗ. Biên điều kiện có chức năng router`state -> next_node_name`Vì vậy, biểu đồ có thể phân ngành trên đầu ra mô hình.
   **边。**节点之间的转换――静态边去一个地方――条件边接受路由函数以在模型输出上分支――

Bạn biên soạn biểu đồ. biên soạn liên kết topology, gắn một điểm kiểm tra (tự chọn nhưng cần thiết cho sản xuất), và trả lại một runnable. Bạn gọi nó với một trạng thái ban đầu và một `thread_id`Mỗi bước hành quyết đều là một điểm kiểm soát được khóa vào`(thread_id, checkpoint_id)`- Tôi không biết.

> Bạn biên dịch图. 编译绑定拓、附加检查点器并返回一个可运行对象. Bạn sử dụng trạng thái ban đầu và `thread_id`调用它. 执行的每一步都会持久化一个检查点.

### Bốn siêu cường

**Checkpointing.**Mỗi chuyển đổi nút viết trạng thái mới vào một cửa hàng (trong bộ nhớ cho các thử nghiệm, Postgres / Redis / SQLite cho prod).`thread_id`Chữ đồ họa bắt đầu từ nơi nó dừng lại.

> **检查点。**Mỗi node chuyển đổi sẽ viết vào kho lưu trữ mới.`thread_id`Tái sử dụng lại để phục hồi.

**Interrupts.**Đánh dấu một nút với `interrupt_before=["human_review"]`và thực thi dừng lại trước khi nút đó chạy. trạng thái vẫn tồn tại. API của bạn trả lời người dùng với "đợi phê duyệt". Một yêu cầu sau đó cho cùng `thread_id`với `Command(resume=...)`bắt đầu hành quyết.

> **中断。**用 `interrupt_before`标记一个节点,执行在该节点运行前停止――状态被持久化――后续请求可恢复执行――

**Streaming.** `graph.stream(state, mode="updates")`đưa ra các vùng Delta như chúng xảy ra. `mode="messages"`truyền các token LLM bên trong các nút mô hình. `mode="values"`bạn chọn những gì sẽ xuất hiện trong UI của bạn.

> **流式输出。** `graph.stream`按发生顺序产出状态增量──你选择在 UI中显示什么──

**Time-travel.** `graph.get_state_history(thread_id)`trả lại toàn bộ nhật ký kiểm soát.`checkpoint_id`đến`graph.invoke`Và bạn đi từ đó. Rất tốt cho debugging ("như thế nào nếu mô hình đã chọn công cụ B thay vào đó?") và cho các thử nghiệm hồi quy để chơi lại các dấu vết sản xuất.

> **时间旅行。**Trở lại toàn bộ kiểm tra điểm nhật ký.`checkpoint_id`, bạn từ đó phân chia điểm.

### Các giảm là điểm

Mỗi trường trạng thái có một reducer. Hầu hết các mặc định đều ổn  một giá trị mới ghi lại giá trị cũ. Nhưng danh sách tin nhắn cần `operator.add`để các tin nhắn mới được thêm vào thay vì thay thế. Biên song song kết kết hợp cập nhật của họ thông qua giảm. Nếu hai nút cả hai cập nhật `messages`Và anh quên `Annotated[list, add_messages]`, thứ hai thắng im lặng và bạn mất một nửa lượt.

> Mỗi trạng thái có một bộ giảm đi.`operator.add`Để thêm thông tin mới thay vì thay thế. Reducer là thứ duy nhất nhỏ bé trong kho này.

### Chữ đồ thị ReAct trong bốn nút

Một đại lý ReAct sản xuất là bốn nút và hai cạnh:

> Một đại lý ReAct cấp sản xuất là bốn điểm và hai bên:

1. `agent` gọi LLM với lịch sử tin nhắn hiện tại. Trả lại tin nhắn trợ lý (có thể chứa tool_calls).
2. `tools` thực hiện bất kỳ tool_call nào trong thông điệp trợ lý cuối cùng, thêm kết quả công cụ như thông điệp công cụ.
3. Một cạnh điều kiện từ `agent`đường này đến `tools`nếu tin nhắn cuối cùng có tool_calls, nếu không thì `END`- Tôi không biết.
4. Một cạnh tĩnh từ `tools`quay lại `agent`- Tôi không biết.

Bạn có được vòng lặp ReAct đầy đủ (Think → Action → Observation → Thought → ...) với kiểm soát, gián đoạn và phát trực tuyến, trong khoảng 40 dòng mã.

> Chính vì vậy. Bạn đã có được hoàn chỉnh ReAct vòng tròn (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (REC) (R) (REC) (REC) (R) (REC) (R) (REC) (R) (REC) (R) (REC) (R) (REC) (R) (REC) (R) (R) (REC) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R)

### StateGraph vs Send (phân tích)

`Send(node_name, state)`cho phép một nút gửi các tiểu hình song song. ví dụ: đại lý quyết định truy vấn ba máy tìm kiếm cùng một lúc. Mỗi `Send`tạo ra một thực hiện song song của nút mục tiêu; các sản phẩm của chúng hợp nhất thông qua nhà giảm trạng thái. Đây là cách LangGraph thể hiện mô hình nhạc công-người làm việc mà không cần threading nguyên thủy.

> `Send(node_name, state)`Hãy để một điểm phân chia và đi theo.`Send`生成目标节点的并行执行;它们的输出通过状态减小器合并──

### Các phụ đề

Một biểu đồ được biên soạn có thể là một nút trong biểu đồ khác. biểu đồ bên ngoài nhìn thấy một nút duy nhất; biểu đồ bên trong có trạng thái riêng của nó và các điểm kiểm soát riêng của nó. Đây là cách các nhóm xây dựng các đại lý người giám sát: biểu đồ giám sát định hướng ý định của người dùng đến một tiểu biểu đồ người lao động trên mỗi miền.

> 编译后图可以是另一个图中的节点――外层图看到单一节点;内层图有自己的状态和检查点――这是团队构建监督员工代理的方法――

## Hãy xây dựng nó.
```figure
l5-state-graph-ledger
```

## Hãy xây dựng nó

### Bước 1: trạng thái và nút

> 步骤 1: trạng thái và điểm

```python
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def agent_node(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State) -> str:
    last = state["messages"][-1]
    return "tools" if getattr(last, "tool_calls", None) else END

tool_node = ToolNode(tools=[search_web, read_file])

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app = graph.compile(checkpointer=MemorySaver())
```

`add_messages`là bộ giảm tính làm cho danh sách tin nhắn tích lũy thay vì ghi lại.

> `add_messages`là để danh sách tin tức tích lũy thay vì không bao phủ giảm.

### Bước 2: chạy với một sợi dây

> 步骤 2: Sử dụng đường dây vận hành.

```python
config = {"configurable": {"thread_id": "user-42"}}
for event in app.stream(
    {"messages": [HumanMessage("find the Anthropic headquarters address")]},
    config,
    stream_mode="updates",
):
    print(event)
```

Mỗi bản cập nhật đều là một lời khuyên.`{node_name: state_delta}`Frontend của bạn có thể phát trực tuyến này đến UI để người dùng thấy "hợp tác viên đang nghĩ... gọi search_web... có kết quả... trả lời".

> Mỗi lần cập nhật là`{node_name: state_delta}`字典──前端可流式传到 UI,让用户看到"agent 思考中... 调用 search_web... 得到结果... 回答中"──

### Bước 3: thêm một người trong vòng cắt đứt

Đánh dấu một nút để thực thi dừng lại trước khi nó chạy.

> 步骤 3: 添加人机协作中断──标记节点使执行其运行前暂停──

```python
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tools"],  # pause before every tool call
)

state = app.invoke({"messages": [HumanMessage("delete the production database")]}, config)
# state["__interrupt__"] is set. Inspect proposed tool calls.
# If approved:
from langgraph.types import Command
app.invoke(Command(resume=True), config)
# If denied: write a rejection message and resume
app.update_state(config, {"messages": [AIMessage("Blocked by human reviewer.")]})
```

Tình trạng, điểm kiểm soát và dây liên tục tồn tại trong suốt thời gian gián đoạn.

> 状态, kiểm tra điểm và đường dây trong thời gian gián đoạn hoàn toàn tồn tại.

### Bước 4: thời gian đi du lịch để debugging

> 步骤 4:调试使用时间旅行──

```python
history = list(app.get_state_history(config))
for snapshot in history:
    print(snapshot.values["messages"][-1].content[:80], snapshot.config)

# Fork from a prior checkpoint
target = history[3].config  # three steps back
for event in app.stream(None, target, stream_mode="values"):
    pass  # replay from that point forward
```

Đi qua `None`khi đầu vào lặp lại từ điểm kiểm soát được cung cấp; vượt qua một giá trị thêm nó như một cập nhật cho trạng thái của điểm kiểm soát đó trước khi tiếp tục. Đây là cách bạn tái tạo một hành động xấu chạy mà không chạy lại toàn bộ cuộc trò chuyện.

> 传入 `None`作为输入从给定的检查点重放;传入值则在恢复前将其作为更新添加到该检查点的状态――这就是如何在不重新运行整个对话的情况下复现一个错误的代理运行――

### Bước 5: Thay đổi điểm kiểm soát cho sản xuất

> 步骤 5: sản xuất môi trường thay thế kiểm tra điểm.

```python
from langgraph.checkpoint.postgres import PostgresSaver

with PostgresSaver.from_conn_string("postgresql://...") as checkpointer:
    checkpointer.setup()
    app = graph.compile(checkpointer=checkpointer)
```

SQLite, Redis, và Postgres đã được vận chuyển. `MemorySaver`Bất cứ thứ gì tồn tại sau khi khởi động lại đều cần một cửa hàng thực sự.

> SQLite、Redis 和 Postgres 已提供──`MemorySaver`Để thử nghiệm, bất cứ thứ gì cần được khởi động lại đều cần lưu trữ thực sự.

## Khả năng

> Bạn xây dựng các đại lý như đồ thị, không như `while True`- Các vòng lặp.
> Anh đã tạo ra một đại lý, chứ không phải là một đại lý.`while True`Chuyện này

Trước khi bạn tìm thấy LangGraph, hãy thiết kế 60 giây:

> Trong khi sử dụng LangGraph  trước, làm một thiết kế 60 giây:

1. **Name the nodes.**Mỗi quyết định riêng biệt hoặc hành động tác động phụ là một nút. "Điều đại lý nghĩ", "công cụ chạy", "đánh giá chấp thuận", "thường xuyên phản hồi". Nếu bạn không thể liệt kê chúng, nhiệm vụ vẫn chưa có hình dạng đại lý.
   **命名节点。**Mỗi quyết định chia tay hoặc động tác phụ đều là một điểm.
2. **Declare the state.**Tối thiểu TypedDict với một giảm cho mỗi trường danh sách. Đừng nhồi tất cả mọi thứ vào `messages`; nâng các lĩnh vực cụ thể về nhiệm vụ (một công việc)`plan`, một `budget`đếm, một `retrieved_docs`(Dân trí) đến cấp cao nhất.
   **声明状态。**n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n
3. **Draw the edges.**Static trừ khi bước tiếp theo phụ thuộc vào đầu ra mô hình. Mỗi cạnh điều kiện cần một chức năng router với các nhánh được đặt tên.
   **画边。**Trừ khi bước tiếp theo phụ thuộc vào mô hình xuất, nếu không sử dụng bên tĩnh.
4. **Choose a checkpointer up front.** `MemorySaver`cho các thử nghiệm, Postgres/Redis/SQLite cho bất cứ điều gì khác. Không vận chuyển mà không có một  không kiểm tra chỉ có nghĩa là không có hồ sơ, không gián đoạn, không có thời gian đi du lịch.
   **提前选择检查点器。**测试用 `MemorySaver`, khác dùng Postgres/Redis/SQLite。
5. **Decide interrupts before tools run, not after.**Sự chấp thuận đi vào cạnh vào một nút tác dụng phụ để bạn có thể hủy trước khi gây hại; xác thực đi vào cạnh ra khỏi mô hình để bạn có thể từ chối cuộc gọi xấu rẻ.
   **在工具运行之前决定中断，而不是之后。**
6. **Stream by default.** `mode="updates"`cho UI, `mode="messages"`cho các dòng chảy cấp token bên trong các nút mô hình, `mode="values"`cho các bức ảnh chụp toàn bộ trong quá trình đánh giá.
   **默认使用流式输出。**

Không gửi một đại lý LangGraph mà không có điểm kiểm soát. Không gửi một đại lý mà gián đoạn sau tác dụng phụ. Không gửi một`messages`trường không có `add_messages`như là chất giảm.

> 拒绝发布没有检查点器的 LangGraph Agent──拒绝发布后中断的 Agent──拒绝发布没有`add_messages`作为减轻的 `messages`字段。

## Tập luyện bài tập

1. **Easy.**Thực hiện biểu đồ ReAct bốn nút trên với một công cụ máy tính và một công cụ tìm kiếm web.`list(app.get_state_history(config))`trả lại ít nhất bốn điểm kiểm soát cho một cuộc trò chuyện hai vòng.
   **简单。**实现上述四节点 ReAct图,验证检查点历史记录──
2. **Medium.**Thêm một `planner`nút chạy trước `agent`và viết một cấu trúc`plan: list[str]`- Tôi đã đi vào tiểu bang.`agent`Đánh dấu các bước kế hoạch như đã thực hiện.`plan`bị mất qua một hồ sơ kiểm soát (trầm giảm).
   **中等。**Thêm một trong `agent`之前运行的 `planner`节点,写入结构化计划到状态.
3. **Hard.**Xây dựng một biểu đồ giám sát mà đường dẫn giữa ba biểu đồ phụ (`researcher`- `writer`- `reviewer`) sử dụng `Send`Mỗi phụ lục có trạng thái và điểm kiểm soát riêng của nó.`interrupt_before=["writer"]`trên biểu đồ bên ngoài để một con người có thể chấp thuận nghiên cứu ngắn. xác nhận rằng thời gian đi từ một điểm kiểm soát trước đó chạy lại chỉ là chi nhánh.
   **困难。** xây dựng một giám sát viên 图, trong ba mô hình  sử dụng `Send`路由──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| StateGraph | "The LangGraph graph" / "LangGraph 图" | The builder object you add nodes and edges to before compile. | StateGraph：编译前添加节点和边的构建器对象 |
| Reducer | "How the field merges" / "字段如何合并" | A function `(old, new) -> merged` applied when a node returns an update for that field; default is overwrite, `add_messages` appends. | Reducer：节点返回更新时应用的合并函数 |
| Thread | "A conversation ID" / "对话 ID" | A `thread_id` string that scopes all checkpoints for one session. | Thread：限定一个会话所有检查点的 thread_id 字符串 |
| Checkpoint | "A paused state" / "暂停的状态" | A persisted snapshot of the full graph state after a node transition, keyed on `(thread_id, checkpoint_id)`. | Checkpoint：节点转换后持久化的完整图状态快照 |
| Interrupt | "Pause for a human" / "暂停等人工" | `interrupt_before` / `interrupt_after` stop execution at a node boundary; resume with `Command(resume=...)`. | Interrupt：在节点边界停止执行，可恢复 |
| Time-travel | "Fork from a prior step" / "从先前步骤分叉" | `graph.invoke(None, config_with_old_checkpoint_id)` replays from that checkpoint forward. | Time-travel：从先前检查点重放 |
| Send | "Parallel subgraph dispatch" / "并行子图分派" | A constructor a node can return to spawn N parallel executions of a target node. | Send：节点返回以生成 N 个并行执行的构造器 |
| Subgraph | "A compiled graph as a node" / "编译后的图作为节点" | A compiled StateGraph used as a node in another graph; preserves its own state scope. | Subgraph：作为另一个图中节点使用的编译后 StateGraph |

## Xem thêm 延伸阅读

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) tham chiếu kinh điển cho StateGraph, giảm, kiểm tra và gián đoạn.
  LangGraph 文档StateGraph、reducer、检查点器和中断的权威参考──
- [LangGraph concepts: state, reducers, checkpointers](https://langchain-ai.github.io/langgraph/concepts/low_level/) mô hình tâm lý bài học này sử dụng, trực tiếp từ nguồn.
  LangGraph 概念: trạng thái, giảm tính, kiểm tra điểm.
- [LangGraph Persistence and Checkpoints](https://langchain-ai.github.io/langgraph/concepts/persistence/) chi tiết về các cửa hàng Postgres/SQLite/Redis, không gian tên điểm kiểm soát và ID chuỗi.
  LangGraph 持久化和检查点详细――
- [LangGraph Human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/) `interrupt_before`- `interrupt_after`- `Command(resume=...)`, và các edit-state pattern.
  LangGraph 人机协作断和复习 模式──
- [Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023)](https://arxiv.org/abs/2210.03629) mô hình mà mỗi đại lý LangGraph thực hiện; đọc nó để lý luận lý luận.
  Mỗi đại lý LangGraph thực hiện ReAct Mode.
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) hình dạng biểu đồ nào ( chuỗi, bộ định tuyến, nhạc công, đánh giá- tối ưu hóa) để thích và khi nào.
  Nhân văn về lựa chọn hình dạng và khi sử dụng hướng dẫn
- Giai đoạn 11 · 09 (Tạm dịch gọi)  các công cụ gọi nguyên thủy mỗi nút đại lý LangGraph sử dụng lại.
  第 11 阶段 · 09(函数调用)每个 LangGraph Agent 节点重用工具调用原语。
- Giai đoạn 11 · 14 (Mô hình Công thức ngữ cảnh)  phát hiện công cụ bên ngoài kết nối vào một LangGraph `ToolNode`qua bộ chuyển đổi MCP.
  第 11 阶段 · 14(MCP) 通过MCP 适配器插入 LangGraph `ToolNode`                                                                                                                                                                                                                                                              
- Giai đoạn 11 · 17 (Tương đương với cơ sở quản lý của các đại lý)  khi nào chọn LangGraph thay vì CrewAI, AutoGen hoặc Agno.
  第 11 阶段 · 17(Agent 框架对比) 何时选择 LangGraph。
