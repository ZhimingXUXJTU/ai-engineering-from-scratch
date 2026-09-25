# Autoencoders & Variation Autoencoders (VAE) Ứng dụng tự lập trình và biến thể tự lập trình

> Một mã mã tự động đơn giản nén lại sau đó tái tạo. Nó ghi nhớ. Nó không tạo ra. Thêm một thủ thuật  buộc mã để trông Gaussian  và bạn có được một mẫu.`z = mu + sigma * epsilon`, đó là lý do tại sao mỗi mô hình ảnh phân tán tiềm ẩn và tương thích dòng chảy mà bạn sử dụng vào năm 2026 có một VAE tại đầu vào.

> **【中文解读】**Thông thường tự mã hóa nén lại, chỉ là ký ức, không thể tạo ra.`z = mu + sigma * epsilon`Để độ cao có thể vượt qua các hoạt động, là chìa khóa của tập luyện VAE.

> **【拓展：VAE 是 Stable Diffusion 的基石】**2026 năm tất cả các mô hình mở rộng tiềm năng ((Stable Diffusion、FLUX) đều hoạt động trong không gian tiềm năng của VAE.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 07 (CNNs / 卷积神经网络), Phase 8 · 01 (Taxonomy / 分类)
**Time:** ~75 minutes

## Vấn đề  vấn đề giới thiệu

Nhiết nét MNIST 784 pixel thành mã số 16, sau đó tái tạo. Một mã tự động đơn giản sẽ làm tái tạo MSE nhưng không gian mã là một sự lộn xộn. Chọn một điểm ngẫu nhiên trong không gian mã, giải mã nó, và bạn sẽ có tiếng ồn. Nó không có mẫu. Đó là một mô hình nén mặc trang phục.

> Để làm cho 784 像素 MNIST số lượng được nén thành 16 数字 mã tái tạo.

Điều bạn thực sự muốn là: (a) không gian mã là một phân bố sạch, trơn tru bạn có thể lấy mẫu từ  nói là một Gaussian isotropic `N(0, I)`, (b) giải mã bất kỳ mẫu nào tạo ra một con số đáng tin cậy, và (c) bộ mã hóa và bộ giải mã vẫn nén tốt. Ba mục tiêu, một kiến trúc, một lỗ.

> Bạn thực sự muốn: a) 编码空间 là干净,平滑,可采用样式分布 像各向同性高斯`N(0, I)`;((b) 解码任何样本都产生合理数字;(c) 编码器和编码器仍然压缩良好──三个目标,一个架构,一个损失──

VAE 2013 của Kingma giải quyết vấn đề này bằng cách đào tạo bộ mã hóa để phát ra một * phân phối * `q(z|x) = N(μ(x), σ(x)²)`, kéo phân phối đó về phía trước `N(0, I)`thông qua một hình phạt KL, và sau đó lấy mẫu `z`từ `q(z|x)`Khi suy luận, hãy thả bộ mã hóa, lấy mẫu`z ~ N(0, I)`Cảnh phạt KL là điều buộc không gian mã phải được cấu trúc.

> Kingma 2013 năm VAE 通过训练编码器输出*分布* `q(z|x) = N(μ(x), σ(x)²)`Để giải quyết vấn đề này, thông qua KL  trừng phạt sẽ được phân phối ra phía trước `N(0, I)`, rồi từ`q(z|x)`Trung采样 `z`Rõ ràng là không phải là một cái gì đó.`N(0, I)`采样 `z`,解码──KL 惩罚正是使编码空间结构化的关键──

Trong năm 2026, VAE hiếm khi được vận chuyển độc lập  chúng đã được vượt trội bởi sự phân tán về chất lượng hình ảnh nguyên thô  nhưng chúng là bộ mã hóa lựa chọn cho mọi mô hình phân tán tiềm ẩn (SD 1/2/XL/3, Flux, AudioCraft).

> Năm 2026 VAE  Very few independent deploy đã được phân phối trên chất lượng hình ảnh ban đầu hơn nhưng nó là bộ lập trình đầu tiên của tất cả các mô hình phân phối tiềm năng (SD 1/2/XL/3、Flux、AudioCraft).

> **【中文解读】**Nhìn sâu sắc cốt lõi của VAE: Hãy để bộ lập trình xuất phát phân phối chứ không phải đánh giá điểm.`z = mu + sigma * epsilon`Để sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình, sử dụng các mô hình và các mô hình, sử dụng các mô hình, sử dụng các mô hình và các mô hình, sử dụng các mô hình và các mô hình.

> **【拓展：beta-VAE 与解耦表示学习】**beta-VAE(2017) thông qua điều chỉnh beta 参数 kiểm soát tái tạo với cân nặng KL;;beta<1 时重建更清晰但潜在空间不规整;beta>1 时潜在空间更规整但图像更模糊;;Beta 足够大时,VAE có thể học được biểu hiện"解" của mỗi chiều kích mã hóa các yếu tố ngữ义独立 ((如色,形,大小) ⋅ điều này đã kích thích mô hình mở rộng tiếp theo trong tiềm năng không gian để làm cho có thể tạo ra có thể kiểm soát được;;

## Khái niệm cốt lõi

![Autoencoder vs VAE: the reparameterization trick](../assets/vae.svg)

**Autoencoder.** `z = encoder(x)`- `x̂ = decoder(z)`, mất mát = `||x - x̂||²`Không gian mã không có cấu trúc.

> **自编码器。** `z = encoder(x)`- Tôi không biết.`x̂ = decoder(z)`, mất mát = `||x - x̂||²`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

**VAE encoder.**Tạo ra hai vector: `μ(x)`và `log σ²(x)`- Chúng định nghĩa`q(z|x) = N(μ, diag(σ²))`- Tôi không biết.

> **VAE 编码器。**输出 2 量:`μ(x)`和 `log σ²(x)` Chúng đã định nghĩa `q(z|x) = N(μ, diag(σ²))`

**Reparameterization trick.**Tiêu chuẩn lấy mẫu từ `q(z|x)`không phân biệt được.`z = μ + σ·ε`nơi `ε ~ N(0, I)`Giờ thì`z`là một hàm xác định của `(μ, σ)`cộng với tiếng ồn không phải tham số  gradient chảy qua `μ`và `σ`- Tôi không biết.

> **重参数化技巧。**Từ `q(z|x)`采样不可微──将采样重写为 `z = μ + σ·ε`, trong số đó `ε ~ N(0, I)`  `z` `(μ, σ)`Các hàm xác định cộng với không số lượng tiếng ồn  thang độ có thể thông qua `μ`和 `σ`Tránh truyền.

**Loss.**Bằng chứng Bind thấp hơn (ELBO), hai thuật ngữ:

```
loss = reconstruction + β · KL[q(z|x) || N(0, I)]
     = ||x - x̂||²  + β · Σ_i ( σ_i² + μ_i² - log σ_i² - 1 ) / 2
```

Việc tái thiết thúc đẩy `x̂`hướng tới`x`KL đẩy.`q(z|x)`Vị trí của các mô hình này được tạo ra bởi các mô hình hình dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng dạng

> Động lực xây dựng`x̂`趋近 `x` KL  thúc đẩy `q(z|x)`趋近先验──两者相互权衡──β 小(<1)= 更利的样本,编码空间不太高斯──β 大(>1)= 更干净的编码空间,更模糊的样本──β-VAE(2017) làm cho vòng này được biết đến,并开启了解表示学习研究──

**Sampling.**Khi kết luận: vẽ`z ~ N(0, I)`Một lần đi trước không có mẫu lặp lại như phân tán.

> **采样。**推理时: từ `N(0, I)`抽取 `z`, gửi vào giải mã trước hướng truyền;; đơn giản trước hướng truyền;; không cần thiết như mô hình mở rộng như vậy;

> **【中文解读】**Hai thành phần của ELBO mất mát có thể được phân chia: tái tạo mất mát đảm bảo chất lượng mã, KL 散度 đảm bảo quy mô tiềm ẩn của không gian. 推理时完全不需要编码器直接从N(0,I) 采样 z 送入解码器──VAE 生成速度快(单次前向传播), nhưng chất lượng hình ảnh thường mơ hồ hơn mô hình mở rộng, vì nó tối ưu hóa là ELBO 下界而非精确似──

> **【拓展：Stable Diffusion 中的 VAE】**Stable Diffusion sử dụng VAE được đào tạo trước sẽ 512x512 图像压缩 xuống 64x64 tiềm năng không gian(8 lần dưới dạng)  quá trình phân tán được thực hiện trong tiềm năng không gian, giảm đáng kể lượng tính toán;. SD 3 sử dụng VAE hơn tiến triển  hỗ trợ 16 đường tiềm năng không gian, chất lượng hình ảnh cao hơn。

## Hãy xây dựng nó.
```figure
vae-latent-grid
```

## Hãy xây dựng nó

`code/main.py`thực hiện một VAE nhỏ bé mà không có numpy hoặc ngọn đuốc. Input là dữ liệu tổng hợp 8-dimensional được lấy từ một hỗn hợp Gaussian 2 thành phần trong 8-D. Encoder và decoder là một lớp ẩn MLPs. Chúng tôi thực hiện hoạt động tanh, đi trước, mất, và một chữ viết tay đi ngược. Không sản xuất  giáo dục.

> `code/main.py`实现一个不依赖于 numpy或火的微型VAE──输入是从8维2 分量高斯混合中抽取的8维合成数据──编码器和编码器是单隐层MLP──我们实现 tanh 激活、前向传播、损失和手写反向传播──不是生产代码纯粹教学──

### Bước 1: mã hóa về phía trước

```python
def encode(x, enc):
    h = tanh(add(matmul(enc["W1"], x), enc["b1"]))
    mu = add(matmul(enc["W_mu"], h), enc["b_mu"])
    log_sigma2 = add(matmul(enc["W_sig"], h), enc["b_sig"])
    return mu, log_sigma2
```

`log σ²`thay vì `σ`Vì vậy, đầu ra mạng không bị hạn chế (softplus của σ là một cái bẫy  gradient chết ở σ ≈ 0).

> Sử dụng `log σ²`Không`σ`Để kết nối mạng không bị ràng buộc,  của softplus là một cái bẫy trong  ≈ 0 时梯度 sẽ biến mất)

### Bước 2: tái định đo và giải mã

```python
def reparameterize(mu, log_sigma2, rng):
    eps = [rng.gauss(0, 1) for _ in mu]
    sigma = [math.exp(0.5 * lv) for lv in log_sigma2]
    return [m + s * e for m, s, e in zip(mu, sigma, eps)]

def decode(z, dec):
    h = tanh(add(matmul(dec["W1"], z), dec["b1"]))
    return add(matmul(dec["W_out"], h), dec["b_out"])
```

### Bước 3: ELBO

```python
def elbo(x, x_hat, mu, log_sigma2, beta=1.0):
    recon = sum((a - b) ** 2 for a, b in zip(x, x_hat))
    kl = 0.5 * sum(math.exp(lv) + m * m - lv - 1 for m, lv in zip(mu, log_sigma2))
    return recon + beta * kl, recon, kl
```

Kế hoạch này được thực hiện bởi các nhà phân phối của các hệ thống phân phối là Gaussian. không tích hợp số. người ta vẫn gửi mã với ước tính Monte-carlo KL vào năm 2026  nó là 3x chậm hơn mà không có lý do.

> 精确的闭式 KL, vì hai phân bố đều cao ⋅ không có số lượng积分⋅2026 năm còn có người phát hành được 蒙特卡洛 KL 估计代码无端慢了3倍⋅

### Bước 4: tạo

```python
def sample(dec, z_dim, rng):
    z = [rng.gauss(0, 1) for _ in range(z_dim)]
    return decode(z, dec)
```

Đó là mô hình tạo ra. 5 dòng.

> Đó là tạo mô hình.

## # Thói bẫy #

- **Posterior collapse.**KL term drive `q(z|x) → N(0, I)`quá mạnh mẽ mà`z`không có thông tin nào về `x`. Lắp đặt: β-annealing (bắt đầu β=0, ramp đến 1), free bits, hoặc skip KL trên kích thước không hoạt động.
  **后验坍塌。**KL 项如此强强地将 `q(z|x)`拉向 `N(0, I)`, dẫn đến`z`Không mang về `x`Từ β=0 开始,逐渐增至1) 、free bits 或跳过不活维度的 KL。
