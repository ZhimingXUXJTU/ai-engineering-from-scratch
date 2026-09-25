# Pontos de verificação e retrocesso.

> Cada transição grafico-estado persiste. Quando um trabalhador cai, o contrato de locação expira e outro trabalhador pega no último ponto de controlo. Os objetos duráveis Cloudflare mantêm o estado durante horas ou semanas. Propõe-se então um compromisso (Lessão 15) define um plano de retrocesso por acção. A verificação pós-ação fecha o ciclo. O artigo 14.o da Lei da UE sobre IA torna obrigatória a supervisão humana eficaz para os sistemas de alto risco  na prática, isto significa que os pontos de controlo devem ser interrogáveis, os rollbacks devem ser ensaiados e a trilha de auditoria deve sobreviver à implantação. O modo de falha aguda: sem as chaves de idempotencia e os controlos de pré-condição, uma nova tentativa após uma falha transitória pode duplicar a execução de uma ação já aprovada. A verificação pós-ação é o que a apanha.

> **【中文解读】**Cada gráfico de estado de transformação de perpétuação. Trabalhador  quando o seu aluguel acaba, outro trabalhador  em último ponto de verificação recolhe.  Objetos duráveis  através de horas ou semanas de posse.  Proposta-de-compromisso  15 ) para cada movimento definir o plano de rotação  movimento  após o teste fechado ciclo.  Artigo 14  do EU AI Fallout  para tornar a supervisão humana de sistemas de alto risco válida  Na prática, o ponto de verificação significa que o controle  regresso deve ser exercido  auditoria de rastreamento deve ser trans-deplojada   Modelo de falha: não  assim como o controle de claves e condições de pré-emposição, o teste instantâneo pode ser duplicado após o teste  execução de certificação de execução já aprovada  movimento  após o processo de captura 

