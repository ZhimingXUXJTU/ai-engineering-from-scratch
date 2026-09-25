# Cache rapide et de contexte Cache 提示缓存与上下文缓存

> Votre système de mise en cache est de 4000 jetons. Votre contexte RAG est de 20.000 jetons. Vous envoyez les deux avec chaque demande. Vous payez également pour les deux  à chaque fois. Le caching rapide permet au fournisseur de garder ce préfixe chaud de son côté et vous facture 10% du taux normal sur la réutilisation.

> **【中文解读】**系统提示4000代币 + RAG 上下文20000代币, chaque demande doit être payée. 提示缓存让供应商保留前,重用时只收取10%费――正确使用可降低50-90%推理成本和40-85%首token延迟――

> **【拓展：提示缓存→RAG生产优化】**Le caching rapide et la réponse caché de l'OpenAI sont des techniques clés pour réduire les coûts du système de production RAG, en particulier avec des suggestions de système fixe et des recherches massives sur les scénarios suivants:

>  **【前置】**Pour les autres, il est nécessaire de prendre en compte les données de l'équipe de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 01 (Prompt Engineering), Phase 11 · 05 (Context Engineering), Phase 11 · 11 (Caching and Cost) | **前置知识:** Phase 11 · 01 (提示工程)、05 (上下文工程)、11 (缓存与成本)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Le problème , l' introduction du problème

Un agent de codage envoie le même message de 15 000 jetons à Claude à chaque tour de conversation.$3/M input tokens is $0,90 en entrée coût seul  avant l'un des messages réels de l'utilisateur. Multipliez par 10 000 conversations quotidiennes et la facture atteint 9 000 $ / jour pour le texte qui ne change jamais.

> Un programmeur agent envoie les mêmes 15 000 jetons à Claude pendant chaque conversation.$3/M 输入 token，仅输入成本就是 $0,90 ne comprend pas les messages réels des utilisateurs.

Vous ne pouvez pas réduire le prompt sans nuire à la qualité. Vous ne pouvez pas éviter de l'envoyer  le modèle a besoin de lui à chaque tournant. La seule étape est d'arrêter de payer le prix complet pour un préfixe que le fournisseur a déjà vu.

> Vous ne pouvez pas réduire la quantité de la proposition sans nuire à la qualité. Vous ne pouvez pas éviter de l'envoyer.

>  **【类比】**Rapidement mis en cache 像"快递公司记住你的常用地址"第一次发货要详细说明"北京市朝阳区...",之后每次发货只需说"老地方",快递公司自动调出地址──技术上: fournisseur de mettre le préfixe KV cache 存在自己的服务器,下次请求来时直接复用,不需要重新计算注意的 K/V矩阵──对用户透明你只需在API调用加个`cache_control`Je suis en train de vous parler.

> ️ **【易错点】**Le caching rapide de 3 个坑:**prefix 顺序敏感**cache 命中要求前形 完全相同(包括空格、换行),système prompt 末尾多一个空格就错过;务必把可变部分(user输入)放最后。(2) **cache TTL 5 分钟**Anthropic 默认 5 分钟过期,没流量时 cache 失效; avec TTL prolongé(1 小时)保住冷启动场景──(3) **没监控命中率** ne savent pas le taux de réussite  ne peuvent pas juger les résultats;`cache_creation_input_tokens`et `cache_read_input_tokens`, enregistré jusqu'à la carte de contrôle.

Cette décision est la mise en cache rapide. Anthropic l'a expédié en août 2024 (avec une variante TTL prolongée de 1 heure en 2025), OpenAI l'a automatisé plus tard cette année-là, Google a expédié la mise en cache explicite de contexte aux côtés de Gemini 1.5, et les trois l'offrent maintenant comme une fonctionnalité de première classe sur leurs modèles frontaliers.

> Cette méthode est de suggérer le cache. Anthropic l'a lancé en août 2024 et OpenAI l'a automatisé plus tard cette année. Google a lancé une mise à jour de cache en ligne à Gemini 1.5.


> **【中文解读】**La valeur du caching rapide dépend du système de caching rapide (en général, 5K+ tokens) et ne change pas dans toutes les demandes.


## Le concept de base.

