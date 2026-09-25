# Estabilidade numérica.

> O ponto flutuante é uma abstração que vai morder-te durante o treino e não vais ver que vai acontecer.
> O número de pontos é um abstracto de fuga de água. Vai mordê-lo durante o treino, mas não o verá chegar.

**Type:** Build | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objetivos de aprendizagem

- Implementar softmax numéricamente estável e log-sum-exp usando o truque de subtração máxima
  Utilize técnicas de redução de valor máximo para alcançar o valor estável de suave max e log-sum-exp
- Identificar o desabastecimento, o desabastecimento e a cancelamento catastrófico nos cálculos de pontos flutuantes
  Identificação de fluxo de dados e de dados
- Verificar gradientes analíticos contra gradientes numéricos usando diferenças finitas centradas
  Uscenterlimitado diferença de teste
- Explique por que o bfloat16 é preferido ao float16 para treinamento e como a escalação de perdas impede o fluxo inferior de gradiente
  Explicação de por que o bfloat16 é mais adequado ao treino do que o float16 e como prevenir a perda de carga

> **【中文解读】**
> 浮点数是漏水的抽象──训练 3 小时后损失 变 NaN é o mais comum de colapsos──本章实现数值稳定的软max(减最大值技巧), explica por que bfloat16 é mais adequado que float16 更适合训练──混合精度训练中使用损失规模化 防止小梯度下溢──

## O problema é o problema da introdução

> **【中文解读】**Três tipos típicos de catástrofe de estabilidade numérica: 1) treinamento 3 horas após a perda 变 NaN某步计算溢出; 2) 精度比论文差 2% float16 累积舍入差食掉准确率; 3) 自写交叉 大逻辑 时返回 inf软max 溢出──这些都是浮点数的"漏水抽象",每个种都有标准修复技巧──

A seguir, adicione uma declaração de impressão, as logites estão bem no passo 9.000.`inf`Por passo 9.002 cada gradiente é`nan`E o treino está morto.
> Você adicionou uma impressão. Os logos em 9.000 passos voltaram a ser normais.`inf`Até a 9.002o passo, todas as etapas são`nan`O treinamento já morreu.

Ou: o seu modelo está pronto para ser concluído, mas a precisão é 2% pior do que o papel afirma. Você verifica tudo. Arquitetura coincide. Hiperparametros coincide. Dados coincidem. O problema é que o papel usou float32 e você usou float16 sem a escala correta. Trinta e dois bits de erro de arredondamento acumulado silenciosamente comido sua precisão.
> Ou: o treinamento do modelo foi concluído, mas a precisão do trabalho foi de 2%. Você verificou tudo.

Ou: você implementa a perda de entropia cruzada a partir do zero.`inf`O softmax desabou porque`exp(100)`Mas, como é que é possível, o sistema de controle de dados é maior do que o float32 pode representar.
> Ou: você desde o início realização de um transmissão  perda  pequenos logits 时正常  quando logits 超过 100 时返回 `inf`- O softmax está a cair.`exp(100)`超越了 float32 的表示范围──

A estabilidade numérica não é uma preocupação teórica. É a diferença entre uma corrida de treinamento que tem sucesso e uma que falha silenciosamente.
> A estabilidade numérica não é um problema teórico. É a diferença entre o sucesso de treinamento e o fracasso silencioso.

## O conceito central.

> **【拓展：Softmax 的数值稳定技巧是面试必考题】**Original Softmax:`softmax(x) = exp(x) / sum(exp(x))`, quando x tem um grande valor quando exp 溢出──解法: diminuição do valor máximo `softmax(x) = exp(x - max(x)) / sum(exp(x - max(x)))`Os resultados matemáticos não mudam mas o valor é estável.`F.cross_entropy`内部使用 log-softmax而非分开计算,就是这个原因──

### IEEE 754: Como os computadores armazenam números reais

Os computadores armazenam números reais como valores de pontos flutuantes seguindo o padrão IEEE 754.
> 计算机根据 IEEE 754 标准将实数存储为浮点值──浮点数有三部分:符号位、指数和尾数──

