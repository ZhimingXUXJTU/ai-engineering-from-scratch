# Adı: Entite Tanınması

> Açıklama sınırları, yuvalar ve domen jargonları ile uğraşana kadar kolay geliyor.
> Bu isimleri çıkarın. Sıkı bir şekilde konuşun.

> **【中文解读】**Metin içinde tanımlanan kişi adı, yer adı, örgüt adı ve diğer varlıklar¬ bilgi çekimi ve bilgi çizelgesinin temelini oluşturur.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word Embeddings) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 5 · 03（词嵌入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

"Apple, Google'ı ABD'deki iPhone arama anlaşması için dava etti". Beş kurum: Apple (ORG), Google (ORG), iPhone (PRODUCT), arama anlaşması (belki), US (GPE). İyi bir NER sistemi hepsini doğru türlerle çıkarır. Kötü bir iPhone'u kaçırır, Apple meyvesini Apple ile karıştırır ve "US" ı PERSON olarak etiketler.

> "Apple, Google'ı ABD'deki iPhone arama anlaşması için dava etti". 五个实体:Apple(ORG)、Google(ORG)、iPhone(PRODUCT)、search deal(可能)、US(GPE)。

NER, her yapılandırılmış çıkarma borusunun altındaki iş atıdır. Tekrarlama analizleri, uyumluluk günlükleri tarama, tıbbi kayıtların anonimleştirilmesi, arama sorgularını anlama, chatbot cevapları için yerleştirme, yasal sözleşme çıkarma. Bunu asla göremezsiniz; her zaman buna bağlısınız.

> NER her yapılandırılmış çekim su hattı altında çalışma motorudur. Özetle analiz, konfor günlük tarama, tıbbi kayıtların anonimleştirilmesi, arama sorgularının anlaşılması, robotların yanıtlarının temelini, yasal sözleşme çekimleri.

Bu ders klasik yolu (kurallara dayalı, HMM, CRF) modern yolu (BiLSTM-CRF, sonra dönüştürücüler) ile yürür.

> Bu ders klasik yollardan (Kılalar Üzerine, HMM, CRF) modern yollara doğru (BiLSTM-CRF, Transformer) gider.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

**BIO tagging**(veya BILOU) birim çıkarımı bir dizi etiketleme sorunu haline getirir.`B-TYPE`(üçleme başlangıcı), `I-TYPE`(dışer bir kuruluş), veya `O`(herhangi bir kurum dışında).

> **BIO 标注**(BILOU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU) )  (BiloU)  (BiloU)  (BiloU)  (BiloU) )  (BiloU)  (BiloU)  (BiloU)  (BiloU)  (BiloU) )  (BiloU)  (BiloU)  (BiloU)  (BiloU) )  (BiloU)  (BiloU)  (B)`B-TYPE`(实体开始)`I-TYPE`(beden içi) veya `O`(hiçbir beden içinde değil)

```
Apple    B-ORG
sued     O
Google   B-ORG
over     O
its      O
iPhone   B-PRODUCT
search   O
deal     O
in       O
the      O
US       B-GPE
.        O
```

Çoklu tokenli kuruluşlar zinciri: `New B-GPE`- Evet .`York I-GPE`- Evet .`City I-GPE`Biyo'yu anlayan bir model keyfi alanları çıkarır.

> Çoklu bir 实体链接:`New B-GPE`- Evet.`York I-GPE`- Evet.`City I-GPE`❖ BIO'nun modelini anlamak istediği çaptan elde edilebilir.

Mimarlık ilerleme:

> 架构演进:

- **Rule-based.**Regex + gazeter aramaları, bilinen kurumlarda yüksek hassasiyet, yeni kurumlarda sıfır kapsam.
  **基于规则。**正则 + 地名词典查找──已知实体精确率高,对新实体零覆盖──
- **HMM.**Gizli Markov modeli, verilen token etiketinin emisyon olasılığı, etiket-etikete geçiş olasılığı, Viterbi dekodlaması, etiketlenmiş veriler üzerinde eğitilmiş.
  **HMM。**隐马尔可夫模型──给定标签的代币 发射概率,标签间转移概率──Viterbi 解码──在标签数据上训练──
