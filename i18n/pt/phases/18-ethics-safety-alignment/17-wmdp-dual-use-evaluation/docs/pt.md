# WMDP e Avaliação de Capacidade de Uso Duplo.  avalia                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

> Li et al., "O Benchmark WMDP: Medir e Reduzir o Uso Malicioso com Desaprendizagem" (ICML 2024, arXiv:2403.03218). 4.157 perguntas de escolha múltipla em matéria de biossegurança (1.520), cibersegurança (2.225) e química (412). As questões operam na "zona amarela"  de conhecimento de proximidade, filtrada por revisão por vários peritos e conformidade com o ITAR/EAR. Dual finalidade: avaliação por procuração da capacidade de duplo uso e referência de desaprendimento (o método RMU acompanhado reduz o desempenho do WMDP, preservando a capacidade geral). Narrativa de campo 2024-2025: as primeiras avaliações do OpenAI/Anthropic 2024 relataram "um leve aumento" sobre a pesquisa na internet; em abril de 2025, o Framework de Preparação v2 da OpenAI disse que os modelos estão "na praia de ajudar significativamente os novatos a criar ameaças biológicas conhecidas". O teste de aquisição de armas biológicas da Anthropic mostrou um aumento de 2,53 vezes, insuficiente para descartar a ASL-3.

> **【中文解读】**Este capítulo apresenta o WMDP  Double Use Assessment  Measure AI systems in bio 化学 网络安全等高风险领域 四,157 多选题 涵盖生物安全  1,520) 网络安全  2,225) 化学  412), em operação 黄区  接近有害流程  能使知识但不是直接合成配方  配套的 RMU  表征误导遗忘) 方法 保持通用能力  随时将 WMDP 分数降至接近随机 

> **【拓展：2024-2025 提升叙述 → 从"轻微"到"关键"】**O modelo de avaliação inicial de 2024 "Light Lift" para os novos utilizadores tem apenas uma pequena vantagem; o modelo de relatório de 2025 "Em breve vai avançar" OpenAI PF v2  relatório modelo irá ajudar significativamente os novos utilizadores a criar ameaças biológicas conhecidas; Antropic 2025 Bioweapons Obtaining Experiment 2,53                                                                                                                                                                                                                                                                                                                                                                                                                                            

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, WMDP-shaped uplift evaluation harness) | **语言:** Python（标准库，WMDP 形式提升评估框架）
**Prerequisites:** Phase 18 · 16 (red-team tooling), Phase 14 (agent engineering) | **前置知识:** Phase 18 · 16 (红队工具), Phase 14 (Agent 工程)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**學本節前 請先掌握:Fase 18·16(red team tools) 、Fase 14。WMDP = Avaliação de Capacidade de Arma de Mata de Grande Dimensão
> - Não .**【类比】**WMDP = "AI 武器化潜力体检"―4157 题(生物 1520+网安 2225+化学 412),"黄色区域"= 接近使能知识但非直接配方──双重用途:(1) 评估 AI 双重用途能力;(2) 遗忘基准(RMU 方法降低 WMDP 分但保通用能力)―2025 OpenAI PF v2 警告模型"在显著帮助新手制造已知生物威胁的边缘"ASL-3 触发线──

## Objetivos de aprendizagem

- Descreva os três domínios do WMDP, as contagens de perguntas e o critério de filtro "zona amarela".

>  Descrição dos três domínios do WMDP  número de problemas e "zona amarelo"  padrão

- Explique a RMU e por que o WMDP é tanto uma avaliação como um ponto de referência para o desaprendizagem.

> Explicar a RMU e por que a WMDP é tanto avaliação como esquecimento.

- Descreva a narrativa de elevação 2024-2025: "elevação leve" -> "no limiar" -> "insufficiente para descartar ASL-3".

> 描述 2024-2025 年提升叙述:"轻微提升" -> "即将突破" -> "不足以排除ASL-3"──

- Distinguir a elevação relativa para novatos da capacidade absoluta para especialistas.

> 区分新手对提升和专家绝对能力──

## O problema é o problema .

A capacidade de duplo uso é o problema de medição no quadro de segurança de fronteira de cada laboratório (Lessão 18). A questão é: o modelo X avança materialmente a capacidade de um novato causar danos em massa em bio, química ou cibernética? A medição direta (pega no modelo para produzir realmente danos) é ilegal e antiética. A medição por procuração necessita de um índice de referência que o modelo não pode recusar (produzir números honestos de capacidade), mas cujas questões não são em si mesmas publicações prejudiciais.

> A capacidade de duplo uso é um problema de medição sob o quadro de segurança da vanguarda de cada laboratório. O problema é: o modelo X é realmente avançado na capacidade de novos usuários em áreas biológicas, químicas ou de rede causar danos em grande escala? a medição direta é ilegal e é imprópria. A medição por agência requer um modelo que não pode rejeitar o seu fundamento, mas o problema em si não é uma publicação prejudicial.

## O conceito .

