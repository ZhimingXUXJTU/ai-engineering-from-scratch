# त्वरित कैशिंग और संदर्भ कैशिंग 提示缓存与上下文缓存

> आपके सिस्टम प्रॉम्प्ट में 4,000 टोकन हैं। आपका RAG संदर्भ 20,000 टोकन है। आप प्रत्येक अनुरोध के साथ दोनों भेजते हैं। आप हर बार दोनों के लिए भी भुगतान करते हैं। प्रॉम्प्ट कैशिंग प्रदाता को उस प्रीफिक्स को अपने पक्ष पर गर्म रखने और आपको पुनः उपयोग पर सामान्य दर का 10% बिल करने की अनुमति देता है। सही तरीके से उपयोग किया जाता है, यह अनुमान लागत को 5090% और पहले टोकन विलंबता को 4085% तक कम करता है।

> **【中文解读】**系统提示4000 टोकन + RAG 上下文20000 टोकन, प्रति अनुरोध भुगतान करना होगा।

> **【拓展：提示缓存→RAG生产优化】**मानवतावादी की त्वरित कैशिंग और ओपनएआई की कैश प्रतिक्रिया आरएजी उत्पादन प्रणाली की लागत कम करने की महत्वपूर्ण तकनीक है, विशेष रूप से स्थिर प्रणाली युक्तियों और भारी मात्रा में खोजों पर नीचे दिए गए परिदृश्यों में।

>  **【前置】**学本节前请先掌握:Phase 11·01(Prompt Engineering)、Phase 11·05(Context Engineering)、Phase 11·11(Caching Cost)。本节是其延伸,讲供应商层(Anthropic cache_control、OpenAI自动缓存、Gemini CachedContent)。

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 01 (Prompt Engineering), Phase 11 · 05 (Context Engineering), Phase 11 · 11 (Caching and Cost) | **前置知识:** Phase 11 · 01 (提示工程)、05 (上下文工程)、11 (缓存与成本)
**Time:** ~60 minutes | **时间:** ~60 分钟

## समस्या  समस्या परिचय

एक कोडिंग एजेंट एक ही 15,000 टोकन प्रणाली सूचित क्लाउड को एक बातचीत के हर मोड़ पर भेजता है।$3/M input tokens is $उपयोगकर्ता के किसी भी वास्तविक संदेश से पहले केवल 0.90 इनपुट लागत । 10,000 दैनिक वार्तालापों से गुणा करें और बिल $9,000 / दिन के लिए मिलता है जो कभी नहीं बदलता है।

> एक प्रोग्रामिंग एजेंट प्रत्येक वार्तालाप के दौरान एक ही 15,000 टोकन भेजता है$3/M 输入 token，仅输入成本就是 $0.90 भी शामिल नहीं है उपयोगकर्ता की वास्तविक संदेशों में।

आप गुणवत्ता को नुकसान पहुंचाए बिना प्रॉम्प्ट को छोटा नहीं कर सकते। आप इसे भेजने से बच नहीं सकते। मॉडल को हर मोड़ पर इसकी आवश्यकता होती है। एकमात्र कदम यह है कि प्रदाता पहले से ही देखे गए एक पूर्वावलोकन के लिए पूर्ण मूल्य का भुगतान करना बंद कर दें।

> आप गुणवत्ता को नुकसान पहुंचाए बिना सुझाव को छोटा नहीं कर सकते हैं। आप इसे भेजने से बचने से नहीं बच सकते। मॉडल को हर समय इसकी आवश्यकता होती है।

>  **【类比】**त्वरित कैशिंग 像"快递公司记住你的常用地址"第一次发货要详细说明"北京市朝阳区...", उसके बाद प्रत्येक发货只需说"老地方",快递公司自动调出地址──技术上: आपूर्तिकर्ता ने पूर्वावलोकन के के के कैश 存在自己的服务器,下次请求来时直接复用,不需要重新计算注意的 K/V矩阵──对用户透明你只需在API 调用加个`cache_control`标记──

> ️ **【易错点】**त्वरित कैशिंग के 3 个坑:(1) **prefix 顺序敏感**cache 命中要求 पूर्वावलोकन 完全相同(包括空格、换行), सिस्टम शीघ्र 末尾多一个空格就错过;务必把可变部分(用户输入) 放最后。(2) **cache TTL 5 分钟**Anthropic 默认 5 分钟过期,没流量时缓存 失效; विस्तारित TTL के साथ**没监控命中率**अज्ञात भाग्य दर असंभव परिणाम; मानव एपीआई प्रतिक्रिया 里有 `cache_creation_input_tokens`和 `cache_read_input_tokens`, रिकॉर्ड तक निगरानी बोर्ड

