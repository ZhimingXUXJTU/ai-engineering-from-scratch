# Bilgi Arama ve Arama Bilgi Arama ve Arama

> BM25 kesin ama kırılgan. Dense geniş bir ağ atıyor ama anahtar kelimeleri kaçırıyor. Hibrit 2026 varsayılan. Her şey ayarlanıyor.
> BM25 精确但脆弱──密检索撒大网但漏掉关键词──混合检索是2026 yılının öntanımlı seçimi──其余都是调参──

> **【中文解读】**RAK'ın araştırma makinesi, bilgi araştırmalarının uygulanmasıdır.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## Sorunlar. Sorunlar.

Kullanıcı "Birisi para almak için yalan söylerse ne olur" yazıyor ve aslında bu durumu kapsadığı statutu bulmayı bekliyor: "Bölüm 420 IPC". Anahtar kelime arama tamamen kaçırır ( paylaşımlı kelime kitlesi yoktur).
> Utentient输入 "kimsenin para almak için yalan söylediğinde ne olur?"并期望找到实际覆盖该内容的法规:"§ 420 IPC"──关键词搜索完全找不到它(没有共享词汇)──如果嵌入没有在法律文本上训练过,语义搜索也会错过它──真正搜索必须同时处理两者──

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.


IR, her RAG sistemi, her arama çubuğu, her dok sitesi'nin bulanık aramalarının altındaki boru hattıdır. 2026 mimarisi üretimde çalışan tek bir yöntem değildir.
> IR her RAG sistemidir, her arama , her dosya sitesi 模糊查找下流水线──2026 yılında üretimde geçerli olan yapı tek bir yöntem değildir── her birinin başarısızlığını yakalamak için bir dizi tamamlayıcı yöntem zinciri vardır──

Bu ders her yakalama başarısız olan her parçayı ve isimleri oluşturur.
> Bu ders, her bölümün hangi başarısızlıkları olduğunu belirtti.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.


## Konsepten bir şey.

![Hybrid retrieval: BM25 + dense + RRF + cross-encoder rerank](../assets/retrieval.svg)
> ![混合检索：BM25 + 稠密 + RRF + 交叉编码器重排序](../assets/retrieval.svg)

Dört katman, ihtiyacın olanları seç.
> Dört katı.

1. **Sparse retrieval (BM25).**Hızlı, tam eşleşmelerde doğru, semantikte berbat bir indeks, milyonlarca belge üzerinde sorgu başına 10 ms altındaki bir indeks, yasal referanslar, ürün kodları, hata mesajları, isimli varlıklar sağlıyor.
2. **Dense retrieval.**Enkodlama sorgu ve belgeleri vektörlere. En yakın komşu arama. Parafrases ve semantik benzerliği yakalar. Bir karakterle farklı olan tam anahtar kelime eşleşmelerini kaçırır. FAISS veya vektör DB ile sorgu başına 50-200 ms.
3. **Fusion.**Ranklı ve yoğun listeleri birleştirin. karşılıklı sıra birleşimi (RRF) kolay varsayımdır çünkü çiğ puanları (farklı ölçeklerde yaşayan) görmezden gelir ve yalnızca sıra pozisyonlarını kullanır.
4. **Cross-encoder rerank.**Top-30'u füzyondan alın. Bir çapraz kodlayıcı çalıştırın (soru + belge birlikte, her çiftin puanlanması). Top-5'ü tutun. çapraz kodlayıcılar çift başına iki kodlayıcılardan daha yavaş ama çok daha doğru.
> 1. **稀疏检索（BM25）。**快速、精确匹配准确、语义上糟糕──在倒排索引上运行──百万文档上每查询亚 10毫秒──正确处理法规引用、产品代码、错误消息、命名实体──
2. **稠密检索。**Bu nedenle, bu bilgiyi kullanmak için bir veri tabanında kullanmak gerekir.
3. **融合。**合并稀疏和密的排列列表──倒数排名融合(Reciprocal Rank Fusion, RRF) basit bir öntanımlı seçimdir, çünkü orijinal分数leri göz ardı eder.
4. **交叉编码器重排序。**Fusion Middle Get Top-30──运行交叉编码器(查询 + 文档一起,对每对打分)──保留 top-5──交叉编码器对双编码器慢但准确得多──你只在前-30 上运行来摊销成本──

