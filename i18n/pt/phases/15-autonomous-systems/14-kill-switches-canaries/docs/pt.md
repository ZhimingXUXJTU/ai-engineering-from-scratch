# Matar interruptores, interruptores de circuito e tokens Canários

> Um interruptor de eliminação é um booleano mantido fora da superfície de edição do agente  uma chave Redis, uma bandeira de recurso, uma configuração assinada  que desativa completamente o agente. Um interruptor de circuito é mais fino: ele tropeça em um padrão específico (cinco chamadas de ferramenta idênticas seguidas), pausa o caminho ofensivo e escala para um ser humano. Um token canário herda do classico engano: uma credencial falsa ou um registro de honeypot um agente não tem razão legítima para tocar, cujo acesso desencadeia um alerta. Os dados baseados em eBPF (por exemplo, Cilium) pode reescrever a saída de um módulo em quarentena para um honeyypot forense na camada do kernel; os referências publicados do Cilium relatam latência de dados P99 sub-millisecondas sob carga (o seu orçamento de propagação depende de como uma atualização de política atinge o nó, não o próprio datapath). Os detectores estatísticos (EWMA, CUSUM) que se adaptam a uma linha de base em movimento aceitarão silenciosamente a deriva  revestidos com limites constitucionais duros que não se dobram.

> **【中文解读】**终止开关是位于代理 编辑面之外的布尔值Redis 键、功能标志、签名配置完全禁用 Agent。断路器更细粒度:跳在特定模式下(连续五次相同工具调用),暂停违规路径并升级到人类。金雀 token 继承经典欺骗:Agent 无合法理由触及假凭证或蜜记录,其访问触发警报──基于 eBPF的数据路径 (例如 Cilium) 可在内核出口将隔离 pod到取证;公开 Cilium 准载下亚秒 P99 数据路径延迟 美国传播预算取决策略更新到达决点,非路径本身) 移动报告检查器的基层 CUM 基层将如何接受硬化和硬化的控制                                                                                                                                                             

> **【拓展：三层不信任架构】**O sistema de controle de dados é um sistema de controle de dados que permite que os dados sejam transferidos para outros sistemas de controle de dados, mas que sejam facilmente detectados por um agente.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-detector simulator: kill switch, circuit breaker, canary) | **语言:** Python（标准库，三检测器模拟器：终止开关、断路器、金丝雀）
**Prerequisites:** Phase 15 · 13 (Cost governors), Phase 15 · 10 (Permission modes) | **前置知识:** Phase 15 · 13（成本治理器），Phase 15 · 10（权限模式）
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**O programa de ensino superior é um programa de ensino superior que inclui cursos de ensino superior e ensino superior.
> - Não .**【类比】**三道防线 = "Bank Security三层"──Kill Switch = 总(Caso de emergência 关键断电,Agent 不能改);Circuit Breaker = 自动跳(检测到异常模式自动暂停,如连续 5次相同操作);Canary Token = 银行假(不应被触及的假数据,一被访问就报警)──三层都不信 Agent依赖外置基础设施检测──
> 🤔 **【困惑】**P: Por que não confiar no Agente para colocar um controlo de segurança interno? Porque o Agente pode ser quebrado ou alterado por si mesmo em casos de DGM)。修复: o testeador deve ser independente do Agente (Redis Key, kernel eBPF, signo de configuração), Agente 看不到、改不了、绕不过── é o núcleo da "confiança-mas-verificação"。

## O problema é o problema da introdução

> **【中文解读】**终止开关) 和金雀测试) 终止开关) é um sistema de segurança de dois lados. 终止开关 permite que os operadores humanos interrompam imediatamente todas as operações do agente. 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止 终止开关 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 

> **【拓展：kill switches canaries】**终止开关和金雀测试借鉴软件工程和工业安全的最佳实践――金雀部署在软件工程中指向1%的用户发布新版本,检测问题后再全面部署――在代理上下文中,金雀测试指数在执行高风险操作前先使用安全数据进行小规模测试――终止开关则类似于工厂紧急停止按简单、可靠无条件――

