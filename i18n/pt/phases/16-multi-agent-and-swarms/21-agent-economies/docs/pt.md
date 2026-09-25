# Economias de agentes, incentivos de tokens, reputação.

> Os agentes autônomos de longo horizonte (a curva de trabalho de 1 a 8 horas da METR) precisam de um agente económico.**5-layer stack**é: **DePIN**(computação física) → **Identity**(DIDs do W3C + capital de reputação) → **Cognition**(RAG + MCP) → **Settlement**(abstração da conta) → **Governance**As redes de incentivos aos agentes de produção incluem:**Bittensor**(Sub-rede de TAO recompensam modelos específicos de tarefas), **Fetch.ai / ASI Alliance**(Token ASI-1 Mini LLM + FET), e **Gonka**Trabalho acadêmico: A AAMAS 2025 utiliza a LaMAS descentralizada **Shapley-value credit attribution**Para recompensar justamente os agentes que contribuem; a Google Research propõe "Design Mechanism for large language models" **token auctions**Esta lição cria um mercado de agentes mínimo, aplica atribuição de crédito de valor Shapley a um pipeline de agentes múltiplos e realiza um leilão de tokens de segundo preço para que a máquina da teoria do jogo aterrisse concretamente.

> **【中文解读】**Esta secção apresenta o mecanismo de negociação de recursos, fixação de preços e mercado no sistema de agentes.

> **【拓展：agent economies→具体应用】**Agente  economia de análise  mecanismo de distribuição e incentivo de recursos no sistema  mecanismo de incentivo   sistema   sistema                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 16 (Negotiation and Bargaining), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 16（协商与讨价还价），Phase 16 · 09（并行群体网络）

> - Não .**【前置】**學本节前請先掌握:Fase 16·16(协商) 、Fase 16·09(Swarm) 、 mecanismo design基础(Shapley 值、拍卖理论) ⋅Agen 经济 = 多 Agent 系统的市场层。
> - Não .**【类比】**Agente 經濟 = "AI 自由市場"──5 層:DePIN(算力) + 身份(DID+声誉) + 认知(RAG+MCP) + 结算(账户抽象) + 治理(Agentic DAO)。Bittensor 子网奖励专门模型,Fetch.ai usou ASI-1 Mini + FET token,Gonka usou transformador PoW 把算力导向生产任务――学术:Shapley 给多 Agent 公平分、二价 拍卖防操纵――
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problema Introdução

Os sistemas de agentes múltiplos tornam-se complicados quando os agentes produzem valor em conjunto, mas precisam ser recompensados individualmente. Mecanismos clássicos  divisão igual, último contribuinte-tomou-todos  são injustos ou jogáveis. A recompensa baseada em coalizão através dos valores de Shapley é justa por construção, mas cara para calcular. A literatura 2025-2026 empurra aproximações úteis: amostragem de Shapley, leilões de agregação monótona e reputação na cadeia que se acumula a partir de contribuições confirmadas.

> Os sistemas de agência em conjunto geram valor, mas precisam de recompensas individuais, tornando-se complexos. O mecanismo clássico é que os últimos contribuintes são totalmente injustos ou manipulaveis. Os recompensas de valor Shapley baseados em alianças são justas na construção, mas calculadas e caras. As publicações de 2025-2026 promovem uma aproximação útil:

Além da atribuição de crédito, o campo se tornou para agentes econômicos reais: a Bittensor TAO recompensa a computação de mineração para ajustar os modelos específicos da sub-rede, Fetch.ai/ASI recompensa o uso de ASI-1 Mini LLM com tokens FET, a Gonka realoca a prova de trabalho de transformador para tarefas produtivas de IA. Agentes que transacionam de forma autônoma existem hoje; a questão é como alinhar os incentivos.

> 超越信用归因, o domínio se tornou um verdadeiro agente económico:Bittensor TAO 奖励挖掘计算来微调子网特定模型,Fetch.ai/ASI usando token FET 奖励 ASI-1 Mini LLM 使用,Gonka vai transformar 工作量证明重新分配到生产性 AI 任务;;

Esta lição trata as economias de agentes como uma família de problemas específicos  atribuição de crédito, design de mecanismo e reputação  e constrói cada uma com a matemática mínima para que as ideias fiquem.

