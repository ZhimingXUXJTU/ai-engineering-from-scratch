# Visual Autoregressive Modeling (VAR): dự đoán quy mô tiếp theo 视觉自归建模 (VAR):下一尺度预测

> Các mô hình phân tán lấy mẫu lặp đi lặp lại theo thời gian (chước đánh dấu). Các mẫu VAR lặp đi lặp lại theo quy mô  nó dự đoán một token 1x1, sau đó 2x2, sau đó 4x4, cho đến độ phân giải cuối cùng, mỗi quy mô điều chỉnh trên quy mô trước đó. Bài báo 2024 cho thấy VAR phù hợp với các quy luật quy mô kiểu GPT cho việc tạo hình ảnh và đánh bại DiT với ngân sách tính toán tương tự. Bài học này xây dựng cơ chế cốt lõi.

> **【中文解读】**扩散模型在时间维度上代采样 (代采样), VAR在尺度维度上代先预测 1x1 token,再2x2,再4x4,直到目标分辨率──2024年论文证明 VAR 展现了GPT 风格的规模法,在相同计算预算下超越DiT──

> **【拓展：VAR 是生成模型的新范式】**VAR sẽ tự trở lại tư tưởng từ "được mở rộng từ một biểu tượng tiếp theo đến một thước đo tiếp theo", mở ra một hướng mới cho việc tạo ra hình ảnh. Nó có thể trở thành mô hình sản xuất thế hệ tiếp theo sau mô hình tiếp theo.

**Type:** Build / 构建型
**Languages:** Python (with PyTorch)
**Prerequisites:** Phase 7 Lesson 03 (Multi-Head Attention / 多头注意力), Phase 8 Lesson 06 (DDPM)
**Time:** ~90 minutes

## Vấn đề  vấn đề giới thiệu

Thế hệ tự do thống trị mô hình hóa ngôn ngữ vì nó có quy mô dự đoán: tính toán nhiều hơn, nhiều tham số hơn, độ bối rối thấp hơn, kết quả tốt hơn.

> Bản thân quay lại tạo ra trong ngôn ngữ xây dựng chiếm vị trí chủ đạo bởi vì nó có thể dự đoán mở rộng: nhiều hơn tính toán, nhiều hơn tham số, ít hơn bối rối, tốt hơn xuất khẩu.

Cả hai đều bị một vấn đề thứ tự thế hệ. Pixel và token được sắp xếp trong một lưới 2D, nhưng mô hình AR phải truy cập chúng trong một thứ tự raster 1D. Một pixel góc sớm không biết hình ảnh cuối cùng trở thành gì. Chất lượng thế hệ leo thang tồi tệ hơn GPT-on-text và không bao giờ đạt đến chất lượng mô hình phân tán với tính toán phù hợp.

> 两者都困难在生成顺序问题──像素和代币 排列在2D 网格中, nhưng AR 模型必须以1D 光顺序访问──早期角落像素不知道图像最终会变成什么──生成质量扩展不像GPT,在相同的计算量下从未达到扩散模型质量──

VAR khắc phục vấn đề thứ tự thế hệ bằng cách thay đổi những gì đang được tạo ra. Thay vì dự đoán các mã thông báo hình ảnh một một trong không gian, VAR dự đoán một bức ảnh toàn bộ với độ phân giải tăng lên. Bước 1: dự đoán một mã thông báo 1x1 (tổng hình "sự tóm tắt"). Bước 2: dự đoán một lưới mã thông báo 2x2 (chức năng rỗng hơn). Bước 3: dự đoán một lưới 4x4. Bước K: dự đoán lưới cuối cùng (H/8) x ((W/8)).

> VAR  thông qua thay đổi tạo đối tượng để sửa đổi tạo thứ tự vấn đề。 không còn từng không gian dự đoán hình ảnh token, VAR bằng tăng độ phân giải dự đoán toàn bộ hình ảnh。 bước 1: dự đoán 1x1 token( toàn局摘要)。 bước 2: dự đoán 2x2 token 网格── bước K: dự đoán cuối cùng网格──

Mỗi thang đo sẽ theo dõi tất cả các thang đo trước đó (từ nguyên nhân đến "sự sắp xếp quy mô") và song song song trong thang đo riêng của nó. Vấn đề thứ tự biến mất: toàn bộ hình ảnh ở thang k được tạo ra trong một chuyển đổi.

> Mỗi thước chú ý đến tất cả các thước trước đó (nếu có kết quả trong "định dạng thước"), trong thước riêng của nó đi cùng đi.

> **【中文解读】**VAR(Visual Autoregressive) của cốt lõi sáng tạo: sẽ hình ảnh tạo tự quay lại theo thứ tự từ " từng hình ảnh / từng token " biến thành " từng thước "。 trước tiên dự đoán tổng kết của 1x1 , tái 2x2 , tái 4x4 chi tiết, cho đến mục tiêu phân giải。 mỗi thước trong các dòng tạo, loại bỏ " vấn đề tự tạo của hình ảnh truyền thống AR "。2024 năm luận chứng minh VAR  thể hiện tương tự như GPT của quy mô Luật。

> **【拓展：VAR 与扩散模型的对比】**VAR là mô hình có tiềm năng nhất sau mô hình tiếp tục lan rộng tạo ra mô hình mới. Ưu điểm: 1) 清晰 Scaling Law像GPT一样可预测扩展; 2) 生成过程结构化先全局后局部,更符合人类感觉; 3) 在相同计算预算下超越DiT.

## Khái niệm cốt lõi

### VQ-VAE Multi-Scale Tokenizer

> ### VQ-VAE 多尺度 Tokenizer

VAR cần một **multi-scale discrete tokenizer**Đối với hình ảnh x, nó tạo ra một chuỗi các lưới token độ phân giải cao hơn dần:

> VAR  cần một**多尺度离散 tokenizer**Đối với hình ảnh x, nó tạo ra một loạt các biểu tượng phân giải tăng lên:

```
x -> encoder -> latent f
f -> tokenize at 1x1: token grid z_1 of shape (1, 1)
f -> tokenize at 2x2: token grid z_2 of shape (2, 2)
...
f -> tokenize at (H/p)x(W/p): token grid z_K of shape (H/p, W/p)
```

Mỗi z_k sử dụng cùng một sổ mã (khu thước điển hình 4096-16384).

```
f ≈ upsample(embed(z_1), target_size) + ... + upsample(embed(z_K), target_size)
```

Đây là một **residual VQ**Kích thước k chụp những gì các quy mô 1..k-1 bỏ lỡ. Decoder lấy tổng số tất cả các nhúng quy mô và tạo ra hình ảnh.

> Đó là một**残差 VQ**变体──尺度 k 捕获尺度 1..k-1 遗漏的内容──解码器将所有尺度嵌入并产生图像──

VQ Tokenizer đa quy mô được đào tạo một lần (như VQGAN) và sau đó đóng băng.

> 多尺度 VQ tokenizer 训练一次 (像 VQGAN) 然后结――所有生成工作由上层的自归模型完成――

### Dự đoán về quy mô tiếp theo

> ### 下一尺度预测

Mô hình tạo là một bộ biến đổi nhìn thấy các token từ tất cả các thang trước đó và dự đoán các token ở thang kế tiếp.

> 生成模型 là một biến thể, nhìn thấy tất cả các biểu tượng của các thước trước và dự đoán các biểu tượng của các thước sau.

Cấu trúc chuỗi đầu vào:
```
[START, z_1 tokens, z_2 tokens, z_3 tokens, ..., z_K tokens]
```

Các vị trí được nhúng mã hóa cả chỉ số thang và vị trí không gian trong thang. Sự chú ý là nguyên nhân theo thứ tự thang: token ở thang k, vị trí (i, j) có thể quan tâm đến tất cả các token ở thang 1..k và đến các token ở thang k chính nó đến sớm hơn trong bất kỳ thứ tự nội bộ quy mô nào được sử dụng (VAR sử dụng sự chú ý vị trí cố định mà không có sự liên quan đến nội bộ quy mô  tất cả các vị trí trong thang được dự đoán song song).

Thiệt lỗ đào tạo: tại mỗi thang k, dự đoán các token z_k được cho tất cả các token thang trước. Thiệt lỗ entropy chéo trên các mã VQ riêng biệt.

### Thế hệ

Khi kết luận:
```
generate z_1 = sample from p(z_1)                    # 1 token
generate z_2 = sample from p(z_2 | z_1)              # 4 tokens in parallel
generate z_3 = sample from p(z_3 | z_1, z_2)         # 16 tokens in parallel
...
decode: f = sum of embed-and-upsample scales 1..K
image = VAE_decoder(f)
```

Đối với quy mô K = 10, thế hệ là 10 chuyển đổi chuyển tiếp. Mỗi lần đi lại tạo ra toàn bộ quy mô của nó song song  không có tự rút theo mã trong quy mô. Đối với hình ảnh 256x256 đây là khoảng 10 lần đi qua so với DiT 28-50.

