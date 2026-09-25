# Porquê Multidimensional?

> Um agente bate numa parede, o movimento inteligente não é um agente maior, é mais agentes.

> **【中文解读】**Esta secção apresenta por que é necessário mais Agente  Sistema  Single Agente                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

> **【拓展：why multi agent→具体应用】** Agente único em processamento de tarefas complexas enfrentam três garrafas:  1) 上下文溢出所有信息塞进一个窗口,重要被淹没; 2) 角色混乱 一个代理扮演多角色导致提示词冲突; 3) 串行执行工具调用只能排队――多代理 通过分工协作解决这些问题――Antropic research indicates,多代理系统在BrowseComp 基准上多代理系统 升 90.2%,80% 方仅由代币使用解释量而差量――

> - Não .**【前置】**O que é que é o "Agentação de Agentes" (Fase 14? 1)? O que é que é o "Agentação de Agentes"?

> - Não .**【类比】**单 Agent vs 多 Agent = 全能管家 vs 专业团队──全能管家──单 Agent) 能干所有事但每件事都不精:上午做饭、下午修车、晚上辅导作业,每样都半吊子──专业团队──多 Agent:厨师专做饭、机修工专修车、家教专辅导,每个人精一行──代价:协调成本(Agent 间通信) 和复杂度增加简单任务单 用 Agent 更划算──

**Type:** Learn | **类型:** 学习
**Languages:** TypeScript | **语言:** TypeScript
**Prerequisites:** Phase 14 (Agent Engineering) | **前置知识:** Phase 14 (Agent 工程)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizagem

- Identificar o limite máximo de um agente único (excesso de conteúdo, experiência mista, garganta de engarrafamento sequencial) e explicar quando dividir em vários agentes é a melhor medida
  Tradução do inglês para tradução do inglês para inglês para tradução do inglês para inglês para inglês para tradução do inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês
- Compare padrões de orquestração (pipeline, fan-out paralelo, supervisor, hierárquico) e selecione o certo para uma dada estrutura de tarefa
  Tradução do inglês para tradução do inglês para inglês: comparar estruturas de montagem (流水线、并行扇出、监督者、分层),并为给定任务结构选择合适的模式
- Projetar um sistema multi-agente com limites claros de papel, estado compartilhado e contrato de comunicação
  Tradução do inglês para Chinês: Design a multi-agent  sistema de um estado de partilha e de um acordo de comunicação
- Analisar as compensações da complexidade multi-agente (latencia, custo, dificuldade de depuração) versus a simplicidade de um único agente
  Tradução em inglês: analysis multiple agent  complexity (em inglês: analysis multiple agent  complexity)

## O problema é o problema da introdução

Você construiu um único agente na Fase 14. Funciona. Ele pode ler arquivos, executar comandos, ligar para APIs e argumentar sobre resultados. Depois você aponta para uma base de código real: 200 arquivos, três idiomas, testes que dependem de infraestrutura e um requisito para pesquisar APIs externas antes de escrever código.

> Você construiu um único agente na Fase 14. Ele funciona bem, consegue ler documentos, executar ordens, usar API e fazer inferências sobre os resultados. Depois você o direcionará a uma verdadeira biblioteca de códigos: 200 documentos, três idiomas, testes de dependência de infraestrutura, bem como necessidades de primeiro estudar as exigências externas da API para reeditar código.

A diferença entre agentes de demonstração e agentes de produção é a diferença entre "um arquivo, uma língua, uma ferramenta" e "muitos arquivos, muitas línguas, muitas ferramentas com dependências". A demonstração funciona porque a tarefa se encaixa.

> A diferença entre Agente e Produtor Agente é a diferença entre "um documento, uma linguagem, um instrumento" e "muitos documentos, muitas linguagens, muitos instrumentos dependentes".

O agente se esmaga. Não porque o LLM seja estúpido, mas porque a tarefa excede o que um agente loop pode lidar. A janela de contexto se enche de conteúdo de arquivo. O agente esquece o que leu 40 chamadas de ferramenta atrás. Ele tenta ser um pesquisador, um codificador e um revisor de uma só vez, e faz mal os três.

