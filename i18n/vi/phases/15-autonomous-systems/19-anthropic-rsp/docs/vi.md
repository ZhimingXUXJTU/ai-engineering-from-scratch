# Chính sách quy mô chịu trách nhiệm nhân bản v3.0  Antropic  trách nhiệm mở rộng chính sách v3.0

> RSP v3.0 đã có hiệu lực vào ngày 24 tháng 2 năm 2026, thay thế chính sách năm 2023. Lượng giảm thiểu hai cấp: những gì Anthropic sẽ làm một bên so với những gì được hình thành như một khuyến nghị toàn ngành (bao gồm cả các tiêu chuẩn bảo mật RAND SL-4). Thêm lộ trình an toàn biên giới và báo cáo rủi ro như các tài liệu thường xuyên thay vì các tài liệu giao hàng một lần. Thả lời hứa nghỉ ngơi năm 2023. Giới thiệu ngưỡng R&D-4 AI: một khi vượt qua, Anthropic phải xuất bản một trường hợp xác nhận xác định rủi ro và giảm thiểu sự không phù hợp. Claude Opus 4.6 không vượt qua nó. Anthropic tuyên bố trong v3.0 thông báo rằng "để loại trừ điều này trở nên khó khăn". SaferAI xếp hạng RSP 2023 ở mức 2.2; họ hạ cấp v3.0 xuống còn 1.9, đưa Anthropic vào danh mục RSP "thô yếu" cùng với OpenAI và DeepMind. Các ngưỡng chất lượng thay thế các cam kết định lượng năm 2023; việc loại bỏ điều khoản tạm dừng là sự lùi mạnh nhất.

> **【中文解读】**RSP v3.0 于 2026 年 2 月 24 日生效,替代 2023 政策。两层缓解:Anthropic 单边做什么 vs 行业范围建议(包括 RAND SL-4 安全标准) ・添加边境安全路线图和风险报告 作为常设文档而非一次性交付物品──删除 2023 暂停承诺──引入AI R&D-4 值:一旦跨越,Anthropic 必须发布识别不对风险和缓解的肯定案例──Claude Opus 4.6 未跨越它──Anthropic 在 v3.0 公告中声明"自信地排除这变得困难"──Safer 评价 2023 RSP 为 2.2;降级 v3.0 至 1.9,将Anthropic 和 DeepMind 开始"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个"一个" "一个" "一个" "一个" "一个" "一个" "一个" "一个" "一个" "一个" "一个" "一个" "一个" "一个"

> **【拓展：v3.0 的核心改动】**三个关键变化:(1) 添加前沿安全路线图、风险报告、AI R&D-4 值;(2) 删除2023 暂停承诺;(3) 重构两层缓解时间表(Anthropic 单边 vs 行业建议) ――SaferAI's降低因素:定性值替代定量、暂停承诺删除、AI R&D-4 缓解描述为"肯定案例"而不是具体措施、审查机制依赖于安тропо的安全咨询组缺乏独立监督──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, RSP threshold decision engine) | **语言:** Python（标准库，RSP 阈值决策引擎）
**Prerequisites:** Phase 15 · 06 (AAR), Phase 15 · 07 (RSI) | **前置知识:** Phase 15 · 06（AAR），Phase 15 · 07（RSI）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**Học本节前请先掌握:Phase 15·06(AAR) 、Phase 15·07(RSI) 、Phase 15·08(RSI bị ràng buộc)。RSP = 前沿实验室的"安全扩展承诺"既是技术文档也是治理信号──
>  **【类比】**RSP = "AI 公司的安全宪法"──2023 版 = 严格(定量值+暂停承诺);v3.0 = 灵活(定性值+删暂停)──SaferAI 评分从2.2 降至1.9("弱"类别)──新增AI R&D-4 值 = Một khi AI 能自动化AI 研发达到某水平,必须强制披露这是RSI 的车──
> 🤔 **【困惑】**Q: Tại sao xóa tạm dừng cam kết? 商业压力──暂停 = 竞争对手超越你──OpenAI、Google 都没暂停,Anthropic 单方面暂停=自杀──修复:行业协调(RAND SL-4 标准) + 监管干预(EU AI Act)才能避免囚犯困境──

