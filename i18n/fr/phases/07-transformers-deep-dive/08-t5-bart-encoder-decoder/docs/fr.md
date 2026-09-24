# T5, BART  Modèles de décodeur-encodeur  T5 BART  Modèle de codeur-décodeur

> Les encoders comprennent. Les décoders génèrent. Rassemblez-les et vous obtenez un modèle construit pour les tâches d'entrée → sortie: traduire, résumer, réécrire, transcrire.

> **【中文解读】**T5 Placez toutes les tâches de PNL en un format texte à texte.

**Type:** Study | **类型:** 学习
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Les GPT et les BERT ne découtent que pour un but différent.

> 解码器专用 GPT 和编码器专用 BERT ont élaboré de nombreuses tâches naturelles sous forme d'entrée-sortie pour différents objectifs:

- Traduction: anglais → français.
  Le mot français traduit par " français ".
- Résumé: 5000 articles à jetons → 200 résumés à jetons.
  Le texte de la note est en français.
- Reconnaissance de la parole: jetons audio → jetons texte.
  Le mot de passe est le mot de passe de la langue française.
- Extraction structurée: prose → JSON.
  Le texte de la première partie de la lettre de Jérémie est écrit en français.

Pour ces derniers, le décodeur-encodeur fait le plus propre ajustement. L'encodeur produit une représentation dense de la source. Le décodeur génère la sortie, en assistant croisée à cette représentation à chaque étape.

> Pour ces tâches, le codeur-décodeur est le choix le plus approprié.

Deux documents ont défini le livre de jeu moderne:

> 两篇论文 définit le modèle moderne:

1. **T5**(Raffel et coll. 2019). " Transformateur de transfert texte-texte. " Chaque tâche de PNL est reframeée comme texte-en, texte-out. Architcture unique, vocabulaire unique, perte unique. Pré-entraîné sur la prédiction de durée masquée (spans corrompus dans l'entrée, décodez-les dans la sortie).
   Le mot grec traduit par " le mot grec "**T5**(Raffel et d'autres, 2019): "L'écriture est transférée en transformateur de texte" (en anglais seulement). Chaque tâche de PNL est redefinie en texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte de texte
2. **BART**(Lewis et coll. 2019). " Transformateur bidirectionnel et auto-régressif. " Déniant l'autoencodeur: entrée corrompue de plusieurs façons (trouble, masque, supprimer, rotation), demandez au décodeur de reconstruire l'original.
   Le mot grec traduit par " le mot grec "**BART**(Lewis 等人,2019) ――"双向自归变压器"―去噪自编码器:用多种方式破坏输入(打乱、掩码、删除、旋转),要求解码器重建原始文本。

En 2026, le format encodeur-décodeur se maintient là où la structure des entrées est importante:

> En 2026, le format de codeur-décodeur continue d'exister dans des scénarios importants de la structure d'entrée:

- Sous-pard (parler → texte).
  Le mot "soupçon" est traduit par "soupçon".
- La pile de traduction de Google.
  Le système de traduction de Google est en cours de développement.
- Certains modèles de complément de code / réparation qui ont des structures de contexte et d'édition distinctes.
  Quelques-uns ont un code complété / modifié.
- Flan-T5 et les variantes pour les tâches de raisonnement structuré.
  Le plan T5 et ses variants, utilisés pour la tâche de calcul structurel.

Le décodeur-seul a gagné le spotlight, mais le décodeur-encodeur n'a jamais disparu.

> Le modèle spécial du décodeur a gagné la lumière, mais le décodeur-codeur n'a jamais disparu.

> **【中文解读】**Le codeur-décodeur architecture reste un avantage dans les tâches structurées "输入→输出" ∞ T5 va unifier toutes les tâches de la PNL en format texte à texte, BART utilise le codeur de bruit entraînement∞ Bien que dans le domaine de la production de texte pur est remplacé par le décodeur seulement, mais dans le langage de la langue identification ((Whisper) ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ 

## Le concept de base.

![Encoder-decoder with cross-attention](../assets/encoder-decoder.svg)

### La boucle avant

```
source tokens ─▶ encoder ─▶ (N_src, d_model)  ──┐
                                                 │
target tokens ─▶ decoder block                   │
                 ├─▶ masked self-attention       │
                 ├─▶ cross-attention ◀───────────┘
                 └─▶ FFN
                ↓
              next-token logits
```

Le décodeur fonctionne autorégressivement mais assiste à la sortie du même encodeur à chaque étape.

> Le codeur ne fonctionne qu'une seule fois pour chaque entrée. Le codeur se retourne à lui-même pour chaque étape, mais il se charge de la même sortie.

> **【中文解读】**交叉注意力是编码器-解码器架构的信息桥梁:Q 来自编码器,K/V 来自编码器输出;;编码器只运行一次(高效),解码器每步都通过交叉注意力访问编码器的完整输出;;

> **【拓展：Whisper 的编码器-解码器设计】**Le modèle de reconnaissance de la langue de l'OpenAI utilise une architecture de codeur-décodeur, car le format et le texte sont complètement différents.

### T5 Pré-entraînement  Corruption de la durée

Choisissez des intervalles aléatoires de l'entrée (longueur moyenne 3 jetons, 15% au total).`<extra_id_0>`- Je suis là .`<extra_id_1>`, etc. Le décodeur ne sort que les spans corrompus avec leur préfixe sentinel:

> 随机选择输入中的片段(平均长度 3 个标志,总计 15%) ⋅ Utilisez le seul détachement de marque pour remplacer chaque fragment:`<extra_id_0>`- Je suis là.`<extra_id_1>`Écoutez, les détecteurs ne font que sortir des fragments détruits et leurs dépêches.

```
source: The quick <extra_id_0> fox jumps <extra_id_1> dog
target: <extra_id_0> brown <extra_id_1> over the lazy
```

Un signal moins cher que de prédire toute la séquence.

> Dans les expériences de dissipation de l'article T5, la concurrence est équivalente à celle de la LM (BERT) et de la LM (UniLM).

### Pré-entraînement BART  dénonciation de bruit multiples

BART essaie cinq fonctions sonores:

> BART 尝试五种噪声函数:

1. Le masquage des jetons.
   Le mot "coup" est traduit par "coup".
2. Suppression des jetons.
   Le code de démarrage est le code de démarrage.
3. Remplissez le texte (masquer une distance, le décodeur insère la longueur correcte).
   Le code de la langue française est le code de la langue française.
4. Permutation de la phrase.
   Le mot "région" est traduit par "région".
5. La rotation des documents.
   Le mot "réfléchisseur" est traduit par "réfléchisseur".

La combinaison de l'infiltration de texte + de la permutation de la phrase a produit les meilleurs nombres en aval. Le décodeur reconstruit toujours l'original.

> Le résultat est le meilleur. Le résumé de la phrase est le plus complet.

> **【中文解读】**T5 et BART: la durée de corruption de T5 est seulement prévue pour les fragments détruits (environ 1 000 pièces), le bruit de BART est codé pour reconstruire l'ensemble du processus (environ 1 000 pièces).

### L'inférence

La même génération autorégressive que GPT. L'échantillonnage avide / faisceau / top-p s'applique. La recherche de faisceau (largeur 45) est standard pour la traduction et la résumé car la distribution de sortie est plus étroite que le chat.

> 推理与 GPT的自归生成相同──贪心/束搜索/top-p 采样都适用──束搜索(宽度 4-5) est la stratégie standard de la traduction et du résumé, car la distribution de sortie est plus étroite que la distribution de dialogue──

> **【拓展：Beam Search 在翻译中的重要性】**Le modèle de codeur-décodeur est souvent utilisé dans les tâches de traduction et de résumé pour rechercher des faisceaux de données (à la largeur de 4-5), car la sortie est plus étroite.

### Quand choisir chaque variante en 2026

| Task | Encoder-decoder? | Why |
|------|------------------|-----|
| 任务 | 是否用编码器-解码器？ | 原因 |
| Translation | Yes, usually | Clear source sequence; fixed output distribution; beam search works |
| 翻译 | 通常是 | 明确的源序列；固定的输出分布；束搜索有效 |
| Speech-to-text | Yes (Whisper) | Input modality differs from output; encoder shapes audio features |
| 语音转文本 | 是（Whisper） | 输入模态与输出不同；编码器处理音频特征 |
| Chat / reasoning | No, decoder-only | No persistent "input" — the conversation is the sequence |
| 对话/推理 | 否，解码器专用 | 没有持久的"输入"——对话本身就是序列 |
| Code completion | Usually no | Decoder-only with long context wins; code models like Qwen 2.5 Coder are decoder-only |
| 代码补全 | 通常否 | 带长上下文的解码器专用胜出；Qwen 2.5 Coder 等代码模型是解码器专用 |
| Summarization | Either works | BART, PEGASUS beat earlier decoder-only baselines; modern decoder-only LLMs match them |
| 摘要 | 都可以 | BART、PEGASUS 超越早期解码器专用基线；现代解码器专用 LLM 能匹配它们 |
| Structured extraction | Either | T5 is clean because "text → text" absorbs any output format |
| 结构化提取 | 都可以 | T5 很干净，因为"文本 → 文本"可以吸收任何输出格式 |

La tendance depuis ~2022: le décodeur-seul prend en charge les tâches que le décodeur-encodeur possédait auparavant parce que (a) les LLM décodeurs-seuls réglés par instruction généralisent à n'importe quoi via une demande, (b) une architecture évolue plus facilement que deux, (c) RLHF suppose un décodeur.

> Depuis 2022, la tendance: le décodeur spécial a pris les tâches que le décodeur-décodeur avait déjà, car (a) l'instruction de décodeur spécial LLM peut être généralisée à travers des suggestions à n'importe quelle tâche, (b) une seule architecture peut être plus facile à étendre que deux, (c) RLHF supposer l'utilisation du décodeur.

> **【拓展：T5 的 text-to-text 统一范式】**Le concept de la T5 est de réaliser toutes les tâches de la PNL en tant que "textbook input→textbook output" format.

## Construisez-le et mettez-le en œuvre.
```figure
encoder-decoder
```

## Faites-le

Regardez !`code/main.py`Nous mettons en œuvre la corruption de la durée de vie T5 pour un corpus de jouets  la pièce la plus utile de cette leçon parce qu'elle apparaît dans chaque recette de prétrainement de codeur-décodeur depuis.

> 参见 `code/main.py` Nous avons réalisé un clip de T5 style pour le langage de jouets  C'est la partie la plus utile de ce cours, car il apparaît dans chaque programme de formation de prédéterminateur de codeur suivant.

### Étape 1: Corruption de la durée

```python
def corrupt_spans(tokens, mask_rate=0.15, mean_span=3.0, rng=None):
    """Pick spans summing to ~mask_rate of tokens. Return (corrupted_input, target)."""
    n = len(tokens)
    n_mask = max(1, int(n * mask_rate))
    n_spans = max(1, int(round(n_mask / mean_span)))
    ...
```

Le format cible est la convention T5: `<sent0> span0 <sent1> span1 ...`. L'entrée corrompue interpose des jetons inchangés avec les jetons sentinel à des endroits de décalage.

> 目标格式 Suivre le T5 约定:`<sent0> span0 <sent1> span1 ...` Les entrées de la destruction seront des jetons inchangés et des jetons de poste de la position 交替排列──

### Étape 2: vérifier le retour et le retour

Compte tenu de l'entrée et de la cible corrompus, reconstruire la phrase originale. Si votre corruption est réversible, le passe avant est bien défini. Ceci est une vérification de la santé mentale  la vraie formation ne fait jamais cela, mais le test est bon marché et attrape des bugs individuels dans votre comptabilité de durée.

> 给定被破坏的输入和目标,重建原始句子──如果破坏是可逆的,前向传播就是良定义的──这是一个合理性检查真实训练从不这样做,但测试成本低且能发现片段簿记中的差一错──

### Étape 3: bruit de BART

Cinq fonctions: `token_mask`- Je suis là .`token_delete`- Je suis là .`text_infill`- Je suis là .`sentence_permute`- Je suis là .`document_rotate`- Composer deux et montrer le résultat.

> 五个函数:`token_mask`- Je suis là.`token_delete`- Je suis là.`text_infill`- Je suis là.`sentence_permute`- Je suis là.`document_rotate`◊ 组合 de ces deux éléments et démontrer les résultats

## Utilisez-le avec le cadre de réalisation

Référence de HuggingFace:

> Coupe de coupe:

```python
from transformers import T5ForConditionalGeneration, T5Tokenizer
tok = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

inputs = tok("translate English to French: Attention is all you need.", return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=32)
print(tok.decode(out[0], skip_special_tokens=True))
```

Le truc T5: le nom de la tâche entre dans le texte d'entrée. Le même modèle gère des dizaines de tâches parce que chaque tâche est texte-en-tête, texte-out. En 2026, ce modèle a été généralisé par des modèles décodeurs uniquement réglés par instruction, mais T5 l'a codifié en premier.

> T5 techniques: le nom de tâche écrit dans le texte d'entrée. Le même modèle peut traiter des dizaines de tâches, car chaque tâche est un texte d'entrée-en-tête de sortie. En 2026, ce modèle a été ordonné par un modélisateur de code de déchiffrement spécial généralisé, mais T5 est le premier à le normaliser.

## Envoyez-le . Produit .

Regardez !`outputs/skill-seq2seq-picker.md`. La compétence choisit entre le décodeur-encodeur et le décodeur-encodeur uniquement pour une nouvelle tâche compte tenu de la structure d'entrée-sortie, de la latence et des objectifs de qualité.

> 参见 `outputs/skill-seq2seq-picker.md` Cette compétence est basée sur la structure d'entrée-sortie, de retard et de qualité, pour les nouvelles tâches choisir un codeur-décodeur ou une architecture spéciale de codeur-décodeur.

## Les exercices

1. **Easy.**On court .`code/main.py`, appliquer la corruption de la durée à une phrase de 30 jetons, vérifier que la concaténage des jetons source non sentinelles avec les étendues cibles décodées reproduit l'original.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`, pour une phrase de 30 tokens, l'application de la pièce de destruction, l'essai sera non-expédition de source de la pièce de théâtre et le code de résolution de l'objet de la pièce de théâtre peut être récupéré.
2. **Medium.**La mise en œuvre de la stratégie BART `text_infill`bruit: remplacer les intervalles aléatoires par un seul `<mask>`Le décodeur doit en déduire la longueur correcte de l'espace plus le contenu.
   Le BART est réalisé`text_infill`Avec un seul.`<mask>`Les symboles  替换随机片段, le décodeur doit déterminer la longueur et le contenu exacts du clip.
3. **Hard.**- Je suis bien .`flan-t5-small`Sur un petit corpus anglais → porc-latin (200 paires). Mesurer le bleu sur un ensemble de 50 paires.`Llama-3.2-1B`sur les mêmes données avec le même calcul.
   Le langage latin est traduit en latin par " pig Latin " et en latin par " pig Latin "`flan-t5-small` 50 pour les tests de la série de mesure BLEU par nombre  avec les mêmes données  les mêmes calculs`Llama-3.2-1B`Pour le contraste.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Encoder-decoder | "Seq2seq transformer" | Two stacks: bidirectional encoder for input, causal decoder with cross-attention for output. |
| 编码器-解码器 | "Seq2seq Transformer" | 两个堆栈：双向编码器处理输入，带交叉注意力的因果解码器生成输出。 |
| Cross-attention | "Where source talks to target" | Decoder's Q × encoder's K/V. The only place encoder information enters the decoder. |
| 交叉注意力 | "源与目标对话的地方" | 解码器的 Q × 编码器的 K/V。编码器信息进入解码器的唯一通道。 |
| Span corruption | "T5's pretraining trick" | Replace random spans with sentinel tokens; decoder outputs the spans. |
| 片段破坏 | "T5 的预训练技巧" | 用哨兵 token 替换随机片段；解码器输出这些片段。 |
| Denoising objective | "BART's game" | Apply a noise function to the input, train the decoder to reconstruct the clean sequence. |
| 去噪目标 | "BART 的游戏" | 对输入应用噪声函数，训练解码器重建干净序列。 |
| Sentinel token | "The `<extra_id_N>` placeholder" | Special tokens that tag corrupted spans in the source and re-tag them in the target. |
| 哨兵 token | "`<extra_id_N>` 占位符" | 在源端标记被破坏片段、在目标端重新标记的特殊 token。 |
| Flan | "Instruction-tuned T5" | T5 fine-tuned on >1,800 tasks; made encoder-decoder competitive at instruction-following. |
| Flan | "指令微调的 T5" | 在 1,800+ 任务上微调的 T5；使编码器-解码器在指令遵循方面具有竞争力。 |
| Beam search | "Decoding strategy" | Keep top-k partial sequences at each step; standard for translation/summarization. |
| 束搜索 | "解码策略" | 每步保留得分最高的 k 个部分序列；翻译/摘要的标准策略。 |
| Teacher forcing | "Training-time input" | During training, feed the true previous output token to the decoder, not the sampled one. |
| Teacher forcing | "训练时输入" | 训练时向解码器输入真实的上一个输出 token，而非采样的 token。 |

## Encore une lecture

- [Raffel et al. (2019). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683)- T5
  Le texte de la première partie est le texte de la première partie.
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461)- Je suis un homme.
  Le texte de la première partie est le suivant:
- [Chung et al. (2022). Scaling Instruction-Finetuned Language Models](https://arxiv.org/abs/2210.11416)- Le plan T5.
  Le texte de la première partie est le suivant:
- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) Whisper, le codeur-découreur canonique de 2026.
  Le thème de la rédaction de l'article est "Résumé de l'article de l'éditeur"
- [HuggingFace `modeling_t5.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/t5/modeling_t5.py) mise en œuvre de référence.
  Le film est sorti en version originale.
