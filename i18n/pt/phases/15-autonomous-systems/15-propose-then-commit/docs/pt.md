# Homem-no-loop: Propõe-Então-Comite.

> O consenso de 2026 sobre o HITL é específico. Não é "o agente pede, o usuário clica em Aprova". É proposta-então-compromissado: a ação proposta é persistida para uma loja duradoura com uma chave de idempotencia; apareceu para um revisor com intenção, linhagem de dados, permissões tocadas, raio de explosão e um plano de retrocesso; cometido apenas após reconhecimento positivo; verificado após execução para confirmar que o efeito colateral realmente aconteceu. O LangGraph's `interrupt()`Além do checkpointing PostgreSQL, o Microsoft Agent Framework `RequestInfoEvent`, e do Cloudflare.`waitForApproval()`O modo de falha canônico é a aprovação de selo de borracha: "Aplicar?" é clicado sem revisão. A mitigação documentada é o desafio e resposta com uma lista de verificação explícita.

> **【中文解读】**2026 ano HITL 共识是具体的──不是"Agent 问, user点击 Approve"──是提出-then-commit:提议动作以等键持久化到持久存储;向审查员呈现意图、数据谱系、触及权限、爆炸半径、回滚计划;仅在正面确认后提交;执行后验证确认副作用实际发生──`interrupt()`加 PostgreSQL 检查点、Microsoft Agent Framework `RequestInfoEvent`、Cloudflare de `waitForApproval()`Todos os países têm o mesmo padrão de desenvolvimento.

> **【拓展：四个状态机步骤】**Propõe-depois-compromete é um estado de estado: 1) 提议Agent 产生动作,以等键持久化带意图/数据谱系/触及权限/爆炸半径/回滚计划; 2) 呈现审查者(人类,非 Agent 自审) 看到所有元数据; 3) 提交正面确认,动作执行; 4) 验证执行后回读副作用确认──这是数据库`RETURNING`- Não, não.`PutObject`后  `GetObject`、Stripe/AWS API 等键模式在代理 审批上的复用──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, propose-then-commit state machine with idempotency) | **语言:** Python（标准库，带幂等的提议-提交状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 14 (Tripwires) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 14（触发器）
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**学本节前请先掌握:Fase 15·12(Execução Durável) Fase 15·14(Kill Switches) Fase 14·15(HITL Agent 模式) 本节是HITL的工程化标准四步状态机──
> - Não .**【类比】**Proposta-depois-Comit = "Banking big额转账审批"――普通 LLM 调用 = 即时转账(错了找客服);Proposta-depois-Comit = 提交转账申请(含收款人、金额、用途、回滚预案)→ 审查员看元数据 → 批准 → 执行 → 验证到账──每一步都不能省──这是人类计算机使用、Claude Code Plan Mode、Stripe API 等的键统一模式──
> ️ **【易错点】**"Aplicar?" 弹窗被用户惯性点"是" → 皮章失效──修复:(1) 多选清单(每个动作独立确认);(2) 强制延迟(3 秒倒计时);(3) 关键动作双确认(输入金额数字);(4) 显示"爆炸半径"(影响 N 个文件、M 个用户) ⋅

## O problema é o problema da introdução

> **【中文解读】**O modelo de "Proposta-Então-Comit") requer que o Agente primeiramente gerar o programa de modificação, mas não imediatamente executar, mas mostrar ao usuário ou outro Agente  Censura, Censura passa apenas depois de ser submetido.

> **【拓展：propose then commit】**O modelo de submissão de código é uma prática de segurança padrão do agente de código de 2026  O código de código de código  O modelo de código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código de código  O código  O código de código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O código  O  O código  O código  O código  O  O código  O  O código  O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O O

O agente toma uma ação. O utilizador tem de decidir: aprovar ou não. Se a decisão é instantânea, provavelmente não é uma revisão.

> O agente  tomar ação  o usuário deve decidir: aprovação ou não aprovação  Se a decisão é imediata, não pode ser revisão 

A questão da engenharia é como fazer uma revisão estruturada o caminho da menor resistência.

> Se a decisão é estruturada, ela é lenta, mas é acreditável.

O padrão HITL da era 2023 foi um pedido sincrônico: "O agente quer enviar e-mail para X com o corpo Y  aprovar?" O usuário clica em Aproveitar. Todo mundo sente que o sistema é seguro. Na prática, esta superfície é fortemente marcada por borracha: os usuários aprovam rapidamente, as aprovações prevêem pouco, e quando o agente falha, a trilha de auditoria mostra um longo histórico de aprovações que o usuário não pode lembrar.

