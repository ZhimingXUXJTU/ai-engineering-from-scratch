# A família de Optimização de Preferências Direitas

> Rafailov e outros. (2023) mostrou que o ótimo da RLHF tem uma forma fechada em termos de dados de preferência, para que você possa ignorar o modelo de recompensa explícito e otimizar a política diretamente. Essa percepção gerou uma família  IPO, KTO, SimPO, ORPO, BPO  cada um corrigindo um modo de falha de DPO. Em 2026, os algoritmos de alinhamento direto enviam mais corridas de pós-treino fronteiriças do que o PPO. Mas a curva de otimização excessiva da lição 2 ainda se aplica: os DAAs não escapam do Goodhart, eles apenas se movem onde morde.

> **【中文解读】**Este capítulo apresenta o modelo de pré-recompensação do RLHF, que foi desenvolvido diretamente a partir do treinamento de dados preferenciais. Rafaelov  et al. (Rafailov, 2023) demonstra que o RLHF é um modelo de pré-recompensação de dados preferenciais, de modo que pode ser superado.

> **【拓展：DPO 家族 → 现代 AI 训练】**Em 2026, a DAA (Projeto de Otimizamento de Pós-Optimização) foi implementada em mais treinamentos anteriores do que a PPO. Mas a curva de Optimização Excessiva da Lição 2 ainda é aplicável.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, six-variant preference-loss comparator) | **语言:** Python（标准库，六种变体偏好损失比较器）
**Prerequisites:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (Reward hacking), Phase 10 · 08 (DPO basics) | **前置知识:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (奖励黑客), Phase 10 · 08 (DPO 基础)

> - Não .**【前置】**学本节前请先掌握:Fase 18·01-02(InstruGPT+古德哈特) 、Fase 10·08(DPO 基础) ・・・DPO 家族 = 绕过显式奖励模型直接从偏好数据训练――
> - Não .**【类比】**DPO = "deletar o jogo de árbitro"―RLHF = 訓練裁判(奖励模型) + 訓練选手优化裁判评分;DPO = 直接用比赛结果;;DPO = 直接用比赛结果;;偏好对) trein选手;;家族变体 IPO/KTO/SimPO/ORPO/BPO 都在修修 DPO 不同缺陷;;2026 DAA(直接对齐算法) 比 PPO 部署更多;;但古德特定法不变只是从"奖励模型过优化"挪到"参考策略比率过度优化"──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Derivar o formato fechado do DPO do RLHF-with-KL-optimum.
  Tradução do português:                                                                                                                                                                                                                                                            
- Indicar o modo de falha de cada uma das correções de IPO, KTO, SimPO, ORPO e BPO no DPO.
  中文翻译:说明 IPO、KTO、SimPO、ORPO、BPO 分别修复了 DPO 的哪个失败模式──
- Distinguir "margem de recompensa implícita" da "força de preferência" e explicar por que o mapeamento da identidade da OPI é importante.
  Tradução do inglês para o inglês: distinguir "hidden reward gap" e "preference strength", explica por que o ranking da IPO é importante.
- Explique por que Rafailov et al. (NeurIPS 2024) provam que os DAAs são excessivamente óptimas apesar de não ter RM explícita.
  No entanto, a taxa de crescimento de R$ 20 milhões em R$ 20 milhões em R$ 20 milhões em R$ 20 milhões em R$ 20 milhões em R$ 20 milhões em R$ 20 milhões em R$ 20 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 milhões em R$ 30 em R$ 30 milhões em R$ 30 em R$ 30 em R$ R$ 30 em R$ 30 em R$ R$ R$ 30 em R$ R$ R$ 30 em R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R$ R

## O problema é o problema da introdução

O objectivo do RLHF (Lessão 1):

> RLHF 目标(Lessão 1):

```
max_pi E_{x,y~pi} [ r(x, y) ] - beta * KL(pi || pi_ref)
```

tem um óptimo conhecido:

> Há o melhor que se sabe:

```
pi*(y|x) = (1/Z(x)) * pi_ref(y|x) * exp(r(x, y) / beta)
```

