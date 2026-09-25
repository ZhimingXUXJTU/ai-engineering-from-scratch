# Tags de POS e Parsagem sintática .

> A gramática estava fora de moda por um tempo, então cada linha de LLM precisava de validar a extração estruturada, e voltou.
> O idioma já não foi popular. Depois, cada linha de LLM precisa de um teste estruturado.

> **【中文解读】**给每个词标注词性,分析句子的语法结构──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

A lição 01 prometeu que a lemmatização precisa de uma etiqueta de parte da fala.`running`É um verbo, um lematizer não pode reduzir a `run`Sem saber .`better`É um adjetivo, não pode ser reduzido a `good`- Não .

> 第01 课承诺过词形还原需要词性标注──不知道 `running`É um termo, um termo não pode ser usado para o seu nome.`run`Não sei.`better`É um termo que não pode ser recuperado.`good`- Não.

Essa promessa oculta um subcampo inteiro. A etiquetação de parte da fala atribui categorias gramaticais. A análise sintática recupera a estrutura da árvore da frase: qual palavra modifica qual, qual verbo governa quais argumentos. A PNL clássica passou vinte anos refinando ambos.

> O que ocorre por trás do compromisso oculta uma área inteira. O que ocorre por trás do compromisso é que o compromisso oculta uma área inteira.

Não a comunidade aplicada. Cada pipeline de extração estruturada ainda usa árvores de POS e dependência sob o capô. JSON gerado pela LLM é validado contra restrições gramaticais. Os sistemas de resposta a perguntas decompõem consultas usando parses de dependência. Avaliação de qualidade de tradução automática verifica o alinhamento das árvores de parse.

> 应用界没有──每个结构化抽取流水线仍在底层使用POS 和依赖树──LLM 生成的JSON 会根据语法约束进行验证──问答系统使用依赖分析来分解查询──机器翻译质量评估器检查分析树的对齐──

Esta lição introduz os tagsets, as linhas de base e o ponto em que você deixa de implementar a partir do zero e chama espaCy.

>  Valor de saber                                                                                                                                                                                                                                                            

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

**POS tagging**É o que significa que cada símbolo é etiquetado com uma categoria gramatical.**Penn Treebank (PTB)**Tagset é o padrão inglês. 36 tags com distinções o leitor casual acha complicado: `NN`singular substantivo, `NNS`Pronom plural, `NNP`Propias substantivas singulares, `VBD`Verbo passado, `VBZ`3o personagem singular presente, etc. O **Universal Dependencies (UD)**Tagset é mais grosseiro (17 tags) e linguístico-agnóstico; tornou-se o padrão para o trabalho translangual.

> **词性标注（POS Tagging）**Para cada símbolo, o que é que é?**Penn Treebank (PTB)**标签集是英语的默认选择──36标签,带有一般读者觉得过于细致的区别:`NN`单数名词、`NNS`复数名词、`NNP`专名词单数、`VBD`动词过去时,`VBZ`动词第三人称单数现在时等等等──**通用依存（Universal Dependencies, UD）**标签集更粗(17 个标签) e não está relacionado com linguagem; tornou-se uma escolha padrão do trabalho translanguagem.

```
The/DET cats/NOUN were/AUX running/VERB at/ADP 3pm/NOUN ./PUNCT
```

**Syntactic parsing**produz uma árvore.

> **句法分析（Syntactic Parsing）**产生一棵树──两种主要风格:

- **Constituency parsing.**Frases de substantivos, frases de verbos, frases preposicionais nidificam dentro um do outro.
  **成分分析（Constituency Parsing）。**Nome: N.P.P. (em inglês)
- **Dependency parsing.**Cada palavra tem uma única palavra-chave em que depende, rotulada com uma relação gramatical.
  **依存分析（Dependency Parsing）。**Cada palavra tem um seu centro de domínio.

A análise de dependência ganhou na década de 2010 porque generaliza limpo entre as línguas, especialmente as de ordem de palavras livre.

> A análise depende de que os países da África do Sul tenham sido influenciados pela sua política de desenvolvimento.

```
running is ROOT
cats is nsubj of running
were is aux of running
at is prep of running
3pm is pobj of at
```

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.
```figure
pos-tagger
```

```figure
dependency-arcs
```

## Construí-lo

### Passo 1: linha de base de etiqueta mais frequente

O tagger mais estúpido que funciona, para cada palavra, prevê a tag que tinha mais vezes no treino.

> O mais usado é o marcador de POS.

```python
from collections import Counter, defaultdict


def train_mft(train_examples):
    word_tag_counts = defaultdict(Counter)
    all_tags = Counter()
    for tokens, tags in train_examples:
        for token, tag in zip(tokens, tags):
            word_tag_counts[token.lower()][tag] += 1
            all_tags[tag] += 1
    word_best = {w: c.most_common(1)[0][0] for w, c in word_tag_counts.items()}
    default_tag = all_tags.most_common(1)[0][0]
    return word_best, default_tag


def predict_mft(tokens, word_best, default_tag):
    return [word_best.get(t.lower(), default_tag) for t in tokens]
```

No corpus Brown, esta linha de base atinge uma precisão de 85%.

> Na biblioteca de linguagem, esta linha de base atinge uma precisão de cerca de 85%. Não é bom, mas é um modelo rigoroso que não deve ser inferior à linha de fundo.

### Passo 2: tagger HMM de bigramas

Modela a probabilidade conjunta da sequência:

> 建模序列的联合概率:

```
P(tags, words) = prod P(tag_i | tag_{i-1}) * P(word_i | tag_i)
```

Duas tabelas: probabilidades de transição (tag dada a tag anterior), probabilidades de emissão (tag dada a palavra). Estima ambas a partir de contagens com suavização Laplace. Decodificar com Viterbi (programação dinâmica sobre a rede de tag).

> 两个表:转移概率 (转移概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射率)  发射 (发射率) 发射率 (发射率) 发射率) 发射率 (发射率) 发射率) 发射率 (发射率) 发射率) 发射率 (发射率) 发射率) 发射率 (发射率) 发射率 (发射率) 发射率) 发射率 (发射率) 发射率) 发射率 (发射率) 发射率 (发射率) 发射率) 发射率 (发射率) 发射率) 发射 (发射) 发射 (发射) 发射) 发射 (发射) 发射) 发射 (发射) 发射 (发射) 发射 (发射) 发射) 发射 (发射) 发射) 发射 (发射) 发射 (发射) 发射) 发射 (发射) 发射)

```python
import math


def train_hmm(train_examples, alpha=0.01):
    transitions = defaultdict(Counter)
    emissions = defaultdict(Counter)
    tags = set()
    vocab = set()

    for tokens, ts in train_examples:
        prev = "<BOS>"
        for token, tag in zip(tokens, ts):
            transitions[prev][tag] += 1
            emissions[tag][token.lower()] += 1
            tags.add(tag)
            vocab.add(token.lower())
            prev = tag
        transitions[prev]["<EOS>"] += 1

    return transitions, emissions, tags, vocab


def log_prob(table, given, key, smooth_denom, alpha):
    return math.log((table[given].get(key, 0) + alpha) / smooth_denom)


def viterbi(tokens, transitions, emissions, tags, vocab, alpha=0.01):
    tags_list = list(tags)
    n = len(tokens)
    V = [[0.0] * len(tags_list) for _ in range(n)]
    back = [[0] * len(tags_list) for _ in range(n)]

    for j, tag in enumerate(tags_list):
        em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
        tr_denom = sum(transitions["<BOS>"].values()) + alpha * (len(tags_list) + 1)
        tr = log_prob(transitions, "<BOS>", tag, tr_denom, alpha)
        em = log_prob(emissions, tag, tokens[0].lower(), em_denom, alpha)
        V[0][j] = tr + em
        back[0][j] = 0

    for i in range(1, n):
        for j, tag in enumerate(tags_list):
            em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
            em = log_prob(emissions, tag, tokens[i].lower(), em_denom, alpha)
            best_prev = 0
            best_score = -1e30
            for k, prev_tag in enumerate(tags_list):
                tr_denom = sum(transitions[prev_tag].values()) + alpha * (len(tags_list) + 1)
                tr = log_prob(transitions, prev_tag, tag, tr_denom, alpha)
                score = V[i - 1][k] + tr + em
                if score > best_score:
                    best_score = score
                    best_prev = k
            V[i][j] = best_score
            back[i][j] = best_prev

    last_best = max(range(len(tags_list)), key=lambda j: V[n - 1][j])
    path = [last_best]
    for i in range(n - 1, 0, -1):
        path.append(back[i][path[-1]])
    return [tags_list[j] for j in reversed(path)]
```

Bigram HMM em Brown atinge ~93% de precisão. O salto de 85% para 93% é principalmente probabilidades de transição  o modelo aprende `DET NOUN`é comum e `NOUN DET`É raro.

> Na biblioteca de linguagem em Brown, o grupo HMM alcançou cerca de 93% de precisão.`DET NOUN`É comum.`NOUN DET`É raro.

### Passo 3: por que os taggers modernos vencem isto

As probabilidades de transição + de emissão são locais.`saw`é um substantivo em "Eu comprei uma serra" mas um verbo em "Eu vi o filme". Um CRF com características arbitrárias (sufixo, forma de palavra, palavra antes e depois, palavra em si) atinge ~97%.

> 转移 + 发射概率是局部的──它们无法捕获 `saw`Em "Eu comprei uma serra" entre é nome word mas em "Eu vi o filme" entre é动词──带有任意特征(后、词形、前后词、词本身) de CRF 达到约97%──BiLSTM-CRF 或 Transformer 达到约98%+──

O teto desta tarefa é definido por discordância entre os anotadores.

> O seu trabalho foi decidido pelos marcadores. Os marcadores humanos chegaram a um acordo em cerca de 97% do tempo no Penn Treebank. Mais de 98% dos modelos podem ser adaptados para o teste.

### Passo 4: Esboço de análise de dependência

A análise completa da dependência a partir do zero está fora de alcance; o tratamento do livro-texto canônico é em Jurafsky e Martin.

> Desde zero realizando a análise completa dependência ultrapassa o alcance; classic's textbooks handling see Jurafsky 和 Martin──needs to know of the two classic series:

- **Transition-based**Parser (arc-eager, arc-standard) atua como um parser de redução de mudanças: eles lêem tokens, os transferem para uma pilha e aplicam ações de redução que criam arcos. A codificação gananciosa é rápida. A implementação clássica é MaltParser. Versão neural moderna: o parser baseado em transição de Chen e Manning.
  **基于转移的**解析器(arc-eager、arc-standard) Como um mecanismo de resolução de arco-árco, o sistema de resolução de arco-árco é baseado em um mecanismo de resolução de arco-árco.
- **Graph-based**Os parseres (algoritmo de Eisner, Dozat-Manning biafina) pontua todas as bordas possíveis dependentes da cabeça e escolhem a árvore de extensão máxima.
  **基于图的**解析器(Eisner 算法、Dozat-Manning 双仿射) para cada possível cabeçalho-dependente 边打分, escolher o máximo de produção de árvore。

Para a maioria dos trabalhos aplicados, liga-se para o spaCy:

>  Para a maioria dos trabalhos, ajuste o espaço:

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running at 3pm.")
for token in doc:
    print(f"{token.text:10s} tag={token.tag_:5s} pos={token.pos_:6s} dep={token.dep_:10s} head={token.head.text}")
```

```
The        tag=DT    pos=DET    dep=det        head=cats
cats       tag=NNS   pos=NOUN   dep=nsubj      head=running
were       tag=VBD   pos=AUX    dep=aux        head=running
running    tag=VBG   pos=VERB   dep=ROOT       head=running
at         tag=IN    pos=ADP    dep=prep       head=running
3pm        tag=NN    pos=NOUN   dep=pobj       head=at
.          tag=.     pos=PUNCT  dep=punct      head=running
```

Leia o `dep`A coluna de baixo para cima e a estrutura gramatical da frase cai.

> Desde baixo até cima`dep`列,句子的语法结构就自然呈现了──

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

Cada biblioteca de produção de PNL envia POS e parseres de dependência como parte de um pipeline padrão.

> Cada produção de PNL 库都把 POS 和依赖解析器 como parte da linha de fluxo de água padrão fornecer.

- **spaCy**(`en_core_web_sm`- Não .`md`- Não .`lg`- Não .`trf`O sistema de informação é rápido, preciso e integrado com tokenization + NER + lemmatization.`token.tag_`- Não .`token.pos_`(UD), `token.dep_`(relação de dependência).
  **spaCy**(`en_core_web_sm`- Não .`md`- Não .`lg`- Não .`trf`)──快速、准确,与分词 + NER + 词形还原集成──`token.tag_`- Não.`token.pos_`(UD)`token.dep_`(dependência)
- **Stanford NLP (stanza)**Sucessor de Stanford ao CoreNLP. Estado da arte em mais de 60 idiomas.
  **Stanford NLP (stanza)**❖ Reitor do Stanford CoreNLP ❖ alcançar um nível avançado em mais de 60 idiomas ❖
- **trankit**- Baseado em transformador, boa precisão UD.
  **trankit**❖ Baseado em Transformer, boa UD 准确率──
- **NLTK**- Não .`pos_tag`- Útil, lento, mais velho, bom para ensinar.
  **NLTK**- Não.`pos_tag`△可用、慢、较旧──适合教学──

### Onde isso ainda importa em 2026

- **Lemmatization.**A lição 01 precisa de um POS para lematizar corretamente.
  **词形还原。**第01 课需要 POS 才能正确词形还原──始终如此──
- **Structured extraction from LLM outputs.**Validar que uma frase gerada respeita restrições gramaticais (por exemplo, acordo entre sujeito e verbo, modificadores necessários).
  **LLM 输出的结构化抽取。**验证生成的句子满足语法约束 (como o principal chamado de acordo, necessário modificar)
- **Aspect-based sentiment.**Os parses de dependência dizem-lhe qual adjetivo modifica qual substantivo.
  **基于方面的情感分析。**Dependência analítica diz-te qual é o nome do nome.
- **Query understanding.**"filmes dirigidos por Wes Anderson com Bill Murray" se descompõem em restrições estruturadas através da análise.
  **查询理解。**"filmes dirigidos por Wes Anderson com Bill Murray" 通过解析分解为结构化约束──
- **Cross-lingual transfer.**As etiquetas UD e as relações de dependência são linguísticas-agnósticas, permitindo uma análise estruturada de zero-shot das novas línguas.
  **跨语言迁移。**UD 标签和依赖与语言无关,支持新语言的零样本结构化分析──
- **Low-compute pipelines.**Se não conseguir enviar um transformador, o POS + o parse de dependência + o gazetteer vai longe.
  **低算力流水线。**Se não conseguires implementar o Transformer, POS + dependência + GeoNomenW典能让你走相当远――

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

## Envia-o . Produto .

Salva como`outputs/skill-grammar-pipeline.md`- Não .

> 保存为 `outputs/skill-grammar-pipeline.md`- Não .

```markdown
---
name: grammar-pipeline
description: Design a classical POS + dependency pipeline for a downstream NLP task.
version: 1.0.0
phase: 5
lesson: 07
tags: [nlp, pos, parsing]
---

Given a downstream task (information extraction, rewrite validation, query decomposition, lemmatization), you output:

1. Tagset to use. Penn Treebank for English-only legacy pipelines, Universal Dependencies for multilingual or cross-lingual.
2. Library. spaCy for most production, stanza for academic-grade multilingual, trankit for highest UD accuracy. Name the specific model ID.
3. Integration pattern. Show the 3-5 lines that call the library and consume the needed attributes (`.pos_`, `.dep_`, `.head`).
4. Failure mode to test. Noun-verb ambiguity (`saw`, `book`, `can`) and PP-attachment ambiguity are the classical traps. Sample 20 outputs and eyeball.

Refuse to recommend rolling your own parser. Building parsers from scratch is a research project, not an application task. Flag any pipeline that consumes POS tags without handling lowercase/uppercase variants as fragile.
```

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Exercícios.

1. **Easy.**Usando a linha de base com mais frequência de tag em um corpus de pequenas tag (por exemplo, subconjunto Brown do NLTK), medir a precisão em frases mantidas. Verifique o resultado de ~ 85%.
   **简单。**Em um pequeno tag tagginal (como o NLTK) usado mais frequentemente em um tagginal, a medida tem uma taxa de precisão de 85% dos resultados.
2. **Medium.**Treinar o HMM de grande formato acima e relatar a precisão/recolha por tag.
   **中等。**訓練上述二元组 HMM并报告每标签精确率/召回率──HMM
3. **Hard.**Use a análise de dependência do spaCy para extrair triples sujeito-verbo-objeto de uma amostra de 1000 frases. Avalie em 50 triples rotulados manualmente. Documentos onde a extração falha (muitas vezes passivos, coordenadas e sujeitos elidados).
   **困难。**Utilize a análise de dependência de espaCy a partir de 1000 palavras sample.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Termos-chave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| POS tag（词性标签） | Word's type / 词的类型 | Grammatical category. PTB has 36; UD has 17. / 语法类别。PTB 有 36 个；UD 有 17 个。 |
| Penn Treebank | Standard tagset / 标准标签集 | English-specific. Fine-grained verb tenses and noun number. / 特定于英语。细粒度的动词时态和名词数。 |
| Universal Dependencies（通用依存） | Multilingual tagset / 多语言标签集 | Coarser than PTB; language-neutral; defaults for cross-lingual work. / 比 PTB 更粗；语言无关；跨语言工作的默认选择。 |
| Dependency parse（依存分析） | Sentence tree / 句子树 | Each word has one head, each edge has a grammatical relation. / 每个词有一个中心词，每条边有一个语法关系。 |
| Viterbi（维特比算法） | Dynamic programming / 动态规划 | Finds the highest-probability tag sequence given emissions and transitions. / 给定发射和转移概率，找到最高概率的标签序列。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.

## Mais leitura 延伸阅读

- [Jurafsky and Martin — Speech and Language Processing, chapters 8 and 18](https://web.stanford.edu/~jurafsky/slp3/) o tratamento canônico de livros de texto de POS e análise. / POS 和解析的经典教科书处理──
- [Universal Dependencies project](https://universaldependencies.org/) o tagset e a coleção de árvores utilizadas por cada parcer multilingue. / 每个多语言解析器使用的跨语言标签集和树库集合。
- [spaCy linguistic features guide](https://spacy.io/usage/linguistic-features) referência prática para cada atributo exposto em `Token`- Não .`Token`Referência prática de cada característica da exposição acima.
- [Chen and Manning (2014). A Fast and Accurate Dependency Parser using Neural Networks](https://nlp.stanford.edu/pubs/emnlp2014-depparser.pdf)O artigo que trouxe os parses neurais para a corrente principal.
