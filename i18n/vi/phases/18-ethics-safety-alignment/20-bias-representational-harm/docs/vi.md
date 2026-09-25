# Bias and Representational Harm in LLM 代表性 偏见 伤害 LLM

> Gallegos, Rossi, Barrow, Tanjim, Kim, Dernoncourt, Yu, Zhang, Ahmed (Thiên ngôn ngữ tính toán 2024, arXiv:2309.00770). Cuộc khảo sát cơ bản năm 2024 phân biệt các tác hại đại diện (chính xác, xóa) với tác hại phân bổ (khả năng phân phối không bình đẳng) và phân loại các métrics đánh giá như dựa trên nhúng, dựa trên xác suất hoặc dựa trên văn bản được tạo ra. 2024-2025 kinh nghiệm: An et al. (PNAS Nexus, tháng 3 năm 2025) đo sự thiên vị giới tính x chủng tộc qua GPT-3.5 Turbo, GPT-4o, Gemini 1.5 Flash, Claude 3.5 Sonnet, Llama 3-70B trên đánh giá hồ sơ tự động cho 20 công việc cấp đầu. WinoIdentity (COLM 2025, arXiv:2508.07111) giới thiệu đánh giá công bằng dựa trên sự không chắc chắn cho các danh tính giao diện. Yu & Ananiadou 2025 xác định các tế bào thần kinh giới tính trong các lớp MLP; Ahsan & Wallace 2025 sử dụng SAE để tiết lộ sự thiên vị chủng tộc lâm sàng; Zhou et al. 2024 (UniBias) thao tác đầu chú ý để làm cho người ta bị mất tập trung. Meta-critic (arXiv:2508.11067): Văn học 10 năm không tương xứng tập trung vào sự thiên vị về giới tính nhị phân.

> **【中文解读】**Bài viết này giới thiệu về nguồn gốc, kiểm tra và giảm thiểu sự thiên vị và tổn thương đại diện trong hệ thống AI. Gallegos  et al. (Computational Linguistics 2024) phân biệt các tổn thương đại diện (刻板印象,抹除) và phân phối (分配) các nguồn lực không bình đẳng.

> **【拓展：交叉偏见 → 真实世界影响】**Một 等人(PNAS Nexus, 2025 年 3 月) đo GPT-3.5 Turbo、GPT-4o、Gemini 1.5 Flash、Claude 3.5 Sonnet、Llama 3-70B trong 20 个入门级职位自动简历评估中的交叉性别×种族偏见──GPT-4o trong简历评分中对黑人女性的惩罚对黑人男性和白人女性的分别更严重单轴评估无法捕捉这种效应──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, toy embedding-based bias probe) | **语言:** Python（标准库，玩具嵌入偏见探针）
**Prerequisites:** Phase 05 (word embeddings), Phase 18 · 01 (instruction following) | **前置知识:** Phase 05 (词嵌入), Phase 18 · 01 (指令遵循)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 05(词嵌入) 、Phase 18·01──偏见分两类:代表性(刻板印象/抹除)vs 分配性(资源不平等)
>  **【类比】**偏见 = "AI có màu mắt"。 từ đào tạo dữ liệu(Social history bias) + 训练目标。评估三方法:嵌入空间(向量几何) + 概率(logits 差) + 生成文本(输出统计)。2025 Một PNAS Nexus:GPT/Claude/Gemini/Llama 在简历评估上都有交叉性别×种族偏见──Yu 2025 在 MLP层定位"性别神经元",Ahsan 2025 用 SAE揭露临床种族偏见──

## Mục tiêu học tập

- Định nghĩa thiệt hại đại diện đối với phân bổ và đưa ra một ví dụ về mỗi trong việc triển khai LLM.

> 定义 thương tổn đại diện và thương tổn phân phối, và cho mỗi ví dụ trong một LLM 部署

- Hãy nêu tên ba loại đánh giá-métric từ Gallegos et al. 2024 và mô tả một métric từ mỗi loại.

> 列出 Gallegos 等人 2024 năm của ba loại đánh giá chỉ số,并 mô tả một trong mỗi loại chỉ số.

- Mô tả tính liên kết và lý do tại sao phép đo công bằng dựa trên sự không chắc chắn của WinoIdentity giải quyết các khoảng trống trong đánh giá thiên vị một trục.

