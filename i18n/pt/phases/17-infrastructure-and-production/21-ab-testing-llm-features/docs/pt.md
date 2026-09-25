# A/B Testing LLM Características  GrowthBook, Statsig, e o Vibes Problem

> Os testes A/B tradicionais não foram construídos para LLM não deterministas. A distinção crítica: os avaliadores respondem "o modelo pode fazer o trabalho?" Os testes A/B respondem "os usuários se importam?" Ambos são necessários; o envio em verificações de vibração acabou. O que testar em 2026: engenharia rápida (formulação), seleção de modelo (GPT-4 vs GPT-3.5 vs OSS; precisão vs custo vs latência), parâmetros de geração (temperatura, top-p). Casos reais: uma variante do modelo de recompensa do chatbot forneceu +70% de comprimento de conversa e +30% de retenção; experimentos de linha de assunto Nextdoor AI forneceram +1% CTR após o refinamento da função de recompensa; Khan Academy Khanmigo iterou em um eixo de latência versus precisão matemática. Divisão de plataforma: **Statsig**(adquirido pela OpenAI por US$ 1,1 bilhão em setembro de 2025)  testes sequenciais, CUPED, tudo em um. **GrowthBook** código aberto, nativo de armazenamento, motores Bayesianos + Frequentistas + Sequenciais, CUPED, verificações SRM, correções Benjamini-Hochberg + Bonferroni.

> **【中文解读】**Este capítulo apresenta os métodos para a avaliação científica do Mestrado em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em Letras em de Letras em Letras em de Letras em Letras em Letras em de Letras em de Letras em Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de Letras em de de de Letras em de Letras em de Letras em de que a que a de de de de de Letras em de que a de de de que a de de que a de que a pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos pos


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy sequential test simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 20 (Progressive Deployment) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 20 (Progressive Deployment)

> - Não .**【前置】**學本節前請先掌握:Fase 17·13(可观测性) ‧Fase 17·20(渐进部署) ‧统计基础(CUPED、序贯测试) ‧传统 A/B 不为非确定性 LLM 设计──
> - Não .**【类比】**LLM A/B 测试 = "usando métodos científicos em vez de um "bracket" ⋅ 关键区别:eval 问"模型能做吗";A/B 问"用户在乎吗"⋅ 两者都要──测什么:prompt措辞、模型选择、生成参数(temperatura/top-p) ⋅ 案例:聊天机器人变体+70% 对话长度+30% 留存;Nextdoor AI 标题+1% CTR;Khanmigo 在延迟 vs 数学准确率间舍舍──平台:Statsig((AI 11 bilhões de compra,全功能) ⋅ GrowthBook ⋅ 开源ware 原生、贝叶斯频率+被序贯引擎) ⋅
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Distinguir as avaliações ("o modelo pode fazer o trabalho") dos testes A/B ("o usuário se importa").
  中文翻译:区分评估("模型能做这个工作吗")和 A/B 测试("用户在乎吗")。
- Enumerar três eixos testáveis (pronto, modelo, parâmetros) e escolher a métrica para cada um.
  Chinese: 列举三可测试轴 (提示、模型、参数)并为每个选择指标──
- Explique CUPED, testes sequenciais e correções de comparação múltipla de Benjamini-Hochberg.
  Tradução do inglês para tradução livre: CUPED、序贯检验和 Benjamini-Hochberg 多重比较校正──
- Escolha Statsig ou GrowthBook com base na postura do armazém SQL e na posição de aquisição corporativa.
  Chinese: 字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字幕,字,字幕,字,字幕,字幕,字,字幕,字,字,字,字,字,字,字,字,字,字,字,字,字,字,字,字,字,字,字,字,

## O problema é o problema da introdução

> **【中文解读】**传统 A/B 测试不是为不确定性 LLM 构建的. 关键区分:评估(evals) responder "模型能做这件事吗?", A/B 测试回答"用户在乎吗?" ambos são necessários凭感觉上线(vibes check) 时代已经结束.

> **【拓展：LLM A/B 测试的真实案例】**O modelo de produção de teste de A/B de 2026 é: 1) 聊天机器人奖励模型变体+70% 对话长度、+30% 留存率; 2) Nextdoor AI 主题行实验奖励函数优化后 +1% CTR; 3) Khan Academy Khanmigo在延迟对数学准确率轴上代;

