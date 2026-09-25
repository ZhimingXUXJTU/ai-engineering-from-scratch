# Değerlendirme  FID, CLIP puanı, insan tercihleri   değerlendirme göstergesi  FID 、 CLIP puanı ve insan tercihleri

> Her jeneratif model lider tablosu, insan tercih alanından FID, CLIP puanı ve kazanım oranını belirtir. Her sayı, belirlenmiş bir araştırmacı oynayabilecek bir başarısızlık moduna sahiptir.

> **【中文解读】**Her bir üretim modeli sıralaması FID'yi (Fréchet Inception Distance) ✓ CLIP Notı ve insan tercihleri kazanım oranını belirtir.

> **【拓展：FID 的局限性】**FID, görüntü üretimi ile gerçek görüntülerin dağılım mesafesini ölçer, ancak seçkin bir şekilde üretilen yüksek oranlı örnekler gibi optimize edilebilir. İnsan tercihlerini değerlendirmek Chatbot Arena modeli gibi daha güvenilir ama daha pahalı bir alternatif olarak kullanılabilir.

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 01 (Taxonomy / 分类), Phase 2 · 04 (Evaluation Metrics / 评估指标) | **前置知识:** 阶段 8 · 01（分类），阶段 2 · 04（评估指标）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Sorunlar. Sorunlar.

Bir jeneratif model * örnek kalitesi * ve * koşullama yapısı * üzerine değerlendirilir. Her ikisi de kapalı bir ölçümüne sahip değildir. Modeliniz 10.000 görüntüyi göstermelidir; bir şey onlara sayı ataması gerekir; model aileleri, çözünürlükler, mimarlıklar boyunca sayılara güvenmeniz gerekir. 2014-2026 eldiveninden üç ölçüm sağ kaldı:

> 生成模型以*样本质量*和*条件遵循度*评判──都没有闭式度量──你的模型必须染 10000张图像;必须有东西给它们打分──三个指标经历了2014-2026的考试:

- **FID (Fréchet Inception Distance).**Bir başlangıç ağının özellik alanında iki dağıtım  gerçek ve üretilen  arasındaki mesafe.
  **FID。**Gerçek ve oluşum, başlangıçta 网络特征空间中的距离──越低越好──
- **CLIP score.**Yaratılan bir görüntüde CLIP-resim yerleştirme ile bir istekle CLIP-metin yerleştirme arasında benzerlik. Daha yüksek daha iyidir.
  **CLIP Score。**Çizgi resim ve metin tesisi için CLIP 嵌入余弦相似度──越高越好──
- **Human preference.**İki modelin aynı sorguya karşı karşıya kalmasını sağlayın, insanların (veya GPT-4 sınıfı bir model) daha iyi olanı seçmesini sağlayın, bir Elo puanına toplamlayın.
  **人类偏好。**两个模型头对头对比,人类或GPT-4 级模型选择更好,聚合为 Elo 分数──

Ayrıca şunları göreceksiniz: IS (başlangıç puanı, büyük ölçüde emekli), KID, CMMD, ImageReward, PickScore, HPSv2, MJHQ-30k. Her biri önceki başarısızlıklardan birinde düzeltir.

> Siz de göreceksiniz: IS(已基本退役) 、KID、CMMD、ImageReward、PickScore、HPSv2 等── hepsi önceki birimin bazı eksikliklerini düzeltti──

> **【中文解读】**生成模型評価の三大指標:(1) FID in Inception 网络特征空间で生成分布と真分布の距離を測定する,越低越好;(2) CLIP Score生成图像と文本提示の语义匹配,越高越好;(3) İnsan tercihleri iki modelden daha iyi seçilir, bir araya gelmek Elo 分数── her bir göstergeye bilinen bir hata vardır, kombinasyon kullanımı daha güvenilir。

> **【拓展：生成模型评估的"刷榜"问题】**FID'nin seçkin bir şekilde yüksek sayıda örnek oluşturulması, düzenlenmesi, başlangıç, modelin özellik katmanı veya referans dağılımına uygun olması için de optimize edilebilir. CLIP Skoru ayrıca bazı kavramlara karşı daha duyarlı bir önyargı vardır.

