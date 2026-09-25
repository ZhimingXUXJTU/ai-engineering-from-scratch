# Üretim ölçeklendirme  Sırlar, Kontrol Noktalar, Dayanıklılık  Kontrol Noktası Üretim  Genişleme  Koordinat

> Çoklu ajan sistemlerini binlerce eşzamanlı çalışmaya ölçeklendirmek gerektirir **durable execution** iş kuyrukları ve kontrol noktaları, böylece herhangi bir işçi herhangi bir kaza sonrası herhangi bir koşuyu yeniden başlayabilir, eğer kiralama işlemleri, idempotent yan etkileri ve belirlenmiş tekrarlamalar yerinde varsa. LangGraph'in çalışma zamanı referans örneğidir: her süper adımın ardından bir kontrol noktası yazar.`thread_id`(Önlüğe bağlı olarak son derece yüksek; çalışan kazalar kiralık bir anlaşma serbest bırakır ve başka bir işçi yeniden başlar.**MegaAgent**(arXiv:2408.09955) üç durum (İdle / İşleme / Cevap) ve iki katlı koordinasyon (grup içi sohbet + gruplararası admin sohbet) ile bir ajan başına bir üreticiler- tüketici kuyruk yürütmüştür. **Fiber/async**LLM akışı için her iş için iplikten geçiyor: ipler token bekleyen zamanın %99'unda hareketsiz kalıyor, lifler işbirliği içinde I/O'da üretmektedir.**FastAPI + Postgres + nothing else**Bu ders, dayanıklı bir kontrol noktası günlüğü, devlet geçişleri ile bir ajan iş kuyrukunu, async vs. thread demo'yu oluşturur ve pragmatik "sadece başlat" kuralını yerleştirir.

> **【中文解读】**Bu bölüm, çoklu ajan  sisteminin üretim genişletilmesi  sıralar  kontrol noktaları ve genişleme stratejileri hakkında bilgi veriyor.

> **【拓展：production scaling queues checkpoints→具体应用】**Çoğu Ajan  sistemin üretim genişleme ihtiyacı:(1) 消息队列Kafka/RabbitMQ 缓冲 Agent 间的消息;(2) 检查点定期保存系统状态以支持恢复;(3) 负担均衡将任务均分配可用Agent 实例;(4) 水平扩展动态增长减速Agent 数量应对负担变化──长图云和时云是该领域的两个主要选择──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `asyncio`, `sqlite3`) | **语言:** Python（标准库，`asyncio`，`sqlite3`）
**Prerequisites:** Phase 16 · 09 (Parallel Swarm Networks), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 09（并行群体网络），Phase 16 · 13（共享内存）

>  **【前置】**学本节前 請先掌握:Fase 16·09(Swarm) 、Fase 16·13(共享内存) 、Fase 15·12(Durable Execution) 、异步编程(asyncio) 。多 Agent 生产扩展 = 分布式系统工程问题。
>  **【类比】**Çocuğu genişletmek için bir süreliğine daha fazla bilgi almak için, bir süreliğine daha fazla bilgi almak için, lütfen lütfen lütfen yayına bakın.
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar sorunun giriş

Bir prototip çoklu ajan sistemi bir dizüstü bilgisayarta üç ajanla bir hafıza olay döngüsünde çalışır.

> Bir bilgisayar üzerinde üç ajanla bir adet akışın içinde çalışmaktadır.

- Ajanlar bazen saatlerce çalışır (uzun araştırma, insan döngü içinde bekler).
  Çinçe Çevirimi Çevirisi:Agent 有时运行数小时(长时间研究、人环等)
- İşçi işlemleri çöküyor, yeniden başlatma durumunu kaybediyor.
  Çeviri: 工作者进程崩──重启丢失状态──
- En yüksek yük ortalama 10x'dir. Yatay ölçeklendirme gerekir.
  Çinçe Çevirisi: Yüksek yük ortalama 10 kat; seviyede genişleme gerekir.
- Kullanıcılar ajanın başına ödeme yaparlar. Ücret almak için tam bir kez semantik gerek.
  Çin Çeviri: User per Agent 运行付费;你需要恰好一次的计费语义──

