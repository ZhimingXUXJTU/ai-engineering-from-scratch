# تقييم الصوت  WER، MOS، UTMOS، MMAU، FAD، والروابط المفتوحة  音频评估指标

> لا يمكنك شحن ما لا يمكنك قياسه. هذه الدروس تسمي المقاييس 2026 لكل مهمة صوتية: ASR (WER، CER، RTFx) ، TTS (MOS، UTMOS، SECS، WER-on-ASR-round-trip) ، لغة الصوت (MMAU، LongAudioBench) ، الموسيقى (FAD، CLAP) ، والمتحدث (EER). بالإضافة إلى لوحة القيادة التي يمكنك مقارنة.

> **【中文解读】**无法度量就无法交付──本课列出 2026年所有音频任务的评估指标:ASR 用 WER(词错率) ✓ TTS 用 MOS(平均意见分) ✓ 音频语言模型用 MMAU、音乐用 FAD、说话人识别用 EER──还有对比排行榜──

> **【拓展：WER 是语音识别的黄金指标】**WER(معدل خطأ الكلمة، كلمة خطأ) = (بدل + حذف +插入) / 总词数── همس كبير v3 在英文上达到 ~5% WER,接近人类水平──中文用 CER(字错率)。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04, 06, 07, 09, 10; Phase 2 · 09 (Model Evaluation) | **前置知识:** 阶段 6 · 04、06、07、09、10；阶段 2 · 09（模型评估）
**Time:** ~60 minutes | **预计用时:** ~60 分钟

## المشكلة المشكلة المشكلة

كل مهمة صوتية لديها مقاييس متعددة، كل قياس محور مختلف. باستخدام المقياس الخاطئ هو كيفية شحن نموذج يبدو رائعا على لوحة التحكم الخاص بك و رهيبة في الإنتاج. قائمة 2026 القنوني:

> كل مهمة صوتية لها العديد من المؤشرات، كل مؤشرات تقيس مختلف الأبعاد.

> **【中文解读】**السؤال الذي يطرحه هذا القسم هو: كيف يمكن فهم هذه التقنية بشكل صحيح وتطبيقها في التجهيز العملي. فهم السياق يساعد على فهم النوع المختص من التكنولوجيا. في النظام الواقعي الذكاء الاصطناعي، فإن التكنولوجيا الخطأ غالباً ما تكون أكثر تكلفة من التنفيذ التفصيلي.


| Task | Primary | Secondary |
|------|---------|-----------|
| ASR | WER | CER · RTFx · first-token latency |
| TTS | MOS / UTMOS | SECS · WER-on-ASR-round-trip · CER · TTFA |
| Voice cloning | SECS (ECAPA cosine) | MOS · CER |
| Speaker verification | EER | minDCF · FAR / FRR at operating point |
| Diarization | DER | JER · speaker confusion |
| Audio classification | top-1 · mAP | macro F1 · per-class recall |
| Music generation | FAD | CLAP · listening panel MOS |
| Audio language model | MMAU-Pro | LongAudioBench · AudioCaps FENSE |
| Streaming S2S | latency P50/P95 | WER · MOS |

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.


## المفهوم الأساسي

![Audio evaluation matrix — metrics vs tasks vs 2026 leaderboards](../assets/eval-landscape.svg)

### مقاييس ASR

> مؤشر تقييم ASR

**WER (Word Error Rate).** `(S + D + I) / N`الحروف الصغرى، التخطيط، التطبيع على الأرقام قبل تسجيل النقاط`jiwer`أو شركة OpenAI`whisper_normalizer`. &lt;5% = قراءة الكلام على قدم المساواة البشرية

> **WER（词错率）。** `(替换 + 删除 + 插入) / 总词数`◊评分前需转小写、除标点、标准化数字──使用 `jiwer`أو OpenAI `whisper_normalizer`❖ أقل من 5% = 朗读语音的人类水平。

**CER (Character Error Rate).**نفس الصيغة، مستوى الأحرف. تستخدم لغات النغمات (الماندرين، الكانتوني) حيث التقسيم الكليمي غير واضح.

