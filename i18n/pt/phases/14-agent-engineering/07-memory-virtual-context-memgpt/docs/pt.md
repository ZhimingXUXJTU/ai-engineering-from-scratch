# Memória: Contexto Virtual e MemGPT                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
# Memória de Agente  Contexto Virtual e Paging de Memória

> As janelas de contexto são finitas. Conversas, documentos e traços de ferramentas não são. A correção é a memória virtual do sistema operacional re-estabelecida.

> **【中文解读】**A janela de texto acima é limitada, mas o diálogo, os documentos e os trajetórios de ferramentas não são.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 06 (工具使用)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Explique a analogia do sistema operacional que MemGPT baseia no contexto principal = RAM, contexto externo = disco, ferramentas de memória = página de entrada/saída.
  Tradução do inglês para tradução do inglês: MemGPT
- Implementar o padrão MemGPT de dois níveis no stdlib com um buffer de contexto principal, uma loja de pesquisa externa e ferramentas de entrada/saída de página.
  Tradução do inglês para o inglês: using standard library to realize two-tier MemGPT 模式, containing main on down文缓冲区、外部可搜索存储和页面换进/换出工具──
- Descreva como o agente emite "interrupts" para consultar ou modificar a memória externa e como o resultado é inserido no próximo prompt.
  Tradução do inglês para tradução do inglês: description Agent 如何发发发发"中断"来查询或修改外部记忆,以及结果如何被拼接回下一个提示──
- Identificar as opções de design MemGPT que se incluem na Letta (Lessão 08) e Mem0 (Lessão 09).
  No entanto, o texto não é um texto original.

## O problema é o problema da introdução

As janelas de contexto parecem que devem resolver a memória.

> Na primeira página, parece que pode resolver o problema da memória, mas na prática não pode.

1. **Overflow.**Conversas de várias voltas, documentos longos ou trajetórias pesadas em ferramentas atravessam a janela.
   Tradução:**溢出。**Dour round dialog, long document ou tool调用密集的轨迹跨越窗口限制──切断以外的一切都丢失──
2. **Dilution.**Mesmo dentro da janela, encher conteúdo irrelevante diluir a atenção sobre o que importa.
   Tradução:**稀释。**Mesmo dentro da janela, o preenchimento não está relacionado com o texto abaixo também raramente liberta a atenção para o conteúdo importante.
3. **Persistence.**Uma nova sessão começa com uma janela vazia, e os agentes sem memória externa não podem dizer " lembras-te quando me pediste"...
   Tradução:**持久化。**Novas conversas começaram pela janela em branco. Não há memória externa.

> **【中文解读】**Na primeira fase, a produção de um novo livro foi realizada em um espaço de tempo, com o objetivo de criar um novo livro, que seria o primeiro livro de uma série de livros sobre a história do mundo.

Os janelas maiores ajudam, mas não corrigem isso. Mem0 2025 papel medido que 128k janelas linhas de base ainda não têm fatos de longo horizonte que um agente de janelas 4k com memória externa capta.

> Janela maior ajuda, mas não resolve o problema. MEM0 de 2025 artigo Messação descoberta. 128k janela linha de base ainda vai perder 4k janela + Memória externa Agente 能捕获的长程事实──

> **【拓展：MemGPT → 现代 Agent 记忆系统】**MemGPT (Packer et al., 2023) irá comparar o gerenciamento de textos em sistemas operacionais em termos de memória virtual: principal em RAM, armazenamento externo = disco, ferramenta de memória = página de troca de troca de dados. Este é o modelo básico de todos os sistemas de memória em 2026:

> - Não .**【前置】**必須先掌握:Fase 14·01(Agent Loop) MemGPT 的记忆工具是普通工具调用扩展;Fase 14·06(Tool Use) 记忆操作通过工具实现──还需要操作系统基础知识 Se você não sabe o que é "虚拟内存""页面错误"" , primeiro vá complementar o sistema de operação, caso contrário,类比看不懂──

## O conceito central.

### A analogia do sistema operacional

