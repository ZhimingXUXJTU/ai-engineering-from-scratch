# Farklı Gizlilik Yüksek Lisans için Farklı Gizlilik Yüksek Lisans

> DP-SGD standart  gürültü enjeksiyonu gradient güncellemeleri olarak kalır. Hesaplama, bellek ve kullanım alanındaki genel maliyetler önemli; parametre-efikas DP ince ayarlama (LoRA + DP-SGD) ortak 2025 yapılandırması (ACM 2025). İki kanıt kümesi gerginlik içinde: Kanarlı üyelik sonucu (Duan et al., 2024) dil modellerine karşı sınırlı başarı raporları; eğitim verileri çıkarma (Carlini et al., 2021; Nasr et al., 2025) önemli kelimel hatıralama geri kazanır. Karar (arXiv:2503.06808, Mart 2025): fark ölçülmüş olan  yerleştirilen kanaryalarla "en çıkarılabilir" veriler arasında. Yeni kanary tasarımları, gölge modelleri olmadan kayıp tabanlı MIA'yı mümkün kılar ve gerçekli DP garantileri ile gerçek verilere dayanan bir LLM'nin ilk önemsiz DP denetimini sağlar. Alternatifler: PMixED (arXiv:2403.15638)  sonraki token dağıtımları konusunda uzmanların karışımı yoluyla çıkarma zamanında özel tahmin; DP sentetik veri üretimi (Google Araştırma 2024). Yeni ortaya çıkan saldırı: LLM Feedback  güven puanı sızdırısı yoluyla Farklı Gizlilik Değişimi.

> **【中文解读】**Bu bölüm LLM'nin farkı gizlilik hakkında bilgi verdi. Bu bölümde, eğitim ve düşünce içinde kullanıcı verileri gizliliğini korumak için matematiksel yöntemler ele alındı. DP-SGD standart yöntemlerdir.

