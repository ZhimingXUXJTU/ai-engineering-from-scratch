# ColPali và Vision-Native Document RAG  ColPali 视觉原生文档 RAG

> RAG truyền thống phân tích các file PDF thành văn bản, chia thành các mảnh, nhúng các mảnh, lưu trữ các vector. Mỗi bước mất tín hiệu: OCR bỏ dữ liệu biểu đồ, chia nhỏ các hàng bảng, nhúng văn bản bỏ qua các số liệu. ColPali (Faysse et al., tháng 7 năm 2024) đặt ra câu hỏi đơn giản hơn: tại sao lại trích xuất văn bản? Nhúng hình ảnh trang trực tiếp thông qua PaliGemma, sử dụng tương tác muộn kiểu ColBERT để lấy lại, và giữ tất cả bố cục, hình ảnh, phông chữ và tín hiệu định dạng tài liệu mang. Các điểm tham khảo được xuất bản: 20-40% độ chính xác đầu đến cuối tốt hơn so với văn bản-RAG trên các tài liệu giàu hình ảnh. ColQwen2, ColSmol và VisRAG đã mở rộng mô hình. Bài học này đọc luận án RAG về thị giác và xây dựng một chỉ số nhỏ giống ColPali.

> **【中文解读】**传统RAG trên PDF là kém hiệu suất, vì mỗi bước đều bị mất tín hiệu: OCR 丢图表、分块破坏表格行、文本嵌入忽略图片。ColPali hỏi một câu hỏi đơn giản hơn: tại sao cần lấy văn bản? trực tiếp sử dụng PaliGemma 嵌入页面图像, sử dụng MaxSim 延迟交互进行检查,保留文档的全部布局、图表、字体和格式信号──在视觉丰富文档上,RAG 准确率高于文本 20-40%──

> **【拓展：ColPali 在金融 RAG 中的应用】**财报 là hình thức điển hình nhất của thị trường tài liệu phong phú Q3  doanh thu tăng trưởng thường trong biểu đồ, khối ký hợp đồng là thực tế thiết kế chứ không phải thực tế văn bản. ColPali  trực tiếp nhúng hình ảnh trang, giữ lại tín hiệu trực quan hoàn chỉnh, rất phù hợp với báo cáo tài chính  hợp đồng  phát phiếu, vv. trường hợp.  Khóa kho mở bán khoảng 5-10 lần của RAG văn bản  thông qua PQ ), nhưng tăng giá trị chính xác thường đạt được chi phí này.

**Type:** Build
**Languages:** Python (stdlib, multi-vector indexer + MaxSim scorer)
**Prerequisites:** Phase 11 (LLM Engineering — RAG basics), Phase 12 · 05 (LLaVA)
**Time:** ~180 minutes

>  **【前置】**学本节前请先掌握:Phase 11·14-16(RAG 基础:embedding/chunking/retrieval)、Phase 11·13(ColBERT 延迟交互检索,ColPali 直接借鉴)、Phase 12·05(LLaVA 视觉编码器)。ColPali = "ColBERT for images"。
>  **【类比】**传统 RAG vs ColPali = "看书先扫描成纯文本" vs "直接看图找答案"──传统 = OCR 提取文字→分块→embedding(图表数据全部丢失);ColPali = 直接对页面图像做补丁嵌入(图表、表格、布局全保留)── 在金融报告中,ColPali 准确率高 20-40%──

## Mục tiêu học tập

- Giải thích sự khác biệt giữa việc lấy lại bộ mã hóa hai (một vector cho mỗi tài liệu) và việc lấy lại tương tác muộn (nhiều vector cho mỗi tài liệu).
  Trung ngữ翻译:解释双编码器检索(每文档一个向量) 和延迟交互检索(每文档多个向量) 的区别──
- Mô tả hoạt động MaxSim của ColBERT và cách ColPali tổng quát nó từ mã thông báo văn bản đến các bản vá hình ảnh.
  Trung ngữ翻译:描述 ColBERT's MaxSim 操作以及 ColPali 如何将其从文本代币推广到图像补丁──
- Xây dựng một chỉ mục nhỏ giống ColPali: trang → bản vá nhúng → MaxSim trên các bản nhúng từ truy vấn → top-k trang.
  中文翻译:构建一个微型 ColPali 式索引器:页面→patch 嵌入→对查询词嵌入做MaxSim→top-k 页面。
