# Watermarking  SynthID, Stable Signature, C2PA 稳定签名 水印 SynthID C2PA

> Ba công nghệ cấu trúc 2026 nguồn gốc nội dung được tạo ra bởi AI. SynthID (Google DeepMind)  đánh dấu nước hình ảnh được tung ra vào tháng 8 năm 2023, văn bản + video tháng 5 năm 2024 (Gemini + Veo), văn bản nguồn mở tháng 10 năm 2024 thông qua Responsible GenAI Toolkit, bộ phát hiện đa phương tiện thống nhất tháng 11 năm 2025 cùng với Gemini 3 Pro. Đánh dấu nước văn bản điều chỉnh khả năng lấy mẫu mã tiếp theo một cách không thể nhận thấy; dấu nước hình ảnh / video tồn tại khi nén, cắt, lọc, thay đổi tốc độ khung hình. Stable Signature (Fernandez et al., ICCV 2023, arXiv:2303.15435)  chỉnh sửa kỹ thuật giải mã phân tán ẩn để mỗi đầu ra chứa một thông điệp cố định; hình ảnh được cắt (10% nội dung) được phát hiện > 90% tại FPR<1e-6. Tiếp theo "Signature stable is Unstable" (arXiv:2405.07145, tháng 5 năm 2024)  điều chỉnh tinh tế loại bỏ dấu nước trong khi vẫn giữ chất lượng. C2PA  chuẩn metadata có dấu hiệu mã hóa, rõ ràng là bị vi phạm (C2PA 2.2 Explainer 2025). Watermarking và C2PA là bổ sung: metadata có thể được xóa nhưng mang nguồn gốc phong phú hơn; watermark tồn tại thông qua transcoding nhưng mang ít thông tin hơn.

> **【中文解读】**Bài viết này giới thiệu về công nghệ in nước AI SynthID、C2PA等 nhận dạng AI tạo nội dung.

> **【拓展：水印 → Deepfake 检测】**水印是深fake 检测的核心技术路径.SynthID的跨模态检测器 (SynthID) có thể đọc tín hiệu từ văn bản, hình ảnh, âm thanh và video. Nhưng giới hạn rõ ràng: mô hình cụ thể.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, token-watermark embed + detect) | **语言:** Python（标准库，token 水印嵌入 + 检测）
**Prerequisites:** Phase 10 · 04 (sampling), Phase 01 · 09 (information theory) | **前置知识:** Phase 10 · 04 (采样), Phase 01 · 09 (信息论)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前请先掌握:Phase 10·04(采样) 、Phase 01·09(信息论) ⋅ 三大水印技术 + 内容追溯标准。
>  **【类比】**水印 = "AI 内容的隐形身份证"──SynthID(Google) = 调整下面代码的采样偏好"绿色"代码,不可察知但可检测;Stable Signature = 微调解码器让每张图都含固定二进制消息(裁剪 10% 仍 >90% 检出);C2PA = 加密签名元数据──互补:元数据可剥但信息丰富;水抗印转码但信息少──
> ️ "Signature stable 不稳定"2024.5:微调即可移除水印保质量──水印不是银弹──

## Mục tiêu học tập

- Mô tả đánh dấu nước cấp token (tý thức văn bản SynthID) và cơ chế mà nó có thể phát hiện.
- Mô tả Stable Signature và cuộc tấn công gỡ bỏ năm 2024 đã phá vỡ nó.
- Vai trò của C2PA của nhà nước và lý do tại sao nó bổ sung cho watermarking.
- Mô tả những hạn chế chính: tín hiệu cụ thể cho mô hình, độ vững chắc dưới sự phác thảo và các cuộc tấn công bảo tồn ý nghĩa (arXiv:2508.20228).

> Mô tả của SIGNATURE và 2024 phá hủy nó và tấn công C2PA và lý giải tại sao nó có liên quan đến SIGNATURE. Mô tả về giới hạn quan trọng: mô hình đặc biệt tín hiệu, sự cố và ý nghĩa của nó để giữ cho tấn công.

## Vấn đề  vấn đề

