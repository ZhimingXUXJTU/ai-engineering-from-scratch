# StyleGAN  StyleGAN  风格生成对抗网络

> Çoğu jeneratör hareket eder .`z`StyleGAN onu bölüyor: ilk harita`z`Ortalama bir kişiye.`w`, sonra * enjekte * `w`AdaIN'den gelen bu tek değişim gizli alanı çözüp fotorealist yüzleri yedi yıl boyunca çözülmüş bir sorun haline getirdi.

> **【中文解读】**StyleGAN, değişikliği z önce orta uzayda görüntüleyecek ve AdaIN'den sonra her çözünürlük düzeyinde w'ye enjekte edecek.

> **【拓展：StyleGAN 的应用】**StyleGAN  yaygın olarak insan yüzü üretimi için kullanılır (thispersondoesnotexist.com) 、虚拟人物创建、艺术创作──其 スタイル混合技术可以混合不同的人脸的粗细特征──

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 8 · 03 (GANs), Phase 4 · 08 (Normalization / 归一化), Phase 3 · 07 (CNNs)
**Time:** ~45 minutes

## Sorunlar. Sorunlar.

DCGAN haritası .`z`Transpose konvulsiyonları bir yığın yoluyla bir görüntüye.`z` poz, aydınlatma, kimlik, arka plan  birbirine karışmış.`z`Modelle "eşit kişi, farklı duruş" soramazsınız çünkü temsil bu şekilde faktör değildir.

> DCGAN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `z`映射为图像──问题是:`z`控制一切姿态、光照、身份、背景纠一起`z`Bir aksiyolu hareket eder, dört parçayı değiştirir.

Karras et al. (2019, NVIDIA) önerisi: beslenmeyi bırakın `z`- Bir sabit besleyin.`4×4×512`8 katmanlı bir MLP öğrenin ki haritalar yapsın.`z ∈ Z → w ∈ W`- Enjeksiyon`w`* Adaptive instance normalization* (AdaIN) aracılığıyla her çözünürlükte: her bir konv özellik haritasını normalleştirin, sonra `w`Stochastic detaylar için katmanlık gürültü ekleyin (deriden porlar, saç iplikleri).

> Karras 等人(2019,NVIDIA) önerdi:停止将 `z`Bir düzenli sayı ile doğrudan gönderilmek.`4×4×512`张量作为网络输入──学习一个8层 MLP将 `z ∈ Z → w ∈ W`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊  ◊ ◊                                                                                                                                                                                                                                         `w`◊ Eklemek için her kat ses kullanılır ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊                                                                                                                                                                                                                                                                          

Sonuç:`W`"Yüksek seviye stili" (koşul, kimlik) vs. "yenis stili" (yalnızca ışıklandırma, renk) için yaklaşık ortogonal ekseller vardır.`w`Düşük çözünürlük seviyeleri ve B görüntüleri için `w`Bu kilitlenmemiş düzenleme, alanlar arası stilleştirme ve tüm "StyleGAN-inversion" araştırma hattı.

> Sonuç:`W`空间对"高级风格" (gestory,身份) ve"精细风格" (精细风格) (光照,颜色)`w`Düşük çözünürlüklü bir katman için kullanılıyor.`w`Yüksek çözünürlüklü bir seviyeye sahip bir değişim biçimi kullanmak. Bu, editörlüğü, bölge biçimlendirmesini ve tüm "StyleGAN Ant-evru" çalışma yönünü çözüyor.

> **【中文解读】**StyleGAN'ın anahtar yenilikleri:(1) 映射网络 z→w 解开纠的隐空间;(2) AdaIN'de her çözünürlük seviyesinde 风格低分辨率层控制粗粒度(姿姿、身份),高分辨率层控制细粒度(颜色、纹理);(3) Her seviyesinde随机噪音添加细节(毛孔、发丝) ・・・Stay Mixing 技术可以混合不同图像的粗细特征──

