# Paylaşılan hafıza ve tablo kalıpları .

> 2026'da çoklu ajan sistemlerinde iki yaklaşım bir arada var:**message pool**(Herkes herkesin mesajlarını görür, AutoGen GroupChat veya MetaGPT gibi) ve **blackboard with subscription**(Ajanslar Kontext-Aware MCP veya Matrix çerçevesinde olduğu gibi ilgili olaylara abone olurlar). Her ikisi de çoklu ajanlı bir sistemin tek durumlu parçası  yani ikisi de ilginç hataların yaşadığı yerdir. İpucu hata modusu **memory poisoning**Bu ders, her iki yapıyı stdlib'den inşa eder, zehirleme saldırısı enjekte eder ve üretimde gerçekten çalışan üç hafiflemeyi gösterir.

> **【中文解读】**Bu bölümde paylaşım anı ve blackboard sistemleri 多代理 系统中的共享知识库和协调机制介绍.

> **【拓展：shared memory blackboard→具体应用】**共享记忆/黑板模型是多代理 系统的经典协调机制所有代理 读写一个共享的知识库――黑板模型来自1980'lerin İşitme-II 语音识别系统――现代实现包括 Redis 共享状态、向量数据库和MCP Resources――优势是简单,劣势是竞争条件(多代理 同时写入) ――


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `threading`) | **语言:** Python (标准库, `threading`)
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 04 (原语模型), Phase 16 · 09 (并行群体网络)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前 請先掌握:Phase 16·04(原语) 、Phase 16·09(Swarm) 、并发编程(锁、竞态) 。共享记忆 = 多 Agent 协调的核心数据结构──
>  **【类比】**共享记忆两种模式 = "办公场景"──消息池(AutoGen GroupChat) = 开放办公区(大家都听);黑板+订阅(Context-Aware MCP) = 公告板(按订阅推送)──失败模式 = 记忆投毒(1 Ajan 幻觉,其他 Ajan 当真) 比崩更难调试──修复:版本号 + 来源标记 + 多源验证──

## Sorunlar sorunun giriş

Çoklu ajan sistemleri, ajanların gerçekleri paylaşması için bir yere ihtiyaç duyar. Sözcük bir seçenek "her şeyi mesajlarda geçiyor"  ancak ekstra kopyalama ile paylaşılan durumu yeniden icat ediyor. Başka bir seçenek ise "herkese küresel bir günlük ver"  ama küresel günlükler sınırsız büyüyor ve kolayca zehirlenir. Üçüncü bir seçenek ise "bir ajan için bir görüntü projesi"  ölçeklenebilir ancak şema ağır.

> Çoğu Ajan  sistem bir yer gerektirir Ajan paylaşmak için gerçeği paylaşmak için. Bir yazı seçeneği "her şeyi haberde aktarmak"  ama bu yeniden icat edilmekle ek olarak kopyalanmış paylaşma durumu gibidir. Diğer bir seçenek "her bireye bir tümleşik günlüğü vermek"  ama tümleşik günlüğü sınırsız büyümek ve kolayca kirlenmek için  üçüncü bir seçenek "her bir Ajan için bir görüntü  yayılabilir ama çok sayıda model tasarımı gerektirir".

Üç seçenek klasik bir dağıtılmış sistem pazarlamasını izler: ucuz ama kırılgan (erzonlar), basit ama ölçeklenemez (global log), ölçeklenebilir ama sert (per-agent projeksiyonları).

> Üç seçenek geçmişi klasik dağıtımlı sistem ağırlığı: ucuz ama kırılgan(消息) 、 basit ama genişletmez 、 tüm alanı 日志) 、 genişletilebilir ama 化 、 her ajanı 投影) 、 hiçbir seçenek yoktur ▽

Bu durumun farkına varan her aşağı akımlı ajan, halüsinasyonu gerçek olarak kabul eder. İnsan farkına varırken, mantık zinciri beş adım derinlikte ve kök neden ise yazılmış üçüncü mesajdır.

