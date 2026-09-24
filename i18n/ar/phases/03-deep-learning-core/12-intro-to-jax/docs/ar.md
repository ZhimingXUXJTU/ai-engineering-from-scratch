# مقدمة لـ JAX JAX دخول

> (بيتورش) يُطفر الجهازات العصبية، (تنسور فلو) يُبني الرسومات، (جاكس) يُجمع وظائف نقية، وهذا الأخير يُغير طريقة تفكيرك بشأن التعلم العميق.

> **【中文解读】**PyTorch 可变张量,TensorFlow 静态图,JAX 编译纯函数──JAX 函数式编程范式是深度学习的新方向Google 双子就用JAX 训练──本章学习JAX 的核心:jit 编译、vmap 向量化、grad 自动微分──

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 03 Lessons 01-10, basic NumPy
**Time:** ~90 minutes

## أهداف التعلم

- كتابة رمز شبكة عصبية ذات وظيفة نقية باستخدام API الوظيفية JAX (jax.numpy، jax.grad، jax.jit، jax.vmap)
- شرح الفرق الرئيسية في التصميم بين طفرة PyTorch المهتمة ونموذج تجميع وظيفي JAX
- تطبيق تجميع jit و vmap التنقل لتسريع حلقات التدريب مقارنة مع بيثون ساذجة
- تدريب شبكة بسيطة في JAX وتقارن إدارة الحالة الصريحة مع نهج PyTorch المتحرك على الكائن

> **【中文解读】**本章学习 JAX的函数式编程范式──与 PyTorch的核心区别:没有可变状态、没有 .后退()、没有 nn.Module──一切通过函数变换实现:jax.grad 计算梯度、jax.jit 编译加速、jax.vmap 自动向量化──Google Gemini 和人类克劳德都使用 JAX 训练──

## المشكلة المشكلة المشكلة

أنت تعرف كيفية بناء شبكات عصبية في PyTorch.`nn.Module`، اتصل`.backward()`،إضغط على المحفّظ، إنه يعمل، ملايين الناس يستخدمونها

> أنت تعرف كيفية بناء شبكة عصبية في PyTorch.`nn.Module`,调用 `.backward()`, تدخل في تحسيناتها.

لكن (بيتورش) لديه قيود في حمض النووي: يتتبع العمليات بحماس، واحدة في كل مرة، في (بايتون).`tensor + tensor`كل خطوة تدريبية تعيد تفسير نفس رمز Python هذا يعمل بشكل جيد حتى تحتاج إلى تدريب نموذج بمليارات 540 على 2048 TPU ثم التكلفة العليا تقتلك

> لكن هناك قيود في حمض النووي لـ (بيتورش): إنه يقوم بتتبع عمليات التتبع بشكل سريع، باستخدام (بايتون)`tensor + tensor`كل خطوة تدريبية تعيد تفسير نفس رمز بايثون. هذا يتطلب من خلال 2,048 TPU تدريب 5400 مليار نموذج العاملات قبل كل شيء يمكن أن يعمل. ثم التسويق سوف يقتلك.

غوجل ديب ميند تدرب جيمين على جياكس. علمت أنتروبيك كلود على جياكس. هذه ليست عمليات صغيرة - إنها أكبر عمليات تدريب شبكة عصبية على الأرض. اختاروا جياكس لأنه يعامل حلقة التدريب الخاصة بك كبرنامج قابل للتجميع، وليس تسلسل من مكالمات بيثون.

> Google DeepMind باستخدام JAX  تدريب Gemini. Anthropic باستخدام JAX  تدريب كلود. هذه ليست عمليات صغيرة الحجم. إنها أكبر شبكة عصبية على الأرض. اختاروا JAX لأنها تعتبر دورة تدريبك كبرنامج قابل للتجميع، وليس سلسلة من Python 调用.

