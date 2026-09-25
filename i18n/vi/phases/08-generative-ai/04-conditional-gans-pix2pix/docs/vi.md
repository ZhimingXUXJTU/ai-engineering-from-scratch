# GAN điều kiện & Pix2Pix  điều kiện GAN với Pix2Pix

> Sự mở khóa lớn đầu tiên của năm 2014-2017 là kiểm soát những gì một GAN tạo ra. Lên nhãn, hoặc hình ảnh, hoặc một câu. Pix2Pix đã làm phiên bản hình ảnh và nó vẫn đánh bại mọi mô hình văn bản chung-to-photos trong các nhiệm vụ hình ảnh-to-photos hẹp.

> **【中文解读】**Vụ đột phá lớn đầu tiên trong năm 2014-2017 là kiểm soát GAN 生成什么: phụ lục, hình ảnh hoặc văn bản. Pix2Pix đã thực hiện phiên bản hình ảnh, cho đến nay vẫn vượt qua các mô hình hình ảnh trong mô hình văn bản chung.

> **【拓展：Pix2Pix 的应用】**Pix2Pix đã mở ra mô hình "photos to images translation": vẽ vẽ→ ảnh、白天→夜晚、线稿→彩色图── mô hình này sau đó được ControlNet thừa kế và phát triển──

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 06 (U-Net), Phase 3 · 07 (CNNs / 卷积神经网络)
**Time:** ~75 minutes

## Vấn đề  vấn đề giới thiệu

Một mẫu GAN vô điều kiện lấy mẫu khuôn mặt tùy ý. hữu ích cho một bản demo, vô dụng trong sản xuất. Bạn muốn: *mở bản phác thảo sang một bức ảnh*, *mở bản đồ sang một bức ảnh trên không*, *mở cảnh ban ngày sang ban đêm*, *mở màu một hình ảnh quy mô xám*. Trong tất cả những hình ảnh này, bạn được cung cấp một hình ảnh nhập`x`và phải phát hành `y`Có nhiều điều đáng tin cậy.`y`S/m`x`Một thất bại đối thủ không làm, bởi vì "có vẻ thật" là sắc bén.

> 无条件 GAN 采样任意人脸──适合演示,不适合生产──你想要的是:*将素描映射为照片*、*将地图映射为航拍图*、*将白天映射为夜*、*给灰度图上色*──在所有这些场景中,给定输入图像`x`, phải xuất ra có ý nghĩa đối với các mối quan hệ .`y` Mỗi người `x`Có nhiều lý do hợp lý.`y`                                                                                                                                                                                                                                                              

GAN có điều kiện (Mirza & Osindero, 2014) thêm một điều kiện `c`như là một đầu vào cho cả hai `G`và `D`Pix2Pix (Isola et al., 2017) chuyên về điều này: điều kiện là một hình ảnh nhập đầy đủ, máy phát điện là một U-Net, phân biệt là một phân loại dựa trên các bản vá (PatchGAN), và mất mát là đối kháng + L1.

> 条件 GAN(2014) trong `G`和 `D`                                                                                                                                                                                                                                                              `c`◊Pix2Pix(2017) đã chuyên về điều này: điều kiện là nhập hình ảnh hoàn chỉnh, trình tạo là U-Net, phân định器 là PatchGAN, mất mát = đối kháng + L1♦.

> **【中文解读】**Điều kiện GAN cải tiến cốt lõi: cho máy phát và máy phân định đều thêm điều kiện nhập c c。XPix2Pix điều kiện là hình ảnh nhập hoàn chỉnh, máy phát U-Net (khả năng lưu trữ không gian chi tiết), máy phân định sử dụng PatchGAN (khả năng tạo hình ảnh) ⋅ mất = đối kháng mất + L1 ⋅ mất.

> **【拓展：从 Pix2Pix 到 ControlNet 的演进】**"Phản xuất hình ảnh" của Pix2Pix được tưởng tượng bởi ControlNet(2023) thừa kế và phát triển.ControlNet sẽ điều kiện kiểm soát ([[边缘]], độ sâu图、姿态等) vào mô hình Stable Diffusion 模型 dự kiến, đạt được việc tạo hình ảnh có thể kiểm soát phổ biến hơn. Từ Pix2Pix đến CycleGAN trở lại ControlNet, đây là một con đường phát triển kỹ thuật "phản xuất có thể kiểm soát" rõ ràng.

## Khái niệm cốt lõi

![Pix2Pix: U-Net generator, PatchGAN discriminator](../assets/pix2pix.svg)

**Conditional G.** `G(x, z) → y`Trong Pix2Pix,`z`là trượt trong G (không có tiếng ồn nhập  Isola tìm thấy tiếng ồn rõ ràng bị bỏ qua).

