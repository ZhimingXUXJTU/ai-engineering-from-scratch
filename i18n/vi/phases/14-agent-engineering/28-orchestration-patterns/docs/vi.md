# Các mẫu dàn nhạc: giám sát viên, nhóm, cấp bậc.

> Bốn mô hình dàn xếp lặp lại trên các khung 2026: người giám sát, nhóm / đồng nghiệp, phân cấp, tranh luận. hướng dẫn của Anthropic: "Đó là về việc xây dựng hệ thống phù hợp với nhu cầu của bạn". Bắt đầu đơn giản; chỉ thêm topology khi một đại lý duy nhất cộng với năm mô hình luồng công việc là không đủ.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 25 (Multi-Agent Debate) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

>  **【前置】**学本节前请先掌握:Phase 14·01(Agent Loop) 单 Agent 基础;Phase 14·12(Tình mẫu dòng công việc)  5 种工作流模式 của nhân loại;Phase 14·25(Vì tranh luận đa Agent) 多 Agent 协作基础。**重要原则**: Đầu tiên sử dụng một đại lý đơn + 工作流, không đủ thời gian để tăng thêm đại lý 拓──

## Mục tiêu học tập

- Hãy nêu tên bốn kiểu dàn nhạc lặp lại và mỗi kiểu phù hợp.
- Mô tả khuyến nghị LangChain 2026: giám sát dựa trên các công cụ và thư viện giám sát.
- Giải thích quy tắc "giải thiện hệ thống" của Anthropic và cách nó ngăn chặn sự lựa chọn topology.
- Thực hiện tất cả bốn trong stdlib chống lại một LLM kịch bản chung.

## Vấn đề  vấn đề giới thiệu

Các nhóm tìm kiếm "multi-agent" trước khi họ cần nó. Bốn mô hình lặp lại trên các khung; một khi bạn có thể đặt tên cho chúng, bạn có thể chọn đúng  hoặc bỏ qua topology hoàn toàn.

> Nhóm đã sử dụng "multi-agent" khi không cần thiết. Bốn mô hình xuất hiện lặp đi lặp lại trong khung; một khi bạn có thể đặt tên cho chúng, bạn có thể chọn đúng một hoặc nhảy hoàn toàn.


> **【中文解读】**Mô hình lập trình đại lý xác định cách phân phối và phối hợp nhiệm vụ trong nhiều đại lý trong hệ thống.

