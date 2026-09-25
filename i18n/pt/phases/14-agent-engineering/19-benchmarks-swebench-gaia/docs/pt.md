# Benchmarks: SWE-bench, GAIA, AgenteBench.

> Três pontos de referência avaliação de agentes ancoradores em 2026. SWE-bench testes patching de código. GAIA testes uso de ferramentas generalistas. AgentBench testes raciocínio multi-ambiente. Conheça sua composição, sua história de contaminação, e o que eles não medem.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 06 (Tool Use) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objetivos de aprendizagem

- Nomear o arame de ensaio do banco SWE (FAIL_TO_PASS) e explicar por que é incompatível com os testes unitários.
- Explique por que existe o SWE-bench Verified (OpenAI, 500 tarefas) e o que elimina.
- Descreva o design da GAIA: simples para os seres humanos, difícil para a IA; três níveis de dificuldade.
- Nomear os oito ambientes do AgentBench e seu principal bloqueador para LLM de código aberto.
- Resumir a constatação da contaminação do banco SWE+ e as suas implicações.

## O problema é o problema da introdução

Os rankings dizem-lhe qual modelo vence num ponto de referência.

> A classificação diz-te qual modelo vence num determinado nível.

> O SWE-bench e o GAIA são os dois principais fundamentos da capacidade do Agente. O SWE-bench avalia a capacidade de modificação do código, o GAIA avalia a capacidade de raciocínio geral.

- Se o indicador de referência está contaminado (soluções nos dados de formação, vazamento de ensaio).
- Se o índice de referência mede o que lhe interessa (código vs navegação vs generalista).
- Se o avaliador é robusto (matching AST, verificações de estado, revisão humana).


> **【中文解读】**SWE-bench e GAIA são os dois principais agentes de 2026 能力基准。SWE-bench 评估 Agent 修复真实 GitHub issue 的能力(软件工程)。GAIA 评估 Agent 回答需要多步推理和工具使用的复杂问题的能力──通用推理── ambas definiram conjuntamente a capacidade do agente.

> **{【拓展：SWE-bench (Princeton, 2023) 包含 2,294 个真实 GitHub is...】}**SWE-bench (Princeton, 2023) incluem 2.294 个真实 GitHub issue,Agente 必须在真实代码库中定位 bug、编写修复并通过测试──2026年 SOTA 是 72% 解决率(OpenAI 的 Codex) ・GAIA (Meta, 2023) 的 466 个问题需要 web 搜索、文件处理、代码执行等工具──人类平均 92% ,最佳代理约70%──
Conheça os três pontos de referência de ancoragem e os seus modos de falha antes de citar um número.

> Antes de citar os dados, primeiro compreenda estes três testes básicos e seu modelo de falha.

> - Não .**【前置】**建议先过:Phase 14·06(Uso de Ferramentas) 理解 Agent 如何调用工具是看懂 GAIA的前提;以及基本的"机器学习评估方法论"精度/回忆、污染(数据污染) 测试集泄漏──

## O conceito central.

### SWE-bench (Jimenez et al., ICLR 2024 oral)

- 2.294 problemas reais do GitHub de 12 repositorios populares do Python.
- Agente recebe: a base de código no pré-fix comit + descrição de problema em linguagem natural.
- O agente produz um parche.
- Avaliação: aplicar correção, executar o conjunto de testes do repo. O correção deve virar testes FAIL_TO_PASS (anteriormente falhando, agora passando) sem quebrar testes PASS_TO_PASS.

O agente SWE (Yang et al., 2024) atingiu 12,5% na liberação enfatizando interfaces agente-computador (comandos de editor de arquivo, sintaxe de pesquisa que o modelo entende).

> - Não .**【类比】**SWE-bench 像考"开卷实操": dar ao Agente uma verdadeira código biblioteca(开卷) 、 um problema 描述(考题) 、一套已有的单元测试(评分标准) ⋅ Agente 像人类工程师一样读代码定位 bug、写补丁、跑测试──**关键设计**O que é que é o "facto" de um "facto" de um "facto" de um "facto" de um "facto" de outro?

> SWE-agent ((Yang 等,2024) alcançou 12,5% no momento da publicação, através do enfatizamento de Agente-computador interface ((文件编辑器命令、模型能理解的搜索语法) ]]

> O SWE-bench e o GAIA são os dois principais fundamentos da capacidade do Agente. O SWE-bench avalia a capacidade de modificação do código, o GAIA avalia a capacidade de raciocínio geral.

