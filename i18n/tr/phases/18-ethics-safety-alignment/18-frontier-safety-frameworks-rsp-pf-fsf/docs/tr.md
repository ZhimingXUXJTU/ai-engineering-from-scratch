# Sınır Güvenlik Çerçeveleri  RSP, PF, FSF   framework Ön kenar Güvenlik RSP

> Üç büyük laboratuvar çerçevesinde, 2026 yılına kadar sınır kapasitesinin endüstri yönetimi tanımlanır. Anthropic Responsible Scaling Policy v3.0 (Febrúar 2026) biyolojik güvenlik seviyelerine dayalı dereceli AI Güvenlik Denizeleri (ASL-1'den ASL-5+'ye kadar) tanıttı. OpenAI Hazırlık Çerçevi v2 (Epril 2025) izlenen yetenekler için beş kriter tanımlar ve yetenek raporlarını güvenlik raporlarından ayırır. DeepMind Frontier Güvenlik Çerçeve v3.0 (Eylül 2025) yeni zararlı manipülasyon CCL'yi içeren kritik yetenek seviyelerini tanıttı. Şimdi üçü de rakip düzenleme şartlarını içerir. Eğer eşdeğer laboratuvarlar benzer korumalar almadan gemiyi gönderirse ertelenmeyi sağlar. Laboratuvar çapındaki uyumlama yapısal olarak kalır, terminolojik olarak değil: "Yeteneklilik Eğitimi", "Yüksek Yeteneklilik Eğitimi" ve "Kritik Yeteneklilik Denizi" benzer yapılandırmalar gösterir.

> **【中文解读】**Bu bölüm ön kenar güvenlik çerçevesini tanıtıyor Antropik RSP、OpenAI Hazırlık、DeepMind FSF等 güvenlik çerçevesine karşılaştırmalar。 Üç laboratuvar çerçevesinin 2026 yılının ön kenar kapasite endüstri yönetimiyi tanımlaması。ASL-3 2025 yılının Mayıs ayında CBRN 関連モデルに激活用された。 güvenlik örneği ise, test deployment'da en kötü durum ihtimalinde güvenliğin kabul edilebilir olup olmadığı konusunda bir makale temsiliyor。

> **【拓展：竞争调整条款 → 竞赛动态】**Tüm üç çerçeve, rekabet düzenleme maddelerini içerir. Rekabetçilerin karşılaştırılabilir garanti önlemleri olmadığı durumlarda gönderme saatinde gecikmesine izin verir. Eleştirmenler bunun rekabet temelini oluşturduğunu düşünüyor: Eğer üç laboratuvar rekabetçilerin karşılamasındaki taleplerin azaltılması, dengenin karşılaşma yönündeki etkisiyle değişmesi.

**Type:** Learn | **类型:** 学习
**Languages:** none | **语言:** 无
**Prerequisites:** Phase 18 · 17 (WMDP), Phase 18 · 07-09 (deception failures) | **前置知识:** Phase 18 · 17 (WMDP), Phase 18 · 07-09 (欺骗失败)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Öğrenci bölümün önüne geçerek:Fase 18·17(WMDP)、Fase 18·07-09(欺骗三角)。三大前沿实验室安全框架横向对比(与Fase 15·19-20 互补)。
>  **【类比】**Güvenlik çerçeve = "AI 实验室的生物安全等级"──Anthropic RSP v3.0(ASL-1 to ASL-5+, BSL 生物安全类似);OpenAI PF v2(5 跟踪能力+能力报告/保障报告分离);DeepMind FSF v3(关键能力等级+操纵 CCL)──ASL-3 已 2025.5 激利用于 CBRN──三家都加"竞争调整"条款若行无类似保障可暂缓──

## Öğrenme hedefleri

- Anthropic'in ASL katman yapısını ve ASL-3'ü neyin aktive ettiğini açıklayın.

> 描述 Antropic'in ASL seviyesi yapısı ve ASL-3'yi nasıl aktive ettiğini

- İzleme yetenekleri için beş OpenAI Hazırlık Çerçevi v2 kriterini belirtin.

