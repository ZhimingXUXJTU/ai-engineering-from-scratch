# Resumo do texto 文本摘要

> Os sistemas de extracção dizem o que o documento disse, os sistemas abstractos dizem o que o autor queria dizer, diferentes tarefas, diferentes armadilhas.
> O sistema de produção diz o que o autor quer dizer.

> **【中文解读】**抽取式 vs 生成式摘要──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation)
**Time:** ~75 minutes | **时间:** ~75 minutes


## O problema é o problema da introdução

Um artigo de notícias de 2.000 palavras chega ao seu feed. Você precisa de 120 palavras que o capturem. Você pode escolher as três frases mais importantes do artigo (extrativa) ou reescrever o conteúdo em suas próprias palavras (abstrativa). Ambos são chamados de resumo.
> Um artigo de 2000 palavras de jornal aparece no seu fluxo de informação. Você precisa de 120 palavras para generalizar. Você pode escolher entre os artigos as três frases mais importantes (extração), ou reescrever o conteúdo (produzir) em seu próprio texto.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.


A resumo extractivo é um problema de classificação.`k`O resultado é sempre gramatical porque é levantado literalmente. O risco é a falta de conteúdo que é distribuído em todo o artigo.
> 抽取式摘要是一个排序问题.`k`O resultado é sempre conforme o linguagem, pois é extraído de cada letra.

A resumo abstrato é um problema de geração. Um transformador produz um novo texto condicionado à entrada. A saída é fluente e compressora, mas pode alucinar fatos que não estavam na fonte. O risco é a fabricação confiante.
> O processo de produção é um problema de produção. O transformador é um processo de produção de texto novo.

Esta lição constrói os dois, com o modo de falha de cada um.
> O estudo foi realizado em uma área de estudos de ciências da saúde.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


## O conceito central.

![Extractive TextRank vs abstractive transformer](../assets/summarization.svg)
> ![抽取式 TextRank vs 生成式 Transformer](../assets/summarization.svg)

**Extractive.**Trate o artigo como um gráfico onde os nós são frases e as bordas são semelhanças. Exerça PageRank (ou algo parecido) sobre o gráfico para marcar frases por como elas estão conectadas a tudo o resto.**TextRank**(Mihalcea e Tarau, 2004).
> **抽取式（Extractive）。**Quando um artigo é visualizado, um ponto é uma frase, um lado é uma semelhança.**TextRank**(Mihalcea e Tarau, 2004):

**Abstractive.**Afinal, o modelo lê o documento e gera o resumo token-by-token através da atenção cruzada.
> **生成式（Abstractive）。**Em seu livro, o autor escreve um texto sobre o que é um livro de ficção, que é um livro de ficção científica.

Avaliação com **ROUGE**(Recall-Oriented Understudy for Gisting Evaluation). ROUGE-1 e ROUGE-2 pontuação unigrama e bigrama se sobrepõem. ROUGE-L pontuação mais longa subsequência comum. Mais alto é melhor, mas 40 ROUGE-L é "bom" e 50 é "excepcional".`rouge-score`- O pacote.
> Utilização **ROUGE**(Recall-Oriented Understudy for Gisting Evaluation) 评估──ROUGE-1 和 ROUGE-2 评分一元组和二元组重叠──ROUGE-L 评分最长公共子序列──越高越好,但40 ROUGE-L 是"好",50 是"出色"──每篇论文都报告全部三个──使用`rouge-score`- Não.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.


## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

```figure
summarize-collapse
```

## Construí-lo

### Passo 1: TextRank (extração)
> 两件事值得注意──相似度函数使用对数归结的词重叠,这是原始 TextRank的变体──TF-IDF 向量的余弦相似度也行──阻尼因子 0.85 和代次数是PageRank的默认值──