> **【中文解读】**Le caching rapide utilise les caractéristiques du logiciel de calcul de la loi. Si plusieurs demandes partagent le même prompt, on peut cacher le KV-cache de la première, éviter de répéter le calcul.

> **【拓展：Prompt Caching 的成本节省】**Le caching rapide d'Anthropic va répéter les entrées précédentes et réduire le coût d'environ 90%.$0.50/M tokens（原价 $5) ・ pour les jetons 5K + une moyenne de 10 fois de reprise, le coût de la mise en service est réduit d'environ 75%


![Prompt caching: write once, read cheap](../assets/prompt-caching.svg)

**The mechanic.**Lorsque le préfixe d'une demande correspond à celui d'une demande récente, le fournisseur sert le cache KV de la mise en œuvre précédente au lieu de recoder les jetons. Vous payez une petite prime d'écriture la première fois et une grande réduction de lecture chaque fois après.

> **机制。**Lorsque le pré-emport de la demande est correspondu à celui de la dernière demande, le fournisseur offre une cache KV au cours de la dernière opération, au lieu de recoder le jeton.

**Three provider flavors in 2026.**

| Provider | API style | Hit discount | Write premium | Default TTL | Min cacheable |
|---------|-----------|--------------|---------------|-------------|---------------|
| Anthropic | Explicit `cache_control` markers on content blocks | 90% off input | 25% surcharge | 5 min (extendable to 1 hour) | 1,024 tokens (Sonnet/Opus), 2,048 (Haiku) |
| OpenAI | Automatic prefix detection | 50% off input | none | Up to 1 hour (best-effort) | 1,024 tokens |
| Google (Gemini) | Explicit `CachedContent` API | Storage-billed; read at ~25% of normal | Storage fee per token·hour | User-set (default 1 hour) | 4,096 tokens (Flash), 32,768 (Pro) |

**The invariant.**Si un jeton diffère entre les requêtes, tout après le premier jeton diffère est une erreur.

> **不变量。**Les trois sont seulement en cache avant. Si entre les requêtes il y a un symbole différent, le premier symbole différent, tout le contenu est ensuite non résolu.

### L' aménagement convivial au cache

```
[system prompt]          <-- cache this
[tool definitions]       <-- cache this
[few-shot examples]      <-- cache this
[retrieved documents]    <-- cache if reused, else don't
[conversation history]   <-- cache up to last turn
[current user message]   <-- never cache (different every time)
```

Violez l'ordre  mettez le message de l'utilisateur au-dessus de la demande du système, interrompez les récupérations dynamiques entre quelques prises de vue  et le cache ne frappe jamais.

>  contre ordre  mettre les messages utilisateur sur les instructions du système, entre quelques échantillons de pénétrer  cache ne sera jamais destinée 

### Le calcul de l'équilibre

Le prix de 25% d'écriture d'Anthropic signifie qu'un bloc caché doit être lu au moins deux fois pour économiser de l'argent net. 1 écrit + 1 lire représente en moyenne 0,675x le coût par requête (économise 32%); 1 écrit + 10 lit en moyenne 0,205x (économise 80%). Règle générale: cache tout ce que vous attendez de réutiliser au moins 3 fois dans le TTL.

> En effet, les données de l'Anthropic 25% 写入溢价 signifient que les blocs de stockage doivent être lus au moins deux fois pour pouvoir nettoyer les économies.

## Construisez-le et mettez-le en œuvre.
```figure
prompt-cache-hit
```

## Faites-le

### Étape 1: Cachage des demandes anthropographiques avec des marqueurs explicites

```python
import anthropic

client = anthropic.Anthropic()

SYSTEM = [
    {
        "type": "text",
        "text": "You are a senior Python reviewer. Follow the rubric exactly.\n\n" + RUBRIC_15K_TOKENS,
        "cache_control": {"type": "ephemeral"},
    }
]

def review(code: str):
    return client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": code}],
    )
```

Le `cache_control`Le marqueur indique à Anthropic de stocker le bloc pendant 5 minutes.

> `cache_control`标记告诉人类将该块存储 5 分钟. 标记告诉人类将该块存储 5 分钟.

**Response usage fields:**

```python
response = review(code_a)
response.usage
# InputTokensUsage(
#     input_tokens=120,
#     cache_creation_input_tokens=15023,   # paid at 1.25x
#     cache_read_input_tokens=0,
#     output_tokens=340,
# )

response_b = review(code_b)
response_b.usage
# cache_creation_input_tokens=0
# cache_read_input_tokens=15023           # paid at 0.1x
```