>  **【类比】**4 种编排模式 = 4 种公司组织:(1) **Supervisor-Worker**= 老板分活给员工 ((最常见, giám sát viên LangGraph);(2) **Swarm/P2P**= 同事相互协作(适合讨论类任务,AutoGen GroupChat);(3) **Hierarchical**= 多层老板(CEO→总监→员工,超复杂任务);(4) **Debate**= 委员会投票 ():

> ️ **【易错点】**编排选错的 3 个坑:(1) **简单任务用多 Agent** đơn đại lý + 5 工具能解决 80% 需求,过早使用监督反而增加复杂度;Anthropic 明确建议"先简单再拓"――(2) **Supervisor 成瓶颈** tất cả nhiệm vụ đều qua giám sát viên 转发,单点延迟 + 单点失败;让工人间直接通信(仅需时报 giám sát viên)**没设 worker 超时** nhân viên chậm 卡住整个流程; mỗi nhân viên调用 phải đặt thời gian,超时返回降级结果──

> **{【拓展：Agent 编排是 2026 年生产 Agent 系统的核心挑战。Anthropic 的模式分类（P...】}**Agent 编排 là thách thức cốt lõi của hệ thống sản xuất vào năm 2026  Anthropic 模式分类 (Prompt Chaining, Routing, Parallelisation, Orchestrator-Workers) đã trở thành tiêu chuẩn. Trong thực tế, hầu hết các hệ thống sử dụng nhiều kiểu kiểu như:
## Khái niệm cốt lõi

### Nhân viên giám sát

- Một trung tâm định tuyến LLM gửi đến các đại lý chuyên nghiệp.
- Quyết định: quay lại với bản thân, giao cho chuyên gia, chấm dứt.
- Các chuyên gia không nói chuyện với nhau; tất cả các tuyến đường đi qua người giám sát.

Các khung: LangGraph `create_supervisor`, nhân vật nhạc sĩ-thợ, CrewAI Hierarchical Process.

> 编排模式描述多 Agent 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

**2026 LangChain recommendation:**làm giám sát thông qua các cuộc gọi trực tiếp công cụ thay vì `create_supervisor`. Giúp kiểm soát kỹ thuật ngữ tinh tế hơn  bạn quyết định chính xác những gì mỗi chuyên gia thấy.

> **2026 年 LangChain 建议：**通过直接工具调用而不是 `create_supervisor`Để thực hiện giám sát, cung cấp các kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ thuật kỹ

### Swarm / peer-to-peer

- Các đại lý giao thông trực tiếp qua một bề mặt công cụ chung.
- Không có bộ định tuyến trung tâm.
- Trễ hơn so với người giám sát (nhiều hop hơn).
- Khó hơn để lý luận về (không có một điểm kiểm soát duy nhất).

Các khung: Topology swarm LangGraph, OpenAI Agents SDK handoffs (khi tất cả các đại lý có thể trao cho tất cả những người khác).

> 编排模式描述多 Agent 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

### Đường bậc

- Giám sát viên quản lý phụ giám sát viên quản lý nhân viên.
- Thực hiện như các subgraph tổ trong LangGraph; các phi hành đoàn tổ trong CrewAI.
- Scale đến các nhóm đại lý lớn với chi phí phức tạp hoạt động.

Khi bạn cần nó: khi ngân sách ngữ cảnh của một giám sát viên duy nhất không thể chứa mô tả về tất cả các chuyên gia.

> Các chuyên gia có thể nói rằng:

> 编排模式描述多 Agent 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

### Cuộc tranh luận

- Các đề xuất song song + phê bình chéo lặp lại (Học 25).
- Không thực sự dàn xếp  nhiều xác minh  nhưng xuất hiện như một lựa chọn topology trong các khung.

### Các đội tự trị so với dòng chảy xác định

CrewAI chính thức hóa hai chế độ triển khai:

- **Flow**cho tự động hóa xác định dựa trên sự kiện (điểm khởi đầu được khuyến cáo cho sản xuất).
- **Crew**cho sự hợp tác dựa trên vai trò tự trị.

Điều này là thẳng thắn với bốn mô hình ở trên nhưng bản đồ cho topology: Flow thường là giám sát hoặc phân cấp; Crew thường là giám sát với một bộ định tuyến LLM.

> 编排模式描述多 Agent 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

### Hướng dẫn của Anthropic

"Sự thành công trong lĩnh vực LLM không phải là xây dựng hệ thống tinh vi nhất mà là xây dựng hệ thống phù hợp với nhu cầu của bạn".

> 编排模式描述多 Agent 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

Định lệnh quyết định:

1. Một đại lý + các mô hình lưu lượng công việc (Dạy học 12)  bắt đầu từ đây.
2. Người giám sát làm việc  khi bạn có 2-4 chuyên gia.
3. Thập tràn khi độ trễ quan trọng hơn sự rõ ràng của lý luận.
4. Đường bậc  chỉ khi ngân sách trong bối cảnh giám sát thất bại.
5. Vài cuộc tranh luận  khi tính chính xác quan trọng hơn chi phí.

### Khi mô hình này đi sai

- **Topology-first thinking.**"Chúng tôi cần nhiều đại lý" trước khi xác định vấn đề mà nhiều đại lý giải quyết.
- **Bouncing handoffs in swarm.**A -> B -> A -> B. Sử dụng máy tính đếm hop.
- **Fake hierarchy.**Ba tầng vì "công ty"; hai đội thực sự.

> **拓扑优先思维。**Trong việc xác định nhiều đại lý  giải quyết vấn đề trước khi nói "Chúng tôi cần nhiều đại lý"
> **群体中弹跳交接。**A -> B -> A -> B。 sử dụng nhảy số tính toán器。
> **虚假层级。**Bởi vì "phase enterprise" đã có ba tầng; thực tế chỉ có hai nhóm.

## Hãy xây dựng nó.
```figure
orchestration-pattern
```

## Hãy xây dựng nó

`code/main.py`thực hiện tất cả bốn mô hình trong stdlib đối với một LLM kịch bản:

> 编排模式描述多 Agent 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

- `Supervisor` bộ định tuyến trung tâm.
- `Swarm` Tương tự với người khác với sự giao tiếp trực tiếp.
- `Hierarchical` Giám sát viên của giám sát viên.
- `Debate` đề xuất song song + chỉ trích.

Mỗi mô hình xử lý cùng một nhiệm vụ ba ý định (trái tiền / lỗi / bán hàng).

> 编排模式描述多 Agent 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

Đi đi.

```
python3 code/main.py
```

Kết quả: theo dõi theo mô hình + số lượng op. Giám sát viên sạch nhất; đàn đông ngắn nhất; cấp bậc là sâu nhất; tranh luận đắt tiền nhất.

> 输出: mỗi模式追踪 + 操作数──监督者最清晰;群体最短;层级最深;辩论最昂贵──

> 编排模式描述多 Agent 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

## Hãy sử dụng nó để thực hiện

- **LangGraph**cho giám sát và cấp bậc (đồ sơ phụ có tổ).
- **OpenAI Agents SDK**cho việc trao đổi như công cụ (tình hình giám sát viên).
- **CrewAI Flow**cho sản xuất xác định.
- **Custom**để tranh luận hoặc khi nào bạn muốn kiểm soát chính xác.

## Chuyển nó đi.

`outputs/skill-orchestration-picker.md`chọn một topology và thực hiện nó.

> `outputs/skill-orchestration-picker.md`选择一个拓并实现它──

> 编排模式描述多 Agent 系统的组织方式──主要模式包括:监督者(中央路由)、群体(点对点移交)、层次化(嵌套监督)、管道(顺序处理)──

## Tập luyện bài tập

1. Làm cho một người làm việc giám sát trở thành một đám đông bằng cách loại bỏ bộ định tuyến.
  Trung ngữ翻译:思考并实践此练习。
2. Thêm một con số nhảy vào đám đông: từ chối sau 3 lần giao hàng.
  Trung ngữ翻译:思考并实践此练习。
3. Xây dựng một hệ thống phân cấp hai cấp cho một lĩnh vực chuyên môn 12.
  Trung ngữ翻译:思考并实践此练习。
4. Xác định bốn mô hình trên khối lượng công việc hình dạng sản xuất.
  Trung ngữ翻译:思考并实践此练习。
5. Đọc bài viết của Anthropic về "Building Effective Agents" và lập bản đồ từng dòng sản xuất của bạn cho một trong bốn dòng sản xuất.
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Supervisor-worker | "Router + specialists" | Central LLM dispatches to specialists; they don't talk to each other |  |
| Swarm | "Peer-to-peer" | Direct handoffs via shared tools; no central router |  |
| Hierarchical | "Supervisors of supervisors" | Nested subgraphs for large populations |  |
| Debate | "Proposer + critique" | Parallel proposers, cross-critique (Lesson 25) |  |
| Tool-call-based supervision | "Supervisor without a library" | Implement supervisor as direct tool calls for context control |  |
| Crew | "Autonomous team" | CrewAI's role-based collaboration mode |  |
| Flow | "Deterministic workflow" | CrewAI's event-driven production mode |  |

## Xem thêm 延伸阅读

- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)5 mô hình + đại lý đối với dòng công việc
  Trung ngữ: 翻译:见原文.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) giám sát viên, đám đông, cấp bậc
  Trung ngữ: 翻译:见原文.
- [CrewAI docs](https://docs.crewai.com/en/introduction) Đội ngũ nhân viên đối với dòng chảy
  Trung ngữ: 翻译:见原文.
- [Du et al., Society of Minds (arXiv:2305.14325)](https://arxiv.org/abs/2305.14325) Mô hình tranh luận
  Trung ngữ: 翻译:见原文.
