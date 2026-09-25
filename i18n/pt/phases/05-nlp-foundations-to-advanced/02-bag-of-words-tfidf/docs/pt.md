# Saco de palavras, TF-IDF, e representação de texto .

> A TF-IDF ainda supera as embarcações em tarefas bem definidas em 2026.
> Antes de contar, depois de pensar, em tarefas definidas, o TF-IDF até 2026 ainda vai ganhar a entrada.

> **【中文解读】**词袋模型忽略词序只统计词频,TF-IDF 通过惩罚常见词突出关键词―― é o método mais básico de expressão de texto――

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 02 (Linear Regression from Scratch) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 02（线性回归从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Construir representações de sacos de palavras e TF-IDF a partir do zero
  Desde零构建词袋模型和 TF-IDF indicar
- Compreender vetores escassos, frequência de termos e frequência de documentos inversa
  Compreender Raridade de Velocidade, Frequência de Palavras e Frequência de Arquivos
- Utilização do CountVectorizer e do TfidfVectorizer da scikit-learn na produção
  Em produção usando um computador de vectores e um vectorizador de tfidf
- Saber quando a TF-IDF vence os embutidos e quando falha
  Sabe o TF-IDF, quando venceu, quando falhou.

## O problema é o problema da introdução

O modelo precisa de números.

> O modelo precisa de números.

Cada pipeline de PNL tem que responder à mesma pergunta. Como transformar um fluxo de tokens de comprimento variável em um vetor de tamanho fixo que um classificador pode consumir. A primeira resposta que o campo aterrou foi a mais estúpida que funciona. Conte as palavras. Faça um vetor.

> Cada linha de fluxo de água da PNL deve responder à mesma pergunta: como transformar o tamanho do token em um tamanho fixo de torção, para que o divisor possa consumir. A primeira resposta dada nesta área é o método mais utilizado.

Esse vetor tem levado mais produção de PNL do que qualquer modelo de incorporação. Filtros de spam, classificadores de tópicos, detecção de anomalias de registro, classificação de pesquisa (antes do BM25), a primeira onda de análise de sentimentos, a primeira década de benchmarks acadêmicos de PNL. 2026 os profissionais ainda alcançam primeiro em tarefas de classificação estreita. É rápido, interpretável e muitas vezes indistinguível de um modelo de inserção de parâmetros de 400M em tarefas onde a presença da palavra é o que importa.

> Esta produção de NLP em carga de vector  aplicações são maiores do que qualquer modelo embutida. Filtros de lixo, filtros de tópicos, registros de exames anormais, pesquisas em ordem de ordem, BM25 antes de surgir)  primeira onda de análise emocional, primeira década do teste de base de NLP acadêmico. Em 2026 os profissionais em tarefas de categorias estreitas ainda vão usá-lo primeiro. É rápido, explicável, e em tarefas de existência ou não de palavras, geralmente é difícil distinguir entre um modelo embutido de 4 bilhões de parâmetros.

Esta lição constrói uma bolsa de palavras, depois TF-IDF, a partir do zero, mostra o scikit-learn fazendo o mesmo em três linhas, e depois nomeia o modo de falha que faz você alcançar as incorporações.

> Este curso começa com o modelo de caixa de palavras, depois construi TF-IDF, e depois mostra o aprendizado de forma simples usando o código de três linhas para fazer o mesmo.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

**Bag of Words (BoW)**Para cada documento, conte quantas vezes cada palavra vocabulário aparece.`i`É a contagem de palavras.`i`- Não .

> **词袋模型（Bag of Words, BoW）**抛弃顺序──对每文档,统计每词表词出现的次数──向量长度是词表大小──位置 `i`É um termo`i`O número de pessoas.

**TF-IDF**Uma palavra que aparece em todos os documentos é pouco informativa, por isso diminui-a. Uma palavra rara em todo o corpo, mas frequente em um único documento é sinal, por isso diminui-a.

> **TF-IDF**Para a BoW, o peso é elevado. O número de palavras em cada documento não é elevado, portanto, o seu peso é reduzido.