Üç yönlü geri alım (BM25 + yoğun + SPLADE gibi öğrenilen boşluk) 2026'da iki yönlü referanslardan daha iyi performans gösterir, ancak öğrenilen boşluk indeksleri için altyapıya ihtiyaç duyar.
> Üç yol kontrolü (BM25 + 密 + 学习稀疏如 SPLADE) 2026 yılında iki yoldan daha iyi, ancak çok az yol göstergesi altyapısını öğrenmek gerekir. Çoğu ekip için iki yol da en iyi dengede yer alır.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.


## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

```figure
gx-hybrid-retrieval
```

## Yapın

### Adım 1: BM25 sıfırdan
> 两个参数值得了解──`k1=1.5`控制词频和;更高 anlamı daha büyük olan kelimenin tekrarlanması.`b=0.75`控制长度归结;0 忽略文档长度,1 完全归结;;默认值是罗伯茨顿 原始论文中的推值,很少需要调整;;

```python
import math
import re
from collections import Counter

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text):
    return TOKEN_RE.findall(text.lower())


class BM25:
    def __init__(self, corpus, k1=1.5, b=0.75):
        if not corpus:
            raise ValueError("corpus must not be empty")
        self.corpus = [tokenize(d) for d in corpus]
        self.k1 = k1
        self.b = b
        self.n_docs = len(self.corpus)
        self.avg_dl = sum(len(d) for d in self.corpus) / self.n_docs
        self.df = Counter()
        for doc in self.corpus:
            for term in set(doc):
                self.df[term] += 1

    def idf(self, term):
        n = self.df.get(term, 0)
        return math.log(1 + (self.n_docs - n + 0.5) / (n + 0.5))

    def score(self, query, doc_idx):
        q_tokens = tokenize(query)
        doc = self.corpus[doc_idx]
        dl = len(doc)
        freq = Counter(doc)
        score = 0.0
        for term in q_tokens:
            f = freq.get(term, 0)
            if f == 0:
                continue
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * dl / self.avg_dl)
            score += self.idf(term) * numerator / denominator
        return score

    def rank(self, query, top_k=10):
        scored = [(self.score(query, i), i) for i in range(self.n_docs)]
        scored.sort(reverse=True)
        return scored[:top_k]
```

Bilmeye değer iki parametredir.`k1=1.5`Bu nedenle, bu süreci daha fazla kullanmak için kullanılır.`b=0.75`Bu nedenle, bu işlemler, bir önceki yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yaz
> L2 归一化嵌入使点积等于余弦──`all-MiniLM-L6-v2` 384 维,快速,对大多数英语检索足够强──多语言工作使用 `paraphrase-multilingual-MiniLM-L12-v2`❖ En yüksek doğruluk oranı`bge-large-en-v1.5`Ya da`e5-large-v2`- Evet.

### Adım 2: İki kodlayıcı ile yoğun çekim
> `k=60`常数 来源原始RRF论文──更高的 `k`Rating farklarının katkıları dengelenmek; daha düşük `k`60'ın çıkardığı öntanımlı değer, çok az düzeltme gerektirir.

```python
from sentence_transformers import SentenceTransformer
import numpy as np


def build_dense_index(corpus, model_id="sentence-transformers/all-MiniLM-L6-v2"):
    encoder = SentenceTransformer(model_id)
    embeddings = encoder.encode(corpus, normalize_embeddings=True)
    return encoder, embeddings


def dense_search(encoder, embeddings, query, top_k=10):
    q_emb = encoder.encode([query], normalize_embeddings=True)
    sims = (embeddings @ q_emb.T).flatten()
    order = np.argsort(-sims)[:top_k]
    return [(float(sims[i]), int(i)) for i in order]
```

L2-normalize yerleşimleri böylece nokta ürünü cosine eşittir. `all-MiniLM-L6-v2`384 boyutlu, hızlı ve İngilizce'nin çoğu için yeterince güçlü.`paraphrase-multilingual-MiniLM-L12-v2`En yüksek doğruluk için,`bge-large-en-v1.5`veya `e5-large-v2`- Evet .
> Üç aşama birleştirme. BM25 搜尋词汇匹配──密找到语义匹配──RRF 合并两个排名不需要分数校准──交叉编码器使用查询-文档对重新对 top-30 打分,捕获双编码器遗漏的细粒度相关性──保留 top-5──

