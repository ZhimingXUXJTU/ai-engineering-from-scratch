# O Agente Autônomo de Codagem Paisagem (2026)

> O banco SWE Verified passou de 4% para 80,9% em menos de três anos. O mesmo Claude Sonnet 4.5 marcou 43,2% no SWE-agent v1 e 59,8% no Cline autónomo  o andaime em torno do modelo agora importa tanto quanto o próprio modelo. OpenHands (anteriormente OpenDevin) é a plataforma mais ativa licenciada pelo MIT e seu loop CodeAct executa ações Python diretamente em uma caixa de areia em vez de chamadas de ferramentas JSON. Os números de cabeçalhos ocultam um problema metodológico: 161 das 500 tarefas verificadas de banco SWE exigem apenas uma alteração de linha de 12, e o banco SWE Pro (10 tarefas de linha superior) fica em 2359% para os mesmos modelos de fronteira.

> **【中文解读】**SWE-bench Verified em não menos de três anos de 4% para 80,9%。 o mesmo Claude Sonnet 4.5 em SWE-agent v1 ganhou 43,2%, em Cline autônomo ganhou 59,8% o modelo em torno de脚手架架现在和模型本身一样重要。 OpenHands(前 OpenDevin) é a plataforma de licença MIT mais ativa, cujo código-ácito ciclo executa diretamente em caixa Python 动作而不是 JSON 工具调调用。

> **【拓展：脚手架 > 模型】**A curva de 2022-2026 mostra que a capacidade de codificação do agente aumenta de três fontes complexas: melhor modelo base, melhor scripting frame (CodeAct, reflexo, ciclo de verificadores)  melhor scripting frame (Verified, eliminando ruído)  Diferença de 16,6 pontos absolutos entre modelos iguais em diferentes scripting frame (s)  modelo base é um componente, ciclo é apenas um produto  É por isso que o agente não pode ser escolhido apenas para ver a lista de modelos 

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, CodeAct vs JSON tool-call comparison) | **语言:** Python（标准库，CodeAct vs JSON 工具调用对比）
**Prerequisites:** Phase 14 · 07 (Tool use), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 14 · 07（工具使用），Phase 15 · 01（长程 Agent）
**Time:** ~45 minutes | **时间:** ~45 分钟

> - Não .**【前置】**學本節前請先掌握:Fase 14·07(工具调用) 、Fase 14·30+(工作台 Agente 实践) 、Fase 15·01(长程 Agent) ⋅本节是 2026 年编码 Agent 全景图选型必读──
> - Não .**【类比】**选编码 Agent = "选车" em vez de "选发动机"。同一发动机(Claude Sonnet 4.5)装在不同车上(SWE-agent vs Cline) velocidade diferença 16 个百分点。脚手架(检索层、规划器、沙箱、edit-verify 循环) é apenas um produto, o modelo é apenas um componente。 portanto, não olhe apenas para a lista de modelos, para ver "My task+my脚手架" de ponta a ponta confiabilidade。
> ️ **【易错点】**Olha SWE-bench Verificado 分数选 Agent = 被基准骗了──500 个任务里 161 个只需要1-2 行修改(容易),看 SWE-bench Pro(10+ 行真实任务) 分数才有参考价值──修复:选 Agent 前用自己代码库的真实问题 测试,而不是看营销基准──

## O problema é o problema da introdução

> **【中文解读】**编码代理景观 é um dos mais rápidos anos de mudança em 2025-2026 应用领域. Os principais jogadores incluem Claude Code, Cursor, GitHub Copilot, Devine, Windsurf, etc.

> **【拓展：coding agent landscape】**2026年编码 Агентт的竞争格局:(1) Claude CodeAnthropic's Autonomous Coding Agent,支持全开发、Git 操作和终端命令执行;(2) Cursor基于 VS Code的 AI 编辑器,强调人机协作;(3) DevinCognition AI's Full Autonomous Coding Agent,可以独立完成开发任务;(4) Windsurf(原 Codeium) AI 优先 IDE──SWE-bench 上的表现是主要竞争指标;;