Você ajudou a um sistema de resposta. Ele se sente melhor. Você enviou. mudanças de conversão por ruído. Você culpou a métrica. Ou você enviou um novo modelo e a conversão não se movia? O modelo se degradou ou a mudança foi pequena demais para detectar? Você não sabe, porque você enviou sem um A / B.

Os equivalentes respondem se o modelo pode fazer uma tarefa em um conjunto rotulado. Eles não respondem se os usuários preferem a saída. Somente um experimento online controlado responde a isso, e somente se o experimento tiver poder suficiente, controla o não-determinismo e corrige para múltiplas comparações.

## O conceito central.

### Evals vs testes A/B

**Evals** offline, conjunto rotulado, juiz (rubrica ou LLM-as-judge ou humano). Resposta: "A saída é correta / útil / segura nesta distribuição fixa?"

**A/B test**Resposta: "A nova variante muda a métrica de nível de usuário que importa?"

Os valores equivalentes confirmam o impacto do produto após a exposição.

### O que testar

1. **Prompt engineering** formulação, estrutura de sistema de instruções, exemplos.
2. **Model selection** GPT-4 vs GPT-3.5-Turbo vs Llama-OSS. Métrica: precisão (tarefa) + custo/requisito + latência P99.
3. **Generation parameters**- temperatura, top-p, max_tokens. Metrica: específica da tarefa (diversidade de saída vs determinismo).

### CUPED  redução da variância

> **【中文解读】**CUPED (em inglês: CUPED) é uma técnica de redução de diferença de tamanho de um teste A/B. O princípio é que, antes do período de comparação, o diferença de tamanho de um teste anterior é reduzida em 30 a 70%, e é efetivo para aumentar gratuitamente a quantidade de amostras.

Experimentos controlados usando dados pré-experimentais. Regressa a variância pré-periódica antes de comparar o pós-periodo. Reduzção típica de variância: 30-70%.

Implementação: ambas as aplicações Statsig e GrowthBook.

### Testeamento seqüencial

A A/B clássica assume tamanho fixo da amostra. Os testes sequenciais ("peek-and-decide") controlam a taxa de falsos positivos sob olhares repetidos. Procedimentos sequenciais sempre válidos (mSPRT, sequências de confiança de Howard) permitem que você pare cedo sobre vencedores claros.

### Correções de comparação múltipla

A correção de Bonferroni aperta α por teste; Benjamini-Hochberg controla a taxa de descoberta falsa.

### Descoincidência da relação SRM  amostras

Assegnação hash randomizes usuários para variantes. Se 50/50 dividir entrega 47/53, algo está quebrado  SRM check flags it. Ambas as plataformas implementar.

### Statsig vs GrowthBook

> **【拓展：Statsig vs GrowthBook 选型】**O Statsig vs GrowthBook de 2026 foi adquirido pela OpenAI em US$ 1,1 bilhão em setembro de 2025. é um SaaS completo. Flags + 实验分析 + 可观测性),内置序贯检查和CUPED, adaptado para o grupo de produtos que desejam ser agrupados.

**Statsig**- Não .
- Adquirido pela OpenAI por US$ 1,1 bilhão (septembro de 2025).
- Testes sequenciais, CUPED, populações resistentes.
- Tudo em um: bandeiras de características + experimentação + observabilidade.
- Melhor ajuste: a equipa já quer um produto em conjunto, não se importa com a propriedade da OpenAI.

**GrowthBook**- Não .
- Open-source (MIT); nativo de armazenamento (leia diretamente Snowflake/BigQuery/Redshift).
- Motores múltiplos: Bayesian, Frequentist, Sequencial.
- CUPED, SRM, Bonferroni, correções de BH.
- Auto-host ou nuvem gerenciada.
- O melhor ajuste: loja de armazenamento SQL, equipe de dados controla a camada métrica, quer OSS.

### Não-determinismo complica o poder

O mesmo prompt produz saídas variadas. Os cálculos tradicionais de potência assumem observações IID. Com o não-determinismo LLM, o tamanho efetivo da amostra é menor que o nominal. Multiplicar o tamanho da amostra exigido por ~ 1,3-1,5x como margem de segurança.

