# BERT  Modélisation du langage masqué  BERT  掩码语言模型

> GPT prédit le mot suivant. BERT prédit un mot manquant. Une phrase de différence  et une demi-décennie de tout en forme d'embedding.

> **【中文解读】**BERT est un transformateur encodé uniquement, avec un entraînement de prédiction de cache.

**Type:** Hands-on | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

En 2018, chaque tâche de PNL  sentiment, NER, QA, entailment  a entraîné son propre modèle à partir de zéro sur ses propres données étiquetées. Il n'y avait pas de point de contrôle "comprendre l'anglais" prétrainé que vous puissiez affiner. ELMo (2018) a montré que vous pouviez pré-entraîner les emblèmes contextuels avec un LSTM bidirectionnel; cela a aidé mais n'a pas généralisé.

> En 2018, chaque tâche de PNL  analyse émotionnelle、 nommage de corps identification、 questions 文本含都 besoin sur ses propres données de marquage de modèle de formation à zéro .

BERT (Devlin et coll. 2018) a demandé: et si nous prenions un encodeur transformateur, l'entraînons sur chaque phrase sur Internet, et le forçons à prédire les mots manquants du contexte des deux côtés?

> BERT(Devlin et d'autres, 2018) pose un problème clé: si avec Transformer 编码器, vous entraînez toutes les phrases sur Internet, vous l'obligez à utiliser les mots cachés sur les deux côtés, comment ?

Le résultat: en 18 mois, BERT et ses variantes (RoBERTa, ALBERT, ELECTRA) ont dominé tous les classements de PNL existants.

> Le résultat est: en 18 mois, BERT et ses variants (Robert, Albert, Electra) ont dominé tous les classements de la PNL.

En 2026, les modèles encodés uniquement sont toujours l'outil idéal pour la classification, la récupération et l'extraction structurée. Ils fonctionnent 510x plus rapidement par jeton que les décodeurs et leurs intégrations sont l'épine dorsale de chaque pile de récupération moderne. ModernBERT (décembre 2024) a poussé l'architecture vers le contexte 8K avec Flash Attention + RoPE + GeGLU.

> En 2026, le modèle spécial de codeur reste le choix exact de la classification, de la recherche et de la structuration. Leur vitesse de fonctionnement par jeton est de 5 à 10 fois plus rapide que celle du codeur.

> **【中文解读】**La révolution de BERT repose sur le modèle "pre-train+micro-modulation": à grande échelle sans marque sur le matériel de référence, il utilise un modèle de langage masqué (MLM) pré-train, puis réduit la quantité de paramètres sur une tâche spécifique.

## Le concept de base.

![Masked language modeling: pick tokens, mask them, predict originals](../assets/bert-mlm.svg)

### Le signal d'entraînement

Prenez une phrase:`the quick brown fox jumps over the lazy dog`- Je suis désolé .

> Je suis un homme.`the quick brown fox jumps over the lazy dog`Il y a une autre.

Masquer 15% des jetons au hasard:

> Le code de débit est de 15%

```
input:  the [MASK] brown fox jumps [MASK] the lazy dog
target: the quick brown fox jumps over the lazy dog
```

Exercez le modèle pour prédire les jetons originaux à des positions masquées.`[MASK]`à la position 1 peut utiliser `brown fox jumps`C'est ce que le GPT ne peut pas faire.

> 訓練模型在被掩藏位置预测原始代币──因为编码器是双向的,预测位置是1 的 `[MASK]`Peut être utilisé pour les positions 2 及后的`brown fox jumps`C'est exactement ce que le GPT ne fait pas.

### Les règles du masque BERT

Parmi les 15% des jetons sélectionnés pour la prédiction:

> Dans les 15% des jetons de prédiction:

- 80% sont remplacés par `[MASK]`- Je suis désolé .
  80% sont remplacés`[MASK]`Il y a une autre.
- 10% sont remplacés par un jeton aléatoire.
  Le taux de change est de 10% à 10% et est remplacé par le taux de change.
- 10% restent inchangés.
  Le taux de croissance est de 10% en moyenne.

Pourquoi pas toujours ?`[MASK]`Parce que ...`[MASK]`Le modèle est formé à s'attendre à ce que la`[MASK]`Les résultats obtenus par le système de calcul de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position de la position

> Pourquoi pas toujours ?`[MASK]`Pourquoi ?`[MASK]`Il n'y aura jamais de réflexion. Si le modèle d'entraînement est à 100% de sa position cachée, on s'attend à ce qu'il soit vu.`[MASK]`, provoque un décalage de distribution entre les entraînements préalables et les modèles.

> **【中文解读】**Les trois règles de BERT 掩码 (80% [MASK]、10% 随机替换、10% 保持不变) sont destinées à réduire la différence de distribution entre la préparation et la modification.

> **【拓展：BERT 在 RAG 系统中的角色】**Dans le système moderne RAG, BERT 变体 est toujours au cœur du processus de recherche. Les transformateurs de phrases sont en réalité utilisés pour la comparaison des modèles de BERT.

### Prédiction de la phrase suivante (NSP)  et pourquoi elle a été abandonnée

BERT original a également été formé sur NSP: donné deux phrases A et B, prédire si B suit A. RoBERTa (2019) l'a abolie et a montré que NSP a blessé, pas aidé.

> Le premier est le premier, qui est le premier, qui est le premier, qui est le premier, qui est le premier, qui est le premier, qui est le premier.

### Ce qui a changé en 2026: ModernBERT

Le papier ModernBERT 2024 a reconstruit le bloc avec des primitifs 2026:

> Le projet ModernBERT de 2024 a été reconstruit avec des composants modernes:

| Component | Original BERT (2018) | ModernBERT (2024) |
|-----------|----------------------|-------------------|
| 组件 | 原始 BERT (2018) | ModernBERT (2024) |
| Positional | Learned absolute | RoPE |
| 位置编码 | 学习式绝对位置 | RoPE |
| Activation | GELU | GeGLU |
| 激活函数 | GELU | GeGLU |
| Normalization | LayerNorm | Pre-norm RMSNorm |
| 归一化 | LayerNorm | 前归一化 RMSNorm |
| Attention | Full dense | Alternating local (128) + global |
| 注意力 | 全密集 | 交替局部 (128) + 全局 |
| Context length | 512 | 8192 |
| 上下文长度 | 512 | 8192 |
| Tokenizer | WordPiece | BPE |
| 分词器 | WordPiece | BPE |

Et contrairement à la pile 2018, il est natif Flash-Attention. L'inférence est 23x plus rapide à la longueur de séquence 8K que DeBERTa-v3 avec de meilleurs scores GLUE.

> Contrairement à la technologie de 2018, ModernBERT a été conçu pour prendre en charge l'attention flash.

### Cas d'utilisation qui choisissent encore un codeur en 2026

| Task | Why encoder beats decoder |
|------|---------------------------|
| 任务 | 为什么编码器优于解码器 |
| Retrieval / semantic search embeddings | Bidirectional context = better embedding quality per token |
| 检索/语义搜索嵌入 | 双向上下文 = 每个 token 更好的嵌入质量 |
| Classification (sentiment, intent, toxicity) | One forward pass; no generation overhead |
| 分类（情感、意图、毒性） | 一次前向传播；无生成开销 |
| NER / token labeling | Per-position output, natively bidirectional |
| NER/token 标注 | 逐位置输出，天然双向 |
| Zero-shot entailment (NLI) | Classifier head on top of encoder |
| 零样本蕴含 (NLI) | 编码器之上的分类器头 |
| Reranker for RAG | Cross-encoder scoring, 10x faster than LLM rerankers |
| RAG 重排序器 | 交叉编码器评分，比 LLM 重排序器快 10 倍 |

## Construisez-le et mettez-le en œuvre.
```figure
transformer-residual
```

## Faites-le

### Étape 1: masquer la logique

Regardez !`code/main.py`- La fonction`create_mlm_batch`Returne les identifiants d'entrée (avec des masques appliqués) et les étiquettes (uniquement dans les positions masquées, -100 ailleurs  PyTorch ignore la convention de l'indice).

