# Çözümleme Çözümleri

> "O, onu aradı. cevap vermedi. Doktor öğle yemeğindeydi". İki kişiye üç referans ve kimse adı verilmedi.
> "O onu aradı. O cevap vermedi. Doktor öğle yemeğindeydi".

> **【中文解读】**Metin içindeki sözcükleri ve isimleri, onların ifade ettiği varlıklara bağlanır.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Coreference çözünürlüğü aynı birliğe atfeden her ifadesi birleştirir. "Barack Obama", "prezident", "o", "Obama" hepsi bir kişiye işaret eder.

> "Barack Obama", "Prezident""",O""",Obama" hepsi bir kişiye işaret eder.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği nasıl gerçek tasarımda doğru şekilde anlayabilir ve uygulayabilirsiniz.

2026'da neden önemli: LLM'ler, bağlam pencerelerinde içerikli olarak coreference ile ilgilenir, ancak RAG kurtarma hala açık bir çözüme ihtiyaç duyar. Bir kullanıcı "ne dedi?" sorarsa, kurtarıcı doğru parçayı bulmadan önce "o" nin kim olduğunu bilmelidir.

> 2026 yıl neden önemli:LLM On the Upper Downline Window'da gizli işlem ortaklığı gösterir, ancak RAG 检索 hala açıkça çözülmesi gerekiyor.

## Konsepten bir şey.

> **【中文解读】**本節介绍核心概念和理论基础──

**Mention detection.**Bir varlığı ifade edebilecek tüm isim cümlelerini ve adın isimleri bulun.

> **指称检测。**找到所有可能指向实体名词短语和代词──使用 POS 标签和分析树──

**Coreference clustering.**Gruplar aynı varlıktan bahsedilenleri belirtir. Bahsedilen çift sınıflandırıcıları, uzaya dayalı modeller veya sonundan sonuna sinirsel yaklaşımlar (Lee et al., 2017).

> **共指聚类。**Aynı varlığın tanımını ayırt etme biçimi, sınıflandırma biçimi, çaprazlı bir model veya sonuna kadar sinir yöntemi üzerine kurulmuş bir biçimdir.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'ye kadar, NLP alanında "her görev bir model eğitimi"nden "her görevyi çözmek için bir model" biçimindeki bir değişim yaşandı.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG)   检索增强生成 (RAG)  RAG)   检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成) 检索增强生成 (RAG) 检索增强生成 (RAG) 检测增强生成) 检测增强生成 (RAG) 检测增强生成) 检测增强的架构 (RAG) 检测) 检测增强的架构

> **【拓展：NLP 的多语言挑战】**Dünya çapında 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve birkaç dil üzerinde yoğunlaşmaktadır.
```figure
coref-links
```

## Yapın

## Yapın.

> **【中文解读】**Bu bölüm kodla birlikte, çekirdek algoritmasını da tamamlıyor.

```python
import spacy

nlp = spacy.load("en_core_web_sm")

def resolve_coref(text):
    doc = nlp(text)
    clusters = {}
    for token in doc:
        if token.pos_ == "PRON":
            # Simple heuristic: look for nearest preceding noun
            for t in reversed(list(doc[:token.i])):
                if t.pos_ in ("NOUN", "PROPN"):
                    clusters[token.text] = t.text
                    break
    return clusters
```

> **【中文解读】**Bu bölüm, bu teknolojiyi nasıl hızlı bir şekilde uygulayacağımızı gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi.

## Çerçeveyi kullanın.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl deploye edileceği üzerinde yoğunlaşmaktadır.

- **spaCy with coreferee.**İngilizce için üretim temel referansı. / spaCy + coreferee。英语生产共指。
- **Hugging Face span-based models.**Nöral çekirdek çözünürlüğü. / Öğünmüş Yüz 基于跨度的模型──
- **LLM prompting.**Yüksek lisans uzmanından temel referansları çözmesini iste.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-coref-picker.md`- ...

> 保存为 `outputs/skill-coref-picker.md`- ...

```markdown
Given a text and need for entity tracking, pick coreference approach.
1. Rule-based vs neural vs LLM.
2. Language support.
3. Latency budget.
```

## Egzersizler.

1. **Easy.**POS etiketleri kullanarak isim çözünürlüğünü uygulayın. / **简单。**POS 标签实现代词消解──
2. **Medium.**50 cümlelik bir kurpus üzerinde bir araştırma yaparak yargıç değerlendirilir.**中等。**50 cümle dil teriminde değerlendirme yapılması için.
3. **Hard.**Çimdikleme öncesi coreferansları çözen bir RAG preprocessor yapın.**困难。**构建在分块前消解共指的RAG 预处理器──

## Anahtar Şartlar .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Coreference（共指） | Multiple expressions referring to the same entity. / 多个表达指向同一实体。 |
| Mention（指称） | A textual reference to an entity. / 对实体的文本引用。 |
| Anaphora（回指） | Pronoun referring to an earlier noun. / 代词指向前面的名词。 |

## Daha fazla okumak

- [Lee et al. (2017). End-to-end Neural Coreference Resolution](https://arxiv.org/abs/1707.07045) 跨度 (span) tabanlı yaklaşım.
- [coreferee](https://github.com/explosion/coreferee) spaCy coreference eklentisi. / spaCy 共指插件──