## Vấn đề  vấn đề giới thiệu

Các phòng thí nghiệm biên giới xuất bản các chính sách quy mô phần nào là tài liệu kỹ thuật, phần nào là tài liệu quản lý và phần nào là tín hiệu cho các nhà quản lý.

> Các phần chính sách mở rộng được công bố bởi phòng thí nghiệm trước đây là tài liệu kỹ thuật, phần là tài liệu quản lý, phần là tín hiệu cho nhà quản lý.

RSP v3.0 là tài liệu Anthropic hiện tại. Đọc nó kỹ lưỡng không phải vì tuân thủ nó là ràng buộc (không phải vậy), nhưng bởi vì khung hình hình hóa cách một phòng thí nghiệm hiểu rủi ro thảm họa và cách họ truyền đạt các sự thỏa hiệp với công chúng.

> RSP v3.0 là hiện tại 文档.仔细阅读 không phải vì quy định có sức ràng buộc, mà vì framework for shaping laboratories về cách hình thành các phòng thí nghiệm về rủi ro thảm họa và cách truyền tải chúng đến công chúng.

Sự khác biệt v3.0 vs v2.0 là đơn vị hữu ích. Những gì đã được thêm vào: Bảng đường đường an toàn biên giới, Báo cáo rủi ro, ngưỡng R&D-4 AI. Những gì đã được loại bỏ: cam kết tạm dừng năm 2023.

> Sự khác biệt giữa v3.0 và v2.0 là một đơn vị hữu ích.

Điều đã được tái định dạng: một lịch trình giảm thiểu hai cấp chia giữa Anthropic- đơn phương và khuyến nghị của ngành công nghiệp.

> 重构: chia thành Anthropic 单边和行业建议的两层缓解时间表──外部审查SaferAI将分数从2.2(v2)降至1.9(v3.0)──这是扩展政策如何在看上看更精细的同时变得更不严谨的──

> **【中文解读】**Chính sách mở rộng trách nhiệm của nhân loại (RSP, Responsible Scaling Policy) xác định được một khuôn khổ để giữ an toàn trong sự phát triển của năng lực AI.

## Khái niệm cốt lõi

### Lịch trình giảm nhẹ hai cấp độ

- **Anthropic unilateral actions**: những gì Anthropic sẽ làm bất kể những gì các phòng thí nghiệm khác làm.
  Trung ngữ翻译:**Anthropic 单边动作**Không kể các phòng thí nghiệm khác làm gì, Antropic sẽ làm gì.
- **Industry-wide recommendations**: những gì Anthropic nghĩ ngành công nghiệp nên làm chung bao gồm các tiêu chuẩn an ninh RAND SL-4.
  Trung ngữ翻译:**行业范围建议**:Anthropic 认为行业应集体做──包括 RAND SL-4 安全标准──这些不是Anthropic 侧的承诺;是政策倡导──

Cơ cấu hai cấp không có trong v2. Điều này có nghĩa là người đọc cần phải xem từng cột nào trong mỗi cam kết sống.

> 两层结构在 v2 中没有──这意味着读者需要看每个承诺在哪一列──"Bảng rộng đề nghị" trong các biện pháp an ninh không phải là cam kết của nhân chủng; là hy vọng của nhân chủng──

### Giá trị của AI R&D-4

Đây là mức năng lực RSP v3.0 đặt tên là ngưỡng tiếp theo quan trọng. cụ thể: một mô hình có thể tự động hóa một phần đáng kể của nghiên cứu AI với chi phí cạnh tranh. Một khi Anthropic tin rằng một mô hình vượt qua nó, họ phải xuất bản một trường hợp xác nhận xác định rủi ro và giảm thiểu sự không phù hợp trước khi tiếp tục mở rộng quy mô.

> Đây là RSP v3.0 được đặt tên là cấp độ năng lực quan trọng. Cụ thể: năng lực tự động hóa chi phí cạnh tranh là một phần tương đương của mô hình nghiên cứu AI.

