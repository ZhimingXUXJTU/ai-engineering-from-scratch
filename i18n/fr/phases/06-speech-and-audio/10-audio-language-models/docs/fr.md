# Modèles audio-langue  Qwen2.5 Omni, Audio Flamingo, GPT-4o Audio 音频语言模型

> Les modèles de langage audio 2026 débattent de la parole + son environnemental + musique. Qwen2.5-Omni-7B correspond à GPT-4o Audio sur MMAU-Pro. Audio Flamingo Next bat Gemini 2.5 Pro sur LongAudioBench. L'écart entre ouvert et fermé est essentiellement fermé  sauf sur les tâches audio multi-collés, où tout le monde est presque aléatoire.

> **【中文解读】**Le modèle de langage de 2026 ann. de l'écoute audio peut comprendre le langage + l'environnement + la musique. Qwen2.5-Omni-7B en MMAU-Pro en ligne avec GPT-4o Audio,Audio Flamingo en ligne avec LongAudioBench en ligne avec Gemini 2.5 Pro.

> **【拓展：音频大模型的新时代】**Le modèle de langue audio étendra la capacité de raisonnement de LLM au domaine de l'audio, permettant de comprendre simultanément le contenu du langage, la reconnaissance de l'environnement, l'analyse de la structure musicale.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 12 · 03 (Vision-Language Models), Phase 7 · 10 (Audio Transformers) | **前置知识:** 阶段 6 · 04（ASR），阶段 12 · 03（视觉语言模型），阶段 7 · 10（音频 Transformer）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Le problème , l' introduction du problème

Vous avez 5 secondes d'audio: les aboiements du chien, quelqu'un crie "arrête!", puis le silence.

> Tu as 5 secondes de temps: un chien crie, quelqu'un crie "arrête!", puis c'est un silence.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

- **Transcription.**"Qu'est-ce qui a été dit?"  Territoire de l'ASR.
  **转录。**"Dié quoi ?" dans le domaine de l'ASR.
- **Semantic reasoning.**"Est-ce que la personne est en danger?"  nécessite une compréhension commune des hurlements + des cris + du silence.
  **语义推理。**"C'est dangereux ?" Il faut comprendre que le chien crie.
- **Music reasoning.**"Quels instruments jouent la mélodie?"
  **音乐推理。**"Quel instrument joue à la mélodie?"
- **Long-audio retrieval.**"Dans cette conférence de 90 minutes, où l'instructeur a- t- il expliqué la descente des gradients?"
  **长音频检索。**"Dans cette conférence de 90 minutes, où le professeur a-t-il expliqué la baisse du degré?"

Un modèle unique qui répond à toutes ces questions avec un seul rappel est un **audio-language model**Separé de l'ASR pur: les LALM produisent des réponses en langage naturel de forme libre, pas seulement des transcriptions.

> Avec un seul conseil, il y a un seul modèle pour répondre à toutes ces questions.**音频语言模型**(LALM / ALM) 区别于纯 ASR:LALM 生成自由形式的自然语言答案, et pas seulement en traduisant le texte.

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![Audio-language model: audio encoder + projector + LLM decoder](../assets/alm-architecture.svg)

### Le modèle à trois composants

Chaque LALM de 2026 a le même squelette:

> ### 3 pièces

> En 2026, chaque LALM aura la même structure:

1. **Audio encoder.**Encodeur à sourcillement · BEATs · CLAP · WavLM · ou un encodeur personnalisé par modèle.
   **音频编码器。**Whisper 编码器 · BEATs · CLAP · WavLM · 或每个模型的自定义编码器──
2. **Projector.**Des fonctionnalités de l'encodeur audio de pontage linéaire ou MLP dans l'espace d'intégration de jetons du LLM.
   **投影器。**Le codeur audio est un codeur de l'écriture de la langue de l'écriture.
3. **LLM.**Décoeur à base de Llama / Qwen / Gemma. Prend le texte interligé + jetons audio; génère du texte.
   **LLM。**基于 Llama / Qwen / Gemma 的解码器──接收交织的文本 + 音频代币;生成文本──

Formation:

> 训练:

- **Stage 1.**Encoder de congélation + LLM; projecteur de train uniquement sur les données ASR / sous-titres.
  **阶段 1。**结编码器 + LLM; seulement dans l'ASR/étiquette données sur le train de projecteur。
