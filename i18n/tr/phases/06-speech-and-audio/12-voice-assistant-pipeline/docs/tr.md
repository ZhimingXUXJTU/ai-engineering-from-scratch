# Ses Asistanı Pipeline'i inşa edin. 6. aşama Kapstone.

> 01-11 derslerinden her şey bir arada dikilir. Dinleyen, akıl yürüten ve konuşan bir ses asistanı oluşturun. 2026'da bu bir çözümlü mühendislik sorunu, bir araştırma sorunu değil  ama entegrasyon detayları, gemiyi göndermeye karar verir.

> **【中文解读】**01-11  derslerin tüm içeriğini bir araya getirerek, bir işitme, düşünme, konuşma ve konuşma gücü olan bir dil yardımcıyı oluşturun. 2026 yılı, bu bir çözümlü bir inşaat sorunu değil, araştırma sorunu.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 05, 06, 07, 11; Phase 11 · 09 (Function Calling); Phase 14 · 01 (Agent Loop) | **前置知识:** 阶段 6 · 04、05、06、07、11；阶段 11 · 09（函数调用）；阶段 14 · 01（智能体循环）
**Time:** ~120 minutes | **预计用时:** ~120 分钟

## Sorunlar. Sorunlar.

Sonundan sonuna kadar bir asistan oluştur:

> 构建一个端到端助手:

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

1. Mikrofon girişini (16 kHz mono) yakalar.
   捕获麦克风输入(16 kHz 单声道)
2. Kullanıcı konuşmasının başlangıcı ve sonu tespit edilir.
   检测用户语音的开始/结束──
3. Akışını kaydeder.
   流式转录──
4. Bir LLM'ye transkripti geçiyor ve araçları çağırabilir (zamanlama, hava, takvim).
   Bu bilgiyi, programın en iyi şekilde kullanılabileceği bir araç olarak kullanabilirsiniz.
5. TTS'e LLM metnini yayınlıyor.
   LLM'yi TTS'e aktarmak için
6. Kullanıcıya ses çalıyor.
   Kullanıcıya yayımla ses sesleri:
7. Kullanıcı cevap ortalarında keserse durur.
   Eğer kullanıcı yanıtda kesilse durdurulur.

Gecikme hedefi: kullanıcı, konuşmasını dizüstü bilgisayar CPU'nda bitirdiği 800 ms içinde ilk TTS ses baytı. Kalite hedefi: kayıp kelimeler, sessizliğe halüsinasyonlu altyazılar, ses klonlama sızdırısı, hızlı enjeksiyon başarısı yok.

> 延迟目标:在笔记本 CPU 上用户说完话后 800 ms 内发出第一个 TTS 音频字节──质量目标:不漏词、静音不产生幻觉字幕、无声音克隆泄漏、提示注入不成功──

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Voice assistant pipeline: mic → VAD → STT → LLM+tools → TTS → speaker](../assets/voice-assistant.svg)

### Yedi bileşen

1. **Audio capture.**Mikrofon → 16 kHz mono → 20 ms parçalar.`sounddevice`Python veya yerel AudioUnit/ALSA/WASAPI'de üretimde.
   **音频捕获。**麦克风 → 16 kHz 单声道 → 20 ms 块──Python 中通常使用 `sounddevice`,生产环境用原生 AudioUnit/ALSA/WASAPI¬
2. **VAD (Lesson 11).**Silero VAD @ eşiği 0,5, min konuşma 250 ms, sessizlik 500 ms.
   **VAD（第 11 课）。**Silero VAD @ 值 0.5, minimum语音 250 ms,静音持续 500 ms──信号"开始"和"结束"──
3. **Streaming STT (Lesson 4-5).**Sıfırlayış, Parakeet-TDT veya Deepgram Nova-3 (API).
   **流式 STT（第 4-5 课）。**Şapış-akıştıran, Parakeet-TDT veya Deepgram Nova-3
4. **LLM with tool calling.**GPT-4o / Claude 3.5 / Gemini 2.5 Flash. Aletler için JSON şeması. Akış tokens.
   **带工具调用的 LLM。**GPT-4o / Claude 3.5 / Gemini 2.5 Flash──工具的 JSON schema──流式代號──
5. **Streaming TTS (Lesson 7).**Kokoro-82M (en hızlı açılış) veya Cartesia Sonic (ticari).
   **流式 TTS（第 7 课）。**Kokoro-82M (TTS) veya Cartesia Sonic (TTS)
6. **Playback.**Konuşmacı çıkıyor, düşük bant genişliği ağları için opus kodlama.
   **回放。**扬声器输出;低带宽网络用 opus 编码──
7. **Interruption handler.**Eğer TTS oynatma sırasında VAD ateş ederse, oynatmayı durdur, LLM'yi iptal et, STT'yi yeniden başlat.
   **打断处理器。**Eğer TTS 播放期间 VAD 触发, stop播放、取消 LLM、重启 STT──

### Başarısızlık modunun üçünü bulacaksınız.

> ### Başarısızlıkların üç türüyle karşılaşacaksın.

