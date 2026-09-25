# LLaVA-OneVision: une seule image, plusieurs images, vidéo dans un modèle

> Avant LLaVA-OneVision (Li et coll., août 2024) le monde VLM ouvert avait des lignées distinctes: LLaVA-1.5 pour les images uniques, les modèles multi-image comme Mantis et VILA, les modèles vidéo comme Video-LLaVA et Video-LLaMA. Chacun a remporté sa référence et échoué aux autres. LLaVA-OneVision a soutenu qu'un seul programme d'études pouvait former un modèle pour dominer les trois scénarios, et que les effets émergents de transfert de tâches (habiletés de l'image unique exportées vers la vidéo, raisonnement multi-image exporté vers l'image unique) ont dépassé la somme des spécialistes. La recette est trompeusement simple: un budget de jeton visuel qui reste constant dans tous les scénarios, plus un programme explicite qui passe d'une seule image à OneVision (multi-image) à la vidéo. Cette leçon est consacrée au budget, au programme et aux comportements émergents.

> **【中文解读】**L'objectif principal de LLaVA-OneVision est de créer un modèle unique de trois scénarios.

> **【拓展：统一多模态模型的产业价值】**Dans les produits réels, l'utilisateur peut simultanément télécharger des images uniques, des images et des vidéos.

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, token budget solver + curriculum planner)  | **语言：Python（标准库，token预算求解器 + 课程规划器）**
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 12 · 06 (any-resolution)  | **前置：阶段12第05课（LLaVA）、阶段12第06课（任意分辨率）**
**Time:** ~180 minutes  | **时长：约180分钟**

>  **【前置】**Je suis en train de faire une étude de la série LLaVA.
>  **【类比】**LLaVA-OneVision = "Overall Swiss Army Knife"。 autres VLM = 专门的单功能刀(单图刀、多图刀、视频刀)。 Swiss Army Knife (LVA-OneVision) ⇒ 子和刀片的总长度恒定,根据场景切换主功能──

## Objectifs d'apprentissage

- Conception d'un budget de jeton visuel qui maintient constants sur les entrées d'image unique, multi-image et vidéo.
- Commander un programme de formation qui transfère des compétences d'une seule image à une vidéo sans oublier catastrophiquement.
- Expliquez pourquoi un modèle unique bat les spécialistes au même nombre de paramètres quand le programme est bien fait.
- Nombre des trois capacités émergentes rapportées par LLaVA-OneVision: raisonnement multi-caméra, mise en marche de la demande, iPhone-écran-agent.

## Le problème , le contexte .

L'image, la vidéo et la vidéo mettent chaque modèle en valeur différemment.

Une image unique nécessite des jetons haute résolution (AnyRes, ~ 2880 jetons visuels) pour capturer OCR et les détails fins.

Multi-image veut plusieurs images à résolution modérée (~ 576 jetons chacun) de sorte que le raisonnement entre les images s'inscrit dans le contexte.

La vidéo a besoin de plusieurs images à faible résolution (~ 196 jetons par image après la mise en commun) pour capturer la dynamique temporelle.

