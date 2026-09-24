# PNL multilingue PNL multilingue

> Un modèle, plus de 100 langues, zéro données de formation pour la plupart d'entre elles. Le transfert interlinguiste est le miracle pratique des années 2020.
> Un modèle, plus de 100 langues, la plupart des langues sont en train de s'installer.

> **【中文解读】**Les différents types de traitement sont les suivants:

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 04 (GloVe, FastText, Subword), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 04（GloVe、FastText、子词），Phase 5 · 11（机器翻译）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

L'anglais a des milliards d'exemples étiquetés. L'ourdou a des milliers. La maithili n'a presque aucun. Tout système pratique de PNL qui sert un public mondial doit travailler sur la longue queue des langues où les données de formation spécifiques à des tâches n'existent pas.

> Il y a des milliards de modèles de balises en anglais. Il y a des milliers en urdu. Il y a presque aucun langage en anglais.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

Les modèles multilingues résolvent cela en formant un modèle sur plusieurs langues simultanément. La représentation partagée permet au modèle de transférer les compétences acquises dans les langues à ressources élevées à celles à ressources faibles. D'accord avec l'analyse anglaise des sentiments, il produit des prédictions surprenantes sur l'urdu. C'est un transfert interlinguel sans décalage, et il a remodelé la façon dont la PNL se transmet dans le monde.

> Le modèle multilingue est utilisé pour former un modèle dans de nombreuses langues en même temps pour résoudre ce problème. Le partage indique que le modèle permettra à des compétences acquises à haute source de langue de passer à des compétences à faible source. Dans l'analyse émotionnelle anglaise, le modèle est ouvert à une prédiction étonnante de bonnes émotions pour l'Urdu.

Cette leçon mentionne les compromis, les modèles canoniques et la seule décision qui incite les équipes nouvelles à travailler en plusieurs langues: choisir une langue source pour le transfert.

> Ce cours a été intitulé "Pétenance"",Modèle classique", ainsi que "Problem multilingual工作新手团队的决策:选择迁移的源语言").

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

![Cross-lingual transfer via shared multilingual embedding space](../assets/multilingual.svg)

**Shared vocabulary.**Les modèles multilingues utilisent un jeton SentencePiece ou WordPiece formé sur le texte de toutes les langues cibles. Le vocabulaire est partagé: la même unité de sous-parts représente le même morphème dans toutes les langues apparentées. `anti-`en anglais et en italien, on obtient le même jeton.

> **共享词表。**Modèle multilingue utilisé dans tous les textes de langue cible pour la formation de la phrasePiece ou WordPiece 分词器──词表是共享的: identiques sous-parts unités représentent les mêmes语素──英语和意大利语的`anti-`Obtenir le même token.

**Shared representation.**Un transformateur prétrainé à la modélisation du langage masqué dans de nombreuses langues apprend que des phrases sémantiquement similaires dans différentes langues produisent des états cachés similaires. mBERT, XLM-R et NLLB le montrent tous.

> **共享表示。**Le transformer apprend à produire des phrases similaires dans différentes langues. Les phrases similaires sont en même temps dans un état caché.

**Zero-shot transfer.**La définition de la langue de référence est la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la définition de la langue de référence, la langue de référence, la langue de référence, la langue de référence, la langue de référence.

> **零样本迁移。**Dans une langue (habituellement anglais), les étiquettes sont utilisées dans des modèles de données.

**Few-shot fine-tuning.**Ajouter 100 à 500 exemples étiquetés dans la langue cible. La précision saute à 95 à 98% de la ligne de base anglaise sur les tâches de classification. C'est le levier le plus rentable dans la PNL multilingue.

> **少样本微调。**Dans les langues cibles, on ajoute 100 à 500 échantillons de marqueurs. Le taux de précision dans les tâches de catégorie monte à 95 à 98% de la base anglaise.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Les modèles .

| Model / 模型 | Year / 年份 | Coverage / 覆盖 | Notes / 说明 |
|-------|------|----------|-------|
| mBERT | 2018 | 104 languages / 104 种语言 | Trained on Wikipedia. First practical multilingual LM. Weak on low-resource. / 在 Wikipedia 上训练。首个实用多语言 LM。低资源语言较弱。 |
| XLM-R | 2019 | 100 languages / 100 种语言 | Trained on CommonCrawl. Sets the cross-lingual baseline. / 在 CommonCrawl 上训练。设定跨语言基线。 |
| XLM-V | 2023 | 100 languages / 100 种语言 | XLM-R with 1M-token vocabulary. Better on low-resource. / XLM-R 配 1M token 词表。低资源更好。 |
| mT5 | 2020 | 101 languages / 101 种语言 | T5 architecture for multilingual generation. / T5 架构用于多语言生成。 |
| NLLB-200 | 2022 | 200 languages / 200 种语言 | Meta's translation model; includes 55 low-resource languages. / Meta 翻译模型；含 55 种低资源语言。 |
| BLOOM | 2022 | 46 languages + 13 programming / 46 种语言 + 13 种编程语言 | Open 176B LLM trained multilingually. / 开源 176B 多语言 LLM。 |
| Aya-23 | 2024 | 23 languages / 23 种语言 | Cohere's multilingual LLM. Strong on Arabic, Hindi, Swahili. / Cohere 多语言 LLM。阿拉伯语、印地语、斯瓦希里语强。 |

