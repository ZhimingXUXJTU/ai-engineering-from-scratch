# Janus-Pro: Des encoders découpés pour les modèles multimodels unifiés

> Les modèles multimodels unifiés ont une tension inévitable. La compréhension a besoin de caractéristiques sémantiques  VECTORS de sortie SigLIP ou DINOv2 riches en informations au niveau du concept. La génération veut des codes conviviaux à la reconstruction  des jetons VQ qui se composent en pixels clairs. Les deux objectifs ne sont pas compatibles dans un seul encodeur. Janus (DeepSeek, octobre 2024) et Janus-Pro (DeepSeek, janvier 2025) affirment que la solution est d'arrêter d'essayer: déconnecter les deux encoders. Partager le corps de transformateur entre les tâches, mais parcourir la compréhension via SigLIP et générer par un tokenizer VQ. À 7B, Janus-Pro bat DALL-E 3 sur GenEval tout en correspondant à LLaVA sur MMMU. Cette leçon explique pourquoi deux encoders fonctionnent quand l'un échoue.

> **【中文解读】**Janus-Pro(DeepSeek,2025年1月) résoudre un paradoxe fondamental: comprendre les tâches nécessitent des caractéristiques de langage (sigLIP), générer les tâches nécessitent de reconstruire un code amicale (VQ token) ⋅ les deux ne peuvent pas être compatibles avec un seul codeur。 Janus-Pro's réponse est: comprendre le chemin de la voie SigLIP, générer le chemin de la voie VQ, partager le transformateur 主体。7B 参数就在 GenEval 上击败了DALL-E 3。

> **【拓展：解耦编码器的产业影响】**L'idée de l'éditeur est devenue une structure par défaut du modèle de 2026: l'InternVL-U l'intégrera dans le cadre de formation préalable à la création de plusieurs modèles.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, dual-encoder routing + shared-body signal) | **语言:** Python（标准库，双编码器路由 + 共享体信号）
**Prerequisites:** Phase 12 · 13 (Transfusion), Phase 12 · 14 (Show-o) | **前置知识:** Phase 12 · 13（Transfusion），Phase 12 · 14（Show-o）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**Le processus de formation est le premier à être réalisé. Il s'agit de la phase 12 de la formation.
>  **【类比】**Janus-Pro = "d'un côté ou de l'esprit" (左脑) = SigLIP (siglifier le concept de chat); Right Brain = VQ-VAE (victoriel) = image de chat)

## Objectifs d'apprentissage

- Expliquez pourquoi un seul codeur partagé compromet la compréhension ou la qualité de la génération.
  > Expliquer pourquoi un seul codeur partagé va nuire à la compréhension ou à la qualité de production.
- Décrivez le routage de Janus-Pro: SigLIP fonctionne sur le côté d'entrée pour la compréhension, VQ tokens à la fois pour l'entrée et la sortie pour la génération.
  > 描述 Janus-Pro 的路由: comprendre les routes d'entrée avec SigLIP Caractéristiques, générer les routes d'entrée et de sortie avec VQ Token。
- Suivez l'échelle des données qui rend Janus-Pro réussi là où Janus ne l'a pas fait.
  > 追溯让Janus-Pro Success et Janus 失败的数据混合扩展──
- Comparer les architectures découplées (Janus-Pro), couplées-continues (Transfusion) et couplées-discrètes (Show-o).
  > Je suis un homme qui a une vieille expérience.

## Le problème , le contexte .

Les modèles unifiés partagent un corps transformateur à travers la compréhension et la génération.

> 统一模型在理解和生成之间共享 Transformer 主体──前一次尝试(Chameleon、Show-o、Transfusion) utilisent tous un appareil de traitement visuel分词器 pour traiter les deux directions──分词器是妥协:

- Optimisé pour la reconstruction (génération): VQ-VAE capture des détails de pixel finement grains mais produit des jetons avec une faible cohérence sémantique.
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de
- Optimisé pour la sémantique (compréhension): SigLIP incrustations de groupe "cat" images près de "cat" jetons mais ne permettent pas une bonne reconstruction.
  Pour le reste, le code de la "cat" est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat" qui est un code de "cat.

Le programme de la Commission a été lancé en juin 1995 et a été lancé en décembre 1995.

> Le programme de transfusion a payé un impôt sur la qualité. Janus-Pro: Pourquoi utiliser un mot-clé lorsque les tâches sont différentes ?

## Le concept de base.

