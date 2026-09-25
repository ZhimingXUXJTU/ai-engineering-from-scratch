# La compréhension vidéo longue dans le contexte de millions de tokens

> Une vidéo 4K d'une heure à 24 FPS, parchée et intégrée, produit l'ordre de 60 millions de jetons. Un épisode de podcast de 2 heures transcrit est de 30 000 jetons. Un long métrage complet Blu-ray, même comprimé avec un pooling agressif, est de centaines de milliers de jetons. Le Gemini 1.5 de Google (mars 2024) a ouvert cette ère avec un contexte de 10 millions de jetons, faisant un rappel fiable de l'aiguille dans un paquet de foin sur des vidéos d'une heure. LWM (Liu et coll., février 2024) a montré la trajectoire d'échelle de l'attention des anneaux. LongVILA et Video- XL ont augmenté leur ingestion. VideoAgent a échangé le contexte brut pour la récupération agentique. Chaque approche est un compromis différent sur la complexité de l'informatique, du rappel et de l'ingénierie. Cette leçon les lit côte à côte.

> **【中文解读】**1 小时 4K 视频可产生约6000.000代币,远超任何模型的上下文窗口。处理长视频有三条路径:(1) 暴力上下文(Gemini 1.5千万代币上下文);(2) Ring Attention 跨设备分布式注意力;(3) Token 压缩(Video-XL 摘要代币);(4) Agent 检索(VideoAgent va regarder la vidéo lors de la recherche de la base de données) ⋅ Chaque chemin a une différence de taille en quantité de calcul, de résultat et de complexité de l'architecture.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, needle-in-haystack simulator + agentic-retrieval router) | **语言:** Python（标准库，大海捞针模拟器 + Agent 检索路由器）
**Prerequisites:** Phase 12 · 17 (video temporal tokens) | **前置知识:** Phase 12 · 17（视频时间 token）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**Je vous invite à prendre le temps de faire des recherches sur la façon de faire le travail.
>  **【类比】**长视频理解 = "看完整部电影后能回答细节"──三种策略:(1) Gemini 1.5 路线 = 把整部电影硬塞进脑子(10M token 上下文,硬件怪兽);(2) Video-XL 路线 = 看完写摘要+检索原始片段(token 压缩);(3) VideoAgent 路线 = 当数据库查,问题导向地拉取相关段段(Agent 检索) ~~

## Objectifs d'apprentissage

- Calculer le nombre total de jetons visuels pour la vidéo longue format à des FPS et des pools variables.
  Le nombre total de fichiers vidéo est de 12 à 15 fois plus élevé que le nombre total de fichiers vidéo.
- Expliquez les trois voies d'échelle: contexte brut (Gemini 1.5), attention aux anneaux (LWM), compression des jetons (LongVILA / Video-XL).
  Le mot "réfléchisseur" est le mot de passe de la langue française.
- Comparer les VLM vidéo contextuelle brute contre les VLM vidéo de récupération agencée (VideoAgent) sur la précision et la latence.
  Comparer avec le premier vidéo VLM et l'agent 检索视频 VLM(VideoAgent)
- Conçuez un test à l'aiguille dans un paquet de foin pour une vidéo de 30 minutes et mesurez le rappel à une minute spécifique.
  Traduction anglaise: pour 30 minutes vidéo design

## Le problème , l' introduction du problème

Un seul cadre de patches de taille Qwen2.5VL à 384 résolution native est de ~ 729 jetons. À 3x3 pooling, c'est 81 jetons par cadre. Un clip de 30 minutes à 1 FPS = 1800 images = 145.800 jetons. Faible d'ici 2025, VLMs ouverts, serrés. À 2 FPS, 291.600 jetons  ne conviennent que aux plus grands contextes.

> Qwen2.5-VL Grosseur de patch en 384 sous résolution originale environ 729 jetons──3x3 池化后每 81 jetons──30 分钟片段 1 FPS = 1800  = 145.800 jetons,2025 An open VLM

Un film de 2 heures à 1 FPS est de 583k jetons. Au-delà de la plupart des modèles ouverts de 2026; nécessite Gemini 2.5 Pro ou un regroupement plus agressif.

> 2 小时电影 1 FPS est 583k token── dépassant la capacité de la plupart des modèles ouverts de 2026; nécessite Gemini 2.5 Pro ou plus activée de la batterie──

