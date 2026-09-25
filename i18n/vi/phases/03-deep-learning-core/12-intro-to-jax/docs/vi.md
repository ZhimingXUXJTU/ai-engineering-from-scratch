# Đề xuất JAX JAX vào

> PyTorch biến đổi các tensor. TensorFlow xây dựng đồ thị. JAX biên soạn các hàm tinh khiết.

> **【中文解读】**PyTorch 可变张量,TensorFlow 静态图,JAX 编译纯函数──JAX 函数式编程范式是深度学习的新方向Google's Gemini 就用JAX 训练──本章学习JAX 的核心:jit 编译、vmap 向量化、grad 自动微分──

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 03 Lessons 01-10, basic NumPy
**Time:** ~90 minutes

## Mục tiêu học tập

- Viết mã mạng thần kinh chức năng thuần túy bằng cách sử dụng API chức năng của JAX (jax.numpy, jax.grad, jax.jit, jax.vmap)
- Giải thích sự khác biệt thiết kế chính giữa đột biến nhiệt tình của PyTorch và mô hình biên soạn chức năng của JAX
- Sử dụng biên soạn jit và vmap vectorization để tăng tốc vòng đào tạo so với Python ngây thơ
- Trình luyện một mạng đơn giản trong JAX và so sánh quản lý trạng thái rõ ràng với cách tiếp cận định hướng đối tượng của PyTorch

> **【中文解读】**本章学习 JAX's hàm式编程范式──与 PyTorch's核心区别:没有可变状态、没有 .后退()、没有 nn.Module──一切通过函数变换实现:jax.grad 计算梯度、jax.jit 编译加速、jax.vmap 自动向量化──Google Gemini 和人类Claude 都使用 JAX 训练──

## Vấn đề  vấn đề giới thiệu

Bạn biết cách xây dựng mạng thần kinh trong PyTorch.`nn.Module`, gọi `.backward()`Nó hoạt động, hàng triệu người sử dụng nó.

> Bạn đã biết làm thế nào để xây dựng mạng thần kinh trong PyTorch. Bạn đã định nghĩa một .`nn.Module`,调用 `.backward()`, tiến bộ tối ưu hóa. Nó có thể làm việc. Hàng triệu người sử dụng nó.

Nhưng PyTorch có một hạn chế trong DNA của nó: nó theo dõi các hoạt động với sự nhiệt tình, một lần một, trong Python.`tensor + tensor`mỗi bước đào tạo lại giải thích lại cùng một mã Python. Điều này hoạt động tốt cho đến khi bạn cần đào tạo một mô hình thông số 540 tỷ trên 2.048 TPU.

> Nhưng trong DNA của PyTorch có một giới hạn: nó từng cá nhân nhanh chóng theo dõi hoạt động, sử dụng Python 执行.`tensor + tensor`Tất cả đều là một khởi động nội nhân độc lập. Mỗi bước đào tạo đều giải thích lại cùng một mã Python.

Google DeepMind đào tạo Gemini trên JAX. Anthropic đào tạo Claude trên JAX. Đây không phải là các hoạt động nhỏ - chúng là các hoạt động đào tạo mạng thần kinh lớn nhất trên Trái Đất. Họ chọn JAX vì nó xử lý vòng đào tạo của bạn như một chương trình có thể biên dịch, không phải là một chuỗi các cuộc gọi Python.

> Google DeepMind sử dụng JAX  đào tạo Gemini。Anthropic sử dụng JAX  đào tạo Claude。These are not small scale operationsthey are the largest neural network training operation on Earth。 Họ chọn JAX vì nó đưa vòng tròn đào tạo của bạn như một chương trình có thể biên dịch, chứ không phải là một loạt Python 调用。

JAX là NumPy với ba siêu năng lực: phân biệt tự động, biên soạn JIT thành XLA và vectorization tự động. Bạn viết một hàm xử lý một ví dụ. JAX cho bạn một hàm xử lý một lô, tính toán gradient, biên soạn thành mã máy và chạy trên nhiều thiết bị. Tất cả mà không thay đổi chức năng ban đầu.