- So sánh ColPali + Qwen2.5VL máy phát điện vs văn bản-RAG + GPT-4 trên một trường hợp sử dụng hóa đơn / báo cáo tài chính.
  Trung文翻译: 在发票/金融报告用例上比较 ColPali + Qwen2.5-VL 生成器 vs 文本 RAG + GPT-4──

## Vấn đề  vấn đề giới thiệu

Text-RAG trên PDF ném đi hầu hết tài liệu. Tăng trưởng doanh thu quý 3 của báo cáo tài chính thường là trong biểu đồ; kết quả của báo cáo y tế là trong hình ảnh ghi chú; khối ký kết hợp đồng pháp lý là một thực tế bố trí, không phải là một thực tế văn bản.

> Các tài liệu trên PDF RAG đã bỏ qua phần lớn thông tin tài liệu.

Các đường ống văn bản-RAG:

> 文本 RAG 管道:

1. PDF → văn bản thông qua OCR / pdftotext.
   中文翻译:PDF → 通过 OCR/pdftotext 提取文本。
2. Text → 300-500 token.
   中文翻译:文本 → 300-500 token 的块──
3. Chunk → nhúng bộ mã hóa (một vector).
   中文翻译:块 → 双编码器嵌入(一个向量) 』
4. User query → embedding → cosine similarity → top-k chunks.
   中文翻译: user quer query → 嵌入 → 余弦相似度 → top-k 块。
5. Chunks + query → LLM.
   中文翻译:块 + 查询 → LLM。

5 bước mất tích, các biểu đồ không được ghi lại, bảng bị chia thành từng mảnh, bố cục nhiều cột bị phẳng, ghi chú hình ảnh biến mất.

> 五有损步骤――图表未捕获――图表被块截截切――多布局被展平――图表注释消失――

Giải pháp của ColPali: bỏ qua OCR, nhúng hình ảnh trang trực tiếp. Sử dụng tương tác muộn kiểu ColBERT để lấy lại để mô hình có thể tham gia vào các bản vá hạt mỏng vào thời điểm truy vấn.

> sửa đổi của ColPali: nhảy qua OCR, trực tiếp nhúng vào hình ảnh trang. Sử dụng ColBERT 风格的延迟交互进行检查, để mô hình có thể quan tâm vào các bản vá nhỏ trong khi truy vấn.

## Khái niệm cốt lõi

> **【中文解读】**ColPali sử dụng phương pháp trực quan hoàn thành RAG: không qua OCR, trực tiếp đặt trang tài liệu như hình ảnh mã hóa để đo, sử dụng kiểm tra tương tự trực quan.

> **【拓展：视觉原生 RAG 的优势**传统RAG管线(OCR -> 文本 -> 嵌入 -> 检索) 在复杂版面面(表格、图表、公式) 上经常失败。ColPali 直接在视觉层次匹配,无需OCR,在包含图表和表格的文档检索上上比传统方法提升 30-50%──缺点是需要更多存储(每页一个向量)。


> **【拓展：ColPali 的效率分析】**ColPali trong quá trình truy cập chậm tương đương với phương pháp truyền thống (khoảng 50ms/query), nhưng tỷ lệ xác thực trên tài liệu có chứa biểu đồ và biểu đồ tăng từ 30-50%.


### Colbert (2020)

ColBERT (Khattab & Zaharia, arXiv:2004.12832) là một phương pháp lấy lại văn bản. Thay vì một vector mỗi tài liệu, nó tạo ra một vector mỗi token.

> Colbert là một phương pháp kiểm tra văn bản không phải là mỗi tập tin một khối lượng, mà mỗi token một khối lượng.

- Các mã thông báo truy vấn có được các nhúng riêng của họ (N_q vector).
  Trung文翻译:查询 token 获得自己的嵌入(N_q 个向量)
- Các token tài liệu nhận được nhúng (N_d vector, thường được lưu trữ trong cache).
  Trung文翻译:文档代币 获得嵌入(N_d 个向量, thường缓存) 』
- Score = tổng trên các mã thông báo truy vấn của max trên các mã thông báo có tính tương tự cosine: Σ_i max_j cos(q_i, d_j).
  中文翻译:分数 = đối với mã thông báo 求和, mỗi mã thông báo 取文档 mã thông báo 中最大余弦相似度:Σ_i max_j cos(q_i, d_j) 』

Đây là hoạt động MaxSim. Mỗi mã thông báo truy vấn "tác" mã thông báo phù hợp nhất của mình. Điểm cuối cùng là tổng.

