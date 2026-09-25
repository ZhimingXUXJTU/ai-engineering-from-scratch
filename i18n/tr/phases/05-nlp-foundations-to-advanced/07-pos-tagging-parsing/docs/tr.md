# POS Etiketleme ve Sintektiksel Parsing .

> Bir süre için dilbilgi modası yoktu, sonra her LLM boru hattı yapılandırılmış çıkarımı doğrulamalıydı ve geri döndü.
> 语法 bir zamanlar popüler değildi. Sonra her LLM 流水线都需要验证结构化抽取, it again came back.

> **【中文解读】**给每一个词标注词性,分析句子的语法结构──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Ders 01 lematizasyonun konuşma bir parçası olduğunu söyledi.`running`Bir lematizer onu kısaltamaz.`run`Bilmeden .`better`Adjektifdir, aşağıya düşemez.`good`- Evet .

> 第01 课 承诺过词形还原需要词性标注──不知道 `running`Evet, evet, evet, evet, evet.`run`Bilmiyorum.`better`Evet, bu bir şey.`good`- Evet.

Bu vaat tüm bir alt alanı sakladı. Konuşmanın bir parçası olarak etiketleme, dilbilimsel kategorileri tahsis eder. Sintiksel analiz cümlenin ağaç yapısını geri kazanır: hangi kelime hangisini değiştirir, hangi fiil hangisini yönetir argümanları. Klasik NLP ikisini de on yıl daha iyi hale getirerek geçti. Sonra derin öğrenme onları önceden eğitilmiş bir transformatörün üstüne bir token sınıflandırma görevine dönüştürdü ve araştırma topluluğu ilerledi.

> O sözcüklerin arkasında bir bütün küçük alanı vardır. Sözcük etiketleri dağılımı.

Kullanılan topluluk değil. Her yapılandırılmış çıkarma boru hattı hala kapının altında POS ve bağımlılık ağaçlarını kullanır. LLM'de üretilen JSON dilbilgisi kısıtlamalarına karşı doğrulanır. Soru- yanıtlama sistemleri bağımlılık parseslerini kullanarak sorguları parçalayır. Makinesi çevirisi kalitesi değerlendicileri parse ağaçlarının hizalanmasını kontrol eder.

> 应用界没有──每个结构化抽取流水线仍在底层使用POS 和依赖树──LLM 生成的JSON 会根据语法约束进行验证──问答系统使用依赖分析来分解查询──机器翻译质量评估器检查分析树的对齐──

Bu ders, etiketleri, temel çizgileri ve sıfırdan uygulamayı bırakan noktayı tanıtır ve spaCy'yi çağırır.

> ❖ Anlamak gerekir. ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖    ❖ ❖    ❖ ❖    ❖       ❖                                                                                                 

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

**POS tagging**Her bir simgeyi bir dilbilimsel kategorisi ile etiketler.**Penn Treebank (PTB)**Tagset İngilizce'de varsayılan bir koddur. 36 etiket farklılıkları olan, sıradan okuyucu için zorlayıcı: `NN`tek isim, `NNS`çoğul isim, `NNP`özel isim tek kelime,`VBD`Geçmiş zamanlı fiil, `VBZ`3rd person singular present, ve benzeri.**Universal Dependencies (UD)**tagset daha kaba (17 etiket) ve dil-agnostiktir; diller arası çalışmalarda öntanımlı hale geldi.

> **词性标注（POS Tagging）**Her bir simge için 标注语法类别──**Penn Treebank (PTB)**Etiketler koleksiyonu İngilizce'de bir defalarca seçilmiştir. 36 etiket vardır.`NN`单数名词、`NNS`复数名词、`NNP`专名词单数、`VBD`动词过去时,`VBZ`动词第三人称单数现在时等等等──**通用依存（Universal Dependencies, UD）**标签集更粗(17 个标签) ve dille ilgisi yok; bu,跨语言工作的默认选择了──

```
The/DET cats/NOUN were/AUX running/VERB at/ADP 3pm/NOUN ./PUNCT
```

**Syntactic parsing**İki büyük stil:

> **句法分析（Syntactic Parsing）**产生一棵树──两种主要风格:

- **Constituency parsing.**Adım cümleleri, fiil cümleleri, önbölüm cümleleri birbirlerinin içinde yuvalar.
  **成分分析（Constituency Parsing）。**Növşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşşş
- **Dependency parsing.**Her kelimenin, bir dilbilgi ile etiketlenmiş, bağımlı olduğu tek bir baş kelimesi vardır.
  **依存分析（Dependency Parsing）。**Her kelime bir hükmeden merkezi kelime vardır, 标注语法关系――输出是一棵树,每条边是一个 (head, dependent, relation) 三元组──

Bağımlılık analiz 2010'larda kazanıldı çünkü diller arasında, özellikle de serbest kelime sırası olanları temiz bir şekilde genelleştirir.

> 依存分析 2010'larda yenildi, çünkü bu diller arasında daha çok yaygınlaşmıştır, özellikle özgürlükçe konuşmacılık.

```
running is ROOT
cats is nsubj of running
were is aux of running
at is prep of running
3pm is pobj of at
```

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
pos-tagger
```

```figure
dependency-arcs
```

## Yapın

### Adım 1: En sık etiketlenen başlangıç çizgisi

Çalışan en aptal POS etiketçisi. Her kelime için, eğitimde en sık kullandığı etiketleri tahmin et.

> En son kullanılan POS etiketleme cihazı. Her kelime için, eğitimde en sık kullanılan etiketleri tahmin etmektedir.

```python
from collections import Counter, defaultdict


def train_mft(train_examples):
    word_tag_counts = defaultdict(Counter)
    all_tags = Counter()
    for tokens, tags in train_examples:
        for token, tag in zip(tokens, tags):
            word_tag_counts[token.lower()][tag] += 1
            all_tags[tag] += 1
    word_best = {w: c.most_common(1)[0][0] for w, c in word_tag_counts.items()}
    default_tag = all_tags.most_common(1)[0][0]
    return word_best, default_tag


def predict_mft(tokens, word_best, default_tag):
    return [word_best.get(t.lower(), default_tag) for t in tokens]
```

Brown'un korpusunda, bu temel çizgi %85 doğruluğa ulaştı.

> Brown 语料库上, bu çizgi yaklaşık %85 doğruluk oranına ulaşmıştır.

### Adım 2: Bigram HMM etiketlemeci

Düzeneğin ortak olasılığını modelleyin:

> 建模序列的联合概率:

```
P(tags, words) = prod P(tag_i | tag_{i-1}) * P(word_i | tag_i)
```

İki tablo: geçiş olasılığı (önceki etiket verilen etiket), emisyon olasılığı (söz verilen etiket).

> 两个表:转移概率 (→ 转移概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射概率 (→ 发射概率)  发射率)  发射 (→ 发射率)  发射率)  发射 (→ 发射率) 发射率)  发射 (→ 发射率) 发射率) 发射 (→ 发射率) 发射率) 发射 (→ 发射率) 发射 (→ 发射) 发射) 发射 (→ 发射) 发射) 发射 (→ 发射) 发射) 发射) 发射 (→ 发射) 发射) 发射 (→ 发射) 发射) 发射 (→ 发射) 发射) 发射 (→ 发射) 发射) 发射 (→

```python
import math


def train_hmm(train_examples, alpha=0.01):
    transitions = defaultdict(Counter)
    emissions = defaultdict(Counter)
    tags = set()
    vocab = set()

    for tokens, ts in train_examples:
        prev = "<BOS>"
        for token, tag in zip(tokens, ts):
            transitions[prev][tag] += 1
            emissions[tag][token.lower()] += 1
            tags.add(tag)
            vocab.add(token.lower())
            prev = tag
        transitions[prev]["<EOS>"] += 1

    return transitions, emissions, tags, vocab


def log_prob(table, given, key, smooth_denom, alpha):
    return math.log((table[given].get(key, 0) + alpha) / smooth_denom)


