# Video Generation Video tạo ra

> Một hình ảnh là một tensor 2D. Một video là một tensor 3D. Lý thuyết là tương tự; tính toán là 10-100x khó hơn. Sora của OpenAI (tháng 2 năm 2024) chứng minh rằng điều đó có thể. Đến năm 2026 Veo 2, Kling 1.5, Runway Gen-3, Pika 2.0, và WAN 2.2 video sản xuất tàu từ văn bản ở 1080p  và khối lượng mở (CogVideoX, HunyuanVideo, Mochi-1, WAN 2.2) là 12 tháng sau.

> **【中文解读】**图像是2D 张量,视频是3D 张量,理论相同但计算量高10-100倍──Sora 证明可行,到2026年多个商业产品(Veo 2、Kling、Runway) đã có thể tạo ra 1080p 视频──

> **【拓展：Sora 的影响】**OpenAI's Sora (OpenAI's Sora) là một trong những thành tựu của video generation, cho thấy khả năng mở rộng mô hình + Transformer 架构.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 7 · 09 (ViT), Phase 8 · 06 (DDPM)
**Time:** ~45 minutes

## Vấn đề  vấn đề giới thiệu

Một video 1080p 10 giây ở 24fps là 240 khung hình 1920×1080×3 pixel. Đó là khoảng 1,5 GB dữ liệu thô mỗi clip.

> 10 giây 1080p 24fps 视频是 240  1920×1080×3 像素, khoảng 1.5 GB dữ liệu nguyên thủy──像素空间扩散不可行──你需要:

1. **Spatiotemporal compression.**Một VAE mã hóa video, không phải khung hình, thành một chuỗi các bản vá không gian-thời gian.
   **时空压缩。**将视频(而非)编码为时空补丁序列的 VAE。
2. **Temporal coherence.**Các khung hình cần chia sẻ nội dung, ánh sáng và danh tính đối tượng trong vài giây.
   **时间连贯性。**                                                                                                                                                                                                                                                              
3. **Compute budget.**Video đào tạo là 10-100 lần đắt hơn so với hình ảnh cho cùng một kích thước mô hình.
   **计算预算。**视频训练比图像贵 10-100 倍──
4. **Conditioning.**Các mô hình sản xuất đều chấp nhận cả bốn.
   **条件化。**文本、图像(首)、音频或其他视频──

Kiến trúc giải quyết vấn đề này là **Diffusion Transformer (DiT)**được áp dụng cho các bản vá không gian-thời gian, được đào tạo trên các bộ dữ liệu lớn (quick, caption, video).

>  giải quyết những cấu trúc này là**Diffusion Transformer (DiT)**应用于时空补丁, tập luyện trên tập dữ liệu quy mô lớn ◊ cùng với thứ 06 

## Khái niệm cốt lõi

![Video diffusion: patchify, DiT, decode](../assets/video-generation.svg)

### Tấn động

> ### Lắp vá

Mã hóa video bằng VAE 3D (đọc compress không gian-thời gian).`[T_latent, H_latent, W_latent, C_latent]`- Chia thành các mảnh nhỏ .`[t_p, h_p, w_p]`. cho những người mẫu kiểu Sora,`t_p = 1`(chăn đệm mỗi khung) hoặc `t_p = 2`Một video 1080p 10 giây nén đến khoảng 20.000-100.000 bản vá.

> 用 3D VAE 编码视频──潜在表示形状为 `[T, H, W, C]`│ │ │ │`[t_p, h_p, w_p]` 10 giây 1080p  video được nén lên khoảng 2-100.000 bản vá

### Tiếp tục không gian thời gian

> ### 时空 DiT

Một bộ biến chuyển xử lý chuỗi phích phích phích. Mỗi phích có một nhúng vị trí 3D (thời gian + y + x).

> Transformer 处理展平的补丁序列──每个补丁有3D 位置编码(时间 + y + x)──注意力通常分解为:

- **Spatial attention**trong các vết bẩn của mỗi khung.
  **空间注意力**Trong mỗi đệm trong.
- **Temporal attention**qua khung hình ở cùng một vị trí không gian.
  **时间注意力**跨的相同空间位置──
- **Full 3D attention**là 16-100 lần đắt hơn; chỉ được sử dụng ở độ phân giải thấp hoặc trong nghiên cứu.
  **完整 3D 注意力**贵 16-100 lần; chỉ trong phân giải thấp hoặc nghiên cứu sử dụng.

> **【中文解读】**视频生成的核心技术:(1) 3D VAE 将视频压缩为时空潜在表示;(2) 将潜在表示切分为时空补丁;(3) DiT(Diffusion Transformer) xử lý chuỗi补丁, sử dụng 3D 位置编码;(4) chú ý thường được phân chia thành không gian chú ý và thời gian chú ý để giảm lượng tính toán.

> **【拓展：Sora 架构与 DiT 在视频中的应用】**Core của Sora là sẽ ViT patch 化思想 mở rộng sang lĩnh vực video.

### Điều kiện văn bản

> ### 文本条件化

Sự chú ý chéo với một bộ mã hóa văn bản lớn (T5-XXL cho Sora, CogVideoX-5B sử dụng T5-XXL).

> Sử dụng bộ lập trình văn bản lớn để làm giao lưu chú ý. Long prompt  rất quan trọng.

### Việc đào tạo

> ### 训练

Thiếu tích phổ thông tiêu chuẩn (ε hoặc v dự đoán) trên các laten không gian-thời gian. Dữ liệu: video web + ~ 100M clip được sắp xếp + tiêu đề văn bản tổng hợp. Xét: 10.000+ giờ GPU cho ngay cả một cuộc nghiên cứu nhỏ; quy mô Sora là 100.000+.

> 时空潜在表示上的标准扩散损失──数据:网络视频 + 约1亿精选片段 + 合成文本标注──计算:小规模研究需要1万+ GPU 小时;Sora 规模是10万+──

## Tầm nhìn sản xuất năm 2026

| Model / 模型 | Date | Max duration / 最长时长 | Max res / 最高分辨率 | Open weights? / 开源？ | Notable / 亮点 |
|-------|------|--------------|---------|---------------|---------|
| Sora (OpenAI) | 2024-02 | 60s | 1080p | No | First model to show world simulator properties at scale / 首个展示世界模拟器属性的模型 |
| Sora Turbo | 2024-12 | 20s | 1080p | No | Production Sora at 5x faster inference / 5 倍推理加速 |
| Veo 2 (Google) | 2024-12 | 8s | 4K | No | Highest quality + physics in 2025 / 2025 年最高质量 |
| Veo 3 | 2025 Q3 | 15s | 4K | No | Native audio and stronger camera control / 原生音频 |
| Kling 1.5 / 2.1 (Kuaishou) | 2024-2025 | 10s | 1080p | No | Best human motion in 2025 Q1 / 最佳人体运动 |
| Runway Gen-3 Alpha | 2024-06 | 10s | 768p | No | Professional video tools on top / 专业视频工具 |
| Pika 2.0 | 2024-10 | 5s | 1080p | No | Strongest character consistency / 最强角色一致性 |
| CogVideoX (THUDM) | 2024 | 10s | 720p | Yes (2B, 5B) | First open 5B-scale video / 首个开源 5B 视频 |
| HunyuanVideo (Tencent) | 2024-12 | 5s | 720p | Yes (13B) | Open SOTA late 2024 / 2024 年末开源 SOTA |
| Mochi-1 (Genmo) | 2024-10 | 5.4s | 480p | Yes (10B) | Most permissively licensed / 最宽松许可 |
| WAN 2.2 (Alibaba) | 2025-07 | 5s | 720p | Yes | Strongest open model mid-2025 / 2025 年中最强开源 |

Các trọng lượng mở đang thu hẹp khoảng cách nhanh hơn trong không gian hình ảnh: HunyuanVideo + WAN 2.2 LoRA đã cung cấp năng lượng cho hầu hết các dòng công việc nguồn mở vào giữa năm 2026.

> nghĩa quyền mở đang giảm khoảng cách nhanh hơn trong lĩnh vực hình ảnh.

## Hãy xây dựng nó.
```figure
video-diffusion-denoise
```

## Hãy xây dựng nó

