# Vision Transformers và Patch-Token Primitive

> Trước khi có bất cứ thứ gì đa phương thức, một hình ảnh phải trở thành một chuỗi các token mà một biến thể có thể ăn. Bài báo ViT 2020 trả lời câu hỏi này bằng các bản vá 16x16 pixel, một dự đoán tuyến tính và một vị trí nhúng. Năm năm sau, mỗi mô hình biên giới 2026 (Claude Opus 4.7 ở 2576px bản địa, Gemini 3.1 Pro, Qwen3.5-Omni) vẫn bắt đầu theo cách này  mã hóa thay đổi từ ViT sang DINOv2 sang SigLIP 2, mã đăng ký đã được thêm vào, kế hoạch vị trí trở thành 2D-RoPE, nhưng nguyên thủy vẫn giữ. Bài học này đọc đường ống mã patch từ đầu đến cuối và xây dựng nó trong stdlib Python để phần còn lại của giai đoạn 12 có một mô hình tinh thần cụ thể cho "tô hiệu thị giác".

> **【中文解读】**Trước khi bước vào nhiều mô hình, hình ảnh phải trở thành một chuỗi mã hóa được xử lý bởi Transformer. ViT sử dụng 16x16 hình ảnh khối + tuyến tính chiếu + mã vị trí đã thực hiện chuyển đổi này, cho đến nay vẫn là nền tảng của tất cả các mô hình phía trước.

> **【拓展：ViT Patch→多模态基础】**Patch-Token là nền tảng của tất cả các mô hình ngôn ngữ video, dù là CLIP của video biên tập viên, LLaVA của hình ảnh nhập hoặc mô hình hiểu văn bản, tất cả đều bắt đầu từ Patch.

>  **【前置】**Học本节前请先掌握:(1) Bước 7·01-05(Transformer 基础) 理解自我注意、Position Embedding;(2) Bước 4·03(CNNs) 理解卷积特征提取,对比 ViT 补丁方法;(3) Bước 10·01(Tokenizers) 理解文本代币,本节是其视觉对应;(4) numpy 矩阵运算──本节是Bước 12 全部 25 节的基础,跳过会看不懂后续──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, patch tokenizer + geometry calculator) | **语言:** Python（标准库，patch tokenizer + 几何计算器）
**Prerequisites:** Phase 7 (Transformers), Phase 4 (Computer Vision) | **前置知识:** Phase 7（Transformer），Phase 4（计算机视觉）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Mục tiêu học tập

- Chuyển đổi một hình ảnh HxWx3 thành một chuỗi các mã hóa vá với mã hóa vị trí chính xác.
  Trung文翻译:将 HxWx3 图像转换为带有正确位置编码的补丁代码 序列──