def viterbi(tokens, transitions, emissions, tags, vocab, alpha=0.01):
    tags_list = list(tags)
    n = len(tokens)
    V = [[0.0] * len(tags_list) for _ in range(n)]
    back = [[0] * len(tags_list) for _ in range(n)]

    for j, tag in enumerate(tags_list):
        em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
        tr_denom = sum(transitions["<BOS>"].values()) + alpha * (len(tags_list) + 1)
        tr = log_prob(transitions, "<BOS>", tag, tr_denom, alpha)
        em = log_prob(emissions, tag, tokens[0].lower(), em_denom, alpha)
        V[0][j] = tr + em
        back[0][j] = 0

    for i in range(1, n):
        for j, tag in enumerate(tags_list):
            em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
            em = log_prob(emissions, tag, tokens[i].lower(), em_denom, alpha)
            best_prev = 0
            best_score = -1e30
            for k, prev_tag in enumerate(tags_list):
                tr_denom = sum(transitions[prev_tag].values()) + alpha * (len(tags_list) + 1)
                tr = log_prob(transitions, prev_tag, tag, tr_denom, alpha)
                score = V[i - 1][k] + tr + em
                if score > best_score:
                    best_score = score
                    best_prev = k
            V[i][j] = best_score
            back[i][j] = best_prev

    last_best = max(range(len(tags_list)), key=lambda j: V[n - 1][j])
    path = [last_best]
    for i in range(n - 1, 0, -1):
        path.append(back[i][path[-1]])
    return [tags_list[j] for j in reversed(path)]
```

Brown'daki Bigram HMM'nin %93 doğruluğu %85'ten %93'e kadar sıçrama olasılığı çoğunlukla geçiş olasılığıdır.`DET NOUN`- Bu çok yaygın ve`NOUN DET`Nadir bir durum.

> Brown 语料库上二元组 HMM  yaklaşık % 93 doğruluk oranına ulaştı. % 85'ten % 93'e kadar atlama, çoğunlukla dönüşüm olasılığından kaynaklanıyor.`DET NOUN`Bu çok normal.`NOUN DET`Bu çok nadir.

### Adım 3: modern etiketçiler neden bunu yendi

Değişim + emisyon olasılığı yerel.`saw`"Bir testere aldım" isimli bir isim, "Filmi gördüm" fiili ise "Filmi gördüm" filidir. "Özenli özellikleri olan bir CRF (sufiks, kelime şekli, kelimeden önce ve sonra, kelime kendisi) ~ 97%'e ulaşır. BiLSTM-CRF veya transformatör ~98%+'e ulaşır.

> 转移 + 发射概率 is局部的──它们无法捕获`saw`"Bir kürsü aldım" içi isim kelimeleridir, ama "Filmi gördüm" içi ise, "Hızlı bir hareketli ifade" içi.

Bu görev için tavan, yorumcu anlaşmazlığı ile belirlenir. İnsan yorumcuları Penn Treebank'ta yaklaşık %97'de aynı fikirde. %98'den önceki modeller muhtemelen test setine fazla uymaktadır.

> Bu görev için yapılan planın belirtici tarafından belirlenmesi ayrılıktır. İnsan belirticilerinin Penn Treebank'ta 97%'i üzerinde bir anlaşma yapmıştır.

### Adım 4: bağımlılık analiz çizelgesi

Tam bir bağımlılık sıfırdan analiz etmek kapsamının dışındadır; kanonik derslik tedavisi Jurafsky ve Martin'de.

> Züre'den tam bir bağımlılık analizinin aşamasını; klasik dersler işleme Jurafsky ve Martin.

- **Transition-based**Parserler (arc-eager, arc-standard) bir shift-reduce parser gibi hareket eder: simgeler okuyor, onları bir yığın üzerine taşıyor ve ark oluşturan azaltma eylemlerini uyguluyor. Açgözlülük çözümü hızlıdır. Klasik uygulaması MaltParser. Modern sinirsel sürüm: Chen ve Manning'in geçiş tabanlı parser.
  **基于转移的**解析器(arc-eager、arc-standard) 解析器 gibi çalış:读进代币,移进到上,应用创建弧的归约动作──贪解码很快──经典实现是MaltParser──现代神经版本:Chen 和 Manning 的基于转移的解析器──
- **Graph-based**Parserler (Eisner'ın algoritması, Dozat-Manning biafin) baş bağımlısı olan her kenarı notlar ve maksimum uzanan ağaç seçer.
  **基于图的**解析器(Eisner 算法、Dozat-Manning 双仿射) 边打分,选择最大生成树──更慢但更准确──

Uygulamalı çalışmaların çoğu için spaCy'yi arayın:

>  çoğu uygulama için, spacy'yi kullanın:

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running at 3pm.")
for token in doc:
    print(f"{token.text:10s} tag={token.tag_:5s} pos={token.pos_:6s} dep={token.dep_:10s} head={token.head.text}")
```