> 2023 时代 HITL 模式是同步提示:"Agente deve enviar um e-mail para X,正文 Y批准?" usuário clique Approve。 Todo mundo sente sistema de segurança。 na prática, esta interface foi gravemente 皮章化: usuário rápida aprovação, aprovação pré-conhecida baixa, quando o Agente saiu de tempo de auditoria, o rastreamento mostra que o usuário não consegue lembrar de sua longa aprovação histórico。

> **【中文解读】**Esta secção apresenta o conceito e o método de implementação do Agente de IA. O Agente é um sistema autónomo impulsionado pelo LLM, capaz de observar o ambiente, pensar decisões, executar a ação e ciclo de vida até a conclusão do objetivo.

O padrão 2026  propor-então-comprometer  move o HITL para um substrato durável, anexa metadados estruturados e requer compromisso positivo.

> Modelo 2026 ano propose-then-commit  will HITL  transfer to持久基板上, adicional estruturada元数据, requisito de apresentação em linha.

Cada SDK gerenciado de agente envia uma versão: LangGraph `interrupt()`, Microsoft Agent Framework `RequestInfoEvent`, Cloudflare `waitForApproval()`Os nomes das API diferem, a forma não.

> Cada agente de gestão SDK`interrupt()`、Microsoft Agent Framework `RequestInfoEvent`Cloudflare`waitForApproval()`△API 名称不同;形态不。

## O conceito central.

### A máquina de proposição e depois compromisso.

1. **Propose.**O agente produz uma ação proposta. Persistindo para um armazém durável (PostgreSQL, Redis, Objeto Durável). Inclui:
   Tradução:**提议。**Agente 产生提议动作──持久化到持久存储(PostgreSQL、Redis、Durable Object) ──incluem:
   - Intenção (por que o agente está fazendo isso)
     Em inglês, "Agent" significa "Agente".
   - Linhagem de dados (que fonte levou à presente proposta)
     Tradução do inglês para inglês:
   - Permissões tocadas (que escopo / arquivos / pontos finais)
     Tradução do inglês: 触及的权限 (qualquer parte do seu território)
   - raio de explosão (o que é o pior caso)
     Tradução do inglês: Explosion halfway (pior mal que se passa é o quê)
   - plano de reestruturação (se for cometido, como o desfechar)
     中文翻译:回滚计划 (como enviar, como retirar)
   - Cláusula de independência (única por proposta; a representação apresenta o mesmo registro)
     Tradução do inglês para inglês: 等键(每提议唯一;重提交返回同一记录)
2. **Surface.**O revisor vê a proposta com todos os metadados.
   Tradução:**呈现。**O revisor vê com todas as suas propostas.
3. **Commit.**Reconhecimento positivo, a ação é executada.
   Tradução:**提交。**Está confirmado.
4. **Verify.**Após a execução, o efeito colateral é lido de volta e confirmado. Se a etapa de verificação falhar, o sistema está em um estado de mau conhecido e o alerta se activa.
   Tradução:**验证。** Se o processo de verificação falhar, o sistema está em estado de malformação conhecida e inicia o alerta

### A chave da impotência.

Sem uma chave de idempotencia, uma nova tentativa após uma falha transitória pode duplicar a execução de uma ação aprovada.

> Não há nenhum problema, o re-teste imediato após o fracasso pode ser duplicado.

Exemplo concreto: o usuário aprova "transferir $100 de A para B". Blip de rede. Fluxo de trabalho retenta. O usuário aprovou uma vez, mas a transferência é executada duas vezes. A chave de idempotency liga a aprovação a um único efeito colateral único; a segunda execução é um no-op.

> 具体例:用户批准"从A 转 $100到B"──网络闪断──工作流重试──用户批准一次但转账执行两次──等键将批准绑定到单一唯一副作用;第二次执行是无-op──

Este é o mesmo padrão de idempotencia que Stripe e AWS API usam. Reutilizar para aprovações de agentes é explícito nos documentos do Microsoft Agent Framework.

> É o mesmo modelo usado pela Stripe e pela AWS API.

### Durabilidade: por que as aprovações ultrapassam os processos

A sala de espera de aprovação é um estado que o agente não possui. O fluxo de trabalho é pausa (Lessão 12). Quando a aprovação chega, o fluxo de trabalho retoma exatamente a partir desse ponto.`interrupt()`com checkpointing PostgreSQL e não apenas estado de memória  uma aprovação dois dias depois ainda encontra o fluxo de trabalho intacto.

> 批准等候室是 Agent 不拥有一片状态──工作流暂停──第 12 课)──批准到达时,工作流从该精确点恢复──这就是为什么 LangGraph将`interrupt()`A aprovação dos pontos de verificação PostgreSQL, em vez de apenas o estado de memória, encontrou ainda um fluxo de trabalho completo.

### As aprovações de selos de borracha e a mitigação de desafios e respostas.