Claude Opus 4.6 không vượt qua nó theo thông báo v3.0. Tài liệu này thêm: "Thật tự tin rằng việc loại trừ điều này đang trở nên khó khăn".

> Claude Opus 4.6 根据 v3.0 公告未跨越它──文档添加:"自信地排除这变得困难──" Lời nói này quan trọng; nó thừa nhận 值足接近以致是现实关注,不是推测性限制──

Bài học 6 (Thiết học Tích ứng tự động) và Bài học 7 (Thiết học tự cải thiện tái phát) tiếp cận trực tiếp với ngưỡng này. Các nhà nghiên cứu sắp xếp tự động vượt qua các thanh chất lượng nghiên cứu là bằng chứng cho thấy ngưỡng R&D-4 AI đang gần gũi.

> 第 6 课                                                                                                                                                                                                                                                             

### Bản đồ đường bộ an toàn biên giới và báo cáo rủi ro .

v3.0 nâng cao hai loại đồ tạo vật lên các tài liệu hiện hữu:

> v3.0 sẽ nâng cấp hai loại sản phẩm thành văn bản thường trực:

- **Frontier Safety Roadmap**: tài liệu nhìn về tương lai mô tả công việc an toàn được lên kế hoạch, kỳ vọng về khả năng và nghiên cứu giảm thiểu.
  Trung ngữ翻译:**前沿安全路线图**: mô tả kế hoạch an ninh工作、能力预期和缓解研究的前文档──
- **Risk Report**: tài liệu phản hồi về các mô hình cụ thể sau khi phát hành, mô tả khả năng được quan sát và rủi ro dư thừa.
  Trung ngữ翻译:**风险报告**: xuất bản sau mô hình cụ thể, mô tả khả năng quan sát và dư风险

Cả hai đều công khai. Cả hai đều được cập nhật theo một thời gian được tuyên bố. Sự hữu ích là: người đọc có thể theo dõi cách những gì Anthropic nói họ sẽ làm trong một lộ trình so sánh với những gì họ báo cáo trong một Báo cáo rủi ro.

> 两者公开──两者按声明节奏更新──效果:读者可追踪 动态图中说会做与风险报告中报告的如何对比──

### Xóa điều khoản tạm dừng

RSP 2023 bao gồm một cam kết tạm dừng rõ ràng: nếu một mô hình vượt qua ngưỡng khả năng cụ thể, đào tạo sẽ tạm dừng cho đến khi giảm thiểu được thực hiện. v3.0 thay thế tạm dừng rõ ràng bằng một công thức mềm hơn (bổ bản một trường hợp khẳng định, tiếp tục nếu giảm thiểu là đầy đủ). SaferAI và các nhà phân tích khác gọi điều này trực tiếp là sự lùi lại mạnh nhất trong tài liệu mới.

> 2023 RSP 包含显式暂停承诺: nếu mô hình vượt qua một năng lực cụ thể, đào tạo sẽ tạm dừng cho đến khi缓解就位──v3.0 用更软表述(发布肯定案例,如缓解充分则继续) thay thế显式暂停──SaferAI 和其他分析师直接指出这是新文档中最强回归──

Nguyên lý chính sách cho sự thay đổi: ngưỡng số lượng vào năm 2023 đã không thể đạt được bởi các chuẩn khả năng thời kỳ 2026 bởi vì các chuẩn chính là đã được quy mô lại. Nguyên lý phản đối: một điều khoản tạm dừng trong một chính sách quy mô là một thiết bị cam kết; loại bỏ nó loại bỏ tính đáng tin cậy của chính sách.

> 变更的政策论文:2023 定量值被2026 时代能力基准证明不可达,因为基准本身被重缩缩. 反论:暂停条款在扩张政策中的暂停条款是承诺装置;移除它移除政策可信度.

### SaferAI được hạ cấp hơn.

SaferAI là một tổ chức độc lập đánh giá các tài liệu kiểu RSP. Đánh giá công khai của họ: 2023 Anthropic RSP đạt 2.2 (từ một thang đo mà 4.0 là RSP tốt nhất hiện tại và 1.0 là danh nghĩa). v3.0 đạt 1.9. Điều này đã di chuyển Anthropic từ "tâm trung" đến "thô yếu", gia nhập OpenAI và DeepMind trong danh mục yếu.

