# وظيفة الاتصال واستخدام الأدوات

> الـ"إلإم" لا يمكنها فعل أي شيء يُنشئون رسائل نصية هذه هي القدرة الكاملة لا يمكنهم التحقق من الطقس، أو استفسار قاعدة بيانات، أو إرسال رسالة بريد إلكتروني، أو تشغيل رمز، أو قراءة ملف. كل "وكيل الذكاء الاصطناعي" رأيته هو LLM الذي يولد JSON الذي يقول ما هي الوظيفة التي يجب الاتصال بها -- ثم رمزك الذي يدعوها فعلاً. النموذج هو الدماغ. الأدوات هي اليدين الدعوة الوظيفية هي الجهاز العصبي الذي يربطهم.

> **【中文解读】**LLM فقط يمكن أن تولد النص.

> **【拓展：Function Calling→MCP与Agent】**الدعوة الوظيفية هي الجهاز الأساسي لـ AI Agent، و على أساس هذا، قامت بروتوكول MCP بتعظيم وصف الأدوات وتطبيق العمليات، وهي بروتوكول أساسي للطريقة التي يستخدمها كلود.

>  **【前置】**学本节前请先掌握:(1) المرحلة 11·01(التجهيزات السريعة) فهم LLM 如何处理快速;(2) المرحلة 11·03(المخرجات المهيكلة) فهم JSON Schema,本节重度依赖;(3) Python 字典、JSON 序列化、尝试/except 异常处理──如果 لا تكتب JSON Schema,先看 jsonschema 库文档本节不会从头讲──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 Lesson 03 (Structured Outputs) | **前置知识:** Phase 11 · 03 (结构化输出)
**Time:** ~75 minutes | **时间:** ~75 分钟
**Related:**المرحلة 11 · 14 (مثال بروتوكول السياق)  عندما يتم مشاركة أداة عبر مضيفات، التخرج من الدعوة الوظيفة المحمولة إلى خادم MCP. هذا الدروس يغطي الحالة المحمولة؛ MCP يغطي الحالة بروتوكول. **相关:**المرحلة 11 · 14 (模型上下文协议)  عندما تحتاج الأدوات إلى عبور المشترك، من وظيفة داخلية调用升级 إلى MCP 服务器。本课讲内联场景;MCP 讲协议场景。

## أهداف التعلم

- تنفيذ حلقة استدعاء الوظيفة: تحديد مخططات الأدوات ، تحليل JSON للدعوة الأدوات للنموذج ، تنفيذ الوظائف ، وإعادة النتائج
  实现函数调用循环:定义工具 schema、解析模型的工具调用 JSON、执行函数并返回结果
- مخططات أدوات التصميم مع وصف واضح ومعايير منخفضة يمكن أن تستند إليها النموذج بشكل موثوق
  تصميم مخطط أداة مع وصف واضح وعنبرات التصنيف، مما يجعل النموذج قادر على التدوين بشكل موثوق
- بناء حلقة وكيل متعددة التحولات التي تتسلسل العديد من المكالمات الوظيفية للإجابة على الأسئلة المعقدة
   بناء وكيل متعددة الجوانب 循环, سلسلة دعوة العديد من الوظائف للإجابة على استفسارات معقدة
- وظيفة التعامل تدعو الحافة الحالات: مكالمات الأدوات المتوازية، انتشار الخطأ، ومنع حلقات الأدوات المتنامية
  处理函数调调的边缘情况:并行工具调用、错误传播和防止无限工具循环

> **【中文解读】**هذا هو بناء النموذج من خلال استخدام البحث، قاعدة بيانات، و API وغيرها من الأدوات للحصول على المعلومات والتنفيذ العملية.


## المشكلة المشكلة المشكلة

تقوم ببناء جهاز دردشة، يطلب المستخدم: "ما هو الطقس في طوكيو الآن؟"

> أنت بنيت جهاز دردشة.

يستجيب النموذج: "ليس لدي إمكانية الوصول إلى بيانات الطقس في الوقت الحقيقي، ولكن بناءً على الموسم،

> 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复 模型回复

هذا هلوسة مرتدية في إعلان عدم المسؤولية النموذج لا يعرف الطقس لن يعرف أبدا الطقس يتغير كل ساعة بيانات التدريب النموذج هي شهور

> هذا هو شعور الحالة الحرة. النموذج لا يعرف الطقس، ولا يعرف أبدا. الطقس يتغير كل ساعة.

الإجابة الصحيحة تتطلب الاتصال بـ OpenWeatherMap API، والحصول على درجة الحرارة الحالية، وعودة الرقم الحقيقي. النموذج لا يمكن أن يدعو API. رمزك يمكن. الجزء المفقود: بروتوكول مهيكلي يسمح للنموذج أن يقول "أحتاج إلى الاتصال بـ API الطقس مع هذه الحجج" ويسمح لكودك بتنفيذها وإعادة إرسال النتيجة.

> صحيح جواب تحتاج إلى تعديل OpenWeatherMap API.

هذا هو الدعوة للعمل. النموذج يخرج JSON مهيكلا يصف الوظيفة التي يجب استدعائها مع أي حجج. تطبيقك يقوم بتنفيذ الوظيفة. النتيجة تعود إلى المحادثة. النموذج يستخدم النتيجة لإنتاج إجابته النهائية.

> هذا هو استخدام الوظيفة. النموذج أوتوت هيكل JSON  وصف ما هي الوظيفة التي يجب استخدامها.

بدون طلب وظيفي، الـ"إللي" هي موسوعات معناها، يصبحون وكلاء.

> لا يوجد وظيفة تستخدم، وكل شيء هو علمي.

>  **【类比】**LLM 像一位"嘴强王者"能讲清楚任何概念,但不能动手──函数调用就是给这位嘴强王者配一个"小弟"系统:它说"小弟,去查东京天气"→小弟照做→回来报告"18度阴天"→它转述给用户──模型从不离开王座(生成代币),但通过发号施令(JSON) 和接收战报(工具_结果),它可以调用整个外部世界──

## المفهوم الأساسي

> **【中文解读】**函数调用 (Function Calling) جعل LLM 生成结构化工具调用请求، وليس مجرد نصوص回复.

> **【拓展：函数调用与 Agent 系统】**تم إطلاق OpenAI في عام 2023 ، ويعمل بالفعل على استخدامها و استخدامها بشكل قاطع.


### الوظيفة التي تدعو إلى الحلقة

كل تفاعل استخدام الأدوات يتبع نفس حلقة 5 خطوات.

> كل مرة تستخدم فيها الأدوات تتبع نفس دورة الخمس خطوات.

```mermaid
sequenceDiagram
    participant U as User
    participant A as Application
    participant M as Model
    participant T as Tool

    U->>A: "What's the weather in Tokyo?"
    A->>M: messages + tool definitions
    M->>A: tool_call: get_weather(city="Tokyo")
    A->>T: Execute get_weather("Tokyo")
    T->>A: {"temp": 18, "condition": "cloudy"}
    A->>M: tool_result + conversation
    M->>A: "It's 18C and cloudy in Tokyo."
    A->>U: Final response
```

