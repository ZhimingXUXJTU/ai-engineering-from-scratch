# Construire un Tokenizer à partir de zéro

> La leçon 1 vous a donné un jouet.

> **【中文解读】**Le BPE de la première classe est un jouet, un composant de la classe de production.

> **【拓展：tiktoken/HuggingFace】**Les phrases de GPT-4 et de Llama sont des éléments de la réalisation de la production de mots.

>  **【前置】**學本节前 請先掌握:(1) Phase 10·01(Tokenizers: BPE/WordPiece/SentencePiece) 理解 BPE 合并循环和合并表的概念;(2) Unicode et UTF-8 编码codepoint、字节、NFC/NFKC 归一化的区别;(3) 正则表达式特别是`\p{L}`- Je suis là.`\p{N}`、负向先行断言 `(?!\S)`;(4) Python `regex`库( ne sont pas des normes `re`Je suis désolé .`re`Il n'est pas compatible avec la propriété Unicode.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 10, Lesson 01 (Tokenizers: BPE, WordPiece, SentencePiece)
**Time:** ~90 minutes

## Objectifs d'apprentissage

- Construire un jeton BPE de qualité de production qui gère Unicode, la normalisation de l'espace blanc et des jetons spéciaux
   Construire le traitement Unicode 空白归归化和特殊代币 的生产级 BPE 分词器
- Implémenter une rétroaction au niveau des octets afin que le jeton puisse encoder toute entrée (y compris les emoji, CJK et code) sans jetons inconnus
  实现字节级回退, faire分词器能编码任何输入(incluant les émojis、CJK、代码) sans produire un jeton inconnu
- Ajouter des modèles regex pré-tokenization qui divisent le texte aux limites des mots avant d'appliquer des fusions BPE
  添加预分词正则模式,在 BPE 合并前按词边界 分分文本
- Exercer un jeton personnalisé sur un corpus et évaluer son rapport de compression par rapport au jeton sur le texte multilingue
  En train de se définir sur le langage, il évalue sa proportion de compression avec le tiktoken

> **【中文解读】**Le but de ce cours est de mettre en place une première classe de jouets BPE  mise à niveau pour les classes de production ⋅ améliorations clés comprennent: Unicode 归一化(NFKC) 、预分词正则 ⋅ prévenir la fusion de la frontière des mots ⋅ 字节级回退 ⋅零未知代币 ⋅ ⋅ spéciaux jetons 管理 ⋅ BOS/EOS/聊天模板标记器 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                            

## Le problème , l' introduction du problème

Votre jeton BPE de leçon 01 fonctionne sur le texte anglais.

> Vous pouvez utiliser le code Python pour le traitement de texte en anglais.

Il se brise.

> Ça va s'effondrer.

Pas parce que BPE est faux - parce que la mise en œuvre est incomplète. Un tokeniseur de production gère les octets bruts dans n'importe quel codage, normalise Unicode avant de le diviser, gère des jetons spéciaux qui ne se fusionnent jamais, gère la pré-tokenization des chaînes avec la diviser des sous-parts, et fait tout cela assez rapidement pour ne pas entraver un pipeline de formation qui traite 15 billions de jetons.

> Non parce que BPE a des problèmes mais parce que la réalisation est incomplète. Production class分词器 traite les caractères originaux de tout code, en divisant avant la unification Unicode, gère toujours pas de combinaison de jetons spéciaux,串联预分词与子词分割, et toutes les opérations sont assez rapides, ne seront pas traitées 15 milliards de jetons de train de tubes de ligne.

Le jeton de GPT-2 a 50 257 jetons. Llama 3 est composé de 128 256. Le GPT-4 a environ 100 000 personnes. Ce ne sont pas des chiffres de jouets. Les tables de fusion derrière ces vocabulaires ont été formées sur des centaines de gigaoctets de texte, et les machines environnantes -- normalisation, pré-tokenization, injection de jetons spéciaux, formatage de modèles de chat -- sont ce qui sépare un tokenizer qui gère "bonjour monde" d'un qui gère l'ensemble d'Internet.

> Le GPT-2 a 50 257 jetons. Llama 3 a 128 256 jetons. GPT-4 a environ 100 000 jetons. Ce ne sont pas des jouets numériques. Ces jetons sont formés sur des centaines de Go de texte, et le mécanisme qui les entoure est la clé de la mise en œuvre de la mise en page de "bonjour" et de la mise en œuvre de la mise en page de l'ensemble de l'Internet.

Vous allez construire cette machine.

> Tu vas construire ce mécanisme.

> **【中文解读】**Le système de calcul de la classe de production n'est pas un seul algorithme, mais un système de calcul de cinq phases: regroupe → pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré pré

>  **【类比】**Le terme "BOS/EOS/PAD" est un terme qui signifie "code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de code de

> **【拓展：Llama 3 的分词器升级】**Meta 在 Llama 3 中将词表从 32K (Piece BPE de Llama 2)升级至 128K (BPE de type tiktoken), spécialement augmenté le débit de jetons de caractères non anglais. Ce changement a permis à l'efficacité de compression multilingue d'augmenter d'environ 2 fois, mais le nombre de matrices de mise en place a également augmenté de 4 fois ((32K→128K) ⋅

## Le concept de base.

### Le pipeline complet

Un jeton de production n'est pas un algorithme, c'est un pipeline de cinq étapes, chacune résolvant un problème différent.

> Le système de production de classe de mots n'est pas un seul algorithme.

```mermaid
graph LR
    A[Raw Text] --> B[Normalize]
    B --> C[Pre-Tokenize]
    C --> D[BPE Merge]
    D --> E[Special Tokens]
    E --> F[Token IDs]

    style A fill:#1a1a2e,stroke:#e94560,color:#fff
    style B fill:#1a1a2e,stroke:#e94560,color:#fff
    style C fill:#1a1a2e,stroke:#e94560,color:#fff
    style D fill:#1a1a2e,stroke:#e94560,color:#fff
    style E fill:#1a1a2e,stroke:#e94560,color:#fff
    style F fill:#1a1a2e,stroke:#e94560,color:#fff
```

Chaque étape a un travail spécifique:

> Chaque étape a des responsabilités spécifiques:

| Stage | What It Does | Why It Matters |
|-------|-------------|----------------|
| Normalize | NFKC Unicode, lowercase optional, strip accents optional | "fi" ligature (U+FB01) becomes "fi" (two chars). Without this, same word gets different tokens. |
| Pre-Tokenize | Split text into chunks before BPE | Prevents BPE from merging across word boundaries. "the cat" should never produce a token "e c". |
| BPE Merge | Apply learned merge rules to byte sequences | The core compression. Turns raw bytes into subword tokens. |
| Special Tokens | Inject [BOS], [EOS], [PAD], chat template markers | These tokens have fixed IDs. They never participate in BPE merges. The model needs them for structure. |
| ID Mapping | Convert token strings to integer IDs | The model sees integers, not strings. |

### BPE de niveau octal

Le tokenizer de la leçon 01 fonctionnait sur des octets UTF-8. C'était la bonne décision. Mais nous avons omis quelque chose d'important: que se passe-t-il lorsque ces octets ne sont pas valides UTF-8?

> Le premier élément de la classe des mots fonctionne sur les caractères UTF-8. C'est une bonne option. Mais nous avons ignoré certaines choses importantes: que se passe-t-il lorsque ces caractères ne sont pas valides dans UTF-8 ?

Le BPE de niveau octet résolve cela en traitant chaque valeur octet possible (0-255) comme un jeton valide. Votre vocabulaire de base est exactement 256 entrées. Tout fichier - texte, binaire, corrompu - peut être jetonné sans produire un jeton inconnu.

> 字节级 BPE 通过将每个可能的字节值(0-255)视为有效代币来解决这个问题――你的基础词表恰好 256条条点――任何文件文本、二进制、损坏的都可以被分词而产生未知代币――

GPT-2 a ajouté une astuce: cartographier chaque octet à un caractère Unicode imprimable afin que le vocabulaire reste lisible par l'homme.

> GPT-2 a ajouté un petit truc: mettre chaque caractère dans un caractère Unicode imprimable, pour que le texte reste lisible.

La puissance réelle: le BPE au niveau des octets traite toutes les langues de la terre. Les caractères chinois sont 3 octets UTF-8 chacun. Le japonais peut être 3 à 4 octets. L'arabe, le Devanagari, l'emoji - tout juste des séquences de octets. L'algorithme BPE trouve des motifs dans ces séquences de octets exactement de la même façon qu'il trouve des motifs dans les octets ASCII anglais.

> Le langage de l'émotion est le même que celui de l'anglais ASCII.

> **【中文解读】**Le système de programmation de caractères BPE est basé sur un système de programmation de caractères BPE. Il est également possible de créer un système de programmation de caractères BPE en utilisant des caractères BPE.

### Pré-tokenization

Avant que BPE touche votre texte, vous devez le diviser en morceaux. Cela empêche l'algorithme de fusion de créer des jetons qui couvrent les limites des mots.

> Avant de traiter votre texte en BPE, vous devez le diviser en blocs. Cela empêche les algorithmes de créer des jetons transversaux.

GPT-2 utilise un modèle regex pour diviser le texte:

> GPT-2 utilise le formulaire d'expression ordinaire pour décomposer le texte:

```
'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+
```

Ce schéma se divise en contractions ("don't" devient "don" + "'t"), mots avec des espaces de pointe optionnels, des nombres, la ponctuation et l'espace blanc.

> Cette méthode est en décomposition séparée. "ne" devient "don" + "t") 带可选前导空格的词、数字、标点和空格。

