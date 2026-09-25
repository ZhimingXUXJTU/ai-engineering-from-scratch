# Grupo de Chat e Seleção de Oradores   grupo de Chat  escolha 发言人

> A orquestração de conversa compartilhada coloca N agentes em uma conversa; uma função selecionadora (LLM, round-robin ou custom) escolhe quem fala a seguir. Este é o arquétipo da conversa emergente multi-agente. Os agentes não sabem o seu papel num gráfico estático, eles apenas reagem ao pool compartilhado. AutoGen GroupChat e AG2 GroupChat são as implementações de referência: a semântica do GroupChat do AutoGen v0.2 foi preservada no garfo AG2; AutoGen v0.4 o reescreveu como um modelo de ator orientado por eventos. A Microsoft colocou o AutoGen em modo de manutenção em fevereiro de 2026 e o fundiu com o Kernel Semântico no Microsoft Agent Framework (RC fevereiro de 2026). O primitivo do GroupChat sobrevive tanto no AG2 quanto no Microsoft Agent Framework. Aprenda uma vez, use em todos os lugares.

> **【中文解读】**Este capítulo apresenta o grupo de conversas entre os falantes escolher mais agentes para decidir quem fala, quando fala e como falar.

> **【拓展：group chat speaker selection→具体应用】**群聊发言人选择是多 Agent 讨论中的关键问题谁发言、什么时候发言、发言多久──三种主要策略:(1) 轮流制按固定顺序发言;(2) 相关性制最相关的 Agent 发言;(3) 仲裁制一个专门协调员决定谁发言──AutoGen's GroupChat 使用 LLM 作为仲裁者──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**学本节前请先掌握:Fase 16·04(原语模型) 、AutoGen 基础──群聊 = N 个 Agente 共享一个对话池,发言人选择决定谁说话──
> - Não .**【类比】**群聊发言人选择 = "presidente da reunião"──轮流制 = 圆桌按序;相关性制 = 谁懂谁说;仲裁制 = 主持人指定──AutoGen GroupChat usando LLM quando o presidente 高成本但灵活──2026 Nota:AutoGen 已被微软合并并到微软代理框架,AG2是社区 fork,都保留了 GroupChat 原语──

## Problema Introdução

Os gráficos estáticos (LangGraph) são ótimos quando o fluxo de trabalho é conhecido. As conversas reais não são estáticas: às vezes o programador pergunta ao revisor, às vezes o pesquisador, às vezes o escritor. A codificação em ar condicionado de cada possível transferência produz uma explosão de borda. Você quer que * agentes reagam a um pool compartilhado*, com alguma função decidindo quem fala a seguir.

> 静态图(LangGraph) em flux de trabalho já conhecido quando é bom.  Verdadeiro diálogo não é estático: às vezes o programador pergunta revisor, às vezes o pesquisador, às vezes o autor pergunta.  Hard coding cada possível contato ocorre quando explode.

O problema da explosão de borda é real: um sistema de 5 agentes com todas as possíveis transferências tem 25 bordas direcionadas. Adicione um sexto agente e você tem 36.

> O problema da explosão é real: com todos os 5 agentes possíveis de comunicação, o sistema tem 25 elementos, tem 25 elementos, tem 6 agentes, 36 elementos, não pode ser expandido para o diálogo atual; você precisa de um conjunto.

É exatamente isso que o AutoGen GroupChat faz.

> É o que o AutoGen GroupChat faz.

## Conceptos básicos

### A forma

```
              ┌─── shared pool ────┐
              │   m1  m2  m3  ...  │
              └─────────┬──────────┘
                        │ (everyone reads all)
      ┌───────┬─────────┼─────────┬───────┐
      ▼       ▼         ▼         ▼       ▼
    Agent A  Agent B  Agent C  Agent D  Selector
                                           │
                                           ▼
                                  "next speaker = C"
```

Cada agente vê todas as mensagens, e uma função selecionadora é invocada em cada turno para escolher quem fala a seguir.

> Cada Agente vê cada mensagem. Cada turno utiliza a função selecionadora para escolher o próximo orador.

O grupo de transparência é tanto o ponto forte quanto o ponto fraco do GroupChat. Força: qualquer agente pode reagir a qualquer coisa que qualquer um diga. Fraqueza: após 20 voltas, o contexto de cada agente é enorme, caro e diluído. Mitigations: projetos visualizações de alcance por agente (Lessão 15) ou terminar cedo.

>                                                                                                                                                                                                                                                               

### Os três sabores selectores

**Round-robin.**Ciclo fixo. Determinista. Escala linearmente em N mas ignora o contexto  um codificador recebe a volta mesmo quando o tópico é revisão legal.

