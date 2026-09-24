# Modèles de séquence en séquence 序列到序列模型 (Seq2Seq)

> Deux RNN prétendant être traducteurs, le goulot d'étranglement qu'ils ont rencontré est la raison de l'attention.
> Les deux RNN sont des traducteurs.

> **【中文解读】**Le mécanisme d'attention est celui inventé pour résoudre son problème.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 08 (CNNs + RNNs for Text), Phase 3 · 11 (PyTorch Intro) | **前置知识:** Phase 5 · 08（CNN 和 RNN 文本处理），Phase 3 · 11（PyTorch 入门）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

La classification trace une séquence de longueur variable à une seule étiquette. La traduction trace une séquence de longueur variable à une autre séquence de longueur variable. L'entrée et la sortie vivent dans différents vocabulaires, éventuellement dans des langues différentes, sans garantie de parité de longueur.

> Les séries de saisie sont classées en un seul et même ensemble. Les entrées et sorties peuvent être différentes dans différentes langues, la longueur est indéterminée.

L'architecture seq2seq (Sutskever, Vinyals, Le, 2014) a décrété cela avec une recette délibérément simple. Deux RNN. L'un lit la phrase source et produit un vecteur de contexte de taille fixe. L'autre lit ce vecteur et génère le jeton de la phrase cible par jeton. Le même code que vous avez écrit pour la leçon 08, collé différemment.

> Seq2seq 架构(Sutskever, Vinyals, Le, 2014) a résolu ce problème avec un schéma intentionnellement simple. Deux RNN.

Il est important de comprendre ce que cela signifie: le problème de l'échec de la PNL est le plus important dans le domaine de l'éducation.

> Il est intéressant d'apprendre pour deux raisons. Premièrement, le premier est l'échec de la plus grande valeur didactique de la PNL. Il a suscité l'attention et le transformateur est bon à tout. Deuxièmement, le programme de formation (en tant que programme de formation, programme de formation, recherche de formation) est toujours applicable à tous les systèmes de production modernes de la PNL.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

**Encoder.**Un RNN qui lit la phrase source.**context vector** un résumé de la totalité de l'entrée en taille fixe.

> **编码器（Encoder）。**Une lecture de la phrase RNN... son état caché final est**上下文向量**                                                                                                                                                                                                                                                              

**Decoder.**Un autre RNN initialement défini à partir du vecteur de contexte. À chaque étape, il prend le jeton généré précédemment comme entrée et produit une distribution sur le vocabulaire cible.`<EOS>`Le jeton est produit ou la longueur maximale est atteinte.

> **解码器（Decoder）。**另一种从上下文向量初始化的 RNN──在每一步,它将先生成的代币作为输入,产生目标词表上的分布──采样或取 argmax 选择下一个代币──将其反进去──重复直到产生`<EOS>`- Le plus grand nombre de personnes qui ont été tuées

**Training:**Perte d'entropie croisée à chaque étape du décodeur, résumée sur la séquence.

> **训练：**Chaque étape de la transition perd, en séquence, des requêtes et des réponses.

**Teacher forcing.**Pendant la formation, l'entrée du décodeur à pas en pas `t`est le symbole de vérité de base à la position `t-1`En effet, les résultats obtenus par le décodeur ne sont pas les mêmes que ceux obtenus par le décodeur.**exposure bias**- Je suis désolé .

> **教师强制（Teacher Forcing）。**訓練時,解码器在步骤 `t`La position de l'entrée est la position`t-1`Le modèle ne peut jamais apprendre à faire de erreur. Le modèle doit utiliser sa propre prédiction, donc il existe toujours une différence de distribution de formation.**暴露偏差（Exposure Bias）**Il y a une autre.

**The bottleneck.**Tout ce que le codeur a appris sur la source doit être comprimé dans ce vecteur de contexte. Les phrases longues perdent de détails. Les mots rares deviennent flou.

> **瓶颈。**Tout ce que l'écrivain a appris sur la source doit être comprimé à la taille de la phrase.

Attention (leçon 10) répare cela en laissant le décodeur regarder * chaque * encodeur caché état, pas seulement le dernier.

