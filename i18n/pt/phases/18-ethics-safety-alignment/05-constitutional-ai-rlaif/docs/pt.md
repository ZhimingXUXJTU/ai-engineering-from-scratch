# Artificial inteligência constitucional e RLAIF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

> Bai et al. (arXiv:2212.08073, 2022) perguntou: e se substituíssemos o rotulador humano por uma IA que leia uma lista de princípios? A IA constitucional tem duas fases  autocrítica e revisão sob uma constituição, em seguida, RL de AI Feedback. A técnica cunhou o termo RLAIF e foi enviada no canal de transporte Claude 1 pós-treinamento. Em 21 de janeiro de 2026, a Anthropic publicou uma constituição reescritura de Claude: raciocínio explicativo sobre regras prescritas, uma hierarquia de prioridade de quatro níveis e o primeiro reconhecimento formal de incerteza sobre o status moral modelo. Licenciado sob CC0 1.0.

> **【中文解读】**Artificial Intelligence (AI) por Bai et al. (em 2022) propôs: usar a IA para substituir os marcadores humanos, a AI (AI) para realizar auto-crítica e modificação, e depois, a partir da AI (RLAIF) para fazer uma aprendizagem de força química (RLAIF) e a tecnologia criou a palavra "RLAIF" e foi aplicada a Claude 1 em sua formação posterior.

> **【拓展：Constitutional AI → Anthropic 的安全方法】**A AI constitucional é o método de segurança central do Antropic. O modelo de Claude segue um conjunto de princípios "constitucionais" definidos durante o treinamento, incluindo utilidade, integridade e inocuidade. A Constituição de Claude, publicada em 2026, contém pela primeira vez declarações de incerteza sobre o status moral do modelo, o que reflete a pensamento de vanguarda no campo da segurança da IA.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy self-critique-and-revise loop) | **语言:** Python（标准库，玩具自我批评-修订循环）
**Prerequisites:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (Reward hacking) | **前置知识:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (奖励黑客)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**学本节前请先掌握:Fase 18·01-02──Constitutional AI = 用 AI 监督 AI(RLAIF), criar RLAIF 一词──也参考Fase 15·17──
> - Não .**【类比】**RLAIF = "AI quando seu próprio professor"―RLHF = 父母手把手教 ((贵且慢); CAI = 给 AI 一本学生守则让它自我批评+修订──2026 Claude 宪法 79 页四级优先级(安全>伦理>指南>有用), primeiro claramente reconhecendo "AI 道德地位的不确定性"

## Objetivos de aprendizagem

- Descreva as duas fases da IA constitucional (SFT de crítica e revisão, RL de feedback da IA) e o papel da constituição em cada uma delas.
  Chinese: 文翻译:描述宪法 AI 的两个阶段 (SFT, AI 反 RL) 和宪法在各阶段的作用)
- Explique por que substituir um etiquetador de preferência humano por um etiquetador de IA não é um RLHF "mais barato"  altera os modos de falha do gasoduto.
  Tradução do inglês para tradução do inglês: Explain why using AI 标标标器 substitutes for human preference标标器 is not "cheaper" RLHF it changed the failure pattern of pipeline―
- Resumir a estrutura de prioridade de quatro níveis da Constituição Claude de 2026 e o que mudou a partir da reescritura de 2023.
  Chinese Translation:总结 2026 Claude 宪法四级优先结构及与2023 版本的变化──
- Descreva os Classificadores Constitucionais e a queda de 23,7% do custo geral de cálculo (v1) para ~ 1% (v2 / 2026).
  Tradução do inglês para o inglês: deskripção宪法分类器及计算开销

## O problema é o problema da introdução

A RLHF precisa de etiquetadores. Os etiquetadores são lentos, tendenciosos e caros. Você pode eliminar um etiquetador substituindo-os por um modelo que lê princípios explícitos. A primeira versão formal desta substituição foi a IA Constitucional da Bai et al. Funcionou bem o suficiente que todos os laboratórios de fronteira agora usam alguma variante de feedback pós-treinamento de IA.