2023-2024 đã thấy các nội dung giả mạo sâu và nội dung được tạo ra bởi AI xâm nhập vào bối cảnh chính trị và tiêu dùng ở quy mô lớn. Watermarking là tín hiệu xuất phát kỹ thuật được đề xuất: đánh dấu các thế hệ tại thời điểm tạo, phát hiện chúng sau đó. 2025 bằng chứng: không có dấu nước chắc chắn không điều kiện, nhưng được xếp lớp với các metadata C2PA sự kết hợp cung cấp một câu chuyện xuất phát có thể sử dụng.

> 2023-2024 năm sâu giả mạo và AI tạo nội dung vào quy mô lớn vào các trường hợp chính trị và tiêu thụ.

## Khái niệm

> **【中文解读】**文本水印机(Kirchenbauer 等人 2023, bởi Google 产品化): mỗi giải mã bước sẽ trước K 个令牌哈希产生词汇表的伪随机"绿色"和"红色"分区,向绿色logits 添加 delta 偏置采样――生成包含比随机更多的绿色令牌――检测:重新哈希每个前,计量生成中的绿色令牌,计算 z 分数――水印文本 z > 0,人类文本 z ~ 0。

### Đánh dấu nước văn bản (tý dạng văn bản SynthID)

Cơ chế Kirchenbauer et al. 2023 được sản xuất bởi Google:

1. Tại mỗi bước giải mã, kết hợp các mã thông báo K trước đó để tạo ra một phân vùng ngẫu nhiên của từ vựng thành tập hợp "công màu xanh lá cây" và "màu đỏ".
2. Tiến mẫu Bias hướng đến tập hợp xanh bằng cách thêm δ vào các logit xanh.
3. Thế hệ này chứa nhiều mã thông báo xanh hơn so với tình cờ.

Khám phá: tái ghi lại từng tiền tố, đếm các mã thông báo xanh trong thế hệ, tính toán điểm z. Điểm z là >0 cho văn bản có dấu nước, ~0 cho văn bản con người.

Các tính chất:
- Không thể nhận thấy được đối với người đọc (δ đủ nhỏ để mất chất lượng là nhỏ).
- Khám phá với truy cập vào chức năng phân vùng từ vựng.
- Không mạnh mẽ để diễn tả  viết lại văn bản phá hủy tín hiệu.

SynthID-text là nguồn mở tháng 10 năm 2024 thông qua Responsible GenAI Toolkit của Google.

> **【中文解读】**Stable Signature(Fernandez 等人, ICCV 2023) Micro调潜在扩散解码器使每个生成图像包含固定二进制消息──剪到原始内容10%的图像在 FPR<1e-6 下检测率 >90%──但2024 年 5 月"Stable Signature is Unstable"证明微调解码器可以在保持图像质量同时移除水印对抗性生成后微调成本低──

### Chữ ký ổn định (hình ảnh)

Fernandez et al. ICCV 2023. Định chỉnh bộ giải mã phân tán tiềm ẩn để mỗi hình ảnh được tạo chứa một tin nhắn nhị phân cố định được nhúng vào đại diện tiềm ẩn. Khám phá được giải mã từ tiềm ẩn bằng một bộ giải mã thần kinh. Hình ảnh cắt (tới 10% nội dung) được phát hiện >90% tại FPR<1e-6.

> Stable Signature 微调潜在扩散解码器 cho phép mỗi hình ảnh được tạo chứa các thông tin định nghĩa thứ hai.

Tháng 5 năm 2024 "Signature stable is unstable" (arXiv:2405.07145): điều chỉnh tinh tế của bộ giải mã loại bỏ dấu nước trong khi vẫn giữ chất lượng hình ảnh.

> 2024 5 月 "Signature stable is unstable" chứng minh máy mã hóa có thể giữ chất lượng hình ảnh đồng thời di chuyển nước印―― tạo ra giá thấp sau khi chống chịu; nước印的对抗鲁棒性有限――

### Bộ phát hiện đơn nhất SynthID (Tháng 11 năm 2025)

Cùng với Gemini 3 Pro: một bộ phát hiện đa phương tiện đọc tín hiệu SynthID từ văn bản, hình ảnh, âm thanh và video trong một API. Thống gốc Google thống nhất.