Llama utilise SentencePiece, qui saute complètement le regex. Il traite le flux de octets brut comme une longue séquence et permet à l'algorithme BPE de déterminer les limites.

> Llama utilise SentencePiece, complètement saut à travers l'expression normale. Il sera considéré comme un long séquence, laissez le BPE algorithme déterminer lui-même la limite.

Le choix est important. le regex de GPT-2 empêche le tokenizer d'apprendre que "le" à la fin d'un mot et "le" au début du suivant devraient fusionner.

> Cette sélection est importante. Le principe de la GPT-2 empêche les mots de se conformer à la "compression" du dernier mot et à la "composition" du premier mot.

### Les jetons spéciaux

Chaque tokenizer de production réserve des identifiants de jetons pour les marqueurs structurels:

> Chaque classe de production分词器都为结构标记保留代币ID:

| Token | Purpose | Used By |
|-------|---------|---------|
| `[BOS]` / `<s>` | Beginning of sequence | Llama 3, GPT |
| `[EOS]` / `</s>` | End of sequence | All models |
| `[PAD]` | Padding for batch alignment | BERT, T5 |
| `[UNK]` | Unknown token (byte-level BPE eliminates this) | BERT, WordPiece |
| `<\|im_start\|>` | Chat message boundary start | ChatGPT, Qwen |
| `<\|im_end\|>` | Chat message boundary end | ChatGPT, Qwen |
| `<\|user\|>` | User turn marker | Llama 3 |
| `<\|assistant\|>` | Assistant turn marker | Llama 3 |