> **【中文解读】**Trois scénarios pour les jetons  Budgets de demande différent: un seul diagramme à haute résolution (((environ 2880 jetons), un grand nombre de diagrammes à moyenne résolution (((environ 576 jetons), un petit nombre de vidéos à faible résolution mais plus de 196 jetons)  Le défi réside dans: comment répondre à trois scénarios en même temps avec un budget fixe。

Si vous entraînez des modèles séparés, vous choisissez un budget. Si vous entraînez un modèle, vous avez besoin du budget pour échanger raisonnablement entre les scénarios sans percer de contexte.

Avant OneVision, la réponse par défaut était "traînez un scénario, ignorez les autres". Video-LLaVA a retrofitté la vidéo sur un modèle d'image avec des étapes d'entraînement supplémentaires. LLaVA-NeXT a ajouté une prise en charge multi-image avec des carreaux. Aucun n'a géré les trois correctement.

## Le concept de base.

### Le budget du jeton OneVision

LLaVA-OneVision choisit un budget unifié de jetons visuels d'environ 3000 à 4000 jetons par échantillon, alloués différemment par scénario:

- Image unique / 单图: AnyRes-9 (3x3 carreaux + miniature), chaque carreaux à 384 avec 729 patches, pooling bilinéaire agressif 2x2 → 182 par carreaux. Total: 9 * 182 + 182 = 1820 jetons.
- Multi-image / 多图: chaque image à résolution modérée (384, pas de carrelage), 729 jetons sans pooling. Budget 6 images → 4374 jetons.
- Vidéo / 视频: 32 images à 384 résolutions avec un pool bilinéaire agressif 3x3 → 81 jetons par image.

L'allocation maintient des jetons totaux à peu près constants. Le LLM ne voit jamais un lot qui souffle son contexte. L'encodeur produit une géométrie différente par scénario, mais le LLM consomme le même budget.

> **【中文解读】**核心思想:总代币 预算保持恒定(约3000-4000), mais la distribution varie selon les scénarios.

### Le programme de trois étapes de cours

Les trains LLaVA-OneVision sont organisés en trois étapes:

1. SFT (étape SI) / 单图指令微调. Toutes les données sont uniques image-plus-texte. entraînez sur une entrée AnyRes haute résolution. Cela enseigne la perception, OCR et la compréhension fine. Utilise des données LLaVA-NeXT ainsi que des données uniques d'image spécifiques à OneVision.
2. OneVision SFT (étape OV) / 统一指令微调. Mix single-image + multi-image + vidéo (cadres échantillonnés de manière uniforme).
3. Transfert de tâches (étape TT) / 任务迁移. Continuez avec un mix de tâches cibles, généralement plus lourd sur plusieurs images ou vidéos selon le produit. Optionnel fine-tune pour le déploiement.

Le programme de formation vidéo-première ou multi-image-première produit de pires performances d'image que la première image-unique, même avec les mêmes données.

> ️ **【易错点】**La séquence de cours de soi-même est très faible. Les performances de la séquence sont considérablement diminuées.
> 🤔 **【困惑】**Q: Pourquoi le budget fixe est-il si important ? Parce que la fenêtre ci-dessus de la LLM est fixe, le seul graphique est soudainement constitué de 5000 jetons、 vidéo 10000 jetons, qui détruira le lotage 和推理预算── le budget fixe = coût de la prévision de la prévision, est la clé de la déploiement du produit──

> **【中文解读】**ordre de cours: pré-unité ∞, ré-unité + vidéo, dernière tâche de déplacement ∞. Si on entraîne d'abord unité ∞ ou unité ∞, les performances de la formation diminuent ∞.

### Pourquoi le programme fonctionne-t-il ?

La formation en image unique construit la base perceptuelle. Les jetons de patch comportent des caractéristiques visuelles fines; le LLM apprend à les intégrer avec le texte.

Si vous entraînez tous les scénarios à partir de zéro ensemble, le modèle est inférieur à la perception (données limitées d'une seule image par lot) et à la structure des surdits (beaucoup de données multiculturelles / vidéo).

L'ordre du programme vous donne une force de perception à partir de l'étape SI, puis un raisonnement compositif/temporal à partir de l'étape OV, sans perdre aucun.

> **【中文解读】**Si on entraîne simultanément tous les scénarios, le modèle manquera de capacité de perception adaptée à chaque lot de données (environ un seul graphisme) et de structure trop adaptée (environ un grand nombre de graphes/vidéos), ce qui entraînera le modèle à faire des hypothèses à travers des graphes mais une compréhension visuelle faible.

### Des compétences émergentes en scénarios croisés

Le document LLaVA-OneVision rapporte trois capacités émergentes:

1. Le modèle intègre correctement les vues malgré le fait de ne jamais avoir vu ce format exact dans la formation.
2. L'utilisateur annotera les objets d'une image avec des marques numérotées; le modèle explique ce que fait la marque 3 par rapport à la marque 7.
3. L'utilisateur fournit une capture d'écran d'un écran de l'iPhone et demande de planifier le prochain clic.

Il ne s'agit pas de tâches formées; elles émergent de la structure compositive du programme.

> **【拓展：涌现能力的工程启示】**La capacité de survenue signifie que la valeur du modèle unifié dépasse les spécialités et les compétences de la prise de vue de plusieurs caméras pouvant être utilisées pour la surveillance de sécurité, la conduite autonome, les conseils de marquage pouvant être utilisés pour les outils de marquage d'images, les interfaces de sélection de caméras pouvant être utilisées pour les tests d'automatisation de l'interface utilisateur.

### Le regroupement de jetons visuels

Le budget des jetons nécessite un regroupement. OneVision utilise une interpolation bilinéaire sur la grille de correctifs 2D: 24x24 = 576 patches devient 12x12 = 144 (2x facteur) ou 8x8 = 64 (3x facteur).

Le choix du facteur de pooling par scénario est lui-même un hyperparamètre. Moins de pooling = plus de jetons = représentation plus riche.

> **【中文解读】**池化在2D 补丁网格空间进行(而非代币 空间), pour conserver l'espace local性──池化因子是每个场景的超参数:少池化=更多代币=更丰富表示;多池化=更少代币=可容纳更多/图像──

### LLaVA-OneVision-1.5

Le suivi de 2025 (LLaVA-OneVision-1.5, arXiv 2509.23661) est " complètement ouvert " dans les données de formation, les poids des modèles et le code. Il correspond à la lacune de propriété sur certains critères de référence et démocratise la recette.

### Comparé à Qwen2.5VL par rapport à Qwen2.5VL

Qwen2.5-VL (Létion 12.09) fait des choix différents. Il utilise M-RoPE et FPS dynamique au lieu de pooling fixe. Ses balances budgétaires avec entrée  une vidéo de 1 minute utilise plus de jetons qu'une vidéo de 5 secondes. LLaVA-OneVision fixe le budget et évolue le pooling.

> **【中文解读】**Qwen2.5VL Utilisation de M-RoPE 和动态率,token 预算随输入缩放;LLaVA-OneVision 固定预算、调整池化──
```figure
l5-onevision-budget
```

## Utilisez-le

## Utilisez-le en pratique

`code/main.py`Il est un programme et un planificateur budgétaire pour un VLM de style OneVision.

- Il attribue la résolution, le facteur de regroupement et les cadres par scénario.
- Vérifie que chaque scénario s'inscrit dans le budget partagé.
- Rapports du nombre de jetons attendus, des FLOP de LLM, et des scénarios qui sont sous-tokenés.
- Il imprime un programme d'entraînement étape par étape.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-onevision-budget-planner.md`. Compte tenu d'une répartition des tâches cibles et d'un budget par échantillon, il émet le facteur AnyRes, le regroupement par cadre, le nombre de images vidéo et les poids des étapes du programme.

> **【中文解读】**Le projet de formation est basé sur le programme de formation de formation et de formation en formation.

## Les exercices

1. Votre produit prend en charge 80% d'images uniques, 10% de plusieurs images (2-4 images), 10% de vidéos (8-16 images). Concevez le budget des jetons.
   | 产品支持 80% 单图、10% 多图（2-4张）、10% 视频（8-16帧）。设计 token 预算。从轻量多图中省下的预算放在哪？

2. Lire la section 4.3 de LLaVA-OneVision (capacités émergentes). Proposer une quatrième compétence émergente que le programme pourrait probablement débloquer mais que le journal n'a pas rapportée.
   | 阅读 LLaVA-OneVision 第 4.3 节（涌现能力）。提出课程学习可能解锁但论文未报告的第四种涌现技能。

3. Changer l'ordre du programme  train d'abord multi-image, puis une seule image, puis vidéo. Prédire quelles valeurs de référence dégradent et pourquoi.
   | 交换课程顺序——先多图，再单图，最后视频。预测哪些基准会下降以及原因。

4. Le document rapporte des benchmarks vidéo formés sur seulement 8 images par échantillon. Cela se généralise-t-il à des vidéos de 30 secondes à l'inférence?
   | 论文报告视频基准只用每样本8帧训练。这对推理时的30秒视频泛化吗？先崩溃的是 token 预算还是时序推理？

5. Le pooling bilinéaire de 24x24 patches à 12x12 est une réduction de 4x par dim.
   | 将 24x24 补丁双线性池化为 12x12 是每维 4 倍缩减。用标准库 Python 实现池化，验证每个 2x2 块的均值与双线性输出一致。

## Les termes clés

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| OneVision scenario | "Single-image, multi-image, or video" | One of three input shapes the unified VLM handles; the budget stays constant across | 统一 VLM 处理的三种输入形态之一，预算在场景间保持恒定 | |
| Token budget | "How many tokens per sample" | Total visual tokens the LLM sees per training / inference sample, typically 3000-4000 | LLM 每样本看到的总视觉 token 数，通常 3000-4000 | |
| Curriculum | "Training order" | Stage ordering (single-image → multi-image → video) chosen for emergent transfer | 课程学习：按单图→多图→视频顺序训练，促进技能迁移 | |
| Bilinear pooling | "Token shrink" | Applying bilinear interpolation to the patch grid (2D) to reduce token count while preserving locality | 在补丁网格上做双线性插值，减少 token 数并保留空间局部性 | |
| Emergent skill | "Not trained, still works" | Capability that appears at inference without matching training data, due to curriculum composition | 课程学习组合带来的未训练即涌现的能力 | |
| AnyRes-k | "k-tile setup" | k sub-tiles of fixed resolution plus one thumbnail, typical k ∈ {4, 9} | k 个固定分辨率子切片加一个缩略图 | |
| Task transfer | "Cross-scenario generalization" | Skills learned on single-image that apply to video (and vice versa) via shared backbone | 通过共享骨干网络，单图技能迁移到视频（反之亦然） | |

## Encore une lecture

- [Li et al. — LLaVA-OneVision (arXiv:2408.03326)](https://arxiv.org/abs/2408.03326)Je suis un homme qui a une vision de l'univers.
- [LLaVA-OneVision-1.5: Fully Open Framework (arXiv:2509.23661)](https://arxiv.org/abs/2509.23661)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
- [Lin et al. — Video-LLaVA (arXiv:2311.10122)](https://arxiv.org/abs/2311.10122)Je suis un homme qui a des problèmes de santé.
- [Lin et al. — VILA (arXiv:2312.07533)](https://arxiv.org/abs/2312.07533)Je suis un homme de bien.
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191)Je suis un homme qui a une bonne idée.
