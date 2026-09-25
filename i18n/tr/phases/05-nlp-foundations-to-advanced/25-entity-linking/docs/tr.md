# Entite Bağlantı ve Açıklama

> NER "Paris"i buldu. "Paris, Fransa"yı bağlantı veren bir varlık Paris Hilton Paris, Texas Paris, Paris (Trojan prens) mı?
> NER 找到了 "Paris"──实体链接决定: 巴黎 (Fransa) 帕里斯·希尔顿 (Paris) 德克萨斯 (Troï王子) 帕里斯 (Troï王子) 没有链接,你的知识图谱保持模糊──

> **【中文解读】**NER'in 提取'i bilgi kütlesindeki tek maddeye bağlamak.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 22 (Embedding Models) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 22（嵌入模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Entity linking (EL) her bahsedilen bilgi tabanında (Wikidata, Wikipedia, GeoNames) benzersiz bir giriş halleder.

> 实体链接(EL) will ہر指称解析为知识库(Wikidata、Wikipedia、GeoNames) 中唯一条目──两步流水线:候选生成(找到可能的匹配) 和消歧(选择正确的)

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği nasıl gerçek tasarımda doğru şekilde anlayabilir ve uygulayabilirsiniz.

## Konsepten bir şey.

> **【中文解读】**本節介绍核心概念和理论基础──

**Candidate generation.**"Jordan" verildiğinde, hangi KB girişleri eşleşir? İpuç eşleşimi, yeniden yönlendirme çözünürlüğü ve popülerlik önlemlerini kullanın. Genellikle en iyi 10-50 adayı alın.

> **候选生成。**给定 "Jordan",哪些知识库条目匹配?使用字符串匹配、重定向解析和流行度先验──通常检索前 10-50个候选──

**Disambiguation.**Konekst benzerliği ile adayları sıralayın. Hız için iki kodlayıcı, doğruluk için çapraz kodlayıcı. Konekst = çevre metni + KB'den varlık açıklaması.

> **消歧。**按上下文相似度排名候选──双编码器用于速度,交叉编码器用于准确率──上下文 = 周围文本 + 知识库中的实体描述──

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'ye kadar, NLP'de değişim biçimi yaşandı.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG)   检索增强生成 (RAG)  RAG)   检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成) 检索增强生成 (RAG) 检索增强生成 (RAG) 检测增强生成) 检测增强生成 (RAG) 检测增强生成) 检测增强的架构 (RAG) 检测) 检测增强的架构

> **【拓展：NLP 的多语言挑战】**Dünya çapında 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve birkaç dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla birlikte, çekirdek algoritmasını da tamamlıyor.
```figure
gx-entity-linking
```

## Yapın

### Adım 1: Wikipedia yönlendirmelerinden bir isim indeks oluşturun

```python
alias_to_entities = {
    "jordan": ["Q41421 (Michael Jordan)", "Q810 (Jordan, country)", "Q254110 (Michael B. Jordan)"],
    "paris":  ["Q90 (Paris, France)", "Q663094 (Paris, Texas)", "Q55411 (Paris Hilton)"],
    "apple":  ["Q312 (Apple Inc.)", "Q89 (apple, fruit)"],
}
```

Wikipedia alias verileri: ~ 18M (alias, entite) çiftleri. Wikidata çöplüklerinden indir. Ters indeks olarak saklayın.

### Adım 2: bağlam tabanlı belirsizlik

```python
def entity_link(mention, context, kb_lookup, embed_model):
    candidates = kb_lookup.get(mention.lower(), [])
    if not candidates:
        return None
    ctx_emb = embed_model.encode([context])
    scores = []
    for cand in candidates:
        cand_emb = embed_model.encode([cand["description"]])
        scores.append((cand, float(np.dot(ctx_emb[0], cand_emb[0]))))
    return max(scores, key=lambda x: x[1])[0]
```

> **【中文解读】**Bu bölüm, bu teknolojiyi nasıl hızlı bir şekilde uygulayacağımızı gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi.

## Çerçeveyi kullanın.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl deploye edileceği üzerinde yoğunlaşmaktadır.

- **OpenTapioca.**Wikidata için hafif EL. / OpenTapioca。Wikidata 轻量 EL。
- **REL (Radboud Entity Linker).**En son Wikipedia EL. / REL。先进 Wikipedia EL。
- **GENRE.**Facebook tarafından bağlantı kurulan bir otoriteregresiv kuruluş. / GENRE。Facebook 自回归实体链接。
- **LLM prompting.**Yüksek Lisans Yüksek Lisansının belirginliğini dile.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-entity-linker.md`- ...

> 保存为 `outputs/skill-entity-linker.md`- ...

```markdown
Given mentions from NER, link them to a knowledge base.
1. KB choice (Wikidata, Wikipedia, custom).
2. Candidate generation strategy.
3. Disambiguation method (embedding similarity, cross-encoder, LLM).
```

## Egzersizler.

1. **Easy.**Wikipedia tabanlı bir aday jeneratörü oluşturun. / **简单。**构建基于维基百科的候选生成器──
2. **Medium.**İki kodlayıcı belirsizliği uygulayın ve test setinde değerlendirin. / **中等。**实现双编码器消歧──
3. **Hard.**Çok dilli bir veri kümesi üzerinde LLM tabanlı EL ile sinirsel EL karşılaştırın. / **困难。**Çok Dilli Verilerde LLM EL vs 神经 EL

## Anahtar Şartlar .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Entity linking（实体链接） | Map mentions to KB entries. / 将指称映射到知识库条目。 |
| Disambiguation（消歧） | Pick the correct entity among candidates. / 在候选中选择正确实体。 |
| Candidate generation（候选生成） | Retrieve possible KB matches for a mention. / 为指称检索可能的知识库匹配。 |

## Daha fazla okumak

- [Wu et al. (2020). Scalable Zero-shot Entity Linking](https://arxiv.org/abs/1910.02854)/ 可扩展零样本实体链接──
- [De Cao et al. (2020). GENRE](https://arxiv.org/abs/1912.01572)/ 自归实体链接──