> **轮询。**O sistema de redação pode ser usado para fazer a leitura de textos.

**LLM-selected.**Uma chamada para um LLM que lê o pool recente e retorna o melhor próximo orador. Consciente do contexto, mas lento: a cada turno adiciona uma chamada de LLM.

> **LLM 选择。**调用 LLM 读取近期并返回最佳下文发言人──上下文感知但慢: cada rodada aumentar uma vez LLM 调用──AutoGen 的默认选择──

**Custom.**Uma função Python com qualquer lógica que você deseja. Típica: LLM-selecionado com regras de fallback (por exemplo, "sempre dar ao verificador a volta após o codificador").

> **自定义。**Uma função Python, usando qualquer lógica que você deseje.

### A API do Agente Conversable

```
agent = ConversableAgent(
    name="coder",
    system_message="You write Python.",
    llm_config={...},
)
chat = GroupChat(agents=[coder, reviewer, tester], messages=[])
manager = GroupChatManager(groupchat=chat, llm_config={...})
```

`GroupChatManager`Quando um agente completa uma volta, o gerente chama o selector, que retorna o próximo agente.

> `GroupChatManager`持有选择器──当 Agent 完成一轮时,管理者调用选择器,返回下一个 Agent──循环继续直到终止条件──

A função selector é o coração do GroupChat. Troque-a, mude o estilo de orquestração. Selector round-robin = determinista. Selector LLM = adaptativo. Selector personalizado = quaisquer regras que você codifique.

> 选择器函数是 GroupChat's核心──换掉它,改变编排风格──轮询选择器 = 确定性──LLM 选择器 = 自适应──自定义选择器 = 你编码的任何规则──相同原语,不同编排──

### Cessão

Três padrões comuns:

> Três tipos de comportamento:

- **Max rounds.**Capeta dura em viradas totais.
  Tradução:**最大轮数。**总轮数的硬上限──
- **"TERMINATE" token.**Os agentes podem emitir uma mensagem sentinela; o gerente parou quando apareceu.
  Tradução:**"TERMINATE" 标记。**O agente pode enviar uma mensagem de polícia; o administrador pode parar quando aparecer.
- **Goal-reached check.**Um verificador leve corre a cada turno e pára o bate-papo quando terminado.
  Tradução:**目标达成检查。**O teste de qualidade de cada rodada de funcionamento e terminação para parar de conversar.

### A AutoGen -> AG2 dividido e o Microsoft Agente Framework fundir
### Linhagem: forças e fusões

No início de 2025, a Microsoft começou uma grande reescritura do AutoGen (v0.4) em torno de um modelo de ator orientado a eventos. A comunidade forcou a semântica GroupChat do AutoGen v0.2 como AG2, preservando a API que os primeiros adotadores tinham integrado.

> No início de 2025, a Microsoft começou a realizar uma reescritura significativa em torno do ator impulsionador de eventos do AutoGen (v0.4) 社区将 AutoGen v0.2 语义分叉为 AG2, retendo os primeiros usuários já integrados de API ⋅

O fork foi necessário porque a versão 0.4 rompeu a compatibilidade retrospectiva de maneiras fundamentais.`GroupChat`- Não .`ConversableAgent`, e `GroupChatManager`A API estável, enquanto a v0.4 introduz novos primitivos orientados por eventos. Ambas as linhas são mantidas ativamente a partir de 2026.

> A divisão é necessária, pois a v0.4 destruiu a compatibilidade para trás em aspectos básicos.`GroupChat`- Não.`ConversableAgent`和 `GroupChatManager`API 稳定, enquanto v0.4  introduzir novos eventos driven原语──截至2026年,两条线都积极维护──

Em fevereiro de 2026, a Microsoft anunciou que o AutoGen iria entrar em modo de manutenção, com o modelo de ator orientado por eventos se fundindo em **Microsoft Agent Framework**(RC fevereiro 2026, agora fundido com o Kernel Semantic). O conceito de GroupChat sobrevive em ambas as faixas; os detalhes de implementação diferem. AG2 é o código preferido para o upstream para o código compatível com v0.2.

> 2026 ano 2 meses, Microsoft anuncia AutoGen  entrar em manutenção mode, evento-driving actor 模型合并到 **Microsoft Agent Framework**(RJ, já está com o Kernel Semântico 合并) ――GroupChat 概念在两个轨道中存活;实现细节不同──AG2 是 v0.2 兼容代码的首选上游──

