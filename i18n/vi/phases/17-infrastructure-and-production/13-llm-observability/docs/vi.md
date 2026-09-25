# LLM Observability Stack Selection  可观测性  chọn LLM

> Thị trường khả năng quan sát năm 2026 chia thành hai loại. Các nền tảng phát triển (LangSmith, Langfuse, Comet Opik) kết hợp giám sát với các đánh giá, quản lý nhanh chóng, lặp lại phiên. Các công cụ Gateway/instrumentation (Helicone, SigNoz, OpenLLMetry, Phoenix) tập trung vào viễn thông. Langfuse là lõi được cấp phép MIT với cân bằng OSS mạnh (50K sự kiện / tháng đám mây miễn phí). Phoenix là OpenTelemetry-native dưới Elastic License 2.0  tuyệt vời cho việc hình dung drift / RAG, không phải là một backend sản xuất bền vững. Arize AX sử dụng tích hợp Iceberg / Parquet không sao chép bằng cách tuyên bố giá rẻ hơn 100 lần so với khả năng quan sát monolithic. LangSmith dẫn đầu cho LangChain / LangGraph, $ 39 / người dùng / tháng, tự lưu trữ trong Enterprise chỉ. Helicone dựa trên proxy với 15-30 phút thiết lập, 100K req / mo miễn phí, nhưng ít sâu hơn trên dấu vết của đại lý. Mô hình sản xuất chung: Gateway (Helicone/Portkey) + nền tảng eval (Phoenix/TruLens) dán bằng OpenTelemetry.

> **【中文解读】**Bài viết này giới thiệu về LLM có thể quan sát được  giám sát và điều tra LLM 推理服务的工具和方法──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy trace-sampling simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 08 (Inference Metrics), Phase 14 (Agent Engineering) | **前置知识:** Phase 17 · 08 (Inference Metrics), Phase 14 (Agent Engineering)

>  **【前置】**学本节前请先掌握:Phase 17·08(推理指标) 、Phase 14(Agent 工程) ・LLM 可观测性两类工具:开发平台 + Gateway/遥测。
>  **【类比】**可观测性工具 = "AI 应用的体检设备"――开发平台(LangSmith/Langfuse/Phoenix) = 全身体检(含评估、快速管理、会话回放);Gateway(Helicone/Portkey) = 心率手环(轻量代理、15-30 分钟部署)。Langfuse 开源 50K 事件/月免费;LangSmith 在 LangChain 生态领先 $39 /用户/月;Helicone 100K 请求/月免费;;生产典型组合:Gateway + 评估平台 + OpenTelemetry 水;;
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Sự khác biệt giữa các nền tảng phát triển (được tập hợp: đánh giá + yêu cầu + phiên) và các công cụ gateway/telemetry (chỉ theo dõi + métrics).
  Trung ngữ翻译:区分开发平台(捆绑:评估 + 提示管理 + 会话)
- Bản đồ sáu công cụ chính (Langfuse, LangSmith, Phoenix, Arize AX, Helicone, Opik) cho các trường hợp cấp phép, giá cả và sử dụng điểm ngọt của họ.
  Trung文翻译:将六个主要工具(Langfuse、LangSmith、Phoenix、Arize AX、Helicone、Opik)映射到其许可、定价和最佳使用例──
- Giải thích mô hình dán OpenTelemetry cho phép bạn kết hợp công cụ cửa ngõ với nền tảng đánh giá riêng biệt.
  Trung ngữ翻译:解释 OpenTelemetry 水模式,该模式允许你将网关工具与独立评估平台组合──
- Hãy nêu tên phân biệt chi phí năm 2026 (chương pháp sao chép bằng không của Arize AX so với tiêu thụ đơn phương) và nêu số nhân khoảng 100x.
  Trung ngữ翻译:说出 2026 年的成本差异化因素(Arize AX 的零拷贝方法 vs 单体式摄入)并说明大约100倍的乘数──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**LLM 可观测性工具分为两类:(1) 开发平台(LangSmith、Langfuse、Opik) 捆绑监控、评估、提示管理、会话回放;(2) 网关/遥测工具(Helicone、SigNoz、OpenLLMetry、Phoenix) 专注于遥测采集──选择涉及四个维度:技术(LangChain?原始 SDK、?) 需求许可证(MIT only?商业可接受?)、预算、自托管──

