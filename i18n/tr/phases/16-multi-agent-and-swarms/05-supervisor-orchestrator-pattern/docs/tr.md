# Gözetmen / Orkestör-İşçi Şablonu

> Bir lider ajan planlar ve delegeler; uzman işçiler paralel bağlamlarda yürütür ve rapor verir. Bu, Anthropic'in Araştırma sisteminin arkasındaki bir örnektir (Claude Opus 4 öncülük olarak, Sonnet 4 subagent olarak), iç araştırma değerlendirmelerinde tek ajan Opus 4'e göre +90.2% olarak ölçülmüştür. Anthropic'in mühendislik yazısı, BrowseComp'deki farklılığın %80'inin sadece token kullanımı ile açıklandığını bildirir. Bu ders, ilklerden denetleme örneğini oluşturur ve 2026'da üretim dağıtımlarından mühendislik derslerini kapsar.

> **【中文解读】**Bir yönetimci ajan 规划并委派任务;专业化工作器在并行上下文中执行并汇报──这是人类研究 系统背后的模式(Claude Opus 4.6 主管,Sonnet 4.5 子 Agent),内部研究评估上单 Agent Opus 4.6 提升 90.2%──核心洞察:多 Agent 胜出主要因为每个子 Agent 获得独立的下文窗口80%

