# Şapışmak  Memurlık ve Fine-Tuning  Şapışmak  Yapı ve biçim

> Whisper, 30 saniyelik bir pencere transformatörü kodlayıcı-dekoder, 680 bin saatlik çok dilli zayıf denetimli ses metni çiftlerinde eğitilmiştir.

> **【中文解读】**Whisper, 30 saniyelik pencerede bir Transformer 编码器-解码器, 680.000小时多语言弱监督音频-文本对上训―― bir yapı, çok tür görevler, 识别,翻译,检测语言), 99 种语言――覆盖的 2026年语音识别的标杆模型――

> **【拓展：Whisper 的生态】**Hısnık 衍生了 Hısnık.cpp(本地部署)、Faster-Hisper(CTtranslate2 加速)、HısnıkX(词级时间)、Bloomsbury(实时流式)等工具链,是语音识别工业部署的事实标准──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 5 · 10 (Attention), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 04（ASR），阶段 5 · 10（注意力机制），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Sorunlar. Sorunlar.

OpenAI tarafından Eylül 2022'de yayınlanan Whisper, bir mal olarak gönderilen ilk ASR modeliydi: ses koy, metin alın, 99 dil, gürültüye dayanıklı, bir dizüstü bilgisayarda çalışır. 2024 yılına kadar OpenAI, Large-v3 ve Turbo çeşitlerini göndermişti; 2026 yılına kadar, Whisper, podcast transkripsiyonundan ses asistanlarına kadar YouTube altyazımlarına kadar her şey için varsayılan temel çizgidir.

> Whisper, OpenAI tarafından 2022 yılının Eylül ayında yayınlanmıştır. Bu, ilk olarak genel ürün olarak yayınlanan ASR modelidir: Yapıştırma, Metin Alışması, 99 种语言, 抗噪, notebook üzerinde kullanılabilir. 2024 yılına kadar, OpenAI tarafından Large-v3 和 Turbo 变体 yayınlanmıştır. 2026 yılına kadar, Whisper, kullanıcılardan ses yardımcısı olarak kaydedilen seslerden YouTube 字幕 ve diğer tüm sahnelerin özgün temelini oluşturmaktadır.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

Ama Whisper, sonsuza kadar kara kutu gibi davranılabilecek bir boru hattı değil.

> Ama fısıltı, kara kutuda sürekli olarak kullanılabilecek bir su hattı değildir. Bölge hareketleri onu yok eder.

1. İçeride ne olduğunu.
   İçinde ne var ki?
2. Nasıl doğru şekilde parçalanmış, akışlı veya uzun formatlı ses verirsin?
   Nasıl doğru bir şekilde bir parça 流式 veya长音频输入?
3. Ne zaman ve nasıl ayarlanacak.
   Ne zaman ve nasıl düzenlenir?

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


## Konsepten bir şey.

![Whisper encoder-decoder, tasks, chunked inference, fine-tune](../assets/whisper.svg)

**Architecture.**Standart transformatör kodlayıcı-dekoder.

> **架构。**标准 Transformer 编码器-解码器。

- Giriş: 30 saniyelik log-mel spektrogramı, 80 mels, 10 ms hop → 3000 çerçeve.
  输入30 秒 log-mel 频谱图,80 mels,10 ms 步长 → 3000 ──短片段零填充,长片段分块──
- Kodlayıcı: konvulsiyon aşağı örnek (addım 2) + `N`Büyük V3: 32 katman, 1280 katman, 20 baş.
  编码器:卷积下采样(步幅 2) + `N`个 Transformer 块──Large-v3:32 层,1280 维,20 头──
- Çözücü: `N`Transformer blokları sebebsel kendi kendine atn + kodlayıcı çıkışına çapraz atn.
  解码器:`N`个带因果自注意力 +编码器输出交叉注意力 Transformer 块──与编码器同大小──
- Çıktı: 51.865'lik bir sözcük üzerinde BPE tokenleri.
  输出:51,865 token 词表上的 BPE token──

Large-v3'de 1.55B parametreleri vardır. Turbo, 4 katlı bir dekodör kullanır (32'den itibaren), %1 WER çarpması ile 8× gecikme keser.

> Büyük-v3 15.5 milyar parametre vardır. Turbo 4 katlı çözücü kullanmak, 32 katlı çözücü kullanmak, 8 katı geçiş, %1'e kadar kaybı yok.

**The prompt format.**Whisper , dekodör uyarısında özel jetonlar tarafından yönlendirilmiş bir çok görevli modeldir:

> **提示格式。**Whisper bir çok görevli model, çözücü ipuçları içindeki özel işaretle kontrol etmek için:

```
<|startoftranscript|><|en|><|transcribe|><|notimestamps|> Hello world.<|endoftext|>
```

- `<|en|>` dil etiketi; çevirme karşı transkripsiyon davranışını zorlar.
  `<|en|>` 语言标签;强制翻译或转录行为──
- `<|transcribe|>`veya `<|translate|>` herhangi bir dil girişinden veya kelimenin tam anlamıyla İngilizce çıkışını çevirin.
  `<|transcribe|>`Ya da`<|translate|>` From any language输入翻译为英文输出,或逐字转录──
- `<|notimestamps|>` kelime seviyesindeki zaman damgasını atlayın (hızlı).
  `<|notimestamps|>` 跳过词级时间(更快)。

Bu, bir modelin birçok görevi yapmasına izin veren bir prompt.`<|en|>`- ...`<|fr|>`Fransızca yazıyor.

> 提示 is to let a model complete many tasks ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒  ⇒  ⇒   ⇒        ⇒                                                                                                                                                                                                                                                                                                                                             `<|en|>`改为 `<|fr|>`Fransızca'ya dönüştürülmüş.

**30-second window.**Her şey 30 saniyeye bağlanır. Uzun klipler parçalanmaya ihtiyaç duyar; kısa klipler dolandırılır. Windows doğal olarak akışlanmaz  bu nedenle WhisperX, Whisper-Streaming ve daha hızlı fısıldayan var.

> **30 秒窗口。**Bir de 30 saniyelik bir basamak için. Daha uzun ses sesleri parça parçaları gerektirir. Daha kısa sesleri doldurulmalıdır. Pencere kendiliğinden orijinal yaşam akımını desteklemiyor.

**Log-mel normalization.** `(log_mel - mean) / std`Whisper'in kendi eğitim kurpusundan gelen istatistikler.`whisper.audio.log_mel_spectrogram`- Hayır .`librosa.feature.melspectrogram`- Evet .

> **Log-mel 归一化。** `(log_mel - mean) / std`Bu sayede Whisper'in kendi eğitimini yaptırmak için kullandığı bir araç var.`whisper.audio.log_mel_spectrogram`), yerine `librosa.feature.melspectrogram`- Evet.

### 2026'da değişiklikler

> ### 2026 yılının değişimi

| Variant | Params | Latency (A100) | WER (LibriSpeech-clean) |
|---------|--------|----------------|------------------------|
| Tiny | 39M | 1× realtime | 5.4% |
| Base | 74M | 1× | 4.1% |
| Small | 244M | 1× | 3.0% |
| Medium | 769M | 1× | 2.7% |
| Large-v3 | 1.55B | 2× | 1.8% |
| Large-v3-turbo | 809M | 8× | 1.58% |
| Whisper-Streaming (2024) | 1.55B | streaming | 2.0% |

| 变体 | 参数量 | 延迟（A100） | WER（LibriSpeech-clean） |
|------|--------|--------------|-------------------------|
| Tiny | 3900 万 | 1× 实时 | 5.4% |
| Base | 7400 万 | 1× | 4.1% |
| Small | 2.44 亿 | 1× | 3.0% |
| Medium | 7.69 亿 | 1× | 2.7% |
| Large-v3 | 15.5 亿 | 2× | 1.8% |
| Large-v3-turbo | 8.09 亿 | 8× | 1.58% |
| Whisper-Streaming（2024） | 15.5 亿 | 流式 | 2.0% |