> Đây là hoạt động của MaxSim. Mỗi mã truy vấn chọn mã tài liệu phù hợp nhất.

Lợi thế: nhớ lại mạnh, xử lý ngữ nghĩa cấp thuật ngữ. Khác: N_d vector mỗi tài liệu, lưu trữ tốn kém.

> 优势:强召回率,处理词级语义――劣势: mỗi文档 N_d 个向量, lưu trữ đắt tiền――

### ColPali

ColPali (Faysse et al., arXiv:2407.01449) áp dụng mô hình ColBERT cho hình ảnh.

> ColPali sẽ sử dụng ColBERT 模式 để hình ảnh.

- Mỗi trang được mã hóa bởi PaliGemma (tiếng ViT +) thành các bản nhúng vá: N_p vector trên mỗi trang.
  Trung文翻译:每页由 PaliGemma(ViT + 语言)编码为补丁 嵌入:每页 N_p 个向量。
- Mỗi truy vấn người dùng (tin nhắn) được mã hóa vào các nội dung mã hóa truy vấn: N_q vector.
  Trung文翻译:每个用户查询(文本)编码为查询代币 嵌入:N_q 个向量。
- Score = Σ_i max_j cos(q_i, p_j), tức là, MaxSim trên truy vấn-text-tokens và page-image-patches.
  中文翻译:分数 = Σ_i max_j cos(q_i, p_j),即查询文本代币 和页面图像补丁的 MaxSim。
- Nhận lại các trang top-k theo điểm số tổng.
  Trung文翻译:按总分检索 top-k 页面──

Vào thời điểm nhập tài liệu: nhúng mỗi trang với PaliGemma, lưu trữ tất cả các bản nhúng vá. Vào thời điểm truy vấn: nhúng các mã thông báo truy vấn, tính toán MaxSim so với tất cả các bản nhúng trang được lưu trữ, trả về các trang top-k.

> 文档摄取时: dùng PaliGemma 嵌入每页, lưu trữ tất cả các bản vá 嵌入──查询时:嵌入查询代币,对所有存储的页面嵌入计算MaxSim,返回顶-k页面──

Lợi thế: kết thúc đến kết thúc vượt qua văn bản-RAG bằng 20-40% trên tài liệu giàu thị giác. Mỗi patch-vector nắm bắt bố cục và nội dung địa phương.

> 优势:端到端在视觉丰富文档上文 RAG cao hơn 20-40%── mỗi bản vá 向量捕获局部布局和内容──

Chưa thích: N_p patches × 4 byte floats × D-dim vectors per page = lưu trữ tăng nhanh. Giảm thiểu bởi PQ / OPQ quantization.

> 劣势:N_p 个补丁 × 4 字节浮点 × D 维向量 mỗi trang = 储存快速增长──可通过 PQ/OPQ 量化缓解──

### ColQwen2 và ColSmol

ColQwen2 (illuin-tech, 2024-2025) thay đổi PaliGemma với Qwen2-VL. Mã hóa cơ sở tốt hơn, lấy lại tốt hơn.

> ColQwen2 sẽ thay thế PaliGemma thành Qwen2-VL.

ColSmol là biến thể quy mô nhỏ hơn cho sử dụng địa phương / cạnh.

> ColSmol là một biến thể quy mô nhỏ hơn sử dụng ở địa phương / biên giới.

### VisRAG

VisRAG (Yu et al., arXiv:2410.10594) là một biến thể khác: thay vì MaxSim trên các bản vá, tập hợp mỗi trang thành một vector duy nhất với một VLM sau đó lấy lại bộ mã hóa hai. Chỉ mục nhanh hơn + lưu trữ nhỏ hơn, nhớ lại yếu hơn.

> VisRAG là một biến thể khác nhau: không phải là trên bản váy để làm MaxSim, mà bằng VLM sẽ phân tích mỗi trang thành một khối lượng đơn và tái lập trình tìm kiếm.

Sự đổi giá về chất lượng: ColPali cho chất lượng, VisRAG cho quy mô.

> 质量与成本的权衡:ColPali 追求质量,VisRAG 追求规模──

### M3DocRAG

M3DocRAG (Cho et al., arXiv:2411.04952) mở rộng tìm kiếm đa phương thức đến lý luận đa tài liệu nhiều trang.

> M3DocRAG sẽ mở rộng nhiều mô hình tìm kiếm đến nhiều trang tìm kiếm tài liệu.

### ViDoRe  chỉ số chuẩn

