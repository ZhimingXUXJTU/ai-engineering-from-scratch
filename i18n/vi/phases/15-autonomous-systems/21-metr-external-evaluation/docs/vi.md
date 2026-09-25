# METR Thời gian và Cấp nhận năng lực bên ngoài  đánh giá ngoại bộ METR

> METR (ex-ARC Evals) là một tổ chức độc lập 501(c)(3) kể từ tháng 12 năm 2023. Điểm chuẩn Time Horizon 1.1 của họ (từ tháng 1 năm 2026) phù hợp với đường cong logistics để xác suất thành công nhiệm vụ so với log(xác nhân hoàn thành thời gian); giao thông ở 50% xác suất xác định chân trời thời gian của mô hình. Bộ tham gia 20252026 bao gồm GPT-5.1, GPT-5.1-Codex-Max và các đánh giá giám sát nguyên mẫu (có thể giám sát các nhiệm vụ bên cạnh bắt giữ; có thể tránh khỏi tác nhân). Các bộ chuẩn: HCAST (180+ ML, cyber, SWE, nhiệm vụ lý luận; 1 phút đến 8+ giờ), RE-Bench (71 ML nhiệm vụ nghiên cứu kỹ thuật với cơ sở chuyên gia), SWAA. Lưu ý trung thực: Các phép đo METR được lý tưởng hóa  không có con người, không có hậu quả thực sự  và nhóm đã ghi lại khoảng cách hành vi đánh giá so với triển khai (Dạy học 1). Một chân trời thời gian là một giới hạn trên, không phải là dự đoán triển khai.

> **【中文解读】**Bài viết này giới thiệu về việc đánh giá của bộ phận bên ngoài của METR  độc lập của bên thứ ba đối với khả năng và rủi ro của AI 


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, logistic-fit horizon estimator) | **语言:** Python（标准库，逻辑拟合时间线估计器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 19 (RSP) | **前置知识:** Phase 15 · 01（长程 Agent）、Phase 15 · 19（RSP）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Học本节前请先掌握:Phase 15·01(长程 Agent)、Phase 15·19-20(RSP 框架)、统计基础(逻辑回归)。METR = 独立第三方评估机构,把"AI R&D-4"等政策值变成可测量数字──
>  **【类比】**METR = "AI 能力的第三方检查中心"──RSP nói"AI R&D-4 值" là trừu tượng;METR's Time Horizon 基准把"AI 能完成多复杂任务"压缩成一个标量"模型 50% 可靠性能完成专家花 X 小时的任务"──类似于使用 IQ 分数概括智力,但METR's数字有可重复测量方法──
> ️ **【易错点】**Để đưa ra METR Time Horizon 当成部署预测 → 错──METR 测试是理想化的(无真人监督、无真实后果), thực tế部署时能力会打折──修复:Time Horizon 是上限不是下限,部署前必须在自己的真实任务上复测──

## Vấn đề  vấn đề giới thiệu

Các chính sách quy mô (Dạy 19, 20) chỉ hữu ích như các phép đo mà chúng tham khảo. "Thỉ số R&D-4 AI" và "Tự trị tầm xa" được định nghĩa trong văn bản chính sách; chúng chỉ có thể được thực hiện khi các đánh giá cụ thể tạo ra các con số cụ thể.

> 扩展政策 (第 19、20 课) chỉ được sử dụng như các phép đo mà chúng được trích dẫn. "AI R&D-4 值" và "长程自主" được định nghĩa trong văn bản chính sách; chúng chỉ được tạo ra một số lượng cụ thể khi đánh giá cụ thể.

METR là tổ chức đánh giá bên ngoài 20242026 đã xác định nhiều số đó. Họ đánh giá các mô hình biên giới  thường được phát hành trước, theo NDA với phòng thí nghiệm  và xuất bản phương pháp sau đó. Time Horizon 1.1 (từ tháng 1 năm 2026) là sản phẩm đầu tiên của họ: một bộ sạc đơn giản thu nhỏ khả năng thành một đơn vị có thể đọc được bởi con người ("chương trình này có thể thực hiện loại nhiệm vụ mà một chuyên gia dành X giờ để làm với độ tin cậy 50%").

