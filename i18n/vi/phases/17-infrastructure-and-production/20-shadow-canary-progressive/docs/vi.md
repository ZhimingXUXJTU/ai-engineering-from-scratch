# Truyền thông bóng tối, Canary Rollout, và triển khai tiến bộ cho LLM

> Các triển khai LLM kết hợp các phần khó khăn nhất của việc triển khai phần mềm: không thử nghiệm đơn vị, chế độ thất bại pha trộn, tín hiệu chậm. Dòng là (1) chế độ bóng  yêu cầu lặp lại cho mô hình ứng viên, đăng ký, so sánh với không tác động người dùng; bắt được các vấn đề phân phối rõ ràng nhưng không phải là một đảm bảo chất lượng; (2) triển khai canary  chuyển lưu lượng tiến bộ 10% → 25% → 50% → 75% → 100% với cổng tại mỗi bước; theo dõi phần trăm độ trễ, chi phí / yêu cầu, tỷ lệ sai lầm / từ chối, phân phối chiều dài đầu ra, tỷ lệ phản hồi người dùng; (3) thử nghiệm A / B cho các lựa chọn khác nhau sau khi ổn định được xác nhận. Không xác định là không thể giảm  lên đến 15% sự khác biệt chính xác trên các chạy với đầu vào giống nhau do GPU FP không liên quan cộng với sự khác biệt kích thước lô. Chi phí là một biến, không phải là liên tục  mô hình tốt hơn 20% có thể đắt hơn 3 lần mỗi cuộc gọi. Tốc độ quay trở lại là quyết định: nếu quay trở lại đòi hỏi phải tái triển khai, bạn quá chậm. Chính sách sống trong cấu hình/ cờ; mô hình sống trong registry với các bản ghi đấm; rollback = chính sách đảo ngược + ngưỡng đảo ngược + pin mô hình cũ trong vài giây.

> **【中文解读】**Chương trình này giới thiệu về các chiến lược triển khai của Shadow / Kim丝雀 / 渐进式部署LLM 服务安全上线


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy canary-progression simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing)

>  **【前置】**学本节前请先掌握:Phase 17·13(可观测性) 、Phase 17·21(A/B 测试) ⋅LLM 上线 = 软件部署最难的组合:无单元测试、失败模式分散、信号延迟──
>  **【类比】**LLM 部署三步 = "飞机首飞流程"。 Shadow = 地面模拟(复制 prod 请求,零用户影响,对比但不换);Canary = 真飞但逐步开载客(10%→25%→50%→50%→100%, mỗi步有门禁);A/B = 商业航班对比(稳定测不同方案)。关键后: không chắc chắn不可消除(GPU 浮点+batch 差异致 15% 准确率波动);成本是变量(好20%的模型可能贵3倍);秒回滚速度决定性(级旗 换不能重新部署)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Hóa độ bóng (sự so sánh không tác động), canary (sự so sánh giao thông trực tiếp tiến bộ) và A/B (sự so sánh được xác nhận ổn định).
  Trung ngữ翻译:区分影子模式 (区分影子模式) 零影响比较) 金丝雀 (金丝雀) 真实流量渐进 (真流量渐进) 及 A/B (统计比较) ⋅
- Đặt ra danh sách năm chỉ số canary cụ thể của LLM (trễ, chi phí/ yêu cầu, lỗi/thiếu nại, phân phối chiều dài đầu ra, phản hồi của người dùng).
  Trung ngữ翻译:列举五个 LLM 特定金丝雀指标(延迟、成本/请求、错误/拒绝、输出长度分布、语义质量样本)
- Giải thích lý do tại sao việc không quyết định LLM (tối đa 15%) thay đổi ý nghĩa "thường ổn định" trong một triển khai.
  Trung ngữ翻译:解释为什么 LLM không xác định (高达15%) đã thay đổi ý nghĩa của "稳定" trong giới thiệu.
- Thiết kế một con đường quay trở lại mất vài giây (phác thảo chính sách) chứ không phải vài giờ (phân bố lại).
  Trung ngữ翻译:设计一个秒级回滚路径 (设计一个秒级回滚路径),而非小时级 (设计一个秒级回滚路),而不是小时级 (设计一个秒级回滚路),而不是小时级 (设计一个秒级重新部署)

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**LLM 部署 kết hợp các phần khó khăn nhất trong software deployment: không đơn vị thử nghiệm 模糊的失败模式、延迟的信号。 chuỗi chính xác là:(1) 影子模式将生产请求复制到候选模型,日志对比,零用户影响;(2) 金丝雀发布10%→25%→50%→75%→100% 渐进流量切换,每个阶段有门控标;(3) A/B 测试稳定性确认后的比比比比;;回滚速度是决定性的策略标志翻转(30秒)vs 重部署(3 小时)

> **【拓展：LLM 非确定性与部署】**Sự không chắc chắn của LLM là không thể tránh được cùng một đầu vào trên cùng một mô hình có thể tạo ra sự khác biệt tỷ lệ chính xác lên đến 15% trên cùng một mô hình.