Định nghĩa chuẩn của ColPali. Đánh giá thu hồi tài liệu trực quan. Các nhiệm vụ bao gồm báo cáo tài chính, bài báo khoa học, tài liệu hành chính, hồ sơ y tế, hướng dẫn.

> Bộ phận quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý và quản lý của ColPali: Bộ phận quản lý quản lý và quản lý của ColPali: Bộ phận quản lý quản lý và quản lý của ColPali: Bộ phận quản lý quản lý và quản lý của ColPali: Bộ phận quản lý quản lý của ColPali: Bộ trưởng Bộ quản lý và quản lý của ColPali: Bộ trưởng Bộ quản lý: Bộ quản lý: Bộ trưởng Bộ quản lý và quản lý: Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ Bộ

ColPali-v1 ghi điểm ~ 80% nDCG@5 trên ViDoRe; text-RAG trên các tài liệu tương tự ghi điểm ~ 50-60%.

> ColPali-v1 trên ViDoRe lên khoảng 80% nDCG@5; văn bản RAG trên cùng một tài liệu khoảng 50-60%。

### Đường ống dẫn RAG đầu đến cuối

Đối với một RAG thị giác:

> 视觉原生 RAG 管道:

1. Thêm: PDF → hình ảnh trang → PaliGemma mã hóa → lưu trữ tất cả các bản nhúng vá.
   中文翻译:摄取:PDF → 页面图像 → PaliGemma 编码 → 存储所有补丁 嵌入──
2. Query: User text → embedment query-token → MaxSim đối với tất cả các trang được chỉ mục → top-k pages.
   Trung文翻译:查询:用户文本 → 查询 token 嵌入 → đối với tất cả các trang chỉ dẫn làm MaxSim → top-k 页面。
3. Tạo: top-k trang hình ảnh + truy vấn → VLM (Qwen2.5-VL hoặc Claude) → câu trả lời.
   中文翻译:生成:top-k 页面图像 + 查询 → VLM(Qwen2.5-VL 或 Claude)→ 回答。

Không có OCR ở đâu cả. Hình ảnh, biểu đồ, phông chữ, bố cục đều chảy vào câu trả lời.

> n toàn không có OCR. n toàn không có OCR.

### Hóa toán lưu trữ

Một báo cáo tài chính 50 trang với 729 bản vá trên mỗi trang và 128 chiều:

> 50 页 财报, mỗi trang 729 个补丁,128 维嵌入:

- ColPali: 50 * 729 * 128 * 4 byte = ~ 18 MB nguyên liệu, ~ 4 MB sau PQ.
  中文翻译:ColPali:50 * 729 * 128 * 4 字节 = 约 18 MB 原始,PQ 后约 4 MB。
- Text-RAG: 50 mảnh * 768-dim * 4 byte = ~ 150 kB.
  中文翻译:文本 RAG:50块 * 768 维 * 4 字节 = 约150 kB。

ColPali là khoảng 30 lần lưu trữ nhiều hơn cho mỗi tài liệu. Ở quy mô, OPQ / PQ làm giảm nó xuống còn ~ 5-10x, thường dung nạp.

> ColPali Mỗi lưu trữ tài liệu khoảng 30 lần.

### Khi text-RAG vẫn thắng

- Tài liệu văn bản thuần túy không có tín hiệu bố trí (thương tự wiki, nhật ký trò chuyện). Text-RAG đơn giản hơn và lưu trữ rẻ hơn.
  Trung ngữ翻译:无布局信号的纯文本文档(维基文章、聊天记录) ――文本 RAG 更简单且存储更便宜──
- Các hồ sơ hàng triệu trang nơi lưu trữ chiếm ưu thế về chi phí.
  Trung ngữ翻译:数百万页档案, lưu trữ chi phí chiếm chủ yếu.
- Các yêu cầu quy định nghiêm ngặt đòi hỏi văn bản OCR có thể thu được bên cạnh việc lấy lại.
  Trung文翻译:严格要求可提取 OCR 文本与检索并存的监管要求.

Đối với tất cả mọi thứ khác vào năm 2026  báo cáo tài chính, bài báo khoa học, hợp đồng pháp lý, hồ sơ y tế, tài liệu UX  RAG vision-native thắng.

> 2026 tất cả các trường hợp khác 财报, khoa học, văn bản, hợp đồng pháp lý, hồ sơ y tế, UX 文档 视觉原生 RAG 胜出.

## Hãy sử dụng nó để thực hiện
```figure
mm-maxsim
```

