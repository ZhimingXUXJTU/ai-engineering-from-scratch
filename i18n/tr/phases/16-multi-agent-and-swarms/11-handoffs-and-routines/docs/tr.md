# Elveriler ve rutinler  İnsansız orkestrasyon 编排 交接 例程 状态

> OpenAI'nin Swarm (Oktyabr 2024) iki primitif'e çoklu ajan orkestrasyonu destil etti: **routines**(elçiye talimatlar + araçlar sistem uyarısı olarak) ve **handoffs**(Bir diğer ajanı geri getiren bir araç). Devlet makinesi yok, DSL'yi branş etmeyin. OpenAI Ajanlar SDK (Mart 2025) üretim varisi. Swarm kendisi en temiz kavramsal referans olarak kalır  tüm kaynağı birkaç yüz satırda yer alır. Şekil viral çünkü API yüzeyi yaklaşık olarak "agent = prompt + tools; handoff = function returning agent".

> **【中文解读】**Bu bölüm, iletişim ve prosedürler hakkında bilgi verir.

> **【拓展：handoffs and routines→具体应用】**交接(Handoffs) is OpenAI Agents SDK'nin temel kavramıdırAgent A kontrolü Ajen B'ye verecek.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前 Lütfen önce bil:Fase 16·04(原语模型)、Fase 14·07(工具调用)。OpenAI Swarm 把多 Agent 简化为2 原语:routine(系统提示+工具)+ hands-off(返回另一个代理的工具)。
>  **【类比】**Handoff = "客服转接"──用户问技术问题→客服 A 接听→判断需要技术支持→转接给技术专员 B。Swarm's天才之处:handoff 就是一个普通工具调用(返回代理),LLM 自动路由──无状态机、无 DSL,几百行代码搞定──OpenAI Agents SDK 是生产版本──

## Sorunlar sorunun giriş

Her multi-agent çerçevesinde DSL'lerini öğrenmenizi ister: LangGraph düğümleri ve kenarları, CrewAI ekipleri ve görevleri, AutoGen GroupChat ve yöneticileri. DSL'ler gerçek soyutlamalardır, ancak bu şeyleri olması gerektiğinden daha ağır hissettirirler.

> Her bir Agent çerçevesinin size DSL'yi öğrenmenizi sağlaması için bir çerçeve vardır: LongGraph'ın nodları ve kenarları; CrewAI'nin ekibi ve görevleri; AutoGen'in GroupChat ve yöneticileri; DSL gerçek bir soyuttur ama bunlar gerçek ihtiyaçlardan daha ağır bir şey hissettirir.

DSL kilitleme, çoklu ajan çerçevesinin vergisi. Her DSL'nin kendi kavramları, kendi hata düzeltme araçları, kendi topluluğu vardır. Bir kere karar verince göç pahalıdır. Swarm'ın bahsi: DSL'yi tamamen atlayın, modelin mevcut araç çağrısını kullanın.

> DSL 锁定是多代理 框架税──每个 DSL有自己的概念──自己的调试工具──自己的社区── once you commit,迁移昂贵──Swarm 的注:完全跳过 DSL,使用模型现有工具调用──

Swarm ters yöne doğru itmektedir: modelin zaten sahip olduğu araç çağrı yeteneğini kullanın. Elveriler araç çağrıları haline gelir. Orkestör şu anda konuşmayı tutan ajandır. Devlet makinesi ajanların sistem isteklerinde iç içindir.

> Swarm 推向相反的方向: modelin mevcut araç kullanma yeteneğini kullanmak.

Bu anlayış derin: bir orkestrasyon DSL'ye ihtiyacınız yok çünkü LLM'ler zaten orkeströrler. Her LLM çağrısı bağlamına göre ne yapılması gerektiğini belirler.

> 洞察深:你不需要编排 DSL,因为 LLM 已经是编排器──每次LLM 调用根据上下文决定下一步做什么──交接只是将该决策暴露为模型可调用工具──

