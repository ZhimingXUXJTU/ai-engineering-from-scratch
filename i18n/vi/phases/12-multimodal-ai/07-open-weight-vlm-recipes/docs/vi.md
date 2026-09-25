# Công thức VLM trọng lượng mở: Điều thực sự quan trọng  开源视觉语言模型配配方: thực sự quan trọng yếu tố

> Văn học VLM trọng lượng mở 2024-2026 là một khu rừng của bảng phân hủy. MM1 của Apple đã thử nghiệm 13 kết hợp mã hóa hình ảnh, kết nối và hỗn hợp dữ liệu. Molmo của Allen AI đã chứng minh các bản tóm tắt chi tiết của con người vượt qua việc chưng cất GPT-4V. Cambrian-1 đã chạy 20 + so sánh mã hóa. Idefics2 đã chính thức hóa không gian thiết kế năm trục. Các VLM Prismatic so sánh 27 công thức đào tạo trên một chỉ số chuẩn bị kiểm soát. Trong tất cả những tiếng ồn đó, một tập hợp nhỏ kết quả có thể được ghi trên giấy tờ: mã hóa hình ảnh quan trọng hơn kiến trúc kết nối, hỗn hợp dữ liệu quan trọng hơn cả hai, và các tiêu đề chi tiết của con người vượt qua dữ liệu tổng hợp được chưng cất. Bài học này đọc các bảng đó để bạn không cần phải.

> **【中文解读】**2024-2026 năm mở nguồn VLM 论文 đầy đủ với rất nhiều thử nghiệm tiêu thụ. Bài học này từ Apple MM1、Allen AI Molmo、Cambrian-1、Idefics2、Prismatic VLMs 等论文中提炼出核心结论:编码器比连接器架构更重要,数据混合比编码器更重要,详细的人工描述胜于蒸数据──

