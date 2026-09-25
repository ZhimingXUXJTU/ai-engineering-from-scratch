# Qwen-VL Famille et Dynamic-FPS Vidéo

> La famille Qwen-VL  Qwen-VL (2023), Qwen2-VL (2024), Qwen2.5-VL (2025), Qwen3-VL (2025)  est la lignée de modèles en langage de vision ouverte la plus influente en 2026. Chaque génération a fait un pari architectural décisif unique que le reste de l'écosystème ouvert a copié en douze mois: résolution dynamique native via M-RoPE, échantillonnage dynamique-FPS avec alignement temporel absolu, attention aux fenêtres dans le ViT, et formats de sortie d'agent structuré. Par Qwen3-VL, la recette s'était stabilisée: un encodeur 2D-RoPE-ViT avec des entrées natives de rapport d'aspect, un projecteur MLP dans une grande base de langage Qwen3, et des étapes de formation qui mettaient l'accent sur le comportement des agents OCR, de la mise à terre et des cibles de première classe. Cette leçon lit la famille chronologiquement pour que vous compreniez pourquoi chaque bouton est là où il est.

> **【中文解读】**La série Qwen-VL est la plus influente de la famille de modèles de langage open source de 2026[6]. Chaque génération a pris une décision d'architecture clé, adoptée par la communauté open source en 12 mois.

> **【拓展：Qwen-VL 的产业生态位】**Dans le domaine financier, Qwen2.5VL peut être utilisé pour comprendre les rapports financiers chinois, les OCR de dépôt de billets, ainsi que l'analyse vidéo.

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, M-RoPE encoder + dynamic-FPS sampler)  | **语言：Python（标准库，M-RoPE 编码器 + 动态帧率采样器）**
**Prerequisites:** Phase 12 · 06 (patch-n'-pack)  | **前置：阶段12第06课（补丁打包）**
**Time:** ~120 minutes  | **时长：约120分钟**

>  **【前置】**Je vous invite à maîtriser la phase 12 de la phase 06.
>  **【类比】**Qwen-VL 系列 = "中文 VLM 旗舰"──和 LLaVA 系列的区别:LLaVA 主打英文 + 简单架构;Qwen-VL 主打中英双语 + 高分辨率 + 结构化输出──如果你做中文场景(财报、合同、票据),Qwen-VL 是默认选择──
> ️ **【易错点】**Qwen-VL 输出边界框坐标时混"绝对像素 vs相对比例"不同代次使用不同约定──Qwen2-VL 用绝对像素(0-1000 范围),Qwen2.5-VL 改用归一化比例(0-1)──修复:使用前查文档,按代次正确解析坐标──

## Objectifs d'apprentissage

- Comptez les trois axes de rotation de M-RoPE (temporal, hauteur, largeur) et expliquez pourquoi ces trois axes sont nécessaires.
- Choisissez une stratégie d'échantillonnage FPS dynamique pour une vidéo et raisonnez sur la précision des jetons par seconde par rapport à la détection des événements.
- Nommez les quatre améliorations générationnelles de Qwen-VL dans l'ordre et ce que chacune a permis.
- Télécharger un format de sortie d'agent JSON de type Qwen2.5VL et analyser les appels d'outils structurés à partir d'une réponse VLM.

## Le problème , le contexte .

Qwen-VL a été expédié en août 2023 en réponse directe à LLaVA-1.5 et BLIP-2.

La résolution: LLaVA-1.5 fonctionnait à 336x336. Bien pour les photos, inutile pour une facture en chinois ou une capture d'écran de feuille de calcul dense. La première innovation de Qwen-VL était 448x448 et la sortie de boîte de délimitation à terre, laissant le modèle pointer sur les choses.

Vidéo: Video-LLaMA a empilé des encoders par cadre et les a alimentés au LLM. Il fonctionnait pour des clips courts, pas pour des vidéos de plusieurs minutes où l'axe temporel est le signal.

Exit structuré: LLaVA émet du texte de forme libre. Un agent a besoin de JSON. Qwen-VL est formé sur des formats de sortie JSON explicites, y compris les coordonnées de boîte de délimitation en tant que texte.

Chaque génération de Qwen-VL étend un de ces trois axes.

> **【中文解读】**Qwen-VL  trois grandes insuffisances de LLaVA-1.5 lancent un défi: 1) résolution 336x336  incapable de traiter en chinois 发票或密集表格截图; 2) vidéo 视频 视频 视频-LLaMA 只有能处理短片段; 3) 结构化输出 LLaVA 输出自由文本,代理需要 JSON──每一代 Qwen-VL 都在三个轴上延伸──

## Le concept de base.

### Qwen-VL (août 2023)

La première génération: OpenCLIP ViT-bigG/14 en tant qu'encodeur (2.5B params), Q-Former compatible avec LLama (1 étape avec 256 requêtes), Qwen-7B base. Contributions:

- La résolution de 448x448 (alors SOTA pour un VLM ouvert).
- "Le chat est à <box> 112, 204, (280, 344)</box>".
- En chinois + en anglais de formation multilingue dès le début.

Les critères de référence à l'époque: compétitif avec GPT-4V en anglais, dominant en chinois.

> **【中文解读】**Qwen-VL première génération de ruptures:448x448 résolution(supérieur à LLaVA 336x336)  capacité de positionnement(output bord bord bord bord bord bord bord bord bord)  中英双语──

### Qwen2-VL (septembre 2024)  M-RoPE et résolution native  Qwen2-VL: M-RoPE avec résolution de résolution de résistance

Qwen2-VL a remplacé la pile Q-Former à résolution fixe par un encodeur ViT à résolution dynamique natif.

- La résolution dynamique native / 原生动态分辨率. Le ViT accepte n'importe quel HxW divisible par 28 (parchage 14 avec fusion spatiale 2x). Une image à 1120x672 (40x24 parches fusionnées) produit 960 jetons visuels. Aucune taille, aucune carreaux, aucune miniature.
- M-RoPE (RoPE multimodale) / 多模态旋转位置编码. Chaque jeton porte une position 3D (t, h, w) au lieu de 1D. Pour les images t = 0, pour la vidéo t = frame_index. RoPE fait tourner les vecteurs de requête / clé par une fréquence par axe. Aucune table d'intégration positionnelle.
- MLP projecteur / MLP 投影器. Jetez le Q-Former; utilisez un MLP à deux couches sur les jetons de patch fusionnés.
- Vidéo avec FPS dynamique / 动态率视频. Vidéo échantillonné à 1-2 FPS par défaut, mais le modèle accepte le nombre d'images arbitraires.

Résultat: Qwen2-VL-7B a paré GPT-4o sur plusieurs critères de référence multimodal et l'a battu sur DocVQA (94,5 contre 88,4).

> **【中文解读】**L'architecture centrale de Qwen2-VL change: supprimer la résolution fixe + Q-Former, remplacer la résolution viT + M-RoPE + MLP  projecteur。M-RoPE pour chaque jeton  conférer une position 3D                                                                                                                                                                                                                                 

### Qwen2.5VL (février 2025)  FPS dynamique + temps absolu  Qwen2.5VL: taux d'activité  Rate +  Absolute temps

Le changement majeur de Qwen2.5VL était la vidéo.

- Les symboles de temps absolus / 绝对时间 token. Au lieu d'indices de position (cadre 0, 1, 2...), utilisez des timestamps réels. "À 0:04, le chat saute. " Le modèle voit `<time>0.04</time>`Les jetons sont interconnectés avec les jetons de cadre.
- Le modèle est à 1 FPS pour les images lentes, 4 FPS pour l'action. L'utilisateur ou l'entraîneur choisit; M-RoPE s'adapte.
- L'attention spatiale est mise en vitre (local dans les blocs) pour le débit; l'attention globale toutes les couches.
- Format de sortie explicite JSON / 显式 JSON 输出格式. Formé sur les données d'appel d'outils: `{"tool": "click", "coords": [380, 220]}`- L'agent est prêt. - L'agent est prêt.
- MRoPE-v2 évolue / MRoPE-v2 缩放. Les positions sont évolue avec la taille maximale de l'entrée afin qu'une vidéo de 10 minutes ne soit pas à court de la plage de fréquence.

Benchmarks: Qwen2.5-VL-72B dépasse GPT-4o sur la plupart des benchmarks vidéo, correspond à Gemini 2.0 sur les documents et définit le SOTA modèle ouvert pour la mise à terre de l'interface graphique (ScreenSpot: 84% de précision contre 38% pour GPT-4o).

> **【中文解读】**Le défi de Qwen2.5VL est de comprendre la vidéo: absolument le temps de jeton 让模型知道"第4秒猫跳了",动态率让模型在动作密集时自动提高采样率,窗口注意力提升 ViT 吞吐量──72B 版本在视频基准上超越GPT-4o,GUI 定位精度(ScreenSpot 84%)远超GPT-4o(38%)──

> **【拓展：结构化输出对 Agent 工程的意义】**Le module de perception visuelle de Qwen2.5VL est structuré en JSON, ce qui signifie que le VLM peut être directement utilisé comme un agent d'utilisation de l'ordinateur.

### Qwen3-VL (novembre 2025)

Qwen3-VL est une mise à niveau progressive qui consolide plutôt que réinvente: plus grande colonne vertébrale de la LLM (Qwen3-72B), données de formation élargies, OCR améliorée, raisonnement plus fort via le "mode de pensée" Qwen3.

Le résultat: en 2025, l'architecture Qwen-VL s'était stabilisée.

> **【中文解读】**Qwen3-VL est une augmentation de la mise à niveau et non une réinvention: plus de données de formation en LLM 骨干、更多训练数据、更好的OCR、更强的推理(Qwen3 "思考模式")。ViT 和 M-RoPE 保持不变──到2025年, la structure de Qwen-VL est déjà stable, la version ultérieure se développe principalement par l'expansion de la taille et l'optimisation des données。

### Je suis un mathématicien.

Le RoPE classique fait tourner une requête `q`de dimension `d`par position `m`en utilisant des coordonnées parées:

```
q_rot[2i]   = q[2i]   * cos(m * theta_i) - q[2i+1] * sin(m * theta_i)   # 经典 RoPE 旋转
q_rot[2i+1] = q[2i]   * sin(m * theta_i) + q[2i+1] * cos(m * theta_i)
theta_i     = 10000^(-2i/d)                                                 # 频率基
```

M-RoPE divise le flou caché en trois bandes.`d = 96`. Assigner 32 décimaux à la température, 32 à la hauteur, 32 à la largeur. Chaque bande tourne par sa propre position d'axe.`R_t(5)`- Je suis là .`R_h(10)`- Je suis là .`R_w(20)`appliqué à ses trois bandes.

Utilisation de jetons texte `t = text_index, h = 0, w = 0`(ou un choix normalisé), en gardant la compatibilité.`t = frame_time, h = row, w = col`. Utilisation d' images uniques `t = 0`- Je suis désolé .

L'avantage: un codeur de position traite le texte, l'image et la vidéo sans brancher le code ou les tables de position différentes.

> **【中文解读】**M-RoPE va concevoir la dimension divisée en trois fréquences (temps, hauteur, largeur), chaque fréquence se déplace selon son axe de position.

### Logique de prélèvement d'échantillons FPS dynamique

Vu la durée de la vidéo `T`secondes et un budget de jetons cibles `B`- Le numéro de la liste:

1. Calculez le FPS maximum que vous pouvez vous permettre: `fps_max = B / (T * tokens_per_frame)`. . . Calculer le taux maximum de dépôt .
2. Choisissez une FPS cible .`{1, 2, 4, 8}`qui satisfait `fps <= fps_max`Je suis un homme de la classe des candidats.
3. Si le mouvement est élevé (heuristique de flux optique ou demande explicite de l'utilisateur), choisissez un FPS plus élevé. Si le mouvement est faible, choisissez un moindre.
4. Prîtres uniformes au SPF choisi; insérer `<time>t</time>`Les jetons entre les cadres.

Qwen2.5-VL entraîne cette logique implicitement; à l'inférence, l'utilisateur contrôle via `fps`Paramètre: une séquence d'action de 60 secondes à 4 FPS avec 81 jetons par cadre = 19440 jetons, gérable dans un contexte de 32k.

> **【中文解读】**动态率的核心思想:根据视频时长、代币 预算和运动量,自动选择最佳率──60秒动作场景在4FPS下产生19440代币,可在32k上下文中处理──

### Les agents structurés sont sortis.

La formation des agents de Qwen2.5VL vise explicitement les appels structurés aux outils:

```
{
  "tool": "mouse_click",          # 工具名称
  "coords": [1024, 512],          # 点击坐标
  "button": "left",               # 鼠标按钮
  "modifier": null                # 修饰键
}
```

Le parsing est déterministe: JSON.parse sur la sortie du modèle. Comparer à la forme libre "cliquez à (1024, 512) " qui nécessitait un traitement de régex et d'ambiguïté. Le changement est la raison pour laquelle les scores ScreenSpot de Qwen2.5-VL ont sauté de 55% à 84%.

> **【中文解读】** Structured output 让VLM可以直接发发出可解析的工具调用 (如点击坐标),无需正则表达式──这是ScreenSpot 精度从55% 跳到84%的关键原因──
```figure
mm-mrope-axes
```

## Utilisez-le

## Utilisez-le en pratique

`code/main.py`les implémentations:

- M-RoPE position calcul pour une séquence emballée mélangeant texte, patches d'image et cadres vidéo.
- Pratiquer le temps de l'échantillon dynamique-FPS: donné (durée, budget, niveau de mouvement), choisir FPS et émettre des timestamps de cadre.
- Un analyseur de sortie JSON Qwen2.5VL qui gère les réponses aux appels avec des champs de coordonnées.

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-qwen-vl-pipeline-designer.md`. En fonction d'une tâche vidéo (surveillance, agent, reconnaissance d'action, accessibilité), il émet la configuration Qwen2.5 VL (budget de cadre, stratégie FPS, drapeau d'attention de fenêtre, mode agent-output) et une estimation de latence.

> **【中文解读】**Le projet de loi de la Commission sur les mesures de lutte contre les émissions de gaz et de gaz aériens (CPC) a été adopté par le Conseil européen des régions de l'Europe centrale et orientale.

## Les exercices

1. Comptez les rotations M-RoPE pour un patch à (t=3, h=5, w=7) avec 48 cachés (16 par bande, theta 10000 de base).
   | 计算 (t=3, h=5, w=7) 补丁的 M-RoPE 旋转，隐藏维度48（每频段16），基数10000。展示每频段前三对的旋转角度。

2. Une caméra de sécurité enregistreur à 1 FPS à 10 minutes produit combien de images ? à 384 résolution avec 3x pool, combien de jetons totaux ?
   | 10分钟安防摄像头录像在 1FPS 下产生多少帧？384分辨率+3x池化后多少 token？Qwen2.5-VL 默认 32k 上下文能处理吗？

3. Choisissez FPS pour un rallye de tennis de 30 secondes contre une démo de recette de 30 secondes contre un enregistrement d'agent d'interface utilisateur de 30 secondes.
   | 为 30 秒网球比赛、30 秒食谱演示、30 秒 UI 代理录像选择帧率。用动态帧率逻辑论证每个选择。

4. Qwen2.5VL dépose entièrement le Q-Former. Pourquoi un simple MLP fonctionne-t-il en 2025 mais pas en 2023?
   | Qwen2.5-VL 完全去掉了 Q-Former。为什么 MLP 在 2025 年可行但 2023 年不行？（提示：数据规模和编码器质量。）

5. Pars trois sorties d'appels d'outil JSON Qwen2.5-VL dans les dicts Python. Qu'est-ce qui manque pour JSON malformé et quelle stratégie de récupération recommande le livre de cuisine Qwen?
   | 将三个 Qwen2.5-VL JSON 工具调用输出解析为 Python 字典。畸形 JSON 会出什么问题？Qwen 食谱推荐的恢复策略是什么？

## Les termes clés

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| M-RoPE | "Multimodal RoPE" | 3D rotary position embedding with temporal, height, and width bands in the hidden dim | 三维旋转位置编码，隐藏维度分时间、高度、宽度三个频段 | |
| Dynamic FPS | "Smart sampling" | Frame sampling rate chosen per video based on motion, duration, and token budget | 根据运动量、时长和 token 预算动态选择帧率 | |
| Absolute time token | "Timestamp token" | `<time>t</time>` interleaved in the sequence so the model sees actual seconds not frame index | 在序列中插入真实时间戳 token | |
| Window attention | "Local attention" | Spatial self-attention restricted to small windows for speed; global attention added periodically | 空间自注意力限制在小窗口内加速，周期性加入全局注意力 | |
| Structured agent output | "JSON mode" | Training data supervision teaching the VLM to emit parseable JSON with coords and tool names | 训练 VLM 输出可解析的 JSON（含坐标和工具名） | |
| min_pixels / max_pixels | "Resolution bounds" | Per-request Qwen2.5-VL controls bounding total pixel count and therefore token count | 按请求控制最小/最大像素数从而控制 token 数 | |
| Grounding | "Point-at-it" | Outputting bounding-box coordinates as text tokens; used since Qwen-VL v1 | 输出边界框坐标作为文本 token，从 Qwen-VL v1 开始支持 | |

## Encore une lecture

- [Bai et al. — Qwen-VL (arXiv:2308.12966)](https://arxiv.org/abs/2308.12966)Je suis un homme de la première génération.
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191)Je suis un homme qui a une vieille fille.
- [Qwen Team — Qwen2.5-VL Technical Report (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923)Je suis un homme qui a une bonne idée.
- [Qwen Team — Qwen3-VL (arXiv:2511.21631)](https://arxiv.org/abs/2511.21631)Je suis en train de faire une mise à niveau de Qwen3VL.
- [Zhu et al. — InternVL3 (arXiv:2504.10479)](https://arxiv.org/abs/2504.10479)Je suis un homme qui a des problèmes avec la police.
