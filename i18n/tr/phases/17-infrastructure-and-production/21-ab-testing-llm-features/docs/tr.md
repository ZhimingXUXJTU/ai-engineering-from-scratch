# A/B Testing LLM Özellikleri  GrowthBook, Statsig ve Vibes Sorunu

> Geleneksel A/B testleri belirlenmez LLM için yapılmadı. Kritik fark: değerlendirme cevapları "model işi yapabilir mi?" A / B testleri "kullanıcılar umurunda mı?" cevapları; her ikisi de gereklidir; vibe kontrolleri ile teslimat bitti. 2026'da neyi test edeceğiz: hızlı mühendislik (sözleme), model seçimi (GPT-4 vs GPT-3.5 vs OSS; doğruluk vs maliyet vs gecikme), üretim parametreleri ( sıcaklık, üst-p). Gerçek durumlar: bir chatbot ödül modeli varianti +70% konuşma uzunluğu ve +30% tutumu sağladı; Nextdoor AI konu hattı deneyleri ödül fonksiyonunu geliştirdikten sonra +1% CTR verdi; Khan Academy Khanmigo gecikme vs. matematik doğruluğu eksisinde tekrarlandı. Platform bölünmesi: **Statsig**(OpenAI tarafından Eylül 2025'te 1.1 milyar dolara satın alındı)  sıralı test, CUPED, tümü bir. **GrowthBook** açık kaynaklı, depo doğası, Bayesian + Frequentist + Sequential motorları, CUPED, SRM kontrolleri, Benjamini-Hochberg + Bonferroni düzeltmeleri. depona SQL tercihlerine göre seçersiniz ve "OpenAI tarafından satın alınması" kuruluşunuz için önemli mi.

> **【中文解读】**Bu bölümde LLM Özelliklerinin AB Test 科学评估 LLM 機能变更效果的方法を紹介しています。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy sequential test simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 20 (Progressive Deployment) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 20 (Progressive Deployment)

>  **【前置】**Öğrenci bölümünün ilk aşamasında: 17·13(可观测性)  17·20(渐进部署) 统计基础 (CUPED、序贯测试)  geleneksel A/B 不为非确定性 LLM 设计──
>  **【类比】**LLM A/B 测试 = "bilimsel yöntemlerle yerine beyin tasası"──关键区别:eval 问"模型能做吗";A/B 问"用户在乎吗"──两者都要──测什么:快措辞、模型选择、生成参数(温度/top-p)──案例:聊天机器人变体+70%对话长度+30% 留存;Nextdoor AI 标题+1% CTR;Khanmigo 在延迟 vs 数学准确率间舍──平台:Statsig((AI 11 milyar satın alma,全功能) 、GrowthBook 开源库 原生、贝叶斯频率+被序贯引擎) ‖
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- Değerlendirme değerlerini ("model işi yapabilir mi") ve A/B testlerini ("kullanıcılar umurunda mı") ayırt edin.
  Çinçe Çevirimiçi:区分评估("模型能做这个工作吗")
- Üç test edilebilir ekseni (sürekli, model, parametreler) sayın ve her bir için metrik seçin.
  Çinçe Çevirimi:列举三个可测试轴 (提示、模型、参数)并为每个选择指标──
- CUPED, sıralı test ve Benjamini-Hochberg çoklu karşılaştırma düzeltmelerini açıklayın.
  Çeviri: CUPED、序贯检验和 Benjamini-Hochberg 多重比较校正──
- Depo-SQL duruşuna ve kurumsal satın alma tutumuna göre Statsig veya GrowthBook'u seçin.
  Çinçe Çevirisi: deposu-SQL 态势和企业收购立场选择 Statsig 或 GrowthBook。

## Sorunlar. Sorunlar.

> **【中文解读】**传统 A/B 测试不是为不确定性 LLM 构建的──关键区分:评估(evals) 回答"模型能做这件事吗?",A/B 测试回答"用户在乎吗?"两者都是必需的凭感觉上线(vibes check) 时代已经结束──2026年可测试的三个维度:提示工程(措辞) 模型选择(GPT-4 vs GPT-3.5 vs OSS;确准率 vs 成本 vs 延迟) 生成参数(温度、top-p) ⋅

> **【拓展：LLM A/B 测试的真实案例】**2026 yılında LLM A/B 测试s production case:(1) 聊天机器人奖励模型变体+70%对话长度、+30% 留存率;(2) Nextdoor AI 主题行实验奖励函数优化后 +1% CTR;(3) Khan Academy Khanmigo在延迟对数学准确率轴上代;;平台选择:Statsig(2025 yıl 9 月被 OpenAI以 $1.1B 收购) 全合一;GrowthBook开源、仓库原生、Bayesian + Frequentist + Sequential 引擎──