الخطوة الأولى: يرسل المستخدم رسالة. الخطوة 2: يتلقى النموذج الرسالة جنبا إلى جنب مع تعريفات الأداة (خطة JSON تصف الوظائف المتاحة). الخطوة الثالثة: بدلاً من الرد بالنص، يقوم النموذج بإخراج طلب أداة -- وهو جسم JSON مهيكلي مع اسم الوظيفة والحجج. الخطوة الرابعة: يقوم رمزك بتنفيذ الوظيفة ويستقطب النتيجة. الخطوة 5: والنتيجة تعود إلى النموذج، والذي لديه الآن بيانات حقيقية لإنتاج إجابته النهائية.

> الخطوة 1: إرسال المستخدم رسالة. الخطوة 2: نموذج تلقي الرسائل و وصف الأدوات. الخطوة 3: النموذج لا يعود إلى النص، ولكن الاستخدام الأدوات المصدرة يحتوي على اسم وظيفة وعناصر من المكونات.

النموذج لا ينفذ أي شيء، إنه يقرر فقط ما الذي يجب أن يُدعى به وبأي حجج.

> النموذج لا يقوم بأي شيء. إنه يقرر فقط ما يستخدم.

> 🤔 **【困惑】**س: لماذا لا يقوم النموذج مباشرة بإجراء الكود؟**隔离** نموذج في الصندوق خارج التنفيذ سيكون آمن                                                                                                                                                                                                                                                       **可观测** تنفيذ في عمليةك، 能加日志、限流、审计؛**可移植** نفس النموذج قادر على التحرك مختلف اللغات 

### تعريفات الأداة: عقد مخطط JSON

يتم تعريف كل أداة بواسطة مخطط JSON الذي يخبر النموذج بما تفعله الوظيفة وما هي الحجج التي تستغرقها وما هي أنواع الحجج التي يجب أن تكون.

