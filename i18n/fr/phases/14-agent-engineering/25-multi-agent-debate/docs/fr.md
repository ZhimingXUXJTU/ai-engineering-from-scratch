# Débat et collaboration multi-agents

> Du et al. (ICML 2024, "Société des esprits") exécutent des instances de modèle N qui proposent indépendamment des réponses, puis se critiquent périodiquement sur des tours R pour converger. Améliore la factualité, le respect des règles, le raisonnement.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 05 (Self-Refine and CRITIC) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objectifs d'apprentissage

- Expliquez le protocole de débat: N propositions, R ronds, convergent sur une réponse partagée.
- Décrivez pourquoi les débats améliorent la réalité, le respect des règles et la raison.
- Expliquez une topologie rare: tous les débatteurs n'ont pas besoin de se voir les uns les autres.
- Mettre en œuvre un débat stdlib sur un LLM scénarisé avec des variantes à plein réseau et rares; mesurer le coût des jetons par rapport à l'exactitude.

## Le problème , l' introduction du problème

L'auto-réfiguraison (leçon 05) est un modèle qui se critique  risque la pensée de groupe.

> L'auto-réfiguraison (en anglais: Self-Refine) est un modèle de critique de soi qui existe dans le groupe.

>  **【前置】**Débat est un modèle de réflexion qui se développe en plusieurs instances, ne comprend pas pourquoi il faut une réflexion en groupe.


> **【中文解读】**En effet, les résultats de la recherche de l'analyse de la qualité de l'analyse de la qualité de l'analyse de la recherche sont plus précises.

> **{【拓展：多 Agent 辩论是 2023-2025 年的研究热点。Du et al. (2023) 证明两个...】}**Du et al. (2023) démontrent que deux exemples de débats ChatGPT peuvent améliorer considérablement le taux de précision de la théorie. La pratique de 2026 montre que les résultats de débats de 3-5 agents sont les meilleurs  trop peu manque de diversité, trop peu entraînent un coût de coordination trop élevé.
## Le concept de base.

### Société des esprits (Du et al., ICML 2024)

>  **【类比】**多 Agent 辩论像学术同行评审:你写论文(N=3 个独立作者各写一版)→ 投稿后 3 个审稿人读对方的版本写评论(R 轮交叉批评)→ 作者根据评审 修改 → 几轮后论文收──关键洞察:单个作者会自信写错(Self-Refine的群体思维),3 个独立作者挑错彼此更容易出现象──但全连接(每个读者所有者) 评审成本是O(N2) 所以会议 "area chair + reviewers" 的星形拓(hub-and-spoke),审稿人只和沟通,成本降至O(N) 

- N cas de modèle proposent indépendamment des réponses à la même question.
- Au cours des tours R, chaque modèle lit les propositions des autres et les critique.
- Les modèles mettent à jour leurs réponses en fonction des critiques.
- Après R, retournez la réponse convergente.

Les expériences originales ont utilisé N=3, R=2 en raison du coût. La précision s'améliore avec plus d'agents et plus de tours sur des problèmes difficiles (MMLU, GSM8K, Validité de mouvement des échecs, génération de biographie).

> Débat multi-agent en permettant à plusieurs agents de poser la même question et de débattre de points de vue différents pour améliorer la qualité de la réflexion. Cette méthode s'avère mieux que celle d'un seul agent sur des tâches de réflexion complexes.

Les combinaisons de modèles croisés ont battu les débats de modèles uniques: ChatGPT + Bard ensemble > soit seul.

> 跨模型组合胜过单一模型辩论:ChatGPT + Bard un débat meilleur que tout seul

> Débat multi-agent en permettant à plusieurs agents de poser la même question et de débattre de points de vue différents pour améliorer la qualité de la réflexion. Cette méthode s'avère mieux que celle d'un seul agent sur des tâches de réflexion complexes.

### Topologie de la séparité

" Améliorer le débat multi-agent avec la topologie de communication Sparse " (arXiv:2406.11776, 2024-2025) a montré que le débat complet n'est pas toujours optimal. Les topologies Sparse (étoile, anneau, hub-et-spoke) peuvent correspondre à la précision à un coût de jeton inférieur. Chaque débatteur ne voit qu'un sous-ensemble de pairs.

> " Améliorer le débat multi-agents avec la topologie de la communication Sparse " (ArXiv:2406.11776, 2024-2025) montre que le débat complet n'est pas toujours le meilleur.

> Débat multi-agent en permettant à plusieurs agents de poser la même question et de débattre de points de vue différents pour améliorer la qualité de la réflexion. Cette méthode s'avère mieux que celle d'un seul agent sur des tâches de réflexion complexes.

Les conséquences:

- N=5, R=3 = 5 × 3 = 15 propositions, chaque lecture de 4 pairs = 60 critiques.
- Star N=5, R=3 (un centre + 4 spokes) = 15 propositions, les spokes lisent seulement le centre = 12 critiques.

### Quand le débat aide

- **Factuality.**N'ayant pas de propositions indépendantes, la vérification croisée réduit les hallucinations.
- **Rule-following.**Validité du mouvement d'échecs  un modèle manque une règle, d'autres la prennent.
- **Open-ended reasoning.**Plusieurs cadres restent à la bonne réponse.

### Quand le débat fait mal

- **Latency-sensitive UX.**Les tirs en série N × R sont une latence que vous ne pouvez pas avoir.
- **Cost-sensitive scale.**N × R par requête.
- **Simple factual lookups.**Une recherche est moins chère que cinq débats.

### 2026 des instances pratiques