> Bir Ajan 幻觉并将幻觉写入共享状态时,每个读取该状态下游 Ajan 都市将幻觉作为事实采纳. İnsan fark ettiğinde, düşünce zinciri zaten beş adım derin bir şekilde oluştu.

Bir kaza size bir sürü iz verir. hafıza zehirlenmesi size güvenle yanlış bir rapor verir.

> 崩给你堆跟踪――内存污染给你自信错误报告―― birincisi birkaç saniye içinde kontrol edilebilir; ikincisi ise orijinal görünümlere kadar birkaç gün sürecek bir veriş işlemi gerektirebilir――

Bu hafıza zehirlenmesidir. MAST taksonomisi'nde ikinci en çok belgelenen başarısızlık ailesi (Cemri ve diğerleri, arXiv:2503.13657) ve yapısal: Kaynaksız ve yazılamaz bir doğrulayıcı olmayan herhangi bir paylaşılan hafıza tasarımı sonunda onu gösterecektir.

> Bu, bir sonraki aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir diğer aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşamada, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aşanda, bir aş aş

## Konsept merkezi konsept

### İki ana topolojisi

**Full message pool.**Her ajan her mesajı okuyor. AutoGen GroupChat ve MetaGPT bunu kullanıyor. Basit, şeffaf, denenebilir, ancak her ajansın bağlamı diğer ajansların çalışmalarıyla dolduğu için ~ 10 ajandan daha fazla ölçeklendirmeyi gerektirir.

> **完整消息池。**Her Ajan 读取每条消息──AutoGen GroupChat 和 MetaGPT kullanımı bu şekilde──简单,透明,可检查,但不能扩展到约10 Ajan以上,因为每个 Ajan的上下文会填满其他 Ajan的工作──

**Blackboard with subscription.**Ajanlar konulara ilgi gösterdiğini belirtir; altyapı yolları sadece ilgili mesajlar gönderir. CA-MCP (arXiv:2601.11595) ve Matrix merkezi olmayan çerçeve (arXiv:2511.21686) bunu kullanırlar. Daha fazla ölçeklendirir, ancak abonelikleri anlamlı hale getirmek için önceden şema tasarımı gerektirir.

> **带订阅的黑板。**Agent                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

### Her biri kazanırken

- **Full pool**Bu nedenle, bu konuyu ele almak için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek için, bir araya gelmek, bir araya gelmek, bir araya gelmek için, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelmek, bir araya gelebilir.
  Çeviri:**完整池**Bu yüzden, bu konuyu ele alalım.