> **【中文解读】**"Yellow Zone" design: requer um processo nocivo que permita obter conhecimento, mas não uma combinação sintética direta.

### A "zona amarela"

Perguntas que exigem um conhecimento próximo de um processo prejudicial sem ser uma receita de síntese direta. "Que reagente cataliza o passo 4 da [caminha publicada]?" e não "como faço [composto perigoso]?" Cada pergunta revisada por vários especialistas em domínio; filtrada para conformidade com o ITAR/EAR de controle de exportação.

> • necessitar de um processo nocivo para facilitar o conhecimento, mas não de uma forma directa de elaboração.

4.157 perguntas no total:
- Biosecuridade: 1.520
- Cibersegurança: 2.225
- Química: 412

>  total de 4.157 道题: bio segurança 1.520、网络安全 2,225、化学 412。

O modelo responde sem ser solicitado a ajudar com nada; a capacidade pode ser medida sem provocar comportamento prejudicial.

> 选择题格式──模型在不被要求协助任何有害活动的情况下回答;能力可以在不引发有害行为的情况下测量──

> **【中文解读】**RMU (Expression Error Guidance Forgotten): é aplicado em LLaMa-2-7B, reduzindo o WMDP a um nível quase acessível, mantendo a base de MMLU e outras capacidades gerais dentro de alguns centos de pontos.

### RMU  Representação Desdirecção para Desaprendizagem

O método de desaprendizagem acompanhado. Aplicado ao LLaMa-2-7B, reduziu as pontuações do WMDP para quase aleatórias, preservando a MMLU e outros benchmarks de capacidade geral dentro de alguns pontos percentuais.

> 配套的遗忘方法── é aplicado a LLaMa-2-7B, reduzindo o número de WMDPs para quase o caso, mantendo a MMLU e outras capacidades gerais baseadas em alguns centos de pontos── é a base de cada subsequente biochemico-network safety forgetting paper──

### A narrativa de 2024-2025

Três fases:

> Três fases:

1. **2024 "mild uplift."**As primeiras avaliações do OpenAI e da Antropic Preparedness/RSP relataram pequenas vantagens em relação à pesquisa na internet para novatos que tentam tarefas bio-adjacentes.

> **2024 年"轻微提升"。**O modelo de avaliação inicial tem poucas vantagens para os novatos.

2. **April 2025 "on the cusp."**O Framework de Preparação da OpenAI v2 relatou modelos "na praça de ajudar significativamente os novatos a criar ameaças biológicas conhecidas".

> **2025 年 4 月"即将突破"。**O modelo de relatório OpenAI PF v2 está prestes a ajudar significativamente os novatos a criar ameaças biológicas conhecidas.

3. **Anthropic's 2025 bioweapon-acquisition trial.**Estudo controlado com participantes novatos, medido sucesso relativo em tarefas de fase de aquisição. 2.53x aumento relatado. Insuficiente para descartar ASL-3 (Lessão 18)  o limiar para a Política de Escalação Responsável de Anthropic nível 3 é cumprido ou aproximado.

> **Anthropic 2025 年生物武器获取试验。**Relativamente à taxa de sucesso dos novos participantes na fase de obtenção de tarefas, o relatório aumentou 2,53 vezes, não sendo suficiente para excluir a ASL-3:

> **【拓展：新手相对提升 vs 专家绝对能力 → 安全案例构建】**Key distinct: novato em relação a elevação é multiplicativo Novato sabe muito pouco, mesmo que a informação de moderação tenha muita ajuda; especialista absoluta capacidade é alta天花板 Especialista sabe o que a pergunta e como explicar.

### Novato-relativo versus especialista-absoluto

Uma distinção crucial:

> 关键区分:

- **Novice-relative uplift.**O modelo ajuda muito um não-perito? Multiplicativo. A vantagem relativa é alta porque os novatos sabem pouco; até mesmo informações modestas ajudam.

> **新手相对提升。**模型对非专家有多少帮助?乘法──新手知道很少,即使适度信息也有很大的帮助──

- **Expert-absolute capability.**O modelo produz quantidade de informação com o máximo de esforço? Um especialista pode extrair mais do que um novato. O teto absoluto é alto.

> **专家绝对能力。**O modelo em seu maior esforço produz muita informação.

Os casos de segurança (Lessão 18) visam tanto: "o modelo não pode dar ao novato um impulso suficiente para executar" como "um especialista não pode extrair informações do modelo que não tenha sido já publicado".

> Leção 18) simultaneamente dirigida a dois: "O modelo não pode dar aos novos um aumento suficiente para executar" adicionado "especialistas não podem extrair informações extra do modelo"

### O problema da medição

O WMDP é um proxy de capacidade, não uma medição de implantação. Um modelo que tem uma pontuação alta no WMDP pode ou não ser explorável por um novato na prática, dependendo de:
- Resistência à provocação (quão difícil é obter a capacidade sem acertar os filtros de segurança)
- Conhecimento tácito (capacidade que exige habilidade em laboratório em molho, não informação)
- Barreiras de execução (adquisições, equipamentos)

