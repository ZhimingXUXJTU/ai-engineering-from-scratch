# Biblioteca de habilidades e aprendizagem ao longo da vida (Voyager)

> Voyager (Wang et al., TMLR 2024) trata o código executável como uma habilidade. Habilidades são nomeadas, recuperáveis, compostas e refinadas por feedback ambiental. Esta é a arquitetura de referência para habilidades SDK do Claude Agent, skillkit e o padrão de biblioteca de habilidades de 2026.

> **【中文解读】**A Voyager vai executar o código como habilidade. A habilidade é denominada, pesquisável, coletável, e através do ambiente, é a estrutura de referência do modelo de habilidades SDK e de habilidades de 2026 da Agência Claude.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta Blocks) | **前置知识:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta 块)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Nomear os três componentes da Voyager  currículo automático, biblioteca de habilidades, incitação iterativa  e o papel de cada um.
  Tradução do inglês para o inglês:                                                                                                                                                                                                                                                          
- Explica porque a Voyager faz o código do espaço de ação, não os comandos primitivos.
  Tradução do inglês para tradução do inglês: Explain Why Voyager Will Move Space Set for Code instead of Original Order.
- Implementar uma biblioteca de habilidades stdlib com registro, recuperação, composição e refinamento de falhas.
  Tradução do inglês para o inglês: using standard library to implement with registration, checkout, assemblage and failure drive refinement.
- Mapa do padrão da Voyager para as habilidades do SDK do Agente Claude 2026 e o ecossistema do skillkit.
  Tradução do inglês para tradução do inglês:将 Voyager 模式映射到2026年Claude Agent SDK skills 和 skillkit 生态系统。

## O problema é o problema da introdução

Os agentes que reconstruem todas as capacidades de zero em cada sessão fazem três coisas erradas:

> A cada reunião, o agente com capacidade de reconstrução de propriedades vai fazer três coisas erradas:

1. **Waste tokens.**Cada tarefa re-excita o mesmo raciocínio.
   Tradução:**浪费 token。**Cada tarefa reinicia o mesmo argumento.
2. **Lose progress.**Uma correcção aprendida na sessão A não se transfere para a sessão B.
   Tradução:**丢失进展。**Em reunião A, a correção que está sendo feita não será transferida para reunião B.
3. **Fail on long-horizon composition.**As tarefas complexas precisam de hierarquias de capacidade; as instruções de um tiro não podem expressá-las.
   Tradução:**在长程组合上失败。**As tarefas complexas exigem níveis de capacidade; as simples dicas não podem expressá-las.

> **【中文解读】**技能库(Skill Libraries) Origem de Voyager (Wang et al., 2023)  Um agente de exploração e aprendizagem autônoma em Minecraft.

A resposta da Voyager: tratar cada capacidade reutiliável como um pedaço de código nomeado armazenado numa biblioteca, recuperável por semelhança, composta com outras habilidades, e refinada por feedback de execução.

> A resposta do Voyager: vai considerar cada capacidade reutiliável como um bloco de código de nome armazenado na arquivo, pode ser pesquisado por semelhança, pode ser combinado com outras habilidades, e pode ser executado por meio de reformulação.

> **【拓展：Voyager 的技能库概念已被 2026 年的编码 Agent 普遍采用】**CLAUDE.md, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, Cursor, e Cursor, e Cursor, e Cursor, são os quais são os usuários e outros outros outros outros outros são os usuários de sua companheiros que foram realizados por mais ou outros em sua companhias, e outros, e outros, e outros, e outros, por mais mais mais mais ainda são capazes, por mais ou até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até até

> - Não .**【前置】**需要先掌握:Fase 14·05(Self-Refine/CRITIC) Voyager's "代提示机制"本质是 Self-Refine + 环境反;Fase 14·07(MemGPT) 技能库的检索机制类似于档案记忆的语义搜索──还需要理解"代码即行动"的概念,区别于"文本即行动"──

## O conceito central.

### Três componentes

A Voyager (arXiv:2305.16291) estrutura um agente em torno de:

> Voyager ((arXiv:2305.16291) em torno dos seguintes três componentes

1. **Automatic curriculum.**Um proponente motivado pela curiosidade escolhe a próxima tarefa com base no conjunto de habilidades atual do agente e no estado do ambiente.
   Tradução:**自动课程。**O agente está em um grupo de habilidades e o seu ambiente.
2. **Skill library.**Cada habilidade é um código executável. Novas habilidades são adicionadas quando uma tarefa é bem sucedida. Habilidades são recuperadas por semelhança entre consulta e descrição.
   Tradução:**技能库。**Cada habilidade é executável. Quando a tarefa é bem sucedida, adicione novas habilidades.
3. **Iterative prompting mechanism.**Em caso de falha, o agente recebe erros de execução, feedback do ambiente e saída de auto-verificação, e depois aperfeiçoar a habilidade.
   Tradução:**迭代提示机制。**失败时,Agent 接收执行错误、环境反和自我验证输出,然后精炼技能──

A avaliação do Minecraft (Wang et al., 2024): 3.3x mais itens únicos, 8.5x mais ferramentas de pedra, 6.4x mais ferramentas de ferro, 2.3x mais longo cruzamento do mapa versus linhas de base. Os números são específicos do Minecraft, mas o padrão transfere.

> Minecraft  avaliação(Wang 等人,2024):3.3 倍更多独特物品、8.5 倍更快石制工具、6.4 倍更快铁制工具、2.3 倍更长地图遍历对比基线──数字是Minecraft 特定的,但模式可迁移──

### Espaço de ação = código

A maioria dos agentes emitem comandos primitivos, a Voyager emite funções JavaScript.

> A maioria dos agentes 发发出原始命令──Voyager 发发出 JavaScript 函数──一个技能是:

```
async function craftIronPickaxe(bot) {
  await mineIron(bot, 3);
  await mineStick(bot, 2);
  await placeCraftingTable(bot);
  await craft(bot, 'iron_pickaxe');
}
```

Composto por sub-habilidades, armazenado com teclas na descrição e embutida, recuperado como um programa, não como um prompt.

> Por meio de um conjunto de habilidades.

Esta é a habilidade do SDK do Agente Claude 2026: um pedaço de código chamado e recuperável, mais instruções que o agente carrega à demanda.

> É o ano de 2026 Claude Agente SDK habilidade: um bloco de código identificado e pesquisável, adicionado a um comando de carga por agente.

> - Não .**【类比】**技能库像程序员的"代码片段库"或IDE snippets: você não precisa de cada vez escrever Python para redesenhar `read_file`Função,调用已有的就行;;Insight of Voyager is to let Agent also do thisIt"invented" a"one"" mining" code, stored into the library, next time again to dig iron mine on direct inspection调用;;**关键**- Não .**代码**Não**提示词**代码可以被环境执行、获得明确反,提示词不行──

### Recuperação de competências

A nova tarefa é fazer um picáxe de diamante.

> Novos trabalhos de produção de ouro

1. Incorporar a descrição da tarefa.
   Tradução do inglês:
2. Pergunto à biblioteca de habilidades para habilidades semelhantes.
   Tradução do inglês para "Question Skills"
3. Retira-se`craftIronPickaxe`- Não .`mineDiamond`- Não .`placeCraftingTable`etc.
   Tradução do português:`craftIronPickaxe`- Não.`mineDiamond`- Não.`placeCraftingTable`E assim...
4. Compõe a nova habilidade a partir de primitivas recuperadas + nova lógica.
   Tradução do inglês para o inglês: from检索到的原语 + 新逻辑组合新技能──

Este é o padrão de implementação dos recursos MCP (Fase 13) e das competências SDK do agente: recuperação sobre uma superfície de conhecimento/código, focada na tarefa atual.

> É o MCP 资源(Fase 13) e o SDK de Agente 模式 实现的模式:在知识/代码表面上检索, limitada às tarefas atuais。

### Refinamento iterativo

O circuito de feedback da Voyager:

> O ciclo de viagem:

1. O agente escreve uma habilidade.
   Tradução do inglês:Agent 编写技能──
2. A habilidade corre contra o ambiente.
   Tradução do inglês: skill dans环境中运行.
3. Um dos três sinais retorna:`success`- Não .`error`(com rastreamento de pilhas), `self-verification failure`- Não .
   Tradução do inglês:`success`- Não.`error`(带堆跟踪)`self-verification failure`- Não.
4. O agente reescreve a habilidade usando o sinal como contexto.
   Tradução do inglês para tradução inglesa:
5. A seguir até o sucesso ou o máximo de rodadas.
   Tradução do inglês para Chinês: ciclo até o sucesso ou alcançar a maior rota de vezes.

É o Auto-Refine (Lessão 05) aplicado à geração de código com verificação baseada no ambiente.

> ️ **【易错点】**Não se pode esquecer que o que é um "failure" é um "failure" que se resume a um "failure" que se resume a um "failure".**后果**A versão antiga do trabalho original foi perdida, a próxima revisão foi feita com uma nova versão de bug.**一行修复**: skills库用版本化 key (conhecimento de conhecimentos)`craft_pickaxe_v3`), fracassou quando nova versão, não cobre a versão antiga; apenas auto-verificação 通過才标记为`latest`- Não.

