# LLM'de Önyargı ve Temsilcilik Zararı

> Gallegos, Rossi, Barrow, Tanjim, Kim, Dernoncourt, Yu, Zhang, Ahmed (Bileştirici Dilbilim 2024, arXiv:2309.00770). Temel 2024 araştırması, temsil zararı (stereyotipler, silme) ve tahsis zararı (eşitsiz kaynak dağılım) arasında ayrım yaparak değerlendirme ölçümlerini yerleştirme tabanlı, olasılık tabanlı veya oluşturulan metrik tabanlı olarak sınıflandırır. 2024-2025 deneysel: An et al. (PNAS Nexus, Mart 2025) GPT-3.5 Turbo, GPT-4o, Gemini 1.5 Flash, Claude 3.5 Sonnet, Llama 3-70B'de 20 giriş düzeyde iş için otomatik olarak özetleme değerlendirmesi üzerinden kesimler arası cinsiyet x ırk ayrımcılığını ölçmek. WinoIdentity (COLM 2025, arXiv:2508.07111) kesimsel kimlikler için belirsizlik tabanlı adil değerlendirmeyi tanıttı. Yu & Ananiadou 2025 MLP katmanlarında cinsiyet nöronlarını tanımlar; Ahsan & Wallace 2025 klinik ırk ayrımcılığını ortaya çıkarmak için SAE'leri kullanır; Zhou ve diğerleri. 2024 (UniBias) dikkat başlıklarını deviseye sokar. Meta-tıkıntısı (arXiv:2508.11067): 10 yıllık edebiyat, eşcinsel önyargıya karşı orantısız bir şekilde odaklanır.

> **【中文解读】**Bu bölümde önyargı ve temsilcilik yarası AI sistemindeki önyargı kaynağı, denetim ve hafifleme yöntemleri Gallegos  et al. Computational Linguistics 2024) temsilcilik yarası ️ 刻板印象 抹除) ve dağılımcılık yarası ️ eşitsiz kaynak dağılımını ayırt eder, ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️ ️  ️ ️ ️ ️ ️ ️  ️ ️  ️ ️   ️    ️  

> **【拓展：交叉偏见 → 真实世界影响】**Bir 等人(PNAS Nexus, 2025 yıl 3 月) GPT-3.5 Turbo、GPT-4o、Gemini 1.5 Flash、Claude 3.5 Sonnet、Llama 3-70B ⇒ 20 个入门级职位自动简历评估中的交叉性别×种族偏见──GPT-4o 在简历评分中黑人女性に対する罰は黑人男性と白人女性に対する分別よりも深刻单轴評価はこの効果を把握できない──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, toy embedding-based bias probe) | **语言:** Python（标准库，玩具嵌入偏见探针）
**Prerequisites:** Phase 05 (word embeddings), Phase 18 · 01 (instruction following) | **前置知识:** Phase 05 (词嵌入), Phase 18 · 01 (指令遵循)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Öğrenci bölümünün ilk aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aşamasında:Düşünme aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş aş
>  **【类比】**偏见 = "AI'nin renk gözlüğü"── eğitim verilerinden oluşuyor(社会历史偏见) + 训练目标──评估三方法:嵌入空间(向量几何) + 概率(logits 差) + 生成文本(输出统计)──2025 PNAS Nexus:GPT/Claude/Gemini/Llama 在简历评估上有交叉性别×种族偏见──Yu 2025 MLP 层定位"性别神经元",Ahsan 2025 用 SAE 揭露临床种族偏见──

## Öğrenme hedefleri

- Temsilcilik vs. tahsis zararı tanımlayın ve LLM dağıtımında her birinin bir örneğini verin.

> ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐

- Gallegos et al. 2024'ten üç değerlendirme-metrik kategorisi adını verin ve her birinden bir metrik tanımlayın.

> 列出 Gallegos 等人 2024 yılının üç sınıf değerlendirme göstergesi,并描述每类中的一个指标──

- Bölümler arası ilişkiyi ve WinoIdentity'nin belirsizlik tabanlı adillik ölçümünün tek eksel önyargılı önyargılı değerlendirme açılarını neden ele aldığını açıklayın.