> O agente                                                                                                                                                                                                                                                              

Este é o teto de agente único, é atingido sempre que uma tarefa requer:

> É o único agente que tem a sua limitação.

O teto é estrutural, não algorítmico. Um LLM melhor retarda o teto, mas não o remove. Uma janela de contexto de 1M-token preenche com tanta certeza quanto um 200k  só leva mais arquivos.

> A limite superior é estrutural, não algorítmica. O melhor LLM é atrasado, mas não se move.

- **More context than fits in one window**- ler 50 arquivos passa 200 mil tokens
  Tradução:**超出一个窗口容量的上下文** 读取 50 文件会超过200k token
- **Different expertise at different stages**- a investigação exige uma motivação diferente da geração de código
  Tradução:**不同阶段需要不同的专业知识** Os estudos precisam de diferentes proposições para gerar código
- **Work that can happen in parallel**- Porque ler três arquivos sequencialmente quando você pode lê-los simultaneamente?
  Tradução:**可以并行执行的工作**Se podemos ler três documentos ao mesmo tempo, por que é que temos de ler?

## O conceito central.

### O teto de um só agente

Um único agente é um loop, uma janela de contexto, um sistema de instruções.

> Um agente é um ciclo, uma janela de texto, um sistema de informação.

```
┌─────────────────────────────────────────┐
│            SINGLE AGENT                 │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │         Context Window            │  │
│  │                                   │  │
│  │  research notes                   │  │
│  │  + code files                     │  │
│  │  + test output                    │  │
│  │  + review feedback                │  │
│  │  + API docs                       │  │
│  │  + ...                            │  │
│  │                                   │  │
│  │  ██████████████████████ FULL ███  │  │
│  └───────────────────────────────────┘  │
│                                         │
│  One system prompt tries to cover       │
│  research + coding + review + testing   │
│                                         │
│  Result: mediocre at everything         │
└─────────────────────────────────────────┘
```

O sistema único de instruções é a causa raiz. Ele tem que dar instruções para pesquisa, codificação, revisão e teste simultaneamente. Cada instrução diluir os outros. O agente acaba "ok" em tudo, excelente em nada.

> 单系统提示是根本原因――它必须同时为研究,编码,审核和测试提供指令――每条指令稀释其他――Agent 最终在所有事上"还行",在任何事上都不优秀――

Três coisas quebram:

> Três problemas levarão ao colapso:

1. **Context saturation**A partir da curva 30, o agente já consumiu 150 mil tokens de conteúdo de arquivo, saídas de comando e raciocínio prévio.
   Tradução:**上下文饱和** 工具结果不断堆积──到第30轮时,Agent 已消耗了150k tokens 文件内容、命令输出和先前推理──第5轮关键细节丢失──

2. **Role confusion**- um sistema de instruções que diz "você é um pesquisador, codificador, revisor e testador" produz um agente que metade pesquisa, metade código, e nunca termina a revisão.
   Tradução:**角色混乱** Um sistema de sugestões que escreve "tu és pesquisador, programador, revisor e testador" produz um meio estudo, meio código, sempre incompleto agente de revisão.

3. **Sequential bottleneck**- O agente lê o arquivo A, depois o arquivo B, depois o arquivo C. Três chamadas de LLM em série, três execuções em série de ferramentas.
   Tradução:**串行瓶颈** Agente 读取文件 A,然后文件 B,然后文件 C──三次串行 LLM 调用──三次串行工具执行──没有并行性──

O agente único é um generalista que é solicitado a ser especialista em cada etapa.

> Um agente é um requisito para se tornar um especialista em cada passo.

### A solução multi-agente

Divida o trabalho, dá a cada agente um trabalho, uma janela de contexto e um sistema de resposta ajustada para esse trabalho:

> 拆分工作── dá a cada agente uma tarefa、 uma janela de texto acima e uma dica do sistema para a tarefa:

Esta é a "separação de preocupações" aplicada aos agentes LLM. O pedido de cada agente é mais curto e mais focado. A janela de contexto de cada agente só possui o que precisa. Cada agente pode ser testado e melhorado de forma independente. O orquestrador lida com a composição.

