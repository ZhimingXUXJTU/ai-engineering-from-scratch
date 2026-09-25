# LLaVA et l' instruction visuelle de réglage .

> LLaVA (avril 2023) est l'architecture multimodal la plus copiée de la planète. Il a remplacé le Q-Former de BLIP-2 par un MLP à 2 couches, a remplacé l'attention croisée fermée de Flamingo par une concatenation de jetons naïve et a été formé sur 158k tours d'instruction visuelle générés par GPT-4 à partir de légendes uniquement textuelles. Tout praticien qui a construit un VLM entre 2023 et 2026 a construit une variante de LLaVA. LLaVA-1.5 a ajouté AnyRes. La résolution de la LVA-NEXT a augmenté. LLaVA-OneVision image unifiée, multi-image et vidéo dans une recette. Cette leçon lit la recette, met en œuvre le projecteur et explique pourquoi "le plus simple a gagné".

> **【中文解读】**LLaVA est l'architecture à plusieurs modèles la plus copiée entre 2023 et 2026. Son idée de base est très simple: utiliser 2 niveaux de MLP pour mettre l'émetteur de l'éditeur visuel dans l'espace de projection du modèle de langue, puis mettre le jeton visuel directement dans la séquence de texte. LLaVA prouve que " l'architecture simple + données de haute qualité " suffit à dépasser la complexité du design.

> **【拓展：多模态大模型的起源】**Avant LLaVA, le modèle à plusieurs modèles dépendait principalement de mécanismes complexes de prise de conscience transmodèle (comme l'attention transmodèle à bord de la clé de Flamingo, Q-Former du BLIP-2). Le succès de LLaVA a marqué une étude à plusieurs modèles qui a été transférée de " meilleure conception à une interface transmodèle " vers " une interface plus simple + plus de données ". Ce modèle a directement influencé les futures VLM principales, l'InternVL, Qwen-VL, Phi-Vision, etc.).

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, projector + instruction-template builder)  | **语言：Python（标准库，投影器 + 指令模板构建器）**
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 11 (LLM Engineering — instruction tuning)  | **前置：阶段12第02课（CLIP）、阶段11（LLM工程——指令微调）**
**Time:** ~180 minutes  | **时长：约180分钟**

>  **【前置】**Le projet de formation de la formation de formation de la formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation
>  **【类比】**LLaVA = " mettre l'image directement imprimée et mise en papier dans le dossier "―BLIP-2 Q-Former = " mettre 256 pages en 32 pages résumé reversé à LLM "; LLaVA MLP = "576 pages d'original intégralement mise en papier à LLM "―L'ancien provincial papier mais perdu de l'information, l'autre paysage papier mais LLM regarde tout le détails de la LLLM sur le sous-titre changement, " le papier " n'est plus un problème, LLaVA naturellement déjà gagné―

## Objectifs d'apprentissage

- Construire un projecteur MLP à 2 couches qui cartographiera les emplacements de patch ViT (dim 1024) à un emplacement de MLL (dim 4096).
- Prenez la recette en deux étapes de LLaVA: (1) alignement du projecteur sur 558k paires de sous-titres, (2) réglage des instructions visuelles sur 158k tours générés par GPT-4.
- Construire un prompt en format LLaVA avec le placeur de jeton d'image, le prompt système et les virages utilisateur/assistant.
- Expliquez pourquoi la communauté est passée de Q-Former à MLP malgré la victoire du budget de jetons de Q-Former.

## Le problème , le contexte .

Le Q-Former de BLIP-2 (Lesson 12.03) comprime une image à 32 jetons. propre, efficace, bon pour les repères. Mais il a deux problèmes.

La première étape consiste à entraîner la perte de l'ITC+ITM+ITG. La deuxième étape consiste à entraîner la perte de l'IM. Les requêtes apprennent une représentation intermédiaire que le MLL doit ensuite décoder.

Deuxièmement, le Q-Former prend 188 millions de paramètres, et à l'échelle 2023 de LLaVA, vous avez dû le co-construire avec votre LLM cible. Changez le LLM, retrainer le Q-Former. Changez le codeur de vision, retrainer. Chaque combinaison était un projet de R&D séparé.

> **【中文解读】**L'ancien Q-Former de BLIP-2 réduirait l'image à 32 tokens, mais il y a deux problèmes principaux: 1) l'objectif de formation ne correspond pas à la première phase avec le CTI/ITM/ITG, la deuxième phase avec le langage construit perdue, les informations sont perdues dans la bouteille; 2) le paramètre est grand (environ 188M) et doit être re-entraîné avec un LLM spécifique.