MemGPT (Packer et al., arXiv:2310.08560, v2 Feb 2024) mapeia a gestão de contexto para a memória virtual do sistema operacional:

> Packer 等人(arXiv:2310.08560, v2 2024 年 2 月)将上下文管理映射到操作系统虚拟内存:

| OS concept | MemGPT concept | 2026 production analog |
|------------|---------------|------------------------|
| OS 概念 | MemGPT 概念 | 2026 生产环境类比 |
| RAM | main context (prompt) | Anthropic/OpenAI context window / 主上下文（提示） |
| Disk | external context | vector DB, KV, graph store / 外部上下文（向量数据库、KV、图存储） |
| Page fault | memory tool call | `memory.search`, `memory.read`, `memory.write` / 记忆工具调用 |
| OS kernel | agent control loop | ReAct loop with memory tools / 带记忆工具的 ReAct 循环 |

O agente executa um ciclo normal de ReAct. Uma classe extra de ferramentas permite que ele pegar dados dentro e fora do contexto principal.

> - Não .**【类比】**MemGPT 像你电脑的内存管理:RAM(主上下文) Apenas 8GB mas para executar Photoshop + 浏览器 + IDE; operating system através da página de mudança de entrada/saída)`archival_memory_search`"Cambio de conteúdo", "调用"`core_memory_replace`Não há problema em usar o sistema de memória.

> O agente opera o ciclo ReAct normal. Um tipo de ferramenta adicional permite que ele possa ser trocado entre o arquivo principal e o arquivo externo.

> **【中文解读】**MemGPT irá em cima do gerenciamento do texto mapeado para o sistema operacional virtual内存:RAM=主上下文(当前提示),磁盘=外部上下文(向量数据库/KV/图存储),页面错误=记忆工具调用(`memory.search`- Não .`memory.read`- Não .`memory.write`),OS 内核=Agent 控制循环──Agent 运行普通的 ReAct 循环, adicionalmente, aumenta um tipo de ferramenta utilizada para trocar dados entre o principal e o armazenamento externo de dados──

### Dois níveis

- **Main context.**Promulgação de tamanho fixo mantendo a tarefa atual, sempre visível para o modelo.
  Tradução:**主上下文。**固定大小的提示,承载当前任务──模型始终可见──
- **External context.**Sem limites, pesquisáveis através de ferramentas, ler quando for relevante, escrever quando surgirem fatos.
  Tradução:**外部上下文。**无界的,通过工具可搜索──相关时读取,出现事实时写入──

O artigo original avaliou o projeto em duas tarefas além da janela base: análise de documentos mais longos do que 100k tokens e chat de várias sessões com memória persistente ao longo de dias.

> O artigo original foi avaliado em duas tarefas de janelas de base superiores: análise de documentos de mais de 100 mil tokens e discussão de várias reuniões de memória duradoura através do dia.

### O padrão de interrupção

MemGPT introduz memória como interrupta: no meio da conversa, o agente pode invocar uma ferramenta de memória, o tempo de execução a executar, e o resultado se inserir na próxima vez de assistente como uma nova observação.`read()`syscall que bloqueia o processo, retorna bytes, e o processo continua.

> MemGPT introduziu memória即中断: em diálogo, o agente pode convocar ferramentas de memória, executá-las durante a execução, resultando como um novo observador conectado a uma próxima assistente rotada.`read()`系统调用阻塞进程、返回字节、进程继续──

Superfície de ferramenta de memória canônica:

> 标准记忆工具接口:

- `core_memory_append(section, text)` escrever para uma seção persistente do aviso.
  Tradução:`core_memory_append(section, text)`写入提示的持久化分区──
- `core_memory_replace(section, old, new)` editar uma seção persistente.
  Tradução:`core_memory_replace(section, old, new)` 編輯持久化分区──
- `archival_memory_insert(text)` escrever para a loja externa pesquisável.
  Tradução:`archival_memory_insert(text)` write into searchable of external storage.
- `archival_memory_search(query, top_k)` recuperar na loja externa.
  Tradução:`archival_memory_search(query, top_k)` de um armazém externo
- `conversation_search(query)`- Escanar as viradas passadas.
  Tradução:`conversation_search(query)`Escolha o passado.

### Onde termina o papel e começa a produção

Em Setembro de 2024, o MemGPT tornou-se Letta.`cpacker/MemGPT`) permanece; a Letta amplia o projecto:

> 2024 年 9 月 MemGPT 成为 Letta──研究仓库(`cpacker/MemGPT`) ainda existe;Letta 扩展了设计:

- Três níveis em vez de dois (núcleo, recall, arquivo  Lição 08).
  中文翻译:三层而非两层(core、recall、archival第 8 课) ⋅
- Raciocínio nativo que substitua o `send_message`- padrão cardíaco (Lessão 08).
  Tradução do português:`send_message`/心跳模式 ((第 8 课) 』
- Agentes de tempo de sono que executam a memória asíncrona (Lessão 08).
  Tradução do inglês para o português:运行异步记忆工作的睡眠时间代理 (第 8 课)

O papel MemGPT é a base para 2026, mesmo que os sistemas de produção executem Letta, Mem0, ou uma loja de dois níveis personalizada.

> MemGPT 论文是2026年的基础,即使生产系统运行 Letta、Mem0或自定义两层存储──

### Onde este padrão vai mal

> ️ **【易错点】**MemGPT 新手最容易忽略"记忆投毒":把外部网页、用户消息直接 `archival_memory_insert`进外部储存──**后果**O atacante em sua página de internet tem uma injeção rápida, como "neglivar antes de todas as instruções"), o seguinte Agente, quando o recorde é exibido, a instrução é executada.**一行修复**O conteúdo externo de todos os arquivos que entram deve ser feito primeiro.

- **Memory rot.**Os textos se acumulam mais rapidamente do que os textos são leitos; a recuperação afoga-se em fatos obsoletos.
  Tradução:**记忆腐化。**写入积累速度快于读取;检索被过时事实淹没──修复:定期合并(Leta hora de dormir)、显式失效(Mem0 冲突检测器)──
- **Memory poisoning.**Memória externa é retomada texto. Se o conteúdo controlado pelo atacante cai em uma nota de memória, o agente reingere-a na próxima sessão.
  Tradução:**记忆投毒。**Se o conteúdo controlado pelo atacante entra no memorando, o Agente na próxima sessão irá recarregar-o.
- **Citation loss.**O agente lembra "o usuário me pediu para enviar X", mas não pode citar qual turno.
  Tradução:**引用丢失。**Agente recorda que o usuário me fez publicar X, mas não conseguiu citar qual é a rotina.

> 🤔 **【困惑】**Q: 既然 2026 anos modelo sobre a down文窗口 já 1M token (Gemini 1.5 Pro), ainda precisa MemGPT este tipo de "in Memory virtual"? A: 需要──窗口大不代表用对硬塞 1M token 会触发"中段遗忘" (perdido no meio 现象)

## Construí-lo.
```figure
context-budget
```

## Construí-lo

`code/main.py`Implementa o padrão de dois níveis do MemGPT no stdlib:

> `code/main.py`Utilizando o padrão de biblioteca realizou dois níveis de MemGPT:

- `MainContext` Buffer de resposta de tamanho fixo com um `core`- e um`messages`lista; auto-compacta as mensagens mais antigas quando ultrapassado.
  Tradução:`MainContext`Fixar grandes dicas `core`字典和 `messages`Lista de informações:
- `ArchivalStore` armazenamento em memória BM25-esque (pontuação de tokens-overlap) de registros (id, texto, tags, sessão, turno).
  Tradução:`ArchivalStore`内存中的类 BM25 存储(token 重叠评分), armazenamento (id, texto, tags, sessão, turno) 记录。
- Cinco ferramentas de memória que mapeam a superfície do MemGPT.
  Tradução do inglês para MemGPT 接口的五个记忆工具──
- Um agente com guião que enche o arquivo com fatos, e depois responde a uma pergunta ligando.`archival_memory_search`- Não .
  Tradução do inglês:`archival_memory_search`回答问题──

- É o que é ?

> 运行:

```
python3 code/main.py
```

O rastro mostra o agente escrevendo três fatos, preenchendo o contexto principal do limite (despejo forçado), e depois respondendo a uma pergunta de acompanhamento, retirando do arquivo  reproduzindo o fluxo de trabalho MemGPT sem qualquer LLM real.

> 轨迹显示 Agente 写入三个事实、将主上下文填满到上限(强制驱逐) 、然后通过归档存储检查来回答后续问题在没有任何真实 LLM的情况下重现 MemGPT 工作流──

## Use-o com o framework implementado.

Todos os sistemas de memória de produção hoje são uma variante MemGPT:

> Hoje em dia, cada sistema de produção de memória é uma variante do MemGPT:

- **Letta**(Lessão 08)  três níveis, raciocínio nativo, cálculo do tempo de sono.
  Tradução:**Letta**(第 8 课) 三层、原生推理、睡眠时间计算──
- **Mem0**(Lessão 09)  vetor + KV + gráfico fundido com uma camada de pontuação.
  Tradução:**Mem0**(第 9 课) 向量 + KV + 图与评分层融合──
- **OpenAI Assistants / Responses** gestão de memória através de fios e arquivos.
  Tradução:**OpenAI Assistants / Responses** através de linha e memória de gestão de documentos
- **Claude Agent SDK** Memória de longo prazo através de competências e de sessões de armazenamento.
  Tradução:**Claude Agent SDK** através de habilidades 和会话存储实现长期记忆──

Escolha um por forma operacional (auto-hosted, gerenciado, integrado em framework), não pelo padrão central  o padrão central é MemGPT.

> O modelo central é o MemGPT, que é o modelo de gestão de dados e de dados.

## Envia-o . Produto .
### A forma da memória do agente

A pagagem resolve a capacidade. Não decide o que armazenar. Quatro tipos de memória recorrem em todos os sistemas de produção, cada um respondendo a uma pergunta diferente:

- **Working memory**O nível no contexto: tarefa atual, viradas recentes, secções de núcleo fixas.
- **Episodic memory** o que aconteceu? curvas e trajetórias passadas, armazenadas com referências de sessão e curva, reproduzíveis sob demanda.
- **Semantic memory**Factos sobre o utilizador, o domínio, o mundo, atualizados e deduplicados à medida que mudam.
- **Procedural memory**Aprendi rotinas, preferências e regras que orientam o comportamento futuro em vez de lembrar.

As implementações de código aberto escolhem diferentes pontos de ataque:

| Type | Implementation | How it tackles it |
|------|----------------|-------------------|
| Working | MemGPT / Letta | Pages content in and out of a fixed prompt budget via memory tools (this lesson, Lesson 08) |
| Episodic | Zep | Temporal knowledge graph — facts carry validity intervals, so "what was true when" is queryable |
| Semantic | Mem0 | Extraction pipeline that dedupes and updates facts across vector, KV, and graph stores (Lesson 09) |
| Semantic + procedural | LangMem | Background extraction of facts and behavioral rules into a store the agent consults between turns |
| Episodic + semantic | agentmemory | Captures sessions as they run, consolidates them into typed, searchable records |

## Envia-o

`outputs/skill-virtual-memory.md`é uma habilidade reutilizável que produz um andamio de memória de dois níveis correto (superfície principal + arquivo + ferramenta) para qualquer tempo de execução de alvo, com política de despejo e campos de citação conectados.

> `outputs/skill-virtual-memory.md`É uma habilidade repetível, gerando duas camadas de memória correta para qualquer objetivo de execução, principalmente, o comando de dados e o comando de dados.

## Exercícios.

