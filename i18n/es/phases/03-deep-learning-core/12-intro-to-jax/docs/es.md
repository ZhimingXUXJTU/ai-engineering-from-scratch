# Introducción a JAX JAX Entrada

> PyTorch muta los tensores, TensorFlow construye gráficos, JAX compila funciones puras, y la última cambia la forma en que pensamos sobre el aprendizaje profundo.

> **【中文解读】**PyTorch 可变张量,TensorFlow 静态图,JAX 编译纯函数──JAX 函数式编程范式是深度学习的新方向Google de Gemini 就用JAX 训练──本章学习JAX 的核心:jit 编译、vmap 向量化、grad 自动微分──

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 03 Lessons 01-10, basic NumPy
**Time:** ~90 minutes

## Objetivos de aprendizaje

- Escriba código de red neuronal de función pura utilizando la API funcional de JAX (jax.numpy, jax.grad, jax.jit, jax.vmap)
- Explica la diferencia clave de diseño entre la mutación ansiosa de PyTorch y el modelo de compilación funcional de JAX
- Aplicar compilación jit y vectorization vmap para acelerar los bucles de entrenamiento en comparación con Python ingenuo
- Entrenar una red simple en JAX y contrastar la gestión explícita del estado con el enfoque orientado a objetos de PyTorch

> **【中文解读】**Este capítulo de aprendizaje JAX de la función de programación de la estructura. Con PyTorch de la diferencia central: no hay cambios de estado.

## El problema es la introducción del problema

Sabes cómo construir redes neuronales en PyTorch.`nn.Module`, llamando`.backward()`Funciona, millones de personas lo usan.

> Ya sabes cómo construir una red neuronal en PyTorch.`nn.Module`,调用 `.backward()`, paso a la optimización. Puede trabajar. Millones de personas lo usan.

Pero PyTorch tiene una limitación en su ADN: rastrea las operaciones ansiosamente, una a la vez, en Python.`tensor + tensor`Cada paso de entrenamiento reinterpreta el mismo código Python. Esto funciona bien hasta que necesitas entrenar un modelo de 540 mil millones de parámetros a través de 2.048 TPU.

> Pero el ADN de PyTorch tiene una limitación: es un proceso de seguimiento de cada uno de ellos, que se ejecuta en Python.`tensor + tensor`Todo es un inicio interno único. Cada entrenamiento es una reinterpretación del mismo código Python. Esto es necesario para entrenar a través de 2.048 TPU.

Google DeepMind entrena a Gemini en JAX. Anthropic entrenó a Claude en JAX. Estas no son pequeñas operaciones, son las operaciones de entrenamiento de red neuronal más grandes de la Tierra. Eligieron JAX porque trata su bucle de entrenamiento como un programa compilable, no una secuencia de llamadas de Python.

> Google DeepMind utiliza JAX  entrenamiento Gemini。Antropico utiliza JAX  entrenamiento Claude。 Estos no son operaciones a pequeña escala Son el mayor operador de la red neuronal de la Tierra。 Ellos eligieron JAX porque considera su ciclo de entrenamiento como un programa complicable, en lugar de una serie de Python 调用。

JAX es NumPy con tres superpoderes: diferenciación automática, compilación JIT a XLA y vectorization automática. Escribir una función que procesa un ejemplo. JAX le da una función que procesa un lote, calcula gradientes, compila al código de máquina y se ejecuta en múltiples dispositivos. Todo sin cambiar la función original.

> JAX es un sistema de tres supercapacidades numéricas: automático, JIT, compilado a XLA y automático, dimensionado. Usted escribe una función de procesamiento de una sola muestra. JAX le da una función de procesamiento de la cantidad, la escala de cálculo, la composición de código de máquina y las funciones que se ejecutan en varios dispositivos.

> **【中文解读】**Las limitaciones de PyTorch: cada entrenamiento reinterpreta el código Python, cada tensor 运算 es un núcleo independiente 启动── en 2048 bloques TPU 训练 540B 参数模型, esta apertura es inaceptable──JAX Colocar el ciclo de entrenamiento en código de máquina, saltar la capa Python, directamente en el acelerador 运行──

