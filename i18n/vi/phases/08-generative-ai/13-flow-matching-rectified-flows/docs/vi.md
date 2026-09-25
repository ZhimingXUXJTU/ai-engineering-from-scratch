# Tỷ lệ lưu lượng phù hợp & Tỷ lệ lưu lượng sửa đổi

> Các mô hình phân phối thực hiện các bước lấy mẫu 20-50 bởi vì chúng đi theo một con đường cong từ tiếng ồn đến dữ liệu. Sự phù hợp dòng chảy (Lipman et al., 2023) và dòng chảy chỉnh sửa (Liu et al., 2022) được đào tạo bằng các con đường thẳng. Các con đường thẳng hơn có nghĩa là ít bước hơn có nghĩa là suy luận nhanh hơn. Stable Diffusion 3, Flux.1, và AudioCraft 2 tất cả chuyển sang sự phù hợp dòng chảy vào năm 2024.

> **【中文解读】**扩散模型需要 20-50 步采样因为走的是曲路径──Flow Matching 和 Rectified Flow 训练直线路径更直的路径意味着更少步数和更快的推理──SD3、FLUX.1、AudioCraft 2 都在2024年转换到Flow Matching──

> **【拓展：Flow Matching 是 2024-2026 的趋势】**Flow Matching đang thay thế quy định phổ biến truyền thống trở thành tiêu chuẩn của mô hình sản xuất thế hệ mới. Nó được phép toán học tốt hơn, hiệu quả hơn trên thực nghiệm.

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 06 (DDPM), Phase 1 · Calculus / 微积分 | **前置知识:** 阶段 8 · 06（DDPM），阶段 1 · 微积分
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Quá trình ngược của DDPM là một bước đi stochastic 1000 bước từ `N(0, I)`DDIM đã phá vỡ nó thành 20-50 bước xác định. Bạn muốn ít hơn các bước  lý tưởng là một.

> Quá trình ngược của DDPM là từ`N(0, I)`Trở lại 1000 bước phân phối dữ liệu theo thời gian. DIM sẽ thu nhỏ nó xuống còn 20-50 bước. Bạn muốn ít hơn một bước.

Nếu bạn có thể đào tạo mô hình như vậy rằng con đường từ tiếng ồn đến dữ liệu là một đường thẳng, một bước đơn giản của Euler từ `t=1`đến`t=0`sẽ hoạt động. Tích hợp dòng chảy xây dựng điều này trực tiếp: xác định một sự phân cực thẳng từ`x_1 ∼ N(0, I)`đến`x_0 ∼ data`, tập hợp một trường vector `v_θ(x, t)`để phù hợp với phái sinh thời gian của nó, tích hợp khi suy luận.

> Nếu mô hình đào tạo làm cho tiếng ồn đến dữ liệu đường dẫn là * đường thẳng*, bước từ `t=1`Đến`t=0`Đủ rồi. Tích hợp dòng chảy trực tiếp xây dựng: định nghĩa`x_1 ∼ N(0, I)`Đến`x_0 ∼ data`                                                                                                                                                                                                                                                              `v_θ(x, t)`匹配时间导数──

Phong trào sửa đổi (Liu 2022) đi xa hơn: lặp đi lặp lại khớp các con đường bằng một thủ tục tái lưu dẫn đến một ODE dần gần hơn đến tuyến tính. Sau hai lần tái lưu, một mẫu 2 bước phù hợp với chất lượng DDPM 50 bước.

> Phòng chảy sửa đổi (Reflow) (Third: 2022): 通过 reflow 过程代拉直路径──两次 reflow 代后,2 步采器匹配 50 步 DDPM质量──

> **【中文解读】**Các mô hình thông tin được chỉnh sửa để có thể kết hợp với các mô hình thông tin được chỉnh sửa để có thể kết hợp với các mô hình thông tin được chỉnh sửa.

> **【拓展：FLUX.1 的 Flow Matching 实现】**FLUX.1 của Black Forest Labs được tạo ra bởi Stable Diffusion (được tạo ra bởi các nhà sản xuất) sử dụng Flow Matching thay thế truyền thống mở rộng điều chỉnh, cộng tác với MMDiT (MDF) cấu trúc, trên chất lượng hình ảnh và tốc độ tạo đều rõ ràng hơn SDXL.