> É aplicado ao "foco de atenção" do Agente LLM. Cada agente tem um ponto de atenção mais curto e mais focado.

```
┌──────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                          │
│                                                          │
│  "Build a REST API for user management"                  │
│                                                          │
│         ┌──────────┬──────────┬──────────┐               │
│         │          │          │          │               │
│         ▼          ▼          ▼          ▼               │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│   │RESEARCHER│ │  CODER   │ │ REVIEWER │ │  TESTER  │  │
│   │          │ │          │ │          │ │          │  │
│   │ Reads    │ │ Writes   │ │ Checks   │ │ Runs     │  │
│   │ docs,    │ │ code     │ │ code     │ │ tests,   │  │
│   │ finds    │ │ based on │ │ quality, │ │ reports  │  │
│   │ patterns │ │ research │ │ finds    │ │ results  │  │
│   │          │ │ + spec   │ │ bugs     │ │          │  │
│   └─────┬────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│         │           │            │             │         │
│         └───────────┴────────────┴─────────────┘         │
│                          │                               │
│                     Merge results                        │
└──────────────────────────────────────────────────────────┘
```

Cada agente tem:
- Um sistema focado de solicitação ("Você é um revisor de código. Seu único trabalho é encontrar bugs. ")
  Tradução do inglês para o inglês: a.s.
- O seu próprio quadro de contexto (não poluído pelo trabalho de outros agentes)
  Tradução do inglês:
- Um contrato de entrada/saída claro (recebe notas de investigação, código de saída)
  Tradução em inglês: klar klar klar klar的输入/输出契约

O agente orquestador só precisa entender a tarefa de alto nível e como delegar. Ele não precisa saber como fazer cada subtarefa. Cada agente especializado só precisa saber seu próprio trabalho estreito.

> 编排 Agente só precisa entender tarefas de alto nível e como as comisar. Não precisa saber como completar cada subtarefa.

### Sistemas reais que fazem isso

**Claude Code subagents**- quando Claude Code gera um subagente com`Task`O pai mantém o contexto limpo, o filho trabalha focado e retorna um resumo.

> **Claude Code 子 Agent** 当 Claude Code 使用 `Task`Quando um agente é criado, ele cria um agente de um grupo limitado.

O padrão é viral porque compõe: um subagente pode gerar seus próprios subagentes. Três níveis de profundidade é comum em tarefas complexas de base de código; além disso, o depuração torna-se doloroso.

> Este modelo viral se espalha porque pode ser combinado: Sub-Agent pode gerar seu próprio Sub-Agent.

**Devin**- executa um agente de planejamento, um agente de codificação e um agente de navegador. O planejador divide o trabalho em etapas. O codificador escreve código. O navegador pesquisa a documentação. Cada um tem contexto separado.

> **Devin** 运行一个规划代理一个编码代理 和一个浏览器代理――规划器将工作分解成步骤――编码器编写代码――浏览器研究文档――cada um tem seu próprio 上下文――

A arquitetura de Devin é o padrão de supervisor de livros didáticos: um planejador que possui o plano global, vários trabalhadores especializados que executam fatias.

> A estrutura de Devin é um modelo de supervisor do ensino básico: um planejador que possui um plano global, vários trabalhos de especialistas executando pedaços.

**Multi-agent coding teams (SWE-bench)**- os sistemas de melhor desempenho no banco SWE utilizam um pesquisador que lê a base de código, um planejador que desenha a correcção e um codificador que a implementa.

> **多 Agent 编码团队 (SWE-bench)** SWE-bench superior melhor desempenho do sistema usando um pesquisador de uma biblioteca de código de leitura, um planejador de um programa de revisão de design e um codificador de revisão de implementação.

O quadro de liderança do banco SWE 2026 é dominado por sistemas multi-agentes. O padrão: um pesquisador com um grande contexto para a compreensão de base de código, um planejador com um prompt focado para o projeto de fixação, um codificador com requisitos de digitação rigorosos para a implementação. Cada papel recebe o prompt que precisa.

> 2026 ano SWE-bench  ranking by multiple Agent system dominado。模式:带大上下文的研究员用于代码库理解、带焦点提示的规划器用于修复设计、带严格类型要求的编码器用于实现──每个角色获得其需要的提示──