1. **First-word clip.**VAD çok geç bir şekilde başlıyor. Kullanıcının "hey"si eksik.
   **首词截断。**VAD 启动晚一拍;;用户的""丢失;; 0.3 yerine 0.5 开始值
2. **Mid-response interrupt confusion.**LLM kullanıcı kesildikten sonra üretmeye devam eder; asistan kullanıcı üzerinde konuşur.
   **回应中打断混乱。**Kullanıcı                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
3. **Silence hallucination.**Sessiz ısıtma çerçevelerinde "seyrettiğiniz için teşekkürler" sessiz fısıldama çıkışı.
   **静音幻觉。**Şöyle sesleniyor: "Sözüm için teşekkürler".

### 2026 üretim referans yığınları

| Stack | Latency | License | Notes |
|-------|---------|---------|-------|
| LiveKit + Deepgram + GPT-4o + Cartesia | 350-500 ms | commercial API | Industry default 2026 |
| Pipecat + Whisper-streaming + GPT-4o + Kokoro | 500-800 ms | mostly open | DIY-friendly |
| Moshi (full-duplex) | 200-300 ms | CC-BY 4.0 | Single-model; different architecture, lesson 15 |
| Vapi / Retell (managed) | 300-500 ms | commercial | Fastest to launch; limited customization |
| Whisper.cpp + llama.cpp + Kokoro-ONNX | offline | open | Privacy / edge |

| 技术栈 | 延迟 | 许可 | 备注 |
|--------|------|------|------|
| LiveKit + Deepgram + GPT-4o + Cartesia | 350-500 ms | 商业 API | 2026 行业默认 |
| Pipecat + Whisper-streaming + GPT-4o + Kokoro | 500-800 ms | 多数开源 | DIY 友好 |
| Moshi（全双工） | 200-300 ms | CC-BY 4.0 | 单模型；不同架构，第 15 课 |
| Vapi / Retell（托管） | 300-500 ms | 商业 | 最快上线；定制有限 |
| Whisper.cpp + llama.cpp + Kokoro-ONNX | 离线 | 开源 | 隐私/边缘 |

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.

> **【拓展：语音隐私与安全】**语音数据 contains a lot of personal privacy information (Sözleşme 对话 内容) ◦深度伪造 (Depfake) 语音技术 (Sözleşme 信息) 语音 数据 语音 数据 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语





## Yapın.
```figure
v4-voice-latency
```

## Yapın

### Adım 1: Mikrofon yakalama (pseudokod)

```python
import sounddevice as sd

def mic_stream(chunk_ms=20, sr=16000):
    q = queue.Queue()
    def cb(indata, frames, time, status):
        q.put(indata.copy().flatten())
    with sd.InputStream(channels=1, samplerate=sr, blocksize=int(sr * chunk_ms/1000), callback=cb):
        while True:
            yield q.get()
```

### Adım 2: VAD kapalı dönüş yakalama

```python
def capture_turn(stream, vad, pre_roll_ms=300, silence_ms=500):
    buf, pre, triggered = [], collections.deque(maxlen=pre_roll_ms // 20), False
    silent = 0
    for chunk in stream:
        pre.append(chunk)
        if vad(chunk):
            if not triggered:
                buf = list(pre)
                triggered = True
            buf.append(chunk)
            silent = 0
        elif triggered:
            silent += 20
            buf.append(chunk)
            if silent >= silence_ms:
                return b"".join(buf)
```

### Adım 3: STT → LLM → TTS akışı

```python
async def turn(audio_bytes):
    transcript = await stt.transcribe(audio_bytes)
    async for token in llm.stream(transcript):
        async for audio in tts.stream(token):
            await speaker.play(audio)
```

### Adım 4: LLM döngüsünün içinde araç çağrısı

```python
tools = [
    {"name": "get_weather", "parameters": {"location": "string"}},
    {"name": "set_timer", "parameters": {"seconds": "int"}},
]

async for chunk in llm.stream(user_text, tools=tools):
    if chunk.type == "tool_call":
        result = dispatch(chunk.name, chunk.args)
        continue_streaming(result)
    if chunk.type == "text":
        await tts.stream(chunk.text)
```

### Adım 5: Kesinlik işlemleri

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


```python
tts_task = asyncio.create_task(tts_loop())
while True:
    chunk = await mic.get()
    if vad(chunk):
        tts_task.cancel()
        await speaker.stop()
        await new_turn()
        break
```




> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

Bakın .`code/main.py`Bu, tüm yedi bileşenini birer parça ile bağlayan çalıştırılabilir bir simülasyon için, böylece donanım olmadan bile boru hattı şeklini görebilirsiniz. Gerçek bir uygulamak için, birer parça ile değiştirin:

> 参见 `code/main.py`获取可运行的模拟,将七组件用模块连接,无需硬件即可见流水线形――实际实现时,将模块替换为:

- `silero-vad`(`pip install silero-vad`) / VAD 模块
- `deepgram-sdk`veya `openai-whisper`/ 流式 STT
- `openai`(`gpt-4o`) veya `anthropic`/ LLM + 工具调用
- `kokoro`veya `cartesia`/ 流式 TTS
- `sounddevice`I/O / 音频输入输出 için



