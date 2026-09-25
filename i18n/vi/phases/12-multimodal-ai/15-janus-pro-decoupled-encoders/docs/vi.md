# Janus-Pro: Các mã hóa tách rời cho mô hình đa mô hình thống nhất

> Các mô hình đa phương tiện thống nhất có một căng thẳng không thể tránh khỏi. Hiểu cần các tính năng ngữ nghĩa  Các vector đầu ra SigLIP hoặc DINOv2 giàu thông tin cấp khái niệm. Thế hệ muốn có mã thân thiện với tái thiết  mã thông báo VQ kết hợp lại thành các pixel sắc nét. Hai mục tiêu không tương thích trong một bộ mã hóa duy nhất. Janus (DeepSeek, tháng 10 năm 2024) và Janus-Pro (DeepSeek, tháng 1 năm 2025) cho rằng giải pháp là ngừng cố gắng: tách hai bộ mã hóa. Chia sẻ cơ thể biến đổi giữa các nhiệm vụ, nhưng hướng hiểu thông qua SigLIP và phát triển thông qua một token VQ. Ở 7B, Janus-Pro đánh bại DALL-E 3 trên GenEval trong khi so sánh LLaVA trên MMMU. Bài học này giải thích tại sao hai bộ mã hóa hoạt động khi một thất bại.

> **【中文解读】**Janus-Pro(DeepSeek,2025年1月) giải quyết một sự mâu thuẫn cơ bản: hiểu nhiệm vụ cần语义特征(SigLIP),生成任务需要重建友好的编码(VQ token) ・・・两者无法兼容单一编码器──Janus-Pro的答案是解:理解走 SigLIP 路径,生成走 VQ 路径,共享变压器 主体──7B 参数就在 GenEval 上击败了DALL-E 3──

> **【拓展：解耦编码器的产业影响】**解编码器思想 đã trở thành cấu trúc mặc định của mô hình thống nhất năm 2026  InternVL-U sẽ tích hợp nó vào khuôn khổ đào tạo dự kiến đa dạng.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, dual-encoder routing + shared-body signal) | **语言:** Python（标准库，双编码器路由 + 共享体信号）
**Prerequisites:** Phase 12 · 13 (Transfusion), Phase 12 · 14 (Show-o) | **前置知识:** Phase 12 · 13（Transfusion），Phase 12 · 14（Show-o）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**学本节前请先掌握:Phase 12·02(SigLIP 语义编码器) Phase 12·13-14(Transfusion/Show-o 统一模型) Phase 8(VQ-VAE 重建编码器) Janus-Pro = "tuyên tắc đối với sinh成的编码器分离"是Phase 12 多模态生成模型的最终答案之一──
>  **【类比】**Janus-Pro = "được làm việc trong bộ não"――左脑 = SigLIP(语义理解,认识"猫"的概念);右脑 = VQ-VAE(像素重建,能画出猫的细节) ――其他统一模型 = 强迫一个脑区同时做两件事,两边都不极致;Janus-Pro = 接受左右脑分工,共享脑干(Transformer 主体) làm suy luận cao层――就像人类视觉皮层理解这个() 和运动皮层(绘画) 本来就在不同脑区.

## Mục tiêu học tập

- Giải thích tại sao một bộ mã hóa được chia sẻ duy nhất làm tổn hại đến sự hiểu biết hoặc chất lượng sản xuất.
  > 解释 tại sao đơn chia sẻ bộ lập trình sẽ làm tổn hại sự hiểu biết hoặc tạo chất lượng.
- Mô tả định tuyến của Janus-Pro: Các tính năng SigLIP trên phía đầu vào để hiểu, token VQ trên cả đầu vào và đầu ra để tạo ra.
  > Mô tả đường dẫn của Janus-Pro: hiểu đường dẫn nhập bên sử dụng đặc điểm SigLIP, tạo đường dẫn nhập và ra ngoài bên sử dụng token VQ。
- Theo dõi quy mô kết hợp dữ liệu làm cho Janus-Pro thành công nơi mà Janus không.
  > 追溯让Janus-Pro thành công và Janus 失败的数据混合扩展──
- So sánh các kiến trúc tách rời (Janus-Pro), nối tiếp (Transfusion) và nối kín (Show-o).
  > 比较解(Janus-Pro) 合连续(Transfusion) 合离散(Show-o) 三种架构──

