# Çok dilli NLP

> Bir model, 100+ dil, çoğu için sıfır eğitim verisi. Diller arası transfer 2020'lerin pratik mucizesidir.
> Bir model, 100+ 种语言, çoğu dil 零训练数据――跨语言迁移是2020'lerin pratik mucizesi――

> **【中文解读】**Çok dilli BERT、XLM-R 等模型处理多种语言──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 04 (GloVe, FastText, Subword), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 04（GloVe、FastText、子词），Phase 5 · 11（机器翻译）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

İngilizce milyarlarca etiketli örneğe sahiptir. Urdu binlerce. Maithili neredeyse hiç bir şey. Küresel bir kitleye hizmet eden herhangi bir pratik NLP sistemi görev-özel eğitim verileri olmayan uzun kuyruğu dillerde çalışmalıdır.

> İngilizce milyarlarca işaret örneği vardır. Ülde binlerce vardır.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

Çok dilli modeller, bir modelin birden fazla dilde aynı anda eğitilmesiyle bunu çözer. Paylaşılan temsil, modelin yüksek kaynaklı dillerde öğrenilen becerileri düşük kaynaklı dillere aktarmasına olanak sağlar. İngilizce duygu analizi modelini ince ayarlayın ve bu, şaşırtıcı derecede iyi duygu tahminlerini Urdu dilinde ortaya çıkarır. Bu sıfır çekimli diller arası transfer ve NLP'nin dünyaya nasıl gönderildiğini yeniden şekillendirdi.

> Çok dilli modeller, aynı zamanda birçok dilde bir model eğitimiyle bu sorunu çözmektedir. Paylaşılan ifade, modellerin yüksek kaynaklı dil öğrenme becerilerini düşük kaynaklı dillere taşıyacağını göstermektedir. İngilizce duygusal analizde, bu model, tüm ülkeden şaşırtıcı iyi duygusal bir öngörüm oluşturabilir. Bu, nörelce diller arası göçün, NLP'nin dünyaya yönelik yolunu yeniden şekillendirdiğini göstermektedir.

Bu ders, değişimlerin, kanonik modellerin ve ekiplerin çok dilli çalışmaya yeni başlamasını sağlayan tek kararın adını veriyor: transfer için bir kaynak dili seçmek.

> Bu ders, "Währungsgewicht"", Klasik Model" ve "Bewältigen Mehrsprachige Arbeiten Neue Handler Teams'in Kararları" adlı bir ders içeriyor.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

![Cross-lingual transfer via shared multilingual embedding space](../assets/multilingual.svg)

**Shared vocabulary.**Çok dilli modeller tüm hedef dillerden metin üzerine eğitilmiş bir SentencePiece veya WordPiece işaretleyicisini kullanır. Sözlük paylaşılan: aynı alt kelime birimi ilgili diller arasında aynı morfemi temsil eder. `anti-`İngilizce ve İtalyanca aynı işaret.

> **共享词表。**Çok dilli modeller kullanılır Tüm hedef dil metinlerinde eğitimlenmiş SentencePiece veya WordPiece 分词器──词表是共享的:相同的子词单元在相关语言中表示相同的语素──英语和意大利语的`anti-`Aynı simgeyi elde etmek için.

**Shared representation.**Birçok dilde maskeli dil modelleme konusunda önceden eğitilmiş bir transformer, farklı dillerde semantik olarak benzer cümlelerin benzer gizli durumlar ürettiğini öğrenir. mBERT, XLM-R ve NLLB hepsi bunu gösterir.

> **共享表示。**Çeşitli dillerde kullanılan dilde benzer cümlelerin benzer gizli durumlar ortaya çıkmasını öğrenmek için Transformer'ın hazırlık yapması bunu göstermiştir. İngilizce "cat" yerleşimi Fransızca "chat" ve İspanyolca "gato" ile bir araya gelerek, tam cümle yerleşimi de aynı şekilde görülmektedir.

**Zero-shot transfer.**Model, bir dilde (genellikle İngilizce) etiketlenmiş verilere dayalı modelde ince ayarlama yapın. Sonuç olarak, modelin desteklediği diğer dillerde çalıştırın. Hedef dili etiketlerine ihtiyaç yoktur. Sonuçlar tipolojik olarak ilişkili dillerde güçlüdür ve uzak dillerde daha zayıfdır.

> **零样本迁移。**Bir dilde (öntenlikle İngilizce) etiket verilerinde küçük modeller bulunmaktadır.

**Few-shot fine-tuning.**Hedef dili 100-500 etiketli örnek ekleyin. Düzgünlük sınıflandırma görevleri için İngilizce temel çizginin 95-98%'ine kadar atlar. Bu, çok dilli NLP'de en ekonomik tek kaldıraçtır.

> **少样本微调。**Hedef dillerinde 100-500 işaret örneği eklemek. Sınıf görevlerinde doğruluk oranı İngilizce temelinin %95-98'ine yükseldi.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Modellerin modeli.

| Model / 模型 | Year / 年份 | Coverage / 覆盖 | Notes / 说明 |
|-------|------|----------|-------|
| mBERT | 2018 | 104 languages / 104 种语言 | Trained on Wikipedia. First practical multilingual LM. Weak on low-resource. / 在 Wikipedia 上训练。首个实用多语言 LM。低资源语言较弱。 |
| XLM-R | 2019 | 100 languages / 100 种语言 | Trained on CommonCrawl. Sets the cross-lingual baseline. / 在 CommonCrawl 上训练。设定跨语言基线。 |
| XLM-V | 2023 | 100 languages / 100 种语言 | XLM-R with 1M-token vocabulary. Better on low-resource. / XLM-R 配 1M token 词表。低资源更好。 |
| mT5 | 2020 | 101 languages / 101 种语言 | T5 architecture for multilingual generation. / T5 架构用于多语言生成。 |
| NLLB-200 | 2022 | 200 languages / 200 种语言 | Meta's translation model; includes 55 low-resource languages. / Meta 翻译模型；含 55 种低资源语言。 |
| BLOOM | 2022 | 46 languages + 13 programming / 46 种语言 + 13 种编程语言 | Open 176B LLM trained multilingually. / 开源 176B 多语言 LLM。 |
| Aya-23 | 2024 | 23 languages / 23 种语言 | Cohere's multilingual LLM. Strong on Arabic, Hindi, Swahili. / Cohere 多语言 LLM。阿拉伯语、印地语、斯瓦希里语强。 |

Kullanımsal durumlara göre seçin. Sınıflama akılda kalmış varsayım olarak XLM-R tabanıyla iyi çalışır. Doğruluk görevleri çevirime göre açık nesil için mT5 veya NLLB gerektirir. Açık bir çok dilli istek kullanan Aya-23 veya Claude ile LLM tarzında iş çiftleri.

> 按用例选择──分类任务以 XLM-R-base 作为合理默认──生成任务根据翻译对开放生成选择 mT5 或 NLLB──LLM 风格工作配合 Aya-23 或 Claude 使用显式多语言提示──

## Kaynak dili kararı (2026 araştırma)

Çoğu ekip, ince ayarlama kaynağı olarak İngilizce'yi varsayım olarak kullanır.

> Büyük çoğunluk takımları İngilizce'yi bir inceleme kaynağı olarak kabul ediyor.

Dil benzerliği, transfer kalitesini ham korpus boyutundan daha iyi tahmin eder. Slavic hedefleri için, Almanca veya Rusça genellikle İngilizce'yi yener.**qWALS**Dünya Dil Yapıları Atlası özelliklerine dayanan 2026 benzerlik metrikası bunu ölçüyor. **LANGRANK**(Lin et al., ACL 2019) dil benzerliği, korpus boyutu ve genetik ilişki kombinasyonundan aday kaynak dillerini sıralayan ayrı, daha eski bir yöntemdir.

> 语言相似性原始语料大小更好地预测迁移质量──对于斯拉夫语目标,德语或俄语通常胜英语──对于印度语目标,印度语通常胜英语──**qWALS**Aynı şekilde, bu noktayı 2026'da ölçtü.**LANGRANK**(Lin 等,ACL 2019) Language similarity、语料大小和遗传关系的组合中排名候选源语言──

Uygulanabilir kurallar: Eğer hedef dilizin tipik olarak yakın bir kaynaklı akrabası varsa, önce onu ince ayarlamaya çalışın, sonra İngilizce ince ayarına karşılaştırın.

>  Praktiksel kural: Eğer hedef diliniz tipolojik olarak yakın yüksek kaynaklı bir dil varsa, önce o dilde inceleme yapmaya çalışın, sonra İngilizce ile incelemeyi karşılaştırın.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
n5-crosslingual-bridge
```

## Yapın

### Adım 1: sıfır çekimli diller arası sınıflandırma

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli")
model = AutoModelForSequenceClassification.from_pretrained("joeddav/xlm-roberta-large-xnli")


def classify(text, candidate_labels, hypothesis_template="This text is about {}."):
    scores = {}
    for label in candidate_labels:
        hypothesis = hypothesis_template.format(label)
        inputs = tok(text, hypothesis, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits[0]
        entail_score = torch.softmax(logits, dim=-1)[2].item()
        scores[label] = entail_score
    return dict(sorted(scores.items(), key=lambda x: -x[1]))


print(classify("I love this product!", ["positive", "negative", "neutral"]))
print(classify("मुझे यह उत्पाद पसंद है!", ["positive", "negative", "neutral"]))
print(classify("J'adore ce produit !", ["positive", "negative", "neutral"]))
```

Bir model, üç dil, aynı API. NLI'de eğitimli XLM-R verileri entailment hilesi ile sınıflandırmaya iyi aktarır.

> Bir model, üç dil, aynı API── NLI verileri üzerinde eğitim alan XLM-R  içeren teknikler sayesinde  iyi bir şekilde sınıflara taşınmıştır──

### Adım 2: Çok Dilli Eklentime Alanı

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

pairs = [
    ("The cat is sleeping.", "Le chat dort."),
    ("The cat is sleeping.", "El gato está durmiendo."),
    ("The cat is sleeping.", "Die Katze schläft."),
    ("The cat is sleeping.", "The dog is barking."),
]

for eng, other in pairs:
    emb_eng = model.encode([eng], normalize_embeddings=True)[0]
    emb_other = model.encode([other], normalize_embeddings=True)[0]
    sim = float(np.dot(emb_eng, emb_other))
    print(f"  {eng!r} <-> {other!r}: cos={sim:.3f}")
```

Çevirmeler yerleşim alanında yakındır. Farklı bir İngilizce cümlesi daha da ilerler. Bu, diller arası arama, gruplama ve benzerlik işlevini yapar.

> 翻訳在嵌入空间中距离很近.                                                                                                                                                                                                                                                         

### Adım 3: Birkaç atışlı ince ayarlama stratejisi

```python
from transformers import TrainingArguments, Trainer
from datasets import Dataset


def few_shot_finetune(base_model, base_tokenizer, examples):
    ds = Dataset.from_list(examples)

    def tokenize_fn(ex):
        out = base_tokenizer(ex["text"], truncation=True, max_length=128)
        out["labels"] = ex["label"]
        return out

    ds = ds.map(tokenize_fn)
    args = TrainingArguments(
        output_dir="out",
        per_device_train_batch_size=8,
        num_train_epochs=5,
        learning_rate=2e-5,
        save_strategy="no",
    )
    trainer = Trainer(model=base_model, args=args, train_dataset=ds)
    trainer.train()
    return base_model
```

100-500 hedef dil örneği için, `num_train_epochs=5`ve `learning_rate=2e-5`Yüksek öğrenme oranları, çok dilli uyumluğun çökmesine neden olur ve sadece İngilizce bir model elde edilir.

> 对于100-500 个目标语言样本,`num_train_epochs=5`和 `learning_rate=2e-5`Daha yüksek öğrenme oranı çok dillerin çökmesine neden olur, sadece İngilizce'ye dayalı bir model elde edersiniz.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Gerçekten işe yarayan değerlendirme.

- **Per-language accuracy on held-out sets.**Toplantı uzun kuyruğu saklıyor.
  **每种语言在留出集上的准确率。**Toplanmayın. Toplanın.
- **Benchmark against monolingual baseline.**Yeterince veri olan diller için, sıfırdan eğitilen tek dilli bir model bazen çok dilli olanı yener.
  **与单语基线比较。**DATA YETİNİLERİ için, baştan eğitimli tek dil modeli bazen birden fazla dil modeliyi yener.
- **Entity-level tests.**Çok dilli modeller genellikle Latin'den uzak metinler için zayıf bir işaretlemeye sahiptir.
  **实体级测试。**目標言語中的命名实体──多语言模型对远离拉丁文的书写的分词通常较弱──
- **Cross-lingual consistency.**İki dilde aynı anlam aynı tahmin oluşturmalı.
  **跨语言一致性。**两种语言中相同含义应产生相同预测――测量差──

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

## Çerçeveyi kullanın.

2026'da:

> 2026 yılının teknolojisi:

| Task / 任务 | Recommended / 推荐 |
|-----|-------------|
| Classification, 100 languages / 分类，100 种语言 | XLM-R-base (~270M) fine-tuned / 微调 |
| Zero-shot text classification / 零样本文本分类 | `joeddav/xlm-roberta-large-xnli` |
| Multilingual sentence embeddings / 多语言句子嵌入 | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Translation, 200 languages / 翻译，200 种语言 | `facebook/nllb-200-distilled-600M` |
| Generative multilingual / 生成式多语言 | Claude, GPT-4, Aya-23, mT5-XXL |
| Low-resource language NLP / 低资源语言 NLP | XLM-V or domain-specific fine-tune / XLM-V 或领域微调 |

Eğer performans önemli ise hedef dilde ince ayarlamalar için her zaman bütçe yapın.

> Eğer performans önemli ise, daima hedef dilinin bütçesi için başlangıç noktası, son çözüm değil.

### Tokenizasyon vergisi.

Çok dilli modeller tüm dillerinde tek bir işaretlemeci paylaşırlar. Bu kelime birikimi İngilizce, Fransızca, İspanyolca, Çinli, Almanca tarafından baskın bir corpus üzerinde eğitilir.

> Çok dilli modeller tüm dillerde bir sözcük paylaşımında bulunmaktadır. Bu sözcükler İngilizce, Fransızca, İspanyolca, Çince ve Almanca'da öğretilen bir dil üzerinde eğitim alıyor.

- **Fertility tax.**Düşük kaynaklı dil metni İngilizce'den çok daha fazla kelime için işaretleme yapar. Bir Hintçe cümlesinin eşdeğer bir İngilizce cümlesinin 3-5 katına kadar işaret ihtiyacı olabilir.
  **繁殖税。**低资源语言文本每词分词成英语比很多的代币──一个印地语句可能需要等价英语句的3-5倍的代币──
- **Variant recovery tax.**Her yazı tipi hatası, diyakritik variansı, Unicode normallaşım eşleşmezliği veya durum değişimi yerleşim alanında soğuk başlangıç ile ilişkili olmayan bir dizige dönüşür.
  **变体恢复税。**Her bir yazma hatası, değişim ses simgesi, değişim, birleşim, uyumsuzluk veya küçük yazma değişimi yerleşik alanın soğuk başlatılmamış bir dizisine dönüştürülür.
- **Capacity spillover tax.**Vergi 1 ve 2 bağlam pozisyonlarını, katman derinliğini ve yerleştirme boyutlarını tüketir. Gerçek mantık için kalan sistematik olarak daha küçüktür.
  **容量溢出税。**税 1 和 2 消耗上下文位置、层深度和嵌入维度── 留给实际推理的系统性地更小──

Pratik semptom: modeliniz normalde Hintçe eğitim alır, kayıp eğri doğru görünür, değerlendirme karmaşıklığı makul görünür ve üretim sonuçları ince yanlış. **You cannot data-scale your way out of a broken tokenizer.**

> 实际症状:模型在印地语上训练正常,损失曲线正确,评估困惑度合理,但生产输出微妙地出错――**你无法通过数据扩展来修复损坏的分词器。**

Yumuşatma yöntemleri: hedef dili için iyi bir kapsamlılık olan bir tokenizer seçin; tutulan hedef metinde tokenleştirme verimliliğini kontrol edin; gerçekten uzun kuyruğu olan senaryolar için bayt seviyesindeki geri dönüşü kullanın.

> 缓解措施:选择对目标语言覆盖良好的分词器;留出的目标文本上验证分词繁殖率;对真正长尾书写使用字节级回退──

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-multilingual-picker.md`- ...

> 保存为 `outputs/skill-multilingual-picker.md`- ...

```markdown
---
name: multilingual-picker
description: Pick source language, target model, and evaluation plan for a multilingual NLP task.
version: 1.0.0
phase: 5
lesson: 18
tags: [nlp, multilingual, cross-lingual]
---

Given requirements (target languages, task type, available labeled data per language), output:

1. Source language for fine-tuning. Default English; check LANGRANK or qWALS if target language has a typologically close high-resource language.
2. Base model. XLM-R (classification), mT5 (generation), NLLB (translation), Aya-23 (generative LLM).
3. Few-shot budget. Start with 100-500 target-language examples if available.
4. Evaluation plan. Per-language accuracy, cross-lingual consistency, entity-level F1 on non-Latin scripts.

Refuse to ship a multilingual model without per-language evaluation. Flag scripts with low tokenization coverage as needing byte-fallback.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Egzersizler.

1. **Easy.**İngilizce, Fransızca, Hindi ve Arapça dillerinde her dilde 10 cümle ile sıfır atış sınıflandırma hattını çalıştırın. Her birinde doğruluk raporlayın.
   **简单。**İngilizce, Fransızca, Hintçe ve Arapça dillerinde çalışmalar, her dilde 10 cümle, rapor doğruluk oranı
2. **Medium.**Kullanım`paraphrase-multilingual-MiniLM-L12-v2`İngilizce sorgulama, herhangi bir dilde belgeler almak.
   **中等。**构建跨语言检索器──用英语查询,检索任何语言的文档──测量回忆@5──
3. **Hard.**Bir Hint sınıflandırma görevi için İngilizce kaynak ve Hintçe kaynak ince ayarları karşılaştırın. Hangi kaynak daha iyi Hintçe doğruluğu ürettiğini bildirin.
   **困难。**İngilizce kaynak ve Hintçe kaynakları ile karşılaştırıldığında Hintçe sınıflandırma görevlerinin etkisine göre daha iyi bir doğruluk oranı elde edilen raporlar rapor edilmiştir.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Anahtar Şartlar .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Multilingual model（多语言模型） | One model, many languages / 一个模型多种语言 | Shared vocabulary and parameters across languages. / 跨语言共享词表和参数。 |
| Cross-lingual transfer（跨语言迁移） | Train on one, run on another / 训练一种，运行另一种 | Fine-tune on source, evaluate on target without target labels. / 在源语言微调，在目标语言评估。 |
| Zero-shot（零样本） | No target labels / 无目标标签 | Transfer without target-language fine-tuning. / 无目标语言微调的迁移。 |
| Few-shot（少样本） | Small target labels / 少量目标标签 | 100-500 target-language examples for fine-tuning. / 100-500 个目标语言样本。 |
| mBERT | First multilingual LM / 首个多语言 LM | 104-language BERT on Wikipedia. / 104 语言 BERT。 |
| XLM-R | Cross-lingual baseline / 跨语言基线 | 100-language RoBERTa on CommonCrawl. / 100 语言 RoBERTa。 |
| NLLB | 200-language MT / 200 语言 MT | No Language Left Behind. 55 low-resource languages. / 不让任何语言掉队。55 种低资源语言。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.

## Daha fazla okumak

- [Conneau et al. (2019). XLM-R](https://arxiv.org/abs/1911.02116) XLM-R makalesi. / XLM-R 论文。
- [Pires et al. (2019). How Multilingual is Multilingual BERT?](https://arxiv.org/abs/1906.01502) diller arası transfer analizi. / 跨语言迁移分析。
- [Costa-jussà et al. (2022). No Language Left Behind](https://arxiv.org/abs/2207.04672) NLLB-200. / NLLB-200 论文。
- [Üstün et al. (2024). Aya Model](https://arxiv.org/abs/2402.07827) Cohere'nin çok dilli LLM. / Cohere 多语言 LLM。
- [Language Similarity Predicts Cross-Lingual Transfer (2026)](https://www.mdpi.com/2504-4990/8/3/65) QWALS / LANGRANK. / qWALS / LANGRANK 源语言论文。