### Düzgün ayarlama

> ### 微调

2026 yılında Kanonik çalışma akışı:

> 2026 Yıllık Standart Gezi:

1. Düzleştirilmiş transkriptlerle hedef alan ses 10100 saat toplayın.
   收集 10-100 小时目标领域的音频及对应转录文本──
2. Çık .`transformers.Seq2SeqTrainer`- Evet .`generate_with_loss`Geri çağır.
   Kullanım`transformers.Seq2SeqTrainer`和 `generate_with_loss`回调运行训练──
3. Parametre- verimli: LoRA `q_proj`- Evet .`k_proj`- Evet .`v_proj`Dikkat katmanlarının GPU belleğini 4×'ye düşürüyor ve WER maliyeti < 0.3'dir.
   参数高效: `q_proj`- Evet.`k_proj`- Evet.`v_proj`Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü Ü
4. Eğer <10 saatiniz varsa kodlayıcıyı dondurun.
   Eğer veriler 10 saatten azsa, sadece küçük bir kodlama makinesi kullanın.
5. Whisper'in kendi tokenizer ve prompt formatını kullanın; tokenizerleri asla değiştirmeyin.
   Whisper kullan  kendi tokenizer 和提示格式;永远不要替换tokenizer──

Topluluk sonuçları: 20 saatlik tıbbi diktasyonda ortalama ayarlama tıbbi kelime birikimine %12'den %4,5'e düşer.

> 社区结果: 20 saatte tıbbi konuşmalarda azalma Ortalama, tıbbi konuşmalarda WER %12'den %4.5'e düştü.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.



## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

```figure
sp-asr-attention
```

## Yapın

### Adım 1: Kıskançlığı kutudan çıkar

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe(
    "clip.wav",
    language="en",
    task="transcribe",
    temperature=0.0,
    condition_on_previous_text=False,  # prevents runaway repetition
)
print(result["text"])
for seg in result["segments"]:
    print(f"[{seg['start']:.2f}–{seg['end']:.2f}] {seg['text']}")
```

Her zaman geçersiz kılmanız gereken anahtar varsayımlar: `temperature=0.0`(defaultları örneğe alarak 0.0 → 0.2 → 0.4 ... geri dönüş zinciri) `condition_on_previous_text=False`(kaskadör halüsinasyon problemini önler) ve`no_speech_threshold=0.6`(Sessizlik algısı).

> Hep kapsamalı olan anahtar gizlilik değerleri:`temperature=0.0`(采样默认为 0.0 → 0.2 → 0.4 ... 回退链)`condition_on_previous_text=False`(proticize seviye hallu problem)`no_speech_threshold=0.6`(静音检测)

### Adım 2: Uzun şekilli parçalar

```python
# whisperx is the 2026 reference for long-form with word-level timestamps
import whisperx
model = whisperx.load_model("large-v3-turbo", device="cuda", compute_type="float16")
segments = model.transcribe("1hour.mp3", batch_size=16, chunk_size=30)
```

WhisperX (1) Silero VAD kaplama, (2) wav2vec 2.0 üzerinden kelime seviyesinde birleştirme, (3) günlükleştirme `pyannote.audio`2026'da üretime dönüştürülecek bir iş atı.

> WhisperX 添加了 (1) Silero VAD 门控,(2) 通过 wav2vec 2.0 实现词级对齐,(3) 通过 `pyannote.audio`实现说话人分离──2026年生产转录的主力工具──

### Adım 3: LoRA ile ince ayarlama

```python
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from peft import LoraConfig, get_peft_model

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3-turbo")
lora = LoraConfig(
    r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1, bias="none", task_type="SEQ_2_SEQ_LM",
)
model = get_peft_model(model, lora)
# model.print_trainable_parameters()  -> ~3M trainable / 809M total
```

Sonra standart Trainer döngüsü, her 1000 adımda bir kontrol noktası, UYK ile beklenmiş durumları değerlendirin.

> Sonra standartlar Trainer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

### Dördüncü adım: Her katman ne öğreniyorsa kontrol edin

```python
# Grab cross-attention weights during decode to see what the decoder attends to.
with torch.inference_mode():
    out = model.generate(
        input_features=features,
        return_dict_in_generate=True,
        output_attentions=True,
    )
