# Évaluation  FID, CLIP Score, préférence humaine  évaluation indicateur  FID  CLIP Score et préférences humaines

> Chaque tableau de classement génératif cite FID, CLIP score et un taux de victoire d'une arène de préférence humaine. Chaque nombre a un mode d'échec un chercheur déterminé peut jouer. Si vous ne connaissez pas les modes d'échec, vous ne pouvez pas dire une amélioration réelle d'une course de jeu.

> **【中文解读】**Chaque classement de génération de modèles cite FID (Fréchet Inception Distance) ✓ CLIP Score 和人类偏好胜率── chaque indicateur a des lacunes qui peuvent être effacées── ne pas comprendre ces lacunes, on ne peut pas distinguer entre des améliorations réelles et des lacunes.

> **【拓展：FID 的局限性】**FID mesure la distance de distribution entre la production d'images et la production d'images réelles, mais elle peut être optimisée (comme la production de échantillons élevés par choix)  Évaluation des préférences humaines (comme le mode Chatbot Arena)  Alternative plus fiable mais plus coûteuse 

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 01 (Taxonomy / 分类), Phase 2 · 04 (Evaluation Metrics / 评估指标) | **前置知识:** 阶段 8 · 01（分类），阶段 2 · 04（评估指标）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Le problème , l' introduction du problème

Un modèle génératif est jugé sur * la qualité de l'échantillon * et * l'adhésion des conditions *. Aucune n'a de mesure de forme fermée. Votre modèle doit rendre 10 000 images; quelque chose doit leur attribuer des nombres; vous devez faire confiance aux nombres dans les familles de modèles, dans les résolutions, dans les architectures. Trois mesures ont survécu au gants 2014-2026:

> Les deux ne sont pas de taille fermée. Votre modèle doit être en train de produire 10000 images; il doit y avoir quelque chose pour les donner.

- **FID (Fréchet Inception Distance).**La distance entre deux distributions  réelles et générées  dans l'espace de fonctionnalités d'un réseau Inception.
  **FID。**Réalité et génération répartis dans l'espace de la création 网络特征空间中的距离──越低越好──
- **CLIP score.**C'est une similitude cosine entre l'intégration de l'image CLIP d'une image générée et l'intégration de texte CLIP d'un prompt.
  **CLIP Score。**Clip en même temps que le texte de la demande.
- **Human preference.**Faites face à face deux modèles sur le même prompt, faites en sorte que les humains (ou un modèle de classe GPT-4) choisissent le meilleur, agrégé à un score Elo.
  **人类偏好。**Les deux modèles sont plus bons que les humains ou les modèles de classe GPT-4, regroupés en Elo.

Vous verrez également: IS (score d'initiation, en grande partie retraité), KID, CMMD, ImageReward, PickScore, HPSv2, MJHQ-30k. Chacun corrige un échec de l'ancien.

> Vous verrez aussi: IS( déjà basé dans le jeu) ∞ KID、CMMD、ImageReward、PickScore、HPSv2 etc.

> **【中文解读】**Les trois grands indicateurs de l'évaluation du modèle de développement: 1) FID dans le cadre de la mise en place de l'espace de caractéristiques du réseau pour mesurer la distance entre la distribution générée et la réelle distribution, plus basse que la bonne; 2) CLIP Score pour la correspondance de la signification de l'image générée avec le texte prompt, plus haut que la bonne; 3) préférence des gens deux modèles sont meilleurs par rapport au choix, concentrés en Elo par nombre.

> **【拓展：生成模型评估的"刷榜"问题】**La FID peut être optimisée à travers la génération sélective de haute part de échantillons, de réglage d'initiation ou de suradaptation à la distribution de référence. Le CLIP Score a également des préjugés. Le CLIP Model est plus sensible à certains concepts. L'évaluation des préférences humaines (comme l'Aréna de l'analyse artificielle) est la méthode la plus fiable mais la plus coûteuse. La tendance de 2026 est d'utiliser le modèle de niveau GPT-4 comme "jugateur automatique" pour approcher les préférences humaines.