> كل أداة يتم تعريفها بواسطة نظام JSON ، أخبر النموذج ما يجب أن تفعله هذه الوظيفة ، وافق على ما هو العيار ، و يجب أن يكون العيار نوعاً ما.

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get current weather for a city. Returns temperature in Celsius and conditions.",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "City name, e.g. 'Tokyo' or 'San Francisco'"
        },
        "units": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"],
          "description": "Temperature units"
        }
      },
      "required": ["city"]
    }
  }
}
```

- نعم`description`النموذج يقرأها لتحديد متى وكيفية استخدام الأداة. وصف غامض مثل "يحصل الطقس" ينتج اختيار أداة أسوأ من "حصل على الطقس الحالي لمدينة. يعيد درجة الحرارة في مئوية والظروف".

> `description`字段至关重要──模型读这些描述来决定何时以及如何使用工具──模糊描述如"获取天气"产生的工具选择效果差于"获取城市当前天气,回归摄氏度温度和天气状况"──描述本身就是工具选择的提示──

> ️ **【易错点】**工具描述的 3 个坑: ((1) **描述太短**"حصول البيانات" هذا التصفية،模型分不清该使用 `get_weather`و كذلك`get_stock_price`,会乱选;修复: كل وصف على الأقل 30 字,写清"做什么 + 输入 + 输出"―(2) **描述互相重叠**دو工具都写"获取信息",模型选哪个全凭运气;修复:每个描述强调独特场景("获取实时天气" vs "获取历史天气")**隐藏前置条件** مثل `delete_file(path)` بحاجة أولا `confirm()`ولكن التوصيف لا يقول، أن النموذج سوف يزيل مباشرة.

### مقارنة المزودين

كل مزود رئيسي يدعم الدعوة الوظيفية، ولكن سطح API يختلف.

> كل مزود رئيسي يدعم وظيفة تدوين، ولكن API 接口 مختلفة.

| Provider | API Parameter | Tool Call Format | Parallel Calls | Forced Calling |
|----------|--------------|-----------------|---------------|----------------|
| OpenAI (GPT-5, o4) | `tools` | `tool_calls[].function` | Yes (multiple per turn) | `tool_choice="required"` |
| Anthropic (Claude 4.6/4.7) | `tools` | `content[].type="tool_use"` | Yes (multiple blocks) | `tool_choice={"type":"any"}` |
| Google (Gemini 3) | `function_declarations` | `functionCall` | Yes | `function_calling_config` |
| Open-weight (Llama 4, Qwen3, DeepSeek-V3) | Native `tools` on Llama 4; Hermes or ChatML on others | Mixed | Model-dependent | Prompt-based or `tool_choice` if supported |

بحلول عام 2026، تجمع المقدمون الثلاثة المغمورين على أشكال متطابقة تقريبا على أساس JSON-Schema.`tools`المجموعة المشتركة من أدوات المضيفين، تفضل MCP (مرحلة 11 · 14) على الدعوة الوظيفة الداخلية  الخادم هو نفسها لجميعهم.

> بحلول عام 2026، تم الاتجاه إلى ثلاثة مزودي مصدر مغلق تقريبا نفسها على أساس نظام JSON.`tools`字段匹配 OpenAI 结构──开源权重微调模型仍然各异Hermes 格式──NousResearch) هي الأكثر شيوعاً في الجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع للجهاز التابع إلىجهاز التابع للجهاز.

### اختيار الأدوات: تلقائي، مطلوب، محدد

أنت تتحكم عندما تستخدم النموذج الأدوات.

> يمكنك التحكم في النموذج عندما تستخدم الأدوات

**Auto**(الابتكار): يقرر النموذج ما إذا كان يجب استدعاء أداة أو الإجابة مباشرة. "ما هو 2 + 2؟" -- يستجيب مباشرة. "ما هو الطقس؟" -- يطلق على الأداة.
**自动（默认）**: النموذج نفسه يقرر هو استخدام أداة أم مباشرة الردود.

**Required**يجب أن يطلب النموذج أداة واحدة على الأقل. استخدم هذا عندما تعرف أن نية المستخدم تتطلب أداة. يمنع النموذج من التخمين بدلاً من البحث عن البيانات الحقيقية.
**必需**يجب أن تستخدم على الأقل أداة واحدة عندما تعرف بشكل واضح أن المستخدم يريد استخدام الأداة

**Specific function**: إجبار النموذج على استدعاء وظيفة معينة. `tool_choice={"type":"function", "function": {"name": "get_weather"}}`يضمن أداة الطقس يتم استدعائها، بغض النظر عن الاستفسار. استخدم هذا للتوجيه -- عندما منطق فوق التيار بالفعل تحدد أداة مطلوبة.
**特定函数**: النموذج الضابطي لتنظيم وظيفة معينة`tool_choice={"type":"function", "function": {"name": "get_weather"}}`ضمان أدوات الطقس يتم استخدامها، بغض النظر عن ما هو الاستفسار.

### مكالمة الوظيفة المتوازية

يمكن أن تقوم GPT-4o وClaude بدعوة وظائف متعددة في جولة واحدة. يسأل المستخدم: "ما هو الطقس في طوكيو ونيويورك؟" النموذج يخرج مكالمات أداة اثنين في وقت واحد:

> GPT-4o و Claude يمكن استخدامها في دورة واحدة.

```json
[
  {"name": "get_weather", "arguments": {"city": "Tokyo"}},
  {"name": "get_weather", "arguments": {"city": "New York"}}
]
```

يقوم رمزك بتنفيذ كلتا (في المثالية في وقت واحد) ، ويستعيد كلا النتائج ، ويجمع النموذج استجابة واحدة. وهذا يقلل من رحلات ذهاب وإياب من 2 إلى 1. بالنسبة للعملاء الذين لديهم 5-10 مكالمات أداة لكل استفسار ، يقلل الاتصال الموازي من التأخير بنسبة 60-80٪.

> تعديل المعلومات عن المعلومات المختلفة، والتي تُستخدم في كل استفسار، وتُعديل المعلومات المختلفة، والتي تُعديل المعلومات المختلفة.

> ️ **【易错点】**وَعَمِلَتْ تَعَمُّلَتَيْنِ:**顺序依赖未声明** مستخدم يسأل "أول مرة بحث A شركة أسعار الأسهم، مرة أخرى بحث B شركة"،模型可能并行调用两个 `get_price`ولكن لا يمكنك ضمان العودة الأولى`get_price`工具的描述 写明"用于独立查询",需要顺序时使用 `compare_stocks(A, B)`单工具封装──(2) **共享状态竞争**并行调用 `increment_counter()`两次,结果只增加 1;修复:工具实现里加锁,或让模型串行调用副作用工具──

### الخروج المهيكلي مقابل الدعوة إلى الوظيفة

درس 03 كان يغطى المخرجات المهيكلة. تستخدم دعوة الوظائف نفس آلة JSON Schema، ولكن لأغراض مختلفة.

> الدرس 03 讲述结构化输出―― وظيفة调用相同 JSON Schema 机制,但目的不同――

**Structured outputs**: إجبار النموذج على إنتاج البيانات في شكل معين. الخروج هو المنتج النهائي.`{name, price, in_stock}`. . .
**结构化输出**: النموذج الضروري حسب شكل معين لتوليد البيانات.`{name, price, in_stock}`.

**Function calling**: يعلن النموذج عن نية لتنفيذ إجراء. إن الخروج هو خطوة متوسطة.`get_weather(city="Tokyo")`-- النموذج يطلب إجراءً، وليس يقدم الإجابة النهائية.
**函数调用**: نموذج بيان تنفيذ بعض الحركات قصدها.`get_weather(city="Tokyo")` نموذج في طلب حركة، ليس أن تكون إجابة نهائية.

استخدم الخروجات المهيكلة عندما تريد استخراج البيانات. استخدم الدعوة الوظيفية عندما تريد أن يتفاعل النموذج مع الأنظمة الخارجية.
القيام بإستخراج البيانات عند استخدام الخروج المهيكلي.

### الأمن: القواعد غير المتفاوضة

إن الدعوة إلى الوظائف هي أكثر القدرات خطورة يمكنك إعطاءها لـ LLM. يختار النموذج ما يجب تنفيذه. إذا كانت مجموعة الأدوات الخاصة بك تشمل استفسارات قاعدة البيانات، يقوم النموذج ببناء الاستفسارات. إذا كان يشمل أوامر القبو، يقوم النموذج بكتابتها.

> 函数调用是你赋予 LLM 最危险的能力──模型决定执行什么── إذا كان مجموعتك من الأدوات تحتوي على استفسارات قاعدة البيانات، فإن模型 سوف تشكل استفسارات语句──如果包含 shell 命令، فإن模型 سوف تكتب أوامر──

**Rule 1: Never pass model-generated SQL directly to a database.**يمكن النموذج ولن يخلق طاولة DROP، حقن UNION، أو استفسارات التي تعود كل سطر. دائما تعريف. دائما التحقق من الصلاحية. دائما استخدام قائمة المسموحات من العمليات.
**规则 1：永远不要把模型生成的 SQL 直接传给数据库。**模型会(也会)生成 DROP TABLE、UNION 注入或返回所有人的查询──始终参数化──始终校验──始终使用操作白名单──

**Rule 2: Allowlist functions.**النموذج لا يمكن أن يدعو إلا وظائف تعريفها صراحة. أبداً بناء عام "تنفيذ أي وظيفة باسم" أداة. إذا كان لديك 50 وظيفة داخلية، كشف فقط 5 المستخدم يحتاج.
**规则 2：函数白名单。**模型只能调用你明确义的函数――永远不要做通用"按名执行任意函数"工具──如果有50函数内部,只暴露用户需要的5函数──

**Rule 3: Validate arguments.**قد يمر النموذج اسم مدينة`"; DROP TABLE users; --"`. تأكيد كل حجج ضد الأنواع المتوقعة، ومناطيس، والتنسيقات قبل تنفيذها.
**规则 3：校验参数。**模型可能传入 `"; DROP TABLE users; --"`作为城市名──执行前对照期望的类型、范围和形式校验每个参数──

**Rule 4: Sanitize tool results.**إذا عادت أداة بيانات حساسة (مفاتيح API، PII، أخطاء داخلية) ، قم بتصفيتها قبل إرسالها إلى النموذج. سيتم تضمين النموذج نتائج الأداة في استجابتها حرفيا.
**规则 4：净化工具结果。**إذا عاد الوسيلة إلى البيانات الحساسة ((API 密钥、PII、内部错误) ، إرسال الوسيلة إلى النموذج قبل قبل过──

**Rule 5: Rate limit tool calls.**يمكن لنموذج في حلقة استدعاء الأدوات مئات المرات. حدد أقصى (10-20 مكالمة لكل محادثة هو معقول). كسر حلقات لا نهاية لها.
**规则 5：限流工具调用。**النموذج في الدورة قد يستخدم أدوات عدة مئات مرات.

> ️ **【易错点】**الحلقة الخالية من السيطرة في حالة حرب حقيقية:`get_weather("Tokyo")`→东京返回 "مطر"→模型"觉得不对"→再调一次→还是雨→继续调... 5 分钟烧了200次调用──修复:(1) 全局 `max_tool_calls=20`计计器,超过即终止;(2) نفس العناصر نفس الأدوات التسلسلية,,3 次后强制跳出;(3) باستخدام مرحلة 15·13 الحاكم التكلفة 监控代币 消耗,超值杀开;;

### التعامل مع الأخطاء

أدوات فشلت، أجهزة التطبيقات الإلكترونية انتهت، قواعد البيانات قد انتهت، الملفات لا توجد، يجب على النموذج أن يعرف متى تفشل أداة ولماذا.

> 工具会失败──API 会超时──数据库会机──文件不存在──模型需要知道工具何时失败以及为什么失败──

إرجاع الأخطاء كنتائج أداة مهيكلة، وليس استثناءات:

> إعادة الخطأ كوسيلة هيكلية، لا تترك غير عادية:

```json
{
  "error": true,
  "message": "City 'Toky' not found. Did you mean 'Tokyo'?",
  "code": "CITY_NOT_FOUND"
}
```

النموذج يقرأ هذا، ويعدل حججاته، ويعيد المحاولات. النموذج جيد في تصحيح الذات من رسائل الخطأ المهيكلة. إنهم سيئون في التعافي من الردود الفارغة أو الأخطاء العامة "شيئا ما ذهب خطأ".

> 模型读这个,调整参数重试――模型擅长自我纠正在结构错误信息中――但不擅长从空响应或泛化"出错了"错误中恢复――

> 🤔 **【困惑】**س: لماذا لا تنزل بشكل مباشر عن الغير عادية لتجربة الطبقة العليا؟ ج: لأن النزل الغير عادية يجعل العميل يتدفق، النموذج لا يرى أبدا إلى الخطأ`"error": true`ويقرر الخطوة التالية: تغيير المعايير إعادة التجربة، تغيير الأدوات، أو فعلاً إخبار المستخدم "أنا لا أفعل ذلك"

### المخططات: نموذج بروتوكول السياق

MCP هو المعيار المفتوح لشركة Anthropic للتفاعل مع الأدوات. بدلاً من كل تطبيق يحدد أدواته الخاصة ، يوفر MCP بروتوكولًا عالميًا: يتم تقديم الأدوات من قبل خادمات MCP ، وتستهلكها عملاء MCP (مثل Claude Code ، Cursor ، أو تطبيقك).

> MCP هو معيار مفتوح من الإنسانية، للاستخدام في أدوات التشغيل. MCP 提供通用协议: أدوات من قبل MCP 服务器提供, من قبل MCP 客户端(如Claude Code、Cursor أو应用你的) الاستهلاك، وليس كل تطبيق حدد أدواتها الخاصة.

يمكن لمخادم MCP واحد تعريض الأدوات إلى أي عميل متوافق. يمنح خادم MCP Postgres أي مستخدم قاعدة بيانات العملاء متوافق مع MCP. يمنح خادم MCP GitHub أي مستخدم متواصل الوصول إلى مخزن العملاء. يتم تعريف الأدوات مرة واحدة ، تستخدم في كل مكان.

> واحد MCP  الخادم يمكن أن تتجه إلى أي متوافق مع المستخدمين أداة الإخبار  Postgres MCP  الخادم إعطاء أي MCP  متوافق مع الوكيل  حرية الوصول إلى قاعدة البيانات  GitHub MCP  الخادم إعطاء أي وكيل  حرية الوصول إلى المخزن  الوسيلة تحديد مرة واحدة، إلى كل مكان الاستخدام 

MCP هو العمل الذي يدعو ما هو HTTP للشبكات. إنه يوحد طبقة النقل حتى تصبح الأدوات محمولة.

> MCP 之于函数调用،就像HTTP 之于网络── إنها تقييمت الطبقة الإرسالية، مما يجعل الأدوات قابلة للنقل──

>  **【前置】**ماذا时从内联函数调用升级到MCP?三个信号:(1) 工具超过 10 个,快装不下;(2) 同一工具要在多个代理框架中共享;(Claude Code、Cursor、Cline) 工具有独立维护团队,需要版本管理;;学到了阶段11·14(MCP) 和阶段13·06-18 之后,你就能把工具做独立服务器,Agent 通过协议消费;;

## بناء ذلك تحرك لتحقيق
```figure
mx-tool-call-loop
```

## بناءها

### الخطوة الأولى: حدد قائمة الأدوات

قم ببناء سجل يحتوي على تعريفات الأدوات وتنفيذها. لكل أداة تعريف JSON Schema (ما يراه النموذج) و وظيفة Python (ما يقوم به رمزك).

> 构建注册表存储工具定义和实现──每个工具有一个JSON Schema定义(模型看的) 和一个Python 函数(你的代码执行的)──

```python
import json
import math
import time
import hashlib


