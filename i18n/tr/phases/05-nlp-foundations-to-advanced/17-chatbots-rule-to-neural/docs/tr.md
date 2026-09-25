# Chatbotlar  Kural tabanlı Neural ile LLM ajanlarına  聊天机器人  规则到神经网络到LLM ajanlarına

> ELIZA, örneğe eşleşen bir cevap verdi. DialogFlow niyetleri haritası yaptı. GPT ağırlıklardan cevap verdi. Claude araçları çalıştı ve doğruladı. Her dönem önceki en kötü başarısızlığı çözdü.
> ELIZA ÜL Mode匹配回复──DialogFlow 映射意图──GPT 权重中回答──Claude 运行工具并验证──每个时代解决了上一个时代最严重失败──

> **【中文解读】**ELIZA'dan Seq2Seq'e GPT Ajanına kadar.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 13 (Question Answering), Phase 5 · 14 (Information Retrieval) | **前置知识:** Phase 5 · 13（问答系统），Phase 5 · 14（信息检索与搜索）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Bir kullanıcı "Uçuşumu değiştirmek istiyorum" diyor. Sistem ne istediğini, hangi bilgileri eksik olduğunu, nasıl alacağını ve eylemini nasıl tamamlayacağını bulmalıdır.

> Kullanıcı "I Wanna Change Your Flight" diyor. Sistem ne istediğini anlamalıdır.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

Bir ML sistemi için konuşma zor. Giriş açık. Çıkış birçok dönüşte tutarlı olmalıdır. Sistemin dünyayı etkilemesi gerekebilir (uçuş değiştir, kart yükleme). Her yanlış adım kullanıcıya görünür.

> ML sistemleri için konuşma çok zor. Giriş açık bir şekilde yapılmaktadır. Çıkış çok sayıda döngü içinde devam etmesi gerekir. Sistemler dünyayı etkilemesi gerekebilir.

Chatbot mimarlıkları dört paradigma ile döngüye girdi, her biri önceki birinin çok görünür bir şekilde başarısız olduğu için kuruldu. Bu ders onları sıraya getiriyor. 2026 üretim manzarası son ikiliğin bir hibrididir.

> 聊天机器人架构经历了四种范式,各种都是因为前一种失败太明显而引入的――本课顺序讲解――2026年生产环境是后者的混合――

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

![Chatbot evolution: rule-based → retrieval → neural → agent](../assets/chatbot.svg)

### Yazılı yarım yüzyıl, 1950-2001

İlk paradigma beş yıl sürmedi. elli yıl sürdü. Onun arkını bilmek önemlidir çünkü içindeki her sistem aynı makine  eşleşen girişi, konserve bir yanıt yayıyor, küçük bir durum  güncelleştirir ve bu makineye kural eklemenin elli yılı genel durumun hiçbir zaman üretilmedi. Bu tavan paradigmaların iki ile dört arasında var olmasının nedeni budur.

**1950.**Turing, "makine düşünüyor mu?" sorusunu ameliyatçı bir değiştirme önerisiyle atlatıyor: Eğer bir sorgulayıcı, bir kişiyi makineden bir telefontep üzerinden ayırt edemezse, felsefi soru tartışmalıdır.

**1956.**İsim Dartmouth'da yazda yapılan bir atölyede "Yapay zeka" paraları üzerine gelir. Bu isim, "bilginliğin her özelliğinin, prensip olarak, onu simüle edecek bir makine yapabileceği kadar kesin olarak tanımlanabileceği" tahmininde yer alır.

**1966.**ELIZA, 1. Adımda oluşturduğunuz yansıma hilesini gönderir: Çürümesi kuralları girişten parçalar çeker, yeniden monte etme kuralları onları soru olarak geri yankılar. 200'e yakın kalıp toplam, sıfır durum, sıfır anlayış  ve kullanıcılar buna her şekilde güvendi. Weizenbaum kariyerinin geri kalanını ne kadar az makine aldığından endişelenerek geçirdi.