- Lượng bộ vi số, số parameter và FLOP cho ViT của một số liệu (kích thước bản vá, độ phân giải, mờ ẩn, độ sâu).
  Trung文翻译:计算给定 ((patch 大小、分辨率、隐藏维度、深度) của ViT của chuỗi dài, số lượng và FLOPs。
- Hãy nêu tên ba nâng cấp đã đưa ViT từ nghiên cứu năm 2020 đến sản xuất năm 2026: tự giám sát trước khi đào tạo (DINO / MAE), mã đăng ký và đóng gói độ phân giải bản địa.
  Trung ngữ翻译:列举将 ViT Từ năm 2020 nghiên cứu推向 2026 năm sản xuất môi trường:自监督预训练(DINO / MAE) 、đăng ký token 和原生分辨率打包──
- Chọn giữa CLS pooling, trung bình pooling, và đăng ký token cho một nhiệm vụ dòng chảy.
  Trung文翻译:为下游任务选择 CLS 池化、平均值池化或注册代币──

## Vấn đề  vấn đề giới thiệu

Các bộ biến chuyển hoạt động trên chuỗi các vector. Văn bản đã là một chuỗi (byte hoặc token). Một hình ảnh là một lưới 2D của các pixel với ba kênh màu  không phải một chuỗi. Nếu bạn phẳng mỗi pixel, một hình ảnh RGB 224x224 trở thành 150,528 token, và sự chú ý tự tại chiều dài đó là không khởi động (quadrat trong chiều dài chuỗi).

> Transformer 操作 là chuỗi khối lượng. Văn bản tự nó là chuỗi. Nhưng hình ảnh là hình ảnh có ba màu trong đường dẫn hình ảnh 2D. Nếu bạn biểu thị bình thường cho mỗi hình ảnh, một hình ảnh RGB 224x224 sẽ trở thành 150.528 hình ảnh, trong khi việc tập trung vào chiều dài này là không thể thực hiện được.

Các cách tiếp cận trước năm 2020 đã kéo một bộ trích dẫn tính năng CNN lên mặt trước: ResNet tạo ra một bản đồ tính năng 7x7 của các vector 2048 chiều, cung cấp 49 token đó cho một biến thể. Điều này hoạt động nhưng thừa hưởng sự thiên vị của CNN (tương đương dịch, các trường thụ thể địa phương) và mất sự thèm ăn của biến thể đối với quy mô.

> Phương pháp trước năm 2020 là trước cuối tiếp theo một bộ thu đặc điểm CNN: ResNet tạo ra 7x7 của 2048 维向量特征图, sẽ đưa 49 token này cho Transformer.

Dosovitskiy et al. (2020) đặt ra câu hỏi thẳng thắn: nếu chúng ta bỏ qua CNN thì sao? Chia hình ảnh thành các bản vá kích thước cố định (chẳng hạn 16x16 pixel), chiếu theo đường thẳng mỗi bản vá vào một vector, thêm một bản nhúng vị trí, và đưa chuỗi vào một bộ biến thể vanilla. Vào thời điểm đó đây là một sự dị giáo mà không có sự xoay quanh. Với đủ dữ liệu (JFT-300M, sau đó là LAION) nó đánh bại ResNet trên ImageNet và tiếp tục cải thiện.

> Dosovitskiy 等人(2020) đưa ra một câu hỏi trực tiếp: nếu chúng ta nhảy qua CNN này? hình ảnh sẽ được chia thành một bản vá lớn cố định (ví dụ như 16x16 hình ảnh), chiếu trực tuyến mỗi bản vá cho một khối lượng, cộng thêm mã vị trí, sau đó sẽ chuyển chuỗi sang Standard Transformer.

Đến năm 2026, ViT nguyên thủy là nền tảng không thể nghi ngờ. Tháp tầm nhìn của mỗi VLM có trọng lượng mở là một số hậu duệ (DINOv2, SigLIP 2, CLIP, EVA, InternViT).

> Đến năm 2026, ViT nguyên ngữ đã trở thành nền tảng không thể tranh cãi. Mỗi tòa nhà quan sát của VLM được mở trọng lượng là những thế hệ sau của nó. Vấn đề không còn là "không nên sử dụng váy?" mà là "vỗ váy nào?

## Khái niệm cốt lõi

> **【中文解读】**Vision Transformer (ViT) sẽ chia hình ảnh thành một bản vá cố định lớn như 16x16 像素), mỗi bản vá 展平后通过线性投影变成一个代币, sau đó giống như Transformer trong NLP.

> **【拓展：ViT 的影响】**Dosovitskiy  et al. 2020 đề xuất ViT chứng minh Transformer trên phân loại hình ảnh có thể vượt qua CNN。ViT-L/14 trên ImageNet đạt 88.5% top-1  độ chính xác率。ViT là nền tảng của các mô hình lập trình hình ảnh CLIP、GPT-4V、Gemini 等多模态模型──Swin Transformer 通过层级化窗口关注解决ViT đối với các hình ảnh độ phân giải cao ⋅


> **【拓展：ViT 对 CNN 的优势】**ViT's toàn cảnh tự tập trung vào lượng dữ liệu đủ lớn khi (như JFT-300M hoặc LAION-5B) đáng kể tốt hơn CNN's cảm nhận địa phương.


### Các bản vá như các token

Nhờ hình ảnh `x`hình dạng`(H, W, 3)`và một kích thước đệm `P`, bạn khắc hình ảnh thành một lưới của `(H/P) x (W/P)`Các đệm không chồng chéo.`P x P x 3`Cube của các pixel. phẳng mỗi cube để một `3 P^2`Vector. Sử dụng một dự án tuyến tính chia sẻ `W_E`hình dạng`(3 P^2, D)`để lập bản đồ mỗi đệm vào chiều kích ẩn của mô hình `D`- Tôi không biết.

