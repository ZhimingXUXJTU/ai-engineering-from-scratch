# Introdução ao JAX JAX Entrada

> PyTorch muda tensores, TensorFlow cria gráficos, JAX compilou funções puras, e a última altera a forma como pensamos sobre aprendizagem profunda.

> **【中文解读】**PyTorch 可变张量,TensorFlow 静态图,JAX 编译纯函数──JAX 函数式编程范式是深度学习的新方向Google's Gemini 就用JAX 训练──本章学习JAX 的核心:jit 编译、vmap 向量化、grad 自动微分──

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 03 Lessons 01-10, basic NumPy
**Time:** ~90 minutes

## Objetivos de aprendizagem

- Escreva código de rede neural de função pura usando a API funcional do JAX (jax.numpy, jax.grad, jax.jit, jax.vmap)
- Explique a diferença de design fundamental entre a mutação ansiosa do PyTorch e o modelo de compilação funcional do JAX
- Aplicar compilação jit e vectorização vmap para acelerar os ciclos de treinamento em comparação com Python ingênuo
- Treinar uma rede simples no JAX e contrastar a gestão explícita de estado com a abordagem orientada a objeto do PyTorch

> **【中文解读】**O que é que é o sistema de computador de JAX? Não há nenhum módulo de JAX.

## O problema é o problema da introdução

Sabes como construir redes neurais em PyTorch.`nn.Module`- Não , não .`.backward()`Funciona, milhões de pessoas usam.

> Já sabes como construir uma rede neural no PyTorch.`nn.Module`,调用 `.backward()`Otimizador... pode funcionar... milhões de pessoas usam.

Mas a PyTorch tem uma limitação no seu DNA: ela rastreia as operações ansiosamente, uma por vez, no Python.`tensor + tensor`Cada etapa de treinamento reinterpreta o mesmo código Python. Isto funciona bem até que você precisa treinar um modelo de 540 bilhões de parâmetros em 2.048 TPUs.

> Mas o DNA do PyTorch tem uma limitação: ele executa operações de rastreamento de cada vez com Python.`tensor + tensor`Todo é um único arranque interno. Cada treino reexplica o mesmo código Python. Isso pode funcionar até que o modelo de 5400 bilhões de parâmetros seja treinado.

O Google DeepMind treina Gemini no JAX. O Anthropic treinou Claude no JAX. Não são pequenas operações - são as maiores operações de treinamento de rede neural na Terra. Eles escolheram o JAX porque trata o seu ciclo de treinamento como um programa compilavel, não uma sequência de chamadas Python.

> Google DeepMind usa JAX  treinar Gemini。 Antropic usa JAX  treinar Claude。 Estas não são operações de pequena escala são as maiores operações de treinamento de rede neuronal da Terra。 Eles escolheram JAX porque ele coloca seu ciclo de treinamento como um programa compilável, em vez de uma série de Python 调用。

JAX é NumPy com três superpoderes: diferenciação automática, compilação JIT para XLA e vectorização automática. Você escreve uma função que processa um exemplo. JAX lhe dá uma função que processa um lote, calcula gradientes, compila para código de máquina e executa em vários dispositivos. Tudo sem alterar a função original.

> JAX é um sistema com três supercapacidades numPy: automático, micro e JIT, composto em XLA e automático, dimensionamento. Você escreve uma função de processamento de uma única amostra. JAX lhe dá uma função de processamento de volume, gradiente de cálculo, composto em código de máquina e executado em vários dispositivos. Todas estas funções não precisam mudar a função original.

> **【中文解读】**Limitações de PyTorch: cada treinamento reexplica o código Python, cada tensor 运算 são kernel único 启动── em 2048 blocos TPU 上训练 540B 参数模型时,这个开销不可接受──JAX Colocar o ciclo de treinamento em código de máquina, saltar Python 层, executar diretamente no acelerador──

> **【拓展：JAX 的工业应用】**Google DeepMind usa JAX  treinar Gemini(máxima versão segundo a lenda superior a 1T 参数)。Antropic usa JAX  treinar Claude 系列。Google's AlphaFold 2/3 também usa JAX。JAX's vantagem em treinamento distribuído em super-massas: usa pmap em mil blocos de TPU, faz auto-curso, usa shard_map fazer modelo ecurso。 mas a dificuldade de ajuste do JAX é muito maior do que a PyTorch。

## O conceito central.

### A filosofia do JAX.

O JAX é um quadro funcional, sem classes, sem estados mutáveis, sem`.backward()`- Em vez disso:

> JAX é um quadro de funções.`.backward()`方法──取而代之 é:

| PyTorch | JAX |
|---------|-----|
| `nn.Module` class with state | Pure function: `f(params, x) -> y` |
| `loss.backward()` | `jax.grad(loss_fn)(params, x, y)` |
| Eager execution | JIT compilation via XLA |
| `for x in batch:` manual loop | `jax.vmap(f)` auto-vectorization |
| `DataParallel` / `FSDP` | `jax.pmap(f)` auto-parallelism |
| Mutable `model.parameters()` | Immutable pytree of arrays |

Esta não é uma preferência de estilo. É uma restrição de compilador. A compilação JIT requer funções puras - as mesmas entradas sempre produzem as mesmas saídas, sem efeitos colaterais. Essa restrição é o que torna possível 100x velocidades.

> Não é um preconceito de estilo. É um composto de compiladores.

> Não é um preconceito de estilo. É um composto de compiladores.

### O conhecido de superfície.

A JAX reimplementa a API NumPy em aceleradores:

```python
import jax.numpy as jnp

a = jnp.array([1.0, 2.0, 3.0])
b = jnp.array([4.0, 5.0, 6.0])
c = jnp.dot(a, b)
```

Os mesmos nomes de funções, as mesmas regras de transmissão, a mesma semântica de corte, mas as matriz estão em GPU/TPU, e cada operação é rastreável pelo compilador.

> Identidade de funções. Identidade de regras de difusão. Identidade de pedaços de texto.

Uma diferença crítica: as matrizes JAX são imutáveis.`a[0] = 5`Em vez disso:`a = a.at[0].set(5)`Isto parece estranho durante uma semana, e depois clique... a imutabilidade é o que faz as transformações como`grad`- Não .`jit`, e `vmap`- Compostabilidade.

> Uma diferença importante: o número de JAX é imutável.`a[0] = 5`- Não, não.`a = a.at[0].set(5)`Primeiro, vai sentir-se diferente, depois, vai perceber que é impossível mudar.`grad`- Não.`jit`和 `vmap`等变换可组合的基础――

### Jax.grad: Funcional Autodiff. jax.grad: função em forma automática

A PyTorch liga gradientes a tensores (`.grad`O JAX liga gradientes às funções.

> PyTorch vai aumentar a escala para a quantidade de`.grad`)―JAX vai aumentar a gradiência para a função―

```python
import jax

def f(x):
    return x ** 2

df = jax.grad(f)
df(3.0)
```

`jax.grad`O valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de um valor de valor de um valor de um valor de um valor de valor de um valor de um valor de valor de um valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de valor de`.backward()`Não há gráfico de cálculo armazenado em tensores. O gradiente é apenas outra função que você pode chamar, compor ou compilar JIT.

> `jax.grad`Receber uma função, retornar uma nova função de um cálculo ∞.`.backward()`调用──张量上不存储计算图──梯度只是另一个你可以调用、组合或JIT 编译的函数──

Isto compõe-se arbitrariamente:

> Pode ser combinado:

```python
d2f = jax.grad(jax.grad(f))
d2f(3.0)
```

