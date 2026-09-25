# Paralel / Swarm / Networked Architectures

> Gözetmen ile karşılaştırıldığında, merkezi karar verme yetkisi yoktur. Ajanlar ortak etkinlik otobüsünü okuyor, işleri asinkron olarak alıyor, sonuçları yazıyor. LangGraph, merkezi olmayan, dinamik ortamlar için açıkça "Swarm Architecture" i destekler. Matrix (arXiv:2511.21686) hem kontrol hem de veri akışını, orkestratör botluğunun ortadan kaldırılması için dağıtılmış kuyruklar üzerinden geçen serileşmiş mesajlar olarak temsil eder. Bu anlaşma açıkça belirlenmiştir: ölçeklendirme için belirleme ve izlenebilirlik. Swarm birçok bağımsız alt sorunlu görevlere uyum sağlar; tek tutarlı bir plana ihtiyaç duyan görevlere uyum sağlamır.

> **【中文解读】**Bu bölüm, ortak bir durum ve çalışma biçimleri ile birlikte çalışan gruplar ağının  büyük bir miktarı ile ilgili olarak ele alınıyor.

> **【拓展：parallel swarm networks→具体应用】**Ve delil gruplar ağı büyük miktarda Agent aynı zamanda işleme görevi, sonra de birleştirme sonuçları.


**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 16 · 05 (Supervisor Pattern), Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 05 (Supervisor Pattern), Phase 16 · 04 (Primitive Model)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Öğrenci Bölüm 1 Başlangıç: 16·04-05
>  **【类比】**Swarm vs. Supervisor = "decentralize" vs. "层级制"──Supervisor = 公司(CEO调度);Swarm = 开源社区(每人看问题 板自己领取)──Swarm 适合独立子任务(多文件编辑、多源查询),不适合需要单一计划的任务──5-10 个代理是最优太多会聚聚时打架──

## Sorunlar sorunun giriş

Gözetmen birkaç işçiye kadar ölçeyor. Yüzlerce ne olacak? Gözetmenin kendisi şişlik boğaz haline geliyor: kim ne yapması hakkında her karar bir ajan aracılığıyla yürütülüyor.

> 監察員 birkaç iş makinesine yayılabilir. 監察員 kendisi bir şişe haline gelir.

Gözetmen kendiliğinden bir LLM çağrısıdır. Yüzlerce işçi üzerinde, gözetmen sadece göndermek için yüzlerce LLM çağrısı yapar. Her çağrı saniyedir; gönderme üstü maliyet baskın. Swarm gözetmeni tamamen kaldırır.

> 监督者本身就是 LLM 调用──在数百个工作器时,监督者只调度就就进行数百次 LLM 调用──每次调用几秒钟;调度开销占主导──群体完全移除监督者──

Swarm mimarileri tasarımı tersine çevirir. Merkez planlayıcı çalışmayı göndermek yerine, işçiler ortak bir kuyruktan çalışmayı seçerler. "Koordinasyon" etkinlik otobüsü semantikasına eklenir. Orkestratör yok; kuyruk yapana kadar sistem ölçeklenir.

> 群体架构翻转了设计――不是中央规划者分发工作,而是工作器从共享队列中获取工作――"协调"嵌入事件总线语义中――没有编排器;系统扩展直到队列成为瓶──

Mimarlık tersleme önemli: şişe boğazı "ne yapılması gerektiğini belirleyen LLM'den" "yolların çalıştığı mesaj aracı"na taşınır. LLM'ler yavaş ve pahalıdır; mesaj aracı hızlı ve ucuz. Swarm ticaretleri LLM şişe boğazı broker şişe boğazı  neredeyse her zaman bir kazanç.

> Bu nedenle, bu süreçte, bir süre önce, bir süre önce, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre, bir süre sonra, bir süre, bir süre sonra, bir süre, bir süre, bir süre bir süre, bir süre bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir sürece, bir sürece, bir sürece, bir sürece, bir sürece, bir sürecececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece

## Konsept merkezi konsept

### Şekil

```
                ┌──── shared queue ────┐
                │                      │
       ┌────────┼────────┐  ◄──────┬───┘
       ▼        ▼        ▼         │
     Worker  Worker  Worker   Worker
      A       B       C        D
       │        │        │         │
       └────────┴────────┴─────────┘
                 │
                 ▼
            results pool
```

Her işçi tekrar eder: bir görevi çek, işlem yap, sonuç yaz (ve seçeneği olarak takip takipleri).

> 没有编排器.每个工作器重复:拉取任务、处理、写入结果.

Merkezli bir karar vericinin olmaması belirleyici bir özelliğidir. İşçiler talimat beklemiyorlar; sırada kendilerini organize ederler. LLM'lere uygulanan aktör modeli budur.

> 缺乏中央决策者是定义特征──工作器不等待指令;它们围绕着队列自组织──这是应用于 LLM'in aktörleri 模型每个工作器是响应消息的独立演员──

### Bir sürü uyum sağladığında

- **Many independent tasks.**Çekim, dönüşüm, sınıflandırma.
  Çeviri:**许多独立任务。**抓取、转换、分类── görevler arasında birbirine bağlı değildir.
- **Variable-duration work.**Bazı görevler 100 ms alıyorsa diğerleri 10s alıyorsa, bir sürüm yükleri otomatik olarak dengeleyecektir  hızlı işçiler sonraki görevleri çekmek.
  Çeviri:**可变持续时间的工作。**Bazı görevler 100 ms ve diğerleri 10 ms gerektiriyorsa, grup otomatik olarak yük dengesini yapar.
- **Throughput over determinism.**Tamamen tamamlanma süresiyle ilgileniyorsun, sıkı siparişlerle değil.
  Çeviri:**吞吐量优先于确定性。**Çekilmez bir sırada değil, zamanla.

### # Bir sürü düştüğünde #

- **Ordered workflows.**Eğer 3 adım 2'nin çıkışına ihtiyaç duyarsa, bir soğan 2 adım tamamlanmadan önce 3 adım ateşleme riski taşır.
  Çeviri:**有序工作流。**Eğer adım 3'in 2'nin çıkışı gerekiyorsa, grupların 3'ün 2'nin tamamlanmasından önce başlama riski vardır.
- **Global-plan tasks.**Karmaşık araştırma soruları planlamacıdan yararlanır.
  Çeviri:**全局计划任务。**复杂 araştırma sorunları, düzenleyicilerden yararlanmaktadır.
- **Debugging.**Merkez kayıtları ve asinkron çalışmalar olmadığından, bir böceği yeniden üretmek pahalıdır.
  Çeviri:**调试。**没有中央日志和异步工作,复现 bug 代价很高──

### Matrix (arXiv:2511.21686)

Matrix, 2025'te yayımlanan bir makaledir ve bu sayede hem kontrol akışı hem de veri akışı, dağıtılmış kuyruklarda serilize edilmiş mesajlardır. Merkez koordinatörü yoktur. Hata toleransı mesaj dayanıklılığından kaynaklanır. Skalabillik mesaj aracı'nın sorunu, sistemin değil.

> Matrix, 2025 yılında grupların doğal sonuçlara doğru ilerlemesi için hazırlanan bir makaledir: kontrol akımı ve veri akımı, dağılımı bir dizi üzerinde sıralanmış haberlerdir.

Makler (Kafka, Redis Streams, NATS) ölçekleme boğazı yaparak, Matrix LLM-örkestrator boğazını tamamen önleyebilir.

> 通過使代理(Kafka、Redis Streams、NATS) 成为扩展瓶,Matrix 完全避开LLM 作为编排器的瓶──如果代理可以,系统可以扩展到数千代理;LLM 纯工作器,永远不是协调器──

Katkı: çoklu ajan koordinasyonunun "bu ajan hangi mesaj konuyu abone ediyor?" yerine "önetici hangi ajanı seçer?" şeklinde bir programlama modeli. Bu, sistemin bir pub/altı etkinlik ağına benziyor.

> 贡献: bir programlama modeli, çok ajan 协调 is "Bu ajan 订阅什么消息主题?" yerine "監督者下一个选择哪个代理?" sistemini bir yayın/订阅事件网格 gibi görünebilir.

### LangGraph'in Swarm Arsitekturası
### Grafik çerçevelerinde bir sürü

LangGraph 2025 belgelerinde "Swarm Architecture" açıkça çoklu ajan modellerinden biri olarak tanımlanır: ajanlar düğümlerdir, ancak kenarlar döngülerle yönlendirilmiş bir grafik oluşturur ve herhangi bir düğüm havuzdan etkinleştirilebilir.

