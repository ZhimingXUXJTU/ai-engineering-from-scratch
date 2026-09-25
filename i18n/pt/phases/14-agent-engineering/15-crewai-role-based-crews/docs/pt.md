# CrewAI: Equipes e fluxos baseados em papéis
# Equipes de agentes baseadas em funções  Funções, tarefas, processos

> Quatro primitivas: Agente, tarefa, tripulação, processo. Duas formas de nível superior: equipes (autônoma, colaboração baseada em papéis) e fluxos (evento-driven, determinista). CrewAI é a implementação de referência de 2026, e seus documentos são contundentes: "para qualquer aplicação pronta para produção, comece com um fluxo".

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 14 (Actor Model) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Objetivos de aprendizagem

- Nomear os quatro primitivos da CrewAI (Agente, Tarefa, Equipamento, Processo) e o que cada um possui.
- Distinguir Sequenciais, Hierárquicos e o processo de Consenso planejado; escolher um por carga de trabalho.
- Distinguir as equipas (baseadas em funções autônomas) das fluxos (determinísticas orientadas por eventos) e explicar a recomendação de produção dos docentes.
- Ferramentas de fio com o `@tool`decorador e `BaseTool`Subclasse; razão sobre saídas estruturadas versus texto livre.
- Nomear os quatro tipos de memória CrewAI e quando cada um paga.
- Implementar uma equipe de três agentes (investigador, escritor, editor) que produz um resumo.
- Determine os três modos de falha da CrewAI: "Inflação rápida", "imposto de gerente-LLM", "transmissões frágeis".

## O problema é o problema da introdução

As equipes que adotam estruturas multi-agentes atingem a mesma parede. "Collaboração autónoma" soa muito bem em uma demonstração. Então um cliente arquivou um bug e você precisa de repetição determinista. Ou financeiro pergunta quanto custa uma equipe de LLM-routed por rodada. Ou em chamada precisa saber qual agente ficou parado às 3 da manhã.

>  Empreendendo vários agentes  framework, as equipes de todos encontram o mesmo muro

As equipes de forma livre com direção LLM não respondem a nenhuma delas de forma limpa.

> O grupo de LLM não pode responder de forma clara a estas perguntas.


> **【中文解读】**A CrewAI  adota um modelo de papel  cada agente tem um papel  papel  metas  metas  metas  e história de fundo  história de fundo  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história  história 

> **{【拓展：CrewAI 是 2024-2025 年增长最快的 Agent 框架之一（GitHub 20k+ s...】}**A CrewAI é uma das mais rápidas de crescimento de 2024-2025 Agentes  estrutura  GITHub 20k+ estrelas) ⋅ Seu ponto de venda central é baixo código Agente  colaborando    através de YAML  configurar arquivo definido Agente  roles e missões ⋅ CrewAI  suporta dois tipos de modelos: Crew  预定义角色团队) e Flow 动态工作流) ⋅ Empresas usuários ⋅ especialmente não técnicos ⋅ Especial青 ⋅ seu intuitivo 角色定义方式──
A divisão da CrewAI é honesta sobre o comércio. Equipes para trabalho colaborativo, baseado em papéis, exploratório. Fluxos para produção orientada a eventos, de propriedade de código, auditable.

> A divisão de integridade da CrewAI faz face a essa medida. A equipe usa o processo de colaboração, o trabalho exploratório baseado em papéis.

> - Não .**【前置】** deve ser aprendido primeiro:Fase 14·12Antropic Workflow Patterns)Flow of CrewAI é a realização destes modelos,Crew é a "auto-edição" do trabalho; bem como Fase 14·14Actor Model)Agenta do Crew 协作本质上是消息传递── também precisa entender Pydantic(struktur化输出验证), pois tarefa de`output_pydantic`É o principal acordo.

## O conceito central.

### Quatro primitivos

A superfície da tripulação é pequena, memorizar isto e o resto é configurar.

> A interface da tripulação é muito pequena.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

