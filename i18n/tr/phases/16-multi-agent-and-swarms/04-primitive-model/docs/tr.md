# Çok Ajanlı İlkel Model. Çok Ajanlı Orijinal.

> Dört primitif, daha fazlası  ajan, teslimat, paylaşılan durum, orkestratör  dört boyutlu bir tasarım alanını kapsar ve 2026'da gönderilen büyük çoklu ajan çerçeveleri (AutoGen, LangGraph, CrewAI, OpenAI Agents SDK, Microsoft Agent Framework) noktalardır. Bu ders onları sıfırdan inşa eder, dörtte bir oyuncak sistemi çalışır, sonra her ana çerçeveyi aynı ekselere haritası yapar böylece yeni bir versiyonu bir paragraf içinde okuyabilirsiniz.

> **【中文解读】**Bu bölüm, çoklu ajan sisteminin temel yapı birimlerini ve iletişim orijinal dillerini tanıttı.

> **【拓展：primitive model→具体应用】**Ço Agent  sisteminin en küçük orijinal dil modeli, Agent  arasındaki temel iletişim modelini tanımladı: 1) mesaj iletişimi Agent                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 (Agent Engineering), Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 14 (Agent 工程), Phase 16 · 01 (为什么需要多 Agent)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前 Lütfen önce bil:Fase 14(Agent 工程)、Fase 16·01(多 Agent 动机)。本节是Fase 16'nın merkezi4个原语(agent/handoff/shared-state/orchestrator) define所有框架的设计空间。
>  **【类比】**4 原语 = "音乐四件套":agent(乐手)、handoff(独奏接力)、shared state(总谱)、orchestrator(指挥)。AutoGen 偏消息传递、LangGraph 偏共享状态、CrewAI 偏角色分工都是这些四个原语的不同组合──学会原语后看任何新框架都能 1段话读懂──

## Sorunlar sorunun giriş

Her altı ayda bir yeni çok ajan çerçeve gemileri. AutoGen 2023. CrewAI 2024. LangGraph ve OpenAI Swarm 2024. Google ADK Nisan 2025. Microsoft Agent Framework RC Şubat 2026. Her basın açıklaması "doğru soyutlama" olduğunu iddia ediyor.

> Her altı ayda bir yeni Multi Agent Framework yayınlanacak. 2023 yılının AutoGen'i, 2024 yılının CrewAI, 2024 yılının LangGraph ve OpenAI Swarm, 2025 yılının 4 ayında Google ADK, 2026 yılının 2 ayında Microsoft Agent Framework RC, her bir basın yazısı kendini "hakiki bir soyut" olarak iddia ediyor.

Yenilik gibi görünen şey genellikle yeniden markalama yapılıyor: aynı dört düğme (agent, transfer, paylaşılan durum, orkestratör) farklı öntanımlı ve sentaks ile.

> 变化是真实的但底层原语没有变化──看似创新的东西经常是重品牌化:相同的四旋: 经纪人,交接,共享状态,编排器) 与不同的默认值和语法── 一旦你看到原语,营销就消失了──

Eğer bunları birbiriyle öğrenmeye çalışarsanız, biter. API'ler farklı görünüyor. Dokümanlar "ajan" nedir konusunda anlaşmazlık yaşıyor. Bir çerçeve paylaşılmış hafızasını "blackboard" olarak adlandırır, bir diğeri "eğitim havuzu" olarak adlandırır, bir diğeri "StateGraph" olarak adlandırır.

> Eğer bunları öğrenmeye çalışırsan, yorulursun. API farklı görünüyor.

Bu değil. pazarlama altında, dört ilkel sabit. Bir kez öğrenin, her yeni çerçeveyi bir paragrafda okuyun.

> Aslında öyle değil. Satış altında dört orijinal dil sabit.

## Konsept merkezi konsept

### Dört ilkel

1. **Agent** bir sistem prompt ve bir araç listesi. İletiksel; her çalıştırma sistem prompt'undan ve mevcut mesaj geçmişinden başlar.
   Çeviri:**Agent** Bir sistem ipucu ekle bir araç listesi.
2. **Handoff** bir ajanın diğerine yönlendirilmiş bir kontrol transferü.
   Çeviri:**交接** Bir Ajan'ın yapısal kontrolü diğer Ajan'a aktarılması.