> 给定形状为`(H, W, 3)`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `x`和 patch  lớn`P`, sẽ cắt hình ảnh cho `(H/P) x (W/P)`个不重叠的补丁 网格── mỗi补丁 là một `P x P x 3`                                                                                                                                                                                                                                                              `3 P^2`维向量──应用形为 `(3 P^2, D)`                                                                                                                                                                                                                                                              `W_E`, sẽ mỗi đệm được chiếu vào kích thước ẩn của mô hình`D`

Đối với cấu hình ViT-B/16:
- Nghị quyết 224, kích thước vá 16 → lưới 14x14 → 196 mã vá.
  中文翻译:分辨率 224, patch 大小 16 → 网格 14x14 → 196 个 patch token。
- Mỗi đệm là `16 x 16 x 3 = 768`giá trị pixel, dự đoán là `D = 768`- Tôi không biết.
  中文翻译: mỗi bản vá 包含 `16 x 16 x 3 = 768`个像素值,投影到 `D = 768`
- Thêm một cái học được `[CLS]`token → chuỗi dài 197.
  Trung ngữ翻译:添加一个可学习的 `[CLS]`token → 序列长度 197。

Dự án váy là toán học giống hệt với một convolution 2D với kích thước hạt nhân `P`, bước đi`P`, và`D`Đó là cách mà mã sản xuất thực sự thực hiện nó `nn.Conv2d(3, D, kernel_size=P, stride=P)`. Phong khung "động chiếu tuyến tính" là khái niệm; Phong khung hạt nhân là hiệu quả.

> Patch  chiếu trên toán học bằng với hạt nhân`P`、步长为 `P`、 xuất khẩu đường dẫn cho `D` 卷积──                                                                                                                                                                                                                                                            `nn.Conv2d(3, D, kernel_size=P, stride=P)`"Lịch chiếu tuyến tính" là khái niệm; thực hiện khối lượng hạt nhân là hiệu quả cao

### Các tích hợp vị trí

Các bản vá không có thứ tự bản chất  người biến hình nhìn thấy chúng như một túi. ViT đầu tiên đã thêm một việc nhúng vị trí 1D có thể học được (một vector 768 chiều mỗi vị trí, 197 trong số đó).

> Patch không có thứ tự cố địnhTransformer sẽ xem chúng như một tập hợp không thứ tự.

Các xương sống thị giác hiện đại sử dụng 2D-RoPE (M-RoPE của Qwen2-VL, mặc định của SigLIP 2) hoặc các vị trí 2D được phân tích theo yếu tố. 2D-RoPE xoay các truy vấn và các vector khóa dựa trên chỉ số của vá (câu, cột), vì vậy mô hình này suy luận vị trí 2D tương đối từ góc quay. Không có bảng vị trí. mô hình xử lý kích thước lưới tùy ý khi suy luận.

> 现代视觉主干网络使用 2D-RoPE(Qwen2-VL của M-RoPE、SigLIP 2默认方案) 或分解式 2D 位置编码──2D-RoPE 根据补丁的(行、列)索引旋转查询 和键向量,因此模型从旋转角度推断对2D 位置──无需位置表──模型在推理时可以处理任意网格大小──

### Các token CLS, đầu ra tổng hợp và mã đăng ký

Định nghĩa hình ảnh là gì? Ba lựa chọn tồn tại cùng nhau:

> 什么是图像级表示? 三种选择并存:

1. `[CLS]`token. Prependable vector để các chuỗi vá. Sau tất cả các khối biến thể, trạng thái ẩn của token CLS là đại diện hình ảnh. thừa kế từ BERT. được sử dụng bởi ViT gốc, CLIP.
   Trung ngữ翻译:`[CLS]`token──在补丁序列前拼接一个可学习向量──所有 Transformer 块之后, trạng thái ẩn của token CLS là biểu tượng──继承自BERT──原始 ViT 和 CLIP 使用──