> **【拓展：JAX 的工业应用】**Google DeepMind utiliza JAX  entrenamiento Gemini(máxima versión según la historia más de 1T 参数)。Antropico utiliza JAX  entrenamiento Claude 系列。Google AlphaFold 2/3 también utiliza JAX。JAX tiene ventajas en un entrenamiento distribuido de gran tamaño: con pmap en miles de bloques de TPU, con shard_map hacer un modelo y hacer un seguimiento。 pero la dificultad de ajuste de JAX es mucho mayor que PyTorch。

## El concepto central.

### La filosofía de JAX.

JAX es un marco funcional.`.backward()`En cambio:

> JAX es un marco de funciones.`.backward()`方法──取而代之 es:

| PyTorch | JAX |
|---------|-----|
| `nn.Module` class with state | Pure function: `f(params, x) -> y` |
| `loss.backward()` | `jax.grad(loss_fn)(params, x, y)` |
| Eager execution | JIT compilation via XLA |
| `for x in batch:` manual loop | `jax.vmap(f)` auto-vectorization |
| `DataParallel` / `FSDP` | `jax.pmap(f)` auto-parallelism |
| Mutable `model.parameters()` | Immutable pytree of arrays |

Esta no es una preferencia de estilo. Es una restricción de compilador. La compilación JIT requiere funciones puras - las mismas entradas siempre producen las mismas salidas, sin efectos secundarios. Esa restricción es lo que hace posible 100 veces velocidades.

> Esto no es un tipo de preferencia. Esto es un sistema de composición.

> Esto no es un tipo de preferencia. Esto es un sistema de composición.

### Jax.numpy: La superficie familiar

JAX reimplementa la API NumPy en los aceleradores:

```python
import jax.numpy as jnp

a = jnp.array([1.0, 2.0, 3.0])
b = jnp.array([4.0, 5.0, 6.0])
c = jnp.dot(a, b)
```

Los mismos nombres de funciones, las mismas reglas de transmisión, la misma semántica de corte, pero las matrículas viven en GPU/TPU, y cada operación es rastreable por el compilador.

> La misma función de nombre. La misma regla de difusión. La misma secuencia de texto. Pero el número en la GPU / TPU, cada operación puede ser rastreada por el compilador.

Una diferencia crítica: las matrices JAX son inmutables.`a[0] = 5`En cambio:`a = a.at[0].set(5)`Esto se siente incómodo durante una semana, y luego hace clic -- la inmutabilidad es lo que hace que las transformaciones como`grad`¿ Qué ?`jit`, y `vmap`- Es muy fácil.

> Una clave: JAX 数组是不可变的. No puedo escribir.`a[0] = 5`, sino que usas `a = a.at[0].set(5)` primero empezará a sentirse diferente, luego se dará cuenta de que es la verdad`grad`¿Qué es esto?`jit`Y `vmap`Las bases de la transformación de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura de la estructura.

### Jax.grad: Funcional Autodiff. jax.grad: Función en forma automática

PyTorch une los gradientes a los tensores (`.grad`JAX une gradientes a las funciones.

> PyTorch va a subir la escala a la cantidad de`.grad`)―JAX se añadirá a la función ‖

```python
import jax

def f(x):
    return x ** 2

df = jax.grad(f)
df(3.0)
```

`jax.grad`toma una función y devuelve una nueva función que calcula el gradiente.`.backward()`No hay gráfico de cálculo almacenado en los tensores. El gradiente es sólo otra función que se puede llamar, componer, o JIT-compilar.

> `jax.grad`Recibir una función, regresar a una nueva función de la escala de cálculo― no necesita `.backward()`调用──张量上不存储计算图──梯度只是另一个你可以调用、组合或 JIT 编译的函数──

Esto se compone arbitrariamente:

> Esto puede ser combinado:

```python
d2f = jax.grad(jax.grad(f))
d2f(3.0)
```