- **Anthropic orchestrator-workers**(Létion 12)  une variante du débat avec une étape de synthèse.
- **LangGraph supervisor**(Létion 13)  routeur central + agents spécialisés peuvent mettre en œuvre le débat comme un nœud.
- **OpenAI Agents SDK**Les agents se déplacent en avant et en arrière pour une critique itérative.
- **Multi-agent evals** Débat par paire + évaluateur-optimisateur pour le signal d'évaluation.

### Où ce modèle va mal

> 🤔 **【困惑】**Q: Le débat est-il vraiment utile à quel moment? Le retard et le coût de la N×R semblent très élevés ? A: Il suffit de l'utiliser dans le scénario " un seul modèle d'erreur coûte bien plus cher que le coût du débat " .

- **Convergence collapse.**Tous les agents convergent sur la première mauvaise réponse, et l'atténuent avec les tirs nécessaires.
- **Hub failure.**Dans une topologie stellaire, un mauvais hub corrompt tout le monde.
- **Prompt homogenization.**Tous les agents utilisent le même prompt; ils produisent les mêmes réponses.

> **收敛崩溃。**Tout agent a reçu la première erreur de réponse.
> **中心故障。**Dans le monde de la planète, un mauvais centre contaminera tous les habitants.
> **提示同质化。**Les agents utilisent les mêmes suggestions; produisent les mêmes réponses.

## Construisez-le et mettez-le en œuvre.

> ️ **【易错点】**场景: développeurs utilisent le même prompt 起了 5 débatteurs 实例期待"多样化观点" → 后果:5 个实例给出几乎相同的答案 (甚至相同的错误),辩论沦为N 倍成本的自我清洗,这叫"快速同化" → 修复:要么用不同模型(GPT-4o + Claude + Gemini,异构带来真分歧),要么给每个辩论者不同角色 (((快速"你是怀疑论者""你是乐观派""你是细节核查员"),要么至少随机化温度──论文 ChatGPT + Bard 组合胜过单模型就是这个道理──
```figure
debate-converge
```

## Faites-le

`code/main.py`Il met en œuvre le débat de la Sdlib:

- `Debater`classe (MLL écrit avec dérive d'opinion par débatteur).
- `FullMeshDebate`et `SparseDebate`Les coureurs.
- Trois questions: une factuelle, une fondée sur des règles, une raison.
- Mesures: réponse convergente, ronde à convergence, opération critique totale.

- Je vais le faire.

```
python3 code/main.py
```

Résultats: précision et coût par protocole; correspondances rares en pleine maillage sur 2/3 des questions à moindre coût.

> 输出: précision et coût de chaque accord; rarement étendu sur 2/3 des questions pour un coût plus bas de correspondance de la connexion complète.

> Débat multi-agent en permettant à plusieurs agents de poser la même question et de débattre de points de vue différents pour améliorer la qualité de la réflexion. Cette méthode s'avère mieux que celle d'un seul agent sur des tâches de réflexion complexes.

## Utilisez-le avec le cadre de réalisation

- **Anthropic orchestrator-workers**Pour les débats simples de deux ou trois travailleurs.
- **LangGraph**Il est important de prendre en compte les mesures prises pour que les États puissent se soumettre à un débat multilatéral avec un contrôle.
- **Custom**pour la recherche ou des garanties de précision spécialisées.

## Envoyez-le . Produit .

`outputs/skill-debate.md`Les règles de convergence sont les mêmes que celles de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition de la définition.

> `outputs/skill-debate.md`La mise en place d'un système de régulation multi-agent

> Débat multi-agent en permettant à plusieurs agents de poser la même question et de débattre de points de vue différents pour améliorer la qualité de la réflexion. Cette méthode s'avère mieux que celle d'un seul agent sur des tâches de réflexion complexes.

## Les exercices

1. Mettre en œuvre une règle de " désaccord forcé ": au cours du premier cycle, chaque débatteur doit présenter une proposition distincte.
  Le mot "exercer" est traduit par "exercer".
2. Ajouter une aggregation pondérée par confiance: les débatteurs retournent (réponse, confiance); l'agrégateur pondère par confiance.
  Le mot "exercer" est traduit par "exercer".
3. Un "agent" est échangé contre un LLM avec des opinions différentes.
  Le mot "exercer" est traduit par "exercer".
4. Mesurez le coût des jetons pour la masse totale contre la masse rare sur vos 3 questions.
  Le mot "exercer" est traduit par "exercer".
5. Lisez le journal de la Société des esprits.
  Le mot "exercer" est traduit par "exercer".

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Debate | "Multi-agent critique" | N proposers, R rounds of cross-critique, converge |  |
| Full mesh | "Everyone reads everyone" | Every debater reads every peer each round |  |
| Sparse topology | "Limited peer view" | Debaters read only a subset of peers |  |
| Hub-and-spoke | "Star topology" | One central debater, N-1 spokes read only the hub |  |
| Convergence | "Agreement" | Debaters converge on a shared answer |  |
| Society of Minds | "Du et al. debate paper" | ICML 2024 multi-agent debate method |  |

## Encore une lecture

- [Du et al., Society of Minds (arXiv:2305.14325)](https://arxiv.org/abs/2305.14325) débat canonique multi-agent
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Sparse Communication Topology (arXiv:2406.11776)](https://arxiv.org/abs/2406.11776) résultats de topologie rares
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) les travailleurs-orchestre en tant que variante de débat
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) contrepartie autocritique de modèle unique
  Le mot "réfléchisseur" est traduit par "réfléchisseur".
