# Kaza Araştırmaları ve 2026 Sanatın Durumu .

> Üç üretim derecesi referansları, her biri farklı bir parça multi-agent mühendisliği gösterir. **Anthropic's Research system**(Orkestratör-işçi, 15x token, +90.2% tek ajan Opus 4 gökkuşağı dağıtımları) kanonik gözetmenlik vakaıdır. **MetaGPT / ChatDev**(SOP kodlanmış bir rol uzmanlığı yazılım mühendisliği için; ChatDev'in "kommunikatif halüsinasyon"u; DAGs üzerinden > 1000 ajanlara MacNet uzantısı, arXiv:2406.07155) kanonik rol parçalanma vakaıdır. **OpenClaw / Moltbook**(aslen Peter Steinberger tarafından Clawdbot, Kasım 2025; iki kez yeniden adlandırıldı; Mart 2026'a kadar 247k GitHub yıldızları; yerel ReAct-loop ajanları; Moltbook, başlatılmasından birkaç gün sonra ~2.3M ajan hesapları olan bir sosyal ağ olarak Meta 2026-03-10 tarafından satın alınmıştır) nüfus ölçeğinde olanları gösterir: gelişen ekonomik aktivite, hızlı enjeksiyon riskleri, devlet düzeyinde düzenleme (Çin, OpenClaw'ı hükümet bilgisayarlarında kısıtladı, Mart 2026).**Framework landscape April 2026:**LangGraph ve CrewAI lider üretimi; AG2 topluluk AutoGen devamıdır; Microsoft AutoGen bakım modunda (Microsoft Agent Framework, RC Feb 2026); OpenAI Agents SDK üretim Swarm'in halefi; Google ADK (Epril 2025) A2A-native girişimcidir. Her büyük çerçeve şimdi MCP desteği gönderir; çoğu A2A gemisi. Bu ders her durumu sonundan sona okuyor ve ortak desenleri distilliyor böylece bir sonraki üretim sisteminiz için doğru referans seçebilirsiniz.

> **【中文解读】**Bu bölüm 2026 SOTA çok ajanlık ıstanı araştırmasını ıfırlıyor ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfır ıfıfıfıfıfıfıfıfı ıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfıfı

> **【拓展：case studies 2026 sota→具体应用】**2026 yılında SOTA 多 Agent 系统案例:(1) Anthropic'in Claude Research多 Agent 协作 协作 深度研究;(2) OpenAI'nin Codex多 Agent 协作编码;(3) Microsoft'un AutoGen 团队多 Agent 软件开发──共同趋势:专业化分工、层化编排、MCP 工具使用和A2A Agent 间通信的结合──


**Type:** Learn (capstone) | **类型:** 学习（顶点）
**Languages:** — | **语言:** —
**Prerequisites:** all of Phase 16 (Lessons 01-24) | **前置知识:** Phase 16 全部（第 01-24 课）

>  **【前置】**Bu bölüm 16'da gerçekleşecek. Bu bölümde, "İşleme ve Geliştirme" adlı bölüm de yayımlanacak.
>  **【类比】**Üç örnek = "三种规模的多代理社会"――Antropic Research = 精小队(10 个代理,深度研究);MetaGPT = 标准开发团队(角色分工,SOP 编码);OpenClaw/Moltbook = 城市级社会(百万 Agent 涌现经济、被政府监管) ――2026 框架格局:LangGraph + CrewAI 领跑生产、AG2 接 AutoGen Microsoft AutoGen 合并、Open Agents SDK 是 Swarm 生产版、Google ADK 是 A2A 原生、
**Time:** ~90 minutes | **时间:** ~90 分钟

## Sorunlar sorunun giriş

Çoklu ajan mühendisliği genç bir disiplin. Üretim referansları az ve her biri farklı bir alanı kapsar. Bunları birbiriyle okumak yararlıdır; onları bir grup olarak karşılaştırmak daha yararlıdır. Bu ders, 2026'da yapılan üç kanonik vaka çalışmasını sonundan sona kadar okuyucu bir liste olarak ele alır, ortak desenleri işaretler ve çerçeve manzarasını haritalar böylece pazarlama değil bilgiyle çerçeve seçimleri yapabilirsiniz.