> É Auto-Refinação (§5) é aplicada em sistemas de código de avaliação ambiental (§5) é utilizada como ferramenta externa como um teste de avaliação (§5) é aplicada como um teste de avaliação.

### Currículo e exploração

O módulo de currículo da Voyager propõe tarefas como "construir um abrigo perto do lago" com base no que o agente tem e o que ainda não fez.

> 🤔 **【困惑】**P: A "habilidade" do Voyager é JavaScript 代码" Por que não Python? é Minecraft Mineflayer API 限制? A: 部分是。Mineflayer é Node.js 库, então o código deve ser JavaScript。 mas a causa mais profunda é:**代码作为动作空间必须可执行** linguagem não é importante, o importante é "canja não pode ser executado diretamente pelo ambiente e retornar o sucesso/sucesso sinal"

> Modulo de curso de Voyager baseado em Agente contato já existente e ainda não concluído para apresentar tarefas, como "Construir um abrigo no lago"

Para os agentes de produção, isso se traduz em um operador de "o que falta": dada a biblioteca de habilidades atual e um domínio, quais habilidades ainda não cobrimos?

> Para o Agente de Produção, isso se traduz em um operador "deficiente": dado o banco de habilidades e áreas atuais, quais habilidades ainda não cobrimos?

### Onde este padrão vai mal

- **Skill library rot.**A mesma habilidade adicionada 10 vezes com descrições ligeiramente diferentes. Adicionar deduplicação na escrita; recuperação retorna apenas uma.
  Tradução:**技能库腐化。**A mesma habilidade usa um pouco de descrição diferente adicionar 10 vezes.
- **Composed-skill drift.**A habilidade dos pais depende de uma criança que foi refinada.
  Tradução:**组合技能漂移。**A habilidade do pai depende de crianças é refinada.
- **Retrieval quality.**A recuperação de vetores sobre descrições de habilidades degrada-se à medida que a biblioteca cresce para além de algumas centenas.`category=tooling`").
  Tradução:**检索质量。**O volume de pesquisa de habilidades na descrição de um banco de dados cresceu mais de algumas centenas de vezes.`category=tooling`"Ámbito de atuação"

## Construí-lo.
```figure
voyager-skills
```

## Construí-lo

`code/main.py`Implementa uma biblioteca de habilidades stdlib:

> `code/main.py`Utilizando o padrão de base para a realização de um padrão de base de habilidades:

- `Skill` nome, descrição, código (como cadeia), versão, tags, dependências.
  Tradução:`Skill`名称、描述、代码(字符串) 、版本、标签、依赖──
- `SkillLibrary` registar, procurar (superposição de tokens), compor (tipologia topológica de deps) e refinar (bomba de versão na atualização).
  Tradução:`SkillLibrary`注册、搜索(token 重叠)、组合(依赖的拓排序) 和精炼(更新时版本递增)
- Um agente com roteiro que registra três habilidades primitivas, compõe uma quarta, atinge um fracasso e aperfeiçoia.
  Tradução do inglês para o inglês: Register Three Original Skills 组合第四个 遇到失败并精炼的脚本 Agent。

- É o que é ?

> 运行:

```
python3 code/main.py
```

O rastro mostra escritos da biblioteca, recuperação, composição, uma execução falhada e um refinamento v2 do ciclo de Voyager de ponta a ponta.

> 轨迹显示库写入、检索、组合、一次失败执行和 v2 精炼Voyager's end to end loop──

## Use-o com o framework implementado.

- **Claude Agent SDK skills**(Antropico)  a referência de 2026: cada habilidade tem uma descrição, código e instruções; carregado a pedido durante uma sessão de agente.
  Tradução:**Claude Agent SDK skills**(Antropico) 2026 ano referência: cada habilidade tem descrição、代码和指示;
