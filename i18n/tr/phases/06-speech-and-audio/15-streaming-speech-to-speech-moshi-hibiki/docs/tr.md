# Konuşma-Söz Akışları  Moshi, Hibiki ve Tam Dubleks Diyaloğu  流式语音到语音  Moshi、Hibiki 与全双工对话

> 2024-2026 ses AI'yi yeniden tanımladı. Moshi, 200 ms gecikme ile aynı anda dinleyen ve konuşan tek bir model gönderir. Hibiki konuşma-söz çevirisini parça parça yapar. Her ikisi de ASR → LLM → TTS borusunu Mimi kodek jetonları üzerinde tek bir tam çiftlik mimarisi için terk eder. Bu yeni referans tasarımıdır.

> **【中文解读】**2024-2026 yıllarında sesleri yeniden tanımladı AI。Moshi 200ms 延迟内同时听和说。Hibiki 逐块进行语音到语音翻译。 ikisi de ASR→LLM→TTS 流水线'i terk etti, Mimi 编解码器 token'a dayalı bir bütünüyle iki yapılandırmayı benimsedi。 bu yeni bir referans tasarımı。

> **【拓展：全双工语音 AI】**傳統语音助手是"半双工" (gelirken söyleyemez),Moshi 实现了"全双工" (gelirken dinleyip konuşur),就像人类自然对话一样──这是2026年语音 AI 最前沿的方向──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 13 (Neural Audio Codecs), Phase 6 · 11 (Real-Time Audio), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 13（神经音频编解码器），阶段 6 · 11（实时音频），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Sorunlar. Sorunlar.

Ders 11 + 12'den oluşturulan her ses ajansı, temel bir gecikme zemine sahip: 300-500 ms civarında: VAD yangınları, STT süreçleri, LLM nedenleri, TTS üretir. Her aşamada kendi minimum gecikme var. Düzenleyebilir ve paralelleştirebilirsiniz, ancak boru hattı şekli sizi kapsar.

> 11 ve 12 derslere dayanan her ses yardımcısı yaklaşık 300-500 ms'lik bir temel gecikme sınırına sahiptir: VAD 触发、STT 处理、LLM 推理、TTS 生成── her aşamada kendi en az gecikme vardır── düzenleyip eşleştirmek mümkündür, ancak akım hattı yapı kendisini sınırlıyor──

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.


Moshi (Kyutai, 2024-2026) farklı bir soru sorar: bir boru hattı yoksa ne olacak?

> Moshi ((Kyutai,2024-2026) farklı bir soru ortaya koydu: Eğer su akışı yoksa? Eğer bir model doğrudan 持续接收音频输入并输出音频,文本只是中间的内心独白而非必要阶段?

Cevap şu:**full-duplex speech-to-speech**- Teorik gecikme 160 ms (80 ms Mimi çerçeve + 80 ms akustik gecikme) - tek L4 GPU'da pratik gecikme 200 ms.

> Cevap şu:**全双工语音到语音**△ teorik geçicilik 160 ms(80 ms Mimi  + 80 ms 声学延迟) ・・・ 在单张 L4 GPU 上实际延迟 200 ms──这是最好的流水线语音助手延迟的一半──

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Moshi architecture: two parallel Mimi streams + inner-monologue text](../assets/moshi-hibiki.svg)

### Moshi mimarisi

> Moshi 架构

**Inputs.**İki Mimi kodek akışı, her ikisi de 12.5 Hz × 8 kod defterinde:

> **输入。**两个 Mimi 编解码器流, ortalama 12.5 Hz × 8 个码本:

- Akış 1: Kullanıcı ses (Mimi-kodlanmış, sürekli gelen)
  Çinçe Çevirim:流 1: user音频(Mimi 编码,持续到达)
- Stream 2: Moshi'nin kendi sesini (Moshi tarafından üretilmiş)
  Çinçe Çevirim:流 2:Moshi 自身的音频(由 Moshi 生成)

**The transformer.**7B parametri olan Zaman Transformer hem akışları hem de bir metin "içi monolog" akışını işliyor.