TOOL_REGISTRY = {}


def register_tool(name, description, parameters, function):
    TOOL_REGISTRY[name] = {
        "definition": {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters,
            },
        },
        "function": function,
    }
```

### الخطوة الثانية: تنفيذ 5 أدوات

قم ببناء آلة حسابية، بحث عن الطقس، محاكاة البحث على الإنترنت، قراءة الملفات، ومدرب رمز.

> 构建计算器、天气查询、网络搜索模拟器、文件读取器和代码运行器──

```python
def calculator(expression, precision=2):
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return {"error": True, "message": f"Invalid characters in expression: {expression}"}
    try:
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        return {"result": round(float(result), precision), "expression": expression}
    except Exception as e:
        return {"error": True, "message": str(e)}


WEATHER_DB = {
    "tokyo": {"temp_c": 18, "condition": "cloudy", "humidity": 72, "wind_kph": 14},
    "new york": {"temp_c": 22, "condition": "sunny", "humidity": 45, "wind_kph": 8},
    "london": {"temp_c": 12, "condition": "rainy", "humidity": 88, "wind_kph": 22},
    "san francisco": {"temp_c": 16, "condition": "foggy", "humidity": 80, "wind_kph": 18},
    "sydney": {"temp_c": 25, "condition": "sunny", "humidity": 55, "wind_kph": 10},
}


def get_weather(city, units="celsius"):
    key = city.lower().strip()
    if key not in WEATHER_DB:
        suggestions = [c for c in WEATHER_DB if c.startswith(key[:3])]
        return {
            "error": True,
            "message": f"City '{city}' not found.",
            "suggestions": suggestions,
            "code": "CITY_NOT_FOUND",
        }
    data = WEATHER_DB[key].copy()
    if units == "fahrenheit":
        data["temp_f"] = round(data["temp_c"] * 9 / 5 + 32, 1)
        del data["temp_c"]
    data["city"] = city
    return data


SEARCH_DB = {
    "python function calling": [
        {"title": "OpenAI Function Calling Guide", "url": "https://platform.openai.com/docs/guides/function-calling", "snippet": "Learn how to connect LLMs to external tools."},
        {"title": "Anthropic Tool Use", "url": "https://docs.anthropic.com/en/docs/tool-use", "snippet": "Claude can interact with external tools and APIs."},
    ],
    "MCP protocol": [
        {"title": "Model Context Protocol", "url": "https://modelcontextprotocol.io", "snippet": "An open standard for connecting AI models to data sources."},
    ],
    "weather API": [
        {"title": "OpenWeatherMap API", "url": "https://openweathermap.org/api", "snippet": "Free weather API with current, forecast, and historical data."},
    ],
}