> Esta aula irá considerar o Agente Econômico como um problema específico de atribuição de crédito, design de mecanismos e reputação e construir cada um com a menor quantidade de matemática, para que o conceito seja realmente compreendido.

## Conceptos básicos

### A pilha de 5 camadas de agente-economia

1. **DePIN (physical compute).**Infraestrutura descentralizada que aluga GPU, armazenamento, largura de banda, sub-rede de Bittensor, Render Network, Akash, não específica para um agente, os agentes usam.
   Tradução:**DePIN（物理计算）。**租 GPU、存储、带宽的去中心化基础设施──Bittensor 子网、Render Network、Akash──非代理 专用;Agent 使用它──
2. **Identity.**Os identificadores descentralizados (DIDs) do W3C dão a cada agente uma identificação duradoura independente de qualquer plataforma. A reputação acumula-se no DID. O protocolo de rede de agentes (ANP) usa o DID como camada de descoberta.
   Tradução:**身份。**W3C 去中心化标识符(DID) dá a cada agente um ID permanente independente da plataforma;;
3. **Cognition.**O ciclo de raciocínio do agente: LLM + RAG + MCP.
   Tradução:**认知。**O ciclo de avaliação do agente: LLM + RAG + MCP.
4. **Settlement.**A abstracção de contas (ERC-4337) permite aos agentes pagar o gás dos seus próprios saldos sem manterem a ETH.
   Tradução:**结算。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
5. **Governance.**DAO agentes: estruturas de governança onde os seres humanos *e* agentes votam sobre alterações de protocolo, com o poder de voto ligado à reputação.
   Tradução:**治理。**Agente DAO: humanos* e* Agente para o acordo de mudança de estrutura de governo, voto e reputação vinculada.

Nem todos os sistemas de produção usam todos os cinco. Bittensor usa 1, 2, parcialmente 3, parcialmente 4, nenhum dos 5.

### Bittensor, Fetch.ai, Gonka  o que corre

**Bittensor (TAO).**As sub-redes são tarefas especializadas (modelagem de linguagem, geração de imagem, previsão). Os mineiros enviam resultados de modelos. Os validadores classificam-nos; a pontuação ponderada pela participação distribui as recompensas da TAO. Cada sub-red tem sua própria avaliação. A lição econômica: pagar pela qualidade de saída específica da tarefa, não computação usada.

**Fetch.ai / ASI Alliance.**O ASI-1 Mini LLM é executado na rede Fetch.ai; os usuários pagam tokens FET para inferir. A narrativa de agentes como pares é mais forte aqui: um agente no Fetch pode chamar outro para uma tarefa e pagar em FET.

**Gonka.**Transformador prova de trabalho: o "trabalho" é passes adiantadas de um transformador. Os mineiros ganham executando tarefas de inferência que conhecem saídas corretas (a partir de dados de treinamento). PoW produtivo de recursos em vez de PoW baseado em hash.

Todos os três são de nível de produção a partir de abril de 2026. A distribuição de pagamentos difere. Bittensor recompensa qualidade em relação a validadores de subnet; Fetch recompensa utilidade medida por usuários pagantes; Gonka recompensa trabalho de inferência verificável.

### Atribuição de crédito de valor Shapley

Três agentes colaboram numa tarefa.

Valor Shapley: a atribuição de crédito única que satisfaz quatro axiomas (eficácia, simetria, linearidade, nulo).`i`- Não .

```
shapley(i) = (1/N!) * sum over all orderings O of (v(S_i_O ∪ {i}) - v(S_i_O))
```

onde`S_i_O`é o conjunto de agentes antes `i`em ordem`O`. Na prática: enumerar todas as permutativas, registar a contribuição marginal de cada agente em cada permutância, média.

Para N=3 agentes, há 6 permutações. Para N=10, 3.6M , então na prática você amostra ordens em vez de enumerar.

### Leilão de segunda ordem para agregação

O Google Research ("Design Mechanism for large language models") propõe leilões de tokens de segundo preço para a agregação de resultados de LLM. Configuração: N agentes propõem cada um uma conclusão; cada um tem um valor particular para ser selecionado. O leilão escolhe a proposta de maior valor e paga o *segundo valor mais elevado* Sob a agregação monótona (o valor depende de qual proposta é escolhida, não de quantos foram ofertados), isto é verdadeiro  agentes oferecem o seu verdadeiro valor.

