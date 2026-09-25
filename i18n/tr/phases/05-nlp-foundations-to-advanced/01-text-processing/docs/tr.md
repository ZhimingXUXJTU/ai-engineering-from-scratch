# Metin İşleme  Tokenizasyon, Stemming, Lemmatizasyon  文本处理  分词、词干提取、词形還原

> Dil sürekli, modeller ayrı, önceden işleme köprüdür.
> 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 语言是连续的. 模型是离散的. 模型是离散的. 语言是离散的. 语言是离散的. 模型是离散的. 模型是离散的.

> **【中文解读】**分词是 NLP'nin ilk adım:把连续文本切成离散代币──包括词干提取和词形还原──在 LLM 时代,分词由 BPE 等子词分词器处理──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Öğrenme hedefleri

- Tokenizasyon, stemming ve lemmatizasyon'u ayrı bir preprocessing operasyonu olarak anlamak
  Anlama分词、词干提取和词形还原 farklı bir önceden işleme işlem olarak
- Regex tokenizer, Porter voter adım ve arama tabanlı lemmatizer oluşturun sıfırdan
  0 yapılandırma ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠ ≠  ≠  ≠   ≠    ≠                                                                                                                                                                                                                                                                                                                               
- NLTK ve spaCy'yi üretim öncesi işleme boru hattları için karşılaştırın
  NLTK ve spaCy ile karşılaştırıldığında üretim öncesi işleme akım su hattındaki avantajlar
- En yaygın iki üretim başarısızlığını tanımak: yeniden üretilebilirlik sürüşü ve tren/inferans eşleşme eksikliği
  识别两种最常见的生产故障:可复现性漂移和训练/推理不匹配

## Sorunlar. Sorunlar.

Bir model "Kediler koşuyordu" diye okuyamıyor. Tam sayıları okuyor.

> Model cannot directly read "Kediler koşuyordu".

Her NLP sistemi aynı üç soruyla başlar. Bir kelime nereden başlar? kelimenin kökü nedir? "hareket", "hareket", "hareket" yardımcı olduğunda aynı şey olarak nasıl ele alıyoruz?

> Her NLP sistemi aynı üç soruya cevap vermeli: Bir kelime nereden başlar? Bu kelime kelimesinin kökü nedir?

Tokenizasyon yanlış olursa model çöpten öğreniyor.`don't`Bir simge olarak ama`do n't`Eğer oylarınız çökerse eğitim dağıtıcılığı bölünür.`organization`ve `organ`Eğer lemmatizer'iniz konuşma bağlamının bir kısmına ihtiyaç duyarsa ama bunu geçmezseniz, fiiller isim olarak değerlendirilir.

> Şöyle yazıyor: "Sözlerin yanlış olduğunu, modelin çöp verilerinden öğrendiğini düşün".`don't`Bir işaret olarak, ama onu`do n't`İki kişiyken, eğitim dağıtılır ve bölünür.`organization`和 `organ`结为同一个词干,主题建模就会失效──如果你的词形还原器需要词性上下文但你没有传入,动词就会被当作名词处理──

Bu ders, üç önceden işleme adımını sıfırdan inşa eder, sonra NLTK ve spaCy'nin aynı işi nasıl yaptığını gösterir. Böylece, pazarlamaları görebilirsiniz.

> Bu ders, üç ön işleme adımını sıfırdan inşa ederek, sonra NLTK ve spaCy'nin aynı işi nasıl yapacağını gösterir ve bunların ağırlığını görmenizi sağlar.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

Her birinin bir işi ve bir başarısızlık modudur.

> Üç işlem, her birinin kendi sorumlulukları ve başarısızlık modeli vardır.

**Tokenization**"Token" kasıtlı olarak belirsizdir çünkü doğru granularlık göreve bağlıdır. Klasik NLP için kelime seviyesini. Transformörler için alt kelime. Beyaz alan olmayan diller için karakter.

> **分词（Tokenization）**Bu kelime, "Token" olarak belirgin kalmak için kullanılır, çünkü uygunlık ölçüsü belirli görevlere bağlıdır. Klasik NLP, kelime seviyesini kullanır, Transformer, çocuk kelime seviyesini kullanır, boşluk olmayan dilli kelime seviyesini kullanır.