- **Agent.** `role + goal + backstory + tools + (optional) llm`O conteúdo é carregável, modela o tom, o julgamento, quando o agente se detém, as ferramentas são funções que o agente pode chamar (mais abaixo).

> - Não .**【类比】**O objetivo é KPI (encontrar tendências importantes em dados), história de fundo é a cultura empresarial do cérebro (encontrar um profissional de 20 anos na IBM, dedicar-se à rigor...).**关键洞察**A história de trás não é decoração, realmente afeta o estilo de julgamento do LLM.
- **Task.** `description + expected_output + agent + (optional) context + (optional) output_pydantic`Uma unidade de trabalho reutiliável.`expected_output`É o contrato.`context`Lista de tarefas que são transmitidas em linha de frente. `output_pydantic`Força uma forma estruturada.
- **Crew.**O contêiner, é o proprietário da lista de`agents`, a lista de `tasks`, o `process`, e opcionais `memory`+ `verbose`+ `manager_llm`configurações.
- **Process.**Estratégia de execução: sequencial, hierárquica, consensal (planificado).

Os agentes não se veem diretamente, as tarefas são de referência, a tripulação sequencia as tarefas, o processo decide quem escolhe a próxima tarefa, é o modelo mental.

> Agente 间不直接见彼此──Task 引用 Agente──Crew 排列任务顺序──Processo que decide quem executar a próxima tarefa──Tese é o modelo inteiro de espírito──

