# Ses-Dil Modelleri  Qwen2.5 Omni, Ses Flamingo, GPT-4o Ses

> 2026 ses dili modelleri konuşma + çevresel ses + müzik üzerinde düşünüyor. Qwen2.5-Omni-7B MMAU-Pro'da GPT-4o Audio ile eşleşir. Audio Flamingo Next LongAudioBench'de Gemini 2.5 Pro'yu yener. Açık ve kapalı arasındaki boşluk, herkesin neredeyse rastgele olduğu çok sesli görevler hariç, esasen kapalıdır.

> **【中文解读】**2026 yılının ses sesli dil modeli bilerek语音+环境声+音乐──Qwen2.5-Omni-7B, MMAU-Pro'da GPT-4o Audio,Audio Flamingo'da LongAudioBench'de LongAudioBench'de 2.5.5 Pro'dan daha üstün olan açık kaynak ve kapalı kaynak farkı tamamen kayboldu──

> **【拓展：音频大模型的新时代】**音频语言模型, LLM'nin düşünme yeteneğini 音频 alanına genişletecek, aynı zamanda语音内容、识别环境声音、分析音乐结构── bu çok modolu AI'nin önemli yönüdür──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 12 · 03 (Vision-Language Models), Phase 7 · 10 (Audio Transformers) | **前置知识:** 阶段 6 · 04（ASR），阶段 12 · 03（视觉语言模型），阶段 7 · 10（音频 Transformer）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Sorunlar. Sorunlar.

5 saniyelik sesiniz var: köpek havlıyor, biri "dur!" diye bağırıyor, sonra sessizlik.

> Bir köpek çığlık atıyor, biri "dur!" diye bağırıyor, sonra da ses sesli.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

- **Transcription.**"Ne söylendi?"  ASR bölgesinde.
  **转录。**"Ne dedi?" ASR 領域。
- **Semantic reasoning.**"İnsan tehlikede mi?"  havlama + bağırmak + sessizlik hakkında ortak bir anlayış gerektirir.
  **语义推理。**"Bu adam tehlikeli mi?"                                                                                                                                                                                                                                                            
- **Music reasoning.**"Ne tür aletler melodi çalıyor?"
  **音乐推理。**"Ne aletler melodi çalıyor?"
- **Long-audio retrieval.**"Bu 90 dakikalık konuşmada öğretmen, gradient düşüşünü nerede açıkladı?"
  **长音频检索。**"Bu 90 dakikalık konuşmada, öğretmen nerede derecenin düşüşünü açıkladı?"

Tüm bunları tek bir çağrı ile cevaplayan tek bir model **audio-language model**(LALM / ALM). Saf ASR'den ayrı: LALM'ler sadece transkriptleri değil, serbest biçimli doğal dil cevapları üretir.

> Tüm bu soruları tek bir örnekle cevaplamak için tek bir ipucu kullanın.**音频语言模型**(LALM / ALM) 〜区别于纯 ASR:LALM 生成自由形式的自然语言答案, sadece metin çevirmek değil,

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![Audio-language model: audio encoder + projector + LLM decoder](../assets/alm-architecture.svg)

### Üç bileşenli şablon

2026'da her LALM'de aynı iskelet vardır:

> ### Üç bileşen şablon

> 2026 yılında her bir LALM'de aynı yapı vardır:

1. **Audio encoder.**Şapış kodlayıcı · BEATs · CLAP · WavLM · veya model başına özel bir kodlayıcı.
   **音频编码器。**Şapışmak 编码器 · BEATs · CLAP · WavLM · 或每个模型的自定义编码器──
2. **Projector.**Lineer veya MLP köprü ses kodlayıcı özellikleri LLM'nin simge yerleştirme alanına.
   **投影器。**Sınıfın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir parçası olarak, bir programın bir araya getirilmiştir.
3. **LLM.**Llama / Qwen / Gemma tabanlı dekodör. Çelişkili metin + ses jetonlarını alır; metin oluşturur.
   **LLM。**基于 Llama / Qwen / Gemma 的解码器──接收交织的文本 + 音频代码;生成文本──

Eğitim:

> 訓練:

- **Stage 1.**Dondurma kodlayıcısı + LLM; tren projeksiyonu sadece ASR / başlık verileri üzerinde.
  **阶段 1。**结编码器 + LLM; sadece ASR/标注数据上训练投影器──
- **Stage 2.**Tam / LoRA ince ayarlamaları, talimatları takip eden ses görevleri (QA, akıl yürütme, müzik anlama) üzerinde.
  **阶段 2。**Bu nedenle, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını yaparak, bu işlemin tamamını gerçekleştirir.