> Çocuğu temsilci olarak çalışmak, bir dizi yenilikçi bir ders olarak çalışmak ve bir çerçeveyi oluşturmak için bilgi üzerine değil, pazarlama üzerine kurulu bir çerçeve seçimi yapabilmek için çok az sayıda araştırma yapmaktadır.

## Konsept merkezi konsept

### Antropik Araştırma Sistemi

Claude Opus 4 planlar ve sentezler; Claude Sonnet 4 paralel olarak subagents araştırma.https://www.anthropic.com/engineering/multi-agent-research-system.

Ana ölçüm sonuçları:

> 关键测量结果:

- **+90.2%**İç araştırma değerlendirmelerinde tek ajan Opus 4'e göre gelişme.
  Çinçe Çevirisi: 提升                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    **+90.2%**- Evet.
- **80% of BrowseComp variance**Açıklandı **token usage alone** Çoklu ajan büyük ölçüde kazanır çünkü her alt eleman yeni bir bağlam penceresi alır.
  Çeviri:**80% 的 BrowseComp 方差**Sadece**token 使用量**解释多 代理 胜出 主要因为每个子 代理 获得新的上下文窗口──
- **15x tokens per query**Tek ajanla karşı.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çev**15 倍 token**- Tek Ajanla karşı.
- **Rainbow deployment**Çünkü ajanlar uzun süreli ve devletçi.
  Çeviri:**彩虹部署**Çünkü ajan uzun süre çalışıyor ve var.

Tasarım dersleri kodlandı:

> 编码化的设计教训:

1. **Scale effort to query complexity.**Basit → 1 ajan 3-10 araç çağrıları. Orta → 3 ajan. Karmaşık araştırma → 10+ alt eleman.
   Çeviri:**按查询复杂度扩展工作量。**简单 → 1 个代理 3-10 次工具调用──中等 → 3 个代理──复杂研究 → 10+ 子 Agent──
2. **Broad first, then narrow.**Subagentler geniş aramalar yapar; kurşun sentezler; takip subagentleri hedef derinlikleri yapar.
   Çeviri:**先广后窄。**Sonraki: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel: Genel:
3. **Rainbow deploys.**Uçuş ajanları bitene kadar eski sürümleri canlı tutun.
   Çeviri:**彩虹部署。**保持旧运行时版本活跃直到正在进行的代理 完成──
4. **Verification is not optional.**Sistem açık bir doğrulama rolü olmadan halüsinasyon yapması gözlemlendi.
   Çeviri:**验证不是可选的。**系统在没有明显验证者角色中被观察到产生幻觉──

Bu, üretim ölçeğinde denetim görevlisi topolojisi (Fase 16 · 05) için referans vakaıdır.

### MetaGPT / ChatDev

SOP rolü parçalanma durumunun kapsamı: arXiv:2308.00352 (MetaGPT) ve arXiv:2307.07924 (ChatDev).

MetaGPT, yazılım mühendisliği SOP'lerini rol istekleri olarak kodlar: Ürün Yöneticisi, Mimar, Proje Yöneticisi, Mühendis, Sorucu Bilgi Mühendisliği.`Code = SOP(Team)`. Her rolün dar ve özel bir ipucu vardır; roller arası teslimatlar yapılandırılmış eserler (PRD belgeleri, mimari belgeleri, kod) taşır.

ChatDev'in katkı: **communicative dehallucination**.Agentler cevap vermeden önce spesifik bilgileri talep eder.  Bir tasarımcı ajan, kullanıcı aracını çizmeden önce programcıya tahmin etmek yerine hangi dilin amaçlandığını sorar.

MacNet (arXiv:2406.07155) ChatDev'i **>1000 agents via DAGs**. DAG düğümleri bir rol uzmanlığıdır; kenarları transfer sözleşmelerini kodlar.

Tasarım dersleri:

> 设计教训:

1. **Structure matters more than size.**5 rolden oluşan SOP ekibi 50 ajanlı bir gruptan daha güçlü.
   Çeviri:**结构比规模更重要。**SOP 团队 紧的 5 角色 SOP 团队胜过 50 Ajanın yapılandırılmamış grupları
2. **Handoff contracts in writing.**Roller arasında geçen eserler bir şema izler.
   Çeviri:**书面交接契约。**角色间传递的制品遵循模式──
3. **Communicative dehallucination**ucuz ve yük taşıyan bir model.
   Çeviri:**交际去幻觉**Bu ucuz bir yöntem.
