# Sự riêng tư khác biệt cho LLM 差分隐私 LLM

> DP-SGD vẫn là chuẩn  các cập nhật độ sốc tiêm tiếng  cung cấp các bảo đảm chính thức (epsilon, delta). Chi phí tổng thể trong tính toán, bộ nhớ và tiện ích là đáng kể; điều chỉnh DP hiệu quả các tham số (LoRA + DP-SGD) là cấu hình 2025 phổ biến (ACM 2025). Hai cơ quan bằng chứng trong căng thẳng: suy luận thành viên dựa trên các ngôn ngữ (Duan et al., 2024) báo cáo thành công hạn chế đối với các mô hình ngôn ngữ; khai thác dữ liệu đào tạo (Carlini et al., 2021; Nasr et al., 2025) phục hồi ghi nhớ từ ngữ đáng kể. Nghị quyết (arXiv:2503.06808, tháng 3 năm 2025): khoảng cách là trong những gì được đo  canaries được đưa vào so với dữ liệu "có thể thu được nhiều nhất". Các thiết kế mới của canary cho phép MIA dựa trên tổn thất mà không có mô hình bóng tối và tạo ra kiểm toán DP không nhỏ đầu tiên của một LLM được đào tạo trên dữ liệu thực với đảm bảo DP thực tế. Các lựa chọn thay thế: PMixED (arXiv:2403.15638)  dự đoán riêng tư tại thời điểm suy luận thông qua sự pha trộn của các chuyên gia về phân phối mã thông báo tiếp theo; DP tạo dữ liệu tổng hợp (Google Research 2024). Cuộc tấn công mới nổi: Sự đảo ngược quyền riêng tư khác nhau thông qua phản hồi LLM  rò rỉ điểm tin cậy.

> **【中文解读】**Bài viết này giới thiệu về sự khác biệt về quyền riêng tư của LLM  trong đào tạo và suy luận  Phương pháp toán học bảo vệ quyền riêng tư dữ liệu người dùng  DP-SGD là phương pháp tiêu chuẩn  Lồn                                                                                                                                                                                                                                   

> **【拓展：MIA vs 训练数据提取 → 衡量差距】**Hai chứng cứ của năm 2024-2025 hình thành张力: 金丝雀 MIA(Duan 等人 2024) báo cáo về thành công của mô hình ngôn ngữ hạn chế; đào tạo dữ liệu提取(Carlini 2021, Nasr 等人 2025) phục hồi một lượng lớn ký ức từng chữ.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, DP-SGD noise-injection and ε-δ accountant demonstration) | **语言:** Python（标准库，DP-SGD 噪声注入和 ε-δ 计数器演示）
**Prerequisites:** Phase 01 · 09 (information theory), Phase 10 · 01 (large-model training) | **前置知识:** Phase 01 · 09 (信息论), Phase 10 · 01 (大模型训练)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 01·09(信息论) 、Phase 10·01(大模型训练) ――DP-SGD = 标准 DP 训练方法,(ε,δ) 保证。
>  **【类比】**DP = "data ẩn身衣"──DP-SGD 在梯度注入噪音,单个样本不影响整体训练→形式化数学证明无法从模型反推是否某条数据在训练集──代价:计算/内存/效用都明显下降──LoRA+DP-SGD 是 2025 实用配置(只DP 微调适配器)──
> 🤔 困境: MIA  tấn công thất bại vs 训练数据提取成功差别在测什么(插入 vs 最易提取) ――2025.3 新金雀设计首次对真数据 LLM做非凡 DP 审计――

## Mục tiêu học tập

- Định nghĩa (epsilon, delta) - sự riêng tư khác biệt và nêu ra công thức DP-SGD.
- Giải thích căng thẳng 2024-2025: MIA canary vs khai thác dữ liệu đào tạo cho thấy hình ảnh khác nhau.
- Mô tả PMixED và lý do tại sao dự đoán riêng tư thời gian suy luận là một sự thay thế cho đào tạo DP.
- Mô tả sự đảo ngược quyền riêng tư khác nhau thông qua cuộc tấn công phản hồi LLM.

> 定义 (epsilon, delta) -差分隐私并说明 DP-SGD 方法──解释 2024-2025 年张力:金丝雀 MIA vs 训练数据提取给出不同图景──描述 PMixED 及为什么推理时私有预测是 DP 训练的替代──描述通过 LLM 反的差分隐私逆转攻击──

## Vấn đề  vấn đề

