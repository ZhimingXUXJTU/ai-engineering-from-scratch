# Le modèle de routage comme un primitif de réduction des coûts

> Un courtier dynamique évalue chaque demande (type de tâche, longueur de jeton, similarité d'intégration, confiance) et envoie des requêtes simples à un modèle bon marché, en augmentant les requêtes complexes à un modèle frontalier. On l'appelle aussi cascade de modèle. Des études de cas de production montrent une réduction de 20 à 60% des coûts à l'aide de l'iso-qualité dans les déploiements aux États-Unis/Royaume-Uni/UE; une amélioration de 30% de l'efficacité de routage sur le SaaS à volume élevé se transforme en économies annuelles de six chiffres. Le contexte de 2026 est que les prix des inférences LLM ont chuté ~ 10x par an  un jeton de classe GPT-4 est allé de $20/M to ~$0,40/M de fin 2022 à 2026. La plupart des dépôts sont plus efficaces pour les piles (phase 17 · 04-09), et non pour le matériel. Le routage est la façon dont vous convertissez cette baisse de prix en marge sans régression du produit. Le mode d'échec est le dérivé du modèle bon marché: le trajet pousse 40% vers un modèle plus faible, la qualité diminue de 3 à 5% sur les tâches de raisonnement, personne ne remarque pendant un quart. Les itinéraires de passerelle par métriques de qualité en ligne, pas seulement les ensembles d'évaluation hors ligne.

> **【中文解读】**Ce chapitre présente les stratégies d'optimisation des coûts de différents modèles en fonction de la complexité des tâches.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cascading router simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 19 (AI Gateways) | **前置知识:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 19 (AI Gateways)

>  **【前置】**Pour les autres, il est nécessaire de prendre en compte la phase 17 de la formation.
>  **【类比】**模型路由 = "hôpital分诊"──简单感冒→社区医生(Haiku/Sonnet);疑难杂症→专家(Opus);急诊→主任(GPT-4)──20-60% 成本降,30% 路由效率改进=六位数年省──背景:LLM 价格 2022-2026 降10倍/年,多数降来自服务改进而非硬件路由把降价转转成利──
> ️ **【易错点】**便宜模型漂移:40% 路由到弱模型→推理质量降低 3-5%→一个季度没人发现──修复:用在线质量监控(不仅离线评估)守住底线──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objectifs d'apprentissage

- Expliquez le cascade de modèle: bon marché-premier avec vérification de la confiance, escalade sur la confiance faible.
  Le prix de la vente est le prix de la vente.
- Enumérer les quatre signaux de routage (classification des tâches, longueur rapide, intégration de la similitude avec un ensemble connu de dur, confiance en soi à partir du premier passage).
  Le premier est le suivant: "Le premier est le premier".
- Calculer le coût combiné attendu à la fraction de routage cible et la tolérance aux pertes de qualité.
  Traduction anglaise: calcul objectif route de la tolérance à la perte de qualité et de la distribution.
- Nombre de mesures de surveillance de la dérive (portée de qualité en ligne) qui prennent le modèle bon marché.
  Le modèle de qualité de la délocalisation est un modèle de qualité de la délocalisation.

## Le problème , l' introduction du problème

> **【中文解读】**模型路由的核心洞察:70% de la requête est simple (:" Paris a quelques points ? "), peut être traité avec un modèle de Haiku à 3% de coût. Seulement 30% nécessite une capacité de raisonnement de GPT-5 级.

> **【拓展：模型路由的产业案例】**Les prix de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de production de l'équipement de l'équipement de production de l'équipement de production de l'équipement de l'équipement de production de l'équipement de l'équipement de l'équipement de l'équipement de l'équipement de l'équipement de l'équipement de l'équipement de l'équipement de l'équipement de l'équipement ont été de la société de la société de l'équipement de l'équipement de l'équipement de la société de l'équipement de l'équipement de l'équipement de l'équipement de l'équipement de la société de la société de la société de l'équipement de la société de la société de l'équipement de la société de l'équipement de l'équipement de l'équipement de l'é de la société de l'équipement de la société de la société de la société de la société de l'équipement de l'é de l'équipement de l'équipement de l'é de la société de la société$20/M 降到 $0,40/M), la plupart de la baisse provient de la suggestion de l'optimisation (Phase 17·04-09)  Le modèle vous permet de capturer ces avantages à l'application, plutôt que d'attendre que tous les utilisateurs se déplacent vers un modèle bon marché  Le routeur ouvert RouteLLM (LMSYS) et le programme commercial Non Diamond sont en train de se dérouler rapidement 

Votre service coûte 80 000 $ par mois sur GPT-5. Vos analyses montrent que 70% des questions sont simples: "qu'est-ce que l'heure est à Paris?" "réphrasez cette phrase". Un modèle de classe Haiku les gère parfaitement à 3% du coût. 30% ont besoin du raisonnement de GPT-5.

Si vous roulez les 70% vers le bon marché et 30% vers le coûteux, votre facture diminue de 65% à la même qualité du produit.

## Le concept de base.

### Quatre signaux de routage

> **【中文解读】**                                                                                                                                                                                                                                                              

1. **Task classification**: simple/complexe/codegen/math/chat. Peut être un classifiant basé sur des règles, un petit LLM (Haiku-class à 0,25 $/M), ou intégrer la similitude avec des seaux étiquetés.

2. **Prompt length**Les commandes <500 de marque n'ont généralement pas besoin de frontière pour la cohérence.

3. **Embedding similarity to known-hard set**: si la requête est proche (cosine > 0,88) d'un seau de dureté connue, escalader directement à la frontière.

4. **Self-confidence from first-pass**Si les tests de logs du modèle montrent une faible confiance OU s'il refuse OU les sorties de langage de couverture, réessayez à la frontière.

### Trois modèles

> **【拓展：模型路由的三种模式】**Le modèle est un modèle de développement de trois modes de réalisation: 1) pré-route  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  préposition  pré

**Pre-route**(classifiateur en avant): ~5-10ms de latence ajoutée; plus rapide dans l'ensemble.

**Cascade**(primaire moins cher, augmentation sur faible confiance): ~ 1,2x la latence médiane (exécution moins chère plus vérification), ~ 2x sur augmentation.

**Ensemble route**(exécution à bas prix et frontière en parallèle pour un échantillon, choix de modèle de récompense): la plus haute qualité, le coût le plus élevé; utilisation uniquement pour des A/B critiques.

### Mise en œuvre

Les passerelles d'IA (phase 17 · 19) exposent le routage.`router`Portkey a des gardiens + routage. Kong AI Gateway a un routage basé sur des plugins. Le marché de modèle OpenRouter expose une API de recommandation.

Le code de base est basé sur le code de base.

### La courbe des prix de 2026

| Model class | Late 2022 | 2026 | Change |
|-------------|-----------|------|--------|
| GPT-4-level quality | ~$20/M | ~$0.40/M | 50x cheaper |
| Frontier (GPT-5, Claude 4) | — | ~$3-10/M | new tier |

La plupart des améliorations sont en service de l'efficacité  les leçons de base de la phase 17 · 04-09 ont été transformées en baisses de coûts du côté du fournisseur.

### La dérive est le risque réel

> **【中文解读】**漂移是模型路由的真正风险──路由将将40% 发送到廉价模型,6 个月后任务分布变化(用户更成熟、问题更长),但路由器的分类器仍然基于Q1 数据训练──质量下降没有投诉足够响亮,直到竞争对手的基准测试中落败才知道──必须通过在线质量指标门控路由:用户反自动LLM 评审(5%采样) 升级率、拒绝率──

> **【拓展：模型路由的实现方案】**L'option de mise en œuvre du modèle de route de 2026 est la suivante: 1) l'AI 网关(Phase 17·19) LiteLLM de routeur configuration  Portkey de gardiens+routage Cong AI Gateway de plug-style route OpenRouter de recommandation API; 2) l'Open Source RouteLLM LMSYS) fournir une base de route complète; 3) 商业Not Diamond 提供 SaaS 模型路由产品──三种路由模式:Pre-route 前置分类,最快) Cascade 先廉价再升级,质量最稳定) Ensemble 并行运行多模型+奖励模型选择,最高质量但最高成本) 

