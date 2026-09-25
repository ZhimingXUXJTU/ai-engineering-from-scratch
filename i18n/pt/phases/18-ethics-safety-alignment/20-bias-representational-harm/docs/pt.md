# Preconceito e Danos Representativos em LLM

> Gallegos, Rossi, Barrow, Tanjim, Kim, Dernoncourt, Yu, Zhang, Ahmed (Linguística Computacional 2024, arXiv:2309.00770). Pesquisa de base de 2024 que distingue os danos representativos (estereótipos, apagamento) dos danos de alocação (distribuição desigual de recursos) e categorizando as métricas de avaliação como baseadas em embutidos, baseadas em probabilidade ou baseadas em texto gerado. 2024-2025 empírico: An et al. (PNAS Nexus, março 2025) medir preconceito intersecional de gênero x raça em GPT-3.5 Turbo, GPT-4o, Gemini 1.5 Flash, Claude 3.5 Sonnet, Llama 3-70B em avaliação automática de currículo para 20 empregos de nível de entrada. A WinoIdentity (COLM 2025, arXiv:2508.07111) introduz uma avaliação de equidade baseada em incerteza para identidades interseccionais. Yu & Ananiadou 2025 identificam neurônios de gênero em camadas de MLP; Ahsan & Wallace 2025 usam SAEs para revelar preconceitos raciais clínicos; Zhou et al. 2024 (UniBias) manipula cabeças de atenção para desbiasing. Meta-crítica (arXiv:2508.11067): A literatura de 10 anos se concentra desproporcionalmente no viés binário de gênero.

> **【中文解读】**Esta secção apresenta a origem, a análise e a redução de preconceitos no sistema de IA. Gallegos  et al. (Linguística Computacional 2024) distingue entre preconceitos representativos e distribuição de recursos, e avaliará os indicadores de classificação em base a inserção, base de probabilidade e base de produção de textos.

> **【拓展：交叉偏见 → 真实世界影响】**An et al. (PNAS Nexus, Março de 2025) mediu GPT-3.5 Turbo、GPT-4o、Gemini 1.5 Flash、Claude 3.5 Sonnet、Llama 3-70B em 20 个入门级职位自动简历评估中的交叉性别×种族偏见──GPT-4o 在简历评分中对黑人女性的惩罚对黑人男性和白人女性的分别更严重单轴评估无法捕捉这种效应──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, toy embedding-based bias probe) | **语言:** Python（标准库，玩具嵌入偏见探针）
**Prerequisites:** Phase 05 (word embeddings), Phase 18 · 01 (instruction following) | **前置知识:** Phase 05 (词嵌入), Phase 18 · 01 (指令遵循)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**O que é que você está fazendo?
> - Não .**【类比】**偏见 = "AI de tem cores"── provenientes de dados de treinamento(social history bias) + 训练目标──评估三方法:嵌入空间(向量几何) + 概率(logits 差) + 生成文本(输出统计)──2025 An PNAS Nexus:GPT/Claude/Gemini/Llama 在简历评估上有交叉性别×种族偏见──Yu 2025 在 MLP层定位"性别神经元",Ahsan 2025 用 SAE 揭露临床种族偏见──

## Objetivos de aprendizagem

- Define os danos representativos versus atribuídos e dê um exemplo de cada um em uma implantação de MLL.

>  define lesões representativas e lesões distributivas, e cada um em um exemplo da implementação do MLL:

- Nomear as três categorias de avaliação-metrica de Gallegos et al. 2024 e descrever uma métrica de cada uma.

> 列出 Gallegos 等人.

- Descreva a interseccionalidade e por que a medição de equidade baseada na incerteza da WinoIdentity aborda as lacunas na avaliação de preconceitos de um eixo único.

> Descrição da intersecção e por que a medição equitativa baseada em incerteza da WinoIdentity resolveu a lacuna na avaliação de preconceitos de um único eixo.

- Descreva duas abordagens de interpretação mecanicista para o viés (neurônios de gênero, características de SAE, manipulação da cabeça de atenção).

> Descrever dois mecanismos de preconceito

## O problema é o problema .

As lições anteriores abrangem danos deliberados (infracções de prisão, esquemas) e governança da segurança.