Assim, a recompensa é definida implícitamente pela relação entre a política ideal e a referência:

> Assim, a taxa de recompensas é definida de forma conceitual pela melhor estratégia e estratégia de referência:

```
r(x, y) = beta * log(pi*(y|x) / pi_ref(y|x)) + beta * log Z(x)
```

Substitua isso na probabilidade de preferência Bradley-Terry e na função de partição .`Z(x)`cancelas porque depende apenas de`x`O que resta é uma perda nos parâmetros da política sozinho.

> Para colocar isso em Bradley-Terry                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      `Z(x)`Porque depende.`x`E assim, o que resta é a função de perda do parâmetro de estratégia puro.

A redução: a derivação assume que o ótimo é alcançável, os dados de preferência são distribuídos e a política de referência é a âncora de modo verdadeiro. Nenhum destes se aplica exatamente.

>  problema consiste em: sugerir hipóteses de melhor alcance  preferência em distribuição de dados                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

## O conceito central.

> **【中文解读】**A proposta do PO:RLF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

### DPO (Rafailov et al., 2023)

```
L_DPO = -log sigmoid(
  beta * log(pi(y_w | x) / pi_ref(y_w | x))
  - beta * log(pi(y_l | x) / pi_ref(y_l | x))
)
```

O que pode dar errado:

> Talvez haja algum problema.

- A diferença implícita de recompensa .`beta * (log(pi/pi_ref)_w - log(pi/pi_ref)_l)`Uma pequena preferência pode produzir uma lacuna arbitrariamente grande.
  O preconceito pode ser arbitrário.
- O disco de perda seleciona e rejeita log-probs em direções opostas. Pode empurrar o log-prob absoluto escolhido para baixo, desde que o rejeitado cai mais rápido.
  O processo de rejeição é um processo de redução da probabilidade de um número de opções.
- As preferências fora da distribuição (par raro raro vs par raro raro) produzem recompensas implícitas arbitrárias.
  Tradução do inglês: Distribuir Outra Preferência

> **【拓展：IPO → DPO 的边界控制】**IPO(Optimização de Preferências de Identidade) com o log-sigmoide, a diferença de preferências foi substituída por H&M, a diferença de preferências foi 1/(2*beta) 封顶.

### O IPO (Azar et al., 2024)

A Optimização de Preferências de Identidade substitui o log-sigmoid por um mapeamento de identidade na probabilidade de preferência. A perda se torna um erro quadrado em um alvo limitado:

> O IPO usou o tipo de mapeamento para substituir o log-sigmoide, a diferença de preferência foi 1/(2 *beta) 封顶── isso resolveu o problema central do DPO: pequenas diferenças de preferência podem gerar qualquer diferença de recompensa oculta grande──

```
L_IPO = (log(pi(y_w | x) / pi_ref(y_w | x)) - log(pi(y_l | x) / pi_ref(y_l | x)) - 1/(2 beta))^2
```

A margem é limitada por `1/(2 beta)`A força de preferência e a diferença implícita entre a recompensa são proporcionais.

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              `1/(2 beta)`O que é que é o melhor?

> **【拓展：KTO → 无配对数据训练】**O KTO (Kahneman-Tversky Optimization) é uma inovação fundamental que consiste em abandonar completamente o conjunto de estruturas, apenas necessitando de um único marcador para o "ideal" ou "imideal" de saída.

### O TCO (Ethayarajh et al., 2024)

A otimização de Kahneman-Tversky elimina completamente a estrutura em pares. Dado uma saída única rotulada e um sinal binário "desejável" ou "indesejável", ele mapeia para um utilitário de teoria prospectiva:

> KTO  completamente abandonou o conjunto de estruturas                                                                                                                                                                                                                                                          

```
v(x, y) = sigma(beta * log(pi(y|x) / pi_ref(y|x)) - z_ref)
```

A vantagem: pode utilizar dados não emparejados, o que é muito mais abundante.

> Para o benefício e perda de uso de diferentes potências, você pode usar dados não comparados, muito mais do que comparados com dados ricos.