- **Stage 2.**Mise à jour complète / LoRA sur les tâches audio suivant les instructions (QA, raisonnement, compréhension de la musique).
  **阶段 2。**Dans le cadre de la mise en œuvre de la loi de l'Union européenne, la mise en œuvre de la loi de l'Union européenne sur les droits de l'homme (CEDEAO) est une mesure de protection des droits de l'homme.
- **Stage 3 (optional).**Le voicing-in / voicing-out ajoute un décodeur de parole.
  **阶段 3（可选）。**语音入/语音出添加语音解码器──Qwen2.5Omni 和 AF3-Chat 实现了这一点──

### La carte modèle 2026

> ### 2026 année modèle

| Model | Backbone | Audio encoder | Output modality | Access |
|-------|----------|---------------|-----------------|--------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | Custom + Whisper | text + speech | Apache-2.0 |
| Qwen3-Omni | Qwen3 | Custom | text + speech | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | text | NVIDIA non-commercial |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | text | NVIDIA non-commercial |
| SALMONN | Vicuna | Whisper + BEATs | text | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | text | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | text | Apache-2.0 |
| Gemini 2.5 Flash/Pro (closed) | Gemini | proprietary | text + speech | API |
| GPT-4o Audio (closed) | GPT-4o | proprietary | text + speech | API |

| 模型 | 骨干 | 音频编码器 | 输出模态 | 访问方式 |
|------|------|-----------|---------|---------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | 自定义 + Whisper | 文本+语音 | Apache-2.0 |
| Qwen3-Omni | Qwen3 | 自定义 | 文本+语音 | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | 文本 | NVIDIA 非商业 |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | 文本 | NVIDIA 非商业 |
| SALMONN | Vicuna | Whisper + BEATs | 文本 | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | 文本 | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | 文本 | Apache-2.0 |
| Gemini 2.5 Flash/Pro（闭源） | Gemini | 专有 | 文本+语音 | API |
| GPT-4o Audio（闭源） | GPT-4o | 专有 | 文本+语音 | API |

### Réalité de référence (2026)

**MMAU-Pro.**1800 paires de QA couvrant la parole / son / musique / mélangée.

| Model | Overall | Speech | Sound | Music | Multi-audio |
|-------|---------|--------|-------|-------|-------------|
| Gemini 2.5 Pro | ~60% | 73.4% | 51.9% | 64.9% | ~22% |
| Gemini 2.5 Flash | ~57% | 73.4% | 50.5% | 64.9% | 21.2% |
| GPT-4o Audio | 52.5% | — | — | — | 26.5% |
| Qwen2.5-Omni-7B | 52.2% | 57.4% | 47.6% | 61.5% | ~20% |
| Audio Flamingo 3 | ~54% | — | — | — | — |
| Audio Flamingo Next | SOTA on LongAudioBench | — | — | — | — |

Le **multi-audio column is damning for everyone.**Le hasard sur le choix multiple de 4 options = 25%; la plupart des modèles ont un score autour de là.

> **多音频列对所有人都是致命的。**4 選 1 多選題的随机概率 = 25%; la plupart des modèles obtiennent des points en direct à proximité.

### Où les LALM sont utiles en 2026

- **Compliance audit of call-center recordings.**"L'agent a-t-il mentionné la divulgation requise?"
  **合规审计通话录音。**"C'est une déclaration de responsabilité nécessaire ?"
- **Accessibility.**Décrivez des événements sonores aux utilisateurs sourds (pas seulement la transcription).
  **无障碍。**Pour écouter les utilisateurs décrire l'événement sonore
- **Content moderation.**Détecter le langage violent + le ton menaçant + le contexte de fond.
  **内容审核。**检测暴力语言 + 威胁语气 + 背景上下文──
- **Podcast / meeting chaptering.**Résumé sémantique, pas seulement les virages de l'orateur.
  **播客/会议章节化。**语义摘要, pas seulement parler à la personne
- **Music catalog analysis.**"Réservez toutes les pistes avec un changement de clé de la section B".
  **音乐目录分析。**" Trouver tous les B's qui ont changé de couleur. "

### Où ils ne sont pas (encore) utiles