Các LLM ghi nhớ. Carlini et al. 2021 cho thấy các mô hình ngôn ngữ sản xuất tái tạo văn bản đào tạo theo yêu cầu. DP là biện pháp phòng thủ chính thức: đào tạo để sản xuất có thể không nhạy cảm với bất kỳ ví dụ đào tạo nào. Bằng chứng 2024-2025 cho thấy DP-SGD là cần thiết nhưng các giá trị ε được triển khai có thể không phù hợp với mô hình đe dọa.

> LLM 会记忆──Carlini 等人 2021 năm trình bày mô hình ngôn ngữ sản xuất có thể theo yêu cầu có thể được thực hiện theo từng từ bài tập văn bản──DP là phòng thủ hình thức hóa: bài tập làm cho xuất khẩu đối với bất kỳ mô hình đào tạo đơn lẻ nào là không nhạy cảm──2024-2025 năm bằng chứng cho thấy DP-SGD là cần thiết nhưng triển khai ε  giá trị có thể không phù hợp với mô hình đe dọa──

## Khái niệm

> **【中文解读】**(epsilon, delta) -差分隐私定义:随机算法 M 是 (epsilon, delta) -DP 的, nếu đối với bất kỳ hai pha khác nhau một ví dụ của dữ liệu tập hợp và bất kỳ sự kiện S:P(M(D) trong S) <= e^epsilon * P(M(D') trong S) + delta。 giải thích:输出分布足够接近(由 epsilon 参数化), bất kỳ đóng góp của cá nhân đơn lẻ nào không thể được đưa ra một cách đáng tin cậy, ngoại trừ tỷ lệ delta。

### (ε, δ) - sự riêng tư khác biệt

Một thuật toán ngẫu nhiên M là (ε, δ) -DP nếu cho bất kỳ hai tập dữ liệu khác nhau trong một ví dụ và bất kỳ sự kiện S nào:
P(M(D) trong S) <= e^ε * P(M(D') trong S) + δ.

> 随机算法 M 是 (ε, δ) -DP 的, nếu đối với bất kỳ hai相差一个示例的数据集和任何事件 S:P(M(D) trong S) <= e^ε * P(M(D') trong S) + δ。

Giải thích: phân bố đầu ra là đủ gần (được định đo bằng ε) để không thể suy luận đáng tin cậy về sự đóng góp của bất kỳ cá nhân nào, ngoại trừ với xác suất δ.

> 解释:输出分布足够接近 (由 ε 参数化) bất kỳ đóng góp của một cá nhân nào không thể được đưa ra một cách đáng tin cậy, ngoại trừ tỷ lệ δ──

### DP-SGD

Abadi et al. 2016. Công thức tiêu chuẩn:
1. Hãy lấy một lô nhỏ.
2. Xét các gradient cho mỗi ví dụ.
3. Clip mỗi gradient mỗi ví dụ đến ngưỡng C.
4. Kết hợp các gradient cắt và thêm tiếng ồn Gaussian với std σ * C.
5. Sử dụng số lượng tiếng ồn để cập nhật các tham số.

> DP-SGD 标准方法:1. 采样小批次――2. 计算 từng từng thang độ――3. 剪切每个 thang đến 值 C―4. 求和剪切后的梯度并添加高的噪音――5.

Chi phí bảo mật được theo dõi bởi một kế toán viên (Tế toán viên Moment, kế toán viên Rényi DP). Các giá trị ε được báo cáo trong văn học LLM khác nhau rất nhiều theo mô hình đe dọa, độ nhạy cảm dữ liệu và mục tiêu hữu ích; không có mặc định "an toàn" chung ε. Các ví dụ được xuất bản khoảng ε ≈ 110 trong một số thiết lập đào tạo LLM, nhưng đây là minh họa  không được khuyến cáo mặc định. Low ε thường đòi hỏi nhiều tiếng ồn hơn và có thể làm tăng mất năng lượng.

> 隐私成本由计计追. 文献中报告的 ε 值因威胁模型不同; không có mặc định chung về "an toàn" ε.

### LoRA + DP-SGD

LoRA (Hu et al. 2022) giới hạn cập nhật gradient cho một bộ chuyển đổi nhỏ, giảm lưu trữ gradient cho mỗi ví dụ. LoRA + DP-SGD là cấu hình phổ biến năm 2025.

> Lộ lượng DP-SGD 训练前沿模型成本过高──LoRA 限制梯度更新到小型适配器,减少逐例梯度储存──LoRA + DP-SGD là 2025 年常见配置──DP 保证适用于适配器;基础模型保持固定──

### Sự căng thẳng 2024-2025

Hai bằng chứng:

> 两条证据线:

- **Canary MIA (Duan et al. 2024).**Đưa các canary độc đáo vào dữ liệu đào tạo, đo lường liệu một kẻ tấn công thông tin thành viên có thể xác định chúng hay không. báo cáo thành công hạn chế trên các mô hình ngôn ngữ.
- **Training-data extraction (Carlini 2021, Nasr et al. 2025).**Cố gắng mô hình với một dấu tiền; đo liệu nó có phục hồi văn bản từ khóa đào tạo hay không. báo cáo ghi nhớ đáng kể.

> Kim丝雀 MIA  báo cáo thành công hạn chế, ám chỉ MIA 困难――训练数据提取报告大量记忆, ám chỉ MIA 在相关意义上容易――

Nghị quyết tháng 3 năm 2025 (arXiv:2503.06808): hai biện pháp khác nhau. MIA hỏi "ví dụ e trong D?" trên cá thể có thể được chèn.

> Giải pháp tháng 3 năm 2025: hai người đo lường khác nhau. MIA hỏi "ví dụ e trong D có?",提取问"我能恢复 D của gì?""最可提取的"ví dụ才是隐私的关键.

Thiết kế mới của canary. MIA dựa trên tổn thất mà không có mô hình bóng. kiểm toán DP đầu tiên không trivial của một LLM trên dữ liệu thực với đảm bảo DP thực tế.

> MIA dựa trên tổn thất của mô hình không bóng, lần đầu tiên thực hiện kiểm toán DP phi thường trên dữ liệu thực tế.

> **【拓展：PMixED → 推理时隐私】**PMixED(arXiv:2403.15638) cung cấp suy đoán khi riêng dự đoán: trong các chuyên gia phân phối tiếp theo, mỗi chuyên gia nhìn thấy một phân đoạn dữ liệu đào tạo, tập hợp thêm tiếng ồn để thực hiện DP。 hoàn toàn tránh DP  đào tạo。DP 合成 dữ liệu tạo(Google Research 2024) sử dụng LoRA 微调采样合成 dữ liệu của DP-SGD, sau đó đào tạo trên dữ liệu tổng hợp dưới游分类器── hai mô hình đe dọa khác nhau để chi phí quy định hiệu quả của đào tạo DP  toàn bộ.

### Các lựa chọn thay thế cho đào tạo DP

- **PMixED (arXiv:2403.15638).**Dự đoán riêng vào thời điểm suy luận. Sự pha trộn của các chuyên gia về phân phối mã thông báo tiếp theo; mỗi chuyên gia thấy một mảnh dữ liệu đào tạo; tổng hợp thêm tiếng ồn cho DP. Tránh đào tạo DP hoàn toàn.
- **DP synthetic data generation (Google Research 2024).**LoRA-fine-tune với DP-SGD, mẫu dữ liệu tổng hợp, đào tạo một phân loại dòng chảy xuống trên dữ liệu tổng hợp.

Cả hai đều tránh chi phí tiện ích của đào tạo DP đầy đủ với chi phí của mô hình đe dọa khác nhau.

> **【中文解读】**差分隐私逆转攻击(2025): sử dụng DP 训练模型的置信分数作为预言机重新识别个体──即使输出不泄露,置信分布也可能泄露──防御:不暴露置信度,或在暴露前截断/量化──这是 (epsilon, delta) -DP 训练之外的额外要求──

### Sự đảo ngược quyền riêng tư khác nhau thông qua phản hồi LLM

Chiến dịch 2025 sắp tới. Sử dụng điểm độ tin cậy của mô hình được đào tạo bằng DP như một lời tiên tri để xác định lại cá nhân. Ngay cả khi các kết quả không bị rò rỉ, phân phối sự tin cậy có thể.

> 2025年新兴攻击: sử dụng DP 训练模型的置信分数作为预言机重新识别个体──即使输出不泄露,置信分布也可能泄露──

Sự bảo vệ: không tiết lộ bí mật, hoặc cắt giảm / định lượng chúng trước khi tiếp xúc. Đây là một yêu cầu bổ sung ngoài đào tạo (ε, δ) -DP.

> 防御:不露置信度,或在露前截断/量化──这是 (ε, δ) -DP 训练以外的额外要求──

### Khi điều này phù hợp với giai đoạn 18

Bài học 20-21 là thiên vị/sự công bằng. Bài học 22 là quyền riêng tư. Bài học 23 là xuất phát thông qua đánh dấu nước. Bài học 27 bao gồm lớp xuất phát dữ liệu quy định.

> Bài học 20-21 là sự thiên vị/ công bằng. Bài học 22 là sự bí mật. Bài học 23 là thông qua nguồn nước. Bài học 27 bao gồm các tầng nguồn dữ liệu giám sát.

> **【拓展：DP-SGD 的实际开销 → LoRA 解决方案】**Lộ lượng DP-SGD  đào tạo mô hình tiền tuyến trong tính toán, lưu trữ và hiệu quả trên giá rất lớn. LoRA(Hu 等人 2022) giới hạn mức độ cập nhật đến các bộ ứng dụng nhỏ, giảm từng trường hợp mức độ lưu trữ. LoRA + DP-SGD là 2025 thường thấy định cấu hình.

## Sử dụng nó.
```figure
an-dp-clip-noise
```

## Sử dụng nó

`code/main.py`mô phỏng DP-SGD trên một bộ dữ liệu phân loại nhựa đồ chơi. Bạn có thể quét nhân âm σ và chuẩn cắt C và theo dõi ngân sách (ε, δ) và chi phí chính xác. Một "cuộc tấn công canary" đưa vào một ví dụ đào tạo độc đáo và đo liệu một bài kiểm tra mất nhật ký có thể phát hiện nó trước và sau DP.

> `code/main.py`Trong tập dữ liệu phân loại hai của đồ chơi mô phỏng DP-SGD. Bạn có thể quét số âm thanh nhân s và cắt số C, theo dõi (ε, δ)  ngân sách và chi phí xác định.

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-dp-audit.md`. Với một tuyên bố DP về việc triển khai mô hình ngôn ngữ, nó kiểm toán: các giá trị (ε, δ), kế toán viên được sử dụng, giao thức đánh giá MIA, và liệu các vector tín dụng-trong phơi nhiễm đã được đánh giá hay không.

> 本课产 出 `outputs/skill-dp-audit.md` Định nghĩa ngôn ngữ mô hình triển khai  DP tuyên bố, kiểm toán: ε, δ) 值、 sử dụng máy tính tính, MIA  đánh giá thỏa thuận và liệu đã đánh giá được độ tin cậy về lượng tiếp xúc 

## Tập luyện bài tập

1. Đi chạy`code/main.py`. Quét σ trong {0,5, 1.0, 2.0} và báo cáo sự đổi giá chính xác (ε, δ).

2. Thực hiện một thử nghiệm canary và một thử nghiệm mất nhật ký. đo tốc độ phát hiện trước và sau DP-SGD ở σ = 1.0.

3. Đọc Nasr et al. 2025 về đào tạo-khai thác dữ liệu. Tại sao thành công khai thác không sụp đổ dưới mức trung bình ε? Điều này có nghĩa là gì về MIA-as-evaluation?

4. Thiết kế một triển khai sử dụng PMixED (arXiv:2403.15638) hoạt động hoàn toàn tại thời điểm suy luận. mô hình đe dọa mà PMixED giải quyết mà DP-SGD không?

5. Xét bản xoay về sự đảo ngược DP thông qua cuộc tấn công phản hồi LLM. Thiết kế một biện pháp phản đối hạn chế rò rỉ điểm tin cậy và ước tính chi phí triển khai của nó.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| DP | "(ε, δ)-differential privacy" | Formal privacy: output distribution close under neighbouring-dataset change |
| DP-SGD | "noise-injected SGD" | Gradient clipping + Gaussian noise addition; standard DP training |
| LoRA + DP-SGD | "efficient private fine-tune" | DP-SGD on low-rank adapters; standard 2025 configuration |
| MIA | "membership inference" | Attack that determines whether an example was in training data |
| Canary | "inserted watermark example" | Unique training example used to measure DP leakage |
| PMixED | "private inference mixture" | Inference-time DP via mixture-of-experts on next-token distributions |
| DP Reversal | "confidence leakage attack" | Attack that uses a model's confidence as an oracle for re-identification |

## Xem thêm 延伸阅读

- [Abadi et al. — DP-SGD (arXiv:1607.00133)](https://arxiv.org/abs/1607.00133) thuật toán đào tạo DP tiêu chuẩn
- [Carlini et al. — Extracting Training Data (arXiv:2012.07805)](https://arxiv.org/abs/2012.07805) giấy khai thác theo luật
- [Duan et al. — Canary MIA on LLMs (arXiv:2402.07841, 2024)](https://arxiv.org/abs/2402.07841) MIA thành công hạn chế
- [Kowalczyk et al. — Auditing DP for LLMs (arXiv:2503.06808, March 2025)](https://arxiv.org/abs/2503.06808) giải quyết căng thẳng
- [PMixED (arXiv:2403.15638)](https://arxiv.org/abs/2403.15638) dự đoán riêng tư thời gian suy luận
