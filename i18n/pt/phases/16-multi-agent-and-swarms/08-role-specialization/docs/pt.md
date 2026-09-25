# Role Specialization  Planeador, Crítico, Executor, Verificador   especialização  crítico  plano 角色

> A decomposição mais comum de multi-agentes em 2026: um agente planeja, um executa, um critica ou verifica. MetaGPT (arXiv:2308.00352) formaliza isso como SOPs codificados em instruções de papel  Product Manager, Architect, Project Manager, Engineer, QA Engineer  seguintes `Code = SOP(Team)`- Não . ChatDev (arXiv:2307.07924) cadeia designer, programador, revisor, testador através de uma "cadeia de bate-papo" com "desalucinação comunicativa" (agentes explicitamente solicitar detalhes faltantes). O verificador é resistente à carga: Cemri et al. (MAST, arXiv:2503.13657) mostram que cada falha multi-agente pode ser rastreada para a verificação faltante ou falhada. A PwC relatou um ganho de precisão de 7x (10% → 70%) a partir de ciclos de validação estruturados na CrewAI.

> **【中文解读】**Esta secção apresenta a especialização de papéis para cada agente, distribuindo papéis e especialidades definidas, para melhorar a eficiência da equipe em geral.

> **【拓展：role specialization→具体应用】**A especialização de papéis é o principal conceito da CrewAI. Cada agente tem um papel. O papel é o objetivo. O objetivo é o contexto. A prática mostra que a definição de papéis definida pode melhorar significativamente a eficiência de cooperação entre vários agentes.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 05 (Supervisor) | **前置知识:** Phase 16 · 04 (Primitive Model), Phase 16 · 05 (Supervisor)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**學本節前 請先掌握:Fase 16·04-05 原语+Supervisor) 本節是2026 最常见的多代理 分解模式:Planner + Critic + Executor + Verifier──
> - Não .**【类比】**角色专业化 = "filme制作团队"──Planner = 编剧(定方向)、Executor = 演员(执行)、Critic = 内审、Verifier = 质检员──MetaGPT、ChatDev、CrewAI 都用这种角色分解──Cemri 等人 MAST论文:所有多 Agent 失败都可追溯到"缺少或破损的验证人"验证是承重墙──PwC 案例:加验证人 让准确率从10% 到70% 7倍)──

## Problema Introdução

Os sistemas multi-agentes genéricos produzem saída genérica. Três programadores em um chat de grupo escrevem três sabores do mesmo código mediocre. Você pode adicionar mais agentes, adicionar mais rodadas e ainda não cruzar o limiar de qualidade.

> O sistema de vários agentes gera uma saída geral. Os três editores do grupo de conversação escreveram três tipos de códigos de sabor semelhante.

O problema não é a quantidade, mas a uniformidade. Três agentes idênticos, dada a mesma tarefa, produzirão três respostas erradas semelhantes. Eles compartilham os mesmos pontos cegos porque compartilham o mesmo impulso e modelo. Adicionar mais do mesmo não ajuda; você precisa de agentes que são diferentes de maneiras produtivas.

>  problema não é quantidade, mas sim qualidade.  três agentes iguais  dado a mesma tarefa gerar três respostas de erro semelhantes   eles compartilham o mesmo ponto de vista porque compartilham as mesmas dicas e modelos                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

A solução não é mais agentes  é * diferentes * agentes. atribuir papéis distintos. Dar as ferramentas críticas que o planejador não tem. Dar ao verificador um conjunto de testes objetivos. Agora o sistema tem desacordo interno com a correção fundamentada, não apenas adivinhação paralela.

> O método de reparação não é mais Agente, mas sim Agente* diferente. Distribuir diferentes papéis.

A mudança chave: de "mais agentes fazendo a mesma coisa" para "agentes diferentes fazendo coisas diferentes". O paralelo sem especialização é apenas um adivinho caro.

