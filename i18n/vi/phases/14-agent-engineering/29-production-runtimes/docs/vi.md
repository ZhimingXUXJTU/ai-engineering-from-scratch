# Thời gian sản xuất: Lịch trình, Sự kiện, Cron  sản xuất  vận hành  Liên minh châu Âu

> Các đại lý sản xuất chạy theo sáu hình dạng thời gian chạy: yêu cầu phản hồi, phát trực tuyến, thực hiện bền, nền dựa trên hàng, dựa trên sự kiện và lập lịch. Chọn hình dạng trước khi bạn chọn khung.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 22 (Voice) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

>  **【前置】**学本节前请先掌握:Phase 14·13(LangGraph) 状态图基础;Phase 17( hạ tầng & sản xuất) 本节是其前置概念,深入生产部署看Phase 17 全部。

## Mục tiêu học tập

- Hãy nêu tên sáu hình dạng thời gian chạy sản xuất và phù hợp với mỗi hình thức khung / sản phẩm.
- Giải thích tại sao việc thực hiện lâu dài (LangGraph) quan trọng đối với các nhiệm vụ dài hạn.
- Mô tả thời gian chạy theo sự kiện và khi nào Claude quản lý đại lý phù hợp.
- Giải thích yêu cầu có thể quan sát được khi tải về các chất đa bước.

## Vấn đề  vấn đề giới thiệu

Các đại lý sản xuất thất bại theo cách mà một sổ ghi chép Jupyter không xuất hiện: thời gian mạng ở bước 37, người dùng treo cuộc gọi giữa giọng nói, công việc cron chết khi khởi động lại máy, nhân viên nền hết bộ nhớ.

> Cách thất bại của sinh sản đại lý là Jupyter  ghi chép không thể thể hiện: 37 bước của mạng siêu thời gian, người dùng bị kết nối trong quá trình thoại thông qua, nhiệm vụ cố định trong máy tính khi khởi động lại, chết, sau đó máy tính trong bộ nhớ không có.


> **【中文解读】**Môi trường sản xuất Cơ quan vận hành cần xử lý các vấn đề không cần thiết về môi trường phát triển: trạng thái bền vững, dung lượng lỗi phục hồi, mở rộng cấp độ, giới hạn tốc độ, kiểm soát chi phí và khả quan.

>  **【类比】**6 种运行时 = 6 种交通工具:(1) **request-response**=出租车(一次一结,最简单);(2) **streaming**=高铁(边走边看风景,token 流式);(3) **durable execution**=房车(sleep one wake to continue open, LangGraph checkpoint);(4) **queue-based**=物流公司(任务排队,Celery/RQ);(5) **event-driven**=外卖平台(事件触发,Claude quản lý đại lý);(6) **scheduled**=钟(定时执行,cron) ・ nhiệm vụ多长多复杂 quyết định chọn nào──

> ️ **【易错点】**运行时选错的 3 个坑:(1) **长任务用 request-response**3 小时任务挂 HTTP 请求,nginx 60s 超时切断; dùng hiệu ứng bền vững(LangGraph) + 后台轮询──(2) **observability 当可选**上线后发现"不知道为失败"; từ ngày đầu tiên就接 Langfuse/LangSmith, mỗi công cụ调用都追踪──(3) **没做 graceful shutdown** dịch vụ khởi động lại khi đang thực hiện nhiệm vụ trực tiếp chết; sử dụng SIGTERM 子 lưu giữ điểm kiểm soát, khởi động lại sau khi từ điểm kiểm soát 续跑。

> **{【拓展：2026年生产 Agent 运行时的选择：(1) LangGraph Cloud——LangGrap...】}**2026年生产代理运行时的选择:(1) LangGraph CloudLangGraph's托管服务,内置状态检查点和重放;(2) Temporal通用工作流引擎,配合AI SDK可构建持久化代理;(3) tự xây dựng基于Redis/Kafka的消息队列 +自定义代理循环──关键决策因素是是否需要持久化执行如果代理可能运行数小时甚至数天,Temporal或LangGraph是更安全的选择──
## Khái niệm cốt lõi

### Đáp lại yêu cầu

- HTTP đồng bộ người dùng chờ kết thúc.
- Chỉ khả thi cho các nhiệm vụ ngắn (< 30s).
- Các đống: Agno (Python + FastAPI), Mastra (TypeScript + Express / Hono / Fastify / Koa).
- Tính năng quan sát: nhật ký truy cập HTTP tiêu chuẩn + phạm vi OTel.

