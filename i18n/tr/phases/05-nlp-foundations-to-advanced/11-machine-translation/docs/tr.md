# Makine çevirisi Makine çevirisi

> Tercüme otuz yıldır NLP araştırmasına ödeyen ve şimdi de ödeyen bir görevdir.
> 翻译是为NLP研究买单三十年的任务,现在仍在继续──

> **【中文解读】**统计机器翻译到神经机器翻译──现代用变压器──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## Sorunlar. Sorunlar.

Bir model bir dilde bir cümle okuyor ve bir cümleyi bir başka dilde üretir. Uzunluk değişir. Kelimeler sırası değişir. Bazı kaynak kelimeleri birden fazla hedef kelimeyi haritası yapar ve tersine. İdiomlar birbir haritasını reddeder. Fransızca'da "Seni özlüyorum" kelimesi "tu me manques"  kelimenin anlamı "benim için eksiksin".
> 模型读取一种语言的句子并产生另一种语言的句子──长度不同──词序不同──一些源词映射到多个目标词,反之亦然──习语拒绝对一映射──"Seni özlüyorum" Fransızca dilinde "Sen beni özledin"  字面意思是"你对我是缺失的"──没有词级对齐能经受住这个──

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.


Makine çevirisi, NLP'yi kodlayıcı-dekodörler, dikkat, dönüştürücüler ve sonunda tüm LLM paradigmasını icat etmeye zorlayan görevdir.
> 机器翻译是迫使NLP 发明编码器-解码器、注意力、Transformer以及最终整个LLM 范式的任务──每一步前进都是因为翻译质量可测量且人与机器之间的差固──

Bu ders tarih dersini atlıyor ve 2026'ın çalışma hattını öğretir: önceden eğitilmiş çok dilli kodlayıcı-dekoder (NLLB-200 veya mBART), alt sözcük işaretleme, ışın araması, BLEU ve chrF değerlendirme ve hala üretime ulaşmamış olan bir avuç başarısızlık modunu.
> Bu ders, profesör 2026 yılının çalışma akışları: 预训练多语言编码器-解码器(NLLB-200 veya mBART) 、子词分词、束搜索、BLEU 和 chrF 评估,以及少数仍将逃过检查进入生产的失败模式──

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![MT pipeline: tokenize → encode → decode with attention → detokenize](../assets/mt-pipeline.svg)
> ![MT 流水线：分词 → 编码 → 带注意力的解码 → 去分词](../assets/mt-pipeline.svg)

Modern MT, paralel metinde eğitimli bir transformer kodlayıcı-dekodördür. Kodlayıcı kaynağı dilinin işaretlemesinde okuyor. Dekoder, hedefi, bir kez bir alt kelimeyi, çapraz dikkat yoluyla kodlayıcıın çıkışını kullanarak üretir (dersi 10). Dekodlama açgözlülükle dekodlama tuzağını önlemek için ışın araması kullanır. Çıkış detokenize edilir, yok edilir ve bir referans karşı puanlanır.
> Modern MT, sıradan metin üzerinde eğitim alan bir Transformer 编码器-解码器──编码器以其语言分词读取源语言──解码器通过交叉注意力(第 10 课) kodlayıcı kullanılarak, her seferinde bir sözcük oluşturur hedef dili──解码使用束搜索避免贪心解码陷──输出经过分词、去真实大小写处理,并与参考评分──

Üç operasyonel seçenek gerçek dünya MT kalitesini güçlendirir.
> Üç operasyon seçeneği gerçek dünyanın MT 質量¬¬

- **Tokenizer.**SentencePiece BPE, karışık diller kurpusunda eğitim almıştır.
- **Model size.**NLLB-200 destilli 600M bir dizüstü bilgisayarına uygundur. NLLB-200 3.3B yayınlanan üretim standartıdır. 54.5B araştırma tavanıdır.
- **Decoding.**Genel içerik için ışın genişliği 4-5 uzunluk cezası çok kısa çıkış önlemek için. Terminoloji tutarlılığına ihtiyaç duyduğunuzda kısıtlı kodlama.
> - **分词器。**Bu nedenle, bu programın temelinde, "Blended Language Language Language" (BİL) ve "BİL" (BİL) üyeleri bulunmaktadır.
- **模型大小。**NLLB-200 蒸 600M 适合笔记本。NLLB-200 3.3B is published in production默认。54.5B is研究天花板。
- **解码。**Genel kullanımı içeriği束宽度 4-5。长度惩罚避免输出过短──需要术语一致性时使用束解码──

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.


