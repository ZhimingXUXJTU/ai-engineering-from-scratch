# Long-running Background Agents: Thử nghiệm lâu dài

> Các tác nhân tầm xa sản xuất không chạy vào `while True`. Mỗi cuộc gọi LLM trở thành một hoạt động với điểm kiểm tra, thử lại và chơi lại. Tích hợp SDK OpenAI Agents của Temporal đã được GA tháng 3 năm 2026. Claude Code Routines (Anthropic) chạy các cuộc gọi Claude Code được lên lịch mà không cần một quy trình địa phương liên tục. Các phiên tạm dừng vào người, tồn tại triển khai và tiếp tục từ điểm kiểm tra mới nhất được khóa bởi`thread_id`. Đằng sau công nghệ mới nằm một mô hình cũ  dàn xếp dòng công việc  với một đầu vào mới: LLM gọi là các hoạt động không xác định mà phải được tái diễn xác định khi phục hồi.

> **【中文解读】**生产长程 Đại lý không ở`while True`Trong hoạt động. Mỗi LLM 调用成为带检查点、重试和重放活动──Temporary of OpenAI Agents SDK 集成于 2026 年 3 月 GA。Claude Code Routines(Anthropic) trong một quá trình không tồn tại tại tại tại tại địa phương.

> **【拓展：LLM 调用 = 活动的精确契合】**LLM 调用完美匹配活动特征: không xác định: nhiệt độ > 0) 昂贵: tiền bạc và chậm trễ)  có thể thất bại: tốc độ giới hạn: quá thời gian  có tác dụng phụ: 调用工具)  đưa mỗi LLM 调用包装为活动即可获得指数退避重试,跨启检点和可重放调试追踪.`thread_id`+ 后端存储 + 最近检查点恢复──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, minimal durable-execution state machine) | **语言:** Python（标准库，最小持久执行状态机）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 01（长程 Agent）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 15·10(权限模式) Phase 15·01(长程 Agent) 分布式系统基础(检查点、重试、等)   执行持续 = 把 Agent 当工作流编排──
>  **【类比】**Thử nghiệm bền = "Bộ lưu trữ của đại lý"。 đại lý = 玩游戏没存档(崩=重头);Thử nghiệm bền = Mỗi LLM 调用后自动存档(崩=读最近的存档)。技巧关键: đưa mỗi LLM 调用包装为"活动",记录输入输出到日志,崩时重放日志 thay vì tái调用既省钱又避免副作用重复执行(如重复转账)。
> ️ **【易错点】**副作用工具(写数据库、调外部 API) không lưu ý quyền hạn khóa → 恢复时重复执行可能导致业务错误(用户被扣两次款) ――修复: mỗi tác dụng phụ调必须带等键(如`idempotency-key: uuid`),后端按键去重──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**持久执行确保 Agent 任务在故障后能恢复――传统 Agent 在内存运行,进程崩意味着从头开始――持久执行将状态保存到外部存储 (database、文件系统),任何时刻都可以从最近检查点恢复――Temporal 和 LangGraph là hai khung chính thức thực hiện việc执行持久――

> **【拓展：durable execution】**持久执行对长时间运行的代理 至关重要―― Nếu một người cần phải运行 2 小时的代理 在第90 分钟崩,没有持久执行就意味着重新开始―― 暂时通过事件追溯源实现持久工作流,LangGraph通过检查点实现持久状态图――2026 年的最佳实践是每一个重要步骤后自动保存检查点――

Hãy xem xét một đại lý chạy trong bốn giờ. Nó gọi ba công cụ, nhắc người dùng hai lần, và thực hiện bốn mươi cuộc gọi LLM.

> 考虑一个运行四小时的代理――它调用三个工具――提示用户两次――进行40次 LLM 调用――中途,运行的主机重新启动――

Chuyện gì xảy ra?

> Chuyện gì xảy ra?

- Trong một sự ngây thơ `while True`vòng lặp: tất cả đều bị mất. Cuộc chạy bắt đầu lại từ đầu. Ba cuộc gọi công cụ (với tác dụng phụ thực sự) thực hiện lại. Người dùng được nhắc lại về những thứ họ đã phê duyệt.
  Trung ngữ翻译:在朴素 `while True`循环中:一切丢失──运行从头头重新启动──三工具调用──带真实副作用) 再执行──用户再次被提示已批准的事──40 个 LLM 调用重新计费──
- Với việc thực hiện lâu dài: chạy tiếp tục từ điểm kiểm soát gần đây nhất. Các hoạt động đã hoàn thành không được thực hiện lại; kết quả của chúng được phát lại từ nhật ký lâu dài. Người dùng không phê duyệt lại những thứ họ đã chấp thuận. Các cuộc gọi LLM đã thực hiện không được tính lại.
  Trung ngữ翻译:有持久执行时:运行从最近检查点恢复──已完成活动不重新执行; 其结果从持久日志重放──用户不重新批准已批准的事──已做 LLM 调用不重新计费──

Đây là mô hình tương tự mà các công cụ lưu lượng công việc đã đưa ra trong một thập kỷ (Temporal, Cadence, Cherami của Uber). Điều mới là các cuộc gọi LLM bây giờ là một loại hoạt động không xác định, đắt tiền, với tác dụng phụ và chúng phù hợp với mô hình này một cách sạch sẽ.

> Đây là mô hình tương tự của xuất khẩu công cụ lao động trong thập kỷ qua.

> **【中文解读】**持久化执行解决长程 经纪人的可靠性问题:四小时运行中主机重启时,朴素循环丢失一切(工具重新执行、用户重新审批、LLM 重新计费),而持久化执行从最近检查点恢复,已完成的活动从持久日志重放而不是重新执行──Temporary OpenAI Agents SDK 集成于2026 年 3 月 GA──核心洞察:LLM调用是一种无确定性、昂贵、有副作用活动,完美适应工作流引擎模式──

Chủ đề của bài học: độ tin cậy về đường chân trời dài suy giảm (METR quan sát "sự suy giảm 35 phút"  tỷ lệ thành công giảm gần như bằng hình vuông với đường chân trời).

> Chủ đề hoạt động của bài này: Long Range Reliability Recession (DRA): METR  quan sát "35 phút suy giảm" tỷ lệ thành công với thời gian (LINE 大致平方反比下降) 

## Khái niệm cốt lõi

### Các hoạt động, quy trình làm việc, và chơi lại.

- **Workflow**: mã dàn xếp xác định. Định nghĩa chuỗi các hoạt động, các nhánh, chờ đợi. Phải xác định để nó có thể được chơi lại từ nhật ký sự kiện mà không có sự khác biệt đáng ngạc nhiên.
  Trung ngữ翻译:**工作流**: xác định tính lập trình mã số. Định nghĩa chuỗi hoạt động.
- **Activity**: một đơn vị công việc không xác định, có khả năng thất bại. LLM call, tool call, file write, HTTP request.
  Trung ngữ翻译:**活动**: không xác định, có thể thất bại trong các đơn vị làm việc.
- **Event log**: cửa hàng hỗ trợ bền vững. Mỗi hoạt động bắt đầu, hoàn thành, thất bại, thử lại, và mỗi quyết định về dòng công việc được ghi lại.
  Trung ngữ翻译:**事件日志**:持久后端存储. Mỗi hoạt động bắt đầu, hoàn thành, thất bại, thử lại và mỗi quyết định trong dòng công việc được ghi lại.
- **Replay**: khi phục hồi, mã workflow chạy lại từ đầu; mỗi hoạt động đã hoàn thành trả lại kết quả ghi lại mà không cần thực hiện lại. Chỉ có các hoạt động chưa hoàn thành thực sự được chạy.
  Trung ngữ翻译:**重放**: hồi phục, workflow code chạy lại từ đầu; mỗi hoạt động đã hoàn thành trở lại kết quả ghi lại mà không thực hiện lại.

Đây là hình dạng tương tự như React tái tạo với một DOM ảo, hoặc Git xây dựng lại một cây làm việc từ commit.

> Đây là tương tự như React  đối với DOM ảo tái tạo hoặc Git từ trình bày tái tạo giống nhau hình dạng của cây làm việc.

### Tại sao LLM gọi phù hợp với mô hình này

Các cuộc gọi LLM là:

> LLM 调用是:

- Không xác định (nhiệt độ > 0; thậm chí nhiệt độ 0 biến động giữa các phiên bản mô hình).
  中文翻译:非确定性( nhiệt độ > 0; ngay cả khi nhiệt độ 0 跨模型版本漂移) 』
- Giá cả đắt (tiền và thời gian trễ).
  Trung ngữ翻译:昂贵(金钱和延迟)
- Khả năng thất bại (giới hạn lãi suất, thời gian trễ).
  Trung文翻译:可能失败(速率限制、超时)
- Tác dụng phụ (nếu họ gọi các công cụ).
  Trung文翻译: có tác dụng phụ

Đó chính xác là hồ sơ hoạt động. Kết thúc mỗi cuộc gọi LLM như một hoạt động cho bạn thử lại với sao chép sao chép, kiểm tra qua khởi động lại, và một dấu vết có thể chơi lại để gỡ lỗi.

> Đây là hồ sơ hoạt động. Mỗi LLM sẽ sử dụng gói để hoạt động cho bạn chỉ số quay lại kiểm tra, qua các điểm kiểm tra và có thể theo dõi kiểm tra.

### Các điểm kiểm soát được khóa bởi `thread_id``thread_id`Vì vậy, điểm kiểm tra

LangGraph, Microsoft Agent Framework, Cloudflare Durable Objects và Claude Code Routines đều hội tụ trên cùng một hình dạng API: a `thread_id`(hoặc tương đương) xác định phiên; mỗi chuyển đổi trạng thái vẫn tồn tại cho một backend (PostgreSQL mặc định, SQLite cho dev, Redis cho cache); tiếp tục đọc điểm kiểm tra mới nhất.

> LangGraph、Microsoft Agent Framework、Cloudflare Durable Objects 和 Claude Code Routines đều nhận được cùng một API 形态:`thread_id`(hoặc giá cả tương tự) 识别会话; mỗi trạng thái chuyển đổi持久化到后端(默认 PostgreSQL、dev dùng SQLite、缓存 dùng Redis);恢复读最新检查点。

Sự lựa chọn của backend quan trọng:

> 后端选择 quan trọng:

- **PostgreSQL**: bền, truy vấn, tồn tại khi triển khai.
  Trung ngữ翻译:**PostgreSQL**Đọc: 持久、可查询、跨部署存活──LangGraph 默认──
- **SQLite**: chỉ là local-dev; mất dữ liệu trên các máy chủ.
  Trung ngữ翻译:**SQLite**: chỉ phát triển bản địa; qua cơ hội mất dữ liệu.
- **Redis**: nhanh nhưng ngắn ngủi trừ khi có cấu hình AOF/phình ảnh.
  Trung ngữ翻译:**Redis**:快但临时, trừ khi định vị AOF/快照。
- **Cloudflare Durable Objects**: được phân phối minh bạch; được định đoan bởi một khóa độc đáo; tồn tại trong nhiều giờ đến vài tuần.
  Trung ngữ翻译:**Cloudflare Durable Objects**: transparent distributed;以唯一键为范围;存活数小时到数周.

### Sự nhập cảnh của con người như một quốc gia hạng nhất.

Đề xuất sau đó cam kết (Dạy 15) đòi hỏi một trạng thái "ngợi đợi con người" lâu dài. Luôn lưu lượng công việc dừng lại, hàng đợi bên ngoài giữ yêu cầu đang chờ đợi, và sự chấp thuận bắt đầu lại từ điểm đó.

> đề xuất-sau-thành động (第 15 课) cần duy trì" chờ loài người" trạng thái.

### Sự suy giảm 35 phút.

METR quan sát thấy rằng mỗi lớp chất đo lường cho thấy sự suy giảm độ tin cậy vượt quá ~ 35 phút hoạt động liên tục.

> METR  quan sát từng phép đo 类别 đại lý trong khoảng 35 phút tiếp tục vận hành đều cho thấy sự suy giảm độ tin cậy.

Việc tăng gấp đôi thời gian nhiệm vụ gần như tăng tỷ lệ thất bại gấp bốn lần. Việc thực hiện lâu dài không khắc phục điều này; nó cho phép bạn chạy lâu hơn hồ sơ độ tin cậy hỗ trợ.

> 任务时长大致使失败率翻倍四倍──持久执行不修复此; nó giúp bạn chạy hơn hơn hơn đáng tin cậy tài liệu hỗ trợ hơn.

### Khi hành động lâu dài là câu trả lời sai.

- Đi chạy ngắn hơn vài phút mà không có sự tham gia của con người.
  Trung ngữ翻译:短于几分钟无人输入的运行──开销 > 收益──
- Khóa thông tin chỉ đọc.
  Trung ngữ翻译:严格只读信息检索。
- Các nhiệm vụ khi sự chính xác đòi hỏi kết thúc đến kết thúc trong một cửa sổ ngữ cảnh (một số nhiệm vụ lý luận; một số việc tạo ra một lần).
  Trung ngữ翻译:正确性需要在一个上下文窗口内端到端的任务(某些推理任务;某些一次性生成)

## Hãy sử dụng nó để thực hiện
```figure
memory-consolidation
```

## Sử dụng nó

`code/main.py`thực hiện một công cụ thực hiện bền tối thiểu trong stdlib Python. Nó hỗ trợ:

> `code/main.py`Sử dụng Python 实现最小持久执行引擎──它支持:

- `@activity`Decorator ghi nhập và đầu ra vào nhật ký sự kiện JSON.
  Trung ngữ翻译:`@activity`装饰器将输入输出记录到 JSON 事件日志。
- Một chức năng lưu lượng công việc theo trình tự các hoạt động.
  Trung文翻译:将活动排序的工作流函数──
- A `run_or_replay(workflow, event_log)`chức năng tái phát các hoạt động đã hoàn thành mà không thực hiện lại chúng.
  Trung ngữ翻译:`run_or_replay(workflow, event_log)`函数重放已完成活动而不重新执行──

Người lái xe mô phỏng một dòng công việc ba hoạt động, bị đâm vào nửa đường, và cho thấy (a) một lần thử lại ngây thơ thực hiện lại mọi thứ so với (b) một lần lặp lại chỉ chạy hoạt động thiếu.

> 驱动器模拟三活动工作流,中途崩,展示 (a) 朴素重试重新执行一切对 (b) 重放只运行缺失活动──

## Chuyển nó đi.

`outputs/skill-durable-execution-review.md`xem xét việc triển khai đại lý lâu dài được đề xuất để xác định hình thức thực hiện lâu dài chính xác: hoạt động, quyết định, hậu quả kiểm soát, trạng thái nhập người và chính sách HITL-on-resume.

> `outputs/skill-durable-execution-review.md`审查 đề xuất  ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành ng thời gian vận hành  thời gian vận hành  thời gian vận hành  thời gian vận hành  thời gian vận hành  thời gian vận hành  thời gian vận hành  thời gian vận hành  thời gian vận hành  thời gian vận hành 

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Quan sát sự khác biệt trong số lượng hoạt động-lực hiện giữa thử lại ngây thơ và tái diễn. Thay đổi điểm sụp đổ và hiển thị số lượng tái diễn thay đổi tương ứng.
   Trung ngữ翻译:运行 `code/main.py`❖ quan sát đơn giản thử và tái tạo giữa các hoạt động thực hiện tính toán khác nhau.

