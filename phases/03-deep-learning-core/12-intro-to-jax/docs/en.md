# Introduction to JAX | JAX 入门

> PyTorch mutates tensors. TensorFlow builds graphs. JAX compiles pure functions. That last one changes how you think about deep learning.

> **【中文解读】** PyTorch 可变张量，TensorFlow 静态图，JAX 编译纯函数。JAX 的函数式编程范式是深度学习的新方向——Google 的 Gemini 就用 JAX 训练。本章学习 JAX 的核心：jit 编译、vmap 向量化、grad 自动微分。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 03 Lessons 01-10, basic NumPy
**Time:** ~90 minutes

## Learning Objectives | 学习目标

- Write pure-function neural network code using JAX's functional API (jax.numpy, jax.grad, jax.jit, jax.vmap)
- Explain the key design difference between PyTorch's eager mutation and JAX's functional compilation model
- Apply jit compilation and vmap vectorization to accelerate training loops compared to naive Python
- Train a simple network in JAX and contrast the explicit state management with PyTorch's object-oriented approach

> **【中文解读】** 本章学习 JAX 的函数式编程范式。与 PyTorch 的核心区别：没有可变状态、没有 .backward()、没有 nn.Module。一切都通过函数变换实现：jax.grad 计算梯度、jax.jit 编译加速、jax.vmap 自动向量化。Google Gemini 和 Anthropic Claude 都用 JAX 训练。

## The Problem | 问题引入

You know how to build neural networks in PyTorch. You define an `nn.Module`, call `.backward()`, step the optimizer. It works. Millions of people use it.

> 你已经知道如何在 PyTorch 中构建神经网络。你定义一个 `nn.Module`，调用 `.backward()`，步进优化器。它能工作。数百万人使用它。

But PyTorch has a constraint baked into its DNA: it traces operations eagerly, one at a time, in Python. Every `tensor + tensor` is a separate kernel launch. Every training step re-interprets the same Python code. This works fine until you need to train a 540-billion-parameter model across 2,048 TPUs. Then the overhead kills you.

> 但 PyTorch 的 DNA 中有一个限制：它逐个急切地追踪操作，用 Python 执行。每次 `tensor + tensor` 都是一次单独的内核启动。每次训练步骤都重新解释相同的 Python 代码。这在需要跨 2,048 个 TPU 训练 5400 亿参数模型之前都能工作。然后开销就会杀死你。

Google DeepMind trains Gemini on JAX. Anthropic trained Claude on JAX. These are not small operations -- they are the largest neural network training runs on Earth. They chose JAX because it treats your training loop as a compilable program, not a sequence of Python calls.

> Google DeepMind 用 JAX 训练 Gemini。Anthropic 用 JAX 训练 Claude。这些不是小规模操作——它们是地球上最大的神经网络训练运行。他们选择 JAX 是因为它把你的训练循环当作可编译的程序，而不是一系列 Python 调用。

JAX is NumPy with three superpowers: automatic differentiation, JIT compilation to XLA, and automatic vectorization. You write a function that processes one example. JAX gives you a function that processes a batch, computes gradients, compiles to machine code, and runs across multiple devices. All without changing the original function.

> JAX 是具有三个超能力的 NumPy：自动微分、JIT 编译到 XLA 和自动向量化。你写一个处理单个样本的函数。JAX 给你一个处理批量、计算梯度、编译为机器码并在多个设备上运行的函数。所有这些都不需要改变原始函数。

> **【中文解读】** PyTorch 的局限：每次训练都重新解释 Python 代码，每个 tensor 运算都是单独的 kernel 启动。在 2048 块 TPU 上训练 540B 参数模型时，这个开销不可接受。JAX 把训练循环编译成机器码，跳过 Python 层，直接在加速器上运行。

> **【拓展：JAX 的工业应用】** Google DeepMind 用 JAX 训练 Gemini（最大版本据传超过 1T 参数）。Anthropic 用 JAX 训练 Claude 系列。Google 的 AlphaFold 2/3 也用 JAX。JAX 的优势在超大规模分布式训练：用 pmap 在数千块 TPU 上自动并行，用 shard_map 做模型并行。但 JAX 的调试难度远高于 PyTorch。

## The Concept | 核心概念

### The JAX Philosophy | JAX 的设计哲学

JAX is a functional framework. No classes, no mutable state, no `.backward()` method. Instead:

> JAX 是一个函数式框架。没有类，没有可变状态，没有 `.backward()` 方法。取而代之的是：

| PyTorch | JAX |
|---------|-----|
| `nn.Module` class with state | Pure function: `f(params, x) -> y` |
| `loss.backward()` | `jax.grad(loss_fn)(params, x, y)` |
| Eager execution | JIT compilation via XLA |
| `for x in batch:` manual loop | `jax.vmap(f)` auto-vectorization |
| `DataParallel` / `FSDP` | `jax.pmap(f)` auto-parallelism |
| Mutable `model.parameters()` | Immutable pytree of arrays |

This is not a style preference. It is a compiler constraint. JIT compilation requires pure functions -- same inputs always produce same outputs, no side effects. That restriction is what makes 100x speedups possible.

> 这不是风格偏好。这是编译器约束。JIT 编译需要纯函数——相同输入总是产生相同输出，没有副作用。这个限制正是 100 倍加速成为可能的原因。

### jax.numpy: The Familiar Surface | jax.numpy：熟悉的接口

JAX reimplements the NumPy API on accelerators:

```python
import jax.numpy as jnp

a = jnp.array([1.0, 2.0, 3.0])
b = jnp.array([4.0, 5.0, 6.0])
c = jnp.dot(a, b)
```

Same function names. Same broadcasting rules. Same slicing semantics. But the arrays live on GPU/TPU, and every operation is traceable by the compiler.

One critical difference: JAX arrays are immutable. No `a[0] = 5`. Instead: `a = a.at[0].set(5)`. This feels awkward for a week, then it clicks -- immutability is what makes transformations like `grad`, `jit`, and `vmap` composable.

### jax.grad: Functional Autodiff | jax.grad：函数式自动微分

PyTorch attaches gradients to tensors (`.grad`). JAX attaches gradients to functions.

```python
import jax

def f(x):
    return x ** 2

df = jax.grad(f)
df(3.0)
```

`jax.grad` takes a function and returns a new function that computes the gradient. No `.backward()` call. No computation graph stored on tensors. The gradient is just another function you can call, compose, or JIT-compile.

This composes arbitrarily:

```python
d2f = jax.grad(jax.grad(f))
d2f(3.0)
```

Second derivatives. Third derivatives. Jacobians. Hessians. All by composing `grad`. PyTorch can do this too (`torch.autograd.functional.hessian`), but it is bolted on. In JAX, it is the foundation.

The constraint: `grad` only works on pure functions. No print statements inside (they run during tracing, not execution). No mutation of external state. No random number generation without explicit key management.

> **【拓展：JAX 的 grad vs PyTorch 的 autograd】** PyTorch 把梯度存在 tensor 上（x.grad），JAX 把梯度看作函数的输出。这意味着 JAX 天然支持高阶导数（grad(grad(f))），而 PyTorch 需要特殊处理。在 JAX 中，计算 Hessian 矩阵只需 `jax.hessian(f)`，PyTorch 需要 `torch.autograd.functional.hessian`。

### jit: Compile to XLA | jit：编译到 XLA

```python
@jax.jit
def train_step(params, x, y):
    loss = loss_fn(params, x, y)
    return loss

fast_step = jax.jit(train_step)
```

On the first call, JAX traces the function -- it records which operations happen, without executing them. Then it hands that trace to XLA (Accelerated Linear Algebra), Google's compiler for TPUs and GPUs. XLA fuses operations, eliminates redundant memory copies, and generates optimized machine code.

