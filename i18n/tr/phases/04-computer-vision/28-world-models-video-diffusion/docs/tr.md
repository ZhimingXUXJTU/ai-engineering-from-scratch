# Dünya Modeller & Video Yayınlama

> Bir sahnenin sonraki saniyesini tahmin eden bir video modeli bir dünya simülatörüdür.

> **【中文解读】**能够预测场景接下几秒的视频模型就是一个世界模拟器――预测条件化为动作,就得到了一个学习的游戏引擎――世界模型是AI'nın öncü yönü让AI理解物理世界的动态规律――

> **【拓展：世界模型的前沿】**Sora(OpenAI) ve Genie(DeepMind) dünya modelinin temsilcisi. Dünya modeli otomatik olarak kullanılabilir.

**Type:** Learn + Build | **类型:** 学习 + 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 10 (Diffusion), Phase 4 Lesson 12 (Video Understanding), Phase 4 Lesson 23 (DiT + Rectified Flow) | **前置知识:** Phase 4 Lesson 10（扩散模型），Phase 4 Lesson 12（视频理解），Phase 4 Lesson 23（DiT + 整流流）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Öğrenme hedefleri

- Saf bir video üretimi modeli (Sora 2) ile eylem koşullu bir dünya modeli (Genie 3, DreamerV3) arasındaki farkı açıklayın.
- Bir video DiT'yi tanımlayın: uzay-zaman yamaları, 3D konum kodlaması, T, H, W tokenleri üzerinde ortak dikkat
- Bir dünya modeli robotlara nasıl bağlanır izleyin: VLM planları → video modeli simülasyonu → ters dinamikler eylemler yayar
- Soralı bir kullanım için Sora 2, Genie 3, Runway GWM-1 Worlds, Wan-Video ve HunyuanVideo arasında seçim yapın (yaratıcı video, interaktif sim, otonom sürücü sentezi)

> **【中文解读】**Öğrenme hedefi, ders bitirilmesinden sonra öğrenilmesi gereken temel becerileri listeler.


## Sorunlar. Sorunlar.

Video üretimi ve dünya modeli 2026'da birleşti. Bir dakikalık video oluşturabilen bir model, bir anlamda dünyanın nasıl hareket ettiğini öğrendi: nesnelerin kalıcılığı, yerçekimi, sebepçilik, stil. Eğer bu tahminleri eylemlere (solda yürüyüş, kapıyı aç) şartlandırırsanız, video modeli bir oyun motoru, bir sürücü simülatörü veya bir robotik ortamı değiştirebilecek bir öğrenilebilir simülatör haline gelir.