> **【拓展：LLM 可观测性市场格局】**Các cầu thủ quan trọng của thị trường LLM 可观测性市场:(1) Langfuse(MIT 开源,50K sự kiện/tháng 免费云)LangSmith 级功能但可自托管;(2) LangSmith(商业,$39/user/month)LangChain 生态最佳;(3) Phoenix(Elastic License 2.0) RAG/漂移可视化优秀;(4) Arize AX(商业) zero-copy Iceberg/Parquet,号称比单体可观便性宜100x;(5) Helicone(MIT,100K req/tháng 免费) proxy-based,15-30 分钟设置──生产常见模式是:网关水 ?? /key) ((((Phoenix 评估平台/Tru Telemetrics 通过连接

Bạn đã gửi một tính năng LLM. Nó hoạt động. Bạn không có khả năng nhìn thấy các lỗi nhanh, vòng lặp công cụ, hồi quy độ trễ, tăng chi phí hoặc tỷ lệ hit của cache nhanh. Bạn Google "Làm chứng của LLM" và nhận được tám công cụ tất cả tuyên bố họ giải quyết cùng một vấn đề với ba điểm giá khác nhau.

Họ không giải quyết cùng một vấn đề. LangSmith trả lời "tại sao chạy LangGraph này thất bại?" Phoenix trả lời "hợp ống RAG của tôi đang dẫn dắt?" Helicone trả lời "tên nào đang đốt token?" Langfuse trả lời "Tôi có thể tự lưu trữ toàn bộ nó không?"

Việc chọn bao gồm bốn trục: hàng đống (LangChain? SDK nguyên liệu? đa nhà cung cấp?), dung nạp giấy phép (chỉ MIT? Elastic OK? phạt thương mại?), ngân sách (tầng miễn phí? $100/mo? $1000/mo?), và tự chủ (đáng lẽ phải? tốt để có? bao giờ?).

## Khái niệm cốt lõi

### Hai loại

**Development platforms**bạn chạy thí nghiệm, xem prompt nào hoạt động, set dữ liệu trở lại một prompt mới chống lại những người chiến thắng cũ. LangSmith, Langfuse, Comet Opik.

**Gateway/telemetry tools**Các công cụ kết luận gọi  prompt, phản ứng, token, độ trễ, mô hình, chi phí. Helicone, SigNoz, OpenLLMetry, Phoenix. Minimalist. Có thể được kết hợp với một công cụ đánh giá riêng biệt thông qua OpenTelemetry.

### Longfuse  cân bằng OSS

> **【拓展：LLM 可观测性工具选型决策】**2026 năm LLM 可观测性工具选型的关键维度:(1) 技术LangChain/LangGraph 生态优先选 LangSmith;自研 SDK 选 Langfuse或Phoenix;(2) 许可证要求 MIT 选 Langfuse/Opik;Elastic License 2.0 可接受选 Phoenix;商业可选 LangSmith;(3) 接受自托管必须自托管选 Langfuse或Opik(Docker 部署);(4) 预算免费层 Langfuse 50K sự kiện/tháng、Helicone 100K req/tháng;(5) 规模>10M dấu vết/ngày 选 Arize AX 零拷贝架构.

- Core Apache / MIT cấp phép; tự lưu trữ thông qua Docker.
- Tầng mây miễn phí: 50 nghìn sự kiện/tháng.
- Evals, quản lý nhanh chóng, dấu vết, tập hợp dữ liệu, bảo hiểm hợp lý của tất cả bốn tính năng của nền tảng phát triển.
- Điểm ngọt ngào: bạn muốn các tính năng lớp LangSmith nhưng phải tự lưu trữ hoặc ở lại giấy phép OSS.

### Phoenix (Arize)  Telemetry-first, OpenTelemetry-native

- Giấy phép 2.0; tự chủ, tầm thường.
- Tốt nhất trong RAG và hình ảnh drift.
- Không được thiết kế như là hậu trường sản xuất bền vững  chủ yếu là khả năng quan sát trong thời gian phát triển.
- Điểm thích hợp: Phát triển đường ống RAG, điều chỉnh drift, cặp với một cửa cổng riêng cho sản xuất.

### Arize AX  chơi quy mô

- Tiếp thị, tích hợp dữ liệu hồ nước bằng Iceberg/Parquet.
- Thuyết toán: bạn lưu trữ dấu vết trong Parquet của riêng bạn trên S3; Arize đọc trực tiếp.
- Điểm mấu chốt: > 10M dấu vết/ngày, hồ dữ liệu hiện có, muốn bảng điều khiển cụ thể LLM mà không có giá Datadog.

### LangSmith  LangChain/LangGraph đầu tiên

- Tiếp thị, 39 đô la/tháng, tự lưu trữ chỉ trên Enterprise.
- Tốt nhất trong lớp cho các đống LangChain và LangGraph. Nếu bạn không tham gia vào cả hai, nó ít hấp dẫn hơn.
- Địa điểm ngọt ngào: đội ngũ cam kết với LangChain, sẵn sàng trả tiền.

### Helicone  dựa trên proxy tối thiểu khả thi

- 15-30 phút thiết lập bằng cách đổi `OPENAI_API_BASE`cho nhân viên của Helicone.
- MIT cấp phép; 100K req / tháng miễn phí, trả $20 / tháng +.
- Bao gồm failover, cache, giới hạn lãi suất  cũng hoạt động như một cổng thông tin.
- Độ sâu thấp hơn trên các dấu vết đại lý / nhiều bước.
- Sweet spot: khởi động nhanh, ứng dụng đơn, cần gateway + khả năng quan sát trong một.

### Opik (Comet)  nền tảng phát triển OSS

- Apache 2.0, hoàn toàn OSS.
- Một tính năng tương tự như Langfuse với di sản sao chổi.
- Địa điểm ngọt ngào: các nhóm ML đã ở trên Comet, muốn LLM có thể quan sát được trong cùng một bảng.

### SigNoz  OpenTelemetry- đầu tiên APM đầy đủ

- Apache 2.0. xử lý APM chung cộng với LLM thông qua OpenTelemetry.
- Điểm ngọt ngào: khả năng quan sát thống nhất giữa các dịch vụ và các cuộc gọi LLM.

### Lớp dán: OpenTelemetry + GenAI các quy ước ngữ nghĩa

> **【中文解读】**OpenTelemetry vào cuối năm 2025 đã phát hành GenAI 语义约定(`gen_ai.system``gen_ai.request.model``gen_ai.usage.input_tokens`),让不同工具可以互操作──2026年的生产模式是:(1) Từ mỗi LLM 调用发发带 GenAI 约定的 OTel;(2) 路由到网关(Helicone/Portkey)做日常监控;(3) 双写到评估平台(Phoenix/Langfuse)做回归检测;(4) 存档到数据湖(Iceberg) thông qua Arize AX hoặc DuckDB做长期分析──

> **【拓展：LLM 可观测性的成本控制】**Trong quy mô > 1M yêu cầu/ ngày, toàn bộ lượng phí bảo tồn vượt quá LLM 调用 bản thân.

OpenTelemetry đã công bố các công ước ngữ nghĩa GenAI vào cuối năm 2025 (`gen_ai.system`- `gen_ai.request.model`- `gen_ai.usage.input_tokens`Các công cụ tiêu thụ OTel có thể tương tác.

1. Cho phép OTel với các hội nghị GenAI từ mỗi cuộc gọi LLM.
2. Hành trình đến cổng (Helicone / Portkey) cho ngày càng ngày.
3. Dual-ship to eval platform (Phoenix / Langfuse) cho các regressions.
4. Tái lưu trữ trong hồ dữ liệu (Iceberg) để phân tích lâu dài thông qua Arize AX hoặc DuckDB.

### Trạm: dùng dụng cụ ở lớp sai

> **【中文解读】**埋点层级的选择: 在 Agent 框架内埋点 (如添加 LangSmith traces) 会合到这个框架; 在 HTTP/OpenAI-SDK 层埋点 (通过 OpenLLMetry或网关)则可移植──2026 年的最佳实践是协议层埋点无论底层使用什么框架,都通过 OpenTelemetry + GenAI 语义约定统一采集──

Các công cụ bên trong khung đại lý của bạn (ví dụ, thêm dấu vết LangSmith) kết nối bạn với khung đó.

### Chọn mẫu, không thể giữ được tất cả.

Với > 1M yêu cầu/ngày, việc giữ lại toàn bộ chi phí cao hơn các cuộc gọi LLM. Dấu mẫu theo quy tắc: 100% lỗi, 100% chi phí cao, 5% thành công.

### Những con số mà bạn nên nhớ

- Lớp đám mây miễn phí Langfuse: 50K sự kiện/tháng.
- LangSmith: 39 đô la/tháng.
- Không sử dụng trực thăng: 100K req/tháng.
- Arize AX tuyên bố: ~ 100 lần rẻ hơn so với monolithic trên quy mô.
- Công ước OpenTelemetry GenAI: 2025 vận chuyển, 2026 được chấp nhận rộng rãi.

## Hãy sử dụng nó để thực hiện
```figure
i4-otel-glue
```

## Sử dụng nó

`code/main.py`mô phỏng một ngày theo dõi 1M trên các chiến lược giữ lại (100% tiêu thụ, lấy mẫu, lấy mẫu + lỗi). báo cáo chi phí lưu trữ và những gì bị mất dưới mỗi.

> `code/main.py`mô phỏng một ngày theo dõi 1M trên các chiến lược giữ lại (100% tiêu thụ, lấy mẫu, lấy mẫu + lỗi). báo cáo chi phí lưu trữ và những gì bị mất dưới mỗi.

> `code/main.py`mô phỏng một ngày theo dõi 1M trên các chiến lược giữ lại (100% tiêu thụ, lấy mẫu, lấy mẫu + lỗi). báo cáo chi phí lưu trữ và những gì bị mất dưới mỗi.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-observability-stack.md`. Với hàng, quy mô, ngân sách, tư thế giấy phép, chọn công cụ (s).

> 本课产 出 `outputs/skill-observability-stack.md`. Với hàng, quy mô, ngân sách, tư thế giấy phép, chọn công cụ (s).

## Tập luyện bài tập

1. Nhóm của anh ở LangChain muốn OSS tự lưu trữ khả năng quan sát.
   Trung ngữ翻译:你的团队使用LangChain,想要开源自托管可观测性──选择Langfuse或Opik 并说明理由──
2. Với 5M tracks/day với Datadog trích dẫn 150K USD/tháng, tính toán break-even cho Arize AX.
   Trung文翻译: 在 5M 痕迹/日 规模下,Datadog 报价 $ 150K/月,计算Arize AX 零拷贝方案的亏平衡点──
3. Thiết kế một thuộc tính OpenTelemetry GenAI đặt hướng dẫn của tổ chức của bạn nên yêu cầu trong mỗi cuộc gọi LLM.
   Trung ngữ翻译:设计一个你的组织指南应强制要求每次 LLM 调用包含的 OpenTelemetry GenAI 属性集──
4. Thảo luận liệu Phoenix một mình có đủ cho sản xuất.
   Trung ngữ翻译:论证 Phoenix 单独使用是否足以满足生产需求――它在什么情况下不够?
5. Helicone là 20ms đại diện trênheadhead. tại P99 TTFT 300ms, đó là chấp nhận được?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| OpenLLMetry | "OTel for LLMs" | Open-source OpenTelemetry instrumentation for LLMs |
| GenAI conventions | "OTel attributes" | Standard OTel attribute names for LLM calls |
| LangSmith | "LangChain observability" | Commercial platform bundled with LangChain ecosystem |
| Langfuse | "OSS LangSmith" | MIT OSS with similar feature set |
| Phoenix | "Arize dev tool" | OpenTelemetry-native dev/eval platform |
| Arize AX | "scale observability" | Commercial zero-copy Iceberg/Parquet observability |
| Helicone | "proxy observability" | HTTP proxy collecting LLM telemetry + gateway features |
| Opik | "Comet LLM" | Apache 2.0 OSS dev platform from Comet |
| Session replay | "trace rerun" | Replay a full agent session with tool calls |
| Eval | "offline test" | Running candidate model/prompt over labeled dataset |

## Xem thêm 延伸阅读

- [SigNoz — Top LLM Observability Tools 2026](https://signoz.io/comparisons/llm-observability-tools/)
- [Langfuse — Arize AX Alternative analysis](https://langfuse.com/faq/all/best-phoenix-arize-alternatives)
- [PremAI — Setting Up Langfuse, LangSmith, Helicone, Phoenix](https://blog.premai.io/llm-observability-setting-up-langfuse-langsmith-helicone-phoenix/)
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Arize Phoenix docs](https://docs.arize.com/phoenix)
- [Helicone docs](https://docs.helicone.ai/)