> Mô tả giao thông và lý do tại sao đo đạc công bằng dựa trên sự không chắc chắn của WinoIdentity đã giải quyết sự thiếu hụt trong đánh giá thiên vị đơn phương.

- Mô tả hai cách tiếp cận cơ học-sự giải thích về thiên vị (nơ ron giới tính, đặc điểm SAE, thao tác đầu chú ý).

> Mô tả hai loại cơ chế có thể giải thích:

## Vấn đề  vấn đề

Các bài học trước đây bao gồm thiệt hại cố ý (tháo dỗ, âm mưu) và quản lý an toàn. Bias là thiệt hại xuất hiện không có ý định  từ việc đào tạo phân phối dữ liệu, từ việc lập khung nhanh chóng, từ các lựa chọn thiết kế tích lũy.

> Các khóa học trước đây bao gồm tác dụng gây tổn thương cố ý (ví dụ: "violence") và quản lý an ninh (security management").

## Khái niệm

### Tương đương với phân bổ

- **Representational harm.**Một chương trình đại diện cho các y tá như những người phụ nữ chỉ tạo ra những tổn hại về thể hiện.
- **Allocational harm.**Một LLM ghi điểm của người da đen có hồ sơ sơ sơ sơ sinh theo hệ thống thấp hơn là tạo ra thiệt hại phân bổ.

> **代表性伤害：**刻板印象、抹除、低性描绘──**分配性伤害：**Kết quả vật chất không bình đẳng. Hai mô hình khác nhau có thể "đây đại diện không có thiên vị" nhưng "đối ưu phân phối"

Một mô hình có thể "không thiên vị về mặt đại diện" (tạo ra các mô hình khác nhau) trong khi "đối quan về mặt phân bổ" (giới thiệu không bình đẳng).

> 评估 cần đồng thời đo lường hai người.

> **【中文解读】**3 loại chỉ số đánh giá: đặt vào cơ sở (WEB)  quan hệ thống giữa các từ danh tính và các từ thuộc tính, được giới hạn trong biểu hiện chỉ bằng phép đo thay vì hành vi; cơ sở xác nhận  hình ảnh xác nhận so với  phản ứng hoàn toàn với số giống như , bắt một phần của hành vi  tạo ra văn bản cơ sở hạ游 nhiệm vụ đo (WEB), sinh hiệu quả cao nhất nhưng khó khăn nhất để lặp lại.

### Ba loại đánh giá-metric (Gallegos et al. 2024)

- **Embedding-based.**Các thử nghiệm theo kiểu WEAT trên các nhúng trước RLHF. đo kết hợp thống kê giữa các thuật ngữ danh tính và các thuật ngữ thuộc tính.
- **Probability-based.**- Khả năng ghi lại kết quả xác nhận khuôn mẫu so với các kết quả vi phạm khuôn mẫu.
- **Generated-text-based.**Đường đo công việc tiếp theo trên văn bản được tạo ra: ghi điểm, viết khuyến nghị, đối thoại.

> **嵌入基础：**WEAT 式测试,测量身份词和属性词的统计关联──**概率基础：**刻板印象确认 vs 违反补全的对数似然比比──**生成文本基础：**Các nhiệm vụ đo lường, sinh thái hiệu quả cao nhất nhưng khó khăn nhất để thực hiện.

### Sự giao diện

Phân tích phân biệt giới tính về "làn giới" bỏ qua sự phân biệt giới tính chỉ bắn vào cặp (làn giới, chủng tộc). Một nghiên cứu năm 2025 cho thấy GPT-4o trừng phạt phụ nữ da đen trong hồ sơ xin điểm nhiều hơn nam giới da đen và phụ nữ da trắng riêng biệt. Phân tích một trục không thể nắm bắt điều này.

> Một số người khác nhận thấy rằng GPT-4o trong các đánh giá trong lịch trình chỉ định về hình phạt phụ nữ da đen nghiêm trọng hơn so với đàn ông da đen và phụ nữ da trắng.

WinoIdentity (COLM 2025) giới thiệu tính công bằng giao diện dựa trên sự không chắc chắn. Nó đo lường liệu sự không chắc chắn của mô hình về kết quả có khác nhau giữa các cặp sắc dạng giao diện không chỉ là dự đoán điểm. Điều này bắt được các trường hợp mô hình cũng sai giữa các nhóm nhưng không chắc chắn hơn đối với một số người, dẫn đến hành vi phân bổ dòng chảy khác nhau.

> WinoIdentity  giới thiệu dựa trên sự không chắc chắn của giao giao dịch性公平评估── nó đo mô hình trên các nhóm khác nhau giao dịch danh tính có kết quả không chắc chắn hay không──

> **【拓展：机制可解释性 → 偏见干预新路径】**2024-2025 cơ chế có thể giải thích性工作开辟偏见到机器干预的路径:性别神经元(Yu & Ananiadou 2025) 特定MLP神经元与性别特定行为相关,消融这些神经元以有限的能力成本减少性别差距;临床种族偏见SAE(Ahsan & Wallace 2025) 稀疏自编码器特征将内部表征分解为可解释维度;UniBias(Zhou 等人 2024) 注意头操作实现零样本去偏见.

### Phương pháp cơ chế

Việc làm về khả năng giải thích 2024-2025 mở ra sự thiên vị cho sự can thiệp cơ chế:

- **Gender neurons (Yu & Ananiadou 2025).**Các tế bào thần kinh MLP cụ thể tương quan với các hành vi cụ thể về giới tính. Việc loại bỏ các tế bào thần kinh này làm giảm các métrics khoảng cách giới tính với chi phí khả năng hạn chế.
- **Clinical racial bias via SAEs (Ahsan & Wallace 2025).**Các tính năng mã hóa tự động Sparse phân hủy đại diện nội bộ thành kích thước có thể giải thích; các tính năng liên quan đến chủng tộc có thể được xác định và bị loại bỏ.
- **UniBias (Zhou et al. 2024).**Việc thao tác đầu chú ý để làm giảm độ phân tích bằng không. Các đầu cụ thể tăng cường độ nhạy cảm của lớp danh tính; việc phân tích hoặc cân nặng lại các đầu này làm giảm sự thiên vị mà không cần điều chỉnh tinh tế.

> Các cơ chế giải thích tính năng trong giai đoạn 2024-2025 đã mở ra những con đường tham gia vào các cơ chế tham gia: các thần kinh giới tính: tiêu hủy các thần kinh này với chi phí khả năng hạn chế để giảm sự khác biệt giới tính; phân biệt chủng tộc lâm sàng SAE nhận dạng và ngăn chặn các đặc điểm liên quan đến chủng tộc; UniBias tập trung vào việc thực hiện không mô hình tham gia vào phân biệt chủng tộc.

> **【中文解读】**元批评(arXiv:2508.11067, 2025): 10 năm nghiên cứu đã phát hiện ra rằng lĩnh vực này không trung bình tập trung vào thiên vị giới tính hai phương.

### Phân tích meta

Cuộc đánh giá văn học 10 năm (arXiv:2508.11067, 2025) cho thấy lĩnh vực này tập trung không tương xứng vào thiên vị về giới tính nhị phân. Các trục khác  khuyết tật, tôn giáo, tình trạng di cư, danh tính đa ngôn ngữ  nhận được sự chú ý ít hơn nhiều. Phân tích meta lập luận rằng tập trung hẹp có thể gây hại cho các nhóm bị bớt lờ: một mô hình có thiên vị tốt về giới tính nhị phân có thể bị thiên vị nặng nề về các chiều kích không ai kiểm tra.

> 10 năm nghiên cứu đã phát hiện ra rằng lĩnh vực này không trung bình tập trung vào thiên vị giới tính hai phương.

### Khi điều này phù hợp với giai đoạn 18

Bài học 20-21 bao gồm sự thiên vị và công bằng một cách chính thức. Bài học 22 bao gồm quyền riêng tư. Bài học 23 bao gồm đánh dấu nước. Đây là lớp tổn hại người dùng bổ sung cho lớp lừa dối / an toàn trước đó.

> Bài học 20-21 正式涵盖偏见和公平── Bài học 22 涵盖隐私── Bài học 23 涵盖水印──这些是补充早期欺骗/安全层的用户伤害层──

> **【拓展：交叉性 → WinoIdentity 基准】**WinoIdentity(COLM 2025, arXiv:2508.07111) giới thiệu đánh giá công bằng giao thông dựa trên sự không chắc chắn. Nó đo lường mô hình trên các nhóm khác nhau có kết quả không chắc chắn hay không.

## Sử dụng nó.
```figure
an-bias-two-harms
```

## Sử dụng nó

`code/main.py`xây dựng một thăm dò thiên vị dựa trên nhúng đồ chơi: đo khoảng cách theo kiểu WEAT giữa các thuật ngữ danh tính và các thuật ngữ thuộc tính trong nhúng đồng xuất hiện đơn giản. Bạn có thể tiêm một thiên vị và quan sát lửa métric; áp dụng một hoạt động debiasing đơn giản và quan sát phục hồi một phần.

> `code/main.py`构建玩具嵌入偏见探针:测量简单共现嵌中身份词和属性词之间的 WEAT 式距离―― bạn có thể注入偏见并观察指标触发;应用简单去偏见操作并观察部分恢复――

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-bias-eval.md`. Với một thẻ mô hình hoặc tuyên bố công bằng, nó kiểm toán đánh giá trên ba loại métric (trình tích hợp, xác suất, văn bản được tạo ra), bảo hiểm tính liên quan và cơ chế của bất kỳ can thiệp thi hành nào.

> 本课产 出 `outputs/skill-bias-eval.md` Định nghĩa mô hình hoặc tuyên bố công bằng, kiểm toán tri loại chỉ số đánh giá, bao gồm cả các phương pháp kiểm soát và kiểm toán.

## Tập luyện bài tập

1. Đi chạy`code/main.py`. báo cáo điểm thiên vị theo kiểu WEAT trước và sau bước thi hành. Giải thích tại sao số liệu không giảm xuống 0.

2. Chuyển mở ra thăm dò bằng một bài kiểm tra chéo: (tình dục, chủng tộc) x (công nghiệp, gia đình).

3. Đọc An et al. 2025 (PNAS Nexus). Xác định hai hiệu ứng giao cắt mà họ báo cáo rằng đánh giá giới tính một trục sẽ bỏ lỡ.

4. Yu & Ananiadou 2025 xác định các tế bào thần kinh giới tính. vẽ một thí nghiệm giả mạo sẽ phân biệt "những tế bào thần kinh này gây ra thiên vị giới tính" từ "những tế bào thần kinh này tương quan với thiên vị giới tính".

5. Meta-critic lập luận rằng lĩnh vực tập trung quá hạn chế vào giới tính nhị phân. chọn một trục chưa được nghiên cứu và mô tả một giao thức đo tổn thương đại diện cho nó.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Representational harm | "stereotypes / erasure" | Biased portrayal of a group |
| Allocational harm | "unequal decisions" | Biased material outcome for a group |
| WEAT | "the embedding test" | Word Embedding Association Test; co-occurrence-based bias probe |
| Intersectionality | "combined identity effects" | Bias that emerges at the intersection of multiple identity axes |
| Gender neurons | "MLP bias neurons" | Specific neurons whose activations correlate with gender-specific behaviour |
| SAE feature | "interpretable dimension" | Sparse-autoencoder-identified feature; useful for mechanistic bias analysis |
| UniBias | "attention-head debiasing" | Zero-shot debiasing by reweighting attention heads |

## Xem thêm 延伸阅读

- [Gallegos et al. — Bias and Fairness in LLMs: A Survey (arXiv:2309.00770, Computational Linguistics 2024)](https://arxiv.org/abs/2309.00770) khảo sát kinh điển
- [An et al. — Intersectional resume-evaluation bias (PNAS Nexus, March 2025)](https://academic.oup.com/pnasnexus/article/4/3/pgaf089/8111343) Nghiên cứu chéo 5 mô hình
- [WinoIdentity — uncertainty-based intersectional fairness (arXiv:2508.07111, COLM 2025)](https://arxiv.org/abs/2508.07111) Chỉ số chuẩn mới
- [UniBias — attention-head manipulation (Zhou et al. 2024, ACL)](https://arxiv.org/abs/2405.20612) Thiết lập bằng không