## Tuzaklar

> 常见陷

- **Logging PII forever.**Tam dönüşlü ses çoğu yargı bölgesinde kişisel bilgi olarak kullanılır. 30 gün boyunca, dinlenmeden şifreli tutulmaktadır.
  **永久记录 PII。**完整轮次音频在多数司法管辖区属于PII──30 天保留,静态加密──
- **No barge-in.**Kullanıcılar kesiler.
  **没有抢话。**Kullanıcı kesilmek zorunda.
- **TTS that blocks.**Sinkron TTS olay döngüsünü engeller. Async veya ayrı bir ip kullanın.
  **阻塞式 TTS。**Aynı zamanda TTS 阻塞事件循环──异步或独立线程──
- **No tool-call error handling.**Araçlar başarısız. LLM hatayı geri almak + bir kez tekrar denemek, sonra zarif bir şekilde düşürmek gerekir.
  **没有工具调用错误处理。**工具会失败──LLM 必须收到错误 + 重试一次,然后优雅降级──
- **Overzealous hallucination filters.**Aşırı filtre ve asistan "Bunu yapamam" diye tekrarlıyor.
  **过度激进的幻觉过滤。**过度过助手会重复"我帮不了"──过不足则什么都说──在留出集上校准──
- **No wake-word option.**Her zaman dinlemek gizlilik sorumluluğudur.
  **没有唤醒词选项。**持续监听是隐私负担──添加唤醒词门控(Porcupine 或 openWakeWord)──

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-voice-assistant-architect.md`.Büjet + ölçek + dil + uyumluluk kısıtlamaları göz önüne alındığında, tam bir stok özellikleri oluşturun.

> 保存为 `outputs/skill-voice-assistant-architect.md`◊ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △    △ △ △ 

## Egzersizler.

1. **Easy.**Çık .`code/main.py`Bir tam dönüşü sonundan sonuna simüle eder.
   **简单。**运行  İşlem`code/main.py`模块模拟一个完整轮次端到端并印各阶段延迟──
2. **Medium.**STT'nin yerine , önceden kaydedilen bir Whisper modeli koyun .`.wav`WER ve sonundan sonuna kadar gecikmeyi ölçmek.
   **中等。**Önceden`.wav`上用真实 Whisper 模型替换 STT 模块──测量 WER 和端到端延迟──
3. **Hard.**Araç çağrısı ekle: uygulay `get_weather`(herhangi bir API) ve `set_timer`. LLM'yi araçlar üzerinden yönlendirin ve kullanıcı "5 dakika zamanlayıcı ayarlayın" dediğinde doğru işlev ateşlendiğini ve konuşulan yanıtın bunu onayladığını kontrol edin.
   **困难。**添加工具调用:实现 `get_weather`(herhangi bir API)`set_timer`❖ Kullanıcı tarafından LLM aracılığıyla doğrulanmış bir işlev kullanılır.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Turn | A user + assistant round-trip | One VAD-bounded user speech + one LLM-TTS response. |
| Barge-in | Interruption | User speaks while assistant talks; assistant stops. |
| Wake word | "Hey assistant" | Short keyword detector; Porcupine, Snowboy, openWakeWord. |
| End-pointing | Turn ending | VAD + min-silence decision that user has finished. |
| Pre-roll | Pre-speech buffer | Keep 200-400 ms of audio before VAD fires to avoid first-word clip. |
| Tool call | Function invocation | LLM emits JSON; runtime dispatches; result feeds back in-loop. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 轮次 | 用户+助手一个来回 | 一次 VAD 界定的用户语音 + 一次 LLM-TTS 回应。 |
| 抢话 | 打断 | 助手说话时用户开口；助手停止。 |
| 唤醒词 | "嘿助手" | 短关键词检测器；Porcupine、Snowboy、openWakeWord。 |
| 端点检测 | 轮次结束 | VAD + 最小静音决策用户已说完。 |
| 预滚 | 语音前缓冲 | 在 VAD 触发前保留 200-400 ms 音频以避免首词截断。 |
| 工具调用 | 函数调用 | LLM 输出 JSON；运行时分发；结果在循环中反馈。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [LiveKit — voice agent quickstart](https://docs.livekit.io/agents/) Üretim derecesi referansı.
  LiveKit语音智能体快速入门生产级参考──
- [Pipecat — voice agent examples](https://github.com/pipecat-ai/pipecat) DIY dostu çerçeve.
  Pipecat语音智能体例DIY 友好框架──
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime) yönetilen ses-dev yol.
  OpenAI Gerçek Zamanlı API托管的语音原生路径──
- [Kyutai Moshi](https://github.com/kyutai-labs/moshi) Tam ikili referans (Desin 15).
  Kyutai Moshi全双工参考(第 15 课)。
- [Porcupine wake-word](https://picovoice.ai/products/porcupine/)- Uyanık söz kaplama.
  Domuz 唤醒词唤醒词门控──
- [Anthropic — tool use guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) LLM fonksiyonu çağrısı.
  Antropik 工具使用指南 LLM 函数调用。

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

