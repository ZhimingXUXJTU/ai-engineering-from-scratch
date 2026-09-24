# Résumé du texte

> Les systèmes extractifs vous disent ce que le document dit, les systèmes abstraits vous disent ce que l'auteur voulait dire, différentes tâches, différents pièges.
> Le système de production vous dit ce que l'auteur veut dire.

> **【中文解读】**抽取式 vs 生成式摘要──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation)
**Time:** ~75 minutes | **时间:** ~75 minutes


## Le problème , l' introduction du problème

Un article de 2000 mots se trouve dans votre flux. Vous avez besoin de 120 mots qui le capturent. Vous pouvez choisir les trois phrases les plus importantes de l'article (extractif) ou réécrire le contenu dans vos propres mots (abstractif).
> Un article de presse de 2000 mots apparaît dans votre flux d'information. Vous avez besoin de 120 mots pour le résumer. Vous pouvez choisir parmi les trois phrases les plus importantes ou réécrire votre propre contenu avec votre propre mot.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.


Le résumé extractif est un problème de classement.`k`Le résultat est toujours grammatical car il est levé littéralement.
> 抽取式摘要是一个排序问题──给每个句子打分,返回排名 `k`Le risque de défaut est généralement réparti dans l'ensemble du contenu de l'article.

La résumation abstractive est un problème de génération. Un transformateur produit un nouveau texte conditionné sur l'entrée. La sortie est fluide et compressive mais peut halluciner des faits qui n'étaient pas dans la source. Le risque est une fabrication confiante.
> Le résumé de la production est un problème de production. Le transformateur produit un nouveau texte en fonction de l'entrée.

Cette leçon les construit tous les deux, avec le mode d'échec de chacun.
> Les deux sont constitués par des modèles de défaillance.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


## Le concept de base.

![Extractive TextRank vs abstractive transformer](../assets/summarization.svg)
> ![抽取式 TextRank vs 生成式 Transformer](../assets/summarization.svg)

**Extractive.**Traitez l'article comme un graphique où les nœuds sont des phrases et les bords sont des similitudes.**TextRank**(Mihalcea et Tarau, 2004).
> **抽取式（Extractive）。**Le niveau de connexion de la phrase avec tout le reste est de la résumé.**TextRank**(Mihalcea et Tarau, 2004)

**Abstractive.**Fin-tune un transformateur encodeur-décodeur (BART, T5, Pegasus) sur les paires document-récapitulatif. À l'inférence, le modèle lit le document et génère le résumé jeton par jeton via l'attention croisée. Pegasus utilise en particulier un objectif de pré-entraînement de la phrase-écart qui le rend excellent pour la résumé sans beaucoup de fin-tune.
> **生成式（Abstractive）。**Dans le cadre de la formation, le modèle de formation est le plus souvent utilisé pour la formation de la formation professionnelle.

Évaluation avec **ROUGE**(Return-Oriented Understudy for Gisting Evaluation). ROUGE-1 et ROUGE-2 scores singramme et bigramme chevauchent. ROUGE-L scores la plus longue sous-sequence commune. Plus élevé est mieux mais 40 ROUGE-L est "bon" et 50 est "exceptionnel".`rouge-score`le colis.
> Utilisation **ROUGE**(Récommendable pour l'évaluation de la gisting) évaluation。ROUGE-1 和 ROUGE-2 评分一元组和二元组重叠。ROUGE-L 评分最长公共子序列。越高越好,但40 ROUGE-L 是"好",50 是"出色"──每篇论文都报告全部三个──使用`rouge-score`- Je suis désolé.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.


## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

```figure
summarize-collapse
```

## Faites-le

### Étape 1: TextRank (extractif)
> 两件事值得注意──相似度函数使用对数归结的词重叠,这是原始 TextRank的变体──TF-IDF 向量的余弦相似度也行──阻尼因子 0.85 和代次数是PageRank的默认值──

```python
import math
import re
from collections import Counter


def sentence_split(text):
    return re.split(r"(?<=[.!?])\s+", text.strip())


def similarity(s1, s2):
    w1 = Counter(s1.lower().split())
    w2 = Counter(s2.lower().split())
    intersection = sum((w1 & w2).values())
    denom = math.log(len(w1) + 1) + math.log(len(w2) + 1)
    if denom == 0:
        return 0.0
    return intersection / denom


def textrank(text, top_k=3, damping=0.85, iterations=50, epsilon=1e-4):
    sentences = sentence_split(text)
    n = len(sentences)
    if n <= top_k:
        return sentences

    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                sim[i][j] = similarity(sentences[i], sentences[j])

    scores = [1.0] * n
    for _ in range(iterations):
        new_scores = [1 - damping] * n
        for i in range(n):
            total_out = sum(sim[i]) or 1e-9
            for j in range(n):
                if sim[i][j] > 0:
                    new_scores[j] += damping * sim[i][j] / total_out * scores[i]
        if max(abs(s - ns) for s, ns in zip(scores, new_scores)) < epsilon:
            scores = new_scores
            break
        scores = new_scores

    ranked = sorted(range(n), key=lambda k: scores[k], reverse=True)[:top_k]
    ranked.sort()
    return [sentences[i] for i in ranked]
```

Deux choses qui valent la peine de nommer. La fonction de similitude utilise une superposition de mots normalisés par jour, qui est la variante originale de TextRank.
> BART-grand-CNN en ligne sur CNN/DailyMail 语料微调──开箱即用产生新闻风格摘要── pour les autres domaines, l'utilisation de Pegasus 检查点应对或在目标数据上微调──

### Étape 2: abstractif avec BART
> 始终使用词干提取──没有它, "running" 和 "run" 被视为不同的词,ROUGE 会低估──

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

article = """(long news article text)"""

summary = summarizer(article, max_length=120, min_length=60, do_sample=False)
print(summary[0]["summary_text"])
```

BART-grand-CNN est bien ajusté sur le corpus CNN/DailyMail. Il produit des résumés de style news hors boîte. Pour d'autres domaines (articles scientifiques, dialogue, juridique), utilisez le point de contrôle Pegasus correspondant ou bien ajustez vos données cibles.
> ROUGE a été l'indicateur principal de résumé pendant vingt ans, mais en 2026 il n'y a plus assez de base.

### Étape 3: Évaluation ROUGE
> - **BERTScore**(上下文嵌入相似度) a attiré l'attention en 2023, la plupart des articles de résumé sont maintenant publiés avec ROUGE un rapport.
- **BARTScore**L'évaluation sera réalisée en suivant les critères suivants:
- **MoverScore**(supérieure à la mise en place) atteint son sommet en 2025 dans le cadre du résumé, car il capture mieux la mise en œuvre du langage que le ROUGE.
- **FactCC**和**基于 QA 的事实性检查**En 2021-2023, il est très courant, maintenant habituellement.**G-Eval**(une sorte de GPT-4 提示链, utilisé en chaîne de pensées pour évaluer la connectivité, l'unanimité, la réaction et la relation)
- **G-Eval**Et les méthodes de commissaire de LLM similaires sont en accord avec les jugements humains à environ 80% dans le cadre de la bonne qualité des critères de notation.

```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
scores = scorer.score(reference_summary, generated_summary)
print({k: round(v.fmeasure, 3) for k, v in scores.items()})
```

Sans lui, "courir" et "courir" comptent comme des mots différents et ROUGE sous-compte.
> Résultats de la formation: Résultats de la formation et des résultats de la formation.

### Au-delà de ROUGE (2026 évaluation de résumé)
> Les résumés de production sont facilement générés par des phénomènes. Le risque de phénomène de résumé extrait est beaucoup plus faible, car la sortie est extraite de la source par mot, même si les phénomènes de production sont détachés du texte suivant, le temps passé ou l'ordre de référence, ils peuvent toujours être mal orientés.

ROUGE est la mesure de synthèse dominante depuis vingt ans et elle est insuffisante en elle-même en 2026.
> 需要命名的幻觉类型:

- **BERTScore**(semblance d'intégration contextuelle) a gagné en popularité jusqu'en 2023 et est maintenant rapporté aux côtés de ROUGE dans la plupart des documents de résumé.
- **BARTScore**traite l'évaluation comme une génération: note le résumé en fonction de la probabilité qu'un BART prétrainé l'attribue compte tenu de la source.
- **MoverScore**(Distances de la Terre sur les emplacements contextuels) a atteint la première place dans les benchmarks de résumé de 2025, car il capture mieux la chevauchement sémantique que ROUGE.
- **FactCC**et **QA-based faithfulness**étaient courantes en 2021-2023, maintenant souvent remplacées par **G-Eval**(une chaîne de réponse GPT-4 qui note la cohérence, la cohérence, la fluidité, la pertinence avec le raisonnement de la chaîne de pensée).
- **G-Eval**Les approches de la Juge LLM correspondent à la décision humaine dans ~80% des cas où les rubriques sont bien conçues.
> - **实体替换。**Il est aussi connu pour son travail.
- **数字漂移。**源说 "25.000"―摘要说"25 millions"―
- **极性翻转。**源说 "a rejeté l'offre"―摘要说 "a accepté l'offre"―
- **事实编造。**源没有提到CEO──摘要说CEO 批准──

Recommandation de production: rapport ROUGE-L pour comparaison antérieure, BERTScore pour superposition sémantique, G-Eval pour cohérence et factualité. Calibration par rapport à 50 à 100 résumés étiquetés par l'homme.
> Méthode d'évaluation efficace:

### Étape 4: le problème de la réalité
> - **FactCC。**Deuxième classe de la formation sur la relation entre les phrases source et résumé.
- **基于 QA 的事实性检查。**À QA 模型问源有答题──如果摘要支持不同的答案,标记──
- **实体级 F1。**Comparer les entités nommées dans le résumé avec les entités nommées dans le résumé.

Les résumés abstraits sont sujets à l'hallucination. Les résumés extractifs comportent un risque d'hallucination beaucoup plus faible parce que la sortie est supprimée littéralement de la source, bien qu'ils puissent toujours induire en erreur si les phrases sources sont décontextualisées, obsolètes ou citées hors ordre. C'est la seule raison pour laquelle les systèmes de production préfèrent encore les méthodes extractives pour le contenu adjacent à la conformité.
> Pour les informations, les médias, la loi, la finance, le retrait est un choix par défaut plus sûr.

Types d'hallucinations à nommer:

- **Entity swap.**La source dit "John Smith". Le résumé dit "John Brown".
- **Number drift.**La source dit 25 000 et le résumé dit 25 millions.
- **Polarity flip.**La source dit "rejeté l'offre". Le résumé dit "accepté l'offre".
- **Fact invention.**La source ne mentionne pas le PDG.

Les approches d'évaluation suivent:

- **FactCC.**Classificateur binaire formé sur l'implication entre la phrase source et la phrase sommaire. Prédit factuel/non factuel.
- **QA-based factuality.**Posez des questions à un modèle d'évaluation de la qualité dont les réponses figurent dans la source.
- **Entity-level F1.**Comparer les entités nommées dans la source par rapport au résumé.

Pour tout ce qui est fait par l'utilisateur où la factualité est importante (nouvelles, médicales, juridiques, financières), l'extractive est la solution la plus sûre.

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

La pile de 2026:
> 2026: année technique

| Use case | Recommended |
|---------|-------------|
| News, 3-5 sentence summary, English | `facebook/bart-large-cnn` |
| Scientific papers | `google/pegasus-pubmed` or a tuned T5 |
| Multi-document, long-form | Any LLM with 32k+ context, prompted |
| Dialog summarization | `philschmid/bart-large-cnn-samsum` |
| Extractive, low hallucination risk by construction | TextRank or `sumy`'s LSA / LexRank |
> Je vous recommande.
|---------|------|
| 新闻，3-5 句摘要，英语 | `facebook/bart-large-cnn` |
| 科学论文 | `google/pegasus-pubmed` 或微调的 T5 |
| 多文档，长文 | 任何 32k+ 上下文的 LLM，提示 |
| 对话摘要 | `philschmid/bart-large-cnn-samsum` |
| 抽取式，结构性低幻觉风险 | TextRank 或 `sumy` 的 LSA / LexRank |

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


Les LLM à long contexte battent souvent les modèles spécialisés en 2026 lorsque le calcul n'est pas une contrainte.
> En 2026 l'économie n'est pas limitée, le MLL est généralement plus élevé que le modèle spécialisé.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-summary-picker.md`- Le numéro de la liste:
> 保存为 `outputs/skill-summary-picker.md`- Le numéro de la liste:

```markdown
---
name: summary-picker
description: Pick extractive or abstractive, named library, factuality check.
version: 1.0.0
phase: 5
lesson: 12
tags: [nlp, summarization]
---

Given a task (document type, compliance requirement, length, compute budget), output:

1. Approach. Extractive or abstractive. Explain in one sentence why.
2. Starting model / library. Name it. `sumy.TextRankSummarizer`, `facebook/bart-large-cnn`, `google/pegasus-pubmed`, or an LLM prompt.
3. Evaluation plan. ROUGE-1, ROUGE-2, ROUGE-L (use rouge-score with stemming). Plus factuality check if abstractive.
4. One failure mode to probe. Entity swap is the most common in abstractive news summarization; flag samples where source entities do not appear in summary.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse abstractive summarization for medical, legal, financial, or regulated content without a factuality gate. Flag input over the model's context window as needing chunked map-reduce summarization (not just truncation).
```

## Les exercices

1. **Easy.**Exécutez TextRank sur 5 articles d'actualité. Comparer les 3 premières phrases à un résumé de référence. Mesurer ROUGE-L. Vous devriez voir 30-45 ROUGE-L sur les articles de style CNN/DailyMail.
2. **Medium.**Implémentation de la factualité au niveau de l'entité: extraire des entités nommées de la source et du résumé (spaCy), rappel calcul des entités sources en résumé et précision des entités résumées par rapport à la source.
3. **Hard.**Comparer BART-grand-CNN à un LLM (Claude ou GPT-4) sur 50 articles CNN/DailyMail. Rapporte ROUGE-L, factualité (par entité F1), et coût par résumé. Document où chaque gagnant.
> 1. **简单。**Dans le cadre de la rédaction de la série, le texte est classé parmi les trois premiers et les trois premiers.
2. **中等。**实现实体级事实性: de source et résumé entre提取命名实体(spaCy), de calcul de source de l'objet dans le résumé et de résumé de l'objet sur la source de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l'objet de l
3. **困难。**Dans le même temps, la Commission a également mis en place des programmes de recherche et de recherche sur les programmes de recherche et de recherche de la région de la France.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive | Pick sentences | Return sentences verbatim from the source. Never hallucinates. |
| Abstractive | Rewrite | Generate new text conditioned on source. Can hallucinate. |
| ROUGE | Summary metric | N-gram / LCS overlap between system output and reference. |
| TextRank | Graph-based extractive | PageRank over sentence similarity graph. |
| Factuality | Is it right | Whether summary claims are supported by the source. |
| Hallucination | Made-up content | Content in the summary that the source does not support. |
> ♪ Les termes que les gens disent souvent ♪ ♪ Le sens réel ♪
|------|-----------|---------|
| 抽取式 | 选取句子 | 从源中逐字返回句子。不会幻觉。 |
| 生成式 | 重写 | 根据源生成新文本。可能幻觉。 |
| ROUGE | 摘要指标 | 系统输出与参考之间的 n-gram / LCS 重叠。 |
| TextRank | 基于图的抽取式 | 句子相似度图上的 PageRank。 |
| 事实性 | 对不对 | 摘要声明是否被源支持。 |
| 幻觉 | 编造内容 | 摘要中源不支持的内容。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) le papier canonique extractif.
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461) le papier BART.
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777) Pegasus et l'objectif de la phrase à écart.
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/) PAPE ROUGE.
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) le document de paysage de la réalité.
> - [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) 抽取式经典论文──
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461) BART 论文。
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777) Pegasus 和间隔句子目标──
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/) ROUGE 论文。
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) Facts性全景论文──