2. Chuyển đổi động cơ đồ chơi để sử dụng `thread_id`Mô phỏng hai phiên đồng thời chia sẻ động cơ và xác nhận nhật ký sự kiện của họ không va chạm.
   Trung ngữ翻译:将玩具引擎转为显式使用 `thread_id`❖模拟共享引擎的两个发发会话并确认其事件日志不冲突──

3. Hãy lấy một hoạt động trong động cơ đồ chơi. Đưa ra một sự không xác định (một dấu thời gian của đồng hồ tường bên trong quyết định luồng làm việc).`Workflow.now()`API).
   Trung ngữ翻译:在玩具引擎中取一个活动──引入不确定性──工作流决策内壁钟时间)──演示重放上的分歧──解释真实引擎如何处理──副作用注册──`Workflow.now()`API) 

4. Đọc bài đăng "Runtime Behind Production Deep Agents" của LangChain, liệt kê từng trạng thái mà runtime vẫn tồn tại và đặt tên chế độ thất bại nào được bao gồm.
   Trung ngữ翻译:阅读 LangChain's "Runtime behind production deep agents"文章──列出运行时持久化的每个状态并命名各覆盖的失败模式──

5. Thiết kế một chính sách kiểm soát điểm cho một nhiệm vụ lập mã tự trị 6 giờ. Bạn kiểm soát điểm ở đâu?
   Trung ngữ翻译:为6小时自主编码任务设计检查点策略──你在哪个检查点?崩恢复什么样?什么需要新鲜HITL?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Workflow | "Agent's script" | Deterministic orchestration code; replayable from event log |
| 工作流 | "Agent 的脚本" | 确定性编排代码；可从事件日志重放 |
| Activity | "A step" | Non-deterministic unit (LLM call, tool call); logged before and after |
| 活动 | "一步" | 非确定性单元（LLM 调用、工具调用）；前后记录 |
| Event log | "The backing store" | Durable record of every state transition |
| 事件日志 | "后端存储" | 每个状态转换的持久记录 |
| Replay | "Resume" | Re-run workflow; completed activities return logged results without re-execution |
| 重放 | "恢复" | 重跑工作流；已完成活动返回记录结果而不重新执行 |
| Checkpoint | "Save point" | Persisted state keyed by thread_id; latest-wins on resume |
| 检查点 | "保存点" | 以 thread_id 为键的持久状态；恢复时最新优先 |
| thread_id | "Session key" | Identifier that scopes durable state |
| thread_id | "会话键" | 范围化持久状态的标识符 |
| 35-minute degradation | "Reliability decay" | METR: success rate drops ~quadratically with horizon |
| 35 分钟衰减 | "可靠性衰减" | METR：成功率与时间线大致平方反比下降 |
| Non-determinism | "Drift on replay" | Wall clock, random, LLM output; must be registered as side effect |
| 非确定性 | "重放漂移" | 墙钟、随机、LLM 输出；必须注册为副作用 |

## Xem thêm 延伸阅读

- [Anthropic — Claude Code Agent SDK: agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) ngân sách, quay và tiếp tục ngữ nghĩa.
  Trung ngữ翻译:预算、轮次和恢复语义。
- [Microsoft — Agent Framework: human-in-the-loop and checkpointing](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) RequestInfoEvent hình dạng.
  中文翻译:RequestInfoEvent 形态。
- [LangChain — The Runtime Behind Production Deep Agents](https://www.langchain.com/conceptual-guides/runtime-behind-production-deep-agents) yêu cầu cụ thể về thời gian chạy.
  Trung ngữ翻译:具体运行时要求。
- [OpenAI Agents SDK + Temporal integration (Trigger.dev announcement)](https://trigger.dev) hình thức hoạt động cho các cuộc gọi LLM.
  Trung文翻译:LLM 调用活动形态。
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) chỉ số phân rã 35 phút.
  Trung ngữ翻译:35 分钟衰减参考──
