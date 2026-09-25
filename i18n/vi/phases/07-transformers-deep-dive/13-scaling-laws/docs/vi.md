# Quy luật quy mô 缩放定律

> Bài báo Kaplan năm 2020 nói: mô hình lớn hơn, tổn thất thấp hơn. Bài báo Hoffmann năm 2022 nói: bạn đang được đào tạo thấp.

> **【中文解读】**Định luật Chinchilla tiết lộ mô hình lớn, dữ liệu, số lượng toán có quan hệ tối ưu nhất.

**Type:** Study | **类型:** 学习
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Khi bạn có C FLOPs của đào tạo tính toán và muốn mô hình tốt nhất, bạn phải đối mặt với hai nút:

> Khi bạn có C FLOPs tập tính lượng và muốn mô hình tốt nhất, bạn phải đối mặt với hai vòng quay:

1. **How many parameters (N)?**Mô hình lớn hơn, dung lượng cao hơn.
   Trung ngữ翻译:**多少参数（N）？**Mô hình càng lớn, dung lượng càng cao.
2. **How many training tokens (D)?**Nhiều dữ liệu hơn, sử dụng năng lực tốt hơn.
   Trung ngữ翻译:**多少训练 token（D）？**Số liệu càng nhiều, dung lượng sử dụng càng tốt.

FLOPs có quy mô khoảng như `6 × N × D`Bạn có thể đẩy N lên và D xuống, hoặc D lên và N xuống.

> FLOPs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `6 × N × D`扩展──你可以增大N 减小D,或增大D 减小N──哪个好?

Trước năm 2022, câu trả lời là "thổi N cứng". GPT-3 (2020) là các tham số 175B được đào tạo trên các token ~ 300B. Tỷ lệ khoảng 1,7 token mỗi tham số. Các luật quy mô Kaplan hỗ trợ điều này.

> Trước năm 2022, câu trả lời là "推大 N"──GPT-3(2020) có 175B tham số, trong khoảng 300B token 上训―― tỷ lệ khoảng 1.7  token cho mỗi tham số──Kaplan 缩放定律支持这一观点──

Hoffmann et al. (2022), đào tạo một gia đình mô hình nhỏ gọi là Chinchilla, tìm thấy một điều khác biệt: tỷ lệ tối ưu gần hơn với **20 tokens per parameter**GPT-3 bị thiếu đào tạo 10 lần. Chinchilla (70B params, 1.4T token) đánh bại GPT-3 (175B, 300B token) trên mọi điểm chuẩn với chi phí suy luận thấp hơn 2,5 lần.

> Hoffmann 等人(2022) đào tạo một nhóm nhỏ tên là mô hình của Chinchilla, phát hiện ra kết quả khác nhau: tỷ lệ tốt nhất gần**每个参数 20 个 token**GPT-3 low estimation training 10 times──Chinchilla(70B 参数,1.4T token) trên mỗi基准测试 đều đánh bại GPT-3(175B,300B token), ước tính chi phí chỉ dành cho người sau đó 2.5 分之一──

2026 là thế giới của Chinchilla với một sự xoay quanh quan trọng. Llama 3 8B được đào tạo trên 15 nghìn tỷ token, tỷ lệ 1.875 token mỗi tham số. Ninety-four lần vượt qua Chinchilla-optimal. Chi phí suy luận quan trọng hơn chi phí đào tạo cho các mô hình sẽ được sử dụng ở quy mô, vì vậy quá trình đào tạo (trước Chinchilla) cho một dấu chân có thể triển khai nhỏ hơn là mặc định năm 2026.

> Năm 2026 là thế giới của Chinchilla nhưng có một bước ngoặt quan trọng. Llama 3 8B đã sử dụng 15 tỷ token  đào tạo, tỷ lệ cho mỗi tham số 1.875 token.

