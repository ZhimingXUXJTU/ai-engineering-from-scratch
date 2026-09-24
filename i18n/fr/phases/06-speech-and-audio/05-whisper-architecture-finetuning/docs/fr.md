# Sous-pardon  Architecture et réglage de la peau 

> Whisper est un transformer de fenêtre de 30 secondes, encodeur-décoeur, formé sur 680 000 heures de paires audio-texte multilingues mal supervisées.

> **【中文解读】**Whisper est un transformateur de 30 secondes, un programme de formation en 680 000 heures en plus de langues.

> **【拓展：Whisper 的生态】**Le mot "souple" est un mot qui signifie "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou "souple" ou

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 5 · 10 (Attention), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 04（ASR），阶段 5 · 10（注意力机制），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Le problème , l' introduction du problème

Whisper, publié par OpenAI en septembre 2022, était le premier modèle ASR à être livré comme une marchandise: coller audio, obtenir du texte, 99 langues, résistant au bruit, fonctionne sur un ordinateur portable.

> Whisper est publié par OpenAI en septembre 2022 et est le premier modèle ASR publié comme produit général: adhérence audio, obtenir du texte, 99 langues, résistance au bruit, utilisable sur un ordinateur.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

Mais Whisper n'est pas un pipeline que vous pouvez traiter comme une boîte noire pour toujours.

> Mais le murmure n'est pas un flux de l'eau qui peut être utilisé à jamais dans la boîte noire.

1. Ce qu'il est vraiment à l'intérieur.
   Elle est à l'intérieur de la structure.
2. Comment le faire en morceaux, en streaming ou en long format audio correctement.
   Comment le faire correctement pour le faire entrer en morceaux ?
3. Quand et comment.
   Qu'est-ce que cela signifie ?

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


## Le concept de base.

![Whisper encoder-decoder, tasks, chunked inference, fine-tune](../assets/whisper.svg)

**Architecture.**Transformateur standard encodeur-décodeur.

> **架构。**标准 Transformer 编码器-解码器。

- Entrée: spectrogramme log-mel de 30 secondes, 80 mels, 10 ms hop → 3000 images.
  输入30 秒 log-mail 频谱图,80 mels,10 ms 步长 → 3000 ──短片段零填充,长片段分块──
- Encodeur: échantillon de con-down (étape 2) + `N`Pour les grandes v3: 32 couches, 1280-dim, 20 têtes.
  编码器:卷积下采样(步幅 2) + `N`个 Transformer 块──Large-v3:32 层,1280 维,20 头──
- Décoder: `N`Les blocs transformateurs avec auto-attn + croisé-attn à la sortie d'encodeur.
  解码器:`N`个带因果自注意力 + Transformer 块──与编码器同大小──
- Résultat: des jetons BPE sur un vocabulaire de 51 865 jetons.
  输出:51,865 jeton 词表上的 BPE jeton。

Le grand-v3 a des paramètres de 1,55B. Turbo utilise un décodeur à 4 couches (à partir de 32), réduisant la latence 8x avec un impact WER de < 1%.

> Le nombre de références de la référencement est de 15,5 milliards.

**The prompt format.**Whisper est un modèle multitâche dirigé par des jetons spéciaux dans le décodeur prompt:

> **提示格式。**Whisper est un modèle multi-tasks, à travers un jeton spécial dans le codeur de pointe pour contrôler:

```
<|startoftranscript|><|en|><|transcribe|><|notimestamps|> Hello world.<|endoftext|>
```

- `<|en|>` tag de langue; force le comportement de traduction versus transcription.
  `<|en|>` 语言标签; forces traduction ou transcription
- `<|transcribe|>`ou `<|translate|>` traduire la sortie anglaise à partir d'une entrée en n'importe quelle langue, ou littéralement.
  `<|transcribe|>`Ou `<|translate|>` From any language输入翻译为英文输出,或逐字转录──
- `<|notimestamps|>` Sauter les timestamps au niveau des mots (plus rapidement).
  `<|notimestamps|>`Je suis en train de faire une petite fête.

Le prompt est ce qui permet à un modèle de faire de nombreuses tâches.`<|en|>`à `<|fr|>`et il transcrit le français.

> Le conseil est de faire un modèle pour effectuer plusieurs tâches.`<|en|>`改为 `<|fr|>`Pour le transcrire en français.

**30-second window.**Tout est fixé à 30 secondes. Les clips plus longs doivent être déchiquetés; les clips plus courts sont rembourrés. Les fenêtres ne sont pas diffusées en streaming natif  c'est pourquoi WhisperX, Whisper-Streaming et faster-whisper existent.