Choisissez par cas d'utilisation. La classification fonctionne bien avec la base XLM-R en tant que défaut sain. Les tâches de génération nécessitent mT5 ou NLLB selon la traduction et la génération ouverte.

> 按用例选择──分类任务以 XLM-R-base 作为合理默认──生成任务根据翻译对开放生成选择 mT5 或 NLLB──LLM 风格工作配合 Aya-23 或 Claude 使用显式多语言提示──

## La décision de la langue source (2026 recherche)

La plupart des équipes utilisent l'anglais comme source de réglage.

> La plupart des équipes reconnaissent que l'anglais est un langage de référence.

La similitude linguistique prédit la qualité de transfert mieux que la taille du corpus brut. Pour les cibles slaves, l'allemand ou le russe battent souvent l'anglais. Pour les cibles indiennes, l'hindi bat souvent l'anglais.**qWALS**La métrique de similitude (2026, basée sur les caractéristiques de l'Atlas mondial des structures linguistiques) quantifie cela. **LANGRANK**(Lin et al., ACL 2019) est une méthode distincte et antérieure qui classe les langues candidates à la source à partir d'une combinaison de similitude linguistique, de taille de corpus et de connexion génétique.

> 语言相似性比原始语料大小更好地预测迁移质量──对斯拉夫语目标,德语或俄语通常胜英语──对印度语目标,印度语通常胜英语──**qWALS**La même quantité de quantité de la même quantité de quantité de la même quantité de quantité de quantité de la même quantité de quantité de quantité de quantité de quantité de quantité de la même quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité de quantité**LANGRANK**(Lin 等,ACL 2019) de la linguistique similaire, du langage et des relations génétiques.

Règle pratique: si votre langue cible a un parent typiquement proche de ressources élevées, essayez d'abord de l'ajuster, puis comparez-le à l'anglais.

> Règles pratiques: si votre langue cible est classé comme étant proche de la langue de haute source, essayez d'abord de la moduler, puis de la comparer à l'anglais.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
n5-crosslingual-bridge
```

## Faites-le

### Étape 1: classification interlinguistique à zéro

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli")
model = AutoModelForSequenceClassification.from_pretrained("joeddav/xlm-roberta-large-xnli")


def classify(text, candidate_labels, hypothesis_template="This text is about {}."):
    scores = {}
    for label in candidate_labels:
        hypothesis = hypothesis_template.format(label)
        inputs = tok(text, hypothesis, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits[0]
        entail_score = torch.softmax(logits, dim=-1)[2].item()
        scores[label] = entail_score
    return dict(sorted(scores.items(), key=lambda x: -x[1]))


print(classify("I love this product!", ["positive", "negative", "neutral"]))
print(classify("मुझे यह उत्पाद पसंद है!", ["positive", "negative", "neutral"]))
print(classify("J'adore ce produit !", ["positive", "negative", "neutral"]))
```

Un modèle, trois langues, la même API. XLM-R formé sur NLI transfère bien les données à la classification via le truc de l'enclusion.

> Un modèle, trois langues, la même API.

### Étape 2: espace d'intégration multilingue

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

pairs = [
    ("The cat is sleeping.", "Le chat dort."),
    ("The cat is sleeping.", "El gato está durmiendo."),
    ("The cat is sleeping.", "Die Katze schläft."),
    ("The cat is sleeping.", "The dog is barking."),
]

for eng, other in pairs:
    emb_eng = model.encode([eng], normalize_embeddings=True)[0]
    emb_other = model.encode([other], normalize_embeddings=True)[0]
    sim = float(np.dot(emb_eng, emb_other))
    print(f"  {eng!r} <-> {other!r}: cos={sim:.3f}")
```

Les traductions se rapprochent dans l'espace d'embedding. Une phrase anglaise différente se rapproche davantage. C'est ce qui rend la récupération, le regroupement et la similitude interlinguistes fonctionnent.

> 翻译在嵌入空间中距离很近. 不同英语句子距离更远. 译在嵌入空间中距离很近.

### Étape 3: stratégie de réglage des points de vue

```python
from transformers import TrainingArguments, Trainer
from datasets import Dataset


def few_shot_finetune(base_model, base_tokenizer, examples):
    ds = Dataset.from_list(examples)

    def tokenize_fn(ex):
        out = base_tokenizer(ex["text"], truncation=True, max_length=128)
        out["labels"] = ex["label"]
        return out

    ds = ds.map(tokenize_fn)
    args = TrainingArguments(
        output_dir="out",
        per_device_train_batch_size=8,
        num_train_epochs=5,
        learning_rate=2e-5,
        save_strategy="no",
    )
    trainer = Trainer(model=base_model, args=args, train_dataset=ds)
    trainer.train()
    return base_model
```

Pour 100 à 500 exemples de langues cibles, `num_train_epochs=5`et `learning_rate=2e-5`Les taux d'apprentissage plus élevés font que l'alignement multilingue s'effondre et vous obtenez un modèle en anglais seulement.

>  Pour 100 à 500 个目标语言样本,`num_train_epochs=5`et `learning_rate=2e-5`Un taux d'apprentissage plus élevé entraînera une chute de plusieurs langues, vous obtenez un modèle uniquement en anglais.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Une évaluation qui fonctionne vraiment.

- **Per-language accuracy on held-out sets.**L'agrégat cache la longue queue.
  **每种语言在留出集上的准确率。**Ne pas se regrouper.
- **Benchmark against monolingual baseline.**Pour les langues avec suffisamment de données, un modèle monolingual entraîné à partir de zéro peut parfois dépasser celui multilingue.
  **与单语基线比较。**Pour les langues qui ont suffisamment de données, le modèle monolinguistique de la formation est parfois supérieur à celui de plusieurs langues.
- **Entity-level tests.**Les modèles multilingues ont souvent une faible tokenization pour les scripts éloignés du latin.
  **实体级测试。**Les noms de plusieurs langues sont généralement plus faibles que ceux de la littérature éloignée du latin.
- **Cross-lingual consistency.**Le même sens dans deux langues devrait produire la même prédiction.
  **跨语言一致性。**两种语言中相同含义应产生相同预测――测量差距――

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

## Utilisez-le avec le cadre de réalisation

La pile de 2026:

> 2026:

| Task / 任务 | Recommended / 推荐 |
|-----|-------------|
| Classification, 100 languages / 分类，100 种语言 | XLM-R-base (~270M) fine-tuned / 微调 |
| Zero-shot text classification / 零样本文本分类 | `joeddav/xlm-roberta-large-xnli` |
| Multilingual sentence embeddings / 多语言句子嵌入 | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Translation, 200 languages / 翻译，200 种语言 | `facebook/nllb-200-distilled-600M` |
| Generative multilingual / 生成式多语言 | Claude, GPT-4, Aya-23, mT5-XXL |
| Low-resource language NLP / 低资源语言 NLP | XLM-V or domain-specific fine-tune / XLM-V 或领域微调 |

Le budget est toujours pour la mise à jour de la langue cible si les performances comptent.

> Si les performances sont importantes, le budget de la langue cible est toujours réduit.

### La taxe de tokenization

Les modèles multilingues partagent un tokenizer dans toutes leurs langues. Ce vocabulaire est formé sur un corpus dominé par l'anglais, le français, l'espagnol, le chinois, l'allemand. Pour toute langue en dehors de l'ensemble dominant, trois taxes se composent silencieusement:

> Les différents modèles linguistiques sont utilisés dans tous les langages. Ils sont utilisés dans des formations de langage en anglais, français, espagnol, chinois, allemand.

- **Fertility tax.**Un texte en langue à faible ressource se transforme en beaucoup plus de jetons par mot que l'anglais. Une phrase en hindi peut avoir besoin de 3-5 fois les jetons d'une phrase anglaise équivalente.
  **繁殖税。**低资源语言文本每词分词成英语比多多的代币――un indi语句可能需要等价英语句的3-5倍的代币――
- **Variant recovery tax.**Chaque erreur de frappe, variante diacritique, déséquilibre de normalisation Unicode ou variation de cas devient une séquence sans rapport de démarrage à froid dans l'espace d'intégration.
  **变体恢复税。**Chaque erreur d'écriture, changement de son, changement de symbole, changement de code, changement de taille, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code, changement de code.
- **Capacity spillover tax.**Les taxes 1 et 2 consomment des positions de contexte, de la profondeur de couche et des dimensions d'embedding. Ce qui reste pour le raisonnement réel est systématiquement plus petit.
  **容量溢出税。**La consommation de la position, de la profondeur et de la dimension de l'implémentation est réduite à un niveau plus petit.

Le symptôme pratique: votre modèle s'entraîne normalement en hindi, la courbe de perte semble correcte, la perplexité d'évaluation semble raisonnable et les résultats de production sont subtilement erronés. **You cannot data-scale your way out of a broken tokenizer.**

> Symptômes réels: modèle en hindi entraîne normal, la perte de courbe correcte, évaluer la confusion raisonnable, mais produire et produire des résultats délicats.**你无法通过数据扩展来修复损坏的分词器。**

Atténuations: choisissez un tokenizer avec une bonne couverture pour votre langue cible; vérifiez la fertilité de la tokenification sur le texte cible retenu; utilisez le bac à niveau de octets pour des scripts vraiment longs.

> 缓解措施: sélectionner un bon分词器 pour couvrir une langue cible; répéter le taux de reproduction des mots dans un texte cible; utiliser un niveau de caractères pour écrire un vrai langage long.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-multilingual-picker.md`- Le numéro de la liste:

> 保存为 `outputs/skill-multilingual-picker.md`- Le numéro de la liste:

```markdown
---
name: multilingual-picker
description: Pick source language, target model, and evaluation plan for a multilingual NLP task.
version: 1.0.0
phase: 5
lesson: 18
tags: [nlp, multilingual, cross-lingual]
---

Given requirements (target languages, task type, available labeled data per language), output:

1. Source language for fine-tuning. Default English; check LANGRANK or qWALS if target language has a typologically close high-resource language.
2. Base model. XLM-R (classification), mT5 (generation), NLLB (translation), Aya-23 (generative LLM).
3. Few-shot budget. Start with 100-500 target-language examples if available.
4. Evaluation plan. Per-language accuracy, cross-lingual consistency, entity-level F1 on non-Latin scripts.

Refuse to ship a multilingual model without per-language evaluation. Flag scripts with low tokenization coverage as needing byte-fallback.
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les exercices

1. **Easy.**Exécutez le pipeline de classification à tir zéro sur 10 phrases par langue en anglais, français, hindi et arabe.
   **简单。**Dans les langues anglaise, française, indienne et arabe, le taux de dépistage des données est de 10 pourcentage par langue.
2. **Medium.**Utilisation `paraphrase-multilingual-MiniLM-L12-v2`Pour obtenir des informations sur les données, il est nécessaire de créer un retriever multilingue sur un petit corpus de langues mixtes.
   **中等。**构建跨语言检索器──用英语查询,检索任何语言的文档──测量回忆@5──
3. **Hard.**Comparer la mise en forme de la langue anglaise et de la langue hindi pour une tâche de classification en hindi. Rapporte quelle source produit une meilleure précision en hindi.
   **困难。**Comparer les sources anglaises et indiennes à l'effet des tâches de classification de la langue indienne.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Les termes clés

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Multilingual model（多语言模型） | One model, many languages / 一个模型多种语言 | Shared vocabulary and parameters across languages. / 跨语言共享词表和参数。 |
| Cross-lingual transfer（跨语言迁移） | Train on one, run on another / 训练一种，运行另一种 | Fine-tune on source, evaluate on target without target labels. / 在源语言微调，在目标语言评估。 |
| Zero-shot（零样本） | No target labels / 无目标标签 | Transfer without target-language fine-tuning. / 无目标语言微调的迁移。 |
| Few-shot（少样本） | Small target labels / 少量目标标签 | 100-500 target-language examples for fine-tuning. / 100-500 个目标语言样本。 |
| mBERT | First multilingual LM / 首个多语言 LM | 104-language BERT on Wikipedia. / 104 语言 BERT。 |
| XLM-R | Cross-lingual baseline / 跨语言基线 | 100-language RoBERTa on CommonCrawl. / 100 语言 RoBERTa。 |
| NLLB | 200-language MT / 200 语言 MT | No Language Left Behind. 55 low-resource languages. / 不让任何语言掉队。55 种低资源语言。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.

## Encore une lecture

- [Conneau et al. (2019). XLM-R](https://arxiv.org/abs/1911.02116) le document XLM-R. / XLM-R 论文。
- [Pires et al. (2019). How Multilingual is Multilingual BERT?](https://arxiv.org/abs/1906.01502) l'analyse des transferts translinguels. / 跨语言迁移分析。
- [Costa-jussà et al. (2022). No Language Left Behind](https://arxiv.org/abs/2207.04672) NLLB-200. / NLLB-200 论文。
- [Üstün et al. (2024). Aya Model](https://arxiv.org/abs/2402.07827) LLM multilingue de Cohere. / Cohere 多语言 LLM。
- [Language Similarity Predicts Cross-Lingual Transfer (2026)](https://www.mdpi.com/2504-4990/8/3/65) QWALS / LANGRANK. / qWALS / LANGRANK 源语言论文。