### Banco SWE Verificado

OpenAI, agosto de 2024. Subconjunto de 500 tarefas curado pelo ser humano. Elimina problemas ambíguos, testes não confiáveis e tarefas onde a correção não era clara.

> OpenAI, agosto de 2024 ⋅ 500 个任务子集 of artificial策划 ⋅ Remove a problemática confusa ⋅ testes e reparações incertos ⋅ "O seu agente pode entregar correções reais?"

> O SWE-bench e o GAIA são os dois principais fundamentos da capacidade do Agente. O SWE-bench avalia a capacidade de modificação do código, o GAIA avalia a capacidade de raciocínio geral.

### Contaminação

- Mais de 94% dos problemas de banco SWE são anteriores à maioria dos cortes de modelos.
- **SWE-bench+**A Comissão concluiu que, em relação aos resultados dos testes, a Comissão não tinha qualquer informação sobre os resultados dos testes.
- Verificado é mais limpo, mas não livre de contaminação.

Implicação prática: um modelo que obtenha 50% em SWE-bench pode obter 35% em SWE-bench+.

> ️ **【易错点】**引用 SWE-bench 分数时不提 Verificado/SWE-bench+。**后果**O estudo foi realizado em um estudo de estudos de ciências da informação sobre a existência de "contaminação" em uma área de investigação.**一行修复**Qualquer citação de SWE-bench números, deve simultaneamente dar Verified 子集分数和 SWE-bench+(去污染版) 分数,注明数据来源日期。

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

> O SWE-bench e o GAIA são os dois principais fundamentos da capacidade do Agente. O SWE-bench avalia a capacidade de modificação do código, o GAIA avalia a capacidade de raciocínio geral.

### A Comissão deve tomar medidas para evitar que a situação seja prejudicial.

- 466 perguntas; 300 mantidas para o ranking privado no huggingface.co/gaia-benchmark.
- Filosofia do design: "conceptualmente simples para os seres humanos (92%) mas difícil para a IA (GPT-4 com plugins: 15%)."
- Teste de raciocínio, multi-modalidade, web, uso de ferramentas.
- Três níveis de dificuldade; o nível 3 requer longas cadeias de ferramentas em todas as modalidades.

GAIA é o que você corre para medir "capacidade generalista". Não confundir com referências específicas de código.

> A GAIA é usada para medir a base de "capacidade geral".

> O SWE-bench e o GAIA são os dois principais fundamentos da capacidade do Agente. O SWE-bench avalia a capacidade de modificação do código, o GAIA avalia a capacidade de raciocínio geral.

### Agente Bench (Liu et al., ICLR 2024)

- 8 ambientes em código (Bash, DB, KG), jogos (Alfworld, LTP), web (WebShop, Mind2Web) e geração aberta.
- Multiplo-turn, ~ 4K-13K voltas por divisão.
- Conclusão primária: raciocínio a longo prazo, tomada de decisão e instrução são os bloqueadores para os LLM OSS alcançar a comercial.

### O que estes não medem

- Custo operacional real (tokens, relógio de parede).
- Comportamento de segurança em condições adversas.
- Performance no seu domínio (utilizar as suas próprias avaliações, lição 30).
- Falhas de cauda (média de valores de referência; os operadores de produção se preocupam com o pior 1%).

### Onde a análise comparativa vai mal

- **Single-number fixation.**O banco SWE 50% diz-lhe menos do que o custo P50/P75/P95 + distribuição de etapas.
- **Contaminated claims.**Relacionar o banco SWE sem mencionar o Verified ou o banco SWE+ é enganoso.
- **Benchmark-as-development-target.**A otimização para o índice de referência diverge da utilidade da produção.

> 🤔 **【困惑】**P: SWE-bench Verified 上 70% + de modelos foram lançados, não é que os engenheiros de software devem estar desempregados? A: ainda cedo.**生产代码库比 SWE-bench 的 12 个开源 Python 仓库复杂得多** private code、跨语言、几十年遗留代码──Bênchmark superior de 70% não é igual a 70% do ambiente de produção──

> **单一数字执念。**SWE-banco 50%  Diga-lhe informações inferior a P50/P75/P95 成本 + 步骤分布──
> **污染声明。**報告 SWE-bank 时不提及 Verificado ou SWE-bank+ é errôneo.
> **基准作为开发目标。**A base da otimização é a de desviar a produção da utilidade.

