# L'étiquetage de POS et le partage syntaxique

> La grammaire était hors mode pendant un moment, puis chaque pipeline de LLM devait valider l'extraction structurée, et elle est revenue.
> Le langage a été autrefois peu populaire.

> **【中文解读】**给每一个词标注词性, analyse la structure du langage de chaque phrase.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

La leçon 1 promettait que la lemmatization avait besoin d'une étiquette de partie du discours.`running`est un verbe, un lemmatizer ne peut pas le réduire à `run`Sans le savoir .`better`est un adjectif, il ne peut pas se réduire à `good`- Je suis désolé .

> 第01 课承诺过词形还原需要词性标注──不知道 `running`Il est impossible de le récupérer.`run`Je ne sais pas.`better`Il est impossible de le récupérer.`good`Il y a une autre.

Cette promesse cachait un sous-field entier. L'étiquetage de la partie de la parole assigne des catégories grammaticales. L'analyse syntaxique récupère la structure de l'arbre de la phrase: quel mot modifie lequel, quel verbe gouverne quels arguments. La PNL classique a passé vingt ans à affiner les deux. Puis l'apprentissage profond les a effondrés en une tâche de classification des jetons en plus d'un transformateur prétrainé, et la communauté de recherche a déménagé.

> Le NLP classique a passé deux décennies à perfectionner ces deux éléments. Ensuite, l'apprentissage en profondeur les va plier en tant que pré-entraînement.

La communauté appliquée n'est pas la communauté. Chaque pipeline d'extraction structurée utilise toujours des arbres de POS et de dépendance sous le capot. Le JSON généré par LLM est validé contre des contraintes grammaticales. Les systèmes de réponse aux questions décomposent les requêtes en utilisant des parses de dépendance. Les évaluateurs de qualité de la traduction automatique vérifient l'alignement des arbres de parse.

> 应用界没有──每个结构化抽取流水线仍在底层使用POS 和依赖树──LLM 生成的JSON 会根据语法约束进行验证──问答系统使用依赖分析来分解查询──机器翻译质量评估器检查分析树的对齐──

Cette leçon présente les tags, les lignes de base et le point où vous arrêtez de mettre en œuvre à partir de zéro et appelez spaCy.

> Il est intéressant de comprendre.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

**POS tagging**Les étiquettes de chaque symbole sont classées dans une catégorie grammaticale.**Penn Treebank (PTB)**Tagset est la version anglaise par défaut. 36 tags avec distinctions le lecteur occasionnel trouve difficile: `NN`nom singulier, `NNS`nom pluriel, `NNP`nom propre singulier, `VBD`verbe passé,`VBZ`Le verbe 3ème personne singular présent, et ainsi de suite.**Universal Dependencies (UD)**Tagset est plus grossier (17 tags) et linguistique; il est devenu le modèle par défaut pour le travail multilingue.

> **词性标注（POS Tagging）**Pour chaque symbole, il y a une classe de mots.**Penn Treebank (PTB)**标签集是英语的默认选择──36标签,带有一般读者觉得过于细致的区别:`NN`单数名词`NNS`复数名词`NNP`专名词单数、`VBD`动词过去时,`VBZ`动词第三人称单数现在时等等等──**通用依存（Universal Dependencies, UD）**Il est devenu une option partagée dans le travail translinguiste.

```
The/DET cats/NOUN were/AUX running/VERB at/ADP 3pm/NOUN ./PUNCT
```

**Syntactic parsing**Il y a deux styles principaux:

> **句法分析（Syntactic Parsing）**产生一棵树──两种主要风格:

- **Constituency parsing.**Les phrases de noms, les phrases verbales, les phrases prépositionnelles s'installent l'une à l'intérieur de l'autre.
  **成分分析（Constituency Parsing）。**Nom: N°1 (en anglais seulement)
- **Dependency parsing.**Chaque mot a un seul mot de tête sur lequel il dépend, étiqueté avec une relation grammaticale.
  **依存分析（Dependency Parsing）。**Chaque mot a un mot central qui le domine, marque le lien.

Le partage de la dépendance a été gagné dans les années 2010 car il généralise nettement les langues, en particulier celles d'ordre de mots libre.

> L'analyse dépendante a gagné en 2010 parce qu'elle est transnationale et est devenue plus efficace, en particulier dans les langues de base.

```
running is ROOT
cats is nsubj of running
were is aux of running
at is prep of running
3pm is pobj of at
```

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
pos-tagger
```

```figure
dependency-arcs
```

## Faites-le

### Étape 1: ligne de base de la marque la plus fréquente

Pour chaque mot, prévoir la balise qu'il avait le plus souvent en formation.

> Pour chaque mot, prévoir que c'est le plus courant dans l'entraînement.

```python
from collections import Counter, defaultdict


