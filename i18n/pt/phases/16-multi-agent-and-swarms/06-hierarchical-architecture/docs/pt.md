# Arquitetura Hierárquica e Seu Modo de Falha

> A hierarquia é a de supervisores, de gerentes, de subgerentes, de trabalhadores.`Process.hierarchical`é a versão do livro de texto: a `manager_llm`O equivalente de LangGraph é `create_supervisor(create_supervisor(...))`É o padrão natural quando a tarefa é um gráfico de órgãos real. É também o padrão mais provável de colapso em circuitos gerenciais.

> **【中文解读】**Esta secção apresenta a estrutura de estrutura em várias camadas, adequada para a decomposição de tarefas complexas.

> **【拓展：hierarchical architecture→具体应用】**A estrutura de nível distribuído irá retornar ao modelo de supervisor em um conjunto de gerentes de nível superior distribuídos para gerentes de nível médio, gerentes de nível médio re-distribuídos para gerentes de nível médio. Isto é semelhante à estrutura de nível de uma organização humana. A prática de 2026 mostra que os níveis de 2 a 3 são os melhores.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 05 (Supervisor Pattern) | **前置知识:** Phase 16 · 05 (监督者模式)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**O que é que se passa com o sistema de gestão?
> - Não .**【类比】**A estrutura de nível = "corporação nível"―1 nível = empresa de criação CEO 直接带工程师);2-3 nível = empresa de tipo médio 最优;4+ nível = grande empresa 病 信息失真、决策缓慢、经理们皮)―Agente também2-3 nível 最优,多了就"管理循环":
> ️ **【易错点】**看到"任务复杂"就加层级 → 管理开销压系统──修复:先用序列或监督者单层跑,确认不够再分层;2-3层是上限──

## Problema Introdução

Uma vez que o padrão de supervisor clique, o próximo passo natural é "e se os trabalhadores são eles mesmos supervisores?" As equipes têm sub-equipas; as empresas têm departamentos de departamentos. Arquiteturas hierárquicas refletem isso.

> Uma vez que o modelo de supervisor é compreendido, o próximo passo da natureza é "se o trabalho em si é também supervisor?"

A tentação é forte porque as organizações humanas trabalham desta forma. Mas as hierarquias LLM herdam todas as patologias das hierarquias humanas (perda de informação, falta de comunicação, iteração lenta) sem os efeitos estabilizadores das relações humanas e da cultura compartilhada.

> A tentação é forte, pois a organização humana trabalha assim. Mas o nível de LLM herdou todos os padrões de doença do nível humano, mas não tem um efeito estável nas relações humanas e na cultura de partilha.

O problema: os gerentes de LLM não são os mesmos que os gerentes humanos. Um gerente humano tem antecedentes estáveis sobre o que seus relatórios sabem. Um gerente de LLM re-raciona a organização a cada passo a partir de qualquer coisa que esteja em seu contexto.

> O problema é que o gerente de LLM não é o mesmo que o gerente humano. O gerente humano sabe o que há em seus subordinados.

Este é o modo de falha central dos sistemas hierárquicos de LLM: cada nível de gerente amplifica os erros do nível anterior.

> É o modelo de fracasso central do sistema LLM: cada gerente aumenta o nível de erro de nível superior.

## Conceptos básicos

### A forma

```
                 Manager
                 ┌─────┐
                 └──┬──┘
           ┌────────┴────────┐
           ▼                 ▼
       Sub-Mgr A         Sub-Mgr B
       ┌─────┐           ┌─────┐
       └──┬──┘           └──┬──┘
         ┌┴──┬──┐          ┌┴──┐
         ▼   ▼  ▼          ▼   ▼
       W1  W2  W3         W4  W5
```

Cada nó interno planeja, delega e sintetiza.

> Cada um dos pontos internos é planejado, comissário e integrado.

O sistema de regulação da composição de órgãos humanos é um sistema de regulação de órgãos humanos que é um sistema de regulação de órgãos humanos.

> Esta configuração da organização humana, que é a sua vantagem e a sua fraqueza, a sua falta de experiência de estabilidade na organização.

### Onde brilha

- **Clear org mapping.**Se a tarefa real for departamental ("revisão legal do documento, revisão financeira do documento, revisão de engenharia do documento, em seguida, resumo para exec"), a hierarquia é explícita.
  Tradução:**清晰的组织映射。**Se a tarefa real é de um departamento, a estrutura de nível é clara.
