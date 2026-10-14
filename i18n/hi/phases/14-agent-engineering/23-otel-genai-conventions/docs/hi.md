# ओपनटेलीमेट्री जेएनएआई सेमेटिक सम्मेलनों

> ओपनटेलीमेट्री के जेएनएआई एसआईजी (अप्रैल 2024 में लॉन्च) एजेंट टेलीमेट्री के लिए मानक योजना को परिभाषित करता है। स्पैन नाम, विशेषताएं और सामग्री कैप्चर नियम विक्रेताओं के बीच एक जैसे होते हैं इसलिए एजेंट ट्रैक का मतलब डेटाडॉग, ग्राफाना, जैगर और हनीकॉमब में एक ही बात होती है।

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 13 (LangGraph), Phase 14 · 24 (Observability Platforms) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## सीखने के लक्ष्य

- GenAI अवधि श्रेणियों का नाम देंः मॉडल/ग्राहक, एजेंट, उपकरण।
- अंतर करें `invoke_agent`ग्राहक बनाम आंतरिक अवधि और जब प्रत्येक लागू होता है।
- शीर्ष स्तर के GenAI गुणों की सूची बनाएंः प्रदाता नाम, अनुरोध मॉडल, डेटा स्रोत आईडी।
- सामग्री कैप्चर अनुबंध की व्याख्या करेंः ऑप्ट-इन, `OTEL_SEMCONV_STABILITY_OPT_IN`, बाहरी संदर्भ सिफारिश।

## समस्या  समस्या परिचय

> **【中文解读】**प्रत्येक आपूर्तिकर्ता ने अपना स्वयं का नाम विकसित किया, परिचालन टीम को अंततः प्रत्येक ढांचे के लिए स्वतंत्र उपकरण बनाने की आवश्यकता है।

प्रत्येक विक्रेता अपना स्वयं का नाम बनाता है। ऑपरेशन टीमें प्रति फ्रेमवर्क डैशबोर्ड बनाती हैं। ओपनटेलीमेट्री के जेएनएआई एसआईजी पूरे पारिस्थितिकी तंत्र के लक्ष्यों को एक मानक द्वारा परिभाषित करके इसे ठीक करता है।

> प्रत्येक आपूर्तिकर्ता ने अपनी अवधि का आविष्कार किया है ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙ ∙  ∙ ∙ ∙ ∙ ∙ ∙    ∙ ∙    ∙ ∙                                                                                                                                                                                          

> **【拓展：OTel GenAI 规范的跨平台统一】**OpenTelemetry GenAI 语义约定 (2024年4月启动) 定义 Agent 遥测的标准方案:span 名称、属性和内容捕获规则跨供应商统一,使 Agent 追踪在 Datadog、Grafana、Jaeger 和 Honeycomb 中具有相同语义──一次埋点,多后端通用──

>  **【前置】**学本节前 कृपया पहले समझेंः चरण 14·01(एजेंट लूप) आपको पहले एजेंट की आवश्यकता है यह इसे दफन करने के लिए; चरण 14·13(लंगग्राफ)  राज्य चित्र को समझने के लिए, क्योंकि span के पिता-स्तरीय स्तर का चित्रण है पूरे इतिहास का दर्पण।

## अवधारणा का मूल अवधारणा

### स्पेन श्रेणियाँ

>  **【类比】**ओटेल जेएनएआई के तीन वर्गों का अवधि 像医院的分级诊疗记录:**Model span**                                                                                                                                                                                                                                                              **Agent span**                                                                                                                                                                                                                                                              **Tool span**️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️`parent_span_id`链回父记录这样的数据库 里你能展开看: पूरा एजेंट 调用 → 5 बार उपकरण调用 → प्रत्येक उपकरण调用里 2 बार LLM 调用──

1. **Model / client spans.**कच्चे एलएलएम कॉल को कवर करें। प्रदाता एसडीके (एथ्रोपिक, ओपनएआई, बेड्रॉक) और फ्रेमवर्क मॉडल एडाप्टर द्वारा जारी किया जाता है।
2. **Agent spans.** `create_agent`(जब एजेंट का निर्माण किया जाता है) और `invoke_agent`(जब यह चलाता है) ।
3. **Tool spans.**प्रति उपकरण कॉल एक; माता-पिता-बच्चे संबंध द्वारा एजेंट स्पैन से जुड़ा हुआ है।

### एजेंट स्पैन नामकरण

- स्पेनिश नाम: `invoke_agent {gen_ai.agent.name}`यदि नामित है; `invoke_agent`. .
- स्पैन प्रकारः
  - **CLIENT** दूरस्थ एजेंट सेवाओं (OpenAI सहायक एपीआई, बेडरोक एजेंट) के लिए।
  - **INTERNAL** प्रक्रिया में एजेंट फ्रेमवर्क (लंगचेन, क्रूएआई, स्थानीय रिएक्ट) के लिए।

### मुख्य विशेषताएं

- `gen_ai.provider.name` `anthropic`,`openai`,`aws.bedrock`,`google.vertex`. .
- `gen_ai.request.model` मॉडल आईडी।
- `gen_ai.response.model` हल मॉडल (रूटिंग के कारण अनुरोध से भिन्न हो सकता है) ।
- `gen_ai.agent.name` एजेंट पहचानकर्ता।
- `gen_ai.operation.name` `chat`,`completion`,`invoke_agent`,`tool_call`. .
- `gen_ai.data_source.id` आरएजी के लिएः किस कॉर्पस या स्टोर से परामर्श किया गया था।

मानव, Azure AI इन्फरेंस, AWS बेड्रॉक, OpenAI के लिए प्रौद्योगिकी-विशिष्ट सम्मेलन मौजूद हैं।

> OpenTelemetry GenAI ने LLM और एजेंट के लिए उपलब्ध मानदंडों को परिभाषित किया है।`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`और...

### सामग्री कैप्चर

> ️ **【易错点】**场景: विकासकर्ता图省事在 `invoke_agent`后果:运维在Jaeger 网页里点开就能看到所有明文,Datadog还会索引做全文检索,等于把合规风险扩散到整个观测链路 → 修复:默认关闭内容捕获,需要时只在跨度里存指标 ID如`gen_ai.input.message_id=row42`), मूल落到带带 ACL के वस्तु भंडार S3 里,运维要查时通过 ID 跳转授权访问──这就是本节反复强调的"बाहरी-参考推"──

डिफ़ॉल्ट नियमः उपकरण डिफ़ॉल्ट रूप से इनपुट/आउटपुट को कैप्चर नहीं करना चाहिए। कैप्चर को ऑप्ट-इन के माध्यम से किया जाता हैः

> OpenTelemetry GenAI ने LLM और एजेंट के लिए उपलब्ध मानदंडों को परिभाषित किया है।`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`और...

- `gen_ai.system_instructions`
- `gen_ai.input.messages`
- `gen_ai.output.messages`

अनुशंसित उत्पादन पैटर्नः सामग्री को बाहरी रूप से स्टोर करें (S3, आपका लॉग स्टोर), स्पैन पर संदर्भ रिकॉर्ड करें (पॉइंटर आईडी, प्रोसा नहीं) । यह पाठ 27 सामग्री विषाक्तता रक्षा है जो पर्यवेक्षण में तारबद्ध है।

> 推的生产模式:将内容外存储(S3、你的日志存储),在 span上记录引用(指针 ID,不是原文) 

> OpenTelemetry GenAI ने LLM और एजेंट के लिए उपलब्ध मानदंडों को परिभाषित किया है।`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`और...

### स्थिरता

मार्च 2026 तक अधिकांश सम्मेलन प्रयोगात्मक हैं।

> OpenTelemetry GenAI ने LLM और एजेंट के लिए उपलब्ध मानदंडों को परिभाषित किया है।`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`और...

```
OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental
```

डेटाडॉग v1.37+ मानचित्र जेएनएआई ने अपने एलएलएम ऑब्जर्वेबिलिटी स्कीम में मूल रूप से श्रेय दिया है। अन्य बैकेंड (ग्राफाना, हनीकॉम्ब, जैगर) कच्चे गुणों का समर्थन करते हैं।

> 🤔 **【困惑】**प्रश्नः `invoke_agent`span 什么时候标签CLIENT,什么时候标签INTERNAL? looks very rounded── A: 看被调用的代理是不是"另一个进程/服务"── यदि आप सीधे Python 进程里 आयात LangChain 运行一个 ReAct, तो यह INTERNAL您自己的代码内子调用── यदि आप OpenAI सहायक API या AWS बेडरोक एजेंट्स को调用 करते हैं, तो यह दूरस्थ HTTP 调用,标签CLIENT──CLIENT span भी स्वचालित रूप से RPC 相关属性 जैसे(`rpc.system``rpc.service`), सुविधा एवं पारंपरिक सेवा अनुवर्ती

> डाटाडॉग v1.37+ 原生将 GenAI 属性映射到其LLM Observability schema──其他后端(Grafana、Honeycomb、Jaeger) समर्थन原始属性──

> OpenTelemetry GenAI ने LLM और एजेंट के लिए उपलब्ध मानदंडों को परिभाषित किया है।`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`और...

### जहां यह पैटर्न गलत हो जाता है

- **Capturing full prompts in spans.**पीआई, रहस्य, ग्राहक डेटा जो ओपी पढ़ सकते हैं।
- **No `gen_ai.provider.name`.**बहु-प्रदाता डैशबोर्ड टूट जाते हैं जब श्रेय गायब होता है।
- **Spans without parent links.**अनाथ उपकरण फैलता है, हमेशा संदर्भ को फैलाने.
- **Not setting stability opt-in.**आपके गुणों को बैक-एंड उन्नयन पर नाम बदल दिया जा सकता है।

