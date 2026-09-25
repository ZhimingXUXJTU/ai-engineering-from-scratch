# Tài liệu và biểu đồ Nghĩa Nghĩa  tài liệu và biểu đồ Nghĩa Nghĩa

> Tài liệu không phải là hình ảnh. Một bản PDF, giấy khoa học, hóa đơn hoặc hình thức viết tay có bố cục, bảng, sơ đồ, ghi chú chân, tiêu đề và cấu trúc ngữ nghĩa mà sự hiểu biết hình ảnh đơn giản không thể nắm bắt được. Dòng trước VLM là một đường ống: Tesseract OCR + LayoutLMv3 + Heuristics khai thác bảng. Đợt VLM thay thế nó bằng các mô hình không OCR  Donut (2022), Nougat (2023), DocLLM (2023)  phát ra dấu hiệu cấu trúc trực tiếp. Đến năm 2026, biên giới chỉ là "giới thiệu hình ảnh trang cho Claude Opus 4.7 ở 2576px bản địa", và đầu ra đánh dấu cấu trúc được cung cấp miễn phí. Bài học này đọc được vòng cung ba thời đại của AI tài liệu.

> **【中文解读】**文档不是照片──PDF、论文、发票、手写表单有布局、表格、图表、脚注、标题等语义结构,普通图像理解无法捕捉──文档 AI 经历了三个时代:(1) OCR管道(Tesseract + LayoutLMv3);(2) OCR-free(Donut、Nougat 直接从图像生成结构化输出);(3) VLM 原生(2026年直接将页面图像给Claude Opus 4.7 即可)

