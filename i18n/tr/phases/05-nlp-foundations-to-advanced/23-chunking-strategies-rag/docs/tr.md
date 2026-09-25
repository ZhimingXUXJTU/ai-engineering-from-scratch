# RAG için parça parça stratejileri

> Çükleme yapılandırması, çekim kalitesini embed model seçimi kadar etkiliyor (Vectara NAACL 2025).
> Bölüm konutlama, inceleme kalitesi üzerindeki etkisi, yerleşim modelinin seçimi ile aynı büyüktür.

> **【中文解读】**RAG 系统中,文档如何切分成块直接影响检索效果──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 22 (Embedding Models), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 22（嵌入模型），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Sorunlar. Sorunlar.

Vectara'nın NAACL 2025 makalesinde, çekim stratejisi çekim kalitesi seçimleri kadar çekim kalitesi konusunda da çok fazla farklılık açıkladığını gösterdi.

> 修复方法不是"买个更好的嵌入模型"──修复方法是正确分块── Vectara'nın NAACL 2025 makalesinde,分块策略, yerleşim seçeneği kadar çok arama kalitesi farkını açıkladığını göstermiştir.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği nasıl gerçek projede doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

2026 Şubat referansları şaşırtıcı sonuçlar göstermektedir: 100 token parçacıkları ve 20 token üst üstelikleri ile saf sabit boyutlu parçacıklama genel amaçlı RAG'deki en "akıllı" parçacıklama stratejilerini yener. Semantik parçacıklama anlatım metni üzerinde yardımcı olur. Cevab seviyesindeki parçacıklama FAQ tarzında içeriğe yardımcı olur. Evrensel bir kazanan yoktur.

> 2026 yılının 2 ayındaki基准 testinde şaşırtıcı sonuçlar ortaya çıktı: basit sabit büyük küçük parçalar ((100 token + 20 token ağırlıklı) genel RAG'de çoğu "akıllı" parça stratejisini yendi.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde, temel kavram ve teorinin temelini ele alır. Bu kavramları öğrenmek, sonradan gerçekleştirilen bir önlemdir.

**Fixed-size chunking.**Metni seçeneği üzerine örtüşen N-token bloklarına bölün. Basit, hızlı, şaşırtıcı derecede etkili.

> **固定大小分块。**Metni N simgesinin bloklarına ayırmak, seçilebilir yüklenmek.

**Sentence-level chunking.**Her parça bir veya daha fazla cümle. Soru sorusu ve kısa cevap almak için iyi.

> **句子级分块。**Bu cümleyi kısaltmak için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için, kısayolları bölmek için.

**Semantic chunking.**cümleler yerleştir, benzer yerleştirmelerle ardıcıl cümleleri parçalara gruplandır.

> **语义分块。**嵌入句, 嵌入式连续句分组为块── better,计算更慢──

**Recursive character chunking.**paragraflara, cümlelere, karakterlere ayırmak LangChain'in standartı.

> **递归字符分块。**按段落分割,然后按句,然后按字符──LangChain 的默认──好通用启发式──

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'ye kadar, NLP alanında "her görev bir model eğitimi"nden "her görevyi çözmek için bir model" biçimindeki bir değişim yaşandı.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG)   检索增强生成 (RAG)  RAG)   检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成) 检索增强生成 (RAG) 检索增强生成 (RAG) 检测增强生成) 检测增强生成 (RAG) 检测增强生成) 检测增强的架构 (RAG) 检测) 检测增强的架构

> **【拓展：NLP 的多语言挑战】**Dünya çapında 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve birkaç dil üzerinde yoğunlaşmaktadır.
```figure
n5-chunk-cuts
```

## Yapın

## Yapın.

> **【中文解读】**Bu bölüm kodla birlikte, çekirdek algoritmasını da tamamlıyor.

### Adım 1: Düz ölçülü parçalanma, üst üste geçiş

```python
def fixed_chunk(text, chunk_size=100, overlap=20):
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunks.append(" ".join(tokens[i:i + chunk_size]))
    return chunks
```

### Adım 2: semantik parçalanma

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def semantic_chunk(text, model_name="sentence-transformers/all-MiniLM-L6-v2", threshold=0.5):
    model = SentenceTransformer(model_name)
    sentences = text.split(". ")
    embeddings = model.encode(sentences, normalize_embeddings=True)
    chunks = [sentences[0]]
    for i in range(1, len(sentences)):
        sim = np.dot(embeddings[i], embeddings[i-1])
        if sim < threshold:
            chunks.append(sentences[i])
        else:
            chunks[-1] += ". " + sentences[i]
    return chunks
```

> **【中文解读】**Bu bölüm, bu teknolojiyi nasıl hızlı bir şekilde uygulayacağımızı gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi.

## Çerçeveyi kullanın.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl deploye edileceği üzerinde yoğunlaşmaktadır.

| Strategy / 策略 | Chunk size / 块大小 | Best for / 最适合 |
|---------|---------|---------|
| Fixed / 固定 | 100-500 tokens | General purpose / 通用 |
| Sentence / 句子 | 1-3 sentences | FAQ, short answers / FAQ、短答案 |
| Semantic / 语义 | Variable / 可变 | Narrative, long docs / 叙述、长文档 |
| Recursive / 递归 | 500-1500 chars | LangChain default / LangChain 默认 |

## İndirin . Ürünler .

- Kaydet .`outputs/skill-chunking-picker.md`- ...

> 保存为 `outputs/skill-chunking-picker.md`- ...

```markdown
Given document type and retrieval task, pick chunking strategy and parameters.
1. Chunking method (fixed, sentence, semantic, recursive).
2. Chunk size and overlap.
3. Evaluation metric (retrieval recall@k, answer quality).
```

## Egzersizler.

1. **Easy.**Düz ölçülü parçalanma, üst üste geçişle uygulanır.**简单。**实现固定大小分块──测量检索质量──
2. **Medium.**Bir anlatım verisi üzerinde sabit vs. semantik parçalanma karşılaştırın. / **中等。**Söyleyen veri kümesi üzerinde sabit vs.
3. **Hard.**Belge tipi başına parça boyutunu adapte eden en uygun parça boru hattı oluşturun. / **困难。**建据文档类型自适应块大小的优分块流水线──

## Anahtar Şartlar .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Chunking（分块） | Splitting documents into retrievable units. / 将文档分割为可检索单元。 |
| Overlap（重叠） | Shared tokens between adjacent chunks. / 相邻块之间的共享 token。 |
| Semantic chunking（语义分块） | Group sentences by embedding similarity. / 按嵌入相似度分组句子。 |

## Daha fazla okumak

- [Vectara NAACL 2025 chunking study](https://vectara.com/blog/breaking-the-ice-chunking-strategies-for-rag) parçalanma referansı. / 分块基准。
- [LangChain text splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/) parça parça uygulamaları. / 分块实现。
