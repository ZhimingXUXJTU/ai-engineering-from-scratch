# MIO et Modèles multimodels en streaming de n'importe qui à n'importe qui

> GPT-4o envoie un produit que la plupart des modèles ouverts ne peuvent pas reproduire: un agent qui entend la voix, voit la vidéo et parle en temps réel. La réponse à l'écosystème ouvert à la fin de 2024 était MIO (Wang et coll., septembre 2024). MIO symbolise le texte, l'image, la parole et la musique, entraîne un transformateur causale sur les séquences interligées et génère toute modalité à toute modalité. AnyGPT (Zhan et coll., février 2024) était la preuve du concept; MIO est l'échelle-up; Unified-IO 2 (Allen AI, décembre 2023) est le cousin avec la vision + action de la terre. Cette leçon est le modèle de tout à tout  quatre tokenizers, un transformateur, décodeur convivial pour le streaming.

> **【中文解读】**GPT-4o  présente une forme de produit impressionnante: un agent capable de entendre, de voir, de répéter le langage en temps réel ⋅ un agent de répéter le langage en temps réel ⋅ un réseau open source jusqu'à la fin de l'année 2024 qui n'a que MIO pour ce programme réalisable ⋅ le concept central de MIO est de symboliser le texte, les images, les voix, la musique entièrement, en utilisant un token intégral, un transformateur de causes ⋅ un traitement unifié, pour réaliser la génération de modèles à modèles.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-modality token allocator + streaming decode loop) | **语言:** Python（标准库，四模态 token 分配器 + 流式解码循环）
**Prerequisites:** Phase 12 · 11 (Chameleon), Phase 6 (Speech and Audio) | **前置知识:** Phase 12 · 11（Chameleon），Phase 6（语音与音频）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**Je suis en train de faire une série de tests de détection de la langue de l'équipe de formation de la langue de l'équipe de formation de la langue de l'équipe de formation de la langue de l'équipe de formation de formation de la langue de l'équipe de formation de la langue de l'équipe de formation de formation de la langue de l'équipe de formation de la langue de l'équipe de formation de la langue de l'équipe de formation de formation de la langue de l'équipe de formation de formation de la langue de l'équipe de formation de formation de la langue de l'équipe de formation de formation de la langue de l'équipe de formation de formation de la langue de l'équipe de formation de formation de la langue de l'équipe de formation de formation de formation de la langue de langue de l'équipe de formation de formation de la langue de langue de langue de l'équipe de formation de formation de formation de la langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de langue de
>  **【类比】**MIO = "万能翻译耳机"──其他多模态系统 = 一堆翻译器接力(视觉翻译→文本→语音翻译→音频), chaque saut retard+ information loss;MIO = un cerveau simultanément écouter, regarder, dire, comme GPT-4o 那样端到端低延迟── le défi est que chaque modèle doit être un tokenizer, et les tokens ne peuvent pas se confondre──

## Objectifs d'apprentissage

- Conçuez un vocabulaire commun qui héberge des jetons de texte, d'image, de parole et de musique sans collision.
  Le code de la langue française est un code de la langue française.
- Comparer SEED-Tokenizer (images) et SpeechTokenizer résiduel-VQ (speech) sur les compromis de compression + reconstruction.
  Le nombre de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries.
- Expliquez le programme en quatre étapes qui construit une génération à l'autre.
  Expliquer la construction de la formation à la formation à la formation à la formation à la formation à quatre étapes.
- Nombre des trois recettes ouvertes à tout le monde et de leurs principales compromis: MIO, AnyGPT, Unified-IO 2.
  Le nombre de personnes qui ont été arrêtées dans le cadre de l'enquête est de 12 à 15 ans.

## Le problème , l' introduction du problème

Un modèle multimodal unifié est facile à revendiquer et difficile à construire à l'échelle. La plupart des systèmes "tout à tout" jusqu'en 2024 ont été pipelineés: modèle de vision → représentation de texte → modèle de parole → audio. Chaque saut perd de l'information, ajoute de la latence et complique la formation. La vidéo démo de GPT-4o a montré une alternative à un modèle unique avec une réponse ultérieure; systèmes ouverts suivis de mois.