## Yapın.
```figure
seq2seq-alignment
```

## Yapın

### Adım 1: önceden eğitilmiş MT çağrısı
> Üç şey çok önemli.`src_lang`告诉分词器使用哪种文字和分割──`forced_bos_token_id`告诉解码器生成哪种语言──两者都是NLLB特有的技巧;mBART 和 M2M-100 使用各自的约定,不可交换──

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_id = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(model_id, src_lang="eng_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

src = "The cats are running."
inputs = tok(src, return_tensors="pt")

out = model.generate(
    **inputs,
    forced_bos_token_id=tok.convert_tokens_to_ids("fra_Latn"),
    num_beams=5,
    length_penalty=1.0,
    max_new_tokens=64,
)
print(tok.batch_decode(out, skip_special_tokens=True)[0])
```

```text
Les chats courent.
```

Burada önemli olan üç şey var.`src_lang`Tokenizer'e hangi senaryo ve bölümlemeyi uygulayacağını söyler. `forced_bos_token_id`Bu iki yöntem de NLLB özel numaralardır; mBART ve M2M-100 kendi geleneklerini kullanır ve birbirlerini değiştiremezler.
> BLEU 測定输出与参考之间的 n-gram 重叠──四种参考 n-gram 大小(1-4),精确率的几何平均,对过短输出的简洁惩罚──分数在 [0, 100]──常用但难解读:30 BLEU 是"可用";40 是"好";50 是"出色";1 BLEU 以内差异是噪声──

### Adım 2: BLEU ve chrF
> chrF  ölçüm karakterleri sınıf F 分数── BLEU 低估匹配的形态丰富语言更敏感──通常与BLEU 一起报告──

BLEU, çıkış ve referans arasında n-gram örtüşmeyi ölçer. Dört referans n-gram boyutu (1-4), hassaslıkların geometrik ortalaması, çok kısa çıkış için kısalık cezası. Not [0, 100]'de bulunur. Genel olarak kullanılır. Tercüme için sinir bozucu: 30 BLEU "kullanılabilir"; 40 "iyi"; 50 "istifadedir"; 1 BLEU'dan aşağıdaki farklılıklar gürültüdür.
> 始终使用 `sacrebleu`︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎

chrF karakter seviyesindeki F puanını ölçer. BLEU'nun az sayısının eşleşmesi olan morfolojik olarak zengin dillere daha duyarlı.
> Modern MT 评估 သုံး互补的标标族──至少两发行──

```python
import sacrebleu

hypotheses = ["Les chats courent."]
references = [["Les chats courent."]]

bleu = sacrebleu.corpus_bleu(hypotheses, references)
chrf = sacrebleu.corpus_chrf(hypotheses, references)
print(f"BLEU: {bleu.score:.1f}  chrF: {chrf.score:.1f}")
```

Her zaman kullan `sacrebleu`Bu, işaretlenmeyi normalleştirir, böylece puanlar makaleler arasında karşılaştırılabilir.
> - **启发式**(BLEU、chrF)──快速、基于参考、可解释、对释义不敏感──用于遗留比较和归检测──
- **学习型**(COMET、BLEURT、BERTScore) ◊ İnsan yargılarında eğitimli sinir modeli; ◊Comparation translation with source and reference of meaning similarity──COMET 2023 yılından beri MT araştırma ile bağlantılı en yüksek, 2026 yılı kalitesi önemli üretim standart seçimi ◊
- **LLM 评委**(referanssız)  Özet Büyük Model 流性、充分性、语调和文化適性上 訳打分── GPT-4 评委 评分标准设计良好时与人类一致性约80%──用于没有参考的开放内容──

### Üç katlı değerlendirme hiyerarşisi (2026)
> 2026 yıl:`sacrebleu`BLEU ve chrF için kullanılır.`unbabel-comet`COMET, LLM, insanlığa yönelik son sinyaller için kullanılır.

Modern MT değerlendirmesi, üç tamamlayıcı metrik ailesi kullanıyor.
> 无参考指标(COMET-QE、BLEURT-QE、LLM 评委) 让你在没有参考的情况下评估翻译, this对不存在参考翻译的长尾语言对很重要──

- **Heuristic**Hızlı, referans tabanlı, yorumlanabilir, parafraseye duyarsız.
- **Learned**(COMET, BLEURT, BERTScore). İnsan yargılarına dayanan sinirsel modeller; kaynak ve referans ile çeviri semantik benzerliğini karşılaştırın. COMET 2023'ten beri MT araştırmalarıyla en yüksek ilişkiye sahiptir ve kalite konularında 2026 üretim standartıdır.
- **LLM-as-judge**(referanssız) Büyük bir model oluşturarak tercümanların akıcılık, yeterlilik, ton, kültürel uygunluk konusunda puanlarını alıntılayın.
> Yukarıdaki iş akışı %80'i başarısızlık modüsü olarak adlandırılır.

Pratik 2026 yığın: `sacrebleu`BLEU ve chrF için, `unbabel-comet`COMET için, ve son insan yüzlü sinyal için uyarılmış bir LLM.
> - **幻觉。**模型发明源中没有的内容──在不熟的领域词汇中常见──症状:输出流但声称源没有陈述的事实──缓解: alan terminologies'in kısıtlamaları çözülmesi, denetim altındaki içeriğe yönelik işgücü inceleme, denetim çıkışı, girişten çok daha uzun bir anormallık──
- **偏离目标语言生成。**模型翻译成错误的语言――NLLB 在罕见语言对上出奇地易出错――缓解:验证`forced_bos_token_id`Hiç kullanılmadı dil tanımlama modeli kontrol çıkışı
- **术语漂移。**"Ask up" olarak "s'inscribe" olarak, "creer un compte" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" veya "değildin" olarak, "değildin" olarak, "değildin" veya "değildin" olarak, "değildin" olarak, "değildin" veya "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin" olarak, "değildin "değildin" olarak, "değildin" olarak, "değildin "değildin" olarak, "değildin "değil, "değil, "değil, "değil, "değil, "de" veya "değil, "değil, "değil, "de" olarak, "değil, "değil, "değil" olarak, "de" olarak, "değil, "değil" olarak, "değil, "de" olarak, "de" olarak, "değil, "de" olarak, "de" olarak, "değ" olarak, "değ" olarak, "değ" olarak, "de" olarak, "de" olarak, "de" olarak, "de" olarak, "değ" olarak, "de" olarak, "de
- **语体不匹配。**Fransızca "tu" vs "vous", japonca 敬语级别。 model seçimi eğitimi içinde daha sık görülen biçim。 Müşteriye yönelik içeriğe göre, bu genellikle yanlışlıktır。
- **短输入长度爆炸。**非常短的输入句子经常产生过长的翻译,因为长度惩罚在约5源代币下面急剧下降──缓解:与源长率比例硬最大长度上限──

Referanssız ölçümler (COMET-QE, BLEURT-QE, LLM-as-judge) referanssız tercümeyi değerlendirmenize olanak sağlar. Referans tercüme bulunmayan uzun kuyruğu dil çiftleri için bu önemlidir.
> 预训模型是通才;;法律、医疗或游戏对话

### Adım 3: Üretimdeki bozukluklar
>  birkaç bin yüksek kaliteli düz örnek yüz binlerce gürültü ağı örnek alıyor  Trainer veri kalitesi en büyük üretim 杆

Yukarıdaki çalışma boru hattı zamanın %80'ini akıcı olarak tercüme eder ve kalan %20'i sessizce başarısız eder.

- **Hallucination.**Model, kaynağa ait olmayan içeriği icat eder. Tanınmayan alan sözlüklerinde yaygın. Simptom: çıkış akıcıdır ancak kaynak belirlemediği gerçekleri iddia eder. Yumuşak başlılık: domen terimlerinde kısıtlı dekode, düzenlenmiş içeriğe insan gözden geçirme, çıkış için girişten çok daha uzun bir izleme.
- **Off-target generation.**Model yanlış dile tercüme eder. NLLB nadir dil çiftlerinde şaşırtıcı derecede bu eğilimindedir.`forced_bos_token_id`ve her zaman çıkış kontrolü için dil-ID model ile çözülür.
- **Terminology drift.**"Aygın" dok 1'de "s'inscribe" ve dok 2'de "creer un compte" haline gelir. UI metni ve kullanıcıya yönelik dizileri için, tutarlılık ham kaliteden daha önemlidir.
- **Formality mismatch.**Fransızca "tu" vs. "vous", Japon kibarlık seviyeleri. Model eğitimde daha yaygın olan formları seçer. Müşteriye yönelik içerik için bu genellikle yanlışdır. Yumuşaklık: model desteklerse resmilik belirti ile bir önbellek ile hemen uyarın veya sadece resmi korporlarda küçük bir modelyi ince ayarlayın.
- **Length explosion on short input.**Çok kısa giriş cümleleri genellikle uzunluk cezası ~ 5 kaynak jetonunun altında bir uçurumdan düştüğü için uzunluktan fazla çeviriler üretir.

### Adım 4: Bir alan için ince ayarlama

Önceden eğitilmiş modeller genelistlerdir. Hukuki, tıbbi veya oyun diyalog çevirisi, alan paralel veriler üzerinde ince ayarlamalardan ölçülebilir şekilde yararlanır.

```python
from transformers import Trainer, TrainingArguments
from datasets import Dataset

pairs = [
    {"src": "The defendant pleaded guilty.", "tgt": "L'accusé a plaidé coupable."},
]

ds = Dataset.from_list(pairs)


def preprocess(ex):
    return tok(
        ex["src"],
        text_target=ex["tgt"],
        truncation=True,
        max_length=128,
        padding="max_length",
    )


ds = ds.map(preprocess, remove_columns=["src", "tgt"])

args = TrainingArguments(output_dir="out", per_device_train_batch_size=4, num_train_epochs=3, learning_rate=3e-5)
Trainer(model=model, args=args, train_dataset=ds).train()
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


Birkaç bin yüksek kaliteli paralel örnek birkaç yüz bin gürültülü web kazı örneğini yener.


> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

MT için 2026 üretim aşaması:
> 2026 yılı MT 生产技术:

| Use case | Recommended starting point |
|---------|---------------------------|
| Any-to-any, 200 languages | `facebook/nllb-200-distilled-600M` (laptop) or `nllb-200-3.3B` (production) |
| English-centric, high quality, 50 languages | `facebook/mbart-large-50-many-to-many-mmt` |
| Short runs, cheap inference, English-French/German/Spanish | Helsinki-NLP / Marian models |
| Latency-critical browser-side | ONNX-quantized Marian (~50 MB) |
| Maximum quality, willing to pay | GPT-4 / Claude / Gemini with translation prompts |
> Scenari kullanın.
|---------|---------|
| 任意到任意，200 种语言 | `facebook/nllb-200-distilled-600M`（笔记本）或 `nllb-200-3.3B`（生产） |
| 以英语为中心，高质量，50 种语言 | `facebook/mbart-large-50-many-to-many-mmt` |
| 短任务，廉价推理，英语-法语/德语/西班牙语 | Helsinki-NLP / Marian 模型 |
| 延迟敏感的浏览器端 | ONNX 量化的 Marian（约 50 MB） |
| 最高质量，愿意付费 | GPT-4 / Claude / Gemini 配合翻译提示 |

LLM'ler artık 2026'dan itibaren, özellikle dil içerikleri ve uzun bağlamlarda uzman MT modellerini üstlenmektedir.
> 2026 yılına kadar, LLM çok dillerde özellikle dil ve dil içerikleri üzerinde özel MT modellerini aşmıştır.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-mt-evaluator.md`- ...
> 保存为 `outputs/skill-mt-evaluator.md`- ...

```markdown
---
name: mt-evaluator
description: Evaluate a machine translation output for shipping.
version: 1.0.0
phase: 5
lesson: 11
tags: [nlp, translation, evaluation]
---

Given a source text and a candidate translation, output:

1. Automatic score estimate. BLEU and chrF ranges you would expect. State whether a reference is available.
2. Five-point human-verifiable check list: (a) content preservation (no hallucinations), (b) correct language, (c) register / formality match, (d) terminology consistency with glossary if provided, (e) no truncation or length explosion.
3. One domain-specific issue to probe. E.g., for legal: named entities and statute citations. For medical: drug names and dosages. For UI: placeholder variables `{name}`.
4. Confidence flag. "Ship" / "Ship with review" / "Do not ship". Tie to the severity of issues found in step 2.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse to ship a translation without a language-ID check on output. Refuse to evaluate without a reference unless the user explicitly opts in to reference-free scoring (COMET-QE, BLEURT-QE). Flag any content over 1000 tokens as likely needing chunked translation.
```

## Egzersizler.

1. **Easy.**5 cümle İngilizce paragrafını Fransızcaya çevirin ve İngilizceye geri dönün `nllb-200-distilled-600M`Geri dönüş yolculuğunun orijinaline ne kadar yakın olduğunu ölçün.
2. **Medium.** kullanarak çeviri çıkışlarında dil kimliği kontrolü gerçekleştirmek`fasttext lid.176`veya `langdetect`. MT çağrısına entegre olun, böylece hedef dışı nesiller geri dönmeden yakalanır.
3. **Hard.**- Güzel sesli .`nllb-200-distilled-600M`5.500 çiftlik bir alan korpusunda, seçtiğinizde. BLEU'yu ince ayarlama yapmadan önce ve sonrasında uzun süren bir set üzerinde ölçün. Hangi cümle türlerinin daha iyi olup, hangileri geriye döndüğünü bildirin.
> 1. **简单。**Kullanım`nllb-200-distilled-600M`将 5 句英语段落翻译成法语再翻回英语──测量往返与原文的接近程度──你应该看到语义保留但用词漂移──
2. **中等。**Kullanım`fasttext lid.176`Ya da`langdetect`实现翻译输出的语言识别检查──集成到MT调用中,在返回前捕获偏离目标语言的生成──
3. **困难。**Seçtiğiniz 5000 alan dilini inceleme`nllb-200-distilled-600M`◊ ölçüm biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊ gösterim biçimleri ◊

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BLEU | Translation score | N-gram precision with brevity penalty. [0, 100]. |
| chrF | Character F-score | Character-level F-score. More sensitive for morphologically rich languages. |
| NMT | Neural MT | Transformer encoder-decoder trained on parallel text. The 2017+ default. |
| NLLB | No Language Left Behind | Meta's 200-language MT model family. |
| Constrained decoding | Controlled output | Force specific tokens or n-grams to appear / not appear in the output. |
| Hallucination | Invented content | Model output that is not supported by the source. |
> # Sözcükler # İnsanlar her zaman söylerdi # Gerçek anlamı #
|------|-----------|---------|
| BLEU | 翻译分数 | 带简洁惩罚的 n-gram 精确率。[0, 100]。 |
| chrF | 字符 F 分数 | 字符级 F 分数。对形态丰富语言更敏感。 |
| NMT | 神经机器翻译 | 在平行文本上训练的 Transformer 编码器-解码器。2017+ 的默认。 |
| NLLB | No Language Left Behind | Meta 的 200 语言 MT 模型系列。 |
| 约束解码 | 控制输出 | 强制特定 token 或 n-gram 出现/不出现在输出中。 |
| 幻觉 | 发明内容 | 模型输出中不被源支持的内容。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672)NLLB makalesini.
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/)Neden ?`sacrebleu`BLEU'yu bildirmenin tek doğru yolu.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) chrF kağıdı.
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) pratik ince ayarlama yürüyüşü.
> - [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672) NLLB 论文。
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/)Neden ?`sacrebleu`BLEU'nun raporlama için tek doğru yolu budur.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) chrF 论文。
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) 实用微调演练。
