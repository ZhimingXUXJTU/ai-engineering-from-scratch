# Le traitement du texte  Tokenization, Stemming, Lemmatization  文本处理  分词、词干提取、词形還原

> Le langage est continu, les modèles sont discrets, le prétraitement est le pont.
> Le langage est continu. Le modèle est dispersé.

> **【中文解读】**Le mot "réinitialisation" est le premier élément de la PNL: mettre en œuvre les techniques de traitement des mots.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Objectifs d'apprentissage

- Comprendre la tokenization, la stemming et la lemmatization comme des opérations de pré-traitement distinctes
  Comprendre le mot-clé
- Construisez un jeton regex, un pas Porter voter, et un lemmatizer basé sur la recherche à partir de zéro
  De la conception de la forme de l'expression à partir de la définition de la forme de l'expression
- Comparer NLTK et spaCy pour les pipelines de pré-traitement de production
  Comparer NLTK et espaCy dans la production pré-traitement des flux d'eau
- Reconnaître les deux défaillances de production les plus courantes: dérive de reproductibilité et désaccord entre train et inférence
  Identification des deux défauts de production les plus courants: détérioration réactive et entraînement/réflexion non compatible

## Le problème , l' introduction du problème

Un modèle ne peut pas lire "Les chats couraient". Il lit des nombres entiers.

> 模型不能直接读取 "Les chats couraient".

Chaque système de PNL ouvre avec les mêmes trois questions. Où commence un mot. Quelle est la racine du mot. Comment traiter "courir", "courir", "courir" comme la même chose quand cela aide, et comme des choses différentes quand cela ne le fait pas.

> Chaque système de PNL doit répondre aux mêmes trois questions: un mot de où commence-t-il? quelle est la racine du mot? comment allons-nous "courir" quand nous avons besoin, "courir" quand nous avons besoin, "courir" quand nous avons besoin, voir la même chose, et différencier le traitement quand nous n'avons pas besoin?

Si vous faites une mauvaise tokenization, le modèle apprend à partir des ordures.`don't`comme un seul symbole mais `do n't`Si votre vote s'effondre, vous pouvez vous faire une idée.`organization`et `organ`Si votre lemmatizer a besoin d'un contexte de part de la parole mais que vous ne le passez pas, les verbes sont traités comme des noms.

> Le modèle est d'apprendre à partir de données de déchets.`don't`Comme un signe, mais tu le fais.`do n't`Quand on est deux, on se divise.`organization`et `organ`归结为同一个词干,主题建模就会失效──如果你的词形还原器需要词性上下文但你没有传入,动词就会被当作名词处理──

Cette leçon construit les trois étapes de pré-traitement à partir de zéro, puis montre comment NLTK et spaCy font le même travail afin que vous puissiez voir les compromis.

> Ce cours commence par la construction de ces trois étapes de prélèvement, puis montre comment faire le même travail par la NLTK et l'espaceCy, vous permettant de voir le poids de l'un d'eux.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

Trois opérations, chacune avec un travail et un mode d'échec.

> Trois opérations, chacun a ses propres responsabilités et mode de défaillance.

**Tokenization**Le mot "token" est délibérément vague parce que la bonne granularité dépend de la tâche.

> **分词（Tokenization）**Le mot "Token" est intentionnellement obscurci, car la granulance adaptée dépend de la tâche spécifique.

**Stemming**Il y a des suffixes avec des règles, rapide, agressif, stupide.`running -> run`- Je suis là .`organization -> organ`Le second est le mode défaillance.

> **词干提取（Stemming）**Utilisation des règles de la procédure de réception`running -> run`Il y a une autre.`organization -> organ`Le deuxième exemple est son mode de défaite.

**Lemmatization**Le nombre de mots dans un dictionnaire est réduit à un nombre de mots en utilisant des connaissances grammaticales.`ran -> run`(il faut savoir que "run" est passé de "run").`better -> good`(ne doit connaître les formes comparatives).

> **词形还原（Lemmatization）**Utiliser le langage français pour traduire les mots en forme de langage.`ran -> run`(Ne pas oublier que "courir" est le passé de "courir")`better -> good`(Ne pas oublier la comparaison de la classe)

Règlement général: écoute quand la vitesse est importante et que tu peux tolérer le bruit (indexation de recherche, classification approximative). Lemmatize quand le sens est important (réponse à la question, recherche sémantique, tout ce que l'utilisateur lira).

> 经验法则: lorsque la vitesse est importante et peut tolérer le bruit, l'utilisation du mot干提取 (en anglais) 搜索引、粗略分类) ⋅ lorsque l'utilisation du mot forma还原 (en anglais) ⋅

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
edit-distance
```

## Faites-le

### Étape 1: un jeton de mot regex

Le jeton de jeton le plus simple est divisé en caractères non alphanumériques tout en conservant la ponctuation comme jeton.

> Le plus simple et pratique des mots-clés sont divisés en caractères numériques non-écrites, tout en conservant le symbole de marque comme symbole indépendant.

```python
import re

def tokenize(text):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[0-9]+|[^\sA-Za-z0-9]", text)
```

Trois modèles dans l'ordre de prééminence.`don't`- Je suis là .`it's`) Nombre pur: tout caractère non alphanumérique unique non en espace blanc en tant que symbole autonome (punctuation).

> Trois mots de rang de priorité`don't`- Je suis là.`it's`)。Pure numérique。Quelque single non-blanc non-écriture numérique caractère comme symbole indépendant(标点符号)。

```python
>>> tokenize("The cats weren't running at 3pm.")
['The', 'cats', "weren't", 'running', 'at', '3', 'pm', '.']
```

Mode d'échec à remarquer. `3pm`Les fractions sont divisées en `['3', 'pm']`parce que nous avons alterné entre les courriels de lettres et les courriels de chiffres. assez pour la plupart des tâches. URL, courriels, hashtags sont tous cassés. Pour la production, ajoutez des modèles avant les plus généraux.

> Il faut faire attention à la façon dont on échoue.`3pm`Ils ont été démolis.`['3', 'pm']`, parce que nous avons fait un échange entre les séquences lettres et les séquences numériques. Pour la plupart des tâches, il est suffisant.

### Étape 2: un Porter stemmer (pas seulement 1a)

L'algorithme complet de Porter comporte cinq phases de règles.

> L'algorithme complet de Porter a cinq étapes de règles. Seulement l'étape 1a couvre les plus courantes en anglais et présente le modèle de règles.

```python
def stem_step_1a(word):
    if word.endswith("sses"):
        return word[:-2]
    if word.endswith("ies"):
        return word[:-2]
    if word.endswith("ss"):
        return word
    if word.endswith("s") and len(word) > 1:
        return word[:-1]
    return word
```

```python
>>> [stem_step_1a(w) for w in ["caresses", "ponies", "caress", "cats"]]
['caress', 'poni', 'caress', 'cat']
```

Lisez les règles de haut en bas.`ies -> i`La règle est la raison .`ponies -> poni`- Je ne sais pas .`pony`Le vrai Porter a l'étape 1B qui le corrige, les règles se disputent, les règles antérieures gagnent, l'ordre compte plus que toute autre règle.

> De haut en bas`ies -> i`La règle est:`ponies -> poni`Au lieu de`pony`Les règles se disputent entre elles, les règles de l'avant gagnent. L'ordre des règles est plus important que n'importe quelle autre règle.

### Étape 3: un lemmatizer basé sur la recherche

La lématisation appropriée nécessite une morphologie.

> Une version pédagogique pratique utilisant des petits dictionnaires et des stratégies de préparation.

```python
LEMMA_TABLE = {
    ("running", "VERB"): "run",
    ("ran", "VERB"): "run",
    ("runs", "VERB"): "run",
    ("better", "ADJ"): "good",
    ("best", "ADJ"): "good",
    ("cats", "NOUN"): "cat",
    ("cat", "NOUN"): "cat",
    ("were", "VERB"): "be",
    ("was", "VERB"): "be",
    ("is", "VERB"): "be",
}

def lemmatize(word, pos):
    key = (word.lower(), pos)
    if key in LEMMA_TABLE:
        return LEMMA_TABLE[key]
    if pos == "VERB" and word.endswith("ing"):
        return word[:-3]
    if pos == "NOUN" and word.endswith("s"):
        return word[:-1]
    return word.lower()
```

```python
>>> lemmatize("running", "VERB")
'run'
>>> lemmatize("cats", "NOUN")
'cat'
>>> lemmatize("better", "ADJ")
'good'
>>> lemmatize("watched", "VERB")
'watched'
```

Le dernier cas est le moment clé de l'enseignement. `watched`Il n' est pas à notre table et notre renversement ne fait que gérer`ing`- Une vraie lemmatisation couvre`ed`, verbes irréguliers, adjectifs comparatifs, plurales avec changements sonores (`children -> child`C'est pourquoi les systèmes de production utilisent WordNet, le morphologiseur de spaCy, ou un analyseur morphologique complet.

> Le dernier exemple est un moment clé de l'enseignement.`watched`Pas dans notre liste, mais notre stratégie de réserve ne traite que.`ing`◊ ⇒ réellement`ed`、不规则动词、比较级形容词、语音变化的复数(`children -> child`)¬ c'est pourquoi le système de production utilise WordNet, un analyseur de forme spatiale ou un analyseur de forme complet¬¬

### Étape 4: les raccorder

```python
def preprocess(text, pos_tagger=None):
    tokens = tokenize(text)
    stems = [stem_step_1a(t.lower()) for t in tokens]
    tags = pos_tagger(tokens) if pos_tagger else [(t, "NOUN") for t in tokens]
    lemmas = [lemmatize(word, pos) for word, pos in tags]
    return {"tokens": tokens, "stems": stems, "lemmas": lemmas}
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

La pièce manquante est un tagger POS. phase 5 · 07 (POS Tagging) en construit un. Pour l'instant, tout est par défaut à `NOUN`et reconnaissez la limitation.

> 缺少的部分是词性标注器──Phase 5 · 07(词性标注) va construire un──`NOUN`Je reconnais cette limitation.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

NLTK et spaCy expédient les versions de production.

> NLTK et spaCy ont fourni une version de production.

### NLTK

```python
import nltk
nltk.download("punkt_tab")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger_eng")

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag

text = "The cats were running."
tokens = word_tokenize(text)
stems = [PorterStemmer().stem(t) for t in tokens]
lemmatizer = WordNetLemmatizer()
tagged = pos_tag(tokens)


def nltk_pos_to_wordnet(tag):
    if tag.startswith("V"):
        return "v"
    if tag.startswith("J"):
        return "a"
    if tag.startswith("R"):
        return "r"
    return "n"


lemmas = [lemmatizer.lemmatize(t, nltk_pos_to_wordnet(tag)) for t, tag in tagged]
```

`word_tokenize`Il traite les contractions, l'Unicode, les cas de bord que votre regex manque.`PorterStemmer`Il est en cinq phases.`WordNetLemmatizer`Il faut traduire la balise POS du schéma Penn Treebank de NLTK vers l'ensemble d'abréviations de WordNet.

> `word_tokenize`处理缩写、Unicode 和你的正则表达式遗漏的边界情况──`PorterStemmer`Il y a cinq étapes.`WordNetLemmatizer`需要将 NLTK's Penn Treebank 词性标注方案转换为 WordNet's缩写集──

### - le secteur

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running.")

for token in doc:
    print(token.text, token.lemma_, token.pos_)
```

```
The      the     DET
cats     cat     NOUN
were     be      AUX
running  run     VERB
.        .       PUNCT
```

SpaCy cache l'ensemble du pipeline derrière.`nlp(text)`- La marquage, le POS et la lemmatization fonctionnent tous. Plus rapide que NLTK à l'échelle. Plus précis à l'extérieur de la boîte.

> L' espace sera entièrement caché dans la ligne de l' eau.`nlp(text)`背后──分词、词性标注和词形还原全部运行──大规模下比NLTK更快,开箱即用更准确──代价是你无法轻松替换单个组件──

### Quand choisir lequel

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Teaching, research, swapping components | NLTK | 教学、研究、需要替换组件 | NLTK |
| Production, multi-language, speed matters | spaCy | 生产环境、多语言、速度要求高 | spaCy |
| Transformer pipeline (you'll tokenize with the model's tokenizer anyway) | Use `tokenizers` / `transformers` and skip classical preprocessing | Transformer 流水线（反正你会用模型自带的分词器） | 使用 `tokenizers` / `transformers`，跳过经典预处理 |

### Les deux modes d'échec que personne ne vous prévient

La plupart des tutoriels enseignent les algorithmes et arrêtent. Deux choses mordent un vrai pipeline de pré-traitement, et ils ne sont presque jamais couverts.

> La plupart des cours sur l'algorithme sont arrêtés.

**Reproducibility drift.**NLTK et spaCy modifient le comportement de la jetonisation et du lemmatizer entre les versions.`['do', "n't"]`dans spaCy 2.x peut produire `["don't"]`Dans 3.x, votre modèle a été formé sur une distribution. l'inference fonctionne maintenant sur une autre. la précision dégrade tranquillement et personne ne sait pourquoi.`requirements.txt`Rédigez un test de régression de pré-traitement qui gelera la marquise attendue de 20 phrases d'échantillon.

> **可复现性漂移。**NLTK et spaCy dans différentes versions seront modifiés par les mots et les formes de mots.`['do', "n't"]`Le résultat, dans 3.x, peut se produire `["don't"]`◊ Votre modèle est formé sur une distribution, la raison est mise en œuvre sur une autre distribution.`requirements.txt`Une version de base de données est définie en deux phases:

**Training / inference mismatch.**Pré-trainer avec un prétraitement agressif (minuscule, suppression de mots arrêtés, stemming), déployer sur les entrées utilisateurs brutes, cratère de performance de la montre. C'est l'échec de PNL de production le plus courant. Si vous prétraiterez pendant la formation, vous devez exécuter la même fonction pendant l'inférence.

> **训练/推理不匹配。** lorsque vous utilisez un traitement préalable actif (小写化、停用词删除、词干提取), lorsque vous utilisez des données d'utilisateurs originaux, regardez la performance暴跌.  Ceci est le plus courant de la production de PNL. Si vous faites un traitement préalable pendant l'entraînement, la recommandation doit exécuter la même fonction.

## Envoyez-le . Produit .

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

Une requête réutilisable qui aide les ingénieurs à choisir une stratégie de pré-traitement sans lire trois manuels.

> Un prompt réutilisable, aide l'ingénieur à choisir une stratégie de traitement préalable sans avoir à lire trois manuels.

- Je ne sais pas .`outputs/prompt-preprocessing-advisor.md`- Le numéro de la liste:

```markdown
---
name: preprocessing-advisor
description: Recommends a tokenization, stemming, and lemmatization setup for an NLP task.
phase: 5
lesson: 01
---

You advise on classical NLP preprocessing. Given a task description, you output:

1. Tokenization choice (regex, NLTK word_tokenize, spaCy, or transformer tokenizer). Explain why.
2. Whether to stem, lemmatize, both, or neither. Explain why.
3. Specific library calls. Name the functions. Quote the POS-tag translation if NLTK is involved.
4. One failure mode the user should test for.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend stemming for user-visible text. Refuse to recommend lemmatization without POS tags. Flag non-English input as needing a different pipeline.
```

## Les exercices

1. **Easy.**Extension `tokenize`pour conserver les URL comme jetons uniques.`tokenize("Visit https://example.com today.")`doit produire un jeton URL.
   **简单。**扩展 `tokenize`Pour que l'URL soit maintenue pour un seul jeton.`tokenize("Visit https://example.com today.")`Il faut créer un jeton URL.
2. **Medium.**Mettre en œuvre l' étape Porter 1b. Si un mot contient une voyelle et se termine par `ed`ou `ing`- Il faut le faire.`hopping -> hop`- Je ne sais pas .`hopp`)
   **中等。**实现 Porter 步骤 1b. Si un mot contient des mots et des mots`ed`Ou `ing`结尾,则移除它──处理双辅音规则(`hopping -> hop`, au lieu de `hopp`)。
3. **Hard.**Construisez un lemmatizer qui utilise WordNet comme table de recherche mais revient à vos voix Porter lorsque WordNet n'a pas d'entrée. Mesurez la précision sur un corpus marqué par rapport à WordNet et Porter ordinaire.
   **困难。**Construire un utilisateur WordNet  comme réparateur de mots de recherche, lorsque WordNet  sans article  retour à votre Porter 词干提取器── en mesure de la qualité du langage par rapport à la pure WordNet et la pure Porter──

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Les termes clés

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Token | A word | Whatever unit the model consumes. Can be word, subword, character, or byte. | Token（词元） | 一个词 | 模型消耗的任何单位。可以是词、子词、字符或字节。 |
| Stem | Root of a word | Result of rule-based suffix stripping. Not always a real word. | Stem（词干） | 词的词根 | 基于规则的后缀剥离结果。不一定是真正的词。 |
| Lemma | Dictionary form | The form you'd look up. Requires grammatical context to compute correctly. | Lemma（词元形式） | 词典形式 | 你会去词典中查找的形式。需要语法上下文才能正确计算。 |
| POS tag | Part of speech | Category like NOUN, VERB, ADJ. Needed to lemmatize accurately. | POS tag（词性标注） | 词性 | 如 NOUN、VERB、ADJ 等类别。准确词形还原需要它。 |
| Morphology | Word shape rules | How a word changes form based on tense, number, case. Lemmatization depends on it. | Morphology（形态学） | 词形变化规则 | 词如何根据时态、数、格变化形式。词形还原依赖它。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.

## Encore une lecture

- [Porter, M. F. (1980). An algorithm for suffix stripping](https://tartarus.org/martin/PorterStemmer/def.txt) le papier original, cinq pages, toujours l'explication la plus claire. / 原始论文,五页,至今仍然是最清晰的解释──
- [spaCy 101 — linguistic features](https://spacy.io/usage/linguistic-features) comment un vrai pipeline est câblé. / 真实流水线是如何连接的──
- [NLTK book, chapter 3](https://www.nltk.org/book/ch03.html)Vous n'avez pas encore pensé à la situation.
