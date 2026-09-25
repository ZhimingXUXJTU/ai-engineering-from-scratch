# Resim Yükleme  GANs  resim Yükleme  resim oluşturma  resim oluşturma 

> Bir GAN, sabit bir oyunda iki sinir ağıdır. Biri çizer, biri eleştirir.

> **【中文解读】**GAN (Generator Against Network) iki sinir ağının bir parçasıdır: generator painting,判别器挑毛病, ikisi birlikte ilerlemektedir.

> **【拓展：GAN 的遗产】**GAN en StyleGAN ️人脸生成) CycleGAN 风格迁移) Super-Resolution GAN ️图像超分辨率) ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ 

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 03 (CNNs), Phase 3 Lesson 06 (Optimizers), Phase 3 Lesson 07 (Regularization) | **前置知识:** Phase 4 Lesson 03（CNN），Phase 3 Lesson 06（优化器），Phase 3 Lesson 07（正则化）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Öğrenme hedefleri

- Generatör ve ayrımcı arasındaki minimumx oyunu ve denge neden p_model = p_data ile karşılık geldiğini açıklayın.
- PyTorch'te DCGAN uygulamak ve 60 satırdan az bir sürede tutarlı 32x32 sentetik görüntü oluşturmak için
- GAN eğitimi üç standart hile ile istikrarlandır: beslenmeyen kayb, spektral norm, TTUR (iki kez güncelleme kuralı)
- Sağlıklı bir yakınlık ve mod çöküşü, ossilasyon ve ayrımcı-kazanacakları tamamen ayırt eden eğitim eğrilerini okuyun

> **【中文解读】**Öğrenme hedefi, ders bitirilmesinden sonra öğrenilmesi gereken temel becerileri listeler.


## Sorunlar. Sorunlar.

Sınıflandırma bir ağı görüntülerin etiketlere haritasını öğretir. Üretim sorunu tersine çevirir: aynı dağılımdan gelen gibi görünen yeni görüntülere örnek verin. Fark edebileceğiniz "doğru" bir çıkış yoktur; sadece taklit etmek istediğiniz bir dağılım vardır.

> Klasik öğretim ağı, görüntüyi etiketlere haritalayacaktır. Bu soruyu geri çevirdi: örnek aynı dağılımın yeni görüntülerinden geliyor.

Standart kayıp fonksiyonları (MSE, çapraz entropi) "Bu örnek gerçek dağılımdan geldi mi" ölçemez.Piksele hatayı en aza indirmek, gerçekçi örnekler değil, bulanık ortalamalar üretir.Kahrı öğrenmek: gerçek ile sahteyi ayırt etme görevi olan ikinci bir ağı eğitmek ve yargıcının yargıcısını jeneratörü itmek için kullanmak.

> 標準損失函数 (MSE、交叉) bu örneğin gerçek dağılımdan olup olmadığını ölçemez.                                                                                                                                                                                                                                                  

GAN'lar (Goodfellow et al., 2014) bu çerçeveyi tanımladı. 2018 yılına kadar StyleGAN fotoğraflardan ayırt edilemez 1024x1024 yüz üretmekteydi.

> GAN(Goodfellow et.,2014) bu çerçeveyi tanımladı. 2018 yılına kadar StyleGAN 已能产生与照片无法区分的1024x1024 面部──扩散模型此后在质量和可控性上夺得王位,但使扩散实用的每一个技巧归归化选择、潜空间、特征损失都是首先在GAN 上理解的──

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


### İki ağ

```mermaid
flowchart LR
    Z["z ~ N(0, I)<br/>noise"] --> G["Generator<br/>transposed convs"]
    G --> FAKE["Fake image"]
    REAL["Real image"] --> D["Discriminator<br/>conv classifier"]
    FAKE --> D
    D --> OUT["P(real)"]

    style G fill:#dbeafe,stroke:#2563eb
    style D fill:#fef3c7,stroke:#d97706
    style OUT fill:#dcfce7,stroke:#16a34a
```