A pergunta certa é: em uma distribuição de tarefas que corresponda ao meu trabalho, com o andaime que vou executar na produção, que confiabilidade de ponta a ponta eu obtiver?

> A questão verdadeira é: na distribuição de tarefas que corresponde ao meu trabalho, usando a escrivaninha que eu vou usar na produção, o que posso obter de extremo a extremo de confiabilidade?

Entre 2022 e 2026, o campo aprendeu que o andaime  a camada de recuperação, o planejador, a caixa de areia, o loop de edição-verificação, o formato de feedback  é carregável. Claude Sonnet 4.5 no SWE-agent v1 marcou 43,2% no banco SWE Verified; o mesmo modelo dentro do andaime autônomo de Cline marcou 59,8%. 16.6 pontos absolutos de diferença, o mesmo peso. O modelo base é um componente; o ciclo é o produto.

> 2022 até 2026 anos, áreas de aprendizagem de guião  revisão de camadas, planejadores, caixas de água  ciclo de verificação de edição  contraformação  é suportada ∙ Claude Sonnet 4.5 em SWE-agent v1  SWE-bench Verificado obtém 43,2%; o mesmo modelo em Cline independente guião  dentro de 59.8%  O mesmo peso diferença 16.6  pontos absolutos ∙ o modelo base é componente; o ciclo é produto ∙

> **【中文解读】**Esta secção apresenta o conceito e o método de implementação do Agente de IA. O Agente é um sistema autónomo impulsionado pelo LLM, capaz de observar o ambiente, pensar decisões, executar a ação e ciclo de vida até a conclusão do objetivo.

O problema é que a saturação de referência oculta regressões.

> O problema é a base e a ocultação do regresso.

O SWE-bench Verified é próximo de saturado, e a cauda de tarefa fácil (161 das 500 tarefas que exigem ≤ 2 linhas) aumenta as pontuações. A qualidade do mundo real é melhor medida em distribuições como o SWE-bench Pro (10+ mudanças de linhas), onde os mesmos líderes ainda estão em 2359%.

> SWE-bench Verificado 接近和,简单任务尾部(500 个任务中 161 个需要 ≤2 行) 拉高顶级分数──现实世界质量在 SWE-bench Pro(10+ 行变更)等分布上测量更好,同领先者仍然只有23-59%──

## O conceito central.

### SWE-bench, um parágrafo.

SWE-bench (Jimenez et al.) toma problemas reais do GitHub com patches de verdade no solo e pede a um agente para produzir um patch que faz com que o conjunto de testes passe. SWE-bench Verified (OpenAI, 2024) é um subconjunto de 500 tarefas curado pelo homem com as tarefas ambíguas e quebradas removidas. SWE-bench Pro é o sucessor mais difícil de tarefas que exigem 10+ linhas de mudança, onde os agentes fronteiriços atuais estão em 2359%.

> SWE-bench(Jimenez 等人) 带真实补丁的真实 GitHub issue, requiring Agent 产生使测试套件通过补丁──SWE-bench Verified(OpenAI,2024) é um conjunto de 500 missões de planejamento artificial, que remove as missões模糊和损坏的──SWE-bench Pro é mais difícil de sucessor 需要 10+ 行变更任务,当前前沿 Agent 在 23-59%──

### O que a curva 2022 → 2026 realmente mostra.

- **2022**A partir de 1 de Janeiro de 1993, a Comissão apresentou um relatório sobre a aplicação do princípio da igualdade de oportunidades entre os Estados-Membros.
  Tradução:**2022**A pesquisa foi realizada em um estudo de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesquisa de pesada.
- **2024**: GPT-4 + andamios de estilo Devin em ~ 14%; agente SWE em ~ 12%.
  Tradução:**2024**GPT-4 + Devin 式脚手架约 14%;SWE-agent 约 12%──
- **2025**Claude 3.5/3.7 Sonnet dentro de Aider e agente SWE empurrar para a faixa de 4055%.
  Tradução:**2025**O que é o "SONET" em Aider e SWE-agent?
- **2026**A lista de classificação da Epoch AI acompanha esta ação ao vivo.
  Tradução:**2026**:Claude Sonnet 4.5 和前沿竞争者在SWE-bench Verified 上 70-80%+──Epoch AI's排名实时跟踪──

A inclinação provém de três fontes de composição: melhores modelos base, melhor andamento (CodeAct, reflexão, circuitos de verificação) e melhores referências (Removimento de ruído verificado).

> 斜率来自三个复合源:更好的基础模型、更好的脚手架(CodeAct、反思、验证器循环)、更好的基准(Verified 去除噪声)。

### CodeAct vs JSON ferramenta ligações .

OpenHands (All-Hands-AI, arXiv:2407.16741, anteriormente OpenDevin) fez uma aposta arquitetônica específica: em vez do modelo emitindo chamadas de ferramenta JSON que um host decodifica e executa, o modelo emite código Python e um kernel de estilo Jupyter executa-o em uma caixa de areia.

> OpenHands(All-Hands-AI,arXiv:2407.16741,前 OpenDevin) sob uma estrutura específica: o modelo não é mais emitido por um servidor de código de execução JSON 工具调用, mas é emitido por Python 代码, executado por Jupyter 风格内核在沙箱中.

O compromisso:

> 权衡:

- **JSON tool calls**: cada ação é de uma vez; fácil de auditoria; composicionalidade limitada; segura por padrão porque cada chamada passa por um validador explícito.
  Tradução:**JSON 工具调用**A primeira fase é a de um processo de verificação de dados.
- **CodeAct**: uma ação pode ser um programa inteiro; composição; requer uma caixa de areia endurecida (OpenHands usa isolamento Docker); modos de falha incluem qualquer coisa que o tempo de execução da caixa de areia permite.
  Tradução:**CodeAct**O sistema pode ser executado em um único modo: um movimento pode ser todo o processo; pode ser combinado; precisa ser consolidado em um box;

As duas arquiteturas estão em produção. CodeAct é dominante em plataformas abertas (OpenHands, smolagents). As chamadas de ferramentas JSON continuam a ser dominantes em serviços gerenciados (Agentes Administrados Antropicos, Assistentes OpenAI) onde o provedor controla o executor.

> 两种架构都在生产中.CodeAct 在开放平台(OpenHands、smolagents) 主导.

### Escafadas na paisagem de 2026

| Scaffold | License | Execution model | Notable property |
|---|---|---|---|
| 脚手架 | 许可 | 执行模型 | 显著属性 |
| OpenHands (OpenDevin) | MIT | CodeAct in Docker | Most active open platform; event-stream replayable |
| OpenHands（OpenDevin） | MIT | Docker 中 CodeAct | 最活跃开放平台；事件流可重放 |
| SWE-agent | MIT | Agent-Computer Interface (ACI) | First end-to-end SWE-bench scaffold |
| SWE-agent | MIT | Agent-计算机接口（ACI） | 首个端到端 SWE-bench 脚手架 |
| Aider | Apache-2 | edit-via-diff in local repo | Minimal scaffold, strong regression stability |
| Aider | Apache-2 | 本地仓库 edit-via-diff | 最小脚手架，强回归稳定性 |
| Cline | Apache-2 | VS Code agent with tool policy | Highest-scoring open scaffold on Sonnet 4.5 |
| Cline | Apache-2 | 带工具策略的 VS Code Agent | Sonnet 4.5 上得分最高的开放脚手架 |
| Devin (Cognition) | Proprietary | Managed VM + planner | First "AI software engineer" product category |
| Devin（Cognition） | 专有 | 管理 VM + 规划器 | 首个"AI 软件工程师"产品类别 |
| Claude Code | Proprietary | Permission modes + routines | Lesson 10 covers the agent loop in detail |
| Claude Code | 专有 | 权限模式 + 例程 | 第 10 课详细介绍 Agent 循环 |

### Porque é que o andaime domina?

Uma corrida de codificação é uma trajetória de longo horizonte (Lessão 1).

> 编码运行是长程轨迹 (第 1 课) ⋅可靠性跨步骤复合 (可靠性跨步骤复合) ⋅脚手架买入分数的三个地方:

1. **Retrieval**O ACI do SWE-agent, o índice de arquivos do OpenHands e o repo-map do Aider atacam tudo isso.
   Tradução:**检索**O que é que é que é o que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é
2. **Verifier loop**A execução de testes, a leitura de pistas e a repetição são 10 pontos delta no banco SWE.
   Tradução:**验证器循环**O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?
3. **Failure containment**O mesmo modelo com e sem um ciclo de verificação parece ser dois produtos diferentes.
   Tradução:**失败遏制**O mesmo modelo tem e não tem um ciclo de comprovador parecem dois produtos diferentes.

### Saturação de referência e distribuição real.

Os autores da OpenHands e da Epoch AI ambos sinalizam que o SWE-bench Verified tem uma cauda fácil: 161 das 500 tarefas precisam apenas de 12 linhas de mudança. As pontuações altas são impulsionadas em parte por essa cauda. O SWE-bench Pro restringe-se a 10+ mudanças de linhas e retorna pontuações na faixa de 2359% mesmo para sistemas de fronteira. Sua distribuição de produção é quase certamente mais próxima do Pro do que do Verified.

> OpenHands Autor e Epoch AI todos marcados SWE-bench Verified 有简单尾部:500 个任务中161 个只需要1-2 行变更──高分部分由该尾部驱动──SWE-bench Pro 限制10+ 行变更,即使前沿系统也返回23-59% 范围──

Implicação para a escolha de um agente: executar um subconjunto Pro-like de seu próprio backlog de bugs. A pontuação que importa é a pontuação em tarefas representativas do que você envia.

> 选择 Agent 的含义: em seu próprio bug 积压上运行 Pro 类子集── 重要分数是代表你发布任务的分数──

## Use-o com o framework implementado.
```figure
a5-scaffold-delta
```

## Usá-lo

`code/main.py`Comparar dois andares de agentes de brinquedo numa distribuição fixa de mini-tarefas:

> `code/main.py`Em uma distribuição fixa de missões, compare dois brinquedos:

1. A.**JSON tool-call**Equipamento que faz uma ação por virada.
   Tradução:**JSON 工具调用**- Não, não.
2. A.**CodeAct**Equipamento que pode emitir um pequeno fragmento Python por ação.
   Tradução:**CodeAct**O que é que é que é?

Ambos usam um "modelo" de estúdio (regras deterministas), de modo que a comparação isola o andaime da qualidade do modelo.

> 两者使用存根"模型" (Regulamento de Determinação) para comparar os quadros de comando e o modelo de qualidade de separação.

## Envia-o . Produto .

`outputs/skill-scaffold-audit.md`ajuda a auditar um esquadrão de agentes de codificação proposto antes da adoção: qualidade de recuperação, presença de verificadores, isolamento de caixa de areia e adequação de referência à distribuição.

> `outputs/skill-scaffold-audit.md` help you in adopting pre audit proposal 编码 Agent 脚手架:检索质量、验证器存在、沙箱隔离、基准到分布契合──

## Exercícios.

1. Corra .`code/main.py`Quantas voltas cada andaime faz no mesmo conjunto de tarefas? Qual é o raio de explosão por ação de cada um?
   Tradução: 运行`code/main.py`Quantas rodas cada um dos quadros tem no mesmo conjunto de tarefas?

2. Leia o artigo OpenHands (arXiv:2407.16741). O artigo argumenta que o CodeAct supera as chamadas de ferramenta JSON em tarefas complexas. Identifique um modo de falha que o artigo reconhece e escreva uma frase sobre quando esse modo dominaria na produção.
   O código-ácito é um código-fonte que é usado para executar um processo de identificação de um documento.

3. Escolha uma tarefa do seu backlog de bugs que exigiria mais de 10 linhas de mudança em dois arquivos. Estima a probabilidade de sucesso de ponta a ponta para um modelo de fronteira sob (a) chamadas de ferramentas JSON e (b) CodeAct. Justifique a lacuna.
   Tradução do idioma japonês: de seu bug 积压中选一个需要跨两文件 10+ 行变更的任务──估算前沿模型在 (a) JSON 工具调用和 (b) CodeAct 下的端到端成功概率──论证差距──

4. O banco SWE Verified tem 161 tarefas de um único arquivo, 12 linhas. Construa uma pontuação que as exclui. Como a tabela de classificação mistura?
   O banco de dados da SWE verificou que existem 161 documentos únicos.

5. Leia "Introdução de SWE-bench Verified" (OpenAI). Explique a metodologia específica usada para remover tarefas ambíguas e nomeie uma categoria que a curadoria não veria.
   中文翻译:阅读"Introdução de SWE-bench Verified" (OpenAI) 』

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| SWE-bench | "Coding benchmark" | Real GitHub issues with ground-truth patches and test suites |
| SWE-bench | "编码基准" | 带真实补丁和测试套件的真实 GitHub issue |
| SWE-bench Verified | "Cleaned subset" | 500 human-curated tasks, easier-tail present |
| SWE-bench Verified | "清理的子集" | 500 个手工策划任务，存在简单尾部 |
| SWE-bench Pro | "Harder subset" | 10+ line changes; frontier sits at 23–59% |
| SWE-bench Pro | "更难的子集" | 10+ 行变更；前沿在 23-59% |
| CodeAct | "Code-as-action" | Agent emits Python; Jupyter-style kernel executes in sandbox |
| CodeAct | "代码即动作" | Agent 发出 Python；Jupyter 风格内核在沙箱执行 |
| JSON tool call | "Function calling" | Each action is a structured JSON payload validated before execution |
| JSON 工具调用 | "函数调用" | 每动作是执行前验证的结构化 JSON 负载 |
| Scaffold | "Agent framework" | Retrieval + planner + executor + verifier loop around the base model |
| 脚手架 | "Agent 框架" | 围绕基础模型的检索 + 规划器 + 执行器 + 验证器循环 |
| ACI (Agent-Computer Interface) | "SWE-agent's format" | Command set designed for LLM ergonomics, not human shells |
| ACI（Agent-计算机接口） | "SWE-agent 格式" | 为 LLM 人体工程学设计的命令集，非人类 shell |
| Verifier loop | "Test-and-retry" | Run tests, read output, revise patch; biggest non-model reliability gain |
| 验证器循环 | "测试并重试" | 运行测试、读输出、修订补丁；最大非模型可靠性增益 |

## Mais leitura 延伸阅读

- [Jimenez et al. — SWE-bench](https://www.swebench.com/) o indicador de referência e a metodologia originais.
  Tradução do inglês para o inglês:
- [OpenAI — Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) como foi construído o subconjunto curado.
  中文翻译:策划子集如何构建──
- [Wang et al. — OpenHands: An Open Platform for AI Software Developers](https://arxiv.org/abs/2407.16741) Arquitetura CodeAct e design de fluxo de eventos.
  Tradução do inglês:CodeAct 架构和事件流设计.
- [Epoch AI — SWE-bench leaderboard](https://epoch.ai/benchmarks)- As pontuações em directo.
  Tradução do inglês:
- [Anthropic — Measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) enquadramento de confiabilidade do agente codificador de longo horizonte.
  Tradução do inglês:长程编码 Agent 可靠性框架──
