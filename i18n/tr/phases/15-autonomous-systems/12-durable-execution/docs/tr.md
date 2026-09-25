# Uzun süreli arka planlı ajanlar: Sürdürülebilir idam

> Üretim uzun uzayda bulunan ajanlar çalışmıyor `while True`. Her LLM çağrısı kontrol noktası, tekrar deneme ve tekrarlama ile bir aktivite haline gelir. Temporal'ın OpenAI Ajanlar SDK entegrasyonu Mart 2026'da GA'ya geçti. Claude Code Routines (Anthropic) sürekli yerel bir süreç olmadan programlı Claude Code hesaba çekmelerini yürütür. Sessiyonlar insan girişleri üzerinde durur, kurtulma dağıtımları sürdürür ve en son kontrol noktasından devam eder.`thread_id`Yeni ergonomiğin arkasında eski bir model yer alır  iş akışının orkestrasyonu  yeni bir giriş ile: LLM, iyileşme sırasında belirsizce tekrarlanması gereken belirsiz faaliyetler olarak çağrılar.

> **【中文解读】**Üretim süreci Ajan yok`while True`Ortalama çalışmaları, her LLM 调用成为带检查点、重试和重放活动──Temporal'ın OpenAI Agents SDK 集成于 2026年 3月 GA。Claude Code Routines(Anthropic) in an undurable local process context run run调度 Claude Code 调用──会话在人类输入时暂停、跨部署存活、最新检查点恢复──新工效学背后是旧模式工作流编排和一个新输入:LLM 调用作为恢复时必须在确定性重放的非确定性活动──

