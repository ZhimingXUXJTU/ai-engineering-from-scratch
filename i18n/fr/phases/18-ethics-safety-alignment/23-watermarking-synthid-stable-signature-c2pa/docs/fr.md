# Marquage d'eau  SynthID, signature stable, C2PA 稳定签名 水印 SynthID C2PA

> Trois technologies structurent la provenance du contenu généré par l'IA en 2026. SynthID (Google DeepMind)  image watermarking lancé en août 2023, texte + vidéo mai 2024 (Gemini + Veo), texte open-source octobre 2024 via Responsible GenAI Toolkit, détecteur multimédia unifié novembre 2025 aux côtés de Gemini 3 Pro. Le marquage d'eau de texte ajuste de manière imperceptible les probabilités de prélèvement des jetons suivants; les marquages d'eau d'image/vidéo survivent à la compression, à la coupe, aux filtres, aux changements de fréquence d'image. Signature stable (Fernandez et coll., ICCV 2023, arXiv:2303.15435)  fine-tune le décodeur de diffusion latent afin que chaque sortie contient un message fixe; images découpées (10% du contenu) générées détectées >90% au FPR<1e-6. Suivi " La signature stable est instable " (arXiv:2405.07145, mai 2024)  ajustement fin supprime la marque d'eau tout en préservant la qualité. C2PA  standard de métadonnées cryptographiquement signé et évident pour les manipulations (C2PA 2.2 Explanatory 2025). Le marquage d'eau et le C2PA sont complémentaires: les métadonnées peuvent être supprimées mais ont une provenance plus riche; les marquages d'eau persistent grâce au transcodage mais contiennent moins d'informations.

> **【中文解读】**Ce chapitre présente la technologie d'impression de l'IA  SynthID、C2PA 等 identifier l'IA  Produire du contenu  SynthID(Google DeepMind) ajuster le prochain jeton 采样概率 生成包含更多"绿色"令牌不可察知但可检测──Stable Signature 微调潜在扩散解码器使每个输出包含固定二进制消息──C2PA est une signature cryptée 改的元数据标准──

> **【拓展：水印 → Deepfake 检测】**L'impression est le chemin de la technologie centrale de l'analyse de fausses informations. L'impression de synthédité est un test transnational de synthédité.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, token-watermark embed + detect) | **语言:** Python（标准库，token 水印嵌入 + 检测）
**Prerequisites:** Phase 10 · 04 (sampling), Phase 01 · 09 (information theory) | **前置知识:** Phase 10 · 04 (采样), Phase 01 · 09 (信息论)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Pour les étudiants, il est nécessaire de préparer la phase 10 de la formation.
>  **【类比】**水印 = "AI 内容的隐形身份证"──SynthID(Google) = 调整下面的代码采样偏好"绿色"代码,不可察觉但可检测;Stable Signature = 微调解码器让每张图都含固定二进制消息(剪裁 10% 仍 >90% 检出);C2PA = 加密签名元数据──互补:元数据可剥但信息丰富;水抗印转码但信息少──
> ️ "Signature stable non stable"2024.5: micro调即可移除水印保质量──水印不是银弹──

## Objectifs d'apprentissage

- Décrivez le marquage à niveau de jeton (style SynthID-text) et le mécanisme par lequel il est détectable.
- Décrivez la signature stable et l'attaque de retrait de 2024 qui l'a brisée.
- Le rôle de l'A2C de l'État et pourquoi il complète l'eau marquée.
- Décrivez les principales limites: signal spécifique au modèle, robustesse sous paraphrase et attaques de préservation du sens (arXiv:2508.20228).

> 描述令牌级水印(SynthID-text 风格) et son mécanisme de contrôle──描述 Stable Signature 和 2024 annum破坏其移除攻击──说明 C2PA's role and why it interacts with water印──描述关键局限性:模型特定信号、释义下鲁棒性和意义保持攻击──

## Le problème .

En 2023-2024, les faux profonds et le contenu généré par l'IA entrent dans des contextes politiques et de consommation à grande échelle. Le marquage d'eau est le signal technique proposé de provenance: marquer les générations au moment de la création, les détecter plus tard.

> Les données de production sont des données de référence, mais elles sont disponibles avec les données de C2PA.

## Le concept.

> **【中文解读】**文本水印机(Kirchenbauer 等人 2023, by Google 产品化): chaque étape de déchiffrement va arriver à K 个令牌哈希产生词汇表的伪随机"绿色"和"红色"分区,向绿色logits 添加三角洲 偏置采样――生成包含比随机更多的绿色令牌――检测:重新哈希每个前,计数生成中的绿色令牌,计算 z 分数――水印文本 z > 0,人类文本 z ~ 0。

