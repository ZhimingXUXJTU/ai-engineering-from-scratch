# Bölünmüş Prefill / Decode  NVIDIA Dynamo ve llm-d 分离式 预填充 解码 LLM

> Ön doldurma hesaplama bağlıdır; çözme hafıza bağlıdır. İkisini de aynı GPU'da çalıştırmak bir kaynak harcamaktadır. Ayrılama onları ayrı bir havuzlara ayırır ve NIXL üzerinden (RDMA/InfiniBand veya TCP fallback) aralarında KV önbelleği aktarır. NVIDIA Dynamo (GTC 2025 duyuru, 1.0 GA) Planner Profiler + SLA Planner otomatik oran-birleştirme prefill:decode oranlarını karşılamak için vLLM/SGLang/TRT-LLM  üzerinde oturur. NVIDIA bu ballpark  developer.nvidia.com'da performans artışlarını yayınlıyor. Nvidia.com (2025-06) orta zamanlı rejimde GB200 NVL72 + Dynamo'da DeepSeek-R1 MoE için ~6x iyileşmeyi göstermektedir. "30x" rakamı, tam bir dizi Blackwell + Dynamo + DeepSeek-R1 raporlarında topluluk toplamıdır; tam olarak 30x'i belirten tek bir ana kaynağı bulamadık, bu yüzden yönlendirme bir iddiası olarak ele alın. llm-d (Red Hat + AWS) Kubernetes-devlidir: bağımsız Hizmetler olarak görev başına HPA ile önceden doldur / çözme / yönlendiricisi. llm-d 0.5 hiyerarşik KV yükleme, önbelleğe uyan LoRA yönlendirme, UCCL ağları, ölçek-sıfır ekler. Ekonomik: Çoklu müşteri açıklamalarının iç içi bir şekilde yayılması, $2M-class inference spend (i.e., $600-800K/yıl) kolla satılan serviden Dynamo ile sabit SLA'da bölünmüş servise geçiş yaparken;$2M→$600-800K rakamı iç bir bileşiktir, tek bir yayınlanan vaka çalışması değil  onu büyüklük sırası demir olarak kullanın, bir referans alıntı değil. Kısa istekler (<512 token, kısa çıkış) transfer maliyetini haklı çıkarmaz.

> **【中文解读】**Bu bölüm, farklı parçalara ayrılmış bir şekilde yapılan bir ödemenin ve birleştirme aşamasının değerlendirilmesini anlatıyor.
**Type:** Learn
**Languages:** Python (stdlib, toy disaggregated-vs-colocated simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 08 (Inference Metrics)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy disaggregated-vs-colocated simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 08 (Inference Metrics) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 08 (Inference Metrics)

>  **【前置】**学本节前 Lütfen önce öğrenin:Fase 17·04(vLLM)、Fase 17·08(指标)。分离式 prefill/decode = 把两种瓶阶段(计算密集 vs 内存密集) 分到不同 GPU 池──
>  **【类比】**Çekilen hesaplama yoğunluğu (Prefill) = 厨师做菜(CPU/GPU 算力);Decode(内存密集) = 服务员端菜(带宽密集)。 Aynı GPU 跑两者 = 厨师又做又菜端菜,浪费某种资源──Dynamo/llm-d 把两者分池,KV cache 通过 NIXL(RDMA) 传输──NVIDIA发布:DeepSeek-R1 在 GB200+Dynamo 提速 ~6 倍;GB300+Dynamo MoE 吞吐最高 50 倍──$2M 推理账单可省 30-40%（即 $600-800K/year)。短请求(<512 token) 不值得──
**Time:** ~75 minutes | **时间:** ~75 minutes

## Öğrenme hedefleri

- Ön doldurma ve çözme neden farklı optimum GPU tahsislerine sahip olduğunu açıklayın ve kolokasyon altında atık miktarını ölçün.
  Çinçe Çevirisi: Neden önceden doldurma ve kodlama farklı en iyi GPU paylaşımı, ve oranlı olarak konum kaynak harcamaları vardır açıklayın.
- Ayrıntılı mimariyi çiz: önceden doldurma havuzu, çözme havuzu, NIXL üzerinden KV aktarımı, yönlendirici.
  Çine dilinde: 図制分离式架构图:预填充池、解码池、通過NIXL 的 KV 转移、路由器──
- Ayrımlama sonuç vermediğinde (kısık istekler, kısa çıkışlar) koşulunu belirtin.
  Çinçe Çevirisi: ︎ ︎ ︎ ︎
- NVIDIA Dynamo'yu (üstündeki yığın) ile llm-d'yi (Kubernetes doğası) ayırt edin ve her birini operasyonel bir bağlamla eşleştirin.
  Çine dilinde:区分 NVIDIA Dynamo (NVIDIA Dynamo)

## Sorunlar. Sorunlar.

> **【中文解读】**Bölünmüş önceden doldurma/ çözme çekirdek sorusu: önceden doldurma hesaplama kısıtlı, dekodlama hesaplama kısıtlı, aynı GPU üzerinde çalışmak için iki yöntemi bir kaynak kaybeder. Karışık çalışma yükü altında, karma çalışma yükü altında, %20-40'ın GPU's'da zaman kaybı yanlış kaynaklarda H100'in hesaplama gücü ile çalışırken, H100'in genişlik sürüşü hesaplama kısıtlılığıyla önceden doldurma yaparken veya H100'in genişlik sürüşü ile çalışırken.

> **【拓展：分离式推理的经济学】**Bölünmüş bir şekilde konuşulan ekonomik: İçeriği genel veriler gösterir ki, ortak bir hizmetten Dynamo bölünmüş bir şekilde dağıtımına geçişten sonra aynı P99  gecikmiş SLA'nın şartıyla %30-40 tasarruf yapılabilir.$2M 年支出可节省 $Baseten  Rapor Dynamo KV yönlendirme 带2x 更快 TTFT 和 61% 更高吞吐──关键条件:提示 >512 token + 输出 >200 token 时才值分离短提示的 KV 传输开销超过收益──

Llama 3.3 70B'yi 8 H100'de çalıştırırsınız. Karışık iş yükü altında (uzun istekler + kısa çıkışlar), GPU'lar çözme sırasında boşalır çünkü hesaplamaların çoğu önceden doldurma için harcanır. Farklı iş yükü altında (kuçük istekler + uzun çıkışlar), tam ters olur. Yerleştirilmiş önceden doldurma + çözme her ikisini de fazla sağlamanızı sağlar.

> **【中文解读】**
> Ön doldurucu işlem yoğunlaşmış bir işlemdir. Tüm prompt'ı işlemeyi, çözümü açıklama işleminin yoğunlaşmış bir işleminin yapılmasıdır. Her bir token sadece çok az miktarda hesaplanır. Aynı GPU ırkında da her iki işlemin de bir çeşit kaynakı vardır.

Bütçe etkisi: GPU zamanının 20-40%'si yanlış kaynakta harcanır. Hatıra bağlı dekodlama için H100 hesap satıyor veya hesap bağlı prefill çalıştırmak için H100 HBM bant genişliği satın alıyor. Her ikisi de pahalı atık.

Ayrımlama, prefill ve decode'yi her bir şişe boynuzuna göre büyük ayrı havuzlara ayırır. KV önbelleği, yüksek bant genişliği olan bir bağlantı yoluyla prefill havuzundan havuzunu dekode eder.

## Konsepten bir şey.

### Neden Boğazlar Farklıdır

**Prefill** transformatörü bir ileriye doğru tüm giriş istekleri üzerinde çalıştırın. Matris çarpımları baskın; hesaplama bağlı. H100 FP8 kullanışlı geçiş için ~2000 TFLOPS sağlar.

**Decode** her iterasyonda tam ağırlıkları okuyarak bir kez bir token oluşturun. bellek bant genişliği sınırlıdır. HBM3 ~ 3 TB / s verir.

Bu işlemler, H100'in her iki yönünde de iyi bir işlem yapması, ancak her iki yöntemi de aynı maliyetle yapılmasıdır.

### Mimarlık

```
            ┌──────────────┐
  Request → │    Router    │ ───────────────────────┐
            └──────┬───────┘                        │
                   │                                │
                   ▼ (prompt only)                  │
            ┌──────────────┐    KV cache    ┌───────▼──────┐
            │ Prefill pool │ ─── NIXL ────► │ Decode pool  │
            │  (compute)   │                │  (memory)    │
            └──────────────┘                └──────┬───────┘
                                                   │ tokens
                                                   ▼
                                                 Client
```

NIXL, NVIDIA'nın düğümler arası taşıma aracıdır. Kullanılabilir olduğunda RDMA/InfiniBand kullanır, aksi takdirde TCP geri dönüşü. Transfer gecikmesi gerçek  tipik olarak 70B FP8'deki 4K-token isteklerinin KV önbelleği için 20-80 ms. Bu nedenle kısa istekler parçalanmayı haklı çıkarmaz: transfer vergisi tasarruftan üstündür.

### Dynamo vs. llm-d

> **【中文解读】**两种分离式推理框架对比:(1) NVIDIA Dynamo位于 vLLM/SGLang/TRT-LLM 之上的编排器,Rust 核心 + Python 扩展,Planner Profiler 自动配置预填:decode 比如,在 GB200 NVL72 + DeepSeek-R1 MoE 上报告 6x 吞吐提升;(2) llm-d(Red Hat + AWS) Kubernetes 原生,prefill/decode/router 作为独立服务,per-role HPA,`packDomain: rack`确保同一机架内高带宽 KV 传输──选 Dynamo Eğer istediğinizde, bir düzenleyici, seçmek ister misiniz, eğer CNCF 生态──

**NVIDIA Dynamo**(GTC 2025 açıklaması, 1.0 GA):
- Orkestör olarak vLLM, SGLang, TRT-LLM'in üstünde oturuyor.
- Planer Profiler iş yükünü ölçer, SLA Planer otomatik olarak prefill:decode oranlarını yapılandırır.
- Kırmızı çekirdek, Python genişletilmesi.
- Geçim artışı: NVIDIA, GB200 NVL72 + Dynamo'da DeepSeek-R1 MoE için orta gecikme rejiminde 6x rapor ediyor (developer.nvidia.com, 2025-06); tam Blackwell + Dynamo + DeepSeek-R1 yığınlarında "30x'e kadar" topluluk raporları tek bir ana kaynağa sahip değil ve yönlendirme olarak değerlendirilmelidir.
- GB300 NVL72 + Dynamo: Dynamo ürün sayfasına göre 50 kat MoE throughput vs Hopper (developer.nvidia.com, tarihsiz).

**llm-d**(Red Hat + AWS, Kubernetes-native):
- Ön doldur / çöz / yönlendiricisi bağımsız Kubernetes Hizmetleri olarak.
- Sıradaki derinlik (prefill) / KV kullanım (decode) sinyalleri ile rol başına HPA.
- `topologyConstraint packDomain: rack`paketler, yüksek bant genişliği KV aktarımı için aynı rakta prefill+decode klikleri kullanır.
- llm-d 0.5 (2026): hiyerarşik KV yükleme, önbelleğe uyan LoRA yönlendirme, UCCL ağlama, ölçek-sıfır.

Yönetilen bir yığın üst orkestratör istiyorsanız Dynamo kullanın.

### Ekonomik

İç kompozit (tek bir yayınlanmış durum çalışması yapılmamış  büyüklük sırası demir):

- 2 milyon dolarlık yıllık sonuçlar, kolleksiyonlu servislere harcanıyor.
- Dinamo ile bölünmüş oldu.
- Aynı talep hacmi, aynı P99 gecikme SLA.
- Raporlanan tasarruflar: $600K–$800K/yıl (3040% azaltım).
- Yeni donanım yok.

Bu rakamı tek bir alıntı yapılabilir vaka çalışması yerine birden fazla müşteri açıklamasından sentezlemişizdir; Baseten'in 2 kat daha hızlı TTFT / Dynamo KV yönlendirme ile %61 daha yüksek geçiş noktası baseten'in (baseten.co, 2025-10), ve VAST + CoreWeave'in 60130% daha fazla token / $'ın 4060% KV hit oranı (vastdata.com, 2025-12) projesi. Para tasarrufu her havuzun doğru boyutunda olması ile elde edilir; önceden doldurma ağır iş yükleri (RAG'ler 8K+ önlemleri ile) dengeli olanlardan daha fazla yarar görür.

### Ne zaman bölünmemek

> **【拓展：分离式推理的适用条件】**Bölünmüş düşünce NOT  uygulanabilir sahne:(1) 提示 <512 token 且输出 <200 tokenKV 传输税超收益;(2) 小集群(<4 GPU) 没有足够的池多样性;(3) 团队无法运营两个按角色扩展的 GPU 池Dynamo 有帮助但并非简单;(4) 没有 RDMA 网络TCP 传输税更重;;NIXL'in 4K-prompt KV 位于 70B FP8 上约500MB,RDMA 100 GB/s 传输 = 5ms,TCP 10 GB/s = 50ms 来严格的SLA 差异巨大.

- < 512 token ve < 200 token çıkışları: Gelir üzerinde transfer vergisi baskın.
- Küçük küme (< 4 GPU): yeterli havuz çeşitliliği yok.
- Ekip, rol başına ölçeklendirme ile iki GPU havuzunu çalıştıramaz: Dynamo yardımcı olur ama önemsiz değildir.
- RDMA yapısı yok: TCP transfer vergisi daha ağır.

### Router 17 · 11 aşamasıyla entegre olur.

Ayrıntılı yönlendiriciler KV-cache-aware (Fase 17 · 11). Bir istek, ön yazısı  ile birlikte, bir önceki  ile eşleşmezse, prefill → decode akışları ile yer alır. Çıkış oranı ve ayrıntı bileşikleri  ön yazıcıya yeni bir ön yazma gerek olup olmadığını belirler.

### Blackwell'deki MOE gerçek rakamların olduğu yer.

> **【中文解读】**MoE(mixte uzman) modeli Blackwell'de üstündür ayrılıcı düşüncesinin en büyük faydalanıcısıdır. MoE'nin uzman yönlendirme aşamasında prefill 阶段 is computation intensive, decode 阶段 is内存 intensive (karşılıklı bir uzman kasa) olarak ayrılıcı iki kat kazanç sağlar.

> **【拓展：分离式推理与缓存路由的协同】**Bölünme düşüncesi yönlendiricisi KV-cache-aware ↓ 17·11) ↓ arayan 池da çözme zamanı, eğer önceden 缓存 varsa, doğrudan tekrar kullanılabilir ve önceden doldurulmadan geçmek gerekir 池命中率与分离部署的收益复合──NIXL, RDMA/InfiniBand (dosya edilebilir zaman) veya TCP dönüşü─4K-gecikletilmiş KV ile 70B FP8'deki aktarım gecikmesi yaklaşık 20-80 ms ↓ bu kısaca gösterilme bölünme bölümünün nedenini anlamıyor.

GB300 NVL72 + Dynamo Hopper tabanları üzerinde 50x MoE throughput gösterir. MoE uzman yönlendirme önceden doldurma üzerinde hesap ağırlığı, ancak çözme üzerinde bellek ağırlığı ( uzman önbelleği), bu nedenle parçalanma iki kat kazanç. 2026 sınır modeli hizmet MoE-dominant (DeepSeek-V3, gelecek GPT-5 çeşitleri).

### Hatırlamalısın numaralar

Benchmark numaraları  NVIDIA ve sonuçlar yığınları her çeyrek sonucunu güncelleyecek.

- GB200 NVL72 + Dynamo'da DeepSeek-R1: ~6x geçiş vs orta gecikme rejiminde temel çizgi (developer.nvidia.com, 2025-06); tüm Blackwell + Dynamo stacks'te topluluk "30x'e kadar" iddiaları tek bir ana kaynak olmadan yönlü toplamlardır.
- GB300 NVL72 + Dynamo: 50 kat MoE throughput vs Hopper (developer.nvidia.com, tarihsiz).
- Para biriktirme demir (daha iç kompozisyon, tek bir vaka çalışması değil): $600-800K/year off a $2 milyon yıllık harcama, sabit SLA.
- Ayrımlık eşiği: istekler > 512 token + çıkışlar > 200 token.
- NIXL üzerinden KV aktarımı: 70B FP8'de 4K-sürekli KV için 20-80 ms.

## Çerçeveyi kullanın.

> **【中文解读】**
> Bölünmüş yapı tüm durumlara uygun değil:短 prompt(<512 token) + 短输出请求不值 KV transfer 的开销;;只有长 prompt + 长输出或大量并发请求时才划算;; NVIDIA Dynamo 方案在 vLLM/SGLang/TRT-LLM 之上),llm-d 是 Kubernetes 原生方案(prefill/decode/router 作为独立服务);;

> **【拓展：分离式推理→下一代基础设施】**Bölünme düşüncesi, 2026 yılında LLM  altyapısının ön kenarında yer alan bir proje. NVIDIA'nın GB200 NVL72 机架专为预填/解码 分离设计,NVLink 带宽足够在 GPU 间传输 KV缓存中. Red Hat'ın llm-d projesi bu kapasiteyi Kubernetes 生态 带来了.
```figure
prefill-decode-split
```

## Kullan

`code/main.py`Kolokasyonlu vs. ayrıştırılmış servis simülasyonu.

> `code/main.py`Kolokasyonlu vs. ayrıştırılmış servis simülasyonu.

> `code/main.py`Kolokasyonlu vs. ayrıştırılmış servis simülasyonu.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-disaggregation-decider.md`- İş yükü ve gruplama göz önüne alındığında, bölünmek mi karar verir.

> 本课产 出 `outputs/skill-disaggregation-decider.md`- İş yükü ve gruplama göz önüne alındığında, bölünmek mi karar verir.

## Egzersizler.

1. Çık .`code/main.py`- Ayrımlama kolokasyonu ne kadar hızlı geçiyor?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ hangi öneride uzunluk altında ayrı ayrı dağıtım hizmetinden daha iyi?
2. P99 önbellek uzunluğu 8K, çıkış 300 ile RAG hizmeti için önceden doldurma havuzu ve çözme havuzu tasarlayın.
   Çine çevirisi: için P99 前长度 8K、300 输出 RAG 服务设计预填充池和码池。
3. Dynamo vs llm-d: Python çalıştırma süresi tercih edilmeyen saf Kubernetes dükkanı için birini seçin.
   ÇXMÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜÜÜÜÜNÜNÜÜÜÜÜÜÜÜÜNÜÜÜÜÜÜÜNÜNÜNÜNÜÜÜÜÜÜNÜÜÜÜÜÜNÜÜÜÜÜÜNÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜNÜÜNÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜNÜÜÜÜÜÜÜÜÜÜÜÜNÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜNÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜÜ
4. KV transfer maliyetini hesaplayın: 70B FP8'de 4K önceden doldurmak = ~500 MB KV. RDMA'da 100 GB/s'de transfer = 5 ms. TCP'de 10 GB/s = 50 ms. SLA için ne önemlidir?
   Çine çevirisi: hesap KV 转移成本:70B FP8 上 4K 预填充 = 约500MB KV──RDMA 100 GB/s 下传输 = 5ms──是否被解码延迟隐藏?
5. MoE uzman yönlendirme KV erişim kalıplarını değiştirir.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Disaggregated serving | "split prefill/decode" | Separate GPU pools for each phase |
| NIXL | "NVIDIA transport" | Dynamo's inter-node KV transfer (RDMA/TCP) |
| NVIDIA Dynamo | "the orchestrator" | Stack-above coordinator for vLLM/SGLang/TRT-LLM |
| llm-d | "Kubernetes native" | Red Hat + AWS K8s disaggregated stack |
| Planner Profiler | "Dynamo auto-config" | Measures workload, configures pool ratios |
| SLA Planner | "Dynamo policy" | Auto-rate-matches prefill:decode to meet SLOs |
| `packDomain: rack` | "llm-d topology" | Pack prefill+decode on same rack for fast KV |
| UCCL | "unified collective" | llm-d 0.5 networking layer for scale-to-zero |
| MoE expert routing | "expert per token" | DeepSeek-V3 pattern; disaggregation helps |

## Daha fazla okumak

- [NVIDIA — Introducing Dynamo](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/)
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/)
- [TensorRT-LLM Disaggregated Serving blog](https://nvidia.github.io/TensorRT-LLM/blogs/tech_blog/blog5_Disaggregated_Serving_in_TensorRT-LLM.html)
- [llm-d GitHub](https://github.com/llm-d/llm-d)
- [llm-d 0.5 release notes](https://github.com/llm-d/llm-d/releases)
