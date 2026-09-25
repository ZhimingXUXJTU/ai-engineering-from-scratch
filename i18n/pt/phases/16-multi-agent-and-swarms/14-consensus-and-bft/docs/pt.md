# Consenso e Tolerança Bizantina à Falha dos Agentes

> Sistemas distribuídos clássicos BFT atende aos LLM estocásticos. Em 2025-2026, surgiram três direcções de investigação: **CP-WBFT**(arXiv:2511.10400) pesa cada voto por uma investigação de confiança; **DecentLLMs**(arXiv:2507.14928) vai sem líder com propostas paralelas de trabalhadores e agregação geométrica-mediana; **WBFT**(arXiv:2505.05103) combina votação ponderada com Clustering de Estrutura Hierárquica para dividir os nós Core e Edge. O resultado empírico honesto de "Can AI Agents Agree?" (arXiv:2603.01213) é que mesmo o acordo escalar é frágil hoje  um único agente enganador pode comprometer uma mistura de agentes. A BFT é necessária, mas não suficiente. Esta lição constrói um protocolo BFT mínimo, injeta três ataques específicos de agentes (mentir bizantino, conformidade sicófante, monocultura de erro correlacionado) e mede como cada variante de consenso lida.

> **【中文解读】**Esta secção apresenta como chegar a um acordo em caso de falha ou mau comportamento de vários agentes.

> **【拓展：consensus and bft→具体应用】**拜占庭容错 (BFT) 在多 Agent 系统中的应用:当部分 Agent 可能故障或被攻击时,如何确保系统整体正确? 经典 BFT 算法(PBFT) 需要 3f+1 个节点容忍 f 个故障节点──在 LLM Agent 上下文中,'故障'可以是幻觉、被注入或拒执行──在实践中使用多数投票作为简化 BFT──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 13（共享内存）

> - Não .**【前置】**Há um período de tempo em que o agente de LLM é "falta" = "iluminação", "injectado"", rejeição de execução"".
> - Não .**【类比】**BFT = "jurígio vota mas deve se proteger de dentro"。 clássico BFT =  tolerancia 1/3 节点说谎(PBFT 3f+1);LLM 版 = 加权投票(按置信度) + 几何中位数聚合 + 层级聚类──三类攻击:拜占庭说谎、附和、相关错误(同一基础模型 全错)。 conclusão:BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problema Introdução

Você tem N LLM agentes cada produzindo uma resposta. Eles discordam. A maioria dos votos escolhe o errado porque dois agentes são correlacionados (o mesmo modelo base, os mesmos dados de treinamento, os mesmos modos de falha). Um terceiro agente acontece que está errado de uma maneira nova , então a maioria é uma maioria falsa.

> Você tem N 个 LLM Agente, cada um produz uma resposta. Eles não concordam. A maioria dos votos escolheu a resposta errada, porque dois Agentes são relacionados.

Agora adicione um agente enganador: ele está de propósito. ou um agente sícofântico: ele concorda com quem falou pela última vez.`f < n/3`A realidade de 2026 é que os nós LLM são estocásticos mesmo quando honestos, correlacionados entre os modelos e influenciados pelas saídas uns dos outros.

> Agora, junte-se a um agente fraudulento: ele intencionalmente mente. Ou um agente fraudulento: ele concorda com o último orador.`f < n/3`并且行为任意──2026年现实是,LLM 节点即使诚实也随机,跨模型相关,并受影响彼此输出──你不能将它们视为独立的伯努利选民──

O BFT clássico (PBFT, 1999) não está errado  é incompleto. Ele lida com o deslocamento arbitrário de bits. Não lida com "três agentes honestos compartilham uma alucinação porque compartilham dados de treinamento". Esta lição se baseia na fundação e camadas do PBFT em três adaptações 2025-2026.

> 经典 BFT(PBFT, 1999)并非错它是不完整的──它处理任意位翻转──但它不处理"三个诚实代理因为共享训练数据产生相同幻觉"──本课程来自PBFT的基础,叠加三个2025-2026年改进──

## Conceptos básicos

### O que o BFT clássico lhe dá

