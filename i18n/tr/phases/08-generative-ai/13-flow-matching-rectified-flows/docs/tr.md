# Akış Düzelenmesi ve Düzelenmiş Akışlar.

> Diffusion modelleri 20-50 örnekleme adımlarını alırlar çünkü gürültüden veriye eğri bir yol izlerler. Akış eşleşimi (Lipman ve diğerleri, 2023) ve düzeltilmiş akış (Liu ve diğerleri, 2022) düz yollar eğitilmiştir. Daha düz yollar daha az adım anlamına gelir daha hızlı sonuçlama anlamına gelir.

> **【中文解读】**扩散模型需要 20-50 步采样因为走的是曲路径──流匹配和修正流 训练直线路径更直的路径意味着更少步数和更快的推理──SD3、FLUX.1、AudioCraft 2 都在2024年转到流匹配──

> **【拓展：Flow Matching 是 2024-2026 的趋势】**Akış Düzeltme, geleneksel yayılma düzenini yeni nesil üretim modelinin standartlarına dönüştürmeye çalışıyor. Matematik olarak daha iyi, deney olarak daha verimli. SD3 ve FLUX'in kalitesi yükseldiği bu gelişmeye büyük ölçüde bağlıdır.

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 06 (DDPM), Phase 1 · Calculus / 微积分 | **前置知识:** 阶段 8 · 06（DDPM），阶段 1 · 微积分
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Sorunlar. Sorunlar.

DDPM'nin ters süreci, 1000 adımlık bir stohastik yürüyüşten `N(0, I)`Bu nedenle, bu işlemin bir sonraki aşamasında, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir sonraki aşamaları belirlemek için, bir aşamaları belirleme yapmak için, bir aşamaları belirlemeyi belirlemeyi gerektir.

> DDPM'nin ters yönü ise`N(0, I)`DİM, verilerin dağıtımının 1000 adımını 20-50 adımlara kadar daraltır. İdeal olarak adımlar daha az adım sayısını istersen.

Eğer modelin sesden veriye giden yolu * düz çizgi* olsaydı,`t=1`- ...`t=0`Akış eşleşimi bunu doğrudan oluşturur:`x_1 ∼ N(0, I)`- ...`x_0 ∼ data`, vektör alanı trenle`v_θ(x, t)`Zaman türevine eşleşmek için, sonuçta entegre.

> Eğer eğitim modeli gürültü verileri yolunun bir * düz* adım Euler tarafından `t=1`- Ne ?`t=0`Bu kadar yeter. Akış Düzleşimi doğrudan yapılandırın.`x_1 ∼ N(0, I)`- Ne ?`x_0 ∼ data`Bu, bir trenin en önemli kısmı.`v_θ(x, t)`匹配时间导数──

Düzeltilmiş akış (Liu 2022) daha da ileriye gidiyor: adım adım bir reflow prosedürü ile yolları düzeltir ve bu da gittikçe daha yakın bir lineer ODE üretir.

> Düzeltilmiş Akış(2022) Daha da ileri: reflow 过程代拉直路径──两次 reflow 代后,2 步采器匹配 50 步 DDPM 质量──

> **【中文解读】**Akış Dönüşümünün temel düşüncesi:DDPM'nin sesli veri yolları 曲的,需要20-50 步采样.

> **【拓展：FLUX.1 的 Flow Matching 实现】**Black Forest Labs'ın FLUX.1(Stable Diffusion tarafından oluşturulmuştur) Flow Matching'i kullanarak  MMDiT ile birlikte geleneksel yayılma düzenini değiştirir, MMDiT(多模态 DiT) yapı, görüntü kalitesi ve üretim hızı konusunda SDXL'den belirgin bir şekilde daha iyi olmuştur。FLUX.1-schnell  sürümü sadece 4 adımdan sonra yüksek kaliteli görüntü üretilebilir, Flow Matching'in gerçek avantajlarını doğruladı。

## Konsepten bir şey.

![Flow matching: straight-line interpolation between noise and data](../assets/flow-matching.svg)

### Düz çizgi akışı.

Define:

> 定义:

```
x_t = t · x_1 + (1 - t) · x_0,   t ∈ [0, 1]
```

nerede`x_0 ~ data`ve `x_1 ~ N(0, I)`Bu düz çizgi boyunca zaman türevini sabit:

> İçlerinden `x_0 ~ data`- Evet .`x_1 ~ N(0, I)` Bu düz çizginin boyunca zaman yönü bir adetdir:

```
dx_t / dt = x_1 - x_0
```

Nöral vektör alanını tanımlayın `v_θ(x_t, t)`ve bu türevle eşleşmesi için eğitilmiştir:

> 定義神经向量场 `v_θ(x_t, t)`Bu yönlendirmeyi uygula:

```
L = E_{x_0, x_1, t} || v_θ(x_t, t) - (x_1 - x_0) ||²
```

Bu da **conditional flow matching**Bu eğitim simülasyonsızdır: ODE'yi asla açmıyorsunuz.`(x_0, x_1, t)`ve geri çekilme.

> İşte bu.**条件 Flow Matching**损失(Lipman 2023) ―― training is simulation-free 的:你永远不需要展开 ODE──只需要采样`(x_0, x_1, t)`Ve geri dönmek için.

### Örnekleme.

Sonuçta, öğrenilen vektör alanını * geriye* zaman içinde entegre edin:

> 推理时,将学到的量场沿时间*反向*积分:

```
x_{t-Δt} = x_t - Δt · v_θ(x_t, t)
```

Başlayın .`x_1 ~ N(0, I)`, Euler-adımı aşağıya`t=0`- Evet .

> - Evet .`x_1 ~ N(0, I)`開始, Euler 步进降到 `t=0`- Evet.

### Düzeltme akışı (Liu 2022) 整流流(Liu 2022)

Düz çizgi akışı çalışır ama öğrenilen yollar * aslında düz değil *  onlar eğri çünkü birçok `x_0`Aynı yere haritası yapabilirsiniz `x_1`Düzeltilmiş akışın yeniden akış aşaması:

> Doğrudan akış etkili olsa da, öğrenilen yol aslında* gerçekten doğru değil* çünkü çok `x_0`Aynı birinden görüntülenebilir.`x_1`,路径会曲──Türtülmüş Akışın yeniden akışı 步骤:

1. Rastgele eşleştirmeler ile tren akışı modeli v_1.
   UZ随机配对训练 Flow 模型 v_1──
2. Örnek N çift `(x_1, x_0)`'den v_1'i entegre ederek`x_1`İnişine kadar`x_0`- Evet .
   通過将 v_1 `x_1`积分到落点 `x_0`采样 N 对 `(x_1, x_0)`- Evet.
3. Bu çiftler artık "ODE eşleşmiş" olduğundan, aralarındaki düz çizgi interpolant gerçekten daha düz.
   Bu çiftlik örneklerinde v_2.. Çünkü çiftlik şimdi "ODE 匹配" olarak adlandırılır, bunlar arasındaki düz çizgi gerçekten daha düz.
4. Tekrar ediyorum.
   Tekrarlıyorum.

Pratikte 2 reflow iterasyonları, 2-4 adım sonucu çıkarmayı mümkün kılar. SDXL-Turbo, SD3-Turbo, LCM hepsi akışla eşleşen destil modellerdir.

>  Praktiki 2 kez reflow 代就能使路径接近线性,从而支持 2-4 步推理──SDXL-Turbo、SD3-Turbo、LCM 都基于Flow Matching 蒸出的模型──

### Neden 2024'te görüntüler için bu kazanıyor?

Üç neden:

> Üç neden:

1. **Simulation-free training** eğitim sırasında hiçbir ODE çıkmaz, uygulamak önemsiz.
   **无需仿真的训练** training时无需展开 ODE,实现非常简单──
2. **Better loss geometry** Düz yollar tutarlı bir sinyal-gürültü ile karşılaştırılırken DDPM ε-kayıp programın kenarlarında kötü SNR'ye sahiptir.
   **更优的损失几何**直线路径信噪比一致, DDPM'nin ε- kaybı ise SNR 调度边缘 较差──
