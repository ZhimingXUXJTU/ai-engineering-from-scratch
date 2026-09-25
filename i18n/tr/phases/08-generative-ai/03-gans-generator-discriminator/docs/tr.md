# GAN'lar  Generator vs. Diskriminator  GAN  Üreticiler ve Yargıcılar

> Goodfellow'un 2014'te yaptığı numara yoğunluğu tamamen atlamak. İki ağ. Biri sahte yapıyor. Biri yakalıyor. Sahte gerçekten ayırt edilemez olana kadar dövüşüyorlar. Bu işe yaramaz.

> **【中文解读】**Goodfellow 2014'in teknikleri yoğunluk tahminini tamamen atladı. İki ağ: bir sahte, bir sahte, gerçek örnekten ayırt edilmez bir şekilde birbirine karşı mücadele etti.

> **【拓展：GAN 的遗产】**StyleGAN (人脸生成) ✓CycleGAN (风格迁移) ✓Pix2Pix (图像翻译) ✓GAN'ın klasik uygulamasıdır. Genişletilmiş modeller 2022'den sonra ana haline gelmesine rağmen,GAN'ın karşı karşı antrenman düşüncesi hala diğer modellerin kalitesini yükseltmek için kullanılıyor.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 08 (Optimizers / 优化器), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## Sorunlar. Sorunlar.

VAE'ler bulanık örnekler üretir çünkü MSE dekodör kaybı * ortalama * görüntü için Bayes-optimal ve birçok makul rakamın ortalaması bulanık bir rakamdır. * makulluğu * ödüllendiren bir kaybı istiyorsunuz, herhangi bir hedefe piksel açısından yakınlık değil. Makulluğu için kapalı bir biçim yoktur. Bunu öğrenmelisiniz.

> VAE'de belirsiz bir örnek oluşur, çünkü MSE  çözücü kaybı * ortalama değerlere* karşı görüntü Bayes'in en iyi  ve birçok mantıklı rakamın ortalama değeri belirsiz bir rakamdır.

Goodfellow'un fikri: sınıflandırıcı eğitmek.`D(x)`Gerçek görüntüleri sahte görüntülerden ayırt etmek için bir jeneratör eğit.`G(z)`- Akılsızlık .`D`Kayıp sinyalini .`G`Neyse .`D`Bu sinyal güncelleştiriler gibi`G`Eğer iki ağ da bir araya gelirse,`G`Bilgi dağıtımını hiç yazmadan öğrenmiş.`log p(x)`- Evet .

> İyi arkadaşın fikri: bir sınıf eğitimi`D(x)`Gerçek sahte görüntü ayır, bir jeneratör eğit.`G(z)`Yalancılık yapalım .`D`- Evet.`G`Kayıp sinyalleri`D`"Gerçek gibi görünen" bir şey olduğunu düşünenler, bu sinyalle birlikte.`G`Bu yenilik, bir hareketli hedefi takip etmek için yapılıyor.`G`Bilgi dağıtımını öğrenmek için yazmak zorunda kalmaz.`log p(x)`- Evet.

Bu bir karşılaşma eğitimi.

```
min_G max_D  E_real[log D(x)] + E_fake[log(1 - D(G(z)))]
```

2026'da GAN'lar artık SOTA jeneratörü değil (haşlama ve akış eşleşimi bu taçı yedi). Ancak StyleGAN 2/3 şimdiye kadar gönderilen en keskin yüz modelleri olarak kalır, GAN ayrımcıları, difüzyon eğitiminde * algı kaybı* olarak kullanılır ve karşıtlık eğitimi gerçek zamanlı difüzyon göndermenizi sağlayan hızlı 1 adımlı destillasiyonları (SDXL-Turbo, SD3-Turbo, LCM) güçlendirir.

> 2026 yılında GAN 再是最先进的生成器 (GAN 再是最先进的生成器) 扩散模型和流相匹配 (Flow Matching) 夺走了冠) ──但是 StyleGAN 2/3 仍然是历史上最利的人脸模型,GAN 判斷器被用于扩散训练中*感觉损失*,对抗训练驱动着快速的1 步蒸(SDXL-Turbo、SD3-Turbo、LCM) ──