> **【拓展：MIA vs 训练数据提取 → 衡量差距】**2024-2025 yılları için iki kanıt çizgi oluşturur Zhang力: 金丝雀 MIA(Duan 等人 2024) rapor dil modelinin başarısı sınırlı; training data提取(Carlini 2021, Nasr 等人 2025) yeniden büyük miktarda kelimelerle hatırı yeniden kazanmak.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, DP-SGD noise-injection and ε-δ accountant demonstration) | **语言:** Python（标准库，DP-SGD 噪声注入和 ε-δ 计数器演示）
**Prerequisites:** Phase 01 · 09 (information theory), Phase 10 · 01 (large-model training) | **前置知识:** Phase 01 · 09 (信息论), Phase 10 · 01 (大模型训练)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Öğrenci: Önemli bir eğitim programı yapın.
>  **【类比】**DP = "data hid身衣"──DP-SGD 梯度注入噪音,单个样本不影响整体训练→形式化数学证明无法从模型反推是否某条数据在训练集──代价:计算/内存/效用都明显下降──LoRA+DP-SGD 是 2025 实用配置((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
> 🤔 困境: 金丝雀式 MIA 攻击失败 vs 训练数据提取成功差在测什么(插入 vs 最易提取) ・・・2025.3 新金丝雀设计首次对真数据 LLM做非凡 DP 审计──

## Öğrenme hedefleri

- (epsilon, delta) -farklı gizlilik tanımlayın ve DP-SGD tarifini belirtin.
- 2024-2025 gerginliğini açıklayın: Kanarya MIA vs. Eğitim- veri çıkarımı farklı resimler verir.
- PMixED'i ve neden sonucu çıkarma zamanı özel tahmininin DP eğitimi için bir alternatif olduğunu açıklayın.
- LLM Feedback saldırısı yoluyla Farklı Gizlilik Değişimi'ni açıklayın.

> 定义 (epsilon, delta) -差分隐私并说明 DP-SGD 方法──解释 2024-2025 年张力:金丝雀 MIA vs 训练数据提取给出不同图景──描述 PMixED 及为什么推理时私有预测是 DP 训练的替代──描述通过 LLM 反的差分隐私逆转攻击──

## Sorun . Sorun .

LLM'ler hafıza. Carlini et al. 2021 üretim dil modellerinin talep üzerine sözde eğitim metnini yeniden ürettiğini gösterdi. DP resmi savunmadır: eğitim, böylece çıkışın herhangi bir eğitim örneğine karşı hassas olmadığını kanıtlar. 2024-2025 kanıtları DP-SGD'nin gerekli olduğunu gösterir, ancak dağıtılan ε değerleri tehdit modeline eşleşmeyebilir.

> LLM 会记忆──Carlini 等人 2021 yıl gösterim üretim dil modeli ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒  ⇒   ⇒  ⇒   ⇒ ⇒ ⇒                                                                                                                             

## Konsep kavramı.

> **【中文解读】**(epsilon, delta) -差分隐私定义:随机算法 M 是 (epsilon, delta) -DP 的, eğer S:P(M(D) 'de herhangi iki fazeden farklı bir örnek için bir dataküt ve herhangi bir olay varsa S:P(M(D) <= e^epsilon * P(M(D') 'de S) + delta。 açıklama:输出分布足够接近(由 epsilon 参数化), herhangi bir tek bireyin katkıları olasılıkla delta dışında güvenilir bir şekilde tahmin edilemez。

### (ε, δ) - Farklı gizlilik

Bir rastgele algoritma M (ε, δ) -DP eğer bir örnekte ve herhangi bir olayda farklı olan iki veri kümesi için S:
S) <= e^ε * P(M(D') S) + δ.

> 随机算法 M 是 (ε, δ) -DP 的, eğer S:P(M(D) S'de herhangi iki fazeden farklı bir örnek için S:P(M(D) <= e^ε * P(M(D') S) + δ。

Anlatma: çıkış dağılımı, herhangi bir bireyin katkılarının, δ olasılığı hariç, güvenilir bir şekilde çıkarılamayacağı kadar yakın ( ε ile parametrelidir).

> 解释:输出分布足够接近 (由 ε 参数化) ), herhangi bir bireyin katkıları, olasılıkla δ ∈ dışında güvenilir olarak tahmin edilemez.

### DP-SGD

Abadi et al. 2016. Standart tarif:
1. Küçük bir partiye örnek ver.
2. Örnek başına gradient hesaplayın.
3. Örnek başına her bir gradient C e bir eşiğine çıkar.
4. Kısaltılan gradientleri toplamlayıp std σ * C ile Gaussian gürültüsü ekleyin.
5. Parametreyi güncellemek için gürültülü miktarı kullanın.

> DP-SGD 標準方法:1. 采样小批次──2. 計算逐例梯度──3. 剪切每梯度到值 C──4. 求和剪切后的梯度并添加高的噪音──5. 使用噪音和更新参数────

Gizlilik maliyetini bir muhasebeci (Moments Muhasebeci, Rényi DP muhasebeci) takip eder. LLM literatüründe bildirilen ε değerleri tehdit modeli, veri hassasiyeti ve kullanım hedefi ile çok farklıdır; evrensel olarak "güvenli" varsayılan ε yoktur. Yayınlanan örnekler bazı LLM eğitim ayarlarında yaklaşık ε ≈ 110'u kapsar, ancak bunlar örnekler  önerilmeyen varsayımlardır. Düşük ε genellikle daha fazla gürültü gerektirir ve kullanım kaybını artırabilir.

> Gizlilik maliyeti, hesaplayıcı tarafından takip edilmektedir.

### LoRA + DP-SGD

Sınır modelinin tam DP-SGD yasaklayıcıdır. LoRA (Hu et al. 2022) gradient güncellemelerini küçük bir adaptöre sınırlıyor ve örneğe göre gradient depolamasını azaltıyor. LoRA + DP-SGD ortak 2025 yapılandırmasıdır. DP garantileri adaptöre uygulanır; temel model sabit tutulur.

> Tümçeve DP-SGD                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

### 2024-2025 yıllarındaki gerginlik

İki kanıt:

> 两条证据线:

- **Canary MIA (Duan et al. 2024).**Eğitim verilerine benzersiz kanaryalar ekle, üyelik-sırh saldırganının onları tanımlayabileceklerini ölç. Dil modellerinde sınırlı başarı raporları. MIA zor olduğunu önerir.
- **Training-data extraction (Carlini 2021, Nasr et al. 2025).**Model'i bir önbellekle gösterin; eğitimden sözlü metni geri aldığını ölçün.

> Kimse Nere MIA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

Mart 2025 çözümü (arXiv:2503.06808): iki ölçüm farklı şeyler. MIA, eklenen kanaryalarda "e örneği D'de mi?" sorusunu sorar. Çöpleme "D'den neyi geri alabilirim?" sorusunu sorar. "En çıkarılabilir" örnek gizlilik için önemli olan şeydir; kanaryalar bunu düşük raporlar çünkü çıkarılabilir olmak için optimize edilmemişlerdir.

> 2025 Mart ayında çözümü: İki farklı şey ölçülüyor. MIA "Örneğin e içinde mi?", "D'nin neyi geri alabilirim?" sorusunu soruyor.

Yeni kanarya tasarımları, gölge modelleri olmayan kayıp tabanlı MIA, gerçekli bir DP garanti ile gerçek veriler üzerine bir LLM'nin ilk önemsiz DP denetimi.

> Yeni KINÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇ

> **【拓展：PMixED → 推理时隐私】**PMixED(arXiv:2403.15638) tarafından önerilen bir projeyi sunar: Bir sonraki belirtilerdeki uzmanlar karışıklıklarda, her uzman bir parça eğitim verisini görür, DP'yi gerçekleştirmek için bir araya getirir. DP'yi tamamen önler. DP'yi tamamen önler. DP'yi tamamen önler.

### DP eğitimi alternatifleri

- **PMixED (arXiv:2403.15638).**Sonraki belirti dağıtımları konusunda uzmanların karışımı; her uzman eğitim verilerinin bir parçalarını görür; toplama DP için gürültü ekler. DP eğitimi tamamen kaçınılmaktadır.
- **DP synthetic data generation (Google Research 2024).**LoRA-fin-tune DP-SGD, örnek sentetik veriler, sentetik verilere bir aşağıdaki sınıflandırıcı eğit.

Her ikisi de farklı bir tehdit modeli masrafıyla tam DP eğitimi yararlı maliyetini önler.

> **【中文解读】**差分隐私逆转攻击(2025): DP 训练模型的置信分数作为预言机重新识别个体──即使输出不泄露,置信分布也可能泄露──防御:不暴露置信度,或在暴露前截断/量化──这是 (epsilon, delta) -DP 训练之外的额外要求──

### LLM Önerileri üzerinden Farklı Gizlilik Değişimi

2025 saldırısı. DP eğitimi almış bir modelin güven puanlarını bireyleri yeniden tanımlamak için bir oracle olarak kullanın.

> 2025 Yeni gelişme saldırısı: DP 訓練模型の置信分数 を予測機として再识别個体として活用します.

Savunma: güvenliği ortaya çıkarmayın veya ortaya çıkmadan önce onları kısaltmayın. Bu (ε, δ) -DP eğitiminin ötesinde bir ek gerekliliktir.

> 防御:不露置信度,或在露前截断/量化──这是 (ε, δ) -DP 训练之外的额外要求──

### Bu 18 fazaya uygun.

Ders 20-21 tarafsızlık/eşitlik. Ders 22 gizlilik. Ders 23 su işaretleme yoluyla kaynak. Ders 27 düzenleyici veri kaynak katmanı kapsar.

> Dersler 20-21 偏见/公平──Lesson 22 隐私──Lesson 23 通过水印的来源──Lesson 27 涵盖监管数据来源层──

> **【拓展：DP-SGD 的实际开销 → LoRA 解决方案】**Tümçeş DP-SGD                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

## Kullanın Kullanın
```figure
an-dp-clip-noise
```

## Kullan

`code/main.py`Oyuncak ikili sınıflandırma verileri üzerinde DP-SGD simülasyonu yapar. Ses çarpıcısı σ ve kesme normı C'yi tarayabilir ve (ε, δ) bütçesini ve doğruluk maliyetini takip edebilir. "Kanary saldırısı" benzersiz bir eğitim örneğini ekler ve bir günlük kaybı testi DP'den önce ve sonra tespit edebilecek olup olmadığını ölçer.

> `code/main.py`Oyuncaklar II sınıfı verilerinde DP-SGD'yi simgeleyen; ses çarpımı s ve kesim biçimleri C'yi tarayabilir, (ε, δ) bütçe ve doğrulama oranı maliyetini takip edebilir.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-dp-audit.md`. Dil modelinin kullanılması üzerine DP iddiası göz önüne alındığında, (ε, δ) değerleri, kullanılan muhasebeci, MIA değerlendirme protokolü ve güven ve maruz kalma vektörlerinin değerlendirilmiş olup olmadığını denetler.

> 本课产 出 `outputs/skill-dp-audit.md`◊ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒   ⇒ ⇒ ⇒    ⇒ ⇒ ⇒ ⇒ ⇒ ⇒     ⇒      ⇒      ⇒                                                                                                                                                                     

## Egzersizler.

1. Çık .`code/main.py`. {0,5, 1.0, 2.0}'da σ'yi tarayıp (ε, δ) doğruluk oranını rapor edin.

2. Kanarya ekleme ve günlük kaybı testi uygulanır. DP-SGD'den önce ve sonra tespit oranını σ = 1.0 ile ölçün.

3. Nasr et al. 2025'te eğitim verileri çıkarma üzerine okuyun. Neden çıkarma başarısı orta ε altında çökmez?

4. PMixED (arXiv:2403.15638) kullanarak, tümüyle sonuçlama zamanında çalışacak bir dağıtım tasarlayın.

5. LLM Feedback saldırısı ile DP Değişimi çizin. Güven puanı sızmasını sınırlayan ve dağıtım maliyetini tahmin eden bir karşı önlem tasarlayın.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| DP | "(ε, δ)-differential privacy" | Formal privacy: output distribution close under neighbouring-dataset change |
| DP-SGD | "noise-injected SGD" | Gradient clipping + Gaussian noise addition; standard DP training |
| LoRA + DP-SGD | "efficient private fine-tune" | DP-SGD on low-rank adapters; standard 2025 configuration |
| MIA | "membership inference" | Attack that determines whether an example was in training data |
| Canary | "inserted watermark example" | Unique training example used to measure DP leakage |
| PMixED | "private inference mixture" | Inference-time DP via mixture-of-experts on next-token distributions |
| DP Reversal | "confidence leakage attack" | Attack that uses a model's confidence as an oracle for re-identification |

## Daha fazla okumak

- [Abadi et al. — DP-SGD (arXiv:1607.00133)](https://arxiv.org/abs/1607.00133) Standart DP eğitim algoritması
- [Carlini et al. — Extracting Training Data (arXiv:2012.07805)](https://arxiv.org/abs/2012.07805) Kanonik çıkarma kağıdı
- [Duan et al. — Canary MIA on LLMs (arXiv:2402.07841, 2024)](https://arxiv.org/abs/2402.07841) Sıkı başarısızlıklı MIA
- [Kowalczyk et al. — Auditing DP for LLMs (arXiv:2503.06808, March 2025)](https://arxiv.org/abs/2503.06808) Gerginliğin çözümü
- [PMixED (arXiv:2403.15638)](https://arxiv.org/abs/2403.15638) İhtiyaçlı zaman özel tahmin
