# Sistemas de Resposta a Perguntas.

> Três sistemas formaram a moderna QA. Extractiva encontrou intervalos. A recuperação aumentou-los em documentos. Gerativo produziu respostas. Cada assistente de IA moderno é uma mistura dos três.
> Três sistemas moldaram a resposta moderna. Três sistemas moldaram a resposta moderna.

> **【中文解读】**A RAC é um sistema de perguntas e respostas.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 11 (Machine Translation), Phase 5 · 10 (Attention Mechanism) | **前置知识:** Phase 5 · 11 (Machine Translation), Phase 5 · 10 (Attention Mechanism)
**Time:** ~75 minutes | **时间:** ~75 minutes


## O problema é o problema da introdução

Um usuário digita "Quando foi lançado o primeiro iPhone?" e espera "29 de junho de 2007". Não "A história da Apple é longa e variada". Não "2007" sentado isolado sem frase. Uma resposta direta, fundamentada e correta.
> Usuário: User输入 "Quando foi lançado o primeiro iPhone?" 并期望得到 "Jun 29, 2007."──不是"Apple's history is long and varied".──不是孤立的"2007" 没有句子上下文──一个直接、有据可依、正确的答案──

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.


Três arquiteturas dominaram a QA na última década.
> Na década passada, três arquiteturas dominaram a questão-resposta.

- **Extractive QA.**Dado uma pergunta e uma passagem que contém a resposta, encontre os índices de início e fim do intervalo de respostas na passagem.
- **Open-domain QA.**A passagem não é dada. Retira a passagem relevante primeiro, depois extrai ou gera uma resposta. Esta é a base de cada oleoduto RAG hoje.
- **Generative / Closed-book QA.**Um modelo de linguagem grande responde a partir de sua memória paramétrica, sem recuperação, mais rápido na inferência, menos confiável nos fatos.
> - **抽取式问答（Extractive QA）。**Dada uma questão e um fragmento de resposta conhecida, encontrar a resposta no início e fim do fragmento SquAD é um clássico 
- **开放域问答（Open-domain QA）。**段落未给定──先检查相关段落,然后抽取或生成答案── é hoje a pedra fundamental de cada RAG 流水线──
- **生成式/闭卷问答（Generative / Closed-book QA）。**O modelo de grande linguagem respondeu em memória parametricada.

A tendência em 2026 é híbrida: recuperar as melhores passagens, em seguida, pedir um modelo gerativo para responder baseado nessas passagens.
> A tendência de 2026 é misturada: pesquisar os melhores fragmentos, e então sugerir que os modelos sejam gerados com base nesses fragmentos.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![QA architectures: extractive, retrieval-augmented, generative](../assets/qa.svg)
> ![问答架构：抽取式、检索增强、生成式](../assets/qa.svg)

**Extractive.**Encode a pergunta e a passagem juntamente com um transformador (família BERT). Treine duas cabeças que preveem índices de token de início e fim da resposta. A perda é entropia cruzada sobre posições válidas. A saída é um espaço de tempo da passagem. Nunca alucina (por construção), nunca lida com perguntas que a passagem não pode responder (por construção).
> **抽取式。**Usador ([[BERT 系列]])                                                                                                                                                                                                                                                          

**Retrieval-augmented (RAG).**Primeiro, um retriever encontra o topo...`k`O sistema de retriever-reader permite que cada um seja treinado e avaliado de forma independente.
> **检索增强（RAG）。**Primeiro, o pesquisador encontra o topo da caixa de linguagem.`k`段落──二,阅读器(抽取式或生成式) utiliza estes fragmentos para produzir respostas──检索器-阅读器分离允许各自独立训练和评估──现代RAG normalmente entre ambos adiciona o seu próprio repertório──

**Generative.**Um LLM apenas para decodificadores (GPT, Claude, Llama) responde a partir de pesos aprendidos. Não há etapa de recuperação. Excelente em conhecimento comum, catastrófico em fatos raros ou recentes. A taxa de alucinação está inversamente correlacionada com a frequência de fatos nos dados pré-treino.
> **生成式。**仅解码器的 LLM(GPT、Claude、Llama) da pesada de aprendizagem responder.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.


## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

```figure
qa-span
```

## Construí-lo