> **【中文解读】**Janus-Pro(DeepSeek) utilise un codeur visuel pour comprendre des tâches (CLIP), un codeur pour générer des tâches (VQ) ⋅ deux codeurs partagent la même mémoire de licence, chacun se spécialisant dans l'optimisation des différents expressions visuelles.

> **【拓展：解耦编码器的动机】**Comprendre les tâches nécessite des caractéristiques linguistiques de haut niveau, générer les tâches nécessite des caractéristiques de détails de bas niveau. Un seul codeur est difficile à faire en même temps.


### Codification visuelle découlée

L'architecture de Janus-Pro sépare les deux encoders:

> L'architecture de Janus-Pro sera divisée en deux éditeurs:

- Compréhension du chemin. image d'entrée → SigLIP-SO400m → corps de transformateur à 2 couches MLP.
  Le modèle de la ligne de référence est le modèle de la ligne de référence.
- Chemin de génération. image d'entrée (si conditionnée sur une image existante) → VQ tokenizer → IDs de jeton → corps transformateur.
  Le code de la carte est le code de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de
- Génération de sortie. Tokens d'image prédits par le transformateur → décodeur VQ → pixels.
  Le modèle de l'image est le modèle de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image.

Le corps du transformateur est partagé, tout en amont et en aval du corps est spécifique à la tâche.

> Le transformateur principal est partagé. Tout ce qui est dans le transformateur est spécifique.

Les entrées sont déambiguées par format prompt: a `<understand>`les itinéraires de marquage à travers le SigLIP; `<generate>`ou le routage est implicite de la tâche.

> 输入通过提示格式消歧:`<understand>`标签路由到 SigLIP;`<generate>`路由到VQ── ou 路由从任务隐式确定──

### Pourquoi ça marche ?

La perte de compréhension obtient des fonctionnalités SigLIP, qui ont été ajustées pour une similitude sémantique par la pré-entraînement CLIP.

> Comprendre la perte d'acquisition de SigLIP, le CLIP 风格的预训已经为语义相似性调优了这些特征―― le test de base de perception du modèle est supérieur à Show-o/Transfusion, car les caractéristiques d'entrée sont plus adaptées à la tâche――

La perte de génération obtient des jetons VQ, qui ont été réglés par un tokeniser pour la reconstruction.

> Les images sont plus efficaces que les images, car VQ 码能干净地组合回像素──

Le corps du transformateur partagé voit deux distributions d'entrée (SigLIP et VQ) et apprend à travailler avec les deux.

> Les transformateurs utilisent des données suffisantes pour absorber les changements.

### Écalement des données  Janus vs Janus-Pro

Janus (original, arXiv 2410.13848) a introduit le découplage mais à petite échelle (1.3B paramètres, données limitées).

> Janus (original version, arXiv 2410.13848) introduit la connaissance  mais la taille est plus petite  13 亿参数, données limitées)  Janus-Pro (arXiv 2501.17811) a été étendu:

- Paramètres 7B (versus 1.3B).
  Le nombre de personnes concernées est de 70 milliards.
- 90 M paires d'images-texte pour la phase 1 (alignement) à partir de 72 M.
  En anglais, le nombre de personnes concernées est de 7200.000.000.
- 72 M pour la phase 2 (unifiée) à partir de 26 M.
  Le nombre de personnes qui ont été vaccinées est de 22 millions de personnes.
- 200 000 échantillons d'instructions de génération d'images ont été ajoutés pour la phase 3.
  Pour la troisième phase, on a ajouté 20 000 images générant des instructions de sample.

Le résultat: Janus-Pro-7B partage LLaVA sur MMMU (60.3 vs ~58) et bat DALL-E 3 sur GenEval (0.80 vs 0.67). Un modèle ouvert, compétitif des deux côtés du spectre unifié.

> 结果:Janus-Pro-7B dans MMMU 上匹配 LLaVA(60.3 vs ~58), dans GenEval 上击败 DALL-E 3(0.80 vs 0.67);; un modèle ouvert, aux deux extrémités du même schéma, il y a une concurrence;;

### JanusFlow  la variante de flux rectifiée

JanusFlow (arXiv 2411.07975) change le chemin de génération de VQ pour un chemin de génération de flux rectifié (continu). La fraction devient SigLIP-pour-compréhension + flux-pour-génération rectifié.