> O WMDP é um agente de capacidade, não uma medida de implantação.

O teste de aquisição de armas biológicas de 2025 da Anthropic adiciona a camada de elicitação de novatos em cima da capacidade de estilo WMDP: mede o sucesso da tarefa real, não a capacidade de escolha múltipla.

> A Antropic 2025 Bioweapons Obtaining Experiment adicionou uma nova estratégia sobre a capacidade do WMDP: medir o sucesso das missões reais e não a capacidade de escolha de vários projetos.

### Onde isto encaixa na Fase 18

Lições 12-16 são ferramentas de ataque e defesa em resultados de modelos. Lição 17 é a camada de capacidade de duplo uso  a medição que os quadros de segurança de fronteira (Lessão 18) avaliam. Lição 30 fecha o arco com a atual evidência de aumento cibernético / bio / químico / nuclear de 2026.

> Lições 12-16 são ferramentas de ataque e defesa do modelo. Lição 17 é a medição da capacidade de uso duplo de nível de segurança. Lição 30 é terminada em 2026:

> **【拓展：测量陷阱 → 能力代理非部署测量】**O WMDP é um agente de capacidade, não uma medida de implantação. O modelo de WMDP ganha alta notação em prática, mas não é necessariamente utilizado por novos utilizadores.

## Usa-o. Usa-o.
```figure
al-wmdp-yellow-zone
```

## Usá-lo

`code/main.py`construi um arnes de avaliação em forma de WMDP. Um modelo simulado é testado em perguntas de categoria; pontuações por domínio são relatadas. Uma simples intervenção de desaprendizagem (representação específica de domínio zero-out) reduz as pontuações; você pode medir a compensação em relação à capacidade geral.

> `code/main.py`Construído um quadro de avaliação de forma WMDP. Modelo em análise de problemas de classificação.

## Envia-o .

Esta lição produz`outputs/skill-wmdp-eval.md`. Tendo em conta uma alegação de capacidade de duplo uso ("o nosso modelo não ajuda significativamente com as armas biológicas"), verifica: quais foram os referências executados, qual foi o caminho de recusa utilizado para a avaliação (completo bruto versus política-gated) e se os estudos de elicitação para novatos complementam o resultado de escolha múltipla.

> 本课产 出 `outputs/skill-wmdp-eval.md` Determine as capacidades de duplo uso, auditoria: quais os critérios de execução;

## Exercícios.

1. Corra .`code/main.py`- Relatar a precisão por domínio antes e após a fase de desaprendimento do brinquedo.

2. Aumentar o brinquedo WMDP com um quarto domínio (por exemplo, radiológico). Especificar dois tipos de perguntas ilustrativas na zona amarela. Explique por que a elaboração de tais perguntas é mais difícil do que adicionar perguntas em forma de MMLU.

3. Leia a secção 5 do WMDP 2024 (metodologia RMU). Esboçar uma abordagem de desaprendizagem mais simples (por exemplo, suprimir neurônios top-k para conteúdo de domínio) e descrever o custo esperado de capacidade geral.

4. O teste de aquisição de armas biológicas da Anthropic 2025 relata um aumento de 2,53x. Descreva duas maneiras de este número ser tendencioso para cima (dimensional de amostra novato, fidelidade da tarefa) e duas para baixo (localização de elicitação, fechamento de segurança do modelo).

5. Articular o que um caso de segurança para ASL-3 requer além de passar o WMDP desaprender.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| WMDP | "the dual-use benchmark" | 4,157 MCQ questions across bio/cyber/chem in the yellow zone |
| Yellow zone | "enabling but not synthesis" | Proximate knowledge adjacent to harmful capability without being a synthesis recipe |
| RMU | "the unlearning baseline" | Representation Misdirection for Unlearning; reduces WMDP scores, preserves general capability |
| Novice-relative uplift | "how much it helps non-experts" | Multiplicative advantage over status-quo internet search for a novice |
| Expert-absolute capability | "ceiling for experts" | Maximum information extractable from the model by a motivated expert |
| Acquisition-phase task | "steps before synthesis" | Procurement, equipment, permits — the earliest parts of a harm pathway |
| ITAR/EAR | "export-control compliance" | Legal frameworks that constrain publishing certain enabling knowledge |

## Mais leitura 延伸阅读

- [Li et al. — The WMDP Benchmark (arXiv:2403.03218, ICML 2024)](https://arxiv.org/abs/2403.03218) o documento de referência e a RMU
- [OpenAI — Preparedness Framework v2 (April 15, 2025)](https://openai.com/index/updating-our-preparedness-framework/) "na ponta"
- [Anthropic — Responsible Scaling Policy v3.0 (February 2026)](https://www.anthropic.com/responsible-scaling-policy) Prazo biológico de ASL-3 e resultados dos ensaios de aquisição
- [DeepMind — Frontier Safety Framework v3.0 (September 2025)](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) CCL de bioelevação
