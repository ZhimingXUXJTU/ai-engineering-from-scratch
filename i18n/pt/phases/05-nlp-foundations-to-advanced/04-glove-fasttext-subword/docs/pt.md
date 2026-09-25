# GloVe, FastText, e Subword Embeddings

> O Word2Vec treinou um incorporado por palavra. O GloVe factorizou a matriz de co-ocorrência. O FastText incorporou as peças. O BPE puenteou para transformadores.
> Word2Vec 为每个词训练一个嵌入──GloVe 分解共现矩阵──FastText 嵌入词的组成部分──BPE 桥接到变压器──

> **【中文解读】**GloVe Utilizando a totalidade da população,FastText 处理子词解决 OOV 问题──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word2Vec from Scratch) | **前置知识:** Phase 5 · 03（Word2Vec 从零实现）
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

A Word2Vec deixou duas perguntas abertas.

> O Word2Vec deixou dois problemas abertos.

Primeiro, havia uma linha paralela de pesquisa que factualizou a matriz de co-ocorrência diretamente (LSA, HAL) em vez de fazer atualizações de skip-gram online. A abordagem iterativa do Word2Vec era fundamentalmente melhor, ou a diferença era um artefato de como os dois métodos são manuseados conta? **GloVe**A resposta foi: factorization de matriz com uma perda cuidadosamente escolhida, que corresponde ou supera o Word2Vec, e custa menos treinar.

> Primeiro, existe uma linha de estudo em linha, que consiste em descomplicar diretamente a matrizes existentes (LSA, HAL), em vez de fazer um esquema de transmissão em linha.**GloVe**回答:配合精心选择的损失函数矩阵分解匹配或超过 Word2Vec,且训练成本较低――

Em segundo lugar, nenhum dos métodos tinha uma história para palavras que nunca tinha visto.`Zoomer-approved`- Não .`dogecoin`, qualquer substantivo próprio cunhado na semana passada, cada forma inflexível de uma raiz rara.**FastText**Fixou isto incorporando caracteres n-gramas: uma palavra é a soma de suas partes, incluindo morfemas, então mesmo palavras fora do vocabulário obtêm um vetor sensível.

> Segundo, duas formas de resolver as questões que nunca foram abordadas.`Zoomer-approved`- Não.`dogecoin`、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 **FastText**通过嵌字符n-gram 修复了这个问题:一个词是其各部分之和,包括语素,因此, mesmo em termos de expressão, palavras fora também podem obter um volume razoável.

Em terceiro lugar, quando chegaram os transformadores, a questão mudou novamente.**Byte-pair encoding (BPE)**E os seus parentes resolveram isto aprendendo um vocabulário de unidades freqüentes de subpalavras que abrange tudo.

> Terceiro, quando o Transformador chegou, o problema mudou novamente.**字节对编码（Byte-Pair Encoding, BPE）** e seus variações através do aprendizado de tudo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

Esta lição vai caminhar para os três, e depois explica qual alcançar para quando.

> Esta aula fala sobre estes três, e depois explica quando usar qual.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

**GloVe (Global Vectors).**Construir a matriz de co-ocorrência palavra-palavra `X`onde`X[i][j]`É a frequência da palavra.`j`aparece no contexto da palavra `i`- Vêctores de trem tais que`v_i · v_j + b_i + b_j ≈ log(X[i][j])`O peso é tão baixo que os pares não dominam.

> **GloVe（全局向量）。**构建词-词共现矩阵 `X`, entre os `X[i][j]`É um termo`j`Aparecer em palavras`i`上下文中的频率── 訓練向量使 `v_i · v_j + b_i + b_j ≈ log(X[i][j])`                                                                                                                                                                                                                                                              

**FastText.**Uma palavra é a soma de seus caracteres n-gramas mais a própria palavra. `where`torna-se`<wh, whe, her, ere, re>, <where>`O vector de palavra é a soma dos vectores componentes.`whereupon`) são compostas por n-gramas conhecidos.

> **FastText。**Um termo é o seu caracter n-gram 之和加上词本身──`where`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `<wh, whe, her, ere, re>, <where>`△词向量是这些组件向量的和──像 Word2Vec 一样训练──好处:未见过的词(`whereupon`) de um conhecido n-grama 组合而成

