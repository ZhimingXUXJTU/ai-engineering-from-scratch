# StyleGAN  StyleGAN  风格 tạo ra chống lại mạng

> Hầu hết các máy phát điện đều làm động`z`StyleGAN chia nó ra: bản đồ đầu tiên`z`cho một trung gian `w`, sau đó * tiêm * `w`Sự thay đổi duy nhất đó đã giải quyết không gian ẩn và làm cho những khuôn mặt chân thực ảnh trở thành một vấn đề được giải quyết trong bảy năm liên tiếp.

> **【中文解读】**StyleGAN sẽ ẩn biến z trước khi được chiếu vào không gian trung gian w, tái thông qua AdaIN trong mỗi cấp độ phân giải được tiêm vào w, đạt được sự kiểm soát độc lập về việc tạo ra hình ảnh ở các cấp độ khác nhau (khác hạt/khác hạt) ⋅ Sự thay đổi này đã mở ra không gian ẩn, khiến việc tạo ra khuôn mặt thực sự trở thành vấn đề đã được giải quyết trong 7 năm.

> **【拓展：StyleGAN 的应用】**StyleGAN 广泛 được sử dụng để tạo khuôn mặt người (thispersondoesnotexist.com) 、虚拟人物创建、艺术创作──其风格混合技术可以混合不同人的脸的粗细特征──

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 08 (Normalization / 归一化), Phase 3 · 07 (CNNs)
**Time:** ~45 minutes

## Vấn đề  vấn đề giới thiệu

Một bản đồ DCGAN `z`để hình ảnh thông qua một loạt các biến chuyển chuyển. Vấn đề:`z`điều khiển mọi thứ  tư thế, ánh sáng, danh tính, nền  dính dáng với nhau.`z`Bạn không thể hỏi mô hình "một người, tư thế khác nhau" bởi vì đại diện không tính đến cách đó.

> DCGAN  thông qua chuyển nhượng`z`映射为图像── vấn đề là:`z`控制一切姿态、光照、身份、背景纠在一起──沿着`z`Một trục chuyển động, bốn đều biến đổi. Bạn không thể yêu cầu mô hình "một người, một姿态 khác nhau", vì biểu hiện không phân giải như vậy.

Karras et al. (2019, NVIDIA) đề xuất: ngừng ăn `z`trực tiếp vào các lớp chứa.`4×4×512`Tensor như đầu vào mạng. Học một MLP 8 lớp mà bản đồ `z ∈ Z → w ∈ W`. Tiêm `w`ở mỗi độ phân giải thông qua * Adaptive Instant Normalization* (AdaIN): bình thường hóa mỗi bản đồ tính năng conv, sau đó quy mô và chuyển đổi bằng các dự đoán tương tự của `w`Thêm tiếng ồn mỗi lớp để chi tiết stochastic (các lỗ da, sợi tóc).

> Karras 等人(2019,NVIDIA) đề xuất: dừng sẽ `z`Đưa trực tiếp vào lớp.`4×4×512`张量作为网络输入──学习一个8层 MLP将 `z ∈ Z → w ∈ W`◊ Thông qua * tự thích ứng thí dụ归一化*(AdaIN) trong mỗi phân giải`w`❖ Tinye mỗi lớp âm thanh được sử dụng theo từng bước.

Kết quả là:`W`có các trục gần như thẳng thắn cho " phong cách cấp cao " (phong, danh tính) vs " phong cách tốt " (của ánh sáng, màu sắc). Bạn có thể trao đổi phong cách giữa hai hình ảnh bằng cách sử dụng hình ảnh A `w`cho các mức độ độ phân giải thấp và hình ảnh B `w`Việc chỉnh sửa mở, phong cách hóa các lĩnh vực và toàn bộ nghiên cứu về "StyleGAN-inversion".

> Kết quả:`W`空间对"高级风格" (姿态,身份) 和"精细风格" (光照,颜色) có một xoắn ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối ối `w`Sử dụng độ phân giải thấp, hình ảnh B của`w`Sử dụng ở cấp độ phân giải cao để trao đổi phong cách.