3. **Faster inference** SDXL-Turbo kalitesiyle 4-8 adım; tutarlılıklı destillasyonla 1 adım.
   **更快的推理**4-8 步即可达到 SDXL-Turbo 质量; 配合一致性蒸可一步生成──

## Akış eşleşimi vs DDPM  tam bağlantı  Akış eşleşimi vs DDPM  精确联系

Gaussian koşullu bir yolla akış eşleşmesi, belirli bir gürültü programı ile * difüsiyondır.`x_t = α(t) x_0 + σ(t) x_1`Zamanlama ve akış eşleşimi , Stratonovich ' in reformülasyonu ile `v = α'·x_0 - σ'·x_1`Bu ikisi Gaussian yolları için cebirsel olarak eşittir.

> Yüksek şartlı yol kullanmak Flow Matching aslında * belirli bir gürültü düzenlemesi* ile yayılma modeli vardır.`x_t = α(t) x_0 + σ(t) x_1`调度后,Flow Matching                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     `v = α'·x_0 - σ'·x_1`                                                                                                                                                                                                                                                              

Akış eşleşimi ne ekledi: hedefin * netliği * (sıradan bir hız), temiz bir kayıp ve Gaussian olmayan interpolantlarla deney yapma izni.

> Akış Düzeltme'nin gerçek katkısı: hedef* açıklık*(sıra hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızlı bir hızla gidermektir.

## Yapın.
```figure
normalizing-flow
```

## Yapın

`code/main.py`1D akış eşleşmesini iki modlu Gaussian karışımı üzerinde uyguluyor.`v_θ(x, t)`Bu, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelik yaparak, bir incelemede, bir incelemede, bir incelemede, bir incelik yaparak, bir incelemede, bir incelemede, bir incelemede, bir incelemede, bir incelemede, bir incelemede, bir incelemede, bir incelemede, bir incelemede, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir

> `code/main.py`İki peyk yüksekliği karışık dağılımda 1-D Akış Düzeltmesi gerçekleştirmek.`v_θ(x, t)`Bu, bir mikro tip MLP, doğrudan hedef eğitimi kullanmak için kullanılır.

### Adım 1: Eğitim kaybı

```python
def train_step(x0, net, rng, lr):
    x1 = rng.gauss(0, 1)
    t = rng.random()
    x_t = t * x1 + (1 - t) * x0
    target = x1 - x0
    pred = net_forward(x_t, t)
    loss = (pred - target) ** 2
    # backprop + update
```

> 訓練損失: 采样噪音                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     `x1`Zamanı `t`, yapılandırma değerleri `x_t`, hedef `x1 - x0`,做平方回归──

### Adım 2: Çok adımlı sonuçlar.

```python
def sample(net, num_steps):
    x = rng.gauss(0, 1)
    for i in range(num_steps):
        t = 1.0 - i / num_steps
        dt = 1.0 / num_steps
        x -= dt * net_forward(x, t)
    return x
```

> Çok adımlı düşünce: Yüksek ses çıkışı, uzun adımlara göre akış açısına doğru.

### Adım 3: Adım sayısını karşılaştırın.

4 adımlı örnekleme cihazının 20 adımlı kaliteye eşleşmesini bekleyin.

> 4 adımlı örnekleme cihazı 20 adımlı kaliteye uygun hale getirilmeli.

## Tuzaklar.

- **Time parameterization.**Akış eşleşimi kullanımı `t ∈ [0, 1]`- Evet .`t=0`Verilerde,`t=1`DDPM kullanıyor `t ∈ [0, T]`- Evet .`t=0`Verilerde,`t=T`Aynı yönde, farklı ölçekte.
  时间参数化: Akış Eşleşimi `t ∈ [0, 1]`- Evet .`t=0`Verilerde,`t=1`Bu sesle ilgili bir konuşma yap .`t ∈ [0, T]`, yön aynı ama ölçüsü farklı.
