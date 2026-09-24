# 视频生成

> 图像是2D子.视频是3D子.理论是相同的;计算是10-100倍更难.OpenAI的Sora (2024年2月) 证明这是可能的.到2026年,Veo 2,Kling 1.5,跑道Gen-3,Pika 2.0和WAN 2.2的船产视频从文字在1080p 和开放权重堆 (CogVideoX,HunyuanVideo,Mochi-1,WAN 2.2) 落后了12个月.

> **【中文解读】**图像是2D张量,视频是3D张量,理论相同但计算量高10-100倍.

> **【拓展：Sora 的影响】**视频生成是2024年2月的最热门赛道之一.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 7 · 09 (ViT), Phase 8 · 06 (DDPM)
**Time:** ~45 minutes

## 问题 问题引入

像像素的速度为10秒 1080p视频,24fps,是240个图片的 1920×1080×3像素.这相当于每片的原始数据约1.5GB.像素空间的扩散是不可能的.你需要:

> 视频是240  1920×1080×3 像素,约1.5GB 原始数据――像素空间扩散不可行――你需要:

1. **Spatiotemporal compression.**编码视频,而不是框架,
   **时空压缩。**将视频(而非)编码为时空补丁序列的VAE──
2. **Temporal coherence.**框架需要分秒分享内容,照明和物体身份.
   **时间连贯性。**之间需要分享内容、光照和物体身份──
3. **Compute budget.**视频训练比像相等尺寸的图像10-100倍昂贵.
   **计算预算。**视频训练比图像贵10-100倍
4. **Conditioning.**文字,图像 (第一片),音频或其他视频.
   **条件化。**文本、图像(首)、音频或其他视频──

解决这个问题的架构是**Diffusion Transformer (DiT)**它们是用于空间时间补丁,训练在巨大的数据集 (即时,字幕,视频).与06课程相同的扩散损失.

> 解决这些架构是**Diffusion Transformer (DiT)**应用于时空补丁,大规模数据集训练――与第06课相同的扩散损失――

## 概念的核心概念

![Video diffusion: patchify, DiT, decode](../assets/video-generation.svg)

### 缩

> ### 补丁

通过3DVAE编码视频 (学习空间时间压缩).`[T_latent, H_latent, W_latent, C_latent]`分成小块`[t_p, h_p, w_p]`对于索拉风格的模型来说,`t_p = 1`(每补丁) 或`t_p = 2`一个10秒的1080p视频将压缩到20,000到100,000个补丁.

> 用3D VAE编码视频──潜在表示形状为`[T, H, W, C]`切分为`[t_p, h_p, w_p]`视频压缩为约2-10万个补丁.

### 时间空间

> ### 时空 时间

变压器处理了平坦的补丁序列.每个补丁都有3D定位嵌入 (时间 + y + x).注意力通常是因子化:

> 变压器处理展平的补丁序列――每个补丁都有3D位置编码(时间+y+x) ─注意力通常分解为:

- **Spatial attention**在每个框架的补丁中.
  **空间注意力**在每一个补丁内.
- **Temporal attention**在同一空间位置的框架上.
  **时间注意力**跨的相同空间位置.
- **Full 3D attention**价格高于16-100倍;仅在低分辨率或研究中使用.
  **完整 3D 注意力**价格16-100倍;仅在低分辨率或研究中使用.

> **【中文解读】**视频生成的核心技术: 1) 3D VAE 将视频缩为时空潜在表示; 2) 将潜在表示切分为时空补丁; 3) DiT(Diffusion Transformer) 处理补丁序列,使用 3D 位置编码; 4) 注意力通常分解为空间注意力和时间注意力以降低计算量.

> **【拓展：Sora 架构与 DiT 在视频中的应用】**索拉的核心是将ViT的补丁化思想扩展到视频领域将视频视频视为"时空补丁序列"――DiT(Diffusion Transformer) 用变压器替代U-Net作为无声网络,在视频生成中表现出更好的扩展性――开源实现如CogVideoX、HunyuanVideo和WAN 2.2 都遵循这一架构――

### 文字调节

> ### 文本条件化

交叉注意力与一个大的文本编码器 (T5-XXL为索拉,CogVideoX-5B使用T5-XXL).长时间提示问题索拉的训练集有GPT生成的密集重写字幕平均每片的200个代币.

> 长提示 很重要 索拉的训练集有GPT 生成的密集重标注,平均每段片段 200 个代币.

### 培训

> ### 训练

空间及时间隐藏的标准扩散损失 (ε或v预测).数据:网络视频+~100M编辑片段+合成文本标题.计算:即使是小型研究运行,也需要10,000+GPU小时;索拉规模为100,000+.

> 时空潜在表示上的标准扩散损失――数据:网络视频 + 约1亿精选片段 + 合成文本标注――计算:小规模研究需要1万+GPU 小时;Sora规模是10万+――

## 未来的2026年生产局面.

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

开放权重比图像空间更快地缩小了差距: 源视频+WAN 2.2 LoRA 已经在2026年中期为大多数开源工作流提供了动力.

> 开源权重正在缩小距离比图像领域更快.

## 建立它,实现它.
```figure
video-diffusion-denoise
```

## 建立它

`code/main.py`模拟了核心空间时间的DT想法:补丁一个小的合成视频,添加一个每补丁位置嵌入,并用变压器式的注意力在补丁上标明整个序列.没有 numpy;纯 Python.我们表明,当相邻的框架补丁共享一个标明和位置嵌入时,即使在1D中也出现时间一致性.