> Os cursos anteriores abrangem lesões intencionais ( (越狱, estratégias) e gestão de segurança.

## O conceito .

### Representação vs atribuição

- **Representational harm.**Estereótipos, apagamento, retratos degradantes, um LLM que retrata enfermeiras como exclusivamente femininas está a produzir danos representativos.
- **Allocational harm.**Um LLM que pontua sistematicamente os currículos dos candidatos negros mais baixos está a produzir danos de atribuição.

> **代表性伤害：**刻板印象、抹除、低性描绘──**分配性伤害：**Resultados de matéria desigual. Os dois modelos diferentes podem ser "representativos sem preconceito", mas "distributivos com preconceito".

Os modelos podem ser "imparciais representativamente" (produzir retratos diversos) enquanto são "participais de forma alocacional" (fazer recomendações desiguais).

> 评估需要同时测量两者──

> **【中文解读】**Três tipos de indicadores de avaliação: emplaçado base (WEB)  estatística de correlação entre palavras de identidade e atributos, restringido a expressões de medida e não a comportamento; base de probabilidade  impressão de confirmação vs                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

### Três categorias de avaliação-metrica (Gallegos et al. 2024)

- **Embedding-based.**Testes de estilo WEAT em embutidas pré-RLHF. Medem associações estatísticas entre termos de identidade e termos de atributo.
- **Probability-based.**Probabilidade de conclusões que confirmem estereótipos versus que violam estereótipos. Medida do lado do decodificador.
- **Generated-text-based.**Medida de tarefas a seguir ao fluxo em texto gerado. pontuação de currículo, escrita de recomendações, diálogo. Mais ecologicamente válido; mais difícil de reproduzir.

> **嵌入基础：**O WEAT 式测试,测量身份词和属性词的统计关联──**概率基础：**O que é que se pode dizer sobre o número de pessoas que estão em situação de doença?**生成文本基础：**Método de tarefa, mais eficaz, mas mais difícil de realizar.

### Intersecção

A avaliação de preconceito sobre "gênero" perde o preconceito que só dispara em pares (gênero, raça). Um e outros descobrimentos de 2025 descobrem que o GPT-4o penaliza as mulheres negras em currículos que pontuavam mais do que os homens negros e mais do que as mulheres brancas separadamente. A avaliação de eixo único não pode capturar isso.

> A avaliação de preconceitos sobre "gênero" omite apenas os preconceitos sobre o sexo, a raça e a natureza.

O WinoIdentity (COLM 2025) introduz a equidade interseccional baseada em incerteza. Medir se a incerteza do modelo sobre os resultados difere entre os tuples de identidade interseccional  não apenas a previsão de pontos.

> WinoIdentity  Introdução à avaliação de equidade de transação baseada em incerteza.

> **【拓展：机制可解释性 → 偏见干预新路径】**O mecanismo explicável de 2024-2025 abriu caminho para a intervenção do mecanismo: neuro-gênero (Yu & Ananiadou 2025)  MLP específico neuro-gênero-especificos comportamentos relacionados, dissipação estes neurônios com um custo limitado de capacidade reduzir a diferença de sexo; clínico racial preconceito SAE  Ahsan & Wallace 2025)  Raridade de código caracteres característicos que se descompõem em dimensões explicáveis; UniBias  Zhou  et al. 2024)  Atenção operação de cabeça de realização de zero amostras para preconceito

### Abordagens mecânicas

O trabalho de interpretação de 2024-2025 abre o viés à intervenção mecânica:

- **Gender neurons (Yu & Ananiadou 2025).**Os neurônios específicos do MLP correlam com comportamentos específicos de gênero.
- **Clinical racial bias via SAEs (Ahsan & Wallace 2025).**As características de autoencodeamento Sparse descompõem a representação interna em dimensões interpretáveis; as características relacionadas à raça podem ser identificadas e suprimidas.
- **UniBias (Zhou et al. 2024).**Manipulação de cabeças de atenção para desaceleração de tiro zero. cabeças específicas amplificam a sensibilidade da classe de identidade; zero ou re-peso dessas cabeças reduz o viés sem ajuste fino.

> O mecanismo explicativo de 2024-2025 abriu caminho para a intervenção do mecanismo: a eliminação de neurônios sexuais com custos limitados de capacidade para reduzir a diferença de sexo; a discriminação racial clínica SAE reconhecimento e supressão de características relacionadas com a raça; a operação de atenção da UniBias para a realização de zero amostras de discriminação.

> **【中文解读】**O estudo da literatura de 2010 descobre que o domínio não se concentra proporcionalmente nas preconceitas de gênero de dois tipos.

### A meta-crítica

A revisão de literatura de 10 anos (arXiv:2508.11067, 2025) conclui que o campo se concentra desproporcionalmente no viés binário de gênero. Outros eixos  deficiência, religião, status migratório, identidade multilingüe  recebem muito menos atenção. A meta-crítica argumenta que o foco estreito pode prejudicar grupos marginalizados por negligência: um modelo bem desviado sobre gênero binário pode ser muito desviado em dimensões que ninguém verificou.

> 10 anos de literatura reviews descobriu que o domínio não se concentra em proporção em preconceitos de gênero de dois tipos.

### Onde isto encaixa na Fase 18

As lições 20-21 cobrem preconceito e justiça formalmente. A lição 22 abrange privacidade. A lição 23 abrange marcas de água. Estas são as camadas de dano ao usuário complementando a camada anterior de engano/segurança.

> Lições 20-21 Forma abrangente preconceito e equidade. Lição 22  abrangente privacidade. Lição 23  abrangente água.

> **【拓展：交叉性 → WinoIdentity 基准】**WinoIdentity(COLM 2025, arXiv:2508.07111) introduz a avaliação de equidade de intercâmbio baseada em incerteza. O modelo de medição em diferentes grupos de identidade de intercâmbio não tem certeza de que os resultados são diferentes.

## Usa-o. Usa-o.
```figure
an-bias-two-harms
```

## Usá-lo

`code/main.py`construiu uma sonda de viés baseada em inserção de brinquedo: mede a distância de estilo WEAT entre termos de identidade e termos de atributo em uma simples inserção de co-ocorrência.

> `code/main.py`Construiu o brinquedo embutidos em pisos de preconceito: Messação simplesmente presente embutidos em dados pessoais e dados pessoais.

## Envia-o .

Esta lição produz`outputs/skill-bias-eval.md`- Tendo em conta um modelo de cartão ou uma alegação de equidade, verifica a avaliação das três categorias métricas (embedding, probabilidade, texto gerado), a cobertura de interseccionalidade e o mecanismo de qualquer intervenção de desactivação.

> 本课产 出 `outputs/skill-bias-eval.md` A avaliação de três tipos de indicadores de auditoria, a cobertura e o mecanismo de intervenção de preconceito.

## Exercícios.

1. Corra .`code/main.py`- Relacionar os resultados de preconceito do tipo WEAT antes e depois da fase de desvio.

2. Extenda a sonda com um teste interseccional: (gênero, raça) x (carreira, família).

3. Leia An et al. 2025 (PNAS Nexus). Identifique os dois efeitos interseccionais que relatam que a avaliação de gênero de um eixo único não seria possível.

4. Yu & Ananiadou 2025 identificar neurônios de gênero. Esboçar um experimento de falsificação que distinguiria "estes neurônios causam preconceito de gênero" de "estes neurônios correlacionam com preconceito de gênero".

5. A meta-crítica argumenta que o campo se concentra muito estreitamente no gênero binário.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Representational harm | "stereotypes / erasure" | Biased portrayal of a group |
| Allocational harm | "unequal decisions" | Biased material outcome for a group |
| WEAT | "the embedding test" | Word Embedding Association Test; co-occurrence-based bias probe |
| Intersectionality | "combined identity effects" | Bias that emerges at the intersection of multiple identity axes |
| Gender neurons | "MLP bias neurons" | Specific neurons whose activations correlate with gender-specific behaviour |
| SAE feature | "interpretable dimension" | Sparse-autoencoder-identified feature; useful for mechanistic bias analysis |
| UniBias | "attention-head debiasing" | Zero-shot debiasing by reweighting attention heads |

## Mais leitura 延伸阅读

- [Gallegos et al. — Bias and Fairness in LLMs: A Survey (arXiv:2309.00770, Computational Linguistics 2024)](https://arxiv.org/abs/2309.00770) Análise canónica
- [An et al. — Intersectional resume-evaluation bias (PNAS Nexus, March 2025)](https://academic.oup.com/pnasnexus/article/4/3/pgaf089/8111343) Estudo interseccional de cinco modelos
- [WinoIdentity — uncertainty-based intersectional fairness (arXiv:2508.07111, COLM 2025)](https://arxiv.org/abs/2508.07111) novo índice de referência
- [UniBias — attention-head manipulation (Zhou et al. 2024, ACL)](https://arxiv.org/abs/2405.20612) Descarga de tiro zero