Les jetons spéciaux ne sont jamais divisés par BPE. Ils sont correspondus exactement avant l'exécution de l'algorithme de fusion, remplacés par leur ID fixe, et le texte environnant est jetonné normalement.

> 特殊 token 永远不会被 BPE 拆分──它们 sont précisément correspondues avant la mise en œuvre du combiné et de l'algorithme, remplacé par un ID fixe, autour du texte normal分词──

> **【中文解读】**Le symbole spécial est le signe de conservation de "non touché" dans le mot de passe:`[BOS]`(序列开始)`[EOS]`(Commencer à la suite)`[PAD]`(Bot次填充) 聊天模板标记等── elles ont une identité fixe, ne participent jamais à la BPE 合并, mais sont éliminées par la mise en conformité préalable à la fusion──Llama 3 使用 `<|start_header_id|>`- Je suis là.`<|end_header_id|>`- Je suis là.`<|eot_id|>`Pour marquer la structure de dialogue,ChatGPT Utilisation `<|im_start|>`et `<|im_end|>`Il y a une autre.

> **【拓展：聊天模板的工程陷阱】**Le tableau de discussion est le lieu le plus facile de se tromper dans la mise en œuvre réelle. Chaque modèle utilise un jeton spécial de format spécifique lors de la formation.`chat_template`Le mécanisme de Jinja2 est pour normaliser ce processus.

