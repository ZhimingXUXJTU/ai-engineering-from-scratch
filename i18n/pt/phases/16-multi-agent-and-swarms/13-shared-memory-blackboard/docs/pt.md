# Memória compartilhada e padrões de quadro negro .

> Em 2026 existem duas abordagens em conjunto: o**message pool**(todos vêem as mensagens de todos, como no AutoGen GroupChat ou MetaGPT) e o **blackboard with subscription**(agentes se inscreverem em eventos relevantes, como no MCP Context-Aware ou na estrutura Matrix). Ambos são a única parte com estado de um sistema multi-agente  o que significa que ambos são onde os bugs interessantes vivem.**memory poisoning**A lição da "Study of the Fire" é uma lição de que um agente alucina um "fatto", outros agentes o tratam como verificado, e a precisão declina gradualmente de uma forma que é muito mais difícil de depurar do que um acidente imediato.

> **【中文解读】**Esta secção apresenta a memória compartilhada e o mecanismo de coordenação no sistema de multi-agentes.

> **【拓展：shared memory blackboard→具体应用】**O modelo de memória/blackboard é um mecanismo de coordenação clássico de vários agentes  sistemas  todos os agentes 阅读写一个共享知识库──黑板模型起源于1980年代的听证会-II语音识别系统──现代实现包括 Redis 共享状态、向量数据库和MCP Resources──优势是简单,劣势是竞争条件(多个代理 同时写入)──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `threading`) | **语言:** Python (标准库, `threading`)
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 04 (原语模型), Phase 16 · 09 (并行群体网络)
**Time:** ~75 minutes | **时间:** ~75 分钟

> - Não .**【前置】**学本节前请先掌握:Fase 16·04(原语)、Fase 16·09(Swarm)、并发编程(锁、竞态)。共享记忆 = 多 Agent 协调的核心数据结构──
> - Não .**【类比】**Compartilhar memórias em duas formas: (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) "o que é um problema de saúde" (a) " (a) "o que é mais difícil de "o que é que é que é "

## Problema Introdução

Os sistemas multi-agentes precisam de um lugar para os agentes compartilharem fatos. Uma opção literal é "passá-lo tudo em mensagens"  mas que reinventa o estado compartilhado com cópia extra. Outra é "dar a todos um log global"  mas os logs globais crescem ilimitados e envenenam facilmente.

> Do agente  sistema precisa de um local para que o agente comunique os fatos. Uma opção de letra é "transmitir tudo na mensagem" mas isto é como reinventar com cópia extra de condição.

As três opções seguem um tradicional trade-off de sistemas distribuídos: barato-mas-fragilidade (mensagens), simples-mas-inscalável (log global), escalavel-mas-rigido (projeções por agente). Nenhuma opção domina.

> Três opções Retrovivência classico sistema distribuído Pesagem: barato mas fraco (chá) 消息 (chá) 简单但不可扩展 (má) 整局日志 (má) 可扩展但化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má) 化 (má)

Quando um dos agentes alucina e escreve a alucinação para o estado compartilhado, cada agente a seguir que lê esse estado adota a alucinação como fato. Quando os humanos percebem, a cadeia de raciocínio está a cinco passos de profundidade e a causa raiz é a terceira mensagem já escrita.

> Quando um dos agentes 幻觉并将幻觉写入共享状态时, cada leitura do estado 游 官员将幻觉作为事实采纳. Quando o ser humano percebe, a cadeia de conclusões já tem cinco passos profundos, e a causa fundamental é a terceira.

Um acidente dá-lhe um rastro de pilha. O envenenamento da memória dá-lhe um relatório confidencialmente errado. O primeiro é detectável em segundos; o segundo pode levar dias de trabalho forense para rastrear a alucinação originária.

> 崩给你堆跟踪――内存污染给你自信错误报告―― primeiro, alguns segundos de detecção; segundo, talvez, alguns dias de verificação para se voltar ao original.

