# Şartlı GAN & Pix2Pix.  Şartlı GAN & Pix2Pix

> 2014-2017 yıllarındaki ilk büyük kilitleme, bir GAN'ın ne yaptığını kontrol etmekti. Bir etiket, ya da bir görüntü veya bir cümle ekleyin. Pix2Pix görüntü sürümünü yaptı ve hala dar bir görüntüden görüntüye görevlerde her genel metin-resim modeliyi yendi.

> **【中文解读】**2014-2017 yıllarındaki ilk büyük atılım GAN'ı kontrol etmekti. GAN: Üzer etiket, resim veya metin üretimi. Pix2Pix, resim sürümünü yaptı.

> **【拓展：Pix2Pix 的应用】**Pix2Pix "İsmetler Bilgiye İnceleme" biçimini başlattı:素描→写真、白天→夜晚、线稿→彩色图── bu biçim daha sonra ControlNet tarafından miras alınmıştır ve geliştirilmiştir──

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 06 (U-Net), Phase 3 · 07 (CNNs / 卷积神经网络)
**Time:** ~75 minutes

## Sorunlar. Sorunlar.

Şartsız bir GAN, keyfi yüzlere örnekler verir. Demo için yararlı, üretim için işe yaramaz. İsterseniz: * bir çizim resmi, * bir hava fotoğrafı haritası, * gündüz sahnesini gece haritası, * gri ölçekli bir resmini renklendirin.`x`ve çıkış yaptırmalı.`y`Bazı anlamlı bir karşılıklılık ile.`y`S / `x`Ortalama kare hatası onları bir karışıklığa dönüştürür.

> 无条件 GAN 采样任意人脸──适合演示,不适合生产──你想要的是:*将素描映射为照片*、*将地图映射为航拍图*、*将白天映射为夜*、*给灰度图上色*──在所有这些场景中,给定输入图像`x`, anlamlı bir ilişki çıkartmak zorundadır.`y`Herkes.`x`Çok mantıklı bir şey var.`y`                                                                                                                                                                                                                                                              

Şartlı GAN (Mirza & Osindero, 2014) bir şart ekler `c`Her ikisine de bir giriş olarak `G`ve `D`Pix2Pix (Isola et al., 2017) bunu uzmanlaştırdı: koşul tam bir giriş görüntüsüdür, jeneratör bir U-Net, ayrımcı bir * patch tabanlı* sınıflandırıcıdır (PatchGAN), ve kayıp + L1'dir. Bu tarif 2026'da bile dar görüntü-resim alanlarında sıfırdan metin-resim modelleri üzerinde daha iyi performans gösteriyor çünkü * çift veriler* üzerinde eğitilmiştir.

> 条件 GAN(2014) `G`和 `D`İçeri girdi `c`◊Pix2Pix(2017) bunu özelleştirdi: şartı tam olarak girdilik görüntü, jeneratör U-Net, ayırt edici PatchGAN, kayb = karşı karşı + L1── bu program 2026 yılında bile, daha sıkı bir görüntü çevirisi görevinde, baştan eğitimli bir yaşam resim modeliden daha iyidir, çünkü bu, * veriyi* birlikte eğitmek için ne ihtiyacınız olan sinyaller vardır.