`code/main.py`mô phỏng ý tưởng DiT không gian thời gian cốt lõi: dán một video tổng hợp nhỏ, thêm một vị trí mỗi bản vá, và đánh dấu toàn bộ chuỗi với một sự chú ý theo kiểu biến thể trên các bản vá. Không numpy; Python tinh khiết. Chúng tôi cho thấy sự liên tục thời gian xuất hiện ngay cả trong 1-D khi các bản vá khung lân cận chia sẻ một ký hiệu và vị trí.

### Bước 1: Lắp ráp một "video" tổng hợp 1D

```python
def make_video(T_frames=8, rng=None):
    # a "video" is a sequence of 1-D values following a smooth trajectory
    base = rng.gauss(0, 1)
    return [base + 0.3 * t + rng.gauss(0, 0.1) for t in range(T_frames)]
```

### Bước 2: Đơn vị tích hợp mỗi khung

```python
def pos_embed(t, dim):
    return sinusoidal(t, dim)
```

### Bước 3: denoiser nhìn thấy toàn bộ chuỗi

Thay vì phủ nhận từng khung hình một cách độc lập, lưới nhỏ bé của chúng ta kết nối tất cả các giá trị khung hình + các nhúng vị trí của chúng và dự đoán tiếng ồn cho tất cả các khung hình cùng nhau.

### Bước 4: Kiểm tra liên tục thời gian

Sau khi tập luyện, lấy mẫu video. đo delta khung hình. Nếu mô hình đã học được cấu trúc thời gian, các delta vẫn nhỏ hơn so với lấy mẫu mỗi khung hình độc lập.

## # Thói bẫy #

- **Independent per-frame sampling = flicker.**Nếu bạn chạy phân phối hình ảnh trên mỗi khung hình riêng biệt, các đầu ra nhấp nháy vì tiếng ồn của mỗi khung hình là độc lập.
- **Naive 3D attention = OOM.**Sự chú ý 3D đầy đủ trên một màn hình 1080p ẩn trong 10 giây là hàng trăm tỷ hoạt động.
- **Data captioning matters more than size.**Việc nâng cấp chính của Sora so với công việc trước đó là đào tạo về các đoạn văn chi tiết hơn ~ 10 lần (gpt-4 được đánh dấu lại). báo cáo kỹ thuật của OpenAI rõ ràng về điều này.
- **First-frame conditioning.**Hầu hết các mô hình sản xuất cũng chấp nhận một hình ảnh như khung hình đầu tiên. Đây là chế độ "phần hình ảnh đến video"; đào tạo bao gồm biến thể này.
- **Physics drift.**Các clip dài (> 10s) tích lũy những sự bất đồng tinh tế.

## Hãy sử dụng nó để thực hiện

| Use case / 用途 | 2026 pick / 2026 选择 |
|----------|-----------|
| Highest-quality text-to-video, hosted / 最高质量托管 | Veo 3 or Sora |
| Camera-controlled cinematic / 相机控制电影感 | Runway Gen-3 with motion brushes |
| Character consistency across clips / 跨片段角色一致 | Pika 2.0 or Kling 2.1 |
| Open weights, fast fine-tune / 开源快速微调 | WAN 2.2 + LoRA |
| Image-to-video / 图生视频 | WAN 2.2-I2V, Kling 2.1 I2V, or Runway |
| Audio-to-video lip sync / 音频对口型 | Veo 3 (native audio) or a dedicated lip-sync model |
| Video editing / 视频编辑 | Runway Act-Two, Kling Motion Brush, Flux-Kontext (still-frame) |

Chi phí mỗi giây của video ở mức độ cân bằng chất lượng đã giảm 20 lần giữa năm 2024 và 2026.

> Giá video mỗi giây giảm 20 lần trong giai đoạn 2024 đến 2026.

## Chuyển nó đi.

- Cứu lại`outputs/skill-video-brief.md`. Skill lấy một đoạn video ngắn (thời gian, tỷ lệ hình ảnh, phong cách, kế hoạch máy ảnh, tính nhất quán của chủ đề, âm thanh) và các kết quả: mô hình + lưu trữ, trình chuẩn nhanh ( ngôn ngữ máy ảnh, mô tả chủ đề, mô tả chuyển động), giao thức hạt giống + khả năng tái tạo, và một danh sách kiểm tra QA cấp khung.

