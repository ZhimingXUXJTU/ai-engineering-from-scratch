# Transfusion: texte autorégressif + image diffusion en un transformateur . Transfusion: un transformateur 兼做自归文本和扩散图像

> Chameleon et Emu3 ont misé tout sur des jetons discrets. Ils fonctionnent, mais le goulot d'étranglement de quantification est visible  les plateaux de qualité d'image en dessous des modèles de diffusion de l'espace continu. La transfusion (Meta, Zhou et al., août 2024) prend le pari opposé: maintenir les images en continu, laisser tomber le VQ-VAE entièrement et entraîner un transformateur avec deux pertes. Les jetons texte prédisent le prochain jeton. Les patchs d'image obtiennent une perte de parallèle de flux / diffusion. Les deux objectifs optimisent les mêmes poids. L'architecture sous-jacente à Stable Diffusion 3 (MMDiT) est un cousin proche. Cette leçon lit la thèse Transfusion, construit un entraîneur de jouets à deux pertes et retrace le masque d'attention qui permet à un transformateur de faire les deux tâches.

> **【中文解读】**Transfusion(Meta,2024年8月) a choisi le chemin opposé à Chameleon/Emu3: garder l'image pour la continuité, sans utiliser VQ-VAE, avec un transformateur, avec le même temps de courir deux pertes textbook token avec le même token 预测, image correction avec流匹配/扩散损失──

> **【拓展：双损失训练的工程挑战】**Le point de difficulté central de la transfusion réside dans l'équilibre entre deux fonctions de perte différentes de la mesure numérique. La différence de la taille des pertes NTP et de la propagation de la MSE peut entraîner une formation de gestion de perte.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, two-loss trainer on MNIST-scale toy) | **语言:** Python（标准库，MNIST 规模玩具的双损失训练器）
**Prerequisites:** Phase 12 · 11 (Chameleon), Phase 8 (Generative AI) | **前置知识:** Phase 12 · 11（Chameleon），Phase 8（生成式 AI）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**Je suis en train de faire une analyse de la situation et de la situation de l'entreprise.
>  **【类比】**Transfusion = "double épaisseur";; Chamélon = une chambre;; tout le contenu avec le même jeton); LLaVA = 联排别;;视觉和文本完全分开,靠桥接连接);Transfusion = 双拼;;一边文本下面的代号损失,一边图像扩散损失,共享承重墙 = 同一个变压器骨干);;
> ️ **【易错点】**两个损失直接相加而不调权重 → 一个损失主导训练(通常扩散 MSE 数值大,文本 NTP被淹没) ――修复:使用损失权重(如 λ_text=1.0, λ_image=0.1) 或 GradNorm自适应平衡──

## Objectifs d'apprentissage