> **Validated against**CrewAI 0.86 (2026-05). As versões mais recentes podem renomear ou fundir os tipos de processo; verifique o [CrewAI Processes docs](https://docs.crewai.com/concepts/processes)antes de depender de uma forma específica.

### Sequenciais vs Hierárquicos vs Consenso

- **Sequential.**As tarefas são executadas na ordem de declaração.`context`O custo mais baixo, mais previsível, usado quando a ordem estiver fixa.
- **Hierarchical.**O agente gerente (chamada de LLM separada) percorre rotas entre especialistas.`manager_llm`Configuração ou padrão. O gerente seleciona a próxima tarefa a cada rodada e pode recusar ou redirecionar.
- **Consensus.**Planeado, não implementado na API pública. Os documentos reservam o nome para um futuro processo baseado em votação. Não confiem nele hoje.

A hierarquica adiciona uma chamada de LLM por rodada (o gerente) em cima de cada chamada especializada. O custo do token pode triplicar em uma corrida de cinco passos. Pague apenas quando você precisa do roteamento.

> ️ **【易错点】**Veja os exemplos de documentos da CrewAI em termos hierárquicos.**后果**O gerente de cada vez mais Mestrado em Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Direito de Dire**一行修复**O que é mais importante é que o seu nível de desempenho seja mais elevado.

> O modelo de nível aumenta a cada rodada de Mestrado em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em Administração em

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

### Equipes vs Fluxos

É o enquadramento com que os médicos vão liderar em 2026.

> Este é o quadro mais central do arquivo de 2026.

- **Crew.**Autonomia orientada pelo LLM. O framework escolhe a forma no tempo de execução. bom para: pesquisa, brainstorming, primeiros rascunhos, onde quer que o caminho seja parte da resposta. Difícil de repetição. Difícil de testar. Barato para protótipo.
- **Flow.**Grafico de eventos que você possui.`@start`Marca a entrada. `@listen(topic)`O que é um passo que dispara quando outro passo emite esse tópico. cada passo é Python simples (pode chamar uma tripulação internamente). bom para: produção. observável. testável. determinista.

Recomendação de produção dos médicos para 2026: comece com um fluxo.`Crew.kickoff()`O fluxo dá-lhe o rastro de auditoria, a tripulação dá-lhe a exploração.

> 文档 2026 年的生产建议:从流动开始――当自主性值其成本时,将船员作为 `Crew.kickoff()`调用嵌入 Flow 步骤中. Flow 提供审计追踪,Crew 提供探索能力.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

### Integração de ferramentas

Três maneiras de dar uma ferramenta a um agente.

> Há três maneiras de dar aos agentes ferramentas. Escolher a mais simples.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

1. **`@tool` decorator.**Funções puras se tornam ferramentas. A assinatura é o esquema; o docstring é a descrição que o LLM vê.

   ```python
   from crewai.tools import tool

   @tool("Search the web")
   def search(query: str) -> str:
       """Return top results for the query."""
       return run_search(query)
   ```

2. **`BaseTool` subclass.**Ferramenta baseada em classe com esquema de args explícito, suporte de async, retries. Utilize quando a ferramenta tem estado (um cliente, um cache) ou precisa de args estruturados.

   ```python
   from crewai.tools import BaseTool
   from pydantic import BaseModel

   class SearchArgs(BaseModel):
       query: str
       limit: int = 10

   class SearchTool(BaseTool):
       name = "web_search"
       description = "Search the web and return top results."
       args_schema = SearchArgs

       def _run(self, query: str, limit: int = 10) -> str:
           return self.client.search(query, limit=limit)
   ```

3. **Built-in toolkits.**A CrewAI envia adaptadores de primeira parte: `SerperDevTool`- Não .`FileReadTool`- Não .`DirectoryReadTool`- Não .`CodeInterpreterTool`- Não .`RagTool`- Não .`WebsiteSearchTool`- Com um único importador.

As saídas estruturadas usam o Pydantic.`output_pydantic=MyModel`A CrewAI valida a resposta do LLM contra o modelo e quer coacciona ou retrata.`expected_output`As saídas de texto livre são boas para os rascunhos; as saídas estruturadas são o que os fluxos de baixo fluxo podem consumir.

>  Struktur化输出使用 Pydantic──在 任务 上传入 `output_pydantic=MyModel` O pessoal de trabalho, segundo o modelo de experiência do LLM, não se encaixa em transformações ou reexames obrigatórios.`expected_output`字符串使用──自由文本输出适合草稿;结构化输出才是下游 Flow 可以消费的──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

### Anéis de memória

A CrewAI envia quatro tipos de memória para fora da caixa.

> A tripulação da AI abre-cabeça fornece quatro tipos de memória.

> **Validated against**CrewAI 0.86 (2026-05).`Memory`O modelo conceitual abaixo ainda vale, mas a superfície da classe pública pode cair para uma única`Memory`ponto de entrada em versões mais recentes; verificação [CrewAI memory docs](https://docs.crewai.com/concepts/memory)para a API atual.

- **Short-term.**O amortecedor de conversação num único passe, apagado no final.
- **Long-term.**Persistindo em todas as corridas. Armazenado em um vector DB (Chroma por padrão, intercambiável). Retirado por semelhança com a tarefa atual.
- **Entity.**"Cliente X está no plano empresarial", baseado em entidade, não em semelhança.
- **Contextual.**Retira a memória relevante no momento em que o agente precisa, não pré-carregada.

Ativar a tripulação com `memory=True`A memória é um dos lugares onde a CrewAI ganha a sua manutenção contra frameworks mais finos; LangGraph puro exige que você cable cada um deles sozinho.

> Em tripulação de passageiros`memory=True`O sistema de memória é um dos principais benefícios do CrewAI em relação a um quadro mais leve.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

### Quando o CrewAI se encaixa
### Quando as equipes baseadas em papéis se adaptam

- Três a seis agentes com papéis identificados e um fluxo de trabalho colaborativo.
- Roteamento em que o julgamento do MLL sobre o próximo passo faz parte do valor (hierárquico).
- Onde quer que a equipa esteja mais feliz lendo .`role + goal + backstory`- Não. - Não.

### Quando não

- DAG deterministas com ordem rigorosa. Use LangGraph (Lessão 13). A forma do gráfico é a abstracção certa; o enquadramento de papel da CrewAI é o atrito.
- Orçamentos de latência subsegundo. Hierárquico adiciona viagens de ida e volta. Mesmo Sequential serializa instruções que incluem histórias de fundo e saídas anteriores.
- Loops de agente único. Esqueça a estrutura; um loop de agente (Lessão 1) mais um registro de ferramentas é mais curto.

A lição 17 (Agent Framework Tradeoffs) expõe isto numa matriz.

> 第 17 课(Agent 框架权衡) usando a matriz mostrou isso.

> 🤔 **【困惑】**P: CrewAI 文档说"生产环境从流动开始",但我看YouTube教程全是 Crew 例子,到底该信谁? A: 信文档。YouTube教程偏向演示 效果(Crew自主协作看起来更酷),但生产环境是什么?**可重放、可审计、可监控** Estes são apenas Flow 能给──建议路径: Use Crew 做原型验证思想 (((一两小时搞定),稳定后用Flow 重写为生产版本──Crew 不是不能用,而是不能直接上生产──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

### Forma de dependência

Independente da LangChain. Python 3.10 a 3.13.`uv`Contagem de estrelas: veja[crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)(Shotshot em 2026-05). A integração AWS Bedrock é documentada; benchmarks vendor relatam um aumento substancial de velocidade versus LangGraph em cargas de trabalho de QA, mas a metodologia (dataset, hardware, métrica de avaliação) não é publicada, então trate os números framework-vendor como direcional apenas.

> Não depende da LangChain.`uv`包管理──AWS Bedrock 集成已有文件;供应商基准测试报告称在QA 工作负载上有显著加速,但方法论(数据集、硬件、评估指标) não foi divulgado, portanto, os dados dos fornecedores do quadro serão apenas de referência──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

### Onde este padrão vai mal

- **Prompt-bloat from backstories.**Uma história de fundo de 2000 palavras por agente e uma equipe de cinco agentes queima o orçamento contextual antes da primeira chamada de ferramenta. Mantenha as histórias de fundo abaixo de 200 palavras. Reutilize frases em todos os agentes; não repita o estilo da casa cinco vezes.

> **背景故事导致的提示膨胀。**Cada história de fundo de Agente 2000 palavras, adicionada a cinco equipes de Agentes, já foi consumida antes da primeira ferramenta de admissão do orçamento seguinte.
- **Manager-LLM token tax.**O processo hierárquico adiciona uma chamada de LLM do gerente antes de cada chamada especialista. Em uma equipe de cinco tarefas que é de seis chamadas de LLM em vez de cinco, e a chamada do gerente carrega a lista completa de tarefas mais saídas anteriores.

> **管理者 LLM 的 Token 税。**O nível de nível aumenta uma vez antes de cada especialista ser chamado para o Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestrado em Mestr
- **Brittle handoffs.**A tarefa N's `expected_output`A tarefa N+1 diz que `context`O LLM produziu quatro, o agente ad-libs, resolveu com o agente de segurança.`output_pydantic`na tarefa N, então a tarefa N+1 lê um objeto digitado, não texto livre.

> **脆弱的交接。**任务 N 的 `expected_output`É um "outro plano" ― tarefa N+1`context`读取并尝试解析三个部分──LLM 生成四个──下游 Agente 即兴发挥──用 `output_pydantic`修复任务 N,让任务 N+1 读取类型化对象而非自由文本。
- **Crew-as-prod.**A tripulação de forma livre enviada para a produção sem um envolvente de fluxo. A variabilidade de saída é alta; repetição é impossível; a chamada não pode diferenciar uma corrida ruim contra uma boa.

> **Crew 直接上生产。**没有包装成流就将自由形式 Crew 发布到生产环境――输出变异性高;无法重放;值班人员无法对抗好坏运行――用流 包装――

## Construí-lo e realizei-o.
```figure
ae-crew-vs-flow
```

## Construí-lo

`code/main.py`Implementa versões STDlib de ambas as formas mais uma tripulação de três agentes.

> `code/main.py`Usando o padrão, realizou duas formas e um grupo de três agentes.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

Forma:

- `Agent`- Não .`Task`Classe de dados correspondente à superfície da CrewAI.
- `SequentialCrew.kickoff(inputs)`Executa tarefas em ordem de declarações, enfiando as saídas como `context`- Não .
- `HierarchicalCrew.kickoff(topic)`Adiciona um agente gerente escolhendo o próximo especialista a cada rodada, para no "feito".
- `Flow`com`@start`E ...`@listen(topic)`Decoradores, um pequeno ciclo de eventos e um rastro.
- `tool(name)`O decorador reflete o CrewAI.`@tool`- Forma.
- `Memory`com`short_term`- Não .`long_term`- Não .`entity`Lojas; comparação ridicularizada usa numpy.
- As respostas falsas de LLM são cordas codificadas com teclado de papel e prefixo de entrada.

Demo de concreto: pesquisador, escritor, equipe de editor produzindo um resumo sobre "engenharia de agentes 2026". Pesquisador tira (se burla) fontes. Escritor rascunhos. Editor apertando. A mesma equipe corre através de um fluxo para mostrar a forma determinista.

> 具体演示:研究员、作者、编辑组成团队,生成一篇关于"agent engineering 2026"的简报──研究员获取(模拟的) 来源──作者起草──编辑精炼──同一个团队通过流动 运行以展示确定性形态──

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

- É o que é ?

```bash
python3 code/main.py
```

Cobertas de rastreamento: sequenciais de tripulantes de threading de saídas através `context`, equipe hierárquica com seleções de gerentes (investigador, escritor, editor, então "feito"), fluxo executando os mesmos três passos com tópicos explícitos (`researched`- Não .`drafted`- Não .`edited`), chamadas de ferramentas encaminhadas através `@tool`, e memória a longo prazo sobreviver a dois golpes.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

A traça da tripulação é fluida, o gerente pode reordenar em princípio.

> O rastreamento da tripulação é fluido; o gerente pode ser reorganizado em princípio.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

## Use-o com o framework implementado.

- **CrewAI Flow**Mesmo quando o fluxo é um passo que chama`Crew.kickoff()`O fluxo dá o limite da auditoria.
- **CrewAI Crew (Sequential)**para o trabalho colaborativo de ordem clara, especialmente os primeiros projectos e os ciclos de revisão.
- **CrewAI Crew (Hierarchical)**Quando o roteamento depende da saída e você tem quatro ou mais especialistas.
- **LangGraph**(Lessão 13) para máquinas de estado explícito, currículo duradouro, ordem rigorosa.
- **AutoGen v0.4**(Lessão 14) para a concurência do modelo de ator e o isolamento de falhas.
- **OpenAI Agents SDK**(Lessão 16) para os produtos OpenAI-first com manchas e barris.
- **Claude Agent SDK**(Lessão 17) para produtos Claude-first com subagentes e loja de sessões.

## Envia-o . Produto .

`outputs/skill-crew-or-flow.md`Seleciona Crew vs Flow para uma tarefa e prepara a implementação mínima. Hard rejeita sobre Crew-sem história de fundo, Flow-sem-tópicos explícitos, Hierárquico com menos de três especialistas.

> `outputs/skill-crew-or-flow.md`Para uma missão escolher Crew ou Flow, e construir o mínimo de realização.

> CrewAI 将多 Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent角色+目标+背景故事)、Task任务)、Crew团容器)、Processo执行策略)──

