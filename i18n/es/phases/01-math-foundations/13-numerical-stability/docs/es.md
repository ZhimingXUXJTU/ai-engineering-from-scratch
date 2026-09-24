# Estabilidad numérica.

> El punto flotante es una abstracción que se filtra, te morderá durante el entrenamiento y no lo verás venir.
> El número de puntos es un extracto de la fuga de agua. Te picará una boca en el entrenamiento, pero no lo verás llegar.

**Type:** Build | **类型:** 动手
**Language:**¿ Qué pasa ?**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~120 minutes | **时间:** ~120 分钟

## Objetivos de aprendizaje

- Implemente softmax y log-sum-exp estable numéricamente utilizando el truco de subtracción máxima
  Utiliza técnicas de reducción de valor máximo para lograr un valor estable de la cantidad de softmax y log-sum-exp
- Identificar el sobreflujo, el bajo flujo y la cancelación catastrófica en los cálculos de puntos flotantes
  Identificación de los puntos de cálculo de la sobrepeso y descenso
- Verificar los gradientes analíticos contra los gradientes numéricos utilizando diferencias finitas centradas
  Uscenter limitado diferencia de prueba de resolución
- Explicar por qué se prefiere bfloat16 sobre float16 para el entrenamiento y cómo la escalación de pérdidas evita el descenso de la corriente
  Explicar por qué el bfloat16 es más adecuado para el entrenamiento y cómo prevenir la disminución de la tasa de desnivel

> **【中文解读】**
> 浮点数是漏水的抽象──训练 3 小时后损失 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 Na n 变 NaN 变 Na n 变 NaN 变 Na n 变 Na n 变 NaN 变 Na n 变 Na n 变 Na n 变 Na n                                                                                                                                                                                                   

## El problema es la introducción del problema

> **【中文解读】**Tres tipos típicos de desastres de estabilidad numérica: 1) entrenamiento 3 horas después de la pérdida 变变 NaN某步计算溢出; 2) 精度比论文差 2% float16的累积舍入差差吃掉准确率; 3) autoescrito交叉大逻辑时返回 infsoftmax 溢出──

Añade una declaración de impresión. Los logits están bien en el paso 9.000.`inf`En el paso 9.002 cada gradiente es`nan`y el entrenamiento está muerto.
> Tu agregaste una impresión... los logitos en los 9.000 pasos volvieron a la normalidad... los 9.001 pasos se convirtieron en`inf`Hasta la 9.002 todas las etapas son`nan`, el entrenamiento ya está muerto.

O: tu modelo se prepara para la finalización pero la precisión es un 2% peor que las afirmaciones del papel. Lo comprobas todo. La arquitectura coincide. Los hiperparámetros coinciden. Los datos coinciden. El problema es que el papel usó float32 y usaste float16 sin la escala correcta. Treinta y dos bits de error de redondeo acumulado se comieron silenciosamente tu precisión.
> O: el entrenamiento del modelo se ha completado pero la precisión del ensayo es de 2%── has revisado todo── la estructura de ajuste, la superparámetro de ajuste, la data de ajuste── el problema es que el ensayo ha usado float32, has usado float16 pero no hay una reducción correcta──

O: se implementa la pérdida de entropía cruzada desde cero. Funciona en pequeños logits. Cuando los logits superan 100, regresa`inf`La máxima suave se desbordó porque`exp(100)`Es más grande de lo que float32 puede representar. cada marco ML maneja esto con un truco de dos líneas.
> O: tu logro es normal. Cuando logros son más de 100 regresos.`inf`✿softmax 溢出了, porque ✿`exp(100)`超了 float32 的表示范围──

La estabilidad numérica no es una preocupación teórica. Es la diferencia entre una carrera de entrenamiento que tiene éxito y una que falla silenciosamente.
> La estabilidad de valores no es un problema teórico. Es la diferencia entre el éxito de entrenamiento y el fracaso silencioso.

## El concepto central.

> **【拓展：Softmax 的数值稳定技巧是面试必考题】**Originario Softmax:`softmax(x) = exp(x) / sum(exp(x))`, cuando x en el medio tiene un valor grande exp 溢出──解法: disminuye el valor máximo `softmax(x) = exp(x - max(x)) / sum(exp(x - max(x)))`, el resultado matemático no cambia pero el valor es estable.`F.cross_entropy`内部使用日志软max而非分开计算,就是这个原因──

### IEEE 754: Cómo almacenan los computadores números reales

Los ordenadores almacenan números reales como valores de puntos flotantes siguiendo el estándar IEEE 754. Una float tiene tres partes: un bit de signo, un exponente y una mantissa (significand).
> Computers según la norma IEEE 754                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

```
Float32 layout (32 bits total):
[1 sign] [8 exponent] [23 mantissa]

Value = (-1)^sign * 2^(exponent - 127) * 1.mantissa
```

La mantissa determina la precisión (cuántos dígitos significativos). El exponente determina el rango (cuán grande o pequeño puede ser un número).
> 尾数决定精度 (Cuánto número válido), índice decide el rango de números (Cuánto número válido)

```
Format     Bits   Exponent  Mantissa  Decimal digits  Range (approx)
float64    64     11        52        ~15-16          +/- 1.8e308
float32    32     8         23        ~7-8            +/- 3.4e38
float16    16     5         10        ~3-4            +/- 65,504
bfloat16   16     8         7         ~2-3            +/- 3.4e38
```

float32 le da aproximadamente 7 dígitos decimales de precisión. float16 le da aproximadamente 3 dígitos. bfloat16 es la respuesta de Google al problema de rango de float16 - el mismo exponente de 8 bits que float32 pero sólo 7 bits mantissa. Para entrenar redes neuronales, el rango importa más que la precisión, por lo que bfloat16 generalmente gana.
> float32  dáte aproximadamente 7 位十进制精度──float16 约 3 位──bfloat16 es la respuesta de Google a la pregunta sobre float16 范围 con un índice de 8 puntos similar a float32 pero sólo 7 位尾数── entrenamiento

### ¿Por qué 0.1 + 0.2 ! es igual a 0.3 ? ¿Por qué 0.1 + 0.2 ! es igual a 0.3 ?

El número 0.1 no puede ser representado exactamente en el punto flotante binario. en base 2, es una fracción repetitiva. Float32 truncado esto a 23 bits de mantissa.
> 0.1 En el punto de flotación de un sistema de dos partes no se puede especificar.

```
In Python:
>>> 0.1 + 0.2
0.30000000000000004

>>> 0.1 + 0.2 == 0.3
False
```

Esto es importante para ML porque: (1) Las comparaciones de pérdidas como `if loss < threshold`Las pruebas de comprobación y reproductibilidad fallan si se comparan los floats con los valores de la suma real.`==`La solución: nunca comparar los flotadores con`==`- Usar .`abs(a - b) < epsilon`o `math.isclose()`¿ Qué ?
> Esto es importante para ML: 1) 损失比较可能出错.`==`Comparar con los puntos de prueba y los puntos de prueba que no se pueden hacer.`==`Comparado con el número de puntos.

### Cancelación catastrófica.

Cuando se restan dos números de puntos flotantes casi iguales, los dígitos significativos se cancelarán y se queda con ruido redondeado promovido a dígitos principales.
> Cuando el número de puntos de vuelo de dos similares se reduce, el número válido se elimina, y el ruido se eleva a un número de vuelo.

```
a = 1.0000001    (stored as 1.00000011920929 in float32)
b = 1.0000000    (stored as 1.00000000000000 in float32)

True difference:  0.0000001
Computed:         0.00000011920929

Relative error: 19.2%
```

La solución: reorganizar las fórmulas para evitar restar números grandes, casi iguales. Para la variación, utilice el algoritmo Welford o centrar los datos primero.
> 修复: Re-排列公式 (re-排列公式) para evitar la reducción de números de grandes aproximaciones, etc. 修复: Re-排列公式 (re-排列公式) para evitar la reducción de números de grandes aproximaciones, etc. 修复: Re-排列公式 (re-排列公式) para evitar la reducción de números de grandes aproximaciones 修复: 修复: Re-排列公式 (re-排列公式) para evitar la reducción de números de números similares 修复: calcular cuáles diferencia en el tiempo con el algoritmo de Welford o datos precentrados 修复:

### Superfluo y subfluo.

El exceso de flujo ocurre cuando un resultado es demasiado grande para representarlo.
> 溢出是结果太大不能表示,下溢是结果太小──