- **Stage 3 (optional).**Ses içi / ses çıkışı konuşma dekodörü ekler. Qwen2.5-Omni ve AF3-Chat bunu yapar.
  **阶段 3（可选）。**语音入/语音出添加语音解码器──Qwen2.5Omni 和 AF3-Chat 实现这一点──

### 2026 model haritası

> ### 2026 yıl model harita

| Model | Backbone | Audio encoder | Output modality | Access |
|-------|----------|---------------|-----------------|--------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | Custom + Whisper | text + speech | Apache-2.0 |
| Qwen3-Omni | Qwen3 | Custom | text + speech | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | text | NVIDIA non-commercial |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | text | NVIDIA non-commercial |
| SALMONN | Vicuna | Whisper + BEATs | text | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | text | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | text | Apache-2.0 |
| Gemini 2.5 Flash/Pro (closed) | Gemini | proprietary | text + speech | API |
| GPT-4o Audio (closed) | GPT-4o | proprietary | text + speech | API |

| 模型 | 骨干 | 音频编码器 | 输出模态 | 访问方式 |
|------|------|-----------|---------|---------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | 自定义 + Whisper | 文本+语音 | Apache-2.0 |
| Qwen3-Omni | Qwen3 | 自定义 | 文本+语音 | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | 文本 | NVIDIA 非商业 |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | 文本 | NVIDIA 非商业 |
| SALMONN | Vicuna | Whisper + BEATs | 文本 | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | 文本 | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | 文本 | Apache-2.0 |
| Gemini 2.5 Flash/Pro（闭源） | Gemini | 专有 | 文本+语音 | API |
| GPT-4o Audio（闭源） | GPT-4o | 专有 | 文本+语音 | API |

### Benchmark gerçeklik kontrolü (2026)

**MMAU-Pro.**1800 konuşma / ses / müzik / karışıklık kapsamındaki QA çiftleri.

| Model | Overall | Speech | Sound | Music | Multi-audio |
|-------|---------|--------|-------|-------|-------------|
| Gemini 2.5 Pro | ~60% | 73.4% | 51.9% | 64.9% | ~22% |
| Gemini 2.5 Flash | ~57% | 73.4% | 50.5% | 64.9% | 21.2% |
| GPT-4o Audio | 52.5% | — | — | — | 26.5% |
| Qwen2.5-Omni-7B | 52.2% | 57.4% | 47.6% | 61.5% | ~20% |
| Audio Flamingo 3 | ~54% | — | — | — | — |
| Audio Flamingo Next | SOTA on LongAudioBench | — | — | — | — |

- Evet .**multi-audio column is damning for everyone.**4 seçeneklü birden fazla seçeneğin rastgele şansı = 25%; çoğu model burada puan alır. LALM'ler hala iki klipin karşılaştırılmasında zorlanırlar.

> **多音频列对所有人都是致命的。**4 選 1 多選題の随機概率 = 25%; çoğu model puanı orada bulunmaktadır.

### 2026 yılında LALM'lerin yararlı olduğu yerler

- **Compliance audit of call-center recordings.**"Agent, gerekli ifşa edilmesini söyledi mi?"
  **合规审计通话录音。**"Customer has提到了必要的免责声明?" diye sordu.
- **Accessibility.**Sesli olayları sağır kullanıcılara anlatın (sadece transkripsiyon değil).
  **无障碍。**Çıktı.
- **Content moderation.**Şiddetli dil + tehdit edici ton + arka plan bağlamı tespit et.
  **内容审核。**检测暴力语言 + 威胁语气 + 背景上下文。
- **Podcast / meeting chaptering.**Semantik özet, sadece konuşmacı döner değil.
  **播客/会议章节化。**语义摘要,不只是说话人轮次──
- **Music catalog analysis.**"B bölümünde anahtar değişikliği ile tüm parçaları bul".
  **音乐目录分析。**"Bütün B bölümlerinin değiştirilmiş şarkılarını bul".

### (Hâlâ) yararlı olmadıkları yerlerde

- Güzel tohumlu müzik teorisi (akord seviyesinin altında).
  精细音乐理论(和弦级别以下)
- Uzun konuşmalar (sadece 10 dakika geçen dereceler) üzerinde konuşmacı tarafından atfedilen mantıklama.
  长对话中的说话人归因推理 (sadece 10 dakika sonra)
- Çok sesli karşılaştırma (22-26% rastgeleden fazla değil).
                                                                                                                                                                                                                                                                