3. **Shared state** birden fazla ajanın okuyabileceği (bazen yazabileceği) herhangi bir veri yapısı. Mesaj havuzu, kara tahtası, anahtar değerleri depolama, vektör belleği.
   Çeviri:**共享状态** Çoklu Ajanlar tarafından okuyabilir (sometimes write in) herhangi bir veri yapısı.
4. **Orchestrator** kim sonraki konuşmayı seçebilir. Seçenekler: açık bir grafik (deterministik), bir LLM konuşmacı seçicisi (yumuşak), son konuşmacı'nın el eleme çağrısı (OpenAI Swarm), veya bir kuyruk üzerinde bir programlayıcı (swarm mimarisi).
   Çeviri:**编排器** karar vermek kimin bir sonraki konuşmacı rolü.

Bu tüm tasarım alanı. Her çerçeve her eksesi için öntanımlı seçenekler seçer.

> Bu, tüm tasarım alanıdır. Her çerçeve her aksel için seçilir.

Sonuç: "en iyi" çoklu ajan çerçeve yoktur. Sadece "işinizin eksel tercihleri için en iyi" vardır. Deterministik boru hattları için orkestrasyonu çivileyen bir çerçeve (LangGraph) ortaya çıkan sohbetler için yanlış (AutoGen kullanın).

> 含义:没有"最佳"多代理框架――只有"最适合你的任务轴偏好的"框架――在确定性流水线上钉住编排的框架――长图) 涌现对话是错误的――使用AutoGen (自动生成)――了解你的轴,然后选择――

### 2026 çerçevesinin nasıl haritası

| Framework | Agent | Handoff | Shared state | Orchestrator |
|-----------|-------|---------|--------------|--------------|
| OpenAI Swarm / Agents SDK | `Agent(instructions, tools)` | tool returns Agent | caller's problem | the LLM's next handoff call |
| AutoGen v0.4 / AG2 | `ConversableAgent` | speaker-selector on GroupChat | message pool | selector function (LLM or round-robin) |
| CrewAI | `Agent(role, goal, backstory)` | `Process.Sequential / Hierarchical` | Task outputs chained | manager LLM or static order |
| LangGraph | node function | graph edge + condition | `StateGraph` reducer | the graph, deterministic |
| Microsoft Agent Framework | agent + orchestration patterns | pattern-specific | thread / context | pattern-specific |
| Google ADK | agent + A2A card | A2A task | A2A artifacts | host decides |

> Çerçeve Ajan bağlantı paylaşım durumu düzenleyicisi
> Bu yüzden de bu kadar çok şey var.
> # AçıkAI Swarm / Ajanlar SDK #`Agent(instructions, tools)`# Araçlar Ajanın Sorularına Geri Dön # # LLM'nin Sonraki Soru Soruları
> # AutoGen v0.4 / AG2 #`ConversableAgent`# Grup Çat'ta konuşma seçeneği # # haber dalı # # seçeneği fonksiyonu #
> # Ekibi yok #`Agent(role, goal, backstory)`- Hayır .`Process.Sequential / Hierarchical`# Görevler çıkış zinciri # # yöneticisi, # veya sabit sırası #
> # LangGraph # # düğüm fonksiyonu # # çizim + koşullar #`StateGraph`- Bu bir şey.
> # Microsoft Ajan Çerçeve # # Ajan # # düzenleme modeli # # belirli bir şablon # # aşağıdaki şablon #
> Google ADK ajanı + A2A kartı

Yüzey farkları büyük görünüyor.

> 表面差异看起来很大──底层:相同的四旋──

### Bu neden önemli?

İlkselleri gördüğünüzde, çerçeve karşılaştırması kısa bir kontrol listesi haline gelir:

> Bir kez orijinal dili gördüğünüzde, framework comparison kısa bir kontrol listesine dönüşüyor:

- Orkestratör LLM'ye yönlendirmeyi (Swarm) güveniyor mu yoksa yönlendirmeyi kodla (LangGraph) belirliyor mu?
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Paylaşılan devlet tam tarihi (GroupChat) mi yoksa projelendirilen (StateGraph reducer) mi?
  Çin Çeviri: Ortaklık durumu is complet istoria (Tüm Tarih) mu yoksa proje (Seviri) mi?
- Ajanlar birbirlerinin isteklerini değiştirebilir mi (CrewAI yöneticisi) yoksa sadece elden mi (Swarm)?
  Çinçe Çevirim:Agent 能否修改彼此的提示?