A Tolerância Prática à Falha Bizantina (Castro & Liskov, OSDI 1999) tolera `f < n/3`Nódos bizantinos. O protocolo tem três fases (preparação, preparação, compromisso) e duas primitivas (mensagens assinadas, certificados de quórum).`n >= 3f + 1`nós honestos ou maliciosos.

> 实用拜占庭容错(Castro & Liskov, OSDI 1999) tolerância `f < n/3`个拜占庭节点──协议有三个阶段 (预备备、准备、提交) 和两个原语 (签名消息、仲裁证书)`n >= 3f + 1`个诚意或恶意节点之间就单一价值达成一致.

As garantias são fortes, mas assumem:

> Estas garantias são fortes, mas suponham que:

1. **Independent faults.**Os bizantinos não se coordenam.
   Tradução:**独立故障。**O que é que se passa?
2. **Honest nodes are truly honest.**A corretão das saídas honestas não é um problema; o protocolo só alinha o desacordo.
   Tradução:**诚实节点真正诚实。**诚实输出正确性 não é um problema; o acordo apenas trata de diferenças.
3. **The question has a ground-truth answer.**O consenso sobre um facto errado continua a ser consenso.
   Tradução:**问题有标准答案。**O consenso sobre os erros ainda é o consenso.

Os agentes da LLM violam os três. Dois agentes que executam o mesmo modelo base compartilham falhas. Um LLM "honesto" ainda alucina. E em questões ambíguas, a "verdade" é o que os agentes decidem.

> O agente LLM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

### Os três ataques específicos da LLM

**Byzantine lie.**Um agente dá uma resposta deliberadamente errada.`f < n/3`- Não .

> **拜占庭撒谎。**Um agente 输出故意错误的答案―― se `f < n/3`, BFT clássico pode ser tratado.

**Sycophantic conformity.**Um agente lê as respostas dos outros antes de votar e alinha-se com quem falou mais tarde. Não é malicioso, mas correlaciona-se com a voz mais alta.

> **谄媚从众。**Um Agente, antes de votar, lê a resposta do outro Agente, e mantém a concordância com o último orador. Não é mau intenção, mas é relacionado com a maior voz.

**Correlated-error monoculture.**Três agentes compartilham um modelo base. Eles alucinam a mesma resposta errada. A maioria está errada.

> **相关错误单一文化。**Três agentes compartilham um modelo básico. Eles geram o mesmo erro. A maioria é errada.

### As respostas de 2025 a 2026

**CP-WBFT**(arXiv:2511.10400)  BFT ponderado com prova de confiança. Cada eleitor anexa uma sonda de confiança à sua resposta (uma probabilidade auto-relatada ou a previsão de um modelo de calibração separado).

> **CP-WBFT**(arXiv:2511.10400) confiança de pesquisa aumentou o poder de BFT── cada eleitor acrescentou uma confiança de pesquisa para sua resposta(probabilidade de auto-relatamento, ou previsão de modelo de calibração individual)── o poder de voto foi reduzido com a confiança── o relatório apresentou uma melhoria do BFT de +85,71% no gráfico completo── em relação às medidas de alívio da população ― de um agente público  tendem a ter uma confiança menor nas posições que propõem voluntariamente)──

**DecentLLMs**(arXiv:2507.14928)  Leaderless. Agentes de trabalhadores propõem em paralelo, agentes de avaliadores pontuações propostas, resposta final é a média geométrica das posições pontuações.`f < n/2`. Mitigation for: mentira bizantina e erros correlacionados (mediana geométrica é robusta a valores fora do plano e atrai para o aglomerado denso, não para a média baseada em modelos).

> **DecentLLMs**(arXiv:2507.14928)                                                                                                                                                                                                                                                          `f < n/2`时稳健.                                                                                                                                                                                                                                                             

**WBFT**(arXiv:2505.05103)  BFT ponderado com Clustering de Estrutura Hierárquica. Pesos de voto são atribuídos pela qualidade da resposta mais uma pontuação de confiança aprendida da história. Agentes de cluster em Core e Edge; Agentes Core devem alcançar consenso primeiro, Agentes Edge seguem. Mitigation para: escalabilidade (Core consensus é pequeno e rápido) e parcialmente para monocultura (Core pode ser escolhido para a diversidade).

