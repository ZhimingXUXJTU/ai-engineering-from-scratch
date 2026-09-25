# Yönetilen LLM Platformları  Bedrock, Vertex AI, Azure OpenAI  平台 托管 OpenAI LLM

> Üç hiper ölçekli, üç farklı strateji. AWS Bedrock, bir API arkasında bir model pazarıdır  Claude, Llama, Titan, Stability, Cohere. Azure OpenAI özel kapasite için özel bir OpenAI ortaklığı ve sağlanan geçiş birimleri (PTU) dir. Vertex AI, en iyi uzun bağlamlı ve multimodal hikaye ile Gemini'nin ilk yeri aldı. 2026 yılında Yapay Analiz, Azure OpenAI'yi ortalama ~ 50 ms ve Bedrock'u Llama 3.1 405B eşdeğerlerinde ~ 75 ms olarak ölçer. Karar kuralının "en hızlı" değil, "ne model katalog ve FinOps yüzey ürünümle eşleşir".

> **【中文解读】**Bu bölüm, OpenAI, Antropik, Google ve diğerleri tarafından sağlanan model hizmet platformu seçim ve karşılaştırmalarını tanıttı.

>  **【前置】**学本节前 Lütfen önce öğrenin:Dava 11(LLM Mühendisliği)全部你已经将会使用OpenAI/Anthropic API 调模型;Dava 13(Yöntemleri ve Protokolleri)理解MCP等协议。本节讲生产部署选哪个云不是技术问题,是商业+合规+技术综合决策。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cost-and-latency comparator) | **语言:** Python（标准库，成本-延迟比较器）
**Prerequisites:** Phase 11 (LLM Engineering), Phase 13 (Tools & Protocols) | **前置知识:** Phase 11（LLM 工程）, Phase 13（工具与协议）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Öğrenme hedefleri

- Üç platform stratejisini (sıklama vs. özel vs. İkiz-birincil) isimlendirin ve her birini bir ürün kullanım durumuna eşleştirin.

>  **【类比】**Üç büyük bir platform LLM 服务 = 三种餐厅:(1) **AWS Bedrock**= 美食广场((1 API 调多家模型,Claude/Llama/Titan,灵活但延迟略高);(2) **Azure OpenAI**= 米其林餐厅(OpenAI 独家合作,PTU 专属容量,延迟最低 ~50ms,但贵且绑定 OpenAI);(3) **Vertex AI**= 主题餐厅(Google Gemini 主打,长上下文和多模态最强,2M token 窗口)。选哪个看你的菜谱(用Claude 还是GPT 还是 Gemini) 和预算──

> ️ **【易错点】**托管平台选型的 3 个坑:(1) **只看标价**Bedrock 上 Claude 比 Anthropic 直连贵15-20% (云税),但合规和统一计值钱;做 TCO (总拥有成本)而非单价比较 (单价比较)**忽略数据驻留** Avrupa kullanıcı verileri Avrupa'da kalmalıdır, Azure EU 区域 veya Bedrock eu-central-1'yi seçmeli; sınır dışı veri aktarımı GDPR'ye aykırı olarak yapılmaktadır.**没做厂商锁定评估** OpenAI PTU 后想换 Bedrock 后想换 Bedrock 后想换 Bedrock 后想换 Bedrock 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后想换 后后后后后后后改 后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后后
  Çin dilinde: ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎
- Azure OpenAI'de sağlanan geçiş ünitelerinin (PTU'lar) size ne satın aldığını ve neden talep üzerine Bedrock'un 405B ölçeğinde tipik olarak yaklaşık 25 ms daha yavaş okuduğunu açıklayın.
  Çinçe Çevirisi: Açıklayın Azure OpenAI'nin önceden hazırlanmış toplama birimi (PTU) ne getirdi ve neden Bedrock'un 405B'de dağıtılması genellikle 25 ms sürer.