```
Float32 layout (32 bits total):
[1 sign] [8 exponent] [23 mantissa]

Value = (-1)^sign * 2^(exponent - 127) * 1.mantissa
```

A mantissa determina a precisão (quantos dígitos significativos). O exponente determina o intervalo (quão grande ou pequeno um número pode ser).
> 尾数决定精度 ((多少有效数字), índice decide范围 ((数字可以多大或多小) ⋅

```
Format     Bits   Exponent  Mantissa  Decimal digits  Range (approx)
float64    64     11        52        ~15-16          +/- 1.8e308
float32    32     8         23        ~7-8            +/- 3.4e38
float16    16     5         10        ~3-4            +/- 65,504
bfloat16   16     8         7         ~2-3            +/- 3.4e38
```

float32 dá-lhe cerca de 7 dígitos decimais de precisão. float16 dá-lhe cerca de 3 dígitos. bfloat16 é a resposta do Google ao problema de intervalo do float16 -- o mesmo exponente de 8 bits que float32 mas apenas 7 bits mantissa. Para treinamento de redes neurais, intervalo importa mais do que precisão, então bfloat16 geralmente ganha.
> float32  dá-lhe cerca de 7 pbits 进制精度──float16 约 3 pbits──bfloat16 é a resposta do Google para a questão float16 范围                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

### Por que 0,1 + 0,2 ! = 0,3 .

O número 0,1 não pode ser representado exatamente em ponto flutuante binário. Na base 2, é uma fração repetitiva. Float32 truncado isso para 23 bits de mantissa.
> 0.1 Em segundo plano não pode ser especificado. É um número circular.

```
In Python:
>>> 0.1 + 0.2
0.30000000000000004

>>> 0.1 + 0.2 == 0.3
False
```

Isto é importante para a ML porque: (1) Comparar perdas como `if loss < threshold`Os testes de verificação e reprodução falham se comparar os floats com os valores de`==`A solução: nunca comparar os flutuantes com`==`- Usar .`abs(a - b) < epsilon`ou `math.isclose()`- Não .
> Isto é muito importante para o ML: 1) 损失比较可能出错──(2) 累积许多小值会偏离真实和──(3) 用`==`Comparar o número de pontos de teste e teste vai falhar.`==`Comparado com os números de pontos.

### Cancellação catastrófica.

Quando subtraímos dois números de pontos flutuantes quase iguais, os dígitos significativos se anula e ficamos com ruído redondeado promovido para dígitos principais.
> Quando você diminui o número de pontos de câmbio de duas formas próximas, o número válido é obstruído, o barulho é elevado para o número de direção.

```
a = 1.0000001    (stored as 1.00000011920929 in float32)
b = 1.0000000    (stored as 1.00000000000000 in float32)

True difference:  0.0000001
Computed:         0.00000011920929

Relative error: 19.2%
```

A solução: reorganizar as fórmulas para evitar subtrair números grandes, quase iguais. Para variância, use o algoritmo Welford ou centra os dados primeiro.
> 修复: Re-排列公式以避免相减大近似相等等的数量──计算方差时使用韦尔福德算法或先中心化数据──

### O fluxo e o fluxo de baixo.

O fluxo excessivo acontece quando um resultado é muito grande para representar.
> O resultado é muito grande, não pode ser expresso, o resultado é muito pequeno.

```
Float32 boundaries:
  Maximum:  3.4028235e+38
  Overflow:  anything > 3.4e38 becomes inf
  Underflow: anything < 1.4e-45 becomes 0.0

exp(88.7)  = 3.40e+38   (barely fits in float32)
exp(89.0)  = inf         (overflow)
```

Em ML, `exp()`aparece em softmax, sigmoid e cálculos de probabilidade. `log()`Aparece na entropia cruzada, probabilidades de log e divergência KL.
> Em meio ao ML,`exp()`Aparece no cálculo de softmax, sigmoide e probabilidade.`log()`Aparece em um círculo de divisão.

### O truque de log-sum-exp

Computação`log(sum(exp(x_i)))`O truque: subtrair o valor máximo antes de exponenciar.
> 直接计算 `log(sum(exp(x_i)))`Número de valores em risco: antes da quantificação, reduzir o valor máximo.

```
log(sum(exp(x_i))) = max(x) + log(sum(exp(x_i - max(x))))
```

Por que isto funciona: depois de subtrair `max(x)`, o maior exponente é `exp(0) = 1`Não é possível sobrecarregar. Pelo menos um termo da soma é 1, portanto a soma é pelo menos 1, e`log(1) = 0`Não há fluxo de água para o`-inf`É possível.
> Porquê ?`max(x)`后, o máximo é `exp(0) = 1`Não é possível. Pelo menos um é 1, por isso, e pelo menos um é 1.`log(1) = 0`Não é possível.`-inf`- Não.

Este truque aparece em todos os lugares no ML: normalização de softmax, perda de entropia cruzada, soma de log-probabilidade, mistura de Gaussianos, inferência variável.
> Esta técnica está presente em ML:softmax 归化、交叉损失、对数概率求和、高斯混合、变分推断──

### Por que Softmax precisa do truque de subtração máxima ?

Sem o truque, logits de [100, 101, 102] causam sobreflow.
> 没有技巧时,logits [100, 101, 102] 导致溢出──有技巧时,减去max(x) = 102:

```
exp(100 - 102) = exp(-2) = 0.135
exp(101 - 102) = exp(-1) = 0.368
exp(102 - 102) = exp(0)  = 1.000
sum = 1.503

softmax = [0.090, 0.245, 0.665]
```

As probabilidades são idênticas, o cálculo é seguro, não é uma otimização, é um requisito para a corretão.
> 概率 é totalmente igual. 計算安全. 計算安全. 計算安全. 概率 é totalmente igual.

### NaN e Inf: Detecção e Prevenção

`nan`E ...`inf`Propaga-se viralmente através de computação.`nan`em uma actualização de gradiente faz o peso `nan`, que produz todas as produções subsequentes `nan`O treino está morto num passo.
> `nan`和 `inf`通过计算病毒式传播――梯度更新中的一个 `nan`O poder de mudança`nan`, fazer todos os resultados`nan`Treinar um passo está morto.

Como ?`nan`aparece: `0.0 / 0.0`- Não .`inf - inf`- Não .`inf * 0`- Não .`sqrt()`de negativo, `log()`Prevenção: entradas de sujeira para`exp()`, adicionar epsilon aos denominadores, usar implementações estáveis, cortar gradientes.
> `nan`如何出现:`0.0/0.0`- Não.`inf-inf`- Não.`inf*0`Negativo`sqrt()`Negativo`log()`Prevenção: limitação`exp()`输入、给分母加 epsilon、使用稳定实现、梯度剪──

### Verificação de gradiente numérico Verificação de gradiente numérico

Os gradientes analíticos (de backpropagation) podem ter bugs.
> 解析梯度 (desde contra-direção de propagação) pode haver bugs.

```
df/dx ~= (f(x + h) - f(x - h)) / (2h)
```

Regras de ouro: relative_error < 1e-7: perfeito; < 1e-5: aceitável; > 1e-3: algo está errado; > 1: completamente errado.
> 经验法则:相对误差 < 1e-7:完美; < 1e-5:可接受;> 1e-3:有问题;> 1:完全错误──

### Treinamento de Precissão Mista. Treinamento de Precissão Mista.

As GPUs modernas têm Tensor Cores que compute multiplicidades de matriz float16 2-8 vezes mais rápido do que float32.
> 现代 GPU tem Tensor Core, float16 矩阵乘法比 float32 快 2-8 倍──混合精度训练利用这一点──

```
1. Maintain float32 master copy of weights
2. Forward pass in float16 (fast)
3. Compute loss in float32 (prevents overflow)
4. Backward pass in float16 (fast)
5. Scale gradients to float32
6. Update float32 master weights
```

A correcção para o fluxo inferior do float16 é a escalação de perdas: multiplicar a perda por um fator de grande escala, passar para trás calcula gradientes maiores, dividir pela escala antes de atualizar os pesos.
> Float16 下溢的修复是损失缩缩:将损失乘以大缩因子,反向传播计算更大的梯度,更新权重前除以缩因子,

### bfloat16 vs float16: por que bfloat16 ganha para treino

O float16 tem mais precisão (10 bits de mantissa) mas alcance limitado (max. ~65,504). o float16 tem menos precisão mas alcance igual ao float32 (max. ~3.4e38).
> float16 精度更高(10 位尾数) 但范围有限(最大 ~65,504) ・bfloat16 精度较低但范围与 float32 相同(最大 ~3.4e38) ・训练时范围更重要──

### Gradiente Cutting .

Os gradientes explosivos ocorrem quando os gradientes crescem exponencialmente. Dois tipos de clipping: clip por valor (clampe cada elemento) e clip por norma (escala todo vetor para que sua norma não exceda um limiar).`torch.nn.utils.clip_grad_norm_()`- Não, não.
> 梯度爆炸发生在梯度指数增长时――两种剪裁:按值剪裁 限制每个元素) 和按范数剪裁 缩放整个向量使范数不超过值)──按范数剪裁保留梯度方向──

