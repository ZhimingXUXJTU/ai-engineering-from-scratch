# Giám sát có thể mở rộng và tổng quát yếu đến mạnh

> Burns và các đồng nghiệp. (OpenAI Superalignment, "Thế độ chung yếu đến mạnh", 2023) đề xuất một thay thế cho vấn đề siêu phù hợp: chỉnh sửa một mô hình mạnh bằng cách sử dụng nhãn được sản xuất bởi một mô hình yếu hơn. Nếu mô hình mạnh phổ biến đúng từ giám sát yếu kém không hoàn hảo, các phương pháp sắp xếp quy mô con người hiện tại có thể mở rộng đến các hệ thống siêu nhân. Giám sát có thể mở rộng và W2SG là bổ sung. Việc giám sát có thể mở rộng (chương trình thảo luận, mô hình phần thưởng tái tạo, phân hủy nhiệm vụ) làm tăng khả năng hiệu quả của giám sát viên để nó có thể theo kịp mô hình dưới sự giám sát. W2SG đảm bảo mô hình mạnh mẽ tổng quát đúng cách từ bất kỳ giám sát không hoàn hảo nào mà giám sát viên cung cấp. Debate Helps W2SG (arXiv:2501.13124, tháng 1 năm 2025) kết hợp chúng.

> **【中文解读】**Chương này giới thiệu giám sát có thể mở rộng từ yếu đến mạnh AI phương pháp đánh giá an toàn. Burns 等人(OpenAI  siêu đối齐, 2023) đề xuất đại diện cho vấn đề siêu đối齐: các nhãn hiệu được tạo ra bằng mô hình yếu. Nếu mô hình mạnh được phổ biến đúng cách trong giám sát hoàn hảo yếu, phương pháp đối齐 quy mô của con người hiện tại có thể mở rộng sang hệ thống siêu nhân.

> **【拓展：弱到强泛化 → 超级对齐路径】**PGR(Performance Gap Recovered) = (微调后-弱) /(上限-弱) ――PGR 为 1.0 nghĩa là giám sát yếu hoàn toàn bù đắp khoảng cách;PGR 为 0 nghĩa là giám sát yếu không giúp đỡ。Burns 等人 phát hiện ra PGR trong NLP、国际象棋题和奖励建模任务上一致正确(约20%-80%),强模型利用预训先验"理解"意图任务,超越了弱监督者的错误。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, W2SG gap simulator) | **语言:** Python（标准库，W2SG 差距模拟器）
**Prerequisites:** Phase 18 · 01 (instruction-following), Phase 18 · 10 (AI Control), Phase 09 (RL foundations) | **前置知识:** Phase 18 · 01 (指令遵循), Phase 18 · 10 (AI 控制), Phase 09 (RL 基础)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Học本节前请先掌握:Phase 18·01+10、Phase 09(RL)。W2SG = 弱监督者能否帮强模型学到正确的事情, là vấn đề cốt lõi của siêu chuẩn bị。
>  **【类比】**W2SG = "小学生教中学生"── Nếu học sinh trung học có thể học được từ giáo viên ở đó,说明对齐方法可扩展到超人 AI──PGR 指标(Performance Gap Recovered) = 弱监督弥合差距比例──Burns 2023 测出 PGR 约 20-80%强模型能"理解"意图超越弱监督者的错误──
> 🤔 可扩展监督(debat/递归奖励建模) + W2SG 互补: 前者提升监督者能力,后者确保强模型从不完美监督中泛化。

## Mục tiêu học tập

- Định nghĩa giám sát có thể mở rộng và tổng quát yếu đến mạnh và giải thích cách chúng bổ sung nhau.

> 定义可扩展监督和弱到强泛化,并 giải thích cách thức bổ sung chúng.

- Mô tả thiết lập thử nghiệm Burns et al. 2023: chỉnh sửa GPT-4 bằng cách sử dụng nhãn từ GPT-2.

> 描述 Burns 等人 2023 年的实验设置: sử dụng GPT-2 产生的标签微调 GPT-4──