A interface padrão para HITL ("Aplicar" / "Rejeitar" botões) produz aprovações rápidas sem revisão genuína. mitigação documentada: uma lista de verificação de desafios e respostas que requer respostas positivas a perguntas específicas antes de o botão Aprovar ser ativado.

> HITL 默认 UI("Aplicar"/"Rejetar" 按)产生快速批准无真实审查──已记录缓解:在 Aplicar 按启动前要求对特定问题正面回答的挑战-响应清单──具体形状:

- "Entendes qual recurso é que isto toca?
  Tradução do inglês:
- "Você verificou que o raio da explosão é aceitável?
  Tradução do inglês:
- "Tem um plano de retrocesso se isto falhar?
  Tradução do inglês: "Se você não consegue, você tem planos para voltar?

O revisor que não pode marcar as caixas quer pede esclarecimento (escalação) ou recusa (default seguro). A pesquisa Anthropic agente-segurança cita explicitamente HITL de lista de verificação como uma mitigação para padrões de aprovação de selos de borracha.

> Não é para burocracia e burocracia é função obrigatória não pode fazer a seleção do quadro de revisor ou exigir a clarificação (avaliar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (rejeitar) (receitar) (receitar) (receitar)  (receitar) )  (receitar)  (receitar)  (receitar)  (receitar) )  ()  ()                                                                                                                          

### O que conta como consequência.

Não todas as acções precisam de propostas e compromissos.

> Não é necessário que cada movimento seja proposto-depois-comitado.

- **Consequential actions**(sempre HITL): registos irreversíveis, transacções financeiras, comunicação de saída, alterações na base de dados de produção, operações destrutivas do sistema de arquivos.
  Tradução:**后果性动作**(总 HITL): não é possível escrever, não é possível fazer transações financeiras, não é possível fazer comunicações externas, não é possível produzir alterações na base de dados, não é possível fazer alterações no sistema de documentos.
- **Reversible actions**(às vezes HITL): edições de arquivos locais, mudanças de env em fase, gravações reversíveis com retrocesso claro.
  Tradução:**可逆动作**(quando HITL): 本地文件编辑、舞台化 环境变更、带清晰回滚的可逆写──
- **Reads and inspections**(never HITL): ler um arquivo, listar recursos, chamar uma API somente leitura.
  Tradução:**读和检查**(从不HITL): read文件、列资源、调用只读API。

### Verificação pós-ação.

"A execução de commit" não é a mesma que "o efeito colateral aconteceu". Condições de partição de rede e corrida podem produzir um fluxo de trabalho que acha que foi bem sucedido enquanto o backend não persistiu. A etapa de verificação lê novamente o recurso alvo após o compromisso de confirmar. Este é o mesmo padrão que as transações de banco de dados com `RETURNING`cláusulas ou AWS `GetObject`Depois`PutObject`- Não .

> "O processo de submissão não é equivalente ao "concorrido efeitos secundários" e as condições de concorrência e de distribuição de dados podem gerar um fluxo de trabalho para o sucesso e o sucesso não se prolongam.`RETURNING`Transações de banco de dados`PutObject`后  `GetObject`A AWS tem um modelo semelhante.

### Artigo 14 da Lei da IA da UE.

O artigo 14.o exige uma supervisão humana eficaz de sistemas de IA de alto risco na UE. "Efectivo" não é decorativo. A linguagem regulatória exclui especificamente padrões de selos de borracha. Proporcionar-depois-comprometer com desafio-e-resposta é a forma que sobrevive ao escrutínio do artigo 14.o nos documentos de conformidade do Kit de ferramentas de governança de agentes da Microsoft.

> Seção 14 条强制 EU高风险 AI 系统的有效人类监督――"有效" não é um "arquitetura"――监管语言明确排除皮章模式――带挑战-响应的建议-然后-承诺 是在微软代理治理工具包 合规文档中通过第 14 条审查的形态――

## Use-o com o framework implementado.
```figure
mx-propose-then-commit
```

## Usá-lo

`code/main.py`Implementa uma máquina de estado de proposta-depois-comitamento em stdlib Python. Armazenamento durável é um arquivo JSON. A chave de idempotency é um hash de (thread_id, action_signature). O driver simula três casos: um fluxo de aprovação limpo, uma retempta após falha transitória (que não deve ser executada duplamente) e um selo de borracha padrão versus um fluxo de desafio e resposta.

> `code/main.py`Usar Python 实现 propose-then-commit 状态机──持久存储是 JSON 文件──等键是 (thread_id, action_signature) 的哈希──驱动器模拟三例:干净批准流、瞬态失败后的重试(必须不双执行)

## Envia-o . Produto .

