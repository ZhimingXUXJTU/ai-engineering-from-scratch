# Construindo um Tokenizer a partir do zero

> A lição 01 deu-te um brinquedo.

> **【中文解读】**Primeiro curso BPE é um brinquedo, este curso é construído para produção de classes.

> **【拓展：tiktoken/HuggingFace】**A frase de GPT-4 para tickokens e lamas são implementadas em uma classe de produção.

> - Não .**【前置】**学本节前请先掌握:(1) Fase 10·01(Tokenizers: BPE/WordPiece/SentencePiece) 理解 BPE 合并循环和合并表的概念;(2) Unicode e UTF-8 编码codepoint、字节、NFC/NFKC 归一化的区别;(3) 正则表达式特别是`\p{L}`- Não.`\p{N}`、负向先行断言 `(?!\S)`;(4) Python `regex`Não é padrão.`re`Porque ...`re`Não suporta propriedade Unicode)。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 10, Lesson 01 (Tokenizers: BPE, WordPiece, SentencePiece)
**Time:** ~90 minutes

## Objetivos de aprendizagem

- Construir um tokenizer BPE de nível de produção que lida com Unicode, normalização do espaço branco e tokens especiais
  Construir processamento Unicode、空白归归一化和特殊代币的生产级 BPE 分词器
- Implementar fallback de nível de byte para que o tokenizer possa codificar qualquer entrada (incluindo emoji, CJK e código) sem tokens desconhecidos
  实现字节级回退, fazer分词器能编码任何输入(incluindo emoji、CJK、代码) sem produzir token desconhecido
- Adicionar padrões regex pré-tokenization que dividem o texto em limites de palavras antes de aplicar fusões BPE
  添加预分词正则模式,在 BPE 合并前按词边界分文本
- Treinar um tokenizer personalizado em um corpus e avaliar sua relação de compressão contra o tiktoken em texto multilingue
  Em linguagem, treinar a auto-definição de palavras, e avaliar a sua comparação com a de tiktoken em textos multilingues

> **【中文解读】**Este curso tem como objetivo dar a primeira aula de brinquedos BPE  upgrade para produção de classes 词器.

## O problema é o problema da introdução

O tokenizer do BPE da lição 01 funciona com texto em inglês, agora atira japonês, emoji, código Python com separadores e espaços mistos.

> Sua primeira aula de BPE 分词器能处理英文文本──现在给它日文──或emoji──或混合制表符和空格的Python代码──

- Está a quebrar.

> Vai cair.

Não porque o BPE esteja errado, porque a implementação é incompleta. Um tokenizer de produção lida com bytes brutos em qualquer codificação, normaliza Unicode antes de se dividir, gerencia tokens especiais que nunca se fundem, cadeias de pré-tokenização com subword splitting, e faz tudo isso rápido o suficiente para não bloquear um pipeline de treinamento processando 15 trilhões de tokens.

> Não é porque o BPE tem problemas, mas porque a implementação é incompleta. O sistema de produção de divisões de palavras processou qualquer código, em divisão antes de unificação do Unicode, gerenciou sempre não participou da unificação de tokens especiais,串联预分词与子词分割,并且所有操作都足够快,不会成为处理15亿代币的训练管线的瓶.

O tokenizer do GPT-2 tem 50.257 tokens. Llama 3 tem 128.256. O GPT-4 tem cerca de 100.000. Estes não são números de brinquedo. As tabelas de fusão por trás desses vocabulários foram treinadas em centenas de gigabytes de texto, e as máquinas que as rodeiam -- normalização, pré-tokenização, injeção especial de tokens, formatamento de modelos de bate-papo -- é o que separa um tokenizer que lida com "Hello World" de um que lida com toda a internet.

> O GPT-2 tem 50.257 tokens. O Llama 3 tem 128.256 tokens. O GPT-4 tem cerca de 100.000. Estes não são números de brinquedos. O conjunto de palavras que estão por trás destes está treinado em 100 GB de texto, enquanto o mecanismo em torno deles é a regeneração, a regeneração, a regeneração, a regeneração, a regeneração, a regeneração e a regeneração de tokens.

