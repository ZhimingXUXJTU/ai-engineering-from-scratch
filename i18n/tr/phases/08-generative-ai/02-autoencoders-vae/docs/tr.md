# Otomatik kodlayıcılar ve Variasyonel Otomatik kodlayıcılar (VAE) ✓

> Bir otomatik kodlayıcı sıkıştırır, sonra yeniden oluşturur. Hatırlıyor. Yaratmaz. Bir numara ekleyin  kodu Gaussian görünmesi için zorlayın  ve bir örneklemeci elde edersiniz.`z = mu + sigma * epsilon`, bu yüzden 2026'da kullandığınız her gizli yayılma ve akış eşleşme görüntü modeli girişinde bir VAE'ye sahip.

> **【中文解读】**Normal otomatik kodlama makinesi baskı yeniden inşa, sadece hatıra, üretemez.`z = mu + sigma * epsilon`让梯度可以穿越采样操作,这是VAE 训练的关键.

> **【拓展：VAE 是 Stable Diffusion 的基石】**2026 yılında tüm potansiyel genişleme modeli ((Stable Diffusion、FLUX) VAE'nin potansiyel alanında çalışır.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 3 · 07 (CNNs / 卷积神经网络), Phase 8 · 01 (Taxonomy / 分类)
**Time:** ~75 minutes

## Sorunlar. Sorunlar.

784 piksel MNIST rakamını 16 sayılık bir kodla sıkıştırın, sonra yeniden yapılandırın. Sıradan bir otomatik kodlayıcı MSE yeniden yapılandırmasını sağlar ancak kod alanı bir karışıklık.

> 784'ü bir MIST olarak yeniden inşa etmek için 16 sayısal bir kod oluşturmak gerekir. Normal bir kodlayıcı MSE'yi iyi yeniden inşa edebilir, ancak kodlama alanı bir takım kötüdür.

Aslında istediğiniz şey: (a) kod alanı temiz ve düzgün bir dağılımdır.`N(0, I)`, (b) herhangi bir örnekin çözümü bir olası rakam üretir ve (c) kodlayıcı ve dekoder hala iyi sıkıştırılır.

> Gerçekten istediğin şey: a) 编码空间是干净,平滑,可采用分布`N(0, I)`Bu, bir sistemin en iyi bir şekilde oluşturulması ve bir şekilde bir sistemin daha daha daha gelişmesi için kullanılabilir.

Kingma'nın 2013 VAE'si kodlayıcının bir * dağıtım* çıkartması için eğitilmesiyle bunu çözer.`q(z|x) = N(μ(x), σ(x)²)`, bu dağılımı öncüye doğru çekerek`N(0, I)`KL cezası ile, sonra örnekleme yapılır.`z`-`q(z|x)`Anlamlama sırasında, kodlayıcıyı bırakın, örnekleyin.`z ~ N(0, I)`KL cezası, kod alanının yapılandırılmasını zorlar.

> Kingma 2013 yılının VAE 通过训练编码器输出*分布* `q(z|x) = N(μ(x), σ(x)²)`Bu sorunu çözmek için KL'den cezalar dağıtılacak.`N(0, I)`Sonra da ...`q(z|x)`Çeviri`z`Tekrar çözmek, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak, yazmak`N(0, I)`采样 `z`KL  ceza, kodlama alanının yapılandırılmasının anahtarıdır.

2026 yılında VAE'ler nadiren bağımsız olarak gönderir  çiğ görüntü kalitesi için difüzyonla üst sınıflandırılmıştır  ama her latent difüzyon modeli için tercih edilen kodlayıcılardır (SD 1/2/XL/3, Flux, AudioCraft).

> 2026 yılında VAE  çok az bağımsız deployment  orijinal görüntü kalitesi üzerinde yayılmış model aşmıştır  ama tüm potansiyel yayılma modelleri SD 1/2/XL/3、Flux、AudioCraft) ilk seçilen kodlayıcı 

> **【中文解读】**VAE'nin temel anlayışı: Kodeciye dağılımdan kaynaklı olarak değerlendirmeler yapılmasını sağlamak.`z = mu + sigma * epsilon`Bu nedenle, bu konularda, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek çözüm yoluyla, bir tek tek çözüm yoluyla, bir tek çözüm yolu ile, bir tek tek çözüm yolu ile, bir tek tek çözüm yolu ile, bir tek tek çözüm yolu ile, bir tek tek tek çözüm yolu ile, tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek tek

