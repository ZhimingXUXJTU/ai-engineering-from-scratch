# Gradiente de control y recomputación de activación .

> Backprop mantiene cada activación intermedia. En parámetros 70B y 128K contexto que es 3 TB de activaciones por rango.

> **【中文解读】**Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información: Reproducción de la información

> **【拓展：梯度检查点→大模型训练】**梯度检查点是训练大模型的标标技术――PyTorch's torch.utils.checkpoint、DeepSpeed's activation checkpointing 都是这一思想的实现――En el entrenamiento de 128K, los puntos de control selectivos pueden ahorrar un 60%+ de la muestra―

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 10·04(Pre-Training GPT);反向传播算法;GPU 显存层次(SRAM vs HBM)。本节是训练超大模型 + 长上下文时的关键技术。
> ¿ Qué es esto ?**【类比】**梯度检查点 = 出差只带必要文件──反向传播──工作完成后回顾所有材料;不检查点 = 把出差路上所有的材料都背着(占满行李箱);全检查点 = 只带护照,需要时重新打印(重算成本高);选择性检查点 = 只扔可重算的(如草稿),保留难重建的(如合同) 平衡存储和速度显――

**Type:** Build
**Languages:** Python (with numpy, optional torch)
**Prerequisites:** Phase 10 Lesson 04 (Pre-Training Mini-GPT), Phase 10 Lesson 05 (Scaling & Distributed)
**Time:** ~70 minutes

## El problema es la introducción del problema

El entrenamiento de un transformador almacena, para cada capa, las entradas de cada operación que se diferencia hacia atrás: las entradas de atención, las proyecciones Q/K/V, la salida de softmax, las entradas FFN, las salidas normales y el flujo residual.`d`, longitud de la secuencia `L`, lote `B`, esto es por orden de`12 * B * L * d`flotan por capa.

>                                                                                                                                                                                                                                                               `d`、序列长度 `L`、 cantidad `B`De las capas, esto es aproximadamente cada capas.`12 * B * L * d`个浮点数── es el número de puntos