> 伴随 Gemini 3 Pro: một bộ kiểm tra hình thức, có thể đọc từ văn bản, hình ảnh, âm thanh và video trong SynthID 信号──统一 Google nguồn kỹ thuật──

> **【拓展：C2PA + 水印互补 → EU AI Act Article 50】**C2PA và nước bản đồ互补:元数据可剥离但带丰富来源链;水印通过转码持久但只带少量比特──Google集成在搜索,广告和"关于此图片"中两者──EU AI Act Điều 50 của minh bạch mã hóa yêu cầu AI tạo ra nội dung nhãn (包括 Deepfake), đây là cần phải Bài học 23 Lớp quản lý kỹ thuật nước bản đồ──

### C2PA

Liên minh về nguồn gốc và xác thực nội dung. Tiêu chuẩn metadata rõ ràng bị vi phạm được ký mật mã. C2PA 2.2 Giải thích (2025). Một bản khai báo C2PA ghi lại tuyên bố nguồn gốc (người đã tạo ra, khi nào, những biến đổi nào) được ký bởi khóa của người tạo.

> C2PA là chữ ký mật mã, bảo vệ dữ liệu của người sáng lập.

Tương tự với watermarking:
- Các metadata có thể bị xóa; dấu nước không thể (hiện dễ dàng).
- Các metadata giàu (chuỗi nguồn gốc đầy đủ); dấu nước mang các bit.
- C2PA phụ thuộc vào việc áp dụng nền tảng; dấu nước được nhúng tự động.

> Với bản in kết nối:元数据可剥离但信息丰富;水印通过转码持久但只携带少量比特;;C2PA phụ thuộc vào nền tảng sử dụng;水印自动嵌入;;

Google tích hợp cả trong Tìm kiếm, quảng cáo và "Thiết kế này".

> Google tập hợp hai trong tìm kiếm, quảng cáo và "thường về hình ảnh này".

> **【拓展：水印局限性 → 模型特定信号问题】**关键局限性:SynthID 水印仅来自启用SynthID模型──"无SynthID 信号" không bằng chứng thực tế未启用SynthID模型生成的任何内容都不会有水印──此外,arXiv:2508.20228(2025) cho thấy ý nghĩa giữ cuộc tấn công có thể phá hủy văn bản水印和多种图像水印──

### Các giới hạn

- **Model-specific.**SynthID watermarks thế hệ từ các mô hình được bật SynthID. Một thế hệ từ một mô hình không có SynthID không được đánh dấu bằng nước, vì vậy "không có tín hiệu SynthID" không phải là bằng chứng về tính xác thực.
- **Paraphrase.**Các dấu nước văn bản không tồn tại trong các đoạn phác thảo giữ lại ý nghĩa.
- **Transformation attacks.**arXiv:2508.20228 (2025) cho thấy các cuộc tấn công bảo tồn ý nghĩa phá hủy cả dấu nước văn bản và nhiều dấu nước hình ảnh.
- **Fine-tune removal.**Theo "Signature ổn định là không ổn định", chỉnh sửa tinh tế sau thế hệ loại bỏ các dấu hiệu nước nhúng.

### Đạo luật AI của EU Điều 50

