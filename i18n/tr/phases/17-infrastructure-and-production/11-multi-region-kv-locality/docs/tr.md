# Çok Bölgelik LLM Hizmet ve KV Kayıt Yerellik .

> Round-robin yük dengeleme, önbelleğe alınmış LLM sonuçları için aktif olarak zararlıdır. Önceden belirtilmiş düğmeye yerleşmeyen bir istek, uzun bir istekle, önbellekle ~80 ms karşılaştırıldığında P50'de yaklaşık 800 ms'lik tam önceden doldurma maliyetini öder. 2026 yılında üretim modeli, KV-cache olaylarını ve prefix-hash eşleşmesi üzerinde rotaları tüketen bir önbelleğe farkındalıklı yönlendirici (vLLM Router in Rust, llm-d yönlendirici) olacaktır. Son araştırmalar (GORGO) yönlendirme hedefi için bölge çapındaki ağ gecikmesini açık bir terim haline getirmiştir. Ticari "bölge çapındaki sonuçlandırma" teklifleri (Bedrock bölge çapındaki sonuçlandırma, GKE çoklu küme geçitleri) sonuçlandırmayı net olmayan bir şekilde değerlendirir  TTFT değil, mevcutluğu ele alırlar. JPMorgan ve Mayo Klinik'i, Kasım 2024'te yaklaşık 22 dakika boyunca, bizim doğu 1'ün başarısızlığını gerçekleştirdi. DR gerçekliği: LLM DR başarısızlıklarının %32'si takımların ağırlıkları yedeklediği ama tokenizer dosyalarını veya kuantitasyon yapılandırmalarını unuttuğu için.

> **【中文解读】**Bu bölüm çok bölgelik KV 局部性跨区域部署 LLM 时的 KV Cache 优化策略を紹介しています.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy prefix-cache-aware router simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving), Phase 17 · 06 (SGLang RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving), Phase 17 · 06 (SGLang RadixAttention)

>  **【前置】**Önemli bir şekilde, bu programın en son gerçekleşmesi için bir süreliğine bir süreliğine daha fazla bilgi alınacaktır.
>  **【类比】**Çok bölgelik LLM = "连锁餐厅中央厨房"──Round-robin = 随机送单到分店(缓存命中率 0,每次重复做);Cache-aware router = 按前哈希送到已有缓存的分店(命中 80ms vs 未命中 800ms)──JPMorgan/Mayo Clinic 2024 灾备演练 22 分钟切换──失败教学:32% LLM DR 失败因为只备权重重忘了代币器量或配置文件清单必须完整──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- Dört-robin yük dengeleme kırıklıklarının neden önbelleğe alınmış olduğunu ve TTFT cezasını ölçdüğünü açıklayın.
  Çinçe Çevirisi: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çüzüzüzüzüzüzüzüzüzüzüzüzüzüz
- Kaş-ağır yönlendiriciyi çiz: girişler (KV-cache olayları), algoritma (prefix-hash eşleşimi), bağlayıcı (GPU kullanımı).
  Çine dilinde: 図制缓存感知路由器:输入(KV 缓存事件) 算法(前哈希匹配)、决胜(GPU kullanım oranı)。
- LLM'ler için %32 DR başarısızlık sürücüsünü (kaybolan tokenizer dosyaları / kuantitasyon yapılandırmaları) isimlendirin ve üç dosya DR kontrol listesini belirtin.
  Çinçe Çevirimi: ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎
- Ticari bölge çapındaki sunuları (Bedrock CRI, GKE Multi-Cluster Gateway) KV-a karşı yönlendirme ile ayırt edin.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

## Sorunlar. Sorunlar.

> **【中文解读】**Çok Bölgelik LLM Servisinin üç temel sorunu: 1) Kaş depolama yolu 轮询 yük dengesi KV Cache  lokaliteyi bozuyor, bu da kaş depolama ortalama oranının %70'ten %8'e düşmesine neden oluyor; 2) DR 卫生32%'nin LLM DR başarısızlığı, takımın bir hesaba çekmesi veya bir biçimleme dosyası veya ölçümleme ayarını unutması nedeniyle olmuştur; 3) Veriler kalmak GDPR   EU kullanıcı verilerini AB'den ayrılmamayı gerektiriyor, kaş farkındalı yönlendirici, Paris kullanıcılarının isteklerini önceden uyumlandırmak için ABD-Doğu'ya yönlendirmeyi başarısız hale getiriyor.

> **【拓展：多区域推理的产业实践】**2026 yıllarında çok bölgelik LLM 部署sın en iyi uygulamaları şunları içerir: 1) Her bölge 独立的缓存知性路由器(vLLM Router / llm-d router),避免跨区域 KV 转移的高延迟(US-EU RTT 约75ms,US-APAC 约 220ms);(2) GORGO araştırması, net gecikmeyi yolların hedeflerinin belirgin projesi olarak 联合优化 prefill_time + network_latency;(3) Bedrock cross-region inference 和 GKE Multi-Cluster Gateway 处理可用性, but don't process TTFT you still need to apply layer cache-aware router;;

Hizmetiniz US-East-1, US-West-2 ve EU-West-1'de çalışmaktadır. Önüne bir ALB koyup, bir round-robin yapıyorsunuz.

> Suzlu hizmetler ABD Doğu-1, ABD Batı-2 ve Avrupa Batı-1'de yürütülüyor. Önceden ALB'yi bulundunuz.

Round-robin, devletsiz hizmetler için optimaldir. LLM sonucu tasarımı ile devletli  KV önbelleği modelin gördüğü her şeyi kodlar. Routing blind yanlış önbelleğe yönlendiriyor.

> 轮询负载均衡对无状态服务优优――LLM 推理自然是有状态的KV 缓存编码了模型看到的所有内容――盲路由就是路由到错误的缓存――

Özellikle, ekibiniz bir DR planı var. S3 bölgesel boyutlarına model ağırlıklarını yedekledin. Bölgesel kesintisi vurulur; başarısızlığa giriyorsunuz; replik başlatmayı reddediyor. Tokenizer.json, kuantitasyon yapılandırması ve RoPE ölçekleme yapılandırması senkronizasyon yapmadığınız ayrı bir kova içindeydi.

> 另一方面,你的团队有灾难恢复计划──你将模型权重跨区域备份到 S3──区域故障发生;你尝试故障转移;副本拒绝启动──你忘记tokenizer.json、量化配置和 RoPE 缩放配置在一个你没有同步的单独桶中──

Çoklu bölge LLM servisleri bir önbelleğe, bir yönlendirme sorunu ve DR-higiyen sorunu  yük dengeleme sorunu değil.

> Çok Bölgelik LLM  servis bir kayıp sorunu, bir yol sorunu ve bir felaket kurtarma sağlık sorunu değil bir yük dengeleyici sorunu.

## Konsepten bir şey.

### Önbelleğe bağlı yönlendirme

> **【中文解读】**Cache-aware 路由工作机制:请求到达后,路由器对前 (如前512 jeton)做哈希,查询每个副本"you是否有这个前缓存?"──副本通过pub/sub 频道发布 KV Cache 事件(分配/淘汰块),路由器维护前哈希→副本的索引──匹配到则路由到该副本,未匹配则按GPU利用率选择──vLLM Router(Rust 实现,2026 üretim-steck) destek O(1) 寻找,未匹配时回归至最小队列深度──

İstek bir istekle gelir. Router öntanımlıyı (örneğin ilk 512 jetonu) hash eder; her replikadan "bu öntanımlıyı önbelleğe kaydetmiş misiniz?" sorar. Replikler blokları tahsis ederken ve çıkarırken bir pub / alt kanalda KV-cache olaylarını yayınlar. Router replikayı eşleşme ile seçer, kimse yapmazsa GPU-util tabanlı bir bağ kırıcıya düşer.

> Lütfen ulaşılacak bir ipucu ile gelmek için yolcuyu gönderin. Bu da her bir başlıkta "Bu başlıklı depo var mı?" sorusunu verir.

**vLLM Router**(Rust, 2026 üretim aşaması):`kv.cache.block_added`O'll) 1 araması ile yollar. Hiç bir eşleşme olmadığı zaman en az sırada derinliklere düşer.

> **vLLM Router**(Rust,2026 üretim aşaması): 订阅 `kv.cache.block_added`事件,维护前哈希 → 副本索引,O(1) 查找路由──无匹配时回归最小队列深度──

**llm-d router**: aynı desen, Kubernetes-dev. ControlPlane API üzerinden etkinlikleri yayınlar.

> **llm-d router**Aynı model, Kubernetes Origins. ControlPlane API'si tarafından yayınlanmaktadır.

**SGLang RadixAttention**(Fase 17 · 06) içe benzerliktir.

> **SGLang RadixAttention**(Fase 17 · 06) is副本内等价物──跨副本路由严格在上游──

### Sayılar

> **【拓展：KV Cache 路由的性能数据】**Çok Bölge KV Cache 路由 性能差:2K-token 提示在 Llama 3.3 70B FP8 H100 上,cache hit(同副本、前常驻) TTFT ~80ms;cache miss( soğuk ön doldurma) TTFT ~800ms10x 差。 Eğer bir yolcu bir副本间 60 80% ′s ön depolama ortalama oranını gerçekleştirirse, N副本容量 altında tek bir副本 性能 ≠ bölge间 RTT de önemli faktördür:us-east-1 us-west-2 ~65ms、us-east-1  eu-west-1 ~75ms、us-east-1 us-southeast-1 ~220ms 跨区域路由只在远 网络中 延迟才时的价格──

TTFT P50 2K-token sorgulamasında, Llama 3.3 70B FP8, H100:
- Önbelleğe ulaşma (aynı kopya, önbellek sakin): ~80 ms.
- Kayıt kaybı (soğuk önceden doldurma): ~ 800 ms.

10x boşluk. Eğer yönlendiriciniz replikler arasında prefix cache'nin %60-80'ini vurursa, N-replik kapasitesinde tek replik performansını tahmini edersiniz. Eğer %10'u vurursa, saf bir ölçeklendirme yaparsınız.

> 2K-token 提示在 Llama 3.3 70B FP8 H100 上的 TTFT P50:缓存命中(同副本,前常驻) yaklaşık 80ms;缓存未命中(冷预填充) yaklaşık 800ms──10 倍差距── Eğer routeriniz副本间实现前缓存命中率 60-80%, N 副本容量下近似单副本性能── eğer sadece 10%,你近似朴素扩展──

### Bölge çapında yeni bir kısıtlama var  Ağ gecikmesi

Bölgelerarası RTT:
- US-East-1  US-West-2: ~65 ms.
- US-East-1  eu-West-1: ~ 75 ms.
- US-East-1  ap-southeast-1: ~ 220 ms.

Eğer yönlendirme bir istek için us-east-1'den bir sıcak önü işaretine alındığında, kaydedilen ön doldurma (800 → 80 ms) 440 ms geri dönüş yolculuğu ile küçültülür. GORGO (2026 araştırması) bunu açıkça  en aza indirir.`prefill_time + network_latency`Genellikle cevap, prefill'in üstün olduğu büyük çok MB önleme dışında bölgesel yönlendirmeyi sürdürmektir.

> Bölge间 RTT:us-east-1  us-west-2 约 65ms;us-east-1  eu-west-1 约 75ms;us-east-1  ap-southeast-1 约 220ms。 eğer yol yol yolundan US-east-1 发送到 ap-southeast-1 的热前,节省的预填充(800 → 80ms) 被 440ms 的往返延迟淹没──GORGO(2026年研究)明确指出联合优化`prefill_time + network_latency`Bu, genellikle yolların bölgeselleştirilmesini sağlamak için yapılır.

### Ticari "bölge çapındaki sonuçlar" burada yardımcı olmaz

AWS Bedrock bölgesel kesinti, kapasitede basınç sırasında diğer bölgelere gelen istekleri otomatik olarak yönlendirir. TTFT değil, kullanılabilirliği optimize eder ve kesintiyi açık olmayan bir şekilde ele alır. GKE Multi-Cluster Gateway aynı  hizmet düzeyinde başarısızlık, KV önbelleği farkında değildir.

> AWS Bedrock 跨区域推理在容量压力下自动将请求路由到其他区域──它优化可用性而不是TTFT,将推理视为不透明──GKE Multi-Cluster Gateway 也是如此服务级故障转移,不感知 KV 缓存──