```
Float32 boundaries:
  Maximum:  3.4028235e+38
  Overflow:  anything > 3.4e38 becomes inf
  Underflow: anything < 1.4e-45 becomes 0.0

exp(88.7)  = 3.40e+38   (barely fits in float32)
exp(89.0)  = inf         (overflow)
```

En ML, `exp()`aparece en softmax, sigmoid y cálculos de probabilidad. `log()`aparece en entropía cruzada, probabilidades de registro y divergencia KL.
> En el ML,`exp()`Se encuentra en el cálculo de la probabilidad y de la suavidad.`log()`Aparece en el medio de la trampa, en el medio de la trampa.

### El truco de registro-sumo-exp

Computación`log(sum(exp(x_i)))`El truco: restar el valor máximo antes de exponenciar.
> 直接计算 `log(sum(exp(x_i)))`Número de valores peligrosos: antes de la indicificación, se reduce el valor máximo.

```
log(sum(exp(x_i))) = max(x) + log(sum(exp(x_i - max(x))))
```

Por qué funciona esto: después de restar `max(x)`, el exponente más grande es `exp(0) = 1`No es posible el desbordamiento. Al menos un término en la suma es 1, por lo que la suma es al menos 1, y `log(1) = 0`No hay flujo de bajo .`-inf`Es posible.
> ¿Por qué es efectivo: reducir `max(x)`后, el máximo índice es `exp(0) = 1`△ imposible de superar. △ por lo menos uno es 1, por lo que y por lo menos 1,`log(1) = 0` Imposible bajar sobre `-inf`¿Qué es eso?

Este truco aparece en todas partes en ML: normalización de la máxima suave, pérdida de entropía cruzada, suma de probabilidad de registro, mezcla de Gaussianos, inferencia variativa.
> Esta técnica está presente en el ML:softmax 归化、交叉损失、对数概率求和、高斯混合、变分推断──

### ¿Por qué Softmax necesita el truco de la subtracción max?

Sin el truco, los logitos de [100, 101, 102] causan sobrecarga.
> 没有技巧时,logits [100, 101, 102] 导致溢出──有技巧时,减去最大(x) = 102:

```
exp(100 - 102) = exp(-2) = 0.135
exp(101 - 102) = exp(-1) = 0.368
exp(102 - 102) = exp(0)  = 1.000
sum = 1.503

softmax = [0.090, 0.245, 0.665]
```

Las probabilidades son idénticas, el cálculo es seguro, no es una optimización, es un requisito para la corrección.
> La probabilidad es la misma. La seguridad de la calculación.

### NaN y Inf: Detección y Prevención

`nan`y `inf`Se propagan por virus a través de la computación.`nan`en una actualización de gradiente hace el peso `nan`, que produce cada salida posterior `nan`El entrenamiento está muerto en un paso.
> `nan`Y `inf`通过计算病毒式传播――梯度更新中的一个 `nan`Que el poder de cambio`nan`, hacer que después todo el producto se cambie`nan`¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡

¿ Cómo ?`nan`aparece: `0.0 / 0.0`¿ Qué ?`inf - inf`¿ Qué ?`inf * 0`¿ Qué ?`sqrt()`de negativo, `log()`Prevención: entradas de acoplamiento a`exp()`, añadir epsilon a los denominadores, utilizar implementaciones estables, recortes de gradientes.
> `nan`¿Cómo se presenta:`0.0/0.0`¿Qué es esto?`inf-inf`¿Qué es esto?`inf*0`、 negativo número `sqrt()`、 negativo número `log()` Prevención: limitación`exp()`输入、给分母加 epsilon、使用稳定实现、梯度剪──

### Verificación de gradientes numéricos Verificación de gradientes numéricos

Los gradientes analíticos (de la retropropagación) pueden tener errores.
> 解析梯度 (desde la dirección contraria) puede haber un error.

```
df/dx ~= (f(x + h) - f(x - h)) / (2h)
```

Reglas de oro: relative_error < 1e-7: perfecto; < 1e-5: aceptable; > 1e-3: algo está mal; > 1: completamente incorrecto.
> 经验法则:相对误差 < 1e-7:完美; < 1e-5:可接受;> 1e-3:有问题;> 1:完全错误──

### Entrenamiento de precisión mixta Entrenamiento de precisión mixta

Las GPU modernas tienen Cores Tensor que calculan las multiplicidades de las matrices float16 2-8 veces más rápido que float32.
> 现代 GPU tiene tensión Core, float16 矩阵乘法比 float32 快 2-8 倍──混合精度训练利用这一点──