- Gerçek zamanlı akışlı akıl yürütme (çoğu çevrimdışı parti sonuçlarıdır).
  实时流式推理 (Büyük çoğunlukla çevrimiçi bir toplama önerisi)

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音、背景噪音、远场拾音、多人说话等──Siri、Alexa、小爱同学等产品都投入了大量工程优化解决这些长尾问题──实时性要求──<300ms 延迟) 语音产品的核心指标──

> **【拓展：多语言语音技术】**Küresel dillerin ses özellikleri büyük bir fark: sesli dillerin sesli taşımacılığı, düşük kaynaklı dillerin eğitim verisi yok. Meta'nın MMS modeli 1000'den fazla dilin sesli tanıma, fısıltıcı bir şekilde çok dil ortamında performansı göstermektedir, ancak hala belirli dillere yönelik küçük değişiklikler gerekir.




## Yapın.
```figure
v4-alm-tokens
```

## Yapın

### Adım 1: Qwen2.5-Omni sorgu

```python
from transformers import AutoModelForCausalLM, AutoProcessor

processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-Omni-7B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-Omni-7B", torch_dtype="auto")

audio, sr = load_wav("clip.wav", sr=16000)
messages = [{
    "role": "user",
    "content": [
        {"type": "audio", "audio": audio},
        {"type": "text", "text": "What sounds do you hear, and what's happening?"},
    ],
}]
inputs = processor.apply_chat_template(messages, tokenize=True, return_tensors="pt")
output = model.generate(**inputs, max_new_tokens=200)
print(processor.decode(output[0], skip_special_tokens=True))
```

### Adım 2: Projector örneği

```python
import torch.nn as nn

class AudioProjector(nn.Module):
    def __init__(self, audio_dim=1280, llm_dim=4096):
        super().__init__()
        self.down = nn.Linear(audio_dim, llm_dim)
        self.act = nn.GELU()
        self.up = nn.Linear(llm_dim, llm_dim)

    def forward(self, audio_features):
        return self.up(self.act(self.down(audio_features)))
```

Bu projector genellikle 1-3 doğrusal katman. ASR çiftlerinde eğitmek (audio → transkript) 1. aşama bahane görevi.

### Adım 3: MMAU / LongAudioBench karşılaştırma

```python
from datasets import load_dataset
mmau = load_dataset("MMAU/MMAU-Pro")

correct = 0
for item in mmau["test"]:
    answer = call_model(item["audio"], item["question"], item["choices"])
    if answer == item["correct_choice"]:
        correct += 1
print(f"Accuracy: {correct / len(mmau['test']):.3f}")
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


Kategori başına (söz / ses / müzik / çok sesli) ayrı rapor edin.




> **【拓展：语音与情感计算】**语音 sadece yazılı bilgiyi aktarmakla kalmaz, aynı zamanda bol miktarda duygusal sinyal taşır. 语调、语速、音高变化) 情感语音识别 (His speech Emotion Recognition, SER) 客服质检,心理健康监测,智能教育等 alanlarda yaygın olarak uygulanmaktadır.

## Çerçeveyi kullanın.

| Task | 2026 pick |
|------|-----------|
| Free-form audio QA (open) | Qwen2.5-Omni-7B |
| Best open on long audio | Audio Flamingo Next |
| Best closed | Gemini 2.5 Pro |
| Voice-in / voice-out agent | Qwen2.5-Omni or GPT-4o Audio |
| Music reasoning | Audio Flamingo 3 or 2 (music-specialized AF-CLAP) |
| Call-center audit | Gemini 2.5 Pro via API, with RAG over your policy docs |

| 任务 | 2026 年选择 |
|------|-----------|
| 自由格式音频 QA（开源） | Qwen2.5-Omni-7B |
| 最佳开源长音频 | Audio Flamingo Next |
| 最佳闭源 | Gemini 2.5 Pro |
| 语音入/语音出智能体 | Qwen2.5-Omni 或 GPT-4o Audio |
| 音乐推理 | Audio Flamingo 3 或 2（音乐专用 AF-CLAP） |
| 呼叫中心审计 | Gemini 2.5 Pro via API，配合策略文档 RAG |



## Tuzaklar

> 常见陷

- **Over-trust on multi-audio.**Göreviniz "Hangi klip X'ye sahip" gereksinimindedirse, rastgele şans düzeyinde performans gerçek olur.
  **过度信任多音频。**Eğer göreviniz "Hapi bölümde X" varsa, o zaman yüzey performans gerçekçi olacaktır.
- **Long-audio degradation.**Son 10 dakika, çoğu modelin hoparlör atributları bozulur. Önce diary'yi (Disim 6), sonra özetle.
  **长音频退化。**超过 10 分钟,大多数模型的说话人归因失效──先做日志化(第 6 课),再总结──
- **Hallucinations on silence.**Aynı Whisper'ın şifresini kullanan LALM'ler tarafından miras alınan Whisper-style sorun.
  **静音上的幻觉。**Whisper 编码器'ın LALM 继承的 Whisper 式问题与相同──用 VAD 过──
- **Benchmark cherry-picking.**Satıcı blog yayınları en iyi durum kategorilerini vurguluyor.
  **基准挑挑拣拣。**供应商博客文章突出最佳类别──自己运行 MMAU-Pro 多音频子集──

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-alm-picker.md`. Verilen ses anlama görevi için LALM + referans alt kümesi + çıkış modalitesi (söz karşılığı metin) seçin.

> 保存为 `outputs/skill-alm-picker.md`◊ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒  ⇒ ⇒ ⇒  ⇒ ⇒         ⇒ ⇒   ⇒ ⇒            ⇒      ⇒                                                    

## Egzersizler.

1. **Easy.**Çık .`code/main.py`Oyuncak projeksiyon örneğini görmek için + (audio-eğlence, metin-token) → çıkış tokenlerinin sahte LALM yönlendirilmesi.
   **简单。**运行  İşlem`code/main.py`查看玩具投影器模式 + 假 LALM 路由(音频嵌入,文本代币)→ 输出代币。
2. **Medium.**100 MMAU-Pro konuşma öğesi üzerinde Qwen2.5 Omni-7B puanı alın.
   **中等。**100 MMAU-Pro 语音项上评 Qwen2.5-Omni-7B──与论文报告的数字比较──
3. **Hard.**Minimum bir ses başlıklı bir temel oluşturun: BEATs kodlayıcı + 2 katmanlı projektor + dondurulmuş Llama-3.2-1B. Sadece AudioCaps'taki projektoru ince ayarlayın. Clotho-AQA'daki SALMONN ile karşılaştırın.
   **困难。**构建最小音频标注基线:BEATs 编码器 + 2层投影器 + 结 Llama-3.2-1B──仅在AudioCaps 上微调投影器──在Clotho-AQA 上与SALMONN 比较──

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| LALM | Audio ChatGPT | Audio encoder + projector + LLM decoder. |
| Projector | Adapter | Small MLP mapping audio features into LLM embedding space. |
| MMAU | The benchmark | 10k audio-QA pairs across speech, sound, music. |
| MMAU-Pro | Harder MMAU | 1800 multi-audio / reasoning-heavy questions. |
| LongAudioBench | Long-form eval | Multi-minute clips with semantic queries. |
| Voice-in / voice-out | Speech-native | Model ingests speech and emits speech without text detour. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| LALM | 音频 ChatGPT | 音频编码器 + 投影器 + LLM 解码器。 |
| 投影器 | 适配器 | 将音频特征映射到 LLM 嵌入空间的小型 MLP。 |
| MMAU | 那个基准 | 跨语音、声音、音乐的 1 万音频-QA 对。 |
| MMAU-Pro | 更难的 MMAU | 1800 个多音频/重推理问题。 |
| LongAudioBench | 长音频评估 | 带语义查询的多分钟片段。 |
| 语音入/语音出 | 原生语音 | 模型直接接收和输出语音，不经文本。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Chu et al. (2024). Qwen2-Audio](https://arxiv.org/abs/2407.10759)Referans mimarisi.
  Çu 等 (2024). Qwen2-Audio 参考架构──
- [Alibaba (2025). Qwen2.5-Omni](https://huggingface.co/Qwen/Qwen2.5-Omni-7B)- Konuşma-söz-söz.
  Alibaba (2025). Qwen2.5-Omni语音入语音出。
- [NVIDIA (2025). Audio Flamingo 3](https://arxiv.org/abs/2507.08128) açık uzun sesli lider.
  NVIDIA (2025). Audio Flamingo 3开源长音频领先者──
- [NVIDIA (2026). Audio Flamingo Next](https://arxiv.org/abs/2604.10905) LongAudioBench SOTA.
  NVIDIA (2026). Audio Flamingo NextLongAudioBench SOTA。
- [Tang et al. (2023). SALMONN](https://arxiv.org/abs/2310.13289) çift kodlayıcı öncü.
  Tang 等 (2023). SALMONN双编码器先驱──
- [MMAU-Pro leaderboard](https://mmaubenchmark.github.io/) 2026'da canlı sıralamalar.
  MMAU-Pro 排行榜2026年实时排名──

> **【中文解读】**延伸阅读, inceleme için yüksek kaliteli kaynaklar sunmaktadır, eleştirel okuma için temel makale olarak seçilen, öncelikli okuma önerileri içerir.