- **Schedule choice.**Düzeltilmiş akışın düz çizgisi "akış eşleşme" programıdır, ancak daha iyi ölçek kapsamı için cosine veya logit-normal t örneğini kullanabilirsiniz (SD3 bunu yapar).
  调度选择:Türtülmüş Akışın düz çizgisi "standard" 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调调度 调度 调调度 调调调调调调调调调调调度 调调调调度调调调调调调调调调调
- **Reflow cost.**Yeniden akış için çiftleştirilmiş veri kümesini oluşturmak, örnek başına tam bir sonuç geçişidir. Sadece 1-2 adım sonuç almanız gerektiğinde tekrar akış yapın.
  Reflow 成本: reflow oluşturmak 配对数据集 配对数据集 配对数据集 配对数据集 配对数据集 配对数据集 配对数据集 配对数据集 配对数据集 配对数据集 配对数据集 配对数据集 配对数据集 配件 配对数据集 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配件 配
- **Classifier-free guidance still applies.**Sadece düzeltilen kombinasyonda ε ile v arasında değiş: `v_cfg = (1+w) v_cond - w v_uncond`- Evet .
  Sınıflandırıcı-Ücretsiz Rehberlik  hala uygundur: sadece 线性组合里 ε 换成 v:`v_cfg = (1+w) v_cond - w v_uncond`- Evet.

## Çerçeveyi kullanın.

| Use case / 用途 | 2026 stack / 2026 技术栈 |
|----------|-----------|
| Text-to-image, best quality / 最佳质量文生图 | Flow matching: SD3, Flux.1-dev |
| Text-to-image, 1-4 steps / 1-4 步文生图 | Distilled flow matching: Flux.1-schnell, SD3-Turbo, SDXL-Turbo |
| Real-time inference / 实时推理 | Consistency distillation from a flow-matched base (LCM, PCM) |
| Audio generation / 音频生成 | Flow matching: Stable Audio 2.5, AudioCraft 2 |
| Video generation / 视频生成 | Flow matching mixed with diffusion (Sora, Veo, Stable Video) |
| Science / physics / 科学/物理 | Flow matching + equivariant vector field |

Bir makalede 2025-2026 yıllarında "difüzondan hızlı" dediğinde neredeyse her zaman akış eşleşmesi + destillasyon oluyor.

> "Böylesene daha hızlı yayılmak" dediğinde, neredeyse her zaman akış eşleşmesi + 蒸。

## İndirin . Ürünler .

- Kaydet .`outputs/skill-fm-tuner.md`. Skill, bir difüzyon tarzında model özellikini alır ve onu akışla eşleşen bir eğitim yapılandırmasına dönüştürür: program seçimi, zaman örneklemesi dağılımı (eşit / logit-normal), optimizer, reflow planı, hedef adım sayımı, eval protokolü.

> 保存为 `outputs/skill-fm-tuner.md`◊ bu beceri bir yayılma modeli düzenini alır, onu Flow Eşleşme  eğitim konumu olarak dönüştürür:调度选择、时间采样分布(uniform / logit-normal) 、优化器、reflow 计划、目标步数、评估协议。

## Egzersizler.

1. **Easy.**Çık .`code/main.py`ve gerçek veri dağıtımına karşı 1 adım vs 20 adım MSE karşılaştırın.
   **简单。**运行  İşlem`code/main.py`, gerçek verilerin dağıtımına göre 1 ve 20 adım arasındaki MSE'yi karşılaştırın.
2. **Medium.**Üniforma ' dan geç .`t`Örneklemeyi normal logit'e (t ortasında örneklemeyi yoğunlaştırır) yapılır.
   **中等。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `t`采样切换为 logit-normal (), 模型质量是否提升 (), 模型质量是否提升 (), 模型质量是否提升 (), 模型质量是否提升 (), 模型质量是否提升 (), 模型质量是否提升 (), 模型质量是否提升 (), 模型质量是否提升 (), 模型质量是否提升 (model质量是否提升)