> Video üretimi ve dünya inşaatı 2026 yılında birleşti. Bir dakika boyunca video üretimi modelinin bir anlamda dünyanın nasıl hareket ettiğini öğrendi: nesnelerin dayanıklılığı, ağırlık, sonuç ilişkileri, biçimleri. Eğer tahminlerde koşul olarak hareket ederseniz (((sol doğru 、 açık), video modeli bir öğrenilebilir bir simülasyon haline gelir, oyun motorunu değiştirebilir, sürücü simülasyon cihazını veya robot ortamını kullanır.

Bahisleri beton. Genie 3 tek bir görüntüden oynanabilir ortamlar oluşturur. Uçuş pistı GWM-1 Dünyaları sonsuz keşfedilebilir sahneleri sentez eder. Sora 2, senkronize edilmiş ses ve modelli fizik ile dakika uzunluğundaki videolar üretir. NVIDIA Cosmos-Drive, Wayve Gaia-2 ve Tesla DrivingWorld, otonom araç eğitim verileri için gerçekçi sürüş videoları üretmektedir. Dünya modeli paradigması robotlar için sessizce sim-real'i ele geçiriyor.

> 利害关系是具体的──Genie 3 From Single张图像生成可玩环境──Runway GWM-1 Worlds 合成无限可探索场景──Sora 2 生成带同步音频和物理建模的分钟级视频──NVIDIA Cosmos-Drive、Wayve Gaia-2 和 Tesla DrivingWorld 为了自动驾驶训练数据生成真实驾驶视频──世界模型范式然接管机器人的真实驾驶视频──

Bu ders 4. aşamada "büyük resim" dersi. Görüntü üretimi, video anlayışı ve ajanik mantıklamaları arxitektura modelinin baskın araştırmanın ilerlediği yönde birleştirir.

> Bu ders, dördüncü aşamada "tam görüntü" dersidir. Görüntü üretimi, video anlama ve akıllı beden düşüncesi ile bağlantılı olarak yönlendirilir.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


### Üç dünya modeli ailesi

```mermaid
flowchart LR
    subgraph GEN["Pure video generation"]
        G1["Text / image prompt"] --> G2["Video DiT"] --> G3["Video frames"]
    end
    subgraph ACTION["Action-conditioned world model"]
        A1["Past frames + action"] --> A2["Latent-action video DiT"] --> A3["Next frames"]
        A3 --> A1
    end
    subgraph RL["World models for RL (DreamerV3)"]
        R1["State + action"] --> R2["Latent transition model"] --> R3["Next latent + reward"]
        R3 --> R1
    end

    style GEN fill:#dbeafe,stroke:#2563eb
    style ACTION fill:#fef3c7,stroke:#d97706
    style RL fill:#dcfce7,stroke:#16a34a
```

- **Sora 2**Bu, sadece video oluşturma, uyarılara bağlı.
  Çeviri:**Sora 2**Sadece video üretimi, önerilerle koşullandırılmış.
- **Genie 3**- Evet .**GWM-1 Worlds**- Evet .**Mirage / Magica**Bu, eylem koşullı dünya modelleri. Gözlemli videolardan gizli eylemleri yerleştirin, sonra eylemler üzerinde gelecek çerçeve tahminlerini koşullandırın.
  Çeviri:**Genie 3**- Evet.**GWM-1 Worlds**- Evet.**Mirage / Magica**Bu, bir videoyu gözlemleyerek potansiyel hareketleri tahmin etmek, sonra da bir projeyi kullanarak bir projeyi öngörmek için kullanılır.
- **DreamerV3**ve klasik RL dünya modeli ailesi açık bir eylem koşullaması ile gizli bir alanda tahmin, ödül sinyalleri üzerinde eğitilmiş. Daha az görsel; örnek verimli RL için daha kullanışlı.
  Çeviri:**DreamerV3**Klasik RL Dünya Model ailesinin potansiyel uzayda öngörü, açık hareket koşulları ile, ödül sinyallerinde eğitim.

### Video DiT mimarisi

```
Video latent:          (C, T, H, W)
Patchify (spatial):    grid of P_h x P_w patches per frame
Patchify (temporal):   group P_t frames into a temporal patch
Resulting tokens:      (T / P_t) * (H / P_h) * (W / P_w) tokens
```

Pozisyonel kodlama 3D'dir: (t, h, w) koordinat başına bir dönümsel veya öğrenilmiş yerleştirme.

- **Full joint** tüm tokenler tüm tokenlere katılır. O(N^2) N tokenlerle. Uzun videolar için yasak.
  Çeviri:**全联合**所有 token 注意所有 token──O(N^2)──对长视频不可行──
- **Divided** değişik zamanlı dikkat (zaman boyunca aynı uzay pozisyonu: `(H*W) * T^2`) ve uzaylı dikkat (eşit zaman aşamasında, uzay boyunca: `T * (H*W)^2`TimeSformer ve çoğu video DiT tarafından kullanılır.
  Çeviri:**分离**交替时间注意力(同一空间位置,跨时间) 和空间注意力(同一时间步,跨空间) ――TimeSformer 和大多数视频 DiT 使用──
- **Window** (t, h, w) yerel pencereler. Video Swin tarafından kullanılır.
  Çeviri:**窗口**(t, h, w) 中的局部窗口──Video Swin 使用──

2026'da her video yayılma modeli bu üç örneğin birinden daha AdaLN şartlandırması (Desin 23) ve düzeltilmiş akış kullanır.

> 2026 yılının her video yayım modeli bu üç modelden birini kullanıyor, AdaLN  koşullandırma 23  ders) ve tüm akış 

### Eylemlerin koşullandırılması: gizli eylem modelleri

Cinsel bir şey öğrenir .**latent action**Bu nedenle, bir modelin dekodörü, açık bir klavye tuşlarında değil, sonuçlandırılmış gizli eylem üzerinde koşullar oluşturur. Sonuçta, bir kullanıcı gizli bir eylem belirleyebilir (veya yeni bir önceden bir örneğe göre) ve model, bu eylemle uyumlu bir sonraki çerçeve üretebilir.

Sora, eylem arayüzünü tamamen atlıyor. Onun dekodörü, geçmiş uzay-zaman tokenlerinden gelecek uzay-zaman tokenlerini tahmin ediyor.

### Fiziksel makulluk

Sora 2'nin 2026'daki çıkışı açıkça ilan edildi.**physical plausibility**: ağırlık, denge, nesne kalıcılığı, sebep ve etkisi. Ekip tarafından el tarafından değerlendirilmiş makullik puanları ile ölçülür; model düşmüş nesneler, çarpışan karakterler ve amaçlı başarısızlıklar (kayıp atlama) karşısında görülebilir bir şekilde iyileşir Sora 1.

Makulluk, baskın başarısızlık modudur. 2024-2025'te insanlar spagetti yiyor veya gözlüklerden içiyor videosunun modelin sürekli nesneler temsil etmemesini ortaya koydu. 2026 modelleri (Sora 2, Runway Gen-5, HunyuanVideo) bunları azaltır, ancak ortadan kaldırmaz.

### Otonom sürücü dünya modelleri

Sürüş dünya modelleri, yoldaki trajektörlere, sınırlama kutularına veya navigasyon haritalarına bağlı gerçekçi yol sahnelerini oluşturur. Kullanım:

- **Cosmos-Drive-Dreams**(NVIDIA) RL eğitimi için dakikalarca sürüş videoları oluşturur.
- **Gaia-2**(Wayve)  Politik değerlendirme için trajektör koşullu sahne sentezi.
- **DrivingWorld**(Tesla)  değişik hava, günün saati, trafik koşullarını simüle eder.
- **Vista**Reaktif sürüş sahnesi sentezi.

Köşe kafesleri için pahalı gerçek dünya verileri toplamalarını değiştirirler  geceleri yaya yürüyüşleri, buzlu kesişmeler, olağandışı araç türleri  aksi takdirde milyonlarca mil sürmeyi gerektirir.

> Bu araçlar, gerçek dünya verileri toplama ve sınır koşullarını ele almak için pahalı gerçek dünya verilerini değiştirdi.

### Robotik yığın: VLM + video modeli + ters dinamik

Yeni çıkan üç bileşenli robotik döngüsü:

> Yeni Yenilenmiş Üç Yapı:

1. **VLM**hedefleri analiz eder ("kırmızı bardakları topla"), yüksek düzeyde bir eylem dizisini planlar.
   Çeviri:**VLM**解析目标("拿起红色杯子"),规划高层动作序列──
2. **Video generation model** N çerçeveleri önümüzdeki gözlemleri tahmin eder.
   Çeviri:**视频生成模型**模拟执行每个动作后样子预测 N 后的观测──
3. **Inverse dynamics model**Bu gözlemleri ortaya çıkaracak beton motor komutlarını çıkarır.
   Çeviri:**逆动力学模型**Bu gözlemlerin yapılması için özel bir elektronik talimat alın.

Bu, ödül şekillendirme ve örnek ağır RL'yi değiştirir. Dünya modeli hayal gücünü yapar; ters dinamikler hareketle ilgili döngüyü kapatır. Genie Envisioner bir örneklemedir; birçok araştırma grubu bu yapıya yaklaşıyor.

> Bu, ödül biçiminin ve örnek yoğunluğunun RL'sini değiştirdi. Dünya modeli sorumlu düşünce; aksine, motoriklik öyküsü yerine getirmek.

### Değerlendirme

- **Visual quality** FVD (Fréchet Video Distance), kullanıcı çalışmaları.
  Çeviri:**视觉质量**FVD(Fréchet 视频距离) 、用户研究。
- **Prompt alignment** Çerçeve başına CLIPS puanı, VQA tarzı değerlendirme.
  Çeviri:**提示对齐**每 CLIPScore、VQA 风格评估──
- **Physical plausibility** Referans değerleri bir takımında (Sora 2'nin iç referans değerleri, VBench) el değeri.
  Çeviri:**物理合理性**在基准套件上人工评分(Sora 2 内部基准、VBench)
- **Controllability**(interaktif dünya modelleri için)  eylem → gözlem tutarlılığı; Önceki bir duruma dönebilir misiniz?
  Çeviri:**可控性**(交互式世界模型) 动作→观测一致性;能否回到前前的状态?

### 2026'da model manzara

| Model | Use | Parameters | Output | License |
|-------|-----|------------|--------|---------|
| Sora 2 | text-to-video, audio | — | 1-min 1080p + audio | API only |
| Runway Gen-5 | text/image-to-video | — | 10s clips | API |
| Runway GWM-1 Worlds | interactive world | — | infinite 3D rollout | API |
| Genie 3 | interactive world from image | 11B+ | playable frames | research preview |
| Wan-Video 2.1 | open text-to-video | 14B | high-quality clips | non-commercial |
| HunyuanVideo | open text-to-video | 13B | 10s clips | permissive |
| Cosmos / Cosmos-Drive | autonomous driving sim | 7-14B | driving scenes | NVIDIA open |
| Magica / Mirage 2 | AI-native game engine | — | modifiable worlds | product |

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：工业部署中的视觉系统】**Gerçek endüstriye dağıtımında, görsel modeller gecikme, model büyüklüğü, kenar cihazların uyumlu olması gibi sorunları düşünmelidir. TensorRT, ONNX Runtime, OpenVINO, yaygın olarak kullanılan bir görsel model hızlandırma aracıdır.

> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质――Label Studio、CVAT is the mainstream tagging tool――在工业场景中,主动学习(Active Learning) 标签成本ı azaltabilir:模型对不确定的样本请求人工标签,确定性的样本自动标签──




## Yapın.
```figure
v4-world-rollout
```

## Yapın

### Adım 1: Video için 3D patchify

```python
import torch
import torch.nn as nn


class VideoPatch3D(nn.Module):
    def __init__(self, in_channels=4, dim=64, patch_t=2, patch_h=2, patch_w=2):
        super().__init__()
        self.proj = nn.Conv3d(
            in_channels, dim,
            kernel_size=(patch_t, patch_h, patch_w),
            stride=(patch_t, patch_h, patch_w),
        )
        self.patch_t = patch_t
        self.patch_h = patch_h
        self.patch_w = patch_w

    def forward(self, x):
        # x: (N, C, T, H, W)
        x = self.proj(x)
        n, c, t, h, w = x.shape
        tokens = x.reshape(n, c, t * h * w).transpose(1, 2)
        return tokens, (t, h, w)
```

Yüklü bir 3D konvoy, çekirdeğe eşit bir adım ile uzay-zamanlı bir patchifier olarak çalışır. `(T, H, W) -> (T/2, H/2, W/2)`- Token şebekesi.

### Adım 2: 3D dönüm pozisyon kodlaması

Rotary Position Embeddings (RoPE)  boyunca ayrı olarak uygulanır`t`- Evet .`h`- Evet .`w`Sekiller:

```python
def rope_3d(tokens, t_dim, h_dim, w_dim, grid):
    """
    tokens: (N, T*H*W, D)
    grid: (T, H, W) sizes
    t_dim + h_dim + w_dim == D
    """
    T, H, W = grid
    n, seq, d = tokens.shape
    if t_dim + h_dim + w_dim != d:
        raise ValueError(f"t_dim+h_dim+w_dim ({t_dim}+{h_dim}+{w_dim}) must equal D={d}")
    assert seq == T * H * W
    t_idx = torch.arange(T, device=tokens.device).repeat_interleave(H * W)
    h_idx = torch.arange(H, device=tokens.device).repeat_interleave(W).repeat(T)
    w_idx = torch.arange(W, device=tokens.device).repeat(T * H)
    # Simplified: just scale channels by frequencies. Real RoPE rotates pairs.
    freqs_t = torch.exp(-torch.log(torch.tensor(10000.0)) * torch.arange(t_dim // 2, device=tokens.device) / (t_dim // 2))
    freqs_h = torch.exp(-torch.log(torch.tensor(10000.0)) * torch.arange(h_dim // 2, device=tokens.device) / (h_dim // 2))
    freqs_w = torch.exp(-torch.log(torch.tensor(10000.0)) * torch.arange(w_dim // 2, device=tokens.device) / (w_dim // 2))
    emb_t = torch.cat([torch.sin(t_idx[:, None] * freqs_t), torch.cos(t_idx[:, None] * freqs_t)], dim=-1)
    emb_h = torch.cat([torch.sin(h_idx[:, None] * freqs_h), torch.cos(h_idx[:, None] * freqs_h)], dim=-1)
    emb_w = torch.cat([torch.sin(w_idx[:, None] * freqs_w), torch.cos(w_idx[:, None] * freqs_w)], dim=-1)
    return tokens + torch.cat([emb_t, emb_h, emb_w], dim=-1)
```

Basitleştirilmiş katkı biçimi. Gerçek RoPE, çiftleşmiş kanalları frekanslarda döndürür; konum bilgileri aynıdır.

### Adım 3: Dikkat blokları

```python
class DividedAttentionBlock(nn.Module):
    def __init__(self, dim=64, heads=2):
        super().__init__()
        self.time_attn = nn.MultiheadAttention(dim, heads, batch_first=True)
        self.space_attn = nn.MultiheadAttention(dim, heads, batch_first=True)
        self.ln1 = nn.LayerNorm(dim)
        self.ln2 = nn.LayerNorm(dim)
        self.ln3 = nn.LayerNorm(dim)
        self.mlp = nn.Sequential(nn.Linear(dim, 4 * dim), nn.GELU(), nn.Linear(4 * dim, dim))

    def forward(self, x, grid):
        T, H, W = grid
        n, seq, d = x.shape
        # time attention: same (h, w), across t
        xt = x.view(n, T, H * W, d).permute(0, 2, 1, 3).reshape(n * H * W, T, d)
        a, _ = self.time_attn(self.ln1(xt), self.ln1(xt), self.ln1(xt), need_weights=False)
        xt = (xt + a).reshape(n, H * W, T, d).permute(0, 2, 1, 3).reshape(n, seq, d)
        # space attention: same t, across (h, w)
        xs = xt.view(n, T, H * W, d).reshape(n * T, H * W, d)
        a, _ = self.space_attn(self.ln2(xs), self.ln2(xs), self.ln2(xs), need_weights=False)
        xs = (xs + a).reshape(n, T, H * W, d).reshape(n, seq, d)
        xs = xs + self.mlp(self.ln3(xs))
        return xs
```

Zaman dikkatinin her uzay pozisyonu boyunca zaman içinde; uzay dikkatinin pozisyonlar boyunca her çerçeve içinde hizmet göstermesi.

### Dördüncü adım: Küçük bir video yaz

```python
class TinyVideoDiT(nn.Module):
    def __init__(self, in_channels=4, dim=64, depth=2, heads=2):
        super().__init__()
        self.patch = VideoPatch3D(in_channels=in_channels, dim=dim, patch_t=2, patch_h=2, patch_w=2)
        self.blocks = nn.ModuleList([DividedAttentionBlock(dim, heads) for _ in range(depth)])
        self.out = nn.Linear(dim, in_channels * 2 * 2 * 2)

    def forward(self, x):
        tokens, grid = self.patch(x)
        for blk in self.blocks:
            tokens = blk(tokens, grid)
        return self.out(tokens), grid
```

Çalışan bir video jeneratörü değil, her parçayı doğru şekillendiren bir yapısal demo.

### Adım 5: Şekilleri kontrol edin

```python
vid = torch.randn(1, 4, 8, 16, 16)  # (N, C, T, H, W)
model = TinyVideoDiT()
out, grid = model(vid)
print(f"input  {tuple(vid.shape)}")
print(f"tokens grid {grid}")
print(f"output {tuple(out.shape)}")
```

Bekle .`grid = (4, 8, 8)`ve `out = (1, 256, 32)`Patching sonrası; başı sonra bir videoya tekrar patched olmaya hazır olarak, per-token uzay-zaman patches'e projesyonlar.

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.





> **【拓展：视觉模型的持续学习】**Üretim ortamında, görsel modeller yeni verilere sürekli uyum sağlamak gerekir. Yeni ürünler, yeni sahne, yeni ışık koşulları. Sürekli öğrenme. Sürekli öğrenme.

## Çerçeveyi kullanın.

2026 yılı için üretim erişim modelleri:

- **Sora 2 API**(OpenAI)  metin-video, senkronize edilmiş ses.
- **Runway Gen-5 / GWM-1**(Runway)  görüntüden videoya, etkileşimli dünyalar.
- **Wan-Video 2.1 / HunyuanVideo** Açık kaynaklı kendi kendine barındırma.
- **Cosmos / Cosmos-Drive**(NVIDIA)  Sürüş simülasyonu açık ağırlıklar.
- **Genie 3** araştırma ön görünümü, erişim talep.

İnteraktif bir dünya modeli demo oluşturmak için: kalite için Wan-Video ile başlayın, etkileşim için gizli eylem adaptörüne katılın.

Robotik için, vahşi bir yığın:

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


1. Dil hedefi -> VLM (Qwen3-VL) -> Yüksek düzeyde plan.
2. Plan -> gizli eylem video modeli -> hayal edilmiş başlatma.
3. Çıkarma -> ters dinamik modeli -> düşük düzeyde eylemler.
4. Eylemler gerçekleştirildi -> gözlem adım 1'e geri döndü.



## İndirin . Ürünler .

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


Bu ders şunları ortaya çıkarır:

- `outputs/prompt-video-model-picker.md` Sora 2 / Runway / Wan / HunyuanVideo / Cosmos arasında seçimler yapılır. Görev, lisans ve gecikme verildi.
- `outputs/skill-physical-plausibility-checks.md` otomatik kontroller ( nesne kalıcılığı, yerçekimi, süreklilik) göndermeden önce herhangi bir video üzerinde çalıştırmak için tanımlayan bir beceri.

## Egzersizler.

1. **(Easy)**5 saniyelik 360p video için işaret sayısını patch-t=2, patch-h=8, patch-w=8'de hesaplayın.
2. **(Medium)**Yukarıdaki bölünmüş dikkat blokunu tam bir ortak dikkat blokuna çevirin ve şekil ve parametreler sayısını ölçün. Gerçek video modellerinde bölünmüş dikkat neden gerekli olduğunu açıklayın.
3. **(Hard)**Minimum bir gizli eylem video modeli oluşturun: (frame_t, action_t, frame_{t+1}) üçlü bir veri kümesi alın (herhangi bir basit 2 boyutlu oyun), eylem gömülmelerine bağlı küçük bir video DiT eğitiniz ve farklı eylemlerin farklı bir sonraki çerçeve ürettiğini gösterin.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| World model | "Learned simulator" | A model that predicts future observations given state and action |
| Video DiT | "Spacetime transformer" | Diffusion transformer with 3D patchification and divided attention |
| Latent action | "Inferred control" | Discrete or continuous action latent inferred from frame pairs; used to condition next-frame generation |
| Divided attention | "Time then space" | Two attention operations per block — across time then across space — to keep O(N^2) manageable |
| Object permanence | "Things stay real" | Scene property that video models must learn; classic failure mode on food, glassware |
| FVD | "Fréchet Video Distance" | Video equivalent of FID; primary visual quality metric |
| Inverse dynamics model | "Observations to actions" | Given (state, next state), output the action that connects them; closes robotics loop |
| Cosmos-Drive | "NVIDIA driving sim" | Open-weights autonomous-driving world model for RL and evaluation |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Sora technical report (OpenAI)](https://openai.com/index/video-generation-models-as-world-simulators/)
- [Genie: Generative Interactive Environments (Bruce et al., 2024)](https://arxiv.org/abs/2402.15391) Gizli eylem dünya modelleri
- [TimeSformer (Bertasius et al., 2021)](https://arxiv.org/abs/2102.05095) Video dönüştürücüler için ayrıntılı ilgi
- [DreamerV3 (Hafner et al., 2023)](https://arxiv.org/abs/2301.04104) RL için dünya modelleri
- [Cosmos-Drive-Dreams (NVIDIA, 2025)](https://research.nvidia.com/labs/toronto-ai/cosmos-drive-dreams/) Sürüş dünya modeli
- [Top 10 Video Generation Models 2026 (DataCamp)](https://www.datacamp.com/blog/top-video-generation-models)
- [From Video Generation to World Model — survey repo](https://github.com/ziqihuangg/Awesome-From-Video-Generation-to-World-Model/)