```
The        tag=DT    pos=DET    dep=det        head=cats
cats       tag=NNS   pos=NOUN   dep=nsubj      head=running
were       tag=VBD   pos=AUX    dep=aux        head=running
running    tag=VBG   pos=VERB   dep=ROOT       head=running
at         tag=IN    pos=ADP    dep=prep       head=running
3pm        tag=NN    pos=NOUN   dep=pobj       head=at
.          tag=.     pos=PUNCT  dep=punct      head=running
```

Oku `dep`sütun altından yukarıya ve cümlenin dilbilgisel yapısı düşüyor.

> Aşağıdan yukarıya oku`dep`列,句子的语法结构就自然呈现了──

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

Her üretim NLP kütüphanesi standart bir boru hattının bir parçası olarak POS ve bağımlılık parserlerini gönderir.

> Her üretilen NLP depoları POS ve bağımlı çözücülerin standart akış hattının bir parçası olarak sağlanmaktadır.

- **spaCy**(`en_core_web_sm`- Ne ?`md`- Ne ?`lg`- Ne ?`trf`). Hızlı, doğru, tokenizasyon + NER + lemmatizasyon ile entegre. `token.tag_`- Evet .`token.pos_`(UD), `token.dep_`( bağımlılık ilişkisi).
  **spaCy**(`en_core_web_sm`- Ne ?`md`- Ne ?`lg`- Ne ?`trf`)──快速、准确,与分词 + NER + 词形还原集成──`token.tag_`- Evet.`token.pos_`(UD)`token.dep_`(Bayanlık)
- **Stanford NLP (stanza)**Stanford'un CoreNLP'nin ardıcısı 60'dan fazla dilde en son teknoloji.
  **Stanford NLP (stanza)**❖ Stanford CoreNLP'nin ardıcı.
- **trankit**Transformer tabanlı, iyi bir UD doğruluğu.
  **trankit**❖ Transformer'a dayalı, iyi bir UD 准确率──
- **NLTK**- Evet .`pos_tag`Kullanılabilir, yavaş, yaşlı, öğretim için iyi.
  **NLTK**- Evet.`pos_tag`❖ kullanılabilir ❖慢、较旧──适合教学──

### 2026'da bu hala önemli olan yerlerde

- **Lemmatization.**Ders 01'de POS'un doğru şekilde lematize olması gerekiyor.
  **词形还原。**İlk sınıfı, "Sevgi" olarak adlandırılan bir sözcük.
- **Structured extraction from LLM outputs.**Yaratılan cümlenin dilbilgilerle ilgili kısıtlamalara (örneğin, konu-ketim anlaşması, gerekli değişiklikler) saygı göstermesini doğrulayın.
  **LLM 输出的结构化抽取。**验证生成的句子满足语法约束 (doğrusu, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru, doğru)
- **Aspect-based sentiment.**Bağımlılık analizleri hangi adetifin hangi isim değiştirdiğini söyler.
  **基于方面的情感分析。**依存分析 size hangi isimleri değiştirdiğini söyler.
- **Query understanding.**"Bill Murray'nin başrolde olduğu Wes Anderson yönettiği filmler" analiz yoluyla yapılandırılmış kısıtlamalara ayrılır.
  **查询理解。**"Bill Murray'nin başrolde olduğu Wes Anderson yönettiği filmler"
- **Cross-lingual transfer.**UD etiketleri ve bağımlılık ilişkileri dil-agnostiktir ve yeni dillerin sıfır çekim yapılmış analizini mümkün kılar.
  **跨语言迁移。**UD 标签和依赖与语言无关,支持新语言的零样本结构化分析──
- **Low-compute pipelines.**Eğer bir transformatör gönderemezsen, POS + bağımlılık analizi + gazetteer şaşırtıcı derecede uzaklara gider.
  **低算力流水线。**Eğer Transformer'ı dağıtamazsan, POS'u kullan + bağımlılık analiz + Yerleşim kelimesi seni oldukça uzakta bırakır.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-grammar-pipeline.md`- ...

> 保存为 `outputs/skill-grammar-pipeline.md`- ...

```markdown
---
name: grammar-pipeline
description: Design a classical POS + dependency pipeline for a downstream NLP task.
version: 1.0.0
phase: 5
lesson: 07
tags: [nlp, pos, parsing]
---

Given a downstream task (information extraction, rewrite validation, query decomposition, lemmatization), you output:

1. Tagset to use. Penn Treebank for English-only legacy pipelines, Universal Dependencies for multilingual or cross-lingual.
2. Library. spaCy for most production, stanza for academic-grade multilingual, trankit for highest UD accuracy. Name the specific model ID.
3. Integration pattern. Show the 3-5 lines that call the library and consume the needed attributes (`.pos_`, `.dep_`, `.head`).
4. Failure mode to test. Noun-verb ambiguity (`saw`, `book`, `can`) and PP-attachment ambiguity are the classical traps. Sample 20 outputs and eyeball.

Refuse to recommend rolling your own parser. Building parsers from scratch is a research project, not an application task. Flag any pipeline that consumes POS tags without handling lowercase/uppercase variants as fragile.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Egzersizler.

1. **Easy.**Küçük bir etiketleme korpusunda en sık etiketlenen temel çizgiyi kullanarak (örneğin NLTK'nin Brown alt kümesi), beklenen cümlelerde doğruluğu ölçün. ~ 85% sonucu doğrulayın.
   **简单。**NLTK'nin Brown 子集ı gibi küçük bir etiket sözcükte en sık kullanılan etiket tabanı, bir cümleye doğrulama oranını ölçmek için %85'e kadar sonuç verilir.
2. **Medium.**Yukarıdaki büyük HMM'yi eğit ve her etiket için doğru bir raporu gönder.
   **中等。**訓練上述二元组 HMM并報告每标签精确率/召回率──HMM En kolay karıştığı hangi etiketler?
3. **Hard.**spaCy'nin bağımlılık analizi kullanarak 1000 cümlelik bir örnekten konu-ketim-objek üçlüler çıkarın. 50 elle etiketlenen üçlü üzerinde değerlendirin. Çekim başarısız olduğu belge (sık sık pasifler, koordinatlar ve uzak konular).
   **困难。**Spasi'nin bağımlılık analizi kullanılarak 1000 cümle örneğinden başlıca üçlü gruptan alınan değerlendirmeler yapılır.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Anahtar Şartlar .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| POS tag（词性标签） | Word's type / 词的类型 | Grammatical category. PTB has 36; UD has 17. / 语法类别。PTB 有 36 个；UD 有 17 个。 |
| Penn Treebank | Standard tagset / 标准标签集 | English-specific. Fine-grained verb tenses and noun number. / 特定于英语。细粒度的动词时态和名词数。 |
| Universal Dependencies（通用依存） | Multilingual tagset / 多语言标签集 | Coarser than PTB; language-neutral; defaults for cross-lingual work. / 比 PTB 更粗；语言无关；跨语言工作的默认选择。 |
| Dependency parse（依存分析） | Sentence tree / 句子树 | Each word has one head, each edge has a grammatical relation. / 每个词有一个中心词，每条边有一个语法关系。 |
| Viterbi（维特比算法） | Dynamic programming / 动态规划 | Finds the highest-probability tag sequence given emissions and transitions. / 给定发射和转移概率，找到最高概率的标签序列。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.

## Daha fazla okumak

- [Jurafsky and Martin — Speech and Language Processing, chapters 8 and 18](https://web.stanford.edu/~jurafsky/slp3/) POS ve analizleme konusunda kanonik derslik tedavisi. / POS 和解析的经典教科书处理──
- [Universal Dependencies project](https://universaldependencies.org/) her çok dilli araştırmacı tarafından kullanılan diller arası etiket kümesi ve ağaç bankası koleksiyonu. / 每个多语言解析器使用的跨语言标签集和树库集合。
- [spaCy linguistic features guide](https://spacy.io/usage/linguistic-features)  `Token`- Hayır .`Token`Yukarıdaki her bir özellik için pratik referans.
- [Chen and Manning (2014). A Fast and Accurate Dependency Parser using Neural Networks](https://nlp.stanford.edu/pubs/emnlp2014-depparser.pdf) sinir parçacıklarını ana akışa getiren makale. / 将神经解析器带入主流的论文.
