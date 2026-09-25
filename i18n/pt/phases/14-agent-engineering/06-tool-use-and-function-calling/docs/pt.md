# Utilização de ferramentas e função chamada 工具使用与函调用

> O Toolformer (Schick et al., 2023) começou a anotação de ferramentas auto-supervisionada. O Berkeley Function Calling Leaderboard V4 (Patil et al., 2025) define a barra de 2026: 40% agente, 30% multi-turn, 10% ao vivo, 10% não ao vivo, 10% alucinação.

> **【中文解读】**Toolformer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 13 · 01 (Function Calling Deep Dive) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 13 · 01 (函数调用深入)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizagem

- Explique o sinal de treinamento auto-supervisionado do Toolformer: mantenha as anotações da ferramenta apenas quando a execução reduz a perda do próximo token.
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para inglês para o inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para inglês para
- Nomear as cinco categorias de avaliação do BFCL V4 e o que cada uma mede.
  Chinese Translation: nói出 BFCL V4 的五个评估类别及每个衡量的内容──
- Implementar um registro de ferramentas stdlib com validação de esquema, coerção de argumentos e sandboxing de execução.
  Tradução em chinês: Uses standard library implement带模式验证、参数强制转换和执行沙箱的工具注册表──
- Diagnóstico dos três problemas abertos de 2026: cadeia de ferramentas de longo horizonte, tomada de decisões dinâmicas e memória.
  Chinese Language Translation: Diagnosis Three 2026 年开放问题:长链工具编排、动态决策和记忆──

## O problema é o problema da introdução

O uso inicial de ferramentas perguntou: o modelo pode prever uma chamada de função correta? o uso moderno de ferramentas pergunta: o modelo pode ferramentas de cadeia através de 40 passos, com memória, com observabilidade parcial, com recuperação de falhas de ferramentas, sem alucinar ferramentas que não existem?

> O problema do uso de ferramentas modernas é: o modelo pode usar ferramentas em 40 etapas em cadeia, ter memória, processar partes observáveis, recuperar das falhas das ferramentas e não parecer que elas não existem?

A ferramentaforum estabeleceu a linha de base: os modelos podem aprender quando chamar ferramentas com auto-supervisão.

> Toolformer  estabeleceu a linha de base: o modelo pode ser usado através do auto-supervisão. BFCL V4 define o objetivo de avaliação de 2026 .

> **【中文解读】**O problema do uso de ferramentas iniciais é: o modelo pode prever a manipulação de funções correta? o problema do uso de ferramentas modernas é: o modelo pode utilizar ferramentas em 40 etapas em cadeia, ter memória, processar partes observáveis, recuperar de uma falha de ferramentas e não parecer que não existem? a manipulação de funções de uma única rodada está perto de ser resolvida, mas a memória, a decisão em movimento e a elaboração de ferramentas de cadeia longa ainda são um problema aberto para 2026.

> **【拓展：BFCL V4 评估体系的演进】**Berkeley Função Calling Leaderboard V4 é um padrão de avaliação de facto de 2026 anos. V3 introduziu avaliação baseada em estado. V4 adicionou Web.

> - Não .**【前置】**Deve-se ler:Fase 13·01(Fúnção Chamando Deep Dive) 本节假设你已经能写 JSON Schema 并理解人类的 `input_schema`vs OpenAI `function.parameters`区别;Fase 14·01(Agent Loop)  Instrumental调用 Agent 循环发生在 Agent 循环中发生,离开循环单独看工具调用会失去上下文──

## O conceito central.

### Instrumentformer (Schick et al., NeurIPS 2023)

Ideia: deixe o modelo anote seu próprio corpus de pré-treino com chamadas de API candidato. Para cada candidato, execute-o. Mantenha a anotação somente se incluir o resultado da ferramenta reduz a perda no próximo token.

> 核心思想:让模型使用自己的预训语料标标签候选人API调调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调. 调.

Ferramentas abrangidas: calculadora, sistema de avaliação de qualidade, motores de busca, tradutor, calendário.

> 覆盖的工具:计算器、QA 系统、搜索引擎、翻译器、日历──自监督信号纯粹关于工具是否帮助预测文本不需要人工标签──

Resultado em escala: o uso de ferramentas surge em escala. Modelos menores prejudicam as anotações de ferramentas; modelos maiores ganham. É por isso que os modelos de fronteira de 2026 têm um forte uso de ferramentas, enquanto a maioria dos modelos 7B precisa de ajustes explícitos no uso de ferramentas para serem confiáveis.