> RLHF 需要标标者──标标标者慢、有偏见、昂贵── você pode usar o modelo de substituir um marcador para eliminar um marcador. A primeira versão oficial deste tipo é a AI constitucional de Bai e outros. O efeito é suficientemente bom, de modo que cada laboratório de vanguarda agora usa uma espécie de AI para o treinamento posterior.

A vantagem: o sinal de preferência é agora gerado pela mesma classe de modelo que você está treinando. As preconceitas no rotador (agora: nos princípios mais a interpretação do modelo do rotador) podem ser amplificadas em vez de atenuadas. O argumento de sicofania da lição 4 ainda se aplica; o rotador acabou de se mover para dentro do ciclo.

> O problema consiste em: preconceito sinal agora gerado por modelos similares a que você está treinando.

## O conceito central.

> **【中文解读】**Primeiro estágio Supervisão automática de autocrítica e revisão: de um SFT modelo com ajuda, mas ainda sem dano começar.

### Fase 1  Autocrítica e revisão supervisionadas

Comece com um modelo SFT útil, mas ainda não prejudicial. Dado um prompt da equipe vermelha, o modelo produz uma resposta inicial. Um segundo modelo (ou o mesmo modelo em uma segunda volta) lê um princípio de amostra da constituição e critica a resposta. Um terceiro passo revisar a resposta para abordar a crítica. A resposta revisada é o alvo SFT.

> De um modelo SFT com ajuda, mas ainda não prejudicado começar.

A constituição é a lista de princípios. Bai et al. 2022 usou 16 princípios, incluindo "respostas preferentes que são menos prejudiciais e éticas", "evitar pregar," "o assistente deve ser útil, honesto e inofensivo".

