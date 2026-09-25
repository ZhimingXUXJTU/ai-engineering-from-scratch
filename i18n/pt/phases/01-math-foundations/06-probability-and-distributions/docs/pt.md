# Probabilidade e Distribuição  概率

> A probabilidade é a linguagem que a IA usa para expressar incerteza.
> 概率 é uma linguagem de IA expressa incerteza.

**Type:** Learn | **类型:** 学习
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Implementar PMFs e PDFs a partir do zero para distribuições Bernoulli, categóricas, Poisson, uniformes e normais
- Compute o valor esperado, a variância e use o Teorema do Limite Central para explicar por que os Gaussianos dominam
- Construir softmax e log-softmax funções com o truque de estabilidade numérica (subtrair logit max)
- Calcular a perda de entropia cruzada dos logits e conectá-la à probabilidade de log negativo

> **【中文解读】**
> 概率 é uma IA que exprime linguagem incerta. 概率 distribuição, modelo de linguagem de 50.000 palavras candidatas em probabilidade de amostra, modelo de expansão de distribuição de aprendizagem para gerar imagens. 概率

> **【拓展：概率在 AI 中的位置】**
> - **Softmax**A transferência de dados de uma rede neuronal para distribuição de probabilidade é o último passo de todos os modelos de categorias.
> - **交叉熵损失**Função de perda padrão de uma tarefa, igual a negativo para número similar.
> - **高斯分布**A compreensão é extremamente limitada para explicar por que o GOS é tão comum na natureza e na IA.

## O problema é o problema da introdução

> **【中文解读】**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `[0.03, 0.91, 0.06]`(91% 概率是猫), modelo de linguagem selecionado entre 50.000 candidatos, modelo de expansão de uma distribuição de aprendizado, que gera imagens.

## O conceito central.

> **【拓展：概率分布是 AI 生成模型的基础】**O núcleo do modelo de produção (VAE, GAN, modelo de expansão) é a distribuição de probabilidade: aprender a uma distribuição de dados p (x), então gerar novos dados a partir do meio da amostra.

Cada previsão que um modelo faz é uma distribuição de probabilidade. Cada função de perda mede a distância que a distribuição prevista está da verdadeira. Cada etapa de treinamento ajusta os parâmetros para fazer uma distribuição parecer mais parecida com outra. Sem probabilidade, você não pode ler um único artigo ML, depurar um único modelo ou entender por que sua perda de treinamento é NaN.

> Cada previsão do modelo é uma distribuição de probabilidade. Cada função de perda mede a diferença entre a distribuição de previsão e a distribuição real.

## O conceito central.

### Eventos, Espaços de Amostra e Probabilidade

O espaço de amostra S é o conjunto de todos os resultados possíveis. Um evento é um subconjunto do espaço de amostra.

> 样本空间 S é o conjunto de todos os resultados possíveis. Eventos são subconjuntos do espaço de um exemplo.

```
Coin flip:
  S = {H, T}
  P(H) = 0.5,  P(T) = 0.5

Single die roll:
  S = {1, 2, 3, 4, 5, 6}
  P(even) = P({2, 4, 6}) = 3/6 = 0.5
```

Três axiomas definem toda a probabilidade:
1. P(A) >= 0 para qualquer evento A
2. P(S) = 1 (algo acontece sempre)
3. P(A ou B) = P(A) + P(B) quando A e B não podem ocorrer ambos

> 概率论由三条公理定义:
> 1. 对于任意事件 A,P(A) >= 0
> 2. P (S) = 1 (necessariamente haverá algum resultado)
> 3. Quando A 和 B não pode acontecer ao mesmo tempo, P  A ou B = P  A + P  B)

Tudo o resto (teorema de Bayes, expectativas, distribuições) segue-se dessas três regras.

> 其他一切 (Beiéis定理,期望,分布) são todos derivados destas três regras.

### Probabilidade condicional e independência

P ((A) B) é a probabilidade de A dada que B aconteceu.

> P (A) é a probabilidade de ocorrência de A em condições de B  já ocorrido.

```
P(A|B) = P(A and B) / P(B)

Example: deck of cards
  P(King | Face card) = P(King and Face card) / P(Face card)
                      = (4/52) / (12/52)
                      = 4/12 = 1/3
```

Dois eventos são independentes quando saber um não diz nada sobre o outro:

> Dois eventos independentes significa saber que um deles não lhe diz nada sobre o outro:

```
Independent:   P(A|B) = P(A)
Equivalent to: P(A and B) = P(A) * P(B)
```

As moedas são independentes, mas não os cartões sem substituição.

> Para a moeda, não há nada de independente.

### Funções de massa de probabilidade vs funções de densidade de probabilidade

As variáveis aleatórias discretas têm uma função de massa de probabilidade (PMF). Cada resultado tem uma probabilidade específica que você pode ler diretamente.

> 离散随机变量有概率质量函数 (PMF) ⋅ cada resultado tem uma probabilidade específica que pode ser lido diretamente ⋅

```
PMF: P(X = k)

Fair die:
  P(X = 1) = 1/6
  P(X = 2) = 1/6
  ...
  P(X = 6) = 1/6

  Sum of all probabilities = 1
```

As variáveis aleatórias contínuas têm uma função de densidade de probabilidade (PDF). A densidade em um único ponto não é uma probabilidade.

> 连续随机变量有概率密度函数 (PDF) ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                                                                                      

```
PDF: f(x)

P(a <= X <= b) = integral of f(x) from a to b

f(x) can be greater than 1 (density, not probability)
integral from -inf to +inf of f(x) dx = 1
```

Esta distinção é importante no ML. As saídas de classificação são PMFs (opções discretas).

> Esta diferença é muito importante em ML.

### Distribuições comuns

**Bernoulli:**Um ensaio, dois resultados.

> **伯努利分布：**Uma experiência, dois resultados.

```
P(X = 1) = p
P(X = 0) = 1 - p
Mean = p,  Variance = p(1-p)
```

**Categorical:**Os modelos de classificação multi-classe (output softmax).

> **分类分布：**Uma experiência, um resultado diferente.

```
P(X = i) = p_i,  where sum of p_i = 1
Example: P(cat) = 0.7,  P(dog) = 0.2,  P(bird) = 0.1
```

**Uniform:**Todos os resultados são igualmente prováveis.

> **均匀分布：**Todos os resultados e probabilidades de surgimento são utilizados para inicialização de forma aleatória.

```
Discrete: P(X = k) = 1/n for k in {1, ..., n}
Continuous: f(x) = 1/(b-a) for x in [a, b]
```

**Normal (Gaussian):**A curva de campanha, parametrizada por média (mu) e variância (sigma^2).

> **正态（高斯）分布：**钟形曲线──由均值 (mu) 和方差 (sigma^2) 参数化──

```
f(x) = (1 / sqrt(2*pi*sigma^2)) * exp(-(x - mu)^2 / (2*sigma^2))

Standard normal: mu = 0, sigma = 1
  68% of data within 1 sigma
  95% within 2 sigma
  99.7% within 3 sigma
```

**Poisson:**Contas de eventos raros em um intervalo fixo.

> **泊松分布：** Contado de eventos raros em zonas fixas 

```
P(X = k) = (lambda^k * e^(-lambda)) / k!
Mean = lambda,  Variance = lambda
```

### Valor esperado e variação

O valor esperado é o resultado médio ponderado.

> O valor esperado é o resultado médio do aumento.

```
Discrete:   E[X] = sum of x_i * P(X = x_i)
Continuous: E[X] = integral of x * f(x) dx
```

Medidas de variação espalhadas em torno da média.

> 方差 (diferência de dimensões)

```
Var(X) = E[(X - E[X])^2] = E[X^2] - (E[X])^2
Standard deviation = sqrt(Var(X))
```

Em ML, o valor esperado aparece como a função de perda (perda média sobre a distribuição de dados).

> Em ML, o valor esperado é representado como perda de função (ou perda média na distribuição de dados), o diferencial diz-lhe que o modelo está estável.

### Distribuições conjuntas e marginais