- Evet .**generator**G bir gürültü vektörü alır `z`Ve bir görüntü çıkarır.**discriminator**D bir görüntü alır ve tek bir ölçekçi çıkarır: görüntüün gerçek olması olasılığı.

> **生成器**G 接收噪声向量 `z`Ve bir resim çıkardı.**判别器**D 接收一张图像并输出一个标量:该图像为真实图像的概率──

### Oyun

G, D'nin yanılmasını istiyor.

> G 希望 D 判断错, D 希望判断正确──形式化地:

```
min_G max_D  E_x[log D(x)] + E_z[log(1 - D(G(z)))]
```

Sağdan sola okuyun: D gerçek (`log D(real)`) ve sahte (`log (1 - D(fake))`G, D'nin sahte görüntüler üzerinde doğruluğunu en aza indirmektedir.`D(G(z))`- Altı yandan.

> D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:D:`log D(real)`) ve sahte görüntüler`log(1 - D(fake))`D. Yalancı görüntülerin sınıflandırma doğruluğu oranı `D(G(z))`- En yüksek seviyede.

Goodfellow , bu minimumın küresel denge olduğunu kanıtladı .`p_G = p_data`D'nin çıkışları her yerde 0.5'dir ve üretilen ve gerçek dağılımlar arasındaki Jensen-Shannon farklılığı sıfır.

> İyi arkadaşım, bu küçük büyük bir şeyin tüm dünyadaki dengeleme noktasının varlığını kanıtladı.`p_G = p_data`,D tüm konumlarda 0.5 çıkış, üretim dağılım ve gerçek dağılım arasındaki Jensen-Shannon ızgarası sıfırdır.

### Doymayan kayıplar

Yukarıdaki form sayısal olarak dengesiz.`D(G(z))`Her sahte için sıfır yakın, yani `log(1 - D(G(z)))`G'ye göre kaybolan eğilime var. Düzeltme: G'nin kayıpını çevir.

> Yukarıdaki biçim sayısal değer üzerinde sabit değil.`D(G(z))`Her numune sıfıra yakındır.`log(1 - D(G(z)))`G'in derecesi yok olmaya eğilimlidir.

```
L_D = -E_x[log D(x)] - E_z[log(1 - D(G(z)))]
L_G = -E_z[log D(G(z))]                          # non-saturating
```

Şimdi ne zaman ?`D(G(z))`G'nin kaybı büyük ve gradienti bilgilendirici.

> Şimdi, şimdi.`D(G(z))`G'nin kaybı çok büyük, 梯度信息充足──每个现代GAN都使用这个变体训练──

### DCGAN mimarisi kuralları

Radford, Metz, Chintala (2015) yıllarca başarısız deneylerin GAN eğitimini istikrarlı yapan beş kurallara ayrıldı:

> Radford、Metz、Chintala(2015) will多年失败实验的经验提炼为五条使GAN 训练稳定的规则:

1. Birleştirmeyi adım adım konvular (her iki ağ) ile değiştirin.
   Çinçe Çevirimi:                                                                                                                                                                                                                                                            
2. G'nin çıkışı ve D'nin giriş hariç, hem jeneratör hem de ayrımcıda parti normunu kullanın.
   Çinçe çevirisi: G'nin çıkış katmanı ve D'nin giriş katmanı hariç, üreticiler ve ayırt edenler arasında tüm grup birleştirme kullanılır.
3. Daha derin mimarlıklarda tamamen bağlantılı katmanları çıkarın.
   Çinçe Çevirisi:                                                                                                                                                                                                                                                            
4. G, çıkış hariç tüm katmanlarda ReLU kullanır (output için [-1, 1]'de tanh).
   ÇINCE TRÜBLÜK:G tüm katlardan ReLU kullanmak,输出层除外(输出层用 tanh 将值域限制在 [-1, 1])。
5. D, tüm katmanlarda LeakyReLU (negative_slope=0.2) kullanır.
   ÇıkışlıLÜ (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R)  (R) )  (R)  () )  ()  () )

