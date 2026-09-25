# Ölçekleme Kanunları

> Kaplan 2020 makalesinde: daha büyük model, daha düşük kayıp. 2022 Hoffmann makalesinde: az eğitim aldığınızı söyledi. Hesaplama iki kova  parametreler ve jetonlara ayrılır  ve bölünme açık değildir.

> **【中文解读】**Chinchilla'nın kanunları, model büyüklüğünü, veri miktarını, hesaplama miktarını ortaya koydu.

**Type:** Study | **类型:** 学习
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Eğitim hesaplamalarının C FLOP'ları olduğunda ve en iyi modeli istediğinde iki düğmeye karşı karşıya kalırsın:

> C FLOPs'in en iyi modeli öğrenmek için çalışıyorsanız, iki dönümcüğe karşı karşıya kalırsınız:

1. **How many parameters (N)?**Daha büyük model, daha büyük kapasite.
   Çeviri:**多少参数（N）？**Model daha büyük, kapasitesi daha yüksek.
2. **How many training tokens (D)?**Daha fazla veri, daha iyi kapasite kullanımı.
   Çeviri:**多少训练 token（D）？**Veriler daha fazla, kapasite daha iyi kullanılıyor.

FLOP'lar yaklaşık olarak `6 × N × D`N'yi yukarı ve aşağıya, ya da D'yi yukarı ve aşağıya itirebilirsin. Hangisi daha iyi?

> FLOPs yaklaşık olarak`6 × N × D`扩展── you can increase N 减小 D, or increase D 减小 N── hangi daha iyi?

2022'den önce, cevap "N zor it" idi. GPT-3 (2020) 175B parametreleri yaklaşık 300B jetonlarda eğitilmişti.

> 2022 yılından önce, cevap "推大 N"──GPT-3(2020) 175B 参数, yaklaşık 300B token 上訓練── oranı her parametre yaklaşık 1.7  token──Kaplan 缩放定律支持这一观点──

Hoffmann et al. (2022), Chinchilla adlı küçük bir model ailesini eğitmekle ilgili farklı bir şey buldu: Optimal oran **20 tokens per parameter**GPT-3 10 kat daha az eğitimliydi. Chinchilla (70B param, 1.4T token) her referans değerinde GPT-3 (175B, 300B token) 2.5 kat daha az sonuç maliyetinde yendi.

> Hoffmann 等人(2022) Chinchilla'nın modeli olarak adlandırılan bir grup eğitimi aldı ve farklı sonuçlar buldu:**每个参数 20 个 token** GPT-3 低估训练了10倍──Chinchilla(70B 参数,1.4T token) her基准测试上都击败了GPT-3(175B,300B token),推理成本仅为后者的2.5分之一──

2026'da Chinchilla'nın dünyası  bir önemli dönüşü ile. Llama 3 8B 15 trilyon jeton üzerinde eğitildi, bu da bir parametreden 1.875 jeton oranı. Ninety-four times past Chinchilla-optimal.

> 2026 yılı Chinchilla'nın dünyasıdır ama önemli bir dönüş vardır Llama 3 8B 15 milyar token  eğitimi kullanmıştır, oranı her parametre 1.875 token                                                                                                                                                                                                                                           

> **【中文解读】**缩放定律的核心洞察:FLOPs ≈ 6 × N × D(参数 × token 数) ;;Kaplan(2020) büyüme eğiliminde N, ancak Chinchilla(2022) kanıt en optimum oranı yaklaşık 20 token/parametr ⋅2026 yılın uygulaması daha ileri:Llama 3 8B 1,875 token/parametr antrenmanı kullanmış 远超 Chinchilla 最优, çünkü tahmin maliyeti antrenman maliyetinden daha önemlidir, aşırı antrenman küçük modelleri ve düşük dağıtım maliyeti endüstri standartı haline gelmiştir;;

> **【拓展：过度训练策略的经济逻辑】**Llama 3 8B 15T token  training(远超Chinchilla 最优的160B token), düşünce maliyeti büyük ölçüde düştü. Bu, düşünce zamanında her bir token'ın hesaplama miktarı ve parametrelerinin oranı ortadadır. 8B parametrelerinin düşünce maliyeti sadece 70B modelinin yaklaşık 1/9'idir. API 服务 gibi büyük miktarda dağıtım için, düşünce maliyetinin tasarrufu aşırı fazla eğitim maliyetini azaltır. Bu, Phi-3-miniwen 3.8B ve Q2-1.5B gibi küçük modellerin neden aşırı eğitildiğini açıklar.

