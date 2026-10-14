# افتتاح التليمتر GenAI مؤتمرات تعريفية

> تعريف نظام GenAI SIG (الذي تم إطلاقه في أبريل 2024) للعملاء التلفزيونية. اسمات المجال والخصائص وقواعد استيراد المحتوى تتقارب بين البائعين بحيث تعني آثار العملاء نفس الشيء في Datadog و Grafana و Jaeger و Honeycomb.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 24 (Observability Platforms) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## أهداف التعلم

- أسمائ فئات المدى GenAI: النموذج/العميل، وكيل، الأداة.
- التمييز`invoke_agent`المستهلك مقابل المستهلك الداخلي و عندما ينطبق كل منهما
- قم بإدراج صفات GenAI على المستوى الأعلى: اسم المقدم، نموذج الطلب، معرف مصدر البيانات.
- شرح عقد استيعاب المحتوى: الاختيار`OTEL_SEMCONV_STABILITY_OPT_IN`، توصية مرجعية خارجية.

## المشكلة المشكلة المشكلة

> **【中文解读】**كل مزود يطور نطاقه الخاص، ويتطلب النظام في النهاية من كل إطار بناء جهاز أجهزة مستقلة.

كل مبيع يختلق أسماء فترة عمله الخاصة. فرق العمليات تنتهي بناء لوحة التحكم لكل إطار. إعدادات OpenTelemetry GenAI SIG تصحيح هذا عن طريق تعريف معيار واحد أهداف النظام الإيكولوجي بأكمله.

> كل مزود يطور نطاقه الخاص 名称──运维团队 في النهاية بحاجة إلى بناء إطار مستقل لكل إطار.

> **【拓展：OTel GenAI 规范的跨平台统一】**OpenTelemetry GenAI 语义约定 (2024年4月启动) 定义 Agent 遥测的标准方案:span 名称、属性和内容捕获规则跨供应商统一,使 Agent 追踪在 Datadog、Grafana、Jaeger 和 Honeycomb 中具有相同语义──一次埋点,多后端通用──

>  **【前置】**تعلمون:                                                                                                                                                                                                                                                              

## المفهوم الأساسي

### فئات المجال

>  **【类比】**تمتد ثلاث فئات من OTel GenAI على نطاق 像医院的分级诊疗记录:**Model span**هو تجربة واحدة ((أسفل المستوى، سجل"سحب الكثير من الدم"",بأي أداة"",نتائج كم" على الرد على الرمز عدد**Agent span**يمناسب معظم المرضات من المرض إلى المرض، ويتضمن العديد من التجارب.**Tool span**هو المشاريع المراقبة (مقاطع)`parent_span_id`链回父记录这样 Datadog 里你能展开看: كل العميل 调用 → 5 مرات الوسائل 调用 → كل مرة الوسائل 调用里 2 مرات الجامعة 调用。

1. **Model / client spans.**تغطي مكالمات LLM الخام. تم إصدارها من قبل SDKs (Anthropic، OpenAI، Bedrock) ومعدلات نموذج الإطار.
2. **Agent spans.** `create_agent`(عندما يتم بناء الوكيل) و `invoke_agent`(عندما يدير)
3. **Tool spans.**واحد لكل دعوة أداة، متصلة مع فترة الوكيل عن طريق علاقة الوالد والطفل.

### اسم العميل span

- اسم الإسبانية: `invoke_agent {gen_ai.agent.name}`إذا كان اسمها ، فلنقل إلى `invoke_agent`. . .
- نوع من النوع:
  - **CLIENT** لخدمات الوكلاء عن بعد (OpenAI Assistants API، Bedrock Agents).
  - **INTERNAL** لأطر العمليات العملية (LangChain، CrewAI، ReAct المحلية).

### الصفات الرئيسية

- `gen_ai.provider.name` `anthropic`،`openai`،`aws.bedrock`،`google.vertex`. . .
- `gen_ai.request.model`هوية النموذج
- `gen_ai.response.model` النموذج الذي تم حلّه (قد يختلف عن الطلب بسبب التوجيه).
- `gen_ai.agent.name` معرف الوكيل
- `gen_ai.operation.name` `chat`،`completion`،`invoke_agent`،`tool_call`. . .
- `gen_ai.data_source.id` لـ RAG: أي مجموعة أو مخزن تم استشارته.

توجد اتفاقيات محددة للتكنولوجيا لـ Anthropic، Azure AI Inference، AWS Bedrock، OpenAI.

> OpenTelemetry GenAI 语义约定 حددت المعايير المرئية لـ LLM و Agent.`gen_ai.request.model`.`gen_ai.usage.input_tokens`.`gen_ai.agent.name`... و هكذا

### التقاط المحتوى

> ️ **【易错点】**المشهد: المطور`invoke_agent`span 里把完整提示(含用户 PII、API key、客户合同条款) كخصية 直接塞进去 → 后果:运维在Jaeger 网页里点开就能看到所有明文,Datadog 还会索引做全文检索,等于把合规风险扩散到整个观测链路 → 修复:默认关闭内容捕获,需要时只在 span 里存指针 ID如`gen_ai.input.message_id=row42`),原文落到带 ACL的对象存储 S3 里,运维要查时通过 ID 跳转授权访问──这就是本节反复强调的"وصية مرجع خارجي"──

القاعدة الافتراضية: لا يجب أن تستقطب الأدوات المدخلات / المخرجات الافتراضية. يتم اختيار الاستقطاب عبر:

> OpenTelemetry GenAI 语义约定 حددت المعايير المرئية لـ LLM و Agent.`gen_ai.request.model`.`gen_ai.usage.input_tokens`.`gen_ai.agent.name`... و هكذا

- `gen_ai.system_instructions`
- `gen_ai.input.messages`
- `gen_ai.output.messages`

نمط الإنتاج الموصى به: تخزين المحتوى خارجيًا (S3 ، مخزن السجل الخاص بك) ، سجل الإشارات على المدى (معرفات المؤشر ، وليس النص). هذا هو الدروس 27 دفاع عن التسمم المحتوى معالجة إلى قابلية للملاحظة.

> نموذج الإنتاج: 将内容外部存储(S3、你的日志存储),在 span 上记录引用(指针 ID,不是原文) 

> OpenTelemetry GenAI 语义约定 حددت المعايير المرئية لـ LLM و Agent.`gen_ai.request.model`.`gen_ai.usage.input_tokens`.`gen_ai.agent.name`... و هكذا

### الاستقرار

معظم المؤتمرات تجربية اعتبارا من مارس 2026. اختر المشاهدة المسبقة المستقرة مع:

> OpenTelemetry GenAI 语义约定 حددت المعايير المرئية لـ LLM و Agent.`gen_ai.request.model`.`gen_ai.usage.input_tokens`.`gen_ai.agent.name`... و هكذا

```
OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental
```

خرائط Datadog v1.37+ تعود GenAI بشكل طبيعي إلى مخطط ملاحظة LLM. الدعم الخلفي الآخر (Grafana، Honeycomb، Jaeger) للمعايير الخام.

> 🤔 **【困惑】**س: `invoke_agent`span 什么时候标 client,什么时候标 INTERNAL? تبدو جيدة حولها. A: 看被调用代理不是"另一个进程/服务"。 إذا كنت مباشرة في Python 进程 وارد LangChain 运行 ReAct، فإنه INTERNAL你自己代码内的子调用── إذا كنت تدعو OpenAI مساعدين API أو AWS Bedrock Agents، فهذا بعيد عن HTTP 调用،标 client。CLIENT span أيضا سوف تتم تلقائيا مع RPC 相关属性 مثل(`rpc.system`.`rpc.service`), سهولة و تقليدية خدمة التتبع على جميع

> Datadog v1.37+ 原生将 GenAI 属性映射到其LLM ملاحظة النظام.

> OpenTelemetry GenAI 语义约定 حددت المعايير المرئية لـ LLM و Agent.`gen_ai.request.model`.`gen_ai.usage.input_tokens`.`gen_ai.agent.name`... و هكذا

### حيث يذهب هذا النمط خطأ

- **Capturing full prompts in spans.**المعلومات الشخصية، السرّات، بيانات العملاء في أثر يمكن للعمليات قراءة.
- **No `gen_ai.provider.name`.**تختفي لوحة التحكم متعددة المزودين عندما يفتقر الخصيص.
- **Spans without parent links.**أدوات اليتامى تتفوق دائماً على النطاق
- **Not setting stability opt-in.**قد يتم إعادة تسمية صفاتك عند تحديث الخلفية.

> **在 span 中捕获完整提示。**运维可以读取的追踪包含 PII、密钥、客户数据──存储外部──
> **缺少 `gen_ai.provider.name`。**缺少归属时,多供应商仪表盘会出错.
> **没有父链接的 span。**孤立的工具 span──始终传播上下文──
> **不设置稳定性选择加入。**قد يتم إعادة تسمية صفاتك في مرحلة التطوير

## بناء ذلك تحرك لتحقيق
```figure
ae-genai-span-tree
```

## بناءها

`code/main.py`ينفذ مستثمر مضربة مدة ستدليب يطابق اتفاقيات جناي:

> OpenTelemetry GenAI 语义约定 حددت المعايير المرئية لـ LLM و Agent.`gen_ai.request.model`.`gen_ai.usage.input_tokens`.`gen_ai.agent.name`... و هكذا

- `Span`مع مخطط صفة GenAI.
- `Tracer`مع`start_span`، سياقات متضمنة
- وكيل مسجل يطلق:`create_agent`،`invoke_agent`(داخلية) ، على كل أداة، `chat`المدة المطلوبة لطلبات الجامعة
- وضع التقاط المحتوى الذي يحفظ الإشارات الخارجية ويستسجل الهويات على المدة.

إشغله

```
python3 code/main.py
```

الناتج: شجرة المدى مع جميع صفات GenAI المطلوبة، و"متجر خارجي" يظهر مراجع المحتوى الاختيار.

> 输出: واحد يحتوي على كل الوصف المطلوب من GenAI 属性 树, فضلا عن واحد يظهر اختيار加入内容引用的"خزنة خارجية"

> OpenTelemetry GenAI 语义约定 حددت المعايير المرئية لـ LLM و Agent.`gen_ai.request.model`.`gen_ai.usage.input_tokens`.`gen_ai.agent.name`... و هكذا

## استخدمها في إطار التنفيذ

- **Datadog LLM Observability**(v1.37+) خرائط خصائص الأصلية.
- **Langfuse / Phoenix / Opik**(الدرس 24)  الآلة الذاتية النظام البيئي.
- **Jaeger / Honeycomb / Grafana Tempo** آثار OTel خام؛ بناء لوحة التحكم من صفات GenAI.
- **Self-hosted** تشغيل مجموعة OTel مع معالج GenAI.

## أرسلها .

`outputs/skill-otel-genai.md`الأسلاك OTel GenAI تمتد إلى وكيل موجود مع إيقاع المحتوى وتخزين المراجع الخارجية.

> `outputs/skill-otel-genai.md`لن يكون هناك أيّة إضافة إلى الوكيل الحالي، ويحتوي على المحتوى الذي يتمّ استيعاب القيمة المتخفّة والخزين الخارجي للمشاركات.

> OpenTelemetry GenAI 语义约定 حددت المعايير المرئية لـ LLM و Agent.`gen_ai.request.model`.`gen_ai.usage.input_tokens`.`gen_ai.agent.name`... و هكذا

## تمارين التدريب

1. أداة دراستك 01 إعادة التأثير مع`invoke_agent`(داخلية) + امتدادات لكل أداة. أرسل إلى مثال جيجر.
  中文翻译: التفكير并实践此练习。
2. إضافة التقاط المحتوى في وضع "المراجع فقط": الإشعارات إلى SQLite، سمات المدة تحمل فقط أجهزة تعريف الصف.
  中文翻译: التفكير并实践此练习。
3. اقرأ المواصفات`gen_ai.data_source.id`. إدفعها إلى بحثك عن الدروس 09
  中文翻译: التفكير并实践此练习。
4. المجموعة`OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`وتحقق من أن صفاتك لا تُعيد اسمها من قبل المجمع
  中文翻译: التفكير并实践此练习。
5. بناء لوحة التحكم: "أي أخطاء أداة تتصل مع أي نماذج" من صفات GenAI وحدها.
  中文翻译: التفكير并实践此练习。

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| GenAI SIG | "OpenTelemetry GenAI group" | OTel working group defining the schema |  |
| invoke_agent | "Agent span" | Name of the span representing an agent run |  |
| CLIENT span | "Remote call" | Span for a call to a remote agent service |  |
| INTERNAL span | "In-process" | Span for an in-process agent run |  |
| gen_ai.provider.name | "Provider" | anthropic / openai / aws.bedrock / google.vertex |  |
| gen_ai.data_source.id | "RAG source" | Which corpus/store a retrieval hit |  |
| Content capture | "Prompt logging" | Opt-in capture of messages; store externally in prod |  |
| Stability opt-in | "Preview mode" | Env var to pin experimental conventions |  |

## المزيد من القراءة

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) المواصفات
  中文翻译:见原文──
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) تمتد GenAI حسب الافتراض
  中文翻译:见原文──
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) امتدادات OTel مدمجة في
  中文翻译:见原文──
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) W3C تعقب النطاق الانتشار
  中文翻译:见原文──