É a segunda família de falhas mais documentada na taxonomia MAST (Cemri et al., arXiv:2503.13657) e é estrutural: qualquer projeto de memória compartilhada sem origem e um verificador não-escritível irá exibí-lo eventualmente.

> É o segundo maior registro em casos de falência da família (Cemri et al., arXiv:2503.13657), mas também é estrutural: qualquer origem sem rastreamento e não-escritível do projeto de memória compartilhada vai eventualmente surgir este problema.

## Conceptos básicos

### As duas principais topologias

**Full message pool.**Cada agente lê cada mensagem. AutoGen GroupChat e MetaGPT usam isso. Simple, transparente, inspecionável, mas não escala além de ~ 10 agentes porque o contexto de cada agente preenche o trabalho de outros agentes.

> **完整消息池。**Cada Agente 读取每条消息──AutoGen GroupChat 和 MetaGPT Use this method──简单,透明,可检查,但不能扩展到约10 Agentes以上,因为每个Agente的上下文会填满其他Agente的工作──

**Blackboard with subscription.**Os agentes declaram interesse em tópicos; os substratos apenas encaminham mensagens relevantes. CA-MCP (arXiv:2601.11595) e a estrutura descentralizada Matrix (arXiv:2511.21686) usam isso. Escala ainda mais, mas requer um projeto de esquema antecipado para tornar as assinaturas significativas.

> **带订阅的黑板。**Agente declaração de interesse em assunto; nível inferior apenas via via relatórios. CA-MCP(arXiv:2601.11595) e Matrix 去中心化框架(arXiv:2511.21686) Usar esse método.

### Quando cada um vencer

- **Full pool**O que é trivial é o que é dito quando todos vêem tudo.
  Tradução:**完整池**Quando cada um vê tudo, a razão que alguém diz é simples.
- **Blackboard**O roteamento economiza custos simbólicos e poluição do contexto.
  Tradução:**黑板**Em Agente 很多、角色同质但实例众多(群体) 、对话长时间运行时胜出──路由节省代币 成本和上下文污染──

Os sistemas de produção frequentemente misturam-se: uma pequena piscina completa no topo (camada de planejamento), placas negras abaixo (camada de trabalhadores).

> Sistema de produção geralmente misturado: topo de um pequeno conjunto de sistemas de produção (pielão de produção), baixo é o quadro de trabalho (pielão de produção).

Este híbrido é o que o sistema de pesquisa da Anthropic faz: um supervisor (pool completo entre alguns agentes principais) delega aos sub-agentes (cada um com seu próprio contexto de alcance, isolado dos irmãos).

> Esta mistura é feita pelo Antropic Research System: supervisor (supervisor)                                                                                                                                                                                                                                                      

### Envenenamento da memória, num cenário

Três agentes trabalham numa tarefa de investigação, o agente A é um agente de recuperação, o agente B é um resumidor, o agente C é um analista.

> Três agentes 处理一个研究任务──Agent A é inspeção agente──Agent B é abstração ―Agent C é analista──

1. A traz uma página e escreve uma mensagem para o estado compartilhado: "O estudo relata uma melhoria de 42 por cento na precisão".
   Chinese:A 获取一个页面并向共享状态写入消息:" estudo relatou aumento da taxa de precisão de 42%".""
2. A página que recebi disse "melhora de 4,2%". Um alucinava um decimal.
   Na verdade, a página de obtenção diz que "4,2% 提升──"A 幻觉一个小数点──.
3. B, lendo o estado compartilhado, escreve: "Grande ganho de precisão de 42% relatado (fonte: A). "
   O estudo foi publicado em 18 de janeiro de 2012 e foi publicado em 18 de janeiro de 2012.
4. C, lendo o estado compartilhado, escreve: "Recomenda adoção  42% elevação é transformadora".
   O estado de comunhão é um estado de mudança.
5. O relatório final cita um número de 42% que nunca existiu.
   O relatório final cita um 42% de números que nunca existiu.