Bu üç sorunun cevabı, hangi çerçeveyi belirtilen bir soruya uygun buluyor. "En iyi çok ajan çerçevesini" satın almaktan vazgeçip aslında önem verdiğiniz ekseni tasarlamaya başlarsınız.

> Bu üç sorunun yanıtları %80'in hangi çerçeveyi uygun bulduğunu soruyor.

Yeni bir çerçeve 2027 yılında başlatıldığında, üç soruyu ona atlayın. Eğer cevapları zaten kullandığınız çerçeveye eşleşirse, göçü atlayın. Eğer önemli olduğunuz bir eksede farklılık gösterirlerse, değerlendirin. Yeni çerçevelerin çoğu yenilik değil yeniden paketleme.

> 2027 yılının yeni çerçevesinin yayınlandığında, bu üç sorunun uygulanması için, eğer cevapları sizin kullandığınız çerçeveye uygunsa, taşınma üzerinden atlayın. Eğer bunlar sizin için önemli olan bir etkendelerden farklıysa, değerlendirin.

### Ülkesiz bir anlayış

Ortak durum hariç her primitif devletsizdir. Ajan bir fonksiyon (sürekli, araçlar). Elde etmek bir fonksiyon çağrısı. Orkestratör bir programcıdır. **The only stateful thing in the system is shared state.**Tüm ilginç hatalar burada yaşar: hafıza zehirlenmesi (Denevi 15), mesaj düzenleme, versiyonlama, yazma tartışmaları.

> Paylaşılan durum dışında, her bir orijinal dil durumsuzdur. Ajanı bir fonksiyon (sürekli, araçlar) olarak tanımlar.**系统中唯一有状态的东西是共享状态。**İşte tüm ilginç hatalar yerinde:内存污染 (内存污染)

Bu anlayış hata düzeltme stratejisini yönlendirir: bir çok ajanlı sistem yanlış davranırsa, önce paylaşılan durumuna bakın. Mesaj havuzu zehirlenmiş mi? Yazılar doğru bir şekilde düzenlenmiş mi? Şema saygı görüyor mu? Devletsiz ajanlar nadiren ince hatalar yaratır; paylaşılan durum onları sürekli olarak neden olur.

> Bu fikirle ilgili bir araştırma yaparak, sistem davranışlarının sıradan olduğu durumlarda, öncelikle paylaşım durumunu kontrol edin.

Paylaşılan durumunu gizleyen çerçeveler (Swarm) sorunu çağıran kişiye yönlendirir. Onu merkezileştiren çerçeveler (LangGraph kontrol noktası, AutoGen havuzu) onu denetleyici yapar ancak koordinasyon maliyetini paylaşılan durum uygulamasına aktarır.

> 藏藏共享状态的框架(Swarm) sorunu kullanıcısına yönlendirecek.

### Tek bir ilkelin anatomisi

#### Ajan .

```
Agent = (system_prompt, tools, model, optional_name)
```

Aynı sistemde iki ajanın mesajı ve araçları değiştirilebilir.

> 没有记忆――没有状态――具有相同的系统提示和工具的两个代理是可互换的――看起来每个代理状态的一切实际上都在共享状态或交互协议中――

Bu mantıklı değil ama güçlü: devletsiz ajanlar önemsiz paralelleşebilir, yeniden başlatabilir ve değişebilir. Aynı ajanın 100 kopyasını çevirebilirsiniz ve hepsi aynı şekilde davranırlar. Devlet başka yerlerde yaşıyor.

> Bu, doğrudan karşılaştırıldığında güçlüdür: Durumsuz Ajan kolayca eşleştirilebilir, yeniden başlatılabilir ve değiştirilebilir. Aynı Ajanın 100 kopyasını başlatabilirsin, davranışları tamamen aynıdır.

#### Elverme

```
Handoff = (from_agent, to_agent, reason, payload)
```

Üç uygulama baskın:

> Üç çeşit başlıca gerçekleşme:

- **Function return**Bu OpenAI Swarm modelidir. Ajanlar araç şemelerinde yönlendirme taşır.
  Çeviri:**函数返回** 工具返回下一个 Agent──这是OpenAI Swarm'ın modeli──Agent在其工具模式中携带路由──
- **Graph edge** LangGraph. Kenarlar deklaratifdir. LLM bir değer üretir; bir koşul bir sonraki düğmeyi seçer.
  Çeviri:**图边** LangGraph──边是声明式的──LLM 产生一个值;条件选择下一个节点──
