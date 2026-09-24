# Tokenización de palabras  BPE, WordPiece, Unigram, SentencePiece  子词分词  BPE、WordPiece、SentencePiece

> Los tokenizadores de palabras se ahogan con palabras invisibles, los tokenizadores de caracteres aumentan la longitud de la secuencia, los tokenizadores de palabras subdividen la diferencia, cada LLM moderno se envía a uno.
> 词级分词器在未见词上卡住──字符分词器爆炸序列长度──子词分词器取中值── cada moderno LLM 都用子词分词──

> **【中文解读】**BPE es GPT usado de分词算法, WordPiece es BERT usado de

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 5 · 04 (GloVe / FastText / Subword) | **前置知识:** Phase 5 · 01（文本处理），Phase 5 · 04（GloVe / FastText / 子词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## El problema es la introducción del problema

Tu vocabulario tiene 50.000 palabras. Un usuario escribe "no se puede tokenizar". Tu tokenizer vuelve.`[UNK]`El modelo ahora no tiene señal sobre la palabra. Lo peor: el documento del 90o percentil en su corpus tiene 40 palabras raras, lo que significa 40 bits de información perdida por documento.

> Su palabra tiene 50.000 palabras. Su usuario ha ingresado "intokenizable". Su palabra ha vuelto.`[UNK]`◊ Modelo ahora no tiene señal para este término. Más malo es que el 90o % de los documentos del lenguaje tiene 40 palabras raras, lo que significa que cada documento pierde 40 bits de información.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

La tokenización de palabras subconsumidas resuelve esto. Las palabras comunes permanecen como tokens únicos. Las palabras raras se descomponen en piezas significativas:`untokenizable`¿ Qué es esto ?`un`¿ Qué ?`token`¿ Qué ?`izable`Los datos de entrenamiento cubren todo porque cualquier cadena es en última instancia una secuencia de bytes.

> 子词分词 resolver el problema.`untokenizable`¿ Qué es esto ?`un`¿Qué es esto?`token`¿Qué es esto?`izable`❖ Entrenamiento de datos cubre todo, ya que cualquier enlace final son enlace de enlaces.

Cada LLM fronterizo en 2026 se envía en uno de los tres algoritmos (BPE, Unigram, WordPiece), envuelto en una de las tres bibliotecas (tiktoken, SentencePiece, HF Tokenizers).

> Cada LLM de 2026 años se basa en tres tipos de algoritmos (BPE, Unigram, WordPiece), envasado en tres tipos de tokens (SentencePiece, HF Tokenizers).

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

![BPE vs Unigram vs WordPiece, character-by-character](../assets/subword-tokenization.svg)

**BPE (Byte-Pair Encoding).**Comience con un vocabulario de nivel de caracteres. Cuente cada par adyacente. Combine el par más frecuente en un nuevo token. Repita hasta que alcances el tamaño del vocabulario objetivo. Algoritmo dominante: GPT-2/3/4, Llama, Gemma, Qwen2, Mistral.

> **BPE（字节对编码）。**Desde el tipo de letra se inicia. Se calcula cada uno de los parámetros de la línea de referencia.

**Byte-level BPE.**El mismo algoritmo pero con más bytes crudos (256 tokens base) en lugar de caracteres Unicode.`[UNK]`Los tokens  codifican cualquier secuencia de byte. GPT-2 utiliza 50.257 tokens (256 bytes + 50.000 fusiones + 1 especial).

> **字节级 BPE。**Es similar al algoritmo pero en el original 字节 (en inglés 字符串) 256 个基础代币) y no en Unicode 字符上──保证零 `[UNK]`Se puede codificar cualquier código de código. GPT-2 Utiliza 50,257 tokens.

**Unigram.**Comience con un vocabulario enorme. Asign a cada token una probabilidad de unigrama. Iterativamente poda los tokens cuya eliminación aumenta menos la probabilidad de registro del corpus. Probabilistic en la inferencia: puede probar tokenizations. Usado por T5, mBART, ALBERT, XLNet, Gemma.

> **Unigram。**Desde el enorme ejemplar de palabras comienza. Se distribuye a cada token en unígramo de probabilidad. Después de la eliminación de cada rama, se aumenta el mínimo de los ejemplares.

**WordPiece.**Combinando parejas que maximizan la probabilidad del cuerpo de entrenamiento en lugar de la frecuencia bruta.

> **WordPiece。**合并使训练语料似然最大化而非原始频率最高对──用于BERT、DistilBERT、ELECTRA──

**SentencePiece vs tiktoken.**SentencePiece es la biblioteca que *entraña* vocabularios (BPE o Unigram) directamente en texto Unicode crudo, codificando el espacio blanco como `▁`. tiktoken es el codificador rápido de OpenAI contra vocabularios preconstruidos; no se entrena.

> **SentencePiece vs tiktoken。**SentencePiece es una pieza de texto original de Unicode, que se puede utilizar para codificar.`▁` tiktoken es un código abierto para el programa de código abierto de palabras de la construcción previa; no se está entrenando.

Regla de oro:

> 经验法则:

- **Training a new vocabulary:**SentencePiece (multilingüe, sin pre-tokenization) o HF Tokenizers.
  **训练新词表：**SentenciaPiece(多语言,无预分词) o HF Tokenizers──
- **Fast inference against GPT vocab:**Tiktoken (cl100k_base, o200k_base).
  **针对 GPT 词表的快速推理：**¡Ticket!
- **Both:**HF Tokenizers  una biblioteca, formación + servicio.
  **两者兼有：**HF Tokenizers  一个库,训练 + 服务。

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
bpe-merge
```

## Construye el mismo

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

### Paso 1: BPE desde cero

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

La orden de fusión es importante. BPE aplica fusiones en orden de entrenamiento, por lo que fusiones anteriores crean tokens más largos que bloquean a los posteriores.

> 合并顺序很重要──BPE 按训练顺序应用合并, por lo que los primeros conjuntos crean más tokens, bloquean los posteriores conjuntos── es por eso que BPE 词表 no puede transitar el modelo de transferencia──

### Paso 2: Tokenization con los tokens y SentencePiece

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

### Paso 3: Comparación de fertilidad

```python
def fertility(text, tokenizer_fn):
    return len(tokenizer_fn(text))

# BPE on English: ~1.3 tokens/word
# BPE on Hindi: ~3.5 tokens/word
# BPE on Amharic: ~8 tokens/word
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Usalo con el marco de ejecución

Escoge por ecosistema.

> 按生态系统选择──

- **OpenAI models (GPT-4, GPT-4o):**Tiktoken. Rapida y exacta reproducción de la tokenización de OpenAI. / tiktoken──快速──精确复现 OpenAI 分词──
- **Multilingual / custom training:**Trenes de texto crudo, maneja cualquier guión. / SentencePiece。 de la formación original, tratar cualquier sistema de escritura。
- **Hugging Face models:**AutoTokenizer. Envuelve el extremo derecho automáticamente. / AutoTokenizer.
- **Maximum speed at inference:**HF Tokenizers (Rust backend) o tiktoken (Python + C). / 推理最高速度:HF Tokenizers 或 tiktoken。

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

## Envíe el producto .

Salvo como`outputs/prompt-tokenizer-picker.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/prompt-tokenizer-picker.md`¿Qué es esto ?

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

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Los ejercicios.

1. **Easy.**Entrenamiento BPE en un corpus pequeño (1000 palabras). Encodizar y decodificar 20 palabras de prueba. Verificar la fidelidad de ida y vuelta. / **简单。**En pequeño lenguaje entrenamiento BPE──编码解码 20 个测试词──验证往返保真度──
2. **Medium.**Compara la fertilidad de tokenización para inglés, chino e hindi usando cl100k_base de tiktoken.**中等。**Utiliza ticktoken comparar en inglés, chino y hindi por cada palabra.
3. **Hard.**Entrenar un modelo de SentencePiece Unigram en un corpus mixto inglés-hindi. Comparar la fertilidad con un modelo de BPE entrenado en los mismos datos. / **困难。**En el lenguaje inglés-indio mezclado, el modelo de unigrama de piezas de sentencias se compara con el modelo de BPE en el mismo dato.

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Términos clave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| BPE（字节对编码） | GPT's tokenizer / GPT 的分词器 | Iteratively merge most frequent adjacent pairs. / 迭代合并最频繁的相邻对。 |
| Unigram | T5's tokenizer / T5 的分词器 | Prune tokens from large vocabulary by likelihood. / 按似然从大词表剪枝。 |
| WordPiece | BERT's tokenizer / BERT 的分词器 | Merge pairs that maximize corpus likelihood. / 合并使语料似然最大化的对。 |
| SentencePiece | Training library / 训练库 | Train BPE or Unigram on raw text. Encodes whitespace as `▁`. / 在原始文本上训练 BPE 或 Unigram。 |
| tiktoken | OpenAI's encoder / OpenAI 编码器 | Fast encoding against pre-built GPT vocabularies. / 针对预构建 GPT 词表的快速编码。 |
| Fertility（繁殖率） | Tokens per word / 每词 token 数 | How many subword tokens a word produces. Lower is better. / 一个词产生多少子词 token。越低越好。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.

## Más Leer más Leer más

- [Sennrich et al. (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) el papel de BPE. / BPE 论文。
- [Kudo (2018). Subword Regularization](https://arxiv.org/abs/1804.10959) el papel de Unigram. / Unigram 论文。
- [SentencePiece documentation](https://github.com/google/sentencepiece) formación y servicio. / 訓練和服務──
- [tiktoken](https://github.com/openai/tiktoken) El tokenizador rápido de OpenAI. / OpenAI 快速分词器──
- [Hugging Face Tokenizers](https://huggingface.co/docs/tokenizers/) Entrenamiento respaldado por la resistencia a la resistencia + servicio. / Entrenamiento posterior a la resistencia + servicio。