Segundo derivativos, terceiro derivativos, jacobianos, hessianos, tudo por composição.`grad`PyTorch também pode fazer isto (`torch.autograd.functional.hessian`No JAX, é a base.

> Segundo o número de números.`grad`实现──PyTorch 也能做(`torch.autograd.functional.hessian`Mas é um pouco mais tarde. No JAX, é a base.

A restrição: `grad`Não há declarações impressas dentro (executa-las durante o rastreamento, não executam). Não há mutação do estado externo. Não há geração de números aleatórios sem gerenciamento de chaves explícito.

> 限制:`grad`Apenas aplicável a funções puras. Não pode ser impresso em seu interior. Não pode ser editado em seu estado externo.

> **【拓展：JAX 的 grad vs PyTorch 的 autograd】**PyTorch Colocar a gradiência existente tensor 上(x.grad),JAX Colocar a gradiência de observação de função de saída── Isto significa JAX 天然支持高阶导数(grad((((f))), enquanto PyTorch 需要特殊处理──`jax.hessian(f)`,PyTorch 需要 `torch.autograd.functional.hessian`- Não.

### Compile para XLA

```python
@jax.jit
def train_step(params, x, y):
    loss = loss_fn(params, x, y)
    return loss

fast_step = jax.jit(train_step)
```

Na primeira chamada, o JAX rastreia a função - registra quais operações acontecem, sem executá-las. Depois entrega esse rastro para o XLA (Algebra Linear Acelerada), o compilador do Google para TPUs e GPUs. O XLA funde operações, elimina cópias redundantes de memória e gera código de máquina otimizado.

> Durante a primeira utilização, a função de rastreamento do JAX registra quais operações ocorreram, e não são executadas na prática.

As chamadas subsequentes ignoram Python inteiramente. O código compilado é executado no acelerador à velocidade de C ++.

> 后续调用完全跳过Python──编译后的代码运行在加速器上以C++ 速度──

Quando o JIT ajuda:

> JIT tem uma cena útil:

- Passo de treinamento (a mesma computação repetida milhares de vezes)
  Tradução do inglês: training steps (também calculado)
- Inferência (mesmo modelo, entradas diferentes)
  Tradução do inglês:
- Qualquer função chamada mais de uma vez com entradas de forma semelhante
  Tradução em chinês: qualquer função em forma semelhante

Quando a JIT dói:

> JIT tem cenários prejudiciais:

- Funções com fluxo de controlo Python que dependem de valores (`if x > 0`onde x é uma matriz rastreada)
  中文翻译:包含依赖值的Python 控制流的函数(`if x > 0`Dentre eles x é o número de pessoas que estão sendo rastreadas)
- Computações de um só momento (compilação superior a tempo de execução)
  Tradução do inglês:一次性计算 (一次性计算)
- Debugging (tracing oculta a execução real)
  Tradução em inglês: 调试 (→ "seguida ocultação concreta")

A restrição de fluxo de controlo é real. `jax.lax.cond`Substitui`if/else`- Não .`jax.lax.scan`Substitui`for`Não são opcionais, são o preço da compilação.

> O controle de fluxo é real.`jax.lax.cond`替代   substituir`if/else`- Não.`jax.lax.scan`替代   substituir`for`循环── estes não são opcionais são o preço da composição

### Vmap: Vectorização Automática

Você escreve uma função que processa um exemplo:

> Você escreveu uma função de tratamento de um único modelo:

```python
def predict(params, x):
    return jnp.dot(params['w'], x) + params['b']
```

`vmap`Levanta-o para processar um lote:

```python
batch_predict = jax.vmap(predict, in_axes=(None, 0))
```

`in_axes=(None, 0)`Mecanismo: não se recolectar em lote `params`(compartilhado), lote sobre o eixo 0 de `x`Não há manual .`for`Não há remodelação, não há threading de dimensão de lote, o JAX calcula a dimensão de lote e vectoriza toda a computação.

> `in_axes=(None, 0)`Indicações:`params`进行批处理(共享),对 `x`O processo de produção de produtos de base é realizado em série.`for`循环──无需重塑──无需手动传递批量维度──JAX Automatically find out批量维度并向量化整个计算──

Não é açúcar sintáctico.`vmap`gera código vectorizado fundido que corre 10-100 vezes mais rápido do que um ciclo Python.`jit`E ...`grad`- Não .

> Não é um açúcar.`vmap`O código de convergência de métricas, em Python, é 10-100 vezes mais rápido que o Python.`jit`和 `grad`组合:

```python
per_example_grads = jax.vmap(jax.grad(loss_fn), in_axes=(None, 0, 0))
```

É quase impossível em PyTorch sem hacks.

> 逐样本梯度──一行代码── é quase impossível não usar técnicas para realizar isso em PyTorch.

### pmap: Paralelismo de dados em dispositivos

```python
parallel_step = jax.pmap(train_step, axis_name='devices')
```

`pmap`Replica a função em todos os dispositivos disponíveis (GPUs/TPUs) e divide o lote.`jax.lax.pmean`E ...`jax.lax.psum`Sincronizar gradientes entre dispositivos.

> `pmap`A função será copiada em todos os dispositivos disponíveis (GPU/TPU) e distribuída em lote.`jax.lax.pmean`和 `jax.lax.psum`跨设备同步梯度──

O Google treina os Gémeos através de milhares de chips TPU v5e usando `pmap`(e seu sucessor `shard_map`O modelo de programação: escrever a versão de um único dispositivo, encerrar com `pmap`- Já está.

> Google utiliza `pmap`(e seus sucessores)`shard_map`) em mil blocos de TPU v5e                                                                                                                                                                                                                                                          `pmap`- Embalagem, completa.

### A estrutura de dados universal.

O JAX opera em "pytrees" - combinações aninhadas de listas, tuples, dicts e matrizes.

> JAX 操作"pytree"列表、元组、字典和数组的嵌套组合── seu modelo é um pytree:

```python
params = {
    'layer1': {'w': jnp.zeros((784, 256)), 'b': jnp.zeros(256)},
    'layer2': {'w': jnp.zeros((256, 128)), 'b': jnp.zeros(128)},
    'layer3': {'w': jnp.zeros((128, 10)),  'b': jnp.zeros(10)},
}
```

Cada transformação do JAX ...`grad`- Não .`jit`- Não .`vmap`- Sabe atravessar os pytrees.`jax.tree.map(f, tree)`aplica-se `f`É assim que os optimizadores atualizam todos os parâmetros de uma só vez:

> Cada JAX muda`grad`- Não.`jit`- Não.`vmap`Todos sabem como atravessar o árvore.`jax.tree.map(f, tree)`- Não .`f` aplicado a cada folha. É assim que o optimizador renova todos os parâmetros:

```python
params = jax.tree.map(lambda p, g: p - lr * g, params, grads)
```

Não , não .`.parameters()`Não há registro de parâmetros, a estrutura da árvore é o modelo.

> Não há nada .`.parameters()`方法──没有参数注册──树结构就是模型──

### Funcional vs Objeto Orientado

As lojas PyTorch afirmam dentro dos objetos:

```python
class Model(nn.Module):
    def __init__(self):
        self.linear = nn.Linear(784, 10)

    def forward(self, x):
        return self.linear(x)
```

JAX usa funções puras com estado explícito:

```python
def predict(params, x):
    return jnp.dot(x, params['w']) + params['b']
```

Os parâmetros são transmitidos. Nada é armazenado. Nada é mutado. Isso torna todas as funções testáveis, compostaveis e compiláveis. Também significa que você gerencia os parâmetros sozinho - ou usa uma biblioteca como o Flax ou Equinox.

> 参数被传输──不存储任何东西──不修改任何东西──这使每个函数可测试、可组合、可编译──这也意味着你需要自己管理参数或使用 Flax或Equinox等库──

### O ecossistema JAX.

A JAX dá-te primitivos, as bibliotecas dão-te ergonomia.

> JAX 提供原语──库提供便利性:

| Library | Role | Style |
|---------|------|-------|
| **Flax** (Google) | Neural network layers | `nn.Module` with explicit state |
| **Equinox** (Patrick Kidger) | Neural network layers | Pytree-based, Pythonic |
| **Optax** (DeepMind) | Optimizers + LR schedules | Composable gradient transforms |
| **Orbax** (Google) | Checkpointing | Save/restore pytrees |
| **CLU** (Google) | Metrics + logging | Training loop utilities |

O Optax é a biblioteca de otimização padrão. Ele separa a transformação de gradiente (Adam, SGD, clipping) da atualização de parâmetros, tornando trivial compor:

> O optaxe é um sistema de optimização padrão. Ele vai mudar de nível (Adam, SGD, corte) com o parâmetro, tornando a combinação mais fácil de transportar.

```python
optimizer = optax.chain(
    optax.clip_by_global_norm(1.0),
    optax.adam(learning_rate=1e-3),
)
```

### Quando usar JAX vs PyTorch

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

A resposta honesta é: Use PyTorch a menos que tenha uma razão específica para usar JAX. Essas razões são: acesso a TPU, necessidade de gradientes por exemplo, treinamento em vários dispositivos em escala maciça, ou trabalhar no Google/DeepMind/Anthropic.

> 诚实的答案: excepto por uma razão específica, ou usar PyTorch.

### Números aleatórios em JAX Número aleatório em JAX

JAX não tem um estado aleatório global.

> JAX  não tem estado de funcionamento completo. Cada operação precisa de uma chave PRNG:

```python
key = jax.random.PRNGKey(42)
key1, key2 = jax.random.split(key)
w = jax.random.normal(key1, shape=(784, 256))
```

Isto é irritante no início, mas garante reprodução em dispositivos e compilações - uma propriedade que PyTorch é`torch.manual_seed`Não pode garantir em configurações de GPUs múltiplos.

> Primeiro, é muito difícil para os homens. Mas isso garante a reprodutividade de transmissão e composição.`torch.manual_seed`Em muitos GPUs, não há garantias.
```figure
batchnorm-effect
```

## Construí-lo

## Construí-lo e realizei-o.

> **【中文解读】**Utilize JAX + Optax  тренинг MNIST 分类器──注意和 PyTorch 关键区别:没有 nn.Module、参数用嵌套字典(pytree) armazenamento、 тренинг步骤是纯函数用 @jax.jit 编译、没有 .zero_grad() /.backward() /.step() 梯度计算和参数更新合并在一个函数中──

### Passo 1: Configuração e dados. Passo 1: Configuração e dados.

Vamos treinar um MLP de 3 camadas no MNIST usando JAX e Optax. 784 entradas, duas camadas ocultas de 256 e 128 neurônios, 10 classes de saída.

> Vamos usar JAX e Optax no MNIST para treinar uma MLP de 3 níveis, 784 entradas, duas 256 e 128 entradas ocultas, 10 categorias de saída.

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

### Passo 2: Iniciar Parâmetros.

Não há classe, apenas uma função que retorna um pytree:

> Não há classe. Apenas uma função de retorno de um pytree:

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

Três chaves PRNG separadas de uma semente, cada peso é uma matriz imutável num dicto aninhado.

> Manual completado He iniciósio── três PRNG chave de uma semente dividida para vir── cada peso são números invariáveis em um emplaçado de texto──

### Passo 3: Passagem avançada.

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

Funções puras, param dentro, previsão fora.`self`Não há estado de armazenamento.`loss_fn`Computa a entropia cruzada a partir do zero. Softmax, log, média negativa.

> 純函数──参数进,预测出──没有 `self`Não há estado de armazenamento.`loss_fn`Desde o início da calculação, o valor médio negativo é o máximo de suavidade.

### Passo 4: Passo de treinamento compilado JIT.

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

`jax.value_and_grad`Retorna tanto o valor de perda como os gradientes em uma passagem.`@jax.jit`O decorador compila ambas as funções para XLA. Após a primeira chamada, cada etapa de treinamento é executada sem tocar no Python.

> `jax.value_and_grad`Durante uma transmissão, retornar ao mesmo tempo perdas e gradientes.`@jax.jit`O equipamento irá compor duas funções para XLA. Depois da primeira adoção, cada passo de treinamento deixa de tocar Python.

### Passo 5: Ciclo de treinamento.

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

10 épocas. ~ 97% de precisão de teste. A primeira é lenta (compilação JIT).

> 10 个时代──~97% 测试准确率──第一个时代 较慢(JIT 编译)──第 2-10 个时代 很快──

Observe o que falta: não .`.zero_grad()`Não , não .`.backward()`Não , não .`.step()`A atualização completa é uma chamada de função composta. Os gradientes são calculados, transformados por Adam e aplicados a parâmetros - todos dentro.`train_step`- Não .

> Não há nada .`.zero_grad()`Não há nada .`.backward()`Não há nada .`.step()` Toda a actualização é uma função de conjunto de módulos.`train_step`"Não é nada".

> **【拓展：JAX 的分布式训练】**O pmap do JAX pode distribuir automaticamente o treinamento em vários dispositivos.`jax.pmap(train_step, axis_name='batch')`Vou dividir o lote automaticamente em 4 partes, cada GPU processar um, depois passar.`jax.lax.pmean`O Google TPU Pod tem milhares de blocos de chips, uma malha de JAX e um shard_map podem ser fabricados em milhares de dispositivos.

## Use-o com o framework implementado.

> **【中文解读】**O sistema de controle de dados é um sistema de controle de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de

### O Google Standard: A biblioteca de padrões do Google.

O Flax é a biblioteca mais comum da rede neural JAX.`nn.Module`- De volta, mas com gestão explícita do Estado:

> O linho é o mais comum de usar o JAX.`nn.Module`, mas usando o sistema de gestão de estado:

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

A mesma estrutura que a PyTorch, mas...`params`é separado do modelo. `model.init()`cria params. `model.apply(params, x)`O objeto modelo não tem estado.

> 结构与 PyTorch 相同, mas `params`Com o modelo separado.`model.init()`创建参数──`model.apply(params, x)`运行前向传播──模型对象没有状态──

### Equinox: A Alternativa Pitônica.

Equinox (de Patrick Kidger) representa modelos como pytrees:

> Equinox ((por Patrick Kidger 开发)将模型表示为 pytree:

```python
import equinox as eqx

model = eqx.nn.MLP(
    in_size=784, out_size=10, width_size=256, depth=2,
    activation=jax.nn.relu, key=jax.random.PRNGKey(0)
)
logits = model(x)
```

O modelo em si é um pytree.`.apply()`Os parâmetros são apenas as folhas do modelo.

> O modelo em si é uma árvore.`.apply()`◊ O parametro é apenas uma folha do modelo.

### Optax: Otimizadores compostos.

O Optax descopla a transformação de gradiente da atualização:

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

O corte de gradientes, o aquecimento da taxa de aprendizagem, a perda de peso, tudo composto por uma cadeia de transformações. Cada transformação vê os gradientes, os modifica e os passa para o próximo. Não há classe de optimizador monolitico.

> 梯度剪、学习率预热、权重衰减全部作为变换链组合──每个变换看梯度,修改它们,传递给下一个──没有巨大的优化器类──

## Envia-o . Produto .

**Installation:**

```bash
pip install jax jaxlib optax flax
```

Para o suporte de GPU:

```bash
pip install jax[cuda12]
```

Para TPU (Google Cloud):

```bash
pip install jax[tpu] -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
```

**Performance gotchas:**

- A primeira chamada JIT é lenta (compilação).
- Evite os loops Python sobre matrizes JAX dentro do JIT.`jax.lax.scan`ou `jax.lax.fori_loop`- Não .
- `jax.debug.print()`Funciona dentro do JIT.`print()`Não é.
- Profil com `jax.profiler`A compilação XLA pode esconder gargalos de garrafa.
- JAX pré-aloca 75% da memória da GPU por padrão.`XLA_PYTHON_CLIENT_PREALLOCATE=false`para desativar.

**Checkpointing:**

```python
import orbax.checkpoint as ocp
checkpointer = ocp.PyTreeCheckpointer()
checkpointer.save('/tmp/model', params)
restored = checkpointer.restore('/tmp/model')
```

**This lesson produces:**
- `outputs/prompt-jax-optimizer.md`-- um prompt para escolher a configuração certa JAX optimizador
- `outputs/skill-jax-patterns.md`-- uma habilidade que cobre padrões funcionais no JAX

## Exercícios.

1. Adicione o desvio ao MLP. No JAX, o desvio requer uma chave PRNG - enrolar uma chave através do passante para a frente e dividir-a para cada camada de desvio. Compare a precisão do teste com e sem.

2. Utilização`jax.vmap`Para calcular gradientes por exemplo para um lote de 32 imagens MNIST. Calcule a norma de gradiente para cada exemplo. Que exemplos têm os maiores gradientes, e por quê?

3. Substitua a função manual para frente por uma genérica `mlp_forward(params, x)`que funciona para qualquer número de camadas.`jax.tree.leaves`para determinar automaticamente a profundidade.

4. Marque de referência o passo de formação com e sem `@jax.jit`Qual é a velocidade do hardware, qual é a taxa de compilação na primeira chamada?

5. Implementar cortes de gradiente através da composição `optax.chain(optax.clip_by_global_norm(1.0), optax.adam(1e-3))`Treinar com e sem cortar, traçar a norma de gradiente sobre o treino para ver o efeito.

## Termos-chave .

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

## Mais leitura 延伸阅读

- Documentação JAX: https://jax.readthedocs.io/- Os docentes oficiais, com excelentes tutoriais sobre grad, jit e vmap
  JAX 文档:https://jax.readthedocs.io/官方文档,关于grad、jit 和 vmap的优秀教程
- "JAX: transformações compostas de programas Python+NumPy" (Bradbury et al., 2018) -- o artigo original que explica a filosofia de design
  Bradbury 等人, JAX:Python+NumPy 程序的可组合变换(2018) 解释设计哲学学的原始论文
- Documentação de linho: https://flax.readthedocs.io/-- A biblioteca de redes neurais do Google para JAX
  Linha  arquivo  Google para JAX  desenvolvimento
- Patrick Kidger, "Equinox: redes neurais no JAX através de PyTrees chamáveis e transformações filtradas" (2021) -- a alternativa Pythonic ao Linho
  Patrick Kidger,Equinox: através de PyTree e over变换实现 JAX 神经网络(2021)Flax Pythonic 替代方案
- DeepMind, "Optax: transformação e otimização de gradientes compostos" -- a biblioteca padrão de otimização
  DeepMind,Optax:                                                                                                                                                                                                                                                           
- "You Don't Know JAX" (Colin Raffel, 2020) - um guia prático para as gotchas e padrões do JAX, de um dos autores do T5
  Colin Raffel,you still don't understand JAX(2020)JAX 陷和模式的实用指南, autor para T5 论文作者之一
