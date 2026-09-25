# Agent Framework Tradeoffs  LangGraph vs CrewAI vs AutoGen vs Agno  Agent Framework vs LangGraph vs CrewAI vs AutoGen vs Agno
# Ajan Çerçeve İşlemleri  Grafi, Rol ve Oyuncu Orkestrasyonu

> Her çerçeve aynı demoyu satar ( Araştırma ajanı bir rapor oluşturur) ve aynı hataları saklar (devlet şeması orkestrasyon katmanı ile savaşır).

> **【中文解读】**Her çerçeve aynı demoyu gösterir, aynı hataları gizler, durum şeması ve düzenlemeler arasında çatışmalar.

> **【拓展：框架选择→Agent工程实践】**LangGraph                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

>  **【前置】**Önemli olan, bu süreçte, en iyi şekilde kullanılan iki 个 (LangGraph, CrewAI, AutoGen, Agno) ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ 

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 16 (LangGraph) | **前置知识:** Phase 11 · 09 (函数调用)、16 (LangGraph)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Bir LLM çağrısı gereken bir göreviniz var. Belki bir araştırma iş akışı (plan, arama, özet, alıntı) olabilir. Belki bir kod inceleme boru hattı (parse diff, critic, patch, validate) olabilir. Belki de uçuşları kitaplayan, e-postalar yazar ve harcama raporlarını dosyalayan bir çok dönüş asistanıdır. Bir çerçeve seçersiniz.

> Bir çok LLM 调用任务──也许是研究工作流 (?? ), belki de bir çerçeve seçmiş olursun.

Üç gün sonra, çerçevenin soyutlama sızdırmalarını keşfedersiniz. CrewAI size roller verir ama " araştırmacı " ' yazıcı " 'ya yapılandırılmış bir plan vermek zorunda kaldığında size savaşır. AutoGen size ajanlar arasında sohbet verir ama birinci sınıf bir durum yoktur. LangGraph size bir devlet grafikini verir ama ajanın ne yapacağını bilmeden önce her geçişin adını vermenizi zorlar. Agno size üç eş zamanlı işçiye yaymaya çalıştığınızda çığlık atan tek ajan bir soyutlama yapar.

> Üç gün sonra, çerçeveye bir soyutlama sızdırdığını görürsün. CrewAI'nin sana bir rol vermesi, ama "daha çalışkan"ın yapılandırma planını "yazar"a vermesi gerektiğinde sorun çıkaracaktır.

Bu çözüm "en iyi çerçeveyi seç" değil. Bu çerçevenin temel soyutlamasını sorunun şekliyle eşleştirmektir. Bu ders bu haritayı çizer.

> Düzeltme yöntemi "en iyi çerçeveyi seçmek" değil, çerçevenin çekirdeği çekimsel olarak sorunun şekliyle uyumlu hale getirilmesi.


> **【中文解读】**Agent 框架选型的三个维度:(1) 任务复杂度简单 RAG 用LlamaIndex,复杂 Agent 用LangGraph;(2) 团队经验新手用LangChain 模板,专家用原生API;(3) 生产要求需要LangSmith 集成选LangChain 生态──

>  **【类比】**选 Agent 框架像选交通工具短途买菜用自行车(stdlib + function calling),跨城出差用车(LangGraph 状态机),多人旅行用面包车(CrewAI 角色),即时通讯用电话(AutoGen 对话) ・・・

> ️ **【易错点】**框架选错的 3 个常见原因:(1) **跟风最热门**AutoGen 火就上 AutoGen,结果发现任务只是单 Agent + 工具,过度工程;先评估任务复杂度再选框架――(2) **被 demo 误导**CrewAI'nin " Araştırmacı + yazar " demosu çok güzel görünüyor, ancak gerçek görevdeki rol sınırları bulanık,CrewAI'nin rolü çekimleri tersine çekilmiştir; önce yap PoC 验证抽象匹配──(3) **低估迁移成本** Agno'yu kullanmaya başlayın 简单,后期要增加 时发现 Agno不支持,重写到 LangGraph 花两周;选框架时看 6 个月后的需求──


## Konsepten bir şey.

> **【中文解读】**Agent  framework                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

> **【拓展：Agent 框架的选型指南】**选型维度:(1) 任务复杂度(简单 RAG 用 LlamaIndex,复杂 Agent 用 LangGraph);(2) 团队经验(新手用 LangChain 模板,专家用原生 API);(3) 生产要求(LangSmith 集成选 LangChain 生态) ・2025 yılın eğilimleri framework lightweight化。