A lição: a superfície da API supera as estruturas. O código escrito contra a API GroupChat da AutoGen v0.2 em 2024 ainda funciona sem alterações através da AG2 em 2026. As estruturas se tornam mais rápidas; os primitivos (pool compartilhado + selector) não.

> O código de código para o Google Analytics é o código de código para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google Analytics para o Google.

### Quando o GroupChat se encaixa

- **Emergent conversations.**Não quer pre-cablear todos os possíveis próximos alto-falantes.
  Tradução:**涌现对话。**Não queres conectar-te a cada um dos próximos comunicadores.
- **Role-mixing tasks.**O codificador pede ao pesquisador, o pesquisador pede ao arquivo, o arquivo pede ao codificador de volta.
  Tradução:**角色混合任务。**编码器问研究员,研究员问档案员,档案员反问编码器──流程不是DAG──
- **Exploratory problem-solving.**Pensa em "reunião de tempestade cerebral", não em "linha de montagem".
  Tradução:**探索性问题解决。**想想"头脑风暴会议", em vez de "装配线"

### Quando falha

- **Strict determinism.**O selector de LLM pode ser inconsistente, o mesmo prompt, diferentes corridas, diferentes oradores próximos.
  Tradução:**严格确定性。**LLM 选择器可能不一致──相同提示,不同运行,不同下一个发言者──
- **Sycophancy cascades.**Os agentes deferem-se a quem falar com mais confiança.
  Tradução:**谄媚级联。**O agente se submete ao mais confiante dos oradores.
- **Context bloat.**Cada agente lê cada mensagem; depois de 10 voltas, o contexto é enorme.
  Tradução:**上下文膨胀。**Cada Agente 读取每条消息;10 轮后上下文巨大──使用投影(Lessão 15)来限定视图──
- **Hot speakers.**Um agente domina a conversa porque o selector favorece suas especialidades.
  Tradução:**热发言者。**Um Agente, o principal, conduz o diálogo, porque o selecionador é orientado para o seu especializado.

### Chat de grupo vs supervisor

Os mesmos primitivos, diferentes padrões:

> Como se fosse o caso, não há nada que me diga.

- Supervisor: um agente planeja e outros executam.
  中文翻译:监督者:一个代理 规划,其他执行──选择器是"问规划者做什么──"
- Chat em grupo: todos os agentes são pares; selector é uma função sobre o pool compartilhado.
  O agente é um elemento de conjunto; o selector é uma função na cadeia de compartilhamento.

Ambos usam os quatro primitivos da lição 04.

> 两者都使用课堂04的四个原语──群聊默认使用 LLM 选择的编排和全池共享状态──

A escolha entre supervisor e chat de grupo é principalmente sobre *quem é o titular do plano*. supervisor: um agente é o dono do plano e os delegados. chat de grupo: o plano é implícito, emerge da conversa. o primeiro é mais controlado; o segundo é mais flexível.

> 监督者和群聊之间的选择主要是关于*谁持有计划*──监督者:一个代理 拥有计划并委派──群聊:计划是隐式的,从对话中涌现──前者更可控;后者更灵活──

## Construí-lo e realizei-o.
```figure
swarm-speaker
```

## Construí-lo

`code/main.py`O programa de discussão é um programa de discussão de grupos que permite a criação de um grupo de conversas de forma a permitir a criação de um grupo de conversas de grupos.`TERMINATE`- O sinal.

> `code/main.py`Usar o padrão de base para a realização de um grupo de conversação.`TERMINATE`O que é que se passa?

A demonstração imprime a transcrição da conversa, mais o rastro de decisão do selector para ambas as variantes.

> 演示印交谈记录以及两种变体的选择器决策追踪──

## Use-o com o framework implementado.

`outputs/skill-groupchat-selector.md`configura um selector GroupChat para uma determinada tarefa  round-robin vs LLM-selected vs custom, e quais entradas do selector (mensagens recentes, especialidades de agente, contagens de viradas) para usar.

> `outputs/skill-groupchat-selector.md`Para determinar a configuração de tarefas GrupoChat  escolher 轮询 vs LLM 选择 vs 自定义, bem como usar o que escolher 输入(最近消息、Agent 专长、轮次计数) ⋅

## Envia-o . Produto .

Lista de verificação:

> 检查清单:

- **Max rounds cap.**Sempre. 10 a 20 para tarefas típicas.
  Tradução:**最大轮数上限。**总是使用──典型任务 10-20──
- **Speaker-balance metric.**As rotas de pista por agente; alerta quando o desequilíbrio excede um limiar.
  Tradução:**发言者平衡指标。**Seguir cada agente de rotas; quando o desequilíbrio excede o valor da agência de notícias.
