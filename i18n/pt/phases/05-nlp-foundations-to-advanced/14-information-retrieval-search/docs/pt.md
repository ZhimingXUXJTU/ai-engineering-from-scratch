# Recuperação de informações e pesquisa de informações e pesquisa.

> BM25 é preciso, mas frágil. Dense lança uma rede larga, mas falta palavras-chave. Hybrid é o padrão de 2026.
> BM25 精确但脆弱──密检索撒大网但漏掉关键词──混合检索是2026年默认选择──其余都是调参──

> **【中文解读】**A partir de palavras-chave correspondentes para pesquisa de volumes.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## O problema é o problema da introdução

O usuário digita "o que acontece se alguém mentiu para obter dinheiro" e espera encontrar o estatuto que realmente cobre isso: "Seção 420 IPC". Uma pesquisa de palavras-chave perde completamente (sem vocabulário compartilhado). Uma pesquisa semântica perde se os incorporados não foram treinados em texto legal.
> Users input "o que acontece se alguém mentiu para obter dinheiro" e não espera encontrar a cobertura real desse conteúdo de regulamentação:"Seção 420 IPC"――Keyword search完全找不到它(没有共享词汇)。

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.


A IR é o pipeline sob cada sistema RAG, cada barra de pesquisa, cada busca confusa do site do doc. A arquitetura de 2026 que funciona na produção não é um único método. É uma cadeia de métodos complementares, cada um capturando as falhas do anterior.
> O IR é cada sistema RAG, cada busca, cada ponto de arquivo, cada ponto de arquivo, cada ponto de arquivo, cada ponto de arquivo, cada um dos quais é um sistema de arquivo.

Esta lição constrói cada peça e nome que falha em cada captura.
> Esta aula construiu cada parte e indicou quais fracassos capturaram cada um.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


## O conceito central.

![Hybrid retrieval: BM25 + dense + RRF + cross-encoder rerank](../assets/retrieval.svg)
> ![混合检索：BM25 + 稠密 + RRF + 交叉编码器重排序](../assets/retrieval.svg)

Quatro camadas, escolha as que precisarem.
> Quatro níveis. Escolha o que precisas.

1. **Sparse retrieval (BM25).**Rapido, preciso em correspondências exatas, terrível em semântica, corre um índice invertido, sub-10ms por consulta em milhões de documentos, dá-lhe referências estatutárias, códigos de produto, mensagens de erro, entidades nomeadas corretas.
2. **Dense retrieval.**Encode query e documentos em vetores. Pesquisa vizinha mais próxima. Capta parafrases e semântica semelhança. Não há correspondências exatas de palavras-chave que diferem por um caracter. 50-200ms por consulta com FAISS ou um vector DB.
3. **Fusion.**Combine as listas classificadas de escassas e densas. A fusão de classificação recíproca (RRF) é a padrão fácil porque ignora as pontuações brutas (que vivem em diferentes escalas) e só usa posições de classificação. A fusão ponderada é uma opção quando você sabe que um sinal domina para seu domínio.
4. **Cross-encoder rerank.**Tome o top-30 da fusão. Execute um cross-encoder (query + document juntos, pontuação de cada par). Mantenha o top-5. Cross-encoders são mais lentos por par do que bi-encoders, mas muito mais precisos.
> 1. **稀疏检索（BM25）。**快速、精确匹配准确、语义上糟糕──在倒排索引上运行──百万档次上每查询亚 10毫秒──正确处理法规引用、产品代码、错误消息、命名实体──
2. **稠密检索。**A sua função é de criar um sistema de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de
3. **融合。**合并稀疏和密的排列列表──倒数排名融合(Reciprocal Rank Fusion, RRF) é uma escolha padrão simples, pois ignora o número inicial (existe em diferentes dimensões) apenas usando a posição de classificação── quando você sabe que um sinal na sua área domina, a fuso de potência é uma escolha──
4. **交叉编码器重排序。**A partir da integração, o top-30 foi retirado. A primeira parte do processo foi iniciada em outubro de 2008.

