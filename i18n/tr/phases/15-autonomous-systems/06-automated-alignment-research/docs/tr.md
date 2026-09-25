# Otomatik Alignment Araştırması (Anthropic AAR)

> Anthropic, bağımsız kum kutularında Claude Opus 4.6 Autonomous Alignment Araştırmacılarının paralel ekiplerini çalıştı ve kayıtları herhangi bir kum kutuunun dışında yaşayan paylaşılan bir forum aracılığıyla koordine etti (bu nedenle ajanlar kendi kayıtlarını silemezler). Zayıf-güçlü eğitim sorunu konusunda AAR'lar insan araştırmacılarını geçirdi. İş akışlarını belirleyen Anthropic'in kendi özetli bayrakları genellikle AAR esnekliğini kısıtlar ve performansını düşürür. Otomatik ayarlama araştırması, RSP'nin tespit etmek istediği tam yanlış ayarlama risklerine kadar zaman çizgisini sıkıştırmak için baskı adımıdır.

> **【中文解读】**Antropik, bağımsız bir sandıkta bir çalışma süresi birçoğu Claude Opus 4.6 Özgür bir çalışma makinesi (AAR), herhangi bir sandık dışında bir kayıt kaydesi (depozit) oluşturur. Bu şekilde Agent, zayıf ve güçlü bir eğitim sorunu açısından, AAR, insan araştırmacılarından daha iyidir.

> **【拓展：自主研究 Agent 的双重性】**AAR'ın varlığı iki yönde: "kompresyon" ve "ikili kullanım" vardır:正面是能加速对齐研究;反面是同系统也能自动化"破坏对齐"。RSP, "AI R&D 自动化值"'nı yükseltme kontrolü başlatıcısı olarak kullanıyor, tam da bu karşılaştırma nedeniyle。Antropic 选择把日志放在外面的代理沙箱.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, parallel-research-forum simulator) | **语言:** Python（标准库，并行研究论坛模拟器）
**Prerequisites:** Phase 15 · 05 (AI Scientist v2), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 05（AI Scientist v2），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Özetleme: 15·05 (İL Bilimci v2  Açık Araştırma)  15·04 (DGM Öz-işim Değişim)  18·11 (Skalable Oversight 弱到强监督)  AAR = AI Bilimci "AI Güvenlik Araştırması Kendisi" için kullanılır 既是工具也是风险。
>  **【类比】**AAR = "AI  kendini yazıp test raporunu"──AI Bilimci v2 = AI Normal Bilim Araştırmaları yapması;AAR = AI Araştırmaları nasıl AI kendini daha güvenli hale getirebilir?── soru: Doktor kendini açıp kesebilir mi?Antropik tasarım = Çok sayıda AI ayrı bir kutuda bağımsız çalışma, forum üzerinden "forum" iletişim, ama forum日志 sandığın dışında mevcuttur.
> 🤔 **【困惑】**S: 既然 AI 能做对齐研究,为什么还需要人类?  AI 能加速但无法保证完整性──弱到强监督的根本困境 (düşünçli olarak güçlü bir şekilde denetleme yapılması gereken bir şey) 

## Sorunlar. Sorunlar.

> **【中文解读】**Otomatikleştirme 齐研究探求AI 系统是否能够自主发现和修复自身安全问题──核心问题是:AI 能否成为自己安全研究的助手?Anthropic 和 Redwood Research deneyleri, LLM'nin, 齐研究人员认为有用的安全洞见的产生可能,但还没有独立完成端到端安全研究的能力──

> **【拓展：automated alignment research】**Otomatisize karşı hazırlık çalışmaları 2025-2026 yıllarındaki AI güvenliği alanında bir sıcak noktadır. Antropik makalesinde AI'nin  Yardımcı  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli  Güvenli 

Düzeltme araştırması insan- araştırmacı zamanında pahalıdır.

> İnsan araştırmacıları için araştırma yapmak çok pahalı.