![Agent framework matrix: core abstraction vs problem shape](../assets/framework-matrix.svg)

2026 manzarasında dört çerçeve hakimdir. Temel soyutlamaları aynı değil.

> 4 çerçeve 2026 yılının yapısını yönlendiriyor.

| Framework | Core abstraction | Best fit | Worst fit |
|-----------|------------------|----------|-----------|
| **LangGraph** | `StateGraph` — typed state, nodes, conditional edges, checkpointer. | Workflows with explicit state and human-in-the-loop interrupts; production agents needing time-travel debugging. | Loose, role-driven brainstorming where the topology is unknown. |
| **CrewAI** | `Crew` — roles (goal, backstory), tasks, process (sequential or hierarchical). | Role-playing or persona-driven workflows with a short linear/hierarchical plan. | Anything stateful beyond the crew's turn history; complex branching. |
| **AutoGen** | `ConversableAgent` pair — two or more agents that speak in turns until an exit condition. | Multi-agent *dialogue* (teacher-student, proposer-critic, actor-reviewer) where the thinking emerges from the chat. | Deterministic workflows with a known DAG; anything needing durable state across restarts. |
| **Agno** | `Agent` — a single LLM + tools + memory, composable into teams. | Fast-to-build single agents and lightweight teams; strong multi-modality and built-in storage drivers. | Deep, explicitly-branched graphs with custom reducers. |

### "Abstraksiyon"un anlamı ne?

Bir çerçevenin temel soyutlama, mimariyi ortaya çıkarırken tahtaya çizdiğiniz şeydir.

> Çerçeve'nin çekirdeği, bir yapı satırken beyaz levha üzerinde çizdiğin bir şeydir.

- **LangGraph**→ bir grafik çizersiniz. düğümler adımlardır, kenarlar geçişlerdir ve her noktada durum nesnesi yazılır.
  Sen bir resim çizdin. Bütçe bir adım, bir dönüşüm.
- **CrewAI**→ bir organ tablosu çizersiniz. her rolün bir iş açıklaması vardır ve bir yöneticisi görevleri yönlendirir.
  Bir organizasyon çizersiniz. Her rolün bir sorumluluk, bir görev yöneticisi vardır.
- **AutoGen**İki ajan birbirine mesaj gönderir, bir üçüncü moderatöre ihtiyacınız varsa katılır.
  Bir Slack, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki ajan, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi, iki kişi
- **Agno**Bir takım için bir kenara kutular koyun. Zihinsel model "batarya dahil bir ajan"tır.
  Sen bir araç çerçevesini çizdin.

### Devlet sorusu

Çoğu çerçeve seçeneğinin üretimde bozulduğu yer devlet.

> 状态是大多数框架选择在生产中出问题的地方──

- **LangGraph.**Tiplenmiş durum (`TypedDict`Bu nedenle, bu süreçte, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre, bir süre sonra, bir süre, bir süre sonra, bir süre sonra, bir süre, bir süre, bir süre sonra, bir süre sonra, bir süre, bir süre, bir süre, bir süre sonra, bir süre, bir süre, bir süre sonra, bir süre, bir süre, bir süre, bir süre sonra, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir sürececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece
  **LangGraph。**类型化状态`TypedDict`veya Pydantic 模型) 、每字段 reducer、一等公民检查点器(SQLite/Postgres/Redis) ⋅恢复、中断和时间旅行免费──(见 Fase 11 · 16──)
- **CrewAI.**Devlet akışları görevler arasındaki bir dizi olarak `context`alanı veya `output_pydantic`- Ekibe başına dayanıklı bir depo yok, eğer eskizlerin yeniden başlatılmasını sağlayacaksa kendi başına gidersin.
  **CrewAI。**状态作为字符串在任务间通过 `context`字段流动, veya `output_pydantic`struktur化──開箱無持久每人乗組員 存儲; 若乗組員 必須生存再開始自外挂──
- **AutoGen.**Durum sohbet geçmişi ve kullanıcı tarafından tanımlanan herhangi bir durumdur `context`. Konuşma transkriptleri kalır; adaptörler yazmadıkça keyfi çalışma akışı durumu olmaz.
  **AutoGen。** durumu chat tarihi ve herhangi bir kullanıcı tanımlı `context` dialog record persistence; arbitrary work flow state does not persistence, unless written adaptation 