> **CER（字错率）。**相同公式,字符级别──用于声调语言(普通话、语),因为词分类 不明确──

**RTFx (inverse real-time factor).**ثواني صوتية معالجة لكل ثانية من ساعة الحائط أعلى أفضل، تصل درجات Parakeet-TDT إلى 3380×

> **RTFx（逆实时因子）。**كل ثانية عملية من الصوت الثانية.

**First-token latency.**ساعة الحائط من إدخال الصوت إلى أول رمز النسخة حرجة للتسجيل

> **首 token 延迟。**من الصوت النقل إلى أول ترميز رمز الوقت الحقيقي.

### مقاييس TTS

> TTS 评估指标

**MOS (Mean Opinion Score).**1-5 تصنيف بشري، معيار الذهب لكن بطيء، جمع أكثر من 20 سمعًا لكل عينة، أكثر من 100 عينة لكل نموذج.

> **MOS（平均意见分）。**1-5 分人工评分──黄金标准但速度慢── كل نموذج جمع 20+ 听者, كل نموذج 100+ 样本──

**UTMOS (2022-2026).**علمت توقعات MOS. تتوافق مع MOS البشري عند المعايير القياسية. F5-TTS: UTMOS 3.95; الحقيقة الأرضية: 4.08.

> **UTMOS（2022-2026）。**学习型 MOS 预测器──在标准基准上与人类 MOS 相关性约0.9──F5-TTS:UTMOS 3.95;真实值:4.08──

**SECS (Speaker Encoder Cosine Similarity).**للتنسيق الصوتي. إيكابا تضمين كوسين بين الإشارة والإنتاج المنسق. &gt; 0.75 = نسخة قابلة للتعرف.

> **SECS（说话人编码器余弦相似度）。**تستخدم لغة كلون. استناد إلى الصوت والإصدار الكلون.

**WER-on-ASR-round-trip.**تشغيل Whisper على إصدار TTS، حساب WER ضد النص المدخل. يلتقط تراجعات التفاهم. 2026 SOTA: &lt; 2% CER.

> **WER-on-ASR-round-trip（ASR 回环 WER）。**على TTS 输出运行                                                                                                                                                                                                                                                           

**TTFA (time-to-first-audio).**تأخير الساعة الجدارية كوكورو-82م: ~100 ms F5-TTS: ~1 ثانية

> **TTFA（首个音频时间）。**实际延迟──Kokoro-82M: حوالي 100 ms;F5-TTS: حوالي 1 ثانية──

### خاصة في عملية استنسخ الصوت

> 语音克隆专用标志

**SECS + MOS + CER**إن التنسيق الذي يحصل على درجة عالية من الـ SECS ولكن منخفضة من MOS يعني الـ timbre-right-but-unnatural؛ والعكس يعني صوت طبيعي ولكن المتحدث الخطأ.

> **SECS + MOS + CER**كثلاثة مؤشرات: الكلون مرتفع في SECS ولكن MOS المنخفضة تعني الصوت صحيح ولكن غير طبيعي.

### التحقق من المتحدث

> يقولون:

**EER (Equal Error Rate).**الحد الأدنى حيث يبلغ معدل قبول كاذب معدل رفض كاذب. ECAPA على VoxCeleb1-O: 0.87%.

> **EER（等错误率）。** خطأ قبول معدل = خطأ رفض معدل                                                                                                                                                                                                                                                          

**minDCF (min Detection Cost).**تكلفة معينة في نقطة تشغيل مختارة (غالباً ما تكون FAR = 0.01).

> **minDCF（最小检测代价）。**في نقطة العمل المحددة (معظمها FAR=0.01) زيادة السلطة تكلفة العمل.

### الإسهال

> 说话人日志指标

**DER (Diarization Error Rate).** `(FA + Miss + Confusion) / total_speaker_time`. كلمة مفقودة + كلمة إنذار خاطئ + مكبر صوت-خلط ، كل منها كجزء. اجتماعات AMI: DER ~ 10-20% هو واقعي. بيانوت 3.1 + دقة-2 الإعلانية: &lt;10% DER على الصوت المسجل جيدًا.

