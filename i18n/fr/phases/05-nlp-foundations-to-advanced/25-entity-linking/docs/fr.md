# Entité Lien & Disambiguation

> NER a trouvé "Paris". L'entité reliant décide: Paris, France? Paris Hilton? Paris, Texas? Paris (le prince de Troie)?
> NER 找到了 "Paris"──实体链接决定:巴黎(France?Paris·Hilton?Paris(Texas?Paris(特洛伊王子?

> **【中文解读】**Le NER est lié à l'unique article de la base de connaissances.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 22 (Embedding Models) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 22（嵌入模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

L'entité de liaison (EL) résolve chaque mention à une entrée unique dans une base de connaissances (Wikidata, Wikipedia, GeoNames).

> 实体链接(EL) va chaque référence être résumée pour le savoir-faire de la base de données de Wikipédia, Wikipédia, les géonames)

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans le cadre de la construction réelle ?

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de la conception.

**Candidate generation.**En fonction de "Jordan", quelles entrées KB correspondent ? Utilisez la correspondance de chaînes, la résolution de redirection et les prérogatives de popularité.

> **候选生成。**给定 "Jordan", quels sont les éléments de base de connaissances qui correspondent ?

**Disambiguation.**Remplissez les candidats par similitude de contexte. Bi-encodeur pour la vitesse, cross-encodeur pour la précision. Context = texte environnant + description de l'entité de KB.

> **消歧。**按上下文相似度排名候选人──双编码器用于速度,交叉编码器用于准确率──上下文 = 周围文本 + 知识库中的实体描述──

> **【拓展：大语言模型的工程实践】**Le GPT à ChatGPT, le NLP, a connu une transformation de la mode.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est la structure la plus populaire de l'IA de l'entreprise actuelle 应用──

> **【拓展：NLP 的多语言挑战】**Dans le monde, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Le code est passé de zéro à zéro pour réaliser l'algorithme central.
```figure
gx-entity-linking
```

## Faites-le

### Étape 1: créer un index alias à partir des redirections de Wikipédia

```python
alias_to_entities = {
    "jordan": ["Q41421 (Michael Jordan)", "Q810 (Jordan, country)", "Q254110 (Michael B. Jordan)"],
    "paris":  ["Q90 (Paris, France)", "Q663094 (Paris, Texas)", "Q55411 (Paris Hilton)"],
    "apple":  ["Q312 (Apple Inc.)", "Q89 (apple, fruit)"],
}
```

Les données de l'alias de Wikipédia: ~ 18M (alias, entité) paires. Télécharger à partir de Wikidata dumps.

### Étape 2: désambiguation fondée sur le contexte

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

> **【中文解读】**Ce chapitre montre comment utiliser un cadre mature pour appliquer rapidement cette technologie.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL.

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**Le présent article se concentre sur la façon dont le modèle sera déployé pour les produits disponibles.

- **OpenTapioca.**EL léger pour Wikidata. / OpenTapioca。Wikidata 轻量 EL。
- **REL (Radboud Entity Linker).**Wikipédia de pointe EL. / REL。先进 Wikipédia EL。
- **GENRE.**Autoregresssive entité liant par Facebook. / GENRE。Facebook 自回归实体链接。
- **LLM prompting.**Demandez à la maîtrise de l'ordre de faire preuve d'ambiguïté.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-entity-linker.md`- Le numéro de la liste:

> 保存为 `outputs/skill-entity-linker.md`- Le numéro de la liste:

```markdown
Given mentions from NER, link them to a knowledge base.
1. KB choice (Wikidata, Wikipedia, custom).
2. Candidate generation strategy.
3. Disambiguation method (embedding similarity, cross-encoder, LLM).
```

## Les exercices

1. **Easy.**Construisez un générateur de candidats basé sur Wikipedia. / **简单。**Construction basée sur Wikipédia 
2. **Medium.**Implémenter la désambiguation par codeur et évaluer sur un ensemble de tests. / **中等。**实现双编码器消歧──
3. **Hard.**Comparer EL basé sur LLM contre EL neural sur un ensemble de données multilingue. / **困难。**Dans le plus grand nombre de langues, on peut comparer LLM EL vs 神经 EL.

## Les termes clés

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Entity linking（实体链接） | Map mentions to KB entries. / 将指称映射到知识库条目。 |
| Disambiguation（消歧） | Pick the correct entity among candidates. / 在候选中选择正确实体。 |
| Candidate generation（候选生成） | Retrieve possible KB matches for a mention. / 为指称检索可能的知识库匹配。 |

## Encore une lecture

- [Wu et al. (2020). Scalable Zero-shot Entity Linking](https://arxiv.org/abs/1910.02854)/ 可扩展零样本实体链接──
- [De Cao et al. (2020). GENRE](https://arxiv.org/abs/1912.01572)/ 自归实体链接──