Vérifiez les deux champs dans l' IC  si `cache_read_input_tokens`reste à zéro sur les demandes, vos clés de cache sont à la dérive.

> Dans le CI, vérifier ces deux paragraphes si`cache_read_input_tokens`Dans plusieurs demandes, gardez votre clé de stockage en mouvement.

### Étape 2: TTL prolongé d'une heure

Pour les travaux de longue durée, le délai de 5 minutes expire entre les travaux.`ttl`- Le numéro de la liste:

```python
{"type": "text", "text": RUBRIC, "cache_control": {"type": "ephemeral", "ttl": "1h"}}
```

Le TTL d'une heure coûte deux fois la prime d'écriture (50% par rapport à la valeur de base au lieu de 25%) mais rembourse rapidement sur tout lot réutilisant le préfixe plus de 5 fois.

> Le prix d'écriture de 1 heure TTL est de 2 fois plus élevé que 50% du prix de base et non de 25%), mais il est très rapide de revenir en arrière dans les opérations de rechange de plus de 5 fois avant la reprise.

### Étape 3: Mise en cache automatique d'OpenAI

OpenAI ne vous donne rien à configurer. Tout préfixe de plus de 1.024 jetons qui correspond à une demande récente obtient automatiquement une réduction de 50%.

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},   # long and stable
        {"role": "user", "content": user_msg},
    ],
)
resp.usage.prompt_tokens_details.cached_tokens  # the discounted portion
```

La même règle de mise en page de cache est applicable.`user`champ (utilisé comme composant de clé cache) et outils de réorganisation.

> Les deux choses tuent le caching d'OpenAI et ne tuent pas l'anthropique:`user`字段和重新排序工具──

### Étape 4: Cachage explicite du contexte de Gémeaux

Gemini traite le cache comme un objet de première classe que vous créez et nommez:

```python
from google import genai
from google.genai import types

client = genai.Client()

cache = client.caches.create(
    model="gemini-3-pro",
    config=types.CreateCachedContentConfig(
        display_name="rubric-v3",
        system_instruction=RUBRIC,
        contents=[FEW_SHOT_EXAMPLES],
        ttl="3600s",
    ),
)

