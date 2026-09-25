# Mô hình nguyên thủy đa đại lý

> Bốn nguyên thủy, không có gì hơn  đại lý, giao hàng, trạng thái chia sẻ, nhạc cụ  trải dài một không gian thiết kế bốn chiều, và các khung đa đại lý lớn được vận chuyển vào năm 2026 (AutoGen, LangGraph, CrewAI, OpenAI Agents SDK, Microsoft Agent Framework) là điểm trong đó. Bài học này xây dựng chúng từ 0, chạy một hệ thống đồ chơi trên tất cả bốn, sau đó lập bản đồ tất cả các khung chính trên cùng một trục để bạn có thể đọc bất kỳ phát hành mới trong một đoạn.

> **【中文解读】**Phần này giới thiệu mô hình nguyên thủy đa đại lý 系统 các đơn vị cấu trúc cơ bản nhất và giao tiếp nguyên thủy

> **【拓展：primitive model→具体应用】**Nhiều Agent 系统的最小原语模型定义了 Agent 之间的基本交互模式:(1) 消息传递Agent 通过发送消息通信;(2) 共享状态Agent 通过阅读写共享存储协调;(3) 事件通知Agent 订阅感兴趣的事件。AutoGen dùng消息传递,LangGraph dùng chia sẻ trạng thái,黑板系统 dùng事件通知。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 (Agent Engineering), Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 14 (Agent 工程), Phase 16 · 01 (为什么需要多 Agent)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Học本节前请先掌握:Phase 14(Agent 工程) 、Phase 16·01(多 Agent 动机) ⋅本节是Phase 16 的核心4个原语(agent/handoff/shared-state/orchestrator) 定义所有框架的设计空间──
>  **【类比】**4 原语 = "音乐四件套":agent(乐手)、handoff(独奏接力)、shared state(总谱)、orchestrator(指挥)。AutoGen 偏消息传递、LangGraph 偏共享状态、CrewAI 偏角色分工都是这4个原语的不同组合──学会原语后看任何新框架都能 1段话读懂──

##                                                                                                                                                                                                                                                               

Mỗi sáu tháng một khung đa đại lý mới được xuất hiện. AutoGen vào năm 2023. CrewAI vào năm 2024. LangGraph và OpenAI Swarm vào năm 2024. Google ADK vào tháng 4 năm 2025. Microsoft Agent Framework RC vào tháng 2 năm 2026. Mỗi thông cáo báo chí tuyên bố là "sự trừu tượng đúng".

> Mỗi sáu tháng sẽ có một khung nhiều đại lý mới được phát hành. AutoGen năm 2023; CrewAI năm 2024; LangGraph năm 2024; và OpenAI Swarm năm 2025: Google ADK tháng 4 năm 2026.

Sự thay đổi là thực tế nhưng nguyên thủy cơ bản không thay đổi. Điều trông giống như đổi mới thường được đổi tên: cùng bốn nút (agent, handoff, shared state, orchestrator) với các mặc định và cú pháp khác nhau. Một khi bạn thấy nguyên thủy, tiếp thị rơi đi.

> Sự thay đổi là thực tế nhưng ngôn ngữ gốc dưới cùng không thay đổi. Có vẻ như những thứ mới thường được tái thương hiệu hóa: cùng bốn vòng: (Agent, communication, sharing state, editor) có giá trị và ngôn ngữ khác nhau.

Nếu bạn cố gắng học chúng một lần một, bạn sẽ bị cháy. các API trông khác nhau. Các tài liệu không đồng ý về "agent" là gì. Một khung gọi bộ nhớ chia sẻ của nó là "blackboard", một cái gọi là "bể tin nhắn", một cái gọi là "StateGraph". Bạn bắt đầu nghi ngờ rằng lĩnh vực chỉ là thổi thùng.

> Nếu bạn cố gắng một cách riêng để học chúng, bạn sẽ mệt mỏi hết sức. API trông khác nhau.