> **【中文解读】**GAN'ın temel düşüncesi: ̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇̇

> **【拓展：GAN 在扩散模型蒸馏中的新角色】**GAN artık ana üretim yöntemidir, ancak anti-trening fikri yayılma modelinde yeni bir yaşam sürüyor. SDXL-Turbo, SD3-Turbo, LCM ve diğer hızlı modeller, anti-hasarın kullanımı ile gerçek zamanlı üretimi gerçekleştirmek için 1-4 adımlar arasında yayılmaya başlayacak. GAN'ın belirleyicisi, sabit algı kaybından daha etkili bir "kalite değerlendirmeci" olarak öğrenilebilir.

## Konsepten bir şey.

![GAN training: generator and discriminator in minimax](../assets/gan.svg)

**Generator `G(z)`.**Bir gürültü vektörünü haritası `z ~ N(0, I)`bir örnek için `x̂`. Dekodör şeklinde bir ağ (sıkı veya transpose konfor).

> **生成器 `G(z)`。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `z ~ N(0, I)`映射为样本 `x̂`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △

**Discriminator `D(x)`.**Bir örnekin bir skalar olasılık (veya puan) haritasına yerleştirildi.

> **判别器 `D(x)`。**Ölçü: %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2

**Loss.**İki alternatif güncelleme:

- **Train `D`:** `loss_D = -[ log D(x) + log(1 - D(G(z))) ]`- Gerçek = 1'de ikili çapraz entropi, sahte = 0'da.
- **Train `G`:** `loss_G = -log D(G(z))`Bu Goodfellow'un kullandığı * doymayan * formdur (orjinal)`log(1 - D(G(z)))`                         `D`Kendine güvenen biri.

> **损失。**两个交替更新:训练 D 用二元交叉(真实=1,伪造=0);训练 G 用非和形式 `-log D(G(z))`(Orijinal Form in D 自信时梯度 kaybolur)

**Training loop.**Bir adım atmak .`D`Bir adım daha .`G`Tekrar ediyorum.

> **训练循环。**Bir adım D, bir adım G, bir değişim yapın.

**Why it works.**- Eğer`G`Tam olarak eşleşir .`p_data`O zaman ...`D`Orası şansın değil . Her yerde 0.5 çıkış .`G`Daha fazla gradient kalmaz.

> **为什么有效。**Eğer `G`完美匹配 `p_data`,则 `D`- Yeterince iyi bir tahmin.`G`Bu da dengenin bir parçası.

