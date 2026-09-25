# Auto-refinamento e CRÍTICA: Melhoria iterativa de produção .

> Self-Refine (Madaan et al., 2023) usa um LLM em três papéis  gerar, feedback, refinar  em um loop. Ganho médio: +20 absoluto em 7 tarefas. CRITIC (Gou et al., 2023) endurece o passo de feedback roteando verificação através de ferramentas externas. Em 2026 este padrão navega em cada quadro como "evaluador-optimizador" (Antropic) ou um loop de guarda (OpenAI Agents SDK).

> **【中文解读】**Auto-refinamento  deixar um LLM desempenhar três papéis: geração, reformulação, refinamento, ciclo de melhoria. 7 个任务平均提升 20 个百分点. CRITIC将验证步骤通过外部工具进行强化. Em 2026, este já se tornou um padrão de cada framework.

> **【拓展：CRITIC → Claude Code 的自我修复】**O código Claude em redação de código vai executar automaticamente test test test 证 é a produção de um modelo crítico. Quando o teste falha, ele é baseado em erros contra modificações do código, até que o teste seja aprovado.

> - Não .**【前置】**必須先過:Fase 14·01(Agent Loop) 和Fase 14·03(Reflexão) ――Self-Refine é a versão de Reflexão de "单次任务内" (Reflexão 跨多次试验,Self-Refine 在一次生成内代) ―― não compreende o mecanismo de Reflexão de "反思存存到记忆",会混的"反不持久化"特征──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizagem

- Explique as três instruções do Estado Auto-Refinação (generar, feedback, refinar) e explique por que a história importa para o requisito de refinar.
  Não é necessário que o processo de auto-refinamento seja feito de forma independente.
- Explique a visão crítica da CRITIC: Os LLM são pouco confiáveis na autoverificação sem base externa.
  Tradução do inglês para tradução do inglês:
- Implementar um loop de auto-refinamento stdlib com histórico e um verificador externo opcional.
  Tradução do inglês para o inglês: using standard library to realize with historical record and selectable external verifier's Self-Refine cycle
- Mapear este padrão para o fluxo de trabalho "evaluador-optimizador" da Anthropic e as barragens de saída do OpenAI Agents SDK.
  Tradução do inglês para Chinês:将将此模式映射到Antropic's"评估器-优化器"工作流和 OpenAI Agents SDK 的输出护──

## O problema é o problema da introdução

Um agente produz uma resposta quase correta. Talvez uma linha de código tenha um erro de sintaxe. Talvez um resumo seja muito longo. Talvez um plano perca um caso de borda. O que você quer é: o agente critica sua própria saída, e depois a corrige.

> O agente  produziu uma resposta quase correta. Talvez uma linha de código tenha um erro de linguagem. Talvez o resumo tenha sido muito longo. Talvez um plano tenha perdido a situação de margem.

O Auto-Refine mostra que isso funciona com um único modelo, sem dados de treinamento, sem RL. Mas há uma pega: os LLM são maus na auto-verificação em fatos concretos.

> Auto-Refina demonstra que o modelo é capaz de trabalhar, sem o treinamento de dados, sem o RL. Mas há uma armadilha: a capacidade de auto-verificação de LLM em hard facts é muito baixa.

Juntos, estes dois artigos definem o padrão 2026 para melhoria iterativa: gerar, verificar (externamente quando possível), refinar, parar quando o verificador passar.

> Estes dois artigos definem em conjunto o modelo de referência para a melhoria da geração de 2026: geração, verificação, verificação externa, como possível.

> **【中文解读】**O conceito central da auto-refinagem: um modelo que desempenha o papel de gerador, crítico, refinador. Mas o LLM em hard facts auto-verificação não é confiável. O programa de revisão da auto-refinagem é executado através de ferramentas externas.

## O conceito central.

### Auto-refinamento (Madaan et al., NeurIPS 2023)

Um LLM, três funções:

> Um LLM, três cargos:

```
generate(task)            -> output_0                          # 生成初始输出
feedback(task, output_0)  -> critique_0                        # 自我批评
refine(task, output_0, critique_0, history) -> output_1       # 根据批评精炼
feedback(task, output_1)  -> critique_1                        # 再次批评
refine(task, output_1, critique_1, history) -> output_2       # 再次精炼
...
stop when feedback says "no issues" or budget exhausted.       # 停止条件
```

