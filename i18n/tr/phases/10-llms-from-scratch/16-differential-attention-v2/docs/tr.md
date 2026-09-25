# Farklı Dikkat (V2) 差分注意力 (V2)

> Softmax dikkat, eşleşmeyen her token üzerinde küçük bir olasılık yayar. 100 bin'den fazla token, bu gürültü toplar ve sinyali boğar. Farklı Transformer (Ye et al., ICLR 2025) dikkatini iki softmax farkı olarak hesaplayarak, paylaşılan gürültü zemini çıkararak düzeltir. DIFF V2 (Microsoft, Ocak 2026) üretim yığınının yeniden yazılmasıdır: Decode latensiyle baseline Transformer'a eşleşen, özel çekirdekler olmayan, FlashAttention uyumlu. Bu ders, Stdlib Python'da çalıştırabileceğiniz fark işlevi uygulaması ile V1'den V2'ye kadar sonundan sonuna kadar.

> **【中文解读】**Softmax dikkat her eşleşmeyen token dağıtımı için küçük olasılıkla, 100K token'un üst ve üst içindeki gürültü birikimi sular sinyalleri oluşturur.

> **【拓展：长上下文优化】**差分注意是长上下文 LLM 优化的重要方向之一──100K+ token'ın üst üst aşağı penceresinde, standart dikkatin "注意力稀释" sorunu giderek daha ciddi hale geldiğinde,差分注意力, bir kurbansız akıl hızının bir çözümü sağladı──

>  **【前置】**Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemlilikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklikliklik
>  **【类比】**标准 Softmax = 大合唱里听不清独唱;; 噪音从所有方向传来);;差分注意力 = 双耳降噪耳机两个麦克风;;

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 02 (self-attention), Phase 7 · 15 (attention variants), Phase 10 · 14 (architecture walkthrough)
**Time:** ~60 minutes

## Öğrenme hedefleri

- Softmax dikkatinin neden gürültü zemine sahip olduğunu ve neden bağlam uzunluğu ile büyüdüğünü kesin olarak belirtin.
   Detaktif açıklama softmax dikkat çekme neden gürültü tabanı var ve neden aşağıdaki uzunluk artışı ile birlikte
- Farklı dikkat formülü'nü çıkarın ve çekim sinyalin korunmasıyla birlikte paylaşılan gürültü bileşenini neden iptal ettiğini açıklayın.
  推导差分注意力公式, neden azalma ile paylaşılmış gürültü miktarı ortadan kaldırılabileceğini açıklayın
- V1-V2 farkını izleyin: ne daha hızlı, ne daha basit, ne daha istikrarlı ve neden her değişiklik üretim öncesi eğitim için gerekli oldu.
  V1 ile V2 arasındaki fark: ne hızlandı, basitleştirildi, sabitlendi ve neden üretim öncesi eğitiminde değişiklikler yapılması gerektiği
- Saf Python'da sıfırdan farklı dikkat uygulayın ve sentetik sinyal artı gürültü sorgularında gürültü iptal etme özelliğini empiri olarak doğrulayın.
  Temiz Python ile sıfırdan gerçekleşen fark farkı dikkat, sentetik sinyal artı ses sorgularında deneysel kanıtlar gürültü giderme özellikleri

## Sorunlar. Sorunlar.

Standart softmax dikkat, matematik özelliklerine sahip ve bu da ölçekte bir operasyonal baş ağrısına dönüşür.`q`, dikkat ağırlıkları `softmax(qK^T / sqrt(d))`Softmax asla tam sıfırlar üretemez  her eşleşmeyen token bazı pozitif kütle elde eder. O kalan kütle gürültüdür ve bağlam uzunluğu ile ölçebilir. 128k jetonlarda, her eşleşmeyen jeton sadece % 0.001% olasılığı alırsa bile, bunların toplamının yaklaşık % 127.999'ünü birleştirir.

> 標準軟max dikkatin bir matematiksel özelliği vardır, büyüklüğünde işleyişin baş ağrısı haline gelir.`q`, dikkat çekme hakkı `softmax(qK^T / sqrt(d))`❖ Softmax 永远不能产生精确零 每个不匹配的代币都获得一些正质量──那残余质量是噪音,且随下文长度增长──在128k 时,即使每一个不匹配的代币只获得0.001%的概率,127.999 个加起来贡献了约12%.模型必须学会绕过一个随下文增长的噪音底──