- **Blackboard**Bu nedenle, bu konularda, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, birbiriyle ilgili olarak, bir diğerine benzer şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, ( ( ( ( ( (a) olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak, olarak,
  Çeviri:**黑板**Bu nedenle, bu durumun bir parçası olarak, bir diğer rolü de var.

Üretim sistemleri genellikle karışır: üstte küçük bir tam havuz (planlama katmanı), altta kara tahtlar (işçi katmanı).

> 生产系统通常混合使用:顶部一个小的完整池 (上部一个小的完整池) (→ 下面是黑板 (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是黑板) (下面是工作器层) (下面是)

Bu hibrid, Anthropic'in Araştırma sisteminin yaptığı şeydir: bir denetçi (bir kaç lider ajan arasında tam bir havuz) alt üyeler (her biri kendi kapsamlı bağlamı, kardeşlerden izole edilmiştir) için delegeler.

> Bu tür bir karışım Antropik Araştırma Sisteminde yapılır: İzleyici (Supervisor) 少数主导代理 之间的完整池) 委派给子代理 (委派给子代理) 每个有自己的范围上下文,与同级隔离) 顶部需要完全透明进行综合;工作器需要隔离以专注──

### Bir senaryoda hafıza zehirlenmesi

Üç ajan araştırma görevi üzerinde çalışıyor A ajanı bir kurtarma ajanı B ajanı bir özetleyici C ajanı bir analist.

> Üç Ücü 处理一个研究任务──Agent A检查剂──Agent B摘要器──Agent C analizt──

1. Bir sayfa getirir ve paylaşılmış durumlara bir mesaj yazar: "Çözüm, %42 doğruluk iyileştirdiğini bildirir".
   Çinçe Çevirimiçi:Bir sayfa elde etmek ve paylaşım durumuna girmek için bir araştırma raporunda %42 doğruluk oranı artmıştır.
2. Aldığım sayfada aslında "% 4,2 iyileşme" yazıyordu.
   Çinçe Çevirisi: elde edilen sayfa aslında "4.2% 提升──" bir hayal bir küçük sayı──
3. B, paylaşılan durumu okuyarak şöyle yazıyor: "Kesinlik artışı %42 oranında rapor edildi (kaynak: A). "
   Çinçe Çevirimiçi:B 读取共享状态,写入:" rapor etti 42% 准确率提升(来源:A) 』
4. C, paylaşılan durumu okuyarak şöyle yazıyor: "Tavsiye edin  42% yükseltme dönüştürücüdür".
   Çinçe Çevirisi:C 读取共享状态,写入:"建议采纳42% 的提升是变革性的。"
5. Son rapor hiçbir zaman var olmamış olan %42'lik bir rakamdan söz ediyor.
   Çin dilinde: "Yöntemel rapor"da hiç var olmayan %42 sayı alıntılandı.

Hiçbir ajan çökmedi, hiçbir test başarısız olmadı, sistem "işledi" halüsinasyon bir ajanın bağlamından, ortak bir durum yoluyla her aşağı akımdaki ajanın mantığına geçti.

> 没有 Agent 崩──没有测试失败──系统"工作"了──幻觉通过共享状态从一个代理的上下文进入每个下游代理的推理──

Bu nedenle hafıza zehirlenmesi hilelidir: hiçbir kaza, hata, uyarı yoktur. Sistem güvenle yanlış bir rapor üretir. Onu tespit etmenin tek yolu, her gerçeği ilk kaynaklardan yeniden çıkarmaktır.

> Bu yüzden, içi kirlilik nişanı: çöküş yok, hata yok, uyarı yok. Sistem güven hatası raporları oluşturur.

### Bu neden yapısal?

A'nın halüsinasyonları A'nın bağlamında kalır. Aşağı akımdaki ajanlar tekrar alacak veya yeniden çıkarabilir ve hatayı yakalayabilir. Saçma ortak durumla A'nın bağlamı herkesin bağlamına dönüşür ve halüsinasyon gerçeklere yıkılır.

> 没有共享状态,Agent A'nın hayaleti A'nın üst下文中停留在 A'nın üst下文中. 下游 Agent 会重新获取或重新推导并可能捕获错误.

Sorun ortak devlet değildir.**without provenance and without an independent verifier**Üç hafifleme yolu:

> 问题不是共享状态本身而是**没有来源追溯和没有独立验证器**Bu sorunu çözmek için üç farklı çözüm önlemi:

Her bir hafifleme farklı bir başarısızlık modunu hedef alır. Provence hataları geri izlemenizi sağlar. Versiyonlama denetim izini korur. Yazılmayan doğrulayıcı bağımsız bir kontrol sağlar. Birlikte zehirlenmeye karşı derin bir savunma oluştururlar.

> Her türlü başarısızlık modülüne yönelik bir çözüm önlemleri vardır.

1. **Attribute provenance on every write.**Paylaşılan devlet kayıtlarında bulunan her giriş, kim yazdı, ne zaman, hangi çağrı altında ve (mümkünse) ajanın hangi kaynağı belirtti.
   Çeviri:**每次写入时归属来源。**Ortaklık durumundaki her bir madde kayıt kim yazdı, ne zaman neyi önerdi, ve eğer geçerli ise, Ajan neyi belirtti.
2. **Version writes; treat them as append-only.**Düzeltme, eski bir giriş yerine yeni bir girişdir, yerleşik bir güncelleştirme değil.
   Çeviri:**版本化写入；视为仅追加。**修正是一个取代旧条目的新条条,不是原地更新──审计跟踪被保留──
3. **Keep at least one agent that cannot write to shared state.**Sadece okuyabilen bir doğrulama aracı girişleri örnekler, kaynakları yeniden alır ve tutarlılıkları işaretler.
   Çeviri:**保留至少一个不能写入共享状态的 Agent。**Sadece okuyucu Ajan 采样条目、重新获取来源并标记不一致──因为它不能写入池,所以不能被池污染──

### Blackboard precedeni (Hayes-Roth, 1985)

Blackboard örneği, LLM ajanlarından dört yıl önceydi. Hayes-Roth (1985, "Control için bir Blackboard Arsitekturası") küresel bir blackboard gözlemleyen, kısmi çözümlere katkıda bulunan ve diğer kaynakları tetikleyen uzman Bilgi Kaynaklarını tanımladı. 2026 kara tahtası (CA-MCP, Matrix) Bilgi Kaynakları ve kısmi çözümler olarak JSON blobları ile LLM ajanları ile aynı kalıptır. Eski edebiyat, modern sistemlerin yeniden keşfettiği tartışma, fırsatçı kontrol ve tutarlılık yazmak için çözümler belgelemiştir.

> 黑板模式比LLM Agent早了四十年. Hayes-Roth ((1985, "A Blackboard Architecture for Control") tüm bölgeyi gözlemleme黑板、贡献部分解决方案并触发其他来源的专业知识源.

Hearsay-II'den ders (70'li yılların konuşma tanıma tahtası): fırsatçı kontrol  tetikleme durumuna uygun olduğunda herhangi bir Bilgi Kaynağı tetiklemeye izin vererek  ortaya çıkan sorun çözümü üretir.

> Dinleme-II(1970'lerin çağının sesli tanımlama 黑板) öğretisi: fırsat kontrolü  herhangi bir bilgi kaynağını onun 触发条件匹配时触发产生涌现问题解决──硬编码工作流图的现代代理系统失去了这一点──黑板的灵活性是其核心创新──

### Projection vs. Full View

Temiz bir tahta her aboneye aynı projeksiyonu verir (topik boyutunda).**per-agent projection**LangGraph'in durum azaltıcıları, kanonik 2026 uygulamasıdır  azaltıcı fonksiyonu küresel durumu rolü özel bir parçaya katlar.

> 純黑板給每個購買者相同的投影 (Bütün temalar aynı şekilde) 更多的激進的設計是**每个 Agent 投影**: Her Ajan, rolüne göre düzenli olarak görüntülenir. LongGraph'in durum kaydını oluşturan kaydın 2026 yılındaki tipik gerçekleşmesi.

Bir ajan projesi daha da genişleşiyor ama bir şema gerek.

> Her Ajanın önerisiyle geçici projeyi yeniden inşa etmelisin.

### Yazıcı içerik biçimleri

Aynı anda birden fazla ajan yazmak sadece bir LLM sorunu değil aynı anda bir sorun.

> Birçok Ajan Aynı Zamanda Yazmak Bir İşleşme Sorunu, Sadece LLM Sorunu Olmuyor.

- **Sequential writer (single producer).**Tüm yazılar bir koordinatör aracı aracılığıyla seriye geçiyor.
  Çeviri:**顺序写入者（单一生产者）。**Tüm yazılar bir koordinasyon ajanı tarafından yapılır.
- **Optimistic concurrency with versioning.**Her giriş bir versiyonunu içerir; yazarlar versiyon eşleşmezliği ve yeniden deneme konusunda başarısız olurlar.
  Çeviri:**带版本控制的乐观并发。**Her bir başlıkta bir versiyon vardır; yazıcılar versiyon eşleşmezken başarısız ve tekrar deneler.
- **Topic partitioning.**Farklı ajanlar farklı konuları var, konuların çapraz tartışması yok, tasarlanmış bölüm sınırları gerektirir.
  Çeviri:**主题分区。**Çeşitli Ajanlar  farklı konuları vardır  hiçbir konu çatışması yoktur                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

2026 çerçevelerinin çoğu, sıralı yazar için varsayımlı çünkü LLM aramaları yeterince yavaş olur ki tartışma nadirdir ve şişe boynuzunun zarar vermemesi.

> Büyük çoğunluk 2026  framework默认使用顺序写入者, çünkü LLM 调用足够慢,冲突很少,瓶不影响.

Eğer bir tartışma (yüksek throughput sürüsü, paralel araştırma ajanları bulguları yazarken) yapıyorsanız, konu bölünmesi genellikle en ucuz çözümdür.

> Eğer gerçekten çatışmaya rastladığınızda, konu bölümü genellikle en ucuz düzeltme olur.

### Yazılmayan doğrulama

En yük taşıyan hafifleme, sadece okunur verifikatördür.

> En önemli hafifleme önlemleri sadece okuyucularındır.

- Verifiyeci, takımla durum paylaşıyor (çapayı veya havuzu okuyor).
  Çinçe Çevirimiçi:验证者与团队共享状态 (BİLİK)
- Verifier'ın yalnızca ayrı bir doğrulama kanalı için paylaşılan  durumu yazma elmi yoktur.
  Çinçe çevirisi: testçi ortak durumuna bir tek test yolu vardır.
- Verifier, yazılardaki kaynakları bağımsız olarak alır.
  Çinçe Çevirisi:验证者独立获取写入中引用的来源──标记不一致──
- Verifier'ın kendi çıkışları bir insan veya ayrı bir karar verme ajanına yönlendirilir ve asla havuza geri verilmez.
  Çinçe Çevirimi: Testçi kendi çıkarını insan veya tek başına karar verme yetkililerine yöneltir, asla geri dönmez.

Bu ayrım olmadan, doğrulayıcının çıkışları havuzda yeni girişler haline gelir, yani zehirli bir havuz doğrulayıcıyı zehirler ve bu da doğrulamalarını zehirler.

> Bu ayrım olmadan, denetçinin çıkışı havuzdaki yeni maddeye dönüşür, bu da kirlenmiş havuzun denetçiyi kirlettiğini ve böylece de onun onayını kirlettiğini gösterir.

Bu yazılmayan doğrulayıcı ilkesidir: denetçi yalnızca denetlenen sistemle ilgili olarak okunmalıdır. denetçiyi uzatsın ve denetimi tehlikeye atarsın. Bu ilke herhangi bir doğrulama rolüne uygulanır  denetlediği sistemden çıkışlarını ayırın.

> Bu yazılmamalı bir denetçi prensibi: denetçi sadece denetlenmiş sistemle okumalıdır.

## Yapın.
```figure
swarm-blackboard
```

## Yapın

`code/main.py`Stdlib Python'da her iki topolojinin de uygulanması, oyuncak zehirlenme saldırısı ve üç hafifleme.

> `code/main.py`Python standart kütüphanesi ile iki tür saldırı ve bir oyuncak kirliliği saldırısı ve üç tür yumuşak başlılık önlemleri gerçekleştirildi.

- `MessagePool` tam okunma ile sadece iplik güvenli ekleme kayıt.
  Çeviri:`MessagePool` 线程安全的仅额外日志,支持完整读取──
- `Blackboard` Konuya bağlı pub/sub, ajan aboneliği ile.
  Çeviri:`Blackboard`                                                                                                                                                                                                                                                              
- `ProvenanceEntry` her yazış kaydı (yazar, zaman damgası, prompt_hash, source_uri).
  Çeviri:`ProvenanceEntry`                                                                                                                                                                                                                                                              
- `PoisoningScenario` A ajanının bir onluk halüsinasyonunu gerçekleştirdiği üç ajanlı bir araştırma görevi yürütür.
  Çeviri:`PoisoningScenario` 运行三 代理研究任务,其中 Agent A 幻觉一个小数点――印最终报告――
- `Verifier` Kaynakları tekrar arayan ve tutarlılıkları işaretleyen sadece okuyabilen bir ajan.
  Çeviri:`Verifier` Bir yeniden elde edilen kaynak ve belirlenmeyen tek bir vekil.

Beklenen üretim:
- 1. Atış (verifikatör yok): halüsinasyonlu %42 son rapora yayılır.
  Çinçe Çevirimiçi:运行 1(无验证者):幻觉的 42% 传播到最终报告──
- 2. Çıkış (verifici ile): verifici tutarlılıktan haberdar olur, havuz "flagged" olarak etiketlenir, son rapor geri çekilmeyi içerir.
  Çin dilinde:运行 2(有验证者):验证者标记不一致,池被标记为"已标记",最终报告包含撤回──

## Çerçeveyi kullanın.

`outputs/skill-memory-auditor.md`Bir multi-agent sisteminin ortak hafıza tasarımı, kaynak, versiyonlama ve doğrulayıcı ayrımı için denetleme becerisi.

> `outputs/skill-memory-auditor.md`Bu, bir yetenektir, bir çok Ajanın  Sisteminin ortak belleği tasarımında kaynakları takip ederken                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

## İndirin . Ürünler .

Ortak bellek tasarımları için:

> 对于任何共享内存设计:

- Her yazıda kaydedilen yer: `(writer, timestamp, prompt_hash, tool_calls_cited, source_uri)`- Evet .
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`(写入者, 时间戳, prompt_hash, 引用的工具调用, source_uri)`- Evet.
- Düzeltmeler, değiştirilen bir yere atıfta bulunan yeni yazılardır.
  Çinçe Çevirisi:使日志仅追加──修正项是引用被取代项的新条目──
- En az bir okunma-tek verifiye aracı, bağımsız kaynak erişimine sahip olarak kullanın.
  Çinçe Çevirisi: deployment en az bir bağımsız kaynaklı ziyaretçi-tekliçli muhalif ajanı vardır.
- Yol doğrulayıcısı, paylaşılmış havuza geri dönmek yerine ayrı bir kanala çıkıyor.
  Çinçe çevirisi:将验证者输出路由到单独通道,而不是回到共享池──
- Yasaklık olan yazılar oranını kaydetmek  artış oranı halüsinasyon kalıplarının erken kanıtlarıdır.
  Çinçe Çevirisi: kayıt kapsamı yazma oranı artış oranı hayali modunun erken kanıtlarıdır.

## Egzersizler.

1. Çık .`code/main.py`1. koşunun halüsinasyonu yaydığını ve 2. koşunun onu yakaladığını onaylayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖
2. İkinci bir halüsinasyon ekleyin: ajan B bir veri kümesi boyutunu icat eder. Verifikatör her ikisini de elle ayarlamadan yakalamalıdır.
   Çin dilinde: Add a second illusion:Agent B 虚构一个数据集 大小──验证者应捕获两者而无需针对任何一个手动调优──
3. Tüm havuzu konu bölümü olan bir tahtaya geçirin (`prices`- Evet .`summaries`- Evet .`analyses`Hangi zehirlenme senaryoları, bölünme olayları zorlaştırır ve hangi senaryolarda yardımcı olmaz?
   Çin Çeviri:                                                                                                                                                                                                                                                            `prices`- Evet.`summaries`- Evet.`analyses`(■) Hangi ilaçlar daha zor uygulanıyor, hangilar daha zor?
4. Hayes-Roth (1985, "Control için bir Blackboard Arsitekturesi") okuyun. 2026 sistemlerinin yararlanabileceği bu dersde tartışılmamış makaledeki iki kontrol kalıpını belirleyin.
   Çinçe Çevirimi Çevirisi: Hayes-Roth okuyun, 1985), "Control için bir Blackboard Arsitekturası")
5. CA-MCP (arXiv:2601.11595). Paylaşılan Konteks Depoyu'nu ya MessagePool ya da Blackboard sınıfına yerleştirin `code/main.py`CA-MCP'nin üst kısmına hangi primitifler eklendi?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç`code/main.py`İçinde Mesaj Havuzu veya Kara Çizgi Klası. CA-MCP'nin üzerine hangi orijinal diller eklendi?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Append-only log that every agent reads. Full transparency, poor scaling. / 每个 Agent 读取的仅追加日志。完全透明，扩展性差。 |
| Blackboard / 黑板 | "Shared workspace" / "共享工作区" | Topic-keyed pub/sub. Agents subscribe to relevant topics. Scales farther. / 基于主题的发布/订阅。Agent 订阅相关主题。扩展性更好。 |
| Provenance / 来源追溯 | "Who wrote what" / "谁写了什么" | Metadata on each write: writer, timestamp, prompt, sources. / 每次写入的元数据：写入者、时间戳、提示、来源。 |
| Memory poisoning / 内存污染 | "Hallucinations spreading" / "幻觉传播" | One agent's error enters shared state, downstream agents adopt it as fact. / 一个 Agent 的错误进入共享状态，下游 Agent 将其作为事实采纳。 |
| Append-only / 仅追加 | "No in-place updates" / "无原地更新" | Corrections are new entries that supersede. Preserves audit trail. / 修正项是取代旧条目的新条目。保留审计跟踪。 |
| Unwritable verifier / 不可写验证者 | "Independent auditor" / "独立审计者" | Read-only agent that re-fetches sources and flags inconsistencies. / 重新获取来源并标记不一致的只读 Agent。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Per-agent view computed from global state. LangGraph reducers are the canonical case. / 从全局状态计算的每个 Agent 视图。LangGraph 归约器是典型实现。 |
| Knowledge Source / 知识源 | "Specialist agent" / "专家 Agent" | Hayes-Roth's 1985 term for a blackboard participant. / Hayes-Roth 1985 年对黑板参与者的称呼。 |

## Daha fazla okumak

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) MAST taksonomisi; hafıza zehirlenmesi bir koordinasyon-kuşkusu alt ailenidir
  Çinçe Çevirimi:Cemri 等人  Neden çok ajan LLM 系统会失败? MAST 分类法;内存污染是协调失败子家族
- [CA-MCP — Context-Aware Multi-Server MCP](https://arxiv.org/abs/2601.11595) Koordinasyonlu MCP sunucular için Ortak Kontekst Depolama
  Çinçe Çevirimi:CA-MCP  上下文感知多服务器 MCP  协调 MCP 服务器的共享上下文存储
- [Matrix — decentralized multi-agent framework](https://arxiv.org/abs/2511.21686) Merkezli bir orkestratör olmadan mesaj kuyruk tabanlı bir tahta
  Çinçe Çevirimi:Matrix  去中心化多 代理 框架  基于消息队列的黑板,无中央编排器
- [LangGraph state and reducers](https://docs.langchain.com/oss/python/langgraph/workflows-agents) üretimdeki ajan başına projeksiyon modeli
  Çeviri:Düzgün grafik  durumu ve dönüşüm  生产中的每个代理 投影模式
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) Bir üretim dağıtımından gelen kaynak ve doğrulama notları
  Çinçe Çevirimi:Antropik  Nasıl Bir Çok Ajan Oluştururuyoruz Araştırma Sistemleri 