यह कदम त्वरित कैशिंग है। मानव ने इसे अगस्त 2024 में (2025 में 1 घंटे के विस्तारित-टीटीएल संस्करण के साथ) लॉन्च किया, ओपनएआई ने उसी वर्ष के अंत में इसे स्वचालित किया, गूगल ने जेमिनी 1.5 के साथ स्पष्ट संदर्भ कैशिंग लॉन्च की, और अब तीनों इसे अपने फ्रंटियर मॉडल पर प्रथम श्रेणी की सुविधा के रूप में पेश करते हैं।

> यह तरीका है सुझाव कैशिंग। मानव विज्ञान ने इसे 2024 में अगस्त में लॉन्च किया था।


> **【中文解读】**त्वरित कैशिंग का मूल्य सिस्टम के त्वरित में होता है आमतौर पर बहुत लंबा होता है 5K + टोकन) और सभी अनुरोधों में अपरिवर्तित होता है। प्रत्येक अनुरोध के बाद इन टोकन के KV-कैश का भारी नुकसान होता है।


## अवधारणा का मूल अवधारणा

> **【中文解读】**शीघ्र कैशिंग LLM 推理的特性 का उपयोग करता है यदि कई अनुरोध साझा एक ही शीघ्र पूर्व, यह पूर्व के KV-कैश 计算结果, दोहराव गणना से बचने के लिए, का उपयोग कर सकता है यह प्रणाली शीघ्र 长且固定的应用(如RAG、Agent) विशेष रूप से प्रभावी

> **【拓展：Prompt Caching 的成本节省】**मानव के त्वरित कैशिंग को दोहराया जाएगा पूर्व के इनपुट लागत घटकर लगभग 90% होगा।$0.50/M tokens（原价 $5)── सिस्टम पर त्वरित 5K टोकन + औसत 10 बार दोहराया जाने वाला परिदृश्य, मासिक लागत लगभग 75% कम हो सकती है──


![Prompt caching: write once, read cheap](../assets/prompt-caching.svg)

**The mechanic.**जब किसी अनुरोध का पूर्वावलोकन हाल के अनुरोध से मेल खाता है, तो प्रदाता टोकन को फिर से एन्कोडिंग के बजाय पिछले रन से KV-कैश की सेवा करता है। आप पहली बार एक छोटा लेखन प्रीमियम और हर बार एक बड़ी रीड डिस्काउंट का भुगतान करते हैं।

> **机制。**जब अनुरोध के पूर्व से हालिया अनुरोध के पूर्व मेल खाते हैं, तो आपूर्तिकर्ता को पहले से ही KV-कैश प्रदान किया जाता है, फिर से कोडित टोकन के बजाय।

**Three provider flavors in 2026.**

| Provider | API style | Hit discount | Write premium | Default TTL | Min cacheable |
|---------|-----------|--------------|---------------|-------------|---------------|
| Anthropic | Explicit `cache_control` markers on content blocks | 90% off input | 25% surcharge | 5 min (extendable to 1 hour) | 1,024 tokens (Sonnet/Opus), 2,048 (Haiku) |
| OpenAI | Automatic prefix detection | 50% off input | none | Up to 1 hour (best-effort) | 1,024 tokens |
| Google (Gemini) | Explicit `CachedContent` API | Storage-billed; read at ~25% of normal | Storage fee per token·hour | User-set (default 1 hour) | 4,096 tokens (Flash), 32,768 (Pro) |

**The invariant.**केवल तीनों कैश प्रीफिक्स। यदि किसी भी टोकन के बीच अनुरोधों में अंतर है, तो पहले भिन्न टोकन के बाद सब कुछ एक चूक है। शीर्ष पर * स्थिर * भागों, * चर * भागों को नीचे रखें।

> **不变量。**तीनों का केवल एक ही संग्रहण है। यदि अनुरोध के बीच कोई भी टोकन है, तो पहला अलग-अलग टोकन है। इसके बाद सभी सामग्री अप्रयुक्त है।

### कैश अनुकूल लेआउट

