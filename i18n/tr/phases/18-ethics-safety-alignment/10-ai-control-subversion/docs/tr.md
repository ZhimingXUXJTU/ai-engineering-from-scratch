# AI Kontrol  Devrimlere rağmen güvenlik  Devrim  Kontrol Güvenlik

> Greenblatt, Shlegeris, Sachan, Roger (Redwood Research, arXiv:2312.06942, ICML 2024). Kontrol güvenlik sorusunu yeniden çerçeveliyor: Size karşı olumsuz optimizasyon sağlayabilecek güvenilir olmayan güçlü bir model U'nun göz önüne alındığında, kabul edilemez bir sonuç olasılığını sınırlayanken yararlı çalışmayı çıkarmanıza hangi protokoller izin veriyor? Kaynaklar güvenilir bir zayıf model T, güvenilir insan iş gücü bütçesi H ve U'nun çıkışlarını düzenleme yeteneğidir. Bu çerçeve içinde, Güvenli Düzenleme Pareto, kod arka kapı görevlerinde güvensiz izleme üzerinde egemenlik kazanır. Çerçeve güvenlik mühendisliği'nden en kötü varsayımları miras alır: güvenlik, U'nun yerine gelen kırmızı takım basıncı altında ölçülen, karşı karşıya seçilen U'nun belirli kabul edilemez bir sonuca neden olamayacağı olasılığıdır.

> **【中文解读】**Bu bölüm, AI  kontrol ve altüst olma risklerini                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

> **【拓展：AI 控制 → 安全工程范式】**AI  kontrol klasik güvenlik mühendisliği'nden en kötü durumlara sahip olan varsayım: güvenlik, kırmızı takım baskısı altında dirençli seçimlerin U'nun kabul edilemez sonuçlar üretme olasılığıdır. Bu, "U'ya güvenilmez mi?"

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, safety-vs-usefulness frontier on code-backdoor task) | **语言:** Python（标准库，代码后门任务的安全-有用性前沿）
**Prerequisites:** Phase 18 · 07 (sleeper agents), Phase 18 · 08 (scheming), Phase 18 · 09 (alignment faking) | **前置知识:** Phase 18 · 07 (潜伏 Agent), Phase 18 · 08 (策略), Phase 18 · 09 (对齐伪装)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Öğrenci bölümün başında:Fase 18·07-09(欺骗三角) ・・・AI Kontrol = Güvenli İnşaat范式:"Eğer U不可信,我们也能安全使用吗?"
>  **【类比】**AI Control = " İyiliğine sahip olan işçilerin "¬;对齐 = 让员工变忠诚(难);控制 = 设计工作流让不忠员工也搞不破坏(实务) ∙资源:可信弱模型 T、人类劳动 H、编辑 U 输出能力──结论:可信编辑 Pareto 占优于不可信监控(代码后门任务) ⋅
> 🤔 对齐 vs 控制:对齐问"U可信吗",对齐问"即使 U不可信吗,安全吗"──两者都需要控制是部署协议属性,对齐是模型属性──

## Öğrenme hedefleri

- Yapay zeka Kontrol tehdidi modeli tanımlayın: güvenilmeyen güçlü model U, güvenilen zayıf model T, güvenilen insan bütçesi H.
  Çinçe Çevirim: defini AI  kontrol tehdit modeli:不可信强模型 U、可信弱模型 T、可信人类劳动预算 H。
- Güvenli Düzenleme protokolünü ve neden ICML 2024 kod arka kapı görevi üzerinde güvensiz izleme üzerinde Pareto'nun baskısı olduğunu açıklayın.
  Çinçe Çevirimiçi: Description可信编辑协议及为什么在ICML 2024 代码后门任务上 Pareto 占优于不可信监控──
- Düzeltme (U güvenilir) ve kontrol (U güvenilir değil ve yine de güvendeyiz) arasındaki farkı açıklayın.
  Çinçe Çevirimiçi: açıklama ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒  ⇒ ⇒ ⇒ ⇒ ⇒ ⇒   ⇒ ⇒ ⇒      ⇒    ⇒ ⇒      ⇒ ⇒     ⇒      ⇒ ⇒      ⇒              ⇒                                                                                                                                                                     