**Stemming**Kurallar ile birlikte, hızlı, saldırgan, aptal.`running -> run`- Evet .`organization -> organ`İkinci bir hata modudur.

> **词干提取（Stemming）**Uygulama kuralları kesintisi ──快速、激进、粗暴──`running -> run`- Evet.`organization -> organ`İkinci örnek ise başarısızlık biçimidir.

**Lemmatization**Bu nedenle, bir kelimeyi dilbilim biçimine düşürmek için dilbilim bilgisini kullanır.`ran -> run`(Run'un "run"ın geçmiş zamanlı olduğunu bilmem gerekiyor).`better -> good`(sırlaştırma biçimlerini bilmesi gerekir).

> **词形还原（Lemmatization）**Bilgiyi kullanmak için bir biçim oluşturmak gerekir.`ran -> run`(Run'un geçmişte olduğunu bilmem gerekiyor)`better -> good`(Bilmek gerekir)

Basmak kuralı. Hız önemli olduğunda ses çıkar ve gürültüye tolere edebilirsiniz (arşiv indeksleme, kaba sınıflandırma). Anlam önemli olduğunda (sorulara cevap vermek, semantik arama, kullanıcı okuyacak her şey) lematize edin.

> 经验法则:当语义重要时使用词干提取(搜索引、粗略分类) ――当语义重要时使用词形还原(问答、语义搜索、任何用户会阅读的场景) ――

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
edit-distance
```

## Yapın

### Adım 1: Regex kelime işaretleyicisi

En basit kullanışlı jeton, öz jetonları olarak noktalama tutarken alfa numerik olmayan karakterlere bölünür.

> En basit pratik yazılımcı, bir simge olmayan bir sayısal simge olarak ayırırken, bir simge olarak ayırır.

```python
import re

def tokenize(text):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[0-9]+|[^\sA-Za-z0-9]", text)
```

Üç örneği öncelik sırasıyla.`don't`- Evet .`it's`) Saf sayılar. Tek beyaz alan olmayan bir karakter olarak bağımsız bir simge (sıkıştırma).

> Üç öncelikli sıralanma biçimi.`don't`- Evet.`it's`)。 saf sayı。 herhangi bir tek boş beyaz olmayan harfsiz sayısal karakter bağımsız bir işarettir.

```python
>>> tokenize("The cats weren't running at 3pm.")
['The', 'cats', "weren't", 'running', 'at', '3', 'pm', '.']
```

Başarısızlık modları fark edilsin. `3pm`bölünür .`['3', 'pm']`Çünkü harf ve rakam süreleri arasında değişiklik yapıyoruz. Çoğu görev için yeterli. URL'ler, e-postalar, hashtaglar hepsi kırılıyor.

> 需要注意的失败模式──`3pm`Çıkarılmış`['3', 'pm']`, çünkü harfler sırası ve sayısal sırası arasında bir değişim yapıyoruz. Çoğu görev için yeterince iyi. URL'ler, e-postalar, konu etiketleri sorun doğurur.

### Adım 2: Porter stemmer (sadece 1a adım)

Porter algoritmasının tamamında beş aşama kuralları vardır. Yalnızca 1a adım en sık İngilizce sufifileri kapsar ve örneği öğretir.

> 完整的波特算法有五阶段的规则──仅步骤1a 就涵盖了最常见的英语后,并展示了规则模式──

```python
def stem_step_1a(word):
    if word.endswith("sses"):
        return word[:-2]
    if word.endswith("ies"):
        return word[:-2]
    if word.endswith("ss"):
        return word
    if word.endswith("s") and len(word) > 1:
        return word[:-1]
    return word
```

```python
>>> [stem_step_1a(w) for w in ["caresses", "ponies", "caress", "cats"]]
['caress', 'poni', 'caress', 'cat']
```

Kuralları yukarıdan aşağı oku.`ies -> i`Kural neden ?`ponies -> poni`- Hayır .`pony`Gerçek Porter'ın 1B adımını atarak bu durumu düzeltebiliriz. Kurallar rekabet eder. Önceki kurallar kazanır.

> Yukarıdan aşağıya kadar okumak kuralları:`ies -> i`規則是   kural`ponies -> poni`Hayır.`pony`Bu sorunun nedenleri: Porter'ın gerçek algoritması bu sorunu çözmek için 1b adımları vardır. Kurallar birbirleriyle rekabet eder, önde gelen kurallar kazanır. Kurallar sırası, herhangi bir kuralın sırasından daha önemlidir.

### Adım 3: Arama tabanlı lemmatizer

Lemmatizasyonun doğru bir morfoloji gerektiriyor.

> Gerçek kelimeler biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biç

```python
LEMMA_TABLE = {
    ("running", "VERB"): "run",
    ("ran", "VERB"): "run",
    ("runs", "VERB"): "run",
    ("better", "ADJ"): "good",
    ("best", "ADJ"): "good",
    ("cats", "NOUN"): "cat",
    ("cat", "NOUN"): "cat",
    ("were", "VERB"): "be",
    ("was", "VERB"): "be",
    ("is", "VERB"): "be",
}

def lemmatize(word, pos):
    key = (word.lower(), pos)
    if key in LEMMA_TABLE:
        return LEMMA_TABLE[key]
    if pos == "VERB" and word.endswith("ing"):
        return word[:-3]
    if pos == "NOUN" and word.endswith("s"):
        return word[:-1]
    return word.lower()
```

```python
>>> lemmatize("running", "VERB")
'run'
>>> lemmatize("cats", "NOUN")
'cat'
>>> lemmatize("better", "ADJ")
'good'
>>> lemmatize("watched", "VERB")
'watched'
```

Son durum, öğretim anının anahtarıdır.`watched`Masamızda değil ve düşüşümüz sadece ele geçiriyor .`ing`Gerçek lemmatizasyon kapsamını .`ed`, düzensiz fiiller, karşılaştırıcı özelliği, ses değişikliği olan çoğullar (`children -> child`Bu nedenle üretim sistemleri WordNet, spaCy'nin morfologizerini veya tam bir morfolojik analizörü kullanır.

> Son örnek, önemli öğretim zamanıdır.`watched`Bizim planlarımızda değil, bizim planlarımızda.`ing`◊ gerçek kelimeler`ed`、不规则动词、比较级形容词、语音变化的复数(`children -> child`)― Bu nedenle üretim sistemi WordNet ̇spaCy'nin biçim analizisini veya tam biçim analizisini kullanmaktadır.

### Dördüncü adım: Onları birleştir .

```python
def preprocess(text, pos_tagger=None):
    tokens = tokenize(text)
    stems = [stem_step_1a(t.lower()) for t in tokens]
    tags = pos_tagger(tokens) if pos_tagger else [(t, "NOUN") for t in tokens]
    lemmas = [lemmatize(word, pos) for word, pos in tags]
    return {"tokens": tokens, "stems": stems, "lemmas": lemmas}
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

Kayıp parça bir POS etiketlemesidir. 5 · 07 aşaması (POS Etiketleme) bir tane oluşturur.`NOUN`Ve sınırlarını kabul et.

> 缺少的部分是词性标注器──Phase 5 · 07(词性标注) 构建一个──目前,将所有词默认为 `NOUN`Bu sınırlılığı kabul etmedim.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

NLTK ve spaCy üretim sürümlerini gönderiyor.

> NLTK ve spaCy, üretim sınıfı sürümleri sunmaktadır.

### NLTK

```python
import nltk
nltk.download("punkt_tab")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger_eng")

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag

text = "The cats were running."
tokens = word_tokenize(text)
stems = [PorterStemmer().stem(t) for t in tokens]
lemmatizer = WordNetLemmatizer()
tagged = pos_tag(tokens)


def nltk_pos_to_wordnet(tag):
    if tag.startswith("V"):
        return "v"
    if tag.startswith("J"):
        return "a"
    if tag.startswith("R"):
        return "r"
    return "n"


lemmas = [lemmatizer.lemmatize(t, nltk_pos_to_wordnet(tag)) for t, tag in tagged]
```

`word_tokenize`- Sıkıntıları, Unicode'u, Regex'in kaçırdığı uç durumları.`PorterStemmer`Beş aşamada devam ediyor.`WordNetLemmatizer`NLTK'nin Penn Treebank skemasından WordNet'in kısaltma setiye çevrilen POS etiketine ihtiyaç duyar.

> `word_tokenize`处理缩写、Unicode 和你的正则表达式遗漏的边界情况──`PorterStemmer`Tüm beş aşama.`WordNetLemmatizer`需要将 NLTK'ın Penn Treebank 词性标注方案转换为 WordNet'in kısaltma kitlesi.

### spaCy

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running.")

for token in doc:
    print(token.text, token.lemma_, token.pos_)
```

```
The      the     DET
cats     cat     NOUN
were     be      AUX
running  run     VERB
.        .       PUNCT
```

spaCy tüm boru hattını arkasına saklıyor .`nlp(text)`Tokenizasyon, POS etiketleme ve lemmatizasyon hepsi çalışıyor. NLTK'den daha hızlı ölçekte. Kutu dışındaki daha doğru.

> Tüm su akışı gizlenmiş olacak.`nlp(text)`背后──分词、词性标注和词形还原全部运行──大规模下 NLTK daha hızlı, açık kutu daha doğru kullanılır──代价是你无法轻松替换单元组件──

### Hangisini seçmek için ne zaman

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Teaching, research, swapping components | NLTK | 教学、研究、需要替换组件 | NLTK |
| Production, multi-language, speed matters | spaCy | 生产环境、多语言、速度要求高 | spaCy |
| Transformer pipeline (you'll tokenize with the model's tokenizer anyway) | Use `tokenizers` / `transformers` and skip classical preprocessing | Transformer 流水线（反正你会用模型自带的分词器） | 使用 `tokenizers` / `transformers`，跳过经典预处理 |

### İki başarısızlık modunu kimse sizi uyarmaz

Çoğu ders algoritmaları öğretir ve durur. İki şey gerçek bir önceden işleme borusunu ısırır ve neredeyse asla kapsamalanmaz.

> Çoğu ders, algoritma öğretimi durduruldu. Gerçek bir önceden işleme akışını bitiren iki sorun var ve neredeyse hiç bahsedilmiyor.

**Reproducibility drift.**NLTK ve spaCy, versiyonlar arasında simgelendirme ve lemmatizer davranışını değiştirir.`['do', "n't"]`spaCy 2.x' de `["don't"]`3.x'te modeliniz bir dağıtım üzerinde eğitildi. İferense şimdi başka bir dağıtım üzerinde çalışır.`requirements.txt`20 örnek cümle beklenen işaretlemeyi dondurarak bir gerileme testi yazın.

> **可复现性漂移。**NLTK ve spaCy, farklı sürümler arasında değişen sözcük ve sözcük biçiminin yeniden oluştuğu davranışlarda oluşur.`['do', "n't"]`Sonuç olarak, 3.x'te oluşabilir.`["don't"]`◊ modeliniz bir dağılımda eğitim alır, bir dağılımda çalışır, bir dağılımda çalışır. ◊ Kesinlik oranı ◊ gerçekten düşer, nedenini kimse bilmiyor.`requirements.txt`Orta sabit kutu versiyonu。 bir ön işlem geri dönüş test,结 20 个样本句的预期分词结果──每次升级时运行──

**Training / inference mismatch.**Bu, en yaygın üretim NLP başarısızlığıdır. Eğitim sırasında önceden işleme yaparsanız, sonuç çıkarma sırasında aynı işlevi çalıştırmalısınız.

> **训练/推理不匹配。**訓練時使用激進的预处理 (小写化、停用词除、词干提取), dep署時使用原始用户输入,看看性能暴跌── NLP üretimi içinde en yaygın tek bir hata. 訓練時使用激進的预处理 (小写化、停用词除、词干提取), dep署時使用原始用户输入,看性能暴跌── NLP üretimi sırasında en yaygın tek bir hata. 訓練時使用激進的预处理 (小写化、停用词除、词干提取), eğer antrenman sırasında önceden işleme yapıyorsanız, önerme zamanı tamamen aynı işlevi yürütmelidir──预处理 olarak bir işlevi yayınlayacak, servis ekibi bir notu tek bir parçacık olarak yeniden yazmak yerine.

## İndirin . Ürünler .

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

Tekrar kullanılabilir bir ipucu, mühendislerin üç ders kitabı okumadan önce işleme stratejisini seçmelerine yardımcı olur.

> Bir tekrarlanabilir hızlı, mühendislerin önceden işleme stratejisini seçmesine yardımcı olmak için üç ders kitabı okumak zorunda değildir.

- Kaydet .`outputs/prompt-preprocessing-advisor.md`- ...

```markdown
---
name: preprocessing-advisor
description: Recommends a tokenization, stemming, and lemmatization setup for an NLP task.
phase: 5
lesson: 01
---

You advise on classical NLP preprocessing. Given a task description, you output:

1. Tokenization choice (regex, NLTK word_tokenize, spaCy, or transformer tokenizer). Explain why.
2. Whether to stem, lemmatize, both, or neither. Explain why.
3. Specific library calls. Name the functions. Quote the POS-tag translation if NLTK is involved.
4. One failure mode the user should test for.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend stemming for user-visible text. Refuse to recommend lemmatization without POS tags. Flag non-English input as needing a different pipeline.
```

## Egzersizler.

1. **Easy.**Uzaklaştırma`tokenize`URL'leri tek bir simge olarak tutmak için. Test: `tokenize("Visit https://example.com today.")`Bir URL simgesi üretmeli.
   **简单。**扩展 `tokenize`URI'yi tek bir simge olarak tutmak için:`tokenize("Visit https://example.com today.")`应产生一个URL标记――
2. **Medium.**Porter Adım 1b uygulamak . Eğer bir kelime vokal içerirse ve sonunda `ed`veya `ing`İkili konsonan kuralını kullan (`hopping -> hop`- Hayır .`hopp`)
   **中等。**实现 Porter 步骤 1b. Eğer bir kelime bir kelimeyi içerirse`ed`Ya da`ing`结尾,则移除它──处理双辅音规则(`hopping -> hop`- Hayır .`hopp`)。
3. **Hard.**WordNet'i arama tablosu olarak kullanan, ancak WordNet'in giriş olmadığı zaman Porter voter'e geri dönen bir lemmatizer oluşturun.
   **困难。**WordNet'in 条目 没有条目时回归你的Porter 词干提取器──%2$%2$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$3$4$3$3$3$4$3$3$4$4$4$4$4$4$4$4$4$4$4$4$$4$4$4$$4$$4$4$$4$$$$$$$$4$4$$$$4$$$$$$4$4$$$$$$$4$$$$4$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Anahtar Şartlar .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Token | A word | Whatever unit the model consumes. Can be word, subword, character, or byte. | Token（词元） | 一个词 | 模型消耗的任何单位。可以是词、子词、字符或字节。 |
| Stem | Root of a word | Result of rule-based suffix stripping. Not always a real word. | Stem（词干） | 词的词根 | 基于规则的后缀剥离结果。不一定是真正的词。 |
| Lemma | Dictionary form | The form you'd look up. Requires grammatical context to compute correctly. | Lemma（词元形式） | 词典形式 | 你会去词典中查找的形式。需要语法上下文才能正确计算。 |
| POS tag | Part of speech | Category like NOUN, VERB, ADJ. Needed to lemmatize accurately. | POS tag（词性标注） | 词性 | 如 NOUN、VERB、ADJ 等类别。准确词形还原需要它。 |
| Morphology | Word shape rules | How a word changes form based on tense, number, case. Lemmatization depends on it. | Morphology（形态学） | 词形变化规则 | 词如何根据时态、数、格变化形式。词形还原依赖它。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.

## Daha fazla okumak

- [Porter, M. F. (1980). An algorithm for suffix stripping](https://tartarus.org/martin/PorterStemmer/def.txt) orijinal makale, beş sayfa, hala en net açıklama. / 原始论文,五页,至今仍然是最清晰的解释──
- [spaCy 101 — linguistic features](https://spacy.io/usage/linguistic-features)Gerçek bir boru hattı nasıl kabloluyor?
- [NLTK book, chapter 3](https://www.nltk.org/book/ch03.html)Hâlâ düşünmediğin tokenizasyon kenarlık vakaları.