> 参见 `code/main.py`◊ fonction `create_mlm_batch`accepter le code d'identification 列表、词表大小和掩码概率, retourner à l'entrée ID(已应用掩码) 和标签(仅在掩码位置有价值,其余为 -100PyTorch的忽略索引约定)

```python
def create_mlm_batch(tokens, vocab_size, mask_prob=0.15, rng=None):
    input_ids = list(tokens)
    labels = [-100] * len(tokens)
    for i, t in enumerate(tokens):
        if rng.random() < mask_prob:
            labels[i] = t
            r = rng.random()
            if r < 0.8:
                input_ids[i] = MASK_ID
            elif r < 0.9:
                input_ids[i] = rng.randrange(vocab_size)
            # else: keep original
    return input_ids, labels
```

### Étape 2: exécuter la prédiction de MLM sur un petit corpus

Prenez un codeur à 2 couches + un chef MLM sur un vocabulaire de 20 mots, 200 phrases.

> En 20 mots et 200 phrases, entraînement sur un éditeur de 2 niveaux + tête de MLM.

### Étape 3: comparer les types de masques

Montrez comment la règle des trois sens rend le modèle utilisable sans `[MASK]`- Prédire une phrase non masquée et une phrase masquée.

> 展示三路规则                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `[MASK]`Les deux devraient générer un distributeur de symboles raisonnable, car les modèles ont été vus dans l'entraînement.