### Marquage d'eau du texte (style SynthID-text)

Le mécanisme Kirchenbauer et al. 2023, produit par Google:

1. À chaque étape de décoding, hash les jetons K précédents pour produire une partition pseudorandom du vocabulaire en ensembles "verts" et "rouges".
2. Prise d'échantillons de biais vers l'ensemble vert en ajoutant δ aux logits verts.
3. La génération contient plus de jetons verts que le hasard ne le produirait.

Détection: réinitialisez chaque préfixe, comptez les jetons verts de la génération, comptez un z-score. Le z-score est >0 pour le texte marqué par eau, ~0 pour le texte humain.

Propriétés:
- Inperceptible par les lecteurs (δ est assez petit pour que la perte de qualité soit mineure).
- Détectable avec accès à la fonction de partition du vocabulaire.
- Pas assez fort pour paraphraser  réécrire le texte détruit le signal.

SynthID-text est open-source en octobre 2024 via le Responsible GenAI Toolkit de Google.

> **【中文解读】**La signature stable (Fernandez et autres, ICCV 2023) permet à chaque génération d'images de contenir un contenu fixe.

### Signature stable (image)

Fernandez et coll. ICCV 2023. Télécharger le décodeur de diffusion latent afin que chaque image générée contient un message binaire fixe intégré à la représentation latente. La détection est décodée à partir du latent avec un décodeur neuronal.

> La signature stable 微调潜在扩散解码器 permet à chaque image générée de contenir des messages fixes de type secondaire.

Mai 2024 " La signature stable est instable " (arXiv:2405.07145): l'ajustement fin du décodeur supprime la marque d'eau tout en préservant la qualité de l'image.

> 2024 5 月 " La signature stable est instable " prouve que le micro-défecteur peut conserver la qualité de l'image tout en délectant l'image.

### Détecteur unifié SynthID (novembre 2025)

Avec Gemini 3 Pro: un détecteur multimédia qui lit les signaux SynthID à partir de texte, d'image, d'audio et de vidéo dans une API. Unifie la pile de provenance de Google.

> 伴随 Gemini 3 Pro: un détecteur de mode transversal, disponible dans le texte, les images, les émissions audio et vidéo pour lire SynthID 信号。 unifié par Google Source Technology──

> **【拓展：C2PA + 水印互补 → EU AI Act Article 50】**C2PA et eau imprimée: les données peuvent être extraites mais portent une chaîne de sources riches; l'eau imprimée par le transfert de code durable mais ne porte que peu de bits. Google les regroupe dans les recherches, les annonces et la "réflexion sur cette image".

### C2PA

Coalition pour la provenance et l'authenticité du contenu. Standard de métadonnées falsifiées signé cryptographiquement. C2PA 2.2 Expliquer (2025). Un manifeste C2PA enregistre les revendications de provenance (qui a créé, quand, quelles transformations) signées par la clé du créateur.

> C2PA est une signature cryptée, un standard de protection des données. C2PA est une déclaration de source de données, signée par le créateur.

Complémentaire à l'eau marquée:
- Les métadonnées peuvent être retirées; les marqueurs d'eau ne peuvent pas (facile).
- Les métadonnées sont riches (chaîne de provenance complète); les balises d'eau contiennent des bits.
- C2PA dépend de l'adoption de la plateforme; les marqueurs d'eau sont intégrés automatiquement.

> Avec l'impression en ligne: données déchiffrables mais riches en informations; l'impression en ligne par transfert de code durable mais ne portant que peu de bits.

Google intègre à la fois dans la recherche, les annonces et "A propos de cette image".

> Google a intégré les deux éléments dans la recherche, la publicité et la "sur cette image".

> **【拓展：水印局限性 → 模型特定信号问题】**关键局限性:SynthID 水印仅来自启用SynthID的模型──"无SynthID 信号"不等于真实性证明未启用SynthID的模型生成的任何内容都不会有水印──此外,arXiv:2508.20228(2025) a démontré le sens de maintenir l'attaque peut également détruire le texte et les diverses images d'impression d'eau──

### Limitations

- **Model-specific.**SynthID marque-eau générations de modèles synthID. Une génération d'un modèle sans SynthID n'est pas marquée par l'eau, donc "aucun signal SynthID" n'est pas une preuve d'authenticité.
- **Paraphrase.**Les marqueurs d'eau du texte ne survivent pas à la paraphrase conservant le sens.
- **Transformation attacks.**arXiv:2508.20228 (2025) montre des attaques de préservation du sens qui détruisent à la fois les marque-eau texte et de nombreuses marque-eau d'image.
- **Fine-tune removal.**Pour "Signature stable est instable", l'ajustement fin post-génération supprime les marque-eau intégrées.

### Loi sur l'IA de l'UE Article 50

Code de transparence pour l'étiquetage des contenus générés par l'IA (premier projet de décembre 2025, deuxième projet de mars 2026, prévu final juin 2026 selon le [European Commission status page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)Le code reste en préparation à compter d'avril 2026 et le calendrier est sujet à changement.

### Là où cela s'inscrit dans la phase 18

Les leçons 22-23 traitent de ce que le modèle émet (données privées, signal d'origine). La leçon 27 couvre la gouvernance des données de formation. La leçon 24 est le cadre réglementaire qui exige ces mesures techniques.

> Les leçons 22-23  concernant les modèles émis par les données privées  Source signal  Les leçons 27  couvrent la formation en gestion des données  Les leçons 24  Exiger le cadre de surveillance de ces mesures techniques 

## Utilisez-le.
```figure
an-watermark-greenlist
```

## Utilisez-le

`code/main.py`construit un code d'eau de texte de jouet. Les jetons sont des nombres entiers 0..N-1; les biais d'échantillonnage marqués d'eau vers le jeu vert défini par hash. Un détecteur calcule le score z du jeton vert. Vous pouvez observer la détection à 1000 générations de jetons, regarder la paraphrase détruire le signal et mesurer le taux de faux positifs sur le texte humain.

> `code/main.py`构建玩具文本水印──令牌是整数 0.N-1;水印采样偏向哈希定义的绿色集──检测器计算绿色令牌 z 分数──你可以观察1000 令牌生成的检测、释义破坏信号以及人类文本上的误报率──

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-provenance-audit.md`. En raison d'un déploiement de contenu avec une revendication de provenance, il contrôle: le mécanisme de marque d'eau (le cas échéant), la chaîne de signature C2PA (le cas échéant), la robustesse des controverses de chacun et la couverture par modalité.

> 本课产 出 `outputs/skill-provenance-audit.md` Déploiement, audit, déploiement de contenu de déclarations de source déterminée: mécanisme d'impression de l'eau, C2PA, chaîne de signature, contrepartie de la réaction et couverture par modèle.

## Les exercices

1. On court .`code/main.py`. Rapportez les z-scores pour la génération de 1000 jetons marqués par eau par rapport au texte écrit par l'homme.

2. Implémenter une attaque par paraphrase qui remplace 30% des jetons par des synonymes.

3. Lisez Kirchenbauer et coll. 2023 Section 6 sur la robustesse. Pourquoi les marque-eau texte échouent-ils sous la paraphrase mais les marque-eau image survivent-ils à la découpe?

4. Développer un déploiement qui utilise SynthID-text + C2PA métadonnées. Décrire la chaîne de provenance qu'un consommateur voit. Identifier un mode d'échec de chaque composant.

5. Le résultat 2024 "Signature stable est instable" montre que l'ajustement fin supprime le point d'eau de l'image.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| SynthID | "Google's watermark" | Cross-modal provenance signal; text, image, audio, video |
| Token watermark | "Kirchenbauer-style" | Biased-sampling text watermark detectable via green-token z-score |
| Stable Signature | "image watermark" | Fine-tuned-decoder watermark; ICCV 2023 |
| C2PA | "the metadata standard" | Cryptographically signed tamper-evident provenance metadata |
| Paraphrase robustness | "does rewording break it" | Text watermark property; currently limited |
| Fine-tune removal | "adversarial unwatermark" | Attack that removes image watermark via decoder fine-tuning |
| Cross-modal detector | "unified SynthID" | November 2025 unified API across modalities |

## Encore une lecture

- [Kirchenbauer et al. — A Watermark for Large Language Models (ICML 2023, arXiv:2301.10226)](https://arxiv.org/abs/2301.10226) le mécanisme de marque d'eau des jetons
- [Fernandez et al. — Stable Signature (ICCV 2023, arXiv:2303.15435)](https://arxiv.org/abs/2303.15435) papier d'image de marque d'eau
- ["Stable Signature is Unstable" (arXiv:2405.07145)](https://arxiv.org/abs/2405.07145) l'attaque de déménagement
- [Google DeepMind — SynthID](https://deepmind.google/models/synthid/) la marque d'eau trans-modale
- [C2PA 2.2 Explainer (2025)](https://c2pa.org/specifications/specifications/2.2/explainer/Explainer.html) Standard de métadonnées