> SaferAI là một tổ chức độc lập trong các tài liệu RSP 式. Its public rating:2023 Anthropic RSP đạt 2.2(4.0 là RSP tốt nhất hiện tại, 1.0 là một trong những loại RSP tốt nhất trên danh sách.

Các yếu tố giảm cấp cho mỗi SAferAI:

> Các yếu tố giảm cấp được đưa ra:

- Các ngưỡng chất lượng thay thế các ngưỡng số lượng.
  Trung文翻译:定性值替代定量──
- Việc tạm dừng được xóa.
  Trung ngữ翻译:暂停承诺移除──
- Các biện pháp giảm thiểu ngưỡng R&D-4 của AI được mô tả là "vụ án xác nhận" chứ không phải là các biện pháp cụ thể.
  Trung文翻译:AI R&D-4 值缓解描述为"肯定案例"而非具体措施──
- Cơ chế xem xét phụ thuộc vào Nhóm tư vấn an toàn của Anthropic, với giám sát độc lập hạn chế.
  Trung ngữ翻译:审查机制依赖人类的安全咨询组,独立监督有限.

### Bài học này không phải là gì.

Đây không phải là một bài học về tuân thủ. RSP v3.0 không phải là một quy định; không có gì buộc Anthropic phải tuân thủ nó.

> Đây không phải là một chương trình quy định.

Bài học là đọc tài liệu với sự cụ thể và hoài nghi mà nó xứng đáng. Các chính sách quy mô là các tín hiệu biên giới công cộng đầu tiên phát ra về các tư thế rủi ro thảm họa. Việc đọc chúng một cách tốt là một kỹ năng thực tế cho bất cứ ai mà công việc của họ phụ thuộc vào khả năng biên giới.

> Các chương trình học là những đặc điểm và nghi ngờ mà nó có thể sử dụng để đọc tài liệu. Chính sách mở rộng là những tín hiệu công khai chính của phòng thí nghiệm tiên phong về các thái độ rủi ro thảm họa.

## Hãy sử dụng nó để thực hiện
```figure
a5-rsp-ladder
```

## Sử dụng nó

`code/main.py`thực hiện một động cơ quyết định nhỏ phản ánh hình dạng đánh giá ngưỡng RSP: với một mô hình ứng viên và một bộ đo khả năng, trả về liệu ngưỡng AI R&D-4 đã vượt qua, các phần trường hợp xác nhận cần thiết, và liệu việc triển khai có thể tiếp tục hay không.

> `code/main.py`实现镜像 RSP 值评估形状的小决策引擎:给定候选模型和一组能力测量, trả lại AI R&D-4 值是否跨越、需要肯定案例节、部署是否可继续──它故意简单;点是让文档逻辑显式──

## Chuyển nó đi.

`outputs/skill-scaling-policy-review.md`xem xét chính sách quy mô (Anthropic, OpenAI, DeepMind hoặc nội bộ) so với tham chiếu v3.0: cấu trúc hai cấp, ngưỡng, cam kết tạm dừng, xem xét độc lập.

> `outputs/skill-scaling-policy-review.md`Đối với v3.0 参考审查扩展政策 ((Anthropic、OpenAI、DeepMind或内部): hai tầng cấu trúc、值、暂停承诺、独立审查。

## Tập luyện bài tập

1. Đi chạy`code/main.py`. Đưa vào ba mô hình tổng hợp ở các cấp độ khả năng khác nhau. Đảm bảo rằng người đánh giá ngưỡng hành vi như mong đợi và tạo ra mẫu trường hợp xác nhận đúng.
   Trung ngữ翻译:运行 `code/main.py` vào 3 cấp độ khác nhau mô hình tổng hợp  xác nhận  giá trị đánh giá theo hành vi dự kiến và tạo ra đúng  xác nhận trường hợp mô hình 

2. Đọc RSP v3.0 đầy đủ (32 trang). Định danh mọi cam kết sống trong cấp độ "sự khuyến nghị toàn ngành".
   Trung ngữ翻译:全文阅读 RSP v3.0(32页) ――识别"行业范围建议"层中的每个承诺──v2 中哪些会是"Anthropic 单边"?

3. Đọc phương pháp đánh giá RSP của SaferAI. Tạo lại điểm số 1.9 của họ cho v3.0 bằng cách áp dụng rubric của họ cho tài liệu. Dòng rubric nào đã thúc đẩy downgrade nhiều nhất?
   Trung文翻译:阅读 SaferAI's RSP 评分方法论──通过将评分量表应用于文档复现 v3.0 的 1.9 分──哪个量表行驱动降级最多?

4. Thỏa thuận tạm dừng năm 2023 đã được loại bỏ. đề xuất một cam kết thay thế để bảo vệ uy tín của chính sách trong khi thừa nhận vấn đề tái quy mô điểm chuẩn năm 2026.
   Trung文翻译:2023 暂停承诺被移除──提议保留政策可信度同时承认2026 基准重缩问题的替代承诺──

5. So sánh RSP v3.0 với OpenAI Preparedness Framework v2 (Dạy 20) Chọn một khu vực mà v3.0 mạnh hơn. Chọn một khu vực mà Preparedness Framework mạnh hơn.
   Trung文翻译:Compared RSP v3.0 với OpenAI Preparedness Framework v2 ((第 20 课) ⋅ chọn một v3.0 更强的领域── chọn một Preparedness Framework 更强的领域──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| RSP | "Anthropic's scaling policy" | Responsible Scaling Policy; v3.0 effective Feb 24, 2026 |
| RSP | "Anthropic 的扩展政策" | Responsible Scaling Policy；v3.0 2026 年 2 月 24 日生效 |
| AI R&D-4 | "Research-automation threshold" | Capability to automate substantial AI research at competitive cost |
| AI R&D-4 | "研究自动化阈值" | 以竞争成本自动化相当部分 AI 研究的能力 |
| Affirmative case | "Safety justification" | Published argument that risks are identified and mitigations adequate |
| 肯定案例 | "安全证明" | 风险已识别缓解充分的已发布论证 |
| Frontier Safety Roadmap | "Forward plan" | Standing document on planned safety work and expected capabilities |
| 前沿安全路线图 | "前瞻计划" | 计划安全工作和预期能力的常设文档 |
| Risk Report | "Retrospective on a model" | Standing document on observed capability and residual risk after release |
| 风险报告 | "模型事后" | 发布后观察能力和剩余风险的常设文档 |
| Two-tier mitigation | "Unilateral vs industry" | Anthropic commitments vs industry recommendations, separated |
| 两层缓解 | "单边 vs 行业" | Anthropic 承诺 vs 行业建议，分开 |
| Pause commitment | "2023 clause" | Explicit promise to pause training; removed in v3.0 |
| 暂停承诺 | "2023 条款" | 暂停训练的显式承诺；v3.0 中移除 |
| SaferAI rating | "Independent RSP grade" | Third-party rubric; v3.0 scored 1.9 (v2 was 2.2) |
| SaferAI 评分 | "独立 RSP 评分" | 第三方量表；v3.0 得 1.9（v2 是 2.2） |

## Xem thêm 延伸阅读

- [Anthropic — Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) Chính sách đầy đủ 32 trang.
  Trung văn翻译:完整 32 页政策。
- [Anthropic — RSP v3.0 announcement](https://www.anthropic.com/news/responsible-scaling-policy-v3) tổng kết các thay đổi từ v2.
  Trung文翻译:v2 变更摘要。
- [Anthropic — Frontier Safety Roadmap](https://www.anthropic.com/research/frontier-safety) Tài liệu thường trực liên kết từ RSP v3.0.
  Trung文翻译:RSP v3.0 链接的常设文档──
- [Anthropic — Risk Report: Claude Opus 4.6](https://www.anthropic.com/research/risk-report-claude-opus-4-6) Nhìn lại về mô hình biên giới hiện tại.
  Trung ngữ翻译:当前前沿模型的事后.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) kết nối AI R&D-4 với tự trị được đo lường.
  Trung文翻译:将 AI R&D-4 连接到测量的自主性──