Không, dưới nền tảng tiếp thị, bốn nguyên thủy đều ổn định. Hãy học chúng một lần, đọc từng khung mới trong một đoạn.

> Thực tế là không như vậy. Trong kinh doanh, bốn ngôn ngữ nguyên thủy là ổn định.

## Khái niệm cốt lõi

### Bốn nguyên thủy

1. **Agent** một hệ thống nhắc cộng với một danh sách công cụ. Không quốc tịch; mỗi chạy bắt đầu từ hệ thống nhắc và lịch sử tin nhắn hiện tại.
   Trung ngữ翻译:**Agent** Một hệ thống提示加上一个工具列表――无状态; mỗi lần chạy từ hệ thống提示和当前消息历史开始――
2. **Handoff** chuyển giao kiểm soát được cấu trúc từ một đại lý sang một đại lý khác.
   Trung ngữ翻译:**交接** Chuyển chuyển kiểm soát cấu trúc của một đại lý sang đại lý khác.
3. **Shared state** bất kỳ cấu trúc dữ liệu nào mà nhiều đại lý có thể đọc (thỉnh thoảng viết).
   Trung ngữ翻译:**共享状态** Nhiều đại lý có thể đọc được bất kỳ cấu trúc dữ liệu nào của 
4. **Orchestrator** người nào quyết định ai nói tiếp theo. Các tùy chọn: một biểu đồ rõ ràng (định nghĩa), một trình chọn loa LLM (mềm), cuộc gọi giao tiếp của người nói cuối cùng (OpenAI Swarm), hoặc một trình lập lịch trên một hàng (kiến trúc swarm).
   Trung ngữ翻译:**编排器** quyết định ai tiếp theo một phát ngôn viên vai trò.

Đó là toàn bộ không gian thiết kế. Mỗi khung chọn các mặc định cho mỗi trục; phần còn lại là tổng hợp bề mặt.

> Đây là toàn bộ không gian thiết kế. Mỗi khung có giá trị mặc định cho mỗi trục chọn.

Kết quả: không có khung đa đại lý "tốt nhất". Chỉ có "tốt nhất cho sở thích trục của nhiệm vụ của bạn". Một khung đóng móng dàn xếp cho đường ống xác định (LangGraph) là sai đối với các cuộc trò chuyện mới nổi ( Sử dụng AutoGen). Biết trục của bạn, sau đó chọn.

