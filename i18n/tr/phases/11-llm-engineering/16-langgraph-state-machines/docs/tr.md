# LangGraph  Ajanlar için Devlet Makineleri  LangGraph:Ajanların Durumu
# Ajan Devlet Makineleri  Grafikler, düğmeler, Kontrol Noktalar

> Elle yazılmış bir ReAct döngüsü bir `while True`Bu, bir açık grafik olarak yazılan aynı döngüdür. kontrol noktası, kesinti, dal ve zaman yolculuğu yapabileceğiniz bir şey.

> **【中文解读】**El yazısı ReAct döngüsü bir .`while True` LangGraph'in yazılı ReAct döngüsü bir çizimdir.

> **【拓展：LangGraph→Agent工程】**LangGraph şu anda en gelişmiş Agent 编排框架, Agent 执行建模为状态图 (StateGraph),支持人机协作、分支逻辑和持久化状态――

>  **【前置】**学本节前请先掌握:(1) Fase 11·09(Fonksiyon Çağrısı);(2) Fase 14·01(Agent Loop) 理解 ReAct 循环;(3) 状态机概念(有限状态机 FSM、节点、边) ――本节会用 `langgraph`- Evet.`langchain-core`- Evet.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 14 (Model Context Protocol) | **前置知识:** Phase 11 · 09 (函数调用)、14 (模型上下文协议)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Bir fonksiyon çağıran ajan göndersiniz. Üç tur için çalışır, sonra bir şey ters gider: model 500'i geri veren bir aracı dener, kullanıcı görev ortasında fikrini değiştirir veya ajan bir siparişi insan imzasız geri ödeme yapmaya karar verir.`while True:`Bu, bir demo'dan sonra gönderdiğiniz an, ajan ya işe yaradı ya da çalışmadı.

> Bir işlevi yayınladınız, Agent'i kullanmak için. Üç tur çalıştı ve sonra bir sorun çıktı: Model bir 500'e geri dönme aracı denedi, kullanıcı bir şekilde fikrini değiştirdi veya Agent, yapay imza olmadan geri ödemeyi karar verdi.`while True:`Çeviri hiç bir 子 yok. Onu durduramazsın. Geri döner, ya da "Model başka bir araç seçerse ne olur" diye bir bölüm yapamazsın.

Bir sonraki adım, gördüğünüzde açık olur. Ajan zaten bir devlet makinesi  sistem tesisi artı mesaj geçmişi artı bekleyen araç çağrıları artı bir sonraki eylem. Devlet makinesini açık bir şekilde yapın: "model düşünür", "bir araç çalışır", "bir insan onaylar" ve aralarındaki koşullu geçişler için kenarlar. Grafiğin açık olduğu zaman, harness dört şeyi ücretsiz olarak alır: kontrol noktası (adılar arasında durum kaydet), kesintiler (insan için durak), akış (akış tokeni ve ara olaylar) ve zaman yolculuğu (önceki bir duruma geri dönüp farklı bir dal denemek).

> Bir kez gördüğünüzde, bir sonraki adım açıkça görülür. Ajanın kendisi bir durum makinesi sisteminin göstergesi, bir mesajın tarihsel olarak kullanılması ve bir sonraki adım hareketinin kullanılmasıdır.

LangGraph bu soyutlamayı gönderen kütüphanedir. LangChain anlamında bir ajan çerçevesidir ("burada bir AgentExecutor, iyi şanslar"). Birinci sınıf durum, birinci sınıf ısrar ve birinci sınıf kesintilerle bir grafik çalıştırma süresi.
Bu soyutlamanın referans uygulanması LangGraph. LangChain anlamında bir ajan çerçevesidir ("burada bir AgentExecutor, iyi şanslar"). Birinci sınıf durum, birinci sınıf ısrar ve birinci sınıf kesintilerle bir grafik çalıştırma süresi.

> LangGraph bu tür bir soyut kütlesini sağlar. LangChain anlamında bir ajan çerçevesidir. Bir vatandaşlık durumu, bir vatandaşlık kalıcılığı ve bir vatandaşlık kesintisi olan bir tablo kuruluşudur.


> **【中文解读】**LangGraph'in temel avantajı, karmaşık kontrol akışını desteklemektir: döngü: √Agent 遇到错误时重试) √条件分支(taski türüne göre farklı araç seçimi) √Yapay onay (高风险操作需要人工确认) √

>  **【类比】**Handwriting ReAct döngüsü gibi çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim çizim

> ️ **【易错点】**LangGraph'in 3 个坑:(1) **状态 schema 太松散**用 `dict`Bu durumda 没类型约束,运行时钥匙 拼错发现不了;用 `TypedDict`Ya da Pydantik Model  define State──(2) **条件边写得太复杂**  边缘 函数里 if/else 嵌套 5 层,调试地狱; 拆成多个简单边缘 函数,每个返回单一节点名――(3) **checkpoint 用 SQLite 不持久化** yeniden başlatma; Postgres veya Redis ile üretim yapma kontrol noktası


## Konsepten bir şey.

> **【中文解读】**LangGraph LLM Ajanı 建模为状态机(State Machine): defines state节点(如检索、生成、验证) 和转换边(条件分支) ・・・相比简单的链式调用,状态机支持循环、条件分支、人工审批等复杂控制流──

> **【拓展：LangGraph 与 Agent 编排】**LangGraph, LangChain  takımının başlatdığı Agent 编排框架,支持:多 Agent 协作、人工介入(Human-in-the-loop) 持久化状态、时间旅行调试――与 CrewAI (CrewAI) 角色扮演 代理) 及 AutoGen (AutoGen) 多 Agent 对话) 相比,LangGraph 更适应需要精确控制流的复杂业务场景──


![LangGraph StateGraph: nodes, edges, and the checkpointer](../assets/langgraph-stategraph.svg)

A.`StateGraph`Üç şey var.

> `StateGraph`Üç şey var.

1. **State.**Grafiği akıtır. Her düğüm tam durumu alır ve kısmi bir güncelleme gönderir, LangGraph'in her alan için *reducer* kullanarak birleştirdiği `operator.add`Toplanması gereken listeler için, varsayılan olarak yazılmasını değiştirin.
   **状态。**流过图的类型化字典──每个节点收到完整状态并返回部分更新──
2. **Nodes.**Python fonksiyonları `state -> partial_state`Her biri ayrı bir adım: "modelle çağırabilir", "alçaları çalıştırır", "cümle yaparlar".
   **节点。**Python 函数 `state -> partial_state` Herkes ayrı bir adım.
3. **Edges.**Kodular arasındaki geçişler. Statik kenarlar bir yere gider. Şartlı kenarlar bir yönlendirme işlevi alır.`state -> next_node_name`Yani grafik model çıkışına dalışabilir.
   **边。**节点之间转换──静态边去一个地方──条件边接受路由函数以在模型输出上分支──

Grafi oluşturur. Topolojiyi bağlar, bir kontrol noktasını bağlar (özel ama üretim için gerekli) ve bir çalıştırılabilirini gönderir.`thread_id`Her atışın bir kontrol noktası vardır .`(thread_id, checkpoint_id)`- Evet .

> Çekim için bir tane daha kullanın.`thread_id`Bu, bir kontrol noktası olarak devam ettirildi.

### Dört süper güç

**Checkpointing.**Her düğüm geçimi yeni durumu bir depoya yazar (testler için hafıza, prod için Postgres/Redis/SQLite).`thread_id`Grafik durduğu yerden devam ediyor.

> **检查点。**Her nodum yeni bir durum kaydına geçecek. Aynı şekilde kullanılarak.`thread_id`Tekrar düzeltmek için.

**Interrupts.**Bir düğüm ile işaretleyin `interrupt_before=["human_review"]`Bu durum devam eder. API'niz kullanıcıya "ilkelme bekliyor" cevabını verir.`thread_id`- Evet .`Command(resume=...)`İdamı yeniden başlatıyor.