## Vấn đề  vấn đề nền

Các mô hình thống nhất chia sẻ một cơ thể biến đổi trên cả sự hiểu biết và sản xuất. Những nỗ lực trước đây (Chameleon, Show-o, Transfusion) đều sử dụng một token thị giác cho cả hai hướng. Tokenizer là một thỏa hiệp:

> 统一模型在理解和生成之间共享 Transformer 主体──之前的尝试(Chameleon、Show-o、Transfusion) đều sử dụng một hình ảnh分词器 xử lý hai hướng──分词器是妥协:

- Được tối ưu hóa để tái tạo (thế hệ): VQ-VAE chụp chi tiết pixel hạt mỏng nhưng tạo ra các token có sự liên kết ngữ nghĩa yếu.
  Trung文翻译:为重建优化(生成):VQ-VAE 捕获细粒度像素细节, nhưng phát sinh biểu tượng 语义一致性弱──
- Được tối ưu hóa cho ngữ nghĩa (nghiểu): SigLIP nhúng nhóm hình ảnh "cat" gần các token "cat" nhưng không cho phép tái tạo tốt.
  Trung ngữ翻译:为语义优化(理解):SigLIP 嵌入将"猫"图像归归归"猫"的代号附近,但不允许好的重建──

Show-o và Transfusion trả tiền cho điều này với một thuế chất lượng rõ ràng trên một hướng. Janus-Pro hỏi: tại sao cần một tokeniser khi các nhiệm vụ có nhu cầu khác nhau?

> Show-o 和 Transfusion vì thế đã trả thuế chất lượng có thể thấy được. Janus-Pro hỏi: Khi nhiệm vụ có nhu cầu khác nhau, tại sao bạn cần một phân từ?

## Khái niệm cốt lõi

> **【中文解读】**Janus-Pro(DeepSeek) sử dụng giải的视觉编码器: một để hiểu nhiệm vụ(CLIP 编码器), một để tạo nhiệm vụ(VQ 编码器)。 hai bộ编码器 chia sẻ cùng một xương sống LLM, mỗi tập trung vào tối ưu hóa các biểu tượng hình ảnh khác nhau。

> **【拓展：解耦编码器的动机】**Để hiểu nhiệm vụ cần các đặc điểm ngữ nghĩa cao cấp, để tạo nhiệm vụ cần các đặc điểm chi tiết cơ bản. Một bộ lập trình đơn khó làm tốt cả hai.


### Mã hóa hình ảnh tách rời

Kiến trúc của Janus-Pro tách hai bộ mã hóa:

> Thiết kế của Janus-Pro sẽ được chia thành hai bộ lập trình:

- Hiểu đường. Hình ảnh đầu vào → SigLIP-SO400m → 2 lớp MLP → cơ thể biến thể.
  中文翻译:理解路径──输入图像 → SigLIP-SO400m → 2 tầng MLP → Transformer 主体──
- Hướng dẫn tạo. Hình nhập (nếu điều kiện trên hình ảnh hiện có) → VQ tokenizer → ID token → thân biến.
  中文翻译:生成路径──输入图像(如果以现有图像为条件)→ VQ 分词器 → token ID → Transformer 主体──
- Tạo sản xuất. Các mã thông báo hình ảnh được dự đoán bởi bộ biến đổi → VQ decoder → pixel.
  中文翻译:输出生成──Transformer 预测的图像代号 → VQ 解码器 → 像素──

Cơ thể biến đổi được chia sẻ. Mọi thứ phía trước và phía dưới của cơ thể là đặc biệt cho nhiệm vụ.

> Transformer 主体是共享的. Tất cả nội dung trên 主体 là nhiệm vụ cụ thể.

Các đầu vào được giải thích bằng định dạng prompt: a `<understand>`Đánh dấu các tuyến đường qua SigLIP; `<generate>`hoặc đường dẫn là ngầm từ nhiệm vụ.

> 输入通过提示格式消歧:`<understand>`标签路由到 SigLIP;`<generate>`路由到VQ──或路由从任务隐式确定──

### Tại sao điều này hiệu quả

Hiểu mất nhận được các tính năng SigLIP, mà CLIP-style pretraining đã điều chỉnh cho sự tương đồng ngữ nghĩa.