Por que isso importa para os sistemas de LLM: pode terceirizar tarefas de conclusão para vários agentes com preços diferentes; o leilão escolhe o melhor + paga justamente, e os agentes não têm incentivo para relatar erroneamente.

### Capitais de reputação

Uma pontuação de reputação vinculada ao DID acumula-se a partir de contribuições confirmadas.

```
rep(i, t+1) = alpha * rep(i, t) + (1 - alpha) * contribution_quality(i, t)
```

Com fator de decomposição`alpha`Próximo a 1. Repútua:

- É barato para ler para decisões de roteamento ("enviar tarefas difíceis para agentes de alta repetição").
- É caro de forjar (acumula ao longo do tempo, ligado ao DID).
- Pode ser cortado: contribuições que não conseguem ser verificadas subtraem.

### AAMAS 2025 LAMAS descentralizada

A proposta LaMAS (AAMAS 2025) combina: identidade DID, atribuição de crédito de valor Shapley e um mecanismo de leilão simples.

### Onde a economia se desmorona

- **Price oracle manipulation.**Se a função de crédito for jogada, os agentes vão jogar.
- **Sybil attacks.**Um operador faz a venda de N agentes falsos para aumentar a sua própria contribuição.
- **Verification cost.**A atribuição de crédito é apenas tão justa quanto o verificador.Se a verificação é barata (pequena LLM), pode ser jogada; se cara (panel humano), o sistema não se escala.
- **Regulatory overhang.**As economias de agentes se cruzam com a regulamentação financeira. Bittensor, Fetch e Gonka operam todas em áreas cinzentas legais em algumas jurisdições a partir de 2026.

### Quando as economias de agentes fazem sentido

- **Open networks with heterogeneous operators.**Nenhuma equipa controla todos os agentes.
- **Verifiable outputs.**Sem verificação, a atribuição de crédito é uma suposição.
- **Long-horizon workflows.**As tarefas de um só tiro não se beneficiam da acumulação de reputação.
- **Tokenized payments are legally viable**- Na sua jurisdição.

Em sistemas corporativos fechados, a economia dá lugar a uma alocação mais simples (os gerentes atribuem trabalho, as métricas são internas).

## Construí-lo.
```figure
swarm-auction
```

## Construí-lo

`code/main.py`Implementos:

- `shapley(value_fn, agents)` cálculo exato de Shapley por enumeração para N pequeno.
- `second_price_auction(bids)`- mecanismo verdadeiro; o vencedor paga o segundo maior.
- `Reputation` Repútua de DID com decadência exponencial e corte.
- Demo 1: três agentes colaboram, o Shapley atribui o crédito exato.
- Demo 2: cinco agentes oferecem uma oportunidade de tarefa; segundo preço de leilão escolhe o vencedor + pagamento.
- Demo 3: 100 rodadas de atribuição de tarefas a agentes com repetição heterogênea; rotação ponderada por repetição bate aleatório.

- Correr .

```
python3 code/main.py
```

Resultados esperados: valores Shapley para cada agente; resultado do leilão mostrando equilíbrio de oferta verdadeira; roteamento ponderado por repetição mostrando ganho de qualidade de 10-20% sobre aleatório após aquecimento.

## Usa-o. Usa-o.

`outputs/skill-economy-designer.md`concebe uma economia de agente mínima: escolha da camada de identidade, mecanismo de atribuição de crédito, mecanismo de pagamento, regra da reputação.

## Envia-o .

- Dirigir uma economia de agentes em 2026:

- **Start with reputation, not tokens.**A reputação é barata de implementar e valiosa sozinha; os tokens acrescentam complexidade jurídica e econômica.
  Tradução:**从声誉开始，不是 token。** a reputação de conseguir um preço barato e de valor exclusivo;  aumente a complexidade jurídica e económica
- **Verify before you reward.**Nunca distribuir crédito sem uma fase de verificação independente.
  Tradução:**先验证再奖励。**Não há nenhum tipo de crédito.
- **Shapley-sample, not Shapley-exact.**Ensaio de 100 a 1000 ordens; a enumeração exata não é escalada.
  Tradução:**Shapley 采样，而非 Shapley 精确。**采样 100-1000 个排序;精确枚举不可扩展──