> **Transformer。**Bir 70 milyar parameterlik zamanlı transformatör aynı zamanda iki akış ve bir metin "内心独白" akışını işliyor.

1. En son kullanıcı Mimi tokenlerini tüketir (8 kod defteri).
   Çin Çeviri: 消费最新的用户 Mimi token
2. En son Moshi Mimi tokenlerini tüketir (8 kod kitabı, üretildiği gibi).
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Çeviri: Ç Ç Ç Ç Ç Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
3. Bir sonraki Moshi metin belirti (iç monolog) oluşturur.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Çeviri: Çeviri: Ç Ç Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
4. Bir sonraki Moshi Mimi jetonlarını yaratabilir (8 küçük derinlik transformörü aracılığıyla kod defteri).
   ÇXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Üç akış  kullanıcı ses, Moshi ses, Moshi metni  paralel olarak çalışır. Moshi konuşurken kullanıcıyı duyabilir; kullanıcı kesildiğinde kendini kesebilir; ana ifadesini kırmadan arka kanal ("mhm") yapabilir.

> Üç 流 user音频、Moshi 音频、Moshi 文本并行运行──Moshi konuşurken kullanıcıyı duyabilir; kullanıcı kesildiğinde kendini kesebilir; başlıca konuşmayı bozmadan karşıya gelebilir.

**The depth transformer.**Bir çerçeve içinde, 8 kod kitabı paralel olarak tahmin edilmez.  kod kitapları arasında bağımlılıklara sahiptirler. Küçük bir iki katmanlı " derinlik transformatörü " onları 80 ms içinde sırayla tahmin eder. Bu AR kodek LM için standart faktörleşme (VALL-E, VibeVoice tarafından da kullanılır).

> **深度 Transformer。**Bir 内,8 码本不是并行预测的它们之间存在码本间依赖. Bir 2 katlı küçük "Deepness Transformer" 内 80 ms içinde sırayla onları öngörüyor. Bu kendi kendine kodlayıcı kodlayıcı dil modelinin standart 因子化 üyesi (VALL-E、VibeVoice da kullanılır) 

### İçerideki tek kelime neden yardımcı olur?

Açık bir metin olmadan, model, akustik akışında dil modeli indirekt olarak oluşturmalıdır. Moshi'nin anlayışı: sesle birlikte metin işaretlerini yaymak için zorlamak. Metin akışı esasen Moshi'nin söylediği şeyin transkriptidir. Bu semantik tutarlılığı artırır, dil model başlığını değiştirmeyi kolaylaştırır ve size transkriptleri ücretsiz verir.

> Neden içi tek kelime metni yardımcıdır: açık metni yoktur, model ses akımında gizli bir yapıtaş dili olmalıdır.

### Hibiki: Konuşma-söz çevirisini akışı

Aynı mimarlık, çeviri çiftlerinde eğitilmiştir. Kaynak ses, hedef dili ses çıkışı, sürekli. Hibiki-Zero (Feb 2026) sözcük düzeyde uyumlu eğitim verilerinin gerekliliğini ortadan kaldırır.

> Hibiki:流式语音到语音翻译──相同的架构,使用翻译对训练──源语言音频输入,目标语言音频输出,持续进行──Hibiki-Zero(2026年 2月)

İlk olarak dört dil çiftine destek verilir; ≈1000 saat ile yeni bir dile uyarlanabilir.

> İlk olarak dört dil destekleme; yaklaşık 1000 saatlik veri yeni dillere göre uygulanabilir.

### Daha geniş Kyutai yığın (2026)

> Daha geniş Kyutai 技术(2026 yıl)

- **Moshi** Tam ikili diyalog (İngilizce iyi desteklenmiş önce Fransızca)
  Çeviri:Moshi  全双工对话 (Fransız öncelikli,英语支持良好)
- **Hibiki / Hibiki-Zero** Aynı anda konuşma çevirisi
  Çeviri:Hibiki / Hibiki-Zero  同步语音翻译
