# Diferencial de privacidade para LLM 差分隐私 LLM

> A DP-SGD continua a ser a norma  as atualizações de gradientes injetadas por ruído fornecem garantias formais (epsilon, delta). O custo geral em computação, memória e utilidade é substancial; o ajuste fino de DP eficiente em parâmetros (LoRA + DP-SGD) é a configuração comum de 2025 (ACM 2025). Dois corpos de evidências em tensão: inferência de adesão baseada em canários (Duan et al., 2024) relata sucesso limitado contra modelos de linguagem; extração de dados de treinamento (Carlini et al., 2021; Nasr et al., 2025) recupera memorizar substancialmente. Resolução (arXiv:2503.06808, março 2025): a diferença é no que é medido  canários inseridos versus dados "mais extraíveis". Os novos projetos de canários permitem a MIA baseada em perdas sem modelos de sombra e produzem a primeira auditoria de DP não trivial de um LLM treinado em dados reais com garantias realistas de DP. Alternativas: PMixED (arXiv:2403.15638)  previsão privada no tempo de inferência através de mistura de especialistas em distribuições de tokens seguintes; geração de dados sintéticos DP (Google Research 2024). Ataque emergente: Reversão diferencial da privacidade através de Feedback de LLM  vazamento de pontuação de confiança.

> **【中文解读】**Este capítulo apresenta a diferença entre a privacidade do LLM e a proteção da privacidade dos dados dos usuários em treinamento e raciocínio.

