# التخزين السريع وتخزين السياق 提示缓存与上下文缓存

> إن طلب نظامك يبلغ 4000 رمز. سياق RAG الخاص بك يبلغ 20,000 رمز. أنت ترسل كلتا مع كل طلب. أنت تدفع أيضاً لكلتا  كل مرة. يسمح الاحتفاظ بالخزينة السريعة للمقدم بإبقاء هذا المقبل دافئًا على جانبه ويفرض عليك 10% من معدل العادة الاستخدام. إذا استخدمت بشكل صحيح، فإنه يقلل من تكلفة الاستنتاج بنسبة 5090% وتخفيف التخفيف من الترميز الأول بنسبة 4085%.

> **【中文解读】**系统提示4000 توكن + RAG 上下文20000 توكن، كل طلب يجب أن يدفع.提示缓存让供应商保留前,重用时只收取10%费用.

> **【拓展：提示缓存→RAG生产优化】**التخزين السريع من الأنثروبيك و الاستجابة المحفظة من OpenAI هي التقنية الرئيسية لخفض تكلفة نظام إنتاج RAG ، وخاصة مع وجود نظام ثابت وفرص كبيرة من البحث على المشهد التالي:

>  **【前置】**学本节前请先掌握:Phase 11·01(التسريع الهندسة)、Phase 11·05(هندسة السياق)、Phase 11·11(تكلفة التخزين)。本节是其延伸,讲供应商层(Anthropic cache_control、OpenAI自动缓存、Gemini CachedContent)。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 01 (Prompt Engineering), Phase 11 · 05 (Context Engineering), Phase 11 · 11 (Caching and Cost) | **前置知识:** Phase 11 · 01 (提示工程)、05 (上下文工程)、11 (缓存与成本)
**Time:** ~60 minutes | **时间:** ~60 分钟

## المشكلة المشكلة المشكلة

وكيل التشفير يرسل نفس النظام 15000 رمز على كل جولة من المحادثة$3/M input tokens is $0.90 في تكلفة المدخل وحدها  قبل أي من الرسائل الفعلية للمستخدم. مضاعفة بـ 10,000 محادثة يومية والفاتورة تصل إلى 9,000 دولار / يوم للنص الذي لا يتغير أبدا.

> وكيل برمجة في كل دورة من المحادثات في إرسال نفس 15،000 رمز النظام نصيحة إلى كلود.$3/M 输入 token，仅输入成本就是 $0.90 لا يحتوي على رسائل المستخدمين الفعلية.

لا يمكنك تقليص الإشارة دون إيذاء الجودة. لا يمكنك تجنب إرسالها  يحتاجها النموذج في كل مرة. الخطوة الوحيدة هي التوقف عن دفع السعر الكامل لمثبتة رأتها مقدمها بالفعل.

> لا يمكنك أن تقلص النقطة دون أن تضر بالجودة. لا يمكنك أن تجنب إرسالها.

>  **【类比】**التخزين السريع 像"快递公司记住你的常用地址"第一次发货要详细说明"北京市朝阳区...",之后每次发货只需说"老地方",快递公司自动调出地址。技术上:供应商把前的KV缓存存在自己的服务器,下次请求来时直接复用,不需要重新计算注意的K/V矩阵。对用户透明你只需要在API调用加个`cache_control`标记──

> ️ **【易错点】**التخزين السريع من 3 个坑:(1) **prefix 顺序敏感**cache 命中要求 prefix 完全相同(包括空格、换行),system prompt 末尾多一个空格就错过;务必把可变部分(用户输入) 放最后。(2) **cache TTL 5 分钟**أنثروبي 默认 5 分钟过期,没流量时缓存 失效; باستخدام TTL مُطَوَّلَة(1 小时)保住冷启动场景──(3) **没监控命中率** لا أعرف معدل الحد الأدنى  لا أستطيع تحديد النتيجة`cache_creation_input_tokens`和 `cache_read_input_tokens`, سجل إلى لوح مراقبة

هذه الخطوة هي التخزين الآلي السريع. أطلقتها Anthropic في أغسطس 2024 (مع فترة 1 ساعة تمتد من تتي إل في 2025) ، وأتمتها OpenAI في وقت لاحق من ذلك العام ، وأطلقت Google التخزين السياقي الصريح جنبا إلى جنب مع Gemini 1.5, والثلاثة الآن تقدمها ك ميزة من الدرجة الأولى على نماذجها الحدودية.

> هذا هو الطريقة لتقديم الحفاظ على الاحتفاظ. أطلقتها شركة الأنثروبات في آب/أغسطس 2024، أطلقتها شركة OpenAI في عام 2025، وأطلقتها شركة Google في Gemini 1.5، على نحو واضح على التالي.


> **【中文解读】**يعتمد قيمة التخزين السريع على النظام السريع عادةً ما تكون طويلة ((5K + توكنات) ولا تتغير في جميع الطلبات. كل مرة يتم فيها إعادة حساب هذه الوتينات.


## المفهوم الأساسي

> **【中文解读】**التخزين السريع يستفيد من خصائص التفكير في الـ LLM  إذا كان العديد من الطلبات تشارك نفس التخزين السريع ، يمكن تخزين هذا التخزين السريع في الـ KV 计算结果,避免重复计算.

> **【拓展：Prompt Caching 的成本节省】**سيتم حفظ الإدخال السريع من قبل الإنساني                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                $0.50/M tokens（原价 $5)。 على النظام على الفور 5K توكن + 平均 10 مرات استعادة المشهد، 月成本可降低约 75%。


![Prompt caching: write once, read cheap](../assets/prompt-caching.svg)

**The mechanic.**عندما يطابق مقدمة طلب واحد من طلب حديث، يقوم المقدم بتقديم KV-Cache من الجولة السابقة بدلاً من إعادة تشفير الرموز. تدفع قسطًا صغيرًا من الكتابة في المرة الأولى وخصمًا كبيرًا من القراءة في كل مرة بعد ذلك.

> **机制。**عندما يتناسب المبلغ السابق للمطالبة مع المبلغ السابق للمطالبة الأخيرة، يقدم الموردون الاحتياطي KV من خلال عمليات التشغيل السابقة، بدلاً من إعادة ترميز الرمز.

**Three provider flavors in 2026.**

| Provider | API style | Hit discount | Write premium | Default TTL | Min cacheable |
|---------|-----------|--------------|---------------|-------------|---------------|
| Anthropic | Explicit `cache_control` markers on content blocks | 90% off input | 25% surcharge | 5 min (extendable to 1 hour) | 1,024 tokens (Sonnet/Opus), 2,048 (Haiku) |
| OpenAI | Automatic prefix detection | 50% off input | none | Up to 1 hour (best-effort) | 1,024 tokens |
| Google (Gemini) | Explicit `CachedContent` API | Storage-billed; read at ~25% of normal | Storage fee per token·hour | User-set (default 1 hour) | 4,096 tokens (Flash), 32,768 (Pro) |

**The invariant.**كل ثلاثة محاورات التخزين فقط. إذا كان أي رمز يختلف بين الطلبات، كل شيء بعد أول رمز مختلف هو غياب. ضع * مستقر* الأجزاء في الأعلى، * المتغير* الأجزاء في الأسفل.

> **不变量。**ثلاثة من كل الاحتياطيات فقط قبل🏼 إذا كان هناك أي رمز بين الطلبات مختلفة، أول رمز مختلف  بعد كل المحتويات هي غير مقصودة‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

### التخطيط الصديق للتخزين

```
[system prompt]          <-- cache this
[tool definitions]       <-- cache this
[few-shot examples]      <-- cache this
[retrieved documents]    <-- cache if reused, else don't
[conversation history]   <-- cache up to last turn
[current user message]   <-- never cache (different every time)
```

انتهاك النظام  وضع رسالة المستخدم فوق طلب النظام، وتوقف الاستعراضات الديناميكية بين القليل من اللقطات  والخزنة الاحتياطية لا تضرب أبدا.

> 违反顺序 将用户消息放在系统提示上,在少样本之间穿插动态检查缓存永远不会命中