> 关键转变: de "mais agentes fazerem o mesmo" a "diferentes agentes fazerem coisas diferentes"― não há conexão especializada apenas costosa conjectura― especialização criação faz com que o sistema capte seus próprios erros de incomparência―

## Conceptos básicos

### Os quatro papéis canônicos

**Planner.**Leia o objetivo, produz uma lista de passos ou uma especificação Ferramentas: recuperação de conhecimentos, documentos.

> **规划者。**读取目标,产生步骤列表或规范──工具: conhecimento, investigação, documentação, produção, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento, desenvolvimento e desenvolvimento.

**Executor.**Leia um plano passo a passo, produz o artefato. Ferramentas: as ferramentas de trabalho reais (compilador de código, shell, cliente API).

> **执行者。**Cada vez que você começa a ler um plano, você começa a fazer um trabalho.

**Critic.**Leia a saída do executor contra a intenção do planejador. Ferramentas: acesso apenas para leitura do artefato, análise estática.

> **批评者。**根据规划者意图阅读执行者输出──工具:对工件的只读访问、静态分析──输出: aceitar/rechazar及原因──

**Verifier.**Leia o artefato e executa uma verificação determinista. Ferramentas: test runner, verificador de tipo, validador de esquema.

> **验证者。**读取工件并运行确定性检查──工具:测试运行器、类型检查器、模式验证器──输出:通过/失败及证据──

O crítico é subjetivo, opinado, muitas vezes baseado em LLM. O verificador é objetivo, determinista, muitas vezes baseado em código.

> Os críticos são objetivos, têm opiniões, geralmente baseados em LLM, verificadores são objetivos, de certeza, geralmente baseados em código, não são o mesmo papel.

A conflação é o erro de design mais comum de vários agentes. Um sistema com apenas críticos (revisores LLM) obtém resultados plausíveis mas errados. Um sistema com apenas verificadores (verificações de código) obtém resultados corretos mas feios. Você precisa de ambos: crítico pelo gosto, verificador pela corretão.

> Misturar-as para uma conversa é o mais comum de muitos agentes design errors. Apenas os críticos LLM reviewer) sistemas obtêm semelhante e não mas errados de saída. Apenas os verificadores code check) sistemas obtêm resultados corretos mas péssimos.

### Padrão de SOP do MetaGPT

MetaGPT (arXiv:2308.00352) codifica os SOPs de engenharia de software como instruções de papel:

> MetaGPT(arXiv:2308.00352)将软件工程 SOP 编码为角色提示:

O enquadramento de "SOP" é emprestado de organizações humanas: Procedimentos Operacionais Padrão transformam o trabalho ad hoc em processo repetível. MetaGPT aplica isso aos LLM  o SOP se torna um sistema de prompt que restringe o LLM a um papel específico com saídas específicas.

> O quadro "SOP" leva-se da organização humana: o processo de operação padrão irá transformar o trabalho temporário em processo repetivel.

- **Product Manager**- O PRD escreve.
  Tradução:**产品经理**编写 PRD。
- **Architect**produz o projeto do sistema.
  Tradução:**架构师**产生系统设计──
- **Project Manager**Divide as tarefas.
  Tradução:**项目经理**- Desligar as tarefas.
- **Engineer**- os instrumentos.
  Tradução:**工程师**Realização:
- **QA Engineer**- Faz testes.
  Tradução:**QA 工程师**运行测试──

Cada função tem um esquema de entrada/saída rigoroso.`Code = SOP(Team)`A formulação  SOPs deterministas transformam uma equipa de LLM num pipeline previsível.

> Cada papel tem um padrão de entrada/saída rigoroso.`Code = SOP(Team)`O SOP vai transformar uma equipe de LLM em uma linha de fluxo previsível.

A principal ideia: codificar o fluxo de trabalho da equipe como código, não como conversa. Cada papel de LLM é um nó em um gráfico determinista; a estrutura do gráfico é escrita pelo homem. Os LLM fazem o trabalho local; os seres humanos possuem o fluxo de trabalho global.

> 关键洞察:将团队工作流编码为代码,而不是对话――每个 LLM 角色是确定性图中的节点;图结构由人类编写――LLM 做局部工作;人类拥有全局工作流――

### A desalucinação comunicativa do ChatDev.

ChatDev adiciona um movimento chave: quando um executor precisa de um detalhe específico que não estava no plano, ele pergunta explicitamente ao designer antes de continuar.

> ChatDev adicionou uma iniciativa fundamental: quando um executivo precisa de detalhes específicos que não existem no plano, ele pergunta claramente ao designer antes de continuar.

O padrão capta alucinações na sua fonte. Em vez de detectar detalhes fabricados após o fato (duro), ele impede a fabricação exigindo que o executor pergunte antes de assumir. O custo é uma viagem de ida e volta extra; o benefício é a corretão.

> O modelo é a captura de ilusões, não o teste de ficção por trás do fato, mas através do requisito de um executor fazer uma pergunta para evitar a ficção.

Implementação: o prompt de função inclui "quando você precisa de informações específicas que não lhe foram dadas, pergunte pelo nome do papel relevante antes de produzir a saída".

> 实现:角色提示包括"quando você precisa de informações específicas que você não é fornecido, antes de produzir o output, por nome pergunte os roles relacionados".""

### Por que o verificador é mais importante

Cemri et al. (MAST) rastreou 1642 falhas de execução de vários agentes. 21,3% foram falhas de verificação  o sistema enviou uma resposta que ninguém tinha verificado. Os restantes 79% muitas vezes remontam a "havia um cheque que falhou silenciosamente ou nunca foi executado". Verificação é o papel de carga.

> Cemri 等人(MAST) rastreou 1642 agentes  executar falhas。21.3% é a deficiência de verificação sistema publicou respostas que ninguém verificou。 o restante 79% geralmente se remonta a "uma verificação silenciosamente falhou ou nunca funcionou"。

O número 21,3% é a estatística mais citada em 2026 em engenharia multi-agente. Diz: se você adicionar apenas um papel ao seu sistema, torne-o um verificador. Não um crítico, não um planejador  um verificador determinista com verificações de nível de código.

> 21,3% Este número é o mais citado em estatísticas de 2026 em mais de um agente. Diz: se você apenas adicionar um papel ao sistema, deixe-o ser verificador. Não é crítico, não é programador.

A PwC relatou (CrewAI deployments, 2025) que a adição de um ciclo de validação estruturada mudou a precisão de 10% para 70%.

> O relatório da PwC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

### Critico vs verificador

- Um crítico é um Mestrado em Direito que avalia um artefato por qualidade.
  O crítico é um LLM de qualidade de um objeto de revisão.
- Um verificador é um programa determinista que funciona no artefato. Objetivo. Dá pass/falha com evidências.
  O verificador é um processo de determinação executado no trabalho.

Use ambos. O crítico detecta problemas de sabor que o verificador não pode articular. O verificador detecta bugs que o crítico não pode ver porque eles aparecem apenas no tempo de execução.

>  ambos usam                                                                                                                                                                                                                                                            

Uma ordem comum: primeiro verificador (rápido, mata o trabalho obviamente quebrado), depois crítico (lento, refina a qualidade). Algumas equipes viram a ordem para detectar problemas de sabor antes de gastar computação em código quebrado.

> 常见顺序:先验证者(快,杀死明显破损工作),然后批评者(慢,精炼质量) ・・・ alguns grupos de trabalho transformaram-se em ordem de trabalho para capturar o problema de qualidade antes de recuperar o código de perdas.

### O anti-patrão

Cada papel no seu sistema é um LLM e cada papel é "parece-me bem". Modo de falha MAST clássico. Adicione pelo menos um verificador cujo pass/falha é decidido por código, não por um LLM.

> Cada papel no sistema é LLM, cada papel é "parece errado" e é "exato" e é "exato".

### Mapas de quadro