- Kontrolün üç sınırını belirtin: İnsanlar ölçeklenmez, güvenilir zayıf modeller sonunda geride kalır, kontrol güvenilir güçlü modeller üretmez.
  Çinçe Çevirimi: kontrolün üç sınırını açıklamak: İnsanın genişletemeyeceği, inanılmaz güçlü bir model oluşturmayacağı, kontrolün son olarak geriye düşmeyeceği, inanılmaz güçlü bir model oluşturmayacağı.

## Sorunlar. Sorunlar.

Dersler 7-9 bir sınır modeli aldatıcı bir şekilde uyumlu, planlama veya sahte uyumlu olabilir. Güvenlik sorusu yeniden çerçeveliyor: Kabul edilemez sonuçlar getirme fırsatı vermeden güvenmediğimiz bir modelden yararlı çalışmalar elde edebilir miyiz? Bu kontrol sorunu ve klasik güvenlik gibi yapılandırılmış: en kötü durumda rakibi varsayın, bir protokol tasarlayın, kırmızı takım baskısı altında rakibin başarısı oranını ölçün.

> Ders 7-9 Ön kenar modelinin sahtekârlık karşısında, strateji veya sahte karşı karşıtlık olarak ortaya çıkmasıdır. Güvenlik sorunu yeniden tanımlanır: güvensiz modelden yararlı bir iş çıkarıp kabul edilemez sonuçlar elde etme fırsatı verebilir miyiz?

## Konsepten bir şey.

> **【中文解读】**威胁模型的三要素:U(不可信强模型) 有能力,可能对抗性;T(可信弱模型) 能力较弱,但已知不是对抗性;H(可信人类劳动) 小预算,不可扩展──系统必须使用U 产生有用输出──对手试图产生具体不可接受结果 (如交付代码中的后门),同时保持一定比例的合法有用工作通过有用性值──

### Tehdit modeli

Kontrol şu varsayımları yapar:
- U  güvenilmeyen güçlü model. Yetenekli. Muhtemelen karşıt (değerlendirme bunu öyle görüyor).
  Çinçe Çevirimiçi:U不可信强模型──有能力──可能对抗性 (Beneçimici)
- Daha zayıf bir model, daha az yetenekli ama düşmanca olmayan biri.
  Çin Çeviri:T可信弱模型──能力较弱,但已知不是对抗性──
- H  güvenilir insan gücü.
  Çeviri: H可信人类劳动──小预算;不可扩展──

Sistem, U kullanarak yararlı bir çıkış üretmelidir. Düşman, yararlılık eşiğinde geçmek için meşru yararlı işlerin bir kısmını korurken, kabul edilemez bir sonuca neden olmaya çalışır (örneğin gönderilen kodda arka kapı).

> 系统 must use U                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

Kontrol, U'ya güvenmeyi bırakır. Güven yokken hangi protokollerin güvenliğini koruduğunu sorar.

> Güvenliğin kontrol edilmesi. Güvenliğin korunması.

### ICML 2024 arka kapı görevi

U'nun, bir çözümün bir arka kapı içerdiği takdirde gizli bir oracle bayraklar (kodun yanlış bir çıkış üretmesini sağlayan belirli bir giriş). Kırmızı takım U'yu kontrol eder ve tüm protokol içsellerini görmesine izin verilir. Protokol, arka kapı nakliye hızını bir eşiğin altında tutarak çözülmüş sorun oranını en üst düzeye çıkarmalıdır.

### Dört protokol karşılaştırıldı

- **Baseline:**U gemisinin çıkışı doğrudan, maksimum kullanılabilirlik, güvenlik minimum.
  Çeviri:**基线：**直接交付 U 的输出──有用性最大──安全性最小──
- **Upfront auditing:**Tüm çıkışlarda H kullanın.
  Çeviri:**前期审计：**Tüm çıkışlar için en büyük güvenlik.
- **Untrusted Monitoring:**U'nun ikinci bir örneği ilk bir örneğin çıkışını puanlar; H, işaretli çıkışları denetler.
  Çeviri:**不可信监控：**U'nun ikinci örneği değerlendirmek; H 审计标记的输出――风险:两个 U's 实例可以串通――