## Construí-lo e realizei-o.
```figure
ae-swebench-gate
```

## Construí-lo

`code/main.py`Instala um arame de brinquedo SWE-bench:

> `code/main.py`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

> O SWE-bench e o GAIA são os dois principais fundamentos da capacidade do Agente. O SWE-bench avalia a capacidade de modificação do código, o GAIA avalia a capacidade de raciocínio geral.

- Tarefas de correção de bugs sintéticas (3 tarefas).
- Um "agente" com guião que propõe patches.
- Um test runner que verifica FAIL_TO_PASS (bug agora corrigido) e PASS_TO_PASS (nada quebrado).
- Um classificador de dificuldade de estilo GAIA baseado na profundidade da decomposição da questão.

- É o que é ?

```
python3 code/main.py
```

A saída mostra a taxa de resolução por tarefa + por dificuldade e torna concretas as regras do avaliador.

> output mostra a taxa de solução de cada tarefa e cada nível de dificuldade, e torna concretizadas as regras do avaliador.

> O SWE-bench e o GAIA são os dois principais fundamentos da capacidade do Agente. O SWE-bench avalia a capacidade de modificação do código, o GAIA avalia a capacidade de raciocínio geral.

## Use-o com o framework implementado.

- **SWE-bench Verified**Sempre relatar as pontuações verificadas.
- **GAIA**Para agentes generalistas, use a divisão de classificação privada.
- **AgentBench**para comparação entre ambientes.
- **Custom evals**(Lessão 30) para a forma real do seu produto.

## Envia-o . Produto .

`outputs/skill-benchmark-harness.md`Construi um arnes de estilo SWE-bench para qualquer par de tarefas base de código com fechamento FAIL_TO_PASS / PASS_TO_PASS.

> `outputs/skill-benchmark-harness.md`Para qualquer código-base- tarefa de construir um SWE-bench 风格的测试工具,带有 FAIL_TO_PASS / PASS_TO_PASS 门控──

> O SWE-bench e o GAIA são os dois principais fundamentos da capacidade do Agente. O SWE-bench avalia a capacidade de modificação do código, o GAIA avalia a capacidade de raciocínio geral.

## Exercícios.

1. Portar o arnes de brinquedo para funcionar em um repo real (põe um do seu). Escrever 3 testes FAIL_TO_PASS para bugs conhecidos.
  Tradução do inglês para tradução do inglês:
2. Adicione uma métrica de contagem de etapas.
  Tradução do inglês para tradução do inglês:
3. Leia o documento SWE-bench+. Implemente uma verificação de fuga de solução (paraleia o padrão com o texto do problema contra a diferença).
  Tradução do inglês para tradução do inglês:
4. Descarregar uma pergunta da GAIA da divisão pública, rastrear o que um agente da classe GPT-4 faria.
  Tradução do inglês para tradução do inglês:
5. Leia a descrição de ambiente do agente Bench, qual ambiente reflete a superfície do produto?
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| SWE-bench | "Code agent benchmark" | 2,294 GitHub issues; patch must flip FAIL_TO_PASS tests |  |
| SWE-bench Verified | "Clean SWE-bench" | 500 human-curated tasks, OpenAI |  |
| FAIL_TO_PASS | "Fix gate" | Tests previously failing that must pass after the patch |  |
| PASS_TO_PASS | "No-regression gate" | Tests that were passing and must still pass |  |
| GAIA | "Generalist benchmark" | 466 human-easy / AI-hard multi-tool questions |  |
| AgentBench | "Multi-env benchmark" | 8 environments; long-horizon multi-turn |  |
| Contamination | "Training-set leak" | Benchmark tasks present in model training |  |
| SWE-bench+ | "Contamination audit" | 32.67% solution leakage found in successful SWE-bench patches |  |

## Mais leitura 延伸阅读

- [Jimenez et al., SWE-bench (arXiv:2310.06770)](https://arxiv.org/abs/2310.06770) o índice de referência original
  Tradução do português:
- [OpenAI, SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) o subconjunto seleccionado
  Tradução do português:
- [Mialon et al., GAIA (arXiv:2311.12983)](https://arxiv.org/abs/2311.12983) Referência geralista
  Tradução do português:
- [Liu et al., AgentBench (arXiv:2308.03688)](https://arxiv.org/abs/2308.03688) Suite multi-ambiente
  Tradução do português:
