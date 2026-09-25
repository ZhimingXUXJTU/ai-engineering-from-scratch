# OpenAI Hazırlık Çerçeve ve DeepMind Sınır Güvenlik Çerçeve .

> OpenAI Hazırlık Çerçeve v2 (Epril 2025) Araştırma Kategorilerini  Uzun mesafeli özerklik, Kum çantası, özerk kopyalama ve uyarlama, korumaları bozan  izlenen kategorilerden farklı olarak tanıttı. İzlenen Kategoriler, Güvenlik Danışmanlık Grubu tarafından incelenen yetenek Raporları ve Güvenlik Raporları ile tetiklenir. DeepMind'in FSF v3 (Eylül 2025, 17 Nisan 2026) kendiliğinden ML R&D ve Siber alanlarına katılır (ML R&D kendiliğindenliği seviyesinin 1 = rekabetçi maliyet vs. insan + AI araçları ile AI R&D borusunu tamamen otomatikleştirir). FSF v3, araçsal akıl yürütme yanlış kullanımını otomatik izleme yoluyla yanıltıcı bir ayarlama ile açıkça ilgilenir. Dürüst bir not: PF v2'deki Araştırma Kategorileri (Uzun Aralıklı Otonomisi dahil) otomatik olarak hafiflemeleri tetiklemez; politika dili "potansiyel".

> **【中文解读】**Bu bölümde, her önde gelen AI 实验室 安全框架 Antropik RSP OpenAI Preparedness DeepMind FSF 


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-framework decision-table diff tool) | **语言:** Python（标准库，三框架决策表差异工具）
**Prerequisites:** Phase 15 · 19 (Anthropic RSP) | **前置知识:** Phase 15 · 19（Anthropic RSP）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**Öte yandan, bu süreçte, bir çok insan tarafından yapılan araştırmalara göre, bu süreçte, bir çok insan tarafından yapılan araştırmalara göre, bu süreçte, bir çok insan tarafından yapılan araştırmalara göre, bu süreçte, bir çok insan tarafından yapılan araştırmalara göre, bu süreçte, bir çok insan tarafından yapılan araştırmalara göre, bu süreçte, bir çok insan tarafından yapılan araştırmalara göre, bu süreçte, bir çok insan tarafından yapılan araştırmalara göre, bu süreçte, bir çok insan tarafından yapılmış olan bir çalışma, bir çok insan tarafından yapılmış olan bir çalışma, bir çok insan tarafından yapılmıştır.
>  **【类比】**Üç büyük laboratuvar RSP karşılaştırma = "三家航空公司的安全手册"。Antropic = 严格但商业压力大(删暂停);OpenAI = 双轨(Tracked 严格+Research 灵活);DeepMind = 域整合(自主性折折 into ML R&D 和网络安全)。
> 🤔 **【困惑】**S: RSP'ler neden gönüllü bir sözleşme? Çünkü zorunlu bir yasa yok. AB AI Yasası ilk bölgesel yasa ancak sadece AB'yi kapsar.

## Sorunlar. Sorunlar.

Ders 19 Anthropic'in ölçeklendirme politikasını yakından okudu. Bu ders, OpenAI'nin ve DeepMind'in resimlerini okuyarak resmi tamamlıyor. Üç belge aynı soruyu ele alan kuzeni eserlerdir  bir sınır laboratuvarı ne zaman durmalı veya bir model kapısı olmalıdır  ve küçük bir kategoride bir araya gelerek ve önemli olan belirli yerlerde farklılık gösterirler.

> Bölüm 19  Antropik'in genişleme politikasını dikkatlice okudum. Bu ders OpenAI ve DeepMind'in politikasını okuyarak tüm görüntüyü tamamladı. Bu üç dosya aynı kaynaklı bir araçtır. Aynı soruyu yanıtladı.