## Konsepten bir şey.

![FID, CLIP, and preference: three axes, different failure modes](../assets/evaluation.svg)

### FID  örnek kalitesi  FID  örnek kalitesi

Heusel et al. (2017). Adımlar:

> Heusel 等人(2017)。步骤:

1. N gerçek görüntüler ve N oluşturulan görüntüler için Inception-v3 özelliklerini (2048-D) çıkarın.
   N 张真像和 N 张生成图像提取 Başlangıç-v3 Özellikleri(2048 维) 』
2. Her havuz için bir Gaussian ayarlayın: hesap ortalaması`μ_r, μ_g`ve kovarians `Σ_r, Σ_g`- Evet .
   Her bir akciğer için: hesaplanan ortalama değer`μ_r, μ_g`&amp; quot; Önemli bir fark &amp; quot;`Σ_r, Σ_g`- Evet.
3. FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`- Evet .
   FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`- Evet.

Anlatma: Özellik alanındaki iki çok değişken Gaussyan arasındaki Fréchet mesafe.

> 解读: 特征空间中两个多元高斯分布之间的 Fréchet 距离──越低 = 分布越相似──

Başarısızlık modları:

> 失败模式:

- **Biased on small N.**FID, özellik dağılımının ortalaması  küçük N'nin hafifçe ölçülmesi, yanlış düşük FID verir.
  FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: FID: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid: Fid:
- **Inception-dependent.**ImageNet'ten uzak alanlar (yüzler, sanat, metin görüntüler) anlamsız FID üretir.
  ImageNet'in alanından uzaklaşmak için, FID'nin anlamsız bir şekilde oluşması gerekir.
- **Gaming.**Başlangıç öncesiye fazla uyum sağlayarak görsel kalitede iyileşme olmadan düşük FID sağlar.
  刷分: Inception'e göre daha düşük FID'yi sağlayabilir ama görüntü kalitesi yükseltilmedi.

### CLIP puanı  hızlı takip  CLIP puanı  hızlı takip 

Radford et al. (2021). Yaratılan bir görüntü için + prompt:

> Radford 等人(2021) ・・・ için oluşturmak için görüntü + prompt:

```
clip_score = cos_sim( CLIP_image(x_gen), CLIP_text(prompt) )
```

30k'da üretilen görüntülerin ortalaması → modeller arasında karşılaştırılabilir bir ölçek.

> 30k 张生成图像的平均求 → 一个模型间比较的标量──

Başarısızlık modları:

> 失败模式:

- **CLIP's own blind spots.**CLIP'in zayıf bir kompozisyon mantığı vardır ("mavi bir kürede kırmızı bir küp" genellikle başarısız olur).
  CLIP 自身的盲点:CLIP 组合推理能力弱 (Clips'in kendi kör noktası:CLIP 组合推理能力弱 (Clips'in kendi kör noktası:CLIP 组合推理能力弱)
- **Short prompt bias.**Kısa çağrılar, daha fazla CLIP görüntü eşleşmesini sağlarken, daha uzun çağrılar mekanik olarak daha düşük CLIP puanlara sahiptir.
  短 prompt 偏差:短 prompt 在野外有更多 CLIP-image 匹配──长 prompt 在 CLIP Score 上机械性地更低──
- **Prompt gaming.**"Yüksek kalite, 4k, şaheser" içeren istek, görüntü-metin bağlanmasını geliştirmeden CLIP puanını yükseltir.
  Çabuk 刷分: 在 prompt 中加入 "yüksek kalite, 4k, şaheser" 能升高 CLIP Score而不改善图文绑定──

CMMD (Jayasumana et al., 2024) bunlardan bazılarını düzeltir: Başlangıç yerine CLIP özelliklerini kullanır, Fréchet yerine maksimum ortalama çelişki.

> CMMD(Jayasumana 等人 2024) bunlardan bazı sorunları düzeltti: CLIP özelliklerini başlangıç olarak kullanmak, MMD'yi kullanmak (maksimum ortalama fark) yerine Frechet 距离──更善于检测细微的质量差异──

