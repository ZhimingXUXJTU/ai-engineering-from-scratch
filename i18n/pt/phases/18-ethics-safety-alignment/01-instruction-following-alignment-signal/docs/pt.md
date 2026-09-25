# Instruções- Seguindo como sinal de alinhamento.

> Todas as críticas posteriores à RLHF argumentam contra este gasoduto. Antes de estudar como a pressão de otimização distorce um proxy, tem de ver o proxy. A instruçãoGPT (Ouyang et al., 2022) definiu a arquitetura de referência: ajuste supervisionado em pares de instrução-resposta, um modelo de recompensa treinado em rankings de preferência em pares e o PPO contra o modelo de recompensa com uma penalidade KL para a política SFT. Um GPT InstructGPT 1.3B foi preferido a um GPT-3 175B. Esse único resultado é a razão pela qual cada laboratório de fronteira em 2026 ainda envia um pipeline de pós-treino em forma de RLHF.

> **【中文解读】**O InstrutorGPT ((Ouyang 等人, 2022) definiu a estrutura de referência de um conjunto de instruções: 1) supervisionar a regulação de micro-modulos (SFT) no treinamento de instruções-resposta; 2) o modelo de recompensa em treinamento de classificação de preferências; 3) o modelo de recompensa de PPO em relação ao modelo de resistência, com KL 惩罚保护;; 1.3B do InstrutorGPT superou o GPT-3 de 175B na avaliação de preferências humanas;; é por isso que cada laboratório da frente ainda está usando a linha de treinamento posterior em formato RLHF em 2026.

> **【拓展：RLHF → 现代 AI 对齐】**RLHF (RHF) é uma das principais técnicas de sucesso do ChatGPT.

> - Não .**【前置】**学本节前 請先掌握:Fase 10·06(SFT 监督微调)、Fase 10·07(RLHF)、Fase 10·08(DPO) 理解三阶段对齐管线的技术细节──本节是Fase 18 的开篇,从工程视角审视对齐后续 29节都基于此基础──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy three-stage pipeline) | **语言:** Python（标准库，玩具三阶段管线）
**Prerequisites:** Phase 10 · 06 (SFT), Phase 10 · 07 (RLHF), Phase 10 · 08 (DPO) | **前置知识:** Phase 10 · 06 (SFT), Phase 10 · 07 (RLHF), Phase 10 · 08 (DPO)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Objetivos de aprendizagem

- Nomear as três fases do gasoduto InstructGPT e a perda utilizada em cada uma delas.
  Tradução do inglês para inglês: InstructGPT 管线的三个阶段及每个阶段使用的损失函数――
- Explique por que um modelo com instruções de 1.3B venceu o GPT-3 bruto de 175B na avaliação das preferências humanas.
  Tradução do inglês para tradução do inglês: Explanation Why 1.3B Instruments Micro Models defeita o original 175B GPT-3
- Explique do que a penalidade KL na fase 3 está a proteger e por que a sua remoção entra em colapso com o comportamento de busca de modo.
  Tradução do inglês para tradução do inglês: Explanation of Third Stage KL 惩罚 protect is what, as quais são as consequências do seu deslocamento.
- Descreva o imposto de alinhamento e a mitigação do PPO-ptx utilizada contra o Ouyang et al.
  O que é o PPO-ptx 缓解方法?

## O problema é o problema da introdução

Os modelos de linguagem pré-treinados completam texto. Eles não respondem perguntas. Pergunte ao GPT-3 "escrever uma função Python que inverte uma lista" e você geralmente recebe outro prompt, porque a maior parte da distribuição de treinamento é texto web que continua com mais texto web. O modelo está fazendo seu trabalho  o trabalho é errado.

> 预训语言模型补充全文,而不是回答问题――让GPT-3 "Escrever uma função Python 函数 de lista de reversos", você muitas vezes recebe outra dica, porque a maioria das distribuições de treinamento continua a gerar mais páginas de texto de páginas de texto.

O proxy que cada laboratório sério usa para corrigir isso é a preferência humana. Duas conclusões vão para um avaliador; o avaliador escolhe o melhor; um modelo de recompensa aprende o avaliador.

> Cada laboratório rigoroso usado para corrigir este problema é o agente das preferências humanas. Dois complementos para os avaliadores; avaliadores escolher melhor; recompensar o modelo de aprendizagem avaliador. Então o ciclo RL irá mover a estratégia para o modelo de recompensas de alta avaliação.

## O conceito central.

### Fase 1: ajuste fino supervisionado (SFT)

Coletar pares de resposta rápida onde a resposta é o que um humano bem intencionado escreveria. Ouyang et al. usou 13k prompts de etiquetadores e a API OpenAI.

> 收集提示-响应, em que responder é o conteúdo escrito por um marcador de boa vontade.

O que o SFT lhe dá: o modelo agora responde às perguntas em vez de continuá-las. O que não lhe dá: qualquer sinal sobre qual resposta o avaliador prefere quando múltiplos são plausíveis.

> SFT  dá-te: modelo agora responde a problemas em vez de continuar completando-os. SFT não dá-te: quando mais respostas são razoáveis, o avaliador prefere qualquer sinal de qual resposta.

> **【中文解读】**SFT 阶段使模型从"补全文本"转向"回答问题",但无法提供关于多个合理答案中哪个更好的信号──RM 阶段使用布拉德利-特里 成对偏好损失 L_RM = -log sigmoid(r(x,y_w) - r(x,y_l)) 在标注者排列的补对上训奖励模型──RM normalmente inicializa o modelo SFT 模型并替代 LM 头为标量头,6B 就足指导 175B 模型──

### Fase 2: Modelo de recompensa (RM)

Para cada resposta rápida, mostre as conclusões K do modelo SFT. Um etiquetador as classifica. Treinar um modelo de recompensa que pontua qualquer par de resposta rápida para que, para pares onde `y_w`Era preferido .`y_l`- Não .

> Para cada sugestão, de SFT 模型采样 K 个补全――标标标对它们排序――训练一个奖励模型对任何提示-响应对打分,使对`y_w`优于                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `y_l`O que é que é?

```
L_RM = -log sigmoid(r(x, y_w) - r(x, y_l))
```

Esta é a perda de preferência em pares Bradley-Terry. O RM é geralmente iniciado a partir do modelo SFT com a cabeça LM substituída por uma cabeça escalar.

> É Bradley-Terry 成对偏好损失──RM geralmente é substituído por SFT 模型初始化,语言模型头换为标量头──

Os modelos de recompensa são pequenos: 6B foi suficiente para o 175B InstructGPT. Eles também são frágeis.

> O modelo de recompensa é muito pequeno: 6B é suficiente para orientar 175B do InstrumentoGPT.

> **【拓展：PPO 阶段 → RLHF 的核心工程】**A função-alvo da fase PPO 阶段 J(pi) = E[r(x,y) - beta * KL(pi do pi_SFT) maximizar o prêmio ao mesmo tempo mantendo a estratégia próxima ao SFT。 KL 系数 beta é a mais importante RLHF 超参数太低导致奖励黑客,太高则 SFT 上无改进。

### Fase 3: PPO com penalidade KL

Define o objectivo:

```
J(pi) = E_{x~D, y~pi(.|x)} [ r(x, y) ] - beta * KL(pi(.|x) || pi_SFT(.|x))
```

Maximizar com PPO.`pi`Sem ele, o optimizador encontra exemplos adversários  cordas que pontuação alta abaixo do RM porque o RM nunca os viu, não porque os seres humanos realmente preferem.

> Utilize PPO maximizar.`pi`Não se opõe a estratégias de SFT. Sem ele, otimizador encontra uma linha de caracteres de resistência em RM, porque RM nunca as viu, e não é a verdadeira preferência humana.

O coeficiente KL `beta`O que é que é o mais importante hiperparâmetro RLHF?

> - Não .`beta`É o mais importante RLHF 超参数──太低:奖励黑客──太高:相比 SFT 没有改进──

> **【中文解读】**O modelo RHF 后模型在人类偏好上更好但在标准基准上退步(SQuAD, HellaSwag, DROP) 上退步。Ouyang 等人称之为"对齐税"并使用PPO-ptx 修复将预训梯度混入RL 目标,使模型不忘从未获奖的下游任务──PPO-ptx 成为标准Anthropic、DeepMind和 Meta 都使用某种变体──

### Imposto de alinhamento

Após o RLHF, o modelo é preferido pelos humanos, mas regredem em benchmarks padrão (SQuAD, HellaSwag, DROP). Ouyang et al. chamam isso de imposto de alinhamento e o corrigem com PPO-ptx: misturam gradientes pré-treinamento no objetivo de RL para que o modelo não esqueça como fazer tarefas a jusante que nunca foi recompensado.

> RLHF 后,模型在人类偏好上更好但在标准基准 (SquAD, HellaSwag, DROP) 上退步。Ouyang 等人称之为"对齐税"并使用PPO-ptx 修复将预训梯度混入RL 目标,使模型不忘从未获奖的下游任务。

```
J_ptx(pi) = J(pi) + gamma * E_{x~D_pretrain} [ log pi(x) ]
```

O PPO-ptx tornou-se padrão. Anthropic, DeepMind e Meta todos usam alguma variante.

> PPO-ptx 成为标准──Antropic、DeepMind 和 Meta 都使用某种变体──

> **【拓展：1.3B vs 175B → 对齐独立于能力】**1.3B InstructGPT sobre a preferência do marcador cerca de 70% do tempo venceu 175B GPT-3。 a diferença na produção de fluxo oculto teste de dica é maior。 dois pontos principais: 1) o marcador é diferente do capacitar 175B tem mais capacidades, 1.3B tem mais marcadores, preferência do marcador é mais comum; 2) capacidade inferior é definida pelo modelo base você não pode RLHF um modelo base faz saber que ele nunca viu fatos.