> **【拓展：StyleGAN 3 的平移等变性】**StyleGAN 2 Üretimsel görüntülerin "teksiri yapışkanlık" sorunu  Özellikler  Başlık gibi  yapışkanlık  belirli bir görüntü konumunda, nesne yüzeyinde değil  yapışkanlık olacaktır  StyleGAN 3  2021  Sinyal anlamı yoluyla bu sorunu anlamak, üretim sonuçlarının düzlem ve dönüm ile eşit değişkenliği  video üretimi ve 3D  uygulamaları için özellikle önemlidir 

## Konsepten bir şey.

![StyleGAN: mapping network + AdaIN + per-layer noise](../assets/stylegan.svg)

**Mapping network.** `f: Z → W`, 8 katlı bir MLP.`Z = N(0, I)^512`- Evet .`W`Gaussian olmak zorunda değil  veriye göre şekil öğrenir.

> **映射网络。** `f: Z → W`8 kat MLP.`W`Yüksek bir öğrenme biçimi için zorlanmamak.

**Synthesis network.**Öğrenilmiş bir sabitden başlar.`4×4×512`. Her çözünürlük blokları: `upsample → conv → AdaIN(w_i) → noise → conv → AdaIN(w_i) → noise`Kararlar iki kat: 4, 8, 16, 32, 64, 128, 256, 512, 1024.

> **合成网络。**Öğrenme ile alışkanlık `4×4×512`开始──每个分辨率块:上采样→卷积→AdaIN→噪声→卷积→AdaIN→噪声──分辨率翻倍:4 到1024──

**AdaIN.**

```
AdaIN(x, y) = y_scale · (x - mean(x)) / std(x) + y_bias
```

nerede`y_scale`ve `y_bias``w`"Style" burada özellik haritasının birinci ve ikinci sıradaki istatistikleridir.

> İçlerinden `y_scale`和 `y_bias`- Evet .`w`Bu, bir sonraki aşamada bir diğer aşamada bir daha bir daha yapılması için kullanılır.

**Per-layer noise.**Tek kanallı Gaussian gürültüsü, her özellik haritasına eklenir ve öğrenilen bir kanal açısından ölçeklenir.

> **每层噪声。** Single-way high noise                                                                                                                                                                                                                                                            

**Truncation trick.**Sonuçta, örnek`z`, hesaplama`w = mapping(z)`O zaman ...`w' = ŵ + ψ·(w - ŵ)`nerede`ŵ`ortalama `w`Çok sayıda örnek üzerinde.`ψ < 1`Neredeyse her StyleGAN demo kullanıyor `ψ ≈ 0.7`- Evet .

> **截断技巧。**- Evet.`w' = ŵ + ψ·(w - ŵ)`, içinden `ŵ`Evet .`w`Birçok örnekte ortalama değer.`ψ < 1`Etooïngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüngyüng`ψ ≈ 0.7`- Evet.

## StyleGAN 1 → 2 → 3  StyleGAN  sürüm geliştirilmek

| Version | Year | Innovation / 创新 |
|---------|------|------------|
| StyleGAN | 2019 | Mapping network + AdaIN + noise + progressive growing. / 映射网络 + AdaIN + 噪声 + 渐进增长。 |
| StyleGAN2 | 2020 | Weight demodulation replaces AdaIN (fixes droplet artifacts); skip/residual architecture; path-length regularization. / 权重解调替代 AdaIN。 |
| StyleGAN3 | 2021 | Alias-free convolution + equivariant kernels; eliminates texture sticking to pixel grid. / 无混叠卷积，消除纹理粘附。 |
| StyleGAN-XL | 2022 | Class-conditional, 1024², ImageNet. / 类别条件，1024²。 |
| R3GAN | 2024 | Rebrands with stronger reg; closes gap to diffusion on FFHQ-1024 with 20x fewer params. / 更强正则化，20 倍更少参数。 |