Para`d=8192, L=8192, B=1`, es 800 MB / capa en BF16. Un modelo de 64 capas es 51 GB de activaciones  y eso es antes de que se multiplica por el tamaño del microbatch, antes de que se añade la atención-softmax intermedios (`L^2`y antes de que se factoren las copias parciales tensor-paralelo.

>  para `d=8192, L=8192, B=1`,BF16 下每层800 MB──64 层模型的激活值为51 GB这还没有乘以微批次大小,还没有加重注意软max中值(每头`L^2`), no se ha previsto que la cantidad de piezas de la misma

El proyecto de ley de dos caras: los pesos BF16 más el estado de optimización pueden caber en 80 GB, pero las activaciones te empujan más allá. El punto de control gradual (también conocido como recomputo de activación) es la solución estándar. Deja caer la mayoría de las activaciones; vuelve a avanzar durante el retroceso para recuperarlas. Costo: FLOPs adicionales. Beneficio: caídas de memoria por la proporción de los segmentos de los puntos de control a las capas totales.

> 双面账单:BF16 权重加优化器状态可能放入80GB,但激活值让你超出──梯度检查点(又称激活重计算) es el estándar de revisión── abandonar la mayor parte del valor activado; hacer de nuevo hacia adelante para la difusión durante el período de reversación para recuperarlos──代价:额外FLOPs──收益:显存按检查段段数与总层数的比例下降──

Si se hace ingenuamente, el punto de control cuesta aproximadamente un 33% más de FLOPs de paso hacia adelante por paso. Si se hace bien, se ahorra 5 veces la memoria por la "elección inteligente" de Korthikanti et al. Se ahorra 5 veces la memoria para menos del 5% de FLOP. Y con las matmulas FP8, FSDP offload, y el experto paralelo MoE esto realmente importa: no puedes permitirte ni la memoria ni la computación desperdiciada.

## El concepto central.

> **【中文解读】**梯度检查点(Gradient Checkpointing) con el cálculo de cambio de almacenamiento: previo a la transmisión no se conserva el valor activo medio, reverso a la transmisión recalculación de la necesidad de activar. Esto se realizará a un precio de extracomputación de aproximadamente el 30%, el valor de activación de la reserva reducirá aproximadamente el 70%。

> **【拓展：梯度检查点在训练中的关键作用】**El punto de control de gradiente es la técnica de etiquetado del modelo de entrenamiento. Para Llama 3 70B, no hay un punto de control en el que cada muestra requiere alrededor de 16 GB de valor activado, disminuyendo hasta 5 GB después de su inicio.


### Lo que realmente necesita el retraso

`output = layer(input)`- El retraso quiere .`grad_input`y `grad_params`Para calcularlos se necesita:

- `input`(para calcular `grad_params = input.T @ grad_output`para capas lineales)
- algunos intermedios derivados de activación (la derivada de ReLU/GELU/softmax depende del valor de activación)

El pase delantero almacena estos automáticamente en el gráfico de autogrado.`tensor.retain_grad()`y cada operación que necesita su entrada conserva una referencia.

### Un control completo ingenuo

Divide la red en dos .`N`Se puede utilizar el sistema de transferencia de datos de los segmentos. durante el futuro, almacena sólo la * entrada* de cada segmento. cuando el retroceso necesita intermedios, vuelva a ejecutar el paso del segmento hacia adelante para materializarlos, luego diferenciar.

Ejemplo: Transformador de 32 capas dividido en 32 segmentos de 1 capa cada uno.

- Memoria: 32 entradas de capas (pequeñas) vs 32 * (volumen de activación por capas) (enorme).
- Computación adicional: 1 paso más adelante por segmento, es decir, ~33% más FLOPs hacia adelante en total (ya que el retroceso es 2 veces hacia adelante, el paso completo se convierte en 1 + 1 + 2 = 4 unidades en lugar de 1 + 2 = 3).

Esta es la receta original de Chen et al. 2016: un punto de control cada `sqrt(L)`Para L=64, eso es 8 puntos de control.

### Control selectivo (Korthikanti 2022)

No todas las activaciones cuestan lo mismo.`B*L*L*heads`La activación oculta de FFN es `B*L*4d`Para secuencias largas, el softmax domina.

El control selectivo mantiene las activaciones baratas para almacenar (proyecciones lineales, residuos) y recalcula sólo las costosas (atención).

Megatron-Core implementa esto como recomputo de activación "selectiva".

### Descarga

Alternativa a la recomputada: envío de activaciones a la RAM de la CPU entre hacia adelante y hacia atrás. Requiere ancho de banda PCIe; beneficioso cuando el ancho de banda ocioso excede el costo de la rematerialización.

FSDP2 descarga como una opción de primera clase. Descarga brilla cuando la GPU está cerrada en la memoria pero la transferencia de CPU-GPU tiene espacio de cabeza.

### Modelo de costes de recomputo

FLOPs por paso con un control ingenuo cada `k`las capas de `L`¿Qué es esto ?

```
flops_fwd_normal = L * f_layer
flops_bwd_normal = 2 * L * f_layer
flops_total_normal = 3 * L * f_layer

flops_fwd_ckpt = L * f_layer
flops_recompute = L * f_layer  # one extra forward per layer in the segment
flops_bwd_ckpt = 2 * L * f_layer
flops_total_ckpt = 4 * L * f_layer
overhead = 4 / 3 - 1 = 0.33 = 33%
```

Con el control selectivo recompite sólo el núcleo de atención, no toda la capa:

```
flops_recompute_selective = L * f_attention ~= L * f_layer * 0.15
overhead_selective = (3 + 0.15) / 3 - 1 = 0.05 = 5%
```

### Modelo de ahorro de memoria

Volumen de activación por capa: `A`- Para .`L`capas, memoria de activación total: `L * A`¿ Qué ?

Punto de control completo (tamaño del segmento 1): solo almacenamiento `L * input_volume`(~)`L * 1/10 A`para un transformador estándar).`9 * L * A * 1/10`¿ Qué ?

Punto de control cada`k`capas: almacenamiento `L/k * A`Además`k-1`valor de las capas dentro del segmento activo.

En el`k = sqrt(L)`, memoria y recomputo costos tanto de escala con `sqrt(L)` la compensación óptima para las capas de coste uniforme.

### Cuando no hay punto de control

- Las capas más profundas de una fase de tubería ya están en vuelo.
- Las primeras y últimas capas si dominan la computación del escenario (raras en transformadores).
- Los núcleos de atención que ya usan FlashAttention  Flash ya recalcula el softmax rápido, por lo que el control adicional de nivel de capa añade poco en la parte superior.