> LangGraph 2025 文档明确将"群体架构"多代理模式之一" olarak tanımlanır:Agent is a node, but on the side formed of a ring with a directional diagram, any node can be activated from the pool.

LangGraph'in katkı: aynı grafik tabanlı zihinsel model şimdi sürüm dinamiklerini destekler. sabit kenarlara değil koşullara göre aktive olan düğümler. Bu, statik-graf ve saf sürüm dünyasını köprüler.

> LangGraph'in katkıları: Aynı grafik tabanlı akıl modelinin şimdi grup hareketlerini desteklediği için, koşullara dayalı değil, sabit kenar aktivasyon noktaları oluşturduğu için, bu durum grafikini ve saf grup dünyasını köprülediği için,

### Başarısızlık modusu: açlık ve sıcak noktalama

Eğer tüm işçiler en hızlı görevi yaparlarsa, uzun süreli görevler tek kalana kadar asla seçilmez.

> Eğer tüm çalışma makineleri en hızlı kullanılabilir görevleri alırsa, uzun süreli çalışmalar, tek kalan görevler haline gelene kadar asla seçilmez.

Açlık, bir sürünün imza başarısızlık modudur. Açıkça yaşlanmadan (priorite bekleme süresi ile artıyor) veya uzman uzun görevli işçiler olmadan, 10 saniyelik bir görev 100 ms görevlerin akışının arkasında sonsuza dek bekler.

> 饥饿, grupların belirgin bir başarısızlık modudur.  Açıkça yaşlanmamıştır.  Uyarılama süresi arttırılır.  Uyarılama süresi artırılır.

Yumuşak başlılık:
- Açıkça yaşlanarak öncelikli kuyruklar (bekleme süresi ile önceliği artırın).
  Çinçe Çevirisi:带显式老化优先队列 (seçilecek zamanla öncelikli sınıfı artış)
- İşçi uzmanlığı: Bazı işçiler sadece "uzun" görevler alır.
  Çinçe Çevirimiçi:工作器专业化: bazı工作器 sadece "长" görevlerini kabul eder.
- Geri basınç: sıraya kaç hızlı görev girdiyse sınırlayın.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

### İçeriğe dayalı yönlendirme bağlantısı