2026 yılında StyleGAN3 (a) yüksek FPS'de dar alan fotorealismi, (b) birkaç atışlı alan uyarlaması (100 görüntü ile yeni bir veri kümesine tren, dondurma haritalama), (c) tersleme tabanlı düzenleme (gör) için standart olarak kalır.`w`Gerçek bir fotoğrafı yeniden oluşturur, sonra onu düzenler.`w`). Açık alanlı metin-resim için,  yayılma aracı değildir.

> 2026 yıl StyleGAN3  hâlâ aşağıdaki sahnelerin belirtilmiş seçeneği: a) Yüksek FPS 狭域写真级真感, b) Küçük örnek alan uyarlama, c) 反演的编辑をベースに──開放域文生图则不是它的工具扩散模型才是──

## Yapın.
```figure
gx-stylegan-mapping
```

## Yapın

`code/main.py`1-D'de bir oyuncak "style-GAN lite" uygulamaktadır: bir haritalama MLP, öğrenilen sabit vektörü alan ve onu modüle eden bir sentez fonksiyonu `w`-Derived scale/bias, ve per layer gürültü.`w`Afine modülasyon eşleşmeleri veya çarpmalarla bağlanarak `z`- Generatör girişine.

> `code/main.py`1D'de bir "StyleGAN lite" gerçekleştirildi: haritalama MLP, sintetizasyon fonksiyonu ve her kat ses.`w`Önder`z`拼接到输入相比效果相当或更好──

### Adım 1: haritalama ağı

```python
def mapping(z, M):
    h = z
    for i in range(num_layers):
        h = leaky_relu(add(matmul(M[f"W{i}"], h), M[f"b{i}"]))
    return h
```

### Adım 2: Adaptif durum normalleşmesi

```python
def adain(x, w_scale, w_bias):
    mu = mean(x)
    sd = std(x)
    x_norm = [(xi - mu) / (sd + 1e-8) for xi in x]
    return [w_scale * xi + w_bias for xi in x_norm]
```

Özellikler haritası ölçeği ve önyargısı `w`Düzsel projeksiyon yoluyla.

>                                                                                                                                                                                                                                                               `w`Yönlendirme:

### Adım 3: Katmanlık gürültü

```python
def add_noise(x, sigma, rng):
    return [xi + sigma * rng.gauss(0, 1) for xi in x]
```

Sigma kanal başına öğrenilmelidir.

> Her yolun sigma'sı öğrenilmelidir.

## Tuzaklar.

- **Droplet artifacts.**StyleGAN 1 özellik haritalarında bir damla damlasını üretti çünkü AdaIN ortalamayı sıfırladı. StyleGAN 2'nin ağırlık demodülasyonu, bunun yerine kıvrım ağırlıklarını ölçeklendirip düzeltir.
  **液滴伪影。**StyleGAN 1 由于 AdaIN 归零均值产生液滴──StyleGAN 2 权重解调通过缩放卷积权重修复──
- **Texture sticking.**StyleGAN 1 ve 2 dokuları, nesne koordinatları değil, piksel koordinatları takip eder (interpolasyon sırasında görünür). StyleGAN 3'ün takma isimsiz kıvrımları bunu pencerelmiş sink filtreleri ile düzeltir.
  **纹理粘附。**StyleGAN 1/2'nin yapısı, bir nesne yerine bir resim izlemektedir.
- **Mode coverage.**Çarpışma`ψ < 0.7`temiz görünüyor ama dar bir kutuptan örnekler; kullan `ψ = 1.0`Eğer çeşitliliğe ihtiyacınız varsa.
  **模式覆盖。**Kesinlikle .`ψ < 0.7`Çok temiz görünüyordu ama çok sıkıydı.`ψ = 1.0`- Evet.
- **Inversion is lossy.**Gerçek bir fotoğrafı `W`Genellikle optimizasyon veya bir kodlayıcı (e4e, ReStyle, HyperStyle) yoluyla yapılır.
  **反演有损。**Gerçek fotoğrafı izleyeceğim.`W`Genellikle optimizasyon veya kodlayıcı ile tamamlanır, sonuçlar sonraki nesillerde çok fazla süredir geçer.

