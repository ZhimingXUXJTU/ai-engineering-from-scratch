# A2A  Các giao thức đại lý-đối với đại lý  A2A:

> Google công bố A2A vào tháng 4 năm 2025; vào tháng 4 năm 2026 thông số kỹ thuật sẽ đạt đến https://a2a-protocol.org/latest/specification/và hơn 150 tổ chức ủng hộ nó. A2A là sự bổ sung ngang cho MCP (Dạy học 13): nơi MCP là dọc (hương cụ ), A2A là ngang (hương cụ ). Nó xác định các thẻ đại lý (khám phá), các nhiệm vụ với các đồ tạo tác (léc văn, dữ liệu có cấu trúc, video), chu kỳ cuộc sống nhiệm vụ không minh bạch và auth. Các hệ thống sản xuất ngày càng kết hợp MCP với A2A. Google Cloud đã đưa hỗ trợ A2A vào Vertex AI Agent Builder trong năm 2025-2026.

> **【中文解读】**Google đã công bố A2A  giao ước vào tháng 4 năm 2025; đến tháng 4 năm 2026, quy định đã có 150+  tổ chức hỗ trợ. A2A là bổ sung cấp độ của MCP: MCP là thẳng đứng ((Agent và công cụ), A2A là điểm đối với điểm ((Agent và Agent) ⋅ định nghĩa thẻ đại lý ((trận ra) ⋅ mang theo sản phẩm nhiệm vụ ⋅ không minh bạch nhiệm vụ chu kỳ sống và chứng nhận⋅ hệ thống sản xuất ngày càng nhiều sẽ sử dụng MCP và A2A ⋅ đối phó.

> **【拓展：A2A → Google 的 Agent 协议】**A2A là một hiệp định tiêu chuẩn giao tiếp giữa các đại lý được Google dẫn đầu, với MCP của Anthropic (Mode Context Protocol) (MCP) (Mode Context Protocol) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (MCP) (M) (MCP) (MCP) (M) (MCP) (MCP) (M) (M) (M) (M) (MCP) (M) (M) (M) (M) (M) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (C) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D) (D

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `http.server`, `json`) | **语言:** Python (标准库, `http.server`, `json`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前请先掌握:Phase 13·15-20(MCP 协议套件) 、Phase 16·04(原语) ・・・A2A là mức độ bổ sung của MCP:MCP=Agent 调工具(垂直),A2A=Agent 找 Agent(横向) ・・・
>  **【类比】**MCP + A2A = "电话黄页 + 直接通话"──MCP = 工具目录(agent 找工具用);A2A = Agent 间通话协议(agent 找 agent 协作)──2026 生产系统标配:MCP(连工具) + A2A(连其他 Agent) + Agent Card(发现)──Google 主导,150+ 组织支持──

##                                                                                                                                                                                                                                                               

Bạn có thể phơi bày một điểm cuối HTTP, xác định một sơ đồ JSON tùy chỉnh, và hy vọng bên kia nói. Mỗi cặp đại lý trở thành một tích hợp tùy chỉnh.

> Bạn có thể phát hiện một HTTP 端点, xác định một mô hình JSON tùy chỉnh, và mong đợi một bên khác có thể hiểu nó.

Vấn đề tích hợp n vuông: với các đại lý N, bạn cần tích hợp tùy chỉnh N × 1) / 2. Với 10 đại lý, đó là 45 tích hợp. Với 100 đại lý, 4950. A2A phá vỡ điều này thành N đại lý thẻ, mỗi mô tả một đại lý.

> N 平方集成问题:N 个代理 需要 N×(N-1)/2 个定制集成──10 个代理 是 45 个集成──100 个代理 是 4950 个──A2A sẽ nén nó thành N 个代理卡片, mỗi mô tả một Agent──

A2A là giao thức cáp phổ biến cho cuộc gọi đó. phát hiện tiêu chuẩn, mô hình nhiệm vụ tiêu chuẩn, giao thông tiêu chuẩn, đồ tạo vật tiêu chuẩn. Giống như HTTP + REST nhưng cho các đại lý như công dân hạng nhất.

> A2A là một giao thức đường chung được sử dụng. Standard Discovery, Standard Task Model, Standard Transmission, Standard Work.

Các đại lý là địa chỉ, các điểm kết thúc mạng được phát hiện. Bạn không " nhập khẩu " một đại lý; bạn " gọi " nó. Điều này tách rời triển khai  đại lý chạy bất cứ nơi nào, bằng bất kỳ ngôn ngữ nào, sử dụng bất kỳ khung nào, miễn là nó nói A2A.

> 关键抽象:Agent là có thể tìm kiếm, có thể tìm thấy, các kết cục mạng. Bạn không "导入" Agent; bạn "调用" nó.

## Khái niệm cốt lõi

### Bốn yếu tố

> 4 yếu tố

**Agent Card.**Một tài liệu JSON tại `/.well-known/agent.json`mô tả đại lý: tên, kỹ năng, điểm cuối, các phương pháp hỗ trợ, yêu cầu của tác giả.

> **Agent 卡片。**位于 `/.well-known/agent.json`文档, description Agent:名称、技能、端点、支持的模态、认证要求──通过读取卡进行发现──

Công ước URL nổi tiếng phản ánh các tiêu chuẩn web (`/.well-known/`là con đường tương tự được sử dụng cho `robots.txt`Bất kỳ đại lý nào tương thích với A2A có thể được phát hiện bằng cách lấy URL đó. Không cần đăng ký, không cần môi giới, không cần thư mục trung tâm.

> 知名 URL 约定镜像 Web 标准(`/.well-known/``robots.txt`、ACME 挑战、OIDC 发现的相同路径) ∼ Bất kỳ A2A 兼容代理 nào cũng có thể thông qua việc truy cập URL 发现──不需要注册表、代理或中央目录──

**Task.**Một vật thể không đồng bộ, có trạng thái với chu kỳ sống:`submitted -> working -> completed / failed / canceled`Một khách hàng gửi một nhiệm vụ, thăm dò hoặc đăng ký cập nhật.

> **任务。**工作单元── có các đối tượng có trạng thái khác nhau trong chu kỳ đời sống:`submitted -> working -> completed / failed / canceled` khách hàng gửi nhiệm vụ, vòng hỏi hoặc đăng ký cập nhật.

**Artifact.**Các loại kết quả được tạo ra bởi một nhiệm vụ. văn bản, cấu trúc JSON, hình ảnh, video, âm thanh. Các đồ tạo được gõ nên các phương thức khác nhau là hạng nhất.

> **工件。**任务产生的结果类型──文本、结构化 JSON、图像、视频、音频──工件是有类型的,因此不同模态是平等公民──

**Opaque lifecycle.**A2A không quy định * làm thế nào * đại lý từ xa giải quyết nhiệm vụ. Khách hàng thấy chuyển đổi trạng thái và các hiện vật; thực hiện là miễn phí để sử dụng bất kỳ khung.

> **不透明生命周期。**A2A 不规定远程 Agent *如何* 解决任务──客户端看状态转换和工件;实现可以自由使用任何框架──

Sự không rõ ràng này là do thiết kế. Một đại lý từ xa được xây dựng trên LangGraph, CrewAI hoặc một kịch bản Python tùy chỉnh đều trông giống như khách hàng A2A. Sự tương tác đến từ sự đồng ý về định dạng dây, chứ không phải nội bộ.

> Sự không minh bạch này được thiết kế như vậy. Cơ quan từ xa xây dựng dựa trên LangGraph, CrewAI hoặc bản Python  kịch bản tự xác định trông giống nhau đối với A2A  khách hàng.

### Sự chia cắt MCP/A2A

- **MCP**(Dạy học 13): công cụ đại lý <->. Đại lý đọc / viết qua JSON-RPC đến một máy chủ công cụ.
  Trung ngữ翻译:**MCP**(Dạy học 13):Nhà <-> 工具──Nhà 通过 JSON-RPC 读写工具服务器──默认无状态──
- **A2A**Các bên đều là các đại lý với lý luận riêng của họ.
  Trung ngữ翻译:**A2A**:Công viên <-> Công viên. đối với các thỏa thuận khác; cả hai đều có Công viên tự đoán.

Các hệ thống sản xuất đa đại lý sử dụng cả hai. Một đồng nghiệp A2A gọi các công cụ MCP ở bên của nó.

> Các hệ thống này đều sử dụng A2A đối với các thiết bị khác trong đó sử dụng các công cụ MCP.

Một mô hình phổ biến: một "hội nghiên cứu" A2A tại công ty A gọi máy chủ công cụ tìm kiếm MCP nội bộ, sau đó trả lại kết quả của mình cho "hội phân tích" A2A tại công ty B. Việc giao tiếp qua các tổ chức là A2A; việc sử dụng công cụ nội bộ là MCP. Mỗi giao thức làm những gì nó tốt nhất.

> 常见模式: A2A " nghiên cứu đại lý " của công ty A trong cuộc điều tra MCP  tìm kiếm công cụ dịch vụ, sau đó sẽ tìm thấy trở lại cho A2A " phân tích đại lý " của công ty B.

Hoặc với streaming: SSE đăng ký `/tasks/{id}/events`để cập nhật.

> Hoặc sử dụng: SSE 订阅 `/tasks/{id}/events`获取推送更新──

### Tác giả

A2A hỗ trợ ba mô hình phổ biến:

> A2A 支持三种常见模式:

Ba mô hình bao gồm các phổ từ "Tôi tin vào nhà cung cấp danh tính của mình" (OAuth2 bearer) đến "Chúng tôi xác minh lẫn nhau" (mTLS) đến "Chúng tôi không tin vào bất kỳ bên thứ ba nào" (HMAC signing). Chọn một nhẹ nhất đáp ứng các yêu cầu bảo mật của bạn.

> 三种模式涵盖从"我信任我的身份提供商" (OAuth2 bearer) 到"我们互相验证彼此" (MTLS) 到"我们不信任任何第三方" (HMAC 签名) 的范围──选择满足你的安全要求最轻量级之一──

- **Bearer token** OAuth2 hoặc không minh bạch.
  Trung ngữ翻译:**Bearer token** OAuth2 或不透明令牌。
- **mTLS** TLS chung; các tổ chức chứng minh danh tính với nhau.
  Trung ngữ翻译:**mTLS** 双向 TLS; tổ chức chứng minh tình trạng lẫn nhau
- **Signed requests** HMAC trên tải trọng hữu ích.
  Trung ngữ翻译:**签名请求** đối với HMAC có hiệu lực

Người được công bố là người có thẻ đại lý, khách hàng phát hiện ra và tuân thủ.

> 认证在代理卡中声明; khách hàng phát hiện并遵守.

### 150 tổ chức hơn vào tháng 4 năm 2026

Việc chấp nhận doanh nghiệp đã thúc đẩy quy mô A2A. tiêu đề: A2A trở thành cách các hệ thống đại lý doanh nghiệp vượt qua ranh giới niềm tin. Google Cloud đã cung cấp hỗ trợ Vertex AI Agent Builder A2A; Microsoft Agent Framework hỗ trợ nó; hầu hết các khung chính (LangGraph, CrewAI, AutoGen) cung cấp A2A adapter.

> 企业采用推动A2A规模化――标题:A2A 成为企业代理 系统跨越信任边界的方式――Google Cloud 提供 Vertex AI Agent Builder A2A 支持;Microsoft Agent Framework 支持它;大多数主要框架(LangGraph、CrewAI、AutoGen)提供 A2A 适配器──

Lý do A2A giành được sự chấp nhận của doanh nghiệp khi FIPA-ACL thất bại: A2A là JSON-native, sử dụng cơ sở hạ tầng web hiện có (HTTP, SSE, OAuth), và không yêu cầu các ontologies chia sẻ.

> A2A trong doanh nghiệp áp dụng FIPA-ACL  Lý do thất bại: A2A là JSON gốc  Sử dụng hiện có cơ sở hạ tầng Web  HTTP  SSE  OAuth)  không cần chia sẻ本体── FIPA  Kế hoạch mở rộng là chết người; A2A 学到了教训──

### Khi A2A thắng

- **Cross-organization calls.**Trưởng công ty A gọi trưởng công ty B. Nếu không có A2A, mỗi cặp đều là hợp đồng được đặt theo yêu cầu.
  Trung ngữ翻译:**跨组织调用。** Công ty A 调用 công ty B  không có A2A, mỗi đối tác đều là hợp đồng
- **Heterogeneous frameworks.**Cảnh sát LangGraph gọi Cảnh sát CrewAI gọi Cảnh sát Python tùy chỉnh.
  Trung ngữ翻译:**异构框架。**LangGraph Agent 调用 CrewAI Agent 调用自定义 Python Agent。A2A 标准化。
- **Typed artifacts.**Kết quả video, cấu trúc JSON, âm thanh  tất cả là hạng nhất.
  Trung ngữ翻译:**类型化工件。**视频结果、结构化 JSON、音频都是一等公民──
- **Long-running tasks.**Chuyển hình đời sống không rõ ràng + thăm dò làm cho các nhiệm vụ kéo dài hàng giờ trở nên đơn giản hơn.
  Trung ngữ翻译:**长时间运行的任务。**Chu kỳ sống không rõ ràng + 轮询 làm cho nhiệm vụ cấp nhỏ trở nên đơn giản.

### Khi A2A đấu tranh

- **Latency-sensitive micro-calls.**Chuyện sống của A2A là không đồng bộ. Sub-millisecond đại lý-to- đại lý không phù hợp; sử dụng trực tiếp RPC.
  Trung ngữ翻译:**延迟敏感的微调用。**Chu kỳ đời của A2A là khác nhau.
- **Tight-coupled in-process agents.**Nếu cả hai đại lý chạy trong cùng một quy trình Python, A2A HTTP round-trip là quá chết người.
  Trung ngữ翻译:**紧耦合的进程内 Agent。**Nếu hai đại lý chạy trong cùng một quá trình Python, A2A HTTP quay trở lại là quá thiết kế.
- **Small teams.**Chi phí chung của các thông số là thực tế; các đại lý chỉ nội bộ có thể không cần các thủ tục.
  Trung ngữ翻译:**小团队。**Quy tắc bán hàng là thực tế; Chỉ có bên trong đại lý có thể không cần sự chính thức này.

### A2A vs ACP, ANP, NLIP

Một số thông số kỹ thuật liên quan xuất hiện trong năm 2024-2026:

> Trong giai đoạn 2024-2026, một số quy định liên quan đã xuất hiện:

- **ACP**(IBM/Linux Foundation)  tiền nhiệm của A2A, phạm vi hạn chế hơn.
  Trung ngữ翻译:**ACP**(IBM/Linux Foundation)  A2A's前身,范围更狭──
- **ANP**(Nhiệm vụ mạng lưới đại lý)  phát hiện đồng nghiệp-sự nặng nề, phân cấp-lần đầu tiên.
  Trung ngữ翻译:**ANP**(Nhiệm vụ mạng lưới đại lý)  重对等发现,去中心化优先
- **NLIP**(Ecma Natural Language Interaction Protocol, tiêu chuẩn hóa tháng 12 năm 2025)  loại nội dung ngôn ngữ tự nhiên.
  Trung ngữ翻译:**NLIP**(Ecma 自然语言交互协议,2025 年 12 月标准化)

A2A là giao thức tương tác được áp dụng nhiều nhất vào tháng 4 năm 2026. Để xem so sánh, xem arXiv:2505.02279 (Liu et al., "Một cuộc khảo sát về giao thức tương tác của các đại lý").

> 截至 2026 年 4 月, A2A là hợp đồng đối tác rộng rãi nhất được áp dụng.

Vị cảnh giao thức 2026 đã ổn định: A2A cho sự hợp tác của các đại lý, MCP cho các công cụ, ACP được hấp thụ vào A2A cho việc ghi chép quỹ đạo, ANP cho danh tính qua các tổ chức. NLIP vẫn là một điểm mấu chốt.

> 2026 năm khuôn khổ thỏa thuận đã ổn định: A2A dùng cho đại lý 协作, MCP dùng cho công cụ, ACP 吸收 A2A dùng cho轨迹日志, ANP dùng cho跨组织身份──NLIP 仍然小众──新提案需要展示真实差距才能获得关注──

## Hãy xây dựng nó.
```figure
sw-agent-card-discovery
```

## Hãy xây dựng nó

`code/main.py`thực hiện một máy chủ và client A2A tối thiểu sử dụng `http.server`và JSON.

> `code/main.py`Sử dụng `http.server`和 JSON 实现 A2A 最小服务器和客户端──服务器:

- - Tự động`/.well-known/agent.json`- Tôi không biết.
  中文翻译:暴露 `/.well-known/agent.json`- Tôi không biết.
- chấp nhận `POST /tasks`- Tôi không biết.
  中文翻译: chấp nhận `POST /tasks`- Tôi không biết.
- quản lý trạng thái nhiệm vụ,
  Trung文翻译: quản lý nhiệm vụ trạng thái,
- trả lại các hiện vật trên `GET /tasks/{id}`- Tôi không biết.
  Trung ngữ翻译:在 `GET /tasks/{id}`Ưu trắc trở lại công việc.

Khách hàng:

> 客户端:

- lấy thẻ đại lý,
  Trung văn翻译:获取 Agent 卡片,
- gửi một nhiệm vụ,
  Trung文翻译:提交任务,
- thăm dò cho đến khi hoàn thành,
  Trung ngữ翻译:轮询直到完成,
- đọc được vật cổ.
  Trung ngữ翻译:读取工件。

Các kịch bản bắt đầu máy chủ trong một chuỗi nền, sau đó chạy khách hàng chống lại nó. Bạn thấy toàn bộ dòng chảy: khám phá, gửi, thăm dò, tạo vật.

> 脚本在后台线程中启动服务器,然后运行客户端──你看完整流程:发现、提交、轮询、工件──

## Hãy sử dụng nó để thực hiện

`outputs/skill-a2a-integrator.md`thiết kế một sự tích hợp A2A: nội dung thẻ đại lý, các kế hoạch nhiệm vụ, lựa chọn tác giả, phát trực tuyến và thăm dò.

> `outputs/skill-a2a-integrator.md`设计 A2A 集成:Công viên 卡片内容、任务模式、认证选择、流式 vs 轮询──

## Chuyển nó đi.

Danh sách kiểm tra:

> 检查清单:

- **Pin the spec version.**A2A vẫn đang phát triển, thẻ đại lý nên tuyên bố phiên bản giao thức.
  Trung ngữ翻译:**固定规范版本。**A2A  vẫn đang phát triển;Agent 卡片应声明协议版本.
- **Idempotent task creation.**Các bài đăng trùng lặp (các thử mạng) nên tạo ra một nhiệm vụ.
  Trung ngữ翻译:**幂等任务创建。**重复提交 (网络重试) 应产生一个任务――
- **Artifact schemas.**Cố định hình dạng mà đại lý trả về; người tiêu dùng nên xác nhận.
  Trung ngữ翻译:**工件模式。**声明 Trưởng  trả lại 形状;消费者应验证。
- **Rate limits + auth.**A2A là đối mặt với công chúng; áp dụng an ninh web tiêu chuẩn.
  Trung ngữ翻译:**速率限制 + 认证。**A2A 面向公众; ứng dụng tiêu chuẩn Web 安全.
- **Dead-letter for failed tasks.**Kiểm tra các mẫu theo thời gian cho các loại lỗi tái phát.
  Trung ngữ翻译:**失败任务死信。**随时检查模式 để phát hiện các loại thất bại lặp lại xuất hiện.

## Tập luyện bài tập

1. Đi chạy`code/main.py`Hãy xác nhận khách hàng phát hiện ra máy chủ và nhận được vật liệu chính xác.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận khách hàng tìm thấy máy chủ không nhận được các công trình chính xác ❖
2. Thêm một kỹ năng thứ hai vào máy chủ (ví dụ: "summarize"). Cập nhật thẻ đại lý. Viết một khách hàng chọn kỹ năng dựa trên loại nhiệm vụ.
   Trung文翻译:向服务器添加第二个技能(如"summarize")。更新 Agent 卡片──编写根据任务类型选择技能的客户端──
3. Thực hiện một điểm cuối truyền SSE: `/tasks/{id}/events`Khách hàng cần làm gì khác?
   Trung文翻译:实现 SSE 流式端点:`/tasks/{id}/events`, phát hiện trạng thái thay đổi.
4. Đọc các thông số kỹ thuật A2A. Chọn ra ba điều mà các thông số kỹ thuật này không thực hiện.
   Trung ngữ翻译:阅读 A2A 规范――识别规范要求的三个此演示未实现的东西――
5. So sánh A2A (Agent Card discovery) với MCP (server-side capability listing via `listTools`(văn số 1 - 2) Sự khác biệt giữa các nhân viên tự mô tả và kiểm tra khả năng là gì?
   中文翻译:比较 A2A(Agent 卡片发现) với MCP(通过 `listTools`(Sự mô tả về người đại lý và khả năng tìm kiếm là gì?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| A2A | "Agent-to-agent" / "Agent 对 Agent" | Peer protocol for agents to call other agents across systems. Google 2025. / Agent 跨系统调用其他 Agent 的对等协议。Google 2025。 |
| Agent Card / Agent 卡片 | "The agent's business card" / "Agent 的名片" | JSON at `/.well-known/agent.json` describing skills, endpoints, auth. / 描述技能、端点、认证的 JSON。 |
| Task / 任务 | "The unit of work" / "工作单元" | Async stateful object with a lifecycle; artifacts produced on completion. / 具有生命周期的异步有状态对象；完成时产生工件。 |
| Artifact / 工件 | "The result" / "结果" | Typed output: text, structured JSON, image, video, audio. First-class media. / 类型化输出：文本、结构化 JSON、图像、视频、音频。一等媒体。 |
| Opaque lifecycle / 不透明生命周期 | "How it's solved is the agent's business" / "如何解决是 Agent 的事" | Client sees state transitions; server is free to choose framework/tools. / 客户端看到状态转换；服务器自由选择框架/工具。 |
| Discovery / 发现 | "Finding the agent" / "找到 Agent" | `GET /.well-known/agent.json` returns the card. / 返回卡片的 GET 请求。 |
| MCP vs A2A | "Tools vs peers" / "工具 vs 对等" | MCP: vertical agent <-> tool. A2A: horizontal agent <-> agent. / MCP：垂直 Agent <-> 工具。A2A：水平 Agent <-> Agent。 |
| ACP / ANP / NLIP | "Sibling protocols" / "兄弟协议" | Adjacent specs; A2A is the most-adopted 2026. / 相邻规范；A2A 是 2026 年采用最广泛的。 |

## Xem thêm 延伸阅读

- [A2A specification](https://a2a-protocol.org/latest/specification/) quy định quy định
  中文翻译:A2A 规范  权威规范
- [Google Developers Blog — A2A announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) Tháng 4 năm 2025
  中文翻译:Google 开发者博客  A2A 公告  2025 年 4 月发布文章
- [A2A GitHub repo](https://github.com/a2aproject/A2A) Các thực hiện và SDK tham chiếu
  中文翻译:A2A GitHub 仓库  参考实现和 SDK
- [Liu et al. — A Survey of Agent Interoperability Protocols](https://arxiv.org/html/2505.02279v1) MCP, ACP, A2A, ANP so sánh
  Trung文翻译:Liu 等人  Agent 互操作性协议综述  MCP、ACP、A2A、ANP 比较
