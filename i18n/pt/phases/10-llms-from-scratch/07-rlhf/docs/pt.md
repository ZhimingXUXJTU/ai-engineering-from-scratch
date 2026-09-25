# RLHF: Modelo de recompensa + PPO baseado em aprendizagem de força humana contra o vírus.

> O SFT ensina o modelo a seguir instruções. Mas não ensina o modelo qual resposta é melhor. Duas respostas gramaticalmente corretas e factualmente precisas podem diferir enormemente em utilidade.

> **【中文解读】**O modelo da Igreja segue instruções, mas não ensina qual responder "melhor"―RLHF utiliza o modelo de recompensa de treinamento de dados preferidos por humanos, reutiliza o modelo de PPO  optimização estratégica para gerar respostas mais adequadas ao julgamento humano― é o que faz com que Claude tenha uso、GPT 礼貌的核心技术──

> **【拓展：PPO→ChatGPT对齐】**O RLHF do ChatGPT  treinar usando o algoritmo PPO : o modelo de recompensa dá respostas por pontuação, o PPO usa esse por cento como sinal de recompensa para otimizar estratégias.

> - Não .**【前置】**学本节前请先掌握:Fase 10·06(SFT) RLHF 起点是SFT 模型;Fase 09·08(PPO) 强化学习 PPO 算法基础;Fase 18·01(Instrução Seguindo) RLHF 在对齐中的位置──本节是Fase 10·08(DPO) 和Fase 18(Ética) 系列的前置──

**Type:** Build
**Languages:** Python (with numpy)
**Prerequisites:** Phase 10, Lesson 06 (Instruction Tuning / SFT)
**Time:** ~90 minutes

