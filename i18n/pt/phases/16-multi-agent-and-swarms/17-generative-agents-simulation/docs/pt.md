# Agentes geracionais e simulação emergente

> Park et al. 2023 (UIST '23, arXiv:2304.03442) povoado **Smallville**, uma caixa de areia de 25 agentes, com uma arquitetura de três partes: **memory stream**(registro de linguagem natural), **reflection**(sínteses de nível superior que o agente gera sobre o seu próprio fluxo), e **plan**(comportamento de nível diário, depois sub-plans). O resultado histórico foi o surgimento da festa do Dia dos Namorados: um agente sementeou com "quer organizar uma festa do Dia dos Namorados", sem mais roteiro, produziu convites espalhados pela população, datas coordenadas, e a festa aconteceu  de 24 agentes que começaram sem saber disso. As ablações mostram que os três componentes são necessários para a credibilidade. Os falhas documentadas são erros de norma espacial (entrada em lojas fechadas, partilha de banheiros para uma pessoa). Esta é a arquitetura de referência para simulações de agentes e avaliação social multi-agente em 2026.

> **【中文解读】**Este episódio apresenta a experiência de 25 agentes de IA em uma comunidade virtual.

> **【拓展：generative agents simulation→具体应用】**斯坦福 实验 实验 Park et al., 2023) criou 25 agentes de IA em vida autónoma em uma pequena cidade virtual todos os dias de ascensão, ascensão, socialização, formação de relacionamentos e memórias.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 04（原语模型），Phase 16 · 13（共享内存）

> - Não .**【前置】**O estudo foi realizado em uma área de estudos de ciências da saúde e da saúde, onde a maioria dos casos de doenças cardiovasculares ocorrem em crianças.
> - Não .**【类比】**Smallville = "AI 版模拟人生"──25 个 AI 居民各有生活、记忆、计划──情人节派对奇迹: 一个代理 想办派对→邀请传开→其他人调整日程→派对真发生全是涌现,无脚本──三件套:memory stream(经历日志) + refleção(自我总结) + plano(日计划)──三者缺一不可, 删除任一代理 行为变得不可信──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problema Introdução

A maioria dos sistemas multi-agentes são equipes estritamente escritas: planos de planejamento, códigos de codificação, revisões de revisores. Isso funciona para tarefas bem definidas. Não captura o comportamento emergente e não escrito que surge quando os agentes têm memória, prioridades e um mundo aberto. Pesquisa, simulação da sociedade e AI de jogos precisam deste segundo tipo.

> A maioria dos sistemas de agentes é uma equipe de escritos estreitos: planejador, editor, codificador, revisor, revisor. Isso é válido para definir tarefas definidas. Mas não pode captar como um agente, possuindo memória, prioridade e comportamento não-escritor no mundo aberto.

A arquitetura de Smallville é o ponto de referência para isso. Até Park 2023, as melhores simulações de agentes eram seguidores de guiões superficiais; depois disso, o padrão é o padrão padrão para agentes geradores em mundos abertos. Se você construir uma simulação de agente em 2026, você está usando os três componentes de Smallville ou justificando explicitamente por que não está.

> A arquitetura de Smallville é a base deste tipo. Até Park 2023, o melhor agente é um seguidor de um roteiro de baixo nível; depois, esse modelo se torna um padrão de agente gerado em um mundo aberto. Se você construir um agente em 2026, você vai usar os três componentes de Smallville, ou explicá-lo claramente por que não o usa.

## Conceptos básicos

### Os três componentes

**Memory stream.**Um registro de observações, ações, reflexões e planos apenas apêndice. Cada entrada tem um timestamp, um tipo, uma descrição (linguagem natural) e metadados derivados: **recency**- Não .**importance**(auto-rated 1-10 pelo agente), e **relevance**(similidade de cosina com a consulta corrente).

> **记忆流。**Uma observação, ação, reflexão e planejamento adicionais.**时效性**- Não.**重要性**(Agente 自评 1-10)**相关性**(Com a semelhança do resto da pesquisa actual)

```
[2026-02-14 09:12:03] observation: Isabella Rodriguez asked me if I like jazz
[2026-02-14 09:14:22] reflection:   I enjoy long conversations about music
[2026-02-14 10:05:00] plan:         Attend Isabella's Valentine's Day party tonight
```

A recuperação da memória combina as três pontuações: `score = w_recency * e^(-decay * age) + w_importance * importance + w_relevance * cos_sim`As entradas de cima-k entram no prompt atual.

**Reflection.**Periodicamente (a cada N memórias ou em eventos importantes), o agente gera síntese de ordem mais alta a partir de memórias recentes. As entradas de reflexão voltam ao fluxo e são recuperáveis como qualquer outra memória. É assim que os agentes construem "entendimentos"  o equivalente da arquitetura de crenças de longo prazo.