**ChatGPT Deep Research**- gerar múltiplos agentes de busca em paralelo, cada um explorando um ângulo diferente, e depois sintetizar os resultados.

> **ChatGPT Deep Research** E gerar vários agentes de busca, cada explorar diferentes ângulos, então reunir resultados.

### O Espectro

O multi-agente não é binário, é um espectro:

> Do agente não é de dois. É uma espectrosfera.

O enquadramento do espectro importa porque a maioria dos sistemas de produção não estão em nenhum dos extremos. Claude Code usa subagentes (um nível de profundidade). Devin usa uma equipe pequena. Sistemas de pesquisa reais usam 5-50 agentes.

> O quadro de espectro é importante, pois a maioria dos sistemas de produção não está em um extremo.

```
SIMPLE ──────────────────────────────────────────── COMPLEX

 Single        Sub-         Pipeline      Team         Swarm
 Agent         agents

 ┌───┐       ┌───┐        ┌───┐───┐    ┌───┐───┐    ┌─┐┌─┐┌─┐
 │ A │       │ A │        │ A │ B │    │ A │ B │    │ ││ ││ │
 └───┘       └─┬─┘        └───┘─┬─┘    └─┬─┘─┬─┘    └┬┘└┬┘└┬┘
               │                │        │   │       ┌┴──┴──┴┐
             ┌─┴─┐          ┌───┘───┐    │   │       │shared │
             │ a │          │ C │ D │  ┌─┴───┴─┐    │ state │
             └───┘          └───┘───┘  │  msg   │    └───────┘
                                       │  bus   │
 1 loop      Parent +      Stage by    │       │    N peers,
 1 context   child tasks   stage       └───────┘    emergent
                                       Explicit      behavior
                                       roles
```

**Single agent**- Um loop, um prompt.

> **单 Agent** Um ciclo, uma dica.

**Subagents**- um pai gera filhos para subtarefas focalizadas. o pai mantém o plano. os filhos relatam. é o que Claude Code faz.

> **子 Agent** O pai Agente é focado em sub-tarefa geradora  O pai Agente                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

**Pipeline**- agentes executam em sequência. A saída do agente A torna-se a entrada do agente B. Bom para fluxos de trabalho em etapas: pesquisa -> código -> revisão -> teste.

> **流水线** Agente 顺序运行──A saída do Agente A se torna entrada do Agente B──适合分阶段的工作流:研究 -> 编码 -> 审阅 -> 测试──

**Team**- Agentes funcionam em paralelo com um bus de mensagens compartilhado cada um tem um papel um orquestrador coordena bom quando diferentes habilidades são necessárias simultaneamente

> **团队** Agente 通過共享消息总线并行运行──每个都有角色──编排器协调──适应需要同时使用不同技能的场景──

**Swarm**- muitos agentes idênticos ou quase idênticos com estado compartilhado.

> **群体**  许多相同或近似相同的代理 共享状态――没有固定的编排器――Agenta de obter trabalho de uma fila――适合高吞吐量的并行任务――

### Os quatro padrões multi-agentes

#### Modelo 1: oleoduto

```
Input ──▶ Agent A ──▶ Agent B ──▶ Agent C ──▶ Output
          (research)  (code)      (review)
```

Cada agente transforma os dados e os transmite, simples de raciocinar, mas o fracasso numa fase bloqueia o resto.

> Cada agente transfere dados e transmite para o próximo.

Use quando: cada etapa tem uma entrada/saída clara e os estágios são naturalmente sequenciais. Pesquisa → código → revisão → teste é o exemplo canônico. Evite quando: estágios podem correr em paralelo ou precisam de iteração entre eles.

> Use Caso: cada fase tem uma clara entrada/saída e fase natural de execução.

#### Padrão 2: Fan-out / Fan-in

```
                ┌──▶ Agent A ──┐
                │              │
Input ──▶ Split ├──▶ Agent B ──├──▶ Merge ──▶ Output
                │              │
                └──▶ Agent C ──┘
```

Dividir o trabalho em agentes paralelos, depois fundir os resultados.