- **Kyutai STT** Akış ASR (500 ms veya 2.5 saniye önümüze bakmak)
  中文翻译:Kyutai STT  流式语音识别(500 ms veya 2.5 s 前视)
- **Kyutai Pocket TTS** 100M-param TTS CPU ile çalışır (Jan 2026)
  中文翻译:Kyutai Pocket TTS  1 亿参数 TTS,可在 CPU 上运行(2026年 1月)
- **Unmute** Bu sistemleri kamu sunucularında birleştiren tam bir boru hattı
  Çinçe Çevirimi:Unmute 

L40S GPU'da geçiş gücü: 64 eşzamanlı oturum 3× gerçek zamanlı.

> L40S GPU'da toplama gücü: 64 个并发会话,3 倍实时速度──

### Sesam CSM  kuzen

Sesame CSM (2025) aynı fikirde kullanıyor. Llama-3 omurgası ve Mimi kodek başı. Ancak CSM tam dupleks yerine tek yönlüdür (teks + metin alır, konuşma üretir). Piyasadaki en iyi "sessiz varlık" TTS'dir; Moshi'nin tam dupleks yeteneğiyle aynı değil.

> Sesame CSM(2025) benzer bir fikir kullanmıştır Llama-3 骨干网络 + Mimi 编解码器头── ancak CSM tek yönlüdür 接收上下文 +文本,生成语音),而非全双工──它是市场上最好的"语音存在感" TTS;但与莫希的全双工能力不完全相同──

### 2026 performans sayıları

| Model | Latency | Use case | License |
|-------|---------|----------|---------|
| Moshi | 200 ms (L4) | full-duplex English / French dialogue / 全双工英/法对话 | CC-BY 4.0 |
| Hibiki | 12.5 Hz framerate | French ↔ English streaming translation / 法↔英流式翻译 | CC-BY 4.0 |
| Hibiki-Zero | same | 5 language-pairs, no aligned data / 5 语言对，无需对齐数据 | CC-BY 4.0 |
| Sesame CSM-1B | 200 ms TTFA | context-conditioned TTS / 上下文条件 TTS | Apache-2.0 |
| GPT-4o Realtime | ~300 ms | closed, OpenAI API / 闭源，OpenAI API | commercial |
| Gemini 2.5 Live | ~350 ms | closed, Google API / 闭源，Google API | commercial |

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.




## Yapın.
```figure
sp-fullduplex
```

## Yapın

### Adım 1: Ara yüzü

> Adım 1: Bağlantı

Moshi, 80 ms'lik Mimi kodlanmış ses parçalarını alan ve her iki yönde de 80 ms'lık Mimi kodlanmış ses parçalarını geri veren bir WebSocket sunucusu ortaya çıkarıyor.

> Moshi 暴露一个WebSocket 服务器,接收80 ms的Mimi 编码音频块并返回80 ms的Mimi 编码音频块──双向,持续进行──

```python
import asyncio
import websockets
from moshi.client_utils import encode_audio_mimi, decode_audio_mimi

async def moshi_chat():
    async with websockets.connect("ws://localhost:8998/api/chat") as ws:
        mic_task = asyncio.create_task(stream_mic_to(ws))
        spk_task = asyncio.create_task(stream_from_to_speaker(ws))
        await asyncio.gather(mic_task, spk_task)
```

### Adım 2: Tam duplex döngüsü

> 2 adım: Tüm iş döngüsü

```python
async def stream_mic_to(ws):
    async for chunk_80ms in mic_stream_at_12_5_hz():
        mimi_tokens = encode_audio_mimi(chunk_80ms)
        await ws.send(serialize(mimi_tokens))

async def stream_from_to_speaker(ws):
    async for msg in ws:
        mimi_tokens, text_token = deserialize(msg)
        audio = decode_audio_mimi(mimi_tokens)
        await play(audio)
```

Python asyncio veya Rust geleceği standart taşımacılıktır.

> 双方向同时运行──Python asyncio 或 Rust futures 标准的传输方式──

