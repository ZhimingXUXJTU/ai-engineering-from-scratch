# Embedings de Word  Word2Vec de zero  Word2Vec de zero

> Uma palavra é a companhia que mantém, e se treinar uma rede superficial sobre essa ideia, a geometria cai.
> Uma palavra depende da empresa que mantém.

> **【中文解读】**Word2Vec Colocar o termo mapeado em um espaço de tensão, semelhante ao termo em um espaço de tensão.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 3 · 03 (Backpropagation from Scratch) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 3 · 03（反向传播从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## O problema é o problema da introdução

O TF-IDF sabe .`dog`E ...`puppy`O que é que é preciso para que o sistema de classificação seja mais eficaz?`dog`Não pode generalizar-se para uma revisão sobre `puppy`Pode-se documentar isto listando sinônimos, mas isso falha em termos raros, jargão de domínio e em todas as línguas que não se anteciparam.

> TF-IDF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `dog`和 `puppy`É uma palavra diferente. Não sabe o que significa.`dog`A classificação do treinamento não pode ser generalizada para sobre`puppy`Você pode compensar por meio da lista de semêntimos, mas isso vai falhar em termos raros e em todas as línguas que você não espera.

Queres uma representação onde`dog`E ...`puppy`Terras próximas no espaço.`king - man + woman`terras próximas`queen`Onde um modelo treinou em`dog`Transfere algum sinal para `puppy`- Não.

> Tu queres um expressão,让 `dog`和 `puppy`Em espaço, perto.`king - man + woman`- Está bem .`queen`附近──让在 `dog`Modelo de treinamento gratuito para`puppy`- Transmitir sinais.

O Word2Vec deu-nos esse espaço. Rede neural de duas camadas, trilhões de tokens de treinamento, publicado em 2013. A arquitetura é quase embaraçosamente simples. Os resultados remodelaram a PNL durante uma década.

> Word2Vec  deu-nos espaço assim ∙ Bi-layered neural network, Million Tokens Training Run, 2013 ∙ Publicado ∙ Arquitetura simples a embaraçoso ∙ Resultados reformulados NLP  Década ∙

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

**Distributional hypothesis**(Primeiro, 1957): "Você saberá uma palavra pela companhia que ela mantém". Se duas palavras aparecem em contextos semelhantes, elas provavelmente significam coisas semelhantes.

> **分布假设（Distributional Hypothesis）**(Primeiro, 1957): "Você vai conhecê-lo através de uma empresa de palavras mantidas". Se duas palavras aparecem similares no texto acima e abaixo, elas podem significar coisas semelhantes.

Word2Vec vem em dois sabores, ambos explorando essa ideia.

> O Word2Vec tem duas variantes, todos usaram essa ideia.

- **Skip-gram.**Dado uma palavra central, prevê as palavras circundantes. `cat -> (the, sat, on)`com tamanho de janela 2.
  **Skip-gram（跳字模型）。**给定中心词,预测周围的词──`cat -> (the, sat, on)`, ventana grande para 2...
- **CBOW (continuous bag of words).**Dadas as palavras circundantes, prevê o centro.`(the, sat, on) -> cat`- Não .
  **CBOW（连续词袋模型）。**给定周围的词,预测中心词──`(the, sat, on) -> cat`- Não.

O Skip-gram é mais lento para treinar, mas lida melhor com palavras raras.

> O Skip-gram  treino mais lento mas melhor para lidar com palavras raras.

A rede tem uma camada oculta sem não linearidade. A entrada é um vetor de um só calor sobre o vocabulário. A saída é um softmax sobre o vocabulário. Depois do treinamento, você joga fora a camada de saída. Os pesos das camadas ocultas são os embebimentos.

> 网络有一个不带非线性激活函数的隐藏层――输入是单词表上的一个热向量――输出是单词表上的软max――训练后,你丢弃输出层――隐藏层的权重就是嵌入――

```
one-hot(center) ── W ──▶ hidden (d-dim) ── W' ──▶ softmax(vocab)
                          ^
                          this is the embedding
```

O truque: a softmax superior a 100 mil palavras é proibitivamente cara.**negative sampling**Previnir "se essa palavra contextual aparece perto desta palavra central, sim ou não". Amostra um punhado de palavras negativas (não co-ocorrentes) por par de treinamento em vez de calcular softmax sobre todo o vocabulário.