2. - Phòng trung bình, trung bình các thông báo của các mã hóa được sử dụng bởi SigLIP, DINOv2, hầu hết các VLM hiện đại.
   Trung文翻译:均值池化──对所有补丁代币的输出隐藏状态取平均──SigLIP、DINOv2 和大多数现代VLM使用──
3. Các mã đăng ký được đào tạo mà không có mã thông báo rửa mặt rõ ràng (2023) quan sát thấy rằng các mã thông báo được đào tạo mà không có mã thông báo rửa mặt rõ ràng phát triển các bản vá "đồ tạo" có chuẩn cao bắt cóc sự chú ý bản thân.
   Trung ngữ翻译:Register token──Darcet 等人(2023) quan sát thấy, không có biểu tượng汇聚 token của ViT 会产生高范数"伪影"patch,劫持自注意力──添加 4-16 个可学习的注册代币可以吸收这种负载,提高密集预测质量──分割、深度──DINOv2 和 SigLIP 2 都带有注册──

Sự lựa chọn quan trọng đối với các nhiệm vụ dòng chảy xuống. CLS là tốt cho việc phân loại. Đối với VLMs cung cấp các mã hóa vá vào LLM, bạn bỏ qua việc hợp nhất hoàn toàn  mỗi mã vá trở thành mã hóa nhập vào LLM. Các sổ đăng ký bị loại bỏ trước khi giao (bạn đang đặt hàng, không phải là nội dung).

> 选择对下游任务很重要──CLS 适合分类──对于将补丁代币进入LLM的VLM,完全跳过池化每个补丁都成为LLM的输入代币──Register 在交接前被丢弃(它们是脚手架,不是内容)──

### Đào tạo trước: giám sát, tương phản, che giấu, tự chưng cất

ViT 2020 đã được đào tạo trước với phân loại giám sát trên JFT-300M.

> ViT trong năm 2020 trong JFT-300M 上用监督分类进行预训――很快被以下方法取代:

- CLIP (2021): hình ảnh-môn ngữ tương phản trên 400M cặp. Bài học 12.02.
  Trung văn翻译:CLIP(2021): 4 tỷ đối với hình ảnh- văn bản đối với học.
- MAE (2021, He et al.): che 75% các bản vá, tái tạo pixel.
  Trung ngữ翻译:MAE(2021,He 等人): 遮蔽 75% của váy,重建像素──自监督,适用于纯图像──
- DINO (2021) / DINOv2 (2023): tự chưng cất với học sinh-người dạy, không có nhãn, không có phụ đề. 2023 DINOv2 ViT-g/14 là xương sống tinh khiết trực quan mạnh nhất và là mặc định cho trường hợp sử dụng "lợi đặc điểm dày đặc".
  Trung ngữ翻译:DINO(2021)/ DINOv2(2023):师生自蒸,无需标签、无需描述──2023 năm của DINOv2 ViT-g/14 là mạnh nhất trong mạng lưới chủ nhân trực quan, cũng là "密集特征" của các ví dụ 默认选择──
- SigLIP / SigLIP 2 (2023, 2025): CLIP với mất tích sigmoid và NaFlex cho tỷ lệ hình ảnh bản địa. Tháp tầm nhìn thống trị trong 2026 mở VLM (Qwen, Idefics2, LLaVA-OneVision).
  Trung文翻译:SigLIP / SigLIP 2(2023,2025): sử dụng sigmoid 损失和 NaFlex 原生宽高比的 CLIP──2026 年开放 VLM(Qwen、Idefics2、LLaVA-OneVision) 主导视觉塔──

Sự lựa chọn của bạn về việc đào tạo trước quyết định xương sống là tốt cho: CLIP/SigLIP cho sự phù hợp ngữ nghĩa với văn bản, DINOv2 cho các tính năng trực quan dày đặc, MAE như một điểm khởi đầu cho chỉnh sửa tinh tế dòng chảy.

> 预训练方式决定主干网络擅长什么: CLIP/SigLIP được sử dụng để phù hợp với ngữ nghĩa của văn bản, DINOv2 được sử dụng cho đặc điểm hình ảnh mật, MAE 作为下游微调的起点──

### Luật quy mô

ViT quy mô (Zhai et al. 2022) đã xác định rằng chất lượng của ViT tuân thủ các luật có thể dự đoán được về kích thước mô hình, kích thước dữ liệu và tính toán.