- **Blurry samples.**Thiết lập: decoder phân biệt (VQ-VAE, NVAE), hoặc chỉ sử dụng VAE như một bộ mã hóa và phân tán chồng trên các laten (đó là điều Stable Diffusion làm).
  **模糊样本。**高斯解码器似然 nghĩa là MSE 重建一组合理数字的平均值是一个模糊的数字──修复:离散解码器(VQ-VAE、NVAE), hoặc chỉ dùng VAE như một bộ lập trình, trên tiềm năng không gian chồng lên mô hình mở rộng──
- **β too large, too early.**Xem sự sụp đổ sau, bắt đầu ở β≈0.01 và tăng tốc.
  **β 太大太早。**见后验塌── từ β≈0.01  bắt đầu并逐渐 tăng──
- **Latent dim too small.**16-D hoạt động cho MNIST, 256-D cho ImageNet 2562, 2048-D cho ImageNet 10242. VAE của Stable Diffusion nén 512×512×3 → 64×64×4 (32x downsample factor trong không gian, 32x trong kênh).
  **潜在维度太小。**MNIST dùng 16 维,ImageNet 2562 dùng 256 维── VAE của Stable Diffusion sẽ được 512×512×3 压缩 thành 64×64×4──

## Hãy sử dụng nó để thực hiện

Bộ VAE năm 2026:

> 2026 年 VAE 技术:

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Image-latent encoder for diffusion / 图像潜在编码器 | Stable Diffusion VAE (`sd-vae-ft-ema`) or Flux VAE |
| Audio-latent encoder / 音频潜在编码器 | Encodec (Meta), SoundStream, or DAC (Descript) |
| Video latents / 视频潜在表示 | Sora's spatiotemporal patches, Latte VAE, WAN VAE |
| Disentangled representation learning / 解耦表示学习 | β-VAE, FactorVAE, TCVAE |
| Discrete latents (for transformer modelling) / 离散潜在表示 | VQ-VAE, RVQ (ResidualVQ) |
| Continuous latents for generation / 连续潜在生成 | Plain VAE, then condition a flow/diffusion model in that latent space |

Một mô hình phân tán ẩn là một mô hình phân tán có một mô hình phân tán sống giữa mã hóa và mã hóa. VAE làm nén thô, mô hình phân tán làm việc nặng.

> 潜在扩散模型就是编码器和编码器之间加入了扩散模型的 VAE──VAE做粗压缩,扩散模型做重活──视频(VAE + 视频 DiT) 和音频(Encodec + MusicGen biến đổi) 同理──

## Chuyển nó đi.

- Cứu lại`outputs/skill-vae-trainer.md`- Tôi không biết.

> 保存 `outputs/skill-vae-trainer.md`

Các kỹ năng được lấy: hồ sơ bộ dữ liệu + mục tiêu trộm laten + sử dụng tiếp theo (tái tạo, lấy mẫu hoặc đầu vào trộm laten) và đầu ra: lựa chọn kiến trúc (sơn/β/VQ/RVQ), lịch trình β, trộm laten, xác suất giải mã (Gaussian vs categorical), và kế hoạch đánh giá (recon MSE, KL per dim, khoảng cách Fréchet giữa `q(z|x)`và `N(0, I)`().

> Kỹ năng nhận: dữ liệu tập hợp概况 + 潜在维度目标 + 下游用途(重建、采样或潜在扩散输入),输出:架构选择(平面/β/VQ/RVQ) 、β 调度、潜在维度、解码器似然(高斯 vs 类别) 和评估计划──

## Tập luyện bài tập

1. **Easy / 简单.**Thay đổi`β`trong `code/main.py`đến`0.01`- `0.1`- `1.0`- `5.0`. ghi lại tái tạo cuối cùng của MSE và KL.
   Trong `code/main.py`Trung `β`改为 `0.01``0.1``1.0``5.0`记录最终重建 MSE 和 KL── nào là tốt nhất đối với dữ liệu tổng hợp của bạn?
2. **Medium / 中等.**Thay thế xác suất decoder Gaussian bằng xác suất Bernoulli (sự mất mát entropy chéo). So sánh chất lượng mẫu trên một phiên bản nhị phân của cùng một dữ liệu tổng hợp.
   将高斯解码器似然然替换为伯努利似然交叉损失
3. **Hard / 困难.**Tăng `code/main.py`thành một VQ-VAE mini: thay thế liên tục `z`- so sánh MSE tái thiết và báo cáo số lượng các mục codebook được sử dụng (sự sụp đổ codebook là thực).
   sẽ`code/main.py`扩展为迷你 VQ-VAE: dùng K=32 的码本最近邻找替换连续 `z`❖ So sánh xây dựng lại MSE và báo cáo đã sử dụng bao nhiêu mã trong các bài viết này.

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Autoencoder | Encode-decode network / 编码-解码网络 | `x → z → x̂`, learn MSE. Not generative. / `x → z → x̂`，学习 MSE。不是生成模型。 |
| VAE | AE with a sampler / 带采样器的 AE | Encoder outputs a distribution, KL penalty shapes code space. / 编码器输出分布，KL 惩罚塑造编码空间。 |
| ELBO | Evidence lower bound / 证据下界 | `log p(x) ≥ recon - KL[q(z\|x) \|\| p(z)]`; tight when `q = p(z\|x)`. |
| Reparameterization | `z = μ + σ·ε` | Rewrites stochastic node as deterministic + pure noise. Enables backprop through sampling. / 将随机节点重写为确定性 + 纯噪声。使采样可反向传播。 |
| Prior | `p(z)` | Target distribution for the latent, typically `N(0, I)`. / 潜在变量的目标分布，通常是 `N(0, I)`。 |
| Posterior collapse | "KL term wins" / "KL 项赢了" | Encoder ignores `x`, outputs the prior; decoder must hallucinate. / 编码器忽略 `x`，输出先验；解码器只能幻觉。 |
| β-VAE | Tunable KL weight / 可调 KL 权重 | `loss = recon + β·KL`. Higher β = more disentangled but blurrier. / β 越高越解耦但越模糊。 |
| VQ-VAE | Discrete latent / 离散潜在变量 | Replace continuous `z` with nearest codebook vector; enables transformer modelling. / 用最近码本向量替换连续 `z`。 |

## Lưu ý sản xuất: VAE là đường dẫn nóng nhất trong một máy chủ phân phối .

Trong một đường ống dẫn Stable Diffusion / Flux / SD3, VAE được gọi hai lần theo yêu cầu  một lần để mã hóa (nếu thực hiện img2img / inpainting) và một lần để giải mã. Tại 10242, đoạn giải mã thường là đỉnh kích hoạt lớn nhất trong toàn bộ đường ống vì nó có thể tăng lên `128×128×16`Lưu ý về `1024×1024×3`Hai hậu quả thực tế:

> Trong dòng chảy ổn định / dòng chảy / SD3, VAE mỗi lần yêu cầu được调用 hai lần một lần编码(img2img/inpainting) một lần giải mã. Trong 10242 phân giải, máy giải mã thường là phần lớn nhất trong dòng chảy.

- **Slice or tile the decode.** `diffusers`- Tự động`pipe.vae.enable_slicing()`và `pipe.vae.enable_tiling()`Tiiling giao dịch một đồ tạo tác nhỏ cho `O(tile²)`trí nhớ thay vì `O(H·W)`- Khả năng thiết yếu cho 10242+ trên các GPU tiêu dùng.
  **切片或分块解码。** `diffusers`提供 `enable_slicing()`和 `enable_tiling()`分块以轻微接伪影换取 `O(tile²)`Nội dung:
- **bf16 decoder, fp32 numerics for the final resize.**SD 1.x VAE được phát hành trong fp32 và * lặng lẽ sản xuất NaNs* khi đúc lên fp16 tại 10242+. tàu SDXL `madebyollin/sdxl-vae-fp16-fix` luôn thích biến thể cố định fp16 hoặc sử dụng bf16.
  **bf16 解码器，fp32 用于最终 resize。**SD 1.x VAE 在 fp16 下 10242+ 会静默产生 NaN──始终使用 fp16-fix 变体或 bf16──

## Xem thêm 延伸阅读

- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) tờ VAE.
- [Higgins et al. (2017). β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework](https://openreview.net/forum?id=Sy2fzU9gl) chia tách β-VAE.
- [van den Oord et al. (2017). Neural Discrete Representation Learning](https://arxiv.org/abs/1711.00937) VQ-VAE.
- [Vahdat & Kautz (2021). NVAE: A Deep Hierarchical Variational Autoencoder](https://arxiv.org/abs/2007.03898) hình ảnh hiện đại nhất VAE.
- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) Sự pha trộn ổn định; VAE như một bộ mã hóa.
- [Défossez et al. (2022). High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438) Encodec, tiêu chuẩn âm thanh VAE.
