# Model, Sistem ve Veri Serisi Kartları

> Üç belge biçimi, Yapay zeka şeffaflığını yapılandırır. Model Kartlar (Mitchell et al. 2019'da,  modeller için beslenme etiketleri: eğitim verileri, miktarlı ayrıştırılmış analizler, etik düşünceler, uyarılar; Hugging Face model kartlarının sadece %0,3'ü etik düşünceler belgelendirir (Oreamuno et al. 2023 yılı). Verim Satıları Verim Sayfaları (Gebru et al. 2018 (CACM)  Motivasyon, kompozisyon, toplama süreci, etiketleme, dağıtım, bakım; elektronik- veri levha analogiyası. Veri Kartları (Pushkarna et al., Google 2022)  Modüler katmanlı detaylar (teleskopik, periskopik, mikroskopik) çeşitli okuyucular için sınır nesneleri olarak. 2024-2025 gelişmeleri: LLM'ler aracılığıyla otomatik üretim (CardGen, Liu et al. Bu nedenle, HF'nin yüklenmesi %29'a kadar artmıştır. 2024); doğrulanabilir sertifikalar (Laminator, Duddu et al. 2024); karbon/su için sürdürülebilirlik raporlama eklemeleri (Jouneaux et al. Temmuz 2025); Avrupa Birliği/ISO düzenleyici kartları ortaya çıkıyor. Sistem Kartları (Sidhpurwala 2024; Meta sistem düzeyinde şeffaflık; "Tevkiye dair Blueprints" arXiv:2509.20394)  Güvenlik yeteneklerini, hızlı enjeksiyon korumasını, veri filtrasyonunun tespitini, insan değerleriyle uyumluyu kapsayan sonundan sonuna kadar AI sistem belgeleri.

> **【中文解读】**Bu bölümde model/ sistem/ veri kümesi kartları AI  sistem şeffaflığı standartlaşmış dosyaları。 üç çeşit dosya biçimleri farklı şeffaflık aralığı vardır:Model Kartlar(Mitchell  et al 2019) Model'in beslenme etiketleri;Data kümeleri için veri levhaları(Gebruary  et al 2018) Data kümesi elektronik kuralları kitapları;System Kartlar端到端 AI 系统文档。

> **【拓展：采用率 → 0.3% 问题】**Oreamuno  et al. 2023  Audit Hugging Face  Model card bulguları sadece %0,3  etik değerleri kaydetti. Liang  et al. 2024                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, model-card + datasheet + system-card generator) | **语言:** Python（标准库，模型卡 + 数据表 + 系统卡生成器）
**Prerequisites:** Phase 18 · 18 (safety frameworks), Phase 18 · 24 (regulatory) | **前置知识:** Phase 18 · 18 (安全框架), Phase 18 · 24 (监管)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前 Lütfen önce öğrenin:Fase 18·18+24──三种透明度文档:模型卡 + 数据集卡 + 系统卡──
>  **【类比】**透明度卡 = "AI'nin ürün açıklaması"──Model Kartlar = 营养标签(训练数据/分析/伦理);Datasheet = 电子元件规格书(数据集动机/组成/收集);System Card = 整机蓝图(端到端系统)──问题:仅0.3% HF 模型卡含伦理考量──
> 🤔 详细卡 → 下载量 29%(HF 2024 数据)  透明度有商业价值──2024-2025 Yeni trend:LLM 自动生成卡(CardGen)、可验证证明(Laminator)、可持续性报告(碳/水)。

## Öğrenme hedefleri

- Mitchell et al. 2019 model kartını ve Gebru et al. 2018 veri sayfasını açıklayın.
- Veri Kartlarının teleskopik/periskopik/mikroskopik katmanını açıklayın.
- Sistem Kartlarını ve sonundan sonuna kadar kapsamını açıklayın.
- 2024-2025 yıllarındaki üç gelişmeyi belirtin (otomatik üretim, doğrulanabilir sertifikalar, sürdürülebilirlik raporlamaları).

> 描述 Mitchell 等人 2019 yılının orijinal modeli卡和 Gebru 等人 2018 yılının verileri tablosu.

## Sorun . Sorun .

Yönetim çerçeveleri (Desin 24) ve laboratuvar güvenliği politikaları (Desin 18) her ikisi de belgelendirme gerektirir. Belge biçimleri model-spesifik (model kartları) ile veri kümesi-spesifik ( veri levhaları) ile sistem-spesifik (sistem kartları) arasında gelişmiştir. Her biri farklı bir şeffaflık kapsamını ele alıyor. 2024-2025 otomasyon ve doğrulanabilir-sertifika çalışmaları uzun süredir devam eden kabul sorunu ele alıyor.

> 监管框架和实验室安全政策都要求文档――文档格式从模型特定 (模型卡) to数据集 (数据集) 特定 (数据表) to system (系统) 特定 (系统卡) 发展――2024-2025 yılları otomatikleştirme ve doğrulama kanıtları çalışmaları uzun süreli kabul sorunlarını çözdü――

## Konsep kavramı.

> **【中文解读】**Model Kartlar 九大板块:模型详情、预期用途、因素(相关人口或环境因素) 、指标、评估数据、训练数据、定量分析(因子分解) 、伦理考量、注意事项和建议──Data Cards(Google 2022) △三层缩写:望远镜级(非专家高层摘要) 潜望镜级(ML 从业者中层概览) 微镜级(审计员显详细特征级文档) △

### Model Kartlar (Mitchell et al. 2019)

Bölümler:
- Model detayları.
- İstihbarat.
- Değerlendirme için önemli demografik veya çevresel faktörler.
- - Metrikler.
- Değerlendirme verileri.
- Eğitim verileri.
- Kvantitatif analizler (faktorlara göre ayrıştırılmış).
- Etik bakış açıları.
- Kafateler ve tavsiyeler.

Evlatlık sorunu: Oreamuno et al. Hugging Face model kartlarının 2023 denetiminde etik değerleri sadece %0,3'ü buldu.

### Verim Satıları Verim Sayfaları (Gebru et al. 2018)

Elektronik- veri levha analogiyası.
- Motivasyon (veriler kümesi neden oluşturuldu).
- Yapılandırma (bunlarda ne var).
- Toplama süreci (gönüllü olarak nasıl toplandı).
- Etiketleme (eğer geçerli ise).
- Kullanımlar (hükümlendirilmiş, yasaklanmış, riskler).
- - dağıtım.
- Bakım.

CACM 2021'de yayınlanmıştır. Veri sayfası yukarıdaki belgelendirme; model kartı veri sayfasının doğru olduğundan bağlıdır.

### Veri Kartları (Pushkarna et al., Google 2022)

Modüler katmanlı detaylar.
- **Telescopic.**Uzman olmayanlar için yüksek düzeyde özet.
- **Periscopic.**ML uygulayıcıları için orta düzeyde genel bakış.
- **Microscopic.**Denetçiler için ayrıntılı özellik düzeyde belgeler.

Sınır-objekt çerçeveli: farklı okuyucular aynı belgeye farklı bilgiler çıkarır.

> **【拓展：System Cards → 部署层透明度】**Sistem Kartlarının kapsamı sonuna kadar AI sistemleri  sistemleri   model + güvenlik  + deployment  on下文 典型板块: güvenlik kapasitesi 提示注入保护、数据外泄检测、与声明的人类价值观对齐、事件响应── "Bluprints of Trust" (ArXiv:2509.20394) Sistem Kartlarını 形式化 模型卡的部署层补充──EU AI Act GPAI 代码实践透明度章节要求模型卡作为合规工件──

### Sistem Kartları

Kapsam: Model + güvenlik yığın + dağıtım bağlamı dahil olmak üzere sonundan sonuna kadar AI sistemi. Bölümler genellikle şunları içerir:
- Güvenlik yetenekleri.
- Hızlı enjeksiyon koruması.
- Veri eksfiltrasyonu tespit.
- Açıklanan insan değerlerine uyum sağlamak.
- - Olay tepkisi.

Sidhpurwala 2024 ve Meta sistem düzeyinde şeffaflık çalışmaları. "Tiranç Buluçları" (arXiv:2509.20394) Sistem Kartını Model Kartlara dağıtım katmanının tamamı olarak resmileştirir.

> **【中文解读】**2024-2025 yılları geliştirilmesinde:CardGen(Liu 等人 2024) LLM tarafından otomatik üretim modeli kartları, rapor birçok yapay kartlardan daha yüksek objektiflik;Laminator(Duddu 等人 2024) tarafından hardware TEE/加密 imzası gerçekleştirmek可验证证明 model kartları taşıma deklarasyon kanıtları sadece bir açıklama değil; sürdürülebilirlik 字段(Jouneaux 等人 2025 yılının 7 月)

### 2024-2025 gelişmeleri

- **CardGen (Liu et al. 2024).**LLM'ler aracılığıyla otomatik model kart üretimi; standart Mitchell 2019 alanlarında birçok insan tarafından yazılan karttan daha yüksek objektiflik raporları.
- **Download correlation (Liang et al. 2024).**Detaylı model kartlar HF  kabul basıncındaki en yüksek indirme oranlarının %29'a kadar oranıyla ilişkili olmakta sadece uyumluluk yönünde değil piyasa yönünde de ilerliyor.
- **Laminator (Duddu et al. 2024).**Hardver TEE / kriptografik imzalar yoluyla doğrulanabilir sertifikalar  model kartın sadece bir talebi değil, bir iddia kanıtı taşımasına izin verir.
- **Sustainability (Jouneaux et al. July 2025).**Karbon, su ve bilgisayar enerjisi ayak izi için eklemeler; ortaya çıkan ISO standartları.
- **Regulatory cards.**AB Yapay zeka Yasası (Deneyim 24) GPAI Uygulama Kodu Şeffaflık bölümünde uyumluluk eseri olarak model kartlar gerekmektedir.

### Bu 18 fazaya uygun.

Ders 24-25 düzenleyici ve CVE katmanlarıdır. Ders 26 belgeler katmanıdır. Ders 27 veri sayfasının yukarı akımı olan eğitim veri yönetimi. Ders 28 kartlarda referans edilen değerlendirmeleri üreten araştırma ekosistemidir.

> Ders 24-25 监管和CVE 层――Lesson 26 文档层――Lesson 27 训练数据治理――Lesson 28 产生卡片中引用评估的研究生态系统――

> **【拓展：可验证证明 → Laminator】**Laminator(Duddu  et al. 2024) Hardware TEE / 加密 imzasını kullanarak verilebilir kanıt gerçekleştirmek için  model kartı sadece bir açıklama değil, bir açıklama ile taşıyabilir. Örneğin, bir model kartı bölümü "X'deki doğruluk oranı % Y" olarak bir verilebilir.

## Kullanın Kullanın
```figure
an-card-scopes
```

## Kullan

`code/main.py`Oyuncak dağıtım için minimal bir model kartı, veri sayfası ve sistem kartı oluşturur. Her biri kanonik bölüm yapısını takip eder.

> `code/main.py`Oyuncuların dağıtımında en küçük model kartı, veri kartı ve sistem kartı üretilir. Her biri standart bölüm yapısını takip eder.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-card-audit.md`. Bir model kart, veri sayfası veya sistem kartı verilirse, bölüm kapsamını, sayısal parçalanmayı ve doğrulanabilir sertifikaların olup olmadığını denetler.

> 本课产 出 `outputs/skill-card-audit.md` Verili model kartı, veri tablosu veya sistem kartı, denetim bölümünün kapsamı, sayısal değer ayrımı ve doğrulanabilir kanıtların olup olmadığını göstermek

## Egzersizler.

1. Çık .`code/main.py`- Yaratılan kartları incelemek. Zayıf olan bölümleri (sadece yer sahibi için) belirlemek ve bunları güçlendirecek kanıtları belirtmek.

2. Modeldeki kartı iki demografik gruba boyutlu bir analizle genişlet (Desin 20).

3. Oreamuno et al. 2023'te 0.3% kabul oranı hakkında okuyun. Etik düşüncelerle kabul edilmeyi artıran bir yapısal değişiklik önerin.

4. Laminator (Duddu et al. 2024) doğrulanabilir attestasyonlar için TEE'leri kullanır. Bir değerlendirme sonuçlarının kriptografik bir attestasyonu bulunan ve doğrulayıcının rolünü açıklayan bir model kart alanı tasarlayın.

5. Geçmiş projelerinizden biri veya hipotezici bir dağıtım için bir Sistem Kartı (Sistem Kartı, Model Kartı değil) yazın.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Model Card | "the Mitchell card" | Mitchell et al. 2019 standard documentation for ML models |
| Datasheet | "the Gebru datasheet" | Gebru et al. 2018 standard documentation for datasets |
| Data Card | "the Pushkarna card" | Google 2022 modular layered data documentation |
| System Card | "the deployment card" | End-to-end AI system documentation including safety stack |
| Boundary object | "different readers, one doc" | Data Cards framing: same document serves diverse audiences |
| Verifiable attestation | "the Laminator attestation" | Cryptographic or TEE proof attached to a documentation claim |
| Sustainability field | "carbon / water footprint" | Emerging 2025 addition for environmental accounting |

## Daha fazla okumak

- [Mitchell et al. — Model Cards for Model Reporting (arXiv:1810.03993, FAT* 2019)](https://arxiv.org/abs/1810.03993) Kanonik model kartı
- [Gebru et al. — Datasheets for Datasets (CACM 2021, arXiv:1803.09010)](https://arxiv.org/abs/1803.09010) Verim sayfası kağıdı
- [Pushkarna et al. — Data Cards (Google 2022)](https://arxiv.org/abs/2204.01075) Katmanlı veri belgesi
- [Sidhpurwala et al. — Blueprints of Trust (arXiv:2509.20394)](https://arxiv.org/abs/2509.20394) Sistem Kartı resmileştirme