- Her platform için FinOps atribut yüzeyini çiz (Bedrock Application Inference Profiles vs Vertex projesi-e-team vs Azure kapsamları + PTU rezervasyonları).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- "İki sağlayıcı minimum" politikasını yazın ve 2026'da tek satıcı kilitlemesinin neden pahalı bir hata olduğunu açıklayın.
  Çinçe Çevirisi:写下"iki tedarikçi en düşük" stratejisi,并解释为什么单供应商锁定是2026年昂贵的错误――

## Sorunlar. Sorunlar.

Ürününüz için Claude 3.7 Sonnet'i seçtiniz. Şimdi servis etmeniz gerekiyor. Anthropic API'yi doğrudan arayabilir veya AWS Bedrock üzerinden arayabilir veya bir geçit üzerinden geçebilirsiniz. Doğrudan API en basit; Bedrock BAAs, VPC son noktaları, IAM ve CloudWatch özelliğini ekler. Geçit servisleri arasında failover, tekelendirilmiş faturalama ve oran sınırlarını ekler.

> Modül için Claude 3.7 Sonnet'i seçtin. Şimdi bunu dağıtmak gerekiyor. AWS Bedrock'tan da doğrudan bir Antropic API'yi kullanabilirsin.

Daha derin bir soru katalog. Eğer aynı üründe Claude, Llama ve Gemini'ye ihtiyacınız varsa, aynı anda Bedrock + Vertex + Azure OpenAI'den başka bir yerden hepsini satın alamayacaksınız.

> Daha derin bir sorun model katalogudur. Aynı ürün içinde Claude、Llama 和 Gemini'ye ihtiyacınız varsa, aynı zamanda Bedrock + Vertex + Azure OpenAI kullanmadıkça tüm modelleri tek bir yerde satın alamayacaksınız.

Bu ders üç bahsi, gecikme boşluğu, FinOps boşluğu ve kilitleme riskiyi haritasıyor.

> Bu ders üç farklılık çizdi.

> **【中文解读】**选定 LLM 后,"在哪里部署" bir altyapı seviyesindeki bir kararıdır. API'yi doğrudan kullanmak en basit, ancak işletme seviyesinin kontrolü yoktur.

> **【拓展：LLM 部署模式】**2024-2026 yılları arasında LLM サービス部署 modeli "direkt API" → "cloud platform托管" → "AI 网关统一路由" gelişimi geçmiştir.OpenRouter、Portkey、LiteLLM gibi AI 网关 projeleri 2025 yılında büyük bir şekilde kullanıldı, temel değeri birden fazla tedarikçi arasında birleşik bağlantı sağlamak, otomatik başarısızlık ve maliyet optimize edilmesidir.

## Konsepten bir şey.

> **【中文解读】**Üç büyük bulut üreticisinin LLM platform stratejisi net olarak farklıdır: AWS Bedrock "model集市", birden fazla tedarikçiyi birleştirir; Azure OpenAI "独家合作",专为 OpenAI 模型; Vertex AI "Gemini 优先", 超长上下文和多媒体能力为卖点――bu stratejilerin farkını anlamak doğru seçim yapmanın temelini oluşturur.

> **【拓展：全球 LLM 云平台格局】**Ayrıca, 2026 yılında da dikkat edilmesi gereken başka bir konu var: Cloudflare İşçileri AI(çetleri düşünce) ✓ Birlikte AI(open source model düşünce platform, $0.18/M Llama 3.1 70B için tokens) ✓ Grroq(LPU  düşünce motor,TTFT < 20ms) ✓ Cerebras(CS-3 wafer ölçekli düşünce,2000+ token/s) ✓ ülke içinde yüzlerce binlerce ✓ 帆 里百炼、火山方舟 vb. var, ancak model katalogu uluslararası platformlarla birbirine bağlanmıyor.

### Üç strateji

**AWS Bedrock**Bu nedenle, bu ürünler, birbiriyle birlikte, bir diğer ürünlerin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de de ürünlerinin de ürünlerinin de ürünlerinin de ürünlerinin de de ürünlerinin de ürünlerinin de de de ürünlerinin de ürünlerinin de de ürünlerinin de de ürünlerinin de ürünlerinin de de de ürünlerinin de de ürünlerinin de de ürünlerinin de deye fişeri olarak üretilmesi gerekir.