## Konsept merkezi konsept

### İki ilkel

**Routine.**Bir ajanın rolünü ve mevcut araçları belirleyen bir sistem uyarısı. "Sen bir triage ajanısın; kullanıcı geri ödeme hakkında sorarsa geri ödeme ajanına teslim et".

> **例程。**定義 Agent 角色和可用工具的系统提示──把它想象成一组范围化的命令:"Sen bir bölge agentisin; eğer kullanıcı para iadeyi sorarsa, para iadei ajanına iletişime geçin"".

**Handoff.**Swarm çalıştırma süresi, Agent'in geri dönüş değerini algılar ve aktif ajanı bir sonraki dönüş için değiştirir.

> **交接。**Ajanı kullanılabilir araç, yeni bir Ajanı geri göndermek için bir nesneyi kullanmak için.

Bütün soyutlama bu.

> Bu bütün bir ifadedir.

```
def transfer_to_refunds():
    return refund_agent  # Swarm sees Agent return → switch active agent

triage_agent = Agent(
    name="triage",
    instructions="Route the user to the right specialist.",
    functions=[transfer_to_refunds, transfer_to_sales, transfer_to_support],
)
```

Sıralama ajanının sistem istekleri, kullanıcı mesajına göre doğru teslimatı seçmesini sağlar. LLM'nin araç çağrısı yönlendirme yapar.

> 分诊 代理的系统提示使其根据用户消息选择正确的交接.

Bu zarif bir hareket: modelin mevcut araç çağrı altyapısını orkestrasyon için yeniden kullanmak. Yeni DSL, grafik düzenleyicisi, devlet makinesi yok. Model zaten doğru aracı nasıl seçileceğini biliyor; teslimatlar sadece geri gönderme ajanları aracıdır.

> Bu, güzel bir girişimdir: modelin mevcut araçlarını yeniden kullanmak, altyapıyı düzenlemek için düzenlemek. Yeni DSL yok, resim düzenleyicisi yok, durum makinesi yok.

### Neden viral?

- **Small API.**Öğrenmek için iki kavram var.
  Çeviri:**小型 API。**Sadece iki kavramı öğrenmek zorundayım.
- **Uses what the model already does.**Araç çağrısı zaten tedarikçiler arasında üretim derecesindedir.
  Çeviri:**使用模型已有的能力。**Her türlü tedarikçi arasında kullanılan araçlar üretim aşamasındadır.
- **No state-machine burden.**Grafiği tanımlamazsın, ajanların istekleri kime teslim ettiklerini anlatır.
  Çeviri:**无状态机负担。**Sen resimleri anlatmazsın. Ajanın tavsiyeleri onları kimlere gönderdiğini anlatır.

### Ülkesiz ticaret

Swarm, çalışmalar arasında açıkça devletsizdir. Çerçeve bir çalışmalar sırasında bir mesaj tarihi tutar, ancak hiçbir şey kalmaz. Hatıra, süreklilik, uzun süreli görevler  tüm arayanın sorunu.

> Swarm, çalışmalar arasında gerçek anlamda durumsuz bir sistemdir. Çerçeve, çalışmalar sırasında haber tarihi tutmak için geçerlidir, ancak hiçbir şeyi sürdürmez.

Devletsiz tasarım kasıtlıdır: çerçeveyi önemsiz olarak yeniden başlatabilir, uzaylı olarak ölçeklenebilir ve hata çözülebilir hale getirir (her çalıştırma bağımsızdır).

> 无状态设计是有意的: framework can easily restart ̇水平扩展和调试 ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇

Üretim (OpenAI Agents SDK, Mart 2025) bu değişen ana şeylerden biriydi: SDK, teslimatın ilkel tutulduğu halde, yerleşik oturum yönetimi, koruma rayları ve izleme ekler.