def web_search(query, max_results=3):
    key = query.lower().strip()
    for db_key, results in SEARCH_DB.items():
        if db_key in key or key in db_key:
            return {"query": query, "results": results[:max_results], "total": len(results)}
    return {"query": query, "results": [], "total": 0}


FILE_SYSTEM = {
    "data/config.json": '{"model": "gpt-4o", "temperature": 0.7, "max_tokens": 4096}',
    "data/users.csv": "name,email,role\nAlice,alice@example.com,admin\nBob,bob@example.com,user",
    "README.md": "# My Project\nA tool-use agent built from scratch.",
}


def read_file(path):
    if ".." in path or path.startswith("/"):
        return {"error": True, "message": "Path traversal not allowed.", "code": "FORBIDDEN"}
    if path not in FILE_SYSTEM:
        available = list(FILE_SYSTEM.keys())
        return {"error": True, "message": f"File '{path}' not found.", "available_files": available, "code": "NOT_FOUND"}
    content = FILE_SYSTEM[path]
    return {"path": path, "content": content, "size_bytes": len(content), "lines": content.count("\n") + 1}


def run_code(code, language="python"):
    if language != "python":
        return {"error": True, "message": f"Language '{language}' not supported. Only 'python' is available."}
    forbidden = ["import os", "import sys", "import subprocess", "exec(", "eval(", "__import__", "open("]
    for pattern in forbidden:
        if pattern in code:
            return {"error": True, "message": f"Forbidden operation: {pattern}", "code": "SECURITY_VIOLATION"}
    try:
        local_vars = {}
        exec(code, {"__builtins__": {"print": print, "range": range, "len": len, "str": str, "int": int, "float": float, "list": list, "dict": dict, "sum": sum, "min": min, "max": max, "abs": abs, "round": round, "sorted": sorted, "enumerate": enumerate, "zip": zip, "map": map, "filter": filter, "math": math}}, local_vars)
        result = local_vars.get("result", None)
        return {"success": True, "result": result, "variables": {k: str(v) for k, v in local_vars.items() if not k.startswith("_")}}
    except Exception as e:
        return {"error": True, "message": f"{type(e).__name__}: {e}"}
```

### الخطوة الثالثة: تسجيل جميع الأدوات

> "سجل كل الأدوات"

```python
def register_all_tools():
    register_tool(
        "calculator", "Evaluate a mathematical expression. Supports +, -, *, /, parentheses, and decimals. Returns the numeric result.",
        {"type": "object", "properties": {"expression": {"type": "string", "description": "Math expression, e.g. '(10 + 5) * 3'"}, "precision": {"type": "integer", "description": "Decimal places in result", "default": 2}}, "required": ["expression"]},
        calculator,
    )
    register_tool(
        "get_weather", "Get current weather for a city. Returns temperature, condition, humidity, and wind speed.",
        {"type": "object", "properties": {"city": {"type": "string", "description": "City name, e.g. 'Tokyo' or 'San Francisco'"}, "units": {"type": "string", "enum": ["celsius", "fahrenheit"], "description": "Temperature units, defaults to celsius"}}, "required": ["city"]},
        get_weather,
    )
    register_tool(
        "web_search", "Search the web for information. Returns a list of results with title, URL, and snippet.",
        {"type": "object", "properties": {"query": {"type": "string", "description": "Search query"}, "max_results": {"type": "integer", "description": "Maximum results to return", "default": 3}}, "required": ["query"]},
        web_search,
    )
    register_tool(
        "read_file", "Read the contents of a file. Returns the file content, size, and line count.",
        {"type": "object", "properties": {"path": {"type": "string", "description": "Relative file path, e.g. 'data/config.json'"}}, "required": ["path"]},
        read_file,
    )
    register_tool(
        "run_code", "Execute Python code in a sandboxed environment. Set a 'result' variable to return output.",
        {"type": "object", "properties": {"code": {"type": "string", "description": "Python code to execute"}, "language": {"type": "string", "enum": ["python"], "description": "Programming language"}}, "required": ["code"]},
        run_code,
    )
```

### الخطوة الرابعة: قم ببناء وظيفة "الدورة"

هذا هو المحرك الأساسي، إنه يحاكي النموذج يقرر أداة الاتصال بها، ويقوم بتنفيذ الأداة، ويرسل النتائج.

> هذا هو المحرك الأساسي. إنه يتحدد ما يستخدم الأدوات.

```python
def simulate_model_decision(user_message, tools, conversation_history):
    msg = user_message.lower()

    if any(word in msg for word in ["weather", "temperature", "forecast"]):
        cities = []
        for city in WEATHER_DB:
            if city in msg:
                cities.append(city)
        if not cities:
            for word in msg.split():
                if word.capitalize() in [c.title() for c in WEATHER_DB]:
                    cities.append(word)
        if not cities:
            cities = ["tokyo"]
        calls = []
        for city in cities:
            calls.append({"name": "get_weather", "arguments": {"city": city.title()}})
        return calls

    if any(word in msg for word in ["calculate", "compute", "math", "what is", "how much"]):
        for token in msg.split():
            if any(c in token for c in "+-*/"):
                return [{"name": "calculator", "arguments": {"expression": token}}]
        if "+" in msg or "-" in msg or "*" in msg or "/" in msg:
            expr = "".join(c for c in msg if c in "0123456789+-*/.() ")
            if expr.strip():
                return [{"name": "calculator", "arguments": {"expression": expr.strip()}}]
        return [{"name": "calculator", "arguments": {"expression": "0"}}]

    if any(word in msg for word in ["search", "find", "look up", "google"]):
        query = msg.replace("search for", "").replace("look up", "").replace("find", "").strip()
        return [{"name": "web_search", "arguments": {"query": query}}]

    if any(word in msg for word in ["read", "file", "open", "cat", "show"]):
        for path in FILE_SYSTEM:
            if path.split("/")[-1].split(".")[0] in msg:
                return [{"name": "read_file", "arguments": {"path": path}}]
        return [{"name": "read_file", "arguments": {"path": "README.md"}}]

    if any(word in msg for word in ["run", "execute", "code", "python"]):
        return [{"name": "run_code", "arguments": {"code": "result = 'Hello from the sandbox!'", "language": "python"}}]

    return []


def execute_tool_call(tool_call):
    name = tool_call["name"]
    args = tool_call["arguments"]

    if name not in TOOL_REGISTRY:
        return {"error": True, "message": f"Unknown tool: {name}", "code": "UNKNOWN_TOOL"}

    tool = TOOL_REGISTRY[name]
    func = tool["function"]
    start = time.time()

    try:
        result = func(**args)
    except TypeError as e:
        result = {"error": True, "message": f"Invalid arguments: {e}"}

    elapsed_ms = round((time.time() - start) * 1000, 2)
    return {"tool": name, "result": result, "execution_time_ms": elapsed_ms}


