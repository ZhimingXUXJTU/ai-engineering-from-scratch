# GANs  Generator vs. Discriminator  GAN  Giao tạo và phân định

> Trù của Goodfellow năm 2014 là bỏ qua mật độ hoàn toàn. Hai mạng. Một tạo giả mạo. Một bắt chúng. Họ chiến đấu cho đến khi giả mạo không thể phân biệt với thực. Nó không nên hoạt động. Nó thường không hoạt động. Khi nó làm, các mẫu vẫn là sắc nét nhất trong văn học cho các miền hẹp.

> **【中文解读】**Goodfellow 2014 là một kỹ thuật hoàn toàn nhảy qua ước tính mật độ. Hai mạng: một giả mạo, một bắt kịp, lẫn nhau để phân biệt cho đến khi giả mạo và thực tế không thể phân biệt. Về lý thuyết không nên làm việc, thực tế thường không làm việc, nhưng một khi thành công, trong lĩnh vực hạn chế tạo vẫn là kết quả lợi ích nhất trong văn bản.

> **【拓展：GAN 的遗产】**StyleGAN (人脸生成)  CycleGAN (风格迁移) Pix2Pix (图像翻译) là ứng dụng cổ điển của GAN. Mặc dù mô hình phổ biến trở thành chủ yếu sau năm 2022, ý tưởng chống đào tạo của GAN vẫn được sử dụng để nâng cao chất lượng mô hình khác.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 08 (Optimizers / 优化器), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## Vấn đề  vấn đề giới thiệu

VAE sản xuất mẫu mờ vì mất mát của decoder MSE của họ là Bayes tối ưu cho hình ảnh * trung bình *  và trung bình của nhiều chữ số hợp lý là một chữ số mờ. Bạn muốn một lỗ hổng thưởng cho * khả thi *, không phải gần gũi với một mục tiêu nào đó. Không có hình thức đóng kín cho khả thi. Bạn phải học nó.

> VAE tạo ra một mẫu mờ, bởi vì MSE 解码器损失对*平均值*图像是贝叶斯最优的而许多合理数字的平均值是一个模糊的数字――你需要一个奖励*逼真度*的损失,而不是与任何目标的像素级接近――逼真度没有闭式解,你必须学习它――

Ý tưởng của Goodfellow: đào tạo một bộ phân loại.`D(x)`để phân biệt hình ảnh thực với hình ảnh giả.`G(z)`để làm trò lừa`D`. tín hiệu mất mát cho `G`là bất cứ điều gì `D`hiện đang nghĩ làm cho một cái gì đó trông thật.`G`Nếu cả hai mạng hội tụ,`G`đã học cách phân phối dữ liệu mà không bao giờ viết xuống `log p(x)`- Tôi không biết.

> Ý tưởng của Goodfellow: Train một phân loại `D(x)`区分真假图像,训练一个生成器 `G(z)`Để lừa dối`D``G`Đ signal mất mát là`D`Khi nghĩ "nhiều gì trông thật" thì tín hiệu này đi theo.`G` theo đuổi một mục tiêu di động. Nếu hai mạng đều được nhận,`G`Nó đã học được phân phối dữ liệu, không cần phải viết ra.`log p(x)`

Đây là huấn luyện đối kháng.

```
min_G max_D  E_real[log D(x)] + E_fake[log(1 - D(G(z)))]
```

Năm 2026, GAN không còn là máy phát điện SOTA (sự pha trộn và phù hợp dòng chảy ăn đống vương miện đó). Nhưng StyleGAN 2/3 vẫn là mô hình khuôn mặt sắc nét nhất từng được vận chuyển, các phân biệt đối xử GAN được sử dụng như là * mất mát nhận thức * trong đào tạo pha trộn, và đào tạo đối kháng cung cấp năng lực cho các loại chưng cất nhanh 1 bước (SDXL-Turbo, SD3-Turbo, LCM) cho phép bạn vận chuyển pha trộn thời gian thực.

> Năm 2026 GAN 不再是最先进的生成器 (扩散模型和流量匹配) 夺走了冠 (冠) ──但 StyleGAN 2/3 仍然是历史上最利的人脸模型,GAN 判定器被用于扩散训练中的*感觉损失*,对抗训练驱动快速的1步蒸(SDXL-Turbo、SD3-Turbo、LCM) ──

> **【中文解读】**GAN's core ideology:不建模密度,通过对抗训练学习生成──生成器 G(z) 尝试生成逼真图像,判别器 D(x) 尝试区分真假──两者在最小x 博中共同进化──VAE's MSE 损失导致模糊──因为它优化最是平均值图像),而GAN's对抗损失奖励"逼真度"──GAN 生成速度快,但训练不稳定──

> **【拓展：GAN 在扩散模型蒸馏中的新角色】**Mặc dù GAN không còn là phương pháp sản xuất chính thống, nhưng chống đào tạo tư tưởng trong mô hình phát triển hơi  phát triển mới. SDXL-Turbo, SD3-Turbo, LCM và các mô hình nhanh chóng sử dụng chống mất sẽ được nhiều bước phát triển hơi 1-4 bước, đạt được thực thời gian sản xuất.

## Khái niệm cốt lõi

![GAN training: generator and discriminator in minimax](../assets/gan.svg)

**Generator `G(z)`.**Bản đồ một vector tiếng `z ~ N(0, I)`cho một mẫu `x̂`Một mạng hình dạng decoder (cụ thể hoặc chuyển thể con).

> **生成器 `G(z)`。**   `z ~ N(0, I)`映射为样本 `x̂`△ Một mạng hình dạng mã hóa △ toàn kết nối hoặc chuyển đặt卷积) △

**Discriminator `D(x)`.**Bản đồ một mẫu đến một xác suất scalar (hoặc điểm số).

> **判别器 `D(x)`。**将样本映射为标量概率 (或分数) ⋅真实 → 1, giả tạo → 0⋅

**Loss.**Hai bản cập nhật thay thế:

- **Train `D`:** `loss_D = -[ log D(x) + log(1 - D(G(z))) ]`- Binary cross-entropy trên real=1, fake=0.
- **Train `G`:** `loss_G = -log D(G(z))`Đây là hình thức không bão hòa được Goodfellow sử dụng (tôi ban đầu)`log(1 - D(G(z)))`saturates và giết chết gradients khi `D`là tự tin).

> **损失。**两个交替更新:训练 D 用二元交叉(真实=1,伪造=0);训练 G 用非和形式 `-log D(G(z))`(từ đầu đã biến mất)

**Training loop.**Một bước đi của `D`, một bước đi của `G`- Lặp lại.

> **训练循环。**Một bước D, bước G, trao đổi tiến hành.

**Why it works.**Nếu`G`Đúng là phù hợp.`p_data`, sau đó `D`không thể làm tốt hơn so với tình cờ và kết quả là 0,5 ở khắp mọi nơi;`G`không còn gradient nữa.

> **为什么有效。**Nếu `G`完美匹配 `p_data`,则 `D`Không thể đoán được hơn, là 0.5.`G`Không còn được cấp độ nữa.

