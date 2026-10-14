# LangGraph: Stateful Graphs và Durable Execution
# Stateful Graph Orchestration  Thực hiện lâu dài và các điểm kiểm soát

> Agent là một máy trạng thái; nút là chức năng; cạnh là chuyển đổi; trạng thái được đặt điểm kiểm soát sau mỗi nút. Bắt đầu từ bất kỳ thất bại nào tại điểm kiểm soát thành công cuối cùng. LangGraph là tham chiếu 2026 cho mô hình này của dàn xếp trạng thái cấp thấp.

> **【中文解读】**LangGraph là một sự thực hiện tham chiếu của 2026 năm tầng dưới có trạng thái sắp xếp.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 12 (Workflow Patterns) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 12 (工作流模式)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Mô tả mô hình cốt lõi của LangGraph: máy trạng thái với trạng thái không thay đổi, nút chức năng, cạnh điều kiện và các điểm kiểm tra sau bước.
  Trung ngữ翻译:描述 LangGraph's核心模型:带不可变状态、函数节点、条件边和步后检查点的状态机――
- Mô tả mô hình cốt lõi của LangGraph: máy trạng thái với trạng thái đánh dấu, nút chức năng, cạnh điều kiện và các điểm kiểm tra sau nút.
- Hãy nêu tên bốn khả năng mà các tài liệu nhấn mạnh: thực hiện bền, phát trực tuyến, người trong vòng lặp, bộ nhớ toàn diện.
  Trung ngữ翻译:说出文档强调的四种能力:持久执行、流式传输、人回路中、全面记忆──
- Giải thích ba topology dàn xếp LangGraph hỗ trợ: giám sát, peer-to-peer (swarm), bậc phân cấp (năm subgraph).
  Trung文翻译:解释 LangGraph 支持的三种编排拓:监督者、点对点(群体)、层次化(嵌套子图)。
- Thực hiện biểu đồ trạng thái stdlib với trạng thái không thay đổi, cạnh có điều kiện và chu kỳ kiểm soát/thường hồi.
  Trung ngữ翻译:Use standard库实现带不可变状态、条件边和检查点/恢复周期的状态图──
- Thực hiện biểu đồ trạng thái stdlib với trạng thái nhập, cạnh có điều kiện và chu kỳ kiểm soát/thường hồi.

## Vấn đề  vấn đề giới thiệu

Các đại lý và dòng công việc chia sẻ một vấn đề: khi một lần chạy 40 bước thất bại ở bước 38, bạn muốn tiếp tục từ bước 38, chứ không phải bắt đầu lại. Các mô hình trạng thái hạng hai để cho các nhà điều hành hack lại các thử nghiệm xung quanh thư viện giả định chạy mới.

> Agent 和工作流共享一个问题: Khi 40 bước chạy trong 38 bước thất bại, bạn muốn phục hồi từ 38 bước thay vì bắt đầu.

Câu trả lời thiết kế của LangGraph: trạng thái là một đối tượng đánh chữ hạng nhất, đột biến là rõ ràng, và các điểm kiểm soát tồn tại sau mỗi nút.`load_state(session_id)`gọi.

> Phản ứng thiết kế của LangGraph: trạng thái là một đối tượng loại dải công dân bình đẳng, thay đổi hoạt động là rõ ràng, điểm kiểm tra ở mỗi node sau đó kéo dài.`load_state(session_id)`

> **【中文解读】**Agent 和工作流共享一个问题: Khi 40 bước chạy trong 38 bước thất bại, bạn muốn phục hồi từ 38 bước thay vì bắt đầu từ đầu.`load_state(session_id)`

> **【拓展：LangGraph → 状态图编排】**LangGraph là một sự thực hiện của sự sắp xếp trạng thái ở tầng đáy năm 2026 . Nó sẽ làm cho Agent 建模为状态机节点是函数,边是条件转换,状态在每个步骤后被检查点保存――LangChain là một khung lõi của hệ sinh thái, được sử dụng rộng rãi trong cấp độ sản xuất.

>  **【前置】**必须先掌握:Phase 14·01(Agent Loop) vàPhase 14·12(Anthropic Workflow Patterns) Langgraph chính là "được duy trì" của mô hình dòng làm việc.

## Khái niệm cốt lõi

### Hình đồ

Một biểu đồ được định nghĩa bởi: Một kiểu dict (hoặc mô hình Pydantic) mà mỗi nút đọc và biến đổi.

> 图由以下定义:一个每个节点都读写的带类型 dict (或 Pydantic 模型) ⋅

- **Nodes.**Các chức năng tinh khiết`(state) -> state_update`Các bản cập nhật được hợp nhất thành trạng thái sau khi trở về.
  Trung ngữ翻译:**节点。**纯函数 `(state) -> state_update`更新在返回后合并到状态中
- **Edges.**Chuyển đổi điều kiện hoặc trực tiếp giữa các nút.
  Trung ngữ翻译:**边。**节点之间的条件或直接转换――
- **Entry and exit.** `START`và `END`Các nút Sentinel đánh dấu ranh giới.
  Trung ngữ翻译:**入口和出口。** `START`和 `END`哨兵节点标记边界──

> **【中文解读】**Hình của LangGraph được xác định bởi ba yếu tố: 1)  trạng thái kiểu mỗi节点读写的带类型 dict 或 Pydantic 模型; 2) 节点纯函数`(state) -> state_update`, trả lại giá trị hợp并到状态中; 3) 边节点之间的条件或直接转换──

Ví dụ: một đại lý với `classify`- `refund`- `bug`- `sales`- `done`nút  một dòng công việc định tuyến như một biểu đồ.

> Ví dụ: một chứa `classify``refund``bug``sales``done`节点的代理路由工作流作为图──

### Thực hiện lâu dài

Sau khi mỗi nút trở lại, runtime sẽ xoay quanh trạng thái và viết nó vào một điểm kiểm tra (SQLite, Postgres, Redis, tùy chỉnh).`resume(session_id)`và bắt đầu từ bước N + 1 với trạng thái chính xác.

> Mỗi node trở lại sau, vận hành trong trạng thái chuỗi và viết vào kiểm tra điểm máy (SQLite, Postgres, Redis, tự xác định)`resume(session_id)`Không từ bước N+1 sử dụng trạng thái chính xác tiếp tục.

Các tài liệu LangGraph rõ ràng nhấn mạnh người dùng sản xuất nơi đây quan trọng: Klarna, Uber, JP Morgan.

>  **【类比】**Điểm kiểm tra của LangGraph 像游戏的"自动档档":每过一个关卡(节点) 就自动档一次――第38关 长关 战关,你不需要从第1关重打读第37关的档接下来打就行――生产代理 运行40步长任务在第38步失败时,没有检查点就从头重运(烧代币),有检查点 直接`resume(session_id)`接着干.

> LangGraph 文档 rõ ràng nhấn mạnh đến việc này của người dùng sản xuất: Klarna, Uber, JP Morgan.

### Chuyển phát

Mỗi nút có thể tạo ra một phần đầu ra. biểu đồ truyền các sự kiện delta mỗi nút đến người gọi để UI cập nhật khi biểu đồ chạy.

> Mỗi nút có thể tạo ra một phần xuất khẩu.

### Người trong vòng lặp

Kiểm tra và sửa đổi trạng thái giữa các nút. Thực hiện: tạm dừng trước một nút quan trọng, trạng thái bề mặt cho một con người, chấp nhận sửa đổi, tiếp tục. Điểm kiểm tra làm cho điều này dễ dàng bởi vì trạng thái đã được phân phối theo chuỗi.

> Trong các nút giữa kiểm tra và sửa đổi trạng thái. Cách thực hiện: trong các nút quan trọng trước tạm dừng, để người thể hiện trạng thái, chấp nhận sửa đổi, phục hồi.

### Tưởng thức

Giao diện LangGraph tích hợp với các hệ thống bộ nhớ bên ngoài (Mem0, tùy chỉnh) thông qua các công cụ.

> 短期 (一次运行内状态中的对话历史) 和长期 (长期) 跨运行 (跨运行) 通过检查点器加独立长期储存持久化) ◊ LongGraph 通过工具与外部记忆系统 (通过工具与外部记忆系统) ◊ Mem0、自定义) 集成──

### Ba topology

1. **Supervisor.**Các bộ định tuyến trung tâm LLM gửi cho các chuyên gia phụ. `create_supervisor()`trong `langgraph-supervisor`(mặc dù nhóm LangChain vào năm 2026 khuyên nên làm điều này thông qua các công cụ gọi trực tiếp cho sự kiểm soát bối cảnh nhiều hơn).
   Trung ngữ翻译:**监督者。**Trung tâm đường từ LLM phân phát đến chuyên gia子 Agent
2. **Swarm / peer-to-peer.**Các nhân viên giao thông trực tiếp qua một công cụ chung không có bộ định tuyến trung tâm.
   Trung ngữ翻译:**群体/点对点。**Trưởng thông qua công cụ chia sẻ giao tiếp trực tiếp chuyển giao.
3. **Hierarchical.**Giám sát viên quản lý các giám sát viên phụ, được thực hiện như các hình phụ tổ.
   Trung ngữ翻译:**层次化。**监督者管理子监督者,实现为嵌套子图──

### Khi mô hình này đi sai

> ️ **【易错点】**Những thất bại thường gặp nhất:`datetime.now()`Hoặc theo số, khi phục hồi những giá trị này sẽ thay đổi.**后果**Từ điểm kiểm soát 恢复, các节点 được thực hiện lại với kết quả khác với hoạt động ban đầu, toàn bộ trạng thái của máy bay vào hỗn loạn.**一行修复**: tất cả nguồn không xác định (( thời gian]],随机、外部 API 返回) đều phải được bắt vào trạng thái 里,节点 hàm đọc trạng thái chứ không phải điều chỉnh trực tiếp `datetime.now()`

- **Checkpoints too small.**Chỉ cần kiểm tra các vòng quay cuộc trò chuyện để lại trạng thái công cụ và bộ nhớ viết không thể phục hồi.
  Trung ngữ翻译:**检查点太小。**Chỉ cần kiểm tra điểm cuộc hội thoại vòng lặp để lại không thể phục hồi được trạng thái công cụ và ghi nhớ.
- **Non-deterministic nodes.**Thử nghiệm lại giả định đầu vào nút tạo ra cùng một cập nhật trạng thái. hạt giống ngẫu nhiên, đồng hồ tường, API bên ngoài phải được chụp.
  Trung ngữ翻译:**非确定性节点。**恢复假设节点输入产生相同状态更新──随机种子、挂钟时间、外部 API 必须被捕──
- **Over-use of conditional edges.**Một biểu đồ với mọi cạnh điều kiện là một máy trạng thái mà không thể lý luận về.
  Trung ngữ翻译:**过度使用条件边。**Mỗi đường bên đều là một biểu đồ của tình trạng không thể đoán được.

> 🤔 **【困惑】**Q: 三种拓( giám sát viên, nhóm, cấp bậc) đến mức nào nên chọn?**任务可分解为独立角色**(如客服/退款/技术) chọn giám sát viên;**Agent 之间是协作关系而非派发关系**(如辩、相互 review) 选群;**任务有天然层次结构**(ví dụ: "Product Line A 下分 5 个团队") chọn thứ tự.

## Hãy xây dựng nó.
```figure
langgraph-state
```

## Hãy xây dựng nó

`code/main.py`thực hiện biểu đồ trạng thái stdlib:

> `code/main.py`Sử dụng standard library thực hiện có trạng thái:

- `State` một lệnh đánh dấu với `messages`- `step`- `route`- `output`- `human_approval`- Tôi không biết.
  Trung ngữ翻译:`State`包含 `messages``step``route``output``human_approval`                                                                                                                                                                                                                                                              
- `Node` được gọi là nhận trạng thái và trả lại một bản cập nhật lệnh.
  Trung ngữ翻译:`Node` chấp nhận trạng thái并返回更新 dict 的可调用对象──
- `StateGraph` nút + cạnh + cạnh điều kiện + chạy + tiếp tục.
  Trung ngữ翻译:`StateGraph`节点 + 边 + 条件边 + 运行 + 恢复。
- `SQLiteCheckpointer`(trong bộ nhớ giả)  tựa trạng thái sau mỗi nút; `load(session_id)`phục hồi.
  Trung ngữ翻译:`SQLiteCheckpointer`(内存模拟)  từng node sau trạng thái chuỗi hóa;`load(session_id)`恢复:
- Một biểu đồ demo: phân loại -> chi nhánh(chuyển / lỗi / bán hàng) -> cổng con người -> gửi.
  中文翻译:演示图:classify -> branch(refund / bug / sales) -> human gate -> send。

Đi đi.

> 运行:

```
python3 code/main.py
```

Hình ảnh cho thấy lần chạy đầu tiên thất bại ở cổng của con người, kiên trì, sau đó tiếp tục sản xuất sản xuất cuối cùng.

> 轨迹 cho thấy lần đầu tiên vận hành trong kiểm soát của con người thất bại, kéo dài, sau đó khôi phục tạo ra đầu ra cuối cùng.

## Hãy sử dụng nó để thực hiện

- **LangGraph** tài liệu tham chiếu, sẵn sàng sản xuất.`create_react_agent`- `create_supervisor`, hoặc xây dựng biểu đồ của riêng bạn.
  Trung ngữ翻译:**LangGraph**参考实现,生产就绪──使用 `create_react_agent``create_supervisor`Hoặc xây dựng hình ảnh của riêng mình.