`outputs/skill-hitl-design.md`Revisar um fluxo de trabalho HITL proposto para propor a forma e a forma de compromisso e sinalizar as camadas de metadados, de independência, de verificação ou de desafios e respostas que faltam.

> `outputs/skill-hitl-design.md`审查提议 HITL 工作流的建议-然后-承诺 形态并标记缺失的元数据、等、验证或挑战-响应层──

## Exercícios.

1. Corra .`code/main.py`- Confirmar que uma nova tentativa de uma proposta aprovada utiliza o registro duradouro e não re-executa.
   Tradução: 运行`code/main.py` confirmar que a reutilização de um projecto de lei aprovado tem um registro permanente e não se reexecutará.

2. Extender o registro das propostas com uma `rollback`Simula uma execução cuja etapa de verificação falha. Mostre o tiro de volta automático.
   Tradução:`rollback`字段扩展提议记录──模拟验证步骤失败的执行──展示回滚自动触发──

3. Leia o Microsoft Agent Framework `RequestInfoEvent`Identifique um campo de metadados que a API inclui que a máquina de brinquedo está faltando.
   Tradução do Novo Mundo:`RequestInfoEvent`文档──识别 API 包含而玩具引擎缺失一元数据字段──添加它并解释它防止什么──

4. Desenhar uma lista de verificação de desafios e respostas para uma ação específica (por exemplo, "postar em uma conta pública no Twitter").
   Por exemplo, "enviar para o Twitter público 账号") desenha desafios-响应清单―― o revisor deve responder a quais três perguntas?

5. Escolha um caso em que uma pergunta sincrônica "Aplicar?" seria suficiente (não é necessária uma loja duradoura). Explique por que, e nome a classe de risco que você está aceitando.
   Chinese: 選一個同步 "Approve?"提示就足足足 (conhecimento) 提示就足足 (conhecimento) 提示就足足 (conhecimento) 提示就足足 (conhecimento) 提示就足足 (conhecimento) 提示就足足 (conhecimento) 提示就足足 (conhecimento) 提示就足足 (conhecimento) 提示就足足 (conhecimento) 提示就足足 (conhecimento) 提示就足 (conhecimento) 提示就足足 (conhecimento) 提示就足足 (conhecimento) 提示就足足 (conhecimento) 提示就足足 (conhecimento) 提示就足 (conhecimento) 提示就足 (conhecimento) 提示就足 (conhecimento) 提示 (conhecimento) 提示 (conhecimento) 提示) 提示 (conhecimento) 提示 (conhecimento) 提示) 提示 (conhecimento) 提示 (conhecimento) 提示) 提示 (explicação) 原因为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为为

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Propose-then-commit | "Two-phase approval" | Persisted proposal + positive commit + verify |
| Propose-then-commit | "两阶段批准" | 持久提议 + 正面提交 + 验证 |
| Idempotency key | "Retry-safe token" | Unique per proposal; second execution no-ops |
| 幂等键 | "重试安全 token" | 每提议唯一；第二次执行 no-op |
| Data lineage | "Where it came from" | The specific source content that led to the proposal |
| 数据谱系 | "它从哪来" | 导致提议的特定源内容 |
| Blast radius | "Worst case" | Scope of effect if the action goes wrong |
| 爆炸半径 | "最坏情况" | 动作出错时的影响范围 |
| Rubber-stamp | "Fast approval" | "Approve" clicked without genuine review |
| 橡皮章 | "快速批准" | 无真实审查地点击"Approve" |
| Challenge-and-response | "Forcing checklist" | Reviewer must positively acknowledge specific questions |
| 挑战-响应 | "强制清单" | 审查者必须正面确认特定问题 |
| RequestInfoEvent | "MS Agent Framework primitive" | Durable HITL request with structured metadata |
| RequestInfoEvent | "MS Agent Framework 原语" | 带结构化元数据的持久 HITL 请求 |
| `interrupt()` / `waitForApproval()` | "Framework primitives" | LangGraph / Cloudflare equivalents of the same shape |
| `interrupt()` / `waitForApproval()` | "框架原语" | 相同形态的 LangGraph / Cloudflare 等价物 |

## Mais leitura 延伸阅读

- [Microsoft Agent Framework — Human in the loop](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop)- Não .`RequestInfoEvent`, aprovações duradouras.
  Tradução:`RequestInfoEvent`、perdurada aprovação―
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/)- Não .`waitForApproval()`e objetos duráveis.
  Tradução:`waitForApproval()`和 Objetos Duráveis
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) HITL como mitigação do risco de longo prazo.
  Tradução do inglês: HITL 作为长程风险缓解──
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/) Linha de base regulatória para sistemas de alto risco.
  Tradução do inglês: 高风险系统的监管基线──
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) enquadramento constitucional em torno da supervisão.
  Tradução do inglês:
