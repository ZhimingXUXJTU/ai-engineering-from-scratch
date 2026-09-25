# Gerçek zamanlı ses işleme.

> Batch boru hattları bir dosyayı işliyor. Gerçek zamanlı boru hattları, sonraki 20 milisaniye gelmeden sonraki 20 milisaniyeyi işliyor. Her konuşma yapay zeka, yayın stüdyosu ve telefon robotu bu gecikme bütçesiyle yaşar ve ölür.

> **【中文解读】**批处理流水线处理文件,实时流水线在下20毫秒到达之前处理完结此20毫秒.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms), Phase 6 · 04 (ASR), Phase 6 · 07 (TTS) | **前置知识:** 阶段 6 · 02（频谱图），阶段 6 · 04（ASR），阶段 6 · 07（TTS）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Sorunlar. Sorunlar.

İnsan konuşmalarının dönüş süresi 230 ms'dir. 500 ms'den fazla olan her şey robot gibi hisseder. 1500 ms'den fazla olan ise kırılmış gibi hisseder.**hear → understand → respond → speak**2026'da döngü:

> İnsan sohbetini süresi yaklaşık 230 ms geciktirmek istiyor.**听 → 理解 → 回应 → 说**Bu bütçe:

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

| Stage | Budget |
|-------|--------|
| Mic → buffer | 20 ms |
| VAD | 10 ms |
| ASR (streaming) | 150 ms |
| LLM (first token) | 100 ms |
| TTS (first chunk) | 100 ms |
| Render → speaker | 20 ms |
| **Total** | **~400 ms** |

| 阶段 | 预算 |
|------|------|
| 麦克风 → 缓冲 | 20 ms |
| VAD | 10 ms |
| ASR（流式） | 150 ms |
| LLM（首 token） | 100 ms |
| TTS（首块） | 100 ms |
| 渲染 → 扬声器 | 20 ms |
| **总计** | **约 400 ms** |

Moshi (Kyutai, 2024) 200 ms tam çiftlik saatini yaptı. GPT-4o gerçek zamanlı saatler (2024) ~ 320 ms. 2022'de kaskad boru hattları 2500 ms'de gönderildi. 10x iyileştirme üç teknikten geldi: (1) her yerde akış, (2) kısmi sonuçlarla asinkron boru hattı, (3) kesilebilir üretim.

> Moshi(Kyutai,2024) 200 ms'i gerçekleştirdi 全双工──GPT-4o-realtime(2024) Yaklaşık 320 ms──2022 yılının seviyesindeki su akışı 2500 ms──10 kat arttı üç teknikten:

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Streaming audio pipeline with ring buffer, VAD gate, interruption](../assets/real-time.svg)

**Frame / chunk / window.**Gerçek zamanlı ses akışı sabit boyutlu bloklar olarak. Genel seçim: 20 ms (320 örnek 16 kHz).

> **帧/块/窗口。**实时音频固定大小的块流动──常见选择:20 ms(16 kHz 下 320 采样点)──下游一切都必须跟上这个节奏──

**Ring buffer.**Sıkı boyutlu döngü tampon. Üreticiler fişi yeni çerçeveler yazar, tüketici fişi okuyor. Sıcak yolda tahsis edilmesini engeller. Ölçüm ≈ maksimum gecikme × örnek hızı; 2 saniye 16 kHz yüzüğü = 32.000 örnek.

> **环形缓冲区。**固定大小的循环缓冲区──生产者线程写入新,消费者线程读取──热路中的内存分配的防止──大小约等于最大延迟 × 采样率;2秒 16 kHz 环形缓冲 = 32,000 采样点──

**VAD (Voice Activity Detection).**Silero VAD 4.0 (2024) CPU'da 30 ms çerçeve başına < 1 ms çalışır. `webrtcvad`Bu daha eski bir alternatif.

> **VAD（语音活动检测）。**无人说话时阻止下游工作──Silero VAD 4.0(2024) CPU'da her 30 ms 运行 <1 ms──`webrtcvad`Daha eski bir alternatif.