> **AWS Bedrock** 模型集市──Claude(Antropik)、Llama(Meta)、Titan(AWS 自有)、Stability(图像)、Cohere(嵌入)、Mistral,以及图像和嵌入子目录──一个API、一个IAM 界面、一个CloudWatch 导出──Bedrock'ın 注是客户想要可选择性而不是单一模型──

**Azure OpenAI** özel ortaklık. Azure veri merkezlerinde GPT-4 / 4o / 5 / o serisi, DALL·E, Whisper ve OpenAI modellerinin ince ayarlarını alırsınız. "Azure OpenAI Hizmet" katalogunda OpenAI olmayan modeller yoktur  bunlar Azure AI Foundry'ye (ayrı bir ürün) gider. Azure'ın bahsi OpenAI'nin sınır olarak kalması ve müşteriler bu özel ilişki üzerinde kurumsal kontroller istemektedir.

> **Azure OpenAI** 独家合作──你在Azure 数据中心获得 GPT-4/4o/5/o 系列、DALL·E、Whisper 和 OpenAI 模型微调──"Azure OpenAI Service" 目录中没有非 OpenAI 模型那些在Azure AI Foundry(独立产品) 中──Azure'ın 注是OpenAI 保持前沿地位和客户想要对此的关系的企业级控制──

**Vertex AI** Gemini önce, diğer her şey ikinci. Gemini 1.5 / 2.0 / 2.5 Flash ve Pro, artı Model Garden (üçüncü taraf). Vertex'in bahsi multimodal uzun bağlam  1M-token Gemini bağlamı farklılık göstericidir.

> **Vertex AI** Gemini  öncelikli, diğer 其次── Gemini 1.5/2.0/2.5 Flash 和 Pro,加上 Model Garden(第三方)──Vertex'in 注是多模态长上下文1M token的 Gemini 上文是差异化因素──

### Ölçüsünde gecikme farkı

Yapay Analiz sürekli referans değerleri kullanıyor. Eşdeğer Llama 3.1 405B dağıtımlarında (dava üzerine paylaşılan), Azure OpenAI ortalama ilk jeton gecikmesi yaklaşık 50 ms; Bedrock yaklaşık 75 ms. Bu boşluk AWS başarısızlığı değil  kapasite model farkıdır. Azure, kiracı için GPU kapasitesini rezerve eden PTU'ları (Provisioned Throughput Units) satıyor. Bedrock'un eşdeğeri (Provisioned Throughput) var ama birim başına saatte yaklaşık 21 $ başlıyor ve çoğu müşteri talep üzerine paylaşılan bir hizmette kalıyor.

> Yapay Analiz 运行持续基准测试。在等效的Llama 3.1 405B 部署) 上,Azure OpenAI 中位首代代币 延迟约50ms;Bedrock 约75ms。差距不是AWS 问题而是容量模型差异。Azure 销售 PTU(预置吞吐量单位),为您租户预留 GPU 容量。Bedrock 等效功能存在但起价约$21/户小时/按量模式,大多数客户使用共享量模式。

İstek üzerine paylaşılan kapasite diğer tüm müşterilerin trafiği ile rekabet eder. Dedicated kapasite değil. Eğer ürün SLA'sı TTFT < 100 ms ise, ya Azure'da PTU'lar satın alırsınız, ya da Bedrock Provisioned Throughput satın alırsınız veya varyasyonu kabul edersiniz.

> 量共享容量与其他客户流量竞争 GPU 资源──专用容量不会── Eğer ürününüzün SLA'sı P99 TTFT < 100ms ise, ya Azure'da PTU satın almak, ya Bedrock Provisioned Throughput satın almak, ya da kabul etmesi gerekir──

