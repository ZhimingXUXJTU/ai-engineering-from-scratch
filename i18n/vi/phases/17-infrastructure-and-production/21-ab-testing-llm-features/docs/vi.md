# A / B kiểm tra LLM Features  GrowthBook, Statsig, và Vibes vấn đề ✓ 特性 LLM PR

> Việc kiểm tra A/B truyền thống không được xây dựng cho LLM không xác định. Sự phân biệt quan trọng: các đánh giá trả lời "có thể mô hình làm công việc này không?" Các thử nghiệm A / B trả lời "có người dùng quan tâm không?" Cả hai đều cần thiết; vận chuyển trên kiểm tra vibe đã kết thúc. Những gì phải thử nghiệm vào năm 2026: kỹ thuật nhanh chóng (lập luận), lựa chọn mô hình (GPT-4 vs GPT-3.5 vs OSS; độ chính xác vs chi phí vs thời gian trễ), các tham số sản xuất (giới nhiệt, top-p). Các trường hợp thực tế: một biến thể mô hình thưởng chatbot cung cấp +70% chiều dài cuộc trò chuyện và +30% lưu giữ; Các thí nghiệm dòng chủ đề AI Nextdoor cung cấp +1% CTR sau khi tinh chỉnh chức năng thưởng; Khan Academy Khanmigo lặp lại trên trục độ trễ so với độ chính xác toán học. Phân chia nền tảng: **Statsig**(được mua lại bởi OpenAI với giá 1,1 tỷ đô la vào tháng 9 năm 2025)  kiểm tra theo trình tự, CUPED, tất cả trong một. **GrowthBook** mã nguồn mở, nhà kho, Bayesian + Frequentist + động cơ theo trình tự, CUPED, kiểm tra SRM, Benjamini-Hochberg + Bonferroni sửa chữa. Bạn chọn dựa trên sở thích nhà kho-SQL và liệu "được mua bởi OpenAI" có quan trọng với tổ chức của bạn hay không.

> **【中文解读】**Bài viết này giới thiệu về các phương pháp làm việc của LLM đặc biệt AB 测试科学评估 LLM 功能变更效果──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy sequential test simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 20 (Progressive Deployment) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 20 (Progressive Deployment)

>  **【前置】**Học本节前请先掌握:Phase 17·13(可观测性) Phase 17·20(渐进部署) 统计基础(CUPED、序贯测试) 传统 A/B 不为不确定性 LLM 设计──
>  **【类比】**LLM A/B 测试 = "with scientific method substitute for拍脑袋"。关键区别:eval 问"模型能做吗";A/B 问"用户在乎吗"。两者都要──测什么:快措辞、模型选择、生成参数(温度/top-p)。案例:聊天机器人变体+70% 对话长度+30% 留存;Nextdoor AI 标题+1% CTR;Khanmigo 在延迟 vs 数学准确率间舍舍──平台:Statsig((AI 11 tỷ 收购,全功能) 、GrowthBook 开源厂 原生、贝叶斯频率+被序贯引擎) ∼
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Sự khác biệt giữa các đánh giá ("có thể mô hình làm công việc") và các thử nghiệm A/B ("do users care").
  Trung文翻译:区分评估("模型能做这个工作吗")和 A/B 测试("用户在乎吗")。
- Đếm ba trục có thể kiểm tra (giải pháp, mô hình, tham số) và chọn số liệu cho mỗi trục.
  Trung文翻译:列举三个可测试轴(提示、模型、参数)并为每个选择指标──
- Giải thích CUPED, kiểm tra theo trình tự và sửa đổi so sánh nhiều lần của Benjamini-Hochberg.
  Trung文翻译:解释 CUPED、序贯检验和 Benjamini-Hochberg 多重比较校正──
- Chọn Statsig hoặc GrowthBook dựa trên tư thế kho-SQL và lập trường mua lại của công ty.
  Trung文翻译:根据仓库-SQL 态势和企业收购立场选择 Statsig 或 GrowthBook。

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**传统 A/B 测试不是为不确定性 LLM 构建的. 关键区分:评估(evals) trả lời"模型能做这件事吗?",A/B 测试回答"用户在乎吗?"两者都是必需的凭感觉上线(vibes check) thời đại đã kết thúc.

> **【拓展：LLM A/B 测试的真实案例】**Các trường hợp sản xuất của LLM A/B 测试 năm 2026:(1) 聊天机器人奖励模型变体+70% đối thoại长度、+30% 留存率;(2) Nextdoor AI 主题行实验奖励函数优化后 +1% CTR;(3) Khan Academy Khanmigo在延迟对数学准确率轴上代;;平台选择:Statsig(2025 年 9 月被 OpenAI以 $1.1B 收购) 全合一;GrowthBook开源、仓库原生、Bayesian + Frequentist + Sequential engine;;