### Adım 3: Karşılıklı Rank Füzyonu
> # İşaret anlamı #
|------|------|
| Recall@k | 存在正确文档的查询中，正确文档在 top-k 中的比例 |
| MRR（平均倒数排名） | 第一个相关文档的 1/rank 的平均值 |
| nDCG@k | 考虑相关性分级，而非仅仅是二元的 相关/不相关 |

```python
def reciprocal_rank_fusion(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, (_, doc_idx) in enumerate(ranking):
            scores[doc_idx] = scores.get(doc_idx, 0.0) + 1.0 / (k + rank + 1)
    fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(score, doc_idx) for doc_idx, score in fused]
```

- Evet .`k=60`sabit orijinal RRF kağıdından geliyor.`k`Renk farklarının katkılarını düzeltir; daha düşük `k`60'ın yayınlanan standart olduğu ve nadiren ayarlanmasına ihtiyacı var.
> Özellikle de RAG,检索器**Recall@k**Eğer doğru bir bölümün arama odaklanmadıysa, okuyucu cevap veremez.

### Dördüncü adım: hibrit arama + yeniden sıralama
> 调试技巧:对于失败的查询,对稀疏和密排名──如果一个找到正确文档而另一个没有,你有词汇不匹配(修复:添加缺失的一半) 或语义歧义(修复:更好的嵌入或重排序器)──

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def hybrid_search(query, bm25, encoder, dense_embeddings, corpus, top_k=5, pool_size=30, reranker=reranker):
    sparse_ranking = bm25.rank(query, top_k=pool_size)
    dense_ranking = dense_search(encoder, dense_embeddings, query, top_k=pool_size)
    fused = reciprocal_rank_fusion([sparse_ranking, dense_ranking])[:pool_size]

    pairs = [(query, corpus[doc_idx]) for _, doc_idx in fused]
    scores = reranker.predict(pairs)
    reranked = sorted(zip(scores, [doc_idx for _, doc_idx in fused]), reverse=True)
    return reranked[:top_k]
```

BM25 sözlük eşleşmelerini bulur. Dense semantik eşleşmelerini bulur. RRF puan kalibrasyonuna ihtiyaç duymadan iki sıralamayı birleştirir. Cross-encoder sorgu-doküman çiftlerini birlikte kullanarak en üst-30'u yeniden puanlar.

### Adım 5: değerlendirme

| Metric | Meaning |
|--------|---------|
| Recall@k | Of queries where the correct document exists, how often is it in the top-k? |
| MRR (Mean Reciprocal Rank) | Average of 1/rank of first relevant document. |
| nDCG@k | Accounts for relevance gradations, not just binary relevant/not. |

Özellikle RAG için,**Recall@k**Eğer doğru pasaj alınmamış bir sette yoksa okuyucu cevap veremez.

Debugging tip: başarısız sorgular için, nadir ve yoğun sıralamaları ayırın. Biri doğru belgeyi bulursa diğerini bulmazsa, kelime birikimi eşleşmezliği (hatar eden yarısını ekle) veya semantik belirsizlik (hatar: daha iyi yerleştirmeler veya yeniden sıralama).


> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.


2026'da:
> 2026 yıl teknik:

| Scale | Stack |
|-------|-------|
| 1k-100k docs | In-memory BM25 + `all-MiniLM-L6-v2` embeddings + RRF. No separate DB. |
| 100k-10M docs | FAISS or pgvector for dense + Elasticsearch / OpenSearch for BM25. Run in parallel. |
| 10M+ docs | Qdrant / Weaviate / Vespa / Milvus with hybrid support. Cross-encoder rerank on top-30. |
| Best-quality frontier | Three-way (BM25 + dense + SPLADE) + ColBERT late-interaction reranking |
> Sıfır ve teknoloji.
|------|--------|
| 1k-100k 文档 | 内存中 BM25 + `all-MiniLM-L6-v2` 嵌入 + RRF。无需独立数据库。 |
| 100k-10M 文档 | FAISS 或 pgvector 做稠密 + Elasticsearch / OpenSearch 做 BM25。并行运行。 |
| 10M+ 文档 | Qdrant / Weaviate / Vespa / Milvus 配混合支持。交叉编码器重排序 top-30。 |
| 最高质量前沿 | 三路（BM25 + 稠密 + SPLADE）+ ColBERT 后期交互重排序 |

Seçtiğiniz her şey, değerlendirme için bütçe. Benchmark retrieval raporu, sonundan sonuna kadar RAG doğruluğunu karşılaştırmadan önce geri çağırın.
> Seçim ne olursa olsun, bütçe değerlendirmek için yapılması gerekir.

### 2026 üretiminden alınan zor dersler
> - **80% 的 RAG 失败追溯到摄取和分块，而不是模型。**团队花几周交换 LLM 和调优提示,检索每三次查询就安静地回归错误的上下文──先修复分块──
- **分块策略比分块大小更重要。**固定大小分割会破坏表格、代码和嵌套标题──句感知是默认选择;语义或基于LLM的分块在技术文档和产品手册上有回报──
- **父文档模式。**检索小的"子"块以获得精度──当同一节的多子块出现时,换进的块以保留下文──; bu cevapların kalitesini sürekli yükseltmek için yeniden eğitilmeye gerek yoktur──
- **k_rerank=3 通常最优。**Bu sayıdan fazla bir blok artırsa, belirtilerin gelişim ve üretim gecikmesi ve cevap kalitesini arttırmaz.
- **HyDE / 查询扩展。**Sorguların ortaya çıkması, içine yerleştirilmesi, kontrol edilmesi, kısa sorular ve uzun dosyalar arasındaki açıklama farkları, eğitim gerektirmez.
- **上下文预算控制在 8K token 以下。**Bu kısıtlama altında devamlı yaşam, yeniden düzenleme  değerini                                                                                                                                                                                                                                                       
- **版本化一切。**提示、分块规则、嵌入模型、重排序器──任何漂移都会静默破坏答案质量──忠诚度、上下文精确率和未回答问题率 上下文精确率和未回答问题率 上下文精确率和未回答率 上下文精确率和未回答问题率 上下文精确率和未回答率 上下文精确率 关闭控制 在用户看到之前阻止回归──
- **三路检索（BM25 + 稠密 + 学习稀疏如 SPLADE）在 2026 年基准上优于两路**Özellikle karışma ve dil anlamı sorguları.

- **80% of RAG failures trace to ingestion and chunking, not the model.**Takımlar haftalarca LLM'leri değiştirirken ve istekleri ayarlarken geri alınan her üçüncü sorguda sessizce yanlış bağlamı gönderir.
- **Chunking strategy matters more than chunk size.**Sıkı boyutlu bölünmeler tabloları, kodları ve yuva başlıklarını kırar. Ceza bilinçli öntanımlıdır; semantik veya LLM tabanlı parçalanma teknik belgeler ve ürün elyazmaları için ödüllendirilir.
- **Parent-doc pattern.**Aynı ana bölümünden birden fazla çocuk ortaya çıktığında, bağlamı korumak için ana blokunu değiştirin. Bu, yeniden eğitilmeden cevap kalitesini sürekli olarak yükseltir.
- **k_rerank=3 is usually optimal.**Eğer k=8 sizin için k=3'ten daha iyi ise, yeniden sıralama işlemi düşük performans gösteriyor.
- **HyDE / query expansion.**Sorgudan bir hipotetik cevap oluşturun, onu yerleştirin, alın. Kısa sorularla uzun belgeleri arasındaki ifade boşluğunu kapatın.
- **Context budget under 8K tokens.**Bu sınırda sürekli vurmak, yeniden sıralama eşiğinin çok gevşek olduğunu gösterir.
- **Version everything.**İndirimler, parçalanma kuralları, yerleştirme modeli, yeniden sıralama. Her türlü akış sessizce cevap kalitesini kırar. CI, sadakat, bağlam doğruluğu ve cevapsız soru oranı kullanıcıların görmeden önce geri dönüşleri engeller.
- **Three-way retrieval (BM25 + dense + learned-sparse like SPLADE) outperforms two-way**2026 referansları, özellikle de doğru isimleri semantikle karıştırmak için sorular için gönderin.
> 2026'da yapılan bir endüstri ölçümüne göre, doğru bir kontrol tasarımı, daha iyi bir kontrolden gelen, daha küçük bir modelden gelen performansın arttırılması ile ilgili olarak %70-90%'lık bir düşüş göstermektedir.

Doğru geri alım tasarımı, 2026 endüstri ölçümlerine göre halüsinasyonları %70-90 oranında azaltır. RAG performans kazanımlarının çoğu daha iyi geri alımdan gelir, model ince ayarlamalardan değil.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.


## İndirin . Ürünler .

- Kaydet .`outputs/skill-retrieval-picker.md`- ...
> 保存为 `outputs/skill-retrieval-picker.md`- ...

```markdown
---
name: retrieval-picker
description: Pick a retrieval stack for a given corpus and query pattern.
version: 1.0.0
phase: 5
lesson: 14
tags: [nlp, retrieval, rag, search]
---

