# Memória híbrida: Vector + Graphic + KV (Mem0) 混合记忆:向量+图+KV(Mem0)
# Memória híbrida: Vector + Graphic + KV

> A memória híbrida executa três lojas em paralelo  vetor para semântica semelhança, KV para rápida pesquisa de fatos, gráfico para raciocínio de relação entre entidades  com uma camada de pontuação que as funde na recuperação. Este é um padrão de produção amplamente usado para memória externa; Mem0 (Chhikara et al., 2025) é uma implementação de referência.

> **【中文解读】**Mem0 vai considerar a memória como três conjuntos de armazenamento  veículo para linguagem semelhança  KV para rápida busca de fatos  图 para raciocínio de relações físicas                                                                                                                                                                                                                                      

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta Blocks) | **前置知识:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta 块)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Explique por que uma única armazenagem (apenas vetorial, apenas gráfico, apenas KV) é insuficiente para a memória do agente.
  Tradução do inglês para o inglês: Explanation of why single one storage (((仅向量、仅图、仅 KV) insuficiente para支 Agent 记忆。
- Nomear as três lojas paralelas do Mem0 e para o que cada uma optimiza.
  O Mem0 tem três funções de armazenamento e seu objetivo de otimização.
- Descreva a pontuação de fusão do Mem0  relevância, importância, recência  e por que é uma soma ponderada, não uma hierarquia.
  Tradução do inglês para o inglês: Mem0's fusion rating 相关性,重要性,时效性以及为什么是加权和而非层级
- Implementar uma memória de brinquedo de três andares em stdlib com um `add()`que escreve para os três e um`search()`que combina os resultados.
  Tradução do inglês:`add()`写入所有三个储存,`search()`融合結果──

## O problema é o problema da introdução

Uma loja é errada para uma das três classes de consulta:

> 单存储对三类查询之一是错误的:

- **Semantic similarity**"O que discutimos sobre o agente drift na semana passada?" Vence o Vector, KV e grafico.
  Tradução:**语义相似性**"Nós discutimos o que aconteceu na semana passada sobre o agente que se mudou?"
- **Fact lookup** "Qual é o número de telefone do usuário?" KV ganha; vetor é desperdício, gráfico é exagerado.
  Tradução:**事实查找**" o número de telefone do usuário é o quê?" KV 胜出;向量浪费,图过度──
- **Relationship reasoning** "Quais clientes compartilham a mesma entidade de faturamento?" Grafico vence; vector e KV não podem responder.
  Tradução:**关系推理**"Qual é o cliente que compartilha a mesma contabilidade?" 图胜出;向量和 KV 无法回答──

Os agentes de produção emitem os três em uma sessão. Uma memória de loja única é sempre errada para dois deles.`add`- Não .`search`A superfície com uma função de pontuação que as funde.

> - Não .**【类比】**Mem0 de três armazéns de imagens de biblioteca de três tipos de índice sistema:向量库像"按主题相关性"的智能推(适合"寻找类似书"),KV库像"按书名/ISBN"的精确搜索(适合"查具体一书"),图库像的网络(适合"寻找作者-出版社-引用关系")

> O agente de produção em uma única reunião emite todas as três perguntas.`add`- Não .`search`接口后面,并用评分函数融合它们──

> **【中文解读】**混合记忆系统 (Mem0) combina memória de trabalho a curto prazo e memória de longo prazo. Em janelas anteriores, a memória a curto prazo é armazenada em uma base de dados e gráficos de veículos.

> **【拓展：Mem0 是目前最流行的 Agent 记忆解决方案之一】**Mem0 (2024-2025) é atualmente um dos mais populares Agente  soluções de memória,GitHub 25k+ estrelas.

> - Não .**【前置】**必須先掌握:Phase 14·07(MemGPT) 和Phase 14·08(Letta Blocks) Mem0 é a "empréstima de armazenamento posterior do seu upgrade edition"── também precisa entender três tipos de base de dados:

## O conceito central.

### Três lojas em paralelo

Mem0 (arXiv:2504.19413, Abril 2025) em `add(text, user_id, metadata)`- Não .

> Mem0(arXiv:2504.19413,2025 年 4 月) 在 `add(text, user_id, metadata)`上:

1. Extrair os factos candidatos do texto (um passo orientado pelo Mestrado em Direito Jurídico).
   Tradução do inglês para o inglês: 文本中提取候选事实 (LDL)
2. Escreva cada fato no armazenamento vetorial (embedding) para pesquisa semântica.
   Tradução do inglês para tradução do inglês: will each facts write into向量存储 (em inglês: ︎)
3. Escreva cada fato para o armazém KV teclado em (user_id, fact_type, entity) para pesquisa O(1).
   Chinese:将每个事实写入 KV 存储,以 (user_id, fact_type, entity) 为键,实现 O(1) 查找。
4. Escreva cada fato no gráfico de armazenamento (Mem0g) como bordas digitalizadas para consultas de relacionamento.
   Tradução do inglês para inglês: will each fact write into图存储 (em inglês: will each fact write into图存储)

- Sim .`search(query, user_id)`- Não .

> Em`search(query, user_id)`上:

1. O vector store retorna o top-k incorporando cosino.
   O volume de armazenamento em forma de semelhança de um conjunto de fios de um conjunto de fios de um conjunto de fios de um conjunto de fios de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material de material.
2. O armazém KV retorna hits diretos teclados em query-derived (user_id, tipo, entidade).
   KV 存储返回基于查询推导的 (user_id, type, entity) 键的直接命中──
3. Graph store retorna subgraph acessível a partir de entidades de consulta.
   Tradução do inglês:图存储返回从查询实体可达的子图.
4. Uma camada de pontuação funde os três.
   Tradução do inglês: 评分层融合三者.

### Ponto de pontuação de fusão

```
score = w_relevance * relevance(q, record)
      + w_importance * importance(record)
      + w_recency * recency(record)
```

- **Relevance** cosino vetorial, KV correspondência exata, peso do caminho do gráfico.
  Tradução:**相关性**                                                                                                                                                                                                                                                              
- **Importance** etiquetado no momento da escrita ou aprendido (alguns fatos importam mais: nomes, identidades, políticas).
  Tradução:**重要性**写入时标记或学习得到 (((某些事事实更重要:姓名、ID、策略) 
- **Recency** decadência exponencial ao longo do tempo desde a última escrita ou leitura.
  Tradução:**时效性**Indexada de tempo decrescente desde a última inscrição ou leitura

Os pesos são ajustados por produto.`w_recency`para agentes de chat; superior `w_importance`para agentes de conformidade; superior `w_relevance`para agentes de recuperação.

> ️ **【易错点】**O valor de referência é o valor de referência de um documento de referência.**后果**O "Caso de Clima de ontem" foi pressionado por um novo "Caso de Clima de ontem", o que levou a uma nova "Caso de Clima de ontem" a ser aplicada.`w_recency`O tempo diminuiu e o tempo se inundou.**一行修复**A primeira é a de um grupo de pesquisadores que trabalha com a empresa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de

> 权重按产品调优──聊天 Agente 使用更高的 `w_recency`; 合规 Agente 使用更高的 `w_importance`;检索代理 使用更高的 `w_relevance`- Não.

### Memorandos e raciocínio temporal

Mem0g adiciona um detector de conflito. Quando um novo fato contradiz uma borda existente, a borda existente é marcada como inválida, mas não excluída.

> Mem0g adicionou um verificador de conflitos. Quando novos fatos e contradições existem, as existências são marcadas como inefetivas, mas não são eliminadas.

Este é o comportamento de conformidade do grau de Letta padrão de invalidação generaliza.

> É um comportamento de classe de con-

### Números de referência

Relatórios do Mem0 (2025):

> Mem0 论文报告(2025):

- **LoCoMo**(memória de conversação de longa duração): 91,6
- **LongMemEval**(memória episódica de longo horizonte): 93,4
- **BEAM 1M**(M-token memory benchmark): 64,1

As linhas de base de comparação (LLC de contexto completo 128k, loja de vetores plana, KV plana) perdem mais de 10 pontos.

> Comparar com base em dados de dados e dados, o sistema de dados e dados de dados não é um erro de quatro quadros.

### Taxonomia de âmbito

Mem0 divide a memória por escopo:

> Mem0 按范围拆分记忆:

- **User memory** persiste durante as sessões, teclado em `user_id`- Não .
  Tradução:**用户记忆**跨会话持久化, em`user_id`É o que eu quero.
- **Session memory** persiste dentro de um fio.
  Tradução:**会话记忆** em um caminho em perpétuo
- **Agent memory** Estado de instância por agente.
  Tradução:**Agent 记忆** Cada agente 实例状态──

Cada escrita escolhe um escopo. A recuperação pode fazer consultas em escopo com pesos por escopo. Misturar escopo sem pensar é como você obtém "o assistente disse à Alice sobre o projeto de Bob" incidentes.

> 🤔 **【困惑】**P: Mem0 3 tipos de armazenamento devem ser implementados, o custo para a pequena equipe é muito alto, não pode usar apenas a armazenagem de veículos?**纯聊天机器人**Utilizando a armazenagem de volume + KV já chega a menos de 90% de complexidade);**多用户企业 Agent**(涉及权限、关系、合规) deve ser usado em uma biblioteca, caso contrário, surgirá o incidente "Alice 见 Bob 的数据"―― os três armazéns do memorial são projetados para "conformar e viver", não todos os cenários são necessários。

> Cada vez que escrever escolha um alcance. A pesquisa pode atravessar o alcance.

### Onde este padrão vai mal

- **Embedding drift.**Os resultados vectoriais que se apresentam bem nas primeiras cem consultas degradam-se à medida que o corpo cresce. Adicione re-embedamento periódico dos registros mais utilizados.
  Tradução:**嵌入漂移。**Antes de 100 vezes, a pesquisa parece ter resultados de vector corretos com o aumento e diminuição do material.
- **KV schema creep.** `(user_id, type, entity)`Parece simples até que cada equipa adicione a sua .`type`- Auditar o tipo definido trimestralmente.
  Tradução:**KV 模式蔓延。** `(user_id, type, entity)`Parece simples, até que cada equipa adicione o seu.`type`◊ Tipo de auditoria trimestral ◊
- **Graph explosion.**Um extrator barulhento adiciona 50 bordas por mensagem.`add`- Não. - Não.
  Tradução:**图爆炸。**Uma máquina de extração de mensagens por cada mensagem adicionar 50 bordas.`add`调用图写入数;丢弃低置信度边缘──

## Construí-lo.
```figure
ae-memory-fusion
```

## Construí-lo

`code/main.py`Implementa o padrão de três andares em stdlib:

> `code/main.py`Utilizando o padrão de armazenamento, implementou três modos de armazenamento:

- `VectorStore` semelhança ingênua entre tokens como um substitutos de incorporação.
  Tradução:`VectorStore`Use simples símbolo 重叠相似性替代嵌入──
- `KVStore`- O que é que é ?`(user_id, fact_type, entity)`- Não .
  Tradução:`KVStore`以 `(user_id, fact_type, entity)`Por isso, não me esqueça.
- `GraphStore` bordas digitais (subjeto, relação, objeto, válido).
  Tradução:`GraphStore`类型化边 (类型化边) 
- `Mem0` fachada de nível superior com `add()`- Não .`search()`, pontuação de fusão, e recuperação consciente de alcance.
  Tradução:`Mem0`- Não, não.`add()`- Não.`search()`、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 、 
- Um rastro de trabalho numa conversa multi-usuário, multi-sessão.
  Tradução do inglês para o português:

- É o que é ?

> 运行:

```
python3 code/main.py
```

A saída mostra três caminhos de recall separados mais o top-k fundido.`main()`e ver a mudança de classificação.

> 输出显示三条独立的召回路加上融合的顶-k---在 `main()`顶部翻转评分权重观察排名变化──

## Use-o com o framework implementado.

- **Mem0 (Apache 2.0)** Pronto para produção. Auto-host com Postgres + Qdrant + Neo4j, ou use a nuvem gerenciada.
  Tradução:**Mem0 (Apache 2.0)**生产就绪──用 Postgres + Qdrant + Neo4j 自托管,或使用托管云──
- **Letta** Núcleo/recall/arquivo de três níveis; traga os seus próprios retrospectivos vetoriais e gráficos.
  Tradução:**Letta**Tres níveis de núcleo/recall/arquivo;
- **Zep** alternativa comercial com KG temporal e extracção de fatos.
  Tradução:**Zep**带时序知识图谱和事实提取的商业替代方案──
- **Custom builds** quando é necessário controlar exatamente o extrator (conformidade) ou os pesos de fusão (agentes de voz onde a recência é dominante).
  Tradução:**自定义构建** quando você precisa de controle preciso                                                                                                                                                                                                                                                           

## Envia-o . Produto .

`outputs/skill-hybrid-memory.md`gera um andamio de memória de três andares com um marcador de fusão, taxonomia de alcance e invalidação temporal conectado.

> `outputs/skill-hybrid-memory.md`O sistema de memória é um sistema de memória de memória, que é um sistema de memória de memória.

## Exercícios.

1. Substitua a semelhança do vetor de brinquedo por um modelo de incorporação real (transformadores de frases, Ollama, incorporações OpenAI).
   Tradução do inglês em japonês:将玩具向量相似性替换为真实嵌入模型──在合成长对话上测量 recall@10──1000次写入后排名会漂移?
2. Adicionar uma consulta temporal: `search(query, as_of=timestamp)`Retorna apenas registos válidos antes desse tempo.
   Tradução do inglês:`search(query, as_of=timestamp)` Apenas retornar a este tempo ou registros anteriores válidos Qual é o armazém que mais precisa de trabalho?
3. Implementar um detector de conflitos: se um fato recebido contradiz uma borda do gráfico, inválide a borda antiga e registre ambos.
   Tradução do inglês para tradução do inglês: si传入事实与图边矛盾,使旧边失效并记录两者──用"usuary lives in Berlin" -> "usuary lives in Lisbon"测试──
4. Portar o marcador de fusão para incluir um `user_feedback`dimensão (ponto adiante dos registos recuperados). Como evitar jogos (o agente só retorna registros que já gostou)?
   Tradução do inglês:将融合评分器移植为包含 `user_feedback`Como é que o agente só volta ao registro que já gostava?
5. Leia os documentos do Mem0 (`docs.mem0.ai`Portar o brinquedo para o`mem0`Comparar a qualidade da recuperação nas mesmas 20 consultas de teste.
   Tradução do inglês: Mem0 文档──将玩具移植为`mem0`客户端调用──比较相同 20 测试查询的检索质量──

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Hybrid memory | "Vector plus graph plus KV" / "向量加图加 KV" | Three stores written in parallel, fused on retrieval / 三个存储并行写入，检索时融合 |
| Fact extraction | "Memory ingestion" / "记忆摄取" | LLM step that breaks text into (entity, relation, fact) tuples / 将文本拆分为（实体、关系、事实）元组的 LLM 步骤 |
| Fusion scoring | "Relevance ranking" / "相关性排序" | Weighted sum of relevance, importance, recency / 相关性、重要性、时效性的加权和 |
| Scope | "Memory namespace" / "记忆命名空间" | user / session / agent — determines who sees what / 用户/会话/Agent——决定谁看到什么 |
| Mem0g | "Memory graph" / "记忆图" | Typed edges with temporal validity for relationship queries / 带时序有效性的类型化边，用于关系查询 |
| Temporal invalidation | "Soft delete" / "软删除" | Mark contradicted edges invalid; never delete / 标记矛盾边为无效；永不删除 |
| Embedding drift | "Retrieval rot" / "检索腐化" | Vector quality degrades as corpus grows; re-embed periodically / 向量质量随语料增长退化；定期重新嵌入 |

## Mais leitura 延伸阅读

- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) O papel original
  Tradução do português:Mem0 原始论文──
- [Mem0 docs](https://docs.mem0.ai/platform/overview) API de produção, SDKs, nuvem gerenciada
  中文翻译:Mem0 文档生产 API、SDK、托管云。
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) o antecessor de contexto virtual
  Tradução do português:MemGPT 论文虚拟上下文的前身──
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) o projeto de três camadas
  中文翻译:Letta 记忆块博客三层兄弟设计。
