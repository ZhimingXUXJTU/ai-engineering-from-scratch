# Pourquoi les agents se cassent ?

> MASFT (Berkeley, 2025) catalogue 14 modes de défaillance multi-agents dans 3 catégories. La taxonomie de Microsoft documente comment les défaillances existantes de l'IA s'amplifient dans les paramètres agence. Les données du domaine de l'industrie convergent sur cinq modes récurrents: actions hallucinées, glissement de portée, erreurs en cascade, perte de contexte, mauvaise utilisation des outils.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 05 (Self-Refine and CRITIC), Phase 14 · 24 (Observability) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

>  **【前置】**學本節前 請先掌握:Phase 14·05(Self-Refine / CRITIC) 理解单 Agent 自我纠错的局限性;Phase 14·24(Observability) 本节假设你已经能使用OpenTelemetry 看完整的痕迹──本节教你**识别 trace 中的失败模式**, est la phase 14·29 (Times de production) de la première étape.

> 🤔 **【困惑】**Q: Pourquoi l'agent failure que le logiciel traditionnel faillir plus difficile à trouver? A: Parce que l'agent failure est "soft failure"code没崩、API 没返回错误, mais l'agent utilise des outils erroris调用、错误参数、错误顺序"成功完成" pour accomplir la tâche.

## Objectifs d'apprentissage

- Nommer les trois catégories de défaillance du MASFT et au moins quatre modes spécifiques dans chacune d'elles.
- Expliquez pourquoi l'échec agentrique amplifie les modes d'échec existants de l'IA (bias, hallucinations).
- Décrivez les cinq modes récurrents dans l'industrie et leurs atténuations.
- Implémenter un détecteur stdlib qui trace les étiquettes de l'agent avec des étiquettes de mode défaillance.

## Le problème , l' introduction du problème

Les équipes envoient des agents qui travaillent sur 90% des traces. Les défaillances de 10% ne sont pas du bruit aléatoire  ils tombent dans un petit nombre de catégories récurrentes. Une fois que vous pouvez les nommer, vous pouvez les surveiller et les corriger.

> L'agent publié par l'équipe travaille normalement sur 90% du suivi. Les défaillances de 10% ne sont pas des bruits aléatoires.


> **【中文解读】**Le mode de défaillance d'un agent diffère du logiciel ordinaire: 1) le niveau de défaillance d'un agent est un facteur de défaillance de la décision d'une erreur; 2) le but de la délocalisation de l'agent est un facteur de défaillance de l'agent dans la longue chaîne; 3) la surconfiance d'un agent dans les erreurs de son travail.

> **{【拓展：2025-2026 年的 Agent 事故报告揭示了系统性失败模式。典型案例如下：(1) 编码 Ag...】}**Le rapport d'accident d'agent pour les années 2025-2026 révèle un modèle de défaillance systémique.

>  **【类比】**Les 5 principales causes de l'accident de voiture: 1)**幻觉动作**=看错导航开错路;(2) **范围蔓延**= aurait été acheté pour la province voisine;**级联错误**=小擦后慌乱撞墙;(4) **上下文丢失**= j'ai oublié où je suis;**工具误用**=把油门当车. 每种失败有应对防御:导航验证、明确终点、紧急停车按、定期回顾、工具白名单──

> ️ **【易错点】**L' agent 失败排查的 3 个坑:**只看最终输出**Agent 自信说"完成", mais le milieu des étapes complet;务必看完整的痕迹,不仅看结尾() 的输出──(2) **不设失败预算** le même erreur连续重试 20 次烧光预算; avec max_retries=3 + 失败计计器──(3) **没做意图验证**L'agent décide de "supprimer le fichier X", mais X est /etc/passwd;

## Le concept de base.

### Les résultats de l'enquête ont été obtenus au cours de la première année de l'enquête.

La taxonomie des défaillances du système multi-agents. 14 modes de défaillance regroupés en 3 catégories.

> Le modèle d'agent 失败包括:级联失败 (un faux pas propagé à plusieurs utilisations) 幻觉成功 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环

