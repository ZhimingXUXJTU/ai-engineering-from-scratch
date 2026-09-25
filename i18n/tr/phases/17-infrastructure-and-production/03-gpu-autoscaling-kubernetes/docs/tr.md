# GPU Otomatik ölçeklendirme Kubernetes  Karpenter, KAI programcı, çete programlaması    Otomatik genişletilmiş Kubernetes  GPU düzenleyici

> Üç kat, bir kat değil. Karpenter rezervi düğümleri dinamik (bir dakikadan az, Cluster Autoscaler'den %40 daha hızlı). KAI Scheduler, grup programlamasını, topoloji farkındalığını ve hiyerarşik kuyrukları ele alır. Uygulama düzeyinde otomatik ölçeklendiriciler (NVIDIA Dynamo Planner, llm-d Workload Variant Autoscaler) sonuçlandırma spesifik sinyalleri üzerinde ölçeklendirir  kuyruk derinliği, KV önbelleği kullanımı  CPU / DCGM görev döngüsü değil. Klasik HPA tuzağı budur .`DCGM_FI_DEV_GPU_UTIL`Bu ders size üç katmanı oluşturmayı ve varsayılan Karpenter'i önlemek için öğretir.`WhenEmptyOrUnderutilized`GPU işlerinin çalışmasını durdurmak için bir politika.

> **【中文解读】**Bu bölümde GPU otomatik genişleme  Kubernetes  LLM  önerme hizmetleri  GPU kaynak otomatik genişleme stratejisi 
**Type:** Learn
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator)
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator) | **语言:** Python（标准库，队列深度自动扩缩模拟器）
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 02（推理平台经济学）, Phase 17 · 04（vLLM 服务内部）

>  **【前置】**学本节前 Lütfen önce öğrenin:Fase 17·02(platform ekonomi)、Fase 17·04(vLLM)、Kubernetes 基础。三层扩缩:Karpenter(节点层)+ KAI Scheduler(Pod 层 帮 调度)+ 应用层(队列深度/KV利用率)。
>  **【类比】**GPU 扩缩 = "餐厅运力调度"。Karpenter = 开新店(分钟级);KAI = 桌位组合(gang scheduling 防 7/8 部分分配,7 桌等 1 桌);应用层 = 服务员按等位队列长度调座。HPA 陷:DCGM kullanım oranı %100 % %10 个或100 个请求必须使用 Goodput(Phase 17·08) 替补。

## Öğrenme hedefleri

- Üç otomatik ölçekleme katmanını (nod sağlama, grup programlaması, uygulama düzeyi) çiz ve her katman için kullanılan araçın adını verin.
  Çinçe Çevirimi: çizim üç katlı otomatik genişleme aşaması (节点供给、gang 调度、应用级)并命名每层使用的工具──
- Nedenini açıkla `DCGM_FI_DEV_GPU_UTIL`vLLM için yanlış HPA sinyali ve iki değiştirme adı (kuyruk derinliği, KV önbelleği kullanımı).
  Çeviri: Neden?`DCGM_FI_DEV_GPU_UTIL`HPA  sinyalini yanlış olarak belirtti ve iki alternatif çözüm ortaya çıkardı.
- Grup programlamasını ve kısmi tahsis hata modunu açıklayın. KAI Scheduler'ın önlediği (7 GPU'dan 8'i boş).
  Çinçe Çevirimiçi: 调度和 KAI 调度和 KAI 调度和 KAI 调度和 KAI 调度和 KAI 调度和 KAI 调度和 KAI 调度和 KAI 调度和 KAI 调度和 KAI 调度和 KAI 调度模式 调度模式 调度模式 调度模式 调度模式 调度模式 调度模式 调度模式 调度模式 调度模式 调度模式 调度模式 调度模式 调度 和 KAI 调度 和 KAI 调度 和 KAI 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度 调度
- Karpenter konsolidasyon politikasını isimlendirin (`WhenEmptyOrUnderutilized`) GPU işlerinin çalışmasını sona erdirir ve 2026'da güvenli bir alternatif belirtiyor.
  Çinçe Çevirimiçi:                                                                                                                                                                                                                                                           `WhenEmptyOrUnderutilized`), 2026 yılındaki güvenlik alternatif programını açıkladı.

## Sorunlar. Sorunlar.

> **【中文解读】**GPU otomatik olarak Kubernetes üzerinde üç aşamalı bir故障 mode vardır: 1) HPA kullanmak yanlış sinyaller (GPU 占用率而非队列深度), bu genişleme zamanı genişleme neden olur; 2) Cluster Autoscaler 节点 supply too slow,长提示请求超时; 3) Multi GPU dağıtımlı düşünce zaman bölümü dağıtım; 7) of-8 tuzağı), 7 GPU 空转等第 8 个.

> **【拓展：GPU 集群管理】**2026 yılında Kubernetes LLM 推理服务的标准编排平台了──NVIDIA DGX Cloud、Google GKE、AWS EKS 都提供GPU 节点池管理──关键挑战在GPU 节点池管理──H100 约$3-4/h), genişletilme kararları kesinleştirilmesi gerekir 过度供给浪费成本,供给不足影响SLA──Karpenter + KAI Scheduler'ın birliği şu anda en olgun GPU 调度方案larıdır──

Ekibiniz Kubernetes'e LLM hizmetini veriyor.`DCGM_FI_DEV_GPU_UTIL`HPA iş saatlerinde %100 kullanımında servis pinleri. HPA asla büyütmez  zaten dolu olduğunu düşünüyor.

> Senin takımın Kubernetes'te bir LLM servisini hazırladı.`DCGM_FI_DEV_GPU_UTIL`作为信号设置了HPA──服务在业务时段保持在100%利用率──HPA 从不扩容它认为你已经满满了──你手动添加一副本;TTFT 下降──HPA 仍然不扩容──信号在欺骗你──

Ayrı bir şekilde, düğümler için Cluster Autoscaler kullanıyorsunuz. 1M-token istekleri sabah 2'de gelir; kümeler 3 dakika bir düğüm sağlıyor ve talep süreleri çıkıyor.

> Diğer taraftan, Cluster Autoscaler'ı kullanıyorsunuz.

Ayrı bir şekilde, 2 düğüm üzerinde 8 GPU gerektiren 70B modelini dağıtıyorsunuz. Kluster 7 GPU'ya sahiptir ve 1 3 düğüm üzerinde yayılmıştır. Kluster Autoscaler 1 eksik GPU için bir düğüm sağlar.

> Tekrar bir taraftan, siz bir 70B modeli dağıttınız ki 2 节 8 GPU'ya ihtiyaç duyulur. 集群 7  GPU boşlukta, 1 节 3 节 üzerinde dağılmış.

Üç katman, üç farklı başarısızlık modu. 2026'da GPU-a karşı otomatik ölçeklendirme HPA'yı açmıyor.

> Üç kat, üç farklı sorun mode──2026 yılının GPU  algılama otomatik genişleme "HPA aç" değil──bu bir kombinasyon düğüm tedarik、gang 调度和应用信号自動扩展──

## Konsepten bir şey.

### Katman 1  düğüm sağlama (Karpenter)

> **【中文解读】**İlk katman, bir düğüm tedarik etmektedir. Karpentre'nin kontrol ve ayarlama modülü, geleneksel bir Cluster Autoscaler'e kıyasla %40'lık bir GPU düğümünü 45-60 saniye içinde oluşturur.`WhenEmptyOrUnderutilized`合并策略 It will terminate running 推理的 GPU 节点 to migrate to cheaper instance type, leading request failure and model reload 5-20 分钟中断) GPU 池应使用 `WhenEmpty`+ `consolidateAfter: 1h`Güvenlik stratejisi.

Karpenter bekleyen kapsüller ve tedbir düğümlerini ~ 45-60 saniye içinde izler (Cluster Autoscaler genellikle GPU düğümleri için 90-120 saniye alır).`NodePool`kısıtlama  eğer kapsülünüz 8 H100'e ihtiyaç duyar ve kümenin eşleşen düğmesi yoksa, Karpenter mevcut bir grubu ölçeklendirmek yerine doğrudan birini sağlar.

> Karpenter  Pod'u kontrol ederken, yaklaşık 45-60 saniye içinde tedarik noktasına ulaştırır.`NodePool`约束动态选择实例类型 Eğer Pod 需要8个 H100 且集群没有匹配节点,Karpenter 直接供应一个,而不是扩展现有组──

**The consolidation trap**Karpenter'ın varsayımsızlığı.`consolidationPolicy: WhenEmptyOrUnderutilized`GPU havuzları için tehlikeli. GPU düğümünü çalıştırarak kapsülleri daha ucuz ve doğru boyutlu bir örnekle aktarır.

> **合并陷阱**Karpenter'ın dediği gibi:`consolidationPolicy: WhenEmptyOrUnderutilized`GPU'ya karşı çok tehlikeli. Çalışan GPU'nun örüngesini sona erdirecek ve Pod'u daha uygun örneklere taşıyacak.

GPU havuzları için güvenli ayar:

```yaml
disruption:
  consolidationPolicy: WhenEmpty
  consolidateAfter: 1h
```

Karpenter'ın bir saat sonra boş düğümleri birleştirmesine izin verir ama çalışan bir işi asla boşaltmaz.

> Karpenter'ın bir saat sonra gerçek anlamda boş bir noktaya ulaşmasını sağlayalım ama asla görevlerini ortadan kaldırmayacağız.

### Katman 2  çete programlaması (KAI programlayıcı)

> **【中文解读】**İkinci katı düzen koordinasyonu. KAI Scheduler  çözme varsayılan kube-scheduler  çözülemez üç sorun: 1) Gang Scheduling tamamı var tamamı düzensiz, 8-GPU  önermek veya tüm başlatmak veya tüm beklemek; 2) 拓 algılama NVLink/InfiniBand/机架拓放置 Pod; 3) bölge sıra sıraları 多团队竞争同一GPU 池时按优先级和配额管理

> **【拓展：GPU 调度器生态】**2026 yılı GPU 调度器'ın seçimi KAI Scheduler'i içerir(原 Karp,支持gang + topology + queue)、YuniKorn(Apache 项目,支持队列和抢占)、以及默认 kube-scheduler + 设备插件。KAI Scheduler'i tek orijinal olarak desteklenen grup programlaması programıdır, Ray ve vLLM üretim-stack 集成──

KAI Scheduler (sonradan "Karp" projesi olarak adlandırılan) varsayılan kube-scheduler'ın yapmadığı şeyleri ele alır:

**Gang scheduling**Bu programın tümü veya hiçü programlanmıştır. 8 GPU'yı gerektiren dağıtılmış bir sonuçlama kapsülü ya 8 GPU'sı birlikte başlar ya da hiçbiri olmaz.

**Topology awareness** hangi GPU'ların NVLink'i paylaştığını, aynı rafta oturan ve aralarında InfiniBand bulunanlarını bil.

**Hierarchical queues** birden fazla ekip öncelik ve kvota ile aynı GPU havuzuna rekabet eder. A Takımı'nın üretim sıkıntısı, B Takımı'nın eğitim işiyle yalnızca öncelik kuralları izin verdiği takdirde ön plana geçiyor.

KAI kube-scheduler ile birlikte ikinci bir programlayıcı olarak kullanılır; kullanmak için iş yüklerini not ediyorsunuz.

> KAI 作为二级调度器与 kube-scheduler 一起部署;你通过注解让工作负载使用它──Ray 和 vLLM üretim-stack 都已集成──

### Katman 3  Uygulama düzeyinde sinyaller

> **【中文解读】**Üçüncü kat uygulamalı bir sinyal.`DCGM_FI_DEV_GPU_UTIL`GPU işleme oranı (customity cycle) göstergesi 100% 100 100                                                                                                                                                                                                                                                   

> **【拓展：推理感知自动扩缩】**NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler, 2026 yılında LLM 推理设计'e özel bir genişleştirici. Bunlar doğrudan tüketim düşünce motorunun iç göstergesiydi.

**The HPA trap**- Evet .`DCGM_FI_DEV_GPU_UTIL`Bu, GPU'nun her örnekleme aralığında çalışıp çalışmadığını ölçer. %100 kullanımı 10 eşzamanlı talep veya 100 anlamına gelebilir; GPU her iki şekilde meşguldi.

Daha da kötüsü, vLLM ve benzeri motorlar KV önbelleği belleğini önceden tahsis eder (ya da `--gpu-memory-utilization`Bir istekle bile hafıza kullanımı %90'a yakın kalır.

**2026 replacement signals**- ...

- Sır derinliği (ön doldurulmayı bekleyen talepleri sayısı).
  Çinçe Çevirim: Koteyin derinliği (Köşek sayısı)
- KV önbelleği kullanımı (blokların aktif dizilere ne kadar bölümü tahsis edilir).
  Çinçe Çevirim:KV 缓存利用率 (KV 缓存利用率)
- Replik P99 TTFT (SLA sinyali).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Güç (saniye başına tüm SLO'ları karşılama talepleri).
  Çinçe Çevirimi:Goodput (((每秒满足所有 SLO 的请求数)

NVIDIA Dynamo Planer ve llm-d Workload Variant Autoscaler bu sinyalleri ve ölçek kopyalarını tüketir. LLM servisinde HPA'yı tamamen değiştirirler.

> NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler 消费这些信号并扩缩副本──它们完全取代了LLM 服务中的HPA──

### Ne zaman kullanılır

| Scale decision / 扩缩决策 | Tool / 工具 |
|----------------|------|
| Add/remove nodes / 添加/移除节点 | Karpenter |
| Schedule multi-GPU jobs / 调度多 GPU 任务 | KAI Scheduler |
| Add/remove replicas / 添加/移除副本 | Dynamo Planner / llm-d WVA (or custom HPA on queue depth) |
| Choose GPU type / 选择 GPU 类型 | Karpenter NodePool |
| Preempt low-priority / 抢占低优先级 | KAI Scheduler queues |

> **【拓展：GPU 集群成本优化策略】**GPU 集群 cost optimization in 2026 key strategies include:(1) Spot InstanceAWS/GCP/Azure's GPU Spot instance contours can save 60-70%, but needs to process interruption(Karpent + 热池缓解);(2) Auto expansionKarpentür non-high peak period period period auto shrinkage节点池,50% 成本节省;(3) GPU 共享通过MIG(Multi-Instance GPU) H100 切除为多个实例,适合小模型推;(4) 混合 GPUFP8/INT4 量化减少内存需求,允许更多并发;(5) 分离式部署prefill/decode 分离到不同本类 节省,30-40% 成本节省;;

### Ayrıntılı prefill/decode her şeyi karmaşıklaştırır.

> **【中文解读】**Bölünmüş ön doldurma/ çözme yapı: 17·17 aşaması daha fazla genişleme karmaşıklığını arttırır: ön doldurma Pod  sıraya göre derin genişleme, KV Cache Pod  basınç genişleme.

> **【拓展：Kubernetes GPU 生态】**2026 yılında Kubernetes GPU  yönetiminin anahtar bileşenleri şunlardır: NVIDIA GPU Operatörü(otomatik yükleme sürücü/CUDA/konteyner araç kümesi)、NVIDIA Cihaz Eklentisi(GPU  kaynak keşfi ve dağıtım)、MIG(Multi-Instance GPU, bir 張 A100/H100 切分为多个实例)、时间分片(GPU 共享)。结合Karpenter + KAI Scheduler + Dynamo Planner,

Ayrıntılı prefill/decode (Fase 17 · 17) çalıştırırsanız, farklı ölçeklendirme tetikleyicileri olan iki pod sınıfınız vardır: ön doldurucu pods ölçeği kuyruk derinliği üzerinde, KV önbelleği basıncı üzerinde dekode pods ölçeği üzerinde. llm-d bunları ayrı olarak ortaya çıkarır `Services`Her iki rolün önüne tek bir HPA koymaya çalışmayın.

> Eğer çalışıyorsanız ayrılıksız prefill/解码(Fase 17 · 17), farklı genişleme hatalı iki Pod türü vardır: prefill Pod 按队列深度扩充,解码 Pod 按 KV 缓存压扩充──llm-d 它们将暴露为独立的`Services`Her rolün kendi HPA'sı vardır.

### Soğuk başlangıç burada da önemli .

Karpenter'in 45-60 saniye ısıtması artı 20GB model yükü artı motor init, sıfırdan başlayan bir istek 2-5 dakika sürer.`min_workers=1`) SLO- kritik yollar için veya uygulama katmanında Modal tarzında kontrol işaretleme kullanın.

> Sıcak başlatma缓解(Fase 17 · 10) is node supply time become user perceptible locale──Karpentrin 45-60 saniye ön sıcaklığı artı 20GB  model yükleme artı motor başlangıcı yani sıfırdan başlayan istek 2-5 dakika gerekir── SLO 关键路径保持热池(`min_workers=1`), veya uygulama aşamasında Modal 风格的检查点──

### Hatırlamalısın numaralar

- Karpenter düğümleri: ~ 45-60s vs. Cluster Autoscaler ~ 90-120s (GPU düğümleri).
  Çeviri:Karpentre 节点供给: yaklaşık 45-60 saniye vs. Kluster Otoscaler yaklaşık 90-120 saniye
- KAI Scheduler, kısmi tahsis atıklarının  7/8 tuzağından kaçınmasını sağlar.
  Çeviri: KAI Programcı 防止部分分配浪费 7 of 8 陷。
- `DCGM_FI_DEV_GPU_UTIL`HPA sinyali olarak: kırılmış; kuyruk derinliği veya KV kullanımı kullanın.
  Çeviri:`DCGM_FI_DEV_GPU_UTIL`作为 HPA 信号:有缺陷;队列深度或 KV利用率的使用率──
- Karpenter `WhenEmptyOrUnderutilized`: GPU işlerini çalıştırmayı bitirir.`WhenEmpty + consolidateAfter: 1h`- Bu sonuca varmak için.
  Çarpentör`WhenEmptyOrUnderutilized`:终止运行中的 GPU 任务──推理使用 `WhenEmpty + consolidateAfter: 1h`- Evet.

## Çerçeveyi kullanın.

> **【拓展：GPU 自动扩缩成本模型】**GPU otomatik genişletilmesinin maliyet optimize edilmesinin merkezi ise boş dönüşüm süresi azaltmaktır.$3/hr）为例，8-GPU 集群 24/7 运行每月成本约 $17.280── Karpenter üzerinden 按需供应`WhenEmpty`合并策略 + 推理感知 HPA, non-高峰时段自动缩放容量至2GPU,将月成本降至约$8,640 (%50 tasarruf) ⋅ Spot instance,60-70% tasarruf yapabilir, ancak işlem kesimi gerekir。
```figure
autoscaling
```

## Kullan

`code/main.py`Üç katmanlı bir oto-skalatörü patlayan bir GPU iş yükü üzerinde simüle eder. Saf HPA ( görev döngüsü), kuyruk derinliği HPA ve KAI-gaş programlı ölçeklemeyi karşılaştırır.

> `code/main.py`Gelişmiş GPU  工作负载上模拟三层自动扩缩机──比较简单 HPA(占用率) 队列深度 HPA 和 KAI 调度扩缩──报告未满足的请求数、空 GPU 分钟数和综合评分──

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-gpu-autoscaler-plan.md`. Kluster topolojisi, iş yükü şekli ve SLO göz önüne alındığında, üç katlı bir otomatik ölçekleme planı tasarlıyor.

> 本课产 出 `outputs/skill-gpu-autoscaler-plan.md`❖ Gösterilen yoğunluk, iş yükü şekli ve SLO, üç katlı otomatik genişleme programı

## Egzersizler.

1. Çık .`code/main.py`Bir iş yükü altında, saf görev döngüsü HPA kaç kere alıyor?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ Çıkışlı iş yükü altında, basit işlenme oranı HPA  kaç tane talep alındı?
2. H100 SXM5'te Llama 3.3 70B FP8 hizmet veren bir klaster için Karpenter NodePool tasarlayın.`capacity-type`- Evet .`disruption.consolidationPolicy`- Evet .`consolidateAfter`, ve GPU olmayan iş yüklerini bu düğümlerden uzak tutan bir leke.
   中文翻译:为在 H100 SXM5 上服务 Llama 3.3 70B FP8 的集群设计 Karpenter NodePool──指定 `capacity-type`- Evet.`disruption.consolidationPolicy`- Evet.`consolidateAfter`Yapılacak olmayan GPU 工作负载隔离的污点──
3. Ekibiniz, "GPU'lar mevcut ama modül programlamıyor" diye dağıtımların beklenmekte olduğunu bildirir.
   Çinçe Çevirimi: Your Team Report Deployment卡在等待状态因为"GPU kullanılabilir ama Pod 调度不能"──诊断是卡潘特,立方-调度仪还是KAI调度仪? Hangi göstergeleri doğrulayabiliriz?
4. Otomatik ölçekli prefill pods'a bir sinyal ve dekode pods'a farklı bir sinyal seçin.
   Çinçe Çevirimiçi: seçin bir sinyal için genişletmek için ayrılma biçiminde önceden doldurma Pod, diğer bir sinyal için çözme Pod.
5. `WhenEmptyOrUnderutilized`24×7 üretim servisinde, günde ortalama 60 talep düşüş olayı olan P99 TTFT > 10s'de bir konsolidasyon tuzağı.
   Çeviri: Kürt`WhenEmptyOrUnderutilized`合并陷 24x7 üretim hizmetindeki maliyet, bu hizmet günde ortalama 60 kez istek atılmasını gerektirir, P99 TTFT > 10 saniye

## Anahtar Şartlar .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Karpenter | "the node provisioner" / "节点供给器" | Kubernetes node autoscaler; sub-minute provisioning / Kubernetes 节点自动扩缩器；亚分钟级供给 |
| Cluster Autoscaler | "the old scaler" / "旧扩缩器" | Kubernetes node autoscaler predecessor; slower, group-based / K8s 节点扩缩前身；更慢，基于组 |
| KAI Scheduler | "the GPU scheduler" / "GPU 调度器" | Secondary scheduler for gang + topology + queues / 用于 gang + 拓扑 + 队列的二级调度器 |
| Gang scheduling | "all or nothing" / "全有全无" | Schedule N pods atomically or defer all of them / 原子调度 N 个 Pod 或全部推迟 |
| Topology awareness | "rack-aware" / "机架感知" | Place pods based on NVLink/IB/rack placement / 基于 NVLink/IB/机架放置 Pod |
| `DCGM_FI_DEV_GPU_UTIL` | "GPU utilization" / "GPU 利用率" | Duty-cycle metric; NOT a scaling signal for LLMs / 占用率指标；不是 LLM 的扩缩信号 |
| Queue depth | "waiting requests" / "等待请求" | Correct HPA signal for prefill-bound scaling / 预填充扩缩的正确 HPA 信号 |
| KV cache utilization | "memory pressure" / "内存压力" | Correct HPA signal for decode-bound scaling / 解码扩缩的正确 HPA 信号 |
| Consolidation | "Karpenter consolidation" / "Karpenter 合并" | Node termination to cheaper instance type / 终止节点迁移到更便宜实例 |
| `WhenEmpty + 1h` | "safe consolidation" / "安全合并" | Policy that doesn't evict running GPU jobs / 不驱逐运行中 GPU 任务的政策 |

## Daha fazla okumak

- [KAI Scheduler GitHub](https://github.com/kai-scheduler/KAI-Scheduler) tasarım belgeleri ve yapılandırma örnekleri.
- [Karpenter Disruption Controls](https://karpenter.sh/docs/concepts/disruption/) konsolidasyon politikası semantikası ve GPU güvenli standardlar.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/)Dinamo Planer'ın sinyalleri.
- [Ray docs — KAI Scheduler for RayClusters](https://docs.ray.io/en/latest/cluster/kubernetes/k8s-ecosystem/kai-scheduler.html) Çığlık entegrasyon modeli.
- [AWS EKS Compute and Autoscaling Best Practices](https://docs.aws.amazon.com/eks/latest/best-practices/aiml-compute.html) yönetilen-Kubernetes-sözlü rehberlik.
- [llm-d GitHub](https://github.com/llm-d/llm-d) İş yükü Variant Autoscaler tasarımı.
