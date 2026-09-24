# Construire un transformateur à partir de zéro  La Capstone   毕业项目

> 13 leçons, un modèle, pas de raccourcis.

> **【中文解读】**整合所有知识, de zéro à réaliser la GPT 架构完整――这是本阶段的核心实践理解这个,你就能读懂任何变压器的代码──

**Type:** Hands-on | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 01 through 13. Don't skip. | **前置知识:** Phase 7 · 01 through 13. Don't skip.
**Time:** ~120 minutes | **时间:** ~120 分钟

## Le problème , l' introduction du problème

Vous avez lu tous les articles, vous avez mis en place des points d'attention, des divisions de plusieurs têtes, des codes positionnels, des blocs d'encodeur et de décodeur, des pertes de BERT et de GPT, des MoE, du cache KV.

> Vous avez déjà lu chaque article. Vous avez réalisé l'attention, la division, le codeur de position, le codeur et le codeur de bloc, le BERT et le GPT.

Le point culminant: entraîner un petit transformateur de décodeur uniquement de bout en bout sur une tâche de modélisation du langage au niveau des personnages. Il lit Shakespeare. Il génère un nouveau Shakespeare. Il est assez petit pour s'entraîner sur un ordinateur portable en moins de 10 minutes. Il est assez correct que l'échange d'un ensemble de données plus grand et une formation plus longue vous donne un véritable LM.

> 毕业项目: On peut apprendre à apprendre à lire Shakespeare, à créer un nouveau Shakespeare, à apprendre à lire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire Shakespeare, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire, à écrire.

Le tutoriel de Karpathy pour 2023 est la mise en œuvre de référence que chaque élève écrit au moins une fois. Nous le levons et le réorganisons autour de ce que nous avons couvert.

> C'est le "nanoGPT" du cours. Il n'est pas original. Le programme de nanoGPT de Karpathie 2023 est une réalisation de référence que chaque élève écrit au moins une fois.

> **【中文解读】**Ce programme de formation complète les 13 sections du programme: intégration de tous les connaissances: langage de type et de type, des symboles, des emplacements, des codes de position, des normes RMS, des facteurs, des facteurs, des connexions, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités, des capacités et des capacités.

> **【拓展：从 nanoGPT 到生产级 LLM】**Le nanoGPT de Karpathy est le meilleur point de départ pour apprendre Transformer. La différence clé entre nanoGPT et production de niveau LLM est: la taille des données (de MB à TB)  l'infrastructure de formation (de GPU unique à plusieurs milliers de GPU)  l'entraînement distribué (data并行, modèle并行,流水线并行)  ainsi que l'entraînement ultérieur (SFT + RLHF)  mais la structure centrale est la même.

## Le concept de base.

![Transformer-from-scratch block diagram](../assets/capstone.svg)

L'architecture, annotée:

> 架构,带注释:

```
input tokens (B, N)
   │
   ▼
token embedding + positional embedding  ◀── Lesson 04 (RoPE option)
   │
   ▼
┌──── block × L ────────────────────┐
│  RMSNorm                          │  ◀── Lesson 05
│  MultiHeadAttention (causal)      │  ◀── Lesson 03 + 07 (causal mask)
│  residual                         │
│  RMSNorm                          │
│  SwiGLU FFN                       │  ◀── Lesson 05
│  residual                         │
└────────────────────────────────── ┘
   │
   ▼
final RMSNorm
   │
   ▼
lm_head (tied to token embedding)
   │
   ▼
logits (B, N, V)
   │
   ▼
shift-by-one cross-entropy            ◀── Lesson 07
```

### Ce que nous expédions

> Nous livrons le contenu:

- `GPTConfig` un seul endroit pour configurer tous les hyperparametres.
  Le mot grec traduit par " le mot grec "`GPTConfig` Un lieu de configuration de tous les superparametres 
- `MultiHeadAttention` cause, en lots, avec une voie optionnelle de style Flash (PyTorch's `scaled_dot_product_attention`)
  Le mot grec traduit par " le mot grec "`MultiHeadAttention` 因果的、批量,可选闪光 风格路径  PyTorch 的 `scaled_dot_product_attention`)。
- `SwiGLUFFN` FFN moderne.
  Le mot grec traduit par " le mot grec "`SwiGLUFFN` 现代 FFN。