resp = client.models.generate_content(
    model="gemini-3-pro",
    contents=["Review this code:\n" + code],
    config=types.GenerateContentConfig(cached_content=cache.name),
)
```

Gemini charge le stockage par token·heure aussi longtemps que le cache dure et lit à ~25% du taux d'entrée normal. C'est la bonne forme lorsque vous réutilisez le même prompt géant sur plusieurs sessions sur plusieurs jours.

> Gemini 按缓存存活期间每代币·小时收取存储费,读取费率约为正常输入的25%──当你在多次会议中跨天重复使用相同的大型提示时,这是正确的选择──

### Étape 5: Mesurer le taux de production

Regardez !`code/main.py`Pour un comptable simulé de trois fournisseurs qui suit le calcul de l'écriture/lecture/mal et calcule le coût mixte par 1K de demandes.

> Je vous en prie .`code/main.py`获取模拟的三供应商会计师,跟踪写入/读取/未命中计数并计算每千请求的混合成本──按目标命中率门控部署多数生产 预热后应见 >80% 读取比例──

## Des pièges qui vont encore arriver en 2026

> L'année 2026 est toujours en ligne:

- **Dynamic timestamps at the top.** `"Current time: 2026-04-22 15:30:02"`chaque requête est ratée. déplacer les timestamps en dessous du point de rupture du cache.
  **顶部的动态时间戳。**系统提示顶部放 `"Current time: 2026-04-22 15:30:02"`                                                                                                                                                                                                                                                              
- **Tool reordering.**La sérialisation des outils dans un ordre stable  un réarrangement dicté entre les déploiements casse chaque coup.
  **工具重排序。**Pour établir l'ordre de la mise en place des outils de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes de répartition des programmes.
- **Free-text near-duplicates.**"Vous êtes utile". vs "Vous êtes un assistant utile".  une différence de 1 octet = total.
  **自由文本近似重复。**"Vous êtes utile". vs "Vous êtes un assistant utile".
- **Too-small blocks.**Anthropic impose un plancher de 1.024 jetons (2 048 pour Haiku).
  **过小的块。**L'anthropologie 强制 1,024 jetons 下限(Haiku 为 2,048)。更小的块静默不缓存。
- **Blind cost dashboards.**Divisez les "tokens d'entrée" en caché et non caché. Sinon, une baisse de trafic ressemble à une victoire caché.
  **盲目的成本仪表板。**Pour les autres, le "porting token" est décomposé en cache versus non cache.

## Utilisez-le avec le cadre de réalisation

La pile de mise en cache de 2026:

> 2026 缓存技术:

| Situation | Pick |
|-----------|------|
| Agent with stable 10k+ system prompt, many turns | Anthropic `cache_control` with 5-min TTL |
| Batch job reusing a prefix for 30+ minutes | Anthropic with `ttl: "1h"` |
| Serverless endpoints on GPT-5, no custom infra | OpenAI automatic (just make your prefix stable and long) |
| Multi-day reuse of a giant code/doc corpus | Gemini explicit `CachedContent` |
| Cross-provider fallback | Keep the cacheable prefix layout identical across providers so any hit works |

| 场景 | 选择 |
|------|------|
| Agent 有稳定 10k+ 系统提示、多轮 | Anthropic `cache_control` 配 5 分钟 TTL |
| 批处理重用前缀 30+ 分钟 | Anthropic 配 `ttl: "1h"` |
| GPT-5 上的无服务器端点、无定制基建 | OpenAI 自动（让前缀稳定且够长） |
| 多天重用大型代码/文档语料 | Gemini 显式 `CachedContent` |
| 跨提供商回退 | 跨提供商保持可缓存前缀布局一致，任何命中都工作 |

Combiner avec le caching sémantique (phase 11 · 11) pour la couche de message utilisateur: manches de caching prompt *reutilisation identique aux jetons*, manches de caching sémantique *reutilisation identique aux significations*.

> Avec le langage de cache (phase 11)

## Envoyez-le . Produit .

- Ça va .`outputs/skill-prompt-caching-planner.md`- Le numéro de la liste:

```markdown
---
name: prompt-caching-planner
description: Design a cache-friendly prompt layout and pick the right provider caching mode.
version: 1.0.0
phase: 11
lesson: 15
tags: [llm-engineering, caching, cost]
---

Given a prompt (system + tools + few-shot + retrieval + history + user) and a usage profile (requests per hour, TTL needed, provider), output:

1. Layout. Reordered sections with a single cache breakpoint marked; explain which sections are stable, which are volatile.
2. Provider mode. Anthropic cache_control, OpenAI automatic, or Gemini CachedContent. Justify from TTL and reuse pattern.
3. Break-even. Expected reads per write within TTL; net cost vs no-cache with math.
4. Verification plan. CI assertion that cache_read_input_tokens > 0 on the second identical request; dashboard split by cached vs uncached tokens.
5. Failure modes. List the three most likely reasons the cache will miss in this setup (dynamic timestamp, tool reorder, near-duplicate text) and how you will prevent each.