## Le concept de base.

![FID, CLIP, and preference: three axes, different failure modes](../assets/evaluation.svg)

### La qualité de l'échantillon

Heusel et coll. (2017).

> Il est également possible de faire une demande de règlement.

1. Extraire les fonctionnalités Inception-v3 (2048-D) pour N images réelles et N générées.
   Pour N 张真像和 N 张生成图像提取 Inception-v3 特征(2048 维)
2. Pour chaque piscine , un Gaussien .`μ_r, μ_g`et la covariance `Σ_r, Σ_g`- Je suis désolé .
   Pour chaque poignée de hauteur: valeur moyenne calculée `μ_r, μ_g`Et les différences`Σ_r, Σ_g`Il y a une autre.
3. FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`- Je suis désolé .
   FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`Il y a une autre.

Interprétation: distance Fréchet entre deux gaussiens multivariés dans l'espace de caractéristiques.

> 解读: Traits de la répartition entre deux différents niveaux de l'espace

Mode d'échec:

> 失败模式:

- **Biased on small N.**Le FID est le carré moyen sur la distribution de fonctionnalités  petit N sous-estime la covariance, donne un FID faussement faible.
  FID est une différence moyenne de la distribution des caractéristiques, et FID est une différence de la distribution des caractéristiques.
- **Inception-dependent.**Inception-v3 a été formé sur ImageNet. Les domaines éloignés d'ImageNet (faces, art, images de texte) produisent des FID sans sens. Utilisez un extracteur de fonctionnalités spécifique au domaine.
  Selon Inception:Inception-v3 dans le domaine de l'imageNet, il se produit des images personnelles sans aucune signification.
- **Gaming.**Le surmatch de la pré-Inception donne une faible FID sans amélioration de la qualité visuelle.
  刷分: Pour Inception, les tests précédents ont permis de fournir un faible FID, mais la qualité visuelle n'a pas augmenté.

### Score CLIP  rapidité de conformité  CLIP Score  rapidité de suivi

Radford et coll. (2021). Pour une image générée + prompt:

> Radford 等人(2021)。 Pour générer des images + prompt:

```
clip_score = cos_sim( CLIP_image(x_gen), CLIP_text(prompt) )
```

La moyenne sur 30 000 images générées → un échelle comparable entre les modèles.

> Pour 30 000 images générées en moyenne → un échantillon comparable entre les modèles

Mode d'échec:

> 失败模式:

- **CLIP's own blind spots.**CLIP a un faible raisonnement compositif (" un cube rouge sur une sphère bleue " échoue souvent).
  CLIP  propre point aveugle: CLIP 组合推理能力弱 (Rouge couleur triangle sur bleu-bleu) ⋅ Modèle peut être classé en haut de CLIP Score mais en réalité ne suit pas vraiment un prompt complexe.
- **Short prompt bias.**Les courts rappel ont plus de matchs d'image CLIP dans la nature.
  短 prompt 偏差:短 prompt 在野外有更多 CLIP-image 匹配──长 prompt 在 CLIP Score 上机械性地更低──
- **Prompt gaming.**L'inclusion de " haute qualité, 4K, chef-d'œuvre " dans le prompt gonfle le score CLIP sans améliorer la liaison image-texte.
  Rapidement 刷分: 在 prompt 中加入 "haute qualité, 4k, chef-d'œuvre" 能升高 CLIP Score而不改善图文绑定──

CMMD (Jayasumana et coll., 2024) corrige certaines de ces caractéristiques: utilise des fonctionnalités CLIP au lieu de Inception, une disparité moyenne maximale au lieu de Fréchet.

> CMMD(Jayasumana 等人 2024) a corrigé certains des problèmes: utiliser CLIP caractéristiques plutôt que d'Inception, utiliser MMD(maximum moyenne différence) plutôt que de Fréchet 距离──更善于检测细微的质量差异──