> JAX là một hệ thống có 3 siêu năng lực: tự động phân phân tích, JIT  biên dịch thành XLA và tự động định lượng hóa. Bạn viết một hàm xử lý một mẫu đơn. JAX cung cấp cho bạn một hàm xử lý khối lượng, tính toán thang độ, biên dịch thành mã máy và hoạt động trên nhiều thiết bị. Tất cả những điều này không cần phải thay đổi hàm gốc.

> **【中文解读】**Biên giới của PyTorch: Mỗi lần đào tạo đều giải thích lại mã Python, mỗi tensor vận hành đều là một hạt nhân riêng biệt khởi động. Trong 2048 khối TPU trên đào tạo 540B mô hình tham số, việc này không thể chấp nhận được.

> **【拓展：JAX 的工业应用】**Google DeepMind sử dụng JAX  đào tạo Gemini(最大版本据传超过1T 参数) ――Anthropic sử dụng JAX 训练Claude 系列──Google's AlphaFold 2/3 cũng sử dụng JAX──JAX's优势在超大规模分布式训练: sử dụng pmap 在数千块 TPU 上自动并行, sử dụng shard_map做模型并行──但 JAX's调试难度远高于Pytorch──

## Khái niệm cốt lõi

### Triết lý thiết kế của JAX

JAX là một hệ thống chức năng không có lớp, không có trạng thái thay đổi, không có`.backward()`Thay vào đó:

> JAX là một khung hàm. Không có loại, không có trạng thái biến đổi, không có.`.backward()`方法──取而代之 là:

| PyTorch | JAX |
|---------|-----|
| `nn.Module` class with state | Pure function: `f(params, x) -> y` |
| `loss.backward()` | `jax.grad(loss_fn)(params, x, y)` |
| Eager execution | JIT compilation via XLA |
| `for x in batch:` manual loop | `jax.vmap(f)` auto-vectorization |
| `DataParallel` / `FSDP` | `jax.pmap(f)` auto-parallelism |
| Mutable `model.parameters()` | Immutable pytree of arrays |

Đây không phải là một sự ưu tiên về phong cách. Đó là một hạn chế biên dịch. Việc biên dịch JIT đòi hỏi các chức năng tinh khiết - cùng đầu vào luôn tạo ra cùng một kết quả, không có tác dụng phụ.

> Đây không phải là một sự lựa chọn kiểu. Đây là một sự ràng buộc của các trình biên dịch.

> Đây không phải là một sự lựa chọn kiểu. Đây là một sự ràng buộc của các trình biên dịch.

### Jax.numpy: The Familiar Surface

JAX tái triển khai API NumPy trên các bộ đẩy:

```python
import jax.numpy as jnp

a = jnp.array([1.0, 2.0, 3.0])
b = jnp.array([4.0, 5.0, 6.0])
c = jnp.dot(a, b)
```

cùng tên chức năng, cùng quy tắc phát sóng, cùng ngữ nghĩa cắt, nhưng các mảng hoạt động trên GPU/TPU, và mọi hoạt động đều có thể theo dõi bởi trình biên dịch.

> Hình thức của các hàm tương tự. Quy tắc phát sóng tương tự.

Một sự khác biệt quan trọng: các mảng JAX không thay đổi.`a[0] = 5`Thay vào đó:`a = a.at[0].set(5)`Điều này cảm thấy khó khăn trong một tuần, sau đó nó nhấp vào -- sự không thay đổi là điều làm cho những biến đổi như`grad`- `jit`, và`vmap`- Đơn vị.

> Một quan trọng khác biệt: JAX 数组 là không thể thay đổi. Không thể viết.`a[0] = 5` thay vì dùng `a = a.at[0].set(5)` Đầu tiên sẽ cảm thấy khác, sau đó sẽ nhận ra nếu biến động chính xác`grad``jit`和 `vmap`等变换可组合的基础――

### jax.grad: Functional Autodiff 

