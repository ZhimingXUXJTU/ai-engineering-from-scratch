# A2A  Ajan-Ajan Protokolü  A2A: Ajan 间通信协议

> Google, A2A'yı Nisan 2025'te duyurdu. Nisan 2026'a kadar özellikleri https://a2a-protocol.org/latest/specification/ve 150'den fazla kuruluş bunu destekliyor. A2A, MCP'nin yatay tamamlayıcıdır (Deneyim 13): MCP dikey (ajan  araçlar), A2A ise eşeğen (ajan  ajan). Agent Kartları (kaşif), eserlerle (metin, yapılandırılmış veriler, video), açık olmayan görev yaşam döngüleri ve ot. Üretim sistemleri giderek daha fazla MCP ile A2A eşleştirir. Google Cloud, 2025-2026 yılları boyunca Vertex AI Ajan Oluşturucu'na A2A desteğini ekledi.

> **【中文解读】**Google, 2025 yılının Nisan ayında A2A  anlaşmasını yayınladı; 2026 yılının Nisan ayında, kuralların 150+  organizasyon desteği vardır. A2A, MCP'nin düzeysel tamamlamasıdır: MCP, dikey bir Ajan ve araçtır. A2A, nokta karşı nokta.

> **【拓展：A2A → Google 的 Agent 协议】**A2A, Google tarafından yönetilen Agent 间通信标准协议, Antropic ile MCP (Model Context Protocol) ile birlikte.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `http.server`, `json`) | **语言:** Python (标准库, `http.server`, `json`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前请先掌握:Phase 13·15-20(MCP 协议套件) 、Phase 16·04(原语) ・・・A2A 是 MCP 的水平补充:MCP=Agent 调工具(垂直),A2A=Agent 找 Agent(横向) ・・・
>  **【类比】**MCP + A2A = "电话黄页 + 直接通话"──MCP = 工具目录(agent 找工具用);A2A = Agent 间通话协议(agent 找 agent 协作)──2026 生产系统标配:MCP(连工具) + A2A(连其他 Agent) + Agent Card(发现)──Google 主导,150+ 组织支持──

## Sorunlar sorunun giriş

Bu nedenle, bir diğer ajanın diğer bir sistemdeki başka bir ajanı araması gerekir. Nasıl? HTTP bir son noktasını ortaya koyabilir, özel bir JSON şeması tanımlayabilir ve diğer tarafın konuşmasını umarsınız. Her çift ajan özel bir entegrasyon haline gelir.

> Bir HTTP biteni ortaya koyabilir, bir yapılandırılmış JSON  modeli tanımlayabilir ve diğer bir tarafın bunu anlayabilmesini ister.

N kare entegrasyon sorunu: N ajanları ile N × 1) 2) / 2 özel entegrasyonlara ihtiyacınız var. 10 ajanla 45 entegrasyon olur. 100 ajanla 4950 A2A bu değerleri N ajan kartlarına ayırır.

> N 平方集成問題:N 个代理 需要 N×(N-1)/2 个定制集成──10 个代理 是 45 个集成──100 个代理 是 4950 个──A2A, 个代理卡片,每个描述一个代理──

A2A, bu çağrı için evrensel kablo protokolüdür. Standart keşif, standart görev modeli, standart ulaşım, standart eserler. HTTP+REST gibi ama birinci sınıf vatandaşlar olarak ajanlar için.

> A2A, standard bulma, standart görev modeli, standart aktarım, standart işlemi, HTTP+REST gibi, ancak bir vatandaş olarak bir ajan olarak kullanılmalıdır.

Anahtar soyutlama: ajanlar adreslenebilir, keşfedilebilir ağ son noktalarıdır. Bir ajanı "import" etmiyorsunuz, "sırıyorsunuz". Bu, dağıtımı koparır  ajan A2A konuşduğu sürece, herhangi bir dilde, hangi çerçeveyi kullanırsa çalıştırılır.

> 关键抽象:Agent is可寻址、可发现的网络端点──你不"导入"Agent;你"调用"它──这解已部署Agent 运行在任何地方、使用任何语言、使用任何框架,只要它说A2A──

## Konsept merkezi konsept

### Dört unsur

> Dört element

**Agent Card.**JSON belgesini `/.well-known/agent.json`Bu, bir kişinin adı, becerileri, son noktaları, desteklenen yöntemleri, yazar gereksinimleri ile ilgili.

> **Agent 卡片。**位于 `/.well-known/agent.json`JSON 文档,描述 Agent:名称、技能、端点、支持的模态、认证要求──通过读取卡进行发现──