> **反思。**定期(每 N 条记忆或在重要事件时),Agento gerou um complexo de alta fase na memória recente.

**Plan.**A decomposição de cima para baixo. Primeiro, um plano de nível diário em grandes traços ("vai trabalhar, jantar com Klaus"). Depois planos a nível horário.

> **计划。**O plano é modificável: quando observado e planejado em contradição, o agente reorganiza o plano em parte.

### Por que as três coisas importam (abertura)

Park et al. executaram ablações que deixam cair cada uma das observações, reflexão e plano.

> Park  et al. realizaram experiências de dissipação, separadamente eliminando observação, reflexão e planejamento.

- Sem .**observation**O agente perde o contexto e age com crenças obsoletas.
  Não há**观察**,Agente 缺失上下文, baseado em passado convicção acção¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬
- Sem .**reflection**O agente não pode formar crenças de ordem superior; as interações permanecem superficiais.
  Não há**反思**,Agente  incapaz de formar alta classe de crença; 交互保持浅层──
- Sem .**plan**O comportamento torna-se ruído reativo; os objetivos se dissiparem.
  Não há**计划**, comportamento se transforma em ruído reactivo; objectivo

Os resultados de credibilidade dos avaliadores humanos são mais altos com os três; a queda de qualquer um produz uma regressão mensurável.

> O índice de credibilidade de um avaliador é o mais alto de todos os tempos; elimina qualquer degradação que produz uma quantidade de medição.

### A emergência do Dia dos Namorados

Uma agente, Isabella Rodriguez, é semeada com o objetivo de "quer organizar uma festa de São Valentim no Hobbs Café em 14 de fevereiro às 17h".

> Uma agente, Isabella Rodriguez, foi implantada como alvo de "pensar em 2 de fevereiro 14 de abril às 5 da tarde no Hobbs Cafe para organizar um festas de festa de amor".

1. O plano da Isabella inclui convidar pessoas.
   O plano de Isabella incluiu convidar pessoas.
2. Cada convite se torna uma observação no fluxo de memória do vizinho.
   Tradução do inglês para Chinês:
3. A reflexão daquele vizinho gera crenças: "Isabella está fazendo uma festa".
   O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é.
4. O plano do vizinho inclui "assistir à festa no dia 14 de fevereiro".
   Tradução do inglês para "Neighbourhood Plan"
5. Os vizinhos dizem aos outros vizinhos, o convite se espalha sem coordenação central.
   Tradução do inglês: vizinho diz ao outro vizinho.
6. Às 17h, 14 de fevereiro, vários agentes convergem no Hobbs Cafe.
   O filme foi lançado em outubro de 2015 e conta com o apoio de vários agentes.

Este é o surgimento no sentido técnico: o comportamento a nível do sistema (um partido) surgiu de interações locais (invitações bilaterais + planejamento individual) sem um orquestador central.

> É um fenómeno em sentido técnico: comportamento de nível sistémico (PSI) que surge de uma interacção local (PPSI) sem um organizador central (PPSI).

### Os modos de falha documentados

Park et al. documentam explícitamente:

> Park  et al. explicitamente recordou:

- **Spatial norm errors.**Os agentes entram em lojas fechadas. Os agentes tentam usar a mesma casa de banho individual. Os agentes comem em salas não destinadas a comer. O modelo não deduz as normas sociais-físicas apenas do ambiente.
  Tradução:**空间规范错误。**Agente 走进关闭的商店──Agente 试图使用同一个人浴室──Agente 在非用餐室用餐──模型不能仅从环境推断社会物理规范──
- **Memory overflow.**A simulação profunda faz com que o custo de recuperação da memória aumente. Remédio prático: compactação periódica da memória (resumo e poda) e decadência em entradas de baixa importância.
  Tradução:**记忆溢出。**A profundidade de simulação de operações levou ao aumento do custo de pesquisa de memória.
- **Reflection hallucination.**Reflexões podem inventar relações que não existem no fluxo de memória. Mitigation: incluir ids de memória fonte em instruções de reflexão e verificar no momento da recuperação.
  Tradução:**反思幻觉。**O reflexo pode desenvolver relações inexistentes no fluxo de memória.

Estes são modos de falha relevantes para a produção: qualquer simulação de agente 2026 herda-os.

> Estes são os modelos de falha relacionados à produção: qualquer agente de 2026 está preparado para herdar-nos.

### Regras de execução de três componentes

1. **Memory is append-only.**Nunca mude uma entrada de memória.
   Tradução:**记忆只追加。**永遠不修改記憶条目──更正是新条目── é uma história que não se pode mudar.
