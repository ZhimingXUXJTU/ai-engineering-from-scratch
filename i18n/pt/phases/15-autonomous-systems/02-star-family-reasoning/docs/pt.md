# STAR, V-STAR, Quiet-STAR  Raciocínio auto- ensinado  STAR série de métodos de auto-revelação

> O menor ciclo de auto-melhoria possível está dentro da lógica. Um modelo gera uma cadeia de pensamentos, mantém os que aterram nas respostas corretas e ajusta-os. É o STAR. O V-STaR adiciona um verificador, por isso a seleção de tempo de inferência é melhor. O Quiet-STaR empurra a razão para cada sinal. Os três trabalham. Nenhum deles é mágico. O ciclo preserva qualquer atalho que aconteceu para chegar à resposta certa.

> **【中文解读】**O menor ciclo de auto-melhora oculta no processo de raciocínio: o modelo gera uma cadeia de pensamentos, mantém o processo de raciocínio das respostas corretas, reduzindo os dados. É o STaR. V-STaR.

> **【拓展：STaR → OpenAI o1/o3 的自我改进】**A série STaR é um modelo de treinamento de "auto-exploração" que utiliza seus próprios pensamentos para se exercitar. O treinamento de fortalecimento da série OpenAI o1/o3 é baseado em um método semelhante: gerar vários caminhos de pensamento, escolher o certo, usá-los para melhorar o modelo.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bootstrap-loop simulator) | **语言:** Python (标准库，bootstrap 循环模拟器)
**Prerequisites:** Phase 13 · 01-03 (Reasoning and CoT), Phase 15 · 01 (long-horizon framing) | **前置知识:** Phase 13 · 01-03（推理与 CoT），Phase 15 · 01（长程框架）
**Time:** ~60 minutes | **时间:** ~60 分钟

> - Não .**【前置】**O STAR é o menor círculo de "auto-destruição + 推理增强" (STAR é o menor círculo de "auto-destruição + 推理增强").
> - Não .**【类比】**STaR = "aluno auto-aprobação"──普通学习 = 老师改作业学生订正(人工标注推理过程);STaR = 学生写推理→对答案→对对的推理保留并自我再练一遍(自我生成训练数据)── problema é: às vezes o processo de推理 é errado mas a resposta é por acaso contra contra contra contra contra contra contra contra contra,STaR vai reforçar este tipo de "蒙对" V-STaR加加一个法官验证器) 掉错推理──
> ️ **【易错点】**STaR  treinamento                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

## O problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o problema é o que é o problema é o que é o problema é o que é o problema é o que é o que é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o o o o é o é o o o o é o o o é o é o o o o o é o é o é o o o o o é o é o o o o o é o é o o o o o é o o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é o é é é o é o é é é é o é o é o é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é é

A maneira mais simples de ensinar um modelo a raciocínio é recolher traços de raciocínio escrito pelo homem.

> O método direto de teorizar modelos é a coleta de trilhas de teorizar do livro humano. Isto é caro e lento, mas também limitado à vontade humana de escrever uma linha de pensamento de alta qualidade.

O STaR (Self-Teught Reasoner, Zelikman et al., 2022) pergunta: e se o modelo escrever seus próprios racionais e classificá-los em relação às respostas conhecidas?

> STaR(auto-education推理器, Zelikman 等人,2022) propôs: se o modelo próprio escrever o processo de sugestão e acompanhar o conhecido resposta?


> **【中文解读】**Star 家族推理技术 (STAR、Quiet-STaR、ReST、ReST-EM) através de um auto-treinamento de geração para melhorar a capacidade de pensar em LLM, o pensamento central: fazer um modelo gerar um caminho para pensar em um caminho, através de um caminho de alta qualidade, usando esses caminhos para um modelo de mudança, ciclo 代── é a base técnica da série OpenAI o1/o3 e do pensamento antropico extendido.

1. Uma resposta de raciocínio, mais um rastro.
2. Se a resposta final for correta, mantenha o rastro.
3. - Aponta os vestígios.
4. Repito. - Não.

