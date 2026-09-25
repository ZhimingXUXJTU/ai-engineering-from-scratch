# Teoria da mente e coordenação emergente

> Li et al. (arXiv:2310.10701) mostraram que os agentes de LLM numa exposição de jogo de texto cooperativa **emergent high-order Theory of Mind**(ToM)  raciocínio sobre o que outro agente acredita sobre as crenças de um terceiro agente  mas falha no planejamento de longo horizonte devido ao gerenciamento de contexto e alucinação. Riedl (arXiv:2510.05174) mediu sinergia de ordem superior em uma população e descobriu que **only**A condição de ToM-prompt produz diferenciação ligada à identidade e complementaridade orientada para os objetivos; as LLM de baixa capacidade apresentam apenas uma emergência falsa. Isto é, a emergência da coordenação é imediatamente condicional e depende do modelo, não gratuita. Esta lição implementa um agente minimalista consciente de TOM, executa uma tarefa cooperativa com e sem o Instrução de TOM, e mede o delta de coordenação em relação ao protocolo Riedl 2025.

> **【中文解读】**Esta secção apresenta o mecanismo de coordenação da teoria do espírito Agente compreensão e previsão de outros agentes 意图的协调机制──

> **【拓展：theory of mind coordination→具体应用】**A teoria do espírito é a capacidade de compreender e prever o estado mental de outras pessoas. Em vários sistemas, o agente com teoria do espírito pode coordinar melhor o que ele sabe que o outro agente sabe o que quer que vai fazer. Pesquisas de 2025-2026 mostram que o plano de outro agente pode aumentar significativamente a eficiência de coordenação, mas também aumentou os custos de cálculo.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 17 (Generative Agents) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 17（生成式 Agent）

> - Não .**【前置】**學本节前请先掌握:Fase 16·07(辩论) 、Fase 16·17(生成式 Agent) 、认知科学 概念思想理论──ToM = Agente 推理"其他 Agent 在想什么"──
> - Não .**【类比】**ToM = "Agente de companheiros de inteligência"──无 ToM Agent = 自言自言;有 ToM Agent = 站在对方角度思考" ele acha que eu sei disso? 高阶 ToM = 嵌套推理?
**Time:** ~75 minutes | **时间:** ~75 分钟

## Problema Introdução

A coordenação multi-agente geralmente parece mágica: os agentes dividem o trabalho, antecipam-se uns aos outros, evitam a redundância. Geralmente, esta "emergência" é um artefato da engenharia de prompt  alguém disse aos agentes para "coordenar".

> Do Agente  coordenação geralmente parece muito estranho: Agente divide-se, prejudia-se mutuamente, evita o reduto. Geralmente, essa "emergência" é um produto do projecto de informação.

A conclusão de Riedl de 2025 é mais rigorosa: sob condições controladas, a coordenação só surge quando os agentes são convidados a raciocinar sobre **other agents' minds**(ToM). Sem o comando de ToM, mesmo modelos fortes mostram padrões de coordenação que não sobrevivem aos controles estatísticos.

> O REDEL 2025 é mais rigoroso: sob condições de controlo, coordenação apenas no Agente é sugerido**其他 Agent 的心理**(ToM) 才涌现――没有ToM 提示,即使强模型也显示出统计控制下不存在的协调模式―― isto é importante para a produção: a função de "多代理协调" da equipa de distribuição depende de提示且脆弱――

Esta lição trata o ToM como uma capacidade específica (razão sobre crenças sobre crenças), constrói um agente mínimo consciente do ToM e mede como é a coordenação real versus como é a vestimenta rápida.

> Este curso irá considerar o TOM como uma capacidade específica de fazer uma análise de crenças sobre crenças), construir um mínimo de TOM percebimento Agente, e medir a verdadeira coordenação e a diferença entre a ideia de decoração.

## Conceptos básicos

### O que significa ToM

Psicologia do desenvolvimento: uma criança de 3 anos pensa que o mundo interior de qualquer pessoa corresponde ao seu. Uma criança de 5 anos entende que os outros têm crenças diferentes. Uma criança de 7 anos explica as crenças sobre crenças ("ela acha que eu acho que a bola está sob o copo").

> 发展心理学: 3 岁的孩子认为任何人的内心世界都与自己相同―― 5 岁的孩子理解别人的信仰―― 7 岁的孩子推理关于信仰的信念――" Ela acha que eu acho que a bola está debaixo do copo")――这些是零阶段,一阶段和二阶段 ToM──