Empirik olarak bu dikkat başı müdahalesi olarak ortaya çıkar: uzun bağlamlı RAG'de halüsinasyonlu alıntılar, 100k işaretini almak görevlerinde ortalama başarısızlıklar ve 32k'den fazla iğne-haystack referanslarında ince doğruluk bozulması. Farklı Transformatör kağıdı (arXiv:2410.05258, ICLR 2025) boşluğu ölçtü: DIFF Transformatörler daha düşük karmaşıklığa, daha yüksek uzun bağlam doğruluğuna ve aynı boyutdaki temel çizgilerden daha az halüsinasyona sahipti.

> 經驗上, bu ifade dikkat başı rahatsızlığı için gösterilmiştir:长上下文 RAG 中的幻觉引用、100k 代币 检索任务的中间丢失失,以及 32k 以上草堆找针基准测试中的微妙精度下降── Diferential Transformer 论文(arXiv:2410.05258, ICLR 2025) 差距:DIFF Transformer 达到更低的困惑度、更高的长上下文精度和更少的幻觉──

DIFF V1'in sınır öncesi eğitim boru hattlarından uzak tutmak için üç sorunu vardı. Değer kaşını her dekodlama adımına iki kez yüklemek zorunda kaldı, FlashAttention uyumluluğunu kıran özel CUDA çekirdekleri gerektirdi ve baş başına RMSNorm 70B-+ ölçekte uzun süreli eğitimleri istikrarsızlaştırdı. DIFF V2 (Microsoft unilm blog, 20 Ocak 2026) üçü de düzeltti. Bu ders her iki versiyonu da yürütüyor, fark operatörünü oluşturur ve oyuncak sorusunda gürültü iptalini referanslandırıyor.

## Konsepten bir şey.

> **【中文解读】**差分注意力 (Differential Attention) İki bağımsız softmax fark değerini hesaplayarak dikkat gürültüsünü ortadan kaldırmak için, modelin gerçekle ilgili bilgilere daha fazla odaklanmasını sağlar. Bu yöntem dikkat mekanizmasındaki dikkat dağılımı problemini azaltır.

> **【拓展：注意力机制的演进】**差分注意力── MLA 差分注意力── DeepSeek-V3'ün KV-cache 压缩ed 约10倍, is推理效率的关键创新──


### Softmax'ın gürültü zemini

Bir sorgu için .`q`Ve anahtarlar `K = [k_1, ..., k_N]`, dikkat ağırlıkları:

```
w_i = exp(q . k_i / sqrt(d)) / sum_j exp(q . k_j / sqrt(d))
```

Hayır .`w_i`- Eğer...`k_i`tamamen bağlantısı yok.`q`, puanı `q . k_i`0 değil  varyansa ile sıfır etrafında dalgalanır `||q||^2 / d`Softmax normalleştikten sonra, her ilişkisi olmayan token hala katkıda bulunur.`O(1/N)`Bağlantı olmayan tokenlerin toplam katkı oranı `O((N-1)/N) = O(1)` küçük bir miktar değil.

Model, sert bir üst k gibi bir şey istiyor: eşleşen tokenlarda yüksek ağırlık, diğer yerlerde neredeyse sıfır ağırlık. Softmax bunu doğrudan yapamayacak kadar düzgün.

### Farklılık fikri

Her başın Q ve K projeksiyonlarını iki bölüme ayırın: Q = (Q_1, Q_2) ve K = (K_1, K_2). İki dikkat haritasını hesaplayın:

```
A_1 = softmax(Q_1 K_1^T / sqrt(d))
A_2 = softmax(Q_2 K_2^T / sqrt(d))
```

Çıktı:

```
DiffAttn = (A_1 - lambda * A_2) V
```

Kısıtlama, iki haritada paylaşılan herhangi bir gürültü dağılımını iptal eder. Her iki haritada 127k bağlantısız simgeler üzerinde yaklaşık aynı ağırlık varsa (herhangi bir rastgele başlangıçta geçer), bunlar iptal edilir.

`lambda`başlıkta öğrenilebilir bir skalar, parametre olarak `lambda = exp(lambda_q1 dot lambda_k1) - exp(lambda_q2 dot lambda_k2) + lambda_init`- Negatif olabilir.`lambda_init`0.8 gibi küçük bir pozitif sayıya varır.

### Bu neden eşleşir başlı gürültü iptal

Aynı sesi kaydeten iki gürültülü mikrofon düşünün. İkisi de hoparlörle ilgili arka plan gürültüsü ile birlikte alırlar. Birini diğerinden çıkarırsanız paylaşılan gürültü düşer. Ses hayatta kalır çünkü iki sinyal tamamen iptal edilmesini önleyecek kadar faz veya amplitudada farklıdır.`lambda`Bu dengeyi öğrenir.