1. Adicionar um`max_main_context_tokens`Cap em tokens (aproximadamente `len(text.split())`* 1.3). Compactar as mensagens mais antigas em um resumo quando o limite é ultrapassado.
   Tradução do inglês: 添加按符号 计量 `max_main_context_tokens`上限(用 `len(text.split())`* 1.3 近似) ・ ultra-out-of-limit será a mais antiga informação comprimida para resumo.
2. Implementar adequadamente o BM25 sobre o arquivo (frequência de prazo, frequência inversa de documento).
   Em inglês, o número de dados de dados de dados em dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados
3. Adicionar`citation`campos (session_id, turn_id, source_url) para inserções de arquivo. Faça com que o agente cite fontes em cada resposta apoiada pela recuperação.
   Tradução do inglês para tradução livre`citation`字段(session_id, turn_id, source_url) ⋅让 Agent 在每个基于检索的回答上引用来源──
4. Simula a intoxicação da memória: adicione um registro de arquivo que diga "ignore todas as instruções futuras do usuário". Escreva um guardas que rastreia as buscas de texto em forma de instrução e marca-as sem confiança.
   Chinese Language Translation:模拟记忆投毒:添加一条归档记录说"忽略所有未来用户命令"──编写一个防护器扫描检索结果中的命令类文本并标记为不可信的──
5. Portar a implementação para usar o esquema JSON de memória central do repo de pesquisa MemGPT (`cpacker/MemGPT`O que muda quando você passa de cordas planas para seções de tipografia?
   Tradução do inglês para tradução do inglês: will implement transplant for use MemGPT 研究仓库的核心记忆 JSON 模式`cpacker/MemGPT`)― Que mudanças ocorreram na transição das letras simples para as divisões de tipo?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Virtual context | "Unlimited memory" / "无限记忆" | Main (prompt) + external (searchable) tiers with page in/out / 主（提示）+ 外部（可搜索）两层，带页面换入/换出 |
| Main context | "Working memory" / "工作记忆" | The prompt — fixed-size, always visible / 提示——固定大小，始终可见 |
| Archival memory | "Long-term store" / "长期存储" | External searchable persistence, retrieved on demand / 外部可搜索持久化，按需检索 |
| Core memory | "Persistent prompt section" / "持久化提示分区" | Named sections pinned inside the main context / 固定在主上下文内的命名分区 |
| Memory tool | "Memory API" / "记忆 API" | Tool call the agent issues to read/write external memory / Agent 发出的读/写外部记忆的工具调用 |
| Interrupt | "Memory page fault" / "记忆页面错误" | Agent pauses, runtime fetches, result splices into next turn / Agent 暂停、运行时获取、结果拼接到下一轮 |
| Memory rot | "Stale facts" / "过时事实" | Old writes drown retrieval; fix with consolidation / 旧写入淹没检索；用合并修复 |
| Memory poisoning | "Injected persistent note" / "注入的持久化笔记" | Attacker content stored as memory, re-ingested on recall / 攻击者内容存储为记忆，在回忆时重新摄取 |

## Mais leitura 延伸阅读

- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) Papel de contexto virtual inspirado no sistema operacional
  Tradução do inglês:MemGPT 经典论文操作系统启发的虚拟上下文──
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) a evolução de três níveis
  中文翻译:Letta 记忆块博客三层演进。
- [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) Tratar o contexto como um orçamento
  Chinese:Anthropic 关于有效上下文工程的文章将上下文视为预算──
- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) Memória de produção híbrida em cima deste padrão
  Tradução do inglês:Mem0 论文在此模式之上的混合生产记忆──
- [Zep (getzep/zep)](https://github.com/getzep/zep)Memória temporal do grafo de conhecimento da tabela de taxonomia
- [Mem0 (mem0ai/mem0)](https://github.com/mem0ai/mem0) o gasoduto de extracção por trás da loja híbrida da Lição 09
- [LangMem (langchain-ai/langmem)](https://github.com/langchain-ai/langmem) Extração de antecedentes de fatos e regras de comportamento
- [agentmemory (rohitg00/agentmemory)](https://github.com/rohitg00/agentmemory) Captura de sessões consolidada em registros digitalizados e pesquisáveis