> **【拓展：beta-VAE 与解耦表示学习】**beta-VAE(2017) düzenleme yoluyla beta parametr kontrol yeniden inşaat KL'nin ağırlığı ile birlikte. beta<1 时重建更清晰但潜在空间不规整; beta>1 时潜在空间更规整但图像更模糊──当 beta 足够大时,VAE'nin " çözüle" olduğunu göstermek için                                                                                                                                                                                                                      

## Konsepten bir şey.

![Autoencoder vs VAE: the reparameterization trick](../assets/vae.svg)

**Autoencoder.** `z = encoder(x)`- Evet .`x̂ = decoder(z)`, kayıp = `||x - x̂||²`- Kod alanı yapılandırılmamış.

> **自编码器。** `z = encoder(x)`- Evet .`x̂ = decoder(z)`, kaybı = `||x - x̂||²`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

**VAE encoder.**İki vektör çıkışı: `μ(x)`ve `log σ²(x)`Bu tanımlar .`q(z|x) = N(μ, diag(σ²))`- Evet .

> **VAE 编码器。**输出 iki 量:`μ(x)`和 `log σ²(x)`- Definiyorlar.`q(z|x) = N(μ, diag(σ²))`- Evet.

**Reparameterization trick.**`q(z|x)`Örnekte farklılık gösterilmez.`z = μ + σ·ε`nerede`ε ~ N(0, I)`- Şimdi .`z``(μ, σ)`Parametre dışı bir gürültü ekle  gradientler akıyor `μ`ve `σ`- Evet .

> **重参数化技巧。**- Evet .`q(z|x)`采样不可微──将采样重写为 `z = μ + σ·ε`, içinden `ε ~ N(0, I)`Şimdi.`z`Evet .`(μ, σ)`                                                                                                                                                                                                                                                              `μ`和 `σ`Çeviriş karşısında.

**Loss.**Kanıt Alt Bağlantısı (ELBO), iki terim:

```
loss = reconstruction + β · KL[q(z|x) || N(0, I)]
     = ||x - x̂||²  + β · Σ_i ( σ_i² + μ_i² - log σ_i² - 1 ) / 2
```

Yeniden inşaat sürükler .`x̂`- Yolu `x`KL ' in itmesi .`q(z|x)`Bu yöntemin bir diğer yönü de, daha önce belirtilmiş olan bir sistemin bir parçası olarak, daha önce belirtilmiş olan bir sistemin bir parçası olarak, daha önce belirtilmiş olan bir sistemin bir parçası olarak, daha önce belirtilmiş olan bir sistemin bir parçası olarak, daha önce belirtilmiş olan bir sistemin bir parçası olarak, daha önce belirtilmiş olan bir sistemin bir parçası olarak, daha önce belirtilmiş olan bir sistemin bir parçası olarak, daha önce belirtilmiş olan bir sistemin bir parçası olarak, daha önce belirtilmiş bir sistemin bir parçası olarak, daha önce belirtilmiş bir sistemin bir parçası olarak, daha önce belirtilmiş bir sistemin bir parçası olarak, daha önce belirtilmiş bir sistemin bir parçası olarak, daha önce belirtilmiş bir sistemin bir parçası olarak, daha önce belirtilmiş bir sistemin bir parçası olarak, daha önce belirtilmiş bir sistemin bir parçası olarak, daha önce belirtilmiş bir sistemin bir parçası olarak, daha sonra belirtilmiş bir sistemin bir parçası olarak, daha sonra bir sistemin bir diğer sistemin bir parçası olarak, daha daha daha daha daha iyi bir şekilde, daha daha daha daha iyi bir şekilde, daha daha daha daha daha daha iyi bir şekilde, daha daha daha daha daha daha daha daha daha iyi bir şekilde, daha daha daha daha daha daha daha daha daha daha daha daha iyi bir şekilde, daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha keşfetmekleyleyleyleyleyleyleyleyleyleyleyleyleyleyleyleyleyleyleyleyleyleyleyleyle

> Yeniden inşaat kaybı`x̂`趋近 `x`✿KL 推动 `q(z|x)`趋近先验──两者相互权衡──β 小(<1)= 更利的样本,编码空间不太高斯──β 大(>1)= 更干净的编码空间,更模糊的样本──β-VAE(2017) bu dönemi tanınmış, 已开启了解表示学习研究──

**Sampling.**Sonuç: çekim`z ~ N(0, I)`Bir ileri geçiş  difüzyon gibi tekrarlayıcı örnekleme yok.

> **采样。**推理时: `N(0, I)`Çekip al .`z`,送入解码器前向传播──单次前向传播无需像扩散模型那样代采样──