## Khái niệm cốt lõi

![Flow matching: straight-line interpolation between noise and data](../assets/flow-matching.svg)

### Dòng chảy thẳng

Định nghĩa:

> 定义:

```
x_t = t · x_1 + (1 - t) · x_0,   t ∈ [0, 1]
```

nơi `x_0 ~ data`và `x_1 ~ N(0, I)`. Tiến dẫn thời gian dọc theo đường thẳng này là không đổi:

> Trong số đó `x_0 ~ data`- Tôi không biết.`x_1 ~ N(0, I)`                                                                                                                                                                                                                                                              

```
dx_t / dt = x_1 - x_0
```

Định nghĩa một trường vector thần kinh `v_θ(x_t, t)`và đào tạo nó để phù hợp với phái sinh này:

> 定义神经向量场 `v_θ(x_t, t)`, tập hợp nó phù hợp với số này:

```
L = E_{x_0, x_1, t} || v_θ(x_t, t) - (x_1 - x_0) ||²
```

Đây là **conditional flow matching**Lỗ tập không có mô phỏng: bạn không bao giờ mở ODE. Chỉ cần lấy mẫu`(x_0, x_1, t)`và lùi lại.

> Đó là điều đó.**条件 Flow Matching**损失(Lipman 2023) ―― 训练是无模拟的:你永远不需要展开 ODE――只需要采样`(x_0, x_1, t)`Và làm trở lại là có thể.

### Chọn mẫu

Khi suy luận, tích hợp trường vector học * trở lại* trong thời gian:

> 推理时,将学到的量场沿时间*反向*积分:

```
x_{t-Δt} = x_t - Δt · v_θ(x_t, t)
```

Bắt đầu từ `x_1 ~ N(0, I)`, bước Euler xuống `t=0`- Tôi không biết.

> Từ `x_1 ~ N(0, I)` bắt đầu, dùng Euler  bước tiến xuống `t=0`

### Chuyển tiếp (Liu 2022) 整流流(Liu 2022)

dòng chảy thẳng hoạt động nhưng các con đường học được không thực sự thẳng`x_0`s có thể lập bản đồ cho cùng `x_1`. bước tái lưu của dòng chảy được sửa chữa:

> Đường thẳng tuy có hiệu quả, nhưng cách học thực sự không thực sự là thẳng vì nhiều.`x_0`Có thể chiếu đến cùng một `x_1`,路径会曲──Tình thức sửa đổi dòng chảy của dòng chảy 步骤:

1. Mô hình dòng tàu v_1 với kết hợp ngẫu nhiên.
   Uzz随机配对训练 Flow 模型 v_1──
2. Mô hình N cặp `(x_1, x_0)`bằng cách tích hợp v_1 từ `x_1`đến khi hạ cánh `x_0`- Tôi không biết.
   通过将 v_1 từ `x_1`积分到落点 `x_0`采样 N đối với `(x_1, x_0)`
3. Cụ thể v_2 trên những ví dụ cặp. Bởi vì cặp hiện nay là "ODE-tích hợp", interpolant thẳng giữa chúng thực sự phẳng hơn.
   Trong các mô hình đối tác này, tập luyện v_2── vì đối tác hiện tại là "ODE 匹配", giá trị giao dịch trực tiếp giữa chúng thực sự đơn giản hơn──
4. Lặp lại.
   Đổi lại

Trong thực tế, 2 lặp lại tái lưu đưa bạn đến gần tuyến tính, cho phép suy luận 2-4 bước. SDXL-Turbo, SD3-Turbo, LCM đều là mô hình khâu khâu từ dòng chảy phù hợp.

> Thực tế 2 lần reflow 代就能使路径接近线性,从而支持 2-4 步推理──SDXL-Turbo、SD3-Turbo、LCM đều dựa trên mô hình Flow Matching 蒸出──

### Tại sao điều này giành chiến thắng cho hình ảnh vào năm 2024 Tại sao 2024 năm hình ảnh sản xuất chuyển sang dòng chảy phù hợp

Ba lý do:

> Ba lý do:

1. **Simulation-free training** không có ODE được thả ra trong quá trình đào tạo, không cần thiết để thực hiện.
   **无需仿真的训练** training时无需展开 ODE, thực hiện rất đơn giản.
2. **Better loss geometry** Các đường thẳng có tín hiệu-xồn nhất quán, trong khi DDPM ε-loss có SNR xấu ở các cạnh lịch trình.
   **更优的损失几何** đường thẳng                                                                                                                                                                                                                                                             
3. **Faster inference** 4-8 bước ở chất lượng SDXL-Turbo; 1 bước với chưng cất phù hợp.
   **更快的推理**4-8 bước đạt được chất lượng SDXL-Turbo; hợp tác kết hợp

## Tương ứng dòng chảy vs DDPM  kết nối chính xác  Tương ứng dòng chảy vs DDPM  精确联系

Tương thích dòng chảy với một con đường Gaussian-conditional là phân tán *with a specific noise schedule*.`x_t = α(t) x_0 + σ(t) x_1`thời gian và dòng chảy phù hợp phục hồi Stratonovich-reformed phân tán với `v = α'·x_0 - σ'·x_1`Hai con đường này là tương đương với đường dẫn Gaussian.

> Sử dụng High-Condition Pathways Flow Matching thực tế là mô hình phổ biến có độ ưa chuộng tiếng ồn cụ thể.`x_t = α(t) x_0 + σ(t) x_1`调度后,Flow Matching còn được tạo ra để mở rộng lại trong hình thức của Stratonovich, trong đó `v = α'·x_0 - σ'·x_1` Đối với đường cao, hai trong số các giá trên cùng 

Những gì phù hợp dòng chảy đã thêm vào: độ rõ ràng của mục tiêu (một tốc độ đơn giản), một mất mát sạch hơn, và giấy phép để thử nghiệm với các chất can thiệp không Gaussian.

> Sự đóng góp thực sự của Flow Matching là: mục tiêu của * độ rõ ràng *(một tốc độ bình thường của chiều hướng) 、 hơn sạch của mất mát, cũng như cố gắng không cao hơn của tự do đính vào giá trị.

## Hãy xây dựng nó.
```figure
normalizing-flow
```

## Hãy xây dựng nó

`code/main.py`thực hiện sự phù hợp dòng chảy 1-D trên một hỗn hợp Gaussian hai chế độ.`v_θ(x, t)`là một MLP nhỏ được đào tạo với mục tiêu thẳng. Khi suy luận, tích hợp 1, 2, 4 và 20 bước của Euler và so sánh chất lượng mẫu.

> `code/main.py`Trong phân bố hỗn hợp hai đỉnh cao thực hiện 1D Flow Matching.`v_θ(x, t)`là một MLP kiểu nhỏ, sử dụng đào tạo mục tiêu trực tuyến.

### Bước 1: mất tập luyện Bước 1: mất tập luyện

```python
def train_step(x0, net, rng, lr):
    x1 = rng.gauss(0, 1)
    t = rng.random()
    x_t = t * x1 + (1 - t) * x0
    target = x1 - x0
    pred = net_forward(x_t, t)
    loss = (pred - target) ** 2
    # backprop + update
```

> 训练损失: 采样噪音 `x1`和 thời gian `t`, cấu trúc giá trị`x_t`, mục tiêu`x1 - x0`,做平方回归──

### Bước 2: Kết luận đa bước Bước 2: nhiều bước

```python
def sample(net, num_steps):
    x = rng.gauss(0, 1)
    for i in range(num_steps):
        t = 1.0 - i / num_steps
        dt = 1.0 / num_steps
        x -= dt * net_forward(x, t)
    return x
```

> Nhiều bước: từ tiếng ồn cao lên, theo bước dài ngược chiều积分── số bước càng nhiều kết quả càng chính xác, nhưng chậm lại càng cao──

### Bước 3: So sánh số bước.

Hi vọng mẫu 4 bước sẽ phù hợp với chất lượng 20 bước  một vấn đề lớn cho thời gian trễ.

> 4 bước lấy thiết bị nên đã phù hợp với 20 bước chất lượng.

## # Thói bẫy #

- **Time parameterization.**Sử dụng phù hợp dòng chảy `t ∈ [0, 1]`với `t=0`trong dữ liệu, `t=1`DDPM sử dụng `t ∈ [0, T]`với `t=0`trong dữ liệu, `t=T`cùng hướng, khác nhau quy mô, báo cáo luôn sai lầm.
  时间参数化: Tốc độ tương ứng `t ∈ [0, 1]`- Tôi không biết.`t=0`Trong dữ liệu,`t=1`Trong tiếng ồn; DDPM sử dụng `t ∈ [0, T]`, hướng giống nhau nhưng kích thước khác nhau.
- **Schedule choice.**Dòng thẳng của dòng chảy được sửa là "the" dòng chảy phù hợp lịch trình, nhưng bạn có thể sử dụng cosine hoặc logit-normal t-sampling (SD3 làm điều này) để bao phủ quy mô tốt hơn.
  调度选择:直线 của Corrected Flow là " tiêu chuẩn " của Flow Matching 调度, nhưng có thể sử dụng cosine hoặc logic-normal của t 采样(SD3 là làm như vậy) để có được một quy mô tốt hơn bao phủ.
- **Reflow cost.**Tạo bộ dữ liệu kết hợp để tái lưu là một thông qua suy luận đầy đủ cho mỗi mẫu. Chỉ làm tái lưu khi bạn thực sự cần suy luận 1-2 bước.
  Reflow 成本: tạo reflow 配对数据集需要每样本一次完整推理──只有真正需要1-2步推理时才做 reflow──
- **Classifier-free guidance still applies.**Chỉ cần thay ε cho v trong kết hợp tuyến tính: `v_cfg = (1+w) v_cond - w v_uncond`- Tôi không biết.
  Hướng dẫn không phân loại vẫn áp dụng: chỉ cần đưa trong bộ phận liên kết ε 换 thành v:`v_cfg = (1+w) v_cond - w v_uncond`

## Hãy sử dụng nó để thực hiện

| Use case / 用途 | 2026 stack / 2026 技术栈 |
|----------|-----------|
| Text-to-image, best quality / 最佳质量文生图 | Flow matching: SD3, Flux.1-dev |
| Text-to-image, 1-4 steps / 1-4 步文生图 | Distilled flow matching: Flux.1-schnell, SD3-Turbo, SDXL-Turbo |
| Real-time inference / 实时推理 | Consistency distillation from a flow-matched base (LCM, PCM) |
| Audio generation / 音频生成 | Flow matching: Stable Audio 2.5, AudioCraft 2 |
| Video generation / 视频生成 | Flow matching mixed with diffusion (Sora, Veo, Stable Video) |
| Science / physics / 科学/物理 | Flow matching + equivariant vector field |

Bất cứ khi nào một bài báo nói "quá nhanh hơn sự pha trộn" trong năm 2025-2026, nó gần như luôn luôn là dòng chảy phù hợp + chưng cất.

> Khi bài viết nói "Bí thuở nhanh hơn" thì, gần như luôn là Flow Matching + 蒸。

## Chuyển nó đi.

- Cứu lại`outputs/skill-fm-tuner.md`. Skill lấy một mô hình mô hình kiểu phân tán và chuyển đổi nó thành một cấu hình đào tạo phù hợp với dòng chảy: lựa chọn lịch trình, phân phối mẫu thời gian (tương đồng / logit- bình thường), tối ưu, kế hoạch tái lưu, con số bước mục tiêu, giao thức đánh giá.

> 保存为 `outputs/skill-fm-tuner.md` Chọn kỹ năng này nhận được một quy định mô hình mở rộng, chuyển đổi thành Flow Matching 训练配置:调度选择、时间采样分布(uniform / logit-normal) ✓优化器、reflow 计划、目标步数、评估协议。

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`và so sánh 1 bước vs 20 bước MSE vs phân phối dữ liệu thực.
   **简单。**运行 `code/main.py`, so sánh 1 bước và 20 bước so với phân phối dữ liệu thực MSE 
2. **Medium.**Thay đổi đồng phục`t`lấy mẫu thành logit-normal (đồng độ lấy mẫu ở giữa t).
   **中等。**sẽ trung bình`t`采样切换为 logit-normal(集中在中间 t 附近采样) ――模型质量是否提升?
3. **Hard.**Thực hiện một lần lặp lại: tạo cặp (x_0, x_1) bằng cách tích hợp mô hình đầu tiên, đào tạo mô hình thứ hai trên các cặp, và so sánh chất lượng mẫu 1 bước.
   **困难。**实现一次反流 代:通过对对对 (x_0, x_1),在对对上训练第二模型,并比较 1 步采样质量.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Flow matching | "Straight-line diffusion" | Train `v_θ(x, t)` to match `x_1 - x_0` along an interpolant. |
| Rectified flow | "Reflow" | Iterative procedure that straightens learned flows. |
| Velocity field | "v_θ" | Output of the model — the direction to move `x_t`. |
| Straight-line interpolant | "The path" | `x_t = (1-t)·x_0 + t·x_1`; trivial target derivative. |
| Euler sampler | "1st order ODE solver" | Simplest integrator; works well when paths are straight. |
| Logit-normal t | "SD3 sampling" | Concentrate `t` sampling toward mid-values where gradients are strongest. |
| Consistency distillation | "1-step sampler" | Train a student to map any `x_t` directly to `x_0`. |
| CFG with velocity | "v-CFG" | `v_cfg = (1+w) v_cond - w v_uncond`; same trick, new variable. |

## Lưu ý sản xuất: Flux.1-schnell là dòng chảy phù hợp với tốc độ nhanh nhất của nó

Chiến thắng sản xuất của Flow matching là Flux.1-schnell  một DiT phù hợp với dòng chảy được chưng cất đến 1-4 bước suy luận trong khi vẫn giữ chất lượng cấp độ Flux-dev. sổ ghi chép "Run Flux trên một máy 8GB" của Niels là công thức triển khai tham khảo: T5 + CLIP mã hóa, định nghĩa MMDiT định lượng (trong 4 bước cho nhanh vs 50 cho dev), VAE mã hóa.

> Flow Matching trong sản xuất là Flux.1-schnell một蒸t đến 1-4 步推理、 giữ Flux-dev 级质量的 Flow-Matched DiT。 Niels's "Flow Matching trên 8GB 机器运行Flux" notebook là tham khảo triển khai方案:T5 + CLIP 编码、量化MMDiT 去噪音(schnell 4 步 vs dev 50 步)、VAE 解码──成本核算:

| Variant | Steps | Latency at 1024² on L4 | Total FLOPs (relative) |
|---------|-------|------------------------|------------------------|
| Flux.1-dev (raw) | 50 | ~15 s | 1.0× |
| Flux.1-schnell | 4 | ~1.2 s | 0.08× (12× faster) |
| SDXL-base | 30 | ~4 s | 0.25× |
| SDXL-Lightning 2-step | 2 | ~0.3 s | 0.03× |

Quy tắc sản xuất: **flow-matched base + distillation = the 2026 default for fast text-to-image.**Mỗi nhà cung cấp lớn đều cung cấp bộ kết hợp này: SD3-Turbo (SD3 + dòng chảy + chưng cất), Flux-schnell (Flux-dev + chỉnh dòng chảy), CogView-4-Flash.

> Quy tắc sinh sản:**Flow-Matched 基座 + 蒸馏 = 2026 年快速文生图的默认方案。**Mỗi nhà sản xuất chính đều đưa ra bộ phận này:SD3-Turbo(SD3 + dòng chảy + 蒸)、Flux-schnell(Flux-dev + dòng chảy sửa chữa 拉直)、CogView-4-Flash──纯扩散基座只为遗留检查点保留──

## Xem thêm 延伸阅读

- [Liu, Gong, Liu (2022). Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/abs/2209.03003) dòng chảy được chỉnh sửa.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) dòng chảy phù hợp.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) SD3, lưu lượng được chỉnh sửa ở quy mô.
- [Albergo, Vanden-Eijnden (2023). Stochastic Interpolants](https://arxiv.org/abs/2303.08797) khung chung bao gồm FM + phát tán.
- [Song et al. (2023). Consistency Models](https://arxiv.org/abs/2303.01469) 1 bước chưng cất của sự pha trộn / dòng chảy.
- [Sauer et al. (2023). Adversarial Diffusion Distillation (SDXL-Turbo)](https://arxiv.org/abs/2311.17042) biến thể turbo.
- [Black Forest Labs (2024). Flux.1 models](https://blackforestlabs.ai/announcing-black-forest-labs/) dòng chảy phù hợp trong sản xuất.