### İnsan tercihleri  yeryüzü gerçeği  İnsan tercihleri  Yeryüzü gerçek değeri

Bir dizi ipucu seçin. Model A ve model B ile oluşturun. İnsanlara çiftler gösterin (veya güçlü bir LLM yargıç).

> 選一批提示──用模型 A 和模型 B 生成──把成对结果展示给人类────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

- **PartiPrompts (Google)**: 1600 farklı sorgu, 12 kategori.
  **PartiPrompts（Google）**: 1600 个多样化 prompt,12 个类别──
- **HPSv2**: 107k insan notları, geniş çapta otomatik temsilci olarak kullanılır.
  **HPSv2**10.70.000 insan etiketleri, geniş çapta otomatik temsilci olarak kullanılır.
- **ImageReward**: 137k çabuk görüntü tercih çiftleri, MIT lisanslı.
  **ImageReward**13.7 bin dolarlık bir görüntü tercihinden dolayı.
- **PickScore**Bu nedenle, bu programın en iyi yönleri,
  **PickScore**- Bu yüzden... - ...bir tane daha.
- **Chatbot-Arena-style image arenas**- Evet .https://imagearena.ai/Ve diğerleri.
  **Chatbot-Arena 风格的图像竞技场**- ...https://imagearena.ai/- Evet.

Başarısızlık modları:

> 失败模式:

- **Judge variance.**Uzmanlar olmayanların tercihleri uzmanlardan farklıdır.
  评判者方差:非专家和专家有不同的偏好──两者都用──
- **Prompt distribution.**Bir aile için iyi bir tavsiye.
  Hızlı dağılım:精心挑选的快速会偏向某一家族──务必记录──
- **LLM-judge reward hacking.**GPT-4 yargıçı güzel ama yanlış sonuçlarla kandırılır.
  LLM 评判被刷分:GPT-4 评判会被"好看但错"的输出欺骗──与人类三角验证──

## Birlikte kullanın.

Üretim değerlendirme raporu şunları içermelidir:

> Bir üretim sınıfı değerlendirme raporu şunları içermelidir:

1. 10-30k örnekle gerçek bir dağıtım ( örnek kalitesi) karşılaştırıldığında FID.
   10-30k örnek üzerinde gerçek dağılımı geride kalan FID (sampel kalitesi) ◊
2. Aynı örnekler karşısında CLIP puanı / CMMD (aitlik).
   Aynı şekilde kendi isteklerine göre CLIP Score / CMMD
3. Kör bir arenada önceki modelle karşı kazanç oranı (toplam tercih).
   Öte yandan, bu durumla ilgili olarak,
4. Başarısızlık modunun analizi: Bilinen sorunlar için işaretlenen 50 rastgele örneklenmiş çıkış (el anatomisi, metin gösterimi, tutarlı nesne sayısı).
   失败模式分析:随机采样 50 输出,标记已知问题(手部解剖、文字染、对象计数一致性)

Her tek metrik yalan. Üç doğrulucu metrik + kaliteli inceleme bir iddiadır.

> 任何单一指标都是谎言──三个相互印证的指标 + 定性审查才算一个声明──

## Yapın.
```figure
gx-fid-distributions
```

## Yapın

`code/main.py`FID, CLIP skor benzeri ve Elo toplamını sentetik "karakter vektörleri" üzerinde uyguluyor.

> `code/main.py`Bu nedenle, "Clear Strength" ile birlikte, FID, CLIP Score, Elo ve Cluster'ı gerçekleştirmek için 4 维向量 kullanıyoruz.

- Küçük bir N'de ve büyük bir N'de FID hesaplama  önyargısı.
  Küçük N 和大 N 上 的 FID 計算偏差──
- "CLIP puanı" özellik havuzları arasındaki kozine benzerlik olarak.
  作为特征池之间余弦相似度的"CLIP Score" (BİZİN)