### Passo 1: AQ extractiva com um modelo pré-treinado
> `deepset/roberta-base-squad2`Em SQuAD 2.0 上 training, contém questões não respondidas.`question-answering`流水线返回最高分分的片段,即使模型的空分数胜出它不自动返回空答案──要获得明显的"无答案"行为,在流水线调调中传入 流水线返回最高分的片段,即使模型的空分数胜出它不自动返回空答案── para obter um comportamento evidente de "无答案", em que o modelo não consegue obter o maior número de respostas.`handle_impossible_answer=True`A linha de água só está em espaço, excede todos os segmentos de espaço.`score`- Não.

```python
from transformers import pipeline

qa = pipeline("question-answering", model="deepset/roberta-base-squad2")

passage = (
    "Apple Inc. released the first iPhone on June 29, 2007. "
    "The device was announced by Steve Jobs at Macworld in January 2007."
)
question = "When was the first iPhone released?"

answer = qa(question=question, context=passage)
print(answer)
```

```python
{'score': 0.98, 'start': 57, 'end': 70, 'answer': 'June 29, 2007'}
```

`deepset/roberta-base-squad2`O programa de formação é formado no SQuAD 2.0, que inclui perguntas sem resposta.`question-answering`O pipeline retorna o período de pontuação mais alto mesmo quando o resultado zero do modelo ganha.`handle_impossible_answer=True`para a chamada de pipeline: a pipeline retorna uma resposta vazia apenas quando a pontuação nula excede todas as pontuações de tempo.`score`campo de qualquer maneira.
> 两段流水线──密检索器(Sentence-BERT) através de linguagem semelhança encontrar os segmentos relacionados──抽取式阅读器(RoBERTa-SquAD) de cima da combinação 段落中提取答案片段── é aplicável a pequenos materiais de linguagem── para milhões de classes de documentos de linguagem, usando FAISS ou向量数据库──

### Passo 2: um gasoduto aumentado de recuperação (esquema)
> 提示模式很重要──显然告诉模型基于上下文答复和上下文不足时回复"Eu não sei",相比简单提示将幻觉率降低40%-60%──更精细的模式添加引用、信任分数和结构化抽取──

```python
from sentence_transformers import SentenceTransformer
import numpy as np

encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

corpus = [
    "Apple Inc. released the first iPhone on June 29, 2007.",
    "Macworld 2007 featured the iPhone announcement by Steve Jobs.",
    "Android launched in 2008 as Google's mobile operating system.",
    "The first iPod was released in 2001.",
]
corpus_embeddings = encoder.encode(corpus, normalize_embeddings=True)


def retrieve(question, top_k=2):
    q_emb = encoder.encode([question], normalize_embeddings=True)
    sims = (corpus_embeddings @ q_emb.T).squeeze()
    order = np.argsort(-sims)[:top_k]
    return [corpus[i] for i in order]


def answer(question):
    passages = retrieve(question, top_k=2)
    combined = " ".join(passages)
    return qa(question=question, context=combined)


print(answer("When was the first iPhone released?"))
```

Duas etapas de pipeline. O Density Retriever (Sentence-BERT) encontra passagens relevantes por semântica semelhança. O leitor extractivo (RoBERTa-SQuAD) tira o intervalo de resposta das passagens superiores combinadas. Trabalha em pequenos corpos. Para um corpus de um milhão de documentos, use FAISS ou um banco de dados vetorial.
> SQUAD Usar**精确匹配（Exact Match, EM）**和 **token 级 F1**◦ EM é o rigoroso correspondência após a regeneração ([[小写、除标点、除冠词]]) 预测要么精确匹配,要么要么要么要么要么要么要么 0。 F1 在预测和参考的代币重叠上计算,给部分分──两者都低估释义:"29 de junho de 2007" vs "29 de junho de 2007" normalmente 0 EM(序数词破坏归化) mas ainda de sobreposição de token 获得可观的F1──

### Passo 3: gerador com RAG
> 对于生产问答:

```python
def rag_generate(question, llm):
    passages = retrieve(question, top_k=3)
    prompt = f"""Context:
{chr(10).join('- ' + p for p in passages)}

Question: {question}

Answer using only the context above. If the context does not contain the answer, say "I don't know."
"""
    return llm(prompt)
```

O padrão de prompt importa. Dizer explicitamente ao modelo que ele esteja no contexto e retornar "não sei" quando o contexto é insuficiente reduz as taxas de alucinação em 40-60% em comparação com o prompting ingênuo. Padrões mais elaborados adicionam citações, pontuações de confiança e extração estruturada.
> - **答案准确率**(LLM 评判或人工评判,因为指标不捕获语义等价)
- **引用准确率。**引用的段落是实际支持答案吗? 引用和检索段落之间的字符串匹配即可轻松自动检查── é fácilmente possível verificar automaticamente
- **拒绝校准。**Quando a resposta não está no intervalo, o sistema diz "não sei"?
- **检索召回率。**Antes do leitor de avaliação, o pesquisador de medição vai colocar o seu...`k`Não posso reparar o que faltou.

### Passo 4: Avaliação que reflita o mundo real
> `RAGAS`专为RAG 系统构建,是2026年发布默认选择――它在不需要黄金参考的情况下从四维度评分:

Utilizações do SQuAD **Exact Match (EM)**E ...**token-level F1**- Não . EM é uma correspondência rigorosa após a normalização (minuscript, puntuação de tira, remover artigos)  ou a previsão coincide exatamente ou marca 0. A F1 é calculada sobre a sobreposição de tokens entre previsão e referência e dá crédito parcial. Ambas as paráfrases de baixo crédito: "29 de junho de 2007" vs "29 de junho de 2007" normalmente obtém 0 EM (a normalização das interrupções ordinárias), mas ainda ganha uma F1 substancial a partir de tokens sobrepostos.
> - **忠实度（Faithfulness）。**Cada declaração na resposta é proveniente da pesquisa? através de uma medição de relação baseada em NLI.
- **答案相关性。**答案是否回应了问题? 答案生成假设问题并与真题相比较来测量── através da resposta gerada por hipóteses do problema e da realidade.
- **上下文精确率。**检索的块中, há quantas realmente estão relacionadas?
- **上下文召回率。**检索集是否包含所有需要的信息?低召回率 = 阅读器无法成功──

Para a produção QA:
>  avaliações sem referência  permite que você possa avaliar o fluxo de produção em tempo real, sem necessidade de planejar a resposta  em um determinado índice de correspondência  sobre a questão de um código aberto sem uso 

- **Answer accuracy**(Judicado pela MLL ou por humanos, uma vez que as métricas não capturam equivalência semântica).
- **Citation accuracy.**É trivial verificar automaticamente com a correspondência de cordas entre citações geradas e passagens recuperadas.
- **Refusal calibration.**Quando a resposta não está nas passagens recuperadas, o sistema diz corretamente "Não sei"?
- **Retrieval recall.**Antes de avaliar o leitor, medir se o retriever consegue a passagem certa para o topo...`k`Um leitor não pode consertar uma passagem faltante.
> `pip install ragas`△ Conectar seu revisor + 阅读器── cada consulta obtém quatro caracteres──

### RAGAS: o quadro de avaliação da produção de 2026

`RAGAS`É especialmente construído para sistemas RAG e é o padrão de transporte em 2026.

- **Faithfulness.**Cada afirmação da resposta vem do contexto recuperado? Medido por implicação baseada em NLI.
- **Answer relevance.**A resposta responde à pergunta? Medida gerando perguntas hipotéticas da resposta e comparando com a pergunta real.
- **Context precision.**Dos pedaços recuperados, qual fração era realmente relevante?
- **Context recall.**O conjunto recuperado continha todas as informações necessárias?

A pontuação sem referências permite que você avalia o tráfego de produção ao vivo sem respostas de ouro.

`pip install ragas`Conecte o retriever + leitor, obtém quatro escalares por consulta, alerta de regressões.

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

A pilha de 2026.
> 2026 年技术──

| Use case | Recommended |
|---------|-------------|
| Given passage, find answer span | `deepset/roberta-base-squad2` |
| Over a fixed corpus, closed-book not acceptable | RAG: dense retriever + LLM reader |
| Real-time over a document store | RAG with hybrid (BM25 + dense) retriever + reranker (lesson 14) |
| Conversational QA (follow-up questions) | LLM with conversation history + RAG on each turn |
| Highly factual, regulated domains | Extractive over an authoritative corpus; never generative alone |
> ♪ Usar a cena ♪
|---------|------|
| 给定段落，找答案片段 | `deepset/roberta-base-squad2` |
| 固定语料上，闭卷不可接受 | RAG：稠密检索器 + LLM 阅读器 |
| 实时文档存储 | RAG 配混合（BM25 + 稠密）检索器 + 重排序器（第 14 课） |
| 对话式问答（追问） | 带对话历史的 LLM + 每轮 RAG |
| 高度事实性、受监管领域 | 在权威语料上的抽取式；永远不要单独用生成式 |

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