> **【中文解读】**Ký năng mới của StyleGAN: 1) 映射网络 z→w 解开纠的隐空间; 2) AdaIN trong mỗi phân giải cấp độ độ 低分辨率层控制粗粒度(姿势、身份), cao độ phân giải cấp kiểm soát细粒度(颜色、纹理); 3) Mỗi cấp随机噪音添加细节(毛孔、发丝) ――Style Mixing 技术可以混合不同图像的粗细特征──

> **【拓展：StyleGAN 3 的平移等变性】**StyleGAN 2 sinh ra hình ảnh có "tơ xích" vấn đề đặc điểm (tương tự như đầu发) sẽ "xích" ở vị trí hình ảnh cụ thể chứ không phải bề mặt vật thể.

## Khái niệm cốt lõi

![StyleGAN: mapping network + AdaIN + per-layer noise](../assets/stylegan.svg)

**Mapping network.** `f: Z → W`, một MLP 8 lớp. `Z = N(0, I)^512`- `W`không bị buộc phải là Gaussian  nó học một hình dạng thích nghi với dữ liệu.

> **映射网络。** `f: Z → W`,8 tầng MLP`W`Không bị buộc phải học tập để thích ứng với hình dạng của nó.

**Synthesis network.**Bắt đầu từ một định vị học hỏi`4×4×512`. Mỗi khối phân giải: `upsample → conv → AdaIN(w_i) → noise → conv → AdaIN(w_i) → noise`- Nghị quyết hai lần: 4, 8, 16, 32, 64, 128, 256, 512, 1024.

> **合成网络。**Từ học tập đến số thường xuyên`4×4×512`开始──每个分辨率块:上采样→卷积→AdaIN→噪音→卷积→AdaIN→噪声──分辨率翻倍:4 到1024──

**AdaIN.**

```
AdaIN(x, y) = y_scale · (x - mean(x)) / std(x) + y_bias
```

nơi `y_scale`và `y_bias`đến từ các dự đoán tương tự của `w`. bình thường hóa theo bản đồ tính năng, sau đó tái tạo. "Style" ở đây là số liệu thống kê thứ nhất và thứ hai của bản đồ tính năng.

> Trong số đó `y_scale`和 `y_bias`Từ`w`Ưu điểm của mô hình hình: 1 và 2

**Per-layer noise.**Giọng nói Gaussian kênh duy nhất được thêm vào mỗi bản đồ tính năng, được quy mô bằng một yếu tố mỗi kênh được học.

> **每层噪声。**                                                                                                                                                                                                                                                              

**Truncation trick.**Khi suy luận, mẫu `z`, tính toán`w = mapping(z)`, sau đó `w' = ŵ + ψ·(w - ŵ)`nơi `ŵ`là trung bình`w`trên nhiều mẫu. `ψ < 1`gần như mọi bản demo của StyleGAN đều sử dụng`ψ ≈ 0.7`- Tôi không biết.

> **截断技巧。**推理时,`w' = ŵ + ψ·(w - ŵ)`, trong số đó `ŵ` `w`Trong nhiều mẫu, giá trị trung bình:`ψ < 1`以多样性换质量──几乎所有 StyleGAN 演示都使用`ψ ≈ 0.7`

## StyleGAN 1 → 2 → 3  StyleGAN  phiên bản phát triển

| Version | Year | Innovation / 创新 |
|---------|------|------------|
| StyleGAN | 2019 | Mapping network + AdaIN + noise + progressive growing. / 映射网络 + AdaIN + 噪声 + 渐进增长。 |
| StyleGAN2 | 2020 | Weight demodulation replaces AdaIN (fixes droplet artifacts); skip/residual architecture; path-length regularization. / 权重解调替代 AdaIN。 |
| StyleGAN3 | 2021 | Alias-free convolution + equivariant kernels; eliminates texture sticking to pixel grid. / 无混叠卷积，消除纹理粘附。 |
| StyleGAN-XL | 2022 | Class-conditional, 1024², ImageNet. / 类别条件，1024²。 |
| R3GAN | 2024 | Rebrands with stronger reg; closes gap to diffusion on FFHQ-1024 with 20x fewer params. / 更强正则化，20 倍更少参数。 |