- **Speaker selection** AutoGen GroupChat. Seçim fonksiyonu (bazen kendisi bir LLM çağrısı) havuzu okuyor ve sonraki konuşmayı seçer.
  Çeviri:**发言者选择** AutoGen GroupChat。 Seçim Aracı Fonksiyonu( sometimes itself is LLM 调用)读取池并选择下一个发言者。

#### Paylaşılan devlet

```
SharedState = { messages: [], artifacts: {}, context: {} }
```

En az bir mesaj listesini oluşturmak. Genellikle daha fazla: yapılandırılmış eserler (CrewAI Görev çıkışları), tipize edilmiş bağlam (LangGraph azaltıcıları), dış bellek (MCP, vektör DB).

> En azından bir mesaj listesi vardır. Genellikle daha fazla: yapılandırma işlemi.

Paylaşılan durumun şekli, hangi tür koordinasyonun mümkün olduğunu belirler. Düz bir mesaj listesi yayını kolaylaştırır, ancak rolü özel filtrelemeyi zorlaştırır. Tiplenen bir şema filtrelemeyi önemsiz yapar, ancak önceden tasarlanmayı gerektirir. Ücretsiz öğle yemeği yoktur.

> Toplantıların düzenlenmesi ve düzenlenmesi için yapılan düzenlemeler, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, genel olarak, kabul edilen, kabul edilen, kabul edilir, kabul edilir, kabul edilir.

İki topoloji: **full pool**(her ajan her mesajı görür) ve **projected**(Agentler rol ölçeği görünümünü görüyor). Tam havuzlar basit ve kötü ölçeklendirilir.

> 两种拓:**完整池**(Her ajan her haber görüyor)**投影**(Agent göre rol aralığı görüntüsü) ―― tam bir küme basit ama genişletilmiş farkı── proje küme genişletilmiş ancak ön dönem modeli tasarımı gerektirir──

#### Orkestratör

```
Orchestrator = ({state, last_speaker}) -> next_agent
```

Dört tat:

> Dört çeşit:

- **Static** grafik inşaat zamanında sabitlenir (LangGraph deterministic, CrewAI Sequential).
  Çeviri:**静态** 图在构建时固定(LangGraph 确定性、CrewAI Sequential)
- **LLM-selected** Bir LLM havuzu okuyor ve bir sonraki konuşmayı seçer (AutoGen, CrewAI Hierarşik).
  Çeviri:**LLM 选择** LLM 读取池并选择下一个发言人(AutoGen、CrewAI Hierarchical)
- **Handoff-driven** mevcut ajan bir teslimat aracı (Swarm) çağırarak karar verir.
  Çeviri:**交接驱动** 当前 Ajan 通过调用交接工具决定(Swarm)
- **Queue-driven** İşçiler ortak bir kuyruktan çekilir; açık bir sonraki hoparlör yok (swarm mimarileri, Matrix).
  Çeviri:**队列驱动** 工作器 from共享队列拉取;没有明确的下一个发言人(群体架构、矩阵)

### Çerçeve arasındaki değişiklikler

İlkeler sabitlendikten sonra, kalan tasarım kararları şunlardır:

> Bir kez orijinal dil sabitlenince, kalan tasarım kararları şunlardır:

- **Memory strategy** geçici vs. dayanıklı kontrol noktası (LangGraph kontrol noktası).
  Çeviri:**内存策略** 临时 vs 持久检查点 (Langgraph kontrol noktası)
- **Safety boundary** bir teslimat (işlemi yapan insan) onaylayabilir.
  Çeviri:**安全边界** 谁可以批准交接 (kimler bu döngü içinde?)
- **Cost accounting** Bir ajan başına token bütçeleri.
  Çeviri:**成本核算** Her ajanın belirti bütçesi 
- **Observability** Elveriler izlemek, tekrar oynamak için devamlı durum.
  Çeviri:**可观测性**                                                                                                                                                                                                                                                              

Hepsi ilk önce uygulanabilir.

> Her şey orijinal dil üzerinde gerçekleşir.

Bir çerçeve "yeni" bir özelliği (işlemde insan, yeniden deneyin, token bütçesi) reklam ettiğinde, aslında yeni bir ilk başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı başlı

> Çerçeve "yeni" işlevleri (insanlar döngü, tekrar deneme, belirti) yayımladığında, yeni orijinal dillerin gerçekten de ortaya çıktığını veya sadece bu dört dilin bir araya geldiğini kontrol eder.