- Théorie de la musique à grains fins (en dessous du niveau d'accord).
  精细音乐理论(和弦级别以下)
- Réflexion attribuée par l'orateur sur de longues conversations (dégrades passés 10 minutes).
  长对话中的说话人归因推理 (en anglais seulement)
- Comparaison audio multi- (22-26% est à peine au-dessus du hasard).
  Il est également utilisé pour la communication de données.
- Réflexion en streaming en temps réel (la plupart sont des déductions de lot hors ligne).
  La plupart sont des démarches de démarrage.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

> **【拓展：语音 AI 的产品化】**La technologie du langage est confrontée à des défis particuliers dans la fabrication de produits: différents sons, bruits de fond, prises de vue, nombreux discours, etc. Les produits de Siri, Alexa, et de petite enfance ont été largement optimisés pour résoudre ces "problèmes de longue durée".

> **【拓展：多语言语音技术】**Les caractéristiques du langage mondial sont énormes: la voix de la langue (en chinois comme en chinois) est à un niveau élevé, les ressources linguistiques sont faibles et les données de formation manquent.




## Construisez-le et mettez-le en œuvre.
```figure
v4-alm-tokens
```

## Faites-le

### Étape 1: requête Qwen2.5-Omni

```python
from transformers import AutoModelForCausalLM, AutoProcessor

processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-Omni-7B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-Omni-7B", torch_dtype="auto")

audio, sr = load_wav("clip.wav", sr=16000)
messages = [{
    "role": "user",
    "content": [
        {"type": "audio", "audio": audio},
        {"type": "text", "text": "What sounds do you hear, and what's happening?"},
    ],
}]
inputs = processor.apply_chat_template(messages, tokenize=True, return_tensors="pt")
output = model.generate(**inputs, max_new_tokens=200)
print(processor.decode(output[0], skip_special_tokens=True))
```

### Étape 2: le modèle du projecteur

```python
import torch.nn as nn

class AudioProjector(nn.Module):
    def __init__(self, audio_dim=1280, llm_dim=4096):
        super().__init__()
        self.down = nn.Linear(audio_dim, llm_dim)
        self.act = nn.GELU()
        self.up = nn.Linear(llm_dim, llm_dim)

    def forward(self, audio_features):
        return self.up(self.act(self.down(audio_features)))
```

C'est tout. Le projecteur est généralement de 1 à 3 couches linéaires.

### Étape 3: comparation MMAU / LongAudioBench

```python
from datasets import load_dataset
mmau = load_dataset("MMAU/MMAU-Pro")

correct = 0
for item in mmau["test"]:
    answer = call_model(item["audio"], item["question"], item["choices"])
    if answer == item["correct_choice"]:
        correct += 1
print(f"Accuracy: {correct / len(mmau['test']):.3f}")
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


Rapportez-le par catégorie (speech / sound / music / multi-audio) séparément.




> **【拓展：语音与情感计算】**Le langage n'est pas seulement un moyen de transmettre des informations, il est également un moyen de transmettre des signaux émotionnels riches.

## Utilisez-le avec le cadre de réalisation

| Task | 2026 pick |
|------|-----------|
| Free-form audio QA (open) | Qwen2.5-Omni-7B |
| Best open on long audio | Audio Flamingo Next |
| Best closed | Gemini 2.5 Pro |
| Voice-in / voice-out agent | Qwen2.5-Omni or GPT-4o Audio |
| Music reasoning | Audio Flamingo 3 or 2 (music-specialized AF-CLAP) |
| Call-center audit | Gemini 2.5 Pro via API, with RAG over your policy docs |

| 任务 | 2026 年选择 |
|------|-----------|
| 自由格式音频 QA（开源） | Qwen2.5-Omni-7B |
| 最佳开源长音频 | Audio Flamingo Next |
| 最佳闭源 | Gemini 2.5 Pro |
| 语音入/语音出智能体 | Qwen2.5-Omni 或 GPT-4o Audio |
| 音乐推理 | Audio Flamingo 3 或 2（音乐专用 AF-CLAP） |
| 呼叫中心审计 | Gemini 2.5 Pro via API，配合策略文档 RAG |



## Les pièges

> 常见陷

- **Over-trust on multi-audio.**Si votre tâche a besoin de "quel clip a X", la performance au niveau aléatoire est réelle.
  **过度信任多音频。**Si votre tâche nécessite " quel segment a X ", les performances horizontales sont réelles.
- **Long-audio degradation.**Au bout de 10 minutes, la plupart des modèles ont une rupture de l'attribution des haut-parleurs.
  **长音频退化。**超过 10 分钟, la plupart des modèles de talk人归因失效──先做日志化(第 6 课),再总结──
- **Hallucinations on silence.**Le même problème de Whisper hérité des LALM qui utilisent le codeur Whisper.
  **静音上的幻觉。**Avec Whisper 编码器's LALM 继承的 Whisper 式问题相同──用 VAD 过──
- **Benchmark cherry-picking.**Les articles de blog des vendeurs mettent en évidence les catégories de meilleurs cas.
  **基准挑挑拣拣。**供应商博客文章突出最佳类别──自运行 MMAU-Pro 多音频子集──

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-alm-picker.md`. Choisissez LALM + sous-ensemble de référence + mode de sortie (texte par rapport à la parole) pour une tâche d'interprétation audio donnée.

> 保存为 `outputs/skill-alm-picker.md`◊ Pour un certain nombre de fonctions de compréhension de tâches de sélection LALM + 基准子集 + 输出模态(文本 vs 语音) ◊

## Les exercices

1. **Easy.**On court .`code/main.py`pour voir un modèle de projecteur de jouet + faux enroulement LALM de (audio-embedding, text-tokens) → jetons de sortie.
   **简单。**运行  référencement`code/main.py`查看玩具投影器模式 + 假 LALM 路由(音频嵌入,文本代币)→ 输出代币──
2. **Medium.**Comparer avec le nombre de messages du journal.
   **中等。**Dans les 100 épisodes de la série MMAU-Pro, Qwen2.5 Omni-7B est comparé aux chiffres du rapport de l'étude.
3. **Hard.**Construire une ligne de base de sous-titres audio minimale: BEATs encodeur + projecteur à 2 couches + gelé Llama-3.2-1B. Toneur fin seulement le projecteur sur AudioCaps. Comparer à SALMONN sur Clotho-AQA.
   **困难。**构建最小音频标注基线:BEATs 编码器 + 2 层投影机 + 结 Llama-3.2-1B──仅在AudioCaps 上微调投影机──在Clotho-AQA 上与SALMONN比较──

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| LALM | Audio ChatGPT | Audio encoder + projector + LLM decoder. |
| Projector | Adapter | Small MLP mapping audio features into LLM embedding space. |
| MMAU | The benchmark | 10k audio-QA pairs across speech, sound, music. |
| MMAU-Pro | Harder MMAU | 1800 multi-audio / reasoning-heavy questions. |
| LongAudioBench | Long-form eval | Multi-minute clips with semantic queries. |
| Voice-in / voice-out | Speech-native | Model ingests speech and emits speech without text detour. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| LALM | 音频 ChatGPT | 音频编码器 + 投影器 + LLM 解码器。 |
| 投影器 | 适配器 | 将音频特征映射到 LLM 嵌入空间的小型 MLP。 |
| MMAU | 那个基准 | 跨语音、声音、音乐的 1 万音频-QA 对。 |
| MMAU-Pro | 更难的 MMAU | 1800 个多音频/重推理问题。 |
| LongAudioBench | 长音频评估 | 带语义查询的多分钟片段。 |
| 语音入/语音出 | 原生语音 | 模型直接接收和输出语音，不经文本。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Chu et al. (2024). Qwen2-Audio](https://arxiv.org/abs/2407.10759) architecture de référence.
  Le projet de loi de la Commission européenne sur les droits de l'homme (CEP) est en cours de réalisation.
- [Alibaba (2025). Qwen2.5-Omni](https://huggingface.co/Qwen/Qwen2.5-Omni-7B)- Le discours dans le discours.
  Alibaba (2025). Qwen2.5-Omni语音入语音出。
- [NVIDIA (2025). Audio Flamingo 3](https://arxiv.org/abs/2507.08128)Le leader de longue voix ouverte.
  NVIDIA (2025). Audio Flamingo 3开源长音频领先者
- [NVIDIA (2026). Audio Flamingo Next](https://arxiv.org/abs/2604.10905) LongAudioBench SOTA.
  NVIDIA (2026). Audio Flamingo Suivant LongAudioBench SOTA──
- [Tang et al. (2023). SALMONN](https://arxiv.org/abs/2310.13289) pionnier du double encodeur.
  Tang 等 (2023). SALMONN双编码器先驱──
- [MMAU-Pro leaderboard](https://mmaubenchmark.github.io/) classement en direct en 2026.
  MMAU-Pro 排行榜2026 年实时排名──

> **【中文解读】**延伸阅读 a fourni des ressources de haute qualité pour l'apprentissage en profondeur, y compris des articles, des cours et des outils.

