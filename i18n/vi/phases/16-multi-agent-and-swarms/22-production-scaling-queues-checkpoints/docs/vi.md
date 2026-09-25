# Scaling sản xuất  Đường xếp, Đường kiểm tra, Độ bền  kiểm tra điểm sản xuất  mở rộng hàng

> Tích thước các hệ thống đa đại lý đến hàng ngàn chạy đồng thời đòi hỏi **durable execution** xếp hàng làm việc cộng với các điểm kiểm soát, vì vậy bất kỳ công nhân nào có thể tiếp tục chạy sau bất kỳ tai nạn nào, miễn là xử lý thuê, tác dụng phụ không có khả năng và tái diễn xác định được thực hiện.`thread_id`(Từ khi bị trục xuất theo mặc định); công nhân bị tai nạn giải phóng hợp đồng thuê và một công nhân khác tiếp tục.**MegaAgent**(arXiv:2408.09955) chạy hàng nhà sản xuất-thành khách mỗi đại lý với ba trạng thái (Idle / Processing / Response) và phối hợp hai lớp (chát nội bộ nhóm + chat quản trị viên giữa nhóm). **Fiber/async**đánh đập thread-per-job cho LLM streaming: các thread ngồi idle 99% thời gian chờ đợi token, sợi hợp tác sản xuất trên I / O. Counterpoint: Ashpreet Bedi "Scaling Agentic Software" lập luận cho **FastAPI + Postgres + nothing else**cho đến khi tải chứng minh khác  kiến trúc đơn giản đi xa hơn dự kiến. Bài học này xây dựng một nhật ký kiểm soát lâu dài, hàng xếp hàng làm việc cho mỗi đại lý với chuyển đổi trạng thái, một bản demo async-vs-thread, và hạ cánh quy tắc thực tế "bắt đầu đơn giản".

> **【中文解读】**Phần này giới thiệu các chiến lược mở rộng sản xuất, kiểm tra và kiểm tra của nhiều đại lý.

> **【拓展：production scaling queues checkpoints→具体应用】**多 Agent 系统的生产扩展需要:(1) 消息队列Kafka/RabbitMQ 缓冲 Agent 间的消息;(2) 检查点定期保存系统状态以支持恢复;(3) 负载均衡将任务均分配给可用 Agent 实例;(4) 水平扩展动态增减 Agent 数量应对负载变化──LangGraph Cloud和 Temporal là hai lựa chọn chính trong lĩnh vực này.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `asyncio`, `sqlite3`) | **语言:** Python（标准库，`asyncio`，`sqlite3`）
**Prerequisites:** Phase 16 · 09 (Parallel Swarm Networks), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 09（并行群体网络），Phase 16 · 13（共享内存）

>  **【前置】**学本节前请先掌握:Phase 16·09(Swarm) 、Phase 16·13(共享内存) 、Phase 15·12(Durable Execution) 、异步编程(asyncio) ⋅多 Agent 生产扩展 = 分布式系统工程问题──
>  **【类比】**多 Agent 扩展 = "外卖平台架构"――检查点:FastAPI + Postgres + 都不加,先跑起来――简单架构往往比预期走得远――
**Time:** ~75 minutes | **时间:** ~75 分钟

##                                                                                                                                                                                                                                                               

Một hệ thống đa đại lý nguyên mẫu hoạt động trên một máy tính xách tay với ba đại lý trong một vòng lặp trong bộ nhớ.

> Các hoạt động của các đại lý trong vòng lặp của các sự kiện trong bộ nhớ trên một máy tính xách tay:

- Các đại lý đôi khi chạy trong nhiều giờ (sự nghiên cứu dài, người trong vòng chờ đợi).
  Trung文翻译:Công viên 有时运行数小时(长时间研究、人在环等)
- Các quy trình công nhân bị hỏng, khởi động lại mất trạng thái.
  中文翻译:工作者进程崩──重启丢失状态──
- Lượng tải cao nhất là trung bình 10x; bạn cần quy mô ngang.
  Trung ngữ翻译: 峰值负载是平均的10倍;你需要水平扩展──
- Người dùng trả tiền cho mỗi người vận hành; bạn cần một cách chính xác một lần để sạc.
  Trung ngữ翻译:用户按代理运行付费;你需要恰好一次的计费语义。

Các tùy chọn canonical 2026 là:

> Trong vòng lặp của các sự kiện trong ký ức, những điều này đều không được thực hiện.

1. Một động cơ lưu lượng công việc với các điểm kiểm soát (Temporal, LangGraph runtime).
   Trung文翻译:带检查点的工作流引擎(Temporal、LangGraph 运行时)
2. Một dòng tin nhắn với một cửa hàng nhà nước (Postgres + SQS/RabbitMQ).
   Trung文翻译:带状态存储的消息队列(Postgres + SQS/RabbitMQ)
3. Các khung mô hình diễn viên (Mỹ nhân sản xuất-thành khách của mỗi đại lý).
   Trung文翻译:Actor 模型框架(MegaAgent 的每 Agent 生产者-消费者)
4. FastAPI + Postgres (trách luận của Bedi).
   Trung文翻译:手工搭建的 FastAPI + Postgres(Bedi 的论点)。

Bài học này tạo ra một hình ảnh nhỏ của mỗi bài học.

> 本课构建每个微型版本的

## Khái niệm cốt lõi

### Hoạt động lâu dài, mô hình

Một động cơ thực hiện bền vững vẫn giữ trạng thái chương trình đầy đủ sau mỗi "giải" (giải siêu, bằng ngôn ngữ LangGraph).

```
worker crashes mid-step
  -> lease timeout
  -> another worker picks up the thread_id
  -> resumes from last checkpoint
  -> no duplicate side effects
```

Yêu cầu để điều này hoạt động:

- **Serializable state.**Tất cả tình trạng đại lý phải duy trì.
- **Deterministic resume.**Với cùng một trạng thái và cùng một đầu vào, đại lý tạo ra các hành động tương tự (hoặc di chuyển đến một ngôn ngữ xác định bên ngoài cho các cuộc gọi LLM).
- **Idempotent side effects.**Các cuộc gọi bên ngoài (các cuộc gọi công cụ, thanh toán) phải là không có khả năng hoặc sử dụng một khóa giảm trùng lặp.

LangGraph viết một điểm kiểm soát sau mỗi bước siêu; Temporal viết sau mỗi hoạt động; Restate sử dụng các tạp chí nguồn gốc sự kiện. Cả ba đều thực hiện mô hình tương tự.

### Một thời gian chạy điểm kiểm soát từng bước

Thời gian chạy của LangGraph là ví dụ được làm việc: mỗi đại lý có một `thread_id`; trạng thái là một lệnh đánh dấu; mỗi siêu bước viết một hàng cho bảng kiểm soát.`interrupt()`chờ đợi sự nhập cảnh của con người; thời gian chạy vẫn tồn tại và giải phóng người lao động.

Đây là thiết kế sản xuất tham chiếu vào tháng 4 năm 2026.

### Đường xếp hàng của MegaAgent cho mỗi đại lý

ArXiv:2408.09955 mô tả một thí nghiệm quy mô: hàng ngàn đại lý đồng thời trong một cụm.

```
agent i:
  state ∈ {Idle, Processing, Response}
  in_queue   <- messages addressed to agent i
  out_queue  -> replies + side effects

coordinators:
  intra-group chat  (agents in the same group)
  inter-group admin chat  (high-level routing)
```

Sự phối hợp hai lớp cho phép cuộc trò chuyện trong nhóm xảy ra dày đặc trong khi giữa nhóm vẫn còn hiếm  mô hình được sử dụng để giữ chi phí tuyến tính trong hàng ngàn đại lý.

### Async vs thread-per-job

Các cuộc gọi LLM là liên kết I / O. Một chuỗi chờ đợi token tiếp theo là vô hiệu 99% thời gian. Các chuỗi chi phí ~ 1MB RAM mỗi lần; với 10.000 cuộc gọi đồng thời, đó là 10GB chỉ cho các đống.

