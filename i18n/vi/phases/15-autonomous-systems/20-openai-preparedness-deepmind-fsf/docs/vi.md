# OpenAI Prep Framework và DeepMind Frontier Safety Framework

> OpenAI Preparedness Framework v2 (ngày 4 năm 2025) giới thiệu các danh mục nghiên cứu  Tự trị tầm xa, Sandbagging, Tái tạo tự trị và thích nghi, Giảm bảo  khác với các danh mục theo dõi. Các danh mục theo dõi kích hoạt các báo cáo về khả năng cộng với báo cáo bảo vệ được xem xét bởi Nhóm tư vấn an toàn. FSF v3 của DeepMind (Thiên tháng 9 năm 2025, với Cấp độ Khả năng theo dõi được thêm vào ngày 17 tháng 4 năm 2026) gấp tự trị thành lĩnh vực R&D và Cyber của ML (ML R&D tự trị cấp 1 = tự động hóa hoàn toàn đường ống R&D AI với chi phí cạnh tranh so với công cụ AI + con người). FSF v3 rõ ràng giải quyết sự sắp xếp sai lầm thông qua giám sát tự động cho việc sử dụng sai dụng lý luận bằng công cụ. Lưu ý trung thực: Các danh mục nghiên cứu trong PF v2 (bao gồm cả Tự trị tầm xa) không tự động kích hoạt giảm thiểu; ngôn ngữ chính sách là "có khả năng". Bản thân DeepMind nói rằng giám sát tự động "sẽ không đủ lâu dài" nếu suy luận công cụ được tăng cường.

> **【中文解读】**Bài viết này giới thiệu các khuôn khổ an toàn của AI 实验室  Anthropic RSP OpenAI Preparedness DeepMind FSF 


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-framework decision-table diff tool) | **语言:** Python（标准库，三框架决策表差异工具）
**Prerequisites:** Phase 15 · 19 (Anthropic RSP) | **前置知识:** Phase 15 · 19（Anthropic RSP）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**Học本节前请先掌握:Phase 15·19(Anthropic RSP) Phase 15·07(RSI) Phase 15·04(DGM Autonomous Agent)  本节对比三大前沿实验室的安全框架发现它们口径不一致──
>  **【类比】**三大实验室 RSP đối比 = "三家航空公司的安全手册"。Anthropic = 严格但商业压力大(删暂停);OpenAI = 双轨(Tracked 严格+Research 灵活);DeepMind = 域整合(自主性折折 into ML R&D 和网络安全)。
> 🤔 **【困惑】**Q: Tại sao RSP đều là cam kết tự nguyện? Vì không có luật pháp bắt buộc. EU AI Act là luật pháp khu vực đầu tiên nhưng chỉ bao gồm EU.

## Vấn đề  vấn đề giới thiệu

Bài học 19 đọc chính sách quy mô của Anthropic một cách gần gũi. Bài học này hoàn thành bức tranh bằng cách đọc OpenAI và DeepMind. Ba tài liệu là đồ tạo tác bằng người anh em cùng một câu hỏi  khi nào một phòng thí nghiệm biên giới nên tạm dừng hoặc cổng một mô hình  và chúng hội tụ trên một tập hợp nhỏ các loại và khác nhau ở những nơi cụ thể có ý nghĩa.

> Chương 19  Xem kỹ Chính sách mở rộng của Anthropic. Bài này qua đọc Chính sách của OpenAI và DeepMind để hoàn thành toàn cảnh.

Sự hội tụ: cả ba nhãn tự trị tầm xa như một lớp khả năng đáng theo dõi. Cả ba đều thừa nhận hành vi lừa đảo là một loại rủi ro cụ thể. Cả ba đều có một cơ quan kiểm tra nội bộ. Sự khác biệt: OpenAI chia các loại thành "Điểm tra" (tạm dịch giảm thiểu bắt buộc) và "Khảo sát" (không có kích hoạt tự động). DeepMind gấp tự trị thành hai miền thay vì đặt tên riêng biệt. Các phòng thí nghiệm đặt tên là Tracked vs Research, hoặc Critical vs Moderate, hoặc Tier-1 vs Tier-2; hậu quả hoạt động của cái thùng mà một khả năng sống trong là khác nhau giữa các phòng thí nghiệm.

> 收点: 三者都将长程自主标记为值得跟踪的能力类别──三者都承认欺骗行为──对齐伪装、沙包) 是特定风险类别──三者都有内部审查机构──分歧点:OpenAI sẽ分为"Tracked"(强制缓解) 和"Research"(无自动触发)──DeepMind sẽ tự chủ性 gấp đôi thành hai lĩnh vực chứ không phải riêng biệt命名──实验室命名 Tracked vs Research、Critical vs Moderate、Tier-1 vs Tier-2; năng lực của các thùng vận hành khác nhau trong các phòng thí nghiệm.