> 交叉性 ve neden WinoIdentity'nin belirsizliklere dayalı adil ölçümleri tek birim önyargılı değerlendirme eksikliğini çözdü.

- Taraflılığa iki mekanizma-tortanlama yaklaşımını açıklayın (cinsel nöronlar, SAE özellikleri, dikkat başı manipülasyonu).

> 描述两种偏见的机制可解释性方法 (BİK'in iki türü vardır)

## Sorun . Sorun .

Önceki dersler kasıtlı zararları (ceilbreaks, scheme) ve güvenlik yönetimi kapsar. Tarafsızlık, amaçsızca  eğitim verileri dağıtımından, hızlı çerçeveleme, toplanmış tasarım seçimlerinden ortaya çıkan zararlardır.

> Önceki dersler kasıtlı zararlar (Hazırlar) ve güvenlik yönetimi ile ilgilidir. Önyargı, amaçsız zararlar (Hazırlar) olarak eğitim verileri dağılımından, öneriler çerçevesinden, toplanmış tasarım seçimlerinden kaynaklanır. Ölçüm ve azaltma, bu, zorluklara karşı farklı bir yöntem teorisiyle karşılaştırılır.

## Konsep kavramı.

### Temsilcilik vs. tahsis

- **Representational harm.**Hemşireleri sadece kadın olarak gösteren bir LLM temsilcilik zarar verir.
- **Allocational harm.**Siyah başvuruda bulunanların özetlerini sistematik olarak daha düşük puan alan bir LLM, tahsis zararı yaratıyor.

> **代表性伤害：**刻板印象、抹除、低性描画──**分配性伤害：**Eşsiz maddi sonuçlar. İki farklı  model "tümellik önyargısız" olabilir, ancak "ürekleyici önyargılı" olabilir.

Bu farklılıklardır. Bir model "tüm yönlerden tarafsız" olabilir (çok çeşitli portreler üretir) ve "tüm yönlerden tarafsız" olabilir (eşitsiz öneriler yapar).

> 评估需要同时测量两者──

> **【中文解读】**Üç sınıf değerlendirme göstergesi: yerleşim tabanı (WEB)  ölçüm kimlik kelime ve özellik kelime arasındaki istatistik ilişki, ölçüm göstergesi yerine davranışta sınırlıdır; olasılık tabanı  şablon onay vs  违反补充对数似然比,捕获部分行为偏见;生成文本基础下游任务测量 (WEB),生态度最高但最难复现.

### Üç değerlendirme-metrik kategorisi (Gallegos et al. 2024)

- **Embedding-based.**RLHF öncesi yerleşimlerde WEAT tarzı testleri. Kimlik terimleri ve atribut terimleri arasındaki istatistiksel ilişkileri ölçer.
- **Probability-based.**Stereotip doğrulayıcı ve stereotip ihlal eden tamamlamaların log-e olasılıkları.
- **Generated-text-based.**Yaratılan metin üzerinde aşağıdaki görev ölçümü. Özetleme puanlaması, tavsiye yazımı, diyalog. En ekolojik olarak geçerli; çoğaltılması en zor.

> **嵌入基础：**WEAT 式测试,测量身份词和属性词的统计关联──**概率基础：**刻板印象确认 vs 违反补全的对数似然比比──**生成文本基础：**Aşağı yukarı görev ölçümleri, en yüksek, ancak en zor tekrarlanmaktadır.

### Bölümler arası

"Cinsiyet" üzerinde önyargılı değerlendirme sadece (cins, ırk) çiftlere ateş eden önyargıyı kaçırır. Bir et al. 2025 bulguları GPT-4o, siyah kadınların özetleme sırasında ayrı ayrı siyah erkeklere ve beyaz kadınlara göre daha fazla puan almasına cezalandırır. Tek eksel değerlendirme bunu yakalayamaz.

> "Gender" üzerindeki önyargı değerlendirmeleri sadece  (gender, race) ile ilgili önyargıları atlatıyor.                                                                                                                                                                                                                                                

WinoIdentity (COLM 2025) belirsizlik tabanlı kesimsel adilliği tanıtır. Modelin kesimsel kimlik tuplesinde sonuçlar üzerindeki belirsizliklerinin farklı olup olmadığını ölçer.

> WinoIdentity  belirsizliğe dayalı bir tartışmacılık adil değerlendirmeyi başlatmak.

> **【拓展：机制可解释性 → 偏见干预新路径】**2024-2025 yılları mekanizma açıklanabilir çalışmaları, önde gelen mekanizma müdahale yollarını açtı: gender neurons (Yü & Ananiadou 2025)  belirli MLP sinirleri, cinsiyetle ilgili belirli davranışlar, gidermek bu sinirlerin sınırlı kapasite maliyetleriyle cinsiyet farkını azaltmak; klinik ırk önde gelen SAE (Ahsan & Wallace) 2025)  nadir kodlama öz kodlama özellikleri iç gösterileri açıklanabilir boyutlara parçalayacak; UniBias (UniBias)  Zhou 等人)  dikkatli işlemler, önde gelen örneği gerçekleştirmek üzere 