Los derivados secundarios, los derivados tercero, los jacobios, los hessianos, todos ellos compuestos.`grad`PyTorch también puede hacer esto (`torch.autograd.functional.hessian`En JAX, es la base.

> Dos fases de la estructura. Tres fases de la estructura.`grad`实现──PyTorch 也能做(`torch.autograd.functional.hessian`), pero es un complemento posterior. En JAX, es la base.

La restricción:`grad`No hay declaraciones impresas dentro (se ejecutan durante el seguimiento, no la ejecución). No hay mutación del estado externo. No hay generación de números aleatorios sin gestión explícita de claves.

> 限制:`grad`Sólo se aplica a funciones puras. No se puede imprimir en el interior.

> **【拓展：JAX 的 grad vs PyTorch 的 autograd】**PyTorch Colocar la gradiencia existe tensor 上(x.grad),JAX Colocar la gradiencia de la función de la salida. Esto significa JAX 天然支持高阶导数(grad((((f))), mientras que PyTorch 需要特殊处理──En JAX, calcular Hessian矩阵只需`jax.hessian(f)`,PyTorch  necesito `torch.autograd.functional.hessian`¿Qué es eso?

### Compilación a XLA

```python
@jax.jit
def train_step(params, x, y):
    loss = loss_fn(params, x, y)
    return loss

fast_step = jax.jit(train_step)
```

En la primera llamada, JAX rastrea la función, registra qué operaciones ocurren, sin ejecutarlas. Luego entrega ese rastro a XLA (Algebra Lineal Acelerada), el compilador de Google para TPU y GPUs. XLA fusiona operaciones, elimina copias redundantes de memoria y genera código de máquina optimizado.

> En la primera modificación, la función de seguimiento de JAX registra las operaciones que ocurren, sin ejecutarlas en realidad. Luego se entrega el seguimiento a XLA, Google para TPU y GPU.

Las llamadas posteriores omiten completamente Python. El código compilado se ejecuta en el acelerador a velocidad de C ++.

> 后续调用完全跳过Python──编译后的代码运行在加速器上以C++ 速度──

Cuando JIT ayuda:

> JIT tiene un escenario útil:

- Pasos de entrenamiento (el mismo cálculo se repite miles de veces)
  En español: train step (también se ha repetido miles de veces)
- Inferencia (el mismo modelo, diferentes entradas)
  Traducción:Tú理(同模型,不同输入)
- Cualquier función llamada más de una vez con entradas de forma similar
  Traducción: cualquier función de forma similar

Cuando JIT duele:

> JIT tiene un escenario malo:

- Funciones con flujo de control de Python que dependen de los valores (`if x > 0`donde x es una matriz rastreada)
  En inglés, traducción de Python 控制流的函数 (en inglés, Python 控制流的函数)`if x > 0`En el caso de x es el número de personas que son seguidas)
- Computaciones de una sola toma (los gastos generales de compilación superan el tiempo de ejecución)
  En español: una vez (en inglés:一次性计算)
- Desarreglo (el rastreo oculta la ejecución real)
  En español: "Há un gran número de personas que han estado haciendo esto".

La restricción de flujo de control es real.`jax.lax.cond`sustituye `if/else`- ¿ Qué ?`jax.lax.scan`sustituye `for`Estos no son opcionales, son el precio de la compilación.

> Control de flujo de restricciones es real.`jax.lax.cond`替代   en el`if/else`¿Qué es eso?`jax.lax.scan`替代   en el`for`循环──These no son opcionales son el precio de la compilación──

### Vmap: Vectorization automática

Escribir una función que procesa un ejemplo:

> Usted escribe una función de tratamiento de un solo muestreo:

```python
def predict(params, x):
    return jnp.dot(params['w'], x) + params['b']
```

`vmap`se eleva para procesar un lote:

```python
batch_predict = jax.vmap(predict, in_axes=(None, 0))
```

`in_axes=(None, 0)`medio: no se entre en lote `params`(compartidos), lote sobre el eje 0 de `x`No hay manual .`for`No hay remodelación, no hay hilo de dimensión de lote, JAX calcula la dimensión de lote y vectoriza todo el cálculo.

> `in_axes=(None, 0)`Se muestra:`params` efectuar el tratamiento de la cantidad de productos`x`El proceso de entrega de la carga se realiza en lote.`for`循环──无需重塑──无需手动传递批量维度──JAX Automatically find out批量维度并向量化整个计算──

Esto no es azúcar sintáctica.`vmap`genera código vectorizado fusionado que se ejecuta 10-100 veces más rápido que un bucle Python.`jit`y `grad`¿Qué es esto ?

> Esto no es un lenguaje.`vmap`Codificación de convergencia de datos, que es 10-100 veces más rápido que Python.`jit`Y `grad`组合:

```python
per_example_grads = jax.vmap(jax.grad(loss_fn), in_axes=(None, 0, 0))
```

Por ejemplo, un gradiente, una línea, es casi imposible en PyTorch sin hacks.

> 逐样本梯度──一行代码── esto es casi imposible en PyTorch sin necesidad de técnicas para lograr──

### Pmap: Paralelo de datos a través de dispositivos

```python
parallel_step = jax.pmap(train_step, axis_name='devices')
```

`pmap`Replica la función en todos los dispositivos disponibles (GPU/TPU) y divide el lote.`jax.lax.pmean`y `jax.lax.psum`sincronizar los gradientes entre los dispositivos.

> `pmap`La función se replica en todos los dispositivos disponibles (GPU/TPU) y se separa en la cantidad de unidades.`jax.lax.pmean`Y `jax.lax.psum`跨设备同步梯度──

Google entrena a Gemini a través de miles de chips TPU v5e usando `pmap`(y su sucesor)`shard_map`El modelo de programación: escribir la versión de un solo dispositivo, envuelto con `pmap`- Ya lo he hecho.

> Google utiliza `pmap`(y sus sucesores)`shard_map`) en mil bloques de TPU v5e  芯片上训练 Gemini──编程模型:写单设备版本,用 `pmap`包装,完成──

### La estructura de datos universal.

JAX opera en "pytrees" - combinaciones anidadas de listas, tuples, dicts y matrices.

> JAX 操作"pytree"列表、元组、字典和数组的嵌套组合──tu parámetro de modelo es un pytree:

```python
params = {
    'layer1': {'w': jnp.zeros((784, 256)), 'b': jnp.zeros(256)},
    'layer2': {'w': jnp.zeros((256, 128)), 'b': jnp.zeros(128)},
    'layer3': {'w': jnp.zeros((128, 10)),  'b': jnp.zeros(10)},
}
```

Cada transformación de JAX ...`grad`¿ Qué ?`jit`¿ Qué ?`vmap`- sabe cómo cruzar los pytrees.`jax.tree.map(f, tree)`se aplica `f`Así es como los optimizadores actualizan todos los parámetros a la vez:

> Cada JAX cambia`grad`¿Qué es esto?`jit`¿Qué es esto?`vmap`Todo el mundo sabe cómo atravesar el árbol.`jax.tree.map(f, tree)`¿ Qué ?`f` aplicado a cada hoja.

```python
params = jax.tree.map(lambda p, g: p - lr * g, params, grads)
```

No , no .`.parameters()`No hay registro de parámetros. La estructura del árbol es el modelo.

> No hay .`.parameters()`方法──没有参数注册──树结构就是模型──

### Funcional vs. orientado a objetos

Las tiendas PyTorch indican dentro de los objetos:

```python
class Model(nn.Module):
    def __init__(self):
        self.linear = nn.Linear(784, 10)

    def forward(self, x):
        return self.linear(x)
```

JAX utiliza funciones puras con estado explícito:

```python
def predict(params, x):
    return jnp.dot(x, params['w']) + params['b']
```

Los parámetros se transmiten. Nada se almacena. Nada se muta. Esto hace que cada función sea verificable, composible y compilable. También significa que gestiones los parámetros tú mismo - o utilizas una biblioteca como Flax o Equinox.

> 参数被传输──不存储任何东西──不修改任何东西── esto hace que cada función pueda ser probada、组合、编译── esto también significa que necesitas manejar por ti mismo los parámetros o usar Flax o Equinox etc.

### El ecosistema JAX.

JAX te da primitivos, las bibliotecas te dan ergonomía.

> JAX 提供原语──库提供便利性:

| Library | Role | Style |
|---------|------|-------|
| **Flax** (Google) | Neural network layers | `nn.Module` with explicit state |
| **Equinox** (Patrick Kidger) | Neural network layers | Pytree-based, Pythonic |
| **Optax** (DeepMind) | Optimizers + LR schedules | Composable gradient transforms |
| **Orbax** (Google) | Checkpointing | Save/restore pytrees |
| **CLU** (Google) | Metrics + logging | Training loop utilities |

Optax es la biblioteca de optimización estándar. Se separa la transformación de gradiente (Adam, SGD, recorte) de la actualización de parámetros, por lo que es trivial componer:

> Optax es un estándar de optimización. Se puede cambiar de grado (Adam, SGD, corte) y de nuevo separarse de los parámetros, haciendo que la combinación sea más fácil de mover:

```python
optimizer = optax.chain(
    optax.clip_by_global_norm(1.0),
    optax.adam(learning_rate=1e-3),
)
```

### ¿Cuándo usar JAX vs PyTorch?

| Factor | JAX | PyTorch |
|--------|-----|---------|
| TPU support | First-class (Google built both) | Community-maintained (torch_xla) |
| GPU support | Good (CUDA via XLA) | Best-in-class (native CUDA) |
| Debugging | Hard (tracing + compilation) | Easy (eager, line-by-line) |
| Ecosystem | Research-focused (Flax, Equinox) | Massive (HuggingFace, torchvision, etc.) |
| Hiring | Niche (Google/DeepMind/Anthropic) | Mainstream (everywhere) |
| Large-scale training | Superior (XLA, pmap, mesh) | Good (FSDP, DeepSpeed) |
| Prototyping speed | Slower (functional overhead) | Faster (mutate and go) |
| Production inference | TensorFlow Serving, Vertex AI | TorchServe, Triton, ONNX |
| Who uses it | DeepMind (Gemini), Anthropic (Claude) | Meta (Llama), OpenAI (GPT), Stability AI |

La respuesta honesta: usar PyTorch a menos que tengas una razón específica para usar JAX. Esas razones son: acceso a TPU, necesidad de gradientes por ejemplo, capacitación multi-dispositivo a gran escala, o trabajar en Google/DeepMind/Anthropic.

> Respuesta: A menos que haya una razón específica, entonces utilizar PyTorch. Estas razones son: TPU 访问、需要逐样本梯度、大规模多设备训练,或在 Google/DeepMind/Anthropic 工作──

### Números aleatorios en JAX Número aleatorio en JAX

JAX no tiene un estado aleatorio global.

> JAX  no tiene un estado de comprobación completo. Cada operación necesita una clave PRNG clara:

```python
key = jax.random.PRNGKey(42)
key1, key2 = jax.random.split(key)
w = jax.random.normal(key1, shape=(784, 256))
```

Esto es molesto al principio, pero garantiza la reproducibilidad entre dispositivos y compilaciones, una propiedad que PyTorch es`torch.manual_seed`no puede garantizar en configuraciones de múltiples GPU.

> Una vez que comenzó muy difícil. Pero garantiza la capacidad de composición de los equipos y la compilación.`torch.manual_seed`En muchos entornos de GPU no se puede asegurar.
```figure
batchnorm-effect
```

## Construye el mismo

## Construye y realiza.

> **【中文解读】**Con JAX + Optax  entrenar MNIST 分类器──注意和 PyTorch 关键区别:没有 nn.Module、参数用嵌套字典(pytree) almacenamiento、 entrenamiento pasos es pura función con @jax.jit 编译、没有 .zero_grad() /.backward() /.step() 梯度计算和参数更新合并在一个函数中──

### Paso 1: Configuración y datos. Paso 1: Configuración y datos.

Entrenaremos una MLP de 3 capas en el MNIST usando JAX y Optax. 784 entradas, dos capas ocultas de 256 y 128 neuronas, 10 clases de salida.

> Usaremos JAX y Optax en el MNIST para entrenar una MLP de 3 niveles. 784 entradas, dos 256 y 128 entradas ocultas de los nervios, 10 categorías de salida.

```python
import jax
import jax.numpy as jnp
from jax import random
import optax

def get_mnist_data():
    from sklearn.datasets import fetch_openml
    mnist = fetch_openml('mnist_784', version=1, as_frame=False, parser='auto')
    X = mnist.data.astype('float32') / 255.0
    y = mnist.target.astype('int')
    X_train, X_test = X[:60000], X[60000:]
    y_train, y_test = y[:60000], y[60000:]
    return X_train, y_train, X_test, y_test
```

### Paso 2: Inicializa los parámetros. Paso 2: Inicializa los parámetros.

No hay clase, sólo una función que devuelve un pytree:

> 没有类──只是一个返回 pytree 的函数:

```python
def init_params(key):
    k1, k2, k3 = random.split(key, 3)
    scale1 = jnp.sqrt(2.0 / 784)
    scale2 = jnp.sqrt(2.0 / 256)
    scale3 = jnp.sqrt(2.0 / 128)
    params = {
        'layer1': {
            'w': scale1 * random.normal(k1, (784, 256)),
            'b': jnp.zeros(256),
        },
        'layer2': {
            'w': scale2 * random.normal(k2, (256, 128)),
            'b': jnp.zeros(128),
        },
        'layer3': {
            'w': scale3 * random.normal(k3, (128, 10)),
            'b': jnp.zeros(10),
        },
    }
    return params
```

El inicio de tres claves PRNG separadas de una semilla, cada peso es una matriz inmutable en un dictado anidado.

> Manual completado de He iniciósio── tres PRNG clave de una semilla dividida para venir── cada peso son un número invariable en el ensamblaje de la escritura──

### Paso 3: Pasado hacia adelante.

```python
def forward(params, x):
    x = jnp.dot(x, params['layer1']['w']) + params['layer1']['b']
    x = jax.nn.relu(x)
    x = jnp.dot(x, params['layer2']['w']) + params['layer2']['b']
    x = jax.nn.relu(x)
    x = jnp.dot(x, params['layer3']['w']) + params['layer3']['b']
    return x

def loss_fn(params, x, y):
    logits = forward(params, x)
    one_hot = jax.nn.one_hot(y, 10)
    return -jnp.mean(jnp.sum(jax.nn.log_softmax(logits) * one_hot, axis=-1))
```

Funciones puras, parámetros, predicción fuera.`self`, no se almacena estado. `loss_fn`computa la entropía cruzada desde cero -- softmax, log, media negativa.

> 纯函数──参数进,预测出──没有 `self`, no hay estado de almacenamiento.`loss_fn`Desde la primera calculación hasta la segunda, el valor de la media negativa es de

### Paso 4: Paso de entrenamiento compilado JIT.

```python
@jax.jit
def train_step(params, opt_state, x, y):
    loss, grads = jax.value_and_grad(loss_fn)(params, x, y)
    updates, opt_state = optimizer.update(grads, opt_state, params)
    params = optax.apply_updates(params, updates)
    return params, opt_state, loss

@jax.jit
def accuracy(params, x, y):
    logits = forward(params, x)
    preds = jnp.argmax(logits, axis=-1)
    return jnp.mean(preds == y)
```

`jax.value_and_grad`El valor de pérdida y los gradientes se devuelven en un solo paso.`@jax.jit`El decorador compila ambas funciones a XLA. Después de la primera llamada, cada paso de entrenamiento se ejecuta sin tocar Python.

> `jax.value_and_grad`En una transmisión simultánea, regresar a la pérdida de valor y de gradiente.`@jax.jit`El dispositivo de decoración compondrá dos funciones en XLA. Después de su primera utilización, cada paso de entrenamiento dejará de tocar Python.

### Paso 5: Ciclo de entrenamiento.

```python
optimizer = optax.adam(learning_rate=1e-3)

X_train, y_train, X_test, y_test = get_mnist_data()
X_train, X_test = jnp.array(X_train), jnp.array(X_test)
y_train, y_test = jnp.array(y_train), jnp.array(y_test)

key = random.PRNGKey(0)
params = init_params(key)
opt_state = optimizer.init(params)

batch_size = 128
n_epochs = 10

for epoch in range(n_epochs):
    key, subkey = random.split(key)
    perm = random.permutation(subkey, len(X_train))
    X_shuffled = X_train[perm]
    y_shuffled = y_train[perm]

    epoch_loss = 0.0
    n_batches = len(X_train) // batch_size
    for i in range(n_batches):
        start = i * batch_size
        xb = X_shuffled[start:start + batch_size]
        yb = y_shuffled[start:start + batch_size]
        params, opt_state, loss = train_step(params, opt_state, xb, yb)
        epoch_loss += loss

    train_acc = accuracy(params, X_train[:5000], y_train[:5000])
    test_acc = accuracy(params, X_test, y_test)
    print(f"Epoch {epoch + 1:2d} | Loss: {epoch_loss / n_batches:.4f} | "
          f"Train Acc: {train_acc:.4f} | Test Acc: {test_acc:.4f}")
```

10 épocas. ~ 97 por ciento de precisión de prueba. La primera era es lenta (compilación JIT).

> 10 个时代──~97% 测试准确率──第一个时代 较慢(JIT 编译)──第 2-10 个时代 很快──

No se puede ver lo que falta .`.zero_grad()`No , no .`.backward()`No , no .`.step()`La actualización completa es una llamada de función compuesta. Los gradientes se calculan, transformados por Adam, y aplicados a los parámetros - todo dentro`train_step`¿ Qué ?

> No hay nada .`.zero_grad()`, no hay `.backward()`, no hay `.step()` Toda la actualización es una combinación de funciones de la función de la escala.`train_step`En completado.

> **【拓展：JAX 的分布式训练】**El mapa de pmap de JAX puede distribuirse automáticamente en varios dispositivos.`jax.pmap(train_step, axis_name='batch')`Se dividirá el lote en 4 partes, cada GPU procesará una, y luego pasará.`jax.lax.pmean`El Pod TPU de Google tiene miles de bloques de chips, la malla de JAX y el shard_map se pueden hacer en miles de dispositivos y seguir adelante.

## Usalo con el marco de ejecución

> **【中文解读】**La base de datos de JAX 生态:Flax(Google de la red de la red nerviosa, similar a nn.Module) √Equinox(más Pythonic de sustitución) √Optax(可组合的优化器库) √Optax de diseño filosofía: Optax de la optimización de los dispositivos es la escala de cambio de la cadena de la combinación √Corte → Adán → 权重衰减, cada paso es un cambio independiente─

### El estándar de Google.

Flax es la biblioteca de red neural JAX más común.`nn.Module`de nuevo, pero con una gestión explícita del estado:

> El lino es el más comúnmente utilizado en JAX.`nn.Module`, pero usando el manejo de estado de la expresión:

```python
import flax.linen as nn

class MLP(nn.Module):
    @nn.compact
    def __call__(self, x):
        x = nn.Dense(256)(x)
        x = nn.relu(x)
        x = nn.Dense(128)(x)
        x = nn.relu(x)
        x = nn.Dense(10)(x)
        return x

model = MLP()
params = model.init(jax.random.PRNGKey(0), jnp.ones((1, 784)))
logits = model.apply(params, x_batch)
```

La misma estructura que PyTorch, pero `params`Se separa del modelo. `model.init()`crea params. `model.apply(params, x)`El objeto modelo no tiene estado.

> 结构与 PyTorch 相同, pero `params`Se separa de los modelos.`model.init()`创建参数──`model.apply(params, x)`运行前向传播──模型对象没有状态──

### Equinox: La alternativa pitónica.

El Equinoccio (de Patrick Kidger) representa los modelos como pytrees:

> Equinox (por Patrick Kidger) 开发)将模型表示为 pytree:

```python
import equinox as eqx

model = eqx.nn.MLP(
    in_size=784, out_size=10, width_size=256, depth=2,
    activation=jax.nn.relu, key=jax.random.PRNGKey(0)
)
logits = model(x)
```

El modelo en sí es un pytree.`.apply()`Los parámetros son sólo las hojas del modelo. Esto es más cerca de cómo piensa JAX.

> El modelo en sí mismo es un árbol.`.apply()`◊ Los parámetros son sólo las hojas del modelo.

### Optax: Optimizadores composibles.

Optax descopla la transformación de gradiente de la actualización:

> Optax 将梯度变换与更新解:

```python
schedule = optax.warmup_cosine_decay_schedule(
    init_value=0.0, peak_value=1e-3,
    warmup_steps=1000, decay_steps=50000
)

optimizer = optax.chain(
    optax.clip_by_global_norm(1.0),
    optax.adamw(learning_rate=schedule, weight_decay=0.01),
)
```

El recorte de gradientes, el aumento de la tasa de aprendizaje, la desintegración del peso, todo compuesto como una cadena de transformaciones. Cada transformación ve los gradientes, los modifica y los pasa al siguiente. No hay clase de optimizador monolitico.

> 梯度剪、学习率预热、权重衰减全部作为变换链组合──每变换看梯度,修改它们,传递给下一个──没有巨大的优化器类──