> Sự hiểu biết của các mô hình đã được cải thiện hơn bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra bởi các mô hình được tạo ra cho các mô hình được tạo ra bởi các mô hình được tạo ra cho các mô hình được được tạo ra.

Thiệt sản xuất nhận được token VQ, mà một token đã điều chỉnh để tái tạo. Chất lượng hình ảnh cải thiện hơn Show-o vì mã VQ kết hợp trở lại với pixel sạch sẽ.

> 生成损失获得VQ token,分词器已为重建调优了这些代币──图像质量超过Show-o,因为VQ码能干净地组合回像素──

Cơ thể biến đổi chia sẻ nhìn thấy hai phân phối đầu vào (SigLIP và VQ) và học cách làm việc với cả hai.

> 共享的变压器 主体看两种输入分布(SigLIP 和 VQ),学会与两者一起工作──声称:足够的数据 +足够的参数,主体能吸收切换──

### Tăng quy mô dữ liệu  Janus vs Janus-Pro

Janus (tôi ban đầu, arXiv 2410.13848) đã giới thiệu việc tách đôi nhưng ở quy mô nhỏ (1.3B param, dữ liệu hạn chế).

> Janus(原始版,arXiv 2410.13848) giới thiệu hiểu nhưng quy mô nhỏ hơn(13 亿参数,有限数据) ・Janus-Pro(arXiv 2501.17811) đã mở rộng:

- 7B Params (vs 1.3B).
  Trung文翻译:70亿参数(对比13亿)
- 90M cặp hình ảnh-môn văn bản cho giai đoạn 1 (sự sắp xếp) lên từ 72M.
  Trung ngữ翻译:9000.000.000图文对用于第一阶段 (→ ), từ 7200.000升.
- 72M cho giai đoạn 2 (tối hợp) lên từ 26M.
  Trung ngữ翻译:7200.000.000 được sử dụng trong giai đoạn thứ hai (统一), từ 260000.000升.
- Thêm 200k mẫu hướng dẫn hình ảnh-gen cho giai đoạn 3.
  Trung văn翻译: cho giai đoạn thứ ba tăng thêm 200.000 hình ảnh tạo chỉ thị mẫu.

Kết quả: Janus-Pro-7B phù hợp với LLaVA trên MMMU (60.3 vs ~58) và đánh bại DALL-E 3 trên GenEval (0.80 vs 0.67).

> Kết quả:Janus-Pro-7B ở MMMU trên匹配 LLaVA(60.3 vs ~58), ở GenEval 上 đánh bại DALL-E 3(0.80 vs 0.67);; Một mô hình mở, ở cả hai đầu của hệ thống谱系 đều có sức cạnh tranh;;

### JanusFlow  biến thể dòng chảy được chỉnh sửa

JanusFlow (arXiv 2411.07975) thay đổi con đường tạo VQ cho con đường tạo dòng chảy chỉnh sửa ( liên tục).

> JanusFlow(arXiv 2411.07975) sẽ thay thế VQ 生成路径 thành整流生成路径(连续) ――分离成 SigLIP 用于理解+整流用于生成──质量上限进一步提升──架构仍然是解编码器-共享主体──

### Công việc của cơ thể chung

Cơ thể biến đổi xử lý một chuỗi thống nhất nhưng với hai phân phối đầu vào.

> Transformer chủ thể xử lý đơn vị nhưng có hai loại phân phối nhập.

- Để hiểu: tiêu thụ các tính năng SigLIP + mã thông báo văn bản → phát ra văn bản tự động.
  Trung văn翻译:理解:消费 SigLIP 特征 + 文本代币 → 自回归输出文本。
- Để tạo: tiêu thụ mã thông báo văn bản + (tài báo VQ hình ảnh tùy chọn) → phát ra mã thông báo VQ hình ảnh theo cách tự động.
  中文翻译:生成:消费文本代币 +(可选图像 VQ代币)→ 自归输出图像 VQ代币──

Cơ thể không có trọng lượng cụ thể cho mỗi khối. Đó là biến đổi kiểu văn bản mà bạn mong đợi sẽ tìm thấy bên trong Qwen hoặc Llama, cộng với hai bộ chuyển đổi đầu vào.

> 主体没有模态特定权重──它就是你在Qwen或Llama中期望找到的文本风格变压器,加上两个输入适配器──

Điều thú vị là điều này có nghĩa là cơ thể của Janus-Pro có thể được khởi tạo từ một LLM được đào tạo trước. Janus-Pro thực sự khởi tạo từ DeepSeek-MoE-7B. Sự lựa chọn đó quan trọng: LLM đóng góp vào khả năng suy luận mà các mô hình thống nhất tinh khiết từ đầu vật lộn để đạt được.

> Điều thú vị là, điều này có nghĩa là Janus-Pro  chủ thể có thể bắt đầu từ quá trình đào tạo LLM.

### So với InternVL-U

InternVL-U (Dạy 12.10) là sự theo dõi năm 2026.

> InternVL-U (第 12.10 课) là kế tiếp của năm 2026.

- Tiến hành trước khi tập luyện đa phương thức (InternVL3 spine).
  Trung文翻译:原生多模态预训练(InternVL3 主干)
- Đường dẫn mã hóa không kết nối (SigLIP vào, VQ + phân tán đầu ra).
  Trung文翻译:解编码器路由(SigLIP 输入,VQ + 扩散头输出) 』
- Sự hiểu biết thống nhất + thế hệ + chỉnh sửa.
  Trung văn翻译:统一理解 + 生成 + 编辑。

InternVL-U kết hợp lựa chọn kiến trúc của Janus-Pro vào một khung lớn hơn. Ý tưởng mã hóa tách rời hiện nay là mặc định cho các mô hình thống nhất ở quy mô.

> InternVL-U sẽ đưa các cấu trúc của Janus-Pro vào một khuôn khổ lớn hơn.

### Các giới hạn

Các bộ mã hóa không kết nối thêm sự phức tạp kiến trúc. Hai tokeniser để đào tạo, hai đường lối đầu vào để duy trì, hai bộ chế độ thất bại. Đối với các sản phẩm không cần sản xuất, Janus-Pro được kỹ thuật quá cao.

> 解编码器 tăng cường phức tạp cấu trúc. 两个分词器要训练,两个输入路要维护,两个组失败模式.

Đối với các sản phẩm không cần hiểu biết, Janus- Pro quá đủ điều kiện  chọn mô hình Stable Diffusion 3 / Flux.

> Đối với các sản phẩm không cần hiểu,Janus-Pro 大材小用选择 ổn định phân bố 3 / dòng chảy 模型。

Đối với các sản phẩm cần cả hai, Janus-Pro hiện là kiến trúc mở tham chiếu.

> Đối với cả hai sản phẩm cần thiết, Janus-Pro hiện là một cấu trúc mở tham khảo.


> **【拓展：Janus-Pro 在基准上的表现】**Janus-Pro trong nhiều mô hình hiểu biết cơ sở trên hơn 3%, trong hình ảnh tạo cơ sở trên hơn khoảng 10-15%. Nghiên cứu của DeepSeek cho thấy giải thích rằng bộ lập trình là đồng thời làm tốt hơn và tạo tốt nhất giải pháp.


## Hãy dùng nó để thực hành
```figure
l5-janus-decouple
```

## Sử dụng nó

`code/main.py`mô phỏng định tuyến Janus-Pro:

> `code/main.py`模拟 Janus-Pro 路由:

- Hai bộ mã hóa giả: giống như SigLIP (tạo ra các vector ngữ nghĩa 256 chiều) và giống như VQ (tạo ra mã số nguyên).
  Trung文翻译:两个模拟编码器:类 SigLIP(产生 256 维语义向量) 和类 VQ(产生整数码) ⋅
- Một router prompt chọn bộ mã hóa dựa trên thẻ nhiệm vụ.
  Trung ngữ翻译:基于任务标签选择编码器的提示路由器──
- Một cơ thể chia sẻ (stand-in) xử lý chuỗi token bất kể bộ mã hóa nào tạo ra chúng.
  Trung文翻译:共享主体(替代), xử lý các mã hiệu 序列, bất kể từ máy编码 nào.
- Một chuyển đổi từ giai đoạn 1 (sẵn sàng) sang giai đoạn 3 (từ hướng dẫn) lịch trình mẫu cân nặng.
  Trung ngữ翻译: từ giai đoạn đầu tiên (对齐) đến giai đoạn thứ ba (指令微调) của加权采样调度切换――

Bác các đường dẫn được định tuyến cho 3 ví dụ: hình ảnh QA, T2I, chỉnh sửa hình ảnh.