> Bu, temel değişikliklerden biridir: SDK, içeride konuşma yönetimi, koruma ve takip ekledi, aynı zamanda iletişimini korudu.

### Swarm/Handoffs uygun olduğunda

- **Triage patterns.**Ön hattı ajanı, kullanıcıyı uzmanlara yönlendirir.
  Çeviri:**分诊模式。**Önceki Ajan kullanıcıyu uzmanlara yönlendirecek.
- **Skill-based handoffs.**"Eğer görev için kod gerekiyorsa kodleyicisi arayın; araştırma gerekiyorsa araştırmacıyı arayın".
  Çeviri:**基于技能的交接。**"Eğer görevler kodlama gerekiyorsa, kodlayıcıyı kullanın; eğer araştırma gerekiyorsa, araştırmacıyı kullanın".
- **Short, bounded conversations.**Müşteri desteği, FAQ-to-ticket, basit iş akışları.
  Çeviri:**短、有界对话。**客户支持、FAQ到工单、简单工作流──

### Swarm'ın mücadele ettiği zaman

- **Long sessions with shared memory.**Handoffs, konuşma durumunu yeni ajanın istek artı geçmişine geri koymuştur.
  Çeviri:**需要共享内存的长会话。**交接将对话状态重置为新代理的提示加历史――调用者管理的内存就没有跨代理的持久状态――
- **Parallel execution.**Handoff, aktif ajanın bir seferde  anahtarlarıdır. Paralelism, arayanın birden fazla Swarm çalışmasını orkestralamasını gerektirir.
  Çeviri:**并行执行。**交接是逐一的活动 交换――并行性需要调用者编排多个 Swarm 运行――
- **Audit and replay.**Devletsiz koşular tam olarak tekrarlanması zordur; LLM'nin teslimat seçimi belirlenmez.
  Çeviri:**审计和回放。**无状态运行难以精确回放;LLM'nin bağlantı seçimi kesin değildir.

### OpenAI Ajanlar SDK (Mart 2025)

Üretim varisi şunları ekliyor:

> 生产继任者添加了:

- **Session state.**Çekilenler arasında sürekli bir iplik.
  Çeviri:**会话状态。**跨运行的持久线程──
- **Guardrails.**Giriş/çıktı doğrulama kaçağı.
  Çeviri:**防护栏。**输入/输出验证子。
- **Tracing.**Her araç çağrısı ve teslimatı kayıtlıdır.
  Çeviri:**追踪。**Her araç kullanımı ve bağlantısı kaydedilmiştir.
- **Handoff filters.**Ne bağlamı transfer ettiğini kontrol et.
  Çeviri:**交接过滤器。**Kontrol et iletişim zamanı 传输 什么上下文──

Elverme ilkeleri hayatta kalır; üretim ergonomikleri etrafında eklenir.

> 交接原语存活下来;生产人体工程学周围添加──

Bu, virüs soyutlamaları için standart ilerleme: basit ilkel gemiler önce (Swarm), üretim üst katmanlarla ilgilidir (Agent SDK).

> Bu, viral 抽象 的标准进展:先发布简单原语(Swarm),生产关注点在其上层叠上(Agent SDK) ・・・原语保持稳定;包装器增长──押注原语──

### Swarm vs GroupChat

Her ikisi de LLM yönlendirme kullanır, ancak farklılıkları var **who picks next**- ...

>                                                                                                                                                                                                                                                               **谁选择下一个**上不同:

- Grup Çat: bir seçiciler (fonksiyon veya LLM) sonraki konuşmayı dışarıdan seçer.
  中文翻译:GroupChat:选择器(函数或 LLM) dıştan seçmek下一个发言者──
- Swarm: mevcut ajan, bir teslim aracı çağırarak halefini seçer.
  Çeviri:Swarm:当前 Agent 通过调用交接工具选择其继任者──

Swarm "Agent neyin bir sonraki kararını verir"; GroupChat "menedjer neyin bir sonraki kararını verir". Swarm'ın kararı aktif ajanın araç çağrısında yaşar; GroupChat'ın hayatı `GroupChatManager`- Evet .

> Swarm "Agent Decides Next Step" dir; GroupChat "Administrator Decides Next Step" dir. Swarm'ın kararları etkinlik ajanının araçları içinde mevcuttur; GroupChat'ın mevcuttur.`GroupChatManager`İçeride.

Pratik anlamı: Swarm, hapsedilmesi daha kolay (aktif ajanın araç çağrılarını takip edin), ancak kısıtlamak daha zor (herhangi bir ajan her yerde teslim edebilir). GroupChat tam tersi: kısıtlamak kolay (seçici işlevi kural eklemek için bir yer), hapsedilmesi daha zor (seçici mantığı açık olmayabilir).

> 实际影响:Swarm 更容易调试(跟踪活动 代理的工具调用) fakat daha güçlükle 调束(Herhangi bir ajan herhangi bir yerde iletişim kurabilir) ――GroupChat 相反:容易约束(选择器函数是添加规则的一个地方),更难调试(选择器的逻辑可能不透明)。

## Yapın.
```figure
sw-handoff-routing
```

## Yapın

`code/main.py`Swarm'i sıfırdan uyguluyor: Bir ajan veri sınıfı, bir teslim mekanizması (üçüm geri verir ajan), ve ajan anahtarlarını algılayan bir çalıştırma döngüsü.

> `code/main.py`Swarm:Agent 数据类、交接机 (Agent return tools)

Demo: bir triage ajanı geri ödeme, satış veya destek uzmanları için yollar. Her uzmanın kendi araçları vardır.

> 演示:分诊 路由到退款、销售或支持专家──每个专家都有自己的工具──运行循环印每次交交──

Çık:

```
python3 code/main.py
```

## Çerçeveyi kullanın.

`outputs/skill-handoff-designer.md`Bu, belirli bir görev için bir transfer topolojisini tasarlar: hangi ajanlar var, hangi transferleri çağırabilirler, hangi bağlamı aktarır.

> `outputs/skill-handoff-designer.md`Görev tasarımında bağlantılama: hangi ajanlar var, hangi bağlantıları kullanabilirler, neyi üst üst düzeylerde aktarırlar.

## İndirin . Ürünler .

Kontrol listesini:

> 检查清单:

- **Handoff logging.**Her teslimat bir olayı izler ve ajanlardan ajanlara bağlamlı bir anlık görüntüler yazır.
  Çeviri:**交接日志。**Her bağlantı, takip olayı içerir.
- **Context transfer rules.**Neyi taşıyacağınızı belirleyin: tam geçmiş (maliyet), son N mesajları veya bir özet.
  Çeviri:**上下文传输规则。**Bu yüzden, bu konuda bir karar vermeyelim.
- **Guardrail on handoff.**Farklı araç yetkileri olan bir uzmanın teslimatı doğrulanmalıdır  aksi takdirde hızlı enjeksiyon istenmeyen teslimatları zorlayabilir.
  Çeviri:**交接防护栏。**交接到具有不同工具权限的专家必须得到认证 否则提示注入可以强制不需要的交接──
- **Loop detection.**İki ajan ileri geri dönerken ortak bir başarısızlık olur. Son K yüzük kontrolü ile tespit edilir.
  Çeviri:**循环检测。**İki ajan tekrar görüşmek için bir başarı yok.
- **Fallback agent.**Eğer bir teslim hedef mevcut değilse, güvenli bir özürlüğe geri dönün.
  Çeviri:**后备 Agent。**Eğer bir bağlantı hedefi yoksa, güvenlik öntanımlı değerine geri dön.

## Egzersizler.

