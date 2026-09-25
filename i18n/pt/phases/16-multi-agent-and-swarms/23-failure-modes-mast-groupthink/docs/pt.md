# Módos de falha  MAST, Groupthink, Monocultura, Erros em Cascata 失败模式 群体思维 MAST

> A taxonomia de referência para 2026 é **MAST**(Cemri et al., NeurIPS 2025, arXiv:2503.13657), derivado de 1642 traços de execução em 7 state-of-the-art open source MAS mostrando **41–86.7% failure rate**. Três categorias raízes: **Specification Problems**(41,77%)  ambiguidade de papel, definições de tarefas pouco claras; **Coordination Failures**(36,94%)  falhas de comunicação, dessincronização de estado; **Verification Gaps**(21,30%)  falta de validação, ausência de verificações de qualidade.**Groupthink**A família (arXiv:2508.05687) acrescenta: colapso da monocultura (o mesmo modelo base → falhas correlacionadas), viés de conformidade (agentes reforçam os erros uns dos outros), teoria de mente deficiente, dinâmica de motivos mistos, falhas de confiabilidade em cascata. Exemplo em cascata: tempestades de retoma em que uma falha de pagamento desencadeia retomas de encomendas, que desencadeiam retomas de inventário, que sobrecarregam o serviço de inventário (10 vezes a carga em segundos  necessitam de interruptores de circuito). Envenenamento da memória: a alucinação de um agente entra na memória compartilhada, agentes a seguir a corrente tratam-na como um fato; a precisão declina gradualmente, tornando doloroso o diagnóstico da causa raiz.**STRATUS**(NeurIPS 2025) relata uma melhoria de 1,5 vezes na mitigação e sucesso através de agentes especializados de detecção / diagnóstico / validação.

> **【中文解读】**Esta secção apresenta o modelo de falha de vários agentes e o grupo de pensamentos sobre os sistemas de falhas de vários agentes.

> **【拓展：failure modes mast groupthink→具体应用】**Do agente sistema                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 13 (Shared Memory), Phase 16 · 14 (Consensus and BFT), Phase 16 · 15 (Voting and Debate Topology) | **前置知识:** Phase 16 · 13（共享内存），Phase 16 · 14（共识与 BFT），Phase 16 · 15（投票与辩论拓扑）

> - Não .**【前置】**學本节前 請先掌握:Fase 16·13-15(共享内存/BFT/投票) ・MAST = 2026 多 Agent 失败模式的标准分类法。
> - Não .**【类比】**MAST 失败分类 = "hôpital急诊分诊"──三类根因:规格问题(42%角色不清)、协调失败(37%通信失灵)、验证缺失(21%无质检)──MAST 1642 条 痕迹 显示 41-87% 失败率多 Agent 不是银弹──Groupthink 家族:单一文化崩(同基模型 全错)、群体盲从级付联错支(修失触发重试暴,10 秒 10 倍负载)──重复:异见 Agent + 随机化发言顺序 + 断路器──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problema Introdução

Os sistemas multi-agentes falham 41-86,7% do tempo em tarefas reais (Cemri et al. 2025 mediram isso em 7 MAS de código aberto). Isso não é depurável por "somente adicionar mais agentes". As falhas têm causas estruturais. A taxonomia MAST dá-lhe as categorias. Esta lição mapeia cada categoria para um padrão concreto de detecção, diagnóstico e mitigação para que os números deixem de parecer arbitrários.