## Sử dụng nó

`code/main.py`- Có thể là:

- Mã hóa đệm đồ chơi: lập bản đồ một "trần" (trung nhỏ các vector tính năng) cho một loạt các bản nhúng đệm.
  Trung文翻译:玩具补丁编码器:将"页面" (trước: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题: 标题
- Máy ghi điểm MaxSim: tính toán điểm số theo kiểu ColBERT giữa một bộ tích hợp mã thông báo truy vấn và một bộ vá trang.
  Trung文翻译:MaxSim 评分器:计算查询 token 嵌入集和页面补丁集 集之间 ColBERT 风格分数──
- Chỉ số 5 trang đồ chơi, chạy 3 truy vấn, trả lại top-k với điểm số.
  Trung文翻译:索引 5 个玩具页面,运行 3 个查询,返回带分数的顶-k――

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-vision-rag-designer.md`Với dự án tài liệu-RAG, chọn ColPali / ColQwen2 / VisRAG / text-RAG và kích thước lưu trữ.

> 本课产 出 `outputs/skill-vision-rag-designer.md` 给定文档 RAG 项目, chọn ColPali / ColQwen2 / VisRAG / 文本 RAG 并估算储存──

## Tập luyện bài tập

1. Một báo cáo hàng năm 200 trang với 729 bản vá trên mỗi trang, 128-dimen emb, 4byte floats. tính toán lưu trữ nguyên liệu và PQ-đẹp (8x) lưu trữ. 200 trang 年报,729 bản vá/页,128维嵌入,4 字节浮点──计算原始存储和 PQ 压缩(8 倍)后储──

2. MaxSim là Σ_i max_j cos(q_i, p_j). Tổng số này nắm bắt được gì mà một sự tương đồng trung bình đơn giản không? MaxSim là Σ_i max_j cos(q_i, p_j) ‒

3. ColPali chỉ mục các trang như bộ váy. Những thay đổi gì nếu chúng ta chỉ mục ở mức từ (như ColBERT làm)? Trade-offs? ColPali 以 patch 集索引页面。如果改为词级索引(如 ColBERT),会怎么样?有什么取舍?

4. Thiết kế đường ống dẫn đầu đến cuối cho một bộ phận 1M trang với ngân sách độ trễ 500ms mỗi truy vấn. Chọn ColQwen2 / VisRAG và biện minh.

5. Đọc M3DocRAG (arXiv:2411.04952). Mô tả mô hình chú ý nhiều trang và cách nó khác với tìm kiếm ColPali một trang.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Late interaction | "ColBERT-style" 延迟交互 | Retrieval using per-token or per-patch embeddings + MaxSim, not a single doc vector 使用逐 token/patch 嵌入 + MaxSim 的检索，非单向量 | |
| MaxSim | "Max-over-patches" 最大相似度 | For each query token, pick the highest-similarity document token; sum across query 对每个查询 token 选最高相似度的文档 token；跨查询求和 | |
| Bi-encoder | "Single-vector" 双编码器 | One vector per document; faster but loses granularity 每文档一个向量；更快但丢失粒度 | |
| Multi-vector | "Many-vectors-per-doc" 多向量索引 | Store N_p vectors per document / page; storage cost grows but recall improves 每文档/页存储 N_p 个向量；存储增长但召回提升 | |
| Patch embedding | "Page feature" 图像块嵌入 | One vector per image patch from a VLM encoder, cached per page VLM 编码器输出的每 patch 一个向量，按页缓存 | |
| ViDoRe | "Vision doc bench" 视觉文档检索基准 | ColPali's benchmark suite for visual document retrieval ColPali 的视觉文档检索基准套件 | |
| PQ quantization | "Product quantization" 乘积量化 | Compression that maintains vector similarity while shrinking storage ~8x 保持向量相似度的同时压缩存储约 8 倍 | |

## Xem thêm 延伸阅读

- [Faysse et al. — ColPali (arXiv:2407.01449)](https://arxiv.org/abs/2407.01449)
- [Khattab & Zaharia — ColBERT (arXiv:2004.12832)](https://arxiv.org/abs/2004.12832)
- [Yu et al. — VisRAG (arXiv:2410.10594)](https://arxiv.org/abs/2410.10594)
- [Cho et al. — M3DocRAG (arXiv:2411.04952)](https://arxiv.org/abs/2411.04952)
- [illuin-tech/colpali GitHub](https://github.com/illuin-tech/colpali)