- **AutoGen v0.4**(Dạy 14)  mô hình diễn viên thay thế cho các kịch bản cạnh tranh cao.
  Trung ngữ翻译:**AutoGen v0.4**(第 14 课) 高并发场景的演员 模型替代方案──
- **Claude Agent SDK**(Dạy 17)  quản lý vòng xoáy với cửa hàng phiên tích hợp.
  Trung ngữ翻译:**Claude Agent SDK**(第 17 课) 带内置会话存储的托管框架──
- **Custom** khi bạn cần kiểm soát chính xác hình dạng trạng thái hoặc backend điểm kiểm tra.
  Trung ngữ翻译:**自定义** Khi bạn cần kiểm soát chính xác trạng thái hình dạng hoặc kiểm tra điểm cuối thời gian.

## Chuyển nó đi.

`outputs/skill-state-graph.md`tạo ra một biểu đồ trạng thái hình LangGraph trong bất kỳ thời gian chạy mục tiêu nào với kiểm tra và tiếp tục được kết nối.

> `outputs/skill-state-graph.md`Trong bất kỳ mục tiêu vận hành, tạo ra LangGraph hình dạng trạng thái biểu đồ, nội dung kiểm tra điểm và phục hồi.

## Tập luyện bài tập

1. Thêm một cạnh điều kiện từ `classify`đến`end`khi sự tin tưởng phân loại dưới ngưỡng.`route`tay.
   Trung ngữ翻译:当分类置信度低于值时添加从 `classify`Đến`end`                                                                                                                                                                                                                                                              `route`后恢复运行──
2. Thay đổi các SQLite giống giả với một SQLite thực sự kiểm tra điểm.
   Trung文翻译:将 SQLite 模拟替换为真实 SQLite 检查点器──测量每步序列化开销──
3. Thực hiện cạnh song song: hai nút chạy đồng thời, hợp nhất bằng một bộ giảm tùy chỉnh.
   Trung ngữ翻译:实现并行边:两个节点并发运行, sử dụng tự định nghĩa giảm 合并――不可变状态在这里带来什么?
4. Đọc `langgraph-supervisor`Đưa đồ chơi vào `create_supervisor`So sánh hình dạng dấu vết.
   中文翻译:阅读 `langgraph-supervisor`参考──将玩具移植为`create_supervisor`比较轨迹形态
5. Thêm streaming: mỗi nút sẽ có trạng thái một phần trong khi nó chạy. Bác in các delta khi chúng đến.
   Trung ngữ翻译:添加流式传输: mỗi节点运行时产生部分状态──印到达的增量──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| State graph | "Agent as state machine" / "Agent 即状态机" | Typed state + nodes + edges + reducers / 带类型状态 + 节点 + 边 + reducer |
| Checkpointer | "Persistence backend" / "持久化后端" | Serializes state after every node; enables resume / 每个节点后序列化状态；支持恢复 |
| Reducer | "State merger" / "状态合并器" | Function that combines current state with a node's update / 将当前状态与节点更新合并的函数 |
| Conditional edge | "Branch" / "分支" | Edge chosen by a function of state / 由状态函数选择的边 |
| Subgraph | "Nested graph" / "嵌套图" | A graph used as a node inside another graph / 作为另一个图内节点使用的图 |
| Durable execution | "Resume from failure" / "从失败恢复" | Restart at the last successful node with exact state / 在最后成功节点处用精确状态重启 |
| Supervisor | "Router LLM" / "路由 LLM" | Central dispatcher for specialist subagents / 专家子 Agent 的中央分派器 |
| Swarm | "P2P agents" / "P2P Agent" | Agents hand off via shared tools; no central router / Agent 通过共享工具移交；无中央路由 |

## Xem thêm 延伸阅读

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) các tài liệu tham chiếu
  Trung文翻译:LangGraph 概览参考文档。
- [langgraph-supervisor reference](https://reference.langchain.com/python/langgraph/supervisor/) API mô hình giám sát
  Trung文翻译:langgraph-supervisor 参考监督者模式 API。
- [AutoGen v0.4, Microsoft Research](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) Đổi thay cho người diễn viên-chương mẫu
  Trung文翻译:AutoGen v0.4 微软研究Actor 模型替代方案。
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) cửa hàng phiên và các bộ phận phụ
  Trung文翻译:Claude Agent SDK 概览会话存储和子代理。