> 含义: không có "các đại lý tốt nhất" nhiều khung 框架. Chỉ có "các phù hợp nhất với bạn nhiệm vụ轴偏好的" khung ⋅ được gắn liền trong định lượng dòng nước dòng ⋅ Longgraph) đối với sự nổi lên của cuộc đối thoại là sai lầm ⋅ với AutoGen (⋅ hiểu được các axes của bạn, sau đó chọn.

### Làm thế nào mỗi khung 2026 được lập bản đồ

| Framework | Agent | Handoff | Shared state | Orchestrator |
|-----------|-------|---------|--------------|--------------|
| OpenAI Swarm / Agents SDK | `Agent(instructions, tools)` | tool returns Agent | caller's problem | the LLM's next handoff call |
| AutoGen v0.4 / AG2 | `ConversableAgent` | speaker-selector on GroupChat | message pool | selector function (LLM or round-robin) |
| CrewAI | `Agent(role, goal, backstory)` | `Process.Sequential / Hierarchical` | Task outputs chained | manager LLM or static order |
| LangGraph | node function | graph edge + condition | `StateGraph` reducer | the graph, deterministic |
| Microsoft Agent Framework | agent + orchestration patterns | pattern-specific | thread / context | pattern-specific |
| Google ADK | agent + A2A card | A2A task | A2A artifacts | host decides |

>  Quản lý  Đội ngũ  Đội ngũ 
> ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬ ♬  ♬ ♬    ♬     ♬     ♬                                                                                                                                                                                                                                                                
>  OpenAI Swarm / Agents SDK `Agent(instructions, tools)` Công cụ quay lại với vấn đề của nhân viên                                                                                                                                                                                                                                                         
> ♬ AutoGen v0.4 / AG2 ♬`ConversableAgent`➡️ GroupChat ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ 
>                                                                                                                                                                                                                                                               `Agent(role, goal, backstory)`♬`Process.Sequential / Hierarchical`Ứng viên quản lý chương trình học hoặc thứ tự tĩnh
>  LangGraph  Nốt hàm  Xếp ảnh `StateGraph`- Định nghĩa.
>  Microsoft Agent Framework  Agent + sắp xếp mô hình  mô hình cụ thể 
>  Google ADK  đại lý + A2A thẻ  A2A nhiệm vụ  A2A công trình  主机决定 

Sự khác biệt bề mặt trông rất lớn.

> 表面差异看起来很大──底层: cùng bốn vòng.

### Tại sao điều này quan trọng

Khi bạn thấy các nguyên thủy, so sánh khung trở thành một danh sách kiểm tra ngắn:

> Một khi bạn nhìn thấy ngôn ngữ gốc, framework comparison biến thành một danh sách kiểm tra ngắn gọn:

- Người tổ chức có tin tưởng LLM để định tuyến (Swarm) hay nó pin định tuyến trong mã (LangGraph)?
  Trung文翻译:编排器是信任 LLM 来路由(Swarm) cũng đang trong代码中固定路由(LangGraph)?
- Có chia sẻ toàn bộ lịch sử trạng thái (GroupChat) hay dự đoán (StateGraph reducer)?
  Trung文翻译:共享状态是完整历史(GroupChat) hay投影的(StateGraph 归约器)?
- Các đại lý có thể sửa đổi các yêu cầu của nhau (các người quản lý CrewAI) hay chỉ giao tay (Swarm)?
  Trung文翻译:Công viên 能否修改彼此的提示?

Ba câu hỏi đó trả lời 80% khung nào phù hợp với một vấn đề nhất định. Bạn ngừng mua "quang khung đa đại lý tốt nhất" và bắt đầu thiết kế cho trục bạn thực sự quan tâm.

> Ba câu hỏi này trả lời 80% về khung nào phù hợp với một câu hỏi nhất định. Bạn không còn mua "đường hợp đa đại lý tốt nhất" mà bắt đầu thiết kế các khung bạn thực sự quan tâm.

Khi một khung mới được tung ra vào năm 2027, hãy chạy ba câu hỏi trên nó. Nếu câu trả lời của nó phù hợp với một khung bạn đã sử dụng, hãy bỏ qua di chuyển. Nếu chúng khác nhau về một trục bạn quan tâm, hãy đánh giá. Hầu hết các khung mới là tái đóng gói, không phải là đổi mới.

> Khi một khung mới năm 2027 được phát hành, hãy giải quyết ba vấn đề này. Nếu câu trả lời phù hợp với khung bạn đã sử dụng, hãy nhảy qua chuyển động. Nếu chúng không giống với trục quan tâm của bạn, hãy đánh giá.

### Sự hiểu biết vô quốc gia

Tất cả nguyên thủy ngoại trừ trạng thái chia sẻ là không có quốc gia. Agent là một hàm của (quick, công cụ). Handoff là một hàm gọi. Orchestrator là một lập trình. **The only stateful thing in the system is shared state.**Đó là nơi mà tất cả những lỗi thú vị sống: ngộ độc trí nhớ (Dạy học 15), sắp xếp tin nhắn, phiên bản, viết tranh cãi.

> Ngoài trạng thái chia sẻ, mỗi ngôn ngữ nguyên thủy đều không trạng thái.**系统中唯一有状态的东西是共享状态。**Đó là tất cả những lỗi thú vị ở nơi:内存污染 (Lớp 15) 消息排序,版本控制,写冲突).

Sự hiểu biết này thúc đẩy chiến lược gỡ lỗi: khi một hệ thống đa đại lý hành vi sai, hãy xem trạng thái chia sẻ trước.

