# L'évaluation à long terme  NIAH, RULER, LongBench, MRCR 长上下文评估  NIAH、RULER

> Gemini 3 Pro annonce 10 millions de jetons de contexte. À 1 million de jetons, le MRCR à 8 aiguilles tombe à 26,3%.
> Gemini 3 Pro 宣称10M token 上下文──在1M token 时,8-needle MRCR 降至26.3%──宣称的 ≠可用──长上下文评估告诉你你正在部署模型的实际能力──

> **【中文解读】**évaluer la performance réelle du LLM dans la fenêtre de la section "La formation professionnelle"

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 27 (LLM Evaluation) | **前置知识:** Phase 5 · 27（LLM 评估）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

C'est l'écart de capacité de contexte de 2026. Les feuilles de spécifications disent 1M de jetons. Les points de référence disent: à 100K de jetons, la précision de récupération diminue de 15 à 40%. à 500K, elle diminue de 40 à 70%. Le modèle ne " voit " pas tout dans sa fenêtre de contexte de la même manière.

> C'est la différence de capacité de l'année 2026 en haut et en bas. Le modèle n'est pas " voir " dans les mêmes fenêtres que dans les autres.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans le cadre de la construction réelle ?

L'évaluation à long terme mesure ces axes: précision de récupération à différentes profondeurs, raisonnement multi-hop sur les documents et agrégation sur les informations distribuées.

> 长上下文评估测量: les différents axes de recherche de profondeur, les taux de précision des recherches, les hypothèses de multiples sauts entre les archives, ainsi que la concentration des informations distribuées.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de la conception.

**NIAH (Needle in a Haystack).**Insérer un fait spécifique dans un document long à différentes positions. Demandez au modèle de le récupérer. Mesures: le modèle peut-il trouver une aiguille à la profondeur X dans un paquet de foin à jetons Y?

> **NIAH（大海捞针）。**Dans chaque position du long archives, il est possible de saisir des faits spécifiques.

**RULER.**Élargit le NIAH avec des tâches multi-aiguilles, à distance variable et d'agrégation.

> **RULER。**扩展 NIAH 添加多针、可变距离和聚合任务──更全面──

**LongBench.**Les tâches de contexte réel: résumé, QA, récupération, code. Plus représentatives que les benchmarks synthétiques.

> **LongBench。**Récapitulatif: récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapitulatif, récapit, récapitulatif, récapitulatif, récapit, récapit, récapit, récapitulatif, récapit, récapit, récapit, récapit, récapitulatif, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit, récapit et récapit, récapit, récapit, récapit et récapit.

**MRCR (Multi-hop Reasoning over Context).**Le raisonnement qui nécessite la connexion d'informations entre plusieurs documents.

> **MRCR（上下文多跳推理）。**Il faut passer à travers plusieurs documents pour obtenir des informations.

> **【拓展：大语言模型的工程实践】**Le GPT à ChatGPT, le NLP, a connu une transformation de la mode.
```figure
gx-niah-decay
```

## Faites-le

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est la structure la plus populaire de l'IA de l'entreprise actuelle 应用──

> **【拓展：NLP 的多语言挑战】**Dans le monde, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Le code est passé de zéro à zéro pour réaliser l'algorithme central.

### Étape 1: test simple de NIAH

```python
def needle_in_haystack(model, context_length, needle, needle_position):
    """Insert needle at position in a long document and test retrieval."""
    haystack = generate_irrelevant_text(context_length)
    full_text = haystack[:needle_position] + f"\n{needle}\n" + haystack[needle_position:]
    question = f"What is the secret fact hidden in the text?"
    response = model(full_text + "\n\n" + question)
    return needle.lower() in response.lower()
```

> **【中文解读】**Ce chapitre montre comment utiliser un cadre mature pour appliquer rapidement cette technologie.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL.

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**Le présent article se concentre sur la façon dont le modèle sera déployé pour les produits disponibles.

| Benchmark / 基准 | Type / 类型 | Measures / 测量 |
|---------|------|---------|
| NIAH | Synthetic / 合成 | Single-fact retrieval at depth. / 深度单事实检索。 |
| RULER | Synthetic / 合成 | Multi-needle + aggregation. / 多针 + 聚合。 |
| LongBench | Real / 真实 | Practical long-context tasks. / 实用长上下文任务。 |
| MRCR | Synthetic / 合成 | Multi-hop reasoning. / 多跳推理。 |

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-long-context-eval.md`- Le numéro de la liste:

> 保存为 `outputs/skill-long-context-eval.md`- Le numéro de la liste:

```markdown
Given a model claiming long-context support, verify actual performance.
1. Context length to test.
2. Benchmarks to run (NIAH, RULER, LongBench).
3. Minimum acceptable accuracy at target length.
```

## Les exercices

1. **Easy.**Exécutez NIAH sur un modèle à 10K et 50K jetons.**简单。**Dans les 10K et 50K, le jeton est en cours de fonctionnement.
2. **Medium.**Construire un test à plusieurs aiguilles, mesurer la récupération de 5 faits dans un contexte de 100K. / **中等。**构建多针测试──
3. **Hard.**Comparer 3 modèles sur LongBench. Rapport qui dégrade le plus rapidement. / **困难。**Dans le long de la banque, on peut comparer 3 modèles:

## Les termes clés

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| NIAH（大海捞针） | Insert fact in long text, test retrieval. / 在长文本中插入事实，测试检索。 |
| Context window（上下文窗口） | Maximum input length a model can process. / 模型能处理的最大输入长度。 |
| Multi-hop reasoning（多跳推理） | Connect info across multiple documents. / 跨文档连接信息。 |

## Encore une lecture

- [NIAH original](https://arxiv.org/abs/2404.05460)Une aiguille dans un tas de foin.
- [RULER](https://arxiv.org/abs/2404.02372) référence prolongée à long contexte. / 扩展长上下文基准。
- [LongBench](https://arxiv.org/abs/2308.14508) tâches de contexte long réelles.