> **【拓展：LLM 调用 = 活动的精确契合】**LLM 调用完美匹配活动特征:不确定性(温度 > 0) 昂贵(金钱和延迟) 、可能失败(速率限制、超时) 、有副作用(调用工具)  把每个 LLM 调用包装为活动即可获得指数退避重试、跨重启检查点和可重放调试追踪──这就是为什么 Temporal、长度图片、云flare Durable Objects、Claude Code Routines 全部收到相同 API 形态`thread_id`+ 后端存储 + 最近检查点恢复──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, minimal durable-execution state machine) | **语言:** Python（标准库，最小持久执行状态机）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 01（长程 Agent）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前 Lütfen önce bil:Fase 15·10(hakki modüsü) Fase 15·01(长程 Ajan)  dağıtılmış sistemli temel 检查点、重试、等)  Sürdürülebilir yürütme = Ajanı 当工作流编排──
>  **【类比】**Sürdürülebilir Çalışma = "Agent'in arşivi noktası"──普通 Agent = 玩游戏没存档(崩=重头);Durable = 每个 LLM 调用后自动存档(崩=读最近的存档)──关键技巧:把每一个 LLM 调用包装为"活动",记录输入输出到日志,崩时重放日志而不是重新调用既省钱又避免副作用重复执行(如重复转账)──
> ️ **【易错点】**副作用工具(写数据库、调外部 API) 不存缺陷键 → 恢复时重复执行可能造成业务错误(用户被扣两次款) ――修复:每个副作用调用必须带等键(如`idempotency-key: uuid`- Ne demek istiyorsun?

## Sorunlar. Sorunlar.

> **【中文解读】**持久执行确保 Agent 任务在故障后能恢复──传统 Agent 在内存中运行,进程崩的意思是从头开始──持久执行将状态保存到外部存储(数据库、文件系统), herhangi bir anda en yakın kontrol noktasından geri kazanılabilir──Temporal 和 LangGraph, sürekli gerçekleştirilen iki ana çerçevelidir──

> **【拓展：durable execution】**持久执行对长时间运行的代理至关重要──如果一个需要运行 2 小时的代理在第90 分钟崩,没有持久执行就意味着重新开始── 暂时 通过事件追溯源实现持久工作流,长图图图 通过检查点实现持久状态图── 2026 yılının en iyi uygulaması her önemli adımdan sonra otomatik olarak kaydedilen kontrol noktasıdır──

Örneğin, dört saat çalışan bir ajanı düşünün. Üç alet çağırır, kullanıcıya iki kez uyarır ve kırk LLM çağrısı yapar.

> 考虑一个运行四小时的代理――它调用三个工具――提示用户两次――进行40次 LLM 调用――中途,运行的主机重启――

Ne oluyor?

> Ne oluyor?

- Saf bir şekilde .`while True`Loop: her şey kayboldu. Çalışma sıfırdan yeniden başlıyor. Üç araç çağrısı (gerçek yan etkileri ile) tekrar yürütülüyor. Kullanıcı zaten onayladığı şeyler için tekrar uyarılıyor.
  Çönsel Türkçe:`while True`循环中:一切丢失──运行从头开始再启──三工具调用(带真实副作用) 再执行──用户再次被提示已批准的事──40 个 LLM 调用再计费──
- Sürdürülebilir yürütme ile: yürütme en son kontrol noktasından devam eder. Daha önce tamamlanmış faaliyetler yeniden yürütülmez; sonuçları sürdürülebilir günlükten tekrar oynanır. Kullanıcı zaten onayladığı şeyleri yeniden onaylamaz. Daha önce yapılan LLM aramaları yeniden fatura edilmez.
  Çinçe Çevirisi:有持久执行时:运行从最近检查点恢复──已完成活动不重新执行;其结果从持久日志重放──用户不重新批准已批准的事──已做 LLM 调用不重新计费──

Bu, çalışma akış motorlarının on yıldır gönderdiği aynı model (Temporal, Cadence, Uber'in Cherami) yeni olan şey, LLM çağrılarının artık bir tür etkinlik olmasıdır  belirsiz, pahalı, yan etkileri  ve bu modelle temiz bir şekilde uyumlu.

> Bu çalışma sürecinin on yıllık süresiyle aynı modelde.

> **【中文解读】**持久化执行解决长程 代理的可靠性问题:四小时运行中主机重启时,朴素循环丢失一切(工具重新执行、用户重新审批、LLM 重新计费), 持久化执行, 持久化执行, 持久日志重放而非重执行, 已完成的活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成活动, 已完成 已完成 已完成 已完成 已完成 已完成 已完成 已完成 已完成 已完成 已完成 已完成 已完成 已完成 已完成 已完成 已完成 已完成 完成 已完成 完成 已完成 完成 已完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成 完成  完成                                                                                                               

Dersin devam eden teması: uzun uzayda güvenilirlik düşüşü (METR "35 dakikalık bir bozulmayı" gözlemler  başarının oranı ufukta yaklaşık olarak dörtlü olarak düşer). Dayanıklı yürütme güvenilirlik profili desteklediğinden daha uzun süren çalışmalar sağlar. Bu, tasarım doğruysa güvenli bir şekilde başarısız olma ve tasarım yanlışsa güvensiz bir şekilde başarısız olma yeni bir yoludur.

> Bu dersin çalışma konusu: Uzun süre güvenilirlik düşüşü(METR  gözlemlenir "35 dakika düşüşü" başarısı oranı ve zaman çizgisi büyüklükte kare karşı karşı karşı karşı düşüşü) ◊ Sürekli yürütülme etkinleştirmek güvenilirlik arşiv desteklenmiş daha uzun süreli çalışmalar, bu tasarlama doğru zaman güven başarısızlık, tasarlama yanlış zaman güven başarısızlık yeni bir yöntemdir.

## Konsepten bir şey.

### Aktiviteleri, iş akışları ve tekrar oynama

- **Workflow**Bu, etkinlik logundan şaşırtıcı bir farklılık olmadan tekrar oynanabilmesi için belirleyici olmalıdır.
  Çeviri:**工作流**Bu, bir olay günlüğünü yeniden oluşturmak ve bekleme konusunda belirlenmiş bir ayrım yapma biçimidir.
- **Activity**Bu uygulama, bir çalışma birimi olarak kullanılır. LLM çağrısı, araç çağrısı, dosya yazısı, HTTP talebi. Her etkinlik girişleri ve (bir kez tamamlandığında) çıkışlarıyla kaydedilmiştir.
  Çeviri:**活动**: अनिश्चित性、可能失败的工作单元──LLM 调用、工具调用、文件写、HTTP 請求── her etkinlik onun girişini ve 完成时)输出──
- **Event log**: dayanıklı destek mağazası. Her etkinlik başlatılır, tamamlanır, başarısız olur, tekrar dener ve her iş akışı karar kaydedilir.
  Çeviri:**事件日志**:持久后端存储── her faaliyet başlıyor、 tamamlıyor、 başarısız oluyor、 tekrar denediyor ve her çalışma akışı kararları kaydedilmiştir──
- **Replay**: kurtarma sırasında, iş akışı kodu başlangıçtan itibaren tekrar çalıştırılır; zaten tamamlanan her etkinlik yeniden çalıştırılmadan kaydedilen sonuçlarını gönderir. Sadece tamamlanmamış etkinlikler gerçekte çalıştırılır.
  Çeviri:**重放**: Restore,工作流代码 baştan tekrar çalış; her tamamlanmış etkinlik yeniden gerçekleştirilmeden kaydedilen sonuçlara geri döner.

Bu, React'ın sanal DOM'e karşı yeniden göstermesi veya Git'in commit'lerden bir iş ağacını yeniden inşa etmesiyle aynı şekildir.

> Bu, React ile  Virtual DOM yeniden yapımı veya Git ile ilgili olarak gönderilen yeniden yapım çalışma ağacının şekli ile aynıdır.

### Neden LLM çağrıları bu şekilde uygulanıyor ?

LLM çağrıları:

> LLM 调用是:

- Deterministik olmayan (temperatür > 0; hatta 0 sıcaklık model sürümleri arasında hareket eder).
  中文翻译:非确定性(temperatür > 0; hatta sıcaklık 0 跨模型版本漂移) 』
- Pahalı (para ve gecikme).
  Çinçe Çevirimi:昂贵(金钱和延迟)
- Potansiyel başarısızlık (sır limitleri, zaman kesintileri).
  Çeviri:                                                                                                                                                                                                                                                             
- Yan etkileri (gerçeleri kullanırlarsa).
  Çinçe Çevirimiçi: yan etkileri varsa

Bu tam olarak etkinlik profili. LLM'nin her çağrısını bir etkinlik olarak kapatmak, eksponensel geri dönüş, yeniden başlatma üzerinden kontrol noktası ve debugging için tekrarlanabilir bir iz sağlar.

> Bu etkinlik arşividir. Her LLM'nin etkinlik için paketleme ayarlaması, tekrar başlatma kontrol noktası ve tekrar başlatılabilir düzenleme takip edilmesi.

### Kontrol noktaları `thread_id`# # Ve #`thread_id`Çeviri noktaları

LangGraph, Microsoft Agent Framework, Cloudflare Durable Objects ve Claude Code Routines hepsi aynı API şeklinde birleşmiştir: a `thread_id`(veya eşdeğer) oturum tanımlanır; her durum geçimi bir arka uçta kalır (PostgreSQL varsayılan, dev için SQLite, önbelleğe Redis); devam, en son kontrol noktasını okuyor.

> LangGraph、Microsoft Agent Framework、Cloudflare Durun Nesneler 和 Claude Code Routines hepsi aynı API biçimini aldı:`thread_id`(or similar price)识别会话;每个状态转换持久化到后端(默认 PostgreSQL、dev 用SQLite、缓存用Redis);恢复读最新检查点──

Arka taraf seçimi önemlidir:

> 后端选择重要:

- **PostgreSQL**LangGraph için öntanımlı.
  Çeviri:**PostgreSQL**Bu yüzden, bu durumun bir parçası olarak, bir diğerinden daha fazla bilgi almak için,
- **SQLite**: sadece yerel dev; sunucular arasında verileri kaybeder.
  Çeviri:**SQLite**: sadece kendi gelişimi;
- **Redis**: hızlı ama geçici, AOF/snapshot yapılandırılmadıkça.
  Çeviri:**Redis**Şimdiki durum:
- **Cloudflare Durable Objects**: şeffaf bir şekilde dağıtılmış; eşsiz bir anahtarla kapsamlı; saatler veya haftalar boyunca hayatta kalır.
  Çeviri:**Cloudflare Durable Objects**: transparent distributed;以唯一键为范围;存活数小时到数周──

### İnsan girişleri birinci sınıf bir devlet olarak.

Teklif-sonra-yürüme (Deneyim 15) dayanıklı bir "insan bekleme" durumunu gerektirir. İş akışı duraklar, dış kuyruk bekleyen talebi tutar ve onay tam olarak o noktadan devam eder. Süreklilik olmadan bu en iyi çaba; onunla, bir gece onay gelir ve iş akışı sabah başlar.

> Önerilen-sonra-devle­den (第 15 课) ihtiyaç duyulan "büyük insan" durumunun devam etmesi gerekir.

### 35 dakikalık çöküş 35 dakikalık düşüş.

METR, ölçülen her ajan sınıfının, sürekli çalışmanın ~35 dakikasından fazla güvenilirlik kaybını gösterdiğini gözlemledi.

> METR  Her ölçümün ajan sınıfı 35 dakika süren bir sürenimden sonra güvenilirliğinin azalmasını gösterdi.

Görev süresini ikiye katlamak başarısızlık oranını yaklaşık dört katına çıkarır. Dayanıklı yürütme bunu düzeltmez; güvenilirlik profili desteklediğinden daha uzun süre çalışmanıza izin verir. Güvenli bir örnektir. Dayanıklılığı, tekrar giriş sırasında taze HITL gerektiren kontrol noktaları ve bütçe öldürme anahtarları (Leçon 13) ile birleştirmek.

> 任务时长大致使失败率四倍──持久执行不修复此; it lets you run better than reliable archives supported by 更多久──安全模式 is going to be a continuity with re-entry time needing new HITL'in checkpoint link, with non-wall time封顶总计算的预算终止开关(第 13 课) link.

### Sürekli işlenme yanlış cevap olduğunda, süren işlenme cevap değildir.

- İnsan girişsiz birkaç dakikadan kısa sürer.
  Çinçe Çevirisi:短于几分钟无人输入的运行──开销 > 收益──
- Sadece okunur bilgi alımı.
  Çevre dilinde: 严格只读信息检索
- Doğru olması için tek bir bağlam penceresinde son-son işlemleri gerektiren görevler (bazı akıl yürütme görevleri; bazı tek çekim nesilleri).
  Çinçe Çevirimiçi:正确性需要在一个上下文窗口内端到端的任务(某些推理任务;某些一次性生成)

## Çerçeveyi kullanın.
```figure
memory-consolidation
```

## Kullan

`code/main.py`stdlib Python'da minimal dayanıklı bir yürütme motorunu uyguluyor.

> `code/main.py`Python standart kütüphanesi en az süren bir uygulama motorunu gerçekleştirir.

- `@activity`JSON olay günlüğüne girdiler ve çıkışları kaydeden dekorator.
  Çeviri:`@activity`装饰器将输入输出记录到 JSON 事件日志。
- İş akışı işlevi, etkinlikleri sıralar.
  Çeviri:                                                                                                                                                                                                                                                             
- A.`run_or_replay(workflow, event_log)`Başarılı etkinlikleri yeniden gerçekleştirmeden tekrarlayan bir işlev.
  Çeviri:`run_or_replay(workflow, event_log)`函数重放已完成活动而不重新执行──

Sürücü üç etkinlik iş akışını simüle eder, yarıda çökür ve (a) tümü yeniden gerçekleştirmek için bir naif tekrar deneme gösterir.

> 驱动器模拟三活动工作流,中途崩,展示 (a) 朴素重试重新执行一切 vs (b) 重放只运行缺失活动──

## İndirin . Ürünler .

`outputs/skill-durable-execution-review.md`uzun süreli ajanların kullanılması için önerilen bir düzenlemeyi doğru süren uygulama biçimi için değerlendirir: faaliyetler, belirleme, kontrol noktalarının arka planı, insan giriş durumu ve HITL-on-resume politikası.

> `outputs/skill-durable-execution-review.md`审查提议的长时运行 署的正确持久执行形状: faaliyet, belirlenme, kontrol noktalarının arkasındaki sonu, insan giriş durumu ve kurtarma zamanı HITL stratejisi

## Egzersizler.

1. Çık .`code/main.py`.Sırırırma noktasını değiştirin ve tekrar sayısının değişmesini gösterin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ gözlem basit ağırlık deneme ve ağırlık sallama faaliyetleri yürütme oranı farkı¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

2. Oyuncak motorunu kullanmak için dönüştür .`thread_id`Motor paylaştığı iki eşzamanlı seansı simüle edin ve olay kayıtlarının çarpışmadığını doğrulayın.
   Çin Çeviri:将玩具引擎转为显式使用`thread_id`❖ 模拟共享引擎的两个并发会话并确认其事件日志不冲突──

3. Oyuncak motorunda bir etkinlik alın. Bir belirsizlik (iş akışının bir kararında bir duvar saat zaman damgası) getirin. Tekrar oynatmada farklılığı gösterin. Gerçek motorların bunu nasıl hallediğini açıklayın ( yan etkisi kaydesi, `Workflow.now()`API'ler).
   Çinçe Çevirimi Çevirisi: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Çeviri Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Çev`Workflow.now()`API) 

4. LangChain'in "Prodüksiyon derinlikleri ajanlarının arkasındaki çalıştırma zamanı" yazısını okuyun.
   Çin Çeviri: LangChain'ın "Prodüksiyon derin ajanlarının arkasındaki çalışma zamanı"

5. 6 saatlik özerk kodlama görevi için kontrol noktası politikası tasarlayın.
   Çinçe Çevirim: 6 saatlik kendi kendine kodlama görev tasarımı kontrol noktası stratejisi.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Workflow | "Agent's script" | Deterministic orchestration code; replayable from event log |
| 工作流 | "Agent 的脚本" | 确定性编排代码；可从事件日志重放 |
| Activity | "A step" | Non-deterministic unit (LLM call, tool call); logged before and after |
| 活动 | "一步" | 非确定性单元（LLM 调用、工具调用）；前后记录 |
| Event log | "The backing store" | Durable record of every state transition |
| 事件日志 | "后端存储" | 每个状态转换的持久记录 |
| Replay | "Resume" | Re-run workflow; completed activities return logged results without re-execution |
| 重放 | "恢复" | 重跑工作流；已完成活动返回记录结果而不重新执行 |
| Checkpoint | "Save point" | Persisted state keyed by thread_id; latest-wins on resume |
| 检查点 | "保存点" | 以 thread_id 为键的持久状态；恢复时最新优先 |
| thread_id | "Session key" | Identifier that scopes durable state |
| thread_id | "会话键" | 范围化持久状态的标识符 |
| 35-minute degradation | "Reliability decay" | METR: success rate drops ~quadratically with horizon |
| 35 分钟衰减 | "可靠性衰减" | METR：成功率与时间线大致平方反比下降 |
| Non-determinism | "Drift on replay" | Wall clock, random, LLM output; must be registered as side effect |
| 非确定性 | "重放漂移" | 墙钟、随机、LLM 输出；必须注册为副作用 |

## Daha fazla okumak

- [Anthropic — Claude Code Agent SDK: agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) bütçe, dönüm ve semantik devam.
  Çinçe Çevirisi: बजेट、轮次和恢复语义。
- [Microsoft — Agent Framework: human-in-the-loop and checkpointing](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) RequestInfoEvent şekli.
  Çeviri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:Tevri:T
- [LangChain — The Runtime Behind Production Deep Agents](https://www.langchain.com/conceptual-guides/runtime-behind-production-deep-agents) Konkret çalışma süresi gereksinimleri.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [OpenAI Agents SDK + Temporal integration (Trigger.dev announcement)](https://trigger.dev) LLM görüşmeleri için etkinlik şekli.
  Çeviri:L.L.M. 调用活动形态──
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) 35 dakikalık çöküş referansı.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çev