> : para 100.000 palavras fazer softmax 代价太高──Word2Vec 使用**负采样（Negative Sampling）**Traduzir para 2o tipo de tarefas. Prevê-lo " este acima abaixo palavra se aparece neste centro palavra perto, é ou não " . Cada treinamento é para a amostra de pouca quantidade de casos negativos (( não comum palavra), em vez de para o conjunto da palavra.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
word-vector-arithmetic
```

## Construí-lo

### Passo 1: par de treinamento a partir de um corpus

```python
def skipgram_pairs(docs, window=2):
    pairs = []
    for doc in docs:
        for i, center in enumerate(doc):
            for j in range(max(0, i - window), min(len(doc), i + window + 1)):
                if i == j:
                    continue
                pairs.append((center, doc[j]))
    return pairs
```

```python
>>> skipgram_pairs([["the", "cat", "sat", "on", "mat"]], window=2)
[('the', 'cat'), ('the', 'sat'),
 ('cat', 'the'), ('cat', 'sat'), ('cat', 'on'),
 ('sat', 'the'), ('sat', 'cat'), ('sat', 'on'), ('sat', 'mat'),
 ...]
```

Cada par (centro, contexto) numa janela é um exemplo positivo de treinamento.

> Cada palavra do centro da janela, acima da janela, é um exemplo de treinamento.

### Passo 2: inserção de tabelas

Duas matrizes.`W`é a tabela de inserção de palavras centrais (a que você mantém). `W'`É a tabela de palavras contextuais (muitas vezes descartada, às vezes mediada com `W`)).

> Duas matrizes.`W`É o centro das palavras em um quadro.`W'`É o que eu faço.`W`取平均) ⋅

```python
import numpy as np


def init_embeddings(vocab_size, dim, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(vocab_size, dim))
    W_prime = rng.normal(0, 0.1, size=(vocab_size, dim))
    return W, W_prime
```

O tamanho do vocabulário 10k e dim 100 é realista; para ensino, 50 vocabulários x 16 dim são suficientes para ver a geometria.

> 小随机初始化──词表大小10.000、维度100是现实;教学用50 词表 x 16 维就足看几何效果──

### Passo 3: objetivo negativo de amostragem

Para cada par positivo `(center, context)`, amostra `k`Exercite o modelo para que o produto ponto`W[center] · W'[context]`É alto para os positivos e baixo para os negativos.

> Para cada tipo de reação`(center, context)`, de " expression " em " sample "`k`个随机词作为负例──训练模型使正例的点积 `W[center] · W'[context]`高,负例的低──

```python
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def train_pair(W, W_prime, center_idx, context_idx, negative_indices, lr):
    v_c = W[center_idx]
    u_pos = W_prime[context_idx]
    u_negs = W_prime[negative_indices]

    pos_score = sigmoid(v_c @ u_pos)
    neg_scores = sigmoid(u_negs @ v_c)

    grad_center = (pos_score - 1) * u_pos
    for i, u in enumerate(u_negs):
        grad_center += neg_scores[i] * u

    W[context_idx] = W[context_idx]
    W_prime[context_idx] -= lr * (pos_score - 1) * v_c
    for i, neg_idx in enumerate(negative_indices):
        W_prime[neg_idx] -= lr * neg_scores[i] * v_c
    W[center_idx] -= lr * grad_center
```

A fórmula mágica: perda logística em pares positivos (quer sigmoide perto de 1) mais perda logística em pares negativos (quer sigmoide perto de 0). Gradientes fluem para ambas as tabelas.

> 神奇的公式:正例对上逻辑损失(希望 sigmoid 接近 1)加上负例对上逻辑损失(希望 sigmoid 接近 0) ・・・梯度流向两个表──完整推导见原始论文; se quiser fazer com que seja compreendido, use papel lápis走一遍──

### Passo 4: treinar em um corpo de brinquedo

```python
def train(docs, dim=16, window=2, k_neg=5, epochs=100, lr=0.05, seed=0):
    vocab = build_vocab(docs)
    vocab_size = len(vocab)
    rng = np.random.default_rng(seed)
    W, W_prime = init_embeddings(vocab_size, dim, seed=seed)
    pairs = skipgram_pairs(docs, window=window)

    for epoch in range(epochs):
        rng.shuffle(pairs)
        for center, context in pairs:
            c_idx = vocab[center]
            ctx_idx = vocab[context]
            negs = rng.integers(0, vocab_size, size=k_neg)
            negs = [n for n in negs if n != ctx_idx and n != c_idx]
            train_pair(W, W_prime, c_idx, ctx_idx, negs, lr)
    return vocab, W
```

Depois de épocas suficientes em um grande corpus, palavras que compartilham contextos têm embutições centrais semelhantes. Em um corpus de brinquedos, você vê o efeito de forma fraca. Em bilhões de tokens, você vê dramaticamente.

> Após passar por rotas suficientes no material de brinquedo, as palavras compartilhadas no texto abaixo têm palavras centrais semelhantes embutidas.

### Passo 5: o truque de analogia

```python
def nearest(vocab, W, target_vec, topk=5, exclude=None):
    exclude = exclude or set()
    inv_vocab = {i: w for w, i in vocab.items()}
    norms = np.linalg.norm(W, axis=1, keepdims=True) + 1e-9
    W_norm = W / norms
    target = target_vec / (np.linalg.norm(target_vec) + 1e-9)
    sims = W_norm @ target
    order = np.argsort(-sims)
    out = []
    for i in order:
        if i in exclude:
            continue
        out.append((inv_vocab[i], float(sims[i])))
        if len(out) == topk:
            break
    return out


def analogy(vocab, W, a, b, c, topk=5):
    v = W[vocab[b]] - W[vocab[a]] + W[vocab[c]]
    return nearest(vocab, W, v, topk=topk, exclude={vocab[a], vocab[b], vocab[c]})
```

Em vetores pré-treinados de 300d de Google News:

```python
>>> analogy(vocab, W, "man", "king", "woman")
[('queen', 0.71), ('monarch', 0.62), ('princess', 0.59), ...]
```

`king - man + woman = queen`Não porque o modelo saiba o que é a realeza, porque o vetor...`(king - man)`Captura algo como "royal", e adicionando-o a `woman`terras perto da região real-fêmea.

> `king - man + woman = queen`Não porque o modelo sabe o que é o reino, mas porque o volume.`(king - man)`Capturar algo parecido com "Royal House", vai adicioná-lo.`woman`Está em cima da área feminina da casa de rei.

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

Escrever Word2Vec a partir do zero é ensinar.`gensim`- Não .

> Desde o zero-editing Word2Vec é para ensinar.`gensim`- Não.

```python
from gensim.models import Word2Vec

sentences = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "dog", "ran", "across", "the", "room"],
]

model = Word2Vec(
    sentences,
    vector_size=100,
    window=5,
    min_count=1,
    sg=1,
    negative=5,
    workers=4,
    epochs=30,
)

print(model.wv["cat"])
print(model.wv.most_similar("cat", topn=3))
```

Para o trabalho real, quase nunca treinas Word2Vec sozinho.

> 实际工作中,你几乎从不自练 Word2Vec──你下载预训向量── você praticamente não treina a si mesmo

- **GloVe** A abordagem de factorizamento de matriz de co-ocorrência de Stanford. 50d, 100d, 200d, 300d pontos de controlo. Boa cobertura geral. A lição 04 abrange especificamente o GloVe.
  **GloVe**  斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦福 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 斯坦 
- **fastText** A extensão Word2Vec do Facebook que incorpora caracteres n-gramas.
  **fastText** Facebook's Word2Vec 扩展,嵌入字符 n-gram──通过组合子词处理词表外词──第 04 课──
- **Pretrained Word2Vec on Google News** 300d, vocabulário de palavras 3M, publicado em 2013. Ainda sendo baixado diariamente.
  **Google News 预训练 Word2Vec** 300 维,300.000词表,2013年发布──至今每天都有人下载──

### Quando o Word2Vec ainda vencer em 2026

- Treinar resumos médicos em uma hora num laptop, obter vetores especializados sem captura de modelos gerais.
  O estudo foi realizado em uma área de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesas em pesas em pes
- Engenharia de recursos em estilo analógico. `gender_vector = mean(man - woman pairs)`Subtrai-o de outras palavras para obter um eixo neutro de gênero.
  类比式特征工程──`gender_vector = mean(man - woman pairs)`                                                                                                                                                                                                                                                              
- Interpretabilidade. 100d é pequeno o suficiente para traçar através de PCA ou t-SNE e realmente ver aglomerados forma.
  可解释性──100 维足够小, pode ser através de PCA ou t-SNE 绘图并实际看到聚类形成──
- Qualquer lugar que seja, a inferência tem que ser executada no dispositivo sem GPU.
  Qualquer necessidade de funcionar em dispositivos sem GPU.

### Onde o Word2Vec falha

A parede policémica.`bank`tem um vetor.`river bank`E ...`financial bank`Partilha.`table`Um classificador para baixo não pode distinguir os sentidos do vetor.

> Dois termos:`bank`Só há um caminho.`river bank`和 `financial bank`Compartilha-a.`table`(electronic表格 vs. 家具) Compartilhar-se.

Embedings contextuais (ELMo, BERT, todos os transformadores desde então) resolveram isso produzindo um vetor diferente para cada ocorrência da palavra com base no contexto circundante.

> 上下文嵌入(ELMo、BERT 以及后的所有变体former) através do desenvolvimento de diferentes volumes para cada palavra, em função da sua circunvalação, resolveu este problema.