- Sintez tercih akışından Elo güncelleme kuralı.
  SYSTETÖ ÖNEMİSİ'nin Elo 更新规则──

### Adım 1: Dört satırda FID.

```python
def fid(real_features, gen_features):
    mu_r, cov_r = mean_and_cov(real_features)
    mu_g, cov_g = mean_and_cov(gen_features)
    mean_diff = sum((a - b) ** 2 for a, b in zip(mu_r, mu_g))
    trace_term = trace(cov_r) + trace(cov_g) - 2 * sqrt_cov_product(cov_r, cov_g)
    return mean_diff + trace_term
```

> Dört satır FID: gerçek ve üretilen özelliklere ayrılığı hesaplama ortalama değer ve eşleme farkı, yeniden hesaplama ortalama değer farkı karşın eşleme farkı.

### Adım 2: CLIP tarzındaki kozine benzerliği

```python
def clip_like(image_feat, text_feat):
    dot = sum(a * b for a, b in zip(image_feat, text_feat))
    norm = math.sqrt(dot_self(image_feat) * dot_self(text_feat))
    return dot / max(norm, 1e-8)
```

> CLIP 风格余弦相似度:点积除以两个向量范数乘积,加epsilon 防止除零──

### Adım 3: Elo toplama

```python
def elo_update(r_a, r_b, winner, k=32):
    expected_a = 1 / (1 + 10 ** ((r_b - r_a) / 400))
    actual_a = 1.0 if winner == "a" else 0.0
    r_a_new = r_a + k * (actual_a - expected_a)
    r_b_new = r_b - k * (actual_a - expected_a)
    return r_a_new, r_b_new
```

> Elo 更新: K=32 is is is is is international chess standard.

## Tuzaklar.

- **FID at N=1000.**Heuristik, N=10k'de güvenilir değil.
  N=1000 时的FID:在N<10k 时不可靠──报告低 N FID 的论文在刷分──
- **Comparing FID across resolutions.**Başlangıç'ın 299×299 boyutları özellik dağılımını değiştirir.
  跨分辨率比较 FID:Inception'ın 299×299 缩放会改变特征分布──只在匹配分辨率下比较──
- **Reporting one seed.**En az 3 tane tohum çalıştırın.
  Sadece bir tohum rapor edin: en az 3 tohum çalıştırın.
- **CLIP score inflation via negative prompts.**Bazı boru hattları, işaretleme cihazını fazla ayarlayarak CLIP'i artırıyor.
  通过负向快速 抬高 CLIP Skor:有些流水线通过过拟合快速 抬高 CLIP──检查视觉和──
- **Elo bias from prompt overlap.**Eğer her iki model de eğitim sırasında bir referans işaretini gördüyse Elo anlamsızdır.
  Hızlı ağırlıklı 偏差: Eğer iki model eğitim sırasında görüldüğünde基准 prompt,Elo 无意义──使用留出的 prompt 集──
- **Human eval paid-crowd skew.**Verimli, MTurk notatörleri genç / teknoloji dostu eğilimi.
  工评付费众包偏差:Proplific、MTurk 标注者偏年轻 / 偏技术友好──混合招募的艺术/设计专家──

## Çerçeveyi kullanın.

2026 yılında üretim değerlendirme protokolü:

> 2026 yılındaki üretim sınıfı değerlendirme anlaşması:

| Pillar / 支柱 | Minimum / 最低要求 | Recommended / 推荐 |
|--------|---------|-------------|
| Sample quality / 样本质量 | FID on 10k vs held-out real | + CMMD on 5k + FID on subset per category |
| Prompt adherence / Prompt 遵循 | CLIP score on 30k | + HPSv2 + ImageReward + VQA-style question answering |
| Preference / 偏好 | 200 blinded pairs vs baseline | + 2000 paired human + LLM-judge + Chatbot Arena |
| Failure analysis / 失败分析 | 50 hand-flagged | 500 hand-flagged + automated safety classifier |

Tek rapordaki dört sütun = iddia.