def train_mft(train_examples):
    word_tag_counts = defaultdict(Counter)
    all_tags = Counter()
    for tokens, tags in train_examples:
        for token, tag in zip(tokens, tags):
            word_tag_counts[token.lower()][tag] += 1
            all_tags[tag] += 1
    word_best = {w: c.most_common(1)[0][0] for w, c in word_tag_counts.items()}
    default_tag = all_tags.most_common(1)[0][0]
    return word_best, default_tag


def predict_mft(tokens, word_best, default_tag):
    return [word_best.get(t.lower(), default_tag) for t in tokens]
```

Sur le corpus Brown, cette ligne de base atteint une précision de 85%.

> Dans la bibliothèque de langage brune, cette ligne de base atteint environ 85% de précision.

### Étape 2: étiquette HMM à bigramme

Modélisez la probabilité commune de la séquence:

> 建模序列的联合概率:

```
P(tags, words) = prod P(tag_i | tag_{i-1}) * P(word_i | tag_i)
```

Deux tableaux: probabilités de transition (tag donné la tag précédente), probabilités d'émission (tag donné le mot). Estimer les deux à partir des comptes avec l'allumage Laplace. Décoder avec Viterbi (programming dynamique sur le réseau de tag).

> 两个表:转移概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射概率 (),发射) 两者均从计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计计

```python
import math


def train_hmm(train_examples, alpha=0.01):
    transitions = defaultdict(Counter)
    emissions = defaultdict(Counter)
    tags = set()
    vocab = set()

    for tokens, ts in train_examples:
        prev = "<BOS>"
        for token, tag in zip(tokens, ts):
            transitions[prev][tag] += 1
            emissions[tag][token.lower()] += 1
            tags.add(tag)
            vocab.add(token.lower())
            prev = tag
        transitions[prev]["<EOS>"] += 1

    return transitions, emissions, tags, vocab


def log_prob(table, given, key, smooth_denom, alpha):
    return math.log((table[given].get(key, 0) + alpha) / smooth_denom)


def viterbi(tokens, transitions, emissions, tags, vocab, alpha=0.01):
    tags_list = list(tags)
    n = len(tokens)
    V = [[0.0] * len(tags_list) for _ in range(n)]
    back = [[0] * len(tags_list) for _ in range(n)]

    for j, tag in enumerate(tags_list):
        em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
        tr_denom = sum(transitions["<BOS>"].values()) + alpha * (len(tags_list) + 1)
        tr = log_prob(transitions, "<BOS>", tag, tr_denom, alpha)
        em = log_prob(emissions, tag, tokens[0].lower(), em_denom, alpha)
        V[0][j] = tr + em
        back[0][j] = 0

    for i in range(1, n):
        for j, tag in enumerate(tags_list):
            em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
            em = log_prob(emissions, tag, tokens[i].lower(), em_denom, alpha)
            best_prev = 0
            best_score = -1e30
            for k, prev_tag in enumerate(tags_list):
                tr_denom = sum(transitions[prev_tag].values()) + alpha * (len(tags_list) + 1)
                tr = log_prob(transitions, prev_tag, tag, tr_denom, alpha)
                score = V[i - 1][k] + tr + em
                if score > best_score:
                    best_score = score
                    best_prev = k
            V[i][j] = best_score
            back[i][j] = best_prev

    last_best = max(range(len(tags_list)), key=lambda j: V[n - 1][j])
    path = [last_best]
    for i in range(n - 1, 0, -1):
        path.append(back[i][path[-1]])
    return [tags_list[j] for j in reversed(path)]