> **【中文解读】**条件 GAN'ın çekirdek geliştirilmesi: c¬¬Pix2Pix'in koşulları tam olarak giriş görüntü, üreticiden U-Net'de ((reserve space detail), ayırt edici ile PatchGAN'da ((plactical image block) ∼ loss = anti-loss + L1 损失── bu tür bir veri antrenmanı, bugün bile eng domen görüntü çevirisi görevlerinde genel metin oluşturma görüntü modeliden daha iyidir.

> **【拓展：从 Pix2Pix 到 ControlNet 的演进】**Pix2Pix'in "izgi koşulları üretimi" fikri ControlNet tarafından 2023 yılında devralınıp geliştirildi. ControlNet koşulları kontrol edecek.

## Konsepten bir şey.

![Pix2Pix: U-Net generator, PatchGAN discriminator](../assets/pix2pix.svg)

**Conditional G.** `G(x, z) → y`Pix2Pix'te.`z`G içindeki çıkış (gelen gelse gelen gürültü yok  Açık gürültü izole edilmedi).

> **条件生成器 G。** `G(x, z) → y`Pix2Pix'te,`z`G 内部的落下 (G 内部的落下) 无输入噪音Isola 发现显式噪音会被忽略) 

**Conditional D.** `D(x, y) → [0, 1]`Giriş * çift* (şart, çıkış) bu ana fark: D'nin `y` ile uyumludur`x`Sadece ...`y`Gerçek görünüyor.

> **条件判别器 D。** `D(x, y) → [0, 1]`◊输入是*配对*(条件,输出) ・关键区别:D 必须判断 `y`Evet veya değil`x`Birliği, sadece değil.`y`Gerçek gibi görünüyor.

**U-Net generator.**Boş boynuz üzerinden atlama bağlantıları olan kodlayıcı-dekoder. Giriş ve çıkış düşük düzeyde bir yapı paylaşan görevler için kritik. Atlamalar olmadan, yüksek frekanslı detaylar kaybolur.

> **U-Net 生成器。**带有跳跃连接的编码器-解码器──输入输出共享低级结构的任务至关重要──没有跳跃连接,高频细节会消失──

**PatchGAN discriminator.**Tek gerçek/sahte puan vermek yerine, D bir `N×N`Bu, Markov'un rastgele alan varsayımıdır: gerçekçilik yerel. Eğitmek çok daha hızlı, daha az parametreler, daha keskin çıkış.

> **PatchGAN 判别器。**D 输出 `N×N`网格而非单一真/假分数,每个单元判断约70×70 像素的感受野──这是马尔可夫随机场假设:真实感是局部的──训练更快,参数更少,输出更利──

**Loss.**

```
loss_G = -log D(x, G(x)) + λ · ||y - G(x)||_1
loss_D = -log D(x, y) - log (1 - D(x, G(x)))
```

L1 terimi eğitimleri istikrarlı hale getirir ve G'yi bilinen hedefe doğru itirir. L1 L2'den daha keskin kenarlar verir (ortalar, ortalama değil). `λ = 100`Pix2Pix'in öntanımlı olduğu.

> L1 项稳定训练并推动 G 趋向已知目标──L1 比 L2 产生更利的边缘(中位数 vs 平均值)──`λ = 100`Pix2Pix'in öntanımlı değeri.

## CycleGAN  çift olmadığında  CycleGAN                                                                                                                                                                                                                                                        

Pix2Pix çiftleştirilmelidir `(x, y)`CycleGAN (Zhu et al., 2017) bu gereksinimleri bir ekstra kaybın bedeliyle düşürüyor: * döngü tutarlılığı kaybı.`G: X → Y`ve `F: Y → X`- Onları eğit .`F(G(x)) ≈ x`ve `G(F(y)) ≈ y`Bu atları zebralara çevirmenizi sağlar, yazdan kışa, çiftli örnekler olmadan.

> Pix2Pix  需要配对 `(x, y)`Data──CycleGAN(2017) bu talebi reddetti, fiyat ek döngü uyumluluk kaybı── iki jeneratör`G: X → Y`和 `F: Y → X`, trenle `F(G(x)) ≈ x`和 `G(F(y)) ≈ y`Bu seni bir örnekle karşılaştırmak zorunda bırakmaz.

2026'da eşleşmemiş görüntü-resim çoğunlukla CycleGAN yerine difüzyon (ControlNet, IP-Adapter) yoluyla yapılır, ancak döngü tutarlılığı fikri neredeyse her eşleşmemiş alan uyarlama kağıdında hayatta kalır.

> 2026 yılında, çakıl uyum düşüncesi tamamlanmak yerine, kontrolnet, IP-adapter (ControlNet, IP-Adapter) tarafından yayılmış bir modelle gerçekleşmiştir.

## Yapın.
```figure
gx-patchgan
```

## Yapın

`code/main.py`1 boyutlu verilere küçük bir şartlı GAN uyguluyor.`c`sınıf etiketidir (0 veya 1). Görev: verilen sınıf için koşullu dağılımdan bir örnek üretmek.

> `code/main.py`Bir boyutlu veri üzerinde bir mikro tip koşullar GAN  koşulları gerçekleştirmek.`c`Yapılan çalışmaların birbiriyle ilgili olarak, bu çalışmaların birbiriyle ilgili olarak, bir diğer çalışmaların birbiriyle ilgili olarak, bir diğer çalışmaların birbiriyle ilgili olarak, bir diğer çalışmaların birbiriyle ilgili olarak, bir diğer çalışmaların birbiriyle ilgili olarak, bir diğer çalışmaların birbiriyle ilgili olarak, bir diğer çalışmaların birbiriyle ilgili olarak, bir diğer çalışmaların bir parçası olarak, bir diğer çalışmaların bir diğer çalışma biçimi olarak, bir diğer çalışma biçimi olarak, bir diğer çalışma biçimi olarak, bir diğer çalışma biçimi olarak, bir diğer çalışma biçimi olarak, bir diğer çalışma biçimi olarak, bir diğer çalışma biçimi olarak, bir diğer çalışma biçimi olarak, bir çalışma biçimi olarak, bir çalışma biçimi olarak, bir çalışma biçimi olarak, bir çalışma biçimi olarak, bir çalışma biçimi olarak, bir çalışma biçimi olarak, bir çalışma biçimi olarak, bir çalışma biçimi olarak, bir çalışma biçimi olarak, bir çalışma biçimi olarak, bir çalışma biçimi olarak, bir çalışma biçimlendirilmiş bir iş olarak, bir çalışma biçim olarak, bir çalışma biçimlendirilmiş bir iş olarak, bir çalışma biçim olarak, bir çalışma biçimlendirilmiş bir iş olarak, bir çalışma biçimlendirilmiş bir iş olarak, bir iş olarak, bir iş olarak, bir iş olarak, bir iş olarak, bir iş olarak, bir iş olarak, bir iş olarak, bir iş olarak, bir iş olarak, bir iş olarak, bir iş olarak, bir iş olarak, bir atfedilmiştir.

### Adım 1: G ve D girişlerine koşul ekle

```python
def G(z, c, params):
    return mlp(concat([z, one_hot(c)]), params)

def D(x, c, params):
    return mlp(concat([x, one_hot(c)]), params)
```

En büyük modeller öğrenilmiş yerleşimleri, FiLM modülasyonunu veya çapraz dikkatini kullanır.

> Tek sıcak 编码 en basit yöntemdir. Daha büyük modeller, 嵌入学, FiLM 调制或交叉注意力, 编码的方法.

### Adım 2: Şartlı tren

```python
for step in range(steps):
    x, c = sample_real_conditional()
    noise = sample_noise()
    update_D(x_real=x, x_fake=G(noise, c), c=c)
    update_G(noise, c)
```

Generatör, verilen koşul için *gerçek dağılım * ile eşleşmelidir, kenarlık değil.

> Ürünler, sınırlı dağılım yerine, belirli koşullar altında gerçek dağılımlara uyum sağlamalıdır.

### Adım 3: Sınıf başına çıkışı doğrulayın

```python
for c in [0, 1]:
    samples = [G(noise, c) for noise in batch]
    mean_c = mean(samples)
    assert_near(mean_c, real_mean_for_class_c)
```

## Tuzaklar.

- **Condition ignored.**G sınır dışı bırakmayı öğrenir, D asla cezalandırmaz çünkü durum sinyali zayıfdır. D durumu daha agresif bir şekilde (başka katman, sadece geç değil) düzeltir, projeksiyon ayrımcılığını kullan (Miyato & Koyama 2018).
  **条件被忽略。**G öğrenmiş, sınır dışı, D ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından ından  ından      ından    ından     ından  ından     ından    ından    ından      ından      ından       ından          ından             ından                                                                                                      
- **L1 weight too low.**G, sadık olmayan keyfi gerçek görünümlü çıkışlara doğru hareket eder.
  **L1 权重太低。**G 偏移到任意看起来真实输出──Pix2Pix 任务从 λ≈100 开始──
- **L1 weight too high.**G, L1'nin hala L_p norması olduğu için bulanık çıkışlar üretir.
  **L1 权重太高。**G 产生模糊输出──训练稳定后逐渐降低──
- **Ground-truth leakage in D.**Konkatenat `(x, y)`Sadece değil, D giriş olarak.`y`Bu D olmadan tutarlılığı kontrol edemezsiniz.
  **D 中的真值泄漏。**- Ben de .`(x, y)`拼接为 D 的输入,而非仅仅 `y`- Evet.
- **Mode collapse per class.**Her sınıf bağımsız olarak çökebilir.
  **每类模式坍塌。**Her sınıf bağımsız çöküşe neden olabilir.

## Çerçeveyi kullanın.

2026 görüntü-resim görevlerinin durumu:

> 2026 Yıllık görüntüden görüntü görevine:

| Task / 任务 | Best approach / 最佳方案 |
|------|---------------|
| Sketch → photo, same domain, paired data / 素描→照片，配对数据 | Pix2Pix / Pix2PixHD (still fast, still sharp) |
| Sketch → photo, unpaired / 素描→照片，非配对 | ControlNet with a Scribble conditioning model |
| Semantic seg → photo / 语义分割→照片 | SPADE / GauGAN2 or SD + ControlNet-Seg |
| Style transfer / 风格迁移 | Diffusion with IP-Adapter or LoRA; GAN methods are legacy |
| Depth → photo / 深度→照片 | ControlNet-Depth over Stable Diffusion |
| Super-resolution / 超分辨率 | Real-ESRGAN (GAN), ESRGAN-Plus, or SD-Upscale (diffusion) |
| Colorization / 上色 | ColTran, diffusion-based colorizers, or Pix2Pix-color |
| Daytime → nighttime, seasons, weather / 白天→夜晚 | CycleGAN or ControlNet-based |

Pix2Pix, (a) binlerce çift örneğe sahip olduğunuzda, (b) görev dar ve tekrarlanabilir ve (c) hızlı bir sonuç almanız gerektiğinde doğru araç olarak kalır.

> Pix2Pix'in şu durumları hala doğru araç: a) binlerce çift örnek var, b) görev kısadır ve tekrarlanabilir, c) hızlı bir şekilde düşünülmesi gerekir,

## İndirin . Ürünler .

- Kaydet .`outputs/skill-img2img-chooser.md`. Yetenek bir görev açıklaması, veri kullanılabilirliği (birleştirilmiş vs eşleştirilmemiş, N örnekler) ve gecikme/kalite bütçesi alır, sonra çıkışlar: yaklaşım (Pix2Pix, CycleGAN, ControlNet varianti, SDXL + IP-Adapter), eğitim veri gereksinimleri, sonucu maliyeti ve değerlendirme protokolü (LPIPS, FID, görev-özel).

> 保存 `outputs/skill-img2img-chooser.md`◊Bilgi alım görev tanımlaması, veri kullanılabilirliği ve gecikme/kalit bütçesi, çıkış programı, veri ihtiyaçlarını eğitmek, maliyetleri ve değerlendirme anlaşmaları

## Egzersizler.

1. **Easy / 简单.**Değiştir `code/main.py`G'nin her sınıfın gürültüsünü doğru modaya yerleştirdiğini onaylayın.
   修改 `code/main.py`添加第三类. G 仍将每个类的噪音映射到正确模式.
2. **Medium / 中等.**L1'i 1-D ayarında algısal bir kayıpla değiştirin (örneğin özellik çıkarıcı olarak hareket eden küçük dondurulmuş D). Şartlı dağılımın keskinliğini değiştirir mi?
   1D ayarında algı kaybı ile L1'i değiştirmek koşulların dağılmasının derecesini değiştirdi mi?
3. **Hard / 困难.**Bir CycleGAN'ı 1D ayarında çizin: iki dağıtım, iki jeneratör, döngü kaybı.
   1D ayarında çizim CycleGAN: iki dağılım, iki üreticiler, döngü kaybı.

## Anahtar Şartlar .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Conditional GAN | "GAN with labels" / "带标签的 GAN" | G(z, c), D(x, c). Both networks see the condition. / 两个网络都看到条件。 |
| Pix2Pix | "Image-to-image GAN" / "图像到图像 GAN" | Paired cGAN with U-Net G and PatchGAN D + L1 loss. / 配对 cGAN + U-Net + PatchGAN + L1。 |
| U-Net | "Encoder-decoder with skips" / "带跳跃的编解码器" | Symmetric conv network; skips preserve high-freq. / 对称卷积网络；跳跃连接保留高频。 |
| PatchGAN | "Local-realism classifier" / "局部真实分类器" | D outputs per-patch score instead of global score. / D 输出逐块分数。 |
| CycleGAN | "Unpaired image translation" / "非配对图像翻译" | Two G's + cycle-consistency loss; no paired data. / 两个 G + 循环一致性损失。 |
| SPADE | "GauGAN" | Normalizes intermediate activations with the semantic map; segmentation-to-image. / 用语义图归一化中间激活。 |
| FiLM | "Feature-wise linear modulation" / "特征级线性调制" | Per-feature affine transform from the condition; cheap conditioning. / 廉价的条件化方式。 |

## Üretim Notu: Pix2Pix'in gecikme sınırlı bir temel çizgi olarak

Veriler ve dar bir görev (sketch → render, semantik harita → foto, gün → gece) eşleştirildiğinde, Pix2Pix'in tek çekim sonucu, gecikme üzerinde büyüklük bir sırayla yayılmayı yener.

> Veriler ve dar alan görevleri olduğunda, Pix2Pix'in tek bir sonucu, genişleme modelinin hızlı bir miktar seviyesine göre gecikme oranında gerçekleşir.

| Path / 方案 | Steps / 步数 | Typical latency at 512² on a single L4 / 典型延迟 |
|------|-------|----------------------------------------|
| Pix2Pix (U-Net forward) | 1 | ~30 ms |
| SD-Inpaint or SD-Img2Img | 20 | ~1.2 s |
| SDXL-Turbo Img2Img | 1-4 | ~0.15-0.35 s |
| ControlNet + SDXL base | 20-30 | ~3-5 s |

Pix2Pix, statik partilerde üretimi kazanır (her talep aynı FLOPs'dir). Diffusion kalitede ve genelleştirmede kazanır. Modern oyun genellikle dar görev için Pix2Pix tarzı bir destil modelini ve kuyruğu girişleri için bir diffusion fallback'i göndermektir.

> Pix2Pix, sabit bir toplama toplama kapasitesinde başarıyla başarmıştır.

## Daha fazla okumak

- [Mirza & Osindero (2014). Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784)- CGAN kağıdı.
- [Isola et al. (2017). Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/abs/1611.07004)Pix2Pix.
- [Zhu et al. (2017). Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks](https://arxiv.org/abs/1703.10593) CycleGAN.
- [Wang et al. (2018). High-Resolution Image Synthesis with Conditional GANs](https://arxiv.org/abs/1711.11585) Pix2PixHD.
- [Park et al. (2019). Semantic Image Synthesis with Spatially-Adaptive Normalization](https://arxiv.org/abs/1903.07291) SPADE / Gaugan.
- [Miyato & Koyama (2018). cGANs with Projection Discriminator](https://arxiv.org/abs/1802.05637) D. Projeksiyon