Bạn đã điều chỉnh một lời nhắc hệ thống. Nó cảm thấy tốt hơn. Bạn gửi nó. Thay đổi chuyển đổi bằng tiếng ồn. Bạn đổ lỗi cho các thước đo. hoặc bạn gửi một mô hình mới và chuyển đổi không di chuyển  mô hình đã xuống cấp hoặc thay đổi quá nhỏ để phát hiện? Bạn không biết, bởi vì bạn đã gửi mà không có A / B.

Các điểm Evals trả lời liệu mô hình có thể thực hiện một nhiệm vụ trên một bộ có nhãn hay không. Họ không trả lời liệu người dùng có thích đầu ra hay không. Chỉ một thí nghiệm trực tuyến được kiểm soát trả lời điều đó, và chỉ khi thí nghiệm có đủ sức mạnh, kiểm soát cho không xác định và sửa chữa cho nhiều so sánh.

## Khái niệm cốt lõi

### Các thử nghiệm Evals vs A/B

**Evals** offline, set được dán nhãn, thẩm phán (rubic hoặc LLM-as-judge hoặc con người).

**A/B test** trực tuyến, người dùng trực tiếp, ngẫu nhiên. Phản ứng: "Phác thức mới có di chuyển các métric cấp người dùng quan trọng không?"

Cả hai đều cần thiết. Evals bắt hồi phục trước khi tiếp xúc; A / B xác nhận tác động của sản phẩm sau đó.

### Điều gì để kiểm tra

1. **Prompt engineering** định dạng, cấu trúc hệ thống-giải pháp, ví dụ.
2. **Model selection** GPT-4 vs GPT-3.5-Turbo vs Llama-OSS. Métric: độ chính xác (các nhiệm vụ) + chi phí / yêu cầu + độ trễ P99.
3. **Generation parameters** nhiệt độ, top-p, max_tokens.

### CUPED  Giảm biến số

> **【中文解读】**CUPED (CUPED) là một công nghệ giảm chênh lệch quan trọng trong thử nghiệm A/B. Nguyên tắc này là quay lại khoảng cách trong thử nghiệm trước khi thử nghiệm sau khi thử nghiệm.

Các thí nghiệm được kiểm soát sử dụng dữ liệu trước thí nghiệm. Khác lại sự khác biệt trước giai đoạn trước khi so sánh sau giai đoạn. Giảm sự khác biệt điển hình: 30-70%.

Thực hiện: cả Statsig và GrowthBook thực hiện.

### Kiểm tra theo trình tự

A / B cổ điển giả định kích thước mẫu cố định. Các thử nghiệm theo dõi ("peek-and-decide") kiểm soát tỷ lệ dương tính sai dưới sự nhìn lặp lại. Các thủ tục theo dõi luôn hợp lệ (mSPRT, chuỗi sự tin tưởng của Howard) cho phép bạn dừng sớm về người chiến thắng rõ ràng.

### Các sửa đổi so sánh nhiều lần

Tiến hành 20 thử nghiệm A / B với sự tự tin 95% tạo ra một dương tính sai tình cờ.

### SRM  tỷ lệ mẫu không phù hợp

Hash phân bổ ngẫu nhiên người dùng thành biến thể. Nếu phân chia 50/50 cung cấp 47/53, một cái gì đó bị hỏng  SRM kiểm tra đánh dấu nó. Cả hai nền tảng thực hiện.

### Statsig vs GrowthBook

> **【拓展：Statsig vs GrowthBook 选型】**Statsig vs GrowthBook của năm 2026  chọn lựa đối với:Statsig 2025 tháng 9 năm được OpenAI mua lại với $1.1B, là toàn bộ hợp nhất của SaaS, các biểu tượng + 实验分析 + 可观测性),内置序贯检查和CUPED, phù hợp với những người muốn捆绑 sản phẩm của nhóm.

**Statsig**- Có thể là:
- Được mua bởi OpenAI với giá 1,1 tỷ USD (Tháng 9 năm 2025).
- Kiểm tra theo trình tự, CUPED, người sống sót.
- Tất cả trong một: cờ đặc trưng + thí nghiệm + khả năng quan sát.
- Đơn vị thích hợp nhất: nhóm đã muốn một sản phẩm được gói, không quan tâm đến quyền sở hữu của OpenAI.

**GrowthBook**- Có thể là:
- Open-source (MIT); warehouse-native (đọc trực tiếp từ Snowflake/BigQuery/Redshift).
- Nhiều động cơ: Bayesian, Frequentist, Sequential.
- CUPED, SRM, Bonferroni, BH sửa chữa.
- Self-host hoặc quản lý đám mây.
- Tích hợp tốt nhất: cửa hàng kho SQL, nhóm dữ liệu kiểm soát lớp mét, muốn OSS.

### Không quyết định nghĩa làm phức tạp quyền lực

Một số tính toán năng lượng truyền thống giả định các quan sát IID. Với LLM không xác định, kích thước mẫu hiệu quả thấp hơn danh nghĩa.

### Kết quả thực tế của trường hợp

- Phân biến mô hình thưởng chatbot: + 70% chiều dài cuộc trò chuyện, + 30% lưu giữ.
- Các dòng chủ đề tiếp theo: +1% CTR sau khi tinh chỉnh chức năng thưởng.
- Khan Academy Khanmigo: giao dịch trễ lặp lại so với độ chính xác toán học.

