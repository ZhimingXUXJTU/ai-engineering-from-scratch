# Video Genre video üretimi

> Bir görüntü 2 boyutlu bir tensördür. Bir video 3 boyutlu bir tenzordur. Teorisi aynıdır; hesaplama 10-100 kat daha zordur. OpenAI'nin Sora (Feb 2024) bunun mümkün olduğunu kanıtladı. 2026 yılına kadar Veo 2, Kling 1.5, Runway Gen-3, Pika 2.0, ve WAN 2.2 gemisi üretim videoları 1080p 'de metin ve açık ağırlıklı yığın (CogVideoX, HunyuanVideo, Mochi-1, WAN 2.2) 12 ay geri.

> **【中文解读】**图像是2D 张量,视频是3D 张量,理论相同但计算量高10-100倍──Sora 证明可行, 2026 yılına kadar birçok ticari ürün ((Veo 2、Kling、Runway) 1080p üretebilir video──

> **【拓展：Sora 的影响】**OpenAI'nin Sora (Feb. 2024) video üretimi için bir atıfta bulunmuştur.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 7 · 09 (ViT), Phase 8 · 06 (DDPM)
**Time:** ~45 minutes

## Sorunlar. Sorunlar.

10 saniyelik 1080p video 24fps'de 240 çerez 1920×1080×3 piksel. Bu, her klip için yaklaşık 1,5 GB ham veri. Piksel alanı yayılması mümkün değildir.

> 10 saniye 1080p 24fps  video 频是 240  1920×1080×3 像素, yaklaşık 1.5 GB 原始数据──像素空间扩散不可行──你需要:

1. **Spatiotemporal compression.**Çerçeve değil, videoları uzay-zamanlı yamalar dizisine kodlayan bir VAE.
   **时空压缩。**将视频(而非)编码为时空补丁序列的 VAE──
2. **Temporal coherence.**Çerçeve, içeriği, aydınlatmayı ve nesne kimliğini saniyeler içinde paylaşmalıdır.
   **时间连贯性。**                                                                                                                                                                                                                                                              
3. **Compute budget.**Video eğitimi aynı model boyutunda görüntüden 10-100 kat daha pahalıdır.
   **计算预算。**视频训练比图像贵 10-100倍──
4. **Conditioning.**Metin, görüntü (birinci çerçeve), ses veya başka bir video.
   **条件化。**文本、图像(首)、音频或其他视频──

Bunu çözen mimarlık **Diffusion Transformer (DiT)**Bu, uzay-zamanlı patchlere uygulanmış, büyük (sürekli, başlıklı, video) veri kümeleri üzerinde eğitilmiştir.

> Bu yapıların çözümü**Diffusion Transformer (DiT)**Zaman ve hava patch'i uygulayarak büyük ölçekli veri kümesi üzerinde eğitim.

## Konsepten bir şey.

![Video diffusion: patchify, DiT, decode](../assets/video-generation.svg)

### Çekil

> ### Çizgileme

Videoyu 3D VAE ile kodlayın.`[T_latent, H_latent, W_latent, C_latent]`- Büyüklükteki parçalara bölünmüş .`[t_p, h_p, w_p]`Sora tarzında modeller için.`t_p = 1`(kadre başına yapıştırmalar) veya `t_p = 2`10 saniyelik 1080p video yaklaşık 20.000-100.000 yama olarak sıkıştırılır.

> 3D VAE 编码视频──潜在表示形状为 `[T, H, W, C]`│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │`[t_p, h_p, w_p]`Büyük bir yama. 10 saniye 1080p video sıkıştırma 2-100.000 yama.

### Uzay-zamanlı DiT

> ### 时空 DiT

Bir transformatör, düz düzlemli yama dizisini işlemelidir. Her yama 3 boyutlu bir konumlandırma (zaman + y + x) sahiptir. Dikkat genellikle faktörlüdür:

> Transformer 处理展平的补丁序列──每个补丁有3D 位置编码(时间 + y + x)──注意力通常分解为:

- **Spatial attention**Her çerçeve patçası içinde.
  **空间注意力**Her bir yama içinde.
- **Temporal attention**Aynı mekanın çerçeveleri üzerinde.
  **时间注意力**跨的相同空间位置──
- **Full 3D attention**16-100 kat daha pahalı; sadece düşük çözünürlükte veya araştırmalarda kullanılır.
  **完整 3D 注意力**贵16-100倍; yalnızca düşük çözünürlükte veya araştırmada kullanılır。

> **【中文解读】**视频生成的核心技术:(1) 3D VAE videoyi zaman boşluğu için sıkıştırır;(2) potansiyel göstergeyi zaman boşluğu için ayırır;(3) DiT(Diffusion Transformer) 3D konum kodlaması kullanarak, patç 序列ini işleme;(4) dikkat genellikle boşluk dikkat ve zaman dikkatini düşük hesaplama miktarı için ayırır.

> **【拓展：Sora 架构与 DiT 在视频中的应用】**Sora'nın merkezi, ViT'in patch 化 düşüncesi video alanına yayılmasıdır. Video video videoları "Time空 patch 序列" olarak adlandırılır. DiT (Diffusion Transformer) Transformer'ı U-Net'i gürültü ağı olarak değiştirerek video üretimi sırasında daha iyi genişlemeyi göstermektedir.

### Metin koşullandırması

> ### 文本条件化

Büyük bir metin kodlayıcısı ile çapraz dikkat (T5-XXL Sora için, CogVideoX-5B T5-XXL kullanır). Uzun çağrılar önemli  Sora'nın eğitim kümesi, her klip için ortalama 200 token ile GPT üretilen yoğun başlıklara sahipti.

> Büyük metin kodlayıcı kullanılarak, bir parça üzerinde 200 tane token oluşturur.

### Eğitim

> ### 訓練

Uzay-zamanlı latenler üzerinde standart difüzyon kaybı (ε veya v tahmin). Veriler: web video + ~ 100M kurate edilmiş klipler + sentetik metin başlıkları. Hesaplama: 10.000+ GPU saatleri küçük bir araştırma çalışması için bile; Sora ölçeği 100.000+

> 时空潜在表示上的标准扩散损失──数据:网络视频 + 约1亿精选片段 + 合成文本标注──计算:小规模研究需要10,000+ GPU 小时;Sora 规模是100,000+──

## 2026 üretim tarzı 2026 üretim planı

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

Açık ağırlıklar, görüntü alanındaki farkı daha hızlı kapatıyor: HunyuanVideo + WAN 2.2 LoRA'lar 2026'ın ortalarına kadar çoğu açık kaynaklı iş akışını güçlendiriyor.

> Açık kaynaklı yük, görüntü alanından daha hızlı bir şekilde küçük bir fark oluşturmaktadır.

## Yapın.
```figure
video-diffusion-denoise
```

## Yapın

`code/main.py`Bu, küçük bir sentetik videoyi patchify, her patch pozisyonu yerleştirme eklemek ve tüm dizini patches üzerinde transformatör tarzında dikkatle denoze.

### Adım 1: sentetik 1D "video" yapıştır

```python
def make_video(T_frames=8, rng=None):
    # a "video" is a sequence of 1-D values following a smooth trajectory
    base = rng.gauss(0, 1)
    return [base + 0.3 * t + rng.gauss(0, 0.1) for t in range(T_frames)]
```

### Adım 2: Çerçeve başına yerleştirme

```python
def pos_embed(t, dim):
    return sinusoidal(t, dim)
```

### Adım 3: Denoiser tüm dizini görür

Her çerçeveyi bağımsız olarak tanımlamak yerine, küçük ağımız tüm çerçeve değerlerini + konum yerleşimlerini birleştirir ve tüm çerçeveler için gürültüyü birlikte tahmin eder.

### Adım 4: Zamanlı tutarlılık testi

Eğitimden sonra bir video örneği alın. Çerçeve-çerçeve delta ölçün. Eğer model zamansal yapıyı öğrenmişse, deltalar her çerçeveyi bağımsız olarak örneğe almaktan daha küçük kalır.

## Tuzaklar.

- **Independent per-frame sampling = flicker.**Her çerçeve üzerinde görüntü difüzyonu ayrı ayrı çalıştırırsanız, çıkış gürültüsü her çerçeve'nin gürültüsü bağımsız olduğundan parlıyor.
- **Naive 3D attention = OOM.**10 saniyelik 1080p latenti üzerinde tam 3 boyutlu dikkat yüz milyarlarca işlemdir.
- **Data captioning matters more than size.**Sora'nın önceki çalışmalara göre en önemli yükseltmesi, yaklaşık 10 kat daha detaylı başlıkları (GPT-4 yeniden etiketlenen klipler) üzerinde eğitimdi.
- **First-frame conditioning.**Çoğu üretim modeli de ilk çerçeve olarak bir görüntü kabul eder. Bu "resim-video" modudur; eğitim bu variansı içerir.
- **Physics drift.**Uzun klipler (> 10s) ince uyumsuzluklar biriktirir.

## Çerçeveyi kullanın.

| Use case / 用途 | 2026 pick / 2026 选择 |
|----------|-----------|
| Highest-quality text-to-video, hosted / 最高质量托管 | Veo 3 or Sora |
| Camera-controlled cinematic / 相机控制电影感 | Runway Gen-3 with motion brushes |
| Character consistency across clips / 跨片段角色一致 | Pika 2.0 or Kling 2.1 |
| Open weights, fast fine-tune / 开源快速微调 | WAN 2.2 + LoRA |
| Image-to-video / 图生视频 | WAN 2.2-I2V, Kling 2.1 I2V, or Runway |
| Audio-to-video lip sync / 音频对口型 | Veo 3 (native audio) or a dedicated lip-sync model |
| Video editing / 视频编辑 | Runway Act-Two, Kling Motion Brush, Flux-Kontext (still-frame) |

Kalite eşitliği ile videoların saniyede maliyeti 2024 ile 2026 arasında 20 kat düştü.

> 质量平价下 视频成本 per second 2024-2026 yılları arasında 20 kat düştü.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-video-brief.md`. Skill, bir video kısa (zaman, boyut oranı, stil, kamera planı, konu tutarlılığı, ses) ve çıkışları alır: model + hosting, hızlı asfaltlama (kamera dili, konu açıklaması, hareket tanımlayıcıları), tohum + yeniden üretilebilirlik protokolü ve çerçeve düzeyinde bir QA kontrol listesi.

## Egzersizler.

1. **Easy.**İçeri`code/main.py`, (a) bağımsız çerçeve örneklemesi için çerçeveye delta karşılaştırın, (b) ortak dizi örneklemesi için.
2. **Medium.**Birinci çerçeve koşulunu ekleyin: pin çerçeve 0 belirli bir değere ve geri kalanı örnekleyin.
3. **Hard.**HuggingFace difüzerlerini kullanarak CogVideoX-2B'yi yerel bir GPU'da çalıştırın. 6 saniyelik bir klip için 720p'de zaman 20 sonucu adımları.

## Anahtar Şartlar .

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

## Üretim Notu: Video latentleri hafıza bant genişliği sorunu.

10 saniyelik 1080p clip 24 fps'de 240 çorap × 1920 × 1080 × 3 ≈ 1.5 GB çiğ pikseli.`2 × spatial × 2 × temporal`Bu, bir dilimde 30 adım boyunca bir uzay-zaman DiT üzerinden çalıştırılır ve HBM  hafıza bant genişliği ile 3 GB/adım geçirilir.

Üç üretim düğmesi, hepsi doğrudan üretim-sözü literatürü sonucu bölümünden:

- **TP across the DiT.**Metin-video modelleri rutin olarak ≥10B parametreleridir. TP=4 4 H100'de standarttır; PP=2 × TP=2 405B sınıfı modeller için.
- **Frame batching = continuous batching.**Video, üretim sırasında kavramsal olarak dikkat ile bağlantılı bir çerçeve seri.`t+1`çerçeve yaparken`t-1`model mimarisi sürükleyici pencere üretimini sağlıyorsa geri veriliyor.
- **Clip-level prefill cache.**Resim-video için, ilk çerçeve koşullaması bir LLM'nin hızlı önceden doldurması ile benzer: bir kez hesaplayın, temporal dekoder geçişleri boyunca tekrar kullanın. Bu aslında video için bir KV-cache.

## Daha fazla okumak

- [Brooks et al. (2024). Video generation models as world simulators](https://openai.com/index/video-generation-models-as-world-simulators/) Sora teknik raporu.
- [Yang et al. (2024). CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer](https://arxiv.org/abs/2408.06072) CogVideoX.
- [Kong et al. (2024). HunyuanVideo: A Systematic Framework for Large Video Generative Models](https://arxiv.org/abs/2412.03603) HunyuanVideo.
- [Genmo (2024). Mochi-1 Technical Report](https://www.genmo.ai/blog/mochi)Mochi-1.
- [Alibaba (2025). WAN 2.2](https://wanvideo.io/) SOTA'yı 2025'in ortalarında açmak.
- [Ho, Salimans, Gritsenko et al. (2022). Video Diffusion Models](https://arxiv.org/abs/2204.03458) video yayım kağıdı.
- [Blattmann et al. (2023). Align your Latents (Video LDM)](https://arxiv.org/abs/2304.08818) Stable Video Diffusion'un ataları.
