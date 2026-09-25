# Compréhension du document et du diagramme  archives et diagrammes compréhension

> Les documents ne sont pas des photos. Un PDF, un document scientifique, une facture ou un formulaire manuscrit ont une disposition, des tableaux, des diagrammes, des notes de bas de page, des en-têtes et une structure sémantique que la compréhension d'une image simple ne peut pas saisir. La pile pré-VLM était un pipeline: Tesseract OCR + LayoutLMv3 + heuristiques d'extraction de table. La vague VLM a remplacé celle-ci par des modèles sans OCR  Donut (2022), Nougat (2023), DocLLM (2023)  qui émettent directement une marquage structurée. En 2026, la frontière est simplement "alimenter l'image de page à Claude Opus 4.7 à 2576px natif", et la sortie de marquage structuré est gratuite. Cette leçon est le cours de l'Arc de l'IA de trois époques.

> **【中文解读】**文档不是照片──PDF、论文、发票、手写表单有布局、表格、图表、脚注、标题等语义结构,普通图像理解无法捕捉──文档 AI 经历了三个时代:(1) OCR 管道(Tesseract + LayoutLMv3);(2) OCR-free(Donut、Nougat 直接从图像生成结构化输出);(3) VLM 原生(2026年直接将页面图像给Claude Opus 4.7 即可)

> **【拓展：文档理解在金融领域的应用】**金融场景是文档 AI's (最重要的应用领域之一:发票解析)                                                                                                                                                                                                                                                     