## Envíe el producto .

**Installation:**

```bash
pip install jax jaxlib optax flax
```

Para soporte de GPU:

```bash
pip install jax[cuda12]
```

Para TPU (nube de Google):

```bash
pip install jax[tpu] -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
```

**Performance gotchas:**

- La primera llamada JIT es lenta (compilación).
- Evite los bucles de Python sobre las matrices JAX dentro de JIT.`jax.lax.scan`o `jax.lax.fori_loop`¿ Qué ?
- `jax.debug.print()`trabaja dentro del JIT.`print()`No lo hace.
- Perfil con `jax.profiler`La compilación XLA puede ocultar cuellos de botella.
- JAX pre-alloca el 75% de la memoria de la GPU por defecto.`XLA_PYTHON_CLIENT_PREALLOCATE=false`para desactivar.

**Checkpointing:**

```python
import orbax.checkpoint as ocp
checkpointer = ocp.PyTreeCheckpointer()
checkpointer.save('/tmp/model', params)
restored = checkpointer.restore('/tmp/model')
```

**This lesson produces:**
- `outputs/prompt-jax-optimizer.md`-- una instrucción para elegir la configuración correcta de JAX optimizador
- `outputs/skill-jax-patterns.md`-- una habilidad que cubre patrones funcionales en JAX