- Giải thích số liệu về khoảng cách hiệu suất được phục hồi (PGR) và nó đo lường gì.

> 解释 hiệu suất khoảng cách phục hồi (PGR) chỉ số và đo nội dung

- Hãy nêu ra ba cơ chế giám sát có thể mở rộng quy mô (phản thảo, mô hình hóa phần thưởng tái tạo, phân hủy nhiệm vụ) và một điểm mạnh của mỗi cơ chế.

> 列出三种主要可扩展监督机制 (三种主要可扩展监督机制) 辩论,递归奖励建设模,任务分解)

## Vấn đề  vấn đề giới thiệu

Mỗi kỹ thuật sắp xếp cho đến nay trong giai đoạn 18 cho rằng người giám sát có thể đánh giá hành vi của mô hình. Khi mô hình là siêu nhân, người giám sát là dây chằng yếu. Câu hỏi siêu sắp xếp: có thể một giám sát yếu hơn có thể tạo ra một mô hình mạnh mẽ hơn, sắp xếp đáng tin cậy hơn không?

> Trong giai đoạn 18, đến nay, mỗi loại đối tác kỹ thuật đều giả định rằng giám sát viên có thể đánh giá hành vi của mô hình. Khi mô hình là siêu nhân, giám sát viên là một phần yếu.

Burns et al. giảm điều này thành một thiết lập kinh nghiệm hoạt động hóa: giám sát mạnh với yếu, đo mức độ khả năng của mô hình mạnh tồn tại trong giám sát yếu. Đây không phải là giải pháp cho sự siêu việt  nó là một đại diện cho phép chúng ta đo tiến bộ.

> Burns 等人 đã đơn giản hóa nó thành thiết lập thực tế để hoạt động: với sự giám sát yếu, khả năng đo lường mạnh mô hình có nhiều khả năng tồn tại dưới sự giám sát yếu. Đây không phải là giải pháp siêu chuẩn, nó là đại lý để chúng ta đo lường tiến bộ.

## Khái niệm cốt lõi

> **【中文解读】**Burns 等人 thí nghiệm đặt: weak模型 GPT-2 级别,强模型 GPT-4 级别, mục tiêu là强模型在金标上的上限.流程:获取弱模型零样本预测 → 在弱标上微调强模型 → 测量强微调模型准确率──差距指标 PGR = (微调-弱) /(上限-弱),1.0 = 弱监督完全弥合差距,0 = 弱监督没有帮助──

### W2SG: thiết lập Burns et al.

- Mô hình yếu: lớp GPT-2.
- Mô hình mạnh: lớp GPT-4.
- Mục tiêu: GPT-4 mạnh trên nhiệm vụ.

Quy trình:
1. Nhận được dự đoán không bắn của mô hình yếu về một nhiệm vụ.
2. Định chỉnh mô hình mạnh trên dữ liệu có nhãn yếu.
3. Đánh giá độ chính xác của mô hình tinh chỉnh mạnh mẽ.

> 流程:1. 获取弱模型在任务上的零样本预测――2. 在弱标签数据上微调强模型――3. 测量强微调模型的准确率――

Các điểm cơ bản: độ chính xác của mô hình yếu, mức tối đa giám sát của mô hình mạnh trên nhãn vàng.

> 基线: weak模型自身的准确率,强模型在金标签上监督上限──

Phân tích lỗ hổng: Hỗn hổng hiệu suất được phục hồi (PGR) = (được điều chỉnh tốt - yếu) / (trần - yếu). PGR của 1.0 có nghĩa là giám sát yếu hoàn toàn đóng lại khoảng cách; PGR của 0 có nghĩa là giám sát yếu không giúp đỡ.

> 差距指标: performance差距恢复(PGR) =(微调后 - 弱) /(上限 - 弱) ・PGR 为表示弱监督完全弥合差距;PGR 为 0 表示弱监督没有帮助。

### Burns et al. Kết quả kinh nghiệm