> **DER（说话人日志错误率）。** `(虚警 + 漏检 + 混淆) / 总说话时间` التحقق من语音 + 虚警语音 + 说话人混,各占比例──AMI 会议:DER 约 10-20% 是现实水平──piannote 3.1 + Precision-2 商业版:在良好录音上 DER 低于10%──

**JER (Jaccard Error Rate).**بديل لـ DER، قوية لـ short-segment bias.

> **JER（Jaccard 错误率）。**البديل لـ DER، على الاختلافات القصيرة

### تصنيف الصوت

> 音频分类标志

متعددة العلامات: **mAP (mean Average Precision)**على جميع الفئات. مجموعة صوتية: 0.548 ماب لـ BEATs-iter3.

> 多标签:**mAP（平均精度均值）**, تغطي جميع الفئات.

حصرية متعددة الفئات: **top-1, top-5 accuracy**. أوامر الكلام v2: 99.0% أعلى 1 (صوت-MAE).

> العديد من التداولات:**top-1、top-5 准确率**❖ أوامر الكلام v2:99.0% أعلى-1

غير متوازن: **macro F1**+ **per-class recall**. تقرير لكل فئة  الدقة الإجمالية تخفي فئات الفئة الفاشلة.

> عدم توازن البيانات:**macro F1**+ **每类召回率** تقرير الفئات معدل التأكد العام سوف يغطي أي فئات فشلت

### جيل الموسيقى

> 音乐生成指标

**FAD (Fréchet Audio Distance).**المسافة بين توزيعات VGGish المدمجة من الصوت الحقيقي مقابل الصوت المولد. MusicGen-small على MusicCaps: 4.5 . MusicLM: 4.0. أقل أفضل.

> **FAD（Fréchet 音频距离）。**الفاصل بين الموسيقى والإنتاج الصوتي.

**CLAP Score.**درجة التنظيم النصي-الصوتي باستخدام إدمجات CLAP. &gt; 0.3 = التنظيم المعقول.

> **CLAP 分数。**استخدام CLAP 嵌入文本音频对齐分数──大于0.3 = 合理对齐──

**Listening panel MOS.**لا يزال الكلمة الأخيرة للموسيقى المستهلكة. سونو v5 ELO 1293 على TTS Arena (من تفضيلات الإنسان المزدوجة).

> **听音评审团 MOS。**لا يزال هذا هو المقياس النهائي للموسيقى المستهلكة.

### معايير اللغة الصوتية

> 音频语言基准测试

**MMAU (Massive Multi-Audio Understanding).**10 ألف زوج صوتي

> **MMAU（大规模多音频理解）。**10000 صوتية

**MMAU-Pro.**1800 عنصر صلب، أربعة فئات: الكلام / الصوت / الموسيقى / متعددة الصوت. فرصة عشوائية 25% على 4 طريق. جيميني 2.5 برو عموما ~ 60%؛ متعددة الصوت ~ 22% على جميع الطرازات.

> **MMAU-Pro。**1800 个难题,四个类别:语音/声音/音乐/多音频──4 选 1 随机猜测 25%──Gemini 2.5 Pro 整体约60%;所有模型在多音频上约22%.──

**LongAudioBench.**مقاطع متعددة الدقائق مع استفسارات معنوية صوت فلامينغو التالي يضرب جيميني 2.5 برو

> **LongAudioBench。**ربما钟音频片段 + 语义查询──Audio Flamingo Next 超过 Gemini 2.5 Pro──

**AudioCaps / Clotho.**إعادة تعريف المعايير المرجعية، معايير SPICE، CIDER، FENSE.

> **AudioCaps / Clotho。**音频描述基准测试──SPICE、CIDER、FENSE 指标──

### التدفق من حديث إلى حديث

> 流式语音 إلى 语音指标

**Latency P50 / P95 / P99.**ساعة الحائط من نهاية المستخدم إلى الاستجابة السمعة الأولى.

> **延迟 P50 / P95 / P99。**من المستخدم صوت انتهى إلى أول وقت قابل للصوت للرد فعل.

**WER / MOS**على الخروج

>  الخروج على **WER / MOS**.

**Barge-in responsiveness.**وقت من توقف المستخدم إلى مساعد صامت الهدف 150 ثانية

> **打断响应时间。**من المستخدم إلى المساعد وقت الصوت. الهدف أقل من 150 ms.

### قائمة اللائحة لعام 2026

| Leaderboard | Tracks | URL |
|------------|--------|-----|
| Open ASR Leaderboard (HF) / 开源 ASR 排行榜（HF） | English + multilingual + long-form / 英语 + 多语言 + 长音频 | `huggingface.co/spaces/hf-audio/open_asr_leaderboard` |
| TTS Arena (HF) / TTS 竞技场（HF） | English TTS / 英语 TTS | `huggingface.co/spaces/TTS-AGI/TTS-Arena` |
| Artificial Analysis Speech / Artificial Analysis 语音 | TTS + STT, ELO from paired votes / TTS + STT，配对投票 ELO | `artificialanalysis.ai/speech` |
| MMAU-Pro / MMAU-Pro | LALM reasoning / LALM 推理 | `mmaubenchmark.github.io` |
| SpeakerBench / VoxSRC / 说话人基准 / VoxSRC | Speaker recognition / 说话人识别 | `voxsrc.github.io` |
| MMAU music subset / MMAU 音乐子集 | Music LALM / 音乐 LALM | （在 MMAU 内） |
| HEAR benchmark / HEAR 基准 | Self-supervised audio / 自监督音频 | `hearbenchmark.com` |

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.

> **【拓展：语音 AI 的产品化】**تقنية الصوت تواجه تحديات فريدة في مجال تصنيع المنتجات: مختلفة النطق، ضوضاء الخلفية، الالتقاط بعيداً، الكثير من الناس يتحدثون، وما إلى ذلك.

> **【拓展：多语言语音技术】**الاختلافات الكبيرة في الاختلافات بين الصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت والصوت.




## بناء ذلك تحرك لتحقيق
```figure
sp-wer-align
```

## بناءها

### الخطوة الأولى: WER مع التطبيع

> الخطوة الأولى: إصلاح المعدات المعتمدة

```python
from jiwer import wer, Compose, ToLowerCase, RemovePunctuation, Strip

transform = Compose([ToLowerCase(), RemovePunctuation(), Strip()])
score = wer(
    truth="Please turn on the lights.",
    hypothesis="please turn on the light",
    truth_transform=transform,
    hypothesis_transform=transform,
)
# ~0.17
```

### الخطوة الثانية: TTS WER ذهاب وإياب

> 步骤 2:TTS 回环 WER

```python
def ttr_wer(tts_model, asr_model, texts):
    errors = []
    for txt in texts:
        audio = tts_model.synthesize(txt)
        recog = asr_model.transcribe(audio)
        errors.append(wer(truth=txt, hypothesis=recog))
    return sum(errors) / len(errors)
```

### الخطوة الثالثة: SECS للتنسخ الصوتي

> 步骤 3:语音克隆的SECS

```python
from speechbrain.inference.speaker import EncoderClassifier
sv = EncoderClassifier.from_hparams("speechbrain/spkrec-ecapa-voxceleb")

emb_ref = sv.encode_batch(load_wav("reference.wav"))
emb_clone = sv.encode_batch(load_wav("cloned.wav"))
secs = torch.nn.functional.cosine_similarity(emb_ref, emb_clone, dim=-1).item()
```

### الخطوة الرابعة: FAD لتوليد الموسيقى

> الخطوة الرابعة:

```python
from frechet_audio_distance import FrechetAudioDistance
fad = FrechetAudioDistance()
score = fad.get_fad_score("generated_folder/", "reference_folder/")
```

### الخطوة 5: إطار الإطار الإقتصادي للمؤلفين (مثل الرمز الذي يستخدم في الدروس 6)

> الخطوة 5: الكود نفسه للقاعدة البحثية (EER)

```python
def eer(same_scores, diff_scores):
    thresholds = sorted(set(same_scores + diff_scores))
    best = (1.0, 0.0)
    for t in thresholds:
        far = sum(1 for s in diff_scores if s >= t) / len(diff_scores)
        frr = sum(1 for s in same_scores if s < t) / len(same_scores)
        if abs(far - frr) < best[0]:
            best = (abs(far - frr), (far + frr) / 2)
    return best[1]
```

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.





> **【拓展：语音与情感计算】**语音 ليس فقط نقل المعلومات الكلمات، ولكن أيضا تحمل إشارات عاطفية غنية (语调、语速、音高变化)  情感语音识别 (语调、语速、音高变化)  语音情绪识别 (语音识别, SER) في مجالات الاختبار الصحي والصحي والصحي والصحة النفسية والتعليم الذكي وغيرها.

## استخدمها في إطار التنفيذ

إزواج كل عملية نشر مع حزمة تقييم ثابتة التي تعمل على كل تحديث نموذج.

> كل عملية نشر تمت مع أداة تقييم ثابتة، في كل عملية تحديث النموذج.

1. **Normalize before scoring.**الحروف الصغرى، شريط النقاط، رقم التوسع، إبلغ عن قاعدة التطبيع
   中文翻译:**评分前标准化。**转小写、去标点、数字展开――报告标准化规则――
2. **Report distributions, not averages.**P50/P95/P99 للخمول. استدعاء لكل فئة للتصنيف. لكل فئة لـ MMAU.
   中文翻译:**报告分布而非均值。**延迟用P50/P95/P99──分类用每类召回率──MMAU用每类──
3. **Run one canonical public benchmark.**حتى لو كانت بيانات الإنتاج الخاصة بك تختلف، فإن تقرير في Open ASR / TTS Arena / MMAU يسمح للمراجعين بمقارنة التفاح مع التفاح.
   中文翻译:**运行一个权威公共基准。**حتى لو كانت بيانات إنتاجك مختلفة، فإن تقرير في "أسر" المفتوحة / "أرينا" التس/ "مماو" يسمح للمراجعة بمقارنة عادلة.



## الفخاخ

> 常见陷

- **UTMOS extrapolation.**تدرب على الكلام النقي في نمط VCTK؛ تسجل صوت ضجيج / مقترح / عاطفي بشكل سيء.
  中文翻译:**UTMOS 外推问题。**في VCTK 风格 纯净语音上训练;对杂/克隆/情感语音评分效果差──
- **MOS panel bias.**20 عامل في شركة أمازون ميكانيكال تورك ≠ 20 مستخدم هدف. ادفع للوحة النطاق إذا كانت المخاطر مرتفعة.
  中文翻译:**MOS 评审团偏差。**20  Amazon Mechanical Turk 工作者不等于 20 目标用户──如果风险高,花钱请领域专家评审团──
- **FAD depends on reference set.**مقارنة مع نفس التوزيع المرجعي بين النماذج.
  中文翻译:**FAD 依赖参考集。**跨模型比较时使用相同的参考分布──
- **Aggregate WER.**5-% WER بشكل عام يمكن أن تخفي 30٪ WER على الكلام المجهز.
  中文翻译:**汇总 WER。** 5% من WER يمكن أن تغطي  30% من WER  حسب تقرير مجموعة الإحصاءات السكانية
- **Public benchmark saturation.**معظم الطرازات الحدودية قريبة من السقف على مقارنات قياسية. قم ببناء مجموعة محمولة داخلية تعكس حركة المرور الخاصة بك.
  中文翻译:**公共基准饱和。**معظم النماذج المتقدمة على المعدل قد اقتربت من الطابور.

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.


## أرسلها .

إبقوا`outputs/skill-audio-evaluator.md`. اختر المقاييس والمؤشرات المرجعية و تنسيق التقارير لأي إصدار من نماذج الصوت

> 保存为 `outputs/skill-audio-evaluator.md`◊ إصدار مؤشر اختيار لأي نموذج صوتي ✓

## تمارين التدريب

1. **Easy.**أركض`code/main.py`الحساب WER / CER / EER / SECS / FAD-ish / MMAU-ish على مدخلات الألعاب.
   中文翻译:**简单。**运行 `code/main.py` في المعدات输入上 حساب WER / CER / EER / SECS / 类 FAD / 类 MMAU
2. **Medium.**قم ببناء حزمة WER TTS ذهابًا وإياباً. قم بتشغيل إصدارك Kokoro أو F5-TTS من خلال Whisper. احسب WER أكثر من 50 إشارة. إشارات العلم مع WER &gt; 10%.
   中文翻译:**中等。**构建 TTS 回环 WER 评估工具──用 Whisper 处理你的Kokoro 或 F5-TTS 输出──在 50 个提示上计算 WER──标记 WER 大于10% 的提示──
3. **Hard.**قم بتسجيل دروسك في الدروس 10 لـ LALM على الخطاب MMAU-Pro + مجموعة فرعية متعددة الصوت (50 عنصر لكل منها).
   中文翻译:**困难。**في MMAU-Pro's语音 + 多音频子集上 (→ 50 项) تقييم للامحوظات التي تتخذها الدرس في الدرس الـ10 . تقرير معدل التأكد من كل فئة ومقارنة مع البيانات المنشورة .

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.


## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| WER | ASR score | `(S+D+I)/N` at word level after normalization. / 标准化后的词级 `(S+D+I)/N` |
| CER | Character WER | For tone languages or char-level systems. / 用于声调语言或字符级系统 |
| MOS | Human opinion | 1-5 rating; 20+ listeners × 100 samples. / 1-5 分评分；20+ 听者 × 100 样本 |
| UTMOS | ML MOS predictor | Learned model; correlates ~0.9 with human MOS. / 学习型模型；与人类 MOS 相关性约 0.9 |
| SECS | Voice-clone similarity | ECAPA cosine between reference and clone. / 参考与克隆之间的 ECAPA 余弦相似度 |
| EER | Speaker verif score | Threshold where FAR = FRR. / FAR = FRR 的阈值 |
| DER | Diarization score | (FA + Miss + Confusion) / total. / (虚警 + 漏检 + 混淆) / 总时间 |
| FAD | Music-gen quality | Fréchet distance on VGGish embeddings. / VGGish 嵌入上的 Fréchet 距离 |
| RTFx | Throughput | Audio seconds per wall-clock second. / 每实际秒处理的音频秒数 |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.


## المزيد من القراءة

- [jiwer](https://github.com/jitsi/jiwer) مكتبة WER/CER مع أدوات التطبيع.
  المعدات المعتمدة
- [UTMOS (Saeki et al. 2022)](https://arxiv.org/abs/2204.02152)تعلمت مقدرة المعدات النظرية
  UTMOS(Saeki 等 2022) 学习型 MOS 预测器。
- [Fréchet Audio Distance (Kilgour et al. 2019)](https://arxiv.org/abs/1812.08466) معيار الموسيقى
  مسافة صوتية (Fréchet Audio Distance) ((Kilgour 等 2019) 音乐生成的标准指标──
- [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) 2026 ترتيبات حية.
  افتتاح ASR 排行榜2026 实时排名──
- [TTS Arena](https://huggingface.co/spaces/TTS-AGI/TTS-Arena) قائمة التصويت البشري في TTS
  تاتس أرنة الانساني التصويت تاتس 排行榜。
- [MMAU-Pro benchmark](https://mmaubenchmark.github.io/) قائمة التفكير LALM
  المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة المملكة المتحدة
- [HEAR benchmark](https://hearbenchmark.com/) أداء النصوص الخاصة بـ SSL
  الاهتمام بالشخصيات

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق، بما في ذلك المقالات والتدريس والأدوات.