> **WBFT**(arXiv:2505.05103) 带层次结构聚类的加权 BFT;; 投票权由响应质量加上从历史中学习的信任分数分配;; 将代理聚类为核心和边缘; 核心代理 必须先达成共识,边缘代理 跟随;; 针对可扩展性的缓解措施 (Centro共识小而快) 和部分针对单一文化的缓解 (Centro pode escolher a diversidade) ;;

### Empirical: "Podem Agentes de IA concordar?" (arXiv:2603.01213)

O papel mede o acordo escalar (agentes LLM que concordam sobre um único valor numérico) em vários modelos de fronteira.

> O artigo mediu a consonância de quantidades em vários modelos de vanguarda (LLM Agent em um único valor alcançado) e o resultado foi perturbador:

- Mesmo sem adversários, os agentes da LLM discordam sobre questões escalares em taxas acima de 30% em muitos índices de referência.
  Mesmo sem contra-mão, o agente LLM em muitos testes de base de referência a desacordo sobre questões de volume de produto excede 30%[1].
- Um único agente que adota uma personalidade enganosa pode tirar o consenso de mistura de agentes 40+ pontos percentuais da linha de base honesta.
  Tradução do inglês: Emprego de um único agente de fraude pode ser misturado Agente Compreensão de base de verdade 40 个百分点以上.
- As taxas de desacordo correlacionam com a diversidade de modelos  conjuntos heterogêneos discordam mais do que os homogêneos (bom: erros não correlacionados) mas também deslocam-se mais lentamente (mau: tempo mais longo para o acordo).
  Chinese:不一致率与模型多样性相关异构集成比同构集成不一致更多(好:不相关错误),但漂移更慢(坏:更长的一致达成时间) ⋅

A conclusão: a BFT fornece uma máquina para alinhar as saídas, mas não diz se a saída alinhada é correta.

> 结论:BFT 提供出口对齐的机制,但不告诉你对齐的出口是否正确──需要结合验证(Fase 16 · 08 角色专业化) 多样性(Fase 16 · 15 辩论变体) 和评估 Agent(Fase 16 · 24 基准测试)──

### O protocolo central, despojado

Um mínimo de BFT para agentes LLM:

```
1. task arrives; each agent i produces answer a_i
2. each agent attaches confidence probe c_i in [0, 1]
3. aggregator collects (a_i, c_i) from all n agents
4. aggregator groups by semantic cluster (equivalent answers)
5. aggregator computes weight for each cluster C:
     w(C) = sum_{i in C} c_i
6. winner = cluster with max weight, if max > threshold * sum(c_i)
   else: retry or escalate
7. minority clusters logged with provenance for post-hoc audit
```

A etapa de agrupamento semântico é a torcida específica do LLM. Duas respostas "o estudo relata 4,2%" e "melhora de 4,2%" são o mesmo agrupamento. Uma verificação ingênua de igualdade de cordas perderia isso.

> 语义聚类步骤是LLM's peculiar innovation. 两答案"研究报告 4.2%"和"4.2%的改进"是同一个. ── 简单的字符相等检查会遗漏这一点. ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──                                                                        

### Apontação do limiar

O `threshold`O parâmetro decide quando aceitar e quando tentar novamente. Muito baixo: aceita majoritades fracas. Muito alto: nunca aceita nada. Intervalo empírico: 0,5-0,67 para `n=5-7`Agentes, mais altos para os menores `n`Abaixo de um limiar, escala para um humano ou para um conjunto de agentes diferentes.

> `threshold`参数决定何时接受、何时重试──太低:接受弱多数──太高:永远不接受任何东西──`n=5-7`个 Agente 时为0.5-0.67,较小的 `n`时更高. 低于值. 时更高. 低于值. 时更高. 低于值. 时更高. 低于值. 时更高. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值. 低于值.

### Quando o consenso não ajuda

- **Ambiguous questions.**Se a questão não tem verdade, o consenso é uma opinião.
  Tradução:**模糊问题。**Se o problema não tem resposta padrão, o consenso é opinião.
- **Compound questions.**"Escreva código e explica-o"  duas respostas.
  Tradução:**复合问题。**"编写代码并解释"两个答案──分别独立投票──