Sợi (Python `asyncio`, đi theo thói quen, Rust `tokio`(văn khoái) hợp tác trong I/O. Các cuộc gọi 10.000 tương tự phù hợp thoải mái trong quá trình.

Ngoại lệ: xử lý sau khi kết nối với CPU (trình tích hợp, các thủ thuật token) vẫn cần các chuỗi hoặc quy trình.

### Phản điểm của Bedi

"Scaling Agentic Software" (Ashpreet Bedi, 2026) lập luận rằng hầu hết các nhóm đã quá kỹ thuật trước khi đo tải.

- FastAPI + Postgres.
- Mỗi hành trình của đại lý là một hàng; trạng thái được cập nhật tại chỗ với sự đồng thời lạc quan.
- Các công việc trong nền tảng qua `pg_notify`hay một công nhân đơn giản của Celery.
- Lại thử chính sách trong mã ứng dụng.

Đối với tải dưới ~ 100 đồng thời chạy đại lý trên các nhiệm vụ có thể quản lý, đây thường là tất cả những gì bạn cần. nâng cấp khi bạn đo nó thất bại.

Quy tắc: áp dụng các khung thực hiện lâu dài khi bạn gặp một vấn đề cụ thể mà kiến trúc đơn giản không thể giải quyết.

### - Đúng là một lần -

Đối với các chuyến bay đại lý trả tiền, bạn cần "đúng một lần hiệu quả" (ít nhất một lần giao hàng + người tiêu dùng vô hiệu lực).

- **Dedup key per run.**Bao gồm nó trong mỗi cuộc gọi tác dụng phụ.
- **Outbox pattern.**Các tác dụng phụ viết cho một bảng trước, sau đó một quá trình riêng biệt thực hiện chúng.
- **Compensating transactions.**Khi một tác dụng phụ thành công nhưng ghi chép theo dõi của nó thất bại, lập kế hoạch một bù đắp.

Đây là các mô hình kỹ thuật cơ sở dữ liệu, không phải đặc biệt cho LLM. Thuế LLM chỉ là các cuộc gọi LLM chậm; tất cả những thứ khác là hệ thống phân tán tiêu chuẩn.

### Việc triển khai sơn sơn

Hệ thống nghiên cứu đa đại lý của Anthropic sử dụng "sử dụng cầu vồng": nhiều phiên bản của thời gian chạy đại lý chạy cùng lúc vì vậy các đại lý chạy lâu không phải bị giết chết trên mỗi bản triển khai mã.

Đây là tiêu chuẩn cho các hệ thống có trạng thái dài; sự thích nghi năm 2026 là các đại lý có thể sống trong nhiều giờ, vì vậy chu kỳ triển khai phải phù hợp.

### Danh sách kiểm tra sản xuất theo quy định

- Tương tự như là:
- - Hậu quả phụ không hiệu quả.
- Lớp I/O Async cho các cuộc gọi LLM.
- Ít nhất một lần giao hàng với Dedup.
- Việc triển khai rainbow/canary cho các khối lượng công việc đầy trạng thái.
- Hình ảnh: theo dõi mỗi đại lý, kiểm toán siêu bước, kiểm tra thử lại.

## Hãy xây dựng nó.
```figure
sw-checkpoint-replay
```

## Hãy xây dựng nó

`code/main.py`thực hiện:

- `CheckpointStore` Quý nhật ký điểm kiểm soát được hỗ trợ bởi SQLite với các khóa thread-id. Mỗi bước siêu thêm một hàng.
- `run_with_checkpoint(agent, thread_id)` mô phỏng một vụ tai nạn giữa chạy; một công nhân thứ hai tiếp tục từ điểm kiểm soát cuối cùng.
- `AgentQueue` mỗi đại lý Máy trạng thái không hoạt động / xử lý / phản ứng với hàng đợi làm việc nhỏ.
- `demo_async_vs_threads()` chạy 500 "call LLM" simulated đồng thời qua asyncio và qua các thread; báo cáo tường đồng hồ và bộ nhớ đỉnh (khoảng).

Đi chạy:

```
python3 code/main.py
```

Khả năng đầu ra dự kiến: Checkpoint resume thành công sau khi bị hỏng mô phỏng; phiên bản async xử lý 500 cuộc gọi đồng thời trong < 1s; phiên bản thread mất vài giây và sử dụng nhiều bộ nhớ hơn theo thứ tự trên mỗi đơn vị đồng thời.

## Sử dụng nó.

`outputs/skill-scaling-advisor.md`tư vấn về lựa chọn thực hiện bền: FastAPI + Postgres, LangGraph runtime, Temporal, hoặc tùy chỉnh.

## Đưa nó lên mạng

Thiết kế sản xuất canonical:

- **Start simple (Bedi's rule).**FastAPI + Postgres cho đến khi bạn đo lường nó thất bại.
- **Instrument everything before optimizing.**HISTORGAM HÀT LÀTN TẠI LÀN, thời gian mỗi bước, đếm lại, phân loại thất bại.
- **Outbox pattern for side effects.**Đặc biệt là thanh toán và các cuộc gọi API bên ngoài.
- **Rainbow deploys.**Đừng bao giờ giết người đang bay trong khi đang triển khai.
- **Adopt durable-execution engines (Temporal / LangGraph / Restate) when**Bạn gặp phải những vấn đề cụ thể: chờ đợi người trong vòng một giờ, phối hợp giữa các khu vực, các chính sách thử nghiệm lại / bồi thường phức tạp.
- **Async for the I/O layer.**Các dây chỉ dành cho xử lý sau khi kết nối với CPU.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đảm bảo điểm kiểm soát làm việc tiếp tục; đo async vs thread sự khác biệt đồng thời.
2. Thực hiện một**outbox**bảng: mỗi cuộc gọi công cụ viết vào hộp thư ra trước, sau đó một goroutine / nhiệm vụ riêng biệt được thực hiện.
3. Tưởng tượng một **rainbow deploy**: hai phiên bản chạy cùng lúc; chuyển hướng một nửa các thread_ids mới cho mỗi; xác nhận rằng các thread trong chuyến bay trên phiên bản cũ không bị gián đoạn.
4. Đọc tài liệu thời gian chạy của LangGraph (đối kết dưới đây). Xác định các tính năng thời gian chạy nào sẽ mất nhiều thời gian hơn để sao chép trong phiên bản FastAPI + Postgres được quét bằng tay. Đó là lý do để áp dụng, hoặc bạn có thể hoãn lại?
5. Đọc MegaAgent (arXiv:2408.09955) Phần 3. Sự phối hợp hai lớp (trong nhóm + trò chuyện quản trị viên giữa nhóm) là rõ ràng.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Durable execution / 持久执行 | "Persist the program state" / "持久化程序状态" | Engine writes state after each super-step; crash recovery is deterministic. / 引擎在每个超步后写入状态；崩溃恢复是确定性的。 |
| Super-step / 超步 | "Transactional boundary" / "事务边界" | Unit of work between checkpoints. LangGraph term. / 检查点之间的工作单元。LangGraph 术语。 |
| thread_id / 线程 ID | "Agent run identifier" / "Agent 运行标识符" | Key that binds checkpoints and resume logic. / 绑定检查点和恢复逻辑的键。 |
| Idempotency / 幂等性 | "Safe to retry" / "安全重试" | Repeating a side effect produces the same result as one attempt. / 重复副作用产生与一次尝试相同的结果。 |
| Outbox pattern / 发件箱模式 | "Decouple side effects" / "解耦副作用" | Write intent to a table; a separate executor performs and marks done. / 将意图写入表；单独的执行器执行并标记完成。 |
| At-least-once delivery / 至少一次投递 | "Possible duplicates" / "可能重复" | Message queue semantics; dedup key makes consumer effective-once. / 消息队列语义；去重键使消费者有效一次。 |
| Rainbow deploy / 彩虹部署 | "Overlapping versions" / "重叠版本" | Multiple runtime versions concurrent during long-running workloads. / 多个运行时版本在长时间工作负载期间并发。 |
| Async fiber / 异步纤程 | "Cooperative yielding" / "协作让步" | User-mode concurrency; cheap compared to threads for I/O-bound loads. / 用户态并发；I/O 密集负载下比线程廉价。 |
| Checkpoint / 检查点 | "State snapshot" / "状态快照" | Serialized state at a super-step boundary; key for resume. / 超步边界处的序列化状态；恢复的关键。 |

## Xem thêm 延伸阅读

- [LangChain — The runtime behind production deep agents](https://www.langchain.com/conceptual-guides/runtime-behind-production-deep-agents) Thiết kế thời gian chạy LangGraph
- [MegaAgent](https://arxiv.org/abs/2408.09955) hàng đầu sản xuất-thành khách mỗi đại lý; phối hợp hai tầng tại hàng ngàn đại lý đồng thời
- [Matrix](https://arxiv.org/abs/2511.21686) khung phân cấp với hàng rào thông điệp như là nền phối hợp
- [Temporal docs](https://docs.temporal.io/) động cơ lưu lượng công việc tham chiếu cho việc thực hiện lâu dài
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) Bài học sản xuất bao gồm việc triển khai cầu vồng