4. **DAGs scale further than chat.**Akış anlaşıldığında, kodlayın.
   Çeviri:**DAG 比聊天扩展更远。**- Evet. - Evet.

Bu, rol uzmanlaşması (Fase 16 · 08) ve yapılandırılmış topoloji (Fase 16 · 15) için referans vakaıdır.

### OpenClaw / Moltbook ekosistem

Üretim nüfus ölçeği vakası.

- **Nov 2025:**Clawdbot (Peter Steinberger'ın yerel ReAct-loop kodlama ajanı) gemileri.
- **Dec 2025 – Mar 2026:**iki kez yeniden adlandırıldı (Clawdbot → OpenClaw → OpenClaw altında devam etti).
- **Feb 2026:**Moltbook aynı primitivlerde sadece ajanlar için kullanılan sosyal ağ olarak başlatılıyor. ~ 2,3 milyon ajan hesabı birkaç gün içinde.
- **Mar 2026 (2026-03-10):**Meta Moltbook'u satın alıyor.
- **Mar 2026:**Çin OpenClaw'ı hükümet bilgisayarlarına kısıtlıyor.
- **Mar 2026:**OpenClaw 247 bin GitHub yıldızını geçiyor.

Bir ortak altyapıya milyonlarca ajan yerleştirildiğinde çoklu ajanın görünümü şöyle:

- **Emergent economic activity.**Ajanlar, simge ödemeleri kullanarak birbirlerini satın alırlar, satarlar ve hizmet verirler.
- **Prompt-injection risks at population scale.**Viral ajan profilindeki bir zararlı ipucu saatler içinde binlerce ajan-a-agent etkileşime yayılır.
- **State-level regulatory response.**Başlatılmasından birkaç hafta sonra, düzenleme ekosistemin içine ulaşır.

Bu olaydan alınan tasarım dersleri kısmen teknik, kısmen yönetimdir:

1. **Multi-agent at population scale is a new regime.**Bireysel sistemlerin en iyi uygulamaları (verifikasyon, rol açıklığı) hala geçerlidir, ancak yeterli değildir.
2. **Prompt injection is the new XSS.**Ajan profillerini ve ajanlar arası mesajları varsayılan olarak güvenilmeyen giriş olarak değerlendirin.
3. **Regulation is faster than design cycles.**Plan yap.
4. **Open-source + viral scale compounds.**4 ay içinde 247k yıldız olağandışı bir şey.

Bakın .[OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)CNBC / Palo Alto Networks ekosistem ayrıntıları için raporlar. Teknik temeller için, Clawdbot / OpenClaw depoları yerel ReAct döngüsünü ortaya çıkarır; Moltbook'un kamu yayınları üstte sosyal-graf mimarisini ortaya çıkarır.

### Çerçeve manzarası Nisan 2026

| Framework | Status | Best for | Notes |
|---|---|---|---|
| **LangGraph** (LangChain) | Production leader | structured graph + checkpointing + human-in-the-loop | recommended default for production |
| **CrewAI** | Production leader | role-based crews with Sequential/Hierarchical processes | strong for role decomposition |
| **AG2** | Community maintained | GroupChat + speaker selection | AutoGen v0.2 continuation |
| **Microsoft AutoGen** | Maintenance mode (Feb 2026) | — | merged into Microsoft Agent Framework RC |
| **Microsoft Agent Framework** | RC (Feb 2026) | orchestration patterns + enterprise integration | new entrant; watch |
| **OpenAI Agents SDK** | Production | Swarm successor | tool-return handoff pattern |
| **Google ADK** | Production (April 2025) | A2A-native | Google Cloud integration |
| **Anthropic Claude Agent SDK** | Production | single-agent + Research extension | see the Research system post |

Her büyük çerçeve şimdi gemi .**MCP**destek; çoğu gemi **A2A**Protokol uyumluluğu artık bir farklılık göstericisi değil.

### Üç durumda da ortak desenler

1. **Orchestrator + workers**(Antropik açık denetçi, MetaGPT PM-as-supervisor, OpenClaw bireysel ajanları + ağ etkileri).
   Çeviri:**编排者 + 工作者**(Antropik 显式监督者,MetaGPT PM 作监督者,OpenClaw 独立代理 + 网络效应)
2. **Structured handoff contracts**(Antropik alt görev tanımları, MetaGPT PRD/architektür belgeleri, OpenClaw A2A eserleri).
   Çeviri:**结构化交接契约**(Antropic 子 Agent 任务描述,MetaGPT PRD/架构文档,OpenClaw A2A 制品)
3. **Verification as first-class role**(Anthropic'in doğrulayıcısı, MetaGPT'in QA mühendisi, OpenClaw'ın ağ içi onaylayıcıları).
   Çeviri:**验证作为一等角色**(Anthropic'in test cihazı,MetaGPT'in QA  mühendisleri,OpenClaw'ın ağ içi test cihazı)
4. **Scaling is topology + substrate, not just more agents**(yağmurlu yayımlar, MacNet DAGs, nüfus ölçeği altyapılar).
   Çeviri:**扩展是拓扑 + 基底，不仅是更多 Agent**(彩虹部署, MacNet DAG, grup büyüklüğü)
5. **Cost is material and disclosed**(15x token, MetaGPT'de rol başına bütçe, Moltbook'da etkileşim başına fiyatlandırma).
   Çeviri:**成本是实质性的且已披露**(MetaGPT 中每角色预算,Moltbook 中每次交互定价)
6. **Security posture is explicit**(Anthropic'in kum kutulaması, MetaGPT'nin rol kısıtlamaları, OpenClaw'ın bilinen saldırı yüzeyi olarak hızlı enjeksiyonu).
   Çeviri:**安全态势是显式的**(Anthropic 的沙盒,MetaGPT 的角色限制,OpenClaw 的提示注入作为已知攻击面)

### Bir sonraki projenizin referansını seçmek

- **Production research / knowledge task → Anthropic Research.**Yeni bağlamlı alt-başlar kazanıyor.
- **Engineering / tool-chain workflow → MetaGPT / ChatDev.**Roller + SOP + el ele uzatma sözleşmeleri.
- **Network-effect social product → OpenClaw / Moltbook.**Altyapı + gelişen ekonomi.
- **Classic enterprise automation → CrewAI or LangGraph**(İsmin lideri, sabit çalışma süresi).

### 2026'daki en son son özet

2026 Nisan'da alanın nerede olduğu:

- **Frameworks are converging.**MCP + A2A desteği masa bahisleri. Elde etmek semantikleri kalan tasarım seçeneği.
- **Evaluation is hardening.**SWE-bench Pro, MARBLE, STRATUS hafifleme referansları.
- **Production failure rates are measurable**(Cemri 2025 MAST; 41-86,7% gerçek MAS) Bu alan "demonya'da harika görünüyor" çağından çıktı.
- **Cost is the central engineering constraint.**Görev başına token maliyeti, etkileşime karşı duvar saati, gökkuşağı dağıtım üst düzey. Çoklu ajan doğruluk kazanır ama maliyet kaybeder  ve bu ticaret iş kararıdır.
- **Regulation is a near-term input, not a background concern.**Yurtlar bireysel dağıtım döngüslerinden daha hızlı hareket ediyor.

## Kullanın Kullanın
```figure
a5-orchestrator-scale
```

## Kullan

`outputs/skill-case-study-mapper.md`Önerilen bir çok ajanlı sistem tasarımı okuyan ve daha yakın bir vaka çalışmasına haritası yapan bir beceri, vaka çalışmasının zaten test ettiği tasarım kararlarını ortaya çıkarır.

## Gönderin.

2026 yılında üretim çoklu ajanı için başlangıç kuralları:

- **Start from a case study, not from scratch.**En yakın Antropik Araştırma / MetaGPT / OpenClaw' ı seçin ve uyarlayın.
  Çeviri:**从案例研究开始，不是从零开始。**选择最接近的人类研究 / MetaGPT / OpenClaw 并适配──
- **Adopt MCP + A2A.**Çerçeveler arasında taşınabilirlik değerlidir; protokol desteği ücretsizdir.
  Çeviri:**采用 MCP + A2A。**Çevre üzerinden taşınabilirlik değerlidir; anlaşma desteği ücretsizdir.
- **Measure against SWE-bench Pro or your internal Pro-equivalent.**Kontrol edilmiş.
  Çeviri:**用 SWE-bench Pro 或你的内部 Pro 等效物衡量。**Kontrol edilmiş 已被污染──
- **Pay the verification tax.**Bağımsız bir doğrulayıcı, token bütçenizin ~ 20-30%'sine mal olur ve ölçülebilir doğruluk satın alır.
  Çeviri:**支付验证税。**独立验证器费用约 20-30% 代币预算,换取可测量的正确性──
- **Rainbow deploy long-running agents.**Çok saatlik ajanlar çalışması rutin bir şey olacak.
  Çeviri:**彩虹部署长时间运行 Agent。**预期多小时 Agent 运行是常规──
- **Read WMAC 2026 and the MAST follow-ups.**Disiplin hızlı ilerliyor.
  Çeviri:**阅读 WMAC 2026 和 MAST 后续。**Bu bilim hızla gelişiyor.

## Egzersizler.

1. Antropik Araştırma sistemini son-son okuyun. Opus 4'i daha küçük bir modelle değiştirirseniz değişecek üç tasarım kararını belirleyin (örneğin, Haiku 4).
2. MetaGPT Bölümleri 3-4 (arXiv:2308.00352). Kendi alanınızdan bir SOP'yi rol istekleri olarak kodlayın.
3. ChatDev'i okuyun. "İletişimsel halüsinasyon" mekanizmasını tanımlayın.
4. OpenClaw ve Moltbook hakkında okuyun. Popülasyon ölçeğinde ortaya çıkan ve 5 ajanlı bir sistemde görünmeyen belirli bir başarısızlık modunu seçin.
5. Şu anki çoklu ajan projenizi seçin. Üç vaka çalışmasının hangisi en yakın referansdır? O vaka çalışmasından hangi tasarım kararlarını henüz kabul etmediniz? Bu çeyrekte kabul edeceğiniz bir tane yazın.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Anthropic Research / Anthropic 研究 | "The supervisor reference" / "监督者参考" | Claude Opus 4 + Sonnet 4 subagents; 15x tokens; +90.2% over single-agent. / Claude Opus 4 + Sonnet 4 子 Agent；15 倍 token；比单 Agent +90.2%。 |
| MetaGPT | "SOP as prompts" / "SOP 作为提示" | Role decomposition for software engineering; `Code = SOP(Team)`. / 软件工程的角色分解；`Code = SOP(Team)`。 |
| ChatDev | "Agents as roles" / "Agent 作为角色" | Designer / programmer / reviewer / tester; communicative dehallucination. / 设计师/程序员/审阅者/测试者；交际去幻觉。 |
| MacNet | "Scale ChatDev via DAG" / "通过 DAG 扩展 ChatDev" | arXiv:2406.07155; 1000+ agents via explicit DAG routing. / arXiv:2406.07155；通过显式 DAG 路由实现 1000+ Agent。 |
| OpenClaw | "Local ReAct-loop agents" / "本地 ReAct 循环 Agent" | Steinberger's project; 247k stars by March 2026. / Steinberger 的项目；2026 年 3 月 247k 星。 |
| Moltbook | "Agent-only social network" / "Agent 专用社交网络" | 2.3M agent accounts; acquired by Meta March 2026. / 230 万 Agent 账户；2026 年 3 月被 Meta 收购。 |
| Rainbow deploy / 彩虹部署 | "Multiple versions concurrent" / "多版本并发" | Keep old runtime versions alive for in-flight long-running agents. / 保持旧运行时版本活跃以支持进行中的长时间 Agent。 |
| Communicative dehallucination / 交际去幻觉 | "Ask before answering" / "先问后答" | Agents request specifics from peers instead of guessing. / Agent 从同伴请求具体信息而非猜测。 |
| WMAC 2026 | "The AAAI workshop" / "AAAI 研讨会" | April 2026 community focal point for multi-agent coordination. / 2026 年 4 月多 Agent 协调的社区焦点。 |

## Daha fazla okumak

- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) denetim işçisi üretim referansı
- [MetaGPT — Meta Programming for Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) SOP rolü parçalanması
- [ChatDev — Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) İletişimsel halüsinasyon
- [MacNet — scaling role-based agents to 1000+](https://arxiv.org/abs/2406.07155) DAG tabanlı ölçek
- [OpenClaw on Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) Ekosistem genel bakış
- [WMAC 2026](https://multiagents.org/2026/) AAAI 2026 Köprü Programı Çoklu Ajan Koordinasyonu Atölyesinde
- [LangGraph docs](https://docs.langchain.com/oss/python/langgraph/workflows-agents) Üretim lideri
- [CrewAI docs](https://docs.crewai.com/en/introduction) Rol Temel Çerçeve