> Cái nhìn này dẫn đến chiến lược điều tra: Khi nhiều Agent  hệ thống hành vi bất thường, trước tiên kiểm tra trạng thái chia sẻ.

Các khung hình che giấu trạng thái chia sẻ (Swarm) đẩy vấn đề đến người gọi. Các khung hình tập trung nó (LangGraph checkpoint, AutoGen pool) làm cho nó có thể kiểm tra nhưng chuyển chi phí phối hợp vào việc thực hiện trạng thái chia sẻ.

> 藏藏共享状态的框架(Swarm) sẽ đưa vấn đề đến người调用者──集中化它的框架(LangGraph 检查点、AutoGen 池) làm cho nó có thể kiểm tra nhưng sẽ chuyển chi phí phối hợp sang trạng thái chia sẻ để thực hiện trên──

### Phân tích của một nguyên thủy duy nhất

#### - Trưởng lý.

```
Agent = (system_prompt, tools, model, optional_name)
```

Không bộ nhớ, không trạng thái, hai đại lý với cùng một hệ thống thông báo và công cụ là có thể thay đổi, mọi thứ trông giống như trạng thái mỗi đại lý thực sự là trong trạng thái chia sẻ hoặc giao thức giao tiếp.

> Không có ký ức. Không có trạng thái. Có hai đại lý có cùng hệ thống gợi ý và công cụ là có thể trao đổi.

Điều này trái với trực giác nhưng mạnh mẽ: các nhân viên vô quốc tịch là không có gì khác, có thể bắt đầu lại và thay đổi. Bạn có thể quay 100 bản sao của cùng một nhân viên và tất cả chúng đều hành xử giống nhau. Nhà nước sống ở nơi khác.

> Đây là phản trực giác nhưng mạnh mẽ: Không trạng thái đại lý có thể dễ dàng được kết hợp, khởi động lại và thay thế. Bạn có thể khởi động 100 bản sao của cùng một đại lý, hành vi của chúng hoàn toàn giống nhau.

#### Chuyển

```
Handoff = (from_agent, to_agent, reason, payload)
```

Ba thực hiện thống trị:

> 三种实现占主导地位:

- **Function return** công cụ trả lại đại lý tiếp theo. Đây là mô hình OpenAI Swarm. Các đại lý mang theo định tuyến trong các sơ đồ công cụ của họ.
  Trung ngữ翻译:**函数返回** 工具返回下一个 Agent──这是 OpenAI Swarm's模式──Agent trong các mô hình công cụ của nó mang theo đường đi──
- **Graph edge** LangGraph. Các cạnh là tuyên bố. LLM tạo ra một giá trị; một điều kiện chọn nút tiếp theo.
  Trung ngữ翻译:**图边** LangGraph──边是声明式的──LLM 产生一个值;条件选择下一个节点──
- **Speaker selection** AutoGen GroupChat. Một chức năng chọn lọc (đôi khi chính nó là cuộc gọi LLM) đọc hồ bơi và chọn người nói tiếp theo.
  Trung ngữ翻译:**发言者选择** AutoGen GroupChat。 chọn器 hàm(有时本身是LLM 调用)读取池并选择下一个发言者。

#### Nhà nước chung

```
SharedState = { messages: [], artifacts: {}, context: {} }
```

Ít nhất, một danh sách các tin nhắn. Thông thường hơn: các vật thể có cấu trúc (các sản phẩm của CrewAI Task), ngữ cảnh được gõ (đảm độ LongGraph), bộ nhớ bên ngoài (MCP, vector DB).

> Ít nhất là một danh sách thông tin. Thông thường nhiều hơn: cấu trúc hóa công cụ.

Hình dạng của trạng thái chia sẻ xác định các loại phối hợp có thể. Danh sách tin nhắn phẳng làm cho phát sóng dễ dàng nhưng lọc đặc biệt vai trò khó khăn. Một sơ đồ được gõ làm cho lọc tầm thường nhưng đòi hỏi thiết kế trước. Không có bữa trưa miễn phí.

