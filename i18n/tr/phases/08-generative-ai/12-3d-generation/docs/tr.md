# 3D Nesli 3D Gelişim

> 3D, 2D-den 3D'ye en güçlü kaldıraçın bulunduğu modalitedir. 2023'te 3D Gaussian Splating'in atılımını gerçekleştirdi. 2024-2026 generatif itme katmanları bir tek istek veya fotoğraftan nesneler ve sahneleri üretmek için üstte çok görüntü yayılması + 3D rekonstrüksiyon.

> **【中文解读】**3D, 2D ile 3D arasındaki en güçlü bağlantı biçimidir. 2023 yılının başlaması 3D Gaussian Splating, 2024-2026 yıllarının üretme eğilimidir.

> **【拓展：3D 生成的应用】**3D 生成用于游戏资产创建、VR/AR 内容、建筑设计、电商产品展示──DreamGaussian、TripoSR 等模型可在秒级从文字/图片生成 3D模型──

**Type:** Learn / 学习型
**Languages:** Python
**Prerequisites:** Phase 4 (Vision / 视觉), Phase 8 · 07 (Latent Diffusion / 潜在扩散)
**Time:** ~45 minutes

## Sorunlar. Sorunlar.

3 boyutlu içerik acı verici:

> 3D 内容很困难:

- **Representation.**Meshler, nokta bulutları, voksel ağları, imzalanan mesafe alanları (SDF), nöral ışın alanları (NeRF), 3 boyutlu Gaussians. Her birinin özelliği vardır.
  **表示方式。**网格、点云、体素、SDF、NeRF、3D 高斯──各有权衡──
- **Data scarcity.**ImageNet'in 14 milyon görüntü olduğu görüldü. En büyük temiz 3D veri kümesi (Objaverse-XL, 2023) ~ 10 milyon nesneye sahip, en düşük kalitede.
  **数据稀缺。**ImageNet'de 14 milyon görüntü var. En temiz 3D verileri 1000'e yakın. Çoğu düşük kaliteli.
- **Memory.**5123 voksel şebekesi 128M voksel; yararlı bir sahne NeRF'nin 1M örnek / ışın ihtiyacı vardır.
  **内存。**5123 vücut sayısı 1.28 milyar vücut sayısı.
- **Supervision.**2 boyutlu bir görüntü için pikseller vardır. 3 boyutlu bir görüntü için genellikle bir avuç 2 boyutlu görüntü vardır ve 3 boyutlu bir görüntüye yükselmek gerekir.
  **监督。**2D görüntüde bir resim vardır.

2026 yığın iki sorunu ayırır. Birincisi, * 2D çok görüntü görüntülerini * bir yayılma modeli ile oluşturmak. İkincisi, * 3D temsil * (genellikle Gaussian splating) bu görüntülere uyumlu.

> 2026 yılının programı iki aşamada: önce genişletilmiş model üretmek * 2D 多视角图像*, tekrar kullanmak * 3D göstermek *(genellikle yüksek 射) 拟合──

> **【中文解读】**3D üretiminin temel zorluğu: gösterim biçimi çok çeşitli(网格、点云、体素、SDF、NeRF、3D 高斯) 、数据稀缺(远低于2D 图像) 、内存需求巨大、监督信号弱(通常只有2D 视图) ⋅2026 yılının ana akım programı iki aşamalı strateji: önce genişletilmiş model kullanmak çoklu bir 2D 图像 üretmek, yeniden 3D 高斯射(Gaussian Splating) uygun 3D göstermek için kullanmak.

> **【拓展：3D Gaussian Splatting 的革命性影响】**3DGS(2023) NeRF'i değiştirmek için 3D yeniden inşa etme ana akımlı bir yöntem haline geldi. Bu, milyonlarca 3D yüksek bolü görüntüleme sahnesini kullanıyor, 染速度快100 倍以上,质量相当或更优──结结合多视角扩散模型,3DGS, oyunlarda, VR/AR'da, yapısal görsellikte büyük bir uygulama önemi vardır.

## Konsepten bir şey.

![3D generation: multi-view diffusion + 3D reconstruction](../assets/3d-generation.svg)

### Temsil: 3D Gaussian Splatting (Kerbl et al., 2023)

Bir sahneyi ~ 1M 3D Gaussians bulutu olarak temsil eder. Her birinin 59 parametri vardır: konum (3), kovarians (6, veya kwaternion 4 + ölçek 3), bulanıklık (1), küre-harmonik renk (48 derece 3, 3 derece 0).

Rendering = projeksiyon + alfa kompozisyon. Hızlı (~ 4090'da 1080p'de 100 fps). Farklılaştırılabilir. Yer gerçekliği fotoğraflarına göre gradient düşüşü ile uyumlu. Bir sahne tüketici GPU'da 5-30 dakika içinde uyumludur.

