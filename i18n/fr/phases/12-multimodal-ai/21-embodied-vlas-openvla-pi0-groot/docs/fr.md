# VLA incorporés: RT-2, OpenVLA, π0, GR00T 具身 VLA: vidéo-langue-motion modèle avec contrôle de l'ordinateur

> La première fois qu'un modèle a lu une recette sur un site Web et l'a exécutée dans un robot de cuisine a été RT-2 (Google DeepMind, juillet 2023). RT-2 a discrétisé les actions en tant que jetons de texte, co-finitionné un VLM sur les données Web plus les données d'action robot, et prouvé que la connaissance du langage de vision à l'échelle Web transfère au contrôle robotique. OpenVLA (juin 2024) a expédié la référence 7B ouverte. La série π0 de Physical Intelligence (2024-2025) a ajouté des experts en action de correspondance de flux. Le GR00T N1 de NVIDIA (mars 2025) a fourni un contrôle à double système (Système 1 / Système 2) pour les robots humanoïdes à grande échelle. Le VLA primitif  vision-langue-action, un modèle unique qui voit, lit et agit  est le pont entre les modèles de compréhension de cette phase et les systèmes autonomes de la phase 15.

> **【中文解读】**RT-2  Première preuve de la connaissance du langage visuel de niveau réseau pouvant être transférée au contrôle de l'ordinateur:将关节动作分散化为文代币,与VLM 联合微调――OpenVLA 是开源 7B 参考,π0 引入流匹配动作专家,GR00T N1 实现双系统(快思考/慢思考) 人形机器人控制──VLA(视觉-语言-动作) est un pont de communication entre la compréhension et le système autonome──

> **【拓展：Embodied VLA 到机器人产业】**Le modèle VLA est en train de passer du laboratoire à l'industrie: Tesla Optimus, Figure 01  1X Technologies et autres entreprises d'ordinateurs sont en train de développer un système de contrôle basé sur VLA. Dans le cadre de l'industrie, VLA peut être utilisé pour les machines de stockage, les machines d'installation, etc. Le défi principal est la sécurité et la fiabilité.