def run_function_calling_loop(user_message, max_iterations=5):
    conversation = [{"role": "user", "content": user_message}]
    tool_definitions = [t["definition"] for t in TOOL_REGISTRY.values()]
    all_tool_results = []

    for iteration in range(max_iterations):
        tool_calls = simulate_model_decision(user_message, tool_definitions, conversation)

        if not tool_calls:
            break

        results = []
        for call in tool_calls:
            result = execute_tool_call(call)
            results.append(result)

        conversation.append({"role": "assistant", "content": None, "tool_calls": tool_calls})

        for result in results:
            conversation.append({"role": "tool", "content": json.dumps(result["result"]), "tool_name": result["tool"]})

        all_tool_results.extend(results)
        break

    return {"conversation": conversation, "tool_results": all_tool_results, "iterations": iteration + 1 if tool_calls else 0}
```

### الخطوة 5: تأكيد الحجة

قم ببناء مؤكدة تفحص حجج الدعوة الأداة مقابل مخطط JSON قبل التنفيذ.

> 构建校验器,在执行前对照 JSON Schema 检查工具调用参数。

```python
def validate_tool_arguments(tool_name, arguments):
    if tool_name not in TOOL_REGISTRY:
        return [f"Unknown tool: {tool_name}"]

    schema = TOOL_REGISTRY[tool_name]["definition"]["function"]["parameters"]
    errors = []

    if not isinstance(arguments, dict):
        return [f"Arguments must be an object, got {type(arguments).__name__}"]

    for required_field in schema.get("required", []):
        if required_field not in arguments:
            errors.append(f"Missing required argument: {required_field}")

    properties = schema.get("properties", {})
    for arg_name, arg_value in arguments.items():
        if arg_name not in properties:
            errors.append(f"Unknown argument: {arg_name}")
            continue

        prop_schema = properties[arg_name]
        expected_type = prop_schema.get("type")

        type_checks = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "array": list, "object": dict}
        if expected_type in type_checks:
            if not isinstance(arg_value, type_checks[expected_type]):
                errors.append(f"Argument '{arg_name}': expected {expected_type}, got {type(arg_value).__name__}")

        if "enum" in prop_schema and arg_value not in prop_schema["enum"]:
            errors.append(f"Argument '{arg_name}': '{arg_value}' not in {prop_schema['enum']}")

    return errors
```

### الخطوة 6: تشغيل الظهور

> 运行演示

```python
def run_demo():
    register_all_tools()

    print("=" * 60)
    print("  Function Calling & Tool Use Demo")
    print("=" * 60)

    print("\n--- Registered Tools ---")
    for name, tool in TOOL_REGISTRY.items():
        desc = tool["definition"]["function"]["description"][:60]
        params = list(tool["definition"]["function"]["parameters"].get("properties", {}).keys())
        print(f"  {name}: {desc}...")
        print(f"    params: {params}")

    print(f"\n--- Argument Validation ---")
    validation_tests = [
        ("get_weather", {"city": "Tokyo"}, "Valid call"),
        ("get_weather", {}, "Missing required arg"),
        ("get_weather", {"city": "Tokyo", "units": "kelvin"}, "Invalid enum value"),
        ("calculator", {"expression": 123}, "Wrong type (int for string)"),
        ("unknown_tool", {"x": 1}, "Unknown tool"),
    ]
    for tool_name, args, label in validation_tests:
        errors = validate_tool_arguments(tool_name, args)
        status = "VALID" if not errors else f"ERRORS: {errors}"
        print(f"  {label}: {status}")

    print(f"\n--- Tool Execution ---")
    direct_tests = [
        {"name": "calculator", "arguments": {"expression": "(10 + 5) * 3 / 2"}},
        {"name": "get_weather", "arguments": {"city": "Tokyo"}},
        {"name": "get_weather", "arguments": {"city": "Mars"}},
        {"name": "web_search", "arguments": {"query": "python function calling"}},
        {"name": "read_file", "arguments": {"path": "data/config.json"}},
        {"name": "read_file", "arguments": {"path": "../etc/passwd"}},
        {"name": "run_code", "arguments": {"code": "result = sum(range(1, 101))"}},
        {"name": "run_code", "arguments": {"code": "import os; os.system('rm -rf /')"}},
    ]
    for call in direct_tests:
        result = execute_tool_call(call)
        print(f"\n  {call['name']}({json.dumps(call['arguments'])})")
        print(f"    -> {json.dumps(result['result'], indent=None)[:100]}")
        print(f"    time: {result['execution_time_ms']}ms")

    print(f"\n--- Full Function Calling Loop ---")
    test_queries = [
        "What's the weather in Tokyo?",
        "Calculate (100 + 250) * 0.15",
        "Search for MCP protocol",
        "Read the config file",
        "Run some Python code",
        "Tell me a joke",
    ]
    for query in test_queries:
        print(f"\n  User: {query}")
        result = run_function_calling_loop(query)
        if result["tool_results"]:
            for tr in result["tool_results"]:
                print(f"    Tool: {tr['tool']} ({tr['execution_time_ms']}ms)")
                print(f"    Result: {json.dumps(tr['result'], indent=None)[:90]}")
        else:
            print(f"    [No tool called -- direct response]")
        print(f"    Iterations: {result['iterations']}")

    print(f"\n--- Parallel Tool Calls ---")
    multi_city_query = "What's the weather in tokyo and london?"
    print(f"  User: {multi_city_query}")
    result = run_function_calling_loop(multi_city_query)
    print(f"  Tool calls made: {len(result['tool_results'])}")
    for tr in result["tool_results"]:
        city = tr["result"].get("city", "unknown")
        temp = tr["result"].get("temp_c", "N/A")
        print(f"    {city}: {temp}C, {tr['result'].get('condition', 'N/A')}")

    print(f"\n--- Security Checks ---")
    security_tests = [
        ("read_file", {"path": "../../etc/passwd"}),
        ("run_code", {"code": "import subprocess; subprocess.run(['ls'])"}),
        ("calculator", {"expression": "__import__('os').system('ls')"}),
    ]
    for tool_name, args in security_tests:
        result = execute_tool_call({"name": tool_name, "arguments": args})
        blocked = result["result"].get("error", False)
        print(f"  {tool_name}({list(args.values())[0][:40]}): {'BLOCKED' if blocked else 'ALLOWED'}")