A AQ extractiva é des moda em 2026 porque a RAG com LLM lida com mais casos.
> A estratégia de perguntas e respostas não é muito popular em 2026, pois o RAG do LLM lida com mais situações.


## Envia-o . Produto .

Salva como`outputs/skill-qa-architect.md`- Não .
> 保存为 `outputs/skill-qa-architect.md`- Não .

```markdown
---
name: qa-architect
description: Choose QA architecture, retrieval strategy, and evaluation plan.
version: 1.0.0
phase: 5
lesson: 13
tags: [nlp, qa, rag]
---

Given requirements (corpus size, question type, factuality constraint, latency budget), output:

1. Architecture. Extractive, RAG with extractive reader, RAG with generative reader, or closed-book LLM. One-sentence reason.
2. Retriever. None, BM25, dense (name the encoder), or hybrid.
3. Reader. SQuAD-tuned model, LLM by name, or "domain-fine-tuned DistilBERT."
4. Evaluation. EM + F1 for extractive benchmarks; answer accuracy + citation accuracy + refusal calibration for production. Name what you are measuring and how you are measuring it.

Refuse closed-book LLM answers for regulatory or compliance-sensitive questions. Refuse any QA system without a retrieval-recall baseline (you cannot evaluate the reader without knowing the retriever surfaced the right passage). Flag questions that require multi-hop reasoning as needing specialized multi-hop retrievers like HotpotQA-trained systems.
```

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 


## Exercícios.

1. **Easy.**Configure o pipeline extractivo SQuAD acima em 10 passagens da Wikipédia. 10 perguntas artesanas. Messa com que frequência a resposta é correta. Você deve ver 7-9 correta se passagens e perguntas são limpas.
2. **Medium.**Adicione um classificador de recusa. Quando a pontuação de recuperação superior estiver abaixo de um limiar (digamos 0,3 cosinos), retorne "Não sei" em vez de ligar ao leitor.
3. **Hard.**Construir um pipeline RAG sobre um corpus de 10.000 documentos de sua escolha. Implementar a recuperação híbrida (BM25 + densa) com fusão RRF (ver lição 14).
> 1. **简单。**Em 10 篇维基百科段落上设置上述 SQuAD 抽取式流线――手工设计 10 问题――测量答案正确率――如果段落和问题干净,你应该看到7-9 个正确――
2. **中等。**Quando o máximo de pesquisas é inferior ao 值 (por exemplo, 0,3 余弦), retorne "Eu não sei" em vez de usar o leitor.
3. **困难。**Em sua seleção, construção de 10.000 文档语料 RAG 流水线――实现混合检索(BM25 + 密)加 RRF 融合(见第 14 课) ――测量有和没有混合步骤的答案准确率──记录哪些问题类型受益最大──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive QA | Find the answer span | Predict start and end indices of the answer within a given passage. |
| Open-domain QA | QA over a corpus | No given passage; must retrieve then answer. |
| RAG | Retrieve then generate | Retrieval-augmented generation. Retriever + reader pipeline. |
| SQuAD | Canonical benchmark | Stanford Question Answering Dataset. EM + F1 metrics. |
| Hallucination | Made-up answer | Reader output not supported by retrieved context. |
| Refusal calibration | Know when to shut up | System correctly says "I don't know" when unable to answer. |
> # O termo # Que as pessoas dizem # # O significado real #
|------|-----------|---------|
| 抽取式问答 | 找答案片段 | 预测给定段落中答案的起始和结束索引。 |
| 开放域问答 | 语料上的问答 | 无给定段落；必须先检索再回答。 |
| RAG | 检索再生成 | 检索增强生成。检索器 + 阅读器流水线。 |
| SQuAD | 经典基准 | 斯坦福问答数据集。EM + F1 指标。 |
| 幻觉 | 编造答案 | 阅读器输出不被检索上下文支持。 |
| 拒绝校准 | 知道何时闭嘴 | 系统在无法回答时正确地说 "I don't know"。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) o documento de referência.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906)DPR, o retriever canônico denso para QA.
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)O jornal que chamava RAG.
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997) Pesquisa abrangente do RAG.
> - [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) 基准论文──
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR, 问答的经典密检索器──
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) 命名 RAG 的论文──
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997) 综合 RAG 综述──