> A partir de então, o resultado será distribuído para um agente em linha para que possa ser dividido em tarefas independentes.

Use quando: a tarefa se divide limpo em peças independentes (por exemplo, pesquise 5 fontes diferentes, resuma 10 documentos). Evite quando: subtarefas dependem umas das outras ou a fusão requer um raciocínio profundo.

> Utiliza cenário: tarefas podem ser claramente divididas em partes independentes (como pesquisa 5 个不同来源、总结 10 份文档)  evitar:

#### Modelo 3: Orquestra-Trabalhador

```
                    ┌──────────┐
                    │  Orch.   │
                    └──┬───┬───┘
                  task │   │ task
                 ┌─────┘   └─────┐
                 ▼               ▼
           ┌──────────┐   ┌──────────┐
           │ Worker A │   │ Worker B │
           └──────────┘   └──────────┘
```

Um orquestrador inteligente decide o que fazer, delega aos trabalhadores e sintetiza os resultados.

> O organizador inteligente decide o que fazer, envia para o operador, e compõe os resultados. O organizador em si é um agente de ferramentas de gerar o operador.

Usar quando: a tarefa é complexa o suficiente para que decidir o que fazer seja um problema difícil.

> Utilize Caso: tarefas suficientemente complexas, decidir o que fazer em si é um problema.

#### Patrão 4: Escolha de pares

```
         ┌───┐ ◄──── msg ────▶ ┌───┐
         │ A │                  │ B │
         └─┬─┘                  └─┬─┘
           │                      │
      msg  │    ┌───────────┐     │ msg
           └───▶│  Shared   │◄────┘
                │  State    │
           ┌───▶│  / Queue  │◄────┐
           │    └───────────┘     │
      msg  │                      │ msg
         ┌─┴─┐                  ┌─┴─┐
         │ C │ ◄──── msg ────▶ │ D │
         └───┘                  └───┘
```

Não há orquestra central, os agentes comunicam entre pares, as decisões surgem da interação, mais difícil de depurar, mas a escala é de muitos agentes.

> 没有中央编排器──Agent 间点对点通信──决策从交互中涌现──更难调试,但可以扩展到许多Agent──

Utilize quando: muitos agentes homogéneos que realizam trabalhos semelhantes (descorrência, classificação) em escala.

> Use Casinos: muitos agentes de qualidade fazer trabalhos similares em grande escala.

### Quando não usar multi-agente

Multi-agente adiciona complexidade. Cada mensagem entre agentes é um ponto de falha potencial. Debug vai de "leia uma conversa" para " rastrear mensagens em cinco agentes".

> Do agente  aumentou a complexidade. Cada mensagem entre os agentes é um potencial falha.

**Stay single-agent when:**
- A tarefa cabe em uma janela de contexto (menos de ~ 100k tokens de dados de trabalho)
  Tradução do inglês para japonês:任务适合一个上下文窗口 (task suits a one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on one on the other)
- Não é preciso diferentes instruções do sistema para diferentes etapas
  Tradução do inglês:不同阶段不需要不同的系统提示
- A execução sequencial é rápida o suficiente.
  Tradução do inglês:
- A tarefa é simples o suficiente para que a divisão adicione mais gastos gerais do que valor
  Tradução do inglês: tarefa suficientemente simples, descomposição aumentou os gastos acima do seu valor

**The complexity cost:**
- Cada limite de agente é um passo de compressão perdida: o contexto completo do agente A é resumido em uma mensagem para o agente B
  Tradução do inglês para inglês: Each Agent 边界 are有损压缩步骤:Agenta A's complete on the following is summarized for sending to Agent B's message
- A lógica de coordenação (quem faz o que, quando, em que ordem) é sua própria fonte de bugs
  中文翻译:协调逻辑(谁做什么、何时做、按什么顺序) em si mesma é um bug fonte
- Aumentam a latência: N agentes significa N chamadas sérias LLM mínimo, mais se eles precisam de falar para frente e para trás
  Tradução do inglês:延迟增加:N 个代理意思至少N 次串行 LLM 调用,如果需要来回对话则更多
- Multiplicação de custos: cada agente queima tokens de forma independente
  Chinese: 代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代引代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代