> **【拓展：MIA vs 训练数据提取 → 衡量差距】**Em 2025, duas matérias-primas foram apresentadas para o MIA: Kim丝雀 MIA (Duan 等人) (Relatório sobre o sucesso do modelo de linguagem limitado; Training Data提取(Carlini 2021, Nasr 等人 2025) (Relatório sobre o sucesso do modelo de linguagem em 2025) para recuperar um grande número de memórias por letra.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, DP-SGD noise-injection and ε-δ accountant demonstration) | **语言:** Python（标准库，DP-SGD 噪声注入和 ε-δ 计数器演示）
**Prerequisites:** Phase 01 · 09 (information theory), Phase 10 · 01 (large-model training) | **前置知识:** Phase 01 · 09 (信息论), Phase 10 · 01 (大模型训练)
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**學本节前请先掌握:Fase 01·09(信息论) 、Fase 10·01(大模型训练) ・DP-SGD = 标准 DP 训练方法,(ε,δ) 保证。
> - Não .**【类比】**DP = "data hid身衣"──DP-SGD em gradiente de injectão de ruído, individual sample does not affect whole training→ formalizada matemática prova não pode ser feita a partir do modelo de re-proposição de algum item de dados em um conjunto de treinamento──代价:计算/内存/效用都明显下降──LoRA+DP-SGD é 2025 实用配置((
> 🤔 困境: 金雀式 MIA 攻击失败 vs 训练数据提取成功差别在测什么(插入 vs 最易提取) ・・・2025.3 新金雀设计首次对真实数据 LLM 做非凡 DP 审计──

## Objetivos de aprendizagem

- Defina a privacidade diferencial (epsilon, delta) e especifique a receita DP-SGD.
- Explicar a tensão de 2024-2025: MIA canária vs extração de dados de treinamento dão imagens diferentes.
- Descreva o PMixED e porque a previsão privada de tempo de inferência é uma alternativa ao treinamento de DP.
- Descreva a Reversão Diferencial da Privacidade através do ataque de Feedback da LLM.

> 定义 (epsilon, delta) -差分隐私并说明 DP-SGD 方法──解释 2024-2025 年张力:金丝雀 MIA vs 训练数据提取给出不同图景──描述 PMixED 及为什么推理时私有预测是 DP 训练的替代──描述通过 LLM 反的差分隐私逆转攻击──

## O problema é o problema .

Os LLM memorizam. Carlini et al. 2021 mostrou que os modelos de linguagem de produção reproduzem texto de treinamento literal sob demanda. DP é a defesa formal: treinar para que a saída seja provavelmente insensível a qualquer exemplo de treinamento. As evidências de 2024-2025 mostram que DP-SGD é necessário, mas os valores implementados ε podem não corresponder ao modelo de ameaça.

> LLM 会记忆──Carlini 等人 2021 anos de demonstração de produção de um modelo de linguagem pode ser aplicado a cada palavra.

## O conceito .

> **【中文解读】**(epsilon, delta) -差分隐私定义:随机算法 M 是 (epsilon, delta) -DP 的, se para qualquer dois números diferentes de um exemplo de dados e qualquer evento S:P(M(D) em S) <= e^epsilon * P(M(D') em S) + delta。

### (ε, δ) - privacidade diferencial

Um algoritmo aleatório M é (ε, δ) -DP se para quaisquer dois conjuntos de dados que diferem em um exemplo e em qualquer evento S:
P(M(D) em S) <= e^ε * P(M(D') em S) + δ.

> 随机算法 M 是 (ε, δ) -DP 的, se para qualquer dos dois ângulos diferem um exemplo de dados e qualquer evento S:P(M(D) em S) <= e^ε * P(M(D') em S) + δ。

Interpretação: a distribuição de saída é suficientemente próxima (parametrizada por ε) para que a contribuição de qualquer indivíduo não possa ser inferida de forma confiável, exceto com probabilidade δ.

> Explicação: Output distribuição suficientemente próxima (por ε 参数化), qualquer contribuição individual não pode ser deduzida com confiança, exceto a probabilidade δ──

### DP-SGD

Abadi et al. 2016. A receita padrão:
1. Prove um mini-parce.
2. Calcule os gradientes por exemplo.
3. Clip cada gradiente por exemplo para um limiar C.
4. Sumar os gradientes cortados e adicionar ruído gaussiano com std σ * C.
5. Use a soma barulhenta para atualizar os parâmetros.

> DP-SGD standards method:1. 采样小批次──2. 计算逐例梯度──3. 剪切每梯度到值 C──4. 求和剪切后的梯度并添加高的噪音──5. 采样小批次──2. 计算逐例梯度──3. 剪切每梯度到值 C──4. 求和剪切后的梯度并添加高的噪音──5. 采样小批次──5. 采样小批次──2. 计算逐例梯度──3. 剪切每梯度到值 C──4. 求和剪切后的梯度并添加高的噪音──5. 使用噪音和更新参数──.

O custo da privacidade é acompanhado por um contador (contador de Moments, contador de Rényi DP). Os valores ε relatados na literatura do LLM variam muito de acordo com o modelo de ameaça, a sensibilidade dos dados e o objetivo de utilidade; não há um padrão "seguro" universal ε. Os exemplos publicados abrangem aproximadamente ε ≈ 110 em algumas configurações de formação de LLM, mas estes são ilustrativos  não são recomendados. A menor ε geralmente requer mais ruído e pode aumentar a perda de utilidade.

> Os custos de privacidade são observados por contadores. Os relatórios em literatura têm um valor diferente do modelo de ameaça; não há uma "segurança" em geral.

### LoRA + DP-SGD

O DP-SGD completo de um modelo de fronteira é proibitivo. LoRA (Hu et al. 2022) limita as atualizações de gradiente a um pequeno adaptador, reduzindo o armazenamento de gradiente por exemplo. LoRA + DP-SGD é a configuração comum de 2025.

> Total volume DP-SGD  treinamento custo do modelo da frente é muito alto. LoRA  limite de gradiente actualizar para pequenos adaptadores, reduzir o nível de armazenamento por caso. LoRA + DP-SGD é uma configuração comum em 2025.

### A tensão de 2024-2025

Duas linhas de evidências:

> 两条证据线:

- **Canary MIA (Duan et al. 2024).**Insira canários únicos em dados de treinamento, mensure se um atacante de inferência de membros pode identificá-los. Relata sucesso limitado em modelos de linguagem. Sugere que a MIA é difícil.
- **Training-data extraction (Carlini 2021, Nasr et al. 2025).**Apresenta o modelo com um prefixo; mede se ele recupera texto literal do treinamento. Relata memorizar substancial. Sugere que a MIA é fácil no sentido relevante.

> O MIA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

Resolução de março de 2025 (arXiv:2503.06808): as duas medidas diferentes. MIA pergunta "é o exemplo e em D?" em canários inseridos. Extração pergunta "o que posso recuperar de D?" O exemplo "mais extrazível" é o que importa para a privacidade; canários relatam isso porque não são otimizados para serem extraídos.

> Resolução de 3 de março de 2025: Dues medidas diferentes.

Novos projetos de canários. MIA baseada em perdas sem modelos de sombra. Primeira auditoria de DP não trivial de um LLM em dados reais com garantias realistas de DP.

> MIA baseada em perda de modelo sem sombra, pela primeira vez, em dados reais com DP real, LLM assegurando a realização de auditoria de DP extraordinária.

> **【拓展：PMixED → 推理时隐私】**PMixED(arXiv:2403.15638) fornece previsão privada: em next-token distribuição especialistas misturados, cada especialista vê um pedaço de dados do treinamento, aglutinando adição de ruído para realizar DP── completamente evitado DP  treinamento──DP  síntese de dados gerada(Google Research 2024) usando DP-SGD LoRA 微调采样合成数据, em seguida, em formação em dados sintéticos 游分类器── ambos com diferentes modelos de ameaça para evitar o custo de utilização de todo o DP 训练──

### Alternativas à formação em DP

- **PMixED (arXiv:2403.15638).**Previsão privada no momento da inferência. Mistura de especialistas em distribuições de tokens seguintes; cada especialista vê um fragmento de dados de treinamento; agregação adiciona ruído para DP. Evita o treinamento DP inteiramente.
- **DP synthetic data generation (Google Research 2024).**LoRA-fine-tune com DP-SGD, amostras de dados sintéticos, treinar um classificador a jusante sobre os dados sintéticos.

Ambos evitam o custo de utilidade de um treinamento completo de DP ao custo de um modelo de ameaça diferente.

> **【中文解读】**差分隐私逆转攻击(2025): usar DP 训练模型的置信分数作为预言机重新识别个体──即使输出不泄露,置信分布也可能泄露──防御:不暴露置信度,或在暴露前截断/量化──这是 (epsilon, delta) -DP 训练之外的额外要求──

### Reversão diferencial da privacidade através de Feedback do MLL

Ataque de 2025 emergente. Use os resultados de confiança de um modelo treinado por DP como um oráculo para re-identificar indivíduos. Mesmo quando as saídas não vazam, distribuições de confiança podem.

> 2025 新兴攻击: usar DP 训练模型的置信分数作为预言机重新识别个体──即使输出不泄露,置信分布也可能泄露──

A defesa: não expõem confidencias, ou truncate/quantize-los antes da exposição.

> 防御:不露置信度,或在露前截断/量化── é um requisito extra fora do treinamento (ε, δ) -DP.

### Onde isto encaixa na Fase 18

As lições 20-21 são preconceito/justiça. A lição 22 é privacidade. A lição 23 é proveniência através de marcas de água. A lição 27 abrange a camada regulatória de proveniência de dados.

> Lições 20-21 é preconceito/justo. Lição 22 é privacidade. Lição 23 é fonte de água. Lição 27 abrange a fonte de dados de supervisão.

> **【拓展：DP-SGD 的实际开销 → LoRA 解决方案】**Total DP-SGD  treinamento modelo de frente em cálculo, memória e utilização em custos enormes. LoRA(Hu 等人 2022) limitação de gradiente atualização para pequenos adaptadores, redução de gradiente de armazenamento por caso. LoRA + DP-SGD é o padrão de configuração de 2025 DP garantia para adaptadores, modelo base manter fixo.

## Usa-o. Usa-o.
```figure
an-dp-clip-noise
```

## Usá-lo

`code/main.py`Simula DP-SGD num conjunto de dados de classificação binária de brinquedos. Você pode varrer o multiplicador de ruído σ e a norma de corte C e rastrear o orçamento (ε, δ) e o custo de precisão. Um "ataque canário" inserir um exemplo de treinamento único e mede se um teste de perda de registro pode detectá-lo antes e depois do DP.

> `code/main.py`Em jogo de segunda classe em conjunto de dados em formato DP-SGD. Você pode analisar o número de ruído multiplicado σ e cortar o número de fânulas C, acompanhar (ε, δ) o orçamento e a taxa de precisão custos.

## Envia-o .

Esta lição produz`outputs/skill-dp-audit.md`. Tendo em conta uma alegação de DP sobre a implantação de um modelo linguístico, verifica: os valores (ε, δ), o contador utilizado, o protocolo de avaliação da MIA e se foram avaliados vetores de confiança-exposição.

> 本课产 出 `outputs/skill-dp-audit.md` Declaração de DP sobre a implementação de um modelo de linguagem, audit: ((ε, δ) 值、使用的计计器、MIA 评估协议以及是否评估了信任暴露向量──

## Exercícios.

1. Corra .`code/main.py`. Escolher σ em {0,5, 1.0, 2.0} e relatar a compensação de precisão (ε, δ).

2. Realizar uma inserção de canários e um teste de perda de registro.

3. Nasr et al. 2025 sobre a extracção de dados de formação. Por que o sucesso da extracção não desmorona em casos moderados?

4. Desenhar uma implantação usando PMixED (arXiv:2403.15638) que funcione inteiramente no momento da inferência. Qual é o modelo de ameaça que PMixED aborda que DP-SGD não faz?

5. Esboçar a reversão do DP através do ataque de feedback do LLM. Projetar uma contra-medida que limite a fuga de dados de confiança e estimar o custo de implantação.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| DP | "(ε, δ)-differential privacy" | Formal privacy: output distribution close under neighbouring-dataset change |
| DP-SGD | "noise-injected SGD" | Gradient clipping + Gaussian noise addition; standard DP training |
| LoRA + DP-SGD | "efficient private fine-tune" | DP-SGD on low-rank adapters; standard 2025 configuration |
| MIA | "membership inference" | Attack that determines whether an example was in training data |
| Canary | "inserted watermark example" | Unique training example used to measure DP leakage |
| PMixED | "private inference mixture" | Inference-time DP via mixture-of-experts on next-token distributions |
| DP Reversal | "confidence leakage attack" | Attack that uses a model's confidence as an oracle for re-identification |

## Mais leitura 延伸阅读

- [Abadi et al. — DP-SGD (arXiv:1607.00133)](https://arxiv.org/abs/1607.00133) o algoritmo padrão de formação DP
- [Carlini et al. — Extracting Training Data (arXiv:2012.07805)](https://arxiv.org/abs/2012.07805) o papel de extracção canônico
- [Duan et al. — Canary MIA on LLMs (arXiv:2402.07841, 2024)](https://arxiv.org/abs/2402.07841) MIA de sucesso limitado
- [Kowalczyk et al. — Auditing DP for LLMs (arXiv:2503.06808, March 2025)](https://arxiv.org/abs/2503.06808) Resolução da tensão
- [PMixED (arXiv:2403.15638)](https://arxiv.org/abs/2403.15638) Previsão privada de tempo de inferência