Given requirements (corpus size, query pattern, latency budget, quality bar, infra constraints), output:

1. Stack. BM25 only, dense only, hybrid (BM25 + dense + RRF), hybrid + cross-encoder rerank, or three-way (BM25 + dense + learned-sparse).
2. Dense encoder. Name the specific model. Match to language(s), domain, and context length.
3. Reranker. Name the specific cross-encoder model if used. Flag that rerank adds 30-100ms latency on top-30.
4. Evaluation plan. Recall@10 is the primary retriever metric. MRR for multi-answer. Baseline first, incremental improvements measured against it.

Refuse to recommend dense-only for corpora with named entities, error codes, or product SKUs unless the user has evidence dense handles exact matches. Refuse to skip reranking for high-stakes retrieval (legal, medical) where the final top-5 decides the user's answer.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


## Egzersizler.

1. **Easy.**Uygulama`hybrid_search`500 belgelik bir korpus üzerinde. 20 sorgu test. BM25'li, yoğun ve hibrid arasında 5'e hatırlama karşılaştır.
2. **Medium.**MRR hesaplamasını ekleyin. Bilinen doğru belge ile yapılan her test sorusu için BM25, yoğun ve hibrit sıralamalarda doğru belgenin sıralamasını bulun. Her biri için MRR rapor edin.
3. **Hard.**MultipleNegativesRankingLoss (Sentence Transformers) kullanarak alanınızda yoğun bir kodlayıcıyı ince ayarlayın. 500 sorgu-doküman çiftinden bir eğitim kümesi oluşturun. Pre- ve post-fine-tune hatırlatma karşılaştırın.
> 1. **简单。**Yukarıdakiları 500 文档语料 üzerinde gerçekleştirmek için`hybrid_search`△测试 20 个查询──比较 BM25-only、density-only 和混合的回忆@5──
2. **中等。**添加 MRR 计算──Bütün bilinen doğru belgeli test sorguları için doğru belge BM25 密和混合排列中的位置中找到──報告各自的MRR──
3. **困难。**Kullanın MultipleNegativesRankingLoss (Sentence Transformers) Alanınızda 500 sorgu-dokümanından yapılandırma eğitim kümesi için.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BM25 | Keyword search | Okapi BM25. Scores documents by term frequency, IDF, and length. |
| Dense retrieval | Vector search | Encode query + doc into vectors, find nearest neighbors. |
| Bi-encoder | Embedding model | Encodes query and doc independently. Fast at query time. |
| Cross-encoder | Reranker model | Encodes query + doc together. Slow but accurate. |
| RRF | Rank fusion | Combine two rankings by summing `1/(k + rank)`. |
| Recall@k | Retrieval metric | Fraction of queries where a relevant doc is in the top-k. |
> # Sözcükler # İnsanlar her zaman söylerdi # Gerçek anlamı #
|------|-----------|---------|
| BM25 | 关键词搜索 | Okapi BM25。按词频、IDF 和长度为文档打分。 |
| 稠密检索 | 向量搜索 | 将查询 + 文档编码为向量，找最近邻。 |
| 双编码器 | 嵌入模型 | 独立编码查询和文档。查询时快速。 |
| 交叉编码器 | 重排序模型 | 一起编码查询 + 文档。慢但准确。 |
| RRF | 排名融合 | 通过对 `1/(k + rank)` 求和合并两个排名。 |
| Recall@k | 检索指标 | 相关文档在 top-k 中的查询比例。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.


## Daha fazla okumak

- [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) BM25 tedavisinin sonucunda.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906)DPR, kanonik iki kodlayıcı.
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720) sıvı ile boşluğu kapatan öğrenilmiş-sparse retriever.
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) RRF kağıdı.
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) Geç etkileşimden kurtarma.
> - [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)BM25 处理──
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, klasik iki kodlayıcı
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720)        密差的学习稀疏检查器
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) RRF 论文。
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) 后期交互检索──