Her modern konfor tabanlı GAN (StyleGAN, BigGAN, GigaGAN) hala bu kurallardan başlayarak parçaları birer birer değiştirir.

> Her modern rollüde dayalı GAN (StyleGAN, BigGAN, GigaGAN) hala bu kurallardan çıkıyor, parçalarını bir bir değiştirmektedir.

### Başarısızlık modları ve imzaları

```mermaid
flowchart LR
    M1["Mode collapse<br/>G produces a narrow<br/>set of outputs"] --> S1["D loss low,<br/>G loss oscillating,<br/>sample variety drops"]
    M2["Vanishing gradients<br/>D wins completely"] --> S2["D accuracy ~100%,<br/>G loss huge and static"]
    M3["Oscillation<br/>G and D keep trading<br/>wins forever"] --> S3["Both losses swing<br/>wildly with no downward trend"]

    style M1 fill:#fecaca,stroke:#dc2626
    style M2 fill:#fecaca,stroke:#dc2626
    style M3 fill:#fecaca,stroke:#dc2626
```

- **Mode collapse**G, D'yi kandırırmak için bir görüntü bulur ve sadece bu görüntü üretir.
  Çinçe Çevirimi: Mode塌G 找到一张能骗过D的图像,然后只生成那张──修复:添加小批量判别、谱归归归归化或标签条件化──
- **Discriminator wins**D'nin daha küçük D'yi düzeltmek, daha düşük D öğrenme oranını artırmak veya etiketleri düzeltmek için gerçek etiketlere uygula.
  Çinçe çevirisi:判别器完胜D 变得太强太快,G 的梯度消失──修复:缩小 D、降低 D 学习率或对真标进行平滑──
- **Oscillation**D'nin (D'nin G'den 2-4 kat daha hızlı öğrenmesi) veya Wasserstein kaybına geçiş.
  Çinçe Çevirimiçi:振荡两个网络交替占优,永远无法接近平衡──修复:TTUR(D 比 G 快 2-4 倍) 或切换到Wasserstein 损失──

### Değerlendirme

GAN'ların temel gerçekleri yok, nasıl çalıştıklarını biliyorsun?

> GAN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

- **Sample inspection** Sadece her dönem sonunda 64 numuneye bak.
  Çinçe Çevirim: نمونے kontrolü  her dönem 末時看 64 个样本──这是不可省略的步骤──
- **FID (Fréchet Inception Distance)** Enception-v3 özellikleri arasındaki gerçek ve üretilen kümelerin dağılımları.
  ÇINCE TRIBULATION:FID(Fréchet Başlangıç Mesafe) 真实集和生成集在 Başlangıç-v3 Özellikler dağılım arasındaki mesafe──越低越好──社区标准──
- **Inception Score** daha yaşlı, daha kırılgan; FID'yi tercih eder.
  Çönem puanı 较老、较脆弱; öncelikli olarak FID kullanmak
- **Precision/Recall for generative models** Kaliteli (düzgünlik) ve kapsamayı (dönüştürme) ayrı ayrı ölçer.
  Çinçe çevirisi:生成模型的精确率/召回率分别衡量质量 (精确率) 和覆盖度 (覆盖率) 〔比单独的FID更有信息量〕

Küçük sentetik veri çalışması için örnek denetimi yeterlidir.

> Küçük boyutlu bir sentetik veri deneyi için, örnek kontrolü yeterlidir.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：工业部署中的视觉系统】**Gerçek endüstriye dağıtımında, görsel modeller gecikme, model büyüklüğü, kenar cihazların uyumlu olması gibi sorunları düşünmelidir. TensorRT, ONNX Runtime, OpenVINO, yaygın olarak kullanılan bir görsel model hızlandırma aracıdır.

> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质――Label Studio、CVAT is the mainstream tagging tool――在工业场景中,主动学习(Active Learning) 标签成本ı azaltabilir:模型对不确定的样本请求人工标签,确定性的样本自动标签──




## Yapın.
```figure
cv-gan-image
```

## Yapın

### Adım 1: Generatör

64 boyutlu gürültü alıyor ve 32x32 görüntü üreten küçük bir DCGAN jeneratörü.

> Küçük bir DCGAN üreticisi, 64 维 gürültü alıyor ve 32x32 图像 üretmektedir.

```python
import torch
import torch.nn as nn

class Generator(nn.Module):
    def __init__(self, z_dim=64, img_channels=3, feat=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.ConvTranspose2d(z_dim, feat * 4, kernel_size=4, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(feat * 4),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(feat * 4, feat * 2, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(feat * 2),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(feat * 2, feat, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(feat),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(feat, img_channels, kernel_size=4, stride=2, padding=1, bias=False),
            nn.Tanh(),
        )

    def forward(self, z):
        return self.net(z.view(z.size(0), -1, 1, 1))
```

4 adet transpose konveyör, her biri `kernel_size=4, stride=2, padding=1`Bu yüzden boşluk büyüklüğünü temiz bir şekilde ikiye katlarlar.

> 4 tane dönüşüm, her kullanımı`kernel_size=4, stride=2, padding=1`Böylece, boşluk boyutu iki katına çıkarılacak.

### İkinci Adım: Ayrımcılık

LeakyReLU, adımlı konvoylar, skalar bir logit ile sona erer.

> Çıkanışlı bir görüntü.

```python
class Discriminator(nn.Module):
    def __init__(self, img_channels=3, feat=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(img_channels, feat, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(feat, feat * 2, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(feat * 2),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(feat * 2, feat * 4, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(feat * 4),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(feat * 4, 1, kernel_size=4, stride=1, padding=0),
        )

    def forward(self, x):
        return self.net(x).view(-1)
```

Son konfor bir `4x4``1x1`. Çıktı görüntü başına tek bir skalar; sadece kayıp hesaplama sırasında sigmoid uygulayın.

> Son bir bölüm`4x4`Özellikleri`1x1`❖ Her resim bir değer çıkarır; sadece kayıp hesaplama sırasında uygulanır.

### Adım 3: Eğitim Adımı

Alternatif: D'yi bir kez, sonra G'yi bir kez, her partide.

> 交替进行: Her parti 先更新 D 一次,再更新 G 一次。

```python
import torch.nn.functional as F

def train_step(G, D, real, z, opt_g, opt_d, device):
    real = real.to(device)
    bs = real.size(0)

    # D step
    opt_d.zero_grad()
    d_real = D(real)
    d_fake = D(G(z).detach())
    loss_d = (F.binary_cross_entropy_with_logits(d_real, torch.ones_like(d_real))
              + F.binary_cross_entropy_with_logits(d_fake, torch.zeros_like(d_fake)))
    loss_d.backward()
    opt_d.step()

    # G step
    opt_g.zero_grad()
    d_fake = D(G(z))
    loss_g = F.binary_cross_entropy_with_logits(d_fake, torch.ones_like(d_fake))
    loss_g.backward()
    opt_g.step()

    return loss_d.item(), loss_g.item()
```

`G(z).detach()`D adımında kritik bir şeydir: güncelleme sırasında G'ye akışan gradientler istemiyoruz.

> D 步骤中的 `G(z).detach()`至关重要: 我们不希望在D的更新过程中梯度流回G―― unutmak tipik bir yeni başlayanın hatasıdır――

### Adım 4: Sintez şekillerde tam eğitim döngüsü