**Why it breaks.**Phong trào chế độ (`G`tìm thấy một chế độ `D`không thể phân loại và mint nó mãi mãi), biến mất gradient (`D`học quá nhanh và `log D`(tỷ lệ học tập, kích thước lô, bất cứ thứ gì).

> **为什么会失败。**模式塌(`G`找到 `D`无法分类一种模式并永远产生它) 梯度消失(`D`Học quá nhanh dẫn đến `log D`和) 、训练不稳定(学习率、批大小等)

## Những biến thể làm cho GAN hoạt động

| Year / 年份 | Innovation / 创新 | Fix / 解决的问题 |
|------|------------|-----|
| 2015 | DCGAN | Conv/deconv, batch norm, LeakyReLU — the first stable architecture. / 首个稳定架构。 |
| 2017 | WGAN, WGAN-GP | Replace BCE with Wasserstein distance + gradient penalty. Fixes vanishing gradient. / 用 Wasserstein 距离替换 BCE，修复梯度消失。 |
| 2017 | Spectral normalization | Lipschitz-bound the discriminator. Still used in 2026 discriminators. / 约束判别器 Lipschitz 常数。 |
| 2018 | Progressive GAN | Train low-res first, add layers. First megapixel results. / 先训练低分辨率，再加层。 |
| 2019 | StyleGAN / StyleGAN2 | Mapping network + adaptive instance norm. State of the art for fixed-domain photorealism. / 映射网络 + AdaIN。 |
| 2021 | StyleGAN3 | Alias-free, translation-equivariant — still the face gold standard in 2026. / 无混叠，平移等变。 |
| 2022 | StyleGAN-XL | Conditional, class-aware, larger scale. / 条件生成，类别感知。 |
| 2024 | R3GAN | Rebrands with stronger regularization; works on 1024² without tricks. / 更强的正则化。 |

## Hãy xây dựng nó.
```figure
gan-minimax
```

## Hãy xây dựng nó

`code/main.py`tạo ra một GAN nhỏ trên dữ liệu 1-D: một hỗn hợp của hai Gaussians. Generator và phân biệt là MLP một lớp ẩn. Chúng tôi thực hiện phía trước, ngược, và vòng minimax bằng tay. Mục tiêu là để xem hai chế độ thất bại chính (các trạng thái sụp đổ + độ sụp đổ) khi chúng xảy ra.

> `code/main.py`Trong một chiều dữ liệu, tập luyện một mô hình GAN nhỏ: 双峰高斯混合――生成器和判判器 là một mảng MLP đơn ẩn――我们手动实现前向、反向和最小x循环――目标是看到两种关键失败模式 (模式塌 + 梯度消失) 的发生过程――

### Bước 1: mất không bão hòa

Cái vanilla Goodfellow mất đi`log(1 - D(G(z)))`D phân loại giả của G là giả với độ tin cậy cao. Tại thời điểm đó gradient cho G về cơ bản là không  G không thể cải thiện.`-log D(G(z))`có asymptote ngược lại: nó nổ ra khi D tự tin, cho G một tín hiệu mạnh mẽ.

> Đời tốt  mất mát `log(1 - D(G(z)))`Trong D độ cao sẽ phân loại giả mạo của G trong thời gian gần 0, trong thời gian này độ của G trong cơ bản là 0.`-log D(G(z))`Có phản ứng gần gũi: Trong thời gian tự tin, hãy gửi tín hiệu mạnh mẽ đến G .

```python
def g_loss(d_fake):
    # maximize log D(G(z))  <=>  minimize -log D(G(z))
    return -sum(math.log(max(p, 1e-8)) for p in d_fake) / len(d_fake)
```

### Bước 2: một bước phân biệt đối xử cho mỗi bước máy phát

```python
for step in range(steps):
    # train D
    real_batch = sample_real(batch_size)
    fake_batch = [G(z) for z in sample_noise(batch_size)]
    update_D(real_batch, fake_batch)

    # train G
    fake_batch = [G(z) for z in sample_noise(batch_size)]  # fresh fakes
    update_G(fake_batch)
```

G mới giả, nếu không thì độ lệch sẽ không còn.

> G sinh ra một mẫu giả mới, nếu không thì quá thời gian.

### Bước 3: xem cho chế độ sụp đổ

```python
if step % 200 == 0:
    samples = [G(z) for z in sample_noise(500)]
    mode_a = sum(1 for s in samples if s < 0)
    mode_b = 500 - mode_a
    if min(mode_a, mode_b) < 50:
        print("  [!] mode collapse: one mode is starved")
```

Các triệu chứng của các phương pháp này là một trong hai chế độ thực sự ngừng được tạo ra.

> 典型症状: Một trong hai mô hình thực không còn được tạo ra nữa.

## # Thói bẫy #

- **Discriminator too strong.**Giảm tốc độ học tập của D 2-5x, hoặc thêm tiếng ồn trường hợp/phần. Nếu D đạt độ chính xác > 95%, G đã chết.
  **判别器太强。**Để giảm tỷ lệ học tập của D 2-5 lần, hoặc thêm trường hợp/phần tiếng ồn. Nếu tỷ lệ học tập của D vượt quá 95%, G sẽ chết.
- **Generator memorizes a mode.**Thêm tiếng ồn vào đầu vào D, sử dụng lớp phân biệt bộ mini-batch, hoặc chuyển sang WGAN-GP.
  **生成器记住了一种模式。**给 D 输入添加噪音, sử dụng lớp máy phân định khối lượng nhỏ, hoặc chuyển đổi sang WGAN-GP。
- **Batch norm leaking statistics.**Các lô thực + lô giả chảy qua cùng một lớp BN trộn lại số liệu thống kê của họ.
  **批归一化泄漏统计量。**Thực đơn và giả đơn đơn qua cùng một BN 层 hỗn hợp thống kê.
- **Inception-score gaming.**FID và IS có tiếng ồn ở số lượng mẫu thấp. Sử dụng ≥ 10k mẫu trong eval.
  **Inception Score 作弊。**FID 和 IS trong lượng mẫu thấp ồn lớn ∙ đánh giá sử dụng ≥ 10k 样本 ∙
- **One-shot sampling is a lie for conditional tasks.**Bạn vẫn cần cân CFG, thủ thuật cắt ngắn, và lấy lại mẫu để có được kết quả có thể sử dụng.
  **条件任务中"单次采样"是个谎言。**Bạn vẫn cần CFG 缩缩, cắt kỹ thuật và tái lấy mẫu để có được sản xuất có sẵn.

## Hãy sử dụng nó để thực hiện

GAN 2026:

> 2026 年 GAN 技术:

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Photoreal human faces, fixed pose / 照片级人脸，固定姿势 | StyleGAN3 (sharpest, smallest) |
| Anime / stylized faces / 动漫/风格化人脸 | StyleGAN-XL or Stable Diffusion LoRA |
| Image-to-image translation / 图像翻译 | Pix2Pix / CycleGAN (Phase 8 · 04) or ControlNet (Phase 8 · 08) |
| Fast 1-step text-to-image / 快速单步文生图 | Adversarial distillation of diffusion (SDXL-Turbo, SD3-Turbo) |
| Perceptual loss inside a diffusion trainer / 扩散训练中的感知损失 | Small GAN discriminator on image crops |
| Anything multi-modal, open-ended / 多模态开放域 | Don't — use diffusion or flow matching / 不要用 GAN——用扩散或 Flow Matching |

GAN là sắc nét nhưng hẹp. Một khi miền của bạn mở  ảnh, các lời nhắc văn bản tùy ý, video  chuyển sang phổ biến. Tránh chống lại tồn tại như một thành phần (khuyết cảm, chưng cất), không phải là một máy phát điện độc lập.

> GAN 利但狭域──一旦领域开放照片、任意文本提示、视频就就转换到扩散模型──对抗技巧作为组件存活(感知损失、蒸),而不是独立生成器──

## Chuyển nó đi.

- Cứu lại`outputs/skill-gan-debugger.md`. Skill lấy một lần chạy GAN thất bại (cập lỗ, lưới mẫu, kích thước tập dữ liệu) và đưa ra một danh sách xếp hạng các nguyên nhân có thể xảy ra, sửa chữa một dòng và một giao thức tái chạy.

> 保存 `outputs/skill-gan-debugger.md`◊Skill  nhận một GAN thất bại 运行(损失曲线、样本网格、数据集大小),输出可能原因排序列、一行修复和重跑方案──

## Tập luyện bài tập

1. **Easy / 简单.**Đi chạy`code/main.py`với các cài đặt cổ phiếu.`D_LR = 5 * G_LR`G mất mát của G sụp đổ nhanh như thế nào?
   用默认设置运行 `code/main.py` rồi đặt `D_LR = 5 * G_LR`Lãng trọng lượng của G mất nhiều gấp đôi?
2. **Medium / 中等.**Thay thế lỗ của Goodfellow BCE bằng lỗ của WGAN: `loss_D = E[D(fake)] - E[D(real)]`- `loss_G = -E[D(fake)]`, và clip D's trọng lượng để `[-0.01, 0.01]`- Trình luyện ổn định hơn không?
   Để thay đổi lỗ của Goodfellow BCE thành lỗ của WGAN, cắt giảm quyền trọng lượng của D`[-0.01, 0.01]`                                                                                                                                                                                                                                                              
3. **Hard / 困难.**Cải nghiệm các mô hình 1D cho các dữ liệu 2D (sự trộn lẫn của 8 Gaussians trên một vòng). Theo dõi bao nhiêu trong số 8 chế độ máy phát điện bắt được ở các bước 1k, 5k, 10k. Thực hiện phân biệt bộ phận nhỏ và đo lại.
   Để mở rộng mô hình 1D sang dữ liệu 2D ((环上 8个高斯混合)  Tracking generator đã bắt được nhiều mô hình trong 1k、5k、10k bước;; thực hiện phân tích và đo lại khối lượng nhỏ;;

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generator | "G" | Noise-to-sample network, `G: z → x̂`. / 噪声到样本的网络。 |
| Discriminator | "D" | Classifier `D: x → [0, 1]`, real vs fake. / 真假分类器。 |
| Minimax | "The game" / "博弈" | `min_G max_D` of a joint objective. / 联合目标的极小极大。 |
| Non-saturating loss | "The fix" / "修复" | Use `-log D(G(z))` for G instead of `log(1 - D(G(z)))`. / 用非饱和形式替代原始损失。 |
| Mode collapse | "G memorized one thing" / "G 记住了一种" | Generator produces few distinct outputs despite diverse data. / 生成器产生少量不同输出。 |
| WGAN | "Wasserstein" | Replace BCE with Earth-Mover distance + gradient penalty; smoother gradient. / 用 Wasserstein 距离替代 BCE。 |
| Spectral norm | "Lipschitz trick" / "Lipschitz 技巧" | Constrain D's weight norms to bound its slope; stabilizes training. / 约束 D 的权重范数以稳定训练。 |
| StyleGAN | "The one that works" / "能用的那个" | Mapping network + AdaIN; best-in-class for faces, still in 2026. / 映射网络 + AdaIN，人脸最佳。 |

## Lưu ý sản xuất: một lần suy luận là lợi thế lâu dài của GAN

GAN không còn giành chiến thắng trên chất lượng mẫu cho việc tạo ra miền mở, nhưng họ vẫn giành chiến thắng trên chi phí suy luận.

> GAN không còn thắng trên chất lượng mẫu được tạo ra trong khu vực mở, nhưng vẫn thắng trên chi phí suy luận.

- **No prefill, no decode stages.**Một người đơn `G(z)`TTFT ≈ thời gian trễ hoàn toàn.
  **无 prefill，无 decode 阶段。**单次 `G(z)`前向传播──TTFT ≈ 总延迟──
- **No KV-cache pressure.**Chỉ có trạng thái là trọng lượng, kích thước của lô được giới hạn bởi bộ nhớ kích hoạt, không phải bộ nhớ cache.
  **无 KV 缓存压力。**Tình trạng duy nhất là quyền trọng lượng.
- **Trivial continuous batching.**Vì mỗi yêu cầu có cùng FLOPs cố định, một lô tĩnh ở vị trí chiếm đóng mục tiêu của máy chủ thường là tối ưu. Không cần lập lịch trong chuyến bay.
  **简单的连续批处理。**Mỗi yêu cầu tiêu thụ FLOP tương tự, khối lượng tĩnh thường tốt nhất.

Đây là lý do tại sao việc chưng cất GAN (SDXL-Turbo, SD3-Turbo, ADD, LCM) là kỹ thuật thống trị cho văn bản nhanh chóng đến hình ảnh vào năm 2026: nó phá vỡ một đường ống dẫn phân phối 20-50 bước thành 1-4 đường chuyền về phía trước theo phong cách GAN trong khi giữ phân phối cơ sở phân phối.

> Đó là lý do tại sao GAN 蒸(SDXL-Turbo、SD3-Turbo、LCM) là công nghệ chủ đạo năm 2026: nó sẽ mở rộng 20-50 bước để nén dòng chảy 1-4 lần của GAN 风格, đồng thời duy trì phân phối mô hình mở rộng.

## Xem thêm 延伸阅读

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661) giấy GAN gốc.
- [Radford et al. (2015). Unsupervised Representation Learning with DCGAN](https://arxiv.org/abs/1511.06434) kiến trúc ổn định đầu tiên.
- [Arjovsky, Chintala, Bottou (2017). Wasserstein GAN](https://arxiv.org/abs/1701.07875) WGAN.
- [Miyato et al. (2018). Spectral Normalization for GANs](https://arxiv.org/abs/1802.05957) SN.
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958) StyleGAN2.
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423) StyleGAN3.
- [Sauer et al. (2023). Adversarial Diffusion Distillation](https://arxiv.org/abs/2311.17042) SDXL-Turbo.