### Les préférences humaines  la vérité du sol  les préférences humaines  la valeur du sol

Choisissez un ensemble de requêtes. Générez avec le modèle A et le modèle B. Montrez des paires aux humains (ou un juge LLM fort).

> 選一批提示──用模型 A 和模型 B 生成──把成对结果展示给人类 (或强 LLM 评判)──把胜场聚聚合为 Elo 或Bradley-Terry 分数──基准:

- **PartiPrompts (Google)**: 1600 demandes de renseignements variées, 12 catégories.
  **PartiPrompts（Google）**: 1600 个多样化 prompt, 12 个类别:
- **HPSv2**: 107 000 annotations humaines, largement utilisées comme proxy automatisé.
  **HPSv2**10,7 000 articles de l'humanité, largement utilisés comme agents automatiques.
- **ImageReward**: 137k paires de préférences d'images instantanées, sous licence MIT.
  **ImageReward**13,7 millions pour les images de préférence, avec la permission du MIT.
- **PickScore**: formé sur les préférences Pick-a-Pic 2.6M.
  **PickScore**Je suis en train de faire des exercices.
- **Chatbot-Arena-style image arenas**Le numéro de la liste:https://imagearena.ai/et d'autres.
  **Chatbot-Arena 风格的图像竞技场**- Le numéro de la liste:https://imagearena.ai/Ça va.

Mode d'échec:

> 失败模式:

- **Judge variance.**Les non-experts ont des préférences différentes des experts.
  评判者方差: les non-experts et les spécialistes ont des préférences différentes.
- **Prompt distribution.**Les conseils choisis favorisent une famille.
  Rapidement déployée: Éclémentation de la sélection rapide 会偏向某一家族──务必记录──
- **LLM-judge reward hacking.**Le juge GPT-4 est trompé par des résultats fausses.
  L'évaluation de la LLM est mise à jour: GPT-4

## Utilisez ensemble

Un rapport d'évaluation de la production devrait inclure:

> Un rapport d'évaluation de la production devrait contenir:

1. D'après le rapport de référence, les données de référence sont les données de référence de l'échantillon.
   En 10 à 30 000 échantillons, la quantité de FID est réellement répartie par rapport à la quantité de échantillons.
2. Score CLIP / CMMD sur les mêmes échantillons par rapport à leurs indications (adhésion).
   Pour les autres, le taux de réussite est de 0,5% par rapport à la moyenne de la moyenne de chaque seconde.
3. Taux de gain dans une arène aveuglée par rapport au modèle précédent (préférence globale).
   Avec un modèle précédent, le taux de victoire dans le marché de l'économie de marché est un taux de victoire total.
4. Analyse du mode défaillance: 50 sorties échantillonnées au hasard, marquées pour des problèmes connus (anatomie de la main, rendu du texte, nombre d'objets cohérent).
   失败模式分析:随机采样 50 输出,标记已知问题(手部解剖、文字染、对象计数一致性)

Toutes les mesures sont fausses, trois mesures corroborantes et une évaluation qualitative sont une affirmation.

> Tout indicateur unique est un mensonge.

## Construisez-le et mettez-le en œuvre.
```figure
gx-fid-distributions
```

## Faites-le

`code/main.py`Il implique l'agrégation FID, CLIP-score-like et Elo sur des "vecteurs de caractéristiques" synthétiques (nous utilisons des vecteurs 4D comme suppléments pour les caractéristiques d'Inception).