## Encaixos.

- **Backstory as flavor.**Teste três variantes por agente, a variância é real, escolha uma e congela-a.

> **把背景故事当装饰。**Ele realmente moldou a saída. Cada agente teste três variações; a diferença é real.
- **Skipping `expected_output`.**Sem um contrato por tarefa, as tarefas a seguir ao fluxo recolhem o que o LLM produziu.

> **跳过 `expected_output`。**没有每个任务的契约,下游任务会接收 LLM 生成的任何内容──Crew 运行通过;审计失败──
- **Memory always-on.**O longo prazo escreve cada corrida, o vector DB cresce, a recuperação fica barulhenta, o escopo escreve para tarefas onde o fato é persistente.

> **记忆始终开启。**长期记忆每次运行都写入──向量数据库不断增长──检索变杂──将写入范围限制在需要持久化事实的任务──
- **Manager prompt drift.**Se o roteamento ficar estranho, despeja-o no modo verbose e leia.

> **管理者提示漂移。**层级模式的管理者提示是隐式的. Se o caminho se tornar estranho, use the verb 模式导出并阅读.
- **Tool side effects in Crews.**Uma tripulação pode ligar para uma ferramenta mais vezes do que o esperado.

> **Crew 中的工具副作用。**A tripulação pode usar mais ferramentas do que o esperado.