Bilinen URL konvansiyonu web standartlarını yansıtır (`/.well-known/`aynı yol için kullanılır `robots.txt`A2A uyumlu herhangi bir ajanı bu URL'yi alarak keşfedebilirsiniz.

> Bilgi URL 约定镜像 Web 标准(`/.well-known/`Yapılacak`robots.txt`、ACME 挑战、OIDC 发现的相同路径) ∼ herhangi bir A2A 兼容 Ajan bu URL 发现 ∼ not required registry ∼代理 ∼ central directory ∼

**Task.**İş birimi. Hayat döngüsü olan asynk, durumlu bir nesne:`submitted -> working -> completed / failed / canceled`Bir müşteri bir görev gönderir, anketler gönderir veya güncellemelere abone olur.

> **任务。**工作单元── yaşam döngüsünde değişik durumlu nesneler:`submitted -> working -> completed / failed / canceled` Müşteri gönderme görevleri, sorgular veya yenilemeler

**Artifact.**Bir görev tarafından üretilen sonuç türü. Metin, yapılandırılmış JSON, görüntü, video, ses. Sanat eserleri yazılır, böylece farklı modaliteler birinci sınıftır.

> **工件。**任务产生的结果类型──文本、结构化 JSON、图像、视频、音频──工件是有类型的,因此不同模态是平等公民──

**Opaque lifecycle.**A2A, uzaktan ajanın görevi nasıl çözeceğini belirlemez. Müşteri, durum geçişlerini ve eserleri görür; uygulamanın herhangi bir çerçeveyi kullanması özgürdür.

> **不透明生命周期。**A2A 不规范远程代理 *如何* 解决任务──客户端看状态转换和工件;实现可以自由使用任何框架──

Bu çürüklük tasarımla gerçekleşir. LangGraph, CrewAI veya özel Python metni üzerine inşa edilmiş bir uzaktan ajan A2A istemcisine benzer görünüyor. İşbirliği, içerikleri değil, tel biçimi üzerinde anlaşmaktan kaynaklanır.

> Bu şekilde açıklıktan çıkmazlar. LangGraph, CrewAI veya Python'un kendiliğinden tanımlanmış bir yazılı yapılandırma üzerine kurulan uzaktan ajan A2A müşteriye göre aynı görünür.

### MCP/A2A bölümü

- **MCP**(Deneyim 13): ajan <-> aracı. Ajan bir araç sunucusuna JSON-RPC üzerinden okur/yazır. Öntanımlı olarak devletsiz.
  Çeviri:**MCP**(Lection 13):Agent <-> 工具──Agent 通过 JSON-RPC 读写工具服务器──默认无状态──
- **A2A**Tıpkı bir diğer örneğin, bir diğer örneğin, bir diğer örneğin, bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de diğerinin de bir diğerinin de diğerinin de bir diğerinin de diğerinin de bir diğerinin de diğerinin de birini de diğerinin de diğerinin de bir diğerinin de diğerinin de bir diğerinin de diğerinin de birini de diğerinin de diğerinin de bir diğerinin de diğerinin de birini de diğerinin de bir diğerinin de diğerinin de birini de diğerinin de bir de diğerinin de diğerinin de de birini de diğerinin de de de diğerinin de bir de diğerinin de de de de de de bir de diğerinin de de de de de de de diğerinin de de de de de bir de diğerinin de de de de de de de de de bir de diğerinin de de de de de de de de de de de de bir de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de de
  Çeviri:**A2A**Ajanın (Agent) ‒ Ajanın (Agent) ‒ Antlaşmaları; her iki taraf da kendi kararlarını veren bir Ajanın (Agent) ‒

Bir A2A eşleri tarafında MCP araçları çağırır.

> Ürünler arasında bir çok A2A var. A2A, diğer terminallerde MCP araçlarını kullanıyor.

Genel bir örnektir: A şirketindeki A2A " araştırma ajanı " bir MCP arama aracı sunucusunu içe çağrıştırır, sonra bulgularını B şirketindeki A2A " analitik ajanına " iade eder. A2A organize iletişimdir; iç araç kullanımı MCP. Her protokol en iyi yaptığı şeyi yapar.

> 常见模式: A2A'nın araştırma ajanı şirket A'nın içi MCP'yi arama araç servisine yönlendirir, sonra B'nin A2A'nın analiz ajanına geri dönerken bulur.

Ya da akışla: SSE aboneliği`/tasks/{id}/events`- Geçici güncellemeler için.

> Ya da kullanın: SSE 订阅 `/tasks/{id}/events`获取推送更新──

### Müellif

A2A üç ortak örneği destekler:

> A2A 支持三种常见模式:

Üç örneği, "Kimlik sağlayıcıma güveniyorum" (OAuth2 taşıyıcısı) "birbirimizi birbirimizle doğruluyoruz" (mTLS) "birbirimiz hiçbir üçüncü kişiye güvenmiyoruz" (HMAC imzası) kadar spektrü kapsar. Güvenlik gereksinimlerinize uyan en hafif olanı seçin.

> Üç çeşit model kapsamına "我信任我的身份提供商" (OAuth2 taşıyıcısı) "我们相互验证彼此" (MTLS) "我们不信任任何第三方" (HMAC) 签名) kadar girer.