```
TF-IDF(w, d) = TF(w, d) * IDF(w)
             = count(w in d) / |d| * log(N / df(w))
```

Onde ?`TF`é a frequência do termo no documento, `df`é a frequência do documento (quantos documentos contêm a palavra), `N`O documento é total.`log`Mantém o peso limitado para palavras onipresentes.

> Entre eles `TF`É um dos mais importantes.`df`É a frequência de documentos (quanta documentação contém esse termo),`N`É o número total de arquivos.`log`O poder de manter o peso das palavras inexistentes tem limites.

Propriedade chave: ambos produzem vetores escassos com eixos interpretáveis. Você pode olhar para os pesos de um classificador treinado e ler quais palavras empurram um documento em direção a cada classe.

> Cariedade-Clínica: ambas produzem uma rara tendência de eixo explicável. Você pode ver o peso de um bom classificador treinado, ler quais palavras o arquivo irá levar para cada categoria. Você não pode fazer isso usando um BERT de 768 dimensiones embutidos em um sistema de classificação.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
bow-tfidf
```

## Construí-lo

### Passo 1: construir o vocabulário

```python
def build_vocab(docs):
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab
```

Entrada: lista de documentos tokenizados (qualquer tokenizer de nível de palavra o fará; o `code/main.py`Esta lição utiliza uma variante simplificada em minúsculas).`{word: index}`O índice de palavras 0 é a primeira palavra vista no primeiro documento.

> 输入:token 化的文档列表( qualquer palavra classe分词器都可以;本课的 `code/main.py`Utilize simplificação ignorar (output:`{word: index}`字典──稳定的插入顺序 significa 字符索引 0 é a primeira palavra que se vê no primeiro arquivo──惯例各不相同;scikit-learn 按字母排序──

### Passo 2: Saco de palavras

```python
def bag_of_words(docs, vocab):
    matrix = [[0] * len(vocab) for _ in docs]
    for i, doc in enumerate(docs):
        for token in doc:
            if token in vocab:
                matrix[i][vocab[token]] += 1
    return matrix
```

```python
>>> docs = [["cat", "sat", "on", "mat"], ["cat", "cat", "ran"]]
>>> vocab = build_vocab(docs)
>>> bag_of_words(docs, vocab)
[[1, 1, 1, 1, 0], [2, 0, 0, 0, 1]]
```

As linhas são documentos, as colunas são índices de vocabulário.`[i][j]`É "quantas vezes palavra `j`aparece no documento `i`. " Doc 1 tem `cat`- Doutor 0 fez.`ran`zero vezes porque não o fez.

> 行是文档──列是词表索引──条目 `[i][j]`É " palavra "`j`Em arquivo`i`"Quantas vezes apareceu"`cat`Porque ele realmente apareceu duas vezes.`ran`Porque não apareceu.

### Passo 3: frequência dos termos e frequência dos documentos

```python
import math


def term_frequency(doc_bow, doc_length):
    return [c / doc_length if doc_length else 0 for c in doc_bow]


def document_frequency(bow_matrix):
    df = [0] * len(bow_matrix[0])
    for row in bow_matrix:
        for j, count in enumerate(row):
            if count > 0:
                df[j] += 1
    return df


def inverse_document_frequency(df, n_docs):
    return [math.log((n_docs + 1) / (d + 1)) + 1 for d in df]
```

Dois truques de suavizamento que valham a pena nomear.`(n+1)/(d+1)`Evita-se .`log(x/0)`- A trailha .`+1`As aplicações de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de como para para para para para para para para para para para para para para para para para para para para para para para os de software de software de software de software de software de software de de software de software`log(N/df)`Ambas funcionam, a versão suave é mais amigável.

> Duas técnicas de planeamento dignas de atenção.`(n+1)/(d+1)` evit `log(x/0)`O que é que é?`+1`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `log(N/df)`两种都有效;平滑版本更友好

### Passo 4: TF-IDF

```python
def tfidf(bow_matrix):
    n_docs = len(bow_matrix)
    df = document_frequency(bow_matrix)
    idf = inverse_document_frequency(df, n_docs)
    out = []
    for row in bow_matrix:
        length = sum(row)
        tf = term_frequency(row, length)
        out.append([tf_j * idf_j for tf_j, idf_j in zip(tf, idf)])
    return out
```

```python
>>> docs = [
...     ["the", "cat", "sat"],
...     ["the", "dog", "sat"],
...     ["the", "cat", "ran"],
... ]
>>> vocab = build_vocab(docs)
>>> bow = bag_of_words(docs, vocab)
>>> tfidf(bow)
```

Três documentos, cinco palavras vocabulares (`the`- Não .`cat`- Não .`sat`- Não .`dog`- Não .`ran` ).`the`Aparece em todos os três, por isso, as forças armadas são baixas.`dog`Os vetores são escassos (a maioria das entradas são pequenas) e as palavras discriminatórias pop.

> Três documentos, cinco palavras para expressão`the`- Não.`cat`- Não.`sat`- Não.`dog`- Não.`ran`)。`the`Todos os três documentos aparecem, então a IDF é muito baixa.`dog`Apenas aparece num arquivo, então sua IDF  muito alta ⋅ volume é raro ⋅ maioria das条目 ⋅ muito pequeno ⋅

### Passo 5: Normalização de linhas L2

```python
def l2_normalize(matrix):
    out = []
    for row in matrix:
        norm = math.sqrt(sum(x * x for x in row))
        out.append([x / norm if norm else 0 for x in row])
    return out
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

Sem normalização, um documento mais longo obtém um vetor maior e domina as pontuações de semelhança. Normalização L2 coloca cada documento na hiperesfera unidade.

> Sem regeneração, arquivos mais longos obtêm maiores volumes e dominam a similaridade de pontos.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

O Scikit-Learn vai enviar a versão de produção.

> O Sikit-Learn forneceu uma versão de produção.

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

docs = ["the cat sat on the mat", "the dog sat on the mat", "the cat ran"]

bow_vectorizer = CountVectorizer()
bow = bow_vectorizer.fit_transform(docs)
print(bow_vectorizer.get_feature_names_out())
print(bow.toarray())

tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(docs)
print(tfidf.toarray().round(3))
```

`CountVectorizer`faz tokenization, vocabulário e BoW em uma chamada. `TfidfVectorizer`Para 100k documentos, a versão densa não cabe na memória; permaneça densa até que o classificador exija densa.

> `CountVectorizer`Durante o seu uso, o termo "completar" é usado para designar um termo "completar".`TfidfVectorizer`增加 IDF 加权和 L2 归结化──都回归稀疏矩阵──对10万篇文档,密集版本放不进内存;在分类器要求密集之前保持稀疏──

Os botões que mudam tudo:

>  modificar tudo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

| Arg | Effect | 参数 | 效果 |
|-----|--------|------|------|
| `ngram_range=(1, 2)` | Include bigrams. Usually boosts classification. | `ngram_range=(1, 2)` | 包含二元组。通常提升分类效果。 |
| `min_df=2` | Drop words in fewer than 2 docs. Trims vocabulary on noisy data. | `min_df=2` | 丢弃出现在少于 2 个文档中的词。在噪声数据上修剪词表。 |
| `max_df=0.95` | Drop words in more than 95% of docs. Approximates stopword removal without a hardcoded list. | `max_df=0.95` | 丢弃出现在超过 95% 文档中的词。近似停用词去除，无需硬编码列表。 |
| `stop_words="english"` | scikit-learn's builtin stopword list. Task-dependent — sentiment analysis should *not* drop negations. | `stop_words="english"` | scikit-learn 内置停用词列表。因任务而异——情感分析不应去除否定词。 |
| `sublinear_tf=True` | Use `1 + log(tf)` instead of raw `tf`. Helps when a term repeats many times in one doc. | `sublinear_tf=True` | 使用 `1 + log(tf)` 代替原始 `tf`。当一个词在一个文档中重复多次时有帮助。 |

### Quando o TF-IDF ainda vencer (a partir de 2026)

- Detecção de spam, rotulagem de tópicos, sinalização de anomalias de registro.
  垃圾邮件检测、主题标注、日志异常标注── existência ou não de palavras é o essencial; significados de pequenas diferenças não são importantes──
- Regimes de baixo nível de dados (centenas de exemplos rotulados).
  低数据场景 ((100 标注样本) ⋅ TF-IDF 加逻辑回归没有预训成本──
- Qualquer lugar que tenha latência, TF-IDF mais um modelo linear responde em microsecondas.
  任何延迟敏感场景──TF-IDF 加线性模型的响应时间是微秒级──通过变压器 嵌入一个文档需要 10-100 毫秒──
- Sistemas que precisam explicar as suas previsões, inspecionar os coeficientes do classificador, as palavras mais positivas são a razão.
  需要解释预测结果的系统──检查分类器的系数──排名最高正权重词就是原因──

### Quando o TF-IDF falhar

Considerem estes dois documentos:

> 语义盲点──考虑以下两个文档:

- "O filme não foi bom".
- "O filme foi excelente".

Uma é uma revisão negativa, outra é positiva, a sua sobreposição entre os TF e os IDF é exatamente o mesmo.`{the, movie, was}`Um classificador de sacos de palavras tem que memorizar essa palavra .`not`Próximo`good`Pode aprender isto com dados suficientes, mas nunca tão graciosamente como um modelo que entende a sintaxe.

> Uma é avaliação negativa, outra é avaliação positiva.`{the, movie, was}`                                                                                                                                                                                                                                                              `good` perto `not`É possível aprender isso com dados suficientes, mas nunca será tão bonito como um modelo de compreensão de linguagem.

O outro fracasso: palavras fora do vocabulário na inferência.`Zoomer-approved`Se o token não apareceu no treinamento, as palavras-chave (leção 04) lidam com isso.

> 另一个失败:推理时的词表外(Out-of-Vocabulary, OOV)词──在 IMDb 评论上训练的 BoW 模型不知道如何处理 `Zoomer-approved`Se este token não aparecer no treino.

### Embedings híbridos: TF-IDF ponderados

O padrão pragmático de 2026 para classificação de dados médios: utilizar pesos TF-IDF como atenção sobre as incorporações de palavras.

> O programa de referência prático para o ano 2026: uso do TF-IDF 权重作为词嵌的注意力――

```python
def tfidf_weighted_embedding(doc, tfidf_scores, embedding_table, dim):
    vec = [0.0] * dim
    total_weight = 0.0
    for token in doc:
        if token not in embedding_table or token not in tfidf_scores:
            continue
        weight = tfidf_scores[token]
        emb = embedding_table[token]
        for i in range(dim):
            vec[i] += weight * emb[i]
        total_weight += weight
    if total_weight == 0:
        return vec
    return [v / total_weight for v in vec]
```

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

Você obtém capacidade semântica a partir de embebimentos e ênfase em palavras raras a partir de TF-IDF. Classificador treina no vetor em conjunto. Isso supera por si só para classificação de sentimento, tópico e intenção abaixo de cerca de 50 mil exemplos rotulados.

> Você obtém habilidade de sintaxe através de emplacamentos, de TF-IDF  obtém raríssimos palavras enfatizadas . . . . . . . . . . . . . . . . .. .. ..................................................................................................................................................................................................................

## Envia-o . Produto .

Salva como`outputs/prompt-vectorization-picker.md`- Não .

```markdown
---
name: vectorization-picker
description: Given a text-classification task, recommend BoW, TF-IDF, embeddings, or a hybrid.
phase: 5
lesson: 02
---

You recommend a text-vectorization strategy. Given a task description, output:

1. Representation (BoW, TF-IDF, transformer embeddings, or a hybrid). Explain why in one sentence.
2. Specific vectorizer configuration. Name the library. Quote the arguments (`ngram_range`, `min_df`, `max_df`, `sublinear_tf`, `stop_words`).
3. One failure mode to test before shipping.

Refuse to recommend embeddings when the user has under 500 labeled examples unless they show evidence of semantic failure in a TF-IDF baseline. Refuse to remove stopwords for sentiment analysis (negations carry signal). Flag class imbalance as needing more than a vectorizer change.

Example input: "Classifying 30k customer support tickets into 12 categories. Most tickets are 2-3 sentences. English only. Need explainability for audit logs."

Example output:

- Representation: TF-IDF. 30k examples is not small; explainability requirement rules out dense embeddings.
- Config: `TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_df=0.95, sublinear_tf=True, stop_words=None)`. Keep stopwords because category keywords sometimes are stopwords ("not working" vs "working").
- Failure to test: verify `min_df=3` does not drop rare category keywords. Run `get_feature_names_out` filtered by class and eyeball.
```

## Exercícios.

1. **Easy.**Implementação `cosine_similarity(doc_vec_a, doc_vec_b)`Verificar que os documentos idênticos têm uma pontuação de 1,0 e os documentos de vocabulário disjunto 0,0.
   **简单。**Em L2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `cosine_similarity(doc_vec_a, doc_vec_b)` Verificação do mesmo arquivo com uma pontuação de 1.0, palavra表完全不相交的文档分分为0.0♦
2. **Medium.**Adicionar`n-gram`apoio a`bag_of_words`Parâmetro .`n`Produz contagens sobre `n`-Testa isso.`n=2`- Não .`["the", "cat", "sat"]`produz conteúdos de bigram para `["the cat", "cat sat"]`- Não .
   **中等。**Por`bag_of_words`添加 `n-gram`支持──参数 `n` produzir `n`-gram de cálculo.`n=2`时  `["the", "cat", "sat"]`产生二元组 `["the cat", "cat sat"]`O número de pessoas.
3. **Hard.**Construa o híbrido de incorporação ponderada TF-IDF acima usando vetores GloVe 100d (descarregar uma vez, cache). Compare a precisão da classificação com a simples TF-IDF e as simples incorporações medias em conjunto no conjunto de dados 20 Newsgroups. Relatório que ganha onde.
   **困难。**Utilize GloVe 100 维向量(download一次并缓存) Construir os acima mencionados esquemas de inserção de TF-IDF加权嵌混合方案── comparar a taxa de classificação de dados em 20 Newsgroups, em comparação com a simples TF-IDF和纯平均值池化嵌入── relatório que está em algum lugar vencer.

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Termos-chave .

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| BoW | Word frequency vector | Counts of vocabulary words in one document. Throws away order. | BoW（词袋模型） | 词频向量 | 一个文档中词表词的计数。抛弃顺序。 |
| TF | Term frequency | Count of a word in a document, optionally normalized by document length. | TF（词频） | 词频 | 一个词在文档中的计数，可选按文档长度归一化。 |
| DF | Document frequency | Count of documents containing the word at least once. | DF（文档频率） | 文档频率 | 至少包含该词一次的文档计数。 |
| IDF | Inverse document frequency | `log(N / df)` smoothed. Downweights words that appear everywhere. | IDF（逆文档频率） | 逆文档频率 | 经平滑的 `log(N / df)`。降低到处出现的词的权重。 |
| Sparse vector | Mostly zeros | Vocabulary is typically 10k-100k words; most are absent from any given document. | 稀疏向量 | 大部分为零 | 词表通常有 1 万到 10 万个词；大多数在任何给定文档中都不出现。 |
| Cosine similarity | Vector angle | Dot product of L2-normalized vectors. 1 is identical, 0 is orthogonal. | 余弦相似度 | 向量夹角 | L2 归一化向量的点积。1 表示相同，0 表示正交。 |

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Mais leitura 延伸阅读

- [scikit-learn — feature extraction from text](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) a referência canônica da API, mais notas em cada botão. / 权威 API 参考,以及每个参数的说明──
- [Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval](https://www.sciencedirect.com/science/article/pii/0306457388900210) o artigo que tornou o TF-IDF o padrão de uma década. / 使 TF-IDF 成为十年默认方案的论文──
- ["Why TF-IDF Still Beats Embeddings" — Ashfaque Thonikkadavan (Medium)](https://medium.com/@cmtwskb/why-tf-idf-still-beats-embeddings-ad85c123e1b2) 2026 assumir quando o velho método vence e porquê. / 2026 年对旧方法何时胜出以及为什么的观点──
