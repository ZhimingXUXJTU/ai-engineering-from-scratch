# Construir un Tokenizer desde cero

> La lección 01 te dio un juguete.

> **【中文解读】**BPE de la primera clase es un juego, este curso construye un nivel de producción.

> **【拓展：tiktoken/HuggingFace】**La pieza de la oración de los tokens y las palabras de GPT-4 es la realización de los sistemas de producción.

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:(1) Fase 10·01(Tokenizers: BPE/WordPiece/SentencePiece) 理解 BPE 合并循环和合并表的概念;(2) Unicode y UTF-8 编码codepoint、字节、NFC/NFKC 归一化的区别;(3) 正则表达式特别是`\p{L}`¿Qué es esto?`\p{N}`、负向先行断言 `(?!\S)`;(4) Python `regex`库(no es estándar `re`, porque `re`No admite la propiedad Unicode)

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 10, Lesson 01 (Tokenizers: BPE, WordPiece, SentencePiece)
**Time:** ~90 minutes

## Objetivos de aprendizaje

- Construir un tokenizer BPE de producción que maneje Unicode, normalización del espacio en blanco y tokens especiales
  Construcción de procesamiento Unicode 空白归归一化和特殊代币的生产级 BPE 分词器
- Implementar fallback a nivel de byte para que el tokenizer pueda codificar cualquier entrada (incluyendo emoji, CJK y código) sin fichas desconocidas
  实现字节级回退, hacer分词器能编码任何输入(incluyendo emoji、CJK、代码) sin producir un token desconocido
- Añadir patrones de regex pre-tokenization que dividen el texto en los límites de palabras antes de aplicar fusiones de BPE
  添加预分词正则模式, en BPE 合并前按词边界 分分文本
- Entrenar un tokenizer personalizado en un corpus y evaluar su ratio de compresión contra tiktoken en texto multilingüe
  En el lenguaje entrenar a sí mismo la definición de los términos, y evaluar su comparación de compresión con el tiktoken en textos multilingüe

> **【中文解读】**El objetivo de este curso es mejorar el nivel de producción de los toys BPE en los niveles de producción de los toys. Estas son las características básicas de la red de Internet.

## El problema es la introducción del problema

Su tokenizer BPE de la lección 01 funciona con texto en inglés. Ahora lanza japonés o emoji o código Python con pestañas y espacios mixtos.

> Tu primer curso de BPE 分词器能处理英文文本──现在给它日文──或 emojis──或混合制表符和空格的 Python 代码──

Se rompe.

> Se derrumbará.

No porque BPE esté equivocado, porque la implementación es incompleta. Un tokenizer de producción maneja bytes crudos en cualquier codificación, normaliza Unicode antes de dividir, gestiona tokens especiales que nunca se fusionan, cadena pre-tokenización con subword splitting, y hace todo esto lo suficientemente rápido como para no bloquear un pipeline de entrenamiento procesando 15 billones de tokens.

> No es porque BPE tenga problemas, sino porque se realiza incompleto. Producción de un parámetro de palabras para procesar cualquier código, en la división pre-integrada Unicode, administrar siempre no participa en la combinación de tokens especiales,串联预分词与子词分分, y todas las operaciones son lo suficientemente rápidas como para procesar 15 millones de tokens.

El tokenizer de GPT-2 tiene 50.257 tokens. El Llama 3 tiene 128.256. GPT-4 tiene aproximadamente 100.000. Estos no son números de juguete. Las tablas de fusión detrás de esos vocabularios fueron entrenadas en cientos de gigabytes de texto, y la maquinaria que los rodea -- normalización, pre-tokenización, inyección de tokens especiales, formato de plantillas de chat -- es lo que separa un tokenizer que maneja "hola mundo" de uno que maneja toda Internet.

> Los componentes de GPT-2 tienen 50,257 tokens. Los componentes de Llama 3 tienen 128,256 tokens. Los componentes de GPT-4 tienen aproximadamente 100,000 tokens. Estos componentes no son números de juguete. Los componentes de GPT-2 se entrenan en un conjunto de 100 GB de texto, mientras que los mecanismos que los rodean son clave para el proceso de integración, pre-partición de palabras, tokens especiales, inserción de modelos de chat.