2023-2024 yılları arasında iki yenilik:
- **Generative Gaussian splats.**LGM, LRM, InstantMesh gibi modeller bir veya birkaç görüntüden doğrudan Gaussian bulutunu tahmin ediyor.
- **4D Gaussian Splatting.**Dinamik sahneler için çerçeve karşılığı olan Gaussians.

### Çok görüntüli yayılma

Tek bir metin istasyonundan veya tek bir görüntüden aynı nesnenin birden fazla tutarlı görüntü oluşturmak için önceden eğitilmiş bir görüntü yayılma modeli ince ayarlayın. Zero123 (Liu et al., 2023), MVDream (Shi et al., 2023), SV3D (Stability, 2024), CAT3D (Google, 2024). Genellikle nesnenin etrafında 4-16 görüntü çıkartılır, Gaussian splating veya NeRF üzerinden 3D'ye kaldırılır.

### Metin--3D boru hattı

| Model | Input | Output | Time |
|-------|-------|--------|------|
| DreamFusion (2022) | text | NeRF via SDS | ~1 hour per asset |
| Magic3D | text | mesh + texture | ~40 min |
| Shap-E (OpenAI, 2023) | text | implicit 3D | ~1 min |
| SJC / ProlificDreamer | text | NeRF / mesh | ~30 min |
| LRM (Meta, 2023) | image | triplane | ~5 s |
| InstantMesh (2024) | image | mesh | ~10 s |
| SV3D (Stability, 2024) | image | novel views | ~2 min |
| CAT3D (Google, 2024) | 1-64 images | 3D NeRF | ~1 min |
| TripoSR (2024) | image | mesh | ~1 s |
| Meshy 4 (2025) | text + image | PBR mesh | ~30 s |
| Rodin Gen-1.5 (2025) | text + image | PBR mesh | ~60 s |
| Tencent Hunyuan3D 2.0 (2025) | image | mesh | ~30 s |

2025-2026 yönü: oyun motorları için uygun PBR malzemeleri ile doğrudan metin-a-ağ modelleri.

### NeRF (tüm bağlam için)

Nöral Radyans Alanı (Mildenhall et al., 2020).`(x, y, z, view direction)`ve çıkışlar `(color, density)`.Sınır boyunca entegre ederek gösterir. Ağ tabanlı yenilikçi görüntü sentezini kaliteli olarak yenir, ancak gösterim 100-1000 kat daha yavaş.

## Yapın.
```figure
v4-3d-multiview
```

## Yapın

`code/main.py`Oyuncak 2D "Gaussian splating" uyumunu uyguluyor: sentetik bir hedef görüntüsünü (sımsıkı bir gradient) 2D Gaussian splatların toplamı olarak temsil eder. Hedefle uyumlu olarak gradient düşüşüyle konumları, renkleri ve kovariansaları optimize edin. İki temel işlem görüyorsunuz: ileriye dönüştürme (splat + alfa-kompozite) ve gradient düşüşüyle uyumlu.

### Adım 1: 2D Gaussian splat

```python
def gaussian_at(x, y, gaussian):
    px, py = gaussian["pos"]
    sigma = gaussian["sigma"]
    d2 = (x - px) ** 2 + (y - py) ** 2
    return math.exp(-d2 / (2 * sigma * sigma))
```

### Adım 2: Çelişkileri toplamla göster

```python
def render(image_size, gaussians):
    img = [[0.0] * image_size for _ in range(image_size)]
    for g in gaussians:
        for y in range(image_size):
            for x in range(image_size):
                img[y][x] += g["color"] * gaussian_at(x, y, g)
    return img
```

Gerçek 3 boyutlu Gaussian splattering, derinlik ve alfa kompozisyonları ile Gaussianları sıralar.

### Adım 3: Şekil düşüşe göre uyumlu

```python
for step in range(steps):
    pred = render(size, gaussians)
    loss = mse(pred, target)
    gradients = compute_grads(pred, target, gaussians)
    update(gaussians, gradients, lr)
```

## Tuzaklar.

- **View inconsistency.**Eğer 4 görüntü bağımsız olarak oluşturursanız ve nesnelerin yapısı hakkında anlaşmazlıkları varsa, 3D uyum bulanık olur.
- **Back-side hallucination.**Tek görüntü → 3D görünmeyen tarafı icat etmek zorunda.
- **Gaussian splat explosion.**Sınırsız eğitim 10M yerlere ve fazlalıklara ulaşmaktadır.
- **Topology issues.**İrtisyen alanlardan (SDF) kaynaklanan ağlar genellikle deliklere veya kendi kendine kesişmelerine sahiptir.
- **License of training data.**Objaverse'ın karıştırılmış lisansları vardır; ticari kullanım model başına değişir.

## Çerçeveyi kullanın.