Subsequent calls skip Python entirely. The compiled code runs on the accelerator at C++ speed.

When JIT helps:
- Training steps (same computation repeated thousands of times)
- Inference (same model, different inputs)
- Any function called more than once with similar-shaped inputs

When JIT hurts:
- Functions with Python control flow that depends on values (`if x > 0` where x is a traced array)
- One-shot computations (compilation overhead exceeds runtime)
- Debugging (tracing hides the actual execution)

The control flow restriction is real. `jax.lax.cond` replaces `if/else`. `jax.lax.scan` replaces `for` loops. These are not optional -- they are the price of compilation.

### vmap: Automatic Vectorization | vmap：自动向量化

You write a function that processes one example:

```python
def predict(params, x):
    return jnp.dot(params['w'], x) + params['b']
```

`vmap` lifts it to process a batch:

```python
batch_predict = jax.vmap(predict, in_axes=(None, 0))
```

`in_axes=(None, 0)` means: do not batch over `params` (shared), batch over axis 0 of `x`. No manual `for` loop. No reshaping. No batch dimension threading. JAX figures out the batch dimension and vectorizes the entire computation.

This is not syntactic sugar. `vmap` generates fused vectorized code that runs 10-100x faster than a Python loop. And it composes with `jit` and `grad`:

```python
per_example_grads = jax.vmap(jax.grad(loss_fn), in_axes=(None, 0, 0))
```

Per-example gradients. One line. This is nearly impossible in PyTorch without hacks.

### pmap: Data Parallelism Across Devices | pmap：跨设备数据并行

```python
parallel_step = jax.pmap(train_step, axis_name='devices')
```

`pmap` replicates the function across all available devices (GPUs/TPUs) and splits the batch. Inside the function, `jax.lax.pmean` and `jax.lax.psum` synchronize gradients across devices.

Google trains Gemini across thousands of TPU v5e chips using `pmap` (and its successor `shard_map`). The programming model: write the single-device version, wrap with `pmap`, done.

### Pytrees: The Universal Data Structure | Pytrees：通用数据结构

JAX operates on "pytrees" -- nested combinations of lists, tuples, dicts, and arrays. Your model parameters are a pytree:

```python
params = {
    'layer1': {'w': jnp.zeros((784, 256)), 'b': jnp.zeros(256)},
    'layer2': {'w': jnp.zeros((256, 128)), 'b': jnp.zeros(128)},
    'layer3': {'w': jnp.zeros((128, 10)),  'b': jnp.zeros(10)},
}
```

Every JAX transformation -- `grad`, `jit`, `vmap` -- knows how to traverse pytrees. `jax.tree.map(f, tree)` applies `f` to every leaf. This is how optimizers update all parameters at once:

```python
params = jax.tree.map(lambda p, g: p - lr * g, params, grads)
```

No `.parameters()` method. No parameter registration. The tree structure is the model.

### Functional vs Object-Oriented | 函数式 vs 面向对象

PyTorch stores state inside objects:

```python
class Model(nn.Module):
    def __init__(self):
        self.linear = nn.Linear(784, 10)

    def forward(self, x):
        return self.linear(x)
```

JAX uses pure functions with explicit state:

```python
def predict(params, x):
    return jnp.dot(x, params['w']) + params['b']
```

The params are passed in. Nothing is stored. Nothing is mutated. This makes every function testable, composable, and compilable. It also means you manage the params yourself -- or use a library like Flax or Equinox.

### The JAX Ecosystem | JAX 生态系统

JAX gives you primitives. Libraries give you ergonomics:

| Library | Role | Style |
|---------|------|-------|
| **Flax** (Google) | Neural network layers | `nn.Module` with explicit state |
| **Equinox** (Patrick Kidger) | Neural network layers | Pytree-based, Pythonic |
| **Optax** (DeepMind) | Optimizers + LR schedules | Composable gradient transforms |
| **Orbax** (Google) | Checkpointing | Save/restore pytrees |
| **CLU** (Google) | Metrics + logging | Training loop utilities |