O problema da falta de vocabulário é o outro fracasso.`Zoomer-approved`O fastText corrige isto com a composição de subpalavras (leção 04).

> 词表外(Out-of-Vocabulary) problema é outro fracaso.`Zoomer-approved`Não há nenhum plano de preparação para o treinamento.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

## Envia-o . Produto .

Salva como`outputs/skill-embedding-probe.md`- Não .

```markdown
---
name: embedding-probe
description: Inspect a word2vec model. Run analogies, find neighbors, diagnose quality.
version: 1.0.0
phase: 5
lesson: 03
tags: [nlp, embeddings, debugging]
---

You probe trained word embeddings to verify they are working. Given a `gensim.models.KeyedVectors` object and a vocabulary, you run:

1. Three canonical analogy tests. `king : man :: queen : woman`. `paris : france :: tokyo : japan`. `walking : walked :: swimming : ?`. Report the top-1 result and its cosine.
2. Five nearest-neighbor tests on domain-specific words the user supplies. Print top-5 neighbors with cosines.
3. One symmetry check. `similarity(a, b) == similarity(b, a)` to within float precision.
4. One degenerate check. If any embedding has a norm below 0.01 or above 100, the model has a training bug. Flag it.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to declare a model good on analogy accuracy alone. Analogy benchmarks are gameable and do not transfer to downstream tasks. Recommend intrinsic + downstream evaluation together.
```

## Exercícios.

1. **Easy.**Exerce o ciclo de treinamento num pequeno corpo (20 frases sobre gatos e cães).`nearest(vocab, W, W[vocab["cat"]])`Retorno `dog`Se não, aumenta os tempos ou o vocabulário.
   **简单。**Em um pequeno discurso, um ciclo de treinamento.`nearest(vocab, W, W[vocab["cat"]])`返回的前3中包含 `dog`Se não houver, aumenta a rotina ou a expressão.
2. **Medium.**Adicionar sub-esampulação de palavras frequentes.`10^-5`Os resultados da análise de dados são apresentados em pares de formação com probabilidade proporcional à sua frequência.
   **中等。**添加高频词子采样──频率高于 `10^-5`A probabilidade de que as palavras sejam em proporção com a sua frequência é de que as palavras sejam eliminadas.
3. **Hard.**Treinar um modelo no corpus de 20 Newsgroups.`he - she`E ...`doctor - nurse`- Projeto de palavras de ocupação em ambos os eixos. Relata quais ocupações têm a maior lacuna de viés. Este é o tipo de investigação de equidade da sonda usada pelos pesquisadores.
   **困难。**Em 20 Newsgroups 语料上训练模型──计算两个偏见轴:`he - she`和 `doctor - nurse`将职业词投投向两个轴上 报告哪些职业有最大偏见差                                                                                                                                                                                                                                                   

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Termos-chave .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Word embedding | Word as a vector | A dense, low-dim (typically 100-300) representation learned from context. | 词嵌入 | 词向量 | 从上下文学习的稠密、低维（通常 100-300）表示。 |
| Skip-gram | Word2Vec trick | Predict context words from center word. Slower than CBOW, better for rare words. | Skip-gram | Word2Vec 技巧 | 从中心词预测上下文词。比 CBOW 慢，对罕见词更好。 |
| Negative sampling | Training shortcut | Replace softmax over full vocab with binary classification against `k` random words. | 负采样 | 训练捷径 | 用对 `k` 个随机词的二分类替换对整个词表的 softmax。 |
| Static embedding | One vector per word | Same vector regardless of context. Fails on polysemy. | 静态嵌入 | 每个词一个向量 | 无论上下文如何都是同一个向量。在多义词上失败。 |
| Contextual embedding | Context-sensitive vector | Different vector for each occurrence based on surrounding words. What transformers produce. | 上下文嵌入 | 上下文敏感向量 | 根据周围词，每次出现都是不同的向量。Transformer 产生的。 |
| OOV | Out of vocabulary | Word not seen in training. Word2Vec cannot produce a vector for these. | OOV（词表外） | 词表外 | 训练中未见过的词。Word2Vec 无法为这些词产生向量。 |

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Mais leitura 延伸阅读

- [Mikolov et al. (2013). Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546)O papel de amostragem negativa. Curto e legível.
- [Rong, X. (2014). word2vec Parameter Learning Explained](https://arxiv.org/abs/1411.2738) a derivação mais clara dos gradientes, se a matemática do papel original se sentir densa. / 最清晰的梯度推导, se você achar que a matemática é muito intensa.
- [gensim Word2Vec tutorial](https://radimrehurek.com/gensim/models/word2vec.html) configurações de treinamento de produção que realmente funcionam. / 真正有效的生产训练设置──