**1972.**PARRY, Stanford'da paranoya modelini oluşturmuş, ELIZA'nın eksik olduğu bir parça ekliyor: İç durum. Korku, öfke ve güvensizlik için sayısal değişkenler, senaryolar sonraki açılışta her dönüşte ve kapıda güncellenir. Böylece aynı girişler şimdiye kadarki konuşmaya bağlı olarak farklı tepkiler üretir. Kör bir transkript testiyle psikiyatristler PARRY'yi insan hastalarından rastgele ayırt ettiler. Kişiliği koşullandırmanın doğrudan atalarıdır  üç yüzen olarak uygulanan bir sistem uyarısı. Aynı yıl, iki bot ARPANET üzerinden birbirine işaret edildi: bir terapist senaryosu paranoya durum makinesi ile röportaj yaparken, bir ağdaki ilk bot-bot konuşması.

**1995.**ALICE, AIML ile ELIZA tarifini ölçeklendirir. Bu, örnektir-şablon çiftleri için XML diyalektidir. Yaklaşık 40.000 el yazılı kategoriler, üç Loebner Ödülü kazandı. Kurallara dayalı sistemlerin ölçeklendirme yasasını kanıtladı: daha fazla kural kapsamayı satın alır, asla genellik. Her kural birisinin koruması gereken bir yüktür.

**2001.**SmarterChild, 30 milyon anlık mesajlaşma kullanıcısının önüne girer ve arka plan bakışlarını  hava, stoklar, film zamanları  şablonlara ekler.

Paradigma, kimsenin onu reddetmesinden değil, el yazılı devlet makinelerinin bakım maliyetinin kapsamıyla doğrusal olarak büyüdüğünden ve kullanıcı beklentilerinin geçen hafta gördükleri ile büyüdüğünden sona erdi.

```figure
chatbot-lineage
```

**Rule-based (ELIZA, AIML, DialogFlow).**El yazılı desenler kullanıcı girişleriyle eşleşir ve cevaplar üretir. İstek sınıflandırıcıları önceden tanımlanmış akışlara yönlendiriyor. Slot doldurma durum makineleri gerekli bilgileri toplar. tasarlanmış olan dar alan içinde parlak çalışır. Hemen dışarda başarısız olur. Hala halüsinasyonların hoşgörülmediği güvenlik kritik alanlarda (banking doğrulama, hava yolu rezervasyonu) gemi.

> **基于规则（ELIZA、AIML、DialogFlow）。**Handwriting Mode Match User Input and Produce Response──意图分类器路由到预定义流程──槽位填充状态机收集所需信息──设计的狭窄范围内表现出色──超出范围立即失败──仍在不容许幻觉的安全关键领域──银行认证、航空公司预订) 中使用──

**Retrieval-based.**Bu, bir sıklık sorusu tarzı sistemidir. Her çiftini kodlayın (söz, cevap). Çalışma zamanında, kullanıcının mesajını kodlayın ve en yakın depolanan yanıtı alın. Zendesk'in klasik "böylece makaleler" özelliğini düşünün. Kurallardan daha iyi parafrase kullanır.

> **基于检索。**FAQ 式システム──编码对对 (话语、响应) ・运行时编码用户消息并检索最近储存响应──类似于Zendesk'in klasik "相似文章" 功能──比规则更好地处理释义──无生成,所以无幻觉──

**Neural (seq2seq).**Çözümlü bir kodlama-dekoder, sohbet günlüğünde eğitimlidir. Baştan cevaplar üretir. Akıcı ancak genel çıkışlara eğilimli ("Bilmiyorum") ve gerçek sürükleme. Konuyla ilgili asla güvenilir değildir. Google, Facebook ve Microsoft'un 2016-2019 yıllarında hayal kırıklığına uğrayan chatbotları olması nedeni.

> **神经（seq2seq）。**Bu nedenle Google, Facebook ve Microsoft'un 2016-2019 yıllarında hayal kırıklığı yaratıcı sohbet makinelerinin olması sebebi olarak, bu konuyu güvenilmez şekilde tutmak için çalışmaktadır.

**LLM agents.**Bir dil modeli, sonuçları planlayan, araçları çağıran ve doğrulayan bir döngü içinde sarılmış bir dil modeli. Uzun bir istekle bir chatbot değil. Bir ajan döngüsü: plan → arama aracı → gözlem sonucu → bir sonraki adımı karar vermek. Arama-birinci yerleştirme (RAG) onu halüsinasyonlardan korur. Araç çağrıları aslında işleri yapmasına izin verir. Bu 2026 mimarisi.