### Resultados reais dos casos

- Variante do modelo de recompensa do chatbot: +70% de comprimento da conversa, +30% de retenção.
- Linhas de assunto de entrada: +1% CTR após refinamento da função de recompensa.
- Khan Academy Khanmigo: troca iterativa de latência versus precisão matemática.

### O antipatrão: transporte em vibrações

> **【拓展：LLM 非确定性对 A/B 测试的影响】**O resultado da análise de resultados é que o resultado da análise de resultados é um resultado de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de resultados de

Todos os engenheiros seniores podem nomear um recurso que foi enviado porque "se sente melhor" sem A/B. A maioria deles regressou métricas de produto que a equipe não notou por meses. A/B é a função forçante.

### Números que você deve lembrar

- Statsig adquirida pela OpenAI: US$ 1,1 bilhão, setembro de 2025.
- GrowthBook: MIT de código aberto; Bayesian + Frequentist + Sequential.
- Reduzir a variância do CUPED: 30-70%.
- Não-determinismo LLM → +30-50% tampão de tamanho de amostra.

## Use-o com o framework implementado.
```figure
mx-sequential-test
```

## Usá-lo

`code/main.py`Simula um teste A/B sequencial com limites fixos e sequenciais.

> `code/main.py`Simula um teste A/B sequencial com limites fixos e sequenciais.

> `code/main.py`Simula um teste A/B sequencial com limites fixos e sequenciais.

## Envia-o . Produto .

Esta lição produz`outputs/skill-ab-plan.md`- Dada a alteração de características, carga de trabalho, linha de base, escolhas de plataforma, portas, tamanho da amostra.

> 本课产 出 `outputs/skill-ab-plan.md`- Dada a alteração de características, carga de trabalho, linha de base, escolhas de plataforma, portas, tamanho da amostra.

## Exercícios.

1. Corra .`code/main.py`Para uma elevação prevista de 5% com conversão de 3% de linha de base, qual tamanho da amostra para 80% de potência?
   Tradução: 运行`code/main.py`◊ expectativa de 5% 提升、基线 3% 转换率, quanto volume de amostra é necessário?
2. Escolha Statsig ou GrowthBook para um cliente local regulado pela assistência médica.
   Tradução do inglês para "Statsig" ou "GrowthBook"
3. Desenhar um A/B que teste GPT-4 vs GPT-3.5 em custo por bilhete resolvido.
   Chinese Translation: Design One On Per Resolution Work Single Cost On Test GPT-4 vs GPT-3.5 A/B 
4. O seu canário passa, mas A/B mostra conversão de -1,2%.
   Chinese: 你的金丝雀通过但A/B 显示 -1.2% 转换率──你上线?写出解释──
5. Aplicar o CUPED a um período prévio com 60% da variação do posto.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Eval | "offline test" | Labeled-set evaluation of model capability |
| A/B test | "experiment" | Live randomized comparison on users |
| CUPED | "variance reduction" | Pre-period regression to reduce variance |
| Sequential test | "peek-ok test" | Always-valid procedure allowing early stop |
| Multiple comparison | "the family error" | Running many tests inflates false positives |
| Bonferroni | "tight correction" | Divide α by number of tests |
| Benjamini-Hochberg | "BH FDR" | False-discovery-rate control, less conservative |
| SRM | "bad split" | Sample ratio mismatch; assignment bug |
| Statsig | "OpenAI owned" | Commercial all-in-one, acquired 2025 |
| GrowthBook | "the OSS one" | MIT warehouse-native platform |
| mSPRT | "sequential probability ratio test" | Classical sequential procedure |

## Mais leitura 延伸阅读

- [GrowthBook — How to A/B Test AI](https://blog.growthbook.io/how-to-a-b-test-ai-a-practical-guide/)
- [Statsig — Beyond Prompts: Data-Driven LLM Optimization](https://www.statsig.com/blog/llm-optimization-online-experimentation)
- [Statsig vs GrowthBook comparison](https://www.statsig.com/perspectives/ab-testing-feature-flags-comparison-tools)
- [Deng et al. — CUPED](https://www.exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf)
- [Howard — Confidence Sequences](https://arxiv.org/abs/1810.08240)
