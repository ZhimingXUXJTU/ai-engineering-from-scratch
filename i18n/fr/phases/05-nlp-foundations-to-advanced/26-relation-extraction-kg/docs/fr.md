# Relations extraction et graphique de connaissances Construction de relations extraction et graphique de connaissances Construction

> L'extraction de relation trouve les bords entre eux. Un graphique de connaissance est la somme des nœuds, des bords et de leur provenance.
> NER 找到了实体──实体链接定了它们──关系抽取找到它们之间的边缘──知识图谱是节点、边及其来源的总和──

> **【中文解读】**De la littérature extraire des relations physiques, construire des plans de connaissances.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 25 (Entity Linking) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 25（实体链接）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Le problème , l' introduction du problème

Relation Extraction (RE) transforme le texte libre en trois éléments structurés: (sujet, relation, objet). "Apple a été fondée par Steve Jobs" → (Apple, fondé_par Steve Jobs).

> 关系抽取(RE)将自由文本转化为结构化三元组:(主语, 关系, 宾语) ・・・"Apple a été fondée par Steve Jobs" → (Apple, fondée par Steve Jobs) ・・・知识图驱动推系统、问答、药物发现和合规监控。

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans le cadre de la construction réelle ?

Le problème de 2026: les LLM extraient les relations avec enthousiasme mais hallucinent des bords qui n'existent pas dans le texte source.

> Question 2026: LLM 热情地抽取关系但会幻源文本中不存在的边缘―― dans la construction de la production de graphiques de connaissances, le taux d'exactitude est plus important que le taux de recul――

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de la conception.

**Supervised RE.**Exercer un classifiateur sur des exemples de relations étiquetées. Entrée: phrase + paire d'entités. Sortie: type de relation. Require des données étiquetées.

> **有监督 RE。**Dans le cadre de la formation de la formation, le personnel de la formation doit être informé de la formation.

**Distant supervision.**L'alignement du texte avec les triples KB existants. Si (A, born_in, B) existe dans le KB, toute phrase mentionnant A et B est un exemple positif. Bruyant mais évolutif.

> **远程监督。**Si le texte est présent dans la base de connaissances existantes (A, Born_in, B), les phrases A et B sont normales tout en faisant référence à la base de connaissances existantes.

**LLM-based RE.**Faire en sorte que le Master extrait les relations, rappel élevé, précision variable, besoin de vérification.

> **基于 LLM 的 RE。**Le taux d'études supérieures est élevé, le taux d'études supérieures est élevé, le taux d'études supérieures est élevé, le taux d'études supérieures est élevé, le taux d'études supérieures est élevé, le taux d'études supérieures est élevé, le taux d'études supérieures est élevé, le taux d'études supérieures est élevé, le taux d'études supérieures est élevé, le taux d'études supérieures est élevé, le taux d'études supérieures est élevé.

> **【拓展：大语言模型的工程实践】**Le GPT à ChatGPT, le NLP, a connu une transformation de la mode.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est la structure la plus populaire de l'IA de l'entreprise actuelle 应用──
```figure
relation-triples
```

## Faites-le

> **【拓展：NLP 的多语言挑战】**Dans le monde, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Le code est passé de zéro à zéro pour réaliser l'algorithme central.

```python
def extract_relations(text, entities, llm):
    prompt = f"""Extract all relations between entities from this text.
Text: {text}
Entities: {entities}
Output as JSON list of {{"subject": "...", "relation": "...", "object": "..."}}."""
    return llm(prompt)
```

> **【中文解读】**Ce chapitre montre comment utiliser un cadre mature pour appliquer rapidement cette technologie.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL.

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**Le présent article se concentre sur la façon dont le modèle sera déployé pour les produits disponibles.

- **spaCy + RE models.**L'équipement de production pour RE. / spaCy + RE 模型──生产 RE 流水线──
- **Hugging Face RE models.**BERT bien ajusté pour la classification des relations. / Embrace face RE 模型。
- **LLM + verification.**Extrait avec LLM, vérifier contre la source. / LLM + 验证。
- **Neo4j.**Réservation et requête des graphiques de connaissances. / Neo4j── stockage et enquête

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-re-kg-builder.md`- Le numéro de la liste:

> 保存为 `outputs/skill-re-kg-builder.md`- Le numéro de la liste:

```markdown
Given a corpus and entity types, build a knowledge graph.
1. RE approach (supervised, distant supervision, LLM).
2. Verification strategy (precision vs recall).
3. KG storage (Neo4j, RDF, property graph).
```

## Les exercices

1. **Easy.**Extraire des relations à partir de 10 phrases en utilisant des modèles de régex. / **简单。**Utilisez le modèle de 10 phrases pour extraire la relation.
2. **Medium.**- modifier le modèle BERT pour la classification des relations sur TACRED. / **中等。**Dans le cadre de la mise en œuvre de la politique de l'emploi, les entreprises doivent être soumises à des mesures de protection des travailleurs.
3. **Hard.**Construire un pipeline KG complet: NER → EL → RE → Neo4j. / **困难。**Construire une ligne de transport en commun.

## Les termes clés

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Relation extraction（关系抽取） | Extract (subject, relation, object) triples from text. / 从文本提取三元组。 |
| Knowledge graph（知识图谱） | Structured graph of entities and relations. / 实体和关系的结构化图。 |
| Distant supervision（远程监督） | Auto-label using existing KB. / 用现有知识库自动标注。 |

## Encore une lecture

- [TACRED](https://nlp.stanford.edu/pubs/tacred17.pdf) relation extraction de l'ensemble de données. / 关系抽取数据集──
- [Neo4j](https://neo4j.com/) base de données graphique. / 图数据库。