> **【拓展：文档理解在金融领域的应用】**金融场景是文档 AI quan trọng nhất trong lĩnh vực ứng dụng:发票解析(自动提取供应商、金额、税率) 、合同审查(条款比对、风险标记) 、财务报表提取(资产负债表、利表的结构化数据抽取) 、KYC 文档处理身份(证券、营业执照的自动识别) ⋅2026 年推方案:纯印发票用 LayoutLMv3 ((成本低),混合文档用手写VLM 原生(PaliGemma 2或Qwen2.5-VL),监管场景用OCR + VLM 交叉验证──

**Type:** Build
**Languages:** Python (stdlib, layout-aware document parser skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 5 (NLP)
**Time:** ~180 minutes

>  **【前置】**Học本节前请先掌握:Phase 12·05(LLaVA) Phase 12·06 ((AnyRes High resolution,对文档至关重要) Phase 5·08 ((LayoutLM 系列文档布局模型) 文档 AI là ứng dụng giá trị cao của VLM, đặc biệt quan trọng,
>  **【类比】**文档理解三时代 = "Hành động của báo cáo kế toán"。OCR 管道 = 人工核对+表格软件(先识别文字再解析布局);OCR-free(Donut) = phần mềm hợp nhất hóa(看图直接生成结构化数据);VLM 原生(Claude) = 全能AI(看图就能理解,回答,推理,无需专门训练)。 Mỗi thế hệ đều để các phương pháp của thế hệ trước hết thời gian, nhưng năm 2026 ba thế hệ của công nghệ vẫn đang sử dụng để chọn các chương trình rẻ nhất theo cảnh tượng ~~
> ️ **【易错点】**简单 OCR 任务用VLM = 杀用牛刀(成本10倍)  Ví dụ: đơn giản văn bản发票用Tesseract + LayoutLMv3 chỉ cần vài分钱, sử dụng GPT-4V 要几毛钱──修复:先评估任务复杂度,简单的OCR管道,复杂的(手写、混合布局、多语言)才上VLM──

## Mục tiêu học tập

- Giải thích ba thời đại của AI tài liệu: đường ống OCR, không OCR, VLM-đồng.
  Trung文翻译:解释文档 AI 的三个时代:OCR管道、无OCR、VLM 原生──
- Mô tả ba dòng đầu vào của LayoutLMv3: văn bản, bố cục (bbox), các bản vá hình ảnh, với sự che giấu thống nhất.
  Trung văn翻译:描述 LayoutLMv3 的三个输入流:文本、布局(bbox)、图像补丁,配合统一掩码──
- So sánh Donut (không OCR, hình ảnh → đánh dấu), Nougat (biên khoa học → LaTeX), DocLLM (sản xuất nhận thức về bố cục), PaliGemma 2 (tự do VLM).
  Trung文翻译:比较 Donut(无 OCR,图像→标记) 、Nougat(科学论文→LaTeX) 、DocLLM(布局感知生成) 、PaliGemma 2(VLM 原生) ⋅
- Chọn mô hình tài liệu cho một nhiệm vụ mới (phần hóa đơn, báo cáo khoa học, biểu mẫu bằng tay, biên bản bằng tiếng Trung).
  Trung văn翻译:为新任务选择文档模型(发票、科学论文、手写表单、中文收据)

## Vấn đề  vấn đề giới thiệu

"Hiểu PDF này" là khó hiểu. Thông tin nằm trong:

> "Giải thích PDF này" dường như đơn giản thực tế khó khăn.

- Nội dung văn bản (90% tín hiệu).
  Trung ngữ翻译:文本内容(90% 的信号) 』
- Layout (chủ đề, ghi chú chân, thanh bên, định dạng hai cột).
  Trung文翻译:布局(标题、脚注、侧边、双格式)
- Bảng (các hàng, cột, các tế bào hợp nhất).
  Trung文翻译:表格(行、列、合并单元格)
- Hình ảnh và sơ đồ.
  Trung ngữ翻译:图表和图示──
- Những ghi chú bằng tay.
  Trung ngữ翻译:手写注释。
- Các font và kiểu chữ (tít hiệu so với thân hình).
  Trung ngữ翻译:字体和排版(标题 vs 正文)。

Một hệ thống quan tâm đến hóa đơn cần biết "Total: $1,245" đến từ bên dưới bên phải, không phải từ một ghi chú chân.

> OCR ban đầu chỉ lấy văn bản, mất phần còn lại của thông tin.

## Khái niệm cốt lõi

> **【中文解读】**文档和图表理解是多模态 AI's quan trọng ứng dụng trường hợp: OCR、表格提取、流程图解读、公式识别等──关键技术:高分辨率输入 (khả năng lưu giữ độ rõ ràng của văn bản) 版面分析 (khả năng phân tích) 版本面分析 (khả năng phân tích) 版本面分析 (khả năng phân tích) 版本结构输出 (khả năng phân tích) 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本 版本

> **【拓展：文档 AI 的工业应用**文档 AI 市场巨大:合同审核、发票处理、学术论文分析等──GPT-4o trên DocVQA đạt 92.8%,InternVL2-26B đạt 92.7%(开源最优)──MarkItDown (Microsoft) sẽ chuyển文档 thành Markdown,ColPali dùng phương pháp nhìn thay thế truyền thống OCR 管线──


> **【拓展：文档理解的技术路线】**文档理解有两条路线:(1) OCR-first(先用 OCR 提取文本,再用 LLM 处理)适合纯文文文文档;(2) Vision-first(直接用 VLM 处理文档图像)适合包含图表、表格的复杂版面──GPT-4o 和 InternVL2 走 Vision-first 路线,在复杂文档理解上表现更好──


### Thời đại 1  Đường ống OCR (trước năm 2021)

Thống cổ điển:

> 经典技术:

1. PDF → hình ảnh trên mỗi trang.
   Trung ngữ翻译:PDF → Mỗi trang图像──
2. Tesseract (hoặc OCR thương mại) trích xuất văn bản với các hộp giới hạn mỗi từ.
   Trung văn翻译:Tesseract (或商业 OCR)提取文本并标注每个词的边界框──
3. Bộ phân tích bố trí xác định các khối (tên, bảng, đoạn).
   Trung ngữ翻译:布局分析器识别块(标题、表格、段落)
4. Các cấu trúc bảng nhận dạng phân tích bảng.
   Trung ngữ翻译:表格结构识别器解析表格──
5. Quy tắc miền + trường trích xuất regex.
   Trung文翻译: 领域规则 + 正则表达式提取字段──

Làm việc cho văn bản in sạch. Phá vỡ chữ viết tay, quét sơn, bảng phức tạp, kịch bản không tiếng Anh. Mỗi chế độ thất bại đòi hỏi một con đường ngoại lệ tùy chỉnh.

> 适用于清洁印刷文本──在手写、倾斜扫描、复杂表格、非英文文字上失败──每种失败模式都需要自定义异常处理──

### TrOCR (2021)

TrOCR (Li et al., arXiv:2109.10282) đã thay thế CNN-CTC cổ điển của Tesseract bằng một bộ mã hóa-chế lập trình được đào tạo trên hình ảnh văn bản tổng hợp + thực.

> TrOCR được sử dụng trong việc đào tạo trên hình ảnh văn bản thực tế + Synthesizer 编码器-解码器 đã thay thế CNN-CTC cổ điển của Tesseract. Trong văn bản viết tay và đa ngôn ngữ vẫn có lợi thế rõ ràng.

### Thời đại 2  Không OCR (2022-2023)

Các mô hình không OCR đầu tiên nói: bỏ qua phát hiện hoàn toàn, bản đồ ảnh ảnh ảnh cho kết quả cấu trúc trực tiếp.

> Đầu tiên không OCR mô hình đề xuất: hoàn toàn nhảy qua kiểm tra, trực tiếp sẽ hình ảnh ảnh được chiếu để cấu trúc xuất.

Donut (Kim et al., arXiv:2111.15664):
- Bộ chuyển đổi mã hóa-đánh mã, mã hóa là Swin-B.
- Output là JSON để hiểu hình thức, đánh dấu cho tổng kết, hoặc bất kỳ sơ đồ cụ thể nào về nhiệm vụ.
- Không OCR, không bố cục, không phát hiện.

> Donut:编码器-解码器 Transformer,编码器为Swin-B──输出是 JSON(表单理解)、标记(摘要) 或任务特定方案──无需 OCR、无需布局、无需检测──

Nougat (Blecher et al., arXiv:2308.13418):
- Được đào tạo đặc biệt về các bài báo khoa học.
- Khả năng phát ra là LaTeX / dấu xuống.
- xử lý các phương trình, bố cục nhiều cột, các số.
- Mô hình mà mọi người gọi.

> Nougat: chuyên trên các bài viết khoa học. │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │

Đây là những chuyên gia, không phải những người nói chung.

> Những cái này là mô hình chuyên gia, không phải là thông minh.

### LayoutLMv3 (2022)

Một bài hát khác. LayoutLMv3 (Huang et al., arXiv:2204.08387) giữ OCR nhưng thêm hiểu biết về bố cục:

> Không giống đường. LayoutLMv3 giữ OCR nhưng thêm trang trí hiểu:

- Ba dòng đầu vào: token văn bản OCR, hộp giới hạn 2D mỗi token, các bản vá hình ảnh.
  中文翻译:三个输入流:OCR 文本代币、每个代币的2D 边界框、图像补丁──
- Mục tiêu đào tạo che giấu trên cả ba phương pháp (môn ngữ che giấu, các bản vá che giấu, bố cục che giấu).
  Trung ngữ翻译:跨三个模态的掩码训练目标(掩码文本、掩码补丁、掩码布局)
- Dòng chảy xuống: phân loại, khai thác đơn vị, bảng QA.
  Trung文翻译:下游任务:分类、实体提取、表格 QA。

LayoutLMv3 là đỉnh cao của sự hiểu biết tài liệu dựa trên OCR. Cung cấp mạnh mẽ trên các biểu mẫu và hóa đơn.

> LayoutLMv3 là đỉnh cao của sự hiểu biết tài liệu dựa trên OCR.

### DocLLM (2023)

DocLLM (Wang et al., arXiv:2401.00908) là người anh em sinh của LayoutLM. Nó tạo ra các câu trả lời dạng tự do tùy thuộc vào các mã thông báo bố trí.

> DocLLM là LayoutLM của tạo式兄弟── dựa trên biểu tượng布局 生成自由形式回答──更适合文档 QA; vẫn phụ thuộc vào OCR 输入──

### Thời đại 3  VLM-native (2024+)

2024 VLM đã trở nên đủ tốt để thay thế đường ống hoàn toàn. Đưa hình ảnh toàn trang ở độ phân giải cao đến VLM, đặt câu hỏi, nhận câu trả lời.

> Năm 2024 VLM  trở nên đủ tốt, có thể thay thế hoàn toàn ống ống.

- LLaVA-NeXT 336-tile AnyRes hoạt động cho các tài liệu nhỏ.
  中文翻译:LLaVA-NeXT 336-tile AnyRes 适用于小文档。
- Qwen2.5VL phân giải động xử lý 2048+ pixel theo bản địa.
  Trung文翻译:Qwen2.5VL 动态分辨率原生处理 2048+ 像素。
- Claude Opus 4.7 hỗ trợ tài liệu 2576px.
  中文翻译:Claude Opus 4.7 支持 2576px 文档。
- PaliGemma 2 (ngày 4 năm 2025) đào tạo đặc biệt cho tài liệu + chữ tay.
  Trung文翻译:PaliGemma 2(2025 年 4 月) Khusus dành cho文档+手写训练。

Khoảng cách giữa ống VLM-native và ống OCR đã nhanh chóng đóng cửa.

> Sự khác biệt giữa VLM nguyên sinh và ống OCR giảm nhanh chóng. Đến năm 2026, VLM nguyên sinh trong các khía cạnh sau đây:

- Văn bản cảnh (được viết tay + in, kịch bản hỗn hợp).
  Trung văn翻译:场景文本(手写+印刷,混合文字) 』
- Các bảng phức tạp với các tế bào hợp nhất.
  Trung ngữ翻译:带合并单元格的复杂表格──
- Các phương trình toán học được nhúng vào văn bản.
  Trung ngữ翻译:嵌入文本的数学公式──
- Các hình ảnh với các chú thích văn bản.
  Trung ngữ翻译:带文本注释的图表──

Các đường ống OCR vẫn thắng:

> Các quy trình OCR vẫn có những thành công sau đây:

- Lượng công việc quét sạch trên quy mô lớn nơi độ trễ mỗi trang quan trọng.
  Trung文翻译: 繁体字:大规模纯扫描工作负载, mỗi trang延迟 rất quan trọng
- Đán chắc của đường ống (sự thất bại quyết định so với ảo giác VLM).
  Trung文翻译:管道可靠性(确定性失败 vs VLM 幻觉)
- Môi trường được điều chỉnh đòi hỏi phải có kết quả OCR kiểm toán được.
  Trung文翻译:需要可审计 OCR 输出监管环境──

### Biên giới Claude 4.7 / GPT-5

Với đầu vào bản địa 2576 pixel, VLM biên giới ghi nhận sự hiểu biết với độ chính xác gần như con người.

> Trong năm 2576 像素原生输入下, tiền tuyến VLM để làm văn bản hiểu tỉ lệ xác thực của con người.

- DocVQA: Claude 4.7 ~ 95.1, PaliGemma 2 ~ 88.4, Nougat ~ 77.3, đường ống LayoutLMv3 ~ 83.
  Trung文翻译:DocVQA:Claude 4.7 约 95.1,PaliGemma 2 约 88.4,Nougat 约 77.3,管道式 LayoutLMv3 约 83。
- ChartQA: Claude 4.7 ~ 92,2, GPT-4V ~ 78.
  Trung文翻译:ChartQA:Claude 4.7 约 92.2,GPT-4V 约 78。
- VisualMRC: Claude 4.7 ~ 94.
  Trung văn翻译:MRC:Claude 4.7 约 94。

Hỗng cách trong mô hình đóng cửa chủ yếu là độ phân giải và quy mô LLM cơ sở.

> Sự khác biệt trong mô hình nguồn đóng chính là trong độ phân giải và quy mô LLM cơ bản.

### Phương trình toán học và đầu ra LaTeX

Các bài báo khoa học cần phải có kết quả LaTeX chính xác cho các phương trình. Nougat được đào tạo về điều này. VLM được đào tạo với mục tiêu LaTeX (Qwen2.5-VL-Math, phái sinh Nougat) tạo ra LaTeX có thể sử dụng.

> Các bài viết khoa học cần phải xác định được LATEX 公式输出──Nougat 在此上训练──使用 LATEX 目标训练的 VLM(Qwen2.5-VL-Math、Nougat 衍生物) để tạo ra LATEX có thể sử dụng──没有明显的 LATEX 训练的 VLM 产生可读但不精确的转录──

Đối với các đường ống giấy khoa học vào năm 2026: chuỗi Nougat trên PDF, sau đó là VLM trên các trang khó khăn.

> 2026 年科学论文管道建议:先用 Nougat 处理 PDF,再用 VLM 处理棘手页面──

### Tác giả

Tuy nhiên, nhiệm vụ phụ khó khăn nhất. Phép in hỗn hợp + chữ viết tay (bảng ghi chú của bác sĩ, biểu mẫu được điền) là nơi các đường ống OCR vẫn đánh bại VLM về chi phí.

> 仍然是最难的子任务──印刷+手写混合(医生笔记、填写的表单) là một hệ thống OCR 管道 trong chi phí vẫn còn thắng VLM 场景──纯手写 VLM đang được cải tiến(Claude 4.7、PaliGemma 2)。

### Công thức 2026

Đối với một dự án AI tài liệu mới:

> Đối với các dự án AI mới:

- Hóa đơn in nguyên chất ở quy mô: LayoutLMv3 + quy tắc, hiệu quả về chi phí.
  Trung文翻译:大规模纯印刷发票:LayoutLMv3 + 规则,成本高效──
- Tài liệu hỗn hợp (khoa học + chữ tay + biểu mẫu): VLM bản địa (PaliGemma 2 hoặc Qwen2.5-VL).
  中文翻译:混合文档(科学+手写+表单):VLM 原生(PaliGemma 2 或 Qwen2.5-VL) 』
- Nóng cho toán học, VLM cho số liệu.
  Trung文翻译:完整 arXiv 处理:Nougat 处理数学,VLM 处理图表。
- Quy định: đường ống OCR + xác thực VLM để kiểm tra chéo.
  Trung文翻译:监管场景:OCR 管道 + VLM 验证器交叉检查。

## Hãy sử dụng nó để thực hiện
```figure
mm-doc-layout
```

## Sử dụng nó

`code/main.py`- Có thể là:

- Một tokeniser thức về bố cục đồ chơi: cho các cặp (text, bbox), tạo ra đầu vào kiểu LayoutLMv3.
  Trung文翻译:玩具布局感知分词器:给定 (text, bbox) 对,生成 LayoutLMv3 风格的输入──
- Một máy phát triển kế hoạch nhiệm vụ kiểu Donut: mẫu JSON cho các biểu mẫu.
  Trung ngữ翻译:Donut 风格的任务方案 生成器:表单的 JSON 模板。
- Một so sánh ngân sách token trên mỗi trang trên OCR-pipeline, Donut, Nougat và VLM-native.
  Trung文翻译:OCR 管道、Donut、Nougat 和 VLM 原生之间每页代币 预算的比较。

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-document-ai-stack-picker.md`. Với một dự án AI tài liệu (khu vực, quy mô, chất lượng, quy định), chọn giữa đường ống OCR, chuyên gia không OCR và VLM-native.

> 本课产 出 `outputs/skill-document-ai-stack-picker.md`                                                                                                                                                                                                                                                              

## Tập luyện bài tập

1. Dự án của bạn là 10 triệu hóa đơn mỗi ngày. Bộ đống nào giảm thiểu chi phí mỗi trang mà không mất độ chính xác? Dự án của bạn xử lý mỗi ngày 1.000.000.000张发票―― loại chương trình nào có thể giảm thiểu chi phí mỗi trang trong trường hợp không mất độ chính xác?

2. Tại sao LayoutLMv3 vượt trội hơn CLIP-VLMs trong hình thức QA nhưng kém trong văn bản cảnh?

3. Nougat tạo ra LaTeX. đề xuất một trường hợp thử nghiệm trong đó VLM-đối đầu ra đánh bại Nougat trên độ trung thành LaTeX, và một trường hợp Nougat thắng. Nougat 生成 LaTeX.

4. Đọc PaliGemma 2 bài báo (Google, 2024). Điều gì là sự bổ sung dữ liệu đào tạo chính để nâng cao độ chính xác tài liệu so với PaliGemma 1?

5. Thiết kế một hệ thống lai hợp an toàn theo quy định: đường ống OCR là chính, VLM là kiểm tra chéo thứ cấp.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| OCR pipeline | "Tesseract-style" OCR 管道 | Stage-wise stack: detect -> OCR -> layout -> rules; deterministic, fragile 分阶段栈：检测→OCR→布局→规则；确定但脆弱 | |
| OCR-free | "Donut-style" 无 OCR | Image-to-output transformer that skips explicit OCR; single model 图像到输出的 Transformer，跳过显式 OCR；单一模型 | |
| Layout-aware | "LayoutLM" 布局感知 | Input includes per-token bbox coordinates; unified masking across modalities 输入包含逐 token 的 bbox 坐标；跨模态统一掩码 | |
| VLM-native | "Frontier VLM" VLM 原生 | Feed page image directly to Claude/GPT/Qwen VLM at high resolution; no pipeline 直接将页面图像输入高分辨率 VLM；无需管道 | |
| DocVQA | "Doc benchmark" 文档 VQA 基准 | Document VQA standard; most-cited score 文档 VQA 标准评测；被引用最多的评分 | |
| Markup output | "LaTeX / MD" 标记输出 | Structured output format instead of free-form text; enables downstream automation 结构化输出格式而非自由文本；支撑下游自动化 | |

## Xem thêm 延伸阅读

- [Li et al. — TrOCR (arXiv:2109.10282)](https://arxiv.org/abs/2109.10282)
- [Blecher et al. — Nougat (arXiv:2308.13418)](https://arxiv.org/abs/2308.13418)
- [Huang et al. — LayoutLMv3 (arXiv:2204.08387)](https://arxiv.org/abs/2204.08387)
- [Kim et al. — Donut (arXiv:2111.15664)](https://arxiv.org/abs/2111.15664)
- [Wang et al. — DocLLM (arXiv:2401.00908)](https://arxiv.org/abs/2401.00908)
