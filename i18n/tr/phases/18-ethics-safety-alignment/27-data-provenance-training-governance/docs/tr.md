# Veri Kaynağı ve Eğitim - Veri Yönetimi

> AB Yapay zeka Yasası, Ağustos 2025'e kadar GPAI için makine okuyabilir seçme standartlarını (AB Telif Hakları Direktifi TDM istisna yoluyla) gerektirir. California AB 2013 (mürze 2024)  Genereatif AI eğitim- veri şeffaflığı geliştiricilerin 12 görevli alanla veri kümelerinin özetini yayınlamasını gerektirir. 2025 DPA'nın meşru çıkarlara ilişkin uyumluluğu: İrlanda DPC (21 Mayıs 2025) Meta'nın ilk taraf kamu AB/Aİ yetişkin içeriği üzerine LLM eğitimini, EDPB'nin görüşünden sonra garantilerle kabul eder; Köln Yüksek Bölgesel Mahkemesi (23 Mayıs 2025) fermanı reddeder; Hamburg DPA acillikten vazgeçiririr; UK ICO (23 Eylül 2025) LinkedIn'in AI eğitim güvencelerine (şeffaflık, basitleştirilmiş seçme, genişletilmiş itiraz pencereleri) olumlu bir düzenleyici yanıt verir ve izlemeyi sürdürür  resmi bir onay değil. Brezilya ANPD (2 Temmuz 2024) Meta'nın yeterli bilgi şeffaflığı nedeniyle işlemini askıya aldı; önleyici önlem, Meta'nın bir uyum planı sunmasından sonra 30 Ağustos 2024'te kaldırıldı. Ana geri dönüşü olmayanlık sorunu: çerez onay çerçeveleri gerçek zamanlı, geri dönüşübilir izleme için tasarlanmıştır; veriler model ağırlıklarda olduğunda, cerrahi silme imkansızdır  eğitimli sinir ağları için GDPR'nin silme hakkı pratik değildir. İstifadeden sonra veri verilecek. Data Provenance Initiative (dataprovenance.org, Longpre, Mahari, Lee et al., "Krizde İznin", Temmuz 2024): Yayıncılar robots.txt kısıtlamalarını ekledikleri için AI veri ortaklarının hızla düştüğünü gösterir.

> **【中文解读】**Bu bölüm, veri kaynağı ve eğitim yönetimini tanıtıyor  AI  eğitim verilerinin yasal ve geri dönüşü sağlıyor ▸ California AB 2013  isteği üretilen AI geliştiricileri yayınlamak içeren 12 önemli bölümler içeren veri kümesi özetleri。 EU AI Yasası ▸ GPAI 2025 yılının Ağustos ayından önce makine okuyabilir çıkış standartlarını gerçekleştirmek için ▸ önemli geri dönüşü olmayan sorun: veri bir kere model ağırlığı, ameliyatlı silinme imkansız ▸ eğitim sinir ağları gerçek bir GDPR yok ▸

> **【拓展：合法利益趋同 → 2025 DPA 立场】**2025 yılının birçok veri koruma kuruluşu meşru bir çıkar pozisyonunda trend: İrlanda DPC(2025 yılının Mayıs 21 günü) Meta on First-Party Open EU/EEA Adult Content on Training LLM planı(带保障措施);Köln Yüksek Bölge Mahkemesi yasaklamayı reddetti;UK ICO(2025 yılının 23 Eylül 23 günü) LinkedIn'e 恢复 AI training 发发发出积极监管回应──趋同原则: meşru çıkarlar açıkça kullanılabilir ilk taraf içeriği üzerinde yapılan eğitimlerin makul olduğunu kanıtlayabilir, onay gerektirmez.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, 12-field California AB 2013 scaffolding generator) | **语言:** Python（标准库，12 字段 California AB 2013 脚手架生成器）
**Prerequisites:** Phase 18 · 24 (regulatory), Phase 18 · 26 (cards) | **前置知识:** Phase 18 · 24 (监管), Phase 18 · 26 (卡片)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前 Lütfen önce öğrenin:Fase 18·24-26── DataTraceability + Training Management AI Training Data's Legality and Traceability──
>  **【类比】**DATABREAD = "Ettomat Source Label"──EU AI Act  requirements 2025.8 前机器可读退出标准(TDM 例外);California AB 2013 要求发布 12 字段数据集摘要──关键不可逆性:cookie 同意框架是实时可逆的;数据进权重后无法手术擦除训练后神经网络没有实际GDPR 被遗忘权──合规窗口在收集时──
> ️ Veri Kaynakları Girişimi 2024.7:AI 数据共享生态快速衰退,出版方加 robots.txt 限制──