## Exercícios.

1. Converte a tripulação Sequencial em Fluxo, conte os pontos de contacto onde a variabilidade diminui, note onde a legibilidade diminuiu.
  Tradução do inglês para tradução do inglês:
2. Adicionar memória da entidade à tripulação: os fatos sobre um cliente persistem durante os lançamentos. Verifique a recuperação atrai a entidade certa.
  Tradução do inglês para tradução do inglês:
3. Implementar um processo hierárquico em que o gerente se recusa a encaminhar para o editor até que a saída do escritor tenha pelo menos três parágrafos.
  Tradução do inglês para tradução do inglês:
4. - O cabo a .`BaseTool`Subclasse para uma pesquisa na web. Compare a forma de rastreamento com a `@tool`versão decorativa.
  Tradução do inglês para tradução do inglês:
5. Adicionar`output_pydantic=Brief`a tarefa do editor, onde `Brief`- Não .`title`- Não .`summary`- Não .`sections`Faça com que a saída da tarefa de escritor tenha JSON mal formado uma vez; verifique o comportamento de retest de CrewAI no rastreamento.
  Tradução do inglês para tradução do inglês:
6. Leia a introdução dos documentos da CrewAI.`crewai`Que garantias a versão do STDlib ignorou?
  Tradução do inglês para tradução do inglês:
7. Liga o agente de operações ou o Langfuse (Lessão 24) para uma corrida real.
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent | "Persona" | Role + goal + backstory + tools |  |
| Task | "Unit of work" | Description + expected output + assignee + optional structured output |  |
| Crew | "Agent team" | Container for Agents + Tasks + Process |  |
| Process | "Execution strategy" | Sequential / Hierarchical / Consensus (planned) |  |
| Flow | "Deterministic workflow" | Event-driven, code-owned, testable |  |
| Backstory | "Persona prompt" | Tone and judgment shaper for the Agent |  |
| `@tool` | "Function tool" | Decorator that turns a function into a tool the Agent can call |  |
| `BaseTool` | "Class tool" | Class-based tool with args schema, retries, async support |  |
| Entity memory | "Per-entity facts" | Memory scoped to a customer / account / issue |  |
| Long-term memory | "Cross-run memory" | Vector-backed memory that survives between kickoffs |  |
| Contextual memory | "Just-in-time retrieval" | Memory pulled at the moment the Agent needs it |  |
| Manager LLM | "Router agent" | Extra LLM in Hierarchical process that picks the next task |  |
| `expected_output` | "Task contract" | String that tells the Agent (and audit) what shape to return |  |

## Mais leitura 延伸阅读

- [CrewAI docs introduction](https://docs.crewai.com/en/introduction): conceitos e caminho de produção recomendado
  Tradução do português:
- [CrewAI Flows guide](https://docs.crewai.com/en/concepts/flows): forma orientada por eventos, `@start`- Não .`@listen`
  Tradução do português:
- [CrewAI tools reference](https://docs.crewai.com/en/concepts/tools)- Não .`@tool`- Não .`BaseTool`, kites de ferramentas incorporados
  Tradução do português:
- [CrewAI memory](https://docs.crewai.com/en/concepts/memory): curto prazo, longo prazo, entidade, contextual
  Tradução do português:
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)Quando o multi-agente ajuda e quando não
  Tradução do português:
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview): a alternativa de máquina de Estado
  Tradução do português:
