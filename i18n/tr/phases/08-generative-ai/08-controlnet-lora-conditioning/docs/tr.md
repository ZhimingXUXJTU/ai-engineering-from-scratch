# Kontrol Net, LoRA & Kondisyonlama

> Tekrar metin çilekli bir kontrol sinyali. ControlNet, önceden eğitilmiş bir difüzyon modelini klonlamanıza ve onu derinlik haritası, iskelet, kazık veya kenar görüntüsü ile yönlendirmenize olanak tanır. LoRA, 10 milyon parametreyi eğiterek 2B parametresi modeli ince ayarlamanıza olanak tanır. Birlikte, Stabil Diffusion'u bir oyuncaktan 2026 görüntü borusuna dönüştürdüler.

> **【中文解读】**純文本控制太粗──ControlNet, derinlik çizimleri, pozisyoni yapı,涂 veya kenar çizimleri kullanarak kesin kontrol üretimi;LoRA sadece 1000 milyon parametreyi 20 milyar parametreyi küçükleştirebilen bir model üzerinde eğitmektedir── ikisi birlikte, oyuncaklardan 2026 yılında her tasarım şirketi tarafından kullanılan görüntü akış hattına dönüştürülmesini sağlar.

> **【拓展：LoRA 是大模型时代的微调标准】**LoRA (Low Range Adaptation) sadece görüntü üretimi sırasında kullanılmakla kalmaz, aynı zamanda LLM'de yaygın olarak kullanılır.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 10 (LLMs from Scratch — for LoRA foundation / LoRA 基础)
**Time:** ~75 minutes

## Sorunlar. Sorunlar.

"Kırmızı elbise giyen bir kadın, yoğun bir sokakta köpek yürütüyor" gibi bir ipucu, modelin köpeğin nerede olduğunu, kadın hangi pozda olduğunu veya sokak perspektifini bilmesine izin vermez.

>  "Kırmızıya bürünmüş bir kadın meşgul bir sokakta  köpek" gibi ipuçları, model köpeklerin nerede olduğunu, kadınların nasıl bir duruş olduğunu söylemez.

Her sinyal için yeni bir koşullu model eğitmek (tıp, derinlik, zekice, segmentasyon) yasaktır. 2.6B-param SDXL omurgasını dondurmak, koşullamayı okuyan küçük bir yan ağ bağlamak ve omurgasının orta özelliklerini itmek istiyorsunuz. Bu ControlNet.

> Her sinyal için (geozü­l, derinlik, kenarlık, bölünme) baştan başta yeni koşullar modeli fiyatı çok yüksek.

Ayrıca, modelin tamamını yeniden eğitmeden yeni kavramlar (yüzünüz, ürününüz, stiliniz) öğretmek istiyorsunuz. 100 kat daha küçük bir delta istiyorsunuz. Bu, mevcut dikkat ağırlıklarına bağlanan düşük rütbeli LoRA  adaptörler.

> modelin yeni kavramını öğretmek istiyorsun. (Öz yüzünü, ürününü, tarzını) tüm modelin yeniden eğitilmesini istemiyorsun.

ControlNet + LoRA + metin = 2026 uygulayıcısının araç kümesi. Çoğu üretim görüntü boru hattı 2-5 LoRA, 1-3 ControlNets ve SDXL / SD3 / Flux tabanının üstünde bir IP-Adapter katıyor.

> ControlNet + LoRA + text = 2026 yıl pratikçilerin araç kutusu。 çoğu üretim görüntü akış su hattı SDXL/SD3/Flux  bazında 2-5 个 LoRA、1-3 个 ControlNet 和一个 IP-Adapter 基础上叠加──

## Konsepten bir şey.

![ControlNet clones the encoder; LoRA adds low-rank deltas](../assets/controlnet-lora.svg)

### ControlNet (Zhang et al., 2023)

