# Suivi de l' état de dialogue

> "Je veux un restaurant bon marché dans le nord... en fait, faire modérer... et ajouter l'italien". Trois tours, trois mises à jour de l'état.
> "Moi veux un restaurant bon marché à l'ouest......réformé en un restaurant bon marché à l'ouest......réformé en un restaurant bon marché à l'ouest......réformé en un restaurant bon marché à l'ouest......réformé en un restaurant bon marché à l'ouest......réformé en un restaurant bon marché à l'ouest......réformé en un restaurant bon marché à l'ouest......réformé en un restaurant bon marché à l'ouest......réformé en un restaurant bon marché à l'ouest......réformé en un restaurant bon marché à l'ouest......réformé en un restaurant bon marché à l'ouest......réformé en un restaurant bon marché à l'ouest...réformé en un restaurant bon marché à l'ouest...réformé en un restaurant bon marché à l'ouest...réformé en un restaurant bon marché à l'ouest...réformé en un restaurant bon marché à l'ouest, en un restaurant bon marché à l'ouest.

> **【中文解读】**Suivre la modification de l'état du dialogue (s)

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 17 (Chatbots), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 17（聊天机器人），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Si vous vous trompez d'une seule fente, le système prend le mauvais restaurant, charge la mauvaise carte ou fixe la mauvaise date.

> Un slot place fait l'erreur, système de réservation de la carte de visite ou de la journée de visite.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans le cadre de la construction réelle ?

Pourquoi cela importe encore en 2026 malgré les LLM: les LLM gèrent l'état simple implicitement mais échouent sur les mises à jour multi-slots complexes, les cascades de correction ("attends, fais de la 7e non de la 8e, et change l'heure à 15h"), et l'état persistant sur de longues sessions.

> Pourquoi 2026 est-il encore important: le traitement de l'LLM dans un état simple mais dans un état complexe de nombreuses tranches de mise à jour, de rectification de la classe de connexion, etc., le changement de 7 n'est pas 8 n°, le changement de temps n'est pas de 3 heures du matin") et le changement de temps de longue durée de la réunion ont échoué.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de la conception.

**Dialogue state.**Un ensemble de paires (slot, valeur) qui capture ce que le système sait sur l'objectif de l'utilisateur à chaque tour.

> **对话状态。**Chaque année, les utilisateurs ont été invités à participer à la conférence de presse de la région de la France.

**State update.**À chaque tour, mettez à jour l'état en fonction de la nouvelle déclaration de l'utilisateur.

> **状态更新。**Chaque round de dialogue est basé sur le nouveau statut de l'utilisateur.

**Belief state.**Distribution de probabilité sur les valeurs de fente possibles. Utilisée lorsque l'utilisateur est ambigu ("un restaurant" → cuisine = Aucune, mais la croyance montre italien = 0,3, chinois = 0,2, ...).

> **信念状态。**Peut-être que la plupart des utilisateurs ont des problèmes de santé, mais la plupart des utilisateurs ont des problèmes de santé.

> **【拓展：大语言模型的工程实践】**Le GPT à ChatGPT, le NLP, a connu une transformation de la mode.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est la structure la plus populaire de l'IA de l'entreprise actuelle 应用──
```figure
n5-slot-tracker
```

## Faites-le

> **【拓展：NLP 的多语言挑战】**Dans le monde, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Le code est passé de zéro à zéro pour réaliser l'algorithme central.

### Étape 1: Tracker de l'état de la valeur de la fente

```python
class DialogueStateTracker:
    def __init__(self, slots):
        self.state = {slot: None for slot in slots}
        self.history = []

    def update(self, slot_values):
        for slot, value in slot_values.items():
            if slot in self.state:
                self.state[slot] = value
        self.history.append(dict(self.state))

    def get_missing_slots(self):
        return [s for s, v in self.state.items() if v is None]

    def is_complete(self):
        return all(v is not None for v in self.state.values())


tracker = DialogueStateTracker(["cuisine", "price", "area", "party_size"])
tracker.update({"cuisine": "Italian", "area": "north"})
print(tracker.get_missing_slots())  # ['price', 'party_size']
print(tracker.is_complete())  # False
```

### Étape 2: Mise à jour de l'état basée sur le LLM

```python
def llm_state_update(dialogue_history, current_state, llm):
    prompt = f"""Given the dialogue history and current state, extract slot updates.

Current state: {current_state}
Dialogue: {dialogue_history[-1]}

Output JSON of updated slots."""
    return llm(prompt)
```

> **【中文解读】**Ce chapitre montre comment utiliser un cadre mature pour appliquer rapidement cette technologie.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL.

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**Le présent article se concentre sur la façon dont le modèle sera déployé pour les produits disponibles.

- **Rule-based DST.**Remplissage de fente avec extraction d'entité. Rapide, prévisible. / 基于规则的DST──正则 + 实体提取──快速、可预测──
- **Neural DST.**Prenez le train sur MultiWOZ ou un ensemble de données similaire.
- **LLM-based DST.**Faire appel à la maîtrise de droit pour extraire des mises à jour de l'état.
- **Hybrid.**LLM pour l'extraction + base de règles pour la validation. recommandation de production. / 混合。LLM 提取 + 规则验证。生产推──

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-dst-builder.md`- Le numéro de la liste:

> 保存为 `outputs/skill-dst-builder.md`- Le numéro de la liste:

```markdown
Given a task-oriented dialogue system, design DST.
1. Slots to track.
2. State update method (rule, neural, LLM).
3. Confirmation and correction handling.
```

## Les exercices

1. **Easy.**Construire un système de réservation de restaurants basé sur des règles. / **简单。**Pour le système de réservation de restaurants construit sur la base des règles du DST.
2. **Medium.**Ajouter l'extraction d'État basée sur le LLM. Comparer à la base de règles. / **中等。**添加基于LLM's status提取──
3. **Hard.**Évaluer le DST sur MultiWOZ. Rapporter l'exactitude des objectifs communs. / **困难。**Dans le cadre de la mise en œuvre de la politique de sécurité,

## Les termes clés

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dialogue state（对话状态） | Current (slot, value) pairs. / 当前槽位-值对。 |
| Slot filling（槽位填充） | Extracting values for predefined slots. / 为预定义槽位提取值。 |
| Belief state（信念状态） | Probability distribution over slot values. / 槽位值的概率分布。 |
| MultiWOZ | Multi-domain dialogue dataset. / 多领域对话数据集。 |

## Encore une lecture

- [MultiWOZ](https://arxiv.org/abs/1810.00278) ensemble de données standard DST. / 标准 DST 数据集──
- [TRADE](https://arxiv.org/abs/1810.00278) Traceur d'état de dialogue transférable. / 可迁移对话状态跟踪器──
- [SimpleTOD](https://arxiv.org/abs/2005.00796) simple DST de bout en bout. / 简单端到端 DST。