## Yapın.
```figure
a5-primitive-radar
```

## Yapın

`code/main.py`Python'un 150 satırında dört ilksel uygulamasını uyguluyor.

> `code/main.py`Yaklaşık 150 adet Python standart kütüphanesiyle dört orijinal dil gerçekleştirildi. Gerçek bir LLM yok.

Dosya ihracatı:

> 文件导出:

- `Agent` isim, sistem prompt, araç, politika işlevi ile ilgili bir veri sınıfı.
  Çeviri:`Agent` 名称、系统提示、工具、策略函数 のデータ类──
- `Handoff` yeni bir ajanı geri veren bir fonksiyon.
  Çeviri:`Handoff` 返回新 Ajan'ın işlevi
- `SharedState` bir iplik güvenli mesaj havuzu.
  Çeviri:`SharedState` 线程安全的消息池──
- `Orchestrator` Üç çeşit: `StaticOrchestrator`- Evet .`HandoffOrchestrator`- Evet .`LLMSelectorOrchestrator`(sümüle edilmiş).
  Çeviri:`Orchestrator` 三种变体:`StaticOrchestrator`- Evet.`HandoffOrchestrator`- Evet.`LLMSelectorOrchestrator`- Evet.

Demo, üç orkestratör türü boyunca aynı üç ajan borusunu ( Araştırma -> Yazma -> Değerlendirme) yürütür ve sonunda mesaj havuzunu yazdırırır.

> 演示通过所有三种编排器类型运行相同三 Agent 流水线(研究 -> 编写 -> 审阅), ve sonunda打印消息池──outputı yalnızca*谁选择下一个* 上不同;Agent 和共享状态在所有运行中相同──

Çek şunu:

```
python3 code/main.py
```

Beklenen çıkış: üç orkestratör çalışması, bir örneğe göre. Her biri son mesaj havuzunu basar. Yükümle yönlendirilmiş çalışmalar araştırmacı erken yapılması karar verirse daha az ajanlara ulaşır.

> 预期输出: Üç kez düzenleyici çalışması, her türlü bir kez── her kez basılan son haber kütlesi── eğer araştırmacı önceden tamamlanmayı karar verirse, iletişim yönlendirme çalışması daha az bir ajanı etkileyecektir.

## Çerçeveyi kullanın.

`outputs/skill-primitive-mapper.md`Bu, bir dizi ajan kod tabanını veya çerçeve belgesini okuyan ve dört temel haritasını geri veren bir beceri.

> `outputs/skill-primitive-mapper.md`Bu bir beceri, herhangi bir diğer Ajan kod defterini veya çerçeve dosyasını okumak ve yeni çerçeve yayınlanınca çalıştırmak, daha derinlemesine okumayı başlamadan önce bir bölümde bir anlayış kazanmak için bir beceri.

## İndirin . Ürünler .

Yeni bir çerçeveyi kabul etmeden önce, bunun için ilk önce haritasını yazın. Eğer yapamazsanız, belgeleri eksik veya çerçeve beşinci ilkciyi icat ediyor (görmediğiniz ortak durum tatı için nadir  kontrol edin).

> Yeni çerçeveyi kullanmadan önce, orijinal dil haritasını yazın. Yapmadığınızda, dosyanın tamamlanmamış olduğunu veya çerçeve beşinci orijinal dil geliştirdiğini belirtin.

Yapılandırmayı mimari belgesine bağlayın. Yeni bir ekip üyesi katıldığında, API belgeleri öncesine harita gönderin. Çerçeve sürümleri değiştiğinde, haritalama değişir, değişim logu değil.

> Yapımcılık dosyaları arasında sabit bir haritalama olacaktır. Yeni ekip üyesi dahil olduğunda, API dosyasından önce gönderilen haritalama olacaktır.

## Egzersizler.