La réponse de LLaVA était embarrassante en raison de sa simplicité: prenez les 576 jetons de patch du ViT, passent chacun par un MLP à 2 couches (`1024 → 4096 → 4096`Pas de goulot d'étrangle, pas de stage 1 de prétrainer sur des objectifs bizarres, entraînez simplement le MLP sur une perte directe de LM.

> **【中文解读】**Le schéma de LLaVA est simple à embarrassant: directement mettre les 576 pièces de monnaie de ViT par le biais d'un MLP de 2 niveaux`1024 → 4096 → 4096`), puis tout est jeté dans la séquence d'entrée de LLM.

> ️ **【易错点】**La première phase doit être formée ! Beaucoup de gens croient que l'on peut sauter la première phase  direct faire des instructions 微调不行! pas formé de projecteur de sortie de flux de flux, LLM 完全看不懂视觉代币 含义, la deuxième phase va faire LLM  把视觉代币 当噪音忽略掉──修复:

D'où viennent les données ? La deuxième idée de LLaVA: utiliser GPT-4 (seulement texte) pour générer des données d'instruction. Donner GPT-4 le titre COCO et les données de boîte de délimitation pour une image, lui demander de produire des conversations, des descriptions et des questions de raisonnement complexes. 158k instructions-réponse tourne gratuitement. Pas de notes humaines.

> **【中文解读】**Le deuxième innovation de LLaVA: générer des instructions avec GPT-4 (pure textbook mode) pour générer des données.

Le résultat: un VLM qui a couru sur 8 A100 pendant une journée, a battu Flamingo sur MMMU, et a expédié un point de contrôle ouvert que la communauté pouvait étendre.

> **【拓展：LLaVA 的产业影响】**LLaVA a prouvé que le VLM n'a pas besoin de calculs énormes. Le VLM n'a pas besoin de calculs énormes.

## Le concept de base.

> **【中文解读】**LLaVA va connecter CLIP  vidéo éditeur à LLM  via vidéo instruction micro调让模型学会看图说话──核心创新: avec GPT-4 生成多模态 instruction data, l'image description sera transformée en question à répondre à──LLaVA-1.5 atteint SOTA sur 11 基准, le coût de formation est d'environ 100 美元──

> **【拓展：LLaVA 的开源生态】**LLaVA est le modèle à grande résolution le plus réussi de tous les modèles. LLaVA-NeXT supporte des entrées à résolution arbitraire, LLaVA-OneVision 统一图像和视频理解.


### L'architecture et l'architecture

LLaVA-1.5 à 13B:
- Encodeur de vision / 视觉编码器: CLIP ViT-L/14 @ 336 (congelé pendant la phase 1, défriché optionnellement étape 2 / 第一阶段结,第二阶段可选解).
- Projecteur / 投影器: 2 couches MLP avec activation GELU / 2 couches MLP + GELU激活, `1024 → 4096 → 4096`- Je suis désolé .
- LLM / 语言模型: Vicuna-13B (plus tard Llama-3.1-8B / 后续使用 Llama-3.1-8B).

Passer en avant une image + texte prompt: 图像+文本提示的前向传播:

```
img -> ViT -> 576 patches of dim 1024           # 图像 -> ViT -> 576个维度1024的补丁
patches -> MLP -> 576 tokens of dim 4096         # 补丁 -> MLP -> 576个维度4096的token
prompt: system + "<image>" placeholder + user question  # 提示词：系统提示 + <image>占位符 + 用户问题
replace <image> token with the 576 projected tokens      # 用576个投影token替换<image>
feed the full sequence to the LLM                       # 将完整序列送入LLM
decode response                                         # 解码响应
```

L'image occupe 576 jetons du contexte LLM. Dans le contexte 2048, cela laisse 1472 jetons pour le texte. Dans le contexte 32k, c'est une erreur d'arrondissement.

> **【中文解读】**Une image occupe 576 jetons de la LLM en 2048; dans la fenêtre de la LLM en 2048 cette proportion est de 28%, il ne reste plus que 1472 jetons de la LLM; mais dans la 32k, cela peut être presque ignoré.

### Étapes 1: alignement du projecteur.

Le code de la langue est un code de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de

Dans une seule époque, au lot 128, cela se fait en quelques heures. Le projecteur apprend à cartographier l'espace ViT à l'espace LLM. Aucune supervision spécifique à la tâche.

> **【中文解读】**La première phase de formation est la réalisation de la première phase du programme de formation en programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de programmation de

### Étapes 2: réglage des instructions visuelles

Défrichez le projecteur (encore entraînable). Défrichez le LLM (généralement complètement, parfois LoRA).

Les données d'instruction sont la ruse.
1. Prenez une image de COCO.
2. Extraire la description du texte (5 sous-titres humains + liste de boîtes de délimitation).
3. Envoyez à GPT-4 avec trois modèles de commande:
   - Conversation / 对话: "Generer un dialogue entre un utilisateur et un assistant sur cette image".
   - Description détaillée / 详细描述: "Donnez une description riche et détaillée de l'image".
   - Réflexion complexe: " Posez une question qui demande de raisonner sur l'image, puis répondez- lui. "
4. Parser la sortie de GPT-4 en paires (instruction, réponse).

Aucun de ces éléments ne touche directement l'image  seulement la description du texte. GPT-4 hallucine le contenu plausible de l'image.

> **【中文解读】**关键创新: la génération de données ne touche pas complètement à l'image elle-même seulement avec la description textuelle。GPT-4 会"幻觉"out of reasonable image content, although there will be noise, but 158k 条数据 sufficient to unlock dialogue capacity。 Cette façon de "générer des modèles faibles avec des modèles forts entraînement données" a ensuite été largement adoptée(comme Self-Instruction、Alpaca, etc.)。

> 🤔 **【困惑】**Q: GPT-4 没看图只看描述,那 LLaVA 训练时实际学学的"视觉"是什么?A: LLaVA 学习是两件事:
> ️ **【易错点】**L'expérience de l'écriture de GPT-4 est un outil de formation de GPT-4 qui est utilisé pour la production de données.

> **【拓展：数据合成的范式意义】**La méthode de synthèse de données de LLaVA (GPT-4 生成指令数据) a ouvert une nouvelle génération de VLM 数据工程.

### Pourquoi la communauté a copié ça ? Pourquoi la communauté a fait ça ?

- Aucune perte spécifique de phase 1 à régler. Perte de LM tout au long.
- Le projecteur s'entraîne en quelques heures, pas en quelques jours.
- LLM peut être échangé (LLaVA-Llama2, LLaVA-Mistral, LLaVA-Llama3) en reentraînant seulement le projecteur.
- Le pipeline de données d'instruction visuelle utilise GPT-4 et est bon marché à régénérer pour un nouveau domaine.

### LLaVA-1.5 et LLaVA-NEXT

LLaVA-1.5 (octobre 2023) ajouté:
- Les données de tâches académiques (VQA, OKVQA, RefCOCO) mélangées à la mise en forme des instructions.
- Un meilleur système de pointe.
- 2048 → 32k contexte.

LLaVA-NeXT (janvier 2024) ajouté:
- AnyRes: divisez les images haute résolution en une grille de 2x2 ou 1x3 de 336 cultures, plus une miniature globale de basse résolution. Chaque culture devient 576 jetons; au total, environ 2880 jetons visuels par image. Les tâches OCR et des graphiques ont augmenté.
- Une meilleure combinaison de données d'instructions avec ShareGPT4V (captions GPT-4V de haute qualité).
- Il est également possible de faire des études de base plus solides (Mistral-7B, Yi-34B).

> **【拓展：AnyRes 与高分辨率理解】**AnyRes est une technique clé de traitement d'images à haute résolution LLaVA. Pour les rapports, les émissions et autres images de documents dans les scènes financières, la haute résolution est essentielle à comprendre.

### LLaVA-OneVision

Leçon 12.08 couvre OneVision en profondeur. version courte: même projecteur, mais formé avec un programme qui couvre une seule image, plusieurs images et vidéo dans un modèle avec un budget de jeton visuel partagé.

> **【中文解读】**Le programme de formation est basé sur la conception de l'image et de la vidéo.

### La comparaison avec Q-Former

| | Q-Former (BLIP-2) | MLP (LLaVA) |
|---|---|---|
| Visual tokens per image / 每张图视觉token数 | 32 | 576 (base/基础) or 2880 (AnyRes) |
| Trainable params / 可训练参数 | 188M + LM | 40M + LM |
| Stage 1 loss / 第一阶段损失 | ITC+ITM+ITG | LM only / 仅语言建模 |
| LLM drop-in / LLM替换 | Requires retrain / 需重新训练 | Swap with minimal retrain / 几乎无需重训 |
| Multi-image / 多图像 | Awkward / 不自然 | Natural (concat) / 自然拼接 |
| Video / 视频 | Awkward / 不自然 | Natural (per-frame concat) / 逐帧拼接 |
| Token budget / Token预算 | Small / 小 | Large / 大 |

Le MLP gagne sur la simplicité et la flexibilité des tokens. Q-Former gagne sur le budget des tokens.

> **【中文解读】**Le MLP en simplification et en flexibilité sur les jetons, Q-Former en jetons  budgétaire sur les jetons                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

> 🤔 **【困惑】**1) Pourquoi ne pas ajouter de Q-Former à LLaVA?加加复杂度变高、训练难度大、收益小(除非视频这样的标志 预算紧张场景)。2) LLaVA-1.5 和 LLaVA-NeXT