### Modelos de aplicación

1. **Function wrapper:**Envuelve un segmento en `torch.utils.checkpoint.checkpoint(fn, input)`Sólo las tiendas PyTorch .`input`, recalcula todo lo demás hacia atrás.

2. **Decorator-based:**las capas de etiqueta como puntos de control; el entrenador decide en el momento de la configuración qué segmentos se envuelven.

3. **Manual explicit recompute:**Escriba el pase hacia atrás usted mismo, llamando una costumbre `recompute_forward`que duplica el forward con la entrada almacenada.

Los tres dan el mismo resultado funcional.

### Interacción con TP / PP / FP8

- **Tensor parallel:**los datos de entrada de los puntos de control deben recogerse o redistribuirse en la recomputada; se encargarán de los costes de comunicación.
- **Pipeline parallel:**El patrón típico es el de controlar el avance de cada etapa de la tubería para que los microbatches de orden inverso puedan reutilizar la memoria de activación.
- **FP8 recompute:**los historias de amax actualizados durante la recomputada deben coincidir con los de los futuros originales, o las derivaciones de la escala FP8.


> **【拓展：梯度检查点与 FSDP 的配合】**Los puntos de control de gradiente suelen ser utilizados en combinación con los FSDP/ZeRO. Los puntos de control de gradiente pueden ser utilizados en el estado de los parámetros y optimizadores de FSDP, los puntos de control de gradiente pueden ser utilizados para reducir el valor de activación de los dispositivos de control de gradiente.


## Construye y realiza.
```figure
activation-recompute
```

## Construye el mismo

### Paso 1: Un modelo de juguete con segmentos

```python
import numpy as np


def linear_forward(x, w, b):
    return x @ w + b


def relu(x):
    return np.maximum(x, 0)


def layer_forward(x, w1, b1, w2, b2):
    h = relu(linear_forward(x, w1, b1))
    return linear_forward(h, w2, b2)


def model_forward(x, params):
    activations = [x]
    h = x
    for w1, b1, w2, b2 in params:
        h = layer_forward(h, w1, b1, w2, b2)
        activations.append(h)
    return h, activations
```

### Paso 2: Naividad hacia atrás Necesita todas las actividades

```python
def model_backward(grad_output, activations, params):
    grads = [None] * len(params)
    g = grad_output
    for i in range(len(params) - 1, -1, -1):
        w1, b1, w2, b2 = params[i]
        x_in = activations[i]
        h_pre = linear_forward(x_in, w1, b1)
        h = relu(h_pre)
        gh = g @ w2.T
        gw2 = h.T @ g
        gb2 = g.sum(axis=0)
        g_pre = gh * (h_pre > 0)
        gx = g_pre @ w1.T
        gw1 = x_in.T @ g_pre
        gb1 = g_pre.sum(axis=0)
        grads[i] = (gw1, gb1, gw2, gb2)
        g = gx
    return g, grads
```

### Paso 3: punto de control-Cada memoria

```python
def model_forward_checkpointed(x, params, k=4):
    saved_inputs = [x]
    h = x
    for i, (w1, b1, w2, b2) in enumerate(params):
        h = layer_forward(h, w1, b1, w2, b2)
        if (i + 1) % k == 0:
            saved_inputs.append(h)
    return h, saved_inputs


def model_backward_checkpointed(grad_output, saved_inputs, params, k=4):
    grads = [None] * len(params)
    g = grad_output
    segments = [(j * k, min((j + 1) * k, len(params))) for j in range(len(saved_inputs))]
    for seg_idx in range(len(saved_inputs) - 1, -1, -1):
        start, end = segments[seg_idx]
        if start >= end:
            continue
        x_in = saved_inputs[seg_idx]
        _, seg_acts = model_forward(x_in, params[start:end])
        g, seg_grads = model_backward(g, seg_acts, params[start:end])
        for j, gr in enumerate(seg_grads):
            grads[start + j] = gr
    return g, grads
```

### Paso 4: Modelo de costes