Votre route envoie 40% au modèle bon marché. Au cours de six mois, la répartition des tâches change (les utilisateurs deviennent plus sophistiqués, posent des questions plus longues). Le routeur ne remarque pas parce que son classifiateur a été formé sur les données du premier trimestre. La qualité diminue silencieusement. Personne ne se plaint assez fort. Vous découvrez dans un benchmark concurrentiel que vous avez perdu.

Route de passerelle selon les mesures de qualité en ligne:

- Les pouces des utilisateurs vers le haut/ vers le bas par route.
- Juge automatique de la LLM sur un échantillon de détention (5%) par route.
- Taux d'escalade: si la cascade monte de plus de 30%, le modèle bon marché est sur-routé.
- Taux de refus par route.

### Les chiffres que vous devriez vous rappeler

- 2026 économie de routage à iso-qualité: 20 à 60% d'études de cas.
- Réduction du prix des LLM 2022-2026: ~ 10 fois par an.
- Niveau GPT-4 2022 contre 2026: ~$20/M → ~$0,40/M.
- Impact de la latence en cascade: ~ 1,2x la médiane, ~ 2x l'escalade (~ 10% du trafic).

## Utilisez-le avec le cadre de réalisation
```figure
model-cascade-router
```

## Utilisez-le

`code/main.py`Les données de l'étude de la Commission sont fournies par le rapport de l'Union européenne, qui a été établi en décembre 2014.

> `code/main.py`Les données de l'étude de la Commission sont fournies par le rapport de l'Union européenne, qui a été établi en décembre 2014.

> `code/main.py`Les données de l'étude de la Commission sont fournies par le rapport de l'Union européenne, qui a été établi en décembre 2014.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-router-plan.md`- En raison de la charge de travail et du budget de qualité, choisit un modèle de routage et des signaux.

> 本课产 出 `outputs/skill-router-plan.md`- En raison de la charge de travail et du budget de qualité, choisit un modèle de routage et des signaux.

## Les exercices

1. On court .`code/main.py`À quel étage de précision la cascade va-t-elle avant le trajet ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ Quel niveau de précision est supérieur à celui de l'interface ?
2. Votre base d'utilisateurs est de 30% d'entreprise (queries complexes), 70% de niveau gratuit (simple).
   Le nombre de personnes qui utilisent le site est de 30% en entreprise, 70% en ligne.
3. Une route réduit la qualité de 2% mais économise 40%.
   Un chemin réduit la qualité de 2% mais économiser 40%...
4. Mettre en œuvre un contrôle de confiance en utilisant des logprobs d'API OpenAI / Anthropic.
   Le code de référence est le code de référence de l'API.
5. Au cours de six mois, le taux d'escalade passe de 8% à 22%.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Model routing | "cost broker" | Dynamic choice of model per request |
| Model cascade | "cheap-first escalate" | Run cheap, fall through to frontier on low confidence |
| Pre-route | "classify first" | Classifier up front; no re-run |
| Ensemble route | "parallel pick" | Run multiple, reward-model picks best |
| Escalation rate | "uprouted %" | Fraction of cascade requests that escalated |
| RouteLLM | "LMSYS router" | OSS router library |
| Not Diamond | "commercial router" | SaaS model-routing product |
| Drift | "cheap creep" | Distribution shift without router noticing |
| Online quality gate | "live check" | Automated LLM-judge sampling live traffic |

## Encore une lecture

- [AbhyashSuchi — Model Routing LLM 2026 Best Practices](https://abhyashsuchi.in/model-routing-llm-2026-best-practices/)
- [Lukas Brunner — Rise of Inference Optimization 2026](https://dev.to/lukas_brunner/the-rise-of-inference-optimization-the-real-llm-infra-trend-shaping-2026-4e4o)
- [RouteLLM paper / code](https://github.com/lm-sys/RouteLLM)
- [Not Diamond — model routing](https://www.notdiamond.ai/)
- [OpenRouter](https://openrouter.ai/) passerelle multimodale avec des primitifs de routage.