Vais construir essa máquina.

> Vais construir esse mecanismo.

> **【中文解读】**O sistema de classificação de dados não é um único algoritmo, mas sim uma linha de dados de cinco fases:归一化 → 预分词 → BPE 合并 → 特殊代币注入 → ID 映射──每个阶段解决不同的问题──例如, NFKC 归一化把 "fi" 连字(U+FB01) se transforma em "fi" 两个字符,预分词防止 "cat" 被合并出 "e c" 这样代币──

> - Não .**【类比】**O seu nome é "BOS/EOS/PAD", mas não está sempre envolvido no pacote de palavras, apenas é "página de código postal" (ID) e qualquer pacote é perdido, o seu nome é "BOS/EOS/PAD".

> **【拓展：Llama 3 的分词器升级】**Meta em Llama 3 中将词表从 32K (Piece BPE de Llama 2) upgrade to 128K (BPE de Llama 2)), especialmente aumentou o distribuição de tokens de letras não-inglês. Esta mudança aumentou a eficiência de compressão em vários idiomas cerca de 2 vezes, mas o número de matrizes embutidas também deve aumentar 4 vezes ((32K→128K) ⋅

## O conceito central.

### O oleoduto completo

Um tokenizer de produção não é um algoritmo, é um pipeline de cinco etapas, cada uma resolvendo um problema diferente.

> O sistema de produção não é um único algoritmo. É uma linha de tubos de cinco fases, cada fase resolve um problema diferente.

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

Cada etapa tem um trabalho específico:

> Cada fase tem responsabilidades específicas:

| Stage | What It Does | Why It Matters |
|-------|-------------|----------------|
| Normalize | NFKC Unicode, lowercase optional, strip accents optional | "fi" ligature (U+FB01) becomes "fi" (two chars). Without this, same word gets different tokens. |
| Pre-Tokenize | Split text into chunks before BPE | Prevents BPE from merging across word boundaries. "the cat" should never produce a token "e c". |
| BPE Merge | Apply learned merge rules to byte sequences | The core compression. Turns raw bytes into subword tokens. |
| Special Tokens | Inject [BOS], [EOS], [PAD], chat template markers | These tokens have fixed IDs. They never participate in BPE merges. The model needs them for structure. |
| ID Mapping | Convert token strings to integer IDs | The model sees integers, not strings. |

### BPE de nível byte

O tokenizer da lição 01 operava em bytes UTF-8. Essa foi a chamada certa. Mas ignoramos algo importante: o que acontece quando esses bytes não são válidos UTF-8?

> Primeiro, o separador de palavras opera em UTF-8 字节. Esta é a escolha correta. Mas nós ignoramos algumas coisas importantes: o que acontece quando esses caracteres não são válidos no UTF-8?

O BPE de nível de byte resolve isso tratando todos os valores de byte possíveis (0-255) como um token válido. Seu vocabulário base é exatamente 256 entradas. Qualquer arquivo - texto, binário, corrupto - pode ser tokenizado sem produzir um token desconhecido.

> 字节级 BPE 通过将每个可能的字节值(0-255)视为有效代币来解决这个问题――你的基础词表恰好 256条条点―― Qualquer documento 文本、二进制、损坏的都可以被分词而不会产生未知代币──

O GPT-2 adicionou um truque: mapear cada byte para um caracter Unicode impressível para que o vocabulário permaneça legível pelo ser humano.

> GPT-2 adicionou um flower trick: transformar cada字节 em um caracteres Unicode impressíveis, fazendo o word表 manter-se leível.

O poder real: o BPE de nível de byte lida com todas as línguas da Terra. Os caracteres chineses são 3 bytes UTF-8 cada. O japonês pode ser 3-4 bytes. Árabe, Devanagari, emoji - tudo apenas sequências de byte. O algoritmo BPE encontra padrões nessas sequências de byte exatamente da mesma forma que encontra padrões em bytes ASCII em inglês.

> A verdadeira força: BPE 字节级 处理地球上的每种语言──中文字符每个占占 3 个 UTF-8 字节──日文占 3-4 字节──阿拉伯文、天城文、emoji都只是字节序列── BPE 算法在这些字节序列中寻找模式的方式与英文 ASCII 字节中完全相同──

> **【中文解读】**O GPT-2 também fez um "花招" para mapear cada字节 em um caracteres Unicode impressíveis, para que o texto seja mais fácil de ler.

### Pre-tokenization

Antes de o BPE tocar no seu texto, você precisa dividir em pedaços. Isso impede que o algoritmo de fusão crie tokens que abrangam os limites das palavras.

> Antes de processar seu texto, você precisa separá-lo em blocos. Isso impede que o algoritmo de combinação criem símbolos transversais.

O GPT-2 usa um padrão regex para dividir o texto:

> GPT-2 Utilizando expressão formal para desmantelar texto:

```
'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+
```

Este padrão se divide em contrações ("don't" se torna "don" + "'t"), palavras com espaços de liderança opcionais, números, pontuação e espaço em branco. O espaço de liderança é mantido ligado à palavra - então "o gato" se torna ["o", "gato"], não ["o", " ", "gato"").

> Esse modelo é um modelo de "do" e "do" e "t" que se transformam em "don" e "t") e não em "the", "cat" e "the", "cat" e não em "the", "cat" e "cat".

Llama usa SentencePiece, que evita regex inteiramente. trata o fluxo de byte bruto como uma sequência longa e permite que o algoritmo BPE descubra os limites. Isso é mais simples, mas dá ao BPE mais liberdade para criar tokens de palavras cruzadas.

> Llama usando SentencePiece, completamente saltando sobre a expressão de texto. Ele será originário de um long sequência, deixando o algoritmo BPE determinar a sua própria fronteira.

A escolha é importante. o regex do GPT-2 impede que o tokenizador aprenda que "o" no final de uma palavra e "o" no início da próxima devem se fundir. a SentencePiece permite isso, o que às vezes produz compressão mais eficiente mas tokens menos interpretáveis.

> Esta escolha é importante. O GPT-2 tem um código de prevenção para que os componentes de um termo não sejam "comprimidos" e "comprimidos" em "comprimidos".

### Tokens especiais

Cada tokenizer de produção reserva identidades de tokens para marcadores estruturais:

> Cada produção de classes de palavras são marcadas para a estrutura e reservam o ID do token:

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

Os tokens especiais nunca são divididos pelo BPE. Eles são combinados exatamente antes do algoritmo de fusão ser executado, substituídos por seu ID fixo, e o texto circundante é tokenizado normalmente.

> Tokens especiais nunca serão separados por BPE. Eles são precisamente combinados antes da implementação do algoritmo de combinação, substituídos por ID fixo, em torno do texto normal分词.

> **【中文解读】**O símbolo especial é o símbolo de reserva de "intoxicável" em palavras:`[BOS]`(序列开始)`[EOS]`(序列結束)`[PAD]`(批次填充) 聊天模板标记等──它们有固定的ID,永远不参与BPE 合并,而在合并之前通过精确匹配被提取出来──Llama 3 使用 `<|start_header_id|>`- Não.`<|end_header_id|>`- Não.`<|eot_id|>`Para marcar a estrutura de diálogo,ChatGPT `<|im_start|>`和 `<|im_end|>`- Não.

> **【拓展：聊天模板的工程陷阱】**O chatting模板 é o lugar mais fácil de sair de erro na implementação real. Cada modelo usa um token especial de formato específico durante o treinamento, qualquer diferença, qualquer falta de troca, mais um espaço, qualquer erro de ordem, tudo o que permite que a entrada seja distribuída, levando ao modelo a sair de lixo.`chat_template`O mecanismo de Jinja2 é para padronizar este processo.

> ️ **【易错点】**实现特殊 token 的三个陷:(1) **特殊 token 内含正则元字符**如 `<|im_start|>`Em meio`|`, tem de ser usado .`re.escape()`转义,否则在 GPT-2 预分词的正则上会被解析成选择符;(2) **未从 BPE 词表中排除特殊 token**若 `<|im_end|>`Não em divisão, a sequência de caracteres é dividida em 8 tokens, o modelo nunca está em plena estrutura;**`add_special_tokens=False` 漏配**调用 `tokenizer.encode(text)`默认会自动加 BOS/EOS,做拼接时会出现 BOS BOS EOS EOS 序列,破坏注意力面具对齐──修复:编码时显式传 `add_special_tokens=False`, por fim, por um lado,

### Modelos de chat

É aqui que a maioria das pessoas fica confusa e a maioria das implementações quebra.

> É onde a maioria das pessoas está confusa, e também onde a maioria realiza erros.

Quando você envia mensagens para um modelo de chat, a API aceita uma lista de mensagens:

> Quando você enviar mensagens para o chat, a API aceita uma lista de mensagens:

```
[
  {"role": "system", "content": "You are helpful."},
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi there!"}
]
```

O modelo não vê JSON. Ele vê uma sequência de tokens plana. O modelo de bate-papo converte mensagens nessa sequência plana usando tokens especiais. Cada modelo faz isso de forma diferente:

> 模型看不到 JSON──它看到的是一个平的代币序列──聊天模板使用特殊代币将消息转换为平序列── cada modelo tem diferentes práticas:

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

Se o modelo for errado, o modelo produz lixo. Foi treinado num formato exato. Qualquer desvio - uma nova linha faltante, um token trocado, um espaço extra - coloca a entrada fora da distribuição de treinamento.

> O modelo está sendo treinado de forma precisa. Qualquer diferença, qualquer falta de troca, qualquer troca de tokens, qualquer espaço, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, qualquer tipo de troca, de troca, de troca, de troca, de troca, de troca, de troca, de troca, de troca, de troca, de troca, de troca, de troca de troca, de troca de troca, de troca de troca, de troca de troca de troca de troca, de troca de troca de troca, de troca de troca de troca de troca de troca.

> 🤔 **【困惑】**P: Llama 3 por que abandonar SentencePiece 改用TikToken?字节级 BPE比原版强在哪? A: 两点关键优势:(1) **SentencePiece 用 ⊗（U+2581）代替空格**, para ASCII 字符和原始空格的混在聊天场下导致代币序列对快速微变过于敏感;tiktoken 直接保留前导空格,"hello"和"hello"是不同的代币,更稳定;**字节级 BPE 词表恰好 256 个基础 token**, teoricamente pode codificar qualquer sequência de caracteres (incluindo emoji、 private区字符), não depende de um idioma específico; SentencePiece 词表若未训练到某字符直接 (UNK) ⋅ Llama 3 词表从32K 扩至128K,多语言压缩比升升 ~2x, é uma decisão de engenharia para calcular o custo de compra单的工程决策──

### Velocidade

O Python é muito lento para tokenização de produção.

> Python 对于生产级分词太慢了──

Tiktoken (OpenAI) é escrito em Rust com ligamentos Python. HuggingFace tokenizers também é Rust. SentencePiece é C ++. Estes alcançam 10-100x velocidades em relação ao Python puro.

> tiktoken(OpenAI) usando Rust 编写并提供 Python 绑定──HuggingFace tokenizers 也是Rust──SentencePiece 是C++──这些比纯Python 快10-100倍──

Para perspectiva: tokenizar 15 trilhões de tokens para o pre-treinamento Llama 3 a 1 milhão de tokens por segundo (Python rápido) levaria 174 dias.

> Por exemplo: velocidade de 100 milhões de tokens por segundo (Quick Speed Python) é de Llama 3 预训分词 1500000000 tokens 需要174 天──以每秒1000000 tokens (Rust) 速度,只需要1.7 天──

Você está construindo em Python para entender o algoritmo. Na produção, você usaria uma implementação compilada e tocaria apenas no envolvente Python.

> Você usa Python para construir para entender algoritmos. Em produção, você usa compilation implement, apenas contato com Python.

## Construí-lo e realizei-o.
```figure
weight-tying
```

## Construí-lo

### Passo 1: Encodificação de nível de byte

A base. Converte qualquer cadeia em uma sequência de bytes, mapeie cada byte para um caráter impressavel para exibição e inverta o processo.

> Base: 将任何字符串转换为字节序列,将每个字节映射到可印字符用于显示,并反转该过程

```python
def bytes_to_tokens(text):
    return list(text.encode("utf-8"))

def tokens_to_text(token_bytes):
    return bytes(token_bytes).decode("utf-8", errors="replace")
```

Teste em texto multilingue para ver o número de bytes:

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

"Hello" é de 5 bytes. "你好" é de 6 bytes (3 por caracter). O emoji de fogo é de 4 bytes. O tokenizer de nível de byte não se importa qual é a linguagem.

> "olá" é 5 字节──"你好" é 6 字节──cada字符 3 字节)──火焰 emoji é 4 字节──字节级分词器不关心它是什么语言──字节就是字节──

### Passo 2: Pre- Tokenizer com Regex

Divida o texto em pedaços usando o padrão GPT-2 regex. Cada pedaço é tokenizado de forma independente pelo BPE.

> Utilize GPT-2 正则模式将文本分成块──每个块由 BPE 独立分词──

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

O `regex`Modulo suporta escapes de propriedade Unicode (`\p{L}`para cartas, `\p{N}`Para números).`re`O módulo não, então nós voltamos para classes de caracteres ASCII. Para a produção de tokenizers multilíngues, instalar `regex`- Não .

> `regex`模块支持 Unicode 属性转义(`\p{L}`Expressão`\p{N}`Indicar números) 』 标准库`re`模块不支持,所以我们回归 ASCII 字符类──对于生产级多语言分词器,请安装 `regex`- Não.

Tenta:

```python
print(pre_tokenize("Hello, world! Don't stop."))
# [' Hello', ',', ' world', '!', " Don", "'t", ' stop', '.']
```

O espaço principal permanece ligado à palavra. As contrações se dividem no apóstrofo. A pontuação se torna sua própria peça.

> Antes de começar, a linha de referência é a linha de referência de um bloco separado.

### Passo 3: BPE em sequências de byte

O algoritmo central da lição 01, mas agora opera em pedaços pré-tokenizados de forma independente.