Trong năm 2026, StyleGAN3 vẫn là mặc định cho (a) quang học miền hẹp với FPS cao, (b) điều chỉnh miền ít ảnh (đào trên một tập dữ liệu mới với 100 hình ảnh, lập bản đồ đóng băng), (c) chỉnh sửa dựa trên đảo ngược (để tìm ra các `w`mà tái tạo lại một bức ảnh thực, sau đó chỉnh sửa nó.`w`). Đối với các miền mở văn bản-đối với hình ảnh, nó không phải là công cụ  phân tán là.

> StyleGAN3 năm 2026  vẫn là một lựa chọn mặc định của các trường hợp sau đây: a) FPS cao 域狭影级真感, b) Lượng mẫu nhỏ thích ứng, c) dựa trên các bài viết phản diễn.

## Hãy xây dựng nó.
```figure
gx-stylegan-mapping
```

## Hãy xây dựng nó

`code/main.py`thực hiện một đồ chơi "style-GAN lite" trong 1-D: một MLP bản đồ, một chức năng tổng hợp lấy một vector liên tục được học và điều chỉnh nó bằng `w`- dẫn đến quy mô/ thiên vị, và tiếng ồn mỗi lớp.`w`qua các trận đấu hoặc nhịp concatenating của các mô-đun hợp`z`vào đầu vào của máy phát điện.

> `code/main.py`Trong 1D thực hiện một "StyleGAN lite": chiếu MLP, hàm tổng hợp và mỗi lớp tiếng ồn. Nó được hiển thị thông qua việc tạo ra các điều chỉnh`w`Với `z`拼接到输入相比效果相当或更好──

### Bước 1: mạng bản đồ

```python
def mapping(z, M):
    h = z
    for i in range(num_layers):
        h = leaky_relu(add(matmul(M[f"W{i}"], h), M[f"b{i}"]))
    return h
```

### Bước 2: Tiêu chuẩn hóa phiên bản thích ứng

```python
def adain(x, w_scale, w_bias):
    mu = mean(x)
    sd = std(x)
    x_norm = [(xi - mu) / (sd + 1e-8) for xi in x]
    return [w_scale * xi + w_bias for xi in x_norm]
```

Skala và thiên vị của bản đồ tính năng xuất phát từ `w`qua chiếu tuyến tính.

> Các đặc điểm của biểu đồ được rút ngắn và chuyển hướng từ`w`                                                                                                                                                                                                                                                              

### Bước 3: Phế độ tiếng ồn mỗi lớp

```python
def add_noise(x, sigma, rng):
    return [xi + sigma * rng.gauss(0, 1) for xi in x]
```

Sigma per-channel là có thể học được.

> Mỗi đường dẫn của sigma là có thể học được.

## # Thói bẫy #

- **Droplet artifacts.**StyleGAN 1 đã tạo ra một giọt nhỏ trong các bản đồ tính năng vì AdaIN đã đánh giá trung bình bằng không.
  **液滴伪影。**StyleGAN 1 vì AdaIN 归零均值产生液滴──StyleGAN 2 的权重解调通过缩卷积权重修复──
- **Texture sticking.**Các kết cấu StyleGAN 1 và 2 theo các phối hợp pixel, không phải các phối hợp đối tượng (có thể nhìn thấy khi liên kết).
  **纹理粘附。**StyleGAN 1/2 có cấu trúc theo hình ảnh của một hình ảnh không phải của một vật thể.
- **Mode coverage.**Truncation `ψ < 0.7`trông sạch nhưng các mẫu từ một cái nếp hẹp; sử dụng `ψ = 1.0`nếu bạn cần sự đa dạng.
  **模式覆盖。**截断 `ψ < 0.7`Có vẻ sạch nhưng có thể dùng nhiều loại.`ψ = 1.0`