### حساب الانسجام

تعني قسيمة كتابة 25% من Anthropic أن بلوك مخزن يجب قراءته مرتين على الأقل لتوفير الأموال الصافية. 1 كتابة + 1 قراءة يبلغ متوسط التكلفة 0.675x لكل طلب (يوفر 32%). 1 كتابة + 10 قراءة يبلغ متوسط 0.205x (يوفر 80%). قاعدة البصمة: حفظ أي شيء تتوقع إعادة استخدامه على الأقل 3 مرات داخل TTL.

> الإنتروباتية 25%  كتابة الفائدة يعني أن كتب الاحتفاظ يجب أن يتم قراءتها على الأقل مرتين لتقديم النقود المالية.

## بناء ذلك تحرك لتحقيق
```figure
prompt-cache-hit
```

## بناءها

### الخطوة 1: التخزين الآلي للطلبات الإنسانية مع علامات صريحة

```python
import anthropic

client = anthropic.Anthropic()

SYSTEM = [
    {
        "type": "text",
        "text": "You are a senior Python reviewer. Follow the rubric exactly.\n\n" + RUBRIC_15K_TOKENS,
        "cache_control": {"type": "ephemeral"},
    }
]

def review(code: str):
    return client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": code}],
    )
```

- نعم`cache_control`علامة تقول أنثروبيك لتخزين الكتلة لمدة 5 دقائق. إعادة استخدام داخل تلك النافذة ضربات؛ إعادة استخدام بعد انتهاء الصلاحية ويكتب مرة أخرى.

> `cache_control`标记告诉安тропоic 将该块存储 5 分钟.

**Response usage fields:**

```python
response = review(code_a)
response.usage
# InputTokensUsage(
#     input_tokens=120,
#     cache_creation_input_tokens=15023,   # paid at 1.25x
#     cache_read_input_tokens=0,
#     output_tokens=340,
# )

response_b = review(code_b)
response_b.usage
# cache_creation_input_tokens=0
# cache_read_input_tokens=15023           # paid at 0.1x
```

تحقق من كلا الحقول في CI  إذا `cache_read_input_tokens`يبقى عند الصفر عبر الطلبات، مفاتيح التخزين الخاصة بك تتحرك.

> في المعلومات المركزية تحقق هذه الصفحتين إذا`cache_read_input_tokens`في العديد من الطلبات الحفاظ على الصفر، كيس الاحتفاظ الخاص بك يزول.

### الخطوة الثانية: تمديد المدة التوقيتية لمدة ساعة واحدة

بالنسبة لموظفات اللحظات طويلة المدى، تنتهي الخمس دقائق المتخلفة بين الوظائف.`ttl`:

```python
{"type": "text", "text": RUBRIC, "cache_control": {"type": "ephemeral", "ttl": "1h"}}
```

تكلفة التسجيل المباشر لمدة ساعة واحدة ضعف قسط الكتابة (50% عن الخط الأساسي بدلاً من 25%) ، ولكن تسترد بسرعة على أي دفعة تستخدم المقبل أكثر من 5 مرات.

> 1 小时 TTL الإدخال المكلفة هو 2 أضعاف 50% من المعدل الأساسي وليس 25%) ، ولكن في أي استخدامات أخرى قبل أكثر من 5 مرات من التجهيز الجماعي بسرعة.

### الخطوة الثالثة: OpenAI التخزين الآلي

لا يقدم لك OpenAI أي شيء لتكوين. أي مقدمة فوق 1024 رمزا تتطابق مع طلب حديث يحصل على خصم 50٪ تلقائيًا.

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},   # long and stable
        {"role": "user", "content": user_msg},
    ],
)
resp.usage.prompt_tokens_details.cached_tokens  # the discounted portion
```

نفس قاعدة التخطيط الصديقة للتخزين القياسية تنطبق. هناك شيئين يقتلون التخزين القياسي OpenAI الذي لا يقتلون التخزين القياسي: تغيير `user`الحقل (المستخدم ككون مفتاح التخزين) وأدوات إعادة ترتيب.

> نفس الاحتفاظ والصحة المشتركة قواعد تطبيقها.`user`字段和重新排序工具──

### الخطوة الرابعة: تخزين السياق الصريح التجميلي

التوأم يعامل الجهاز كشيء من الدرجة الأولى يمكنك إنشاءه وتسميته:

```python
from google import genai
from google.genai import types