PyTorch gắn gradient với các tensor (`.grad`JAX gắn gradient với các hàm.

> PyTorch sẽ thêm thang lên 张量上`.grad`(※JAX sẽ được thêm vào hàm trên.

```python
import jax

def f(x):
    return x ** 2

df = jax.grad(f)
df(3.0)
```

`jax.grad`lấy một hàm và trả lại một hàm mới tính toán gradient.`.backward()`không có biểu đồ tính toán được lưu trữ trên các tensor. gradient chỉ là một chức năng khác bạn có thể gọi, soạn, hoặc JIT-compile.

> `jax.grad`接收一个函数, trả lại một hàm mới của tính toán梯度.`.backward()`调用──张量上不存储计算图──梯度只是另一个你可以调用、组合或 JIT 编译的函数──

Điều này tạo thành tùy tiện:

> Có thể được kết hợp tùy chọn:

```python
d2f = jax.grad(jax.grad(f))
d2f(3.0)
```

Các phái sinh thứ hai, phái sinh thứ ba, Jacobian, Hessian, tất cả bằng cách tạo ra`grad`PyTorch cũng có thể làm điều này (`torch.autograd.functional.hessian`Trong JAX, nó là nền tảng.

> Hai giai đoạn. Ba giai đoạn.`grad`实现──PyTorch 也能做(`torch.autograd.functional.hessian`Nhưng nó là một phần sau. Trong JAX, đó là cơ sở.

Sự hạn chế:`grad`Không có lệnh in bên trong (bạn chạy trong quá trình theo dõi, không thực hiện). Không có đột biến của trạng thái bên ngoài. Không tạo ra số ngẫu nhiên mà không có quản lý khóa rõ ràng.

> 限制:`grad`Chỉ áp dụng cho hàm đơn giản. Không có thể in được trong các hàm. Không thể thay đổi trạng thái bên ngoài. Không có quản lý khóa rõ ràng. Không thể tạo ra số tự nhiên.

> **【拓展：JAX 的 grad vs PyTorch 的 autograd】**PyTorch 把梯度存在テンসর 上(x.grad),JAX 把梯度看作函数的输出──这意味着JAX 天然支持高阶导数(grad((grad(f))),而 PyTorch 需要特殊处理──在JAX 中,计算 Hessian矩阵只需`jax.hessian(f)`,PyTorch  cần `torch.autograd.functional.hessian`

### XLA: biên dịch thành XLA

```python
@jax.jit
def train_step(params, x, y):
    loss = loss_fn(params, x, y)
    return loss

fast_step = jax.jit(train_step)
```

Khi gọi đầu tiên, JAX theo dõi chức năng - nó ghi lại các hoạt động xảy ra mà không thực hiện chúng. Sau đó nó đưa manh mối đó đến XLA (Quá trình lập trình tuyến tính tăng tốc), bộ sưu tập của Google cho TPU và GPU. XLA hợp nhất các hoạt động, loại bỏ các bản sao bộ nhớ dư thừa, và tạo ra mã máy tối ưu hóa.

> Trong lần đầu tiên sử dụng, hàm theo dõi JAX ghi lại những hoạt động xảy ra, không thực hiện. Sau đó sẽ chuyển giao theo dõi cho XLA, Google cho TPU và GPU.

Các cuộc gọi sau đó bỏ qua Python hoàn toàn. Mã được biên soạn chạy trên bộ tăng tốc ở tốc độ C ++.

> 后续调用 hoàn toàn nhảy qua Python──编译后代码运行在加速器上以C++ 速度──

Khi JIT giúp:

> JIT có giúp đỡ cảnh:

- Các bước đào tạo (sự tính toán tương tự lặp lại hàng ngàn lần)
  Trung ngữ翻译:训练步骤(相同计算重复数千次)
- Tự luận (một mô hình, đầu vào khác nhau)
  Trung ngữ翻译:推理(相同模型,不同输入)
- Bất kỳ hàm nào được gọi nhiều hơn một lần với các đầu vào hình dạng tương tự
  Trung文翻译: bất kỳ hàm nào được sử dụng nhiều lần trong hình dạng tương tự

Khi JIT đau:

> JIT có cảnh sát:

- Các hàm với dòng kiểm soát Python phụ thuộc vào các giá trị (`if x > 0`nơi x là một mảng được theo dõi)
  Trung文翻译:包含依赖值的 Python 控制流的函数`if x > 0`Trong số đó x là số lượng bị theo dõi)
- Các tính toán một lần (giá tổng hợp vượt quá thời gian chạy)
  Trung ngữ翻译:一次性计算 (一次性计算)
- Debug (tracing che giấu thực tế thực hiện)
  Trung ngữ翻译:调试(追踪隐藏了实际执行)

Sự hạn chế lưu lượng kiểm soát là thực. `jax.lax.cond`thay thế `if/else`- `jax.lax.scan`thay thế `for`Loops. Đây không phải là tùy chọn - đó là giá của việc biên soạn.

> 控制流限制 là thực.`jax.lax.cond`替代 `if/else``jax.lax.scan`替代 `for`循环──These are not optionalthey are the cost of compilation──These are not optionalThese are the cost of compilation──These are not optionalThese are the cost of compilation──These are not optionalThese are the cost of compilation──These are not optionalThese are the cost of compilation──These are not optionalThese are the cost of compilation──These are not optionalThese are not optionalThese are the cost of compilation──These are not optional

### vmap: tự động vectorization

Bạn viết một hàm xử lý một ví dụ:

> Bạn viết một hàm xử lý đơn mô hình:

```python
def predict(params, x):
    return jnp.dot(params['w'], x) + params['b']
```

`vmap`nâng nó để xử lý một lô:

```python
batch_predict = jax.vmap(predict, in_axes=(None, 0))
```

`in_axes=(None, 0)`phương tiện: không đợt đợt `params`(cùng), lô trên trục 0 của `x`Không có hướng dẫn.`for`không có hình dạng lại, không có chuỗi kích thước lô, JAX tính ra kích thước lô và vector hóa toàn bộ tính toán.

> `in_axes=(None, 0)`表示: không đối với`params`进行批处理(共享), đối với `x`                                                                                                                                                                                                                                                              `for`循环──无需重塑──无需手动传递批量维度──JAX tự động tìm ra批量维度并向量化整个计算──

Đây không phải là đường tổng hợp.`vmap`tạo ra mã vector hóa hợp nhất chạy nhanh hơn 10-100 lần so với một vòng lặp Python.`jit`và `grad`- Có thể là:

> Đó không phải là một đường.`vmap`生成融合的向量化代码, hơn Python 循环快 10-100 倍.`jit`和 `grad`组合:

```python
per_example_grads = jax.vmap(jax.grad(loss_fn), in_axes=(None, 0, 0))
```

Một đường, điều này gần như không thể trong PyTorch mà không có hack.

> 逐样本梯度──一行代码── trong PyTorch gần như không thể không cần kỹ thuật để thực hiện.

### pmap: Data Parallelism Across Devices  pmap: Over Device Data

```python
parallel_step = jax.pmap(train_step, axis_name='devices')
```

`pmap`Tái bản chức năng trên tất cả các thiết bị có sẵn (GPU / TPU) và chia các lô.`jax.lax.pmean`và `jax.lax.psum`đồng bộ hóa gradient trên các thiết bị.

> `pmap`Để làm việc trong các thiết bị có sẵn, hãy phân tách số lượng.`jax.lax.pmean`和 `jax.lax.psum`跨设备同步梯度──

Google đào tạo Gemini qua hàng ngàn chip TPU v5e sử dụng `pmap`(và người kế nhiệm của nó)`shard_map`). Mô hình lập trình: viết phiên bản đơn thiết bị, kết thúc với `pmap`- Được rồi.

> Google sử dụng `pmap`(và những người kế tiếp của nó)`shard_map`) trên hàng ngàn khối chip TPU v5e 训练 Gemini.`pmap`包装,完成──

### Phytrees: Cơ cấu dữ liệu phổ quát

JAX hoạt động trên "pytrees" - kết hợp tổ hợp của danh sách, tuples, dicts, và array.

> JAX 操作"pytree"列表、元组、字典和数组的嵌套组合──你的模型参数就是一个 pytree:

```python
params = {
    'layer1': {'w': jnp.zeros((784, 256)), 'b': jnp.zeros(256)},
    'layer2': {'w': jnp.zeros((256, 128)), 'b': jnp.zeros(128)},
    'layer3': {'w': jnp.zeros((128, 10)),  'b': jnp.zeros(10)},
}
```

Mỗi sự biến đổi của JAX...`grad`- `jit`- `vmap`- biết cách vượt qua cây Pytrees.`jax.tree.map(f, tree)`áp dụng `f`Đây là cách mà các trình tối ưu hóa cập nhật tất cả các tham số cùng một lúc:

> Mỗi JAX 变换`grad``jit``vmap`都知道如何穿过Pytrie.`jax.tree.map(f, tree)`sẽ`f`应用到每个叶子――这是优化器一次更新所有参数的方式:

```python
params = jax.tree.map(lambda p, g: p - lr * g, params, grads)
```

Không .`.parameters()`Không có ký hiệu tham số.

> Không có gì`.parameters()`方法──没有参数注册──树结构就是模型──

### Phương thức chức năng đối với đối tượng định hướng

Các cửa hàng PyTorch cho biết bên trong các vật thể:

```python
class Model(nn.Module):
    def __init__(self):
        self.linear = nn.Linear(784, 10)

    def forward(self, x):
        return self.linear(x)
```

JAX sử dụng các hàm thuần khiết với trạng thái rõ ràng:

```python
def predict(params, x):
    return jnp.dot(x, params['w']) + params['b']
```

Các param được truyền vào. Không có gì được lưu trữ. Không có gì được đột biến. Điều này làm cho mọi chức năng có thể kiểm tra, hợp tác và được biên soạn. Nó cũng có nghĩa là bạn tự quản lý các param - hoặc sử dụng thư viện như Flax hoặc Equinox.

> Các tham số được truyền vào. Không lưu trữ bất cứ thứ gì. Không sửa đổi bất cứ thứ gì. Điều này giúp cho mỗi hàm có thể kiểm tra, kết hợp, biên dịch.

### Hệ sinh thái của JAX

JAX cho bạn những thứ nguyên thủy. Thư viện cho bạn những thứ ergonomic:

> JAX 提供原语──库提供便利性:

| Library | Role | Style |
|---------|------|-------|
| **Flax** (Google) | Neural network layers | `nn.Module` with explicit state |
| **Equinox** (Patrick Kidger) | Neural network layers | Pytree-based, Pythonic |
| **Optax** (DeepMind) | Optimizers + LR schedules | Composable gradient transforms |
| **Orbax** (Google) | Checkpointing | Save/restore pytrees |
| **CLU** (Google) | Metrics + logging | Training loop utilities |

Optax là thư viện tối ưu hóa tiêu chuẩn. Nó tách chuyển đổi gradient (Adam, SGD, cắt) khỏi bản cập nhật tham số, khiến nó trở nên tầm thường để soạn:

> Optax là bộ nhớ tối ưu hóa tiêu chuẩn. Nó sẽ thay đổi độ thay đổi (Adam, SGD, cắt) với các tham số mới phân chia, làm cho các bộ kết hợp trở nên dễ dàng và dễ dàng:

```python
optimizer = optax.chain(
    optax.clip_by_global_norm(1.0),
    optax.adam(learning_rate=1e-3),
)
```

### Khi nào sử dụng JAX vs PyTorch

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

Câu trả lời trung thực: sử dụng PyTorch trừ khi bạn có lý do cụ thể để sử dụng JAX. Những lý do đó là: truy cập TPU, nhu cầu gradient mỗi ví dụ, đào tạo đa thiết bị quy mô lớn, hoặc làm việc tại Google/DeepMind/Anthropic.

> 诚实的答案: trừ khi có lý do cụ thể, nếu không sử dụng PyTorch.

### Số ngẫu nhiên trong JAX

JAX không có trạng thái ngẫu nhiên toàn cầu.

> JAX không có trạng thái bất động toàn bộ. Mỗi hoạt động bất động đều cần một khóa PRNG rõ ràng:

```python
key = jax.random.PRNGKey(42)
key1, key2 = jax.random.split(key)
w = jax.random.normal(key1, shape=(784, 256))
```

Điều này ban đầu khó chịu, nhưng nó đảm bảo khả năng tái tạo trên các thiết bị và các bộ sưu tập - một tính năng mà PyTorch đã tạo ra`torch.manual_seed`không thể đảm bảo trong cài đặt nhiều GPU.

> Một khởi đầu rất khó khăn. Nhưng nó đảm bảo tính khả thi của các thiết bị và biên dịch.`torch.manual_seed`Trong nhiều môi trường GPU không thể đảm bảo được.
```figure
batchnorm-effect
```

## Hãy xây dựng nó

## Hãy xây dựng nó.

> **【中文解读】**Với JAX + Optax 训练 MNIST 分类器──注意和 PyTorch 的关键区别: không nn.Module、参数用嵌套字典(pytree) 存储、训练步骤是纯函数用 @jax.jit 编译、没有 .zero_grad() /.backward() /.step() 梯度计算和参数更新合并在一个函数中──

### Bước 1: Cài đặt và dữ liệu Bước 1: Cài đặt và dữ liệu

Chúng tôi sẽ đào tạo một MLP 3 tầng trên MNIST sử dụng JAX và Optax. 784 đầu vào, hai lớp ẩn của 256 và 128 tế bào thần kinh, 10 lớp đầu ra.

> Chúng tôi sẽ sử dụng JAX và Optax trên MNIST để đào tạo một 3 tầng MLP―784 đầu vào, hai 256 và 128 tầng ẩn của thần kinh,10 loại đầu ra―

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

### Bước 2: Tạo ra các tham số. Bước 2: Tạo ra các tham số.

Không có lớp, chỉ là một hàm trả lại một cây:

> Không có loại. Chỉ là một hàm của một cây quay lại:

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

- He-initialisation, làm bằng tay ba phím PRNG tách ra từ một hạt.

> Hàm động hoàn thành He 初始化──三个 PRNG 钥匙 từ một hạt chia chia đến. Mỗi trọng lượng là một số lượng không thể thay đổi trong bản ngữ bản ngữ.

### Bước 3: Chuyển tiếp. Bước 3: Chuyển tiếp.

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

- Các chức năng tinh khiết, các param vào, dự đoán ra.`self`, không lưu trữ trạng thái. `loss_fn`tính toán sự chuyển đổi từ đầu -- softmax, log, trung bình âm.

> 纯函数──参数进,预测出──没有 `self`, không có trạng thái lưu trữ.`loss_fn`Từ đầu tính toán交叉softmax、log、负平均值──

### Bước 4: Bước tập hợp JIT

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

`jax.value_and_grad`trả lại cả giá trị mất và gradient trong một lần đi.`@jax.jit`khi thiết kế kết hợp cả hai chức năng cho XLA. Sau cuộc gọi đầu tiên, mỗi bước đào tạo chạy mà không chạm vào Python.

> `jax.value_and_grad`Trong một lần truyền tải, đồng thời trả lại giá trị và mức độ mất mát.`@jax.jit`装饰器 sẽ biên dịch hai hàm thành XLA. Sau lần đầu tiên, mỗi bước tập luyện không còn chạm vào Python.

### Bước 5: vòng tập luyện.

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

10 thời đại. ~ 97% độ chính xác thử nghiệm. thời đại đầu tiên chậm (sự biên soạn JIT).

> 10 个时代──~97% 测试准确率──第一个时代 较慢(JIT 编译)──第 2-10 个时代 很快──

Nhìn xem thiếu gì: không `.zero_grad()`Không .`.backward()`Không .`.step()`Toàn bộ bản cập nhật là một cuộc gọi hàm tổng hợp. Các gradient được tính toán, biến đổi bởi Adam, và áp dụng cho các tham số - tất cả bên trong`train_step`- Tôi không biết.

> chú ý thiếu gì: không có gì`.zero_grad()`, không có `.backward()`, không có `.step()`△ toàn bộ update là một tập hợp hàm调用──梯度被计算、被亚当变换、被应用到参数上全部在`train_step`Trong hoàn thành.

> **【拓展：JAX 的分布式训练】**Bản đồ pmap của JAX có thể tự động phân phối tập luyện trên nhiều thiết bị.`jax.pmap(train_step, axis_name='batch')`Bắt đống tự động chia thành 4 phần, mỗi GPU xử lý một, rồi qua.`jax.lax.pmean`Đồng bước trình độ: Google's TPU Pod có hàng ngàn khối chip, lưới và shard_map của JAX có thể được thực hiện trên hàng ngàn thiết bị.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**JAX 生态的核心库:Flax(Google 的神经网络层库,类似 nn.Module) 方程 (Equinox) 更多 Pythonic 的替代) 、Optax(可组合的优化器库) ⋅Optax 的设计哲学:优化器是梯度变化的链式组合剪 → Adam → 权重衰减,每一步都是独立的变化──

### Lục: Thư viện tiêu chuẩn Google

Flax là thư viện mạng thần kinh JAX phổ biến nhất.`nn.Module`trở lại, nhưng với quản lý nhà nước rõ ràng:

> Lạt là hệ thống truyền thống JAX. Nó được giới thiệu lại.`nn.Module`, nhưng sử dụng quản lý trạng thái rõ ràng:

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

Tương tự như PyTorch, nhưng `params`được tách biệt với mô hình. `model.init()`tạo ra Params. `model.apply(params, x)`chạy đường đi trước. đối tượng mô hình không có trạng thái.

> 结构与 PyTorch 相同, nhưng `params`Với mô hình phân biệt.`model.init()`创建参数――`model.apply(params, x)`运行前向传播──模型对象没有状态──

### Equinox: Phương pháp thay thế Python

Equinox (do Patrick Kidger) đại diện cho các mô hình như các cây pytrees:

> Equinox (由 Patrick Kidger 开发) 将模型表示为 pytree:

```python
import equinox as eqx

model = eqx.nn.MLP(
    in_size=784, out_size=10, width_size=256, depth=2,
    activation=jax.nn.relu, key=jax.random.PRNGKey(0)
)
logits = model(x)
```

Bản thân mô hình là một cây Pytree.`.apply()`Các thông số chỉ là lá của mô hình.

> Mô hình chính nó là một cây.`.apply()`◊ Các số chỉ là một cái lá của mô hình.

### Optax: Composable Optimizers  Optax: có thể được kết hợp

Optax tách chuyển đổi gradient từ bản cập nhật:

> Optax sẽ thay đổi độ với giải thích mới:

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

Giảm gradient, tăng tốc độ học tập, giảm cân - tất cả đều được tạo thành như một chuỗi chuyển đổi. Mỗi chuyển đổi nhìn thấy gradient, sửa đổi chúng, và chuyển chúng sang lớp tiếp theo. Không có lớp tối ưu hóa đơn phương.

> 梯度剪、学习率预热、权重衰减全部作为变换链组合──每个变换看梯度,修改它们,传递给下一个──没有庞大的优化器类──

## Chuyển nó đi.

**Installation:**

```bash
pip install jax jaxlib optax flax
```

Đối với hỗ trợ GPU:

```bash
pip install jax[cuda12]
```

Đối với TPU (Google Cloud):

```bash
pip install jax[tpu] -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
```

**Performance gotchas:**

- Cuộc gọi đầu tiên của JIT là chậm (sự biên soạn).
- Tránh các vòng Python trên các mảng JAX bên trong JIT. Sử dụng `jax.lax.scan`hoặc `jax.lax.fori_loop`- Tôi không biết.
- `jax.debug.print()`làm việc trong JIT.`print()`Không.
- Hình ảnh với `jax.profiler`XLA có thể che giấu những lỗ hổng.
- JAX dự định phân bổ 75% bộ nhớ GPU theo mặc định.`XLA_PYTHON_CLIENT_PREALLOCATE=false`để vô hiệu hóa.

**Checkpointing:**

```python
import orbax.checkpoint as ocp
checkpointer = ocp.PyTreeCheckpointer()
checkpointer.save('/tmp/model', params)
restored = checkpointer.restore('/tmp/model')
```

**This lesson produces:**
- `outputs/prompt-jax-optimizer.md`-- một lời nhắc cho việc chọn đúng cấu hình tối ưu hóa JAX
- `outputs/skill-jax-patterns.md`-- một kỹ năng bao gồm các mô hình chức năng trong JAX

## Tập luyện bài tập

1. Thêm dropup vào MLP. Trong JAX, dropup đòi hỏi một phím PRNG - đinh một phím qua các bước đi phía trước và chia nó cho mỗi lớp dropup. So sánh độ chính xác của thử nghiệm với và ngoài.

2. Sử dụng `jax.vmap`để tính toán gradient cho mỗi ví dụ cho một loạt 32 hình ảnh MNIST. tính toán chuẩn gradient cho mỗi ví dụ. ví dụ nào có gradient lớn nhất, và tại sao?

3. Thay thế hàm hướng về phía trước bằng một hàm chung `mlp_forward(params, x)`Nó có thể hoạt động cho bất kỳ lớp nào.`jax.tree.leaves`để xác định độ sâu tự động.

4. Đánh giá bước đào tạo với và không `@jax.jit`Thời gian 100 bước mỗi lần. tốc độ trên phần cứng của bạn là bao nhiêu?

5. Thực hiện cắt gradient bằng cách tạo `optax.chain(optax.clip_by_global_norm(1.0), optax.adam(1e-3))`Tren với và không cắt, vẽ chuẩn gradient trên tập để xem hiệu quả.

## Từ khóa  Từ khóa nhanh chóng

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

## Xem thêm 延伸阅读

- Tài liệu JAX: https://jax.readthedocs.io/- Các bác sĩ chính thức, với các hướng dẫn tuyệt vời về Graduate, jit, và vmap
  JAX 文档:https://jax.readthedocs.io/官方文档, liên quan đến chương trình tốt nghiệp jit 和 vmap
- "JAX: những biến đổi hợp nhất của các chương trình Python+NumPy" (Bradbury et al., 2018) - bài báo ban đầu giải thích triết lý thiết kế
  Bradbury 等人,JAX:Python+NumPy 程序的可组合变换(2018) 解释设计哲学学的原始论文
- Tài liệu bằng len: https://flax.readthedocs.io/-- Thư viện mạng thần kinh của Google cho JAX
  Flax 文档Google cho JAX  phát triển Neural Network库
- Patrick Kidger, "Equinox: mạng thần kinh trong JAX thông qua PyTrees có thể gọi và chuyển đổi lọc" (2021) - sự thay thế Pythonic cho Flax
  Patrick Kidger,Equinox: thông qua có thể调用 PyTree 和过变换实现 JAX 神经网络(2021)Flax của Pythonic thay thế方案
- DeepMind, "Optax: biến đổi và tối ưu hóa gradient hợp nhất" -- thư viện tối ưu hóa tiêu chuẩn
  DeepMind,Optax:可组合的梯度变换和优化标准优化器库
- "You Don't Know JAX" (Colin Raffel, 2020) - một hướng dẫn thực tế về các trò chơi và mô hình JAX, từ một trong những tác giả của T5
  Colin Raffel,你还不了解JAX(2020)JAX 陷和模式的实用指南,作者为T5 论文作者之一