> JanusFlow(arXiv 2411.07975) va remplacer VQ 生成路径 par 整流流生成路径(连续) ・・・分离成 SigLIP Utilisé pour comprendre + 整流用于生成──质量上限进一步提升──架构仍然是解编码器-共享主体──

### Le travail du corps commun

Le corps transformateur traite une séquence unifiée mais avec deux distributions d'entrée.

> Le transformateur principal traite la séquence de l'entrée mais il a deux types de distribution de l'entrée.

- Pour comprendre: consommer les fonctionnalités SigLIP + jetons de texte → émettre du texte autorégressivement.
  Le code de la langue française est le code de la langue française.
- Pour la génération: consommer des jetons de texte + (jetons VQ d'image optionnels) → émettre des jetons VQ d'image autogressivement.
  Le code de référence est le code de référence de la carte de crédit.

Le corps n'a pas de poids spécifique à la modalité par bloc. C'est le transformateur de style texte que vous attendez de trouver à l'intérieur de Qwen ou Llama, plus les deux adaptateurs d'entrée.

> Le principal n'a pas de mode de poids spécifique. C'est le type de transformateur que vous souhaitez trouver au Qwen ou à Llama.

Il est intéressant de noter que le corps de Janus-Pro pourrait être initialisé à partir d'un LLM prétrainé. Janus-Pro commence à partir de DeepSeek-MoE-7B. Ce choix compte: le LLM contribue à la capacité de raisonnement que les modèles unifiés purement de zéro luttent pour atteindre.

> Il est intéressant de noter que Janus-Pro  les sujets peuvent être initiés à partir de la formation préalable de LLM.

### Comparé à InternVL-U

Le programme de suivi de l'internVL-U (leçon 12.10) est le suivant pour 2026.

> Le programme de formation de l'international est un programme de formation de l'international de formation professionnelle (international level) qui est un programme de formation de l'international de formation professionnelle (international level) et qui est un programme de formation de l'international de formation professionnelle (international level).

- Pré-entraînement multimodal natif (rétectrice interne VL3).
  Le premier est le premier.
- Routage par codeur découplé (siglip en, diffusion VQ + se déplace).
  Le code de code est le code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de
- Compréhension unifiée + génération + édition.
  Le texte de la première partie est le texte de la première partie.

InternVL-U intègre le choix architectural de Janus-Pro dans un cadre plus large.

> InternVL-U a intégré l'architecture de Janus-Pro dans un cadre plus large.

### Limitations

Les encoders découpés ajoutent une complexité architecturale. Deux tokenizers à former, deux chemins d'entrée à entretenir, deux ensembles de modes de défaillance. Pour les produits qui ne nécessitent pas de génération, Janus-Pro est sur-ingénierie.

> Le codeur augmente la complexité de l'architecture. Deux mots doivent être formés, deux voies d'entrée doivent être maintenues, deux groupes de défaillance. Pour les produits non produits, Janus-Pro a choisi un modèle de compréhension de la famille LLaVA.

Pour les produits qui ne nécessitent pas de compréhension, Janus-Pro est surqualifié  choisissez un modèle Stable Diffusion 3 / Flux.

> Pour les produits qui ne nécessitent pas d'interprétation, Janus-Pro

Pour les produits qui ont besoin des deux, Janus-Pro est maintenant l'architecture ouverte de référence.

> Pour les deux produits dont nous avons besoin, Janus-Pro est maintenant une référence en architecture ouverte.


> **【拓展：Janus-Pro 在基准上的表现】**Janus-Pro est un programme de programmation de 3 à 5% de la base de compréhension multiforme sur le système de programmation de l'ensemble, de 10 à 15% sur le système de production d'images.


## Utilisez-le en pratique
```figure
l5-janus-decouple
```

## Utilisez-le

`code/main.py`simule le routage Janus-Pro:

> `code/main.py`模拟 Janus-Pro 路由:

- Deux encoders simulés: SigLIP (produit des vecteurs sémantiques de 256 dimensions) et VQ (produit des codes entiers).
  Le code de code de type VQ est composé de 256 caractères.
- Un routeur rapide qui choisit l'encodeur en fonction d'une balise de tâche.
  Traduction anglaise: basé sur les étiquettes de tâches
- Un corps partagé (stand-in) qui traite les séquences de jetons, quel que soit le codeur qui les a produites.
  Le codex est un codex de codex.
- Un passage de l'étape 1 (alignement) à l'étape 3 (tune d'instruction) du calendrier des échantillons pondérés.
  Le premier est le deuxième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième, le troisième et le troisième.

Imprimez les chemins routés pour 3 exemples: image QA, T2I, édition d'image.

> 印 3 个示例的路由路径:图像问答、T2I、图像编辑──

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-decoupled-encoder-picker.md`. Étant donné qu'un produit qui veut une génération unifiée + une compréhension de la qualité de pointe, il choisit Janus-Pro, JanusFlow ou InternVL-U avec une recommandation concrète sur l'échelle des données.

> 本课产 出 `outputs/skill-decoupled-encoder-picker.md`◊ Donnée la nécessité de la qualité de la vie en tant que produit de compréhension, il est possible de choisir entre Janus-Pro、JanusFlow ou InternVL-U, avec des recommandations de taille de données spécifiques.

## Les exercices

1. Janus-Pro-7B surpasse DALL-E 3 sur GenEval. Expliquez pourquoi un modèle ouvert 7B peut être compatible avec un modèle propriétaire de frontière sur la génération mais pas sur la compréhension.
   Le généval de Janus-Pro-7B a surmonté DALL-E 3[6]. Explique pourquoi le modèle ouvert 7B peut être généré sur un modèle spécialisé en avant-garde, mais ne peut pas être compris.

2. Implémenter une fonction de routeur: en donnant un texte prompt, classer comme `understand`ou `generate`Comment gérer des demandes ambiguës comme "décrire et ensuite dessiner"?
   Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la`understand`Ou `generate`Comment faire pour décrire et dessiner ?

3. JanusFlow remplace le chemin VQ par un flux rectifié.
   Le flux de l'équipement est en train de changer.

4. Proposer une quatrième tâche que l'architecture Janus-Pro pourrait gérer avec un encodeur déconnecté supplémentaire.
   Le projet de loi de Janus-Pro est une proposition de loi qui vise à créer un système de programmation de type "Janu-Pro" et à développer une structure de programmation de type "Janu-Pro" qui peut être utilisée pour la création de l'ensemble de l'architecture de type "Janu-Pro" et de type "Janu-Pro" (Janu-Pro) et de type "Janu-Pro" (Janu-Pro) et de type "Janu-Pro" (Janu-Pro) et de type "Janu-Pro" (Janu-Pro) et de type "Janu-Pro" (Janu-Pro).

5. Lisez la section 4.2 de Janus-Pro sur l'échelle des données.
   Le deuxième chapitre de Janus-Pro, section 4.2 sur l'expansion des données, décrit la phase de données qui a le plus contribué à l'amélioration de la qualité de T2I.

## Les termes clés

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Decoupled encoding | "Two visual encoders" | Separate tokenizer or encoder per direction: semantic for understanding, reconstruction for generation | 每个方向使用独立的分词器或编码器：理解用语义，生成用重建 |
| Shared body | "One transformer" | Single transformer processes either encoder's output; no modality-specific weights | 单一 Transformer 处理任一编码器的输出；无模态特定权重 |
| SigLIP for understanding | "Semantic features" | CLIP-family vision tower providing rich conceptual features but poor reconstruction | CLIP 家族视觉塔，提供丰富的概念特征但重建能力差 |
| VQ for generation | "Reconstruction codes" | Vector-quantized tokens that decode cleanly back to pixels | 可干净解码回像素的向量量化 token |
| JanusFlow | "Rectified-flow variant" | Janus-Pro with a continuous flow-matching generation head instead of VQ | 使用连续流匹配生成头替代 VQ 的 Janus-Pro |
| Routing tag | "Task tag" | Prompt marker (`<understand>` / `<generate>`) that picks the input encoder | 选择输入编码器的提示标记 |

## Encore une lecture

- [Wu et al. — Janus (arXiv:2410.13848)](https://arxiv.org/abs/2410.13848)
  Le texte de Janus est en français.
- [Chen et al. — Janus-Pro (arXiv:2501.17811)](https://arxiv.org/abs/2501.17811)
  Le texte de la première partie de la série est le suivant:
- [Ma et al. — JanusFlow (arXiv:2411.07975)](https://arxiv.org/abs/2411.07975)
  Le projet de loi de la loi de l'Union européenne sur les droits de l'homme
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877)
  Le texte de l'article est le suivant:
- [Dong et al. — DreamLLM (arXiv:2309.11499)](https://arxiv.org/abs/2309.11499)
  Le récit de la rédaction de ce livre est le récit de la rédaction de ce livre.