- **Local summarization.**Cada sub-gerente sintetiza a produção de sua equipe antes que o gerente superior a veja.
  Tradução:**局部摘要。**Cada gerente de nível superior vê antes de integrar as saídas de seu grupo.

### Onde se quebra

Três modos de falha os post-mortem de 2026 continuam a encontrar:

> Análise de eventos de 2026 constantes encontram três modelos de fracasso:

Cemri et al. (MAST, arXiv:2503.13657) documentam estes como "falha de especificação" e "desalinhamento interpessoal" subfamílias.

> Cemri 等人(MAST,arXiv:2503.13657) vai registar estes problemas como "规范失败" e "人际不对齐"子家族──分层系统比平系统更容易出现这些问题,因为每层添加重新解释步骤──

1. **Task assignment error.**O gerente lê o objetivo, alucina uma decomposição e delega ao sub-gerente errado. Porque o sub-gerente obedece a o que lhe foi dado, o erro só surge na síntese superior  um nível removido de onde um ser humano poderia tê-lo pego.
   Tradução:**任务分配错误。**管理者读取目标,幻觉出分解,并委派给错误的子管理者──因为 o filho-manager obedece a uma determinada tarefa, o erro só surge em uma posição superior ao que o ser humano poderia capturar quando é composto por uma camada superior.
2. **Output misinterpretation.**O sub-gerente retorna "não pode verificar a reivindicação X". O gerente superior resume como "a reivindicação X não confirmada". O significado varia em todos os níveis.
   Tradução:**输出误解。**"O nível superior do gerente é totalmente inconfirmado".
3. **Consensus loops.**Dois sub-gerentes discordam; o gerente superior pede-lhes que se reconciliem; eles re-delegam para baixo; os trabalhadores re-existem; os sub-gerentes retornam respostas ligeiramente diferentes; ciclo.`Process.hierarchical`O que é que é o problema?
   Tradução:**共识循环。**Os dois filhos administradores não concordam; os administradores de topo exigem que eles se coordinem; eles se dirigem para baixo; o trabalho se reinicializa; os filhos administradores retornam com respostas diferentes; os ciclos.`Process.hierarchical`通过步骤限制来保护, mas o limite em si é agora um superparâmetro.

### A questão decisiva

Sequencial (linha linear) vs hierárquica: a sua tarefa realmente tem sub-equipas independentes, ou é um fluxo linear fingindo ser uma árvore?

> 顺序(线性流水线) vs 分层: sua tarefa realmente tem sub-équipe independente, também é um processo linear de árvore? Se é o último, use顺序。 Se é o primeiro, use分层, mas precisa orçamento claro de regras de coordenação。

Este é o teste que a maioria das equipes evita. Eles buscam hierarquias porque parece sofisticado, e depois passam semanas a depurar a deriva de decomposição.

> É o teste que a maioria das equipes passou. Eles escolhem as camadas porque parecem altas, e depois passam algumas semanas a tentar desintegrar e deslocar-se.

### Implementação da CrewAI
### Implementação do quadro de funções

A tripulação da IAA `Process.hierarchical`O gerente:

> `Process.hierarchical`Em especial, o grupo de profissionais de saúde é um dos principais parceiros de saúde.

O gerente LLM é em si um agente completo com seu próprio contexto, prompt e ferramentas. Não é um despachador determinista  faz chamadas de julgamento sobre delegação, o que significa que pode fazer chamadas de julgamento erradas. Esta é a fonte do modo de falha de atribuição de tarefas.

> O gerente LLM é um agente completo de si mesmo em baixo, sugerências e ferramentas. Não é um regulador de determinação que faz decisões sobre o uso do comitê, o que significa que pode fazer decisões erradas sobre o uso do comitê.

- recebe a tarefa de nível superior,
  Tradução do inglês:
- atribui subtarefas às tripulações,
  Tradução do inglês:
- Avalia as saídas da tripulação,
  Tradução do inglês: evalu team输出,
- Decide se aceitar, re-delegar ou iterar.
  Chinese: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 代: 

Documentação: https://docs.crewai.com/en/introduction(veja "Processo hierárquico" no ponto "Conceptos fundamentais").

> 文档:https://docs.crewai.com/en/introduction（在核心概念中查找"HierarchicalProcesso")

### Implementação do LangGraph
### Implementação do quadro gráfico

LangGraph usa nested `create_supervisor`O supervisor interno tem seu próprio gráfico; o supervisor externo trata o gráfico interno como um nó opaco. Isso é mais limpo do que o CrewAI para depurar (você pode passar por cada gráfico separadamente), mas é mais difícil expressar a remodelação dinâmica da árvore.

> LangGraph usando um conjunto de`create_supervisor`调用──内部监督者有自己的图;外部监督者将内部图视为不透明节点──这在调试方面比 CrewAI更清晰(tu peux分别步进每个图),但更难表达树的动态重塑──

A vantagem de depuração é real: quando algo vai mal em uma hierarquia de LangGraph de 3 níveis, você pode isolar qual nível falhou passando por cada gráfico de forma independente.

> 调试优势真实: Quando 3 níveis de LangGraph se errão, você pode passar por um passo independente em cada plano para separar quais níveis falharam.

Referência: https://reference.langchain.com/python/langgraph-supervisor.

>  referência:https://reference.langchain.com/python/langgraph-supervisor。

## Construí-lo e realizei-o.
```figure
swarm-hierarchy-token
```

## Construí-lo

`code/main.py`Funciona numa hierarquia de três níveis:

> `code/main.py`运行一个3层层级:

- gerente superior: divide uma tarefa em "engenharia" e "jurídica",
  Tradução do inglês para "máquinas"
- Sub-gerente de engenharia: se divide em trabalhadores "frontend" e "backend",
  Tradução em inglês:工程子管理者:拆分为"前端"和"后端"工作器,
- Sub-gerente jurídico: um trabalhador.
  Tradução do inglês: 法务子管理者:一个工作器──

Demo contrasta caminho feliz (todos concordam) contra um **perturbed path**Quando a decomposição do gerente superior marca erroneamente "legal" como "finance" e observa a cascata de erros  o subgerente obedece ao trabalho financeiro, o sintetizador superior relata as conclusões financeiras, a questão legal original fica sem resposta.

> O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?**扰动路径**, entre os quais o top level manager's breakdown will "legal" erroneously labeled as "financial"并 observe err err erroneously class 子 manager obediently do do do do do do do do do do do do do do do do do do do do do do do do top level compiler report financial findings, original legal question not answered.

O caminho perturbado é o aviso: os sistemas hierárquicos amplificam os erros silenciosamente. O sub-gerente não retrocede ("você disse finanças, mas a tarefa disse legal").

>  perturbation pathway is warning:分层系统静默放大错误――子管理者不反驳("Tu dizes que é financeira, mas que é tarefa dizer que é legal")―它假设管理者更了解──当任何人注意到时,原始意图已丢失──

- Correr .

```
python3 code/main.py
```

A saída mostra ambos os caminhos com um lado claro do lado de "o que foi pedido" versus "o que foi entregue".

> 输出显示两条路径的清晰并排对比:" exigir o que"与" entregar o que"

## Use-o com o framework implementado.

`outputs/skill-hierarchy-fitness.md`A avaliação da utilização de um supervisor hierárquico, sequencial ou plano em uma determinada tarefa.

> `outputs/skill-hierarchy-fitness.md` avaliação de determinadas tarefas deve ser feita através de uma ordem ou um nível de supervisor ∞

## Envia-o . Produto .

Se você enviar hierárquica:

> Se você depõe uma estrutura de nível:

- **Cap tree depth at 2.**Três níveis já escondem a maioria dos erros da observabilidade.
  Tradução:**将树深度限制在 2。**Três camadas já estão escondidas a maioria dos erros fora da observação.
- **Explicit reconciliation budget.**Defina o máximo de rodadas antes que o gerente principal se comprometa.
  Tradução:**明确的协调预算。**O gerente de topo deve definir o número máximo de rotas antes de enviar.
- **Provenance on every synthesis.**O resumo de cada nó deve indicar quais as saídas de folha que o produziram.
  Tradução:**每次综合的来源追溯。**O resumo de cada ponto deve citar a sua produção de folhas.
