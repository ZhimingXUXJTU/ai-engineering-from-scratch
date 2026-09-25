# Resim boyamak, resim boyamak ve resim düzenleme

> Metin-yazar yeni şeyler yapar. Renkleme eski şeyleri düzeltir. Üretimde, fatura edilebilir görüntü işinin %70'i düzenleme yapmaktadır.

> **【中文解读】**文本生成图像创造新东西,图像修复(油漆) değiştirmek mevcut olanları──制作中70%的付费图像工作是编辑换背景、去标志、扩展画布、重画手──油漆就是扩散模型真正钱的地方──

> **【拓展：Photoshop 生成式填充】**Adobe Photoshop'un üretimi biçimi (Generative Fill) incil yapımı teknolojisine dayanmaktadır.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 07 (Latent Diffusion / 潜在扩散), Phase 8 · 08 (ControlNet & LoRA)
**Time:** ~75 minutes

## Sorunlar. Sorunlar.

Bir müşteri arka planda dikkat dağıtan bir işaretle mükemmel bir ürün fotoğrafı gönderir. İşaretini silmek ve geri kalan her şeyi piksel-tıpkı bir şekilde bırakmak istiyorsunuz.

> 客户发来一张完美产品照片,背景有分散注意的标志――你想抹去标志并保持其他像素完全一致――你不能从头运行文生图结果将有不同的颜色、光照和产品角度――你想只重生*遮蔽区域*,并让重生内容尊重周围上下文――

Bu boyalama.

> İşte bu resim.

- **Inpainting.**Maske içinde yeniden canlandırın, piksellerin dışında kalın.
  **图像修复。**Sınırlı bir şekilde yeniden doğarken, dış görünümlerini korumak için.
- **Outpainting.**Maskenin dışına (veya kanvasın ötesine) geri dönüştürün, içeride kalın.
  **图像扩展。**İçinde kalın, dışarıda yeniden doğurun.
- **Image editing.**Tüm görüntüyü yeniden oluşturmak ancak orijinaline semantik veya yapısal sadakatini korumak (SDEdit, InstructPix2Pix).
  **图像编辑。**Tüm görüntüyü yeniden oluşturmak ama dil anlamını veya yapısal uyumluğunu korumak.

2026'da her difüzyon borusunda bir boyanma modunu gönderir. Flux.1-Fill, Stable Diffusion Inpaint, SDXL-Inpaint, DALL-E 3 Edit. Aynı prensip üzerinde çalışırlar.

> 2026 yıl her yayım su hattı boyanma 模式──Flux.1-Fill、SD-Inpaint、SDXL-Inpaint、DALL-E 3 Edit──原理相同──

> **【中文解读】**İnceleme (Images Repair) üretim ortamında en yaygın görüntü düzenleme ihtiyacıdır. Çabanın merkezi: sadece örtülü bölgeyi yeniden üretmek, aynı zamanda çevresindeki aşağıdaki metinle uyumlu davranmak. Doğru uygulama, değiştirilmiş U-Net'i eğitmek, 9 kanallı giriş yapmaktır.

> **【拓展：Photoshop 生成式填充与商业 Inpainting】**Adobe Photoshop'un oluşturduğu üslup, resim yapma teknolojisinin bir dönüm noktası uygulamasıdır. Genişleme modeli ve kenar birleşim teknolojisini birleştirir. Kullanıcıların doğal dil talimatları ile resimdeki herhangi bir içeriği kaldırma/değiştirmelerine izin verir.

## Konsepten bir şey.

![Inpainting: mask-aware denoising with context-preserving reinjection](../assets/inpainting.svg)

### Saf yaklaşım (ve neden yanlış)

> ### 朴素方法 (öntemli yöntem)

Maske ile standart metin-resim çalıştırın. Her örnekleme adımında gürültülü gizlilerin maske dışı bölgesi önüne yayılmış temiz görüntü ile değiştirin.

> Sınırlı bir şekilde, her örnekte bir bölgeyi değiştirmek için kullanılan standart resimler vardır.

### Doğru boyalama modeli

> ### Doğrudur Ressam

4 yerine 9 giriş kanalı alan değiştirilmiş U-Net'i çalıştır.

```
input = concat([ noisy_latent (4ch), encoded_image (4ch), mask (1ch) ], dim=channel)
```

Ekstra kanallar VAE kodlanmış kaynak resminin bir kopyasıdır ve bir tek kanal maskesi. Eğitim sırasında, görüntülerin rastgele bölgelerini maskelenir ve modelin maskeli bölgeyi sadece ifade etmesini eğitirken maskeli bölge temiz bir şartlama sinyali olarak verilir.

SD-Inpaint, SDXL-Inpaint, Flux-Fill hepsi bu 9 kanallı (veya analog) giriş kullanıyor.`StableDiffusionInpaintPipeline`- Evet .`FluxFillPipeline`- Evet .

> SD-Inpaint、SDXL-Inpaint、Flux-Fill 都使用这种9通道(或类似)输入──

### SDEdit (Meng et al., 2022)  ücretsiz düzenleme

> ### SDEdit  免费编辑