> **中断。**Kullan .`interrupt_before`标记一个节点,执行在该节点运行前停止――状态被持久化――后续请求可恢复执行――

**Streaming.** `graph.stream(state, mode="updates")`Bu durumlar, Delta eyaletlerini de etkiledi.`mode="messages"`LLM tokenlerini model düğümler içinde akıtır. `mode="values"`Uygulama alanında neyi açacaklarını seçersiniz.

> **流式输出。** `graph.stream`按发生顺序产出状态增量──你选择在 UI 中显示什么──

**Time-travel.** `graph.get_state_history(thread_id)`Kontrol noktasının tamamını gönderir.`checkpoint_id`- ...`graph.invoke`Bu durum, " modelin yerine araç B seçtiği olsaydı ne olurdu?" ve üretim izlerini tekrarlayan gerileme testleri için harika.

> **时间旅行。**返回完整的检查点日志──传进任何前所的 `checkpoint_id`Bu noktadan ayrıldın.

### Kısıtlayıcılar önemli .

Her durum alanında bir azaltıcı vardır. Çoğu varsayılanlar iyi  yeni bir değer eski değerleri üstü yazıyor. Ama mesaj listeleri gerekir `operator.add`Bu nedenle, yeni mesajlar değiştirmek yerine eklenir. Düz kenarları güncellemelerini azaltıcı aracılığıyla birleştirir.`messages`Ve sen unutmuşsun.`Annotated[list, add_messages]`Kısaltıcı kütüphanede tek ince şey, doğru yaparsanız geri kalanı yazarsınız.

> Her bir durum bölümünde bir azaltıcı vardır.`operator.add`Yeni haberlerin değiştirilmesinden ziyade eklenmesi için.

### ReAct grafik 4 düğümde

Bir üretim ReAct ajanı dört düğüm ve iki kenardan oluşur:

> Bir üretim sınıfı ReAct Ajanı dört nokta ve iki kenar vardır:

1. `agent` mevcut mesaj geçmişi ile LLM'yi çağırır. Yardımcı mesajını gönderir ( tool_calls içerebilir).
2. `tools` son asistan mesajında herhangi bir tool_call'u gerçekleştirir, araç sonuçlarını araç mesajları olarak ekler.
3. Şartlı bir kenar `agent`Bu yollar `tools`Eğer son mesajda tool_calls varsa, başka bir şekilde `END`- Evet .
4. `tools`Geri dön .`agent`- Evet .

Tam ReAct döngüsünü (Though → Action → Observation → Thought → ...) yaklaşık 40 satır kodla kontrol, kesinti ve akışla elde ediyorsunuz.

> İşte böyle. Bu da tam bir ReAct döngüsü. Düşün → hareket → gözlem → düşün → ...), kontrol noktaları, kesintisi ve akışlı çıkış, yaklaşık 40 行代码.

### StateGraph vs Gönder (fanout)

`Send(node_name, state)`Bir düğüm paralel altgrafları gönderir. Örnek: ajan üç geri alıcıyı bir anda sormaya karar verir. Her biri `Send`LangGraph, hedef düğümün paralel bir yürütmesini sağlar; çıkışları durum azaltıcısı aracılığıyla birleşir.

> `Send(node_name, state)`Bir nokta ayırıp bir resim yap.`Send`生成目標节点の并行実行; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并──; 合并; 合并; 通过; 合并; 通过; 通过; 通过; 通过; 发出; 发出; 发出; 发出; 发; 发出; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发; 发;

### Altyazılar

Bir grafik başka bir grafikte bir düğüm olabilir. Dış grafik tek bir düğüm görür; iç grafik kendi durumuna ve kendi kontrol noktalarına sahiptir.

> 编译后图可以是另一个图中的节点――外层图看到单一节点;内层图有自己的状态和检查点――这是团队构建监督员工代理的方法――

## Yapın.
```figure
l5-state-graph-ledger
```

## Yapın

### Adım 1: Durum ve düğümler