> Dört sütun tamamı bir açıklama.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-eval-report.md`. Skill yeni bir model kontrol noktasını + temel çizgiyi alır ve tam bir değerlendirme planını çıkarır: örnek boyutları, ölçümler, başarısızlık modundaki araştırmalar, onay kriterleri.

> 保存为 `outputs/skill-eval-report.md`◊ Bu beceri yeni bir model kontrol noktasını + 基线, tam bir değerlendirme planı: sample number, indicator, failure mode, signature standardı:

## Egzersizler.

1. **Easy.**Çık .`code/main.py`Aynı sentetik dağılımlarda N=100 vs N=1000'de FID'yi karşılaştırın.
2. **Medium.**CMMD'yi sentetik CLIP tarzı özelliklerden uygulayın (formül için Jayasumana et al., 2024'e bakın).
3. **Hard.**HPSv2 ayarını tekrarlayın: Pick-a-Pic alt kümesinden 1000 görüntü-sürekli çift alın, küçük bir CLIP tabanlı puanlayıcıyı tercihlere göre ince ayarlayın ve uyumunu bir tutulan kümle ile ölçün.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| FID | "Fréchet Inception Distance" | Fréchet distance of Gaussian fits to real vs gen Inception features. |
| CLIP score | "Text-image similarity" | Cosine similarity between CLIP image and text embeddings. |
| CMMD | "FID's replacement" | CLIP-feature MMD; less biased, no Gaussian assumption. |
| IS | "Inception score" | Exp KL(p(y|x) || p(y)); correlates poorly on modern models, retired. |
| HPSv2 / ImageReward / PickScore | "Learned preference proxies" | Small models trained on human preferences; used as automatic judges. |
| Elo | "Chess rating" | Bradley-Terry aggregation of pairwise wins. |
| PartiPrompts | "The benchmark prompt set" | 1,600 Google-curated prompts across 12 categories. |
| FD-DINO | "Self-sup replacement" | FD using DINOv2 features; better for out-of-ImageNet domains. |

## Üretim Not: değerlendirme de bir sonuç iş yüküdür

10k örnekler üzerinde FID çalıştırmak 10k görüntü üretmek anlamına gelir. Tek L4'te 10242'de 50 adımlı SDXL tabanı için, bu ~11 saat tek istek sonucu anlamına gelir. Değerlendirme bütçeleri gerçek, ve çerçeve tam olarak çevrimdışı sonucu senaryoya (maksimum çıkışlılık, TTFT'yi ihmal et):

- **Batch hard, forget latency.**Offline eval = hafızaya uygun en büyük boyutta statik seri. `pipe(...).images`- Evet .`num_images_per_prompt=8`80GB H100'de, tek istekten 4-6 kat daha hızlı bir duvar saati kullanılır.
- **Cache the real features.**Gerçek referans kümesi üzerinde başlatma (FID) veya CLIP (CLIP-score, CMMD) özelliği çıkarımı *once* olarak çalıştırılır.`.npz`- Değerlendirme başına yeniden hesaplama.

CI / regresyon kapıları için: PR başına 500 örnek alt kümesi üzerinde FID + CLIP puanı çalıştırın (~ 30 dakika); gecelik 10k FID + HPSv2 + Elo çalıştırın.

## Daha fazla okumak

- [Heusel et al. (2017). GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium (FID)](https://arxiv.org/abs/1706.08500)- FID kağıdı.
- [Jayasumana et al. (2024). Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603) CMMD.
- [Radford et al. (2021). Learning Transferable Visual Models from Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020)- Klip.
- [Wu et al. (2023). HPSv2: A Comprehensive Human Preference Score](https://arxiv.org/abs/2306.09341) HPSv2.
- [Xu et al. (2023). ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation](https://arxiv.org/abs/2304.05977) ImageReward.
- [Yu et al. (2023). Scaling Autoregressive Models for Content-Rich Text-to-Image Generation (Parti + PartiPrompts)](https://arxiv.org/abs/2206.10789)PartiPrompts.
- [Stein et al. (2023). Exposing flaws of generative model evaluation metrics](https://arxiv.org/abs/2306.04675) Başarısız mod anket.