Refuse to ship a cache plan that places a dynamic field above the breakpoint. Refuse to enable 1h TTL without a reuse count that makes the 2x write premium pay back.
```

## Les exercices

1. **Easy.**Faites une conversation de 10 tours avec un système de 5000 jetons contre Claude.`cache_control`Rapporte le projet de loi de jeton d'entrée pour chacun.
   Prenez une conversation de 10 tours et 5000 jetons 系统提示,不使用和使用 `cache_control`Répondre à la demande de l'équipe de formation
2. **Medium.**Écrivez un harnais de test qui, compte tenu d'un modèle prompt et d'un journal de demande, calcule le taux de réussite et les économies en dollars attendus par fournisseur (Anthropic 5m, Anthropic 1h, OpenAI automatique, Gemini explicite).
    édition d'outils de test, de formulaires de suggestions et de journaux de demandes, calcul des taux de réussite et des économies de chaque fournisseur
3. **Hard.**Construire un optimisateur de mise en page: une demande et une liste de champs marqués `stable=True/False`, réécrire la demande pour mettre un seul point de rupture de cache à la position maximale de cache-friendly sans perdre des informations.
   构建布局优化器:重写提示将缓存断点放在最大缓存友好位置──

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Prompt caching | "Makes long prompts cheap" / "让长提示变便宜" | Reusing a provider-side KV-cache for matching prefixes; 50-90% discount on repeated input tokens. | 提示缓存：重用供应商端的 KV-cache，对重复输入 token 提供 50-90% 折扣 |
| `cache_control` | "The Anthropic marker" / "Anthropic 标记" | Content-block attribute that declares "everything up to here is cacheable"; `{"type": "ephemeral"}`. | cache_control：内容块属性，声明"到这里为止的内容可缓存" |
| Cache write | "Paying the premium" / "付溢价" | The first request that populates the cache; billed at ~1.25x input rate on Anthropic, free on OpenAI. | 缓存写入：第一次填充缓存的请求 |
| Cache read | "The discount" / "折扣" | Subsequent requests matching the prefix; billed at 10% (Anthropic), 50% (OpenAI), ~25% (Gemini). | 缓存读取：匹配前缀的后续请求 |
| TTL | "How long it lives" / "存活时间" | Seconds the cache stays warm; Anthropic 5m default (extendable 1h), OpenAI best-effort up to 1h, Gemini user-set. | TTL：缓存保持活跃的秒数 |
| Extended TTL | "1-hour Anthropic cache" / "1小时缓存" | `{"type": "ephemeral", "ttl": "1h"}`; 2x write premium but worth it for batch reuse. | 扩展 TTL：1 小时缓存，2 倍写入溢价 |
| Prefix match | "Why my cache missed" / "为什么缓存未命中" | Caches only hit when every token from the start up to the breakpoint is byte-identical. | 前缀匹配：缓存只在从开头到断点的每个 token 完全相同时才命中 |
| Context caching (Gemini) | "The explicit one" / "显式缓存" | Google's named, storage-billed cache object; best for multi-day reuse of large corpora. | 上下文缓存 (Gemini)：命名、按存储计费的缓存对象 |

## Encore une lecture

- [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) `cache_control`Une heure TTL, des tables de réparation.
  L'équipe de gestion de la gestion des données et de la gestion des données
- [OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) correspondance automatique des préfixes.
  Ouvrir une liste de l'équipe de rédaction
- [Google — Context caching](https://ai.google.dev/gemini-api/docs/caching) `CachedContent`API et prix de stockage.
  Google 上下文缓存文档CachedContent API 和存储定价──
- [Anthropic engineering — Prompt caching for long-context workloads](https://www.anthropic.com/news/prompt-caching) poste de lancement original avec numéros de latence.
  Les données de l'équipe de recherche de l'entreprise sont disponibles en ligne.
- Phase 11 · 05 (ingénierie du contexte)  où couper le prompt pour que le cache puisse atterrir.
  Le projet de réforme de la politique de l'emploi est en cours de réalisation.
- Phase 11 · 11 (Cachage et coût)  couples de mise en cache avec un cache sémantique sur les messages utilisateurs.
  Section 11 阶段 · 11(缓存与成本)  will suggest缓存与用户消息的语义缓存配对──
- [Pope et al., "Efficiently Scaling Transformer Inference" (2022)](https://arxiv.org/abs/2211.05102) le modèle de mémoire KV-cache qui invite à la mise en cache expose aux utilisateurs; explique pourquoi un préfixe en cache est ~ 10 fois moins cher à relire que à recomputer.
  Expliquer pourquoi le cache est moins cher que le KV-cache
- [Agrawal et al., "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills" (2023)](https://arxiv.org/abs/2308.16369) préfill est le raccourci de mise en cache de phase rapide; ce document explique pourquoi le TTFT diminue considérablement sur le cache frappé alors que le TPOT n'est pas affecté.
  Expliquer pourquoi la TTFT a diminué de façon spectaculaire et la TPOT n'a pas été affectée
- [Leviathan et al., "Fast Inference from Transformers via Speculative Decoding" (2023)](https://arxiv.org/abs/2211.17192) le caching rapide se trouve aux côtés du décoding spéculatif, de l'attention flash et de la MQA/GQA comme leviers qui plient la courbe des coûts d'inférence; lisez ceci pour les trois autres.
  提示缓存与投机解码、Flash Attention 和 MQA/GQA 并列的推理成本曲线杆──