## Öğrenme hedefleri

- California AB 2013'in 12 görev alanını anlatın.
- DPA'nın 2025 yılında meşru çıkarlı LLM eğitimine ilişkin pozisyonunu belirtin (İrlanda DPC, UK ICO, Hamburg, Köln).
- Geri dönüşülemezlik sorunu anlatın: GDPR'nin silme hakkının eğitimli sinir ağları için pratik eşdeğerleri neden yok.
- Veri Kaynak Girişiminin "Krizde İzin" bulgularını belirtin.

> California AB 2013'in 12 önemli bölümünü anlatın. 2025 yılı DPA'nın  Legal Interest LLM  Training Standards: Description irreversible problem: Why GDPR

## Sorun . Sorun .

Eğitim veri yönetimi, her model kartın (Desin 26) ve düzenleyici yükümlülüklerin (Desin 24) ön tarafında bulunur. 2024-2025 yıllarında, düzenleyici manzara üç ilke üzerinde birleştirilmiştir: seçme altyapısı, her veri kümesi açısından açıklama ve halka açık veriler için meşru çıkar uyumları. Toplama zamanında uyumlu olmayan sağlayıcılar aşağıdaki durumu düzeltemezler.

> DATA GERENMENT'i eğitmek her modelin ve denetim yükümlülüğünün üst üssüdür. 2024-2025 yılları için denetim manzarası üç prensipte pekiştirilmiştir: altyapıdan çıkmak, her veri kümesinin açıklanması ve açık kullanılabilir verilerin yasal çıkarlarının düzenlenmesi. Toplama sırasında uygunsuzluk sağlayıcıları aşağı üssü destekleyemezler.

## Konsep kavramı.

> **【中文解读】**California AB 2013'in 12 önemli bölümleri: Data set source/owners DATA set how to promote AI system expected purpose DATA point number DATA point type description DATA set contains copyrighted/trade mark/patent protected data DATA set DATA set DATA set DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA DATA  DATA DATA DATA DATA DATA           DATA DATA DATA DATA DATA DATA   DATA DATA DATA DATA      DATA      DATA DATA     

### California AB 2013