> ️ **【易错点】**实现特殊 token 的三个陷:(1) **特殊 token 内含正则元字符**如 `<|im_start|>`Le centre`|`Il faut le faire .`re.escape()`转义, sinon dans GPT-2 预分词的正则上会被解析成选择符;(2) **未从 BPE 词表中排除特殊 token**若 `<|im_end|>`Non divisé avant d'être déchiré, sa séquence de caractères sera déchirée en 8 symboles, le modèle ne sera jamais visible jusqu'à ce que la structure complète soit marquée;**`add_special_tokens=False` 漏配**调用 `tokenizer.encode(text)`默认会自动加 BOS/EOS,做拼接时会出现 BOS BOS EOS EOS 序列,破坏注意力面具对齐──修复:编码时显式传 `add_special_tokens=False`Il y a aussi des modèles de logique.

### Templates de chat

C'est là que la plupart des gens se confondent et que la plupart des mises en œuvre se cassent.

> C'est là que la plupart des gens sont confus, mais aussi là où la plupart des gens réalisent des erreurs.

Lorsque vous envoyez des messages à un modèle de chat, l'API accepte une liste de messages:

> Quand vous envoyez des messages à Chat, l'API accepte une liste de messages:

```
[
  {"role": "system", "content": "You are helpful."},
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi there!"}
]
```

Le modèle ne voit pas JSON. Il voit une séquence de jetons plat. Le modèle de chat convertit les messages en cette séquence plate en utilisant des jetons spéciaux. Chaque modèle le fait différemment:

> Le modèle ne se trouve pas dans JSON. Il voit une séquence de jetons 平.

```
Llama 3:
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are helpful.<|eot_id|><|start_header_id|>user<|end_header_id|>

Hello<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Hi there!<|eot_id|>

ChatGPT:
<|im_start|>system
You are helpful.<|im_end|>
<|im_start|>user
Hello<|im_end|>
<|im_start|>assistant
Hi there!<|im_end|>
```

Si vous faites le modèle mal, le modèle produit des ordures. Il a été formé sur un format exact. Tout écart -- une nouvelle ligne manquante, un jeton échangé, un espace supplémentaire -- met l'entrée hors de la distribution de formation.

> 模板搞错了模型就会产生垃圾输出――它是在一个精确的形式上训练的――任何偏差缺少换行、交换代币、多一个空格都会使输入偏离训练分布──

> 🤔 **【困惑】**Q: Llama 3 Pourquoi abandonner SentencePiece 改用tiktoken?字节级 BPE比原版强在哪? A: 两点关键优势:(1) **SentencePiece 用 ⊗（U+2581）代替空格**, à l'ASCII 字符和原始空格的混在聊天场景下导致代币序列对即时 微小变变过敏感;tiktoken 直接保留前导空格,"hello"和"hello"是不同的代币,更稳定;**字节级 BPE 词表恰好 256 个基础 token**, théoriquement peut coder n'importe quel type de texte, y compris les émoji, ne dépend pas de la composition spécifique;SentencePiece 词表若未训练到某字符直接 (UNK) ⋅Llama 3 词表从32K 扩扩至128K,多语言压缩比升升 ~2x, c'est pour le calcul du coût de la construction.

### Vite

Python est trop lent pour la tokenization de production.

> Python est trop lent pour la production.

