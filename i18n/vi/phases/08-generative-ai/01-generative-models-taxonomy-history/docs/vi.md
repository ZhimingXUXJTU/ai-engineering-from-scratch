# Mô hình tạo ra  Thuế học & Lịch sử  生成模型  分类与历史

> Mỗi mô hình hình ảnh, mô hình văn bản, mô hình video và mô hình 3D đều phù hợp với một trong năm cái thùng. Chọn cái thùng sai và bạn sẽ chiến đấu với toán học trong nhiều tuần. Chọn cái đúng và 12 năm tiến bộ của lĩnh vực này được xếp vào đầu bạn.

> **【中文解读】**Tất cả hình ảnh, văn bản, video và mô hình sản xuất 3D có thể được phân loại thành 5 loại: VAE、GAN、 mở rộng mô hình, dòng mô hình và mô hình tự quay lại.

> **【拓展：生成式 AI 的五大路线】**(1) VAE变分自编码器,Stable Diffusion的编码器;(2) GAN生成对抗网络,StyleGAN的核心;(3) 扩散模型DDPM/DDIM,当前图像生成主流;(4) 流模型Flow Matching,SD3/FLUX的新方向;(5) 自归GPT 模式,VAR 应用于图像──

**Type:** Learn / 学习型
**Languages:** Python
**Prerequisites:** Phase 2 (ML Fundamentals / 机器学习基础), Phase 3 (Deep Learning Core / 深度学习核心), Phase 7 · 14 (Transformers / Transformer)
**Time:** ~45 minutes

## Vấn đề  vấn đề giới thiệu

Một mô hình tạo ra làm một công việc: lấy mẫu đào tạo từ một số phân phối không rõ `p_data(x)`, xuất hiện các mẫu mới trông giống như chúng đến từ cùng một phân phối. khuôn mặt, câu, tệp MIDI, cấu trúc protein  tất cả đều là vấn đề tương tự nếu bạn nháy mắt.

> Một mô hình chỉ làm một điều: được định từ một phân bố không rõ`p_data(x)`Trong mô hình tập luyện được rút ra, xuất hiện trông giống như từ mô hình mới phân bố giống nhau.

Cái quái vật là thế.`p_data`sống trong một không gian có hàng triệu chiều kích (một hình ảnh RGB 512x512 là ~ 786k chiều kích), các mẫu nằm trên một bộ sợi mỏng bên trong không gian đó, và bạn chỉ có có thể 10M ví dụ.

>  vấn đề là`p_data`Một hình ảnh RGB 512x512 có khoảng 78,60.000 kích thước), mẫu chỉ chiếm một hình dạng mỏng trong không gian đó, trong khi bạn có thể chỉ có một triệu mẫu.

Năm gia đình đã sống sót trong mười hai năm qua.

> Trong 12 năm qua, 5 trong số 5 gia đình mô hình đã tồn tại. Để hiểu được những gì mỗi gia đình đã thỏa hiệp, bạn sẽ biết tại sao nó đã thành công trong một số nhiệm vụ và sụp đổ trong những nhiệm vụ khác.

> **【中文解读】**Nhiệm vụ cốt lõi của mô hình sinh: học từ mô hình đào tạo phân bố không rõ p_data(x), sau đó tạo ra trông từ mô hình mới phân bố giống nhau. 挑战 nằm trong không gian cao.  512x512 图像约786K 维) 图像中的稀疏数据.

> **【拓展：从扩散模型到 Flow Matching 的范式转移】**Xu hướng quan trọng nhất trong năm 2024-2026 là chuyển đổi từ mô hình phổ biến (DDPM) sang Flow Matching (Flow Matching) .

## Khái niệm cốt lõi

![Five families of generative models — taxonomy by what they model](../assets/taxonomy.svg)

**1. Explicit density, tractable.**Hãy viết`log p(x)`mô hình tự động (PixelCNN, WaveNet, GPT) tính toán`p(x) = ∏ p(x_i | x_<i)`. Tạo ra dòng chảy bình thường (RealNVP, Glow)`p(x)`Pro: xác suất chính xác, mất tập luyện sạch. Con: suy luận tự giảm là theo trình tự (nước chậm cho các chuỗi dài), dòng chảy cần kiến trúc đảo ngược (chỉ hạn chế về kiến trúc).