Regra geral: se uma tarefa requer menos de 20 chamadas de ferramentas e se encaixa em 100k tokens, mantenha-a monoposto.

> 經驗法则: Se uma tarefa só precisa de menos de 20 vezes para usar ferramentas, e é adequada a 100k tokens, mantenha um único agente.

## Construí-lo e realizei-o.
```figure
swarm-messages
```

## Construí-lo

### Passo 1: O Agente Solteiro sobrecarregado

Aqui está um único agente tentando fazer tudo. Tem um enorme sistema de resposta e uma janela de contexto contendo pesquisa, código e avaliações:

> É um único agente que tenta fazer tudo. Tem um sistema de dicas e uma janela de análise de código e revisão.

```typescript
type AgentResult = {
  content: string;
  tokensUsed: number;
  toolCalls: number;
};

async function singleAgentApproach(task: string): Promise<AgentResult> {
  const systemPrompt = `You are a full-stack developer. You must:
1. Research the requirements
2. Write the code
3. Review the code for bugs
4. Write tests
Do ALL of these in a single conversation.`;

  const contextWindow: string[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const research = await fakeLLMCall(systemPrompt, `Research: ${task}`);
  contextWindow.push(research.output);
  totalTokens += research.tokens;
  totalToolCalls += research.calls;

  const code = await fakeLLMCall(
    systemPrompt,
    `Given this research:\n${contextWindow.join("\n")}\n\nNow write code for: ${task}`
  );
  contextWindow.push(code.output);
  totalTokens += code.tokens;
  totalToolCalls += code.calls;

  const review = await fakeLLMCall(
    systemPrompt,
    `Given all previous context:\n${contextWindow.join("\n")}\n\nReview the code.`
  );
  contextWindow.push(review.output);
  totalTokens += review.tokens;
  totalToolCalls += review.calls;

  return {
    content: contextWindow.join("\n---\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

Problemas com esta abordagem:
- A janela de contexto cresce com cada etapa.
  Na tradução chinesa, a janela de estudo contém notas e códigos de estudo e as suas conclusões anteriores.
- O sistema de instrução é genérico, não pode ser ajustado para cada etapa.
  Tradução do inglês para o inglês: system提示是通用──不能为每个阶段调优──
- Nada corre em paralelo.
  Não faz parte da obra.

O ciclo de um único agente obriga o LLM a alternar o contexto entre tarefas cognitivas muito diferentes (pesquisa vs codificação vs revisão) em cada turno.

> 单代理 循环迫使 LLM Cada turno está em tarefas de conhecimento muito diferentes (研究 vs 编码 vs 审阅) entre os trocos.

### Passo 2: Agentes especializados

Agora, divide-o, cada agente tem um trabalho:

> Agora, desmantelem-no. Cada agente consegue uma missão:

```typescript
type SpecialistAgent = {
  name: string;
  systemPrompt: string;
  run: (input: string) => Promise<AgentResult>;
};

function createSpecialist(name: string, systemPrompt: string): SpecialistAgent {
  return {
    name,
    systemPrompt,
    run: async (input: string) => {
      const result = await fakeLLMCall(systemPrompt, input);
      return {
        content: result.output,
        tokensUsed: result.tokens,
        toolCalls: result.calls,
      };
    },
  };
}

const researcher = createSpecialist(
  "researcher",
  "You are a technical researcher. Read documentation, find patterns, and summarize findings. Output only the facts needed for implementation."
);

const coder = createSpecialist(
  "coder",
  "You are a senior TypeScript developer. Given requirements and research notes, write clean, tested code. Nothing else."
);