> **【拓展：VLM 工程的实践指南】**Kết luận của bài học này trực tiếp hướng dẫn thực tế kỹ thuật VLM. Khi bạn thấy hiệu suất VLM không đạt tiêu chuẩn, bạn nên theo các ưu tiên sau đây: 1) số lượng mã thông báo trực quan có đủ không? 60% 方差), 2) 编码器选择是否合适? 20%), 3) 数据质量是否足够 ((10%), 4) 连接器架构 ((5%,几乎不影响) ;;

**Type:** Learn + lab  | **类型：学习 + 实验**
**Languages:** Python (stdlib, ablation table parser + recipe picker)  | **语言：Python（标准库，消融表解析器 + 配方选择器）**
**Prerequisites:** Phase 12 · 05 (LLaVA baseline)  | **前置：阶段12第05课（LLaVA基线）**
**Time:** ~180 minutes  | **时长：约180分钟**

>  **【前置】**Học本节前请先掌握:Phase 12·02-06(CLIP/BLIP-2/Flamingo/LLaVA/NaFlex 全套);Phase 11·08(Instruction Tuning)。本节是Phase 12 前半段的总结:所有架构都学过了,现在看看哪些选择真正重要。
>  **【类比】**开源 VLM 五轴选择 = "买车选配置"──编码器 = 发动机(性能差 5-7分);连接器 = 中控台界面(几乎不影响驾驶);LLM = 车身大小;数据 = 油品(差油再好的发动机也跑不快);分辨率 = 轮胎(决定能跑什么地形)──纠结界面(连接器) là những rào cản mới,老司机优先看发动机和油。

## Mục tiêu học tập

- Tên không gian thiết kế VLM năm trục: mã hóa hình ảnh, kết nối, LLM, data mix, thời gian phân giải.
- Đọc bảng phân tích MM1 / Idefics2 / Cambrian-1 và dự đoán nút nào di chuyển một điểm chuẩn nhất định.
- Chọn một công thức (code, kết nối, dữ liệu, độ phân giải) cho một VLM mới với một ngân sách tính toán và hỗn hợp nhiệm vụ.
- Hãy giải thích tại sao các bản tóm tắt chi tiết của con người lại đánh bại việc chưng cất GPT-4V ở cùng một số lượng mã thông báo.

## Vấn đề  vấn đề nền

Có hàng trăm VLM có trọng lượng mở. Hầu hết khoảng cách giữa "tốt" và "đại cấp" không phải là kiến trúc. Đó là dữ liệu, lịch trình độ phân giải và lựa chọn mã hóa. Biết phải xoay đầu tiên khi mô hình của bạn hoạt động kém sẽ giúp bạn tiết kiệm một lỗi 5 triệu GPU-tham.

Làn sóng 2023 (LLaVA-1.5, InstructBLIP, MiniGPT-4) chạy trên cặp tiền huấn luyện + LLaVA-Instruct-150k.

Làn sóng 2024 (MM1, Idefics2, Molmo, Cambrian-1, Prismatic VLMs) đã chạy các vụ trừu tượng đầy đủ.

> **【中文解读】**Trong hàng trăm VLM nguồn mở, sự khác biệt giữa "tốt" và "tốt nhất" chủ yếu không phải là cấu trúc, mà là dữ liệu, độ phân giải điều chỉnh và chọn bộ lập trình.

## Khái niệm cốt lõi

### Không gian thiết kế 5 trục

Idefics2 (Laurençon et al., 2024) đã đặt tên các trục:

1. Bộ mã hóa hình ảnh / 图像编码器. CLIP ViT-L/14, SigLIP SO400m/14, DINOv2 ViT-g/14, InternViT-6B. Các bộ mã hóa khác nhau về kích thước váy, độ phân giải và mục tiêu trước khi đào tạo / 编码器在补丁大小、分辨率和预训目标上各不相同.
2. Kết nối / 连接器. MLP (2-4 lớp), Q-Former (32 truy vấn + chéo-attn), Perceiver Resampler (64 truy vấn), C-Abstractor (tích hợp hợp xoắn + hai tuyến) / MLP(2-4 tầng)、Q-Former(32查询+交叉注意力)、Perceiver 重采样器(64查询)、C-Abstractor(卷积+双线性池化).
3. Mô hình ngôn ngữ / 语言模型. Llama-3 8B / 70B, Mistral 7B, Phi-3, Gemma-2, Qwen2.5.
4. Dữ liệu đào tạo / 训练数据. cặp phụ đề (CC3M, LAION), liên kết (OBELICS, MMC4), hướng dẫn (LLaVA-Instruct, ShareGPT4V, PixMo, Cauldron) / 描述对、交错数据、指令数据.
5. Định hướng phân giải / phân giải độ调度. cố định 224/336/448, AnyRes, động lực bản địa. Ramped trong đào tạo hoặc liên tục /  cố định phân giải、AnyRes、原生动态分辨率── đào tạo trong quá trình tăng hoặc恒定.

Mỗi sản xuất VLM đưa ra một lựa chọn trên mỗi trục. Hầu hết sự khác biệt trong điểm số MMMU được giải thích bởi trục 1, 4, và 5  chứ không phải bởi các kết nối bạn chọn.

> **【中文解读】**Mỗi VLM được lựa chọn trên 5 trục. Phần lớn các phân số MMMU khác nhau bởi trục1 (xế) ⋅xế4 (xế) ⋅ dữ liệu (xế) ⋅ phân giải (xế) ⋅ phân giải (xế) ⋅ thay vì bạn chọn kết nối nào.

### Trục 1: mã hóa > kết nối 编码器 > kết nối

MM1 Phần 3.2 cho thấy: trao đổi từ CLIP ViT-L/14 sang SigLIP SO400m/14 thêm 3 điểm MMMU. Thay đổi các kết nối từ MLP sang nhận dạng Resampler thêm ít hơn 1 điểm. Idefics2 sao chép: SigLIP > CLIP, Q-Former ≈ MLP ≈ nhận dạng với cùng số lượng mã thông báo.

Cambrian-1 "Cambrian Vision Encoders Match-Up" (Tong et al., 2024) chạy 20 + bộ mã hóa trên một tiêu chuẩn trung tâm tầm nhìn (CV-Bench).

Mã mã mặc định 2026 cho VLM mở là SigLIP 2 SO400m/14 cho các tính năng ngữ nghĩa + mật, đôi khi được kết nối với các tính năng DINOv2 ViT-g/14 (Cambrian's "Spacial Vision Aggregator" làm điều này).

> **【中文解读】**换编码器(CLIP→SigLIP)加3+ 分 MMMU,换连接器(MLP→Perceiver)加不到1分──2026年开源 VLM的默认编码器是SigLIP 2 SO400m/14,有时与DINOv2 ViT-g/14拼接(Cambrian的"空间视觉聚合器"就是这样做的)──

> ️ **【易错点】**Người mới thường mắc kẹt trong cái bẫy của "调连接器架构" cho rằng Q-Former 更优雅就更值得研究──事实是连接器架构只贡献 1% 方差,把时间花在更换更好的编码器(CLIP→SigLIP 2) 和增加代币 数上更有性价比──修复:先使用2层 MLP + SigLIP 2 跑基线,再考虑复杂性──

### Trục 2: Thiết kế kết nối là một sự rửa sạch.

MM1, Idefics2, Prismatic và MM-Interleaved đều đạt được kết luận tương tự: với số lượng mã thị giác cố định, kiến trúc kết nối hầu như không quan trọng.

Điều quan trọng là số lượng token. Nhiều token hình ảnh hơn = tính toán LLM hơn = hiệu suất tốt hơn đến một điểm, sau đó giảm lợi nhuận. 64 token mỗi hình ảnh là quá ít cho OCR. 576-1024 token là điểm ngọt ngào cho hầu hết các VLM mở. 2048+ chỉ giúp cho tài liệu và biểu đồ.

Q-Former vs MLP là một câu hỏi về chi phí, không phải là một câu hỏi về chất lượng: Q-Former giới hạn các token ở 32-64 bất kể độ phân giải hình ảnh; MLP phát ra tất cả các token patch. Đối với các đầu vào độ phân giải cao, Q-Former lưu trữ bối cảnh LLM; cho độ phân giải thấp, sự khác biệt là tiếng ồn.

> **【中文解读】**Trong số lượng token hình ảnh cố định, cấu trúc kết nối hầu như không ảnh hưởng đến hiệu suất.2.2 tầng MLP và 32 查询 Q-Former khoảng cách là trong 1 phút.

### Trục 3: Mức độ LLM đặt trần

Tăng gấp đôi LLM từ 7B đến 13B một cách đáng tin cậy thêm 2-4 điểm trên MMMU trên mỗi bài báo VLM. Ở 70B bạn bão hòa hầu hết các điểm chuẩn. Mức giới hạn lý luận đa phương thức của VLM là giới hạn lý luận văn bản của LLM  bộ mã hóa thị giác chỉ có thể cung cấp nó, không phải lý do cho nó.

Đây là lý do tại sao Qwen2.5VL-72B và Claude Opus 4.7 đập vỡ MMMU-Pro và ScreenSpot-Pro: bộ não ngôn ngữ là rất lớn. Một VLM 7B không thể thay thế cho một VLM 70B thông qua thiết kế kết nối thông minh.

> **【中文解读】**LLM 翻倍(7B→13B) ổn định tăng 2-4 分 MMMU──70B 时大多数基准和──VLM 的多模态推理天花板就是LLM 的文本推理天花板视觉编码器只能""数据,不能取代推理──这就是为什么72B 参数的VLM 能压7B 的语言脑规模不可替代的原因──

### Dòng 4: dữ liệu  chi tiết người tiêu đề vượt qua chưng cất DATA: Kỹ thuật mô tả chiến thắng qua hơi 

Molmo + PixMo (Deitke et al., 2024) là kết quả 2024 mà mọi người nên đọc. Allen AI đã có các nhà ghi chú con người mô tả hình ảnh trong 1-3 phút mật độ nói chuyện-đối với văn bản, tạo ra 712K hình ảnh có nét mật. Không có khử trùng GPT-4V ở bất cứ đâu trong dữ liệu đào tạo.

Molmo-72B đánh bại Llama-3.2-90B-Vision trên 11 trong 11 điểm chuẩn. Delta không phải là kiến trúc  nó là chất lượng caption. Các tựa đề chi tiết của con người chứa 5-10 lần nhiều thông tin mỗi hình ảnh so với các tựa đề web ngắn và ở lại thực tế được đặt nền trong khi phân tán GPT-4V ảo giác.

ShareGPT4V (Chen et al., 2023) và Cauldron (Idefics2) đã theo dõi cùng một cuốn sách chơi với các tiêu đề người + GPT-4V hỗn hợp.

> **【中文解读】**Phát hiện cốt lõi của Molmo: để người đánh dấu sử dụng 1-3 phút mô tả âm thanh dày đặc hình ảnh, nhận được 712K 张高质量标注图像, hoàn toàn không sử dụng GPT-4V 蒸── Molmo-72B trong 11/11 基准 trên đánh bại Llama-3.2-90B-Vision── khoảng cách không cấu trúc là mô tả chất lượng── chi tiết nhân tạo mô tả mỗi张图的信息量是短网络描述的 5-10倍,且实确准确,不像GPT-4V 数据会"继承"蒸幻觉──

> **【拓展：数据质量的投资回报】**Phát hiện này có một ý nghĩa quan trọng đối với lĩnh vực xây dựng thẳng đứng VLM: với việc chi tiêu rất nhiều năng lực điều chỉnh cấu trúc, không giống như đầu tư các nguồn lực để có được lượng dữ liệu trong lĩnh vực chất lượng cao. Trong bối cảnh tài chính, việc sử dụng các nhân viên chuyên nghiệp để đánh dấu báo cáo, phát hành, mô tả hình ảnh hợp đồng sẽ có hiệu quả tốt hơn so với việc sử dụng GPT-4V tự tạo dữ liệu.

### Vòng 5: độ phân giải và lịch trình phân giải và điều chỉnh

Idefics2's ablations: 384 -> 448 thêm 1-2 điểm. 448 -> 980 với phân chia hình ảnh (AnyRes) thêm 3-5 điểm khác trên các tiêu chuẩn OCR.

Cambrian-1 đã thực hiện một sự đổi giá độ phân giải so với token: với tính toán cố định, bạn có thể có nhiều token với độ phân giải thấp hơn hoặc ít token với độ phân giải cao hơn.

Công thức sản xuất năm 2026: tàu giai đoạn 1 ở 384 cố định, giai đoạn 2 với độ phân giải động lên đến 1280 cho các nhiệm vụ nặng OCR.

> **【中文解读】**Độ phân giải tăng từ 384 lên 448 tăng 1-2 分,448 lên 980 ((加 AnyRes) trên cơ sở OCR tăng thêm 3-5 分.

### Prismatic kiểm soát so sánh Prismatic kiểm soát so với thí nghiệm

Prismatic VLMs (Karamcheti et al., 2024) là bài báo kiểm soát tất cả các trục.

- Số lượng biểu tượng hình ảnh cho mỗi hình ảnh giải thích khoảng 60% sự khác biệt.
- Sự lựa chọn của bộ mã hóa giải thích ~ 20%.
- Thiết kế kết nối giải thích ~ 5%.
- Mọi thứ khác (data mix, scheduler, LR) phần còn lại là ~15%.

Đây là một sự phân hủy thô lỗ, nhưng nó là câu trả lời sạch nhất cho "điều gì tôi nên bỏ đi trước" trong văn học.

> **【中文解读】**Prismatic VLM là những thí nghiệm kiểm soát sạch nhất cùng 13B LLM cùng chỉ dẫn dữ liệu cùng đánh giá, mỗi lần chỉ thay đổi một轴 kết luận: thị giác mã số(60%)> 编码器(20%)> 其余(15%)> 连接器(5%)── đây là " nên đầu tiên tiêu融什么" là câu trả lời tốt nhất.

### Một người chọn cho năm 2026

Với bằng chứng, công thức mở VLM mặc định cho một dự án mới vào năm 2026:

- Mã hóa / 编码器: SigLIP 2 SO400m/14 ở độ phân giải bản địa với NaFlex, kết nối với DINOv2 ViT-g/14 cho các tính năng dày đặc nếu bạn cần phân đoạn / đặt đất / 如需分割/定位则拼接 DINOv2.
- Kết nối / 连接器: MLP 2 tầng trên mã thông báo vá. Trượt Q-Former trừ khi bạn bị hạn chế mã thông báo / 除非 mã thông báo 受限制否则跳过 Q-Former.
- LLM / 语言模型: Qwen2.5 / Llama-3.1 / Gemma 2, 7B cho chi phí / 成本优先选7B, 70B cho chất lượng /质量优先选70B, được chọn theo độ trễ mục tiêu / 按延迟目标选择.
- Dữ liệu / dữ liệu: PixMo + ShareGPT4V + Cauldron, được bổ sung với dữ liệu hướng dẫn cụ thể về nhiệm vụ / 补充任务特定指令数据.
- Độ phân giải / phân giải: động (min 256, tối đa 1280 pixel mỗi bên dài) / 动态( tối thiểu 256,最大1280像素 mỗi长边).
- Chương trình / 调度: Lớp nối giai đoạn 1 (chỉ chiếu máy chiếu / 仅投影器), giai đoạn 2 hoàn chỉnh chỉnh / 全参数微调, giai đoạn 3 nhiệm vụ cụ thể chỉnh / 任务特定微调.

Mỗi một trong những mặc định này bắt nguồn từ một sự giảm cân đo lường trong các báo cáo được trích dẫn ở cuối bài học này.

> **【中文解读】**Trên đây là những kết quả của các thử nghiệm tiêu hủy trong bài viết được trích dẫn trong bài học này. Đây là cách tốt nhất để bắt đầu xây dựng dự án VLM mới vào năm 2026.

## Hãy dùng nó để thực hành
```figure
l5-vlm-recipe-knobs
```

## Sử dụng nó

`code/main.py`là một trình phân tích bảng phân hủy và chọn công thức. Nó mã hóa các bảng phân hủy MM1 và Idefics2 (đồng nhất) và cho phép bạn truy vấn:

- "Giả sử ngân sách X và nhiệm vụ Y, công thức nào sẽ thắng?"
- "Nếu tôi đổi SigLIP thành CLIP trên một 7B Llama, dự kiến delta MMMU là gì?"
- "Tôi nên chọn trục nào trước tiên để có được câu trả lời 80% tự tin?"

Kết quả là một danh sách công thức xếp hạng với các điểm tham khảo dự kiến và một khuyến nghị "blah trước".

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-vlm-recipe-picker.md`. Với một kết hợp nhiệm vụ mục tiêu, ngân sách tính toán và mục tiêu trễ, nó phát hành một công thức đầy đủ (code, kết nối, LLM, kết hợp dữ liệu, lịch trình giải quyết) với các trích dẫn đến việc trừ bỏ biện minh cho mỗi lựa chọn.

> **【中文解读】**本课产出 VLM 配方选择工具――给定目标任务组合、计算预算和延迟目标,输出完整配方,每项选择都附文消融实验的引用――避免工程师每次新开VLM 项目都必须重新做 Idefics2 消融表――

## Tập luyện bài tập

1. Đọc MM1 Phần 3.2. Đối với một LLM 2B cố định với ngân sách 50M hình ảnh, mã hóa nào thắng?
   | 阅读 MM1 第 3.2 节。在固定 2B LLM 和 50M 图像预算下，哪个编码器最优？在 13B LLM 时答案会翻转吗？为什么？

2. Cambrian-1 phát hiện ra rằng kết nối DINOv2 + SigLIP vượt trội hơn chỉ riêng trên các điểm tham khảo tập trung vào tầm nhìn nhưng không thêm tín hiệu nào trên MMMU.
   | Cambrian-1 发现 DINOv2+SigLIP 拼接在视觉中心基准上优于单独使用，但在 MMMU 上无增益。预测哪些基准提升、哪些持平。

3. Mục tiêu của bạn là một đại lý UI di động trên một 2B LLM. Chọn bộ mã hóa, kết nối, độ phân giải và kết hợp dữ liệu. Định lý cho mỗi lựa chọn bằng một bảng ablation cụ thể.
   | 目标是在 2B LLM 上构建移动端 UI 代理。选择编码器、连接器、分辨率和数据混合，用具体消融表论证每个选择。

4. Molmo bán mẫu 4B và 72B. 4B cạnh tranh với các VLM 7B đóng cửa; 72B đánh bại Llama-3.2-90B-Vision trên các điểm chuẩn 11/11. Điều đó cho bạn biết gì về giả thuyết cao nguyên kích thước LLM?
   | Molmo 的 4B 模型与闭源 7B VLM 竞争力相当；72B 在 11/11 基准上击败 Llama-3.2-90B-Vision。这对 LLM 规模饱和假说意味着什么？

5. Thiết kế một bảng phân hủy để tách chất lượng hỗn hợp dữ liệu từ chất lượng mã hóa trên một VLM 7B.
   | 设计消融实验表，在 7B VLM 上隔离数据混合质量和编码器质量。最少需要多少次训练？提出四组轴设置。

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Ablation | "Turning one knob" | Training multiple runs that differ in exactly one design-space axis, holding everything else constant | 消融实验：只改变一个设计轴、保持其他不变的多组训练 | |
| Connector | "Bridge" / "projector" | Trainable module that maps vision encoder output into the LLM's token space (MLP, Q-Former, Perceiver) | 连接器：将视觉编码器输出映射到 LLM token 空间的可训练模块 | |
| Detailed human caption | "Dense caption" | A multi-sentence human-written description (typically 80-300 tokens) richer than a web alt text | 详细人工描述：人类编写的多句描述（通常80-300 token） | |
| Distillation | "GPT-4V captions" | Training data generated by a stronger proprietary VLM; convenient but prone to inherited hallucination | 蒸馏：用更强的专有 VLM 生成训练数据；方便但会继承幻觉 | |
| AnyRes / dynamic res | "High-res path" | Strategy to feed images larger than the encoder's native resolution via tiling or M-RoPE | AnyRes/动态分辨率：通过切片或 M-RoPE 处理超过编码器原生分辨率的图像 | |
| Resolution ramp | "Curriculum" | Training schedule that starts low-resolution and increases, speeding alignment learning | 分辨率递增：从低分辨率开始逐步增加的训练调度 | |
| Vision-centric bench | "CV-Bench / BLINK" | Evaluation that stresses fine-grained visual perception rather than language-heavy reasoning | 视觉中心基准：测试精细视觉感知能力而非语言推理 | |
| PixMo | "Molmo's data" | Allen AI's 712K densely-captioned image dataset; human speech transcribed into dense captions | Allen AI 的 712K 密集标注图像数据集；人工语音转录为密集描述 | |

## Xem thêm 延伸阅读

- [McKinzie et al. — MM1 (arXiv:2403.09611)](https://arxiv.org/abs/2403.09611) Apple MM1 nhiều mô hình mô hình tiêu hóa kinh nghiệm
- [Laurençon et al. — Idefics2 / What matters building VLMs (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) Các yếu tố quan trọng để xây dựng VLM
- [Deitke et al. — Molmo and PixMo (arXiv:2409.17146)](https://arxiv.org/abs/2409.17146) Molmo và PixMo
- [Tong et al. — Cambrian-1 (arXiv:2406.16860)](https://arxiv.org/abs/2406.16860) Cambrian-1
- [Karamcheti et al. — Prismatic VLMs (arXiv:2402.07865)](https://arxiv.org/abs/2402.07865) VLM Prismatic  kiểm soát trải nghiệm tiêu hủy