### O resultado

Um 1.3B InstructGPT (SFT + RM + PPO-ptx) é preferido pelos etiquetadores sobre o 175B base GPT-3 cerca de 70% do tempo.

> 1.3B de instruçãoGPT(SFT + RM + PPO-ptx) em cerca de 70% do tempo é preferido pelo marcador superior a 175B base GPT-3― a diferença na produção de fluxo oculto teste de sugestões é maior― a partir deste número pode ser lido duas coisas:

1. O modelo 175B tinha mais capacidade; o modelo 1.3B tinha mais alinhamento; os etiquetadores preferiam o alinhado.
   O modelo 175B tem mais capacidade; 1.3B modelo tem mais capacidade; o marcador prefere o que tem mais capacidade.
2. O nível de capacidade é definido pelo modelo base.
   Não pode passar pelo RLHF 让基础模型知道它从未见过的事实──

> **【拓展：Phase 18 后续课程 → 每个都在攻击此管线】**Cada crítica do curso seguinte está em uma parte da linha de ataque: recompensa black客 (Lessão 2) fase de ataque (Lessão 2) fase de ataque (Lessão 2) fase de ataque (Lessão 3) fase de combinação (Lessão 2) fase 2 e 3, CAI (Lessão 5) substituição de marcadores humanos (Lessão 4) mostra marcadores é um sinal de preconceito, para fazer uma falsa figura (Lessão 9) estratégia de demonstração pode ser completamente contornada pela fase 3 (Lessão 3)

### Por que é este o ponto de referência para a Fase 18

Cada crítica nas aulas posteriores  hacking de recompensa (Lessão 2), DPO (Lessão 3), sicofania (Lessão 4), CAI (Lessão 5), agentes adormecedores (Lessão 7), alinhamento falsificação (Lessão 9)  argumenta contra alguma parte deste pipeline. Ataques de hacking de recompensa estágio 2. O DPO desmorona nos estágios 2 e 3. A CAI substitui o rotulador humano. A sícofancia mostra que o rotulador é um sinal tendencioso. A falsificação de alinhamento mostra que a política pode percorrer a fase 3 inteiramente. Não se pode seguir nenhuma dessas críticas sem o pipeline na cabeça primeiro.

> Cada crítica no curso seguinte  recompensa黑客(Lessão 2)、DPO(Lessão 3)、(Lessão 4)、CAI(Lessão 5)、潜伏 Agent(Lessão 7)、对齐伪装(Lessão 9)都在攻击此管线的某部分中──奖励黑客攻击第二阶段──DPO 合并第二和第三阶段──CAI 替换人类标志者──展示标志者是有偏见信号──对齐伪装展示策略可以完全绕过第三阶段──如果没有在脑中这个管线,就无法理解这些批评──

## Use-o com o framework implementado.
```figure
al-instruct-pipeline
```

## Usá-lo

`code/main.py`Simula as três etapas dos dados de preferência dos brinquedos. A "política" base é uma moeda tendenciosa sobre as ações {A, B, C}. Estação 1 SFT imita ações de rotulagem em 200 instruções. O estágio 2 corresponde a um modelo de recompensa Bradley-Terry de 500 rankings em pares. A fase 3 apresenta uma atualização simplificada do PPO com uma penalidade KL para a política de SFT. Você pode assistir ao aumento da recompensa, a divergência KL crescer, e a política de deriva  e você pode desligar o termo KL para ver o hacking de recompensa aparecer dentro de 50 passos de atualização.

> `code/main.py`Em dados de preferência de brinquedos simulação em três fases. Base "estratégia" é a ação {A, B, C} de um tipo de moeda.

O que ver:

Observação:

- Tráetoria de recompensa com `beta = 0.1`- Não .`beta = 0.0`- Não .
  Tradução:`beta = 0.1`- Não .`beta = 0.0`时的奖励轨迹──
- O programa de formação é um dos principais programas de formação.
  Tradução do inglês: training step step in KL(pi)
- Distribuição final de ações em comparação com a preferência do etiquetador.
  Tradução em chinês:

## Envia-o . Produto .

Esta lição produz`outputs/skill-instructgpt-explainer.md`. Tendo em conta uma descrição do gasoduto RLHF ou um resumo de papel, identifica qual das três fases está a ser modificada, qual a perda a utilizar em cada etapa e se existe uma penalidade KL ou reguladora equivalente.