const reviewer = createSpecialist(
  "reviewer",
  "You are a code reviewer. Find bugs, security issues, and logic errors. Be specific. Cite line numbers."
);
```

Cada especialista tem um prompt focado, cada um obtém uma janela de contexto limpa com apenas a entrada que precisa.

> Cada especialista tem uma dica focada. Cada um obtém uma janela de texto acima e abaixo, contendo apenas as entradas necessárias.

O prompt do pesquisador é otimizado para leitura e resumo. O prompt do codificador é otimizado para escrever código limpo. O prompt do revisor é otimizado para encontrar bugs. Nenhum single prompt tenta fazer as três coisas.

> As dicas dos investigadores para leitura e optimização de resumo. As dicas dos editores para redação de código puro. As dicas dos revisores para detecção de bugs. Não há dicas individuais para tentar fazer estas três coisas ao mesmo tempo.

### Passo 3: Coordenar através de mensagens

Entregue os especialistas com mensagem explícita:

> 通过显式消息传递将专家连接起来:

```typescript
type AgentMessage = {
  from: string;
  to: string;
  content: string;
  timestamp: number;
};

async function multiAgentApproach(task: string): Promise<AgentResult> {
  const messages: AgentMessage[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const researchResult = await researcher.run(task);
  messages.push({
    from: "researcher",
    to: "coder",
    content: researchResult.content,
    timestamp: Date.now(),
  });
  totalTokens += researchResult.tokensUsed;
  totalToolCalls += researchResult.toolCalls;

  const coderInput = messages
    .filter((m) => m.to === "coder")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const codeResult = await coder.run(coderInput);
  messages.push({
    from: "coder",
    to: "reviewer",
    content: codeResult.content,
    timestamp: Date.now(),
  });
  totalTokens += codeResult.tokensUsed;
  totalToolCalls += codeResult.toolCalls;

  const reviewerInput = messages
    .filter((m) => m.to === "reviewer")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const reviewResult = await reviewer.run(reviewerInput);
  messages.push({
    from: "reviewer",
    to: "orchestrator",
    content: reviewResult.content,
    timestamp: Date.now(),
  });
  totalTokens += reviewResult.tokensUsed;
  totalToolCalls += reviewResult.toolCalls;

  return {
    content: messages.map((m) => `[${m.from} -> ${m.to}]: ${m.content}`).join("\n\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

Cada agente recebe apenas as mensagens que lhe são dirigidas, sem contaminação de contexto, os 50 mil tokens de leitura de documentação do pesquisador nunca entram no contexto do revisor.

> Cada agente só recebe mensagens para si mesmo. Não há nenhuma contaminação.

Esta é a vitória principal: isolamento de informações. A janela de contexto de cada agente é dedicada à sua própria tarefa. O orçamento de 200k tokens de um agente não é desperdiçado no trabalho de arranque de outros agentes.

> É o principal benefício: informação isolada. Cada agente se concentra em suas próprias tarefas. Um agente tem 200 mil tokens.

### Passo 4: Comparar

```typescript
async function compare() {
  const task = "Build a rate limiter middleware for an Express.js API";

  console.log("=== Single Agent ===");
  const single = await singleAgentApproach(task);
  console.log(`Tokens: ${single.tokensUsed}`);
  console.log(`Tool calls: ${single.toolCalls}`);

  console.log("\n=== Multi-Agent ===");
  const multi = await multiAgentApproach(task);
  console.log(`Tokens: ${multi.tokensUsed}`);
  console.log(`Tool calls: ${multi.toolCalls}`);
}
```

A versão multi-agente usa mais tokens totais (três agentes, três chamadas separadas de LLM), mas o contexto de cada agente permanece limpo.

> Dois agentes, três agentes independentes, três LLM, mas cada um dos agentes mantém sua qualidade em cada fase, pois o sistema de instruções é especializado.

O comércio é claro: gastar mais tokens, obter melhor produção. Vale a pena quando a tarefa é difícil. Não vale a pena para "resumir este parágrafo".

> 权衡很清:花更多代币,获得更好的输出――任务难时值――对"总结这一段"不值――

## Use-o com o framework implementado.

Esta lição produz uma indicação reutilizables para decidir quando se deve ir para multi-agente.`outputs/prompt-multi-agent-decision.md`- Não .

> Este curso apresenta uma dica repetível para determinar quando utilizar mais agentes.`outputs/prompt-multi-agent-decision.md`- Não.

O prompt faz quatro perguntas de diagnóstico: (1) a tarefa necessita de mais de 100 mil tokens de contexto de trabalho? (2) requer diferentes conhecimentos em diferentes fases? (3) existe trabalho paralelo? (4) vale a pena a complexidade?

> A dica pergunta quatro questões de diagnóstico: 1) a tarefa precisa de mais de 100 mil tokens de trabalho? 2) as diferentes fases necessitam de diferentes conhecimentos especializados? 3) se há trabalho possível? 4) a complexidade vale a pena ser comercializada?

