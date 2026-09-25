# ControlNet, LoRA & Conditioning  ControlNet, LoRA và điều kiện kiểm soát

> Chỉ riêng văn bản là một tín hiệu điều khiển khó xử. ControlNet cho phép bạn sao chép một mô hình phân tán được đào tạo trước và điều khiển nó bằng một bản đồ độ sâu, hình dạng hình dạng xương, vỏ hoặc cạnh. LoRA cho phép bạn điều chỉnh một mô hình tham số 2B bằng cách đào tạo 10 triệu tham số. Cùng nhau họ đã biến Stable Diffusion từ một đồ chơi thành đường ống dẫn hình ảnh 2026 được gửi đến mọi cơ quan.

> **【中文解读】**纯文本控制太粗──ControlNet sử dụng độ sâu图图,姿态骨架涂或边缘图精确控制生成;LoRA chỉ đào tạo 1000 triệu参数就能微调 20 tỷ参数模型── hai kết hợp để tạo ra sự pha trộn ổn định từ đồ chơi trở thành dòng hình ảnh chảy nước trong mỗi công ty thiết kế sử dụng vào năm 2026──

> **【拓展：LoRA 是大模型时代的微调标准】**LoRA không chỉ được sử dụng trong việc tạo hình ảnh, nó cũng được sử dụng rộng rãi trong LLM 微调 (như LLaMA-LoRA)  chỉ cần đào tạo 0,1% các tham số để thích ứng với nhiệm vụ mới, làm cho AI 定制 hóa chi phí giảm đáng kể.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 10 (LLMs from Scratch — for LoRA foundation / LoRA 基础)
**Time:** ~75 minutes

## Vấn đề  vấn đề giới thiệu

Một lời nhắc nhở như "một người phụ nữ mặc váy đỏ đi bộ một con chó trên một con đường bận rộn" không cho mô hình thông tin về * đâu * con chó, * tư thế nào * người phụ nữ đang ở, hoặc * quan điểm * của đường phố.

>  như "một người phụ nữ mặc đỏ  trên con chó bận rộn trên đường phố" như vậy không nói cho mô hình chó đang ở * ở đâu *、 người phụ nữ là * gì tư thế *、 đường phố * quan điểm * làm thế nào── văn bản chỉ có thể xác định khoảng 10% thông tin hình ảnh── phần còn lại là hình ảnh, không thể sử dụng chữ để mô tả hiệu quả──

Việc đào tạo một mô hình điều kiện mới từ đầu cho mỗi tín hiệu (phòng, độ sâu, tinh tế, phân đoạn) là cấm kỵ. Bạn muốn giữ cho xương sống SDXL 2.6B-param được đóng băng, gắn một mạng bên nhỏ đọc điều kiện, và nó đẩy các tính năng trung gian của xương sống. đó là ControlNet.

> Để mỗi tín hiệu (giới thiệu về hình thái, độ sâu, cạnh, chia) từ đầu đào tạo, giá của mô hình điều kiện mới quá cao. Bạn muốn duy trì SDXL có 2,6B tham số, thêm một mạng bên nhỏ có điều kiện đọc.

Bạn cũng muốn dạy cho mô hình những khái niệm mới (mô hình của bạn, sản phẩm của bạn, phong cách của bạn) mà không cần đào tạo lại mô hình đầy đủ. Bạn muốn một delta nhỏ hơn 100 lần. Đó là các bộ điều chỉnh hạng thấp LoRA  kết nối với trọng lượng chú ý hiện có.