> `code/main.py`Dans la synthèse "Tréciles de l'échelle" pour réaliser FID, classe CLIP Score et Elo 聚合(nous utilisons 4 维向量 au lieu de Traits d'Inception)

- Le calcul FID sur un petit N et sur un grand N  le biais.
  FID de petite N et grande N de haute N calculer les différences
- "Clip score" comme similitude cosine entre les pools de fonctionnalités.
  作为特征池之间余弦相似度的"CLIP Score" (Clip Score)
- Règlement de mise à jour Elo à partir d'un flux de préférences synthétiques.
  Il est également utilisé dans les produits de la production de produits de haute qualité.

### Étape 1: FID en quatre lignes.

```python
def fid(real_features, gen_features):
    mu_r, cov_r = mean_and_cov(real_features)
    mu_g, cov_g = mean_and_cov(gen_features)
    mean_diff = sum((a - b) ** 2 for a, b in zip(mu_r, mu_g))
    trace_term = trace(cov_r) + trace(cov_g) - 2 * sqrt_cov_product(cov_r, cov_g)
    return mean_diff + trace_term
```

> Quatre lignes FID: séparation entre la valeur moyenne du calcul et la différence de la valeur moyenne du calcul et la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence de la différence.

### Étape 2: Clip-style cosine-semblance

```python
def clip_like(image_feat, text_feat):
    dot = sum(a * b for a, b in zip(image_feat, text_feat))
    norm = math.sqrt(dot_self(image_feat) * dot_self(text_feat))
    return dot / max(norm, 1e-8)
```

> CLIP 风格余弦相似度: point积除以两个向量范数乘积,加epsilon 防止除零──

### Étape 3: L'agrégation d'élo

```python
def elo_update(r_a, r_b, winner, k=32):
    expected_a = 1 / (1 + 10 ** ((r_b - r_a) / 400))
    actual_a = 1.0 if winner == "a" else 0.0
    r_a_new = r_a + k * (actual_a - expected_a)
    r_b_new = r_b - k * (actual_a - expected_a)
    return r_a_new, r_b_new
```

> Elo 更新: Basé sur les attentes de victoire et les résultats réels, K=32 est le standard de l'échelle internationale.

## Les pièges sont des pièges.

- **FID at N=1000.**Les documents rapportant une faible N FID sont en jeu.
  N=1000 时的FID:在N<10k 时不可靠──报告低NFID的论文在刷分──
- **Comparing FID across resolutions.**La taille de l'Inception 299×299 modifie la distribution des fonctionnalités.
  跨分辨率比较 FID:Inception's 299×299 缩放会改变特征分布──只在匹配分辨率下比较──
- **Reporting one seed.**Faites au moins 3 semences.
  Rapport d'une seule graine: au moins 3 graines ont été lancées.
- **CLIP score inflation via negative prompts.**Certains pipelines augmentent le CLIP en ajustant trop le prompt.
  通过负向快速 抬高 CLIP Score:有些流水线通过过拟合快速 抬高 CLIP──检查视觉和──
- **Elo bias from prompt overlap.**Si les deux modèles ont vu une demande de référence pendant la formation, Elo est inutile.
  Rapide surpôt provoqué par Elo 偏差: si deux modèles entraînés lors de la formation ont vu le prompt de base, Elo 无意义──使用留出的 prompt 集──
- **Human eval paid-crowd skew.**Les annotateurs MTurk prolifiques sont plus jeunes / plus adaptés à la technologie.
  工评付费众包偏差:Prolific、MTurk 标注者偏年轻 / 偏技术友好──混合招募的艺术/设计专家──

## Utilisez-le avec le cadre de réalisation

Protocole d'évaluation de la production en 2026:

> Accord d'évaluation des niveaux de production de 2026:

| Pillar / 支柱 | Minimum / 最低要求 | Recommended / 推荐 |
|--------|---------|-------------|
| Sample quality / 样本质量 | FID on 10k vs held-out real | + CMMD on 5k + FID on subset per category |
| Prompt adherence / Prompt 遵循 | CLIP score on 30k | + HPSv2 + ImageReward + VQA-style question answering |
| Preference / 偏好 | 200 blinded pairs vs baseline | + 2000 paired human + LLM-judge + Chatbot Arena |
| Failure analysis / 失败分析 | 50 hand-flagged | 500 hand-flagged + automated safety classifier |

Les quatre piliers d'un rapport = revendication.

> Les quatre piliers sont un seul et même énoncé.

## Envoyez-le . Produit .

- Ça va .`outputs/skill-eval-report.md`. Skill prend un nouveau point de contrôle + ligne de base du modèle et produit un plan d'évaluation complet: tailles d'échantillons, mesures, sondes en mode défaillance, critères de résiliation.

> 保存为 `outputs/skill-eval-report.md` Cette compétence reçoit un nouveau point de contrôle de modèle + 基线, produit un plan d'évaluation complet: sample numbers, indication, défaillance, signature, standard.

## Les exercices

1. **Easy.**On court .`code/main.py`. Comparer le FID à N=100 contre N=1000 sur les mêmes distributions synthétiques.
2. **Medium.**Implémenter le CMMD à partir de caractéristiques de style CLIP synthétique (voir Jayasumana et coll., 2024 pour la formule).
3. **Hard.**Répliquez la configuration HPSv2: prenez 1000 paires d'images de la suite de Pick-a-Pic, ajustez un petit marqueur basé sur CLIP sur les préférences, et mesurez son accord avec un ensemble de retenu.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| FID | "Fréchet Inception Distance" | Fréchet distance of Gaussian fits to real vs gen Inception features. |
| CLIP score | "Text-image similarity" | Cosine similarity between CLIP image and text embeddings. |
| CMMD | "FID's replacement" | CLIP-feature MMD; less biased, no Gaussian assumption. |
| IS | "Inception score" | Exp KL(p(y|x) || p(y)); correlates poorly on modern models, retired. |
| HPSv2 / ImageReward / PickScore | "Learned preference proxies" | Small models trained on human preferences; used as automatic judges. |
| Elo | "Chess rating" | Bradley-Terry aggregation of pairwise wins. |
| PartiPrompts | "The benchmark prompt set" | 1,600 Google-curated prompts across 12 categories. |
| FD-DINO | "Self-sup replacement" | FD using DINOv2 features; better for out-of-ImageNet domains. |

## Note de production: évaluation est une charge de travail de déduction trop

Exécuter FID sur des échantillons 10k signifie générer des images 10k. Pour une base SDXL de 50 étapes à 10242 sur un seul L4, c'est ~ 11 heures d'inférence à une seule demande. Les budgets d'évaluation sont réels, et le cadrage est exactement le scénario d'inférence hors ligne (maximiser le débit, ignorer TTFT):

- **Batch hard, forget latency.**Évaluation hors ligne = lotage statique à la taille la plus grande qui correspond à la mémoire. `pipe(...).images`avec `num_images_per_prompt=8`sur un H100 de 80 Go fonctionne 4 à 6 fois plus vite que sur demande unique.
- **Cache the real features.**L'extraction de la fonction Inception (FID) ou CLIP (CLIP-score, CMMD) sur le jeu de référence réel est exécutée *une fois*, stockée en tant que `.npz`Ne recomptez pas par évaluation.

Pour les portes CI / régression: exécuter FID + CLIP score sur un sous-ensemble de 500 échantillons par PR (~ 30 min); exécuter plein 10k FID + HPSv2 + Elo chaque nuit.

## Encore une lecture

- [Heusel et al. (2017). GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium (FID)](https://arxiv.org/abs/1706.08500) papier FID.
- [Jayasumana et al. (2024). Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603) CMMD.
- [Radford et al. (2021). Learning Transferable Visual Models from Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020)- Je suis en train de vous dire.
- [Wu et al. (2023). HPSv2: A Comprehensive Human Preference Score](https://arxiv.org/abs/2306.09341) HPSv2.
- [Xu et al. (2023). ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation](https://arxiv.org/abs/2304.05977) ImageReward.
- [Yu et al. (2023). Scaling Autoregressive Models for Content-Rich Text-to-Image Generation (Parti + PartiPrompts)](https://arxiv.org/abs/2206.10789) PartiPrompts.
- [Stein et al. (2023). Exposing flaws of generative model evaluation metrics](https://arxiv.org/abs/2306.04675) enquête en mode défaillance.