client = genai.Client()

cache = client.caches.create(
    model="gemini-3-pro",
    config=types.CreateCachedContentConfig(
        display_name="rubric-v3",
        system_instruction=RUBRIC,
        contents=[FEW_SHOT_EXAMPLES],
        ttl="3600s",
    ),
)

resp = client.models.generate_content(
    model="gemini-3-pro",
    contents=["Review this code:\n" + code],
    config=types.GenerateContentConfig(cached_content=cache.name),
)
```

تتقاضى Gemini التخزين لكل رمز·ساعة طالما أن الكاشة تعمل، وتقرأ عند ~ 25% من معدل إدخال العادي. هذا هو الشكل الصحيح عندما تستخدم نفس الإشارة العملاقة عبر العديد من الجلسات على مدى أيام.

> التنين 按缓存存活期间每代币·小时收取存储费,读取费率约为正常输入的25%──当你在多次会议中跨天重复使用相同的大型提示时,这是正确的选择──

### الخطوة 5: قياس معدل الضربة في الإنتاج

انظر`code/main.py`للمحاسب المحاكي الممثل من ثلاثة مزودي يقوم بتتبع حسابات الكتابة / القراءة / الإغفال وحساب التكلفة المختلطة لكل طلبات 1K. تنشر بوابة مع معدل ضرب هدف  معظم الإعدادات الإنتاجية الأنثروبية يجب أن ترى > 80% جزء القراءة بعد التدفئة.

> 见 `code/main.py`获取模拟的三供应商会计师,跟踪写入/读取/未命中计数并计算每千请求的混合成本──按目标命中率门控部署多数生产 类型 设置在预热后应见 >80% 读取比例──

## الفخاخ التي لا تزال تشغل في عام 2026

> 2026 سنة لا تزال في الصعود:

- **Dynamic timestamps at the top.** `"Current time: 2026-04-22 15:30:02"`في أعلى طلب النظام كل طلب يفشل، نقلها تحت نقطة كسر التخزين
  **顶部的动态时间戳。**系统提示顶部放 `"Current time: 2026-04-22 15:30:02"`كل طلب كان غير مقصود.
- **Tool reordering.**إعادة تشكيل الأدوات في ترتيب مستقيم
  **工具重排序。**في إثبات الترتيبات وترتيبات الأدوات 部署间的字典重排破坏每次命中──
- **Free-text near-duplicates.**"أنت مفيد". مقابل "أنت مساعد مفيد".
  **自由文本近似重复。**"أنت مفيد" vs "أنت مساعد مفيد".一字节差异 = 完全未命中。
- **Too-small blocks.**إنثروبيك يفرض سطحًا من 1,024 رمزًا (2،048 في هايكو). لا يتم تخزين الكتل الصغيرة بصمت.
  **过小的块。**الأنثروبي 强制 1,024 رمز  下限                                                                                                                                                                                                                                                        
- **Blind cost dashboards.**تقسيم "شعار المدخل" إلى مخزن مخزن مقابل غير مخزن مخزن وإلا فإن انخفاض حركة المرور يبدو وكأنه مكاسب مخزن مخزن.
  **盲目的成本仪表板。**وضع "أوراق إدخال" في الحافظة مقابل عدم الحافظة.

## استخدمها في إطار التنفيذ

كومة التخزين الاحتياطي لعام 2026:

> 2026 缓存技术:

| Situation | Pick |
|-----------|------|
| Agent with stable 10k+ system prompt, many turns | Anthropic `cache_control` with 5-min TTL |
| Batch job reusing a prefix for 30+ minutes | Anthropic with `ttl: "1h"` |
| Serverless endpoints on GPT-5, no custom infra | OpenAI automatic (just make your prefix stable and long) |
| Multi-day reuse of a giant code/doc corpus | Gemini explicit `CachedContent` |
| Cross-provider fallback | Keep the cacheable prefix layout identical across providers so any hit works |

| 场景 | 选择 |
|------|------|
| Agent 有稳定 10k+ 系统提示、多轮 | Anthropic `cache_control` 配 5 分钟 TTL |
| 批处理重用前缀 30+ 分钟 | Anthropic 配 `ttl: "1h"` |
| GPT-5 上的无服务器端点、无定制基建 | OpenAI 自动（让前缀稳定且够长） |
| 多天重用大型代码/文档语料 | Gemini 显式 `CachedContent` |
| 跨提供商回退 | 跨提供商保持可缓存前缀布局一致，任何命中都工作 |

الجمع مع التخزين الآلي (المرحلة 11 · 11) للطبقة الرسالة المستخدم: التخزين الآلي المفاجئ * إعادة استخدام الوهم المماثلة *، التخزين الآلي المماثلة * إعادة استخدام المعنى.

> مع لغة كاشووري (بالإنجليزية: 语义缓存处理)

## أرسلها .

إنقاذ`outputs/skill-prompt-caching-planner.md`:

```markdown
---
name: prompt-caching-planner
description: Design a cache-friendly prompt layout and pick the right provider caching mode.
version: 1.0.0
phase: 11
lesson: 15
tags: [llm-engineering, caching, cost]
---