### Le format de commande

```
A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions. USER: <image> Describe this image in detail. ASSISTANT: The image shows ...
```

`<image>`Le Tokenizer voit une séquence légèrement plus longue qu'elle n'a été formée, mais le LLM gère la nouvelle entrée parce que l'étape 1 l'a appris.

> **【中文解读】** `<image>`Il est donc capable de traiter ces entrées jamais vues, c'est parce que la première phase de formation l'a enseigné à comprendre les représentations visuelles post-projection.

### Économie paramètre Économie paramètre

LLaVA-1.5-7B décomposition:
- CLIP ViT-L/14 @ 336: 303M (étape congelée 1, souvent défrichée étape 2 / 第一阶段结,第二阶段通常解).
- Projecteur (2x linéaire) / 投影器: ~22M entraînable / 可训练.
- Llama-7B: 7B.
- Total / 总计: 7,3B paramètres. Trainable pendant la phase 2 / Deuxième étape Trainable: projecteur complet 7B + 22M / 全部7B + 22M projecteur.

Coût de formation pour l'étape 2: ~ 20 heures sur 8xA100. C'est le numéro clé  un jour, un nœud, reproduisable. C'est pourquoi la LLaVA se propage.

> **【中文解读】**Deuxième étape Coût de formation: 8 张 A100 跑约20小时── c'est le chiffre clé一天──一台机器──可复现── c'est la raison pour laquelle LLaVA 能够迅速传播──
```figure
mm-llava-projector
```

## Utilisez-le

## Utilisez-le en pratique

`code/main.py`Les outils:`code/main.py`实现:

1. Le projecteur MLP à 2 couches (dim 16 → 32 → 32 pour l'échelle des jouets) en Python pur.
2. Le pipeline de construction rapide: système rapide + `<image>`remplacé par N des jetons projetés + tour d'utilisateur + placeholder de génération assistante.`<image>`替换为N个投影代币 + 用户轮次 + 助手生成占位符──
3. Un visualisateur pour voir à quoi ressemble le bloc visuel de 576 jetons dans le contexte LLM (pourcentage de 2k / 32k / 128k de contexte consommé).

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-llava-vibes-eval.md`. En raison d'un point de contrôle familial LLaVA, il utilise une suite de vibrations à 10 impulsions (3 sous-titres, 3 VQA, 2 raisonnements, 2 refus) et rapporte une carte de score lisible par l'homme.

> **【中文解读】**本课产 出 `outputs/skill-llava-vibes-eval.md` Donner un point de contrôle de la série LLaVA, exécuter 10 sujets de test "vibes-eval" avec 3 descriptions, 3 VQA, 2 propositions, 2 refus), générer des résultats artificiellement lisibles.

## Les exercices

1. Calculer le nombre de paramètres entraînables pour le projecteur MLP à 2 couches à `1024 → 4096 → 4096`Avec GELU et biais, quelle fraction de LLaVA-13B représente-t-il ?
   | 计算维度为 `1024 → 4096 → 4096` 的 2 层 MLP 投影器的可训练参数量。含 GELU 和 bias，它占 LLaVA-13B 的多少比例？

2. Construire une demande de réponse LLaVA pour un cas de "réjection"  l'image contient un particulier. Écrivez la réponse attendue de l'assistant. Pourquoi LLaVA devrait-elle refuser ce tir zéro et quelles données de formation seraient nécessaires pour renforcer le refus?
   | 为"拒绝"场景构建 LLaVA 提示词——图像包含私人个体。写出期望的助手回复。为什么 LLaVA 应该零样本拒绝？需要什么训练数据来强化拒绝行为？

3. Lisez la section AnyRes du blog LLaVA-NeXT. Comptez le nombre de jetons visuels pour une image 1344x672 à AnyRes. Comparer à la base 576 jetons à 336x336.
   | 阅读 LLaVA-NeXT 博客的 AnyRes 部分。计算 1344x672 图像在 AnyRes 下的视觉 token 数量，并与 336x336 基础设置的 576 个 token 比较。

4. Le projecteur LLaVA de phase 1 est entraîné avec une perte de LM sur les légendes. Que se passe-t-il si vous sautez la phase 1 et passez directement à la phase 2 (tonnement des instructions visuelles)?
   | LLaVA 第一阶段投影器用描述文本的语言建模损失训练。如果跳过第一阶段直接进入第二阶段会怎样？引用 Prismatic VLMs 消融实验（arXiv:2402.07865）回答。

5. LLaVA-Instruct-150k utilise GPT-4 avec des légendes COCO pour générer des instructions. Pour un nouveau domaine (rayons X médicaux, images satellites), décrivez le pipeline de données en quatre étapes pour générer des instructions de domaine.
   | LLaVA-Instruct-150k 用 GPT-4 从 COCO 描述生成指令。对于新领域（医疗X光、卫星图像），描述生成领域指令的四步数据管线。每步可能出什么问题？

## Les termes clés

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|----------------|------------------------|----------|---------|
| Projector | "MLP bridge" | 2-layer MLP with GELU mapping ViT dim to LLM dim | 投影器：将ViT维度映射到LLM维度的2层MLP | |
| Image token | "<image> placeholder" | Prompt marker replaced by N projected visual tokens before inference | 图像token：推理前被替换为N个投影视觉token的提示标记 | |
| Visual instruction tuning | "LLaVA stage 2" | Training on GPT-4-generated (image, instruction, response) triplets | 视觉指令微调：在GPT-4生成的（图像,指令,回复）三元组上训练 | |
| Stage 1 alignment | "Projector pretraining" | Freeze ViT and LLM, train projector with LM loss on captions | 第一阶段对齐：冻结ViT和LLM，用描述文本的LM损失训练投影器 | |
| AnyRes | "Multi-crop tiling" | Split high-res image into a tile grid and concatenate each tile's visual tokens | AnyRes：将高分辨率图像切分为网格，拼接各切片的视觉token | |
| LLaVA-Instruct | "GPT-4-generated" | 158k instruction-response pairs synthesized from COCO captions + GPT-4 | LLaVA指令数据：用COCO描述+GPT-4合成的158k指令-回复对 | |
| Vision encoder freeze | "Backbone locked" | CLIP weights do not update in stage 1, sometimes not in stage 2 either | 视觉编码器冻结：CLIP权重在阶段1不更新，有时在阶段2也不更新 | |
| ShareGPT4V | "Better captions" | 1M dense captions generated by GPT-4V, used for higher-quality alignment | 100万条GPT-4V生成的密集描述，用于更高质量的对齐 | |
| VQA | "Visual question answering" | Task of answering a free-form question about an image | 视觉问答：回答关于图像的自由形式问题 | |
| Prismatic VLMs | "Design-space paper" | Karamcheti 2024 ablation systematically testing projector and data choices | 系统测试投影器和数据选择的设计空间消融实验论文 | |

## Encore une lecture

- [Liu et al. — Visual Instruction Tuning (arXiv:2304.08485)](https://arxiv.org/abs/2304.08485)Le journal de la LLAVA.
- [Liu et al. — Improved Baselines with Visual Instruction Tuning (arXiv:2310.03744)](https://arxiv.org/abs/2310.03744)Il est en train de se faire une idée.
- [Chen et al. — ShareGPT4V (arXiv:2311.12793)](https://arxiv.org/abs/2311.12793) un ensemble de données de sous-titres denses. 密集描述数据集
- [Karamcheti et al. — Prismatic VLMs (arXiv:2402.07865)](https://arxiv.org/abs/2402.07865) Ablations de conception de l'espace.
- [Li et al. — LLaVA-OneVision (arXiv:2408.03326)](https://arxiv.org/abs/2408.03326) Unified single-image, multi-image, vidéo.
