# Modeller yerleştirmek 2026 Deep Dive

> Word2Vec size kelimenin bir vektörü verdi. Modern yerleştirme modelleri size geçit başına bir vektör verir, diller arası, nadir, yoğun ve çok vektörlü görüntüler ile, indeksiye uygun boyutlarda. Yanlış seçin ve RAG yanlış şeyi alır.
> Word2Vec  size her kelimeyi bir yönlendirme sağlar. Modern yerleşim modeli size her bölümde bir yönlendirme sağlar.

> **【中文解读】**嵌入模型 RAG 和语义 arama çekirdeğidir.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word Embeddings), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 03（词嵌入），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Sorunlar. Sorunlar.

2026'da bir gömme seçmek beş eksel arasında seçim yapmak demektir: yoğun vs. nadir vs. çok vektör, tek dil vs. çok dil, model boyutu, eğitim amacı ve vektör veritabanınızın boyut kısıtlamalarına uygun olup olmadığını.

> 2026 yılını seçmek, beş aksan üzerinde seçmek anlamına gelir: 密 vs 稀疏 vs 多向量、单语 vs 多语言、模型大小、训练目标、以及是否适合您的量数据库尺寸约束──

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği nasıl gerçek projede doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde, temel kavram ve teorinin temelini ele alır. Bu kavramları öğrenmek, sonradan gerçekleştirilen bir önlemdir.

**Dense embeddings.**Tek sabit boyutlu vektör tek metin (örneğin MiniLM'den 768-dim).

> **稠密嵌入。**Her metin sabit büyüklükteki bir vektördür.

**Sparse embeddings.**Sözlük terimi başına bir ağırlık (bilimli TF-IDF gibi). SPLADE, BM25. Anahtar kelime ağır sorular için iyi.

> **稀疏嵌入。**Her kelime bir ağırlıkta bulunur.

**Multi-vector / ColBERT.**Token başına bir vektör, geç etkileşim puanlaması.

> **多向量 / ColBERT。**Her bir simge, bir yön, bir geçiş, bir değerlendirme.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'ye kadar, NLP alanında "her görev bir model eğitimi"nden "her görevyi çözmek için bir model" biçimindeki bir değişim yaşandı.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG)   检索增强生成 (RAG)  RAG)   检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成) 检索增强生成 (RAG) 检索增强生成 (RAG) 检测增强生成) 检测增强生成 (RAG) 检测增强生成) 检测增强的架构 (RAG) 检测) 检测增强的架构

> **【拓展：NLP 的多语言挑战】**Dünya çapında 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve birkaç dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla birlikte, çekirdek algoritmasını da tamamlıyor.
```figure
gx-matryoshka
```

## Yapın

### Adım 1: yerleştirme modelleri karşılaştırmak

```python
from sentence_transformers import SentenceTransformer
import numpy as np

models = {
    "MiniLM": "sentence-transformers/all-MiniLM-L6-v2",
    "multilingual": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
}

query = "What is attention in transformers?"
docs = ["Self-attention computes weighted sums of values.", "The cat sat on the mat."]

for name, model_id in models.items():
    model = SentenceTransformer(model_id)
    q_emb = model.encode([query], normalize_embeddings=True)
    d_embs = model.encode(docs, normalize_embeddings=True)
    sims = (d_embs @ q_emb.T).flatten()
    print(f"{name}: {list(zip(docs, sims.round(3)))}")
```

> **【中文解读】**Bu bölüm, bu teknolojiyi nasıl hızlı bir şekilde uygulayacağımızı gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi.

## Çerçeveyi kullanın.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl deploye edileceği üzerinde yoğunlaşmaktadır.

| Model / 模型 | Dim / 维度 | Best for / 最适合 |
|------|------|---------|
| all-MiniLM-L6-v2 | 384 | English, speed / 英语，速度 |
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | Multilingual / 多语言 |
| BGE-large-en-v1.5 | 1024 | English accuracy / 英语准确率 |

## İndirin . Ürünler .

- Kaydet .`outputs/skill-embedding-picker.md`- ...

> 保存为 `outputs/skill-embedding-picker.md`- ...

```markdown
Given requirements (language, accuracy, latency, index size), pick the right embedding model.
1. Dense vs sparse vs multi-vector.
2. Model checkpoint.
3. Dimension and index budget.
```

## Egzersizler.

1. **Easy.**MiniLM ile BGE'yi 100 sorguyu geri alan görevle karşılaştırın. / **简单。**100 查询检索任务上比较 MiniLM vs BGE
2. **Medium.**Hibride yoğun+sparse çekim yapın. / **中等。**构建混合密+稀疏检索──
3. **Hard.**Domen-specifik çiftler üzerinde bir gömleyici modeli ince ayarlayın. / **困难。**Üstteki küçük modeller için belirli alanlarda yerleştirilmiştir.

## Anahtar Şartlar .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dense embedding（稠密嵌入） | Fixed-size vector per text. / 固定大小向量。 |
| Sparse embedding（稀疏嵌入） | One weight per vocab term. / 每个词表项一个权重。 |
| ColBERT / multi-vector | One vector per token, late interaction. / 每个 token 一个向量。 |
| Hybrid search（混合搜索） | Combine dense + sparse retrieval scores. / 结合稠密+稀疏检索。 |

## Daha fazla okumak

- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) yerleştirme referansları. / 嵌入模型基准──
- [SPLADE](https://arxiv.org/abs/2109.10086) nadir öğrenilen yerleşimler. / 稀疏学习嵌入。
- [ColBERT](https://arxiv.org/abs/2004.12832) geç etkileşim geri alımı. / 延迟交互检索。