Ölçeklenebilir denetim, ödül özellikleri veya zayıf-güçlü eğitim gibi sorunlar, her tekrarlama için haftalar süren deneylere ihtiyaç duyar. Sınır yetenekleri ilerledikçe, uyum iş yükü nitelikli araştırmacıların tedarikinden daha hızlı büyür.

> Genişletilmiş gözetim, ödüllendirme kuralları veya zayıflıktan güçlü eğitim gibi sorunlar, her yıl bir dizi haftalık deney gerektirir.

Otomatik Alignment Research (AAR), aynı sınır modellerinin, sınırlandırmayı aşma kapasitesinin bu boşluğu kapatmaya katkıda bulunabileceklerini sorar. Anthropic'in AAR tarafından yürütülen zayıf-güçlü eğitim çalışması (alignment.anthropic.com/2026/automated-w2s-researcher/) hakkındaki 2026 raporu, bu sınıfın dağıtılmış bir sisteminden ilk kamu sonuçlarından biridir.

> Otomatik birleştirme çalışmaları (AAR) sorma yeteneği, aynı önde gelen modellerin birleştirme konusunda başarısının kapalı kesintinin katkıda bulunup bulunmadığını sormak için birleştirme çalışmaları (AAR) Antropik 2026 yılı AAR'ın zayıflıktan güçlüye kadar çalışması çalışmaları raporu bu sınıfın ilk açık sonuçlarından biridir.


> **【中文解读】**Bu bölümde, AI Güvenliği Teknolojisinin İnsan İstelikleri ve Değerlerine Uygun Olmasını Sağlayan Birimle İlgili bilgiler sunuldu.

Sonuç gerçekten olumlu: AAR'lar insan başlangıç çizgisinden daha iyi bir araştırma sorunu çözmüştür.

> Sonuç gerçek anlamda doğru: AAR, araştırma sorunlarında insan tabanından üstündür. Ancak bu sonuç, bu aşamada gelişen tüm ilgi noktalarının bir sistemde yoğunlaşmasını sağlayacaktır.

Eğer uyum araştırması otomatik hale getirilebilirse, korumaları tehlikeye atan parçalar da otomatik hale gelebilir.

> Eğer tüm araştırmalar otomatik hale getirilebilirse, bu güvenlik önlemlerinin bir kısmı da otomatik hale gelebilir.

## Konsepten bir şey.

### Yapı (açık açıklama)

- **Parallel agents.**Claude Opus 4.6'un birden fazla örneği, her biri bağımsız bir kum kutuunda AAR olarak çalışır. Kum kutuları dosya sistemini, ağını ve işlem yüzeyini sınırlandırır.
  Çeviri:**并行 Agent。**Çoğu Claude Opus 4.6  örnekleri AAR 运行, her biri bağımsız 沙箱中──沙箱限制文件系统、网络和进程表面──
- **Shared forum.**Bulgular her kum kutuunun dışında bulunan depolama arka planı bulunan bir paylaşılan forumda yayınlanır. Ajanlar forumı okuyabilir; Ajanlar kendi kum kutuları içinde forum kayıtlarını silemez veya düzenleyemez.
  Çeviri:**共享论坛。**Bulup paylaşım forumuna gönderilen, depolama son kısmı her kutu dışındadır.
- **Task allocation.**İnsan tasarımındaki görev kuyrukları AAR'lara araştırma sorunları atfeder. AAR'lar parçalanma önerileri, deneyler yürütmek, bulguları yazmak.
  Çeviri:**任务分配。**İnsanlık tasarımı görev sırası, araştırma sorunlarını AAR'a dağıtacak.
- **Weak-to-strong training focus.**Yayınlanan çalışma, zayıf-güçlü eğitimi  daha güçlü bir öğrenci modeli eğitmek için daha zayıf bir denetçi modelini kullanarak ele aldı.
  Çeviri:**弱到强训练聚焦。**Yayınlanan araştırmalar zayıf ve güçlü eğitimlere yöneliktir. Daha zayıf denetim modellerini kullanarak daha güçlü öğrenci modellerini eğitmek için AAR bu görevde insan araştırmacılarından üstündür.

### Neden kum kutusundan çıkmış günlük önemli?