> **在 span 中捕获完整提示。**运维可以读取的追踪中包含PII、密钥、客户数据──外部存储──
> **缺少 `gen_ai.provider.name`。**缺少归属时,多供应商仪表盘会出错.
> **没有父链接的 span。**孤立的工具 span──始终传播上下文──
> **不设置稳定性选择加入。**आपका गुण बाद में उन्नयन के दौरान पुनः नामित किया जा सकता है।

## इसे बनाओ, इसे पूरा करो।
```figure
ae-genai-span-tree
```

## इसे बनाओ

`code/main.py`GenAI सम्मेलनों से मेल खाने वाले एक stdlib स्पैन उत्सर्जक को लागू करता हैः

> OpenTelemetry GenAI ने LLM और एजेंट के लिए उपलब्ध मानदंडों को परिभाषित किया है।`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`और...

- `Span`GenAI विशेषता योजना के साथ।
- `Tracer`के साथ`start_span`, घोंसले हुए संदर्भों.
- एक स्क्रिप्ट एजेंट चलाता है जो उत्सर्जन करता हैः `create_agent`,`invoke_agent`(आंतरिक), प्रति उपकरण स्पैन्स, `chat`LLM कॉल के लिए अवधि।
- सामग्री कैप्चर मोड जो बाहरी रूप से संकेतों को संग्रहीत करता है और स्पैन पर आईडी रिकॉर्ड करता है।

इसे चलाओः

```
python3 code/main.py
```

आउटपुटः सभी आवश्यक GenAI गुणों के साथ एक स्पैन ट्री और ऑप्ट-इन सामग्री संदर्भों को दिखाने वाला एक "बाहरी स्टोर"

> 输出: एक जिसमें सभी आवश्यक GenAI 属性 span 树, तथा एक प्रदर्शित चयन सामग्री引用的" बाह्य भंडारण"

> OpenTelemetry GenAI ने LLM और एजेंट के लिए उपलब्ध मानदंडों को परिभाषित किया है।`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`और...

## इसे फ्रेमवर्क के साथ लागू करें

- **Datadog LLM Observability**(v1.37+) नक्शे गुण मूल रूप से.
- **Langfuse / Phoenix / Opik**(पाठ 24)  ऑटो-इकोसिस्टम को उपकरण।
- **Jaeger / Honeycomb / Grafana Tempo** कच्चे ओटेल निशान; GenAI गुणों से डैशबोर्ड बनाएँ।
- **Self-hosted** ओटेल कलेक्टर को जीएनएआई प्रोसेसर से चलाएं।

## इसे भेजें उत्पाद

`outputs/skill-otel-genai.md`तार OTel GenAI सामग्री कैप्चर डिफ़ॉल्ट और बाहरी संदर्भ भंडारण के साथ एक मौजूदा एजेंट में फैलता है।

> `outputs/skill-otel-genai.md`ओटीएल जीएनएआई अवधि को शामिल करना मौजूदा एजेंट, सामग्री कैप्चर डिफ़ॉल्ट मान और बाहरी संदर्भ भंडारण शामिल है

> OpenTelemetry GenAI ने LLM और एजेंट के लिए उपलब्ध मानदंडों को परिभाषित किया है।`gen_ai.request.model``gen_ai.usage.input_tokens``gen_ai.agent.name`और...

## अभ्यास विषय

1. अपने पाठ 01 के साथ रीएक्ट लूप का उपयोग करें`invoke_agent`(आंतरिक) + प्रति उपकरण स्पैन. एक Jaeger उदाहरण भेजें.
  中文翻译:思考并实践此练习──
2. "केवल संदर्भ" मोड में सामग्री कैप्चर जोड़ेंः SQLite के लिए प्रॉम्प्ट, स्पैन गुण केवल पंक्ति आईडी रखते हैं।
  中文翻译:思考并实践此练习──
3. विवरण पढ़ें`gen_ai.data_source.id`. इसे अपने पाठ 09 मेमो खोज में वायर करें.
  中文翻译:思考并实践此练习──
4. सेट `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`और अपने गुणों को सत्यापित करने के लिए नहीं प्राप्त करने के लिए नाम संग्रहकर्ता द्वारा.
  中文翻译:思考并实践此练习──
5. एक डैशबोर्ड बनाएंः केवल GenAI गुणों से "कौन से उपकरण त्रुटियां किस मॉडल के साथ सहसंबंधित हैं।
  中文翻译:思考并实践此练习──

## कीवर्ड्स  शब्द खोज तालिका

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

## आगे पढ़ना 延伸閱讀

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) विनिर्देश
  中文翻译:见原文──
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) डिफ़ॉल्ट रूप से GenAI अवधि
  中文翻译:见原文──
- [AutoGen v0.4 (Microsoft Research)](https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/) ओटीएल स्पैन्स में निर्मित
  中文翻译:见原文──
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) W3C ट्रैक संदर्भ प्रसार
  中文翻译:见原文──
