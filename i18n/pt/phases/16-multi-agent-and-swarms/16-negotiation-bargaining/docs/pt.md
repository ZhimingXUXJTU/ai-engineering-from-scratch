# Negociação e Negociação Negociação

> Os agentes negociam recursos, preços, atribuições de tarefas e termos. O conjunto de referência de 2026 é claro: NegotiationArena (arXiv:2402.05863) mostra que os LLM podem melhorar os saldos ~20% através da manipulação de persona ("desespero"); "Medir as habilidades de negociação" (arXiv:2402.15813) mostra que o comprador é mais difícil do que o vendedor e a escala não ajuda  seus **OG-Narrator**(Generador de Ofertas Deterministas + Narrador de LLM) empurrou a taxa de negócios de 26,67% para 88,88%; a Grande Concurso de Negociação Autônoma (arXiv:2503.06416) realizou cerca de 180 mil negociações e descobriu que**chain-of-thought-concealing**Bhattacharya et al. 2025 em Harvard Negotiation Project metrics classificou Llama-3 mais eficaz, Claude-3 agressivo, GPT-4 mais justo. Esta lição implementa o Protocolo de Contrato Net (o ancestral da FIPA, lição 02), funsiona um comprador/vendedor de estilo LLM, realiza uma decomposição de estilo OG-Narrador e mede como a taxa de negócios muda com cada escolha estrutural.

> **【中文解读】**Esta secção apresenta estratégias de negociação na distribuição de recursos e tarefas de vários agentes.

> **【拓展：negotiation bargaining→具体应用】**协商和讨价还价是多代理 资源分配的核心机制――三种协商策略:(1) 合作型Agente 追求整体利益最大化;(2) 竞争型Agente 追求自身利益最大化;(3) 混合型兼顾个体和整体──Em economia de agente, as negociações geralmente são realizadas através de acordos de proposta-resposta estruturados, semelhantes aos acordos de rede de contratos(Contract Net Protocol) ⋅


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 02 (FIPA-ACL Heritage), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 02（FIPA-ACL 遗产），Phase 16 · 09（并行群体网络）

> - Não .**【前置】**O processo de negociação de contratos de contratos de investimento (FIPA) foi concluído em 31 de janeiro de 2015 e foi concluído em 31 de janeiro de 2015.
> - Não .**【类比】**Agente 协商 = "二手市场砍价"──LLM 通过 persona 操纵(装穷)能多 20%;隐藏推理过程的Agente 赢对手看不到你的底线──OG-Narrator 把协商拆为"确定性提议生成"+"LLM 叙述",deal rate 26%→89%──模型差异:Llama-3 最有效、Claude-3 强势、GPT-4公平 最选即模型选风格──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problema Introdução

Os dois agentes precisam concordar em um preço. Deixados para si mesmos com indicações de linguagem pura, os LLM 2024-2026 fecham negócios a taxas surpreendentemente baixas (~ 27% em negócios com parâmetros apertados em arXiv:2402.15813).

> 两个代理 需要就价格达成一致. 在纯语言提示下,2024-2026年 LLM 成交率惊人地低. 在 arXiv:2402.15813 的紧密参数化议价中约27%) 规模化不能解决: GPT-4 não é melhor na estrutura de preços do que GPT-3.5 ; é apenas melhor no preço de议价*

O problema principal é que os LLM misturam dois trabalhos  decidindo a oferta e narrando a oferta. OG-Narrator separou estes: um gerador de oferta determinista calcula os movimentos numéricos; o LLM apenas narra.

>  fundamental problema é LLM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

O protocolo de contrato (FIPA, 1996; Smith, 1980) é o mecanismo de referência do mercado de tarefas.

> Isso reflete um clássico mecanismo de comunicação e comunicação. O processo de desenvolvimento de um sistema de gestão de dados e de dados é um processo de desenvolvimento de um sistema de gestão de dados e de dados.

## Conceptos básicos

### Contrato Net, num parágrafo

O Protocolo de Contratação Net de Smith de 1980: a **manager**Transmissão de televisão **call for proposals (cfp)**- O que é ?**bidders**Responder com **propose**mensagens que contêm as suas ofertas; o gerente escolhe um vencedor e envia **accept-proposal**para o vencedor e **reject-proposal**O vencedor faz o trabalho.**refuse**A FIPA codificou isto como:`fipa-contract-net`Protocolo de interação.