### Chuyển phát

- SSE hoặc WebSocket cho phát triển tiến bộ.
- LiveKit mở rộng điều này cho WebRTC cho giọng nói / video (Dạy 22).
- Stacks: bất kỳ framework nào với hỗ trợ streaming + một frontend xử lý SSE/WS.
- Tính năng quan sát: thời gian mỗi phần, thời gian trễ đầu tiên, thời gian trễ đuôi.

### Thực hiện lâu dài

- Nhà nước kiểm soát sau mỗi bước; tự động tiếp tục khi thất bại.
- Mô hình diễn viên AutoGen v0.4 cô lập các thất bại với một đại lý (Dạy học 14).
- Các phân biệt nhân cốt lõi của LangGraph (Dạy học 13).
- Điều cần thiết khi số bước không được biết và chi phí phục hồi cao.

### Dựa trên hàng / nền

- Công việc vào hàng, nhân viên nhận, kết quả chảy về qua webhooks hoặc pub / sub.
- Khả năng thiết yếu cho các đại lý đường chân trời dài (chỉ hàng chục đến hàng trăm bước cho mỗi nhiệm vụ, cho mỗi thông báo sử dụng máy tính của Anthropic).
- Các đống: Celery (Python), BullMQ (Node), SQS + Lambda (AWS), tùy chỉnh.
- Sự quan sát: độ sâu hàng, phân phối độ trễ mỗi công việc, kích thước DLQ.

### Động cơ sự kiện

- Các đại lý đăng ký các kích hoạt: email mới, PR mở, cron fire.
- Claude quản lý đại lý bao gồm điều này ngoài hộp (Dạy học 17).
- CrewAI Flow (Dạy 15) cấu trúc các dòng công việc xác định dựa trên sự kiện.
- Hình ảnh: nguồn kích hoạt, thời gian trễ bắt đầu sự kiện, thời gian trễ của đại lý.

### Chương trình

- Các nhân viên hình Cron chạy thường xuyên.
- Kết hợp với việc thực hiện lâu dài để một cuộc chạy không thành công mỗi đêm tiếp tục lần tiếp theo.
- Stacks: Kubernetes CronJob + một framework bền; được lưu trữ (Render cron, Vercel cron).

### 2026 mô hình triển khai

- **CrewAI Flows**cho sản xuất dựa trên sự kiện.
- **Agno**FastAPI không có quốc gia cho các dịch vụ vi mô Python.
- **Mastra**Các bộ chuyển đổi máy chủ (Express, Hono, Fastify, Koa) để nhúng.
- **Pipecat Cloud / LiveKit Cloud**cho giọng nói được quản lý (Học 22).
- **Claude Managed Agents**cho sự đồng bộ hóa lâu dài được lưu trữ.

### Sự quan sát là chịu tải

Không có OpenTelemetry GenAI (Dạy 23) cộng với một Langfuse / Phoenix / Opik backend (Dạy 24) bạn không thể gỡ lỗi một đại lý đa bước đã thất bại ở bước 40.