> 列出 OpenAI Preparedness Framework v2  takip kabiliyetinin beş kriteridir.

- DeepMind'in Kritik Yetenek Duruşumu ve Zararlı Manipülasyon CCL'si'ni açıklayın.

> DeepMind'in anahtar yetenekleri, yapı ve zararlı yönlendirmeler

- Rekabetçi ayarlama klauzüllerini ve yarış dinamikleri için neden önemli olduğunu açıklayın.

> ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐

- Güvenlik kapısını tanımlayın ve üç sütunlu yapıyı (öneticilik, okumayı engelleme, yetersizliği) açıklayın.

> 定義安全案例并描述三支柱结构(監控、不可讀性、無能)

## Sorun . Sorun .

Dersler 7-17 aldatmanın mümkün olduğunu, çift kullanım kabiliyetinin var olduğunu ve değerlendirme sınırlarının olduğunu belirler. Sınırlara uygun bir model olan bir laboratuvarın, aşağıdakileri içeren bir yönetim yapısına ihtiyacı vardır:
- Yeni garantilerin gerekli olduğu için eşiği belirler.
- Ölçeklendirme öncesi gerekli değerlendirmeyi tanımlar.
- Güvenlik kafasının nasıl olduğunu anlatıyor.
- Yarış dinamik problemini ele alır (renişçiler koruma olmadan gemiyi açarsa ne yaparsınız?).

> Ders 7-17: Yalancılığın mümkün olduğunu belirler, ikili kullanım yeteneğinin varlığını belirler, sınırlı değerlendirir, ön kenar yetenek modeline sahip olan laboratuvarların iç yönetim yapısı gerektirir: yeni garanti değerinin ne zaman gerektirdiğini tanımlar, genişleme ön gereksinimlerinin değerlendirilmesini belirler, güvenlik durumlarının örneği, rekabet dinamikleri sorunu oluşturur.

2025-2026 dönemindeki üç çerçeve, gelişmekte olan ve laboratuvarlar arasında yeterince uyumlu olan son teknoloji  kusurlu ve gelişmekte olan çerçeveler, yönetim sorusunun şimdi mevcut olup olmadığını değil, çerçevelerin yeterli olup olmadığını sormaktadır.

> Üç 2025-2026 çerçevesinin en gelişmiş teknolojisi  kusursuz  gelişmekte  laboratuvarlar arasında yeterince uyumlu, yönetim sorunu şimdi çerçevesin yeterli olup olmadığını ve olup olmadığını oluşturmaktadır.

## Konsep kavramı.

> **【中文解读】**Anthropic RSP v3.0'un ASL  yapısı:ASL-1 非前沿模型;ASL-2 当前前前沿基线;ASL-3 大幅更高的灾难性滥用风险(CBRN),2025年 5月激活;ASL-4 AI R&D-2 跨越值(可自动化进入级 AI 研究);ASL-5+ 高级 AI R&D(大幅加速有效扩张)

### Antropik Sorumlu Ölçekleme Politikası v3.0 (Feb. 2026)

ASL yapısı:
- ASL-1: sınır modeli değil (sınırdan zayıf bir temel çizgi ile toplamlanmıştır).
- ASL-2: mevcut sınır başlangıç çizgisi; normal güvenlik önlemleri ile uygulanmaktadır.
- ASL-3: felaketli kötüye kullanma riski önemli ölçüde daha yüksek; CBRN ile ilgili yetenekler.
- ASL-4: AI R&D-2 geçme eşiği; girişim düzeyinde AI araştırmasını otomatikleştirebilecek modeller.
- ASL-5+: etkili ölçeklendirmeyi çarpıcı bir şekilde hızlandıran gelişmiş AI R&D; modelleri.

> ASL struktur:ASL-1 非前沿模型;ASL-2 当前前沿基线;ASL-3 大幅更高的灾难性滥用风险(CBRN),2025年 5 月激活;ASL-4 AI R&D-2 跨越值;ASL-5+ Yüksek Sınıflı AI R&D──

