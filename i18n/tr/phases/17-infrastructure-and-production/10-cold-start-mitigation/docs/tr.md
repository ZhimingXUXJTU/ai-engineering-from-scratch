# Servissiz LLM için soğuk başlangıç azaltma .

> 20 GB model görüntüsü soğuktan servise gitmek için 5-10 dakika (7B) ile 20+ dakika (70B) sürer. Gerçek bir sunucu olmayan dünyada, bu bir                                                                                                                                                                                                                                                            Yumuşaklaştırmalar beş katman üzerinde çalışır: önceden ekilmiş düğüm görüntüleri (AWS'de Bottlerocket, iki hacimli ark), model akışı (NVIDIA Run:ai Model Streamer, vLLM'de doğuşcu), GPU bellek anlık çekme (Modal kontrol noktaları, 10 kat daha hızlı yeniden başlatma), sıcak havuzlar (`min_workers=1`Bu ders, beş katı ölçmeyi, bütçeyi ve yığmayı öğretir. Bu ders, beş katı ölçmeyi, bütçeyi ve yığmayı öğretir.

> **【中文解读】**Bu bölüm, LLM'nin ilk tepkisi için bir süreliğine gelmesi için kullanılan yöntemleri ele aldı.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cold-start path simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling)

>  **【前置】**Önemli bir ders: 17·02(platform ekonomi)  17·03 (GPU  genişletilir)  Serversiz LLM soğuk başlat = 5-20 分钟(热身 değil, is停服) 
>  **【类比】**soğuk başlatma缓解 = "汽车预热"。朴素加载 = 钥匙一从零启动(20 分钟);五层加速:(1) 预热节点镜像;(2) 模型流式加载;(3) GPU 内存快照(Modal 10 倍提速);(4) 暖池 min_workers=1;(5) 分层加载(ServerlessLLM NVMe→DRAM→HBM,10-200 倍延迟降低)。Modal实测 2-4 秒冷启动,Baseten 5-10 秒预热版亚秒)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- Soğuk başlangıç hafifletme sisteminin beş katmanını sıralayın ve her katman için bir araç veya model belirleyin.
  Çinçe Çevirimi: 列举冷启动缓解的五层策略,并说出每层一个工具或模式──
- 70B modelinde toplam soğuk başlangıç zamanı (nod sağlanması) + (koşul yükleme ağırlıkları) + (koşul yükleme ağırlıkları) + (motor başlangıcı) toplamı olarak hesaplayın.
  Çin dilinde tercüme:计算 70B 模型总冷启动时间 = 节点供给 + 权重下载 + 权重加载至HBM + 引擎初始化──
- Canlı göçün neden KV önbelleği değil girme jetonları (KB) aktardığını ve cezanın ne olduğunu (yağnadan hesaplama) açıklayın.
  Çinçe Çevirimi Çevirisi: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüzüz
- Sıcak havuz pazarlama oranını (sürük GPU için ödeme veya soğuk başlangıç kuyruk kabul) ve SLA eşiğini belirtin.`min_workers > 0`İhtiyaclı olur.
  Çinçe Çevirimi:                                                                                                                                                                                                                                                            `min_workers > 0`变为强制性的 SLA 值──

## Sorunlar. Sorunlar.

> **【中文解读】**Serversiz LLM 端点の冷起動問題:70B 模型 from零 to service needs 3-8 分钟(节点供应 45-60s + 容器拉取 120-300s + 权重载 45-120s + 引擎初始化 10-30s),远超2s  SLA── çözüm ise 热池保留(min_workers=1), ancak bu da 24/7 支付空 GPU 费用5 产品各保留 1 热副本,每月 3600 GPU-hours 无论有用户调.

> **【拓展：Serverless LLM 平台对比】**2026 yıl Serverless LLM 平台の冷起動表现:Modal 凭借 GPU 快照技术实现 2-4s冷启动(業界最快);Baseten 默认 5-10s,预加热后可低于 1s;AWS Lambda + 容器镜像通常10-30s(不含模型加载);GCP Cloud Run + GPU 较新,冷启动约15-30s──TTFT P99 < 60s 70B+ 模型 için,热池は強制性 60s内完成全流内任何冷启动优化能

Sunucusuz LLM son noktası gece içinde sıfıra yükselmiş.

> Senin Sunucusuz LLM 端点在夜间缩容容到零──早晨 8 点流量激增──第一个请求等:

1. Karpenter, GPU düğümünü 45-60s'a kadar sağlıyor.
   Çeviri:Karpenter 供给GPU 节点:45-60 秒──
2. Kontener, ağırlıkları olan 30 GB görüntü çekir: 120-300s.
   Çinçe Çevirimi:容器拉取 30GB'nin içeriği: 120-300 saniye
3. Motorun ağırlıkları HBM'ye yüklenmesi: model boyutuna ve depolama hızına bağlı olarak 45-120s.
   Çin dilinde: Motoru HBM:45-120 saniyeye kadar yüklenecek, model büyüklüğüne ve depolama hızına bağlı olarak.
4. vLLM veya TRT-LLM CUDA grafiklerini initializer, KV önbelleği havuzu, tokenizer: 10-30s.
   中文翻译:vLLM 或 TRT-LLM 初始化 CUDA grafik、KV 缓存池、分词器:10-30 秒──

Toplam: 220-510s (yaklaşık 3-8 dakika) bir token geri gelmeden önce. SLA 2s.`min_workers=1`Bu yüzden, bu işlemler, bir kullanıcı tarafından yapılan veya yapılmayan bir işlem için kullanılır.

> Bir token geri dönmek için toplam sayı:220-510 saniye...`min_workers=1`Sorun kaybolmuş gibi görünüyor, ama şimdi 24 saatlik bir boş GPU ödemesi için çalışıyorsun. Eğer hizmetin her birinden 5 ürün varsa, 5 × 24 × 30 = 3.600 GPU-saati / ay, kullanıcıların kullanımı ne olursa olsun.

Soğuk başlangıç hafiflemesi, her zaman aktif olanların gecikmesini yaklaşırken sunucusuz ekonomisini nasıl koruyacağımızdır.

> Sıcak başlatma hafiflemesi, hizmetsiz ekonomide kalmak ve sürekli hizmetin geçmesini yaklaştırmakla beraberdir.

## Konsepten bir şey.

### Katman 1  önceden tohumlanmış düğüm görüntüleri (Bottlerocket)

> **【中文解读】**İlk katı 预播种节点镜像──AWS Bottlerocket'in iki tomlu yapı, işletim sistemi ile veri ayrımı──将容器镜像(含模型权重) 预到数据卷快照中,在 `EC2NodeClass`Yeni bir nodun başlatılması sırasında, yeni bir nodun yüklenmesi, büyük bir model için 2-4 dakikalık tasarruf için kendi kendine tanımlanmış bir VM 鏡像模式ı olan Azure'da bulunmaktadır.

AWS'de Bottlerocket'ın iki hacmelik mimarisi işletim sistemini verilerden ayırır.`EC2NodeClass`Yeni düğümler yerel NVMe'de ağırlıklarla başlatılır  adım 2 ve 3'ün bir kısmı ortadan kaybolur. Karpenter ile doğuştan çalışır. Tipik tasarruf: büyük modeller için soğuk başlangıç başına 2-4 dakika.

> AWS'de, Bottlerocket'in iki tomlu yapı, işletim sistemi ile veriyi ayırır.`EC2NodeClass`Yeni bölüm başlatma sırasında ağırlıklılık yerel NVMe 上步骤 2 和部分步骤 3 消除──原生与Karpenter 配合──典型节省:大型模型每次冷启动 2-4 分钟──

GCP'de eşdeğer: önceden pişirilmiş konteyner katmanları ile özel VM görüntüleri. Azure'da: aynı desenle yönetilen disk anlık görüntüleri.

> GCP 等价方案:预容器层的自定义 VM 镜像──Azure:托管磁盘快照加相同模式──

### Katman 2  model akışı (Run:ai Model Streamer)

> **【中文解读】**İkinci katı 模型流式加载──NVIDIA Run:ai Model Streamer 没有需要等等整个文件加载完才开始服务,而是将权重逐层流式加载到 GPU 内存,并将权重逐层流式加载到 GPU内存,并将第一变压器块加载完成后就开始处理──2026年 vLLM 原生支持此功能──兼容 S3、GCS 和本地 NVMe──通过重叠 I/O 和计算设置,可将大型模型的权重加载时间减半──

İlk talebi cevaplamadan önce tüm dosyayı yüklemek yerine, GPU bellek tabakasından tabakaya akış ağırlıklarını akışlatın ve ilk transformatör bloğu oturan olduğu anda işlem yapmaya başlayın. NVIDIA Run:ai Model Streamer vLLM 2026'da doğuştan gönderir. S3, GCS ve yerel NVMe ile çalışır.

> İlk istekle cevap vermek için, önce tüm dosyaları yüklemek gerekir, ancak önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce önce

### Katman 3  GPU hafıza anlık görüntüleri (Modal)

> **【中文解读】**Üçüncü katı GPU 内存快照──Modal  GPU  durumu için ilk yüklenmeden sonra(权重、CUDA grafik、KV Cache 区域) kontrol noktası yapın, 后续重启直反序列化至HBM比重启动快10x── bu "2 saniye 热启动 GPU" en yakın teknoloji──代价是快照与 GPU 拓绑定 Eğer Karpenter farklı SKU'ya taşınırsa, yeniden üretmek gerekir 快照──

> **【拓展：冷启动优化策略叠加】**五层冷启动缓解可叠加使用:(1) 预播种镜像(消除镜像拉取) + (2) 模型流式加载(减重重重重荷时间) + (3) GPU 快照(消除重重重荷) + (4) 热池(避免冷启动) + (5) 分层加载(NVMe→DRAM→HBM) ――全叠加将 70B 模型从 328s 冷启动降至约15s22x 改善。选择哪几层取决于SLA 严格程度和预算。

Modal, ilk yüklenmeden sonra GPU durumunun kontrol noktasını (koşmalar, CUDA grafikleri, KV önbelleği bölgesi) alır. Sonrasında yeniden başlatılan HBM  10x daha hızlı olarak doğrudan deserialize olur. Bu "sıcak bir GPU'yu 2 saniye içinde başlatmak" için en yakın şeydir.

> Modal ilk yüklenmesinden sonra GPU  durumu için kontrol noktası yapılır. HBM  reboot  reboot                                                                                                                                                                                                                                                 

### Katman 4  sıcak havuzlar (min_workers=1)

> **【拓展：Serverless LLM 平台的冷启动对比】**2026 yıl Serverless LLM 平台の冷启动表现:Modal 以 GPU 快照技术实现 2-4s(業界最快);Baseten 默认 5-10s,预加热后 <1s;AWS Lambda + 容器镜像通常10-30s(不含模型加载);原始 70B 模型冷启动 3-8 分钟。Modal 快照技术的关键差它将 GPU 状态(权重 + CUDA graph + KV Cache 区域)序列化,重启时直接反序列化至HBM,重启动快 10x。代价是快照与 GPU 拓绑定,迁移至不同 SKU 需要重制快照──

En basit hafifleme: her zaman bir kopya hazır tutun.$0.85-$1.50/saat 30s soğuk başlangıçtan kaçınmak için) ve büyük olanlara karşı kibar (5 dakikalık soğuk başlangıçtan kaçınmak için 4 $ / saat ödeyin).

> En basit çözüm: bir kopya tutmak için her zaman hazırlıklı olmalısın.$0.85-$1.50/小时以避免30秒冷启动),大模型则相对友好(付 $4/小时以避免5分冷启动) ・・・热池变为强制性SLA 值:通常是70B+ 模型上 TTFT P99 < 60 秒──

### Katman 5  Katmanlı yükleme (ServerlessLLM)

ServerlessLLM depolama bir hiyerarşi olarak değerlendiriyor: NVMe (hızlı ama büyük), DRAM (ortaya ancak katlı), HBM (küçük ama anlık). Ağırlıklar önceden DRAM'a yüklenir; talep üzerine yükleme HBM'ye. Kağıt soğuk yüklerde naif disk-HBM'ye karşı 10-200x gecikme azaltımı rapor ediyor. Üretim kabulü erken ama vLLM ile entegrasyonlar var.

> ServerlessLLM depolama görevi olarak seviyesine göre:NVMe(快但大)、DRAM(中等但分层)、HBM(小但即时)。权重预加载到DRAM;按需加载到HBM。论文报告冷启动延迟降低 10-200倍──生产采用早,但已存在与vLLM的集成──