## Konsepten bir şey.

![Chinchilla curves: loss vs compute at various N/D ratios](../assets/scaling-laws.svg)

### Hoffmann Yasası

Chinchilla gazetesinden kayıp şöyle:

> Chinchilla'nın makalesinden, kayıp aşağıdakileri içerir:

```
L(N, D) = A / N^α + B / D^β + E
```

- `N`= parametre (tökeltilmemiş).
  Çeviri:`N`= 参数量(非嵌入)
- `D`= eğitim simgeler.
  Çeviri:`D`= 訓練符号 数──
- `α ≈ 0.34`- Evet .`β ≈ 0.28`(kaykayla simetrik).
  Çeviri:`α ≈ 0.34`- Evet.`β ≈ 0.28`(大致对称)
- `E ≈ 1.69`, azaltabilir kayıp tavanı.
  Çeviri:`E ≈ 1.69`, yokluk sınırları vardır.
- `A ≈ 406`- Evet .`B ≈ 411`- Evet .
  Çeviri:`A ≈ 406`- Evet.`B ≈ 411`- Evet.

İki terim birbirine karşı ticaret yaparken ölçerken.`N`sabit hesaplama (C = 6ND) ile çözülür:

> 两项在扩展时相互制衡──在固定计算量 (C = 6ND) 下对`N`求导并求解:

```
N_opt ≈ 0.6 × (C/6)^0.5
D_opt ≈ 0.6 × (C/6)^0.5
D_opt / N_opt ≈ 20
```

Hesaplama-optimal: Parametre başına 20 token.

> 計算最优: Her parametre 20 个符号──

### Ne gerek var ki fazla eğitim görsün.

Chinchilla-optimal, her antrenman için antrenman kaybını en aza indirger.

> Chinchilla, her antrenmanın FLOP'un antrenman kaybını en iyi şekilde en aza indirmiştir.

Ayda bir trilyon tokeni hizmet veren bir chatbot için, sonuç toplam maliyet üzerinde egemenlik yapmaktadır. Llama'nın yaklaşımı: daha küçük, daha uzun tren. 8B'nin 15T tokenleri sonucun optimize edilmesiyle derin bir şekilde optimize edilmiştir:

>                                                                                                                                                                                                                                                               

- İsteğe bağlı GPU'lara uyar.
  Çinçe Çevirimi:适配消费级 GPU。
- Gecikme 70B Chinchilla-optimal bir bölümü.
  Çinçilla, 70B için en iyi bir kısım.
- Kalitesizlik çoğu görev için yeterince yakın.
  Çinçe Çevirimi:质量对大多数任务而言足够接近──

DeepMind'in 2024 makalesinde ("Üzer eğitim yeni en iyi şeydir") bunu resmileştirdi. İhtiyaçlı iş yükleri için, doğru oran, servis hacmine bağlı olarak parametre başına 100500 tokene yakındır.

> DeepMind 2024 yılının makalesinde "Ünce eğitim yeni en iyi" olarak bu noktayı formallaştırmıştır.

### Çıkış vs. Düzgünlük

İddia: belirli yetenekler (aritmetik, çok adımlı akıl yürütme, düşünce zinciri takip) aniden bir ölçekte "gelen"ler.

> 声称:某些能力 (算术、多步推理、思维链遵循)

Schaeffer et al. (2023) bunun bir ölçüm eseri olduğunu savundu: ortaya çıkan ölçümler, altındaki logitlerde düzgün bir gelişmeyi gizleyen kesintisiz puanlama (tam eşleşme, eşiğinde doğruluk) kullanır.

> Schaeffer 等人(2023) bu ölçümün sahte görüntüsü olduğunu düşünüyor:涌现指标使用不连续的评分(精确匹配、值准确率), hid hid hid hid hiding the smoothing improvement of bottom logits──连续指标──交叉) 显示平滑曲线──

2026'da konsensüs: Sürekli kayıplar üzerinden tahminler güvenilirdir. Benchmark sıçramaları genellikle puanlama sanatlarıdır. Sürekli ölçümlere göre bütçeleri planlayın.