> O acordo de contrato de 1980 de Smith:**管理者**广播**提案请求（cfp）**O artigo 2.o**投标人**回复 contendo seu preço**提案**消息; administrator选择获胜者并向获胜者发送**接受提案**, para os candidatos**拒绝提案**❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖**拒绝**(投标人拒绝提案) ― A FIPA 将其编码为`fipa-contract-net`交互协议── Não é o que se passa?

### Por que o OG-Narrador ganha

"Messuring Negotiating Abilities of Language Models" (arXiv:2402.15813) observou que:

> "Meter linguagem modelo de议价能力" (arXiv:2402.15813) observa:

- As LLM frequentemente infringem as regras de negociação (oferta a preços sem sentido, ignorar o ZOPA do outro lado).
  O LLM  frequentemente viola as regras de preços (→ "preço de oferta sem sentido, ignorando o ZOPA do outro")
- Eles ancoram mal (aceitam ofertas iniciais ruins; contra-oferta em quantidades simbólicas em vez de estratégicas).
  O preço da primeira rodada é muito ruim, mas não é estratégico.
- Os modelos maiores tornam a linguagem mais plausível com erros estratégicos semelhantes.
  Tradução do inglês para o inglês: "Living in the same language" (em inglês: "Living in the same language") é uma linguagem mais racional, mas há erros estratégicos semelhantes.

A decomposição do OG-Narrador:

```
           ┌──────────────────┐        ┌──────────────────┐
  state  → │ offer generator  │ price → │  LLM narrator    │ → message
           │  (deterministic) │        │  (writes the     │
           │                  │        │   human-style    │
           └──────────────────┘        │   accompaniment) │
                                       └──────────────────┘
```

O gerador de ofertas é uma estratégia de negociação clássica: um modelo de negociação de Rubinstein, uma estratégia Zeuthen, ou um simples tit-for-tat sobre o preço.

A taxa de negócios aumenta porque:
- Os preços permanecem na zona de negociação.
- Ancores são estratégicos, não emocionais.
- O LLM faz o que é bom: escrever.

> 成交率 Jump up:
> - 价格保持在议价区间内──
> - 点是战略性的,而非情绪化的.
> - LLM fazer o que é bom: escrever.

### NegociaçãoConstatos da Arena

O arXiv:2402.05863 fornece o índice de referência canônico.

> ArXiv:2402.05863  forneceu normas básicas.

- As LLM podem melhorar os salários ~20% adotando personas ("Estou desesperado por vender isso até sexta-feira")  Manipulação de persona é uma tática real.
  O LLM pode aumentar os lucros em cerca de 20% através da adoção de personalidades.
- Os agentes justos/cooperativos são explorados por agentes adversários; a defesa exige uma contraposta explícita.
  Tradução em inglês: fair/合作的代理被对抗性代理利用; defense needs manifestant reversal attitude──
- Os paramentos simétricos convergem a resultados inegais em cerca de 40% dos cenários de referência.
  O que é o resultado de um acordo de acordo com o acordo de acordo?

Não é "os LLM são maus negociadores". É "os LLM negociam muito como os humanos, incluindo as partes exploráveis".

> Não é "o LLM é um mau negociador" mas sim "o modo de negociação do LLM é muito humano, incluindo partes utilizáveis".

### O ocultamento da cadeia de pensamentos

A Grande Concurso de Negociação Autônoma (arXiv:2503.06416) realizou cerca de 180 mil negociações em muitas estratégias de LLM. Os vencedores ocultaram seu raciocínio de seus colegas:

> A grande competição de negociação autónoma ([[arXiv:2503.06416) ] foi realizada cerca de 180.000 vezes em várias estratégias de LLM.

- Se um agente imprimir "Eu só vou para o$75; my reservation price is $70" num raspadinho visível ao público, o adversário lê-o.
  Se o agente vai "Eu só vou sair"$75；我的保留价是 $70" impresso em um esboço de público, para leitura em mãos.
- Os vencedores compute estratégia em privado; o canal de saída contém apenas a oferta e a narrativa mínima necessária.
  Tradução em chinês: 获胜者私下计算策略;输出通道只包含报价和最低限度的叙述──

Este é um eco de 2026 da teoria clássica do jogo (Aumann 1976 sobre racionalidade e informação): revelar a sua avaliação privada custos de pagamento. LLM não intuir isso e felizmente digitar suas reservas em rastros de raciocínio que tornam-se visíveis para a contraparte.

> É um clássico blog post (Aumann 1976  Sobre a Raciologia e Informação) em 2026 Reacção: revelar a perda de lucros da avaliação privada.

Engenharia takeaway: separar o contexto privado-scratchpad do contexto de mensagem pública. Não opcional.

> 工程要点:将私人草稿本上下文与公开消息上下文分离── Isso não é opcional──

### Bhattacharya et al. 2025  classificações de modelos

Em relação às métricas do Projeto de Negociação de Harvard (negociação em princípio, respeito pela BATNA, reciprocidade de interesses):

> Em Havard谈判项目目标标标上:

- **Llama-3**foi mais eficaz em negociações (taxa de transacção + pagamento).
  Tradução:**Llama-3**Em termos de transacções de acordo, mais eficaz:
- **Claude-3**O Conselho Europeu de Ministros dos Negócios Estrangeiros (CEC) defendeu que a Comissão não pode, em qualquer caso, fazer qualquer intervenção para que o Conselho possa tomar medidas para evitar que a situação seja prejudicada.
  Tradução:**Claude-3**É o negociador mais agressivo.
- **GPT-4**foi a mais justa (menos variação de pagamento entre as paradas).
  Tradução:**GPT-4**O resultado da análise é o mínimo de diferença entre os resultados.

Este é um snapshot de 2025. O ponto não é qual modelo vence em abril de 2026  é que diferentes modelos base têm estilos de negociação persistentes. Ensembles heterogêneos (Lessão 15) incluem isso como uma fonte de diversidade.

> Este é o rápido lançamento de 2025: o foco não é em qual modelo vencer em 2026 mas em um modelo base diferente que tenha um estilo de negociação duradouro.

### A atribuição de tarefas através de contrato líquido + MLL

A reutilização moderna de Contract Net para LLM multi-agente:

> 合同网在现代 LLM 多 Agent 中中重用:

1. O agente gerente decompõe uma tarefa em unidades.
   Tradução do inglês: Manager Agent 将任务分解为单元――
2. Transmissões `cfp`Com descrição da tarefa aos agentes dos trabalhadores.
   Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês`cfp`- Não.
3. Cada trabalhador retorna uma oferta: `(price, eta, confidence)`onde o preço pode ser tokens, unidades de cálculo ou dólares.
   Tradução do inglês para tradução inglesa:`(price, eta, confidence)`, o preço pode ser token ̇ calcular unidades ou dólares ̇
4. O gerente seleciona os vencedores (singular ou múltiplos, dependendo da tarefa) e os prémios.
   Tradução do inglês para "manager" (em inglês: administrator)
5. Os trabalhadores recusados são livres para fazer propostas para outras tarefas.
   Tradução do inglês:被拒的工作者可以竞标其他任务.

Esta escala ultrapassa bem 100 trabalhadores porque a coordenação é de transmissão e resposta, não de chat sincrono.

> Isso pode ser muito bem expandido para mais de 100 trabalhadores, pois coordenação é um modo de comunicação e resposta, e não um modo de conversação.

### Negociação interativa entre as partes interessadas da MLL

NeurIPS 2024 (https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf) introduz jogos multipartícios marcáveis com **secret scores**E ...**minimum-acceptance thresholds**. Cada parte interessada tem serviços públicos privados; o LLM deve inferir-los a partir de mensagens. Esta é a generalização da negociação bipartidária para a formação de coalizões de partidos N. Relevante para mercados de tarefas de produção com capacidades trabalhadoras heterogêneas.

> O NeurIPS 2024  introduziu**秘密分数**和**最低接受阈值**O LLM tem que ser deduzido da informação. É uma promoção de duas partes que se baseia na formação de uma união.

### A regra narrativa contra o mecanismo

Em todas as referências de negociação de 2024 a 2026, a regra de engenharia consistente é:

> Deixe o LLM narrar, não deixe o LLM calcular a oferta.

> 让LLM 叙述──不要让LLM 计算报价──

Se a oferta precisar ser um número (preço, ETA, quantidade), gerá-la deterministicamente a partir do estado de negociação e faça com que o LLM produza a enquadramento.

> Se a oferta for necessária de uma estrutura de proposta, se a oferta for necessária de uma estrutura de tarefas, se a oferta for necessária de uma estrutura de tarefas, se a oferta for necessária de uma estrutura de tarefas, se a oferta for necessária de uma estrutura de tarefas, se a oferta for necessária de uma estrutura de tarefas, se a oferta for necessária de uma estrutura de tarefas, se a oferta for necessária de uma estrutura de trabalho, se a oferta for necessária de uma estrutura de trabalho, se a oferta for necessária de uma estrutura de trabalho, se a oferta for necessária de uma estrutura de trabalho, se a oferta for necessária de uma estrutura de trabalho, se a oferta for necessária de uma estrutura de trabalho, se a oferta for necessária de uma estrutura de trabalho, se a oferta for necessária de uma estrutura de trabalho, se a oferta for necessária de uma estrutura de trabalho, mas se a oferta for necessária de uma avaliação de qualidade, se a proposta for necessária para a realização de uma avaliação de um acordo com o modelo e o conjunto de um grupo.

## Construí-lo.
```figure
a5-og-narrator
```

## Construí-lo

`code/main.py`Implementos:

- `ContractNetManager`- Não .`ContractNetTask`- Não .`Bid` gerente + licitantes, emissões de televisão, recolha de propostas, concessão.
  Tradução:`ContractNetManager`- Não.`ContractNetTask`- Não.`Bid` 管理者 + 投标人,广播 cfp,收集提案,授标──
- `og_narrator_bargain(state, rng)` Comprador OG-Narrador: concessão determinista de estilo Zeuthen em direção ao ponto médio.
  Tradução:`og_narrator_bargain` OG-Narrador 买方:确定性 Zeuthen 风格向中间点让步──
- `seller_response(state, rng)` política determinista de contra-oferta do vendedor (a verdade estrutural para ambos os estilos).
  Tradução:`seller_response` 确定性卖方回价策略 ( 确定性卖方回价策略)
- `naive_llm_bargain(state, rng)` simula uma negociação de LLM: escolhe preços com alta variação, muitas vezes fora da ZOPA.
  Tradução:`naive_llm_bargain` 模拟全 LLM 议价者:以高方差选价,经常超出 ZOPA──
- Medida: taxa de transacção em mais de 1000 ensaios, com preços de reserva frescos recolhidos em amostra por ensaio.
  Tradução do inglês: : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : :   :                                                                                     

- Correr .

```
python3 code/main.py
```

Resultado esperado: taxa de negócio naívo-LLM ~65-75%; taxa de negócio OG-Narrador ~85-95%; a diferença de 15-25 pontos é a vantagem estrutural de decompor a geração de ofertas da narração.

> 预期输出:朴素 LLM 成交率约65-75%;OG-Narrator 成交率约85-95%;15-25 个百分点差距是将报价生成与叙述解的结构优势──加上一个三个投标者和一个任务的合同网任务市场分配示例──

## Usa-o. Usa-o.

`outputs/skill-bargainer-designer.md`Desenha um protocolo de negociação: quem gera ofertas (determinista ou LLM), quem narra, como os scratchpads privados se separam das mensagens públicas e como a taxa de negócios é monitorada.

> `outputs/skill-bargainer-designer.md`设计一个议价协议:谁生成报价 (definitividade ou MLL),谁叙述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述, etc.

## Envia-o .

Lista de verificação de negociações de produção:

- **Separate scratchpad.**O Estado privado nunca chega ao contexto da contraparte.
  Tradução:**分离草稿本。**O estado privado nunca chega ao adversário.
- **Deterministic offer generation.**Preços, quantidades, datas de chegada: calcular, não pedir.
  Tradução:**确定性报价生成。**价格、数量、ETA:计算, não fazer propinas。
- **Validate all incoming offers**Rejeitar ofertas fora do ZOPA na fronteira do protocolo.
  Tradução:**验证所有传入报价**De acordo com o modelo, o acordo foi rejeitado pela ZOPA.
- **Bound rounds.**3-5 tiros no máximo; escala para mediador em um impasse.
  Tradução:**限制轮次。**Máximo 3-5 rotas; morto-locado quando elevado ao moderador.
- **Measure deal rate and payoff variance**Uma taxa de negócios em queda é um sintoma, muitas vezes uma deriva rápida ou um ataque do lado da contraparte.
  Tradução:**持续测量成交率和收益方差。**A taxa de convergência baixa é um sintoma, geralmente por causa de movimentos de tendência ou ataques de cara a cara.
- **Log all rejected proposals**Para os gestores da Rede de Contratos, os licitadores perdedores precisam entender o porquê.
  Tradução:**记录所有被拒绝的提案**及确定性理由── para os gestores de rede de contratos, os candidatos a concessão de contratos precisam entender as razões──

## Exercícios.

1. Corra .`code/main.py`Confirme que o OG-Narrador supera o LLM na taxa de negócios.
   Tradução: 运行`code/main.py`Confirmar OG-Narrador em taxa de conclusão superior a LLM simples.
2. Implementação **persona-based payoff improvement**O comprador adota um "desesperado para comprar esta semana" personalidade apenas na narrativa, oferece gerador inalterado.
   Tradução do português: implementar**基于人格的收益改进**(arXiv:2402.05863)  comprador apenas em narração adotando "本周急需购" personalidade,报价生成器不变──成交率或收益有变吗?
3. Implementar a cadeia de pensamento **concealment**O que acontece se você o vazar acidentalmente (simulação trocando os canais)?
   Tradução do inglês:**隐藏**O que acontece se não tivermos a intenção de divulgar o seu esboço?
4. Extenda o contrato líquido para o leilão de N-adjudicador com preço de reserva. Quando todas as ofertas excederem a reserva, como o gerente decide entre o preço mais baixo e a mais alta qualidade?
   Quando todas as propostas ultrapassam o preço de retenção, como é que o gerente escolhe entre o preço mínimo e a qualidade máxima?
5. Leia Bhattacharya et al. 2025 sobre as métricas do Projeto de Negociação de Harvard. Implemente dois negociadores com estilos diferentes (agressivo vs justo).
   Tradução do inglês para o inglês: Bhattacharya  et al. Essays on the 2025 Year About Harvard Negotiation Project ⋅ realizando dois diferentes estilos de negociação ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                                                        

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Contract Net / 合同网 | "Task market" / "任务市场" | Smith 1980, FIPA 1996. cfp + propose + accept/reject. The canonical task-market. / Smith 1980, FIPA 1996。cfp + propose + accept/reject。规范的任务市场。 |
| ZOPA / 可能协议区 | "Zone of possible agreement" / "可能协议区域" | Overlap between buyer's max and seller's min. Offers outside it cannot close. / 买方最大值和卖方最小值的重叠。超出此范围的报价无法成交。 |
| BATNA / 最佳替代方案 | "Best alternative to a negotiated agreement" / "谈判协议的最佳替代方案" | Your fallback if this deal fails. Sets your reservation price. / 如果交易失败的后备方案。设定你的保留价。 |
| OG-Narrator / OG-叙述者 | "Offer generator + narrator" / "报价生成器 + 叙述者" | Decomposition: deterministic offer, LLM narration. / 分解：确定性报价，LLM 叙述。 |
| Zeuthen strategy / Zeuthen 策略 | "Risk-minimizing concession" / "风险最小化让步" | Classical offer-generator that concedes based on risk limits. / 基于风险限制让步的经典报价生成器。 |
| Rubinstein bargaining / Rubinstein 议价 | "Alternating-offer equilibrium" / "交替报价均衡" | Game-theoretic model for infinite-horizon bargaining with discounting. / 带折现的无限期议价博弈论模型。 |
| CoT concealment / CoT 隐藏 | "Hide your reasoning" / "隐藏推理" | Winners in arXiv:2503.06416 kept private scratchpads; public channel shows offer only. / arXiv:2503.06416 的获胜者保持私人草稿本；公开通道只显示报价。 |
| Persona manipulation / 人格操纵 | "Emotional posturing" / "情绪姿态" | arXiv:2402.05863: ~20% payoff gain from desperation/urgency personas. / arXiv:2402.05863：绝望/紧迫人格带来约 20% 的收益增益。 |

## Mais leitura 延伸阅读

- [NegotiationArena](https://arxiv.org/abs/2402.05863) o índice de referência; constatações de manipulação e exploração de pessoas
- [Measuring Bargaining Abilities of Language Models](https://arxiv.org/abs/2402.15813) OG-Narrador e o resultado de comprador-mais duro do que vendedor
- [Large-Scale Autonomous Negotiation Competition](https://arxiv.org/abs/2503.06416) ~ 180 mil negociações; a ocultação da cadeia de pensamentos ganha
- [LLM-Stakeholders Interactive Negotiation (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf) Jogos multi-partidários marcadores com utilitários secretos
- [Smith 1980 — The Contract Net Protocol](https://ieeexplore.ieee.org/document/1675516) o mecanismo clássico, IEEE Transações em Computadores