### Phản ứng: vận chuyển trên vibes

> **【拓展：LLM 非确定性对 A/B 测试的影响】**Phân tích thống kê của A / B kiểm tra ảnh hưởng. cùng một gợi ý tạo ra các đầu ra khác nhau, sức mạnh truyền thống  tính toán giả thuyết IID  quan sát giá trị. Trong LLM không chắc chắn, lượng mẫu hiệu quả thấp hơn giá trị danh tính  cần phải được nhân lượng mẫu cần thiết là 1.3-1.5x như một biên giới an toàn.

Mỗi kỹ sư cấp cao có thể đặt tên một tính năng được vận chuyển bởi vì "nó cảm thấy tốt hơn" mà không có A / B. Hầu hết các số liệu sản phẩm đã trở lại mà nhóm không nhận thấy trong nhiều tháng. A / B là chức năng buộc.

### Những con số mà bạn nên nhớ

- Statsig được OpenAI mua lại: $1.1B, tháng 9 năm 2025.
- GrowthBook: mã nguồn mở MIT; Bayesian + Frequentist + Sequential.
- Giảm biến biến số CUPED: 30-70%.
- LLM không xác định → +30-50% buffer kích thước mẫu.

## Hãy sử dụng nó để thực hiện
```figure
mx-sequential-test
```

## Sử dụng nó

`code/main.py`mô phỏng một thử nghiệm A / B theo trình tự với ranh giới cố định và theo trình tự. cho thấy các thứ tự cho phép bạn dừng sớm.

> `code/main.py`mô phỏng một thử nghiệm A / B theo trình tự với ranh giới cố định và theo trình tự. cho thấy các thứ tự cho phép bạn dừng sớm.

> `code/main.py`mô phỏng một thử nghiệm A / B theo trình tự với ranh giới cố định và theo trình tự. cho thấy các thứ tự cho phép bạn dừng sớm.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-ab-plan.md`. Với sự thay đổi tính năng, tải trọng công việc, đường cơ sở, chọn nền tảng, cổng, kích thước mẫu.

> 本课产 出 `outputs/skill-ab-plan.md`. Với sự thay đổi tính năng, tải trọng công việc, đường cơ sở, chọn nền tảng, cổng, kích thước mẫu.

## Tập luyện bài tập

1. Đi chạy`code/main.py`Đối với một nâng 5% dự kiến với chuyển đổi 3% cơ sở, kích thước mẫu nào đến 80% sức mạnh?
   Trung ngữ翻译:运行 `code/main.py`❖ Dự kiến 5% tăng trưởng, cơ sở 3% tỷ lệ chuyển đổi, cần bao nhiêu lượng mẫu?
2. Chọn Statsig hoặc GrowthBook cho khách hàng được điều chỉnh bởi chăm sóc sức khỏe tại địa điểm.
   Trung ngữ翻译:为医疗保健监管的本地部署客户选择 Statsig 或 GrowthBook。
3. Thiết kế một A/B để thử nghiệm GPT-4 so với GPT-3.5 trên chi phí cho mỗi vé được giải quyết.
   Trung ngữ翻译:设计一个在每解决工单成本上测试 GPT-4 vs GPT-3.5 的 A/B.
4. Canary của bạn qua nhưng A/B cho thấy chuyển đổi -1,2%.
   Trung ngữ翻译:你的金丝雀通过但A/B 显示 -1.2% 转换率──你上线吗?写出解释──
5. Sử dụng CUPED cho một giai đoạn trước với 60% sự khác biệt của bài viết.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Eval | "offline test" | Labeled-set evaluation of model capability |
| A/B test | "experiment" | Live randomized comparison on users |
| CUPED | "variance reduction" | Pre-period regression to reduce variance |
| Sequential test | "peek-ok test" | Always-valid procedure allowing early stop |
| Multiple comparison | "the family error" | Running many tests inflates false positives |
| Bonferroni | "tight correction" | Divide α by number of tests |
| Benjamini-Hochberg | "BH FDR" | False-discovery-rate control, less conservative |
| SRM | "bad split" | Sample ratio mismatch; assignment bug |
| Statsig | "OpenAI owned" | Commercial all-in-one, acquired 2025 |
| GrowthBook | "the OSS one" | MIT warehouse-native platform |
| mSPRT | "sequential probability ratio test" | Classical sequential procedure |

## Xem thêm 延伸阅读

- [GrowthBook — How to A/B Test AI](https://blog.growthbook.io/how-to-a-b-test-ai-a-practical-guide/)
- [Statsig — Beyond Prompts: Data-Driven LLM Optimization](https://www.statsig.com/blog/llm-optimization-online-experimentation)
- [Statsig vs GrowthBook comparison](https://www.statsig.com/perspectives/ab-testing-feature-flags-comparison-tools)
- [Deng et al. — CUPED](https://www.exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf)
- [Howard — Confidence Sequences](https://arxiv.org/abs/1810.08240)
