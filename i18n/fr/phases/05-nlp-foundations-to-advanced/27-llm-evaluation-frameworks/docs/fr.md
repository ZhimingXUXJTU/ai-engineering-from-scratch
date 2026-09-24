# L'évaluation de la licence  RAGAS, DeepEval, G-Eval  LLM  évaluer  RAGAS DeepEval

> L'équivalence sémantique est absente. L'examen humain n'est pas à l'échelle. LLM-as-judge est la réponse de production  avec suffisamment d'étalonnage pour faire confiance au nombre.
> 精确匹配和 F1 捕捉不到语义等价――examen artificiel non extensible――LLM 作为评审是生产答案经过足够的校准可以信任这个数字――

> **【中文解读】**évaluer la qualité de la formation en LLM, y compris les résultats de RAG 效果──RAGAS、DeepEval、G-Eval ‒ est le cadre principal──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 23 (Chunking), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 23（分块），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Le problème , l' introduction du problème

Votre système RAG répond: " 29 juin 2007. " La réponse de référence dit: " 29 juin 2007. " Le match exact dit faux. BLEU dit partiel. Un humain dit vrai. Vous avez besoin d'une mesure qui est d'accord avec les humains, équivaut à des milliers de sorties, et coûte moins cher que l'annotation humaine.

> Vous avez besoin d'une mesure compatible avec l'homme, qui peut être étendue à des milliers de sorties, et dont le coût est inférieur à celui de l'étiquetage artificiel.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans le cadre de la construction réelle ?

Maintenant, multipliez par 10 000 cas de test. Multipliez à nouveau par chaque mise à jour de modèle que vous voulez envoyer. L'évaluation humaine n'est pas à l'échelle. Vous avez besoin de mesures automatisées qui corrélataient avec le jugement humain à r ≥ 0,85.

> Il est maintenant nécessaire de multiplier par 10 000 les cas de test.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de la conception.

2026 a trois cadres qui possèdent ce problème.

> En 2026, trois cadres régissent ce problème:

**RAGAS.**Évaluation RAG. Évaluation de la récupération + génération conjointement. Mesures: fidélité, pertinence des réponses, précision du contexte, rappel du contexte.

> **RAGAS。**Réglage de la réaction de la Commission à la réaction de la Commission en matière de réaction à la crise économique et sociale

**DeepEval.**Le cadre de test unitaire pour les résultats du LLM. Mesures: pertinence des réponses, fidélité, biais, toxicité.

> **DeepEval。**Le programme de formation en médecine est un outil de formation en médecine.
```figure
n5-judge-gauge
```

## Faites-le

**G-Eval.**La chaîne de pensée qui incite à générer des critères d'évaluation, puis à marquer des résultats.

> **G-Eval。**Il est également possible de faire des recherches sur les résultats de la recherche et de la recherche.

> **【拓展：大语言模型的工程实践】**Le GPT à ChatGPT, le NLP, a connu une transformation de la mode.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est la structure la plus populaire de l'IA de l'entreprise actuelle 应用──

> **【拓展：NLP 的多语言挑战】**Dans le monde, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Le code est passé de zéro à zéro pour réaliser l'algorithme central.

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# Evaluate RAG pipeline
results = evaluate(
    dataset=rag_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
    llm=judge_llm,
    embeddings=embed_model,
)
print(results)
```

```python
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric

metric = FaithfulnessMetric(threshold=0.7, model="gpt-4")
assert_test(test_case, [metric])
```

> **【中文解读】**Ce chapitre montre comment utiliser un cadre mature pour appliquer rapidement cette technologie.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL.

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**Le présent article se concentre sur la façon dont le modèle sera déployé pour les produits disponibles.

| Framework / 框架 | Focus / 重点 | Best for / 最适合 |
|---------|--------|---------|
| RAGAS | RAG evaluation / RAG 评估 | Retrieval + generation / 检索 + 生成 |
| DeepEval | Unit testing / 单元测试 | CI/CD integration / CI/CD 集成 |
| G-Eval | Research / 研究 | Custom metrics / 自定义指标 |

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-llm-eval.md`- Le numéro de la liste:

> 保存为 `outputs/skill-llm-eval.md`- Le numéro de la liste:

```markdown
Given an LLM application (chatbot, RAG, agent), design evaluation pipeline.
1. Framework (RAGAS, DeepEval, G-Eval).
2. Metrics to track.
3. Calibration against human labels.
```

## Les exercices

1. **Easy.**Évaluer un simple pipeline RAG avec RAGAS. / **简单。**Utilisez RAGAS  évaluer une simple RAG 流水线。
2. **Medium.**Construire une suite de tests DeepEval pour un chatbot.**中等。**Pour créer un ensemble de tests DeepEval
3. **Hard.**Calibrer le LLM en tant que juge contre 200 étiquettes humaines.**困难。**Il a été créé par le gouvernement de l'État de New York.

## Les termes clés

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| RAGAS | RAG evaluation framework. / RAG 评估框架。 |
| Faithfulness（忠实度） | Answer is supported by context. / 答案有上下文支持。 |
| LLM-as-judge | LLM evaluates other LLM outputs. / LLM 评估其他 LLM 输出。 |

## Encore une lecture

- [RAGAS](https://docs.ragas.io/) Cadre d'évaluation du RAG. / RAG 评估框架。
- [DeepEval](https://docs.confident-ai.com/) Test d'unité de LLM. / LLM 单元测试。
- [G-Eval](https://arxiv.org/abs/2303.16634) évaluation de la chaîne de pensée. / 思维链评估。