3. **Hard.**Bir reflow iterasyonunu uygulayın: ilk modeli entegre ederek çiftleştirilmiş (x_0, x_1) oluşturun, çiftler üzerinde ikinci bir model eğitiniz ve 1 adım örnek kalitesini karşılaştırın.
   **困难。**实现一次反流 代:通过对对第一个模型积分生成对对 (x_0, x_1),在对对上训练第二模型,并比较 1 步采样质量──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Flow matching | "Straight-line diffusion" | Train `v_θ(x, t)` to match `x_1 - x_0` along an interpolant. |
| Rectified flow | "Reflow" | Iterative procedure that straightens learned flows. |
| Velocity field | "v_θ" | Output of the model — the direction to move `x_t`. |
| Straight-line interpolant | "The path" | `x_t = (1-t)·x_0 + t·x_1`; trivial target derivative. |
| Euler sampler | "1st order ODE solver" | Simplest integrator; works well when paths are straight. |
| Logit-normal t | "SD3 sampling" | Concentrate `t` sampling toward mid-values where gradients are strongest. |
| Consistency distillation | "1-step sampler" | Train a student to map any `x_t` directly to `x_0`. |
| CFG with velocity | "v-CFG" | `v_cfg = (1+w) v_cond - w v_uncond`; same trick, new variable. |

## Üretim Notu: Flux.1-schnell en hızlı akış eşleşme süresi .

Flow matching'in üretim kazancı Flux.1-schnell  bir akış eşleşen DiT Flux-dev dereceli kalitesi korurken 1-4 sonuçlandırma adımlarına doğru destillenir. Niels'in "Run Flux on an 8GB machine" not defteri referans dağıtım tarifi: T5 + CLIP kodlaması, kuantistik MMDiT tanımlaması (sharp vs. 50 için 4 adım), VAE kodlaması.

> Flow Matching in production is Flux.1-schnell a蒸到 1-4 步推理、保持 Flux-dev 级质量的 Flow-Matched DiT──Niels'in "Flow on 8GB 机器上运行Flux" defteri referans deployment方案:T5 + CLIP 编码、量化 MMDiT 去噪(schnell 4 步 vs dev 50 步)、VAE 解码──成本核算:

| Variant | Steps | Latency at 1024² on L4 | Total FLOPs (relative) |
|---------|-------|------------------------|------------------------|
| Flux.1-dev (raw) | 50 | ~15 s | 1.0× |
| Flux.1-schnell | 4 | ~1.2 s | 0.08× (12× faster) |
| SDXL-base | 30 | ~4 s | 0.25× |
| SDXL-Lightning 2-step | 2 | ~0.3 s | 0.03× |

Üretim kuralı: **flow-matched base + distillation = the 2026 default for fast text-to-image.**Her büyük satıcı bu kombinasyonu gönderir: SD3-Turbo (SD3 + akış + destillasyon), Flux-schnell (Flux-dev + düzeltilmiş akış düzeltmesi), CogView-4-Flash.

> Doğum kuralları:**Flow-Matched 基座 + 蒸馏 = 2026 年快速文生图的默认方案。**Her ana üreticisi bu tür bir kombinasyon geliştirdi:SD3-Turbo(SD3 + akış + 蒸)、Flux-schnell(Flux-dev + Düzeltilmiş Akış 拉直)、CogView-4-Flash──纯扩散基座只为遗留检查点保留──

## Daha fazla okumak

- [Liu, Gong, Liu (2022). Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/abs/2209.03003) Düzeltilmiş akış.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) akış eşleşimi.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) SD3, ölçekte düzeltilmiş akış.
- [Albergo, Vanden-Eijnden (2023). Stochastic Interpolants](https://arxiv.org/abs/2303.08797) FM + yayılımı kapsadığı genel çerçeve.
- [Song et al. (2023). Consistency Models](https://arxiv.org/abs/2303.01469) 1 aşamalı difüzyon/ akış destilasyonu.
- [Sauer et al. (2023). Adversarial Diffusion Distillation (SDXL-Turbo)](https://arxiv.org/abs/2311.17042)Turbo varianti.
- [Black Forest Labs (2024). Flux.1 models](https://blackforestlabs.ai/announcing-black-forest-labs/) üretimdeki akış eşleşimi.