> **条件生成器 G。** `G(x, z) → y` Trong Pix2Pix,`z`là G 内部的落下 (无输入噪音) Isola 发现显式噪音会被忽视) 

**Conditional D.** `D(x, y) → [0, 1]`. Input là *pair* (cấp, đầu ra). Đây là sự khác biệt chính: D phải đánh giá liệu`y`phù hợp với `x`, không chỉ là`y`trông thật.

> **条件判别器 D。** `D(x, y) → [0, 1]`◊输入是*配对*(条件,输出) ・关键区别:D 必须判断 `y``x`Một致, không chỉ là `y`Có vẻ thật không?

**U-Net generator.**Mã hóa-kết giải có kết nối skip trên nút chai. Khí yết cho các nhiệm vụ mà đầu vào và đầu ra chia sẻ cấu trúc cấp thấp (về, hình xảo).

> **U-Net 生成器。**带有跳跃连接的编码器-解码器――对于输入输出共享低级结构的任务至关重要――没有跳跃连接,高频细节会消失――

**PatchGAN discriminator.**Thay vì đưa ra một điểm thực/sự giả, D đưa ra một `N×N`lưới mà mỗi tế bào đánh giá một lĩnh vực thụ thể của ~ 70 × 70 pixel. trung bình. Đây là một giả định trường ngẫu nhiên Markov: thực tế là địa phương.

> **PatchGAN 判别器。**D 输出 `N×N`网格而不是单一真/假分数, mỗi đơn vị đánh giá khoảng 70×70 像素的感受野──这是马尔可夫随机场假设:真实感是局部的──训练更快,参数更少,输出更利──

**Loss.**

```
loss_G = -log D(x, G(x)) + λ · ||y - G(x)||_1
loss_D = -log D(x, y) - log (1 - D(x, G(x)))
```

Thuật ngữ L1 ổn định đào tạo và đẩy G về phía mục tiêu được biết đến. L1 cung cấp cạnh sắc nét hơn L2 (tương đương, không phải là trung bình). `λ = 100`là Pix2Pix mặc định.

> L1 项稳定训练并推动 G 趋向已知目标──L1 比 L2 产生更利的边缘(中位数对平均值)──`λ = 100`Đó là giá trị mặc định của Pix2Pix.

## CycleGAN  khi bạn không có cặp đống  CycleGAN  没有配对数据时

Pix2Pix cần được ghép `(x, y)`Data. CycleGAN (Zhu et al., 2017) giảm yêu cầu này với chi phí của một tổn thất thêm: mất * chu kỳ nhất quán * hai máy phát `G: X → Y`và `F: Y → X`- Đọc cho họ làm thế này`F(G(x)) ≈ x`và `G(F(y)) ≈ y`Điều này cho phép bạn chuyển đổi ngựa thành ngựa, mùa hè sang mùa đông, mà không có những ví dụ.

> Pix2Pix  cần phải đối tác `(x, y)`Số liệu: CycleGAN (Tỷ lệ sinh hoạt của các máy tính) đã từ bỏ yêu cầu này, giá là mất tích hợp vòng lặp ngoại lệ.`G: X → Y`和 `F: Y → X`, tập luyện`F(G(x)) ≈ x`和 `G(F(y)) ≈ y`nghệng cho bạn không cần thiết để đối tác mô hình để có thể biến ngựa thành ngựa, mùa hè thành mùa đông

Năm 2026, không cặp hình ảnh-to-photos được thực hiện chủ yếu thông qua phân tán (ControlNet, IP-Adapter) thay vì CycleGAN, nhưng ý tưởng nhất quán chu kỳ tồn tại trong hầu hết các giấy thích ứng miền không cặp.

> Năm 2026, không có kết nối hình ảnh được dịch chuyển chủ yếu thông qua mô hình phổ biến (ControlNet、IP-Adapter) thay vì CycleGAN được hoàn thành, nhưng ý tưởng thống nhất vòng lặp hầu như tồn tại trong mỗi bài viết không có kết nối trong các bài viết thích ứng.

## Hãy xây dựng nó.
```figure
gx-patchgan
```

## Hãy xây dựng nó

`code/main.py`thực hiện một GAN điều kiện nhỏ trên dữ liệu 1D.`c`là một nhãn lớp (0 hoặc 1). Nhiệm vụ: tạo ra một mẫu từ phân phối có điều kiện cho lớp được đưa ra.

> `code/main.py`Trong một dimension dữ liệu thực hiện một điều kiện nhỏ GAN.`c`: : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : :

### Bước 1: thêm điều kiện cho cả hai đầu vào G và D

```python
def G(z, c, params):
    return mlp(concat([z, one_hot(c)]), params)

def D(x, c, params):
    return mlp(concat([x, one_hot(c)]), params)
```