3.0'da yeni:
- Sınır Güvenliği Yol Haritaları (sözlenmiş biçimde halka açık).
- Risk Raporları (tört yılda bir, bazılarının dıştan gözden geçirilmesi).
- AI R&D, AI R&D-2 ve AI R&D-4'e ayrıştırılmıştır.
- AI R&D-4'i geçtikten sonra, yanlış uyumlu hedefleri takip eden modellerden yanlış uyum sağlama risklerini belirleyen bir onaylı güvenlik durumu gerekmektedir.

> v3.0 Yeni gelişme: Ön kenar güvenlik yolu çizelgesi (www.proto.org) 季度风险报告 (www.proto.org) 部分外部审查) 、AI R&D 分割 R&D-2 和 R&D-4、R&D-4 跨越后需要肯定性安全案──

> **【拓展：OpenAI PF v2 → 五项追踪标准】**OpenAI'nin 5 takip kabiliyet standartları: 1) makul  varlığı makul tehdit modeli; 2) ölçülebilir  deney değerlendirme mümkün; 3) ciddi  zarar büyük; 4) net yeni  risk arttırılmamış; 5) anlık veya telafi edilemez  zarar hızla meydana gelmek veya geri çekilmemek için;

### OpenAI Hazırlık Çerçeve v2 (15 Nisan 2025)

Takip edilen yetenekler için beş kriter:
- **Plausible.**Makul bir tehdit modeli var.
- **Measurable.**Empirik değerlendirme mümkün.
- **Severe.**Zarar çok büyük.
- **Net-new.**Daha önce var olan bir risk değil.
- **Instantaneous-or-irremediable.**Zarar hızlı bir şekilde olur veya telafi edilmez.

> 追踪能力の五つの基準: 合理的、可測量的、严重的、純新的、即時的、不可补救的、

Beş kişiyi de karşılayan yetenekler izlenir.

> 满足所有五项的能力被追踪,其他不追踪──

Diğer PF v2 yapısı:
- Kapayolu Raporları (modelin yapabileceği şeyler) ve Koruma Raporları (kontrollerin varlığı) için ayrı.
- Güvenlik Danışmanlık Grubu'nun incelemeleri.
- Yönetim onaylıyor; Kurul Güvenlik ve Güvenlik Komitesi gözetim yapıyor.
- "Düzeltme klazuli": OpenAI, diğer laboratuvar gemileri karşılaştırılabilir güvenlik önlemleri almıyorsa gereklilikleri azaltabilir.

> PF v2 其他结构: ayrılık kapasitesi rapor ve güvence rapor, güvenlik danışmanlık grubu inceleme, liderlik onayları, yönetim kurulu güvenlik komitesi gözetimi, "调整条款"

### DeepMind Sınır Güvenlik Çerçeve v3.0 (Eylül 2025)

Bölümler açısından kritik kapasite seviyeleri (CCL):
- Biyolojik Silahların Yüklenmesi
- Siber Yüklenme
- ML Araştırma ve Gelişim Hızlandırması
- Zararlı Manipülasyon (v3.0'da yeni): yüksek riskli bağlamlarda inançları / davranışları önemli ölçüde değiştirebilecek modeller.

> 按领域关键能力级别(CCL): Biyoarms提升、网络提升、ML R&D 加速、有害操纵(v3.0 新增)

V2.0 (Feb. 2025) bir aldatıcı uyum bölümünü ve ML R&D CCL'ler için daha yüksek güvenlik seviyelerini ekledi.

> 2.0'da dolandırıcılık ve ML R&D CCL'nin daha yüksek güvenlik seviyesini ekledi.

### Laboratuvar çaplı uyum

- Antropik "Kapalet Eğitimi".
- DeepMind "Kritik yetenek seviyeleri".
- OpenAI "Yüksek Yeteneklilik Eğitimi".

> Antropik "Yeteneklilik Eğitimi"、Dünyet "Kritik Yeteneklilik Denizi"、OpenAI "Yüksek Yeteneklilik Eğitimi"──

Endüstri standartları için terminoloji yoktur. Struktörel olarak uyumlu: yayınlanmış değerlendirme kriterleri ile sınır kapasitesinin üç seviyesi.

> 没有行业标准术语──结构上对齐:三层前沿能力、发布评估标准、竞争调整条款──

> **【中文解读】**Güvenlik durumları üç sütun yapısı: 1) denetim  Eğer kötü davranışlar olursa, biz bunu tespit edebilir miyiz? 2) okunmaz  model sürekli zarar planı gerçekleştirme yeteneği eksik mi? 3) okunmaz  model ilgili zararlar getirme yeteneği eksik mi?