Valores típicos: `max_norm=1.0`para transformadores, `max_norm=0.5`para RL, `max_norm=5.0`para redes mais simples.
> 典型值:Transformer 用 `max_norm=1.0`- Não.`max_norm=0.5`, simples rede de uso`max_norm=5.0`- Não.

### Bugs Numericos comuns em ML

**Bug: Loss is NaN after a few epochs.**Causa: logits muito grandes, softmax sobrefluido.
> **Bug: 几个 epoch 后 loss 变 NaN。**原因:logits 太大,softmax 溢出──修复:使用稳定softmax,降低学习率,添加梯度剪──

**Bug: Validation accuracy is lower by 1-3%.**Causa: precisão mista sem escala de perda adequada.
> **Bug: 验证精度低 1-3%。**原因:混合精度没有正确的损失缩放──修复:启动动态损失缩放,或转换到 bfloat16──

**Bug: `exp()` returns `inf` in loss computation.**Correcção: uso `torch.nn.functional.log_softmax()`que implementa log-sum-exp internamente.
> **Bug: 损失计算中 `exp()` 返回 `inf`。**修复: usar `torch.nn.functional.log_softmax()`- Não.

## Construí-lo e realizei-o.

### Passo 1: Demonstre limites de precisão de ponto flutuante.
**Bug: Validation accuracy is lower than expected by 1-3%.**
Causa: precisão mista sem escalagem adequada de perdas.
Correcção: habilitar a escalação dinâmica de perdas ou mudar para bfloat16.

**Bug: Gradient norms are 0.0 for some layers.**
Causa: neurônios ReLU mortos (todas as entradas negativas), ou float16 subfluxo.
Corrigir: usar LeakyReLU ou GELU, usar escala de gradiente, verificar a inicialização do peso.

**Bug: Model works on one GPU but gives different results on another.**
Causa: ordem não determinista de acumulação de pontos flutuantes. As reduções paralelas da GPU somam em diferentes ordens em diferentes hardware, e a adição de pontos flutuantes não é associativa.
Fix: aceitar pequenas diferenças (1e-6), ou definir `torch.use_deterministic_algorithms(True)`E aceitar a penalidade de velocidade.

**Bug: `exp()` returns `inf` in loss computation.**
Causa: logits crus passados para `exp()`sem o truque de subtração máxima.
Correcção: uso `torch.nn.functional.log_softmax()`que implementa log-sum-exp internamente.

**Bug: Training diverges after switching from float32 to float16.**
Causa: float16 não pode representar magnitudes de gradiente abaixo de 6e-8 ou ativas acima de 65,504.
Correcção: utilizar precisão mista com escala de perda (AMP), ou usar bfloat16 em vez disso.

```figure
logsumexp-stability
```

## Construí-lo

### Passo 1: Demonstrar limites de precisão de ponto flutuante

```python
print("=== Floating Point Precision ===")
print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}")
print(f"Difference: {(0.1 + 0.2) - 0.3:.2e}")
```

### Passo 2: Implementar naívo vs. Softmax estável.