**Streaming ASR.**Ses geldiğinde kısmi transkriptleri yayan modeller. Parakeet-CTC-0.6B akış modunda (NeMo, 2024) 320 ms gecikme ile %2 5% WER yapar. Whisper-Streaming (Macháček et al., 2023) ~ 2 saniye gecikme ile yakında akışmak için Whisper parçaları.

> **流式 ASR。**随音频到达而输出部分转录的模型──Parakeet-CTC-0.6B 流式模式──NeMo,2024) 320 ms 延迟下实现 2-5% WER──Whisper-Streaming──Macháček 等,2023) Whisper 分块实现接近流式的约2秒延迟──

**Interruption.**Kullanıcı konuşurken asistan konuşurken, (a) barge-in'i algılamanız, (b) TTS'yi durdurmanız, (c) kalan LLM çıkışını atmanız gerekir.

> **打断。**Bu nedenle, bu programın tümü 100 ms içinde tamamlanmak için kullanıcının ağzını açmak için kullanılır.

**WebRTC Opus transport.**20 ms çerçeveleri, 48 kHz, adapte bit hızı 8128 kbps. Tarayıcı ve mobil için standart. LiveKit, Daily.co, Pion ses uygulamaları oluşturmak için 2026 yığınlarıdır.

> **WebRTC Opus 传输。**20 ms ,48 kHz, öz uygulama oranı 8-128 kbps。 browser ve mobil端 standartları。LiveKit、Daily.co、Pion is 2026 year building语音应用的技术──

**Jitter buffer.**Ağ paketleri düzensiz / geç gelir. Jitter tamponu yeniden düzenlenir ve düzeltir; çok küçük → sesli boşluklar, çok büyük → gecikme. 6080 ms tipik.

> **抖动缓冲区。**网络包乱序/迟到到达──动缓冲区重排和平滑;太小 → 可听间隙,太大 → 延迟──典型值 60-80 ms──

### Ortak çöpler

> ### 常见陷

- **Thread contention.**Python'un GIL + ağır modelleri ses düğümünü aç bırakabilir. C- çağrı geri ses kütüphanesi (ses cihazı, PortAudio) kullanın ve Python'u sıcak yoldan uzak tutun.
  **线程竞争。**Python'un GIL + 重模型会使音频线程饥饿──使用 C 回调音频库(son cihaz、PortAudio),让 Python 远离热路径──
- **Sample-rate conversion latency.**Boru hattının içinde yeniden örnekleme 520 ms ekler. Ya önce yeniden örnekleme veya sıfır gecikme yeniden örnekleme kullanın (PolyPhase, `soxr_hq`)
  **采样率转换延迟。**流水线内部重采样增加5-20 ms──要么提前重采样,要么使用零延迟重采样器──
- **TTS priming.**Kokoro gibi hızlı TTS'ler bile ilk istek üzerine 100 200 ms ısınma süresi kullanıyor.
  **TTS 预热。**Hatta Kokoro gibi hızlı TTS ilk istek sırasında da 100-200 ms 预热──缓存模型 + ilk gerçek turda 预用假运行预热──
- **Echo cancellation.**AEC olmadan, TTS çıkışı mikrofona geri giriyor ve botun kendi sesinde ASR'yi tetikler. WebRTC AEC3 açık kaynaklı varsayılanıdır.
  **回声消除。**没有AEC,TTS 输出重新进入麦克风并触发 ASR 识别机器人自己的声音──WebRTC AEC3 是开源默认方案──

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.

> **【拓展：语音隐私与安全】**语音数据 contains a lot of personal privacy information (Sözleşme 对话 内容) ◦深度伪造 (Depfake) 语音技术 (Sözleşme 信息) 语音 数据 语音 数据 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 信息 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语音 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语 语





## Yapın.
```figure
nyquist-aliasing
```

## Yapın

### Adım 1: Yüzük tamponu