> Hình thức của trạng thái chia sẻ quyết định sự phối hợp có thể nào.

Hai topology: **full pool**(mỗi nhân viên đều thấy mọi tin nhắn) và **projected**(các đại lý xem một khung hình vai trò). các hồ bơi đầy đủ là đơn giản và quy mô không tốt. các hồ bơi dự kiến quy mô nhưng yêu cầu thiết kế sơ đồ trước.

> 两种拓:**完整池**(Tất cả các đại lý nhìn thấy mỗi câu tin) và**投影**(Hội nhân xem hình ảnh phạm vi vai trò)  toàn bộ bộ hồ sơ đơn giản nhưng mở rộng khác nhau  chiếu hồ sơ có thể mở rộng nhưng cần thiết kế mô hình trước期 

#### Nhà dàn nhạc

```
Orchestrator = ({state, last_speaker}) -> next_agent
```

Bốn hương vị:

> 4 kiểu:

- **Static** biểu đồ được cố định tại thời gian xây dựng (LangGraph xác định, CrewAI theo trình tự).
  Trung ngữ翻译:**静态** 图在构建时固定(LangGraph 确定性、CrewAI Sequential)
- **LLM-selected** một LLM đọc hồ bơi và chọn người nói tiếp theo (AutoGen, CrewAI Hierarchical).
  Trung ngữ翻译:**LLM 选择** LLM 读取池并选择下一个发言人(AutoGen、CrewAI Hierarchical)
- **Handoff-driven** đại lý hiện tại quyết định bằng cách gọi một công cụ giao hàng (Swarm).
  Trung ngữ翻译:**交接驱动** 当前 通过调用交接工具决定(Swarm)
- **Queue-driven** công nhân kéo ra khỏi một hàng đợi chung; không có loa tiếp theo rõ ràng (nền kiến trúc đám đông, Matrix).
  Trung ngữ翻译:**队列驱动** 工作器 từ chia sẻ đội ngũ kéo; không rõ ràng

### Những thay đổi giữa các khung

Một khi nguyên thủy được cố định, các quyết định thiết kế còn lại là:

> Một khi ngôn ngữ gốc được cố định, phần còn lại của quyết định thiết kế là:

- **Memory strategy** kiểm tra tạm thời so với kiểm tra bền (chỉ lục LangGraph).
  Trung ngữ翻译:**内存策略** 临时 vs 持久检查点(Langgraph checkpointer)。
- **Safety boundary** người có thể chấp thuận giao hàng (người trong vòng lặp).
  Trung ngữ翻译:**安全边界** 谁可以批准交接 (năm người trong vòng lặp) 
- **Cost accounting** ngân sách token cho mỗi đại lý.
  Trung ngữ翻译:**成本核算** Mỗi đại lý của biểu tượng ngân sách 
- **Observability** theo dõi giao hàng, duy trì trạng thái để tái phát.
  Trung ngữ翻译:**可观测性** 跟踪交接  持久化状态以便回放

Tất cả đều có thể thực hiện trên những nguyên thủy.

> Tất cả đều được thực hiện trên ngôn ngữ ban đầu.

Khi một framework quảng cáo một tính năng "mới" (người trong vòng lặp, thử lại, ngân sách token), kiểm tra xem nó thực sự giới thiệu một nguyên thủy mới hay chỉ tạo thành bốn.

> Khi framework quảng bá "những chức năng mới" (được xem là nó thực sự đưa ra bốn ngôn ngữ nguyên thủy hay chỉ là một tập hợp của chúng) thì người ta sẽ xem xét xem nó có thực sự đưa ra bốn ngôn ngữ nguyên thủy hay không.

## Hãy xây dựng nó.
```figure
a5-primitive-radar
```

## Hãy xây dựng nó

`code/main.py`thực hiện bốn nguyên thủy trong ~ 150 dòng stdlib Python. Không có LLM thực sự  mỗi đại lý là một chính sách kịch bản vì vậy trọng tâm vẫn còn trên cấu trúc phối hợp.