### V1 vs V2: fark

V1 parametre sayısını baseline Transformer ile eşit tutmuştur. Baş başına iki sorgu almak için baş boyutunu yarıya düşürmüştür. Bu baş ifade gücünü ve  daha acı verici  baş başına değer önbelleğini yarıya düşürmüştür. Dekode, değer önbelleğini her adımda iki kez (softmax dal başına bir kez) yüklemek zorunda kalmıştır. Sonuç: eşleşen parametre sayısına rağmen, baseline göre yavaş dekode edilmiştir.

V2 sorgu başlıklarının sayısını ikiye katlar ve KV başlıklarını aynı tutar (yukarı projeksiyondan parametre ödünç alır). Baş boyutu başlangıç çizgisinde kalır. Kısaltmadan sonra, ek boyut, başlangıç Transformer'ın O_W projeksiyine eşleşmek için aşağıya projeksiyona geri gönderilmektedir.

1. Deşifreleme hızı başlangıç çizgisiyle eşleşir (KV önbelleği bir kez yüklenir).
2. FlashAttention değişmez olarak çalışır (herhangi bir özel çekirdek yoktur).
3. Dekodlama sırasında aritmetik yoğunluk artıyor (HBM'den yüklenen bayt başına daha fazla hesaplama).

V2 ayrıca V1'in çıkarmayı istikrarlı hale getirmek için kullandığı baş başına RMSNorm'i de kaldırır. 70B sınıfı öncesi eğitim ölçeklerinde, RMSNorm geç eğitimleri istikrarsızlaştırır. V2 onu ekstra modül olmadan eğitimden uzak tutan daha basit bir başlangıç şeması ile değiştirir.

### Ne zaman ulaşmak için

| Workload | Benefit |
|----------|---------|
| Long-context RAG (64k+) | Cleaner attention maps, fewer hallucinated citations |
| Needle-in-haystack benchmarks | Substantial accuracy lift past 32k |
| Multi-document QA | Less cross-document interference |
| Code completion at 8k | Marginal, not worth the architecture change |
| Short chat (< 4k) | Essentially indistinguishable from baseline |

4k'de gürültü zemini standart dikkat için yeterince küçüktür. 128k'de size zarar veriyor.

### 2026'daki diğer düğmelerle nasıl birleştiği

| Feature | Compatible with DIFF V2? |
|---------|------------------------|
| GQA | Yes (V2 increases Q heads, not KV heads) |
| MLA (DeepSeek) | Yes in principle, no published paper combining them |
| MoE | Yes (attention is independent of MLP block) |
| RoPE | Yes (unchanged) |
| YaRN / long-context scaling | Yes (exactly where DIFF helps most) |
| FlashAttention | Yes in V2 (was no in V1) |
| Speculative decoding | Yes (attention change is invisible to the spec-decode loop) |


> **【拓展：注意力机制的关键创新时间线】**2017 yıl Multi-Head Dikkat 2022 yılına kadar GQA(Llama 2, KV-cache azaltmak) 2024 yılına kadar MLA(DeepSeek-V2,KV prescide potential space) 2024 yılına kadar Farklı Dikkat( dikkat gürültüsünü ortadan kaldırmak)。MLA KV-cache 缩小小约10倍。


## Yapın.
```figure
differential-attention
```

## Yapın

`code/main.py`Bilinen sinyal artı gürültü yapısı ile oyuncak sorusu, gürültü-iptal oranını doğrudan ölçmenizi sağlar.

### Adım 1: Standart softmax dikkat

Stdlib matris operasyonları: listeler listesi, manuel matmul, softmax, maksimum sayı-stabilite çıkarımı ile.

```python
def softmax(row):
    m = max(row)
    exps = [math.exp(x - m) for x in row]
    s = sum(exps)
    return [e / s for e in exps]
```

### Adım 2: Q, K'yi iki yarıya ayır

V1 tarzı: baş boyutunu yarıya düşürün. V2 tarzı: baş boyutunu koruyun ve baş sayısını ikiye katlayın. Oyuncak uygulaması pedagojik açıklık için V1 kullanır  matematik aynıdır, sadece muhasebe farklıdır.

### Adım 3: iki softmax dal + çıkarma

```python
A1 = [softmax([dot(q1, k) / scale for k in K1]) for q1 in Q1]
A2 = [softmax([dot(q2, k) / scale for k in K2]) for q2 in Q2]
diff_weights = [[a1 - lam * a2 for a1, a2 in zip(r1, r2)] for r1, r2 in zip(A1, A2)]
out = [[sum(w * v[j] for w, v in zip(row, V)) for j in range(d_v)] for row in diff_weights]
```

Not: çıkış ağırlıkları negatif olabilir. Bu iyi  değer önbelleği hala imza katkıları işleme. Sonraki V projeksiyonu işaretini absorbe eder.

### 4. adım: Sesli iptal ölçümü

1024 uzunluğunda sentetik bir dizini oluşturun. Sinyal simgesini bilinen bir konuma koy, geri kalanını gürültüyle doldurun. A) sinyal pozisyonunda standart softmax dikkat ağırlığını ve b) farklı dikkat ağırlığını hesaplayın. Her bir sinyal ile gürültü oranını ölçün. DIFF dikkat, iki dalın ne kadar farklılık göstermesi için eğitildiğine bağlı olarak 3x-10x oranında daha yüksek bir sinyal-gürültü oranı üretir.