```

Le Bigram HMM sur Brown atteint ~93% de précision. Le saut de 85% à 93% est principalement des probabilités de transition  le modèle apprend `DET NOUN`est commun et `NOUN DET`C'est rare.

> Dans le brown 语料库上二元组 HMM 达到约93% de précision                                                                                                                                                                                                                                                    `DET NOUN`C'est le cas de tous les jours.`NOUN DET`C'est rare.

### Étape 3: pourquoi les taggers modernes ont battu ce

Les probabilités de transition + émission sont locales.`saw`est un nom dans "J'ai acheté une scie" mais un verbe dans "J'ai vu le film". Un CRF avec des caractéristiques arbitraires (suffixe, forme de mot, mot avant et après, mot lui-même) atteint ~97%. Un BiLSTM-CRF ou transformateur atteint ~98%+.

> Le taux de transfert + de sortie est local.`saw`Dans le cas de "J'ai acheté une scie" il y a un nombre de mots mais dans le cas de "J'ai vu le film" il y a un mot.

Les annotateurs humains sont d'accord sur 97% du temps sur Penn Treebank. Les modèles au-delà de 98% sont probablement trop adaptés au jeu de test.

> Le plan de cette tâche est déterminé par les émetteurs de la liste. Les émetteurs de la liste humaine sont arrivés à un accord à environ 97% du temps de la Penn Treebank.

### Étape 4: schéma d'analyse de dépendance

La totalité de la dépendance paralysant à partir de zéro est hors de portée; le traitement canonique des manuels est dans Jurafsky et Martin.

> De la réalisation de l'analyse complète dépasse la portée; les deux séries classiques de cours de traitement voir Jurafsky et Martin.

- **Transition-based**Les parser (arcs-eager, arc-standard) agissent comme un parser réducteur de changement: ils lisent des jetons, les déplacent sur une pile et appliquent des actions réductrices qui créent des arcs. Le décoding avide est rapide. La mise en œuvre classique est MaltParser.
  **基于转移的**解析器(arc-eager、arc-standard) Comme un résolveur de mouvement:读进代币,移进到上,应用创建弧的归约动作──贪解码很快──经典实现是MaltParser──现代神经版本:Chen 和 Manning 的基于转移的解析器──
- **Graph-based**Les parseurs (algorithme d'Eisner, Dozat-Manning biaffine) marquent chaque bord possible dépendant de la tête et choisissent l'arbre d'étendue maximale.
  **基于图的**解析器(Eisner 算法、Dozat-Manning 双仿射) à chaque possible tête dépendante 边打分, choisir le plus grand générer arbre。

Pour la plupart des travaux appliqués, appelez spaCy:

>  Pour la plupart des applications, il faut utiliser l'espace:

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running at 3pm.")
for token in doc:
    print(f"{token.text:10s} tag={token.tag_:5s} pos={token.pos_:6s} dep={token.dep_:10s} head={token.head.text}")
```

```
The        tag=DT    pos=DET    dep=det        head=cats
cats       tag=NNS   pos=NOUN   dep=nsubj      head=running
were       tag=VBD   pos=AUX    dep=aux        head=running
running    tag=VBG   pos=VERB   dep=ROOT       head=running
at         tag=IN    pos=ADP    dep=prep       head=running
3pm        tag=NN    pos=NOUN   dep=pobj       head=at
.          tag=.     pos=PUNCT  dep=punct      head=running
```

Lisez le `dep`la colonne de bas en haut et la structure grammaticale de la phrase tombe.

> De la descente à la descente`dep`La structure de la phrase est naturellement présente.

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

Chaque bibliothèque de PNL de production envoie des parseurs de POS et de dépendance dans le cadre d'un pipeline standard.

> Chaque production de PNL est fournie par un POS et un résolveur dépendant.

- **spaCy**(le secteur de l'énergie)`en_core_web_sm`- Je suis là .`md`- Je suis là .`lg`- Je suis là .`trf`) Rapide, précis, intégré à la tokenization + NER + lemmatization. `token.tag_`Je suis désolé.`token.pos_`(UD), `token.dep_`(relation de dépendance).
  **spaCy**(le secteur de l'énergie)`en_core_web_sm`- Je suis là .`md`- Je suis là .`lg`- Je suis là .`trf`)──快速、准确,与分词 + NER + 词形还原集成──`token.tag_`Je suis désolé.`token.pos_`(UD)`token.dep_`Je suis en train de faire une petite histoire.
- **Stanford NLP (stanza)**Le successeur de Stanford au CoreNLP.
  **Stanford NLP (stanza)** Successeur de Stanford CoreNLP  atteindre un niveau avancé dans plus de 60 langues 
- **trankit**- Basé sur un transformateur, bonne précision UD.
  **trankit** Basé sur le Transformer, bon taux de détection des données 准确率
- **NLTK**- Je suis là .`pos_tag`Utilisable, lent, plus âgé, bon pour enseigner.
  **NLTK**Il y a une autre.`pos_tag`◊可用、慢、较旧── adapté à l'enseignement。

### Où cela importe encore en 2026

- **Lemmatization.**La leçon 1 a besoin de la POS pour le lemmatizer correctement.
  **词形还原。**Il faut toujours que les gens fassent des choses comme ça.
- **Structured extraction from LLM outputs.**Valider que la phrase générée respecte les contraintes grammaticales (par exemple, accord sujet-verbe, modificateurs requis).
  **LLM 输出的结构化抽取。**验证生成的句子满足语法约束 (en anglais seulement)
- **Aspect-based sentiment.**Les parses de dépendance vous disent quel adjectif modifie quel nom.
  **基于方面的情感分析。**L'analyse dépendante vous dit quel est le nom de l'expression.
- **Query understanding.**"les films réalisés par Wes Anderson avec Bill Murray" se décomposent en contraintes structurées par le biais de l'analyse.
  **查询理解。**"films réalisés par Wes Anderson et mettant en vedette Bill Murray"
- **Cross-lingual transfer.**Les balises UD et les relations de dépendance sont agnostiques par rapport aux langues, ce qui permet une analyse structurée sans échec des nouvelles langues.
  **跨语言迁移。**UD 标签和依赖与语言无关,支持新语言的零样本结构化分析──
- **Low-compute pipelines.**Si vous ne pouvez pas expédier un transformateur, POS + dépistage de dépendance + gazetté vous emmène étonnamment loin.
  **低算力流水线。**Si vous ne pouvez pas déployer Transformer, POS + 依存分析 + 地名词典能让你走相当远――

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-grammar-pipeline.md`- Le numéro de la liste:

> 保存为 `outputs/skill-grammar-pipeline.md`- Le numéro de la liste:

```markdown
---
name: grammar-pipeline
description: Design a classical POS + dependency pipeline for a downstream NLP task.
version: 1.0.0
phase: 5
lesson: 07
tags: [nlp, pos, parsing]
---

Given a downstream task (information extraction, rewrite validation, query decomposition, lemmatization), you output:

1. Tagset to use. Penn Treebank for English-only legacy pipelines, Universal Dependencies for multilingual or cross-lingual.
2. Library. spaCy for most production, stanza for academic-grade multilingual, trankit for highest UD accuracy. Name the specific model ID.
3. Integration pattern. Show the 3-5 lines that call the library and consume the needed attributes (`.pos_`, `.dep_`, `.head`).
4. Failure mode to test. Noun-verb ambiguity (`saw`, `book`, `can`) and PP-attachment ambiguity are the classical traps. Sample 20 outputs and eyeball.

Refuse to recommend rolling your own parser. Building parsers from scratch is a research project, not an application task. Flag any pipeline that consumes POS tags without handling lowercase/uppercase variants as fragile.
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les exercices

1. **Easy.**En utilisant la ligne de base de la balise la plus fréquente sur un petit corpus de balises (par exemple, le sous-ensemble Brown de NLTK), mesurez l'exactitude des phrases retenues. Vérifiez le résultat de ~ 85%.
   **简单。**Dans un petit étiquette (comme le NLTK) utilisé le plus souvent sur le langage de référence, la mesure a permis de mesurer le taux de précision des phrases sorties.
2. **Medium.**Exercez le HMM de bigramme ci-dessus et rapportez la précision/reprise par balise.
   **中等。**訓練上述二元组 HMM 并报告每标签精确率/召回率──HMM Quels sont les étiquettes les plus faciles à confondre?
3. **Hard.**Utilisez l'analyse de dépendance de spaCy pour extraire des triples sujet-verbe-objet d'un échantillon de 1000 phrases. Évaluez sur 50 triples labellés manuellement. Document où l'extraction échoue (souvent passifs, coordonnées et sujets éliminés).
   **困难。**Utilisez l'analyse de la dépendance de l'espace à partir de 1000 exemples de phrases pour tirer le principal titre de l'étiquette.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Les termes clés

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| POS tag（词性标签） | Word's type / 词的类型 | Grammatical category. PTB has 36; UD has 17. / 语法类别。PTB 有 36 个；UD 有 17 个。 |
| Penn Treebank | Standard tagset / 标准标签集 | English-specific. Fine-grained verb tenses and noun number. / 特定于英语。细粒度的动词时态和名词数。 |
| Universal Dependencies（通用依存） | Multilingual tagset / 多语言标签集 | Coarser than PTB; language-neutral; defaults for cross-lingual work. / 比 PTB 更粗；语言无关；跨语言工作的默认选择。 |
| Dependency parse（依存分析） | Sentence tree / 句子树 | Each word has one head, each edge has a grammatical relation. / 每个词有一个中心词，每条边有一个语法关系。 |
| Viterbi（维特比算法） | Dynamic programming / 动态规划 | Finds the highest-probability tag sequence given emissions and transitions. / 给定发射和转移概率，找到最高概率的标签序列。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.

## Encore une lecture

- [Jurafsky and Martin — Speech and Language Processing, chapters 8 and 18](https://web.stanford.edu/~jurafsky/slp3/) le traitement canonique des manuels de lecture de POS et de parsing. / POS 和解析的经典教科书处理──
- [Universal Dependencies project](https://universaldependencies.org/) le ensemble de balises et de collections de banques utilisés par chaque parseur multilingue. / 每个多语言解析器使用的跨语言标签集和树库集合。
- [spaCy linguistic features guide](https://spacy.io/usage/linguistic-features) référence pratique pour chaque attribut exposé sur `Token`- Je suis là .`Token`Références pratiques à chaque facteur de l'exposition.
- [Chen and Manning (2014). A Fast and Accurate Dependency Parser using Neural Networks](https://nlp.stanford.edu/pubs/emnlp2014-depparser.pdf)Le papier qui a introduit les parieurs neuronaux dans le courant dominant.