Log-integritet özelliği, kontrol edilen bir deney ile potansiyel olarak tehlikeye girebilecek bir deney arasındaki farktır.

> Günlük tamamlayıcılık özelliği kontrol edilen deney ile olası hasarlı deney arasındaki farkı oluşturur.

Eğer AAR'lar kendi kayıtlarını düzenleyebilseydi, başarısız veya şüpheli deneyleri örtbas edebilirlerdi. Antropik bayraklar bunu doğrudan: mülkiyet araştırma sonuçlarına güvenmek için gerekli bir şarttır ve doğrulama önemsiz değildir.

> Eğer AAR kendi günlüğünü düzenleyebilirse, başarısızlıklarını veya şüpheli deneyleri örtbas edebilir.

Altyapı açısından analog sadece ekleme kayıtları dış depolama (örneğin S3 nesne kilitleme, değişmez Datadog kayıtları) ile yazılıdır. Ajanın geçmiş kayıtları değiştirmek için yetkisi yoktur. Bu 2026 kurumsal güvenlik ekiplerinin ransomware- dirençli denetim izleri yapmak için kullandığı aynı kalıp.

> 基础设施术语中的类比是写入外部存储的仅额外日志 (S3对象锁,不可变数据库日志)  Agent 无证证修改过去记录──2026 yılındaki Enterprise Security Team tarafından anti-勒索 yazılım denetim takipini oluşturma biçimiyle aynıdır──

### İş akışının belirlenmiş değişimi.

Anthropic'in raporunda belirtilmiş iş akışlarının genellikle AAR esnekliğini kısıtladığını ve performansı düşürdüğünü belirtiyor.

> Anthropic'in raporunda belirtildiği gibi, düzenli çalışma akımları genellikle AAR'ın çevikliğini sınırlandırır ve performansını düşürür.

Başka bir deyişle: insan tasarımcısı araştırma planını adım adım yazarsa, AAR'lar yüksek düzeyde hedefler ve parçalanma özgürlüğü verildiğinde daha kötü sonuçlar elde eder. Bu, ajan araştırmaları (LangGraph, Microsoft'un Agent Framework)  aşırı belirtilen asfaltlar yetenekli ajanları zarar verir.

> Başka bir deyişle: Eğer insan tasarımcısı aşamalı bir araştırma planı hazırlarsa, AAR'ın göstergesi yüksek seviyede hedef ve çözülme özgürlüğüne uygun değildir. Bu, Ajanlı çalışmaların sonuçlarına uymaz.

Güvenlik anlamı ince. AAR performansını iyileştiren esneklik aynı zamanda onaylanmamış parçalanma, yeni araç kullanım ve hedef kaydırma izin veren esnekliktir.

> Güvenlik anlamı inceliklidir. AAR'ın seks enerjisinin esnekliğini yükseltmek, yetkisiz parçalanmalarına da izin verir. Yeni araçların kullanımı ve hedeflerin hareket etmesine de izin verir.

### Sıkıştırma riski.

RSP v3.0 (Desin 19) bir AI R&D yetenek eşiği tanıttı: rekabetçi maliyet vs. insan + AI araçları ile AI R&D borusunu tamamen otomatikleştirme yeteneği. DeepMind'in FSF v3 benzer bir ML R&D özerklik seviyesini içerir. Her iki çerçeve de bu eşiği yükseltilmiş kontrollerin tetikçisi olarak ele alıyor.

> RSP v3.0 (第 19 课) AI R&D 能力值: İnsan + AI 工具竞争的成本下完全自动化 AI R&D 管道的能力──DeepMind'in FSF v3 类似的 ML R&D 独立级别──两框架都将此值视为升级控制的触发器──

AAR, eylemi bir adım daha azdır: borunun bir kısmını otomatikleştirir (özel, iyi kapsamlı görevler üzerinde uyum araştırmaları), ancak son-son kapasite geliştirme döngüsünü değil.

> AAR 离值一步之遥: zaman çizgisi sorunu, farkın hızla kapatılması değil, belirli 范围明确任务上的对齐研究的部分 (特定、范围明确任务上的对齐研究) olarak otomatikleştirilmiş bir borunun parçasıdır.

Sıkıştırılmış zaman çizgileri, birleşme başarısızlığı endişesi. Düzeltme araştırmaları ve kapasite araştırması benzer hızlarla birleşirse, yanlış uyum sağlama riski yüzeyi, kapasite kadar hızlı büyür. Eğer yetenekler daha hızlı bir şekilde (tarihi eğilim) artarsa, fark genişler. Bu, AAR'ın nitelikli bir mal olması için bir argüman: Her ek uyumlandırma sonucu, araştırma sürecinin güvenilir olması durumunda ve yalnızca bu sürece farkı azaltır.

> 压缩时间线是复利失败担忧―― eğer 齐研究和能力研究对相似速率复利,对不齐风险表面至少与能力一样快速增长――如果能力更快复利 (capacity) 历史趋势),差距扩大―― bu AAR 作为"有限好"论文:

### AAR'ın yerini alamadığı şey AAR'ın yerini alamadığı şey

İnsan araştırmacıları görev sırasını belirler, sonuçları gözden geçirir ve anayasa yetkisini tutar.

> İnsan araştırmacıları görev sırasını belirler, sonuçları inceler ve anayasa yetkisine sahiptir.

AAR'lar, sonları değil, boru hattının ortasını hızlandırır. Anthropic'in yayınlanan çıkışları hem AAR katkılarını hem de neyi yayınlayacağı, neyi geri çekeceği ve neyi geliştirmesi gerektiği konusunda insan-kalip yargısını içerir.

> AAR, iki taraf yerine bir hızla tüpünün orta kısmını oluşturur. Antropik  yayınlanan çıkışlar AAR katkılarını ve neyi yayınlamak, neyi geri çekmek, neyi tamamlamak hakkında insan araştırmacılarının kararlarını içerir.

Bu, araştırmaya uygulanan Ders 15'in önerme-doğrusu-yaptırma örneğine uyuyor: AAR'lar önerir; insanlar görev yapar.

> Bu, 15. Sınıf ile birlikte önerilen ve sonra yapılan bir proje modelinin kendiliğinden çalışmaya uygulanmasıdır.

## Çerçeveyi kullanın.
```figure
aar-forum
```

## Kullan

`code/main.py`Üç bağımsız " araştırma ajanı " paralel olarak çalışarak bulguları yalnızca ekleme forumuna, seçmeli bozukluk denemeleri ile yayınlar.

> `code/main.py`模拟多 AAR 研究论坛──三个独立"研究代理"并行运行,将发现发布到带可选改尝试的仅额外论坛──

- Gözleyin.

> 观察:

- Kum kutusundan çıkmış kayıplar kayıpları bozmaktan nasıl kaçınıyor?
  Çinçe Çevirimi:沙箱外日志 nasıl yakalamak 図書 改尝试。
- Özgür parçalanma ile görev dağılımı daha zor sorunlar üzerinde sabit iş akışlarını nasıl üstlenir.
  Çinçe çevirisi:带自由分解的任务分配如何在更难问题上优于固定工作流──
- Bir tek compromised AAR forum sinyalini bulaştırır nasıl eğer kayıt tamir edici değilse.
  Çinçe Çevirisi:日志不可改时,单个被攻破的 AAR 如何污染论坛信号──

## İndirin . Ürünler .

`outputs/skill-aar-deployment-review.md`otomatik uyumlama-kağıt araştırma hattının, yerleştirilmeden önce bir incelemesi.

> `outputs/skill-aar-deployment-review.md`Bu, bir araştırma sisteminin otomatikleştirilmesi ve kontrol edilmesi için bir düzenleme yapılmasıdır.

## Egzersizler.

1. Çık .`code/main.py`"Sıkı iş akışı" ile "savaşsız parçalanma" ayarlarını karşılaştırın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ "Sıkı çalışma akımı" ile "Özgür çözüme kavuşturma" ayarlarını karşılaştırın.