- `Block` pré-norme, attention enveloppée résiduelle + FFN.
  Le mot grec traduit par " le mot grec "`Block` Pré-régulier, attention des restes + FFN。
- `GPT` intégrations, blocs empilés, tête LM, générer().
  Le mot grec traduit par " le mot grec "`GPT`Il est aussi possible de créer des fichiers de données.
- Boucle d'entraînement avec AdamW, cosine LR, coupage de gradient.
  Avec AdamW, le rythme d'apprentissage est réduit à un rythme de formation.
- Un jeton de niveau Char sur le texte de Shakespeare.
  Le texte de Shakespeare est en français.

> **【中文解读】**完整的GPT 实现包含:配置类型、多头因果注意力(可选 Flash Attention)、SwiGLU FFN、前归归一化残差块、完整的GPT 模型类型(嵌入 + 堆叠块 + LM 头 + 生成函数)、AdamW + 余弦学习率训练循环──为了简洁, utilisé une position de learning嵌入式(而不是 RoPE) 且未实现 KV 缓存, mais l'exercice exige que vous ajoutiez ces éléments──

### Ce que nous ne livrons pas

> Nous ne livrons pas le contenu:

- RoPE  est mis en œuvre conceptuellement dans la leçon 04. Nous utilisons ici des embellissements positionnels appris pour la simplicité.
  En français, le RoPE est un concept de mise en œuvre.
- Le cache KV pendant la génération  chaque étape de génération recompte l'attention sur le préfixe complet. Plus lent mais plus simple.
  Traduction anglaise: KV de génération 缓存  Chaque étape de génération à l'avance complète 重新计算注意力──慢慢但更简单──练习要求你添加 KV 缓存──
- Attention Flash  PyTorch 2.0+ envois automatiques si les entrées correspondent; nous utilisons `F.scaled_dot_product_attention`- Je suis désolé .
  Le pyTorch 2.0+ est utilisé pour la mise en ligne de l'application.`F.scaled_dot_product_attention`Il y a une autre.
- Vous avez vu le MoE dans la leçon 11.
  Vous êtes dans la classe 11 课见过 MoE。

### Mesures cibles

Sur un ordinateur portable Mac M2, un four-couche, quatre têtes, d_model=128 GPT entraîné pour 2000 pas sur `tinyshakespeare.txt`- Le numéro de la liste:

> Dans le Mac M2 笔记本上,4 层、4 头、d_model=128 de GPT `tinyshakespeare.txt`上训练 2000 步:

- La perte d'entraînement converge de ~4,2 (random) à ~1,5 en environ 6 minutes.
  Le train perd de 4,2 à 1,5 minutes.
- L'échantillon de production semble en forme de Shakespeare: des mots archaïques, des interruptions de lignes, des noms propres comme "ROMEO:" émergent.
  Le mot "roméo" est un mot qui ressemble à Shakespeare.
- La perte de valeur (détenue à 10% du texte final) suit de près la perte de formation; aucune surcoche à cette taille/budget.
  L'équipe de formation de la formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de formation de

> **【拓展：从字符级到子词级 Tokenizer】**Le projet utilise un jeton de classe de caractères (BPE) mais est peu efficace. Le projet utilise un jeton de classe de caractères (BPE) ou un jeton de classe de caractères (SentencePiece etc.).

## Construisez-le et mettez-le en œuvre.
```figure
n5-block-stack
```

## Faites-le

Cette leçon utilise PyTorch.`torch`(La construction du processeur est bonne).`code/main.py`Le scénario est:

> 本课使用 PyTorch。安装 `torch`(CPU 版本即可)`code/main.py`❖ Le scénario de traitement:

- Téléchargement `tinyshakespeare.txt`si elle manque (ou si elle lit une copie locale).
  Le mot " défaut " est traduit par " défaut "`tinyshakespeare.txt`(Ou lire le titre)
- Le jeton char au niveau octet.
  Le mot "souvent" est traduit par "souvent".
- Le train/val est divisé à 90/10.
  Le groupe de formation et de formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la
- Boucle d'entraînement avec bf16 autocast sur le matériel pris en charge.
  Le système de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de formation de l'équipe de formation de l'équipe de formation de l'équipe de formation de l'équipe de l'équipe de formation de l'équipe de l'équipe de formation de l'équipe de l'équipe de l'équipe de formation de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de l'équipe de soutien.