### Mekanik yaklaşımlar

2024-2025 tarihleri arasında yapılan yorumlama çalışmaları, mekanizma müdahalelerine önyargıyı açar:

- **Gender neurons (Yu & Ananiadou 2025).**Özel MLP nöronları cinsiyet-spesifik davranışlarla ilişkilidir. Bu nöronları silmek, sınırlı kapasite maliyeti ile cinsiyet fark ölçümlerini azaltır.
- **Clinical racial bias via SAEs (Ahsan & Wallace 2025).**Sparse oto kodlayıcı özellikleri, iç temsilini yorumlanabilir boyutlara parçalayır; ırk ile ilişkili özellikler tanımlanabilir ve bastırılabilir.
- **UniBias (Zhou et al. 2024).**Zıfır atışlı deviseleştirme için dikkat başı manipülasyonu. Özel başlar kimlik sınıfının hassasiyetini artırır; bu başları sıfırlamak veya yeniden ağırlaştırmak ince ayarlama olmadan tarafsızlığı azaltır.

> 2024-2025 Mechanism explainable work, önde gelenleri önlemleme ve müdahale için yol açtı: gender neurons 消融 bu neurons sınırlı kapasite maliyetleriyle cinsiyet farkını azaltmak; klinik ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ırk ır

> **【中文解读】**元評論(arXiv:2508.11067, 2025): 10 yıllık literatür incelemesi bu alanda ikili cinsiyet önyargısına orantısız bir şekilde odaklandığını buldu.

### Meta-kritik

10 yıllık literatür incelemesi (arXiv:2508.11067, 2025) alanın ikili cinsiyet ayrımcılığına orantısız bir şekilde odaklandığını buldu. Diğer ekseler  engelliği, din, göç durumunu, çok dilli kimliği  çok daha az ilgi görüyor. Meta-tıkıntısı, sınır dışı gruplara ihmal ederek dar bir odaklanma yaratabileceğini savunuyor: ikili cinsiyet üzerinde iyi ayrımcılık yapan bir model, kimsenin kontrol etmediği boyutlarda kötü bir tarafsızlık gösterebilir.

> 10 yıllık bir araştırma, bu alanda ikili cinsiyet önyargısına orantısız bir şekilde odaklandığını buldu. Diğer bir diğer etken ise engelliğin, dinin, göçmenliğin, çok dilli bir olgunluğun daha az ilgi alanını elde etmesi.

### Bu 18 fazaya uygun.

Dersler 20-21 ayrımcılık ve adilliği resmi olarak kapsar. Ders 22 gizliliği kapsar. Ders 23 su işaretlemeyi kapsar. Bunlar daha önceki aldatma / güvenlik katmanını tamamlayan kullanıcı zarar katmanı.

> Dersler 20-21 正式涵盖偏见和公平──Lesson 22 涵盖隐私──Lesson 23 涵盖水印──这些是补充早期欺骗/安全层的用户伤害层──

> **【拓展：交叉性 → WinoIdentity 基准】**WinoIdentity(COLM 2025, arXiv:2508.07111) belirsizliklere dayalı交叉性公平评估── farklı交叉身份元组 üzerindeki sonuçların belirsizliği 不仅是点预测── bu, modellerin her grup arasında "aynı hata ama bazı gruplar için daha belirsiz" durumunu yakalar, bu da farklı aşağı dağılım davranışları ortaya çıkarır.

## Kullanın Kullanın
```figure
an-bias-two-harms
```

## Kullan

`code/main.py`Oyuncak yerleştirme tabanlı bir önyargı araştırması yapar: basit bir eşleşme yerleştirme ile kimlik terimleri ve atribut terimleri arasındaki WEAT tarzı mesafeyi ölçer. Bir önyargı enjekte edebilir ve metrik ateşi gözlemleyebilirsiniz; basit bir defibasing işlevi uygulayarak kısmi geri kazanımı gözlemleyebilirsiniz.

> `code/main.py` Oyuncaklar yerleştirme önyargı çubuğu oluşturdu: ölçme                                                                                                                                                                                                                                                     

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-bias-eval.md`. Bir model kart veya adillik iddiası göz önüne alındığında, üç metrik kategoride (eğlenme, olasılık, oluşturulan metrik), kesimler arası kapsam ve herhangi bir devisaj müdahale mekanizması için değerlendirme denetlenir.

> 本课产 出 `outputs/skill-bias-eval.md`❖ Önemli bir model veya eşitlik bildirimi, denetim üç sınıfı göstergeleri değerlendirme, geçiş kapsamı ve önyargılı önlem mekanizması

## Egzersizler.

1. Çık .`code/main.py`- Debiasing adımından önce ve sonra WEAT tarzı tarafsızlık puanlarını bildirin.

2. Sonda kesimler arası bir test ile uzantı: (cinsel, ırk) x (kariyer, aile).

3. An et al. 2025 (PNAS Nexus) okuyun. Tek eksel cins değerlendirmesinin kaçırılacağı iki kesimsel etkeni belirleyin.

4. Yu & Ananiadou 2025'te cinsiyet nöronlarını tanımlar. "Bu nöronlar cinsiyet önyargısına neden olur" ve "bu nöronlar cinsiyet önyargısıyla ilişkilidir" arasındaki farkı yaratacak bir sahtelik deneyimi çizer.

5. Meta-kritik alanın ikili cinsiyet üzerinde çok dar bir şekilde odaklandığını iddia ediyor.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Representational harm | "stereotypes / erasure" | Biased portrayal of a group |
| Allocational harm | "unequal decisions" | Biased material outcome for a group |
| WEAT | "the embedding test" | Word Embedding Association Test; co-occurrence-based bias probe |
| Intersectionality | "combined identity effects" | Bias that emerges at the intersection of multiple identity axes |
| Gender neurons | "MLP bias neurons" | Specific neurons whose activations correlate with gender-specific behaviour |
| SAE feature | "interpretable dimension" | Sparse-autoencoder-identified feature; useful for mechanistic bias analysis |
| UniBias | "attention-head debiasing" | Zero-shot debiasing by reweighting attention heads |

## Daha fazla okumak

- [Gallegos et al. — Bias and Fairness in LLMs: A Survey (arXiv:2309.00770, Computational Linguistics 2024)](https://arxiv.org/abs/2309.00770) Kanonik araştırma
- [An et al. — Intersectional resume-evaluation bias (PNAS Nexus, March 2025)](https://academic.oup.com/pnasnexus/article/4/3/pgaf089/8111343) Beş model çapraz çalışma
- [WinoIdentity — uncertainty-based intersectional fairness (arXiv:2508.07111, COLM 2025)](https://arxiv.org/abs/2508.07111) Yeni bir referans değer
- [UniBias — attention-head manipulation (Zhou et al. 2024, ACL)](https://arxiv.org/abs/2405.20612) sıfır atışlı devreye atış