- **Alert on decomposition drift.**Registre a decomposição do gerente por etapa; diferir contra a consulta do usuário. Se a decomposição não cobrir mais a consulta, inicie um alerta.
  Tradução:**分解漂移告警。**记录管理者每步的分解;与用户查询对比.

## Exercícios.

1. Corra .`code/main.py`Quantos níveis de entrega do gerente são necessários antes que a saída máxima diverja completamente da pergunta do usuário?
   Tradução: 运行`code/main.py`Não é comparado com o caminho normal e o caminho perturbador.
2. Adicione um terceiro nível (top -> sub -> sub-sub -> worker). Meter a frequência com que o caminho perturbado se corrige e diverge completamente à medida que a profundidade cresce.
   Chinese Translation: Add Add Third Layer (Third Layer) (título original) (em inglês)
3. Implementar um trabalhador "canário" em cada sub-gerente que sempre é feito a pergunta original do usuário inalterada. Use a resposta canária para detectar a deriva de decomposição. Como o gerente deve reagir quando o canário não concorda com a resposta sintetizada?
   Tradução em chinês: em cada filho gerente implementar um "金雀" máquina de trabalho, sempre é questionado sobre o problema do usuário original não mudar.
4. Leia o CrewAI `Process.hierarchical`Identificar um barranco de segurança de concreto que a CrewAI aplica (limite de passos, restrição manager_llm) e descrever o modo de falha que visa.
   Tradução do Novo Mundo:`Process.hierarchical`文档──识别 CrewAI 应用一个具体防护措施(步骤限制、manager_llm 约束)并描述它针对的失败模式──
5. Comparar os supervisores de LangGraph aninhados com os hierárquicos da CrewAI.
   Tradução do inglês para tradução do inglês: Comparar um sistema de LangGraph 监督者与 CrewAI 分层──, que facilita o controlo do ciclo de coordenação?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Hierarchical / 分层 | "Org chart pattern" / "组织架构模式" | Supervisors over supervisors; only leaves do work. / 监督者之上还有监督者；只有叶子节点做实际工作。 |
| Manager LLM / 管理者 LLM | "The boss" / "老板" | The LLM that decomposes, assigns, and validates at an internal node. / 在内部节点进行分解、分配和验证的 LLM。 |
| Decomposition drift / 分解漂移 | "The boss lost the plot" / "老板偏离了主题" | Top manager's split no longer covers the original question. / 顶层管理者的拆分不再覆盖原始问题。 |
| Reconciliation loop / 协调循环 | "Endless meetings" / "无尽会议" | Sub-managers disagree; top re-delegates; workers re-run; loop until budget exhausted. / 子管理者不一致；顶层重新委派；工作器重新运行；循环直到预算耗尽。 |
| Depth-2 ceiling / 深度-2 上限 | "Don't go deeper than 2 levels" / "不要超过 2 层" | Empirical guardrail: 3+ levels collapses observability. / 经验防护：3+ 层使可观测性崩溃。 |
| Canary question / 金丝雀问题 | "Ground truth at every level" / "每层的基准真相" | A worker that is always asked the original query unchanged, to detect drift. / 一个总是被问及原始查询不变的工作器，用于检测漂移。 |
| Provenance chain / 来源链 | "Who said what" / "谁说了什么" | Trace from each synthesis back to the leaf outputs that produced it. / 从每个综合追溯到产生它的叶子输出。 |

## Mais leitura 延伸阅读

- [CrewAI introduction — Process.hierarchical](https://docs.crewai.com/en/introduction) Manual hierárquico com um gerente LLM
  Tradução do idioma:CrewAI 介绍  Processos.hierárquico 带管理者 LLM 教科书式分层
- [LangGraph supervisor reference](https://reference.langchain.com/python/langgraph-supervisor) supervisor aninhado via `create_supervisor`
  中文翻译:LangGraph 监督者参考  通过 `create_supervisor`de um supervisor
- [Anthropic engineering — Research system](https://www.anthropic.com/engineering/multi-agent-research-system) por que a Anthropic escolheu deliberadamente um supervisor plano em vez de um supervisor hierárquico
  Chinese:Antropic 工程  研究系统  Por que Antropic 有意选择平监督者而不是分层
- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Taxonomia MAST; secção sobre falhas de coordenação documentação de descomposição deriva
  Por que muitos agentes LLM 系统会失败?  MAST 分类法;协调失败部分记录了分解漂移