Bu cihazları kullanırken bile bir uygulama katmanının önbelleğe hazırlanmış bir yönlendirmeye ihtiyacınız var. "US-East-1 yanıyor" durumunu ele alırlar.

> Bu ürünleri kullanırken bile, TTFT'yi işleme için bir aşama depolama sensörüne ihtiyacınız var.

### DR hijyen  %32'lik eksik dosya sorunu

> **【中文解读】**DR 卫生的三文件最低清单:(1) HF 模型仓库下的所有文件(权重 + 配置 + 分词器);(2) 引擎特定服务配置(vllm_config.yaml等);(3) 部署清单(K8s YAML、Dockerfile、依赖锁文件) ▽加上:

> **【拓展：LLM 灾难恢复最佳实践】**2026 yılında LLM DR'nin önemli uygulaması: 1) model ürünü tamlığı sadece ağırlıklı dosya değil, aynı zamanda tokenizer.json、quantize_config.json、RoPE 缩放配置、聊天模板; 2) 跨区域同步S3 model depolarına yönelik bölge çapındaki kopyalama, tüm bölgeleri tam bir副本ye sahip olmasını sağlamak; 3) otomatik DR 测试 Chaos Engineering kullanımı; 3) 17·24 aşaması; 4) RTO 目標 enterprise level LLM サービス genellikle RTO < 30 dakika ⋅

Çok sayıda alıntılanan 2026 statüsü: LLM DR başarısızlıklarının %32'si takımların ağırlıkları yedeklediği ama unuttuğu için gerçekleşir:

- `tokenizer.json`veya `tokenizer.model`
- Kvantitasyon yapılandırmaları (`quantize_config.json`, AWQ ölçekleri, GPTQ sıfır noktaları)
- Model-specifik yapılandırmalar (RoPE ölçeklendirme, dikkat maskeleri, sohbet şablonları)
- Motoru yapılandırma (`vllm_config.yaml`, örnekleme öntanımlıları, LoRA adaptör manifestoları)

> 2026 yılındaki yaygın olarak alıntılanan istatistik: LLM'nin %32'si başarısız oldu çünkü takımlar ağırlık kaydetmiş fakat unutmuşlardır:分词器文件、量化配置、模型特定配置、エンジン配置──

Düzeltme üç dosya minimum DR manifesti:

1. HF model repo (bozukluk + yapılandırma + tokenizer) altında bulunan tüm dosyalar.
2. Motor özel servis yapılandırması.
3. Deployment manifesti (K8s YAML, Dockerfile, bağımlılık kilitli).

> 修复方案是三文件最低 DR 清单:(1) HF 模型仓库下的所有文件(权重 + 配置 + 分词器);(2) 引擎特定服务配置;(3) 部署清单(K8s YAML、Dockerfile、依赖锁文件) ⋅

Ayrıca, JPMorgan'ın US-East 1 hareketi, sadece oyun kitabı prova edildiği için Kasım 2024'te 22 dakika geri kazanmış.

> Ayrıca: Her dönem DR 演练──JPMorgan 2024 yılının 11 月 US-East-1 演练 22 dakika geri kazanmaya ulaştı, çünkü önceden yapılan 演练──

### Veriler ortogonal olarak yerleşik

AB müşteri PHI AB'yi terk edemez. Eğer önbellek bağlantısı için Paris'ten gelen bir istek gönderirseniz, TTFT kazançına bakmaksızın GDPR'yi ihlal etmiş olursunuz.

> AB  müşteri PHI, AB'den ayrılamaz. Eğer depolama algılama yönlendiriciniz, Paris'ten gelen bir talebi ABD-Doğu'ya gönderirse, TTFT'nin nasıl kazancına bakılmaksızın, GDPR'yi ihlal etmiş olursunuz.

### Hatırlamalısın numaralar

- Kaş çarpması vs. kaçırılan TTFT boşluğu: ~ 10x (80 ms vs 800 ms 2K prompt üzerinde).
- Bölgelerarası RTT ABD-AB: ~75 ms.
- DR başarısızlığı: %32'si tokenizer/quant yapılandırmalarını kaçırıyor.
- JPMorgan us-east-1 başarısızlığı Kasım 2024: 22 dakika (30 dakika SLA).

## Çerçeveyi kullanın.
```figure
cache-aware-router
```

## Kullan

`code/main.py`bir çok bölge iş yükünde üç yönlendirme stratejisini (dolap robin, cache-ağır bölgesel, cache-ağır küresel) simüle eder.

> `code/main.py`Çok bölgelik iş yükü üzerinde üç yol stratejisi oluşturmak için:

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-multi-region-router.md`Bölgeler, ikamet kısıtlamaları ve SLA göz önüne alındığında, bir yol planı tasarlar.

> 本课产 出 `outputs/skill-multi-region-router.md`❖ belirli bölge ❖ SLA ve SLA, tasarım yolları ❖

## Egzersizler.

1. Çık .`code/main.py`75 ms RTT'ye göre, bölge arası yönlendirme sadece yerel yönlendirmeyi ne kadar hızlı bir şekilde geçirir?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ 75ms RTT'yi belirleyerek, hangi gösterge uzunluğunda bölge yolunun kendi yolundan daha iyi olması gerekir?
2. Önbellek trafiğin %70'den %12'e düştü.
   Çinçe Çevirisi: Senin beklenme oranı %70'den %12'e düştü.
3. VLLM'de hizmet veren 70B AWQ-quantized model için 5 LoRA adaptörü ile DR manifesti tasarlayın.
   Çinçe Çevirimi: VLLM için 5  LoRA 适配器 70B AWQ 量化模型设计 DR 清单──列出每个文件和配置──
4.    Çinçe Çevirisi:论证 Bedrock 跨区域推理对有严格 TTFT SLO 的金融科技公司是否足够──引用具体行为──
   ÇXMÜNÜFÜLÜŞÜN: ÇXMÜNÜFÜLÜŞÜN: ÇXMÜNÜFÜLÜŞÜN: ÇXMÜNÜFÜLÜŞÜN: ÇXMÜNÜFÜLÜŞÜN: ÇXMÜNÜFÜLÜŞÜN: ÇXMÜNÜFÜLÜN: ÇXMÜNÜFÜLÜN: ÇXMÜNÜFÜLÜN: ÇXMÜNÜFÜLÜN: ÇXMÜNÜFÜLÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇXMÜN: ÇÜN: ÇXMÜN: ÇÜN: ÇÜN: ÇÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜ
5. Paris'ten gelen bir talebimiz, Doğu 1'deki bir önbellekle eşleşir.
   Çin Çeviri: Bir Paris Kaynağı'nın Araması:

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Cache-aware routing | "smart LB" | Route on prefix-hash match to KV-cache-holding replica |
| KV-cache events | "cache pub-sub" | Replicas publish block add/evict; router indexes |
| Prefix hash | "cache key" | Hash of first N tokens used as router lookup |
| GORGO | "cross-region routing research" | arXiv 2602.11688; network latency as explicit term |
| Cross-region inference | "Bedrock CRI" | AWS product; availability failover, not TTFT awareness |
| DR manifest | "the backup list" | Every file needed to restore — not just weights |
| Data residency | "GDPR boundary" | Legal constraint on which region sees user data |
| RTT | "round-trip time" | Network latency; 75 ms US-EU, 220 ms US-APAC |
| LLM-aware LB | "cache-hit LB" | Cache-aware router as a product category |

## Daha fazla okumak

- [BentoML — Multi-cloud and cross-region inference](https://bentoml.com/llm/infrastructure-and-operations/multi-cloud-and-cross-region-inference)
- [arXiv — GORGO (2602.11688)](https://arxiv.org/html/2602.11688v1) Ağ gecikme süreci ile bölge çapındaki KV-cache yeniden kullanımı.
- [TianPan — Multi-Region LLM Serving Cache Locality](https://tianpan.co/blog/2026-04-17-multi-region-llm-serving-data-residency-routing)
- [AWS Bedrock Cross-Region Inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) Dosyaların kullanılabilirliği.
- [vLLM Production Stack Router](https://github.com/vllm-project/production-stack) Kaş-bilinen yönlendirme kaynağı.
