# Systèmes de réponse aux questions.

> Trois systèmes ont façonné l'AQ moderne. Extractive trouvé des spans. récupération augmentée les a mis à terre dans les documents. Génératif produit des réponses. chaque assistant d'IA moderne est un mélange des trois.
> Les trois systèmes ont façonné la réponse moderne à la question. Le processus de tirage au sort de l'IA est un mélange de trois personnes.

> **【中文解读】**De l'information à la production de questions à la réponse.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 11 (Machine Translation), Phase 5 · 10 (Attention Mechanism) | **前置知识:** Phase 5 · 11 (Machine Translation), Phase 5 · 10 (Attention Mechanism)
**Time:** ~75 minutes | **时间:** ~75 minutes


## Le problème , l' introduction du problème

Un utilisateur tape "Quand a été lancé le premier iPhone?" et s'attend à "29 juin 2007". Pas "L'histoire d'Apple est longue et variée". Pas "2007" assis en isolement sans phrase. Une réponse directe, basée sur la terre, correcte.
> User输入 "Quand a été lancé le premier iPhone?"并期望得到 "29 juin 2007."──不是"Apple's history is long and varied".──不是孤立的"2007" 没有句子上下文──一个直接、有据可依、正确的答案──

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.


Trois architectures ont dominé l'AQ au cours de la dernière décennie.
> Au cours de la dernière décennie, trois architectures ont dominé la question et la réponse.

- **Extractive QA.**En raison d'une question et d'un passage qui contient la réponse, trouvez les indices de début et de fin de la période de réponse dans le passage.
- **Open-domain QA.**Le passage n'est pas donné. Retrouvez le passage pertinent d'abord, puis extraire ou générer une réponse.
- **Generative / Closed-book QA.**Un modèle de langage de taille moyenne répond à sa mémoire paramétrique, sans récupération, le plus rapide à l'inférence, le moins fiable sur les faits.
> - **抽取式问答（Extractive QA）。**给定一个问题和已知含答案的段落, trouver la réponse dans le début et la fin des paragraphes 索引.
- **开放域问答（Open-domain QA）。**段落未给定──先检查相关段落,然后抽取或生成答案── c'est la pierre angulaire de chaque ligne de RAG 流水――
- **生成式/闭卷问答（Generative / Closed-book QA）。**Le modèle de la langue est le plus rapide, le plus faible de la fiabilité.

La tendance en 2026 est hybride: récupérer les meilleurs passages, puis demander un modèle génératif pour répondre en se basant sur ces passages.
> Les tendances de l'année 2026 sont mixtes: recherchez les meilleurs quelques paragraphes, puis proposez de générer des modèles sur la base de ces paragraphes pour répondre à ces questions.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![QA architectures: extractive, retrieval-augmented, generative](../assets/qa.svg)
> ![问答架构：抽取式、检索增强、生成式](../assets/qa.svg)

**Extractive.**Encode la question et le passage avec un transformateur (famille BERT). Formez deux têtes qui prédisent les indices de début et de fin des jetons de la réponse. La perte est l'entropie croisée sur les positions valides. La sortie est une distance du passage.
> **抽取式。**Avec le transformateur ([[BERT 系列]]) avec le code problème et le passage. Entrenage deux prédiction réponse de début et fin de l'indexation des jetons.

**Retrieval-augmented (RAG).**Deux étapes, un retriever trouve le haut...`k`Les résultats de la recherche de l'analyse de la réaction de la réaction de l'analyse de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de la réaction de
> **检索增强（RAG）。**Deux étapes. Premièrement, le référentiel de la bibliothèque de la langue trouve le haut...`k`段落──二,阅读器(抽取式或生成式) utilise ces段落产生答案──检索器-阅读器分离允许各自独立训练和评估──现代RAG

**Generative.**Un LLM (GPT, Claude, Llama) qui ne décode que les réponses à partir de poids appris. Pas de étape de récupération. Excellent sur la connaissance commune, catastrophique sur des faits rares ou récents. Le taux d'hallucination est inversement corrélateur avec la fréquence des faits dans les données de pré-entraînement.
> **生成式。**Il s'agit d'un programme de formation de formation professionnelle qui consiste à étudier les techniques de formation et de formation de base.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.


## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

```figure
qa-span
```

## Faites-le