Đọc chúng cùng nhau là bài tập hữu ích. Khả năng tương tự có thể là "sự giảm thiểu bắt buộc" tại Anthropic, "đánh giá nhưng không kích hoạt" tại OpenAI, và "để theo dõi trong một lĩnh vực cụ thể" tại DeepMind.

> Để cùng người đọc là một bài tập hữu ích. Một khả năng tương tự trong Anthropic là "phục hồi bắt buộc", trong OpenAI là "phản tra nhưng không xúc tác", trong DeepMind là "để theo dõi trong một lĩnh vực cụ thể".

## Khái niệm cốt lõi

### Khung chuẩn bị OpenAI v2 (ngày 4 tháng 4 năm 2025)

Cấu trúc:

> 结构:

- **Tracked Categories**: báo cáo khả năng (cái gì mô hình có thể làm) cộng với báo cáo bảo vệ (cái gì là giảm thiểu đang được thực hiện).
  Trung ngữ翻译:**Tracked Categories（跟踪类别）**:触发能力报告 (模型能做什么)加防护报告 (已有哪些缓解)
- **Research Categories**: các khả năng mô hình mà phòng thí nghiệm đang theo dõi nhưng chưa cam kết giảm thiểu cụ thể. Bao gồm tự trị tầm xa, Sandbagging, sao chép tự trị và thích nghi, Giảm bảo bảo vệ.
  Trung ngữ翻译:**Research Categories（研究类别）**: phòng thí nghiệm đang theo dõi nhưng chưa cam kết xác định khả năng mô hình giảm nhẹ.

Các phân loại nghiên cứu không tự động kích hoạt giảm thiểu. Ngôn ngữ chính sách là giảm thiểu "có khả năng". Đây là delta cụ thể để xem: vị trí của một phân loại trong Tracked vs Research là vòng tròn giữa "cửa" và "được quan sát".

> V2 của khung quan trọng:Phân loại nghiên cứu không tự động触发缓解.

### DeepMind Frontier Safety Framework v3 (Tháng 9 năm 2025; Cấp năng lượng theo dõi được thêm vào ngày 17 tháng 4 năm 2026)

Cấu trúc:

> 结构:

- **Critical Capability Levels (CCLs)**: ngưỡng khả năng trong năm lĩnh vực: Cyber, Bio, ML R&D, CBRN, tự trị (được gấp vào ML R&D và Cyber).
  Trung ngữ翻译:**Critical Capability Levels（CCL，关键能力等级）**:跨五个领域的能力值:网络、生物、机器学习研发、CBRN、自主性(lập đến机器学习研发和网络中)
- **Tracked Capability Levels**Ví dụ cụ thể: ML R&D tự trị cấp 1 = tự động hóa hoàn toàn đường ống dẫn R&D AI với chi phí cạnh tranh so với công cụ AI + con người.
  Trung ngữ翻译:**Tracked Capability Levels（跟踪能力等级）**:2026  4 月 追加额外粒度──具体例:机器学习研发自主级 1 = 以与人类+AI 工具竞争的成本完全自动化AI 研发管道──
- **Deceptive alignment monitoring**: cam kết rõ ràng về việc theo dõi tự động cho việc sử dụng sai dụng các phương tiện lý luận.
  Trung ngữ翻译:**欺骗对齐监控**: Cảm bảo rõ ràng về việc tự động giám sát việc lạm dụng các công cụ.

Các khung tự trị khác với OpenAI. DeepMind không giữ "Autonomy" như một tên miền cấp cao; nó được gấp vào các tên miền mà tự trị sẽ gây ra thiệt hại (ML R&D và Cyber).

> Quản lý tự chủ không giống OpenAI. Thiết kế sâu không được giữ lại cho "tự chủ" như một lĩnh vực cấp cao; nó được gấp đôi thành lĩnh vực tự chủ gây tổn hại cho cơ sở học máy và phát triển mạng.

### Những gì cả ba tụ tập