### Étape 4: tête de réglage

Remplacez la tête de MLM par une tête de classification sur un ensemble de données de sentiment de jouets. Seuls les têtes sont chargées; l'encodeur est gelé. C'est le modèle que suit chaque application BERT.

> Utilisez le type de tête de remplacement de tête de MLM, entraînement sur un ensemble de données de jouets émotionnels.

> **【拓展：BERT 微调的实践技巧】**Les meilleures pratiques de BERT 微调 comprennent: 1) Utiliser un taux d'apprentissage plus faible(2e-5 à 5e-5) éviter de perturber le pouvoir de formation préalable; 2) Exploiter des tokens pour les tâches de catégorie par catégorie comme expression de phrase; 3) Exploiter des tokens pour chaque tâche de NER; 4) Défricher progressivement (defrigeration progressive)

## Utilisez-le avec le cadre de réalisation

```python
from transformers import AutoModel, AutoTokenizer

tok = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base")

text = "Attention is all you need."
inputs = tok(text, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, N, 768)
```

**Embedding models are fine-tuned BERT.** `sentence-transformers`modèles comme `all-MiniLM-L6-v2`Le codeur est le même, la perte a changé.

> **嵌入模型是微调后的 BERT。** `sentence-transformers`模型如 `all-MiniLM-L6-v2`La structure du codeur est la même que celle du BERT, mais la fonction de perte est modifiée.

**Cross-encoder rerankers are also fine-tuned BERT.**Classification par paires`[CLS] query [SEP] doc [SEP]`L'attention bidirectionnelle entre requête et document est exactement ce qui donne aux encoders croisés leur avantage de qualité par rapport aux biencoders.

> **交叉编码器重排序器也是微调后的 BERT。**Dans le`[CLS] query [SEP] doc [SEP]`La double attention entre les requêtes et les archives est la raison pour laquelle la qualité des éditeurs de croisement est supérieure à celle des éditeurs de croisement.

**When not to pick BERT in 2026.**Tout ce qui génère. L'encodeur n'a aucun moyen sensé de produire des jetons autoregressif.

> **2026 年何时不选 BERT。**任何生成式任务──编码器 ne possède aucun moyen raisonnable de réaliser un jeton de retour à soi 生成──此外, dans les scénarios suivants, les petits décodeurs (comme Phi-3-Mini、Qwen2-1.5B) peuvent obtenir une flexibilité suffisante avec moins de paramètres──

> **【拓展：ModernBERT 的现代化改进】**ModernBERT(2024) va mettre à niveau l'architecture BERT de 2018:RoPE 替代学习式位置编码、GeGLU 替代 GELU、前归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归

## Envoyez-le . Produit .

Regardez !`outputs/skill-bert-finetuner.md`. Les compétences sont un réglage fin du BERT (choix de colonne vertébrale, spécifications de tête, données, évaluation, arrêt) pour une nouvelle tâche de classification ou d'extraction.