> Áquele modelo é o que mais se pode fazer para melhorar a sua capacidade de utilização de ferramentas, enquanto a maioria dos modelos 7B precisa de ferramentas visíveis para reduzir a sua capacidade de confiança.

> **【中文解读】**O conceito central do Toolformer é: fazer com que o modelo use seu próprio pre-training linguagem para marcar o candidato API 调用. Para cada candidato, executá-lo. Apenas quando o resultado do instrumento é capaz de reduzir a perda do próximo token, é que ele retém o marcador.

### Berkeley Função chamada Leaderboard V4 (Patil et al., ICML 2025)

BFCL é a avaliação de facto de 2026.

> O BFCL é um padrão de avaliação de fatos em 2026:

- **Agentic (40%)** Tráetoras de agentes completos: memória, múltiplos turnos, decisões dinâmicas.
  Tradução:**智能体 (40%)** completo Agente 轨迹: memori¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬
- **Multi-Turn (30%)** conversas interativas com cadeias de ferramentas.
  Tradução:**多轮 (30%)**带工具链的交互式对话──
- **Live (10%)** Instruções reais enviadas pelo utilizador (distribuição mais difícil).
  Tradução:**实时 (10%)**                                                                                                                                                                                                                                                              
- **Non-Live (10%)** casos de ensaio sintéticos.
  Tradução:**非实时 (10%)**合成测试用例──
- **Hallucination (10%)** detectar quando não deve ser chamada nenhuma ferramenta.
  Tradução:**幻觉 (10%)**检测何时不应调用工具── não é necessário utilizar ferramentas.

V3 introduziu avaliação baseada em estado: após uma sequência de ferramentas, verifique o estado real da API (por exemplo, "o arquivo foi criado?") em vez de corresponder à AST das chamadas de ferramentas. V4 adicionou pesquisa web, memória e categorias de sensibilidade ao formato.

> V3 introduziu uma avaliação baseada em estado: após a execução da série de ferramentas, verificou o estado real da API, como "Fichos já foram criados?") em vez de usar ferramentas de configuração de AST。V4 adicionou a Web  busca、 memória e classe de sensibilidade ao formato。

Descoberta chave de 2026: a chamada de função de turno único está quase resolvida. As falhas se concentram na memória (carregando contexto através de turnos), na tomada de decisões dinâmicas (escolhendo ferramentas com base em resultados anteriores), em cadeias de longo horizonte (deslocação após 20+ passos) e na detecção de alucinações (recusando-se a ligar quando nenhuma ferramenta se encaixa).

> Descoberta-se que a função de rotação única está quase resolvida.

### Esquema de ferramenta

Cada fornecedor tem um esquema.

> Cada fornecedor tem o seu próprio padrão.

```
name: string
description: string (what it does, when to use it)
input_schema: JSON Schema (properties, required, types, enums)
```

Utilizações antropológicas `input_schema`O OpenAI utiliza`function.parameters`As descrições são carregadoras, o modelo as lê para escolher a ferramenta certa. Descrições de ferramentas ruins são a principal causa de falhas escolhidas com ferramentas erradas.

> - Não .**【类比】**O modelo nunca viu a sua ferramenta, a única coisa que pode depender é a descrição.`name: get_user, description: "gets user"`O modelo não sabe se é por ID ou por caixa de correio, e o regresso é o objeto completo ou apenas o nome.**好描述包含三要素**: fazer quê + 何時用 + 输入输出语义──

> ️ **【易错点】**O modelo é um modelo de referência para o modelo de referência.`"5"`(字符串) Retorno à expectativa`int`O esquema...**后果**: your tool function `TypeError`A queda, todo o ciclo de agentes, a interrupção.**一行修复**: в инструмента执行入口统一做 `pydantic.BaseModel.parse_obj`Ou similar a experiência, verificação fracassada quando retornar erros estruturais, como`{"error": "expected int, got str"}`- Não, não.

> Antropico  пряма употреба `input_schema`❖ OpenAI `function.parameters`◊ Ambos aceitam o JSON Schema── descrição é o modelo de carga central através da leitura da descrição para escolher o instrumento correto── descrição de ferramentas ruins é a principal causa do fracasso do instrumento de escolha.

### Validação de argumentos

Não confiem em nenhuma chamada de ferramenta.

> Não acredite em qualquer instrumento.

1. **Type coercion.**O modelo pode retornar uma cadeia "5" onde o esquema diz int. Forçar se é inequívoco; rejeitar se não.
   Tradução:**类型强制转换。**模型可能返回字符串 "5" 但模式要求 int──如果无歧义则强制转换;否则拒绝──
2. **Enum validation.**Se o esquema diz:`status in {"open", "closed"}`e emissões de modelo `"in_progress"`, rejeitar com um erro descritivo.
   Tradução:**枚举验证。**Se mode especificado `status in {"open", "closed"}`E o modelo de saída`"in_progress"`, usando o erro descritivo de rejeição.
3. **Required fields.**Falta campo necessário -> observação de erro imediato de volta ao modelo, não uma queda.
   Tradução:**必填字段。**缺少必填字段 -> 立即回归错误观察给模型, não um colapso.
4. **Format validation.**Data, e-mails, URLs validam com parseres de concreto, não regex.
   Tradução:**格式验证。**O sistema de dados de dados é um sistema de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de

Cada falha de validação deve devolver uma observação estruturada para que o modelo possa tentar novamente com a forma correta.

> Cada teste falha deve retornar à observação estrutural, para que o modelo possa ser reprovado com o formato correto.

### Chamadas paralelas de ferramentas

Os provedores modernos suportam chamadas paralelas de ferramentas em um turno de assistente.

> 现代提供商支持在一个助手轮次中并行调用工具──循环:

1. O modelo emite 3 chamadas de ferramenta com distinção `tool_use_id`S.
   Tradução do inglês:模型发出 3 个带有不同 `tool_use_id`O que é que é o "outil de comunicação"?
2. O runtime executa-as (em paralelo, se independente).
   Tradução do inglês:运行时执行它们 (如果独立则并行)
3. Cada resultado retorna como um`tool_result`Bloco correlacionado por `tool_use_id`- Não .
   Tradução do português:`tool_result`Voltar, através de `tool_use_id`- Não.

Regra de engenharia: tratar as identidades de correlação como suportes de carga. Trocá-las e você obtém o roteamento de ferramenta para resultado errado.

> 🤔 **【困惑】**A: Não é. 40% é para refletir a produção real, mas a taxa de precisão de rotas é ainda baseada em funções de agência.

> 工程规则:将关联 ID 视为核心承载──交换它们会导致错误的工具-结果路由──

### Sandboxing

A execução da ferramenta é a fronteira da caixa de areia. Veja a lição 09 para detalhes. Versão curta: cada ferramenta deve especificar a superfície de leitura/escrita, acesso à rede, tempo de saída, limite de memória.`run_shell(cmd)`é uma bandeira vermelha; especificamente `git_status()`É mais seguro.

> 工具执行是沙箱边界──详见第 9 课――简短版: Cada instrumento deve ser especificado como um espaço de leitura, acesso à rede, tempo e memória.`run_shell(cmd)`É a bandeira vermelha; especifico `git_status()`Mais seguro.

## Construí-lo.
```figure
tool-routing
```

## Construí-lo

`code/main.py`Implementa um registo de ferramentas de forma de produção:

> `code/main.py`实现一生产级工具注册表:

- JSON Schema subconjunto validador (só stdlib).
  中文翻译:JSON Schema 子集验证器 (JSON Schema 子集验证器)
- Registro de ferramenta com descrição, esquema de entrada, tempo de encerramento e executor.
  Tradução do inglês para o inglês:带描述、输入模式、超时和执行器的工具注册。
- A coerção de argumentos e a validação enum.
  Tradução do inglês para Inglês: 参数强制转换和枚举验证.
- Disposição paralela de ferramentas com identificação de correlação.
  Tradução do inglês: 带关联 ID 的并行工具分派──
- Observações de erro como cadeias estruturadas.
  中文翻译:错误观察作为结构化字符串──

- É o que é ?

> 运行:

```
python3 code/main.py
```

O rastro mostra um mini agente chamando três ferramentas em uma vez, com uma chamada deliberadamente malformada que é rejeitada com um erro descritivo que o modelo pode agir.

> 轨迹显示一个迷你代理在一轮次中调用三个工具,其中一个故意形式错误的调用被描述性错误拒绝,模型可以根据此行动.

## Use-o com o framework implementado.

Cada fornecedor tem seu próprio esquema de ferramentas  Antropic, OpenAI, Gemini, Bedrock. Use uma camada de tradução (OpenAI Agents SDK, Vercel AI SDK, LangChain tool adapter) se você precisar de multi-provedor.

> Cada fornecedor tem seu próprio modelo de ferramentas: Antropico, OpenAI, Gemini, Bedrock, se você precisar de mais fornecedores, use o seu próprio modelo de ferramentas.

## Envia-o . Produto .

`outputs/skill-tool-registry.md`gera um catálogo de ferramentas, esquema e registro para um determinado domínio de tarefa. Inclui verificações de qualidade de descrição (a descrição de cada ferramenta diz ao modelo quando usá-lo?).

> `outputs/skill-tool-registry.md`Para um determinado domínio de tarefa gerar o catálogo de ferramentas, padrões e registros.

## Exercícios.

1. Adicione uma ferramenta "no-op" que permite que o modelo se recuse explícitamente a usar qualquer outra ferramenta.
   Chinese: 添加一个"无操作"工具,让模型显然拒绝使用任何其他工具──在类 BFCL 幻觉测试上测量──
2. Implementar a coerção de argumentos para int-as-string e flotar-as-string.
   Tradução do inglês: implementar o parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro de um parâmetro.
3. Adicione um timeout por ferramenta e um interruptor de circuito (rejeita a ferramenta por 60 anos após 3 falhas consecutivas).
   Chinese Translation: Add each tool's supertime and断器 ((连续 3 times failure after reject tool 60 秒) ⋅ Isso como mudar o modo de recuperação do modelo?
4. Leia a descrição do BFCL V4. Escolha uma categoria (por exemplo, "multi-turn") e execute 10 exemplos de instruções através do seu agente.
   中文翻译:阅读 BFCL V4 描述──选择一个类别(如"多轮")并通过你的代理 运行 10 个示例提示──报告通过率──
5. Portar o validador do STDlib para a Pydantic ou Zod.
   Chinese:将标准库验证器移植到Pydantic 或 Zod──Pydantic/Zod 捕获了玩具版本遗漏的什么?

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Function calling | "Tool use" / "工具使用" | Structured-output tool invocation with validated schema / 带验证模式的结构化输出工具调用 |
| Toolformer | "Self-supervised tool annotation" / "自监督工具标注" | Schick 2023 — keep tool calls whose results reduce next-token loss / Schick 2023——保留减少下一个 token 损失的工具调用 |
| BFCL | "Berkeley Function Calling Leaderboard" / "Berkeley 函数调用排行榜" | 2026 benchmark: 40% agentic, 30% multi-turn, 10% live, 10% non-live, 10% hallucination / 2026 基准：40% 智能体、30% 多轮、10% 实时、10% 非实时、10% 幻觉 |
| Tool schema | "Function signature for the model" / "模型的函数签名" | name, description, JSON Schema of arguments / 名称、描述、参数的 JSON Schema |
| tool_use_id | "Correlation ID" / "关联 ID" | Ties a tool call to its result; essential for parallel dispatch / 将工具调用与其结果关联；并行分派必需 |
| Hallucination detection | "Know when not to call" / "知道何时不调用" | V4 category: refuse to call when no tool fits / V4 类别：无合适工具时拒绝调用 |
| Argument coercion | "String-to-int repair" / "字符串到整数的修复" | Narrow fixes for predictable schema-mismatch; reject if ambiguous / 可预测模式不匹配的窄修复；如果歧义则拒绝 |
| Sandboxing | "Tool execution boundary" / "工具执行边界" | Per-tool read/write surface, network, timeout, memory cap / 每个工具的读写范围、网络、超时、内存上限 |

## Mais leitura 延伸阅读

- [Schick et al., Toolformer (arXiv:2302.04761)](https://arxiv.org/abs/2302.04761) Anotado de ferramentas auto-supervisionadas
  中文翻译:Toolformer 经典论文自监督工具标注。
- [Berkeley Function Calling Leaderboard (V4)](https://gorilla.cs.berkeley.edu/leaderboard.html) Valor de referência de avaliação 2026
  中文翻译:Berkeley 函数调用排行榜 V42026 年评估基准──
- [Anthropic, Tool use documentation](https://platform.claude.com/docs/en/agent-sdk/overview) Esquema de ferramentas de produção no SDK Claude Agent
  中文翻译:Antropic 工具使用文档Claude Agent SDK 中的生产级工具模式──
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) Tipo de ferramenta e Guardrails
  中文翻译:OpenAI Agents SDK 文档函数工具类型和护。