> - Não .**【类比】**RLHF = 訓練物学杂技。SFT é " fazer demonstração para fazer o cão se preocupar" ([[Supervisão de aprendizagem]])。RLHF é " cão fazer um movimento, você dar comida, você dar comida, você dar alta recompensa) ou ignorar ([[Premio baixo]]), cão慢慢学会讨零食的动作" ([[Strong化学习]])。 reward model = exibição em seu rosto (((preveto quais movimentos você vai receber recompensa),PPO = 狗调整动策略;;KL 惩罚 = "别太离谱"狗不能为了零食转圈咬自己尾巴──

> ️ **【易错点】**RLHF's 3 个坑:(1) **奖励模型过拟合**RM em preferência de dados acc=99%, mas generalização diferença; com maior RM + 早停 + 验证集监控──(2) **KL 系数设错**太大(> 0.5)模型不动如 SFT,太小(< 0.01)模型乱跑"奖励黑客"; típico 0.05-0.2──(3) **reward hacking** Modelo encontrou "加更多表情符号 RM 给高分",输出全是emoji; continuous monitoring output distribution, encontrou anormal imediatamente parada.

## Objetivos de aprendizagem

- Construir um modelo de recompensa que marque a qualidade da resposta dos pares de preferências humanas (escolhidos versus rejeitados)
  构建从人类偏好对(选择对拒绝)评分回复质量奖励模型
- Implementar o ciclo de formação PPO que otimiza uma política de modelo de linguagem contra o modelo de recompensa com uma penalidade KL
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
- Explique por que a RLHF exige três modelos (SFT, recompensa, política) e como a restrição KL impede o hacking de recompensas
  Explicação de por que a RLHF precisa de três modelos (SFTs, incentivos, estratégias) e como evitar que os clientes recebam um incentivo
- Avaliação do efeito do RLHF comparando a qualidade da resposta antes e após a otimização das preferências
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

> **【中文解读】**O RLHF é um sistema de informação e comunicação que permite a criação de dados e de dados para o seu uso.

## O problema é o problema da introdução

Pergunte a um modelo "Explicar a computação quântica" e ele pode produzir:

> 问模型"解释量子计算", é possível produzir:

**Response A:**"A computação quântica usa qubits que podem existir em superposição, o que significa que eles podem ser 0, 1 ou ambos simultaneamente. Isso permite que computadores quânticos processem certos cálculos exponencialmente mais rápido do que computadores clássicos. Algoritmos-chave incluem o algoritmo de Shor para factorizar grandes números e o algoritmo de Grover para pesquisar bases de dados não ordenadas".

> **回复 A：**"A utilização de cálculos quânticos pode estar em qubits de superposição, o que significa que eles podem ser simultaneamente 0 ̊1 ou dois. Isso permite que os computadores quânticos processem certos cálculos em comparação com os computadores clássicos.

**Response B:**"A computação quântica é um tipo de computação que usa fenômenos mecânicos quânticos. Foi proposto pela primeira vez na década de 1980. Richard Feynman sugeriu que os sistemas quânticos poderiam ser simulados por computadores quânticos. O campo cresceu significativamente desde então. Muitas empresas estão agora trabalhando em computadores quânticos. IBM, Google e outros fizeram progressos. A supremacia quântica foi reivindicada pelo Google em 2019".

> **回复 B：**"A computação quântica é uma forma de calcular usando o fenômeno da quântica. Foi apresentada pela primeira vez nos anos 1980.[3] Richard Feynman sugeriu que os sistemas quânticos possam ser imitados por computadores quânticos.[4] A partir deste momento, o campo desenvolveu-se significativamente.[4] Muitas empresas estão agora a desenvolver computadores quânticos e IBM, Google etc.

Ambas as respostas são factualmente corretas. Ambas são gramaticalmente sólidas. Ambas seguem as instruções. Mas a resposta A é claramente melhor. É mais concisa, mais informativa e melhor estruturada. Um ser humano escolheria A toda vez.

> 两回复事实上都正确――语法上都无问题――都遵循命令――但回复 A 明显更好――更简洁、更有信息量、结构更好――人类每次都会选 A――

O SFT não pode capturar essa distinção. Ele treina o modelo em respostas "corretas", mas não tem nenhum mecanismo para dizer "esta resposta é melhor do que aquela". Trata cada exemplo de treinamento como igualmente bom.

> A SFT não consegue capturar esta diferença. Está no modelo de treinamento "corretamente" repetido, mas não há mecanismo que diga "este feedback é melhor do que o outro".

A RLHF resolve isto. Treina um modelo de recompensa para prever qual resposta um ser humano preferiria, e depois usa esse sinal de recompensa para empurrar o modelo de linguagem para resultados de maior qualidade. O InstrutorGPT (o precursor do ChatGPT) usou RLHF para melhorar dramaticamente a utilidade, veracidade e inocuidade do GPT-3. Os avaliadores internos da OpenAI preferiram as saídas InstructGPT às saídas GPT-3 em 85% dos casos, apesar de a InstructGPT ser 135 vezes menor (1.3B vs 175B parâmetros).

> RLHF resolveu o problema. Ele treinou um modelo de recompensa para prever quais respostas as pessoas preferem, e então usou este sinal de recompensa para impulsionar o modelo de linguagem a gerar saídas de maior qualidade.

> **【中文解读】**A limitação da SFT está em que não consegue distinguir "qual é a melhor resposta" dois linguagens corretas ▌factos precisos podem ser diferentes na utilidade. RLHF  através de um modelo de incentivo treinado para prever as preferências humanas, reutiliza este modelo de incentivo para gerar uma saída de maior qualidade. Instruir GPT  O ex-presidente do GPT                                                                                                                                                                                                               

> **【拓展：InstructGPT 的突破】**IntroduçãoGPT 论文(OpenAI 2022)  RLHF 应用于大模型的里程碑──关键发现:(1) 1.3B 参数的RLHF 模型优于175B 的原始GPT-3;(2) RLHF 显著减少有害输出(毒性降低约80%);(3) 真实性也升升.

## O conceito central.

### As três etapas

O RLHF não é uma única corrida de treinamento, é um conjunto de três etapas sequenciais, cada uma construindo sobre a anterior.

> RLHF não é um único treinamento de execução. É uma linha de ordem de três fases, cada fase é construída sobre o anterior.

**Stage 1: SFT.**Treinar um modelo base em pares de instruções e respostas (Lessão 06).

> **阶段 1：SFT。**Em instrução-repetir para o modelo básico de treinamento superior (第六课) . Isso dá-lhe um modelo que pode seguir instruções, mas não sabe qual é o melhor.

**Stage 2: Reward Model.**Recolha dados de preferências humanas: mostre aos anotadores duas respostas ao mesmo prompt e pergunte "o que é melhor?" Treine um modelo para prever essas preferências.

> **阶段 2：奖励模型。**收集人类偏好数据:向标标记者展示对同一提示的两个回复并问"哪个更好?"训练一个模型来预测这些偏好―― recompensa modelo以 (prompto, resposta) 为输入,输出一个标量分数――

**Stage 3: PPO.**Use o modelo de recompensa para gerar um sinal de treinamento para o modelo de linguagem. O modelo de linguagem gera respostas, o modelo de recompensa as marca e o PPO atualiza o modelo de linguagem para produzir respostas com pontuação maior. Uma penalidade de divergência KL impede que o modelo de linguagem se afaste muito do ponto de controle SFT.

> **阶段 3：PPO。**Utilize reward model for language model generate training signal. Language model generate feedback.

> **【中文解读】**O RLHF utiliza três fases de tubo: Estação 1 para que o SFT 让基础模型学会跟随指令; Estação 2 para que o SFT 让基础模型学会跟随指令; Estação 2 para que o SFT 让基础模型学会跟随指令; Estação 2 para que o SFT 让基础模型学会跟随指令; Estação 2 para que o SFT 让基础模型学会跟随指令; Estação 2 para que o SFT 让基础模型学会跟随指令; Estação 2 para que o SFT 让基础模型学会跟随指令; Estação 2 收集人类偏好数据; Estação 2 收集人类偏好数据; Estação 2 收集人类偏好数据; Stage 3 para que o PPO 算法 让策略模型产生高奖励的回复,同时, utiliza KL 散度惩罚防止偏离 SFT 模型. KL 惩罚是反奖励黑客的关键没有它,策略会发现奖励模型的漏洞而不是真正改善输出质量.

```mermaid
graph TD
    subgraph Stage1["Stage 1: SFT"]
        B["Base Model"] --> S["SFT Model"]
        D["Instruction Data\n(27K examples)"] --> S
    end

    subgraph Stage2["Stage 2: Reward Model"]
        S --> |"Generate responses"| P["Preference Pairs\n(prompt, winner, loser)"]
        H["Human Annotators"] --> P
        P --> R["Reward Model\nR(prompt, response) → score"]
    end

    subgraph Stage3["Stage 3: PPO"]
        S --> |"Initialize policy"| PI["Policy Model\n(being optimized)"]
        S --> |"Freeze as reference"| REF["Reference Model\n(frozen SFT)"]
        PI --> |"Generate"| RESP["Response"]
        RESP --> R
        R --> |"Reward signal"| PPO["PPO Update"]
        REF --> |"KL penalty"| PPO
        PPO --> |"Update"| PI
    end

    style S fill:#1a1a2e,stroke:#51cf66,color:#fff
    style R fill:#1a1a2e,stroke:#e94560,color:#fff
    style PI fill:#1a1a2e,stroke:#0f3460,color:#fff
    style REF fill:#1a1a2e,stroke:#0f3460,color:#fff
    style PPO fill:#1a1a2e,stroke:#e94560,color:#fff
```

### O Modelo de Recompensa

O modelo de recompensa é um modelo de linguagem reutilizado como um marcador. Pegue o modelo SFT, substitua o cabeçalho de modelagem de linguagem (que produz uma distribuição sobre o vocabulário) por um cabeçalho escalar (que produz um único número). A arquitetura é idêntica até a camada final.

> 奖励模型是重新使用作评分器的语言模型──取 SFT 模型,将语言建模头 (output word表上的分布) 换成标量头 (output单个数字) ‖架构直到最后层都相同──

Input: um prompt concatenado com uma resposta.

> 输入: 一个提示 拼接一个回复――输出: 一个标量奖励分数――

Os dados de treinamento são pares de preferências humanas. Para cada pedido, os anotadores veem duas respostas e escolhem a melhor.

> 訓練資料是人類偏好對──對每個提示,標標記者看到兩回复并選擇更好──這創建了訓練三元组:(prompt, 首选回复, 拒绝回复)──

A função de perda usa o modelo Bradley-Terry de preferências em pares:

```
loss = -log(sigmoid(reward(preferred) - reward(rejected)))
```

Esta é a equação chave.`sigmoid(reward(A) - reward(B))`dá a probabilidade de que a resposta A seja preferida à resposta B. A perda empurra o modelo de recompensa para atribuir uma pontuação mais alta à resposta preferida.

> É o caminho mais importante.`sigmoid(reward(A) - reward(B))`给出回复 A 被偏好于回复 B 的概率──损失推动奖励模型给首选回复分配更高分数──

Por que comparações em pares em vez de pontuações absolutas? Porque os seres humanos são terríveis em atribuir pontuações de qualidade absoluta ("É esta resposta um 7,3 ou um 7,5 de 10?") mas muito bons em comparações relativas ("É A melhor que B?"). O modelo Bradley-Terry converte comparações relativas em um sistema consistente de pontuação absoluta.

> Por que usar o comparativo em vez de classificação absoluta? Porque os seres humanos não são bons em distribuir classificações de qualidade absoluta (((" essa resposta é 7,3 ou 7,5 em 10 minutos?") mas são bons em comparação ((("A é melhor do que B?")  O modelo Bradley-Terry irá transformar a comparação em um sistema de classificação absoluta em conformidade;;

**InstructGPT numbers:**A OpenAI recolheu 33.000 pares de comparação de 40 empreiteiros. Cada comparação levou cerca de 5 minutos. Isso é 2.750 horas de trabalho humano para os dados do modelo de treinamento de recompensa.

> **InstructGPT 数据：**A OpenAI reuniu 33 mil comparativos de 40 empreiteiros. Cada comparativo custou cerca de 5 minutos.

### PPO: Otimizar as políticas próximas

O PPO é um algoritmo de aprendizado de reforço. Na RLHF, o "ambiente" é o modelo de recompensa, o "agente" é o modelo de linguagem e a "ação" está gerando um token.

> O PPO é um algoritmo de aprendizagem de força. No RLHF, "ambiente" é um modelo de recompensa, "智能体" é um modelo de linguagem, "动作" é gerar um token.

O objectivo:

> 优化目标:

```
maximize: E[R(prompt, response)] - beta * KL(policy || reference)
```

O primeiro termo empurra o modelo para gerar respostas de alta recompensa. O segundo termo (penalidade de divergência KL) impede que o modelo se desvie muito longe do ponto de controlo SFT.

> Primeiro, promover o modelo gerar alta recompensa, segundo, impedir o modelo desviar-se da SFT.

Por que a penalidade KL? Sem ela, o modelo encontra soluções degeneradas. O modelo de recompensa é treinado em um conjunto finito de dados de preferências humanas. Tem pontos cegos. O modelo de linguagem explorará esses pontos cegos - encontrando resultados que pontuação alta no modelo de recompensa, mas são realmente insensatos. Exemplos clássicos:

> Por que precisa KL  punição? sem ele, o modelo encontrará soluções degradadas. O modelo de recompensa treinará em um conjunto limitado de dados de preferências humanas, tem pontos cegos. O modelo de linguagem usará esses pontos cegos para encontrar resultados de alta, mas não significativos, no modelo de recompensa.

- Repetição de "Sou tão útil e inofensivo!" tem pontuações elevadas nos modelos de recompensa de ajuda/inharmonia
  Tradução do inglês para "I'm very useful very harmless!"
- Produzir respostas verbais, formalmente sonoras, mas vazias que correspondem a padrões de "alta qualidade"
  Tradução do inglês para "Generar冗长、 formal, mas em vão"
- Exploração de frases específicas que se correlacionaram com alta recompensa nos dados de formação
  Tradução do inglês para tradução do inglês: utilise training data 中恰好与高奖励相关的特定短语

A penalidade KL diz: você pode melhorar, mas não pode se tornar um modelo completamente diferente. Fique perto da versão SFT, que já era razoável.

> KL 惩罚说: Você pode melhorar, mas não pode se tornar um modelo completamente diferente.

**InstructGPT numbers:**O treinamento de PPO usou lr=1.5e-5, coeficiente KL beta=0.02, 256K episódios (pares de resposta rápida) e 4 épocas de PPO por lote.

> **InstructGPT 数据：**O treinamento de PPO usando lr=1.5e-5, KL 系數β=0.02,256K 个集 (pp), por lote 4 个 PPO époque── toda a RLHF 管线在 GPU 集群上运行了几天──

```mermaid
graph LR
    subgraph PPO["PPO Training Loop"]
        direction TB
        PROMPT["Sample prompt\nfrom dataset"] --> GEN["Policy generates\nresponse"]
        GEN --> SCORE["Reward model\nscores response"]
        GEN --> KL["Compute KL divergence\nvs reference model"]
        SCORE --> OBJ["Objective:\nreward - beta * KL"]
        KL --> OBJ
        OBJ --> UPDATE["PPO gradient update\n(clipped surrogate loss)"]
        UPDATE --> |"repeat"| PROMPT
    end

    style PROMPT fill:#1a1a2e,stroke:#0f3460,color:#fff
    style SCORE fill:#1a1a2e,stroke:#51cf66,color:#fff
    style KL fill:#1a1a2e,stroke:#e94560,color:#fff
    style OBJ fill:#1a1a2e,stroke:#e94560,color:#fff
```

### Objectivo do PPO em Detalhes

O PPO usa um "objetivo substituto cortado" para evitar atualizações excessivamente grandes. A relação entre a nova política e as probabilidades de política antiga é cortada para a faixa [1 - epsilon, 1 + epsilon], onde o epsilon é tipicamente 0,2.

> O PPO usa "Objetivo de intercepção" para evitar grandes atualizações. A taxa entre as probabilidades de novas estratégias é interceptada em intervalos de [1 - epsilon, 1 + epsilon], entre os quais o epsilon geralmente é de 0,2 epsilon.

```
ratio = pi_new(action | state) / pi_old(action | state)
clipped_ratio = clip(ratio, 1 - epsilon, 1 + epsilon)
loss = -min(ratio * advantage, clipped_ratio * advantage)
```

A função vantagem estima o quanto melhor a resposta atual é comparada à qualidade esperada.

> 优势函数估计当前回复比期望质量 优势函数估计当前回复比期望质量 优势函数估计当前回复比期望质量 优势函数估计当前回复比期望质量 优势函数估计当前回复比期望质量 优势函数估计当前回复比期望质量 优势函数估计当前回复比期望质量 优势函数估计当前回复比期望量 优势函数估计当前回复比期望量 优势函数估计当前回复比期望量 优势函数估计当前回复比期期期期期期期期期期期期期期量 优势函数数

```
advantage = reward(prompt, response) - baseline
```

A linha de base é muitas vezes a recompensa média em relação às respostas recentes. Uma vantagem positiva significa que a resposta foi melhor do que a média; uma vantagem negativa significa que foi pior.

> O benefício positivo significa melhor do que o nível médio; o benefício negativo significa diferença do nível médio. O PPO aumenta a probabilidade de resposta acima do nível médio, reduz a probabilidade de resposta abaixo do nível médio.

O corte evita atualizações catastróficas. Se uma única resposta recebe uma recompensa incomumente alta, a relação não cortada pode ser muito grande, fazendo com que o modelo mude drasticamente em direção a essa resposta.

> 截断防止灾难性更新── Se uma única repetição recebe um ganho anormalmente alto, a taxa de não interrupção pode ser muito grande, levando o modelo a se deslocar drasticamente para essa repetição──截断限制更新幅度, manter o treinamento estável──

### Recompensas de Hacking

O lado negro da RLHF. O modelo de linguagem está otimizando contra o modelo de recompensa, que é um proxy imperfeito para as preferências humanas. À medida que o modelo de linguagem melhora na maximização da recompensa, começa a explorar as fraquezas do modelo de recompensa.

> O modelo de linguagem da RLHF é o ideal do modelo de recompensa, enquanto o modelo de recompensa é o agente imperfeito das preferências humanas.

Modos comuns de falha:

> 常见失败模式:

| Failure | What happens | Why |
|---------|-------------|-----|
| Verbosity / 冗长 | Model produces longer and longer responses / 模型生成越来越长的回复 | Human annotators often preferred longer, more detailed responses, so the reward model assigns higher scores to length / 人类标注者通常偏好更长、更详细的回复，因此奖励模型给长度分配更高分数 |
| Sycophancy / 谄媚 | Model agrees with everything the user says / 模型同意用户说的一切 | Annotators preferred responses that agreed with the premise of the question / 标注者偏好同意问题前提的回复 |
| Hedging / 模糊 | Model refuses to commit to an answer / 模型拒绝给出确定答案 | Hedged responses ("This is a complex topic with many perspectives...") rarely get marked as wrong / 模糊的回复很少被标记为错误 |
| Format gaming / 格式投机 | Model uses bullet points and headers excessively / 模型过度使用列表和标题 | Formatted responses looked more "polished" to annotators / 格式化的回复在标注者看来更"精致" |

Estratégias de mitigação: penalização KL mais forte (impede que o modelo se desvie o suficiente para explorar fraquezas), treinamento do modelo de recompensa em exemplos adversários (modos de falha conhecidos de patch) e uso de vários modelos de recompensa com diferentes arquiteturas (mais difícil de hackear todos simultaneamente).

> 缓解策略:更强的 KL 惩罚(prevenir o modelo desviar para suficiente para utilizar o grau de fraqueza)  treinar o modelo de recompensa em frente a um modelo de prova (reconstruir o modelo de fracasso conhecido)  usar vários modelos de recompensa de diferentes estruturas ((更难同时攻破所有模型) 

### Empréstimos de energia

| Model | Comparison Pairs | Annotators | RM Size | PPO Steps | KL Coeff |
|-------|-----------------|------------|---------|-----------|----------|
| InstructGPT | 33K | 40 | 6B | 256K | 0.02 |
| Llama 2 Chat | ~1M | undisclosed | 70B | undisclosed | 0.01 |
| Claude | undisclosed | undisclosed | undisclosed | undisclosed | undisclosed |
| Anthropic RLHF paper | 22K | 20 | 52B | 50K | 0.001 |

> Configuração de treinamento RLHF de cada modelo:InstructGPT usando 33K  preferência contra 6B  modelo de recompensa;Llama 2 Chat usando cerca de 1M  preferência contra 70B  modelo de recompensa;Antropic RLHF 论文在 22K比较上训练了52B 的奖励模型──

O artigo de 2022 da Anthropic treinou um modelo de recompensa 52B em 22.000 comparações. Os modelos de recompensa maiores produzem sinais mais confiáveis, o que torna o treinamento de PPO mais estável. Usar um modelo de recompensa pequeno para treinar um modelo de linguagem grande é arriscado - o modelo de recompensa não tem capacidade suficiente para capturar as nuances de respostas boas versus ruins.

> O artigo do Anthropic 2022 comparou com 22.000 pessoas o modelo de recompensa de 52B. O modelo de recompensa maior produz sinais mais confiáveis, fazendo o treinamento de PPO mais estável. O modelo de recompensa menor é um modelo de risco. O modelo de recompensa não tem capacidade suficiente para capturar as pequenas diferenças entre boa resposta e boa resposta.

## Construí-lo e realizei-o.
```figure
rlhf-pipeline
```

## Construí-lo

### Passo 1: Dados de preferência sintéticos

Na produção, os anotadores humanos criam dados de preferência. Criaremos pares sintéticos onde a resposta "preferida" é objetivamente melhor (mais concisa, mais precisa, mais útil).

> Em produção, os marcadores humanos criam dados preferenciais. Vamos criar um conjunto de dados, entre os quais "首选"回复客观上更好 (pior simples, mais preciso, mais útil)

```python
import numpy as np

PREFERENCE_DATA = [
    {
        "prompt": "What is the capital of France?",
        "preferred": "The capital of France is Paris.",
        "rejected": "France is a country in Europe. It has many cities. The capital is Paris. Paris is known for the Eiffel Tower.",
    },
    {
        "prompt": "Explain gravity in one sentence.",
        "preferred": "Gravity is the force that attracts objects with mass toward each other.",
        "rejected": "Gravity is something that makes things fall down when you drop them.",
    },
    {
        "prompt": "What is 15 times 7?",
        "preferred": "15 times 7 is 105.",
        "rejected": "Let me think about this. 15 times 7. Well, 10 times 7 is 70, and 5 times 7 is 35, so the answer might be around 105.",
    },
    {
        "prompt": "Name three programming languages.",
        "preferred": "Python, Rust, and TypeScript.",
        "rejected": "There are many programming languages. Some popular ones include various languages like Python and others.",
    },
    {
        "prompt": "What year did World War II end?",
        "preferred": "World War II ended in 1945.",
        "rejected": "World War II was a major global conflict. It involved many countries. The war ended in the mid-1940s, specifically in 1945.",
    },
    {
        "prompt": "Define machine learning.",
        "preferred": "Machine learning is a field where algorithms learn patterns from data to make predictions without being explicitly programmed.",
        "rejected": "Machine learning is a type of AI. AI stands for artificial intelligence. Machine learning uses data to learn.",
    },
]
```

As respostas preferidas são concisas e diretas. As respostas rejeitadas apresentam modos de falha comuns: enchimento desnecessário, cobertura, explicação redundante e impreciso. Este é exatamente o tipo de distinção que a SFT não pode capturar, mas a RLHF pode.

> 首选回复简洁直接──被拒回复展示常见失败模式:不必要的填充、模糊、冗余解释和不精确── é uma forma de SFT não ser capturado, mas RLHF pode distinguir diferenças──

### Passo 2: Arquitetura Modelo de Recompensa

O modelo de recompensa reutiliza a arquitetura do transformador do mini GPT, mas substitui a cabeça de saída do tamanho do vocabulário com uma única projeção escalar.

> O modelo de recompensa repetiu a estrutura de transformador do mini GPT, mas substituirá o tamanho do volume de saída do seu volume para um único volume de projeção.

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "04-pre-training-mini-gpt", "code"))
from main import MiniGPT, LayerNorm, Embedding, TransformerBlock


class RewardModel:
    def __init__(self, vocab_size=256, embed_dim=128, num_heads=4,
                 num_layers=4, max_seq_len=128, ff_dim=512):
        self.embedding = Embedding(vocab_size, embed_dim, max_seq_len)
        self.blocks = [
            TransformerBlock(embed_dim, num_heads, ff_dim)
            for _ in range(num_layers)
        ]
        self.ln_f = LayerNorm(embed_dim)
        self.reward_head = np.random.randn(embed_dim) * 0.02

    def forward(self, token_ids):
        seq_len = token_ids.shape[-1]
        mask = np.triu(np.full((seq_len, seq_len), -1e9), k=1)

        x = self.embedding.forward(token_ids)
        for block in self.blocks:
            x = block.forward(x, mask)
        x = self.ln_f.forward(x)

        last_hidden = x[:, -1, :]
        reward = last_hidden @ self.reward_head

        return reward
```

O modelo de recompensa leva o estado oculto na posição do token *last* e o projeta para um escalar. Por que o último token? Porque a máscara de atenção causal significa que a última posição atendeu a cada token anterior. Tem a representação mais completa de toda a sequência (prompt, resposta).

> O modelo de recompensa leva o último token  posição do estado oculto e projecta para a quantidade de token. Por que é o último token? Porque o factor de atenção escondido significa que a última posição já está atenta a todos os tokens anteriores.

### Passo 3: Perdida Bradley-Terry

Treinar o modelo de recompensa em pares de preferências usando a perda em pares Bradley-Terry.

> Utilize Bradley-Terry 成对损失在偏好对上训奖励模型.

```python
def tokenize_for_reward(prompt, response, vocab_size=256):
    prompt_tokens = [min(t, vocab_size - 1) for t in list(prompt.encode("utf-8"))]
    response_tokens = [min(t, vocab_size - 1) for t in list(response.encode("utf-8"))]
    return prompt_tokens + [0] + response_tokens


def sigmoid(x):
    return np.where(
        x >= 0,
        1.0 / (1.0 + np.exp(-x)),
        np.exp(x) / (1.0 + np.exp(x))
    )


def bradley_terry_loss(reward_preferred, reward_rejected):
    diff = reward_preferred - reward_rejected
    loss = -np.log(sigmoid(diff) + 1e-8)
    return loss


def train_reward_model(rm, preference_data, num_epochs=10, lr=1e-4, max_seq_len=128):
    print(f"Training Reward Model: {len(preference_data)} preference pairs, {num_epochs} epochs")
    print()

    losses = []
    accuracies = []

    for epoch in range(num_epochs):
        epoch_loss = 0.0
        epoch_correct = 0
        num_pairs = 0

        indices = np.random.permutation(len(preference_data))

        for idx in indices:
            pair = preference_data[idx]

            preferred_tokens = tokenize_for_reward(pair["prompt"], pair["preferred"])
            rejected_tokens = tokenize_for_reward(pair["prompt"], pair["rejected"])

            preferred_tokens = preferred_tokens[:max_seq_len]
            rejected_tokens = rejected_tokens[:max_seq_len]

            preferred_ids = np.array(preferred_tokens).reshape(1, -1)
            rejected_ids = np.array(rejected_tokens).reshape(1, -1)

            r_preferred = rm.forward(preferred_ids)[0]
            r_rejected = rm.forward(rejected_ids)[0]

            loss = bradley_terry_loss(r_preferred, r_rejected)

            if r_preferred > r_rejected:
                epoch_correct += 1

            diff = r_preferred - r_rejected
            grad = sigmoid(diff) - 1.0

            rm.reward_head -= lr * grad * rm.ln_f.forward(
                rm.embedding.forward(preferred_ids)
            )[:, -1, :].flatten()

            epoch_loss += loss
            num_pairs += 1

        avg_loss = epoch_loss / max(num_pairs, 1)
        accuracy = epoch_correct / max(num_pairs, 1)
        losses.append(avg_loss)
        accuracies.append(accuracy)

        if epoch % 2 == 0:
            print(f"  Epoch {epoch + 1:3d} | Loss: {avg_loss:.4f} | Accuracy: {accuracy:.1%}")

    return rm, losses, accuracies
```

A métrica de precisão é simples: qual fração dos pares de preferências o modelo de recompensa classifica corretamente? Um modelo aleatório tem uma pontuação de 50%. Um modelo de remuneração bem treinado em dados limpos deve exceder 70%. O modelo de recompensa da InstructGPT alcançou uma precisão de cerca de 72% em comparações prolongadas, o que soa baixo, mas é realmente bom - muitos pares de preferências são ambíguas, mesmo para os seres humanos (o acordo entre os anotadores foi de cerca de 73%).

>  Precisão de índice é muito intuitivo: qual é a preferência para a proporção de classificação correta do modelo de recompensa?  Aspecto de modelo de pontuação 50%  O modelo de recompensa bem treinado em dados de limpeza deve ser superior a 70%  InstructGPT's model de recompensa alcançou cerca de 72% de precisão em comparação com a retenção, parece baixo, mas na realidade muito bom Muitas preferências para os seres humanos também têm diferenças  Concordância entre marcadores é de cerca de 73%.

### Passo 4: Loop simplificado de PPO

A implementação completa do PPO é complexa. Esta implementação capta o mecanismo central: gerar respostas, pontua-las, calcular a vantagem e atualizar a política com uma penalidade KL.

> O PPO completo é muito complexo. Esta implementação captura o mecanismo central: gerar feedback, avaliação, vantagem de cálculo, usando estratégias de KL.

```python
def compute_kl_divergence(policy_logits, reference_logits):
    policy_probs = np.exp(policy_logits - policy_logits.max(axis=-1, keepdims=True))
    policy_probs = policy_probs / policy_probs.sum(axis=-1, keepdims=True)
    policy_probs = np.clip(policy_probs, 1e-10, 1.0)

    ref_probs = np.exp(reference_logits - reference_logits.max(axis=-1, keepdims=True))
    ref_probs = ref_probs / ref_probs.sum(axis=-1, keepdims=True)
    ref_probs = np.clip(ref_probs, 1e-10, 1.0)

    kl = np.sum(policy_probs * np.log(policy_probs / ref_probs), axis=-1)
    return kl.mean()


def generate_response(model, prompt_tokens, max_new_tokens=30, temperature=0.8, max_seq_len=128):
    tokens = list(prompt_tokens)

    for _ in range(max_new_tokens):
        context = np.array(tokens[-max_seq_len:]).reshape(1, -1)
        logits = model.forward(context)
        next_logits = logits[0, -1, :]

        next_logits = next_logits / max(temperature, 1e-8)
        probs = np.exp(next_logits - next_logits.max())
        probs = probs / probs.sum()
        probs = np.clip(probs, 1e-10, 1.0)
        probs = probs / probs.sum()

        next_token = np.random.choice(len(probs), p=probs)
        tokens.append(int(next_token))

    return tokens


def copy_model_weights(source, target):
    target.embedding.token_embed = source.embedding.token_embed.copy()
    target.embedding.pos_embed = source.embedding.pos_embed.copy()
    target.ln_f.gamma = source.ln_f.gamma.copy()
    target.ln_f.beta = source.ln_f.beta.copy()
    for s_block, t_block in zip(source.blocks, target.blocks):
        t_block.attn.W_q = s_block.attn.W_q.copy()
        t_block.attn.W_k = s_block.attn.W_k.copy()
        t_block.attn.W_v = s_block.attn.W_v.copy()
        t_block.attn.W_out = s_block.attn.W_out.copy()
        t_block.ffn.W1 = s_block.ffn.W1.copy()
        t_block.ffn.W2 = s_block.ffn.W2.copy()
        t_block.ffn.b1 = s_block.ffn.b1.copy()
        t_block.ffn.b2 = s_block.ffn.b2.copy()
        t_block.ln1.gamma = s_block.ln1.gamma.copy()
        t_block.ln1.beta = s_block.ln1.beta.copy()
        t_block.ln2.gamma = s_block.ln2.gamma.copy()
        t_block.ln2.beta = s_block.ln2.beta.copy()


def ppo_training(policy_model, reference_model, reward_model, prompts,
                 num_episodes=20, lr=1.5e-5, kl_coeff=0.02, max_seq_len=128):
    print(f"PPO Training: {num_episodes} episodes, lr={lr}, KL coeff={kl_coeff}")
    print()

    rewards_history = []
    kl_history = []

    for episode in range(num_episodes):
        prompt_text = prompts[episode % len(prompts)]
        prompt_tokens = [min(t, 252) for t in list(prompt_text.encode("utf-8"))]

        response_tokens = generate_response(
            policy_model, prompt_tokens,
            max_new_tokens=20, temperature=0.8, max_seq_len=max_seq_len
        )

        response_ids = np.array(response_tokens[:max_seq_len]).reshape(1, -1)
        reward = reward_model.forward(response_ids)[0]

        policy_logits = policy_model.forward(response_ids)
        ref_logits = reference_model.forward(response_ids)
        kl = compute_kl_divergence(policy_logits, ref_logits)

        total_reward = reward - kl_coeff * kl

        rewards_history.append(float(reward))
        kl_history.append(float(kl))

        for block in policy_model.blocks:
            update_scale = lr * total_reward
            block.ffn.W1 += update_scale * np.random.randn(*block.ffn.W1.shape) * 0.01
            block.ffn.W2 += update_scale * np.random.randn(*block.ffn.W2.shape) * 0.01

        if episode % 5 == 0:
            avg_reward = np.mean(rewards_history[-5:]) if rewards_history else 0
            avg_kl = np.mean(kl_history[-5:]) if kl_history else 0
            print(f"  Episode {episode:3d} | Reward: {reward:.4f} | KL: {kl:.4f} | "
                  f"Avg Reward: {avg_reward:.4f}")

    return policy_model, rewards_history, kl_history
```

O ciclo central: (1) amostrar um pedido, (2) gerar uma resposta, (3) avaliá-lo com o modelo de recompensa, (4) calcular a divergência KL contra a referência congelada, (5) calcular a recompensa ajustada (recompensa menos penalidade KL), (6) atualizar a política. A penalidade KL aumenta à medida que a política se diverge da referência, evitando automaticamente o hacking de recompensa.

> 核心循环:(1) 采样一个提示,(2) 生成回复,(3) 用奖励模型评分,(4) 计算与结参考模型的 KL 散度,(5) 计算调整后的奖励(奖励减 KL 惩罚),(6) 更新策略──KL 惩罚随策略偏离参考模型而增长,自动防止奖励黑客──

### Passo 5: Comparar as notas de recompensa

Após o RLHF, as respostas do modelo de política devem obter uma pontuação mais elevada no modelo de recompensa do que as respostas do modelo SFT original.

> Após RLHF, a resposta do modelo estratégico no modelo de recompensa deve ser superior à resposta do modelo SFT original.

```python
def compare_models(sft_model, rlhf_model, reward_model, prompts, max_seq_len=128):
    print("Model Comparison (reward scores)")
    print("-" * 60)
    print(f"  {'Prompt':<35} {'SFT':>10} {'RLHF':>10}")
    print("  " + "-" * 55)

    sft_total = 0.0
    rlhf_total = 0.0

    for prompt in prompts:
        prompt_tokens = [min(t, 252) for t in list(prompt.encode("utf-8"))]

        sft_response = generate_response(
            sft_model, prompt_tokens,
            max_new_tokens=20, temperature=0.6, max_seq_len=max_seq_len
        )
        rlhf_response = generate_response(
            rlhf_model, prompt_tokens,
            max_new_tokens=20, temperature=0.6, max_seq_len=max_seq_len
        )

        sft_ids = np.array(sft_response[:max_seq_len]).reshape(1, -1)
        rlhf_ids = np.array(rlhf_response[:max_seq_len]).reshape(1, -1)

        sft_reward = reward_model.forward(sft_ids)[0]
        rlhf_reward = reward_model.forward(rlhf_ids)[0]

        sft_total += sft_reward
        rlhf_total += rlhf_reward

        truncated_prompt = prompt[:33] + ".." if len(prompt) > 35 else prompt
        print(f"  {truncated_prompt:<35} {sft_reward:>10.4f} {rlhf_reward:>10.4f}")

    n = len(prompts)
    print("  " + "-" * 55)
    print(f"  {'Average':<35} {sft_total/n:>10.4f} {rlhf_total/n:>10.4f}")

    return sft_total / n, rlhf_total / n
```

## Use-o com o framework implementado.

### Demo completo do oleoduto RLHF

```python
if __name__ == "__main__":
    np.random.seed(42)

    print("=" * 70)
    print("RLHF PIPELINE: REWARD MODEL + PPO")
    print("=" * 70)
    print()

    print("STAGE 1: SFT Model (from Lesson 06)")
    print("-" * 40)
    sft_model = MiniGPT(
        vocab_size=256, embed_dim=128, num_heads=4,
        num_layers=4, max_seq_len=128, ff_dim=512
    )
    print(f"  Parameters: {sft_model.count_parameters():,}")
    print()

    print("STAGE 2: Train Reward Model")
    print("-" * 40)
    rm = RewardModel(
        vocab_size=256, embed_dim=128, num_heads=4,
        num_layers=4, max_seq_len=128, ff_dim=512
    )

    rm, rm_losses, rm_accuracies = train_reward_model(rm, PREFERENCE_DATA, num_epochs=10, lr=1e-4)
    print()

    print("Reward Model Evaluation:")
    print("-" * 40)
    correct = 0
    for pair in PREFERENCE_DATA:
        pref_tokens = tokenize_for_reward(pair["prompt"], pair["preferred"])[:128]
        rej_tokens = tokenize_for_reward(pair["prompt"], pair["rejected"])[:128]

        r_pref = rm.forward(np.array(pref_tokens).reshape(1, -1))[0]
        r_rej = rm.forward(np.array(rej_tokens).reshape(1, -1))[0]

        if r_pref > r_rej:
            correct += 1
        print(f"  Preferred: {r_pref:+.4f} | Rejected: {r_rej:+.4f} | {'Correct' if r_pref > r_rej else 'Wrong'}")

    print(f"\n  Accuracy: {correct}/{len(PREFERENCE_DATA)} = {correct/len(PREFERENCE_DATA):.1%}")
    print()

    print("STAGE 3: PPO Training")
    print("-" * 40)

    policy_model = MiniGPT(
        vocab_size=256, embed_dim=128, num_heads=4,
        num_layers=4, max_seq_len=128, ff_dim=512
    )
    reference_model = MiniGPT(
        vocab_size=256, embed_dim=128, num_heads=4,
        num_layers=4, max_seq_len=128, ff_dim=512
    )

    copy_model_weights(sft_model, policy_model)
    copy_model_weights(sft_model, reference_model)

    train_prompts = [pair["prompt"] for pair in PREFERENCE_DATA]

    policy_model, rewards, kls = ppo_training(
        policy_model, reference_model, rm,
        train_prompts, num_episodes=20, lr=1.5e-5, kl_coeff=0.02
    )
    print()

    print("=" * 70)
    print("COMPARISON: SFT vs RLHF")
    print("=" * 70)
    print()

    eval_prompts = [
        "What is the capital of France?",
        "Explain gravity.",
        "Name three programming languages.",
    ]

    sft_avg, rlhf_avg = compare_models(sft_model, policy_model, rm, eval_prompts)
    print()

    print("=" * 70)
    print("KL DIVERGENCE ANALYSIS")
    print("=" * 70)
    print()

    if kls:
        print(f"  Initial KL: {kls[0]:.4f}")
        print(f"  Final KL:   {kls[-1]:.4f}")
        print(f"  Max KL:     {max(kls):.4f}")
        kl_threshold = 0.1
        print(f"  KL > {kl_threshold}: {'Yes (model drifted significantly)' if max(kls) > kl_threshold else 'No (model stayed close to reference)'}")
```

## Envia-o . Produto .

Esta lição produz`outputs/prompt-reward-model-designer.md`- um prompt para a concepção de canais de treinamento de modelos de recompensa. Dado um comportamento alvo (utilidade, capacidade de codificação, segurança), produz um protocolo de coleta de dados, diretrizes de anotador e critérios de avaliação de modelos de recompensa.

> 本课产 出 `outputs/prompt-reward-model-designer.md` Um prompt para a formação de um modelo de recompensa para desenho.

## Exercícios.

1. Modifique o modelo de recompensa para usar a média de todos os estados ocultos em vez apenas da última posição. Comparar precisão. A abordagem de pooling média dá a cada token igual peso, enquanto a abordagem da última posição depende da atenção causal para informações agregadas. Teste nos 6 pares de preferências e informe qual abordagem marca maior precisão.
   Modificar o modelo de recompensa utiliza o valor médio de todos os estados ocultas e não apenas a última posição.

2. Após o treino, exiba todos os pares de preferências através do modelo de recompensa e computa: (a) a recompensa média para respostas preferidas, (b) a recompensa média para respostas rejeitadas, (c) a margem (preferida menos rejeitada). Um modelo bem calibrado deve ter uma margem clara.
   Tradução do inglês para tradução do inglês: implementing reward model校准── training, will all preferences to pass reward model calcula: a) 首选回复的平均奖励, b) 被拒回复的平均奖励, c) 边距 (边距) ─ 首选减被拒) ─ 良好校准的模型应有明显边距──然后添加 4 个新偏好对,检查边距是否保持在未见数据上──

3. Simulação de hacking de recompensa. Crie um modelo de recompensa que dê pontuações altas a respostas longas (recompensa = len(resposta) / 100). Execute PPO com este modelo de recompensa defeituoso e observe o modelo de política gerando resultados cada vez mais longos e repetitivos. Adicione uma penalidade KL de 0,1 e mostre que previne o comportamento degenerado.
   O modelo de recompensa é um modelo de recompensa que permite a criação de um modelo de recompensa para executar um PPO, observando o modelo de estratégia para gerar um aumento de tempo e retornar a produção.

4. Implementar uma recompensa multi-objetiva. Treinar dois modelos de recompensa - um para utilidade e outro para conciseza. Combinar-os como R = 0,7 * R_helpful + 0,3 * R_concise. Mostrar que o objetivo combinado produz respostas que são úteis e concisas, evitando a armadilha de verbosidade de uma única recompensa de utilidade.
   Tradução do inglês para tradução do inglês: implementing multi-goal reward;. training two reward models one for usefulness, one for simplicity;.

5. Compare diferentes coeficientes KL. Execute PPO com beta=0.001 (muito baixo, hacking de recompensa), beta=0.02 (padrão) e beta=0.5 (muito alto, sem aprendizado).
   Comparar diferentes KL 系数── Usar beta=0.001(Too Low, recompensa黑客)、beta=0.02(标准) e beta=0.5(Too High,不学习) executar PPO── desenhar cada grupo de curva de recompensa e KL 曲线──beta=0.02 应显示稳定的奖励提升和有界的 KL──

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| RLHF | "Training with human feedback" | Reinforcement Learning from Human Feedback: a three-stage pipeline (SFT, reward model, PPO) that optimizes language model outputs using human preference signals | 基于人类反馈的强化学习，三阶段管线 |
| Reward model | "A model that scores responses" | A transformer with a scalar output head, trained on pairwise human preferences using the Bradley-Terry loss | 奖励模型，用 Bradley-Terry 损失在偏好对上训练 |
| Bradley-Terry | "The comparison model" | A probabilistic model where P(A > B) = sigmoid(score(A) - score(B)), converting pairwise preferences into a consistent scoring function | Bradley-Terry 模型，将成对偏好转为一致评分 |
| PPO | "The RL algorithm" | Proximal Policy Optimization: updates the policy to maximize reward while clipping the update magnitude to prevent instability | 近端策略优化，裁剪更新幅度防止不稳定 |
| KL divergence | "How different two distributions are" | A measure of the difference between the policy model's token distribution and the reference model's -- used as a penalty to prevent reward hacking | KL 散度，衡量策略与参考分布的差异 |
| KL penalty | "The leash on the model" | Beta * KL(policy \|\| reference) subtracted from the reward signal -- prevents the policy from diverging too far from the SFT checkpoint | KL 惩罚，防止策略偏离 SFT 检查点 |
| Reward hacking | "Gaming the reward" | When the policy finds degenerate high-reward outputs by exploiting weaknesses in the reward model instead of genuinely improving | 奖励黑客，策略利用奖励模型弱点获得高奖励 |
| Preference pair | "Which is better, A or B?" | A training example consisting of (prompt, preferred_response, rejected_response) -- the fundamental unit of RLHF training data | 偏好对，RLHF 训练数据的基本单元 |
| Reference model | "The frozen SFT checkpoint" | A copy of the SFT model whose weights never change -- used as the anchor for KL divergence computation | 参考模型，冻结的 SFT 检查点 |

## Mais leitura 延伸阅读

- [Ouyang et al., 2022 -- "Training language models to follow instructions with human feedback" (InstructGPT)](https://arxiv.org/abs/2203.02155)-- o artigo que tornou o RLHF prático para grandes modelos de linguagem
- [Schulman et al., 2017 -- "Proximal Policy Optimization Algorithms"](https://arxiv.org/abs/1707.06347)-- o papel original da OpenAI
- [Bai et al., 2022 -- "Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback"](https://arxiv.org/abs/2204.05862)-- O artigo da Anthropic RLHF com análise detalhada do hacking de recompensa e da pena KL
- [Stiennon et al., 2020 -- "Learning to summarize with human feedback"](https://arxiv.org/abs/2009.01325)-- RLHF aplicado à resumo, mostrando que os modelos de recompensa podem capturar julgamentos de qualidade matizados
- [Christiano et al., 2017 -- "Deep reinforcement learning from human preferences"](https://arxiv.org/abs/1706.03741)-- o trabalho fundamental sobre funções de recompensa de aprendizagem a partir de comparações humanas