- **Trusted Editing:**T her sorguda U'nun çıkışını düzenler. T güvenmezse, H'ye yönlendirin.
  Çeviri:**可信编辑：**T'nin her sorguda edit U'nun çıkışı. Eğer T'nin belirsiz olması durumunda H'ye yol açılır.

Greenblatt et al. ' in bulduğu gibi güvenilir düzenleme Pareto-dominates güvensiz izleme: her güvenlik seviyesinde daha yüksek kullanışlılık.

> Greenblatt  et al. Pareto'nun güvenilir editörlüğü güvenilmez denetimden daha iyi olduğunu buldu: her güvenlik seviyesinde daha yüksek bir kullanışlılık vardır.

> **【拓展：可信编辑 vs 不可信监控 → 共谋问题】**İtiraf edilmez denetim gereksinimlerinin ikinci örnekleri U'nun ilk koordinasyon  koalisyon  ile birlikte gerçekleşemez.  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Koalisyon  Ko

### Neden Güvenli Düzenleme Başarıyor

Güvenilmeyen izleme U'nun ikinci durumunun ilk durumla koordinasyon yapamayacağını gerektirir. Kolluzyona steganografik ipuçları veya ortak eğitim öncesi yoluyla ulaşılabilir. Protokol, monitörün sinyalini azaltan bir anlaşmazlığa direnç (parafrasi, bulanıklık) bütçesini yatırım yapmalıdır. Güvenli Düzenleme, tamamen anlaşmazlıktan kaçınır çünkü T güvenilir  T'nin önerdiği herhangi bir düzenleme varsayımla karşıt değildir. Maliyet T'nin daha az yeteneği olması, yani ince arka kapıları aşırı reddedebilir veya kaçırır.

> U'nun ikinci örneği, ilk koordinasyonla uyumludur. Kömüntü, gizli yazma yöntemleri ile gerçekleşir.

### Dört protokol eksesi

1. U'nun rolü: sadece üreticisi, monitör veya her ikisi de.
   Çeviri: U 扮演什么角色:仅生产者、监督者或两者──
2. T'nin rolü nedir: editör, monitör veya resampler.
   Çeviri:T 扮演什么角色:编辑者、监督者或重采样者──
3. H'nin nasıl dağıtılması: birer denetim, rastgele denetim veya bayrak yönlendirilmiş denetim.
   Çinçe Çevirim:H 如何分配:均审计、随机审计或标记导向审计──
4. Protokolün anlaşma direnci için harcadığı miktarı hesaplayın.
   Çinçe Çevirisi: protokol on kontra共谋 için ne kadar harcanır?

### Düzeltme vs. kontrol

- Düzeltme: "Sana güvenmek için güvenli misin?" 2., 4., 5., 6., 7., 8. 9. dersler buna dayanır.
  Çinçe Çevirimi:对齐:"U安全可信吗?" Dersleri 2, 4, 5, 6, 7, 8, 9 都与此相关──
- Kontrol: "U'yu güvenmeden güvenli bir şekilde kullanabilir miyiz?" Ders 10.
  Çinçe Çevirimiçi: kontrol:"Bizim güvenim yokken güvenli bir şekilde kullanılabilir mi?" Ders 10。

Düzeltme, modelin bir özelliğidir. Kontrol, dağıtım protokolünün bir özelliğidir. Kontrol, düzeltme modellerini üretmez; düzeltme olmayan modellerin güvenli bir şekilde kullanımı sağlar. Her iki gündeme de gereklidir.

> Kontrol, birbiriyle uyumlu bir model oluşturmaz; bu, birbiriyle uyumsuz bir modelin güvenli kullanımını oluşturabilir.

> **【中文解读】**Kontrolün üç temel sınırlaması: 1) İnsanın genişlemediği H Büdceyi istekli denetleme zorlukları AI  Çıkışının insan sayısı ile sınırlı; 2) T 远弱于 U 时,T'in editör sinyalleri gürültü haline geldiğinde son olarak geride kaldı; 3) Kontrol, T 远弱于 U 时,T'in editör sinyalleri gürültü haline geldiğinde başarısız olabilir; 3) kontrol, ASL-3'de uygulanabilir bir anlaşmaya sahip değil.