Detalhe-chave:`refine`O artigo abla isto: queda de história e queda de qualidade acentuada.

> - Não .**【类比】**Auto-refinar 像写论文的"自改稿"流程:第一稿(genera)→ 通读找问题(feedback)→ 按问题改第二稿(refinar, mas para olhar para o primeiro稿和批注改,否则会重复同样错)→ 再找问题→再改──**关键**A cada refinamento, é necessário juntar o histórico e o lote para o modelo, caso contrário, o modelo "esquece o problema da rotina acima", e entra em um ciclo.

> ️ **【易错点】**常见 bug: apenas "上一轮输出" 给精炼, 没有反──**后果**Refinar 后的输出重新引入反见指出的问题,陷入"指出问题→改→再指出→再改"的死循环──**一行修复**- Não .`refine_prompt = task + output_0 + critique_0 + output_1 + critique_1 + ... + output_n` História deve ser totalmente transmitida.

> 关键细节:`refine`能看到完整历史所有前前的输出和批评因此不会重复错误──论文对此进行消融实验:删除历史记录后质量急剧下降──

Título: +20 melhorias absolutas em média em 7 tarefas (matemática, código, sigla, diálogo) incluindo GPT-4.

> 核心数据: 平均绝对提升 20 个百分点, incluindo GPT-4──无需训练──无需外部工具──单一模型──

### CRITA (Gou et al., arXiv:2305.11738, v4 fevereiro 2024)

A fraqueza da auto-refinagem: a etapa de feedback é a própria pontuação do LLM. Para as alegações factuais, esta é pouco confiável (uma alucinação muitas vezes parece convincente para o modelo que a produziu).`feedback(task, output)`com`verify(task, output, tools)`onde`tools`inclui:

> A fraqueza da auto-refinação:反步骤是LLM 给自己评分── para declarações de fato é inconfiável.`verify(task, output, tools)`替代   substituir`feedback(task, output)`, entre os `tools`Incluem:

- Um motor de busca de alegações factuais.
  Tradução do inglês para "factual declaration"
- Um intérprete de código para corretão de código.
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês
- Uma calculadora para aritmética.
  Tradução do inglês para tradução do inglês para inglês:
- Verificadores específicos de domínio (testes de unidade, verificadores de tipo, linters).
  Tradução do inglês para inglês: Domain-specific test-ficher (s)

O verificador produz uma crítica estruturada baseada nos resultados das ferramentas.

> O testador produz uma crítica estruturada baseada nos resultados das ferramentas.

Título: CRITIC supera a Auto-Refina em tarefas factuais porque a crítica é fundamentada. Em tarefas sem verificadores externos (escritura criativa, formatação), CRITIC reduz-se a Auto-Refina.

> 🤔 **【困惑】**P: 既然 CRITIC é mais refinado do que auto-refinado 强, por que não usar CRITIC? A: Porque CRITIC depende de ferramentas externas.**事实类用 CRITIC，创造类用 Self-Refine**- Não.

> 核心数据:CRITIC 超越Self-Refine, on factual tasks, because criticism is based on. ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒  ⇒ ⇒ ⇒   ⇒   ⇒     ⇒     ⇒      ⇒       ⇒       ⇒            ⇒                                                                                                                                                                                                                                                           

### A condição de parada

Duas formas comuns:

> 两种常见形式:

1. **Verifier passes.**Os testes externos apresentam sucesso. Preferido quando disponível (testes de unidade, verificador de tipo, afirmação de barragem).
   Tradução:**验证器通过。**Exterior Test returns success──在可用时优先单元测试、类型检查器、护断言)──
2. **No feedback issued.**Modelo diz "a saída está bem". Mais barato, mas não confiável; par com um limite máximo de iteração.
   Tradução:**无反馈发出。**模型说"输出没问题"──更便宜但不可靠;配合最大代次上限──

2026 padrão: combiná-los. "Pare se o verificador passar OR modelo diz bem E iterações >= 2 OR iterações >= max_iterations".

> 2026 年默认做法:组合使用──"Se o verificador passar, ou o modelo dizer que não há problema e que o número de vezes >= 2, ou o número de vezes >= máximo, então parar──"

### Otimizador de avaliação (Antropic, 2024)

O post de dezembro de 2024 da Anthropic nomeia isso como um dos cinco padrões de fluxo de trabalho.

> O artigo do Anthropic 2024 Year 12 月的文章将此命名为五种工作流模式之一──两个角色:

- O avaliador: marca a produção e produz uma crítica.
  O que é que é o resultado?
- Otimizador: revisa a saída dada a crítica.
  Tradução do inglês: 优化器:根据批评修改输出──

O sistema de avaliação de dados é um sistema de análise de dados que é um sistema de análise de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de

> 循环直到评估器通过──这是人类的框架下自精/CRITIC──人类的关键工程细节:评估器和优化器提示应该有实质性差异,以免模型只是皮图章──

### Os dispositivos de segurança de saída do SDK OpenAI Agents

O OpenAI Agents SDK envia este padrão como "gardalas de saída".`OutputGuardrailTripwireTriggered`Os guardrails podem chamar ferramentas (estilo CRITIC) ou ser funções puras (estilo Auto-Refinação).

> O OpenAI Agents SDK vai utilizar este modelo como "output protection" para fornecer informações sobre o seu produto.`OutputGuardrailTripwireTriggered`),输出被拒绝,Agent pode reprovar.

### 2026 armadilhas

- **Rubber-stamp loops.**O mesmo modelo fazendo geração e crítica com o mesmo estilo de prompt converge em "parece-me bem". Use instruções estruturalmente diferentes, ou um modelo mais pequeno e barato para a crítica.
  Tradução:**橡皮图章循环。**O mesmo modelo utiliza o mesmo estilo de apresentação de propostas e recebe críticas até "parece errado" (como "parece errado").
- **Over-refinement.**Cada passagem de refinamento adiciona latência e tokens. O orçamento 1-3 passa; depois disso, escala para revisão humana.
  Tradução:**过度精炼。**Cada refinamento aumenta o atraso e o token.
- **CRITIC on trivial tasks.**Se não houver um verificador externo, o CRITIC degenera para Auto-Refine; não pague a latência por um verificador de estúdio.
  Tradução:**在简单任务上使用 CRITIC。**Se não houver um verificador externo, o CRITIC 退化为自理化; não se deve pagar atrasos por um verificador.

## Construí-lo e realizei-o.
```figure
self-refine
```

## Construí-lo

`code/main.py`A verificação de dados é feita por um grupo de dados que são utilizados para verificar o formato de um objeto.

> `code/main.py`Em um trabalho de brinquedo, realizar Auto-refinamento e CRITIC: dado determinado tema gerar lista curta.

Componentes:

> 组件:

- `generate`- Produtor de roteiro.
  Tradução:`generate`脚本生成器──
- `feedback` Autocrítica de estilo LLM.
  Tradução:`feedback`LLM 风格自我批评──
- `verify_external` Verificador baseado de estilo CRITIC.
  Tradução:`verify_external`CRITA 风格定验器──
- `refine` reescreve a saída dada história.
  Tradução:`refine`根据历史重写输出──
- Condição de parada  passes de verificador ou max 4 iterações.
  O teste de teste é feito em quatro vezes.

- É o que é ?

> 运行:

```
python3 code/main.py
```

Compare as corridas Auto-Refina versus CRITIC. CRITIC pega um erro factual Auto-Refina omitido porque o verificador externo tem terra a auto-crítica não.

> Comparar Auto-Refinação e CRITA 运行──CRITA  Captured Self-Refinação 遗漏 fact errors, pois os testadores externos possuem uma base definida em que não há auto-críticas──

## Use-o com o framework implementado.

O avaliador-optimizador da Anthropic é este padrão em linguagem amigável à Claude. Os guardrails de saída do OpenAI Agents SDK são CRITIC-formados (guardrails podem chamar ferramentas). LangGraph envia um nó de reflexão que lê como Self-Refine. O Gemini 2.5 Computer Use do Google adiciona um avaliador de segurança por passo que é uma variante CRITIC: cada ação é verificada antes de se comprometer.