- **Adversarial multi-round.**Se os agentes podem observar rodadas anteriores e imitar (debate Du 2023), eles começam a concordar entre si independentemente da verdade.
  Tradução:**对抗性多轮。**Se o agente pode observar os primeiros ciclos e simulando os debates, eles não podem concordar uns com os outros.

## Construí-lo.
```figure
swarm-consensus-wave
```

## Construí-lo

`code/main.py`Implementos:

- `AgentVoter` uma política escrita com (resposta, confiança).
  Tradução:`AgentVoter` 带有(答案,置信度) do livro estratégia.
- `MajorityVote` Pluralidade clássica.
  Tradução:`MajorityVote` 经典多数投票──
- `CPWBFT` votação ponderada pela confiança com agrupamento semântico.
  Tradução:`CPWBFT` 带语义聚类的信度加权投票──
- `DecentLLMs` Agregação geométrica-mediana das propostas pontuações.
  Tradução:`DecentLLMs` 评分 提案上的几何中位数聚聚合──
- `Scenario` executa cada agregador sob três padrões de ataque.
  Tradução:`Scenario` Operar em três modos de ataque em cada aglomerador.

Padrões de ataque implementados:

> 实现的攻击模式:

1. `byzantine`Um agente está a mentir com grande confiança.
   Tradução:`byzantine`Um agente de confiança mentiroso.
2. `sycophancy`Um agente copia a primeira resposta que vê, com a mesma confiança.
   Tradução:`sycophancy`Um agente replica a primeira resposta que vê, com certeza.
3. `monoculture`A resposta é errada (erro correlacionado) e os três agentes compartilham uma resposta errada com confiança moderada.
   Tradução:`monoculture`Três agentes: 共享一个错误答案 (),置信度中等.

- Correr .

```
python3 code/main.py
```

Output esperado: uma tabela de (ataque, agregador) -> resposta final, com a resposta correta destacada. Pluralidade falha no caso da monocultura. A ponderação de confiança do CPWBFT atinge a sicofania.

> 预期输出:一张(攻击,聚合器) -> Formação do último respondido, resposta correcta, alta lucidez mostrando―― maioria dos votos falhou em casos de cultura única― CPPWBFT aumentou a sua confiança e o seu poder de aliviar── Quando a cultura única não chega a metade da hora, o número de decentes LLM tendem para a sinceridade──

## Usa-o. Usa-o.

`outputs/skill-consensus-designer.md`Desenha um protocolo de consenso para um conjunto de agentes múltiplos: método de agrupamento, ponderação, limiar e política de escalação para rodadas de sub limiar.

> `outputs/skill-consensus-designer.md`Para vários agentes 集合 design consensus protocolos: metodologia de agregação, peso, valor, bem como estratégias de valorização de turnos de valor inferior.

## Envia-o .

Antes de enviar qualquer mecanismo de consenso:

- **Attack-test with at least the three patterns**O seu protocolo deve falhar de forma previsível, não silenciosamente.
  Tradução:**至少用上述三种模式进行攻击测试。**O teu acordo deve ser um fracasso previsível, e não um fracasso silencioso.
- **Log every minority cluster**Os grupos minoritários são o sistema de alerta precoce para erros correlacionados.
  Tradução:**记录每个少数派簇**O sistema de prevenção inicial é um sistema de prevenção inicial.
- **Enforce bounded rounds.**Não "continuem a debater até um acordo" que recompensa a cegoação.
  Tradução:**强制限制轮次。**Não me deixe debater até que eu concorde com o que ele fez.
- **Separate agreement from correctness.**A saída de consenso vai para um verificador; o verificador é independente do conjunto.
  Tradução:**分离一致性和正确性。**共识输出交给验证器;验证器 independente do conjunto.
- **Monitor the agreement rate.**Um aumento acentuado significa preconceito de conformidade; uma queda acentuada significa deriva do modelo.
  Tradução:**监控一致率。**A alta acentuada significa desvio de população; a baixa acentuada significa deslocamento do modelo.

## Exercícios.