*Klon * U-Net'in kodlayıcı yarısını. Orijinalı dondur. Ekstra şartlandırma girişini kabul etmek için klonu eğit. * sıfır konvulsiyon* sıfır bağlantıları ile klonu orijinalin dekodör yarısına tekrar bağlayın (1×1 konvis sıfır  olarak başlatılır  no-op olarak başlayın, delta öğrenin).

```
SD U-Net decoder:   ... ← orig_enc_features + zero_conv(controlnet_enc(condition))
```

Zero-conv init, ControlNet'in eğitimden önce bile kimlik olarak başlaması  zarar vermemesi anlamına gelir. 1M'de tren (sürekli, durum, görüntü) standart difüzyon kaybı ile üç katına çıkar.

Per-modality ControlNets küçük yan modeller olarak (SDXL için ~ 360M, SD 1.5 için ~ 70M) gönderir.

```
features += weight_a * control_a(depth) + weight_b * control_b(pose)
```

### LoRA (Hu et al., 2021)

Herhangi bir doğrusal katman için `W ∈ R^{d×d}`Modelde, dondurma `W`ve aşağı derecede bir delta ekle:

```
W' = W + ΔW,  ΔW = B @ A,  A ∈ R^{r×d},  B ∈ R^{d×r}
```

- Evet .`r << d`4-16 sıra dikkat için standart, 64-128 sıra ağır ince tonlar için.`2 · d · r`yerine`d²`. SDXL dikkat için `d=640`- Evet .`r=16`Adaptör başına 20k param 410k yerine  20x azaltma. Tüm model boyunca: bir LoRA genellikle 20-200MB vs. temel 5GB.

Sonuç olarak , LoRA ' yı ölçebilirsiniz:`W' = W + α · B @ A`- Evet .`α = 0.5-1.5`Bir çok LoRA'nın ek olarak yığılması (doğru uyarı ile, doğrusal olmayan şekillerde etkileşime girmeleri) normaldir.

### IP-Adapter (Ye et al., 2023)

* resim * bir şartlama olarak kabul eden küçük bir adaptör (metin yanında). Görüntü jetonları üretmek için CLIP görüntü kodlayıcısını kullanır, onları metin jetonları yanında çapraz dikkat içine enjekte eder. ~ 20 MB baz model başına.

## Yapılandırılabilirlik matrisi.

| Tool / 工具 | What it controls / 控制内容 | Size / 大小 | When to use / 使用时机 |
|------|------------------|------|-------------|
| ControlNet | Spatial structure (pose, depth, edges) / 空间结构 | 70-360MB | Exact layout, composition / 精确布局 |
| LoRA | Style, subject, concept / 风格、主题、概念 | 20-200MB | Personalization, style / 个性化、风格 |
| IP-Adapter | Style or subject from reference image / 参考图像风格 | 20MB | No text can describe the look / 文字无法描述 |
| Textual Inversion | Single concept as a new token / 单概念新 token | 10KB | Legacy, mostly replaced by LoRA / 旧方案 |
| DreamBooth | Full fine-tune on a subject / 完整微调 | 2-5GB | Strong identity, high compute / 强身份 |
| T2I-Adapter | Lighter ControlNet alternative / 轻量 ControlNet | 70MB | Edge devices, inference budget / 边缘设备 |

Kontrol Ağı, uzaylı, LoRA, semantik.

> ControlNet ≈ 空间控制──LoRA ≈ 语义控制──两者配合使用──

> **【中文解读】**ControlNet'in çekirdek mekanizması: Klon SD U-Net 编码器,结原始部分,训练克隆部分接受额外条件输入(边缘、深度、姿态)。零卷积(零卷积) 初始化确保训练开始时 ControlNet does not affect the original model。LoRA 在线性层上添加低排矩阵 B@A, training极少参数量(20-200MB vs 基础模型 5GB)。

> **【拓展：ControlNet + LoRA 的组合控制】**实际生产中,ControlNet(空间控制) 和 LoRA(风格/主题控制) genellikle bir araya gelerek kullanılır. Örneğin:ControlNet 控制人物姿态,LoRA 注入特定艺术风格,文本提示 场景内容的描述──这种三层控制机制是2026年商业AI 图像服务的标准配置──IP-Adapter 则提供了"图像控制图片"的第四维度──

## Yapın.
```figure
v4-controlnet-zero
```

## Yapın

`code/main.py`1-D'de iki mekanizmayı simüle eder:

1. **LoRA.**Önceden eğitilmiş bir çizgi katman .`W`- Dondur. Düşük bir sınıfı eğit.`B @ A`Bu kadar .`W + BA`Hedef çizgisi katmanına eşleşir.`r = 1`Birinci seviye düzeltmesini mükemmel öğrenmek için yeterli.

2. **ControlNet-lite.**Bir "dondurulmuş taban" tahmincisi ve bir " yan ağ " ek bir sinyal okuyor. yan ağın çıkışı sıfır olarak başlatılmış bir öğrenilebilir skalar tarafından kapalıdır (sıfır-conv versiyonumuz).

### Adım 1: LoRA matematik

```python
def lora(W, A, B, x, alpha=1.0):
    # W is frozen; A, B are the trainable low-rank factors.
    return [W[i][j] * x[j] for i, j in ...] + alpha * (B @ (A @ x))
