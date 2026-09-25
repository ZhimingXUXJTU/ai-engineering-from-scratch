# Red-Teaming: PAIR e Ataques Automáticos

> Chao, Robey, Dobriban, Hassani, Pappas, Wong (NeurIPS 2023, arXiv:2310.08419). PAIR  Rapido Automático Iterativo Refinamento  é o canônico automático de caixa preta jailbreak. Um LLM atacante com um sistema de red-team prompt propõe iterativamente jailbreaks para um LLM alvo, acumulando tentativas e respostas em seu próprio histórico de bate-papo como feedback no contexto. O PAIR normalmente consegue dentro de 20 consultas, ordens de magnitude mais eficientes do que o GCG (a pesquisa de gradientes de nível de token do Zou et al.) e sem exigir acesso em caixa branca. O PAIR é agora uma linha de base padrão no JailbreakBench (arXiv:2404.01318) e HarmBench, ao lado do GCG, AutoDAN, TAP e Prompt Adversarial persuasivo.

> **【中文解读】**Este capítulo apresenta o método de avaliação de segurança sistematizado do Red Team Test, usando ataques automatizados para descobrir falhas do sistema AI DATA. PAIR(Prompt Automatic Iterative Refinement, NeurIPS 2023) é o padrão de automação da caixa negra.

> **【拓展：PAIR → GCG → 攻击家族谱系】**GCG(Zou 等人 2023) em令牌级梯度搜索对抗后,需要白盒访问,产生不可读字串;;PAIR 是黑盒的,产生自然语言攻击且可跨模型迁移;;AutoDAN 使用进化搜索,TAP 引入分支剪枝,PAP 编码人类说服技术;;JailbreakBench(100 有害行为) 和 HarmBench(510 行为) estándardized assessment;;

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, mock PAIR loop against a toy target) | **语言:** Python（标准库，针对玩具目标的模拟 PAIR 循环）
**Prerequisites:** Phase 18 · 01 (instruction-following), Phase 14 (agent engineering) | **前置知识:** Phase 18 · 01 (指令遵循), Phase 14 (Agent 工程)
**Time:** ~75 minutes | **时间:** ~75 分钟

> - Não .**【前置】**學本节前请先掌握:Fase 18·01、Fase 14──PAIR = 自动化黑盒越狱, atacar LLM 代生成越狱 prompt──
> - Não .**【类比】**PAIR = "AI 自 自动找漏洞"──手工红队 = 人写越狱(慢);PAIR = 攻击 LLM 看目标 LLM 反应,代改进(normalmente 20 查询内成功,比 GCG 快几个数量级)──JailbreakBench/HarmBench 标准基线──

## Objetivos de aprendizagem

- Descreva o algoritmo PAIR: o sistema de ataque rápido, refinamento iterativo, feedback no contexto.

> 描述 PAIR 算法: атака者系统提示、代改进、上下文反──

- Explique por que o PAIR é estritamente mais eficiente do que o GCG quando o alvo é a caixa negra.

> Explica por que PAIR é mais rigoroso do que GCG.

- Nomear outras quatro linhas de base de ataque automatizado (GCG, AutoDAN, TAP, PAP) e indicar uma característica distintiva de cada uma delas.

> 列出其他四种自动化攻击基线 (GCG、AutoDAN、TAP、PAP) 和各自的区分特征──

- Descreva os protocolos de avaliação JailbreakBench e HarmBench e o que significa "taxa de sucesso de ataque" em cada um deles.

> Descrição do JailbreakBench e HarmBench  avaliação de acordo e significado de cada "ataque taxa de sucesso".

## O problema é o problema .

A red-teaming costumava ser uma atividade manual. Um pequeno número de testadores especialistas construíram instruções adversárias e acompanharam as que funcionaram. Isto não é escalavel: a taxa de sucesso do ataque precisa de uma amostra estatística, e o alvo é um alvo em movimento com cada lançamento de modelo. PAIR operacionaliza a red-teaming como um problema de otimização com um alvo de caixa negra.

> 红队测试过去是手动活动──少数专家测试者构建对抗性提示并跟踪哪些有效── é inexplicable: a taxa de sucesso de ataques precisa ser estatística, e cada modelo é lançado com um objetivo em constante mudança──PAIR irá transformar a operação do teste da Red Team em um problema de otimização do objetivo da caixa negra──

## O conceito .

> **【中文解读】**PAIR  algoritmo processo:输入目标 LLM T、评判 LLM J、攻击者 LLM A、目标字符串 G、预算 K(normalmente 20 查询)  ciclo k=1..K:A 根据目标和历史(提示,响应) 对发出新提示 p_k;提交 p_k 到 T 获得响应 r_k;J 评分;如果分数超过值则停止;否则增加到历史继续;;NeurIPS 2023 结果: 对 GPT-3.5-turbo 和 Llama-2-7B-chat 攻击成功率 >50%,平均成功查询数在 10-20 范围内.

### Algoritmo de PAIR

