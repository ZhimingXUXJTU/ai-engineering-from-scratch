# Tópicos Modelagem  LDA e BERTopic 

> LDA: documentos são misturas de tópicos, tópicos são distribuições sobre palavras. BERTopic: documentos em aglomeração em espaço de inserção, aglomerações são tópicos.
> LDA:文档是主题的混合,主题是词的分布──BERTOPIC:文档在嵌入空间中的聚类,聚类就是主题──相同目标,不同分解──

> **【中文解读】**LDA usando o modelo de probabilidade de descoberta de tópicos, BERTopic usando BERT 嵌入──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec)
**Time:** ~45 minutes | **时间:** ~45 分钟


## O problema é o problema da introdução

Você tem 10.000 ingressos de suporte ao cliente, 50.000 artigos de notícias ou 200.000 tweets. Você precisa saber sobre o que a coleção é sem lê-la. Você não tem categorias rotuladas. Você nem sabe quantas categorias existem.
> Você tem 10.000 张客户支持工单,50.000 篇新闻文章或200.000 条推文── você precisa entender o tópico deste conjunto sem ler── você não tem categorias marcadas── você nem sabe quantas categorias existem──

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.


A modelagem de tópicos responde a isso sem supervisão. Dê-lhe um corpus, retome um pequeno conjunto de tópicos coerentes e, para cada documento, uma distribuição sobre esses tópicos.
> Tema construção em caso de não supervisão responder a esta questão.

Dois famílias algorítmicas dominam. LDA (2003) trata cada documento como uma mistura de tópicos latentes e cada tópico como uma distribuição sobre palavras.
> 两个算法族占主导地位――LDA(2003) vai considerar cada artigo como uma mistura de tópicos potenciais, cada tópico como uma distribuição de palavras―― o teor é de Beyes―― ainda é necessário distribuir os tópicos membros mistos e publicar na produção de uma distribuição de probabilidade de termos de classes explicáveis――

O BERTopic (2020) codifica documentos com BERT, reduz a dimensionalidade com UMAP, agrupa com HDBSCAN e extrai palavras tópicas através de TF-IDF baseado em classe. Ganha no texto curto, mídias sociais e em qualquer coisa onde a semântica semelhante importa mais do que a sobreposição de palavras. Um documento recebe um tópico, que é uma limitação para o conteúdo de formato longo.
> BERTopic(2020) com o documento de codificação BERT, com UMAP 降维, com HDBSCAN 聚类, através de tipos baseados em TF-IDF 提取主题词──它在短文本、社交媒体和语义相似性比词重叠更重要的内容上胜出──一篇文档获得一个主题,这对长篇内容是一个限制──

Esta lição constrói a intuição para ambos e nomes para escolher para um determinado corpo.
> Esta aula é para os dois construir um intuito e indicar que o material de linguagem deve ser escolhido.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


## O conceito central.

![LDA mixture model vs BERTopic clustering](../assets/topic-modeling.svg)
> ![LDA 混合模型 vs BERTopic 聚类](../assets/topic-modeling.svg)

**LDA generative story.**Cada tópico é uma distribuição sobre palavras. Cada documento é uma mistura de tópicos. Para gerar uma palavra em um documento, amostre um tópico da mistura do documento, em seguida, amostre uma palavra da distribuição desse tópico. Inferência inverte isso: dada palavras observadas, infer a distribuição do tópico por documento e a distribuição da palavra por tópico.
> **LDA 生成故事。**Cada tema é a distribuição de palavras. Cada documento é a mistura de temas. Deve-se gerar uma palavra no documento, de uma mistura de documentos, e depois de uma palavra, de uma distribuição de dados.

A saída de LDA chave:
> 关键 LDA 输出:

- `doc_topic`: matriz `(n_docs, n_topics)`, cada linha é de 1 (mistura de tópicos do documento).
- `topic_word`: matriz `(n_topics, vocab_size)`, cada linha é de 1 (distribuição de palavras do tópico).
> - `doc_topic`- Não .`(n_docs, n_topics)`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,
- `topic_word`- Não .`(n_topics, vocab_size)`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,

**BERTopic pipeline.**
> **BERTopic 流水线。**

1. Cada documento é codificado com um transformador de frases (por exemplo, `all-MiniLM-L6-v2`(v. 384) vectores de dimensão 384.
2. Reduzir a dimensionalidade com UMAP para ~ 5 dimensões. Embedments BERT são muito escuras para agrupamento.
3. Cluster com HDBSCAN. Baseado na densidade, produz clusters de tamanho variável e um rótulo "outlier".
4. Para cada cluster, calcular TF-IDF baseado em classe sobre os documentos do cluster para extrair as principais palavras.
> 1. Us句子 Transformer`all-MiniLM-L6-v2`(Categoria: "Divulgação")
2. Utilize UMAP 降维到大约5维度.
3. Utilizando HDBSCAN 聚类── baseada na densidade, produzir variações de grande dimensão 聚类和离群值标签──
4. Para cada classe, em documentos de classe, calculado com base em classe TF-IDF para extrair palavras de topo.

A saída é um tópico por documento (mais um -1 outlier label). Opcionalmente, uma adesão suave através do vetor de probabilidade do HDBSCAN.
> 输出是每篇文档一个主题 (加上 -1 离群值标签) ⋅可选地, através da HDBSCAN ⋅

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.


## Construí-lo e realizei-o.
```figure
topic-drift
```

## Construí-lo

### Passo 1: LDA via scikit-learn
> Nota: removeu o termo "suspendido", min_df 和 max_df 过罕见和无处不在的词, use CountVectorizer ( não TfidfVectorizer), pois LDA 期望原始计数。

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


def fit_lda(documents, n_topics=5, max_features=1000):
    cv = CountVectorizer(
        max_features=max_features,
        stop_words="english",
        min_df=2,
        max_df=0.9,
    )
    X = cv.fit_transform(documents)
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=50,
        learning_method="online",
    )
    doc_topic = lda.fit_transform(X)
    feature_names = cv.get_feature_names_out()
    return lda, cv, doc_topic, feature_names


def print_top_words(lda, feature_names, n_top=10):
    for idx, topic in enumerate(lda.components_):
        top_idx = np.argsort(-topic)[:n_top]
        words = [feature_names[i] for i in top_idx]
        print(f"topic {idx}: {' '.join(words)}")
```

Nota: palavras de parada removidas, min_df e max_df filtros termos raros e onipresentes, CountVectorizer (não TfidfVectorizer) porque LDA espera contagens brutas.
> `Topic != -1`O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é.`min_topic_size`控制 HDBSCAN's minimum聚类大小;BERTopic 库默认为 10──本例为课程的规模显然设为15──对于超过10,000 文档语料,增加到50或100──

### Passo 2: BERTopic (produção)
> 两种方法都输出主题词――问题是这些词是否连贯――

```python
from bertopic import BERTopic

topic_model = BERTopic(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    min_topic_size=15,
    verbose=True,
)

topics, probs = topic_model.fit_transform(documents)
info = topic_model.get_topic_info()
print(info.head(20))
valid_topics = info[info["Topic"] != -1]["Topic"].tolist()
for topic_id in valid_topics[:5]:
    print(f"topic {topic_id}: {topic_model.get_topic(topic_id)[:10]}")
```

O filtro ligado .`Topic != -1`elimina o bucket de outlier do BERTopic (documentos que o HDBSCAN não pôde agrupar). `min_topic_size`O sistema de controle de dados HDBSCAN controla o tamanho mínimo do cluster; a biblioteca padrão do BERTopic é 10. Este exemplo define-o explicitamente em 15 para a escala da lição. Para corpora acima de 10.000 documentos, aumentar para 50 ou 100.
> - **主题连贯度（c_v）。**结合滑动窗口上下文中顶级词对的 NPMI ([[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]), ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]] ]]`gensim.models.CoherenceModel`配 `coherence="c_v"`- Não.
- **主题多样性。**Proporção de palavras em todos os tópicos.
- **定性检查。**阅读每个主题的顶级词――它们是否命名一个真实的东西?

### Passo 3: Avaliação

Os dois métodos produzem palavras temáticas.

- **Topic coherence (c_v).**Combina NPMI (informação mútua pontual normalizada) de pares de palavras principais em contextos de janela deslizante, agrega as pontuações em vetores de tópicos e compara esses vetores através de semelhança cosínica.`gensim.models.CoherenceModel`com`coherence="c_v"`- Não .
- **Topic diversity.**Fração de palavras únicas em todas as principais palavras de todos os tópicos.
- **Qualitative inspection.**Leia as palavras principais de cada tópico.


> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Quando escolher qual

| Situation | Pick |
|-----------|------|
| Short text (tweets, reviews, headlines) | BERTopic |
| Long documents with topic mixtures | LDA |
| No GPU / limited compute | LDA or NMF |
| Need document-level multi-topic distributions | LDA |
| LLM integration for topic labeling | BERTopic (direct support) |
| Resource-constrained edge deployment | LDA |
| Max semantic coherence | BERTopic |

A maior consideração prática é o comprimento do documento. Embedings BERT truncate; LDA conta trabalho em qualquer comprimento. Para documentos mais longos do que o contexto do modelo de embebimento, seja chunk + agregado ou use LDA.

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


## Use-o com o framework implementado.

A pilha de 2026:
> 2026  

- **BERTopic.**Default para texto curto e qualquer coisa que seja semântica.
- **`gensim.models.LdaModel`.**LDA clássico para produção, maduro, testado em batalha.
- **`sklearn.decomposition.LatentDirichletAllocation`.**LDA fácil para experimentos.
- **NMF.**Factorization de matriz não negativa, alternativa rápida à LDA, qualidade comparável em texto curto.
- **Top2Vec.**Design semelhante ao BERTopic, comunidade menor, mas boa em alguns pontos de referência.
- **FASTopic.**Mais novo, mais rápido do que o BERTopic em corpora muito grandes.
- **LLM-based labeling.**Execute qualquer agrupamento, e depois peça a um modelo para nomear cada agrupamento.
> - **BERTopic。**短文本和语义重要的场景的默认选择──
- **`gensim.models.LdaModel`。**Classe de produção LDA, maduro, longa experiência
- **`sklearn.decomposition.LatentDirichletAllocation`。**实验用简单 LDA──
- **NMF。**Não-negativo de matrizes de desintegração.
- **Top2Vec。**类似BERTopic的设计──社区较小但在某些基准上表现良好──
- **FASTopic。**更新,在超大语料上比BERTopic 快──
- **基于 LLM 的标注。**- Não. - Não. - Não.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-topic-picker.md`- Não .
> 保存为 `outputs/skill-topic-picker.md`- Não .

```markdown
---
name: topic-picker
description: Pick LDA or BERTopic for a corpus. Specify library, knobs, evaluation.
version: 1.0.0
phase: 5
lesson: 15
tags: [nlp, topic-modeling]
---

Given a corpus description (document count, avg length, domain, language, compute budget), output:

1. Algorithm. LDA / NMF / BERTopic / Top2Vec / FASTopic. One-sentence reason.
2. Configuration. Number of topics: `recommended = max(5, round(sqrt(n_docs)))`, clamped to 200 for corpora under 40,000 docs; permit >200 only when the corpus is genuinely large (>40k) and note the increased compute cost. `min_df` / `max_df` filters and embedding model for neural approaches also belong here.
3. Evaluation. Topic coherence (c_v) via `gensim.models.CoherenceModel`, topic diversity, and a 20-sample human read.
4. Failure mode to probe. For LDA, "junk topics" absorbing stopwords and frequent terms. For BERTopic, the -1 outlier cluster swallowing ambiguous documents.

Refuse BERTopic on documents longer than the embedding model's context window without a chunking strategy. Refuse LDA on very short text (tweets, reviews under 10 tokens) as coherence collapses. Flag any n_topics choice below 5 as likely wrong; flag >200 on corpora under 40k docs as likely over-splitting.
```

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 


## Exercícios.

1. **Easy.**Aplique LDA com 5 tópicos no conjunto de dados de 20 Newsgroups. Imprima as 10 principais palavras por tópico. Etiquete cada tópico à mão. O algoritmo encontrou as categorias reais?
2. **Medium.**Compare o número de tópicos encontrados, palavras principais e coerência qualitativa com a LDA. Qual superficia as categorias reais de forma mais limpa?
3. **Hard.**Calcule a coerência c_v para tanto LDA quanto BERTopic no seu corpus. Execute cada um com 5, 10, 20, 50 tópicos. Conserva a coerência versus a contagem de tópicos. Relate qual método é mais estável em todas as contagens de tópicos.
> 1. **简单。**Em 20 Newsgroups dados com 5 temas adequados LDA;. Imprimir cada tema top 10 palavras;.
2. **中等。**Em 20 Newsgroups, os mesmos grupos de notícias foram criados para o BERTopic.
3. **困难。**Em seu linguagem, calcular a LDA e o BERTopic de c_v 连贯度── separadamente com 5、10、20、50 题运行── desenhar a连贯度 vs.题数── relatar quais métodos em mudanças em número de temas são mais estáveis──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Topic | A thing the corpus is about | A probability distribution over words (LDA) or a cluster of similar documents (BERTopic). |
| Mixed membership | Doc is multiple topics | LDA assigns each document a distribution over all topics. |
| UMAP | Dimensionality reduction | Manifold learning that preserves local structure; used in BERTopic. |
| HDBSCAN | Density clustering | Finds variable-size clusters; produces "noise" label (-1) for outliers. |
| c_v coherence | Topic quality metric | Average pointwise mutual information of top topic words within sliding windows. |
> # O termo # Que as pessoas dizem # # O significado real #
|------|-----------|---------|
| 主题 | 语料关于的东西 | 词的概率分布（LDA）或相似文档的聚类（BERTopic）。 |
| 混合成员资格 | 文档是多个主题 | LDA 为每篇文档分配所有主题上的分布。 |
| UMAP | 降维 | 保留局部结构的流形学习；BERTopic 中使用。 |
| HDBSCAN | 密度聚类 | 找到变大小聚类；为离群值产生 "噪声" 标签（-1）。 |
| c_v 连贯度 | 主题质量指标 | 滑动窗口内顶级主题词的平均逐点互信息。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)- O artigo LDA.
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) o artigo BERTopic.
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf)O jornal que introduziu o C_V e os amigos.
- [BERTopic documentation](https://maartengr.github.io/BERTopic/)- a referência da produção.
> - [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) LDA 论文──
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) BERTópico 论文──
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) 引入 c_v 及相关标标的论文──
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) 生产参考──优秀示例──