GSM8K e CommonsenseQA melhoraram sem novas anotações humanas. Mas o loop tem um viés incorporado: qualquer raciocínio que produziu a resposta certa é mantido, independentemente de se o raciocínio em si foi sólido. V-STaR (Hosseini et al., 2024) corrige isso com um verificador aprendido; Quiet-STaR (Zelikman et al., 2024) generaliza a ideia para per-token raciocínios internos.

> É válido. GSM8K e CommonsenseQA têm sucesso sem marcação de nova humanidade. Mas o ciclo tem uma diferença interna: qualquer processo de raciocínio que produz uma resposta correta é mantido, independentemente de se a raciocínio em si é racional.

## O conceito central.

### STaR: bootstrap no que funcionou

Comece a partir de um modelo base com alguma capacidade de raciocínio fraca. Em cada problema de treinamento, amostre uma razão mais resposta. Se a resposta coincide com o rótulo, mantenha o (problema, raciocínio, resposta) triplo. Ajuste o modelo no conjunto mantido. Repita.

> Começa com um modelo básico com capacidade de raciocínio mais fraca. Em cada problema de treinamento, adota um processo de raciocínio para responder.

Uma vez que o modelo nunca consegue resolver um problema, o ciclo não pode aprender com ele.**rationalization**Para os problemas que o modelo falha, injectar a resposta correta como uma sugestão e re-instigar o modelo para produzir uma racionalização que o leve a ele.

> Uma transformação fundamental: se o modelo nunca consegue responder corretamente a uma questão, o ciclo não consegue aprender a partir dele.**合理化**Para o problema de falha do modelo, a resposta correta será injectada como um exemplo, o modelo será re-injectado para o processo de raciocínio da resposta.

Resultado no artigo original (Zelikman et al., 2022): um modelo base GPT-J melhorou no GSM8K de 5,8% para 10,7% através de rodadas repetidas de STaR com racionalização  cerca de 5 pontos percentuais absolutos. No CommonsenseQA, o GPT-J 6B treinado no STaR atingiu 72,5%, comparável a um GPT-3 175B (~73%)

> Resultados do artigo original: (((Zelikman 等人,2022):GPT-J  base modelo através da racionalização repetidas vezes STaR  rotas, no GSM8K aumentou de 5,8%                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

### V-STaR: treinar um verificador com o DPO

Os dados são também dados: cada par de (rationale, "is this correct") pode treinar um verificador. Eles usam a otimização de preferências diretas sobre soluções corretas e incorretas para construir um ranker.

> STaR  abandonar as conclusões incorretas──Hosseini 等人2024) observou que estas também são dados: por contra  processos de conclusão, "Ese é o caso de ser correto") podem ser treinados por verificadores.

Delta relatada: +4 a +17 pontos percentuais em relação às linhas de base de auto-melhoria anteriores no GSM8K e no MATH, com a maior parte do ganho proveniente da utilização do verificador para a seleção do tempo de inferência em vez de para o ajuste fino adicional do gerador.

> 報告の提升: GSM8K 和 MATH 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上 上

### Quiet-STaR: racionalidades internas por token

Zelikman et al. (2024) perguntou: e se o modelo aprende a gerar uma raciocínio interna curta em cada posição de token, não apenas entre problema e resposta? Quiet-STaR treina um modelo para emitir um "pensamento" oculto antes de cada token previsto, em seguida, mistura a previsão consciente do pensamento com a previsão de linha de base através de um peso aprendido.

> Zelikman  et al. 2024) propôs: se o modelo se reunir em cada token   posição gerar uma raciocínio interna breve, não apenas entre a questão e a resposta?

Resultado: Mistral 7B ganhou melhorias absolutas de zero-shot no GSM8K de 5,9% para 10,9% e CommonsenseQA de 36,3% para 47,2% sem ajuste específico de tarefa. O modelo aprendeu "quando pensar"  tokens duros obtêm racionalidades internas mais longas; os fáceis quase nenhuma.

> Resultado:Mistral 7B em GSM8K acima de zero amostra absolutamente aumentou de 5,9% para 10,9%, em CommonsenseQA de 36,3% para 47,2%, sem necessidade de tarefas específicas de micro-modução.

### Por que os três compartilham uma preocupação com a segurança