Para os agentes da LLM, a ToM ordena um mapa para:

> Para o agente de LLM, para o seguinte:

- **Zeroth-order:**O agente só age com base nas suas próprias observações.
  Tradução:**零阶：**Não há modelo de outro. Agente só de acordo com suas próprias observações.
- **First-order:**"Alice acredita em X".
  Tradução:**一阶：**"Alice acredita em X".
- **Second-order:**"Alice acredita que o Bob acredita em X".
  Tradução:**二阶：**"Alice acredita em Bob, acredita em X".

Li et al. 2023 descobriram que a ToM de primeira e segunda ordem surgem em agentes LLM em jogos cooperativos, mas se degradam com um longo horizonte e comunicação pouco confiável.

> Li 等人, em 2023 descobriu, primeira fase e segunda fase ToM em cooperação jogo em Agente LLM emergente, mas em longo prazo e descontrolado comunicação descadação.

### O teste Sally-Anne, em resumo

Um teste de crença falsa de 1985: Sally coloca um mármore na cesta A, deixa. Anne o move para a cesta B. Onde Sally vai olhar quando ela voltar? Uma criança com ToM de primeira ordem diz cesta A (a crença de Sally difere da realidade).

> 1985                                                                                                                                                                                                                                                               

Os LLM da era GPT-4 passam testes de estilo Sally-Anne quando posados de forma clara. Eles falham quando a narrativa é longa, a cena muda várias vezes ou a pergunta é formulada indiretamente. Esse é o estado prático de 2026 do ToM em LLM de produção.

> GPT-4 时代的LLM 在直接问时通过Sally-Anne 风格测试――当叙述很长,场景多次变化或问题间接表达时失败――这是2026年生产LLM 中 ToM的实际状态――

### Medida de coordenação da Riedl

Riedl (arXiv:2510.05174) construiu um teste em escala populacional: N agentes, um objectivo cooperativo, condições de prontidão variáveis.

> Riedl(arXiv:2510.05174) construiu grupo de dimensão test:N 个 Agent,合作目标,可变提示条件――测量:

1. **Identity-linked differentiation.**Os agentes desenvolvem diferenças de papel estáveis ao longo do tempo?
   Tradução:**身份关联分化。**Agente, o que é que se passa?
2. **Goal-directed complementarity.**As acções dos agentes complementam-se (subtarefas diferentes) em vez de duplicarem-se?
   Tradução:**目标导向互补性。**O comportamento do agente é complementar e não repetitivo?
3. **Higher-order synergy.**Uma medida estatística de se o grupo consegue o que nenhum subconjunto poderia.
   Tradução:**高阶协同。**O grupo alcançou uma quantidade estatística que qualquer grupo não pode alcançar.

Resultado: somente sob a condição de ToM prompt, todas as três métricas produzem sinal acima da linha de base. Sem ToM prompt, as métricas flutuam perto da chance para modelos de capacidade moderada.

> Resultado: somente sob as condições de TOM 提示, três indicadores produzem mais alto que o sinal da linha de base. Sem TOM 提示, o indicador do modelo de capacidade média está próximo ao nível de random.

### A ilusão de coordenação

Sem controles estatísticos, a "coordenação emergente" nas demonstrações muitas vezes reflete:

> 没有统计控制, em演示中"涌现协调" geralmente reflete:

- Engenharia rápida que se baseia em coordenação (comunações de sistema que dizem "trabalhar juntos").
  Tradução em inglês:嵌入协调的提示工程(系统提示说"一起工作")
- Bias de observadores (vemos padrões que esperamos).
  Tradução do inglês para o inglês: Observer's bias (We see expectation of pattern)
- Seleção de corridas bem sucedidas após o hockey.
  O sucesso de um negócio é o resultado de uma escolha.

Os sistemas de produção que comercializam a "coordenação emergente" sem sinal mensurável devem ser tratados como comercializados.

>  não há sinais de medição sobre a propaganda de "emergência coordena" o sistema de produção deve ser considerado como marketing.

### Um agente minimamente consciente de TOM

Estrutura:

```
agent state:
  own_beliefs:    {facts the agent believes}
  other_models:   {other_agent_id -> {beliefs_the_agent_attributes_to_them}}
  actions_last_N: [history of others' actions]

observation update:
  - update own_beliefs from direct observation
  - update other_models[agent_id] from their action + prior beliefs

action selection:
  - enumerate candidate actions
  - for each, predict what each other agent will do next given their modeled beliefs
  - pick action that maximizes joint outcome under those predictions
```