> **LLM Agent。**包装在循环中的语言模型,规划、调用工具并验证结果──不是带长提示的聊天机器人──一个代理 循环:规划 → 调用工具 → 观察结果 →决定下一步──检索优先的定(RAG) 防止幻觉──工具调用让它实际做事──这是2026年架构──

Dört paradigma sıradan bir değiştirme değildir. 2026 üretim chatbotı dört yönüyle geçiyor: doğrulama ve yıkıcı eylemler için kural tabanlı, FAQ için geri alınma, doğal ifade için sinir jenerasyonu, belirsiz açık sorular için LLM ajanı.

> Bu dört tip bir düzen değişmez. 2026 yılında üretilen sohbet makineleri dört yolla geçer: Kanunlara dayalı doğrulama ve yıkıcı işlemler, sorgular için sorgular, doğaya yönelik beyin üretimi, belirsiz açık sorgular için LLM ajanı.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

### Adım 1: Kurallara dayalı örneğe eşleşme

```python
import re


class RulePattern:
    def __init__(self, pattern, response_template):
        self.regex = re.compile(pattern, re.IGNORECASE)
        self.template = response_template


PATTERNS = [
    RulePattern(r"my name is (\w+)", "Nice to meet you, {0}."),
    RulePattern(r"i (need|want) (.+)", "Why do you {0} {1}?"),
    RulePattern(r"i feel (.+)", "Why do you feel {0}?"),
    RulePattern(r"(.*)", "Tell me more about that."),
]


def rule_based_respond(user_input):
    for pattern in PATTERNS:
        m = pattern.regex.match(user_input.strip())
        if m:
            return pattern.template.format(*m.groups())
    return "I don't understand."
```

ELIZA 20 satırda. "Üzülüyorum" ("Ben üzgün hissediyorum" → "Neden üzgün hissediyorsun") refleks hilesi 1966'da Weizenbaum'dan gelen kanonik psikoterapist demo'dur.

> 20 行 ELIZA。反射技巧("Üzgün hissediyorum" → "Neden üzgün hissediyorsun") 1966 yılında Weizenbaum'un klasik psikolojik terapist gösterisi。

### Adım 2: Arama tabanlı (FAQ)

Bu örnek kısım için `pip install sentence-transformers`(Kahkahalar)`code/main.py`Bu dersin yerine bir stdlib Jaccard benzerliği kullanıldığı için dersi dış bağımlılıklardan uzak duruyor.

> Bu örnek kodlama parçası gerekiyor.`pip install sentence-transformers`(会拉取火) 〜 本课的可运行 `code/main.py`Standard Library'in Jaccard benzerliği yerine, bu tür dersler dıştan bağımlılık yoktur.

```python
from sentence_transformers import SentenceTransformer
import numpy as np


FAQ = [
    ("how do i reset my password", "Go to Settings > Security > Reset Password."),
    ("how do i cancel my order", "Go to Orders, find the order, click Cancel."),
    ("what is your return policy", "30-day returns on unused items, original packaging."),
]


encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
faq_questions = [q for q, _ in FAQ]
faq_embeddings = encoder.encode(faq_questions, normalize_embeddings=True)


def faq_respond(user_input, threshold=0.5):
    q_emb = encoder.encode([user_input], normalize_embeddings=True)[0]
    sims = faq_embeddings @ q_emb
    best = int(np.argmax(sims))
    if sims[best] < threshold:
        return None
    return FAQ[best][1]
```

Sınır tabanlı reddetme, en iyi eşleşmenin yeterince yakın olmadığı durumlarda, geri dön `None`ve sistemin tırmanmasına izin ver.

>  değerlere dayalı reddedilme, bir tasarım seçeneğidir.`None`让系统升级处理――

### Adım 3: Nöral jenerasyon (Başlam)

Küçük bir talimat ayarlı kodlayıcı-dekoder (FLAN-T5) veya ince ayarlı bir konuşma modeli kullanın. 2026'da kendi başına kullanılamaz (tüşünç, konu dışı sürükleme, gerçek saçmalık), ama doğal ifade için hibrit sistemler içinde gemiler. DialoGPT tarzı sadece dekodörlü modeller, tutarlı cevaplar üretmek için açık bir dönüş ayırıcıları ve EOS yönetimine ihtiyaç duyar; bir öğretim örneği için FLAN-T5 metin2 metin boru hattı kutudan dışarıda çalışır.