> 参见 `outputs/skill-bert-finetuner.md` Cette compétence est nécessaire pour la mise en place de nouvelles classes ou projets de mise en œuvre de la BERT 微调方案 (régularisation des compétences en matière de formation et de formation) 

## Les exercices

1. **Easy.**On court .`code/main.py`Confirmer ~ 15% sont sélectionnés, et de ces ~ 80% deviennent `[MASK]`- Je suis désolé .
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`En effet, les résultats de la campagne ont été très positifs, et la répartition des échantillons a été approuvée.`[MASK]`Il y a une autre.
2. **Medium.**Mettre en œuvre le masquage de mots entiers: si un mot est symbolisé en sous-words, masquer tous les sous-words ensemble ou pas. Mesurer si cela améliore la précision de MLM sur un corpus de 500 phrases.
   Si un mot est divisé en plusieurs mots, soit tout est masqué, soit tout n'est pas masqué, mesure si le taux de MLM est augmenté en 500 phrases.
3. **Hard.**Exercer un petit BERT de 2 couches, d=64, sur 10 000 phrases d'un ensemble de données public.`[CLS]`Comparer avec une ligne de base uniquement décodeur à des paramètres correspondants
   Le mot " petit " est traduit par " petit ".`[CLS]`Quel est le meilleur symbole utilisé pour SST-2 ?

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| MLM | "Masked language modeling" | Training signal: randomly replace 15% of tokens with `[MASK]`, predict the originals. |
| MLM | "掩码语言建模" | 训练信号：随机将 15% 的 token 替换为 `[MASK]`，预测原始 token。 |
| Bidirectional | "Looks both ways" | Encoder attention has no causal mask — every position sees every other position. |
| 双向 | "看两边" | 编码器注意力没有因果掩码——每个位置都能看到其他所有位置。 |
| `[CLS]` | "The pooler token" | A special token prepended to every sequence; its final embedding is used as the sentence-level representation. |
| `[CLS]` | "池化 token" | 一个特殊 token，添加到每个序列开头；其最终嵌入用作句子级表示。 |
| `[SEP]` | "Segment separator" | Separates paired sequences (e.g. query/doc, sentence A/B). |
| `[SEP]` | "片段分隔符" | 分隔成对序列（如查询/文档、句子 A/B）。 |
| NSP | "Next sentence prediction" | BERT's second pretraining task; shown to be useless in RoBERTa, dropped after 2019. |
| NSP | "下一句预测" | BERT 的第二个预训练任务；RoBERTa 证明其无用，2019 年后弃用。 |
| Fine-tuning | "Adapt to a task" | Keep the encoder mostly frozen; train a small head on top for the downstream task. |
| 微调 | "适应任务" | 保持编码器基本冻结；在顶部训练一个小头用于下游任务。 |
| Cross-encoder | "A reranker" | A BERT that takes both query and doc as input, outputs a relevance score. |
| 交叉编码器 | "重排序器" | 同时接收查询和文档作为输入的 BERT，输出相关性分数。 |
| ModernBERT | "2024 refresh" | Encoder rebuilt with RoPE, RMSNorm, GeGLU, alternating local/global attention, 8K context. |
| ModernBERT | "2024 刷新版" | 用 RoPE、RMSNorm、GeGLU、交替局部/全局注意力重建的编码器，8K 上下文。 |

## Encore une lecture

- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805) papier original.
  Le texte original de la lettre de Bert est écrit en français.
- [Liu et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692) comment former correctement BERT; tue NSP.
  Comment faire pour apprendre à utiliser le BERT ?
- [Clark et al. (2020). ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators](https://arxiv.org/abs/2003.10555) la détection de jeton remplacé dépasse MLM à l'ordinateur correspondant.
  Le code de débit est utilisé pour les données de référence.
- [Warner et al. (2024). Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder](https://arxiv.org/abs/2412.13663) Le papier ModernBERT.
  Le texte de la première partie de la série est le suivant:
- [HuggingFace `modeling_bert.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/bert/modeling_bert.py) référence au codeur canonique.
  Le modèle de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de la société de