JAX هو NumPy مع ثلاثة قوى خارقة: التمييز التلقائي، تجميع JIT إلى XLA، والمتصفح التلقائي. تكتب وظيفة التي تعالج مثال واحد. JAX يعطيك وظيفة التي تعالج مجموعة، وحسب التراجع، وتقوم بتجميعها إلى رمز الآلة، وتشغيل عبر أجهزة متعددة. كل ذلك دون تغيير الوظيفة الأصلية.

> JAX هو لديه ثلاثة قدرات فائقة من NumPy: التشغيل الآلي و التقييم الآلي. يمكنك كتابة عمل معين واحد. JAX يمنحك عملية معالجة واحدة.

> **【中文解读】**حدود PyTorch: كل تدريب يعيد تفسير Python 代码، كل تنسور 运算都是 محور منفصل 启动。 في 2048 بلاك TPU 上训练 540B 参数模型, هذا التسويق غير مقبول。JAX 把训练循环编译成机器码,跳过 Python 层,直接运行在加速器上──

> **【拓展：JAX 的工业应用】**Google DeepMind باستخدام JAX  تدريب Gemini(أكبر إصدار حسب التقاليد تزيد عن 1T 参数)。Anthropic باستخدام JAX  تدريب كلود 系列。Google's AlphaFold 2/3 أيضا باستخدام JAX。

## المفهوم الأساسي

### فلسفة جياكس

JAX هو إطار عمل لا فئات ولا حالة متغيرة لا`.backward()`الطريقة بدلاً من ذلك:

> JAX هو إطار عمل.`.backward()`方法──取而代之 هي:

| PyTorch | JAX |
|---------|-----|
| `nn.Module` class with state | Pure function: `f(params, x) -> y` |
| `loss.backward()` | `jax.grad(loss_fn)(params, x, y)` |
| Eager execution | JIT compilation via XLA |
| `for x in batch:` manual loop | `jax.vmap(f)` auto-vectorization |
| `DataParallel` / `FSDP` | `jax.pmap(f)` auto-parallelism |
| Mutable `model.parameters()` | Immutable pytree of arrays |

هذه ليست تفضيل الأسلوب. إنها قيود للمؤلف. تجميع JIT يتطلب وظائف نقية -- نفس المدخلات دائما تنتج نفس المخرجات، لا آثار جانبية. هذا القيود هو ما يجعل 100x السرعة ممكنة.

> هذا ليس من المفضلات الرائقة. هذا هو الحد الأقصى للجهاز المُعدّل.

> هذا ليس من المفضلات الرائقة. هذا هو الحد الأقصى للجهاز المُعدّل.

### جاكس: المعرفي السطح

يقوم JAX بإعادة تنفيذ API NumPy على المسارع:

```python
import jax.numpy as jnp

a = jnp.array([1.0, 2.0, 3.0])
b = jnp.array([4.0, 5.0, 6.0])
c = jnp.dot(a, b)
```

نفس أسماء الوظائف نفس قواعد البث نفس النقشة الزمنية ولكن المجموعات تعيش على GPU / TPU وكل عملية تتبع بواسطة المُحْتَرِك

> نفس اسم الوظيفة. نفس قواعد الإعلان. نفس القسم. ولكن في GPU / TPU، كل عملية يمكن تعقبها بواسطة المُعدل.

الفرق الحاسم واحد: صفوف JAX غير قابلة للتغيير.`a[0] = 5`بدلاً من ذلك:`a = a.at[0].set(5)`هذا يشعرني بالشعور الحرج لمدة أسبوع، ثم يضغط -- عدم التغيير هو ما يجعل التحولات مثل`grad`،`jit`و`vmap`قابلة للتحكم

> واحد المفتاح: JAX عدد المجموعات لا يمكن تغييرها.`a[0] = 5`ولكن لا تستخدم`a = a.at[0].set(5)`أولاً سأشعر بالتحول ثم سأدرك أن هذا هو الأمر`grad`.`jit`和 `vmap`等变换可组合的基础──

### jax.grad: التشغيل الذاتي التشغيلي

يربط PyTorch المراجع إلى الجهاز (`.grad`JAX يربط التراجع بالعملات

> سيتم زيادة درجة (PyTorch) إلى (张量上)`.grad`.♦ JAX سوف تدرجة إضافة إلى وظيفة على♦

```python
import jax

def f(x):
    return x ** 2

df = jax.grad(f)
df(3.0)
```

`jax.grad`يأخذ وظيفة ويرد وظيفة جديدة تحسب التراجع. لا `.backward()`لا يوجد مخطط حساب مخزن على الجهاز التنسوري. التراجع هو مجرد وظيفة أخرى يمكنك الاتصال، أو إعداد، أو JIT-إعداد.

> `jax.grad`接收一个函数,返回一个计算梯度的新函数──不需要 `.backward()`调用──张量上不存储计算图──梯度只是另一个你可以调用、组合或JIT 编译的函数──

هذا يشكّل بشكل تعسفي:

> يمكن أن تكون أي مجموعة:

```python
d2f = jax.grad(jax.grad(f))
d2f(3.0)
```

المشتقات الثانية المشتقات الثالثة الجيكوبيون الهيسيون كل ذلك من خلال التركيب`grad`(بيتورش) يمكنه فعل هذا أيضاً`torch.autograd.functional.hessian`في JAX، هو الأساس.

> ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية. ثانوية.`grad`实现──PyTorch 也能做(`torch.autograd.functional.hessian`لكنّه إضافاتٌ لاحقة.

القيود:`grad`لا توجد بيانات مطبوعة داخل (تتم تشغيلها أثناء التتبع وليس التنفيذ). لا توجد طفرة في الحالة الخارجية. لا توجد إنتاج أرقام عشوائية دون إدارة مفتاح صريحة.

> الحد:`grad`لا يمكن استخدامها في وظائف نقية. لا يمكن أن يكون هناك طباعة في الداخل.

> **【拓展：JAX 的 grad vs PyTorch 的 autograd】**بيتورش وضع梯度 وجود تنسور 上(x.grad) ، JAX وضع梯度看作函数的输出── هذا يعني JAX 天然支持高阶导数(grad((((f)) ، بينما بيتورش 需要特殊处理──`jax.hessian(f)`, بيتورش  أحتاج `torch.autograd.functional.hessian`.

### قم بتجميعها إلى XLA

```python
@jax.jit
def train_step(params, x, y):
    loss = loss_fn(params, x, y)
    return loss

fast_step = jax.jit(train_step)
```

في المكالمة الأولى، تتبع JAX الوظيفة -- تسجل العمليات التي تحدث، دون تنفيذها. ثم تمنح ذلك التتبع إلى XLA (الجيبر الخطوي المتسارع) ، محفز جوجل لـ TPUs و GPUs. XLA يدمج العمليات، يزيل نسخة ذاكرة زائدة، ويولد رمز آلة محسن.

> في أول مرة، يُسجل وظيفة التتبع JAX ما حدث، دون تنفيذ عملياتها. ثم يُسلم التتبع إلى XLA، Google تطور TPU و GPU.

المكالمات اللاحقة تتجاوز Python بالكامل. يتم تشغيل الكود المجمّع على المسرّع بسرعة C ++.

> 后续调用完全跳过Python──编译后代码以C++ 速度运行在加速器上──

عندما يساعد JIT:

> المشهد المفيد:

- خطوات التدريب (تكرر نفس الحساب آلاف المرات)
  中文翻译: تدريب步骤(相同计算重复数千次)
- الإستدلال (الموديل نفسه، المدخلات المختلفة)
  中文翻译:推理(相同模型,不同输入)
- أي وظيفة تُدعى أكثر من مرة مع مدخلات ذات شكل مماثل
  中文翻译: أي وظيفة في شكل مشابه

عندما يؤلم الجيت:

> المشهد المضايق:

- وظائف مع تدفق التحكم في Python التي تعتمد على القيم (`if x > 0`حيث x هو صف متتبع)
  中文翻译:包含依赖值的 Python 控制流的函数(`if x > 0`من بينها x هو عدد من المتعقبين)
- الحسابات المقطوعة الواحدة (تكلفة التجميع العلوية تتجاوز وقت التشغيل)
  中文翻译:一次性计算 (التي تُعَدُّ على التسجيل)
- إزالة الأخطاء (التتبع يخفي التنفيذ الفعلي)
  中文翻译:调试(追踪隐藏了实际执行)

قيود تدفق التحكم حقيقية`jax.lax.cond`يُستبدل`if/else`. .`jax.lax.scan`يُستبدل`for`هذه ليست اختياريّة، إنها ثمن التجميع.

> الحد من التدفقات هو حقيقي`jax.lax.cond`替代 `if/else`.`jax.lax.scan`替代 `for`هذه ليست خياراتهم هي تكلفة الترجمة

### vmap: التنقل الآلي

تكتب وظيفة تعالج مثال واحد:

> أنت كتب وظيفة معالجة نموذج واحد:

```python
def predict(params, x):
    return jnp.dot(params['w'], x) + params['b']
```

`vmap`يرفعه لتحويل دفعة:

```python
batch_predict = jax.vmap(predict, in_axes=(None, 0))
```

`in_axes=(None, 0)`الوسائل: لا تتعب`params`(مشتركة) ، اللحظة فوق محور 0 من `x`لا دليل`for`لا تشكيل إعادة تشكيل، لا خيوط بعدة دفعة، يحدد JAX بعدة دفعة ويتم تحديد الحساب بأكمله

> `in_axes=(None, 0)`表示: لا对 `params`进行批处理(共享) ،对 `x` التدريبات المختلفة`for`循环──无需重塑──无需手动传递批量维度──JAX自动查出批量维度并向量化整个计算──

هذا ليس سكرًا صيغيًا`vmap`يخلق رمز متجه مزامج يعمل 10-100 مرة أسرع من حلقة Python. ويتكون من`jit`و`grad`:

> هذا ليس لغة "سكر"`vmap`كودات التجميع المتعدد، أكثر من بيثون 循环快 10-100 倍.`jit`和 `grad`组合:

```python
per_example_grads = jax.vmap(jax.grad(loss_fn), in_axes=(None, 0, 0))
```

على سبيل المثال، خط واحد، هذا مستحيل تقريباً في (بيتورش) بدون حوادث

> 逐样本梯度──一行代码── هذا تقريبا مستحيل لاستخدام المهارات في PyTorch

### pmap: مواصلة البيانات عبر الأجهزة

```python
parallel_step = jax.pmap(train_step, axis_name='devices')
```

`pmap`يكرر الوظيفة عبر جميع الأجهزة المتاحة (GPUs / TPUs) ويقسّم المجموعة. داخل الوظيفة، `jax.lax.pmean`و`jax.lax.psum`التزامن بين التراجع بين الأجهزة.

> `pmap`سوف تقوم بتكرار الوظيفة إلى جميع الأجهزة المتاحة على GPU / TPU ، و تمزيقها إلى الجملة.`jax.lax.pmean`和 `jax.lax.psum`عبر الجهاز مع التقدم درجة

جوجل تدرب التوأم عبر آلاف رقائق TPU v5e باستخدام `pmap`(و خليفته)`shard_map`النموذج التخطيطي: كتابة نسخة جهاز واحد، وترتيبها`pmap`لقد انتهى

> استخدام جوجل`pmap`(ومتابعيها)`shard_map`) على آلاف الكتل من TPU v5e 芯片 على تدريب Gemini。编程模型:写单设备版本,用 `pmap`الحزمة، الانتهاء.

### بيترز: هيكل البيانات العالمي بيترز: هيكل البيانات العام

يعمل JAX على "شجرة البيترا" -- مزيجات متجمعة من القوائم والجماعات والقوائم والصفوف.

> JAX 操作"Pytree"列表、元组、字典和数组的嵌套组合── your model parameters is one pytree:

```python
params = {
    'layer1': {'w': jnp.zeros((784, 256)), 'b': jnp.zeros(256)},
    'layer2': {'w': jnp.zeros((256, 128)), 'b': jnp.zeros(128)},
    'layer3': {'w': jnp.zeros((128, 10)),  'b': jnp.zeros(10)},
}
```

كل تحول من (جاكس)`grad`،`jit`،`vmap`-يعرف كيف يعبر الشجرة`jax.tree.map(f, tree)`يطبق`f`هكذا يقوم المحسنون بتحديث جميع المعلمات في وقت واحد:

> كلّ جاكس`grad`.`jit`.`vmap`都知道如何穿越普特ree‬`jax.tree.map(f, tree)`ستعمل`f`تطبيق إلى كل ورقة. هذا هو الطريقة التي يُحسن بها المُعدّل مرة واحدة كل العناصر:

```python
params = jax.tree.map(lambda p, g: p - lr * g, params, grads)
```

لا , لا`.parameters()`لا يوجد تسجيل لمعلمات، بنية الشجرة هي النموذج

> لا يوجد`.parameters()`方法──没有参数注册──树结构就是模型──

### وظيفي مقابل موضوعي المتحور

مخازن PyTorch تصريح داخل الأشياء:

```python
class Model(nn.Module):
    def __init__(self):
        self.linear = nn.Linear(784, 10)

    def forward(self, x):
        return self.linear(x)
```

JAX يستخدم وظائف نقية مع حالة صريحة:

```python
def predict(params, x):
    return jnp.dot(x, params['w']) + params['b']
```

يتم نقل المعلمات. لا يتم تخزين أي شيء. لا يوجد شيء يتغير. وهذا يجعل كل وظيفة قابلة للتحقق، قابلة للتكوين، ويمكن تجميعها. وهذا يعني أيضًا أنك تدير المعلمات بنفسك - أو تستخدم مكتبة مثل فلانكس أو إيكوينوكس.

> يتم نقل العناصر إلى داخلها. لا تخزين أي شيء. لا تغيير أي شيء. هذا يجعل كل وظيفة قابلة للاختبار.

### نظام جيكس البيئي

"جاكس" يعطيك البدائية، والمكتبات تعطيك التجربة

> JAX 提供原语──库提供便利性:

| Library | Role | Style |
|---------|------|-------|
| **Flax** (Google) | Neural network layers | `nn.Module` with explicit state |
| **Equinox** (Patrick Kidger) | Neural network layers | Pytree-based, Pythonic |
| **Optax** (DeepMind) | Optimizers + LR schedules | Composable gradient transforms |
| **Orbax** (Google) | Checkpointing | Save/restore pytrees |
| **CLU** (Google) | Metrics + logging | Training loop utilities |

أوبتاكس هو مكتبة المحفز القياسي. فإنه يفصل تحويل التراجع (أدام، SGD، قطع) من تحديث المعلمات، مما يجعل من غير المهم أن تكوين:

> الاختيار هو المعدات المعيارية المعدة. سوف تغير درجة التغيير (أدم، SGD، خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيارات خيار

```python
optimizer = optax.chain(
    optax.clip_by_global_norm(1.0),
    optax.adam(learning_rate=1e-3),
)
```

### متى تستخدم (جاكس) مقابل (بيتورش) ؟

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

الجواب الصادق: استخدم PyTorch ما لم يكن لديك سبب محدد لاستخدام JAX. هذه الأسباب هي -- وصول TPU، الحاجة إلى تراجع لكل مثال، تدريب متعدد الأجهزة على نطاق واسع، أو العمل في Google / DeepMind / Anthropic.

> 诚实的答案: ما لم يكن هناك سبب محدد، وإلا استخدام PyTorch.

### أرقام عشوائية في JAX عدد عشوائي في JAX

لا يوجد في JAX حالة عشوائية عالمية. كل عملية عشوائية تتطلب مفتاح PRNG صريح:

> JAX  ليس لديها حالة كلية كليا 

```python
key = jax.random.PRNGKey(42)
key1, key2 = jax.random.split(key)
w = jax.random.normal(key1, shape=(784, 256))
```

هذا مزعج في البداية، لكنه يضمن إعادة التأهيل عبر الأجهزة والجمعات -- خاصية التي يستخدمها PyTorch`torch.manual_seed`لا يمكن أن تضمن في إعدادات متعددة GPU.

> بدأ الأمر مشاكل جداً ولكن هذا يضمن التطبيقات والتحرير`torch.manual_seed`في بيئة متعددة من المستخدمين غير مؤكدة
```figure
batchnorm-effect
```

## بناءها

## بناء ذلك تحرك لتحقيق

> **【中文解读】**استخدام JAX + Optax 訓練 MNIST 分类器──注意和 PyTorch 的关键区别:没有 nn.Module、参数用嵌套字典(pytree) مخزن、 تدريب步骤是纯函数用 @jax.jit 编译、没有 .zero_grad() /.backward() /.step() 梯度计算和参数更新合并在一个函数中──

### الخطوة الأولى: الإعداد والبيانات الخطوة الأولى: الإعدادات والبيانات

سنقوم بتدريب 3 طبقات من المعلمين على نظام التعلم المختص بالمنظمة باستخدام JAX و Optax 784 مدخلات، طبقتين مخفيتين من 256 و 128 عصبية، 10 فصول خروج.

> سنستخدم JAX و Optax في MNIST لتدريب 3 طبقات MLP―784 إدخال، اثنين من 256 و 128 طبقة مخبأة من العصب، 10 طبقات إخراج

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

### الخطوة الثانية: إعادة تشغيل المعايير

لا يوجد فئة، مجرد وظيفة تعيد ثمرة:

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

يبدأ بإعداد المفاتيح اليدوية ثلاثة مفاتيح PRNG منفصلة من بذرة واحدة كل وزن هو صف غير قابل للتغيير في إصدار مقيم

> يدخل المكتملة. إنه الأولويات. ثلاثة مفاتيح PRNG من فصل واحد من البذور. كل وزن هو عدد لا يتغير في الكتب المكتوبة.

### الخطوة الثالثة: التسلل إلى الأمام

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

وظائف نقية، إدخال المعلمات، تنبؤ خارج.`self`لا يوجد حالة تخزين`loss_fn`يحسب الانتروبيا المتقاطعة من الصفر -- softmax، log، متوسط سلبي.

> 純函数──参数进,预测出──没有 `self`لا يوجد حالة تخزين`loss_fn`من رأس حساب交叉softmax、log、负平均值。

### الخطوة الرابعة: خطوة التدريب المجمعة من JIT

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

`jax.value_and_grad`يعيد قيمة الخسارة والتحركات في مرور واحد.`@jax.jit`يقوم المعدل بتجميع كل من الوظائف إلى XLA. بعد الدعوة الأولى، يتم تشغيل كل خطوة تدريبية دون لمس Python.

> `jax.value_and_grad`في وقت واحد من الانتشار في نفس الوقت العودة إلى الخسارة والدرجة.`@jax.jit`سوف يقوم المعدات بتحويل وظيفتين إلى XLA. بعد أول تدوين، كل خطوة تدريبية لا تتصل بـ Python.

### الخطوة 5: حلقة التدريب

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

10 أوقات. ~ 97٪ دقة الاختبار. الأوقات الأولى بطيئة (جميع JIT). أوقات 2-10 سريعة.

> 10 个时代──~97% 测试准确率──第一个时代 较慢(JIT 编译)──第 2-10 个时代 很快──

لاحظ ما يفتقد: لا`.zero_grad()`لا , لا`.backward()`لا , لا`.step()`التحديث كله هو دعوة عمل واحد مركب. يتم حساب المعدلات، وتحوّلها من قبل آدم، وتطبيقها على المعلمات -- كل شيء داخل`train_step`. . .

> انتبه إلى ما فات`.zero_grad()`لا يوجد`.backward()`لا يوجد`.step()` الإصلاح كله هو مجموعة من وظائف المستخدمة.`train_step`إنهُ تمّ إنجازه

> **【拓展：JAX 的分布式训练】**خريطة pmap JAX يمكن تزويد التدريبات بشكل تلقائي على العديد من الأجهزة.`jax.pmap(train_step, axis_name='batch')`سوف تقوم بتقسيم المجموعة بشكل تلقائي إلى أربعة أجزاء ، كل قطعة من الجيبو`jax.lax.pmean`مع التسلسلات: Google TPU Pod لديه آلاف الكتل من الشرائح، وJAX الشبكة و shard_map يمكن أن تكون على آلاف الأجهزة وتعمل على النموذج.

## استخدمها في إطار التنفيذ

> **【中文解读】**المجموعة الأساسية للنظام JAX 生态:Flax(Google's Neural Network Layer Library, similar to nn.Module) √Equinox(更 Pythonic 的替代) √Optax(可组合的优化器库) √Optax's design philosophy:优化器是梯度变化的链式组合剪 → آدم → 权重衰减,每一步都是独立的变化──

### فالنس: قاعدة بيانات جوجل

فلانكس هو المكتبة الأكثر شيوعا للشبكة العصبية JAX.`nn.Module`ولكن مع إدارة دولية صريحة:

> فلانكس هو الأكثر استخداماً في قاعدة JAX النبيوية.`nn.Module`، ولكن باستخدام إدارة الحالة الواضحة:

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

نفس الهيكل مثل (بيتورش) ، لكن`params`هو منفصل عن النموذج. `model.init()`يخلق "بارام".`model.apply(params, x)`يُجري المُسلّم الأمامي، وكلّ هذا المُسلّم لا يملك حالة.

> 结构与 PyTorch 相同,但 `params`مع النموذج`model.init()`创建参数──`model.apply(params, x)`运行前向传播──模型对象没有状态──

### الإستثمار: البديل البايتوني

يمثل الإيكنوكس (من قبل باتريك كيدجر) النماذج كثلاثة أشجار:

> الإيقونوس (بالإنجليزية: Equinox) بواسطة Patrick Kidger 开发)

```python
import equinox as eqx

model = eqx.nn.MLP(
    in_size=784, out_size=10, width_size=256, depth=2,
    activation=jax.nn.relu, key=jax.random.PRNGKey(0)
)
logits = model(x)
```

النموذج نفسه هو شجرة`.apply()`هذه أقرب إلى طريقة تفكير جياكس

> الموديل نفسه هو شجرة`.apply()`العنصر مجرد ورقة النموذج.

### أوتتاكس: محفزات تحسينات قابلة للتكوين

أوتتاكس يقطع صيغة التحول من التحديث:

> التطبيقات ستقوم بتغيير التدريج مع تحديث解:

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

قطع التدرج، ارتفاع معدل التعلم، تدهور الوزن -- كل ذلك مركب كسلسلة من التحولات. كل تحويل يرى التدرج، يغيره، ويمر به إلى التالي. لا يوجد فئة تحسينات واحدة.

> 梯度剪、学习率预热、权重衰减全部作为变换链组合──每个变化看梯度,修改它们,传递给下一个──没有巨大的优化器类──

## أرسلها .

**Installation:**

```bash
pip install jax jaxlib optax flax
```

لدعم GPU:

```bash
pip install jax[cuda12]
```

بالنسبة لـ TPU (Google Cloud):

```bash
pip install jax[tpu] -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
```

**Performance gotchas:**

- أول مكالمة JIT بطيئة (التجميع) ، احترق قبل تقييم الموازنة.
- تجنب حلقات Python على صفوف JAX داخل JIT. استخدم `jax.lax.scan`أو`jax.lax.fori_loop`. . .
- `jax.debug.print()`يعمل داخل JIT.`print()`لا يُمكنك ذلك
- الملف الشخصي مع `jax.profiler`أو TensorBoard. تجميع XLA يمكن أن تخفي ضباب الزجاجة.
- JAX يخصص 75٪ من ذاكرة GPU من قبل افتراضي.`XLA_PYTHON_CLIENT_PREALLOCATE=false`لتعطيل.

**Checkpointing:**

```python
import orbax.checkpoint as ocp
checkpointer = ocp.PyTreeCheckpointer()
checkpointer.save('/tmp/model', params)
restored = checkpointer.restore('/tmp/model')
```

**This lesson produces:**
- `outputs/prompt-jax-optimizer.md`-- طلب لتحديد التكوين المناسب لشركة JAX
- `outputs/skill-jax-patterns.md`-- مهارة تغطي أنماط وظيفية في JAX

## تمارين التدريب

1. إضافة التوقف إلى MLP. في JAX، يتطلب التوقف مفتاح PRNG -- خيط مفتاح من خلال الممر الأمامي وتقسيمه لكل طبقة التوقف. مقارنة دقة الاختبار مع وخارج.

2. استخدام`jax.vmap`لتحديد تراجع لكل مثال لـ 32 صورة من MNIST. احسب معايير تراجع لكل مثال. أي أمثلة لديها أكبر تراجع، ولماذا؟

3. استبدل وظيفة الإستعراض اليدوية بالظروف العامة`mlp_forward(params, x)`يعمل على أي عدد من الطبقات. استخدم `jax.tree.leaves`لتحديد العمق تلقائيًا.

4. قم بتحديد خطوة التدريب مع و بدون`@jax.jit`كم عدد التسريع على أجهزةك؟ ما هو تكلفة التجميع على المكالمة الأولى؟

5. تنفيذ قطع التراجع عن طريق التركيب `optax.chain(optax.clip_by_global_norm(1.0), optax.adam(1e-3))`تدريب مع و بدون قطع رسم معايير التراجع فوق التدريب لمعرفة التأثير

## شروط الرئيسية

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

## المزيد من القراءة

- وثائق JAX: https://jax.readthedocs.io/- الأدب الرسمي، مع دروس ممتازة على درجة، jit، و vmap
  JAX 文档:https://jax.readthedocs.io/文档, حول درجات jit 和 vmap
- "جاكس: تحولات قابلة للتكوين من برامج بايثون+نومبي" (برادبري وآخرون، 2018) -- الورقة الأصلية التي تشرح فلسفة التصميم
  برادبري 等人,JAX:بايتون+نومبي 程序的可组合变换(2018) 解释设计哲学学的原始论文
- وثائق من الكتان: https://flax.readthedocs.io/-- مكتبة شبكة عصبية جوجل لل JAX
  فلانكس 文档 谷歌为JAX 开发 神经网络库
- باتريك كيدجر، "الإنكوانوكس: شبكات عصبية في JAX عبر PyTrees المزعومة والتحولات المصفاة" (2021) -- البديل البايتوني للفني
  باتريك كيدجر،Equinox: من خلال قابل للتدويل PyTree و 过变换实现 JAX 神经网络(2021) Flax  Pythonic 替代方案
- ديب ميند، "أوبتاكس: تحويل وتحسين التراجع المتكامل" -- مكتبة المحسن القياسي
  DeepMind,Optax:可组合的梯度变换和优化标准优化器库
- "أنت لا تعرف جياكس" (كولين رافيل، 2020) -- دليل عملي على جاكس gotchas والأنماط، من أحد مؤلفي T5
  كولين رافيل،أنت لا تعرف أيضا JAX(2020)JAX 陷和模式的实用指南,作者为T5 论文作者之一