> **1. 显式密度，可处理。**sẽ`log p(x)`写成可以实际求值的求和──自归归模型(PixelCNN、WaveNet、GPT) sẽ được phân phối hợp chia thành condicion分布的乘积──标准化流(RealNVP、Glow) thông qua đơn giản phân phối của có thể đảo ngược thay đổi cấu trúc`p(x)`△优点:精确似然,训练损失清晰──缺点:自归推理是顺序的(长序列慢),流需要可逆架构(架构受限)。

**2. Explicit density, approximate.**Bị buộc `log p(x)`từ dưới (ELBO) và tối ưu hóa đường biên. VAE (Kingma 2013) sử dụng một bộ mã hóa-chế vị có một hậu biến. Các mô hình phân tán (DDPM, Ho 2020) đào tạo một mô hình biểu thị tối ưu hóa một ELBO cân nặng.

> **2. 显式密度，近似。**Từ bên dưới `log p(x)`(ELBO)并优化该下界──VAE 使用编码器-解码器和变分后验──扩散模型训练去噪器,隐式优化加权 ELBO──扩散模型是2026年图像、视频和3D 的主导骨干──

**3. Implicit density.**Trượt độ mật độ hoàn toàn; học máy phát điện `G(z)`sản xuất mẫu và phân biệt đối xử `D(x)`GAN (Goodfellow 2014). Nhanh chóng suy luận (một vượt qua phía trước) nhưng không ổn định trong quá trình đào tạo. StyleGAN 1/2/3 vẫn là hiện đại cho quang học miền cố định (người, phòng ngủ) ngay cả trong năm 2026.

> **3. 隐式密度。** hoàn toàn nhảy qua độ đậm định; học một máy tạo `G(z)`产生样本,一个判辨器 `D(x)`区分真假──GAN 推理快(单次前向传播), nhưng đào tạo极不稳定──StyleGAN 1/2/3 thậm chí còn là mô hình tiên tiến nhất của thực tế cấp độ ảnh trong lĩnh vực cố định năm 2026──

**4. Score-based / continuous-time.**Tìm hiểu gradient của khối lượng gỗ `∇_x log p(x)`Song & Ermon (2019) cho thấy kết quả kết hợp tổng hợp phân phối đến SDE. Kết hợp dòng chảy (Lipman 2023) là độ nóng 2024-2026: đào tạo không mô phỏng, các con đường thẳng hơn, lấy mẫu nhanh hơn DDPM 4-10 lần. Stable Diffusion 3, Flux, AudioCraft 2 tất cả sử dụng kết hợp dòng chảy.

> **4. 基于分数/连续时间。**直接学习对数密度的梯度(分数函数) ――Song & Ermon (2019) 证明分数匹配将扩散推广到SDE──Flow Matching(2023) là một trong những khóa học năm 2024-2026:

> **【中文解读】**分数匹配和流量匹配 là sự biến đổi và cải tiến của mô hình phổ biến. 分数匹配 trực tiếp học log 密度的梯度 (分数函数),Flow Matching tiếp tục đơn giản hóa quá trình đào tạo.

**5. Token-based autoregressive over discrete codes.**Cấp dữ liệu độ sâu cao bằng VQ-VAE hoặc lượng tử dư thành một chuỗi nhỏ các token riêng biệt, sau đó sử dụng một Transformer để mô hình hóa chuỗi token. Parti, MuseNet, AudioLM, VALL-E, token patch của Sora đều sử dụng điều này. Đây là bucket 1 cộng với một token học.

> **5. 基于离散 token 的自回归。**Sử dụng VQ-VAE hoặc残差量化器 sẽ nén dữ liệu cao để chuỗi ngắn của token phân tán, sau đó sử dụng Transformer 建模 token 序列──Parti、MuseNet、AudioLM、VALL-E、Sora của patch tokeniser đều sử dụng cách này── đây là loại đầu tiên cộng với một tokenized được học được──

## Một lịch sử ngắn.