> 本课产 出 `outputs/skill-instructgpt-explainer.md` Dado RLHF 管线描述或论文摘要, identifica qual das três fases foi modificada  cada fase utiliza quais funções de perda, bem como se existe um KL 惩罚或等效正则化器──

## Exercícios.

1. Corra .`code/main.py`- Set .`beta = 0.0`E informar a distribuição de ação após 200 etapas de PPO. Explique o comportamento de busca de modo num parágrafo.
   Tradução: 运行`code/main.py`- Configuração.`beta = 0.0`E relatar 200 步 PPO 后的动作分布──用一段话解释模式崩行为──

2. Modifique o modelo de recompensa para ter um preconceito de +0,5 para a ação B (um bug de recompensa simulado).`beta = 0.1`A penalidade KL impede que a política explore o preconceito?`beta`torna-se visível a exploração?
   Tradução do inglês: Modificar o modelo de recompensa faz o movimento B`beta = 0.1`运行 PPO──KL 惩罚能否阻止策略利用偏置? 在什么?`beta`O valor da utilização torna-se visível?

3. Leia Ouyang et al. (arXiv:2203.02155) Figura 1. Reproduzir a curva de preferência de etiquetador executando PPO por 1, 5, 20, 100 passos e medindo a preferência em relação ao modelo SFT.
   Tradução do português:阅读 Ouyang 等人(arXiv:2203.02155)图 1──通过运行PPO 1、5、20、100 步并测量对SFT 模型的偏好来复现标注者偏好曲线──

4. A secção 4.3 do jornal relata que um 1.3B InstructGPT supera o 175B GPT-3 cerca de 70% do tempo.
   O relatório 1.3B InstructGPT venceu 175B GPT-3 em cerca de 70% do tempo. Por que essa proporção em pontuação de produção oculta é maior do que a própria pontuação do marcador?

5. Substituir a perda de PPO por DPO (Fase 10 · 08) com base nos mesmos dados de preferência. Comparar a derivação final da política (KL a SFT) e a recompensa final. Qual método deriva mais longe com a recompensa correspondente?
   Tradução do inglês: In the same preference data on using DPO (Pase 10 · 08) substituir PPO 损失 (Pase 10 · 08) substituir PPO 损失 (Pase 10 · 08)

## Termos-chave .

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| SFT | "instruction tuning" / "指令微调" | Stage 1: cross-entropy fine-tune on prompt-response pairs / 阶段 1：在提示-响应对上交叉熵微调 |
| Reward model | "the RM" / "奖励模型" | Scalar regressor over (prompt, response) trained with Bradley-Terry on pairwise labels / 用 Bradley-Terry 在成对标签上训练的标量回归器 |
| Bradley-Terry | "pairwise preference loss" / "成对偏好损失" | -log sigmoid(r_w - r_l); reduces pairwise ranking to binary classification / 将成对排序简化为二分类 |
| KL penalty | "the regularizer" / "正则化器" | `beta * KL(pi \|\| pi_SFT)` — keeps the RL policy near the SFT anchor / 保持 RL 策略接近 SFT 锚点 |
| PPO-ptx | "PPO with pretraining mix" / "带预训练混合的 PPO" | Adds a fraction of pre-training log-likelihood to the PPO objective to offset the alignment tax / 将部分预训练对数似然加入 PPO 目标以抵消对齐税 |
| Alignment tax | "the RLHF regression" / "RLHF 退步" | Post-RLHF drop on standard benchmarks that RLHF did not target / RLHF 后在未针对的标准基准上的性能下降 |
| Labeler preference | "the ground truth" / "地面真实" | Sample of human rankings; the RM is a statistical proxy for this, not for "human values" / 人类排序的样本；RM 是其统计代理，而非"人类价值观" |

## Mais leitura 延伸阅读

- [Ouyang et al. — Training language models to follow instructions with human feedback (arXiv:2203.02155)](https://arxiv.org/abs/2203.02155) o papel InstructGPT, base para cada oleoduto RLHF que se seguiu
  Tradução do português:Ouyang 等人InstructGPT 论文,此后每个RLHF 管线的基础
- [Stiennon et al. — Learning to summarize from human feedback (arXiv:2009.01325)](https://arxiv.org/abs/2009.01325) o antecessor do RLHF para resumo
  O que é que é o "Relance" do livro?
- [Christiano et al. — Deep reinforcement learning from human preferences (arXiv:1706.03741)](https://arxiv.org/abs/1706.03741) a formulação original de RL baseada em preferências
  Chinese:Christiano 等人                                                                                                                                                                                                                                                            
- [Bai et al. — Training a Helpful and Harmless Assistant with RLHF (arXiv:2204.05862)](https://arxiv.org/abs/2204.05862) Extensão da HH do gasoduto InstructGPT pela Anthropic
  Tradução do português: Bai 等人Antropic对 InstructGPT 管线的 HH 扩展