```python
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

def synthetic_images(num=2000, size=32, seed=0):
    rng = np.random.default_rng(seed)
    imgs = np.zeros((num, 3, size, size), dtype=np.float32) - 1.0
    for i in range(num):
        r = rng.uniform(6, 12)
        cx, cy = rng.uniform(r, size - r, size=2)
        yy, xx = np.meshgrid(np.arange(size), np.arange(size), indexing="ij")
        mask = (xx - cx) ** 2 + (yy - cy) ** 2 < r ** 2
        color = rng.uniform(-0.5, 1.0, size=3)
        for c in range(3):
            imgs[i, c][mask] = color[c]
    return torch.from_numpy(imgs)

device = "cuda" if torch.cuda.is_available() else "cpu"
data = synthetic_images()
loader = DataLoader(TensorDataset(data), batch_size=64, shuffle=True)

G = Generator(z_dim=64, img_channels=3, feat=32).to(device)
D = Discriminator(img_channels=3, feat=32).to(device)
opt_g = torch.optim.Adam(G.parameters(), lr=2e-4, betas=(0.5, 0.999))
opt_d = torch.optim.Adam(D.parameters(), lr=2e-4, betas=(0.5, 0.999))

for epoch in range(10):
    for (batch,) in loader:
        z = torch.randn(batch.size(0), 64, device=device)
        ld, lg = train_step(G, D, batch, z, opt_g, opt_d, device)
    print(f"epoch {epoch}  D {ld:.3f}  G {lg:.3f}")
```

`Adam(lr=2e-4, betas=(0.5, 0.999))`DCGAN'ın varsayılan  düşük beta1'si, momentum süreci, rakip oyunu çok fazla istikrarlandırmaktan korur.

> `Adam(lr=2e-4, betas=(0.5, 0.999))`DCGAN'ın önlenmiş yapılandırması  düşük beta1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

### Adım 5: Örnekleme

```python
@torch.no_grad()
def sample(G, n=16, z_dim=64, device="cpu"):
    G.eval()
    z = torch.randn(n, z_dim, device=device)
    imgs = G(z)
    imgs = (imgs + 1) / 2
    return imgs.clamp(0, 1)
```

Örnek alma öncesi her zaman değerlendirme moduna geçin. DCGAN için bu önemlidir çünkü parti normları çalıştırma istatistikleri parti istatistikleri yerine kullanılır.

> 采样前务必切换到 eval 模式── DCGAN için bu çok önemlidir, çünkü birim birleştirme, mevcut parti için değil, çalışma zamanında kullanılacak birim istatistikası için kullanılır──

### Adım 6: Spektral normallaştırma

Şebekenin garantili olan ayrımcıda BN'nin bir yerine 1-Lipschitz girer.

> 谱归归化是判别器中批归归化即插即用替代方案,保证网络是1-Lipschitz 的──能修复大多数"D 赢得太彻底"的问题──