## Tập luyện bài tập

1. **Easy.**Trong `code/main.py`, so sánh khung-đối với khung delta cho (a) lấy mẫu độc lập mỗi khung, (b) lấy mẫu theo chuỗi chung. báo cáo trung bình và sự biến động của các delta.
2. **Medium.**Thêm một điều kiện khung đầu tiên: khung pin 0 đến một giá trị nhất định và lấy mẫu phần còn lại. đo cách biến số được gắn vào.
3. **Hard.**Sử dụng các bộ pha trộn HuggingFace để chạy CogVideoX-2B trên GPU địa phương. Tiêu khắc 20 bước suy luận ở 720p cho một clip 6 giây.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Video VAE | "3-D VAE" | Encoder that compresses `(T, H, W, C)` → spatiotemporal latent. |
| Patches | "The tokens" | Fixed-size 3-D blocks of the latent; input to the DiT. |
| Factorized attention | "Spatial + temporal" | Run attention over space, then over time; skip full 3-D attention. |
| Image-to-video (I2V) | "Animate this photo" | Model takes an image + text, outputs a video that starts from it. |
| Keyframe conditioning | "Anchor frames" | Pin specific frames to control the video's arc. |
| Motion brush | "Directional hint" | UI input where the user paints motion vectors onto the image. |
| Re-captioning | "Dense captions" | Using an LLM to re-label training clips with detailed prompts. |
| Flicker | "Temporal artifact" | Frame-to-frame inconsistency; fixed with coupled denoising. |

## Lưu ý sản xuất: video laten là một vấn đề về băng thông bộ nhớ.

Một clip 1080p 10 giây ở 24 fps là 240 khung hình × 1920 × 1080 × 3 ≈ 1,5 GB pixel nguyên liệu.`2 × spatial × 2 × temporal`(văn) là ~ 100 MB mỗi yêu cầu. Động hành này qua một DiT không gian-thời gian trong 30 bước tại lô 1 và bạn đang di chuyển ~ 3 GB / bước qua băng thông bộ nhớ HBM , không phải FLOPs, là nút thắt.

Ba nút sản xuất, tất cả đều trực tiếp từ chương luận án văn học sản xuất-đánh giá:

- **TP across the DiT.**Các mô hình văn bản-video thường là ≥10B. TP = 4 trên 4 H100 là tiêu chuẩn; PP = 2 × TP = 2 cho các mô hình lớp 405B. Độ trễ mỗi bước giảm theo đường thẳng với TP lên đến tường giảm hoàn toàn.
- **Frame batching = continuous batching.**Tại thời điểm phát triển, video là một loạt các khung hình được liên kết bởi sự chú ý.`t+1`trong khi khung `t-1`được trả lại, nếu kiến trúc mô hình cho phép tạo ra cửa sổ trượt.
- **Clip-level prefill cache.**Đối với hình ảnh-video, điều kiện khung hình đầu tiên tương tự như việc điền trước nhanh của LLM: tính toán nó một lần, sử dụng lại qua các đoạn mã hóa thời gian.

## Xem thêm 延伸阅读

- [Brooks et al. (2024). Video generation models as world simulators](https://openai.com/index/video-generation-models-as-world-simulators/) Báo cáo kỹ thuật của Sora.
- [Yang et al. (2024). CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer](https://arxiv.org/abs/2408.06072) CogVideoX.
- [Kong et al. (2024). HunyuanVideo: A Systematic Framework for Large Video Generative Models](https://arxiv.org/abs/2412.03603) HunyuanVideo.
- [Genmo (2024). Mochi-1 Technical Report](https://www.genmo.ai/blog/mochi) Mochi-1.
- [Alibaba (2025). WAN 2.2](https://wanvideo.io/) SOTA mở vào giữa năm 2025.
- [Ho, Salimans, Gritsenko et al. (2022). Video Diffusion Models](https://arxiv.org/abs/2204.03458) giấy truyền hình video.
- [Blattmann et al. (2023). Align your Latents (Video LDM)](https://arxiv.org/abs/2304.08818) Tổ tiên của Stable Video Diffusion.