```python
import collections

class RingBuffer:
    def __init__(self, capacity):
        self.buf = collections.deque(maxlen=capacity)
    def write(self, frame):
        self.buf.extend(frame)
    def read(self, n):
        return [self.buf.popleft() for _ in range(min(n, len(self.buf)))]
    def level(self):
        return len(self.buf)
```

Kapasite maksimum tampon gecikmesini belirler. 32 bin örnek 16 kHz = 2 saniye.

### Adım 2: VAD kapısı

```python
def simple_energy_vad(frame, threshold=0.01):
    return sum(x * x for x in frame) / len(frame) > threshold ** 2
```

Silero VAD ile değiştirilmek:

```python
import torch
vad, _ = torch.hub.load("snakers4/silero-vad", "silero_vad")
is_speech = vad(torch.tensor(frame), 16000).item() > 0.5
```

### Adım 3: Akış ASR

```python
# Parakeet-CTC-0.6B streaming via NeMo
from nemo.collections.asr.models import EncDecCTCModelBPE
asr = EncDecCTCModelBPE.from_pretrained("nvidia/parakeet-ctc-0.6b")
# chunk_ms=320 ms, look_ahead_ms=80 ms
for chunk in audio_stream():
    partial_text = asr.transcribe_streaming(chunk)
    print(partial_text, end="\r")
```

### 4. Adım: Kesinlik yöneticisi

```python
class Dialog:
    def __init__(self):
        self.tts_task = None

    def on_user_speech(self, frame):
        if self.tts_task and not self.tts_task.done():
            self.tts_task.cancel()   # barge-in
        # then feed to streaming ASR

    def on_final_user_utterance(self, text):
        self.tts_task = asyncio.create_task(self.reply(text))

    async def reply(self, text):
        async for tts_chunk in llm_then_tts(text):
            speaker.write(tts_chunk)
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


Async I/O ve iptal edilebilir TTS akışında. WebRTC peerconnection.stop() ses izinde kanonik yol.

> TTS 流式传输――WebRTC'nin eş bağlantısı.stop() 停止音频轨道是标准方式──




> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

2026'da:

| Layer | Pick |
|-------|------|
| Transport | LiveKit (WebRTC) or Pion (Go) |
| VAD | Silero VAD 4.0 |
| Streaming ASR | Parakeet-CTC-0.6B or Whisper-Streaming |
| LLM first-token | Groq, Cerebras, vLLM-streaming |
| Streaming TTS | Kokoro or ElevenLabs Turbo v2.5 |
| Echo cancel | WebRTC AEC3 |
| End-to-end native | OpenAI Realtime API or Moshi |

| 层 | 选择 |
|----|------|
| 传输 | LiveKit（WebRTC）或 Pion（Go） |
| VAD | Silero VAD 4.0 |
| 流式 ASR | Parakeet-CTC-0.6B 或 Whisper-Streaming |
| LLM 首 token | Groq、Cerebras、vLLM-streaming |
| 流式 TTS | Kokoro 或 ElevenLabs Turbo v2.5 |
| 回声消除 | WebRTC AEC3 |
| 端到端原生 | OpenAI Realtime API 或 Moshi |



## Tuzaklar

> 常见陷

- **Buffering 500 ms to be safe.**Bufer, gecikme zemininiz.
  **缓冲 500 ms 求安全。**缓冲区*就是*你的延迟下限──缩小它──
- **Not pinning threads.**Uayından öncelikli olarak düşük bir düğümde ses çağrısı = yük altında hatalar.
  **没有绑定线程。**音频回调 低于 UI 优先线程上 = 负载下出现故障──
- **TTS chunks too small.**200 ms altındaki parçalar Vocoder eserlerini duyururur. 320 ms parçaları en güzel noktayı.
  **TTS 块太小。**200 ms'dan az olan bloklar ses kodlayıcıyı sahte görüntülebilir. 320 ms'lik bloklar en iyi dengeleyici noktadır.
- **No jitter buffer.**Gerçek ağlar sinirlidir. Yumuşatmadan poplar olur.
  **没有抖动缓冲。**Gerçek ağlar var, hiç bir düzlük yok.
- **Single-shot error handling.**Ses boruları çarpışmalara karşı sağlam olmalı.
  **单次错误处理。**Bir an önce bir ölümle karşılaştım.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-realtime-designer.md`.Eğer bir aşama için belirli gecikme bütçeleri ile gerçek zamanlı bir ses borusunu tasarlayın.