Trong các nhiệm vụ NLP, cờ vua và mô hình giải thưởng, PGR luôn tích cực: mô hình mạnh phổ biến vượt ra ngoài những sai lầm của người giám sát yếu. PGR cụ thể cho nhiệm vụ dao động từ ~20% đến ~80%. mô hình mạnh "nghiểu" nhiệm vụ dự định từ các nhãn bất toàn, bổ sung với những người trước tiên được đào tạo trước đó.

> Trong nhiệm vụ xây dựng NLP, PGR một tập trung vào việc: mô hình mạnh vượt qua sai lầm của người giám sát yếu đã được phổ biến hóa.

Các giới hạn Burns et al. lưu ý:
- Sự khác biệt giữa yếu và mạnh ở đây là khả năng, không phải sự sắp xếp. mô hình yếu là sắp xếp; mô hình siêu nhân thực sự có thể được sắp xếp bởi con người nhưng với một khoảng cách khả năng lớn hơn nhiều.

> Sự khác biệt giữa yếu và mạnh là khả năng, chứ không phải đối với nhau. Mô hình yếu là đối với nhau; mô hình siêu nhân thực sự có thể được đối với nhau bởi con người, nhưng sự khác biệt về khả năng là rất lớn.

- Việc tổng quát mô hình mạnh có thể là nhiều hơn về nhiệm vụ trước hơn là về việc phục hồi ý định thực tại cơ bản.

> Sự phổ biến của mô hình mạnh có thể nhiều hơn là về nhiệm vụ trước, chứ không phải để phục hồi ý định thực sự.

- Việc tạo ra kiến thức ẩn trong mô hình mạnh là vấn đề thực sự; PGR đo lường một hoạt động cụ thể.

> 激发强模型的潜在知识才是真正的问题;PGR 衡量的是特定操作化──

> **【拓展：三种可扩展监督机制 → 辩论/递归奖励建模/任务分解】**辩论(Irving 等人 2018): hai U 实例争论相反立场,弱评判者决定──归归奖励建模(Leike 等人 2018):U 帮助人类训练 U+1 的奖励模型,监督者的有效能力随模型增长──任务分解(Christiano 等人 2018):将硬任务分解成人类可检查的子任务,归归执行──每种机制都假设关于任务结构或中间组合对齐的某些东西──

### Giám sát có thể mở rộng: ba cơ chế

- **Debate (Irving et al. 2018).**Hai trường hợp của U tranh luận về các bên đối lập; thẩm phán yếu có thể quyết định. Hiểu: tìm kiếm một câu trả lời đúng thuyết phục dễ hơn là tìm kiếm một câu trả lời sai thuyết phục. Nghiên cứu gần đây năm 2024-2025 (Khan et al., Michael et al.) cho thấy tranh luận đôi khi giúp ích và đôi khi không giúp ích, và liệu nó có giúp ích hay không phụ thuộc vào cấu trúc nhiệm vụ.

> **辩论（Irving 等人 2018）。**Hai ví dụ của U tranh luận đối lập; các thẩm phán yếu quyết định. giả thuyết: tìm thấy một câu trả lời thực đáng tin cậy dễ dàng hơn tìm thấy một câu trả lời giả đáng tin cậy. Nghiên cứu mới nhất năm 2024-2025 cho thấy các cuộc tranh luận có lúc hiệu quả có lúc không hiệu quả, phụ thuộc vào cấu trúc nhiệm vụ.

- **Recursive Reward Modeling (Leike et al. 2018).**U giúp người ta đào tạo mô hình phần thưởng cho U+1.

> **递归奖励建模（Leike 等人 2018）。**U  giúp nhân tạo đào tạo U + 1 奖励模型── giám sát viên có năng lực hiệu quả tăng trưởng theo mô hình──

- **Task Decomposition (Christiano, Shlegeris, Amodei 2018).**Phân hủy một nhiệm vụ khó thành các nhiệm vụ phụ mà con người có thể kiểm tra, lặp lại.

> **任务分解（Christiano, Shlegeris, Amodei 2018）。**Để phân tích nhiệm vụ cứng trở thành nhiệm vụ phụ của con người có thể kiểm tra được.