2. Simülatörü değiştirin, böylece bir ajan kayıt kayıtlarını değiştirmeye çalışır. Sadece eklenen kayıt kayıtlarını tespit etmesini onaylayın.
   Çinçe çevirisi: Modify模拟器让一个代理 尝试日志改──确认仅增加日志检测到──写一段准确描述日志中检测签名的外观──

3. Anthropic'in zayıf-güçlü AAR raporunu okuyun. AAR'ların insan araştırmacılarını yendiği belirli alt görevi belirleyin.
   Çin dilinde: 阅读 弱到强 AAR 报告──识别 AAR 击败人类研究者的具体子任务──什么让它适合自动化?

4. AAR esnekliğini (yani daha iyi sonuçlar) belirlenen iş akışı kısıtlamalarıyla (sederce denetim) dengeleyen görev sırası tahsis politikası tasarlayın.
   Çinçe çevirisi: design balancing AAR 灵活性(更好结果) 规范工作流约束(更易审计) 任务队列分配策略──描述如何A/B 测试两者──

5. RSP v3.0'un AI R&D-4 eşiğini okuyun. Bir paragrafda, AAR'ın şu anda yapmadığı aşmayı düşündüğünüz şeyi açıklayın.
   Çin dilinde: RSP v3.0'un AI R&D-4  değerini okuyun.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AAR | "Automated Alignment Researcher" | Claude Opus 4.6 instance operated autonomously on alignment problems |
| AAR | "自动化对齐研究器" | 在对齐问题上自主操作的 Claude Opus 4.6 实例 |
| Weak-to-strong training | "Training a stronger model with a weaker supervisor" | Classic scalable-oversight benchmark AARs outperformed humans on |
| 弱到强训练 | "用较弱监督者训练较强模型" | AAR 击败人类的经典可扩展监督基准 |
| Shared forum | "Where agents publish findings" | Append-only, out-of-sandbox storage |
| 共享论坛 | "Agent 发布发现之处" | 仅追加、沙箱外存储 |
| Out-of-sandbox log | "Agent cannot edit its own record" | Tamper-evident write-through to external storage |
| 沙箱外日志 | "Agent 不能编辑自己的记录" | 写入外部存储的防篡改透写 |
| Prescribed workflow | "Step-by-step plan from human designer" | Constrains AAR; often degrades performance vs free decomposition |
| 规定工作流 | "人类设计者的逐步计划" | 约束 AAR；通常比自由分解降低性能 |
| Free decomposition | "Agent decides how to break the task" | More capable, harder to audit |
| 自由分解 | "Agent 决定如何拆分任务" | 更有能力，更难审计 |
| AI R&D threshold | "RSP/FSF capability level" | Full automation of R&D pipeline at competitive cost |
| AI R&D 阈值 | "RSP/FSF 能力级别" | 在竞争成本下完全自动化 R&D 管道 |
| Compressed timeline | "Alignment vs capability race" | If capability compounds faster than alignment, misalignment risk grows |
| 压缩时间线 | "对齐与能力竞赛" | 若能力比对齐复利更快，不对齐风险增长 |

## Daha fazla okumak

- [Anthropic — Automated Weak-to-Strong Researcher](https://alignment.anthropic.com/2026/automated-w2s-researcher/) İlk kaynak.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çev
- [Anthropic Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) AI Araştırma ve Gelişim Eğlence Çelişkisi çerçevesinde.
  Çin dilinde: AI R&D  değer çerçeve
- [Anthropic — Measuring AI agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) daha geniş bir ajan-özerk çerçevesini oluşturmak.
  Çinçe Çevirisi:更宽的代理自主性框架──
- [DeepMind Frontier Safety Framework v3](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) ML Araştırma ve Gelişim özerkliği seviyeleri RSP ile paralel.
  Çinçe Çevirimiçi: RSP 平行 ML R&D 自主级别──
- [Burns et al. (2023). Weak-to-Strong Generalization (OpenAI)](https://openai.com/index/weak-to-strong-generalization/) AAR'ların saldırdığı temel sorun.
  Çeviri:AAR  saldırının alt katı sorunları
