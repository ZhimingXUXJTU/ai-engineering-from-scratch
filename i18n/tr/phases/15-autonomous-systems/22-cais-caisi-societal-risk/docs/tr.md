# CAIS, CAISI ve Toplumsal Ölçüsünde Risk

> San Francisco'daki AI Güvenliği Merkezi (CAIS, Hendrycks ve Zhang tarafından 2022 yılında kurulan) dört risk çerçevesini yayınlıyor  kötü amaçlı kullanım, AI yarışları, kurumsal riskler, kötü amaçlı AI  ve yüzlerce profesör ve şirket liderinin imzaladığı yok olma riskine ilişkin Mayıs 2023 açıklaması. CAIS'ten 2026'da yayınlanan yayınlar: Sınır model değerlendirmesi için AI Dashboard, Uzak İş İndeksi (Scale AI ile), Süper İstihbarat Stratejisi Kağıdı, AI Sınırları haber bülten. Ayrı bir kurum: NIST AI Standartları ve Yenilikleri Merkezi (CAISI)  ABD hükümetine yönelik gönüllü anlaşmalar ve siber, biyolojik ve kimyasal silah risklerine odaklanan sınıflandırılmamış kapasite değerlendirmeleri. CAIS, kurumsal riskleri dört üst düzey riskten biri olarak belirtiyor: Güvenlik kültürü, katı denetimler, çok katlı savunmalar ve bilgi güvenliği temel ama düzenli olarak dağıtım hızı karşılığında satılır. Eğer imzalanırsa, Kaliforniya SB-53, ABD'de ilk devlet düzeyinde felaket riski düzenlemesi olacaktır.

