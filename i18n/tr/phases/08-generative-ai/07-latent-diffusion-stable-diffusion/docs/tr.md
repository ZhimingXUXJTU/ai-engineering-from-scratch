# Latent Diffusion & Stable Diffusion.

> Rombach ve diğerleri (2022) bir görüntü oluşturmak için tüm 786k boyutlarına ihtiyacınız olmadığını fark etti.

> **【中文解读】**512x512 像素空间做扩散是计算灾难──Rombach 等人发现不需要全部 78.6万维度只需捕获语义结构,剩余用解码器补充──在VAE'deki潜在空间中运行扩散,这个想法就是稳定的扩散──

> **【拓展：Stable Diffusion 的革命】**Stabil Diffusion, genişleme sürecini, bir görüntü boşluğundan potansiyel boşluğa taşıyacak, hesaplama miktarını on kat daha az düşürecek, tüketim seviyesindeki GPU'ları çalıştırmak için kullanılabilir hale getirecek. Açık kaynak yayınlanmasından sonra LoRA, ControlNet ve diğerleri zengin bir ekosistem yaratmıştır ve AIGC'nin yaygınlaşmasına katkıda bulunmaktadır.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 02 (VAE), Phase 8 · 06 (DDPM), Phase 7 · 09 (ViT)
**Time:** ~75 minutes

## Sorunlar. Sorunlar.

5122 ' de piksel-uzayda yayılma U-Net ' in şekil tensörleri üzerinde çalışmasını sağlar .`[B, 3, 512, 512]`Her örnekleme adımı 500M-param U-Net için ~100 GFLOPS. 50 adım bir görüntü başına 5 TFLOPS. Bir milyar görüntü üzerinde çalıştırın ve hesaplama faturu saçmalık.

> 5122 像素空间扩散 anlamı U-Net'in içinde`[B, 3, 512, 512]`张量上运行──每采样步约100 GFLOPS──50 步就是5 TFLOPS──在十亿图像上训练计算成本荒谬──

Bu FLOP'lerin çoğu, kaybeden bir VAE'nin sıkıştırdığı yüksek frekanslı dokuyu ağ üzerinden algılamaca önemsiz detayları itmeye gider. Rombach'un fikri: bir VAE'yi bir kez (* birinci aşama*) eğitmek, dondurmak ve tamamen 4 kanal 64×64 gizli alanında (* ikinci aşama*) yayılmayı çalıştırmak. Aynı U-Net.

> Büyük bölüm FLOPs, duyuru üzerinde önemli olmayan ayrıntıları ileri sürmek için kullanılır. Rombach'ın fikri: VAE'yi bir kez eğitmek, tamamıyla 4 通道 64×64 潜在空间运行扩散, tamamıyla bitmek.

Bu, Stable Diffusion tarifi. SD 1.x / 2.x 860M U-Net kullanıyor.`64×64×4`SDXL'de 2.6B U-Net kullanıldı.`128×128×4`, SD3 U-Net'i akış eşleşmesi ile bir Diffusion Transformer (DiT) ile değiştirdi. Flux.1-dev (Black Forest Labs, 2024) 12B-param DiT-MMDiT'yi gönderir. Hepsi aynı iki aşamalı altyapıda çalışır.

> İşte Stabil Diffusion'un bir üsulu. SD 1.x/2.x 860M U-Net'le 64×64×4'e, SDXL 2.6B U-Net'le 128×128×4'e, SD3 DiT + Flow Matching ile U-Net'i değiştirmek. Flux.1-dev 12B MMDiT'le birlikte aynı iki aşamada çalışmaktadır.

> **【中文解读】**Stable Diffusion'in çekirdek yapısı iki aşamalı tasarımdır: 1) Birinci aşamalı VAE kodlayıcı 512x512 ıfsı sıkıştırarak 64x64x4  potansiyel uzay  16 ıfsı sıkıştırarak; 2) İkinci aşamalı ıfsı genişletilme sürecinde çalışmaktadır.

> **【拓展：从 U-Net 到 DiT 的架构变迁】**SD 1.x/2.x U-Net'i kullanmak Delargio Network olarak──SD3(2024) y FLUX 转向 DiT(Diffusion Transformer) U-Net'i değiştirmek için Transformer kullanmak  DiT'in avantajları genişleme daha iyiymiş.

## Konsepten bir şey.

![Latent diffusion: VAE compression + diffusion in latent space](../assets/latent-diffusion.svg)

**Two stages, separately trained.**

> **两个阶段，分别训练。**

