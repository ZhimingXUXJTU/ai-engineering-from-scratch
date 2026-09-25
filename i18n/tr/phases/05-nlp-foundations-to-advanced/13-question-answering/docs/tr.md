# Soru cevaplama sistemleri.

> Üç sistem modern bilgi akimiyetini şekillendirdi. Ekstraktif bulma alanları. Arama ile güçlendirilmiş belgelere yerleştirildi. Geliştirici cevaplar üretildi. Her modern AI asistanı üçün bir karışımıdır.
> Üç sistem modern soru cevapları oluşturdu. Çekim biçimi, metin parçalarını buldu.

> **【中文解读】**Bilgi aramasından soru sorma biçimine kadar RAK bir soru sorma sistemi haline gelmiştir.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 11 (Machine Translation), Phase 5 · 10 (Attention Mechanism) | **前置知识:** Phase 5 · 11 (Machine Translation), Phase 5 · 10 (Attention Mechanism)
**Time:** ~75 minutes | **时间:** ~75 minutes


## Sorunlar. Sorunlar.

Bir kullanıcı "İlk iPhone ne zaman piyasaya sürüldü?" diye yazar ve "29 Haziran 2007" diye bekler. "Apple'ın tarihi uzun ve çeşitli". değil. "2007" diye değil.
> User输入 "İlk iPhone ne zaman piyasaya sürüldü?"并期望得到 "29 Haziran 2007."──不是"Apple'ın tarihi uzun ve çeşitli.""不是孤立的"2007" 没有句子上下文──一个直接、有据可依、正确的答案──

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.


Son on yılda üç mimarlık, kaliteyi yönetiyor.
> Son on yılda üç yapı soru cevapları yönlendirdi.

- **Extractive QA.**Cevabı içeren bilinen bir soru ve bir pasaj verildiğinde, pasajda cevap aralığının başlangıç ve son indekslerini bul. SQuAD kanonik referans ölçüsüdür.
- **Open-domain QA.**Geçit verilmiyor. Önce ilgili geçitleri alın, sonra bir cevap çıkarın veya oluşturun. Bu gün RAG boru hattının temel taşıdır.
- **Generative / Closed-book QA.**Büyük bir dil modeli parametrik hafızasından cevap verir.
> - **抽取式问答（Extractive QA）。**给定一个问题和已知含答案的段落,找到答案在段落中的起和结索引──SQuAD is classic基准──
- **开放域问答（Open-domain QA）。**段落未给定──先检查相关段落,然后抽取或生成答案──这是当今每个RAG流水线的基石──
- **生成式/闭卷问答（Generative / Closed-book QA）。**Büyük dil modelinden parametrize edilmiş hafıza cevapları.

2026'daki eğilim hibriddir: en iyi birkaç pasajı geri almak, sonra da bu pasajlarda yerleşik bir cevap vermesi için bir jeneratif model oluşturmak. Bu RAG, ve ders 14 geri alım yarısını derinlemesine kapsar. Bu ders, QA yarısını oluşturur.
> 2026 yılının eğilimleri bir karışımdır: en iyi birkaç bölüm araştırmak, sonra bu bölümlerin temelinde cevaplar üretmek için bir model oluşturmak.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


![QA architectures: extractive, retrieval-augmented, generative](../assets/qa.svg)
> ![问答架构：抽取式、检索增强、生成式](../assets/qa.svg)

**Extractive.**Bir transformatörle birlikte soru ve geçiş kodlayın (BERT ailesi). Cevabın başlangıç ve son belirtiler indeksi tahmin eden iki başı eğitiniz. Kayıp geçerli pozisyonlar üzerinde çapraz entropi. Çıkış geçiden bir uzaktır. Asla halüsinasyon yapmaz (konstrüksiyonla), asla geçiş cevaplayamayacak soruları ele almaz (konstrüksiyonla).
> **抽取式。**Transformer(BERT 系列) birlikte kodlama sorusu ve bölümleri。 eğitim iki tahmin cevapları başlangıç ve son belirti 索引の头。損失は有効位置上の交叉──输出は段落の中の一段。

**Retrieval-augmented (RAG).**İki aşamada. Birincisi, bir retriever üstü bulur.`k`Bir kitapçıkta bir bölümden bir bölüm bulunur. İkincisi, bir okuyucu (ekstraktif veya jeneratif) bu bölümleri kullanarak cevap üretir. Retriever-okuyucu bölünmesi her birinin bağımsız olarak eğitilmesine ve değerlendirilmesine izin verir. Modern RAG genellikle aralarında bir reranker ekler.
> **检索增强（RAG）。**Birinci aşamada, konuşma kütüphanesinden en üstünü bul.`k`段落──第二,阅读器(抽取式或生成式) bu bölümleri kullanarak cevaplar üretmek için kullanılır.

**Generative.**Sadece dekodörlü bir LLM (GPT, Claude, Llama) öğrenilen ağırlıklardan cevaplar verir. İzleme adımları yoktur. Genel bilgiye mükemmel, nadir veya son gerçeklerde felaketli. Halüsinasyon oranı eğitim öncesi verilerdeki gerçek sıklığı ile ters olarak ilişkilidir.
> **生成式。**仅解码器的 LLM(GPT、Claude、Llama) öğrenilenlerin ağırlığından cevaplar──无检索步骤──常见知识上出色,在罕见或近期事实上灾难性──幻觉率与预训数据中的事实频率负相关──

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.


## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

```figure
qa-span
```

## Yapın

### Adım 1: önceden eğitilmiş bir model ile ekstraksiyonsal QA
> `deepset/roberta-base-squad2`SQUAD 2.0'da cevaplanamayan sorular bulunmaktadır.`question-answering`流水線返回最高得分的片段, even the model's空分数胜出 it does not automatically return to空答案── 流水线返回最高得分的片段, even the model's空分数胜出 it does not automatically return to空答案── 流水线调用中传入`handle_impossible_answer=True`Su akışı sadece boş bölümlerin sayısını aşırır.`score`- Evet.

```python
from transformers import pipeline

qa = pipeline("question-answering", model="deepset/roberta-base-squad2")

passage = (
    "Apple Inc. released the first iPhone on June 29, 2007. "
    "The device was announced by Steve Jobs at Macworld in January 2007."
)
question = "When was the first iPhone released?"

answer = qa(question=question, context=passage)
print(answer)
```

```python
{'score': 0.98, 'start': 57, 'end': 70, 'answer': 'June 29, 2007'}
```

`deepset/roberta-base-squad2`Bu program, cevaplanamayan sorular içeren SQuAD 2.0 üzerinde eğitim almıştır.`question-answering`pipeline, modelin sıfır puanı kazanırsa bile en yüksek puan alanı gönderir  *not* otomatik olarak boş bir cevap gönderir. Açık bir " cevap verilmemesi " davranışını elde etmek için geç `handle_impossible_answer=True`Pipeline çağrısına: Pipeline, yalnızca sıfır puan her zaman puanı aşırsa boş bir cevap verir.`score`Her iki taraftan da.
> 两段流水线──密检索器(Sentence-BERT) 通过语义相似度找到相关段落──抽取式阅读器(RoBERTa-SquAD) 合并的顶段落中提取答案片段──适用于小语料库──对百万级文档语料,使用 FAISS或向量数据库──

### Adım 2: Arama ile artırılmış bir boru hattı (sket)
> 提示模式 çok önemlidir. Açıkça anlatın ki, model yukarıdaki aşağıdaki cevaplara dayanır ve aşağıdaki aşağıdaki yetersizliğe dayanırken "Bilmiyorum" diye cevap verir.

```python
from sentence_transformers import SentenceTransformer
import numpy as np

encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

corpus = [
    "Apple Inc. released the first iPhone on June 29, 2007.",
    "Macworld 2007 featured the iPhone announcement by Steve Jobs.",
    "Android launched in 2008 as Google's mobile operating system.",
    "The first iPod was released in 2001.",
]
corpus_embeddings = encoder.encode(corpus, normalize_embeddings=True)


def retrieve(question, top_k=2):
    q_emb = encoder.encode([question], normalize_embeddings=True)
    sims = (corpus_embeddings @ q_emb.T).squeeze()
    order = np.argsort(-sims)[:top_k]
    return [corpus[i] for i in order]


def answer(question):
    passages = retrieve(question, top_k=2)
    combined = " ".join(passages)
    return qa(question=question, context=combined)


print(answer("When was the first iPhone released?"))
```

İki aşamalı boru hattı. Dense retriever (Sentence-BERT) anlamlı benzerlik ile ilgili pasajlar bulur. Ekstraktif okuyucu (RoBERTa-SquAD) top pasajlardan cevap aralığını çekir. Küçük korpuslarda çalışır.
> SQUAD kullanımı**精确匹配（Exact Match, EM）**和 **token 级 F1**◦ EM, birleştirilmesinden sonra yapılan ciddi bir uyumdur. ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦ ◦    ◦ ◦  ◦

### Adım 3: RAG ile üreticidir
> 对于生产问答:

```python
def rag_generate(question, llm):
    passages = retrieve(question, top_k=3)
    prompt = f"""Context:
{chr(10).join('- ' + p for p in passages)}

Question: {question}

Answer using only the context above. If the context does not contain the answer, say "I don't know."
"""
    return llm(prompt)
```

Hızlı bir örneğe önem verir. Modele bağlamda yerleştirilmesini açıkça söylemek ve bağlam yetersiz olduğunda "Bilmiyorum" diyerek halüsinasyon oranlarını naif bir uyarı ile karşılaştırıldığında 40-60% azaltır. Daha karmaşık örnekler alıntılar, güven puanları ve yapılandırılmış çıkarma ekler.
> - **答案准确率**(LLM 评判或人工评判,因为指标不捕获语义等价)
- **引用准确率。**引用的段落是否实际支持答案? 引用和检索段落 arasındaki字符串匹配即可轻松自动检查──
- **拒绝校准。**Cevaplar verilecekken sistem doğru bir şekilde "Bilmiyorum" diyor mu?
- **检索召回率。**Değerlendirme okuyucuyu kullanmadan önce, ölçüm kontrolcü, doğru bir şekilde üst katına yerleştirilir mi?`k`❖ Reader: Can't Repair Missing Seqment:

### Dördüncü adım: Gerçek dünyayı yansıtan değerlendirme
> `RAGAS`专为RAG 系统构建,是2026年发布默认选择――它在不需要黄金参考的情况下从四维度评分:

SQuAD kullanımı **Exact Match (EM)**ve **token-level F1**- Evet . EM, normallaşmadan sonra sıkı bir eşleşme (büyük yazılar, çizgi noktalama, makale çıkarma)  ya tahmin tam olarak eşleşir ya da 0 puan alır. F1 tahmin ve referans arasındaki token örtüşmesi üzerinden hesaplanır ve kısmi kredi verir. Her iki kredi altındaki parafrasi: "29 Haziran 2007" vs "29 Haziran 2007" tipik olarak 0 EM (ordinal kesinti normallaşması) alır, ancak yine de üst üste gelen jetonlardan önemli bir F1 kazanır.
> - **忠实度（Faithfulness）。**Cevaptaki her açıklama, sorunun üst üstelik aşağıdaki metrajından mı kaynaklanıyor?
- **答案相关性。**答案是否回应了问题? 答案den ortaya çıkan varsayılan sorunun gerçek soruna karşılaştırılması ve ölçülmesi yoluyla
- **上下文精确率。**检索的块中, 检索的块中, 检索的块中, 检索的块中, 检索的块中, 检索的块中, 检索的块中, 检索的块中, 检索的块中, 检索的块中, 检索的块中, 检索的块中, 检索的块中, 检索的块中, 检索的块中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的噪音中, 检索的
- **上下文召回率。**检索集是否包含所有需要的信息?

Üretim için QA:
> 无参考评分让你可以在实时生产流量上评估,无需策划黄金答案――精确匹配指标无用的开放式问题上叠加 LLM 评委――

- **Answer accuracy**(LLM veya insan tarafından değerlendirilmiş, çünkü ölçümler semantik eşdeğerliği yakalamamaktadır).
- **Citation accuracy.**İfadelenen pasaj gerçekten cevabı destekliyor mu?
- **Refusal calibration.**Cevap alınan bölümlerde bulunmadığında, sistem doğru bir şekilde "Bilmiyorum" der mi?
- **Retrieval recall.**Okuyucuyu değerlendirmeden önce, geri alıcıya en üst kısmına doğru geçiş sağlıyor mu ölçün.`k`Bir okuyucu kayıp bir pasajı düzeltemez.
> `pip install ragas`△ Kontrol cihazına bağlanmak △ okuyucu △ her sorgu dört karakter elde etmek △ geri dönüş zaman rapor △

### RAGAS: 2026 üretim değerlendirme çerçevesini

`RAGAS`RAG sistemleri için özel olarak inşa edilmiş ve 2026'da gemilerde standart olarak kullanılır. Altın referansların gereksiz olduğu dört boyutlu bir puan elde eder:

- **Faithfulness.**Cevabın her iddiası alınan bağlamdan geliyor mu?
- **Answer relevance.**Cevabın soruyu cevapladığını mı? Cevabın hipotetik soruları oluşturarak ve gerçek soruya karşılaştırarak ölçülür.
- **Context precision.**Alınan parçalardan hangi bölümü gerçekten önemli?
- **Context recall.**Alınan set tüm gerekli bilgileri içeriyor muydu? Düşük hatırlama = okuyucu başarılı olamaz.

Referanssız puanlama, canlı üretim trafiğini kurate altın cevaplar olmadan değerlendirmenizi sağlar.

`pip install ragas`Retriever + Reader'i bağlayın, her soruya 4 skalar alın.

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

2026'da.
> 2026 yıl teknik ──

| Use case | Recommended |
|---------|-------------|
| Given passage, find answer span | `deepset/roberta-base-squad2` |
| Over a fixed corpus, closed-book not acceptable | RAG: dense retriever + LLM reader |
| Real-time over a document store | RAG with hybrid (BM25 + dense) retriever + reranker (lesson 14) |
| Conversational QA (follow-up questions) | LLM with conversation history + RAG on each turn |
| Highly factual, regulated domains | Extractive over an authoritative corpus; never generative alone |
> Şekil kullanma önerisi
|---------|------|
| 给定段落，找答案片段 | `deepset/roberta-base-squad2` |
| 固定语料上，闭卷不可接受 | RAG：稠密检索器 + LLM 阅读器 |
| 实时文档存储 | RAG 配混合（BM25 + 稠密）检索器 + 重排序器（第 14 课） |
| 对话式问答（追问） | 带对话历史的 LLM + 每轮 RAG |
| 高度事实性、受监管领域 | 在权威语料上的抽取式；永远不要单独用生成式 |

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


Ekstraktif QA 2026'da modası kalmadı çünkü LLM ile RAG daha fazla dava ele alıyor.
> Çekilme biçimindeki sorular 2026 yılında popüler olmaya başladı, çünkü LLM ile RAG daha fazla durumla ilgileniyor.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-qa-architect.md`- ...
> 保存为 `outputs/skill-qa-architect.md`- ...

```markdown
---
name: qa-architect
description: Choose QA architecture, retrieval strategy, and evaluation plan.
version: 1.0.0
phase: 5
lesson: 13
tags: [nlp, qa, rag]
---

Given requirements (corpus size, question type, factuality constraint, latency budget), output:

1. Architecture. Extractive, RAG with extractive reader, RAG with generative reader, or closed-book LLM. One-sentence reason.
2. Retriever. None, BM25, dense (name the encoder), or hybrid.
3. Reader. SQuAD-tuned model, LLM by name, or "domain-fine-tuned DistilBERT."
4. Evaluation. EM + F1 for extractive benchmarks; answer accuracy + citation accuracy + refusal calibration for production. Name what you are measuring and how you are measuring it.

Refuse closed-book LLM answers for regulatory or compliance-sensitive questions. Refuse any QA system without a retrieval-recall baseline (you cannot evaluate the reader without knowing the retriever surfaced the right passage). Flag questions that require multi-hop reasoning as needing specialized multi-hop retrievers like HotpotQA-trained systems.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


## Egzersizler.

1. **Easy.**SQuAD çıkarım borusunu yukarıda 10 Wikipedia pasajına ayarlayın. El sanatı 10 soru. Cevabın ne kadar sık doğru olduğunu ölçün.
2. **Medium.**Bir reddetme sınıflandırıcısı ekleyin. En üst geri alınma puanı bir eğimden aşağı olduğunda (deyelim 0.3 cosine), okuyucuyu aramak yerine "Bilmiyorum" i geri verin. Eğimleri bir sürede tutunmuş bir set üzerinde ayarlayın.
3. **Hard.**Seçtiğiniz 10.000 belge korpusunda RAG boru hattı oluşturun. RRF füzyonu ile hibrit geri alımı (BM25 + yoğun) uygulayın (derse 14)
> 1. **简单。**SQAD 抽取式流水线──手工设计 10 问题──测量答案正确率──如果段落和问题干净,你应该看到7-9 个正确──
2. **中等。**添加拒绝分类器──当最高检索分数低于值(例如 0.3余弦) 当, "Bilmiyorum" yerine调用阅读器──在留出集上调整值──
3. **困难。**Seçtiğiniz 10.000 文档语料 üzerinde inşa RAG 流水线。 gerçekleştirmek karışık inceleme(BM25 + 密) artı RRF 融合(gör 14. ders)。 ölçüm var ve karışık adımların cevap doğruluk oranı。 hangi sorunun türünün en fazla faydalanmasını kaydetmek。

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive QA | Find the answer span | Predict start and end indices of the answer within a given passage. |
| Open-domain QA | QA over a corpus | No given passage; must retrieve then answer. |
| RAG | Retrieve then generate | Retrieval-augmented generation. Retriever + reader pipeline. |
| SQuAD | Canonical benchmark | Stanford Question Answering Dataset. EM + F1 metrics. |
| Hallucination | Made-up answer | Reader output not supported by retrieved context. |
| Refusal calibration | Know when to shut up | System correctly says "I don't know" when unable to answer. |
> # Sözcükler # İnsanlar her zaman söylerdi # Gerçek anlamı #
|------|-----------|---------|
| 抽取式问答 | 找答案片段 | 预测给定段落中答案的起始和结束索引。 |
| 开放域问答 | 语料上的问答 | 无给定段落；必须先检索再回答。 |
| RAG | 检索再生成 | 检索增强生成。检索器 + 阅读器流水线。 |
| SQuAD | 经典基准 | 斯坦福问答数据集。EM + F1 指标。 |
| 幻觉 | 编造答案 | 阅读器输出不被检索上下文支持。 |
| 拒绝校准 | 知道何时闭嘴 | 系统在无法回答时正确地说 "I don't know"。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) referans kağıdı.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906)DPR, QA için kanonik yoğun geri alıcı.
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)- RAG adını veren gazetede.
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997) kapsamlı RAG araştırması.
> - [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) 基准论文──
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, 问答的经典密检索器──
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) 命名 RAG 的论文──
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997) 综合 RAG 综述。