1. Çık .`code/main.py`İkinci turun aktif ajanının geri ödeme yapıldığını onaylayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`,分诊到退款代理──确认第二轮活动代理──退款──
2. Bir döngü tespit kuralı ekleyin: Aynı iki ajan üç kez sırayla teslim olduysa, çıkış zorlayın.
   Çin Çeviri: Ek döngü kontrol kuralları: Eğer aynı iki Ajan 连续交接 3 kez,强制退出──设计后备方案──
3. OpenAI Agents SDK dosyalarını teslimat filtreleri üzerine okuyun. "Handov-on-Handoff" sürümünü uygulayın: giden ajan, gelen ajanın devralmasından önce bağlamı bir mermi özetine sıkıştırır.
   Çinçe Çevirim: OpenAI Ajanlar SDK 关于交接过器的文档──实现"交接时总结" versiyonu:传出 Agent 在传入 Agent 接管之前将上下文缩为要点摘要──
4. Swarm'ın teslimatını GroupChatManager seçicisi ile karşılaştırın. Hangi desen hızlı enjeksiyonu kötüleştirir ve neden?
   Çeviri: Swarm 交接与 GroupChatManager 选择器── hangi model önerileri daha kötü hale getiriyor, neden?
5. Swarm'ın bir açık tasarım kararı belirleyin. Swarm OpenAI Ajanları SDK'sinin değiştirildiğini veya korunulduğunu yapar.
   Çeviri: Swarm 手册, Swarm Yapılan bir açık tasarım karar, OpenAI Ajanları SDK  değiştirmek veya korumak için.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Routine / 例程 | "The agent prompt" / "Agent 提示" | System prompt + tool list. Defines role and available handoffs. / 系统提示 + 工具列表。定义角色和可用交接。 |
| Handoff / 交接 | "Transfer to another agent" / "转移到另一个 Agent" | A tool the active agent can call that returns a new Agent. The runtime switches active agent. / 活动 Agent 可以调用的工具，返回新 Agent。运行时切换活动 Agent。 |
| Stateless / 无状态 | "No memory between runs" / "运行间无记忆" | Swarm does not persist anything; memory is the caller's responsibility. / Swarm 不持久化任何东西；内存是调用者的责任。 |
| Active agent / 活动 Agent | "Who's speaking now" / "现在谁在说话" | The agent currently holding the conversation. Handoff changes this. / 当前持有对话的 Agent。交接改变这个。 |
| Context transfer / 上下文传输 | "What moves on handoff" / "交接时传输什么" | Policy for what history the incoming agent sees: full, last N, or summarized. / 传入 Agent 看到什么历史的策略：完整、最后 N 条或摘要。 |
| Handoff loop / 交接循环 | "Agents ping-pong" / "Agent 乒乓" | Failure mode where two agents keep handing back to each other. / 两个 Agent 持续互相交接的失败模式。 |
| OpenAI Agents SDK | "Production Swarm" / "生产 Swarm" | March 2025 successor; adds sessions, guardrails, tracing on top of the handoff primitive. / 2025 年 3 月继任者；在交接原语之上添加会话、防护栏、追踪。 |
| Handoff filter / 交接过滤器 | "Gate on transfer" / "传输门" | SDK feature to inspect and modify context at the handoff boundary. / 在交接边界检查和修改上下文的 SDK 特性。 |

## Daha fazla okumak

- [OpenAI cookbook — Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) Referans kelime
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [OpenAI Swarm repo](https://github.com/openai/swarm) orijinal uygulanma, kavramsal referans olarak saklanır
  Çeviri:OpenAI Swarm  deposu  原始实现,保留为概念参考
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) Sessiyon ve izleme ile üretim halefi
  Çinçe Çevirimi:OpenAI Ajanları SDK 文档  带会话和追踪的生产继任者
- [Anthropic handoff-in-Claude notes](https://docs.anthropic.com/en/docs/claude-code) Claude Code alt üyeleri nasıl bir teslimat biçimi kullanıyor `Task`
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`Task`Kullanımlı iletişim modeli