## Çerçeveyi kullanın.

| Use case / 用途 | Approach / 方案 |
|----------|----------|
| Photoreal human faces (anime, product, narrow) / 照片级人脸 | StyleGAN3 FFHQ / custom fine-tune |
| Face editing from a photo / 从照片编辑人脸 | e4e inversion + StyleSpace / InterFaceGAN directions |
| Face swap / reenactment / 换脸/重演 | StyleGAN + encoder + blending |
| Avatar pipelines / 虚拟形象 | StyleGAN3 w/ ADA for low-data fine-tune |
| Domain adaptation from a few images / 少样本域适应 | Freeze mapping network, fine-tune synthesis |
| Multi-modal or text-conditioned generation / 多模态生成 | Don't — use diffusion / 不要用——用扩散模型 |

Cevabı "bir kişinin yüzünün fotoğrafı" olduğu ürün sınıfı gösterimleri için StyleGAN, sonuçlama maliyetinde yayılım (tek ileri geçiş, <10ms bir 4090) ve aynı kalite çubuğu için keskinliği yener.

>  "İnsan Yüz Fotoğrafları" sınıfı ürün gösterimi için, StyleGAN tahmin maliyetinde,4090'ın üzerinde <10 ms) ve eşit kalite altında 度 üzerinde kazanmış yayılma modeli

## İndirin . Ürünler .

- Kaydet .`outputs/skill-stylegan-inversion.md`. Skill gerçek bir fotoğraf çekir ve sonuçlar: tersleme yöntemi (e4e / ReStyle / HyperStyle), beklenen gizli kayb, düzenleme bütçesi (ne kadar uzun `W`eserlerden önce hareket edebilirsiniz) ve bilinen iyi düzenleme yönlerinin (yaş, ifade, poz) bir listesini.

> 保存 `outputs/skill-stylegan-inversion.md`◊ Gerçek fotoğraflar almak, çıkış ve gösterim yöntemleri, olası kayıpları beklemek, düzenleme bütçesi ve bilinen düzenleme yönleri

## Egzersizler.

1. **Easy / 简单.**Çık .`code/main.py`- Evet .`adain_on=True`ve `adain_on=False`- Sıkı bir latente ile rahatsız edilmiş bir latente için çıkışların yayılmasını karşılaştırın.
   Ayrılıklı kullan`adain_on=True`和 `adain_on=False`运行──Fixed Hid Variable ve perturbative Hid Variable'nin çıkış dağılımını karşılaştırmak
2. **Medium / 中等.**Karıştırma düzenlenmesini uygula: bir eğitim parti için hesaplama`w_a`- Evet .`w_b`, ve uygulanır `w_a`Sintezin ilk yarısında ve `w_b`Dekodör çözülmüş stiller öğrenir mi?
   实现混合正则化──解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码器 解码 解码器 解码器 解码器 解码器 解码 解码器 解码 解码器 解码 解码 解码器 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 解 
3. **Hard / 困难.**Önceden eğitilmiş bir StyleGAN3 FFHQ modeli (ffhq-1024.pkl) alın.`w`Etiketlenmiş örnekler üzerinde bir SVM'yi eğitirek "gümüş" kontrol eden yön; kimlik sürüklemeden önce ne kadar ileri gidebileceğinizi bildirin.
   Uygulama: StyleGAN3 FFHQ 模型, SVM 找到控制"微笑"的`w`Yönlendirme.