Nenhum agente caiu, nenhum teste falhou, o sistema "funcionou", a alucinação passou do contexto de um agente para o raciocínio de cada agente através de um estado compartilhado.

> 没有 Agent 崩──没有测试失败──系统"工作"了──幻觉通过共享状态从一个代理的上下文进入了每个下游代理的推理──

É por isso que o envenenamento da memória é insidioso: não há acidente, nenhum erro, nenhum aviso. O sistema produz um relatório confidencialmente errado. A única maneira de detectá-lo é retomar cada fato de fontes primárias  que derrota o ponto de ter agentes.

> É por isso que a contaminação de memória entra em risco: não há queda, não há erro, não há aviso. O sistema gera um relatório de erro de confiança.

### Por que é estrutural

Sem estado compartilhado, a alucinação do agente A permanece no contexto de A. Agentes do fluxo inferior re-recolherão ou re-derivarão e podem pegar o erro. Com estado compartilhado ingênuo, o contexto de A se torna o contexto de todos, e a alucinação é lavada em fato.

> 没有共享状态,A Ágente A's illusion parked in A's upper down文中──下游A Ágente 会重新获取或重新推导并可能捕获错误──

O problema não é o estado compartilhado em si.**without provenance and without an independent verifier**Três medidas de mitigação abordam isto:

> 问题不是共享状态本身而是**没有来源追溯和没有独立验证器**O Estado Compartilhado: Três medidas de alívio para resolver este problema:

Cada mitigação visa um modo de falha diferente. A provência permite rastrear erros de volta. A versão preserva o rastro de auditoria. O verificador não-escritível fornece uma verificação independente. Juntos, formam uma defesa profunda contra envenenamento.

> Cada tipo de medidas de alívio contra diferentes modelos de fracasso.

1. **Attribute provenance on every write.**Cada entrada em registros estaduais compartilhados quem a escreveu, quando, sob que prompt e (se aplicável) qual a fonte citada pelo agente.
   Tradução:**每次写入时归属来源。**Cada artigo no estado de comunhão registra quem escreveu, quando, em que ponto, e se for o caso, o agente cita o que é fonte.
2. **Version writes; treat them as append-only.**Uma correcção é uma nova entrada que substitui a antiga, não uma atualização no local.
   Tradução:**版本化写入；视为仅追加。**修正是一个取代旧条目的新条条,不是原地更新──审计跟踪被保留──
3. **Keep at least one agent that cannot write to shared state.**Um agente de verificação de somente leitura recolhe amostras de entradas, recorre a fontes e sinaliza inconsistências.
   Tradução:**保留至少一个不能写入共享状态的 Agent。**Apenas leitura de testes Agente 采样条目、重新获取来源并标记不一致──因为 não pode ser escrita em uma caixa, por isso não pode ser contaminada em uma caixa──

### Precedente de quadro negro (Hayes-Roth, 1985)

O padrão de quadro negro precede os agentes de LLM em quatro décadas. Hayes-Roth (1985, "A Blackboard Architecture for Control") descreveu fontes de conhecimento especializadas que observam uma tabela negra global, contribuem com soluções parciais e desencadeiam outras fontes. O quadro negro de 2026 (CA-MCP, Matrix) é o mesmo padrão com agentes LLM como fontes de conhecimento e manchas JSON como soluções parciais. A literatura antiga tem documentado soluções para escrever contenção, controle oportunista e consistência que os sistemas modernos redescobrem.

> O modelo de blackboard é mais antigo do que o de um agente LLM há quatro décadas. Hayes-Roth (em 1985, "A Blackboard Architecture for Control") descreveu a observação de um quadro negro, contribuindo para uma solução e provocando outras fontes de conhecimento especializado.

A lição de Hearsay-II (o quadro de reconhecimento de voz dos anos 1970): controle oportunista  deixando qualquer fonte de conhecimento desencadear quando sua condição de desencadeamento coincide  produz solução de problemas emergentes.