Trois sentiers d'escalade sont apparus.

> Il y a eu trois élargissements de la route.

## Le concept de base.

> **【中文解读】**长视频理解(百万代币 级别) est une défi de l'IA à plusieurs modèles.

> **【拓展：Gemini 1.5 Pro 的百万 token 上下文**Gemini 1.5 Pro  supporte 1M de jetons  input, peut traiter environ 1 heure de vidéo ou 1000 pages de documents ⋅ par raré attention ⋅ seulement attention liée ⋅) et partage de bloc de traitement ⋅ dans la longueur de la vidéo ⋅ QA ⋅ mission, le taux de précision de Gemini 1.5 Pro est plus lent avec la longueur de la vidéo, mais il y a encore une différence significative avec l'homme ⋅


### Voie 1: contexte brut (Gemini 1.5, Claude Opus)

Jetez du matériel au problème, étalonnez le contexte à des millions de jetons, traitez tout en une seule passe.

> Utiliser des outils pour résoudre les problèmes de violence.

Gemini 1.5 Pro est lancé avec 1M de jetons; Gemini 1.5 Ultra à 10M; Gemini 2.5 Pro en 2026 fait des heures de vidéo de manière fiable.

> Gemini 1.5 Pro avec 1M de jetons  lancé; Gemini 1.5 Ultra  étendu à 10M; Gemini 2.5 Pro en 2026 peut être traitée de manière fiable nombre d'heures de vidéo ⋅ article enregistré un taux de récupération de 99.7% de la prise de poids de la grande mer dans la gamme de 9.5M de jetons ⋅

Ingénierie: une mise en œuvre d'attention personnalisée avec hiérarchie de mémoire (local + global + rare) plus un routage par expert MoE pour une efficacité de long contexte.

> 工程实现: self-definition attention mechanisme,带有内存级别(局部+全局+稀疏),加上 MoE 专家路由提升长上下文效率──未完整公开──非开源──

### Voie 2: Attention aux anneaux (LWM, LongVILA)

L'attention à l'anneau répartit de longues séquences entre les appareils dans un "anneau" où chaque appareil tient une pièce.

> **【中文解读】**Ring Attention distribuera la longue séquence sur plusieurs appareils, chaque appareil possédant un bloc de séquence, en calculant la longueur de la ligne de l'attention globale.

LWM (Liu et coll., 2024) a formé un modèle de contexte de 1M-token de cette façon.

> LWM(Liu 等人,2024) a utilisé cette méthode pour former 1M token 上下文模型── entraîner le calcul de la quantité avec la croissance de la ligne de basse et non la deuxième partie attention de la deuxième partie est distribuée sur les appareils en forme de ring。

LongVILA (arXiv:2408.10188) a adapté le modèle aux VLM. Vidéos de 1400 images à 192 jetons par image = 268k contexte, entraînées avec l'attention des anneaux sur le parallélisme à 8 voies.

> LongVILA va adapter ce mode à VLM──1400 视频, par 192 jetons = 268k 上下文, par 8 路并行环形注意力训练──

### Voie 3: Compression des jetons (vidéo-XL, LongVA)

Plus bon marché que le contexte brut: comprimé agressivement avant que le LLM ne voie la séquence.

> Bille violence sur la suite: en LLM  voir la séquence précédente de réaliser une intensification de la compression 

Video-XL (arXiv:2409.14485) utilise un jeton de résumé visuel: chaque clip de N cadres produit un seul jeton de "récapitulation" qui se trouve au-dessus du N. En conséquence, le LLM voit un jeton de résumé par clip, réduisant considérablement le contexte.

> Vidéo-XL Utilisation de jeton de résumé visuel: chaque N 片段 générer un jeton de résumé, faire attention à ce N  faire attention à la MLL.

LongVA étend le contexte de LLM de 200 000 à 2 millions avec une technique de "transfert de contexte long".

> LongVA utilise la technique de "长上下文迁移" pour élargir le programme de formation de 200 000 à 2 000 mètres.

La compression des jetons échange le rappel à des timestamps spécifiques pour l'évolutivité. Le modèle sait généralement ce qui s'est passé mais manque parfois des cadres exacts.

> Le coût de la compression des jetons est échangeable en échange de la capacité de diffusion des jetons à un temps déterminé.