> **【中文解读】**延迟差的本质是"容量模型"差. 延迟差的本质是"容量模型"差. 延迟差的本质是"容量模型"差. 延迟差的本质是"容量模型"差. 延迟差的本质是"容量模型"差. 延迟差的本质是"容量模型"差. 延迟差的本质是"容量模型"差. 延迟差的本质是"容量模型"差. 延迟差的本质是"容量模型"差. 共有量量部署中,您的请求与其他客户的流量竞争 GPU 资源;专用容量(PTU)则保留独占 GPU .  Azure PTU在40%利用率下可节省高达70% 成本,但空时仍付费.

### Sağlanan Çıktılama Ekonomi

Azure PTU'ları: bir sonucu hesaplama rezervasyonu. Önceden tahmin edilebilir iş yükleri için %70 tasarruf karşı talep. Trafikten bağımsız olarak saat başına sabit maliyetler  boşlukta bile rezervasyon için ödeme yaparsınız. Kesinlik genellikle sürdürülebilir kullanımın %40-60 civarındadır.

> Azure PTU: öncekil hesaplama blokları. Önceden tahmin edilebilir iş yükü için, ağırlık modülü tasarruf ile %70'e kadar.

Yataklı Çıktıran: $21-$Model ve bölgeye bağlı olarak saatte 50'lik. Benzer matematik  Break-even yaklaşık yarım en yüksek kullanımdır. Aylık taahhüt gereklidir.

> Yataklı Yüküm: 每小时 $21-$50, model ve bölgeye bağlıdır. Buna benzer ekonomik modellerin  hüzün noktası, en yüksek değer kullanım oranının yaklaşık yarısıdır.

Vertex'in sağlanan kapasitesi Gemini SKU'na göre satılır; fiyatlandırma model ve bölgeye göre değişir ve daha az kamuoyuna duyurulur.

> Vertex  Gemini SKU  Satışına göre ön planlama kapasitesi; fiyat model ve bölgeye göre farklı, açık bilgi daha az

### FinOps yüzeyi  gerçek farklılık

**Bedrock Application Inference Profiles**Bu, pazardaki en temiz atribut.`team`- Evet .`product`- Evet .`feature`; tüm model çağrılarını üzerinden yönlendirir; CloudWatch, post-işlemeden profil başına maliyetleri koparır. 2025'te eklendi, hala en granüler hiperkaler doğası.

> **Bedrock Application Inference Profiles**Pazarda en net maliyet özelliği programı.`team`- Evet.`product`- Evet.`feature`Tahmini yapılandırma dosyası; tüm modellerin kullanılması; CloudWatch  İhtiyacın yok sonrası işlemleri; yapılandırma dosyasının ayrılması için maliyetleri.

**Vertex**Bu yüzden, bu programın tüm programları bir grup için kullanmak için kullanılır. Bu programın tüm programları bir grup için kullanılır.

> **Vertex**归因是项目-per-团队加无处不在标签――你将每个团队建模为一个GCP项目,在每个资源上放置标签,使用BigQuery Billing Export + DataStudio 进行汇总――工作量更大,但BigQuery 允许你对成本数据执行任意SQL――

**Azure**PTU rezervasyonları birinci sınıf bir maliyet nesnesi olarak abonelik / kaynak grubu alanlarına ve etiketlere dayanır. Etiketler başlıkları damgalayan bir geçit gerektirir.

> **Azure**Bu nedenle, her talebin özelliği gereklidir Uygulama anlayışları özgün tanımlama göstergesi veya başlıklı bir net bağlantı.

Şekil: Bedrock en temiz yerli, Vertex en esnek BigQuery, Azure en açık değil instrument kullanmadıkça.

> Bedrock, Vertex, BigQuery, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Azure, Az

> **【中文解读】**FinOps (云财务运营) LLM 基础设施中最低估的维度──Bedrock's Application Inference Profiles is currently the most precise original generated in attribution scheme团队,产品,功能标签 分拆调用成本;Vertex 通过 BigQuery 导出提供最大灵活性,可用SQL任意聚合;Azure 最为不透明,除非你自行使用应用洞察的埋点──选择平台时,FinOps 能力与延迟、价格等等重要──