> **【中文解读】**Bu bölümde CAIS/CAISI'nin sosyal risk değerlendirmesi hakkında bilgi edinilir.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-risk inventory and mitigation matcher) | **语言:** Python（标准库，四风险盘点与缓解匹配器）
**Prerequisites:** Phase 15 · 19 (RSP), Phase 15 · 20 (PF + FSF) | **前置知识:** Phase 15 · 19（RSP）、Phase 15 · 20（PF + FSF）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**Öğrenci bölümünün ilk aşaması: 15·19-20 (Bünyaklar) 实验室 RSP)  15·21 (METR dış departmanının değerlendirme)  本节是"第三视角"民间社会和政府对AI风险的态度──
>  **【类比】**CAIS = "AI 风险的智囊团" (民间研究,发言,推框架);CAISI = "AI 风险的政府办公室" (NIST 下属,协调自愿协议) (BİİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİ
> 🤔 **【困惑】**S: Bu organizasyonlar benim için yapıyorum  AI Engineering ne işe yarar?  直接用途是合规: eğer ürünleriniz yüksek riskli durumlara ilişkinse (medical·金融、招聘), CAIS 框架 for risk assessment (CAIS 框架 for risk assessment) references gerektirir, muhtemelen AB AI Act 、加州 SB-53 等法规则 (EU AI Act 、加州 SB-53 等法规) ⇒修复:建立组织内部安全文化 (organism inside safety culture) ⇒ CAIS 四风险中最可控的"组织风险" (CAIS 四风险中最可控的) ⇒

## Sorunlar. Sorunlar.

Dersler 19 ve 20 laboratuvar içi ölçeklendirme politikalarını kapsamaktadır. Ders 21 bağımsız kapasite değerlendirmesini kapsamaktadır. Bu ders üçüncü bakış açısını kapsar: sivil toplum ve kamuoyu düzenlemelerini ve AI riskini felaketle karşılayan düzenleyici temelini şekillendiren hükümet örgütlerini.

> Bölüm 19 ve 20'ler laboratuvar içi genişleme politikasını kapsar. Bölüm 21 bağımsız yetenek değerlendirmesini kapsar. Bu ders üçüncü bakış açısını kapsar: kamu tartışmalarını ve felaketleri şekillendirmek.

CAIS, AI riskleri hakkında düşünme çerçeveleri yayınlayan ve kamu açıklamalarını koordine eden bir kar amacı gütmeyen araştırma örgütüdür. CAISI, NIST'in içinde gönüllü anlaşmalar yapan ve sınıflandırılmamış kapasite değerlendirmeleri yapan bir ABD hükümet merkezi.

> İki farklı varlık önemlidir. CAIS, AI'nin 风险思考框架并协调公声明的非营利研究组织. CAISI, NIST'deki ABD hükümet merkezi, laboratuvarın gönüllü çalışma anlaşması ve gizli yetenek değerlendirmesi ile birlikte.

Pratik içeriği: CAIS'in dört risk çerçevesinin literatürde en çok alıntılanan toplumsal ölçek risk taksonomisi. Güvenlik kültürü ve örgütsel risk bu dörtten biridir ve bu bir uygulayıcının kontrolü altındaki en doğrudan bir şeydir. SB-53 (Kaliforniya) imza yapılırsa ABD eyalet düzeyinde ilk felaket riski düzenlemesi olacaktır; tasarının çerçevesinde önemli olan, çünkü eyalet düzeyinde düzenleme tarihsel olarak ABD teknolojik politikasında federal eylemlere yol açmıştır.

>  Pratik içeriği:CAIS'in dört risk çerçevesinin, yayınlarda en geniş olarak alıntılanan sosyal ölçek risk sınıfı kurallarıdır. Güvenlik kültürü ve örgüt riskleri, en doğrudan uygulayıcıların kontrolü altındaki birincidir. SB-53 ((Kazova) Eğer imzalanırsa, ilk ABD eyalet düzeyinde felaket risk kontrolü olacaktır. Bu yasayın çerçevesinin önemli olduğu için, eyalet düzeyinde düzenleme ABD teknolojik politikasında tarihinde önde gelen federal eylemdir.

## Konsepten bir şey.

### CAIS  AI Güvenliği Merkezi

- San Francisco'da 2022 yılında Dan Hendrycks ve meslektaşları tarafından kurulmuştur ( "Zhang" adı, mevcut bir ortak kurucu değil, erken bir işbirlikçiyi ifade eder; mevcut liderlik için CAIS web sitesine bakın).
  Çinçe çevirisi:成立:2022年在旧金山,由 Dan Hendrycks 和同事创立("Zhang"指早期合作者,非当前联合创始人;当前领导见 CAIS 网站) 
- Durum: 501 ((c) ((3) kâr amacı gütmeyen kuruluş.
  Çeviri: 501 (c) 3) 非营利。
- Görkemli 2023 sonucu: yüzlerce araştırmacı ve CEO'nun ortak imzaladığı yok olma riskiyle ilgili açıklama. "İS'ten yok olma riskini azaltmak, salgın hastalıklar ve nükleer savaş gibi diğer toplumsal risklerle birlikte küresel bir öncelik olmalıdır" dedi.
  Çin Çeviri: 2023  显著产出:灭绝风险宣言, yüzlerce araştırmacı ve CEO 联合签署──声明:"AI 灭绝风险应应与流行病和核战争等等其他社会规模风险并列作为全球优先──"
- 2026 çıkışları: Sınır model değerlendirmesi için AI Tablosu, Uzaktan İş İndeksi (Scale AI ile birlikte), Süper zeka Stratejisi Kağıdı, AI Sınırları haber bültenleri.
  中文翻译:2026 产出:前沿模型评估 AI Dashboard、Remote Labor Index(vec Scale AI 联合)、Superintelligence Strategy Paper、AI Frontiers 简报。

### Dört risk çerçevesini

CAIS çerçevesinde, felaketli AI riskini dört üst düzey kategoride gruplandırıyor:

> CAIS'in çerçevesinde felaketli AI 风险 dört üst sınıflara ayrılmıştır:

1. **Malicious use**: kötü bir oyuncu, AI'yi zarar vermek için kullanır (biyo silah sentezi, yanlış bilgi, siber saldırılar).
   Çeviri:**恶意使用**:坏人 AI kullanmak 伤害 yaratmak 生物武器合成、虚假信息、网络攻击)
2. **AI races**Laboratuvarlar, şirketler veya ülkeler arasındaki rekabet basıncı, dağıtımın güvenli olduğu noktan öteye doğru ilerlemesini sağlar.
   Çeviri:**AI 竞赛**Laboratuvarlar, şirketler veya ülkeler arasında rekabet basıncı, deploymayı güçlendirme ve güvenliği sağlama noktasını artırmaktadır.
3. **Organizational risks**: iç laboratuvar dinamikleri (güven kültüründe başarısızlıklar, yetersiz denetim, yetersiz kaynaklı güvenlik) kötü bir uygulama üretir.
   Çeviri:**组织风险**İçeriği: interne实验室动态(安全文化失败、审计不足、安全资源不足) kötü bir yerleşim oluştu.
4. **Rogue AIs**: Yeterince yetenekli bir Yapay zeka, insan refahıyla çelişen hedefleri takip eder.
   Çeviri:**失控 AI**: Yeterince yetkin bir AI  İnsan refahı ile çatışma amaçlarını takip etmek

Bu tek taksonom değil; en çok alıntılanan. Kategoriler birbirini hariç tutmuyor  bir yarışta hız denetimi yapan bir organizasyon tarafından üretilen bir çirkin AI dörttür.

> Bu tek sınıflandırma yasası değil; en sık alıntılananıdır.

### Organizasyonel riskin yaşadığı yer

Dört kategoriden, örgütsel risk uygulanabilir bir laboratuvarın güvenlik kültürü, denetim sıkıntısı, savunma katmanlama ve bilgi güvenliği, ders 1018 kontrolleri ile model gemilerinin gerçekten yer aldığını veya bu kontrollerin kimsenin doğrulanmadığı kontrol listesi öğeleri olup olmadığını belirler.

> Dört sınıf arasında, organizasyon riskleri, uygulayıcılar için en çok uygulanabilir olanlardır. Laboratuvar güvenlik kültürü, denetim sıkıntısı, savunma katmanları ve bilgi güvenliği, onların modellerinin 10-18 sınıfı kontrolü ile gerçekte yayınlandığını veya bu kontrollerin insan tarafından onaylanmamış bir listeyi belirlemesini belirler.

Konkret organizasyonel risk levhaları:

> 具体组织风险杆:

- **Safety culture**CAIS anketleri bu durumun diğer derecelerin güçlü bir tahmincisi olduğunu buldu.
  Çeviri:**安全文化**Bu, diğer 杆lerin güçlü tahmin faktörü olduğunu ortaya koydu.
- **Rigorous audits**Sadece iç denetimler iyimser raporlar üretir.
  Çeviri:**严格审计**Dış ve iç: Sadece iç denetimler 乐观报告产生──
- **Multi-layered defenses**: tek bir katman yeterli değildir (Faz 15'in devam konusu).
  Çeviri:**多层防御**:无单层足够 (Fase 15) 贯穿主题)
- **Information security**Modelle ağırlık sızdırılması, değerlendirme verileri sızdırılması, izleyici-önleme teknikleri sızdırılması.
  Çeviri:**信息安全**Model:Devayı değerlendirmek, veri sızmasını değerlendirmek, denetim ve teknik sızıntıları önlemek.

### CAISI  AI Standartları ve Yenilikler Merkezi

- NIST'de çalışır.
  Çin Çeviri:
- Sınır laboratuvarlarıyla gönüllü anlaşmalar yürütüyor.
  Çinçe Çevirisi:与前沿实验室运行自愿协议。
- Siber, biyolojik ve kimyasal silah risklerine odaklanan sınıflandırılmamış kapasite değerlendirmeleri yayınlar.
  Çinçe Çevirisi: Yayınlı bir net, biyolojik ve kimyasal silah riskleri gizli yetenek değerlendirmesi.
- CAIS'ten farklı; kısaltmalar çarpışır; hangi birini okuduğunuzu doğrultmak için URL'yi (nist.gov) kontrol edin.
  ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXXV ÇXXXXXXXXXXXX ÇXX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

CAISI'nin rolü, METR'nin özel laboratuvar çalışmalarına (Desin 21) kamu ve hükümet karşıtıdır. CAISI raporları sınıflandırılmamıştır; METR raporları genellikle NDA kapalıdır.

> CAISI'nin rolü METR Private Person Laboratory kooperasyon (II. Sınıf) 'nın kamuoyuna yönelik hükümet karşısında yapılan çalışmalardır.

### Kaliforniya SB-53

Kaliforniya Senatosu tasarısı (2025 2026 seansı) sınır modellerinden gelen felaket riskini ele alıyor.

> 加州 Senatosu Yasası (Kazova) 2025 2026 会期)

