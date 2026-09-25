# Geração de texto antes dos transformadores  N-gram Language Models  Transformer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

> Se uma palavra é surpreendente, o modelo é ruim. A perplexidade torna surpresa um número.
> Se uma palavra é surpreendente, o modelo é ruim.

> **【中文解读】**N-gram 统计词频预测 下一个词──GPT 就是更强大的语言模型──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

Antes dos transformadores, antes dos RNNs, antes das incorporações de palavras, um modelo de linguagem previu a próxima palavra contando a frequência com que ela seguiu a anterior `n-1`Conte "o gato" → "sede" 47 vezes, "o gato" → "saltou" 12 vezes, "o gato" → "frigerador" 0 vezes. Normalize para obter uma distribuição de probabilidade.

> Antes do Transformer, antes do RNN, antes do Word Embedded, antes do Language Model                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `n-1`个词后面跟着当前词的频率来预测下一个词――统计 "o gato" → "sat" 出现 47 次, "o gato" → "jumped" 出现 12 次, "o gato" → "frigerador" 出现 0 次。归归化得到概率分布。

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

Este é um modelo de linguagem n-gram. Ele executou todos os reconhecedores de fala, todos os verificadores de ortografia e todos os sistemas de tradução automática baseados em frases de 1980 a 2015.

> É o modelo de linguagem n-gram. De 1980 a 2015, ele funcionou em cada identificador de voz, cada revisor de ortografia e em cada sistema de tradução automática baseado em palavras curtas. Quando você precisa de um dispositivo barato para construir linguagem, ele ainda funciona.

O problema interessante é o que fazer com n-gramas invisíveis. Um modelo baseado em contagem crua atribui probabilidade zero a qualquer coisa que não tenha visto, o que é catastrófico porque as frases são longas e quase todas as frases longas contêm pelo menos uma sequência invisível. Cinquenta anos de pesquisa de suavizagem fixaram isso.

> A questão interessante é: como lidar com o n-grama não visto. O modelo primitivo baseado em cálculo distribui zero probabilidades para qualquer coisa não vista, que é catastrófico, porque as frases são longas, quase todas as frases longas contêm pelo menos uma sequência não vista.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

![N-gram model: count, smooth, generate](../assets/ngram.svg)

### O jogo de previsão

Antes de qualquer uma dessas máquinas existir, um experimento definia o que é um modelo de linguagem. Cubra a próxima letra de uma frase inglesa. Peça a alguém para adivinhar, uma adivinha de cada vez, até que eles a consigam bem. Escreva a contagem de adivinhações. Repita por algumas centenas de letras.

As contagens de adivinhações não são triviais. São uma recodificação sem perda do texto: entregue a sequência de contagem a um segundo adivinhador idêntico e eles podem reconstruir cada letra, porque em cada posição eles sabem exatamente quais adivinhas são as primeiras. Uma mensagem que você pode recodificar em menos símbolos carrega menos informações por símbolo, então as estatísticas de contagem de adivinhações colocam um teto na entropia do inglês.

Shannon fez isto em 1951 e conseguiu um número que ainda governa o campo. Um alfabeto de 27 símbolos (26 letras mais espaço) poderia levar`log2(27) ≈ 4.75`Os adivinhadores humanos com 100 letras de contexto aterraram entre 0,6 e 1,3 bits por letra. Inglês é aproximadamente três quartos de movimentos forçados. A estrutura que um modelo deve aprender foi medida antes que qualquer modelo pudesse aprendê-lo.

Cada modelo de linguagem desde então é um jogador mecânico deste jogo, e cada número de avaliação nesta lição é o jogo marcado:

- **Cross-entropy loss**O treinamento de um LM é literalmente minimizar sua pontuação no jogo de adivinhação.
- **Perplexity**É o que é`2^bits`(ou `e^nats`O factor de ramificação ainda está diante do modelo após a sua conjectura.
- **Context length is the player's memory.**Um modelo de trigramas joga com dois tokens de memória. Um transformador joga o mesmo jogo com 100K tokens. As regras nunca mudaram; o jogador melhorou.

Uma unidade de rotação: as pontuações do jogo por letra em bits (`log2`), enquanto as fórmulas n-gram abaixo pontuação por palavra token em nats (log natural)  e desde perplexidade `e^H`em nats iguais `2^H`em bits, as duas visões são a mesma medida em unidades diferentes.

```figure
prediction-game
```

**N-gram probability:** `P(w_i | w_{i-n+1}, ..., w_{i-1})`- Corrigir .`n`(normalmente 3 para trigramas, 4 para 4 gramas).

> **N-gram 概率：** `P(w_i | w_{i-n+1}, ..., w_{i-1})`Fixação`n`(三元组通常为 3,四元组为 4) ⋅

```text
P(w | context) = count(context, w) / count(context)
```

**The zero-count problem.**Qualquer n-gram não visto no treinamento recebe probabilidade zero. Um estudo de 2007 sobre o corpus de Brown descobriu que mesmo um modelo de 4 gramas tinha 30% de 4 gramas não vistos no treinamento.

> **零计数问题。**Os n-grams que não foram vistos em qualquer treinamento obtiveram probabilidade zero. Em 2007, um estudo da Brown Language Library descobriu que, mesmo em quadruplo-compositivos, 30% dos quadruplo-compositivos não foram vistos em qualquer treinamento.

**Smoothing approaches, in order of sophistication:**

> **平滑方法，按复杂度排序：**

1. **Laplace (add-one).**Adicionar um a cada contagem.
   **拉普拉斯（加一）。**Para cada conta, adicione um.
2. **Good-Turing.**Realocar a massa de probabilidade de eventos de alta frequência para os invisíveis com base na frequência de frequências.
   **Good-Turing。**Baseado na frequência da frequência, a qualidade da probabilidade será redistribuída de eventos de alta frequência para eventos invisíveis.
3. **Interpolation.**Combinar n-gram, (n-1)-gram, etc., estimativas com pesos ajustáveis.
   **插值。**Usada para a avaliação de peso
4. **Backoff.**Se n-gram tem contado zero, cair de volta para (n-1)-gram.
   **回退。**Se n-gram 计数为零, retornará a (n-1)-gram。Katz retornará a sua regeneração。
5. **Absolute discounting.**Subtrair um desconto fixo `D`De todas as contas, redistribuir para o invisível.
   **绝对折扣。**De todas as contas deduzido o desconto fixo`D`, re-distribuição para eventos não vistos.
6. **Kneser-Ney.**Desconto absoluto mais uma escolha inteligente para o modelo de ordem inferior: usar * probabilidade de continuação* (quantos contextos uma palavra aparece) em vez de freqüência bruta.
   **Kneser-Ney。**绝对折扣加上低阶模型的巧妙选择:使用*续接概率*(一个词出现在多少上下文中) em vez de freqüência original。

A visão do Kneser-Ney é profunda. "San Francisco" é um bigrama comum. O unigrama "Francisco" aparece principalmente após "San". O desconto absoluto ingênuo dá a "Francisco" uma alta probabilidade de unigrama (porque a contagem é alta). A Kneser-Ney observa que o "Francisco" aparece apenas num contexto e reduz, em conformidade, a probabilidade de sua continuação. Resultado: um bigrama romântico terminando em "Francisco" obtém a probabilidade apropriada.

> Kneser-Ney's insight is very deep──"San Francisco" is a commonplace of the two-way group──一元组 "Francisco" 主要 appears in "San" 后──朴素绝对折扣给"Francisco" 高一元组概率(因为计数高)──Kneser-Ney nota que "Francisco" só aparece em um 上下文中,相应地降其续概率──结果:以"Francisco"结尾的新二元组获得适当的低概率──

**Evaluation: perplexity.**O exponente da probabilidade média negativa de registro por palavra em um conjunto de testes prolongados. Baixo é melhor. Uma perplexidade de 100 significa que o modelo é tão confuso quanto ele escolheria uniformemente entre 100 palavras.

> **评估：困惑度。**留出测试集上每字平均负对数似然的指数──越低越好──困惑度 100 significa que a confusão do modelo é equivalente à média de seleção entre 100 palavras──

```text
perplexity = exp(- (1/N) * Σ log P(w_i | context_i))
```

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
ngram-backoff
```

## Construí-lo

### Passo 1: contagem de trigramas

```python
from collections import Counter, defaultdict


def train_ngram(corpus_tokens, n=3):
    ngrams = Counter()
    contexts = Counter()
    for sentence in corpus_tokens:
        padded = ["<s>"] * (n - 1) + sentence + ["</s>"]
        for i in range(len(padded) - n + 1):
            ctx = tuple(padded[i:i + n - 1])
            word = padded[i + n - 1]
            ngrams[ctx + (word,)] += 1
            contexts[ctx] += 1
    return ngrams, contexts


def raw_probability(ngrams, contexts, context, word):
    ctx = tuple(context)
    if contexts.get(ctx, 0) == 0:
        return 0.0
    return ngrams.get(ctx + (word,), 0) / contexts[ctx]
```

A entrada é uma lista de frases tokenizadas. A saída é n-gram counts e contexts counts. `<s>`E ...`</s>`São limites de sentença.

> 输入是分词后的句子列表──输出是n-gram 计数和上下文计数──`<s>`和 `</s>`É a linha da fronteira.

### Passo 2: Limeamento de laplace

```python
def laplace_probability(ngrams, contexts, vocab_size, context, word):
    ctx = tuple(context)
    numerator = ngrams.get(ctx + (word,), 0) + 1
    denominator = contexts.get(ctx, 0) + vocab_size
    return numerator / denominator
```

Adiciona 1 a cada contagem, mas super-aloca massa para eventos invisíveis, prejudicando eventos raros também.

>  para cada contação adição 1― mas distribuição de qualidade em excesso  para eventos inéditos, também prejudica eventos conhecidos raros―

### Passo 3: Kneser-Ney (bigrama, interpolada)

```python
def kneser_ney_bigram_model(corpus_tokens, discount=0.75):
    unigrams = Counter()
    bigrams = Counter()
    unigram_contexts = defaultdict(set)

    for sentence in corpus_tokens:
        padded = ["<s>"] + sentence + ["</s>"]
        for i, w in enumerate(padded):
            unigrams[w] += 1
            if i > 0:
                prev = padded[i - 1]
                bigrams[(prev, w)] += 1
                unigram_contexts[w].add(prev)

    total_unique_bigrams = sum(len(ctx_set) for ctx_set in unigram_contexts.values())
    continuation_prob = {
        w: len(ctx_set) / total_unique_bigrams for w, ctx_set in unigram_contexts.items()
    }

    context_totals = Counter()
    for (prev, w), count in bigrams.items():
        context_totals[prev] += count

    unique_follow = defaultdict(set)
    for (prev, w) in bigrams:
        unique_follow[prev].add(w)

    def prob(prev, w):
        count = bigrams.get((prev, w), 0)
        denom = context_totals.get(prev, 0)
        if denom == 0:
            return continuation_prob.get(w, 1e-9)
        first_term = max(count - discount, 0) / denom
        lambda_prev = discount * len(unique_follow[prev]) / denom
        return first_term + lambda_prev * continuation_prob.get(w, 1e-9)

    return prob
```

Três partes móveis.`continuation_prob`"Quantos contextos diferentes esta palavra aparece?" (a inovação Kneser-Ney).`lambda_prev`A probabilidade final é o termo principal descontado mais o termo ponderado de continuação.

> Três partes do movimento.`continuation_prob`捕获 "这个词出现在多少不同上下文中?" ([[Kneser-Ney's创新]])`lambda_prev`A probabilidade final é a de um desconto principal, o que significa que o desconto é mais elevado.

### Passo 4: gerar texto com amostragem

```python
import random


def generate(prob_fn, vocab, prefix, max_len=30, seed=0):
    rng = random.Random(seed)
    tokens = list(prefix)
    for _ in range(max_len):
        candidates = [(w, prob_fn(tokens[-1], w)) for w in vocab]
        total = sum(p for _, p in candidates)
        r = rng.random() * total
        acc = 0.0
        for w, p in candidates:
            acc += p
            if r <= acc:
                tokens.append(w)
                break
        if tokens[-1] == "</s>":
            break
    return tokens
```

Amostragem proporcional à probabilidade. Sempre dá diferentes resultados por semente. Para resultados semelhantes a uma busca de feixe, escolha o argmax em cada passo (avididade) e adicione um pequeno botão de aleatoriedade (temperatura).

> Para o resultado de um estudo semelhante, cada passo recebe um volume máximo de arg () e adiciona uma pequena rotação randomizada () temperatura).

### Passo 5: perplexidade

```python
import math


def perplexity(prob_fn, sentences):
    total_log_prob = 0.0
    total_tokens = 0
    for sentence in sentences:
        padded = ["<s>"] + sentence + ["</s>"]
        for i in range(1, len(padded)):
            p = prob_fn(padded[i - 1], padded[i])
            total_log_prob += math.log(max(p, 1e-12))
            total_tokens += 1
    return math.exp(-total_log_prob / total_tokens)
```

Para o corpus Brown, um modelo KN de 4 gramas bem ajustado atinge perplexidade em torno de 140. Um transformador LM atinge 15-30 no mesmo conjunto de teste. O gap é cerca de 10x. Esse gap é o motivo pelo qual o campo se movia.

> 越低越好── Para o Brown 语料库, uma concentração de quatro componentes do modelo KN 模块困惑度约140──Transformer 语言模型在同一测试集上达到15-30──差距约10倍──这种差距就是这个领域转向的原因──

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

- **Classical NLP teaching.**A exposição mais clara ao suavizamento, MLE e perplexidade que pode ter.
  **经典 NLP 教学。**A melhor experiência de planeamento que você pode ter.
- **KenLM.**Biblioteca de produção n-gram. Utilizado como rescador em sistemas de fala e MT onde a baixa latência importa.
  **KenLM。**Gênero de produção n-gram 库── Usage for low delay语音和MT 系统的重评分器──
- **On-device autocomplete.**Modelos de trigramas nos teclados.
  **设备端自动补全。**Modelo de três grupos de teclado.
- **Baselines.**Sempre calcule uma perplexidade de LM de n gramas antes de declarar o seu LM neural bom.
  **基线。**Antes de anunciar o seu modelo de linguagem nervosa, sempre calcula n gramas de LM 困惑度── Se o seu Transformer  não bater o KN, então há problemas──

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

## Envia-o . Produto .

Salva como`outputs/prompt-lm-baseline.md`- Não .

> 保存为 `outputs/prompt-lm-baseline.md`- Não .

```markdown
---
name: lm-baseline
description: Build a reproducible n-gram language model baseline before training a neural LM.
phase: 5
lesson: 16
---

Given a corpus and target use (next-word prediction, rescoring, perplexity baseline), output:

1. N-gram order. Trigram for general English, 4-gram if corpus is large, 5-gram for speech rescoring.
2. Smoothing. Modified Kneser-Ney is the default; Laplace only for teaching.
3. Library. `kenlm` for production, `nltk.lm` for teaching, roll your own only to learn.
4. Evaluation. Held-out perplexity with consistent tokenization between train and test sets.

Refuse to report perplexity computed with different tokenization between systems being compared — perplexity numbers are comparable only under identical tokenization. Flag OOV rate in test set; KN handles OOV poorly unless you reserve a special <UNK> token during training.
```

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Exercícios.

1. **Easy.**Treinar um trigrama LM num corpo de Shakespeare de 1.000 frases. Gerencie 20 frases. Serão plausíveis localmente mas globalmente incoerentes. Esta é a demonstração canônica.
   **简单。**Em 1000 frases de Shakespeare, o texto é um modelo de linguagem de três grupos.
2. **Medium.**Aplique perplexidade para o seu modelo KN em uma divisão Shakespeare prolongada. Comparar com Laplace. Você deve ver perplexidade KN menor por 30-50%.
   **中等。**Em seu livro de Shakespeare, o seu modelo de constrangimento é reduzido em 30 a 50%.
3. **Hard.**Construir um corrector de ortografia de trigramas: dada uma palavra errada e seu contexto, gerar correções e classificar por probabilidade de contexto sob o LM. Avalie no corpus de ortografia Birkbeck (público).
   **困难。**构建三元组拼写纠错器:给定一个拼写错误的词及其上下文,生成纠正并按 LM 下的上下文概率排序──在 Birkbeck 拼写语料库(公开) 上评估──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Termos-chave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| N-gram | Word sequence / 词序列 | Sequence of `n` consecutive tokens. / `n` 个连续 token 的序列。 |
| Smoothing（平滑） | Avoiding zeros / 避免零 | Reallocating probability mass so unseen events get non-zero probability. / 重新分配概率质量使未见事件获得非零概率。 |
| Perplexity（困惑度） | LM quality metric / LM 质量指标 | `exp(-average log-prob)` on held-out data. Lower is better. / 留出数据上的 `exp(-平均对数概率)`。越低越好。 |
| Backoff（回退） | Fallback to shorter context / 回退到更短上下文 | If trigram count is zero, use bigram. Katz backoff formalizes this. / 如果三元组计数为零，使用二元组。Katz 回退将其形式化。 |
| Kneser-Ney | Best smoothing for n-grams / 最佳 n-gram 平滑 | Absolute discounting + continuation probability for the lower-order model. / 绝对折扣 + 低阶模型的续接概率。 |
| Continuation probability（续接概率） | KN-specific / KN 特有 | `P(w)` weighted by number of contexts `w` appears in, not by raw count. / `P(w)` 按 `w` 出现的上下文数量加权，而非原始计数。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.

## Mais leitura 延伸阅读

- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) o tratamento canônico de n-gram LM e suavização. / n-gram 语言模型和平滑的经典教材──
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739) o papel que resolveu Kneser-Ney como o melhor n-gram mais liso. / 确定 Kneser-Ney 为最佳 n-gram 平滑器的论文──
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) o papel KN original. / 原始 KN 论文。
- [KenLM](https://kheafield.com/code/kenlm/) produção rápida n-gram LM, ainda utilizada em 2026 para aplicações sensíveis à latência. / 快速生产级 n-gram 语言模型,2026年仍用于延迟敏感应用──
| N-gram | Word sequence | Sequence of `n` consecutive tokens. |
| Smoothing | Avoiding zeros | Reallocating probability mass so unseen events get non-zero probability. |
| Perplexity | LM quality metric | `exp(-average log-prob)` on held-out data. Lower is better. |
| Backoff | Fallback to shorter context | If trigram count is zero, use bigram. Katz backoff formalizes this. |
| Kneser-Ney | Best smoothing for n-grams | Absolute discounting + continuation probability for the lower-order model. |
| Continuation probability | KN-specific | `P(w)` weighted by number of contexts `w` appears in, not by raw count. |
| Entropy of text | Information per symbol | Average bits needed to encode the next symbol given the context. Shannon's 1951 estimate for printed English with up to 100 letters of context: 0.6-1.3 bits/letter, measured before any model existed. |

## Mais leitura

- [Shannon (1951). Prediction and Entropy of Printed English](https://www.princeton.edu/~wbialek/rome/refs/shannon_51.pdf) o experimento de adivinhação que definiu o alvo que cada modelo de linguagem ainda otimiza.
- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) o tratamento canônico de N-gram LM e o suavização.
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739)O papel que resolveu o Kneser-Ney como o melhor n-gram suave.
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) o papel KN original.
- [KenLM](https://kheafield.com/code/kenlm/) LM de produção rápida n-gram, ainda utilizado em 2026 para aplicações sensíveis à latência.