> **【拓展：幂等+前置条件+验证+回滚四件套】**仅等不够: considerar"当余额 > $1000 时从 A 转 $100 até B" de aprovação de movimentos. Reforço de execução em colapso, apenas  e outros exames serão aprovados, mas se A  saldo em colapso e recuperação entre outros fluxos de trabalho diminuir para $500,  Pre-condição de verificação falha  sem que ela já seja emitida através de um pagamento.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, checkpoint and rollback state machine) | **语言:** Python（标准库，检查点和回滚状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 15 (Propose-then-commit) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 15（propose-then-commit）
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**O programa de ensino de língua inglesa é um programa de ensino de língua inglesa que inclui a formação de professores de língua inglesa e da língua inglesa.
> - Não .**【类比】**检查点回滚 = "arquivo do jogo e leitura"──检查点 = "arquivo automático" (em inglês) 检查点回滚 = "arquivo automático") 检查点回滚 = "arquivo automático" (em inglês) 检查点回滚 = "arquivo automático") 检查点回滚 = "arquivo automático" (em inglês) 检查点回滚 = "arquivo automático" (em inglês) 检查点回滚 = "arquivo automático" (em inglês) 检查点回滚 = "arquivo automático) 检查点回滚 = "arquivo automático" (em inglês) 检查点回滚 = "arquivo automático" (em inglês) 检查点回滚 = "arquivo automático" (em inglês) 检查点回滚 = "arquivo automático" (em inglês) 检查点回滚 = "arquivo automático" (em inglês) 检查点回滚 = "arquivo automático" (em inglês) 检查点回滚 = "arquivo automático" (em inglês) 检查点回滚") 检查点回滚 = "checkpoint" (em "checkpoint" (em "checkpoint) 检查点回滚动机" (em "checkpoint") 检查点) 检查点回滚" = "checkpoint" (em "check") 检查点" (check) 检查点" (check) 检查点" (check) 检查点) 检查点: "checkpoint: "check" (check) 检查点: "check" (check) 检查点: "check) 检查点: "check: "check" (check) "check" (check) "check" (check) "check" (check) "check) "check" (check) "check" (check) "check" = "check" (check) "check" = "check" = "check" (check" = "check" = "check" = "check" = "check" = "check" (check" =
> ️ **【易错点】**只有等键没有前置条件检查 → 重启时余额已被其他流程改了仍执行 → 透支──修复: 恢复时必须重检"批准时的世界状态"是否还成立 (如"余额>$1000"是否还成立)

## O problema é o problema da introdução

> **【中文解读】**O mecanismo de checkpoint e rollback permite que o Agente conserve o estado de rápido controle durante o processo de execução, e saiba o erro quando ele retorna ao bom estado anterior. Isto é semelhante ao controle de base de dados e versão do Git. O checkpoint mantém um ponto-chave (como antes de modificar o documento), o rollback é executado quando o checkpoint é executado.

> **【拓展：checkpoints rollback】**检查点-回滚是可靠的代理系统的基础设施――实现选择:(1) 文件系统级使用 Git或快照保存文件状态;(2) 数据库级使用事务保证数据一致性;(3) 应用级Agent自我管理检查点(如LangGraph)──关键权衡是检查点粒度太细会增加开销,太粗会丢失更多工作──

A execução duradoura (Lessão 12) torna um agente falhado reiniciável.

> 持久执行 (第 12 课) 使崩 Agent 可恢复──Proposição-em-apoio (第 15 课) 使批准动作可审计──

Esta lição se une a eles: o que acontece quando uma ação aprovada é executada parcialmente, falha e retoma?

> O que acontece quando a ratificação da atividade é executada?

Os sistemas reais transmitem isto de forma diferente:

> Realmente sistema conectado diferente:

> **【中文解读】**Esta secção apresenta o conceito e o método de implementação do Agente de IA. O Agente é um sistema autónomo impulsionado pelo LLM, capaz de observar o ambiente, pensar decisões, executar a ação e ciclo de vida até a conclusão do objetivo.

- **LangGraph**Os dados de trabalho são de acordo com o sistema de verificação de dados de um funcionário.`interrupt()`, que por si só persiste.
  Tradução:**LangGraph**O que é que você está fazendo?`interrupt()`É um processo de transição.
- **Cloudflare Durable Objects**Mantém o estado de cada chave durante horas ou semanas. Co-localize o cálculo com o armazenamento para a ação aprovada.
  Tradução:**Cloudflare Durable Objects**跨数小时或数周持有每键状态──将计算与已批准动作的存储同址──
- **Microsoft Agent Framework**expõe`Checkpoint`As alterações de desempenho são consideradas como "primitivas" na API do fluxo de trabalho; replay mais idempotency cobre retemptations.
  Tradução:**Microsoft Agent Framework**Em trabalho fluxo API`Checkpoint`Orig语;重放加等覆盖重试──

Em todos os casos, a combinação que realmente funciona é: chave de idempotencia + verificação de pré-condição + verificação pós-ação + retrocesso em verificação-falha.

> Em cada caso, a combinação real eficaz é: 等键 + 前置条件检查 + 动作后验证 + 验证失败时回滚──

## O conceito central.

### Cada transição persiste. Cada transformação se perpétua.

Uma transição grafico-estado é qualquer passo que move o fluxo de trabalho de um estado chamado para outro. Implementações ingênuos persistem apenas em pontos específicos de compromisso; implementações de produção persistem em cada transição. O custo (alguns escritos extras) é pequeno em relação ao ganho de confiabilidade (replay aterrissa em qualquer lugar, recuperação de arrendamento é precisa).

> 图状态转换是将工作流从一个命名状态转移到另一个命名状态的任何步骤──简单实现只在特定提交点持久化;生产实现持久化每转换──成本几次额外写) 相对可靠性收益重放落在任何地方、租约恢复精确) 小──

### Recuperação de arrendamento.

Quando um trabalhador cai, o fluxo de trabalho não é perdido; o contrato de locação (uma alegação de curta duração de que esse trabalhador está executando essa corrida) simplesmente expira. Outro trabalhador pega o último ponto de controle e retoma. O mecanismo de locação é o que permite que os sistemas de produção sobrevivam às implantações em movimento sem perder o trabalho em voo.