> Không có OpenTelemetry GenAI span ((第 23 课) cộng với Langfuse/Phoenix/Opik 后端 ((第 24 课), bạn không thể调试 trong 40 步失败的多步代理―― điều này đối với môi trường sản xuất không phải là lựa chọn―― đây là sự khác biệt giữa "快速调试" và "从头重放并添加更多日志"――

> Việc triển khai, mở rộng và đáng tin cậy của đại lý. Các yếu tố quan trọng bao gồm: quản lý tình trạng, khôi phục sai lầm, hạn chế dòng chảy, quản lý hàng ngũ và kiểm soát chi phí.

### Khi thời gian chạy sản xuất không thành công

- **Wrong shape choice.**Chọn yêu cầu-phản ứng cho một nhiệm vụ 5 phút người dùng ngắt điện thoại, nhân viên tập hợp, thử lại hợp chất.
- **No DLQ.**Người lao động xếp hàng không có chữ cái chết.
- **Opaque background work.**Trình tác giả nền chạy mà không có dấu vết xuất khẩu.
- **Skipping durable state.**Bất kỳ chạy > 30 giây mà bạn không thể đủ khả năng khởi động lại cần thực hiện lâu dài.

> **错误的形态选择。**为 5 分钟 nhiệm vụ chọn yêu cầu-响应;; người dùng bị nhét;工作器堆积;重试叠;;
> **没有 DLQ。**队列工作器没有死信队列――失败任务消失――
> **不透明的后台工作。**后台 Agent 运行没有追踪导出――失败不可见直到用户报告――
> **跳过持久化状态。**Bất kỳ hoạt động nào dài hơn 30 giây và không thể chịu được khởi động lại đều cần phải được thực hiện lâu dài.

## Hãy xây dựng nó.
```figure
wb-runtime-shapes
```

## Hãy xây dựng nó

`code/main.py`là một stdlib nhiều hình dạng demo:

- Endpoint request-response (tức là hàm đơn giản).
- Bộ xử lý dòng chảy (generator).
- Một công nhân xếp hàng với DLQ.
- Đăng ký kích hoạt sự kiện.
- - Một trình lập lịch hình Cron.

Đi đi.

```bash
python3 code/main.py
```

Kết quả: năm dấu vết cho thấy hành vi của mỗi hình dạng trên cùng một nhiệm vụ. logic đại lý tương tự, các lớp vỏ bên ngoài khác nhau.

> 输出:五种追踪显示每种形态在同一任务上的行为――相同的代理逻辑,不同的外──持久化执行――第六种形态) 有意在第13 课中通过 LangGraph 检查点覆盖――

> Việc triển khai, mở rộng và đáng tin cậy của đại lý. Các yếu tố quan trọng bao gồm: quản lý tình trạng, khôi phục sai lầm, hạn chế dòng chảy, quản lý hàng ngũ và kiểm soát chi phí.

## Hãy sử dụng nó để thực hiện

- **Request-response**cho UX kiểu trò chuyện.
- **Streaming**cho các phản ứng tiến bộ.
- **Durable**cho các nhiệm vụ dài hạn.
- **Queue**cho lô / async / dài hạn.
- **Event**cho phản ứng của đại lý.
- **Cron**cho việc quản lý nhà (tăng cường bộ nhớ, đánh giá, báo cáo chi phí).

## Chuyển nó đi.

`outputs/skill-runtime-shape.md`chọn hình dạng runtime cho một nhiệm vụ và dây các yêu cầu khả năng quan sát.

> `outputs/skill-runtime-shape.md`Để chọn một hoạt động trong hình dạng và kết nối có thể quan sát được yêu cầu.

> Việc triển khai, mở rộng và đáng tin cậy của đại lý. Các yếu tố quan trọng bao gồm: quản lý tình trạng, khôi phục sai lầm, hạn chế dòng chảy, quản lý hàng ngũ và kiểm soát chi phí.

## Tập luyện bài tập

1. Chuyển tập 01 của bạn ReAct vòng lặp đến tất cả sáu hình dạng trong hàng của bạn. hình dạng nào phù hợp với bề mặt sản phẩm nào?
  Trung ngữ翻译:思考并实践此练习。
2. Thêm một DLQ vào trình diễn dựa trên hàng. mô phỏng thất bại 10% công việc; bề mặt DLQ kích thước.
  Trung ngữ翻译:思考并实践此练习。
3. Viết một đại lý đánh giá được kích hoạt cron chạy mỗi đêm với 20 dấu vết hàng đầu của ngày.
  Trung ngữ翻译:思考并实践此练习。
4. Thực hiện streaming với áp lực ngược: nếu khách hàng chậm, tạm dừng đại lý.
  Trung ngữ翻译:思考并实践此练习。
5. Khi nào bạn sẽ chuyển một nhân viên tự chủ đến quản lý?
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Request-response | "Synchronous" | User waits; short tasks only |  |
| Streaming | "SSE / WS" | Progressive output; better UX; latency observable per chunk |  |
| Durable execution | "Resume from failure" | Checkpointed state; restart at last step |  |
| Queue-based | "Background jobs" | Producer / worker pool / DLQ |  |
| Event-driven | "Trigger-based" | Agent reacts to external events |  |
| DLQ | "Dead-letter queue" | Parking lot for failed jobs |  |
| Claude Managed Agents | "Hosted harness" | Anthropic-hosted long-running async with caching + compaction |  |

## Xem thêm 延伸阅读

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) chi tiết thực hiện lâu dài
  Trung ngữ: 翻译:见原文.
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) máy tính không đồng bộ chạy lâu
  Trung ngữ: 翻译:见原文.
- [Anthropic, Introducing computer use](https://www.anthropic.com/news/3-5-models-and-computer-use) "chỉ hàng chục đến hàng trăm bước cho mỗi nhiệm vụ"
  Trung ngữ: 翻译:见原文.
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) Tự tách lỗi mô hình diễn viên
  Trung ngữ: 翻译:见原文.
