# LMCache KV Çıkarma ile vLLM Üretim Stack
# Üretim Hizmetleme Stack  KV Çıkartma ve Kaş Bilgisi Routing

> Bir üretim servisinde bir Kubernetes dağıtımında yığın teller yönlendiricisi, motorlar ve gözlemliliği  ve GPU'yu bırakabilecek bir kaynak olarak KV önbelleği ile davranır. KV boşaltma, GPU belleğinden KV önbelleğini çıkarır ve sorgular ve motorlar (CPU DRAM, sonra disk/Ceph) arasında tekrar kullanır. vLLM'nin üretim-buğdayı referans dağıtımdır; LMCache, boşaltma katmanıdır. vLLM 0.11.0 KV Deşüt Bağlantısı (Ocak 2026) bu asinkron ve Bağlantı API (v0.9.0+) üzerinden bağlanabilir hale getirir. Çıkış yolu genellikle istek yolundan gizlenir, ancak önbelleğin eksikliği ve promosyonlar son-son gecikmeyi ekleyebilir. LMCache paylaşılan önleme olmadan bile değerlidir  bir GPU'nun KV boşluklarından yoksun kalması durumunda, önceden gönderilen istekler yeniden hesaplama yerine CPU'dan geri yüklenebilir. 4 a3-highgpu-4g'de 16x H100 (80GB HBM) üzerinde yayınlanan referans değerleri: KV önbelleği HBM'yi aşırırken, hem yerel CPU yükü hem de LMCache geçiş hızını önemli ölçüde artırır; düşük KV ayak izi durumunda, tüm yapılandırmalar küçük genel maliyetlerle temel çizgiyi eşleştiriyor.

> **【中文解读】**Bu bölüm vLLM  Önerilen hizmetleri  PayedAttention 连续批处理和分块预填三大核心优化 
**Type:** Learn
**Languages:** Python (stdlib, toy KV-spill simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 06 (SGLang/RadixAttention)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy KV-spill simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang/RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang/RadixAttention)

>  **【前置】**Önemli bir şekilde, bu süreçte, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir sürecececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece
>  **【类比】**LMCache = "GPU 内存搬家"──KV cache 装不下 HBM → 溢出到CPU DRAM 再到磁盘──GPU 满时 预先请求可从CPU 恢复(无需重算预填)──异步、对用户透明──即使无共享前也值──16x H100 基准:KV 超HBM 时大幅升吞;低KV 占用时开销很小──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- VLLM üretim katmanlarının çizimini çizin: yönlendiricisi, motorlar, KV yükü çıkartılması, gözlemlenebilirlik.
  Çeviri: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Ç Ç Ç Çizgi: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- KV Deşüt Bağlantısı API'sini (v0.9.0+) ve 0.11.0 asinkron yolunun nasıl deşüt gecikmesini sakladığını açıklayın.
  Çeviri: KV Çıkarma Bağlantısı API ((v0.9.0+) ve 0.11.0 异步路径如何隐藏卸载延迟──
- LMCache CPU-DRAM'ın (KV > HBM) vs. overhead (KV HBM'ye uygun olmak için yeterince küçük) yardımı ne zaman ölçülüyor.
  Çinçe çevirisi: LMCache CPU-DRAMı ölçmek
- Yerel vLLM CPU yüklenmesi ve LMCache bağlantısı arasında seçim, dağıtım kısıtlamaları verildi.
  Çinçe Çevirimiçi:给定部署约束,在原生 vLLM CPU 卸载和 LMCache 连接器之间选择──

## Sorunlar. Sorunlar.

> **【中文解读】**vLLM 推理服务在高并发时 GPU HBM 占满,发生抢占事件请求被逐出、重新排队、同一个2K-token提示一分钟内被重新填充四次──GPU 计算花在冗余预填上,Goodput 远低于原始吞吐──添加更多 GPU 是线性成本,但CPU DRAM 很便宜一个插座有512GB+,延迟虽然比HBM 差几个数级,但对于"临时热温"的KV Cache 足够──

> **【拓展：vLLM Production Stack 架构】**VLLM üretim-butapı, 2026 yılında önerilen Kubernetes 部署方案, içerir: 1) Router cache-aware(Phase 17·11),消费 KV 事件;(2) Motorlar vLLM çalışanları, her GPU veya her TP/PP 组一个;(3) KV Cache 卸载LMCache 部署或原生连接器;(4) 可观测性Prometheus + Grafana + OTel izleri;(5) 控制面面服务发现、配置、滚动更新──以 Helm + operator 形式发布──

VLLM servisiniz, GPU'ları %100 HBM'de gösterir ve eşzamanlılık yükseldiğinde önleme olayları gösterir. Talepler çıkarılır, sıraya alınır ve aynı 2K-token istekini dakikada dört kez yeniden doldurursunuz. GPU hesaplamaları redundant prefills için harcanır; goodput hamı throughput'un çok altında.

Daha fazla GPU eklemek lineer olarak maliyetlidir. Daha fazla HBM eklemek mümkün değildir. Ama CPU DRAM ucuz  bir soket HBM'den daha kötü bir büyüklükteki gecikme siparişinde 512 GB +'e sahiptir, ancak "vazgeçmeden sıcak" KV önbelleği için iyidir.

LMCache, KV önbelleğini CPU DRAM'a çıkarır, böylece önceleri istenen istekler hızlıca geri kazanılır ve her motor yeniden doldurulmadan motorlar arasında tekrarlanan önbellekler önbelleği paylaşır.

## Konsepten bir şey.

### vLLM üretim aşaması

`github.com/vllm-project/production-stack`referans Kubernetes dağıtımıdır:

- **Router** cache-aware (Fase 17 · 11). KV olaylarını tüketir.
- **Engines** VLLM çalışanları. GPU veya TP/PP grubuna bir kişi.
- **KV cache offload** LMCache dağıtım veya yerel bağlantı.
- **Observability**Prometheus kazı, Grafana ara çubuğu, OTel izleri.
- **Control plane** hizmet keşfi, yapılandırma, süren güncellemeler.

Helm chart + operatörü olarak gönderildi.

### KV Şarj Bağlantısı API (v0.9.0+)

vLLM 0.9.0, eklenebilir KV önbelleği arka planları için bir Connector API'yi tanıttı. Motorunuz blokları bağlantıya yükler; bağlantı onları depolar (RAM, disk, nesne depolama, LMCache).

vLLM 0.11.0 (Ocak 2026) asinkron bir boş yük yolu ekler  boş yük arka planda gerçekleşebilir, böylece motor normal durumlarda onu engellemez. Sonundan sonuna kadar gecikme ve geçiş hala iş yükünün şekli, KV önbelleği isabet oranı ve sistem basıncından bağlıdır; vLLM'in kendi notları, özel çekirdeğin boş yükünün düşük isabet oranlarında geçiş oranını düşürdüğünü ve async programlamanın spekülasyonsal dekodla etkileşim sorunları olduğunu belirtmektedir.

### Doğal CPU yükleme karşı LMCache

> **【中文解读】**两种 KV Cache 卸载方案对比:(1) 原生 vLLM CPU 卸载引擎本地,存储 KV 块到主机 RAM,实现快速,零网络跳转,但不跨引擎共享;(2) LMCache 连接器集群级,存储块到共享 LMCache 服务器(CPU DRAM + Ceph/S3 压层), herhangi bir motor da erişilebilir.

**Native vLLM CPU offload**: motor-yalı. KV bloklarını host RAM'de saklar. uygulamaya hızlı, sıfır ağ hop. Motorları geçmez.

**LMCache connector**: cluster ölçeği. Blükleri ortak bir LMCache sunucusunda (CPU DRAM + Ceph/S3 seviyesinde) depolar. Blükler herhangi bir motor için erişilebilir. 16x H100 referansları yayınlandı.

Tek bir motor HBM basıncı olduğunda yerel seçin. Çoklu motorlar öntanımları paylaştığında LMCache seçin (orta sistem istekleri olan RAG, paylaşılan şablonlarla çoklu kiracı).

### Benchmark davranışları

> **【拓展：LMCache 基准测试数据】**LMCache 16x H100(80GB HBM) üzerinden 4 个 a3-highgpu-4g 基准测试表现:(1) 低KV 足迹(短提示、低并发) 所有配置匹配基线,LMCache 增加~3-5% 开销;(2) 中等足迹LMCache 开始在前复用方面提供帮助;(3) KV 超越 HBM原生 CPU 卸载和LMCache 显著改善吞吐量,LMCache 由于发动机共享收益更大.

16x H100 (80 GB HBM) 4 a3-highgpu-4g testinde yayılmış:

- Düşük KV ayak izleri (kısık istekler, düşük eşzamanlılık): tüm yapılandırmalar temel çizgiyle eşleşir, LMCache ~ 3-5% genel maliyeti ekler.
- Orta derecede ayak izleri: LMCache, motorlar arasında ön işaretlerin yeniden kullanılmasına yardımcı olmaya başlar.
- KV HBM'yi aşar: yerel CPU yükü ve LMCache ikisi de geçiş hızı önemli ölçüde artırır; LMCache motor çapındaki paylaşım nedeniyle daha büyük kazanç elde eder.

### LMCache belirgin olduğunda

> **【中文解读】**LMCache, aşağıdaki durumlarda belirleyici: 1) 多租户服务系统提示跨租户共享; 2) RAG文档块跨查询重复; 3) 微调变体(LoRA) 同一基础模型的 KV 复用减少冗余工作; 4) 抢占密集型工作负载 CPU 恢复比重新预填 更便宜。不应启动场景:HBM 压力小(只有开销没有收益) 短上下文(<1K token,传输时间 > 重新预填) 单租户单单单无复用可捕获提示)

> **【拓展：KV Cache 卸载的集成】**17·17 bölünmüş hizmet + LMCache'nin ortak etkisi: Ön doldurur 池den dekode 池'nin KV  transfer eğer hemen kullanılmıysa, LMCache'ye kaydedilebilir; sonraki sorgular LMCache'den yeniden doldurulmak yerine çekilir.