> **30 秒窗口。**Tout est à 30 secondes pour basé. Les émissions de plus de temps ont besoin de blocs; les émissions de plus de temps ont besoin de combustion.

**Log-mel normalization.** `(log_mel - mean) / std`Vous devez utiliser le préprocessage de Whisper (`whisper.audio.log_mel_spectrogram`), pas `librosa.feature.melspectrogram`- Je suis désolé .

> **Log-mel 归一化。** `(log_mel - mean) / std`, dont la statistique provient de Whisper  propre entraînement语料──你*must*use Whisper 的预处理(`whisper.audio.log_mel_spectrogram`), plutôt que `librosa.feature.melspectrogram`Il y a une autre.

### Variantes en 2026

> ### Changements de l'année 2026

| Variant | Params | Latency (A100) | WER (LibriSpeech-clean) |
|---------|--------|----------------|------------------------|
| Tiny | 39M | 1× realtime | 5.4% |
| Base | 74M | 1× | 4.1% |
| Small | 244M | 1× | 3.0% |
| Medium | 769M | 1× | 2.7% |
| Large-v3 | 1.55B | 2× | 1.8% |
| Large-v3-turbo | 809M | 8× | 1.58% |
| Whisper-Streaming (2024) | 1.55B | streaming | 2.0% |

| 变体 | 参数量 | 延迟（A100） | WER（LibriSpeech-clean） |
|------|--------|--------------|-------------------------|
| Tiny | 3900 万 | 1× 实时 | 5.4% |
| Base | 7400 万 | 1× | 4.1% |
| Small | 2.44 亿 | 1× | 3.0% |
| Medium | 7.69 亿 | 1× | 2.7% |
| Large-v3 | 15.5 亿 | 2× | 1.8% |
| Large-v3-turbo | 8.09 亿 | 8× | 1.58% |
| Whisper-Streaming（2024） | 15.5 亿 | 流式 | 2.0% |

### Réglage de la qualité

> ### 微调

Flux de travail canonique en 2026:

> Le processus standard de l'année 2026:

1. Ramasser 10100 heures d'audio pour le domaine cible avec des transcriptions alignées.
   收集 10-100 小时目标领域的音频及对应转录文本──
2. On court .`transformers.Seq2SeqTrainer`avec `generate_with_loss`Je vous rappelle.
   Utilisation `transformers.Seq2SeqTrainer`et `generate_with_loss`Réfléchissez à ce que je vais faire.
3. Paramètre-efficacité:`q_proj`- Je suis là .`k_proj`- Je suis là .`v_proj`Les couches d'attention réduisent la mémoire de la GPU 4x avec un coût de WER de < 0,3.
   参数高效: dans le niveau de l'attention `q_proj`- Je suis là.`k_proj`- Je suis là.`v_proj`上使用Lora,GPU内存降低4倍,WER 损失 <0.3──
4. Fermez le codeur si vous avez < 10 heures.
   Si les données ne sont pas suffisantes, il suffit de les modifier.
5. Utilisez le propre jetonnisateur et le format prompt de Whisper; ne changez jamais de jetonnisateur.
   Utilisez votre propre jeton et votre propre jeton.

Résultats communautaires: ajustement de la durée moyenne de 20 heures de dictation médicale réduit la RER de 12% à 4,5% du vocabulaire médical.

> 社区结果: en 20 小时医疗口述上微调 Média, la moyenne des taux de réaction des médicaments est passée de 12% à 4,5%

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.



## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

```figure
sp-asr-attention
```

## Faites-le

### Étape 1: exécuter Whisper hors de la boîte

```python
import whisper
model = whisper.load_model("large-v3-turbo")
result = model.transcribe(
    "clip.wav",
    language="en",
    task="transcribe",
    temperature=0.0,
    condition_on_previous_text=False,  # prevents runaway repetition
)
print(result["text"])
for seg in result["segments"]:
    print(f"[{seg['start']:.2f}–{seg['end']:.2f}] {seg['text']}")
```