Bộ luật minh bạch cho việc dán nhãn nội dung được tạo ra bởi AI (mở đầu tiên vào tháng 12 năm 2025, dự thảo thứ hai vào tháng 3 năm 2026, dự kiến cuối cùng vào tháng 6 năm 2026 theo các quy định của quy định của quy định tại quy định của quy định tại quy định của quy định tại quy định của quy định tại quy định của quy định tại quy định của quy định tại quy định tại quy định của quy định tại quy định tại quy định của quy định tại quy định tại quy định tại quy định của quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định tại quy định:[European Commission status page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)(c) Bộ luật vẫn còn trong dự thảo từ tháng 4 năm 2026 và thời gian có thể thay đổi.

### Khi điều này phù hợp với giai đoạn 18

Bài học 22-23 là về những gì mô hình phát ra (dữ liệu riêng tư, tín hiệu xuất xứ). Bài học 27 bao gồm quản lý dữ liệu đào tạo. Bài học 24 là khuôn khổ quy định đòi hỏi các biện pháp kỹ thuật này.

> Bài học 22-23 关于模型发发出什么(私有数据、来源信号) ・ Bài học 27 涵盖训练数据管理―― Bài học 24 là yêu cầu khung quản lý các biện pháp kỹ thuật này――

## Sử dụng nó.
```figure
an-watermark-greenlist
```

## Sử dụng nó

`code/main.py`xây dựng một dấu nước văn bản đồ chơi. Các mã thông báo là số nguyên số 0..N-1; dấu nước lấy mẫu thiên hướng đến bộ màu xanh lá cây được xác định bằng hash. Một máy dò tính điểm z của mã thông báo xanh lá cây. Bạn có thể quan sát phát hiện ở 1000 thế hệ mã thông báo, xem cách phác thảo phá hủy tín hiệu và đo lường tỷ lệ dương tính sai trên văn bản con người.

> `code/main.py`构建玩具文本水印──令牌是整数 0.N-1;水印采样偏向哈希定义的绿色集──检测器计算绿色令牌 z 分数──你可以观察1000 令牌生成的检测、释义破坏信号以及人类文本上的误报率──

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-provenance-audit.md`. Với việc triển khai nội dung với tuyên bố xuất xứ, nó kiểm toán: cơ chế watermark (nếu có), chuỗi ký kết C2PA (nếu có), độ bền đối kháng của mỗi loại và bảo hiểm theo từng modality.

> 本课产 出 `outputs/skill-provenance-audit.md` Đưa ra các tuyên bố có nguồn gốc: Content deploy, audit: waterprint mechanisms, C2PA  signature chain, các đối tác chống lại sự cố và từng mô hình bao phủ.

## Tập luyện bài tập

1. Đi chạy`code/main.py`. báo cáo điểm z cho hệ thống 1000 token được đánh dấu bằng nước so với văn bản do con người viết.

2. Thực hiện một cuộc tấn công phrasing thay thế 30% mã thông báo bằng các từ đồng nghĩa.

3. Đọc Kirchenbauer et al. 2023 Phần 6 về độ bền. Tại sao các dấu nước văn bản thất bại trong việc phác thảo nhưng các dấu nước hình ảnh tồn tại khi cắt?

4. Thiết kế một triển khai sử dụng SynthID-text + C2PA metadata. Mô tả chuỗi nguồn gốc mà người tiêu dùng thấy. Xác định một chế độ thất bại của mỗi thành phần.

5. Kết quả 2024 "Signature ổn định không ổn định" cho thấy điều chỉnh tinh tế loại bỏ dấu nước hình ảnh. Thiết kế một điều khiển triển khai hạn chế cuộc tấn công này.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| SynthID | "Google's watermark" | Cross-modal provenance signal; text, image, audio, video |
| Token watermark | "Kirchenbauer-style" | Biased-sampling text watermark detectable via green-token z-score |
| Stable Signature | "image watermark" | Fine-tuned-decoder watermark; ICCV 2023 |
| C2PA | "the metadata standard" | Cryptographically signed tamper-evident provenance metadata |
| Paraphrase robustness | "does rewording break it" | Text watermark property; currently limited |
| Fine-tune removal | "adversarial unwatermark" | Attack that removes image watermark via decoder fine-tuning |
| Cross-modal detector | "unified SynthID" | November 2025 unified API across modalities |

## Xem thêm 延伸阅读

- [Kirchenbauer et al. — A Watermark for Large Language Models (ICML 2023, arXiv:2301.10226)](https://arxiv.org/abs/2301.10226) cơ chế watermark token
- [Fernandez et al. — Stable Signature (ICCV 2023, arXiv:2303.15435)](https://arxiv.org/abs/2303.15435) hình ảnh giấy watermark
- ["Stable Signature is Unstable" (arXiv:2405.07145)](https://arxiv.org/abs/2405.07145) cuộc tấn công dỡ bỏ
- [Google DeepMind — SynthID](https://deepmind.google/models/synthid/) dấu nước hình thái chéo
- [C2PA 2.2 Explainer (2025)](https://c2pa.org/specifications/specifications/2.2/explainer/Explainer.html) Tiêu chuẩn siêu dữ liệu
