# 简介:Jax入门

> 光器突变了光器. 光流构建了图表. JAX编译了纯函数.

> **【中文解读】**火可变张量,光流 静态图,JAX 编译纯函数──JAX 的函数式编程范式是深度学习的新方向Google的双胞胎就用JAX 训练──本章学习JAX的核心:jit 编译、vmap 向量化、grad 自动微分──

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 03 Lessons 01-10, basic NumPy
**Time:** ~90 minutes

## 学习目标

- 使用JAX的功能 API (jax.numpy, jax.grad, jax.jit, jax.vmap) 编写纯函数神经网络代码
- 解释PyTorch的热情突变和JAX的功能编译模型之间的关键设计区别
- 应用 jit 编译和 vmap 矢量化来加速训练循环与天真的 Python 相比
- 训练一个简单的网络在JAX和对比明确的状态管理PyTorch的对象导向方法

> **【中文解读】**本章学习 JAX的函数式编程范式──与 PyTorch的核心区别:没有可变状态──没有 .后退() 、没有 nn.Module──一切通过函数变化实现:jax.grad 计算梯度、jax.jit 编译加速、jax.vmap 自动向量化──Google Gemini 和人类克劳德都使用 JAX 训练──

## 问题 问题引入

你知道如何在 PyTorch 构建神经网络.`nn.Module`打电话`.backward()`通过优化器,它可以工作,数百万人使用它.

> 你已经知道如何在 PyTorch 中构建神经网络.`nn.Module`调用`.backward()`进步优化器. 它能工作. 数百万人使用它.

但PyTorch在DNA中有着一个限制:它热切地追踪了Python中的操作,一次性.`tensor + tensor`每个训练步骤都重新解释了相同的Python代码. 这就会很好地运行,直到你需要训练一个540亿参数模型在2,048个TPU上. 然后,上层费用会杀死你.

> 但PyTorch的DNA有一个限制:它逐个急切地追踪操作,使用Python执行.`tensor + tensor`每个训练步骤都重新解释相同的Python代码. 在需要跨2,048个TPU训练之前,

谷歌深心训练双胞胎在JAX上.人类训练克劳德在JAX上. 这些不是小操作 - - 这是地球上最大的神经网络训练运行. 他们选择JAX,因为它把你的训练循环视为一个可编译的程序,而不是一个序列的Python呼叫.

> 谷歌深度思维使用JAX训练双胞胎.人类使用JAX训练克劳德. 这些不是小规模的操作.它们是地球上最大的神经网络训练运行. 他们选择JAX是因为它把你的训练循环作为编译程序,而不是一系列的Python调用.

JAX是NumPy,具有三个超级能力:自动分化,JIT编译到XLA,自动向量化.你写一个处理一个例子的函数.JAX给你一个处理批量,计算梯度,编译到机器代码,并运行在多个设备上.所有这些都没有改变原始函数.

> JAX 是三个超能力的NumPy:自动微分、JIT 编译成XLA 和自动向量化──你写一个处理单个样本的函数──JAX 给你一个处理批量、计算梯度、编译为机器码和运行于多个设备的函数──所有这些都不需要改变原始函数──

> **【中文解读】**皮托尔奇的局限性:每次训练都重新解释了Python代码,每个子运算都是单独的内核启动. 在2048块TPU上训练540B参数模型时,这个开销是不可接受的.

> **【拓展：JAX 的工业应用】**谷歌深心使用JAX 训练双子座(最大版本据传超过1T参数) ――人类使用JAX 训练Claude 系列――谷歌的AlphaFold 2/3也使用JAX――JAX的优势在超大规模分布式训练中:使用pmap 在数千块TPU上自动并行,使用shard_map做模型并行――但JAX的调试难度远高于PyTorch――

## 概念的核心概念

### 杰克斯的设计哲学

没有类,没有变态,没有变态.`.backward()`方法,而是:

> JAX 是一个函数式框架.`.backward()`方法──取而代之之是:

| PyTorch | JAX |
|---------|-----|
| `nn.Module` class with state | Pure function: `f(params, x) -> y` |
| `loss.backward()` | `jax.grad(loss_fn)(params, x, y)` |
| Eager execution | JIT compilation via XLA |
| `for x in batch:` manual loop | `jax.vmap(f)` auto-vectorization |
| `DataParallel` / `FSDP` | `jax.pmap(f)` auto-parallelism |
| Mutable `model.parameters()` | Immutable pytree of arrays |

这不是一种风格偏好.这是一个编译器的限制.JIT编译需要纯粹的函数 - - 同样的输入总是产生相同的输出,没有副作用.这种限制是使得100倍的速度可能.

> 这不是风格偏好. 这就是编译器约束. 编译需要纯函数.

> 这不是风格偏好. 这就是编译器约束. 编译需要纯函数.

### 简单的说法是:

JAX重新实现NumPy API在加速器上:

```python
import jax.numpy as jnp

a = jnp.array([1.0, 2.0, 3.0])
b = jnp.array([4.0, 5.0, 6.0])
c = jnp.dot(a, b)
```

它们的功能名称和规则相同,它们的语义也相同,但它们的数组在GPU/TPU上运行,

> 同样的函数名称――同样的广播规则――同样的切片语义――但数组在GPU/TPU上,每个操作都可由编译器追踪――

另一个关键区别是, JAX 阵列是不可变的.`a[0] = 5`换句话说:`a = a.at[0].set(5)`这一周觉得很尬,然后点击-- 变化是什么让变化像`grad`现在`jit`其他`vmap`的.

> 一个关键区别:JAX 数组是不可变的.`a[0] = 5`,而是用`a = a.at[0].set(5)`首先会感觉到变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变得变`grad`,我知道.`jit`和 `vmap`等变换可组合的基础.

### 简单的定义是:

光将梯度粘合到光 (`.grad`X将梯度连接到函数.

> 火将梯度加到张量上`.grad`简单的函数是

```python
import jax

def f(x):
    return x ** 2

df = jax.grad(f)
df(3.0)
```

`jax.grad`取一个函数,返回一个新的函数,计算梯度.`.backward()`电梯是另一个函数,你可以调用,编译或编译JIT.

> `jax.grad`接收一个函数,返回一个计算梯度的新函数.`.backward()`调用――张量上不存储计算图――梯度只是你可以调用、组合或JIT编译的另一个函数――

这任意构成:

> 这可以任意组合:

```python
d2f = jax.grad(jax.grad(f))
d2f(3.0)
```

它们是二次衍生,第三次衍生,雅可比亚,赫西亚,所有这些都是由编译.`grad`皮托奇也可以做到这一点.`torch.autograd.functional.hessian`在JAX中,它是基础.

> 两阶导数――三阶导数――可比矩阵――海森矩阵――全部通过组合`grad`实现──PyTorch 也能做`torch.autograd.functional.hessian`在JAX中,这是基础.

限制:`grad`没有打印语句 (它们在追踪过程中运行,而不是执行). 没有外部状态的突变.没有无明确的关键管理的随机数生成.

> 限制:`grad`内部不能有打印语句,它们在追踪时运行,在执行时运行) 不能修改外部状态.

> **【拓展：JAX 的 grad vs PyTorch 的 autograd】**皮托尔奇 把梯度存在子上(x.grad),JAX 把梯度看作函数的输出――这意味着JAX 天然支持高阶导数(grad(((f))),而皮托尔奇需要特殊处理――在JAX中,计算赫西亚矩阵只需要`jax.hessian(f)`火器需要`torch.autograd.functional.hessian`,我知道.

### 编译到XLA

```python
@jax.jit
def train_step(params, x, y):
    loss = loss_fn(params, x, y)
    return loss

fast_step = jax.jit(train_step)
```

在第一次电话中,JAX追踪了函数,记录了哪些操作发生,而不执行它们.然后将这些痕迹交给了Google的TPU和GPU编译器XLA.XLA将操作合并,消除冗余的内存副本,并生成优化的机器代码.

> 在第一次调用时,JAX 追踪函数记录发生的操作,而实际执行不了.然后将追踪交给XLA,Google为TPU和GPU开发的编译器.

随后的调用完全跳过Python.编译的代码在C++速度上运行.

> 后续调用完全跳过Python──编译后代码以C++速度在加速器上运行──

当JIT有助于:

> 让我们有帮助的场景:

- 训练步骤 (同样的计算重复了数千次)
  中文翻译:训练步骤(同样的计算重复数千次)
- 推理 (相同的模型,不同的输入)
  中文翻译:推理(同样模型,不同输入)
- 任何一个函数,多次调用,具有类似形状的输入
  中文翻译:任何以相似形状输入多次调用函数

当JIT疼痛时:

> ,我知道你有什么问题.

- 基于值的Python控制流程的函数 (`if x > 0`在 x 是一个追踪数组)
  中文翻译:包含依赖值的 Python 控制流的函数`if x > 0`其中x是被追踪的数组)
- 单次计算 (编译总费超过运行时间)
  中文翻译:一次性计算 (编译开销超过运行时间)
- 调试 (追踪隐藏实际执行)
  中文翻译:调试(追踪隐藏了实际执行)