İçerik tabanlı yönlendirme ile doğal olarak bir dizi çift oluşturun (Dene 22. Genel bir kuyruk yerine, mesaj tipi başına bir kuyruk vardır. Uzman işçiler yalnızca tiplerine abone olurlar. Bu, binlerce ajanın ölçekine kadar uzanan mesaj otobüs mimarlarının temelini oluşturur.

> 群体与内容基的路由 (Desin 22) Doğal ilişki, genel bir sıra değil, her bir haber türünün bir sıra olmasıdır.

İçerik tabanlı yönlendirme artı sürüm size pub/alt etkinlik ağını verir: herhangi bir ajansın herhangi bir mesaj türünü yayınlayabileceği ve yalnızca ilgilenen ajansların alabileceği bir altyapı. Bu Matrix, CA-MCP ve 2026 üretiminin çoğu çok ajans sisteminin temelidir.

> İçeriği dayalı yollar ve gruplar size yayın / abonelik olayları net: herhangi bir ajan herhangi bir haber türünü yayınlayabilir ve sadece ilgi gösteren ajanı alabilir. Bu Matrix, CA-MCP ve çoğu 2026 yılının üretimi çoklu ajan sisteminin temelidir.

## Yapın.
```figure
sw-work-stealing
```

## Yapın

`code/main.py`paylaşılan bir ipten çekilen 4 işçi iplik bir sürüsü uyguluyor `queue.Queue`Görevlerin değişken süresi vardır (bazı hızlı, bazıları yavaş).

> `code/main.py`4 tane paylaşım gerçekleştirdim.`queue.Queue`拉取工作线程──任务有可变持续时间(一些快,一些慢)──演示对比:

Üç yönlü bir karşılaştırma eğitim değeridir: aynı görevler, aynı işçiler, sadece gönderme stratejisi değişir. Sequential = slow. Fixed = wasteful. Swarm = optimal. Duvar saatleri rakamları bu durumu empirize yapar.

> Üç taraf karşılaştırma eğitim değeri: aynı görev, aynı çalışma makinesi, sadece düzen stratejisi değişimi, sırası = 慢, sabit = 浪费, grup = 最优, saat saatı dijital deneyimli olarak kanıtlanmış durum,

- **Sequential baseline:**Bir işçi tüm görevleri seri olarak işliyor.
  Çeviri:**顺序基线：**Bir iş makinesi tüm görevleri işliyor.
- **Fixed assignment:**belirli bir işçiye önceden atanan her görev (nözetçi tarzında).
  Çeviri:**固定分配：**Her görev önceden belirli bir çalışma makinesine dağıtılır.
- **Swarm:**İşçiler ortak bir kuyruktan çekiliyorlar.
  Çeviri:**群体：**工作器 from共享队列拉取──

Swarm balances otomatik olarak yüklenir; sabit görevler verilen görev yavaş olduğunda hızlı çalışanları hareketsiz bırakır.

> 群体自动平衡负载;固定分配在分配任务慢时让快速工作器空──

"Eşitsiz ama en iyi" dağılım, bir sürüm imzasıdır. 50 ms içinde görevini bitirmiş bir işçi, 2 saniyelik bir görevde çalışan bir işçi hala ilkindeyken üç tane daha çekir.

> "Bekleyici değil ama en iyi" dağılım grup özellikleri  50 ms  görev tamamlama iş makinesi 2 saniyelik görev iş makinesi hala ilk görev üzerinde üç daha fazla görev alır   Genel saat saat süresi en yavaş tek görev sınırlaması, toplam değil 

Çıktılık, çalışan başına görev sayısını (sürük eşitsiz ama optimal bir şekilde dağıtılır) ve duvar saatini gösterir.

> 输出显示每个工作器的任务计数(群体分布不均但优优) 和挂钟时间──

## Çerçeveyi kullanın.

`outputs/skill-swarm-fit.md`Bir görevden swarm vs. supervisor kullanılması gerektiğini değerlendirir. Girişler: görev bağımsızlığı, süresi varyansi, sipariş gereksinimleri, hata çözülebilirliği gereksinimleri.

> `outputs/skill-swarm-fit.md`评估任务应使用群体还是监督者――输入: görev bağımsızlığı、持续时间差、排序要求、可调调试性需求――

## İndirin . Ürünler .

Kontrol listesini:

> 检查清单:

- **Priority queue with aging.**Uzun görevli açlıktan kaçınmak.
  Çeviri:**带老化的优先队列。**防止长任务 açlık.
- **Worker idempotency.**Bir işçi çalışmanın ortasında kaza yaparsa bir görev birden fazla kez atılabilir.
  Çeviri:**工作器幂等性。**Eğer iş makinesi çökerse, görevler çok fazla sürede çekilebilir.
- **Durable queue.**Yapım için Kafka, Redis Akışları veya veritabanı destekleyen bir kuyruk kullanın. `queue.Queue`Sadece hafıza.
  Çeviri:**持久队列。**生产环境使用 Kafka、Redis Streams 或数据库支持的队列──`queue.Queue`Sadece kayıtta.
- **Observability per task.**Her görevde bir iz kimliği vardır; her işçi bu işten başlayıp biter.
  Çeviri:**每个任务的可观测性。**Her görevde takip kimliği vardır; her iş cihazı başlıyor/biter.
- **Back-pressure.**Eğer sıra işçilerin boşaltmasından daha hızlı büyürse, üreticinin yavaşlamasını sağlayın.
  Çeviri:**背压。**Eğer sıraların büyümesi hızla iş makinesi boşluk hızına göre yavaşlarsa üreticileri azaltır.

## Egzersizler.

1. Çık .`code/main.py`Değişken süresi iş yükü üzerinde süren sürenden ne kadar hızlı?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ Gruplar değişen süren çalışma yükü üzerinde nasıl bir sırayla?
2. Öncelik kuyruk variansı ekle (kullanım `queue.PriorityQueue`) Görev "Önem" alanına öncelik belirleyin.
   Çine dili: 添加优先队列变体(使用 `queue.PriorityQueue`)。 "Önemli" görev bölümüne göre öncelik dağıtımı─── düşük öncelikli görevlerin sürekli yük altında açlık olup olmadığını gözlemlemek──────────
3. Bir işçi en yavaş işçiye göre 3 kat daha fazla görev işlediğinde sıcak nokta algılayıcısını uygula: bu, görev süresi dağılımıyla ilgili neyi gösterir?
   Çinçe çevirisi: ısı noktası denetleyicisini gerçekleştirmek: herhangi bir iş makinesi en yavaş iş makinesi ile 3 kat daha fazla işlemi işlediğinde kayıt yaparken.
4. Matrix makalesini okuyun (arXiv:2511.21686) soyut ve Bölüm 3. Matrix'in kabul ettiği (skalabilme kazancı) ve bıraktığı (içime geçiş, belirleme) belirli bir ödemeyi tanımlayın.
   Çinli dilde: matrix 论文 (arXiv:2511.21686) özet ve 3. bölüm.
5. Swarm demo'sunu bir `queue.Queue`Görevler heterogen olduğunda hangi yönlendirme kuralları mantıklıdır?
   Çine dilinde:将群体演示转换为使用 (task_type, payload) 元组的`queue.Queue`, çalışma makinesi sadece belirli bir türden abone edilmektedir.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Swarm architecture / 群体架构 | "Decentralized agents" / "去中心化 Agent" | Workers pull from shared queue; no central orchestrator. / 工作器从共享队列拉取；没有中央编排器。 |
| Event bus / 事件总线 | "Agents subscribe to topics" / "Agent 订阅主题" | Message broker that routes tasks to workers by type or content. / 按类型或内容将任务路由到工作器的消息代理。 |
| Starvation / 饥饿 | "Task never runs" / "任务永远不运行" | Low-priority task never gets picked because higher-priority work arrives continuously. / 低优先级任务因为高优先级工作持续到达而永远不被选中。 |
| Hot-spotting / 热点 | "One worker drowns" / "一个工作器淹没" | Load imbalance where one worker gets most tasks. / 一个工作器获得大部分任务的负载不均衡。 |
| Back-pressure / 背压 | "Slow down the producer" / "减慢生产者" | Mechanism that signals upstream to stop producing when the queue fills up. / 当队列填满时向上游发出停止生产的信号机制。 |
| Idempotent worker / 幂等工作器 | "Safe to re-run" / "安全重新运行" | A task processed twice produces the same result. Required because workers may crash mid-run. / 任务处理两次产生相同结果。因为工作器可能中途崩溃所以需要。 |
| Durable queue / 持久队列 | "Survives crashes" / "崩溃后存活" | Queue backed by disk or replicated storage; tasks are not lost when a worker crashes. / 由磁盘或复制存储支持的队列；工作器崩溃时任务不丢失。 |
| Matrix framework / Matrix 框架 | "Full message-passing swarm" / "全消息传递群体" | Both data and control flow are serialized messages on distributed queues. / 数据流和控制流都是分布式队列上的序列化消息。 |

## Daha fazla okumak

- [LangGraph workflows and agents — Swarm Architecture](https://docs.langchain.com/oss/python/langgraph/workflows-agents) açık bir sürüm desteği
  Çinçe Çevirim:LangGraph 工作流和 Agent  群体架构  明确的群体支持
- [Matrix — A Decentralized Framework for Multi-Agent Systems](https://arxiv.org/abs/2511.21686) Tam mesaj geçiren bir sürüm
  Çinçe Çevirimi:Matrix  多 Agent 系统的去中心化框架  全消息传递群体
- [Anthropic engineering — why supervisor not swarm in Research](https://www.anthropic.com/engineering/multi-agent-research-system) belirli bir üretim sistemi neden açıkça sürüden önce denetçiyi seçti
  Çinçe çevirisi:Antropik 工程  Neden araştırma sistemi gözlemciyi seçerken grup değil  Neden belirli bir üretim sistemi belirgin bir şekilde gözlemciyi seçerken grup değil
- [AutoGen v0.4 actor-model docs](https://microsoft.github.io/autogen/stable/) olay yönlendirici aktör yeniden yazmak, v0.2'nin GroupChat'ten daha yakındır
  中文翻译:AutoGen v0.4 aktör 模型文档  事件驱动 actor 重写,比 v0.2 的 GroupChat 更接近群体
