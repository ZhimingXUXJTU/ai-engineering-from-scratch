# Le caching rapide et le caching sémantique Économie  Économie  Réservation des relations publiques

> **Pricing snapshot dated 2026-04.**Les revendications numériques ci-dessous reflètent les cartes de taux des fournisseurs capturées à la publication de cette leçon; vérifiez les documents liés avant de les citer en aval.

> **【中文解读】**Ce chapitre présente les réponses à des suggestions par le biais de la mise en cache similaire pour réduire les coûts de la réflexion.


> Le caching se fait à deux niveaux. L2 (niveau fournisseur) le caching de prompt/prefix réutilise attention KV pour les préfixes répétés  Les documents de caching de prompt d'Anthropic annoncent une réduction de coût allant jusqu'à 90% et une réduction de latence de 85% sur les longues demandes; pour Claude 3.5 Sonnet, les lectures de cache sont $0.30/M vs $3,00/M frais avec un TTL de 5 minutes et une prime de rédaction de 2 fois pour l'option TTL d'une heure (docs.anthropic.com, 2026-04). Le caching rapide OpenAI s'applique automatiquement pour les instructions ≥ 1024 jetons et les prix de l'entrée caché à environ 90% de réduction par rapport au frais (platform.openai.com, 2026-04); le taux exact de caching par modèle dépend de la carte de taux en direct. L1 (app-level) cache sémantique saute le LLM entièrement sur l'intégration de hits de similitude. Vendor "95% accuracy" désigne la correction des correspondances, pas le taux de succès  les taux de succès de production rapportés vont de 10% (chat ouvert) à 70% (FAQ structurée); aucun fournisseur ne publie une ligne de base officielle, alors traitez-les comme une télémétrie communautaire plutôt que comme des garanties. Les pièges de production: la parallélisation tue le caching (N requêtes parallèles émises avant la première écriture du cache peuvent gonfler les dépenses plusieurs fois), et le contenu dynamique à l'intérieur du préfixe empêche les hits du cache entièrement. ProjectDiscovery a rapporté passer de 7% à 74% de taux de succès (2025-11) en déplaçant du texte dynamique hors du préfixe cacheable.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy two-layer cache simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang RadixAttention)
**Time:** ~60 minutes | **时间:** ~60 minutes
**Type:** Learn
**Languages:** Python (stdlib, toy two-layer cache simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 06 (SGLang RadixAttention)
**Time:** ~60 minutes

>  **【前置】**Les échanges sont les plus courants et les plus courants.
>  **【类比】**缓存 = "翻历史聊天记录"──L2 提示缓存(Anthropic/OpenAI)= 服务商帮你存储(90% 成本降,85% 延迟降);L1 语义缓存 = 自己用嵌入 找相似问题直接返回──陷:并行请求会破坏缓存、前里塞动态内容(时间)= 永远命中不了──ProjectDiscovery 把动态文本挪出可存前后,命中 7%率→74%──
> ️ **【易错点】**厂商宣传 "95% 准确率" désigne le taux de correspondance de la justesse plutôt que du succès.

## Objectifs d'apprentissage

- Distinguer le caching de prompts/préfixes L2 (reutilisation de KV chez le fournisseur) du caching sémantique L1 (bypass de LLM sur des prompts similaires).
  Le premier est le premier, qui est le premier, qui est le premier.
- Expliquez à l'anthropique `cache_control`marquage explicite et les deux options TTL (5 min contre 1 heure) avec leurs multiplicateurs de prix.
  Le mot " anthropologie " est traduit par " anthropologie ".`cache_control`显式标记和两种 TTL 选项(5 分钟对1 小时) et son prix multiplication
- Comptez les économies mensuelles attendues compte tenu du taux de succès, du mix prompt/response et des prix des jetons.
  Le taux de change est le taux de change de la valeur de l'échange.
- Nommez le modèle anti-parallélisation qui gonfle les factures de 5 à 10 fois et le modèle anti-contenu dynamique qui s'effondre taux de frappe.
  Traduction chinoise: dire que la croissance des comptes est de 5 à 10 fois plus forte que la croissance des taux de change et que les taux de change sont de 5 à 10 fois plus élevés que les taux de change.

## Le problème , l' introduction du problème

> **【中文解读】**提示缓存有两个常见失败模式:(1) 并行化反模式Agent 发发出 10 并行工具调用, toutes les demandes sont écrites dans le premier cache 完成前到达,10 次写入、0 次读取,账单膨胀 5-10x;(2) 动态内容反模式系统提示中包含当前时间、请求 ID等动态内容,每个请求都唯一,缓存中率 0%──修复方法:将静态内容放缓存前,动态内容放缓边界后──

> **【拓展：提示缓存的经济价值】**提示缓存是LLM 成本优化中最直接的杆──Anthropic 的缓存 仅阅读 仅阅读$0.30/M（Claude 3.5 Sonnet），比 fresh input $3.00/M 便宜 10x──OpenAI pour les suggestions de 1024 jetons ≥ 1024 cache automatique, les suggestions de cache sont à 10% du prix des nouvelles suggestions. Dans les systèmes RAG de production, le taux de cache moyen des suggestions du système de partage peut atteindre 60-80%, un économiser mensuel de plusieurs millions de dollars──语义缓存(L1) dans les situations structurées de FAQ peut atteindre 40-70% de taux de vie──

Vous ajoutez le caching rapide à votre service RAG. La facture reste plate. Vous mesurez le taux de succès; il est de 7%. Vos demandes semblent statiques mais elles ne le sont pas.

> **【中文解读】**
> 提示缓存分两层:L2(fournisseur级) 重用重复前的 KV cacheAnthropic 声称缓存读取成本降低90%、延迟降低85%;L1(应用级)语义缓存存在嵌入相似度命中时直接跳过LLM。

Par ailleurs, votre agent effectue 10 appels parallèles par requête utilisateur. Tous les 10 arrivent au fournisseur avant la fin de la première mise en cache. 10 écrit, zéro est lu. Votre facture est de 5 à 10 fois plus cher que ce que "avec la mise en cache" était censé coûter.

Le caching est un protocole, pas un drapeau, deux couches, deux modes de défaillance différents.

## Le concept de base.

### L2  mise en cache des prompts/préfixes du fournisseur

> **【中文解读】**L2 层(提供商级)提示缓存复用重复前的注意力 KV──Anthropique 使用显式 `cache_control`标记,TTL 选项有5分钟(写入成本 1.25x)和1 小时(2x),读取成本仅为新鲜输入的1/10──OpenAI对 ≥1024代币提示自动缓存,无需标记──Google Gemini 通过显式 API 提供语境缓存──自部署方案使用vLLM预写缓存或SGLang RadixAttention──

Le fournisseur stocke le KV d'attention pour un préfixe cacheable et le réutilise à la prochaine demande qui correspond au préfixe.

**Anthropic (Claude 3.5 / 3.7 / 4 series)**: explicite `cache_control`TTL: 5 minutes (écriture coûte 1,25x base) ou 1 heure (écriture coûte 2x base).$0.30/M on Claude 3.5 Sonnet vs $3,00/M frais  10 fois moins cher (docs.anthropic.com, à partir de 2026-2004). Les tarifs diffèrent par modèle (Opus/Haiku publié séparément); vérifiez toujours la page de prix en direct.

**OpenAI**: mise en cache automatique pour les instructions ≥1024 jetons (platform.openai.com, 2026-04). Aucun drapeau explicite. L'entrée en cache est environ 10 fois moins chère que la fraîche sur les cartes de taux gpt-4o/gpt-5 actuelles. Ni les documents ni les notes de sortie ne publient une ligne de base officielle de taux d'accident; les rapports communautaires se regroupent autour de 3060% avec une conception rapide soigneuse. Moniteur `usage.cached_tokens`Pour mesurer les vôtres.

**Google (Gemini)**: le caching de contexte via une API explicite; le caching de contexte 1M-token signifie que le caching paie encore plus.

**Self-hosted (vLLM, SGLang)**: La phase 17 · 06 couvre RadixAttention  le même schéma à votre propre calcul.

### L1  Cachage sémantique au niveau de l'application

> **【中文解读】**L1 层(应用级)语义缓存在调用 LLM 之前,对提示做哈希和嵌入查找. 如果找到相似度超过值 (通常 0.95+) 的缓存请求,直接返回缓存响应.

Avant d'appeler le LLM, faites le hash de la demande, encassez-la et recherchez une demande en cache similaire (semblance de cousin au-dessus du seuil, généralement 0,95 +).

Le code de base est le code de base de la base de données.

Les revendications de précision du fournisseur se réfèrent à la fréquence à laquelle la réponse en cache retournée était sémantiquement appropriée  et non à la fréquence de frappe.

- Chat ouvert: 10 à 15%.
- Questions fréquentes structurées / soutien: 40-70%.
- Questions de code: 20-30% (petites variantes tuent les hits).
- Agents de voix répéter des instructions: 50-80% (configuration fixe de normalisation vocale).

### Le modèle anti-parallélisation

> **【拓展：并行化反模式的真实案例】**L'expérience typique de la production:Agent vers Anthropic  Émet 10 outils de mise en ligne pour la production, partageant un seul outil de 4K-token  Système de suggestion  L'écriture de cache d'Anthropic est terminée environ 300ms, mais la requête 2-10 arrive dans la même fenêtre de millisecondes, et chacun voit le cache manquer.

Votre agent fait 10 appels d'outils en parallèle. Tous les 10 ont la même requête système 4K-token. Les écritures de cache anthropic sont par requête; la première écriture de cache se termine environ 300 ms après que le fournisseur a vu la requête. Les demandes 2-10 arrivent dans la même fenêtre de milliseconde et chacune voit le cache manquer. Vous payez 10 primes d'écriture, 0 rabais de lecture.

Correction: lot avec séquentiel-first  faire la demande 1 seul, puis le feu 2-10 une fois que le cache 1 a été peuplé. Ajout de 300 ms au premier appel de l'outil; économise 5-10x la facture.

### Le modèle anti-contenu dynamique

Votre commande de système ressemble à:

```
You are a helpful assistant. The current time is 14:32:17.
User ID: abc123. Today is Tuesday...
```

Chaque requête est unique, chaque requête écrit, nul succès.

Correction: déplacer tout ce qui est vraiment statique vers le préfixe cacheable; ajouter du contenu dynamique après la limite de cache:

```
[cacheable]
You are a helpful assistant. [rules, examples, instructions]
[/cacheable]
[dynamic, not cached]
Current time: 14:32:17. User: abc123.
```

ProjectDiscovery est passé de 7% à 74% de taux de cache de cette façon et a publié l'anatomie.

### Charge de pile + cache pour les charges de travail de nuit

Les API de lot (phase 17 · 15) offrent une réduction de 50% à la rotation de 24 heures. Les entrées cachées en haut vous donnent ~ 10 fois plus. Les charges de travail de classification, d'étiquetage et de génération de rapports peuvent diminuer de ~ 10% du coût synchrone-non-caché par stacking.

### Les chiffres que vous devriez vous rappeler

Les points de prix sont capturés 2026-04 à partir des documents des fournisseurs liés et dérivent tous les quelques mois  vérifier à nouveau avant de s'y fier.

- Lire en cache: 0,30 $/M sur Claude 3.5 Sonnet, environ 10 fois moins cher que les entrées fraîches (docs.anthropic.com).
- Prémium d'écriture de cache anthropic: 1,25x (5 min TTL) ou 2x (1 heure TTL).
- OpenAI automatique de mise en cache: s'applique aux signaux de commande ≥ 1024; entrée en cache au prix d'environ 10% de l'entrée fraîche sur les cartes de taux courants (platform.openai.com).
- Taux de succès du cache sémantique (reporté par la communauté): ~10% de chat ouvert; jusqu'à ~70% de FAQ structurées. Pas de base documentée par le fournisseur.
- ProjectDiscovery: 7% → 74% de taux de succès en déplaçant la dynamique hors préfixe (blog du projet, 2025-11).
- Anti-pattern de parallélisation: rapports typiques d'inflation de factures 510x lorsque N requêtes parallèles manquent la première cache écrire.

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**
> Le meilleur moyen de résoudre les problèmes de l'environnement est de mettre en place des modèles de données pour les utilisateurs.`cache_control`标记静态前──实测案例:把动态内容移出缓存前,命中率从7% 跳到74%── Pour les RAG 系统, 静态系统提示 + 检索到的文档属于缓存范围, les problèmes des utilisateurs ne relèvent pas──

> **【拓展：提示缓存→成本优化】**提示缓存是 LLM 成本优化最直接的手段──Anthropic Claude 的缓存读取价格为$0.30/M token，不到新鲜输入 $Pour les systèmes RAG qui traitent des millions de demandes par jour, le caching d'options peut faire baisser le montant des comptes API mensuels de centaines de milliers de dollars à des dizaines de milliers de dollars.
```figure
semantic-cache-hit
```

## Utilisez-le

`code/main.py`Les rapports de taux de rebond, facturation et montre la pénalité de parallélisation.

> `code/main.py`Les rapports de taux de rebond, facturation et montre la pénalité de parallélisation.

> `code/main.py`Les rapports de taux de rebond, facturation et montre la pénalité de parallélisation.

## Envoyez-le . Produit .

> **【拓展：缓存 + 批处理叠加优化】**L'effet de superposition de l'API de stockage et de traitement en série: API de stockage 50% de réduction + 缓存输入 ~10x de réduction = environ 10% du coût de synchronyme non stockage.

Cette leçon produit `outputs/skill-cache-auditor.md`- compte tenu du modèle et du trafic, il vérifie la cachéabilité et recommande une restructuration.

> 本课产 出 `outputs/skill-cache-auditor.md`- compte tenu du modèle et du trafic, il vérifie la cachéabilité et recommande une restructuration.

## Les exercices

1. On court .`code/main.py`- Quel est le prix de la facture ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ changement de marché ◊ augmentation du chiffre d'affaires
2. Votre commande système a une date.
   Le système de calcul est un système de calcul.
3. Calculer le break-even pour 1 heure TTL (2 fois écrit) contre 5 minutes TTL (1,25 fois écrit) compte tenu du taux d'arrivée de votre demande.
   Le taux de change est de 1,25% en moyenne.
4. Le cache sémantique à 0,95 atteint 20%. à 0,85 il atteint 50% mais vous voyez des réponses cachées incorrectes. Choisissez le bon seuil et justifiez.
   Le taux de réussite est de 0,95 %, mais vous verrez le taux de réussite de 0,95 %.
5. Vous faites 10 requêtes parallèles par requête utilisateur. Réécrivez pour la facilité de mise en cache sans ajouter de latence de bout en bout.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| L2 prompt cache | "prefix cache" | Provider stores KV for repeated prefix |
| `cache_control` | "Anthropic cache marker" | Explicit attribute marking cacheable blocks |
| Cache write premium | "write tax" | Extra cost for first miss-to-cache (1.25x or 2x) |
| L1 semantic cache | "embedding cache" | App-level hash-and-embed before calling LLM |
| GPTCache | "LLM caching lib" | Popular OSS L1 cache library |
| Cache hit rate | "hits / total" | Fraction of requests served from cache |
| Parallelization anti-pattern | "the N-write trap" | N parallel requests miss cache N times |
| Dynamic content trap | "the time-in-prompt trap" | Dynamic bytes in prefix kill hit rate |
| RadixAttention | "intra-replica cache" | SGLang's prefix-cache implementation |

## Encore une lecture

- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) officiel `cache_control`la sémantique et les TTL.
- [OpenAI Prompt Caching](https://platform.openai.com/docs/guides/prompt-caching) comportement de mise en cache automatique et admissibilité.
- [TianPan — Semantic Caching for LLMs Production](https://tianpan.co/blog/2026-04-10-semantic-caching-llm-production)
- [ProjectDiscovery — Cut LLM Costs 59% With Prompt Caching](https://projectdiscovery.io/blog/how-we-cut-llm-cost-with-prompt-caching)
- [DigitalOcean / Anthropic — Prompt Caching](https://www.digitalocean.com/blog/prompt-caching-with-digital-ocean)