> METR là 20242026  xác định nhiều số liệu này của tổ chức đánh giá bên ngoài. Họ đánh giá mô hình tiền tuyến thường được phát hành trước ̊ ký NDA sau khi đăng bài luận. Time Horizon 1.1 基准(1 tháng 1 năm 2026) là công cụ tiêu đề của họ: một mô hình sẽ được nén thành mô hình của nhân loại có thể đọc được.

Bài học phần nào là về phương pháp học (cách thức tính toán chân trời) và phần nào về giải thích (tại sao chân trời là ranh giới trên, chứ không phải dự đoán triển khai).

> Phần này về phương pháp học (How to calculate time line), phần về giải thích (Why time line is up-limit rather than deployment prediction)  Những kỹ năng này đi kèm.

## Khái niệm cốt lõi

### METR nền

- Được thành lập: Tháng 12 năm 2023 (trước đây là Evals, tách ra thành 501 ((c) ((3)).
  Trung文翻译:成立:2023 年 12 月(原 ARC Evals,分拆为独立 501(c)(3))
- phạm vi: đánh giá khả năng tự động của các mô hình biên giới, thường được phát hành trước.
  Trung ngữ翻译:范围:前沿模型自主能力评估, thường xuất bản trước.
- Các phòng thí nghiệm đối tác: Anthropic, OpenAI (các dự án 2025-2026).
  Trung文翻译:合作实验室:Anthropic、OpenAI(20252026 多次合作)。
- Các kết quả đáng chú ý: Time Horizon 1.0 (tháng 3 năm 2025), Time Horizon 1.1 (tháng 1 năm 2026), các đánh giá giám sát nguyên mẫu.
  Trung文翻译:显著产出:Time Horizon 1.0(2025 年 3 月) 、Time Horizon 1.1(2026 年 1 月) 、原型监控评估──

### Time Horizon phù hợp

Phương pháp (từ blog và bài báo của METR):

> 方法论(来自 METR 博客和论文):

1. Thu thập một bộ nhiệm vụ trải dài từ thời gian hoàn thành chuyên gia theo quy mô phút đến giờ.
   Trung ngữ翻译:收集覆盖分钟级到小时级专家完成时间的任务集──当前集:HCAST(180+任务)、RE-Bench(71 任务)、SWAA──
2. Thực hiện mô hình cho mỗi nhiệm vụ; ghi thành công hoặc thất bại.
   Trung ngữ翻译: 在每个任务上运行模型;记录成功或失败。
3. Đưa ra một đường cong hậu cần: P(sự thành công) như một hàm của log(người chuyên gia hoàn thành thời gian).
   Trung文翻译:拟合逻辑曲线:P(成功)作为 log(专家完成时间) 的函数──
4. Khía cảnh là thời gian chuyên môn khi P ((success) = 0,5.
   Trung ngữ翻译:时间线是 P(成功) = 0.5 时的专家时间──

Hình thức phù hợp với hậu cần là đúng vì khả năng thường có mối quan hệ tăng lên, tiếp cận cao nguyên với khó khăn nhiệm vụ. Điểm 50% là một sự lựa chọn (có thể là 10%, 90%); METR báo cáo nhiều ngưỡng trong bài báo chi tiết nhưng dẫn đầu với 50% vì nó là trực quan nhất.

> Hình thức phù hợp hợp hợp lý là đối với, vì khả năng và khó khăn nhiệm vụ thường là một cách đơn giản gia tăng, xu hướng về mối quan hệ trên nền tảng. 50% điểm là lựa chọn; METR báo cáo nhiều giá trị trong các bài báo chi tiết nhưng 50% chủ yếu vì nó trực tiếp nhất.

### Số tháng 1 năm 2026

Theo thời gian Horizon 1.1:

> 按 Time Horizon 1.1:

- Claude Opus 4.6: ~ 14 giờ với độ tin cậy 50%, tính từ Time Horizon 1.1 (từ tháng 1 năm 2026).
  Trung文翻译:Claude Opus 4.6:截至 Thời gian Tự chân trời 1.1(2026 年 1 月),50% 可靠性下约 14 小时──
- Thời gian tăng gấp đôi đối với các nhiệm vụ theo kiểu HCAST: ~ 4,3 tháng (130,8 ngày) trên phù hợp sau năm 2023 được báo cáo bởi Time Horizon 1.1 (từ tháng 1 năm 2026); con số ~ 7 tháng là phù hợp đầy đủ từ Time Horizon 1.0 20192025 và được báo cáo trong TH1.1 cùng với số sau năm 2023.
  Trung ngữ翻译:HCAST 类任务的倍增时间:Time Horizon 1.1(1月2026年) 报告的 2023 后拟合上约 4.3 个月(130.8 天); 约 7 个月的数字是Time Horizon 1.0 完整 20192025 拟合,在 TH1.1 中与 2023 后数字一起报告──

Đó là các con số cụ thể phần còn lại của các tham chiếu giai đoạn 15. Chúng được trích dẫn trong RSP v3.0 (Dạy 19) của Anthropic và FSF v3 (Dạy 20) của DeepMind như một trong những phép đo cung cấp đánh giá ngưỡng.

> Đây là các số cụ thể của giai đoạn 15 phần còn lại của các chỉ số. Chúng được trích dẫn trong Anthropic RSP v3.0 (đọc 19 课) và DeepMind FSF v3 (đọc 20 课) là một trong những chỉ số đánh giá giá giá trị.

### Đồ chung điểm

- **HCAST**: 189 nhiệm vụ trên ML, an ninh mạng, kỹ thuật phần mềm và lý luận chung.
  Trung ngữ翻译:**HCAST**:跨机器学习、网络安全、软件工程和通用推理的189任务──范围:1 分钟到8+ 小时专家时间──时间线数字背后主套件──
- **RE-Bench**: 71 ML nhiệm vụ nghiên cứu kỹ thuật với cơ sở chuyên gia con người. đo liệu mô hình có thể thực hiện loại công việc R&D ML cung cấp cho ngưỡng R&D-4 AI.
  Trung ngữ翻译:**RE-Bench**:71 个带人类专家基线的机器学习研究工程任务――衡量模型是否能进入AI R&D-4 值类机器学习研发工作――
- **SWAA**: các nhiệm vụ ngắn hơn; hữu ích cho việc chuẩn bị cuối thấp của đường viền.
  Trung ngữ翻译:**SWAA**:较短任务;用于校准时间线曲线低端──

### Các đánh giá giám sát nguyên mẫu

20252026 Công việc METR bao gồm các nguyên mẫu giám sát-học định: có thể một màn hình bắt được một mô hình thực hiện một nhiệm vụ phụ (một cái gì đó khác hơn những gì nhà điều hành yêu cầu); có thể đại lý trốn tránh màn hình.

> 20252026 METR 工作包括监控评估原型:监控器能否捕获模型执行副任务(操作员请求以外的事);Agent 能否规避监控器──这些直接入 OpenAI PF v2 的"破坏防护"类别和 DeepMind FSF v3(第 20 课) của lừa đảo đối với齐监控──

### Tại sao chân trời là giới hạn trên

- **Idealized tooling**Các nhiệm vụ chuẩn cho mô hình các công cụ sạch và dữ liệu được định dạng tốt.
  Trung ngữ翻译:**理想化工具**: Kỷ nguyên nhiệm vụ cho mô hình các công cụ và dữ liệu có định dạng tốt hơn.
- **No real consequences**: mô hình không bao giờ thực sự tính phí khách hàng, xóa dữ liệu thực, hoặc liên lạc với người thực.
  Trung ngữ翻译:**无真实后果**Mô hình từ không thực tế cho khách hàng tính phí 删除 dữ liệu thực tế hoặc liên hệ với người thực tế  thực tế triển khai có thể không thể đảo ngược 注
- **Eval-context gaming**Bài học 1: Các mô hình hành vi khác nhau trong các thử nghiệm. Báo cáo an toàn AI quốc tế 2026 ghi lại điều này bằng chứng.
  Trung ngữ翻译:**评估上下文博弈**Chương 1: 课. 模型在测试中行为不同. 2026 国际 AI 安全报告实证记录此.
- **No legitimate user variance**Các người dùng thực tế tạo ra các yêu cầu mơ hồ, phụ thuộc vào bối cảnh.
  Trung ngữ翻译:**无合法用户方差**:基准 prompt 是结构化──真实用户产生模糊、上下文相关的请求──

Tốc độ này là giới hạn khả năng trong điều kiện thuận lợi.

> 时间线是有利条件下的能力上限――部署可靠性是不同的数字,更低,团队必须测量自己的分布以知晓――

### Trường hợp đánh giá bên ngoài

Đánh giá bên ngoài quan trọng bởi vì các phòng thí nghiệm nội bộ có động lực để tối ưu hóa các số liệu mà họ báo cáo. Sự độc lập của METR với một phương pháp được tuyên bố và các bài báo được đánh giá bởi các đồng nghiệp là sự giảm thiểu cấu trúc. Nó không đủ một mình (bên phòng thí nghiệm vẫn kiểm soát những gì METR nhìn thấy), nhưng nó là nghiêm ngặt hơn không có đánh giá bên ngoài.

> Việc đánh giá của bên ngoài là rất quan trọng, bởi vì phòng thí nghiệm nội bộ có khả năng cải thiện các chỉ số báo cáo.

### Làm thế nào để sử dụng các số đường chân trời trong thực tế

- **As a capability filter**Nếu chân trời của một mô hình nằm dưới thời gian chuyên môn của một nhiệm vụ được đề xuất, đừng gửi nó tự động (tệp kỹ năng của Lesson 1).
  Trung ngữ翻译:**作为能力过滤器**Nếu thời gian mô hình thấp hơn thời gian chuyên gia của các nhiệm vụ đề xuất, đừng để nó tự phát hành bài tập kỹ năng thứ nhất.
- **As a trend indicator**: thời gian tăng gấp đôi cho bạn biết cách thức hiện tại sẽ vẫn an toàn bao lâu ngay cả khi không có các biện pháp giảm thiểu mới.
  Trung ngữ翻译:**作为趋势指标**: tăng thời gian cho bạn biết thực hành hiện tại ngay cả khi không có sự giảm nhẹ mới vẫn giữ an toàn trong thời gian dài.
- **As a prior**: một chân trời 14 giờ là điểm khởi đầu.
  Trung ngữ翻译:**作为先验**:14 小时时间线是起点.

## Hãy sử dụng nó để thực hiện
```figure
a5-horizon-fit
```

## Sử dụng nó

`code/main.py`thực hiện một sự phù hợp hậu cần của nhiệm vụ thành công so với log(thời gian chuyên gia), với một tập kết quả tổng hợp. Nó báo cáo chân trời 50% (tựa của METR), chân trời 10% (tâm lý), và chân trời 90% ( lạc quan).

> `code/main.py`给定合成结果集实现任务成功率 vs log(专家时间) 的逻辑拟合――报告 50% 时间线(METR 标题) 、10% 时间线(保守) 、90% 时间线(乐观) ⋅

## Chuyển nó đi.

`outputs/skill-horizon-interpretation.md`xem xét yêu cầu về đường chân trời của nhà cung cấp và tạo ra phân tích khoảng cách giữa yêu cầu tham chiếu và thực tế triển khai.

> `outputs/skill-horizon-interpretation.md`审查 tuyên bố thời gian của nhà cung cấp và tạo ra tuyên bố cơ bản và phân tích sự khác biệt giữa thực tế triển khai.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Hãy xác nhận chân trời phù hợp 50% phù hợp với thực tế mặt đất tổng hợp.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận phù hợp 50%  thời gian phù hợp với giá trị thực.

2. Đọc bài đăng trên blog Time Horizon 1.1 của METR. Xác định các nhiệm vụ cụ thể nơi độ tin cậy cao nhất và thấp nhất. Giải thích lý do tại sao khoảng cách tồn tại.
   Trung ngữ翻译:阅读 METR Time Horizon 1.1 博客──识别可靠性最高和最低的具体任务──解释为什么存在差距──

3. Đọc tài nguyên "Mét khả năng AI tự trị" của METR. Đặt danh sách các loại nhiệm vụ HCAST. Chọn một loại mà bạn sẽ cân nặng nặng hơn cho một nhiệm vụ sản xuất và biện minh lý do tại sao.
   Trung ngữ翻译:阅读 METR's "Mét tự động AI 能力"资源──列出 HCAST 任务类别──选择一个你为生产任务加权的类别并论证为何──

4. Lấy game trong mô phỏng: chuyển ~ 20% các nhiệm vụ thất bại thành công. Báo cáo chân trời mới. Điều này gần như tương đương với tỷ lệ game 20% với số lượng được quan sát.
   Trung ngữ翻译: 在模拟器中引入 eval-context gaming:将约20% 失败任务翻转为成功――报告新时间线――

5. Thiết kế đánh giá chân trời nội bộ trên backlog lỗi của riêng bạn hoặc một bộ nhiệm vụ đại diện. Mô tả bộ sưu tập dữ liệu, phù hợp và kết quả xuất phát cho bạn biết gì. So sánh với số METR.
   Trung ngữ翻译: Trong bản bug backlog hoặc đại diện của mình tập hợp nhiệm vụ trên thiết kế trong thời gian đánh giá.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| METR | "External evaluator" | ex-ARC Evals; independent 501(c)(3) since Dec 2023 | METR：原 ARC Evals，独立第三方 |
| Time Horizon | "Capability measure" | Expert task length at 50% reliability, from logistic fit | 时间线：50% 可靠性下专家任务长度 |
| HCAST | "METR's main suite" | 180+ tasks spanning 1 min to 8+ hours | HCAST：METR 主套件，180+ 任务 |
| RE-Bench | "Research engineering" | 71 ML research-engineering tasks with human baseline | RE-Bench：71 个机器学习研发任务 |
| SWAA | "Short-task suite" | Calibrates the low end of the horizon curve | SWAA：短任务套件，校准低端 |
| Doubling time | "Growth rate" | Time for the 50% horizon to double; ~7 months per HCAST | 倍增时间：50% 时间线翻倍所需时间 |
| Eval-context gaming | "Model behaves differently" | Documented behavior gap between tests and deployment | 评估上下文博弈：测试与部署行为差距 |
| Upper bound | "Horizon is a ceiling" | Benchmark horizon > deployment reliability under load | 上限：基准时间线 > 负载下部署可靠性 |

## Xem thêm 延伸阅读

- [METR — Resources for Measuring Autonomous AI Capabilities](https://metr.org/measuring-autonomous-ai-capabilities/) Định hướng HCAST, RE-Bench, SWAA.
  中文翻译:HCAST、RE-Bench、SWAA 规范
- [METR — Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) giấy chân trời gốc.
  Trung ngữ翻译:原始时间线论文
- [METR — Time Horizon 1.1 (January 2026)](https://metr.org/research/) số liệu và phương pháp hiện tại.
  Trung ngữ翻译:当前数字和方法论
- [Epoch AI — METR Time Horizons benchmark](https://epoch.ai/benchmarks/metr-time-horizons) theo dõi trực tiếp.
  Trung ngữ翻译:实时跟踪
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Quan điểm nội bộ về các phép đo của METR.
  Trung文翻译:METR 测量的内部视角