```
1. Maintain float32 master copy of weights
2. Forward pass in float16 (fast)
3. Compute loss in float32 (prevents overflow)
4. Backward pass in float16 (fast)
5. Scale gradients to float32
6. Update float32 master weights
```

La solución para el flujo inferior de float16 es la escala de pérdidas: multiplicar la pérdida por un factor de gran escala, recortar hacia atrás calcula gradientes más grandes, dividir por escala antes de actualizar los pesos.
> float16 下溢的修复是损失缩放:将损失乘以缩放因子,反向传播计算更大的梯度,更新权重前除以缩放因子,

### bfloat16 vs float16: por qué bfloat16 gana para entrenamiento

El float16 tiene una mayor precisión (10 bits de mantissa) pero un rango limitado (máximo ~65,504).
> float16 精度更高(10 位尾数) pero el alcance limitado(最大 ~65,504)。bfloat16 精度较低但范围与 float32 相同(最大 ~3.4e38)。

### El corte gradual.

Los gradientes explosivos ocurren cuando los gradientes crecen exponencialmente. Dos tipos de recortes: clip por valor (clam cada elemento) y clip por norma (escala todo el vector para que su norma no exceda un umbral).`torch.nn.utils.clip_grad_norm_()`- Sí, lo hace.
> 梯度爆炸发生在梯度指数增长时――两种剪裁:按值剪裁 限制每个元素) 和按范数剪裁 缩放整个向量使范数不超过值)──按范数剪裁保留梯度方向──

Valores típicos: `max_norm=1.0`para transformadores, `max_norm=0.5`para RL, `max_norm=5.0`para redes más simples.
> 典型值:Transformer 用 `max_norm=1.0`,RL Usado`max_norm=0.5`, simple uso de la red `max_norm=5.0`¿Qué es eso?

### Bugs numéricos comunes de ML                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

**Bug: Loss is NaN after a few epochs.**Causa: logits demasiado grandes, softmax sobrefluido.
> **Bug: 几个 epoch 后 loss 变 NaN。**原因:logits 太大,softmax 溢出──修复:使用稳定softmax,降低学习率,添加梯度剪──

**Bug: Validation accuracy is lower by 1-3%.**Causa: precisión mixta sin una escala de pérdida adecuada.
> **Bug: 验证精度低 1-3%。**原因:混合精度没有正确的损失缩放──修复:启动动态损失缩放,或切换到bfloat16──

**Bug: `exp()` returns `inf` in loss computation.**Corrección: uso `torch.nn.functional.log_softmax()`que implementa log-sum-exp internamente.
> **Bug: 损失计算中 `exp()` 返回 `inf`。**修复: usar `torch.nn.functional.log_softmax()`¿Qué es eso?

## Construye y realiza.

### Paso 1: Demuestra los límites de precisión de los puntos flotantes.
**Bug: Validation accuracy is lower than expected by 1-3%.**
Causa: precisión mixta sin una escalación adecuada de pérdidas.
Corrección: habilitar la escalación dinámica de pérdidas o cambiar a bfloat16.

**Bug: Gradient norms are 0.0 for some layers.**
Causa: neuronas muertas de ReLU (todas las entradas negativas), o float16 bajo flujo.
Corrección: utilizar LeakyReLU o GELU, usar escala de gradientes, comprobar la inicialización del peso.

**Bug: Model works on one GPU but gives different results on another.**
Causa: orden de acumulación de puntos flotantes no determinista. Las reducciones paralelas de GPU suman en diferentes órdenes en diferentes equipos, y la adición de puntos flotantes no es asociativa.
Corrección: acepta pequeñas diferencias (1e-6), o fija `torch.use_deterministic_algorithms(True)`Y acepta la pena de velocidad.

**Bug: `exp()` returns `inf` in loss computation.**
Causa: los logits crudos pasados a `exp()`Sin el truco de la subtracción máxima.
Corrección: uso `torch.nn.functional.log_softmax()`que implementa log-sum-exp internamente.

**Bug: Training diverges after switching from float32 to float16.**
Causa: float16 no puede representar magnitudes de gradiente por debajo de 6e-8 o activaciones por encima de 65,504.
Corrección: utilizar precisión mixta con escala de pérdida (AMP), o utilizar bfloat16 en su lugar.