```

### Adım 2: sıfır-bit yan ağ

```python
side_out = control_net(x, condition)
gated = gate * side_out  # gate initialized to 0
h = base(x) + gated
```

0'da çıkış, tabanla aynıdır.`gate`Yavaşça  felaketli bir sürükleme yok.

> İlk aşamada, baskı modeliyle tamamen aynı.`gate`更新缓慢 没有灾难性偏移──

## Tuzaklar.

- **Over-scaling LoRAs.** `α = 2`veya `α = 3`Bu, "güçlü yap" hack'in yaygın bir yöntemidir.`α ≤ 1.5`- Evet .
  **LoRA 过度缩放。** `α = 2`Ya da`α = 3`Bu, normalde "güçlendirilmiş" bir uygulama, aşırı bir şekilde biçimlendirilmiş/karşılaştırılmış bir üretim meydana getirir.`α ≤ 1.5`- Evet.
- **ControlNet weight conflict.**Pose ControlNet'in 1.0 ağırlıklı ve 1.0 ağırlıklı derinlik kontrol ağının kullanılması genellikle aşırı atışlar yapar.
  **ControlNet 权重冲突。**权重之和 ≈ 1.0 güvenlik için öntanımlı değerlerdir.
- **LoRA on the wrong base.**SDXL LoRA'sı sessizce SD 1.5'de çalışmıyor çünkü dikkat boyutları eşleşmiyor.
  **LoRA 用错基础模型。**SDXL LoRA SD 1.5'de sessizce hareketsizliğe sahiptir.
- **Textual Inversion drift.**Bir kontrol noktasında eğitilen tokenler diğerinde kötü hareket eder.
  **Textual Inversion 漂移。**Bir kontrol noktasında bir diğerinde ciddi bir hareket göstergesi vardır.
- **LoRA weight-merging and storage.**Daha hızlı sonuçlar için temel model ağırlıklarına bir LoRA pişirebilirsiniz (kurut zamanının eklenmesi yok), ancak ölçekleme yeteneğini kaybediyorsunuz `α`İkisi de kalsın.
  **LoRA 权重合并。**Basit modellerde düşünmeyi hızlandırabilir ama çalışmayı kaybetmekle düzenlenir.`α`- Yetenekleri...

## Çerçeveyi kullanın.

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

## İndirin . Ürünler .

- Kaydet .`outputs/skill-sd-toolkit-composer.md`. Yetenek bir görev alır (geleneksel varlıklar: hızlı, seçeneği referans görüntü, seçeneği poz, seçeneği derinlik, seçeneği kazıklama) ve araç yığın, ağırlıklar ve yeniden üretilebilir bir tohum protokolü çıkarır.

## Egzersizler.

1. **Easy / 简单.**İçeri`code/main.py`, LoRA sıralarını değiştirir .`r`1 ile 4 arasında, LoRA tam olarak 2. sırada bir hedef delta ile aynıdır.
   - Evet .`code/main.py`LRA 秩 中将`r`1'den 4'e kadar değişen bir zaman. Hangi sırada LoRA 2'ye uygun?
2. **Medium / 中等.**İki ayrı LoRA'yı iki hedef dönüşümüne çalıştırın. Onları bir araya getirin ve katılımcı etkileşimlerini gösterin.
   İki hedef değişiminde ayrı ayrı eğitim LoRA. Birlikte yüklenmek ve göstermek.
3. **Hard / 困难.**Düğme için difüzerler kullanın: SDXL-base + Canny-ControlNet (vezi 0,8) + bir stil LoRA (α 0,8) + IP-Adapter (vezi 0,6). Düğme ağırlıkları değiştikçe FID-vs-prompt-yapışma değişikliğini ölçün.
   FID ile birlikte 堆叠组合, ölçüm 

## Anahtar Şartlar .

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

## Üretim Notu: LoRA değişimi, ControlNet yolları, çoklu kiracı servisleri

Gerçek bir metin-yazar SaaS aynı temel kontrol noktasında yüzlerce LoRA ve bir düzine ControlNets'e hizmet verir. Servis sorunu LLM çok kiracılığına çok benziyor (prodüksiyon literatürü sürekli batching ve LoRAX / S-LoRA altında LLM durumunu kapsar):

- **Hot-swap LoRAs, do not merge.**Birleştirme`W' = W + α·B·A`Üstelik bu aşamada ~ 3-5% daha hızlı bir sonuç çıkarır ama dondurulur.`α`LRA'ları VRAM'da r sıra delta olarak sıcak tutun; difüzerler açığa çıkarır.`pipe.load_lora_weights()`+ `pipe.set_adapters([...], adapter_weights=[...])`Arama başına etkinleştirme için.`2 · d · r · num_layers`ağırlıklar  MB ölçeği, alt ikinci.
- **ControlNet as a second attention lane.**Klonlanmış kodlayıcı tabanla paralel olarak çalışır. Her biri 1.0 ağırlığında iki ControlNet = her adım için iki ekstra ileri geçiş, bir birleşik geçiş değil.
- **Quantized LoRAs too.**Temelini kuantleştirirseniz (Desin 07, 8GB'de akış) LoRA delta da temiz bir şekilde 8 bit veya 4 bit olarak kuantleştirir. QLoRA tarzında yükleme, hafızayı patlatmadan 4 bitlik bir Flux tabanının üzerine 5-10 LoRA'yı yığmanıza olanak sağlar.

Fluks-Specifik: Niels'in Flux-on-8GB bilgisayarı tabanı 4 bit olarak kvantize eder; LoRA (`pipe.load_lora_weights("user/style-lora")`) bu kuantitasyon tabanında `weight_name="pytorch_lora_weights.safetensors"`Bu, 2026'da çoğu SaaS ajansının gönderdiği reçete.

## Daha fazla okumak

- [Zhang, Rao, Agrawala (2023). Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543)Kontrol ağı.
- [Hu et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) LoRA (aslen LLM için; difüzyon için limanlar).
- [Ye et al. (2023). IP-Adapter: Text Compatible Image Prompt Adapter](https://arxiv.org/abs/2308.06721) IP Adaptörü.
- [Mou et al. (2023). T2I-Adapter: Learning Adapters to Dig Out More Controllable Ability](https://arxiv.org/abs/2302.08453) Kontrol Net'e daha hafif alternatif.
- [Ruiz et al. (2023). DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/abs/2208.12242)- Hayal sandalyesi.
- [HuggingFace Diffusers — ControlNet / LoRA / IP-Adapter docs](https://huggingface.co/docs/diffusers/training/controlnet) Referans boru hattı.