Bạn gửi một mô hình mới. đánh giá ngoại tuyến cho thấy tăng độ chính xác 3% bạn biến nó vào trong sản xuất trong vòng 24 giờ, chi phí tăng 40%, người dùng ngón tay xuống tăng 8%, ba vé khách hàng báo cáo "câu trả lời kỳ lạ". Bạn quay lại. tái triển khai mất 3 giờ. cuối tuần của bạn bị phá hủy.

Mỗi phần của điều đó có thể tránh được. chế độ bóng sẽ bắt được 40% tăng giá trước khi bất kỳ người dùng nào thấy nó. Canary sẽ dừng ở 10% khi ngón tay xuống di chuyển. Phục hồi cờ chính sách sẽ mất 30 giây. Phân khúc là điều gì điền vào khoảng cách giữa "đánh giá ngoại tuyến trông tốt" và "người dùng thực sự hạnh phúc".

## Khái niệm cốt lõi

### Chế độ bóng

> **【中文解读】**影子模式候选模型接收与生产相同的请求,输出仅记录不回归用户――日志内容包括:输出内容(与生产不同) 、代号数量(成本差异)、延迟、拒绝和错误――能捕获:成本爆炸、长度退化、明显拒变、硬错误――不能捕获:用户会感知质量差异影子是烟雾测试,不是质量测试――

Người ứng cử nhận được cùng các yêu cầu như sản xuất; đầu ra được ghi lại, không được trả lại cho người dùng. Không tác động của người dùng.

- Nội dung sản lượng (các biệt so với sản xuất).
- Số lượng token (cost delta).
- - Trễ.
- Sự từ chối và sai lầm.

Các lần bắt: tăng chi phí, giảm chiều dài, thay đổi từ chối rõ ràng, sai lầm khó khăn. Không bắt: người dùng delta chất lượng sẽ nhận ra. bóng là một bài kiểm tra khói, không phải là một bài kiểm tra chất lượng.

### Việc triển khai Canary

> **【拓展：LLM 金丝雀发布的五个门控指标】**LLM 金丝雀 phát hành phải giám sát được 5 chỉ số kiểm soát:(1) 延迟百分位(P50/P95/P99) Canary P99 > 1.5x 基线则触发;(2) Mỗi yêu cầu chi phí>20% 高于基线则触发;(3) 错误/拒绝率2x 基线则触发;(4) 输出长度分布均值 + P99 分布偏移值则触发;(5) 用户反率指 down/工单 1.5x 基线则触发;;典型进度 1%→10%→25%→50%→50%→75%→100%, mỗi giai đoạn tích lũy đủ 5-15 分钟 分样检查间隔)

Sự chuyển đổi giao thông tiến bộ với các cửa. Tiêu chuẩn tiến bộ: 1% → 10% → 25% → 50% → 75% → 100%.

1. **Latency percentiles** P50, P95, P99. Vi phạm: con cá voi có P99 > 1,5x điểm cơ sở.
2. **Cost per request** hỗn hợp. Vi phạm: > 20% trên đường cơ sở.
3. **Error / refusal rate**5xx cộng với việc từ chối rõ ràng.
4. **Output length distribution** trung bình + P99. Vi phạm: chuyển đổi phân phối.
5. **User-feedback rate** Thumbs down / ticket fileings. Vi phạm: 1,5x đường cơ bản.

### Không quyết định là sự khác biệt mới

Các đầu vào giống nhau tạo ra các đầu ra không giống nhau.

- Không liên quan đến GPU FP (sự sắp xếp giảm điểm nổi khác nhau theo lô).
- Sự khác biệt kích thước lô (những lần cùng nhau trong lô 128 so với lô 16).
- Tiêu chuẩn:

Đường: biến số chính xác lên đến 15% chạy-to-run trên các bộ đánh giá giống nhau. "Thường" trong một bản triển khai có nghĩa là các métrics nằm trong sự khác biệt dự kiến, không giống với đường cơ sở. Đặt cửa trên sàn tiếng ồn.

### Chi phí là một biến

Một mô hình tốt hơn 20% có thể đắt hơn 3 lần mỗi cuộc gọi. Chi phí / yêu cầu là một trong năm cổng. Việc vận chuyển một mô hình "bất kỳ" phá vỡ nền kinh tế đơn vị là một trường hợp trở lại.

### Rollback là vũ khí.

- Lập khẩu chính sách (chương trình cờ tính năng): tỷ lệ đảo ngược trong cấu hình; mất vài giây.
- Model pinning (registry digest): mô hình pin không tự động nâng cấp.
- Rollback = đảo ngược cờ + đặt bản ghi đính vào trước.

Nếu đống của bạn cần phải tái triển khai để quay trở lại, sửa chữa trước khi quay.

### Thiết bị công cụ