O `other_models`O atributo é o estado ToM. O primeiro ordenamento ToM mantém apenas um nível.`other_models[i][other_models_of_j]`O que eu acho que o Agente J acredita.

### Por que o longo horizonte dói

Li et al. documento: limites de contexto fazem com que os agentes esqueçam qual crença pertence a quem. A alucinação adiciona crenças falsas a outros modelos de agentes. Ambos produzem erros "Eu pensei que ele pensava X" que se compõem ao longo do tempo.

As medidas de mitigação documentadas no documento e em seguimento em 2024-2026:

- **Explicit ToM state in the prompt.**Formatos estruturados: `{agent_id: belief_list}`Força a recuperação para preservar a vinculação entre identidade e crença.
- **Shorter reasoning chains.**Menos atualizações de ToM por turno reduzem a alucinação composta.
- **External ToM store.**Manter o modelo fora do contexto do MLL; injetar apenas partes relevantes por turno.

### Quando a ToM falhar na produção

- **Adversarial settings.**Os agentes com boa ToM são mais fáceis de manipular (você pode modelar o que eles modelam de você, depois explorar).
- **Heterogeneous teams.**Quando os modelos são diferentes, o modelo ToM que funciona para um oponente não generaliza.
- **Ground-truth-dependent tasks.**A TOM é sobre crenças; se a correcção depende dos fatos, a TOM pode ser uma distração.

### A coordenação que você pode realmente medir

Três sinais práticos que a coordenação de uma equipa é real, em vez de vestida de forma rápida:

1. **Complementarity over time.**Em uma tarefa de várias rotas, as ações dos agentes cobrem sub-tarefas dissociadas?
2. **Anticipation.**A ação do agente A na virada T + 1 depende de uma previsão sobre a ação de B em T + 2 que resultou correta?
3. **Correction.**Quando A interpreta erroneamente a crença de B na curva T, A corrige com a curva T + 2?

Estes são mensuráveis num sistema de multi-agentes registados. São a versão substancial da narrativa de "coordenação".

## Construí-lo.
```figure
sw-theory-of-mind
```

## Construí-lo

`code/main.py`Implementos:

- `ToMAgent` acompanha as próprias crenças e os modelos de crenças de cada agente.
  Tradução:`ToMAgent` Seguir as suas próprias crenças e o modelo de crenças de cada outro agente.
- Uma tarefa cooperativa: três agentes devem coletar três tokens de três caixas; cada caixa pode conter um token.
  Em inglês, "Tres agentes" é uma palavra que significa "três agentes" ou "três agentes".
- Duas configurações: `zeroth_order`(sem TOM) e `first_order`(ToM com modelo de crença de nível único).
  Tradução do português:`zeroth_order`(sem TOM)`first_order`(带一层信念模型的 ToM)
- Medida de 200 ensaios aleatórios: taxa de conclusão, taxa de duplicação (dois agentes que visam a mesma caixa), rotação média até conclusão.
  中文翻译:200 次随机试验的测量:完成率、重复率(dois agentes 准同一个盒子) 、 média completa轮次。

- Correr .

```
python3 code/main.py
```

Output esperado: agentes de ordem zero duplicam o esforço a uma taxa de ~ 35% e completam ~ 60% dos ensaios em 10 voltas. agentes ToM de primeira ordem duplicam a ~ 5% e completam ~ 95%.

> 预期输出: Zero-fase Agente 以约 35% de porcentagem de re-obração e completar em 10 rodadas cerca de 60% de experiências.

## Usa-o. Usa-o.

`outputs/skill-tom-auditor.md`É uma habilidade que verifica a afirmação de "coordenação emergente" de um sistema multi-agente.

> `outputs/skill-tom-auditor.md`É uma habilidade de um agente de auditoria  sistema "emerge coordenação" declaração  inspecção de sugestões de decoração  comparação entre a significância estatística e a complementação de medidas 

## Envia-o .

Lista de verificação das reivindicações de coordenação:

- **Control condition.**Uma versão do seu sistema sem o aviso de coordenação.
  Tradução:**对照条件。**Não há coordenação de informação em todas as partes.
- **Statistical test.**A diferença entre sistema e controlo é significativa em `p < 0.05`- Na sua métrica?
  Tradução:**统计测试。**A diferença entre o sistema e o compartimento está no seu indicador.`p < 0.05`É muito significativo?
