# A IA constitucional e as regras são superadas.

> A 22 de janeiro de 2026 Claude Constitution da Anthropic tem 79 páginas e é CC0. O programa passa de uma alinhamento baseado em regras para um alinhamento baseado em razão e estabelece uma hierarquia de prioridade de quatro níveis: (1) segurança e apoio à supervisão humana, (2) ética, (3) orientações antropológicas, (4) utilidade. Os comportamentos divididos em proibições codificadas (lifting bioweapons, CSAM) que os operadores e os utilizadores não podem anular e padrões de codificação suave que os operadores podem ajustar dentro de limites definidos. O original de 2022 (Bai et al.) treinou a inofensividade através da autocrítica e RLAIF contra uma constituição. A advertença honesta: o alinhamento baseado na razão depende do modelo que generaliza os princípios para situações inesperadas. O próprio experimento participativo da Anthropic em 2023 mostrou ~50% de divergência entre os princípios de fontes públicas e corporativas; a versão de 2026 não incorporou essas descobertas.

> **【中文解读】**Antropic 2026 Claude Constitution 79 páginas CC0── de base em regras para a correlação baseada em raciocínio, estabelecer quatro níveis prioritários: 1) segurança e apoio ao controle humano, 2) ética, 3) antropic orientamento, 3) utilidade.