A recuperação em três vias (BM25 + densa + espaçamento aprendido como SPLADE) supera os dois caminhos em 2026 mas precisa de infraestrutura para índices de espaçamento aprendido.
> 三路检索(BM25 + 密 + 学习稀疏如SPLADE) em 2026 é melhor que os dois caminhos, mas precisa aprender infraestrutura de índice de raridade.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.


## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

```figure
gx-hybrid-retrieval
```

## Construí-lo

### Passo 1: BM25 a partir do zero
> ∆os parâmetros vale a pena entender`k1=1.5`控制词频和;更高 significa palavra repetida`b=0.75`控制长度归结;0 忽略文档长度,1 完全归结;;默认值是罗伯茨森原始论文中的推值,很少需要调整;;

```python
import math
import re
from collections import Counter

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text):
    return TOKEN_RE.findall(text.lower())


class BM25:
    def __init__(self, corpus, k1=1.5, b=0.75):
        if not corpus:
            raise ValueError("corpus must not be empty")
        self.corpus = [tokenize(d) for d in corpus]
        self.k1 = k1
        self.b = b
        self.n_docs = len(self.corpus)
        self.avg_dl = sum(len(d) for d in self.corpus) / self.n_docs
        self.df = Counter()
        for doc in self.corpus:
            for term in set(doc):
                self.df[term] += 1

    def idf(self, term):
        n = self.df.get(term, 0)
        return math.log(1 + (self.n_docs - n + 0.5) / (n + 0.5))

    def score(self, query, doc_idx):
        q_tokens = tokenize(query)
        doc = self.corpus[doc_idx]
        dl = len(doc)
        freq = Counter(doc)
        score = 0.0
        for term in q_tokens:
            f = freq.get(term, 0)
            if f == 0:
                continue
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * dl / self.avg_dl)
            score += self.idf(term) * numerator / denominator
        return score

    def rank(self, query, top_k=10):
        scored = [(self.score(query, i), i) for i in range(self.n_docs)]
        scored.sort(reverse=True)
        return scored[:top_k]
```

Dois parâmetros que vale a pena conhecer.`k1=1.5`O sistema de regulação de frequência de termo, que é mais elevado, significa mais peso na repetição do termo. `b=0.75`Os padrões padrão são as recomendações de Robertson do papel original e raramente precisam de sintonização.
> L2 归一化嵌入使点积等于余弦──`all-MiniLM-L6-v2`É 384 维, 快速, para a maioria dos inglês`paraphrase-multilingual-MiniLM-L12-v2` Taxa máxima de utilização`bge-large-en-v1.5`Ou `e5-large-v2`- Não.

### Passo 2: recuperação densa com um bi-encodador
> `k=60`常数来自原始RRF论文──更高的 `k`A contribuição de diferença de classificação varia em nível; menor `k`Utilize o seu valor de classificação.

```python
from sentence_transformers import SentenceTransformer
import numpy as np


def build_dense_index(corpus, model_id="sentence-transformers/all-MiniLM-L6-v2"):
    encoder = SentenceTransformer(model_id)
    embeddings = encoder.encode(corpus, normalize_embeddings=True)
    return encoder, embeddings


def dense_search(encoder, embeddings, query, top_k=10):
    q_emb = encoder.encode([query], normalize_embeddings=True)
    sims = (embeddings @ q_emb.T).flatten()
    order = np.argsort(-sims)[:top_k]
    return [(float(sims[i]), int(i)) for i in order]
```

L2-normalizar embebimentos para que o produto ponto é igual a cosino. `all-MiniLM-L6-v2`É 384 dim, rápido e forte o suficiente para a maioria da recuperação em inglês.`paraphrase-multilingual-MiniLM-L12-v2`Para a máxima precisão,`bge-large-en-v1.5`ou `e5-large-v2`- Não .
> O sistema de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados

### Passo 3: Fusão de Câncreas Reciprocas
> O sinal significa.
|------|------|
| Recall@k | 存在正确文档的查询中，正确文档在 top-k 中的比例 |
| MRR（平均倒数排名） | 第一个相关文档的 1/rank 的平均值 |
| nDCG@k | 考虑相关性分级，而非仅仅是二元的 相关/不相关 |

```python
def reciprocal_rank_fusion(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, (_, doc_idx) in enumerate(ranking):
            scores[doc_idx] = scores.get(doc_idx, 0.0) + 1.0 / (k + rank + 1)
    fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(score, doc_idx) for doc_idx, score in fused]
```

O `k=60`A constante vem do papel original RRF.`k`A redução da contribuição das diferenças de grau;`k`60 é o padrão publicado e raramente precisa de sintonização.
> ), em especial, para os RAG, os**Recall@k**Se o segmento correto não estiver em busca, o leitor não pode responder.

### Passo 4: Busca híbrida + re-ranqueamento
> 调试技巧:对于失败的查询,对比稀疏和密排名──如果一个找到正确文档而另一个没有,你有词汇不匹配 (如果你找到正确文档而另一个没有,你有词汇不匹配)

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def hybrid_search(query, bm25, encoder, dense_embeddings, corpus, top_k=5, pool_size=30, reranker=reranker):
    sparse_ranking = bm25.rank(query, top_k=pool_size)
    dense_ranking = dense_search(encoder, dense_embeddings, query, top_k=pool_size)
    fused = reciprocal_rank_fusion([sparse_ranking, dense_ranking])[:pool_size]

    pairs = [(query, corpus[doc_idx]) for _, doc_idx in fused]
    scores = reranker.predict(pairs)
    reranked = sorted(zip(scores, [doc_idx for _, doc_idx in fused]), reverse=True)
    return reranked[:top_k]