Tiktoken (OpenAI) est écrit en Rust avec des liaisons Python. HuggingFace Tokenizers est également Rust. SentencePiece est C++. Ils atteignent des vitesses de 10 à 100 fois supérieures à Python pur.

> tiktoken(OpenAI) avec Rust 编写并提供 Python 绑定──HuggingFace Tokenizers 也是Rust──SentencePiece 是C++──这些比纯Python 快10-100倍──

Pour la perspective: la mise en séquence de 15 billions de jetons pour Llama 3 à 1 million de jetons par seconde (Python rapide) prendrait 174 jours.

> Le nombre de jetons à la vitesse de 1 milliard de jetons par seconde est de 1,7 milliard.

Vous construisez en Python pour comprendre l'algorithme.

> Vous utilisez Python pour construire afin de comprendre les algorithmes.

## Construisez-le et mettez-le en œuvre.
```figure
weight-tying
```

## Faites-le

### Étape 1: Enchâssage au niveau octet

La base. Convertir une chaîne en une séquence de octets, cartographier chaque octet à un caractère imprimable pour affichage, et inverser le processus.

> 基础── transformera n'importe quel caractère en séquence de caractères, maquillera chaque caractère en caractères imprimables pour l'affichage, et inversera ce processus──

```python
def bytes_to_tokens(text):
    return list(text.encode("utf-8"))

def tokens_to_text(token_bytes):
    return bytes(token_bytes).decode("utf-8", errors="replace")
```

Test sur le texte multilingue pour voir le nombre de octets:

```python
texts = [
    ("English", "hello"),
    ("Chinese", "你好"),
    ("Emoji", "🔥"),
    ("Mixed", "hello你好🔥"),
]

for label, text in texts:
    b = bytes_to_tokens(text)
    print(f"{label}: {len(text)} chars -> {len(b)} bytes -> {b}")
```

"Hello" est de 5 octets. "你好" est de 6 octets (3 par caractère). L'emoji de feu est de 4 octets. Le jeton de niveau octet ne se soucie pas de quelle langue il s'agit.

> "Hello" est 5 字节──"你好" est 6 字节──每个字符 3 字节──火焰 emoji est 4 字节──字节级分词器不关心它是什么语言──字节就是字节──

### Étape 2: Pré-tokenizer avec Regex

Divisez le texte en morceaux en utilisant le modèle GPT-2 regex. Chaque morceau est sélectionné indépendamment par BPE.

> Utiliser GPT-2 正则模式将文本分成块──每个块由 BPE 独立分词──

```python
import re

try:
    import regex
    GPT2_PATTERN = regex.compile(
        r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    )
except ImportError:
    GPT2_PATTERN = re.compile(
        r"""'(?:[sdmt]|ll|ve|re)| ?[a-zA-Z]+| ?[0-9]+| ?[^\s\w]+|\s+(?!\S)|\s+"""
    )

def pre_tokenize(text):
    return [match.group() for match in GPT2_PATTERN.finditer(text)]
```

