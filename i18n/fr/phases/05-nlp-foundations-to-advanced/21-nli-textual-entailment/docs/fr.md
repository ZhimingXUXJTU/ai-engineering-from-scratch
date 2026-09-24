# L'inference en langage naturel  Entraînement textuel 

> "t implique h" signifie qu'une lecture humaine t conclurait h est vrai. NLI est la tâche de prédire l'implication / contradiction / neutre.
> "t 含 h" signifie que l'homme a lu et fait des conclusions h 为真──NLI est un prévé­sage 含/矛盾/中性的任务──表面无聊,生产中承重──

> **【中文解读】**NLI 判断两个句子之间的逻辑关系: 含、矛盾、中性──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment Analysis), Phase 5 · 10 (Attention) | **前置知识:** Phase 5 · 05（情感分析），Phase 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Vous avez construit un chatbot. Il a répondu "oui". Comment savez-vous que "oui" est soutenu par les preuves? Vous devez classer 10 000 articles d'actualité par sujet. Vous avez 50 exemples étiquetés. Vous le transformez en NLI: "ce texte concerne {thème}"  implication ou contradiction? Vous devez vérifier si un résumé généré est fidèle à la source. NLI encore.

> Vous avez construit un chat en ligne. Il répond "oui" et vous savez comment "oui" a des preuves ? Vous avez besoin de 50 échantillons de fichiers pour les articles de discussion. Vous allez les transformer en NLI:

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

Les trois problèmes se réduisent à l'inference naturelle. NLI est la tâche de base qui prend en charge la vérification des faits, la classification à tir zéro, l'évaluation de la résumé et la vérification de la récupération.

> Ces trois problèmes se résument à la logique du langage naturel. L'INL est le support de la vérification des faits, de la mise en œuvre de la classification des échantillons, de l'évaluation et de la vérification des résultats.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

**The task.**En raison de la prémisse `t`et hypothèse `h`, classent leur relation comme l'une des suivantes: Entraînement (t implique h), Contradiction (t contredit h), Neutral (ni l'un ni l'autre).

> **任务。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `t`Et si vous le voulez`h`,将它们的关系分类为: 含t 含 h) 、矛盾t 矛盾 h) 、中性都不是) ∼三分类。

**Cross-encoder approach.**Concaténer t et h, alimenter par un transformateur, classer. Utilisé pour des applications critiques de précision. Lent parce que vous exécutez le modèle complet pour chaque paire.

> **交叉编码器方法。**拼音 t 和 h,通过 Transformer,分类──用于准确率关键的应用──慢因为每对运行完整模型──

**Bi-encoder approach.**Encodez t et h séparément, comparez les emblèmes (semblance de cosine). Rapide pour la récupération mais moins précis.

> **双编码器方法。**Résumé: Le code de l'écriture est le même que celui de la rédaction de la lettre.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.
```figure
nli-router
```

## Faites-le

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

### Étape 1: classification à zéro tir via NLI

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("roberta-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli")

def nli_classify(premise, hypothesis):
    inputs = tok(premise, hypothesis, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits[0]
    # 0=contradiction, 1=neutral, 2=entailment
    probs = torch.softmax(logits, dim=-1)
    labels = ["contradiction", "neutral", "entailment"]
    return {labels[i]: probs[i].item() for i in range(3)}

print(nli_classify("A man is playing guitar.", "Someone is making music."))
```

> **【中文解读】**Ce chapitre montre comment mettre en œuvre rapidement cette technique dans un cadre mature.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

La pile NLI de production:

> Produire une PNL 技术:

- **Zero-shot classification:**Modèles de NLI (DeBERTa-v3-grand-mnli). / 零样本分类:NLI 模型。
- **Fact verification:**NLI en codeur croisé sur la réclamation contre la preuve. / 事实验证:交叉编码器 NLI。
- **Summary faithfulness:**Vérifiez chaque phrase résumée par rapport à la source. / 摘要忠实度:检查每个摘要句子与源。
- **RAG grounding:**Le contexte récupéré de vérifier prend en charge la réponse. / RAG 定:验证检索上下文支持答案──

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-nli-applications.md`- Le numéro de la liste:

> 保存为 `outputs/skill-nli-applications.md`- Le numéro de la liste:

```markdown
Given a production need (fact-checking, zero-shot classification, summary evaluation), design the NLI pipeline.
1. Model choice. Cross-encoder (accuracy) or bi-encoder (speed).
2. Input format. Premise-hypothesis pairs.
3. Evaluation. Accuracy on labeled NLI datasets.
```

> **【中文解读】**练习题按照 Easy/Medium/Hard 三个难度递进――建议至少完成 级别题――

## Les exercices

1. **Easy.**Utilisation `roberta-large-mnli`pour la classification des sujets à tir zéro sur 20 phrases. / **简单。**Utilisation `roberta-large-mnli`Pour 20 phrases faire zéro échantillon sujet de catégorie:
2. **Medium.**Construisez un vérificateur de fidélité de résumé à l'aide de NLI. Évaluez sur CNN/DailyMail. / **中等。**Utilisation de l'analyse de fidélité de l'analyse de fidélité de l'analyse de fidélité de l'analyse de fidélité de l'analyse de la fidélité de l'analyse de la fidélité de l'analyse de la fidélité de l'analyse de la fidélité de l'analyse de la fidélité de l'analyse de la fidélité de l'analyse de la fidélité de l'analyse de la fidélité de l'analyse de la fidélité de l'analyse de la fidélité de la fidélité de l'analyse de la fidélité de l'analyse de la fidélité de la fidélité de l'analyse de la fidélité de la fidélité de l'analyse de la fidélité de la fidélité de la fidélité de la fidélité de la fidélité de la fidélité.
3. **Hard.**Comparer le cross-encoder contre le bi-encoder NLI pour la vérification des réponses RAG.**困难。**Comparer un codeur de croisement avec un codeur de double NLI utilisé pour l'évaluation des réponses RAG.

## Les termes clés

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NLI（自然语言推理） | Entailment task / 蕴含任务 | Classify premise-hypothesis pairs as entailment/contradiction/neutral. / 将前提-假设对分类为蕴含/矛盾/中性。 |
| Cross-encoder（交叉编码器） | Joint encoding / 联合编码 | Encode both texts together through the full model. / 通过完整模型联合编码两个文本。 |
| Bi-encoder（双编码器） | Separate encoding / 分离编码 | Encode each text independently, compare embeddings. / 独立编码每个文本，比较嵌入。 |

## Encore une lecture

- [Bowman et al. (2015). SNLI](https://nlp.stanford.edu/pubs/snli_paper.pdf) le ensemble de données de Stanford NLI. / Stanford NLI 数据集──
- [He et al. (2021). DeBERTa v3](https://arxiv.org/abs/2111.09543) modèle NLI de pointe. / 先进 NLI 模型。