```figure
logsumexp-stability
```

## Construye el mismo

### Paso 1: Demostrar los límites de precisión de los puntos flotantes

```python
print("=== Floating Point Precision ===")
print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}")
print(f"Difference: {(0.1 + 0.2) - 0.3:.2e}")
```

### Paso 2: Implementar naividad vs. estabilidad softmax. Paso 2: lograr simple y estabilidad softmax.

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

### Paso 3: Implementar log-sum-exp estable.

```python
def logsumexp_stable(values):
    c = max(values)
    return c + math.log(sum(math.exp(v - c) for v in values))
```

### Paso 4: Implementar la entropía cruzada estable.

```python
def cross_entropy_stable(true_class, logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = math.log(sum(math.exp(s) for s in shifted))
    log_prob = shifted[true_class] - log_sum_exp
    return -log_prob
```

### Paso 5: Control gradual.

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

## Usalo con el marco de ejecución

¿ Qué ?`code/numerical.py`para implementaciones completas con todas las pruebas de casos de riesgo.
> 完整实现见 `code/numerical.py`¿Qué es eso?

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

## Envíe el producto .

Esta lección produce:
> En el curso de la educación

- `code/numerical.py`con softmax estable, log-sum-exp, entropía cruzada, control de gradientes y simulación de precisión mixta
  包含稳定软max、log-sum-exp、交叉、梯度检查和混合精度模拟
- `outputs/prompt-numerical-debugger.md`para el diagnóstico de la NNA/Inf y de los problemas numéricos en la formación
  Usado para el diagnóstico de entrenamiento en el problema de NaN/Inf y valores

## Los ejercicios.

1. **Catastrophic cancellation.**Calcule la variación de [1000000.0, 1000001.0, 1000002.0] utilizando la fórmula ingenua `E[x^2] - E[x]^2`Luego computa con el algoritmo en línea de Welford. Compara los errores con la varianza verdadera (0.6667).
   **灾难性抵消。**Utilizando simples fórmulas y Welford 算法 calcular el diferencial de las formas, comparación y error.

2. **Precision hunt.**Encuentra el menor valor positivo float32 `x`Es así .`1.0 + x == 1.0`- Verifique si coincide .`numpy.finfo(numpy.float32).eps`¿ Qué ?
   **精度搜索。**找到使   encontrar`1.0 + x == 1.0`La mínima flotación correcta es 32 ⋅valor.

3. **Log-sum-exp edge cases.**Prueba su`logsumexp_stable`Función con: a) todos los valores iguales, b) un valor mucho mayor que los demás, c) todos los valores muy negativos (-1000).
   **Log-sum-exp 边界情况。**测试稳定 log-sum-exp 在极端输入下表现──

4. **Gradient checking a neural network layer.**Implementar una sola capa lineal `y = Wx + b`y verificar la corrección de una matriz de peso 3x2.
   **梯度检查神经网络层。**实现 un nivel lineal de nivel y verificar la correccinidad.

5. **Loss scaling experiment.**Simula el entrenamiento con float16: mide qué fracción de gradientes se vuelve cero.
   **损失缩放实验。**模拟 float16 训练, medir la gradiente en proporción de 0, luego aplicar la pérdida reducida a la re-medida¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

## Términos clave .

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

## Más Leer más Leer más

- [What Every Computer Scientist Should Know About Floating-Point Arithmetic (Goldberg 1991)](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)-- la referencia definitiva
  浮点算术 autoridad referente
- [Mixed Precision Training (Micikevicius et al., 2018)](https://arxiv.org/abs/1710.03740)-- el documento de NVIDIA sobre la escala de pérdidas
  NVIDIA 损失缩放论文
- [AMP: Automatic Mixed Precision (PyTorch docs)](https://pytorch.org/docs/stable/amp.html)-- Guía práctica
  PyTorch 混合精度实践指南
- [bfloat16 format (Google Cloud TPU docs)](https://cloud.google.com/tpu/docs/bfloat16)-- por qué Google eligió este formato
  Google 选择 bfloat16 的原因
- [Kahan Summation (Wikipedia)](https://en.wikipedia.org/wiki/Kahan_summation_algorithm)-- algoritmo para reducir el error de redondeo
  减少舍进差的 Kahan 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法 求和算法