> 步骤 1: durum ve nokta

```python
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def agent_node(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State) -> str:
    last = state["messages"][-1]
    return "tools" if getattr(last, "tool_calls", None) else END

tool_node = ToolNode(tools=[search_web, read_file])

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

app = graph.compile(checkpointer=MemorySaver())
```

`add_messages`Bu, mesaj listesini üst yazmak yerine toplayarak azaltır.

> `add_messages`Bu, haber listesi toplanıp kapsamayan bir azaltıcıdır. Unutmayın ki bu en yaygın LangGraph hatalarıdır.

### Adım 2: İpuçla çalıştır

> 步骤 2: Uçuş yoluyla yürüyüşe geçmek.

```python
config = {"configurable": {"thread_id": "user-42"}}
for event in app.stream(
    {"messages": [HumanMessage("find the Anthropic headquarters address")]},
    config,
    stream_mode="updates",
):
    print(event)
```

Her güncelleme bir diktedir .`{node_name: state_delta}`Ön uçlarınız bunları kullanıcı arayüzüne aktarır böylece kullanıcılar "Agent düşünüyor"... arama web... sonuç aldı... cevap veriyor".

> Her güncellemesi var .`{node_name: state_delta}`字典──前端可流式传到 UI,让用户看到"agent 思考中... 调用 search_web... 得到结果... 回答中"──

### Adım 3: Bir insan-da-da-da-da döngü kesintisi ekleyin

Bir düğüm işaretleyin, böylece çalıştırmadan önce çalıştırma durur.

> 步骤 3:添加人机协作中断──标记节点使执行在运行前暂停──

```python
app = graph.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tools"],  # pause before every tool call
)

state = app.invoke({"messages": [HumanMessage("delete the production database")]}, config)
# state["__interrupt__"] is set. Inspect proposed tool calls.
# If approved:
from langgraph.types import Command
app.invoke(Command(resume=True), config)
# If denied: write a rejection message and resume
app.update_state(config, {"messages": [AIMessage("Blocked by human reviewer.")]})
```

Durum, kontrol noktası ve ip kesinti boyunca devam ediyor.

> Durum, kontrol noktası ve bağlantı kesinti sırasında tüm kalıcılıklanmaktadır.

### Adım 4: Debugging için zaman yolculuğu

> 步骤 4:调试用时间旅行──

```python
history = list(app.get_state_history(config))
for snapshot in history:
    print(snapshot.values["messages"][-1].content[:80], snapshot.config)

# Fork from a prior checkpoint
target = history[3].config  # three steps back
for event in app.stream(None, target, stream_mode="values"):
    pass  # replay from that point forward
```

Geçmek .`None`Bu, bir değer geçerek, tekrar başlamadan önce bu kontrol noktasının durumuna bir güncelleme olarak ekler.

> 传入 `None`作为输入从给定检查点重放;传输值则在恢复前将其作为更新添加到该检查点的状态――这是如何在不重新运行整个对话的情况下复现一个错误的代理运行――

### Adım 5: Kontrol noktasını üretim için değiştir

> Çekim 5: üretim ortamı kontrol noktaları için değiştirilmiştir.

```python
from langgraph.checkpoint.postgres import PostgresSaver

with PostgresSaver.from_conn_string("postgresql://...") as checkpointer:
    checkpointer.setup()
    app = graph.compile(checkpointer=checkpointer)
```

SQLite, Redis ve Postgres gönderiliyor.`MemorySaver`Yeniden başlatma sırasında devam eden her şey gerçek bir mağazaya ihtiyaç duyar.

> SQLite、Redis 和 Postgres 已提供──`MemorySaver`Test için kullanılıyor. Sürekli olarak yeniden başlatılması gereken her şey gerçek depolama ihtiyacı vardır.

## Yetenek

> Ajanları grafik olarak inşa ediyorsun, değil.`while True`- Çubuklar.
> Sen bir ajanı yaratıyorsun.`while True`Çeviri:

LangGraph'e ulaşmadan önce 60 saniyelik bir tasarım yapın:

> LangGraph kullanmadan önce, 60 saniyelik bir tasarım yapın:

1. **Name the nodes.**Her ayrı karar veya yan etkisi olan eylem bir düğümdür. "Agent düşünür," "üçüm çalışır," "temizleyici onaylar," " yanıt akışları".
   **命名节点。**Her ayrılık kararı veya yan etkisi bir noktadır.
2. **Declare the state.**Her liste alanı için bir azaltıcı ile en az Tiplenmiş Dikt.`messages`; görev-sözlü alanları (bir çalışma `plan`, a `budget`karşılama, bir `retrieved_docs`listesi) en üst seviyeye kadar.
   **声明状态。**En küçük Tip Tip, her listede bir kısım vardır.
3. **Draw the edges.**Bir sonraki adım model çıkışına bağlı değilse, her koşullu kenarın isimli dallarla bir yönlendirme fonksiyonu olması gerekir.
   **画边。**Sonraki adım model çıkışına bağlı değilse, hareketsiz kenar kullanmakla birlikte.
4. **Choose a checkpointer up front.** `MemorySaver`Testler için Postgres/Redis/SQLite başka bir şey için.
   **提前选择检查点器。**测试用 `MemorySaver`, Diğerleri Postgres/Redis/SQLite
5. **Decide interrupts before tools run, not after.**Onaylamalar kenarında yan etkileme düğümüne gider böylece zarar vermeden iptal edebilirsiniz; onaylama modelin kenarında gider böylece kötü çağrıları ucuz bir şekilde reddedebilirsiniz.
   **在工具运行之前决定中断，而不是之后。**
6. **Stream by default.** `mode="updates"`UI için, `mode="messages"`Modelle düğümler içinde token seviyesinde akış için, `mode="values"`değerlendirme sırasında tam anlık fotoğraflar için.
   **默认使用流式输出。**

Kontrol noktası olmayan LangGraph ajanını göndermeyi reddedin yan etkiden sonra kesilen bir ajanı göndermeyi reddedin bir kontrol noktası olmayan LangGraph ajanını göndermeyi reddedin yan etkiden sonra kesilen bir ajanı göndermeyi reddedin bir kontrol noktası olmayan bir ajanı göndermeyi reddedin bir kontrol noktası olmayan bir ajanı göndermeyi reddedin bir kontrol noktası olmayan bir ajanı göndermeyi reddedin bir kontrol noktası olmayan bir ajanı göndermeyi reddedin bir kontrol noktası olmadan bir kontrol noktası göndermeyi reddedin bir kontrol noktası için bir kontrol noktası göndermeyi reddedin`messages` olmadan alan`add_messages`- Kısıtlayıcı olarak.

>                                                                                                                                                                                                                                                               `add_messages`作为减轻的 `messages`- Evet.

## Egzersizler.

1. **Easy.**Yukarıdaki dört düğümlü ReAct grafiğini bir hesap makinesi aracı ve bir web arama aracı ile uygulayın.`list(app.get_state_history(config))`İki dönüşlü bir konuşma için en az dört kontrol noktasını geri gönderir.
   **简单。**实现上述四节点 ReAct 图,验证检查点历史记录──
2. **Medium.**Bir ekle`planner`Önceden giden düğüm`agent`ve yapılandırılmış bir yazı yazar.`plan: list[str]`- Eyalete.`agent`Plan adımlarını işaretleyin.`plan`kontrol noktası özetlemesinde kaybolur (sahte azaltıcı).
   **中等。**Bir tane ekle.`agent`之前运行的 `planner`节点,写入结构化计划到状态──