# out.cross_attentions: layer × head × step × src_len
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


Bir ısıtma haritasıyla görselleştirin  dekodör adımları kodlayıcı çerçeveleri aracılığıyla tarayılırken diyagonal ayar görülecektir.

> 热力图可视化你会看到解码器步骤进扫描编码器时的对角线对齐那条对角线就是 Whisper'in kelime 时间 概念──




> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

2026'da:

> 2026 yılının teknolojisi:

| Situation | Pick |
|-----------|------|
| General English, offline | Large-v3-turbo via `whisperx` |
| Mobile / edge | Whisper-Tiny quantized (int8) or Moonshine |
| Multilingual long-form | Large-v3 via `whisperx` + diarization |
| Low-resource language | Fine-tune Medium or Turbo with LoRA |
| Streaming (2 s latency) | Whisper-Streaming or Parakeet-TDT |
| Word-level timestamps | WhisperX (forced alignment via wav2vec 2.0) |

| 场景 | 选择 |
|------|------|
| 通用英文、离线 | 通过 `whisperx` 使用 Large-v3-turbo |
| 移动端/边缘设备 | 量化 Whisper-Tiny（int8）或 Moonshine |
| 多语言长音频 | 通过 `whisperx` 使用 Large-v3 + 说话人分离 |
| 低资源语言 | 用 LoRA 微调 Medium 或 Turbo |
| 流式（2 秒延迟） | Whisper-Streaming 或 Parakeet-TDT |
| 词级时间戳 | WhisperX（通过 wav2vec 2.0 强制对齐） |

`faster-whisper`(CTranslate2 backend) 2026'da en hızlı CPU + GPU sonuç süresi  4x aynı çıkışla vanilya daha hızlıdır.

> `faster-whisper`(CTranslate2 后端) 2026 yılının en hızlı CPU+GPU 推理运行时比原始版本快4倍,输出完全相同──



## 2026'da hala yolculuk eden tuzaklar

> 2026 yılı hâlâ suçlu bir tuzağa düşüyor.

- **Hallucinated text on silence.**Başlıklara göre eğitilmiş fısıltılar "Seyrettiğiniz için teşekkürler!", "Abone olun!", şarkı sözleri içerir.
  **静音上的幻觉文本。**Sısırlamak, "Sözüm için teşekkürler!"
- **`condition_on_previous_text` cascade.**Bir halüsinasyon sonraki pencereleri kirletiyor.`False`Eğer parçalar arasında akıcılık gerekmezse.
  **`condition_on_previous_text` 级联。**Bir görüntü kirlenmeden sonra penceresi.`False`- Evet.
- **Short-clip padding.**30 saniyeye kadar doldurulan 2 saniyelik bir klip, sonraki sessizlikte halüsinasyonlar yaratabilir.`pad=False`Ya da VAD-gate.
  **短片段填充。**2 saniyelik bölüm 30 saniye kadar doldurular.`pad=False`Ya da çok kötü.