> 2026 yılındaki ortak fikir: Sıralama Kayıpları ile Tahmin Etmek Güvenilirdir.

> **【中文解读】**"涌现能力" (açış) 2023 yılında büyük bir tartışmaya neden oldu. Bazı yetenekler belirli bir ölçekte aniden ortaya çıkıyor gibi görünüyor. Ancak Schaeffer 等人 bunun ölçümün sahte olduğunu kanıtladı.

> **【拓展：数据质量比数据量更重要】**2026 yılında küçültme teorisinin yeni değişimi veri kalitesi olarak görülüyor. Microsoft'un Phi serisi, dikkatle seçilmiş "yüksek kalite" tokeninin etkin hesaplama miktarını 2 kat daha fazla artırabileceği kanıtlanmıştır. Llama 3 veri dağılımının optimize edilmesi ve sentez veri artırılması ile yapılmıştır. MoE yapısalı, toplam eleman sayısını ve aktif hesaplama miktarını daha da açıklamıştır. Bu faktörler geleneksel Chinchilla eğriğini yeniden yapılandırmak için gereklidir.

### 2026'daki resim.

Ölçekleme yasaları hala geçerlidir, ama:

> 缩放定律仍然有效, ancak:

| Factor | Changed how |
|--------|-------------|
| 因素 | 变化方式 |
| Data quality | Curating "good" tokens (Phi-style) shifts curves by >2× effective compute |
| 数据质量 | 筛选"优质" token（Phi 风格）使曲线偏移超过 2 倍有效计算 |
| MoE | Total params decouple from active FLOPs; scaling laws per-active-FLOP |
| MoE | 总参数量与活跃 FLOPs 解耦；按活跃 FLOPs 的缩放定律 |
| Post-training | Some capabilities (instruction following, code) shift with SFT+RLHF more than pretraining |
| 后训练 | 某些能力（指令遵循、代码）通过 SFT+RLHF 的提升大于预训练 |
| Multimodality | Image + text tokens scale together; separate curves per modality |
| 多模态 | 图像 + 文本 token 一起扩展；每种模态有独立曲线 |
| Synthetic data | Models generate training data; effective compute can compound |
| 合成数据 | 模型生成训练数据；有效计算可复合增长 |

> **【拓展：合成数据与缩放定律的未来】**2026 yılında küçültme teorisi, veri duvarı sorununa karşı çıktı. Yüksek kaliteli insan metni verileri gelecek yıllarda tükenebilir.

Muon optimizer (Kimi Moonlight, 2024) eşleşen verilerde AdamW'ye göre ~2x etkili hesaplama kazancı gösterdi. 2026 eğitim sürümlerinin bazıları varsayılan olarak Muon kullanır.

> Muon 优化器 (Mün ışığı 2024) aynı veriler üzerinde, AdamW'ye göre yaklaşık 2 katı geçerli hesaplama artışını gösterdi. 2026 yılının bazı eğitimleri Muon'u kullanmayı tercih etti.

## Yapın.
```figure
scaling-laws
```

## Yapın

Bakın .`code/main.py`Chinchilla kaybı denklemini uygulayarak hesaplama-optimal için çözüyoruz .`(N, D)`Her bir hesaplama bütçesinin birinde.

> 参见 `code/main.py` Çincilla  kaybı denklemini gerçekleştirdik ve çok sayıda hesaplama bütçesinde en iyi hesaplama çözümünü bulduk `(N, D)`- Evet.

### Adım 1: Chinchilla kaybı

```python
def chinchilla_loss(N, D, A=406.4, B=410.7, alpha=0.34, beta=0.28, E=1.69):
    return A / N ** alpha + B / D ** beta + E
```

Çeviri`L`Bir kontur olarak `(N, D)`sabit olarak `C = 6ND`En azını bul.

> - Ben de .`L` olarak `(N, D)`Çekil, sabit`C = 6ND`En az değer bul.

### Adım 2: Bilgisayar-optimal sınır

Bilgisayar bütçeleri için `1e17`- ...`1e25`FLOPs, bul `(N, D)``6ND = C`- Rakipleri kontrol edin .`D/N ≈ 20`- Evet .

>  için `1e17`- Ne ?`1e25`FLOPs'in hesaplama bütçesi, kayıpları en aza indirgenir.`(N, D)`- Evet .`6ND = C`❖ Test oranı `D/N ≈ 20`- Evet.

