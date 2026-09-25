# Mô hình phân phối  DDPM từ đầu   Mô hình mở rộng  Từ không thực hiện DDPM

> Ho, Jain, Abbeel (2020) đã cho lĩnh vực một công thức mà nó không thể ngừng. Hủy bỏ dữ liệu bằng tiếng ồn trên một ngàn bước nhỏ. Hướng dẫn một mạng lưới thần kinh để dự đoán tiếng ồn. đảo ngược quá trình khi suy luận. Ngày nay mọi hình ảnh, video, 3D và mô hình âm nhạc chính thống chạy trên vòng lặp này, có thể với các thủ thuật phù hợp hoặc phù hợp trên đầu.

> **【中文解读】**Phương pháp cốt lõi của DDPM: sử dụng 1000 bước từng bước để tăng dữ liệu làm phá vỡ dữ liệu, đào tạo một mạng lưới dự đoán tiếng ồn, đưa ra ý kiến ngược chiều loại bỏ tiếng ồn.

> **【拓展：扩散模型是当前 AI 生成的核心】**Stable Diffusion、DALL-E 3、Midjourney、Sora đều dựa trên mô hình phổ biến──DDPM chứng minh một mục tiêu giảm tiếng ồn đơn giản có thể tạo ra khả năng sản xuất đáng kinh ngạc──

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## Vấn đề  vấn đề giới thiệu

Anh muốn lấy mẫu cho `p_data(x)`. GANs chơi một trò chơi tối thiểu mà thường khác nhau. VAEs sản xuất các mẫu mờ từ một decoder Gaussian.`log p(x)`(vì vậy bạn có khả năng), và (c) các mẫu tương tự chất lượng SOTA.

> Anh muốn`p_data(x)`Trong khi đó, các nhà sản xuất của các máy tính có thể tìm thấy các sản phẩm khác nhau trong các máy tính.`log p(x)`样本质量匹配 SOTA──

Sohl-Dickstein et al. (2015) đã có một câu trả lời lý thuyết: xác định một chuỗi Markov `q(x_t | x_{t-1})`Điều này dần dần thêm tiếng ồn Gaussian, và đào tạo một chuỗi ngược.`p_θ(x_{t-1} | x_t)`Ho, Jain, Abbeel (2020) cho thấy mất mát có thể được đơn giản hóa thành một dòng  dự đoán tiếng  và làm sạch toán học.

> Sohl-Dickstein (2015) đã đưa ra câu trả lời lý thuyết: định nghĩa chuỗi Markov của tiếng ồn tăng dần, đào tạo chống lại chuỗi để gây ồn đi. Ho ỹng (2020) sẽ giảm thiểu đơn giản hóa thành một dòng  dự đoán tiếng ồn. Năm 2020 là một điều mới lạ, năm 2021 sản xuất mẫu SOTA, năm 2022 trở thành Phân phối ổn định, năm 26 nó là cơ sở hạ tầng.

> **【中文解读】**DDPM's three-step process:(1) 前向过程逐步增加噪音直到数据变为纯噪音;(2) 训练学习网络预测每一步增加噪音;(3) 反向过程从纯噪音开始逐步到噪音,恢复到真实数据──损失函数简化为"预测噪音"

> **【拓展：从 DDPM 到实用扩散模型】**DDPM 原始论文在像素空间操作,速度慢(需要1000步去噪音) ;;三个关键改进使其成为实用工具:(1) DDIM(2020) sẽ采样步数从1000 降到20-50;(2) 潜在扩散(2021,Rombach) 在 VAE 潜在空间中操作,大幅降低计算量;(3) CFG(Classifier-Free Guidance,2022) 通过条件/无条件预测的差提升生成质量;;

## Khái niệm cốt lõi

![DDPM: forward noise, reverse denoise](../assets/ddpm.svg)

**Forward process `q`.**Thêm tiếng ồn Gaussian vào `T`Các bước nhỏ. hình thức đóng  lý do toán học có thể xử lý  là bước tích lũy cũng là Gaussian:

> **前向过程 `q`。**Trong `T`Các bước nhỏ trong bước tăng lên tiếng ồn cao.

```
q(x_t | x_0) = N( sqrt(α̅_t) · x_0,  (1 - α̅_t) · I )
```

nơi `α̅_t = ∏_{s=1..t} (1 - β_s)`cho một lịch trình của `β_t`- Chọn`β_t`từ 1e-4 đến 0,02 theo đường thẳng trên T=1000 bước và`x_T`là khoảng `N(0, I)`- Tôi không biết.

> Trong số đó `α̅_t = ∏_{s=1..t} (1 - β_s)`将 `β_t`Từ 1e-4 đến 0,02 线性排列 T=1000 步,`x_T`gần như`N(0, I)`

**Reverse process `p_θ`.**Học một mạng lưới thần kinh`ε_θ(x_t, t)`Điều này dự đoán về tiếng ồn đã được thêm vào.`x_t`, chỉ định bằng:

> **反向过程 `p_θ`。**Học một mạng thần kinh`ε_θ(x_t, t)`预测添加的噪音──给定 `x_t`,去噪音方式为:

```
x_{t-1} = (1 / sqrt(α_t)) · ( x_t - (β_t / sqrt(1 - α̅_t)) · ε_θ(x_t, t) )  +  σ_t · z
```

nơi `σ_t`là hoặc `sqrt(β_t)`hoặc một sự khác biệt học.`x_{t-1}`vì phía sau `q(x_{t-1} | x_t, x_0)`và thay thế `x_0`với ước tính dự đoán về tiếng ồn của nó.

> Trong số đó `σ_t` `sqrt(β_t)`Hoặc học đến cách khác biệt.`q(x_{t-1} | x_t, x_0)`求解 `x_{t-1}`

**Training loss.**

```
L_simple = E_{x_0, t, ε} [ || ε - ε_θ( sqrt(α̅_t) · x_0 + sqrt(1 - α̅_t) · ε,  t ) ||² ]
```

Mô hình `x_0`từ dữ liệu, chọn một số ngẫu nhiên `t`, mẫu `ε ~ N(0, I)`, tính toán tiếng ồn ồn ồn ồn ồn`x_t`Một lần bắn qua hình thức đóng, và lùi lại tiếng ồn.

> Từ dữ liệu`x_0`, tự chọn`t`, như vậy`ε ~ N(0, I)`, qua một lần tính toán có tiếng ồn`x_t`, đối với tiếng ồn làm trở lại.

**Sampling.**Bắt đầu`x_T ~ N(0, I)`. Lặp lại bước ngược từ `t = T`đến`1`- Được rồi.

> **采样。**Từ `x_T ~ N(0, I)`开始,从 `t = T`Đến`1`代反向步骤──完成──

## Tại sao nó hoạt động? Tại sao nó hiệu quả?

Ba cảm giác:

> 3 trực giác:

1. **Denoising is easy; generating is hard.**Tại `t=T`, dữ liệu là tiếng ồn thuần túy  mạng phải giải quyết một vấn đề tầm thường.`t=0`, mạng chỉ cần làm sạch một vài pixel.`t`, vấn đề là khó khăn nhưng mạng có nhiều gradient chảy qua cùng một trọng lượng từ mọi mức tiếng ồn.
   **去噪容易，生成难。**Trong `t=T`Khi, dữ liệu là tiếng ồn đơn giản, mạng chỉ cần giải quyết một vấn đề đơn giản.`t=0`时, mạng chỉ cần dọn dẹp một lượng nhỏ các hình ảnh.

2. **Score matching in disguise.**Vincent (2011) chứng minh rằng dự đoán tiếng ồn tương đương với ước tính `∇_x log q(x_t | x_0)`, điểm * điểm*. SDE ngược sử dụng điểm này để đi lên độ d density gradient  một bước ngẫu nhiên hướng về các vùng có khả năng cao.
   **伪装的分数匹配。**预测 tiếng ồn bằng giá tính toán`∇_x log q(x_t | x_0)`❖ ngược SDE sử dụng số này dọc theo độ mật độ thang lên ❖

3. **The ELBO reduces to simple MSE.**Các biến động bên dưới hoàn toàn có một thuật ngữ KL mỗi bước thời gian. Với các tham số của DDPM các thuật ngữ KL đơn giản hóa cho MSE về dự đoán tiếng ồn với các hệ số cụ thể; Ho giảm các hệ số (chẳng định nó là "simple" mất mát) và chất lượng * cải thiện*.
   **ELBO 简化为简单 MSE。**完整的变分下界 每个时间步骤都有 KL 项――Ho 丢弃系数后质量反而*提升*了――