**Type:** Build
**Languages:** Python (stdlib, layout-aware document parser skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 5 (NLP)
**Time:** ~180 minutes

>  **【前置】**Il est également important de comprendre la phase 12 de la série de documents de la VLM.
>  **【类比】**文档理解三时代 = "développement des rapports comptables"。OCR 管道 = 人工核对+表格软件(先识别文字再解析布局);OCR-free(Donut) = intégration de logiciels(看图直接生成结构化数据);VLM 原生(Claude) = 全能AI(看图就能理解,回答、推理,无需专门训练)。
> ️ **【易错点】**简单 OCR 任务用VLM = 杀用牛刀(成本10倍) 例如纯文本发票用Tesseract + LayoutLMv3 只需几分钱,使用GPT-4V 要几毛钱──修复:先评估任务复杂度,简单的OCR管道,复杂的(手写、混合布局、多语言)才上VLM──

## Objectifs d'apprentissage

- Expliquez les trois époques de l'IA du document: pipeline OCR, libre de OCR, VLM-native.
  Le système d'exploitation de l'IA est un système de gestion de la vie et de l'énergie.
- Décrivez les trois flux d'entrée de LayoutLMv3: texte, mise en page (bbox), correctifs d'image, avec masquage unifié.
  Le modèle de l'image est un modèle de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image de l'image.
- Comparez Donut (sans OCR, image → marquage), Nougat (papier scientifique → LaTeX), DocLLM (génératif en connaissance de mise en page), PaliGemma 2 (natif VLM).
  Le texte de la première partie de la série est le texte de la première partie de la série.
- Choisissez un modèle de document pour une nouvelle tâche (factures, documents scientifiques, formulaires manuscrits, reçus chinois).
  Le texte est écrit en français et en français.

## Le problème , l' introduction du problème

"Comprendre ce PDF" est trompeur.

> "Comprendre ce PDF" semble simple, il est difficile.

- Contenu du texte (90% du signal).
  Le texte est en français.
- L'élaboration (titres, notes de bas de page, barres latérales, format de deux colonnes).
  Le texte est écrit en français.
- Tableaux (lignes, colonnes, cellules fusionnées).
  Le mot grec traduit par "seigneur" signifie "seigneur".
- Des chiffres et des diagrammes.
  Le texte est en français.
- Des notes écrites à la main.
  Le mot "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire "c'est-à-dire" est un mot qui signifie "c'est-à-dire" ou "c'est-à-dire" ou "c'est-à-dire" ou "c'est-à-dire" ou "c'est-à-dire" est un mot qui signifie "c'est-à-dire" ou "c'est-à-dire" ou "c'est-à-dire" est un mot qui signifie "c'est" ou "c'est" ou "c'est" ou "c'est"
- Fonts et typographie (titre contre corps).
  Le texte est en français.

Un système qui se soucie des factures doit savoir que "Total: $1.245" est venu du bas à droite, pas d'une note de bas de page.

> Le système de vote a besoin de savoir "total: $1,245" vient du coin droit, et non du script.

## Le concept de base.

> **【中文解读】**La compréhension du document et du graphique est une application importante de l'IA à plusieurs modes: OCR, présentation, extraction, processus, explication, formule d'identification, etc.

> **【拓展：文档 AI 的工业应用**文档 AI 市場巨型:合同审核、发票处理、学术论文分析等──GPT-4o sur DocVQA atteint 92,8%,InternVL2-26B atteint 92,7%(Open Source最优)──MarkItDown (Microsoft) va transformer le document en Markdown,ColPali avec la méthode visuelle pour remplacer la tradition OCR 管线──


> **【拓展：文档理解的技术路线】**文档理解有两条路线:(1) OCR-first(先用 OCR 提取文本,再用 LLM 处理)适合纯文文文文档;(2) Vision-first(直接用 VLM 处理文档图像)适合包含图表、表格的复杂版面── GPT-4o 和 InternVL2 走 Vision-first 路线,在复杂文档理解上表现更好──


### Époque 1  L'oléoduc OCR (avant 2021)

La pile classique:

> 经典技术:

1. PDF → image par page.
   Le texte de la première page est le même que celui de la deuxième page.
2. Tesseract (ou OCR commercial) extrait du texte avec des boîtes de délimitation par mot.
   Le texte est écrit en français et en français.
3. L'analyseur de mise en page identifie les blocs (titre, tableau, paragraphe).
   Le code de la page d'accueil est le code de la page d'accueil.
4. Le reconnaisseur de structure de table partage les tables.
   Le système de reconnaissance de structure est un système de reconnaissance de structure.
5. Règles de domaine + champs d'extrait de régex.
   Le texte de la loi est le texte de la loi.

Fonctionne pour un texte imprimé propre. Faites une pause sur l'écriture, des scans déformés, des tables complexes, des scripts non anglais. Chaque mode d'échec nécessite un chemin d'exception personnalisé.

> 适用于清洁印刷文本──在手写、倾斜扫描、复杂表格、非英文文字上失败──每种失败模式都需要自定义异常处理──

### Régime de contrôle des risques

Le TROCR (Li et al., arXiv:2109.10282) a remplacé le classique CNN-CTC de Tesseract par un transformateur encodeur-décodeur formé sur des images de texte synthétiques + réelles.

> Le transformer 编码器-解码器 a remplacé le classique CNN-CTC de Tesseract. Il a obtenu des avantages évidents sur la main-d'œuvre et le texte multilingue.

### Ére 2  exempte de RCO (2022-2023)

Les premiers modèles sans OCR disaient: sauter la détection entièrement, cartographier les pixels d'image à la sortie structurée directement.

> Première génération sans OCR 模型 proposé: complètement sauter sur le contrôle, directement le cartographie des images pour la sortie structurée.

Donuts (Kim et coll., arXiv:2111.15664):
- Transformateur de décodeur-encodeur, le codeur est Swin-B.
- La sortie est JSON pour la compréhension des formes, le décompte pour la résumé ou tout schéma spécifique à la tâche.
- Pas de RCR, pas de mise en page, pas de détection.

> Donut:编码器-解码器 Transformer,编码器为Swin-B──输出是 JSON(表单理解)、markingdown(摘要) 或任务特定方案──无需 OCR、无需布局、无需检测──

Nougat (Blecher et coll., arXiv:2308.13418):
- Formé spécifiquement sur des documents scientifiques.
- La sortie est LaTeX / marquage.
- Il traite des équations, des lignes de plusieurs colonnes, des chiffres.
- Le modèle que chaque arXiv parser appelle.

> Nougat: spécialisé dans les travaux scientifiques.

Les spécialistes, pas les généralistes, les donuts sur un article scientifique échouent, les nougat sur une facture échouent.

> Ces sont des modèles spécialisés, pas des talents.

### L'élaboration de l'équipe

L'arrangementLMv3 (Huang et al., arXiv:2204.08387) conserve l'OCR mais ajoute la compréhension de la mise en page:

> L'équipement de la LCV3 est conservé en OCR mais l'équipement est compréhensible.

- Trois flux d'entrée: des jetons de texte OCR, des boîtes de délimitation 2D par jeton, des correctifs d'image.
  Le code de référence est le code de référence de chaque code de référence.
- Objectif de formation masquée dans les trois modalités (texte masqué, correctifs masqués, mise en page masquée).
  Le code de la ligne de travail est le code de la ligne de travail.
- En aval: classification, extraction d'entités, tableau QA.
  Le groupe de travail est composé de deux groupes de travail.

LayoutLMv3 est le sommet de la compréhension des documents basés sur OCR. Fort sur les formulaires et les factures. Requiert OCR en amont.

> LayoutLMv3 est le sommet de la compréhension des documents basés sur OCR.

### DocLLM (2023)

DocLLM (Wang et al., arXiv:2401.00908) est le frère génératif de LayoutLM. Génère des réponses de forme libre conditionnées sur des jetons de mise en page.

> DocLLM est le génération de LayoutLM.

### Époque 3  VLM-native (2024+)

2024 VLMs sont devenus assez bons pour remplacer le pipeline entièrement.

> En 2024, le VLM est devenu assez bon, il peut remplacer complètement le tuyau.

- LLaVA-NeXT 336-tile AnyRes fonctionne pour les petits documents.
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la
- Qwen2.5VL à résolution dynamique gère 2048+ pixels nativement.
  Le code de la société est le code de la société.
- Claude Opus 4.7 prend en charge les documents de 2576px.
  Le texte de la première partie de la série est le texte de la première partie de la série.
- PaliGemma 2 (avril 2025) est une formation spécifique pour les documents + écriture à la main.
  Le programme de formation de la langue française est basé sur la langue française.

Le fossé entre le VLM-native et le pipeline OCR s'est rapidement fermé.

> La différence entre les tuyaux VLM Orig生 et OCR s'est rapidement réduite.

- Textes de scène (écrit à la main + imprimé, scripts mixtes).
  Le texte est écrit en français.
- Tableaux complexes avec cellules fusionnées.
  Le texte est en français.
- Des équations mathématiques intégrées dans le texte.
  Le mot grec traduit par "réfléchisse" est traduit par "réfléchisse".
- Figures avec annotations de texte.
  Le texte de la lettre de la première lettre est écrit en français.

Les pipelines OCR gagnent encore sur:

> Le pipeline OCR est encore en vigueur dans les aspects suivants:

- Des charges de travail à grande échelle où la latence par page compte.
  La tâche de nettoyage à grande échelle est très importante.
- La fiabilité des pipelines (failles déterministiques par rapport aux hallucinations de VLM).
  Le système de contrôle de la sécurité est un système de contrôle de la sécurité.
- Environnements réglementés nécessitant une sortie de RCR auditable.
  En anglais, la production de produits de base est une activité de production de produits de base.

### La frontière Claude 4.7 / GPT-5

À 2576 pixels, les VLM frontaliers documentent la compréhension à une précision presque humaine.

> En 2576 像素原生输入下, VLM à l'avant-garde pour approcher le taux de précision de l'homme faire une compréhension documentée.

- DocVQA: Claude 4.7 ~95.1, PaliGemma 2 ~88.4, Nougat ~77.3, en tuyau LayoutLMv3 ~83.
  Le texte de la loi est le texte de la loi de l'Église.
- Le tableau QQ: Claude 4.7 ~ 92,2 GPT-4V ~ 78.
  Le texte de la lettre de Claude IV est écrit en français.
- Le MRC visuel: Claude 4.7 ~ 94.
  Le film est aussi connu sous le nom de "MRC".

Les modèles fermés sont principalement de résolution et de base à l'échelle LLM. Les modèles ouverts à 7B sont quelques points en retard mais se rattrapent.

> La différence entre les modèles de source fermée et les modèles de base de LLM est principalement de résolution.

### Équations mathématiques et sortie LaTeX

Les documents scientifiques ont besoin d'une sortie exacte de LaTeX pour les équations. Nougat a été formé à ce sujet. Les VLM formés avec des cibles LaTeX (Qwen2.5-VL-Math, dérivés Nougat) produisent un LaTeX utilisable. Sans formation explicite LaTeX, les VLM produisent des transcriptions lisibles mais imprécises.

> Il est nécessaire de définir la méthode de formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de

Pour les pipelines de papier scientifique en 2026: chaîne Nougat sur le PDF, puis un VLM sur des pages délicates.

> 2026 年科学论文管道建议:先用 Nougat 处理 PDF,再用 VLM 处理棘手页面──

### Écriture manuscrite

La plus difficile est encore la sous-tâche. La composition imprimée + manuscrite (notes médicales, formulaires remplis) est le point où les pipelines OCR battent encore les VLM en termes de coûts.

> 仍然是最难的子任务──印刷+手写混合(医生笔记、填写的表单) 仍然是 OCR 管道在成本上仍然胜胜了VLM的场景──纯手写VLM 正在改进(Claude 4.7、PaliGemma 2)──

### Récipitée 2026

Pour un nouveau projet d'IA-document:

>  Pour les nouveaux projets d'IA:

- Les factures imprimées à l'échelle pure: LayoutLMv3 + règles, rentables.
  Le modèle de l'écriture est le modèle de l'écriture de l'écriture.
- Documents mixtes (scientifiques + manuscrits + formulaires): VLM natifs (PaliGemma 2 ou Qwen2.5-VL).
  Le texte de la première partie est le texte de la première partie.
- L'ingestion complète de l'arXiv: Nougat pour les mathématiques, VLM pour les chiffres.
  Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la
- Régulateur: pipeline OCR + validateur VLM pour vérification croisée.
  Le projet de loi de la Commission européenne sur les droits de l'homme (CEP) est en cours de mise en œuvre.

## Utilisez-le avec le cadre de réalisation
```figure
mm-doc-layout
```

## Utilisez-le

`code/main.py`- Le numéro de la liste:

- Un jetoniseur de jouets conscient de la mise en page: donné (texte, bbox) paires, produit l'entrée de style LayoutLMv3.
  Le jeu est un jeu de mots qui se joue à la mode.
- Générateur de schéma de tâche de style Donut: modèle JSON pour les formulaires.
  Le schéma de tâche de Donut 风格的任务方案 生成器:表单的 JSON 模板。
- Une comparaison des budgets de jetons par page sur OCR-pipeline, Donut, Nougat et VLM-native.
  Le code de la vie civile est un code de vie qui est utilisé pour la vie civile.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-document-ai-stack-picker.md`. En raison d'un projet d'IA document (domaine, échelle, qualité, réglementation), choisissez entre pipeline OCR, spécialiste libre de OCR et VLM-native.

> 本课产 出 `outputs/skill-document-ai-stack-picker.md` la gestion des projets d'IA dans le domaine de la dimension, de la qualité et de la surveillance), dans les pipelines OCR, sans spécialistes OCR et VLM.

## Les exercices

1. Votre projet est de 10 millions de factures par jour. Quelle pile minimise le coût par page sans perdre de précision?

2. Pourquoi LayoutLMv3 surpasse les CLIP-VLM pur sur le formulaire QA mais ne fonctionne pas bien sur le texte scénario ?

3. Nougat génère LaTeX. Proposez un cas de test où la sortie native VLM bat Nougat sur la fidélité LaTeX, et un cas où Nougat gagne. Nougat 生成 LaTeX.

4. Lire le document PaliGemma 2 (Google, 2024). Quelle est la principale addition de données de formation qui a augmenté la précision du document par rapport à PaliGemma 1 ?

5. Conception d'un hybride réglementaire sûr: OCR pipeline comme primaire, VLM comme secondaire cross-check. Comment résoudre le désaccord?

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| OCR pipeline | "Tesseract-style" OCR 管道 | Stage-wise stack: detect -> OCR -> layout -> rules; deterministic, fragile 分阶段栈：检测→OCR→布局→规则；确定但脆弱 | |
| OCR-free | "Donut-style" 无 OCR | Image-to-output transformer that skips explicit OCR; single model 图像到输出的 Transformer，跳过显式 OCR；单一模型 | |
| Layout-aware | "LayoutLM" 布局感知 | Input includes per-token bbox coordinates; unified masking across modalities 输入包含逐 token 的 bbox 坐标；跨模态统一掩码 | |
| VLM-native | "Frontier VLM" VLM 原生 | Feed page image directly to Claude/GPT/Qwen VLM at high resolution; no pipeline 直接将页面图像输入高分辨率 VLM；无需管道 | |
| DocVQA | "Doc benchmark" 文档 VQA 基准 | Document VQA standard; most-cited score 文档 VQA 标准评测；被引用最多的评分 | |
| Markup output | "LaTeX / MD" 标记输出 | Structured output format instead of free-form text; enables downstream automation 结构化输出格式而非自由文本；支撑下游自动化 | |

## Encore une lecture

- [Li et al. — TrOCR (arXiv:2109.10282)](https://arxiv.org/abs/2109.10282)
- [Blecher et al. — Nougat (arXiv:2308.13418)](https://arxiv.org/abs/2308.13418)
- [Huang et al. — LayoutLMv3 (arXiv:2204.08387)](https://arxiv.org/abs/2204.08387)
- [Kim et al. — Donut (arXiv:2111.15664)](https://arxiv.org/abs/2111.15664)
- [Wang et al. — DocLLM (arXiv:2401.00908)](https://arxiv.org/abs/2401.00908)