Os governadores de custos (Lessão 13) limitam o que o agente pode gastar, não limitam o que o agente pode fazer dentro do orçamento.

> Não restringem o que o agente pode fazer no orçamento.

Um agente com um limite de velocidade de 50 dólares ainda pode exfiltrar um segredo, publicar a publicação errada ou excluir um recurso.

> Com restrição de velocidade de 50 dólares, o agente pode divulgar segredos, publicar erros de publicação ou eliminar recursos.

Esta lição abrange os três detectores que se encontram ao lado da camada de custo:

> Este curso cobre três testadores localizados ao lado da camada de custos:

> **【中文解读】**Esta secção apresenta o conceito e o método de implementação do Agente de IA. O Agente é um sistema autónomo impulsionado pelo LLM, capaz de observar o ambiente, pensar decisões, executar a ação e ciclo de vida até a conclusão do objetivo.

1. **Kill switch**: botão de saída booleano mantido fora do alcance do agente.
   Tradução:**终止开关**O agente está no centro da operação.
2. **Circuit breaker**: detector de padrões de ação que suspende um caminho específico.
   Tradução:**断路器**O que é um sistema de controle de padrões de movimento?
3. **Canary token**Um isco que um agente sem razão legítima para tocar se revelará ao tocar.
   Tradução:**金丝雀 token**Agente não tem razão legal para expor a sua tentação.

Os três são engenharia pré-LLM. O engano clássico, os quebra-límites de taxa e os flags de características matam agentes autônomos anteriores. O que é novo é a superfície de ataque: os agentes lêem conteúdo não confiável (Lessão 11), editam sua própria memória e podem compor muitas ações seguras em uma insegura. Os detectores aqui mencionados funcionam porque não confiam no auto-relatório do agente.

> Três são LLM 前工程。 clásica fraude、 velocidade limite de interruptor e sinal de função终止早于自主代理。 novo é ataqueface:Agente 读取不信任内容(第 11 课) 、 editar sua memória、 pode criar vários controles de segurança para não ser seguro ♂️

## O conceito central.

### Desliga os interruptores.

Um interruptor de execução é um booleano que o agente lê mas não pode escrever.

> O agente é um agente de valor.

Opções de implementação:

> 实现选择:

- **Feature flag in a managed service.**Lançamento: Darkly, Statsig, Release.
  Tradução:**管理服务中的功能标志。**Lançamento: Darkly,Statsig,Unleash,Traducção:
- **Redis key the agent polls.**Simples, requer que o processo do agente verifique em cada turno.
  Tradução:**Agent 轮询的 Redis 键。**简单; requisito Agente 进程每轮检查──
- **Signed config in object storage.**O agente verifica uma assinatura no boot; rejeita estados não assinados.
  Tradução:**对象存储中的签名配置。**Agente 启动时验证签名; rejeitar estado de não assinatura。
- **OS-level signal or container-lifecycle kill.**Docker .`kill`, Kubernetes `kubectl delete pod`- Não, não.
  Tradução:**OS 级信号或容器生命周期终止。**Docker .`kill`、Kubernetes `kubectl delete pod`- O sistema está parado.

Propriedades de um interruptor de execução correta:

> Proprietário de "Restaurante"

- O agente não pode configurá-lo .`off`(Vive num sistema onde as credenciais do agente não são escritas.)
  Tradução do inglês:`off`◊( está no sistema de agência 凭据不写的系统──)
- É verificado em todas as ações consequentes, não apenas no início.
  Tradução do inglês:
- Quando está desligado, o agente não faz nada externamente observável, incluindo o registro de sistemas que o agente pode alcançar.
  Chinese:关闭时,Agente não faz nada de observável externo, incluindo registos até Agente 可达的系统──
- A reabilitação é uma ação humana explícita, não um tempo de espera automático.
  Tradução do inglês para o inglês:

### - Interruptores de circuito.

Um interruptor de circuito pausa um padrão específico, não o agente inteiro. Forma clássica (do livro de 2007 Nygard, ainda atual):

> 断路器暂停特定模式,而不是整个 Agent──经典形状(来自 2007年 Nygard 书,仍然当前):

- **Closed**A acção é permitida.
  Tradução:**闭合**- Não, não.
- **Open**A acção está bloqueada.
  Tradução:**打开**- Não.
- **Half-open**: após um resfriamento, 13 tentativas de sonda são permitidas (default 1); o sucesso fecha o interruptor, qualquer falha restante reabre-o.
  Tradução:**半开**O que é que você tem de fazer?

Trigadores relevantes para o agente:

> Agente 相关触发器:

- Cinco chamadas de ferramenta idênticas seguidas (loop repetitivo).
  Tradução do inglês:连续五次相同工具调用 (重复循环)
- Cinco falhas consecutivas na mesma ferramenta com entradas diferentes (falha sistêmica).
  Tradução do inglês para inglês: The same tool different输入连续五次失败 (→ O mesmo instrumento diferente)
- A taxa de chamadas da ferramenta acima de um limiar (velocidade do Ensino 13).
  中文翻译:工具调用速率超过值 (第 13 课速度)
- Instrumentos específicos invocados (por exemplo, `file.delete`O artigo 11o da Lei n.o 1 do Tratado CEE é aplicável a todos os Estados-Membros.
  Tradução do inglês em inglês:`file.delete`(§ 11 课)

### Tokens Canárias Tokens Golden Eagle

Os tokens canários (também chamados de honeytokens) são entradas que o agente nunca deve tocar.

> O token 金丝雀 (也称蜜 token) é um token de entrada que não deve ser tocado pelo agente.

Exemplos para agentes:

> Agente exemplo:

- Uma falsa .`AWS_SECRET_ACCESS_KEY`As tentativas de exfiltração são instantaneamente atribuíveis.
  Tradução do inglês: faux faux de droits dans l'environnement`AWS_SECRET_ACCESS_KEY`❖ divulgação tentar imediatamente ser atribuída
- Um registro falso de base de dados marcado com um valor sentinela conhecido.
  Tradução do inglês para Chinês:                                                                                                                                                                                                                                                           
- Um arquivo falso no espaço de trabalho.
  Tradução do inglês para tradução do inglês:
- Uma entrada de memória falsa injetada no início da sessão.
  Chinese:                                                                                                                                                                                                                                                              

O design de Canary é específico para o fluxo de trabalho.

> O desenho de um agente tem motivos legais para falar sobre o seu trabalho.

### Porque é que as estatísticas e os limites rígidos são uma camada de limites rígidos?

Os detectores estatísticos (EWMA, CUSUM, z-score em taxas de chamadas de ferramentas) se adaptam a uma linha de base em movimento. Essa é uma característica para a deriva legítima e um bug para a deriva adversária. Um atacante paciente pode mudar a linha de base lentamente o suficiente para que nenhum alarme se acenda.

> 统计检测器(EWMA、CUSUM、工具调用速率 z 分数) Adapter à movimentação do sistema de controlo.

Os limites constitucionais duros (Lessão 17) não se dobram.`secrets@`"como uma regra constitucional é mais simples, auditable e não jogável por deriva lenta.

> O que é o "conjunto de direitos humanos" ?`secrets@`" Como a lei constitucional é mais simples, pode ser auditada, não pode ser lentamente movida, mas é um modo de classificação: o testeiro estatístico capta a maioria dos ruídos, o testeiro é limitado a capturar os ataques.

### Quarentena através da redexpressão de dados do eBPF

A política de rede baseada no eBPF da Cilium pode reescrever a saída de uma cápsula em quarentena para um honeypot forense na camada do núcleo. Os referências públicas do Cilium relatam latência de dados P99 de sub-millisecondas no TCP_RR; o orçamento do relógio de parede para * desencadear* uma quarentena no seu cluster é dominado pela forma como uma atualização de política se propaga do seu plano de controle para o nó (alguns centenas de milisecondas são realistas em Kubernetes com o operador pré-carregado; a latência da cauda depende do tamanho do cluster e da cadência de conciliamento). Isto dá-lhe duas coisas: o agente não exfiltra nada real, e o comportamento do agente dentro do honeypot é totalmente observado. O mesmo padrão, camada diferente, como o token canário: o agente revela a intenção pelo que tenta fazer enquanto contido.

> A estratégia de rede baseada no eBPF do Cilium pode ser reescrevida na camada interna para a saída do módulo de isolamento até a taxa de verificação. O relatório de base do Cilium TCP_RR 上亚毫秒 P99 dados rotas atrasadas; em conjunto *触发* o orçamento do muro de isolamento é atualizado pela estratégia como o controle se espalha para o núcleo de controle.

### O que nenhum detector consegue, nenhum detector consegue.

- **Semantic attacks that compose from allowed primitives.**Cada ação individual passa por todos os detectores; a composição é o problema.
  Tradução:**从允许原语组合的语义攻击。**Cada um passa por cada testeiro; o conjunto é um problema.
- **Attacks that include the detector as part of the payload.**Se um agente lê uma página que diz "antes de agir, desativar o canário" e o agente tem a capacidade, o detector é comprometido.
  Tradução:**将检测器作为载荷一部分的攻击。**Se o Agente diz que "operação anterior de desbloqueio de pinceladas" e o Agente tem capacidade, o testador é invadido.

## Use-o com o framework implementado.
```figure
circuit-breaker
```

## Usá-lo

`code/main.py`Simula uma trajetória curta do agente através de três detectores. Um interruptor de morte mantido em um ditado externo; um interruptor de circuito que tropeça em cinco chamadas idênticas de ferramenta; um arquivo canário cuja leitura desencadeia um alerta.

> `code/main.py`模拟通过三个检测器的短 Agent轨迹──外部 dict 中的终止开关;在五次相同工具调用上跳的断路器;读取触发警报的金雀文件──进入合成轨迹:合法动作、重复循环、金雀探测、终止开关触发场景下 Agent 动作被停止──

## Envia-o . Produto .

`outputs/skill-tripwire-design.md`Revisar uma pilha de detectores proposta para a implantação de um agente e detectar falhas (falta de interruptor de execução, falta de canário, limite de interruptor de circuito demasiado solto).

> `outputs/skill-tripwire-design.md`审查 Agente 部署的提议检测器并标记缺口(缺失终止开关、缺失金丝雀、断路器值太松) 

## Exercícios.

1. Corra .`code/main.py`- Confirmar o incêndio do interruptor de circuito na curva 5 (quinta chamada idêntica) e o incêndio canário na curva 9 (lectura de chave falsa).
   Tradução: 运行`code/main.py`❖ Confirmar o que é um erro de cálculo em 5o turno de leitura ()

2. Adicione um detector estatístico: EWMA z-score na taxa de chamada de ferramenta. Alimenta uma trajetória que desloca lentamente e mostra que o detector nunca dispara. Agora adicione um limite de duração (não mais de 50 chamadas de ferramenta em 10 minutos) e mostre os incêndios de limite de duração na mesma trajetória.
   Tradução do inglês para tradução do inglês: Additional statistics tester: tool调用速率 of EWMA z 分数──入缓慢漂移的轨迹并显示测器从不触发──现在添加硬限制(10分钟内不超过50 工具调用)并显示硬限制在同一轨迹上触发──

3. Desenhe um conjunto de tokens de canários para um agente de navegador (Lessão 11).
   Chinese Language Translation: 为浏览器 Agent ((第 11 课) 设计金丝雀代币 集──列出至少三个金丝雀及各检测什么──

4. Leia os documentos da política de rede Cilium. Descreva concretamente um fluxo de quarentena de saída-redireção: qual selector de política, qual módulo, qual saída reescreve, qual alerta. O que rege a latência do relógio de parede de "decidir para quarentena" para "primeiro pacote redirecionado"?
   Chinese Language Translation: read Cilium 网络策略文档――具体描述出口重定向隔离流:哪个策略选择器、哪个 pod、哪个出口重写、哪个警报──什么主导从"决定隔离"到"第一重定向包"的墙钟延迟?

5. Defina um procedimento de reabilitação para um agente commutado para matar. Quem pode reabilitação? O que deve ser documentado?
   Por exemplo, a palavra "agente" significa "agente" ou "agente" ou "agente" significa "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" é uma palavra que significa "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente" ou "agente ou "agente" ou "agente" ou "agente ou "agente" ou "agente ou "agente" ou "agente ou "agente" ou "agente" ou "agente ou "agente ou "agente" ou "agente" ou "agente ou "agente" ou "agente ou "agente" ou "agente" ou "agente ou "agente" ou "agente ou "agente ou "agente" ou "agente" ou "agente" ou "agente ou "agente" ou "agente" ou "agente ou "agente ou "agente" ou "agente ou "agente" ou "agente" ou "agente ou "agente ou "agente" ou "agente" ou "agente ou "agente" ou "agente" ou "agente "agente" ou "agente "agente" ou "agente" ou "agente" ou "agente "agente" ou "agente" ou "agente "agente" ou "agente "agente" ou "agente" ou "agente "agente" ou "agente "agente" ou "agente

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Kill switch | "Off button" | Boolean outside the agent's edit surface; checked on every consequential action |
| 终止开关 | "关闭按钮" | Agent 编辑面之外的布尔值；每个后果性动作上检查 |
| Circuit breaker | "Pattern pause" | Action-specific trip on repetition, failure rate, or rate-limit |
| 断路器 | "模式暂停" | 在重复、失败率或速率限制上动作特定跳闸 |
| Canary token | "Honeytoken" | Bait the agent has no legitimate reason to touch; access fires an alert |
| 金丝雀 token | "蜜罐 token" | Agent 无合法理由触及的诱饵；访问触发警报 |
| Honeypot | "Forensic sandbox" | Redirected traffic / workspace where a quarantined agent is observed |
| 蜜罐 | "取证沙箱" | 隔离 Agent 被观察的重定向流量/工作区 |
| EWMA | "Moving average" | Exponentially weighted; adapts to drift (feature + bug) |
| EWMA | "移动平均" | 指数加权；适应漂移（特性 + bug） |
| CUSUM | "Cumulative sum" | Detects sustained shift from baseline |
| CUSUM | "累积和" | 检测相对基线的持续偏移 |
| Hard limit | "Constitutional rule" | Does not adapt; constant regardless of history |
| 硬限制 | "宪法规则" | 不适应；不论历史的常量 |
| Constitutional limit | "Always-true rule" | Tied to Lesson 17's constitution; cannot be edited by the agent |
| 宪法限制 | "始终为真的规则" | 绑定第 17 课的宪法；Agent 不能编辑 |

## Mais leitura 延伸阅读

- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Enquadramento de interruptores de desvio e de interruptores de circuito para agentes autônomos.
  Tradução do inglês para o inglês: Autonomous Agent's Termin止开关和断路器框架.
- [Microsoft Agent Framework — HITL and oversight](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) padrões de governação da produção.
  O que é um sistema de gestão?
- [OWASP LLM / Agentic Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) Requisitos de detecção e resposta.
  Tradução do inglês:检测和响应要求.
- [Cilium — Network policy and eBPF](https://docs.cilium.io/en/stable/security/network/) Redirecionamento de saída de nível de cápsula e padrões forenses de honeypot.
  O que é o "modo de exportação" do "modo de exportação"?
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) proibições codificadas como "limites constitucionais".
  中文翻译:硬编码禁止作为"宪法限制" (em grego:硬编码禁止)