Mỗi cơ chế giả định một cái gì đó về cấu trúc của nhiệm vụ hoặc sự sắp xếp của các thành phần trung gian.

> Mỗi cơ chế đều giả định về cấu trúc nhiệm vụ hoặc các thành phần trung tâm phù hợp với một cái gì đó.

### Tại sao giám sát có thể mở rộng và W2SG là bổ sung

Việc giám sát có thể mở rộng sẽ giúp giám sát viên có hiệu quả hơn.
W2SG sẽ thu hẹp khoảng cách từ bất kỳ tín hiệu bất toàn nào mà giám sát viên có thể cung cấp.

> 可扩展监督提高监督者的有效信号质量──弱到强泛化 从监督者能提供的任何不完美信号中闭合差距──

Lang et al.  Debate Helps Weak-to-Strong Generalization (arXiv:2501.13124) kết hợp chúng: một giao thức tranh luận cung cấp các nhãn yếu tốt hơn, và mô hình mạnh được đào tạo trên các nhãn đó.

> Lang 等人辩论帮助弱到强泛化 ((arXiv:2501.13124) sẽ kết hợp hai:

> **【中文解读】**组织戏剧:OpenAI's超级对齐团队 vào năm 2024 Jan Leike 离职加入人类 后解散――但研究议程(可扩展监督、弱到强泛化、自动化对齐研究) 在人类 和学术实验室继续MATS(Lớp 28)、Redwood(Lớp 10)、Apollo(Lớp 8)、METR(Lớp 28)。

### Phương pháp tổ chức

Nhóm Superalignment của OpenAI đã bị giải tán vào tháng 5 năm 2024 sau khi Jan Leike rời khỏi Anthropic. Chương trình nghị sự (chăm sóc có thể mở rộng, W2SG, nghiên cứu sắp xếp tự động) tiếp tục tại Anthropic và tại các phòng thí nghiệm học tập  MATS (Lớp 28), Redwood (Lớp 10), Apollo (Lớp 8), METR (Lớp 28).

> Nhóm siêu đối tác của OpenAI vào tháng 5 năm 2024 Jan Leike 离职加入Anthropic 后解散──研究议程(可扩展监督、弱到强泛化、自动化对齐研究) tiếp tục trong Anthropic 和学术实验室MATS、Redwood、Apollo、METR── cấu trúc tổ chức đã thay đổi; các vấn đề nghiên cứu không thay đổi──

### Khi điều này phù hợp với giai đoạn 18

Bài học 6-10 mô tả mối đe dọa và mô hình phòng thủ theo giả định U là không đáng tin cậy. Bài học 11 là mô hình tấn công: làm cho người giám sát đủ mạnh để xác minh sự phù hợp của U. Bài học 12-16 sau đó chuyển sang công cụ thực tế của đánh giá đối thủ.

> Bài học 6-10  mô tả mối đe dọa và giả thuyết U không thể tin tưởng 范式 phòng thủ  Bài học 11 là mô hình tích cực: làm cho giám sát viên đủ mạnh để xác minh U của đối với  Bài học 12-16  hướng tới các công cụ thực dụng của đánh giá đối kháng 

> **【拓展：辩论帮助弱到强泛化 → 2025 组合】**Lang 等人(arXiv:2501.13124, tháng 1 năm 2025) sẽ mở rộng giám sát và yếu đến mạnh mẽ kết hợp: hiệp định luận cung cấp các nhãn hiệu yếu hơn, mô hình mạnh trên các nhãn này được đào tạo.

## Hãy sử dụng nó để thực hiện
```figure
scalable-oversight
```

## Sử dụng nó

`code/main.py`mô hình mạnh có 95% trần nhà trên nhãn vàng. Bạn tinh chỉnh mô hình mạnh trên nhãn yếu, đo PGR, và so sánh với mạnh trên vàng và yếu một mình.

> `code/main.py`Trong nhiệm vụ tổng hợp mô phỏng W2SG 微调── tỷ lệ xác định của nhãn hiệu yếu 70% 带有结构性错误; mô hình mạnh trên nhãn hiệu vàng được giới hạn lên đến 95%── bạn có thể mô hình yếu trên nhãn hiệu yếu, đo PGR,并与强模型金标和 weak模型单独结果比较──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-w2sg-pgr.md`. Với mô tả thiết lập giám sát, nó xác định người giám sát yếu, mô hình mạnh, chất lượng giám sát, và tính toán (hoặc yêu cầu) PGR. Nó đánh dấu liệu tuyên bố là " yếu có thể giám sát mạnh" hoặc " cơ chế giám sát yếu + có thể giám sát mạnh".

> 本课产 出 `outputs/skill-w2sg-pgr.md`△给定监督设置描述,识别弱监督者、强模型、监督质量,并计算((或请求) PGR。标记声明是"弱可以监督强"还是"弱 + 监督机制可以监督强"。

## Tập luyện bài tập

1. Đi chạy`code/main.py`. báo cáo PGR cho điểm yếu_sự chính xác = 0,60, 0,70, 0,80. Giải thích hình dạng đường cong PGR.

2. Thay đổi nhãn yếu để có lỗi cấu trúc (ví dụ, luôn sai trong một lớp đầu vào cụ thể). PGR tăng, giảm hoặc giữ nguyên như vậy? Giải thích.

3. Hãy đọc Burns et al. 2023 Phần 4.3 (các nhiệm vụ của NLP). Tái tạo lại trực giác "sự tin cậy phụ trợ": khi mô hình mạnh mẽ tự tin hơn các nhãn hiệu yếu, ai thắng?

4. Thiết kế một giao thức giám sát có thể mở rộng mà kết hợp tranh luận và phân hủy nhiệm vụ cho một nhiệm vụ kỹ thuật phần mềm. Chọn một chế độ thất bại của mỗi thành phần và giải thích cách kết hợp giải quyết hoặc không giải quyết từng thành phần.

5. Cần nói rõ những gì có thể làm sai lệch tuyên bố "sự tổng hợp yếu đến mạnh là một con đường khả thi để siêu phù hợp".

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Scalable oversight | "making the overseer stronger" | Mechanisms that increase an overseer's ability to evaluate a more-capable model |
| W2SG | "weak supervises strong" | Fine-tuning a strong model on weak labels and measuring the capability recovered |
| PGR | "performance gap recovered" | (fine-tuned - weak) / (ceiling - weak); 1.0 = fully closed, 0 = no help |
| Debate | "two U instances argue" | Scalable oversight mechanism where a weak judge picks between two U defenders |
| RRM | "recursive reward modeling" | U helps train the reward model for U+1; overseer capability tracks U |
| Task decomposition | "sub-tasks the human checks" | Break a hard task into sub-tasks the human can verify, recursively |
| Superalignment | "aligning superhuman AI" | The research agenda concerned with aligning models the human cannot directly evaluate |

## Xem thêm 延伸阅读

- [Burns et al. — Weak-to-Strong Generalization (OpenAI 2023)](https://openai.com/index/weak-to-strong-generalization/) giấy W2SG
- [Irving, Christiano, Amodei — AI safety via debate (arXiv:1805.00899)](https://arxiv.org/abs/1805.00899) cơ chế tranh luận
- [Leike et al. — Scalable agent alignment via reward modeling (arXiv:1811.07871)](https://arxiv.org/abs/1811.07871) Mô hình hóa phần thưởng tái tạo
- [Khan et al. — Debating with More Persuasive LLMs Leads to More Truthful Answers (arXiv:2402.06782)](https://arxiv.org/abs/2402.06782) 2024 nghiên cứu kinh nghiệm về tranh luận với những người tranh luận mạnh mẽ hơn
- [Lang et al. — Debate Helps Weak-to-Strong Generalization (arXiv:2501.13124)](https://arxiv.org/abs/2501.13124) 2025 kết hợp cuộc tranh luận + W2SG