- **CRF.**Şartlı Random Alan. HMM gibi ama ayrımcı, böylece keyfi özellikleri (söz şekli, başlık, komşu kelimeler) karıştırmak için.
  **CRF。**条件随机场── HMM'ye benzer, ancak 判别式, böylece herhangi bir özelliği bir araya getirebilir.
- **BiLSTM-CRF.**LSTM cümleyi her iki yönde de okuyor, üstteki CRF katmanı tutarlı etiket dizilerini uyguluyor.
  **BiLSTM-CRF。**Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görevler: Görev
- **Transformer-based.**Token sınıflandırma başlığı ile ince ayarlı BERT. En iyi doğruluk.
  **基于 Transformer。**Kullanılan simge 分类头微调 BERT──最佳准确率──最多计算量──

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
ner-bio-tagging
```

## Yapın

### Adım 1: BIO etiketleme yardımcıları

```python
def spans_to_bio(tokens, spans):
    labels = ["O"] * len(tokens)
    for start, end, label in spans:
        labels[start] = f"B-{label}"
        for i in range(start + 1, end):
            labels[i] = f"I-{label}"
    return labels


def bio_to_spans(tokens, labels):
    spans = []
    current = None
    for i, label in enumerate(labels):
        if label.startswith("B-"):
            if current:
                spans.append(current)
            current = (i, i + 1, label[2:])
        elif label.startswith("I-") and current and current[2] == label[2:]:
            current = (current[0], i + 1, current[2])
        else:
            if current:
                spans.append(current)
                current = None
    if current:
        spans.append(current)
    return spans
```

```python
>>> tokens = ["Apple", "sued", "Google", "over", "iPhone", "sales", "."]
>>> labels = ["B-ORG", "O", "B-ORG", "O", "B-PRODUCT", "O", "O"]
>>> bio_to_spans(tokens, labels)
[(0, 1, 'ORG'), (2, 3, 'ORG'), (4, 5, 'PRODUCT')]
```

### Adım 2: El yapımı özellikler

Klasik (neural olmayan) NER için özellikler oyundur.

> 经典 (非神经) NER için, özellikler 关键――有用的特征:

```python
def token_features(token, prev_token, next_token):
    return {
        "lower": token.lower(),
        "is_upper": token.isupper(),
        "is_title": token.istitle(),
        "has_digit": any(c.isdigit() for c in token),
        "suffix_3": token[-3:].lower(),
        "shape": word_shape(token),
        "prev_lower": prev_token.lower() if prev_token else "<BOS>",
        "next_lower": next_token.lower() if next_token else "<EOS>",
    }


def word_shape(word):
    out = []
    for c in word:
        if c.isupper():
            out.append("X")
        elif c.islower():
            out.append("x")
        elif c.isdigit():
            out.append("d")
        else:
            out.append(c)
    return "".join(out)
```

`word_shape("iPhone")`Devamı`xXxxxx`- Evet .`word_shape("USA-2024")`Devamı`XXX-dddd`Başlık kalıpları, gerçek isimler için yüksek sinyallidir.

> `word_shape("iPhone")`Geri dön .`xXxxxx`- Evet.`word_shape("USA-2024")`Geri dön .`XXX-dddd`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊    ◊     ◊        ◊                                                                                                                                                                                    

### Adım 3: Basit bir kural tabanlı + sözlük tabanı

```python
ORG_GAZETTEER = {"Apple", "Google", "Microsoft", "OpenAI", "Meta", "Amazon", "Netflix"}
GPE_GAZETTEER = {"US", "USA", "UK", "India", "Germany", "France"}
PRODUCT_GAZETTEER = {"iPhone", "Android", "Windows", "ChatGPT", "Claude"}


def rule_based_ner(tokens):
    labels = []
    for token in tokens:
        if token in ORG_GAZETTEER:
            labels.append("B-ORG")
        elif token in GPE_GAZETTEER:
            labels.append("B-GPE")
        elif token in PRODUCT_GAZETTEER:
            labels.append("B-PRODUCT")
        else:
            labels.append("O")
    return labels
```

Üretim gazetelerinde Wikipedia ve DBpedia'dan milyonlarca giriş çıkartılmıştır.`Apple`Bu yüzden istatistik modeller kazanmış.

> 生产地名词典有数百万条目,从 Wikipedia 和 DBpedia 抓取──覆盖率不错──消歧(公司 `Apple`Su meyvesi`apple`Bu da bir statistiksel başarının sebebi.

### 4. adım: CRF adım (sketch, full implant değil)

50 satırdaki sıfırdan tam CRF, olasılık teorisi temelleri olmadan aydınlatıcı değildir.`sklearn-crfsuite`Bunun yerine:

> 概率 teorisi temelinin olmadığı halde, sıfırdan 50′ye kadar tam bir CRF'yi gerçekleştirmek bilinmiyor.`sklearn-crfsuite`- ...

```python
import sklearn_crfsuite

def to_features(tokens):
    out = []
    for i, tok in enumerate(tokens):
        prev = tokens[i - 1] if i > 0 else ""
        nxt = tokens[i + 1] if i + 1 < len(tokens) else ""
        out.append({
            "word.lower()": tok.lower(),
            "word.isupper()": tok.isupper(),
            "word.istitle()": tok.istitle(),
            "word.isdigit()": tok.isdigit(),
            "word.suffix3": tok[-3:].lower(),
            "word.shape": word_shape(tok),
            "prev.word.lower()": prev.lower(),
            "next.word.lower()": nxt.lower(),
            "BOS": i == 0,
            "EOS": i == len(tokens) - 1,
        })
    return out


crf = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True)
X_train = [to_features(s) for s in sentences_tokenized]
crf.fit(X_train, bio_labels_train)
```

`c1`ve `c2`L1 ve L2 düzenlenmesi. `all_possible_transitions=True`modelin yasa dışı diziler öğrenmesine izin verir (örneğin,`I-ORG`Sonra .`O`) olasılığı düşüktür, bu nedenle bir CRF, kısıtlama yazmadan BIO tutarlılığını nasıl zorlar.

> `c1`和 `c2`L1 ve L2 düzeltilmiştir.`all_possible_transitions=True`让模型学习非法序列 (yani yasa dışı bir süreç öğrenmek)`O`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `I-ORG`) çok olası değil, bu CRF'nin, bir şey yazmadığınızda BIO'yu zorla bir şekilde yapmasıdır.

### Adım 5: BiLSTM-CRF'nin ne eklediği

Özellikler öğrenilmektedir. Girişler: simge yerleştirmeler (GloVe veya fastText). LSTM soldan sağa ve sağdan sola okuyor. Konkaten gizli durumlar bir CRF çıkış katmanı üzerinden geçer. CRF hala etiket-seyrek tutarlılığını zorlar; LSTM el yapımı özellikleri öğrenilmiş özelliklerle değiştirir.

> Özellikler öğrenilmeye dönüştürülmüştür. Giriş: token 嵌入(GloVe veya fastText) ・・・LSTM soldan sağya ve sağdan solya okuyun。

```python
import torch
import torch.nn as nn


class BiLSTM_CRF_Head(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_labels):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(hidden_dim * 2, n_labels)

    def forward(self, token_ids):
        e = self.embed(token_ids)
        h, _ = self.lstm(e)
        emissions = self.fc(h)
        return emissions
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

CRF katmanı için kullan `torchcrf.CRF`El yapımı CRF'den elde edilen kazanç ölçülebilir ama on binlerce etiketli cümle yoksa beklediğinizden daha küçüktür.

> CRF 层使用 `torchcrf.CRF`(Pip yükle pytorch-crf) ◊ karşılaştırıldığında el işlemi CRF'nin yükseltilmesi ölçülebilir, ama beklediğinizden küçük, eğer birkaç milyon işaret cümlesi yoksa.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

spaCy üretim derecesindeki NER'leri kutudan çıkarıyor.

> Bu, üretim sınıfı NER'i sağlamak için kullanılır.

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple sued Google over its iPhone search deal in the US.")
for ent in doc.ents:
    print(f"{ent.text:20s} {ent.label_}")
```

```
Apple                ORG
Google               ORG
iPhone               ORG
US                   GPE
```

Not:`iPhone`etiketlenmiş`ORG`- Hayır .`PRODUCT` spaCy'nin küçük modeli zayıf ürün birimi kapsamına sahiptir.`en_core_web_lg`Transformer modeli (`en_core_web_trf`) daha iyi yapıyor.

> Dikkat et .`iPhone`İşaretlendirilmiş`ORG`Hayır.`PRODUCT` spaCy'nin küçük modeli ürün varlıklarının kapsamından daha zayıfdır──大模型(`en_core_web_lg`)更好──Transformer 模型(`en_core_web_trf`Daha iyi.

BERT tabanlı NER için Kucaklı Yüz:

> Kucaklanmak Yüzü'nün BERT'e dayalı NER:

```python
from transformers import pipeline

ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
print(ner("Apple sued Google over its iPhone in the US."))
```

```
[{'entity_group': 'ORG', 'word': 'Apple', ...},
 {'entity_group': 'ORG', 'word': 'Google', ...},
 {'entity_group': 'MISC', 'word': 'iPhone', ...},
 {'entity_group': 'LOC', 'word': 'US', ...}]
```

`aggregation_strategy="simple"`Bu işlem olmadan, simge seviyesindeki etiketler elde eder ve kendinizi birleştirmek zorundasınız.

> `aggregation_strategy="simple"`Bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir bir de bir bir de bir de bir bir bir de bir de bir bir bir de bir bir de bir bir de bir bir bir de bir de bir bir bir de bir de bir bir bir bir de bir bir de bir bir bir de bir de bir bir bir bir de bir de bir bir bir de bir bir bir de bir bir de bir bir bir de bir de bir bir bir bir de bir bir de bir bir bir de bir de bir bir bir bir de bir de bir bir bir bir bir de bir de bir bir bir de bir de bir bir bir de bir bir bir bir bir de bir de bir bir bir de bir de bir bir bir bir de bir de bir bir bir bir de bir de bir bir bir de bir de bir bir bir bir de bir de bir bir bir bir de bir de bir bir bir bir de bir de bir bir bir de bir de bir bir bir de bir de bir bir bir bir de bir de bir de bir bir bir bir de bir de bir bir bir bir de bir de bir bir de bir de bir bir bir bir de bir de bir bir bir bir bir de bir de bir bir bir de bir de bir de bir de bir de bir de bir bir bir bir bir de bir de bir bir bir bir de bir de bir de bir bir bir de bir de bir de bir bir bir de bir de bir bir bir bir de bir de bir de bir de bir de bir de bir bir de bir de bir de bir bir de bir

### LLM tabanlı NER (2026 seçeneği)

Zero-shot ve few-shot LLM NER artık birçok alanda ince ayarlanmış modellerle rekabetçi ve etiketlenmiş veriler kıt olduğunda çarpıcı olarak daha iyi.

> 零样本和少样本 LLM NER artık birçok alanda küçük modelle rekabetçi, etiket verisi eksikliği zaman avantajları daha büyüktür.

- **Zero-shot prompting.**LLM'ye bir varlık türlerinin listesini ve örnek bir şemayı verin. JSON çıkışını isteyin. Kutunun dışına çalışır; doğruluk yeni alanlarda orta derecede.
  **零样本提示。**LLM'ye bir varlık tip listesi ve örnek modeli vermek için JSON 输出, yeni alanlarda doğruluk oranı, vb.
- **ZeroTuneBio-style prompting.**Görevyi aday çıkarma → anlam açıklama → yargı → tekrar kontrol edin. Çok aşamalı bir istek (tek çekim değil) biyomedikal NER'de doğruluğu önemli ölçüde yükseltir. Aynı model yasal, finansal ve bilimsel alanlarda çalışır.
  **ZeroTuneBio 风格提示。**Bu nedenle, bu yöntemin bir sonraki döneminde de uygulanacağı bir çalışma olarak belirtilmiştir.
- **Dynamic prompting with RAG.**Her sonuç çağrısı için küçük bir notlu tohum seti ile en benzer etiketlenen örnekleri alın; birkaç atışlı istekleri uçan bir şekilde oluşturun. 2026 referans değerlerinde, bu, GPT-4 biyomedikal NER F1'i statik isteklere göre %11-12 oranında yükseltir.
  **动态 RAG 提示。**Her düşünce, en benzer etiket örneklerini az sayıda etiketleme tohumundan araştırmaya yöneltir. 2026 yılında GPT-4 Biomedical NER F1'in durum önerilerinden %11-12 oranında artması görülüyor.
- **Per-entity-type decomposition.**Uzun belgelere göre, tüm varlık türlerini bir anda çıkaran tek bir çağrı, uzunluk arttıkça hatırlanmayı kaybeder. Varlık tipi başına bir çıkarma geçitini çalıştırın. Daha yüksek sonuçlama maliyeti, önemli ölçüde daha yüksek doğruluk. Bu klinik notlar ve yasal sözleşmeler için standart bir örnektir.
  **按实体类型分解。**长文档, tüm fiziksel tipleri bir kez kullanıldığında, uzunluğu arttıkça kaybeden çağrı oranı artar.

2026'dan itibaren üretim önerisi: Eğitim verileri toplamanızdan önce LLM sıfır çekim başlangıç çizgisinden başlayın.

> 2026 yıl üretim önerisi: before collecting training data, first use LLM 零样本基线开始──通常 F1'den fazlası yeterli, you never need any minor modification──

### Klasik NER hala kazanırken

LLM'ler mevcut olsa bile, klasik NER:

> Hatta LLM kullanılabilir, klasik NER aşağıdaki durumlarda kazanmak:

- Gecikme bütçesi 50 ms'den aşağı.
  Geçer bütçesi 50 millimetrinden az.
- Binlerce etiketli örnek var ve %98+ F1 gerekiyor.
  Binlerce etiket örneği var ve %98+ F1 gerekiyor.
- Alanın, önceden eğitilmiş bir CRF veya BiLSTM'nin iyi transfer ettiği istikrarlı bir ontolojisi vardır.
   alanı stabil bir yapı, CRF veya BiLSTM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
- Yasal kısıtlamalar, yerleşim yerinde, üreticisiz bir model gerektirir.
  监管约束要求本地部署的非生成式模型──

### - Nerede düşüyor ?

- **Domain shift.**CoNLL'de yasal sözleşmeler konusunda eğitimli olan NER gazeteciden daha kötü bir performans gösteriyor.
  **领域偏移。**CoNLL'de eğitim alanında NER 处理法律合同同时比地名词典还差──在你的领域上微调──
- **Nested entities.**"Bank of America Tower" aynı zamanda bir ORG ve bir FASILITY'dir. Standart BIO üst üste dönen uzantıları temsil edemez.
  **嵌套实体。**"Bank of America Tower" 同时是 ORG 和 FASILITY──标准 BIO 无法表示重叠跨度──你需要嵌套 NER(多遍或基于跨度的模型)──
- **Long entities.**"United States Federal Deposit Insurance Corporation". Token seviyesindeki modeller bazen bunu bölüyor.`aggregation_strategy`veya işlemi sonrası.
  **长实体。**"United States Federal Deposit Insurance Corporation" Token 级模型有时会拆分这个──使用 `aggregation_strategy`Ya da son işleme.
- **Sparse types.**Tıp NER etiketleri Drug_Brand, ADVERSE_EVENT, DOSE. Genel amaçlı modeller hiçbir fikre sahip değiller. Scispacy ve BioBERT bu noktalar için başlangıç noktasıdır.
  **稀疏类型。**医疗 NER 标签如Drug_BRAND、ADVERSE_EVENT、DOSE。通用模型一无所知。Scispacy 和 BioBERT is there's starting point──

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-ner-picker.md`- ...

> 保存为 `outputs/skill-ner-picker.md`- ...

```markdown
---
name: ner-picker
description: Pick the right NER approach for a given extraction task.
version: 1.0.0
phase: 5
lesson: 06
tags: [nlp, ner, extraction]
---

Given a task description (domain, label set, language, latency, data volume), output:

1. Approach. Rule-based + gazetteer, CRF, BiLSTM-CRF, or transformer fine-tune.
2. Starting model. Name it (spaCy model ID, Hugging Face checkpoint ID, or "custom, trained from scratch").
3. Labeling strategy. BIO, BILOU, or span-based. Justify in one sentence.
4. Evaluation. Use `seqeval`. Always report entity-level F1 (not token-level).

Refuse to recommend fine-tuning a transformer for under 500 labeled examples unless the user already has a pretrained domain model. Flag nested entities as needing span-based or multi-pass models. Require a gazetteer audit if the user mentions "production scale" and labels are unchanged from CoNLL-2003.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Egzersizler.

1. **Easy.**Uygulama`bio_to_spans`(Tüm yönleri `spans_to_bio`) ve 10 cümle ile geri dönüş tutarlılığını kontrol etmektedir.
   **简单。** gerçekleştirmek `bio_to_spans`(`spans_to_bio`Bu da bir diğer yöntemdir.
2. **Medium.**Bu nedenle, bu durumun üstündeki sklearn-crfsuite CRF'yi CoNLL-2003 İngilizce NER veri kümesine göre eğitmek gerekir.`seqeval`Tipik sonuç: ~84 F1.
   **中等。**Bu nedenle, bu durumun bir diğer nedeni de, bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de bir diğerinin de birini de bir diğerinin de birinden de bir diğerinin de birinden de bir diğerinin de birinden de bir diğerinin de bir diğerini de bir diğerinin de birinden de bir diğerinin de birinden de bir diğerini de bir diğerinin de birinden de bir diğerini de bir diğerinden de bir diğerinden de bir diğerinden de birinden de bir diğerini de bir diğerinden de bir diğerinden de bir diğerinden de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir de bir`seqeval`報告每类 F1──典型结果:~84 F1──
3. **Hard.**- Güzel sesli .`distilbert-base-cased`Bu, bir alanın özel bir NER veri kümesi (tıp, hukuki veya finansal) üzerinde yapılmıştır.
   **困难。**Özel alanlarda NER (medicine, hukuk veya finans)`distilbert-base-cased`▽ SpaceY 小模型比较──记录数据泄漏检查并写下让你惊的地方──

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Anahtar Şartlar .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NER（命名实体识别） | Extract names / 提取名字 | Label token spans with types (PERSON, ORG, GPE, DATE, ...). / 用类型（PERSON、ORG、GPE、DATE 等）标注 token 跨度。 |
| BIO | Tagging scheme / 标注方案 | `B-X` begins, `I-X` continues, `O` outside. / `B-X` 开始，`I-X` 继续，`O` 外部。 |
| BILOU | Better BIO / 更好的 BIO | Adds `L-X` (last), `U-X` (unit) for cleaner boundaries. / 添加 `L-X`（最后）、`U-X`（单元）以获得更清晰的边界。 |
| CRF（条件随机场） | Structured classifier / 结构化分类器 | Models transitions between labels, not just emissions. Enforces valid sequences. / 对标签间的转移建模，而不仅仅是发射。强制有效序列。 |
| Nested NER（嵌套 NER） | Overlapping entities / 重叠实体 | One span is a different entity than a sub-span of it. BIO cannot express this. / 一个跨度与其子跨度是不同的实体。BIO 无法表达这一点。 |
| Entity-level F1（实体级 F1） | Proper NER metric / 正确的 NER 指标 | Predicted span must match true span exactly. Token-level F1 overstates accuracy. / 预测跨度必须与真实跨度完全匹配。Token 级 F1 会高估准确率。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.

## Daha fazla okumak

- [Lample et al. (2016). Neural Architectures for Named Entity Recognition](https://arxiv.org/abs/1603.01360)BiLSTM-CRF makalesi. Kanonik. / BiLSTM-CRF 论文──经典──
- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805) standard haline gelen token sınıflandırma örneğini tanıtır. /  introduced into becoming standard token 分类模式──
- [spaCy linguistic features — named entities](https://spacy.io/usage/linguistic-features#named-entities)    `Doc.ents`ve `Span`- Hayır .`Doc.ents`和 `Span`Üstteki her özellikten geçerli bir referans.
- [seqeval](https://github.com/chakki-works/seqeval) doğru metrik kütüphanesi. her zaman kullan. / 正确的指标库──始终使用它──