## Anahtar Şartlar .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Mapping network | "The MLP" / "那个 MLP" | `f: Z → W`, 8 layers, decouples latent geometry from data statistics. / 解耦隐变量几何与数据统计。 |
| W space | "The style space" / "风格空间" | Output of the mapping network; roughly disentangled. / 映射网络的输出；大致解耦。 |
| AdaIN | "Adaptive instance norm" / "自适应实例归一化" | Normalize feature map, then scale + shift by `w`-projection. / 归一化后用 `w` 投影缩放偏移。 |
| Truncation trick | "Psi" | `w = mean + ψ·(w - mean)`, ψ<1 trades diversity for quality. / ψ<1 以多样性换质量。 |
| Path-length regularization | "PL reg" | Penalizes large changes in image per unit change in `w`; makes `W` smoother. / 惩罚 `w` 单位变化引起的大图像变化。 |
| Weight demodulation | "The StyleGAN2 fix" / "StyleGAN2 修复" | Normalize conv weights instead of activations; kills droplet artifacts. / 归一化卷积权重而非激活。 |
| Alias-free | "StyleGAN3's trick" / "StyleGAN3 技巧" | Windowed sinc filters; eliminates texture sticking to the pixel grid. / 窗口 sinc 滤波器消除纹理粘附。 |
| Inversion | "Find w for a real image" / "找 w" | Optimize or encode `x → w` so `G(w) ≈ x`. / 优化或编码使 `G(w) ≈ x`。 |

## Üretim Not: neden StyleGAN 2026 yılında hala gemiye gidiyor ?

StyleGAN3 4090'da 10242 FFHQ yüzü 10 ms'ten kısa bir süre içinde üretir `num_steps = 1`Bu, herhangi bir görüntü jeneratörü için zemin gecikmesi. 50 adımlı bir SDXL + VAE-decode borusu aynı çözünürlükte ~ 3 saniye.**300× gap**, ve dar alan ürünleri için (avatar hizmetleri, kimlik belgeleri boru hattı, stok yüzü üretimi) TCO'da kazanır.

> StyleGAN3 4090'da 10 ms'e kadar sürüyor.`num_steps = 1`, VAE 解码,交叉注意力──50 步 SDXL 同分辨率约3秒──这是**300 倍差距**, Sık bölgedeki ürünler üzerinde TCO 勝利──

İki operasyonsal sonuç:

> 两个运营后果:

- **No scheduler, no batcher.**Hedefli işlevdeki statik parti en iyisidir. Sürekli partileşme (LLM ve yayım için gereklidir) her talep aynı FLOP'leri aldığı için sıfır fayda sağlar.
  **无需调度器或批处理器。**静态批量最优──连续批处理(LLM için çok önemlidir)零收益──
- **Truncation `ψ` is the safety knob.** `ψ < 0.7`Karteleme ağının aralığındaki dar bir kutuptan örnekler. Bu, servis katmanının örnek değişkenliği üzerinde sahip olduğu tek kaldıraç.`ψ`En yüksek yükte, premium kullanıcılar için yükseltin.
  **截断 `ψ` 是安全旋钮。** `ψ < 0.7`Servis seviyesinin kontrolü arasındaki farkın tek 杆──高峰负荷時降低──`ψ`, Yüksek kullanıcılar zaman yükseltmek için.

## Daha fazla okumak

- [Karras et al. (2019). A Style-Based Generator Architecture for GANs](https://arxiv.org/abs/1812.04948) StyleGAN.
- [Karras et al. (2020). Analyzing and Improving the Image Quality of StyleGAN](https://arxiv.org/abs/1912.04958) StyleGAN2.
- [Karras et al. (2021). Alias-Free Generative Adversarial Networks](https://arxiv.org/abs/2106.12423) StyleGAN3.
- [Tov et al. (2021). Designing an Encoder for StyleGAN Image Manipulation](https://arxiv.org/abs/2102.02766) e4e tersine.
- [Sauer et al. (2022). StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets](https://arxiv.org/abs/2202.00273) StyleGAN-XL.
- [Huang et al. (2024). R3GAN: The GAN is dead; long live the GAN!](https://arxiv.org/abs/2501.05441) Modern minimal GAN tarifi.