Optax is the standard optimizer library. It separates the gradient transformation (Adam, SGD, clipping) from the parameter update, making it trivial to compose:

```python
optimizer = optax.chain(
    optax.clip_by_global_norm(1.0),
    optax.adam(learning_rate=1e-3),
)
```

### When to Use JAX vs PyTorch | 何时用 JAX vs PyTorch

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

The honest answer: use PyTorch unless you have a specific reason to use JAX. Those reasons are -- TPU access, need for per-example gradients, multi-device training at massive scale, or working at Google/DeepMind/Anthropic.

### Random Numbers in JAX | JAX 中的随机数

JAX does not have a global random state. Every random operation requires an explicit PRNG key:

```python
key = jax.random.PRNGKey(42)
key1, key2 = jax.random.split(key)
w = jax.random.normal(key1, shape=(784, 256))
```

This is annoying at first. But it guarantees reproducibility across devices and compilations -- a property that PyTorch's `torch.manual_seed` cannot guarantee in multi-GPU settings.

## Build It | 动手实现

> **【中文解读】** 用 JAX + Optax 训练 MNIST 分类器。注意和 PyTorch 的关键区别：没有 nn.Module、参数用嵌套字典（pytree）存储、训练步骤是纯函数用 @jax.jit 编译、没有 .zero_grad()/.backward()/.step()——梯度计算和参数更新合并在一个函数中。

### Step 1: Setup and Data | 第一步：设置与数据

We will train a 3-layer MLP on MNIST using JAX and Optax. 784 inputs, two hidden layers of 256 and 128 neurons, 10 output classes.

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

### Step 2: Initialize Parameters | 第二步：初始化参数

No class. Just a function that returns a pytree:

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

He-initialization, done manually. Three PRNG keys split from one seed. Every weight is an immutable array in a nested dict.

### Step 3: Forward Pass | 第三步：前向传播

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

Pure functions. Params in, prediction out. No `self`, no stored state. `loss_fn` computes cross-entropy from scratch -- softmax, log, negative mean.

### Step 4: JIT-Compiled Training Step | 第四步：JIT 编译的训练步骤

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

`jax.value_and_grad` returns both the loss value and the gradients in one pass. The `@jax.jit` decorator compiles both functions to XLA. After the first call, each training step runs without touching Python.

### Step 5: Training Loop | 第五步：训练循环

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

10 epochs. ~97% test accuracy. The first epoch is slow (JIT compilation). Epochs 2-10 are fast.

Notice what is missing: no `.zero_grad()`, no `.backward()`, no `.step()`. The entire update is one composed function call. Gradients are computed, transformed by Adam, and applied to parameters -- all inside `train_step`.

> **【拓展：JAX 的分布式训练】** JAX 的 pmap 可以自动将训练分布到多设备。在 4 块 GPU 上训练：`jax.pmap(train_step, axis_name='batch')` 将 batch 自动分成 4 份，每块 GPU 处理一份，然后通过 `jax.lax.pmean` 同步梯度。Google 的 TPU Pod 有数千块芯片，JAX 的 mesh 和 shard_map 可以在数千设备上做模型并行——这是 Gemini 能训练到 1T+ 参数的关键基础设施。

## Use It | 用框架实现

> **【中文解读】** JAX 生态的核心库：Flax（Google 的神经网络层库，类似 nn.Module）、Equinox（更 Pythonic 的替代）、Optax（可组合的优化器库）。Optax 的设计哲学：优化器是梯度变换的链式组合——裁剪 → Adam → 权重衰减，每一步都是独立的变换。

### Flax: The Google Standard | Flax：Google 的标准库

Flax is the most common JAX neural network library. It adds `nn.Module` back, but with explicit state management:

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

Same structure as PyTorch, but `params` is separate from the model. `model.init()` creates params. `model.apply(params, x)` runs the forward pass. The model object has no state.

### Equinox: The Pythonic Alternative | Equinox：Pythonic 替代方案

Equinox (by Patrick Kidger) represents models as pytrees:

```python
import equinox as eqx

model = eqx.nn.MLP(
    in_size=784, out_size=10, width_size=256, depth=2,
    activation=jax.nn.relu, key=jax.random.PRNGKey(0)
)
logits = model(x)
```

The model itself is a pytree. No `.apply()` needed. Parameters are just the model's leaves. This is closer to how JAX thinks.

### Optax: Composable Optimizers | Optax：可组合优化器

Optax decouples the gradient transformation from the update:

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

Gradient clipping, learning rate warmup, weight decay -- all composed as a chain of transforms. Each transform sees the gradients, modifies them, and passes them to the next. No monolithic optimizer class.

## Ship It | 产出物

**Installation:**

```bash
pip install jax jaxlib optax flax
```

For GPU support:

```bash
pip install jax[cuda12]
```

For TPU (Google Cloud):

```bash
pip install jax[tpu] -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
```

**Performance gotchas:**

- First JIT call is slow (compilation). Warm up before benchmarking.
- Avoid Python loops over JAX arrays inside JIT. Use `jax.lax.scan` or `jax.lax.fori_loop`.
- `jax.debug.print()` works inside JIT. Regular `print()` does not.
- Profile with `jax.profiler` or TensorBoard. XLA compilation can hide bottlenecks.
- JAX pre-allocates 75% of GPU memory by default. Set `XLA_PYTHON_CLIENT_PREALLOCATE=false` to disable.

**Checkpointing:**

```python
import orbax.checkpoint as ocp
checkpointer = ocp.PyTreeCheckpointer()
checkpointer.save('/tmp/model', params)
restored = checkpointer.restore('/tmp/model')
```

**This lesson produces:**
- `outputs/prompt-jax-optimizer.md` -- a prompt for choosing the right JAX optimizer configuration
- `outputs/skill-jax-patterns.md` -- a skill covering functional patterns in JAX

## Exercises | 练习题

1. Add dropout to the MLP. In JAX, dropout requires a PRNG key -- thread a key through the forward pass and split it for each dropout layer. Compare test accuracy with and without.

2. Use `jax.vmap` to compute per-example gradients for a batch of 32 MNIST images. Compute the gradient norm for each example. Which examples have the largest gradients, and why?

3. Replace the manual forward function with a generic `mlp_forward(params, x)` that works for any number of layers. Use `jax.tree.leaves` to determine the depth automatically.

4. Benchmark the training step with and without `@jax.jit`. Time 100 steps of each. How large is the speedup on your hardware? What is the compilation overhead on the first call?

5. Implement gradient clipping by composing `optax.chain(optax.clip_by_global_norm(1.0), optax.adam(1e-3))`. Train with and without clipping. Plot the gradient norm over training to see the effect.

## Key Terms | 术语速查表

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

## Further Reading | 延伸阅读

- JAX documentation: https://jax.readthedocs.io/ -- the official docs, with excellent tutorials on grad, jit, and vmap
- "JAX: composable transformations of Python+NumPy programs" (Bradbury et al., 2018) -- the original paper explaining the design philosophy
- Flax documentation: https://flax.readthedocs.io/ -- Google's neural network library for JAX
- Patrick Kidger, "Equinox: neural networks in JAX via callable PyTrees and filtered transformations" (2021) -- the Pythonic alternative to Flax
- DeepMind, "Optax: composable gradient transformation and optimisation" -- the standard optimizer library
- "You Don't Know JAX" (Colin Raffel, 2020) -- a practical guide to JAX gotchas and patterns, from one of the T5 authors