- **Agno.**Bir    ile bağlanan yerleşik depolama sürücüleri (SQLite, Postgres, Mongo, Redis, DynamoDB)`Agent`-`storage=` sohbet seansları ve kullanıcı hatıraları otomatik olarak kalır.
  **Agno。**İçeride depolama gücü (SQLite, Postgres, Mongo, Redis, DynamoDB)`storage=`- Evet .`Agent`Ü sohbet konuşması ve kullanıcı hafızası otomatik olarak kalıcılaştırılmaktadır.

- **LangGraph.**Tiplenmiş durum (`TypedDict`Bu nedenle, bu süreçte, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre, bir süre sonra, bir süre, bir süre sonra, bir süre sonra, bir süre, bir süre, bir süre sonra, bir süre sonra, bir süre, bir süre, bir süre, bir süre sonra, bir süre, bir süre, bir süre sonra, bir süre, bir süre, bir süre, bir süre sonra, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir sürececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece
- **CrewAI.**Devlet akışları görevler arasındaki bir dizi olarak `context`alanı veya `output_pydantic`- Ekibe başına dayanıklı bir depo yok, eğer eskizlerin yeniden başlatılmasını sağlayacaksa kendi başına gidersin.
- **AutoGen.**Durum sohbet geçmişi ve kullanıcı tarafından tanımlanan herhangi bir durumdur `context`. Konuşma transkriptleri kalır; adaptörler yazmadıkça keyfi çalışma akışı durumu olmaz.
- **Agno.**Bir    ile bağlanan yerleşik depolama sürücüleri (SQLite, Postgres, Mongo, Redis, DynamoDB)`Agent`-`storage=` sohbet seansları ve kullanıcı hatıraları otomatik olarak kalır.

### Şekil sorusu

Her küçük bir ajanın şubesi, şubenin meselelerini kim karar verir.

> Her sıradışı ajanın bir bölümü vardır.

- **LangGraph** koşullu kenarlar üzerinden karar verirsiniz. Routing, isimli dallarla bir Python fonksiyonu. Şubeler oluşturulan grafikte birinci sınıf; kontrol noktası hangi şubenin alınmış olduğunu kaydeder.
  **LangGraph**你决定,通过条件边──路由是带命名分支的 Python 函数──分支是编译图中的一等公民;检查点器记录走哪条──
- **CrewAI** yöneticinin hiyerarşik modunda karar vermesi; sıralı modda oluşturma zamanında karar vermesi. Routing görev listesinde içindir; yöneticinin isteklendirilmesinden başka birinci sınıf "eğer" yoktur.
  **CrewAI**分层模式由经理决定;顺序模式你在构建时决定──路由隐含在任务列表中;经理提示外无一等公民"if"──
- **AutoGen**-Agentler sohbet yoluyla karar verir.`GroupChatManager`bir sonraki konuşmacı seçer; bir `speaker_selection_method`Ama standart, LLM ile yönlendirilir.
  **AutoGen**Agent 通過聊天決定──分支從誰下一個說話中涌现──`GroupChatManager`选下一个发言人;可手写 `speaker_selection_method`Ama kabul edilen LLM'yi kullanıyorum.
- **Agno** ajan, hangi aracı kullanıp bir sonraki çağrıda bulunacağını belirler.
  **Agno**Agent 通過下一個调用哪个工具决定──团队有协调员/路由器/合作者模式; dışında分支由开发者负责──

- **LangGraph** koşullu kenarlar üzerinden karar verirsiniz. Routing, isimli dallarla bir Python fonksiyonu. Şubeler oluşturulan grafikte birinci sınıf; kontrol noktası hangi şubenin alınmış olduğunu kaydeder.
- **CrewAI** yöneticinin hiyerarşik modunda karar vermesi; sıralı modda oluşturma zamanında karar vermesi. Routing görev listesinde içindir; yöneticinin isteklendirilmesinden başka birinci sınıf "eğer" yoktur.
- **AutoGen**-Agentler sohbet yoluyla karar verir.`GroupChatManager`bir sonraki konuşmacı seçer; bir `speaker_selection_method`Ama standart, LLM ile yönlendirilir.
- **Agno** ajan, hangi aracı kullanıp bir sonraki çağrıda bulunacağını belirler.

### Gözlemsellik sorusu

> Görüşme sorunları

- **LangGraph** LangSmith veya herhangi bir OTel ihracatçısı üzerinden OpenTelemetry. Her düğüm geçimi bir iz uzadıdır; kontrol noktaları tekrarlanabilir izler olarak ikiye katlanır. LangSmith ilk taraf seçeneğidir; Langfuse / Phoenix'in de adaptörleri vardır.
  **LangGraph** LangSmith veya herhangi bir OTel 导出器'ın OpenTelemetry üzerinden。 her bir noktayı dönüştürmek bir iz aralığıdır;检查点兼作重放追踪。 LangSmith ilk seçeneği; Langfuse/Phoenix ayrıca adapte cihazı vardır。
- **CrewAI** 2025 sonlarından itibaren birinci sınıf OpenTelemetry; Langfuse, Phoenix, Opik, AgentOps ile entegrasyonlar.
  **CrewAI**2025 yıl sonu 1.等公民 OpenTelemetry;集成 Langfuse、Phoenix、Opik、AgentOps。
- **AutoGen** OpenTelemetry'nin entegrasyonu üzerinden `autogen-core`AgentOps ve Opik'in bağlantıları var.
  **AutoGen**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `autogen-core`Bu, bir diğer diğer yöntemdir.
- **Agno** İçeriye yerleştirilmiş `monitoring=True`Bayrak ve OpenTelemetry ihracatçıları; seans izleri için Langfuse ile sıkı bir entegrasyon.
  **Agno**内置 `monitoring=True`标志加 OpenTelemetry 导出器;与 Langfuse 紧密集成会话追踪──

### Masraf ve gecikme

Tüm dört çerçeve, arama başına genel maliyet ( çerçeve mantığı, doğrulama, serileştirme) ekler. Genel maliyetin artması için kaba bir sırayla: Agno ≈ LangGraph < CrewAI ≈ AutoGen. Fark, çerçeveye ne kadar fazladan LLM yönlendirme yapması ile baskınlaşır. CrewAI'nin hiyerarşik yöneticisi, kimlerin sonraki olduğuna karar vermek için jetonlar harcar.`GroupChatManager`LangGraph'in de sadece yazıp verdiğin tokenleri harcayacağı yer.`llm.invoke`Agno'nun tek ajan yolu ince.

> Dört çerçeve her bir çalışma için artar.

Bir koşu başına maliyet önemli olduğunda açık yönlendirmeyi tercih edin (LangGraph kenarları, AutoGen `speaker_selection_method`) ile LLM seçilen yönlendirme.

> Her seferinde çalışma maliyeti önemli olduğunda, öncelikli olarak açık yolu kullanmak yerine LLM seçme yolu kullanmak gerekir.

### İşbirliği

> 互操作性

- **LangGraph** **LangChain**MCP sunucu olarak ithal edilen araçlar, retrievers, LLMs. Birinci sınıf MCP adaptörü.
  **LangGraph** **LangChain**工具、检索器、LLM──一等公民 MCP 适配器(工具作为 MCP 服务器导入)
- **CrewAI** araçlardan miras alınan araçlar `BaseTool`LangChain araçları, LlamaIndex araçları ve MCP araçları hepsi uyum sağlar.`allow_delegation=True`- Evet .
  **CrewAI** 工具继承自 `BaseTool`LongChain 工具、LlamaIndex 工具、MCP 工具都适配进来──crew-to-crew 委派通过`allow_delegation=True`- Evet.
- **AutoGen**→ `FunctionTool`Python'un çağrılabilir tüm programlarını kapsıyor, MCP adaptörü mevcut.
  **AutoGen**→ `FunctionTool`包装任何Python可调用;MCP 适配器可用──与AG2 生态紧密合用于代理 间模式──
- **Agno**→ `@tool`dekorasyon veya BaseTool alt sınıfı; MCP adaptörü; araçlar ajanlar ve ekipler arasında paylaşılabilir.
  **Agno**→ `@tool`装饰器或 BaseTool 子类;MCP 适配器;工具可跨 Agent 和团队共享──

## Yetenek

> Bir cümleyle, belirli bir çerçeveyi belirli bir ajan sorunu için neden doğru olduğunu açıklayabilirsiniz.
> Bir Ajanın sorunu için bir çerçeve neden uygun olduğunu bir cümleyle açıklayabilirsin.

Öntanımlı kontrol listesi:

> 构建前检查清单:

1. **Draw the shape.**Bu bir grafik mi (tipileşmiş durum, isimlendirilmiş geçişler)? Rol oyunu (özeller işten vazgeçti)?
   **画出形状。**Bu bir oyun mu, bir sohbet mi, yoksa bir araçla çalışan bir ajan mı?
2. **Decide who branches.**Geliştiriciler tarafından belirlenen dalgalama → LangGraph. Yöneticiler tarafından belirlenen ajanlar tarafından belirlenen personeller → CrewAI hiyerarşik. Çat-yönemli → AutoGen. Araç-sağlama-verilen kararlar → Agno.
   **决定谁分支。**开发者决定 → LangGraph──经理 Agent决定 → CrewAI──聊天涌现 → AutoGen──工具调用决定 → Agno──
3. **Check the state budget.**Kontrol noktasından devam etmeniz gerekiyor mu? Zaman yolculuğu? İnsan çalışmanın ortasında keser mi? Evetse, LangGraph varsayılan; Agno seansları konuşma ölçekli durumları kapsar.
   **检查状态预算。**Kontrol noktasından geri dönmek mi gerekiyor?
4. **Check the cost budget.**LLM'nin seçtiği yönlendirme, her turda ekstra token ödemektedir.
   **检查成本预算。**LLM 选择的路由每轮额外消耗代币──
5. **Budget the framework overhead.**Her çerçeve başka bir bağımlılıktır. Eğer görev iki LLM çağrısı ve bir araç ise, basit Python'un 30 satırı yazın; hiçbir çerçeve hiçbir çerçeveden daha ucuz değildir.
   **预算框架开销。**Her çerçeve bir diğerine bağlıdır. Eğer görev sadece iki kez bir LLM'yi kullanırsanız, 30 adet saf Python yazın.

Grafiği, organ grafikini, sohbet yapmayı ya da ajan kutusunu çizmeden önce bir çerçeveye ulaşmayı reddet.

> Çizim yapmadan önce, bir çerçeveye el uzatma, bir düzenleme yapmadan önce, bir şey seçme, bu seni dövüşmeye zorlayacak bir şey seçme.

## Karar Matrisi

| Problem shape | Preferred framework | Why |
|---------------|---------------------|-----|
| Workflow DAG with typed state, human approvals, long-running | LangGraph | First-class state, checkpointer, interrupts, time-travel. |
| Research / writing pipeline with distinct roles | CrewAI (sequential) or LangGraph subgraphs | Role-per-task is cheap to express in CrewAI; scale up with LangGraph when branching gets complex. |
| Proposer-critic or teacher-student dialogue | AutoGen | Two-agent chat is its native shape. |
| Single agent with tools, sessions, memory | Agno | Thinnest setup, built-in storage and memory. |
| Thousands of parallel fanouts with reducers | LangGraph + `Send` | The only one with a first-class parallel-dispatch API. |
| Quick prototype, no framework commitment | Plain Python + provider SDK | No framework is the fastest framework. |

| 问题形状 | 推荐框架 | 原因 |
|---------|---------|------|
| 类型化状态的工作流 DAG、人工审批、长期运行 | LangGraph | 一等公民状态、检查点、中断、时间旅行 |
| 研究写作流水线带不同角色 | CrewAI（顺序）或 LangGraph 子图 | CrewAI 表达每任务角色便宜；分支复杂时用 LangGraph |
| 提议者-评论者或师生对话 | AutoGen | 双 Agent 聊天是其原生形状 |
| 单 Agent 带工具、会话、记忆 | Agno | 最薄设置，内置存储和记忆 |
| 数千并行扇出带 reducer | LangGraph + `Send` | 唯一带一等公民并行分派 API 的 |
| 快速原型、不绑定框架 | 纯 Python + 提供商 SDK | 无框架是最快的框架 |

## Egzersizler.
```figure
l5-framework-fit
```

## Egzersizler

1. **Easy.**Aynı görevi  "Anthropic'in merkez merkezini araştırın, 200 kelimelik bir kısaca yazın, kaynakları alıntılayın"  ve LangGraph'te (dört düğüm: plan, arama, yazma, alıntı) ve CrewAI'de (üç rol: araştırmacı, yazar, editör) uygulayın.
   LangGraph ve CrewAI'de gerçekleştirilen aynı görevle, her çalışmanın simgesi, kod ve yapı sayısı rapor edilmektedir.
2. **Medium.**Aynı görevi AutoGen'de oluşturun ( araştırmacı  yazar sohbet, editör üzerinden katılır `GroupChat`) ve Agno (tek bir ajanla birlikte)`search_tools`ve `write_tools`Dört uygulamayı a) her koşuşturma maliyetine, b) bir kaza sonrası yeniden başlatma yeteneğine, c) yazma aşamasından önce insan onayını enjekte etme yeteneğine göre sıralayın.
   AutoGen ve Agno'da aynı görevi gerçekleştirmek, maliyetlere göre  çöküş geri kazanma kapasitesi  yapay onaylı enjeksiyon kapasitesi sıralaması
3. **Hard.**Karar ağacı metni oluştur `pick_framework.py`Bu kısa bir sorun açıklaması (JSON: `{has_typed_state, has_roles, has_dialogue, has_parallel_fanout, needs_resume}`) ve bir cümleyle bir tavsiye ile bir tembih gönderir.
   构建决策树脚本,问题描述根据回归框架推──

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Orchestration | "How the agents coordinate" / "Agent 如何协调" | The layer that decides which node/role/agent runs next. | 编排：决定哪个节点/角色/Agent 下一步运行的层 |
| Durable state | "Resume after a restart" / "重启后恢复" | State that survives process death, attached to a checkpoint or session store. | 持久状态：在进程终止后仍存活的状态 |
| LLM-selected routing | "Let the model decide" / "让模型决定" | A planner LLM picks the next step each turn; flexible but pays tokens on every decision. | LLM 选择路由：规划 LLM 每轮选择下一步 |
| Explicit routing | "Developer decides" / "开发者决定" | A Python function or static edge picks the next step; cheap and auditable. | 显式路由：Python 函数或静态边选择下一步 |
| Crew | "A CrewAI team" / "CrewAI 团队" | Roles + tasks + process (sequential or hierarchical) bound into a single runnable. | Crew：角色+任务+流程绑定成一个可运行单元 |
| GroupChat | "AutoGen's multi-agent chat" / "AutoGen 多 Agent 聊天" | A managed conversation between N agents with a speaker selector. | GroupChat：N 个 Agent 之间的托管对话 |
| Team (Agno) | "Multi-agent Agno" / "多 Agent Agno" | Route / coordinate / collaborate mode over a set of agents. | Team (Agno)：Agent 集合上的路由/协调/协作模式 |
| StateGraph | "LangGraph's graph" / "LangGraph 图" | Typed-state, node, conditional-edge, checkpointer abstraction. | StateGraph：类型化状态、节点、条件边、检查点抽象 |

## Daha fazla okumak

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) StateGraph, kontrol noktaları, kesintiler, zaman yolculuğu.
  LangGraph 文档StateGraph、检查点、中断、时间旅行──
