# CNN et RNN pour le texte

> Les convolutions apprennent n-grammes, les récurrents se souviennent, les deux sont remplacés par l'attention, les deux sont encore importants sur un matériel restreint.
> Le cycle de l'apprentissage n-gramme, le cycle responsable de la mémoire, est remplacé par le mécanisme de l'attention, mais il est toujours important sur les appareils limités.

> **【中文解读】**La réforme de la structure de l'équipement de transformation a été mise en œuvre par le gouvernement de la République de Chine.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 11 (PyTorch Intro), Phase 5 · 03 (Word Embeddings), Phase 4 · 02 (Convolutions from Scratch) | **前置知识:** Phase 3 · 11（PyTorch 入门），Phase 5 · 03（词嵌入），Phase 4 · 02（从零实现卷积）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

TF-IDF et Word2Vec ont produit des vecteurs plats qui ignorent l'ordre des mots.`dog bites man`de `man bites dog`L'ordre des mots porte parfois le signal.

> TF-IDF et Word2Vec  génèrent des volumes de volet 平向量                                                                                                                                                                                                                                                    `dog bites man`et `man bites dog`Il y a des signaux.

Deux familles d'architectes ont comblé ce vide avant l'arrivée des transformateurs.

> Avant la sortie du Transformer, les deux familles ont rempli ce vide.

**Convolutional nets for text (TextCNN).**Appliquer des convolutions 1D sur des séquences d'embedding de mots. Un filtre de largeur 3 est un détecteur de trigrammes apprenable: il couvre trois mots et donne un score. Ampiler différentes largeurs (2, 3, 4, 5) pour détecter des motifs à grande échelle. Max-pool à une représentation de taille fixe. Plat, parallèle, rapide.

> **文本卷积网络（TextCNN）。**Le détecteur de trois groupes de mots est un détecteur de trois groupes de mots: il traverse trois mots et en sort un nombre de composants. Il se compose de différentes dimensions. Il est utilisé pour détecter les modèles de plusieurs dimensions.

**Recurrent nets (RNN, LSTM, GRU).**Les jetons de traitement un à la fois, en maintenant un état caché qui transmet l'information. Sequentielle, porteuse de mémoire, longueur d'entrée flexible. Modélisation de séquence dominée de 2014 à 2017, puis l'attention est venue.

> **循环网络（RNN、LSTM、GRU）。**个个处理代币,维护向前传递信息的隐藏状态――顺序、有记忆、灵活输入长度―― de 2014 à 2017 la séquence principale a été construite, puis un mécanisme d'attention est apparu―

Cette leçon construit les deux, puis nomme l'échec qui a motivé l'attention.

> Ce cours construit les deux, puis souligne l'échec de la dérive de l'attention.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

**TextCNN**Les jetons sont intégrés.`k`La convolutions 1D glissent un filtre sur une suite `k`-grammes d'embeddings, produisant une carte de fonctionnalités. le maximum global de pooling sur cette carte choisit l'activation la plus forte.

> **TextCNN**(Kim, 2014) ⋅Token est intégré ⋅宽度为 `k`Le premier tome est en continu.`k`-gramme 嵌上滑波器,产生特征图――对该特征图做全局最大池化选择最强激活――从多个波器宽度最大池化输出拼接――送进分类器头――

Pourquoi cela fonctionne-t-il ? un filtre est un n-gramme apprenable. le max-pooling est position-invariant, donc " pas bon " déclenche la même fonction au début ou au milieu d'un examen. trois largeurs de filtre avec 100 filtres chacun vous donne 300 détecteurs de n-gramme apprises.

> Pourquoi efficace ?波器是可学习的 n-gram──最大池化是位置不变的,所以"not good"在评论开头或中间触发相同特征──三波器宽度各 100 波器给你300 个可学习的 n-gram──检测器──训练是并行的;没有顺序依赖──

**RNN.**À chaque étape .`t`, l' état caché `h_t = f(W * x_t + U * h_{t-1} + b)`Partager`W`- Je suis là .`U`- Je suis là .`b`L'état caché dans le temps.`T`est un résumé de l'ensemble du préfixe.`h_1 ... h_T`(maximum, moyen ou dernier).