Mã hóa một lần là cách đơn giản nhất. Các mô hình lớn hơn sử dụng nhúng học, mô-đun FiLM hoặc sự chú ý chéo.

> One-hot 编码 là cách đơn giản nhất.

### Bước 2: Đường xe có điều kiện

```python
for step in range(steps):
    x, c = sample_real_conditional()
    noise = sample_noise()
    update_D(x_real=x, x_fake=G(noise, c), c=c)
    update_G(noise, c)
```

Máy phát điện phải phù hợp với phân bố thực * cho điều kiện được đưa ra *, chứ không phải là biên.

> Các máy sinh sản phải phù hợp với phân bố thực sự trong các điều kiện nhất định, chứ không phải phân bố bên cạnh.

### Bước 3: xác minh đầu ra mỗi lớp

```python
for c in [0, 1]:
    samples = [G(noise, c) for noise in batch]
    mean_c = mean(samples)
    assert_near(mean_c, real_mean_for_class_c)
```

## # Thói bẫy #

- **Condition ignored.**G học cách bớt đi xa, D không bao giờ phạt vì tín hiệu điều kiện yếu.
  **条件被忽略。**G học tập đã bị phân lập, D từ không trừng phạt vì điều kiện tín hiệu yếu.
- **L1 weight too low.**G di chuyển đến các kết quả thực sự tùy ý, không phải là trung thành. Bắt đầu λ≈100 cho các nhiệm vụ kiểu Pix2Pix.
  **L1 权重太低。**G 偏移到任意看起来真实输出──Pix2Pix 任务从 λ≈100 开始──
- **L1 weight too high.**G tạo ra các kết quả mờ vì L1 vẫn là một chuẩn L_p.
  **L1 权重太高。**G 产生模糊输出──训练稳定后逐渐降低──
- **Ground-truth leakage in D.**Concatenate `(x, y)`như D đầu vào, không chỉ `y`Không có D này thì không thể kiểm tra sự phù hợp.
  **D 中的真值泄漏。**sẽ`(x, y)`拼接为 D 的输入,而非仅仅`y`
- **Mode collapse per class.**Mỗi lớp có thể sụp đổ một cách độc lập.
  **每类模式坍塌。**Mỗi loại có thể tự lập 塌──运行类别条件多样性检查──

## Hãy sử dụng nó để thực hiện

2026 trạng thái các nhiệm vụ hình ảnh-đối với hình ảnh:

> 2026 năm hình ảnh đến hình ảnh nhiệm vụ trạng thái:

| Task / 任务 | Best approach / 最佳方案 |
|------|---------------|
| Sketch → photo, same domain, paired data / 素描→照片，配对数据 | Pix2Pix / Pix2PixHD (still fast, still sharp) |
| Sketch → photo, unpaired / 素描→照片，非配对 | ControlNet with a Scribble conditioning model |
| Semantic seg → photo / 语义分割→照片 | SPADE / GauGAN2 or SD + ControlNet-Seg |
| Style transfer / 风格迁移 | Diffusion with IP-Adapter or LoRA; GAN methods are legacy |
| Depth → photo / 深度→照片 | ControlNet-Depth over Stable Diffusion |
| Super-resolution / 超分辨率 | Real-ESRGAN (GAN), ESRGAN-Plus, or SD-Upscale (diffusion) |
| Colorization / 上色 | ColTran, diffusion-based colorizers, or Pix2Pix-color |
| Daytime → nighttime, seasons, weather / 白天→夜晚 | CycleGAN or ControlNet-based |

Pix2Pix vẫn là công cụ phù hợp khi (a) bạn có hàng ngàn ví dụ cặp, (b) nhiệm vụ là hẹp và lặp lại, và (c) bạn cần suy luận nhanh.

> Pix2Pix trong tình huống sau đây vẫn là công cụ chính xác: a) Có hàng ngàn mẫu đối tác, b) Nhiệm vụ nhỏ và có thể lặp lại, c) cần nhanh chóng đưa ra các nhiệm vụ, mở rộng mô hình chiến thắng.

## Chuyển nó đi.

- Cứu lại`outputs/skill-img2img-chooser.md`. Skill lấy mô tả nhiệm vụ, tính sẵn có dữ liệu (cặp với không cặp, mẫu N) và ngân sách độ trễ/ chất lượng, sau đó đưa ra: phương pháp tiếp cận (Pix2Pix, CycleGAN, biến thể ControlNet, SDXL + IP-Adapter), yêu cầu dữ liệu đào tạo, chi phí suy luận và giao thức đánh giá (LPIPS, FID, cụ thể cho nhiệm vụ).

