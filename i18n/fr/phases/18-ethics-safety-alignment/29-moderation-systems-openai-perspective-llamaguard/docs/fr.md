# Les systèmes de modération  OpenAI, Perspective, garde de llama  Perspective garde de llama  Audit OpenAI

> Les systèmes de modération de production mettent en œuvre les politiques de sécurité définies dans les leçons 12 à 16.`omni-moderation-latest`(2024) basé sur GPT-4o classifie le texte + les images dans un appel; 42% mieux sur le test multilingue que la version précédente; le schéma de réponse renvoie 13 catégories de booléans  harcèlement, harcèlement/menace, haine, haine/menace, illicite, illicite/violente, auto-harmage, auto-harmage/intention, auto-harmage/instructions, sexuel, sexuel/minors, violence, violence/graphique; gratuit pour la plupart des développeurs. Modèles en couches: modération des entrées (pré-génération), modération des sorties (post-génération), modération personnalisée (règles de domaine). Les appels parallèles asynchrone cachent la latence; les réponses de place-hold sur le flag. Llama Guard 3/4 (leçon 16): 14 dangers liés aux MLCommons, abus d'interprète de code, 8 langues (v3), multi-image (v4). API de perspective (Google Jigsaw): score de toxicité antérieur à la vague de la MLL en tant que modérateur; toxicité principalement à dimension unique avec des variantes de toxicité sévère/insulte/prophétie; référence pour la recherche sur la modération du contenu. Dépréciations: Modérateur de contenu Azure a été déprécié en février 2024, retiré en février 2027, remplacé par Azure AI Content Safety.

> **【中文解读】**Le présent article présente le système d'audit de contenu OpenAI Perspective、Llama Guard等 contenu de sécurité.

> **【拓展：审核栈 → 生产配置】**OpenAI et Llama Guard ont une "légitimité" comme catégories générales, Llama Guard est divisée en "crime violent" et "crime non violent"[6].

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, three-layer moderation harness) | **语言:** Python（标准库，三层审核框架）
**Prerequisites:** Phase 18 · 16 (Llama Guard / Garak / PyRIT) | **前置知识:** Phase 18 · 16 (Llama Guard / Garak / PyRIT)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Les résultats de l'étude sont les suivants:
>  **【类比】**审核系统 = "AI 服务台的保安"――OpenAI Moderation API(GPT-4o 驱动) = 一次调用分类 13 类(骚扰/仇恨/非法/自残/性/暴力等);Llama Guard 3/4(14 MLCommons 类别,多模态);Perspective API(Google Jigsaw,毒性打分,LLM 前的旧时代)。
>  三层默认配置:输入审核(pre-gen) + 输出审核(post-gen) + 自定义审核(域规则)

## Objectifs d'apprentissage

- Décrivez la taxonomie de catégorie de l'API OpenAI Moderation et la différence qu'elle présente avec l'ensemble des MLCommons de Llama Guard 3.
- Décrivez les trois modèles de couche de modération (entrée, sortie et personnalisation) et nommez un mode d'échec de chacun.
- Décrivez la position de l'API Perspective comme une ligne de base pré-LLM et pourquoi elle reste utilisée dans la recherche.
- Indiquez le calendrier de dépréciation Azure.

> Décrire la différence entre OpenAI Moderation API et le Llama Guard 3 MLCommons 集的区别── décrire le modèle d'audit à trois niveaux et un modèle de défaillance à chaque niveau── décrire la position de l'API en perspective en tant que base de la LLM── décrire Azure 弃用时间线──

## Le problème .

Les leçons 12-16 décrivent les attaques et les outils de défense. La leçon 29 couvre les systèmes de modération déployés qui fonctionnent les défenses à la surface où les utilisateurs touchent le produit.

> Les leçons 12-16  Décrire les outils d'attaque et de défense  Leçon 29  couvre le système d'audit déployé de l'opération de défense                                                                                                                                                                                                                                         

## Le concept.

> **【中文解读】**13 catégories de l'API OpenAI Moderation: harcèlement/harcèlement-menace、 haine/hatred-threat、自残/自残-意图/自残-指示、性/性-未成年人、暴力/暴力-图形、非法/非法-暴力──多模态支持适用于暴力、自残和性但不包括性-未成年人,其余仅仅文本──比上一代审核端点多语言测试集上 42%好──