> **RNN。**Dans chaque étape du temps`t`, état caché`h_t = f(W * x_t + U * h_{t-1} + b)`Il y a une autre.`W`- Je suis là.`U`- Je suis là.`b`跨时间共享──时间 `T`Le résumé de l'ensemble de la préface est le résumé de l'ensemble des sections.`h_1 ... h_T`La plus grande valeur moyenne ou dernière

Les RNN simples souffrent de dégradations qui disparaissent.**LSTM**Il ajoute des portes qui décident de ce qu'il faut oublier, de ce qu'il faut stocker et de ce qu'il faut sortir, stabilisant les gradients à travers de longues séquences.**GRU**simplifie le LSTM à deux portes; fonctionne de manière similaire avec moins de paramètres.

> Il y a un problème de disparition de la RNN.**LSTM**添加决定忘了什么,储存什么,输出什么,稳定长序列的梯度.**GRU**Simplifier LSTM en deux parties; les paramètres sont moins nombreux mais les résultats sont similaires.

**Bidirectional RNNs**chaque token voit à la fois le contexte gauche et droit. essentiel pour l'étiquetage des tâches.

> **双向 RNN**运行一个RNN向前、另一个向后,拼接隐藏状态──每个代币的表示看左右两侧的上下文──对标注任务必不可少──

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
rnn-unroll
```

## Faites-le

### Étape 1: TextCNN en pyTorch

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class TextCNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, n_classes, filter_widths=(2, 3, 4), n_filters=64, dropout=0.3):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.convs = nn.ModuleList([
            nn.Conv1d(embed_dim, n_filters, kernel_size=k)
            for k in filter_widths
        ])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(n_filters * len(filter_widths), n_classes)

    def forward(self, token_ids):
        x = self.embed(token_ids).transpose(1, 2)
        pooled = []
        for conv in self.convs:
            c = F.relu(conv(x))
            p = F.max_pool1d(c, c.size(2)).squeeze(2)
            pooled.append(p)
        h = torch.cat(pooled, dim=1)
        return self.fc(self.dropout(h))
```

Le `transpose(1, 2)`réformations `[batch, seq_len, embed_dim]`à `[batch, embed_dim, seq_len]`Parce que`nn.Conv1d`Les données de sortie sont de taille fixe, quelle que soit la longueur de l'entrée.

> `transpose(1, 2)`Il va`[batch, seq_len, embed_dim]`Réchauffement`[batch, embed_dim, seq_len]`Je suis désolé .`nn.Conv1d`La sortie après la mise en place de la pile est de taille fixe, quelle que soit la longueur de l'entrée.

### Étape 2: Classificateur LSTM

```python
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_classes, bidirectional=True, dropout=0.3):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=bidirectional)
        factor = 2 if bidirectional else 1
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * factor, n_classes)

    def forward(self, token_ids):
        x = self.embed(token_ids)
        out, _ = self.lstm(x)
        pooled = out.max(dim=1).values
        return self.fc(self.dropout(pooled))
```

Pour la classification, le maximum-pooling est généralement supérieur à prendre l'ultime état caché parce que les informations à la fin d'une longue séquence ont tendance à dominer l'ultime état.

> Pour les classes, le plus grand accumulation est généralement préférable à l'arrivée cachée, car les informations du bout de la longue séquence ont tendance à dominer l'arrivée finale.

### Étape 3: la démo du gradient de disparition (intuition)

Un RNN simple sans gate ne peut pas apprendre les dépendances à long terme.`A`Il est apparu n'importe où dans une séquence.`A`Si la position 1 est à la position 1 et que la séquence est de 100 jetons, le gradient de la perte doit se dérouler à travers 99 multiplications du poids récurrent. Si le poids est inférieur à 1, le gradient disparaît.

> 没有门控的普通RNN 无法学习长程依赖――考虑一个玩具任务:预测 token `A`Si elle est présente dans n'importe quelle position de la séquence.`A`En position 1, la longueur de la séquence est de 100, le degré de perte doit passer par 99 fois le cycle de multiplication du poids. Si le poids est inférieur à 1, le degré disparaît.

```python
def vanishing_gradient_sim(seq_len, recurrent_weight=0.9):
    import math
    return math.pow(recurrent_weight, seq_len)


# At weight=0.9 over 100 steps:
#   0.9 ^ 100 ≈ 2.7e-5
# The gradient from step 100 to step 1 is effectively zero.
```

Les LSTMs la corrigent avec un **cell state**Les GRU font quelque chose de similaire avec moins de paramètres. Les deux vous donnent une formation stable à travers 100+ séquences d'étapes.