> Trabalhador 崩时工作流不丢失; arrêdo(Este trabalhador está em execução deste funcionamento declaração provisória) é apenas um período de tempo. outro trabalhador 拾起最新检查点恢复;; mecanismo de arrêdo permite que o sistema de produção prossiga no trabalho em caso de não perder;

### Impotência mais condições prévias.

A independência não basta.$100 from A to B when balance > $1000. " O fluxo de trabalho é comprometido, desabar no meio da execução e retoma. Se apenas a chave de idempotencia for verificada e a execução for retomada, a transferência será executada uma vez (correto). Mas considere que entre o crash e o resume, o saldo de A cai para $500 através de um fluxo de trabalho diferente. O controle de idempotencia ainda passa; a pré-condição não. Sem um controle de pré-condição, enviamos um overdraft.

>  等不够──考虑: 工作流被批准"当余额 > $1000 时从 A 转 $100 até B"── 工作流提交、执行中崩、恢复──若仅检查等关键执行恢复,转账运行一次(正确) 但考虑崩和恢复间 A 余额通过另一工作流降至$500──等检查仍通过;前置条件不──没有前置条件检查,我们发透支──

Toda a acção consequente requer:

> Cada movimento sexual posterior requer dois:

- **Idempotency key**: previne a dupla execução.
  Tradução:**幂等键**: evitar duplo execução.
- **Precondition check**A Comissão considera que o Estado deve dar continuidade ao seu acordo.
  Tradução:**前置条件检查**O Estado de Confirmação continua a ser aprovado.

### Verificação pós-ação.

"A ferramenta devolvida 200" não é verificação. Verificação real lê novamente o estado-alvo e confirma o efeito colateral realmente aconteceu. padrões:

> "工具返回 200" não é um teste.

- Atualização da base de dados: `UPDATE ... RETURNING *`A seguir, afirmar o estado previsto das correspondências de filas devolvidas.
  Tradução do português:`UPDATE ... RETURNING *`Então, eu disse que eu estava no estado de espera.
- Envio de e-mail: verifique a pasta enviada para a identificação da mensagem após a submissão.
  Tradução do inglês: 文本中文翻译:邮件发送:提交后检查发送文件 中的消息 ID──
- Escrever arquivo: ler o arquivo de volta e hash-o.
  Tradução do inglês:文件写:回读文件并哈希──
- Aplicação da API: acompanhamento `GET`sobre o recurso alvo.
  Tradução do inglês para inglês:`GET`- Não.

Se a verificação falhar, o fluxo de trabalho está num estado conhecido de mau desempenho.

> 验证失败时工作流处于已知坏状态――回滚启动――

### Plano de retrocesso .

Cada acção consequente na proposta-depois-compromisso (Lessão 15) contém um plano de retrocesso.