### API de modération OpenAI

`omni-moderation-latest`(2024). Construit sur GPT-4o. Classifie le texte + les images en un appel. Gratuit pour la plupart des développeurs.

Catégories (13 booliens dans le schéma de réponse):
- le harcèlement, le harcèlement/la menace
- haine, haine ou menace
- L'autodestruction, l'autodestruction/l'intention, l'autodestruction/l'instruction
- sexuels, sexuels/minors
- violence, violence/graphique
- Illicite, illicite/violente

Le soutien multimodal s' applique à `violence`- Je suis là .`self-harm`, et `sexual`Mais pas !`sexual/minors`Le reste est uniquement texte.

Pour le code de la bande dans `code/main.py`Nous allons faire tomber le `/threatening`- Je suis là .`/intent`- Je suis là .`/instructions`, et `/graphic`Les codes de production devraient utiliser le schéma complet de 13 catégories.

Les résultats par catégorie; les applications fixent des seuils.

### Garde de la lame 3/4

14 catégories de risques MLCommons (organisées différemment des 13 booliens de schéma de réponse d'OpenAI). Supporte 8 langues (v3). Llama Guard 4 (avril 2025) est natifement multimodal, 12B.

Les taxonomies OpenAI et Llama Guard se chevauchent mais divergent. OpenAI a "illicite" comme une catégorie large; Llama Guard a "crimes violents" et "crimes non violents" séparément.

### API de perspective (Google Jigsaw)

Système de notation de toxicité antérieur à la vague de la LLM en tant que modérateur (avant 2020). Catégories: TOXICITÉ, SEVERE_TOXICITÉ, INSULT, PROFANITÉ, THREAT, IDENTITÉ_ATTACK. Score primaire à une seule dimension (TOXICITÉ) avec des variantes sous-dimensionnelles.

Largement utilisé comme base de recherche de modération de contenu parce que l'API est stable, documentée et a des années de données d'étalonnage. Pour les cas d'utilisation modernes LLM adjacents, Llama Guard ou OpenAI Moderation est généralement mieux adapté.

> **【中文解读】**Logique de conception du modèle de vérification à trois niveaux: l'entrée de vérification doit être terminée avant la production, l'entrée de vérification doit être terminée après la production.

### Le motif à trois couches

1. **Input moderation.**Classifier le prompt de l'utilisateur avant la génération. Rejeté si marqué.
2. **Output moderation.**Classifier la sortie du modèle avant la livraison. Remplacer par un refus si marqué.
3. **Custom moderation.**Règles spécifiques à un domaine (régex, permis, politique commerciale).

Les trois couches sont séquentielles par conception: la modération d'entrée doit être terminée avant la génération et la modération de sortie se déroule après la génération. Le parallélisme s'applique à l'intérieur d'une couche  exécutant plusieurs classifiateurs (par exemple, OpenAI Moderation + Llama Guard + Perspective) simultanément sur le même texte cachant la latence par classifiateur. En tant qu'optimisation optionnelle, une réponse placeholder ("un moment, vérification...") peut être affichée pendant que la modération d'entrée est complète et que le streaming de token-1 est reporté. Le comportement du drapeau est configurable: rejeter, désinfecter, escalader à l'examen humain.

> **【拓展：失败模式 → 为什么需要多层】**仅输入审核无法捕获输出幻觉(Létion 12-14 编码攻击绕过输入分类器);仅输出审核允许任何输入到达模型(augmenter les coûts, exposer l'attaquant à des hypothèses internes);仅自定义审核不跨类别鲁棒(正则表达式脆弱)──分层是默认安全带+吊带──

### Mode d'échec

- **Input only.**Ne capture pas les hallucinations de sortie (les attaques de codage de leçon 12-14 contournent les classifiateurs d'entrée).
- **Output only.**Permet à toute entrée d'atteindre le modèle; augmente le coût; surfaces de raisonnement interne à l'attaquant.
- **Custom only.**Les régexes sont fragiles.

La couche est par défaut.

### Dépréciation de l'azur

Modérateur de contenu Azure: dépassé en février 2024, retraité en février 2027. remplacé par Azure AI Content Safety, basé sur LLM et intégré à Azure OpenAI. La migration est un projet de niveau de terrain 2024-2027 pour les déploiements Azure.

### Là où cela s'inscrit dans la phase 18

La leçon 16 couvre les outils de modération dans le contexte de l'équipe rouge. La leçon 29 couvre la modération déployée. La leçon 30 se termine avec les preuves actuelles de capacité à double usage.

> Leçon 16 dans le contexte du red team couvre les outils d'audit. Leçon 29 couvre les contrôles déployés. Leçon 30 est terminée avec le certificat de capacité à double utilisation.

> **【拓展：Azure 迁移 → 2024-2027 行业项目】**Azure Content Moderator 2024 annonce le 2 février 2022 annonce le retrait de l'emploi en 2027, remplaçant le contenu Azure AI basé sur le LLM en matière de sécurité et d'intégration avec Azure OpenAI ⋅ Migration est un projet de niveau industriel de 2024 à 2027 ⋅ Chaque déploiement du Modérateur de contenu Azure nécessite un processus de planification de la migration ⋅ C'est une transition systémique de l'audit traditionnel du contenu vers le contrôle de l'entreprise LLM ⋅ Drive Audit ⋅

## Utilisez-le.
```figure
an-moderation-layers
```

## Utilisez-le

`code/main.py`construit un harnais de modération à trois couches: modérateur d'entrée (mot clé + score de catégorie), modérateur de sortie (même classifiateur sur la sortie), modérateur personnalisé (règles de domaine). Vous pouvez exécuter les entrées et observer quelle couche capture quoi.

> `code/main.py`构建三层审核框架:输入审核器、输出审核器、自定义审核器──你可以运行输入并观察哪一层捕获什么──

Cette leçon produit `outputs/skill-moderation-stack.md`- En raison d'un déploiement, il recommande une configuration de pile de modération: quel classifiateur à l'entrée, quel à la sortie, quelles règles personnalisées et quel juge pour les cas de bord.

> 本课产 出 `outputs/skill-moderation-stack.md` la mise en place d'un programme de révision et de révision des procédures de révision.

## Les exercices

1. On court .`code/main.py`- Faites passer une entrée bénigne, limite et nocive à travers les trois couches.

2. Élargir le harnais avec un score de toxicité de style Perspective-API pour une catégorie spécifique.

3. Lisez les documents API de modération OpenAI et la liste des catégories Llama Guard 3. Mettez chaque catégorie OpenAI dans les catégories Llama Guard les plus proches. Identifiez trois catégories qui ne sont pas nettement cartographiées.

4. Conceptez une pile de modération pour un déploiement d'assistant de code (par exemple, GitHub Copilot). Identifiez les catégories les plus et les moins pertinentes et proposez des règles personnalisées.

5. Azure Content Moderator prend sa retraite en février 2027. Planifiez une migration vers Azure AI Content Safety. Identifiez l'élément à risque le plus élevé de la migration.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| OpenAI Moderation | "omni-moderation-latest" | GPT-4o-based 13-category (text) classifier with partial multimodal support |
| Perspective API | "Google Jigsaw toxicity" | Pre-LLM-era toxicity scoring baseline |
| Llama Guard | "MLCommons 14-category" | Meta's hazard classifier (v3: 8B text, 8 langs; v4: 12B multimodal) |
| Input moderation | "pre-generation filter" | Classifier on user prompt before model call |
| Output moderation | "post-generation filter" | Classifier on model output before delivery |
| Custom moderation | "domain rules" | Deployment-specific rules (regex, allowlist, policy) |
| Layered moderation | "all three layers" | Standard production deployment pattern |

## Encore une lecture

- [OpenAI Moderation API docs](https://platform.openai.com/docs/api-reference/moderations) point final de l'omni-modération
- [Meta PurpleLlama + Llama Guard](https://github.com/meta-llama/PurpleLlama) Répôt de garde de l'armée
- [Google Jigsaw Perspective API](https://perspectiveapi.com/) Score de toxicité
- [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/) Remplacement d'Azure