### Étape 1: QA extractif avec un modèle prétrainé
> `deepset/roberta-base-squad2`Dans le cadre de la formation SQuAD 2.0, il y a des questions à ne pas répondre.`question-answering`流水线返回最高分分的片段, même si le nombre de空分胜出它不自动返回空答案── 为了 obtenir un comportement " sans réponse " évident, 流水线调用中传进`handle_impossible_answer=True`:Reflux de l'eau dans le vide surpasse le nombre de fragments de l'air.`score`Je suis en train de vous dire:

```python
from transformers import pipeline

qa = pipeline("question-answering", model="deepset/roberta-base-squad2")

passage = (
    "Apple Inc. released the first iPhone on June 29, 2007. "
    "The device was announced by Steve Jobs at Macworld in January 2007."
)
question = "When was the first iPhone released?"

answer = qa(question=question, context=passage)
print(answer)
```

```python
{'score': 0.98, 'start': 57, 'end': 70, 'answer': 'June 29, 2007'}
```

`deepset/roberta-base-squad2`Le programme de formation est basé sur le SQuAD 2.0, qui comprend des questions à laquelle il n'y a pas de réponse.`question-answering`Le pipeline renvoie la période de scoring la plus élevée même lorsque le score nul du modèle gagne  il ne * pas * renvoie automatiquement une réponse vide. Pour obtenir un comportement explicite " pas de réponse ", passez `handle_impossible_answer=True`à l'appel de pipeline: le pipeline ne renvoie une réponse vide que lorsque le score nul dépasse chaque score de span.`score`Le champ de tous les deux.
> 两段流水线──密检索器(Sentence-BERT) à travers la similitude de la langue pour trouver des paragraphes associés──抽取式阅读器(RoBERTa-SquAD) à partir du haut de la même section 提取答案片段── s'applique à la petite bibliothèque de langages── pour les millions de documents de langue, à l'aide de FAISS ou de la bibliothèque de données de volume──

### Étape 2: un pipeline augmenté en récupération (boîtier)
> Le modèle de suggestion est important. Le modèle de suggestion est clairement indiqué en fonction des réponses et des réponses et des réponses de "je ne sais pas" lorsque les réponses sont insuffisantes.

```python
from sentence_transformers import SentenceTransformer
import numpy as np

encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

corpus = [
    "Apple Inc. released the first iPhone on June 29, 2007.",
    "Macworld 2007 featured the iPhone announcement by Steve Jobs.",
    "Android launched in 2008 as Google's mobile operating system.",
    "The first iPod was released in 2001.",
]
corpus_embeddings = encoder.encode(corpus, normalize_embeddings=True)


def retrieve(question, top_k=2):
    q_emb = encoder.encode([question], normalize_embeddings=True)
    sims = (corpus_embeddings @ q_emb.T).squeeze()
    order = np.argsort(-sims)[:top_k]
    return [corpus[i] for i in order]


def answer(question):
    passages = retrieve(question, top_k=2)
    combined = " ".join(passages)
    return qa(question=question, context=combined)


print(answer("When was the first iPhone released?"))
```