Dönüşüm: Üçü de uzun mesafeli özerkliği takip edilmeye değer bir kapasite sınıfı olarak etiketlenmiştir. Üçü de aldatıcı davranışları belirli bir risk sınıfı olarak kabul ediyor. Üçü de iç bir inceleme organına sahiptir. Ayrılık: OpenAI kategorileri "İzlenmiş" (mümkün hafifletme) ve "Araştırma" (otomatik tetikleme yapılmamış) olarak bölüyor. DeepMind, kendi kendine isim vermek yerine, iki alanı özerklikle birleştirir. Laboratuvarlar Tracked vs Research veya Critical vs Moderate veya Tier-1 vs Tier-2 isimlerini kullanır. Bir yetenekin içinde yaşadığı operasyonel sonuçlar laboratuvarlar arasında farklıdır.

> 收点: 三者都将长程自主标记为值得跟踪的能力类别──三者都承认欺诈行为──对齐伪装、sandbagging) 是特定风险类别──三者都有内部审查机构──分歧点:OpenAI将类别分为"Tracked"(强制缓解) 和"Research"(无自动触发)──DeepMind 自主性将折叠到两个领域而非单独命名──实验室名称 Tracked vs Research、Critical vs Moderate、Tier-1 vs Tier-2;能力桶的运营后果在实验室间不同──

Bu özellikler arasında, Anthropic'de "mümkün hafifleme", OpenAI'de "önerleme yapılması, ancak tetikleme yapılması" ve DeepMind'de "belirli bir alanda izlenmesi" de yer alabilir.

> Bu, aynı antropoloji becerilerinin "zorbanlı hafifleme" olarak kullanılmasıdır, OpenAI'de "genceleme ama etkileme" olarak kullanılmasıdır, DeepMind'de "belirli bir alanda takip etmek" olarak kullanılmasıdır.

## Konsepten bir şey.

### OpenAI Hazırlık Çerçevi v2 (Epril 2025)

Yapı:

> 结构:

- **Tracked Categories**Bu, bir diğer önemli gelişme olarak görülüyor.
  Çeviri:**Tracked Categories（跟踪类别）**Bu nedenle, bu durumun önümüze geçmesi için, bu durumun önüne geçmek için, bir güvenlik danışmanlığı grubu tarafından yapılan bir inceleme yapılması gerekmektedir.
- **Research Categories**: laboratuvarın takip ettiği ancak henüz belirli azaltmalara bağlı olmayan model yetenekleri.
  Çeviri:**Research Categories（研究类别）**: Laboratuvar takip ediliyor ama henüz belirli bir hafifleme modeli yeteneğini belirlemeyi taahhüt etmemişlerdir.

V2'de anahtar çerçeve: Araştırma Kategorileri otomatik olarak hafiflemeleri tetiklemez. Politika dili "potansiyel" hafiflemelerdir. Bu izlemek için özel bir delta: Takip edilen vs Araştırma'da bir kategorinin yeri "kapalı" ve "otardığı" arasındaki bir sarmalıktır.

> v2'nin anahtar çerçevesinde: Araştırma Kategorileri 不自动触发缓解――政策语言是"潜在"缓解――这是关注的具体差异:一个类别在追踪还是研究位置是"门控"和"观察"之间的链――

### DeepMind Frontier Güvenlik Çerçevi v3 (Eylül 2025; 17 Nisan 2026'da izlenilen yetenek seviyeleri eklendi)

Yapı:

> 结构:

- **Critical Capability Levels (CCLs)**: beş alan boyunca yetenek eşiği: Siber, Biyolojik, ML Araştırma ve Geliştirme, CBRN, Otonomya (M.L. Araştırma ve Geliştirme ve Siber)
  Çeviri:**Critical Capability Levels（CCL，关键能力等级）**:跨五个领域的能力值:网络、生物、机器学习研发、CBRN、自主性(folding to machine learning研发和网络中)
- **Tracked Capability Levels**Ek olarak Nisan 2026'da ek bir granularlık. Konkret örnek: ML R&D özerkliği seviye 1 = rekabetçi maliyet karşılığında AI R&D borusunu tamamen otomatikleştirme karşılığında insan + AI araçlar.
  Çeviri:**Tracked Capability Levels（跟踪能力等级）**:2026 yıl 4 月 追加额外粒度──具体例:机器学习研发自主级 1 = 以与人类+AI 工具竞争的成本完全自动化AI 研发管道──