L'affirmation centrale: les défaillances sont des défaillances de conception fondamentales dans les systèmes multi-agents, et non des limites de la MLL à corriger avec de meilleurs modèles de base.

> 核心主张: l'échec est une faille de conception fondamentale du système multi-agent, et non une limitation de la loi qui peut être réparée par un meilleur modèle de base.

> Le modèle d'agent 失败包括:级联失败 (un faux pas propagé à plusieurs utilisations) 幻觉成功 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环

### Taxonomie de Microsoft du mode d'échec dans les systèmes d'IA agencés

- Les défaillances existantes de l'IA (bias, hallucinations, fuites de données) se amplifient dans les paramètres agents.
- De nouveaux échecs émergent de l'autonomie: action involontaire à grande échelle, utilisation abusive des outils, dérive de mission.
- Le livre blanc est le registre des risques pour les produits agencés.

### Caractériser les défauts de l'IA agentique (arXiv:2603.06847)

- Les échecs résultent de l'orchestration, de l'évolution de l'état interne et de l'interaction environnementale.
- Pas seulement "mauvais code" ou "mauvais modèle de sortie".

### Enquête sur les hallucinations d'agents de la LLM (arXiv:2509.18970)

Deux manifestations principales:

1. **Instruction-following Deviation**L'agent ne suit pas les instructions du système.
2. **Long-range Contextual Misuse** l'agent oublie ou utilise mal le contexte des virages précédents.

Erreurs de sous-intention: omission (pas de étape), redondance (étape répétée), désordre (étapes hors ordre).

> Le modèle d'agent 失败包括:级联失败 (un faux pas propagé à plusieurs utilisations) 幻觉成功 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环

### Les cinq modes récurrents dans l'industrie

Les analyses de terrain d'Arize, Galileo et NimbleBrain 2024-2026 convergent sur:

> Le modèle d'agent 失败包括:级联失败 (un faux pas propagé à plusieurs utilisations) 幻觉成功 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环

1. **Hallucinated actions.**L'agent invoque un outil qui n'existe pas ou fabrique des arguments.
2. **Scope creep.**L'agent élargit la tâche au-delà de la demande de l'utilisateur (crée des relations publiques supplémentaires, envoie des courriels supplémentaires).
3. **Cascading errors.**Un faux appel déclenche des effets en aval. Une hallucination fantôme SKU déclenche quatre appels API  un incident multi-système.
4. **Context loss.**Les tâches à long horizon oublient les contraintes de tour en début de journée.
5. **Tool misuse.**Appelle le bon outil avec les mauvais arguments, ou le mauvais outil entièrement.

Les agents ne peuvent pas distinguer "j'ai échoué" de "la tâche est impossible" et hallucinent souvent un message de succès sur 400 erreurs pour fermer la boucle.

> L'agent ne peut pas distinguer "j'ai échoué" et "la tâche est impossible à accomplir", il apparaît souvent dans 400 erreurs sur le fait de sortir une nouvelle réussite pour fermer le cycle.

> Le modèle d'agent 失败包括:级联失败 (un faux pas propagé à plusieurs utilisations) 幻觉成功 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环

### L'atténuation: portes à chaque étape

Ports de vérification automatisés à chaque étape d'une chaîne de raisonnement, vérifiant la base factuelle par rapport à l'état de l'environnement.

> Le modèle d'agent 失败包括:级联失败 (un faux pas propagé à plusieurs utilisations) 幻觉成功 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环

- Classifiateur de sécurité par étape (leçon 21).
- Validation des arguments d'appel à l'outil (leçon 06).
- Contrôle croisé des contenus récupérés par rapport à des faits connus (leçon 05, CRITIC).
- Détecter les hallucinations de succès en réessayant l'état (le fichier a-t-il été créé?).

### Où le contrôle des défaillances va mal

- **Tagging only crashes.**La plupart des défaillances d'agents produisent une sortie valide.
- **No baseline.**La détection de la dérive a besoin d'un dernier bien connu; sans elle, vous ne pouvez pas dire "cela s'aggrave".
- **Over-alerting.**Chaque défaillance produit une page, un cluster et une limite de taux.

