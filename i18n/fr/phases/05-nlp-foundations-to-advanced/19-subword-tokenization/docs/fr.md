# Le code de la phrase est un code de la phrase.

> Les jetons de mots s'étouffent sur des mots invisibles, les jetons de caractères augmentent la longueur de la séquence, les jetons de sous-vérités divisent la différence, chaque LLM moderne en fait un.
> Le nombre de mots dans le système de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion

> **【中文解读】**BPE est GPT utilisé par les mots, WordPiece est BERT utilisé par les mots.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 5 · 04 (GloVe / FastText / Subword) | **前置知识:** Phase 5 · 01（文本处理），Phase 5 · 04（GloVe / FastText / 子词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Le problème , l' introduction du problème

Votre vocabulaire a 50 000 mots. Un utilisateur tape "non-tokenizable". Votre tokenizer revient.`[UNK]`Le modèle n'a plus de signal sur le mot. Pire encore: le document de 90 pour cent dans votre corpus a 40 mots rares, ce qui signifie 40 bits d'informations perdues par document.

> Vous avez 50 000 mots. Les utilisateurs ont entré "non-connaissable".`[UNK]`◊ Modèle maintenant pour ce mot n'a pas de signal.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

La symbolisation des sous-parts résolve cela. Les mots communs restent des jetons uniques. Les mots rares se décomposent en morceaux significatifs:`untokenizable`- Je suis là.`un`- Je suis là .`token`- Je suis là .`izable`Les données de formation couvrent tout parce que n'importe quelle chaîne est en fin de compte une séquence de bytes.

> 子词分词解决了这个问题──常见词保持单个标语──罕见词分解为有意义的片段:`untokenizable`- Je suis là.`un`- Je suis là.`token`- Je suis là.`izable`◊ entraînement de données couvre tout, parce que tout caractère est finalement un ordre de caractères.

Chaque LLM frontalier en 2026 est livré sur l'un des trois algorithmes (BPE, Unigram, WordPiece), enveloppé dans une des trois bibliothèques (tiktoken, SentencePiece, HF Tokenizers).

> Chaque premier cycle de la formation en droit de l'homme de 2026 est basé sur trois algorithmes (BPE, Unigram, WordPiece), enveloppé dans trois types de tokens (SentencePiece, HF Tokenizers).

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

![BPE vs Unigram vs WordPiece, character-by-character](../assets/subword-tokenization.svg)

**BPE (Byte-Pair Encoding).**Commencez par un vocabulaire au niveau des caractères. Comptez chaque paire adjacente. Fusez la paire la plus fréquente dans un nouveau jeton. Répétez jusqu'à ce que vous atteigniez la taille du vocabulaire cible. Algorithme dominant: GPT-2/3/4, Llama, Gemma, Qwen2, Mistral.

> **BPE（字节对编码）。**Le plus souvent, les mots sont utilisés pour créer un nouveau symbole.

**Byte-level BPE.**Le même algorithme mais avec des octets bruts (256 jetons de base) au lieu de caractères Unicode.`[UNK]`Les tokens  sont des codes de séquences de octets. GPT-2 utilise 50 257 tokens (256 octets + 50 000 fusions + 1 spécial).

> **字节级 BPE。**Il est également utilisé dans les algorithmes de base (en français: "code") et non dans les caractères Unicode.`[UNK]`Les symboles sont tous codés.

**Unigram.**Commencez par un énorme vocabulaire. attribuez à chaque jeton une probabilité de singramme. taillez à plusieurs reprises des jetons dont la suppression augmente le moins la probabilité de log de corpus.

> **Unigram。**De la énorme expression commencent. Pour chaque symbole, on distribue le seul gramme de probabilité. Après le détachement, on déplace le plus petit nombre de symboles.

**WordPiece.**Les paires de fusion qui maximisent la probabilité du corpus d'entraînement plutôt que la fréquence brute.

> **WordPiece。**合并使训练语料似然最大化而非原始频率最高对──用于BERT、DistilBERT、ELECTRA──

**SentencePiece vs tiktoken.**SentencePiece est la bibliothèque qui entraîne les vocabulaires (BPE ou Unigram) directement sur le texte brut Unicode, en encodant l'espace blanc comme `▁`. tiktoken est le codeur rapide d'OpenAI contre les vocabulaires prédéfinis; il ne s'entraîne pas.

> **SentencePiece vs tiktoken。**SentencePiece est dans la base de données originale Unicode 文本上*训练*词表的库,将空格编码为 `▁` tiktoken est un codeur de code rapide pour les utilisateurs de l'OpenAI; il ne s'entraîne pas.

Règle générale:

> 经验法则:

- **Training a new vocabulary:**SentencePiece (multilingue, sans pré-tokenization) ou HF Tokenizers.
  **训练新词表：**La phrase "Piece" est traduite par "HF Tokenizers").
- **Fast inference against GPT vocab:**Il est également possible de modifier le code de la marque.
  **针对 GPT 词表的快速推理：**Je suis un peu dégoûté.
- **Both:**HF Tokenizers  une bibliothèque, formation + service.
  **两者兼有：**HF Tokenizers  一个库,训练 + 服务。

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.
```figure
bpe-merge
```

## Faites-le

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

### Étape 1: BPE à partir de zéro

```python
from collections import Counter, defaultdict


def train_bpe(corpus, vocab_size, special_tokens=None):
    """Train BPE tokenizer from a list of pre-tokenized word strings."""
    special_tokens = special_tokens or ["<unk>"]
    word_freqs = Counter(corpus)
    splits = {word: list(word) for word in word_freqs}
    merges = {}

    while len(special_tokens) + len(set(t for parts in splits.values() for t in parts)) + len(merges) < vocab_size:
        pair_counts = Counter()
        for word, freq in word_freqs.items():
            symbols = splits[word]
            for i in range(len(symbols) - 1):
                pair_counts[(symbols[i], symbols[i + 1])] += freq
        if not pair_counts:
            break
        best = max(pair_counts, key=pair_counts.get)
        new_token = best[0] + best[1]
        merges[best] = new_token
        for word in splits:
            symbols = splits[word]
            new_symbols = []
            i = 0
            while i < len(symbols):
                if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == best:
                    new_symbols.append(new_token)
                    i += 2
                else:
                    new_symbols.append(symbols[i])
                    i += 1
            splits[word] = new_symbols
    return merges, special_tokens


def bpe_encode(text, merges, special_tokens):
    """Encode text using learned BPE merges."""
    tokens = list(text)
    for (a, b), merged in merges.items():
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and tokens[i] == a and tokens[i + 1] == b:
                new_tokens.append(merged)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens
    return tokens
```

L'ordre de fusion est important. BPE applique des fusions dans l'ordre de formation, de sorte que des fusions antérieures créent des jetons plus longs qui bloquent les plus tardifs.

> 合并顺序很重要──BPE 按训练顺序应用合并,所以较早的合并创建更长的代币,阻止后续合并──这就是为什么BPE 词表不能跨模型移植──

### Étape 2: Tokenization avec des tokens et SentencePiece

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
tokens = enc.encode("Hello, world!")
print(tokens)           # [9906, 11, 1917, 0]
print(enc.decode(tokens))  # Hello, world!
```

```python
import sentencepiece as spm

spm.SentencePieceTrainer.train(input="corpus.txt", model_prefix="m", vocab_size=1000)
sp = spm.SentencePieceProcessor(model_file="m.model")
print(sp.encode("Hello world", out_type=str))  # ['▁Hello', '▁world']
```

### Étape 3: comparaison de la fertilité

```python
def fertility(text, tokenizer_fn):
    return len(tokenizer_fn(text))

# BPE on English: ~1.3 tokens/word
# BPE on Hindi: ~3.5 tokens/word
# BPE on Amharic: ~8 tokens/word
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