Given a prompt (system + tools + few-shot + retrieval + history + user) and a usage profile (requests per hour, TTL needed, provider), output:

1. Layout. Reordered sections with a single cache breakpoint marked; explain which sections are stable, which are volatile.
2. Provider mode. Anthropic cache_control, OpenAI automatic, or Gemini CachedContent. Justify from TTL and reuse pattern.
3. Break-even. Expected reads per write within TTL; net cost vs no-cache with math.
4. Verification plan. CI assertion that cache_read_input_tokens > 0 on the second identical request; dashboard split by cached vs uncached tokens.
5. Failure modes. List the three most likely reasons the cache will miss in this setup (dynamic timestamp, tool reorder, near-duplicate text) and how you will prevent each.

Refuse to ship a cache plan that places a dynamic field above the breakpoint. Refuse to enable 1h TTL without a reuse count that makes the 2x write premium pay back.
```

## تمارين التدريب

1. **Easy.**إجراء محادثة 10 جولات مع طلب نظام 5,000 رمز ضد كلود.`cache_control`و بعدها مع. إبلغ فاتورة إدخال رموز لكل واحد.
   خذ 10 دورات من الحوار و 5000 رمز`cache_control`分別运行,报告输入代币 费用──
2. **Medium.**اكتب قناة اختبارية، التي، بالنظر إلى نموذج سريع ومسجل طلب، تحسب معدل الوصول المتوقع والوفور بالدولار لكل مزود (Anthropic 5m، Anthropic 1h، OpenAI تلقائي، Gemini صريح).
   كتابة أدوات الاختبار، ومشاريع ومجلات الطلبات، وحساب معدل الوصول المتوقع لكل مزود ومبلغ الادخار.
3. **Hard.**قم ببناء محفز التخطيط: إعطاء عرض وعبارة عن قائمة من الحقول المعلنة `stable=True/False`إعادة كتابة الإشارة لإعادة وضع نقطة وقف واحدة في التخزين في أقصى وضع صديقة للتخزين دون فقدان المعلومات. التحقق من نقطة نهاية الأنثروبيك الحقيقية.
   构建布局优化器:重写提示将缓存断点放在最大缓存友好位置――

## شروط الرئيسية

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Prompt caching | "Makes long prompts cheap" / "让长提示变便宜" | Reusing a provider-side KV-cache for matching prefixes; 50-90% discount on repeated input tokens. | 提示缓存：重用供应商端的 KV-cache，对重复输入 token 提供 50-90% 折扣 |
| `cache_control` | "The Anthropic marker" / "Anthropic 标记" | Content-block attribute that declares "everything up to here is cacheable"; `{"type": "ephemeral"}`. | cache_control：内容块属性，声明"到这里为止的内容可缓存" |
| Cache write | "Paying the premium" / "付溢价" | The first request that populates the cache; billed at ~1.25x input rate on Anthropic, free on OpenAI. | 缓存写入：第一次填充缓存的请求 |
| Cache read | "The discount" / "折扣" | Subsequent requests matching the prefix; billed at 10% (Anthropic), 50% (OpenAI), ~25% (Gemini). | 缓存读取：匹配前缀的后续请求 |
| TTL | "How long it lives" / "存活时间" | Seconds the cache stays warm; Anthropic 5m default (extendable 1h), OpenAI best-effort up to 1h, Gemini user-set. | TTL：缓存保持活跃的秒数 |
| Extended TTL | "1-hour Anthropic cache" / "1小时缓存" | `{"type": "ephemeral", "ttl": "1h"}`; 2x write premium but worth it for batch reuse. | 扩展 TTL：1 小时缓存，2 倍写入溢价 |
| Prefix match | "Why my cache missed" / "为什么缓存未命中" | Caches only hit when every token from the start up to the breakpoint is byte-identical. | 前缀匹配：缓存只在从开头到断点的每个 token 完全相同时才命中 |
| Context caching (Gemini) | "The explicit one" / "显式缓存" | Google's named, storage-billed cache object; best for multi-day reuse of large corpora. | 上下文缓存 (Gemini)：命名、按存储计费的缓存对象 |

## المزيد من القراءة

- [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) `cache_control`، 1 ساعة TTL ، كسر طاولات التوازن.
  النتائج التالية:
- [OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) تطابق المقبلات الآلية.
  OpenAI 提示缓存文档自动前匹配──
- [Google — Context caching](https://ai.google.dev/gemini-api/docs/caching) `CachedContent`معدل التكلفة و التخزين
  Google 上下文缓存文档CachedContent API 和存储定价──
- [Anthropic engineering — Prompt caching for long-context workloads](https://www.anthropic.com/news/prompt-caching) البريد الأصلي للانطلاق مع أرقام التأخير.
  التلفزيونية 工程博客长上下文工作负载的提示缓存,含延迟数据──
- المرحلة 11 · 05 (هندسة السياق)  أين تقطع المشاركة حتى يتمكن الكاش من الهبوط.
  第 11 阶段 · 05 上下文工程) 在哪里切分提示以便缓存生效
- المرحلة 11 · 11 (التخزين والتكلفة)  زوج التخزين المحفظة التخزينية مع تخزين معنوي على رسائل المستخدم.
  第 11 阶段 · 11(缓存与成本)  سوف تُذكر الاحتفاظ بالاحتفاظ بالاحتفاظ بالاتصال مع المستخدم
- [Pope et al., "Efficiently Scaling Transformer Inference" (2022)](https://arxiv.org/abs/2211.05102) نموذج الذاكرة في الاحتفاظ بالكاش KV الذي يُعرض للمستخدمين للتخزين الآلي؛ يشرح لماذا يكون إعادة قراءة مقدمة محفظة محفظة الأحتفاظ بها ~ 10x أرخص من إعادة الحساب.
  解释为什么缓存前比重算便宜约10倍的KV-cache内存模型论文──
- [Agrawal et al., "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills" (2023)](https://arxiv.org/abs/2308.16369) prefill هي اختصارات التخزين المحفظي المطلوب في مرحلة التخزين؛ هذا الورق يشرح لماذا تنخفض TTFT بشكل كبير على ضرب التخزين المحفظي بينما TPOT غير متأثر.
  解释为什么缓存命中时TTFT大幅下降而TPOT不受影响论文──
- [Leviathan et al., "Fast Inference from Transformers via Speculative Decoding" (2023)](https://arxiv.org/abs/2211.17192) التخزين الآلي يقع جنبا إلى جنب مع تشفير التكهنات، الانتباه الفلاش، و MQA / GQA كجهاز تدفع يلتوي منحنى تكلفة الاستنتاج؛ اقرأ هذا بالنسبة للثلاثة الأخرى.
  提示缓存与投机解码、Flash Attention 和 MQA/GQA 并列的推理成本曲线杆──