Bir sistem uyarısını elle ayarladınız. Daha iyi hissettiriyor. Gönderirsiniz. Değişiklikler gürültüyle değişir. Metrikleri suçluyorsunuz. Yoksa yeni bir model gönderdiniz ve dönüşüm hareket etmedi.

Evals, modelin etiketlenen bir set üzerinde bir görev yapabileceğini ve yapamayacağını cevaplar. Kullanıcıların çıkışa tercih ettiğini cevaplamaz. Sadece kontrol edilen bir çevrimiçi deney buna cevap verir ve deneyin yeterli gücü varsa, belirlenmeci olmayanı kontrol eder ve birden fazla karşılaştırma için düzeltir.

## Konsepten bir şey.

### Evals vs A/B testleri

**Evals** çevrimdışı, etiketlenen set, yargıç (rubrik veya yargıç olarak veya insan olarak). Cevap: "Bu sabit dağıtımda çıkış doğru / yararlı / güvenli mi?"

**A/B test** online, canlı kullanıcılar, rastgele. Cevap: "Yeni variant önemli olan kullanıcı seviyesindeki ölçüyü değiştiriyor mu?"

Her ikisi de gereklidir. Evals, maruz kalma öncesi gerilemeleri yakalar; A/B, ürün etkisini sonrasında doğruluyor.

### Neyi test edelim

1. **Prompt engineering** kelime, sistem-sürekli yapı, örnekler.
2. **Model selection** GPT-4 vs GPT-3.5-Turbo vs Llama-OSS. Metrik: doğruluk (iş) + maliyet/ talep + gecikme P99. Çoklu hedef.
3. **Generation parameters** sıcaklık, üst-p, max_tokens. Metrik: görev-specifik (çıkış çeşitliliği vs. belirleme).

### CUPED  değişkenlik azaltımı

> **【中文解读】**CUPED (CUPED) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cuped) (Cup) (Cup) (C) (C) (C) (C) (C

Kontrol edilen deneyler, deneyden önceki verileri kullanarak. Dönem öncesi varyansiyonu, sonrası varyansiyonu karşılaştırmadan önce geri çevir. Tipik varyansiyon azaltımı: 30-70%.

Uygulama: Statsig ve GrowthBook uygulaması.

### Sıralama testleri

Klasik A/B, sabit örnek boyutunu varsayır. Sıralama testleri ("bakıp karar") tekrarlanan bakışlar altında yanlış pozitif oranı kontrol eder. Her zaman geçerli sıralı prosedürler (mSPRT, Howard'ın güven sırası) net kazanıcıları erken durdurmanıza izin verir.

### Çoklu karşılaştırma düzeltmeleri

%95 güvenle 20 A/B testi yapılması tesadüf olarak bir yanlış pozitif üretir. Bonferroni düzeltmesi test başına α'yı sıkılaştırır; Benjamini-Hochberg yanlış keşif oranını kontrol eder. GrowthBook her ikisini de uyguluyor.

### SRM  örnek oranı eşleşmezliği

Görev hash kullanıcıları varyasyonlara rastgeleleştirir. 50/50 bölünme 47/53'ü verirse, bir şey kırılır  SRM kontrolü onu işaretler.

### Statsig vs. GrowthBook

> **【拓展：Statsig vs GrowthBook 选型】**Statsig vs GrowthBook'un 2026 yıl seçimi modeli karşılaştırma:Statsig 2025 yılının Eylül ayında OpenAI tarafından 1.1B $ ile satın alınmıştır, tamamı bir SaaS'dır (Figure flags + 实验分析 + 可观测性),内置序贯检查和 CUPED, 捆绑产品的团队适合――GrowthBook is MIT 开源,仓库原生 (直接读 Snowflake/BigQuery/Redshift), Bayesian + Frequentist + Sequential 三种引擎、CUPED、SRM 检查、Benjamin-Hochberg + Bonferroni 正正, 适合数据团队控制的偏标的库-SQL 商店──选型关键:是否介意 OpenAI所有权 + 是否仓库-SQL──

**Statsig**- ...
- OpenAI tarafından 1.1 milyar dolarlık bir fiyatla satın alındı (Eylül 2025).
- Sıralama testleri, CUPED, dayanıklı popülasyonlar.
- Tüm birer: özellik bayrakları + deney + gözlemlenme.
- En iyi uygulama: Takım zaten bir paketli ürün istiyor, OpenAI'nin sahipliği umurunda değil.

**GrowthBook**- ...
- Açık kaynaklı (MIT); depo-dev (Snowflake/BigQuery/Redshift'ten doğrudan okur).
- Çoklu motorlar: Bayesian, Frequentist, Sequential.
- CUPED, SRM, Bonferroni, BH düzeltmeleri.
- Kendi kendine barındırma veya yönetilen bulut.
- En iyi uygunluk: deposu SQL dükkanı, veri ekibi metrik katmanı kontrol ediyor, OSS istiyor.

### Kararlılıktan uzak olmak güçleri karmaşıklaştırır

Aynı prompt farklı çıkışlar üretir. Geleneksel güç hesaplamaları IID gözlemlerini varsayır. LLM belirlemeciliği ile, etkili örnek boyutu nominalden daha düşüktür.

### Gerçek dava sonuçları

- Chatbot ödül modeli varianti: +70% konuşma uzunluğu, +30% tutma.
- Sonraki konu çizgileri: Ödül fonksiyonunun geliştirilmesinden sonra %1 + CTR.
- Khan Academy Khanmigo: İteratif gecikme karşı matematik doğruluk ticareti.

### Anti-pattern: vibes üzerinde nakliye

> **【拓展：LLM 非确定性对 A/B 测试的影响】**LLM'nin belirsizlik etkisi A/B testlerinin istatistik fonksiyonu. Aynı fikir farklı çıkışlar, geleneksel güç  hesaplama hipotezi IID gözlem değerleri oluşturur. LLM belirsizliği altında, geçerli örnek miktarı nominal değerden aşağıdır.

Her üst düzey mühendis, gönderilen bir özelliğin adını verebilir çünkü "A/B olmadan daha iyi hissettiriyor". Çoğu ürün ölçümleri, takım aylarca fark etmedi. A/B zorlayıcı fonksiyon.

### Hatırlamalısın numaralar

- Statsig, OpenAI tarafından satın alındı: 1.1 milyar dolar, Eylül 2025.
- GrowthBook: açık kaynaklı MIT; Bayesian + Frequentist + Sequential.
- CUPED değişkenlik azaltımı: 30-70%.
- LLM belirlenmezliği → +30-50% örnek boyut tamponu.

## Çerçeveyi kullanın.
```figure
mx-sequential-test
```

## Kullan

`code/main.py`sabit ve sıralı sınırlar ile bir dizi A/B testi simüle eder.

> `code/main.py`sabit ve sıralı sınırlar ile bir dizi A/B testi simüle eder.

> `code/main.py`sabit ve sıralı sınırlar ile bir dizi A/B testi simüle eder.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-ab-plan.md`Özellik değişikliği, iş yükü, başlangıç çizgisi, platform seçimi, kapılar, örnek boyutu göz önüne alındığında.

> 本课产 出 `outputs/skill-ab-plan.md`Özellik değişikliği, iş yükü, başlangıç çizgisi, platform seçimi, kapılar, örnek boyutu göz önüne alındığında.

## Egzersizler.

1. Çık .`code/main.py`% 5 yükseltme için, başlangıç değerinde % 3 dönüşüm ile, % 80 güç için hangi örnek boyutu?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ %5 提升 基线 3% 转换率, kaç örnek miktarı gerekiyor?
2. Sağlık hizmetleri ile düzenlenen bir yerleşim müşteri için Statsig veya GrowthBook'u seçin.
   Çinçe Çevirisi: Çeviri veya Büyüme Kitabı
3. GPT-4 vs GPT-3.5'i çözülmüş bilet fiyatına test eden bir A/B tasarlayın.
   Çinçe Çevirimiçi: Design One On Per Resolution工单成本上测试 GPT-4 vs GPT-3.5'in A/B ⇒
4. Kanarya geçiyor ama A/B %1,2 dönüşüm gösterir.
   Çinçe Çevirim: Senin Kızılçak Geçer, Ama A/B  Göster -1.2%  dönüşüm oranı.
5. CUPED'i, bir ön dönemde, post varyansiyonunun %60'ı ile uygulayın.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Eval | "offline test" | Labeled-set evaluation of model capability |
| A/B test | "experiment" | Live randomized comparison on users |
| CUPED | "variance reduction" | Pre-period regression to reduce variance |
| Sequential test | "peek-ok test" | Always-valid procedure allowing early stop |
| Multiple comparison | "the family error" | Running many tests inflates false positives |
| Bonferroni | "tight correction" | Divide α by number of tests |
| Benjamini-Hochberg | "BH FDR" | False-discovery-rate control, less conservative |
| SRM | "bad split" | Sample ratio mismatch; assignment bug |
| Statsig | "OpenAI owned" | Commercial all-in-one, acquired 2025 |
| GrowthBook | "the OSS one" | MIT warehouse-native platform |
| mSPRT | "sequential probability ratio test" | Classical sequential procedure |

## Daha fazla okumak

- [GrowthBook — How to A/B Test AI](https://blog.growthbook.io/how-to-a-b-test-ai-a-practical-guide/)
- [Statsig — Beyond Prompts: Data-Driven LLM Optimization](https://www.statsig.com/blog/llm-optimization-online-experimentation)
- [Statsig vs GrowthBook comparison](https://www.statsig.com/perspectives/ab-testing-feature-flags-comparison-tools)
- [Deng et al. — CUPED](https://www.exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf)
- [Howard — Confidence Sequences](https://arxiv.org/abs/1810.08240)