> Đối với K = 10 个尺度,生成是10次变压器 前向传播──每次产生整个尺度尺度内无分代号自归──256x256 图像约10次传播 vs DiT的28-50次──

### Tại sao quy mô tiếp theo thắng hơn quy mô tiếp theo

> ### Tại sao một thước đo thấp hơn một token thấp hơn

Ba chiến thắng cơ cấu:

> 3 lợi thế cấu trúc:

1. **Coarse-to-fine aligns with natural image statistics.**Nhận thức trực quan của con người và các bộ dữ liệu hình ảnh đều có tính thường lệ phụ thuộc vào quy mô: cấu trúc tần số thấp ổn định và có thể dự đoán được; chi tiết tần số cao phụ thuộc vào nội dung tần số thấp. Dự đoán quy mô tiếp theo khai thác điều này.
   **从粗到细与自然图像统计一致。**低频结构稳定可预测;高频细节依赖低频内容──
2. **Parallel generation within scale.**Không giống như token AR kiểu GPT, VAR tạo ra tất cả các token ở một quy mô trong một bước.
   **尺度内并行生成。**Không giống như GPT 风格 của token AR, VAR một bước tạo ra toàn bộ kích thước của token.
3. **No generation order bias.**Các token ở thang k nhìn thấy tất cả các thang k-1; không có "vẫn" hoặc "nâng" thiên vị buộc các token sớm phải cam kết trước khi bối cảnh muộn có sẵn.
   **无生成顺序偏差。**Địa chỉ của thước k  xem thước k-1 của toàn.

### Luật quy mô

> ### Luật quy mô / 缩放定律

Tian và các đồng nghiệp. chứng minh rằng VAR theo đường cong quy mô pháp luật cho FID trên ImageNet  giống như GPT làm cho sự bối rối. Việc tăng gấp đôi các tham số hoặc tính toán một cách đáng tin cậy làm giảm một nửa lỗi. Đây là mô hình tạo hình ảnh đầu tiên thể hiện kiểu hành vi quy mô này một cách sạch sẽ như mô hình ngôn ngữ. Kết quả là dự đoán quy mô VAR trở nên dự đoán từ tính toán, không phải phỏng đoán thực nghiệm cho mỗi kiến trúc.

> Tian 等人 chứng minh VAR trên ImageNet trên FID  theo luật lệ curvature 像 GPT đối với sự bối rối như vậy── gấp đôi các tham số hoặc tính toán lượng đáng tin cậy sẽ giảm sai lệch một nửa── đây là mô hình hình ảnh tạo ra mô hình hình ngôn ngữ rõ ràng như mô hình này biểu hiện hành vi curvature ⋅

### Mối quan hệ với sự pha trộn

> ### Quan hệ với mô hình mở rộng

VAR và diffusion chia sẻ cùng một câu chuyện nén dữ liệu: cả hai phá vỡ vấn đề sản xuất thành một chuỗi các phụ vấn dễ dàng hơn.

> VAR và mở rộng chia sẻ cùng một câu chuyện nén dữ liệu: tất cả sẽ tạo ra các vấn đề phân chia thành chuỗi các vấn đề đơn giản hơn.

- Phân phối: dần dần thêm tiếng ồn, học cách hủy bỏ một bước.
  扩散: từng bước tăng tiếng ồn, học rút lại từng bước.
- VAR: dần dần thêm độ phân giải, học cách dự đoán quy mô tiếp theo.
  VAR: từng bước tăng độ phân giải, học dự đoán

Cả hai đều tạo ra phân phối điều kiện có thể xử lý. Về cơ bản, VAR nhanh hơn khi suy luận ( ít hơn đi qua, tất cả đều song song trong một thang) và phù hợp hoặc vượt qua DiT trên ImageNet theo điều kiện lớp học. VAR theo điều kiện văn bản (VARclip, HART) là một hướng nghiên cứu tích cực.

> 它们是穿越问题的不同轴──两者都产生可处理的条件分布──实验上 VAR 推理更快(更少传播,尺度内全并行),在类别条件 ImageNet 上匹配或超越 DiT──文本条件 VAR 是活跃研究方向──

## Hãy xây dựng nó.
```figure
gx-var-next-scale
```

## Hãy xây dựng nó

Trong `code/main.py`bạn sẽ:
1. Hãy xây một cái nhỏ.**multi-scale VQ tokenizer**trên dữ liệu "hình ảnh" tổng hợp (2D vòng Gaussian).
2. Đào một **VAR-style transformer**để dự đoán các token quy mô tiếp theo.
3. Mô hình bằng cách gọi bộ biến đổi 4 lần (4 thang) và giải mã.
4. Kiểm tra rằng đào tạo theo quy mô sắp xếp tạo ra tương đồng trong quy mô.