> **【拓展：Supervisor 模式 → Claude DevFleet】**Claude Code'nin çoklu ajanı düzenleme aracı Claude DevFleet'in yönetimsel yönetim modeli gerçekleştirilmesi için bir baş ajanı görevleri çözmek için gönderir.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `threading`) | **语言:** Python (标准库, `threading`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前 Lütfen önce bil:Fase 16·04(4 个原语)、Fase 14·01(Agent 循环) ――Suporvisor 模式 = 多 Agent 中最常用的一种一个主管 + 多个工作器──
>  **【类比】**Gözetmen 模式 = "project manager + 工程师团队"──主管(Opus)分解任务+审查,工作器(Sonet) 各干一摊──Antropic 数据:BrowseComp 80% 方差由代币 使用解释多 代理 赢是因为每个子 代理有独立上下文窗口(fresh context),不是协调本身魔法──

## Sorunlar sorunun giriş

Araştırma tek ajan sistemlerinin başarısız olduğu prototip bir görevdir. "23-2026 yılları arasında çok ajan sistemlerinde ne değişmiştir?" diye sorarsanız, tek ajan beş makaleyi sıradan okuyor, bağlamının yarısını metinleriyle dolduruyor ve sonra hepsini birlikte düşünüyor. Beşinciye ulaştığında ilk makaleyi unutuyor. Paralelleşemez.

> Araştırma, tek Ajan  Sistem başarısızlığı tipik görevidir. "2023 ile 2026 yılları arasında çok sayıda Ajan  Sisteminde ne değişiklikler oldu?" diye soruyorsunuz.

Tek ajanın başarısızlığı yapay, daha iyi çağrılarla düzeltilmez. Sistem çağrısı ne kadar iyi olursa olsun, bağlam penceresi dolur.

> 单代理 失败是结构性的,不能用更好的提示修复──不管系统提示多好,上下文窗口都会填满──综合需要的信息(所有五篇论文的关键发现)

Gözetmen örneği bunu düzeltir: bir lider ajanı arama planlıyor, her alt soruyu bir işçiye delegeler ediyor ve sentezler. Her işçi dar bir soru için kendi 200k jeton penceresini alır. Önder asla çiğ kağıtları görmez  sadece işçi özetlerini.

> 监督者模式修复了这个问题:一个主导代理 规划搜索,将每个子问题委派给一个工作器,然后综合――每个工作器获得自己的200k代币 窗口用于一个狭窄的问题――主导永远不看原始论文只看工作器摘要――

Bilgi akışı tasarımdır: ham veri işçi bağlamlarında kalır; sadece sıkıştırılmış bulgular liderine ulaşır. liderin bağlamı verilerin yüklenmesine değil senteze adanır. Bu mimari kazanç  veriler ağır işlerin sentesis ağır işlerden ayrılmasıdır.

> 信息流是设计:原始数据留在工作器上下文中; yalnızca sıkıştırılmış bulgular yöneticiye ulaşmıştır.

Anthropic'in üretim Araştırma sistemi, iç araştırma değerlendirmelerinin %90.2'si ile tek bir Opus 4'ün karşılaştırıldığını bildirir. Aynı yayın, BrowseComp'in %80'inin sadece *token kullanımı* ile açıklandığını belirtir.

> Anthropic'in üretim araştırma sistemi raporu, iç araştırma değerlendirmelerinde tek bir Opus 4'e göre %90.2 arttı. Aynı makalede BrowseComp'in                                                                                                                                                                                                                                           

%80 numarası başlık bulgu: model seçimi, prompt mühendisliği ve araçlama birlikte değişikliğin yalnızca %20'sini açıklar. Eğer daha iyi bir araştırma ajanı performansını istiyorsanız, uyarıları düzeltmeden önce daha fazla token (daha fazla alt kısım, daha büyük bağlamlar) harcayın.

> %80 bu rakam bir başlık bulma: model seçimi, öneriler ve araçlar artışı sadece %20'in farkını açıklar. Eğer daha iyi bir araştırma yapmak istiyorsanız, Ajan performansını düzenleme önerilerinden önce daha fazla token harcamalısınız.

## Konsept merkezi konsept

### - Şekil

```
                 ┌──────────────┐
                 │   Lead       │  plans, decomposes,
                 │  (Opus 4)    │  synthesizes
                 └──┬────┬───┬──┘
                    │    │   │
            ┌───────┘    │   └───────┐
            ▼            ▼           ▼
      ┌─────────┐  ┌─────────┐  ┌─────────┐
      │ Worker1 │  │ Worker2 │  │ Worker3 │
      │(Sonnet) │  │(Sonnet) │  │(Sonnet) │
      └─────────┘  └─────────┘  └─────────┘
         fresh       fresh        fresh
         context     context      context
```

Ögürlük asla hammaddeyi okumayı, işçiler birbirlerinin çalışmalarını, ögürün sentezlenmesi kadar görmez.

> Üstünler daima birbirlerinin çalışmalarını görmezler.

Bu bilgi izolasyonu temel tasarım seçeneğidir. Önderin bağlam penceresi planlama ve senteze odaklanır.

> Bu tür bilgi ayrımı, çekirdek tasarım seçimi. Üstün bir pencerede, düzenleme ve kompleks üzerinde odaklanmak için devam eder.

### Neden kazanıyor?

Üç mekanizma:

> Üç mekanizma:

1. **Fresh context per subagent.**"FIPA-ACL mirası"nı keşfeden bir işçi, 40 bin tokeni taşımaz.
   Çeviri:**每个子 Agent 的清新上下文。**探索"FIPA-ACL 遗产" çalışma cihazı taşımaz.
2. **Specialization via prompt.**Önderin emri "şehirlen ve sentezlen" değil, " araştır". Her çalışanın emri dar: "X'de ne değişmiş bul. "
   Çeviri:**通过提示专业化。**Önderin önerisi " çözülme ve bütünleşme " değil, " araştırmak "dır. Her çalışma makinesi önerisi kısadır.
3. **Parallelism.**İşçiler aynı anda çalışıyorlar.`max(worker_times) + plan + synthesis`- Hayır .`sum(worker_times)`- Evet .
   Çeviri:**并行性。**工作器并发运行──挂钟时间大约是 `max(worker_times) + plan + synthesis`- Hayır .`sum(worker_times)`- Evet.

### Mühendislik dersleri (Antropik 2025)

Anthropic yazısı, 2026 yılı için hâlâ geçerli olan birkaç üretim dersi listelerini listeler:

> Anthropic'in makalesinde 2026 yılındaki üretim deneyimleri için hâlâ geçerli olan birkaç madde belirtildi:

- **Scale effort to query complexity.**Basit sorular: bir ajan, 3-10 araç çağrısı. Karmaşık sorular: 10+ ajan.
  Çeviri:**按查询复杂度缩放工作量。**简单查询:一个代理,3-10次工具调用──复杂查询:10+个代理──主管必须估计这一点,而不是调用者──
- **Broad then narrow.**Önce geniş alt sorulara ayrılır, sonra cevap derinliği gerekirse, her alt soruya daha fazla işçi doğurur.
  Çeviri:**先宽后窄。**Önce geniş bir çocuk sorusu olarak ayrılır, eğer cevap derinlik gerektirirse, her çocuk sorusu için daha fazla çalışma makinesi üretilir.
- **Rainbow deployments.**Agentler uzun süredir ve devletlidir. Geleneksel mavi-yeşil işe yaramaz. Antropik gökkuşağı kullanır: eski sürümler boşalırken yeni sürümlerin yavaş yavaş yayılması.
  Çeviri:**彩虹部署。**Agent is longtime running and has a state of use. Geleneksel bir yeşil şubenin etkisi yok.
- **Token usage dominates.**Çoklu ajan, tek ajanın tokenlerinin 15 katı. Sadece görev değeri maliyeti haklı çıkarırsa çalıştırın.
  Çeviri:**Token 使用量占主导。**Çoğu ajan tek ajanın yaklaşık 15 katı bir simgesidir. Sadece görev değerini kanıtlayan maliyetin makul olduğu zaman kullanılır.

### Grafik-devlik dönüş

LangGraph başlangıçta bir `langgraph-supervisor`Yüksek düzeyde bir kütüphane ile `create_supervisor`LangChain, 2025 yılında tavsiyede yardımcı olanlara yardımcı olmak için, yönetici modelini doğrudan araç çağrısı yoluyla uygulamaya yöneltti. Çünkü araç çağrısı, yönetici'nin gördüğü şey üzerinde daha fazla kontrol sağlar.

> LangGraph ilk olarak bir tane yüksek seviye olan bir yayın yayınladı .`create_supervisor`Yardımcı`langgraph-supervisor`库──2025 yıl LangChain, 工具调用对*监督者看什么*(上下文工程) için daha fazla kontrol sağlamak için doğrudan gerçekleştirilen denetçi modelini kullanmak için bir araç olarak değiştirilmesini önerecektir.

Değişim 2025-2026'daki bir anlayışı yansıtır: bağlam mühendisliği orkestrasyon mühendisliği'nden daha önemlidir. Müdürün gördüğü planlama yapabileceklerini belirler. Çiğ işçi bağlamını geçmek liderin planlama yeteneğini öldürür; dar özetleri geçmek onu korur.

> Bu dönüşüm 2025-2026 yıllarındaki anlayışları yansıtıyor: Ünlü yazılım tasarımından daha önemlidir. Kontrolcü neyi planlayabileceğini belirlediğini görüyor.

### Başarısız modları

- **Lead hallucinates the plan.**Eğer lider gerçek soruyu çözemeden alt sorular ortaya çıkarsa, işçiler yanlış hedefe doğru bir araştırma yaparlar.
  Çeviri:**主导者幻觉计划。**Eğer yönetici oluşturduğu çocuk sorunu gerçek sorunu çözmezse, çalışma makinesi yanlış hedef üzerinde kesin bir araştırma yapar.
- **Workers over-explore.**Açık bir kapsam sınırları olmadan, işçiler kendilerine verilen alt sorunun ötesine doğru ilerler ve sentez aşamasını kirletirler.
  Çeviri:**工作器过度探索。** açık bir kapsam sınırları olmadan, iş makinesi dağıtılmış alt sorunlardan ve kirlenme genel adımlardan uzaklaşır.
- **Synthesis conflicts.**İki işçi çelişkili gerçekleri iletir. Önder ya tekrar sormalıdır (bir yuvarlak ekle) veya anlaşmazlığı açıkça not etmelidir.
  Çeviri:**综合冲突。**两个工作器回复矛盾的事实――主导者必须重新询问(增加一轮) 或明确记录分歧――静默选择一方是最糟糕的失败:用户永远不知道发生分歧――

### Müdürün yanıldığında

- **Sequential tasks.**Eğer adım 2'nin adım 1'in çıkışına gerçekten ihtiyacı varsa paralellik hiçbir şey satın almaz.
  Çeviri:**顺序任务。**Eğer adım 2 gerçekten adım 1'nin çıkışına ihtiyaç duyarsa, işlem hiç yardımcı olmaz.
- **Simple queries.**Tek ajan, işçilerin doğurulmasından önce liderin "skala çaba" kontrolünü kullanın.
  Çeviri:**简单查询。**单代理 更快更便宜地处理它们―― 发作工作器之前使用主导的"缩放工作量"检查――
- **Strict determinism.**Gözetmen, LLM tarafından seçilen bir delegasyon kullanır.
  Çeviri:**严格确定性。**监督者使用 LLM 选择的委派──当审计/回放比适应性更重要时,静态图更好──

## Yapın.
```figure
supervisor-hierarchy
```

## Yapın

`code/main.py`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `threading`. Önder bir soruyu alt sorulara parçalayır, işçiler her alt soruya eş zamanlı olarak çalışır ve önder sentez eder. Gerçek LLM'ler yoktur  işçiler getirip toplamak simüle etmek için yazılmıştır.

> `code/main.py`Kullanım`threading`❖ bir üç ortak çalışma makinesi gözetmeni gerçekleştirmek. ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖  ❖ ❖    ❖ ❖                                                                                                              

Ana yapı:

> 关键结构:

- `Lead.plan(query)`Bir soruyu 3 alt soruya ayırır.
  Çeviri:`Lead.plan(query)`Soru sorgularını üç bölümde bölmek istiyorum.
- `Worker.run(sub_q)`sahte bir özet gönderir (prodüksiyonda herhangi bir araç kullanan bir ajan olabilir).
  Çeviri:`Worker.run(sub_q)`返回一个假摘要(在生产中可以是任何工具的代理)
- `Lead.run(query)`İşçilerin iplerini, bağlarını ve sentezlerini teker teker teker.
  Çeviri:`Lead.run(query)`Bu arada, çalışmayı başlatın, bekleyin, sonra bir araya gelin.

Çık:

```
python3 code/main.py
```

Çıktılık planı, paralel işçi izlerini başlangıç/sonluk zaman damgaları ve son sentezi gösterir. Duvar saati kazanır: 0.3 saniyelik üç işçi 0.35 saniye içinde koştu, 0.9 değil.

> 输出显示计划、带有开始/结束时间的并行工作器跟踪和最终综合―― hang钟时间优势:三个 0.3 秒的工作器在0.35 秒内运行而不是0.9 秒内运行――

## Çerçeveyi kullanın.

`outputs/skill-supervisor-designer.md`Kullanıcı sorguyu alır ve bir denetim örneği tasarımı üretir: lider sistem sorgu, işçi rolleri, alt sorgu parçalanma kuralları ve sentez şablonu.

> `outputs/skill-supervisor-designer.md`接收用户查询并生成监督者模式设计:主导系统提示、工作器角色、子问题分解规则和综合模板──在构建新研究风格 系统之前使用──

## İndirin . Ürünler .

Gözetmenlik örneğini kullanmadan önce kontrol listesi:

> 部署监督者模式之前的检查清单:

- **Model pairing.**Dönüşüm düzeyi modeli üzerinde liderlik (Opus sınıfı, `o3`Daha hızlı ve daha ucuz bir model üzerinde çalışanlar (Sonet, `o4-mini`)
  Çeviri:**模型配对。**主导者使用推理级模型(Opus 类、`o3`类) ・工作器使用更快、更便宜的模型(Sonet、`o4-mini`)。
- **Worker timeout.**Ortalama çalışmanın 2 katını aşan herhangi bir işçi öldürülür; lider ya daha dar bir kapsamla yeniden doğar ya da olmadan devam eder.
  Çeviri:**工作器超时。** 2 kat daha fazla çalışma süresi olan herhangi bir çalışma makinesi sona ermiştir; yönetici ya daha dar bir kapsamda yeniden üretilir ya da kullanmaya devam eder.
- **Token cap per worker.**Zor bir sınır (örneğin, beklenen sentez girişinin 10 katı) kaçak bir işçinin bütçeyi patlatmasını engeller.
  Çeviri:**每个工作器的 Token 上限。**硬限制 (örneğin, önlenmiş toplam girişin 10 katı) kontrolden çıkmış çalışma makinelerinin bütçeyi tüketmesini önlemek için.
- **Observability.**Önderin planını, her çalışanın araç çağrısını ve sentezi takip edin.
  Çeviri:**可观测性。**Bu, her işçinin alet düzenlemesi ve bütünleşmesi için yapılan bir çalışma.
- **Rainbow rollout.**Devletlerin uzun süreli ajanları, sıcak değişim değil, yavaş yavaş bir sürüm geçişine ihtiyaç duyarlar.
  Çeviri:**彩虹推出。**Bir ajanın sıcak bir değişim yerine bir geçiş yapması gerekiyor.

## Egzersizler.

1. Çık .`code/main.py`Bu demo'da, hangi işçi sayısında, atlama maliyeti paralel tasarruftan daha fazla mı?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`, sonra yöneticiyi 3 yerine 5 çalışma makinesi üretmek için değiştirir.
2. İşçi zamanlaması uygulayın: 0.5 saniyeden uzun süre çalışan herhangi bir işçiyi öldürün ve kalan sonuçları sentezleştirin.
   Çinçe Çevirimi: gerçekleştirmek için çalışma makinesi süper zaman: İş makinesi 0.5 saniye geçmeden herhangi bir çalışmayı durdur, yöneticinin toplam kalan sonuçları görmesini sağlayın.
3. Önderin sentezine çatışma tespit adımını ekleyin: iki işçi çelişkili cevaplar verirse, önder bir tanesini seçmek yerine anlaşmazlığı not eder. LLM'yi çağırmadan çelişkiyi nasıl tespit edersiniz?
   Çinçe çevirisi: Önderin kompleksinde çatışma kontrolü ekleme adımları: Eğer iki işçi bir çatışma yanıtını geri verirse, önder bir tanesini seçmek yerine ayrılığa düşebilir.
4. Anthropic'in Araştırma-Sistem Mühendisliği yazısını okuyun.
   Çinçe çevirisi:阅读Antropic的研究系统工程文章──列出这个玩具演示需要在生产中采用三种做法──
5. LangGraph'in karşılaştırması `create_supervisor`(Memleket) vs. yeni araç çağrısı önerisi. Bu size denetçinin gördüğü şeylerin üzerinde daha iyi bir kontrol sağlar. Neden Anthropic açıkça sadece alt cevapları ve ham işçi bağlamını senteze geçirir?
   Çeviri: LangGraph'ın `create_supervisor`(Old version) Yeni araçlar ile birlikte düzenlenmiş öneriler. Hangi yönlendirmeler sizi daha iyi kontrol eden gözetmenlere ne gösterir?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Supervisor / 监督者 | "Lead agent" / "主导 Agent" | An orchestrator agent that plans, delegates, and synthesizes. Does not do the work itself. / 规划、委派和综合的编排 Agent。不做实际工作。 |
| Worker / 工作器 | "Subagent" / "子 Agent" | A focused agent invoked by the supervisor with narrow scope and its own context window. / 由监督者调用的聚焦 Agent，具有狭窄范围和自己的上下文窗口。 |
| Orchestrator-worker / 编排器-工作器 | "Supervisor pattern" / "监督者模式" | Same thing, different name. The 2026 literature uses both. / 同一事物，不同名称。2026 年文献两者都用。 |
| Fresh context / 清新上下文 | "Clean window" / "干净窗口" | A worker's context starts from its system prompt and assigned question, not the lead's history. / 工作器的上下文从其系统提示和分配的问题开始，而不是主导者的历史。 |
| Rainbow deployment / 彩虹部署 | "Gradual rollout" / "渐进推出" | Long-running stateful agents need versioned drain-and-replace, not blue-green. / 长时间运行的有状态 Agent 需要版本化的排空和替换，而不是蓝绿部署。 |
| Token dominance / Token 主导 | "Context is the variable" / "上下文是变量" | 80% of research-eval variance comes from total tokens used, not model choice, per Anthropic. / 80% 的研究评估方差来自使用的总 token，而不是模型选择，据 Anthropic。 |
| Scale effort / 缩放工作量 | "Match agent count to complexity" / "按复杂度匹配 Agent 数量" | Lead estimates query difficulty, spawns 1 vs 10+ workers accordingly. / 主导者估计查询难度，相应地生成 1 个或 10+ 个工作器。 |
| Synthesis conflict / 综合冲突 | "Workers disagree" / "工作器不一致" | Two workers return contradictory facts; the lead must surface disagreement, not silently pick one. / 两个工作器返回矛盾的事实；主导者必须揭示分歧，而不是静默选择一方。 |

## Daha fazla okumak

- [Anthropic engineering — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) denetim modelinin üretim referansı
  Çinçe Çevirimi:Antropik 工程  我们如何构建多 代理研究系统 监督者模式的生产参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) Araç çağıran denetçi artık önerilen form
  Çinçe Çevirimi:LangGraph 工作流和 Agent  工具调用监督者现在是推的形式
- [LangGraph supervisor reference](https://reference.langchain.com/python/langgraph-supervisor) 2026 üretiminde hala kullanılan miras yardımcı
  中文翻译:LangGraph 监督者参考  旧版助手,仍用于 2026年生产
- [OpenAI cookbook — Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) Transfer tabanlı denetim varianti
  Çinçe Çevirimi:OpenAI 手册  编排 Ajan:例程和交接  基于交接的监督者变体