İşlem 2024. 1 Ocak 2022'de veya sonrasında yayınlanan sistemler için belgeler 1 Ocak 2026'da veya daha önce yayınlanmalıdır. 3111 (a) Bölüm geliştiricilerin eğitimde kullanılan veri kümelerinin 12 yasal madde ile yüksek düzeyde bir özetini yayınlamasını gerektirir:
1. Veritabelerin kaynakları veya sahipleri.
2. Veriler kümelerinin, AI sisteminin amaçlanan amacını nasıl ilerlettiğini açıklamak.
3. Veriler topluluğundaki veri noktalarının sayısı (genel aralıkları kabul edilebilir; dinamik veri toplulukları için tahminler).
4. Veri noktalarının türlerinin açıklaması (etiketlenmiş veri kümeleri için etiket türleri; etiketlenmemişler için genel özellikler).
5. Veri kümeleri, telif hakkı, ticari marka veya patentle korunan herhangi bir veri içerir veya tamamen kamu alanında olup olmadığını.
6. Veri kümelerinin satın alınmış veya lisanslanmış olup olmadığını.
7. Veriler topluluğunun kişisel bilgiler içermeyeceği (Civil Code §1798.140 ((v)).
8. Veriler kümelerinin toplam tüketicilerle ilgili bilgileri içerdiği (Civil Code §1798.140 ((b)).
9. İnşaatçı tarafından amaçlı temizlik, işleme veya diğer değişiklikler.
10. Verilerin toplandığı süre, toplanmanın devam ettiği durumla ilgili bildirim ile.
11. Veriler ilk kez geliştirme sırasında kullanılmış tarihler.
12. Sistemin sentetik veri üretimi kullanıp kullanmayacağı veya sürekli kullanmayacağı.

12. madde (sünetik veriler) Gebru et al. 2018 verilerinin yeni bir parçasıdır. 7. madde (kişiye ait bilgiler) Gizlilik Hakları Yasası (CPRA) yükümlülüklerini tetikler. Kanun güvenlik/integritesi, uçak operasyonu ve sadece federal ulusal güvenlik sistemlerini (Bölüm 3111(b)) istisna eder.

### AB AI Yasası (Denevi 24) ve TDM'den çıkış

Avrupa Birliği Telif Hakları Direktifi'nde metin ve veri madenciliği istisna, hak sahibi seçilmedikçe halka açık içerikler üzerine eğitim vermeyi sağlar. AB AI Yasası GPAI Uygulama Kodu Telif Hakları bölümünde GPAI sağlayıcılarının makine okuyabilir seçilme sinyalleri (robots.txt, C2PA "AI eğitimsizin" iddiası vb.)

### 2025 DPA'nın meşru çıkarlara dayalı bir yakınlaştırılması

İrlanda DPC (21 Mayıs 2025): Meta'nın ilk taraf kamu içerikleri için eğitim planı, EDPB'nin görüşünden sonra korumalarla kabul edilen AB/Aİ yetişkin kullanıcıları içerikleri. Köln Yüksek Bölge Mahkemesi (23 Mayıs 2025) Meta'ya karşı bir karar verme kararı reddetti: İstifa etmek yeterlidir. Hamburg DPA, AB genelinde tutarlılık için acillik prosedürünü kaldırıyor. UK ICO (23 Eylül 2025) LinkedIn'in benzer güvenlik önlemleri ve sürekli izleme ile AI eğitiminin yeniden başlatılmasına olumlu bir düzenleyici yanıt verdi.

Dönüştürücü ilke: meşru bir ilgi, kamuya açık ilk taraf içerikleri üzerine eğitim yapmayı onaylamayı haklı çıkarabilir.

### Brezilya ANPD (Haziran 2024)

Meta'nın, Yapay zeka eğitimi için Brezilya kullanıcı verilerini işlemeyi yetersiz bilgi şeffaflığı nedeniyle durdurdu.

> **【中文解读】**Çözümsellik sorunu:Cookie 同意框架为实时、可逆的跟踪设计──训练数据不同 once data enters model weight, surgical erasure impossible──从头重新训练是唯一完整补救措施,且成本过高──部分补救措施包括:遗忘(近似移除,通过MIA 衡量)、影响函数定位(识别最受影响的数据权重并选择性更新)、微调抑制(训练模型拒绝从该数据衍生的输出) ⋅

### Geri dönüşülemezlik sorunu

Cookie-izdiyan gerçek zamanlı, geri dönüşümlü izleme için tasarlanmıştır. Eğitim verileri farklıdır: veriler model ağırlıklarına girdiğinde, cerrahi silme mümkün değildir.

Bölümsel düzeltmeler:
- **Unlearning.**Yaklaşık çıkarma; MIA ile ölçülmüştür (Denevi 22).
- **Influence function-based localization.**Verilerden en çok etkilenen ağırlıkları belirleyin; seçici olarak güncelleyin.
- **Fine-tune-suppression.**Model'i verilerden elde edilen çıkışları reddetmeye eğit.

Hiçbirisi sorunu tam olarak çözmedi.

> **【拓展：数据来源倡议 → AI 公地萎缩】**Data Provenance Initiative (dataprovenance.org) tarafından yayınlanan "Crisis Consent" (Krizde İzin Vermek) (July 2024) bulguları: Yayıncılar hızla robotlar ekliyor.

### Veriler Kaynağı Girişimi

dataaprovenance.org. Longpre, Mahari, Lee et al. "Krizde Rıza" (Yül 2024): AI eğitim verileri ortaklarının büyük ölçekli denetimi. Bulma: Yayıncılar robots.txt kısıtlamalarını hızla ekliyor. Açıkça eğitimli ortaklıklar hızla küçülüyor. 2023 -> 2024'te en iyi eğitim kaynaklarının yaklaşık %25'i bazı kısıtlamalar ekledi. Etkisi: Gelecekteki eğitim verileri kullanılabilirliği yeni satın alma paradigmalarına (lisanslama, sentetik üretim, teşvikli katılım) bağlıdır.

### Bu 18 fazaya uygun.

Ders 26 model düzeyde belgeler. Ders 27 veri kümesi düzeyinde yönetim. Birlikte şeffaflık katmanı tanımlar. Ders 28 bu soruları üzerinde çalışan araştırma ekosistemini haritalar.

> Ders 26 model sınıfı dosyalarıdır. Ders 27 veri kümesi sınıfı yönetimi.

> **【拓展：巴西 ANPD → 不同监管结果】**Brezilya ANPD(2024 yılının Haziran ayında) bilgi şeffaflığı eksikliği nedeniyle Meta'nın Brezilya kullanıcı verileri için AI eğitiminin işlenmesi için yapılan çalışmaları durdurdu. AB DPA'nın sonuçları ile farklıydı.

## Kullanın Kullanın
```figure
an-provenance-oneway
```

## Kullan

`code/main.py`Oyuncak verileri için California AB 2013 uyumlu 12 alan veri kümesi özetli bir heyet oluşturur. Alanları doldurabilir ve hangisinin gizlilik veya telif hakkı takip yükümlülüklerini tetiklediğini gözlemleyebilirsiniz.

> `code/main.py`Oyuncaklar için bir veri kümesi oluşturmak California AB 2013'e uygun bir 12 bölüm veri kümesi özetleri.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-provenance-check.md`. Eğitimde kullanılan bir veri kümesi göz önüne alındığında AB 2013 12 alan kapsamını, seçme altyapısının uygunluğunu, DPA'nın uyumluğunu ve geri dönüşü olmayan risk değerlendirmesini kontrol eder.

> 本课产 出 `outputs/skill-provenance-check.md`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊                                                                                                                                                                                                                                          

## Egzersizler.

1. Çık .`code/main.py`. Oyuncak verileri için 12 alanın özetini oluşturun ve hangi alanların az belirtilen olduğunu belirleyin.

2. AB Telif Hakları Direktifi TDM'den çıkma makine okuyabilir. Seçim dışı sinyal için standart bir biçim önerin ve robot.txt ve C2PA "AI Eğitim Yok" ile karşılaştırın.

3. Veriler Kaynağı Girişimi'nin "Krizde Rıza" ( Temmuz 2024) adlı makalesini okuyun. En hızlı kısıtlayıcı üç içerik kategorisini açıklayın ve bir ekonomik sonuçta tartışın.

4. 2025 DPA uyumluluğu, kamu içerikleri eğitimi için meşru bir ilgiyi kabul eder. meşru bir ilgi yeterli olmayacak bir senaryo oluşturur ve yerine bir sağlayıcıya ihtiyaç duyacak yasal temelleri belirler.

5. Her veri kümesi için AB 2013 alanları ve C2PA imzalı bir kaynak zinciri ile oluşan bir eğitim veri kaynak manifesti çizin.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| AB 2013 | "the California law" | Generative AI training-data transparency; 12 mandated fields |
| TDM exception | "text-and-data-mining" | EU Copyright Directive training-data exception with opt-out |
| Legitimate interest | "the EU basis" | GDPR Article 6 basis that may justify training on public content |
| Opt-out signal | "machine-readable no-train" | robots.txt, C2PA "No AI Training," TDM.Reservation |
| Irreversibility | "cannot un-train" | Data in model weights is not surgically removable |
| Unlearning | "approximate removal" | Post-training interventions to reduce model dependence on specific data |
| Consent in Crisis | "the DPI audit" | July 2024 finding of accelerating robots.txt restrictions |

## Daha fazla okumak

- [California AB 2013](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB2013) Genereatif Yapay zeka eğitimi - Verilerin Şeffaflığı Yasası
- [EU AI Act + GPAI Code of Practice (Lesson 24)](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) Telif hakkı bölümü
- [Longpre, Mahari, Lee et al. — Consent in Crisis (dataprovenance.org, July 2024)](https://www.dataprovenance.org/consent-in-crisis-paper) DPI denetimi
- [IAPP — EU Digital Omnibus GDPR amendments (2025)](https://iapp.org/news/a/eu-digital-omnibus-amendments-to-gdpr-to-facilitate-ai-training-miss-the-mark) Yönetim bağlamı