> Doo Agente  sistemas em missões reais 41-86,7% do tempo vai falhar (((Cemri  et al. 2025 em 7 个开源 MAS 上测量) ⋅ Não é " acrescentar mais Agente " em termos de capacidade de fazer o teste.

A prática de produção 2026 é tratar os modos de falha como entradas de design.

> A prática de produção de 2026 é um modelo de design de entrada que vai falhar. A sua estrutura não será "bem o suficiente" até que você possa se dirigir para cada classe MAST e dizer que sua implementação é uma medida de alívio.

## Conceptos básicos

### Categorias de MÁST

**Specification Problems (41.77% of failures).**A tarefa do agente não foi definida suficientemente estritamente.

> **规范问题（41.77% 的失败）。**A missão do agente não é suficientemente definida.

- Ambiguidade de papel: dois agentes pensam que são os críticos.
  O papel dos agentes é o de um autor.
- A tarefa foi subespecificada: "resumir isto" quando o usuário queria um ângulo específico.
  Tradução do inglês para japonês:任务规格不足:"总结这个",但用户想要特定角度──
- Critérios de sucesso implícitos: o agente não pode dizer se foi bem sucedido.
  中文翻译:成功标准隐含:Agente 无法判断是否成功──

Mitigações:

> 缓解措施:

- Escreva contratos de funções explícitos. O aviso de cada agente indica o que faz *e o que não faz*.
  Tradução do inglês para o inglês: 编写显式角色契约──每个代理的提示声明它做什么和不做什么.
- Antes de começar, define "feito parece X".
  Tradução do inglês para o inglês: Each task's acceptance test.
- Verificação das especificações pré-voio: um agente separado revisa a definição da tarefa antes do envio.
  Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame: Pre-exame is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is

**Coordination Failures (36.94%).**Comunicação ou falhas de estado.

> **协调失败（36.94%）。**Comunicação ou estado de incapacidade.

Exemplos:

> - Não .

- Dois agentes atualizam o estado compartilhado sem sincronização.
  Tradução do inglês:
- Mensagem perdida entre agentes (falha da fila, tempo de espera).
  O agente 间消息丢失 (Agent 间消息丢失)
- Drift de estado: o agente A acha que a tarefa está concluída; o agente B ainda está executando.
  中文翻译:状态漂移:Agente A 认为任务完成;Agente B ainda está em execução。

Mitigações:

> 缓解措施:

- Estado compartilhado com simultâneo otimista.
  Tradução do idioma japonês:带乐观并发的版本化共享状态──
- Reconhecimento explícito de mensagens críticas (reter até aque).
  Tradução do inglês: [default]
- Pontos de controlo periódicos de sincronização de estado; detecção da deriva precoce.
  Tradução do inglês para "periodical state"

**Verification Gaps (21.30%).**Não há verificação independente das saídas.

> **验证缺口（21.30%）。**Não há controlo independente para a saída.

Exemplos:

> - Não .

- Um agente afirma ser bem sucedido, ninguém verifica.
  Tradução do inglês:
- A cadeia de agentes, cada um, confia na saída do anterior.
  Tradução do original: "Agenta de cada um de nós".
- A cobertura de teste que falta no comportamento composto emergente.
  O que é que é o comportamento de um grupo de pessoas?

Mitigações:

> 缓解措施:

- Agente verificador independente (Lessão 13). Acesso à fonte independente, somente de leitura.
  中文翻译:独立验证 Agent (独立验证) ([[13o 课) ]]
- Contrato de transferência explícito: "A saída de A deve passar o check C antes de B começar".
  Tradução do inglês para tradução do inglês:
- Registros de resultados para análise pós-hoc.
  O resultado é usado para análise de eventos.

### Família de pensamento em grupo (arXiv:2508.05687)

Cinco falhas relacionadas quando os agentes homogeneizam ou imitam uns aos outros:

**Monoculture collapse.**O mesmo modelo base ou dados de treinamento → erros correlacionados. Quando três agentes compartilham um LLM, eles compartilham suas alucinações.

**Conformity bias.**Os agentes se adaptam ao colega mais alto ou mais confiante, mesmo quando estão errados.

**Deficient ToM.**Os agentes não conseguem modela-se mutuamente nas crenças; a coordenação cai em colapso (Lessão 18).

**Mixed-motive dynamics.**Os agentes com incentivos parcialmente alinhados desviam para o meio de compromisso, o que não satisfaz ninguém.

**Cascading reliability failures.**O padrão de erro de um componente desencadeia padrões de erro em componentes dependentes.

### Exemplo em cascata  a tempestade de retomada

Um padrão clássico de incidentes de 2026:

```
payment service fails 10% of requests
   ↓
order agent retries payment (exponential backoff but naive)
   ↓
each retry is a new order-inventory check
   ↓
inventory service sees 2x normal load
   ↓
inventory service starts timing out
   ↓
every order retries inventory check
   ↓
inventory service sees 10x normal load
   ↓
cluster goes down
```

A solução é clássica:**circuit breakers**- Quando a taxa de erro inferior exceder o limiar, curto-circuito com resultados em cache ou por defeito.

Os interruptores de circuito são uma das poucas medidas de mitigação de falhas de vários agentes que emprestamos diretamente a partir de sistemas distribuídos sem modificações.

### Envenenamento da memória (revisto)

A partir da lição 13: a alucinação de um agente torna-se fato de memória compartilhada; agentes a jusante raciocinam sobre o fato envenenado.

A degradação gradual da precisão é o sintoma.

Mitigation: só apenda registro, proveniência, verificador não-escritível. Já abordado na lição 13.

### STRATUS  Agentes especializados para detecção de falhas

O STRATUS (NeurIPS 2025) relata uma melhoria de 1,5 vezes no sucesso da mitigação quando se implementa:

- **Detection agent.**Observação dos padrões de sintomas (alto desacordo, picos de retest, deriva de precisão).
- **Diagnosis agent.**Dados os sintomas, deduz a provavelmente causa raiz da taxonomia MAST.
- **Validation agent.**Após a aplicação de uma mitigação, verifique se os sintomas desaparecem.

Esta é a resposta a incidentes no estilo SRE, aplicada a sistemas de agentes.

### A auditoria de modo de falha

Uma melhor prática para 2026 é uma auditoria anual (ou por lançamento maior) de modo de falha:

1. **Trace sample.**Coletar 1000 traços reais de execução.
2. **Categorize.**Para cada falha de rastreamento, mapear para categorias MAST + Groupthink.
3. **Compute failure-by-category rate.**Que categorias dominam o seu sistema?
4. **Rank mitigations.**Qual solução eliminaria a maioria dos falhas?
5. **Pick 2-3 mitigations.**Implementação; re-auditoria no próximo trimestre.

A disciplina é mais importante do que as escolhas específicas.

### Quando os sistemas falham silenciosamente

A categoria de falhas mais perigosa é falha de corretão silenciosa. Um sistema que falha em voz alta (crash, exceção, alerta) pode ser monitorado. Um sistema que produz saídas plausíveis mas erradas não pode ser detectado por registros de exceção. É por isso que as lacunas de verificação são a categoria mais cara por falha, embora sejam apenas 21,30% em contagem.

Investi em:
- Revisão humana baseada em amostras.
- Testes de regressão do conjunto de dados dourados.
- Verificação de resultados importantes.

### Falha versus falha lenta

Algumas falhas são imediatas; outras são lentas. falhas imediatas (out of time, desajuste de esquema, erro de autor) são baratas de detectar. falhas lentas (intoxicação da memória, deriva de monocultura, ambiguidade de papel) são caras de detectar e prevenir.

A mudança de engenharia de 2026: proxies de falha lenta do instrumento para que você possa capturar a deriva antes que se torne um erro visível.

## Construí-lo.
```figure
a5-retry-cascade
```

## Construí-lo

`code/main.py`Implementos:

- `FailureTaxonomy` categoriza os incidentes simulados em categorias MAST + Groupthink.
- `CircuitBreaker` padrão clássico; abre quando a taxa de erro excede o limiar.
- `RetryStormSimulator` mostra a falha de cascata; liga/ desliga o interruptor de circuito.
- `DetectionAgent`- Simptoma de STRATUS.

- Correr .

```
python3 code/main.py
```

Produção esperada:
- Tormenta de retest sem interruptor de circuito: erros de inventário explodem (simulados).
- com interruptor de circuito: tampa no limiar; respostas em modo degradado servidas.
- O agente de detecção marca o padrão e nomeia a categoria MAST.

## Usa-o. Usa-o.

`outputs/skill-mast-auditor.md`Executa uma auditoria de modo de falha de estilo MAST em um sistema multi-agente.

## Envia-o .

Disciplina de modo de falha na produção:

- **MAST audit per quarter.**Não é anual, as categorias mudam à medida que o sistema cresce.
  Tradução:**每季度 MAST 审计。**Não é anual.
- **Circuit breakers everywhere.**Cada chamada de saída para qualquer serviço dependente.
  Tradução:**到处都是熔断器。**Cada estação de saída de serviço de dependência é utilizada em valores de 5 a 10% de erro.
- **Golden datasets.**Pequenas, de alta qualidade, verificadas à mão, testes de regressão contra elas semanalmente.
  Tradução:**黄金数据集。**O tipo de material que é utilizado para a produção de produtos de qualidade é o tipo de material que é utilizado para a produção de produtos de qualidade.
- **STRATUS trio.**Detecção + Diagnóstico + Agentes de validação monitorando a produção. Comece com apenas o agente de detecção; adicione o diagnóstico quando os sintomas são barulhentos.
  Tradução:**STRATUS 三重奏。**检测 + 诊断 + 验证 Agente 监控生产――从检测 Agente 开始;当症状杂时添加诊断――
- **Failure budget.**Explicita a taxa de falhas por categoria.
  Tradução:**失败预算。**按类别失败率显然SLO──超出预算触发停止发布对话──

## Exercícios.

1. Corra .`code/main.py`Confirme que o interruptor de circuito bloqueia a tempestade, varia o limiar de falha e observa a compensação.
2. Implementar um **slow-failure proxy**A taxa de concordância entre três agentes paralelos. Quando cair drasticamente, activa um alerta. Simula uma deriva de monocultura, correlação gradual das saídas dos agentes.
3. Leia Cemri et al. (arXiv:2503.13657). Escolha um dos seus 7 sistemas MAS e mapeie as suas três principais categorias de falhas.
4. Leia o artigo "Grupo de reflexão" (arXiv:2508.05687). Identifique qual dos cinco padrões é mais difícil de detectar na produção.
5. Desenhe um trio de detecção-diagnóstico-validação de estilo STRATUS para um sistema específico de vários agentes que você conhece. Que sintomas a detecção observa? Que mitigações o diagnóstico recomenda? Como a validação confirma que funcionam?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MAST / MAST 分类法 | "The 2026 taxonomy" / "2026 年分类法" | Cemri 2025; 3 root categories + 14 sub-types of failures. / Cemri 2025；3 个根类别 + 14 个失败子类型。 |
| Specification Problem / 规范问题 | "Role ambiguity" / "角色模糊" | Task or role under-defined; agents do not know what to do. / 任务或角色定义不足；Agent 不知道做什么。 |
| Coordination Failure / 协调失败 | "State drift" / "状态漂移" | Communication or sync breakdown between agents. / Agent 之间的通信或同步故障。 |
| Verification Gap / 验证缺口 | "No one checked" / "没人检查" | Outputs accepted without independent validation. / 输出未经独立验证即接受。 |
| Groupthink family / 群体思维族 | "Homogeneity failures" / "同质性失败" | Monoculture, conformity, deficient ToM, mixed-motive, cascading. / 单一文化、从众、ToM 不足、混合动机、级联。 |
| Monoculture collapse / 单一文化崩溃 | "Same model, same hallucinations" / "相同模型，相同幻觉" | Correlated errors from shared base model or training data. / 共享基础模型或训练数据的相关错误。 |
| Retry storm / 重试风暴 | "Cascading error amplification" / "级联错误放大" | One failure triggers retries which amplify load downstream. / 一次失败触发重试，放大下游负载。 |
| Circuit breaker / 熔断器 | "Fail fast on error rate" / "错误率快速失败" | Open when error rate exceeds threshold; short-circuit with default. / 错误率超阈值时断开；用默认值短路。 |
| STRATUS | "Incident response trio" / "事件响应三重奏" | Detection + diagnosis + validation agents. 1.5x mitigation success. / 检测 + 诊断 + 验证 Agent。1.5 倍缓解成功。 |
| Memory poisoning / 记忆投毒 | "Hallucinations propagate" / "幻觉传播" | Shared-memory fact tainted; downstream agents reason on poison. / 共享记忆事实被污染；下游 Agent 在毒化数据上推理。 |

## Mais leitura 延伸阅读

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Taxonomia MAST, NeurIPS 2025
- [Groupthink failures in multi-agent LLMs](https://arxiv.org/abs/2508.05687) monocultura, conformidade e taxonomia de cinco famílias
- [STRATUS — specialized agents for MAS incident response](https://neurips.cc/) Inscrição no processo NeurIPS 2025 (detecção + diagnóstico + validação)
- [Release It! — stability patterns (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/) a referência canónica do interruptor de circuito
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) Notas de falha de produção