**Why it breaks.**Mod çöküşü (`G`Bir mod bulur `D`- ...bunu sonsuza kadar sınıflandırıp, bir araya getiremiyorum.`D`Çok hızlı öğrenir ve `log D`Bu nedenle, eğitimde de bir değişiklik yapılması gerekmektedir.

> **为什么会失败。**模式塌(`G`找到 `D`无法分类 一种模式并永远产生它) 梯度消失(`D`Çok hızlı bir şekilde öğrendi.`log D`和) 、 training is not stable (Trening is not stable)  learning rate (Trening is not stable) 

## GAN'ı başarılı kılan varyasyonlar

| Year / 年份 | Innovation / 创新 | Fix / 解决的问题 |
|------|------------|-----|
| 2015 | DCGAN | Conv/deconv, batch norm, LeakyReLU — the first stable architecture. / 首个稳定架构。 |
| 2017 | WGAN, WGAN-GP | Replace BCE with Wasserstein distance + gradient penalty. Fixes vanishing gradient. / 用 Wasserstein 距离替换 BCE，修复梯度消失。 |
| 2017 | Spectral normalization | Lipschitz-bound the discriminator. Still used in 2026 discriminators. / 约束判别器 Lipschitz 常数。 |
| 2018 | Progressive GAN | Train low-res first, add layers. First megapixel results. / 先训练低分辨率，再加层。 |
| 2019 | StyleGAN / StyleGAN2 | Mapping network + adaptive instance norm. State of the art for fixed-domain photorealism. / 映射网络 + AdaIN。 |
| 2021 | StyleGAN3 | Alias-free, translation-equivariant — still the face gold standard in 2026. / 无混叠，平移等变。 |
| 2022 | StyleGAN-XL | Conditional, class-aware, larger scale. / 条件生成，类别感知。 |
| 2024 | R3GAN | Rebrands with stronger regularization; works on 1024² without tricks. / 更强的正则化。 |

## Yapın.
```figure
gan-minimax
```

## Yapın

`code/main.py`1 boyutlu verilere göre küçük bir GAN'ı eğitir: iki Gaussians karışımı. Generatör ve ayrımcı tek katmanlı MLP'lerdir. Ön, geriye ve minimax döngüsünü elle uyguluyoruz. Amaç iki anahtar başarısızlık modunu (mod çöküş + kaybolan gradient) görmektir.

> `code/main.py`Bir boyutlu veri üzerinde eğitim bir mikrotip GAN:双峰高斯混合―― jeneratör ve ayırt edici MLP tek gizli katmanıdır――.

### Adım 1: Doymayan kayıp

Vanilya Goodfellow kaybı .`log(1 - D(G(z)))`D'nin G'nin sahte olduğunu yüksek güvenle sahte olarak sınıflandırırken 0'ya gider.`-log D(G(z))`D'nin güven içindeyken patlar ve G'ye güçlü bir sinyal verir.

>  原始 İyi arkadaş                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         `log(1 - D(G(z)))`D Yüksek Güven Sende G'nin sahte sınıflandırılması, sahte olarak 0'ye yakın hale gelmektedir.`-log D(G(z))`D'in kendi kendine patlaması sırasında, G'ye güçlü sinyal ver.

```python
def g_loss(d_fake):
    # maximize log D(G(z))  <=>  minimize -log D(G(z))
    return -sum(math.log(max(p, 1e-8)) for p in d_fake) / len(d_fake)
```

### Adım 2: Bir jeneratör adımı başına bir ayrımcı adım

```python
for step in range(steps):
    # train D
    real_batch = sample_real(batch_size)
    fake_batch = [G(z) for z in sample_noise(batch_size)]
    update_D(real_batch, fake_batch)

    # train G
    fake_batch = [G(z) for z in sample_noise(batch_size)]  # fresh fakes
    update_G(fake_batch)
```

G için yeni sahte, aksi takdirde gradientler eskidir.

> Yeni bir sahte örnek oluşturmak için, yoksa zaman geçecek.

### Adım 3: Mod çöküşünü kontrol edin

```python
if step % 200 == 0:
    samples = [G(z) for z in sample_noise(500)]
    mode_a = sum(1 for s in samples if s < 0)
    mode_b = 500 - mode_a
    if min(mode_a, mode_b) < 50:
        print("  [!] mode collapse: one mode is starved")
```

Kanonik semptom: iki gerçek moddan biri üretilmeyi bırakır. Ayrımcı onu düzeltmeyi bırakır çünkü asla sahte olarak görülmez.

> Tipik belirti: İki gerçek moddan biri artık üretilmiyor.

## Tuzaklar.

- **Discriminator too strong.**D'nin öğrenme hızını 2-5 kat azaltın veya örnek/katman gürültüsü ekleyin.
  **判别器太强。**D'nin öğrenme oranı 2-5 kat azalır veya örnek/sınıf gürültüsü eklenir. D'nin doğruluk oranı %95'ten fazla ise, G ölür.
- **Generator memorizes a mode.**D girişlerine gürültü ekleyin, minibatch-dizginci katmanı kullanın veya WGAN-GP'ye geçin.
  **生成器记住了一种模式。**给 D 输入添加噪音,使用小批量判别器层,或切换到WGAN-GP──
- **Batch norm leaking statistics.**Aynı BN katmanından akışan gerçek parti + sahte parti istatistiklerini karıştırır.
  **批归一化泄漏统计量。**Gerçek ve sahte gruplar aynı BN katmanıyla statistik miktarı karıştırıyor.
- **Inception-score gaming.**FID ve IS düşük örnek sayımlarında gürültülüdür.
  **Inception Score 作弊。**FID 和 IS 在低样本量时噪声大──评估时使用 ≥10k样本──
- **One-shot sampling is a lie for conditional tasks.**Hala CFG ölçekleri, kesim hileleri ve kullanılabilir çıkışlar elde etmek için yeniden örneklenmeye ihtiyacınız var.
  **条件任务中"单次采样"是个谎言。**CFG'nin genişlemesi, kesim becerileri ve yeniden örneklenmesi hala gerekli.

## Çerçeveyi kullanın.

2026 GAN yığın:

> 2026 yıl GAN 技术:

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Photoreal human faces, fixed pose / 照片级人脸，固定姿势 | StyleGAN3 (sharpest, smallest) |
| Anime / stylized faces / 动漫/风格化人脸 | StyleGAN-XL or Stable Diffusion LoRA |
| Image-to-image translation / 图像翻译 | Pix2Pix / CycleGAN (Phase 8 · 04) or ControlNet (Phase 8 · 08) |
| Fast 1-step text-to-image / 快速单步文生图 | Adversarial distillation of diffusion (SDXL-Turbo, SD3-Turbo) |
| Perceptual loss inside a diffusion trainer / 扩散训练中的感知损失 | Small GAN discriminator on image crops |
| Anything multi-modal, open-ended / 多模态开放域 | Don't — use diffusion or flow matching / 不要用 GAN——用扩散或 Flow Matching |

GAN'lar keskin ama dar. Bir kez alanınız  fotoğrafları açtığında, keyfi metin istekleri, video  yayıma geçiyor.

> GAN 利但狭域──一旦领域开放照片、任意文本提示、视频就就切换到扩散模型──对抗技巧作为组件存活(感知损失、蒸),而非独立生成器──

## İndirin . Ürünler .

- Kaydet .`outputs/skill-gan-debugger.md`. Skill, başarısız bir GAN çalışmasını (kayıp eğri, örnek şebekesi, veri kümesi boyutu) alır ve olası nedenlerin sıralamalı bir listesini, tek satırlı düzeltmeleri ve tekrar çalıştırma protokolünü çıkarır.

> 保存 `outputs/skill-gan-debugger.md`◊Skill 收取一个失败的GAN 运行(损失曲线、样本网格、数据集大小),输出可能原因排序列、一行修复和重跑方案──

## Egzersizler.

1. **Easy / 简单.**Çık .`code/main.py`- O zaman ayarlayın.`D_LR = 5 * G_LR`G'nin kaybı ne kadar hızlı bir sabit haline gelir?
   Uzd默认设置运行 `code/main.py`Sonra ayarlayın.`D_LR = 5 * G_LR`Ağırlık kaybı, sürekli düşüştür.
2. **Medium / 中等.**Goodfellow BCE kaybını WGAN kaybıyla değiştirin: `loss_D = E[D(fake)] - E[D(real)]`- Evet .`loss_G = -E[D(fake)]`, ve D'nin ağırlıklarını `[-0.01, 0.01]`- Eğitim daha istikrarlı mı?
   Goodfellow'u bir KÖ'ye dönüştürmek , bir KÖ'ye dönüştürmek , bir KÖ'ye dönüştürmek , bir KÖ'ye dönüştürmek , bir KÖ'ye dönüştürmek , bir KÖ'ye dönüştürmek , bir KÖ'ye dönüştürmek , bir KÖ'ye dönüştürmek , bir KÖ'ye dönüştürmek , bir KÖ'ye dönüştürmek , bir KÖ'ye dönüştürmek , bir KÖ'ye dönüştürmek .`[-0.01, 0.01]`◊ daha iyi bir eğitim mi?
3. **Hard / 困难.**1-D örneğini 2-D verilere (bir yüzük üzerinde 8 Gaussians karışımı) uzatın. Generatörün 1k, 5k, 10k adımlarında kaç tane 8 mod yakaladığını takip edin. Minibatch ayrımcılığını uygulayın ve yeniden ölçün.
   1D örnekleri 2D verilere yaymak için:                                                                                                                                                                                                                                                         

## Anahtar Şartlar .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generator | "G" | Noise-to-sample network, `G: z → x̂`. / 噪声到样本的网络。 |
| Discriminator | "D" | Classifier `D: x → [0, 1]`, real vs fake. / 真假分类器。 |
| Minimax | "The game" / "博弈" | `min_G max_D` of a joint objective. / 联合目标的极小极大。 |
| Non-saturating loss | "The fix" / "修复" | Use `-log D(G(z))` for G instead of `log(1 - D(G(z)))`. / 用非饱和形式替代原始损失。 |
| Mode collapse | "G memorized one thing" / "G 记住了一种" | Generator produces few distinct outputs despite diverse data. / 生成器产生少量不同输出。 |
| WGAN | "Wasserstein" | Replace BCE with Earth-Mover distance + gradient penalty; smoother gradient. / 用 Wasserstein 距离替代 BCE。 |
| Spectral norm | "Lipschitz trick" / "Lipschitz 技巧" | Constrain D's weight norms to bound its slope; stabilizes training. / 约束 D 的权重范数以稳定训练。 |
| StyleGAN | "The one that works" / "能用的那个" | Mapping network + AdaIN; best-in-class for faces, still in 2026. / 映射网络 + AdaIN，人脸最佳。 |

## Üretim Not: Tek çekim sonucu GAN'ın kalıcı avantajıdır.

GAN'lar artık açık alan üretimi için örnek kalitesi üzerinde kazanmazlar, ancak hala sonuçlandırma maliyetinde kazanırlar.

> GAN, açık alanlarda üretilen örneklerin kalitesi üzerinde bir daha kazanmadı, ancak üretim teorisi terminolojisinde, değerlendirme maliyetinde hâlâ kazanmıştır:

- **No prefill, no decode stages.**Tek bir tane .`G(z)`TTFT ≈ toplam gecikme.
  **无 prefill，无 decode 阶段。**单次 `G(z)`Önümüze yayılmak için ≈ 总延迟。
- **No KV-cache pressure.**Tek durum ağırlıklar.Battery boyutu, cache değil, aktivasyon belleği ile sınırlıdır.
  **无 KV 缓存压力。**Tek durum, ağırlık ve büyüklüktür.
- **Trivial continuous batching.**Her istek aynı sabit FLOPs'i aldığı için, sunucu'nun hedef yerleşimindeki statik bir parti genellikle en iyisidir.
  **简单的连续批处理。**Her istek aynı FLOP'yi tüketir, statik miktar genellikle en iyidir.

Bu nedenle GAN destilasyonu (SDXL-Turbo, SD3-Turbo, ADD, LCM) 2026'da hızlı metin-resim için baskın tekniktir: yavaş jeneratörleri hızlılara dönüştürmek için bir antrenman zaman düğmesi olarak kalır.

> İşte bu yüzden GAN 蒸(SDXL-Turbo、SD3-Turbo、LCM) 2026 yılındaki en yönetici teknoloji: 20-50 adım genişletilmiş su hattı, GAN 风格'ın 1-4 kez ön yönde yayılmasını sağlayacak ve aynı zamanda genişletilmiş modelin dağılmasını sağlayacak.

## Daha fazla okumak

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661) orijinal GAN kağıdı.
- [Radford et al. (2015). Unsupervised Representation Learning with DCGAN](https://arxiv.org/abs/1511.06434) İlk sabit mimarlık.
- [Arjovsky, Chintala, Bottou (2017). Wasserstein GAN](https://arxiv.org/abs/1701.07875) WGAN.
- [Miyato et al. (2018). Spectral Normalization for GANs](https://arxiv.org/abs/1802.05957) SN.
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958) StyleGAN2.
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423) StyleGAN3.
- [Sauer et al. (2023). Adversarial Diffusion Distillation](https://arxiv.org/abs/2311.17042)SDXL-Turbo.
