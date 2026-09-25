# SRE cho AI  Đáp ứng nhiều nhân viên, sổ chạy, phát hiện dự đoán 

> AI SRE sử dụng LLM dựa trên dữ liệu cơ sở hạ tầng (logbock, runbook, topology dịch vụ) thông qua RAG để tự động hóa các giai đoạn điều tra, tài liệu và phối hợp. Mô hình kiến trúc năm 2026 là tổ chức đa đại lý  các đại lý chuyên môn (logbo, métrics, runbook) được phối hợp bởi một giám sát viên; AI đề xuất giả thuyết và câu hỏi, con người chấp thuận các cuộc gọi phán xét. Datadog Bits AI và Azure SRE Agent vận chuyển này như các sản phẩm được quản lý. Các sổ chạy đang phát triển: NeuBird Hawkeye sử dụng đánh giá đối kháng ( hai mô hình phân tích cùng một sự cố; sự đồng thuận = sự tin tưởng, bất đồng = không chắc chắn); trí nhớ hoạt động tồn tại trong các thay đổi nhóm. Tự trị tự động vẫn thận trọng: AI đề nghị, con người chấp thuận. Hành động tự trị hoàn toàn là hẹp (tái khởi động pod, rollback cụ thể triển khai) với các rào chắn chặt chẽ  bất cứ ai bán "đặt nó và quên nó" là bán quá mức. Biên giới mới nổi: dự đoán trước sự cố. Nghiên cứu của MIT báo cáo một LLM được đào tạo về các nhật ký lịch sử + thời gian GPU + mô hình lỗi API dự đoán 89% các vụ gián đoạn 10-15 phút sớm hơn. Dự báo: 95% LLM doanh nghiệp đã tự động chuyển giao thất bại vào cuối năm 2026.

> **【中文解读】**Bài viết này giới thiệu về phương pháp kỹ thuật SRE của AI  thực tế LLM  dịch vụ của các điểm đáng tin cậy.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy multi-agent incident triage simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 24 (Chaos Engineering) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 24 (Chaos Engineering)

>  **【前置】**学本节前请先掌握:Phase 17·13(可观测性) 、Phase 17·24(混沌工程) 、SRE 基础(runbook/incident 响应) 。AI SRE = LLM 加持的故障响应。
>  **【类比】**AI SRE = "AI 急诊医生"。多 Agent 编排:日志 Agent+指标 Agent+runbook Agent 协调;AI 提假设+查日志,人类批准判断。Datadog Bits AI、Azure SRE Agent 是托管产品。NeuBird Hawkeye 用对抗评估(两模型和分析事件,一致=高置信)。自动修复保持谨慎:AI 建议+人批准。前沿:预故障预测(MIT 用历史日志+GPU 温度+API 错误模式预测 89% 故障 10-15 分钟)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Chụp đồ họa kiến trúc AI SRE đa đại lý: giám sát viên + đại lý chuyên ngành (logbo, métrics, runbook) + cổng chấp thuận con người.
  Trung文翻译:绘制多 Agent AI SRE 架构:主管 + 专业 Agent(日志、指标、运行手册)
- Giải thích lý do tại sao tự khắc phục lại lại lại là hẹp (tái khởi động, tái triển khai) thay vì rộng (công vụ tái thiết).
  Trung ngữ翻译: giải thích tại sao tự động sửa chữa là phạm vi hạn chế của(重启 Pod、回滚部署) thay vì phạm vi rộng của(重新架构)。
- Hãy nêu tên mô hình đánh giá đối kháng (NeuBird Hawkeye): hai mô hình đồng ý = sự tin tưởng; không đồng ý = leo thang.
  Trung文翻译:说出对抗性评估模式 (NewBird Hawkeye): hai mô hình nhất định = 置信度;不一致 = 升级到人类).
- Hãy trích dẫn kết quả phát hiện sớm 89% của MIT và hạn chế hoạt động: dự đoán không kích hoạt chỉ là bảng điều khiển.
  Trung ngữ翻译:引用 MIT 89% 早期检测结果和运维约束:无历史基线的预测不可行──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**AI SRE's Core Insights:2026: 20 phút trước cuộc điều tra sự kiện được tự động hóa  theo dịch vụ phân组日志、关联 đến gần đây triển khai、匹配 runbook đều là RAG + 工具使用。 giám sát được thực hiện trước khi người ta mở Datadog 完成首轮分类并呈现假设── hoàn toàn tự lập sửa chữa là các vấn đề khác nhau重启 Pod 安全扩展 GPU 池安全──如果策略允许)  tái cấu trúc dịch vụ tuyệt đối không đi.

> **【拓展：AI SRE 产品市场】**2026 năm AI SRE  sản phẩm:(1) Datadog Bits AIDatadog 内部托管 SRE copilot;(2) Azure SRE AgentAzure 原生;(3) NeuBird Hawkeye对抗性评估(两个模型独立分析同一事件,一致=高置信,不一致=升级) + 操作记忆(post-mortem 存入向量 DB);(4) PagerDuty AIOps分类 + 去重;5)(Incident.io Autopilot事件指挥官 + 协调。MIT 2025 Nghiên cứu cho thấy, GPULLM trong lịch sử 志 + 温度 + API 错误模式训练,可在 10-15 分钟 分前预测 89% của停机.

Một kỹ sư đang gọi được gọi vào 3 giờ sáng "Tỷ lệ lỗi cao trong thanh toán". Họ kiểm tra Datadog, Loki, ba sổ chạy, nhật ký triển khai. 30 phút sau họ nhận ra nguyên nhân gốc là một vLLM OOM từ một ổ đĩa cache KV. Họ khởi động lại pod; lỗi xóa.

Năm 2026, 20 phút đầu tiên của cuộc điều tra đó có thể tự động hóa. Nhóm nhật ký theo dịch vụ, tương quan với các triển khai gần đây, phù hợp với các sổ chạy  tất cả là RAG + sử dụng công cụ. Một đại lý được giám sát có thể thực hiện phân loại lần đầu tiên và trình bày một giả thuyết trước khi con người mở Datadog.

Phong trào tự trị hoàn toàn là một vấn đề khác. Khởi động lại: an toàn. Scale GPU pool: an toàn nếu chính sách cho phép. tái thiết kế dịch vụ: hoàn toàn không. Phân lý đang vẽ đường hẹp.

## Khái niệm cốt lõi

### Kiến trúc đa đại lý

> **【中文解读】**Nhiều Agent AI SRE  cấu trúc:Sản lý sẽ phân chia các sự kiện thành truy vấn, phân bổ cho chuyên nghiệp Agent 日志 Agent 搜索日志、 chỉ định Agent 查询 PromQL、Runbook Agent 检索文档) Sản lý 综合,向人类呈现假设 + 证据──人类批准或重定向──安全自动修复范围:重启 Pod、回滚特定部署、在预批准范围内扩展池──不安全范围:更改服务拓、更改资源限制、部署新代码、更改 IAM──

```
          Incident
             │
             ▼
        Supervisor
        /    |    \
       ▼     ▼     ▼
  Log agent  Metric agent  Runbook agent
       │     │     │
       └─────┴─────┘
             │
             ▼
        Hypothesis + evidence
             │
             ▼
        Human approval
             │
             ▼
        Action (narrow set)
```

Giám sát viên chia vụ việc thành các câu hỏi phụ. Các đại lý chuyên môn có quyền truy cập công cụ (hướng dẫn tìm kiếm nhật ký, PromQL, tìm kiếm tài liệu). Giám sát viên tổng hợp, trình bày giả thuyết + bằng chứng cho con người. Con người chấp thuận hoặc chuyển hướng.

### Khu vực tự trị

> **【拓展：AI SRE 自动修复的安全边界】**AI SRE tự động sửa đổi biên giới an ninh chia sẻ: an toàn(đường hạn)  tái khởi động Pod、回滚特定部署、在预批准范围内扩展池、启用预批准功能旗──不安全(广范围) 更改服务拓、修改资源限制、部署新代码、更改 IAM、修改数据库── bất kỳ nhà cung cấp nào tuyên bố "đặt lập sau đã quên" đều có cam kết an toàn quá mức.

**Safe (narrow)**: khởi động lại pod, quay lại triển khai cụ thể, quy mô trong giới hạn được chấp thuận trước, cho phép cờ tính năng được chấp thuận trước.

**Not safe (broad)**: thay đổi topology dịch vụ, thay đổi giới hạn nguồn lực, triển khai mã mới, thay đổi IAM, thay đổi cơ sở dữ liệu.

Bất cứ ai bán "đặt nó và quên nó" là bán quá mức.

### Đánh giá đối lập (NeuBird Hawkeye)

Hai mô hình phân tích độc lập sự cố tương tự. Nếu họ đồng ý về nguyên nhân gốc rễ, sự tự tin cao. Nếu họ không đồng ý, leo thang lên con người với cả hai giả thuyết có thể nhìn thấy.

### Khoá sử dụng

Tiến đổi nhóm là việc giết chết im lặng của các lá kiến thức bộ lạc truyền thống của SRE. AI SRE lưu trữ sổ chạy + hậu tử vong trong một DB vector; các đại lý lấy lại trên mỗi sự cố mới. Khi các kỹ sư mới tham gia, AI có lịch sử đầy đủ.

### Dự đoán trước sự cố

Nghiên cứu MIT 2025: LLM được đào tạo về các nhật ký lịch sử, nhiệt độ GPU, mô hình lỗi API dự đoán 89% các sự cố xảy ra 10-15 phút trước khi chúng xảy ra trên bộ thử nghiệm.

Kiểm tra thực tế: dự đoán không có kích hoạt là bảng điều khiển. Câu hỏi hoạt động là "Khi chúng ta dự đoán, chúng ta làm gì?" Phòng thoát phòng ngừa? Pager? tự động quy mô? Câu trả lời là chính sách cụ thể.

### Sản phẩm vào năm 2026

- **Datadog Bits AI** quản lý SRE phi công bên trong Datadog.
- **Azure SRE Agent** Người gốc Azure.
- **NeuBird Hawkeye** đánh giá đối kháng + trí nhớ hoạt động.
- **PagerDuty AIOps** phân loại + giảm gấp đôi.
- **Incident.io Autopilot** chỉ huy vụ việc + phối hợp.