### 步骤1:修补一个合成1D视频

```python
def make_video(T_frames=8, rng=None):
    # a "video" is a sequence of 1-D values following a smooth trajectory
    base = rng.gauss(0, 1)
    return [base + 0.3 * t + rng.gauss(0, 0.1) for t in range(T_frames)]
```

### 步骤2:每架位置嵌入

```python
def pos_embed(t, dim):
    return sinusoidal(t, dim)
```

### 步骤3:指标器看到整个序列

而不是独立地揭示每个框架,我们的小网连接了所有框架值+它们的位置嵌入,并预测了所有框架的噪音.

### 步骤4:时间一致性测试

训练后,取样视频.测量框架到框架的三角形. 如果模型已经了解了时间结构,三角形将保持比独立取样每一个框架更小.

## 陷常见的陷

- **Independent per-frame sampling = flicker.**如果在每个图片单独运行图像扩散,输出闪,因为每个图片的噪音是独立的.视频扩散通过通过关注或共享噪音将图片连接起来来解决这一问题.
- **Naive 3D attention = OOM.**完全3D的注意力在10秒的1080p隐藏的数以亿计的操作.
- **Data captioning matters more than size.**索拉在之前的工作中的主要升级是对大约10倍更详细的字幕 (GPT-4重新标记的剪辑) 的培训.
- **First-frame conditioning.**大多数生产模型也接受图像作为第一框.这是"图像到视频"模式;培训包括这种变体.
- **Physics drift.**长片 (>10秒) 积累微妙的不一致性.滑动窗口生成+键盘固有助.

## 用它实现框架

| Use case / 用途 | 2026 pick / 2026 选择 |
|----------|-----------|
| Highest-quality text-to-video, hosted / 最高质量托管 | Veo 3 or Sora |
| Camera-controlled cinematic / 相机控制电影感 | Runway Gen-3 with motion brushes |
| Character consistency across clips / 跨片段角色一致 | Pika 2.0 or Kling 2.1 |
| Open weights, fast fine-tune / 开源快速微调 | WAN 2.2 + LoRA |
| Image-to-video / 图生视频 | WAN 2.2-I2V, Kling 2.1 I2V, or Runway |
| Audio-to-video lip sync / 音频对口型 | Veo 3 (native audio) or a dedicated lip-sync model |
| Video editing / 视频编辑 | Runway Act-Two, Kling Motion Brush, Flux-Kontext (still-frame) |

在2024年至2026年间,视频的质量均的成本每秒下降了20倍.

> 质量平价下每秒视频成本在2024年至2026年间下降了20倍.

## 运送它.

保存`outputs/skill-video-brief.md`技能采用视频简介 (时间,视角比率,风格,摄像头计划,主题一致性,音频) 和输出:模型+托管,即时架构 (摄像头语言,主题描述,运动描述符),种子+可复制性协议以及级QA检查清单.

## 练习题

1. **Easy.**在`code/main.py`根据该报告,每一个框架的数据,每一个框架的数据,每一个框架的数据,每一个框架的数据,每一个框架的数据,每一个框架的数据,每一个框架的数据,每一个框架的数据,每一个框架的数据,每一个框架的数据,每一个框架的数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据,每一个数据.
2. **Medium.**添加一个第一框条件:框0到给定的值,然后样本剩下的.测量值如何传播.
3. **Hard.**使用 HuggingFace 扩散器在本地 GPU 上运行 CogVideoX-2B. 时间 20 推断步骤在 720p 时 6 秒的剪辑. 配置空间时间注意力以确定瓶.

## 关键词 快速查找表

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

## 产品注:视频潜伏是内存带宽问题

通过4×视频VAE压缩 (VAE) 进行,可在24fps的10秒 1080p剪辑中获得240个 × 1920 × 1080 × 3 ≈1.5GB原始像素.`2 × spatial × 2 × temporal`通过一个空间时间的DIT进行30步的运行,你将通过HBM 内存带宽,而不是FLOPs,移动3GB/步.

直接从生产推理文学推理章中得到的三个生产:

- **TP across the DiT.**文字到视频模型通常是10B参数. 4H100的TP=4是标准的; 405B类模型的PP=2 ×TP=2.每步延迟大致在线性下降,TP达到全减墙.
- **Frame batching = continuous batching.**在生成时,视频概念上是一个由注意力连接的框架.`t+1`在框架中`t-1`如果模型架构允许滑窗生成,则将返回.
- **Clip-level prefill cache.**对于图像到视频,第一框调节类似于LLM的快速预填:计算一次,重复使用时间解码器. 这实际上是视频的KV缓存.

## 继续阅读 继续阅读

- [Brooks et al. (2024). Video generation models as world simulators](https://openai.com/index/video-generation-models-as-world-simulators/)索拉技术报告.
- [Yang et al. (2024). CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer](https://arxiv.org/abs/2408.06072)      
- [Kong et al. (2024). HunyuanVideo: A Systematic Framework for Large Video Generative Models](https://arxiv.org/abs/2412.03603)    视频
- [Genmo (2024). Mochi-1 Technical Report](https://www.genmo.ai/blog/mochi)莫奇-1.
- [Alibaba (2025). WAN 2.2](https://wanvideo.io/)2025年中期开放SOTA.
- [Ho, Salimans, Gritsenko et al. (2022). Video Diffusion Models](https://arxiv.org/abs/2204.03458)视频传播纸.
- [Blattmann et al. (2023). Align your Latents (Video LDM)](https://arxiv.org/abs/2304.08818) 稳定视频传播的祖先.