Bu olaylar için bir tane daha kullanın. 2026'da kullanılabilecek olan seçenekler:

> İç kayda olay döngüsü bunlar da yapılmaz.

1. Kontrol noktaları olan bir iş akışı motoru (Temporal, LangGraph çalıştırma zamanı).
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Çeviri Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
2. Devlet mağazası ile bir mesaj sırası (Postgres + SQS/RabbitMQ).
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
3. Aktör model çerçeveleri (MegaAgent'in her ajanı için üreticisi- tüketicisi).
   Çeviri:Actor 模型框架 (MegaAgent'ın her bir ajanı 生产者-消费者)
4. Elle fırlatılmış FastAPI + Postgres (Bedi'nin argümanı).
   Çinçe Çevirisi:手工搭建的FastAPI + Postgres(Bedi 的论点)

Bu ders her birinin küçük bir biçimini oluşturur.

> Bu ders her birinin küçük bir versiyonunu oluşturur.

## Konsept merkezi konsept

### Sürekli çalıştırma, örneği

Sürdürülebilir bir çalıştırma motoru, her "adım" (LangGraph'in dilinde süper adım) sonrasında programın tam durumunu sürdürür.

```
worker crashes mid-step
  -> lease timeout
  -> another worker picks up the thread_id
  -> resumes from last checkpoint
  -> no duplicate side effects
```

Bu iş için gerekli şartlar:

- **Serializable state.**Tüm ajan durumları devamlı olmalıdır.
- **Deterministic resume.**Aynı durum ve aynı girişler verildiğinde, ajan aynı eylemleri üretir (veya LLM çağrıları için dış bir belirleyici oracleye geçirir).
- **Idempotent side effects.**Dış çağrılar (örnek çağrıları, ödeme) geçersiz olmalıdır veya bir kopyalanma anahtarı kullanmalıdır.

LangGraph, her süper adımdan sonra bir kontrol noktası yazar; Temporal her etkinliğin ardından yazar; Restate olay kaynaklı dergiler kullanır.

### Bir adım adım kontrol noktası için bir çalışma süresi

LangGraph'in çalıştırma süresi çalışılmış bir örnektir: her ajanın bir `thread_id`Bu durum, her süper adım kontrol noktaları tablosuna bir satır yazar.`interrupt()`İnsan girişini beklerken, çalışma süresi devam eder ve işçiyi serbest bırakır.

Bu, Nisan 2026'daki referans üretim tasarımı.

### MegaAgent'in ajan başına sırası

arXiv:2408.09955 bir ölçek deneyini tanımlar: binlerce eşzamanlı ajan bir küme içinde.

```
agent i:
  state ∈ {Idle, Processing, Response}
  in_queue   <- messages addressed to agent i
  out_queue  -> replies + side effects

coordinators:
  intra-group chat  (agents in the same group)
  inter-group admin chat  (high-level routing)
```

İki katlı koordinasyon, grup içi konuşmanın yoğun şekilde gerçekleşmesine izin verirken gruplar arası konuşma nadir kalır.

### Async vs. iş başına ip

LLM çağrıları I / O bağlıdır. Bir sonraki jetonu bekleyen bir düğüm zamanın %99'unda boştur. Düğümler her biri ~ 1 MB RAM maliyetini; 10.000 eşzamanlı çağrılarda, bu sadece yığınlar için 10 GB.

Fiber (Python `asyncio`, Goruutines, Rust `tokio`) işbirliği içinde I/O'da verimlilik sağlıyor. Aynı 10.000 çağrı işlemde rahatlıkla uyumludur. LLM-agent ölçeğinde async bir optimizasyon değil  mimaridir.

İstisna: CPU'ya bağlı post-işlem (eğlenme, tokenizer hileleri) hala ipler veya işlemler istiyor.

### Bedi'nin karşı noktası

"Skaling Agentic Software" (Ashpreet Bedi, 2026) çoğu ekibin yükü ölçmeden önce aşırı mühendislik yaptığını savunuyor.

- FastAPI + Postgres.
- Her ajan çalışması bir sıra; durum iyi bir eşzamanlılık ile güncelleştirilmiş.
- Arka planlı işler`pg_notify`Ya da basit bir Seleri işçisi.
- Başvuru kodu ile tekrar deneyin.

Yönetilebilir görevlerde ~ 100'den az eşzamanlı ajan çalışması için, genellikle ihtiyacınız olan tek şey bu.

Kural: basit mimarlıklar çözemediği bir problemle karşılaştığınızda dayanıklı bir uygulama çerçevesini benimsemek.

### Tam bir kez semantik

Ödenmiş ajanlar için "eşit bir etkinlik" (en az bir teslimat + idempotent tüketicisi) gerekir.

- **Dedup key per run.**Her yan etki çağrısında dahil edin.
- **Outbox pattern.**Yan etkiler önce bir tabloya yazılır sonra ayrı bir süreç onları gerçekleştirir.
- **Compensating transactions.**Yan etkisi başarılı olduğunda, ancak takip yazısı başarısız olduğunda, bir tazminat programı yapın.

Bu vergileri LLM'ye özel değil, veritabanı mühendisliği kalıplarıdır. LLM vergisi sadece LLM çağrılarının yavaş olmasıdır; diğer her şey standart dağıtılmış sistemlerdir.

### Gökkuşağı dağıtımı

Anthropic'in çoklu ajan araştırma sistemi "hemirbakır dağıtımları" kullanır: ajanın çalıştırma süresi birden fazla versiyonda aynı anda çalışır, bu nedenle uzun süre çalışan ajanların her kod dağıtımında öldürülmesi gerekmez. Kanarlı yeni sürümler bir trafik parçası üzerinde; ajanları bitince eski sürümleri geri çekmek.

Bu uzun süre çalışan devletli sistemler için standart; 2026 uyarlaması ajanların saatlerce yaşayabilmeleri, bu nedenle dağıtım döngüleri uyumlu olmalıdır.

### Kanonik üretim kontrol listesini

- Kalıcı durum (kontrol noktaları, anlık görüntüleri veya dış kutu + tekrarlanabilir kayıt).
- İdempotent yan etkileri.
- LLM çağrıları için async I/O katmanı.
- En azından bir kez dedup ile teslimat.
- Devasa iş yükleri için gökkuşağı/kanar dağıtım.
- Gözlem: ajan başına izler, süper adım denetimi, tekrar deneme numarası.

## Yapın.
```figure
sw-checkpoint-replay
```

## Yapın

`code/main.py`Uygulamaları:

- `CheckpointStore` SQLite desteklenen kontrol noktası logu ve iplik kimliği anahtarları. Her süper adım bir satır ekler.
- `run_with_checkpoint(agent, thread_id)` uçuş ortasında bir kaza simülasyonu; ikinci bir işçi son kontrol noktasından devam eder.
- `AgentQueue` küçük bir iş sırası olan ajan başına İzle / İşleme / Cevaplama durum makinesi.
- `demo_async_vs_threads()` asyncio ve threads üzerinden 500 simülasyonlu simülasyonlu "LLM çağrı" çalıştırır; duvar saati ve zirve hafızasını rapor eder (yaklaşılır).

Çık:

```
python3 code/main.py
```

Beklenen çıkış: kontrol noktası devamı simülasyonu çöküşten sonra başarılıdır; async sürümü 500 eşzamanlı çağrıyı < 1s'de ele alır; thread sürümü birkaç saniye sürer ve eşzamanlı birim başına büyüklük sıralamaları daha fazla bellek kullanır.

## Kullanın Kullanın

`outputs/skill-scaling-advisor.md`Sürekli çalıştırma seçeneği konusunda tavsiye eder: FastAPI + Postgres, LangGraph çalıştırma süresi, Zamanlı veya özelleştirilmiş.

## Gönderin.

Canonical üretim sertleştirme:

- **Start simple (Bedi's rule).**FastAPI + Postgres' i ölçene kadar başarısız.
- **Instrument everything before optimizing.**Bir atış için gecikme histogramı, bir adım için zaman, tekrar deneme sayısı, başarısızlık kategorisasyonu.
- **Outbox pattern for side effects.**Özellikle ödeme ve dış API çağrıları.
- **Rainbow deploys.**Uçuş sırasında ajanları asla öldürmeyin.
- **Adopt durable-execution engines (Temporal / LangGraph / Restate) when**Özel sorunlar yaşıyorsunuz: saatlerce insan bekleme, bölge çapındaki koordinasyon, karmaşık yeniden deneme/tüzelme politikaları.
- **Async for the I/O layer.**Sadece CPU'ya bağlı post-işleme için ipler.

## Egzersizler.

1. Çık .`code/main.py`Kontrol noktası devamı çalışmalarını doğrulayın; async vs. ip eşzamanlılık farkını ölçün.
2. Bir **outbox**tablo: her araç çağrısı önce dış kutuya yazılır, sonra ayrı bir goroutine/ görev yürütülür.
3. Simülasyonu**rainbow deploy**: iki eşzamanlı çalıştırma sürümü; her birine yeni thread_ids'lerin yarısını yönlendirin; eski sürümdeki uçuş içi threadlerin kesilmediğini onaylayın.
4. LangGraph'in çalıştırma süresi belgesini okuyun (aşağıda bağlantılıdır). Elle fırlatılmış FastAPI + Postgres sürümünde çalıştırma süresi hangi özelliklerin çoğaltılmasına en uzun sürdüğünü belirleyin. Bu benimsemenin bir nedeni mi yoksa ertelenir misiniz?
5. MegaAgent (arXiv:2408.09955) Bölüm 3. İki katlı koordinasyon (grup içi + gruplararası admin sohbet) açık.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Durable execution / 持久执行 | "Persist the program state" / "持久化程序状态" | Engine writes state after each super-step; crash recovery is deterministic. / 引擎在每个超步后写入状态；崩溃恢复是确定性的。 |
| Super-step / 超步 | "Transactional boundary" / "事务边界" | Unit of work between checkpoints. LangGraph term. / 检查点之间的工作单元。LangGraph 术语。 |
| thread_id / 线程 ID | "Agent run identifier" / "Agent 运行标识符" | Key that binds checkpoints and resume logic. / 绑定检查点和恢复逻辑的键。 |
| Idempotency / 幂等性 | "Safe to retry" / "安全重试" | Repeating a side effect produces the same result as one attempt. / 重复副作用产生与一次尝试相同的结果。 |
| Outbox pattern / 发件箱模式 | "Decouple side effects" / "解耦副作用" | Write intent to a table; a separate executor performs and marks done. / 将意图写入表；单独的执行器执行并标记完成。 |
| At-least-once delivery / 至少一次投递 | "Possible duplicates" / "可能重复" | Message queue semantics; dedup key makes consumer effective-once. / 消息队列语义；去重键使消费者有效一次。 |
| Rainbow deploy / 彩虹部署 | "Overlapping versions" / "重叠版本" | Multiple runtime versions concurrent during long-running workloads. / 多个运行时版本在长时间工作负载期间并发。 |
| Async fiber / 异步纤程 | "Cooperative yielding" / "协作让步" | User-mode concurrency; cheap compared to threads for I/O-bound loads. / 用户态并发；I/O 密集负载下比线程廉价。 |
| Checkpoint / 检查点 | "State snapshot" / "状态快照" | Serialized state at a super-step boundary; key for resume. / 超步边界处的序列化状态；恢复的关键。 |

## Daha fazla okumak

- [LangChain — The runtime behind production deep agents](https://www.langchain.com/conceptual-guides/runtime-behind-production-deep-agents) LangGraph çalıştırma süresi tasarımı
- [MegaAgent](https://arxiv.org/abs/2408.09955) Üreticilere göre üreticiler- tüketiciler sırası; binlerce eş zamanlı ajanlarda iki katlı koordinasyon
- [Matrix](https://arxiv.org/abs/2511.21686) Koordinasyon altyapısı olarak mesaj kuyrukları ile merkezi olmayan çerçeve
- [Temporal docs](https://docs.temporal.io/) Sürdürülebilir çalışmalar için referans çalışma akışı motoru
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) Gökkuşağı dağıtımını içeren üretim dersleri