Đây là một sự triển khai đồ chơi. Điểm là để thấy mặt nạ tập trung quy mô cấu trúc và thế hệ song song trong quy mô thực sự hoạt động.

> Đây là một công cụ thực hiện. Điểm nhấn là nhìn thấy sự tập trung của quy mô cấu trúc hóa ẩn chứa và quy mô trong cùng đường tạo ra công việc thực sự.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-var-tokenizer-designer.md` một kỹ năng thiết kế một tokenizer đa quy mô: số lượng quy mô, tỷ lệ quy mô, kích thước sổ mã, chia sẻ dư thừa, kiến trúc decoder.

> 本课产生 `outputs/skill-var-tokenizer-designer.md` Thiết kế nhiều kích thước tokenizer kỹ năng: kích thước số, tỷ lệ kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, kích thước, và độ độ, và độ độ độ cao, và độ cao, và độ cao, độ cao, độ cao, độ cao, và độ cao.

## Tập luyện bài tập

1. **Scale count ablation.**Đào tạo VAR với 4, 6, 8, 10 thang. đo chất lượng tái thiết so với số lượng các đường đi tự rút.

2. **Codebook size.**Đường bộ mã hóa với kích thước codebook 512, 4096, 16384.

3. **Parallel-within-scale check.**Đối với một VAR được đào tạo, đo mô hình chú ý một cách rõ ràng. Trong thang k, mô hình có quan tâm đến các vị trí qua thang nhưng không phải trong thang?

4. **VAR vs DiT scaling.**Đối với cùng một nhiệm vụ tùy thuộc vào lớp ImageNet, đào tạo VAR và DiT với ngân sách param phù hợp (ví dụ: 33M, 130M, 458M).

5. **Text conditioning.**Lũ rộng VAR để lấy một bản ghi văn bản (CLIP hợp nhất) như một đầu vào điều kiện thêm thông qua adaLN. Đây là công thức HART. FID cải thiện bao nhiêu trên lấy mẫu phù hợp với văn bản?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| VAR | "Visual AutoRegressive" | Image generation by next-scale prediction over a pyramid of VQ token grids |
| Next-scale prediction | "Predict coarser, then finer" | The model predicts tokens at increasing resolution scales, conditioning on all previous scales |
| Multi-scale VQ tokenizer | "Residual VQ" | VQ-VAE that produces K token grids of increasing resolution, with decoder summing all scales |
| Scale k | "Pyramid level k" | One of K resolution levels, from 1x1 at k=1 up to (H/p)x(W/p) at k=K |
| Parallel-within-scale | "One forward per scale" | All tokens at scale k are predicted in one transformer pass, not autoregressively |
| Causal-across-scales | "Scale-ordered attention" | Token at scale k can attend to all of scales 1..k but not scales k+1..K |
| Residual VQ | "Additive tokenization" | Each scale's tokens encode the residual left by lower scales; decoder sums all scale embeddings |
| VAR scaling law | "Image GPT scaling" | FID follows a predictable power law in compute, like language models' perplexity |
| HART | "Hybrid VAR + text" | Text-conditional VAR variant combining MaskGIT-style iterative decoding with VAR's scale structure |
| Scale position embedding | "(scale, row, col) triple" | Positional encoding carries both the scale index and spatial coordinates within the scale |

## Xem thêm 延伸阅读

- [Tian et al., 2024 — "Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction"](https://arxiv.org/abs/2404.02905) giấy VAR, tài liệu tham chiếu theo luật
- [Peebles and Xie, 2022 — "Scalable Diffusion Models with Transformers"](https://arxiv.org/abs/2212.09748) DiT, đường cơ sở so sánh phân tán
- [Esser et al., 2021 — "Taming Transformers for High-Resolution Image Synthesis"](https://arxiv.org/abs/2012.09841) VQGAN, gia đình tokenizer VAR của tokenizer đa quy mô mở rộng
- [van den Oord et al., 2017 — "Neural Discrete Representation Learning"](https://arxiv.org/abs/1711.00937) VQ-VAE, nền tảng của việc mã hóa hình ảnh riêng biệt
- [Tang et al., 2024 — "HART: Efficient Visual Generation with Hybrid Autoregressive Transformer"](https://arxiv.org/abs/2410.10812) VAR theo văn bản