> Attention(第 10 课) 通过让解码器查看*每个*编码器隐藏状态(不仅仅是最后一个) 来修复这个问题――这是全部的关键点――

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
lstm-gates
```

## Faites-le

### Étape 1: un codeur

```python
import torch
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, src_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(src_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)

    def forward(self, src):
        e = self.embed(src)
        outputs, hidden = self.gru(e)
        return outputs, hidden
```

`outputs`a une forme`[batch, seq_len, hidden_dim]` un état caché par position d'entrée. `hidden`a une forme`[1, batch, hidden_dim]`La leçon 08 dit "répondre les sorties pour la classification". Ici, nous gardons l'état caché dernier comme vecteur de contexte, et ignorons les sorties par étape.

> `outputs`形状为 `[batch, seq_len, hidden_dim]` Chaque entrée est dans un état caché.`hidden`形状为 `[1, batch, hidden_dim]` Ultérieurement.  Section 08 课说 "在输出上池化做分类"──这里我们保留最后隐藏状态作为上下文向量,忽略逐步输出──

### Étape 2: décodeur

```python
class Decoder(nn.Module):
    def __init__(self, tgt_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(tgt_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, tgt_vocab_size)

    def forward(self, token, hidden):
        e = self.embed(token)
        out, hidden = self.gru(e, hidden)
        logits = self.fc(out)
        return logits, hidden
```

Le décodeur est appelé étape par étape. L'entrée: un lot de jetons individuels et l'état caché actuel. sortie: logits vocabulaire pour le jeton suivant et l'état caché mis à jour.

> 解码器每次调用一步──输入:一批单个代币 和当前隐藏状态──输出: 下一个代币的词表 logits 和更新后的隐藏状态──

### Étape 3: cycle de formation avec l'enseignant forçant

```python
def train_batch(encoder, decoder, src, tgt, bos_id, optimizer, teacher_forcing_ratio=0.9):
    optimizer.zero_grad()
    _, hidden = encoder(src)
    batch_size, tgt_len = tgt.shape
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    loss = 0.0
    loss_fn = nn.CrossEntropyLoss(ignore_index=0)

    for t in range(tgt_len):
        logits, hidden = decoder(input_token, hidden)
        step_loss = loss_fn(logits.squeeze(1), tgt[:, t])
        loss += step_loss
        use_teacher = torch.rand(1).item() < teacher_forcing_ratio
        if use_teacher:
            input_token = tgt[:, t].unsqueeze(1)
        else:
            input_token = logits.argmax(dim=-1)

    loss.backward()
    optimizer.step()
    return loss.item() / tgt_len
```

Deux boutons qui méritent d'être nommés.`ignore_index=0`Il saute des pertes sur les jetons de rembourrage. `teacher_forcing_ratio`est la probabilité d'utiliser le vrai jeton par rapport à la prédiction du modèle à chaque étape. Commencez à 1.0 (forcement complet de l'enseignant) et annulez jusqu'à ~0.5 sur l'entraînement pour combler l'écart de biais d'exposition.

> Deux éléments à noter:`ignore_index=0`- Je suis désolé.`teacher_forcing_ratio`La probabilité d'utilisation de jetons réels et de prévisions de modèle est de 1,0,0 à 0,0 pour chaque étape.

### Étape 4: boucle d'inférence (avidité)

```python
@torch.no_grad()
def greedy_decode(encoder, decoder, src, bos_id, eos_id, max_len=50):
    _, hidden = encoder(src)
    batch_size = src.shape[0]
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    output_ids = []
    for _ in range(max_len):
        logits, hidden = decoder(input_token, hidden)
        next_token = logits.argmax(dim=-1)
        output_ids.append(next_token)
        input_token = next_token
        if (next_token == eos_id).all():
            break
    return torch.cat(output_ids, dim=1)
```

Le décodeur avide choisit le token le plus probable à chaque étape. Il peut s'égarer: une fois que vous vous engagez à un token, vous ne pouvez pas le désactiver. **Beam search**Il garde le dessus...`k`Les séquences partielles sont en vie et choisit la plus haute score complète à la fin.

> 贪心解码每步选择最高概率的代币――它可能走偏: une fois que vous avez soumis un dépôt, il est impossible de le retirer――**束搜索（Beam Search）**保持排名前 `k`La partie de la séquence survient, dans la sélection finale de la séquence complète de la plus haute partie.

### Étape 5: le cou de bouteille, démontré

Formez le modèle à la copie de jouets: source `[a, b, c, d, e]`, cible `[a, b, c, d, e]`Augmentez la longueur de la séquence, observez la précision.

> Dans les jeux de copie des tâches de formation`[a, b, c, d, e]`, objectif `[a, b, c, d, e]`                                                                                                                                                                                                                                                              

```
seq_len=5   copy accuracy: 98%
seq_len=10  copy accuracy: 91%
seq_len=20  copy accuracy: 62%
seq_len=40  copy accuracy: 23%
```

Un seul état caché GRU ne peut pas mémoriser sans perte une entrée de 40 jetons. L'information est là à chaque étape de l'encodeur, mais le décodeur ne voit que l'état dernier.

> 单个GRU 隐藏状态无法无损记忆 40 代币的输入――信息存在于每个编码器步骤中,但解码器只看到最后状态――注意力直接修复了这个问题――

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

PyTorch a été .`nn.Transformer`et `nn.LSTM`- basé sur des modèles de seq2seq.`transformers`Les modèles de codeur-décodeur complets (BART, T5, mBART, NLLB) sont formés sur des milliards de jetons.

> Il y a une torche .`nn.Transformer`et à base`nn.LSTM`模板──Hugging Face of `transformers`Les données de la base de données sont fournies par le système de gestion des données.

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tok = AutoTokenizer.from_pretrained("facebook/bart-base")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

src = tok("Translate this to French: Hello, how are you?", return_tensors="pt")
out = model.generate(**src, max_new_tokens=50, num_beams=4)
print(tok.decode(out[0], skip_special_tokens=True))
```

Les décodeurs modernes ont laissé tomber les RNN pour les transformateurs. La forme de haut niveau (encodeur, décodeur, générer des jetons par des jetons) est identique au papier seq2seq 2014. Le mécanisme à l'intérieur de chaque bloc est différent.

> Le Transformer moderne a remplacé RNN── haute structure(编码器、解码器、个代币 生成) avec le seq2seq 2014 论文 est complètement le même── chaque bloc interne est différent.

### Quand encore trouver le seq2seq basé sur le RNN

Pour les nouveaux projets, il y a des exceptions:

> Pour les nouveaux projets, il n'y a pratiquement aucune exception:

- Translation en streaming où vous consommez une entrée à la fois avec une mémoire limitée.
  流式翻译, chaque symbole 消耗输入,内存有界──
- Génération de texte sur appareil où le coût de la mémoire du transformateur est prohibitif.
  设备端文本生成,Transformer 内存成本过高──
- Comprendre le goulet d'étranglement entre le codeur et le décodeur est le chemin le plus rapide pour comprendre pourquoi les transformateurs ont gagné.
  Le changement de format est le plus rapide.

### Les préjugés d'exposition et leurs atténuations

- **Scheduled sampling.**Le rapport de force des enseignants pendant la formation afin que le modèle apprenne à se remettre de ses propres erreurs.
  **计划采样（Scheduled Sampling）。** Pendant l'entraînement, le professeur de retrait obligatoire, laisse le modèle de l'école récupérer de ses erreurs
- **Minimum risk training.**Traînez sur le score BLEU au niveau de la phrase au lieu de l'entropie croisée au niveau des jetons.
  **最小风险训练（Minimum Risk Training）。**En train de faire des exercices de niveau BLEU, les fractions sont plus rapprochées de ce que vous voulez.
- **Reinforcement learning fine-tuning.**Récompenser le générateur de séquences avec une métrique utilisée dans le RLHF moderne.
  **强化学习微调。**Utilisation de la formation professionnelle en médecine moderne

Les trois sont toujours applicables à la génération basée sur des transformateurs.

> Cette méthode est toujours applicable à la production basée sur Transformer.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/prompt-seq2seq-design.md`- Le numéro de la liste:

> 保存为 `outputs/prompt-seq2seq-design.md`- Le numéro de la liste:

```markdown
---
name: seq2seq-design
description: Design a sequence-to-sequence pipeline for a given task.
phase: 5
lesson: 09
---

Given a task (translation, summarization, paraphrase, question rewrite), output:

1. Architecture. Pretrained transformer encoder-decoder (BART, T5, mBART, NLLB) is the default. RNN-based seq2seq only for specific constraints.
2. Starting checkpoint. Name it (`facebook/bart-base`, `google/flan-t5-base`, `facebook/nllb-200-distilled-600M`). Match the checkpoint to task and language coverage.
3. Decoding strategy. Greedy for deterministic output, beam search (width 4-5) for quality, sampling with temperature for diversity. One sentence justification.
4. One failure mode to verify before shipping. Exposure bias manifests as generation drift on longer outputs; sample 20 outputs at the 90th-percentile length and eyeball.

Refuse to recommend training a seq2seq from scratch for under a million parallel examples. Flag any pipeline that uses greedy decoding for user-facing content as fragile (greedy repeats and loops).
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les exercices

1. **Easy.**Mettre en œuvre la tâche de copie du jouet. Exercer un GRU seq2seq sur des paires d'entrée-sortie où la cible est égale à la source. Mesurer la précision aux longueurs 5, 10, 20.
   **简单。**实现玩具复制任务──训练 GRU seq2seq 在目标等于源的输入输出对上──测量长度 5、10、20 的准确率──复现瓶──
2. **Medium.**Ajouter le décoding de recherche de faisceau avec largeur de faisceau 3. Mesurer le bleu sur un petit corpus parallèle contre la cupidité. Document où la recherche de faisceau gagne (généralement les derniers jetons) et où cela ne fait aucune différence.
   **中等。**添加束宽度为 3束搜索解码──在小平行语料上测量对贪心的蓝色──记录束搜索在哪里胜出(habituellement les derniers jetons)以及在哪里没有区别──
3. **Hard.**- Je suis bien .`facebook/bart-base`Comparer la sortie de faisceau 4 du modèle finement ajusté avec celle du modèle de base sur les entrées conservées.
   **困难。**Dans le 10 000 pour la libération de données`facebook/bart-base`◊ dans le groupe 4 de la modélisation de la différence entre la différence de sortie et la différence de sortie et de sortie de la base.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Les termes clés

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Encoder（编码器） | Input RNN / 输入 RNN | Reads source. Produces per-step hidden states and a final context vector. / 读取源。产生逐步隐藏状态和最终上下文向量。 |
| Decoder（解码器） | Output RNN / 输出 RNN | Initialized from context vector. Generates target tokens one at a time. / 从上下文向量初始化。逐个生成目标 token。 |
| Context vector（上下文向量） | The summary / 摘要 | Final encoder hidden state. Fixed size. The bottleneck attention solves. / 最终编码器隐藏状态。固定大小。注意力解决的瓶颈。 |
| Teacher forcing（教师强制） | Use true tokens / 使用真实 token | Feed the ground-truth previous token at training time. Stabilizes learning. / 训练时馈入真实的前一个 token。稳定学习。 |
| Exposure bias（暴露偏差） | Train/test gap / 训练/测试差距 | Model trained on true tokens never practiced recovering from its own mistakes. / 在真实 token 上训练的模型从未练习从自己的错误中恢复。 |
| Beam search（束搜索） | Better decoding / 更好的解码 | Keep top-k partial sequences alive at each step instead of committing greedily. / 每步保持排名前 k 的部分序列存活，而非贪心提交。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.

## Encore une lecture

- [Sutskever, Vinyals, Le (2014). Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215) le papier original de la suite.
- [Cho et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078) introduit le GRU et le cadre de codeur-décodeur. / 引入了 GRU 和编码器-解码器框架──
- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) le papier d'attention. Lisez immédiatement après cette leçon. / 注意力论文──在本课后立即阅读──
- [PyTorch NLP from Scratch tutorial](https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html) Seq2seq + code attention. / 可构建的 seq2seq + 注意力代码──
