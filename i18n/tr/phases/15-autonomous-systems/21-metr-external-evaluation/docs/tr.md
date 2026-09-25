# METR Zaman Uzaklıkları ve Dış Yetenek Değerlendirme

> METR (ex-ARC Evals), Aralık 2023'ten beri bağımsız bir 501(c)(3) kuruluşu. Time Horizon 1.1 referans değerleri (Ocak 2026) görev başarısı olasılığı ile log ((insan uzmanı tamamlama zamanı) arasındaki lojistik bir eğriye uyar; %50 olasılıkla kesişme modelin zaman ufkunu tanımlar. 20252026 görev kümesi GPT-5.1, GPT-5.1-Codex-Max ve prototip izleme değerlendirmelerini kapsar (monitor yakalama yan görevleri yapabilir; ajan kaçınabilir). Benchmark suites: HCAST (180+ ML, cyber, SWE, akıl yürütme görevleri; 1 dakika ila 8+ saat), RE-Bench (71 ML araştırma- mühendislik görevleri uzman tabanı ile), SWAA. Dürüst bir not: METR ölçümleri idealize edilmiştir  insanlık yok, gerçek sonuçlar yok  ve ekip değerlendirme vs. dağıtım davranış boşluğu (Desin 1) belgelenmiştir. Zaman ufku bir üst sınır, bir yerleşim tahmin değil.

> **【中文解读】**Bu bölümde METR Dış Departmanının bağımsız üçüncü tarafların AI sistem kapasitesini ve riskini değerlendirmesini tanıtıyor.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, logistic-fit horizon estimator) | **语言:** Python（标准库，逻辑拟合时间线估计器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 19 (RSP) | **前置知识:** Phase 15 · 01（长程 Agent）、Phase 15 · 19（RSP）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Öğrenci bölümünün başında öğrenmek için öncelikle öğrenin: 15·01 aşama (長程代理)  15·19-20 aşama (RSP framework) 统计基础 (逻辑归归)  METR = bağımsız üçüncü taraf değerlendirme kurumu, "AI R&D-4" ve diğer politikaların değerini ölçülebilir bir rakam haline getirmek.
>  **【类比】**METR = "AI 能力的第三方体检中心"──RSP diyor ki "AI R&D-4 值" ise çürüdür; METR'in Zaman Uçurumu 基准把"AI 能完成多复杂任务"压缩成一个标量"模型 50% 可靠性能完成专家花 X 小时的任务"──类似于IQ 分数概括智力,但METR'in数字有可重复测量方法──
> ️ **【易错点】**METR Zaman Uçaklığı: Zaman Uçaklığı: Yukarı sınır değil, Aşağı sınırdır, Uçaklık Önceki Gerçek Görevinde Devam Etmek Gerektirir.

## Sorunlar. Sorunlar.

Ölçekleme politikaları (Lection 19, 20) sadece referansları olan ölçümler kadar yararlıdır. "AI R&D-4 eşiği" ve "Uzun mesafeli özerklik" politika prozasında tanımlanır; sadece belirli değerlendirmeler belirli sayıları ürettiğinde uygulanabilir hale gelir.

> 扩展政策 (第 19、20 课) kullanımı, sadece onların alıntıladığı ölçümlerle aynıdır.

METR, bu rakamların çoğunu tanımlayan 20242026 dış değerlendirme örgütüdür. Sınır modelleri  genellikle önceden yayınlanır, NDA ile laboratuvarlar  altında değerlendirilir ve daha sonra metodoloji yayınlanır. Time Horizon 1.1 referans göstergesi (Ocak 2026) başlık eseridir: tek bir skalar, yetenekleri insan okuyabilir bir birime sıkıştırır ("bu model, bir uzmanın %50 güvenilirlik ile X saat harcadığı türde bir görevi yapabilir").

> METR, 20242026'da bu rakamların çoğunu dış değerlendirme örgütüdür. Önceki modelleri genellikle yayınlanmadan önce  Laboratuvar imzaladı NDA  sonrasında yayınlanmış yöntem teorisidir. Time Horizon 1.1 基准(2026 yılının 1 ayı) başlıklı bir yapıtıdır: "Bu model, %50 güvenilirlik altında tamamlanabilir".

Ders kısmen metodoloji (bir ufuk nasıl hesaplanır) ve kısmen yorumlama (bir ufuk neden bir üst sınırdır, bir dağıtım tahmin değil) ile ilgilidir.

> Bu ders bölümünün bir kısmı yöntemsel olarak, bölümünün bir kısmının açıklamasıdır. Bu iki beceriyi birlikte kullanmak için, "14 saat" filmindeki "14 saat" filmindeki takımların kötü tedarikçi açıklamaları tarafından aptalca şekilde ele alınması daha zor.

## Konsepten bir şey.

### METR arka planı