> **仅标记崩溃。**La plupart des agents ne réussissent pas à produire des produits efficaces.
> **没有基线。**漂移检测 nécessite un état de santé parfait; sans elle, vous ne pouvez pas dire "c'est un mauvais état".
> **过度告警。**Chaque défaite produit une page.

## Construisez-le et mettez-le en œuvre.
```figure
failure-cascade
```

## Faites-le

`code/main.py`met en œuvre un étiquetage de mode d'échec stdlib:

> Le modèle d'agent 失败包括:级联失败 (un faux pas propagé à plusieurs utilisations) 幻觉成功 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环

- Un ensemble de données de traces synthétiques couvrant les cinq modes.
- Les fonctions du détecteur par mode (patterns de signature des appels à l'outil, sorties, répétitions d'actions).
- Un étiquetage qui étiquette chaque trace et rapporte la distribution de mode.

- Je vais le faire.

```
python3 code/main.py
```

Produit: étiquettes par trace + distribution agrégée, une reproduction bon marché de ce que les surfaces de clustering de trace de Phoenix.

> 输出: chaque étiquette de suivi + 聚合分布,Phoenix 追踪聚类所显示内容的廉价复现──

> Le modèle d'agent 失败包括:级联失败 (un faux pas propagé à plusieurs utilisations) 幻觉成功 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环

## Utilisez-le avec le cadre de réalisation

- **Phoenix**pour le regroupement des dérives de production (leçon 24).
- **Langfuse**pour la répétition de session + annotation.
- **Custom**pour les signatures spécifiques à un domaine que votre plateforme d'observabilité ne peut pas détecter.

## Envoyez-le . Produit .

`outputs/skill-failure-detector.md`génère des détecteurs de mode d'échec adaptés à votre domaine, câblés à un magasin de traces.

> `outputs/skill-failure-detector.md`Un détecteur de défaillance de votre domaine, connecté à la réserve de suivi.

> Le modèle d'agent 失败包括:级联失败 (un faux pas propagé à plusieurs utilisations) 幻觉成功 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环爆炸 (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环 explosion (un faux pas est fait) 循环

## Les exercices

1. Ajouter un détecteur pour "hallucination réussie": l'agent renvoie le succès mais l'état cible est inchangé.
  Le mot "exercer" est traduit par "exercer".
2. Étiquettez 100 traces réelles d'un produit que vous avez construit. Quel mode domine?
  Le mot "exercer" est traduit par "exercer".
3. Mettre en œuvre une métrique de "radius de cascade": compte tenu d'une défaillance à l'étape N, combien d'étapes en aval a-t-elle affectées?
  Le mot "exercer" est traduit par "exercer".
4. Lisez les 14 modes de défaillance de MASFT, choisissez trois qui s'appliquent à votre produit, écrivez des détecteurs.
  Le mot "exercer" est traduit par "exercer".
5. Le câblage d'un détecteur dans un travail d'informatique: défaillance de la construction si >=5% des traces étiquetent un mode.
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| MASFT | "Multi-agent failure taxonomy" | Berkeley 14-mode categorization |  |
| Cascading error | "Ripple failure" | One early mistake propagates through N steps |  |
| Context loss | "Forgot the constraint" | Long-horizon turn drops early-turn facts |  |
| Tool misuse | "Wrong tool / wrong args" | Valid call, wrong invocation |  |
| Success hallucination | "Faked completion" | Agent claims success on a 400; state unchanged |  |
| Scope creep | "Overreach" | Agent does more than asked |  |
| Instruction-following deviation | "Disobedience" | Ignores system prompt or user constraint |  |
| Sub-intention errors | "Plan bugs" | Omission, redundancy, disorder in plan execution |  |

## Encore une lecture

- [Cemri et al., MASFT (arXiv:2503.13657)](https://arxiv.org/abs/2503.13657) 14 modes de défaillance, 3 catégories
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Microsoft, Taxonomy of Failure Mode in Agentic AI Systems](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) registre des risques
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Arize Phoenix](https://docs.arize.com/phoenix) Clustering à la dérive dans la pratique
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) lorsque les modèles plus simples évitent complètement les modes
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