```

## استخدمها في إطار التنفيذ

### الاتصال بالعمل OpenAI

> OpenAI 函数调用。

```python
# from openai import OpenAI
#
# client = OpenAI()
#
# tools = [{
#     "type": "function",
#     "function": {
#         "name": "get_weather",
#         "description": "Get current weather for a city",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "city": {"type": "string"},
#                 "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
#             },
#             "required": ["city"]
#         }
#     }
# }]
#
# response = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[{"role": "user", "content": "Weather in Tokyo?"}],
#     tools=tools,
#     tool_choice="auto",
# )
#
# tool_call = response.choices[0].message.tool_calls[0]
# args = json.loads(tool_call.function.arguments)
# result = get_weather(**args)
#
# final = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {"role": "user", "content": "Weather in Tokyo?"},
#         response.choices[0].message,
#         {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)},
#     ],
# )
# print(final.choices[0].message.content)
```

يعيد OpenAI مكالمات الأداة على شكل `response.choices[0].message.tool_calls`كل مكالمة لها`id`يجب أن تضيف عند إرجاع النتيجة. النموذج يستخدم هذا الهوية لتطابق النتائج مع المكالمات. GPT-4o يمكن أن تعيد العديد من المكالمات الأداة في استجابة واحدة - تكرار وتنفيذ جميعها.

> OpenAI ضع الأدوات في استخدامها`response.choices[0].message.tool_calls`返回── كل调用有 `id`يجب أن يكون النتائج المرجعية تحتوي على النموذج باستخدام هذا الهوية وضع النتائج مطابقة إلى الاستجابة.

### استخدام الأدوات الإنسانية

> الأنثروبية 工具使用──

```python
# import anthropic
#
# client = anthropic.Anthropic()
#
# response = client.messages.create(
#     model="claude-sonnet-5",
#     max_tokens=1024,
#     tools=[{
#         "name": "get_weather",
#         "description": "Get current weather for a city",
#         "input_schema": {
#             "type": "object",
#             "properties": {
#                 "city": {"type": "string"},
#                 "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
#             },
#             "required": ["city"]
#         }
#     }],
#     messages=[{"role": "user", "content": "Weather in Tokyo?"}],
# )
#
# tool_block = next(b for b in response.content if b.type == "tool_use")
# result = get_weather(**tool_block.input)
#
# final = client.messages.create(
#     model="claude-sonnet-5",
#     max_tokens=1024,
#     tools=[...],
#     messages=[
#         {"role": "user", "content": "Weather in Tokyo?"},
#         {"role": "assistant", "content": response.content},
#         {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_block.id, "content": json.dumps(result)}]},
#     ],
# )
```

يعود أداة الأنثروبيك دعوات كحجرات المحتوى مع `type: "tool_use"`. نتيجة الأداة تذهب في رسالة للمستخدم مع `type: "tool_result"`لاحظ الفرق الرئيسي: استخدامات الأنثروبية`input_schema`لتحديدات ملامح الأداة، بينما يستخدم OpenAI `parameters`. . .

> أنثروبي 把工具调用作为 `type: "tool_use"`المواد المحتويات المعدنية`type: "tool_result"`‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬`input_schema`定义工具参数,OpenAI 用 `parameters`.

### تكامل MCP

> المملكة المركزية

```python
# MCP servers expose tools over a standardized protocol.
# Any MCP-compatible client can discover and call these tools.
#
# Example: connecting to a Postgres MCP server
#
# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client
#
# server_params = StdioServerParameters(
#     command="npx",
#     args=["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"],
# )
#
# async with stdio_client(server_params) as (read, write):
#     async with ClientSession(read, write) as session:
#         await session.initialize()
#         tools = await session.list_tools()
#         result = await session.call_tool("query", {"sql": "SELECT count(*) FROM users"})
```

MCP يقطع تنفيذ الأدوات من استهلاك الأدوات. خادم Postgres يعرف SQL. خادم GitHub يعرف API. وكيلك فقط اكتشف ودعوة الأدوات - لا تحتاج إلى رمز محدد للمقدم لكل تكامل.

> MCP 解了工具实现和工具消费──Postgres 服务器懂 SQL──GitHub 服务器懂 API──وكيلك فقط يحتاج إلى العثور على وتدوين الأدوات不需要每个集成写提供商特定代码──

## أرسلها .

هذا الدرس يُنتج`outputs/prompt-tool-designer.md`-- نموذج استشارة قابلة للاستعمال مرة أخرى لتصميم تعريفات الأدوات. أعطيه وصفًا لما تريد أداة القيام به ، ويُنتج تعريف مخطط JSON كامل مع التصفيات والأنواع والقيود.

> 本课产出 `outputs/prompt-tool-designer.md` تصميم أداة تحديدات قابل للنقل نموذجها.

كما أنها تنتج`outputs/skill-function-calling-patterns.md`-- إطار قرار لتنفيذ الوظيفة التي تدعو إلى الإنتاج، تغطي تصميم الأدوات ومعالجة الأخطاء والأمن وأنماط محددة للمورد.

> أيضاً`outputs/skill-function-calling-patterns.md` بيئة إنتاجية تطبيقات عمل الإطار القرارية، تغطي تصميم الأدوات والتعامل الخاطئ والسلامة والموارد المحددة للمقدم.

## تمارين التدريب

1. **Add a 6th tool: database query.**تنفيذ أداة SQL محاكاة مع جدول في الذاكرة. تقبل الأداة اسم الجدول وشروط المرشح (ليس SQL الخام). تأكد من أن اسم الجدول موجود في قائمة الإذن وأن مشغلي المرشحات مقيدون على `=`،`>`،`<`،`>=`،`<=`. أعيد الصفوف المتطابقة كـ JSON
   **添加第 6 个工具：数据库查询。**استخدام النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النم النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النموذج النم النموذج النموذج النموذج النم النم النموذج النم النموذج النموذج النموذج النموذج النموذج النم النموذج النموذج النم النموذج النم النموذج النموذج النم النموذج النم النموذج النم النم النموذج النم النموذج النم النم النموذ`=`.`>`.`<`.`>=`.`<=` ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬

2. **Implement retry with error feedback.**عندما تفشل مكالمة أداة (على سبيل المثال ، لم يتم العثور على المدينة) ، قم بإعادة رسالة الخطأ إلى وظيفة القرار النموذجي ودعها تصحيح حججها. تتبع عدد التجربات التي تستغرقها كل مكالمة. حدد ما يزيد عن 3 تجارب لكل مكالمة أداة.
   **实现带错误反馈的重试。**عندما يُعدّل الوسائل إلى المُختلفة (مثلاً: فالتقاط النقاط) ، قم بتعديل المعلومات الخطأة إلى وظيفة القرارات النموذجية لتعديلها.

3. **Build a multi-step agent.**بعض الأسئلة تتطلب طلبات أدوات السلاسل: "اقرأ ملف التكوين وأخبرني عن النموذج الذي يتم تشكيله ، ثم ابحث في الويب عن تسعير هذا النموذج". تنفيذ حلقة تعمل حتى يقرر النموذج أنه لا حاجة إلى المزيد من الأدوات ، وإرسال النتائج المتراكمة في كل خطوة قرار. الحد من 10 تكرارات لمنع حلقات لا نهاية لها.
   **构建多步 agent。**بعض الاستفسارات تحتاج إلى أدوات تشبيكية: "قرأ ملف تعريف أخبرني ما هو النموذج الذي تم تعيينه، ثم ابحث على الإنترنت عن تثبيت هذا النموذج.

4. **Measure tool selection accuracy.**قم بإنشاء 30 استفسار اختباري مع أسماء الأدوات المتوقعة. قم بتشغيل وظيفة القرار الخاصة بك على جميع 30 وقياس ما هي النسبة المئوية من الوقت الذي يختار فيه الأدوات الصحيحة. حدد أي استفسارات تسبب الأكثر ارتباكا بين الأدوات.
   **测量工具选择准确率。**创建30个带预期工具名的测试查询――对所有30个运行决策函数,测量选对工具的百分比――识别哪些查询最容易混工具――

5. **Implement tool call caching.**إذا تم استدعاء نفس الأداة مع حجج متطابقة في غضون 60 ثانية، ارجع النتيجة المحفوظة في الاحتفاظ بدلاً من إعادة تنفيذها. استخدم قاموسًا مع مفتاح `(tool_name, frozenset(args.items()))`. قياس معدلات الوصول إلى الكاش عبر المحادثة مع 20 استفسار
   **实现工具调用缓存。**60 ثانية في حالة استخدام نفس الأداة مع نفس العيارات، عودة إلى النتيجة كاشوف بدلا من إعادة تنفيذها.`(tool_name, frozenset(args.items()))`│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │                               

## شروط الرئيسية

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Function calling | "Tool use" | The model outputs structured JSON describing a function to invoke with specific arguments -- your code executes it, not the model | 函数调用：模型输出结构化 JSON 描述要调用的函数及参数——你的代码执行，而非模型 |
| Tool definition | "Function schema" | A JSON Schema object describing a tool's name, purpose, parameters, and types -- the model reads this to decide when and how to use the tool | 工具定义：JSON Schema 描述工具名、用途、参数和类型——模型读它决定何时如何使用 |
| Tool choice | "Calling mode" | Controls whether the model must call a tool (required), may call a tool (auto), or must call a specific tool (named) | 工具选择：控制模型必须调用（required）、可以调用（auto）或必须调用特定工具（named） |
| Parallel calling | "Multi-tool" | The model outputs multiple tool calls in a single turn, reducing round trips -- GPT-4o and Claude both support this | 并行调用：模型单轮内输出多个工具调用，减少往返——GPT-4o 和 Claude 都支持 |
| Tool result | "Function output" | The return value from executing a tool, sent back to the model as a message so it can use real data in its response | 工具结果：执行工具的返回值，作为消息送回模型，让其在回复中使用真实数据 |
| Argument validation | "Input checking" | Verifying that model-generated arguments match the expected types, ranges, and constraints before executing the tool | 参数校验：执行前验证模型生成的参数是否匹配期望的类型、范围和约束 |
| MCP | "Tool protocol" | Model Context Protocol -- Anthropic's open standard for exposing tools via servers that any compatible client can discover and call | MCP：模型上下文协议——Anthropic 开放标准，通过服务器暴露工具，任何兼容客户端可发现和调用 |
| Agent loop | "ReAct loop" | The iterative cycle of model-decides-tool, code-executes-tool, result-feeds-back until the model has enough information to respond | Agent 循环：模型决定-代码执行-结果反馈的迭代循环，直到模型有足够信息回复 |
| Tool poisoning | "Prompt injection via tools" | An attack where tool results contain instructions that manipulate the model's behavior -- sanitize all tool outputs | 工具投毒：工具结果含操纵模型行为的指令的攻击——净化所有工具输出 |
| Rate limiting | "Call budget" | Setting a maximum number of tool calls per conversation to prevent infinite loops and runaway API costs | 限流：设每次对话工具调用上限，防无限循环和失控 API 成本 |

## المزيد من القراءة

- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)-- الإشارة النهائية لاستخدام الأدوات مع GPT-4o، بما في ذلك المكالمات المتوازية، المكالمات القسرية، والحجج المهيكلة
  OpenAI  وظيفة调用指南GPT-4o 工具使用权威参考,含并行调用、强制调用和结构化参数
- [Anthropic Tool Use Guide](https://docs.anthropic.com/en/docs/tool-use)-- أداة كلود استخدام تنفيذ مع input_schema، استجابات متعددة الأدوات، وتكوين tool_choice
  الأنثروبات 工具使用指南Claude 工具使用实现,含 input_schema、多工具响应和 tool_choice 配置
- [Model Context Protocol Specification](https://modelcontextprotocol.io)-- المعيار المفتوح للتشامل بين الأدوات عبر تطبيقات الذكاء الاصطناعي، مع بنية الخادم / العميل
  模型上下文协议规范AI 应用间工具互操作的开放标准,采用服务器/客户端架构
- [Schick et al., 2023 -- "Toolformer: Language Models Can Teach Themselves to Use Tools"](https://arxiv.org/abs/2302.04761)-- ورقة أساسية حول تدريب الدرجات العليا لتحديد متى وكيفية استدعاء الأدوات الخارجية
  شيك 等 2023 "أداة" تدريب LLM قرر كيفية استخدام الأدوات الخارجية
- [Patil et al., 2023 -- "Gorilla: Large Language Model Connected with Massive APIs"](https://arxiv.org/abs/2305.15334)-- تحسين الـ LLM لتحقيق مكالمات API على طول 1645 API مع تقليل الهلوسة
  باتيل 等 2023 "غوريلا"微调 LLM في 1645 个 API 上准调并减少幻觉
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html)-- مقياس قياسي في الوقت الحقيقي مقارنة الوظيفة التي تدعو دقة عبر GPT-4o، كلود، جيمين، والنماذج المفتوحة
  伯克利 وظيفة调用排行榜比较 GPT-4o、Claude、Gemini 和开源模型函数调用准确率的实时基准
- [Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023)](https://arxiv.org/abs/2210.03629)-- حلقة التفكير-العمل-الملاحظة التي هي حلقة الوكيل الخارجي حول كل مكالمة الأداة؛ حيث ينتهي هذا الدروس، المرحلة 14 تبدأ.
  ياو 等 "ReAct" ((ICLR 2023)  التفكير- العمل- مشاهدة دورة، هي كل أداة تطبيق عامل الطبقة الخارجية دورة.
- [Anthropic — Building effective agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents)-- خمسة أنماط قابلة للتكوين (السلسلة السريعة، التوجيه، التوازي، الموسيقي العامل، المقيّم المُحسن) بنيت من أداة استخدام واحدة البدائية.
  إنسانية构建有效代理(2024年 12月)  بناء على أداة واحدة استخدام الجهات الأصلية الخمسة نموذج