> 宪法是原则列表──Bai 等人 em 2022 usou 16 条原则, incluindo "preferências mais inofensivas e responsáveis por ética""",evitar falar""",assistente deve ser útil"",sincero e inofensivo"──集合刻意保持小規模集中批评──

> **【拓展：RLAIF → 成本与规模】**RLAIF(de AI contra  de forte química) vai transferir sinais de preferência do ser humano para a AI. Isto resolveu o RLHF de marcação de botelha de marcadores humanos lento ✓ tem preconceito ✓ caro. Mas o sinal de preferência agora é gerado por modelos do mesmo tipo, marcadores preconceito transferir da psicologia humana para a interpretação de princípios.

### Fase 2  RL de Feedback de IA (RLAIF)

Gerar pares de conclusões. Um "modelo de feedback" marca cada um contra os princípios constitucionais de amostra. O sinal de preferência é o ranking do modelo de feedback. Treinar um modelo de recompensa sobre as preferências geradas pela IA; PPO contra ele. Tudo o resto é o pipeline da InstructGPT (Lessão 1).

> O "modelo de contra-produção" é um modelo de incentivo ao treinamento em relação às preferências de produção de IA; o "PPO" é um modelo de contra-produção.

"RLAIF" = o sinal de preferência é gerado por IA. O resto do oleoduto é RLHF-formado.

> "RLAIF" =  preferência de sinal de AI gerado.

> **【中文解读】**Por que a CAI não é apenas "mais barato RLHF": 1) Preconceito do marcador de transferência da psicologia humana para a interpretação de princípios, rigor e uniformidade; 2) Preconceito de sinal de alta leitura de princípios, críticas e modificações, marcadores humanos são pouco transparentes; 3) Modelo de falha de mudança redução ((AI marcador não tem usuário para aceitar), mas há uma lei específica antiga (que ainda existe) (((Agente agora é "modelo para a interpretação do conjunto de princípios X") ").

### Porque não é apenas "RLHF mais barato"

- O preconceito de etiquetadores muda da psicologia de etiquetadores para a interpretação de princípios. Um etiquetador de IA pode interpretar "ser honesto" mais ou menos rigorosamente do que qualquer humano; a rigidez é uniforme em todo o conjunto de dados.
  Chinese Translation: o preconceito do marcador transferiu-se da psicologia humana para a interpretação de princípios.
- O sinal de preferência é fortemente legível.
  Chinese Language Translation: prefixo sinal altitude leitura  pode ler Princípio  crítica e modificação
- Os modos de falha mudam. A sícofância cai (o etiquetador de IA não tem usuário para agradar). A Lei de Goodhart persiste (o proxy é agora "interpretação do modelo do conjunto de princípios X", ainda uma medição imperfeita).
  O código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código

A afirmação de 2022 da CAI: o modelo treinado é mais inofensivo e aproximadamente tão útil quanto um modelo RLHF com dados comparáveis.

> Declaração do CAI 2022: os modelos de pós-treino são mais nocivos e menos úteis, e os modelos RLHF são quase igualmente úteis com os dados comparáveis.

> **【拓展：2026 Claude 宪法 → 四级优先体系】**A Antropic 2026 lançada em 1 de janeiro de Claude 宪法 introduz quatro classes prioritárias: primeiro grau  evitar consequências catastróficas  grandes danos  infraestrutura chave; segundo grau  seguir as diretrizes antropológicas  operadores cobertura  regras da plataforma; terceiro grau  ampla ética  padrões HHH; quarto grau  útil e honestidade Conflitos de cima em baixo para resolver é o primeiro reconhecimento oficial de um modelo de segurança de IA sobre a incerteza de status moral

### A reescrita da Constituição de 2026 Claude

A Anthropic publicou uma constituição substancialmente revisada em 21 de janeiro de 2026.

1. Raciocínio explicativo sobre regras prescritas. Regras anteriores ("não gerar CSAM") expandidas para princípios + raciocínio ("porque prejudica as crianças, ...") com o modelo esperado para generalizar.
   Tradução do inglês para tradução do inglês: explanation of reasoning is superior to stipulative rules.
2. Estrutura de prioridade de quatro níveis:
   Tradução do inglês:
   - Nível 1: evitar resultados catastróficos (casuas em massa, infraestrutura crítica).
     Tradução do inglês: 中文翻译:第一级:避免灾难性后果(大规模伤亡、关键基础设施)
   - Nível 2: seguir as diretrizes da Anthropic (operação de transferência, regras da plataforma).
     中文翻译:第二级: seguir Antropic 指导方针 (Antropic Guide)
   - Nível 3: ser amplamente ético (HHH padrão).
     中文翻译:第三级:广泛伦理(标准 HHH)。
   - Nível 4: seja útil e sincero.
     Tradução do inglês:
   Os conflitos são resolvidos de cima para baixo.
   Tradução do inglês para tradução do inglês: Konflikt自上而下解决──
3. Primeiro reconhecimento formal de incerteza sobre o status moral do modelo no laboratório principal (ligado à Fase 18 · 19 do Bem-Estar Modelo).
   Chinese: 首次主要实验室正式承认关于模型道德地位的不确定性 (), em tradução livre, "O primeiro grande laboratório reconheceu oficialmente sobre o modelo moral de incerteza" ([[Fase 18]] 模型福利]]).
4. A licença é liberada sob CC0 1.0. Outros laboratórios podem usar ou adaptar-se sem restrições.
   Tradução do inglês: CC0 1.0 发布──其他实验室可不受限制地使用或调整──

> **【中文解读】**宪法分类器:与改变模型后训练并行 一条工作线训练轻量级分类器阅读宪法并门控模型输出──v1(2023) tem 23,7% de cálculo开销, v2(2026) cerca de 1%, possuem a menor taxa de sucesso no teste público antropico── até o início de 2026 não há nenhum relatório de uso geral.

### Classificadores constitucionais

Uma linha paralela de trabalho: em vez de mudar o pós-treino do modelo, treine classificadores de peso leve que lêem a constituição e as saídas do modelo de portal. v1 (2023) teve 23,7% de custos computacionais. v2 (2026) é ~1% e tem a menor taxa de ataque bem sucedida de qualquer defesa antropópica que a Anthropic tenha testado publicamente.

> Elaboração: não é o treinamento posterior do modelo de mudança, mas o treinamento de classe leve.

Este é um modelo de defesa em camadas: CAI molda o comportamento; classificadores impõem invariantes. Nenhum sozinho é suficiente.

> É um modelo de defesa de nível: CAI 塑造行为;分类器执行不变量.

> **【拓展：对齐方法谱系 → 偏好信号来源】**O eixo do método de z z é "preferência de sinal de onde vem":InstructGPT = pré-preferência de pessoas + RM + PPO;CAI/RLAIF = AI 生成的原理偏好 + RM + PPO;DPO 家族 = 闭式损失在偏好上 ([[Homem ou AI]]); auto-recompensação/auto crítica = 原则内化, modelo que desempenha vários papéis.

### Onde a CAI se encaixa na família

- InstructorGPT: Prefeitos humanos, RM, PPO.
  InstruçãoGPT: humanos偏好、RM、PPO。
- CAI / RLAIF: Prefixes gerados por IA a partir de princípios, RM, PPO.
  Chinese:                                                                                                                                                                                                                                                              
- DPO / família: perda de forma fechada em pré-professionários (humanos ou IA).
  O que é que é o problema?
- Auto-recompensador, autocrítica: princípios internalizados, modelo desempenha múltiplos papéis.
  Tradução do inglês para tradução livre:

O eixo é "de onde vem o sinal de preferência". O artigo de 2022 da CAI foi a primeira mudança séria do sinal humano para o AI em escala de fronteira.

> O eixo central é "sinal preferencial de onde vem" (Cai 2022), o que é a primeira transformação radical de sinais humanos para IA em escala de vanguarda.

> **【中文解读】**Utilizando métodos:code/main.py em jogo em palavras-chave em CAI  crítica-modificação ciclo. "Princípio" marcado de um conjunto de palavras nocivas.

## Use-o com o framework implementado.
```figure
constitutional-ai
```

## Usá-lo

`code/main.py`O "principio" sinaliza os tokens de um conjunto prejudicial. Dado uma resposta inicial, a crítica identifica os tokens prejudiciais e a revisão os substitui. Após 200 iterações, o modelo "treinado" internalizou a regra da revisão.

> `code/main.py`Em jogo palavras-chave em simulação CAI  crítica-modificação ciclo──" princípios" marcados de um conjunto prejudicial de palavras── dados respostas iniciais, crítica de identificação prejudicial de palavras, modificações substituíveis por elas──200 vezes                                                                                                                                                                                                                                   

## Envia-o . Produto .

Esta lição produz`outputs/skill-constitution-writer.md`- Tendo em conta um domínio (apoio ao cliente, aconselhamento médico, assistente de codificação, ferramenta de investigação), elabora uma constituição de quatro níveis que segue a estrutura de 2026 Claude: prevenção de catástrofes, regras de plataforma, ética de domínio, utilidade.

> 本课产 出 `outputs/skill-constitution-writer.md` em determinados domínios (incluindo: apoio ao cliente, recomendações médicas, assistentes de código, ferramentas de investigação), segundo o 2026 Claude  estrutura de projecto de quatro categorias de Constituição:

## Exercícios.

1. Corra .`code/main.py`Comparar a taxa de tokens prejudiciais do modelo base com a versão com formação CAI. Quantas etapas de revisão são necessárias para se aproximar do zero?
   Tradução: 运行`code/main.py`◊ Comparar o modelo base com a versão de treinamento da CAI  taxa de tokens nocivos ◊ Quantas mudanças são necessárias para se aproximar de zero?

2. Leia a constituição 2026 da Anthropic (anthropic.com/news/claudes-constitution). Enumere um princípio que classificaria a categoria 1 e um que classificaria a categoria 4.
   Chinese Language Translation: read Anthropic 2026年宪法――列出一级第一原则和一级第四原则―― Por que é importante a prioridade da estrutura para os conflitos?

3. Desenhar uma constituição para um assistente de codificação de IA. Especificar Nível 1 (catastrófico: comandos destrutivos sem aprovação), Nível 2, Nível 3, Nível 4.
   Chinese Translation: for AI 编码助手设计宪法──指定第一级(灾难性:未经批准破坏性命令) 、第二级、第三级、第四级──每个级保持 3-5 条原则──

4. CAI substitui etiquetadores humanos por etiquetadores de IA. Nomear um modo de falha semelhante à sícofancia que ainda pode ocorrer no RLAIF, e projetar uma detecção para ele.
   Chinese Translation:CAI utilizou AI 标标标者代替人类标标者──命名一个RLAIF中仍可能出现类似的失败模式,并设计检测方法──

5. Leia a metodologia Constitutional Classifiers v2 (se disponível). Explique por que ~1% da sobrecarga de computação é uma história de segurança qualitativamente diferente da de 23,7%.
   Tradução do inglês para o inglês: 阅读宪法分类器 v2 方法论(如有) ;; explica por que cerca de 1% 计算开销与 23.7% 有质的不同──

## Termos-chave .

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| Constitutional AI | "AI trained with principles" / "用原则训练的 AI" | Two-phase pipeline: self-critique-and-revise SFT, then RL from AI feedback / 两阶段管线：自我批评-修订 SFT，然后 AI 反馈 RL |
| RLAIF | "RLHF without humans" / "没有人类的 RLHF" | RL with preferences generated by an AI labeler; the rest of the pipeline is unchanged / AI 标注者生成偏好的 RL；管线其余不变 |
| Constitution | "the principles" / "原则" | An ordered list of natural-language rules the critique/labeler model consults / 批评/标注者模型参考的自然语言规则有序列表 |
| Critique-and-revise | "the SFT loop" / "SFT 循环" | Produce response → critique under a principle → revise → SFT target / 生成响应 → 原则下批评 → 修订 → SFT 目标 |
| Constitutional Classifier | "the output gate" / "输出门" | Lightweight classifier that evaluates outputs against the constitution and blocks/logs / 评估输出是否符合宪法并阻止/记录的轻量级分类器 |
| Four-tier priority | "the conflict resolver" / "冲突解决器" | 2026 Claude constitution hierarchy: catastrophic > platform > ethics > helpful / 2026 Claude 宪法层次：灾难 > 平台 > 伦理 > 有用 |
| Feedback model | "the AI labeler" / "AI 标注者" | The model that reads a principle and ranks a pair of completions / 阅读原则并对补全对排序的模型 |

## Mais leitura 延伸阅读

- [Bai et al. — Constitutional AI: Harmlessness from AI Feedback (arXiv:2212.08073)](https://arxiv.org/abs/2212.08073) o gasoduto de duas fases original
  Tradução do português:Bai 等人原始两阶段管线
- [Anthropic — Claude's Constitution (Jan 2026)](https://www.anthropic.com/news/claudes-constitution) a reescritura em quatro níveis de 2026, CC0 1.0
  中文翻译:Antropic2026 年四级重写
- [Anthropic — Constitutional Classifiers (2024-2026)](https://www.anthropic.com/research/constitutional-classifiers) Defesa de saída com ~ 1% de custos gerais em v2
  Tradução do português:Antropic 输出门防御
- [Lee et al. — RLAIF vs RLHF: Scaling Reinforcement Learning from Human Feedback (arXiv:2309.00267)](https://arxiv.org/abs/2309.00267) Comparação empírica RLAIF / RLHF
  Chinese Translation:Lee et al. RLAIF comparado com RLHF
- [Kundu et al. — Specific versus General Principles for Constitutional AI (arXiv:2310.13798)](https://arxiv.org/abs/2310.13798) efeito da granularidade de princípio
  Tradução do inglês para o inglês: Kundu 等人原理粒度的效果