- **Complementarity measure.**Ações-disjunção ao longo do tempo, não apenas o sucesso final.
  Tradução:**互补性测量。**O movimento não se encaixa com o tempo, não é apenas o sucesso final.
- **Failure-case log.**Quando os agentes se descoordenam, como é que o estado do ToM parece?
  Tradução:**失败案例日志。**Quando o agente coordena falha, como é que está o teu estado?
- **Model-capacity disclosure.**Se o efeito desaparecer em modelos menores, diga-o.
  Tradução:**模型能力披露。**Se o efeito desaparecer no modelo menor, explica isso.

## Exercícios.

1. Corra .`code/main.py`Confirme que a ToM de primeira ordem reduz a taxa de duplicação em cerca de 7x. A diferença persiste quando escalas para 5 agentes e 5 caixas?
   Tradução: 运行`code/main.py`Confirmar que a primeira fase da TOM reduzirá a taxa de repetição em cerca de 7 vezes.
2. Implementar a ToM de segunda ordem (agente A modela o que B pensa sobre C). Melhora-se em relação à primeira ordem?
   Tradução do inglês para tradução do inglês: implementar a segunda fase do trabalho.
3. Injectar um **hallucination**O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?
   中文翻译:向 ToM 状态注入**幻觉**A cada rodada, a cada vez mais, a convicção é transformada.
4. Leia Li et al. (arXiv:2310.10701). Reproduzir a descoberta de "degradação de longo horizonte": à medida que as turnas crescem de 10 para 30, como o seu desempenho de primeira ordem ToM muda?
   Chinese Translation:阅读 Li 等人(arXiv:2310.10701)。复现"长期退化"发现:当轮次从10 增长到30 时,你的一阶 ToM 性能如何变化?
5. Leia Riedl 2025 (arXiv:2510.05174). Implemente a estatística de sinergia de ordem superior nos seus registros de simulação.
   Não há nenhum tipo de "condição" que possa ter efeito?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Theory of Mind / 心智理论 | "Understanding others' minds" / "理解他人的心理" | The capacity to model another agent's beliefs. Graded by order (0, 1, 2+). / 建模另一个 Agent 信念的能力。按阶次分级（0, 1, 2+）。 |
| Sally-Anne test / Sally-Anne 测试 | "The false-belief test" / "错误信念测试" | 1985 developmental psychology; LLMs pass plain versions, fail complex ones. / 1985 年发展心理学；LLM 通过简单版本，复杂版本失败。 |
| First-order ToM / 一阶 ToM | "A believes X" / "A 相信 X" | Modeling one other's beliefs about facts. / 建模另一个关于事实的信念。 |
| Second-order ToM / 二阶 ToM | "A believes B believes X" / "A 相信 B 相信 X" | Recursive modeling one level deeper. / 递归建模更深一层。 |
| Identity-linked differentiation / 身份关联分化 | "Stable roles over time" / "稳定的角色" | Riedl's metric: roles persist, not random. / Riedl 的指标：角色持续而非随机。 |
| Goal-directed complementarity / 目标导向互补性 | "Disjoint actions" / "不交动作" | Agents target different subtasks, not the same one. / Agent 瞄准不同子任务，不是同一个。 |
| Higher-order synergy / 高阶协同 | "Group exceeds any subset" / "群体超越任何子集" | Riedl's statistical measure for real coordination. / Riedl 对真正协调的统计度量。 |
| Coordination illusion / 协调幻觉 | "It looks coordinated" / "看起来协调" | Prompt-dressed appearance of coordination without measurable signal. / 没有可测量信号的提示装饰的协调外观。 |

## Mais leitura 延伸阅读

- [Li et al. — Theory of Mind for Multi-Agent Collaboration via Large Language Models](https://arxiv.org/abs/2310.10701) ToM emergente em jogos cooperativos; modos de falha de longo horizonte
- [Riedl — Emergent Coordination in Multi-Agent Language Models](https://arxiv.org/abs/2510.05174) medição em escala populacional; a indicação de TOM é a condição de carga
- [Premack & Woodruff — Does the chimpanzee have a theory of mind?](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/does-the-chimpanzee-have-a-theory-of-mind/1E96B02CD9850E69AF20F81FA7EB3595) a origem do conceito de TOM em 1978
- [Baron-Cohen, Leslie, Frith — Does the autistic child have a theory of mind?](https://doi.org/10.1016/0010-0277(85)90022-8)  o artigo Sally-Anne (1985)