```python
import math
import re
from collections import Counter


def sentence_split(text):
    return re.split(r"(?<=[.!?])\s+", text.strip())


def similarity(s1, s2):
    w1 = Counter(s1.lower().split())
    w2 = Counter(s2.lower().split())
    intersection = sum((w1 & w2).values())
    denom = math.log(len(w1) + 1) + math.log(len(w2) + 1)
    if denom == 0:
        return 0.0
    return intersection / denom


def textrank(text, top_k=3, damping=0.85, iterations=50, epsilon=1e-4):
    sentences = sentence_split(text)
    n = len(sentences)
    if n <= top_k:
        return sentences

    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                sim[i][j] = similarity(sentences[i], sentences[j])

    scores = [1.0] * n
    for _ in range(iterations):
        new_scores = [1 - damping] * n
        for i in range(n):
            total_out = sum(sim[i]) or 1e-9
            for j in range(n):
                if sim[i][j] > 0:
                    new_scores[j] += damping * sim[i][j] / total_out * scores[i]
        if max(abs(s - ns) for s, ns in zip(scores, new_scores)) < epsilon:
            scores = new_scores
            break
        scores = new_scores

    ranked = sorted(range(n), key=lambda k: scores[k], reverse=True)[:top_k]
    ranked.sort()
    return [sentences[i] for i in ranked]
```

Duas coisas que vale a pena nomear. A função de semelhança usa sobreposição de palavras normalizadas de log, que é a variante original do TextRank.
> BART-large-CNN em CNN/DailyMail 语料上微调──开箱即即用产生新闻风格摘要── para outros domínios, usando o Pegasus 检查点应应或在目标数据上微调──

### Passo 2: abstracto com BART
> 始终使用词干提取──没有它, "running" 和 "run" 被视为不同的词,ROUGE 会低估──

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

article = """(long news article text)"""

summary = summarizer(article, max_length=120, min_length=60, do_sample=False)
print(summary[0]["summary_text"])
```

O BART-large-CNN é ajustado no corpus da CNN/DailyMail. Ele produz resumos de estilo de notícias fora da caixa. Para outros domínios (revistas científicas, diálogo, jurídico), use o ponto de verificação Pegasus correspondente ou ajuste os dados de seu alvo.
> ROUGE, que há vinte anos é o principal indicador de resumo, mas em 2026 já não é suficiente.

### Passo 3: Avaliação ROUGE
> - **BERTScore**(上下文嵌入相似度) ganhou atenção em 2023, agora a maioria dos resumos dos artigos estão relacionados com o ROUGE 一起报告──
- **BARTScore**A avaliação será feita através do treinamento prévio BART                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
- **MoverScore**(sobre a linha de base) alcançar o topo no cenário de resumo de 2025, porque é melhor capturar a tradução do que o ROUGE.
- **FactCC**和**基于 QA 的事实性检查**Em 2021-2023 anos muito comum, agora normalmente são **G-Eval**(uma forma de GPT-4 提示链, usando a corrente de pensamento para avaliar a conexão, a concordância, a relação e a relação)
- **G-Eval**E o método de avaliação de LLM similar é 80% de acordo com o julgamento humano quando o critério é bem concebido.

```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
scores = scorer.score(reference_summary, generated_summary)
print({k: round(v.fmeasure, 3) for k, v in scores.items()})
```

Sem ele, "correr" e "correr" contam como palavras diferentes e o ROUGE contam em baixo.
> Produção de recomendações: relatório ROUGE-L Usado para comparação de legados, BERTScore Usado para gramática sobreposição, G-Eval Usado para coerência e factualidade.

### Além do ROUGE (2026 avaliação de resumo)
> O risco de extração de resumos é muito menor, pois a saída é extraída de forma gradual da fonte, embora se as frases de origem forem separadas da seguinte, o tempo ou a ordem de citação, elas ainda podem ser erradas. Esta é a principal razão pela qual os sistemas de produção ainda preferem o método de extração em conteúdo de conformidade.

A ROUGE tem sido a métrica de resumo dominante há vinte anos e é insuficiente por si só em 2026.
> 需要命名的幻觉类型:

- **BERTScore**(similidade de inserção contextual) ganhou terreno até 2023 e é agora relatado ao lado de ROUGE na maioria dos documentos de resumo.
- **BARTScore**Tratar a avaliação como uma geração: avaliar o resumo com base na probabilidade de um BART pré-treinado atribuí-lo dada a fonte.
- **MoverScore**(Distança do Mover da Terra sobre embebimentos contextuais) alcançou o primeiro lugar em 2025 referências de resumo porque capta sobreposição semântica melhor do que ROUGE.
- **FactCC**E ...**QA-based faithfulness**foram comuns em 2021-2023, agora muitas vezes substituídas por **G-Eval**(uma cadeia de resposta GPT-4 que avalia a coerência, a consistência, a fluência, a relevância com o raciocínio da cadeia de pensamento).
- **G-Eval**e abordagens similares de LLM-juiz correspondem ao julgamento humano ~ 80% do tempo em que as rubricas são bem concebidas.
> - **实体替换。**源说"John Smith"―摘要说"John Brown"―
- **数字漂移。**源说 "25,000"―摘要说 "25 milhões"―
- **极性翻转。**源说 "rejeitou a oferta"―摘要说 "aceitou a oferta"―
- **事实编造。**Não se fala do CEO. Resumo: CEO aprova.

Recomendação de produção: relatório ROUGE-L para comparação de legado, BERTScore para sobreposição semântica, G-Eval para coerência e factualidade. Calibração em relação a 50-100 resumos etiquetados por humanos.
> Método de avaliação eficaz:

### Passo 4: o problema da factualidade
> - **FactCC。**O que é um sistema de análise de dados que permite a análise de dados e de dados?
- **基于 QA 的事实性检查。**Para QA 模型提问源中有答题──如果摘要支持不同的答案,标记──
- **实体级 F1。**Comparar a origem com o objeto de nomeado no resumo.

Os resumos abstractos são propensos a alucinação. Os resumos extrativos têm um risco de alucinação muito menor porque a saída é levantada literalmente da fonte, embora ainda possam enganar se as frases de origem são descontextualizadas, ultrapassadas ou citadas fora de ordem. Esta é a única maior razão pela qual os sistemas de produção ainda preferem métodos extrativos para conteúdo adjacente à conformidade.
> Para o conteúdo de facto importante para o usuário (novazi, medicina, leis, finanças), a extração é uma escolha padrão mais segura.

Tipos de alucinação:

- **Entity swap.**A fonte diz "John Smith". O resumo diz "John Brown".
- **Number drift.**A fonte diz "25.000". O resumo diz "25 milhões".
- **Polarity flip.**A fonte diz que "recusou a oferta". O resumo diz que "aceitou a oferta".
- **Fact invention.**A fonte não menciona o CEO, mas diz que o CEO aprovou.

As abordagens de avaliação são:

- **FactCC.**Um classificador binário treinado em relação entre frase fonte e frase resumida.
- **QA-based factuality.**Faça perguntas a um modelo de QA cujas respostas estão na fonte.
- **Entity-level F1.**Compare entidades nomeadas na fonte versus resumo.

Para qualquer coisa que esteja voltada ao usuário onde a factualidade seja importante (noticias, médicos, legais, financeiros), a extração é a defesa mais segura.

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

A pilha de 2026:
> 2026  

| Use case | Recommended |
|---------|-------------|
| News, 3-5 sentence summary, English | `facebook/bart-large-cnn` |
| Scientific papers | `google/pegasus-pubmed` or a tuned T5 |
| Multi-document, long-form | Any LLM with 32k+ context, prompted |
| Dialog summarization | `philschmid/bart-large-cnn-samsum` |
| Extractive, low hallucination risk by construction | TextRank or `sumy`'s LSA / LexRank |
> ♪ Usar a cena ♪
|---------|------|
| 新闻，3-5 句摘要，英语 | `facebook/bart-large-cnn` |
| 科学论文 | `google/pegasus-pubmed` 或微调的 T5 |
| 多文档，长文 | 任何 32k+ 上下文的 LLM，提示 |
| 对话摘要 | `philschmid/bart-large-cnn-samsum` |
| 抽取式，结构性低幻觉风险 | TextRank 或 `sumy` 的 LSA / LexRank |

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


Os LLM com longo contexto geralmente superam os modelos especializados em 2026 quando a computação não é uma restrição.
> O Mestrado em Matemática em 2026 é um modelo de cálculo e de cálculo.


## Envia-o . Produto .

Salva como`outputs/skill-summary-picker.md`- Não .
> 保存为 `outputs/skill-summary-picker.md`- Não .

```markdown
---
name: summary-picker
description: Pick extractive or abstractive, named library, factuality check.
version: 1.0.0
phase: 5
lesson: 12
tags: [nlp, summarization]
---