> LSTM  par un**细胞状态** Réparer ce problème, cet état ne fait que passer par l'ajout de la communication à travers le réseau  oublier la réduction de la fréquence de son travail, mais le gradient reste en mouvement le long de la "autoroute"  GRU utilise moins de paramètres pour faire des choses similaires  les deux vous permettent de vous entraîner à stabiliser sur des séquences de 100 étapes+.

### Étape 4: pourquoi cela n'était pas suffisant

Trois problèmes persistaient même avec les LSTM.

> Même s'il y a des LSTM, trois problèmes persistent.

1. **Sequential bottleneck.**La formation d'un RNN sur une séquence de longueur 1000 nécessite 1000 étapes en série vers l'avant/retour.
   **顺序瓶颈。**En train de suivre une séquence de 1000 séquences, RNN nécessite 1000 étapes de ligne droite/contre direction.
2. **Fixed-size context vector in encoder-decoder setups.**Le décodeur ne voit que l'état caché final de l'encodeur, comprimé sur l'ensemble de l'entrée. Les entrées longues perdent les détails.
   **编码器-解码器中的固定大小上下文向量。**Le décodeur ne voit que l'état caché final du codeur, comprimé l'intégralité de l'entrée.
3. **Distant-dependency accuracy ceiling.**Les LSTM dépassent les RNN simples mais ont encore du mal à propager des informations spécifiques sur plus de 200 étapes.
   **远距离依赖准确率天花板。**LSTM est supérieur à la RNN ordinaire, mais diffuser des informations spécifiques entre 200 étapes reste difficile.

L'attention a résolu les trois transformateurs ont complètement abandonné la récurrence leçon 10 est le pivot

> Attention résolu tous les trois problèmes. Le transformateur a complètement abandonné le cycle.

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

Le PyTorch's `nn.LSTM`- Je suis là .`nn.GRU`, et `nn.Conv1d`Le code de formation est standard.

> PyTorch de `nn.LSTM`- Je suis là.`nn.GRU`et `nn.Conv1d`Le code de formation est standard.

Embracer les navires face intégrations prétrainées que vous branchez comme la couche d'entrée:

> Embracer le visage  fournir un entraînement pré-installé comme un entrée layer

```python
from transformers import AutoModel

encoder = AutoModel.from_pretrained("bert-base-uncased")
for param in encoder.parameters():
    param.requires_grad = False


class BertCNN(nn.Module):
    def __init__(self, n_classes, filter_widths=(2, 3, 4), n_filters=64):
        super().__init__()
        self.encoder = encoder
        self.convs = nn.ModuleList([nn.Conv1d(768, n_filters, kernel_size=k) for k in filter_widths])
        self.fc = nn.Linear(n_filters * len(filter_widths), n_classes)

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            out = self.encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        x = out.transpose(1, 2)
        pooled = [F.max_pool1d(F.relu(conv(x)), kernel_size=conv(x).size(2)).squeeze(2) for conv in self.convs]
        return self.fc(torch.cat(pooled, dim=1))
```

Liste de contrôle de l'utilisation quand il convient.

> 适用约束检查清单──

- **Edge / on-device inference.**TextCNN avec GloVe est 10 à 100 fois plus petit qu'un transformateur.
  **边缘/设备端推理。**带 GloVe 嵌入的 TextCNN 比变压器 小 10-100 倍──如果部署目标是手机,那就是你的技术──
- **Streaming / online classification.**RNN traite un jeton à la fois; les transformateurs ont besoin de la séquence complète. Pour le texte entrant en temps réel, les LSTM gagnent toujours.
  **流式/在线分类。**RNN Chaque fois traité un jeton; Transformer  nécessite une séquence complète。 Pour le réel temps de saisie, LSTM  encore gagner ∞
- **Tiny models for baselines.**Une nouvelle tâche est rapide, entraînez un TextCNN en 5 minutes sur un processeur.
  **用于基线的微型模型。**Dans la nouvelle mission, rapide à la CPU, 5 minutes de formation en texte.
- **Sequence labeling with limited data.**BiLSTM-CRF (leçon 06) est toujours une architecture NER de qualité de production pour les phrases étiquetées 1k-10k.
  **数据有限的序列标注。**BiLSTM-CRF (第 06 课) Pour 1k-10k 标注句子 encore en production de classe NER 架构──

Tout le reste va à un transformateur.

> Tout le reste avec Transformer.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/prompt-text-encoder-picker.md`- Le numéro de la liste:

> 保存为 `outputs/prompt-text-encoder-picker.md`- Le numéro de la liste:

```markdown
---
name: text-encoder-picker
description: Pick a text encoder architecture for a given constraint set.
phase: 5
lesson: 08
---

Given constraints (task, data volume, latency budget, deploy target, compute budget), output:

1. Encoder architecture: TextCNN, BiLSTM, BiLSTM-CRF, transformer fine-tune, or "use a pretrained transformer as a frozen encoder + small head".
2. Embedding input: random init, GloVe / fastText frozen, or contextualized transformer embeddings.
3. Training recipe in 5 lines: optimizer, learning rate, batch size, epochs, regularization.
4. One monitoring signal. For RNN/CNN models: attention mechanism absence means they miss long-range deps; check per-length accuracy. For transformers: fine-tuning collapse if LR too high; check train loss.

Refuse to recommend fine-tuning a transformer when data is under ~500 labeled examples without showing that a TextCNN / BiLSTM baseline has plateaued. Flag edge deployment as needing architecture-before-everything.
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les exercices

1. **Easy.**Exercer un TextCNN sur un ensemble de données de jouets de 3 classes (vous inventez les données). Vérifiez que les largesses du filtre (2, 3, 4) dépassent en moyenne une largeur unique (3) de F1.
   **简单。**Dans un ensemble de données de 3 types de jouets, l'entraînement TextCNN (télécharger les données de votre propre invention) ⋅ test 波器宽度 (2, 3, 4) est supérieur à la moyenne F1 en termes de largeur individuelle (3).
2. **Medium.**Implémenter le pool max, le pool moyen et le pool de dernier état pour le classifiateur LSTM. Comparer sur un petit ensemble de données; document qui gagne le pooling et hypothésier pourquoi.
   **中等。**Pour LSTM, les classes de données peuvent être classées en termes de valeur moyenne et de valeur moyenne.
3. **Hard.**Construisez un tagger NER BiLSTM-CRF (combine la leçon 06 et celle-ci).
   **困难。**Construire un étiquetteur NER BiLSTM-CRF 结合第 06 课和本课) ⋅ en cours de formation en CoNLL-2003 ⋅ avec le cours 06 ⋅ de la ligne de base pure CRF et BERT 微调比较── rapport de formation Temps、内存和F1──

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Les termes clés

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| TextCNN | CNN for text / 文本 CNN | Stack of 1D convolutions over word embeddings with global max-pool. Kim (2014). / 在词嵌入上堆叠一维卷积加全局最大池化。Kim (2014)。 |
| RNN（循环神经网络） | Recurrent net / 循环网络 | Hidden state updated at each time step: `h_t = f(W x_t + U h_{t-1})`. / 每个时间步更新隐藏状态：`h_t = f(W x_t + U h_{t-1})`。 |
| LSTM | Gated RNN / 门控 RNN | Adds input / forget / output gates + a cell state. Trains stably through long sequences. / 添加输入/遗忘/输出门 + 细胞状态。在长序列上稳定训练。 |
| GRU | Simpler LSTM / 更简单的 LSTM | Two gates instead of three. Similar accuracy, fewer parameters. / 两个门代替三个。类似准确率，更少参数。 |
| Bidirectional（双向） | Both directions / 两个方向 | Forward + backward RNN concatenated. Every token sees both sides of its context. / 前向 + 后向 RNN 拼接。每个 token 看到其上下文两侧。 |
| Vanishing gradient（梯度消失） | Training signal dies / 训练信号消失 | Repeated multiplication by <1 weights in plain RNNs makes early-step gradients effectively zero. / 普通 RNN 中对小于 1 的权重反复乘法使早期步骤的梯度实际上为零。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.

## Encore une lecture

- [Kim, Y. (2014). Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1408.5882) le document TextCNN. 8 pages. Lireable. / TextCNN 论文──八页──易读──
- [Hochreiter, S. and Schmidhuber, J. (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf)Le document LSTM est inattendu et lucide.
- [Olah, C. (2015). Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/) les diagrammes qui ont rendu les LSTM accessibles à tous. /  Faites en sorte que les LSTM soient compréhensibles pour tout le monde.