- **Inversion is lossy.**Chuyển một bức ảnh thực vào `W`thường được thực hiện thông qua tối ưu hóa hoặc một bộ mã hóa (e4e, ReStyle, HyperStyle). Kết quả trôi qua nhiều lần lặp lại.
  **反演有损。**Sẽ thực sự chụp ảnh phản diễn đến`W`Thông thường thông qua tối ưu hóa hoặc bộ lập trình được hoàn thành, kết quả sẽ di chuyển trong nhiều thế hệ sau đó.

## Hãy sử dụng nó để thực hiện

| Use case / 用途 | Approach / 方案 |
|----------|----------|
| Photoreal human faces (anime, product, narrow) / 照片级人脸 | StyleGAN3 FFHQ / custom fine-tune |
| Face editing from a photo / 从照片编辑人脸 | e4e inversion + StyleSpace / InterFaceGAN directions |
| Face swap / reenactment / 换脸/重演 | StyleGAN + encoder + blending |
| Avatar pipelines / 虚拟形象 | StyleGAN3 w/ ADA for low-data fine-tune |
| Domain adaptation from a few images / 少样本域适应 | Freeze mapping network, fine-tune synthesis |
| Multi-modal or text-conditioned generation / 多模态生成 | Don't — use diffusion / 不要用——用扩散模型 |

Đối với các bản demo cấp sản phẩm mà câu trả lời là "photos of a person's face", StyleGAN đánh bại sự pha trộn về chi phí suy luận (single forward pass, <10ms on a 4090) và sắc thái cho cùng một thanh chất lượng.

> Đối với trình bày sản phẩm hạng "photos face face" ,StyleGAN trong chi phí dự đoán(4090 lần trước đến trước để truyền tải,4090 trên <10ms) và cùng chất lượng dưới mức độ đã thắng trên mô hình phổ biến.

## Chuyển nó đi.

- Cứu lại`outputs/skill-stylegan-inversion.md`. Skill chụp ảnh thực tế và kết quả: phương pháp đảo ngược (e4e / ReStyle / HyperStyle), dự kiến mất mát ẩn, ngân sách chỉnh sửa (từ đâu `W`bạn có thể di chuyển trước các đồ tạo vật), và một danh sách các hướng sửa đổi được biết đến (năm, biểu hiện, tư thế).

> 保存 `outputs/skill-stylegan-inversion.md`◊ Khả năng nhận ảnh thực sự, xuất bản phản ứng, dự đoán thiệt hại tiềm tàng, ngân sách biên tập và hướng biên tập đã biết

## Tập luyện bài tập

1. **Easy / 简单.**Đi chạy`code/main.py`với `adain_on=True`và `adain_on=False`So sánh sự lây lan của các đầu ra cho một cố định tiềm ẩn vs bị rối loạn tiềm ẩn.
   分別用 `adain_on=True`和 `adain_on=False`运行―― so sánh số lượng cố định và phân bố số lượng xuất hiện của các biến động
2. **Medium / 中等.**Thực hiện quy định trộn: cho một loạt đào tạo, tính toán `w_a`- `w_b`, và áp dụng `w_a`cho nửa đầu của tổng hợp và `w_b`Bộ giải mã học được các phong cách không liên quan?
   实现混合正则化──解码器是否学到了解的风格?