### Katman 6  canlı göç (bonus modeli)

Bir düğüm bulunmadığında (spot eviction, node drain), geleneksel bir örnektir soğuk başlatma ve başka bir kopya ve dren talep kuyruk. Canlı göç giriş jetonlarını (kilobit) model yüklenmiş bir hedefe taşıyor ve KV önbelleğini hedefte yeniden hesaplar. Yeniden hesaplama, ağ üzerinden GB KV önbelleğini aktarmaktan daha ucuz.

> Zamanlı olarak, bir diğer bir başvuru başlatmak için bir diğer başvuru başlatmak için kullanılan bir modudur. Bu modü, yüklü bir modelin hedef noktalarına taşınmak için kullanılır.

### Sıcak havuz matematikleri

> **【中文解读】**热池数学: P99 TTFT SLA 为 2s 的服务,问题不是"热池是/no"而是"多少热副本、哪些路径需要"──高价值交互路径(实时聊天、语音代理)→ min_workers=1-2;后台批处理路径(夜间分类)→ ölçek-to-zero 可接受;高级层级 → 按租户专用热副本。简单算术:5 个产品各 1 热副本 = 5 × 24 × 30 = 3600 GPU-hours/月,无论有用户调用是否──

P99 TTFT SLA'sı 2s'li bir servis için, soru "sıcak havuz evet/hayır" değil "ne kadar sıcak kopya ve hangi yollar onları alır".

> P99 TTFT SLA için 2 saniyelik servis, sorunun "热池 evet/hayır" değil, "ne kadar热副本, hangi yollar onları gerektirir" olmasıdır.

- Yüksek değerli etkileşim yolları (canlı sohbet, sesli ajan): `min_workers=1-2`- Evet .
  Çinçe Çevirimi:高价值交互路径 (高价值交互路径)`min_workers=1-2`- Evet.
- Arka planlı parti yolları (gece sınıflandırması): ölçekle sıfır arasında kabul edilir, 5-10 dakika soğuk başlangıç kabul edilebilir.
  Çinçe Çevirimi: 后台批处理路径 (natt间分类): 接受缩容到零,5-10 分钟冷启动可容忍──
- Premium seviye: `min_workers`Özel kapasiteye sahip kiracı başına.
  Çeviri: Yüksek seviye:`min_workers`专用容量──

### Optimize edilmeden önce ölçme

> **【中文解读】**70B 模型冷启动解剖(示意数据):节点供应50s + 镜像拉取180s + 权重至HBM 75s + 引擎初始化20s + 首次前向3s = 总计 328s。全缓解后:预播种消除镜像拉取、模型流式加载减半权重加载、GPU 快照消除重复初始化 = 约15s 总冷启动(22x 降低)。

70B modeli için taze bir düğüm üzerinde soğuk başlangıç anatomisi (önergeci):

| Phase | Time | Mitigation |
|-------|------|-----------|
| Node provision | 50s | Bottlerocket + pre-seeded image, warm pool |
| Image pull | 180s | Pre-seeded data volume (eliminate) |
| Weights to HBM | 75s | Model streamer (halve); GPU snapshot (eliminate) |
| Engine init | 20s | Persistent CUDA graph cache |
| First forward | 3s | Min inherent latency |
| **Total cold** | **328s** | |
| **Total with mitigations** | **~15s** | 22x reduction |

### Hatırlamalısın numaralar

- Modal soğuk başlangıç: 2-4 saniye (GPU çabuk çekimleri ile).
  Modal soğuk başlatma:2-4 saniye
- Baseten standart soğuk başlangıç: 5-10 saniye; ön ısınma ile alt saniye.
  Çeviri: Baseten 默认冷启动:5-10 秒;预加热后亚秒级。
- Çiğ 70B soğuk başlangıç: 3-8 dakika.
  Çin Çeviri: 原始 70B 冷启动:3-8 分钟──
- Run:ai Model Streamer: ~ 2x ağırlık yük hızlandırması.
  Çeviri:ai Model Streamer: yaklaşık 2 倍权重加载加速。
