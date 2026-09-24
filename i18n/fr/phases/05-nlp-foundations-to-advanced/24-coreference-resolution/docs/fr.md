# Référence de résolution.

> "Elle l'a appelé, il n'a pas répondu, le médecin était au déjeuner". Trois références à deux personnes et personne n'est nommé.
> "Elle l'a appelé, il n'a pas répondu, le médecin était au déjeuner".

> **【中文解读】**Les mots et les noms des textes sont liés à leur objet de référence.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

La résolution de la Coreference relie chaque expression qui fait référence à la même entité. "Barack Obama", "le président", "il", "Obama" pointent tous vers une personne. Sans elle, votre système NER rapporte quatre entités au lieu d'une, vos fragments de graphes de connaissances, et votre résumé laisse tomber les sujets au milieu du document.

> "Barack Obama""",le président"",il""",Obama" sont tous dirigés vers un seul homme. Sans elle, votre système NER rapporte quatre entités au lieu d'une seule, savoir-faire brisé, résumé dans le milieu du dossier abandonné principal.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans le cadre de la construction réelle ?

Pourquoi cela importe en 2026: les LLM gèrent la coréférence implicitement dans leur fenêtre contextuelle, mais la récupération RAG a toujours besoin d'une résolution explicite. Si un utilisateur demande "qu'a-t-elle dit?", le récupérateur doit savoir qui "elle" est avant de pouvoir trouver la bonne pièce.

> Pourquoi est-ce important:LLM dans le top down文窗口内隐式处理共指, mais RAG 检索仍然需要显然消解――如果用户问"what did she say?",检索器在找到正确的块之前需要知道"she"是谁――

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de la conception.

**Mention detection.**Trouvez toutes les phrases et pronoms substantifs qui pourraient se référer à une entité.

> **指称检测。**找到所有可能指向实体名词短语和代词──使用 POS 标签和分析树──

**Coreference clustering.**Les groupes mentionnent des entités qui se réfèrent à la même entité.

> **共指聚类。**Il s'agit d'un système de décomposition de la même chose.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu une transition de la " formation de chaque tâche à un modèle " à " un modèle pour résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est la structure la plus populaire de l'IA de l'entreprise actuelle 应用──

> **【拓展：NLP 的多语言挑战】**Dans le monde, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.
```figure
coref-links
```

## Faites-le

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Le code est passé de zéro à zéro pour réaliser l'algorithme central.

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

> **【中文解读】**Ce chapitre montre comment utiliser un cadre mature pour appliquer rapidement cette technologie.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL.

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**Le présent article se concentre sur la façon dont le modèle sera déployé pour les produits disponibles.

- **spaCy with coreferee.**Coreference de production pour l'anglais. / spaCy + coreferee。英语生产共指。
- **Hugging Face span-based models.**Référence de la coréférence neuronale. / Face embrassée 基于跨度的模型──
- **LLM prompting.**Demandez au Master de résoudre les problèmes de base.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-coref-picker.md`- Le numéro de la liste:

> 保存为 `outputs/skill-coref-picker.md`- Le numéro de la liste:

```markdown
Given a text and need for entity tracking, pick coreference approach.
1. Rule-based vs neural vs LLM.
2. Language support.
3. Latency budget.
```

## Les exercices

1. **Easy.**Implémenter la résolution du pronom à l'aide de balises POS. / **简单。**Utilisez le POS 标签实现代词消解。
2. **Medium.**Évaluer le sujet sur un corpus de 50 phrases.**中等。**Dans les 50 phrases suivantes, on peut évaluer le nombre de participants.
3. **Hard.**Construire un préprocesseur RAG qui résolve les coreférences avant de le déchiqueter.**困难。**Construction de traitement RAG 预处理器 de la section précédente

## Les termes clés

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Coreference（共指） | Multiple expressions referring to the same entity. / 多个表达指向同一实体。 |
| Mention（指称） | A textual reference to an entity. / 对实体的文本引用。 |
| Anaphora（回指） | Pronoun referring to an earlier noun. / 代词指向前面的名词。 |

## Encore une lecture

- [Lee et al. (2017). End-to-end Neural Coreference Resolution](https://arxiv.org/abs/1707.07045) l'approche basée sur la durée. / 基于跨度的方法──
- [coreferee](https://github.com/explosion/coreferee) spCy plugin de référence. / spCy 共指插件──