- Télécharger un transformateur qui exécute deux pertes (NTP sur les jetons de texte, MSE de diffusion sur les patchs d'image) sur une colonne vertébrale.
  > Construire un transformateur qui peut fonctionner sur le même osseux avec deux pertes (NTP + image patch)
- Expliquez pourquoi l'attention bidirectionnelle sur les patchs d'image plus l'attention causale sur les jetons de texte est le bon choix de masque.
  > Expliquer pourquoi " image patch 双向 + 文本代币 因果 " est le vrai choix de masquerade.
- Comparez le style Transfusion (images continues, perte de diffusion) au style Chameleon (images discrètes, NTP) en termes de calcul, de qualité et de complexité de code.
  > Comparer Transfusion 风格 (continuous image, diffusion loss) à Chameleon 风格 (disparation image, NTP)
- Nommer la contribution de MMDiT: poids spécifiques à la modalité à chaque bloc, attention commune au flux résiduel.
  > 列举 MMDiT's contributions: Modèle de chaque bloc spécifique de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de poids, de po.

## Le problème , le contexte .

Le débat sur les jetons d'image discrets et continus est plus ancien que les LLM. Les représentations continues (pixels bruts, VAE latents) préservent les détails.

> Le débat entre le démarrage et le démarrage de la séquence d'image est plus rapide que celui de la séquence d'image.

Chameleon / Emu3 est allé discrète: une perte, une architecture, mais la fidélité d'image limitée par la qualité du tokenizer.

> Chameleon / Emu3 选择离散: une perte, une structure, mais l'image est sécurisée par la qualité des mots.

Les modèles de diffusion sont restés continuels: une qualité d'image exceptionnelle, mais un modèle séparé du LLM, un génie de programmation du bruit complexe et aucune intégration propre avec la génération de texte.

> 扩散模型选择连续:卓越的图像质量, mais avec LLM est un modèle indépendant, nécessitant un générateur de réglage du bruit complexe, incapable de générer un net intégration avec le texte.

La transfusion demande: pouvons-nous avoir les deux ? Gardez les images continuelles, entraînez toujours un modèle, utilisez deux pertes cousues en une étape de gradient.

> Transfusion 问:能否兼得两者? garder l'image连续, encore entraîner un modèle, avec deux pertes拼拼到一个梯度步中──

## Le concept de base.

> **【中文解读】**Transfusion(Meta) sera auto-retourné dans le modèle de génération et de diffusion du modèle d'image génération de fusion dans le même Transformer En: texte jeton Utilisation de la perte de prédiction de jeton suivant, jeton d'image Utilisation de perte de diffusion。 deux types de modèle partagé le même modèle paramètres mais utilisant des objectifs de formation différents。

> **【拓展：多模态训练目标的融合】**Transfusion  prouve l'auto-réintégration et la propagation peuvent être présentes dans le même modèle et  communité                                                                                                                                                                                                                                                


### L'architecture à deux pertes

Un transformateur unique à décodeur seul traite une séquence qui contient:

> 单一解码器 Transformer 处理 contient le suivant:

- Les jetons texte (discrète, du vocabulaire BPE).
  Le mot "sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-sans-
- Patch d'image (blocs de pixels 16x16 continus projetés dans un obscur caché via intégration linéaire  le même que l'entrée d'un encodeur ViT).
  Le modèle de la vidéo est le même que celui de la vidéo.
- `<image>`et `</image>`les balises indiquant où vivent les patchs continus.
  Le mot grec traduit par " le mot grec "`<image>`et `</image>`标签标记连续补丁的位置──

Le pass avant passe une fois.

> Il y a deux types de coups de feu:

- Pour les jetons de texte: entropie croisée standard sur la tête du logiteur de vocabulaire.
  Le code de référence est le code de référence.
- Pour les correctifs d'image: perte de diffusion sur les correctifs continus  prédire le bruit ajouté à chaque correction.
  Le patch d'image est le patch de l'image.

Le gradient coule dans le corps du transformateur partagé.

> 梯度通过共享的变压器 体回流――两个损失同时改进共享权重――

### Masque d'attention: texte causal + image bidirectionnelle

Les jetons de texte doivent être causaux  vous ne pouvez pas laisser un jeton de texte attirer le texte futur, ou un enseignant forcer des pauses.

> 文本代币 必須是因果的不能让文本代币 关注未来文本,否则教师强制会失败――但图像补丁代表一个快照; elles devraient être dans le même bloc d'image à se concentrer les unes sur les autres――

Le masque:

> - Je suis désolé .

```
M[i, j] = 1 if:
  (i is text and j is text and j <= i)   # causal for text
  OR (i is image and j is image and same_image_block(i, j))   # bidirectional within image
  OR (i is text and j is image and j < i_image_end)   # text attends to previous images
  OR (i is image and j is text and j < i_image_start)   # image attends to preceding text
```

Appliqué comme masque triangulaire à l'entraînement et à l'inférence.

> En train de s'entraîner et de réfléchir, il faut réaliser le bloc.

### Perte de diffusion à l'intérieur du transformateur

La perte de diffusion est standard: ajouter du bruit à un patch d'image, demander au modèle de prédire le bruit (ou le patch propre, équivalemment).

> 扩散损失是标准的: donner un patch d'image 添加噪音,让模型预测噪音(或等价地预测干净补丁) ◊ Transfusion 版本使用流匹配预测从噪音到干净的速度场──

Pendant la formation:
1. Pour chaque patch d'image x0, prenez un échantillon d'un pas de temps aléatoire t.
   Pour chaque image patch x0, le temps passe à l'échelle.
2. L'échantillon de bruit ε, calcul xt = (1-t) * x0 + t * ε (interpolation linéaire pour l'ajustement des flux).
   Le nombre de personnes concernées est de 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 à 0,9 en moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de la moyenne de
3. Le transformateur prédit v_theta(xt, t); perte = MSE(v_theta(xt, t), ε - x0).
   Le changement de la structure de l'équipement est le changement de la structure de l'équipement.
4. L'arrière-proposition aux côtés du texte NTP perd de la même séquence.
   Traduction anglaise: NTP 损失与反向传播──

En inférence, la génération est:
- Les jetons de texte: prélèvement autorégressif standard.
  Le code de référence est le code de référence.
- Parches d'image: boucle d'échantillonnage de diffusion (10-30 étapes typiques) conditionnée sur les jetons de texte précédents.
  Le patch d'image est un symbole de la propagation de la forme de cycle (habituellement 10 à 30 étapes).

### MMDiT: Variante de la diffusion stable 3

Stable Diffusion 3 (Esser et coll., mars 2024) a expédié MMDiT (Transformateur de diffusion multimodal) à peu près au même moment que Transfusion.