> ViT 缩放定律 ((Zhai 等人,2022) đã xác định chất lượng của ViT theo quy tắc có thể dự đoán về mô hình lớn, dữ liệu lớn và số lượng tính toán:.

- Mô hình lớn hơn + dữ liệu nhiều hơn → chất lượng tốt hơn.
  Trung文翻译:更大的模型 + 更多数据 → 更好的质量──
- Kích thước các bản vá là một đòn bẩy về độ dài chuỗi so với độ trung thực. Patch 14 (đặc trưng cho DINOv2/SigLIP SO400m) cung cấp nhiều token mỗi hình ảnh so với patch 16; tốt hơn cho OCR và các nhiệm vụ dày đặc, tệ hơn cho tốc độ.
  Patch 大小是序列长度与保真度之间的杆──Patch 14 ((DINOv2/SigLIP SO400m 的典型配置) hơn patch 16 mỗi张图像产生更多代币;更适合 OCR 和密集任务,但速度更慢──
- Khả năng giải quyết là một đòn bẩy lớn khác. Đi từ 224 đến 384 đến 512 hầu như luôn luôn giúp, với chi phí vuông trong FLOP.
  Trung ngữ: phân giải là một yếu tố quan trọng khác. Từ 224 tăng lên 384 và 512 gần như luôn có ích, nhưng FLOP đã tăng trưởng lần thứ hai.

ViT-g/14 (1B params, patch 14, độ phân giải 224 → 256 token) và SigLIP SO400m/14 (400M params, patch 14) là hai mã hóa ngựa làm việc cho 2026 VLM mở.

> ViT-g/14(10 tỷ参数, patch 14,分辨率 224 → 256 个代币) và SigLIP SO400m/14(4 tỷ参数, patch 14) là hai máy lập trình chính của VLM được mở vào năm 2026:

### Số parameter cho một ViT

Việc tính toán đầy đủ là trong `code/main.py`Đối với ViT-B/16 ở 224:

> 完整计算见 `code/main.py`Đối với ViT-B/16 ở độ phân giải 224:

```
patch_embed = 3 * 16 * 16 * 768 + 768  =  591k
cls + pos    = 768 + 197 * 768          =  152k
block        = 4 * 768^2 (QKVO) + 2 * 4 * 768^2 (MLP) + 2 * 2*768 (LN)
             = 12 * 768^2 + 3k          =  7.1M
12 blocks    = 85M
final LN    = 1.5k
total       ≈ 86M
```

Đặt bóng vào mỗi VT trước khi bạn tải vào điểm kiểm soát.

> Trước khi tải kiểm tra điểm, sử dụng phương pháp này để ước tính từng ViT.

### 2026 cấu hình sản xuất

Các mã hóa VLM mở nhất tàu với năm 2026 là SigLIP 2 SO400m/14 với độ phân giải bản địa (NaFlex).

> 2026 Phần lớn các bộ lập trình được trang bị VLM là bản gốc phân giải của SigLIP 2 SO400m/14 của NaFlex.

- Các tham số 400M.
  Trung ngữ翻译:4 亿参数。
- kích thước vá 14, độ phân giải mặc định 384 → 729 mã vá cho mỗi hình ảnh.
  Trung文翻译:Patch 大小 14,默认分辨率 384 → 每张图像 729 个补丁代币──
- Đội trung bình cho các nhiệm vụ cấp hình ảnh; tất cả 729 bản vá chảy vào LLM cho VQA.
  Trung文翻译:图像级任务使用平均值池化; tất cả 729 个补丁 流入 LLM 进行视觉问答。
- 4 thẻ đăng ký, bị loại bỏ trước khi giao LLM.
  Trung ngữ翻译:4 个注册代币,交给 LLM 前丢弃
- 2D-RoPE với quy mô cấp hình ảnh cho tỷ lệ hình ảnh bản địa.
  Trung ngữ翻译:2D-RoPE,带图像级缩缩以支持原生宽高比──

Mỗi quyết định trong bộ sưu tập đó đều có nguồn gốc từ một tờ báo mà bạn có thể đọc.

> Mỗi quyết định trong cấu hình có thể được truy cập vào bài báo bạn có thể đọc.

## Hãy sử dụng nó để thực hiện
```figure
image-patch-tokens
```

## Sử dụng nó

`code/main.py`là một token hóa bản vá và máy tính hình học. Nó lấy (hình H, W, bản vá P, ẩn D, độ sâu L) và báo cáo:

> `code/main.py`là một mã hóa bản vá 和几何计算器──它接收(图像 H, W, bản vá P, 隐藏维度 D, 深度 L)并报告:

- Hình dạng lưới và chiều dài chuỗi sau khi dán.
  Trung文翻译:Patch 切分后的网格形状和序列长度──
- Dòng mã thông báo cho hình ảnh đồ chơi tổng hợp 8x8 pixel (làm bộ qua đường phẳng + dự án).
  Trung文翻译:合成 8x8 像素玩具图像的符号序列(遍历展平 + 投影路径) 』
- Số parameter được chia theo patch embed, position embed, block biến thể và head.
  Trung文翻译:按补丁 嵌入、位置编码、Transformer 块和头分解的参数──
- FLOPs cho mỗi lần đi về phía trước tại độ phân giải mục tiêu.
  Trung ngữ翻译:目标分辨率下 每次前向传播的 FLOPs──
- Một bảng so sánh trên ViT-B/16 @ 224, ViT-L/14 @ 336, DINOv2 ViT-g/14 @ 224, SigLIP SO400m/14 @ 384.
  中文翻译:ViT-B/16 @ 224、ViT-L/14 @ 336、DINOv2 ViT-g/14 @ 224、SigLIP SO400m/14 @ 384 的对比表──

Hãy chạy nó, so sánh số lượng tham số với số lượng được xuất bản, chơi với kích thước và độ phân giải để cảm nhận chi phí số lượng token.

> 运行它.  将参数与发布数据相比. 调整补丁大小和分辨率 để cảm nhận chi phí số lượng token.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-patch-geometry-reader.md`Với cấu hình ViT (kích thước bản vá, độ phân giải, mờ ẩn, độ sâu), nó tạo ra một số lượng token, số parameter và ước tính VRAM với các biện minh. Sử dụng kỹ năng này bất cứ khi nào bạn chọn một xương sống thị giác cho một VLM  nó ngăn chặn "các token nổ và bối cảnh LLM của tôi điền" bất ngờ.

> 本课产 出 `outputs/skill-patch-geometry-reader.md` Đưa định ViT 配置 ((patch 大小、分辨率、隐藏维度、深度), nó tạo ra token số lượng, tham số và ghi nhớ ước tính và dựa trên đó.

## Tập luyện bài tập

1. Xét chiều dài chuỗi mã đệm cho Qwen2.5-VL tại đầu vào 1280x720 gốc với kích thước đệm 14. Làm thế nào so sánh với một đại diện CLS-chỉ?
   Trung文翻译:计算 Qwen2.5VL 在原生 1280x720 输入、patch 大小 14 下的补丁符号序列长度──与仅使用 CLS表示相比如何?

2. Một khung hình 1080p (1920x1080) ở patch 14 tạo ra bao nhiêu token? Với 30 FPS trong một video 5 phút, bao nhiêu token trực quan tổng thể? Chi phí nào tiết kiệm bạn nhiều nhất: tập hợp, lấy mẫu khung hình hoặc hợp nhất token?
   Trung ngữ翻译:一 1080p 图像(1920x1080) Trong bản vá 14 下 tạo ra bao nhiêu token?

3. Thực hiện trung bình tập hợp trên mã thông báo vá trong Python tinh khiết. Kiểm tra rằng trung bình tập hợp trên 196 mã thông báo của một DINOv2 đầu ra phù hợp với mô hình `forward`trả lại khi bạn yêu cầu một tập hợp tích hợp.
   Trung文翻译:用纯Python 实现补丁代币的平均值池化──验证对DINOv2 输出196代币做平均值池化是否与模型`forward`                                                                                                                                                                                                                                                              

4. Đọc Phần 3 của "Các bộ biến đổi tầm nhìn cần đăng ký" (arXiv:2309.16588).
   Trung文翻译:阅读"Vision Transformers Need Registers" (ArXiv:2309.16588) 第 3 节──用两句描述注册 吸收了什么伪影,以及为什么对下游密集预测很重要──

5. Thay đổi `code/main.py`để hỗ trợ patch-n'-pack: được đưa ra một danh sách hình ảnh với độ phân giải khác nhau, tạo ra một chuỗi gói đơn và mặt nạ chú ý khối-chương vị.
   Trung ngữ翻译:修改 `code/main.py`以支持 patch-n'-pack: cho một bộ hình ảnh có độ phân giải khác nhau, tạo ra một chuỗi gói và khối đối với góc                                                                                                                                                                                                                                                

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Patch | "16x16 pixel square" | A fixed-size non-overlapping region of the input image; becomes one token | 固定大小的非重叠图像区域；成为一个 token |
| Patch embedding | "Linear projection" | A shared learned matrix (or Conv2d with stride=P) mapping flattened patch pixels to D-dim vectors | 共享的学习矩阵（或步长为 P 的 Conv2d），将展平的 patch 像素映射为 D 维向量 |
| CLS token | "Class token" | Prepended learnable vector whose final hidden state represents the whole image; optional in 2026 | 前置可学习向量，其最终隐藏状态代表整张图像；2026 年可选 |
| Register token | "Sink token" | Extra learnable tokens that absorb the high-norm attention artifacts ViTs develop during pretraining | 额外可学习 token，吸收 ViT 预训练中产生的高范数注意力伪影 |
| Position embedding | "Positional info" | Per-position vector or rotation making the sequence-order-aware; 2D-RoPE is the modern default | 每个位置的向量或旋转，使序列具有顺序感知；2D-RoPE 是现代默认方案 |
| Grid | "Patch grid" | The (H/P) x (W/P) 2D array of patches for a given resolution and patch size | 给定分辨率和 patch 大小下的 (H/P) x (W/P) 2D patch 数组 |
| NaFlex | "Native flexible resolution" | SigLIP 2 feature: single model serves multiple aspect ratios and resolutions without retraining | SigLIP 2 特性：单一模型服务多种宽高比和分辨率，无需重新训练 |
| Backbone | "Vision tower" | The pretrained image encoder whose patch-token outputs feed the LLM in a VLM | 预训练的图像编码器，其 patch-token 输出喂入 VLM 中的 LLM |
| Pooling | "Image-level summary" | Strategy to turn patch tokens into one vector: CLS, mean, attention pool, or register-based | 将 patch token 转为一个向量的策略：CLS、均值、注意力池化或基于 register |
| Patch 14 vs 16 | "Finer vs coarser grid" | Patch 14 produces more tokens per image, better fidelity for OCR, slower; patch 16 is the classic default | Patch 14 每张图产生更多 token，OCR 保真度更高但更慢；patch 16 是经典默认值 |

## Xem thêm 延伸阅读

- [Dosovitskiy et al. — An Image is Worth 16x16 Words (arXiv:2010.11929)](https://arxiv.org/abs/2010.11929) ViT gốc.
  Trung ngữ翻译:原始 ViT 论文。
- [He et al. — Masked Autoencoders Are Scalable Vision Learners (arXiv:2111.06377)](https://arxiv.org/abs/2111.06377) MAE, tự giám sát trước khi tập luyện.
  Trung ngữ翻译:MAE,自监督预训练──
- [Oquab et al. — DINOv2 (arXiv:2304.07193)](https://arxiv.org/abs/2304.07193) tự chưng cất ở quy mô, không có nhãn.
  Trung文翻译: 大规模自蒸,无需标签──
- [Darcet et al. — Vision Transformers Need Registers (arXiv:2309.16588)](https://arxiv.org/abs/2309.16588) đăng ký token và phân tích đồ tạo vật.
  Trung文翻译:Tài báo đăng ký 和伪影分析。
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) tháp tầm nhìn mặc định năm 2026.
  Trung ngữ翻译:2026 年默认的视觉塔──
- [Zhai et al. — Scaling Vision Transformers (arXiv:2106.04560)](https://arxiv.org/abs/2106.04560) Luật quy mô thực nghiệm.
  Trung文翻译: kinh nghiệm缩放定律.