```python
import math

def softmax_naive(logits):
    exps = [math.exp(z) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def softmax_stable(logits):
    max_logit = max(logits)
    exps = [math.exp(z - max_logit) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

safe_logits = [2.0, 1.0, 0.1]
print(f"Naive:  {softmax_naive(safe_logits)}")
print(f"Stable: {softmax_stable(safe_logits)}")

dangerous_logits = [100.0, 101.0, 102.0]
print(f"Stable: {softmax_stable(dangerous_logits)}")
# softmax_naive(dangerous_logits) would return [nan, nan, nan]
```

### Passo 3: Implementar log-sum-exp estável .

```python
def logsumexp_stable(values):
    c = max(values)
    return c + math.log(sum(math.exp(v - c) for v in values))
```

### Passo 4: Implementar a entropia cruzada estável.

```python
def cross_entropy_stable(true_class, logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = math.log(sum(math.exp(s) for s in shifted))
    log_prob = shifted[true_class] - log_sum_exp
    return -log_prob
```

### Passo 5: Verificação gradual.

```python
def numerical_gradient(f, x, h=1e-5):
    grad = []
    for i in range(len(x)):
        x_plus = x[:]
        x_minus = x[:]
        x_plus[i] += h
        x_minus[i] -= h
        grad.append((f(x_plus) - f(x_minus)) / (2 * h))
    return grad

def check_gradient(analytical, numerical, tolerance=1e-5):
    for i, (a, n) in enumerate(zip(analytical, numerical)):
        denom = max(abs(a), abs(n), 1e-8)
        rel_error = abs(a - n) / denom
        status = "OK" if rel_error < tolerance else "FAIL"
        print(f"  param {i}: analytical={a:.8f} numerical={n:.8f} "
              f"rel_error={rel_error:.2e} [{status}]")
```

## Use-o com o framework implementado.

Veja .`code/numerical.py`para implementações completas com todas as demonstrações de casos de risco.
> 完整实现见 `code/numerical.py`- Não.

```python
# 梯度裁剪
def clip_by_norm(gradients, max_norm):
    total_norm = math.sqrt(sum(g**2 for g in gradients))
    if total_norm > max_norm:
        scale = max_norm / total_norm
        return [g * scale for g in gradients]
    return gradients

# NaN/Inf 检测
def check_tensor(name, values):
    has_nan = any(math.isnan(v) for v in values)
    has_inf = any(math.isinf(v) for v in values)
    if has_nan or has_inf:
        print(f"WARNING {name}: nan={has_nan} inf={has_inf}")
        return False
    return True
```

## Envia-o . Produto .

Esta lição produz:
> 本课程产出:

- `code/numerical.py`com softmax estável, log-sum-exp, entropia cruzada, verificação de gradientes e simulação de precisão mista
  包含稳定软max、log-sum-exp、交叉、梯度检查和混合精度模拟
- `outputs/prompt-numerical-debugger.md`para o diagnóstico de NaN/Inf e questões numéricas na formação
  Usado para o diagnóstico em treinamento NaN/Inf 和数值问题

## Exercícios.

1. **Catastrophic cancellation.**Calcule a variância de [1000000.0, 1000001.0, 1000002.0] usando a fórmula ingênua `E[x^2] - E[x]^2`Em float32. Então, compute-o usando o algoritmo online de Welford. Compare os erros com a variância verdadeira (0.6667).
   **灾难性抵消。**Utilize simples fórmula e Welford 算法计算 [1000000.0, 1000001.0, 1000002.0] 的方差,比较误差──

2. **Precision hunt.**Encontre o menor valor positivo float32 `x`Tal como isso .`1.0 + x == 1.0`Verifique se coincide .`numpy.finfo(numpy.float32).eps`- Não .
   **精度搜索。**找到使 `1.0 + x == 1.0`O mínimo de float32 ⋅ valor.

3. **Log-sum-exp edge cases.**Teste o teu .`logsumexp_stable`Função com: a) todos os valores iguais, b) um valor muito maior que os outros, c) todos os valores muito negativos (-1000).
   **Log-sum-exp 边界情况。**测试稳定 log-sum-exp 在极端输入下表现──

4. **Gradient checking a neural network layer.**Implementar uma única camada linear `y = Wx + b`e verificar a correcção para uma matriz de peso 3x2.
   **梯度检查神经网络层。**实现单层线性层并验证正确性──

5. **Loss scaling experiment.**Simulação de treinamento com float16: medir qual fração de gradientes se torna zero. Aplicar a escalação de perda e medir novamente.
   **损失缩放实验。**模拟 float16 训练, medir gradiente em proporção a zero, então aplicar perda reduzida em re-medidação。

## Termos-chave .

| Term / 术语 | What people say | What it actually means / 实际含义 |
|------|----------------|----------------------|
| IEEE 754 | "The float standard" | International standard defining binary floating point formats. / 定义二进制浮点格式的国际标准。 |
| Machine epsilon / 机器精度 | "The precision limit" | The smallest value e such that 1.0 + e != 1.0. For float32, ~1.19e-7. / 使 1.0 + e != 1.0 的最小值。float32 约 1.19e-7。 |
| Catastrophic cancellation / 灾难性抵消 | "Precision loss from subtraction" | Significant digits cancel when subtracting nearly equal numbers. / 相减近似相等数时有效数字抵消。 |
| Overflow / 溢出 | "Number too big" | A result exceeds the maximum representable value and becomes inf. / 结果超过最大可表示值变为 inf。 |
| Underflow / 下溢 | "Number too small" | A result is closer to zero than the smallest representable positive number. / 结果比最小可表示正数更接近零。 |
| Log-sum-exp trick / Log-sum-exp 技巧 | "Subtract the max first" | Computing log(sum(exp(x))) by factoring out exp(max(x)). / 通过提取 exp(max(x)) 计算 log(sum(exp(x)))。 |
| Stable softmax / 稳定 softmax | "Softmax that does not explode" | Subtracting max(logits) before exponentiating. / 指数化前减去最大 logit。 |
| Gradient checking / 梯度检查 | "Verify your backprop" | Comparing analytical vs numerical gradients to catch bugs. / 比较解析和数值梯度以捕获 bug。 |
| Mixed precision / 混合精度 | "Float16 forward, float32 backward" | Using lower-precision for speed, higher-precision for accuracy. / 低精度加速，高精度保准确。 |
| Loss scaling / 损失缩放 | "Prevent gradient underflow" | Multiplying loss by a large constant to keep gradients in float16 range. / 将损失乘以大常数使梯度保持在 float16 范围内。 |
| bfloat16 | "Brain floating point" | Google's 16-bit format with 8 exponent bits. Preferred for training. / Google 的 16 位格式，8 位指数。训练首选。 |
| Gradient clipping / 梯度裁剪 | "Cap the gradient norm" | Scaling the gradient vector so its norm does not exceed a threshold. / 缩放梯度向量使范数不超过阈值。 |
| NaN | "Not a Number" | Special float value from undefined operations. Propagates through all arithmetic. / 未定义操作的特殊浮点值。通过所有算术传播。 |
| Inf | "Infinity" | Special float value from overflow or division by zero. / 溢出或除零产生的特殊浮点值。 |
| Numerical gradient / 数值梯度 | "Brute force derivative" | Approximating a derivative by evaluating f(x+h) and f(x-h). / 通过求 f(x+h) 和 f(x-h) 近似导数。 |

## Mais leitura 延伸阅读

- [What Every Computer Scientist Should Know About Floating-Point Arithmetic (Goldberg 1991)](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)-- a referência definitiva
  浮点算术
- [Mixed Precision Training (Micikevicius et al., 2018)](https://arxiv.org/abs/1710.03740)- O artigo da NVIDIA sobre a escalação de perdas
  NVIDIA  损失缩放论文
- [AMP: Automatic Mixed Precision (PyTorch docs)](https://pytorch.org/docs/stable/amp.html)-- guia prático
  PyTorch 混合精度实践指南
- [bfloat16 format (Google Cloud TPU docs)](https://cloud.google.com/tpu/docs/bfloat16)- porque é que o Google escolheu este formato
  Google 选择 bfloat16 的原因
- [Kahan Summation (Wikipedia)](https://en.wikipedia.org/wiki/Kahan_summation_algorithm)-- algoritmo para reduzir o erro de arredondamento
   reduzir os erros de Kahan  procura e algoritmo