> Stable Diffusion 3 (Esser 等人,2024 年 3 月) a publié MMDiT (多模态扩散变压器), avec Transfusion 差不多同时──两者架构是兄弟──

Les principales différences de MMDiT:

> Les principales différences entre MMDiT et MMDiT:

- Les poids spécifiques à la modalité par bloc. Chaque bloc transformateur a des poids séparés Q, K, V et MLP pour les jetons de texte par rapport aux patchs d'image.
  Chaque bloc de transformateur a un texte indépendant qui est un jeton versus un patch d'image.
- Une variante spécifique de correspondance de flux avec le prélèvement d'échantillons connu et des mathématiques plus simples que la DDPM.
  Le cours de formation est un cours de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de
- L'échelle. MMDiT est la colonne vertébrale de SD3 (2B et 8B paramétrages).
  Le projet de transformation est étendu à 70 milliards.

Les deux convergent sur la même idée fondamentale: un transformateur exécute NTP sur texte et diffusion sur représentations d'image continues.

> 两者收到同一核心理念: un transformateur dans le texte fonctionne NTP, dans la représentation d'images en continu sur le flux de diffusion.

### Pourquoi ça bat le style du chamelion ?

L'écart de qualité entre la diffusion continue et la NTP discrète sur la génération d'images est mesurable.

>  Continuous diffusion et dispersion NTP dans la production d'images est quantifiable.

- À 7B, il bat un modèle de même taille au style de Chameleon sur FID de 3 à 5 points.
  Le modèle de la caméléon est de 3 à 5 minutes.
- Aucune formation de tokenizer n'est requise  l'encodeur d'image est plus simple (projection linéaire à cache, la même que la couche d'entrée d'une ViT).
  Le format de l'image est plus simple que le format de l'image.
- L'inference peut paralléliser la dénonciation de patch d'image, contrairement aux jetons d'image autorégressifs.
  Traduction anglaise: Sug理可以并行化图像补丁 去噪音, différent de la jeton d'image auto-retour.

Les effets négatifs: la transfusion est un modèle à double perte, ce qui rend la dynamique de formation plus difficile. Les poids de perte nécessitent une régulation.

> 缺点: La transfusion est un modèle de double perte, entraînement plus complexe.

### Ce qui est en aval

Janus-Pro (leçon 12.15) affinera l'idée de Transfusion en découplant le codeur de vision pour la compréhension et la génération  SigLIP pour l'un, VQ pour l'autre  tout en partageant le corps du transformateur. Show-o (leçon 12.14) swaps diffusion pour diffusion discrète (prédiction masquée).

> Janus-Pro (Leçon 12) 12.15 课) 通过解视觉编码器改进了转化思想SigLIP 用于理解,VQ 用于生成同时共享转化 主体──Show-o (Leçon 12) 12.14 课) 将扩散换换换为离散扩散(掩码预测)──统一生成家族在转化后迅速分化──

Les VLM de production 2026 qui émettent des images  Gemini 3 Pro, GPT-5, chemin de génération d'images de Claude Opus 4.7  utilisent presque certainement un descendant de cette famille.

> En 2026, la production de VLM Gemini 3 Pro 、GPT-5 、Claude Opus 4.7  est presque certainement utilisé par une autre génération de cette famille.


> **【拓展：TransFusion 的推理过程】**Transfusion  Key steps of thinking: text token auto-generation, rencontré image commence à marquer lors de la transition vers le mode de diffusion ⋅ diffusion processus se déroule dans le lieu de la image ⋅ lieu de la place de la image, avec le texte génération partage le même modèle paramètres ⋅


## Utilisez-le en pratique
```figure
cfg-guidance-scale
```

## Utilisez-le

`code/main.py`construit un jouet Transfusion sur un petit problème comme MNIST:

> `code/main.py`Dans le domaine de la construction de jouets, le MNIST

- Les légendes de texte sont de courtes séquences entières décrivant un chiffre (0-9).
  Le texte décrit la séquence de nombres à longueur courte.
- Les images sont des grilles de 4x4 octets.
  Le tableau est 4x4 字节网格。
- Une paire de projections linéaires partagées de poids agit comme le substitut du transformateur; perte de NTP sur le texte, perte de MSE sur les correctifs bruyants.
  Une projection de ligne en tant que transformateur 替代; un correcteur de bruit 损失, un correcteur de bruit 损失, un correcteur de bruit 损失.
- La boucle d'entraînement alternera les deux pertes, le masque d'attention est explicite.
  Le cycle de formation change en deux perdants, l'attention cache est évidente.
- La génération produit une légende texte et une image 4x4 dans un passage avant.
  Néo-latin: génération dans une fois avant de se propager produire une description et une image en 4x4