Les défauts clés que vous devez toujours annuler: `temperature=0.0`(échantillonnage des défauts à 0,0 → 0,2 → 0,4 ... chaîne de retrait), `condition_on_previous_text=False`(évitant le problème de l' hallucination en cascade), et `no_speech_threshold=0.6`(détection du silence).

> Vous devriez toujours couvrir la clé de la valeur par défaut:`temperature=0.0`(en anglais seulement, 0,0 → 0,2 → 0,4 ...`condition_on_previous_text=False`(prévenir les problèmes de connexion) et `no_speech_threshold=0.6`Je suis en train de vous dire:

### Étape 2: forme longue en morceaux

```python
# whisperx is the 2026 reference for long-form with word-level timestamps
import whisperx
model = whisperx.load_model("large-v3-turbo", device="cuda", compute_type="float16")
segments = model.transcribe("1hour.mp3", batch_size=16, chunk_size=30)
```

WhisperX ajoute (1) le gate Silero VAD, (2) l'alignement au niveau du mot via wav2vec 2.0, (3) la diarisation via `pyannote.audio`Le cheval de travail de 2026 pour la transcription de production.

> WhisperX 添加了 (1) Silero VAD 门控,(2) 通过 wav2vec 2.0 实现词级对齐,(3) 通过 `pyannote.audio`实现说话人分离──2026年生产转录的主力工具──

### Étape 3: régler avec LoRA

```python
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from peft import LoraConfig, get_peft_model

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3-turbo")
lora = LoraConfig(
    r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1, bias="none", task_type="SEQ_2_SEQ_LM",
)
model = get_peft_model(model, lora)
# model.print_trainable_parameters()  -> ~3M trainable / 809M total
```

Puis la boucle de formation standard, un point de contrôle tous les 1000 pas, et une évaluation avec WER.

> Ensuite, le standard de formation  entraînement cycle ⋅ chaque 1000 étapes de conservation de point de contrôle ⋅ en résidence ⋅ utilisation de l'évaluation WER ⋅

### Étape 4: inspecter ce que chaque couche apprend

```python
# Grab cross-attention weights during decode to see what the decoder attends to.
with torch.inference_mode():
    out = model.generate(
        input_features=features,
        return_dict_in_generate=True,
        output_attentions=True,
    )
# out.cross_attentions: layer × head × step × src_len
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


Visualisez avec une carte thermique  vous verrez l'alignement diagonal en scannant les étapes du décodeur à travers les cadres d'encodeur. Cette diagonale est la notion de Whisper de timestamps de mots.

> Utilisez la chaleur du tableau de bord pour voir le décodeur dans le scanner du temps.




> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

La pile de 2026:

> 2026:

| Situation | Pick |
|-----------|------|
| General English, offline | Large-v3-turbo via `whisperx` |
| Mobile / edge | Whisper-Tiny quantized (int8) or Moonshine |
| Multilingual long-form | Large-v3 via `whisperx` + diarization |
| Low-resource language | Fine-tune Medium or Turbo with LoRA |
| Streaming (2 s latency) | Whisper-Streaming or Parakeet-TDT |
| Word-level timestamps | WhisperX (forced alignment via wav2vec 2.0) |

| 场景 | 选择 |
|------|------|
| 通用英文、离线 | 通过 `whisperx` 使用 Large-v3-turbo |
| 移动端/边缘设备 | 量化 Whisper-Tiny（int8）或 Moonshine |
| 多语言长音频 | 通过 `whisperx` 使用 Large-v3 + 说话人分离 |
| 低资源语言 | 用 LoRA 微调 Medium 或 Turbo |
| 流式（2 秒延迟） | Whisper-Streaming 或 Parakeet-TDT |
| 词级时间戳 | WhisperX（通过 wav2vec 2.0 强制对齐） |

`faster-whisper`(CTranslate2 backend) est le plus rapide CPU + GPU déduction runtime en 2026  4x plus rapide que la vanille avec une sortie identique.

> `faster-whisper`(CTranslate2 后端) est le processeur + GPU le plus rapide de l'année 2026 推理运行时比原始版本快4倍,输出完全相同──



## Des pièges qui vont encore arriver en 2026

> 2026 est toujours en train de tomber

- **Hallucinated text on silence.**Les paroles de la chanson "Whisper" sont formées sur des légendes comme "Thanks for watching!", "Subscribe!", toujours VAD-gate avant d'appeler.
  **静音上的幻觉文本。**Whisper dans le cadre de l'entraînement, contient "Merci de vous avoir regardé!"
- **`condition_on_previous_text` cascade.**Une hallucination pollue les fenêtres suivantes.`False`à moins que vous ayez besoin de fluidité à travers les morceaux.
  **`condition_on_previous_text` 级联。**Une fois que la pollution est apparue, la fenêtre est mise en place.`False`Il y a une autre.
- **Short-clip padding.**Un clip de 2 secondes rembourré à 30 secondes peut halluciner dans le silence qui suit.`pad=False`ou la porte VAD.
  **短片段填充。**2 secondes de temps pour le remplissage jusqu'à 30 secondes peut être utilisé pour le remplissage de l'image.`pad=False`Ou bien, vous avez été blessé.
- **Wrong mel stats.**L'utilisation de la libérosa mels au lieu de Whisper produit une sortie presque aléatoire.`whisper.audio.log_mel_spectrogram`- Je suis désolé .
  **错误的 mel 统计量。**Utiliser des mélanges de bibliothèque et non des sons de chuchotement produira presque toutes sortes de sorties. Utiliser`whisper.audio.log_mel_spectrogram`Il y a une autre.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-whisper-tuner.md`- Conceptionner un pipeline de résonance ou d'inférence Whisper pour un domaine donné.

> 保存为 `outputs/skill-whisper-tuner.md`◊ Pour un domaine déterminé de conception

## Les exercices

1. **Easy.**On court .`code/main.py`Il symbolise une requête de style Whisper, calcule les budgets de forme décodés et imprime le calendrier des pièces pour un clip de 10 minutes.
   **简单。**运行  référencement`code/main.py`Il a été créé par le gouvernement de la République de Suède pour la première fois en 2011.
2. **Medium.**Installez`faster-whisper`, transcrire un podcast de 10 minutes, comparer WER à une transcription humaine.`language="auto"`contre forcé`language="en"`- Je suis désolé .
   **中等。**Montage`faster-whisper`, Transcription 10 minutes播客, avec une traduction artificielle comparée à WER.`language="auto"`Avec une obligation`language="en"`Il y a une autre.
3. **Hard.**Utilisation de HF `datasets`, choisissez une langue avec laquelle Whisper lutte (par exemple, l'urdu), ajustez le moyen avec le LoRA pendant 2 époques sur 2 heures, et rapportez le delta WER.
   **困难。**Utilisation de la HF `datasets`, choisir un langage difficile à chuchoter (en français), en utilisant le langage LoRA 微调 Medium 2 个时代, rapport WER 差值──

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 30-sec window | Whisper's limit | Hard input cap; chunk longer audio. |
| SOT | Start-of-transcript | `<\|startoftranscript\|>` kicks off the decoder prompt. |
| Timestamps token | Temporal alignment | Every 0.02 s offset is a special token in the 51k vocab. |
| Turbo | The fast variant | 4-decoder layers, 8× faster, <1% WER regression. |
| WhisperX | The long-form wrapper | VAD + Whisper + wav2vec alignment + diarization. |
| LoRA fine-tune | Efficient tuning | Add low-rank adapters to attention; train ~0.3% of params. |
| Hallucination | The silent failure | Whisper produces fluent English from noise/silence. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| 30 秒窗口 | Whisper 的限制 | 硬性输入上限；更长音频需分块。 |
| SOT | 转录开始 | `<\|startoftranscript\|>` 启动解码器提示。 |
| 时间戳 token | 时间对齐 | 每 0.02 秒偏移是 51k 词表中的特殊 token。 |
| Turbo | 快速变体 | 4 层解码器，快 8 倍，WER 回退 <1%。 |
| WhisperX | 长音频封装 | VAD + Whisper + wav2vec 对齐 + 说话人分离。 |
| LoRA 微调 | 高效调优 | 在注意力层添加低秩适配器；仅训练约 0.3% 参数。 |
| 幻觉 | 静默失败 | Whisper 从噪声/静音中产生流畅的英文。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Radford et al. (2022). Whisper paper](https://arxiv.org/abs/2212.04356) l'architecture et la recette de formation originales.
  Radford et autres (2022).
- [OpenAI (2024). Whisper Large-v3-turbo release](https://github.com/openai/whisper/discussions/2363)Décoeur à 4 couches, accélération 8 fois.
  OpenAI (2024). Whisper Large-v3-turbo 发布4 层解码器,8 倍加速──
- [Bain et al. (2023). WhisperX](https://arxiv.org/abs/2303.00747)- Longues, alignées sur les mots, quotidiennes.
  La première fois que je suis venu ici, j'ai entendu parler de la musique.
- [Systran — faster-whisper repo](https://github.com/SYSTRAN/faster-whisper) CTranslate2 supporté, 4x plus rapide.
  Systranfaster-whisper 仓库CTranslate2 后端,快4 倍──
- [HuggingFace — Whisper fine-tune tutorial](https://huggingface.co/blog/fine-tune-whisper) L'ACE canonique / traversée à plein FT.
  Coups de tête  Sourires 微调教程 标准 LoRA/全参数微调指南。

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