## Exercícios.

1. Adicione um quarto especialista: um agente "tester" que recebe código do codificador e revisar feedback do revisor, em seguida, escreve testes
   Chinese: 添加第四专家: 一"测试员"Agente, recebe código do codificador e o revisor, então escreve o teste
2. Modificar o pipeline para que o revisor possa enviar feedback de volta ao codificador para um ciclo de revisão (max 2 rodadas)
   Tradução do idioma japonês: Modificar fluid, para que o revisor possa enviar o código para o redator para o ciclo de modificação (maximum 2 rounds)
3. Converte o pipeline sequencial em um fan-out: execute o pesquisador e um agente "analista de requisitos" em paralelo, em seguida, funcione suas saídas antes de passar para o codificador
   Tradução em chinês:将顺序流水线转换为扇出:并行运行研究员和"需求分析师"agente, então juntar suas saídas e reenviá-las ao codificador

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Swarm / 群体 | "A hive mind of AI agents" / "AI Agent 的蜂巢思维" | A set of peer agents with shared state and no fixed leader. Behavior emerges from local interactions. / 一组具有共享状态且无固定领导者的对等 Agent。行为从局部交互中涌现。 |
| Orchestrator / 编排器 | "The boss agent" / "老板 Agent" | An agent whose tools include spawning and managing other agents. It plans and delegates but may not do the actual work. / 一个工具包括生成和管理其他 Agent 的 Agent。它规划和委派，但可能不做实际工作。 |
| Coordinator / 协调器 | "The traffic cop" / "交通警察" | A non-agent component (often just code, not an LLM) that routes messages between agents based on rules. / 一个非 Agent 组件（通常只是代码，不是 LLM），根据规则在 Agent 之间路由消息。 |
| Consensus / 共识 | "The agents agree" / "Agent 们达成一致" | A protocol where multiple agents must reach agreement before proceeding. Used when conflicting outputs need resolution. / 多个 Agent 在继续之前必须达成一致的协议。用于需要解决冲突输出的情况。 |
| Emergent behavior / 涌现行为 | "The agents figured it out themselves" / "Agent 自己想出来的" | System-level patterns that arise from agent interactions but were not explicitly programmed. Can be useful or harmful. / 从 Agent 交互中产生但未被明确编程的系统级模式。可能有用也可能有害。 |
| Fan-out / fan-in / 扇出/扇入 | "Map-reduce for agents" / "Agent 的 Map-reduce" | Splitting a task across parallel agents (fan-out), then combining their results (fan-in). / 将任务分配给并行 Agent（扇出），然后合并它们的结果（扇入）。 |
| Message passing / 消息传递 | "Agents talk to each other" / "Agent 之间互相交谈" | The communication mechanism between agents: structured data sent from one agent to another, replacing shared context windows. / Agent 之间的通信机制：从一个 Agent 发送到另一个 Agent 的结构化数据，替代共享上下文窗口。 |

## Mais leitura 延伸阅读

- [The Landscape of Emerging AI Agent Architectures](https://arxiv.org/abs/2409.02977)- análise dos padrões de agentes múltiplos
  Tradução do inglês para Chinês: 新兴 AI Agent 架构概览  多 Agent 模式综述
- [AutoGen: Enabling Next-Gen LLM Applications](https://arxiv.org/abs/2308.08155)- O framework de conversação multi-agente da Microsoft
  AutoGen:赋能下一代 LLM 应用  微软的多代理对话框架
- [Claude Code subagents documentation](https://docs.anthropic.com/en/docs/claude-code)- como Claude Code delega com a tarefa
  中文翻译:Claude Code 子 Agente 文档  Claude Code 如何使用任务委派
- [CrewAI documentation](https://docs.crewai.com/)- quadro multiagente baseado em funções
  Tradução do inglês para inglês: CrewAI 文档  基于角色的多代理框架