- [CrewAI documentation](https://docs.crewai.com/) Ekipleri, Akışlar, Ajanlar, Görevler, İşlemler.
  CrewAI 文档 Crew、Flow、Agent、Task、Process──
- [AutoGen documentation](https://microsoft.github.io/autogen/) KonuşılabilirAgent, Grup Çat, takımlar, araçlar.
  AutoGen 文档ConversableAgent、GroupChat、teams、tools。
- [Agno documentation](https://docs.agno.com/)- Ajan, takım, iş akışı, depolama, hafıza.
  Agno 文档Agent、Team、Workflow、storage、memory。
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) Şablon kütüphanesi (sürekli zincirleme, yönlendirme, paralelleştirme, orkestrasyon-işçiler, değerlendirici-optimalisyen) çerçeve-agnostik.
  Antropik  About Constructing Valiant Agent's Model Library, çerçeve
- [Yao et al., "ReAct: Synergizing Reasoning and Acting" (ICLR 2023)](https://arxiv.org/abs/2210.03629) her çerçeve döngüye bürünür.
  Her çerçeve paketleme ReAct döngüsünün orijinal makalesinde yer almaktadır.
- [Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" (2023)](https://arxiv.org/abs/2308.08155) AutoGen'in tasarım kağıdı.
  AutoGen'in tasarım makalesi
- [Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (UIST 2023)](https://arxiv.org/abs/2304.03442)CrewAI tarzı karakter yığınlarının üzerine kurduğu rol oynaması temelleri.
  CrewAI 风格角色堆所基于的角色扮演基础──
- Bu ders karşılaştırma çerçevesini 11 · 16 (LangGraph)
  Bu ders karşılaştırma temel çerçeve
- 11 · 19 aşaması (Refleksiyon)  LangGraph'e temiz bir şekilde, ancak CrewAI'ye garip bir şekilde haritan bir desen.
  LangGraph'de net bir haritalama ama CrewAI'de çirkin bir model.
- 11 · 22 aşama (İşlemenin gözlemlenebilirliği)  hangi çerçeveyi seçtiğinizden bağımsız olarak nasıl bir araç kullanacağınız.
  Nasıl seçtiğin herhangi bir çerçeveyi ekleyeceksin.