> **【中文解读】**ELBO  kaybının iki bileşeni vardır: yeniden inşaat kaybı çözüme kalitesi, KL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

> **【拓展：Stable Diffusion 中的 VAE】**Stable Diffusion Pre-training kullanımı ile VAE 512x512 ı görüntü 64x64'in potansiyel alanına sıkıştırır.

## Yapın.
```figure
vae-latent-grid
```

## Yapın

`code/main.py`Bu uygulama, bir numpy veya meşale olmadan küçük bir VAE uygulamaktadır. Giriş, 8-D'deki 2 bileşenli Gaussian karışımından alınan 8 boyutlu sentetik veridir. Kodlayıcı ve dekodör tek gizli katmanlı MLP'lerdir. Tanh etkinleştirimi, ileri geçişi, kaybı ve el yazılı geri geçişi uyguluyoruz.

> `code/main.py`∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞

### Adım 1: Kodlayıcı ileriye

```python
def encode(x, enc):
    h = tanh(add(matmul(enc["W1"], x), enc["b1"]))
    mu = add(matmul(enc["W_mu"], h), enc["b_mu"])
    log_sigma2 = add(matmul(enc["W_sig"], h), enc["b_sig"])
    return mu, log_sigma2
```

`log σ²`yerine`σ`Böylece ağ çıkışı kısıtlı değildir (s'nin yumuşak artışı bir tuzak  gradientleri σ ≈ 0'da ölür).

> Kullanım`log σ²`Hayır.`σ`≈ 0 时梯度会消失) ⋅

### Adım 2: yeniden ölçümleme ve çözme

```python
def reparameterize(mu, log_sigma2, rng):
    eps = [rng.gauss(0, 1) for _ in mu]
    sigma = [math.exp(0.5 * lv) for lv in log_sigma2]
    return [m + s * e for m, s, e in zip(mu, sigma, eps)]

def decode(z, dec):
    h = tanh(add(matmul(dec["W1"], z), dec["b1"]))
    return add(matmul(dec["W_out"], h), dec["b_out"])
```

### Adım 3: ELBO

```python
def elbo(x, x_hat, mu, log_sigma2, beta=1.0):
    recon = sum((a - b) ** 2 for a, b in zip(x, x_hat))
    kl = 0.5 * sum(math.exp(lv) + m * m - lv - 1 for m, lv in zip(mu, log_sigma2))
    return recon + beta * kl, recon, kl
```

Bu da bir diğer deyişle, bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir bir de bir de bir de bir de bir bir de bir bir bir de bir de bir de bir de bir bir de bir de bir de bir bir bir de bir de bir de bir de bir de bir bir bir de bir bir bir de bir de bir de bir de bir bir bir de bir de bir bir de bir de bir bir de bir bir de bir de bir de bir de bir bir de bir bir de bir bir de bir bir de bir de bir bir de bir de bir de bir bir de bir bir de bir bir de bir de bir de bir bir de bir de bir de bir de bir bir de bir bir bir de bir de bir de bir bir de bir de bir de bir bir de bir de bir bir bir de bir de bir bir de bir de bir bir bir bir de bir de bir de bir de bir de bir de bir bir bir bir de bir de bir bir bir bir bir de bir de bir de bir bir bir de bir de bir bir bir bir de bir de bir bir bir bir de bir de bir de bir bir de bir de bir de bir bir bir de bir de bir de bir de

> 精确的闭式 KL,因为两个分布都是高的──不要数值积分──2026年还有人发布蒙特卡洛 KL 估计代码无端慢了3倍──

### Dördüncü adım: oluştur

```python
def sample(dec, z_dim, rng):
    z = [rng.gauss(0, 1) for _ in range(z_dim)]
    return decode(z, dec)
```

Bu, üreticik model. Beş satır.

> İşte bu model üretmek.

## Tuzaklar.

- **Posterior collapse.**KL term sürücüleri `q(z|x) → N(0, I)`O kadar agresif ki`z`hakkında hiçbir bilgi taşımaz.`x`. Düzeltme: β-anelleme (start β=0, ramp to 1), serbest bitler veya KL'yi aktif olmayan boyutlarda atlayın.
  **后验坍塌。**KL 项如此强强地将 `q(z|x)`拉向                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `N(0, I)`, neden oluyor`z`- Hayır.`x`Bu, bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha
- **Blurry samples.**Gaussian dekodör olasılığı, L2 için Bayes-optimal olan MSE yeniden yapılandırmasını içerir (ortalama)  bir dizi makul rakamın ortalaması bulanık bir rakamdır. Düzelt: ayrı dekodör (VQ-VAE, NVAE), veya VAE'yi yalnızca bir kodlayıcı ve yataklarda yığın yayılması olarak kullanın (Stable Diffusion yapar).
  **模糊样本。**高斯解码器似然意味着 MSE 重建一组合理数字的平均值是一个模糊的数字──修复:离散解码器(VQ-VAE、NVAE),或只是将VAE 用作编码器,在潜在空间上叠加扩散模型──
- **β too large, too early.**Arka çöküşü gör, β≈0.01'den başlayın ve ramp.
  **β 太大太早。**见后验塌── β≈0.01 开始并逐渐增加──
- **Latent dim too small.**16-D, MNIST için, 256-D, ImageNet 2562, 2048-D için ImageNet 10242 için çalışır.
  **潜在维度太小。**MNIST 16 维,ImageNet 2562 256 维;; Stabil Diffusion'ın VAE'si 512×512×3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

## Çerçeveyi kullanın.

2026 VAE'nin birimleri:

> 2026 yıl VAE 技术:

| Situation / 场景 | Pick / 选择 |
|-----------|------|
| Image-latent encoder for diffusion / 图像潜在编码器 | Stable Diffusion VAE (`sd-vae-ft-ema`) or Flux VAE |
| Audio-latent encoder / 音频潜在编码器 | Encodec (Meta), SoundStream, or DAC (Descript) |
| Video latents / 视频潜在表示 | Sora's spatiotemporal patches, Latte VAE, WAN VAE |
| Disentangled representation learning / 解耦表示学习 | β-VAE, FactorVAE, TCVAE |
| Discrete latents (for transformer modelling) / 离散潜在表示 | VQ-VAE, RVQ (ResidualVQ) |
| Continuous latents for generation / 连续潜在生成 | Plain VAE, then condition a flow/diffusion model in that latent space |

Bir latent-difüzyon modeli, kodlayıcı ve dekodör arasında yaşayan bir difüzyon modeli olan bir VAE'dir. VAE kaba sıkıştırmayı yapar, difüzyon modeli ağır yüklemeyi yapar. Video (VAE + video-difüzyon DiT) ve ses (Encodec + MusicGen transformatörü) için aynı desen.

> 潜在扩散模型就是编码器和编码器之间加入了扩散模型的 VAE──VAE yapmak粗压缩,扩散模型做重活──视频(VAE + 视频 DiT) 和音频(Encodec + MusicGen transformer) 同理──

## İndirin . Ürünler .

- Kaydet .`outputs/skill-vae-trainer.md`- Evet .

> 保存 `outputs/skill-vae-trainer.md`- Evet.

Yetenek alınması: veri kümesi profili + laten-dim hedefi + aşağıdaki kullanım (yakınlama, örnekleme veya laten-difüzyona giriş) ve çıkışlar: mimarlık seçimi (sırf/β/VQ/RVQ), β programı, laten-dim, dekodör olasılığı (Gaussian vs kategorik) ve değerlendirme planı (recon MSE, KL per dim, Fréchet mesafesi `q(z|x)`ve `N(0, I)`)

> Yetenek  Alım: Dataset概况 + 潜在维度目标 + 下游用途(重建、采样或潜在扩散输入),输出:架构选择(plain/β/VQ/RVQ) 、β 调度、潜在维度、解码器似然(高斯 vs 类别) 和评估计划──

## Egzersizler.

1. **Easy / 简单.**Değişiklik`β`İçeride`code/main.py`- ...`0.01`- Evet .`0.1`- Evet .`1.0`- Evet .`5.0`Son yeniden yapılanma MSE ve KL'yi kaydet. Sentetik verileriniz için en iyi Pareto beta hangisi?
   - Evet .`code/main.py`- Ben .`β`改为 `0.01`- Evet.`0.1`- Evet.`1.0`- Evet.`5.0` Kayıt: MSE ve KL'yi yeniden inşa etmek için en iyi yöntem hangisi?
2. **Medium / 中等.**Gaussian dekoder olasılığını Bernoulli olasılığı (çaplak entropi kaybı) ile değiştirin. Aynı sentetik verilerin ikili sürümünde örnek kalitesini karşılaştırın.
   Bu nedenle, bu değerlerin bir kısmı olarak değerlendirilen bir değerin değerini değerlendirmek için kullanılır.