```python
def checkpoint_cost(n_layers, segment_size, flops_per_layer=1.0):
    fwd = n_layers * flops_per_layer
    recompute = n_layers * flops_per_layer
    bwd = 2 * n_layers * flops_per_layer
    return {
        "fwd": fwd,
        "recompute": recompute,
        "bwd": bwd,
        "total": fwd + recompute + bwd,
        "overhead_vs_no_ckpt": (fwd + recompute + bwd) / (fwd + bwd) - 1.0,
    }


def selective_checkpoint_cost(n_layers, attention_fraction=0.15,
                              flops_per_layer=1.0):
    fwd = n_layers * flops_per_layer
    recompute = n_layers * attention_fraction * flops_per_layer
    bwd = 2 * n_layers * flops_per_layer
    return {
        "fwd": fwd,
        "recompute": recompute,
        "bwd": bwd,
        "total": fwd + recompute + bwd,
        "overhead_vs_no_ckpt": (fwd + recompute + bwd) / (fwd + bwd) - 1.0,
    }
```

### Paso 5: Estimador de memoria

```python
def activation_memory_mb(n_layers, hidden=8192, seq=8192,
                        batch=1, bytes_per_value=2):
    per_layer = 12 * batch * seq * hidden * bytes_per_value
    return n_layers * per_layer / 1e6


def memory_after_checkpoint(n_layers, segment_size, hidden=8192,
                           seq=8192, batch=1, bytes_per_value=2):
    n_seg = max(1, n_layers // segment_size)
    saved = (n_seg + segment_size) * 1 * batch * seq * hidden * bytes_per_value
    return saved / 1e6
```

### Paso 6: Tamaño óptimo del segmento

```python
def optimal_segment(n_layers):
    return int(round(np.sqrt(n_layers)))
```

### Paso 7: Decisión selectiva sobre los puntos de control

```python
def should_recompute(layer_type, activation_bytes, recompute_flops_ratio):
    if layer_type == "attention" and activation_bytes > 100 * 1e6:
        return True
    if layer_type == "ffn" and activation_bytes > 500 * 1e6:
        return recompute_flops_ratio < 0.1
    return False
```

## Usalo con el marco de ejecución

- **torch.utils.checkpoint**¿ Qué es esto ?`from torch.utils.checkpoint import checkpoint` el envoltorio canónico en PyTorch. Envuelve una función; almacena sólo entradas, recalcula hacia atrás.
- **Megatron-Core activation recomputation**: apoyos `selective`¿ Qué ?`full`, y `block`Modos de formación estándar en 2024+ fronterizo.
- **FSDP2 offload**¿ Qué es esto ?`module.to_empty(device="cpu")`con`offload_policy`en FSDP2 se desglosan las activaciones a la CPU en lugar de recomputar.
- **DeepSpeed ZeRO-Offload**: Descarga de CPU para estados y activaciones de optimización, complementando el punto de control.

## Envíe el producto .

Esta lección produce`outputs/prompt-activation-recompute-policy.md` un prompt que toma la configuración de su modelo (capas, ocultos, secu, lotes) y la memoria de GPU disponible y emite una política de recomputo por capa (no / selectiva / completa / descarga).

> 本课产 出  `outputs/prompt-activation-recompute-policy.md` Una configuración de modelo aceptada (laje número ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ 

## Los ejercicios.

1. Verifique la exactitud.`model_forward`¿ Qué es eso ?`model_backward`(activaciones completas) vs `model_forward_checkpointed`¿ Qué es eso ?`model_backward_checkpointed`Los gradientes de parámetros deben ser idénticos a la precisión de la máquina.
   En inglés, "Experiencia de la verdad".`model_forward`¿ Qué es eso ?`model_backward`(完整激活) con `model_forward_checkpointed`¿ Qué es eso ?`model_backward_checkpointed`(分段) ◊ La escala de los parámetros debe ser de acuerdo con la precisión de la máquina.

2. Tamaño del segmento de barrido `k`de 1 a `L`- Traza FLOP sobre la cabeza y la memoria.
   En español: 将段大小`k`Desde 1 hasta`L`◊ dibujar FLOP 开销和内存── encontrar los puntos de la curva──

3. Implementar un punto de control selectivo: almacenar la entrada del módulo de atención pero no sus intermediarios.
   En la actualidad, el sistema de control de datos de la memoria de un sistema de datos de datos de datos de un sistema de datos de datos de datos de un sistema de datos de datos de datos de un sistema de datos de datos de datos de un sistema de datos de datos de datos de un sistema de datos de datos de un sistema de datos de datos de datos de un sistema de datos de datos de datos de un sistema de datos de datos de datos de un sistema de datos de datos de datos de un sistema de datos de datos de datos de un sistema de datos de datos de datos de datos de un sistema de datos de datos de datos de datos de un sistema de datos de datos de datos de datos de un sistema de datos de datos de datos de datos de un sistema de datos de datos de datos de datos de datos de un sistema de datos de datos de datos de datos de datos de datos de un sistema de datos de datos de datos de datos de datos de datos de un sistema de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de datos de

4. Añadir descarga. Guardar las entradas de segmentos en un simulado "buffer de CPU" (una lista separada). Medir "ancho de banda de PCIe" como bytes/tiempo y encontrar el punto de equilibrio entre descarga y recomputo.
   China: 添加卸载. 将段输入保存到模拟的"CPU缓冲区" (en inglés)  单独的列表)  以字节/时间测量 (en inglés) PCIe 带宽 (en inglés) 并找到卸载和重计算之间的平衡点.

