# Métodos de amostragem

> A amostragem é como a IA explora o espaço das possibilidades.
> 采样是 AI 探索可能性空间的方式──

**Type:** Build | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 06-07 (Probability, Bayes' Theorem) | **前置知识:** Phase 1, 第 06-07 课（概率、贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objetivos de aprendizagem

- Implementar a amostragem de CDF inversa, rejeição e importância a partir do zero usando apenas números aleatórios uniformes
  Utilizando o número de dados que podem ser utilizados para a análise de dados, a análise de dados e a análise de dados deve ser feita em conformidade com o artigo 10.o, n.o 1, do Regulamento (UE) n.o 1095/2011.
- Construir amostragem de temperatura, top-k e top-p (núcleo) para geração de tokens de modelos de linguagem
  构建用于语言模型代号 生成的温度、top-k 和 top-p(núcleo) 采样
- Explique o truque de reparametrização e por que permite a propagação de volta através da amostragem em VAEs
  解释重参数化技巧(Reparameterization Trick) e por que ele pode fazer que a operação de tomada de VAE suporte à contra-direção de propagação
- Execute o MCMC Metropolis-Hastings para amostrar de uma distribuição-alvo não normalizada
  运行 Metropolis-Hastings MCMC 从未归纳化的目标分布中采样


> **【中文解读】**
> 采样是 AI 探索可能性的方式──LLM Usar temperatura/top-k/top-p 控制文本生成多样性──VAE Usar técnicas de heavy parameterization让采样可微──

## O problema é o problema da introdução

Um modelo de linguagem termina de processar o seu pedido e produz um vetor de 50.000 logits, um para cada token no seu vocabulário.

> Depois de processar sua dica, gerará um volume de 50 mil logitas, para cada token da lista de palavras.

Se ele sempre escolhe o token de maior probabilidade, cada resposta é idêntica. Determinista. Aborrecido. Se ele escolhe uniformemente ao acaso, a saída é confusa. A resposta vive em algum lugar entre esses extremos, e que em algum lugar é controlada pela amostragem.

> Se cada vez escolher o token de probabilidade mais alta, cada vez responderão com a mesma certeza, sem discussão. Se cada vez escolherem o sinal de probabilidade mais alto, a saída será entre os dois extremos, enquanto o meio será controlado pela estratégia de amostragem.

A amostragem não se limita à geração de textos. O aprendizado de reforço estima os gradientes das políticas através de trajetórias de amostragem. Os VAEs aprendem representações latentes tomando amostras de distribuições aprendidas e propagando-se para trás através da aleatoriedade. Os modelos de difusão geram imagens através da amostragem de ruído e denociamento iterativo. Os métodos de Monte Carlo estimam integrals que não têm solução fechada. Os algoritmos MCMC exploram distribuições posteriores de alta dimensão que são impossíveis de enumerar.

> 采样不仅限于文本生成──强化学习通过采样轨迹(Trajectory) 來估计策略梯度──VAE 通过从学习到分布中采样并反向传播来学习隐表示──扩散模型通过采样噪声并代去噪声来生成图像──蒙特卡洛方法估算没有解析的积分──MCMC 算法探索无法枚举的高维后验分布──

Cada sistema de IA gerador é um sistema de amostragem. A estratégia de amostragem determina a qualidade, a diversidade e a controlagem da saída. Esta lição constrói todos os principais métodos de amostragem a partir do zero, começando por números aleatórios uniformes e terminando com as técnicas que alimentam os LLMs e modelos geradores modernos.

> Cada sistema de IA gerado é, em essência, um sistema de amostragem. A estratégia de amostragem determina a qualidade, a diversidade e a capacidade de controle da saída.

## O conceito central.

> **【中文解读】**
> 采样问题无处不在:语言模型需要从50,000 token中选一个,VAE需要从隐空间采样,扩散模型需要从噪声逐步到噪声. O desafio central é que você só pode diretamente de simples distribuição, deve ser feito através de mudanças para obter uma distribuição de objetivos complexos.

### Por que é importante tomar amostras

A amostragem aparece em quatro papéis fundamentais em IA e aprendizado de máquina:

> 采样 em AI e machine learning desempenha quatro papéis básicos:

**Generation.**Os modelos de linguagem, modelos de difusão e GANs produzem todas as saídas por amostragem. O algoritmo de amostragem controla diretamente a criatividade, a coerência e a diversidade.

> **生成。**语言模型、扩散模型和 GAN 都通过采样产生输出──采样算法直接控制创造力、连贯性和多样性──温度、top-k 和核采样是工程师每日调节的"旋──采样算法直接控制创造力、连贯性和多样性──temperatura、top-k 和核采样是工程师每天调节的"旋──采样算法是采样算法的"采样算法"──采样算法是采样算法的直接控制创造力、连贯性和多样性──采样算法是采样的"旋"──采样算法是采样的"采样算法"──采样算法是采样的"采样算法"──采样算法是采样的"采样的" ,采样算法是采样的" ,采样的"采样的" ,采样的"采样是采样的" ,采样的"采样是采样的" ,采样是采样的"的"采样式是采样式的" ,采样式是采样是采样的的的的" ,采样式是是是采样式的的的的的的的的的的的

**Training.**Estocástico padrão de descida de amostras mini-batches. Desistência de amostras de neurônios para desativar. Ampliação de dados amostras de transformações aleatórias. Importância de amostragem repesam amostras para reduzir a variância de gradiente na aprendizagem de reforço (PPO, TRPO).

> **训练。**随机梯度下降(SGD) 采样 mini-batch──Dropout 采样要禁用神经元──数据增强采样随机变换──重要性采样重新加权样样以后降强化学习──PPO、TRPO) 采样方差

**Estimation.**Muitas quantidades em ML não têm solução fechada. A perda esperada sobre uma distribuição de dados, a função de partição de um modelo baseado em energia, a evidência na inferência Bayesiana.

> **估计。**Muitas quantidades do ML não foram resolvidas. A perda de expectativas na distribuição de dados, a função de repartição do modelo de energia, a evidência da sugestão de Bayes, a avaliação de Monte Carlo, através de uma amostra, procura uma média para aproximar todas essas quantidades.

**Exploration.**Algoritmos MCMC exploram distribuições posteriores na inferência Bayesiana. estratégias evolutivas amostram perturbações de parâmetros.

> **探索。**MCMC 算法 в Белеес推断中探索后验分布──进化策略──Evolutionary Strategies) 采样参数扰动──Thompson 采样在多臂老虎机问题中平衡探索与利用──

O desafio principal: só pode tomar amostras diretamente de distribuições simples (uniforme, normal).

> 核心挑战: você só pode ser diretamente tomado de uma simples distribuição (均分布、正态分布) em uma outra distribuição.

> **【拓展：LLM 采样策略的工程实践】**
> GPT-4 等模型推理时,temperatura normalmente definida como 0.0-1.0,top-p 设为 0.9-1.0。OpenAI API 默认温度=1.0、top_p=1.0。研究表明 top-p (núcleo) 采样在大多数任务上优于 top-k,因为它能根据模型置信度自适应调整候选集大小──对于代码生成,temperatura=0.2 + top_p=0.95 是常见配置──

### Amostra aleatória uniforme

Cada método de amostragem começa aqui. Um gerador de números aleatórios uniforme produz valores em [0, 1) onde cada sub-intervalo de igual comprimento tem igual probabilidade.

> Todos os métodos de adoção começam a partir deste ponto.

```
U ~ Uniform(0, 1)

P(a <= U <= b) = b - a    for 0 <= a <= b <= 1

Properties:
  E[U] = 0.5
  Var(U) = 1/12
```