```

BM25 encontra correspondências léxicas. Denso encontra correspondências semânticas. RRF combina as duas classificações sem precisar de calibração de pontuação. Cross-encoder recorre ao top-30 usando pares de documentos de consulta juntos, o que capta a relevância de grãos finos que o bi-encoder perdeu. Mantenha o top-5.

### Passo 5: Avaliação

| Metric | Meaning |
|--------|---------|
| Recall@k | Of queries where the correct document exists, how often is it in the top-k? |
| MRR (Mean Reciprocal Rank) | Average of 1/rank of first relevant document. |
| nDCG@k | Accounts for relevance gradations, not just binary relevant/not. |

Para o RAG especificamente, **Recall@k**O seu leitor não pode responder se a passagem correta não estiver no conjunto recuperado.

Dica de defeito: para consultas falhadas, diferencie as classificações escassas e densas. Se um encontra o documento certo e o outro não, você tem um desajuste de vocabulário (fixado: adicionar a metade faltante) ou uma ambigüidade semântica (fixado: melhores inserções ou um re-ranqueador).


> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


A pilha de 2026:
> 2026  

| Scale | Stack |
|-------|-------|
| 1k-100k docs | In-memory BM25 + `all-MiniLM-L6-v2` embeddings + RRF. No separate DB. |
| 100k-10M docs | FAISS or pgvector for dense + Elasticsearch / OpenSearch for BM25. Run in parallel. |
| 10M+ docs | Qdrant / Weaviate / Vespa / Milvus with hybrid support. Cross-encoder rerank on top-30. |
| Best-quality frontier | Three-way (BM25 + dense + SPLADE) + ColBERT late-interaction reranking |
> ♪ A escala, a tecnologia ♪
|------|--------|
| 1k-100k 文档 | 内存中 BM25 + `all-MiniLM-L6-v2` 嵌入 + RRF。无需独立数据库。 |
| 100k-10M 文档 | FAISS 或 pgvector 做稠密 + Elasticsearch / OpenSearch 做 BM25。并行运行。 |
| 10M+ 文档 | Qdrant / Weaviate / Vespa / Milvus 配混合支持。交叉编码器重排序 top-30。 |
| 最高质量前沿 | 三路（BM25 + 稠密 + SPLADE）+ ColBERT 后期交互重排序 |

Qualquer que seja o seu orçamento para avaliação. Recall de recuperação de benchmark antes de comparar a precisão de RAG de ponta a ponta. Um leitor não pode corrigir o que o retriever perdeu.
> O que quer que escolha, deve ser feito para avaliar o orçamento.

### As lições duramente obtidas da produção RAG de 2026
> - **80% 的 RAG 失败追溯到摄取和分块，而不是模型。**O grupo passou algumas semanas trocando LLM e advertências, enquanto o exame de cada três vezes de consulta foi feito em uma posição de segurança.
- **分块策略比分块大小更重要。**固定大小分割会破坏表格、代码和嵌套标题──句子感知是默认选择;语义或基于LLM分块在技术文档和产品手册有回报──
- **父文档模式。**检索小的"子"块以获得精度──当同一节的多子块出现时,换进父块以保留下文──这持续提升答案质量而无需重新训练──
- **k_rerank=3 通常最优。**Cada aumento de um bloco acima desse número aumenta o token, a produção e o atraso de produção não aumentam a qualidade da resposta.
- **HyDE / 查询扩展。**A partir de uma consulta, gerar hipóteses de resposta, embuchar-se nela, pesquisar.
- **上下文预算控制在 8K token 以下。**Na esta restrição, o sucesso significa que o sistema de reorganização é muito fácil.
- **版本化一切。**提示、分块规则、嵌入模型、重排序器──任何漂移都会静默破坏答案质量──忠诚度、上下文精确率和未回答问题率 关键控在用户看到之前阻止回归──
- **三路检索（BM25 + 稠密 + 学习稀疏如 SPLADE）在 2026 年基准上优于两路**, especialmente os inquéritos de mixto e significado.

- **80% of RAG failures trace to ingestion and chunking, not the model.**As equipes passam semanas trocando LLM e sintonizando as instruções enquanto a recuperação retorna silenciosamente o contexto errado a cada terceira consulta.
- **Chunking strategy matters more than chunk size.**As divisões de tamanho fixo quebram tabelas, código e cabeçalhos aninhados. Sentence-aware é o padrão; o chunking semântico ou baseado em LLM compensa os documentos técnicos e manuais de produtos.
- **Parent-doc pattern.**Retire pequenos pedaços de "criança" para precisão. Quando vários filhos da mesma seção dos pais aparecem, troque no bloco dos pais para preservar o contexto. Isso aumenta consistentemente a qualidade da resposta sem reformulação.
- **k_rerank=3 is usually optimal.**Cada pedaço extra passado que adiciona custo de token e latência de geração sem aumentar a qualidade da resposta.
- **HyDE / query expansion.**Gerenciar uma resposta hipotética da consulta, incorporar, recuperar. Prepara a lacuna de frase entre perguntas curtas e documentos longos.
- **Context budget under 8K tokens.**Os ataques consistentes nesse limite significam que o limiar de re-ranqueamento é muito solto.
- **Version everything.**Instruções, regras de fragmentação, modelo de inserção, re-ranqueador. Qualquer deriva quebra silenciosamente a qualidade da resposta. Portas de CI sobre fidelidade, precisão de contexto e taxa de perguntas sem resposta bloqueiam regressões antes que os usuários as vejam.
- **Three-way retrieval (BM25 + dense + learned-sparse like SPLADE) outperforms two-way**Em 2026 as referências são utilizadas, especialmente para consultas que misturam substantivos adequados com semântica.
> De acordo com as medições do setor de 2026, o design de inspeção correta reduz o 70-90% das imagens. A maioria dos RAGs aumentam o desempenho de inspeção melhor, e não de modelagem reduzida.

O design adequado de recuperação reduz as alucinações em 70-90% de acordo com medições da indústria de 2026.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-retrieval-picker.md`- Não .
> 保存为 `outputs/skill-retrieval-picker.md`- Não .

```markdown
---
name: retrieval-picker
description: Pick a retrieval stack for a given corpus and query pattern.
version: 1.0.0
phase: 5
lesson: 14
tags: [nlp, retrieval, rag, search]
---

Given requirements (corpus size, query pattern, latency budget, quality bar, infra constraints), output:

1. Stack. BM25 only, dense only, hybrid (BM25 + dense + RRF), hybrid + cross-encoder rerank, or three-way (BM25 + dense + learned-sparse).
2. Dense encoder. Name the specific model. Match to language(s), domain, and context length.
3. Reranker. Name the specific cross-encoder model if used. Flag that rerank adds 30-100ms latency on top-30.
4. Evaluation plan. Recall@10 is the primary retriever metric. MRR for multi-answer. Baseline first, incremental improvements measured against it.

Refuse to recommend dense-only for corpora with named entities, error codes, or product SKUs unless the user has evidence dense handles exact matches. Refuse to skip reranking for high-stakes retrieval (legal, medical) where the final top-5 decides the user's answer.
```

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 


## Exercícios.

1. **Easy.**Implementação `hybrid_search`Comparar recall em 5 entre BM25-somente, denso-somente e híbrido.
2. **Medium.**Adicione o cálculo do MRR. Para cada consulta de teste com um documento correto conhecido, encontre a classificação do documento correto em BM25, classificados denso e híbrido.
3. **Hard.**Fecha uma sintonia de um codificador denso no seu domínio usando MultipleNegativesRankingLoss (Sentence Transformers). Construa um conjunto de treinamento a partir de 500 pares de documentos de consulta. Comparar a recall de pré e pós-fine-tune.
> 1. **简单。**Em 500 文档语料 `hybrid_search`△测试 20 个查询──比较 BM25-only、density-only 和混合的回忆@5──
2. **中等。**Para cada consulta de teste de documentos verdadeiros conhecidos, encontre os documentos verdadeiros em posição entre BM25 密和混合排名.
3. **困难。**Utilize MultipleNegativesRankingLoss(Sentence Transformers) em seu campo de pesquisa, de 500 consultas-documentos para a construção de um conjunto de treinamentos, de comparação, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa e de pesquisa, de pesquisa, de pesquisa e de pesquisa, de pesquisa e de pesquisa, de pesquisa e de pesquisa, de pesquisa e de pesquisa, de pesquisa e de pesquisa, de pesquisa e de pesquisa, de pesquisa, de pesquisa e de pesquisa, de pesquisa, de pesquisa e de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, e de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, de pesquisa, em 2011.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BM25 | Keyword search | Okapi BM25. Scores documents by term frequency, IDF, and length. |
| Dense retrieval | Vector search | Encode query + doc into vectors, find nearest neighbors. |
| Bi-encoder | Embedding model | Encodes query and doc independently. Fast at query time. |
| Cross-encoder | Reranker model | Encodes query + doc together. Slow but accurate. |
| RRF | Rank fusion | Combine two rankings by summing `1/(k + rank)`. |
| Recall@k | Retrieval metric | Fraction of queries where a relevant doc is in the top-k. |
> # O termo # Que as pessoas dizem # # O significado real #
|------|-----------|---------|
| BM25 | 关键词搜索 | Okapi BM25。按词频、IDF 和长度为文档打分。 |
| 稠密检索 | 向量搜索 | 将查询 + 文档编码为向量，找最近邻。 |
| 双编码器 | 嵌入模型 | 独立编码查询和文档。查询时快速。 |
| 交叉编码器 | 重排序模型 | 一起编码查询 + 文档。慢但准确。 |
| RRF | 排名融合 | 通过对 `1/(k + rank)` 求和合并两个排名。 |
| Recall@k | 检索指标 | 相关文档在 top-k 中的查询比例。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) o tratamento definitivo do BM25.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906)DPR, o bi-encodador canônico.
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720)O retriever de espaços aprendidos que fecha a lacuna com denso.
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)Papel RRF.
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) Retorno de interação tardia.
> - [Robertson and Zaragoza (2009). The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) 权威的BM25 处理──
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, clásico dobê编码器──
- [Formal et al. (2021). SPLADE: Sparse Lexical and Expansion Model](https://arxiv.org/abs/2107.05720)                                                                                                                                                                                                                                                              
- [Cormack, Clarke, Büttcher (2009). Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) RRF 论文──
- [Khattab and Zaharia (2020). ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832) 后期交互检索──