Given a task (document type, compliance requirement, length, compute budget), output:

1. Approach. Extractive or abstractive. Explain in one sentence why.
2. Starting model / library. Name it. `sumy.TextRankSummarizer`, `facebook/bart-large-cnn`, `google/pegasus-pubmed`, or an LLM prompt.
3. Evaluation plan. ROUGE-1, ROUGE-2, ROUGE-L (use rouge-score with stemming). Plus factuality check if abstractive.
4. One failure mode to probe. Entity swap is the most common in abstractive news summarization; flag samples where source entities do not appear in summary.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse abstractive summarization for medical, legal, financial, or regulated content without a factuality gate. Flag input over the model's context window as needing chunked map-reduce summarization (not just truncation).
```

## Exercícios.

1. **Easy.**Exerça o TextRank em 5 artigos de notícias. Compare as três principais frases com um resumo de referência. Mese ROUGE-L. Você deve ver 30-45 ROUGE-L em artigos de estilo CNN / DailyMail.
2. **Medium.**Implementar factualidade a nível da entidade: extrair entidades nomeadas da fonte e resumo (spaCy), recuperar computacional das entidades fontes em resumo e precisão das entidades resumidas contra a fonte.
3. **Hard.**Compare o BART-Grande-CNN com um LLM (Claude ou GPT-4) em 50 artigos da CNN/DailyMail.
> 1. **简单。**Em 5 篇新闻文章上运行 TextRank──将 top-3 句子与参考摘要比较──测量 ROUGE-L── em CNN/DailyMail 风格文章上你应该看到 30-45 ROUGE-L──
2. **中等。**实现实体级事实性:从源和摘要中提取命名实体(spaCy), 计算源实体在摘要中的召唤率和摘要实体对源的精确率──高精确率低召唤率意味着安全但简略; 低精确率意味着幻觉实体──
3. **困难。**Em 50 篇 CNN/DailyMail 文章上比较BART-big-CNN与LLM(Claude或GPT-4);; relatório ROUGE-L、事实性(按实体F1)和每个摘要的成本;;记录各自的胜场景──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive | Pick sentences | Return sentences verbatim from the source. Never hallucinates. |
| Abstractive | Rewrite | Generate new text conditioned on source. Can hallucinate. |
| ROUGE | Summary metric | N-gram / LCS overlap between system output and reference. |
| TextRank | Graph-based extractive | PageRank over sentence similarity graph. |
| Factuality | Is it right | Whether summary claims are supported by the source. |
| Hallucination | Made-up content | Content in the summary that the source does not support. |
> # O termo # Que as pessoas dizem # # O significado real #
|------|-----------|---------|
| 抽取式 | 选取句子 | 从源中逐字返回句子。不会幻觉。 |
| 生成式 | 重写 | 根据源生成新文本。可能幻觉。 |
| ROUGE | 摘要指标 | 系统输出与参考之间的 n-gram / LCS 重叠。 |
| TextRank | 基于图的抽取式 | 句子相似度图上的 PageRank。 |
| 事实性 | 对不对 | 摘要声明是否被源支持。 |
| 幻觉 | 编造内容 | 摘要中源不支持的内容。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) o papel canônico extractivo.
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461)O papel BART.
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777) Pegasus e o objectivo da frase de diferença.
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/)Papel vermelho.
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) o papel de paisagem de facto.
> - [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) 抽取式经典论文──
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461) BART 论文──
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777)Pegasus e seu objetivo
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/) ROUGE 论文──
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) Fakt性全景论文──
