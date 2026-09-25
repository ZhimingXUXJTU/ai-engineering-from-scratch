# Sự pha trộn ẩn và sự pha trộn ổn định 

> Sự phân tán không gian phích số trên hình ảnh 512x512 là một tội ác chiến tranh tính toán. Rombach et al. (2022) nhận thấy rằng bạn không cần tất cả các kích thước 786k để tạo ra một hình ảnh  bạn cần đủ để chụp cấu trúc ngữ nghĩa, và một bộ giải mã riêng cho phần còn lại.

> **【中文解读】**Trong 512x512 像素空间做扩散是计算灾难. Rombach 等人发现不需要全部78.6万维度只需要捕获语义结构,剩余用解码器补充.

> **【拓展：Stable Diffusion 的革命】**Stable Diffusion sẽ mở rộng quá trình di chuyển từ không gian hình ảnh đến không gian tiềm ẩn, lượng tính toán giảm xuống hàng chục lần, cho phép GPU cấp tiêu thụ có thể hoạt động. Sau khi phát hành nguồn mở, nó đã tạo ra LoRA, ControlNet và các môi trường phong phú, thúc đẩy phổ biến AIGC.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 02 (VAE), Phase 8 · 06 (DDPM), Phase 7 · 09 (ViT)
**Time:** ~75 minutes

## Vấn đề  vấn đề giới thiệu

Sự phân tán trong không gian phím tại 5122 có nghĩa là U-Net chạy trên các tensor hình dạng .`[B, 3, 512, 512]`Mỗi bước lấy mẫu là ~ 100 GFLOPS cho một U-Net 500M-param. 50 bước là 5 TFLOPS cho mỗi hình ảnh. Đưa trên một tỷ hình ảnh và hóa đơn tính toán là vô lý.

> 5122 像素空间扩散 nghĩa là U-Net trong `[B, 3, 512, 512]`张量上运行──每采样步约100 GFLOPS──50步就是5 TFLOPS──在十亿图像上训练计算成本荒谬──

Hầu hết các FLOP đó đi đến đẩy các chi tiết không quan trọng về nhận thức qua mạng  kết cấu tần số cao mà một VAE bị mất có thể nén ra. Ý tưởng của Rombach: đào tạo một VAE một lần (tầng * đầu tiên*), đóng băng nó, và chạy truyền hoàn toàn trong không gian ẩn 64×64 4 kênh (tầng * hai*).

> Phần lớn FLOPs được sử dụng để đưa ra cảm giác trên không quan trọng chi tiết.

Đây là công thức Stable Diffusion. SD 1.x / 2.x sử dụng một U-Net 860M trên `64×64×4`Các hệ thống này được phát triển trong các trường hợp tiềm ẩn, SDXL sử dụng một mạng U-Net 2.6B trên `128×128×4`, SD3 thay đổi U-Net với một Difusion Transformer (DiT) với dòng chảy phù hợp. Flux.1-dev (Black Forest Labs, 2024) vận chuyển một DiT-MMDiT 12B-param. Tất cả chạy trên cùng một nền hai giai đoạn.

> Đây là phương thức của Stable Diffusion. SD 1.x/2.x sử dụng 860M U-Net trên 64×64×4 trên, SDXL sử dụng 2.6B U-Net trên 128×128×4 trên, SD3 sử dụng DiT + Flow Matching thay thế U-Net. Flux.1-dev sử dụng 12B MMDiT。 tất cả hoạt động trên cùng hai giai đoạn cơ sở.

> **【中文解读】**Các thiết kế của Stable Diffusion là hai giai đoạn: 1) giai đoạn đầu tiên VAE 编码器 sẽ 512x512 图像压缩 thành 64x64x4  tiềm năng空间(16 lần压缩); 2) giai đoạn thứ hai 运行在潜在空间中运行扩散过程――U-Net 在 64x64 张量上运行,计算量降低约64倍――从 SD 1.x到 SD3 演进:U-Net → DiT(Diffusion Transformer),DDPM → Flow Matching――

> **【拓展：从 U-Net 到 DiT 的架构变迁】**SD 1.x/2.x Sử dụng U-Net  như một mạng để gây tiếng ồn.SD3(2024) và FLUX  chuyển hướng đến DiT(Diffusion Transformer)  sử dụng Transformer  thay thế U-Net。  DiT                                                                                                                                                                                                                                 

## Khái niệm cốt lõi

![Latent diffusion: VAE compression + diffusion in latent space](../assets/latent-diffusion.svg)

**Two stages, separately trained.**

> **两个阶段，分别训练。**

1. **Stage 1 — VAE.**Mã hóa `E(x) → z`, decoder `D(z) → x`. Nhấn mục tiêu: 8x mẫu xuống trong mỗi trục không gian + điều chỉnh các kênh để tổng kích thước ẩn là ~ 1/16 của số lượng pixel.`z`không phải là quá Gaussian, bởi vì chúng tôi không cần mẫu chính xác từ `z`Thường được huấn luyện với một thất bại đối thủ vì vậy hình ảnh được giải mã là sắc nét.

   **阶段 1 — VAE。**编码器 `E(x) → z`, giải mã `D(z) → x`△ mục tiêu: mỗi không gian轴 8 倍下采样──损失 = 重建(L1 + LPIPS) + KL(小权重)。

2. **Stage 2 — diffusion on `z`.**Chữa bệnh`z = E(x_real)`Đào tạo một U-Net (hoặc DiT) để phản đối`z_t`- Khi kết luận: mẫu`z_0`qua sự phân tán, sau đó `x = D(z_0)`- Tôi không biết.

   **阶段 2 — 在 `z` 上扩散。**sẽ`z = E(x_real)`视为数据──训练 U-Net(或 DiT) 去噪音──推理时:采样 `z_0`, rồi rồi`x = D(z_0)`

**Text conditioning.**Hai thành phần bổ sung. Một mã hóa văn bản đóng băng (CLIP-L cho SD 1.x, CLIP-L+OpenCLIP-G cho SD 2/XL, T5-XXL cho SD3 và Flux).`[Q = image features, K = V = text tokens]`Các mã chỉ là cách duy nhất văn bản ảnh hưởng đến hình ảnh.

> **文本条件化。**2 phần phụ: 结的文本编码器和交叉注意注入── mỗi U-Net 块 dùng `[Q = 图像特征, K = V = 文本 token]`Làm giao lưu chú ý. Đài chỉ là cách duy nhất để ảnh hưởng đến văn bản.

**The loss function is identical to Lesson 06.**DDPM / dòng chảy tương ứng MSE trên tiếng ồn. Bạn chỉ cần thay đổi miền dữ liệu.

> **损失函数与第 06 课完全相同。**只是交换了数据域──

## Các biến thể kiến trúc

| Model / 模型 | Year | Backbone / 骨干 | Latent shape / 潜在形状 | Text encoder / 文本编码器 | Params / 参数量 |
|-------|------|----------|--------------|--------------|--------|
| SD 1.5 | 2022 | U-Net | 64×64×4 | CLIP-L (77 tokens) | 860M |
| SD 2.1 | 2022 | U-Net | 64×64×4 | OpenCLIP-H | 865M |
| SDXL | 2023 | U-Net + refiner | 128×128×4 | CLIP-L + OpenCLIP-G | 2.6B + 6.6B |
| SDXL-Turbo | 2023 | Distilled | 128×128×4 | same | 1-4 step sampling / 1-4 步采样 |
| SD3 | 2024 | MMDiT (multimodal DiT) | 128×128×16 | T5-XXL + CLIP-L + CLIP-G | 2B / 8B |
| Flux.1-dev | 2024 | MMDiT | 128×128×16 | T5-XXL + CLIP-L | 12B |
| Flux.1-schnell | 2024 | MMDiT distilled | 128×128×16 | T5-XXL + CLIP-L | 12B, 1-4 step |

Xu hướng: thay thế U-Net bằng DiT (giới chuyển đổi trên các bản vá ẩn), mở rộng mã hóa văn bản (T5 vượt CLIP để tuân thủ nhanh chóng), tăng các kênh ẩn (4 → 16 cung cấp nhiều không gian phân tích hơn).

> 趋势: sử dụng DiT 替代 U-Net, mở rộng văn bản编码器(T5 在 prompt 遵循上优于CLIP), tăng tiềm năng thông qua(4→16 给更多细节余量)

## Hãy xây dựng nó.
```figure
noise-schedule
```

## Hãy xây dựng nó

`code/main.py`xếp hàng một đồ chơi 1-D "VAE" (tự xác định mã hóa + decoder, để chứng minh; một VAE thực sự sẽ là một con conv net) trên đầu DDPM từ Bài học 06 và thêm điều kiện lớp với hướng dẫn không phân loại. Nó cho thấy rằng cùng một mất tích phân tán hoạt động cho dù bạn chạy trên giá trị nguyên chất 1-D hoặc trên giá trị mã hóa  thông tin sâu sắc chính.

> `code/main.py`Trong lớp 06 DDPM                                                                                                                                                                                                                                                            

### Bước 1: mã hóa/bản giải mã

```python
def encode(x):    return x * 0.5          # toy "compression" to smaller scale
def decode(z):    return z * 2.0
```

Một VAE thực sự có trọng lượng được đào tạo.`z`không quan tâm đến không gian dữ liệu gốc.

> Trong thực tế, VAE có thể có được một số tập luyện tốt.`z`Ưu hành không quan tâm đến không gian dữ liệu nguyên thủy.

### Bước 2: phân tán trong `z`- Không gian

DDPM tương tự như bài học 06.`z = E(x)`Sau khi lấy mẫu`z_0`, giải mã với `D(z_0)`- Tôi không biết.

> DDPM giống như thứ 06                                                                                                                                                                                                                                                            `z = E(x)`   `z_0`后用 `D(z_0)`解码.

### Bước 3: hướng dẫn không có phân loại

Trong quá trình đào tạo, hãy bỏ nhãn lớp 10% thời gian (đổi lại bằng một token không).`ε_cond`và `ε_uncond`, sau đó:

```python
eps_cfg = (1 + w) * eps_cond - w * eps_uncond
```

`w = 0`= không có hướng dẫn (cụ thể đa dạng),`w = 3`= mặc định, `w = 7+`= bão hòa / quá sắc nét.

> `w = 0`= 无引导(完全多样性),`w = 3`= 默认,`w = 7+`= 和/过度利。

### Bước 4: Điều kiện văn bản (định nghĩa, không phải mã)

Thay thế nhãn lớp bằng một đầu ra mã hóa văn bản đóng băng. Cho các văn bản nhúng vào U-Net thông qua sự chú ý chéo:

> Sử dụng 结文编码器输出替换类别标签.

```python
h = h + CrossAttention(Q=h, K=text_embed, V=text_embed)
```

Đây là sự khác biệt đáng kể duy nhất giữa mô hình phân tán theo điều kiện lớp và phân tán ổn định.

> Đây là sự khác biệt duy nhất về chất lượng giữa mô hình phân bố và phân bố ổn định.

## # Thói bẫy #

- **VAE-scale mismatch.**SD 1.x VAEs có một định lượng không đổi (`scaling_factor ≈ 0.18215`(Phần 2) được áp dụng sau khi mã hóa.
  **VAE 尺度不匹配。**SD 1.x VAE 编码 sau có số lượng thường xuyên bị thu nhỏ.
- **Text encoder silently wrong.**SD3 cần T5-XXL với >=128 token, và sự quay lại CLIP-chỉ là thua lỗ.`use_t5=True`hoặc các miệng núi lửa trung thành.
  **文本编码器静默错误。**SD3 需要 T5-XXL 且 >=128 token──
- **Mixing latent spaces.**SDXL, SD3, Flux đều sử dụng các VAE khác nhau. LoRA được đào tạo trên các laten SDXL sẽ không hoạt động trên SD3.
  **混合潜在空间。**SDXL、SD3、Flux sử dụng các VAE khác nhau──SDXL của LoRA không thể sử dụng trên SD3──
- **CFG too high.** `w > 10`tạo ra những hình ảnh bão hòa, dầu và quá phù hợp với các yêu cầu với chi phí của sự đa dạng.`w = 3-7`- Tôi không biết.
  **CFG 太高。** `w > 10`tạo ra hình ảnh 和、油的图像──
- **Negative prompts leaking.**Lần báo âm trống trở thành biểu tượng không; một lời báo âm đầy trở thành `ε_uncond`Chúng không giống nhau; một số đường ống âm thầm mặc định đến null.
  **负向 prompt 泄漏。**空负向 prompt 变为零代币;填充的变为 `ε_uncond`                                                                                                                                                                                                                                                              

## Hãy sử dụng nó để thực hiện

Các đống sản xuất vào năm 2026:

> 2026 年生产技术:

| Target / 目标 | Recommended backbone / 推荐骨干 |
|--------|----------------------|
| Narrow domain, paired data, from scratch / 窄域配对从零训练 | SDXL fine-tune (LoRA / full) — fastest to ship |
| Open-domain text-to-image, open weights / 开放域开放权重 | Flux.1-dev (12B, Apache / non-commercial) or SD3.5-Large |
| Fastest inference, open weights / 最快推理开放权重 | Flux.1-schnell (1-4 step, Apache) or SDXL-Lightning |
| Best prompt adherence, hosted / 最佳 prompt 遵循，托管 | GPT-Image / DALL-E 3, Midjourney v7, Imagen 4 |
| Edit workflows / 编辑工作流 | Flux.1-Kontext (Dec 2024) — natively accepts image + text |
| Research, baseline / 研究基线 | SD 1.5 — ancient but well-studied |

## Chuyển nó đi.

- Cứu lại`outputs/skill-sd-prompter.md`. Skill lấy một prompt văn bản + phong cách mục tiêu và đầu ra: mô hình + điểm kiểm tra, thang CFG, mẫu, prompt tiêu cực, độ phân giải, sự kết hợp tùy chọn ControlNet / IP-Adapter, và danh sách kiểm tra QA từng bước.

> 保存 `outputs/skill-sd-prompter.md` Khả năng nhận văn bản提示+ mục tiêu风格,输出模型+检查点、CFG、采样器、负向提示等──

## Tập luyện bài tập

1. **Easy / 简单.**Đi chạy`code/main.py`Với hướng dẫn`w ∈ {0, 1, 3, 7, 15}`- Đăng mẫu trung bình theo lớp.`w`có phải các phương tiện lớp khác nhau ngoài phương tiện dữ liệu thực?
   用 `w ∈ {0, 1, 3, 7, 15}`运行――在哪里 `w`Giá trị trung bình của phân loại so với giá trị trung bình dữ liệu thực?
2. **Medium / 中等.**Thay đổi bộ mã hóa hàng tuyến đồ chơi cho cặp mã hóa / mã hóa tanh-MLP với mất tích tái tạo. Phục trệ phân tán trên các dấu ẩn mới.
   Để thay thế máy lập trình game linear để tanh-MLP 编码/ giải mã器.
3. **Hard / 困难.**Thiết lập một suy luận Stable Diffusion thực sự với các diffuser: tải `sdxl-base`, chạy 30 bước Euler với CFG=7, thời gian nó.`sdxl-turbo`cùng chủ đề, chất lượng khác nhau  mô tả những gì đã thay đổi và tại sao.
   Sử dụng các bộ phân tán 搭建真实SD 推理, so sánh SDXL-base 和 SDXL-Turbo──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| First stage | "The VAE" | Trained encoder/decoder pair; compresses 512² to 64². / 训练好的编码/解码器对；将 512² 压缩到 64²。 |
| Second stage | "The U-Net" | Diffusion model over the latent space. / 潜在空间上的扩散模型。 |
| CFG | "Guidance scale" / "引导缩放" | `(1+w)·ε_cond - w·ε_uncond`; tunes conditioning strength. / 调节条件化强度。 |
| Null token | "Empty prompt embed" / "空 prompt 嵌入" | Unconditional embed used for `ε_uncond`. / 用于无条件预测的嵌入。 |
| Cross-attention | "How text gets in" / "文本如何进入" | Each U-Net block attends to text tokens as K and V. / 每个 U-Net 块对文本 token 做注意力。 |
| DiT | "Diffusion Transformer" | Replace U-Net with a transformer over latent patches; scales better. / 用 Transformer 替代 U-Net。 |
| MMDiT | "Multi-modal DiT" / "多模态 DiT" | SD3's architecture: text and image streams with joint attention. / SD3 架构：文本和图像流的联合注意力。 |
| VAE scaling factor | "Magic number" / "魔数" | Divides latents by ~5.4 so diffusion operates in unit-variance space. / 除以约 5.4 使扩散在单位方差空间操作。 |

## Lưu ý sản xuất: chạy Flux-12B trên GPU tiêu dùng 8GB  Lưu ý sản xuất: trên GPU tiêu thụ 8GB  chạy Flux-12B

Liên kết Flux là công thức "Tôi có một GPU tiêu dùng, tôi có thể vận chuyển này không?"

> 参考流体集成是经典的"我只有消费级GPU,能部署吗?"方案──三旋方案:

1. **Staggered loading.**Flux có ba mạng không bao giờ cần phải tồn tại cùng nhau trong VRAM: T5-XXL mã hóa văn bản (~ 10 GB trong fp32), CLIP-L (còn nhỏ), 12B MMDiT và VAE. Mã hóa yêu cầu trước, * xóa * các mã hóa, tải DiT, từ chối, * xóa * DiT, tải VAE, giải mã. GPU 8GB tiêu dùng chỉ phù hợp với một giai đoạn tại một thời điểm.
   **交错加载。**Flux có 3 không cần phải cùng thời gian ở lại mạng VRAM. 编码提示 后删除编码器, tải DiT,去噪声后删除, tải VAE 解码.
2. **4-bit quantization via bitsandbytes.** `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)`trên cả mã hóa T5 và DiT. Giảm bộ nhớ 8x, giảm chất lượng không thể nhận thấy cho văn bản-đến hình ảnh theo các tiêu chuẩn của Aritra (được liên kết trong sổ ghi chép).
   **4 位量化。**T5 và DiT được định lượng lên 4 vị trí, bộ nhớ giảm 8 lần, chất lượng bị mất rất ít.
3. **CPU offload.** `pipe.enable_model_cpu_offload()`tự động đổi các mô-đun giữa CPU và GPU khi mỗi bước tiến tiến.
   **CPU 卸载。**Tự động chuyển đổi giữa CPU và GPU.

Việc ghi nhớ là: `10 GB T5 / 8 = 1.25 GB`được định lượng,`12 B params × 0.5 bytes = ~6 GB`TP=1 kết luận không có mô hình song song, lượng hóa tối đa. Đối với sản xuất bạn sẽ chạy TP=2 hoặc TP=4 trên H100s; cho một máy tính xách tay phát triển duy nhất, đây là công thức.

## Xem thêm 延伸阅读

- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) Sự pha trộn ổn định.
- [Podell et al. (2023). SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis](https://arxiv.org/abs/2307.01952) SDXL.
- [Peebles & Xie (2023). Scalable Diffusion Models with Transformers (DiT)](https://arxiv.org/abs/2212.09748) DiT.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) SD3, MMDiT.
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) CFG.
- [Labs (2024). Flux.1 — Black Forest Labs announcement](https://blackforestlabs.ai/announcing-black-forest-labs/) Gia đình Flux1.
- [Hugging Face Diffusers docs](https://huggingface.co/docs/diffusers/index) thực hiện tham chiếu cho mỗi điểm kiểm soát trên.