> **【中文解读】**SimPO removeu estratégias de referência, substituindo por longitude unification parallelization parallelization, acrescentando marginale gama  estabilização treinamento. Isto resolveu diretamente o DPO de longitude parallelization mode failure  maior y_w  construção de forma a gerar maior diferença de probabilidade de parallelamento. ORPO mais intensificado: adicionar o preconceito por um padrão SFT  NLL                                                                                                                                                                                                                                                                                                                                                                                                                       

### SimPO (Meng et al., 2024)

Otimizar as preferências simples alinha o sinal de treinamento com a geração.

> SimPO irá treinar sinais e gerar para todos.

```
L_SimPO = -log sigmoid(
  (beta / |y_w|) * log pi(y_w | x)
  - (beta / |y_l|) * log pi(y_l | x)
  - gamma
)
```

com uma margem `gamma`A normalização da comprimento elimina o incentivo a explorar o modo de falha de viés de comprimento do DPO (mais`y_w`dá uma maior lacuna de log-prob por construção).

> Além do outro lado.`gamma`稳定训练――长度归结消除了利用DPO 长度偏见失败模式的激励 (DPO 长度归结) 更多`y_w`                                                                                                                                                                                                                                                              

### ORPO (Hong et al., 2024)

Otimizar a preferência de odds-ratio adiciona um termo de preferência à probabilidade de registro negativo de SFT padrão:

> O ORPO vai adicionar os preconceitos ao padrão SFT 负对数似然上:

```
L_ORPO = L_NLL(y_w) + lambda * L_OR
L_OR = -log sigmoid(log(odds(y_w) / odds(y_l)))
```

Não há política de referência  o termo SFT é o regulador. Trein em uma única etapa do modelo base ao modelo alinhado. Não há ponto de controle separado SFT.

> 无参考策略SFT 项就是正则化器──单阶段从基础模型训练到对齐模型──无需单独的SFT 检查点──

### BPO (submissão ICLR 2026, OpenReview id=b97EwMUWu7)

Identifica o problema de respostas degradadas escolhidas: DPO preserva o ranking `y_w > y_l`Mas o log-prob absoluto de `y_w`BPO adiciona uma correção de linha única que penaliza os movimentos para baixo na resposta escolhida.

> BPO 识别了"退化选择响应" problema:DPO 保持 `y_w > y_l`排序但 `y_w`A probabilidade absoluta de contra-ataque pode diminuir.