Le `regex`module prend en charge les échappes de propriété Unicode (`\p{L}`pour les lettres, `\p{N}`La bibliothèque standard `re`Le module n'a pas, donc nous revenons aux classes de caractères ASCII. Pour les jetons multilingues de production, installez `regex`- Je suis désolé .

> `regex`模块支持 Unicode 属性转义(`\p{L}`Préciseur de la lettre`\p{N}`Pour les autres, il y a un nombre de points.`re`模块不支持,所以我们回归 ASCII 字符类── Pour les différents langages de production, veuillez installer `regex`Il y a une autre.

Essayez !

```python
print(pre_tokenize("Hello, world! Don't stop."))
# [' Hello', ',', ' world', '!', " Don", "'t", ' stop', '.']
```

L'espace principal reste attaché au mot. Les contractions se divisent à l'apostrophe. La ponctuation devient sa propre pièce. BPE ne fusionnera jamais des jetons à travers ces frontières.

> Avant de commencer, le code de la ligne de référence est "B" et "B" est "B" et "B" est "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" sont "B" et "B" respectivement "B" et "B" sont "B" et "B" et "B" sont "B" et "B" et "B" sont "B" et "B" respectivement "

### Étape 3: BPE sur les séquences en octets

L'algorithme de base de la leçon 01, mais fonctionne maintenant sur des morceaux pré-tokénisés de manière indépendante.

> Le premier élément est le premier élément de l'algorithme central, mais il est maintenant indépendant de l'exploitation du bloc de prédictions.

```python
from collections import Counter

def get_byte_pairs(chunks):
    pairs = Counter()
    for chunk in chunks:
        byte_seq = list(chunk.encode("utf-8"))
        for i in range(len(byte_seq) - 1):
            pairs[(byte_seq[i], byte_seq[i + 1])] += 1
    return pairs

def apply_merge(byte_seq, pair, new_id):
    merged = []
    i = 0
    while i < len(byte_seq):
        if i < len(byte_seq) - 1 and byte_seq[i] == pair[0] and byte_seq[i + 1] == pair[1]:
            merged.append(new_id)
            i += 2
        else:
            merged.append(byte_seq[i])
            i += 1
    return merged
```

### Étape 4: Traitement des jetons spéciaux

Les jetons spéciaux ont besoin d'une correspondance exacte et d'identifiants fixes.

> Les symboles spéciaux ont besoin d'une correspondance et d'une identification fixes.

```python
class SpecialTokenHandler:
    def __init__(self):
        self.special_tokens = {}
        self.pattern = None

    def add_token(self, token_str, token_id):
        self.special_tokens[token_str] = token_id
        escaped = [re.escape(t) for t in sorted(self.special_tokens.keys(), key=len, reverse=True)]
        self.pattern = re.compile("|".join(escaped))

    def split_with_specials(self, text):
        if not self.pattern:
            return [(text, False)]
        parts = []
        last_end = 0
        for match in self.pattern.finditer(text):
            if match.start() > last_end:
                parts.append((text[last_end:match.start()], False))
            parts.append((match.group(), True))
            last_end = match.end()
        if last_end < len(text):
            parts.append((text[last_end:], False))
        return parts
```

### Étape 5: Classe de jetons complète

Chaînez tout ensemble: normaliser, diviser en jetons spéciaux, pré-tokenizer, fusionner BPE, carte à identifiants.

> Pour les autres, il est nécessaire de mettre en place un système de gestion de la gestion des données.

```python
import unicodedata

class ProductionTokenizer:
    def __init__(self):
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.special_handler = SpecialTokenHandler()
        self.next_id = 256

    def normalize(self, text):
        return unicodedata.normalize("NFKC", text)

    def train(self, text, num_merges):
        text = self.normalize(text)
        chunks = pre_tokenize(text)
        chunk_bytes = [list(chunk.encode("utf-8")) for chunk in chunks]

        for i in range(num_merges):
            pairs = Counter()
            for seq in chunk_bytes:
                for j in range(len(seq) - 1):
                    pairs[(seq[j], seq[j + 1])] += 1
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            new_id = self.next_id
            self.next_id += 1
            self.merges[best] = new_id
            self.vocab[new_id] = self.vocab[best[0]] + self.vocab[best[1]]
            chunk_bytes = [apply_merge(seq, best, new_id) for seq in chunk_bytes]

    def add_special_token(self, token_str):
        token_id = self.next_id
        self.next_id += 1
        self.special_handler.add_token(token_str, token_id)
        self.vocab[token_id] = token_str.encode("utf-8")
        return token_id

    def encode(self, text):
        text = self.normalize(text)
        parts = self.special_handler.split_with_specials(text)
        all_ids = []
        for part_text, is_special in parts:
            if is_special:
                all_ids.append(self.special_handler.special_tokens[part_text])
            else:
                for chunk in pre_tokenize(part_text):
                    byte_seq = list(chunk.encode("utf-8"))
                    for pair, new_id in self.merges.items():
                        byte_seq = apply_merge(byte_seq, pair, new_id)
                    all_ids.extend(byte_seq)
        return all_ids

    def decode(self, ids):
        byte_parts = []
        for token_id in ids:
            if token_id in self.vocab:
                byte_parts.append(self.vocab[token_id])
        return b"".join(byte_parts).decode("utf-8", errors="replace")

    def vocab_size(self):
        return len(self.vocab)
```

### Étape 6: Test multilingue

Le vrai test, lancez l'anglais, le chinois, l'emoji et le code.

> L'anglais, le chinois, l'emoji et le code sont tous oubliés.

```python
corpus = (
    "The quick brown fox jumps over the lazy dog. "
    "The quick brown fox runs through the forest. "
    "Machine learning models process natural language. "
    "Deep learning transforms how we build software. "
    "def train(model, data): return model.fit(data) "
    "def predict(model, x): return model(x) "
)

tok = ProductionTokenizer()
tok.train(corpus, num_merges=50)

bos = tok.add_special_token("<|begin|>")
eos = tok.add_special_token("<|end|>")

test_texts = [
    "The quick brown fox.",
    "你好世界",
    "Hello 🌍 World",
    "def foo(x): return x + 1",
    f"<|begin|>Hello<|end|>",
]

for text in test_texts:
    ids = tok.encode(text)
    decoded = tok.decode(ids)
    print(f"Input:   {text}")
    print(f"Tokens:  {len(ids)} ids")
    print(f"Decoded: {decoded}")
    print()
```

Les caractères chinois produisent 3 octets chacun. L'emoji produit 4 octets. Aucun de ces casse le jeton. Aucun produit des jetons inconnus. C'est la puissance de BPE au niveau des octets.

> Les émotions produisent 4 caractères. Ces éléments ne font pas tomber les mots.

> **【中文解读】**Le code supérieur va connecter tous les composants: regrouper → 特殊代币 分割 → 预分词 → BPE 合并 → ID 映射──测试覆盖英文、中文、emoji、代码和特殊代币的混合场景──字节级 BPE garantie que toute entrée ne se produit pas de jeton inconnu c'est la raison fondamentale pour laquelle il est devenu un standard industriel──

> **【拓展：分词速度的工程意义】** Pure Python 分词器每秒处理约1M tokens,Llama 3 pré-entraînement语料有1500000000 tokens,使用Python 需要174 天──tiktoken(Rust 实现) 每秒需要100M tokens,只需1.7 天──这就是为什么生产级分词器都用编译语言:tiktoken用Rust,HuggingFace tokenizers用Rust,SentencePiece用C++──

## Utilisez-le avec le cadre de réalisation

### Comparer les vrais jetons

Chargez les jetons réels de Llama 3, GPT-4 et Mistral. Voir comment chacun traite le même paragraphe multilingue.

> L'écriture de la langue est un langage de langue de l'autre.

```python
import tiktoken

gpt4_enc = tiktoken.get_encoding("cl100k_base")

test_paragraph = "Machine learning is powerful. 机器学习很强大。 L'apprentissage automatique est puissant. 🤖💪"

tokens = gpt4_enc.encode(test_paragraph)
pieces = [gpt4_enc.decode([t]) for t in tokens]
print(f"GPT-4 ({len(tokens)} tokens): {pieces}")
```

```python
from transformers import AutoTokenizer

llama_tok = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
mistral_tok = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

for name, tok in [("Llama 3", llama_tok), ("Mistral", mistral_tok)]:
    tokens = tok.encode(test_paragraph)
    pieces = tok.convert_ids_to_tokens(tokens)
    print(f"{name} ({len(tokens)} tokens): {pieces[:20]}...")
```

Vous verrez différents nombres de jetons pour le même texte. Llama 3 avec 128K vocabulaire est plus agressif à fusionner les modèles communs. GPT-4 avec 100K se trouve au milieu. Mistral avec 32K produit plus de jetons mais a une couche d'embedding plus petite.

> Vous verrez différents symboles du même texte. La taille des symboles de Llama 3 est de 128K. Les symboles de Llama 3 sont plus positifs.

Le compromis est toujours le même: un vocabulaire plus grand signifie des séquences plus courtes mais plus de paramètres.

> Le poids est toujours le même: plus grand nombre de mots signifie plus court de séquence mais plus de paramètres.

## Envoyez-le . Produit .

Cette leçon produit une demande pour la construction et le débogage des tokenizers de production.`outputs/prompt-tokenizer-builder.md`- Je suis désolé .

> Ce cours est élaboré pour la construction et la modification de la production de classe de mots.`outputs/prompt-tokenizer-builder.md`Il y a une autre.

## Les exercices

1. **Easy:**Ajouter un `get_token_bytes(id)`Il est utilisé pour vérifier ce que vos jetons fusionnés les plus courants représentent réellement.
   Le mot " accroche " est traduit par " accroche "`get_token_bytes(id)`方法,显示任意 token ID 的原始字节──用它检查您最常用的合并代币──实际代表什么──
2. **Medium:**Implémenter le pré-tokenizer de style Llama qui se divise sur l'espace blanc et les chiffres mais conserve les espaces de pointe.
   Le texte est en anglais, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français, en français
3. **Hard:**Ajoutez une méthode de modèle de chat qui prend une liste de `{"role": ..., "content": ...}`Les messages et produit la séquence de jetons correcte pour le format de chat Llama 3.
   Le mot "réponse" est traduit par "réponse".`{"role": ..., "content": ...}`消息列表并生成 Llama 3 聊天格式的正确代币序列──对照 HuggingFace 实现进行测试──

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Byte-level BPE | "Tokenizer that works on bytes" | BPE with a base vocabulary of 256 byte values -- handles any input without unknown tokens | 字节级 BPE，基础词表 256 个字节值 |
| Pre-tokenization | "Splitting before BPE" | Regex or rule-based splitting that prevents BPE from merging across word boundaries | 预分词，防止跨词边界的 token 合并 |
| NFKC normalization | "Unicode cleanup" | Canonical decomposition followed by compatibility composition -- "fi" ligature becomes "fi", fullwidth "A" becomes "A" | NFKC 归一化，统一 Unicode 表示 |
| Chat template | "How messages become tokens" | The exact format for converting a list of role/content messages into a flat token sequence -- model-specific and must match training format | 聊天模板，消息转 token 的格式规则 |
| Special tokens | "Control tokens" | Reserved token IDs that bypass BPE -- [BOS], [EOS], [PAD], chat markers -- matched exactly before merge | 特殊 token，绕过 BPE 的控制标记 |
| Fertility | "Tokens per word" | Ratio of output tokens to input words -- 1.3 for English in GPT-4, 2-3 for Korean, higher means wasted context | 生育率，每词 token 数 |
| tiktoken | "OpenAI tokenizer" | Rust BPE implementation with Python bindings -- 10-100x faster than pure Python | OpenAI 的 Rust 分词器实现 |
| Merge table | "The vocabulary" | Ordered list of byte-pair merges learned during training -- this IS the tokenizer's learned knowledge | 合并表，分词器的核心知识 |

## Encore une lecture

- [OpenAI tiktoken source](https://github.com/openai/tiktoken)-- Implementation de BPE à rouille utilisée par GPT-3.5/4
- [HuggingFace tokenizers](https://github.com/huggingface/tokenizers)-- La bibliothèque de jetons de rouille prenant en charge BPE, WordPiece, Unigram
- [Llama 3 paper (Meta, 2024)](https://arxiv.org/abs/2407.21783)-- détails sur le vocabulaire et la formation des tokenizers 128K
- [SentencePiece (Kudo & Richardson, 2018)](https://arxiv.org/abs/1808.06226)-- Tokenization linguistique
- [GPT-2 tokenizer source](https://github.com/openai/gpt-2/blob/master/src/encoder.py)-- la cartographie originale en octets vers Unicode