控制流量限制是真实的.`jax.lax.cond`替换`if/else`现在,我们要去.`jax.lax.scan`替换`for`这些不是可选的,它们是编译的价格.

> 控制流限制是真实的.`jax.lax.cond`替代`if/else`,我知道.`jax.lax.scan`替代`for`循环──这些不是可选的它们是编译的代价──

### 它们是自动向量化.

你写一个函数,处理一个例子:

> 你写一个处理单个样本的函数:

```python
def predict(params, x):
    return jnp.dot(params['w'], x) + params['b']
```

`vmap`提升它处理一批:

```python
batch_predict = jax.vmap(predict, in_axes=(None, 0))
```

`in_axes=(None, 0)`方式:不要批量过度`params`                                                          `x`没有手册`for`没有重塑,没有批量维度线程, JAX 计算了批量维度,并向量化了整个计算.

> `in_axes=(None, 0)`表示:不对`params`进行批处理(共享),对`x`无需手动处理`for`循环――无需重塑――无需手动传递批量维度――JAX自动查出批量维度并向量化整个计算――

这不是语法糖.`vmap`它生成的结合向量化代码比Python循环快10-100倍.`jit`其他`grad`其他:

> 这不是语法糖.`vmap`成融合的量化代码,比Python 循环快10-100倍.`jit`和 `grad`组合:

```python
per_example_grads = jax.vmap(jax.grad(loss_fn), in_axes=(None, 0, 0))
```

没有黑客,这几乎是不可能的.

> 逐样本梯度――一行代码――这在PyTorch中几乎不可能不用技巧实现――

### 跨设备数据并行

```python
parallel_step = jax.pmap(train_step, axis_name='devices')
```

`pmap`复制功能在所有可用的设备 (GPU/TPU) 上,并分组.`jax.lax.pmean`其他`jax.lax.psum`通过设备进行梯度同步.

> `pmap`将函数复制到所有可用的设备上,并分量.`jax.lax.pmean`和 `jax.lax.psum`跨设备同步梯度――

谷歌将双子座训练通过数千个TPU v5e芯片使用`pmap`(以及其继任者)`shard_map`编程模型:写单设备版本,用 `pmap`完成了.

> 谷歌使用`pmap`(及其后继者`shard_map`) 在数千块的TPU v5e 芯片上训练双子.编程模型:写单设备版本,用`pmap`包装,完成.

### 普世数据结构

简单的说法是,我们可以在一个字符串中找到一个字符串,

> 简单的定义是:

```python
params = {
    'layer1': {'w': jnp.zeros((784, 256)), 'b': jnp.zeros(256)},
    'layer2': {'w': jnp.zeros((256, 128)), 'b': jnp.zeros(128)},
    'layer3': {'w': jnp.zeros((128, 10)),  'b': jnp.zeros(10)},
}
```

每一个JAX变化--`grad`现在`jit`现在`vmap`知道如何穿越树.`jax.tree.map(f, tree)`适用`f`这就是优化器一次更新所有参数的方式:

> 每个JAX 变换`grad`,我知道.`jit`,我知道.`vmap`都知道如何穿过这个树.`jax.tree.map(f, tree)`将`f`应用到每个叶子. 这就是优化器一次更新所有参数的方式:

```python
params = jax.tree.map(lambda p, g: p - lr * g, params, grads)
```

没有.`.parameters()`没有参数登记.树结构是模型.

> 没有`.parameters()`方法──没有参数注册──树结构就是模型──

### 函数式对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对象对比

皮托奇的商店表示物体内:

```python
class Model(nn.Module):
    def __init__(self):
        self.linear = nn.Linear(784, 10)

    def forward(self, x):
        return self.linear(x)
```

JAX使用纯函数,具有明确状态:

```python
def predict(params, x):
    return jnp.dot(x, params['w']) + params['b']
```

任何东西都存储不存在. 任何东西都没有变化. 这使得每个函数都能测试,编译和编译. 这也意味着你自己管理这些参数 - 或者使用像或平行一样的图书馆.

> 参数被传输. 没有存储任何东西. 没有修改任何东西. 这使每个函数可测试,组合,编译. 这也意味着你需要自己管理参数.

### 杰克斯生态系统

简单的图书馆,是机械的.

> 简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单

| Library | Role | Style |
|---------|------|-------|
| **Flax** (Google) | Neural network layers | `nn.Module` with explicit state |
| **Equinox** (Patrick Kidger) | Neural network layers | Pytree-based, Pythonic |
| **Optax** (DeepMind) | Optimizers + LR schedules | Composable gradient transforms |
| **Orbax** (Google) | Checkpointing | Save/restore pytrees |
| **CLU** (Google) | Metrics + logging | Training loop utilities |

优化图库是标准优化图库.它将梯度转换 (亚当,SGD,剪辑) 与参数更新分开,使得编写:

> 优化是标准优化器库. 它将变化梯度 (Adam,SGD,剪裁) 与参数更新分离,使组合变得轻松和易举:

```python
optimizer = optax.chain(
    optax.clip_by_global_norm(1.0),
    optax.adam(learning_rate=1e-3),
)
```

### 什么时候使用JAX和PyTorch

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

诚实答案:使用 PyTorch 除非你有特定的理由使用 JAX. 这些原因是: TPU 访问,需要每个例子的梯度,

> 诚实的答案:除非有特定的原因,否则使用 PyTorch──这些原因是TPU 访问、需要逐样本梯度、大规模多设备训练,或在Google/DeepMind/Anthropic工作──

### 在JAX中随机数

简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的简单的

> 没有全局随机状态. 每个随机操作都需要显然的PRNG密钥:

```python
key = jax.random.PRNGKey(42)
key1, key2 = jax.random.split(key)
w = jax.random.normal(key1, shape=(784, 256))
```

这一点最初很令人丧,但它保证了设备和编译中可再生性. PyTorch 开发的特性`torch.manual_seed`在多GPU设置中不能保证.

> 开始很麻烦人. 但它保证了跨设备和编译的可复性.`torch.manual_seed`在多个GPU环境中无法保证的.
```figure
batchnorm-effect
```

## 建立它

## 建立它,实现它.

> **【中文解读】**用JAX + Optax 训练 MNIST 分类器──注意和 PyTorch 的关键区别:没有 nn.Module、参数用嵌套字典(pytree) 存储、训练步骤是纯函数用 @jax.jit 编译、没有 .zero_grad() /.backward() /.step() 梯度计算和参数更新合并在一个函数中──

### 设置和数据.

我们将在MNIST上训练一个3层MLP使用JAX和Optax. 784输入,两个隐藏的 256和 128个神经元层, 10个输出类.

> 我们将使用 JAX 和 Optax 在 MNIST 上训练一个3层 MLP──784个输入,两个256 和 128 层 神经的隐藏层,10个输出类别──

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

### 启动参数.

没有类,只是返回一个字符:

> 没有类. 只是一个返回字符的函数:

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

按手动启动,三个PRNG键从一个种子中分开,每个重量都是一个无变的数组.

> 手动完成的 他初始化――三个PRNG 密钥从一个种子分离而来――每个权重都是嵌套字典中的不可变数组――

### 步骤3:前进传递.

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

纯功能的参数,预测.`self`没有存储状态.`loss_fn`计算了从零开始的交叉缩--软max,日志,负平均.

> 纯函数――参数进,预测出――没有`self`没有存储状态.`loss_fn`从头计算交叉软max、log、负平均值──

### 编译的训练步骤

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

`jax.value_and_grad`输出值和梯度均返回一次.`@jax.jit`装饰器将这两个函数组合到XLA. 在第一次调用后,每个训练步骤都会运行,而不需要触摸Python.

> `jax.value_and_grad`在一次传播中同时返回损失值和梯度.`@jax.jit`装饰器将两个函数编译成XLA――第一次调用后,每个训练步骤不再接触 Python――

### 训练循环第五步:训练循环

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

测试精度为97%左右.第一阶段缓慢 (JIT编译).2-10阶段快速.

> 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为97% 测试准确率为9

注意什么缺失:没有`.zero_grad()`没有`.backward()`没有`.step()`整个更新是一个复合函数调用. 基准被计算,由亚当转化,`train_step`现在,我们要去.

> 注意缺失了什么:没有`.zero_grad()`没有`.backward()`没有`.step()`△整个更新是一个组合函数调用――梯度被计算、被亚当变换、被应用到参数上全部在`train_step`在完成中.

> **【拓展：JAX 的分布式训练】**JAX的 pmap 可以自动将训练分布在多个设备中.`jax.pmap(train_step, axis_name='batch')`按一下,每块GPU处理一个,然后通过一个.`jax.lax.pmean`同步梯度──谷歌的TPUPod有数千块芯片,JAX的网格和 shard_map可以在数千个设备上进行模型和行程.

## 用它实现框架

> **【中文解读】**JAX 生态的核心库:Flax(Google的神经网络层库,类似 nn.Module) √Equinox(更 Pythonic的替代) √Optax(可组合的优化器库) ・Optax的设计哲学:优化器是梯度变化的链式组合剪 → Adam → 权重衰减,每一步都是独立的变化──

