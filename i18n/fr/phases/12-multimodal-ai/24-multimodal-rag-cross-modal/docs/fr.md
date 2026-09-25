# RAG multimodal et récupération croisée de modes

> Le document RAG est une tranche. Le RAG multimodal de production est plus large  en récupérant du texte, des images, de l'audio et de la vidéo pour des flux de travail tels que la planification des voyages (" trouvez-moi un brunch végétalien tranquille avec lumière naturelle "), le triage médical (" quelle blessure correspond à cette photo + ces notes "), le commerce électronique (" tenues similaires à cette selfie, dans ma taille ") et le service sur le terrain (" diagnostiquez ce son du moteur plus la photo de la pièce "). Trois enquêtes de 2025  Abootorabi et al., Mei et al., Zhao et al.  codifier les sous-problèmes: récupération trans-modale, fusion de récupération, mise à terre de la génération, évaluation multimodale. Cette leçon lit les enquêtes et conçoit un pipeline de production.

> **【中文解读】**Le RAG dépasse le seul document de recherche  nécessite un référencement à travers le texte, les images, les sons, les vidéos, les recherches pour le planning de voyage, la clinique, les conseils de commerce électronique, les services en cours, etc. ⋅ Les trois articles de l'article définissent quatre questions: référencement à travers le modèle, référencement à fusion, génération de terrains, référencement à plusieurs modèles ⋅ évaluation ⋅ Le défi principal est la stratégie de fusion des résultats de plusieurs référencements ⋅

**Type:** Build
**Languages:** Python (stdlib, cross-modal retriever with fusion + grounded generator)
**Prerequisites:** Phase 12 · 23 (ColPali), Phase 11 (RAG basics)
**Time:** ~180 minutes

>  **【前置】**Il s'agit de la phase 12 de la formation et de la formation en matière de formation professionnelle.
>  **【类比】**Le patient dit "Mon seau souffre" (文本) + 给你看心电图 (图像) + 让你听心跳录音 (音频) 医生要同时检索医学文献 (文本) ♡心电图案库 (图像) ♡心跳声纹库 (音频),融合多源信息后给出诊断 (诊断) 融合策略:分数融合 = 让分分分分分加权;注意力融合 = 专业融合 = 让分分分分分加权; 专业融合 = 让分分分分分加权; 专业融合 = 让分分分分分分加权; 专业融合 = 专业融合 = 不同专业处理不同模态;;

## Objectifs d'apprentissage

- Réception par modalities croisées: texte → image, image → texte, audio → vidéo, etc.
  Le texte de la loi est le texte de la loi.
- Comparer trois stratégies de fusion: fusion de score, fusion axée sur l'attention, fusion MoE.
  Le nombre de personnes qui ont été impliquées dans la fusion de données est de plus de 100 000 personnes.
- Expliquez la mise à terre de la génération: à quoi ressemble "citer vos sources" lorsque les sources sont un mélange de modalités.
  Traduction anglaise: "Quand la source est une multitude de formes mélangées, la source de référence est une multitude de formes".
- Nombre des trois enquêtes canoniques multimodelles du RAG de 2025 et de leur taxonomie sous-problème.
  Le récit de la série de la série de films de l'année de l'histoire de l'histoire de la société japonaise

## Le problème , l' introduction du problème

Le RAG à modalité unique est un schéma résolu: intégrer la requête, intégrer les morceaux, récupérer, les choses dans le LLM. Le RAG multimodale nécessite:

> 单模态 RAG 是已解决的模式:嵌入查询、嵌入块、检索、塞入 LLM──多模态 RAG 需要:

1. Plusieurs têtes de récupération (chaque modalité a besoin d'embeddings dans un espace compatible).
   En anglais, le mot "référencement" est traduit par "référencement".
2. La fusion des résultats de récupération entre les modalités.
   Le terme "région" est traduit par "région".
3. Le terrain de génération qui cite des sources à travers les modalités.
   Le terme "région" est traduit par "région".
4. Les mesures d'évaluation couvrant le signal trans-modal.
   En français, le mot "évaluation" est traduit par "évaluation".

Les enquêtes de 2025 arrivent toutes à la même taxonomie.

> Les résultats de l'ensemble de l'année 2025 sont identiques.

## Le concept de base.

> **【中文解读】**跨模态 RAG  étendu le texte traditionnel RAG, soutenir le recherche et la génération de plusieurs modèles: peut être utilisé pour la recherche d'images, avec des images pour la recherche de texte, ou mélangé recherche de plusieurs modèles de documents.

> **【拓展：多模态 RAG 的应用**Le marché de l'information et de la communication (RAS) est un secteur très important dans le domaine de la santé, de la recherche et de la recherche.


### Récupération croisée

Retrouvez les documents de la modalité B à la suite d'une requête de la modalité A. Trois modèles:

> 给定模态 A 的查询,检索模态 B 的文档──三种模式:

1. L'espace d'embedding partagé. CLIP et CLAP produisent des emblèmes de texte + image / texte + audio dans un espace partagé. La similitude cosine entre les modalités fonctionne directement. Limité aux paires formées par CLIP.
   En français, le CLAP est utilisé pour créer des images et des images en ligne.

2. Encodeur de modalité + traduction. Encodeur de texte + encodeur d'image + un petit module de traducteur cartographiant entre les espaces. Sen2Sen par Gupta et coll. et d'autres conceptions 2024.
   Chaque mode de conception est un modèle de conception de l'image.

3. Utilisez les états cachés d'un VLM comme représentation de récupération.
   Le VLM est utilisé comme un codeur.

Choix: CLIP / SigLIP 2 pour texte + image; CLAP pour texte + audio; VLM-états cachés pour la qualité transversale à frontière.

> 选择建议:文本+图像用 CLIP/SigLIP 2;文本+音频用 CLAP;前沿质量跨模态用 VLM 隐藏状态──

### Stratégies de fusion

Vous avez récupéré 10 résultats: 5 images, 3 passages de texte, 2 clips audio. Comment fusionnons-nous ?

> Vous avez cherché 10 résultats: 5 images, 3 articles, 2 articles, 2 articles, 2 articles, 2 articles, 2 articles, 3 articles, 3 articles, 2 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 articles, 3 ...

La fusion de scores (plus bon marché). Chaque modalité a son propre retriever, chacun rend des scores. Normalizer les scores dans la modalité puis somme. Simple, fonctionne souvent.

> Le modèle a son propre référentiel, chacun de ses propres référentiels.

La fusion basée sur l'attention. Concaténer tous les objets récupérés, laisser un petit réseau d'attention les peser.

> Attention intégration, mise en œuvre de tous les processus, faire augmenter le pouvoir de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de l's.

La fusion MoE. Gating des itinéraires réseau vers des experts spécifiques à la modalité.

> MoE 融合──门控网络路由到模态特定专家──不同查询类型路由不同视觉问题给图像更高权重──

Par défaut de production: fusion de score avec un léger biais vers la modalité dominante de la requête.

> Si les tests A/B dans votre domaine montrent des avantages évidents, améliorez-les à MoE。

> **【中文解读】**三种融合策略:(1) 分数融合各模块检索器分别归归化分数后加权求和,最简单;(2) 注意力融合小网络学习权重,需要训练;(3) MoE 融合门控网络按查询类型路由到不同专家──生产默认是分数融合 + 微偏置对查询主导模块的微偏置──

> **【拓展：多模态 RAG 的跨模态检索基础】**跨模态检索有三种模式:(1) 共享嵌入空间(CLIP/SigLIP 2 用图文,CLAP 用文本-音频);(2) 每模态独立编码器 + 翻译模块;(3) 用 VLM 隐藏状态作为检索表示──选择建议:文本+图像用 CLIP/SigLIP 2,文本+音频用 CLAP,跨模态前沿质量用 VLM 隐藏状态──

### Le rajeunissement de la génération

La MLL doit citer le point récupéré qui a motivé chaque réclamation.

> L'AML 应引用哪个检索项驱动了每个声明. Pour plusieurs modèles:

- Source de texte: citation standard `[1]`- Je suis désolé .
  Traduction anglaise:`[1]`Il y a une autre.
- Source d'image: `[img 3]`avec une courte légende.
  Le mot "c'est-à-dire " est traduit par "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire" est traduit par "c'est-à-dire" est traduit par "c'est-à-dire" est traduit par "c'est-à-dire "c'est-à-dire" est traduit par "c'est-à-dire "est-à-dire" est traduit par "est-à-dire "est" est traduit par "est"`[img 3]`附简短描述──
- Audio: `[audio 2 at 0:34]`- Je suis désolé .
  Le mot "l'écriture" est traduit par "l'écriture".`[audio 2 at 0:34]`Il y a une autre.

Entraînez le générateur avec des données de base: chaque affirmation dans la cible de formation est marquée par l'indice source.

> Utilisation de l'analyse des données générateur de formation: chaque déclaration de l'objectif de formation sont marquées source de référence.

### Les enquêtes de 2025

Abootorabi et al. (arXiv:2502.08826, "Ask in Any Modality"): taxonomie pour RAG multimodal. Couvre le retrait, la fusion, la génération. Couverture la plus large.

> Les résultats de la recherche ont été obtenus par la Commission européenne.

Mei et al. (arXiv:2504.08748, "A Survey of Multimodal RAG"): se concentre sur les repères de sous-tâche et les modes d'échec. Utilisés pour la conception d'évaluation.

> Mei et d'autres: mise au point des tâches et des défauts

Zhao et coll. (arXiv:2503.18016): enquête axée sur la vision.

> Zhao 等人:聚焦视觉的综述──对 ColPali 系列工作覆盖深入──

Lire les trois vous donne l'état de l'art au printemps 2025.

> 阅读全部三篇 可获得2025年春最前沿状态―― la plupart des enfants sont encore ouverts―

### MuRAG  le document fondateur

MuRAG (Chen et coll., 2022) a été le premier RAG multimodal. Il a récupéré une image + texte à partir d'un KB multimodal, généré des réponses. Il a montré sa faisabilité avant la vague VLM.

> Le MURAG est le premier RAG à avoir été créé à partir de plusieurs modèles de données, à la recherche d'images et de textes, à la génération de réponses.

### Un exemple de planificateur de voyage de production

" Trouvez-moi un petit déjeuner végétalien tranquille avec de la lumière naturelle. "

> "Donne-moi un petit déjeuner tranquille et pur, avec la lumière naturelle".

L'équipement de transport:

> - Le conduit:

1. Décomposer la requête. "quiet" → mot clé audio/révision; "vegan brunch" → élément du menu; "lumière naturelle" → fonction d'image.
   Le mot grec traduit par "réfléchir" est "réfléchir" et "réfléchir".
2. Retour par modalité:
   Le mot "c'est-à-dire " est traduit par "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire" est traduit par "c'est-à-dire" est traduit par "c'est-à-dire" est traduit par "c'est-à-dire" est traduit par "c'est-à-dire" est traduit par "c'est-à-dire" est traduit par "c'est-à-dire" est traduit par "c'est-à-dire " est traduit par " est traduit par " est traduit par " est traduit par " est traduit par " est traduit en grec par " est traduit par "
   - Récupération de texte sur les commentaires: "brunch végétalien, ambiance calme".
     Le cinéma est un cinéma de la culture.
   - Retrait d'image sur les photos du restaurant: "Lumière naturelle, airée".
     Le récit de la première édition de la série est le suivant:
   - Récupération audio sur des clips sonores ambiants: " bas décibels, pas de musique ".
     Le mot "réalité" est traduit par "réalité".
3. Chaque restaurant a un score composé.
   Chaque salle de jeux a un nombre de parties.
4. Les restaurants Top-k → générateur VLM avec toutes les preuves → réponse avec des citations.
   Le premier est le premier, qui est le premier.

Chaque modalité ajoute un signal que le texte seul manque.

> Le texte est bien supérieur à la RAG. Chaque modèle est ajouté uniquement à partir des signaux omis par le texte.

### RG multimodaux agencés

Multi-hop: si la première récupération ne renvoie pas de réponses de haute confiance, le LLM reformula et récupère à nouveau.

> Do jump: si la première fois que le test a été effectué ne réagit pas à la réponse de haute confiance, LLM 重新表述并再次检索──Phase 14 de l'agent RAG 模式在此适用──exemple:

- Retriever le top-10 initial → LLM demande "trop bruyant, filtre pour <40 dB" → récupérer.
  Le premier est le premier, le deuxième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième et le troisième.
- Retriever des images → LLM voit que l'on a un menu → récupérer le texte du menu → réponse.
  Le texte de la lettre de l'auteur est écrit en français.

Ajout de complexité mais gère des requêtes que la récupération à un seul coup ne peut pas.

> augmenter la complexité mais peut traiter une seule enquête 

### Évaluation

L'évaluation intermodale est encore immature.

> 跨模态评估 encore inmaturée.

- Rappel par modalité.
  Le récit de la rédaction de la lettre de la Loi de l'Église de Jérusalem
- Une précision top-k fusionnée.
  Le taux de concentration de la concentration de l'eau dans le monde est de 0,5% en moyenne.
- La satisfaction de bout en bout jugée par l'homme.
  Traduction anglaise: fin de la révision artificielle
- Spécifique de tâche (réservations effectuées, achats effectués).
  Le terme "achat" est traduit par "achat".

Aucune référence standard ne couvre toutes les modalités.

> 没有标准基准覆盖所有模态── la plupart des articles sont évalués sur des tâches spécifiques dans un domaine──

## Utilisez-le avec le cadre de réalisation
```figure
contrastive-matrix
```

## Utilisez-le

`code/main.py`- Le numéro de la liste:

- Trois faux récupérateurs (texte, image, audio) opèrent sur un corps commun de restaurants.
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la [de.
- Fusion de scores qui combine les scores de modalité avec des poids configurables.
  Le nombre de composants est de 0,9 à 0,9 par rapport à 0,9 par rapport à 0,9 par rapport à 0,9 par rapport à 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par rapport au 0,9 par par par rapport au 0,9 par par par par rapport au 0,9 par par par par par par par par par par rapport au 0,9 par par par par par par par par par par par par par par par par rapport au 0,0.
- Un étiquette générateur qui émet une réponse finale avec des citations.
  Le générateur de réponse finale ──
- Une simple boucle agencée qui réformula la requête si la confiance est faible.
  Traduction anglaise: 置信度低时重新表述查询的简单代理循环──

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-multimodal-rag-designer.md`- étant donné une spécification de produit avec un flux de requête multimodal, les conceptions de récupérateurs, de fusion, de générateur et d'évaluation.

> 本课产 出 `outputs/skill-multimodal-rag-designer.md` déterminer les spécifications des produits, la conception des enquêteurs, la stratégie de fusion, les générateurs et les programmes d'évaluation du flux de recherche 

## Les exercices

1. Proposer un RAG multimodal médical-triage: requête = photo de blessure + symptômes de texte. Quelles modalités récupérer de quel KB? 设计医疗分诊多模态 RAG:查询 = 伤处照片 + 文字症状──哪些模态从哪些知识库检索?

2. La fusion de scores est une somme simple pondérée. Quel mode d'échec a-t-elle qui éviterait la fusion MoE?

3. Lisez la taxonomie d'Abootorabi et coll. (section 3). Quels sont les trois sous-problèmes canoniques et comment les cartographier sur votre produit choisi ?

4. Conçu une spécification d'évaluation pour un RAG multimodal de planificateur de voyage. Quelles mesures couvrent le rappel d'images, le rappel audio et la précision composite?

5. Le RAG multi-hop agent a une taxe de latence par aller-retour. À quelle difficulté de requête le gain de précision justifie-t-il la latence?

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Cross-modal retrieval | "Query one modality, retrieve another" 跨模态检索 | Text query retrieves images; image query retrieves text; requires a shared space or translator 文本查询检索图像；图像查询检索文本；需要共享空间或翻译器 | |
| Score fusion | "Combine scores" 分数融合 | Weighted sum of per-modality retrieval scores; simplest fusion 各模态检索分数的加权和；最简单的融合方式 | |
| MoE fusion | "Modality-routed experts" 混合专家融合 | Gating network picks which modality's scores to trust per query 门控网络按查询选择信任哪个模态的分数 | |
| Grounded generation | "Cite your sources" 接地生成 | Each claim in the answer tagged with the source index 回答中的每个声明都标注来源索引 | |
| MuRAG | "First multimodal RAG" 首个多模态 RAG | 2022 paper that established the multimodal RAG pattern 2022 年建立多模态 RAG 模式的论文 | |
| Agentic multi-hop | "Reformulate and retry" Agent 多跳 | LLM re-queries retrievers when first-pass confidence is low 首次检索置信度低时 LLM 重新查询检索器 | |

## Encore une lecture

- [Abootorabi et al. — Ask in Any Modality (arXiv:2502.08826)](https://arxiv.org/abs/2502.08826)
- [Mei et al. — A Survey of Multimodal RAG (arXiv:2504.08748)](https://arxiv.org/abs/2504.08748)
- [Zhao et al. — Vision RAG Survey (arXiv:2503.18016)](https://arxiv.org/abs/2503.18016)
- [Chen et al. — MuRAG (arXiv:2210.02928)](https://arxiv.org/abs/2210.02928)
- [Liu et al. — REACT (arXiv:2301.10382)](https://arxiv.org/abs/2301.10382)