```python
from torch.nn.utils import spectral_norm

def build_sn_discriminator(img_channels=3, feat=64):
    return nn.Sequential(
        spectral_norm(nn.Conv2d(img_channels, feat, 4, 2, 1)),
        nn.LeakyReLU(0.2, inplace=True),
        spectral_norm(nn.Conv2d(feat, feat * 2, 4, 2, 1)),
        nn.LeakyReLU(0.2, inplace=True),
        spectral_norm(nn.Conv2d(feat * 2, feat * 4, 4, 2, 1)),
        nn.LeakyReLU(0.2, inplace=True),
        spectral_norm(nn.Conv2d(feat * 4, 1, 4, 1, 0)),
    )
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


Değişme`Discriminator`için`build_sn_discriminator()`Spektral norm, uygulanabilecek en kolay tek dayanıklılık yükseltmesidir.

> - Ben de .`Discriminator`替换为 `build_sn_discriminator()`后通常就不需要TTUR技巧了──谱归化, uygulayabileceğiniz en basit tek bir 鲁棒性升级──




> **【拓展：视觉模型的持续学习】**Üretim ortamında, görsel modeller yeni verilere sürekli uyum sağlamak gerekir. Yeni ürünler, yeni sahne, yeni ışık koşulları. Sürekli öğrenme. Sürekli öğrenme.

## Çerçeveyi kullanın.

Ciddi jenerasyon için önceden eğitilmiş ağırlıkları kullanın veya difüzyona geçin.

- `torch_fidelity`Aday değerlendirme kodu yazmadan, jeneratörünüzde FID / IS hesaplar.
- `pytorch-gan-zoo`(miras) ve `StudioGAN`DCGAN, WGAN-GP, SN-GAN, StyleGAN ve BigGAN'ın gemi tarafından test edilmiş uygulamaları.

2026 yılında GAN'lar hala: gerçek zamanlı görüntü üretimi (latensi <10 ms), stil transferü, kesin kontrol ile görüntüden görüntüye çevirme (Pix2Pix, CycleGAN) için en iyi seçimdir.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.




## İndirin . Ürünler .

Bu ders şunları ortaya çıkarır:

- `outputs/prompt-gan-training-triage.md` bir eğitim eğri tanımını okuyan ve başarısızlık modunu (modus çöküşü, D- kazançları, titreşim) ve tek önerilen düzeltmeyi seçen bir istek.
- `outputs/skill-dcgan-scaffold.md` DCGAN'dan bir heykel yazma becerisi`z_dim`, hedef`image_size`ve`num_channels`, eğitim döngüsü ve örnek tasarrufu da dahil.

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


## Egzersizler.

1. **(Easy)**Yukarıdaki DCGAN'ı sentetik döngü verisi kümesine ekleyin ve her dönem sonunda 16 numuneyi bir ağla kaydetin.
2. **(Medium)**Farklılık normunu spektral norm ile değiştirin. Her iki versiyonu da yan yana çalıştırın. Hangisi daha hızlı bir şekilde yaklaşıyor? Hangisinin üç tohum arasında daha düşük bir varyansi var?
3. **(Hard)**Şartlı DCGAN uygulayın: sınıf etiketini hem G hem de D'ye ekleyin (G'de gürültüye tek sıcaklık, D'de sınıf ekleme kanalını kısaltın). Ders 7'den sentetik "dahalar vs kare" veri kümesine çalışın ve sınıf koşullandırmasının belirli etiketlerle örnekleme yaparak çalıştığını gösterin.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Generator (G) | "The draws-stuff net" | Maps noise to images; trained to fool the discriminator |
| Discriminator (D) | "The critic" | Binary classifier; trained to distinguish real from generated images |
| Minimax | "The game" | min over G, max over D of an adversarial loss; equilibrium is p_G = p_data |
| Non-saturating loss | "The numerically sane version" | G's loss is -log(D(G(z))) instead of log(1 - D(G(z))) to avoid vanishing gradients early in training |
| Mode collapse | "Generator makes one thing" | G produces only a small subset of the data distribution; fix with SN, minibatch discrimination, or larger batch |
| TTUR | "Two learning rates" | D learns faster than G, typically by a factor of 2-4; stabilises training |
| Spectral norm | "1-Lipschitz layer" | A weight-normalisation that bounds each layer's Lipschitz constant; stops D from becoming arbitrarily steep |
| FID | "Fréchet Inception Distance" | Distance between Inception-v3 feature distributions of real and generated sets; the standard evaluation metric |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Generative Adversarial Networks (Goodfellow et al., 2014)](https://arxiv.org/abs/1406.2661)- Herşeye başlayan gazete.
- [DCGAN (Radford, Metz, Chintala, 2015)](https://arxiv.org/abs/1511.06434) GAN'ları eğitime yararlı kılan mimari kuralları
- [Spectral Normalization for GANs (Miyato et al., 2018)](https://arxiv.org/abs/1802.05957) En faydalı istikrar hilesi
- [StyleGAN3 (Karras et al., 2021)](https://arxiv.org/abs/2106.12423)Son on yılın en büyük şarkıları gibi okuyor.