- **Deceptive alignment monitoring**: araçsal akıl kullanımı kötüye kullanılması için otomatik izleme konusunda açık bir taahhüt.
  Çeviri:**欺骗对齐监控**: Yüklü araçların kullanımına yönelik otomatik izleme konusunda açık bir taahhüt

Özerklik çerçevesinin OpenAI'den farklı olması. DeepMind "Özerlik" i üst düzey bir alan olarak tutmaz; özerklik zarar verecek alanlara (ML R&D ve Cyber) katlanır.

> Özgürlük çerçevesinin OpenAI ile farklı olmasıdır. Derin Düşünce, "özgürlük" i üst düzey alan olarak koruyacak; özgürlük zararlı alanlara çarpıştıracak.

### Üçün de birleştiği

- İç Güvenlik Danışman Grubu (Anthropic SAG, OpenAI SAG, DeepMind iç komitesi olarak adlandırılır). Yüksek kapasiteli modeller için kullanımdan önce inceleme yapılır.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Ç Çeviri Çeviri Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Yanlış bir ayarlama / ayarlama sahteliği risk sınıfı olarak açıkça belirtilmiştir.
  Çinçe Çevirimiçi:明确提及欺骗对齐/对齐伪装作为风险类别──
- Açıklanan bir kadens üzerinde kalıcı eserler (Antropik: Sınır Güvenliği Yol Haritası, Risk Raporu; OpenAI: Yetenekler ve Koruma Raporları; DeepMind: FSF güncelleme döngüsü).
  Çinçe Çevirisi:                                                                                                                                                                                                                                                            
- Sadece izleme savunmalarının bir tavanın olduğunu kabul etmek. DeepMind açıkça: "otomatik izleme uzun vadede yeterli olmayacak".
  Çin dilinde: "Automatisiyalı izleme uzun süreliğine yeterli olmayacak" diyor.

### Farklı yerlerde

- **Anthropic**: v3.0'da duraklı yükümlülük kaldırıldı; AI R&D-4 eşiği, bir sonraki kapı olarak adlandırıldı.
  Çeviri:**Anthropic**:v3.0 移除暂停承诺;AI R&D-4 值是命名的下一个门控──
- **OpenAI**: İzleyici vs Araştırma bölümü; Araştırma Kategorileri (Uzun Uzakluk Özerklikleri dahil) otomatik olarak geçit geçmez.
  Çeviri:**OpenAI**:Tracked vs Research 分割;Tahlil Kategorileri(include长程自主)不自动门控──
- **DeepMind**: özerklik diğer alanlara katıldı; takip edilen yetenek seviyeleri Nisan 2026'da granularlık ekliyor.
  Çeviri:**DeepMind**: Özgürlük diğer alanlara çarpma; 2026 yılında 4 aylık artırılmış kapasite seviyeleri takip edilmektedir.

### Kum çantası: üçü de karmaşıklaştıran belirli bir yetenek

Sandbagging (değerlendirmelerde stratejik olarak düşük performans gösteren bir model) OpenAI'nin Araştırma Kategorilerinde bulunmaktadır. Anthropic'in RSP v3.0 değerlendirme- bağlam boşluğu (Desin 1). DeepMind FSF v3'te yanıltıcı bir uyum izleme yoluyla bu sorunları ele alır.

