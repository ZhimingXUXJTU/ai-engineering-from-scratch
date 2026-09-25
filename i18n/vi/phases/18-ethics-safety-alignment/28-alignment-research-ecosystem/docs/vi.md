# Nghiên cứu sinh thái phù hợp MATS, Redwood, Apollo, METR

> Năm tổ chức xác định lớp nghiên cứu không phải trong phòng thí nghiệm năm 2026. MATS (ML Alignment & Theory Scholars): 527+ nhà nghiên cứu kể từ cuối năm 2021, 180+ bài báo, 10K+ trích dẫn, h-index 47; mùa hè 2024 nhóm được thành lập như 501 ((c) ((3) với ~ 90 học giả và 40 cố vấn; 80% cựu sinh viên trước năm 2025 làm việc về an toàn / an ninh với 200+ tại Anthropic, DeepMind, OpenAI, UK AISI, RAND, Redwood, METR, Apollo. Nghiên cứu Redwood: phòng thí nghiệm sắp xếp ứng dụng được thành lập bởi Buck Shlegeris; giới thiệu AI Control (Lớp học 10); hợp tác với AISI Anh về các trường hợp an toàn kiểm soát. Nghiên cứu Apollo: đánh giá kế hoạch trước khi triển khai cho các phòng thí nghiệm biên giới; tác giả của In-Context Scheming (Dạy 8) và Towards Safety Cases for AI Scheming. METR (Model Evaluation and Threat Research): đánh giá khả năng dựa trên nhiệm vụ, nghiên cứu về khung thời gian nhiệm vụ tự trị; "Thông tố chung của các chính sách an toàn AI biên giới" so sánh các khung thí nghiệm. Eleos AI Research: đánh giá trước khi triển khai mô hình phúc lợi (Dạy học 19); tiến hành đánh giá phúc lợi của Claude Opus 4.

> **【中文解读】**Chương trình này giới thiệu về các cơ quan nghiên cứu trong lĩnh vực nghiên cứu ̋AI an toàn ̋, luận văn và dự án nguồn mở ̋.

> **【拓展：外部评估 → 利益冲突缓解】**单一来源评估不可靠: phòng thí nghiệm đánh giá mô hình của riêng mình có xung đột lợi ích cấu trúc. Các nhà đánh giá bên ngoài có thể phát hiện và chứng minh các mô hình thất bại của phòng thí nghiệm.

**Type:** Learn | **类型:** 学习
**Languages:** none | **语言:** 无
**Prerequisites:** Phase 18 · 01-27 (prior Phase 18 lessons) | **前置知识:** Phase 18 · 01-27（先前 Phase 18 课程）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**本节是阶段18的"机构地图"整合 01-27所有内容──五大非实验室对齐研究机构──
>  **【类比】**Đối với齐研究生态 = "AI 安全的人才输送网"――MATS(527+ 学者,h-index 47,80% 在 Anthropic/DeepMind/OpenAI等做安全);Redwood(Buck Shlegeris 创立,AI Control 议程 Bài 10);Apollo(预部署策略评估,Lớp 8 作者);METR(任务时间线评估 Bài 21/Phase 15·21);Eleos AI模型福利 Bài 19);; Mỗi tổ chức đối phó với một số chủ đề của giai đoạn 18;;

## Mục tiêu học tập

- Xác định năm tổ chức của hệ sinh thái nghiên cứu không phải trong phòng thí nghiệm và sản lượng cốt lõi của chúng.
- Mô tả quy mô của MATS (những học giả, bài báo, chỉ số h) và vai trò của nó như một đường ống tài năng.
- Mô tả chương trình nghị sự kiểm soát AI của Redwood và quan hệ đối tác của nó với AISI của Anh.
- Mô tả phương pháp đánh giá dựa trên nhiệm vụ của METR.

> 识别非实验室对齐研究生态系统的五个组织及其核心产品――描述 MATS规模及其作为人才管道的角色――描述 Redwood's AI 控制议程和英国 AISI合作――描述 METR's task-based assessment method――

## Vấn đề  vấn đề

Các phòng thí nghiệm biên giới (Học 18) sản xuất đánh giá an toàn nội bộ và xuất bản kết quả được chọn. Hệ sinh thái bên ngoài phòng thí nghiệm là nơi đánh giá được xác nhận, nơi các chế độ thất bại mới được phát hiện lần đầu tiên, và nơi đào tạo tài năng. Hiểu hệ sinh thái giúp giải thích những phát hiện nghiên cứu nào được tin cậy bởi ai.

> Phòng thí nghiệm phía trước tạo ra đánh giá an toàn bên trong và phát hành kết quả được chọn lựa. Hệ sinh thái bên ngoài phòng thí nghiệm là nơi đánh giá được chứng minh, mô hình thất bại mới được phát hiện lần đầu tiên và nhân tài được đào tạo.

## Khái niệm

> **【中文解读】**Kích thước và ảnh hưởng của MATS: từ cuối năm 2021 527+ nghiên cứu viên, 180+ bài luận, 10K+ 引用,h-index 47。2024年夏季:90 名学者 + 40 名导师, đăng ký là 501(c) ) ) 职业成果: khoảng 80% của năm 2025 校友从事安全/安全工作,200+ 人在人类的•DeepMind、OpenAI、英国AISI、RAND、Redwood、METR、Apollo。

