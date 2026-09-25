# Critérios de equidade  Grupo, Individual, Contrafactual  Contras fatos                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

> Três famílias estruturam a literatura de justiça. Equidade de grupo: paridade demográfica, probabilidades igualadas, igualdade de precisão de utilização condicional  taxas iguais entre grupos protegidos em média. A justiça individual (Dwork et al. 2012): indivíduos semelhantes recebem decisões semelhantes; condição de Lipschitz no mapa de decisão. A justiça contrafactual (Kusner et al. A decisão é justa para um indivíduo se não for alterada quando atributos sensíveis são alterados de forma contraditória. Resultado teórico 2024 (NeurIPS 2024): existe uma compensação inerente entre CF e precisão; um método modelo-agnóstico converte um preditor óptimo, mas injusto, em um CF com perda de precisão limitada. Contrafactualidades de retrocesso (arXiv:2401.13935, janeiro 2024): novo paradigma que evita exigir intervenções em atributos legalmente protegidos. Reconciliação filosófica (ICLR Blogposts 2024): com gráficos causais, satisfazer certas medidas de equidade de grupo implica equidade contrafactual.

> **【中文解读】**Esta secção apresenta os princípios de equidade: equidade de grupo, equidade de grupo e equidade de fato.

> **【拓展：不可能定理 → 公平性冲突】**Chouldechova / Kleinberg-Mullainathan-Raghavan (em 2017): teorema impossível: o direito à igualdade de população ̇ a igualdade de preferência e as condições de utilização da taxa de precisão ̇ a igualdade em uma taxa de base de desigualdade não podem ser simultaneamente satisfeitas ̇ é um resultado matemático, não um limite de engenharia ̇ qualquer sistema envolvendo grupos de desigualdade deve escolher qual é o padrão justo sacrificado ̇

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-criteria comparison) | **语言:** Python（标准库，三标准比较）
**Prerequisites:** Phase 18 · 20 (bias), Phase 02 (classical ML) | **前置知识:** Phase 18 · 20 (偏见), Phase 02 (经典 ML)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**学本节前请先掌握:Fase 18·20(偏见) 、Fase 02(经典 ML) 、因果推断基础──公平性三大家族──
> - Não .**【类比】**公平 = "AI's justiça normal"──群体公平(demográfica paridade/quotas igualadas) = 平均上各组别结果相等;个体公平(Dor 2012),= 相似个体得相似决策;反事实公平(Kusner 2017) = 改变敏感属性决策不变──三者不能同时满足选择是政策决定──
> 🤔 NeurIPS 2024:CF-versus-accurate Há peso dentro, mas há um método de transformação de perda de limites existem.

## Objetivos de aprendizagem

- Indique os três critérios de justiça de grupo (paridade demográfica, probabilidades igualadas, igualdade de precisão de utilização condicional) e um resultado de impossível.

> Explicar três grupos de equidade:

- Descrever a equidade individual através da formulação de Lipschitz de Dwork et al. 2012.

> 描述通过 Dwork 等人 2012年 Lipschitz 公式定义的个体公平──

- Descreva a justiça contrafactual e a sua dependência do gráfico causal.

> 描述反事实公平及其因果图依赖──

- Explique as contrafactuais de retrocesso e por que elas evitam o problema da intervenção sobre atributos protegidos.

> Explicar os fatos e por que eles evitam a intervenção na natureza protegida.

## O problema é o problema .

A lição 20 foi sobre a medição de preconceito. A lição 21 é sobre a definição do padrão de justiça que a medição deve servir. As três famílias dão padrões estruturalmente diferentes  um modelo pode ser grupo-justo e individual-injusto, contrafactualmente justo e grupo-injusto. Escolher um padrão é uma decisão política; nenhum padrão é universalmente ótimo.

> Lição 20 é sobre preconceitos de medição. Lição 21 é sobre a definição de padrões equitativos de medição e serviço.

## O conceito .

> **【中文解读】**群体公平三大标准: população平权P(Y=1 whereA=a) = P(Y=1 whereA=a'),各组接受率相等;均等化赔率P(Y=1whereY*=y,A=a) = P(Y=1whereY*=y,A=a'),各组真阳性率和假阳性率相等;条件使用准准率均等P Y*=yY=y,A=a) = P各Y(*=yY=y,A=a'),

### Equidade de grupo

- **Demographic parity.**P (Y=1) A (A) = P (Y=1) A (A) = P (Y=1) para todos os grupos. Taxas de aceitação iguais.
- **Equalized odds.**P (Y=1\Y*=y, A=a) = P (Y=1\Y*y=y, A=a) = P (Y=1\Y*y, A=a) = P (Y=1\Y*y, A=a) = P (Y=1\Y) = Y=y, Y=y, A=a) = P (Y=1\Y) = Y=y, Y=y, Y=y, A=a) = P (Y=1\Y) = Y=y, Y=y, Y=y, A=a) = P (Y=1\Y) = Y=y, Y=y=y, Y=y=y, A=a) = P (Y=y) = y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=
- **Conditional use accuracy equality.**P (Y*=y) = P (Y*=y) = P (Y*=y) = Y=y, A=a') = Valor preditivo igual entre os grupos.

> O número de pessoas que estão em situação de risco de morte é igual ao número de pessoas que estão em situação de risco de morte.

Impossibilidade (Chouldechova, Kleinberg-Mullainathan-Raghavan 2017): estas três não podem ser satisfeitas simultaneamente sob taxas de base desiguais.

> Não é possível resolver: em uma base de desigualdade, estas três coisas não podem ser satisfeitas simultaneamente.

### Equidade individual

Dwork et al. 2012. Um mapa de decisão f é individualmente justo em relação a uma métrica de similaridade específica de tarefa d se f(x) - f(x') <= L * d(x, x') para alguma constante Lipschitz. Indivíduos semelhantes recebem decisões semelhantes.

> Dwork 等人 2012──decision mapping f Se para um determinado Lipschitz 常数 L 满足  f  x) - f  x') ≠ <= L * d  x, x'),则对任务特定相似度度度度度 d 是个体公平──相似个体得到相似决策──

Requer definir d. Questão política, não estatística.

> 需要定义 d. É uma questão de política, não de estatística.

> **【拓展：反事实公平 → 因果图依赖】**Kusner 等人(2017) de Antifaktual Fairness: sob o modelo de causa, se a decisão não mudar após a alteração da atributos sensíveis do indivíduo à realidade, então a decisão é justa para o indivíduo.

### A justiça contrafactual

Uma decisão é contrafactualmente justa para o indivíduo se, sob um modelo causal da população, a decisão não é alterada quando os atributos sensíveis do i são alterados contrafactualmente.

> Kusner  et al. 2017 ⋅ Em um modelo de causa, se a decisão não mudar após a alteração da atributos sensíveis ao fato do indivíduo, a decisão é justa contra o fato do indivíduo.

Requer um DAG causal. O DAG é uma escolha de modelagem. A justificação contrafactual é apenas tão justificada quanto o DAG.

> 需要因果 DAG──DAG 是建模选择──反事实公平的合理性取决于DAG的合理性──

### O acordo de compensação entre CF e precisão

NeurIPS 2024 teórico: há um trade-off inerente entre a justiça contrafactual e a precisão preditiva. Um método modelo-agnóstico pode converter um preditor ótimo, mas injusto, em um CF, a um custo de precisão limitado. O custo de precisão depende da magnitude do coeficiente de atributo sensível no preditor injusto ótimo.

> NeurIPS 2024  Teórico Resultados: Existe um peso fixo entre o anti fato público e a precisão de previsão.

### Contradições de retrocesso

ArXiv:2401.13935 (janeiro 2024). Contratações tradicionais exigem intervenções no atributo sensível  "a decisão mudaria se essa pessoa tivesse sido de gênero diferente".

> O conflito entre as realidades tradicionais e as práticas é um problema de natureza sensível.

Os contrafactos de retrocesso viram a direção: em vez de intervir no atributo, pergunte qual combinação das características reais do indivíduo teria produzido o resultado contrafactual.

> O retrocesso contra os fatos não é uma característica de intervenção, mas é uma questão de saber qual é a combinação das características reais do indivíduo que produz os resultados contra os fatos.

> **【中文解读】**哲学调和(ICLR Blogposts 2024): tendo um gráfico de causa, satisfazer a medida de equidade de certos grupos é um tipo de equidade que inclui a desigualdade de fatos.

### Reconciliação filosófica

ICLR Blogposts 2024. Com um gráfico causal em mãos, satisfazer certas medidas de justiça de grupo implica justiça contrafactual. As três famílias não são ortogonais; são facetas diferentes da mesma estrutura causal subjacente.