```
[system prompt]          <-- cache this
[tool definitions]       <-- cache this
[few-shot examples]      <-- cache this
[retrieved documents]    <-- cache if reused, else don't
[conversation history]   <-- cache up to last turn
[current user message]   <-- never cache (different every time)
```

आदेश का उल्लंघन करें  सिस्टम प्रॉम्प्ट के ऊपर उपयोगकर्ता संदेश रखें, कुछ शॉट्स के बीच गतिशील पुनर्प्राप्ति को छोड़ दें  और कैश कभी हिट नहीं करता है।

>  क्रमानुसार  उपयोगकर्ता संदेश को सिस्टम टिप पर रखा जाएगा,  कैश स्टोरेज हमेशा के लिए नहीं रहेगा 

### ब्रेक-ईवेंस गणना

एंथ्रोपिक के 25% लेखन प्रीमियम का मतलब है कि नेट-सॉवर पैसे के लिए कैश ब्लॉक को कम से कम दो बार पढ़ा जाना चाहिए। 1 लिखें + 1 पढ़ें प्रति अनुरोध औसत 0.675x लागत (बचत 32%); 1 लिखें + 10 पढ़ें औसत 0.205x (बचत 80%) । अंगूठे का नियमः कुछ भी कैश आप TTL के भीतर कम से कम 3 बार पुनः उपयोग करने की उम्मीद है.

> मानविकी के 25%  write in premium का अर्थ है कि भंडारण ब्लॉक को कम से कम दो बार पढ़ा जाना चाहिए ताकि शुद्ध रूप से पैसा बचाया जा सके।

## इसे बनाओ, इसे पूरा करो।
```figure
prompt-cache-hit
```

## इसे बनाओ

### चरण 1: स्पष्ट मार्करों के साथ मानव संकेत कैशिंग

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

`cache_control`मार्कर एंथ्रोपिक को 5 मिनट के लिए ब्लॉक को स्टोर करने के लिए कहता है। उस विंडो के भीतर पुनः उपयोग हिट; समाप्त होने के बाद पुनः उपयोग और फिर से लिखता है।

> `cache_control`标记告诉人类将该块存储 5 分钟.

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

यदि  में दोनों फ़ील्डों की जाँच करें`cache_read_input_tokens`अनुरोधों के बीच शून्य पर रहता है, अपने कैश कुंजी बहाव कर रहे हैं.

> इन दोनों खण्डों को जांचें यदि`cache_read_input_tokens`कई बार अनुरोध में शून्य के लिए बनाए रखें, आपका कैशबैक कुंजी भटक रही है।

### चरण 2: एक घंटे का विस्तारित टीटीएल

लंबे समय तक चलने वाली बैच नौकरियों के लिए, 5 मिनट का डिफ़ॉल्ट कार्य कार्य के बीच समाप्त होता है।`ttl`:

```python
{"type": "text", "text": RUBRIC, "cache_control": {"type": "ephemeral", "ttl": "1h"}}
```

1 घंटे का टीटीएल लेखन प्रीमियम (50% की तुलना में 25%) का 2 गुना है, लेकिन 5 से अधिक बार उपसर्ग का पुनः उपयोग करने वाले किसी भी बैच पर तेजी से भुगतान करता है।

> 1 小时 TTL के लिए लिखित प्रीमियम का 2 गुना है (किस्म के 50% के बजाय 25%), लेकिन किसी भी पुनः उपयोग से पहले 5 बार से अधिक के थोक प्रसंस्करण में बहुत जल्दी वापस आ गया है।

### चरण 3: ओपनएआई स्वचालित कैशिंग

OpenAI आपको कॉन्फ़िगर करने के लिए कुछ भी नहीं देता है. 1,024 टोकन से अधिक कोई भी पूर्वावलोकन जो हाल ही में अनुरोध से मेल खाता है स्वचालित रूप से 50% छूट प्राप्त करता है।

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

वही कैश-अनुकूल लेआउट नियम लागू होता है. दो चीजें OpenAI के कैश को मारती हैं जो Anthropic को नहीं मारती हैंः बदलना `user`क्षेत्र (कैश कुंजी घटक के रूप में उपयोग किया जाता है) और पुनर्गठन उपकरण।

> इसी तरह कैशबॉग के नियम लागू होते हैं। दो चीजें ओपनएआई के कैशबॉग को मार देंगी और एंथ्रोपिक को नहीं मारेंगी: बदलाव `user`字段和重新排序工具──

### चरण 4: मिथुन स्पष्ट संदर्भ कैशिंग

मिथुन कैश को एक प्रथम श्रेणी के वस्तु के रूप में व्यवहार करता है जिसे आप बनाते हैं और नाम देते हैंः

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

मिथुन प्रति टोकन·घंटे के लिए भंडारण चार्ज करता है जब तक कैश रहता है, और सामान्य इनपुट दर के ~ 25% पर पढ़ता है। यह सही आकार है जब आप कई सत्रों में कई दिनों के दौरान एक ही विशाल प्रॉम्प्ट का पुनः उपयोग करते हैं।

> Gemini 按缓存存活期间每代币·小时收取存储费,读取费率约为正常输入的25%──当你在多次会话中跨天重复使用相同的大型提示时,这是正确的选择──

### चरण 5: उत्पादन में हिट दर का माप

देखो`code/main.py`एक अनुकरण तीन प्रदाता लेखाकार के लिए जो लिखता है / पढ़ता है / याद करता है गणना और 1K अनुरोधों के प्रति मिश्रित लागत की गणना करता है। गेट एक लक्ष्य हिट दर पर तैनात करता है  अधिकांश उत्पादन मानव सेटअप को गर्म होने के बाद > 80% पढ़ने का अंश देखना चाहिए।

> 见 `code/main.py`获取模拟的三供应商会计师,跟踪写入/读取/未命中计数并计算每千请求的混合成本──按目标命中率门控部署多数生产 预热后应见在预热设置 >80% 读取比例──

## 2026 में भी फंसे हुए जाल

> 2026 में भी इस तरह की स्थिति बनी हुई है।

- **Dynamic timestamps at the top.** `"Current time: 2026-04-22 15:30:02"`सिस्टम प्रॉम्प्ट के शीर्ष पर. हर अनुरोध चूक जाता है. समय टिकट कैश ब्रेकपॉइंट से नीचे ले जाएं.
  **顶部的动态时间戳。**系统提示顶部放 `"Current time: 2026-04-22 15:30:02"` प्रत्येक अनुरोध का समय  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में  काश के अंत में 
- **Tool reordering.**स्थिर क्रम में उपकरण को क्रमबद्ध करें  तैनाती के बीच एक निर्दिष्ट पुनर्व्यवस्थापन हर हिट को तोड़ता है।
  **工具重排序。**इस स्थिर क्रम क्रम क्रमबद्धकरण उपकरण 部署间的字典重排破坏每次命中──
- **Free-text near-duplicates.**"आप सहायक हैं" बनाम "आप सहायक हैं"  एक बाइट अंतर = पूर्ण चूक।
  **自由文本近似重复。**"आप सहायक हैं" बनाम "आप सहायक हैं।"
- **Too-small blocks.**एंथ्रोपिक 1,024 टोकन (2,048 हैकू के लिए) की मंजिल लागू करता है। छोटे ब्लॉक चुपचाप कैश नहीं करते हैं।
  **过小的块。**मानव 强制 1,024 टोकन 下限(हायकू 为 2,048)。更小的块静默不缓存。
- **Blind cost dashboards.**"इनपुट टोकन" को कैश बनाम अनकैश में विभाजित करें अन्यथा ट्रैफ़िक में गिरावट कैश जीत की तरह दिखती है।
  **盲目的成本仪表板。**"输入 टोकन" को कैश में विघटित करें बनाम 未 कैश में। अन्यथा प्रवाह घटता है कैश जीतने की तरह दिखता है।

## इसे फ्रेमवर्क के साथ लागू करें

2026 कैशिंग स्टैकः

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

उपयोगकर्ता-संदेश परत के लिए अर्थिक कैशिंग (चरण 11 · 11) के साथ संयोजनः शीघ्र कैशिंग हैंडल *टोकन-समान* पुनः उपयोग, अर्थिक कैशिंग हैंडल *मतलब-समान* पुनः उपयोग।

> के लिए प्रयोग किया जाता है उपयोगकर्ता संदेश स्तर:提示缓存处理*token 完全相同* के重用,语义缓存处理*语义相同* के重用──

## इसे भेजें उत्पाद

सहेजें`outputs/skill-prompt-caching-planner.md`:

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

## अभ्यास विषय

1. **Easy.**एक 10 टर्न बातचीत के साथ एक 5,000 टोकन प्रणाली संकेत क्लाउड के खिलाफ.`cache_control`और फिर साथ. प्रत्येक के लिए इनपुट टोकन बिल रिपोर्ट.
   取一个10轮对话和5000 टोकन 系统提示,不使用和使用 `cache_control`分別运行, रिपोर्ट输入 टोकन 费用──
2. **Medium.**एक परीक्षण हर्नस लिखें जो एक शीघ्र टेम्पलेट और एक अनुरोध लॉग को देखते हुए, प्रति प्रदाता (एंट्रोपिक 5m, एंट्रोपिक 1h, ओपनएआई स्वचालित, जुड़वां स्पष्ट) के अपेक्षित हिट दर और डॉलर की बचत की गणना करता है।
   परीक्षण उपकरण, सुझावों का पैटर्न और अनुरोध की तारीख लिखना, प्रत्येक प्रदाता की अपेक्षित भाग्य दर और बचत राशि की गणना करना
3. **Hard.**एक लेआउट अनुकूलक बनाएंः एक प्रॉम्प्ट और चिह्नित क्षेत्रों की सूची दी गई `stable=True/False`, एक वास्तविक मानव अंत बिंदु पर सत्यापित करें जानकारी खोने के बिना अधिकतम कैश-अनुकूल स्थिति पर एक एकल कैश ब्रेकपॉइंट रखने के लिए प्रम्प्ट को फिर से लिखें.
   构建布局优化器:重写提示将缓存断点放在最大缓存友好位置――

## कीवर्ड्स  शब्द खोज तालिका

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

## आगे पढ़ना 延伸閱讀

- [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) `cache_control`, 1 घंटे TTL, तोड़ समतल टेबल.
  मानव 提示缓存文档cache_control、1 小时 TTL、亏平衡表──
- [OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) स्वचालित उपसर्ग मिलान।
  OpenAI 提示缓存文档自动前匹配──
- [Google — Context caching](https://ai.google.dev/gemini-api/docs/caching) `CachedContent`एपीआई और भंडारण मूल्य निर्धारण।
  Google 上下文缓存文档CachedContent API 和存储定价──
- [Anthropic engineering — Prompt caching for long-context workloads](https://www.anthropic.com/news/prompt-caching) विलंबता संख्याओं के साथ मूल लॉन्च पोस्ट।
  मानविकी 工程博客长上下文工作负载的提示缓存,含延迟数据──
- चरण 11 · 05 (सामग्री इंजीनियरिंग)  जहां प्रॉम्प्ट को स्लाइड करने के लिए ताकि कैश लैंड कर सके।
  第 11 阶段 · 05 上下文工程) 在哪里切分提示以便缓存生效──
- चरण 11 · 11 (कैशिंग और लागत)  उपयोगकर्ता संदेशों पर एक अर्थपूर्ण कैश के साथ कस्टिंग कस्टिंग जोड़ी।
  第 11 阶段 · 11(缓存与成本) 
- [Pope et al., "Efficiently Scaling Transformer Inference" (2022)](https://arxiv.org/abs/2211.05102) KV-कैश मेमोरी मॉडल जो कैशिंग को उपयोगकर्ताओं के लिए उजागर करता है; यह बताता है कि कैश किए गए प्रीफिक्स को फिर से पढ़ने के लिए पुनः गणना करने की तुलना में ~ 10 गुना सस्ता क्यों है।
  解释为什么缓存前比重算便宜约10倍KV-cache内存模型论文──
- [Agrawal et al., "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills" (2023)](https://arxiv.org/abs/2308.16369) prefill चरण शीघ्र कैशिंग शॉर्टकट है; यह पेपर बताता है कि TTFT कैश हिट पर नाटकीय रूप से गिरता है जबकि TPOT अप्रभावित है।
  解释为什么缓存命中时TTFT大幅下降而TPOT不受影响的论文──
- [Leviathan et al., "Fast Inference from Transformers via Speculative Decoding" (2023)](https://arxiv.org/abs/2211.17192) शीघ्र कैशिंग अनुमानित डिकोडिंग, फ्लैश ध्यान, और MQA/GQA के साथ बैठता है जो अनुमान लागत वक्र को मोड़ते हैं; अन्य तीनों के लिए इसे पढ़ें।
  提示缓存与投机解码、Flash Attention 和 MQA/GQA 并列的推理成本曲线杆──