> 印 3 个示例的路由路径: hình ảnh问答、T2I、图像编辑──

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-decoupled-encoder-picker.md`. Với một sản phẩm muốn tạo ra một thế hệ thống nhất + hiểu biết về chất lượng hàng rào, nó chọn Janus-Pro, JanusFlow hoặc InternVL-U với một khuyến nghị quy mô dữ liệu cụ thể.

> 本课产 出 `outputs/skill-decoupled-encoder-picker.md`❖ Đưa ra nhu cầu trước tiên về chất lượng trong suốt đời của sản phẩm, nó được lựa chọn giữa Janus-Pro、JanusFlow hoặc InternVL-U, cùng với các đề xuất quy mô dữ liệu cụ thể.

## Tập luyện bài tập

1. Janus-Pro-7B vượt qua DALL-E 3 trên GenEval. Giải thích tại sao mô hình mở 7B có thể phù hợp với mô hình độc quyền hàng rào về thế hệ nhưng không phải về sự hiểu biết.
   Trung ngữ翻译:Janus-Pro-7B 在 GenEval 上击败 DALL-E 3──解释为什么 7B 开放模型能在生成上匹敌前沿专业模型,但在理解上不能──

2. Thực hiện chức năng router: cho văn bản prompt, phân loại như `understand`hoặc `generate`Làm sao để xử lý những lời nhắc nhở không rõ ràng như "để mô tả và sau đó vẽ"?
   Trung văn翻译:实现路由函数:给定提示文本,分类为 `understand`Hoặc`generate` Làm thế nào để xử lý mô tả và vẽ ra?

3. JanusFlow thay thế con đường VQ bằng dòng chảy được chỉnh sửa.
   Trung ngữ翻译:JanusFlow dùng toàn流 thay thế VQ 路径──Tranformateur 主体现在输出什么?损失有什么变化?

4. đề xuất một nhiệm vụ thứ tư mà kiến trúc Janus-Pro có thể xử lý với một bộ mã hóa tách rời hơn. ví dụ: phân đoạn hình ảnh (tương tự DINO), độ sâu (tương tự MiDaS).
   Trung文翻译: đề xuất Janus-Pro 架构通过增加一个解编码器可以处理的第四种任务──如:图像分割(DINO 风格)、深度(MiDaS 风格)。

5. Đọc phần 4.2 của Janus-Pro về quy mô dữ liệu.
   Trung ngữ翻译:阅读 Janus-Pro 第 4.2 节关于数据扩展――哪个数据阶段对T2I质量提升贡献最大?

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Decoupled encoding | "Two visual encoders" | Separate tokenizer or encoder per direction: semantic for understanding, reconstruction for generation | 每个方向使用独立的分词器或编码器：理解用语义，生成用重建 |
| Shared body | "One transformer" | Single transformer processes either encoder's output; no modality-specific weights | 单一 Transformer 处理任一编码器的输出；无模态特定权重 |
| SigLIP for understanding | "Semantic features" | CLIP-family vision tower providing rich conceptual features but poor reconstruction | CLIP 家族视觉塔，提供丰富的概念特征但重建能力差 |
| VQ for generation | "Reconstruction codes" | Vector-quantized tokens that decode cleanly back to pixels | 可干净解码回像素的向量量化 token |
| JanusFlow | "Rectified-flow variant" | Janus-Pro with a continuous flow-matching generation head instead of VQ | 使用连续流匹配生成头替代 VQ 的 Janus-Pro |
| Routing tag | "Task tag" | Prompt marker (`<understand>` / `<generate>`) that picks the input encoder | 选择输入编码器的提示标记 |

## Xem thêm 延伸阅读

- [Wu et al. — Janus (arXiv:2410.13848)](https://arxiv.org/abs/2410.13848)
  Trung ngữ翻译:Janus 论文。
- [Chen et al. — Janus-Pro (arXiv:2501.17811)](https://arxiv.org/abs/2501.17811)
  Trung văn翻译:Janus-Pro 论文。
- [Ma et al. — JanusFlow (arXiv:2411.07975)](https://arxiv.org/abs/2411.07975)
  Trung文翻译:JanusFlow 论文。
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877)
  Trung văn翻译:InternVL-U 论文。
- [Dong et al. — DreamLLM (arXiv:2309.11499)](https://arxiv.org/abs/2309.11499)
  Trung文翻译:DreamLLM 论文。