> **【拓展：LLM 渐进式部署工具链】**Ứng dụng lựa chọn: 1) Argo Rollouts / FlaggerKubernetes 原生渐进式部署控制器,与 Istio/Linkerd 加权路由集成; 2) Istio cân nhắc định tuyến服务网格级流量切分; 3) KServe / Seldon Core模型服务自带卡纳里功能; 4) Feature flagsLaunchDarkly、Flagsmith、Unleash,策略级翻转无需重新部署;; 回滚基础设施:策略标志标志功能系统)翻转百分比在配置中秒级) 模型注册摘要固定pinged digest 不自动升级)  Nếu bạn cần một堆重新部署回滚, 上线再复.

**Argo Rollouts**- **Flagger** Kubernetes bộ điều khiển giao hàng tiến bộ.

**Istio weighted routing** phân chia giao thông cấp độ dịch vụ- lưới.

**KServe / Seldon Core** mô hình phục vụ với canary tích hợp.

**Feature flags** LaunchDarkly, Flagsmith, Unleash.

### Tỷ lệ thời gian

Canary gate kiểm tra mỗi 5-15 phút tùy thuộc vào khối lượng lưu lượng. 1% lưu lượng với 10 req / min cung cấp 50-150 điểm dữ liệu mỗi cửa sổ  đủ cho độ trễ nhưng ồn ào cho phản hồi của người dùng. 10% cung cấp ~ 10x nhiều hơn.

### Bước A/B là tùy chọn

Nếu mô hình mới khác biệt rõ ràng (hành vi khác nhau, đường cong chi phí khác nhau, âm thanh khác nhau), A / B kiểm tra nó ở 50% sau khi canary vượt qua.

### Những con số mà bạn nên nhớ

- Tăng tiến của loài cá: 1% → 10% → 25% → 50% → 75% → 100%.
- Tối thượng không xác định: lên đến 15% sự khác biệt chạy đến chạy trên các đầu vào giống nhau.
- Năm métrics canary: độ trễ, chi phí, lỗi/thiếu nại, thời gian đầu ra, phản hồi của người dùng.
- Cổng chi phí: > 20% trên đường cơ sở là vi phạm.
- Lần quay lại: giây, không phải giờ.

## Hãy sử dụng nó để thực hiện
```figure
i4-canary-ramp
```

## Sử dụng nó

`code/main.py`mô phỏng một canary rollout với sự lùi hốc. báo cáo các giai đoạn rollout dừng lại tại và cổng nào kích hoạt.

> `code/main.py`mô phỏng một canary rollout với sự lùi hốc. báo cáo các giai đoạn rollout dừng lại tại và cổng nào kích hoạt.

> `code/main.py`mô phỏng một canary rollout với sự lùi hốc. báo cáo các giai đoạn rollout dừng lại tại và cổng nào kích hoạt.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-rollout-runbook.md`. Với mô hình ứng cử viên, đường cơ sở và dung nạp rủi ro, thiết kế kế shadow→canary→100% kế hoạch.

> 本课产 出 `outputs/skill-rollout-runbook.md`. Với mô hình ứng cử viên, đường cơ sở và dung nạp rủi ro, thiết kế kế shadow→canary→100% kế hoạch.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đưa lại 25% chi phí.
   Trung ngữ翻译:运行 `code/main.py` Đưa 25% thành phần trở lại                                                                                                                                                                                                                                                           
2. Mô hình mới của bạn có mức độ chính xác tăng 3% ngoài khơi nhưng chi phí / yêu cầu là +18%.
   Trung ngữ翻译:Your new model离线精度提升3% nhưng成本/请求+18%──值得上线吗?
3. Thiết kế một lần quay lại trong vòng 60 giây.
   Trung文翻译:设计端到端 60秒内回滚──列出所需基础设施──
4. Không xác định nghĩa cho thấy ±7% trong đánh giá của bạn.
   Trung文翻译:非确定性显示 +/-7%──设金丝雀门控以避免误报──
5. Chế độ bóng sẽ tăng giá 40% trước canary.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Shadow mode | "duplicate to new" | Zero-impact send-to-candidate for logging |
| Canary | "progressive traffic" | Gradual user-exposed rollout with gates |
| Gates | "rollout checks" | Metric thresholds that block progression |
| Non-determinism | "LLM variance" | Irreducible run-to-run differences |
| Policy flag | "flag flip rollback" | Config-level rollback, seconds not hours |
| Model pin | "registry digest" | Immutable reference to a model version |
| Argo Rollouts | "K8s progressive" | Kubernetes-native canary/rollback controller |
| KServe | "inference K8s" | Model serving with canary primitives |
| Istio weighted | "mesh split" | Service-mesh traffic splitter |

## Xem thêm 延伸阅读

- [TianPan — Releasing AI Features Without Breaking Production](https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing)
- [MarkTechPost — Safely Deploying ML Models](https://www.marktechpost.com/2026/03/21/safely-deploying-ml-models-to-production-four-controlled-strategies-a-b-canary-interleaved-shadow-testing/)
- [APXML — Advanced LLM Deployment Patterns](https://apxml.com/courses/mlops-for-large-models-llmops/chapter-4-llm-deployment-serving-optimization/advanced-llm-deployment-patterns)
- [Argo Rollouts docs](https://argo-rollouts.readthedocs.io/)
- [Flagger docs](https://docs.flagger.app/)