1. Corra .`code/main.py`- Confirmar a pluralidade falha no ataque das monoculturas, mas o CPWBFT mitigou parcialmente quando a confiança das monoculturas é inferior a 0,7.
   Tradução: 运行`code/main.py`Confirmar a maioria dos votos falhou no ataque à cultura única, mas quando a confiança à cultura única foi inferior a 0,7 horas, a CPWBFT aliviou o problema.
2. Adicione um quarto padrão de ataque:**silent abstention** um agente recusa-se a responder ("não sei"). Como deve cada agregador tratar as abstenções?
   Tradução do inglês:**静默弃权** 一个代理 拒绝回答("我不知道")―. Como cada aglomerador deve lidar com o abandono?
3. Esquievar o agrupamento semântico da canonização de cadeia para a semelhança de inserção (utilizar qualquer modelo de inserção de código aberto). O que acontece com o ataque de sicofancia?
   Chinese Translation:将语义聚类从字符串规范化换为嵌入相似度 () 攻击会发生什么?
4. Leia CP-WBFT (arXiv:2511.10400). Implementar a etapa de calibração de sonda de confiança (um modelo de calibração separado verifica a auto-relatada confiança de cada agente).
   Tradução do inglês para o português:PDF-BBFT (en)
5. Leia "Podem Agentes de IA concordar?" (arXiv:2603.01213). Reproduzir um experimento simplificado de acordo escalar: três agentes, uma pergunta escalar, o prompt de pessoa enganadora.
   中文翻译:阅读"AI Agente 能达成一致吗?"(arXiv:2603.01213)。复现一个简化标量一致性实验:三个 Agent,一个标量问题,欺骗人格提示──CPWBFT或DecentLLMs 能捕获吗?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| BFT / 拜占庭容错 | "Byzantine fault tolerance" / "拜占庭容错" | Castro-Liskov 1999 protocol for consensus with `f < n/3` arbitrary faults. / Castro-Liskov 1999 协议，容忍 `f < n/3` 个任意故障节点的共识。 |
| Byzantine / 拜占庭 | "Any bad behavior" / "任何不良行为" | A node that can lie, drop messages, fail silently — anything but crash safely. / 可以撒谎、丢弃消息、静默失败的节点——除了安全崩溃外的任何行为。 |
| Confidence probe / 置信度探测 | "How sure are you?" / "你有多确定？" | Self-reported or calibrator-predicted probability attached to a vote. / 附加在投票上的自报或校准器预测的概率。 |
| Semantic clustering / 语义聚类 | "Same answer, different words" / "相同答案，不同措辞" | Grouping equivalent answers before counting votes. / 在计票前将等价答案分组。 |
| Geometric median / 几何中位数 | "Robust center" / "稳健中心" | The point minimizing sum of distances to sample points. Robust to outliers, unlike the mean. / 最小化到样本点距离之和的点。对异常值稳健，与均值不同。 |
| Monoculture / 单一文化 | "Same model, same failures" / "相同模型，相同失败" | Correlated errors when agents share training data or base model. / Agent 共享训练数据或基础模型时的相关错误。 |
| Sycophantic conformity / 谄媚从众 | "Agreeing with the loud voice" / "附和最大声的声音" | An agent's vote biases toward whoever spoke first/loudest. / Agent 的投票偏向最先/最大声发言的人。 |
| Core/Edge / 核心/边缘 | "Hierarchical BFT" / "层次化 BFT" | WBFT split: small Core consensus first, Edge nodes follow. Bounds latency. / WBFT 分割：小核心先达成共识，边缘节点跟随。限制延迟。 |

## Mais leitura 延伸阅读

- [Castro & Liskov — Practical Byzantine Fault Tolerance (OSDI 1999)](https://pmg.csail.mit.edu/papers/osdi99.pdf) a fundação
- [CP-WBFT — Confidence-Probe Weighted BFT](https://arxiv.org/abs/2511.10400) Peso de votos por confiança
- [DecentLLMs — leaderless multi-agent consensus](https://arxiv.org/abs/2507.14928) Agregação geométrica-mediana
- [WBFT — Weighted BFT with Hierarchical Structure Clustering](https://arxiv.org/abs/2505.05103) Divisão Core/Edge para latência limitada
- [Can AI Agents Agree?](https://arxiv.org/abs/2603.01213) Fragilidade dos acordos escalares e ataque de pessoa enganosa