Para amostrar uniformemente a partir de um conjunto discreto de n itens, gerar U e retornar piso ((n * U). Para amostrar a partir de um intervalo contínuo [a, b], calcular a + (b - a) * U.

> Para que o conjunto de elementos seja dividido em uma massa, produzir U e retornar ao piso,

A principal ideia: um único número aleatório uniforme contém exatamente a quantidade certa de aleatoriedade para produzir uma amostra de qualquer distribuição.

> 关键洞察: número de azar único contém um azar suficiente para que possa ser produzido um padrão de qualquer distribuição.

> **【中文解读】**
> 均分布是所有采样基石── em computadores, um falso gerador de números de ordem (como Mersenne Twister) é o resultado de uma distribuição média [0,1) .

### Método de CDF inverso (análise de transformação inversa)

A função de distribuição cumulativa (CDF) mapeia os valores para probabilidades:

```
F(x) = P(X <= x)

Properties:
  F is non-decreasing
  F(-inf) = 0
  F(+inf) = 1
  F maps the real line to [0, 1]
```

O CDF inverso mapeia as probabilidades de volta aos valores. Se U ~ Uniform(0, 1), então X = F_inverse(U) segue a distribuição-alvo.

> 逆 CDF 将概率映射回值──若 U ~ Uniform(0, 1), então X = F_inverse(U) 服从目标分布──

```
Algorithm:
  1. Generate u ~ Uniform(0, 1)
  2. Return F_inverse(u)

Why it works:
  P(X <= x) = P(F_inverse(U) <= x) = P(U <= F(x)) = F(x)
```

**Exponential distribution example:**

```
PDF: f(x) = lambda * exp(-lambda * x),   x >= 0
CDF: F(x) = 1 - exp(-lambda * x)

Solve F(x) = u for x:
  u = 1 - exp(-lambda * x)
  exp(-lambda * x) = 1 - u
  x = -ln(1 - u) / lambda

Since (1 - U) and U have the same distribution:
  x = -ln(u) / lambda
```

Isto funciona perfeitamente quando você pode escrever F_inversos em forma fechada. Para a distribuição normal, não há CDF inverso fechado de forma, então usamos outros métodos (Box-Muller, ou aproximação numérica).

> Quando você pode escrever expressão de resolução de F_inverse, este método é perfeito para funcionar. Para a distribuição de estado normal, não há forma de resolução em CDF, então usamos outros métodos.

**Discrete version:**Para distribuições discretas, construa o CDF como uma soma cumulativa, gera U e encontre o primeiro índice onde a soma cumulativa excede U.`sample_categorical`Trabalha na lição 06.

> **离散版本：**Para a distribuição de separação, a CDF é construída para acumulação, gerando U, encontrando acumulação e superação de U por primeira vez.`sample_categorical`O que é que é o trabalho?

> **【中文解读】**
> 逆 CDF 方法的核心思想:CDF 函数 F(x) Colocar o valor de variação de random em relação à probabilidade de [0,1], enquanto sua função de random em relação a F_inverse está bem reversamente colocando o valor de random em relação ao valor de distribuição de objetivos.

### Rejeição de amostras

Quando não se pode inverter o CDF, mas pode avaliar o PDF-alvo até uma constante, a amostragem de rejeição funciona.

> Quando você não consegue pedir contra CDF, mas pode calcular o objetivo PDF (todo diferentemente de um constante)

```
Target distribution: p(x)  (can evaluate, possibly unnormalized)
Proposal distribution: q(x)  (can sample from)
Bound: M such that p(x) <= M * q(x) for all x

Algorithm:
  1. Sample x ~ q(x)
  2. Sample u ~ Uniform(0, 1)
  3. If u < p(x) / (M * q(x)), accept x
  4. Otherwise, reject and go to step 1

Acceptance rate = 1/M
```

Quanto mais apertada a M, maior a taxa de aceitação. Em dimensões baixas (1-3), a amostragem de rejeição funciona bem. Em dimensões altas, a taxa de aceitação cai exponencialmente porque a maior parte do volume da proposta é rejeitada. Esta é a maldição da dimensionalidade para a amostragem de rejeição.

> Em um espaço de baixa dimensão, a taxa de aceitação diminuiu, pois a maior parte dos projetos foram rejeitados.

**Example: sampling from a truncated normal.**Use uma proposta uniforme sobre a faixa truncada. O envelope M é o máximo do PDF normal nessa faixa.

> **示例：从截断正态分布采样。**Em um campo de intercepção, o uso de um total de propostas é distribuído.

**Example: sampling from a semicircle.**Propõe uniformemente no retângulo delimitante. Aceite se o ponto cai dentro do semicírculo. É assim que Monte Carlo calcula pi: a taxa de aceitação é igual à proporção de área pi/4.

> **示例：从半圆采样。**Em um quadrado de extrato, a proporção de proposições é aceita se o ponto estiver no meio-circuito.

> **【拓展：拒绝采样在粒子滤波中的应用】**
> 粒子波(Particle Filter) é um algoritmo central de rastreamento de objetivos e de localização de máquinas. Em essência, é um método de rejeição de amostragem usando um conjunto de "partículas" de distribuição de probabilidade, com base nos resultados de observação sobre a amostragem de partículas. Em empresas de autônomo como Waymo, em real-time localização, utilizou centenas de milhares de partículas em um "波器", atualizado dezenas de vezes por segundo.

### Importância da amostragem

Às vezes, você não precisa de amostras da distribuição-alvo p(x). Você precisa estimar uma expectativa sob p(x), e você tem amostras de uma distribuição diferente q(x).

> Às vezes, você não precisa de uma amostra de uma distribuição de p (x) meta, mas precisa de uma estimativa de uma expectativa de p (x) meta, enquanto você tem uma amostra de uma outra distribuição q (x) meta.

```
Goal: estimate E_p[f(x)] = integral of f(x) * p(x) dx

Rewrite:
  E_p[f(x)] = integral of f(x) * (p(x)/q(x)) * q(x) dx
            = E_q[f(x) * w(x)]

where w(x) = p(x) / q(x)  are the importance weights.

Estimator:
  E_p[f(x)] ~ (1/N) * sum(f(x_i) * w(x_i))    where x_i ~ q(x)
```

Isto é fundamental na aprendizagem de reforço. Em PPO (Proximal Policy Optimization), você coleta trajetórias sob uma política antiga pi_old mas quer otimizar uma nova política pi_new. O peso de importância é pi_new ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇a ̇

> Isto é essencial no fortalecimento da aprendizagem. Em PPO, você está no antigo estratégia, mas pensa em melhorar o novo estratégia.

> **【拓展：PPO 中的重要性采样】**
> O PPO é o algoritmo central do treinamento do ChatGPT RLHF. O PPO é um algoritmo de grande importância para melhorar a distribuição entre as novas estratégias. O PPO é um recurso de grande importância para reduzir o peso do peso do pesado.

A variação do estimador de importância da amostragem depende de quão similar q é a p. Se q é muito diferente de p, algumas amostras recebem pesos enormes e dominam a estimativa.

> A diferença de importância do estimador de amostras depende da similaridade entre q e p. Se q e p forem muito diferentes, uma pequena quantidade de amostras obterá um peso enorme e irá conduzir a estimativa.

```
E_p[f(x)] ~ sum(w_i * f(x_i)) / sum(w_i)
```

### Estimação de Monte Carlo

A estimativa de Monte Carlo aproxima os integrals, mediando amostras aleatórias.

> A estimativa de Monte Carlo, através da qual a média de amostras de cada tipo é aproximada, garante a receita.

```
Goal: estimate I = integral of g(x) dx over domain D

Method:
  1. Sample x_1, ..., x_N uniformly from D
  2. I ~ (Volume of D / N) * sum(g(x_i))

Error: O(1 / sqrt(N))   regardless of dimension
```

A taxa de erro é independente de dimensões, razão pela qual os métodos de Monte Carlo dominam em dimensões altas onde a integração baseada em rede é impossível.

> A taxa de erro não tem relação com a dimensão. É por isso que o método Monte Carlo ocupa o lugar dominante em espaço de grande dimensão.

> **【中文解读】**
> O essencial do método de Monte Carlo: usar a média de um sample de qualquer momento para obter uma expectativa aproximada. A grande quantidade de teorías garante a receita, e a taxa de erro O(1/sqrt(N)) não tem relação com a dimensão.

**Estimating pi:**

```
Sample (x, y) uniformly from [-1, 1] x [-1, 1]
Count how many fall inside the unit circle: x^2 + y^2 <= 1
pi ~ 4 * (count inside) / (total count)
```

**Estimating expectations:**

```
E[f(X)] ~ (1/N) * sum(f(x_i))    where x_i ~ p(x)

The sample mean converges to the true expectation.
Variance of the estimator = Var(f(X)) / N
```

### Cadeia Markov Monte Carlo (MCMC): Metrópole-Hastings

O MCMC constrói uma cadeia de Markov cuja distribuição estática é a distribuição-alvo p ((x). Após passos suficientes, as amostras da cadeia são (aproximadamente) amostras de p ((x).

> MCMC construir uma cadeia de Markov ), sua distribuição estática ), é a distribuição de p (x) ⋅ através de um número suficiente de passos, a cadeia ⋅ quase ⋅ é a distribuição de p (x) ⋅

```
Target: p(x)  (known up to a normalizing constant)
Proposal: q(x'|x)  (how to propose the next state given the current state)

Metropolis-Hastings algorithm:
  1. Start at some x_0
  2. For t = 1, 2, ..., T:
     a. Propose x' ~ q(x'|x_t)
     b. Compute acceptance ratio:
        alpha = [p(x') * q(x_t|x')] / [p(x_t) * q(x'|x_t)]
     c. Accept with probability min(1, alpha):
        - If u < alpha (u ~ Uniform(0,1)): x_{t+1} = x'
        - Otherwise: x_{t+1} = x_t
  3. Discard first B samples (burn-in)
  4. Return remaining samples
```

Para propostas simétricas (q(x' (x) = q(x (x) = x)), a relação se simplifica para p(x')/p(x. Este é o algoritmo Metropolis original.

> 对于对称提议 (q) = q) ),比率简化为 p (x) /p (x) .

**Why it works.**A regra de aceitação garante o equilíbrio detalhado: a probabilidade de estar em x e se mover para x' é igual à probabilidade de estar em x' e se mover para x. O equilíbrio detalhado implica que p ((x) é a distribuição estacionária da cadeia.

> **为什么有效。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

> **【拓展：MCMC 在贝叶斯深度学习中的应用】**
> O núcleo do quadro de pesquisa Bayesian é o MCMC. O NUTS (No-U-Turn Sampler) é a variante mais avançada do MCMC, que regula automaticamente o seu tempo e direção.

**Practical considerations:**
- Combustão: descartar amostras iniciais antes que a cadeia atinja o equilíbrio
  预热期(Burn-in): desisto de cadeia para alcançar o equilíbrio
- Desminução: manter cada k-sample para reduzir a autocorrelação
  稀释(Tinning): cada um de cada um de nós mantém um para reduzir
- Escala de propostas: muito pequena e a cadeia se move lentamente (alta aceitação, exploração lenta); muito grande e a maioria das propostas é rejeitada (baita aceitação, em vigor)
  提议尺度(Proposal Scale): 太小则链移动缓慢(aceitação alta mas explorar lenta); 太大则大多数提议被拒绝(aceitação baixa,原地不动)
- A taxa de aceitação ideal para uma proposta gaussiana em dimensões elevadas é de aproximadamente 0,234
  O melhor índice de aceitação do High Levels of High Levels é de 0,234

### Amostração de Gibbs

A amostragem de Gibbs é um caso especial do MCMC para distribuições multivariadas. Em vez de propor um movimento em todas as dimensões de uma só vez, atualiza uma variável por vez de sua distribuição condicional.

> O modelo de Gibbs é um exemplo especial do MCMC na distribuição de múltiplas variações. Não se move simultaneamente em todas as dimensões, mas, cada vez, a partir da distribuição de condições, se renova uma variação.

```
Target: p(x_1, x_2, ..., x_d)

Algorithm:
  For each iteration t:
    Sample x_1^{t+1} ~ p(x_1 | x_2^t, x_3^t, ..., x_d^t)
    Sample x_2^{t+1} ~ p(x_2 | x_1^{t+1}, x_3^t, ..., x_d^t)
    ...
    Sample x_d^{t+1} ~ p(x_d | x_1^{t+1}, x_2^{t+1}, ..., x_{d-1}^{t+1})
```

A amostragem de Gibbs requer que você possa amostrar de cada distribuição condicional p ((x_i ∈ x_{-i}).
- Redes Bayesianas: os condicionalis seguem a partir da estrutura do gráfico
  贝叶斯网络: condições distribuídas por diagramas estruturais
- Misturas gaussianas: os condicionantes são gaussianas
  Modelo de alta mistura: condição distribuída é alta
- Modelos de ising: a condição de cada giro depende apenas de seus vizinhos
  Ising 模型: cada condição de rotação é distribuída dependendo apenas de seus vizinhos

A taxa de aceitação é sempre de 1 (todas as propostas são aceitas), porque a amostragem a partir da condição exata satisfaz automaticamente o equilíbrio detalhado.

>  taxa de aceitação é sempre 1 cada proposta é aceita), pois a partir de condições de distribuição precisas, a aceitação automática de condições de equilíbrio.

**Limitation.**Quando as variáveis são altamente correlacionadas, a amostragem de Gibbs mistura-se lentamente porque atualizar uma variável de cada vez não pode fazer grandes movimentos diagonais através da distribuição.

> **局限性。**Quando as variações estão altamente relacionadas, o modelo de Gibbs é muito lento, pois apenas uma variação é atualizada e não pode fazer grandes movimentos de canto na distribuição.

> **【中文解读】**
> O modelo de Gibbs é um exemplo especial do MCMC: cada vez que apenas uma variação é atualizada, a partir da distribuição condicional, a cada probabilidade é de uma distribuição condicional precisa, de modo que a taxa de aceitação é sempre 100%.

### Amostragem de temperatura (utilizada em LLM)

Modelos de linguagem emitem logits z_1, ..., z_V para cada token no vocabulário. Softmax converte estes em probabilidades.

> 语言模型为词汇表 输出 logits z_1, ..., z_V──Softmax 将将它们转换为概率──Temperatura(温度) 在软max 之前对 logits 进行缩放:

```
p_i = exp(z_i / T) / sum(exp(z_j / T))

T = 1.0: standard softmax (original distribution)
T -> 0:  argmax (deterministic, always picks highest logit)
T -> inf: uniform (all tokens equally likely)
T < 1.0: sharpens the distribution (more confident, less diverse)
T > 1.0: flattens the distribution (less confident, more diverse)
```

**Why it works.**Dividir logits por T < 1 amplifica as diferenças entre logits. Se z_1 = 2 e z_2 = 1, dividindo por T = 0,5 dá z_1/T = 4 e z_2/T = 2, tornando o fosso maior. Depois de softmax, o token de logit mais alto recebe uma participação muito maior.

> **为什么有效。**Se z_1 = 2、z_2 = 1, se z_1/T = 0.5  get z_1/T = 4、z_2/T = 2, a diferença é maior.

**In practice:**
- T = 0,0: decodificação gananciosa, melhor para perguntas e respostas factuais
  贪心解码, mais adequado ao facto
- T = 0,3-0,7: ligeiramente criativo, bom para a geração de código
  略有创意, Adapto代码生成
- T = 0,7-1,0: equilibrado, bom para conversa geral
  均衡,适合一般对话
- T = 1,0-1,5: escrita criativa, brainstorming
  创意写作、头脑风暴
- T > 1,5: cada vez mais aleatório, raramente útil
  - Não é muito útil.

A temperatura não muda quais tokens são possíveis, mas a massa de probabilidade atribuída a cada token.

> A temperatura não muda quais tokens podem ser selecionados.

> **【中文解读】**
> Temperatura é LLM 输出多样性的"旋"──T < 1 让分布更尖(更像贪心),T > 1 让分布更平坦(更随机)──T → 0 退化为 argmax,T → ∞ 退化为均分布──实际中 T=0.7 é o ponto de equilíbrio mais comum──注意: temperatura não muda quaisquer tokens há que ser selecionados, apenas mudar a distribuição da probabilidade──

### Amostração de Top-k

A amostragem top-k restringe o conjunto candidato aos tokens k com as maiores probabilidades, em seguida, renormaliza e amostragem desse conjunto restringido.

> Top-k 采样将候选集限制为概率最高的 k 个代币,然后重新归纳并从该受限集合中采样.

```
Algorithm:
  1. Compute softmax probabilities for all V tokens
  2. Sort tokens by probability (descending)
  3. Keep only the top k tokens
  4. Renormalize: p_i' = p_i / sum(p_j for j in top-k)
  5. Sample from the renormalized distribution

k = 1:  greedy decoding
k = V:  no filtering (standard sampling)
k = 40: typical setting, removes long tail of unlikely tokens
```

Top-k impede que o modelo selecione tokens extremamente improváveis (typos, nonsense) que existem na cauda longa da distribuição do vocabulário. O problema: k é fixo independentemente do contexto. Quando o modelo é confiante (um token tem 95% de probabilidade), k = 40 ainda permite 39 alternativas. Quando o modelo é incerto (a probabilidade é espalhada por 1000 tokens), k = 40 corta opções plausíveis.

> Top-k 防止模型选择词汇分布长尾中极不可能的代币(错别字、无意义的词) ⋅ o problema é:k é fixo, não se segue a seguinte mudança.

### Amostragem de topo (núcleo)

A amostragem top-p ajusta dinamicamente o tamanho do conjunto candidato.Em vez de manter um número fixo de tokens, ele mantém o menor conjunto de tokens cuja probabilidade cumulativa excede p.

> Top-p 采样动态调整候选集大小── não retém um número fixo de tokens, mas retém uma probabilidade acumulada superior a p do mínimo de tokens 集合──

```
Algorithm:
  1. Compute softmax probabilities for all V tokens
  2. Sort tokens by probability (descending)
  3. Find smallest k such that sum of top-k probabilities >= p
  4. Keep only those k tokens
  5. Renormalize and sample

p = 0.9:  keeps tokens covering 90% of probability mass
p = 1.0:  no filtering
p = 0.1:  very restrictive, nearly greedy
```

Quando o modelo é confiante, a amostragem de núcleo mantém poucos tokens (talvez 2-3). Quando o modelo é incerto, mantém muitos (talvez 200).

> Quando o modelo tem confiança, o núcleo 采样只保留少量 token (可能 2-3 个) ⋅ Quando o modelo não está certo, ele conserva muito (可能 200 个) ⋅ Este comportamento de auto-adaptação é o núcleo 采样通常比 top-k 产生更好的文本的原因──

**Common combinations:**
- Temperatura 0,7 + p superior 0,9: boa configuração de uso geral
  Bom ajuste geral
- Temperatura 0,0 (avidas): ideal para tarefas deterministas
  O máximo adequado à determinação das tarefas
- Temperatura 1.0 + top-k 50: Fan et al. (2018) configuração original de papel
  Fan 等人 (2018) 原论文设置

Top-k e top-p podem ser combinados. Aplique top-k primeiro, e depois top-p no conjunto restante.

> Top-k 和 top-p pode ser combinado usando-¬ Primeiro aplicar top-k, novamente em restante conjunto aplicar top-p¬¬¬

### Tricolor de reparametrização (usado em VAEs)

Os autoencodadores variáveis (VAEs) aprendem codificando entradas em uma distribuição em espaço latente, tomando amostras dessa distribuição e decodificando a amostra de volta.

> 变分自编码器(VAE) através da entrada de código para a distribuição no espaço oculto 、 de essa distribuição 、 então o desenho do código vai voltar para aprender ;; o problema é: você não pode fazer a transmissão de um desenho através da operação de distribuição reversa ;;

```
Standard sampling (not differentiable):
  z ~ N(mu, sigma^2)

  The randomness blocks gradient flow.
  d/d_mu [sample from N(mu, sigma^2)] = ???
```

O truque de reparametrização separa a aleatoriedade dos parâmetros:

> Técnicas de pesquisa de parâmetros serão aleatórias e parâmetros serão separados:

```
Reparameterized sampling:
  epsilon ~ N(0, 1)          (fixed random noise, no parameters)
  z = mu + sigma * epsilon   (deterministic function of parameters)

  Now z is a deterministic, differentiable function of mu and sigma.
  d(z)/d(mu) = 1
  d(z)/d(sigma) = epsilon

  Gradients flow through mu and sigma.
```

Isso funciona porque N(mu, sigma^2) tem a mesma distribuição que mu + sigma * N(0, 1).

> É por isso que é válido, é porque N ∈ Mu, sigma^2) com mu + sigma * N ∈ 0, 1) ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N ∈ N   ∈ N ∈ N                                                                                                                                                                                                       

**In the VAE training loop:**
1. As saídas do codificador mu e log ((sigma^2) para cada entrada
2. Amostra de epsilon ~ N(0, 1)
3. Computação z = mu + sigma * epsilon
4. Decodificar z para reconstruir a entrada
5. Propagação para trás através das etapas 4, 3, 2, 1 (possivel porque a etapa 3 é diferenciável)

Sem o truque de reparametrização, as VAEs não podem ser treinadas com a propagação de volta padrão.

> Sem técnicas de pesquisa, a VAE não pode usar o treinamento padrão de contra-direção.

> **【拓展：重参数化技巧的广泛应用】**
> O método de agregação de peso não é limitado ao modelo de expansão de VAE. Em cada etapa do modelo de difusão estável, DALL-E, o uso de peso é feito com agregação de peso: z = mu + sigma * epsilon.

### Gumbel-Softmax (Análise categórica diferenciável)

O truque de reparameterização funciona para distribuições contínuas (Gaussian). Para distribuições categóricas discretas, precisamos de uma abordagem diferente. Gumbel-Softmax fornece uma aproximação diferenciável à amostragem categórica.

> Técnicas de peso-parametrização são aplicáveis à distribuição contínua. Para distribuição de classes separadas, precisamos de diferentes métodos.

**The Gumbel-Max trick (non-differentiable):**

```
To sample from a categorical distribution with log-probabilities log(p_1), ..., log(p_k):
  1. Sample g_i ~ Gumbel(0, 1) for each category
     (g = -log(-log(u)), where u ~ Uniform(0, 1))
  2. Return argmax(log(p_i) + g_i)

This produces exact categorical samples.
```

**Gumbel-Softmax (differentiable approximation):**

```
Replace the hard argmax with a soft softmax:
  y_i = exp((log(p_i) + g_i) / tau) / sum(exp((log(p_j) + g_j) / tau))

tau (temperature) controls the approximation:
  tau -> 0:  approaches a one-hot vector (hard categorical)
  tau -> inf: approaches uniform (1/k, 1/k, ..., 1/k)
  tau = 1.0: soft approximation
```

Gumbel-Softmax produz um relaxamento contínuo de uma amostra discreta. A saída é um vetor de probabilidade (modo um-quente) em vez de um-quente duro. Os gradientes fluem através do softmax. Durante o passagem para frente no treinamento, você pode usar o estimador "direto-a-caminho": use o argmax duro para o passagem para frente, mas os gradientes macios de Gumbel-Softmax para o passagem para trás.

> Gumbel-Softmax 产生离散样本的连续松(Continuous Relaxation) ・・・输出是一个概率向量(软一个热) 而不是硬一个热――梯度可以流过软max──在训练的前向传播中,你可以使用"直通估计器"(Straight-Through Estimator):前向传播使用硬 argmax,反向传播使用软 Gumbel-Softmax 梯度──

**Applications:**
- Variaveis latentes discretos em VAEs
  Variação de separação entre os EAA
- Pesquisa de arquitetura neural (escolha de operações discretas)
  神经架构搜索 (em inglês)
- Mecanismos de atenção dura
  硬注意力机械
- Aprendizagem reforçada com ações discretas
  离散动作强化学习 (dispersão)

### Amostragem estratificada

A amostragem padrão de Monte Carlo pode deixar vagas no espaço de amostragem por acaso.

> 标准蒙特卡洛采样可能会偶然留下空隙在样本空间中──分层采样──Stratified Sampling) 通过将空间分为层 (Strata) 并从每层中采样来强制均覆盖──

```
Standard Monte Carlo:
  Sample N points uniformly from [0, 1]
  Some regions may have clusters, others gaps

Stratified sampling:
  Divide [0, 1] into N equal strata: [0, 1/N), [1/N, 2/N), ..., [(N-1)/N, 1)
  Sample one point uniformly within each stratum
  x_i = (i + u_i) / N   where u_i ~ Uniform(0, 1),  i = 0, ..., N-1
```

A amostragem estratificada tem sempre uma variância menor ou igual em comparação com a Monte Carlo padrão:

> A diferença de camadas é sempre inferior ou igual ao padrão de Monte Carlo:

```
Var(stratified) <= Var(standard Monte Carlo)

The improvement is largest when f(x) varies smoothly.
For piecewise-constant functions, stratified sampling is exact.
```

**Applications:**
- Integração numérica (quasi-Monte Carlo)
  Número de pontos de vista (prefeitura)
- Divisões de dados de formação (a garantia do equilíbrio de classes em cada dobra)
  訓練数据划分( assegurar cada troca de classe equilibrada)
- Amostragem de importância com estratificação (combinação de ambas as técnicas)
  结合分层的重要性采样
- NeRF (Neural Radiance Fields) usa amostragem estratificada ao longo dos raios da câmera
  NeRF( campo de radiação neurológica) ao longo da fase máquina de luz usando

### Conexão a modelos de difusão

Os modelos de difusão geram imagens através de um processo de amostragem. O processo avançado adiciona ruído gaussiano a uma imagem em passos T até que se torne ruído puro. O processo inverso aprende a denotar, recuperando a imagem original passo a passo.

> O modelo de expansão através do processo de captação gera imagem. O processo de expansão aumenta gradualmente a imagem, até que se torna puro ruído.

```
Forward process (known):
  x_t = sqrt(alpha_t) * x_{t-1} + sqrt(1 - alpha_t) * epsilon
  where epsilon ~ N(0, I)

  After T steps: x_T ~ N(0, I)  (pure noise)

Reverse process (learned):
  x_{t-1} = (1/sqrt(alpha_t)) * (x_t - (1 - alpha_t)/sqrt(1 - alpha_bar_t) * epsilon_theta(x_t, t)) + sigma_t * z
  where z ~ N(0, I)

  Each denoising step is a sampling step.
```

A ligação com os métodos desta lição:
- Cada etapa de denotação utiliza o truque de reparametrização (ruído de amostra, aplicar transformação determinista)
  Cada passo de desvio de ruído é usado técnicas de re-paramentação (táctica de tomada de ruído, aplicação de determinação)
- O cronograma de ruído {alpha_t} controla uma forma de anelação de temperatura
  噪声调度 {alpha_t} 控制一种形式的温度退火(Temperatura Anealing)
- O treinamento utiliza a estimativa de Monte Carlo para aproximar o ELBO (evidência limite inferior)
                                                                                                                                                                                                                                                                
- A amostragem ancestral em modelos de difusão é uma cadeia de Markov (cada etapa depende apenas do estado atual)
  扩散模型中的祖先采样 (Ancestral Sampling) é uma cadeia de caráter (cada passo depende apenas do estado atual)

Todo o processo de geração de imagens é amostragem iterativa: comece com o ruído e, em cada passo, amostre uma versão ligeiramente menos ruidosa condicionada ao modelo de denotação aprendido.

> Todo o processo de produção de imagens é de tomada de molde: a partir do ruído, em cada passo, baseado na aprendizagem de um modelo de tomada de ruído, uma versão um pouco diferente.

## Construí-lo e realizei-o.
```figure
monte-carlo-pi
```

## Construí-lo

### Passo 1: Amostragem uniforme e inversa de CDF

```python
import math
import random

def sample_uniform(a, b):
    return a + (b - a) * random.random()  # 线性变换：把 [0,1) 映射到 [a,b)

def sample_exponential_inverse_cdf(lam):
    u = random.random()                   # 生成均匀随机数
    return -math.log(u) / lam             # 逆 CDF：x = -ln(u) / lambda
```

Gerenciar 10.000 amostras exponenciais e verificar a média é 1/lambda.

> Produção de 10.000 个指数分布样本,验证平均值为 1/lambda──

### Passo 2: Amostragem de rejeição

```python
def rejection_sample(target_pdf, proposal_sample, proposal_pdf, M):
    while True:                           # 持续采样直到被接受
        x = proposal_sample()             # 从提议分布采样
        u = random.random()               # 均匀随机数用于决定接受/拒绝
        if u < target_pdf(x) / (M * proposal_pdf(x)):  # 接受条件
            return x
```

Utilize a amostragem de rejeição para extrair de uma distribuição normal truncada. Verifique a forma através da histogramagem das amostras.

> Utilizando a rejeição de amostra de uma distribuição de corto-circuito em estado normal.

### Passo 3: Amostragem de importância

```python
def importance_sampling_estimate(f, target_pdf, proposal_pdf, proposal_sample, n):
    total = 0
    for _ in range(n):
        x = proposal_sample()
        w = target_pdf(x) / proposal_pdf(x)
        total += f(x) * w
    return total / n
```

Estimar E[X^2] sob uma distribuição normal usando uma proposta uniforme.

> Utilize均提议分布估计正态分布下 E[X^2]──与已知答案 (mu^2 + sigma^2) 比较──

### Passo 4: Estimação de Monte Carlo de pi

```python
def monte_carlo_pi(n):
    inside = 0
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x*x + y*y <= 1:
            inside += 1
    return 4 * inside / n
```

### Passo 5: MCMC Metropolis-Hastings

```python
def metropolis_hastings(target_log_pdf, proposal_sample, proposal_log_pdf, x0, n_samples, burn_in):
    samples = []
    x = x0                                # 初始状态
    for i in range(n_samples + burn_in):
        x_new = proposal_sample(x)        # 从提议分布生成新候选
        log_alpha = (target_log_pdf(x_new) + proposal_log_pdf(x, x_new)  # 计算接受比的对数
                     - target_log_pdf(x) - proposal_log_pdf(x_new, x))
        if math.log(random.random()) < log_alpha:  # 以 min(1, alpha) 的概率接受
            x = x_new
        if i >= burn_in:                  # 丢弃 burn-in 阶段的样本
            samples.append(x)
    return samples
```

Amostra de uma distribuição bimodal (mistura de dois Gaussianos). Visualize a trajetória da cadeia.

> A partir de duas pistas de distribuição (de duas altitudes)

### Passo 6: Amostragem de Gibbs

```python
def gibbs_sampling_2d(conditional_x_given_y, conditional_y_given_x, x0, y0, n_samples, burn_in):
    x, y = x0, y0
    samples = []
    for i in range(n_samples + burn_in):
        x = conditional_x_given_y(y)
        y = conditional_y_given_x(x)
        if i >= burn_in:
            samples.append((x, y))
    return samples
```

### Passo 7: Amostragem de temperatura

```python
def softmax(logits):
    max_l = max(logits)
    exps = [math.exp(z - max_l) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def temperature_sample(logits, temperature):
    scaled = [z / temperature for z in logits]  # 温度缩放：除以 T
    probs = softmax(scaled)                      # 计算缩放后的概率分布
    return sample_from_probs(probs)
```

Mostre como a temperatura altera a distribuição de saída para um conjunto de logits de token.

>  demonstrar como a temperatura altera um conjunto de logits de tokens de saída de distribuição。

### Passo 8: Amostragem de ponta e ponta

```python
def top_k_sample(logits, k):
    indexed = sorted(enumerate(logits), key=lambda x: -x[1])
    top = indexed[:k]
    top_logits = [l for _, l in top]
    probs = softmax(top_logits)
    idx = sample_from_probs(probs)
    return top[idx][0]

def top_p_sample(logits, p):
    probs = softmax(logits)
    indexed = sorted(enumerate(probs), key=lambda x: -x[1])
    cumsum = 0
    selected = []
    for token_idx, prob in indexed:
        cumsum += prob
        selected.append((token_idx, prob))
        if cumsum >= p:
            break
    sel_probs = [pr for _, pr in selected]
    total = sum(sel_probs)
    sel_probs = [pr / total for pr in sel_probs]
    idx = sample_from_probs(sel_probs)
    return selected[idx][0]
```

### Passo 9: Truque de reparametrização

```python
def reparam_sample(mu, sigma):
    epsilon = random.gauss(0, 1)          # 标准正态噪声，不含可学习参数
    return mu + sigma * epsilon            # 确定性变换，梯度可流过

def reparam_gradient(mu, sigma, epsilon):
    dz_dmu = 1.0                          # z 对 mu 的梯度恒为 1
    dz_dsigma = epsilon                   # z 对 sigma 的梯度是 epsilon
    return dz_dmu, dz_dsigma
```

Demonstrar que os gradientes fluem através da amostra reparametrizada, mas não através da amostragem direta.

> A escala de demonstração pode fluir através de amostras de peso, mas não pode fluir através de amostras diretas.

### Passo 10: Gumbel-Softmax

```python
def gumbel_sample():
    u = random.random()
    return -math.log(-math.log(u))

def gumbel_softmax(logits, temperature):
    gumbels = [math.log(p) + gumbel_sample() for p in logits]
    return softmax([g / temperature for g in gumbels])
```

Mostre como a diminuição da temperatura faz com que a saída se aproxime de um vetor de um só-quente.

> Demonstrar a redução da temperatura como fazer a saída se aproximar de uma temperatura quente.

Implementações completas com todas as visualizações estão em `code/sampling.py`- Não .

> A realização completa de todas as visualizações`code/sampling.py`- Não.

## Use-o com o framework implementado.

> **【拓展：扩散模型中的采样工程】**
> Estabilidade de difusão Desde a publicação em 2022, o método de amostragem evoluiu de 1000 passos de DDPM para DDIM、DPM-Solver++ etc. apenas precisa de um método de 20-50 passos.

Com NumPy e SciPy, as versões de produção:

> Utilize NumPy 和 SciPy de produção:

```python
import numpy as np

rng = np.random.default_rng(42)

exponential_samples = rng.exponential(scale=2.0, size=10000)
print(f"Exponential mean: {exponential_samples.mean():.4f} (expected 2.0)")

from scipy import stats
normal = stats.norm(loc=0, scale=1)
print(f"CDF at 1.96: {normal.cdf(1.96):.4f}")
print(f"Inverse CDF at 0.975: {normal.ppf(0.975):.4f}")

logits = np.array([2.0, 1.0, 0.5, 0.1, -1.0])
temperature = 0.7
scaled = logits / temperature
probs = np.exp(scaled - scaled.max()) / np.exp(scaled - scaled.max()).sum()
token = rng.choice(len(logits), p=probs)
print(f"Sampled token index: {token}")
```

Para a MCMC em escala, utilize bibliotecas dedicadas:
- PyMC: modelagem Bayesiana completa com NUTS (HMC adaptativo)
  完整的贝叶斯建模, usando NUTS(自适应 HMC)
- Emcee: amostragem MCMC de conjunto
  集成 MCMC 采样器
- NumPyro/JAX: MCMC acelerado por GPU
  GPU acelerado MCMC

Construíste isto do zero, agora sabes o que fazem as chamadas da biblioteca.

> Você construiu estes métodos a partir de zero. Agora você sabe o que a função da biblioteca está fazendo.

## Exercícios.

1. Implemente a amostragem CDF inversa para a distribuição Cauchy. O CDF é F(x) = 0,5 + arctan(x) / pi. Gerencie 10.000 amostras e trace o histograma contra o PDF verdadeiro. Observe as caudas pesadas (valores extremos longe do centro).
   实现柯西分布(Cauchy Distribution) 采样──CDF 为 F(x) = 0,5 + arctan(x) /pi──生成 10,000 个样本并绘制直方图与真实 PDF 对比──注意重尾(远离中心极端值)。

2. Use a amostragem de rejeição para gerar amostras de uma distribuição Beta(2, 5) usando uma proposta Uniform(0, 1).
   Utilize rejeitar a amostra de Beta(2, 5) 分布中生成样本,提议分布使用Uniform(0, 1)─绘制接受样本与真实Beta PDF的对比图──理论接受率是多少?

3. Estima a integral de sin ((x) de 0 a pi usando Monte Carlo com 1.000, 10.000 e 100.000 amostras. Compare o erro em cada nível. Verifique se a escala de erro é O(1/sqrt(N)).
   Utilize Monte Carlo method estimation sin(x) em 0 até pi 积分, separadamente usando 1.000、10,000 和 100.000 个样本──比较各级的误差──验证误差按O(1/sqrt(N)) 缩放──

4. Implementar Metropolis-Hastings para amostragem de uma distribuição 2D p ((x, y) proporcional a exp ((-(x^2 * y^2 + x^2 + y^2 - 8*x - 8*y) / 2).
   实现 Metropolis-Hastings De 2D 分布 p(x, y) ~ exp(-(x^2*y^2 + x^2 + y^2 - 8x - 8y) /2) 中采样──绘制样本和链的轨迹──尝试不同的提议标准差──

5. Construir uma demonstração completa de geração de texto: dado um vocabulário de 10 palavras com logits, gerar sequências de 20 tokens usando (a) ganancioso, (b) temperatura = 0,7, (c) top-k = 3, (d) top-p = 0,9. Compare a diversidade de saídas em 5 corridas.
   构建一个完整的文本生成演示:给定 10 个词的词汇表和logits,使用 (a) 贪心、(b) temperatura=0,7、((c) top-k=3、((d) top-p=0,9 生成 20 个代币的序列──比较 5 次运行的输出多样性──

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sampling | "Drawing random values" | Generating values according to a probability distribution. The mechanism behind all generative AI |
| Uniform distribution | "All equally likely" | Every value in [a, b] has equal probability density 1/(b-a). The starting point for all sampling methods |
| Inverse CDF | "Probability transform" | F_inverse(U) converts a uniform sample into a sample from any distribution with known CDF. Exact and efficient |
| Rejection sampling | "Propose and accept/reject" | Generate from a simple proposal, accept with probability proportional to target/proposal ratio. Exact but wastes samples |
| Importance sampling | "Reweight samples" | Estimate expectations under p(x) using samples from q(x) by weighting each sample by p(x)/q(x). Core to PPO in RL |
| Monte Carlo | "Average random samples" | Approximate integrals as sample averages. Error O(1/sqrt(N)) regardless of dimension |
| MCMC | "Random walk that converges" | Construct a Markov chain whose stationary distribution is the target. Metropolis-Hastings is the foundational algorithm |
| Metropolis-Hastings | "Accept uphill, sometimes downhill" | Propose moves, accept based on density ratio. Detailed balance ensures convergence to target distribution |
| Gibbs sampling | "One variable at a time" | Update each variable from its conditional distribution holding others fixed. 100% acceptance rate |
| Temperature | "Confidence knob" | Divides logits by T before softmax. T<1 sharpens (more confident), T>1 flattens (more diverse) |
| Top-k sampling | "Keep the k best" | Zero out all but the k highest-probability tokens, renormalize, sample. Fixed candidate set size |
| Nucleus sampling (top-p) | "Keep the probable ones" | Keep the smallest set of tokens whose cumulative probability exceeds p. Adaptive candidate set size |
| Reparameterization trick | "Move randomness outside" | Write z = mu + sigma * epsilon where epsilon ~ N(0,1). Makes sampling differentiable. Essential for VAE training |
| Gumbel-Softmax | "Soft categorical sampling" | Differentiable approximation to categorical sampling using Gumbel noise + softmax with temperature |
| Stratified sampling | "Forced coverage" | Divide sample space into strata, sample from each. Always lower variance than naive Monte Carlo |
| Burn-in | "Warm-up period" | Initial MCMC samples discarded before the chain reaches its stationary distribution |
| Detailed balance | "Reversibility condition" | p(x) * T(x->y) = p(y) * T(y->x). Sufficient condition for p to be the stationary distribution of a Markov chain |
| Diffusion sampling | "Iterative denoising" | Generate data by starting from noise and applying learned denoising steps. Each step is a conditional sampling operation |

## Mais leitura 延伸阅读

- [Holbrook (2023): The Metropolis-Hastings Algorithm](https://arxiv.org/abs/2304.07010)- um tutorial detalhado sobre as bases do MCMC
- [Jang, Gu, Poole (2017): Categorical Reparameterization with Gumbel-Softmax](https://arxiv.org/abs/1611.01144)- papel original Gumbel-Softmax
- [Holtzman et al. (2020): The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)- papel de amostragem de núcleo (top-p)
- [Kingma & Welling (2014): Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)- Papel de AAE que introduz o truque de reparametrização
- [Ho, Jain, Abbeel (2020): Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)- O DDPM conecta a amostragem à geração de imagem