Kaynak görüntüsüne biraz ara ses ekleyin `t`, sonra ters zinciri çalıştır `t`Yeni bir çağrı ile 0'ya düştü.`t`Yaratıcı özgürlüğü için sadakat ticaretinde:

> Bir görüntü kaynağı, bir ortağa gürültü ver.`t`Sonra yeni bir hızla geriye doğru ses çıkarmak için tekrar çalışmak zorunda kalıyorsun.`t`Bu konuda bir seçim yapın.

- `t/T = 0.3`→ kaynağı ile neredeyse aynı, küçük stil değişimleri / 几乎与源相同,小风格变化
- `t/T = 0.6`→ moderat düzenlemeler, kaba yapıyı korur / 中等编辑,保留粗结构
- `t/T = 0.9`→ yakın gürültüden üretilen, minimum kaynak koruma / 从近噪声生成,最小源保留

### InstructPix2Pix (Brooks et al., 2023)

> ### InstructPix2Pix

Bir difüzyon modeliyi ince ayarlayın `(input_image, instruction, output_image)`Üçlü. Sonuçta, giriş görüntüde ve bir metin talimatında hem koşul ("güneş batmasını yapın", "ejderha ekleyin"). İki CFG ölçeği: görüntü ölçeği ve metin ölçeği.

> - Evet .`(输入图像, 指令, 输出图像)`Üç grup üzerinde küçük düzenli yayılma modeli¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

### RePaint (Lugmayr et al., 2022)

> ### Resimleme

Standart koşulsuz bir yayılma modeli tutun. Her ters adımda tekrar örnekleyin  ara sıra daha gürültülü bir duruma atlayın ve yenilenin. Sınır eserlerinden kaçının. Eğitimli bir boya modeli olmadığında kullanılır.

> 保持标准无条件扩散模型──在每反向步骤中重采样跳回更噪的状态重新生成──避免边界伪影──

## Yapın.
```figure
inpaint-mask-reinject
```

## Yapın

`code/main.py`Bu yöntem 5 boyutlu verilere 1 boyutlu boyama şeklini uyguluyor. Her örnek iki kümeden biriyle 5 tane yüzüyor. Sonuç olarak 5 boyuttan 2'sini "maske" ediyoruz, her adımda maskeli üçün gürültülü ön versiyonunu enjekte ediyoruz ve sadece maskeli boyutları yenilentiyoruz.

### Adım 1: 5-D DDPM verileri

```python
def sample_data(rng):
    cluster = rng.choice([0, 1])
    center = [-1.0] * 5 if cluster == 0 else [1.0] * 5
    return [c + rng.gauss(0, 0.2) for c in center], cluster
```

### Adım 2: 5 dims üzerinde tren denoiser

Standart DDPM. Ağ çıkışları 5 boyutlu gürültü girişleri için 5 boyutlu gürültü öngörüsü.

### Adım 3: Sonuçta, maskeden haberdar olan ters

```python
def inpaint_step(x_t, mask, clean_image, alpha_bars, t, rng):
    # replace unmasked dims with a freshly noised version of the clean source
    a_bar = alpha_bars[t]
    for i in range(len(x_t)):
        if not mask[i]:
            x_t[i] = math.sqrt(a_bar) * clean_image[i] + math.sqrt(1 - a_bar) * rng.gauss(0, 1)
    # ...then run the normal reverse step on x_t
```

Bu saf bir yaklaşım ve oyuncak 1 boyutlu veriler üzerinde çalışır. Gerçek görüntü boyaması 9 kanal girişini kullanır çünkü doku tutarlılığı daha önemlidir.

### Dördüncü adım: Çizgi

Çizgi maskası tersine boyanarak boyanır: yeni (önceden mevcut olmayan) kumaşı maskelenir, geri kalanını orijinal ile doldurun.

## Tuzaklar.

- **Seams.**Naif yaklaşım görünür sınırları bırakır çünkü gradient bilgileri maske boyunca akmaz. Düzelt: maskeyi 8-16 piksel genişlet veya uygun bir boya modeli kullanın.
- **Mask leakage.**Eğer maske görüntüsünün maske dışı bölgesi düşük kaliteli veya gürültülü ise maskenin içindeki nesli kirletiyor.
- **CFG interacts with mask size.**Küçük maske üzerinde yüksek CFG = doymuş yama. Küçük düzenlemeler için CFG azalt.
- **SDEdit fidelity cliff.**- Evet .`t/T = 0.5`- ...`t/T = 0.6`- Deneme ve kontrol noktası.
- **Prompt mismatch.**Bu mesaj sadece yeni içeriği değil, * bütün* görüntüyü tanımlamalıdır.

## Çerçeveyi kullanın.

| Task / 任务 | Pipeline / 方案 |
|------|----------|
| Remove object, small mask / 移除物体 | SD-Inpaint or Flux-Fill, standard prompt |
| Replace sky / 替换天空 | SD-Inpaint + "blue sky at sunset" |
| Extend canvas / 扩展画布 | SDXL outpaint mode (8px feather) or Flux-Fill with outpaint mask |
| Regenerate hand / face / 重画手/脸 | SD-Inpaint with prompt re-describing the subject + ControlNet-Openpose |
| Change style of one region / 改变区域风格 | SDEdit at `t/T=0.5` on masked region |
| "Make it sunset" / "变成日落" | InstructPix2Pix or Flux-Kontext |
| Background replacement / 背景替换 | SAM mask → SD-Inpaint |
| Ultra-high-fidelity / 超高保真 | Flux-Fill or GPT-Image (hosted) for hardest cases |

SAM (Meta'nın Segment Anything, 2023) + difüzyon boya 2026 arka plan kaldırma borusudur. SAM 2 (2024) video üzerinde çalışır.

> SAM(Meta'nın Segment Anything) + 扩散 inpaint is 2026 yılın背景移除流水线。SAM 2(2024)支持视频。

## İndirin . Ürünler .

- Kaydet .`outputs/skill-editing-pipeline.md`. Skill orijinal bir görüntü + düzenleme açıklaması + seçmeli maske (veya SAM sorgulaması) alır ve çıkışlar: mask-genreasyon yaklaşımı, temel model, CFG ölçekleri (resim + metin), SDEdit-t veya boyanma modu ve QA kontrol listesi.

## Egzersizler.

1. **Easy.**İçeri`code/main.py`, maskeli boyutların bölümü 0,2'den 0,8'e kadar değişir.
2. **Medium.**RePaint uygulamak: her 10. geri adımda 5 adım geri at (gürültü ekle) ve yeniden tanımlayın. Maskenin kenarında kalan sınırın azalıp azalmadığını ölçün.
3. **Hard.**Karşılaştırmak için Hugging Face difüzerlerini kullanın: SD 1.5 Inpaint + ControlNet-Openpose vs Flux.1- 20 yüz yenilenme görevini doldurun.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Inpainting | "Fill the hole" | Regenerate inside a mask; keep outside pixels. |
| Outpainting | "Extend the canvas" | Regenerate outside the canvas; keep inside. |
| 9-channel U-Net | "Proper inpainting model" | U-Net with `noisy \| encoded-source \| mask` as input. |
| SDEdit | "Img2img with noise level" | Noise to time `t`, denoise with new prompt. |
| InstructPix2Pix | "Text-only edits" | Fine-tuned diffusion on (image, instruction, output) triples. |
| RePaint | "No retraining" | Re-noise periodically during reverse to reduce seams. |
| SAM | "Segment Anything" | Mask generator by clicks or boxes; pairs with inpaint. |
| Flux-Kontext | "Edit with context" | Flux variant that accepts a reference image + instruction for edits. |

## Üretim Notu: düzenleme boru hattları gecikme hassasıdır

Bir görüntü düzenleyen kullanıcılar 5 saniyelik bir geri dönüş bekler. 10242'de 30 adımlı SDXL-Inpaint, L4'te 3-4 saniye, SAM maskesi üretimi (~ 200 ms) ve VAE kodlama/dekodlama (~ 500 ms birleştirilmiştir).

- **SAM-H is the slow one.**SAM-H 10242'de ~200 ms; SAM-ViT-B ise ~40 ms küçük kalite kaybı ile. SAM 2 (video) zamanlı overhead ekler; tek görüntü düzenlemeleri için kullanmayın.
- **Skip the encode when possible.** `pipe.image_processor.preprocess(img)`Eğer önceki neslinin latenti varsa (iteratif düzenleme UI'lerinde tipik), doğrudan `latents=...`Bir VAE kodunu atlamak için.
- **Mask dilation matters for throughput too.**Küçük bir maske, U-Net ileri geçişinin çoğunun boşa gittiğini (maske dışı pikseller her neyse sıkıştırılır) gösterir. `diffusers`"`StableDiffusionInpaintPipeline`U-Net'in tümünü kullanır. Sadece 9 kanallı düzgün boyama sürümleri maskeli hesaplama kullanır.
- **Flux-Kontext is the 2025 answer.**Tek ileri geçiş .`(source_image, instruction)`H100'de bir düzenleme yaklaşık 1,5 saniye içinde gönderir. Mimarlık dersi: aşamaları çöktür.

## Daha fazla okumak

- [Lugmayr et al. (2022). RePaint: Inpainting using Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2201.09865) eğitimsiz boyanma.
- [Meng et al. (2022). SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations](https://arxiv.org/abs/2108.01073)- Öldürülmüş.
- [Brooks, Holynski, Efros (2023). InstructPix2Pix](https://arxiv.org/abs/2211.09800) metin talimatları düzenleme.
- [Kirillov et al. (2023). Segment Anything](https://arxiv.org/abs/2304.02643)SAM, maske kaynağı.
- [Ravi et al. (2024). SAM 2: Segment Anything in Images and Videos](https://arxiv.org/abs/2408.00714) Video SAM.
- [Hertz et al. (2022). Prompt-to-Prompt Image Editing with Cross-Attention Control](https://arxiv.org/abs/2208.01626) Dikkat düzeyinde düzenleme.
- [Black Forest Labs (2024). Flux.1-Fill and Flux.1-Kontext](https://blackforestlabs.ai/flux-1-tools/)2024 araçları.