- Çoklu kiracı servisinde, sistem istekleri kiracılara paylaşılan bir servis.
- RAG, belgelerin parçalarının sorular arasında tekrarlandığı yer.
- Bas model KV'nin yeniden kullanılması gereksiz işlerin kesildiği aynı bazda ince ayarlanmış variantlar (LoRA).
- Önleme ağır iş yükleri: CPU'dan yeniden doldurmaktan daha ucuz bir şekilde geri yüklenir.

### Ne zaman etkinleştirmemek

- Küçük HBM basıncı  Üst maliyetini ödemeyi ücretsiz olarak yaparsın.
- Kısa bağlamlar (< 1K token)  transfer zaman > yeniden doldurma.
- Tek kiracı tek seferlik iş yükü  yakalamak için tekrar kullanılamaz.

### Ayrıntılı servis ile entegrasyon

17 · 17 aşama ayrıştırılmış servis + LMCache bileşikleri: KV, LMCache'deki önceden doldurma havuzundan kullanılmazsa havuz topraklarını çözmeye aktarır; sonraki sorular LMCache'den çekilir. 17 · 11 aşama önbelleği bilen yönlendirici, yerel veya LMCache- paylaşılmış önbelleği eşleşen motora yönlendirebilir.

### Hatırlamalısın numaralar

- vLLM 0.9.0: Bağlantı API gönderildi.
- vLLM 0.11.0 (Jan 2026): asinkron boş yük yolu; uçtan sonuna gecikme etkisi iş yüküne, KV çarpma hızına ve sistem basıncına bağlıdır (mutlak bir garanti değil).
- 16x H100 referans değer: KV ayak izi HBM' den fazla olduğunda LMCache yardımcı olur.
- Küçük HBM basıncı: 3-5% üst maliyet, fayda olmadan.

## Çerçeveyi kullanın.
```figure
zero-sharding
```

## Kullan

`code/main.py`LMCache ile ve olmadan önleme ağır bir iş yükünü simüle eder.

> `code/main.py`LMCache ile ve olmadan önleme ağır bir iş yükünü simüle eder.

> `code/main.py`LMCache ile ve olmadan önleme ağır bir iş yükünü simüle eder.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-vllm-stack-decider.md`. İş yükünün şekli ve vLLM dağıtımını göz önüne alarak, native vs LMCache vs. hiçbirini belirler.

> 本课产 出 `outputs/skill-vllm-stack-decider.md`. İş yükünün şekli ve vLLM dağıtımını göz önüne alarak, native vs LMCache vs. hiçbirini belirler.

## Egzersizler.

1. Çık .`code/main.py`LMCache hangi HBM kullanımı ile ödeme yapmaya başlar?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`LMCache hangi HBM kullanımı oranında tasarlamaya başladı?
2. Bir kiracı, 6K-token sistemi ile 200 sorgu / saat boyunca paylaşır. Kiracı başına beklenen LMCache tasarrufu hesaplayın.
   Çinçe Çevirisi: bir kiracıda 200 查询/小时中共享 6K token 系统提示――计算 LMCache 的预期节省──
3. LMCache sunucusu tek bir başarısızlık noktasıdır. HA stratejisini (replikler, doğaya geri dönüş) tasarlayın.
   Çinçe Çevirimi:LMCache  server is单点故障──设计 HA 策略(副本、回退到重算)。
4. LMCache, Ceph'e dönüm disken depolar. 70B FP8 (500 MB) 4K-token KV için okuma süresi vs. yeniden doldurma ne kadar?
   Çinçe Çevirimi:LMCache  Makine sert disketinde depolanır Ceph。 70B FP8 için 4K token KV(500MB),读取延迟是多少?与重算比较。
5. VLLM 0.11.0 asinkron yolunun "beyaz" olup olmadığını tartışın  üst uç nerede saklanıyor?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Production-stack | "the reference deployment" | vLLM's Kubernetes Helm chart + operator |
| Connector API | "KV backend interface" | vLLM 0.9.0+ pluggable KV store interface |
| Native CPU offload | "engine-local spill" | Store KV in host RAM of same engine |
| LMCache | "cluster KV cache" | Cross-engine KV cache server on CPU DRAM + disk |
| 0.11.0 async | "non-blocking offload" | Offload hidden behind engine stream |
| Preemption | "evict to make room" | KV cache shuffle when HBM full |
| Prefix reuse | "same system prompt" | Multiple queries share beginning; cache hit |
| Ceph tier | "disk tier" | Durable storage below DRAM in the cache hierarchy |

## Daha fazla okumak

- [vLLM Blog — KV Offloading Connector (Jan 2026)](https://blog.vllm.ai/2026/01/08/kv-offloading-connector.html)
- [vLLM Production Stack GitHub](https://github.com/vllm-project/production-stack) Helm grafik + operatör.
- [LMCache for Enterprise-Scale LLM Inference (arXiv:2510.09665)](https://arxiv.org/html/2510.09665v2)
- [LMCache GitHub](https://github.com/LMCache/LMCache) Bağlantı uygulaması.
- [vLLM 0.11.0 release notes](https://github.com/vllm-project/vllm/releases) Asinkron yol ayrıntıları.