- Devlet düzeyinde yükümlülükleri tetikleyen özel kapasite eşiği.
  Çinçe Çevirimi:触发州级义务的特定能力值──
- AI laboratuvarı çalışanları için haberci koruma.
  Çin dilinde:AI 实验室员工举报人保护
- Katastrofik başarısızlıklar için olay raporlama gereksinimleri.
  Çinçe Çevirisi: Katastrofe性失败的事故報告要求──

Eğer imzalanırsa, ABD eyalet düzeyinde ilk felaket riski düzenlemesi olacaktır. İmza durumuna bakılmaksızın, yasa tasarısının çerçevesinde diğer eyalet mevzuatçılarının soruna nasıl yaklaştığı şekillendirilir. Kaliforniya'daki uygulayıcılar yasa tasarısının durumunu takip etmelidir; diğer yerlerde uygulayıcılar ABD eyalet düzeyinde düzenlemenin nasıl görüneceğini anlamak için okumalıdır.

> Eğer imzalanırsa, bu ilk ABD eyalet düzeyinde felaket riskı düzenlemesi olacaktır. İmzalanırsa, yasaın çerçevesinin diğer eyalet mevzuat kurumlarının sorunları nasıl ele aldığını şekillendirdiğini görmezden gelmek için, Kaliforniya'daki uygulayıcılar yasaın durumunu takip etmelidir.