### Voie 4: Récupération par agent (VideoAgent)

Ne pas fournir la vidéo complète au LLM. Traitez plutôt la vidéo comme une base de données et utilisez un LLM pour la consulter.

> Ne donnez pas tout le vidéo à la L.L.M. mais la donnez à la L.L.M. comme base de données.

VidéoAgent (arXiv:2403.10517):

> Je suis un homme de la famille de l'épouse.

1. LLM lit la question.
   > Le programme de formation en droit est un programme de formation en droit.
2. Le MLL demande un outil de récupération pour les clips pertinents ("montre-moi des segments avec un chat").
   > LLM 调用检索工具获取相关片段("给我看有猫的片段")
3. L'outil renvoie les timestamps correspondants.
   > 工具返回匹配的片段时间──
4. LLM lit ces clips par le biais d'un VLM.
   > LLM 通过VLM 读取这些片段──
5. Le MLL compose la réponse ou pose des questions de suivi.
   > Le MLL 生成回答或发起后续查询──

C'est le modèle LLM-as-agent appliqué à la vidéo longue.

> C'est le cas de la formation en tant qu'agent.

### Indices de référence pour l'aiguille dans un tas de foin

Le test de long-context standard: insérer un marqueur visuel ou textuel unique à un point aléatoire de la vidéo, puis poser une requête qui nécessite son rappel.

> 标准长上下文测试: insérer un seul marqueur visuel ou texte à chaque fois que vous le souhaitez dans un vidéo, puis poser une requête pour le rappel du marqueur.

Métrique: Recall@k sur la longueur de la vidéo et la position du marqueur.

> Indications: travers la longueur de la vidéo et la position du marqueur

Les modèles Open 72B (Qwen2.5-VL-72B, InternVL3-78B) obtiennent un score de ~85-90% à 30 minutes et se dégradent au-delà de 60.

> Le nombre de personnes qui ont été appelées à l'emploi est de 9 à 9%.

VideoAgent peut correspondre ou battre les modèles de contexte brut à plus de 2 heures parce que la récupération frappe l'aiguille si l'outil est bon.

> Le modèle vidéo peut être adapté ou supérieur à l'original dans les vidéos de 2 heures ou plus, car si l'outil est bon, le processus de recherche peut atteindre un objectif.

### Quelle voie choisir ?

Pour un clip de 15 minutes à la précision de la frontière: ouvrir 72B + contexte natif fonctionne généralement.

> 15 minutes 片段 追求前沿准确率: 开放 72B + 原生上下文通常可行──选 Qwen2.5-VL-72B──

Pour le contenu de 30 minutes à 1 heure: LongVILA ou Video-XL pour ouvert; Gemini 2.5 Pro pour fermé.

> 30 minutes à 1 heure contenu: ouverture à LongVILA ou vidéo-XL; ouverture à Gemini 2.5 Pro;;

Pour un contenu de plus de 2 heures: VideoAgent ou des modèles de récupération similaires.

> 2 小时以上内容:VideoAgent ou similaire à un mode de recherche.

### Modèle de production 2026

En pratique, les pipelines de production vidéo longue sont hybrides:

> En pratique, la production de films est un schéma mixte:

1. Exécutez un prélèvement dynamique en FPS + un regroupement agressif sur l'ensemble de la vidéo (obtenir une représentation globale de 100k-token).
   Le film est sorti en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en version originale en fait en version originale en version originale en version originale en version originale en fait en version originale en version originale en version originale en fait en version originale en version originale en fait en version originale en version originale en fait en version originale en fait en version originale en version originale en fait en version originale en fait en version originale en version originale en fait en version originale en fait en version originale en fait en version originale en version originale en fait en version originale en fait en version originale en fait en version originale en fait en version en fait en version en version en fait en version en version en version en fait en version en version en fait en version en version en fait en version en fait en version en version en fait en version en version en version en fait en version en version en version en version en version en libre en libre en version en version en version en version en libre en version en version en version en libre en version en version en version en version en version en version en libre en version en version en version en libre en version en version en version en version en libre en version en version en version en version en libre en version en version en version en libre en version en du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du du
2. Passez à un VLM 72B pour un résumé global.
   Le récit de la première partie de la série est le suivant:
3. Si l'utilisateur pose des questions détaillées, effectuer une recherche agentique en utilisant le résumé comme index.
   Si l'utilisateur pose des questions détaillées, utilisez le résumé comme indice de fonctionnement de l'agent 检索。

Cela combine le contexte brut pour la compréhension globale et la récupération des détails locaux.

> Il combine la compréhension globale du contexte de la violence et la capacité de recherche des détails locaux.

## Utilisez-le avec le cadre de réalisation
```figure
mm-video-token-budget
```

## Utilisez-le

`code/main.py`- Le numéro de la liste:

- Compute les budgets de jetons pour les vidéos de 1 minute à 3 heures à des FPS + pooling variables.
  Le nombre de films différé par le film est de 5 à 7 minutes.
- Simulation d'une course à l'aiguille dans un tas de foin: injection d'un marqueur à un timestamp aléatoire, pose une question, score rappel.
  Le nombre de personnes qui ont été interrogées par le médecin est de 22 à 30 ans.
- Inclut un simulateur de routeur de récupération d'agents qui choisit des clips spécifiques pour les alimenter à un VLM en aval.
  Le code de la ligne de référence est le code de la ligne de référence.

Faites le bilan et ressentez l'écart de l'échelle.

> 运行预算表, perception de la différence de taille

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-long-video-strategy-planner.md`. Compte tenu de la durée de la vidéo et de la complexité de la requête, il choisit entre le contexte brut, la compression et la récupération agencée, et calcule les attentes de latence + qualité.

> 本课产 出 `outputs/skill-long-video-strategy-planner.md`◊ étant donné la complexité de la vidéo et de la requête, il est en violence ∞ comprimé et agent ∞ entre sélection, et calculer le retard + prévision de qualité ∞

## Les exercices

1. Une conférence de 45 minutes à 1 FPS, 81 jetons par cadre. Total de jetons?

2. Conception d'un test à l'aiguille dans un tas de foin: à quelle minute vous injectez le marqueur, et quel est le format exact de la requête?

3. Comparer le contexte brut Qwen2.5-VL-72B (context 80k) à VideoAgent (Claude 3.5 + récupération) sur une vidéo de 1 heure.

4. L'attention à l'anneau coûte de mémoire de façon linéaire en longueur de séquence et en ligneur dans le nombre d'appareils. Expliquez pourquoi et ce qui échoue si vous laissez tomber la phase de rotation d'anneau.

5. Lire Gemini 1.5 Section 5 sur l'aiguille dans un paquet de foin. Qu'est-ce que le journal a trouvé sur le rappel à la limite des jetons 1M vs 10M?

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Brute context | "Just more tokens" 暴力上下文 | Scale LLM context to millions of tokens; process everything in one pass 将 LLM 上下文扩展到百万 token，一次前向传播处理全部内容 | |
| Ring attention | "LWM-style parallel" 环形注意力 | Distributed attention pattern where each device holds a chunk and rotates 分布式注意力模式，每个设备持有一块并在环中轮转 | |
| Token compression | "Summary tokens" 摘要 token | Reduce per-clip tokens via a learned compressor before the LLM LLM 前通过学习型压缩器减少每片段 token 数 | |
| Needle-in-haystack | "NIH test" 大海捞针测试 | Insert a unique marker at a random point, ask model to recall it at test time 在随机位置插入唯一标记，测试时要求模型回忆 | |
| Agentic retrieval | "LLM as query planner" Agent 检索 | LLM asks a retrieval tool for relevant clips, reads them via a VLM, composes answer LLM 调用检索工具获取相关片段，通过 VLM 阅读并生成回答 | |
| VideoAgent | "Retrieval pattern for video" 视频检索模式 | Canonical agentic-retrieval design: question -> tool -> clip -> answer 经典 Agent 检索设计：问题→工具→片段→回答 | |

## Encore une lecture

- [Gemini Team — Gemini 1.5 (arXiv:2403.05530)](https://arxiv.org/abs/2403.05530)
- [Liu et al. — LWM / RingAttention (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
- [Xue et al. — LongVILA (arXiv:2408.10188)](https://arxiv.org/abs/2408.10188)
- [Shu et al. — Video-XL (arXiv:2409.14485)](https://arxiv.org/abs/2409.14485)
- [Wang et al. — VideoAgent (arXiv:2403.10517)](https://arxiv.org/abs/2403.10517)