1. **Stage 1 — VAE.**Kodlayıcı`E(x) → z`, dekodör`D(z) → x`. Hedef sıkıştırma: her alan eksisinde 8× aşağı örnek + kanalları ayarlayın böylece toplam gizli boyut piksel sayısının 1/16'sidir. Kayıp = yeniden yapılandırma (L1 + LPIPS algılama) + KL (küçük ağırlık böylece `z`Bu çok Gaussian zorunlu değil, çünkü tam örnekleme ihtiyacımız yok.`z`Genellikle bir düşmana karşı bir kayıpla eğitilmiştir. Bu yüzden kodlanmış görüntüler keskin.

   **阶段 1 — VAE。**编码器 `E(x) → z`, çözücü `D(z) → x`△ hedef basınç: 每空间轴 8 倍下采样──损失 = 重建(L1 + LPIPS) + KL(小权重)。

2. **Stage 2 — diffusion on `z`.**Tedavi et .`z = E(x_real)`Bir U-Net (veya DiT) 'yi denetlemeyi eğit.`z_t`Sonuçta: örnek`z_0`O zaman difüzyondan.`x = D(z_0)`- Evet .

   **阶段 2 — 在 `z` 上扩散。**- Ben de .`z = E(x_real)`视为数据──训练 U-Net(或 DiT) 去噪──推理时:采样 `z_0`Sonra ...`x = D(z_0)`- Evet.

**Text conditioning.**İki ek bileşen. Dondurulmuş bir metin kodlayıcısı (SD 1.x için CLIP-L, SD 2/XL için CLIP-L+OpenCLIP-G, SD3 ve Flux için T5-XXL).`[Q = image features, K = V = text tokens]`Tek yol metin görüntüyü etkilemektir.

> **文本条件化。**结的文本编码器和交叉注意注入──每个 U-Net 块用 结的文本编码器和交叉注意注入──`[Q = 图像特征, K = V = 文本 token]`Yapmak için dikkat çekmek. Token, metin'in resme etkisiyle etkilemesinin tek yolu.

**The loss function is identical to Lesson 06.**Aynı DDPM / akış eşleşen MSE gürültü. Sadece veri alanı değiştirmek.

> **损失函数与第 06 课完全相同。**Sadece veri alanı değişti.

## Yapısal değişimler.

| Model / 模型 | Year | Backbone / 骨干 | Latent shape / 潜在形状 | Text encoder / 文本编码器 | Params / 参数量 |
|-------|------|----------|--------------|--------------|--------|
| SD 1.5 | 2022 | U-Net | 64×64×4 | CLIP-L (77 tokens) | 860M |
| SD 2.1 | 2022 | U-Net | 64×64×4 | OpenCLIP-H | 865M |
| SDXL | 2023 | U-Net + refiner | 128×128×4 | CLIP-L + OpenCLIP-G | 2.6B + 6.6B |
| SDXL-Turbo | 2023 | Distilled | 128×128×4 | same | 1-4 step sampling / 1-4 步采样 |
| SD3 | 2024 | MMDiT (multimodal DiT) | 128×128×16 | T5-XXL + CLIP-L + CLIP-G | 2B / 8B |
| Flux.1-dev | 2024 | MMDiT | 128×128×16 | T5-XXL + CLIP-L | 12B |
| Flux.1-schnell | 2024 | MMDiT distilled | 128×128×16 | T5-XXL + CLIP-L | 12B, 1-4 step |

Eğilim: U-Net'i DiT (lakent yamalar üzerinde transformatör) ile değiştirin, metin kodlayıcısını ölçeklendirin (T5 hızlı bir şekilde takip için CLIP'i yener), latent kanalları artırın (4 → 16 daha fazla ayrıntılı bir yer verir).

> 趋势: DiT 替代U-Net,扩展文本编码器(T5 在 prompt 遵循上优于CLIP),增加潜在通道(4→16 给更多细节余量)

## Yapın.
```figure
noise-schedule
```

## Yapın

`code/main.py`Ders 06'dan DDPM'nin üstüne bir oyuncak 1-D "VAE" (tıpkı gösterim için kimlik kodlayıcı + dekoder; gerçek bir VAE bir konfor ağı olurdu) yığar ve sınıflandırıcı-sağ rehberliği ile sınıf koşullandırmasını ekler.

> `code/main.py`6. Sınıfın DDPM'sine bir oyuncak 1D "VAE" eklendi ve sınıflandırma koşullandırılmış bir sınıflandırma yöneticisi eklendi.

### Adım 1: Kodlayıcı/Kodlayıcı

```python
def encode(x):    return x * 0.5          # toy "compression" to smaller scale
def decode(z):    return z * 2.0
```