> Algoritmos centrais da primeira classe, mas agora operam independentemente dos blocos de pré-discussão.

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

### Passo 4: Manuseio de Tokens Especiais

Os tokens especiais precisam de identificação fixa e correspondência exacta.

> Tokens especiais precisam de identificação e identificação fixa.

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

### Passo 5: Classe de Tokenizer Completo

Encaixar tudo juntos: normalizar, dividir em tokens especiais, pre-tokenize, BPE fundir, mapa para IDs.

> 将所有步骤串联:归一化,按特殊代号 分割,预分词, BPE 合并,映射到ID,

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

### Passo 6: Teste de Multilinguagem

O teste real é jogar inglês, chinês, emoji e código.

> O teste real foi dado.

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

Os caracteres chineses produzem 3 bytes cada. O emoji produz 4 bytes. Nenhum deles acerta o tokenizer. Nenhum produz tokens desconhecidos. Isso é o poder do BPE de nível de byte.

> 中文字符每个产生 3 字节──emoji 产生 4 字节──这些都不会使分词器崩──都不会产生未知代币──这是字节级 BPE 的力量──

> **【中文解读】**O código acima vai ligar todos os componentes:归一化 → 特殊代币 分割 → 预分词 → BPE 合并 → ID 映射――测试覆盖英文,中文,emoji、代码和特殊代币的混合场景――字节级 BPE Garantizar que qualquer entrada não produzirá um token desconhecido é por isso que se tornou o padrão fundamental da indústria――