> **【拓展：LLM FinOps 实践】**企业 LLM 支出 in 2025 year average increased 300% ((Flexera 2025 云状态报告) 常见 FinOps 策略包括:(1) 按代币 消耗设置团队预算告警;(2) 使用缓存层(Semantic Cache) 模型路由简单任务用小模型、复杂任务用大模型,可节省50%+ 成本;(4) 批量 API 在非实时场景可降低50% 价格;;

### 2026 yılındaki risk kilitlenme.

Tek bir hiperkalterli yükümlülük bir model baskın olduğunda iyiydi. 2026 yılında sınır ayda  Claude 3.7 bir çeyrekte, Gemini 2.5 bir sonraki, GPT-5 bir sonraki çeyrekte hareket eder. Bir platformun kilitlenmesi sınırın üçte ikisini kilitler.

> Bir model yönetiyorken, tek bir sözleşme de olabilir. 2026 yılının ön kenar modeli her ay değişmektedir. Bir dönem Claude 3.7, bir dönem Gemini 2.5, bir dönem GPT-5'dir. Bir platform kilitlenmesi, iki üçte birinin ön kenar kapasitesini ifade eder.

Model çalışma takımları: Herhangi bir ürün kritik LLM çağrısı için iki sağlayıcı minimum. Bedrock artı Azure OpenAI ortak çiftidir  Claude birinden, diğerinden GPT, bunlar arasında bir hata geçidi, aynı geçit. Geçiş yolları optimal olduğundan maliyet artışı önemsizdir; kesintiler sırasında kullanılabilirlik artışı (Azure OpenAI Ocak 2025 olayı gibi, AWS us-east-1 kesinti) belirleyici.

> Yüksek performanslı ekip kullanımı modeli: herhangi bir ürün anahtar LLM 调用双供应商最低策略。Bedrock + Azure OpenAI en yaygın bir kombinasyonudur biri Claude sağlar, diğeri GPT sağlar, aynı ağ bağlantısı üzerinden故障转移が行われます。 maliyetler giderek artıyor. Çünkü ağ bağlantısı yoluyla en iyi; 机期間に可用性提升 (Azure OpenAI 2025 yılının 1 月事件、AWS us-east-1 机) 決定性です。

> **【中文解读】**2026 yılının en büyük altyapı riskleri tedarikçi kilitlenmesidir. Ön kenar modeli her dönem değişmektedir. Claude 3.7, Q2 ile Gemini 2.5, Q3 ile GPT-5 ile. GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT-5 ile GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le GPT'le Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute Gute G

> **【拓展：云厂商宕机事件】**Azure OpenAI'nin 1 Ocak 2025'te uzun süredir süren genel bir hata yaşadığı, tüm tek Azure'ın ChatGPT  işletme müşterilerine etkisiyle sonuçlandı. Aynı yıl AWS'in US-East-1 bölgesinde de ciddi bir hata oluştu. Birçok tedarikçi stratejisi bu olaylarda değerini kanıtladı: Bir 机时, 网关 otomatik olarak akışını diğerine geçirir, sıfır algılama hataları aktarılır. Cloudflare'ın 2025 yılı kullanılabilirlik raporunda, çok tedarikçi ticari yapılarının LLM hizmetlerinin kullanılabilirliği %99.99'a ulaşırken, tek tedarikçi genellikle %99.9'a ulaşır.

### Veri oturumları, BAA'lar ve düzenlenmiş endüstriler

Bedrock: Çoğu bölgede BAA'lar; VPC son noktaları; koruma rayları.
Azure OpenAI: HIPAA, SOC 2, ISO 27001; AB veri ikamet; kurumsal düzenlenmiş varsayım.
Vertex: HIPAA, GDPR, bölge başına veri oturum; Google Cloud'un uyumluluk yığıncağı.

> Bedrock:多数区域提供 BAAs; VPC 端点;防护──常见金融科技默认选择──
> Azure OpenAI:HIPAA、SOC 2、ISO 27001;EU 数据驻留;企业监管默认选择──
> Vertex:HIPAA、GDPR、 selon données régionales résidentes;Google Cloud'ın 🏻

Üçü de temel kontrol kutusuna uymaktadır. Farklılıklar veri saklama politikaları, günlüklerin nasıl işlenmesi ve kötüye kullanımı izleme trafiğinizin okunup okunmadığı (öntemli olarak çoğu için seçilme; işletme için seçilme seçenekleri mevcuttur).

> Üç kişi de temel şart şartlarını karşılıyor. Farklılık, veri saklama stratejisi, günlük işleme biçimi ve trafiklerinizin kullanımını kontrol etmekle ilgilidir.

### Hatırlamalısın numaralar

- Azure OpenAI ortalama TTFT Llama 3.1 405B eşdeğerlerinde: ~ 50 ms (PTU ile).
  Çeviri:Azure OpenAI 在 Llama 3.1 405B 等效模型上中位 TTFT:~50ms(PTU kullan)
- İsteğe bağlı yatak ortalaması TTFT: ~75 ms.
  Çeviri:Bedrock 按量模式中位 TTFT:~75ms。
- Yataklı Çıktıran: $21-$Birim başına 50/saat.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri$21-$50/小时──
- Azure PTU'nun dengesi: %40-60 sürdürülebilir kullanım.
  中文翻译:Azure PTU 亏平衡点:~40-60% 持续利用率──
- Yüksek kullanım oranında talep karşısında PTU tasarrufları: %70'e kadar.
  Çinçe çevirisi:PTU: %70'e kadar yüksek kullanım oranı ile karşılaştırıldığında

## Çerçeveyi kullanın.
```figure
i4-platform-lanes
```

## Kullan

`code/main.py`Sintez bir iş yükü üzerinde üç platformu karşılaştırır  talep karşısında PTU ekonomisini, TTFT varyansını ve maliyet atributun sadakatini modeller.

> `code/main.py`Yapısal çalışma yükü ile karşılaştırıldığında üç platform var. Bu platform, üretim miktarı ile PTU'nun ekonomikliği arasında TTFT ı farkı ve maliyet oranı arasında gerçeklik ve doğruluk ile karşılaştırılmıştır.

> **【中文解读】**实践部分通过模拟工作负载对比三大平台──关键指标包括:TTFT(首代币 延迟) 、吞吐量、每百万代币 成本──通过调整利用率参数,直观看 PTU 在什么负载水平下比按量计费更划算──

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-managed-platform-picker.md`. İş yükü profilini (gerekli modeller, TTFT SLA, günlük hacmi, uyumluluk gereksinimleri) göz önüne alarak, birincil bir platform, bir geri dönüş ve FinOps alet planı önerir.

> 本课产 出 `outputs/skill-managed-platform-picker.md`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊                                                                                                                                                                                                                                                                            

> **【拓展：生产环境平台选型 Checklist】**生产环境 LLM 平台选型应考虑:(1) 模型目录是否覆盖所需模型;(2) 延迟 SLA 是否满足用户体验要求;(对话 < 200ms TTFT,批处理无严格要求);(3) 合规认证;(HIPAA/SOC2/ISO27001);(4) 数据驻留(GDPR 欧盟 区域存储要求);(5) 成本归因粒度;(能否按团队/产品拆分账单);(6) 容量方案(多区域/多应供应商失败)

## Egzersizler.

1. Çık .`code/main.py`Azure PTU, 70B sınıfı modelini talep üzerine hangi sürdürülebilir kullanım oranında geçiyor?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ Azure PTU'nun 70B sınıfı modelinden daha iyi bir kullanım oranı altında, reklamın %40-60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %60 oranında %70 oranında %60 oranında %70 oranında %70 oranında %70 oranında %70 oranında %70 oranında %70 oranında %70 oranında %70 oranında %70 oranında %10% oranında %%%%%% oranında %%%%%% oranında %%%%%%% oranında %%%%%%%%%%%%%%%%%%% oranında %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
2. Ürününüz Claude 3.7 Sonnet ve GPT-4o'ya ihtiyaç duyar. Hangi hiperkaler'e giden iki tedarikçi dağıtımını tasarlayın, önde hangi kapı oturuyor, başarısızlık politikası nedir?
   Çinçe Çevirimi: Ürünleriniz Claude 3.7 Sonnet 和 GPT-4o.
3. Düzenlenmiş bir sağlık hizmetleri müşteri BAAs, ABD Doğu veri oturum ve sub-100ms P99 TTFT gerektirir. Bir platform seçin ve üç özel özellikle haklı çıkarın.
   Çinçe çevirisi: bir denetim altında olan sağlık hizmetleri müşterisi BAA'lara ihtiyaç duyar, ABD Doğu'da kalma ve P99 TTFT < 100ms.
4. Bu ay Bedrock faturanın trafik değişiminin olmamasına rağmen 4 kat artığını keşfedin.
   Çinçe Çevirimi: You found 本月 Bedrock 账单翻了4倍但流量未变──没有应用推理个人资料 怎么找到原因?有个人资料 需要多长时间?
5. Azure OpenAI ve Bedrock fiyat sayfalarını okuyun. 100M-token / ay Claude iş yükü için, daha ucuz  doğrudan Anthropic API, Bedrock talep üzerine veya Bedrock sağlanan geçiş?
   Çine dilinde: Çıkış: okuyun Azure OpenAI 和 Bedrock 定价页面── 100M token/month'ın Claude 工作负载 için, hangisi daha uygun?

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| Bedrock | "AWS LLM service" | Model marketplace across Claude, Llama, Titan, Mistral, Cohere | AWS 的 LLM 模型集市平台 |
| Azure OpenAI | "Azure's ChatGPT" | Exclusive OpenAI models in Azure datacenters with enterprise controls | Azure 独家托管 OpenAI 模型的企业服务 |
| Vertex AI | "Google's LLM" | Gemini-first platform with Model Garden for third-party models | Google 的 Gemini 优先 AI 平台 |
| PTU | "dedicated capacity" | Provisioned Throughput Unit — reserved inference GPUs, priced per hour | 预置吞吐量单位——独占推理 GPU 容量 |
| Application Inference Profile | "Bedrock tagging" | Per-product cost/usage profile with tags, CloudWatch-native | Bedrock 按产品归因的推理配置文件 |
| Model Garden | "Vertex catalog" | Vertex AI's third-party model section, separate from Gemini | Vertex AI 第三方模型目录 |
| Two-provider minimum | "LLM redundancy" | Policy of running every critical LLM path across ≥2 hyperscalers | 双供应商最低策略——关键 LLM 调用跨 2+ 云商 |
| BAA | "HIPAA paperwork" | Business Associate Agreement; required for PHI; provided by all three | 业务关联协议——HIPAA 合规必需 |
| Abuse monitoring | "the log watcher" | Provider-side safety scan on prompts/outputs; opt-out in enterprise | 平台侧的 prompt/输出安全扫描 |

## Daha fazla okumak

- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) yetkili oran kartı ve sağlanan throughput fiyatlandırması.
- [Azure OpenAI Service Pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/) PTU ekonomisi ve oran kartları.
- [Vertex AI Generative AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) Gemini katları ve Model Garden taksitleri.
- [Artificial Analysis LLM Leaderboard](https://artificialanalysis.ai/) Sağlayıcılar arasında sürekli gecikme ve geçiş referansları.
- [The AI Journal — AWS Bedrock vs Azure OpenAI CTO Guide 2026](https://theaijournal.co/2026/03/aws-bedrock-vs-azure-openai/) Kurumsal karar çerçevesini.
- [Finout — Bedrock vs Vertex vs Azure FinOps](https://www.finout.io/blog/bedrock-vs.-vertex-vs.-azure-cognitive-a-finops-comparison-for-ai-spend) Atribut mekanizması yan yana.
