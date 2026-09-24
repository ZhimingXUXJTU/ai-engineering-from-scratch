# Nommé Identification d' Entité

> Ça semble facile jusqu'à ce que vous ayez affaire à des limites ambiguës, à des entités nichées et au jargon de domaine.
> Prenez le nom et le prenez.

> **【中文解读】**Le nom de l'individu, le nom de l'organisation, etc. sont la base de l'extraction des informations et du schéma de connaissance.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word Embeddings) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 5 · 03（词嵌入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

"Apple a poursuivi Google pour son accord de recherche sur iPhone aux États-Unis". Cinq entités: Apple (ORG), Google (ORG), iPhone (PRODUCT), accord de recherche (peut-être), US (GPE). Un bon système NER les extrait tous avec des types corrects. Un mauvais manque iPhone, confond Apple le fruit avec Apple la société, et étiquette "US" comme PERSON.

> "Apple a poursuivi Google pour son accord de recherche sur l'iPhone aux États-Unis". 五个实体:Apple(ORG)、Google(ORG)、iPhone(PRODUCT)、search deal(可能)、US(GPE)。

NER est le cheval de travail sous chaque pipeline d'extraction structurée. L'analyse de résumé, la numérisation du journal de conformité, l'anonymisation des dossiers médicaux, la compréhension des requêtes de recherche, la mise à terre des réponses des chatbots, l'extraction de contrats juridiques. Vous ne le voyez jamais complètement; vous en dépendez toujours.

> NER est le moteur de travail de chaque structure pour extraire des flux d'eau. Vous ne le voyez pas, mais vous êtes toujours dépendant de lui.

Cette leçon passe le chemin classique (basé sur les règles, HMM, CRF) vers le chemin moderne (BiLSTM-CRF, puis transformateurs). Chaque étape résout une limitation spécifique de celle qui l'a précédée.

> Ce cours est passé de la route classique à la route moderne, à la route basée sur des règles, à la HMM, à la CRF, à la BiLSTM, à la CRF, puis à la Transformer. Chaque étape a résolu les limites spécifiques de l'étape précédente.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

**BIO tagging**(ou BILOU) transforme l'extraction d'entités en un problème d'étiquetage de séquences.`B-TYPE`(début de l'entité), `I-TYPE`(entité interne), ou `O`(à l'extérieur de toute entité).

> **BIO 标注**(ou BILOU) sera l'objet de l'extraction et de la transformation en séquence de marquage de question.`B-TYPE`(实体开始)`I-TYPE`(en interne) ou `O`(ne figure pas dans le corps)

```
Apple    B-ORG
sued     O
Google   B-ORG
over     O
its      O
iPhone   B-PRODUCT
search   O
deal     O
in       O
the      O
US       B-GPE
.        O
```

Chaîne d'entités multi-tokens: `New B-GPE`- Je suis là .`York I-GPE`- Je suis là .`City I-GPE`Un modèle qui comprend la bio peut extraire des spans arbitraires.

> Les symboles sont:`New B-GPE`- Je suis là.`York I-GPE`- Je suis là.`City I-GPE` Comprendre le modèle de la bio peut être utilisé à n'importe quel niveau.

La progression de l'architecture:

> 架构演进:

- **Rule-based.**Regex + recherche de gazeteur. haute précision sur les entités connues, zéro couverture sur les nouvelles.
  **基于规则。**正则 + 地名词典查找──对已知实体精确率高,对新实体零覆盖──
- **HMM.**Le modèle de Markov caché, la probabilité d'émission d'un jeton donné, la probabilité de transition de la jeton à la jeton, le décode Viterbi, l'entraînement sur les données étiquetées.
  **HMM。**隐马尔可夫模型──给定标签的代币 发射概率,标签间转移概率──Viterbi 解码──在标签数据上训练──
- **CRF.**C'est un champ aléatoire conditionnel. Comme HMM mais discriminatif, vous pouvez donc mélanger des caractéristiques arbitraires (forme de mot, capitalisation, mots voisins).
  **CRF。**条件随机场──类似 HMM,但判别式,所以可以混合任意特征词形、大小写、相邻词)──depuis 2026 encore est la principale force de production classique du RRD.
- **BiLSTM-CRF.**Les caractéristiques neuronales au lieu de manuelles. LSTM lit la phrase dans les deux sens, la couche CRF en haut impose des séquences de balises cohérentes.
  **BiLSTM-CRF。**Le système de données de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette de l'étiquette.