### Adım 3: Üstü eğitim maliyeti

10× daha küçük bir model eğitimi için ödeyen ekstra kaybı hesaplayın (1/10'ün en iyi N, 10×'nın en iyi D).

> 計算訓練一個 10倍小模型 ((最优 N 的 1/10,最优 D 的 10倍) 付出的额外損失──報告作为交换的推理 FLOP 节约(与 N 成正比)──

### 4. adım: Gerçek modellerle karşılaştır

Bilinenleri gör .`(N, D)`GPT-3, Chinchilla, Llama 3 8B, DeepSeek-V3 (aktif paramlar) için çiftler ve tahmin edilen kayıp ile bildirilen kayıpları karşılaştırın.

> GPT-3 ∞ Chinchilla ∞ Llama 3 8B ∞ DeepSeek-V3 ∞`(N, D)`Önemli Kayıpları Rapor Kayıplarıyla karşılaştırın.

## Çerçeveyi kullanın.

Kendiniz sınır modeli eğitmek için yeterli değilsiniz ama ölçekleme yasaları size şunu söylüyor:

> Kendini eğitmek için çok fazla şansın yok. Ama kısaltma kuralları şöyle diyor:

1. **Whether your fine-tune has enough data.**Görev-özel verileriniz temel modelin parametre başına 20 tokenden aşağıysa, bir kayıp zemininde doymuşluğa sahip olmayı bekleyin.
   Çeviri:**你的微调是否有足够数据。**Eğer göreviniz belirli veriler temel model için 20 tane tokenden düşükse, bir kayıp sınırında beklenir.
2. **Whether to pick a bigger base model.**Bütün bütçenizi sonuç çıkarmaya harcıyorsanız, daha küçük, daha uzun süre eğitimli bir modeli tercih edin.
   Çeviri:**是否选择更大的基础模型。**Eğer tüm bütçeyi düşünceye harcadıyorsan, daha küçük bir model seçmeye öncelik ver.
3. **Where the returns diminish.**1000× Chinchilla-optimal'ın ötesinde, günlük kaybı değişiklikleri gürültü haline gelir.
   Çeviri:**收益递减在哪里。** Çinçilla'nın en iyi 1000'den sonra, sayı kaybı değişimleri gürültü haline gelir.

**The research trajectory in 2026:**

> **2026 年的研究方向：**

- **Data-constrained regime.**Web'de sınırlı sayıda yüksek kaliteli token bulunmaktadır (filtreden sonra yaklaşık 5 10 trilyon İngilizce). Sınır öncesi eğitim bu tavanın yaklaştığını gösteriyor. Sintez veriler, çok dilli, multimodal ve RLHF ölçekli ince ayarlamalar bir sonraki kaldıraçlardır.
  Çeviri:**数据受限时代。**网络上高质量代币 数量有限 ((过后约5-10亿亿英语) ⋅前沿预训练正在接近这个上限──合成数据、多语言、多模态和RLHF 缩放的微调是下一个杆──
- **Compute-multiplier tricks.**Muon optimizer, MoE, daha iyi veri kurasyonu  her biri asimptote değil mutlak sabitleri değiştirir.
  Çeviri:**计算倍增技巧。**Muon 优化器、MoE、更好的数据策展各自变化绝对常数,而不是渐近线──
- **Scaling laws for RL.**Açık soru. İlk kanıtlar RL örneklerinde güç yasasını gösteriyor ama eğitim öncesi olanlardan çok farklı bir gösterge ile.
  Çeviri:**RL 的缩放定律。**开放问题──早期 deliller RL 样本 律关系有意的,但指数与预训大不相同──

## İndirin . Ürünler .

Bakın .`outputs/skill-training-budget-estimator.md`- Yetenek seçimi .`(N, D, hours, GPU)`Yeni bir eğitim süreci için hesaplama bütçesi, dağıtım kısıtlamaları ve hedef kaybı göz önüne alındı.

> 参见 `outputs/skill-training-budget-estimator.md` Bu beceri 計算予算 部署束と目標損失, yeni eğitim için çalıştırma seçimi `(N, D, hours, GPU)`- Evet.

## Egzersizler.

1. **Easy.**Çık .`code/main.py`- Çincilla-optimal basın .`(N, D)`Bilgisayar bütçeleri için `1e20`- Evet .`1e22`- Evet .`1e24`Gerçek model masasına kıyasla.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ 打印计算预算为`1e20`- Evet.`1e22`- Evet.`1e24`Çincilla'nın en iyisi`(N, D)`                                                                                                                                                                                                                                                              
2. **Medium.**Hoffmann'ın hesaplama işlev kaybı eğrisini uygulayın.`log10(C)`Bilgisayar-optimal sınır için.`>10^28`FLOPs, önümüzdeki 0,1'lik çapraz entropi azaltımı için.
   Çinçe Çevirimi: Hoffmann'ın başarısı 損失-計算量曲線──绘制計算最优前沿的損失 vs 計算最优前沿的損失`log10(C)`❖ belirlemek ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒  ⇒ ⇒ ⇒      ⇒ ⇒    ⇒ ⇒     ⇒      ⇒     ⇒                  ⇒                                                                                                                                                                           `>10^28`FLOPs 才能使交叉再降低 0.1──
3. **Hard.**Aynı veri kümesi üzerinde eğitilen 5 küçük modelde (100K'den 10M'ye kadar) kendi ölçekleme yasasını uygulayın.`α`ve `E`- Eksponentlerin yayınlananlarla ne kadar uyumlu?
   Çinçe Çevirimi: 5 个小模型的训练在同一数据集上 (short five models) 100K~10M 参数) 并适应自己的缩放定律──估算`α`和 `E`◊ İndeksi ve yayın değerleri nasıl eşleşir?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Parameters (N) | "Model size" | Non-embedding weight count; determines capacity. |
| 参数 (N) | "模型大小" | 非嵌入权重数量；决定容量。 |
| Tokens (D) | "Training data" | Number of training tokens seen; determines how well the parameters get used. |
| Token (D) | "训练数据" | 看到的训练 token 数量；决定参数被利用的程度。 |
| Compute (C) | "FLOPs spent" | Approximately `6 × N × D` for a standard transformer. |
| 计算量 (C) | "FLOPs 花费" | 标准 Transformer 约为 `6 × N × D`。 |
| Chinchilla-optimal | "D/N ≈ 20" | Ratio that minimizes loss per FLOP of pretraining. |
| Chinchilla 最优 | "D/N ≈ 20" | 最小化每个预训练 FLOP 损失的比例。 |
| Over-training | "Past Chinchilla" | Spend extra training FLOPs to save inference FLOPs; D/N >> 20. |
| 过度训练 | "超过 Chinchilla" | 额外训练 FLOPs 以节省推理 FLOPs；D/N >> 20。 |
| Irreducible loss | "The floor" | The `E` term in the scaling law; the entropy of the data itself. |
| 不可约损失 | "底线" | 缩放定律中的 `E` 项；数据本身的熵。 |
| Emergent capability | "Sudden jumps at scale" | Often a scorer artifact; continuous loss is smooth. |
| 涌现能力 | "规模上的突然跳变" | 通常是评分伪影；连续损失是平滑的。 |
| Effective compute | "Training-efficiency multiplier" | Better data / optimizer / architecture multiplies how far a FLOP goes. |
| 有效计算 | "训练效率倍增器" | 更好的数据/优化器/架构使每个 FLOP 走得更远。 |

## Daha fazla okumak

- [Kaplan et al. (2020). Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361) ilk ölçekleme hukuku makalesi; yetersiz eğitimli.
  Çinçe Çevirimiçi:第一篇缩放定律论文;低估训练了──
- [Hoffmann et al. (2022). Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)- Chinchilla.
  Çinceşila 论文。
- [Schaeffer et al. (2023). Are Emergent Abilities of Large Language Models a Mirage?](https://arxiv.org/abs/2304.15004) ölçüm eseri olarak ortaya çıkış.
  Çinçe Çevirisi: 涌现能力是否是幻觉的论文──
- [Sardana, Frankle (2024). Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws](https://arxiv.org/abs/2401.00448) Llama'nın aşırı eğitimi neden iş yükü için doğru.
  Çinçe Çevirisi: Neden Llama'nın iş yükü üzerinde aşırı eğitim doğru?
- [Jordan et al. (2024). Muon: An optimizer for hidden layers in neural networks](https://kellerjordan.github.io/posts/muon/)2× hesaplama çarpıcısı.
  Çinçe Çevirim:Muon 优化器,2 倍计算倍增器。