Gerçek bir VAE'nin eğitimli ağırlıkları vardır.`z`Orijinal veri alanını önemsemeden.

> Gerçek VAE'nin iyi eğitimli bir ağırlığı var.`z`Ün Operasyon ve Kaygılanma

### İkinci adım: `z`- Uzay

DDPM'nin 06. dersiyle aynı.`z = E(x)`Örnek alınca`z_0`,  ile çözülür .`D(z_0)`- Evet .

> 6. Sınıf ile aynı DDPM.`z = E(x)`                                                                                                                                                                                                                                                              `z_0`Son kullanımı`D(z_0)`Çözüm.

### Adım 3: sınıflandırıcı dışı rehberlik

Eğitim sırasında sınıf etiketini %10'da bırakın (sürekli bir simge ile değiştirin).`ε_cond`ve `ε_uncond`O zaman:

```python
eps_cfg = (1 + w) * eps_cond - w * eps_uncond
```

`w = 0`= rehberlik yok (tam çeşitlilik),`w = 3`= default, `w = 7+`= doymuş / aşırı keskin.

> `w = 0`= 无引导(完全多样性),`w = 3`= 默认,`w = 7+`= 和/过度利。

### Adım 4: Metin koşullandırması (konsept, kod değil)

Sınıf etiketini dondurulmuş bir metin kodlayıcı çıkışı ile değiştirin. U-Net'e gömülü metni çapraz dikkat yoluyla besleyin:

> Metin kodlayıcı, metin içeriğini U-Net'e göndermek için bir araç oluşturur.

```python
h = h + CrossAttention(Q=h, K=text_embed, V=text_embed)
```

Bu, sınıf koşullı bir difüzyon modeli ile sabit difüzyon arasındaki tek önemli fark.

> Bu, sınıf koşulları yayılma modeli ile sabit dağılım arasındaki tek gerçek farkıdır.

## Tuzaklar.

- **VAE-scale mismatch.**SD 1.x VAE'ler ölçekleme sabitine sahiptir (`scaling_factor ≈ 0.18215`Bu, U-Net'in çok yanlış bir değişim ile gizli bir şekilde çalışmasını sağlar.
  **VAE 尺度不匹配。**SD 1.x VAE  kodlama sonrası kısaltılmış konular vardır. U-Net'in hata farkı potansiyel alan üzerinde eğitim görmesini sağlar.
- **Text encoder silently wrong.**SD3'nin T5-XXL'ye ihtiyacı var ve T5 = 128 tokeni vardır.`use_t5=True`Ya da hızlı sadakat kraterleri.
  **文本编码器静默错误。**SD3 需要 T5-XXL 且 >=128 token──
- **Mixing latent spaces.**SDXL, SD3, Flux hepsi farklı VAE'ler kullanır. SDXL latenti üzerinde eğitilmiş bir LoRA SD3 üzerinde çalışmaz.
  **混合潜在空间。**SDXL、SD3、Flux farklı VAE¬lerle SDXL'nin LoRA'sı SD3'de kullanılamaz.
- **CFG too high.** `w > 10`Doymuş, yağlı görüntüler üretir ve çeşitlilik masrafına karşı uyarıyı aşırı uyarır.`w = 3-7`- Evet .
  **CFG 太高。** `w > 10`产生和、油的图像──
- **Negative prompts leaking.**Boş negatif istek sıfır simge olur; doldurulmuş negatif istek `ε_uncond`Bunlar aynı değil; bazı boru hattları sessizce sıfır açılır.
  **负向 prompt 泄漏。**空负向 prompt 变为零代币; doldur 变为`ε_uncond`İki farklı şey var.

## Çerçeveyi kullanın.

2026'da üretim aşamaları:

> 2026 yıl üretim teknolojisi:

| Target / 目标 | Recommended backbone / 推荐骨干 |
|--------|----------------------|
| Narrow domain, paired data, from scratch / 窄域配对从零训练 | SDXL fine-tune (LoRA / full) — fastest to ship |
| Open-domain text-to-image, open weights / 开放域开放权重 | Flux.1-dev (12B, Apache / non-commercial) or SD3.5-Large |
| Fastest inference, open weights / 最快推理开放权重 | Flux.1-schnell (1-4 step, Apache) or SDXL-Lightning |
| Best prompt adherence, hosted / 最佳 prompt 遵循，托管 | GPT-Image / DALL-E 3, Midjourney v7, Imagen 4 |
| Edit workflows / 编辑工作流 | Flux.1-Kontext (Dec 2024) — natively accepts image + text |
| Research, baseline / 研究基线 | SD 1.5 — ancient but well-studied |