> ICLR 2024: Com o desenho de causa, satisfazer a equidade de certos grupos é uma medida que inclui a equidade de contras factos.

Isto não resolve os teoremas da impossibilidade (tasas de base desiguais ainda impedem a justiça simultânea de grupo), mas mostra que a aparente oposição entre "grupo" e "indivíduo / contrafactual" é parcialmente um artefato de não ser explícito sobre o modelo causal.

> Não há solução teoricamente impossível, mas demonstrar a parte superficial em relação entre "grupos" e "individuais/antifactos" é porque não há hipóteses de causalidade definidas.

### Onde isto encaixa na Fase 18

A lição 20 é a medição de preconceito. A lição 21 é a definição de equidade. A lição 22 é privacidade (privacia diferencial). A lição 23 é marcação de água. Estas são as lições adjacentes à alocação complementando as lições 7-11 adjacentes ao engano.

> Lição 20 é preconceito. Lição 21 é justiça. Lição 22 é privacidade. Lição 23 é água.

> **【拓展：CF vs 准确性权衡 → 实际影响】**NeurIPS 2024  Teórico Resultado: Existe um peso fixo entre o anti fato público e a precisão da previsão. O método do modelo inconhecível pode converter o melhor, mas não justo, pré-previsor em CF.

## Usa-o. Usa-o.
```figure
an-fairness-trilemma
```

## Usá-lo

`code/main.py`Classificação binária de brinquedos com um atributo sensível e taxas de base desiguais. Compute paridade demográfica, chances igualadas e igualdade de precisão de uso condicional em um classificador simples. Observe as três métricas discordantes. Aplique uma re-ponderação para paridade demográfica e observe seu custo nos outros dois.

> `code/main.py` Construir um conjunto de dados de brinquedos com características sensíveis e taxas de base de desigualdade.

## Envia-o .

Esta lição produz`outputs/skill-fairness-criterion.md`- Tendo em conta uma alegação ou política de equidade, identifica qual é o critério a ser reivindicado, se o modelo pode satisfazer os restantes critérios sob as taxas de base desiguais reivindicadas e de que DAG causal depende a alegação.

> 本课产 出 `outputs/skill-fairness-criterion.md` A declaração de equidade ou política, a declaração de identificação, a declaração de que os critérios respeitam-se ou não, em base à desigualdade, e a declaração de que os fatores dependem.

## Exercícios.

1. Corra .`code/main.py`- Relacionar as três métricas do grupo nos dados padrão.

2. Implementar a métrica de justiça individual de Dwork et al. 2012 usando L2 em características não sensíveis.

3. Leia Kusner et al. 2017. Construa um simples DAG causal de duas características para pontuação de resumo e identifique a condição de justiça contrafactual que implica.

4. O documento de contrafactos de retrocesso de 2024 evita a intervenção em atributos protegidos.

5. A reconciliação ICLR 2024 argumenta que a equidade de grupo e contrafactual são facetas da mesma estrutura.`code/main.py`E indicar a suposição causal que os faria equivalentes.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Demographic parity | "equal rates" | P(Y=1 | A=a) equal across groups |
| Equalized odds | "equal TPR/FPR" | Equal true-positive and false-positive rates across groups |
| Conditional use accuracy | "equal PPV/NPV" | Equal predictive values across groups |
| Individual fairness | "Lipschitz condition" | Similar individuals get similar decisions |
| Counterfactual fairness | "causal alteration invariance" | Decision unchanged under counterfactual attribute alteration |
| Backtracking counterfactual | "explain via actuals" | Counterfactual reasoned backward from outcome, not forward from attribute |
| Impossibility theorem | "the three conflict" | Chouldechova / KMR 2017: group criteria mutually exclusive under unequal base rates |

## Mais leitura 延伸阅读

- [Dwork et al. — Fairness through Awareness (arXiv:1104.3913)](https://arxiv.org/abs/1104.3913) Equidade individual
- [Kusner, Loftus, Russell, Silva — Counterfactual Fairness (arXiv:1703.06856)](https://arxiv.org/abs/1703.06856) equidade contrafactual
- [Chouldechova — Fair prediction with disparate impact (arXiv:1703.00056)](https://arxiv.org/abs/1703.00056) Impossibilidade
- [Backtracking Counterfactuals (arXiv:2401.13935)](https://arxiv.org/abs/2401.13935) novo paradigma para as intervenções de atributo protegido