- **Transformer-based.**Un BERT à réglage fin avec une tête de classification de jetons, une précision optimale, un calcul optimal.
  **基于 Transformer。**Utilisation du symbole 分类头微调 BERT──最佳 précision──最多计算量──

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
ner-bio-tagging
```

## Faites-le

### Étape 1: les aides à l'étiquetage biologique

```python
def spans_to_bio(tokens, spans):
    labels = ["O"] * len(tokens)
    for start, end, label in spans:
        labels[start] = f"B-{label}"
        for i in range(start + 1, end):
            labels[i] = f"I-{label}"
    return labels


def bio_to_spans(tokens, labels):
    spans = []
    current = None
    for i, label in enumerate(labels):
        if label.startswith("B-"):
            if current:
                spans.append(current)
            current = (i, i + 1, label[2:])
        elif label.startswith("I-") and current and current[2] == label[2:]:
            current = (current[0], i + 1, current[2])
        else:
            if current:
                spans.append(current)
                current = None
    if current:
        spans.append(current)
    return spans
```

```python
>>> tokens = ["Apple", "sued", "Google", "over", "iPhone", "sales", "."]
>>> labels = ["B-ORG", "O", "B-ORG", "O", "B-PRODUCT", "O", "O"]
>>> bio_to_spans(tokens, labels)
[(0, 1, 'ORG'), (2, 3, 'ORG'), (4, 5, 'PRODUCT')]
```

### Étape 2: Caractéristiques faites à la main

Pour les NER classiques (non neuronaux), les caractéristiques sont le jeu.

> Pour les classiques, les caractéristiques sont essentielles.

```python
def token_features(token, prev_token, next_token):
    return {
        "lower": token.lower(),
        "is_upper": token.isupper(),
        "is_title": token.istitle(),
        "has_digit": any(c.isdigit() for c in token),
        "suffix_3": token[-3:].lower(),
        "shape": word_shape(token),
        "prev_lower": prev_token.lower() if prev_token else "<BOS>",
        "next_lower": next_token.lower() if next_token else "<EOS>",
    }


def word_shape(word):
    out = []
    for c in word:
        if c.isupper():
            out.append("X")
        elif c.islower():
            out.append("x")
        elif c.isdigit():
            out.append("d")
        else:
            out.append(c)
    return "".join(out)
```

`word_shape("iPhone")`Retour `xXxxxx`- Je suis là .`word_shape("USA-2024")`Retour `XXX-dddd`Les modèles de capitalisation sont très significatifs pour les noms propres.

> `word_shape("iPhone")`Retour`xXxxxx`Il y a une autre.`word_shape("USA-2024")`Retour`XXX-dddd`◊ la mode d'écriture pour les noms spéciaux est un haut signal caractéristique.

### Étape 3: une base de référence simple basée sur des règles + dictionnaire

```python
ORG_GAZETTEER = {"Apple", "Google", "Microsoft", "OpenAI", "Meta", "Amazon", "Netflix"}
GPE_GAZETTEER = {"US", "USA", "UK", "India", "Germany", "France"}
PRODUCT_GAZETTEER = {"iPhone", "Android", "Windows", "ChatGPT", "Claude"}


def rule_based_ner(tokens):
    labels = []
    for token in tokens:
        if token in ORG_GAZETTEER:
            labels.append("B-ORG")
        elif token in GPE_GAZETTEER:
            labels.append("B-GPE")
        elif token in PRODUCT_GAZETTEER:
            labels.append("B-PRODUCT")
        else:
            labels.append("O")
    return labels
```

Les journaux de production ont des millions d'entrées extraites de Wikipédia et DBpedia.`Apple`La société contre les fruits) est terrible.

> Il y a des millions d'articles dans le vocabulaire de la région de la région de la région de la région, tirés de Wikipédia et de DBpedia 抓取──覆盖率不错──消歧(公司 `Apple`contre 水果 `apple`C'est la raison pour laquelle le modèle statistique a gagné.

### Étape 4: étape CRF (boîtier, pas implantation complète)

Le CRF complet à partir de zéro en 50 lignes n'est pas éclairant sans les bases de la théorie des probabilités.`sklearn-crfsuite`au lieu de:

>  sans base de probabilité  réaliser un CRF complet à partir de zéro dans 50                                                                                                                                                                                                                                                    `sklearn-crfsuite`- Le numéro de la liste:

```python
import sklearn_crfsuite