- **CrewAI**- Não .`Agent(role, goal, backstory)`é a superfície de especialização dos livros didáticos.
  Tradução:**CrewAI**- Não .`Agent(role, goal, backstory)`É a superfície de especialização do ensino.
- **LangGraph**Os nós podem ter indicações especializadas; as bordas reforçam o pipeline.
  Tradução:**LangGraph** 节点可以有专门提示;边强制流水线──
- **AutoGen** Agentes conversáveis específicos de função com nomes de uma palavra em um Chat de Grupo.
  Tradução:**AutoGen** Em GroupChat, um agente conversável tem um papel específico.
- **OpenAI Agents SDK** Transferência de ferramentas entre agentes especializados em funções.
  Tradução:**OpenAI Agents SDK** 角色专业化 Agente 间交接工具──

## Construí-lo e realizei-o.
```figure
swarm-roles
```

## Construí-lo

`code/main.py`Implementa um pipeline de 4 funções construindo uma função Python simples:

> `code/main.py`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

- **Planner**produz uma especificação.
  Tradução:**规划者**产生规范── Não é o que se passa?
- **Executor**gera uma cadeia de código.
  Tradução:**执行者**O que é que eu faço?
- **Critic**(SIMULADO DE MULTIMENTO) sinaliza problemas óbvios.
  Tradução:**批评者**(LLM 模拟) 标记明显问题──
- **Verifier**executa o código gerado em uma caixa de areia (`exec`) contra um caso de ensaio.
  Tradução:**验证者**Em uma caixa`exec`) em termos de testes de uso de casos de execução gerados de código.

Demo é executado duas vezes: uma vez quando o executor produz código correto (crítica + verificador ambos passam), uma vez quando o executor produz código off-spec (crítica perde o bug porque parece plausível, verificador pegou porque o teste falha).

> 演示运行两次:一次执行者产生正确的代码(批评者 + 验证者都通过),一次执行者产生偏离规范的代码(批评者因为看起来合理而错过错误,验证者因为测试失败而捕获它) ]]

## Use-o com o framework implementado.

`outputs/skill-role-designer.md`O sistema de verificação de dados é um sistema de verificação de dados que permite a verificação de dados.

> `outputs/skill-role-designer.md`接收任务并产生角色名册(3-5 个角色) 、 cada papel de entrada/saída mode y verificador chequear──在将 Agent 连接到框架之前使用──

## Envia-o . Produto .

Lista de verificação:

> 检查清单:

- **At least one deterministic verifier.**Nunca tudo-LLM.
  Tradução:**至少一个确定性验证者。**Não quero nunca o LLM.
- **Explicit I/O schema per role.**O planejador retorna uma especificação, não prosa; o executor lê esse esquema.
  Tradução:**每个角色有明确的 I/O 模式。**规划者回归规范, não散文; execução
- **Communicative dehallucination.**O executor deve perguntar ao planejador quando falta informação; nunca a invente.
  Tradução:**交流去幻觉。** Executor em falta de informação deve perguntar ao planejador; nunca inventar.
- **Critic/verifier ordering.**Execute primeiro o crítico (barato, detecta problemas de design), segundo o verificador (lento, detecta bugs).
  Tradução:**批评者/验证者顺序。**Previamente, o programa foi lançado em outubro de 2015.
- **Loop budget.**Max 2 revisão de crítico-executivo rodadas antes de escalar para humano.
  Tradução:**循环预算。**O máximo de 2 críticos-executivos antes de ser submetido ao nível humano.

## Exercícios.