> 保存 `outputs/skill-img2img-chooser.md` Kỹ năng nhận nhiệm vụ mô tả, tính khả dụng dữ liệu và dự trù/khu lượng ngân sách, các kế hoạch phát hành, đào tạo nhu cầu dữ liệu, ước tính chi phí và thỏa thuận đánh giá.

## Tập luyện bài tập

1. **Easy / 简单.**Thay đổi `code/main.py`để thêm một lớp thứ ba. xác nhận G vẫn lập bản đồ tiếng ồn của mỗi lớp vào chế độ chính xác.
   修改 `code/main.py`添加第三类. 确认 G 仍将每个类噪音映射到正确的模式.
2. **Medium / 中等.**Thay thế L1 bằng một mất mát theo kiểu nhận thức trong thiết lập 1-D (ví dụ: một D đông lạnh nhỏ hoạt động như chất thu thập tính năng).
   Trong thiết lập 1D, sử dụng mất cảm giác thay thế L1... nó thay đổi điều kiện phân phối độ?
3. **Hard / 困难.**Chụp một CycleGAN trong cài đặt 1-D: hai phân phối, hai bộ phát điện, mất chu kỳ.
   Trong thiết lập 1D 勾画中CycleGAN:两个分布、两个生成器、循环损失――证明它无需配对数据就能学习映射――

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Conditional GAN | "GAN with labels" / "带标签的 GAN" | G(z, c), D(x, c). Both networks see the condition. / 两个网络都看到条件。 |
| Pix2Pix | "Image-to-image GAN" / "图像到图像 GAN" | Paired cGAN with U-Net G and PatchGAN D + L1 loss. / 配对 cGAN + U-Net + PatchGAN + L1。 |
| U-Net | "Encoder-decoder with skips" / "带跳跃的编解码器" | Symmetric conv network; skips preserve high-freq. / 对称卷积网络；跳跃连接保留高频。 |
| PatchGAN | "Local-realism classifier" / "局部真实分类器" | D outputs per-patch score instead of global score. / D 输出逐块分数。 |
| CycleGAN | "Unpaired image translation" / "非配对图像翻译" | Two G's + cycle-consistency loss; no paired data. / 两个 G + 循环一致性损失。 |
| SPADE | "GauGAN" | Normalizes intermediate activations with the semantic map; segmentation-to-image. / 用语义图归一化中间激活。 |
| FiLM | "Feature-wise linear modulation" / "特征级线性调制" | Per-feature affine transform from the condition; cheap conditioning. / 廉价的条件化方式。 |

## Lưu ý sản xuất: Pix2Pix như một đường cơ sở bị ràng buộc bởi độ trễ .

Khi bạn kết hợp dữ liệu và một nhiệm vụ hẹp (phác thảo → render, bản đồ ngữ nghĩa → ảnh, ban ngày → đêm), kết luận một lần của Pix2Pix đánh bại sự phân tán bằng một thứ tự về độ trễ.

> Khi bạn có một hệ thống dữ liệu và các nhiệm vụ phạm vi hạn chế, các suy luận đơn lẻ của Pix2Pix là chậm hơn mô hình phổ biến nhanh hơn một số lượng.

| Path / 方案 | Steps / 步数 | Typical latency at 512² on a single L4 / 典型延迟 |
|------|-------|----------------------------------------|
| Pix2Pix (U-Net forward) | 1 | ~30 ms |
| SD-Inpaint or SD-Img2Img | 20 | ~1.2 s |
| SDXL-Turbo Img2Img | 1-4 | ~0.15-0.35 s |
| ControlNet + SDXL base | 20-30 | ~3-5 s |

Pix2Pix thắng trên thông suất trong các lô tĩnh (mỗi yêu cầu đều là FLOPs tương tự). Diffusion thắng trên chất lượng và tổng quát.

> Pix2Pix trong trạng thái khối lượng dung lượng trên chiến thắng;; mỗi yêu cầu FLOPs tương tự);; mô hình phổ biến trong chất lượng và phổ biến trên chiến thắng;;

## Xem thêm 延伸阅读

- [Mirza & Osindero (2014). Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784) giấy cGAN.
- [Isola et al. (2017). Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/abs/1611.07004) Pix2Pix.
- [Zhu et al. (2017). Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks](https://arxiv.org/abs/1703.10593) CycleGAN.
- [Wang et al. (2018). High-Resolution Image Synthesis with Conditional GANs](https://arxiv.org/abs/1711.11585) Pix2PixHD.
- [Park et al. (2019). Semantic Image Synthesis with Spatially-Adaptive Normalization](https://arxiv.org/abs/1903.07291) SPADE / GauGAN.
- [Miyato & Koyama (2018). cGANs with Projection Discriminator](https://arxiv.org/abs/1802.05637) chiếu D.