**BPE (Byte-Pair Encoding).**Comece com um vocabulário de bytes individuais (ou caracteres). Conte cada par adjacente no corpus. Combine o par mais frequente em um novo token. Repita para `k`O resultado: um vocabulário de `k + 256`Tokens em que seqüências frequentes (`ing`- Não .`tion`- Não .`the`As palavras raras são divididas em pedaços familiares.

> **BPE（字节对编码）。**A frequência de surgimento de cada um dos seus vizinhos no linguagem da estatística será a mais frequente para a combinação de novos tokens.`k`O resultado: um.`k + 256`个 token 的词表, em que高频序列(`ing`- Não.`tion`- Não.`the`) é um único símbolo, raras palavras são divididas em fragmentos familiares.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
n5-subword-merge
```

## Construí-lo

### GloVe: factorizar a matriz de co-ocorrência

```python
import numpy as np
from collections import Counter


def build_cooccurrence(docs, window=5):
    pair_counts = Counter()
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    for doc in docs:
        indexed = [vocab[t] for t in doc]
        for i, center in enumerate(indexed):
            for j in range(max(0, i - window), min(len(indexed), i + window + 1)):
                if i != j:
                    distance = abs(i - j)
                    pair_counts[(center, indexed[j])] += 1.0 / distance
    return vocab, pair_counts


def glove_train(vocab, pair_counts, dim=16, epochs=100, lr=0.05, x_max=100, alpha=0.75, seed=0):
    n = len(vocab)
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(n, dim))
    W_tilde = rng.normal(0, 0.1, size=(n, dim))
    b = np.zeros(n)
    b_tilde = np.zeros(n)

    for epoch in range(epochs):
        for (i, j), x_ij in pair_counts.items():
            weight = (x_ij / x_max) ** alpha if x_ij < x_max else 1.0
            diff = W[i] @ W_tilde[j] + b[i] + b_tilde[j] - np.log(x_ij)
            coef = weight * diff

            grad_W_i = coef * W_tilde[j]
            grad_W_tilde_j = coef * W[i]
            W[i] -= lr * grad_W_i
            W_tilde[j] -= lr * grad_W_tilde_j
            b[i] -= lr * coef
            b_tilde[j] -= lr * coef

    return W + W_tilde
```

Duas peças móveis que valham a pena nomear.`f(x) = (x/x_max)^alpha`- de peso inferior em pares muito frequentes (como `(the, and)`O valor final da integração é a soma de`W`(centro) e `W_tilde`(contexto) tabelas. Somando ambas é um truque publicado que tende a superar usando apenas um.

> 两个值得指出的要点──加权函数 `f(x) = (x/x_max)^alpha`降低非常频繁的对(如 `(the, and)`O peso do peso é o que o faz perder o peso.`W`(Centro词) 和 `W_tilde`(上下文词)表之和──对两者求和是一个已发表的技巧,通常优于只使用其中一个──

### FastText: embutidos conscientes de subpalavras

```python
def char_ngrams(word, n_min=3, n_max=6):
    wrapped = f"<{word}>"
    grams = {wrapped}
    for n in range(n_min, n_max + 1):
        for i in range(len(wrapped) - n + 1):
            grams.add(wrapped[i:i + n])
    return grams
```

```python
>>> char_ngrams("where")
{'<where>', '<wh', 'whe', 'her', 'ere', 're>', '<whe', 'wher', 'here', 'ere>', '<wher', 'where', 'here>'}
```

Cada palavra é representada por seu conjunto de n-gramas (normalmente de 3 a 6 caracteres).

> Cada palavra é inserida em um n-gram 集合 (normalmente 3 a 6 caracteres) e é inserida em um n-gram 嵌入之和.

```python
def fasttext_vector(word, ngram_table):
    grams = char_ngrams(word)
    vecs = [ngram_table[g] for g in grams if g in ngram_table]
    if not vecs:
        return None
    return np.sum(vecs, axis=0)
```

Para uma palavra invisível, você ainda obtém um vetor desde que alguns de seus n-gramas são conhecidos. `whereupon`Ações `<wh`- Não .`her`- Não .`ere`, e `<where`com`where`, então os dois aterrissam perto um do outro.

> Para palavras não vistas, desde que sua parte n-grama é conhecida, você ainda pode obter um volume.`whereupon`Com`where`Compartilhamento`<wh`- Não.`her`- Não.`ere`和 `<where`Então, os dois estão em posição próxima.

### BPE: vocabulário de subpalavras aprendido

```python
def learn_bpe(corpus, k_merges):
    vocab = Counter()
    for word, freq in corpus.items():
        tokens = tuple(word) + ("</w>",)
        vocab[tokens] = freq

    merges = []
    for _ in range(k_merges):
        pair_freq = Counter()
        for tokens, freq in vocab.items():
            for a, b in zip(tokens, tokens[1:]):
                pair_freq[(a, b)] += freq
        if not pair_freq:
            break
        best = pair_freq.most_common(1)[0][0]
        merges.append(best)

        new_vocab = Counter()
        for tokens, freq in vocab.items():
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i + 1 < len(tokens) and (tokens[i], tokens[i + 1]) == best:
                    new_tokens.append(tokens[i] + tokens[i + 1])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            new_vocab[tuple(new_tokens)] = freq
        vocab = new_vocab
    return merges


def apply_bpe(word, merges):
    tokens = list(word) + ["</w>"]
    for a, b in merges:
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i + 1 < len(tokens) and tokens[i] == a and tokens[i + 1] == b:
                new_tokens.append(a + b)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens
    return tokens
```

```python
>>> corpus = Counter({"low": 5, "lower": 2, "newest": 6, "widest": 3})
>>> merges = learn_bpe(corpus, k_merges=10)
>>> apply_bpe("lowest", merges)
['low', 'est</w>']
```

A primeira iteração mistura o par adjacente mais comum.`low`- Não .`est`- Não .`tion`O que é que se passa com o "comércio de produtos" e o "comércio de produtos" ?

> A primeira vez que se juntaram os mais comuns ao próximo.`low`- Não.`est`- Não.`tion`(Reflexão)

Os tokenizadores GPT / BERT / T5 reais aprendem fusões de 30k-100k. Resultado: qualquer texto tokeniza em uma sequência de comprimento limitado de IDs conhecidas, sem OOV nunca.

> GPT / BERT / T5 分词器学习 3 000 a 10 000 vezes合并── Resultados: qualquer texto é dividido em uma sequência de distinção de tamanho de ID conhecida, nunca haverá OOV──

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

Na prática, raramente treinas isto sozinho.

> Na prática, você praticamente não se treina.

```python
import fasttext.util
fasttext.util.download_model("en", if_exists="ignore")
ft = fasttext.load_model("cc.en.300.bin")
print(ft.get_word_vector("whereupon").shape)
print(ft.get_word_vector("zoomerapproved").shape)
```

Para a tokenização de subpalavras no estilo BPE na era dos transformadores:

> 对于 Transformer 时代的 BPE 风格子词分词:

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
print(tok.tokenize("unbelievably tokenized"))
```

```
['un', 'bel', 'iev', 'ably', 'Ġtoken', 'ized']
```

O `Ġ`O prefixo marca os limites das palavras (uma convenção GPT-2).

> `Ġ`Antes de começar, a primeira parte do livro foi escrita por um escritor, que escreveu o livro de um escritor, que escreveu o livro de um escritor, que escreveu o livro de um escritor, que escreveu o livro de um escritor, que escreveu o livro de um escritor, que escreveu o livro de um escritor, que escreveu o livro de um escritor, que escreveu o livro de um escritor, que escreveu o livro de um escritor, que escreveu o livro de um escritor, que escreveu o livro de um escritor, que foi publicado em 1928.

### Quando escolher qual

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Pretrained general-purpose word vectors, no OOV tolerance needed | GloVe 300d | 预训练通用词向量，不需要处理 OOV | GloVe 300 维 |
| Pretrained general-purpose word vectors, must handle misspellings / neologisms / morphologically rich languages | FastText | 预训练通用词向量，必须处理拼写错误 / 新词 / 形态丰富的语言 | FastText |
| Anything going into a transformer (training or inference) | Whatever tokenizer the model shipped with. Never swap. | 输入 Transformer 的任何场景（训练或推理） | 模型自带的分词器。永远不要替换。 |
| Training your own language model from scratch | Train a BPE or SentencePiece tokenizer on your corpus first | 从零训练自己的语言模型 | 先在你的语料上训练 BPE 或 SentencePiece 分词器 |
| Production text classification with a linear model | Still TF-IDF. Lesson 02. | 使用线性模型的生产文本分类 | 仍然用 TF-IDF。第 02 课。 |

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

## Envia-o . Produto .

Salva como`outputs/skill-embeddings-picker.md`- Não .

```markdown
---
name: tokenizer-picker
description: Pick a tokenization approach for a new language model or text pipeline.
version: 1.0.0
phase: 5
lesson: 04
tags: [nlp, tokenization, embeddings]
---

Given a task and dataset description, you output:

1. Tokenization strategy (word-level, BPE, WordPiece, SentencePiece, byte-level). One-sentence reason.
2. Vocabulary size target (e.g., 32k for an English-only LM, 64k-100k for multilingual).
3. Library call with the exact training command. Name the library. Quote the arguments.
4. One reproducibility pitfall. Tokenizer-model mismatch is the single most common silent production bug; call out which pair must be used together.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend training a custom tokenizer when the user is fine-tuning a pretrained LLM. Refuse to recommend word-level tokenization for any model targeting production inference. Flag non-English / multi-script corpora as needing SentencePiece with byte fallback.
```

## Exercícios.

1. **Easy.**Corra .`char_ngrams("playing")`E ...`char_ngrams("played")`- Calcule a sobreposição Jaccard dos dois conjuntos de n-gram.`pla`- Não .`lay`- Não .`play`), razão pela qual o FastText transfere bem entre as variantes morfológicas.
   **简单。**运行 `char_ngrams("playing")`和 `char_ngrams("played")`△ calcular dois n-gramas 集合的Jaccard 重叠度── você deve ver um grande número de partes compartilhadas`pla`- Não.`lay`- Não.`play`), esta é a razão pela qual o FastText é bem mudado entre os diferentes tipos de texto.
2. **Medium.**Extensão`learn_bpe`Para rastrear o crescimento do vocabulário. Plot tokens-per-corpus-caracter como função do número de fusões. Você deve ver compressão rápida no início, assimptando cerca de ~2-3 caras por token.
   **中等。**扩展 `learn_bpe`以跟踪词表增长──绘制每个语料字符的符号 数作为合并次数的函数── você deve ver quando começar a comprimir rapidamente, em cerca de 2-3 字符/符号 附近渐近──
3. **Hard.**Treinar um BPE de 1k de fusão sobre as obras completas de Shakespeare. Comparar a tokenização de palavras comuns com nomes próprios raros. Medir tokens médios por palavra antes e depois. Escrever o que surpreendeu.
   **困难。**Em Shakespeare, o total de treinos de 1 mil vezes combinado de BPE, comparado com palavras comuns e raras, foi de um total de milhares de palavras.

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Termos-chave .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Co-occurrence matrix | Word-word frequency table | `X[i][j]` = how often word `j` appears in a window around word `i`. | 共现矩阵 | 词-词频率表 | `X[i][j]` = 词 `j` 在词 `i` 周围窗口中出现的频率。 |
| Subword | Piece of a word | A character n-gram (FastText) or learned token (BPE/WordPiece/SentencePiece). | 子词 | 词的片段 | 字符 n-gram（FastText）或学习到的 token（BPE/WordPiece/SentencePiece）。 |
| BPE | Byte-pair encoding | Iterative merging of most-frequent adjacent pairs until vocabulary hits target size. | BPE（字节对编码） | 字节对编码 | 迭代合并最频繁的相邻对，直到词表达到目标大小。 |
| OOV | Out of vocabulary | Word the model has never seen. Word2Vec/GloVe fail. FastText and BPE handle it. | OOV（词表外） | 词表外 | 模型从未见过的词。Word2Vec/GloVe 会失败。FastText 和 BPE 能处理。 |
| Byte-level BPE | BPE on raw bytes | GPT-2's scheme. Vocabulary starts with 256 bytes, so nothing is ever OOV. | 字节级 BPE | 对原始字节的 BPE | GPT-2 的方案。词表从 256 个字节开始，所以永远不会有 OOV。 |

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Mais leitura 延伸阅读

- [Pennington, Socher, Manning (2014). GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf)O Glove paper, sete páginas, ainda é a melhor derivação da perda.
- [Bojanowski et al. (2017). Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606) FastText. / FastText 论文。
- [Sennrich, Haddow, Birch (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) o artigo que introduziu o BPE na PNL moderna. / 将 BPE 引入现代 NLP 的论文──
- [Hugging Face tokenizer summary](https://huggingface.co/docs/transformers/tokenizer_summary) como BPE, WordPiece e SentencePiece realmente diferem na prática.