### Adım 3: Eğitim amacı (konseptik)

> 步骤 3: training目标 (öğrenme amacı)

Her 80 ms çerçeve için `t`- ...

> 对于每80 ms 的`t`- ...

- Giriş: `user_mimi[0..t]`- Evet .`moshi_mimi[0..t-1]`- Evet .`moshi_text[0..t-1]`
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`user_mimi[0..t]`- Evet.`moshi_mimi[0..t-1]`- Evet.`moshi_text[0..t-1]`
- Önceden:`moshi_text[t]`O zaman ...`moshi_mimi[t, codebook_0..7]`
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`moshi_text[t]`Sonra da `moshi_mimi[t, codebook_0..7]`

Metin sesden önce (içer monolog) öngörülür; ses derinlik transformatöründe kod defteri-sükvensel olarak öngörülür.

> 文本在音频之前预测(内心独白);音频在深度 Transformer 内按码本顺序预测。

### Dördüncü adım: Moshi'nin nerede kazanacağı ve nerede kazanacağı.

> 步骤 4:Moshi'nin avantajları ve eksiklikleri

Moshi kazanır:

> Moshi'nin avantajları:

- Alt 250 ms ucuza ucuza malzemeler.
  Çinçe Çevirisi: 250 ms'den az olan ucuza malzemeler.
- Doğal arka kanallar ve kesintiler.
  Çinçe Çevirim: Doğalın karşılığı ve kırma yeteneği
- - Pipeline yapışkan kodları yok.
  Çinçe Çevirim:无需流水线水代码──

Moshi kazanmıyor:

> Moshi'nin eksikliği:

- Araç çağrısı (bunu yaptırmadınız; ayrı bir LLM yoluna ihtiyacınız var).
  Çinçe Çevirimiçi:工具调用 (未针对此训练;需要单独的 LLM 路径)