> Propõe-depois-compromete ((第 15 课) 中每个后果性动作带回滚计划──类型:

- **In-band rollback**: inverter directamente o efeito colateral (`DELETE`Depois`INSERT`- Não .`Send-correction-email`após a envio).
  Tradução:**带内回滚**: direct反转副作用`INSERT`后  `DELETE`、enviar depois ‧enviar mais correio
- **Compensating transaction**: uma nova acção que neutraliza o original (patrão SAGA padrão).
  Tradução:**补偿事务**O que é que é o "São Paulo" (São Paulo)
- **Out-of-band rollback**Alerta um ser humano, pausa o fluxo de trabalho, deixa o mau estado para investigação.
  Tradução:**带外回滚**A polícia de Nova York, em Londres, disse que a polícia não estava a investigar o caso.

Ações sem retrocesso exigem um maior nível de TIH no momento do compromisso (Lessão 15 - desafio e resposta).

> Não-op 回滚("我们不能撤销 this") deve ser nomeado no提议中.

### Lei da UE sobre IA Artigo 14 leitura operacional .

O artigo 14.o exige "supervisão humana eficaz" dos sistemas de alto risco.

> 第 14 条要求高风险系统的有效人类监督"──运营术语中,实现者读为:

- Os pontos de controlo são consultáveis por um auditor.
  Tradução do inglês: checkpoint可被审计者查询──
- Os rollbacks são ensaiados (testados de ponta a ponta pelo menos uma vez).
  Tradução do inglês para tradução inglesa: 回滚演练 (((至少端到端测试一次) ▽
- A trilha de auditoria sobrevive a uma implantação (o backend do checkpoint não é efêmero).
  Tradução do inglês para tradução do inglês:
- As verificações falhadas são alertadas, não registadas silenciosamente.
  O que é que é um erro?

Um fluxo de trabalho que falhe no meio do compromisso, retoma e completa o efeito colateral sem um caminho de verificação + retrocesso não sobrevive ao teste do artigo 14.o.

> 提交中崩、恢复、无验证+回滚路完成副作用工作流不通过第 14条测试──

### O modo de falha acentuada: o duplo executar .

O incidente de produção mais comum neste espaço: Ação aprovada, iniciação de compromissos, retorno 200, falhas de fluxo de trabalho antes de persistir status, reinicialização e re-execução.

> O acidente de produção mais comum neste domínio: movimentos de aprovação, submissão, reencaminhamento, 200;

1. Ação aprovada, chave de independência k.
   Tradução do inglês: 动作批准, 等键 k。
2. Compromissos inicia, executa, retorna 200.
   Tradução do inglês:提交开始、执行、返回 200。
3. O fluxo de trabalho falha antes de persistir o status de "compromiso".
   Tradução do inglês para "Ação em desenvolvimento"
4. O fluxo de trabalho é reiniciado; vê "aprovado, mas não comprometido"; re-executado.
   中文翻译:工作流恢复; see"批准但未提交";重新执行──
5. Efeito secundário disparos duas vezes.
   O que é que é um problema?

Mitigação: persistir em uma intenção "em voo" antes da execução, executar com uma chave de idempotency, em seguida, marcar "comprometeu" apenas após a verificação pós-ação ser bem sucedida. Se o tiro de ação e o status write falhar, você sabe para verificar e (se necessário) refire. Se o status write é bem sucedido e a ação falha, você verificar e disparar exatamente uma vez através do caminho de recuperação.

> 缓解: executação pre-持久化"in-flight"意图, us等键执行, apenas em movimento após verificação sucesso após marcador "ha sido enviado"──如动作触发而状态写失败,你知道要验证(如必要) 重触发──如状态写成功而动作失败,你验证并通过恢复路径精确触发一次──

## Use-o com o framework implementado.
```figure
checkpoint-replay
```

## Usá-lo

`code/main.py`Implementa um fluxo de trabalho com controle de controle com idempotencia, pré-condições, verificação e retrocesso. O motorista simula quatro cenários: execução limpa, retoma após o acidente (apanhadas de idempotencia), falha de pré-condição (abortes de fluxo de trabalho sem disparos), verificação de falha (incêndios de retrocesso).

> `code/main.py`实现带等、前置条件、验证和回滚的检查点工作流──驱动器模拟四场景:干净运行、崩后重试(等捕获)、前置条件失败(工作流停止不触发)、验证失败(回滚触发)。

## Envia-o . Produto .

`outputs/skill-rollback-rehearsal.md`concebe um teste de ensaio de retrocesso para um fluxo de trabalho proposto e verifica o backend do ponto de controlo para verificar a persistência da trilha de auditoria.

> `outputs/skill-rollback-rehearsal.md`Para a proposta de trabalho, o projeto de revisão de um processo de avaliação e auditoria, a revisão de um processo de revisão e de um processo de revisão e de revisão de um processo de revisão e de revisão de um processo de revisão e de revisão de um processo de revisão e de revisão de um processo de revisão e de revisão de um processo de revisão e de revisão de um processo de revisão e de revisão de um processo de revisão e de revisão de revisão de revisão e de revisão de revisão de revisão e de revisão de revisão de revisão e de revisão de revisão de revisão.

## Exercícios.

1. Corra .`code/main.py`Verifique os quatro cenários, para o caso de acidente durante o compromisso, confirme os disparos de ação exatamente uma vez em todas as retemptadas.
   Tradução: 运行`code/main.py` verificar quatro cenários.  verificar o caso de um colapso no processo de entrega, confirmar o movimento em um ensaio repetido.

2. Modifique o padrão "marque como feito primeiro, depois faça" para que o status escreva incêndios após a ação. Reinicie o cenário de crash. Messa quantas ações duplicadas disparam.
   Tradução do inglês para "Preciso de marcar o início do processo"

3. Desenhar um plano de reestruturação para uma ação de produção específica (por exemplo, "postar para um canal Slack"). Classificar como dentro da banda, compensando ou fora da banda. Justificar a escolha.
   Tradução do inglês para "Relação de um processo de produção" (em inglês: "Relations of a process process process"), em inglês: "Relations of a process" (em inglês: process process process process process)

4. Tome um fluxo de trabalho que você conhece. Identifique cada transição de estado. Marque cada uma com um requisito de durabilidade (persistir / não persistir). Conte aqueles que você não está atualmente persistir.
   Chinese Language Translation: Get a Knowledge of Workflow. Identificar cada estado de transformação.

5. Teste repetido de retrocesso: desenhar um teste de ponta a ponta que execute um fluxo de trabalho real, o bloqueie e confirme os incêndios do caminho de retrocesso.
   Tradução do inglês em japonês:演练回滚测试:设计端到端测试运行真实工作流、崩、确认回滚路径触发──测试断言什么?

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Checkpoint | "Save point" | Every graph-state transition persists to a durable store |
| 检查点 | "保存点" | 每个图状态转换持久化到持久存储 |
| Lease | "Worker claim" | Short-lived claim that a worker is executing a run; expires on crash |
| 租约 | "Worker 声明" | worker 正在执行运行的短暂声明；崩溃时过期 |
| Precondition | "State gate" | Assertion that the state is still consistent with the approved action |
| 前置条件 | "状态门" | 状态仍与批准动作一致的断言 |
| Post-action verify | "Re-read check" | Confirm the side effect actually happened in the target system |
| 动作后验证 | "回读检查" | 确认副作用在目标系统中实际发生 |
| In-band rollback | "Direct undo" | Reverse the side effect with the inverse operation |
| 带内回滚 | "直接撤销" | 用逆操作反转副作用 |
| Compensating transaction | "SAGA undo" | A new action that neutralizes the original |
| 补偿事务 | "SAGA 撤销" | 抵消原始动作的新动作 |
| Mark-as-done-first | "Status write order" | Persist the committed status before returning from commit |
| 先标记完成 | "状态写顺序" | 从提交返回前持久化已提交状态 |
| Article 14 | "EU AI Act human oversight" | Operational: queryable checkpoints, rehearsed rollbacks, auditable trail |
| 第 14 条 | "EU AI 法案人类监督" | 运营：可查询检查点、演练回滚、可审计追踪 |

## Mais leitura 延伸阅读

- [Microsoft Agent Framework — Checkpointing and HITL](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) Primitivos de pontos de controlo e recuperação de arrendamento.
  Tradução do inglês: Check Check点原语和租约恢复。
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) Objetos duráveis como um substrato de estado.
  中文翻译:Objetos duráveis 作为状态基板。
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/) Linha de base regulatória.
  Tradução do português:监管基线。
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) enquadramento de confiabilidade para os fluxos de trabalho de longo prazo.
  Tradução do inglês:长程工作流的可靠性框架.
- [Anthropic — Claude Code Agent SDK: agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) Forma do fluxo de trabalho para Routines de código Claude.
  中文翻译:Claude Code Routines 的工作流形态──