Vas a construir esa maquinaria.

> Construirás ese mecanismo.

> **【中文解读】**El sistema de clasificación de palabras no es un solo algoritmo, sino un conjunto de cinco fases: regeneración → 预分词 → BPE 合并 → 特殊代币注入 → ID 映射──每个阶段解决不同的问题──例如, NFKC 归一化把 "fi" 连字(U+FB01) se convierte en "fi" 两个字符,预分词防止 "the cat" 被合并出 "e c" 这样代币──

> ¿ Qué es esto ?**【类比】**Se trata de un tipo de código postal que se utiliza para el procesamiento de mensajes de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de la oficina de correos de correos de la oficina de correos de correos de la oficina de correos de correos de la oficina de correos de correos de correos de la oficina de correos de correos de correos de la oficina de correos de correos de correos de la oficina de correos de correos de correos de la oficina de correos de correos de correos de la oficina de correos de correos de correos de correos de la oficina de correos de correos de correos de la oficina de correos de correos de correos de correos de correos de correos de la oficina de correos de correos de correos de la oficina de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de la oficina de la oficina de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de la oficina de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos de correos

> **【拓展：Llama 3 的分词器升级】**Meta en Llama 3 中将词表从32K (Piece BPE de Llama 2)升级至128K (tiktoken风格字节级 BPE), especialmente aumentó el token de los caracteres no ingleses de distribución. Este cambio hizo que la eficiencia de compresión en varios idiomas se elevó aproximadamente 2 veces, pero el número de matrices de inserción también se incrementó 4 veces ((32K→128K) ⋅

## El concepto central.

### El oleoducto completo

Un tokenizer de producción no es un algoritmo, es un pipeline de cinco etapas, cada una resolviendo un problema diferente.

> El sistema de producción no es un solo algoritmo. Es una línea de tuberías de cinco etapas, cada etapa resuelve diferentes problemas.

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

Cada etapa tiene un trabajo específico:

> Cada etapa tiene una función específica:

| Stage | What It Does | Why It Matters |
|-------|-------------|----------------|
| Normalize | NFKC Unicode, lowercase optional, strip accents optional | "fi" ligature (U+FB01) becomes "fi" (two chars). Without this, same word gets different tokens. |
| Pre-Tokenize | Split text into chunks before BPE | Prevents BPE from merging across word boundaries. "the cat" should never produce a token "e c". |
| BPE Merge | Apply learned merge rules to byte sequences | The core compression. Turns raw bytes into subword tokens. |
| Special Tokens | Inject [BOS], [EOS], [PAD], chat template markers | These tokens have fixed IDs. They never participate in BPE merges. The model needs them for structure. |
| ID Mapping | Convert token strings to integer IDs | The model sees integers, not strings. |

### BPE de nivel byte

El tokenizer de la lección 01 funcionaba en bytes UTF-8. Fue la llamada correcta. Pero nos saltamos algo importante: ¿qué pasa cuando esos bytes no son válidos UTF-8?

> Primero, el primer ensayo de la sección de palabras se ejecuta en un código de UTF-8.

BPE de nivel de byte resuelve esto tratando cada valor de byte posible (0-255) como un token válido. Su vocabulario base es exactamente 256 entradas. Cualquier archivo - texto, binario, corrupto - puede ser tokenizado sin producir un token desconocido.

> 字节级 BPE 通过将每个可能的字节值(0-255)视为有效代币来解决这个问题――你的基础词表恰好 256条条点―― cualquier archivo 文本、二进制、损坏的都能被分词而产生未知代币──

GPT-2 añadió un truco: mapear cada byte a un carácter de Unicode imprimible para que el vocabulario permanezca legible por el hombre. Byte 0x20 (espacio) se convierte en el carácter "G" en su mapeo. Esto es puramente cosmético. El algoritmo no le importa.

> GPT-2 añade un plan: convertir cada caracter en un Unicode imprimible, para que el caracter se mantenga legible.

El poder real: el BPE de nivel de byte maneja todos los idiomas de la tierra. Los caracteres chinos son 3 bytes UTF-8 cada uno. El japonés puede ser 3-4 bytes. Árabe, Devanagari, emoji - todos sólo secuencias de byte. El algoritmo BPE encuentra patrones en estas secuencias de byte exactamente de la misma manera que encuentra patrones en bytes ASCII en inglés.

> El algoritmo BPE trata cada idioma de la Tierra. El alfabeto BPE es el mismo que el inglés ASCII.

> **【中文解读】**字节级 BPE:基础字符表恰好 256 字节值, cualquier entrada puede codificarse. GPT-2 también hizo un "花招" de mapear cada字节 a un caracter Unicode imprimible, hacer que el texto sea más fácil de leer.

### Pre-tokenization

Antes de que BPE toque su texto, debe dividirlo en trozos. Esto evita que el algoritmo de fusión cree tokens que abarcan los límites de las palabras.

> Antes de que el BPE procese su texto, necesita separarlo en bloques. Esto evita que el algoritmo de combinación cree tokens de transversalidad.

GPT-2 utiliza un patrón regex para dividir el texto:

> GPT-2 Uso de la expresión normal para desglosar el texto:

```
'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+
```

Este patrón se divide en contracciones ("no" se convierte en "don" + "'t"), palabras con espacios de dirección opcionales, números, puntuación y espacio blanco. El espacio de dirección se mantiene unido a la palabra, por lo que "el gato" se convierte en ["el", "el gato"], no en ["el", " ", "el gato"").

> Este modelo se abrevió en separar las partes de la letra "don" + "t") 带可选前导空格的词、数字、标点和空格。前导空格保持在词上所以"the cat" 变成 ["the", "cat"],而不是 ["the", "", "cat"]。

Llama utiliza SentencePiece, que omite regex por completo. Trata el flujo de byte crudo como una secuencia larga y permite al algoritmo BPE calcular los límites. Esto es más simple, pero le da a BPE más libertad para crear tokens de palabras cruzadas.

> Llama utiliza SentencePiece, completamente saltando sobre el ejemplar de expresión. Se considerará el original en un largo secuencia, permitiendo que el algoritmo BPE determine el límite de forma automática.

La elección es importante. el regex de GPT-2 impide que el tokenizer aprenda que "el" al final de una palabra y "el" al comienzo de la siguiente deben fusionarse. SentencePiece lo permite, lo que a veces produce una compresión más eficiente pero tokens menos interpretables.

> Esta opción es importante. La norma de GPT-2 evita que los terminales de un término se aprendan con "el" y el siguiente término comienza con "el" 并──SentencePiece permite que esto se haga, a veces generando una compresión más eficaz, pero no muy explicable.

### Tokens especiales

Cada tokenizer de producción reserva ID de tokens para marcadores estructurales:

> Cada producción de los niveles de la palabra para la estructura de marcación de ID de token:

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

Los tokens especiales nunca se dividen por BPE. Se emparejan exactamente antes de que se ejecute el algoritmo de fusión, se reemplazan con su ID fijo, y el texto circundante se tokeniza normalmente.

> Los tokens especiales nunca serán separados por BPE. Se ajustan con precisión antes de que se ejecute el algoritmo de combinación.

> **【中文解读】**特殊 token is分词器中"不可触" de la marca de retención:`[BOS]`(序列开始)`[EOS]`(序列结束)`[PAD]`(批次填充) 聊天模板标记等──它们 tienen una identificación fija, nunca participan en BPE 合并, sino que se extraen de la combinación antes de la combinación mediante la correspondencia exacta──Llama 3 使用 `<|start_header_id|>`¿Qué es esto?`<|end_header_id|>`¿Qué es esto?`<|eot_id|>`Para marcar la estructura de conversación, ChatGPT `<|im_start|>`Y `<|im_end|>`¿Qué es eso?

> **【拓展：聊天模板的工程陷阱】**聊天模板 es el lugar más fácil de salir de la implementación real. Cada modelo utiliza un token especial de un formato específico durante el entrenamiento, cualquier diferencia 缺少换行、多个空格、代币 顺序错误 都让输入偏离训练分布,导致模型输出垃圾──HuggingFace的`chat_template`Jinja2 模板机制就是为了标准化这个过程――

> ️ **【易错点】**实现 especial token 的三个陷:(1) **特殊 token 内含正则元字符**¿ Qué es esto ?`<|im_start|>`En el centro`|`, tiene que usar`re.escape()`转义,否则在 GPT-2 预分词的正则上会被解析成选择符;(2) **未从 BPE 词表中排除特殊 token**若 `<|im_end|>`No se divide antes de ser desprendido, su secuencia de caracteres se divide en 8 tokens, el modelo siempre se mira no hasta el marcado de la estructura completa;**`add_special_tokens=False` 漏配**调用 `tokenizer.encode(text)`默认会自动加 BOS/EOS,做拼接时会出现 BOS BOS EOS EOS 序列,破坏注意口罩对齐──修复:编码时显式传 `add_special_tokens=False`, finalmente por el modelo de lógica unificada en la entrada.

### Template de chat

Aquí es donde la mayoría de la gente se confunde y la mayoría de las implementaciones se rompen.

> Es donde la mayoría de la gente se encuentra en la confusión, también es donde la mayoría realiza errores.

Cuando envías mensajes a un modelo de chat, la API acepta una lista de mensajes:

> Cuando envías mensajes a Chattalk, API acepta una lista de mensajes:

```
[
  {"role": "system", "content": "You are helpful."},
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi there!"}
]
```

El modelo no ve JSON. Ve una secuencia de tokens plana. La plantilla de chat convierte mensajes en esa secuencia plana utilizando tokens especiales. Cada modelo hace esto de manera diferente:

> 模型看不到 JSON──它看到的是一个平的代币序列──聊天模板使用特殊代币将消息转换为平序列── cada modelo tiene diferentes prácticas:

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

Si la plantilla se equivoca, el modelo produce basura. Fue entrenado en un formato exacto. Cualquier desviación - una nueva línea faltante, un token cambiado, un espacio extra - pone la entrada fuera de la distribución de entrenamiento.

> 模板搞错了模型就会产生垃圾输出―― es una forma precisa de entrenamiento―― cualquier diferencia falta de cambios 交换代币、多一个空格都会使输入偏离训练分布――

> ¿ Qué es esto ?**【困惑】**P: ¿Por qué abandonó la frasePiece 改用tiktoken?字节级 BPE比原版强在哪? A: 两点关键优势:(1) **SentencePiece 用 ⊗（U+2581）代替空格**, para ASCII 字符和原始空格的混在聊天场景下导致代币序列对快速 微小变化过于敏感;tiktoken 直接保留前导空格,"hello"和"hello"是不同的代币,更稳定;**字节级 BPE 词表恰好 256 个基础 token**, en teoría puede codificar cualquier secuencia de caracteres (incluyendo emoji, caracteres de la zona privada), no depende de un lenguaje específico;SentencePiece 词表若未训练到某字符直接 (UNK) ⋅Llama 3 词表从32K 扩扩至128K,多语言压缩比升升 ~2x, esto es para la determinación del coste de compra de la decisión de construcción。

### Velocidad

Python es demasiado lento para la tokenización de producción.

> Python es demasiado lento para la producción.

Tiktoken (OpenAI) está escrito en Rust con enlaces Python. HuggingFace tokenizers también es Rust. SentencePiece es C ++. Estos logran 10-100x velocidades en Python puro.

> Tiktoken(OpenAI) con Rust 编写并提供 Python 绑定──HuggingFace tokenizers 也是Rust──SentencePiece es C++──这些比纯Python 快 10-100 倍──

Para la perspectiva: tokenizar 15 billones de tokens para Llama 3 pre-entrenamiento a 1 millón de tokens por segundo (Python rápido) tomaría 174 días.

> Por ejemplo: velocidad de 100 millones de tokens por segundo (la velocidad de Python) es de Llama 3 预训分词 1500000000 tokens 需要174天──以每秒1000000 tokens (Rust) velocidad, sólo necesita 1.7天──

Usted está construyendo en Python para entender el algoritmo. En la producción, usted usaría una implementación compilada y sólo tocar el envoltorio de Python.

> Usted utiliza Python para construir para entender el algoritmo. En la producción, usted utiliza la composición para realizar, sólo se pone en contacto con Python.

## Construye y realiza.
```figure
weight-tying
```

## Construye el mismo

### Paso 1: codificación de nivel de byte

Convierta cualquier cadena en una secuencia de bytes, mapa cada byte a un carácter imprimible para la visualización, y invierta el proceso.

> 基础── convertir cualquier caracteres en secuencias de caracteres, mapear cada caracteres a caracteres impresos para mostrar, y reversar este proceso──

```python
def bytes_to_tokens(text):
    return list(text.encode("utf-8"))

def tokens_to_text(token_bytes):
    return bytes(token_bytes).decode("utf-8", errors="replace")
```

Prueba en texto multilingüe para ver el número de bytes:

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

"Hola" es 5 bytes. "你好" es 6 bytes (3 por carácter). El emoji de fuego es 4 bytes. El tokenizer de nivel de byte no importa qué idioma es.

> "Hola" es 5 字节──"你好" es 6 字节──cada uno de los 3 字节──火焰 emoji es 4 字节──字节级分词器不关心它是什么语言──字节就是字节──

### Paso 2: Pre-tokenizer con Regex

Divide el texto en trozos usando el patrón de regex GPT-2. Cada trozo se tokeniza de forma independiente por BPE.

> Utiliza GPT-2 正则模式将文本分分成块──每块由 BPE 独立分词──

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

El `regex`el módulo admite las escapes de propiedad Unicode (`\p{L}`para las cartas, `\p{N}`La biblioteca estándar `re`El módulo no tiene, por lo que regresamos a las clases de caracteres ASCII. Para la producción de tokenizers multilingües, instalar `regex`¿ Qué ?

> `regex`模块支持 Unicode 属性转义(`\p{L}`Se dice que es un "título"`\p{N}`Se muestra el número de personas.`re`模块不支持,所以我们回归 ASCII 字符类──对于生产级多语言分词器,请安装 `regex`¿Qué es eso?

Prueba .

```python
print(pre_tokenize("Hello, world! Don't stop."))
# [' Hello', ',', ' world', '!', " Don", "'t", ' stop', '.']
```

El espacio principal se mantiene unido a la palabra. las contracciones se dividen en el apóstrofo. La puntuación se convierte en su propia pieza.

> Antes de la creación de la sociedad, el gobierno de la Unión Europea ha establecido un sistema de control de las fronteras de la UE.

### Paso 3: BPE en secuencias de byte

El algoritmo central de la Lección 01, pero ahora opera en trozos pre-tokenizados de forma independiente.

> El algoritmo central de la primera clase, pero ahora se opera independientemente de los bloques de pre-partición de palabras.

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

### Paso 4: Manejo de tokens especiales

Los tokens especiales necesitan una coincidencia exacta y identificación fija.

> Los tokens especiales necesitan una correspondencia precisa y un ID fijo.

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

### Paso 5: Clasificación completa de tokenizaje

Enlace todo juntos: normaliza, divida en tokens especiales, pre-tokenize, BPE fusionar, mapa a IDs.

> Se puede ver en el siguiente video:

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

### Paso 6: Prueba multilingüe

La prueba real, lanza inglés, chino, emoji y código.

> ¡En verdad! ¡En verdad! ¡En verdad!

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

Los caracteres chinos producen 3 bytes cada uno. El emoji produce 4 bytes. ninguno de estos se estropean el tokenizer. ninguno produce tokens desconocidos. Eso es el poder de BPE de nivel de byte.

> Los elementos de la letra se producen en el gráfico de la letra.

> **【中文解读】**Más allá de los códigos, todos los componentes se conectan:归一化 → 特殊代币 分割 → 预分词 → BPE 合并 → ID 映射――测试覆盖英文,中文,emoji,代码和特殊代币的混合场景――字节级 BPE Garantizar que ninguna entrada no se produzca un token desconocido

> **【拓展：分词速度的工程意义】**纯Python 分词器每秒处理约1M tokens,Llama 3的预训语料有15亿亿代币,使用Python 需要174天――tiktoken(Rust 实现) 每秒100M代币,只需1.7天――这就是为什么生产级分词器都用编译语言:tiktoken用Rust,HuggingFace代币器用Rust,SentencePiece用C++──

## Usalo con el marco de ejecución

### Comparar los Tokenizers reales

Cargue los tokenizers reales de Llama 3, GPT-4 y Mistral. Ve cómo cada uno maneja el mismo párrafo multilingüe.

> La información sobre la información disponible en el sitio web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de la web de de de de.

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

Verá diferentes recuentos de tokens para el mismo texto. Llama 3 con vocabulario 128K es más agresivo en la fusión de patrones comunes. GPT-4 con 100K se encuentra en el medio. Mistral con 32K produce más tokens pero tiene una capa de embebimiento más pequeña.

> Verás diferentes tokens de la misma textura. Número de tokens. La forma de la palabra de 128K de Lama 3 en el modo de combinar y de forma habitual es más activa.

La compensación es siempre la misma: un vocabulario más grande significa secuencias más cortas pero más parámetros.

> 权衡始终相同: mayor palabra表 significa secuencia más corta pero más parámetros。

## Envíe el producto .

Esta lección produce una instrucción para construir y deshacerse de tokenizers de producción.`outputs/prompt-tokenizer-builder.md`¿ Qué ?

> Este curso se ha desarrollado para la construcción y la modificación de la producción de los ordenadores de palabras.`outputs/prompt-tokenizer-builder.md`¿Qué es eso?

## Los ejercicios.

1. **Easy:**Añadir un`get_token_bytes(id)`método que muestra los bytes crudos para cualquier ID de token. Utilice para inspeccionar lo que sus tokens más comunes fusionados representan realmente.
   En inglés:`get_token_bytes(id)`方法,显示任意 token ID的原始字节──用它检查您最常用的合并代币 实际代表什么──
2. **Medium:**Implemente el pre-tokenizer de estilo Llama que se divide en espacio blanco y dígitos pero mantiene espacios de liderazgo. Compara su vocabulario con el enfoque GPT-2 regex en el mismo corpus.
   Traducción: implementar Llama 风格的预分词器,按空格和数字分分但保留前导空格── en el mismo语料 comparar su表表与 GPT-2 正则方法──
3. **Hard:**Añadir un método de plantilla de chat que toma una lista de `{"role": ..., "content": ...}`Los mensajes y produce la secuencia de tokens correcta para el formato de chat Llama 3.
   En inglés, el lenguaje de la lengua inglesa es el idioma de la lengua inglesa.`{"role": ..., "content": ...}`消息列表并生成 Llama 3 聊天格式的正确代币序列──对照 HuggingFace 实现进行测试──

## Términos clave .

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

## Más Leer más Leer más

- [OpenAI tiktoken source](https://github.com/openai/tiktoken)-- Implementación de BPE de resistencia utilizada por GPT-3.5/4
- [HuggingFace tokenizers](https://github.com/huggingface/tokenizers)-- Rust tokenizer biblioteca que admite BPE, WordPiece, Unigram
- [Llama 3 paper (Meta, 2024)](https://arxiv.org/abs/2407.21783)-- detalles sobre el vocabulario y la formación de tokenizadores de 128K
- [SentencePiece (Kudo & Richardson, 2018)](https://arxiv.org/abs/1808.06226)-- Tokenización lingüística-agnóstica
- [GPT-2 tokenizer source](https://github.com/openai/gpt-2/blob/master/src/encoder.py)-- el mapa original de byte a Unicode