- L'échantillonnage après l'entraînement est terminé.
  Le train complet de la formation est terminé.

### Étape 1: données

```python
text = open("tinyshakespeare.txt").read()
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda xs: "".join(itos[x] for x in xs)
```

65 caractères uniques, un petit vocabulaire, une taille de 4 bytes, pas de BPE, pas de drame de tokenizer.

> 65 个唯一字符──微型词表──适配 4 字节 vocab_size──没有 BPE,没有分词器的麻烦──

### Étape 2: modèle

Regardez !`code/main.py`Le bloc est un manuel de cours de la leçon 05  pré-norme, RMSNorm, SwiGLU, MHA causal.

> 参见 `code/main.py`◊ Ce bloc est le cours de la 5ème classe de réalisation  pré-régulieration  RMSNorm  SwiGLU ∞

### Étape 3: boucle d'entraînement

Il y a un lot aléatoire de vitres de 256 longues, en avant, en entropie croisée, en arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en marche arrière, en arrière, en arrière, en arrière, en arrière, en arrière, en arrière, en arrière, en arrière, en arrière, en arrière, en arrière, en arrière, en arrière, en arrière.

> 获取随机批量长度为 256 标签窗口──前向传播──偏移一位的交叉──反向传播──AdamW 步进──记录──重复──

```python
for step in range(max_steps):
    x, y = get_batch("train")
    logits = model(x)
    loss = F.cross_entropy(logits.view(-1, vocab_size), y.view(-1))
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    opt.zero_grad()
```

### Étape 4: échantillon

Si vous recevez une demande, faites-la à plusieurs reprises, prenez un échantillon des logits supérieurs, ajoutez-le et continuez. Arrêtez après 500 jetons.

> 给定一个提示,反复前向传播, de la première logite 采样,追加,继续──500 个标志 后停止──

### Étape 5: lire la sortie

Après 2 000 pas:

> 2 000 étapes:

```
ROMEO:
Away and mild will not thy friend, that thou shalt wit:
The chief that well shame and hath been his friends,
...
```

Pas Shakespeare, mais en forme de Shakespeare, une victoire claire pour 800 000 paramètres et 6 minutes sur un ordinateur portable.

> Ce n'est pas Shakespeare, mais comme Shakespeare, il y a 800 000 points sur le bloc-notes.

## Utilisez-le avec le cadre de réalisation

Cette pierre d'achèvement est une architecture de référence.

> Ce projet de formation est une structure de référence.

1. **Swap the tokenizer.**Utilisez le BPE (p. ex. `tiktoken.get_encoding("cl100k_base")`La taille du vocabulaire passe de 65 à 50 000 exemplaires.
   Le mot grec traduit par " le mot grec "**替换分词器。**Utilisation de la BPE`tiktoken.get_encoding("cl100k_base")`)──词表大小 de 65 跳到约50,000──模型容量需要相应扩展──
2. **Train on a bigger corpus.**Utilisation `OpenWebText`ou `fineweb-edu`Les jetons 10B sur un seul A100 prennent environ 24 heures pour un GPT de 125M param.
   Le mot grec traduit par " le mot grec "**在更大的语料上训练。**Utilisation `OpenWebText`Ou `fineweb-edu`(HuggingFace) ~~ dans un seul张 A100 上用10B token 训练 125M 参数 GPT 约需24小时──
3. **Add RoPE + KV cache + Flash Attention.**Les exercices ci-dessous vous guideront dans chacun d'eux.
   Le mot grec traduit par " le mot grec "**添加 RoPE + KV 缓存 + Flash Attention。**Les exercices suivants vous guideront à chaque étape.

Ce dernier se termine par un GPT de 125 M qui génère un anglais fluide. Pas un modèle frontalier. Mais le même chemin de code  juste plus grand  est ce que Karpathy, EleutherAI et l'Institut Allen utilisent pour former les points de contrôle de recherche en 2026.

> Il est possible de trouver un modèle de 125M GPT, mais le même code est utilisé par le Carpathy, EleutherAI et Allen Institute en 2026.

> **【拓展：Karpathy 的 nanoGPT 与教育意义】**Le nanoGPT d'Andrej Karpathy est l'un des enseignements les plus influents de l'enseignement de l'IA dans l'histoire de l'enseignement. Il prouve un GPT complet et entraînable qui peut être réalisé avec environ 300 pages PyTorch. Ce " procédé d'enseignement de la construction à zéro " vous permet de vraiment comprendre le rôle de chaque composant, plutôt que de le transformer en une boîte noire.