- Uzun bir mantık (Moshi, Claude/GPT-4 değil, 8B diyalog modeli).
  Çinçe Çevirimiçi:长链推理 ((Moshi, Claude/GPT-4) değil, yaklaşık 80 milyar 参数 的对话模型,
- Niş konularındaki gerçek doğruluk.
  Çinçe Çevirisi: 小众话题的事实准确性
- Çoğu üretim işletmesi kullanım durumları (2026 yılında hala boru hattları kullanılıyor).
  Çin dilinde: çoğu üretim sınıfı işletme sahnesinde (→ 2026 yıl hâlâ kullanılıyor)

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.





> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

| Situation | Pick |
|-----------|------|
| Lowest-latency voice companion / 最低延迟语音伴侣 | Moshi |
| Live translation call / 实时翻译通话 | Hibiki |
| Voice demo / research / 语音演示/研究 | Moshi, CSM |
| Enterprise agent with tools / 企业级带工具的 agent | Pipeline（第 12 课），不是 Moshi |
| Custom-voice TTS in context / 上下文中的自定义音色 TTS | Sesame CSM |
| Speech-to-speech, any languages / 任意语言的语音到语音 | GPT-4o Realtime 或 Gemini 2.5 Live（商业） |



## Tuzaklar

> 常见陷

- **Limited tool calling.**Moshi bir iletişim modeli, bir ajan çerçevesidir.
  Çeviri:**有限的工具调用。**Moshi, bir iletişim modeli, bir ajan değil 框架── needs with flowwater line 结合实现工具调用──
- **Specific-voice conditioning.**Moshi tek bir eğitimli kişilik kullanır; klonlama ayrı bir eğitim koşusudur.
  Çeviri:**特定语音调节。**Moshi tek bir eğitim insanlığı kullanır; Klon tek bir eğitim sürecine ihtiyaç duyar.
- **Language coverage.**Fransızca + İngilizce mükemmel, diğerleri sınırlıdır. Hibiki-Zero yardımcı olur, ancak hala eğitim verilerine ihtiyacınız var.
  Çeviri:**语言覆盖。**Fransızca + İngilizce performans iyi; diğer diller sınırlı。 Hibiki-Zero yardımcı, ama hala eğitim gerektirir。
- **Resource cost.**Tam bir Moshi oturumunda GPU boşluğu bulunur; ucuz paylaşılan kiracı dağıtım modeli değil.
  Çeviri:**资源成本。**Bir tam bir Moshi toplantısı bir GPU 插槽 ile yapılır; ucuz bir paylaşım kiracılık dağıtım modeli değildir.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-duplex-pipeline.md`Sesli ajan iş yükü için pipeline vs. full-duplex mimarisi seçin.

> 保存为 `outputs/skill-duplex-pipeline.md`❖ Bir dil asistanı için ❖

## Egzersizler.

1. **Easy.**Çık .`code/main.py`İki akımlı + iç monolog mimarisini sembolik olarak simüle eder.
   Çeviri:**简单。**运行  İşlem`code/main.py`                                                                                                                                                                                                                                                              
2. **Medium.**HuggingFace'den Moshi'yi çek, sunucu çalıştır, bir konuşmayı test et, kullanıcı konuşmasından Moshi tepkisine kadar duvar saati gecikmesini ölç.
   Çeviri:**中等。**HuggingFace 拉取 Moshi,运行服务器,测试一段对话──测量 从用户语音结束到 Moshi 回复开始的实际延迟──
3. **Hard.**Ders 12 boru hattı ajanını al ve 20 eşleşen test açıklaması ile P50 gecikme oranını Moshi ile karşılaştır.
   Çeviri:**困难。**12. sınıfın su akışı asistanı ile Moshi 20 条匹配测试语句上比较 P50 延迟。 bir rapor yazın.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Full-duplex | Hear-and-speak at once | Two audio streams active simultaneously on the same model. / 同一模型同时维护两条音频流 |
| Inner monologue | Model's text stream | Moshi emits text tokens alongside its audio output. / Moshi 在音频输出同时输出文本 token |
| Depth transformer | Inter-codebook predictor | Small transformer that predicts 8 codebooks within one 80 ms frame. / 在一个 80 ms 帧内预测 8 个码本的小型 Transformer |
| Mimi | Kyutai's codec | 12.5 Hz × 8 codebooks; semantic+acoustic; powers Moshi. / 12.5 Hz × 8 码本；语义+声学；驱动 Moshi |
| Streaming S2S | Audio → audio live | Chunk-by-chunk translation/dialogue, no pipeline stages. / 逐块翻译/对话，无流水线阶段 |
| Back-channeling | "Mhm" reactions | Moshi can emit small acknowledgments without breaking its turn. / Moshi 可发出小反馈而不打断自己的轮次 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Défossez et al. (2024). Moshi — speech-text foundation model](https://arxiv.org/html/2410.00037v2)- Gazete.
  Defossez 等(2024). Moshi语音-文本基础模型原始论文──
- [Kyutai Labs (2026). Hibiki-Zero](https://arxiv.org/abs/2602.12345) Düzleştirilmiş veriler olmadan akışlı çeviri.
  Hibiki-Zero 无需对齐数据的流式翻译──
- [Sesame (2025). Crossing the uncanny valley of voice](https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice) CSM spesifikasyonu.
  Sesame (şehir) 跨越语音的恐怖谷 (selam) 规范 (söz) 规范 (söz) 规范 (söz) 规范 (söz) 规范 (söz) 规范 (söz) 规范)
- [Kyutai — Moshi repo](https://github.com/kyutai-labs/moshi) yükle + sunucu.
  KyutaiMoshi  depo安装 + 服务器。
- [OpenAI — Realtime API](https://platform.openai.com/docs/guides/realtime) kapalı ticari eş.
  Açık AI Realtime API Kapat kaynaklı iş dünyası 
- [Kyutai — Delayed Streams Modeling](https://github.com/kyutai-labs/delayed-streams-modeling) Kapus altındaki STT/TTS çerçevesini.
  KyutaiDelayed Streams Modeling底层 STT/TTS 框架──

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