| Year / 年份 | Model / 模型 | Why it mattered / 重要意义 |
|------|-------|-----------------|
| 2013 | VAE (Kingma) | First deep generative model with a usable training loss. / 首个具有可用训练损失的深度生成模型。 |
| 2014 | GAN (Goodfellow) | Implicit density, no likelihood — shockingly sharp samples. / 隐式密度，无需似然——惊人的锐利样本。 |
| 2015 | DRAW, PixelCNN | Sequential image generation. / 顺序图像生成。 |
| 2017 | Glow, RealNVP | Invertible flows; exact likelihood with depth. / 可逆流；深度带来精确似然。 |
| 2017 | Progressive GAN | First megapixel faces. / 首个百万像素人脸。 |
| 2019 | StyleGAN / StyleGAN2 | Photorealistic faces still hard to beat for that one domain. / 照片级真实人脸，该领域至今难以超越。 |
| 2020 | DDPM (Ho) | Diffusion becomes practical. / 扩散模型变得实用。 |
| 2021 | CLIP, DALL-E 1, VQGAN | Text-to-image goes mainstream. / 文本生成图像走向主流。 |
| 2022 | Imagen, Stable Diffusion 1, DALL-E 2 | Latent diffusion + text conditioning = commodity. / 潜在扩散 + 文本条件 = 大众化。 |
| 2022 | ControlNet, LoRA | Fine control over pretrained diffusion. / 对预训练扩散模型的精细控制。 |
| 2023 | SDXL, Midjourney v5, Flow matching | Scale + better training dynamics. / 规模化 + 更好的训练动态。 |
| 2024 | Sora, Stable Diffusion 3, Flux.1 | Video diffusion; flow matching wins. / 视频扩散；Flow Matching 胜出。 |
| 2025 | Veo 2, Kling 1.5, Runway Gen-3, Nano Banana | Production-grade video. / 生产级视频。 |
| 2026 | Consistency + Rectified Flow | One-step sampling from diffusion backbones. / 从扩散骨干实现单步采样。 |

## Phân tích 5 câu hỏi.

Khi một mẫu giấy tạo ra mới rơi xuống, hãy trả lời năm câu hỏi này trước khi đọc phần phương pháp.

> Khi một bài viết mô hình tạo mới được công bố, trước khi đọc phần phương pháp hãy trả lời năm câu hỏi này.

1. **What is being modeled?**Pixel, laten, token riêng biệt, Gaussians 3D, lưới, hình dạng sóng?
   **正在建模什么？**像素、潜在表示、离散代币、3D 高斯、网格、波形?
2. **Is the density explicit or implicit?**Họ ghi lại `log p(x)`- Không .
   **密度是显式还是隐式的？**Họ có viết ra không?`log p(x)`- Không .
3. **Sampling: one-shot or iterative?**Iterative có nghĩa là suy luận chậm hơn; một lần bắn thường có nghĩa là đối kháng hoặc chưng cất.
   **采样：单次还是迭代？**代 có nghĩa là suy nghĩ chậm hơn; đơn次 thường có nghĩa là đối kháng hoặc hơi hơn.
4. **Conditioning: unconditional, class, text, image, pose?**Điều này xác định sự mất mát và kiến trúc bàn phẳng.
   **条件：无条件、类别、文本、图像、姿态？**Điều này quyết định hàm mất và cấu trúc khung.
5. **Evaluation: FID, CLIP score, IS, human preference, task accuracy?**Mỗi người đều có những chế độ thất bại (xem Bài học 14).
   **评估：FID、CLIP Score、IS、人类偏好、任务准确率？**Mỗi người đều có một mô hình thất bại đã biết (xem Chương 14)

Bạn sẽ trả lời lại 5 câu này cho mỗi bài học trong giai đoạn này.

> Bạn sẽ trả lời lại 5 câu hỏi này trong mỗi bài học của giai đoạn này. Cuối cùng, chúng sẽ trở thành trực giác của bạn.

> **【中文解读】**Những năm vấn đề này (để phân tích các mô hình tạo ra các mô hình) là một khuôn khổ chung của bất kỳ mô hình nào.

## Hãy xây dựng nó.
```figure
autoencoder-bottleneck
```

## Hãy xây dựng nó

Mã cho bài học này là một hình ảnh nhẹ: phù hợp với một hỗn hợp Gaussans 1-D từ các mẫu bằng cách sử dụng ba phương pháp chơi game (thấp độ hạt nhân, histogram phân biệt, và một máy phát điện "GAN-ish" mẫu gần nhất) để bạn có thể thấy sự khác biệt giữa mật độ rõ ràng vs âm tính trên một vấn đề bạn có thể in trên một màn hình.

> Mã trong bài này là một hình ảnh có thể nhìn thấy một cách nhẹ: sử dụng ba phương pháp đơn giản:

Đi chạy`code/main.py`Nó lấy 2000 mẫu từ một hỗn hợp Gaussian hai chế độ, sau đó in:

> 运行 `code/main.py`Nó lấy từ 2 đỉnh cao trong hỗn hợp 2000 mẫu, rồi in:

```
explicit density (histogram): p(x in [-0.5, 0.5]) ≈ 0.38
approximate density (KDE):     p(x in [-0.5, 0.5]) ≈ 0.41
implicit (nearest-sample gen): 20 new samples printed, no p(x)
```

Lưu ý: hai câu đầu tiên cho phép bạn hỏi "điều này có khả năng như thế nào?" thứ ba không thể. Đây là sự phân biệt * rõ ràng và ngầm * sẽ quan trọng cho mọi bài học trong tương lai.

> Lưu ý: hai phương pháp trước có thể trả lời "điều này có nhiều khả năng cao không?"

## Hãy sử dụng nó để thực hiện

Gia đình nào, nhiệm vụ nào, vào năm 2026?

> Năm 2026, gia đình nào phù hợp với nhiệm vụ nào?

| Task / 任务 | Best family / 最佳家族 | Why / 原因 |
|------|-------------|-----|
| Photoreal faces, narrow domain / 照片级人脸，窄域 | StyleGAN 2/3 | Still sharpest, fastest inference. / 仍然最锐利，推理最快。 |
| General text-to-image / 通用文本生成图像 | Latent diffusion + flow matching | SD3, Flux.1, DALL-E 3. |
| Fast text-to-image / 快速文本生成图像 | Rectified flow + distillation | SDXL-Turbo, SD3-Turbo, LCM. |
| Text-to-video / 文本生成视频 | Diffusion Transformer + flow matching | Sora, Veo 2, Kling. |
| Speech + music / 语音+音乐 | Token-based AR (AudioLM, VALL-E, MusicGen) or flow matching (AudioCraft 2) | Discrete tokens scale cheaply. / 离散 token 扩展成本低。 |
| 3D scenes / 3D 场景 | Gaussian Splatting fit, diffusion prior | 3D-GS for reconstruction, diffusion for novel-view. / 3D-GS 用于重建，扩散用于新视角。 |
| Density estimation (no sampling) / 密度估计（不采样） | Flows | Only family with exact `log p(x)`. / 唯一有精确 `log p(x)` 的家族。 |
| Simulation / physics / 模拟/物理 | Flow matching, score SDE | Straight-line paths, smooth vector fields. / 直线路径，平滑向量场。 |

## Chuyển nó đi.

Cứ như `outputs/skill-model-chooser.md`- Tôi không biết.

> 保存为 `outputs/skill-model-chooser.md`

Kỹ năng này có một mô tả nhiệm vụ và kết quả: (1) gia đình nào để sử dụng, (2) một danh sách xếp hạng của ba tùy chọn mở và ba lưu trữ, (3) chế độ thất bại có thể bạn nên xem xét, và (4) một ngân sách tính toán / thời gian.

> Các kỹ năng  nhận nhiệm vụ mô tả,输出: 1) 应 sử dụng哪个家族, 2) 三个开源和三个托管选项的排列列表, 3) 应注意的可能失效模式, 4) 计算/时间预算.

## Tập luyện bài tập

1. **Easy / 简单.**Đối với mỗi năm sản phẩm này, xác định gia đình và xương sống: hình ảnh ChatGPT, Midjourney v7, Sora, Runway Gen-3, ElevenLabs. Bằng chứng nên là từ các báo cáo kỹ thuật công khai.
   Đối với 5 sản phẩm này, IDHÊNHÊN HÀN HÀN HÀN: CHATGPT hình ảnh, MIDJURNEY v7 索拉, Runway Gen-3 ElevenLabs 证据应来自公开技术报告.
2. **Medium / 中等.**Bài báo bạn sắp đọc ngày mai tuyên bố lấy mẫu nhanh hơn 100 lần so với việc phân tán.
   Bạn ngày mai cần đọc bài báo tuyên bố tăng gấp 100 lần mẫu. Viết ra ba câu hỏi để kiểm tra liệu tăng tốc có còn tồn tại trong điều kiện sản xuất và độ phân giải cao không.