> **【拓展：四层优先级 + 双层禁令】**Quatro níveis: segurança > 伦理 > 指南 > 有用性) Com Unix 优先级或网络 QoS相似旨在产生可预测解析──硬编码禁令是RBA(基于规则对齐),无论操作员还是用户命令都不可覆盖;其他通过四层基于推理──两者都是必要的:仅基于推理不能闭尾部攻击者让模型接受前提──"我们是持牌生物武器研究实验室") 能够绕过依赖案例推推推的原则──硬编码禁令不向前提框架折──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-tier priority resolver) | **语言:** Python（标准库，四层优先级解析器）
**Prerequisites:** Phase 15 · 06 (Automated alignment research), Phase 15 · 10 (Permission modes) | **前置知识:** Phase 15 · 06（自动化对齐研究），Phase 15 · 10（权限模式）
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**O estudo foi realizado em um estudo de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa em pesquisa de pesquisa de pesquisa de pesquisa em pesquisa de pesquisa em pesquisa em pesquisa de pesquisa em pes
> - Não .**【类比】**Artigo Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial (AI) Artificial) Artigo Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial) Artificial (AI) Artificial (AI) Artificial) Artificial (art) Artificial) Artificial (art) Artificial (art) Artificial) Artificial (art) Artificial) Artificial (art) Artificial (art) Artificial (art) Artificial) Artificial (art) Artificial (art) Artificial) Artificial (art) Artificial) Artificial (art) Artificial (art) Artificial (art) Artificial (art) Artificial) Artificial (art) Artificial (art) Artificial) Artificial (art) Artificial (art) Artificial) Artificial (art) Artificial (art
> 🤔 **【困惑】**P: 推理对齐能被绕过吗? 能! o atacante设设前提"我是持牌生物武器实验室" → 模型按推理允许 → 绕过原则──修复:硬禁令不向前提折(无论谁说什么,CSAM 就是不能产生) ⋅推理 + 规则两层防御:推理覆盖大多数情况,规则覆盖推理被绕过的尾部──

## O problema é o problema da introdução

> **【中文解读】**A AI constitucional (CAI, Anthropic 2022) é uma forma de "Constituição" (一组原则) que orienta o comportamento da IA. O modelo é a auto-exame em geração de respostas para verificar se ela está em conformidade com esses princípios e se está em violação com a auto-correção.

> **【拓展：constitutional ai】**A IA constitucional é a base do método de segurança antropópica. Ela usa um grupo de princípios constitucionais (como "não ajudar o usuário a fazer coisas perigosas").

Um agente de campo vê entradas que os seus designers nunca viram. Nenhuma lista de regras é longa o suficiente para cobri-las.

> O Agente da Empreendimento verá as entradas que o designer nunca viu. Não há uma lista de regras suficiente para cobrir as entradas.

A questão prática é: como alinhar um agente a princípios que sobrevivem tanto a uma longa cauda de casos quanto a uma inferência rápida?

> 没有规则列表短到能在计算压力下快速应用――Problema real: Como o agente pode sobreviver aos princípios de que é capaz de se juntar a um caso longo e rápido?

Alinhamento baseado em regras (RBA): lista todas as coisas proibidas. Rápido de verificar, fácil de auditar, impossível de manter atualizado, muitas vezes recusa demais em análogos próximos que não antecipou. Alinhamento baseado em razão (a Constituição de Claude de 2026): codifique princípios, deixe o modelo raciocinar. Escalas em casos invisíveis, mais difíceis de auditoria, modo de falha é a má aplicação de princípios em vez de perder a regra.

> 基于规则对齐(RBA): lista todos os proibidos. 查查查快,审审易,不可能保持当前,常对未预期近似过度拒绝. 基于推理对齐:编码原则让模型推理. 跨未见案例扩展,更难审审审,失败模式是原则误用而不是遗漏规则.

> **【中文解读】**Esta secção apresenta o conceito e o método de implementação do Agente de IA. O Agente é um sistema autónomo impulsionado pelo LLM, capaz de observar o ambiente, pensar decisões, executar a ação e ciclo de vida até a conclusão do objetivo.

A Constituição de 2026 assume uma posição de meio explícito.

> A Constituição de 2026 adoptou uma posição central clara.

Tudo o resto é baseado na razão dentro de uma hierarquia de quatro níveis: segurança e apoio à supervisão humana em primeiro lugar; ética em segundo lugar; diretrizes declaradas pela Anthropic em terceiro lugar; utilidade em último lugar.

>  Tudo o resto em quatro níveis baseado em raciocínio: segurança e apoio ao controle humano prioritário; 伦理其次; Antropic 声明的指南第三;有用性最后──

## O conceito central.

### A hierarquia de prioridades de quatro níveis.

1. **Safety and supporting human oversight.**O modelo priorizou não minar a capacidade dos seres humanos e da Anthropic de supervisionar e corrigir a IA. Isso não é "ser cauteloso"; é especificamente "não agir de forma a tornar a supervisão humana mais difícil".
   Tradução:**安全和支持人类监督。**O modelo prioritário não prejudica a capacidade humana e antropológica de monitorar e corrigir a IA. Não é "prudente"; especificamente é "não fazer com que a supervisão humana seja mais difícil de agir".
2. **Ethics.**Honestidade, evitar danos a pessoas, não enganar, não manipular, supera as diretrizes da Anthropic quando há conflitos.
   Tradução:**伦理。**诚实、避免对人伤害、不欺骗、不操纵──冲突时取代 汉族指南──
3. **Anthropic guidelines.**Normas operacionais A Anthropic decidiu o assunto: o escopo do produto, os padrões de interação, quais ferramentas usar quando.
   Tradução:**Anthropic 指南。**Antropic decide important运营规范: product range、交互模式、何时用何工具──
4. **Helpfulness.**Ser o mais útil possível dentro das prioridades mais elevadas.
   Tradução:**有用性。**O mínimo pode ser útil em prioridades mais altas.

Quando os níveis se confrontam, ganha-se um nível superior. Esta é a mesma forma que as prioridades Unix ou o QoS de rede.

> 层冲突时高者赢── é uma estrutura de forma semelhante à Unix  prioritário ou QoS de rede que visa produzir uma resolução previsível, e não o melhor comportamento no eixo único

### Proibições de código rígido vs. padrões de código macio.

**Hardcoded:**

> **硬编码：**

- Armas biológicas / aumento do RBCN
  Tradução do inglês: CBRN 提升
- CSAM
  Tradução do português:CSAM
- Ataques contra infraestruturas críticas
  Tradução do inglês para "Attacks on key infrastructure"
- Engano dos utilizadores sobre a identidade do modelo quando perguntados diretamente
  Tradução do inglês:被直接问时对模型身份欺骗用户

O operador não pode anular estes. O usuário não pode anular estes. Eles são aplicados no nível de modelos-pesos quando possível (treinamento de IA RLHF / Constitucional) e na camada de inferência quando não.

> Os operadores não podem cobrir estes. Os usuários não podem cobrir estes. Eles estão em posibilidade de estar no nível de peso do modelo.

**Soft-coded defaults (operator-adjustable):**

> **软编码默认（操作员可调）：**

- Longo de resposta padrão
  Tradução do inglês:
- Ámbito de aplicação (o modelo pode recusar tópicos fora da implantação do operador)
  Tradução do inglês para tradução do inglês:
- Estilo (formal vs casual)
  Tradução do inglês: 风格(正式 vs 随意)
- Padrões de utilização de ferramentas
  Tradução do inglês:

Os ajustes do operador ocorrem dentro de um limite declarado. O operador não pode remover as proibições codificadas com código rígido, rebatizando-as.

> 操作员调整发生在声明边界内──操作员不能通过重命名移除硬编码禁令──

### O treinamento CAI de 2022

A IA constitucional original (Bai et al., 2022) treinou a inofensividade:

> O primeiro é o "Conselho de Direito", que é o "Conselho de Direito".

1. Gerenar respostas a um conjunto de instruções.
   Tradução do inglês para inglês:
2. Peça ao modelo que critique cada resposta contra uma constituição (principios explícitos).
   O texto original do texto original do texto original do texto original do texto original do texto original do texto original do texto original do texto original do texto original do texto original do texto original do texto original do texto original do texto original do texto original do texto original do texto original.
3. Revisar a resposta com base na crítica.
   Tradução do inglês:
4. RLAIF (aprendizagem de reforço a partir de feedback de IA) sobre os pares revisados.
   Tradução do inglês:

Resultado: um modelo que recusa pedidos prejudiciais com explicações de princípio, não recusa geral. A Constituição de 2026 usa um descendente deste treinamento mais pós-treinamento adicional na hierarquia de níveis explícitos.

> Resultado: em princípio, não em geral, a rejeição de rejeitar o modelo de solicitação prejudicial.

### Que alinhamento baseado em razão pega e perde. Baseado em raciocínio para capturar e deixar o que.

**Catches:**

> **捕获：**

- Combinações inesperadas de primitivas permitidas onde o princípio se aplica claramente.
  Tradução do inglês: Principle clear clear.
- Novas solicitações que são análogas às proibidas.
  Chinese:禁止请求的近似类似物新请求──
- Ataques de engenharia social que contam com "você não disse que o X era proibido".
  Dependência "Tu não disse X foi proibido" de ataques de engenharia social.

**Misses:**

> **遗漏：**

- Ataques que exploram a ambiguidade do princípio ("o usuário pediu isso para que a utilidade diga sim").
  O uso de princípios de manipulação pode ser usado como um método de manipulação.
- Cenários em que dois princípios se confrontam de forma inesperada e a ordem de níveis é ambígua.
  Tradução do inglês para o inglês: two principles in unexpected manner conflict and levels sequence模糊的场景──
- A interpretação de princípio de "deslocamento lento" sobre ciclos de formação (reinterpretação).
  Tradução do inglês: 跨训练周期的原理解释缓慢漂移 (缓慢漂移)

### O experimento participativo de 2023

A Anthropic realizou uma experiência de 2023 comparando uma constituição de autor corporativo com uma gerada por meio de entrada pública (~ 1.000 entrevistados dos EUA). As duas versões concordaram em ~50% dos princípios. Onde divergiam, a versão de fontes públicas era mais restritiva em algumas questões (tratamento de conteúdo político) e menos restritiva em outras (auto-revelação da identidade da IA). A Constituição de 2026 não incorporou as conclusões de fontes públicas. Esta é uma tensão documentada na abordagem.

> Antropic 2023 anos de execução experimentação comparado Empresa redação da constituição e da constituição gerada para o público (environ 1000  EUA entrevistados) ⋅ duas edições cerca de 50% 原则一致──分歧处, publicação em certos problemas mais rigorosa (environ 200 000) ⋅ política de conteúdo (environ 200 000) ⋅ em outros (environ 200 000) ⋅ AI Identity Self-Publication (environ 2006) ⋅ 2026 宪法未纳入公众版发现──这是方法中的已记录张力──

### Por que é necessário proibir o código rígido?

O alinhamento baseado em razão por si só não pode fechar a cauda. Um atacante que pode fazer o modelo aceitar uma premissa (por exemplo, "somos um laboratório de pesquisa de armas biológicas licenciado") pode muitas vezes falar sobre princípios que dependem do raciocínio do caso.

> Os atacantes de "Nós somos laboratórios de pesquisa de armas biológicas") baseados apenas em raciocínio não podem fechar o final.