Os três métodos usam a resposta final como o sinal de gradiente. Uma razão que chega à resposta correta através de raciocínio defeituoso  explorando um atalho, adivinhando ou usando um padrão não generalizador  é reforçada positivamente. Em problemas de distribuição, o atalho funciona. Em problemas fora da distribuição, quebra em silêncio.

> Três métodos usam a resposta final como sinal de gradiente. O processo de argumentação de soluções erradas para obter uma resposta correta é reforçado de forma positiva.

O verificador do V-STaR atenuam aprendendo a classificar racionais, mas o verificador é treinado no mesmo conjunto de rótulos. Ele pode aprender a preferir o raciocínio errado bem formatado ao contrário de incerteza honesta. O design mais seguro é combinar dados no estilo STaR com (a) modelos de recompensa supervisionados pelo processo (recompensando passos intermediários, não apenas respostas) e (b) avaliação de OOD realizada que quebra atalhos simples.

> O verificador V-STaR é capaz de aprender a classificar as hipóteses, mas é treinado no mesmo conjunto de etiquetas. Pode ser que tenha um formato preferido de boa, mas errada, e não seja um tipo de incerteza.

### Comparativo

| Method | Training signal | Inference cost | Data waste | Known failure mode |
|---|---|---|---|---|
| 方法 | 训练信号 | 推理成本 | 数据浪费 | 已知失败模式 |
| STaR | keep (rationale, answer) if correct | 1x | discards all incorrect rationales | shortcut rationales |
| STaR | 正确时保留（推理，答案） | 1x | 丢弃所有不正确的推理 | 捷径推理 |
| STaR + rationalization | above + correct-answer hinted retries | 1x | less | rationalized rationales may be implausible |
| STaR + 合理化 | 上述 + 正确答案提示重试 | 1x | 较少 | 合理化的推理可能不可信 |
| V-STaR | STaR + DPO verifier from both classes | Nx (best-of-N) | minimal | verifier can reinforce confident wrongness |
| V-STaR | STaR + 两类 DPO 验证器 | Nx（N 中选优） | 最少 | 验证器可能强化自信的错误 |
| Quiet-STaR | per-token rationale + mixing weight | 1.5-3x | minimal | still answer-conditioned gradient |
| Quiet-STaR | 每 token 推理 + 混合权重 | 1.5-3x | 最少 | 仍是答案条件梯度 |

### Onde esta fica no monte de 2026

O STAR é velho. Mas o padrão reaparece em toda parte em 2025-2026. RL em problemas matemáticos verificáveis (DeepSeek-R1, Kimi-k1.5, o1) é o sinal de gradiente de resposta condicionado do STaR, aumentado. Os modelos de recompensa de processo (Lightman et al., 2023; "Verificemos passo a passo" da OpenAI) são a alternativa supervisionada pelo processo. AlphaEvolve (Lessão 3) é STaR para código, com um evaluador de programa em vez de um rótulo. Darwin Godel Machine (Lessão 4) é STaR para o próprio andaime do agente.

> STaR  muito velho. Mas este modelo surgiu em 2025-2026 anos de idade. RL ((DeepSeek-R1、Kimi-k1.5、o1) é a resposta de STaR 条件梯度信号的放大版──过程奖励模型──Lightman 等人,2023; OpenAI 的"逐步验证") é uma alternativa ao processo de supervisão──AlphaEvolve (III) 课) é um código de STaR, usado como um avaliador de programas em vez de um rótulo──Darwin Godel Machine (IV) é um agente 脚手架本身的 STaR──

Entender o STaR faz todos estes cliques. É o ciclo de auto-melhora mínimo viável.

> Entender que o STaR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

## Use-o com o framework implementado.
```figure
reflection-loop
```

## Usá-lo

`code/main.py`executa um ciclo STaR simulado numa tarefa aritmética de brinquedo.

- Como a precisão sobe sobre as balas de arranque.
  Tradução do inglês: 准确率如何在bootstrap 轮次中升──
- Como os atalhos se infiltram: o simulador inclui uma classe de raciocínio "voeiro" que obtém a resposta certa 40% das vezes, mas generaliza mal.
  O método de formação de um sistema de simulação contém um tipo de "pânico", 40% do tempo obtém respostas corretas, mas a generalização é muito ruim.
- Como um verificador (estilo V-STaR) ajuda na inferência, mas não pode recortar completamente os atalhos introduzidos durante o treinamento.
  Tradução do inglês para tradução do inglês: Testing Machine (V-STAR 风格)

## Envia-o . Produto .

`outputs/skill-star-loop-reviewer.md`ajuda a auditar um pipeline de raciocínio autodidacta antes de treinar.

> `outputs/skill-star-loop-reviewer.md` ajudar-te a avaliar o auto-aprendizagem do curso antes do treino 

## Exercícios.

1. Execute o simulador. Configure a frequência de atalho para zero, em seguida para 0,4.
   Tradução do inglês: Quantos pontos precisam ser divididos entre as duas operações, mesmo que ambos tenham atingido > 90% na distribuição de treino?

2. Adicione um teste de OOD prolongado ao simulador. Desenhe problemas de uma distribuição diferente e avalia o modelo arrancado em conjuntos de distribuição e OOD. Cuantifique a lacuna.
   Tradução do inglês: 量化差距──

3. Leia o artigo Quiet-STaR (arXiv:2403.09629) Secção 3. Explique o símbolo "final de pensamento" e a cabeça de peso de mistura em três frases cada.
   中文翻译:用三句话分别解释"思考结束"token 和混合权重头──

4. Compare o filtro de manutenção se correto da STaR com uma alternativa supervisionada por processos que recompensa cada passo racional de forma independente.
   Tradução do inglês para inglês: 识别标注成本差异和质量差异.

5. Desenhar uma avaliação que capture racionais de atalhos em um modelo implementado. Não precisa ser perfeito  tem que quebrar os atalhos mais simples que um ciclo STaR reforçaria.
   Tradução do inglês: It only needs to break the simplest way of strengthening the STaR cycle.

## Termos-chave .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| STaR | "Self-Taught Reasoner" | Fine-tune on model-generated rationales that land correct answers; repeat |
| STaR | "自我教学推理器" | 在模型生成的正确推理上微调；重复 |
| Rationalization | "Hinted retry" | Inject the correct answer and re-prompt for a rationale |
| 合理化 | "提示重试" | 注入正确答案重新提示推理 |
| V-STaR | "Verifier STaR" | DPO-train a verifier on both correct and incorrect rationales |
| V-STaR | "验证器 STaR" | DPO 训练验证器用于推理时选择 |
| Quiet-STaR | "Per-token rationales" | Generate hidden thoughts at every token position; mix with baseline |
| Quiet-STaR | "每 token 推理" | 在每个 token 位置生成隐藏思考；与基线预测混合 |
| Answer-conditioned gradient | "Outcome-based signal" | The training loop rewards final answers, not reasoning steps |
| 答案条件梯度 | "基于结果的信号" | 训练循环奖励最终答案，而非推理步骤 |
| Process reward model | "Step-level verifier" | Reward model trained on per-step correctness, not outcome |
| 过程奖励模型 | "步骤级验证器" | 在每步正确性上训练的奖励模型 |
| Shortcut rationale | "Right answer, wrong reasoning" | A rationale that reaches the label via a non-generalizing pattern |
| 捷径推理 | "正确答案，错误推理" | 通过不可泛化模式达到标签的推理 |

## Mais leitura 延伸阅读

- [Zelikman et al. (2022). STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465)- O papel original.
  Tradução do português:
- [Hosseini et al. (2024). V-STaR: Training Verifiers for Self-Taught Reasoners](https://arxiv.org/abs/2402.06457) adiciona um verificador DPO para a selecção do tempo de inferência.
  Chinese: 添加 DPO 验证器用于推理时选择──
- [Zelikman et al. (2024). Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking](https://arxiv.org/abs/2403.09629) rationalizações internas por token.
  Tradução do inglês:
- [Lightman et al. (2023). Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) Modelos de recompensa de processo, o sinal de gradiente alternativo.
  Tradução do inglês para tradução livre: process reward model,替代梯度信号──
- [DeepSeek-R1 paper (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948) RL em tarefas verificáveis, STaR escalado para formação de fronteira.
  Tradução do inglês para tradução do inglês: RL,STaR 扩展到前沿训练──
