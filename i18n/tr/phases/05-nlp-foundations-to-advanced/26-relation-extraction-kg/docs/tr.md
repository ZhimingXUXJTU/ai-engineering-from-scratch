# İlişki Çekim ve Bilgi Grafi Yapılandırması İlişki Çekim ve Bilgi Grafi Yapılandırması

> NER varlıkları buldu. varlık bağlantısı onları demirledi. ilişki çıkarımı aralarındaki kenarları bulur. Bilgi grafi düğümlerin, kenarların ve kökenlerinin toplamıdır.
> NER 找到了实体――实体链定了它们――关系抽取找到它们之间的边――知识图谱是节点、边及其来源的总和――

> **【中文解读】**Yazılar içinden çekilen fiziksel ilişkiler, bilgi planı oluşturmak.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 25 (Entity Linking) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 25（实体链接）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Sorunlar. Sorunlar.

Relation Extraction (RE) serbest metni yapılandırılmış üçlüler haline getirir: (subject, relation, object). "Apple Steve Jobs tarafından kuruldu" → (Apple, found_by, Steve Jobs). Bilgi güç önerme sistemlerini, soru cevaplarını, ilaç keşifini ve uyumluluk izlemeyi grafikler.

> 关系抽取(RE)将自由文本转化为结构化三元组:(主语, 关系, 宾语) ・・・"Apple'ın kurucusu Steve Jobs'tu" → (Apple, kurucusu_Steve Jobs) ・・・知识图驱动推系统、问答、药物发现和合规监控。

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği nasıl gerçek tasarımda doğru şekilde anlayabilir ve uygulayabilirsiniz.

2026 sorunu: LLM'ler ilişkileri coşkuyla çıkarır, ancak kaynak metinde bulunmayan kenarları halüsinasyonlandırır.

> 2026 yılının sorusu:LLM 热情地抽取关系但会幻源文本中不存在的边缘――知识图谱构建生产中,精确率比召回率更重要――

## Konsepten bir şey.

> **【中文解读】**本節介绍核心概念和理论基础──

**Supervised RE.**Etiketlenmiş ilişki örneklerine bir sınıflandırıcı eğit. Giriş: cümle + varlık çift. Çıktı: ilişki türü. Etiketlenmiş verileri gerektirir.

> **有监督 RE。**Bu nedenle, bu tür bir programın bir parçası olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir diğer olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, ifade edilebilir.

**Distant supervision.**Eğer (A, born_in, B) KB'de mevcutsa, A ve B'yi bahsedilen herhangi bir cümle olumlu bir örnektir.

> **远程监督。**Eğer bilgi kütlesinde varsa (A, doğmuş, B), A ve B cümlelerinin herhangi bir zamanda bahsedilenleri geçerlidir.

**LLM-based RE.**Yüksek hatırlama, değişken hassasiyet, doğrulama gerektirir.

> **基于 LLM 的 RE。**提示 LLM 抽取关系──高召回率,精确率不稳定──需要验证──

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'ye kadar, NLP'de değişim biçimi yaşandı.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG)   检索增强生成 (RAG)  RAG)   检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成) 检索增强生成 (RAG) 检索增强生成 (RAG) 检测增强生成) 检测增强生成 (RAG) 检测增强生成) 检测增强的架构 (RAG) 检测) 检测增强的架构
```figure
relation-triples
```

## Yapın

> **【拓展：NLP 的多语言挑战】**Dünya çapında 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve birkaç dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla birlikte, çekirdek algoritmasını da tamamlıyor.

```python
def extract_relations(text, entities, llm):
    prompt = f"""Extract all relations between entities from this text.
Text: {text}
Entities: {entities}
Output as JSON list of {{"subject": "...", "relation": "...", "object": "..."}}."""
    return llm(prompt)
```

> **【中文解读】**Bu bölüm, bu teknolojiyi nasıl hızlı bir şekilde uygulayacağımızı gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi.

## Çerçeveyi kullanın.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl deploye edileceği üzerinde yoğunlaşmaktadır.

- **spaCy + RE models.**RE. / spaCy + RE 模型──生产 RE 流水线──
- **Hugging Face RE models.**İlişki sınıflandırması için ince ayarlanmış BERT. / Hugging Face RE 模型。
- **LLM + verification.**LLM ile çıkar, kaynağa karşı doğrulay. / LLM + 验证。
- **Neo4j.**Bilgi grafiklerini saklayın ve sorun. / Neo4j── depolama ve sorgulama bilgi planı──

## İndirin . Ürünler .

- Kaydet .`outputs/skill-re-kg-builder.md`- ...

> 保存为 `outputs/skill-re-kg-builder.md`- ...

```markdown
Given a corpus and entity types, build a knowledge graph.
1. RE approach (supervised, distant supervision, LLM).
2. Verification strategy (precision vs recall).
3. KG storage (Neo4j, RDF, property graph).
```

## Egzersizler.

1. **Easy.**Regex modellerini kullanarak 10 cümleden ilişkileri çıkarın. / **简单。**10 cümle içinde bir ilişki çekmek için kullanın.
2. **Medium.**BERT modeli, TACRED'de ilişki sınıflandırması için ince ayarlanmalıdır. / **中等。**Bu yüzden, bu bir şey değil.
3. **Hard.**Tam bir KG boru hattı inşa edin: NER → EL → RE → Neo4j. / **困难。**构建完整 KG 流水线──

## Anahtar Şartlar .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Relation extraction（关系抽取） | Extract (subject, relation, object) triples from text. / 从文本提取三元组。 |
| Knowledge graph（知识图谱） | Structured graph of entities and relations. / 实体和关系的结构化图。 |
| Distant supervision（远程监督） | Auto-label using existing KB. / 用现有知识库自动标注。 |

## Daha fazla okumak

- [TACRED](https://nlp.stanford.edu/pubs/tacred17.pdf) ilişki çıkarma verileri. / 关系抽取数据集──
- [Neo4j](https://neo4j.com/) Grafik veritabanı. / 图数据库。