3. **Hard / 困难.**Hãy lấy một lĩnh vực bạn quan tâm (ví dụ: cấu trúc protein, CAD, phân tử, quỹ đạo). trả lời phân loại năm câu hỏi cho mô hình SOTA hiện tại trong lĩnh vực đó và phác thảo những gì mô hình tốt hơn sẽ thay đổi.
   选择一个你关心的领域 (如蛋白质结构,CAD,分子轨迹) ⋅ đối với lĩnh vực này hiện tại SOTA 模型回答五问分类法,并勾绘更好的模型会改变什么──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generative model | "It makes new stuff" / "它生成新东西" | Learns a sampler for `p_data(x)`, optionally exposes `log p(x)`. / 学习 `p_data(x)` 的采样器，可选暴露 `log p(x)`。 |
| Explicit density | "You can evaluate it" / "可以计算" | Model provides a closed-form or tractable `log p(x)`. / 模型提供闭式或可处理的 `log p(x)`。 |
| Implicit density | "GAN-style" / "GAN 风格" | Only a sampler — no way to evaluate `p(x)` of a given point. / 只有采样器——无法计算给定点的 `p(x)`。 |
| ELBO | "Evidence lower bound" / "证据下界" | A tractable lower bound on `log p(x)`; VAEs and diffusion optimize it. / `log p(x)` 的可处理下界；VAE 和扩散模型优化它。 |
| Score | "Gradient of log-density" / "对数密度梯度" | `∇_x log p(x)`; diffusion and SDE models learn this field. / 扩散和 SDE 模型学习这个场。 |
| Manifold hypothesis | "Data lives on a surface" / "数据在曲面上" | High-dim data concentrates on a low-dim manifold; why dimensionality reduction works. / 高维数据集中在低维流形上；降维有效的原因。 |
| Autoregressive | "Predict the next piece" / "预测下一个" | Factorize joint as product of conditionals. / 将联合分布分解为条件分布的乘积。 |
| Latent | "Compressed code" / "压缩编码" | Low-dim representation from which a decoder can reconstruct the input. / 解码器可从中重建输入的低维表示。 |

## Lưu ý sản xuất: 5 gia đình, 5 hình dạng suy luận

Mỗi gia đình lập bản đồ đến một đường cong chi phí inference-server khác nhau. Văn học sản xuất-inference khung inference LLM như prefill + decode; phân hủy tương tự áp dụng ở đây:

> Mỗi gia đình đối phó với các suy luận khác nhau về chi phí dịch vụ.

- **Autoregressive (bucket 1 and 5).**Việc giải mã theo trình tự thống trị thời gian trễ; KV-cache, batching liên tục và giải mã suy đoán đều áp dụng trực tiếp.
  **自回归（第 1 和 5 类）。**顺序解码主导延迟;KV 缓存、连续批处理和推测解码直接适用──
- **VAE / diffusion / flow-matching (buckets 2 and 4).**Không có mã hóa trong ý nghĩa LLM.`num_steps × step_cost`, và `step_cost`là một biến thể hoặc U-Net phía trước với độ phân giải ẩn tình đầy đủ.
  **VAE / 扩散 / Flow Matching（第 2 和 4 类）。**LLM 意义上没有解码──成本 = `num_steps × step_cost`, sản xuất điều chỉnh vòng tròn là số bước, lượng lớn và độ chính xác.
- **GAN (bucket 3).**Một lần đi trước, không có lịch trình, không có cache KV, TTFT ≈ thời gian trễ hoàn toàn, đó là lý do tại sao StyleGAN vẫn thắng trong UX miền hẹp.
  **GAN（第 3 类）。**单次前向传播──没有调度,没有 KV 缓存──TTFT ≈ 总延迟──这就是StayGAN 在狭域UX上仍然胜出的原因──

Khi bạn thấy "quá hơn sự lan rộng" trong bản tóm tắt trên giấy, hãy dịch nó thành " ít bước x cùng chi phí bước" hoặc "những bước x chi phí bước rẻ hơn". Mọi thứ khác là tiếp thị.

> Khi bài luận trích dẫn trong nói "Bí hơn phổ biến nhanh hơn" thì, dịch thành "Làm ít hơn bước số × tương đồng chi phí" hoặc "Làm tương tự bước số × rẻ hơn chi phí bước"── còn lại là tiếp thị──

## Xem thêm 延伸阅读

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661) giấy GAN.
- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) tờ VAE.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) Báo cáo DDPM.
- [Song et al. (2021). Score-Based Generative Modeling through SDEs](https://arxiv.org/abs/2011.13456) phân tán như một SDE.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) giấy phù hợp với dòng chảy.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) Sự pha trộn ổn định 3.