### Güvenlik kapıları

Güvenlik durumu, en kötü durumlarda bir dağıtımın kabul edilebilir bir şekilde güvenli olduğunu gösteren yazılı bir argümandır.

> Güvenlik örneği, en kötü durumlarda deployment, en kötü durumlarda güvenliğe uygun olup olmadığını varsaymak için yazılı bir çalışma.

- **Monitoring.**Eğer kötü bir davranış olursa onu tespit edebilir miyiz?
- **Illegibility.**Model zarar vermek için tutarlı bir plan yürütme yeteneğine sahip değil mi?
- **Incapability.**Model, söz konusu zararı yaratabilecek yeteneği yok mu?

> **监控：**Eğer kötü bir davranış olursa, bunu kontrol edebilecek miyiz?**不可读性：**模型是否缺乏执行连贯伤害计划的能力?**无能：**模型是否缺乏相关伤害的能力?

Farklı güvenlik vakaları farklı direkleri hedef alır. ASL-3 CBRN vakaları için, yetersizlik (öğrenmeyi bırakmak yoluyla) ana hedefdir. Yanlış uyum, izleme ve okumayı hedefler. Siber yükseltme için, üçü de önemlidir.

> Çeşitli güvenlik durumları farklı sütunlara yöneliktir: ASL-3 CBRN olayları esas olarak güçsüzlere yöneliktir, haksızlıklara yöneliktir ve kontrol ve okunmazlığa yöneliktir, ağ geliştirme üçü de ilgilitir.

### Yarış dinamik problemi

Rekabetçi ayarlama klauzüleri tartışmalıdır. Eleştirmenler, aşağıya bir yarış yarattıklarını savunuyor: rekabetçi kusurlu olduğunda üç laboratuvar da gereklilikleri azaltırsa, denge kaçaklığa doğru kayar. Savunmacılar alternatif (bir taraflı korumalar) kaçakçı laboratuvarın güvenliği konusunda daha az bilinçli olması durumunda daha kötü sonuçlar doğurduğunu savunuyor.

> 竞争调整条款有争议──批评者认为它们创造竞争底:如果三个实验室都在竞争对手违约时减少要求,均衡向违约偏移──维护者认为替代方案(单边保障) 违约实验室安全意识较低时产生更差的结果──

İngiltere AISI, ABD CAISI ve AB AI Ofisi (Denevi 24) dış yönetim eşleri. Laboratuvar çerçeveleri gönüllüdür; düzenleyici çerçeveler ortaya çıkmaktadır.

> Birleşik Krallık AISI, ABD CAISI ve AB AI Ofisi, dış yönetim ve çözüm yöntemleri için gönüllüdür.

### Bu 18 fazaya uygun.

Dersler 17-18, aldatma ve kırmızı takım analizlerinin üstündeki ölçüm ve yönetim katmanıdır. Dersler 19-24 refah, tarafsızlık, gizlilik, su işaretleme ve düzenleyici yapıyı kapsar. Ders 28 değerlendirmeleri işletiyen araştırma ekosistemini (MATS, Redwood, Apollo, METR) haritalar.

> Dersler 17-18: Aldatma ve kırmızı takım analizinin ölçüm ve yönetim seviyeleri. Dersler 19-24: Fayda, Önyargı, Gizlilik, Su ve İzleme yapısı.

> **【拓展：跨实验室对齐 → 结构性而非术语性】**Üç çerçeve terminologie nonconform but structurally on齐:Antropic "Capability Thresholds" = DeepMind "Critical Capability Levels" = OpenAI "High Capability Thresholds"──三层前沿能力、发布评估标准、竞争调整条款结构趋同──英国 AISI, US CAISI 和 EU AI Office (Daabi 24)

## Kullanın Kullanın
```figure
al-asl-ladder
```

## Kullan

Bu ders için kod yok. Üç ana kaynağı okuyun: RSP v3.0, PF v2, FSF v3.0. Her laboratuvarın katman yapısını diğerlerine haritasın ve her laboratuvarın diğerlerinin tanımlamadığı bir eşiği belirleyin.

> Bu ders kodsızdır. Üç ana kaynağı okuyun:RSP v3.0、PF v2、FSF v3.0── her laboratuvarın aşama yapısını diğer laboratuvarlara harekete geçirir ve her laboratuvarın tanımlandığı ancak diğerlerinin bir değersiz olduğunu tanımlar.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-framework-diff.md`. Bir güvenlik çerçevesini veya açıklama notunu göz önünde bulundurarak, çerçevenin eşiğin tanımlarını, gerekli değerlendirmeleri ve güvenlik durumunun yapısını RSP v3.0, PF v2, FSF v3.0 ile karşılaştırır ve laboratuvar çapındaki boşlukları işaretler.

> 本课产 出 `outputs/skill-framework-diff.md` Güvenlik çerçevesini veya yayın açıklamasını belirle, değerlendirmeyi tanımla, değerlendirme ve güvenlik durumunun yapılarını RSP v3.0PF, v2 ̊ FSF v3.0 ile karşılaştır, laboratuvar arasındaki farkı işaretle

## Egzersizler.

1. RSP v3.0, PF v2 ve FSF v3.0'u okuyun. Her laboratuvarın CBRN eşiğinin, her birinin AI araştırma ve geliştirme eşiğinin ve her birinin gerekli görevlendirme öncesi değerlendirmesinin bir tablosunu oluşturun.

2. Rekabetçi ayarlama klazuli üç çerçeve (2025+) de bulunmaktadır. Bunun için bir paragraf yazın; karşı bir paragraf yazın. Her pozisyonun bağlı olduğu varsayımı tanımlayın.

3. Anthropic'in AI R&D-4 eşiğine geçen bir model için bir güvenlik kazası tasarlayın.

4. DeepMind'in FSF v3.0'u zararlı Manipülasyon CCL'yi tanıttı. Bir modelin bu eşiği geçtiğini gösteren üç empiriyel ölçüm önerin.

5. METR'nin "Sınırlı AI Güvenlik Politikası Ortak Elemleri" (2025) 'ni okuyun. En güçlü üç laboratuvar çapındaki birleştiği ve en büyük iki farklılığı isimlendirin.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| RSP | "Anthropic's framework" | Responsible Scaling Policy; ASL tiers; v3.0 February 2026 |
| PF | "OpenAI's framework" | Preparedness Framework; five criteria; v2 April 2025 |
| FSF | "DeepMind's framework" | Frontier Safety Framework; CCLs; v3.0 September 2025 |
| ASL-3 | "biosafety level 3-analog" | Anthropic tier for CBRN-relevant capabilities; activated May 2025 |
| CCL | "critical capability level" | DeepMind's threshold construct; per-domain |
| Safety case | "the formal argument" | Written argument that deployment is acceptably safe under worst-case U |
| Adjustment clause | "competitor defection allowance" | Framework provision for reducing requirements if competitors ship without comparable safeguards |

## Daha fazla okumak

- [Anthropic — Responsible Scaling Policy v3.0 (February 2026)](https://www.anthropic.com/responsible-scaling-policy) ASL seviyeleri, yol hariteleri, AI Araştırma ve Gelişim bölümü
- [OpenAI — Updating the Preparedness Framework (April 15, 2025)](https://openai.com/index/updating-our-preparedness-framework/) Beş kriter, uyumsal hüküm
- [DeepMind — Strengthening our Frontier Safety Framework (September 2025)](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) CCL v3.0, Zararlı Yönetim
- [METR — Common Elements of Frontier AI Safety Policies (2025)](https://metr.org/blog/2025-03-26-common-elements-of-frontier-ai-safety-policies/) Laboratuvarlar arası karşılaştırma
