# لانغغراف  آلات الدولة للعملاء  لانغراف: حالة العميل
# الوكيل الآلات الدولة  الرسومات، العقد، نقاط التفتيش

> حلقة ReAct مكتوبة يدويا هي `while True`نفس الحلقة المكتوبة على الرسم البياني الصريح هي شيء يمكنك التفتيش، والقطع، والفرع، والسفر عبر الزمن.

> **【中文解读】**من خلال كتابة كتابة " ردة فعل "`while True` استخدام لنجراف كتب ReAct 循环 هو رسم  يمكن فحص نقطة حفظ ‬中断 ‬分支 时间旅行‬

> **【拓展：LangGraph→Agent工程】**لانغغغراف هي الأكثر تقدما في إطار تنظيم الوكلاء، والوكيل سوف تنفيذ المثابة للحالة، والحالة الدائمة.

>  **【前置】**学本节前请先掌握:(1) المرحلة 11·09(تصل بالوظيفة);(2) المرحلة 14·01(حلقة العميل)  فهم ReAct 循环;(3) 状态机概念(有限状态机 FSM、节点、边) ――本节会用 `langgraph`.`langchain-core`.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 09 (Function Calling), Phase 11 · 14 (Model Context Protocol) | **前置知识:** Phase 11 · 09 (函数调用)、14 (模型上下文协议)
**Time:** ~75 minutes | **时间:** ~75 分钟

## المشكلة المشكلة المشكلة

أنت ترسل وكيل يدعو وظيفة. يعمل لمدة ثلاث دورات، ثم يحدث شيء خاطئ: النموذج يحاول أداة تعيد 500، المستخدم يغير رأيه في منتصف المهمة، أو الوكيل يقرر إعادة طلب دون توقيع بشري.`while True:`لا يمكنك أن تعيقه، لا يمكنك أن تعيد التفريغ، ولا يمكنك أن تتحول إلى "ماذا لو كان النموذج قد اختار الأداة الأخرى". في اللحظة التي ترسلها هذا بعد عرض تجريبي،

> أنت أصدرت وظيفة لتدعو الوكيل. عملت ثلاث دورات، ثم خرجت مشكلة: النموذج حاول إعادة 500 أداة، المستخدم في طريق تغيير رأيه، أو الوكيل قرر إرجاعها دون توقيع اصطناعي.`while True:`لا يوجد دورة. لا يمكنك إيقافها أو إرجاعها أو إعادة التوزيع إلى "ماذا سيحدث إذا اخترت النموذج أداة أخرى"

الخطوة التالية واضحة بمجرد رؤيتها الوكيل هو بالفعل آلة حالة  نظام استئناف بالإضافة إلى تاريخ الرسائل بالإضافة إلى المنتظرات الأداة مكالمات بالإضافة إلى العمل التالي. اجعل آلة الحالة واضحة: العقدة لـ "النموذج يفكر" "أداة تعمل" "إنسان يوافق" والحواف للانتقالات المشروطة بينها. بمجرد أن يكون الرسم البياني واضحًا ، يحصل الحزام على أربعة أشياء مجانًا: التفتيش (إنقاذ حالة بين الخطوات) ، والقاطع (وقف للإنسان) ، والتشغيل (الرموز التدريبية والأحداث المتوسطة) ، والسفر عبر الزمن (العودة إلى حالة سابقة ومحاولة فرع مختلف).

> بمجرد أن ترى، الخطوة التالية واضحة. العميل هو نفسه هو حالة من الجهاز.

لنجغراف هي المكتبة التي ترسل هذه الاستخراج. انها ليست إطار عميل في معنى لنجشين ("هنا عميل، حظا سعيدا"). انها وقت تشغيل الرسم البياني مع حالة من الدرجة الأولى، والثبات من الدرجة الأولى، والقطع من الدرجة الأولى. حلقة العميل هو شيء ترسم، وليس شيء تكتب يدويا.
إن تنفيذ مرجعية لهذا التجريد هو LangGraph. إنه ليس إطار عميل بمعنى LangChain ("هنا AgentExecutor ، حظاً طيباً"). إنه جدول تشغيل مع حالة من الدرجة الأولى ، ومثابرة من الدرجة الأولى ، ومقاطعات من الدرجة الأولى. حلقة العميل هي شيء ترسم ، وليس شيء تكتب به يدك.

> لاغراف هي المقدمة هذه المجموعة من الاختصارات. انها ليست في مفهوم لنج تشين الإطار الوكيل. انها هي واحدة من المواطنين المساواة الحالة الوطنية، والسكانية المثبتة والسكانية المقطوعة في التنفيذ.


> **【中文解读】**الميزة الأساسية لـ LangGraph هي دعم التدبير المعقد: دورة: (((الوكيل 遇到错误时重试) 、条件分支(وفقا لقياس المهام) 、 التصديق الاصطناعي ((高风险操作需要人工确认) 。

>  **【类比】**手写 ReAct 循环像在沙上画流程图画完就没了,潮水一冲就消失了。 LongGraph 像在白板上画流程图并保存每个节点("نموذج التفكير"、"工具执行"、"人工审批") و边边((条件跳转) كلها واضحة، يمكن فحص نقاط الاحتفاظ(暂停后继续) 时间旅行(عودة إلى بعض节试点不同分支) 、人工中断(等

> ️ **【易错点】**3 个坑: ((1) **状态 schema 太松散**用 `dict`عندما تكون هناك نوع من القيود، والفاصلة`TypedDict`أو نموذج بيدانتيك 定义 State。(2) **条件边写得太复杂** حافة 函数里 إذا / غيرها 嵌套 5 层,调试地狱; تفكيك إلى多个简单边 函数,每个返回单一节点名――(3) **checkpoint 用 SQLite 不持久化** إعادة تشغيل الخدمة في حالة فقدان؛ إنتاج باستخدام Postgres أو Redis القيام بمراقبة


## المفهوم الأساسي

> **【中文解读】**LangGraph 将 LLM Agent 建模为状态机(State Machine): تحديد الحالة 节点(如检索、生成、验证) و转换边 ((条件分支)  بالمقارنة بسيطة سلسلة التدريب، الحالة 支持循环、条件分支、人工审批等复杂控制流──

> **【拓展：LangGraph 与 Agent 编排】**لانغغراف هو الوكيل الذي أطلقته فريق لانغ تشين ، ويعزز:多 وكيل 协作、人工介入(Human-in-the-loop) 持久化状态、时间旅行调试――与 CrewAI(角色扮演 وكيل) وAutoGen(多 وكيل على المحادثة) مقارنة ، لانغراف 更适应需要精确控制流的复杂业务场景――


![LangGraph StateGraph: nodes, edges, and the checkpointer](../assets/langgraph-stategraph.svg)

أ`StateGraph`لديه ثلاثة أشياء

> `StateGraph`هناك ثلاثة أشياء

1. **State.**إشارة مدمجة (TypedDict أو نموذج Pydantic) التي تتدفق عبر الرسم البياني. كل عقدة تتلقى الحالة الكاملة وتعيد تحديثًا جزئيًا ، والذي يدمجها LangGraph باستخدام *reducer* لكل حقل `operator.add`بالنسبة لقوائم يجب أن تتراكم، إعادة كتابة حسب الاختيار.
   **状态。**流過图的类型化字典── كل节点收到完整状态并返回部分更新──
2. **Nodes.**وظائف Python `state -> partial_state`كل خطوة منفصلة: "تصل النموذج" "تشغيل الأدوات" "تجميع".
   **节点。**Python 函数 `state -> partial_state`كل واحد هو مجرد فصول
3. **Edges.**الانتقال بين العقد. الحواف الدولية تذهب إلى مكان واحد. الحواف الشروطية تأخذ وظيفة الجهاز التوجيه`state -> next_node_name`حتى يمكن أن تتفرق الرسم البياني على النموذج الخارجي.
   **边。**节点之间的转换──静态边去一个地方──条件边接受路由函数以在模型输出上分支──

تقوم بتجميع الرسم البياني. تقوم بتجميع يربط التطبيقات، ويربط نقطة التفتيش (اختيارية ولكن ضرورية للإنتاج) ، ويرجع إمكانية التشغيل. تستدعيها مع حالة أولية و `thread_id`كل خطوة من الإعدام تستمر بمراقبة معلقة`(thread_id, checkpoint_id)`. . .

> أنت تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدّلُ. تُعدُ. تُعدُ. تُعدُ. تُعدُ. تُعدُ. تُدُ.`thread_id`كل خطوة من عملياتها ستستمر في تحديد نقطة فحص

### القوى العظمى الأربعة

**Checkpointing.**كل انتقال عقد يكتب الحالة الجديدة إلى مخزن (في الذاكرة للتجارب، Postgres/Redis/SQLite للإنتاج). استأنف عن طريق استدعاء الرسم البياني مرة أخرى بنفس `thread_id`الرسم البياني يستمر من حيث توقف

> **检查点。**كل نقطة تحويل ستكتب حالة جديدة إلى مخزن.`thread_id`إعادة استخدام الرسم لتحسينها

**Interrupts.**قم بتشخيص العقدة`interrupt_before=["human_review"]`وتوقف التنفيذ قبل تشغيل تلك العقدة. الحالة لا تزال. API الخاص بك يستجيب للمستخدم مع "انتظار الموافقة". طلب لاحقا لنفس `thread_id`مع`Command(resume=...)`يستأنف الإعدام

> **中断。**استخدام`interrupt_before`标记一个节点,执行在该节点运行前停止――状态被持久化――后续请求可恢复执行――

**Streaming.** `graph.stream(state, mode="updates")`يُعطى الدولة ديلتا كما يحدث.`mode="messages"`يُدفق رموز الـ LLM داخل عقدة النموذج. `mode="values"`يُعطى صورًا مفصلة. تختار ما ستظهر في واجهتك التفاعلية.

> **流式输出。** `graph.stream`按发生顺序产出状态增量──你选择在 UI显示什么──

**Time-travel.** `graph.get_state_history(thread_id)`يعيد سجل المراقبة الكاملة. اجتياز أي سابقة `checkpoint_id`إلى`graph.invoke`و أنت تشرق من تلك النقطة. عظيم للتحليل ("ماذا لو كان النموذج قد اخترت الأداة B بدلا؟") و للاختبارات التراجعة التي تعيد تشغيل آثار الإنتاج.

> **时间旅行。**عودوا إلى النقطة التفتيشية الكاملة`checkpoint_id`، أنت من تلك النقطة المفترقة.

### القلص هو النقطة

كل حقل حالة لديه خفض. معظم الافتراضات تصلح  قيمة جديدة تغطي القديمة. ولكن القوائم الرسائل تحتاج `operator.add`لذا يتم إضافة رسائل جديدة بدلاً من استبدالها. الحواف المتوازية تجمع تحديثاتها من خلال القلل. إذا تم تحديث كلا العقدين`messages`و نسيتِ`Annotated[list, add_messages]`و الفائز الثاني في الصمت و تخسر نصف الجولة و القلل هو الشيء الوحيد الخفيف في المكتبة

> كل حالة في الحالة لديها خفض`operator.add`لتزييد المعلومات الجديدة بدلاً من البدولة.

### الرسم البياني ReAct في أربعة عقدات

وكيل ReAct الإنتاج هو أربع عقدين وعضوين:

> وكيل ReAct من الدرجة الإنتاجية هو أربع نقاط و 2 جانبي:

1. `agent` يدعو الجامعة مع تاريخ الرسالة الحالية. يعيد رسالة المساعد (التي قد تحتوي على tool_calls).
2. `tools` تنفيذ أي tool_calls في آخر رسالة المساعد، ويربط نتائج الأداة كرسائل الأداة.
3. حافة مشروطة من`agent`تلك الطرق إلى`tools`إذا كانت الرسالة الأخيرة تحتوي على tool_calls ، وإلا `END`. . .
4. حافة ثابتة من`tools`عودوا إلى`agent`. . .

هذا هو الأمر. تحصل على حلقة ReAct كاملة (الفكر → العمل → الملاحظة → الفكر → ...) مع التقاطع، والقطع، والتشغيل، في حوالي 40 سطر من الشفرة.

> هذا هو الحال. حصلت على دورة كاملة من ReAct. التفكير. التصرف. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير. التفكير.

### StateGraph vs Send (موقع)

`Send(node_name, state)`يسمح للعقد بإرسال المخططات الفرعية المتوازية. مثال: الوكيل يقرر استفسار ثلاثة متسابقين في وقت واحد. كل `Send`يخلق تنفيذ متوازي للعقدة المستهدفة؛ وتتدمج نتائجها من خلال خفض الحالة. هكذا يعبر لانغغغراف عن نمط الموسيقي-العمال دون خيط البدائيات.

> `Send(node_name, state)`让一个节点分派并行子图──每个 `Send`生成 هدف قطاع المواصلات التنفيذ؛ انتاجها من خلال خفض الحالة 合并。

### المخطوطات الفرعية

يمكن أن يكون الرسم البياني المجمّع عقدة في الرسم البياني الآخر. الرسم البياني الخارجي يرى عقدة واحدة؛ الرسم البياني الداخلي له حالته الخاصة ومراقبها الخاص. هكذا تقوم فرق بناء وكلاء عامل المشرف: يرسل الرسم البياني المشرف نية المستخدم إلى سبغراف عامل لكل نطاق.

> يمكن أن تكون الرسمة بعد التدوين هي النقطة في الرسمة الأخرى. الرسمة الخارجية ترى نقطة واحدة. الرسمة الداخلية لها حالةها الخاصة ومراقبة نقطة.

## بناء ذلك تحرك لتحقيق
```figure
l5-state-graph-ledger
```

## بناءها

### الخطوة الأولى: الحالة والعقد

> الخطوة الأولى: الحالة والقطعة

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

`add_messages`هو القيادة التي تجمع قائمة الرسائل بدلا من إعادة كتابتها. إنسيانها هو أخطاء LangGraph الأكثر شيوعا.

> `add_messages`هو جعل القائمة الإخبارية تتراكم وليس تغطي القلل... نسي أنه الأكثر شيوعا لاندغراف الأخطاء...

### الخطوة الثانية: تشغيل بشبكة

> الخطوة الثانية:

```python
config = {"configurable": {"thread_id": "user-42"}}
for event in app.stream(
    {"messages": [HumanMessage("find the Anthropic headquarters address")]},
    config,
    stream_mode="updates",
):
    print(event)
```

كل تحديث هو أمر`{node_name: state_delta}`. يمكن أن تقوم الجبهة بتدفق هذه إلى واجهة المستخدم حتى يرى المستخدمون "الوكيل يفكر...

> كل تحديث هو`{node_name: state_delta}`字典──前端可流式传到 UI,让用户看到"وكيل 思考中... 调用搜索_web... 得到结果... 回答中"──

### الخطوة الثالثة: إضافة الإنسان في الحلقة المقاطعة

قم بتشخيص العقدة حتى يتوقف التنفيذ قبل تشغيله

> الخطوة الثالثة: إضافة الإنسان إلى المشاركة في عملية التقطيع.

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

الحالة، نقطة التفتيش، والخيط يستمرون طوال المقاطعة لا يوجد شيء في الذاكرة إلا أثناء الإعدام

> حالة 、 نقطة التفتيش والخطوط في فترة الانقطاع كلها استمررت ٬ ما عدا فترة الإجراء، لا يوجد شيء في الذاكرة ٬

### الخطوة الرابعة: السفر عبر الزمن لإعداد التحليلات

> الخطوة الرابعة:

```python
history = list(app.get_state_history(config))
for snapshot in history:
    print(snapshot.values["messages"][-1].content[:80], snapshot.config)

# Fork from a prior checkpoint
target = history[3].config  # three steps back
for event in app.stream(None, target, stream_mode="values"):
    pass  # replay from that point forward
```

يمر`None`عندما تقوم المدخل بإعادة تشغيل من نقطة التفتيش المحددة؛ إعادة إعطاء قيمة يضيفها كتحديث لحالة نقطة التفتيش تلك قبل استئنافها. هكذا تقوم بإعادة تشغيل وكيل سيء دون إعادة تشغيل المحادثة بأكملها.

> 传入 `None`作为输入从给定的检查点重放;传输值则在恢复前将其作为更新添加到该检查点的状态――这就是如何在不重新运行整个对话的情况下复现一个错误的代理运行――

### الخطوة 5: تبادل نقطة التفتيش للإنتاج

> الخطوة 5: إنتاج البيئة بديل عن المراقبة

```python
from langgraph.checkpoint.postgres import PostgresSaver

with PostgresSaver.from_conn_string("postgresql://...") as checkpointer:
    checkpointer.setup()
    app = graph.compile(checkpointer=checkpointer)
```

(سكلايت) و (ريديس) و (بوسغريس) أرسلت`MemorySaver`أي شيء يستمر عبر إعادة التشغيل يريد متجر حقيقي

> SQLite、Redis 和 Postgres 已提供──`MemorySaver`كل شيء يحتاج إلى تخزين حقيقي

## المهارة

> أنتِ تبنيين العملاء كرسومات، وليس كـ`while True`حلقات
> أنتِ ستُبنيين العميل على الخطّ، وليس على الخطّ`while True`الحلقة

قبل أن تصل إلى لنجراف، قم بتصميم 60 ثانية:

> قبل استخدام LangGraph، قم بتصميم 60 ثانية:

1. **Name the nodes.**كل قرار منفصل أو عمل يؤثر جانبي هو عقدة. "الوكيل يفكر،" "الأداة تعمل،" "المراجع يوافق،" "تدفقات الاستجابة".
   **命名节点。**كل قرار أو حركة ضارة هي نقطة واحدة
2. **Declare the state.**الحد الأدنى من النمطDict مع خفض لكل حقل القائمة. لا تضع كل شيء في `messages`؛ رفع الحقول المحددة للمهمة (عمل`plan`، أ`budget`العداد، a `retrieved_docs`(قائمة) إلى المستوى الأعلى.
   **声明状态。**أحدث نوع من القواعد، كل قائمة
3. **Draw the edges.**ثابتة ما لم تعتمد الخطوة التالية على إصدار النموذج. كل حافة مشروطة تحتاج إلى وظيفة توجيه مع فرع مسمى.
   **画边。**إلا أن الخطوة التالية تعتمد على النموذج المخرج، وإلا استخدم الحدود الموقفة.
4. **Choose a checkpointer up front.** `MemorySaver`لا يتم شحن دون واحد  لا يوجد نقطة تفتيش لا تعني لا وجود ليرة الذكر، لا وجود لقطعة، لا وجود للسفر عبر الزمن.
   **提前选择检查点器。**测试用 `MemorySaver`, آخر استخدام Postgres/Redis/SQLite
5. **Decide interrupts before tools run, not after.**الموافقة تذهب على الحافة إلى عقدة تأثير جانبي حتى تتمكن من إلغاء قبل الضرر؛ التحقق من التحقق من التحقق من التحقق من النموذج حتى تتمكن من رفض المكالمات السيئة رخيصة.
   **在工具运行之前决定中断，而不是之后。**
6. **Stream by default.** `mode="updates"`للصفحة الواحدة، `mode="messages"`للتدفق على مستوى الرمز داخل عقدة النموذج ، `mode="values"`لقطات مفصلة خلال التقييم.
   **默认使用流式输出。**

رفض شحن وكيل لنجراف الذي لا يمتلك نقطة التفتيش رفض شحن واحد الذي يقاطع بعد التأثير الجانبي رفض شحن`messages`الحقل بدون`add_messages`كمخفضة لها

> رفض نشر أي عامل LangGraph من جهاز التفتيش. رفض نشر أي عامل بعد تعطل الجانب العضوي. رفض نشر أي عامل.`add_messages`كمخفض`messages`字段。

## تمارين التدريب

1. **Easy.**تنفيذ الرسم البياني ReAct الأربعة العقدة أعلاه مع أداة الحاسبة و أداة بحث الويب. تحقق من أن `list(app.get_state_history(config))`يعود أربع نقاط تفتيش على الأقل للحوار المزدوج.
   **简单。**实现上述四节点 ReAct 图,验证检查点历史记录──
2. **Medium.**إضافة`planner`العقدة التي تمر قبلها`agent`وكتب كتابة منظمة`plan: list[str]`إلى الولاية`agent`علامة خطة الخطوات كما فعلت. فشل في الاختبار إذا`plan`ضاعت في سيرته الذاتية في نقطة التفتيش (المخفض الخاطئ).
   **中等。**إضافة واحدة في`agent`之前运行的 `planner`节点,写入结构化计划到状态中──
3. **Hard.**بناء الرسم البياني للإشراف الذي يتوجب بين ثلاث صور فرعية (`researcher`،`writer`،`reviewer`) باستخدام `Send`كل فرعي لديه حالته ومراقبه الخاص`interrupt_before=["writer"]`على الرسم البياني الخارجي حتى يستطيع الإنسان الموافقة على البحث المختصر. تأكيد أن السفر عبر الزمن من نقطة تفتيش سابقة يعد فقط الفرشة المفترقة.
   **困难。**بناء مشرف 图, بين ثلاثة صور استخدام `Send`-المركز

## شروط الرئيسية

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

## المزيد من القراءة

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) الإشارة القنوية لـ StateGraph، والخفضات، والمركبات التفتيشية، والقاطعات.
  LangGraph 文档StateGraph、reducer、检查点器和中断的权威参考──
- [LangGraph concepts: state, reducers, checkpointers](https://langchain-ai.github.io/langgraph/concepts/low_level/)النموذج العقلي الذي تستخدمه هذه الدروس مباشرة من المصدر
  لنجراف 概念: حالة ‬مقلل ‬مراقبة ‬مراقبة ‬
- [LangGraph Persistence and Checkpoints](https://langchain-ai.github.io/langgraph/concepts/persistence/) التفاصيل على متاجر Postgres/SQLite/Redis، ومناطق أسماء نقاط التفتيش، وتعريفات الأسلاك.
  لنجراف 持久化和检查点详情
- [LangGraph Human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/) `interrupt_before`،`interrupt_after`،`Command(resume=...)`، و النمط من إصدار الحالة.
  لانغغراف 人机协作断和恢复 模式──
- [Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023)](https://arxiv.org/abs/2210.03629) النمط الذي ينفذ كل وكيل لنجراف؛ اقرأه للحصول على دليل التفكير.
  كل وكيل لنجراف ينجح في تنفيذ نظام ReAct
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) أي أشكال الرسم البياني (سلسلة، راوتر، موظف أوركستراتور، مقدم تقييم-تحسين) تفضل ومتى.
  الأنثروبية حول اختيار أي نوع من الصور ومعرفة متى تستخدم
- المرحلة 11 · 09 (تدعو الوظيفة)  أداة-دعوة البدائية كل عقدة عامل LangGraph إعادة استخدامها.
  第 11 阶段 · 09(函数调用) 每个 LangGraph Agent 节点重用工具调用原语。
- المرحلة 11 · 14 (مثال بروتوكول السياق)  اكتشاف أداة خارجية تتصل مع LangGraph `ToolNode`عبر جهاز التكيف MCP
  第 11 阶段 · 14(MCP) 通过MCP 适配器插入 LangGraph `ToolNode`أدوات خارجية
- المرحلة 11 · 17 (تبادلات إطار العملاء)  متى لاختيار LangGraph على CrewAI، AutoGen، أو Agno.
  第 11 阶段 · 17(وكيل 框架对比) 何时选择 LangGraph。