Le système de récupération dense (Sentence-BERT) trouve des passages pertinents par similitude sémantique. Le lecteur extractif (RoBERTa-SQuAD) tire la durée de réponse des passages supérieurs combinés.
> SQUAD Utilisation**精确匹配（Exact Match, EM）**et **token 级 F1**◦ EM est un accord strict après la réunification ([[小写、除标点、除冠词) 预测要么精确匹配,要么得 0♦ F1 在预测和参考的代币重叠上计算,给部分分──两者都低估释义:"29 juin 2007" vs "29 juin 2007" "通常得 0 EM(序数词破坏归化) mais encore obtenir un F1 considérable de la réunification des dons.

### Étape 3: génératif avec RAG
> 对于生产问答:

```python
def rag_generate(question, llm):
    passages = retrieve(question, top_k=3)
    prompt = f"""Context:
{chr(10).join('- ' + p for p in passages)}

Question: {question}

Answer using only the context above. If the context does not contain the answer, say "I don't know."
"""
    return llm(prompt)
```

Le motif prompt compte. Dire explicitement au modèle de se poser dans le contexte et de retourner "je ne sais pas" lorsque le contexte est insuffisant réduit les taux d'hallucination de 40-60% par rapport à la provocation naïve.
> - **答案准确率**(LLM 评判或人工评判,因为指标不捕获语义等价)
- **引用准确率。**引用的段落是真的支持答案吗?Utiliser la correspondance des caractères entre la génération de citations et la recherche de段落 est facile à vérifier automatiquement.
- **拒绝校准。**Lorsque la réponse n'est pas dans le processus de recherche, le système dit-il correctement "je ne sais pas"?
- **检索召回率。**Avant d'évaluer le lecteur, le lecteur de mesure sera-t-il correctement placé en haut...`k`❖ Les épisodes manquants ne peuvent être réparés.

### Étape 4: évaluation qui reflète le monde réel
> `RAGAS`专为RAG 系统构建,是2026年发布默认选择――它在不需要黄金参考的情况下从四维度评分:

Utilisation de la SQUAD **Exact Match (EM)**et **token-level F1**- Je suis désolé . EM est un match strict après normalisation (case minuscule, ponctuation de strip, suppression d'articles)  soit la prédiction correspond exactement ou il marque 0. F1 est calculé sur la superposition des symboles entre la prédiction et la référence et donne un crédit partiel. Les deux parafractions sous-crédites: "29 juin 2007" vs "29 juin 2007" obtient généralement 0 EM (la normalisation des ruptures ordinaires), mais gagne toujours une F1 substantielle grâce à des jetons se chevauchant.
> - **忠实度（Faithfulness）。**Chaque déclaration de la réponse provient-elle du résultat de la recherche?
- **答案相关性。**答案是否回应了问题? 答案生成假设问题并与真题相比较量化通过答案生成假设问题并与真题相比较量化而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量而测量
- **上下文精确率。**Dans le bloc de recherche, combien sont réellement liés ?
- **上下文召回率。**Le référencement contient-il toutes les informations dont il a besoin ?

Pour la production QA:
>  évaluation sans référence  évaluation en temps réel sur le flux de production  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation en temps réel  évaluation  évaluation en temps réel  évaluation  évaluation en temps réel  évaluation  évaluation  évaluation  évaluation  évaluation  évaluation  évaluation  évaluation  évaluation 

- **Answer accuracy**(Juge par la LLM ou par l'homme, puisque les mesures ne capturent pas l'équivalence sémantique).
- **Citation accuracy.**Le passage cité soutient-il réellement la réponse ?
- **Refusal calibration.**Lorsque la réponse n'est pas dans les passages récupérés, le système dit-il correctement " Je ne sais pas "? Mesurer le taux de confiance fausse.
- **Retrieval recall.**Avant d'évaluer le lecteur, mesurez si le retriever obtient le bon passage dans le haut-`k`Un lecteur ne peut pas réparer un passage manquant.
> `pip install ragas`◊ Connectez votre référencement + 阅读器── chaque référencement obtient quatre étiquettes──

### RAGAS: le cadre d'évaluation de la production de 2026

`RAGAS`Il est conçu spécifiquement pour les systèmes RAG et est le modèle de livraison par défaut en 2026.

- **Faithfulness.**Chaque affirmation de la réponse provient du contexte récupéré? Mesurée par l'implication basée sur les NLI.
- **Answer relevance.**La réponse répond-elle à la question? Mesurée en générant des questions hypothétiques à partir de la réponse et en comparant à la question réelle.
- **Context precision.**Parmi les morceaux récupérés, quelle fraction était réellement pertinente ?
- **Context recall.**Le jeu récupéré contient-il toutes les informations nécessaires ?

Le score sans référence vous permet d'évaluer le trafic de production en direct sans obtenir de réponses en or.

`pip install ragas`- Connectez votre retriever + lecteur.

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

La pile de 2026.
> 2026 année de technologie

| Use case | Recommended |
|---------|-------------|
| Given passage, find answer span | `deepset/roberta-base-squad2` |
| Over a fixed corpus, closed-book not acceptable | RAG: dense retriever + LLM reader |
| Real-time over a document store | RAG with hybrid (BM25 + dense) retriever + reranker (lesson 14) |
| Conversational QA (follow-up questions) | LLM with conversation history + RAG on each turn |
| Highly factual, regulated domains | Extractive over an authoritative corpus; never generative alone |
> Je vous recommande.
|---------|------|
| 给定段落，找答案片段 | `deepset/roberta-base-squad2` |
| 固定语料上，闭卷不可接受 | RAG：稠密检索器 + LLM 阅读器 |
| 实时文档存储 | RAG 配混合（BM25 + 稠密）检索器 + 重排序器（第 14 课） |
| 对话式问答（追问） | 带对话历史的 LLM + 每轮 RAG |
| 高度事实性、受监管领域 | 在权威语料上的抽取式；永远不要单独用生成式 |

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


L'AQ extractive est démodé en 2026 car RAG avec LLM traite plus de cas. Il est toujours disponible dans des contextes où une citation littérale est requise: recherche juridique, conformité réglementaire, outils d'audit.
> La question de l'extraction de questions n'est plus courante en 2026, car le RAG de la LLM traite plus de situations.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-qa-architect.md`- Le numéro de la liste:
> 保存为 `outputs/skill-qa-architect.md`- Le numéro de la liste:

```markdown
---
name: qa-architect
description: Choose QA architecture, retrieval strategy, and evaluation plan.
version: 1.0.0
phase: 5
lesson: 13
tags: [nlp, qa, rag]
---

Given requirements (corpus size, question type, factuality constraint, latency budget), output:

1. Architecture. Extractive, RAG with extractive reader, RAG with generative reader, or closed-book LLM. One-sentence reason.
2. Retriever. None, BM25, dense (name the encoder), or hybrid.
3. Reader. SQuAD-tuned model, LLM by name, or "domain-fine-tuned DistilBERT."
4. Evaluation. EM + F1 for extractive benchmarks; answer accuracy + citation accuracy + refusal calibration for production. Name what you are measuring and how you are measuring it.

Refuse closed-book LLM answers for regulatory or compliance-sensitive questions. Refuse any QA system without a retrieval-recall baseline (you cannot evaluate the reader without knowing the retriever surfaced the right passage). Flag questions that require multi-hop reasoning as needing specialized multi-hop retrievers like HotpotQA-trained systems.
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──


## Les exercices

1. **Easy.**Mettez le pipeline extractif SQuAD en haut sur 10 passages de Wikipédia. 10 questions à la main. Mesurez la fréquence avec laquelle la réponse est correcte. Vous devriez voir 7-9 correct si les passages et les questions sont propres.
2. **Medium.**Ajoutez un classifiateur de refus. Lorsque le score de récupération supérieur est inférieur à un seuil (disons 0,3 cosines), retournez "Je ne sais pas" au lieu d'appeler le lecteur.
3. **Hard.**Construisez un pipeline RAG sur un corpus de 10 000 documents de votre choix. Implémenter la récupération hybride (BM25 + dense) avec la fusion RRF (voir leçon 14). Mesurer la précision des réponses avec et sans l'étape hybride. Document qui les types de questions bénéficient le plus.
> 1. **简单。**Dans le cadre de la mise en place de la section de l'article, vous pouvez voir les résultats de la section de la section de la section de la section de la section de la section de la section de l'article.
2. **中等。**添加拒绝分类器──当最高检索分数低于值(如0.3余弦) 当,返回"I don't know"而不是调用阅读器──在留出集上调整值──
3. **困难。**Dans le cadre de la mise en œuvre de la recherche mixte, la recherche mixte de la RAG est mise en œuvre.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive QA | Find the answer span | Predict start and end indices of the answer within a given passage. |
| Open-domain QA | QA over a corpus | No given passage; must retrieve then answer. |
| RAG | Retrieve then generate | Retrieval-augmented generation. Retriever + reader pipeline. |
| SQuAD | Canonical benchmark | Stanford Question Answering Dataset. EM + F1 metrics. |
| Hallucination | Made-up answer | Reader output not supported by retrieved context. |
| Refusal calibration | Know when to shut up | System correctly says "I don't know" when unable to answer. |
> ♪ Les termes que les gens disent souvent ♪ ♪ Le sens réel ♪
|------|-----------|---------|
| 抽取式问答 | 找答案片段 | 预测给定段落中答案的起始和结束索引。 |
| 开放域问答 | 语料上的问答 | 无给定段落；必须先检索再回答。 |
| RAG | 检索再生成 | 检索增强生成。检索器 + 阅读器流水线。 |
| SQuAD | 经典基准 | 斯坦福问答数据集。EM + F1 指标。 |
| 幻觉 | 编造答案 | 阅读器输出不被检索上下文支持。 |
| 拒绝校准 | 知道何时闭嘴 | 系统在无法回答时正确地说 "I don't know"。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) le document de référence.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, le retriever canonique pour l'AQ.
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)Le journal qui a nommé RAG.
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997) enquête exhaustive du RAG.
> - [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) 基准论文──
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, 问答的经典密检索器──
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) 命名 RAG 的论文──
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997) 综合 RAG 综述。