> Sandbagging (模型在评估中战略性表现不佳) (OpenAI'nin Araştırma Kategorileri arasında).Antropik RSP v3.0 通过评估上下文差距 (第 1 课)处理──DeepMind 通过 FSF v3 的欺骗对齐监控处理──

Eğer bir model değerlendirme üzerinde kum çantaları varsa, her çerçeve'nin kapasite eşiği küçümselir. Çerçeve yalnızca ölçümün işe yaraması durumunda çalışır. Bu nedenle laboratuvar kendiliğinden değerlendirilmesi dışında dış ölçüm (Denevi 21, METR) ve karşıt değerlendirme gereklidir.

> Eğer model değerlendirilmişse, her çerçeve kapasitesinin değerleri küçülür. Çerçeve sadece ölçümde geçerli olduğunda geçerlidir. Bu nedenle, laboratuvarın kendi kendini değerlendirmesinden başka, dış ölçümlerin (METR) ve karşı değerlendirmenin gerekliliği vardır.

### Politikayı okumak becerisi

- Bul: ilgilendiğiniz her yetenek poliçede bulunmalıdır.
  Çeviri:**定位**Politikada bulunması gereken her bir yetenek bulunur.
- Sınıflandır: izlenmiş mi (dönüştürme azaltımı) yoksa araştırma mı (izlenmiş mi, tetiklemeci değil)? OpenAI buna isim verir; Anthropic ve DeepMind'in kendi eşdeğerleri vardır.
  Çeviri:**分类**Bu nedenle, bu tür bir araştırma yapılması için, bu tür bir araştırma yapılması gerekir.
- Cadence: politika açıklanan bir zaman çizelgesinde güncelleştiriliyor mu, yoksa sadece belirli olaylardan sonra mı?
  Çeviri:**节奏**Politikası açıklama planı güncelleştirilmiş mi, yoksa sadece belirli olaylardan sonra mı?
- Bağımsızlık: dış inceleme zorunlu mu yoksa seçmeli mi? Apollo ve ABD AI Güvenlik Enstitüsü ile antropik ortaklar; METR ile OpenAI; iç SAG ile öncelikle DeepMind.
  Çeviri:**独立性**Dış inceleme zorunlu mu yoksa seçilebilir mi?Antropik Apollo ve ABD AI Güvenlik Enstitüsü ile işbirliği;OpenAI ve METR  işbirliği;DeepMind esas ve iç SAG¬¬lar

## Çerçeveyi kullanın.
```figure
a5-tracked-vs-research
```

## Kullan

`code/main.py`Bu, bir bilgi kaynağı olarak kullanılır ve bir bilgi kaynağı olarak kullanılır. bu bilgi kaynağı, bir bilgi kaynağı olarak kullanılır.

> `code/main.py`Küçük karar verme biçimindeki farkı gerçekleştirmek için bir araçtır.Özgürlük, aldatmacılık, gelişmiş otomasyon, ağ güçlendirme ve diğerleri için bir güç oluşturmak için üç politika çıkarmak, bu yetenekleri nasıl sınıflandırır ve hangi hafiflemeleri başlatmak için bir araçtır.

## İndirin . Ürünler .

`outputs/skill-cross-policy-diff.md`Üç çerçeveyi referans olarak kullanarak belirli bir kapasite için politikalar arası bir karşılaştırma yapar.

> `outputs/skill-cross-policy-diff.md`Özellikle de, üç çerçeveyi kullanarak politika karşılaştırma yapma kapasitesini oluşturmak için bir referans olarak kullanılır.

## Egzersizler.

1. Çık .`code/main.py`. Farklı araçların çıktısının kaynak belgelere karşı doğrulanabilecek en az iki özellik için politikalara uymasını onaylayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Farklılıkları Kanıtlama Aracının Çıkışı ve Kaynak Kaynakları Kanıtlama Aracının En Az İki Yetkisiyle Uygunlaşır.

2. OpenAI Hazırlık Çerçeve v2'yi tamamıyla okuyun. Her Araştırma Kategori'sini tanımlayın. Her biri için, takip edilmektense neden Araştırmada olduğunu bir cümle yazın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Çeviri: Ç Ç Ç Çev

3. DeepMind FSF v3'i tamamıyla okuyun, ayrıca Nisan 2026'da takip edilen yetenek seviyeleri güncelleme. ML R&D özerklik seviyesinin özel değerlendirme kriterlerini belirleyin.
   Çin dilinde: Full reading DeepMind FSF v3 加 2026 yıl 4 月 İzlenen Yetenek seviyeleri 更新。识别机器学习研发自主等级 1 的具体评估标准──你会如何外部测量?

4. Sandbagging OpenAI'nin Araştırma Kategori'sindedir. Sandbagging modelinin gerçek yeteneğini ortaya çıkarmak için zorlayacak bir değerlendirme tasarlayın.
   Çamur Çamaşırcılık, Çamur Çamaşırcılığı, Çamur Çamaşırcılığı, Çamur Çamaşırcılığı, Çamur Çamaşırcılığı ve Çamur Çamaşırcılığı, Çamur Çamaşırcılığı, Çamur Çamaşırcılığı ve Çamur Çamaşırcılığı, Çamur Çamaşırcılığı, Çamur Çamaşırcılığı, Çamur Çamaşırcılığı, Çamur Çamaşırcılığı, Çamur Çamaşırcılığı, Çamur Çamur Çamaşırcılığı, Çamur Çamur Çamaşırcılığı, Çamur Çamur Çamaşırcılığı, Çamur Çamur Çamaşırcılığı, Çamur Çamur Çamaşırcılığı, Çamur Çamur Çamaşırcılığı, Çamur Çamur Çamaşırcılığı, Çamurçamaşırcılığı, Çamurçamaşırcılığı, Çamurçamaşırcılık, Çamurçamaşırcılık, Çamurçamaşırcılık, Çamurçamaşırcılık, Çamurçalama, Çamurçamaşırçlık, Çamurçalama.

5. Özel bir yetenekle ilgili üç politikayı karşılaştırın (seçiminize göre). Hangi politikayı en sıkı ve en azını sınıflandırmayı bulduğunuzu belirleyin. Kaynak metni ile haklı gösterin.
   Çinçe Çevirimiçi:Comparison Three policies dans une spécifique capacité (), ︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| Preparedness Framework | "OpenAI's scaling policy" | PF v2 (April 2025); Tracked vs Research categories | OpenAI 准备度框架：PF v2，Tracked vs Research |
| Tracked Category | "Mandatory mitigation" | Triggers Capabilities + Safeguards Reports; SAG review | 跟踪类别：触发能力+防护报告，SAG 审查 |
| Research Category | "Monitored only" | Tracked but no automatic mitigation; includes Long-range Autonomy | 研究类别：跟踪但不自动缓解，含长程自主 |
| Frontier Safety Framework | "DeepMind's scaling policy" | FSF v3 (Sept 2025) + Tracked Capability Levels (Apr 2026) | DeepMind 前沿安全框架 |
| CCL | "Critical Capability Level" | DeepMind threshold per domain (Cyber, Bio, ML R&D, CBRN) | 关键能力等级：DeepMind 各领域阈值 |
| ML R&D autonomy level 1 | "R&D automation" | Fully automate AI R&D pipeline at competitive cost | 机器学习研发自主等级 1：完全自动化研发管道 |
| Sandbagging | "Strategic underperformance" | Model underperforms on evals; in OpenAI Research Categories | Sandbagging：模型战略性表现不佳 |
| Instrumental reasoning | "Means-ends reasoning" | Reasoning about how to achieve goals; target of DeepMind monitoring | 工具性推理：DeepMind 监控目标 |

## Daha fazla okumak

- [OpenAI — Updating our Preparedness Framework](https://openai.com/index/updating-our-preparedness-framework/)V2 duyuru.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [OpenAI — Preparedness Framework v2 PDF](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf) Tam belge.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [DeepMind — Strengthening our Frontier Safety Framework](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/)FSF v3 duyuru.
  Çeviri: FSF v3 公告
- [DeepMind — Updating the Frontier Safety Framework (April 2026)](https://deepmind.google/blog/updating-the-frontier-safety-framework/) İzlenen Yeteneklilik Doluları eklenmesi.
  中文翻译:Sahitlik seviyeleri 添加
- [Gemini 3 Pro FSF Report](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_fsf_report.pdf) FSF biçimindeki Risk Raporu örneği.
  Çinçe Çevirimi:FSF 格式风险报告 örnek