5. Indique un verdadero transformador PyTorch con y sin `torch.utils.checkpoint`. Medir la memoria (via `torch.cuda.max_memory_allocated`) y el tiempo de paso.
   Chino:对真实 PyTorch transformador 分别使用和不使用 `torch.utils.checkpoint`进行基准测试──测量内存(通过 `torch.cuda.max_memory_allocated`) y el tiempo largo.

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Gradient checkpointing | "Save memory by redoing forward" | Store segment inputs only; recompute intermediates during backward to get gradient-support tensors | 梯度检查点，仅保存段输入，反向时重算中间值 |
| Activation recomputation | "Same as checkpointing" | The HPC-flavored name for the same technique | 激活重计算，梯度检查点的 HPC 叫法 |
| Segment size (k) | "How many layers per checkpoint" | Number of layers whose intermediates are dropped and rematerialized together | 段大小，每个检查点包含的层数 |
| Selective checkpointing | "Korthikanti's trick" | Recompute only expensive-to-store activations (attention softmax); keep cheap ones | 选择性检查点，只重算存储昂贵的激活 |
| Full checkpointing | "The naive version" | Recompute every layer's intermediates in every segment | 全量检查点，朴素版本重算所有中间值 |
| Block checkpointing | "Coarse-grained" | Checkpoint whole transformer blocks; largest granularity | 块级检查点，以 Transformer 块为粒度 |
| FLOP overhead | "The compute tax" | Extra FLOPs per step = (recompute FLOPs) / (fwd + bwd FLOPs); 33% naive, 5% selective | FLOP 开销，朴素版 33%，选择性版 5% |
| Activation offload | "Ship to CPU" | Move activations to CPU RAM across forward->backward; alternative to recompute | 激活卸载，将激活移到 CPU 内存 |
| sqrt-L rule | "The classical optimum" | For uniform-cost layers, optimal checkpoint spacing is sqrt(L) layers | sqrt-L 规则，均匀层代价的最优检查点间隔 |
| Attention-softmax volume | "The O(L^2) problem" | L^2 * heads * batch floats; dominates activation memory at long contexts | 注意力 softmax 体积，O(L^2) 的显存问题 |

## Más Leer más Leer más

- [Chen et al., 2016 -- "Training Deep Nets with Sublinear Memory Cost"](https://arxiv.org/abs/1604.06174)-- el papel original que formalizó el control de gradientes
- [Korthikanti et al., 2022 -- "Reducing Activation Recomputation in Large Transformer Models"](https://arxiv.org/abs/2205.05198)-- recomputo selectivo de activación y análisis formal de costes
- [Pudipeddi et al., 2020 -- "Training Large Neural Networks with Constant Memory using a New Execution Algorithm"](https://arxiv.org/abs/2002.05645)-- enfoque alternativo de memoria constante mediante rematerialización en modo inverso
- [Ren et al., 2021 -- "ZeRO-Offload: Democratizing Billion-Scale Model Training"](https://arxiv.org/abs/2101.06840)-- descarga de activación a escala
- [PyTorch torch.utils.checkpoint docs](https://pytorch.org/docs/stable/checkpoint.html)-- la API estándar
- [Megatron-Core activation recomputation documentation](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/features/memory_optimizations.html)-- modos selectivos, completos y bloqueados
