# LLM Gözlem Güçlülik Satır Seçimi .

> 2026 gözlemlenebilirlik pazarı iki kategoriye ayrılır. Gelişim platformları (LangSmith, Langfuse, Comet Opik) değerlendirmeler, hızlı yönetim, seans tekrarlamalarıyla birlikte izlemeyi birleştirir. Gateway/instrumentasyon araçları (Helicone, SigNoz, OpenLLMetry, Phoenix) telemetri üzerine odaklanmaktadır. Langfuse, güçlü OSS dengesi (50K etkinlik / ay ücretsiz bulut) ile MIT lisanslı bir çekirdektir. Phoenix, Elastic License 2.0 altında OpenTelemetry- doğuşlu, sürükleme / RAG görselleştirme için mükemmel, sürekli bir üretim arka planı değil. Arize AX, monolit gözlemsellikten 100 kat daha ucuz olduğunu iddia eden sıfır kopyalı Iceberg/Parquet entegrasyonunu kullanıyor. LangSmith, LangChain/LangGraph için liderlik ediyor, 39 $ / user / mo, sadece Enterprise'da kendi kendine barındırıyor. Helicone 15-30 dakikalık ayarlama ile proxy tabanlı, 100K req/mo ücretsiz, ama ajan izleri daha az derinlik. Ortak üretim tarzı: Gateway (Helicone/Portkey) + eval platformu (Phoenix/TruLens) OpenTelemetry ile yapıştırılmış.

> **【中文解读】**Bu bölümde LLM'nin gözlemlenebilirliği hakkında bilgi edinilir.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy trace-sampling simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 08 (Inference Metrics), Phase 14 (Agent Engineering) | **前置知识:** Phase 17 · 08 (Inference Metrics), Phase 14 (Agent Engineering)

>  **【前置】**Önemli bir ders: 17·08(推理指标) 、14(Agent 工程) ◦LLM 可观测性
>  **【类比】**可观测性工具 = "AI 应用的体检设备"――开发平台(LangSmith/Langfuse/Phoenix) = 全身体检(含评估、即时管理、会话回放);Gateway(Helicone/Portkey) = 心率手环(轻量代理、15-30 分钟部署)。Langfuse 开源 50K 事件/月免费;LangSmith 在 LangChain 生态领先 $39 /用户/月;Helicone 100K 请求/月免费;;生产典型组合:Gateway + 评估平台 + OpenTelemetry 水──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- Gelişme platformlarını (bundled: evals + prompt + sessions) gateway/telemetry araçlarından (sadece izler + metrikler) ayırt edin.
  Çinçe Çevirimiçi:区分开发平台 (Bundert:评估 + 提示管理 + 会话)
- Altı ana aletin (Langfuse, LangSmith, Phoenix, Arize AX, Helicone, Opik) lisanslama, fiyatlandırma ve tatlı nokta kullanım durumlarına haritasını yapın.
  Çinli dilde:将六个主要工具 (将六个主要工具)  Langfuse、 LangSmith、Phoenix、Arize AX、Helicone、Opik) 映射到其许可、定价和最佳用例──
- Bir geçit aracı ile ayrı bir değerleme platformu birleştirmenizi sağlayan OpenTelemetry-kalem örneğini açıklayın.
  Çinçe Çevirimiçi: açıklama OpenTelemetry 水模式, bu model, internet bağlantısı araçlarını bağımsız değerlendirme platformuyla birleştirmenize izin verir.
- 2026 maliyet farkçısını (Arize AX'in sıfır kopya yaklaşımı vs. monolit alımı) isimlendirin ve kaba 100x katlayıcısını belirtin.
  Çinçe çevirisi:                                                                                                                                                                                                                                                            

## Sorunlar. Sorunlar.

> **【中文解读】**LLM 可观测性工具分为两类:(1) 开发平台(LangSmith、Langfuse、Opik) 捆绑监控、评估、提示管理、会话回放;(2) 网关/遥测工具(Helicone、SigNoz、OpenLLMetry、Phoenix) 专注于遥测采集──选择涉及四个维度:技术(LangChain?原始 SDK、?) 需求许可证(MIT sadece?商业可接受?)、预算、自托管──

> **【拓展：LLM 可观测性市场格局】**2026 yıl LLM 可观测性市场的关键玩家:(1) Langfuse(MIT 开源,50K etkinlikler/ay 免费云)LangSmith 级功能但可自托管;(2) LangSmith(商业,$39/user/month)LangChain 生态最佳;(3) Phoenix(Elastic License 2.0) RAG/漂移可观化优秀;(4) Arize AX(商业) 零副本 Iceberg/Parquet,号称单体可观便性宜100x;(5) Helicone(MIT,100K req/月 免费) 代理 tabanlı,15-30 分钟设测模式──生产常见水是:网关 ?? 关/key) (((((Phoenix 评估平台/Tru Telemetrics 通过连接

Bir LLM özelliği göndermişsiniz. Çalışıyor. Hemen başarısızlık, araç döngüleri, gecikme gerilemeleri, maliyet zirvesi veya hızlı önbelleğe ulaşma oranına dair hiçbir görünürlüğünüz yok. "LLM gözlemliliği" Google'a girin ve sekiz araç elde edin. Hepsi aynı sorunu üç farklı fiyat noktasında çözeceklerini iddia eder.

LangSmith, "Bu LangGraph çalışması neden başarısız oldu?" diye cevap verir. Phoenix, "RAG borumu akıntı mı?" diye cevap verir. Helicone, "Hangi uygulama jetonları yakıyor?" diye cevap verir. Langfuse, "Bütünü kendiliğimle otirebilir miyim?" diye cevap verir.

Seçim dört etkisi içerir: yığın (LangChain? çiğ SDK? çok satıcı?), lisans toleransı (sadece MIT? Elastik Tamam mı? ticari ceza mı?), bütçe ( ücretsiz seviyede? $100/mo? $1000/ay?), ve kendi kendine ev sahibi (heç zaman mı?

## Konsepten bir şey.

### İki kategori

**Development platforms**Bu, bir dizi deney çalıştırmak, hangi bir istek işe yaradı, hangi bir istek geri dönüşü, eski kazananlara karşı yeni bir istek. LangSmith, Langfuse, Comet Opik.

**Gateway/telemetry tools**Bu yöntemler,  prompt, response, tokens, latency, model, cost. Helicone, SigNoz, OpenLLMetry, Phoenix. Minimalist. OpenTelemetry üzerinden ayrı bir değerleme aracı ile birleştirilebilir.

### Langfuse  OSS dengesi

> **【拓展：LLM 可观测性工具选型决策】**2026 yıl LLM 可观测性工具选型的关键维度:(1) 技术LangChain/LangGraph 生态优先选 LangSmith;自研 SDK 选 Langfuse 或 Phoenix;(2) 许可证 MIT 选 Langfuse/Opik;Elastic License 2.0 可接受选 Phoenix;商业可选 LangSmith;(3) 自托管必须自托管选 Langfuse 或 Opik(Docker 部署);(4) 预算免费层 Langfuse 50K etkinlikler/ay,、Helicone 100K req/ay;(5) 规模> 10M 痕迹/day 选 Arize AX sıfır kopyası 架构;;

- Core Apache / MIT lisanslı; Docker üzerinden kendi kendine barındırma.
- Bulut ücretsiz seviyesi: ayda 50 bin etkinlik.
- Evals, hızlı yönetim, izler, veri kümeleri.
- Tatlı nokta: LangSmith sınıfı özellikleri istiyorsanız ama kendi kendini barındırmak veya OSS lisansı ile kalmak zorundasınız.

### Phoenix (Arize)  Telemetri-birincisi, OpenTelemetry-native

- Elastik Lisans 2.0; kendi kendine ev sahibi önemsiz.
- RAG ve drift görselleştirme konusunda mükemmel.
- Sürekli üretim arka uç olarak tasarlanmamış  öncelikle gelişme zamanında gözlemlenebilirlik.
- Tatlı nokta: RAG boru hattı geliştirme, drift debugging, üretim için ayrı bir kapı ile çiftleştirme.

### Arize AX  ölçek oyunu

- Ticari, buzberg/parket üzerinden sıfır kopyalı veri gölü entegrasyonu.
- S3'te kendi Parket'inizde izleri sakladığınız için matematik, Arize'nin doğrudan okuduğu bir şey.
- Tatlı nokta: Günde > 10M iz, mevcut veri gölü, DATADOG fiyatlandırması olmadan LLM özel araç çubuğu istiyor.

### LangSmith  LangChain/LangGraph önce

- Ticari, 39 dolar, aylık kullanıcı.
- LangChain ve LangGraph yığınları için sınıfında en iyi.
- Tatlı nokta: LangChain'e bağlı bir ekip, ödeme yapmaya hazır.

### Helicone  Proxy tabanlı minimum uygulanabilir

- 15-30 dakika ayarlayarak değiştir .`OPENAI_API_BASE`Helicone vekili.
- MIT lisanslı; 100 bin dolar ücretsiz, 20 dolar ücretli.
- Bu, failover, caching, rate limitleri de içerir.
- Ajan / çok adımlı izler üzerinde daha az derinlik.
- Tatlı nokta: hızlı başlatma, tek yığınlı uygulama, bir kapı + gözlemliliğe ihtiyaç duyar.

### Opik (Comet)  OSS geliştirme platformu

- Apache 2.0, tamamen OSS.
- Langfuse'nin Komet mirasına benzer bir özellik.
- Şimdiden Comet'te olan ML takımları aynı panelde LLM gözlemini istiyor.

### SigNoz  OpenTelemetry-first full APM

- Apache 2.0. OpenTelemetry üzerinden genel APM ve LLM ile ilgileniyor.
- Sweet spot: hizmetler ve LLM çağrıları arasında tek bir gözlemsellik.

### Yapıştırıcı: OpenTelemetry + GenAI semantik konvansiyonları

> **【中文解读】**OpenTelemetry 2025 yılının sonlarında GenAI 语义约定'i yayınladı .`gen_ai.system`- Evet.`gen_ai.request.model`- Evet.`gen_ai.usage.input_tokens`), 让不同工具可以互操作──2026 yılının üretim modeli şunlardır:(1) Her LLM'den 调用发出带 GenAI 约定的 OTel;(2) 路由到网关(Helicone/Portkey)做日常监控;(3) 双写到评估平台(Phoenix/Langfuse)做回归检测;(4) 存档到数据湖(Iceberg) do Arize AX veya DuckDB do长期分析;;

> **【拓展：LLM 可观测性的成本控制】**> 1M Yalvarma/Günün ölçeğinde, tüm kalıcılık maliyetinin toplamı LLM'nin kendi kendine kullanımından fazlasını yapmaktadır.

OpenTelemetry, 2025'in sonlarında GenAI semantik sözleşmelerini yayınladı (`gen_ai.system`- Evet .`gen_ai.request.model`- Evet .`gen_ai.usage.input_tokens`Otel tüketen araçlar birbirine etkileşime girebilir.

1. Her LLM görüşmesinden GenAI'nin toplantılarını yayınlayın.
2. Gündüzlü olarak kapıya giden yol (Helicone / Portkey).
3. Geri dönüşler için ikili gemi değerlendirme platformu (Phoenix / Langfuse).
4. Arize AX veya DuckDB üzerinden uzun süreli analiz için veri gölünde (Iceberg) arşiv.

### Tuzak: Yanlış katman üzerinde alet kullanmak

> **【中文解读】**埋点层级的选择:在 Agent 框架内埋点 (如添加 LangSmith traces) 会合到该框架;在 HTTP/OpenAI-SDK 层埋点 (通过 OpenLLMetry 或网关) 则可移植──2026 yılının en iyi uygulaması ise, protokol层埋点 (birlikte gömülmek için yapılan bir işlem)  Hangi çerçeve kullanıldığına bakılmaksızın, hepsi OpenTelemetry + GenAI 语义约定统采集──

Ajan çerçevesinin içinde araç kullanmak (örneğin LangSmith izlerini eklemek) sizi bu çerçeveye bağlar. HTTP/OpenAI-SDK katmanında (OpenLLMetry veya geçitinizle) araç kullanmak taşınabilir.

### Örnek almak  her şeyi saklayamazsın

Günlük > 1M talep, tam iz tutma LLM çağrılarından daha fazla maliyetlidir. Kurallar ile örnek: 100% hata, 100% yüksek maliyet, 5% başarı. Toplantıları her zaman tutun; uzun kuyruğu için ham tutun.

### Hatırlamalısın numaralar

- Langfuse ücretsiz bulut: Ayda 50 bin olay.
- LangSmith: 39 dolar / ay.
- Helikon ücretsiz: ayda 100 bin.
- Arize AX iddiası: ~ 100 kat daha ucuz monolit ölçekte.
- OpenTelemetry GenAI Sözleşmeleri: 2025 nakliye, 2026 geniş çapta kabul edildi.

## Çerçeveyi kullanın.
```figure
i4-otel-glue
```

## Kullan

`code/main.py`%100'lik tüketim, örnekleme, örnekleme + hatalar) depolama maliyetini ve her bir altta ne kaybolduklarını rapor eder.

> `code/main.py`%100'lik tüketim, örnekleme, örnekleme + hatalar) depolama maliyetini ve her bir altta ne kaybolduklarını rapor eder.

> `code/main.py`%100'lik tüketim, örnekleme, örnekleme + hatalar) depolama maliyetini ve her bir altta ne kaybolduklarını rapor eder.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-observability-stack.md`.Skala, bütçe, lisans duruşu göz önüne alındığında, araçları seçer.

> 本课产 出 `outputs/skill-observability-stack.md`.Skala, bütçe, lisans duruşu göz önüne alındığında, araçları seçer.

## Egzersizler.

1. LangChain'deki ekibiniz OSS'in kendi kendine konutlanmış gözlemselliğini istiyor.
   Çin Çeviri: Your team uses LangChain, wants to open source from托管可观测性──选择 Langfuse 或 Opik 并说明理由──
2. 5M izleri / gün ile Datadog ayda 150K $ teklifler, hesaplama Arize AX için eşitlik kırıklığı.
   Çinçe Çevirimiçi: 5M iz/gün  ölçeğinde,Datadog  fiyatı 150K $/月, hesap Arize AX 零拷贝方案的亏平衡点──
3. OpenTelemetry GenAI özelliğini oluşturun.
   Çinçe Çevirimi: Design a Your Organization Guide应强制要求每次 LLM 调用包含的 OpenTelemetry GenAI 属性集──
4. Phoenix'in üretime yeterli olup olmadığını tartışın.
   Çin dilinde:论证 Phoenix 单独使用是否足足以满足生产需求──它在什么情况下不够?
5. Helicone 20 ms proxy overhead. P99 TTFT 300 ms, kabul edilebilir mi?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| OpenLLMetry | "OTel for LLMs" | Open-source OpenTelemetry instrumentation for LLMs |
| GenAI conventions | "OTel attributes" | Standard OTel attribute names for LLM calls |
| LangSmith | "LangChain observability" | Commercial platform bundled with LangChain ecosystem |
| Langfuse | "OSS LangSmith" | MIT OSS with similar feature set |
| Phoenix | "Arize dev tool" | OpenTelemetry-native dev/eval platform |
| Arize AX | "scale observability" | Commercial zero-copy Iceberg/Parquet observability |
| Helicone | "proxy observability" | HTTP proxy collecting LLM telemetry + gateway features |
| Opik | "Comet LLM" | Apache 2.0 OSS dev platform from Comet |
| Session replay | "trace rerun" | Replay a full agent session with tool calls |
| Eval | "offline test" | Running candidate model/prompt over labeled dataset |

## Daha fazla okumak

- [SigNoz — Top LLM Observability Tools 2026](https://signoz.io/comparisons/llm-observability-tools/)
- [Langfuse — Arize AX Alternative analysis](https://langfuse.com/faq/all/best-phoenix-arize-alternatives)
- [PremAI — Setting Up Langfuse, LangSmith, Helicone, Phoenix](https://blog.premai.io/llm-observability-setting-up-langfuse-langsmith-helicone-phoenix/)
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Arize Phoenix docs](https://docs.arize.com/phoenix)
- [Helicone docs](https://docs.helicone.ai/)
