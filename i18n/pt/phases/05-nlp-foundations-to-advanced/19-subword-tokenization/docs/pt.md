# Tokenization de subpalavras  BPE, WordPiece, Unigram, SentencePiece  子词分词  BPE、WordPiece、SentencePiece

> Os tokenizadores de palavras sufocam-se em palavras invisíveis, os tokenizadores de caracteres aumentam o comprimento da sequência, os tokenizadores de subpalavras dividem a diferença, cada Mestrado moderno é um.
> 词级分词器在未见词上卡住──字符分词器爆炸序列长度──子词分词器取中值──每个现代 LLM 都用子词分词──

> **【中文解读】**BPE é GPT usado de分词算法, WordPiece é BERT usado de

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 5 · 04 (GloVe / FastText / Subword) | **前置知识:** Phase 5 · 01（文本处理），Phase 5 · 04（GloVe / FastText / 子词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## O problema é o problema da introdução

O seu vocabulário tem 50.000 palavras. Um usuário digita "inconizable". O seu tokenizer retorna.`[UNK]`O modelo agora não tem sinal sobre a palavra. O pior: o documento de 90 percentual no seu corpus tem 40 palavras raras, o que significa 40 bits de informação perdida por documento.

> Seu vocabulário tem 50.000 palavras. Usuário inserir "intokenizable"`[UNK]`◊ Modelo agora para esta palavra não há sinal.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

A tokenização de subpalavras resolve isso. Palavras comuns permanecem tokens únicos. Palavras raras se descomponem em peças significativas:`untokenizable`→ `un`- Não .`token`- Não .`izable`Os dados de treinamento cobrem tudo porque qualquer cadeia é, em última análise, uma sequência de bytes.

> 子词分词 resolver este problema.`untokenizable`→ `un`- Não.`token`- Não.`izable`❖ O treinamento data cobre tudo, porque qualquer string final são sequências de bits.

Cada LLM de fronteira em 2026 é enviado em um dos três algoritmos (BPE, Unigram, WordPiece), envolto em uma das três bibliotecas (tiktoken, SentencePiece, HF Tokenizers).

> Cada LLM de 2026 anos em frente é baseado em três tipos de algoritmos (BPE, Unigram, WordPiece), embalado em três tipos de tokens (SentencePiece, HF Tokenizers).

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

![BPE vs Unigram vs WordPiece, character-by-character](../assets/subword-tokenization.svg)

**BPE (Byte-Pair Encoding).**Comece com um vocabulário de nível de caracteres. Conte cada par adjacente. Combine o par mais frequente em um novo token. Repita até atingir o tamanho do vocabulário alvo. Algoritmo dominante: GPT-2/3/4, Llama, Gemma, Qwen2, Mistral.

> **BPE（字节对编码）。**Desde o nível de caracteres para o tamanho do símbolo, o número de caracteres para cada um dos parentes é de um tamanho de um tamanho de um símbolo.

**Byte-level BPE.**O mesmo algoritmo, mas com bytes brutos (256 tokens base) em vez de caracteres Unicode.`[UNK]`Tokens  qualquer código de sequência de byte. GPT-2 usa 50.257 tokens (256 bytes + 50.000 fusões + 1 especial).

> **字节级 BPE。**É o mesmo algoritmo mas em original 字节 (→ 256 个基础 token) e não Unicode 字符上──保证零 `[UNK]`Token  任何字节序列都可编码──GPT-2 使用 50,257 个 token──

**Unigram.**Comece com um vocabulário enorme. atribuir a cada token uma probabilidade de unigrama. Iterativamente poda tokens cuja remoção aumenta o mínimo a probabilidade de registro do corpus. Provavelmente na inferência: pode amostrar tokenizations. Usado por T5, mBART, ALBERT, XLNet, Gemma.

> **Unigram。**Desde o enorme discurso começou. A cada token distribuído o unigrama  probabilidade.

**WordPiece.**Combinar pares que maximizam a probabilidade do corpo de treinamento em vez de freqüência bruta.

> **WordPiece。**合并使训练语料似然最大化而非原始频率最高对── para uso em BERT、DistilBERT、ELECTRA──

**SentencePiece vs tiktoken.**SentencePiece é a biblioteca que *treina* vocabulários (BPE ou Unigram) diretamente em texto Unicode bruto, codificando o espaço branco como `▁`. tiktoken é o codificador rápido da OpenAI contra vocabulários pré-construídos; não treina.

> **SentencePiece vs tiktoken。**SentencePiece é em original Unicode 文本上*训练*词表的库,将空格编码为 `▁` tiktoken é um código aberto para o desenvolvimento de palavras-chave; não é treinado.

Regra geral:

> 经验法则:

- **Training a new vocabulary:**SentencePiece (multilíngue, sem pre-tokenization) ou HF Tokenizers.
  **训练新词表：**SentencePiece(多语言,无预分词) 或 HF Tokenizers──
- **Fast inference against GPT vocab:**Tiktoken (cl100k_base, o200k_base).
  **针对 GPT 词表的快速推理：**- O que é isso?
- **Both:**HF Tokenizers  uma biblioteca, formação + serviço.
  **两者兼有：**HF Tokenizers  一个库,训练 + 服务。

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
bpe-merge
```

## Construí-lo

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

### Passo 1: BPE a partir do zero

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

A ordem de fusão é importante. BPE aplica fusões em ordem de treinamento, de modo que fusões anteriores criam tokens mais longos que bloqueiam os posteriores.

> 合并顺序很重要──BPE 按训练顺序应用合并,所以较早的合并创建更长的代币,阻止后续合并──这就是为什么BPE 词表不能跨模型移植──

### Passo 2: Tokenization com tiktoken e SentencePiece

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

### Passo 3: Comparação de fertilidade

```python
def fertility(text, tokenizer_fn):
    return len(tokenizer_fn(text))

# BPE on English: ~1.3 tokens/word
# BPE on Hindi: ~3.5 tokens/word
# BPE on Amharic: ~8 tokens/word
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

Escolha por ecossistema.

> 按生态系统选择──

- **OpenAI models (GPT-4, GPT-4o):**Tiktoken. Rapida e exata reprodução da tokenization do OpenAI. / tiktoken──快速──精确复现 OpenAI 分词──
- **Multilingual / custom training:**SentencePiece. Trens de texto bruto, lida com qualquer script. / SentencePiece。 de original文本训练,处理任何书写系统。
- **Hugging Face models:**AutoTokenizer. Enrola o backend direito automaticamente. / AutoTokenizer.
- **Maximum speed at inference:**HF Tokenizers (Rust backend) ou tiktoken (Python + C). / 推理最高速度:HF Tokenizers 或 tiktoken。

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

## Envia-o . Produto .

Salva como`outputs/prompt-tokenizer-picker.md`- Não .

> 保存为 `outputs/prompt-tokenizer-picker.md`- Não .

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

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Exercícios.

1. **Easy.**Treinar BPE em um pequeno corpus (1000 palavras). Encoderar e decodificar 20 palavras de teste. Verificar a fidelidade de ida e volta. / **简单。**Em pequeno idioma, treinar BPE.
2. **Medium.**Compare a fertilidade de tokenization para inglês, chinês e hindi usando cl100k_base do tiktoken.**中等。**Utilize tiktoken comparar Inglês, Chinês e índice de taxa de reprodução de palavras.
3. **Hard.**Treinar um modelo SentencePiece Unigram em um corpo misturado de Inglês e Hindi. Comparar a fertilidade com um modelo BPE treinado com os mesmos dados. / **困难。**Em um mix Inglês-Indian linguagem linguística treinamento SentencePiece Unigram 模型── comparado com BPE 模型 em um mesmo dados treinamento 模型 comparar taxa de reprodução──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Termos-chave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| BPE（字节对编码） | GPT's tokenizer / GPT 的分词器 | Iteratively merge most frequent adjacent pairs. / 迭代合并最频繁的相邻对。 |
| Unigram | T5's tokenizer / T5 的分词器 | Prune tokens from large vocabulary by likelihood. / 按似然从大词表剪枝。 |
| WordPiece | BERT's tokenizer / BERT 的分词器 | Merge pairs that maximize corpus likelihood. / 合并使语料似然最大化的对。 |
| SentencePiece | Training library / 训练库 | Train BPE or Unigram on raw text. Encodes whitespace as `▁`. / 在原始文本上训练 BPE 或 Unigram。 |
| tiktoken | OpenAI's encoder / OpenAI 编码器 | Fast encoding against pre-built GPT vocabularies. / 针对预构建 GPT 词表的快速编码。 |
| Fertility（繁殖率） | Tokens per word / 每词 token 数 | How many subword tokens a word produces. Lower is better. / 一个词产生多少子词 token。越低越好。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.

## Mais leitura 延伸阅读

- [Sennrich et al. (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909)O artigo BPE.
- [Kudo (2018). Subword Regularization](https://arxiv.org/abs/1804.10959)O artigo Unigram.
- [SentencePiece documentation](https://github.com/google/sentencepiece) formação e serviço. / 訓練和服務。
- [tiktoken](https://github.com/openai/tiktoken) O tokenizador rápido do OpenAI. / OpenAI 快速分词器──
- [Hugging Face Tokenizers](https://huggingface.co/docs/tokenizers/) Formação apoiada em corrosão + serviço. / Rust 后端训练 + 服务。