Le transformateur est un jouet, les tuyaux à deux pertes, la construction du masque d'attention et la boucle d'inférence sont les vrais artefacts.

> Le transformateur est un jouet de classe. Les deux lignes de perte de tuyau, la construction et le cycle de conception sont les seuls produits.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-two-loss-trainer-designer.md`. En raison d'une nouvelle tâche de formation multimodale (texte + image, texte + audio, texte + vidéo), il conçoit le calendrier de deux pertes (poids de perte, forme de masque, blocs partagés par rapport à des modalités spécifiques) et détermine les risques de mise en œuvre.

> 本课产 出 `outputs/skill-two-loss-trainer-designer.md`◊ a été donné une nouvelle tâche de formation en mode multispécial (en anglais: textbook + image 文本+音频、文本+视频), elle a conçu une double perte de poids (en anglais: loss of weight ≠ maskode shape ≠ sharing vs. mode) et a marqué la réalisation du risque (en anglais: risk △).

## Les exercices

1. Un modèle de transfusion entraîne 70% de jetons de texte et 30% de correctifs d'image. La perte de diffusion d'image est ~ 10x la perte de NTP de texte en magnitude. Quels poids de perte les équilibrent?
   Traduction chinoise:Transfusion 风格模型训练 70% 文本代币 和 30% 图像补丁──图像扩散损失在量级上约为文本NTP损失的10倍──什么损失权重能平衡它们?

2. Mettre en œuvre le masque triangulaire de bloc pour une séquence: `[T, T, <image>, P, P, P, P, </image>, T]`Marquez chaque entrée 0 ou 1.
   Pour la première fois, il y a eu une série de`[T, T, <image>, P, P, P, P, </image>, T]`实现块三角掩码──标记每个条目为0或1──

3. MMDiT a des poids de QKV spécifiques à la modalité. Quel compte de paramètres ajoute-t-il par rapport au transformateur entièrement partagé de Transfusion ?
   En anglais, le nombre de paramètres de transfusion est de 70 milliards de paramètres de valeur.

4. Génération: donné une requête de texte, le modèle exécute NTP pour 50 jetons, puis frappe `<image>`Il y a une diffusion sur 256 patchs sur 20 pas de dénos.
   Le modèle est utilisé pour la mise en service de 50 tokens NTP, puis rencontré.`<image>`, puis dans 256 patchs, 20 étapes de propagation du bruit.

5. Lisez le document SD3 Section 3. Décrivez le débit rectifié et pourquoi il converge en moins de démarches d'inférence que le DDPM.
   Le texte de la SD3 est en cours de rédaction.

## Les termes clés

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Two-loss training | "NTP + diffusion" | A single transformer optimizes both cross-entropy on text tokens and MSE on continuous image patches in the same gradient step | 单一 Transformer 在同一梯度步中优化文本 token 交叉熵和连续图像 patch MSE |
| Flow matching | "Rectified flow" | Diffusion variant that predicts a velocity field from noise to clean data; simpler math than DDPM | 预测从噪声到干净数据速度场的扩散变体；数学比 DDPM 更简单 |
| MMDiT | "Multimodal DiT" | Stable Diffusion 3's architecture: joint attention, modality-specific MLPs and norms | SD3 架构：联合注意力、模态特定 MLP 和归一化 |
| Block-triangular mask | "Causal text + bidirectional image" | Attention mask that is causal across text but bidirectional within image regions | 文本因果、图像区域内双向的注意力掩码 |
| Continuous image representation | "No VQ" | Image patches as real-valued vectors, not integer codebook indices | 图像 patch 为实值向量，非整数码本索引 |
| Velocity prediction | "v-parameterization" | Network output is the velocity field between noise and data, not the noise itself | 网络输出为噪声和数据之间的速度场，非噪声本身 |

## Encore une lecture

- [Zhou et al. — Transfusion (arXiv:2408.11039)](https://arxiv.org/abs/2408.11039)
  Le texte de la traduction est le suivant:
- [Esser et al. — Stable Diffusion 3 / MMDiT (arXiv:2403.03206)](https://arxiv.org/abs/2403.03206)
  Traduction anglaise: Diffusion stable 3 / MMDiT 论文。
- [Peebles & Xie — DiT (arXiv:2212.09748)](https://arxiv.org/abs/2212.09748)
  Le texte de la première partie de la série est le texte de la première partie de la série.
- [Zhao et al. — MonoFormer (arXiv:2409.16280)](https://arxiv.org/abs/2409.16280)
  Le texte est en français.
- [Xie et al. — Show-o (arXiv:2408.12528)](https://arxiv.org/abs/2408.12528)
  Le thème de la série est "La vie est une chose".