## İndirin . Ürünler .

- Kaydet .`outputs/skill-sd-prompter.md`. Skill bir metin uyarısı + hedef stil ve çıkışları alır: model + kontrol noktası, CFG ölçeği, örnekleme, negatif uyarı, çözünürlük, seçmeli ControlNet/IP-Adapter kombinasyonu ve adım başına bir kalite kontrol listesi.

> 保存 `outputs/skill-sd-prompter.md`◊Skill 接收文本提示+目标风格,输出模型+检查点、CFG、采样器、负向提示等──

## Egzersizler.

1. **Easy / 简单.**Çık .`code/main.py`Yönlendirmelerle`w ∈ {0, 1, 3, 7, 15}`Sınıflara göre ortalama örnek kaydet.`w`sınıf anlamları gerçek verilerin anlamlarından daha uzak mı?
   Kullan .`w ∈ {0, 1, 3, 7, 15}`- Ne oldu?`w`Value de classe moyenne de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur de valeur
2. **Medium / 中等.**Oyuncak çizgisi kodlayıcıyı yeniden yapılandırma kaybı olan tanh-MLP kodlayıcı/dekoder çiftine değiştirin. Yeni latentlerde yayılımı yeniden eğit. Örnek kalitesi değişiyor mu?
   Oyuncak Linear Kodlayıcı Tanh-MLP Kodlama/Kodleme Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama Uygulama U
3. **Hard / 困难.**Düzenleyici ile gerçek Stable Diffusion inference ayarlayın: yük `sdxl-base`CFG=7 ile 30 Euler adımı at.`sdxl-turbo`Aynı konu, farklı kalite  neyin değiştiğini ve neden değiştiğini açıklayın.
   Sıfırlayıcılar kullanın 搭建真实SD 推理,比较SDXL-base 和SDXL-Turbo──

## Anahtar Şartlar .

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

## Üretim Notu: 8GB tüketici GPU'da Flux-12B çalıştırmak

Referans Flux entegrasyonu kanonik "Benim tüketici bir GPU var, bunu gönderebilir miyim?" tarifi.

> 参考流集成是经典的"Min sadece tüketim seviyesindeki GPU,能部署吗?"方案──三旋方案:

1. **Staggered loading.**Flux'in VRAM'da birlikte yaşamaya ihtiyacı olmayan üç ağı vardır: T5-XXL metin kodleyicisi (fp32'de ~ 10 GB), CLIP-L (küçük), 12B MMDiT ve VAE. Önce istekle kodlayın, * kodlayıcıları silin, DiT'yi yükleyin, denoise, * delete* DiT'yi yükleyin, VAE'yi yükleyin, dekode edin.
   **交错加载。**Flus var üç zaman içinde VRAM'ın ağında kalmak zorunda değil.
2. **4-bit quantization via bitsandbytes.** `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)`T5 kodlayıcı ve DiT'de. 8× hafıza keser, Aritra'nın referans değerleri (notbukta bağlantılı) için metin-resim oranında kalitede düşüş algılanamaz.
   **4 位量化。**T5 ve DiT'yi 4 bit'e kadar ölçevelemek,内存 8 kat düşmek, kalite kaybı azdır.
3. **CPU offload.** `pipe.enable_model_cpu_offload()`CPU ve GPU arasında otomatik olarak modül değiştirir. Her ileri geçiş ilerlerken, %10-20 gecikme artırır.
   **CPU 卸载。**Otomatik olarak CPU ve GPU arasında değişim modülleri. % 10-20 artarken, akım hattı çalışmaya devam eder.

Hatıra muhasebe: `10 GB T5 / 8 = 1.25 GB`Kvantistik olarak`12 B params × 0.5 bytes = ~6 GB`TP=1 sonucu  model paralelliği, maksimum kuantitasyon. üretim için H100'lerde TP=2 veya TP=4 çalıştırırsınız; tek bir dev dizüstü bilgisayar için, bu tarif.

## Daha fazla okumak

- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) Dönüştürülme.
- [Podell et al. (2023). SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis](https://arxiv.org/abs/2307.01952) SDXL.
- [Peebles & Xie (2023). Scalable Diffusion Models with Transformers (DiT)](https://arxiv.org/abs/2212.09748)- DiT.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) SD3, MMDiT.
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598)CFG.
- [Labs (2024). Flux.1 — Black Forest Labs announcement](https://blackforestlabs.ai/announcing-black-forest-labs/) Flux.1 ailesi.
- [Hugging Face Diffusers docs](https://huggingface.co/docs/diffusers/index) yukarıdaki her kontrol noktası için referans uygulanması.