1. Çık .`code/main.py`Orkestör seçiminin hangi ajanları yöneteceğini gözlemleyin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`Üç kez. Gözlem düzenleyicisi hangi ajanı değiştirmek için seçtiğini izler.
2. Dördüncü orkestrasyon türünü uygulayın: ajanların iş için durumunu paylaştığı kuyruklu bir tür.
   Çinçe Çevirim: Çarşıncı düzenleyici türünü gerçekleştirmek: Koordinasyon süren,Agent 轮询共享状态获取工作──可能发生什么死锁,你如何检测?
3. LangGraph hızlı başlangıcı al ve dört ilkel olarak yeniden yaz. LangGraph'in soyutlama haritasından hangisi 1:1 ve hangisi rahatlık kaplamaları?
   Çin Çeviri:将 LangGraph 快速入门改写为四个原语――LangGraph'ın hangi çubukları 1:1 映射, hangi özellikleri kolaylık paketleme cihazı?
4. OpenAI Swarm yemek kitabı okuyun. Swarm'ın en ergonomiğiyle ilgili dört ilkelden hangisini belirleyin ve hangisini çağıran kişiye itirir.
   Çinçe Çevirimi Çevirisi:阅读 OpenAI Swarm 手册。识别四个原语 中 Swarm 使哪个最符合人体工程学,哪个推给调用者。
5. Bu tabloda paylaşılmış durumu tamamen gizleyen bir çerçeve bul ve ajanların geçmişi yeniden okumadan teslimatları koordine etmeleri gerektiğinde neyin kırıldığını açıkla.
   Çinçe Çevirisi: Çevre içinde tamamen gizli bir ortaklık durumu çerçevesini bulmak. Açıklama: Bir ajan olarak, tarihini yeniden okumak zorunda olduğu durumlarda, iletişim koordinasyonu sırasında ortaya çıkan sorunlar nelerdir.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Agent | "An LLM with tools" / "带工具的 LLM" | A `(system_prompt, tools, model)` triple. Stateless. / 一个 `(system_prompt, tools, model)` 三元组。无状态。 |
| Handoff / 交接 | "Transfer of control" / "控制转移" | A structured call that names the next agent and optional payload. Three implementations: function return, graph edge, speaker selection. / 命名下一个 Agent 和可选有效载荷的结构化调用。三种实现：函数返回、图边、发言者选择。 |
| Shared state / 共享状态 | "Memory" / "context" / "内存" / "上下文" | The only stateful part of a multi-agent system. Message pool or blackboard. / 多 Agent 系统中唯一有状态的部分。消息池或黑板。 |
| Orchestrator / 编排器 | "Coordinator" / "协调器" | Whoever decides who runs next. Static graph, LLM selector, handoff-driven, or queue-driven. / 决定谁下一个运行的角色。静态图、LLM 选择器、交接驱动或队列驱动。 |
| Primitive / 原语 | "Abstraction" / "抽象" | One of the four axes every framework parameterizes. Not a framework feature. / 每个框架参数化的四个轴之一。不是框架特性。 |
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Full-history shared state. Easy to reason about, scales badly. / 完整历史共享状态。易于推理，扩展性差。 |
| Projected state / 投影状态 | "Scoped view" / "范围视图" | Role-specific view into shared state. Scales, requires schema design. / 角色特定的共享状态视图。可扩展，需要模式设计。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | Orchestrator pattern where a function (often an LLM) picks the next agent from a group. / 编排器模式，函数（通常是 LLM）从组中选择下一个 Agent。 |

## Daha fazla okumak

- [OpenAI cookbook: Orchestrating Agents — Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) el ele yönlendirilmiş orkestrasyonun en net ifade edilmesi
  Çinçe Çevirimi:OpenAI 手册:编排 Ajan  例例和交接 交接驱动编排的最清晰阐述
- [AutoGen stable docs](https://microsoft.github.io/autogen/stable/) GroupChat + konuşmacı seçimi LLM seçilen orkestrasyon için referanstır
  中文翻译:AutoGen 稳定文档  GroupChat + 发言人选择是 LLM 选择编排的参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) Grafik kenarında orkestrasyon ve azaltıcı tabanlı ortak durum
  Çinçe Çevirim:LangGraph 工作流和 Agent  图边编排和基于归约器的共享状态
- [CrewAI introduction](https://docs.crewai.com/en/introduction) Rol-hedef-geçmişli ajanlar, Sequential / Hierarchical processes
  Çeviri:CrewAI 介绍  角色-目标-背景故事 Ajan,Sekvensial / Hierarşik 流程
- [AG2 (community AutoGen continuation)](https://github.com/ag2ai/ag2) Microsoft'un v0.4'i bakıma geçirdiğinden sonra canlı AutoGen v0.2 hattı
  Çinçe Çevirimi:AG2(社区 AutoGen 延续)  微软将 v0.4 移入维护后的活跃 AutoGen v0.2 线