Uma distribuição conjunta P ((X, Y) descreve duas variáveis aleatórias juntas.

> 联合分布 P(X, Y)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

Exemplo de PMF comum (X = clima, Y = guarda-chuva):
联合 PMF示例(X = 天气,Y = 是否带):

| | Y=0 (no umbrella / 不带伞) | Y=1 (umbrella / 带伞) | Marginal P(X) / 边缘 P(X) |
|---|---|---|---|
| X=0 (sun / 晴天) | 0.40 | 0.10 | P(X=0) = 0.50 |
| X=1 (rain / 下雨) | 0.05 | 0.45 | P(X=1) = 0.50 |
| **Marginal P(Y) / 边缘 P(Y)** | P(Y=0) = 0.45 | P(Y=1) = 0.55 | 1.00 |

A distribuição marginal soma a outra variável:

> 边缘分布通过对另一个变量求和得到:

```
P(X = x) = sum over all y of P(X = x, Y = y)
```

Os números totais de filas e colunas da tabela acima são os marginais.

> A distribuição de correntes e de correntes é a distribuição de margens.

### Por que a distribuição normal aparece em todos os lugares

O Teorema do Limite Central: a soma (ou média) de muitas variáveis aleatórias independentes converge para uma distribuição normal, independentemente da distribuição original.

> Centro极限定理: muitos valores independentes de variação e (ou média) recebidos para distribuição normal, independentemente da distribuição original é o que.

```
Roll 1 die:  uniform distribution (flat)
Average of 2 dice:  triangular (peaked)
Average of 30 dice: nearly perfect bell curve

This works for ANY starting distribution.
```

É por isso que:
- Os erros de medição são aproximadamente normais (muitas pequenas fontes independentes)
  Tradução do inglês:                                                                                                                                                                                                                                                            
- Inicializações de peso em redes neurais usam distribuições normais
  Tradução do inglês para "Natural Language"
- O ruído gradiente no SGD é aproximadamente normal (suma de muitos gradientes de amostra)
  Tradução do inglês:SGD
- A distribuição normal é a distribuição máxima de entropia para uma determinada média e variância
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para inglês para tradução do inglês para inglês para inglês para inglês para inglês para inglês

### Probabilidades de registro

As probabilidades crudas causam problemas numéricos. Multiplicar muitas probabilidades pequenas juntas rapidamente desce para zero.

> A probabilidade inicial leva a um problema numérico.

```
P(sentence) = P(word1) * P(word2) * ... * P(word_n)
            = 0.01 * 0.003 * 0.02 * ...
            -> 0.0 (underflow after ~30 terms)
```

As probabilidades de registro corrigem isto.

> Para a probabilidade numérica resolveu este problema.

```
log P(sentence) = log P(word1) + log P(word2) + ... + log P(word_n)
                = -4.6 + -5.8 + -3.9 + ...
                -> finite number (no underflow)
```

Regras:
- log(a * b) = log(a) + log(b)
- As probabilidades de log são sempre <= 0 (desde 0 < P <= 1)
- Mais negativo = menos provável
- A perda de entropia cruzada é a probabilidade de registro negativo da classe correta

> 规则:
> - log(a * b) = log(a) + log(b)
> - Para a probabilidade de número, é sempre <= 0 ((0 < P <= 1)
> - 越负 = 越不可能
> - 交叉损失就是正确类别的负对数概率

### Softmax como distribuição de probabilidade

As redes neurais emitem pontuações brutas (logits).

> 神经网络输出原始分数(logits) ――Softmax irá transformá-los em uma distribuição de probabilidade eficaz―

```
softmax(z_i) = exp(z_i) / sum(exp(z_j) for all j)

Properties:
  - All outputs are in (0, 1)
  - All outputs sum to 1
  - Preserves relative ordering of inputs
  - exp() amplifies differences between logits
```

O truque softmax: subtrair o logit máximo antes de exponenciar para evitar o desbordamento.

> Softmax 技巧: em emprego antes de reduzir o máximo logit, evitar a sobreposição

```
z = [100, 101, 102]
exp(102) = overflow

z_shifted = z - max(z) = [-2, -1, 0]
exp(0) = 1  (safe)

Same result, no overflow.
```

Log-softmax combina softmax e log para estabilidade numérica. PyTorch usa isso internamente para perda de entropia cruzada.

> Log-softmax vai softmax e log 合并 para um passo para manter a estabilidade numérica.

### Amostragem

"Este tipo de análise é o resultado de uma análise de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados
- Deixe de lado as amostras aleatórias que os neurônios para zero
  Tradução do inglês:Dropout 随机采样决定哪些神经元置零
- Ampliação de dados amostras de transformações aleatórias
  Tradução do inglês: dados aumentados
- Modelos de linguagem amostram o próximo token da distribuição prevista
  中文翻译:语言模型从预测分布中采样下一个词
- Modelos de difusão de amostra de ruído e denotação progressiva
  Tradução do inglês para tradução do inglês:

A amostragem a partir de distribuições arbitrárias requer técnicas como amostragem de transformação inversa, amostragem de rejeição ou o truque de reparametrização (usado em VAEs).

> A partir de uma distribuição arbitrária entre as amostras, é necessário um cambio de amostras, rejeitar amostras ou técnicas de re-paramentação (VAE) e outras técnicas.

## Construí-lo e realizei-o.
```figure
gaussian-pdf
```

## Construí-lo

### Passo 1: Basics of Probability

```python
import math
import random

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def combinations(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def conditional_probability(p_a_and_b, p_b):
    return p_a_and_b / p_b

p_king_given_face = conditional_probability(4/52, 12/52)
print(f"P(King | Face card) = {p_king_given_face:.4f}")
```

### Passo 2: PMF e PDF a partir do zero

```python
def bernoulli_pmf(k, p):
    return p if k == 1 else (1 - p)

def categorical_pmf(k, probs):
    return probs[k]

def poisson_pmf(k, lam):
    return (lam ** k) * math.exp(-lam) / factorial(k)

def uniform_pdf(x, a, b):
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0

def normal_pdf(x, mu, sigma):
    coeff = 1.0 / (sigma * math.sqrt(2 * math.pi))
    exponent = -0.5 * ((x - mu) / sigma) ** 2
    return coeff * math.exp(exponent)
```

### Passo 3: Valor esperado e variação

```python
def expected_value(values, probabilities):
    return sum(v * p for v, p in zip(values, probabilities))

def variance(values, probabilities):
    mu = expected_value(values, probabilities)
    return sum(p * (v - mu) ** 2 for v, p in zip(values, probabilities))

die_values = [1, 2, 3, 4, 5, 6]
die_probs = [1/6] * 6
mu = expected_value(die_values, die_probs)
var = variance(die_values, die_probs)
print(f"Die: E[X] = {mu:.4f}, Var(X) = {var:.4f}, SD = {var**0.5:.4f}")
```

### Passo 4: Amostragem a partir de distribuições

```python
def sample_bernoulli(p, n=1):
    return [1 if random.random() < p else 0 for _ in range(n)]

def sample_categorical(probs, n=1):
    cumulative = []
    total = 0
    for p in probs:
        total += p
        cumulative.append(total)
    samples = []
    for _ in range(n):
        r = random.random()
        for i, c in enumerate(cumulative):
            if r <= c:
                samples.append(i)
                break
    return samples

def sample_normal_box_muller(mu, sigma, n=1):
    samples = []
    for _ in range(n):
        u1 = random.random()
        u2 = random.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        samples.append(mu + sigma * z)
    return samples
```

### Passo 5: Softmax e probabilidades de registro

```python
def softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    exps = [math.exp(z) for z in shifted]
    total = sum(exps)
    return [e / total for e in exps]

def log_softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = max_logit + math.log(sum(math.exp(z) for z in shifted))
    return [z - log_sum_exp for z in logits]

def cross_entropy_loss(logits, target_index):
    log_probs = log_softmax(logits)
    return -log_probs[target_index]
```

### Passo 6: Teorema de Limite Central demonstração

```python
def demonstrate_clt(dist_fn, n_samples, n_averages):
    averages = []
    for _ in range(n_averages):
        samples = [dist_fn() for _ in range(n_samples)]
        averages.append(sum(samples) / len(samples))
    return averages
```

### Passo 7: Visualização

```python
import matplotlib.pyplot as plt

xs = [mu + sigma * (i - 500) / 100 for i in range(1001)]
ys = [normal_pdf(x, mu, sigma) for x, mu, sigma in ...]
plt.plot(xs, ys)
```

Implementações completas com todas as visualizações estão em `code/probability.py`- Não .

> incluindo a realização completa de todas as observações`code/probability.py`- Não.

## Use-o com o framework implementado.

Com NumPy e SciPy, tudo acima é de uma linha:

> Use NumPy e SciPy, todas as funções acima só precisam de uma linha de código:

```python
import numpy as np
from scipy import stats

normal = stats.norm(loc=0, scale=1)
samples = normal.rvs(size=10000)
print(f"Mean: {np.mean(samples):.4f}, Std: {np.std(samples):.4f}")
print(f"P(X < 1.96) = {normal.cdf(1.96):.4f}")

logits = np.array([2.0, 1.0, 0.1])
from scipy.special import softmax, log_softmax
probs = softmax(logits)
log_probs = log_softmax(logits)
print(f"Softmax: {probs}")
print(f"Log-softmax: {log_probs}")
```

Construíste isto do zero, agora sabes o que fazem as chamadas da biblioteca.

> Você construiu tudo isso desde o zero. Agora sabe o que a função da biblioteca está fazendo.

## Exercícios.

1. Implementar a amostragem de transformação inversa para a distribuição exponencial. Verifique amostragem de valores de 10.000 e comparando o histograma com o PDF verdadeiro.

2. Construa uma tabela de distribuição conjunta para dois dados carregados.

3. Calcule a perda de entropia cruzada para um classificador de 5 classes que produz logits `[2.0, 0.5, -1.0, 3.0, 0.1]`Quando a classe correta é o índice 3. Então verifique sua resposta com PyTorch `nn.CrossEntropyLoss`- Não .

4. Escreva uma função que tome uma lista de probabilidades de registro e retorna a sequência mais provável, a probabilidade total de registro e a probabilidade bruta equivalente. Teste com uma frase de 50 palavras onde cada palavra tem probabilidade de 0,01.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sample space | "All the possibilities" / "所有可能性" | The set S of every possible outcome of an experiment / 实验所有可能结果的集合 S |
| PMF | "The probability function" / "概率函数" | A function that gives the exact probability of each discrete outcome, summing to 1 / 给出每个离散结果精确概率的函数，总和为 1 |
| PDF | "The probability curve" / "概率曲线" | A density function for continuous variables. Integrate it over an interval to get probability / 连续变量的密度函数，在区间上积分得到概率 |
| Conditional probability | "Probability given something" / "条件概率" | P(A\|B) = P(A and B) / P(B). The foundation of Bayesian thinking and Bayes' theorem / 贝叶斯思维和贝叶斯定理的基础 |
| Independence | "They don't affect each other" / "互不影响" | P(A and B) = P(A) * P(B). Knowing one event tells you nothing about the other / 知道一个事件不影响另一个 |
| Expected value | "The average" / "平均值" | The probability-weighted sum of all outcomes. The loss function is an expected value / 所有结果的概率加权求和，损失函数就是一种期望值 |
| Variance | "How spread out" / "离散程度" | The expected squared deviation from the mean. High variance = noisy, unstable estimates / 偏离均值的平方的期望，方差大 = 噪声大、不稳定 |
| Normal distribution | "The bell curve" / "钟形曲线" | f(x) = (1/sqrt(2*pi*sigma^2)) * exp(-(x-mu)^2/(2*sigma^2)). Appears everywhere due to the CLT / 因中心极限定理而无处不在 |
| Central Limit Theorem | "Averages become normal" / "平均趋于正态" | The mean of many independent samples converges to a normal distribution regardless of the source / 许多独立样本的均值收敛到正态分布 |
| Joint distribution | "Two variables together" / "两个变量一起" | P(X, Y) describes the probability of every combination of X and Y outcomes / 描述 X 和 Y 每种组合的概率 |
| Marginal distribution | "Sum out the other variable" / "消去另一个变量" | P(X) = sum_y P(X, Y). Recovers one variable's distribution from the joint / 从联合分布中恢复单个变量的分布 |
| Log probability | "Log of the probability" / "概率的对数" | log P(x). Turns products into sums, preventing numerical underflow in long sequences / 将乘法变加法，防止长序列数值下溢 |
| Softmax | "Turn scores into probabilities" / "分数转概率" | softmax(z_i) = exp(z_i) / sum(exp(z_j)). Maps real-valued logits to a valid probability distribution / 将实数值 logits 映射为有效概率分布 |
| Cross-entropy | "The loss function" / "损失函数" | -sum(p_true * log(p_predicted)). Measures how different two distributions are. Lower is better / 衡量两个分布的差异，越小越好 |
| Logits | "Raw model outputs" / "模型原始输出" | Unnormalized scores before softmax. Named after the logistic function / softmax 之前的未归一化分数 |
| Sampling | "Drawing random values" / "随机取值" | Generating values according to a probability distribution. How models generate output / 按概率分布生成值，模型用它生成输出 |

## Mais leitura 延伸阅读

- [3Blue1Brown: But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo)- prova visual de que as médias se tornam normais
- [Stanford CS229 Probability Review](https://cs229.stanford.edu/section/cs229-prob.pdf)- uma referência concisa que abrange tudo aqui e mais
- [The Log-Sum-Exp Trick](https://gregorygundersen.com/blog/2020/02/09/log-sum-exp/)- por que a estabilidade numérica é importante e como alcançá-la