## Los ejercicios.

1. Añadir la falla en el MLP. En JAX, la falla requiere una clave PRNG - enlazar una llave a través del pase hacia adelante y dividirlo por cada capa de falla. Comparar la precisión de la prueba con y sin.

2. Usar`jax.vmap`Para calcular los gradientes por ejemplo para un lote de 32 imágenes MNIST. Compute la norma de gradiente para cada ejemplo. ¿Qué ejemplos tienen los gradientes más grandes, y por qué?

3. Reemplazar la función manual hacia adelante con una genérica `mlp_forward(params, x)`que funciona para cualquier número de capas.`jax.tree.leaves`para determinar la profundidad automáticamente.

4. Marque de referencia el paso de formación con y sin `@jax.jit`¿Cuánto velocidad tiene el hardware? ¿Cuál es el costo de compilación en la primera llamada?

5. Implementar el recorte de gradientes mediante la composición `optax.chain(optax.clip_by_global_norm(1.0), optax.adam(1e-3))`Entrenar con y sin recortes.

## Términos clave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| XLA | "The thing that makes JAX fast" | Accelerated Linear Algebra -- a compiler that fuses operations and generates optimized GPU/TPU kernels from a computation graph |
| JIT | "Just-in-time compilation" | JAX traces the function on first call, compiles to XLA, then runs the compiled version on subsequent calls |
| Pure function | "No side effects" | A function where the output depends only on inputs -- no global state, no mutation, no randomness without explicit keys |
| vmap | "Auto-batching" | Transforms a function that processes one example into one that processes a batch, without rewriting |
| pmap | "Auto-parallelism" | Replicates a function across multiple devices and splits the input batch |
| Pytree | "Nested dict of arrays" | Any nested structure of lists, tuples, dicts, and arrays that JAX can traverse and transform |
| Tracing | "Recording the computation" | JAX executes the function with abstract values to build a computation graph, without computing real results |
| Functional autodiff | "grad of a function" | Computing derivatives by transforming functions, not by attaching gradient storage to tensors |
| Optax | "JAX's optimizer library" | A composable library of gradient transformations -- Adam, SGD, clipping, scheduling -- that chain together |
| Flax | "JAX's nn.Module" | Google's neural network library for JAX, adding layer abstractions while keeping state explicit |