- **Termination token.** `TERMINATE`ou um agente verificador dedicado.
  Tradução:**终止标记。** `TERMINATE`Ou agente de verificação especializado.
- **Projection or scoped memory.**Após ~ 10 mensagens, considere dar a cada agente apenas uma visão de alcance para evitar o conteúdo inflado.
  Tradução:**投影或范围内存。**Após cerca de 10 notícias, considere dar a cada agente apenas uma visão de alcance para evitar a inflamação da informação.
- **Selector logging.**Para as variantes selecionadas pelo LLM, registre tanto a entrada do selector quanto a sua escolha.
  Tradução:**选择器日志。**对于LLM 选择变体,记录选择器的输入和选择――否则调试不可能――

## Exercícios.

1. Corra .`code/main.py`Comparar a conversa entre um round-robin e um LLM selecionado.
   Tradução: 运行`code/main.py`◊ Comparar a consulta ao Mestrado em Direito e Direito Jurídico  Seleção do diálogo ◊ Em cada tipo de processo, qual agente é o principal?
2. Adicione uma regra de "max-speaks-per-agent" no selector.
   Tradução do inglês em japonês: в избирателя в добавлении "cada agente máximo número de vezes de palavras"
3. Implementar uma terminação atingida: parar quando o revisor retornar "aprovado".
   Tradução do inglês para o inglês: Realization goal achievement终止: When the reader returns "approved" when stops.
4. Leia os documentos estáveis do AutoGen no GroupChat. Identifique o selector padrão usado por `GroupChatManager`- Não .
   中文翻译:阅读 AutoGen 稳定文档中的 GroupChat──识别 `GroupChatManager`Utilize of默认选择器──
5. Leia o repo AG2 e compare seu v0.2 GroupChat com a versão v0.4 orientada por eventos. Que propriedade concreta (transmissão, tolerância a falhas, composibilidade) adiciona o v0.4?
   Chinese Language Translation: read AG2 仓库并比较其 v0.2 GroupChat 与 v0.4 事件驱动版本──v0.4 添加了什么具体属性(吞吐量、容错、可组合性?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GroupChat / 群聊 | "Agents in one chat room" / "一个聊天室中的 Agent" | Shared message pool + selector function. AutoGen / AG2 primitive. / 共享消息池 + 选择器函数。AutoGen / AG2 原语。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | The function that picks the next agent. Round-robin, LLM-selected, or custom. / 选择下一个 Agent 的函数。轮询、LLM 选择或自定义。 |
| GroupChatManager / 群聊管理者 | "The meeting host" / "会议主持人" | AutoGen component that owns the selector and loops over turns. / 拥有选择器并循环轮次的 AutoGen 组件。 |
| ConversableAgent / 可对话 Agent | "The base agent" / "基础 Agent" | AutoGen base class; an agent that can send and receive messages. / AutoGen 基类；可以发送和接收消息的 Agent。 |
| Termination token / 终止标记 | "The 'stop' word" / "停止词" | Sentinel string (usually `TERMINATE`) that ends the chat. / 结束聊天的哨兵字符串（通常是 `TERMINATE`）。 |
| Hot speaker / 热发言者 | "One agent dominates" / "一个 Agent 主导" | Failure mode where the selector keeps picking the same agent. / 选择器持续选择同一 Agent 的失败模式。 |
| Context bloat / 上下文膨胀 | "Pool grows unbounded" / "池无限增长" | Each agent reads every prior message; context grows with turns. / 每个 Agent 读取每条先前消息；上下文随轮次增长。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Role-specific view into the shared pool to prevent context bloat. / 角色特定的共享池视图以防止上下文膨胀。 |

## Mais leitura 延伸阅读

- [AutoGen group chat docs](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/group-chat.html) a execução de referência
  中文翻译:AutoGen 群聊文档  参考实现
- [AG2 repo](https://github.com/ag2ai/ag2) comunidade AutoGen v0.2 continuação
  中文翻译:AG2 仓库  社区 AutoGen v0.2 延续
- [Microsoft Agent Framework docs](https://microsoft.github.io/agent-framework/) Sucessor fundido, RC Fevereiro 2026
  中文翻译:Microsoft Agent Framework 文档  合并后后的继任者,2026 年 2 月 RC
- [Microsoft Agent Framework docs](https://learn.microsoft.com/en-us/agent-framework/) Sucessor fundido, RC Fevereiro 2026
- [AutoGen v0.4 release notes](https://microsoft.github.io/autogen/stable/) Detalhes de reescritura do modelo de ator orientado para eventos
  中文翻译:AutoGen v0.4 发布说明  事件驱动 actor 模型重写详情
