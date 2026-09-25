# FinOps cho LLM  Kinh tế đơn vị và phân bổ nhiều người thuê  FinOps của LLM  đơn vị kinh tế và đa thuê nhà

> FinOps truyền thống phá vỡ chi tiêu LLM. Chi phí là giao dịch mã thông báo, không phải thời gian sử dụng nguồn lực. Tags không lập bản đồ  một cuộc gọi API là một giao dịch, không phải là tài sản. Các quyết định kỹ thuật (phác thảo nhanh, cửa sổ ngữ cảnh, chiều dài đầu ra) là quyết định tài chính.`user_id`) cho giá ghế và mở rộng, mỗi nhiệm vụ (`task_id`+ `route`) cho chi phí bề mặt sản phẩm và ưu tiên, cho người thuê (`tenant_id`) về kinh tế đơn vị và tái tạo. Bốn lớp token  prompt, công cụ, bộ nhớ, phản ứng  một cái thùng ẩn chi tiêu. Đường thang thực thi cho các sản phẩm đa thuê nhân: giới hạn tỷ lệ cho mỗi thuê nhân (2-3x mức cao nhất dự kiến, vượt qua 429 + thử lại sau); giới hạn chi tiêu hàng ngày (1.5-3x mức trần hợp đồng; kích hoạt tăng tốc + cảnh báo); tắt các chuyển đổi khi chi tiêu điểm z > 4 (tự động tạm dừng + trang khi gọi). Các mô hình phân loại: Tag-and-aggregate, telemetry-joiner (trace-ID → thanh toán; độ chính xác cao nhất), lấy mẫu và kéo dài, phân bổ dựa trên mô hình, nguồn gốc sự kiện, phát trực tuyến thời gian thực. Đoạn số: chi phí cho mỗi truy vấn được giải quyết, chi phí cho mỗi vật tạo ra không phải mã thông báo $/M. Việc gắn thẻ ngược luôn bị bỏ qua; công cụ tạo theo yêu cầu.

> **【中文解读】**传统FinOps trong LLM 支出失效成本是代币交易而不是资源运行时间──工程决策──提示设计、上下文窗口、输出长度) 就是财务决策──2026年Playbook 建议在第一天建立三个归因维度:按用户"",按任务"",按租户──四个代币层──提示、工具、单位记忆、响应) không thể được kết hợp thành một桶──指标应为"每次解决查询成本"",而不是"每百万代币 成本"──

> **【拓展：FinOps → LLM 成本优化】**Trong ứng dụng LLM, kiểm soát chi phí là thách thức cốt lõi. VLLM + 定量化部署 có thể giảm chi phí suy luận, phương pháp mô hình.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cost-attribution simulator with kill switch) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 14 (Caching) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 14 (Caching)

>  **【前置】**学本节前请先掌握:Phase 17·13(可观测性) 、Phase 17·14(缓存) 、云 FinOps 基础。LLM FinOps = 传统 FinOps 失效后的新方法。
>  **【类比】**LLM FinOps = "按用收费的水电费"。传统 FinOps = 按服务器 uptime(标签=资产);LLM FinOps = 按代币交易(标签=交易)。三大归因维度(1 ngày nhất nhất nhất thiết phải埋):per-user(席位定价)、per-task(产品成本)、per-tenant(单位经济)。四层代币(quan/工具/memory/response) phải分桶合并一个桶会掩盖真实开销──
> ️ **【易错点】**单位指标使用 $/M token 是错的,应该使用"每次解决查询的成本"──强制阶梯:限流(2-3x 峰值)→日上限(1.5-3x 合约)→ Kill switch(z-score>4 自动暂停)──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Giải thích lý do tại sao FinOps truyền thống (tags + tiers) phá vỡ chi tiêu LLM và nêu tên ba chiều kích thuộc về mới.
  Trung ngữ翻译:解释为什么传统FinOps (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps) (traductional FinOps))
- Đặt ra danh sách bốn lớp token (quá trình, công cụ, bộ nhớ, phản ứng) và lý do tại sao việc thanh toán một thùng chứa chứa chi phí.
  Trung文翻译:列举四个标志层 (四个标志层) 提示、工具、记忆、响应),以及为什么单桶计费产生误导――
- Thiết kế một thang thực thi (số phí → giới hạn chi tiêu → chuyển đổi giết người) cho một sản phẩm đa thuê nhà.
  Trung文翻译:设计执行阶梯(速率 -> 支出上限 -> 断开关) dùng cho nhiều thuê户 LLM 服务。
- Chọn một số liệu đơn vị (chi phí cho mỗi truy vấn / đồ tạo được giải quyết) thay vì mã thông báo $ / M.
  Trung文翻译:选择单位指标 ((每次解决查询/产品成本) thay vì mã thông báo $/M。

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**传统FinOps trong LLM 支出失效的核心原因:LLM 成本是代币 交易而不是资源运行时间──标签(tags) không thể trực tiếp映射API 调用是交易而不是资产──工程决策(提示设计、上下文窗口、输出长度) là quyết định tài chính──账单显示40,000$, nhưng bạn không biết: thuê nhà đã chi tiêu bao nhiêu, sản phẩm nào, chức năng được thúc đẩy có hữu ích không, liệu nó nhanh chóng 膨胀还是工具调用还是记忆导致放大了──

Tài khoản của anh viết 40.000 đô la.
- Người thuê nhà nào đã chi tiền đó.
- Tính năng sản phẩm nào đã thúc đẩy nó.
- Nếu một người dùng cá nhân đã lạm dụng.
- Dù là bùng phát nhanh, gọi công cụ, hay tăng cường bộ nhớ là thủ phạm.

Tag-and-aggregate trên bên nhà cung cấp hoạt động cho các nguồn tài nguyên đám mây (EC2, S3) nơi thẻ lan rộng đến các mục dòng. LLM API gọi không tự động thẻ  bạn phải dán dấu người dùng / nhiệm vụ / thuê nhà tại trang web cuộc gọi và thực hiện. Thanh niên ứng ngược luôn bỏ lỡ các trường hợp cạnh.

## Khái niệm cốt lõi

### Ba chiều kích thuộc tính

**Per-user**(`user_id`): ai đang chi phí gì.

**Per-task**(`task_id`+ `route`): bề mặt sản phẩm nào chi phí bao nhiêu.

**Per-tenant**(`tenant_id`): khách hàng nào là lợi nhuận.

Trình chơi cả ba ở vị trí gọi vào ngày đầu tiên.

### Bốn lớp biểu tượng

| Layer | Example | Typical % of total |
|-------|---------|---------------------|
| Prompt | system + user input | 40-60% |
| Tool | tool-call results fed back | 20-40% (agent workloads) |
| Memory | prior conversation / retrieved docs | 10-30% |
| Response | model output | 10-30% |

Việc kết hợp tất cả bốn thứ này làm cho tối ưu hóa bị mù.

### Đường thang thực thi

> **【中文解读】**Nhiều thuê hàng có 3 cấp độ bắt buộc:(1)  tỷ lệ giới hạn mỗi thuê hàng 2-3x  dự kiến đỉnh giá trị, trở lại 429 + Retry- Sau đó, thuê hàng cảm thấy căng thẳng nhưng không có kế toán bất ngờ;(2) 日支出上限 mỗi thuê hàng 1.5-3x 合约上限,触发时收紧率限制 + 告警客户成功团队;(3) Kill switch当支出 z-score > 4(相对租户基线) 时自动暂停租户,通知班,升级运维和客户成功;;

> **【拓展：LLM FinOps 的复合优化栈】**Lớp 17·14)  khoảng 10x hơn hơn nhập khẩu;(2) 批处理(Phase 17·15) 50% giảm giá;(3) 路由到廉价模型(Phase 17·16) 60% giảm giá;(4) 网关效率(Phase 17·19) 冗余 + 重试――全叠加最优可降至朴素基线的约5-10%──大多数团队 chỉ bật 2-3 杆, rất ít có đội 叠加四个.

1. **Rate limit**mỗi người thuê nhà. 2-3 lần mức cao nhất dự kiến.`Retry-After`Người thuê nhà thấy sự chi phối, không có tiền bất ngờ.

2. **Daily spend cap**- Thích: giới hạn tốc độ củng cố + cảnh báo thành công của khách hàng.

3. **Kill switch**trên điểm chi tiêu z > 4 so với đường cơ sở của người thuê nhà. tự động tạm dừng người thuê nhà; trang trên cuộc gọi; leo thang đến các hoạt động + CS.

### Các mô hình phân bổ

- **Tag-and-aggregate**: tiêu đề metadata dấu; tổng hợp sau đó. đơn giản; thô.
- **Telemetry joiner**: kết nối dấu vết với thanh toán thông qua thẻ tín hiệu dấu vết độ chính xác cao nhất.
- **Sampling + extrapolation**: mẫu 5-10%, nhân. chi phí hiệu quả cho chi tiêu thô; bỏ qua đuôi.
- **Model-based allocation**: regression để suy luận driver chi phí. cho dữ liệu cũ mà không có thẻ.
- **Event-sourced**: chi phí như các sự kiện trong một dòng chảy (Kafka / Kinesis).
- **Real-time streaming**: bản cập nhật bảng điều khiển dưới giây.

### Chi phí cho mỗi X là đơn vị métric

> **【中文解读】**Các mã thông báo $/M là ngôn ngữ nhà cung cấp. Chỉ số sản phẩm nên là: 1) Mỗi giải pháp hỗ trợ công việc đơn phí; 2) Mỗi sản xuất văn bản chi phí; 3) Mỗi thành công Agent  nhiệm vụ chi phí; 4) Mỗi người dùng sẽ có thời gian chi phí.

$/M token là nhà cung cấp nói.

- Chi phí cho mỗi vé hỗ trợ được giải quyết.
- Chi phí cho mỗi sản phẩm được tạo ra.
- Chi phí cho mỗi nhiệm vụ của một đại lý thành công.
- Chi phí mỗi người dùng-phần-tháng phút.

Kết hợp chi phí với kết quả sản phẩm, nếu không tối ưu hóa không được hợp nhất.

### Hình dạng dấu vết của quy định chi phí

```
trace_id: abc123
  user_id: u_42
  tenant_id: t_7
  task_id: task_classify_doc
  route: model_haiku
  layers:
    prompt_tokens: 1800
    tool_tokens: 600
    memory_tokens: 400
    response_tokens: 150
  cost_usd: 0.0135
  cached_input: true
  batch: false
```

Tạo ra mỗi cuộc gọi. Cung cấp dữ liệu trong hồ dữ liệu. tổng hợp theo kích thước.

### Thống tiền tiết kiệm hợp chất

Stack: cache + batch + route + gateway.
- Cache L2 (Phase 17 · 14): ~ 10 lần đầu vào rẻ hơn.
- Nhóm (Phase 17 · 15): giảm 50%
- Đường đến mô hình rẻ (Phase 17 · 16): giảm chi phí 60%.
- Hiệu quả Gateway (Phase 17 · 19): redundancy + retries.

Các trường hợp tốt nhất được xếp chồng lên: ~ 5-10% so với đường cơ bản ngây thơ. Hầu hết các đội có 2-3 đòn bẩy tham gia; ít xếp chồng lên cả bốn.

### Những con số mà bạn nên nhớ

- Các kích thước phân bổ: cho mỗi người dùng, cho mỗi nhiệm vụ, cho mỗi người thuê nhà.
- Bốn lớp biểu tượng: prompt, tool, memory, response.
- Động cơ tắt: sử dụng điểm z > 4.
- Đơn vị đo: chi phí cho mỗi truy vấn được giải quyết, không phải mã thông báo $/M.
- Các tối ưu hóa xếp chồng lên: ~ 5-10% của đường cơ sở có thể.

## Hãy sử dụng nó để thực hiện
```figure
i4-spend-ladder
```

## Sử dụng nó

`code/main.py`mô phỏng một dịch vụ LLM đa thuê nhân với thang thực thi ba cấp. Nhổ vào một thuê nhân lạm dụng và chứng minh việc bắn tắt chuyển đổi.

> `code/main.py`mô phỏng một dịch vụ LLM đa thuê nhân với thang thực thi ba cấp. Nhổ vào một thuê nhân lạm dụng và chứng minh việc bắn tắt chuyển đổi.

> `code/main.py`mô phỏng một dịch vụ LLM đa thuê nhân với thang thực thi ba cấp. Nhổ vào một thuê nhân lạm dụng và chứng minh việc bắn tắt chuyển đổi.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-finops-plan.md`Với sản phẩm và quy mô, thiết kế các quy trình quy định và thang thực thi.

> 本课产 出 `outputs/skill-finops-plan.md`Với sản phẩm và quy mô, thiết kế các quy trình quy định và thang thực thi.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đường độ x của cái chuyển đổi bắn ở mức nào?
   Trung ngữ翻译:运行 `code/main.py`断开关在什么z-score 下触发? làm thế nào để ngăn chặn báo cáo sai?
2. Thiết kế bảng điều khiển chi phí cho mỗi người thuê, mỗi nhiệm vụ.
   Trung ngữ翻译: thiết kế theo thuê nhà, theo nhiệm vụ của bạn.
3. Người thuê nhà lớn nhất của bạn là đơn vị kinh tế tiêu cực.
   Trung ngữ翻译:你最大的租户单位经济学为负.
4. Xét chi phí cho mỗi vé được giải quyết cho một sản phẩm hỗ trợ: 3M token/ticket, ~800 vé/ngày, tỷ lệ lưu trữ GPT-5.
   Trung ngữ翻译:计算支持产品的每解决工单成本:3M token/工单,约2.5次重试――单位经济学可行吗?
5. Hãy tranh luận liệu việc gắn thẻ ngược lại có thể hoạt động được không.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Per-user attribution | "user-level cost" | `user_id` stamped on every call |
| Per-task attribution | "feature cost" | `task_id` + `route` identify product surface |
| Per-tenant attribution | "customer cost" | `tenant_id`; drives unit economics |
| Four token layers | "cost layers" | prompt + tool + memory + response |
| Rate limit | "429 guard" | Per-tenant ceiling enforced at gateway |
| Daily spend cap | "daily ceiling" | Tenant-scoped budget with alert |
| Kill switch | "auto-pause" | Spend z-score > 4 triggers auto-suspension |
| Cost per resolved | "product unit metric" | Cost tied to product outcome, not tokens |
| Telemetry joiner | "trace-to-billing" | Highest-accuracy attribution pattern |
| Stacked optimization | "cache+batch+route+gateway" | Compounding savings to ~5-10% baseline |

## Xem thêm 延伸阅读

- [FinOps Foundation — FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/)
- [FinOps School — Cost per Unit 2026 Guide](https://finopsschool.com/blog/cost-per-unit/)
- [Digital Applied — LLM Agent Cost Attribution 2026](https://www.digitalapplied.com/blog/llm-agent-cost-attribution-guide-production-2026)
- [PointFive — Managed LLMs in Azure OpenAI](https://www.pointfive.co/blog/finops-for-ai-economics-of-managed-llms-in-azure-open-ai)