## Más Leer más Leer más

- Documentación JAX: https://jax.readthedocs.io/-- los documentos oficiales, con excelentes tutoriales en graduado, jit, y vmap
  JAX 文档:https://jax.readthedocs.io/官方文档, sobre el curso de grad,jit y vmap
- "JAX: transformaciones composibles de los programas Python+NumPy" (Bradbury et al., 2018) -- el documento original que explica la filosofía del diseño
  Bradbury 等人, JAX:Python+NumPy 程序的可组合变换(2018) 解释设计哲学学的原始论文
- Documentación de lino: https://flax.readthedocs.io/-- la biblioteca de red neuronal de Google para JAX
  Flax 文档 Google para JAX  desarrollo de la red de datos
- Patrick Kidger, "Equinox: redes neuronales en JAX a través de PyTrees llamables y transformaciones filtradas" (2021) -- la alternativa Pythonic al lino
  Patrick Kidger,Equinox: a través de PyTree y over变换实现 JAX 神经网络(2021)Flax de Pythonic 替代方案
- DeepMind, "Optax: transformación y optimización de gradientes composibles" -- la biblioteca de optimización estándar
  Profundo Mente, Optax:                                                                                                                                                                                                                                                          
- "No sabes JAX" (Colin Raffel, 2020) - una guía práctica de las gotchas y patrones de JAX, de uno de los autores de T5
  Colin Raffel,you still don't understand JAX(2020)JAX 陷和模式的实用指南, autor para T5 论文作者之一