3. **Hard / 困难.**Uzaklaştırma`code/main.py`Mini VQ-VAE'ye dönüştürülür: sürekli `z`K=32 giriş kod defterinde en yakın komşu arayışı ile. Yeniden inşa MSE'yi karşılaştırın ve kaç kod defter girişinin kullanıldığını bildirin (kod defter çöküşü gerçek).
   - Ben de .`code/main.py`扩展为迷你 VQ-VAE:用 K=32 的码本近邻寻找替换连续 `z`❖ MSE yeniden inşa edilmesi ve raporlama ile ilgili olarak bu konuyla ilgili olarak daha fazla bilgi alınmıştır.

## Anahtar Şartlar .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Autoencoder | Encode-decode network / 编码-解码网络 | `x → z → x̂`, learn MSE. Not generative. / `x → z → x̂`，学习 MSE。不是生成模型。 |
| VAE | AE with a sampler / 带采样器的 AE | Encoder outputs a distribution, KL penalty shapes code space. / 编码器输出分布，KL 惩罚塑造编码空间。 |
| ELBO | Evidence lower bound / 证据下界 | `log p(x) ≥ recon - KL[q(z\|x) \|\| p(z)]`; tight when `q = p(z\|x)`. |
| Reparameterization | `z = μ + σ·ε` | Rewrites stochastic node as deterministic + pure noise. Enables backprop through sampling. / 将随机节点重写为确定性 + 纯噪声。使采样可反向传播。 |
| Prior | `p(z)` | Target distribution for the latent, typically `N(0, I)`. / 潜在变量的目标分布，通常是 `N(0, I)`。 |
| Posterior collapse | "KL term wins" / "KL 项赢了" | Encoder ignores `x`, outputs the prior; decoder must hallucinate. / 编码器忽略 `x`，输出先验；解码器只能幻觉。 |
| β-VAE | Tunable KL weight / 可调 KL 权重 | `loss = recon + β·KL`. Higher β = more disentangled but blurrier. / β 越高越解耦但越模糊。 |
| VQ-VAE | Discrete latent / 离散潜在变量 | Replace continuous `z` with nearest codebook vector; enables transformer modelling. / 用最近码本向量替换连续 `z`。 |

## Üretim Notu: VAE bir yayım sunucusunda en sıcak yoludur.

Stable Diffusion / Flux / SD3 borusunda VAE'ye istek başına iki kez çağrılır  bir kez kodlamak için (img2img / inpainting yapıyorsanız) ve bir kez de kodlamaktır. 10242'de dekodör geçişi genellikle tüm borusunda en büyük tek etkinleştirme hafızası zirvesidür çünkü yukarıdaki örnekler `128×128×16`- Yeterince .`1024×1024×3`İki pratik sonuç:

> Stable Diffusion / Flux / SD3 流水线中,VAE Her seferinde istek iki kez  bir kez kodlanır ({{padle=##########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

- **Slice or tile the decode.** `diffusers`Açıklamalar`pipe.vae.enable_slicing()`ve `pipe.vae.enable_tiling()`Tiling küçük bir dikiş eseriyle ticaret yapıyor .`O(tile²)`- Anımsamak yerine .`O(H·W)`- 10242+ için gerekli.
  **切片或分块解码。** `diffusers`提供 `enable_slicing()`和 `enable_tiling()`分块以轻微接伪影换取 `O(tile²)`İç kaydı.
- **bf16 decoder, fp32 numerics for the final resize.**SD 1.x VAE fp32'de serbest bırakıldı ve 10242+ SDXL gemilerinde fp16'a döküldüğünde *sessizçe NaNs* üretir.`madebyollin/sdxl-vae-fp16-fix` her zaman fp16- sabit variansı tercih edin veya bf16 kullanın.
  **bf16 解码器，fp32 用于最终 resize。**SD 1.x VAE 在 fp16 下 10242+ 会静默产生 NaN──始终使用 fp16-fix 变体或 bf16──

## Daha fazla okumak

- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) VAE kağıdı.
- [Higgins et al. (2017). β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework](https://openreview.net/forum?id=Sy2fzU9gl) çözülmüş β-VAE.
- [van den Oord et al. (2017). Neural Discrete Representation Learning](https://arxiv.org/abs/1711.00937) VQ-VAE.
- [Vahdat & Kautz (2021). NVAE: A Deep Hierarchical Variational Autoencoder](https://arxiv.org/abs/2007.03898) En son görüntü VAE.
- [Rombach et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) Dönüştürme; VAE kodlayıcı olarak.
- [Défossez et al. (2022). High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438) Encodec, sesli VAE standardı.
