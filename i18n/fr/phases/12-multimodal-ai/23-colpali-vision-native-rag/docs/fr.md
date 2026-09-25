# ColPali et le document natif de vision RAG

> Le RAG traditionnel analyse les PDF en texte, les divise en morceaux, les intègre en morceaux, les stocke en vecteurs. Chaque étape perd un signal: le OCR supprime les données du graphique, le déchiquetage rompt les lignes de table, les emblèmes de texte ignorent les chiffres. ColPali (Faysse et coll., juillet 2024) a posé la question la plus simple: pourquoi extraire du tout du texte ? Embed l'image de page directement via PaliGemma, utiliser l'interaction tardive de style ColBERT pour la récupération, et garder tous les lignes, les chiffres, les polices et le signal de formatage du document. Les critères de référence publiés: une précision de bout en bout de 20 à 40% supérieure à celle du texte-RAG sur les documents riches en visuels. ColQwen2, ColSmol et VisRAG ont étendu le schéma. Cette leçon lit la thèse de RAG et construit un minuscule index ColPali.

> **【中文解读】**Traditionnellement, les performances de RAG sur PDF sont mauvaises, car chaque étape est en train de perdre un signal: OCR  perdu graphique  fragmentation  destruction de la feuille de calcul  intégration de texte  ignoration de l'image  ColPali pose une question plus simple: pourquoi extraire du texte ? directement avec PaliGemma  intégration de l'image de page, avec le style ColBERT MaxSim  retard de communication pour effectuer la recherche, conserver la totalité de la mise en page    graphique  caractères et le format du document   signal     en vue de la richesse du texte  RAG  précision de 20 à 40% plus élevé que le texte 

> **【拓展：ColPali 在金融 RAG 中的应用】**Le rapport financier est le plus typique du rapport financier. Le chiffre d'affaires de Q3 augmente généralement dans les graphiques, les blocs de signatures de contrats sont des faits de mise en page et non des faits de texte. ColPali intègre directement l'image de page, conserve un signal visuel complet, très adapté au rapport financier, aux contrats, aux émissions, etc. C'est le cas de la vente de stock qui représente environ 5 à 10 fois la valeur du texte RAG, mais une augmentation du taux de précision est généralement le coût.

**Type:** Build
**Languages:** Python (stdlib, multi-vector indexer + MaxSim scorer)
**Prerequisites:** Phase 11 (LLM Engineering — RAG basics), Phase 12 · 05 (LLaVA)
**Time:** ~180 minutes

>  **【前置】**Il est également possible de faire une analyse de la situation de l'image de l'image de l'image.
>  **【类比】**传统 RAG vs ColPali = "看书先扫描成纯文本" vs "直接看图找答案"──传统 = OCR 提取文字→分块→embedding(图表数据全部丢失);ColPali = 直接对页面图像做补丁嵌入(图表、表格、布局全保留)── Dans les documents de "图表为王" tels que les rapports financiers, ColPali 准确率高 20-40%──

## Objectifs d'apprentissage

- Expliquez la différence entre la récupération de deux encoders (un vecteur par document) et la récupération d'interaction tardive (plusieurs vecteurs par document).
  Traduction anglaise: expliquer les différences entre les deux types de codeurs (un seul et même émetteur) et le différent entre les deux types de codeurs (un seul et même émetteur)
- Décrivez l'opération MaxSim de ColBERT et comment ColPali la généralise des jetons de texte aux correctifs d'image.
  Le code de Colbert est un code de code de code de type "CollPali" qui est utilisé pour la mise en page de la page d'accueil.
- Construisez un petit index ColPali: page → patch embeddings → MaxSim sur les emblèmes de requête → top-k pages.
  Le code de la page est le code de la page.
- Comparez le générateur ColPali + Qwen2.5 VL versus le générateur texte-RAG + GPT-4 sur un cas d'utilisation des factures / rapports financiers.
  Le rapport financier est utilisé pour comparer ColPali + Qwen2.5-VL 生成器 vs 文本 RAG + GPT-4。

## Le problème , l' introduction du problème

Le texte-RAG sur les PDF jette la plupart du document. La croissance des revenus du troisième trimestre d'un rapport financier est généralement dans un graphique; les résultats d'un rapport médical sont dans des images annotées; le bloc de signature d'un contrat juridique est un fait de mise en page, pas un fait de texte.

> Le texte du rapport RAG a abandonné la plupart des informations du document. La croissance des revenus du troisième trimestre du rapport financier est généralement dans les graphiques. Les résultats du rapport médical sont marqués sur les images.

Le pipeline texte-RAG:

> 文本 RAG 管道:

1. PDF → texte via OCR / pdftotext.
   Le texte est à la base de l'article suivant:
2. Le texte → 300 à 500 pièces de jetons.
   Le code de la carte est de 300 à 500 blocs.
3. Chunk → intégration de bi-encodeur (un vecteur).
   Le code de la carte est un code de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de
4. Recherche utilisateur → intégration → similitude cosine → top-k morceaux.
   Le nombre de personnes qui ont été interrogées est de 7 à 7 ans.
5. Les élèves + les étudiants → LLM.
   Le texte de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la lettre de la

Cinq étapes perdantes, des graphiques non capturés, des tables brisées en morceaux, des tableaux à colonne multiplie, des annotations de figure disparaissent.

> 五有损步骤──图表未捕获──图表被块截截切──多布局被展平──图表注释消失──

Correction de ColPali: sauter OCR, intégrer directement l'image de page. Utilisez l'interaction tardive de style ColBERT pour la récupération afin que le modèle puisse répondre aux correctifs à grains fins au moment de la requête.

> ColPali Modification: saute OCR, directement intégré dans l'image de page. Utilisez ColBERT 风格的延迟交互进行检查, de sorte que le modèle puisse être concentré sur le petit grain de patch lors de la requête.

## Le concept de base.

> **【中文解读】**ColPali utilise une méthode visuelle pure pour réaliser RAG: sans passer par OCR, directement intégrer la page du document en tant qu'image codée à la taille, en utilisant la recherche de similitude visuelle. L'innovation centrale de ColPali est que chaque jeton de la requête MaxSim est intégré à chaque patch de la page du document pour faire le plus grand équilibre de similitude, puis rechercher et..

> **【拓展：视觉原生 RAG 的优势**传统RAG管线(OCR -> 文本 -> 嵌入 -> 检索) 面复杂面面(表格、图表、公式) 上经常失败。ColPali 直接在视觉层次匹配,无需OCR,在包含图表和表格的文档检索上上比传统方法提升 30-50%──缺点是需要更多存储(每页一个向量)。


> **【拓展：ColPali 的效率分析】**ColPali a augmenté de 30 à 50% le taux de précision sur les archives contenant des graphiques et des formulaires. L'absence est que le coût de stockage des index est plus élevé.


### Le projet de loi

ColBERT (Khattab & Zaharia, arXiv:2004.12832) est une méthode de récupération de texte. Au lieu d'un vecteur par document, il produit un vecteur par jeton.

> Colbert est une méthode de recherche de texte.

- Les jetons de requête obtiennent leurs propres emplacements (vecteurs N_q).
  Le code de la carte est le code de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de la carte de
- Les jetons de document obtiennent des emblèmes (vecteurs N_d, généralement en cache).
  Le code de dépôt est un code de dépôt de données.
- Score = somme sur les jetons de requête de max sur les jetons de document de similitude cosine: Σ_i max_j cos(q_i, d_j).
  Le nombre de points de référence est le plus élevé de la taille de la ligne de référence.

C'est l'opération MaxSim. chaque jeton de requête "choisit" son jeton de document le mieux correspondant. Le score final est la somme.

> C'est le fonctionnement de MaxSim. Chaque jeton de requête "choisir" son jeton de document le mieux adapté.

Avantages: rappel fort, gère la sémantique au niveau des termes.

> 优势:强召回率,处理词级语义――劣势:每文档 N_d 个向量, stockage昂贵――

### ColPali

ColPali (Faysse et coll., arXiv:2407.01449) applique le modèle ColBERT aux images.

> ColPali va utiliser le modèle ColBERT pour les images.

- Chaque page est codée par PaliGemma (langue ViT+) en emblèmes de correctifs: vecteurs N_p par page.
  Le code de la page est en ligne.
- Chaque requête utilisateur (texte) est codée dans des emblèmes de jetons de requête: vecteurs N_q.
  Le code de référence est le code de référence de chaque utilisateur.
- Score = Σ_i max_j cos(q_i, p_j), c'est-à-dire MaxSim sur les jetons de texte de requête et les patchs d'image de page.
  Le code de la page est le code de la page.
- Récupérez les pages de premier ordre par score total.
  Suivant: Le mot de passe de la page

Au moment de l'ingestion du document: intégrer chaque page avec PaliGemma, stocker toutes les intégrations de correctifs. au moment de la requête: intégrer les jetons de requête, calculer MaxSim par rapport à toutes les intégrations de page stockées, retourner les pages top-k.

> 文档摄取时: Utilisez PaliGemma 嵌入每页, stockage tous les correctifs 嵌入──查询时:嵌入查询代币,对所有存储的页面嵌入计算MaxSim,返回顶-k 页面──

Les avantages: le texte de bout en bout dépasse le RAG de 20 à 40% sur les documents riches en visuel.

> 优势:端到端在视觉丰富文档上文 RAG élevé de 20 à 40%── par patch 向量捕获局部布局和内容──

Cons: N_p patches × 4 bytes flottant × D-dim vecteurs par page = stockage croît rapidement. Atténuée par la quantification PQ / OPQ.

> 劣势:N_p 个补丁 × 4 字节浮点 × D 维向量每页 = 储存快速增长──可通过 PQ/OPQ 量化缓解──

### ColQwen2 et ColSmol

ColQwen2 (illuin-tech, 2024-2025) échange PaliGemma contre Qwen2-VL. Meilleur encodeur de base, meilleure récupération.

> ColQwen2 va remplacer PaliGemma par Qwen2-VL.

ColSmol est la variante à plus petite échelle pour l'utilisation locale / bord. Un retriever ColSmol à ~ 1B paramètres fonctionne sur un GPU de consommation.

> ColSmol est un petit type de processeur de recherche qui fonctionne sur des GPU de niveau de consommation.

### VisRAG

VisRAG (Yu et al., arXiv:2410.10594) est une variante différente: au lieu de MaxSim sur les correctifs, regroupez chaque page en un seul vecteur avec un VLM puis récupérez le bi-encodeur.

> VisRAG est une variante différente: pas en patch, mais avec VLM, chaque page sera reconditionnée en un seul vecteur de re-double coder.

Le compromis qualité-coût: ColPali pour la qualité, VisRAG pour l'échelle.

> 质量与成本的权衡: ColPali 追求质量,VisRAG 追求规模──

### M3DocRAG

M3DocRAG (Cho et al., arXiv:2411.04952) étend la récupération multimodal au raisonnement multi-pages multi-document.

> M3DocRAG va étendre la recherche de plusieurs modèles à plusieurs pages de documents de recherche de plusieurs pages, pour VLM 组合多页上下文──

### ViDoRe  l'indice de référence

Évaluation visuelle de la récupération de documents. Les tâches comprennent les rapports financiers, les documents scientifiques, les documents administratifs, les dossiers médicaux, les manuels.

> Le projet de loi de la Commission européenne sur les droits de l'homme (CEDEAO) a été publié le 30 décembre.

ColPali-v1 donne ~80% de nDCG@5 sur ViDoRe; le texte-RAG sur les mêmes documents donne ~50 à 60% de résultats.

> ColPali-v1 en ViDoRe en haut d'environ 80% nDCG@5; texte RAG en haut de la même archives en haut d'environ 50-60%。

### Le pipeline RAG de bout en bout

Pour un RAG natif de vision:

> 视觉原生 RAG 管道:

1. Ingest: PDF → images de page → PaliGemma encoding → stockage de tous les emplacements de correctifs.
   Le code de la page est le code de la page.
2. Recherche: texte utilisateur → emblèmes de jetons de requête → MaxSim contre toutes les pages indexées → pages top-k.
   Encore une fois, le code de référence est utilisé pour les pages de référence.
3. Générer: images de la page top-k + requête → VLM (Qwen2.5-VL ou Claude) → réponse.
   Le nom de l'équipe de formation est le nom de la société de formation.

Aucun OCR, les chiffres, les graphiques, les polices, la mise en page vont tous dans la réponse.

> Tout le processus sans OCR.

### Mathématiques de stockage

Un rapport financier de 50 pages avec 729 correctifs par page et 128 dimensions intégrées:

> 50 pages rapport financier, page 729 par patch, 128 dimensions:

- ColPali: 50 * 729 * 128 * 4 octets = ~ 18 Mo brut, ~ 4 Mo après PQ.
  Le texte original est écrit en français.
- RAC texte: 50 morceaux * 768-dim * 4 octets = ~ 150 kB.
  Le texte de la première partie de la série est le texte de la première partie de la série.

ColPali est ~ 30 fois plus de stockage par document. À l'échelle, OPQ / PQ le réduit à ~ 5-10 fois, généralement tolérable.

> ColPali Chaque archives stockées à environ 30 fois.

### Quand le texte-RAG gagne toujours

- Document pur texte sans signal de mise en page (articles wiki, journaux de discussion).
  Le texte de la loi est plus simple et plus facile à stocker.
- Des archives de plusieurs millions de pages où le stockage domine le coût.
  Le coût de stockage est le principal.
- Exigences réglementaires strictes exigeant que le texte OCR extraitable soit ajouté à la récupération.
  La loi de l'État de l'Occident prévoit des exigences de surveillance et de contrôle des opérations de dépôt de fonds.

Pour tout le reste en 2026  rapports financiers, documents scientifiques, contrats juridiques, dossiers médicaux, documentation UX  vision-native RAG gagne.

> Les résultats de la recherche de l'équipe de recherche de l'UE pour la première fois ont été publiés en décembre 2026.

## Utilisez-le avec le cadre de réalisation
```figure
mm-maxsim
```

## Utilisez-le

`code/main.py`- Le numéro de la liste:

- Encodeur de patch de jouet: il cartographiera une "page" (petite grille de vecteurs de caractéristiques) à un ensemble d'embeddings de patch.
  Le jeu est un jeu de société de jeu.
- Scorer MaxSim: calcule le score de style ColBERT entre un ensemble d'intégration de jetons de requête et un ensemble de correctifs de page.
  Le code de référence est le code de référence de la page de Google.
- Il indique 5 pages de jouets, exécute 3 requêtes, renvoie le top-k avec des scores.
  En anglais, le nombre de joueurs est de 5 pages, le nombre de joueurs est de 3 pages, le nombre de joueurs est de 5 pages, le nombre de joueurs est de 3 pages, le nombre de joueurs est de 5 pages, le nombre de joueurs est de 5 pages, le nombre de joueurs est de 5 pages, le nombre de joueurs est de 5 pages, le nombre de joueurs est de 5 pages, le nombre de joueurs est de 5 pages, le nombre de joueurs est de 5 pages, le nombre de joueurs est de 5 pages, le nombre de joueurs est de 5 pages, le nombre de joueurs est de 3 pages, le nombre de joueurs est de 3 pages.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-vision-rag-designer.md`. Dans le cadre d'un projet document-RAG, choisissez ColPali / ColQwen2 / VisRAG / text-RAG et taillez le stockage.

> 本课产 出 `outputs/skill-vision-rag-designer.md` Donner des données à caractère personnel, choisir ColPali / ColQwen2 / VisRAG / 文本 RAG 并估算存储──

## Les exercices

1. Un rapport annuel de 200 pages à 729 patchs par page, 128-dim emb, 4 bytes flottant. Compute le stockage brut et le stockage comprimé PQ (8x). 200 pages années.

2. MaxSim est Σ_i max_j cos(q_i, p_j). Qu'est-ce que cette somme capture qu'une similitude moyenne simple ne le fait pas ? MaxSim est Σ_i max_j cos(q_i, p_j) ⋅

3. ColPali indice les pages comme des ensembles de correctifs. Quels changements si nous indiquons au niveau des mots (comme ColBERT le fait)?

4. Conception du pipeline de bout en bout pour un corpus de 1M de page avec un budget de latence de 500ms par requête. Choisissez ColQwen2 / VisRAG et justifiez.

5. Décrivez le modèle d'attention multi-pages et comment il diffère de la récupération ColPali d'une seule page.

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Late interaction | "ColBERT-style" 延迟交互 | Retrieval using per-token or per-patch embeddings + MaxSim, not a single doc vector 使用逐 token/patch 嵌入 + MaxSim 的检索，非单向量 | |
| MaxSim | "Max-over-patches" 最大相似度 | For each query token, pick the highest-similarity document token; sum across query 对每个查询 token 选最高相似度的文档 token；跨查询求和 | |
| Bi-encoder | "Single-vector" 双编码器 | One vector per document; faster but loses granularity 每文档一个向量；更快但丢失粒度 | |
| Multi-vector | "Many-vectors-per-doc" 多向量索引 | Store N_p vectors per document / page; storage cost grows but recall improves 每文档/页存储 N_p 个向量；存储增长但召回提升 | |
| Patch embedding | "Page feature" 图像块嵌入 | One vector per image patch from a VLM encoder, cached per page VLM 编码器输出的每 patch 一个向量，按页缓存 | |
| ViDoRe | "Vision doc bench" 视觉文档检索基准 | ColPali's benchmark suite for visual document retrieval ColPali 的视觉文档检索基准套件 | |
| PQ quantization | "Product quantization" 乘积量化 | Compression that maintains vector similarity while shrinking storage ~8x 保持向量相似度的同时压缩存储约 8 倍 | |

## Encore une lecture

- [Faysse et al. — ColPali (arXiv:2407.01449)](https://arxiv.org/abs/2407.01449)
- [Khattab & Zaharia — ColBERT (arXiv:2004.12832)](https://arxiv.org/abs/2004.12832)
- [Yu et al. — VisRAG (arXiv:2410.10594)](https://arxiv.org/abs/2410.10594)
- [Cho et al. — M3DocRAG (arXiv:2411.04952)](https://arxiv.org/abs/2411.04952)
- [illuin-tech/colpali GitHub](https://github.com/illuin-tech/colpali)