def to_features(tokens):
    out = []
    for i, tok in enumerate(tokens):
        prev = tokens[i - 1] if i > 0 else ""
        nxt = tokens[i + 1] if i + 1 < len(tokens) else ""
        out.append({
            "word.lower()": tok.lower(),
            "word.isupper()": tok.isupper(),
            "word.istitle()": tok.istitle(),
            "word.isdigit()": tok.isdigit(),
            "word.suffix3": tok[-3:].lower(),
            "word.shape": word_shape(tok),
            "prev.word.lower()": prev.lower(),
            "next.word.lower()": nxt.lower(),
            "BOS": i == 0,
            "EOS": i == len(tokens) - 1,
        })
    return out


crf = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True)
X_train = [to_features(s) for s in sentences_tokenized]
crf.fit(X_train, bio_labels_train)
```

`c1`et `c2`Les taux de régularisation de L1 et L2 sont: `all_possible_transitions=True`permet au modèle d'apprendre des séquences illégales (p. ex., `I-ORG`après `O`) sont peu probables, c'est pourquoi un CRF impose la cohérence des BIO sans que vous écriviez la contrainte.

> `c1`et `c2`Il est L1 et L2`all_possible_transitions=True`让模型学习非法序列 (par exemple)`O`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `I-ORG`) est peu probable, c'est la façon dont le CRF oblige la bio uniforme en cas de non-écriture.

### Étape 5: ce qu'ajoute un FCR BiLSTM

Les fonctionnalités deviennent apprises. Les entrées: embeddings de jetons (GloVe ou fastText). LSTM lit de gauche à droite et de droite à gauche. Les états cachés concaténés traversent une couche de sortie CRF. Le CRF impose toujours la cohérence de la séquence de balises; le LSTM remplace les fonctionnalités fabriquées à la main par des fonctionnalités apprises.

> Les caractéristiques sont modifiées en fonction de la couche de formation. Les caractéristiques sont modifiées en fonction de la couche de formation.

```python
import torch
import torch.nn as nn


class BiLSTM_CRF_Head(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_labels):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(hidden_dim * 2, n_labels)

    def forward(self, token_ids):
        e = self.embed(token_ids)
        h, _ = self.lstm(e)
        emissions = self.fc(h)
        return emissions
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

Pour la couche CRF, utiliser `torchcrf.CRF`Le gain sur le CRF fait à la main est mesurable mais plus petit que prévu à moins que vous ayez des dizaines de milliers de phrases étiquetées.

> L'utilisation de la CRF`torchcrf.CRF`(Pip install pytorch-crf) ⋅ Comparé à la CRF manuelle, l'augmentation de CRF est mesurable, mais à moins que vous n'ayez des milliers de phrases de marque,

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

spaCy expédie des NER de qualité de production hors boîte.

> L'espace est ouvert à la production de NER.

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple sued Google over its iPhone search deal in the US.")
for ent in doc.ents:
    print(f"{ent.text:20s} {ent.label_}")
```

```
Apple                ORG
Google               ORG
iPhone               ORG
US                   GPE
```

Remarque `iPhone`étiqueté `ORG`plutôt que `PRODUCT` Le modèle de petite taille de spaCy a une faible couverture des entités de produits.`en_core_web_lg`Le modèle transformateur (`en_core_web_trf`) est encore mieux.

> Attention !`iPhone`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `ORG`Il n'y a pas de`PRODUCT` le petit modèle de l'espace est plus faible que la couverture du produit physique.`en_core_web_lg`Il est aussi un modèle de transformateur.`en_core_web_trf`Je suis plus heureuse.

Faces d'embrassement pour NER à base de BERT:

> La NER basée sur BERT:

```python
from transformers import pipeline

ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
print(ner("Apple sued Google over its iPhone in the US."))
```

```
[{'entity_group': 'ORG', 'word': 'Apple', ...},
 {'entity_group': 'ORG', 'word': 'Google', ...},
 {'entity_group': 'MISC', 'word': 'iPhone', ...},
 {'entity_group': 'LOC', 'word': 'US', ...}]
```

`aggregation_strategy="simple"`Si vous ne le faites pas, vous obtenez des étiquettes au niveau des jetons et vous devez vous fusionner.

> `aggregation_strategy="simple"`Vous obtenez un étiquette de niveau B-X, vous devez vous-même le faire.

### NER fondé sur la MLL (option 2026)

Le LLM NER à tir zéro et à tir peu est désormais compétitif avec des modèles finement ajustés sur de nombreux domaines, et est nettement meilleur lorsque les données étiquetées sont rares.

> Le MLL NER est aujourd'hui compétitif dans de nombreux domaines avec les modèles de micro-modèles, avec de plus grands avantages en cas de pénurie de données d'étiquette.

- **Zero-shot prompting.**Donnez au LLM une liste de types d'entités et un schéma d'exemple. Demandez une sortie JSON. Fonctionne hors boîte; la précision est modérée sur les nouveaux domaines.
  **零样本提示。** donner à la LLM une liste de types et des exemples de modèle.
- **ZeroTuneBio-style prompting.**Décomposer la tâche en extraction de candidat → signification explication → jugement → re-check. Un prompt à plusieurs étapes (pas un seul coup) augmente considérablement la précision sur le NER biomédical. Le même schéma fonctionne pour les domaines juridique, financier et scientifique.
  **ZeroTuneBio 风格提示。**Le même modèle s'applique aux domaines de la loi, de la finance et de la science.
- **Dynamic prompting with RAG.**Retirer les exemples étiquetés les plus similaires à partir d'un petit ensemble de graines annotées pour chaque appel d'inférence; construire la demande de quelques coups en mouvement.
  **动态 RAG 提示。**Chaque réflexion est basée sur la recherche de l'échantillon d'étiquette le plus similaire à partir d'une petite quantité d'étiquettes; la formation de l'échantillon de suggestions est faible en 2026 et le taux de suggestions de GPT-4 en biomédecine NER F1 est en hausse de 11 à 12% par rapport à l'échantillon d'étiquettes statiques.
- **Per-entity-type decomposition.**Pour les documents longs, un appel unique qui extrait tous les types d'entités à la fois perd le rappel à mesure que la longueur augmente. Exécuter un passe d'extraction par type d'entité. Coût d'inférence plus élevé, précision nettement plus élevée. C'est le modèle standard pour les notes cliniques et les contrats juridiques.
  **按实体类型分解。**Pour les archives longues, une fois la mise en œuvre de tous les types d'entités, le taux de perte de réception augmente avec la durée.

Recommandation de production à partir de 2026: commencez par un programme de base de la formation de licence avant de collecter les données de formation.

> 2026: Avant de recueillir les données de formation, commencez d'abord à utiliser le programme de formation en ligne de base.

### Où la NER classique gagne toujours

Même avec des LLM disponibles, la NER classique gagne lorsque:

> Même si vous avez un LLM, vous pouvez obtenir un diplôme de la NER dans les cas suivants:

- Le budget de latence est inférieur à 50 ms.
  Le budget de retard est inférieur à 50 millimètres de seconde.
- Vous avez des milliers d'exemples étiquetés et vous avez besoin de 98% + F1.
  Vous avez des milliers d'échantillons et vous avez besoin de 98% + F1
- Le domaine a une ontologie stable où un CRF ou un BiLSTM prétrainé transfère bien.
   domaines ayant un corps physique stable, pré-entraînement du CRF ou du BiLSTM   迁移良好──
- Les contraintes réglementaires exigent un modèle non génératif sur place.
  监管约束要求本地部署的非生成式模型──

### Là où il s'effondre

- **Domain shift.**Le NER formé à la LNC sur les contrats juridiques fonctionne pire qu'un journaliste.
  **领域偏移。**En ce qui concerne la formation de la NER, le NER est également différent de celui du vocabulaire.
- **Nested entities.**La "Bank of America Tower" est à la fois un ORG et une FACEILITÉ. La norme BIO ne peut pas représenter des spans se chevauchant.
  **嵌套实体。**"Bank of America Tower" est également un ORG et une facilité.
- **Long entities.**"Corporation fédérale d'assurance dépôt des États-Unis". Les modèles au niveau des jetons divisent parfois ceci.`aggregation_strategy`ou après le traitement.
  **长实体。**"Corporation fédérale d'assurance dépôts des États-Unis"`aggregation_strategy`Ou après traitement.
- **Sparse types.**Les étiquettes médicales NER comme DRUG_BRAND, ADVERSE_EVENT, DOSE. Les modèles à usage général n'ont aucune idée.
  **稀疏类型。**Le système de santé de la société est un système de santé qui est un facteur de développement.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-ner-picker.md`- Le numéro de la liste:

> 保存为 `outputs/skill-ner-picker.md`- Le numéro de la liste:

```markdown
---
name: ner-picker
description: Pick the right NER approach for a given extraction task.
version: 1.0.0
phase: 5
lesson: 06
tags: [nlp, ner, extraction]
---

Given a task description (domain, label set, language, latency, data volume), output:

1. Approach. Rule-based + gazetteer, CRF, BiLSTM-CRF, or transformer fine-tune.
2. Starting model. Name it (spaCy model ID, Hugging Face checkpoint ID, or "custom, trained from scratch").
3. Labeling strategy. BIO, BILOU, or span-based. Justify in one sentence.
4. Evaluation. Use `seqeval`. Always report entity-level F1 (not token-level).

Refuse to recommend fine-tuning a transformer for under 500 labeled examples unless the user already has a pretrained domain model. Flag nested entities as needing span-based or multi-pass models. Require a gazetteer audit if the user mentions "production scale" and labels are unchanged from CoNLL-2003.
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les exercices

1. **Easy.**Mise en œuvre `bio_to_spans`(l' inverse de `spans_to_bio`) et vérifier la cohérence entre les deux phrases.
   **简单。** réaliser `bio_to_spans`(le secteur de l'énergie)`spans_to_bio`de la fonction inverse) et de la cohérence de 10 phrases.
2. **Medium.**Trainer le CRF sklearn-crfsuite ci-dessus sur le ensemble de données NER anglais CoNLL-2003.`seqeval`Résultat typique: ~84 F1.
   **中等。**En 2003 en anglais NER données collectes de formation sur le marché de l'emploi.`seqeval`報告每类 F1──典型结果: ~84 F1──
3. **Hard.**- Je suis bien .`distilbert-base-cased`Les données de l'équipe de recherche sont également disponibles sur un ensemble de données NER spécifique à un domaine (médicale, juridique ou financière).
   **困难。**Dans un domaine spécifique, les données NER (medicine, droit ou finance) sont réduites.`distilbert-base-cased`◊ Comparer avec l'espace ◊ Comparer avec l'espace ◊ enregistrer des fuites de données ◊ vérifier et écrire en bas de faire vous surprendre là où ◊

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Les termes clés

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NER（命名实体识别） | Extract names / 提取名字 | Label token spans with types (PERSON, ORG, GPE, DATE, ...). / 用类型（PERSON、ORG、GPE、DATE 等）标注 token 跨度。 |
| BIO | Tagging scheme / 标注方案 | `B-X` begins, `I-X` continues, `O` outside. / `B-X` 开始，`I-X` 继续，`O` 外部。 |
| BILOU | Better BIO / 更好的 BIO | Adds `L-X` (last), `U-X` (unit) for cleaner boundaries. / 添加 `L-X`（最后）、`U-X`（单元）以获得更清晰的边界。 |
| CRF（条件随机场） | Structured classifier / 结构化分类器 | Models transitions between labels, not just emissions. Enforces valid sequences. / 对标签间的转移建模，而不仅仅是发射。强制有效序列。 |
| Nested NER（嵌套 NER） | Overlapping entities / 重叠实体 | One span is a different entity than a sub-span of it. BIO cannot express this. / 一个跨度与其子跨度是不同的实体。BIO 无法表达这一点。 |
| Entity-level F1（实体级 F1） | Proper NER metric / 正确的 NER 指标 | Predicted span must match true span exactly. Token-level F1 overstates accuracy. / 预测跨度必须与真实跨度完全匹配。Token 级 F1 会高估准确率。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.

## Encore une lecture

- [Lample et al. (2016). Neural Architectures for Named Entity Recognition](https://arxiv.org/abs/1603.01360) le document BiLSTM-CRF. Canonical. / BiLSTM-CRF 论文──经典──
- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805) introduit le modèle de classification des jetons qui est devenu standard. /  introduced into becoming standard's token 分类模式──
- [spaCy linguistic features — named entities](https://spacy.io/usage/linguistic-features#named-entities) référence pratique pour chaque attribut de `Doc.ents`et `Span`- Je suis là .`Doc.ents`et `Span`Références pratiques de chaque attribut.
- [seqeval](https://github.com/chakki-works/seqeval) la bibliothèque métrique correcte. Utilisez-la toujours. / 正确的指标库──始终使用它──