### MATS (ML Alignment & Theory Scholars)

Bắt đầu vào cuối năm 2021. Chương trình hướng dẫn nghiên cứu; các học giả dành 10-12 tuần với một nhà nghiên cứu cấp cao về một vấn đề sắp xếp cụ thể.

> 2021 年底开始──研究导师项目;学者在高级研究员指导下花 10-12 周研究特定对齐问题──

Scale (2026):
- 527+ nhà nghiên cứu kể từ khi thành lập.
- 180+ bài báo được xuất bản.
- 10K + trích dẫn.
- H-index 47.
- Mùa hè 2024: 90 học giả + 40 cố vấn; được thành lập như là 501 ((c) ((3).

> 规模:527+ 研究员、180+ 论文、10K+ 引用、h-index 47。

Kết quả nghề nghiệp: ~ 80% cựu sinh viên trước năm 2025 đang làm việc về an toàn / an ninh. 200+ tại Anthropic, DeepMind, OpenAI, UK AISI, RAND, Redwood, METR, Apollo.

> Kết quả nghề nghiệp: Khoảng 80% sinh viên trước năm 2025 làm việc an ninh / an ninh,200+ người trong tổ chức chính.

> **【拓展：研究风格差异 → 组织定位】**Phong cách của Redwood: mô hình đe dọa cụ thể, tình huống tồi tệ nhất đối với người dùng, quy định cụ thể của bài kiểm tra có thể áp lực. Phong cách của Apollo: thiết lập đại diện để đánh giá tình huống có thể xuất hiện trong tình huống lừa đảo, phân giải trí mô hình của các nghiên cứu được tìm thấy bởi những người tin tưởng.

### Nghiên cứu gỗ đỏ

Phòng thí nghiệm sắp xếp ứng dụng. Được thành lập bởi Buck Shlegeris. Ông giới thiệu chương trình nghị sự kiểm soát AI (Dạy 10) hợp tác với AISI của Anh về các trường hợp an toàn kiểm soát. Ông tư vấn cho DeepMind và Anthropic về thiết kế đánh giá.

> 应用对齐实验室──由 Buck Shlegeris 创立──引入 AI 控制议程(Lớp 10)──与英国AISI 合作控制安全案例──

Các bài báo Canonical: Greenblatt, Shlegeris et al., "AI Control" (arXiv:2312.06942, ICML 2024); Alignment Faking (Greenblatt, Denison, Wright et al., arXiv:2412.14093, chung với Anthropic).

Thiết kế: mô hình đe dọa cụ thể, đối thủ tồi tệ nhất, các giao thức cụ thể có thể được kiểm tra bằng căng thẳng.

> 风格: Mô hình đe dọa cụ thể, tình huống tồi tệ nhất đối với người dùng, thỏa thuận cụ thể của bài kiểm tra có thể áp lực.

### Nghiên cứu Apollo

Đánh giá kế hoạch trước khi triển khai cho các phòng thí nghiệm biên giới. Tác giả In-Context Scheming (Lớp 8, arXiv:2412.04984). Đối tác về sự hợp tác đào tạo chống kế hoạch OpenAI năm 2025.

> Ưu điểm của dự kiến triển khai của phòng thí nghiệm.

Thiết kế: đánh giá thiết lập cơ quan nơi có thể xuất hiện lừa đảo; phân hủy ba trụ (không phù hợp, hướng mục tiêu, nhận thức tình huống).

> 风格: Trình lập đại lý đánh giá trong tình huống lừa đảo có thể xuất hiện; 三支柱分解──

### METR (Phân tích đánh giá mô hình và nghiên cứu về mối đe dọa)

Đánh giá khả năng dựa trên nhiệm vụ. Nghiên cứu thời gian hoàn thành nhiệm vụ tự trị. "Các yếu tố chung của Chính sách an toàn AI biên giới" (metr.org/common-elements, 2025) so sánh các khung thí nghiệm.

> 基于任务能力评估――自主任务完成时间范围研究――"Điều chung của Chính sách an toàn AI biên giới"比较实验室框架――

Đồng tác giả của bản phác thảo trường hợp an toàn với Apollo.

Thiết kế: đánh giá nhiệm vụ theo đường chân trời dài, đo khả năng thực nghiệm, tổng hợp khung.

> 风格:长程任务评估、经验能力测量、框架综合──

### Eleos AI Research

Các mô hình đánh giá phúc lợi trước khi triển khai. thực hiện đánh giá phúc lợi Claude Opus 4 được ghi lại trong phần 5.3 của thẻ hệ thống. cung cấp kiểm tra phương pháp bên ngoài cho các tuyên bố liên quan đến phúc lợi trong Bài 19.

> **【中文解读】**生态系统流动:MATS 训练研究员 → 毕业生去人类、DeepMind、OpenAI(实验室安全团队) hoặc Redwood、Apollo、METR、Eleos(外部评估)→ 外部评估员与实验室和英国 AISI / CAISI 合作 → 出版回 MATS 给下一期──人才管道是这个生态系统的命脉──

### Dòng chảy

MATS đào tạo các nhà nghiên cứu. Sinh viên tốt nghiệp đi đến Anthropic, DeepMind, OpenAI (nhóm an toàn phòng thí nghiệm) hoặc đến Redwood, Apollo, METR, Eleos (học định bên ngoài). Các nhà đánh giá bên ngoài hợp tác với các phòng thí nghiệm và với AISI / CAISI của Anh. Các ấn phẩm cung cấp hệ sinh thái trở lại MATS cho nhóm tiếp theo.

> MATS  đào tạo nghiên cứu viên. 毕业生 đến phòng thí nghiệm nhóm an ninh hoặc tổ chức đánh giá bên ngoài.

### Tại sao lớp này quan trọng

Các đánh giá từ một nguồn không đáng tin cậy: các phòng thí nghiệm đánh giá các mô hình của riêng họ có một xung đột lợi ích cấu trúc. Các nhà đánh giá bên ngoài có thể nâng cao và xác nhận các chế độ thất bại mà phòng thí nghiệm có thể báo cáo thấp. Bài báo của 2024 Sleeper Agents (Lớp 7) là Anthropic + Redwood; Alignment Faking là Anthropic + Redwood; In-Context Scheming là Apollo; Anti-Scheming là Apollo + OpenAI. Cơ cấu đa cơ quan là kiểm soát chất lượng.

> 单源评估不可靠: phòng thí nghiệm đánh giá mô hình của riêng mình có xung đột lợi ích cấu trúc.

### Khi điều này phù hợp với giai đoạn 18

Bài học 7-11 đề cập đến công việc Redwood và Apollo; Bài học 18 đề cập đến so sánh khung METR; Bài học 19 đề cập đến Eleos. Bài học 28 là bản đồ tổ chức rõ ràng cho hệ sinh thái mà phần còn lại của giai đoạn dựa trên.

> **【拓展：外部评估者 → 多机构交叉验证】**Bài luận quan trọng năm 2024 cho thấy giá trị của sự hợp tác đa cơ quan: tiềm năng Cơ quan là Anthropic + Redwood; đối với nhau giả mạo là Anthropic + Redwood; trên dưới đây chiến lược là Apollo; chống chiến lược là Apollo + OpenAI;. Mỗi nhà đánh giá bên ngoài mang lại phong cách và quan điểm khác nhau về phương pháp.

## Sử dụng nó.
```figure
sae-features
```

## Sử dụng nó

Không có mã. Đọc "Các yếu tố chung của các chính sách an toàn AI biên giới" của METR như một ví dụ về cách tổng hợp bên ngoài thêm giá trị vào công việc chính sách nội bộ trong phòng thí nghiệm.

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-ecosystem-map.md`. Với yêu cầu hoặc đánh giá về sự phù hợp, nó xác định tổ chức, địa điểm xuất bản, phong cách phương pháp và kiểm tra chéo đối với các tổ chức đối tác được biết đến.

## Tập luyện bài tập

1. Chọn một bài báo từ Bài học 7-15 và xác định các tổ chức liên quan.

2. Đọc "Các yếu tố chung của các chính sách an toàn AI biên giới" của METR.

3. Kết quả nghề nghiệp MATS là ~ 80% an toàn / an toàn. tranh luận liệu áp lực lựa chọn này có thích ứng (đào tạo lĩnh vực) hoặc thiên vị (đánh lọc các vị trí không chính xác).

4. Redwood và Apollo đều làm việc kiểm soát / kế hoạch nhưng với phong cách khác nhau. chọn một chế độ thất bại và mô tả cách mỗi người sẽ điều tra nó.

5. Eleos AI là tổ chức phúc lợi mô hình thuần túy duy nhất. Thiết kế một tổ chức thứ hai giả thuyết tập trung vào một câu hỏi phúc lợi khác nhau (tự do nhận thức, thể hiện robot, vv) và diễn tả phương pháp của nó.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| MATS | "the mentorship program" | ML Alignment & Theory Scholars; 527+ researchers since 2021 |
| Redwood Research | "the control lab" | Applied alignment; AI Control authors; UK AISI partner |
| Apollo Research | "the scheming evals" | Pre-deployment scheming evaluations for frontier labs |
| METR | "the task-horizon evals" | Task-based capability evaluations; framework synthesis |
| Eleos AI | "the welfare lab" | Model-welfare pre-deployment evaluations |
| Talent pipeline | "MATS -> labs" | MATS graduates flow to Anthropic, DM, OpenAI, Redwood, Apollo, METR |
| External evaluation | "non-lab check" | Evaluation not done by the model's producer; adds credibility |

## Xem thêm 延伸阅读

- [MATS (ML Alignment & Theory Scholars)](https://www.matsprogram.org/) chương trình dạy dỗ
- [Redwood Research](https://www.redwoodresearch.org/) AI Control Paper
- [Apollo Research](https://www.apolloresearch.ai/) đánh giá kế hoạch
- [METR — Common Elements of Frontier AI Safety Policies](https://metr.org/blog/2025-03-26-common-elements-of-frontier-ai-safety-policies/) So sánh khung
- [Eleos AI Research](https://www.eleosai.org/research) Mô hình phương pháp phúc lợi