> O discurso-II ([[1970s]]) da aprendizagem: oportunidade de controlar deixar qualquer fonte de conhecimento em suas condições de correspondência quando o desencadeamento surgir em problemas de solução.

### Projeção vs visão completa

Uma placa negra pura dá a cada assinante a mesma projeção (tema-escalado).**per-agent projection**A função de redução dobra o estado global em uma fatia específica de papel.

> O quadro negro puro dá a cada assinante a mesma projeção.**每个 Agent 投影**Cada agente obtém um visual de acordo com seu papel. O status de um LongGraph é um logro típico de 2026 em que a função de um logro irá dobrar o estado geral em um pedaço específico do papel.

A projeção por agente aumenta mais, mas precisa de um esquema, sem um, você reconstrui a projeção ad hoc em cada agente.

> Cada Agente  Projeção expandindo melhor mas precisa de um modelo. Não há um modelo, você refaz uma projeção temporária em cada agente.

### Padrões de conteúdo de escrita

A escrita simultânea de vários agentes é um problema de simultâneo, não apenas um problema de LLM.

> Multidão de agentes, simultaneamente, escrever é um problema, não apenas LLM  problema.

- **Sequential writer (single producer).**Todas as cartas passam por um agente coordenador que serializa.
  Tradução:**顺序写入者（单一生产者）。**Todos os escritos são feitos por um agente coordenado.
- **Optimistic concurrency with versioning.**Cada entrada tem uma versão; os escritores falham em versão de desajuste e retestar.
  Tradução:**带版本控制的乐观并发。**Cada artigo tem uma versão; o autor não consegue fazer essa versão.
- **Topic partitioning.**Diferentes agentes possuem tópicos diferentes, não há contenção entre tópicos, requer limites de partição projetados.
  Tradução:**主题分区。**Diferente Agente  possui diferentes temas  não há conflito entre temas  precisa de divisão de fronteiras de design 

A maioria dos frameworks 2026 é padrão para o escritor sequencial porque as chamadas de LLM são lentas o suficiente para que a contenção seja rara e o gargalo de engarrafamento não dói.

> Mas a maioria dos estudantes de licenciatura em 2026 usam as regras de inscrição, porque o LLM é suficientemente lento, há poucas conflitos, não há nenhum impacto.

Quando você bate em contenção (enxame de alta produção, agentes de pesquisa paralelas escrevendo descobertas), a partição de tópicos é geralmente a solução mais barata.

> Quando você realmente encontra conflitos, a divisão de tópicos geralmente é a mais barata.

### O verificador não escritível

A maior mitigação da carga é a verificação de somente leitura.

> A maior medida de alívio é apenas o teste.

- O verificador compartilha o estado com a equipe (leia o quadro negro ou o pool).
  Tradução do inglês para "Testemunho" (em inglês: Testem)
- Verificador não tem manobra de escrita para condicionar estado  apenas para um canal de verificação separado.
  O verificador não tem um único caminho de verificação para o estado de compartilhamento.
- Verificador independentemente traz fontes citadas em escritos.
  Tradução do inglês para o inglês: 验证者独立获取写入中引用的来源──标记不一致──
- As próprias saídas do verificador são encaminhadas para um ser humano ou um agente de decisão separado, nunca voltadas para a piscina.
  O testador próprio de saída é feito pelo homem ou por um agente de decisão exclusivo, nunca voltará para o buraco.

Sem esta separação, as saídas do verificador tornam-se novas entradas na piscina, o que significa que uma piscina envenenada envenena o verificador, o que envenena as suas verificações.

> Sem essa separação, a saída do verificador se transforma em uma nova entrada na piscina, o que significa que a piscina contaminada contaminou o verificador, contaminando assim sua verificação.

Este é o princípio do verificador não-escritível: o auditor deve ser lido apenas em relação ao sistema a ser auditado.

> É o princípio imperativo de um auditor: o auditor deve ler apenas o sistema de auditoria.

## Construí-lo e realizei-o.
```figure
swarm-blackboard
```

## Construí-lo

`code/main.py`Implementa as duas topologias no STDlib Python, mais um ataque de intoxicação de brinquedo e as três mitigações.

> `code/main.py`Usando a base de padrões Python, realizou duas expansões, um ataque à contaminação de brinquedos e três medidas de alívio.

- `MessagePool` Registo de apêndice só com leitura completa.
  Tradução:`MessagePool` 线程安全的仅额日志,支持完整读取──
- `Blackboard` Pub/sub com tema-chave com assinaturas por agente.
  Tradução:`Blackboard`  basear-se em publicações/consulências, apoiar cada agente's subscrição.
- `ProvenanceEntry` todos os registros de escrita (writer, timestamp, prompt_hash, source_uri).
  Tradução:`ProvenanceEntry` Cada vez que escrevo o seu registro (s)
- `PoisoningScenario` executa uma tarefa de investigação de três agentes, onde o agente A alucina um decimal.
  Tradução:`PoisoningScenario` 运行三 Agent 研究任务, entre os quais Agent A 幻觉一个小数点――印印最终报告――
- `Verifier` um agente de somente leitura que retoma fontes e sinaliza inconsistências.
  Tradução:`Verifier` Uma fonte de recoberta não identificada apenas como agente de leitura.

Produção esperada:
- Corrida 1 (sem verificador): o 42% alucinado se propaga para o relatório final.
  Tradução do inglês para tradução inglesa:运行 1(无验证者):幻觉的 42% 传播到最终报告──
- Corrida 2 (com verificador): o verificador sinaliza a inconsistência, o grupo é rotulado "bandoado", o relatório final inclui uma retração.
  Chinese:运行 2(有验证者):验证者标记不一致,池被标记为"已标记",最终报告包含撤回──

## Use-o com o framework implementado.

`outputs/skill-memory-auditor.md`É uma habilidade que verifica o projeto de memória compartilhada de qualquer sistema multi-agente para proveniência, versão e separação de verificador.

> `outputs/skill-memory-auditor.md`É uma habilidade, auditoria de qualquer agência de sistemas de memória compartilhada no design de origem, rastreamento, controle de versão e verificação separados.

## Envia-o . Produto .

Para qualquer projeto de memória compartilhada:

> 对于任何共享内存设计:

- Registo de proveniência em cada escrita: `(writer, timestamp, prompt_hash, tool_calls_cited, source_uri)`- Não .
  Tradução do inglês:`(写入者, 时间戳, prompt_hash, 引用的工具调用, source_uri)`- Não.
- As correções são novas entradas que fazem referência à substituição.
  Chinese:使日志仅追加──修正项是引用被取代项的新条目──
- Deploia pelo menos um agente de verificação de somente leitura com acesso à fonte independente.
  Em inglês, o nome de um agente de segurança é usado para identificar os agentes de segurança.
- A saída do verificador de rota para um canal separado, não de volta para o pool compartilhado.
  Tradução do inglês para tradução do inglês:
- Registrar a proporção de escritos que são supersões  uma proporção crescente é uma evidência inicial de padrões de alucinação.
  Tradução do inglês para o inglês: record cover writing ratio upward ratio is early evidence of illusion mode

## Exercícios.

1. Corra .`code/main.py`Confirme que a primeira fase propaga a alucinação e a segunda a apanha.
   Tradução: 运行`code/main.py`❖ Confirmar a execução 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
2. Adicione uma segunda alucinação: o agente B inventa um conjunto de dados de tamanho.
   Chinese: 添加第二幻觉:Agenta B 虚构一个数据集 大小──验证者应该捕获两者而无需针对任何一个手动调优──
3. Transforma a piscina inteira para um quadro com partições de tópicos (`prices`- Não .`summaries`- Não .`analyses`Quais são os cenários de intoxicação que o tema de partição torna mais difícil de realizar, e com quais não ajuda?
   Tradução do inglês:将完整池切换为带主题分区的黑板`prices`- Não.`summaries`- Não.`analyses`■■ temática: quais são os casos de inundação mais difíceis de implementar, quais não ajudaram?
4. Leia Hayes-Roth (1985, "A Blackboard Architecture for Control"). Identifique dois padrões de controle do artigo não discutidos nesta lição que os sistemas 2026 beneficiariam.
   No entanto, o sistema de controle é um sistema de controle que pode ser usado para controlar a sua própria estrutura.
5. Leia CA-MCP (arXiv:2601.11595). Mapear seu Comércio de Contexto Compartilhado para a classe MessagePool ou Blackboard em `code/main.py`Que primitivas adiciona o CA-MCP?
   Tradução do português:阅读 CA-MCP(arXiv:2601.11595)`code/main.py`O Centro de Mensagens ou Tabela Negra 类──CA-MCP Adicionou quais linguagens originais?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Append-only log that every agent reads. Full transparency, poor scaling. / 每个 Agent 读取的仅追加日志。完全透明，扩展性差。 |
| Blackboard / 黑板 | "Shared workspace" / "共享工作区" | Topic-keyed pub/sub. Agents subscribe to relevant topics. Scales farther. / 基于主题的发布/订阅。Agent 订阅相关主题。扩展性更好。 |
| Provenance / 来源追溯 | "Who wrote what" / "谁写了什么" | Metadata on each write: writer, timestamp, prompt, sources. / 每次写入的元数据：写入者、时间戳、提示、来源。 |
| Memory poisoning / 内存污染 | "Hallucinations spreading" / "幻觉传播" | One agent's error enters shared state, downstream agents adopt it as fact. / 一个 Agent 的错误进入共享状态，下游 Agent 将其作为事实采纳。 |
| Append-only / 仅追加 | "No in-place updates" / "无原地更新" | Corrections are new entries that supersede. Preserves audit trail. / 修正项是取代旧条目的新条目。保留审计跟踪。 |
| Unwritable verifier / 不可写验证者 | "Independent auditor" / "独立审计者" | Read-only agent that re-fetches sources and flags inconsistencies. / 重新获取来源并标记不一致的只读 Agent。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Per-agent view computed from global state. LangGraph reducers are the canonical case. / 从全局状态计算的每个 Agent 视图。LangGraph 归约器是典型实现。 |
| Knowledge Source / 知识源 | "Specialist agent" / "专家 Agent" | Hayes-Roth's 1985 term for a blackboard participant. / Hayes-Roth 1985 年对黑板参与者的称呼。 |

## Mais leitura 延伸阅读

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Taxonomia MAST; intoxicação da memória é uma subfamília de falhas de coordenação
  Por que muitos agentes LLM 系统会失败?  MAST 分类法;内存污染是协调失败子家族
- [CA-MCP — Context-Aware Multi-Server MCP](https://arxiv.org/abs/2601.11595) Compartilhado conteúdo de armazenamento para servidores MCP coordenados
  中文翻译:CA-MCP  上下文感知多服务器 MCP  协调 MCP 服务器的共享上下文存储
- [Matrix — decentralized multi-agent framework](https://arxiv.org/abs/2511.21686) quadro de texto baseado em fila de mensagens sem um orquestrador central
  Tradução do inglês:Matrix  去中心化多 Agent 框架  基于消息队列的黑板,无中央编排器
- [LangGraph state and reducers](https://docs.langchain.com/oss/python/langgraph/workflows-agents) o padrão de projecção por agente na produção
  中文翻译:LangGraph 状态和归约器  生产中的每个 Agent 投影模式
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) Notas de proveniência e de verificação de uma implantação de produção
  Tradução do idioma: Antropico  Nós como construir vários agentes  Sistema de estudo  Origem da produção 