- **Bearer token** OAuth2 veya açık olmayan.
  Çeviri:**Bearer token** OAuth2 或不透明令牌。
- **mTLS** karşılıklı TLS; kuruluşlar birbirlerine kimliklerini kanıtlar.
  Çeviri:**mTLS** 双向 TLS;组织相互证明身份──
- **Signed requests**- HMAC, yararlı yük üzerinde.
  Çeviri:**签名请求** HMAC'ın geçerli yüklemesi için.

Auth, ajan kartında açıklanmıştır. Müşteriler bulup uyarlar.

> 认证在代理卡中声明;客户端发现并遵守──

### 150'den fazla kuruluş Nisan 2026'a kadar

İşletme kurulumu A2A ölçeğini hızlandırdı. Başlık: A2A, işletme ajan sistemlerinin güven sınırlarını geçmesinin yolu haline geldi. Google Cloud Vertex AI Agent Builder A2A desteğini gönderdi; Microsoft Agent Framework onu destekler; çoğu ana çerçeve (LangGraph, CrewAI, AutoGen) A2A adaptörlerini gönderdi.

> 企业采用推动了A2A'nın ölçeklenmesini。标题:A2A 成为企业代理 系统跨越信任边界的方式。Google Cloud 提供了Vertex AI Agent Builder A2A 支持;Microsoft Agent Framework 支持它;大多数主要框架(LangGraph、CrewAI、AutoGen)提供了A2A 适配器。

A2A'nın FIPA-ACL'nin başarısız olduğu kurumsal kabul kazanmasının nedeni: A2A JSON- doğaldır, mevcut web altyapısını kullanır (HTTP, SSE, OAuth), ve paylaşılan ontolojiler gerektirmez. FIPA'nın genel maliyeti katildi; A2A dersi öğrendi.

> A2A, işyerinde FIPA-ACL'in başarısız olmasının nedenleri: A2A, JSON'un doğuşundan oluştu, mevcut Web altyapısını kullanmak, HTTP, SSE, OAuth)

### A2A'nın kazandığı yer

- **Cross-organization calls.**A şirketindeki ajan B şirketindeki ajanı arıyor. A2A olmadan her çift özel bir sözleşme olur.
  Çeviri:**跨组织调用。**Şirket A'nın Ajanı Şirket B'nin Ajanı...
- **Heterogeneous frameworks.**LangGraph ajanı CrewAI ajanı özel Python ajanı arıyor.
  Çeviri:**异构框架。**LangGraph Ajanı 调用 CrewAI Ajanı 调用自定义 Python Ajanı。A2A 标准化。
- **Typed artifacts.**Video sonucu, yapılandırılmış JSON, ses  hepsi birinci sınıf.
  Çeviri:**类型化工件。**视频结果、结构化 JSON、音频都是一等公民──
- **Long-running tasks.**Çürük yaşam döngüsü + anketler saatlerce süren görevleri kolaylaştırır.
  Çeviri:**长时间运行的任务。**Açıklama olmayan yaşam döngüsü + sorgular, küçük bir zamanlı görevleri basitleştirir.

### A2A'nın mücadele ettiği yer

- **Latency-sensitive micro-calls.**A2A'nın yaşam döngüsü asynk. Sub-millisecond ajan-a-agent uyumlu değil; doğrudan RPC kullanın.
  Çeviri:**延迟敏感的微调用。**A2A'nın yaşam döngüsü değişiktir.
- **Tight-coupled in-process agents.**Eğer her iki ajan da aynı Python işleminde çalışırsa, A2A'nın HTTP geri dönüş yolculuğu aşırı derecede.
  Çeviri:**紧耦合的进程内 Agent。**Eğer iki ajan aynı Python sürecinde çalışırsa, A2A'nın HTTP dönüşü aşırı tasarlanmıştır.