1. Corra .`code/main.py`E observe como o verificador detecta o bug que o crítico perdeu. Adicione uma verificação de análise estática (contar ocorrências de `return`O que é que ele pega quando o teste de tempo de execução falha?
   Tradução: 运行`code/main.py`Não observe como o testador pega o erro do crítico.`return`O que foi capturado durante a operação?
2. Adicione um quinto papel: "analista de requisitos" que traduz o desejo do usuário em especificação pronta para planejamento.
   Chinese: 添加第五个角色:"需求分析师",将用户愿望翻译为规范可用规范──什么样的交流去幻觉请求应该流上方?
3. Leia a secção 3 do MetaGPT ("Agentes"). Enumere o esquema de entrada/saída de cada uma das 5 funções do MetaGPT.
   中文翻译:阅读 MetaGPT 第 3 节("Agente")。列出 MetaGPT 5 个角色中每个的输入/输出模式──
4. Leia o diagrama da cadeia de bate-papo do ChatDev (arXiv:2307.07924 Figura 3). Identifique onde a desalucinação comunicativa quebra um ciclo que de outra forma seria infinito.
   Chinese: 阅读 ChatDev 的聊天链图(arXiv:2307.07924 图 3)  Identificação de um diálogo entre os seres humanos
5. O ganho de precisão 7x da PwC veio de loops de verificação.
   Chinese Translation:PwC 7 vezes a taxa de precisão de aumento de provimento do ciclo de verificação.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Role specialization / 角色专业化 | "Different agents, different jobs" / "不同 Agent，不同工作" | Distinct system prompts tuned for planner/executor/critic/verifier roles. / 为规划者/执行者/批评者/验证者角色调优的独特系统提示。 |
| SOP pattern / SOP 模式 | "Encoded standard operating procedure" / "编码标准操作流程" | MetaGPT's framing: strict I/O schemas per role turn a team into a pipeline. / MetaGPT 的框架：每个角色的严格 I/O 模式将团队变成流水线。 |
| Communicative dehallucination / 交流去幻觉 | "Ask before inventing" / "先问再发明" | ChatDev pattern: executor asks planner when a detail is missing rather than making one up. / ChatDev 模式：执行者在细节缺失时询问规划者而不是编造。 |
| Critic / 批评者 | "LLM reviewer" / "LLM 审阅者" | Subjective, opinionated reviewer. Catches taste issues. Can be fooled by plausible prose. / 主观的、有观点的审阅者。捕获质量问题。可以被似是而非的散文愚弄。 |
| Verifier / 验证者 | "Deterministic check" / "确定性检查" | Code-based pass/fail. Test runner, type checker, schema validator. Cannot be fooled. / 基于代码的通过/失败。测试运行器、类型检查器、模式验证器。不能被愚弄。 |
| Verification gap / 验证缺口 | "No one checked" / "没人检查" | 21.3% of MAST failures. Answer shipped without a check that would have caught the bug. / 21.3% 的 MAST 失败。发布答案时没有会捕获 bug 的检查。 |
| Revision loop / 修订循环 | "Critic sends it back" / "批评者打回" | Critic rejection triggers executor re-run with feedback. Needs a budget. / 批评者拒绝触发带反馈的执行者重新运行。需要预算。 |
| All-LLM anti-pattern / 全 LLM 反模式 | "Looks good to me" / "看起来不错" | Every role is an LLM, no deterministic check. Classic MAST failure. / 每个角色都是 LLM，没有确定性检查。经典的 MAST 失败。 |

## Mais leitura 延伸阅读

- [Hong et al. — MetaGPT: Meta Programming for Multi-Agent Collaboration](https://arxiv.org/abs/2308.00352) O documento de referência de PEC-as-roles
  中文翻译:Hong 等人  MetaGPT:多 Agent 协作的元编程  SOP 作为角色提示的参考论文
- [Qian et al. — Communicative Agents for Software Development (ChatDev)](https://arxiv.org/abs/2307.07924) Cadeia de bate-papo + desalucinação comunicativa
  Chinese:   软件开发的通信代理 聊天链 + 交流去幻觉
- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Taxonomia MAST; as lacunas de verificação representam 21,3% das falhas
  Chinese Translation:Cemri 等人  Por que muitos agentes LLM 系统会失败? MAST 分类法;验证缺口占失的21.3%
- [CrewAI docs — Agent roles](https://docs.crewai.com/en/introduction) superfície de especificação de papel de produção
  中文翻译:CrewAI 文档  Agente 角色  生产角色规范表面