- Aralık 2023'te kuruldu (eski ARC Evals, bağımsız 501 ((c) ((3)) olarak ayrıldı).
  Çin dilinde Türkçe:成立:2023年 12 月(原 ARC Evals,分拆为独立 501(c)(3))
- Kapsam: Sınır modellerinin özerk yeteneklerinin değerlendirilmesi, genellikle önceden yayınlanmaktadır.
  Çeviri: önde model kendi kendine yetenek değerlendirmesi, genellikle yayınlanmaktadır.
- Ortak laboratuvarlar: Anthropic, OpenAI (çoklu görevler 20252026).
  Çinçe Çevirimi:合作实验室:Anthropic、OpenAI(20252026 多次合作)
- Görülen sonuçlar: Time Horizon 1.0 (Mart 2025), Time Horizon 1.1 (Ocak 2026), prototip izleme değerlendirmeleri.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

### Zaman Uçaklığı

Metodoloji (METR blogundan ve makaleleri):

> 方法论(METR'den gelen 博客和论文):

1. Dakika ölçeği ile saat ölçeği uzman tamamlama süreleri arasında bir görev kümesi toplayın.
   Çinçe Çevirimi:收集覆盖分钟级到小时级专家完成时间的任务集──当前集:HCAST(180+任务)、RE-Bench(71 任务)、SWAA──
2. Her görev için model çalıştırın; başarıyı ya da başarısızlığı kaydetin.
   Çinçe Çevirimiçi: 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書
3. Logistik bir eğri ayarlayın: P(başarılılık) log(ekspert tamamlama süresi fonksiyonu olarak).
   Çinçe Çevirim:拟合逻辑曲线:P(成功) olarak log(专家完成时间)
4. Uçaklık, P ((başarılılık) = 0.5'in uzman zamanıdır.
   Çinçe Çevirimi: 时间线是 P(成功) = 0.5 时的专家时间──

Logistik uygunluk şekli doğru bir şekildir çünkü yetenek genellikle görev zorluğu ile yükselen, plato yaklaşımlı bir ilişkiye sahiptir. 50% noktası bir seçimdir (% 10 olabilir,% 90); METR ayrıntılı kağıda birden fazla eşiği bildirir, ancak en sezgisel olduğu için % 50 ile liderlik eder.

> Logici olarak uygun şekil, genellikle tek bir şekilde artışa ve görevi zorluklara yöneliktir. %50'lik bir seçimdir. %10'a veya %90'a ulaşılabilir.

### 2026 Ocak sayıları

Zaman Uzaklığı 1.1:

> 按时间视野1.1:

- Claude Opus 4.6: Time Horizon 1.1 (Ocak 2026) itibariyle %50 güvenilirlik ile ~14 saat.
  ÇXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
- HCAST tarzı görevlerde iki katlama süresi: ~4.3 ay (130.8 gün) Time Horizon 1.1 tarafından bildirilen 2023 sonrası uyum için (Ocak 2026); ~7 aylık rakam Time Horizon 1.0'dan tam 20192025 uyum için ve TH1.1 ile 2023 sonrası sayı ile birlikte bildirilmiştir.
  Çinçe çeviride:HCAST 类任务的倍增时间:Time Horizon 1.1(2026年1月) raporunun 2023 后拟合上约 4.3 个月(130.8 天); yaklaşık 7 个月的数字是Time Horizon 1.0'ın tam 20192025 拟合, TH1.1'de 2023 后数字 ile birlikte rapor edilmektedir。

Bu, 15'inci aşamada bulunan diğer referansların belirli sayılarıdır. Anthropic'in RSP v3.0 (Denevi 19) ve DeepMind'in FSF v3 (Denevi 20) 'de eşiği değerlendirmeleri sağlayan ölçümlerden biri olarak alıntılanmıştır.

> Bunlar, 15 aşamasının geri kalan kısmının alıntılarının belirli sayılarıdır. Bunlar Anthropic RSP v3.0 (sınıf 19) ve DeepMind FSF v3 (sınıf 20) 'de değer değer değerlendirmesi ölçümlerinden biri olarak alıntılanmıştır.

### Benchmark suiteları

- **HCAST**: 189 görev, siber güvenlik, yazılım mühendisliği ve genel akıl yürütme alanında.
  Çeviri:**HCAST**Zaman: 1 dakika 8+ 小时专家时间──时间线数字背后主套件──
- **RE-Bench**: 71 ML araştırma- mühendislik görevleri insan uzmanı bir temel çizgi ile. Modelin AI R&D-4 e sahip olan ML T&D çalışmalarını yapabilecek-eceğini ölçer.
  Çeviri:**RE-Bench**:71 个带人类专家基线的机器学习研究工程任务―― AI R&D-4 值 
- **SWAA**: daha kısa görevler; ufak bir ufaklık eğriğinin alt ucunu kalibre etmek için kullanışlıdır.
  Çeviri:**SWAA**Kısa görev: Kısa görev; Kalkınma zamanı için kullanılır.

### Prototyp izleme değerlendirmeleri

20252026 METR çalışması, izleme-değerlendirme prototiplerini içeriyordu: bir monitör yan görev yapan bir modeli yakalayabilir mi (operatörün istediği dışında bir şey); ajan monitörden kaçıyor mu? Bular doğrudan OpenAI PF v2'deki "Kafetleri azaltma" kategorisini ve DeepMind FSF v3'deki yanıltıcı uyum izlemeyi besler (Desin 20).

> 20252026 METR 工作包括监控评估原型:监控器能否捕获模型执行副任务(操作员请求以外的事);Agent 能否规避监控器──这些直接进入 OpenAI PF v2'nin "破坏防护" sınıfı ve DeepMind FSF v3(第 20 课)

### Neden ufuklar üst sınırlar

- **Idealized tooling**Bu nedenle, bu işlerin yapılması için, modelin işlevlerini ve işlevlerini kontrol etmek gerekir.
  Çeviri:**理想化工具**: KİRİT görevleri modelin net araç ve iyi biçimlendirilmiş verileri sağlar.
- **No real consequences**Modelle hiçbir zaman gerçek bir müşteriye fatura çekmez, gerçek verileri silmez veya gerçek insanlarla temas etmez.
  Çeviri:**无真实后果**Modelle: Gerçek personellerle bağlantı kurmak veya gerçek verileri silmek için gerçek müşteriye hesaplama ücretlerini uygulamaktan geçerli değildir.
- **Eval-context gaming**Ders 1. Testlerde modeller farklı davranır. 2026 Uluslararası AI Güvenlik Raporu bunu empirize olarak belgelendirir.
  Çeviri:**评估上下文博弈**1. Sınıf: 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図
- **No legitimate user variance**Benchmark istekleri yapılandırılmıştır. Gerçek kullanıcılar belirsiz, bağlamlara bağlı istekler üretir.
  Çeviri:**无合法用户方差**KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİNİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ: KİŞ:

Uyumlu koşullarda kapasite tavanı ufaklık. Deployment güvenilirliği farklı bir sayı, daha düşük ve ekipler bunu bilmek için kendi dağılım ölçmek gerekir.

> 时间线是有利条件下能力上限――部署可靠性是不同的数字,更低,团队必须测量自己的分布以知晓――

### Dış değerlendirici durum

Dış değerlendirme önemlidir çünkü iç laboratuvarlar rapor ettikleri ölçümleri optimize etmek için teşviklere sahiptir. METR'nin bağımsızlığı  bir 501(c)(3) açıklanmış bir metodoloji ve eşcinsel inceleme makaleleriyle  yapısal hafifletme. Tek başına yeterli değildir (laborlar hala METR'nin gördüğünü kontrol eder), ancak hiçbir dış değerlendirme olmaktan kesinlikle daha iyidir.

> Dış değerlendirmeler önemlidir, çünkü iç laboratuvarın iyileştirilmiş raporlama göstergesi hareketleri vardır. METR'in bağımsızlığı 501(c) 3) 带声明方法论和同行评议论文是结构性缓解──它单独不够(实验室仍控制METR 看到什么),但比无外部评估严格更好──

### Uygulamalarda ufuk sayıları nasıl kullanılır

- **As a capability filter**: Eğer bir modelin ufukları önerilen bir görevin uzmanlık süresinden çok daha aşağıysa, onu kendiliğinden göndermeyin (Lesson 1'in beceri dosyası).
  Çeviri:**作为能力过滤器**Eğer model zaman çizgisi önerilen görevlerin uzman zamanından çok daha düşükse, kendiliğinden yayınlanmasına izin vermeyin.
- **As a trend indicator**: iki katlama süresi, yeni hafiflemeler olmadan da mevcut uygulama ne kadar süre güvenli kalacağını gösterir.
  Çeviri:**作为趋势指标**Bu yüzden, bu yeni bir çözüm bile uzun süreliğine güvenli kalmaya devam edecektir.
- **As a prior**Görev dağılımınız, araç kaliteniz ve dağıtım bağlamınız için ayarlayın.
  Çeviri:**作为先验**14 saatlik zaman çizgisi başlangıç noktasıdır. Görevlerin dağılmasına göre, araçların kalitesi ve dağıtımına göre, aşağıdaki yazılarını düşürür.

## Çerçeveyi kullanın.
```figure
a5-horizon-fit
```

## Kullan

`code/main.py`Yapısal bir sonuç kümesi verildiğinde görev başarısı ile logist zaman arasındaki lojistik bir uyum sağlar. 50% ufuk (METR başlığı), 10% ufuk (sağlam) ve 90% ufuk (önemli). Ayrıca eval-kontext oyunları ile başarının süsü olarak şişirilmesiyle ne değişiklikler olduğunu gösterir.

> `code/main.py`给定合成结果集实现任务成功率 vs log(专家时间) 的逻辑拟合――报告 50% 时间线(METR 标题) 、10% 时间线(保守) 、90% 时间线(乐观) ──

## İndirin . Ürünler .

`outputs/skill-horizon-interpretation.md`Bir satıcının ufuk iddiasını gözden geçirir ve referans değer iddiası ile uygulama gerçekliği arasındaki boşluk analizini yapar.

> `outputs/skill-horizon-interpretation.md`审查供应商时间线声明并产生基准声明与部署现实之间的差异分析──

## Egzersizler.

1. Çık .`code/main.py`- Düzeltme %50 ufkunun sentetik yer gerçeğiyle uyumlu olduğunu doğrulayın. Şimdi görev zaman çubuğunu yarıya indir. ufkun değişimi anlamlı bir şekilde tahmin ediyor mu?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ %50'lik time line match synthesis real value. ❖ Şimdi görev zamanının yarısını azaltmak; zaman çizgisinin tahmininin anlamlı bir değişimi olup olmadığını belirlemek.

2. METR'nin Time Horizon 1.1 blog yazısını okuyun. Güvenliğin en yüksek ve en düşük olduğu belirli görevleri belirleyin.
   Çinçe çevirisi:METR Zaman Uçaklığı 1.1 博客──识别可靠性最高和最低的具体任务──解释为什么存在差距──

3. METR'nin "Autonom Yapay zeka yeteneklerini ölçmek" kaynaklarını okuyun. HCAST görev kategorilerini listelenin. Bir üretim görevi için daha ağır ağır ağırlık vereceğiniz bir kategorisi seçin ve nedenini haklı çıkarın.
   Çinçe çevirisi:METR'in "Özünlü Yapay Yeteneklilik Ölçü" kaynağı.

4. Simülatörde eval-context oyunlarını kullanın: başarısız görevlerin %20'ini başarıyla döndürün. Yeni ufku rapor edin. Bu,%20'lik bir oyun oranının gözlemlenen sayıya ne yaptığını yakındır.
   Çin Çeviri: Önemli oyunlar: %20 失败任务翻转为成功.

5. Kendi hata arka kaydı veya temsilci bir görev kümesi üzerinde iç ufuk değerlendirmesini tasarlayın. Verilerin toplanmasını, uyumunu ve çıkışın size ne söylediğini açıklayın. METR sayıları ile karşılaştırın.
   Çinçe çevirisi: Öz bug backlog veya temsilcilik görev kümesi üzerinde tasarım iç zaman çizgisi değerlendirmek.

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| METR | "External evaluator" | ex-ARC Evals; independent 501(c)(3) since Dec 2023 | METR：原 ARC Evals，独立第三方 |
| Time Horizon | "Capability measure" | Expert task length at 50% reliability, from logistic fit | 时间线：50% 可靠性下专家任务长度 |
| HCAST | "METR's main suite" | 180+ tasks spanning 1 min to 8+ hours | HCAST：METR 主套件，180+ 任务 |
| RE-Bench | "Research engineering" | 71 ML research-engineering tasks with human baseline | RE-Bench：71 个机器学习研发任务 |
| SWAA | "Short-task suite" | Calibrates the low end of the horizon curve | SWAA：短任务套件，校准低端 |
| Doubling time | "Growth rate" | Time for the 50% horizon to double; ~7 months per HCAST | 倍增时间：50% 时间线翻倍所需时间 |
| Eval-context gaming | "Model behaves differently" | Documented behavior gap between tests and deployment | 评估上下文博弈：测试与部署行为差距 |
| Upper bound | "Horizon is a ceiling" | Benchmark horizon > deployment reliability under load | 上限：基准时间线 > 负载下部署可靠性 |

## Daha fazla okumak

- [METR — Resources for Measuring Autonomous AI Capabilities](https://metr.org/measuring-autonomous-ai-capabilities/) HCAST, RE-Bench, SWAA özellikleri.
  Çeviri:HCAST、RE-Bench、SWAA 规范
- [METR — Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) orijinal ufuk kağıdı.
  Çin Çeviri:原始时间线论文
- [METR — Time Horizon 1.1 (January 2026)](https://metr.org/research/) mevcut sayı ve yöntem.
  Çinçe Çevirimi: 当前数字和方法论
- [Epoch AI — METR Time Horizons benchmark](https://epoch.ai/benchmarks/metr-time-horizons)- Canlı izleme.
  Çin Çeviri:实时跟踪
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) METR'nin ölçümleri için iç perspektif.
  Çeviri:METR 测量的内部视角