- Nhóm tư vấn an toàn nội bộ (nghĩa là Anthropic SAG, OpenAI SAG, DeepMind ủy ban nội bộ).
  中文翻译:内部安全咨询组 ((名为人类SAG、OpenAI SAG、DeepMind 内部委员会) ――高能力模型部署前审查。
- Việc ghi rõ ràng về sự sắp xếp / sắp xếp giả mạo khiêu dâm như một lớp rủi ro.
  Trung ngữ翻译:明确提及欺骗对齐/对齐伪装作为风险类别──
- Các hiện vật cố định trên một thời gian được tuyên bố (Anthropic: Roadmap an toàn biên giới, Báo cáo rủi ro; OpenAI: Báo cáo về khả năng và bảo vệ; DeepMind: chu kỳ cập nhật FSF).
  Trung ngữ翻译:按声明节奏发布的常设工件(Anthropic:前沿安全路线图、风险报告;OpenAI:能力和防护报告;DeepMind:FSF 更新周期) ⋅
- Sự thừa nhận rằng các phòng thủ chỉ theo dõi có một giới hạn. DeepMind rõ ràng: "Việc giám sát tự động sẽ không đủ lâu dài".
  Trung文翻译: thừa nhận chỉ có kiểm soát phòng thủ có giới hạn.

### Ở đâu chúng khác nhau

- **Anthropic**: cam kết tạm dừng được loại bỏ trong v3.0; AI R&D-4 ngưỡng là cửa tiếp theo được đặt tên.
  Trung ngữ翻译:**Anthropic**:v3.0 移除暂停承诺;AI R&D-4 值是命名的下一个门控──
- **OpenAI**: Tracked vs Research chia; Các danh mục nghiên cứu (bao gồm Autonomy tầm xa) không tự động mở cửa.
  Trung ngữ翻译:**OpenAI**:Tracked vs Research 分割;Phát nghiên cứu
- **DeepMind**: tự trị được gấp vào các lĩnh vực khác; Các mức độ khả năng theo dõi thêm tính chi tiết vào tháng 4 năm 2026.
  Trung ngữ翻译:**DeepMind**: tự chủ性 gấp lên các lĩnh vực khác;Cấp độ khả năng theo dõi trong năm 2026 4月 tăng粒度。

### Sandbagging: một khả năng cụ thể phức tạp cả ba

Sandbagging (một mô hình có hiệu quả kém về chiến lược trong các đánh giá) nằm trong các danh mục nghiên cứu của OpenAI. RSP v3.0 của Anthropic giải quyết nó thông qua khoảng cách đánh giá-mô tả (Dạy học 1). DeepMind giải quyết nó thông qua giám sát sắp xếp lừa đảo trong FSF v3.

> Sandbagging (模型在评估中战略性表现不佳) trong OpenAI's Research Categories 中──Anthropic RSP v3.0 通过评估上下文差距(第 1 课) xử lý──DeepMind 通过 FSF v3 的欺骗对齐监控处理──

Nếu một mô hình không thực hiện các đánh giá, ngưỡng khả năng của mỗi khung được đánh giá thấp.

> Nếu mô hình được đánh giá trong khi được cài đặt, khả năng của mỗi khung được đánh giá thấp.

### Kỹ năng đọc chính sách

- Tìm: mọi khả năng bạn quan tâm nên được tìm thấy trong chính sách. Nếu không có, chính sách không bao gồm nó.
  Trung ngữ翻译:**定位**: Mỗi năng lực bạn quan tâm nên được tìm thấy trong chính sách. Nếu không thể tìm thấy, chính sách không bao gồm nó.
- Định dạng: nó được theo dõi (đẩy ra giảm thiểu) hay nghiên cứu (đẩy ra nhưng không kích hoạt)? OpenAI đặt tên cho điều này; Anthropic và DeepMind có tương đương riêng của họ.
  Trung ngữ翻译:**分类**: là theo dõi (chuyên tắc) hay nghiên cứu (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc) (chuyên tắc)
- Tỷ lệ: chính sách được cập nhật theo một lịch trình được tuyên bố, hoặc chỉ sau các sự kiện cụ thể?
  Trung ngữ翻译:**节奏**Chính sách theo tuyên bố kế hoạch mới, hoặc chỉ sau một sự kiện cụ thể?
- Sự độc lập: xem xét bên ngoài là bắt buộc hay tùy chọn? Đối tác nhân bản với Apollo và Viện An toàn AI của Mỹ; OpenAI với METR; DeepMind với SAG nội bộ chủ yếu.
  Trung ngữ翻译:**独立性**Các nghiên cứu bên ngoài có bắt buộc hay có thể lựa chọn?Anthropic với Apollo và Viện An ninh AI Hoa Kỳ hợp tác;OpenAI với METR hợp tác;DeepMind chủ yếu với SAG bên trong:

## Hãy sử dụng nó để thực hiện
```figure
a5-tracked-vs-research
```

## Sử dụng nó

`code/main.py`thực hiện một công cụ khác biệt bảng quyết định nhỏ. Với một khả năng (tự trị, sắp xếp lừa đảo, tự động hóa R&D, nâng cao mạng, vv), nó đưa ra cách mỗi ba chính sách phân loại khả năng, và điều gì kích hoạt giảm thiểu. Đó là một công cụ đọc, không phải là một công cụ chính sách.

> `code/main.py`实现小型决策表差异工具――给定一个能力 ((自主性、欺骗对齐、研发自动化、网络增强等), đưa ra ba chính sách về cách phân loại năng lực này, cũng như kích thích những sự giảm nhẹ nào.

## Chuyển nó đi.

`outputs/skill-cross-policy-diff.md`tạo ra một so sánh giữa các chính sách cho một khả năng cụ thể, sử dụng ba khung làm tham chiếu.

> `outputs/skill-cross-policy-diff.md`Để xác định khả năng tạo ra các chính sách so sánh, sử dụng ba khung như một tài liệu tham khảo.

## Tập luyện bài tập

1. Đi chạy`code/main.py`. Đảm bảo sản xuất của công cụ khác nhau phù hợp với các chính sách cho ít nhất hai khả năng bạn có thể xác minh với tài liệu nguồn.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận sự khác biệt công cụ xuất khẩu phù hợp với ít nhất hai khả năng xác minh tài liệu nguồn bạn có thể có.

2. Đọc OpenAI Preparedness Framework v2 đầy đủ. Định danh từng hạng mục nghiên cứu. Đối với mỗi hạng mục, hãy viết một câu về lý do tại sao nó nằm trong Research thay vì Tracked.
   Trung文翻译:完整阅读 OpenAI Preparedness Framework v2──识别每个研究类型──为每个写一句话说明为何在研究而非追踪──

3. Đọc đầy đủ DeepMind FSF v3, cộng với cập nhật Capacity Levels Tracked tháng 4 năm 2026 xác định các tiêu chí đánh giá cụ thể của ML R&D tự trị cấp 1. Làm thế nào bạn sẽ đo nó bên ngoài?
   Trung文翻译:完整阅读 DeepMind FSF v3 加 2026 年 4 月 Theo dõi Capacity Levels 更新──识别机器学习研发自主等级 1 的具体评估标准──你会如何外部测量?

4. Sandbagging nằm trong các danh mục nghiên cứu của OpenAI. Thiết kế một đánh giá mà sẽ buộc một mô hình sandbagging để tiết lộ khả năng thực tế của nó. tham khảo bài học 1 đánh giá-những trò chơi ngữ cảnh.
   Trung文翻译:Sandbagging 在 OpenAI Research Categories 中──设计一个评估迫使沙bagging 模型揭示其真实能力──参考第 1 课评语文游戏讨论──

5. So sánh ba chính sách về một khả năng cụ thể (tự chọn của bạn).Chỉ ra phân loại chính sách nào bạn thấy nghiêm ngặt nhất và ít nhất.
   Trung ngữ翻译:比较三政策在特定能力 (你选) 上分类──命名你认为最严格和最不严格的分类──用源文本论证──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| Preparedness Framework | "OpenAI's scaling policy" | PF v2 (April 2025); Tracked vs Research categories | OpenAI 准备度框架：PF v2，Tracked vs Research |
| Tracked Category | "Mandatory mitigation" | Triggers Capabilities + Safeguards Reports; SAG review | 跟踪类别：触发能力+防护报告，SAG 审查 |
| Research Category | "Monitored only" | Tracked but no automatic mitigation; includes Long-range Autonomy | 研究类别：跟踪但不自动缓解，含长程自主 |
| Frontier Safety Framework | "DeepMind's scaling policy" | FSF v3 (Sept 2025) + Tracked Capability Levels (Apr 2026) | DeepMind 前沿安全框架 |
| CCL | "Critical Capability Level" | DeepMind threshold per domain (Cyber, Bio, ML R&D, CBRN) | 关键能力等级：DeepMind 各领域阈值 |
| ML R&D autonomy level 1 | "R&D automation" | Fully automate AI R&D pipeline at competitive cost | 机器学习研发自主等级 1：完全自动化研发管道 |
| Sandbagging | "Strategic underperformance" | Model underperforms on evals; in OpenAI Research Categories | Sandbagging：模型战略性表现不佳 |
| Instrumental reasoning | "Means-ends reasoning" | Reasoning about how to achieve goals; target of DeepMind monitoring | 工具性推理：DeepMind 监控目标 |

## Xem thêm 延伸阅读

- [OpenAI — Updating our Preparedness Framework](https://openai.com/index/updating-our-preparedness-framework/) V2 thông báo.
  Trung ngữ翻译:v2 公告
- [OpenAI — Preparedness Framework v2 PDF](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf) Tài liệu đầy đủ.
  Trung ngữ翻译:完整文档
- [DeepMind — Strengthening our Frontier Safety Framework](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) Thông báo FSF v3.
  Trung ngữ翻译:FSF v3 公告
- [DeepMind — Updating the Frontier Safety Framework (April 2026)](https://deepmind.google/blog/updating-the-frontier-safety-framework/) Tăng thêm các mức độ khả năng theo dõi.
  中文翻译:Cấp độ khả năng theo dõi 添加
- [Gemini 3 Pro FSF Report](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_fsf_report.pdf) ví dụ về báo cáo rủi ro theo định dạng FSF.
  Trung文翻译:FSF 格式风险报告 ví dụ
