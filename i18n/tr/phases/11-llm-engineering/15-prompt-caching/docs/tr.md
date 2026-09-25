# Hızlı Kayıtlama ve Kontekst Kayıtlama 提示缓存与上下文缓存

> Sistem istekiniz 4.000 simge. RAG bağlamınız 20.000 simge. Her istekle her ikisini de gönderiyorsunuz. Her seferinde ikisini de ödersiniz. Anlık önbelleği sağlayıcıya bu önbellekleri yanlarında sıcak tutmalarını ve tekrar kullanma normal oranın% 10'unu ödemelerini sağlar. Doğru kullanıldığında, sonuçlama maliyetini % 50  90% ve ilk simge gecikmesini % 40  85% azaltır.

> **【中文解读】**Sistem提示4000 token + RAG 上下文20000 token, her istek ödemek gerekir.提示缓存让供应商保留前,重用时只收取10%费――正确使用可降低50-90%推理成本和40-85%首token延迟――

> **【拓展：提示缓存→RAG生产优化】**Antropic'in Hızlı Kayıtlama ve OpenAI'nin Kayıtlı Yanıtlama, RAG üretim sisteminin maliyetleri azaltma anahtar teknolojidir, özellikle sabit sistem önerisi ve büyük miktarda aramalar vardır.

>  **【前置】**Önemli bir şekilde, bu süreçte, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir sürece, bir sürece, bir sürece, bir sürece, bir sürece, bir sürecececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 01 (Prompt Engineering), Phase 11 · 05 (Context Engineering), Phase 11 · 11 (Caching and Cost) | **前置知识:** Phase 11 · 01 (提示工程)、05 (上下文工程)、11 (缓存与成本)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Sorunlar. Sorunlar.

Bir kodlama ajanı, Claude'a her konuşmanın her dönüşünde aynı 15.000 jetonlu sistem uyarısını gönderir.$3/M input tokens is $Kullanıcının gerçek mesajlarından herhangi biri olmadan önce giriş maliyetinin sadece 0.90'u. Günde 10.000 konuşma ile çoğaltın ve hiç değişmeyen metin için fatura günde 9.000 dolara ulaşır.

> Bir programlama ajanı, her konuşma turunda aynı 15.000 token gönderir.$3/M 输入 token，仅输入成本就是 $0.90  Ayrıca kullanıcıların gerçek haberlerini içermiyor.

Bu nedenle, bu konuyla ilgili bir görüşme yaparak, bu konuyla ilgili bir görüşme yaparak, bu konuyla ilgili bir görüşme yaparak, bu konuyla ilgili bir görüşme yaparak, bu konuyla ilgili bir görüşme yaparak, bu konuyla ilgili bir görüşme yaparak, bu konuyla ilgili bir görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşmeyi gerçekleştirmek için, bu görüşme yaparak, bu görüşmeyi gerçekleştirmek için, bu görüşme yaparak, bu görüşmeyi gerçekleştirmek için, bu görüşme yaparak, bu görüşmeyi gerçekleştirmek için, bu görüşme yaparak, bu görüşmeyi gerçekleştirmek için, bu görüşme yaparak, bu görüşme yaparak, bu görüşmeyi gerçekleştirmek için, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme yaparak, bu görüşme konusunda, bu görüşme yaparak, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu

> Kaliteli bozacak şekilde küçük bir ipucu gönderemezsiniz. Her seferinde ona ihtiyaç duyulan bir model göndermekten kaçınabilirsiniz. Tek yol, tedarikçilerin önceden gördüğü tüm fiyatları ödemeyi durdurmaktır.

>  **【类比】**Hızlı önbelleğe kaydetme 像"快递公司记住你的常用地址"第一次发货要详细说明"北京市朝阳区...",之后每次发货只需说"老地方",快递公司自动调出地址──技术上:供应商把前的KV缓存 存在自己的服务器,下次请求来时直接复用,不需要重新计算注意的K/V矩阵──对用户透明你只需要在API调用加个`cache_control`- Evet.

> ️ **【易错点】**Hızlı önbelleğe yerleştirme: 1)**prefix 顺序敏感**cache 命中要求 prefix 完全相同(包括空格、换行), sistem prompt 末尾多一个空格就错过;务必把可变部分(user输入) 放最后。(2) **cache TTL 5 分钟**Antropik 默认 5 分钟过期,没流量时缓存 失效; uzattığı TTL(1 小时)保住冷启动场景──(3) **没监控命中率**                                                                                                                                                                                                                                                              `cache_creation_input_tokens`和 `cache_read_input_tokens`, kayıt kontrol panelenin için.

Bu hareket hızlı önbelleğe girmek. Anthropic onu Ağustos 2024'te (2025'te 1 saatlik uzatılmış TTL varianti ile) gönderdi, OpenAI onu o yılın sonunda otomatikleştirdi, Google, Gemini 1.5 ile birlikte açık bağlamalı önbelleğe gönderdi ve şimdi üçü de sınır modelleri üzerinde birinci sınıf bir özellik olarak sunmaktadır.

> Bu yöntem, bir öneri bekleme yöntemidir. Antropik, 2024 yılının Ağustos ayında yayınladı.


> **【中文解读】**Hızlı Kayıtlama değerleri sistem hızlı genellikle çok uzun olur ve tüm istekler arasında değişmez.


## Konsepten bir şey.

> **【中文解读】**Hızlı Kayıtlama, LLM'nin 推理的特性を利用します Eğer birden fazla istek aynı kvası paylaşırsa, bu kvası kaydetmek mümkündür 計算結果,重複計算を避ける.

> **【拓展：Prompt Caching 的成本节省】**Anthropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'in Antropic'i Antropic'in Antropic'in Antropic'in Antropic'in Antropic's Antropic's Antropic's Antropic's Antropic's Antropic's Antropic's Antropic's Antropic's Antropic's Antroptic's Antroptic's Antroptic's price will decrease.$0.50/M tokens（原价 $5)。 Sistem için 5K simgeler + ortalama 10 kez tekrar kullanılabilir sahne, aylık maliyet yaklaşık %75 oranında düşebilir。


![Prompt caching: write once, read cheap](../assets/prompt-caching.svg)

**The mechanic.**Bir istek önlüğü son bir istekle eşleşince, sağlayıcı, simgelerin yeniden kodlanması yerine önceki çalışmadan KV-cache'yi sunuyor.

> **机制。**Arayanın önüne gelen ücretin sonuncu talebe göre eşleşmesi halinde, tedarikçi, ilk kez küçük bir yazma ödemesi yerine, önceki işlemlerden KV-cache sunuyor.

**Three provider flavors in 2026.**

| Provider | API style | Hit discount | Write premium | Default TTL | Min cacheable |
|---------|-----------|--------------|---------------|-------------|---------------|
| Anthropic | Explicit `cache_control` markers on content blocks | 90% off input | 25% surcharge | 5 min (extendable to 1 hour) | 1,024 tokens (Sonnet/Opus), 2,048 (Haiku) |
| OpenAI | Automatic prefix detection | 50% off input | none | Up to 1 hour (best-effort) | 1,024 tokens |
| Google (Gemini) | Explicit `CachedContent` API | Storage-billed; read at ~25% of normal | Storage fee per token·hour | User-set (default 1 hour) | 4,096 tokens (Flash), 32,768 (Pro) |

**The invariant.**Eğer herhangi bir token istekler arasında farklılık gösterirse, ilk farklı token sonrası her şey bir hata olur.

> **不变量。**Üçcüdu sadece缓存前── Eğer istekler arasında herhangi bir simge varsa farklı, ilk farklı simge  sonra tüm içeriği belirlenmemiş ──将将*稳定*部分放在顶部,*可变*部分放在底部──

### Önbelleğe dostu düzen

```
[system prompt]          <-- cache this
[tool definitions]       <-- cache this
[few-shot examples]      <-- cache this
[retrieved documents]    <-- cache if reused, else don't
[conversation history]   <-- cache up to last turn
[current user message]   <-- never cache (different every time)
```

 Kullanıcı mesajını sistem uyarısının üstünde koyun, birkaç çekim arasında dinamik çekimleri  ve önbelleği asla vurmaz.

> 违序将用户信息放在系统提示上,在少样本之间穿插动态检查缓存永远不会命中

### Kesinlik hesaplama

Anthropic'in %25 yazma ödemesi, net para tasarrufu için en az iki kez önbelleğe alınan bir blok okunması gerektiği anlamına gelir. 1 yaz + 1 okuyucu, talep başına ortalama 0.675x maliyetini (%32 tasarruf eder); 1 yaz + 10 okuyucu ortalama 0.205x (%80 tasarruf eder).

> Antropik'in %25  yazma ödemesi, depolama bloklarının en az iki kez okunması gerektiği anlamına gelir.

## Yapın.
```figure
prompt-cache-hit
```

## Yapın

### Adım 1: Açık işaretle Antropik çağrı önbelleği

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

- Evet .`cache_control`Markör, Anthropic'e blokun 5 dakika saklanmasını söyler.

> `cache_control`标记告诉 Antropic 将该块存储 5 分钟.

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

 if                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `cache_read_input_tokens`İstekler boyunca sıfırda kalır, önbelleğin anahtarları sürüklenir.

> Bu iki bölümde bir kontrol yapın.`cache_read_input_tokens`Çok defa isteklerde sıfır tutun, kaydındaki anahtarlar hareket ediyor.

### Adım 2: Bir saatlik uzatılmış TTL

Uzun süreli seri işlerde, 5 dakikalık özür işler arasında geçerlidir.`ttl`- ...

```python
{"type": "text", "text": RUBRIC, "cache_control": {"type": "ephemeral", "ttl": "1h"}}
```

1 saatlik TTL yazma priminin iki katı (50% yerine 25%) maliyetini artırır, ancak önbellekten 5'den fazla kez tekrar kullanılan her parti için hızlı bir şekilde ödenir.

> 1 saat TTL'nin yazma ödemesi %25 değil %50'dir, ancak her türlü yeniden kullanımı öncesinde 5 kez daha fazla toplama işleminde çok hızlı bir şekilde geri dönüştürülmektedir.

### Adım 3: OpenAI otomatik önbelleği

OpenAI size yapılandırmak için hiçbir şey vermez. 1.024 tokenden fazla bir önbölüm son bir talebe eşleşir otomatik olarak %50 indirim alır.

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

Aynı önbelleğe dostu düzen kuralı geçerlidir. OpenAI'nin önbelleğini öldüren iki şey Anthropic'i öldürmeyen:`user`alan (cache anahtar bileşen olarak kullanılır) ve yeniden düzenleme araçları.

> Aynı şekilde, bu iki şey OpenAI'nin bu şekilde kalmasını öldürür, fakat Anthropic'i öldürmez.`user`字段和重新排序工具──

### Adım 4: Gemini açık bağlamı önbelleği

Gemini , önbelleği oluşturup adlandırdığınız birinci sınıf bir nesne olarak değerlendirir:

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

Gemini, önbelleğin ömrü boyunca her token·saati depolama ücretini alır ve normal giriş oranının %25'inde okur.

> Gemini 按缓存存活期间每代币·小时收取存储费,读取费率约为正常输入的25%──当你在多次会话中跨天重复使用相同的大型提示时,这是正确的选择──

### Adım 5: Üretimdeki vurma oranını ölçmek

Bakın .`code/main.py`1K talepleri başına yazma/okuma/kayıp sayıları izleyen ve karışık maliyet hesaplayan simülasyonlu üç sağlayıcı muhasebeci için.

> Görüyorum .`code/main.py`获取模拟的三供应商会计师,跟踪写入/读取/未命中计数并计算每千请求的混合成本──按目标命中率门控部署多数生产 预热后应见在预热设置在预热应见 >80% 读取比例──

## 2026'da hala yolculuk eden tuzaklar

> 2026 yılında hâlâ bir tuzak var:

- **Dynamic timestamps at the top.** `"Current time: 2026-04-22 15:30:02"`Sistem isteklerinin üst kısmında, her istek kayıp olur.
  **顶部的动态时间戳。**Sistem提示顶部放 `"Current time: 2026-04-22 15:30:02"`                                                                                                                                                                                                                                                              
- **Tool reordering.**Düzenli bir sırada araçları seriye etmek  bir devre yeniden düzenlemesi her vurguyu bozar.
  **工具重排序。**Bu, bir dizi aşama şeklinde bir dizi aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şeklinde bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama şekle bir aşama aşama şekle bir aşama şekle bir aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aş
- **Free-text near-duplicates.**"Yardımcısın". vs "Yardımcı bir asistansın".  bir bayt fark = tam eksiklik.
  **自由文本近似重复。**"Yardımcısın" vs "Yardımcı bir asistansın".
- **Too-small blocks.**Anthropic 1.024 token zemini (2.048 Haiku için) zorlar.
  **过小的块。**Antropik 强制 1,024 token 下限(Haiku 为 2,048)。更小的块静默不缓存。
- **Blind cost dashboards.**"Geliş tokensini" önbelleğe alınan ve önbelleğe alınmayan bölün. Yoksa trafik düşüşü önbelleğe alınan kazanç gibi görünür.
  **盲目的成本仪表板。**Bu "输入 token" ı kassa karşı kassa olarak ayırmak.

## Çerçeveyi kullanın.

2026'da önbelleğe alınan:

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

Kullanıcı mesaj katmanı için semantik önbelleğe (Fase 11 · 11) birleştirin: prompt önbelleğe *token-identical* reuse, semantic caching handles *meaning-identical* reuse.

> %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s

## İndirin . Ürünler .

- Kaydet .`outputs/skill-prompt-caching-planner.md`- ...

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

## Egzersizler.

1. **Easy.**Claude'a karşı 5000 tokenli bir sistemle 10 dönüş konuşma yapın.`cache_control`Her biri için giriş belirti faktürünü rapor edin.
   10 dakikalık bir konuşma ve 5.000 tane işaret alın.`cache_control`Bölüm: Kısıtlama, rapor:
2. **Medium.**Bir istek şablonu ve bir talep günlüğü verildiğinde, bir sağlayıcıya göre beklenen hit oranını ve dolar tasarrufini hesaplayan bir test harnesini yaz (Anthropic 5m, Anthropic 1h, OpenAI otomatik, Gemini açık).
    test araçları, öneriler formu ve istek günlüğü, hesaplama ve tasarruf oranı
3. **Hard.**Bir düzenleme optimizörü oluştur: bir istek ve işaretli alanların bir listesini göster `stable=True/False`, bir tek önbelleği kırılma noktasını gerçek bir Anthropic son noktasında doğrulayın.
   构建布局优化器:重写提示将缓存断点放在最大缓存友好位置――

## Anahtar Şartlar .

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

## Daha fazla okumak

- [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) `cache_control`1 saat TTL, düzlem masaları.
  Antropik 提示缓存文档cache_control、1 小时 TTL、亏平衡表──
- [OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) otomatik ön işaret eşleşimi.
  OpenAI 提示缓存文档自动前匹配──
- [Google — Context caching](https://ai.google.dev/gemini-api/docs/caching) `CachedContent`API ve depolama fiyatları.
  Google 上下文缓存文档CachedContent API 和存储定价──
- [Anthropic engineering — Prompt caching for long-context workloads](https://www.anthropic.com/news/prompt-caching) gecikme numaraları ile orijinal başlatma noktası.
  Antropik 工程博客长上下文工作负载的提示缓存,含延迟数据──
- 11 · 05 aşaması (Kontext Mühendisliği)  Kaynak yerleşebilsin diye istekleneni kesmek için nerede.
  Bölüm 11 阶段 · 05 上下文工程) 在哪里切分提示以便缓存生效──
- Fase 11 · 11 (Kesleme ve Maliyet)  kullanıcı mesajlarında semantik bir önbelleğe sahip bir önbelleğe sahip bir çift önbelleğe girme.
  Bölüm 11. Aşama · 11(Kazanlık ve maliyet) 
- [Pope et al., "Efficiently Scaling Transformer Inference" (2022)](https://arxiv.org/abs/2211.05102) KV-cache bellek modeli, önbelleği kullanan kullanıcılara açığa çıkarır; önbelleği önbelleğin yeniden okumak için yeniden hesaplamaktan ~ 10x daha ucuz olduğunu açıklar.
  解释为什么缓存前比重算便宜约10倍的KV-cache内存模型论文──
- [Agrawal et al., "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills" (2023)](https://arxiv.org/abs/2308.16369) prefill, faz prompt önbelleğe geçirme kısayollarıdır; bu makale TTFT'nin neden TPOT'nin etkilenmediği sürece önbelleğe geçirilmesinde önemli ölçüde düştüğünü açıklar.
  解释为什么缓存命中时 TTFT 大幅下降而 TPOT不受影响的论文──
- [Leviathan et al., "Fast Inference from Transformers via Speculative Decoding" (2023)](https://arxiv.org/abs/2211.17192) hızlı önbelleğe kaydedilme spekülatör çözme, Flash Dikkat ve MQA/GQA ile birlikte sonuç maliyet eğriğini eğdiren kaldıraçlar olarak yer alır; diğer üç için bunu okuyun.
  提示缓存与投机解码、Flash Attention 和 MQA/GQA 并列的推理成本曲线杆──