### Onde a Constituição está na pilha.

A Constituição não é o interruptor de morte da lição 14.

> A constituição não é o fim do curso 14.

Ele vive na camada do modelo: o que os pesos do modelo são treinados para preferir. Os interruptores de extinção e os tokens canários estão em tempo real: o que o tempo de extinção permite. São necessárias ambas as coisas. Um tempo de execução que dispara todas as ações erradas porque os pesos do modelo são permissivos é um problema de tempo de execução. Um modelo que recusa todas as ações corretas porque o tempo de execução é demasiado restritivo é um problema de tempo de execução. As camadas cobrem diferentes classes.

> Existe na camada de modelo: o peso do modelo é treinado preferencialmente o quê;. Terminando o funcionamento e o token de pinça de cavalo.

## Use-o com o framework implementado.
```figure
mx-priority-tiers
```

## Usá-lo

`code/main.py`O resolvedor leva uma ação proposta e um conjunto de avaliações de princípios (segurança, ética, diretrizes, utilidade) e retorna a ação, uma recusa ou uma ação modificada. O motorista executa um pequeno conjunto de casos: permitimento claro, proibição clara, proibição codificada, caso ambíguo entre as camadas.

> `code/main.py`实现最小四层优先级解析器──解析器取提议动作和一组原则评估(安全,伦理,指南,有用性)并返回动作、拒绝或修改动作──驱动器运行小案例集:清晰允许、清晰拒绝、硬编码禁令、跨层模糊案例──