> **【拓展：分词速度的工程意义】**Pure Python 分词器每秒处理约1M tokens,Llama 3预训语料有15亿亿 tokens,使用Python 需要174 天――tiktoken(Rust 实现) per秒100M tokens,只需要1.7 天――这就是为什么生产级分词器都用编译语言:tiktoken 用Rust,HuggingFace tokenizers 用Rust,SentencePiece 用C++──

## Use-o com o framework implementado.

### Comparar Tokenizers reais

Carregue os tokenizadores reais de Llama 3, GPT-4 e Mistral. Veja como cada um lida com o mesmo parágrafo multilingue.

> 加载 Llama 3、GPT-4 和 Mistral 的实际分词器──看看每个分词器如何处理同一段多语言文本──

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

Você verá diferentes contagens de tokens para o mesmo texto. Llama 3 com vocabulário 128K é mais agressivo em fundir padrões comuns. GPT-4 com 100K fica no meio. Mistral com 32K produz mais tokens, mas tem uma camada de inserção menor.

> Você verá diferentes tokens do mesmo texto. Número de tokens. Llama 3 de 128K 词表在合并常见模式上更积极. GPT-4 de 100K está no meio. Mistral de 32K 产生更多的代币,但嵌层更小.

A compensação é sempre a mesma: um vocabulário maior significa sequências mais curtas mas mais parâmetros.

> 权衡始终相同: maior vocabulário significa menor sequência mas mais parâmetros。

## Envia-o . Produto .

Esta lição produz um prompt para a construção e depuração de tokenizadores de produção.`outputs/prompt-tokenizer-builder.md`- Não .

> Este curso foi desenvolvido para a construção e a regulação de máquinas de produção.`outputs/prompt-tokenizer-builder.md`- Não.

## Exercícios.

1. **Easy:**Adicionar um`get_token_bytes(id)`método que mostra os bytes brutos para qualquer ID de token. Use-o para inspecionar o que seus tokens mais comuns combinados realmente representam.
   Tradução: 添加`get_token_bytes(id)`方法,显示任意 token ID 的原始字节──用它检查您最常用的合并代币──实际代表什么──
2. **Medium:**Implementar o pre-tokenizer de estilo Llama que se divide em espaços brancos e dígitos, mas mantém espaços de liderança. Compare seu vocabulário com a abordagem GPT-2 regex no mesmo corpus.
   Tradução do inglês para tradução do inglês: implementar Llama 风格的预分词器,按空格和数字分分但保留前导空格──在相同语料上比较其词表与GPT-2 正则方法──
3. **Hard:**Adicionar um método de modelo de chat que leva uma lista de `{"role": ..., "content": ...}`A sequência de tokens é correta para o formato de chat Llama 3.
   Tradução do inglês: 添加聊天模板方法,接受 `{"role": ..., "content": ...}`消息列表并生成 Llama 3 聊天格式的正确代币序列──对照 HuggingFace 实现进行测试──

## Termos-chave .

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

## Mais leitura 延伸阅读

- [OpenAI tiktoken source](https://github.com/openai/tiktoken)-- Implementação de BPE de resistência utilizada pelo GPT-3.5/4
- [HuggingFace tokenizers](https://github.com/huggingface/tokenizers)-- Rust tokenizer biblioteca que suporta BPE, WordPiece, Unigram
- [Llama 3 paper (Meta, 2024)](https://arxiv.org/abs/2407.21783)-- detalhes sobre o vocabulário de 128K e a formação de tokenizadores
- [SentencePiece (Kudo & Richardson, 2018)](https://arxiv.org/abs/1808.06226)-- Tokenization linguística-agnóstica
- [GPT-2 tokenizer source](https://github.com/openai/gpt-2/blob/master/src/encoder.py)-- o mapeamento original de byte para Unicode