> **【拓展：DAA 过度优化 → 通用防御】**Rafailov  et al. (((NeurIPS 2024) em vários conjuntos de dados e KL  orçamento treinamento DPO、IPO、SLiC  estratégia。 real recompensa com a curva de KL apresentada a mesma forma de avanço e descida com Gao  et al.。 DAA recompensa oculta durante o treinamento procura distribuição fora amostra, KL 正则化无法稳定这一点──通用修复更好的数据、集成、早停对PPO和 DPO家族同样适用──

### O resultado universal: os DAAs ainda se optimizam demais

Rafailov et al. "Lei de Escalada para a Optimização Excessiva de Modelos de Recompensa em Algoritmos de Alinhamento Direto" (NeurIPS 2024) treinou políticas com DPO, IPO, SLiC em múltiplos conjuntos de dados em todos os orçamentos KL. As curvas ouro-recompensa-versus-KL têm a mesma forma Gao et al. Pico e colapso. A busca implícita de recompensa de amostras fora da distribuição durante o treinamento; regularização KL não estabiliza isso.

> Rafailov  et al. treinaram DPO、IPO、SLiC  estratégias em vários conjuntos de dados e no orçamento da KL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

Os DAAs não escapam de Goodhart. Eles mudam a superfície onde morde de "modelo de recompensa super-otimizado" para "ratio de política de referência super-otimizado".

> DAA não escapou da antiga lei específica. Eles apenas vão atacar a superfície de "modelo de recompensa de otimização excessiva" para "referência estratégia de otimização excessiva de taxa de informação".

> **【中文解读】**O método de seleção de 2026 ano: há um grande número de pares de preferências dados → DPO(保守 beta) ou SimPO((se houver uma longitude de preconceito); há não pares de dois divisores反 → KTO; querer um único estágio de tubo → ORPO;DPO 日志显示选择概率下降 → BPO; preferência intensidade varia grande e DPO 和 → IPO;; cada laboratório em todos os métodos executado novamente segundo tarefas seleção 优数学推理和安全的最佳方法可能不同.

### Escolher entre eles (2026)

- Se tiver grandes dados de preferência em pares: DPO com beta conservador, SimPO se for evidente o viés de comprimento.
  Chinese: 有大量配对偏好数据 → DPO(保守 beta),如有长度偏见使用 SimPO──
- Se tiver feedback binário não pareado: KTO.
  Chinese: 有非配对二元反 → KTO。
- Se quiser um gasoduto de uma única etapa de um modelo base: ORPO.
  Tradução do inglês para tradução do inglês: want from基础模型的单阶段管线 → ORPO──
- Se virem registos degradados de registos escolhidos nos registos do DPO: BPO.
  中文翻译:DPO 日志中看选择概率下降 → BPO。
- Se as preferências variarem muito e o DPO estiver saturado: IPO.
  Prefixo forte variação grande e DPO 和 → IPO。

Cada laboratório corre todos os cinco em uma bateria e escolhe o vencedor por tarefa. Não há razão para o ótimo ser o mesmo para o raciocínio matemático e segurança.

> Cada laboratório corre perfeitamente em todos os métodos, sem nenhuma razão para pensar que a melhor maneira de raciocínio matemático e segurança é a mesma.

> **【拓展：DPO 家族实践 → 方法选择】**Em 2026 cada laboratório de vanguarda foi executado em todos os métodos. Não há razão para pensar que a melhor maneira de raciocínio e segurança matemática é a mesma.

## Use-o com o framework implementado.
```figure
dpo-margin
```

## Usá-lo

`code/main.py`Comparar seis perdas (DPO, IPO, KTO, SimPO, ORPO, BPO) em um conjunto de dados de preferências de brinquedos onde a força de preferência real varia por pares. Cada perda é otimizada contra a mesma amostra de 500 pares com uma pequena política de softmax.

> `code/main.py`Em um conjunto de dados de jogadores com variação de intensidade preferencial, comparar seis tipos de perdas: DPO, IPO, KTO, SimPO, ORPO, BPO) ⋅ cada tipo de perda no mesmo 500 para a amostra com pequenas softmax estratégias de otimização ⋅ desenhar a taxa de vitória final de cada método ⋅ selecionar probabilidade de deslocamento e distribuição de prêmios ocultas ⋅

## Envia-o . Produto .

Esta lição produz`outputs/skill-preference-loss-selector.md`. Tendo em conta as estatísticas dos conjuntos de dados (paradas versus não paradas, variáveis versus preferências uniformes, distribuição de comprimento) e um alvo (estágio único ou SFT-then-preferência), recomendamos uma perda de preferência e relatamos o modo de falha contra o qual protege.

> 本课产 出 `outputs/skill-preference-loss-selector.md` dados dados dados dados de dados (incluindo: comparativo versus não comparativo, variação versus preferência média, intensidade, distribuição de longitude) e objetivos (incluindo:

## Exercícios.

1. Corra .`code/main.py`. Relatar a queda final de registro-probes escolhido para DPO e BPO.
   Tradução: 运行`code/main.py` Relatório DPO e BPO  O resultado final da seleção para a probabilidade de número diminuiu.

2. Modifique os dados de preferência para que todos os pares tenham a mesma força. Qual dos seis métodos é mais robusto? Qual degrada? Explique a vantagem da IPO aqui.
   Tradução do inglês para tradução do inglês: Modified preference data makes all correspondence strength相等.

3. Faça as respostas rejeitadas em média 2 vezes mais longas do que as escolhidas.
   Chinese Language Translation:使拒绝响应平均比选择响应长 2倍──不改变其他东西, 數值显示 DPO 的长度利用和 SimPO 的修复──

4. Rafailov et al. (NeurIPS 2024) alegam que os DAAs otimizam demais. Reproduzir uma versão de ponto único: gráfico escolhido-menos-rejeitado divergência KL e observar o excesso de otimização no DPO em beta grande.
   O que é que o DPO disse sobre o excesso de otimização em grande beta?

5. Leia o resumo do documento do BPO (OpenReview b97EwMUWu7).`code/main.py`- Não .
   Tradução do idioma:BPO 论文摘要(OpenReview b97EwMUWu7)。写下 BPO对 DPO 添加的单行修正──对照`code/main.py`Confirmação de implementação.

## Termos-chave .

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| DPO | "RLHF without a reward model" / "没有奖励模型的 RLHF" | Loss derived from the closed-form RLHF optimum; policy parameters only / 从闭式 RLHF 最优解推导的损失；仅策略参数 |
| Implicit reward | "the log-ratio" / "对数比率" | `beta * log(pi(y\|x) / pi_ref(y\|x))` — the DPO-implied reward / DPO 隐含的奖励 |
| IPO | "bounded DPO" / "有界 DPO" | Replaces log-sigmoid with identity; implicit reward gap capped by `1/(2 beta)` / 用恒等映射替换 log-sigmoid；隐式奖励差距被 `1/(2 beta)` 封顶 |
| KTO | "unpaired DPO" / "非配对 DPO" | Prospect-theory utility over single labels with loss aversion / 带损失厌恶的单标签前景理论效用 |
| SimPO | "reference-free DPO" / "无参考 DPO" | Length-normalized log-likelihood + margin; no reference policy / 长度归一化对数似然 + 边际；无参考策略 |
| ORPO | "one-stage DPO" / "单阶段 DPO" | NLL + odds-ratio preference term; trains from base model in one pass / NLL + 胜率比偏好项；单阶段从基础模型训练 |
| BPO | "chosen-preserving DPO" / "保留选择的 DPO" | DPO plus a penalty for decreasing the chosen response's absolute log-prob / DPO 加上降低选择响应绝对对数概率的惩罚 |
| Degraded Chosen | "chosen goes down" / "选择概率下降" | DPO decreases chosen log-prob so long as rejected falls faster / DPO 降低选择对数概率只要拒绝下降更快 |
| DAA | "direct alignment algorithm" / "直接对齐算法" | Any preference-loss method that skips an explicit RM / 任何跳过显式 RM 的偏好损失方法 |

## Mais leitura 延伸阅读

- [Rafailov et al. — Direct Preference Optimization (NeurIPS 2023, arXiv:2305.18290)](https://arxiv.org/abs/2305.18290)
  中文翻译:Rafailov 等人DPO 原始论文
- [Azar et al. — A General Theoretical Paradigm to Understand Learning from Human Preferences (AISTATS 2024, arXiv:2310.12036)](https://arxiv.org/abs/2310.12036) OPI
  中文翻译:Azar 等人IPO 论文
- [Ethayarajh et al. — KTO: Model Alignment as Prospect Theoretic Optimization (arXiv:2402.01306)](https://arxiv.org/abs/2402.01306)
  中文翻译:Ethayarajh 等人KTO 论文
- [Meng, Xia, Chen — SimPO (NeurIPS 2024, arXiv:2405.14734)](https://arxiv.org/abs/2405.14734)
  中文翻译:Meng 等人SimPO 论文
- [Hong, Lee, Thorne — ORPO (EMNLP 2024, arXiv:2403.07691)](https://arxiv.org/abs/2403.07691)
  中文翻译:Hong 等人ORPO 论文
- [BPO — Behavior Preservation Optimization (ICLR 2026 OpenReview b97EwMUWu7)](https://openreview.net/forum?id=b97EwMUWu7)
  Tradução do inglês:BPO behavior keep optimization
- [Rafailov et al. — Scaling Laws for RM Overoptimization in DAAs (NeurIPS 2024, arXiv:2406.02900)](https://arxiv.org/abs/2406.02900)
  Tradução do português: Rafael 等人DAA 过度优化缩放定律
