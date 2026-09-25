# Shadow Traffic, Canary Rollout ve LLM için Gelişmiş Deployment

> LLM dağıtımları, yazılım dağıtımının en zor bölümlerini birleştirir: birim testleri yoktur, dağılmamış başarısızlık modları, gecikmiş sinyaller. Düzeni (1) gölge modudur  aday modeline çift pro pro talepleri, kayıt, sıfır kullanıcı etkisi ile karşılaştırın; açık dağılım sorunlarını yakalar ancak kalite garantisi değildir; (2) Kanarya dağıtım  ilerici trafik değişimi 10% → 25% → 50% → 75% → 100% her adımda kapılar ile; izleme gecikme yüzdeleri, maliyet / taleb, hata / reddetme oranı, çıkış uzunluğu dağılım, kullanıcı geri bildirim oranı; (3) istikrarı onayladıktan sonra farklı alternatifler için A / B testleri. Deterinizm olmayan  %15'e kadar kesinlik değişimi aynı girişlerle çalışmalar arasında GPU FP'nin ilişkili olmaması ve parti boyutları değişimi nedeniyle azaltılamaz. Masraf değişken, sabit değil  %20 daha iyi bir model her çağrı için 3 kat daha pahalı olabilir. Çıkarım hızı belirleyici: Çıkarım yeniden dağıtım gerektirirse, çok yavaşsınız. Politika konfig/bandarlarda yaşar; model kayıtta sabitlenmiş dijeslerle yaşar; rollback = flip politika + geri dönüş eşiği + saniye içinde eski modelin pinini.

> **【中文解读】**Bu bölümde Shadow / Kinsheyr / Graduous Mekanı LLM  Service Security on-line'nin deployment stratejisi anlatılıyor.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy canary-progression simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing)

>  **【前置】**Önemli bir program oluşturmak için en zor olan bir program oluşturmak için, bu programın en zor bir programı oluşturmak için en zor bir program oluşturmak için en zor olan programdır.
>  **【类比】**LLM 部署三步 = "飞机首飞流程"。 Shadow = 地面模拟(复制 prod 请求,零用户影响,对比但不切换);Canary = 真飞但逐步开载客(10%→25%→50%→100%→100%;A/B = 商务航班对比(稳定测不同方案)。关键后:非确定性不可消除(GPU 浮点+batch 差异致 15% 准确率波动);成本是变量(好20% 的模型可能贵3倍);回滚速度决定性(秒级旗 切换不可重新部署)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- Gölge modunu (sıfır etki karşılaştırması), kanary (canal trafik ilerleyici) ve A/B (sağlık doğrulanmış karşılaştırma) ayırt edin.
  Çinçe çevirisi:区分影子模式 (区分影子模式) 零影响比较) 金丝雀 (真流量渐进)  A/B (统计比较) ⋅
- LLM'ye özel beş kanarya ölçüsünü (kenaklık, maliyet/ talep, hata/ reddedilme, çıkış uzunluğu dağılım, kullanıcı yanıtları) listeleyin.
  Çinçe Çevirimi:列举五个 LLM 特定金丝雀指标(延迟、成本/请求、错误/拒绝、输出长度分布、语义质量样本)
- LLM belirlenme yetkisi (% 15'e kadar) neden bir dağıtımda "sağlık" anlamına gelen şeyi değiştirdiğini açıklayın.
  Çinçe Çevirimi: LLM'nin neden belirsiz olduğunu açıklayın.
- Sekünteler (politik dönüşü) değil saatler (değişiklik) alan bir geri dönüş yolu tasarlayın.
  Çinçe Çevirim: Design a second级回滚路径 (öncü kelime)

## Sorunlar. Sorunlar.

> **【中文解读】**LLM'nin dağıtımında yazılım dağıtımının en zor kısmı: hiç bir birim test edilmemesi, belirsiz başarısızlık modeli, gecikme sinyalleri bulunmaktadır. Doğru sırası şunlardır: 1) 影模式 üretim talebini aday modeline, 日志 karşılığı, sıfır kullanıcı etkisiyle kopyalayacaktır; 2) 金丝雀 yayın 10%→25%→50%→75%→100% 渐进流量切换, her aşamada bir kontrol göstergesi vardır; 3) A/B 测试稳定性确认后的比比比──回滚速度是决定性的策略标志翻转(30秒)vs 重部署(3 小时)

> **【拓展：LLM 非确定性与部署】**LLM'nin belirsizlikleri belirsizdir. Aynı giriş aynı modelde %15'e kadar doğruluk oranı farkı oluşturabilir. Bu nedenle, LLM'de "sağlamlık" "önemli kesimlerde" anlamına gelir.

Yeni bir model gönderiyorsunuz. Offline değerlendirmeler %3 doğruluk artışını gösterir. Üretimde geri çevirirsiniz. 24 saat içinde, maliyet %40 arttı, kullanıcı parmakları%8 arttı, üç müşteri biletinin "acayip cevaplar" raporunu. Geri dönersiniz. Yeniden dağıtmak 3 saat alır. Hafta sonu mahvoldu.

Bu durumun her parçası önlenebilirdi. Gölge modunda herhangi bir kullanıcı bunu görmeden önce maliyet artışının %40'ını yakalamış olacaktı. Canary, parmak parmakları aşağı hareket ederken %10'da durmuş olacaktı. Politika bayrağı geri çekilmesi 30 saniye sürmüş olacaktı. Disiplin "offline değerlendirmeler iyi görünüyor" ve "gerçek kullanıcılar mutlu" arasındaki boşluğu dolduruyor.

## Konsepten bir şey.

### Gölge modusu

> **【中文解读】**影模式候选模型接收与生产相同的请求,输出仅记录不回归用户――日志内容包括:输出内容(与生产不同)、代码数量(成本差)、延迟、拒绝和错误――能捕获:成本爆炸、长度退化、明显拒绝变化、硬错――不能捕获:用户会感知到质差影子是烟雾测试,不是质量测试――

İsteğe giren isteği üretim ile aynı şekilde alır; çıkışlar kayıtlıdır, kullanıcılara geri verilmez. Kullanıcı etkisi sıfır.

- Üretim içeriği (ürünme karşı fark).
- Token sayıları (maliyet delta).
- Gecikme.
- İtiraz ve hata.

Yaptıkları: maliyet uçuşları, uzunluk gerilemeleri, açıkça reddedilen değişiklikler, sert hatalar. Yaptıkları: kalite delta kullanıcıları algılar. Gölge bir duman testi, kalite testi değil.

### Kanaryaların dağıtımı

> **【拓展：LLM 金丝雀发布的五个门控指标】**LLM 金丝雀 yayınlaması kontrol edilmesi gereken beş kontrol göstergesi:(1) 延迟百分位(P50/P95/P99) kanary P99 > 1.5x 基线则触发;(2) her talep maliyeti>20% 高于基线则触发;(3) 错误/拒绝率2x 基线则触发;(4) 输出长度分布均值 + P99 分布偏移值则触发;(5) 用户反率指下/工单 1.5x 基线则触发;;典型进度 1%→10%→25%→50%→75%→100%;

Gelişen trafik geçişleri. Tipik ilerleme: 1% → 10% → 25% → 50% → 75% → 100%.

1. **Latency percentiles** P50, P95, P99.
2. **Cost per request** karışık $. ihlal: başlangıç seviyesinden %20'lik.
3. **Error / refusal rate**5xx artı açık bir reddedilme.
4. **Output length distribution** ortalama + P99.
5. **User-feedback rate**- Başparmak aşağı / bilet kayıtları.

### Devrimsizlik yeni bir değişimdir.

Aynı girişler aynı çıkışları üretmez.

- GPU FP ilişkisizliği (yürüyüş noktası azaltma sırası partiye göre değişir).
- Satır boyutları değişimi (128 vs. 16 satır)
- Örnekleme (temperatür > 0).

Ölçülmüş: aynı değerleme setlerinde çalıştırılan %15'e kadar doğruluk değişikliği. "Stabil" bir dağıtımda ölçümler beklenen değişiklik içinde, başlangıç çizgisine benzer değildir.

### Masraf değişken

%20 daha iyi bir model her çağrıda 3 kat daha pahalı olabilir. Masraf / talep beş kapıdan biridir. Birim ekonomisini kıran "en iyi" bir model göndermek bir geri dönüş durumudur.

### Rollback silah.

- Politika bayrağı (önümlü bayrağı sistemi): yapılandırmalarda dönüş yüzdesi; saniyeler alır.
- Model sıkıştırılması (registri sindirme): sıkıştırılmış model otomatik olarak yükseltilmez.
- Geri dönüş = bayrak + öncekiye sabitlenmiş bir dizgest ayarlayın.

Eğer yığın yeniden dağıtılmak için geri dönüş gerektiriyorsa, fırlatmadan önce düzeltin.

### Araçlama

> **【拓展：LLM 渐进式部署工具链】**2026 yılında LLM 渐进式部署的工具选择:(1) Argo Rollouts / FlaggerKubernetes 原生渐进式部署控制器,与 Istio/Linkerd 加权路由集成;(2) Istio ağır yönlendirme服务网格级流量切分;(3) KServe / Seldon Core模型服务自带卡纳里功能;(4) Özellik bayraklarıLaunchDarkly、Flagsmith、Unleash,策略级翻转无需重新部署──回滚基础设施:策略标志标志(Flag mark system)翻转百分比在配置中秒级) 模型注册摘要固定pinged digest 不自动升级)  Eğer sizin堆重新部署回滚,(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

**Argo Rollouts**- Ne ?**Flagger** Kubernetes ilerici teslimat kontrolörleri. Istio/Linkerd ağırlıksız yönlendirme ile entegre.

**Istio weighted routing** hizmet ağı seviyesindeki trafik bölümü.

**KServe / Seldon Core** İçerilen kanaryalı servisi.

**Feature flags** LançDarkly, Flagsmith, Unleash.

### Metrikler kadansı

Kanarlı kapılar trafik hacmine bağlı olarak her 5-15 dakikada bir kontrol eder. %1 trafiğin 10 req/min ile penceresi başına 50-150 veri noktası verir  gecikme için yeterli ama kullanıcı geri bildirimleri için gürültülü. %10 ~ 10 kat daha fazla verir.

### A/B adımı seçeneğe bağlıdır.

Yeni model belirgin bir şekilde farklı ise (farklı davranış, farklı maliyet eğri, farklı ton), kanary geçtikten sonra %50'de A/B testini yapın.

### Hatırlamalısın numaralar

- Kanarya ilerleme: 1% → 10% → 25% → 50% → 75% → 100%.
- Determinizm sınırlaması: Aynı girişlerde %15'e kadar devamlı değişim.
- Beş kanarya ölçüsü: gecikme, maliyet, hata/reddedilme, çıkış uzunluğu, kullanıcı geri bildirimi.
- Masraf kapısı: >20%'den fazla baseline karşı bir ihlal.
- Sekünteler, saatler değil.

## Çerçeveyi kullanın.
```figure
i4-canary-ramp
```

## Kullan

`code/main.py`İndirilen geri dönüşlerle bir kanarya yayımını simüle eder. Yayınlama durakları ve hangi kapı tetiklendiği raporları.

> `code/main.py`İndirilen geri dönüşlerle bir kanarya yayımını simüle eder. Yayınlama durakları ve hangi kapı tetiklendiği raporları.

> `code/main.py`İndirilen geri dönüşlerle bir kanarya yayımını simüle eder. Yayınlama durakları ve hangi kapı tetiklendiği raporları.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-rollout-runbook.md`. Başvuru modeli, başlangıç çizgisi ve risk toleransı göz önüne alındığında, shadow→canary→100% planı tasarlıyor.

> 本课产 出 `outputs/skill-rollout-runbook.md`. Başvuru modeli, başlangıç çizgisi ve risk toleransı göz önüne alındığında, shadow→canary→100% planı tasarlıyor.

## Egzersizler.

1. Çık .`code/main.py`- %25 maliyet geri dönüşü enjekte edin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`%25'i içiyor. Hangi aşamada yakaladınız?
2. Yeni modeliniz %3 doğruluk kazancı offline ama maliyet / talep %18'dir.
   Çinçe Çevirimiçi: Yeni modeliniz %3 oranında daha iyi bir şekilde çevrimiçi hale geldi.
3. 60 saniyeden kısa bir geri dönüş yapın.
   Çine Çeviri: Design End to End 60 saniye içinde dönmek.
4. - Değerlendirme eksikliği %7'e ulaştı.
   Çinçe Çevirimi: belirsizlik gösterir +/-7%── ayarlama
5. Gölge modunda, kanaryalardan önce maliyet artışı %40'a ulaşır.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Shadow mode | "duplicate to new" | Zero-impact send-to-candidate for logging |
| Canary | "progressive traffic" | Gradual user-exposed rollout with gates |
| Gates | "rollout checks" | Metric thresholds that block progression |
| Non-determinism | "LLM variance" | Irreducible run-to-run differences |
| Policy flag | "flag flip rollback" | Config-level rollback, seconds not hours |
| Model pin | "registry digest" | Immutable reference to a model version |
| Argo Rollouts | "K8s progressive" | Kubernetes-native canary/rollback controller |
| KServe | "inference K8s" | Model serving with canary primitives |
| Istio weighted | "mesh split" | Service-mesh traffic splitter |

## Daha fazla okumak

- [TianPan — Releasing AI Features Without Breaking Production](https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing)
- [MarkTechPost — Safely Deploying ML Models](https://www.marktechpost.com/2026/03/21/safely-deploying-ml-models-to-production-four-controlled-strategies-a-b-canary-interleaved-shadow-testing/)
- [APXML — Advanced LLM Deployment Patterns](https://apxml.com/courses/mlops-for-large-models-llmops/chapter-4-llm-deployment-serving-optimization/advanced-llm-deployment-patterns)
- [Argo Rollouts docs](https://argo-rollouts.readthedocs.io/)
- [Flagger docs](https://docs.flagger.app/)