- Input:
- Alvo LLM T (o modelo que estamos a atacar).
- Juez LLM J (pontua se uma resposta é uma fuga de prisão).
- O atacante LLM A (otimizador da equipa vermelha).
- Capa de meta G: "responde com [instrução prejudicial]."
- Orçamento K (geralmente 20 consultas).

> 输入:目标 LLM T(我们攻击的模型) 评判 LLM J(评分响应是否越狱) 攻击者 LLM A(红队优化器) 目标字符串 G("用[有害指令]响应") 预算 K(通常 20 查询) ⋅

Loop, para k em 1..K:
1. A é provocada com o objetivo G e o histórico de pares (prompto, resposta) até agora.
2. A emite um novo sinal de resposta.
3. Enviar p_k para T; receber resposta r_k.
4. J marca (p_k, r_k) no gol.
5. Se a pontuação >= limiar, parar o jailbreak encontrado.
6. Caso contrário, adicione (p_k, r_k) ao histórico de A; continue.

> 循环 k=1..K:1. A 被提示目标 G 和历史(提示,响应) 对──2. A 发出新提示 p_k──3. 提交 p_k 到 T;接收响应 r_k──4. J 评分(p_k, r_k) ・・・5.

Resultado empírico (NeurIPS 2023): > 50% taxa de sucesso de ataque contra GPT-3.5-turbo, Llama-2-7B-chat; consultas médias para sucesso na faixa de 10-20.

> 实证结果(NeurIPS 2023): para GPT-3.5-turbo、Llama-2-7B-chat  ataque taxa de sucesso > 50%; número de perguntas de sucesso média em 10-20  范围──

### Por que a PAIR é eficaz

GCG (Zou et al. 2023) busca sufissivos de tokens adversários por gradiente; requer acesso a modelos de caixa branca e produz sufissivos ilegíveis. PAIR é caixa negra e produz ataques em linguagem natural que se transferem entre modelos.

> GCG 通過梯度搜尋对抗性令牌后;需要白盒访问且产生不可读后──PAIR é uma caixa negra, produzindo modelos de migração de ataques à linguagem natural──PAIR 的上下文反让攻击者从每次拒中学习; GCG 没有等价机制──

### Ataques automatizados relacionados

- **GCG (Zou et al. 2023, arXiv:2307.15043).**A busca de gradientes de nível de tokens para sufisso adversário.

> **GCG（Zou 等人 2023）。**O que é que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é o que é?

- **AutoDAN (Liu et al. 2023).**Pesquisa evolutiva sobre os pedidos, guiada por um objetivo hierárquico.

> **AutoDAN（Liu 等人 2023）。**进化搜索提示, por nível 进化目标指导──

- **TAP (Mehrotra et al. 2024).**Árvore de ataques com poda  ramos múltiplas implementações de estilo PAIR.

> **TAP（Mehrotra 等人 2024）。**O ataque de árvores de cortes foi lançado em vários países.

- **PAP (Zeng et al. 2024).**Prompts adversários persuasivos codifica técnicas de persuasão humana como modelos de prompts.

> **PAP（Zeng 等人 2024）。**O que é um exemplo de que a tecnologia de persuasão humana é um modelo de persuasão?

> **【拓展：ASR 指标 → 评估陷阱】**ATAKING SUCCESS RATE (ASR) DATAS) DATAS: 90% ATAKINGS: 90% ATAKINGS: 200 ATAKINGS: 85% ATAKINGS: 20 ATAKINGS: 85% ATAKINGS: 85% ATAKINGS: 20% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: 90% ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAKINGS: ATAK ATAKINGS: ATAKINGS: 

### JailbreakBench e HarmBench

Ambas (2024) padronizam a avaliação:

> 两者(2024) estándarização avaliada:

- JailbreakBench (arXiv:2404.01318). 100 comportamentos prejudiciais em 10 categorias de políticas OpenAI. Taxa de sucesso de ataque (ASR) como a métrica primária. Requer um juiz (GPT-4-turbo, Llama Guard ou StrongREJECT).

> JailbreakBench: 100 个有害行为,横跨 10 个 OpenAI 政策类别── ataque taxa de sucesso(ASR) como principal indicador── necessita de um juiz──

- HarmBench (Mazeika et al. 2024). 510 comportamentos em 7 categorias, com testes de danos semânticos e funcionais. Comparou 18 ataques contra 33 modelos.

> HarmBench:510 个行为,横跨 7 个类别,包含语义和功能性危害测试──比较 18 种攻击对 33 模型──

A ASR é geralmente relatada com um orçamento fixo de consulta.

> Os ASR normalmente são relatados sob um orçamento fixo de consulta.

> **【中文解读】**2026 Ano de implementação significado: cada laboratório de frente agora está em publicação antes de lançar para o modelo de produção operação PAIR 和 TAP。ASR 轨迹出现在模型卡(Lessão 26) y安全案例附录(Lessão 18) 中──

### Razões pelas quais é importante para as implantações de 2026

Cada laboratório de fronteira agora corre PAIR e TAP contra modelos de produção antes de serem lançados. As trajetórias ASR aparecem em cartões de modelo (Lessão 26) e apêndices de casos de segurança (Lessão 18).

> Cada laboratório de vanguarda está agora em fase de lançamento para o modelo de produção operação PAIR 和 TAP。ASR 轨迹 appears in modelcard and safety case attachment。This is not a special attack It is standard infrastructure。

### Onde isto encaixa na Fase 18

A lição 12 é a base do ataque automatizado. A lição 13 (Many-Shot Jailbreaking) é uma exploração complementar de comprimento. A lição 14 (ASCII Art / Visual) é um ataque de codificação. A lição 15 (Indirect Prompt Injection) é a superfície de ataque de produção de 2026. A lição 16 abrange as contrapartes de ferramentas defensivas (Llama Guard, Garak, PyRIT).

> Lição 12 é a base de ataque automatizado. Lição 13 é a utilização de longo prazo de intercâmbio. Lição 14 é a codificação de ataques. Lição 15 é a produção de ataques de 2026. Lição 16 abrange ferramentas de defesa.

> **【拓展：TAP 和 PAP → 攻击进化】**TAP(Mehrotra 等人 2024) através de várias divisões de PAIR 式 lançou e cortou ramos para expandir PAIR mais alta ASR mas mais calcular──PAP(Zeng 等人 2024) vai tornar a tecnologia de persuasão humana codificada como modelo de dica── atacar a família de GCG de busca de caixa branca para a busca de PAIR de caixa negra代改进, novamente para a busca de árvore de TAP e a engenharia social de PAP── cada geração é mais forte em diferentes dimensões de ataque.

## Usa-o. Usa-o.
```figure
al-pair-loop
```

## Usá-lo

`code/main.py`O atacante é um refinador baseado em regras que tenta parafrasear, criar um quadro de roteiro e codificar. O juiz marca a resposta. Você vê o atacante ter sucesso em ~5-15 iterações contra o filtro de palavras-chave e falhar contra um filtro semântico.

> `code/main.py`Construir um ciclo de PAIR de brinquedos. O objetivo é rejeitar as "evidentes" sugestões prejudiciais.                                                                                                                                                                                                                                                

## Envia-o .

Esta lição produz`outputs/skill-attack-audit.md`- Com base num relatório de avaliação da equipa vermelha, verifica quais foram os ataques (PAIR, GCG, TAP, AutoDAN, PAP), a que orçamento cada um, com que juiz, em que comportamento prejudicial foi estabelecido (JailbreakBench, HarmBench, interno).

> 本课产 出 `outputs/skill-attack-audit.md` Determine o relatório de avaliação da equipa vermelha, auditoria: quais ataques foram executados, orçamento de cada ataque, utilizou quais juízes, em que conjunto de comportamentos prejudiciais.

## Exercícios.

1. Corra .`code/main.py`- Medir as necessidades médias para o sucesso das três estratégias de ataque integradas.

2. Implementar uma quarta estratégia de ataque (por exemplo, tradução para outra língua, codificação base64).

3. Leia Chao et al. 2023 Figura 5 (comparação PAIR vs GCG). Descreva dois cenários em que o GCG é preferido apesar da vantagem de eficiência do PAIR.

4. O JailbreakBench relata a ASR contra um conjunto de objetivos fixos. Desenhe uma métrica adicional que mede a diversidade de ataque (variação em pedidos de sucesso). Explique por que a diversidade é importante para a avaliação da defesa.

5. TAP (Mehrotra 2024) estende o PAIR com ramificação + poda. Esboçar uma extensão no estilo TAP para `code/main.py`e descrever a compensação entre custos computacionais e taxas de sucesso.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| PAIR | "automated jailbreak" | Prompt Automatic Iterative Refinement; attacker-LLM + judge-LLM loop |
| GCG | "gradient jailbreak" | White-box token-level gradient search for adversarial suffixes |
| Attack success rate (ASR) | "% jailbreaks at k queries" | Primary metric; must be reported with query budget and judge identity |
| Judge LLM | "the scorer" | LLM that grades whether a response satisfies the harmful goal |
| JailbreakBench | "the evaluation" | Standardized harmful-behaviour set with tagged categories |
| HarmBench | "the broader bench" | 510 behaviours, functional + semantic harm tests |
| TAP | "tree of attacks" | PAIR with branching + pruning; better ASR at higher compute |

## Mais leitura 延伸阅读

- [Chao et al. — Jailbreaking Black Box LLMs in Twenty Queries (arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) Papel PAR, NeurIPS 2023
- [Zou et al. — Universal and Transferable Adversarial Attacks on Aligned LLMs (arXiv:2307.15043)](https://arxiv.org/abs/2307.15043) Papel GCG
- [Chao et al. — JailbreakBench (arXiv:2404.01318)](https://arxiv.org/abs/2404.01318) Avaliação padronizada
- [Mazeika et al. — HarmBench (ICML 2024)](https://arxiv.org/abs/2402.04249) avaliação mais ampla