### Toplumsal risk tek katmanlı bir sorun değildir.

15'inci aşamada devam eden teması  derin savunma  toplumsal katmanlarda da geçerlidir. Tek bir organizasyon, düzenleme veya çerçeve felaket riski kapatmaz.

> Bölüm 15'ün geçiş konusu: Derin savunma; sosyal seviyeye de uygulanmaktadır.

- Laboratuvarlar'ın ölçeklendirme politikaları (Deneyimler 19, 20).
  Çin dilinde:实验室发布扩展政策 (nüfusu genişletilmesi için yapılan çalışmalar)
- Dış değerlendiciler ölçümler yapar (Denevi 21).
  Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çev
- Sivil toplum izleme ve kamuoyuna yayımlama (CAIS).
  Çinçe Çevirisi:民间社会跟踪和宣传 (CAIS)
- Hükümet gönüllü programlar ve temel düzenleme (CAISI, SB-53) yürütüyor.
  Çin dilinde:政府运行自愿计划和基线监管 (CAISI、SB-53)
- Pratikçiler çok katlı kontroller inşa (Düşünmeler 1018).
  Çinçe Çevirimiçi:从业者构建多层控件 (→ 10 课)

Bu, aşama için son sentez: her önceki ders, tamamlılığı herhangi bir tabaka gücünden daha önemli olan bir yığındaki bir katmandır.

> Bu aşamaların son birincil bir parçasıdır: önceki her bölüm, bir katmanın bir katmanıdır, bütünlüğü herhangi bir katmanın gücünden daha önemlidir.

## Çerçeveyi kullanın.
```figure
a5-four-risks
```

## Kullan

`code/main.py`Bu, bir risk envanteri aracı uygulamaktadır. Bir önerilen dağıtımla, dağıtımın dört risk kategorisine karşı etiketlenmesini ve azaltma kontrol listesini gönderir.

> `code/main.py` Küçük Riskler Bütçeleme Aracı:  Öneriler için 4 Riskler Kategorisi için Deployment,  Elimin için 4 Riskler Kategorisi için Deployment ve  Geri dönüş

## İndirin . Ürünler .

`outputs/skill-societal-risk-review.md`Toplum ölçeğinde risk pozisyonu için bir uygulama değerlendiriyor: dört kategoriden hangisine değiniyor, hangi hafiflemeler uygulanıyor, kurumsal risk maruz kalması nedir.

> `outputs/skill-societal-risk-review.md`审查部署的社会规模风险姿态: dört kategori arasında hangileri ele alın 已有哪些缓解 组织风险暴露是什么──

## Egzersizler.

1. Çık .`code/main.py`. Farklı ölçeklerde üç sentetik dağıtım ekleyin. Dört risk etiketlerinin beklediğinizle uyumlu olduğunu doğrulayın; araçın düşük veya aşırı etiketlendiği bir durum belirleyin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py` Üç farklı büyüklükteki bir yapım devreyi giriş yapmak.

2. CAIS dört risk kağıdı'nı tamamıyla okuyun. Bir risk kategorisini seçin ve 2026'da bu kategoride en önemli gelişme olduğuna inandığınız şey hakkında iki paragraf yazın.
   Çin dilinde: Full reading CAIS 四风险论文──选一风险类别,写两段关于你认为该类 2026 最重要发展──

3. California SB-53'in hazırkı taslağını okuyun.
   Çinçe çevirisi: read Kazahu SB-53 当前──草案识别你认为强化灾难性风险姿态的一个条款和弱化的一个──论证两者──

4. Bildiğiniz bir üretim AI dağıtımını seçin (seninki veya yayınlanmış bir tane). Kurumsal risk alt dereceleri ile karşılaştırın: güvenlik kültürü, denetim sıkılığı, çok katlı savunmalar, bilgi güvenliği. En zayıf olan hangisi?
   Çinçe çevirisi: seçin bir biliyorsunuz üretim AI deployment (İşiniz veya açık) ⋅ örgüt kuruluşları için 杆打分: güvenlik kültürü ⋅ denetim sertliği ⋅ çok katlı savunma ⋅ bilgi güvenliği ⋅ hangi en zayıf? standartlara ulaşmak için ne kadar maliyet gerekir?

5. Dört risk çerçevesinin 2028 versiyonunu çizin ki bu bir yılın ek kapasite ve bir yılın ek dağıtım deneyimi yansıtır. Neyi ekleyeceksiniz, çıkarırsınız veya yeniden gruplandırırsınız?
   Çinçe Çevirimiçi: Çıkışlar bir yıllık ekstra yetkinliği ve bir yıllık dış görev deneyimini yansıtır.

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| CAIS | "Center for AI Safety" | Non-profit; four-risk framework; 2023 extinction statement | CAIS：非营利，四风险框架 |
| CAISI | "US government AI safety" | NIST Center; voluntary agreements; unclassified evals | CAISI：NIST 中心，自愿协议 |
| Four-risk framework | "CAIS's taxonomy" | malicious use, AI races, organizational risks, rogue AIs | 四风险框架：恶意使用/AI 竞赛/组织风险/失控 AI |
| Malicious use | "Bad actor uses AI" | Bioweapons, disinformation, cyberattacks | 恶意使用：生物武器、虚假信息、网络攻击 |
| AI races | "Competitive pressure" | Labs/companies/nations push deployment past safety | AI 竞赛：竞争压力推动部署越过安全 |
| Organizational risk | "Lab internal failure" | Safety culture, audit, defenses, infosec | 组织风险：安全文化、审计、防御、信息安全 |
| Rogue AI | "Misaligned agent" | Capable AI pursuing goals conflicting with human welfare | 失控 AI：追求冲突目标的强大 AI |
| California SB-53 | "State-level regulation" | 2025–2026 bill; first US state catastrophic-risk regulation if signed | 加州 SB-53：州级灾难性风险监管法案 |

## Daha fazla okumak

- [Center for AI Safety](https://safe.ai/) Dört risk çerçevesinin kurumsal evleri.
  Çinçe Çevirisi:四风险框架的机构之家
- [CAIS — AI Risks that Could Lead to Catastrophe](https://safe.ai/ai-risk) dört riskli kağıt.
  Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Ç Çevre: Çevre: Çevre: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- [CAIS — May 2023 statement on extinction risk](https://safe.ai/statement-on-ai-risk) Kısa ortak açıklama.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [NIST CAISI](https://www.nist.gov/caisi) Hükümet karşısında AI standartları ve yenilik merkezi.
  Çinçe Çevirisi: Face towards政府的AI 标准和创新中心
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) laboratuvar düzeyinde yapılan yükümlülükleri toplumsal ölçekte bir çerçeveye bağlar.
  Çinçe Çevirimi:                                                                                                                                                                                                                                                            
