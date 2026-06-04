# JAX 入门

> PyTorch 可变张量，TensorFlow 构建图，JAX 编译纯函数。最后一种改变了你对深度学习的思考方式。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 03 第 01-10 课、基础 NumPy
**预计时间：** ~90 分钟

## 学习目标

- 使用 JAX 函数式 API（jax.numpy、jax.grad、jax.jit、jax.vmap）编写纯函数神经网络代码
- 解释 PyTorch 的 eager mutation 和 JAX 函数式编译模型之间的关键设计差异
- 应用 jit 编译和 vmap 向量化加速训练循环
- 在 JAX 中训练简单网络，对比显式状态管理与 PyTorch 面向对象方法

## 问题引入

PyTorch 有一个约束：它逐个追踪操作，在 Python 中即时执行。每次 `tensor + tensor` 都是单独的内核启动。这在 2048 块 TPU 上训练 540B 参数模型时开销不可接受。

Google DeepMind 用 JAX 训练 Gemini。Anthropic 用 JAX 训练 Claude。它们选择 JAX 因为它把训练循环当作可编译的程序，而非 Python 调用序列。

JAX 是带三个超能力的 NumPy：自动微分、JIT 编译到 XLA 和自动向量化。

## 核心概念

### JAX 的设计哲学

| PyTorch | JAX |
|---------|-----|
| `nn.Module` 带状态 | 纯函数：`f(params, x) -> y` |
| `loss.backward()` | `jax.grad(loss_fn)(params, x, y)` |
| 即时执行 | 通过 XLA 的 JIT 编译 |
| 手动循环 | `jax.vmap(f)` 自动向量化 |
| `DataParallel` / `FSDP` | `jax.pmap(f)` 自动并行 |
| 可变 `model.parameters()` | 不可变 pytree 数组 |

### jax.numpy

JAX 在加速器上重新实现 NumPy API。函数名相同，广播规则相同，切片语义相同。但数组在 GPU/TPU 上，每个操作都可被编译器追踪。

关键区别：JAX 数组不可变。不能 `a[0] = 5`，而是 `a = a.at[0].set(5)`。

### jax.grad：函数式自动微分

PyTorch 将梯度附加到张量（`.grad`）。JAX 将梯度附加到函数。

```python
df = jax.grad(f)   # grad 接收函数，返回新函数
df(3.0)            # 计算梯度

d2f = jax.grad(jax.grad(f))  # 二阶导数
```

可任意组合。二阶导、三阶导、Jacobian、Hessian——通过组合 `grad` 实现。

### jit：编译到 XLA

```python
@jax.jit
def train_step(params, opt_state, x, y):
    loss, grads = jax.value_and_grad(loss_fn)(params, x, y)
    updates, opt_state = optimizer.update(grads, opt_state, params)
    params = optax.apply_updates(params, updates)
    return params, opt_state, loss
```

首次调用时 JAX 追踪函数，然后交给 XLA 编译器。后续调用跳过 Python，编译后的代码在加速器上以 C++ 速度运行。

### vmap：自动向量化

```python
batch_predict = jax.vmap(predict, in_axes=(None, 0))
```

`in_axes=(None, 0)` 表示：params 不分批（共享），x 按轴 0 分批。不需要手动循环、不需要 reshape。JAX 自动处理批量维度。

### Pytrees

JAX 操作"pytrees"——列表、元组、字典和数组的嵌套组合。模型参数就是 pytree。`jax.tree.map(f, tree)` 将 f 应用于每个叶子。

```python
params = jax.tree.map(lambda p, g: p - lr * g, params, grads)
```

### 何时用 JAX vs PyTorch

诚实回答：除非有特定原因，否则用 PyTorch。那些原因是：TPU 访问、需要逐样本梯度、大规模多设备训练，或在 Google/DeepMind/Anthropic 工作。

## 动手实现

用 JAX + Optax 训练 MNIST 分类器：

```python
import jax
import jax.numpy as jnp
from jax import random
import optax

# 参数是嵌套字典（pytree）
params = {
    'layer1': {'w': ..., 'b': ...},
    'layer2': {'w': ..., 'b': ...},
    'layer3': {'w': ..., 'b': ...},
}

# 纯函数前向传播
def forward(params, x):
    x = jnp.dot(x, params['layer1']['w']) + params['layer1']['b']
    x = jax.nn.relu(x)
    x = jnp.dot(x, params['layer2']['w']) + params['layer2']['b']
    x = jax.nn.relu(x)
    x = jnp.dot(x, params['layer3']['w']) + params['layer3']['b']
    return x

# JIT 编译训练步骤
@jax.jit
def train_step(params, opt_state, x, y):
    loss, grads = jax.value_and_grad(loss_fn)(params, x, y)
    updates, opt_state = optimizer.update(grads, opt_state, params)
    params = optax.apply_updates(params, updates)
    return params, opt_state, loss
```

10 epoch，约 97% 测试准确率。注意缺少的东西：没有 `.zero_grad()`、没有 `.backward()`、没有 `.step()`。整个更新是一个组合函数调用。

## 用框架实现

### Flax：Google 标准

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
```

### Optax：可组合优化器

```python
optimizer = optax.chain(
    optax.clip_by_global_norm(1.0),
    optax.adamw(learning_rate=schedule, weight_decay=0.01),
)
```

梯度裁剪、warmup、权重衰减——全部作为变换链组合。

## 练习题

1. 在 MLP 中添加 dropout，需要传入 PRNG key。
2. 用 `jax.vmap` 计算逐样本梯度。
3. 用 `jax.tree.leaves` 实现通用 mlp_forward。
4. 对比有/无 `@jax.jit` 的训练速度。
5. 用 Optax 组合梯度裁剪和 Adam。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| XLA | "让 JAX 快的东西" | 加速线性代数——融合操作生成优化 GPU/TPU 内核的编译器 |
| JIT | "即时编译" | 首次调用时追踪函数，编译到 XLA，后续调用运行编译版本 |
| 纯函数 (Pure function) | "无副作用" | 输出只依赖输入的函数——无全局状态、无变异 |
| vmap | "自动批处理" | 将处理单个样本的函数提升为处理批量的函数 |
| Pytree | "嵌套字典数组" | JAX 可遍历和变换的列表、元组、字典、数组的嵌套结构 |
| 追踪 (Tracing) | "记录计算" | JAX 用抽象值执行函数来构建计算图 |
| Optax | "JAX 的优化器库" | 可组合的梯度变换库 |

## 延伸阅读

- JAX 文档：https://jax.readthedocs.io/
- Flax 文档：https://flax.readthedocs.com/
- "You Don't Know JAX" (Colin Raffel, 2020)