- ServersizLLM katlı yükleme: 10-200 kat daha az gecikme (kağıt sayıları).
  Çinçe Çevirim:ServerlessLLM 分层加载:10-200 倍延迟降低(论文数据)

## Çerçeveyi kullanın.
```figure
cold-start-pipeline
```

## Kullan

`code/main.py`Her bir hafifleme ile ve olmadan soğuk başlangıç yolunu modellemektedir.

> `code/main.py`建模有/无每种缓解的冷启动路径――报告总冷启动时间、热池成本和热池自付自给自付的亏平衡请求率──

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-cold-start-planner.md`SLA, model boyutu ve trafik şekli göz önüne alındığında, hangi hafiflemeleri toplayacağını seçer.

> 本课产 出 `outputs/skill-cold-start-planner.md`❖ SLA ❖ model büyüklüğü ve akım biçimi, hangi hafifleme stratejileri seçmek ❖

## Egzersizler.

1. Çık .`code/main.py`SLO'da ek talep düşüşleri ile soğuk başlangıç vergisini ödemekten daha ucuz olan bir sıcak kopyasının karşılığı olarak, eşitlik oranını hesaplayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ hesaplı ⇒ SLO ⇒ Ücretsiz talep ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ SLO ⇒ S
2. 3s'lik P99 TTFT SLA ile 13B modelini kullanın.
   Çinçe Çevirim: 你部署一个13B模型,P99 TTFT SLA 为 3 秒──选择实现它的最小缓解(最少层级)──
3. Bottlerocket öncesi çekim görüntü çekimi ortadan kaldırır, ancak ağırlıklar hala anlık hbm'den yüklenir. Anlık hbm'nin 7 GB/s'de okunması durumunda 70B modeli için duvar saati hesaplayın.
   Çinçe çevirisi:Bottlerocket 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播种 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播时 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 预播 
4. Sunucusuz sağlayıcı GPU anında görüntüler sunuyor (Modal) ve ekibiniz "anında görüntüler PII sızdırıyor" diye reddediyor.
   Çin dilinde:Your Service Provider provides GPU 快照(Modal), ancak ekip "快照泄露 PII" nedeniyle reddetti.
5. Bir katlı sıcak havuz politikası tasarlayın: ücretli kullanıcılar, deneme kullanıcıları ve seri iş yükleri için kaç sıcak kopya? Matematik gösterin.
   Çinçe Çevirimi: design分层热池策略:付费用户、试用用户和批处理工作负载各多少热副本?展示计算──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Cold start | "the big pause" | Time from request to first token on a fresh replica |
| Warm pool | "always-on minimum" | `min_workers >= 1` to keep at least one replica ready |
| Pre-seeded image | "baked AMI" | Node image with container weights pre-resident |
| Bottlerocket | "AWS node OS" | AWS container-optimized OS with dual-volume snapshot support |
| Model streamer | "streaming load" | Overlap weights I/O with compute setup |
| GPU snapshot | "checkpoint to HBM" | Serialize post-load GPU state; deserialize on restart |
| Tiered loading | "NVMe + DRAM + HBM" | Hierarchy of storage tiers; load on demand |
| Live migration | "move tokens" | Transfer input (KB), recompute KV on destination |
| `min_workers` | "warm replicas" | Serverless minimum keep-alive count |
| Scale-to-zero | "full serverless" | No cost when idle; accept full cold-start tax |

## Daha fazla okumak

- [Modal — Cold start performance](https://modal.com/docs/guide/cold-start) Modal'ın yayınladığı referans değerleri ve kontrol nokta mimarisi.
- [AWS Bottlerocket](https://github.com/bottlerocket-os/bottlerocket) Önceden ekilen veri hacmi anında görüntüsü örneği.
- [NVIDIA Run:ai Model Streamer](https://github.com/run-ai/runai-model-streamer) hesaplama ayarıyla birlikte örtüşen ağırlıklar yüklenir.
- [Baseten — Cold-start mitigation](https://www.baseten.co/blog/cold-start-mitigation/)                                                                                                                                                                                                                                                              
- [ServerlessLLM paper (USENIX OSDI'24)](https://www.usenix.org/conference/osdi24/presentation/fu) Dört katlı yükleme tasarımı.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) ayrıntılı yerleştirmeler için canlı göç.