> `code/main.py`Sử dụng khoảng 150 行 Python 实现了四个原语――没有真正的 LLM Mỗi đại lý là một chiến lược kịch bản, để tập trung giữ được trong cấu trúc phối hợp――

Các tập tin xuất khẩu:

> 文件导出:

- `Agent` một lớp dữ liệu tên, hệ thống prompt, công cụ, chức năng chính sách.
  Trung ngữ翻译:`Agent` 名称、系统提示、工具、策略函数的数据类──
- `Handoff` một hàm trả lại một đại lý mới.
  Trung ngữ翻译:`Handoff` 返回新代理的函数──
- `SharedState` một hồ chứa thông điệp an toàn.
  Trung ngữ翻译:`SharedState` 线程安全的消息池──
- `Orchestrator` ba biến thể: `StaticOrchestrator`- `HandoffOrchestrator`- `LLMSelectorOrchestrator`(được mô phỏng).
  Trung ngữ翻译:`Orchestrator` 三种变体:`StaticOrchestrator``HandoffOrchestrator``LLMSelectorOrchestrator`(模拟) 

Demos chạy cùng một đường ống ba đại lý (phát tích -> viết -> xem xét) thông qua cả ba loại nhạc cụ và in hồ bơi tin nhắn ở cuối. Bạn có thể thấy rằng các kết quả chỉ khác nhau trong * ai chọn tiếp theo *; các đại lý và trạng thái chia sẻ là giống nhau trên các chạy.

> 演示通过所有三种编排器类型运行相同的三 Agent 流水线(研究 -> 编写 -> 审阅), và cuối cùng in 信息池──你可以看到输出只有在*谁选择下一个*上不同;Agent 和共享状态在所有运行中都是相同的──

Đi đi.

```
python3 code/main.py
```

Kết quả dự kiến: ba lần chạy nhạc cụ, một lần mỗi mẫu. Mỗi lần in hồ sơ tin nhắn cuối cùng.

> 预期输出: 3 lần điều chỉnh máy vận hành, mỗi mô hình một lần.

## Hãy sử dụng nó để thực hiện

`outputs/skill-primitive-mapper.md`là một kỹ năng đọc bất kỳ cơ sở mã hoặc tài liệu khung đa đại lý nào và trả lại bản đồ bốn nguyên thủy.

> `outputs/skill-primitive-mapper.md`là một kỹ năng, đọc bất kỳ nhiều tài liệu văn bản và quay lại bốn nguyên ngữ.

## Chuyển nó đi.

Trước khi áp dụng một framework mới, hãy viết bản đồ nguyên thủy cho nó. Nếu bạn không thể, các tài liệu không đầy đủ hoặc framework đang phát minh ra một nguyên thủy thứ năm (đếm  kiểm tra hương vị trạng thái chia sẻ mà bạn không thấy).

> Trong khi đó, các nhà nghiên cứu đã có nhiều nghiên cứu về các ngôn ngữ gốc của họ.

Đặt bản đồ vào tài liệu kiến trúc của bạn. Khi một thành viên mới của nhóm tham gia, gửi bản đồ cho họ trước khi các tài liệu API. Khi phiên bản khung thay đổi, thay đổi bản đồ, không phải bản ghi thay đổi.

> Sẽ được chuyển giao vào các phiên bản cấu trúc, thay vì chuyển đổi ngày.

## Tập luyện bài tập

1. Đi chạy`code/main.py`3 lần với các chính sách của các đại lý khác nhau.
   Trung文翻译:用不同的代理 策略运行 `code/main.py`三次──观察编排器选择如何改变哪些代理运行──
2. Thực hiện một loại nhạc công thứ tư: một loại điều khiển hàng rào nơi các đại lý thăm dò chia sẻ tình trạng cho công việc.
   Trung ngữ翻译:实现第四种编排器类型:队列驱动的,Agent 轮询共享状态获取工作──可能发生什么死锁,你如何检测?