## Envoyez-le . Produit .

Regardez !`outputs/skill-transformer-review.md`. La compétence examine une mise en œuvre transformatrice à partir de zéro pour vérifier la précision des 13 leçons précédentes.

> 参见 `outputs/skill-transformer-review.md`◊ Cette compétence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

## Les exercices

1. **Easy.**On court .`code/main.py`Vérifiez que la perte de validation de votre modèle formé est inférieure à 2.0.`max_steps`La perte de val est-elle toujours en amélioration ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` L'évaluation de la perte de votre modèle de formation est inférieure à 2,0 `max_steps`La perte de certificat de 2000 à 5000 000 est-elle encore en train de s'améliorer ?
2. **Medium.**Remplacez les embellissements positionnels appris par RoPE.`MultiHeadAttention`La perte de valve est au moins aussi faible.
   Le texte est en français.`MultiHeadAttention`Le niveau de l'épreuve de la formation est au moins le même que celui de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation de la formation.
3. **Medium.**Implémenter un cache KV dans la boucle d'échantillonnage. Générer 500 jetons avec et sans cache. Le mur-horloge devrait s'améliorer de 520x sur un ordinateur portable.
   En chinois, la mise en œuvre de KV 缓存──有缓存和无缓存 产生 500 代币── notebook devrait avoir 5-20 fois l'amélioration du temps réel──
4. **Hard.**Ajoutez une deuxième tête au modèle qui prédit le prochain jeton plus un (MTP  Multi-Token Prediction de DeepSeek-V3).
   Le code de démarrage est un code de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage de démarrage.
5. **Hard.**Remplacez le FFN unique par bloc par un MoE de 4 experts. Routeur + routage top-2. Voir comment la perte de val change aux paramètres actifs correspondants.
   Le nombre de FFN de chaque bloc est remplacé par 4 专家 MoE──路由器 + top-2 路由── observer en correspondant à la valeur active 

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| nanoGPT | "Karpathy's tutorial repo" | Minimal decoder-only transformer training code, ~300 LOC; the canonical reference. |
| nanoGPT | "Karpathy 的教程仓库" | 最小解码器专用 Transformer 训练代码，约 300 行；经典参考。 |
| tinyshakespeare | "The standard toy corpus" | ~1.1 MB of text; every character-LM tutorial since 2015 uses it. |
| tinyshakespeare | "标准玩具语料库" | 约 1.1 MB 文本；自 2015 年以来每个字符级语言模型教程都用它。 |
| Tied embeddings | "Share input/output matrix" | LM head weight = transpose of token embedding matrix; saves parameters, improves quality. |
| 绑定嵌入 | "共享输入/输出矩阵" | LM 头权重 = token 嵌入矩阵的转置；节省参数，提高质量。 |
| bf16 autocast | "Training precision trick" | Run forward/back in bf16, keep optimizer state in fp32; standard since 2021. |
| bf16 自动混合精度 | "训练精度技巧" | 前向/反向用 bf16，优化器状态用 fp32；2021 年以来的标准。 |
| Gradient clipping | "Stops spikes" | Cap global grad norm at 1.0; prevents training blowups. |
| 梯度裁剪 | "阻止尖峰" | 将全局梯度范数限制在 1.0；防止训练爆炸。 |
| Cosine LR schedule | "The 2020+ default" | LR ramps up linearly (warmup) then decays cosine-shaped to 10% of peak. |
| 余弦学习率调度 | "2020+ 默认" | 学习率线性升温（warmup）然后余弦衰减到峰值的 10%。 |
| MFU | "Model FLOP Utilization" | Achieved FLOPs / theoretical peak; 40% dense, 30% MoE is strong in 2026. |
| MFU | "模型 FLOP 利用率" | 实际 FLOPs / 理论峰值；2026 年稠密 40%、MoE 30% 是好的。 |
| Val loss | "Held-out loss" | Cross-entropy on data the model never saw; overfit detector. |
| 验证损失 | "留出损失" | 模型从未见过的数据上的交叉熵；过拟合检测器。 |

## Encore une lecture

- [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/) la mise en œuvre classique annotée.
  Le texte de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la traduction de la langue de la langue de la langue de l'anglais.