3. **Hard.**Üç alt grafik arasında yol alan bir denetim grafiği oluştur (`researcher`- Evet .`writer`- Evet .`reviewer`) kullanılarak `Send`Her altgrafın kendi durumu ve kontrol noktası vardır.`interrupt_before=["writer"]`Bir insan araştırma raporu onaylayabilsin diye dış grafikte.
   **困难。**Construct a supervisor 图,在三个子图之间使用 `Send`Yollar.

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| StateGraph | "The LangGraph graph" / "LangGraph 图" | The builder object you add nodes and edges to before compile. | StateGraph：编译前添加节点和边的构建器对象 |
| Reducer | "How the field merges" / "字段如何合并" | A function `(old, new) -> merged` applied when a node returns an update for that field; default is overwrite, `add_messages` appends. | Reducer：节点返回更新时应用的合并函数 |
| Thread | "A conversation ID" / "对话 ID" | A `thread_id` string that scopes all checkpoints for one session. | Thread：限定一个会话所有检查点的 thread_id 字符串 |
| Checkpoint | "A paused state" / "暂停的状态" | A persisted snapshot of the full graph state after a node transition, keyed on `(thread_id, checkpoint_id)`. | Checkpoint：节点转换后持久化的完整图状态快照 |
| Interrupt | "Pause for a human" / "暂停等人工" | `interrupt_before` / `interrupt_after` stop execution at a node boundary; resume with `Command(resume=...)`. | Interrupt：在节点边界停止执行，可恢复 |
| Time-travel | "Fork from a prior step" / "从先前步骤分叉" | `graph.invoke(None, config_with_old_checkpoint_id)` replays from that checkpoint forward. | Time-travel：从先前检查点重放 |
| Send | "Parallel subgraph dispatch" / "并行子图分派" | A constructor a node can return to spawn N parallel executions of a target node. | Send：节点返回以生成 N 个并行执行的构造器 |
| Subgraph | "A compiled graph as a node" / "编译后的图作为节点" | A compiled StateGraph used as a node in another graph; preserves its own state scope. | Subgraph：作为另一个图中节点使用的编译后 StateGraph |

## Daha fazla okumak

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) StateGraph, azaltıcılar, kontrol noktaları ve kesintiler için kanonik referans.
  LangGraph 文档StateGraph、reducer、检查点器和中断的权威参考──
- [LangGraph concepts: state, reducers, checkpointers](https://langchain-ai.github.io/langgraph/concepts/low_level/) bu dersin kullandığı zihinsel model, doğrudan kaynağından.
  LangGraph 概念: status、reducer、检查点器──
- [LangGraph Persistence and Checkpoints](https://langchain-ai.github.io/langgraph/concepts/persistence/) Postgres/SQLite/Redis depoları, kontrol noktaları isim alanları ve ip kimlikleri üzerindeki detaylar.
  LangGraph 持久化和检查点详情──
- [LangGraph Human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/) `interrupt_before`- Evet .`interrupt_after`- Evet .`Command(resume=...)`, ve düzenleme durumu kalıbı.
  LangGraph 人机协作 interrupt 和 resume 模式──
- [Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023)](https://arxiv.org/abs/2210.03629) her LangGraph ajanının uyguladığı örneği; mantık izlenimi mantıklılığı için okuyun.
  Her LangGraph Ajanı gerçekleştirilen ReAct Mode
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) hangi grafik şekilleri ( zincir, yönlendirici, orkestrasyon-işçiler, değerlendirici-optimalisyoncu) tercih etmek ve ne zaman.
  Antropik 关于选择哪种图形以及何时使用指南──
- Eğlence çağrısı primitifleri her LangGraph ajan düğümünü tekrar kullanır.
  第 11 阶段 · 09(函数调用) 每个 LangGraph Agent 节点重用工具调用原语。
- 11 · 14 aşama (Model Kontext Protokolü)  LangGraph'e bağlanan dış araç keşfi `ToolNode`MCP adaptörü üzerinden.
  第 11 阶段 · 14(MCP) MCP 适配器插入 LangGraph `ToolNode`Dış aletlerin bulunması
- Eğlence 11 · 17 (Agent çerçeve pazarlamaları)  LangGraph'i CrewAI, AutoGen veya Agno'dan ne zaman seçmek.
  第 11 阶段 · 17(Agent 框架对比) 何时选择 LangGraph──