| Task / 任务 | 2026 pick / 2026 选择 |
|------|-----------|
| Scene reconstruction from photos / 照片场景重建 | Gaussian splatting (3DGS, Gsplat, Scaniverse) |
| Text-to-3D object for games / 文本生成游戏 3D | Meshy 4 or Rodin Gen-1.5 (PBR output) |
| Image-to-3D / 图像生成 3D | Hunyuan3D 2.0, TripoSR, InstantMesh |
| Novel-view synthesis from few images / 少样本新视角 | CAT3D, SV3D |
| Dynamic scene reconstruction / 动态场景重建 | 4D Gaussian Splatting |
| Avatar / clothed human / 虚拟人/穿衣人体 | Gaussian Avatar, HUGS |
| Research / SOTA / 研究 | Whatever dropped last week / 上周发布的任何模型 |

Bir oyun veya e-ticaret borusunda 3D üretim nakliye için: Meshy 4 veya Rodin Gen-1.5 çıkış PBR ağları doğrudan Unity / Unreal'e gider.

> Oyun veya elektronik akışın içinde 3D: Meshy 4 veya Rodin Gen-1.5 输出可直接用于 Unity/Unreal 的 PBR 网格──

## İndirin . Ürünler .

- Kaydet .`outputs/skill-3d-pipeline.md`. Skill 3D bir özet alır (gelenek: metin / bir görüntü / birkaç görüntü; çıkış: mesh / splat / NeRF; kullanımı: render / oyun / VR) ve çıkışlar: boru hattı (çok görüşlü difüzyon + uyum veya doğrudan mesh modeli), temel model, iterasyon bütçesi, topoloji sonrası işleme, gerekli malzeme kanalları.

## Egzersizler.

1. **Easy.**Çık .`code/main.py`4, 16, 64 Gaussians ile.
2. **Medium.**RGB'ye kadar uzanın.
3. **Hard.**Gsplat veya Nerfstudio kullanarak, 50 fotoğraf çekiminden gerçek bir nesne yeniden oluşturun.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 3D Gaussian Splatting | "3DGS" | Scene as a cloud of 3D Gaussians; differentiable alpha-composite render. |
| NeRF | "Neural radiance field" | MLP that outputs color + density at a 3D point; render by ray integration. |
| Triplane | "Three 2-D planes" | Factor 3D into three 2-D axis-aligned feature grids; cheaper than volumetric. |
| SDS | "Score distillation sampling" | Train 3D model by using 2D-diffusion score as pseudo-gradient. |
| Multi-view diffusion | "Many views at once" | Diffusion model that outputs a batch of consistent camera views. |
| PBR | "Physically-based rendering" | Material with albedo, roughness, metallic, normal channels. |
| Densification | "Grow splats" | 3DGS training heuristic: split / clone splats in high-gradient regions. |

## Üretim Not: 3D'de henüz ortak bir altyapı yok.

Görüntü (latent difüzyon + DiT) ve video (spatiotemporal DiT) aksine, 3D'nin 2026'da tek bir baskın çalıştırma süresi yoktur.

- **NeRF / triplane.**5122 renderi milyonlarca MLP ileri gerektirir. Rayon örneklerini agresif bir şekilde toplayın; SDPA/xformers uygulanır.
- **Multi-view diffusion + LRM reconstruction.**İki aşamalı boru hattı. 1 aşamalı (çok görüntü DiT) bir difüzyon sunucusu olarak ders 07. 2 aşamalı (LRM transformatör) bir atış ileri görüşler üzerinde geçmek. genel gecikme profili "difüzyon + bir atış"  seçin aşama göre hizmet ilkesi.
- **SDS / DreamFusion.**Aset başına optimizasyon, sonuç değil.

2026 ürünlerinin çoğu için doğru cevap "iltimos üzerine bir çok görüntü yayılma modeli çalıştırın, asinkron olarak 3DGS'e yeniden yapılandırın, gerçek zamanlı görüntüleme için 3DGS'e hizmet verin". Bu, iş yükünü temiz bir GPU-inference sunucusu (hızlı) ve bir çevrimdışı optimizör (yavaş) arasında bölüyor.

## Daha fazla okumak

- [Mildenhall et al. (2020). NeRF: Representing Scenes as Neural Radiance Fields](https://arxiv.org/abs/2003.08934)NeRF.
- [Kerbl et al. (2023). 3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://arxiv.org/abs/2308.04079)3DGS.
- [Poole et al. (2022). DreamFusion: Text-to-3D using 2D Diffusion](https://arxiv.org/abs/2209.14988) SDS.
- [Liu et al. (2023). Zero-1-to-3: Zero-shot One Image to 3D Object](https://arxiv.org/abs/2303.11328)- Zero123.
- [Shi et al. (2023). MVDream](https://arxiv.org/abs/2308.16512) Çoklu görüntü yayılması.
- [Hong et al. (2023). LRM: Large Reconstruction Model for Single Image to 3D](https://arxiv.org/abs/2311.04400) LRM.
- [Gao et al. (2024). CAT3D: Create Anything in 3D with Multi-View Diffusion Models](https://arxiv.org/abs/2405.10314)- CAT3D.
- [Stability AI (2024). Stable Video 3D (SV3D)](https://stability.ai/research/sv3d)- SV3D.