- **Wrong mel stats.**Whisper'in yerine librosa'nın mels'ini kullanmak neredeyse rastgele çıkış üretir.`whisper.audio.log_mel_spectrogram`- Evet .
  **错误的 mel 统计量。**Kütüphanenin fısıltıları değil, fısıltılar neredeyse her zaman çıkış yapar.`whisper.audio.log_mel_spectrogram`- Evet.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-whisper-tuner.md`- Belirli bir alan için Whisper ince ayar veya sonuçlar boru hattı tasarlayın.

> 保存为 `outputs/skill-whisper-tuner.md`❖ belirli alanlar için tasarlanmıştır

## Egzersizler.

1. **Easy.**Çık .`code/main.py`Whisper tarzı bir istek simgesi oluşturur, çözülmüş biçim bütçelerini hesaplar ve 10 dakikalık bir klip için parça programını basar.
   **简单。**运行  İşlem`code/main.py`❖ Bu, Whisper 风格 风格 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 提示 
2. **Medium.**Kurulum`faster-whisper`, 10 dakikalık bir podcast transkripte, WER'i insan transkriptine karşı karşılaştır.`language="auto"`- Zorla`language="en"`- Evet .
   **中等。**- Yapımcılık`faster-whisper`, Transcript 10 dakika, yapay transcript ile karşılaştırın WER 尝试`language="auto"`İhtiyaçlı`language="en"`- Evet.
3. **Hard.**HF kullanmak `datasets`, Whisper'in mücadele ettiği bir dil seçin (örneğin, Urdu), 2 saatte 2 dönem boyunca Orta ile LoRA'yı ince ayarlayın ve WER delta raporunu yapın.
   **困难。**HF kullan `datasets`, seçin Bir Şapış 困难的语言(如乌尔都语), 2 小时数据上使用 LoRA 微调 Medium 2 个时代,报告 WER 差值──

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 30-sec window | Whisper's limit | Hard input cap; chunk longer audio. |
| SOT | Start-of-transcript | `<\|startoftranscript\|>` kicks off the decoder prompt. |
| Timestamps token | Temporal alignment | Every 0.02 s offset is a special token in the 51k vocab. |
| Turbo | The fast variant | 4-decoder layers, 8× faster, <1% WER regression. |
| WhisperX | The long-form wrapper | VAD + Whisper + wav2vec alignment + diarization. |
| LoRA fine-tune | Efficient tuning | Add low-rank adapters to attention; train ~0.3% of params. |
| Hallucination | The silent failure | Whisper produces fluent English from noise/silence. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 30 秒窗口 | Whisper 的限制 | 硬性输入上限；更长音频需分块。 |
| SOT | 转录开始 | `<\|startoftranscript\|>` 启动解码器提示。 |
| 时间戳 token | 时间对齐 | 每 0.02 秒偏移是 51k 词表中的特殊 token。 |
| Turbo | 快速变体 | 4 层解码器，快 8 倍，WER 回退 <1%。 |
| WhisperX | 长音频封装 | VAD + Whisper + wav2vec 对齐 + 说话人分离。 |
| LoRA 微调 | 高效调优 | 在注意力层添加低秩适配器；仅训练约 0.3% 参数。 |
| 幻觉 | 静默失败 | Whisper 从噪声/静音中产生流畅的英文。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Radford et al. (2022). Whisper paper](https://arxiv.org/abs/2212.04356) orijinal mimarlık ve eğitim tarifi.
  Radford 等 (2022). Whisper 论文原始架构和训练方案──
- [OpenAI (2024). Whisper Large-v3-turbo release](https://github.com/openai/whisper/discussions/2363)4 katlı dekodör, 8 kat hızlandırma.
  OpenAI (2024). Whisper Large-v3-turbo 发布4 层解码器,8 倍加速──
- [Bain et al. (2023). WhisperX](https://arxiv.org/abs/2303.00747)Uzun şekil, kelimeyle uyumlu, günlük.
  Sıcaklık, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma, sesli konuşma.
- [Systran — faster-whisper repo](https://github.com/SYSTRAN/faster-whisper) CTranslate2 desteklenmiş, 4x daha hızlı.
  Sistem Faster-Whisper 仓库 CTranslate2 后端,快4 倍──
- [HuggingFace — Whisper fine-tune tutorial](https://huggingface.co/blog/fine-tune-whisper) Kanonik LoRA / tam FT yürüyüş.
  Öğünmüş YüzFısıltı 微调教程标准 LoRA/全参数微调指南。

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