> 统一多模态模型 facile à prétendre mais difficile à construire à grande échelle. Jusqu'en 2024, la plupart des systèmes "volontaires à volontaires" étaient en tubes:

> **【中文解读】**Le plus grand défi du système de modèles est de ne pas reutiliser les tuyaux de classe (vidéo) parce que chaque étape perd de l'information et augmente la retardation.

Les défis de l'ingénierie:

> 工程挑战:

- Les tokenizers doivent exister pour chaque modalité, compresser sans perte - suffisamment pour la reconstruction, et produire des jetons à des taux que le transformateur peut consommer.
  Chaque mode doit avoir un composant, une perte de compression suffisamment petite pour être reconstruite, et un taux de transformation à consommation.
- Un seul vocabulaire doit allouer de l'espace pour le texte (32k+), l'image (16k+), la parole (4k+), la musique (8k+).
  Le nombre de mots et de mots dans le texte est de 32 000 +.
- Les données de formation doivent couvrir chaque paire d'entrées et de sorties (textes→image, images→speech, speech→image, etc.) ou le modèle doit être composé.
  Le modèle doit être assemblé.
- L'inference doit diffuser des jetons de sortie assez rapidement pour une latence de conversation (<500ms temps à premier octet audio).
  Traduction anglaise: la mise en œuvre doit être effectuée à une vitesse suffisamment rapide pour satisfaire le retard de dialogue.

## Le concept de base.

> **【中文解读】**MIO 实现 arbitrary to arbitrary multi-mode flow flow processing: texttext、image、audio、video entre peut être arbitrary assemblage d'entrée et de sortie. Le cœur est un unified dispersed token 化 tous les modèles sont codés en token 序列, avec un transformateur 统一处理──

> **【拓展：全模态模型的趋势】**La tendance de l'année 2025 est de "vision+langue" vers "full mode":GPT-4o Origins supporting audio input output,Gemini  supporting video real time flow,Meta's Spirit LM 统一语音和文本。Le problème central du modèle full mode doit être résolu est la différence de densité d'information des différents modèles1 seconde vidéo environ 30 1, seconde audio environ 16K échantillons, besoin de haute efficacité comprimée。


### Quatre tokenizers pour quatre modalités

La pile de jetons de MIO:

> **【中文解读】**MIO pour quatre modèles différents avec un tokenizer spécial, les jetons sortis sont tous cartographiés dans le code standard BPE (en anglais seulement) [32,000 mots), images avec SEED-Tokenizer (en anglais seulement) [3000 mots), voix avec SpeechTokenizer (en anglais seulement) [80]

- Le texte: BPE standard, vocables ~32000.
  Le nombre de personnes concernées est de 32 000 à 32 000 en moyenne.
- Image: SEED-Tokenizer (2023)  VAE quantifié avec un codebook discret, 4096 entrées, 32x32 jetons par image.
  Le code de la série est le code de la série de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries de séries.
- Discours: SpeechTokenizer résiduel-VQ (2023)  encode la forme d'onde 16 kHz en 8 livres de code hiérarchiques; le premier niveau est le contenu grossier, les niveaux ultérieurs ajoutent la prosodie et l'identité du haut-parleur.
  Le code de 16 kHz est en 8 niveaux; le premier est un contenu grossier, le second est un ajout à la loi et un nom de personne.
- Musique: résiduel similaire-VQ (famille de la musique Gen / Encodec de Meta), 4 à 8 livres de code.
  Le groupe est composé de musiciens de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la musique de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de la langue de laquelle.

Chaque modalité produit des jetons entiers. Les jetons obtiennent des plages d'identification disjointes dans le vocabulaire partagé:

> Chaque mode génère un nombre total de jetons.

```
text:   0..31999
image:  32000..36095  (4096 image tokens)
speech: 36096..40191  (4096 speech base tokens, plus residual layers)
music:  40192..48383  (8192 music tokens)
sep:    48384..48390  (<image>, <speech>, <music>, </...>, etc.)
```

Total: ~ 48k vocabulaire. L'intégration d'entrée et la projection de sortie couvrent tout cela.

> 总计约 48k 词汇量──输入嵌入和输出投影覆盖全部词汇──

### Décode de diffusion

La génération de la parole utilise le VQ résiduel. Le transformateur prédit les jetons de parole de base (couche 0); un quantificateur résiduel décodé parallèle prédit les couches suivantes. Chaque jeton de couche 0 est d'environ 50 ms d'audio à 16 kHz.

> 语音生成使用残差 VQ──Transformer 预测基础层(第0层)语音代币;并行解码的残差量化器预测后续层──每个第0层代币 大约对应 16kHz 下的50ms 音频──

> **【中文解读】**Le processus de déchiffrement de la clé est de traiter: Transformer  prédiction de la couche de base de la voix, résidual de la couche de suivi de la couche de suivi de chaque couche de base de la couche de traitement de la voix.

Le schéma de diffusion:

> 流式模式:

1. L'utilisateur parle en microphone; le jeton audio en temps réel émet des jetons de parole tous les 50 ms.
   Le nombre de voix dans le langage chinois est de 50 m.
2. MIO consomme des jetons à leur arrivée (précomplissement immédiat + avance progressive).
   Le code de la carte est le code de la carte de crédit.
3. Les jetons de sortie sont diffusés comme générés; un décodeur de voix parallèle les convertit en échantillons audio avec une latence de ~50-150 ms.
   Le code de sortie est en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en mode sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sortie en sor
4. Temps à premier octet audio: ~300-500 ms dans le papier MIO, approchant ~250 ms de GPT-4o.
   Le temps de l'écriture est d'environ 300 à 500 ms, proche de 250 ms de GPT-4o.

Mini-Omni (arXiv:2408.16725), GLM-4-Voice (arXiv:2412.02612), et Moshi (arXiv:2410.00037) sont des conceptions de streaming de la parole-LLM complémentaires.

> Mini-Omni、GLM-4-Voice 和 Moshi est un projet de logiciel de programmation de langue en ligne complémentaire.

### Programme de formation en quatre étapes

Le programme de formation du MIO:

> Le programme de formation de MIO:

1. Étapes 1  alignement. Corps de paire de modalités à grande échelle: image texte, discours texte, musique texte. Chaque paire utilise son propre segment de vocabulaire de jeton.
   Le texte est un langage qui est écrit en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français ou en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français ou en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français ou
2. Étapes 2  interligés. Documents interligés multi-modalité (blogs avec images + vidéo, podcasts avec transcriptions, etc.).
   Le texte de la première partie est le texte de la première partie de la première partie.
3. Étapes 3  amélioré par la parole. Données audio supplémentaires pour améliorer la qualité de la parole sans perdre la capacité du texte.
   Le niveau de qualité du son est augmenté.
4. Étapes 4  SFT. L'écoute des instructions dans les différentes modalités: VQA, sous-titres, narration, dialogue de parole à parole.
   Le texte de la première partie est le texte de la première partie.

Le manque d'une étape dégrade les capacités spécifiques: sauter la phase 2 et le modèle perd le contexte de la modalité croisée; sauter la phase 3 et la parole est mauvaise.

> 跳过某一阶段会导致特定能力退化:跳过阶段 2 模型失去跨模态上下文;跳过阶段 3 语音质量差──

> **【中文解读】**Le programme de formation en quatre étapes du MIO est un programme de formation qui permet de construire progressivement: 1) un modèle pour un large format de texte, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un modèle pour un langage, un langage pour un langage, un langage, un langage pour un langage, un langage, un langage pour un langage, un langage, un langage, un langage, un langage, un langage, un langage, un langage, un langage, un langage, un langage, un langage, un langage, un langage, un langage, un langage, un langage, un langage, etc.

### Chaîne de pensée visuelle

MIO introduit la chaîne de pensée visuelle: le modèle émet des jetons d'image intermédiaires comme une étape de raisonnement.

> MIO introduit la chaîne de pensée visuelle: modèle dans le processus de pensée générer un symbole d'image intermédiaire.

1. Émissions `<image>`les jetons qui rendent la scène (à partir de l'image d'entrée ou d'un schéma).
   Le mot " exportation " est traduit par " exportation " .`<image>`Les symboles de la scène de la mort sont:
2. Il émet un texte analysant le dessin.
   Le texte est traduit en français par "L'écriture est une langue étrangère".
3. Il émet la réponse finale.
   Le texte de la lettre de la première lettre est écrit en français.

L'image intermédiaire rendue sert de scratchpad. Les repères améliorent les tâches de raisonnement spatial. L'idée reflète la chaîne de pensée pour le raisonnement du texte.

> L'image intermédiaire de la projection est chargée comme un tableau de bord.

> **【拓展：视觉思维链的应用前景】**Dans le domaine financier, cette technique peut être utilisée pour analyser des diagrammes complexes: la chaîne de pensée visuelle est une extension du domaine visuel.

### Les concurrents dans n'importe quel

- AnyGPT (arXiv:2402.12226): 4 modalités (texte, image, discours, musique), conception similaire.
  Le texte est en anglais, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français ou en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français ou en français, en français, en français, en français, en français, en français, en français, en français, en français ou en français, en français ou en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français ou en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français
- Unified-IO 2 (arXiv:2312.17172): ajoute des sorties d'action de vision, de profondeur, de normes. Plus de diversité de tâches, plus petite échelle.
  En anglais, le nombre de tâches est de plus en plus petit.
- NExT-GPT (arXiv:2309.05519): décodeurs de diffusion LLM + modalité spécifique. Pas une approche de modèle unique.
  Le modèle de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de formation de la région de la région.
- CoDi (arXiv:2305.11846): diffusion composable; tout à tout via latente partagée.
  Le code de la société est le code de la société.

MIO est le plus proche de pure-token à tout. AnyGPT est son ancêtre conceptuel.

> MIO est le plus proche de la pure marque de l'alternative à l'alternative.

### Budget de la latence

Pour un produit conversationnel, la latence de chaque composant compte:

> Pour les produits de dialogue, le retard de chaque composant est important:

- Mic à jetons audio: ~ 50 ms.
  Le signal de la fréquence: environ 50ms.
- Préchargement (tokens audio + historique): ~ 100 ms sur un modèle 8B.
  Le code de la vidéo est le code de la vidéo.
- Le premier jeton de sortie: ~50ms.
  Le premier jeton de sortie: environ 50ms.
- Décodeur de parole parallèle résiduel-VQ +: ~100-150 ms.
  Le nombre de voix dans le monde est de 100 à 150 ms.

Temps total de la première octet audio: ~ 300 ms minimum. GPT-4o revendique ~ 250 ms. Moshi revendique 160 ms. MIO / AnyGPT sont dans la plage de 400 à 600 ms par référence publique.

> Le temps total de l'essai est d'environ 300ms. Le temps total de l'essai est d'environ 250ms.

> **【中文解读】**Pour les produits de retard budget:麦克风→语音代币(~50ms)→ 预填充(~100ms)→ 首个输出代币(~50ms)→ 残差 VQ + 语音解码(~100-150ms)。总计TTFAB 约300ms 起──GPT-4o 约250ms,Moshi 仅160ms(单 GPU 上最快的开源方案)。

### Pourquoi tout le monde reste dur

Même en 2026, les modèles ouverts à n'importe qui suivront ceux fermés sur deux axes:

> Même en 2026, le modèle libre à libre est encore en retard sur le modèle fermé en deux dimensions:

- La qualité de la parole. Le jeton VQ résiduel est déficient; la parole de conversation sonne robotique par rapport aux voix de classe ElevenLabs.
  Le niveau de qualité du langage est de plus en plus élevé que celui des autres langages.
- Le raisonnement à travers les modalités: demander au modèle " chanter sur ce que vous voyez " échoue encore plus souvent que les tâches de vision pure.
  Le modèle " chantez ce que vous voyez " est encore plus souvent défaillant que la tâche de simple vision.

Ce sont des problèmes de recherche ouverts. Qwen3-Omni (leçon 12.20) est la tentative ouverte la plus avancée en 2025.

> Ces questions sont des questions de recherche ouvertes.

## Utilisez-le avec le cadre de réalisation
```figure
any-to-any-stream
```

## Utilisez-le

`code/main.py`- Le numéro de la liste:

> `code/main.py`- Le numéro de la liste:

- Définit l'allocation du vocabulaire à quatre modalités et l'imprime.
  Le mot grec traduit par "répartition" est traduit par "répartition".
- Route une liste d'entrées multimodal (texte, image, clipe audio, musique) via le routeur du tokenizer.
  Le texte est écrit en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français en français
- Simule le décode en streaming pour une réponse texte-à-speech avec le comptage de la latence.
  Le mot "translation" est traduit par "translation".
- Compute le temps attendu de la première octet audio donné de l'encodeur, de la pré-remplissage et des latences du décodeur.
  Selon le codeur, le codeur est rempli et le codeur est retardé.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-any-to-any-pipeline-auditor.md`. Compte tenu d'une spécification de produit de conversation (modalités d'entrée, modalités de sortie, cible de latence), il vérifie les choix de conception de la famille MIO et calcule le budget de latence.

> 本课产 出 `outputs/skill-any-to-any-pipeline-auditor.md`◊ donner des règles de production de produits, elle examine la sélection de conception et le budget de la série MIO ◊

## Les exercices

1. Votre produit accepte l'entrée de la parole et renvoie la sortie de la parole. Quelle est la cible budgétaire de latence de bout en bout?

2. Le discours Tokenizer résiduel-VQ utilise 8 livres de code. Proposez pourquoi le décoding parallèle des niveaux résiduels est nécessaire (versus séquentiel) et quelles économies de latence cela apporte.

3. Votre vocabulaire a 32k de texte + 4k d'image + 4k de discours. Ajoutez 8k de musique et ~10 séparateurs. Quel est le coût du paramètre d'intégration-matrice à dim 4096 caché?

4. La chaîne de pensée visuelle émet une image intermédiaire. Quels types de questions bénéficient? Quels types sont blessés par les jetons supplémentaires?

5. Lisez Moshi (arXiv:2410.00037). Décrivez sa technique de "monologue interne" et comparez-la à la chaîne de pensée visuelle de MIO.

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Any-to-any | "Multimodal in/out" 任意模态进出 | A single model that accepts and emits text, image, speech, and music in any direction 单一模型接受并以任意方向输出文本、图像、语音、音乐 | |
| Residual-VQ | "Speech tokenizer stack" 语音分词器栈 | Multi-codebook tokenization where each layer adds information; base layer is content, later layers are prosody 多码本分词，每层添加信息；基础层是内容，后续层是韵律 | |
| SEED-Tokenizer | "Image codes" 图像编码 | Discrete image tokenizer with 4096-entry codebook used by MIO 离散图像分词器，4096 码本 | |
| Chain-of-visual-thought | "Visual scratchpad" 视觉草稿板 | The model generates an intermediate image as a reasoning step before its final answer 模型在最终回答前生成中间图像作为推理步骤 | |
| Time-to-first-audio-byte | "TTFAB" 首音频字节延迟 | Latency from user voice to first audio output; <500ms for conversational feel 用户语音到首个音频输出的延迟；<500ms 才有对话感 | |
| Four-stage curriculum | "Training recipe" 训练配方 | Alignment -> interleaved -> speech-enhanced -> SFT, in that order 对齐→交错→语音增强→指令微调的四阶段训练流程 | |

## Encore une lecture

- [Wang et al. — MIO (arXiv:2409.17692)](https://arxiv.org/abs/2409.17692)
- [Zhan et al. — AnyGPT (arXiv:2402.12226)](https://arxiv.org/abs/2402.12226)
- [Lu et al. — Unified-IO 2 (arXiv:2312.17172)](https://arxiv.org/abs/2312.17172)
- [Wu et al. — NExT-GPT (arXiv:2309.05519)](https://arxiv.org/abs/2309.05519)
- [Tang et al. — CoDi (arXiv:2305.11846)](https://arxiv.org/abs/2305.11846)