> Küçük talimatları kullanmak için kullanılır. FAN-T5) veya konuşma modelinin biçimlendirmesi için kullanılır.

```python
from transformers import pipeline

chatbot = pipeline("text2text-generation", model="google/flan-t5-small")

response = chatbot("Respond politely to: Hi there!", max_new_tokens=40)
print(response[0]["generated_text"])
```

### 4. Adım: LLM ajan döngüsü

2026 üretim şekli:

> 2026 yılındaki üretim biçimi:

```python
def agent_loop(user_message, tools, llm, max_steps=5):
    history = [{"role": "user", "content": user_message}]
    for _ in range(max_steps):
        response = llm(history, tools=tools)
        tool_call = response.get("tool_call")
        if tool_call:
            tool_name = tool_call.get("name")
            args = tool_call.get("arguments")
            if not isinstance(tool_name, str) or tool_name not in tools:
                history.append({"role": "assistant", "tool_call": tool_call})
                history.append({"role": "tool", "name": str(tool_name), "content": f"error: unknown tool {tool_name!r}"})
                continue
            if not isinstance(args, dict):
                history.append({"role": "assistant", "tool_call": tool_call})
                history.append({"role": "tool", "name": tool_name, "content": f"error: arguments must be a dict, got {type(args).__name__}"})
                continue
            fn = tools[tool_name]
            result = fn(**args)
            history.append({"role": "assistant", "tool_call": tool_call})
            history.append({"role": "tool", "name": tool_name, "content": result})
        else:
            return response["content"]
    return "I could not complete the task in the step budget."
```

Bu nedenle, bu işlemler, bir süre önce bir süre önce yapılan işlemlere ilişkin olarak, bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha

> Üç önemli nokta: araç, LLM'nin kullanılabilir bir işlevi.

Gerçek üretim ekler: ilk olarak yerleştirme (her LLM çağrısı öncesi ilgili belgeler enjekte), koruma (tatsil olmadan yıkıcı eylemleri reddet), gözlemlenebilirlik (her adımı kaydetmek) ve değerlendirme (özel kontroller ajan davranışının spesifik durumda kalmasını sağlar).

> 实际生产还需要:检索优先定(每次 LLM 调用前注入相关文档) 护(未经确认拒绝破坏性操作) 可观测性(记录每步) 和评估(自动检查代理 行为保持规范) 

### Adım 5: hibrit yönlendirme

```python
def hybrid_chat(user_input):
    if is_destructive_action(user_input):
        return structured_flow(user_input)

    faq_answer = faq_respond(user_input, threshold=0.6)
    if faq_answer:
        return faq_answer

    return agent_loop(user_input, tools, llm)


def is_destructive_action(text):
    danger_words = ["delete", "cancel", "charge", "refund", "transfer"]
    return any(w in text.lower() for w in danger_words)
```

Şekil: yıkıcı bir şey için belirleyici kurallar, konserveli Soru sorular için arama, diğer her şey için LLM ajanları. 2026 müşteri desteği sistemleri bu.

> 模式: herhangi bir yıkıcı işlem için kesinlik kuralları kullanmak, sabit FAQ kullanmak, kontrol etmek, LLM Ajanı kullanmak için her şey için.

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

2026'da:

> 2026 yılının teknolojisi:

| Use case / 使用场景 | Architecture / 架构 |
|---------|---------------|
| Booking, payment, authentication / 预订、支付、认证 | Rule-based state machines + slot filling / 基于规则的状态机 + 槽位填充 |
| Customer support FAQs / 客户支持 FAQ | Retrieval over curated answers / 对精选答案的检索 |
| Open-ended help chat / 开放式帮助聊天 | LLM agent with RAG + tool calls / 带 RAG + 工具调用的 LLM Agent |
| Internal tools / IDE assistants / 内部工具 / IDE 助手 | LLM agent with tool calls (search, read, write) / 带工具调用的 LLM Agent（搜索、读写） |
| Companion / character chatbots / 伴侣/角色聊天机器人 | Tuned LLM with persona system prompt, retrieval on knowledge / 微调 LLM 配角色系统提示和知识检索 |

Her zaman üretimde hibrit yönlendirme kullanın. Tek bir mimarlık her talebi iyi yönetmez. Routing katmanı kendisi tipik olarak küçük bir niyet sınıflandırıcısıdır.

> Üretim sırasında her zaman karışık yol kullanılır. Her soruyu işleyebilecek tek bir yapı yoktur.

## Hala gönderiliyor olan başarısızlık modları hala üretim başarısızlığı moduna girecek.

- **Confident fabrication.**Yumuşak başlılık: sonuçları doğrula, araç çağrılarını kaydet, LLM'nin başarılı bir araç dönüşü olmadan bir şey yaptığını iddia etmesine asla izin verme.
  **自信捏造。**LLM Ajanı, başarısız bir işlem tamamladığını iddia ediyor.
- **Prompt injection.**Kullanıcı, sistem istasyonunu geçersiz kılan metni ekler. LLM01 OWASP LLM Başvuruları 2025 için Top 10'da sıralamaktadır. İki tad: doğrudan enjeksiyon (çat'a yapıştırılmış) ve dolaylı enjeksiyon (evlatör okuyan belgelerde, e-postalarda veya araç çıkışlarında gizli).
  **提示注入。**User插入覆盖系统提示的文本── 在 OWASP LLM 应用 2025 Top 10 中排 LLM01──两种形式:直接注入(粘贴到聊天中) 和间接注入(藏在文档、邮件或代理 读取的工具输出中)

  Scenariye göre saldırı oranları değişir. Ölçülen başarı oranları, genel araç kullanım ve kodlama referans değerlerinde sınır modellerinde %0,5-8,5 arasında değişmektedir. Özel yüksek riskli ayarlamalar (Sİ kodlama ajanlarına yönelik uyarlama saldırıları, savunmasız orkestrasyon) %84'e ulaştı. Üretim CVE'leri arasında EchoLeak (CVE-2025-32711, CVSS 9.3)  bir saldırgan tarafından kontrol edilen e-posta tarafından tetiklenen Microsoft 365 Copilot'ta sıfır tıklama ile veri sızdırma hatası bulunmaktadır.
  攻撃 başarısı oranı, olaylara göre değişir. Genel araç kullanımında ve kodlama temelinde ön kenar modelinin ölçüm başarısı oranı yaklaşık 0.5-8.5%'dir.

  Yumuşaklıklar: Kullanıcı girişini döngü boyunca güvenilmez olarak ele alın; araç çağrılarından önce temizlenir; ana uyarıdan araç çıkışlarını izole eder; ajanın önce planladığı Plan-Tahmini-Etkinleştir (PVE) örneğini kullanır, ardından uygulamadan önce bu plana karşı her eylemini doğrulayır (bu, araç sonuçlarını yeni planlanmamış eylemler enjekte etmeden durdurur); yıkıcı eylemler için kullanıcı onayını gerektirir; araç alanlarına en az ayrıcalık uygulayın.
  缓解措施: tüm döngü boyunca kullanıcı girişini güvenilmez olarak görülecektir; tool调用前消毒; tool outputı ile ana noktaları ayır; planlama-teskik-ürümet (PVE) modeli kullanın,Agent önceden planlama, sonra her operasyon için planlama doğrulama sonrası tekrar gerçekleştirilmek için

  Bu riskin tamamen ortadan kaldırılmasına hiçbir zaman gerek yoktur.
  Bu nedenle, bu durumun tamamen ortadan kaldırılması için birçok önerme yapılmamıştır.
- **Scope creep.**Ajan, bir araç çağrısı ile ilgili bilgiyi geri döndüğünde görevden ayrılır.
  **范围蔓延。**Agent çünkü araç çağrısı indirekte ilgili bilgi ve koşuşturma soruları geri gönderir.
- **Infinite loops.**Ajan aynı araçları arıyor, kısıtlama: adım bütçesi, araç çağrıları kopyalanması, LLM yargıçı "yöntemleri mi yapıyoruz?"
  **无限循环。**Agent 持续调用相同工具──缓解:步骤预算、工具调用去重、LLM 判断" progressed"──
- **Context window exhaustion.**Uzun konuşmalar en erken dönüşleri bağlamdan dışarı çıkarır. Yumuşatma: eski dönüşleri özetlemek, benzerliklerle ilgili geçmiş dönüşleri almak veya uzun bağlamlı bir model kullanmak.
  **上下文窗口耗尽。**长对话将最早轮次推出上下文──缓解:摘要旧轮次、相似性检查相关历史轮次、或使用长上下文模型──

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-chatbot-architect.md`- ...

> 保存为 `outputs/skill-chatbot-architect.md`- ...

```markdown
---
name: chatbot-architect
description: Design a chatbot stack for a given use case.
version: 1.0.0
phase: 5
lesson: 17
tags: [nlp, agents, chatbot]
---

Given a product context (user need, compliance constraints, available tools, data volume), output:

1. Architecture. Rule-based, retrieval, neural, LLM agent, or hybrid (specify which paths go where).
2. LLM choice if applicable. Name the model family (Claude, GPT-4, Llama-3.1, Mixtral). Match to tool-use quality and cost.
3. Grounding strategy. RAG sources, retrieval method (see lesson 14), tool contracts.
4. Evaluation plan. Task success rate, tool-call correctness, off-task rate, hallucination rate on held-out dialogs.

Refuse to recommend a pure-LLM agent for any destructive action (payments, account deletion, data modification) without a structured confirmation flow. Refuse to skip the prompt-injection audit if the agent has write access to anything.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Egzersizler.

1. **Easy.**Bir kahve mağazası sipariş bot için yukarıdaki kural tabanlı cevap uygulamasını 10 model ile uygulayın. Test kenar vakaları: çift sipariş, değişiklikler, iptal, net olmayan niyet.
   **简单。**Bu nedenle, bu konularda, bir dizi farklı yöntemi oluşturan bir dizi yöntem bulunmaktadır.
2. **Medium.**Bir hibrid FAQ + LLM fallback oluşturun. SaaS ürünü için 50 konserve FAQ giriş, doküman sitesi üzerinden geri alınma ile LLM fallback. 100 gerçek destek sorusu üzerinde reddetme oranını ve doğruluğunu ölçün.
   **中等。**构建混合 FAQ + LLM 回退──50 个 SaaS 产品的固定 FAQ 条目,LLM 回退带文档站检索──100 个真实支持问题上测量拒绝率和准确率──
3. **Hard.**Yukarıdaki ajan döngüsünü üç araçla uygulayın (arşiv, okuyucu verileri, e-posta gönder).
   **困难。**Üç araç kullanın ((Search 、Read取用户数据、发送邮件) yukarıdaki ajan döngüsünü gerçekleştirmek için. 50 test durumunun değerlendirilmesi, girişimde bulunma önerisi, girişimde bulunma oranı, başarısızlık oranı ve herhangi bir girişimde bulunma oranı gibi.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Anahtar Şartlar .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Intent（意图） | What the user wants / 用户想要什么 | Categorical label (book_flight, reset_password). Routed to a handler. / 分类标签（book_flight、reset_password）。路由到处理器。 |
| Slot（槽位） | A piece of info / 一条信息 | Parameter the bot needs (date, destination). Slot filling is the sequence of asks. / 机器人需要的参数（日期、目的地）。槽位填充是依次询问的过程。 |
| RAG（检索增强生成） | Retrieval plus generation / 检索加生成 | Retrieve relevant docs, then ground the LLM's response. / 检索相关文档，然后锚定 LLM 的响应。 |
| Tool call（工具调用） | Function invocation / 函数调用 | LLM emits a structured call with name + args. Runtime executes, returns result. / LLM 发出带名称和参数的结构化调用。运行时执行并返回结果。 |
| Agent loop（Agent 循环） | Plan, act, verify / 规划、执行、验证 | Controller that runs LLM calls interleaved with tool calls until task complete. / 运行 LLM 调用与工具调用交错直到任务完成的控制器。 |
| Prompt injection（提示注入） | User attacks prompt / 用户攻击提示 | Malicious input that tries to override the system prompt. / 试图覆盖系统提示的恶意输入。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.

## Daha fazla okumak

- [Weizenbaum (1966). ELIZA — A Computer Program For the Study of Natural Language Communication](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf) kural tabanlı chatbot kağıdı. / 原始基于规则的聊天机器人论文──
- [Thoppilan et al. (2022). LaMDA: Language Models for Dialog Applications](https://arxiv.org/abs/2201.08239) Google'ın geç sinirsel sohbetçi makalesi, LLM ajanları devralmadan hemen önce. / Google 后期神经聊天机器人论文,就在LLM Agent 接管之前.
- [Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) ajan döngüsü örneğini belirten kağıt. / 命名 Agent 循环模式的论文。
- [Anthropic's guide on building effective agents](https://www.anthropic.com/research/building-effective-agents)2024 üretim öngörü, 2026 yılında hala geçerli. / 2024年生产指南,2026年仍然有效──
- [Greshake et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) hızlı enjeksiyon kağıdı. / 提示注入论文。
- [OWASP Top 10 for LLM Applications 2025 — LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)                                                                                                                                                                                                                                                              
- [AWS — Securing Amazon Bedrock Agents against Indirect Prompt Injections](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agents-a-guide-to-safeguarding-against-indirect-prompt-injections/)Plan-Verify-Execute ve kullanıcı-tasdiklama akışları dahil olmak üzere pratik orkestrasyon katmanlı savunmalar.
- [EchoLeak (CVE-2025-32711)](https://www.vectra.ai/topics/prompt-injection) indirek prompt enjeksiyonundan gelen kanonik sıfır tıklama veri-ekfiltrasyon CVE. Yazma erişim ajanlarının neden çalıştırma zaman savunmalarına ihtiyaç duyduğu için referans vakaları. / 间接提示注入的典型零点击数据泄露 CVE──写入权限 Agent 需要运行时防御的参考案例──
| Intent | What the user wants | Categorical label (book_flight, reset_password). Routed to a handler. |
| Slot | A piece of info | Parameter the bot needs (date, destination). Slot filling is the sequence of asks. |
| RAG | Retrieval plus generation | Retrieve relevant docs, then ground the LLM's response. |
| Tool call | Function invocation | LLM emits a structured call with name + args. Runtime executes, returns result. |
| Agent loop | Plan, act, verify | Controller that runs LLM calls interleaved with tool calls until task complete. |
| Prompt injection | User attacks prompt | Malicious input that tries to override the system prompt. |

## Daha Fazla Okumak

- [Turing (1950). Computing Machinery and Intelligence](https://academic.oup.com/mind/article/LIX/236/433/986238) Konuşmayı alanın referans noktası yapan makale.
- [Weizenbaum (1966). ELIZA — A Computer Program For the Study of Natural Language Communication](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf) orijinal kural tabanlı chatbot kağıdı.
- [Colby, Weber, Hilf (1971). Artificial Paranoia](https://doi.org/10.1016/0004-3702(71)90002-6)  PARRY'nin etkisi değişken mimarisi, ilk devletli chatbot.
- [Thoppilan et al. (2022). LaMDA: Language Models for Dialog Applications](https://arxiv.org/abs/2201.08239)Google'ın geç neural chatbot makalesi, LLM ajanları devralmadan hemen önce.
- [Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) ajan döngüsü örneğini belirleyen kağıt.
- [Anthropic's guide on building effective agents](https://www.anthropic.com/research/building-effective-agents)2024 üretim öngörü, 2026'da hala geçerli.
- [Greshake et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) hızlı enjeksiyon kağıdı.
- [OWASP Top 10 for LLM Applications 2025 — LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) hızlı enjeksiyonu en büyük güvenlik endişesi yapan sıralama.
- [AWS — Securing Amazon Bedrock Agents against Indirect Prompt Injections](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agents-a-guide-to-safeguarding-against-indirect-prompt-injections/) Plan-Verify-Execute ve kullanıcı-tasdiklama akışları dahil olmak üzere pratik orkestrasyon katman savunmaları.
- [EchoLeak (CVE-2025-32711)](https://www.vectra.ai/topics/prompt-injection) indirek hızlı enjeksiyondan gelen sıfır tıklama ile veri eksfiltrasyonu CVE. Yazma erişim ajanlarının neden çalıştırma zamanının korunmasına ihtiyaç duyduğu için referans vaka.