## Hãy xây dựng nó.
```figure
diffusion-denoise
```

## Hãy xây dựng nó

`code/main.py`thực hiện một DDPM 1D. Dữ liệu là một hỗn hợp hai chế độ. "Net" là một MLP nhỏ mà mất`(x_t, t)`và các kết quả dự đoán tiếng ồn. đào tạo là mất một dòng. lấy mẫu lặp lại chuỗi ngược.

> `code/main.py`实现一维 DDPM──数据是双峰混合──"网络" là một mô hình MLP nhỏ, nhận `(x_t, t)`输出预测噪音──训练就是那一行损失──采样代反向链──

### Bước 1: lịch trình tiến hành (mẫu đóng)

```python
betas = [1e-4 + (0.02 - 1e-4) * t / (T - 1) for t in range(T)]
alphas = [1 - b for b in betas]
alpha_bars = []
cum = 1.0
for a in alphas:
    cum *= a
    alpha_bars.append(cum)
```

### Bước 2: mẫu`x_t`trong một cú bắn

```python
def forward_sample(x0, t, alpha_bars, rng):
    a_bar = alpha_bars[t]
    eps = rng.gauss(0, 1)
    x_t = math.sqrt(a_bar) * x0 + math.sqrt(1 - a_bar) * eps
    return x_t, eps
```

### Bước 3: một bước đào tạo

```python
def train_step(x0, model, alpha_bars, rng):
    t = rng.randrange(T)
    x_t, eps = forward_sample(x0, t, alpha_bars, rng)
    eps_hat = model_forward(model, x_t, t)
    loss = (eps - eps_hat) ** 2
    return loss, gradient_step(model, ...)
```

### Bước 4: lấy mẫu ngược

```python
def sample(model, alpha_bars, T, rng):
    x = rng.gauss(0, 1)
    for t in range(T - 1, -1, -1):
        eps_hat = model_forward(model, x, t)
        beta_t = 1 - alphas[t]
        x = (x - beta_t / math.sqrt(1 - alpha_bars[t]) * eps_hat) / math.sqrt(alphas[t])
        if t > 0:
            x += math.sqrt(beta_t) * rng.gauss(0, 1)
    return x
```

Đối với một vấn đề 1-D với 40 bước thời gian và 24 đơn vị MLP, điều này học được hỗn hợp hai chế độ trong ~ 200 thời đại.

> Đối với 40 bước thời gian và 24 đơn vị MLP, khoảng 200 vòng có thể học được hai đỉnh hỗn hợp.

## Thời gian điều kiện.

Mạng cần biết nó đang chỉ ra thời gian nào.

> 网络 cần biết nó đang trong giai đoạn nào.

- **Sinusoidal embedding.**Giống như Transformer định vị mã hóa.`embed(t) = [sin(t/ω_0), cos(t/ω_0), sin(t/ω_1), ...]`- Đi qua một MLP, phát sóng lên mạng.
  **正弦嵌入。**类似Tranformator 位置编码──
- **Film / group-norm conditioning.**Dự án tích hợp theo quy mô/chânal (FiLM) tại mỗi khối.
  **FiLM / 组归一化条件化。**sẽ được cài đặt chiếu cho mỗi đường dẫn

Mã đồ chơi của chúng tôi sử dụng sinusoidal → concat.

> Chúng tôi có thể làm việc với các máy tính.

## # Thói bẫy #

- **Schedule matters a lot.**Đường thẳng`β`là DDPM mặc định nhưng lịch trình cosine (Nichol & Dhariwal, 2021) cung cấp FID tốt hơn cho cùng một tính toán.
  **调度很重要。**线性 `β`DDPM 默认但余弦调度在相同计算量下 FID 更好──
- **Timestep embedding is fragile.**Tới qua .`t`như một float hoạt động cho đồ chơi 1-D nhưng thất bại cho hình ảnh; luôn sử dụng một nhúng đúng.
  **时间步嵌入脆弱。**原始 `t`浮点数在玩具 1D 可用但图像不行──
- **V-prediction vs ε-prediction.**Đối với các chế độ hẹp (t rất nhỏ hoặc rất lớn), `ε`có tín hiệu-đồn kém.`v = α·ε - σ·x`) ổn định hơn; SDXL, SD3 và Flux sử dụng nó.
  **V 预测 vs ε 预测。**Trong thời gian cực kỳ, V 预测更稳定;SDXL、SD3、Flux sử dụng nó。
- **Classifier-free guidance.**Khi suy luận, tính toán cả điều kiện và vô điều kiện `ε`, sau đó `ε_cfg = (1 + w) · ε_cond - w · ε_uncond`với `w ≈ 3-7`- Được đề cập trong Bài học 8.
  **无分类器引导。**推理时计算条件和无条件预测的差值──第 08 课详述──
- **1000 steps is a lot.**Việc sản xuất sử dụng DDIM (20-50 bước), DPM-Solver (10-20 bước) hoặc chưng cất (1-4 bước).
  **1000 步太多了。**生产用 DDIM(20-50 步)、DPM-Solver(10-20 步) hoặc蒸(1-4 步)。

## Hãy sử dụng nó để thực hiện

| Role / 角色 | Typical stack in 2026 / 2026 典型技术栈 |
|------|-----------------------|
| Image pixel-space diffusion (small, toy) / 像素空间扩散 | DDPM + U-Net |
| Image latent diffusion / 潜在扩散 | VAE encoder + U-Net or DiT (Lesson 07) |
| Video latent diffusion / 视频潜在扩散 | Spatiotemporal DiT (Sora, Veo, WAN) |
| Audio latent diffusion / 音频潜在扩散 | Encodec + diffusion transformer |
| Science (molecules, proteins, physics) / 科学 | Equivariant diffusion (EDM, RFdiffusion, AlphaFold3) |

Sự pha trộn là xương sống tạo ra phổ quát. Sự phù hợp dòng chảy (Dạy học 13) là đối thủ cạnh tranh 2024-2026 thường chiến thắng trên tốc độ suy luận cho chất lượng tương tự.

> 扩散是通用生成骨干;;Flow Matching (第 13 课) là đối thủ cạnh tranh của 2024-2026, thường suy luận nhanh hơn dưới cùng chất lượng.

## Chuyển nó đi.

- Cứu lại`outputs/skill-diffusion-trainer.md`. Skill lấy một bộ dữ liệu + ngân sách tính toán và đầu ra: lịch trình (lín/cosine/sigmoid), mục tiêu dự đoán (ε/v/x), số bước, quy mô hướng dẫn, gia đình mẫu và một giao thức đánh giá.

> 保存 `outputs/skill-diffusion-trainer.md` Khả năng nhận dữ liệu + tính toán ngân sách, xuất khẩu điều chỉnh, dự đoán mục tiêu, bước số, hướng dẫn quy mô, thu thập dữ liệu và thỏa thuận đánh giá.

## Tập luyện bài tập

1. **Easy / 简单.**Thay đổi T từ 40 lên 10 trong `code/main.py`. Làm thế nào chất lượng mẫu (histogram hình ảnh của các sản phẩm) suy giảm?
   T từ 40  đổi thành 10 ∙ chất lượng mẫu làm thế nào giảm?
2. **Medium / 中等.**Chuyển từ dự đoán ε sang dự đoán v. Lấy lại bước ngược. So sánh chất lượng mẫu cuối cùng.
   Từ ε 预测切换到 v 预测。重新推导反向步骤──比较最终样本质量──
3. **Hard / 困难.**Thêm hướng dẫn không có phân loại.`c ∈ {0, 1}`, giảm nó 10% thời gian trong quá trình đào tạo, và trong thời gian lấy mẫu sử dụng `ε = (1+w)·ε_cond - w·ε_uncond`- đo tỷ lệ bị ảnh hưởng theo chế độ điều kiện ở `w = 0, 1, 3, 7`- Tôi không biết.
   添加无分类器引导──测量 `w = 0, 1, 3, 7`时的条件模式命中率──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Forward process | "Adding noise" / "加噪" | Fixed Markov chain `q(x_t \| x_{t-1})` that destroys the data. / 破坏数据的固定马尔可夫链。 |
| Reverse process | "Denoising" / "去噪" | Learned chain `p_θ(x_{t-1} \| x_t)` that reconstructs the data. / 重建数据的学习链。 |
| β schedule | "The noise ladder" / "噪声阶梯" | Per-step variance; linear, cosine, or sigmoid. / 每步方差；线性、余弦或 S 形。 |
| α̅ | "Alpha bar" | Cumulative product `∏(1 - β)`; gives closed-form `x_t` from `x_0`. / 累积乘积，给出闭式 `x_t`。 |
| Simple loss | "MSE on noise" / "噪声 MSE" | `\|\|ε - ε_θ(x_t, t)\|\|²`; all variational derivations collapse to this. / 所有变分推导最终坍塌为此。 |
| ε-prediction | "Predict noise" / "预测噪声" | Output is the noise added; standard DDPM. / 输出是添加的噪声。 |
| V-prediction | "Predict velocity" / "预测速度" | Output is `α·ε - σ·x`; better conditioning across t. / 跨时间步条件化更好。 |
| DDPM | "The paper" / "那篇论文" | Ho et al. 2020; linear β, 1000 steps, U-Net. |
| DDIM | "Deterministic sampler" / "确定性采样器" | Non-Markov sampler, 20-50 steps, same training objective. / 非马尔可夫采样器。 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional noise predictions to amplify conditioning. / 混合条件和无条件预测以放大条件化。 |

## Lưu ý sản xuất: suy luận phân tán là một vấn đề đếm từng bước.

Bảng DDPM chạy các bước ngược T=1000. Không ai đưa ra trong sản xuất. Mỗi đống suy luận thực sự chọn một trong ba chiến lược  và mỗi bản đồ sạch sẽ đến khung sản xuất của "tạm thời đến từ đâu":

> DDPM 论文 sử dụng T=1000 ngược向步──生产中没有人这样做──每种策略对应生产中"延迟来自哪里":

1. **Faster sampler, same model.**DDIM (20-50 bước), DPM-Solver++ (10-20), UniPC (8-16).`ε_θ`- Cắt độ trễ 20 đến 50 lần.
   **更快的采样器，相同模型。**DDIM、DPM-Solver++、UniPC──即插即用替换反向循环,降低延迟 20-50倍──
2. **Distillation.**Căn nuôi học sinh để phù hợp với giáo viên trong ít bước: Phân phối tiến bộ (2 → 1), Mô hình nhất quán (tự nguyện → 1-4), LCM, SDXL-Turbo, SD3-Turbo. Giảm độ trễ thêm 5-10x, đòi hỏi phải tái đào tạo.
   **蒸馏。**训练学生模型在更少步数匹配教师──再降延迟 5-10 倍,需要重训──
3. **Caching and compilation.** `torch.compile(unet, mode="reduce-overhead")`, các hậu cảnh phân tán của TensorRT-LLM,`xformers`/SDPA chú ý, bf16 trọng lượng. Giảm độ trễ mỗi bước ~ 2x.
   **缓存和编译。**Torch.compile、TensorRT、xformers、bf16──降低每步延迟约2倍──

Đối với một máy chủ truyền tải sản xuất, cuộc trò chuyện về ngân sách giống như văn học sản xuất mô tả cho LLM: độ trễ là `num_steps × step_cost + VAE_decode`, thông qua là `batch_size × (num_steps × step_cost)^-1`TTFT là nhỏ (một bước); TPOT tương đương với thời gian phản ứng đầy đủ vì việc tạo hình ảnh là "tất cả một lần" từ quan điểm của người dùng.

> 生产扩散服务器的预算对话与 LLM 相同:延迟 = `num_steps × step_cost + VAE_decode`△TTFT 很小(一步);TPOT 等价物是完整响应时间──

## Xem thêm 延伸阅读

- [Sohl-Dickstein et al. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://arxiv.org/abs/1503.03585) giấy truyền, trước thời gian của nó.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) DDPM.
- [Song, Meng, Ermon (2021). Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502) DDIM, ít bước hơn.
- [Nichol & Dhariwal (2021). Improved DDPM](https://arxiv.org/abs/2102.09672) lịch trình cosine, học biến.
- [Dhariwal & Nichol (2021). Diffusion Models Beat GANs on Image Synthesis](https://arxiv.org/abs/2105.05233) hướng dẫn về phân loại.
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) CFG.
- [Karras et al. (2022). Elucidating the Design Space of Diffusion-Based Generative Models (EDM)](https://arxiv.org/abs/2206.00364) ghi chú thống nhất, công thức sạch nhất.