### 谷歌标准库

是最常见的JAX神经网络库.`nn.Module`只有一个国家管理:

> 是最常用的JAX神经网络库.`nn.Module`通过显式状态管理:

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

结构与PyTorch相同,但`params`单独与模型.`model.init()`创造了"".`model.apply(params, x)`模型对象没有状态.

> 结构与 PyTorch 相同,但`params`与模型分离.`model.init()`创建参数――`model.apply(params, x)`运行前向传播――模型对象没有状态――

### 平:字thon的替代方案

方程 (由帕特里克·基德格) 代表模型为 pytrees:

> 方程 (由Patrick Kidger 开发) 将模型表示为 pytree:

```python
import equinox as eqx

model = eqx.nn.MLP(
    in_size=784, out_size=10, width_size=256, depth=2,
    activation=jax.nn.relu, key=jax.random.PRNGKey(0)
)
logits = model(x)
```

模型本身就是一个字树.`.apply()`参数只是模型的叶子. 这就像JAX的想法.

> 模型本身就是一个木.`.apply()`参数只是模型的叶子.

### 优质:可组合优化器

tax将梯度转换与更新分离:

> 优势将变化与更新解:

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

渐变减小,学习速度升温,体重衰减,都构成了一系列转变. 每次转变都会看到梯度,修改它们,然后将它们传递给下一个.没有单一的优化器类.

> 梯度剪裁,学习率预热,权重减弱,全部作为变化链组合.

## 运送它.

**Installation:**

```bash
pip install jax jaxlib optax flax
```

对于GPU支持:

```bash
pip install jax[cuda12]
```

对于TPU (谷歌云):

```bash
pip install jax[tpu] -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
```

**Performance gotchas:**

- 首先,JIT调用速度缓慢 (编译).
- 避免在JIT内部的JAX阵列上使用Python循环.`jax.lax.scan`或`jax.lax.fori_loop`现在,我们要去.
- `jax.debug.print()`在JIT内部工作.`print()`没有.
- 个人资料`jax.profiler`果版可以隐藏瓶.
- 预定配置了75%的GPU内存.`XLA_PYTHON_CLIENT_PREALLOCATE=false`禁止使用.

**Checkpointing:**

```python
import orbax.checkpoint as ocp
checkpointer = ocp.PyTreeCheckpointer()
checkpointer.save('/tmp/model', params)
restored = checkpointer.restore('/tmp/model')
```

**This lesson produces:**
- `outputs/prompt-jax-optimizer.md`-- 提示选择正确的JAX优化器配置
- `outputs/skill-jax-patterns.md`-- 涵盖JAX的功能模式的技能

## 练习题

1. 在JAX中,中断需要一个PRNG键 - - 通过前进传输键将一个键分为每个中断层.

2. 使用`jax.vmap`计算每一个例子的梯度为32个MNIST图像.计算每个例子的梯度标准.哪个例子有最大的梯度,为什么?

3. 取代手动前进函数以通用函数`mlp_forward(params, x)`使用  片`jax.tree.leaves`为了自动确定深度.

4. 准训练步骤,包括和没有`@jax.jit`时间100步. 您的硬件的加快速度是多大?

5. 通过编译实现梯度剪切`optax.chain(optax.clip_by_global_norm(1.0), optax.adam(1e-3))`炼,不剪切,炼,炼,看效果.

## 关键词 快速查找表

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

## 继续阅读 继续阅读

-  JAX 文件: https://jax.readthedocs.io/官方的博士, 提供了优秀的教程,
  简介:https://jax.readthedocs.io/官方文档,关于大和vmap的优秀教程
- "JAX:Python+NumPy程序的可组合转换" (Bradbury等, 2018) -- 解释设计哲学的原始论文
  布拉德伯里 等人,JAX:Python+NumPy 程序的可组合变换(2018) 解释设计哲学原始论文
- 料文件: https://flax.readthedocs.io/谷歌的神经网络库用于JAX
  布文档 谷歌为JAX开发 神经网络库
- 帕特里克·基德格"等式:通过可调用的PyTrees和过转换在JAX中的神经网络" (2021) - - 的Pythonic替代品
  通过可调用PyTree 和过变换实现JAX 神经网络(2021) Flax的 Pythonic替代方案
- 果:可构成梯度转换和优化"--标准优化库
                                                                                                                                                                                                                                                                
- "你不知道JAX" (Colin Raffel,2020) - - 一本来自T5作者的一份关于JAX的方法和模式的实用指南
  卡林·拉菲尔,你还不了解JAX(2020) JAX 陷和模式的实用指南,作者为T5 论文作者之一