2. **Importance scores are cheap.**Liga para o Mestrado para avaliar a importância entre 1 e 10 no momento da escrita.
   Tradução:**重要性分数是廉价的。**写入时调用 LLM 评分 1-10──缓存分数──
3. **Retrieval is ranked, not filtered.**Top-k por pontuação combinada; não use filtros duros (que perdem contexto).
   Tradução:**检索是排序的，不是过滤的。**按综合分数取 top-k; não use duro过(会丢失上下文) ⋅
4. **Reflection runs periodically.**Trigger quando a soma da importância das memórias não processadas exceda um limiar (por exemplo, 150).
   Tradução:**反思定期运行。**Quando não processado a importância da memória total e superior ao valor (por exemplo, 150)
5. **Plans are revisable.**Quando uma nova observação contradiz um plano, regenerar apenas o segmento afetado, não o plano inteiro.
   Tradução:**计划可修订。**Quando uma nova observação e um plano se contradizem, apenas se reproduzem partes afetadas, não todo o plano.

### Agentes geradores para além de Smallville

A literatura de acompanhamento 2024-2026 estende a arquitetura:

> A literatura posterior para 2024-2026 amplia a estrutura:

- **Multi-agent social simulation for policy / market research.**Populações semelhantes a Smallville simulam o comportamento do usuário em resposta a características.
  Tradução:**用于政策/市场研究的多 Agent 社会模拟。**类似Smalville 的人群模拟用户对功能的响应──比A/B 测试更快;准确性有争议──
- **NPC AI for games.**Jogos de papel com agentes de Smallville produzem histórias emergentes em vez de missões guiadas.
  Tradução:**游戏 NPC AI。**Com o Agente de Smallville, o RPG é um romance que surge em vez de ser um roteiro.
- **Generative-agent evaluation benchmarks.**Em vez de precisão da tarefa, a métrica se torna credibilidade + coerência do comportamento em longas corridas.
  Tradução:**生成式 Agent 评估基准。**Em outras palavras, a taxa de precisão de tarefas, a taxa de credibilidade de operações de longo prazo, a taxa de continuidade de comportamento, a taxa de continuidade de operações de longo prazo, a taxa de continuidade de operações de longo prazo, a taxa de continuidade de operações de longo prazo e a taxa de continuidade de operações de longo prazo.

A arquitetura é a referência. As extensões trocam componentes (localização vetorial para memória, reflexão aumentada por recuperação, plano neurosimbólico), mas mantêm a estrutura de três partes.

> A estrutura é referência. • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • •

### Por que isso importa para a engenharia multi-agente

Smallville é a prova do conceito de que a emergência de multi-agentes é barata quando os componentes são corretos. A arquitetura foi agora replicada em modelos de código aberto (LLCs menores perdem credibilidade graciosamente, não fortemente). Qualquer sistema de produção que precisa **emergent social behavior**Qualquer sistema que precise.**tight task execution**utiliza os padrões de supervisor / papéis / primitivos de início nesta fase.

> Smallville é um conceito de teste, que mostra que quando o componente é correto, o multi-agent surge é barato.**涌现社会行为**Todos os sistemas de produção usam essa forma.**紧密任务执行**O sistema é usado neste estágio de primeiros supervisores/rôles/modelo de idioma original.

## Construí-lo.
```figure
a5-memory-reflection
```

## Construí-lo

`code/main.py`Implementa os três componentes em stdlib Python com políticas de agente scripted (sem LLM real).

- `MemoryStream` Registro de apêndice apenas com recuperação de recência/importância/relevância.
  Tradução:`MemoryStream` 带时效性/重要性/相关性检索的只额外日志──
- `reflect(stream)` reflexão escrita sobre memórias recentes de grande importância.
  Tradução:`reflect` Reflexião sobre a escrita de memórias de grande importância recente
- `plan(agent_state)` planos de nível diário e horário baseados nas crenças atuais.
  Tradução:`plan`  Baseado em dias e horas de planejamento de convicções atuais.
- O cenário: 5 agentes, o agente 1 começa com "a festa de lançamento às 17h".
  O agente 1 é o primeiro a ser convidado a participar da reunião de eventos.

- Correr .

```
python3 code/main.py
```

A produção esperada: rastreamento de tique por tique. No tique final, pelo menos 3 dos 5 agentes mostram o partido em seu plano, e convergem no local do partido. A única semente produziu a chegada coordenada sem nenhum orquestrador.

> 预期输出:逐步跟踪―― em último tempo, passo, passo, 5 agentes, pelo menos 3 mostraram festas no plano, eles se reuniram no local da festa― semente individual, em caso de não haver um organizador, gerou coordenação até à chegada―

## Usa-o. Usa-o.

`outputs/skill-simulation-designer.md`concebe uma simulação de agente gerador: número de agentes, esquema de memória, cadência de reflexão, horizonte de plano e métrica de avaliação.

> `outputs/skill-simulation-designer.md`design a generated Agent 模拟:Agente Número, Módulo de Memória, Frequência de Reflexo, Esquema de Planejamento e Indicadores de Avaliação

## Envia-o .

Regras para simulações de produção:

- **Memory is the database.**Escolha uma loja real (vector DB, Postgres) em escala.
  Tradução:**记忆是数据库。**Em escala selecionar o armazenamento real (~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **Log the retrieval trace.**Para cada ação, registra as memórias que o levaram.
  Tradução:**记录检索轨迹。**Para cada movimento, o registro impulsiona a sua memória superior.
- **Budget per-agent tokens.**Cada agente de recuperação + refletir + plano por tick é O(k) LLM chamadas. N agentes × T ticks × chamadas-por-tick pode enanimar o seu orçamento.
  Tradução:**预算每 Agent token。**Cada Agente Cada passo de tempo de revisão + reflexo +  plano é O(k) O segundo LLM 调用──N 个 Agente × T 个时间步 × 每时间步调用数可能让你的预算相形见──
- **Compact memory periodically.**Resumir e cortar as entradas de baixa importância.
  Tradução:**定期压缩记忆。**Resumo e modificação de menor importância Artigo¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬
- **Detect spatial / social norm violations**A arquitetura não os aprende.
  Tradução:**显式检测空间/社会规范违规。**As arquiteturas não as aprendem.

## Exercícios.

1. Corra .`code/main.py`Aumentar os agentes para 10 .
   Tradução: 运行`code/main.py`Confirmar 3 ou mais agentes 汇聚到派对── 将代理增加到10涌现还会发生吗?
2. Remova o passo de reflexão. Como é que o comportamento parece? Mapa para a descoberta de ablação no Park 2023.
   O que é que o comportamento parece?
3. Introduza um objetivo sementeado em competição ("Klaus quer dar uma palestra de pesquisa às 17h").
   Chinese: Introdução a um objetivo de semente de competição ("Klaus 想在下午 5 点做研究报告")
4. Adicione restrições espaciais: Hobbs Cafe pode conter no máximo 4 agentes. O maná de simulação transbordar graciosamente, ou atinge o padrão de falha de "banheiro de uma pessoa única"?
   O Hobbs Cafe, o máximo de 4 agentes, é capaz de lidar com a situação de "bairro de um só homem" ou não?
5. Leia Park et al. (arXiv:2304.03442) Seção 6 (experimentos de comportamento emergente). Identifique um comportamento não reprodutivel em sua miniatura. Que componente da arquitetura você precisaria melhorar?
   No entanto, o que é que você precisa de fazer para melhorar a estrutura?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Memory stream / 记忆流 | "The agent's diary" / "Agent 的日记" | Append-only log of observations, actions, reflections, plans. / 观察、行动、反思、计划的只追加日志。 |
| Recency / 时效性 | "How new is the memory" / "记忆有多新" | Exponential-decay score by age. / 按年龄的指数衰减分数。 |
| Importance / 重要性 | "How much does the agent care" / "Agent 有多在意" | Self-rated 1-10 at write time. Cached. / 写入时自评 1-10。已缓存。 |
| Relevance / 相关性 | "How related to the current query" / "与当前查询有多相关" | Cosine similarity (embedding-based). / 余弦相似度（基于嵌入）。 |
| Reflection / 反思 | "Higher-order belief" / "高阶信念" | Synthesis generated from recent memories, re-ingested as a new memory. / 从最近记忆生成的综合，作为新记忆重新摄入。 |
| Plan / 计划 | "Day/hour/action decomposition" / "日/小时/动作分解" | Top-down plan tree. Revisable when observations contradict. / 自顶向下计划树。观察矛盾时可修订。 |
| Smallville / 小镇 | "Park 2023's sandbox" / "Park 2023 的沙盒" | 25-agent simulation that produced the Valentine's Day emergence. / 25 个 Agent 的模拟，产生了情人节涌现。 |
| Believability / 可信度 | "The quality metric" / "质量指标" | Human-rater score for whether behavior seems like a plausible agent. / 人类评分者对行为是否像合理 Agent 的评分。 |

## Mais leitura 延伸阅读

- [Park et al. — Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) a arquitetura de referência
- [UIST '23 paper page](https://dl.acm.org/doi/10.1145/3586183.3606763) local de publicação
- [Smallville code release](https://github.com/joonspk-research/generative_agents) implementação de Python de referência
- [Hayes-Roth 1985 — A Blackboard Architecture for Control](https://www.sciencedirect.com/science/article/abs/pii/0004370285900639) arte anterior para agentes de memória estruturada