> Bạn cũng muốn dạy mô hình mới khái niệm ((nước mặt của bạn, sản phẩm của bạn, phong cách của bạn) không tập trung vào toàn bộ mô hình. Bạn cần tăng trưởng nhỏ gấp 100 lần. Đó là LoRA.

ControlNet + LoRA + text = bộ công cụ của người thực hành năm 2026. Hầu hết các ống dẫn hình ảnh sản xuất lớp 2-5 LoRA, 1-3 ControlNets và một bộ điều chỉnh IP trên đỉnh một SDXL / SD3 / Flux.

> ControlNet + LoRA + text = 2026 năm thực hành viên toolbox。 hầu hết sản xuất hình ảnh流水线 trên SDXL/SD3/Flux  cơ sở chồng lên 2-5 个 LoRA、1-3 个 ControlNet 和一个 IP-Adapter。

## Khái niệm cốt lõi

![ControlNet clones the encoder; LoRA adds low-rank deltas](../assets/controlnet-lora.svg)

### ControlNet (Zhang et al., 2023)

Hãy lấy một SD được đào tạo trước. *Clone* một nửa mã hóa của U-Net. Đóng băng bản gốc. Trén nhân tạo để chấp nhận một đầu vào điều kiện bổ sung (về, độ sâu, tư thế). Kết nối nhân tạo trở lại phần mã hóa nửa của bản gốc với *zero-convolution* skip kết nối (1×1 convs khởi tạo thành 0  bắt đầu như một no-op, học một delta).

```
SD U-Net decoder:   ... ← orig_enc_features + zero_conv(controlnet_enc(condition))
```

Zero-conv init có nghĩa là ControlNet bắt đầu với tính cách  không gây hại ngay cả trước khi đào tạo.

Các ControlNets cho tính năng tính năng được vận chuyển như các mô hình phụ nhỏ (~ 360M cho SDXL, ~ 70M cho SD 1.5).

```
features += weight_a * control_a(depth) + weight_b * control_b(pose)
```

### LoRA (Hu et al., 2021)

Đối với bất kỳ lớp tuyến tính nào `W ∈ R^{d×d}`trong mô hình, đóng băng `W`và thêm một delta hạng thấp:

```
W' = W + ΔW,  ΔW = B @ A,  A ∈ R^{r×d},  B ∈ R^{d×r}
```

với `r << d`. Đường 4-16 là tiêu chuẩn cho sự chú ý, hạng 64-128 cho các âm thanh tinh tế nặng.`2 · d · r`thay vì `d²`. Để SDXL chú ý với `d=640`- `r=16`: 20k params mỗi bộ điều chỉnh thay vì 410k  giảm 20x. Trên toàn bộ mô hình: một LoRA thường là 20-200MB so với 5GB cơ sở.

Khi suy luận bạn có thể mở rộng LoRA: `W' = W + α · B @ A`- `α = 0.5-1.5`LoRA nhiều chồng lên bổ sung (với cảnh báo thông thường rằng chúng tương tác theo cách không tuyến tính).

### Đáp ứng IP (Ye et al., 2023)

Một bộ điều chỉnh nhỏ chấp nhận một hình ảnh như là điều kiện (cùng với văn bản). Sử dụng mã hóa hình ảnh CLIP để tạo ra các mã thông báo hình ảnh, tiêm chúng vào sự chú ý chéo bên cạnh các mã thông báo văn bản. ~ 20MB mỗi mô hình cơ sở. Cho phép bạn "tạo một hình ảnh theo phong cách của tham chiếu này" mà không cần LoRA.

## Matrix hợp thể

| Tool / 工具 | What it controls / 控制内容 | Size / 大小 | When to use / 使用时机 |
|------|------------------|------|-------------|
| ControlNet | Spatial structure (pose, depth, edges) / 空间结构 | 70-360MB | Exact layout, composition / 精确布局 |
| LoRA | Style, subject, concept / 风格、主题、概念 | 20-200MB | Personalization, style / 个性化、风格 |
| IP-Adapter | Style or subject from reference image / 参考图像风格 | 20MB | No text can describe the look / 文字无法描述 |
| Textual Inversion | Single concept as a new token / 单概念新 token | 10KB | Legacy, mostly replaced by LoRA / 旧方案 |
| DreamBooth | Full fine-tune on a subject / 完整微调 | 2-5GB | Strong identity, high compute / 强身份 |
| T2I-Adapter | Lighter ControlNet alternative / 轻量 ControlNet | 70MB | Edge devices, inference budget / 边缘设备 |

ControlNet ≈ không gian, LoRA ≈ ngữ nghĩa.

> ControlNet ≈ 空间控制──LoRA ≈ 语义控制──两者配合使用──

> **【中文解读】**Cơ chế cốt lõi của ControlNet: Klon SD U-Net 编码器,结原始部分,训练克隆部分接受额外条件输入(边缘、深度、姿态)。零卷积(零卷积) 初始化确保训练开始时 ControlNet không ảnh hưởng đến mô hình nguyên thủy。LoRA 在线性层上添加低排矩阵 B@A, chỉ训练极少参数量(20-200MB vs 基础模型 5GB)。

> **【拓展：ControlNet + LoRA 的组合控制】**Trong thực tế,ControlNet (ControlNet) và LoRA (ControlNet) thường được sử dụng trong các bộ sưu tập. Ví dụ:ControlNet (ControlNet)  kiểm soát tư thế nhân,LoRA (LoRA) vào phong cách nghệ thuật cụ thể, văn bản nhắc nhở mô tả nội dung cảnh.

## Hãy xây dựng nó.
```figure
v4-controlnet-zero
```

## Hãy xây dựng nó

`code/main.py`mô phỏng hai cơ chế trên 1-D:

1. **LoRA.**Một lớp tuyến tính được huấn luyện trước `W`- Đưa máy xuống.`B @ A`như thế này`W + BA`phù hợp với một lớp đường thẳng mục tiêu.`r = 1`là đủ để học một sự điều chỉnh cấp 1 hoàn hảo.

2. **ControlNet-lite.**Một dự đoán "đấu chốt" và một "hạng bên" đọc một tín hiệu bổ sung.

### Bước 1: LH toán LoRA

```python
def lora(W, A, B, x, alpha=1.0):
    # W is frozen; A, B are the trainable low-rank factors.
    return [W[i][j] * x[j] for i, j in ...] + alpha * (B @ (A @ x))
```

### Bước 2: mạng bên không-init

```python
side_out = control_net(x, condition)
gated = gate * side_out  # gate initialized to 0
h = base(x) + gated
```

Ở bước 0 đầu ra giống hệt với cơ sở.`gate`chậm rãi không có sự xoay xở thảm khốc.

> Trong bước thứ 0 đầu ra và mô hình cơ bản hoàn toàn giống nhau.`gate`更新缓慢没有灾难性偏移──

## # Thói bẫy #

- **Over-scaling LoRAs.** `α = 2`hoặc `α = 3`là một hack "làm nó mạnh hơn" phổ biến tạo ra các kết quả quá kiểu hóa / bị phá vỡ.`α ≤ 1.5`- Tôi không biết.
  **LoRA 过度缩放。** `α = 2`Hoặc`α = 3`là "các hành vi" thường thấy, sẽ tạo ra quá nhiều kiểu hóa/phong hỏng của sản xuất.`α ≤ 1.5`
- **ControlNet weight conflict.**Sử dụng một Pose ControlNet với trọng lượng 1.0 và một Depth ControlNet với trọng lượng 1.0 thường vượt quá.
  **ControlNet 权重冲突。**权重之和 ≈ 1.0 là giá trị mặc định của an toàn.
- **LoRA on the wrong base.**SDXL LoRA âm thầm không hoạt động trên SD 1.5 vì kích thước chú ý không phù hợp.
  **LoRA 用错基础模型。**SDXL LoRA trong SD 1.5 上会静默无效.
- **Textual Inversion drift.**Các token được huấn luyện tại một điểm kiểm soát sẽ bị lôi kéo xấu ở điểm kiểm soát khác.
  **Textual Inversion 漂移。**Trong một điểm kiểm tra, biểu tượng tập luyện trên một điểm khác.
- **LoRA weight-merging and storage.**Bạn có thể nướng một LoRA vào các trọng lượng mô hình cơ bản để suy luận nhanh hơn (không thêm thời gian chạy), nhưng bạn mất khả năng để mở rộng `α`- Giữ cả hai phiên bản.
  **LoRA 权重合并。**Có thể tăng tốc trong mô hình cơ bản, nhưng mất thời gian điều chỉnh`α`của khả năng.

## Hãy sử dụng nó để thực hiện

| Goal / 目标 | 2026 pipeline / 方案 |
|------|---------------|
| Reproduce a brand's art style / 复刻品牌艺术风格 | LoRA trained on ~30 curated images at rank 32 |
| Put my face in a generated image / 把我的脸放入生成图像 | DreamBooth or LoRA + IP-Adapter-FaceID |
| Specific pose + prompt / 特定姿态+提示 | ControlNet-Openpose + SDXL + text |
| Depth-aware composition / 深度感知构图 | ControlNet-Depth + SD3 |
| Reference + prompt / 参考+提示 | IP-Adapter + text |
| Exact layout / 精确布局 | ControlNet-Scribble or ControlNet-Canny |
| Background replace / 背景替换 | ControlNet-Seg + Inpainting (Lesson 09) |
| Fast 1-step style / 快速单步风格 | LCM-LoRA on SDXL-Turbo |

## Chuyển nó đi.

- Cứu lại`outputs/skill-sd-toolkit-composer.md`. Nghệ năng thực hiện một nhiệm vụ (tài sản đầu vào: prompt, hình ảnh tham chiếu tùy chọn, tư thế tùy chọn, độ sâu tùy chọn, vít tùy chọn) và đưa ra các khối công cụ, trọng lượng và một giao thức hạt giống có thể tái tạo.

## Tập luyện bài tập

1. **Easy / 简单.**Trong `code/main.py`, thay đổi cấp độ LoRA `r`Từ 1 đến 4, ở mức nào LoRA chính xác phù hợp với một điểm mục tiêu hạng 2?
   Trong `code/main.py`Trung tướng LoRA 秩 `r`Từ 1 变 đến 4 ⋅ ở đâu trong các hạng mục  LoRA 恰好匹配 trong các mục tiêu 2 ?
2. **Medium / 中等.**Đào tạo hai LoRA riêng biệt trên hai biến đổi mục tiêu. Lái chúng lại với nhau và cho thấy sự tương tác phụ gia của chúng.
   Trong hai mục tiêu thay đổi trên phân biệt đào tạo LoRA.
3. **Hard / 困难.**Sử dụng các diffuser để xếp chồng: SDXL-base + Canny-ControlNet (tín 0,8) + một kiểu LoRA (α 0,8) + IP-Adapter (tín 0,6).
   Sử dụng các phân tán 堆叠组合, đo FID và prompt 遵循的权衡──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| ControlNet | "Spatial control" / "空间控制" | Cloned encoder + zero-conv skips; reads a conditioning image. / 克隆编码器 + 零卷积跳跃。 |
| Zero convolution | "Starts as identity" / "起始为恒等" | 1×1 conv initialized to zero; ControlNet starts as no-op. / 1×1 卷积初始化为零。 |
| LoRA | "Low-rank adapter" / "低秩适配器" | `W + B @ A`, `r << d`; 100x fewer params than a full fine-tune. / 比完整微调少 100 倍参数。 |
| rank r | "The knob" / "那个旋钮" | LoRA compression; 4-16 typical, 64+ for heavy personalization. / LoRA 压缩；典型 4-16。 |
| α | "LoRA strength" / "LoRA 强度" | Runtime scaling of the LoRA delta. / LoRA 增量的运行时缩放。 |
| IP-Adapter | "Reference image" / "参考图像" | Small image-conditioning adapter via CLIP-image tokens. / 通过 CLIP 图像 token 的小型适配器。 |
| DreamBooth | "Full subject fine-tune" / "完整主题微调" | Train the full model on ~30 images of a subject. / 在约 30 张主题图像上训练完整模型。 |
| Textual Inversion | "New token" / "新 token" | Learn a new word embedding only; legacy, mostly replaced. / 仅学习新词嵌入；旧方案。 |

## Lưu ý sản xuất: LoRA swaps, ControlNet lanes, dịch vụ cho nhiều người thuê nhà.

Một SaaS văn bản thực tế phục vụ hàng trăm LoRA và một chục ControlNets trên cùng một điểm kiểm soát cơ sở. Vấn đề phục vụ trông giống như LLM đa thuê (bibliografi sản xuất bao gồm trường hợp LLM dưới sự phân phối liên tục và LoRAX / S-LoRA):

- **Hot-swap LoRAs, do not merge.**Thêm vào`W' = W + α·B·A`vào cơ sở cho ~ 3-5% nhanh hơn mỗi bước suy luận nhưng đóng băng `α`Giữ LoRAs nóng trong VRAM như rank-r delta; diffuser phơi bày `pipe.load_lora_weights()`+ `pipe.set_adapters([...], adapter_weights=[...])`cho kích hoạt theo yêu cầu. chi phí trao đổi là `2 · d · r · num_layers`trọng lượng  MB-scale, sub-second.
- **ControlNet as a second attention lane.**Các mã hóa được sao chép chạy song song với cơ sở. Hai ControlNets với trọng lượng 1.0 mỗi = hai vượt qua phía trước thêm mỗi bước, không phải một vượt qua hợp nhất.
- **Quantized LoRAs too.**Nếu bạn định lượng cơ sở (xem Bài học 07, Flux trên 8GB), delta LoRA cũng định lượng sạch đến 8-bit hoặc 4-bit. Loading theo kiểu QLoRA cho phép bạn xếp 5-10 LoRA trên đỉnh cơ sở Flux 4-bit mà không làm hư hỏng bộ nhớ.

Flux-specific: Niels' Flux-on-8GB notebook định lượng cơ sở thành 4 bit; xếp chồng một kiểu LoRA (`pipe.load_lora_weights("user/style-lora")`) trên cơ sở lượng tử đó tại `weight_name="pytorch_lora_weights.safetensors"`Đây là công thức mà hầu hết các công ty SaaS sẽ đưa ra vào năm 2026.

## Xem thêm 延伸阅读

- [Zhang, Rao, Agrawala (2023). Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543)ControlNet.
- [Hu et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) LoRA (trước đây là LLM; các cổng để pha trộn).
- [Ye et al. (2023). IP-Adapter: Text Compatible Image Prompt Adapter](https://arxiv.org/abs/2308.06721) Đổi IP
- [Mou et al. (2023). T2I-Adapter: Learning Adapters to Dig Out More Controllable Ability](https://arxiv.org/abs/2302.08453) thay thế nhẹ hơn cho ControlNet.
- [Ruiz et al. (2023). DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/abs/2208.12242) DreamBooth.
- [HuggingFace Diffusers — ControlNet / LoRA / IP-Adapter docs](https://huggingface.co/docs/diffusers/training/controlnet) đường ống dẫn tham chiếu.