### Üç temel sınırlama

- İnsan ölçeklendirme yapmaz. H bütçesi zor AI çıkışlarını denetlemeyi isteyen insanların sayısıyla sınırlıdır.
  Çinçe Çevirisi: İnsanın genişlemesi mümkün değil.
- Güvenli zayıf modeller sonunda geride kalır. T U'dan çok daha zayıf olduğunda, T'nin düzenleme sinyali gürültü haline gelir.
  Çinçe Çevirimiçi:可信弱模型最终滞后──T'in editör sinyalleri gürültüye dönüştü.
- Kontrol bir uyum değildir. ASL-3'de (Desin 18) çalışan protokoller, T'yi manipüle edebilir veya H'nin denetim dağılımını akıl yürütürse, kontrol başarısız olabilir.
  Çinçe Çevirisi: kontrol değil.

### 2025'in gelişiminin

UK AISI ve Redwood Kontrol Güvenlik Kazları (metr.org / redwoodresearch.org 2025) üzerinde işbirliği yapmaktadır: bir kontrol güvenliği vakaı, U hakkında en kötü varsayımlarda, protokol kabul edilemez bir sonuç olasılığını sınırlıyor. Güvenlik vakaları (Desin 18) kontrol çerçevesini miras alır.

> UK AISI 和 Redwood 合作开展控制安全案例 (Control Security Case) (KONTROL SİKYETE KASAŞLARI) (KONTROL SİKYETE KASAŞLARI) (KONTROL SİKYETE KASAŞLARI) (KONTROL SİKYETE KASAŞLARI) (KONTROL SİKYETE KASAŞLARI) (KONTROL SİKYETE KASAŞLARI) (KONTROL SİKYETE KASAŞLARI) (KONTROL SİKYETE KASAŞLARI) (KONTROL SİKYETE KASAŞLARI) (KONTROL SİKYETE KASAŞLARI) (Lection 18) kontrol çerçevesini miras aldı.

### Bu 18 fazaya uygun.

Ders 6-9 tehdit ( aldatma mümkün) tanımlar. Ders 10 tehdit gerçek olduğu varsayımıyla savunma paradigmasını tanımlar. Ders 11 tamamlayıcı saldırı paradigmasını tanımlar (U'yu ölçeklenebilir denetim yoluyla güvenilir hale getirir).

> Ders 6-9  tehditleri tanımlamak (Bullugging is possible) ◊ Ders 10  Defians范式を描述する ⇒ Hileler gerçek varlığı tehditlerini tanımlamak (Fifse) ◊ Ders 11 互补的积极范式を描述する ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒             ⇒                                                                                                              

> **【拓展：控制安全案例 → UK AISI 合作】**2025 yılında İngiltere AISI ve Redwood  işbirliği ile kontrol güvenlik durumları  U hakkında en kötü durum varsayımında, çalışma anlaşması kabul edilemez sonuçların olasılığını sınırladı  Güvenlik durumları  Ders 18) kontrol çerçevesini miras aldı  kontrol dört birliği: U  role  T  role    role     nasıl dağıtıldı  protokol muhalefet kavgacılık üzerinde ne kadar harcadığını hesaplamak 

## Çerçeveyi kullanın.
```figure
al-control-protocol
```

## Kullan

`code/main.py`Oyuncak arka kapı görevinde dört protokolü simüle eder. U çıkışlar üretir; bir bölümü arka kapı (kırmızı takım politikası). T onaylar veya düzenlemeler yapar. H bir bütçe üzerine çağrılır. Pareto sınırını yeniden üretmek için bütçeyi ve anlaşma parametresini Greenblatt et al. 2024'te görüntüleyebilirsiniz.

> `code/main.py`Oyuncaklar için dört çeşit bir anlaşma oluşturulur.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-control-protocol-audit.md`. Bir dağıtım protokolü açıklaması verildiğinde, U / T / H rollerini tanımlar, anlaşma vektörlerini isimlendirir ve protokolün kullanılabilirlik-güvenlik sınırında kırmızı takım basıncı altında konumunu tahmin eder.

> 本课产 出 `outputs/skill-control-protocol-audit.md` U/T/H rollerini tanımlamak,  Kötülük ve güvenlik ön yarısında konumlandırma anlaşması,  Kötülük ve güvenlik ön yarısında konumlandırma anlaşması

## Egzersizler.

1. Çık .`code/main.py`Güvenli Düzenleme ile Güvensiz Denetim için yararlılık-güvenlik sınırını yeniden üretmek.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖   ❖ ❖            ❖                                                                                                               

2. Yeni bir protokol ekleyin: "T düşük sıcaklıkta yeniden örnekler, sonra U T'nin çıkışını düzenler".
   Çinçe Çevirimi: Yeni Protokol Ekle:"T düşük sıcaklıklı ağırlıklı bir şekilde, sonra U 編集 T の輸出──" Neden bu güvenilir editör başarısızlığı daha felaketli?

3. 2024 makalesinde U'nun protokolü görebileceğini varsayıyor. U'nun denetlendiği çıkışlardan saklanan bir protokol tasarlıyor. Bu protokol yerleştirme altyapısından ne gerektirir?
   ÇINCE TRANSLATION:2024 yılın makalesi U görebilirsiniz görmesi için bir anlaşma tasarım  U  gizleyen hangi çıkışlar tarafından denetlenmiş anlaşma için 

4. Greenblatt et al. 2024 Bölüm 7 (koşulma) okuyun.
   Çinli dilde:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:{{lang-en:en:{{lang-en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en:en

5. U = GPT-4 sınıfı, T = GPT-3.5 sınıfı, H = % 1 denetim edilen çıkışları kullanan bir dağıtım için bir kontrol güvenlik kazasını açıklayın. Kaza bağlı olan tek en güçlü varsayımı tanımlayın.
   Çinçe Çevirimi: için U = GPT-4 级、T = GPT-3.5 级、H = 1% 输出审计的部署陈述控制安全案例──

## Anahtar Terimler

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| AI Control | "safety under subversion" / "颠覆下的安全" | Protocol design that bounds unacceptable outcomes under a worst-case U / 在最坏情况 U 下限制不可接受结果的协议设计 |
| Untrusted model (U) | "the strong model" / "强模型" | The capable model we want to extract work from but do not trust / 我们想从中提取工作但不信任的能力模型 |
| Trusted model (T) | "the weak model" / "弱模型" | A weaker model, known not to be adversarial, used as editor/monitor / 已知不是对抗性的较弱模型 |
| Trusted human (H) | "the audit budget" / "审计预算" | Bounded expert labor; expensive; the ground-truth signal / 有界的专家劳动；昂贵；地面真实信号 |
| Trusted Editing | "T edits U" / "T 编辑 U" | Protocol where T is the gate on U's outputs; H called on ambiguous outputs / T 是 U 输出的门控的协议 |
| Untrusted Monitoring | "U monitors U" / "U 监控 U" | Protocol where a second U instance scores outputs; collusion-resistant only with extra investment / 第二个 U 实例评分输出的协议 |
| Control safety case | "the formal argument" / "正式论证" | Written argument that a protocol bounds the adversary's success under worst-case U / 协议在最坏情况 U 下限制对手成功的书面论证 |

## Daha fazla okumak

- [Greenblatt, Shlegeris, Sachan, Roger — AI Control (arXiv:2312.06942)](https://arxiv.org/abs/2312.06942) Kanonik ICML 2024 kağıdı
  Çeviri:Central Cities of the Philippines (Central Cities of the Philippines)
- [Redwood Research — Recent AI Control papers index](https://redwoodresearch.substack.com/) 2024-2025 takipleri
  中文翻译:Redwood Research2024-2025 后续
- [UK AISI + METR — Control safety cases](https://metr.org/blog/2025-03-26-common-elements-of-frontier-ai-safety-policies/) Sınır laboratuvarlarının operasyonelleştirilmesi
  中文翻译:UK AISI + METR前沿实验室的操作化
- [Hubinger et al. — Sleeper Agents (Lesson 7, arXiv:2401.05566)](https://arxiv.org/abs/2401.05566) Tehdit modeli kontrolü varsayımları
  Çinçe Çevirimi:Hubinger 等人 kontrol假设的威胁模型