- **skillkit**(npm: skillkit)  Gestão de competências entre agentes para 32+ agentes de codificação de IA.
  Tradução:**skillkit**(npm: skillkit) 32+ AI 编码 Agente 技能管理──
- **Custom skill libraries** Específico de domínio (habilidades SQL para agentes de dados, habilidades Terraform para infra-agentes).
  Tradução:**自定义技能库** domínio específico DATA Agent  SQL skills、 infraestrutura 技能)
- **OpenAI Agents SDK `tools`** no final inferior; cada ferramenta é uma habilidade leve.
  Tradução:**OpenAI Agents SDK `tools`**低端; cada ferramenta é uma habilidade de nível leve.

## Envia-o . Produto .

`outputs/skill-skill-library.md`gera uma biblioteca de habilidades em forma de Voyager com registro, recuperação, versão e refinamento conectado para qualquer tempo de execução de alvo.

> `outputs/skill-skill-library.md`A base de habilidades de forma Voyager, embutida em registro, pesquisa, versão e refinamento, adequada para qualquer objetivo de execução.

## Exercícios.

1. Adicionar um detector de ciclo de dependência para `compose()`O que acontece quando a habilidade A depende de B que depende de A?
   Tradução:`compose()`Controle de ciclo de dependência. Habilidade A Depende B, B Depende A. O que acontece quando A? erro ou aviso?
2. Implementar a versão por habilidade de pinagem.`crafting@1`, um refinamento para `crafting@2`Não deve silenciosamente atualizar o pai.
   Tradução do inglês em japonês:                                                                                                                                                                                                                                                           `crafting@1`时,`crafting@2`O meu trabalho não é fazer isso.
3. Substitua a recuperação de token-overlap com transformadores de frases embutidos (ou um impl stdlib BM25).
   O que é o "tempo de recuperação" de uma frase?
4. Adicionar um agente de "curriculum": dada a biblioteca atual e uma descrição de domínio, propor 5 habilidades faltantes.
   Tradução do inglês para o inglês: Add"course"Agente:给定当前库和领域描述,提出 5 个缺失技能──每周调用一次──
5. Leia os documentos de habilidades do SDK do Claude Agent da Anthropic, e transporte a biblioteca de brinquedos para o esquema de habilidades do SDK.
   Chinese Language Translation: read Anthropic's Claude Agent SDK skill 文档──将玩具库移植为 SDK's skill 模式──可发现性有什么变化?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Skill | "Reusable capability" / "可复用能力" | Named chunk of code + description, retrievable by similarity / 命名的代码块 + 描述，可按相似性检索 |
| Skill library | "Agent memory of how-to" / "Agent 的操作记忆" | Persistent store of skills, searchable and composable / 技能的持久化存储，可搜索可组合 |
| Curriculum | "Task proposer" / "任务提议器" | Bottom-up goal generator driven by current capability gap / 由当前能力差距驱动的自底向上目标生成器 |
| Composition | "Skill DAG" / "技能 DAG" | Skills invoking skills; topologically sorted on execution / 技能调用技能；执行时拓扑排序 |
| Iterative refinement | "Self-correcting loop" / "自我纠错循环" | Env feedback + errors + self-verification fold back into the next version / 环境反馈+错误+自我验证反馈到下一版本 |
| Action-space-as-code | "Programmatic actions" / "编程式动作" | Emit functions, not primitive commands, for temporally extended behavior / 发出函数而非原始命令，用于时间扩展行为 |
| Dedup on write | "Skill collapse" / "技能合并" | Near-duplicate descriptions collapse to one canonical skill / 近似重复描述合并为一个规范技能 |

## Mais leitura 延伸阅读

- [Wang et al., Voyager (arXiv:2305.16291)](https://arxiv.org/abs/2305.16291) o papel original da biblioteca de habilidades
  Tradução do português:Voyager
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) competências como a produtividade de 2026
  中文翻译:Claude Agent SDK 概览2026 年产品化技能──
- [Anthropic, Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) competências e subagens na prática
  Chinese: 关于用Claude Agent SDK 构建 Agent 的文章实践中的技能和子代理──
- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) o ciclo de refinamento debaixo do Voyager
  Tradução do inglês: Self-Refine 论文Voyager 底层的精炼循环──