Choisissez par écosystème.

> 按生态系统选择──

- **OpenAI models (GPT-4, GPT-4o):**Tiktoken. Rapide et exact reproduction de la symbolisation de OpenAI. / tiktoken。快速、精确复现 OpenAI 分词。
- **Multilingual / custom training:**SentencePiece. Traîne à partir de texte brut, gère n'importe quel script. / SentencePiece。
- **Hugging Face models:**AutoTokenizer. Enrouler le fond droit automatiquement. / AutoTokenizer.
- **Maximum speed at inference:**HF Tokenizers (Rust backend) ou tiktoken (Python + C). / 推理最高速度:HF Tokenizers 或 tiktoken。

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/prompt-tokenizer-picker.md`- Le numéro de la liste:

> 保存为 `outputs/prompt-tokenizer-picker.md`- Le numéro de la liste:

```markdown
---
name: tokenizer-picker
description: Pick the right tokenizer for a given model or training pipeline.
phase: 5
lesson: 19
---

Given a model family or training goal, output:

1. Algorithm. BPE (GPT family), Unigram (T5 family), WordPiece (BERT family).
2. Library. tiktoken (GPT inference), SentencePiece (training), HF Tokenizers (both).
3. Vocabulary size and its impact on context window utilization.
4. Fertility estimate for the target language(s).

Refuse to mix tokenizer families in the same pipeline without explicit encode/decode boundaries.
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les exercices

1. **Easy.**Exercer BPE sur un petit corpus (1000 mots). Encodez et décodez 20 mots de test. Vérifiez la fidélité du retour. / **简单。**En particulier, les tests de qualité sont effectués en utilisant des techniques de test de qualité.
2. **Medium.**Comparer la fertilité de la tokenization pour l'anglais, le chinois et l'hindi en utilisant la base cl100k_base de tiktoken.**中等。**Utiliser des jetons comparer avec les mots anglais, chinois et indiens.
3. **Hard.**Exercer un modèle SentencePiece Unigram sur un corpus mixte anglais-hindi. Comparer la fertilité avec un modèle BPE formé sur les mêmes données. / **困难。**En train de faire des séries de synthèse en anglais-hindois avec des modèles de BPE avec des données similaires, le taux de reproduction est relativement élevé.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Les termes clés

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| BPE（字节对编码） | GPT's tokenizer / GPT 的分词器 | Iteratively merge most frequent adjacent pairs. / 迭代合并最频繁的相邻对。 |
| Unigram | T5's tokenizer / T5 的分词器 | Prune tokens from large vocabulary by likelihood. / 按似然从大词表剪枝。 |
| WordPiece | BERT's tokenizer / BERT 的分词器 | Merge pairs that maximize corpus likelihood. / 合并使语料似然最大化的对。 |
| SentencePiece | Training library / 训练库 | Train BPE or Unigram on raw text. Encodes whitespace as `▁`. / 在原始文本上训练 BPE 或 Unigram。 |
| tiktoken | OpenAI's encoder / OpenAI 编码器 | Fast encoding against pre-built GPT vocabularies. / 针对预构建 GPT 词表的快速编码。 |
| Fertility（繁殖率） | Tokens per word / 每词 token 数 | How many subword tokens a word produces. Lower is better. / 一个词产生多少子词 token。越低越好。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.

## Encore une lecture

- [Sennrich et al. (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) le papier BPE. / BPE 论文。
- [Kudo (2018). Subword Regularization](https://arxiv.org/abs/1804.10959) le papier Unigram. / Unigram 论文。
- [SentencePiece documentation](https://github.com/google/sentencepiece) formation et service. / 訓練和服務。
- [tiktoken](https://github.com/openai/tiktoken) Le jeton rapide d'OpenAI. / OpenAI 快速分词器。
- [Hugging Face Tokenizers](https://huggingface.co/docs/tokenizers/) Formation à l'aide de la rouille + service. / Rust 后端训练 + 服务。