- **Small teams.**Spec overhead gerçek; sadece içsel ajanlar için resmiye ihtiyaç duyulmayabilir.
  Çeviri:**小团队。**规范开销是真实的; yalnızca içsel ajanın bu resmiğe ihtiyacı olmayabilir.

### A2A vs ACP, ANP, NLIP

2024-2026 yıllarında ilgili birkaç özellik ortaya çıktı:

> 2024-2026 yılları arasında birkaç ilgili kural ortaya çıktı:

- **ACP**(IBM/Linux Vakfı)  A2A'nın öncesi, daha dar kapsam.
  Çeviri:**ACP**(IBM/Linux Vakfı)  A2A'nın öncemi, kapsamı daha darıktır.
- **ANP**(Agent Network Protocol)  Eş-Kahtap-Kahtap-Kahtap, Merkezsiz-İlk.
  Çeviri:**ANP**(Agent Network Protocol) 重对等发现,去中心化优先
- **NLIP**(Ecma Doğal Dil İşbirliği Protokolü, standartlaştırılmış Aralık 2025)  Doğal dil içerik türü.
  Çeviri:**NLIP**(Ecma Natura Language交互协议,2025年 12 月標準化)

A2A, Nisan 2026 itibariyle en çok kabul edilen eşler arası protokoldür. karşılaştırma için arXiv:2505.02279 (Liu et al., "A Survey of Agent Interoperability Protocols") bakınız.

> 截至 2026 年 4 月, A2A en geniş çaplı karşılaştırma anlaşması kullanılmıştır.

2026 protokol manzarası istikrar kazanmıştır: A2A ajan işbirliği için, MCP araçlar için, ACP'ler yörüngelerin kaydedilmesi için A2A'ya emildi, ANP'ler örgütler arası kimlik için. NLIP niş kalıyor.

> 2026 yıl anlaşma şekli belirlenmiştir: A2A Ajan işbirliği, MCP araçlar, ACP A2A'yı yansıtmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'yı kullanmak için A2A'nın kullanılması için A2A'nın kullanılması için A2A'nın kullanılması için A2A'nın kullanılması için A2A'nın kullanılması için A2A'nın kullanılması için A2A'nın kullanılması için A2A'nın kullanılması için A2A'nın kullanılması için A2A'nın kullanılması için A'nın kullanılması gerekir.

## Yapın.
```figure
sw-agent-card-discovery
```

## Yapın

`code/main.py`A2A-minimal bir sunucu ve istemci uyguluyor `http.server`Ve JSON.

> `code/main.py`Kullanım`http.server`A2A için JSON uygulaması en küçük sunucu ve müşteri sunucu:

- Açıklamalar`/.well-known/agent.json`- Evet .
  Çıkış:`/.well-known/agent.json`- Evet .
- kabul eder .`POST /tasks`- Evet .
  Çeviri: kabul`POST /tasks`- Evet .
- Görev durumu yönetir,
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Artefakları geri gönderir .`GET /tasks/{id}`- Evet .
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Ç Ç Ç Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç`GET /tasks/{id}`Ünlü işlere geri dönmek.

Müşteri:

> 客户端:

- Ajan kartını alır.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- görev gönderir,
  Çeviri: Görev Görevleri
- Seçimler tamamlanana kadar,
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- - Bu eser okur.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

Skenar, sunucuyu arka plan bir ipçeye başlatır, sonra da istemciyi ona karşı çalışır.

> 脚本在后台线程中启动服务器,然后运行客户端──你看完整流程:发现、提交、轮询、工件──

## Çerçeveyi kullanın.

`outputs/skill-a2a-integrator.md`A2A entegrasyonu tasarlıyor: Agent Kart içeriği, görev skemeleri, yazar seçimi, akış ve anket.

> `outputs/skill-a2a-integrator.md`设计 A2A 集成:Agent 卡片内容、任务模式、认证选择、流式 vs 轮询──

## İndirin . Ürünler .

Kontrol listesini:

> 检查清单:

- **Pin the spec version.**A2A hala gelişmekte. Ajan Kartı protokol versiyonunu açıklamalı.
  Çeviri:**固定规范版本。**A2A  hâlâ gelişmekte;Agent 卡片应声明协议版本
- **Idempotent task creation.**Çift gönderiler (ağ yeniden denemeleri) bir görev oluşturmalıdır.
  Çeviri:**幂等任务创建。**重复提交 (网络重试) bir görev oluşmalıdır.
- **Artifact schemas.**Ajanın hangi şekilleri gönderdiğini bildirin; tüketicilerin onaylaması gerekir.
  Çeviri:**工件模式。**声明 Ajan 返回什么形状;消费者应验证。
- **Rate limits + auth.**A2A kamuya yöneliktir; standart web güvenliği uygulayın.
  Çeviri:**速率限制 + 认证。**A2A 面向公众;应用标准Web安全──
- **Dead-letter for failed tasks.**Sürekli aralıklı arıza türleri için zaman içinde kalıpları kontrol edin.
  Çeviri:**失败任务死信。**随时检查模式反复出现的失败类型的发现――

## Egzersizler.

1. Çık .`code/main.py`Müşteri sunucuyu keşfettiğini ve doğru eseri aldığını onaylayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Müşteriyi bulma servisinin doğru işlemi kabul etmediğini doğrula.
2. Servere ikinci bir beceri ekleyin (örneğin "cümle edin"). Ajan Kartı güncelleyin. Görev türüne göre beceri seçen bir istemci yazın.
   Çinçe Çevirimi Çevirisi:向服务器添加第二个技能 (,) "cadetleştirmek" gibi.
3. SSE akış sonucu uygulamak: `/tasks/{id}/events`Müşterinin farklı bir şekilde ne yapması gerekiyor?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`/tasks/{id}/events`...evlenme durumu değişir. Müşteriye ne yapılması gerekiyor?
4. A2A spesifikasyonunu okuyun. Bu demo uygulamayan üç şeyi belirleyin.
   Çinçe Çevirimiçi:A2A 规范──识别规范要求的三个演示未实现的东西──
5. A2A (Agent Card keşfi) ile MCP (server tarafı yetenek listesi üzerinden) karşılaştırın `listTools`Kendini tanımlayan ajanlar ile yetenek denetleme arasındaki fark nedir?
   Çinçe Çevirimiçi: A2A Agent 卡片发现) ile MCP Agent 卡片发现)`listTools`Servisör Endüme Yetenek Listesi) ◊ Özben tanımlama Ajan ve Yetenek Araştırmacıları arasındaki tartışma nedir?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| A2A | "Agent-to-agent" / "Agent 对 Agent" | Peer protocol for agents to call other agents across systems. Google 2025. / Agent 跨系统调用其他 Agent 的对等协议。Google 2025。 |
| Agent Card / Agent 卡片 | "The agent's business card" / "Agent 的名片" | JSON at `/.well-known/agent.json` describing skills, endpoints, auth. / 描述技能、端点、认证的 JSON。 |
| Task / 任务 | "The unit of work" / "工作单元" | Async stateful object with a lifecycle; artifacts produced on completion. / 具有生命周期的异步有状态对象；完成时产生工件。 |
| Artifact / 工件 | "The result" / "结果" | Typed output: text, structured JSON, image, video, audio. First-class media. / 类型化输出：文本、结构化 JSON、图像、视频、音频。一等媒体。 |
| Opaque lifecycle / 不透明生命周期 | "How it's solved is the agent's business" / "如何解决是 Agent 的事" | Client sees state transitions; server is free to choose framework/tools. / 客户端看到状态转换；服务器自由选择框架/工具。 |
| Discovery / 发现 | "Finding the agent" / "找到 Agent" | `GET /.well-known/agent.json` returns the card. / 返回卡片的 GET 请求。 |
| MCP vs A2A | "Tools vs peers" / "工具 vs 对等" | MCP: vertical agent <-> tool. A2A: horizontal agent <-> agent. / MCP：垂直 Agent <-> 工具。A2A：水平 Agent <-> Agent。 |
| ACP / ANP / NLIP | "Sibling protocols" / "兄弟协议" | Adjacent specs; A2A is the most-adopted 2026. / 相邻规范；A2A 是 2026 年采用最广泛的。 |

## Daha fazla okumak

- [A2A specification](https://a2a-protocol.org/latest/specification/) Kanonik özellik
  Çeviri:A2A 规范  权威规范
- [Google Developers Blog — A2A announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) Nisan 2025'te başlatma tarihi
  中文翻译:Google 开发者博客  A2A 公告  2025 yıl 4 月发布文章
- [A2A GitHub repo](https://github.com/a2aproject/A2A) Referans uygulamalar ve SDK'lar
  中文翻译:A2A GitHub 仓库  参考实现和 SDK
- [Liu et al. — A Survey of Agent Interoperability Protocols](https://arxiv.org/html/2505.02279v1) MCP, ACP, A2A, ANP karşılaştırması
  中文翻译:Liu 等人  Agent 互操作性协议综述  MCP、ACP、A2A、ANP 比较