**Type:** Learn
**Languages:** Python (stdlib, action tokenizer + VLA inference skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 15 (Autonomous Systems, referenced)
**Time:** ~180 minutes

>  **【前置】**Pour les autres, il est nécessaire de se préparer à la phase 12 de la phase 15 du système de gestion de l'environnement.
>  **【类比】**VLA = " donner à un ordinateur un appareil à la fois à l'esprit et aux yeux "。 traditions 机器人 = 程序员写死 if-else 规则(看红色就停下); VLA = 像人看图说话做事("把红杯放到桌上"→看杯→规划路径→控制关节执行)。RT-2 Placez l'opération dispersée en jeton = Placez l'opération comme un texte dans un prompt;π0 流匹配 = 输出连续动作而非 dispersée jeton, plus précisément。

## Objectifs d'apprentissage

- Décrire la tokenization d'action: codage discrète en bin (RT-2), jetons d'action efficaces FAST, actions de correspondance continue des flux (π0).
  Le mot d'ordre est "réaction" et "réaction".
- Expliquez pourquoi la co-finition des données sur le web + les robots préserve le transfert de connaissances générales vers de nouvelles tâches.
  Expliquer pourquoi les données des ordinateurs et des pages Web+ peuvent être utilisées pour maintenir la capacité de transférer les connaissances vers de nouvelles tâches.
- Comparer OpenVLA (ouverte 7B Llama+VLM), π0 (correspondance de flux) et GR00T N1 (dual-système) sur la même tâche robot.
  Le système de gestion de la gestion des données est un système de gestion de données qui est utilisé pour la gestion des données.
- Nombre de données sur l'Open X-Embodiment et son rôle de corps de formation RT-X.
  Le rôle de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de l'équipe de l'équipe de formation de l'équipe de formation de l'équipe de l'équipe de formation de l'équipe de référencencencadrille de formation du groupe de formation du groupe de formation du groupe de formation du groupe de formation.

## Le problème , l' introduction du problème

Un robot qui fait des tâches ménagères à partir d'instructions de langage naturel a été une cible de recherche depuis les années 1970. La réponse des années 2020: un modèle d'action de langage de vision (VLA). La même architecture VLM utilisée pour VQA, mais la sortie est des actions (tombes conjoints, poses d'effet de fin, commandes discrètes) au lieu de texte.

> L'utilisation de l'ordre de la langue naturelle pour faire des machines à la maison depuis les années 1970 est l'objectif de la recherche.

Défis spécifiques aux VLA:

> Les défis particuliers de la VLA:

1. Les espaces d'action sont continus (angle commun, forces) et à haute dimension (7 bras DOF + poignée 3-DOF = 10 dims à 30 Hz).
   Le nombre de branches de l'espace est de 7 à 10 dimensions.
2. Les données de formation spécifiques aux robots sont rares. Open X-Embodiment a environ 1M de trajectoires; image de texte Web est 5B+.
   Le système X-Embodyment est ouvert à environ 100 millions de trajets; pages Web
3. La fréquence de contrôle est importante.
   Le contrôle de fréquence est important. 30 Hz.
4. Une mauvaise action endommage le matériel, les personnes ou les biens.
   Les erreurs de la conduite sont des erreurs de la conduite.

## Le concept de base.

> **【中文解读】**Le modèle de VLA est le modèle représentatif de la VLA, de la Pi0 (Intelligence physique) et de la NVIDIA Groot.

> **【拓展：具身智能的进展**OpenVLA-7B sur Google Robot pour réaliser environ 80% des tâches de succès. Pi0 utilise le flux correspondant pour générer des trajectoires de continuité, plus lisses que les opérations de démarrage traditionnelles. NVIDIA Groot se concentre sur les robots humains. Le défi principal de l'intelligence est la rareté des données.


### Tokenization des actions (RT-2)

RT-2: représente chaque cible conjointe comme un jeton de texte quantifié. Discrète la plage normalisée [-1, 1] en 256 poubelles, carte chaque poubelle à un ID vocabulaire. Une action de 10 DOF devient 10 jetons à chaque étape de contrôle.

> RT-2: mettre chaque section dans un code de référence. La portée de chaque code est de 256 bits, chaque bits étant définies en un code de référence.

Co-finition d'un VLM PaLM-X sur un mélange:

> Dans les données mixtes, les modèles PaLM-X VLM:

- Parmi les éléments suivants, il y a:
  Le texte de la première page est le texte de la première page.
- Des démonstrations de robots, des actions en tant que jetons.
  Le mot "défense" est traduit par "défense".

Le modèle voit " pick up the red cube " (langue) → image (vision) → séquence d'action de 10 jetons (objectifs conjoints discrétisés). Le prétrainage Web préserve le transfert de connaissances générales: RT-2 peut suivre " le mouvement vers l'objet en mouvement rapide " même si " le mouvement rapide " n'est pas dans les données de formation.

> 模型看"拿起红色方块" (en anglais) 图像 (en anglais) 视觉 (en anglais) 图像 (en anglais) 视觉 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像 (en anglais) 图像) 图像 (en anglais) 图像) 图像 (en anglais) 图像) 图像 (en anglais) 图像) 图像) 图像 (en anglais) 图像) 图像 (en anglais) 图像) 图像) 图像 (en anglais) 图像) 图像) 图像 (en anglais) 图像) 图像) 图像 (en anglais) 图像) 图) 图) 图) 图) 图) 图) 图) 图) 图) 图 (en anglais) 图) 图) 图) 图 (en anglais) 图) 图) 图) 图 (en anglais) 网页 (from French) 页 (from French)  }} }} [from French) }} [from French) }} [from French) }} [from French

L'inference à 3-5 Hz dans le papier RT-2, limitée par le décode autorégressif VLM.

> RT-2 论文中推理速度 3-5 Hz, limité à VLM 自归解码──

### OpenVLA  la référence 7B ouverte

OpenVLA (Kim et coll., juin 2024) est l'équivalent RT-2 à poids ouvert. 7B Llama spine dorsale, DINOv2 + SigLIP double vision encodeur, action Tokenization sur 256 poubelles.

> OpenVLA est un outil de programmation de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture de l'écriture.

Formé sur Open X-Embodiment (970 000 trajectoires sur 22 robots).

> Dans le cadre de la formation du système X, 22 appareils ont été installés.

Inference: 4 à 5 Hz sur un A100 avec quantification.

> 推理:A100 上量化后 4-5 Hz──对慢速操作足够,不适合高频控制──

### FAST Tokenizer  décodeur d'action plus rapide

Pertsch et coll. (2024) ont montré que la jetonisation discrète bin est inefficace  la plupart des actions se regroupent dans une petite région de bin-space. FAST (Frequency-domain Action Sequence Tokenizer) comprime les séquences d'action via DCT et quantifie les coefficients.

> Pertsch 等人(2024) indique le taux de détachement de bin par par le nombre de mots de la plupart des mouvements se rassemblent dans les petites régions de bin 空间──FAST(频域动作序列分词器)

Une trajectoire d'action de 30 étapes devient ~ 10 jetons FAST au lieu de 300 jetons discret-bin.

> 30 étapes de trajet se sont transformées en 10 jetons FAST, plutôt que 300 jetons de bin dispersés.

### π0 et actions de correspondance des flux

Le π0 de Physical Intelligence (Black et al., octobre 2024) remplace les jetons d'action discrets par un expert en action de correspondance de flux:

> Le jeton d'opération de l'intelligence physique:

- Un petit transformateur d'action lit les états cachés du VLM et produit une séquence d'action continue de 50 étapes via un flux rectifié.
  Transformer 读取 VLM 隐藏状态, 通过正流输出连续的50 步动作序列──
- La tête d'action s'entraîne avec une perte de correspondance de débit; la VLM reste inchangée avant l'entraînement.
  Le train de l'équipe de formation est en train de se détériorer.
- Inference: séquence d'action complète émise en ~5 étapes dénonciatrices, contrôle efficace à 50 Hz.
  Le système de commande est en train de se dérouler à environ 5 pas.

L'acte continu de la formulation préserve la douceur que la discrétion détruit.

> π0 声称: sur une large échelle de tâches d'exploitation, il a vaincu OpenVLA et Octo.

> **【中文解读】**π0 Utilisation de flux de correspondance de séquence de mouvement de remplacement: un petit mouvement Transformer 读取 VLM 隐藏状态, via 正流输出连续的50 步动序列──推理时只需约5步去噪音,实现效率等效50Hz 控制频率──连续动作表达保留了散化会破坏的动作平滑性──

π0.5 et π0-FAST sont des améliorations progressives. π0-FAST combine la symbolisation FAST avec le flux de correspondance.

> π0.5 et π0-FAST est la croissance de la croissance.

### GR00T N1  système double pour les humanoïdes

Le GR00T N1 (mars 2025) de NVIDIA est conçu pour les robots humanoïdes (> 30 DOF, corps complet):

> GR00T N1 de NVIDIA pour un design en forme humaine:

- Système 2: une grande scène de lecture VLM + instruction, produisant des sous-objectifs de haut niveau à ~ 1 Hz.
  Le système de gestion des données de l'entreprise est un système de gestion des données de l'entreprise.
- Système 1: un petit transformateur à tête d'action produisant des commandes conjointes de bas niveau de 50 à 100 Hz conditionnées sur les sous-objectifs.
  Le système de transformation est un petit mouvement de tête.

Les cartes divisées à Kahneman de la pensée rapide et lente: Système 2 plans, Système 1 agit.

> Le système 2 planification, système 1 exécution  avantages: le planning lent VLM ne bloquera pas le contrôle rapide; le système 1 maintient une petite échelle pour assurer un retard faible

GR00T N1.7 (fin 2025) améliore l'évolutivité des données. GR00T est affiné avec des données sim-to-real de l'Omniverse.

> GR00T N1.7 ((2025 année de fin) a amélioré l'expansion des données. Gr00T utilise Omniverse pour effectuer des modifications.

### Le corps X ouvert

Les données de formation. RT-X (octobre 2023) a assemblé 22 ensembles de données couvrant 1M de trajectoires sur 22 robots. Open X-Embodiment est le corpus que tout le monde utilise:

> 训练数据──RT-X(2023 年 10 月) a regroupé 22 collections de données, couvrant 100 000 条轨迹 de 22 机器人──Open X-Embodiment est le langage utilisé par tous:

- ALOHA / Bridge V2 / Droid / RT-2 Cuisine / Tableau de langue.
  Le nom de la ville est le nom de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville de la ville.
- Chaque échantillon: (état du robot, vue de la caméra, instruction, séquence d'action).
  Le texte de la lettre de la première lettre est écrit en français.
- L'hygiène de formation: unifier l'espace d'action, normaliser les rangées articulaires, redimensionner les caméras.
  Le nombre de photos de la vidéo est de plus de 100 000 personnes.

OpenVLA et π0 se développent sur Open X-Embodiment.

> OpenVLA et π0 dans Open X-Embodiment

### Co-ajustement par rapport aux robots seulement

Le co-ajustement mélange les données VQA web avec les trajectoires des robots. Le rapport importe: trop de VQA et le modèle oublie les actions; trop de données robot et le modèle perd les connaissances générales.

> 联合微调将网页 VQA 数据与机器人轨迹混合──比例很重要:VQA 太多模型忘记动作;机器人数据太多模型失去通用知识──

Le rapport RT-2 est un hyperparamètre à régler par taille de jeu de données.

> RT-2 est en proportion d'environ 1:1[6].OpenVLA est en proportion d'environ 0.5:1[6].

L'entraînement robot seulement produit des modèles spécifiques à la tâche qui échouent sur les instructions hors de distribution. Co-finition est la différence entre "pick up the red cube (en démo) " et "pick up the third largest object from the left (novel phrasing)".

>                                                                                                                                                                                                                                                               

### Limits de sécurité et d'action

Chaque VLA de production est équipée de:

> Chaque VLA de production est équipé:

- Limits d'articulation dures (ne peut pas dépasser le couple spécifique).
  Le caractère strict de la loi est un caractère strict.
- Limite de vitesse (coupe douce).
  Le mot "déconnexion" est traduit par "déconnexion".
- Limits de l'espace de travail (l'éffecteur final ne peut pas quitter la table).
  Le terminal de l'exécuteur ne peut pas quitter la table.
- Approbation humaine en cours pour des tâches nouvelles.
  Le projet de loi de la République de Chine est en cours de révision.

Ces éléments sont placés à l'extérieur du VLA comme contrôles de couche de contrôle.

> Ces contrôles sont effectués à l'extérieur du VLA.

## Utilisez-le avec le cadre de réalisation
```figure
mm-action-tokens
```

## Utilisez-le

`code/main.py`- Le numéro de la liste:

- Il met en œuvre la tokenization et la détokenization d'action 256 bin.
  Le mot chinois traduit par " réaliser " est " réaliser " 256 bin 动作分词化和反分词化。
- Dessine un jeton FAST basé sur la quantification DCT +.
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la
- Comparer le nombre de jetons par étape d'action (bin discrète, FAST, flux continu).
  Le nombre de symboles de chaque étape est de trois manières:
- Imprime un résumé de lignée de RT-2 → OpenVLA → π0 → GR00T.
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-vla-action-format-picker.md`. En raison d'une tâche robot (manipulation, navigation, corps entier humanoïde), choisissez entre bin discret + RT-2, FAST + OpenVLA, flux-matching + π0, ou système double + GR00T.

> 本课产 出 `outputs/skill-vla-action-format-picker.md`◊ given given machine tasks (operation, navigation, personnage), dans le cas où le système est différent + RT-2 ≈ FAST + OpenVLA ≈ Rue correspondance +π0 ou + GR00T ≈

## Les exercices

1. Un bras 10 DOF à 30 Hz de contrôle. La jetonisation discrète-bin à 256 pouces émet combien de jetons par seconde? un VLM 7B peut-il suivre? 10 liberté de bras mécanique, 30 Hz de contrôle fréquence, 256 fréquence de détachement.

2. La symbolisation rapide comprime les trajectoires de 30 étapes à ~ 10 jetons. Que perd l'utilisateur si la trajectoire a un mouvement à haute fréquence (par exemple, le tambour)?

3. Le débit de la tête de correspondance de π0 se détériore en ~5 étapes.

4. Le système 1 / système 2 de GR00T divise les cartes de Kahneman. Proposez une division différente (système 3?) qui pourrait aider à marcher à deux pieds. GR00T's système1/ système2 se démarque contre la théorie de la carte.

5. Lisez la section 4 sur la conservation des ensembles de données. Nommez les trois règles de conservation qui empêchent la fuite de domaine.

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| VLA | "Vision-language-action" 视觉-语言-动作模型 | Model that takes image + instruction and outputs action commands 接受图像+指令并输出动作命令的模型 | |
| Action tokenization | "Discrete bins" 离散 bin 编码 | Quantize continuous joint targets into 256 bins per dim, each a vocab ID 将连续关节目标量化为每维 256 个 bin，每个 bin 对应一个词表 ID | |
| FAST tokenizer | "Frequency action tokens" 频域动作 token | DCT + quantize to compress 30-step trajectories to ~10 tokens 用 DCT + 量化将 30 步轨迹压缩为约 10 个 token | |
| Co-fine-tune | "Mix web + robot" 混合微调 | Train on web VQA data alongside robot demos to preserve general knowledge 在网络 VQA 数据和机器人演示上联合训练以保留通用知识 | |
| Flow-matching action head | "pi0 continuous output" 流匹配动作头 | Small transformer that outputs a 50-step action sequence via rectified flow 通过矫正流输出 50 步连续动作序列的小型 Transformer | |
| System 1 / System 2 | "Dual-system control" 双系统控制 | Large VLM plans slowly, small action head acts quickly; GR00T pattern 大 VLM 慢规划，小动作头快执行；GR00T 模式 | |
| Open X-Embodiment | "RT-X dataset" 开放具身数据集 | 1M-trajectory cross-robot dataset; the training corpus 100 万轨迹跨机器人数据集；标准训练语料 | |

## Encore une lecture

- [Brohan et al. — RT-2 (arXiv:2307.15818)](https://arxiv.org/abs/2307.15818)
- [Kim et al. — OpenVLA (arXiv:2406.09246)](https://arxiv.org/abs/2406.09246)
- [Black et al. — π0 (arXiv:2410.24164)](https://arxiv.org/abs/2410.24164)
- [NVIDIA — GR00T N1 (arXiv:2503.14734)](https://arxiv.org/abs/2503.14734)
- [Open X-Embodiment Collab — RT-X (arXiv:2310.08864)](https://arxiv.org/abs/2310.08864)