### Các sổ chạy như mã

> **【拓展：AI SRE 实施路径】** 1) 首先将非结构化跑本转换为结构化标记;;症状、假设、验证、行动; 2) 实现对抗性评估两个独立模型分析同一事件; 3) 建立操作记忆将 post-mortem + runbook 存入向量 DB; 4) 从"AI 建议人类批准"开始,不要直接跳到自主行动; 5) 预事件预测MIT 研究显示 10-15 分钟提前量,但"预测后做什么"策略定义(预排?告警?自动扩展?);;

Các runbook phát triển từ các trang Confluence đến các phiên bản đánh dấu xuống với các phần có cấu trúc (symptom, giả thuyết, xác minh, hành động).

### Những con số mà bạn nên nhớ

- Phát hiện sớm MIT: 89% các vụ gián đoạn, thời gian dẫn đầu 10-15 phút.
- Phân loại đa đại lý: giám sát viên + (logbo, métrics, runbook) + con người.
- Bộ tự động khắc phục an toàn: khởi động lại pod, tái triển khai, quy mô trong giới hạn.
- Đánh giá đối lập: hai mô hình độc lập; sự đồng thuận = sự tin tưởng.

## Hãy sử dụng nó để thực hiện
```figure
i4-incident-agents
```

## Sử dụng nó

`code/main.py`mô phỏng phân loại đa đại lý: đại lý đăng ký tìm thấy lỗi, đại lý métric tìm thấy CPU spike, runbook đại lý phù hợp với vấn đề được biết đến. giám sát viên xếp hạng giả thuyết.

> `code/main.py`mô phỏng phân loại đa đại lý: đại lý đăng ký tìm thấy lỗi, đại lý métric tìm thấy CPU spike, runbook đại lý phù hợp với vấn đề được biết đến. giám sát viên xếp hạng giả thuyết.

> `code/main.py`mô phỏng phân loại đa đại lý: đại lý đăng ký tìm thấy lỗi, đại lý métric tìm thấy CPU spike, runbook đại lý phù hợp với vấn đề được biết đến. giám sát viên xếp hạng giả thuyết.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-ai-sre-plan.md`Với số lượng vụ việc hiện tại, độ trưởng thành của nhóm, thiết kế một AI SRE.

> 本课产 出 `outputs/skill-ai-sre-plan.md`Với số lượng vụ việc hiện tại, độ trưởng thành của nhóm, thiết kế một AI SRE.

## Tập luyện bài tập

1. Đi chạy`code/main.py`Nếu các nhân viên ghi chép và đo không đồng ý thì làm sao người giám sát giải quyết?
   Trung ngữ翻译:运行 `code/main.py`Nếu ngày lịch và chỉ số đại lý không phù hợp thì làm sao?
2. Định nghĩa ba hành động tự khắc phục "an toàn" cho dịch vụ của bạn.
   Trung ngữ翻译:为你的服务定义三个"安全"的自动修复操作──为每个提供理由──
3. Viết một mẫu runbook có cấu trúc: các phần, các trường yêu cầu, lệnh xác minh.
   Trung文翻译:编写结构化运行手册模板:章节、必填字段、验证命令。
4. Hình ảnh phát hiện dự đoán phát hiện ở mức 12 phút dẫn đầu.
   Trung ngữ翻译:预测性检测在 12 分钟提前量触发.
5. Thảo luận liệu một nhóm 3 người nên áp dụng AI SRE vào năm 2026 hay chờ.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| AI SRE | "agent for on-call" | LLM-backed incident investigation + coordination |
| Supervisor agent | "the orchestrator" | Top-level agent breaking incidents into sub-queries |
| Specialized agent | "domain agent" | Sub-agent with tool access (logs, metrics, runbooks) |
| Auto-remediation | "AI fixes it" | Narrow pre-approved action; NOT broad re-architecture |
| Operational memory | "vector runbooks" | Post-mortems + runbooks in vector DB for RAG |
| Adversarial eval | "two-model check" | Independent analyses; agreement = confidence |
| NeuBird Hawkeye | "the adversarial one" | Product with adversarial-eval + memory pattern |
| Bits AI | "Datadog's SRE agent" | Datadog-managed AI SRE |
| Pre-incident prediction | "early detection" | 10-15 min lead time on outage prediction |

## Xem thêm 延伸阅读

- [incident.io — AI SRE Complete Guide 2026](https://incident.io/blog/what-is-ai-sre-complete-guide-2026)
- [InfoQ — Human-Centred AI for SRE](https://www.infoq.com/news/2026/01/opsworker-ai-sre/)
- [DZone — AI in SRE 2026](https://dzone.com/articles/ai-in-sre-whats-actually-coming-in-2026)
- [Datadog Bits AI](https://www.datadoghq.com/product/bits-ai/)
- [NeuBird Hawkeye](https://www.neubird.ai/)
- [awesome-ai-sre](https://github.com/agamm/awesome-ai-sre)