3. **Hard / 困难.**Hãy lấy một mô hình StyleGAN3 FFHQ được đào tạo trước (ffhq-1024.pkl).`w`hướng điều khiển "mỉm cười" bằng cách đào tạo một SVM trên các mẫu được dán nhãn; báo cáo về mức độ bạn có thể đẩy trước khi danh tính biến mất.
   Sử dụng bài tập trước StyleGAN3 FFHQ 模型, thông qua SVM  tìm thấy kiểm soát"微笑" của `w`方向:

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Mapping network | "The MLP" / "那个 MLP" | `f: Z → W`, 8 layers, decouples latent geometry from data statistics. / 解耦隐变量几何与数据统计。 |
| W space | "The style space" / "风格空间" | Output of the mapping network; roughly disentangled. / 映射网络的输出；大致解耦。 |
| AdaIN | "Adaptive instance norm" / "自适应实例归一化" | Normalize feature map, then scale + shift by `w`-projection. / 归一化后用 `w` 投影缩放偏移。 |
| Truncation trick | "Psi" | `w = mean + ψ·(w - mean)`, ψ<1 trades diversity for quality. / ψ<1 以多样性换质量。 |
| Path-length regularization | "PL reg" | Penalizes large changes in image per unit change in `w`; makes `W` smoother. / 惩罚 `w` 单位变化引起的大图像变化。 |
| Weight demodulation | "The StyleGAN2 fix" / "StyleGAN2 修复" | Normalize conv weights instead of activations; kills droplet artifacts. / 归一化卷积权重而非激活。 |
| Alias-free | "StyleGAN3's trick" / "StyleGAN3 技巧" | Windowed sinc filters; eliminates texture sticking to the pixel grid. / 窗口 sinc 滤波器消除纹理粘附。 |
| Inversion | "Find w for a real image" / "找 w" | Optimize or encode `x → w` so `G(w) ≈ x`. / 优化或编码使 `G(w) ≈ x`。 |

## Lưu ý sản xuất: tại sao StyleGAN vẫn được xuất khẩu vào năm 2026

StyleGAN3 trên một 4090 tạo ra một khuôn mặt 10242 FFHQ trong vòng dưới 10 ms `num_steps = 1`, không có mã hóa VAE, không có thông qua sự chú ý chéo. Về mặt sản xuất đây là độ trễ sàn cho bất kỳ máy phát hình ảnh nào. Một đường ống giải mã SDXL + VAE 50 bước với cùng độ phân giải là ~ 3 giây.**300× gap**, và đối với các sản phẩm miền hẹp (các dịch vụ avatar, đường ống giấy tờ ID, sản xuất mặt hàng) nó thắng trên TCO.

> StyleGAN3 trong 4090 lên không đến 10ms 生成 10242 người mặt`num_steps = 1`, không VAE 解码, không giao giao lưu chú ý.**300 倍差距**, trong khu vực hạn chế sản phẩm TCO 获胜.

Hai hậu quả hoạt động:

> 两个运营后果:

- **No scheduler, no batcher.**Các lô hàng tĩnh tại chỗ chiếm được mục tiêu là tối ưu. Lớp hàng liên tục (tất yếu cho LLM và phân phối) cung cấp lợi ích không vì mỗi yêu cầu có cùng FLOP.
  **无需调度器或批处理器。**静态批量最优──连续批处理( đối với LLM 和扩散模型至关重要)零收益──
- **Truncation `ψ` is the safety knob.** `ψ < 0.7`mẫu từ một con hẹp của phạm vi của mạng bản đồ. Đây là đòn bẩy duy nhất mà lớp phục vụ có trên sự khác biệt mẫu.`ψ`khi tải cao nhất, tăng nó cho người dùng cao cấp.
  **截断 `ψ` 是安全旋钮。** `ψ < 0.7`Từ phạm vi của mạng lưới chiếu, đây là điểm duy nhất của sự khác biệt trong các mô hình kiểm soát cấp độ dịch vụ.`ψ`, người dùng cao cấp tăng lên.

## Xem thêm 延伸阅读

- [Karras et al. (2019). A Style-Based Generator Architecture for GANs](https://arxiv.org/abs/1812.04948) StyleGAN.
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958) StyleGAN2.
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423) StyleGAN3.
- [Tov et al. (2021). Designing an Encoder for StyleGAN Image Manipulation](https://arxiv.org/abs/2102.02766) đảo ngược e4e.
- [Sauer et al. (2022). StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets](https://arxiv.org/abs/2202.00273) StyleGAN-XL.
- [Huang et al. (2024). R3GAN: The GAN is dead; long live the GAN!](https://arxiv.org/abs/2501.05441) Công thức GAN tối thiểu hiện đại.