- **Cap decay factor and floor reputation.**A decomposição ilimitada esvaziar os contribuintes legítimos; a decomposição muito lenta recompensa agentes ultrapassados de alta repetição.
  Tradução:**限制衰减因子和最低声誉。**无界衰减抹抹合法贡献者; 太慢的衰减奖励过时的高声誉代理──
- **Audit mechanisms adversarially.**Exerça cenários de equipe vermelha antes de abrir a rede.
  Tradução:**对抗性审计机制。**O sistema tem um problema, você quer encontrar uma falha, não um atacante.

## Exercícios.

1. Corra .`code/main.py`Confirmar a soma dos valores de Shapley para o valor total (axioma da eficiência). Mudar a função de valor; as atribuições de Shapley mudam na direção esperada?
2. Implementar Shapley *sampling* (Monte Carlo sobre K ordens). Como K afeta a precisão da aproximação?
3. Implementar uma etapa de formação de coalizão antes do leilão: os agentes podem se fundir em equipes e fazer ofertas como uma unidade.
4. Leia o post de design de mecanismos da Google Research. Identifique uma suposição que, se violada, quebra a veracidade. Como é que esse modo de falha parece em um ambiente de LLM?
5. Leia o artigo LaMAS descentralizado AAMAS 2025. Implemente o passo Shapley sobre 10 agentes em uma tarefa sintética. Quanto tempo leva o cálculo exato?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| DePIN / 去中心化物理基础设施 | "Decentralized physical infrastructure" / "去中心化物理基础设施" | Token-incentivized compute/storage/bandwidth. Bittensor, Akash, Render. / Token 激励的计算/存储/带宽。Bittensor、Akash、Render。 |
| DID / 去中心化标识符 | "Decentralized identifier" / "去中心化标识符" | W3C spec for portable IDs. Agent reputation binds to DID, not to a platform. / W3C 便携 ID 规范。Agent 声誉绑定到 DID，而非平台。 |
| ERC-4337 / 账户抽象 | "Account abstraction" / "账户抽象" | Contract accounts that can sponsor gas, enabling agent payments. / 可以赞助 gas 的合约账户，使 Agent 支付成为可能。 |
| Shapley value / Shapley 值 | "Fair credit attribution" / "公平信用归因" | Unique allocation satisfying efficiency, symmetry, linearity, null. / 满足效率、对称、线性、零贡献者的唯一分配。 |
| Second-price auction / 二价拍卖 | "Vickrey auction" / "Vickrey 拍卖" | Truthful mechanism: winner pays second-highest bid. Monotone aggregation compatible. / 诚实机制：获胜者支付第二高出价。兼容单调聚合。 |
| Reputation capital / 声誉资本 | "Accumulated quality score" / "累积质量分数" | DID-bound score from confirmed contributions; decays over time. / DID 绑定的来自确认贡献的分数；随时间衰减。 |
| Agentic DAO / Agent DAO | "Agents + humans govern" / "Agent + 人类治理" | DAO with agent voters as first-class, voting power tied to reputation. / Agent 投票者作为一等公民的 DAO，投票权与声誉绑定。 |
| TAO / FET / GPU credits / Token 面额 | "Token denominations" / "Token 面额" | Bittensor TAO, Fetch.ai FET, various DePIN tokens. / Bittensor TAO、Fetch.ai FET、各种 DePIN token。 |

## Mais leitura 延伸阅读

- [The Agent Economy](https://arxiv.org/abs/2602.14219) Enquesta de 2026 sobre a pilha de 5 camadas de economia de agentes
- [Google Research — Mechanism design for large language models](https://research.google/blog/mechanism-design-for-large-language-models/) Leilões simbólicas com agregação monótona
- [AAMAS 2025 — decentralized LaMAS](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2896.pdf) Atribuição de crédito de valor Shapley
- [Bittensor TAO documentation](https://docs.bittensor.com/) Estrutura da sub-rede e distribuição de recompensas
- [Fetch.ai / ASI Alliance](https://fetch.ai/) ASI-1 Mini LLM e FET token
- [W3C Decentralized Identifiers (DIDs) spec](https://www.w3.org/TR/did-core/) Fundação da identidade