> 保存为 `outputs/skill-realtime-designer.md`❖ tasarım her aşamada belirli bir gecikme bütçesi vardır.

## Egzersizler.

1. **Easy.**Çık .`code/main.py`. Bir yüzük tamponu + enerji VAD simülasyonu; sahte 10 saniye akış için aşama gecikmelerini yazdırır.
   **简单。**运行  İşlem`code/main.py`❖ 模拟环形缓冲区 + 能量 VAD; 印假 10 秒流の各段延迟──
2. **Medium.**Kullanım`sounddevice`, 20 ms çerçeve içinde mikrofonunu işleyen ve her çerçeveye VAD durumu yazdırırmak için bir geçiş yolu döngüsü oluşturmak.
   **中等。**Kullanım`sounddevice` 20 ms'lik bir düz döngü oluşturun ve her gün VAD'de basın.
3. **Hard.**Tam bir duplex ekro testi yapın `aiortc`: browser → WebRTC → Python → WebRTC → browser. 1 kHz nabızla camdan camya gecikmeyi ölçün.
   **困难。**Kullan .`aiortc`构建全双工回声测试:浏览器 → WebRTC → Python → WebRTC → 浏览器──用 1 kHz 脉冲测量端到端延迟──

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Ring buffer | The circular queue | Fixed-size, lock-free (or SPSC-locked) FIFO for audio frames. |
| VAD | Silence gate | Model or heuristic marking speech vs non-speech. |
| Streaming ASR | Real-time STT | Emits partial text as audio arrives; bounded lookahead. |
| Jitter buffer | Network smoother | Queue reordering out-of-order packets; 60–80 ms typical. |
| AEC | Echo cancellation | Subtracts speaker-to-mic feedback path. |
| Barge-in | User interrupt | System detects user speech mid-TTS; must cancel playback. |
| Full duplex | Simultaneous both ways | User and bot can talk at the same time; Moshi is full duplex. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 环形缓冲 | 那个循环队列 | 固定大小、无锁（或 SPSC 锁）的音频帧 FIFO。 |
| VAD | 静音门 | 标记语音 vs 非语音的模型或启发式。 |
| 流式 ASR | 实时 STT | 随音频到达输出部分文本；有限前瞻。 |
| 抖动缓冲 | 网络平滑器 | 重排乱序包的队列；典型 60-80 ms。 |
| AEC | 回声消除 | 减去扬声器到麦克风的反馈路径。 |
| 抢话 | 用户打断 | 系统在 TTS 播放中检测用户语音；必须取消播放。 |
| 全双工 | 双向同时 | 用户和机器人可以同时说话；Moshi 是全双工。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Macháček et al. (2023). Whisper-Streaming](https://arxiv.org/abs/2307.14743) Yaklaşık akışlı fısıldama.
  Macháček 等 (2023). Şapşır-Streaming分块近流式 Şapşır。
- [Kyutai (2024). Moshi](https://kyutai.org/Moshi.pdf) Tam duplex 200 ms gecikme.
  Kyutai (2024). Moshi全双工 200 ms 延迟──
- [LiveKit Agents framework (2024)](https://docs.livekit.io/agents/) üretim ses ajan orkestrasyonu.
  LiveKit Ajanları 框架(2024) 生产级音频智能体编排──
- [Silero VAD repo](https://github.com/snakers4/silero-vad) sub-1 ms VAD, Apache 2.0.
  Silero VAD  depo 亚毫秒 VAD,Apache 2.0
- [WebRTC AEC3 paper](https://webrtc.googlesource.com/src/+/main/modules/audio_processing/aec3/) Açık kaynak altında yankon iptal edilmesi.
  WebRTC AEC3 论文 开源回声消除──

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