3. Hãy lấy LangGraph Quickstart và viết lại nó như bốn nguyên thủy.
   Trung ngữ翻译:将 LangGraph 快速入门改写为四个原语――LangGraph có gì là mô hình 1: 1 映射, có gì là tiện ích đóng gói?
4. Đọc sách nấu ăn OpenAI Swarm. xác định ra cái nào trong bốn nguyên thủy mà Swarm làm cho ergonomic nhất, và cái nào nó đẩy đến người gọi.
   Trung ngữ翻译:阅读 OpenAI Swarm 手册。识别四个原语中 Swarm 使哪个最符合人体工程学,哪个推给调用者。
5. Tìm một khung trong bảng này mà ẩn hoàn toàn trạng thái chia sẻ. giải thích những gì phá vỡ khi các đại lý cần phối hợp qua giao hàng mà không cần đọc lại lịch sử.
   Trung ngữ翻译: trong bảng tìm thấy một khung trạng thái chia sẻ hoàn toàn ẩn trong bảng.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Agent | "An LLM with tools" / "带工具的 LLM" | A `(system_prompt, tools, model)` triple. Stateless. / 一个 `(system_prompt, tools, model)` 三元组。无状态。 |
| Handoff / 交接 | "Transfer of control" / "控制转移" | A structured call that names the next agent and optional payload. Three implementations: function return, graph edge, speaker selection. / 命名下一个 Agent 和可选有效载荷的结构化调用。三种实现：函数返回、图边、发言者选择。 |
| Shared state / 共享状态 | "Memory" / "context" / "内存" / "上下文" | The only stateful part of a multi-agent system. Message pool or blackboard. / 多 Agent 系统中唯一有状态的部分。消息池或黑板。 |
| Orchestrator / 编排器 | "Coordinator" / "协调器" | Whoever decides who runs next. Static graph, LLM selector, handoff-driven, or queue-driven. / 决定谁下一个运行的角色。静态图、LLM 选择器、交接驱动或队列驱动。 |
| Primitive / 原语 | "Abstraction" / "抽象" | One of the four axes every framework parameterizes. Not a framework feature. / 每个框架参数化的四个轴之一。不是框架特性。 |
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Full-history shared state. Easy to reason about, scales badly. / 完整历史共享状态。易于推理，扩展性差。 |
| Projected state / 投影状态 | "Scoped view" / "范围视图" | Role-specific view into shared state. Scales, requires schema design. / 角色特定的共享状态视图。可扩展，需要模式设计。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | Orchestrator pattern where a function (often an LLM) picks the next agent from a group. / 编排器模式，函数（通常是 LLM）从组中选择下一个 Agent。 |

## Xem thêm 延伸阅读

- [OpenAI cookbook: Orchestrating Agents — Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) sự diễn giải rõ ràng nhất của dàn nhạc do tay tay tay
  Trung文翻译:OpenAI 手册:编排  例例和交接 交接驱动编排的最清晰阐述
- [AutoGen stable docs](https://microsoft.github.io/autogen/stable/) GroupChat + sự lựa chọn loa là tham chiếu cho dàn nhạc LLM được lựa chọn
  中文翻译:AutoGen 稳定文档  GroupChat + 发言人选择是 LLM 选择编排的参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) Phân phối cạnh biểu đồ và trạng thái chia sẻ dựa trên giảm
  Trung ngữ翻译:LangGraph 工作流和 Agent  图边编排和基于归约器的共享状态
- [CrewAI introduction](https://docs.crewai.com/en/introduction) các nhân viên vai trò-goal-backstory, quy trình theo trình / Trật tự
  Trung文翻译:CrewAI 介绍  角色-目标-背景故事 Agent,Sequential / Hierarchical 流程
- [AG2 (community AutoGen continuation)](https://github.com/ag2ai/ag2) dòng AutoGen v0.2 trực tiếp sau khi Microsoft chuyển v0.4 vào bảo trì
  Trung文翻译:AG2(社区 AutoGen 延续)  微软将 v0.4 移入维护后的活跃 AutoGen v0.2 线