### Adım 5: V1 vs V2 parametresi muhasebe edilmesi

Bir yapılandırma verildiğinde (hidden=4096, heads=32, d_head=128), bas:

- Baseline Transformer: her boyut Q, K, V `hidden * hidden`- 4* gizli.
- DIFF V1: Her boyut için Q, K `hidden * hidden`, V boyutu `hidden * hidden`(Görünmez), başı içinden yarıya kısılmış.`lambda`parametre (O(başlar * d_başlar)).
- DIFF V2: Q boyutu `2 * hidden * hidden`, K boyutu `hidden * hidden`, V boyutu `hidden * hidden`O_W ' dan önce daha düşük bir görüntü . Aynı şey ekliyor .`lambda`Parametre.

Oyuncak , V2 için ekstra parametreler maliyetini ölçer (yaklaşık olarak `hidden * hidden`(Blok dikkat) ve yazdırırır.

## Çerçeveyi kullanın.

DIFF V2 henüz Nisan 2026 itibariyle her üretim sonuç sunucusunda gönderilmiyor, ancak vLLM ve SGLang'da entegrasyon yürütülüyor.

- Microsoft'un iç uzun bağlamlı üretim modelleri.
- Birkaç açık model eğitiminde 256k'dan fazla bağlamı hedef alan araştırma kopyaları.
- DIFF dikkatini alternatif katmanlarda kaydırıcı pencere dikkatini birleştiren hibrit mimarlıklar.

2026'da bunu elde edeceğiniz zaman:

- 64k'den fazla etkili bağlamı hedef alan yeni bir modelin sıfırdan eğitilmesi.
- Ortalama hataların değerlendirmeyi ele aldığı uzun bağlamlı bir modelin ince ayarlanması.

Sen yapmadığın zaman:

- Uzun bağlamlı ve stabil bir performansla önceden eğitilmiş yoğun bir model sunuyorsunuz.
- Sen her zaman 16 bin altındasın.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-diff-attention-integrator.md`. Bir model mimarisini, hedef bağlam uzunluğunu, halüsinasyon profilin ve eğitim bütçesini göz önünde bulundurarak, yeni bir eğitim öncesi koşuya veya LoRA ince ayarına farklı ilgiyi eklemek için bir entegrasyon planı üretir.

> 本课产 出 `outputs/skill-diff-attention-integrator.md` Önemli model yapı, hedef ve uzunluk, hayal yapılandırması ve eğitim bütçesi, yeni hazırlık çalışmalarına veya LoRA 微调 集成 planlarına yoğunlaştırılmış bir dikkat çekme yönünde farklılık yaratacaktır.

## Egzersizler.

1. Çık .`code/main.py`. Farklı dikkat için bildirilen sinyal-gürültü oranının sentetik sorguda standart softmax dikkatinden daha yüksek olduğunu kontrol edin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ Test fark farkı dikkat raporunun ses oranı, yapay sorgularda standart yumuşaklık maksimum dikkat noktasından daha yüksek.

2. 7B sınıfı modeli için parametre sayımı delta'sını baseline'den DIFF V1'e ve baseline'den DIFF V2'ye hesaplayın (hidden=4096, heads=32, d_head=128, 32 kat). Hangi bileşenlerin parametre kazandığını ve hangi bileşenlerin aynı kalıpta kaldığını gösterin.
   Çin dilinde:计算 7B 级模型(hidden=4096,heads=32,d_head=128,32 层) KİFV1 ve KİFV2'nin parametre farkı.

3. DIFF V1 makalesinin 3. bölümünü ve DIFF V2 Hugging Face blogunun 2. bölümünü okuyun.
   Çinçe çevirisi:DIFF V1 论文第3节和DIFF V2 Hugging Face 博客第2节──用两句解释为什么V1'in逐头 RMSNorm is necessary,以及为什么V2'in neden antrenman yayılmasına neden olmamasına neden olarak kaldırılabileceğini──

4. Bir ablation uygulamak:  ile farklılık dikkatini hesaplamak`lambda = 0`(temiz ilk yumuşaklık) ve `lambda = 1`(tam kâr) Sintez sorguda, sinyal-gürültü tarama boyunca nasıl değişir ölçün.`lambda`Bu sinyal-gürültüyi en üst düzeye çıkarır.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`lambda = 0`(püren ilk yumuşaklık maksimum)`lambda = 1`(tamamen azaltma) hesaplama farkı dikkat çekmek.`lambda`- Evet.

5. Oyuncakları GQA + DIFF V2'ye kadar uzatın. 8 KV başlığı ve 32 Q başlığı seçin. KV önbelleğinin boyutunun aynı (8, 32) yapılandırma ile bir temel GQA modeliyle eşleştiğini gösterin.
   Çin dilinde:将玩具模型扩展到 GQA + DIFF V2──选择 8 个 KV 头和 32 个 Q 头──展示 KV 缓存大小与相同 (8, 32) 配置的基线 GQA 模型匹配──

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Differential attention | "Two softmaxes minus each other" | Split Q, K into two halves, compute two softmax maps, subtract the second (scaled by lambda) from the first, then multiply by V | 差分注意力，两个 softmax 相减消除噪声 |
| Noise floor | "The non-zero tail of softmax" | The O(1/N) weight softmax puts on every unrelated token, which sums to O(1) across long contexts | 噪声基底，softmax 对不相关 token 的非零权重 |
| lambda | "The subtraction scale" | Per-head learnable scalar parameterized as `exp(lq1.lk1) - exp(lq2.lk2) + lambda_init`; can be negative | lambda 参数，可学习的减法缩放标量 |
| DIFF V1 | "The ICLR 2025 version" | Original Differential Transformer; halves head dim to preserve parameter count, needs custom kernel, slower decode | DIFF V1，原始差分 Transformer，需要自定义核 |
| DIFF V2 | "The January 2026 fix" | Doubles Q heads keeping KV heads; matches baseline decode speed and works with FlashAttention | DIFF V2，双倍 Q 头保持 KV 头，兼容 FlashAttention |
| Per-head RMSNorm | "The V1 stabilizer" | Extra norm V1 applied after the difference; V2 removed it to prevent late-training instability | 逐头 RMSNorm，V1 的稳定器，V2 移除 |
| Signal-to-noise ratio | "How much attention is wasted" | Ratio of weight on the true signal position to average weight on unrelated positions | 信噪比，信号位置权重与不相关位置平均权重之比 |
| Lost in the middle | "Long-context failure mode" | Empirical phenomenon where retrieval accuracy dips for documents in the middle of a long context — DIFF attention reduces this | 中间丢失现象，长上下文中间文档检索准确率下降 |
| Arithmetic intensity | "FLOPs per byte loaded" | Ratio V2 increased at decode by doubling queries per KV load; important for memory-bound decode | 算术强度，每次字节加载的 FLOPs 比 |

## Daha fazla okumak

- [Ye et al. — Differential Transformer (arXiv:2410.05258, ICLR 2025)](https://arxiv.org/abs/2410.05258) Ses iptalı teorisi ve uzun bağlamlı ablations ile orijinal makale
- [Microsoft unilm — Differential Transformer V2 (Hugging Face blog, January 2026)](https://huggingface.co/blog/microsoft/diff-attn-v2) üretim aşamasında yeniden yazılmak, baseline dekoduna eşleşmek, FlashAttention uyumlu
- [Understanding Differential Transformer Unchains Pretrained Self-Attentions (arXiv:2505.16333)](https://arxiv.org/abs/2505.16333) Kısıtlama neden önceden eğitilmiş dikkat yapısını geri kazanır teorik analiz
- [Shared DIFF Transformer (arXiv:2501.17900)](https://arxiv.org/html/2501.17900) Parametre paylaşım varianti
- [Vaswani et al. — Attention Is All You Need (arXiv:1706.03762)](https://arxiv.org/abs/1706.03762) Transformer DIFF'nin başlangıç çizgisi
- [Liu et al. — Lost in the Middle (arXiv:2307.03172)](https://arxiv.org/abs/2307.03172) DIFF dikkat hedefi uzun bağlamlı referans değerleri