> **【中文解读】**缩放定律的核心洞察:FLOPs ≈ 6 × N × D(参数 × token 数)  Kaplan(2020) xu hướng tăng lớn hơn N, nhưng Chinchilla(2022) chứng minh tỷ lệ tối ưu khoảng 20 token/parameter。2026 năm thực hành hơn nữa:Llama 3 8B sử dụng 1,875 token/parameter training远超 Chinchilla tối ưu, vì tính toán chi phí hơn chi phí đào tạo, quá tập luyện mô hình nhỏ sau đó chi phí triển khai thấp đã trở thành tiêu chuẩn ngành.

> **【拓展：过度训练策略的经济逻辑】**Llama 3 8B sử dụng token 15T  đào tạo(远超Chinchilla 最优的160B token), chi phí tính toán đã giảm đáng kể. Đó là do chi phí tính toán của mỗi token được tính toán và số lượng được phân tích tương đương với số lượng chính xác. Chi phí tính toán của các parameter 8B chỉ khoảng 1/9 của mô hình 70B. Đối với mô hình có quy mô lớn như API 服务), chi phí tính toán tiết kiệm là chi phí quá mức.

## Khái niệm cốt lõi

![Chinchilla curves: loss vs compute at various N/D ratios](../assets/scaling-laws.svg)

### Luật Hoffmann

Từ tờ Chinchilla, mất mát là sau:

> Từ Chinchilla 论文, mất mát theo:

```
L(N, D) = A / N^α + B / D^β + E
```

- `N`= các tham số (không bao gồm).
  Trung ngữ翻译:`N`= 参数量(非嵌入)
- `D`= token đào tạo.
  Trung ngữ翻译:`D`= 训练 token số:
- `α ≈ 0.34`- `β ≈ 0.28`(cứu độ đối xứng).
  Trung ngữ翻译:`α ≈ 0.34``β ≈ 0.28`(大致对称)
- `E ≈ 1.69`, mức tối đa mất mát không thể giảm.
  Trung ngữ翻译:`E ≈ 1.69`, không thể mất đi trên giới hạn.
- `A ≈ 406`- `B ≈ 411`- Tôi không biết.
  Trung ngữ翻译:`A ≈ 406``B ≈ 411`

Hai thuật ngữ giao dịch với nhau khi bạn mở rộng quy mô.`N`ở tính toán cố định (C = 6ND) và giải quyết:

> 两项在扩展时相互制衡──在固定计算量 ((C = 6ND) 下对 `N`求导并求解:

```
N_opt ≈ 0.6 × (C/6)^0.5
D_opt ≈ 0.6 × (C/6)^0.5
D_opt / N_opt ≈ 20
```

Tính tối ưu tính toán: 20 token cho mỗi tham số.

> 计算最优: mỗi参数 là 20 token.

### Sao lại tập quá nhiều?

Chinchilla-optimal giảm thiểu sự mất mát trong tập luyện cho mỗi tập FLOP. Nhưng bạn trả phí huấn luyện một lần; chi phí suy luận mãi mãi.

> Chinchilla tối ưu tối thiểu hóa mỗi tập FLOP của training mất mát. Nhưng tập phí chỉ trả một lần; ước tính chi phí mãi mãi.

Đối với một chatbot phục vụ một nghìn tỷ token mỗi tháng, suy luận thống trị tổng chi phí. Cách tiếp cận của Llama: đào tạo nhỏ hơn, dài hơn. 8B tại 15T token được tối ưu hóa sâu sắc theo suy luận:

> Đối với dịch vụ hàng tháng của tỷ đồng token, các phương pháp của Llama: đào tạo nhỏ hơn, dài hơn.

- Khớp với GPU của người tiêu dùng.
  Trung ngữ翻译:适配消费级 GPU。
- Tốc độ trễ là một phần nhỏ của 70B Chinchilla tối ưu.
  Trung文翻译:延迟仅为70B Chinchilla 最优的一小部分──
- Chất lượng là đủ gần để làm hầu hết các nhiệm vụ.
  Trung ngữ翻译:质量 đối với hầu hết các nhiệm vụ là đủ gần.

Bài báo 2024 của DeepMind ("Thay đào tạo là tối ưu mới") đã chính thức hóa điều này. Đối với tải trọng công việc bị chi phối bởi suy luận, tỷ lệ đúng gần 100500 token mỗi tham số tùy thuộc vào khối lượng phục vụ.

> DeepMind 2024 năm bài luận ((" quá tập là mới nhất") đã hình thành điểm này. Đối với tải trọng công việc chủ đạo theo suy luận, tỷ lệ chính xác gần mỗi tham số 100-500 token, phụ thuộc vào lượng dịch vụ.

### Sự xuất hiện vs sự trơn tru

Thuyết: một số khả năng (làm toán, lý luận nhiều bước, theo dõi chuỗi suy nghĩ) đột nhiên "phơi lên" ở một số quy mô.

> 声称:某些能力 (một số khả năng) 算术,多步推理,思维链遵循) ở một số quy mô"涌现" (tự động hóa)

Schaeffer et al. (2023) lập luận rằng đây là một đồ tạo phép đo: các métrics mới nổi sử dụng điểm số không liên tục (sự phù hợp chính xác, độ chính xác ở ngưỡng) che giấu sự cải thiện trơn tru trong các logit cơ bản.

> Schaeffer 等人(2023) cho rằng đây là một phép đo giả: xu hướng sử dụng không liên tục của các chỉ số đánh giá(精确匹配、值准确率), ẩn giấu sự cải thiện thanh toán của các logic tầng dưới đây。连续指标(交叉) hiển thị đường cong thanh toán。

Năm 2026, sự đồng thuận là: dự đoán thông qua mất tích liên tục là đáng tin cậy.

> Sự đồng ý năm 2026 là: Dự đoán thông qua mất tích liên tục là đáng tin cậy.

> **【中文解读】**"tăng lực hiện tại" (涌现能力) đã gây ra nhiều cuộc thảo luận trong năm 2023 Một số năng lực dường như xuất hiện đột ngột ở một quy mô cụ thể. Nhưng Schaeffer 等人 chứng minh rằng đây có thể là một phép đo giả: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không liên tục: không: không liên tục: không: không liên tục: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không: không

> **【拓展：数据质量比数据量更重要】**Năm 2026 biến thể mới của quy định thu nhỏ là chất lượng dữ liệu. Phi của Microsoft chứng minh, các token "hoàn chất lượng" được chọn kỹ sẽ tăng lượng tính toán hiệu quả gấp 2 lần hoặc hơn. Llama 3 sử dụng tối ưu hóa tỷ lệ phân phối dữ liệu và tăng cường dữ liệu tổng hợp.

### Hình ảnh năm 2026

Luật quy mô vẫn còn hiệu quả, nhưng:

> 缩放定律 vẫn còn hiệu lực, nhưng:

| Factor | Changed how |
|--------|-------------|
| 因素 | 变化方式 |
| Data quality | Curating "good" tokens (Phi-style) shifts curves by >2× effective compute |
| 数据质量 | 筛选"优质" token（Phi 风格）使曲线偏移超过 2 倍有效计算 |
| MoE | Total params decouple from active FLOPs; scaling laws per-active-FLOP |
| MoE | 总参数量与活跃 FLOPs 解耦；按活跃 FLOPs 的缩放定律 |
| Post-training | Some capabilities (instruction following, code) shift with SFT+RLHF more than pretraining |
| 后训练 | 某些能力（指令遵循、代码）通过 SFT+RLHF 的提升大于预训练 |
| Multimodality | Image + text tokens scale together; separate curves per modality |
| 多模态 | 图像 + 文本 token 一起扩展；每种模态有独立曲线 |
| Synthetic data | Models generate training data; effective compute can compound |
| 合成数据 | 模型生成训练数据；有效计算可复合增长 |

> **【拓展：合成数据与缩放定律的未来】**Năm 2026 quy định thu nhỏ đối mặt với vấn đề tường dữ liệu Hàm lượng dữ liệu văn bản con người có thể sẽ hết hạn trong vài năm tới. DATA tổng hợp (từ các mô hình tạo ra dữ liệu) là giải pháp tiềm năng. Phi của Microsoft sử dụng GPT-4 sinh ra "cách sách chất lượng" dữ liệu tổng hợp để thực hiện đào tạo, Nemotron của NVIDIA sử dụng dữ liệu tổng hợp tăng cường. Nếu dữ liệu tổng hợp có hiệu quả, quy định thu nhỏ có hiệu quả có thể tiếp tục tăng trưởng.

Máy tối ưu hóa Muon (Kimi Moonlight, 2024) cho thấy tăng hiệu quả tính toán ~ 2x so với AdamW ở dữ liệu phù hợp. Một số chạy đào tạo 2026 sử dụng Muon mặc định.

> Muon 优化器(Kimi Moonlight,2024) trên cùng dữ liệu cho thấy tăng tính toán hiệu quả hơn khoảng 2 lần so với AdamW. Một số bài tập năm 2026 được sử dụng tùy chọn Muon. Nó thay đổi số thường tuyệt đối của quy luật giảm, thay vì hình dạng của nó.

## Hãy xây dựng nó.
```figure
scaling-laws
```

## Hãy xây dựng nó

Nhìn xem`code/main.py`Chúng ta thực hiện phương trình mất mát của Chinchilla và giải quyết cho tính toán tối ưu`(N, D)`trong mỗi số các ngân sách tính toán.

> 参见 `code/main.py`Chúng tôi thực hiện phương trình mất mát Chinchilla, và tìm kiếm giải pháp tốt nhất trong nhiều ngân sách tính toán.`(N, D)`

### Bước 1: mất Chinchilla

```python
def chinchilla_loss(N, D, A=406.4, B=410.7, alpha=0.34, beta=0.28, E=1.69):
    return A / N ** alpha + B / D ** beta + E
```

Hình ảnh`L`như một đường viền trên `(N, D)`ở mức cố định `C = 6ND`Tìm tối thiểu.

> sẽ`L`作为 `(N, D)`     `C = 6ND`❖ tìm giá trị tối thiểu.

### Bước 2: Biên giới tối ưu tính toán

Đối với ngân sách tính toán từ `1e17`đến`1e25`FLOPs, tìm `(N, D)`giảm thiểu thiệt hại theo quy định của:`6ND = C`- Kiểm tra tỷ lệ`D/N ≈ 20`- Tôi không biết.

> Đối với`1e17`Đến`1e25`FLOPs của tính toán ngân sách, tìm kiếm để giảm thiểu thiệt hại `(N, D)`,约束 `6ND = C`❖ tỷ lệ chứng minh`D/N ≈ 20`

### Bước 3: chi phí quá trình đào tạo

Xét thêm tổn thất bạn trả để đào tạo một mô hình nhỏ hơn 10 × (1/10 của tối ưu N, 10 × tối ưu D).

> 计算训练一个 10倍小模型(最优 N 的 1/10,最优 D 的 10倍) 付出的额外损失──报告作为交换的推理 FLOP 节约(与 N 成正比)──

### Bước 4: so sánh với các mô hình thực

Đưa vào biết `(N, D)`cặp cho GPT-3, Chinchilla, Llama 3 8B, DeepSeek- V3 (chỉ số hoạt động), và so sánh dự đoán so với tổn thất được báo cáo.

> 输入 GPT-3、Chinchilla、Llama 3 8B、DeepSeek-V3(活跃参数) của đã biết `(N, D)`Đối với, so sánh dự báo mất mát với báo cáo mất mát.

## Hãy sử dụng nó để thực hiện

Bạn không thể tự đào tạo một mô hình biên giới, nhưng luật quy mô cho bạn biết:

> Bạn không thể tự tập luyện mô hình tiền tuyến... nhưng quy luật quy mô cho bạn biết:

1. **Whether your fine-tune has enough data.**Nếu dữ liệu cụ thể của bạn là dưới 20 token mỗi param của mô hình cơ bản, mong đợi bão hòa ở một số mức thua lỗ.
   Trung ngữ翻译:**你的微调是否有足够数据。**Nếu nhiệm vụ của bạn ít hơn dữ liệu cơ bản của mô hình 20 điểm, dự kiến sẽ ở một số lỗ hổng.
2. **Whether to pick a bigger base model.**Nếu bạn đang chi tiêu tất cả ngân sách của mình cho suy luận, hãy chọn một mô hình nhỏ hơn, được đào tạo lâu hơn.
   Trung ngữ翻译:**是否选择更大的基础模型。**Nếu bạn dành tất cả ngân sách vào suy nghĩ, ưu tiên chọn mô hình nhỏ hơn, tập luyện lâu hơn.
3. **Where the returns diminish.**Ngoài 1000x Chinchilla tối ưu, thay đổi mất gỗ trở thành tiếng ồn.
   Trung ngữ翻译:**收益递减在哪里。**n hơn 1000 lần tối ưu của Chinchilla, biến đổi về số mất thành tiếng ồn.

**The research trajectory in 2026:**

> **2026 年的研究方向：**

- **Data-constrained regime.**Web có một số lượng giới hạn của các token chất lượng cao (~ 510 nghìn tỷ tiếng Anh sau khi lọc). Bước trước hàng rào đang tiến gần ngưỡng này. Dữ liệu tổng hợp, đa ngôn ngữ, đa phương pháp và điều chỉnh tinh tế theo quy mô RLHF là các đòn bẩy tiếp theo.
  Trung ngữ翻译:**数据受限时代。**Số lượng mã thông báo chất lượng cao trên mạng có giới hạn.
- **Compute-multiplier tricks.**Muon Optimizer, MoE, data curation tốt hơn  mỗi thay đổi các định vị tuyệt đối, không phải asymptote.
  Trung ngữ翻译:**计算倍增技巧。**Muon 优化器, MoE, better data策展 mỗi người thay đổi số thường nhất định, chứ không phải là dòng tiến gần.
- **Scaling laws for RL.**Câu hỏi mở: bằng chứng sớm cho thấy luật quyền lực trong các mẫu RL nhưng với các biểu tượng rất khác so với trước khi tập luyện.
  Trung ngữ翻译:**RL 的缩放定律。** Open Problem:  Các bằng chứng sớm cho thấy RL mẫu có mối quan hệ hợp pháp, nhưng chỉ số và dự kiến đào tạo không giống nhau.

## Chuyển nó đi.

Nhìn xem`outputs/skill-training-budget-estimator.md`- Nghề chọn kỹ năng`(N, D, hours, GPU)`cho một cuộc đào tạo mới với ngân sách tính toán, hạn chế triển khai và mất mục tiêu.

> 参见 `outputs/skill-training-budget-estimator.md` Kỹ năng này 根据计算预算,部署约束和目标损失,为新训练运行选择 `(N, D, hours, GPU)`

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`- Bác in Chinchilla tối ưu`(N, D)`cho ngân sách tính toán `1e20`- `1e22`- `1e24`So sánh với cái bàn mô hình thực.
   Trung ngữ翻译:运行 `code/main.py`❖ 打印计算预算为 `1e20``1e22``1e24`时的Chinchilla 最优 `(N, D)`                                                                                                                                                                                                                                                              
2. **Medium.**Thực hiện đường cong mất tích như hàm của máy tính Hoffmann.`log10(C)`Để xác định khi nào luật pháp dự đoán chúng ta cần`>10^28`FLOPs cho việc giảm 0,1 lần nữa trong sự chuyển động.
   Trung文翻译:实现 Hoffmann 损失-计算量曲线――绘制计算最优前沿的损失对`log10(C)`❖ xác định định định luật dự đoán何时需要 `>10^28`FLOPs 才能使交叉再降低 0.1──
3. **Hard.**Đáp ứng luật quy mô của riêng bạn trên 5 mô hình nhỏ (100K đến 10M params) được đào tạo trên cùng một tập dữ liệu.`α`và `E`Các tác giả của anh phù hợp với những tác giả được công bố như thế nào?
   Trung ngữ翻译: 在相同数据集上训练 5 个小模型 ((100K 到 10M参数)并适应自己的缩放定律──估计`α`和 `E`◊ Chỉ số của bạn phù hợp với giá trị phát hành như thế nào?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Parameters (N) | "Model size" | Non-embedding weight count; determines capacity. |
| 参数 (N) | "模型大小" | 非嵌入权重数量；决定容量。 |
| Tokens (D) | "Training data" | Number of training tokens seen; determines how well the parameters get used. |
| Token (D) | "训练数据" | 看到的训练 token 数量；决定参数被利用的程度。 |
| Compute (C) | "FLOPs spent" | Approximately `6 × N × D` for a standard transformer. |
| 计算量 (C) | "FLOPs 花费" | 标准 Transformer 约为 `6 × N × D`。 |
| Chinchilla-optimal | "D/N ≈ 20" | Ratio that minimizes loss per FLOP of pretraining. |
| Chinchilla 最优 | "D/N ≈ 20" | 最小化每个预训练 FLOP 损失的比例。 |
| Over-training | "Past Chinchilla" | Spend extra training FLOPs to save inference FLOPs; D/N >> 20. |
| 过度训练 | "超过 Chinchilla" | 额外训练 FLOPs 以节省推理 FLOPs；D/N >> 20。 |
| Irreducible loss | "The floor" | The `E` term in the scaling law; the entropy of the data itself. |
| 不可约损失 | "底线" | 缩放定律中的 `E` 项；数据本身的熵。 |
| Emergent capability | "Sudden jumps at scale" | Often a scorer artifact; continuous loss is smooth. |
| 涌现能力 | "规模上的突然跳变" | 通常是评分伪影；连续损失是平滑的。 |
| Effective compute | "Training-efficiency multiplier" | Better data / optimizer / architecture multiplies how far a FLOP goes. |
| 有效计算 | "训练效率倍增器" | 更好的数据/优化器/架构使每个 FLOP 走得更远。 |

## Xem thêm 延伸阅读

- [Kaplan et al. (2020). Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361) bài báo luật quy mô đầu tiên; chưa được đào tạo.
  Trung ngữ翻译:第一篇缩放定律论文;低估训练了──
- [Hoffmann et al. (2022). Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556) Chinchilla.
  Trung ngữ翻译:Chinchilla 论文。
- [Schaeffer et al. (2023). Are Emergent Abilities of Large Language Models a Mirage?](https://arxiv.org/abs/2304.15004) xuất hiện như một vật tạo ra phép đo.
  Trung ngữ翻译:涌现能力是否是幻觉的论文──
- [Sardana, Frankle (2024). Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws](https://arxiv.org/abs/2401.00448) tại sao việc đào tạo quá mức của Llama là điều thích hợp cho khối lượng công việc của nó.
  Trung ngữ翻译:为什么Llama's overtraining to its workload is correct──
- [Jordan et al. (2024). Muon: An optimizer for hidden layers in neural networks](https://kellerjordan.github.io/posts/muon/) 2x nhân tính toán.
  Trung文翻译:Muon 优化器,2 倍计算倍增器。