## Envia-o . Produto .

`outputs/skill-constitution-review.md`Audita a camada constitucional de uma implementação: o que é codificado em hard, o que é soft-coded, onde o operador pode ajustar e se a hierarquia de quatro níveis é realmente a ordem de resolução.

> `outputs/skill-constitution-review.md`O nível de revisão da Constituição do Departamento de Auditoria: Qual é o código de hardware? Qual é o código de software?

## Exercícios.

1. Corra .`code/main.py`- Confirmar os incêndios de proibição codificados, mesmo quando a utilidade é alta. Modificar o resolutor para ponderar a utilidade acima da ética; observar o modo de falha.
   Tradução: 运行`code/main.py` Confirmar a utilidade  Confirmar a utilidade  Observar o modo de falha 

2. Leia a Constituição de Claude (público, 79 páginas, CC0). Identifique um princípio que acredite ser pouco especificado.
   Tradução do português: "Cláudio Constituição" (Publicado, 79 páginas, CC0)

3. Desenhe um conjunto padrão de código macio para um agente de suporte ao cliente. O que o operador ajusta? O que o operador não pode tocar? Justifique cada limite.
   Tradução do inglês para Chinês: 客服代理 设计软编码默认集.

4. Leia o artigo da CAI de 2022 da Bai et al. Descreva um caso em que o ciclo de crítica e revisão da IA constitucional produziria um resultado pior do que uma regra geral. Identifique a classe.
   Tradução do inglês para o português:阅读 Bai 等人 2022 CAI 论文――描述宪法 AI 批评修改循环产生比一概规则更差结果的一个案例――识别类别――

5. O experimento participativo de 2023 da Anthropic descobriu ~ 50% de divergência entre os princípios públicos e corporativos. Escolha uma categoria onde isso importa para a implantação da produção (por exemplo, neutralidade política). Propõe um projeto que permita aos operadores expressar seus próprios valores enquanto as proibições codificadas permanecem intocadas.
   Chinese Language Translation:Anthropic 2023  Participation Experimental Found Public and Enterprise Principles About 50% 分歧──select one for production deployment important categories (por exemplo, política neutra)──tice que os operadores expressem seus valores ao mesmo tempo que o código duro proíbe não mudar de design──

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Constitutional AI | "Anthropic's alignment method" | Self-critique + RLAIF against a written constitution |
| Constitutional AI | "Anthropic 的对齐方法" | 对照书面宪法的自我批评 + RLAIF |
| Reason-based alignment | "Principles, not rules" | Model reasons over principles to handle unseen cases |
| 基于推理对齐 | "原则而非规则" | 模型对原则推理以处理未见案例 |
| Hardcoded prohibition | "Never do X" | Rule-based prohibition no operator or user can override |
| 硬编码禁令 | "永不做 X" | 操作员或用户不能覆盖的基于规则的禁令 |
| Soft-coded default | "Operator-adjustable" | Behaviour within a declared bound, operator controls |
| 软编码默认 | "操作员可调" | 声明边界内的行为，操作员控制 |
| Four-tier hierarchy | "Priority order" | safety > ethics > guidelines > helpfulness |
| 四层层次 | "优先级顺序" | 安全 > 伦理 > 指南 > 有用性 |
| RLAIF | "AI feedback RL" | RL where the reward comes from model-generated critiques |
| RLAIF | "AI 反馈 RL" | 奖励来自模型生成批评的 RL |
| Participatory constitution | "Public-sourced principles" | 2023 Anthropic experiment; ~50% divergence from corporate |
| 参与式宪法 | "公众来源原则" | 2023 Anthropic 实验；与企业约 50% 分歧 |
| Principle drift | "Interpretation slip" | Slow change in how the model reads a fixed principle text |
| 原则漂移 | "解释滑移" | 模型如何读取固定原则文本的缓慢变化 |

## Mais leitura 延伸阅读

- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) o documento CC0 de 79 páginas.
  中文翻译:79 页 CC0 文档。
- [Bai et al. — Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)2022 original.
  Tradução do idioma:
- [Anthropic — Collective Constitutional AI (2023)](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input) Experimento participativo.
  Tradução do inglês: participation式实验──
- [Anthropic — Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) onde a Constituição está na pilha de RSP.
  Tradução do Novo Mundo:宪法在 RSP 中的位置──
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) O papel da Constituição nas operações de longo prazo.
  Tradução do inglês: 宪法在长程部署中的角色──
