# Les stratégies de déchiquetage pour RAG

> La configuration de l'emballage influence la qualité de la récupération autant que le choix du modèle d'emballage (Vectara NAACL 2025).
> Le déploiement de blocs de recherche a un impact aussi important que celui du choix du modèle de placement.

> **【中文解读】**Dans le système RAG, le décomposition des documents en blocs affecte directement les résultats du dépistage.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 22 (Embedding Models), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 22（嵌入模型），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Le problème , l' introduction du problème

La solution n'est pas "acheter un meilleur modèle d'intégration". La solution est de décomposer correctement. Le document NAACL 2025 de Vectara a montré que la stratégie de décomposition explique autant de variance dans la qualité de récupération que le choix d'intégration.

> La méthode de réparation n'est pas " acheter un meilleur modèle de placement "― la méthode de réparation est correctement divisée en blocs. Le thème de la NAACL 2025 de Vectara indique que la stratégie de placement explique les différences de qualité de la recherche autant que la sélection de placement.

> **【中文解读】**Le problème posé dans ce chapitre est: comment comprendre et appliquer correctement cette technique dans le projet réel.

Les benchmarks de février 2026 montrent des résultats surprenants: le déchiquetage naïf de taille fixe avec des déchichets de 100 jetons et une superposition de 20 jetons bat la plupart des stratégies de déchiquetage "intelligentes" sur RAG à usage général. Le déchiquetage sémantique aide au texte narratif. Le déchiquetage au niveau de la phrase aide au contenu de style FAQ. Il n'y a pas de gagnant universel.

> Le test de base de 2 mois de 2026 a montré des résultats étonnants: simple fixe en gros blocs ((100 jetons plus 20 jetons) surchargés) a battu la plupart des stratégies de blocs intelligents de RAG.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases de la théorie.

**Fixed-size chunking.**Divisez le texte en blocs de jetons N avec chevauchement optionnel. Simple, rapide, étonnamment efficace.

> **固定大小分块。**Le texte est divisé en N blocs de jetons, qui peuvent être choisis.

**Sentence-level chunking.**Partagez-les en limites de phrases. chaque morceau = une ou plusieurs phrases.

> **句子级分块。**Dans chaque phrase, chaque bloc = une ou plusieurs phrases.

**Semantic chunking.**Embed des phrases, regrouper des phrases consécutives avec des embedding similaires en morceaux.

> **语义分块。**嵌入句子, seront emplacés en blocs de séquences similaires.

**Recursive character chunking.**Partagé par paragraphe, par phrase, par caractère, par défaut, LangChain.

> **递归字符分块。**按段落分割, puis按句, puis按字符── LongChain 的默认──

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu une transition de la " formation de chaque tâche à un modèle " à " un modèle pour résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est la structure la plus populaire de l'IA de l'entreprise actuelle 应用──

> **【拓展：NLP 的多语言挑战】**Dans le monde, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.
```figure
n5-chunk-cuts
```

## Faites-le

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Le code est passé de zéro à zéro pour réaliser l'algorithme central.

### Étape 1: déchiquetage en taille fixe avec chevauchement

```python
def fixed_chunk(text, chunk_size=100, overlap=20):
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunks.append(" ".join(tokens[i:i + chunk_size]))
    return chunks
```

### Étape 2: décomposition sémantique

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

> **【中文解读】**Ce chapitre montre comment utiliser un cadre mature pour appliquer rapidement cette technologie.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL.

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**Le présent article se concentre sur la façon dont le modèle sera déployé pour les produits disponibles.

| Strategy / 策略 | Chunk size / 块大小 | Best for / 最适合 |
|---------|---------|---------|
| Fixed / 固定 | 100-500 tokens | General purpose / 通用 |
| Sentence / 句子 | 1-3 sentences | FAQ, short answers / FAQ、短答案 |
| Semantic / 语义 | Variable / 可变 | Narrative, long docs / 叙述、长文档 |
| Recursive / 递归 | 500-1500 chars | LangChain default / LangChain 默认 |

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-chunking-picker.md`- Le numéro de la liste:

> 保存为 `outputs/skill-chunking-picker.md`- Le numéro de la liste:

```markdown
Given document type and retrieval task, pick chunking strategy and parameters.
1. Chunking method (fixed, sentence, semantic, recursive).
2. Chunk size and overlap.
3. Evaluation metric (retrieval recall@k, answer quality).
```

## Les exercices

1. **Easy.**Mettre en œuvre une déchiquetation de taille fixe avec chevauchement. Mesurer la qualité de la récupération. / **简单。**实现固定大小分块──测量检索质量──
2. **Medium.**Comparer les fractions fixes et sémantiques sur un ensemble de données narrative. / **中等。**Dans le recueil de données de la description, comparer les blocs fixes et les blocs de données.
3. **Hard.**Construire un pipeline de déchiquetage optimal qui adapte la taille de la pièce par type de document. / **困难。**Construction par type de documentation de type de bloc de taille de l'élément le plus élevé de la ligne de flux de l'eau.

## Les termes clés

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Chunking（分块） | Splitting documents into retrievable units. / 将文档分割为可检索单元。 |
| Overlap（重叠） | Shared tokens between adjacent chunks. / 相邻块之间的共享 token。 |
| Semantic chunking（语义分块） | Group sentences by embedding similarity. / 按嵌入相似度分组句子。 |

## Encore une lecture

- [Vectara NAACL 2025 chunking study](https://vectara.com/blog/breaking-the-ice-chunking-strategies-for-rag) référence de décomposition. / 分块基准。
- [LangChain text splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/) décomposer les mises en œuvre. / 分块实现。