> O Antropic é um sistema de avaliação de dados que é usado pela Claude Friendly Language. O Output da SDK de Agentes OpenAI é de forma CRITICA. O LongGraph fornece um reflexo semelhante ao Self-Refine.

## Envia-o . Produto .

`outputs/skill-refine-loop.md`Configura um loop de avaliador-otimizador dado a forma da tarefa, disponibilidade do verificador e orçamento de iteração. Emite instruções para gerador, avaliador/verificador e optimizador, além de uma política de parada.

> `outputs/skill-refine-loop.md`De acordo com a forma de tarefa, a disponibilidade do verificador e o ciclo de configuração do orçamento do avaliador-otimizador, a entrada de dados, a sugestão do avaliador/verificador e do optimizador, bem como a estratégia de suspensão.

## Exercícios.

1. Execute o brinquedo com max_iterations=1.
   中文翻译:用 max_iterations=1 运行――CRITIC  ainda há ajuda?
2. Substitua o verificador externo por um barulhento (random 30% falsos positivos). O que faz o loop? Esta é a realidade de 2026 da maioria das pilhas de guarda-roupa.
   O que fazer em um ciclo de negociações? É a realidade da maioria dos países em desenvolvimento em 2026.
3. Implementar uma variante de "generação crítica em diferentes modelos": grandes modelos geram, pequenos modelos criticam.
   Tradução do inglês para tradução do inglês: implementar " diferentes modelos de produção- crítica "变体:大模型生成,小模型批评――比同模型更好吗?
4. Leia a secção 3 CRITIC (arXiv:2305.11738 v4).
   Tradução do inglês para tradução do inglês: read CRITIC 第 3 節。说出三种验证工具类别并各举一例──
5. Mapa do SDK de Agentes OpenAI `output_guardrails`O que é que o SDK está errado e o que é que está certo?
   中文翻译:将 OpenAI Agents SDK 的`output_guardrails`O que é que está a fazer bem, o que não está a fazer bem?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Self-Refine | "LLM that fixes itself" / "自我修复的 LLM" | Generate -> feedback -> refine loop in one model, with history / 一个模型内的生成→反馈→精炼循环，带历史记录 |
| CRITIC | "Tool-grounded verification" / "工具锚定验证" | Replace feedback with an external verifier (search, code, calc, tests) / 用外部验证器替代反馈 |
| Evaluator-Optimizer | "Anthropic workflow pattern" / "Anthropic 工作流模式" | Two roles — evaluator scores, optimizer revises — looped to convergence / 两个角色——评估器评分、优化器修改——循环到收敛 |
| Output guardrail | "Post-hoc check" / "事后检查" | OpenAI Agents SDK validator that runs after an agent produces output / Agent 输出后运行的验证器 |
| Verify step | "Critique phase" / "批评阶段" | The load-bearing decision: grounded or self-rated / 核心决策：基于外部工具还是自我评价 |
| Refine history | "What the model already tried" / "模型已尝试的内容" | Prior outputs + critiques prepended to refine prompt; drop and quality collapses / 先前输出+批评前置到精炼提示；去掉则质量崩溃 |
| Rubber-stamp loop | "Self-agreement failure" / "自我认同失败" | Same-prompt critique returns "looks good"; fix with structurally different prompts / 相同提示批评返回"看起来不错"；用结构性不同的提示修复 |
| Stop condition | "Convergence test" / "收敛测试" | Verifier passes OR no feedback AND iteration cap; never single-condition / 验证器通过或无反馈且达到迭代上限；永不使用单一条件 |

## Mais leitura 延伸阅读

- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) o papel canônico
  中文翻译:Self-Refine 经典论文自我精炼代改进。
- [Gou et al., CRITIC (arXiv:2305.11738)](https://arxiv.org/abs/2305.11738) Verificação baseada em ferramentas
  Tradução do português:Critic 工具 定验证──
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) padrão de fluxo de trabalho de avaliador-optimizador
  Tradução do inglês para "Antropic 关于构建有效代理的指导评估器-优化器工作流模式").
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) barris de saída como verificadores em forma CRITIC
  中文翻译:OpenAI Agents SDK 文档输出护作为Critic 形式的验证器──
