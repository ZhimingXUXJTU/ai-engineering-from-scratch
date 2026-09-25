# JAX giriş.

> PyTorch tensorları mutasyonlandırır. TensorFlow grafikler oluşturur. JAX saf fonksiyonları oluşturur. Sonuncusu derin öğrenme hakkında düşüncelerinizi değiştirir.

> **【中文解读】**PyTorch 可变张量,TensorFlow 静态图,JAX 编译纯函数──JAX'ın işlevi biçimli programlama biçimi derin öğrenmenin yeni yönüGoogle'un Gemini JAX 训练──本章学习 JAX'in çekirdeği:jit 编译、vmap 向量化、grad 自动微分──

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 03 Lessons 01-10, basic NumPy
**Time:** ~90 minutes

## Öğrenme hedefleri

- JAX'in işlevsel API'si (jax.numpy, jax.grad, jax.jit, jax.vmap) kullanarak saf işlevli sinir ağ kodu yazın
- PyTorch'ın coşkulu mutasyonu ile JAX'in fonksiyonel bir komile modeli arasındaki temel tasarım farkını açıklayın.
- Naif Python'a kıyasla eğitim döngüslerini hızlandırmak için jit kompiliasyonu ve vmap vektörleştirmesini uygulayın
- JAX'de basit bir ağ eğit ve açık durum yönetimini PyTorch'ın nesne odaklı yaklaşımı ile karşılaştır

> **【中文解读】**Bu bölümde JAX'in işletim biçiminin programlanması için bir bölüm çalışıyorum.

## Sorunlar. Sorunlar.

PyTorch'te sinir ağlarını nasıl inşa edeceğinizi biliyorsunuz.`nn.Module`- Arayın .`.backward()`Milyonlarca insan kullanıyor.

> PyTorch'te nasıl bir sinir ağı oluşturacağınızı biliyorsunuz.`nn.Module`,调用 `.backward()`, step into optimization. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

Ama PyTorch'in DNA'sına bir kısıtlama girdi: Python'da operasyonları birer birer seve izliyor.`tensor + tensor`Bu, 540 milyar parametrelik bir modelin 2.048 TPU'da eğitilmesi gerektiği sürece iyi çalışır.

> Fakat PyTorch'in DNA'sında bir sınırlama var: Python'la hızlı bir şekilde takip ediliyor.`tensor + tensor`Tüm bunlar tek bir çekirdek başlatma aşamasıdır. Her bir eğitim aşamasında aynı Python kodunun yeniden yorumlanması gerekir.

Google DeepMind, Gemini'yi JAX'de eğitir. Anthropic Claude'u JAX'de eğitmiştir. Bunlar küçük operasyonlar değil, bunlar Dünya'daki en büyük sinir ağı eğitim sürümleri. JAX'i seçtiler çünkü eğitim döngüsünü Python çağrılarının bir dizi değil, bir yapılandırılabilir program olarak değerlendirir.

> Google DeepMind JAX'i kullanarak Gemini'yi eğitmektedir. Antropik JAX'i kullanarak Claude'u eğitmektedir. Bunlar küçük ölçekli işlemler değildir. Dünyadaki en büyük sinir ağı eğitimleri.

JAX, NumPy'yi üç süper güçle oluşturur: otomatik farklılaşma, JIT'in XLA'ya birleştirilmesi ve otomatik vektörleştirme. Bir örneği işleyen bir işlevi yazarsınız. JAX size bir partiyi işleyen, gradientleri hesaplayan, makine koduna birleştiren ve birden fazla cihazda çalıştırılan bir işlevi verir.

> JAX üç süper kapasiteye sahip NumPy: otomatik parçacık、JIT  XLA ile otomatik boyutlandırma olarak düzenlenir.

> **【中文解读】**PyTorch'in sınırları: Her antrenman Python kodunu yeniden açıklıyor, her tensor 运算都是单独的内核 启动──在2048 块 TPU 上训练 540B 参数模型时,这个开销不可接受──JAX 练循环编译成机码,跳过Python层,直接在加速器上运行──

> **【拓展：JAX 的工业应用】**Google DeepMind JAX  eğitimi Gemini(最大版本据传超过1T 参数) ・・・Anthropic JAX  eğitimi Claude 系列。Google's AlphaFold 2/3 is also using JAX。JAX'in avantajları süper büyük ölçekli dağılımı eğitiminde: pmap ile binlerce blok TPU üzerinde otomatik olarak yürüyüşe, shard_map ile model yapma işlemesine。 ama JAX'in düzenleme zorluğu PyTorch'den çok daha yüksek。

## Konsepten bir şey.

### JAX'in tasarım felsefesi.

JAX, işlevsel bir çerçeve.`.backward()`- Bu yöntem yerine:

> JAX bir fonksiyonel çerçeve.`.backward()`方法──取而代之 şunlardır:

| PyTorch | JAX |
|---------|-----|
| `nn.Module` class with state | Pure function: `f(params, x) -> y` |
| `loss.backward()` | `jax.grad(loss_fn)(params, x, y)` |
| Eager execution | JIT compilation via XLA |
| `for x in batch:` manual loop | `jax.vmap(f)` auto-vectorization |
| `DataParallel` / `FSDP` | `jax.pmap(f)` auto-parallelism |
| Mutable `model.parameters()` | Immutable pytree of arrays |

Bu bir stil tercih değil. Bu bir kompilatör kısıtlaması. JIT komisyonu saf işlevler gerektirir - aynı girişler her zaman aynı çıkışlar üretir, yan etkileri yoktur. Bu kısıtlama 100 kat hızlandırmayı mümkün kılan şeydir.

> Bu bir biçim tercih değildir. Bu bir düzenlemeci bir kısıtlama. JIT  düzenleme tam bir işlevi gerektirir. Aynı giriş, aynı çıkış ve yan etkileri yoktur. Bu kısıtlama, mümkün olma sebebidir.

> Bu bir biçim tercih değildir. Bu bir düzenlemeci bir kısıtlama. JIT  düzenleme tam bir işlevi gerektirir. Aynı giriş, aynı çıkış ve yan etkileri yoktur. Bu kısıtlama, mümkün olma sebebidir.

### - Tanıdık yüzey.

JAX NumPy API'sini hızlandırıcılarda yeniden uyguluyor:

```python
import jax.numpy as jnp

a = jnp.array([1.0, 2.0, 3.0])
b = jnp.array([4.0, 5.0, 6.0])
c = jnp.dot(a, b)
```

Aynı işlev isimleri, aynı yayın kuralları, aynı kesim semantikası ama diziler GPU/TPU'da canlı ve her işlem kompiliör tarafından izlenebilir.

> Aynı işlevi adı. Aynı yayın kuralları. Aynı parçalar. Ama GPU/TPU'da, her işlem, bir çevirmen tarafından takip edilebilir.

Tek önemli fark: JAX dizileri değişmez.`a[0] = 5`Bunun yerine:`a = a.at[0].set(5)`Bu bir hafta boyunca garip geliyor, sonra da basıyor-- değişmezlik dönüşümleri böyle yapar.`grad`- Evet .`jit`ve`vmap`- Düzgün.

> Bir anahtar fark:JAX sayıları değişmez.`a[0] = 5`Ama kullanıyorum.`a = a.at[0].set(5)`Birden değişmeye başlayacak, sonra da değişmeyeceğini anlayacaksın.`grad`- Evet.`jit`和 `vmap`Çözülebilir bir temel oluşturmak için.

### - Bu da bir işlev.

PyTorch gradientleri tenzorlara bağlar (`.grad`JAX fonksiyonlara gradient bağlar.

> PyTorch'in ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı ı                   `.grad`)―JAX, işlevi için bir derece ekleyecektir.

```python
import jax

def f(x):
    return x ** 2

df = jax.grad(f)
df(3.0)
```

`jax.grad`Bir fonksiyonu alır ve gradiyenti hesaplayan yeni bir fonksiyonu gönderir.`.backward()`Tansörlerde depolanmış hesaplama grafikleri yok. gradient sadece bir başka fonksiyon, çağırabilir, yazabilir veya JIT-kompile edebilirsiniz.

> `jax.grad`Bir işlevi al, bir hesaplama derecesinin yeni işlevi geri getir.`.backward()`调用──张量上不存储计算图──梯度只是另一个你可以调用、组合或JIT 编译的函数──

Bu, keyfi bir şekilde oluşturuyor:

> Bu herhangi bir kombinasyon olabilir:

```python
d2f = jax.grad(jax.grad(f))
d2f(3.0)
```

İkinci türevler, üçüncü türevler, Yakobyanlar, Hessyanlar, hepsi de bir araya gelerek.`grad`PyTorch bunu da yapabilir.`torch.autograd.functional.hessian`JAX'de, temel oluşturur.

> İki aşama. Üç aşama.`grad`实现──PyTorch 也能做(`torch.autograd.functional.hessian`Ama bu bir artış. JAX'de bu temel.

Zorluk:`grad`Bu işlemler sadece saf fonksiyonlarda çalışır. İçinde baskı açıklamaları yoktur (içinde izleme sırasında çalıştırılır, çalıştırılmaz). Dış durum mutasyonları yoktur. Açık bir anahtar yönetimi olmadan rastgele sayı üretimi yoktur.

> 限制:`grad`Sadece saf fonksiyonlar için uygundur. İçeri baskı yapılamaz.

> **【拓展：JAX 的 grad vs PyTorch 的 autograd】**PyTorch 梯度存在テンソ 上(x.grad),JAX 梯度看作函数的输出──これは JAX 天然支持高阶导数(grad(grad((f)) anlamına gelir),而 PyTorch 特殊処理──在 JAX 中,计算 Hessian矩阵只需`jax.hessian(f)`,PyTorch 需要 `torch.autograd.functional.hessian`- Evet.

### XLA'ya kompile et.

```python
@jax.jit
def train_step(params, x, y):
    loss = loss_fn(params, x, y)
    return loss

fast_step = jax.jit(train_step)
```

İlk çağrıda JAX fonksiyonu izler. Hangi işlemlerin gerçekleştiğini, uygulanmadan kaydeder. Sonra bu izleri Google'ın TPU ve GPU'lar için kompiler olan XLA'ya verir. XLA işlemleri birleştirir, fazladan hafıza kopyalarını ortadan kaldırır ve optimize edilmiş makine kodu üretir.

> İlk kez kullanıldığında, JAX  takip işlevi, hangi işlemlerin gerçekleştiğini kaydetir, gerçekte gerçekleştirilmez. Sonra takip XLA'ya verilir.

Sonraki aramalar Python'ı tamamen atlatır.

> 后续调用完全跳过Python──编译后的代码在加速器上运行以C++ 速度──

JIT yardımcı olduğunda:

> JIT'in yardımcı bir sahne:

- Eğitim adımları (aynı hesaplama binlerce kez tekrarlanır)
  Çinçe Çevirimi: training step (shame calculate)
- İndirim (aynı model, farklı girişler)
  Çönüm: (sözüm: (sözüm: (sözüm: (sözüm: (sözüm: (sözüm: (sözüm: (sözüm: (sözüm: (sözüm:)))
- Benzer şekilli girişlerle birden fazla kez çağrılan herhangi bir fonksiyon
  Çinçe Çevirimi: herhangi bir benzer şekil ile birçok kez yapılan bir işlev

JIT ağrıyınca:

> JIT'in zararlı bir sahne:

- Python kontrol akışıyla birlikte değerlere bağlı fonksiyonlar (`if x > 0`x izlenmiş bir dizidir)
  Çinçe Çevirim: içerir Python 控制流的函数`if x > 0`(x = takip edilen sayı)
- Tek çekim hesaplamaları (kompile overhead runtime'den fazla)
  Çinçe Çevirimi:一次性计算 (),
- Debugging (içinden izleme gerçek çalıştırmayı gizler)
  Çinçe Çevirimi:调试(追踪隐藏了实际执行)

Kontrol akışı kısıtlaması gerçek.`jax.lax.cond`yerine getirir .`if/else`- Evet .`jax.lax.scan`yerine getirir .`for`Bunlar seçmeli değiller - birleştirme fiyatıdır.

> Kontrol akışı sınırlaması gerçektir.`jax.lax.cond`替代 `if/else`- Evet.`jax.lax.scan`替代 `for`Bu seçenekler seçilebilir değiller.

### Vmap: Otomatik vektörleşme

Bir örneği işleyen bir işlevi yazıyorsunuz:

> Bir işlem tek örnek işlevi yazıyorsun:

```python
def predict(params, x):
    return jnp.dot(params['w'], x) + params['b']
```

`vmap`bir partiyi işlemek için kaldırır:

```python
batch_predict = jax.vmap(predict, in_axes=(None, 0))
```

`in_axes=(None, 0)`Yöntem: toplanmayın `params`(tükeltilmiş),    0      `x`- Yönlük yok .`for`Bu yüzden, bu birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, birim, bir, birim, bir, birim, bir, bir, bir, birim, bir, bir, birim, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir

> `in_axes=(None, 0)`表示: 不对`params`进行批处理(共享),对 `x`Bu işlemlerin bir kısmı olarak,`for`循环──无需重塑──无需手动传递批量维度──JAX otomatik olarak批量维度出查并向量化整个计算──

Bu sintaksik şeker değil.`vmap`Python döngüsünden 10-100 kat daha hızlı çalışan birleşik vektörlü kod üretir.`jit`ve `grad`- ...

> Bu bir şeker değil.`vmap`Bu, Python'dan 10-100 kat daha hızlı bir şekilde gerçekleşir.`jit`和 `grad`组合:

```python
per_example_grads = jax.vmap(jax.grad(loss_fn), in_axes=(None, 0, 0))
```

Bir çizgi, PyTorch'de hack olmadan neredeyse imkansız.

> 逐样本梯度──一行代码── PyTorch'de neredeyse imkansızdır.

### pmap: Cihazlar arası veri paralelliği

```python
parallel_step = jax.pmap(train_step, axis_name='devices')
```

`pmap`işlevi tüm mevcut cihazlarda (GPU/TPU) kopyalar ve partiyi bölür.`jax.lax.pmean`ve `jax.lax.psum`cihazlar arasında gradientleri senkronize etmek.

> `pmap`Bu işlem, tüm kullanılabilir cihazlara göre yapılır.`jax.lax.pmean`和 `jax.lax.psum`跨设备同步梯度──

Google Gemini ' yi binlerce TPU v5e çipten kullanıyor .`pmap`(ve onun varisi)`shard_map`Programlama modeli: tek cihazlı versiyonu yazın, `pmap`- Tamam.

> Google kullanımı `pmap`(ve sonrası `shard_map`) binlerce blok TPU v5e 芯片 üzerinde eğitim Gemini。编程模型:写单设备版本,用 `pmap`- Tamam.

### Pytrees: Evrensel Veri Yapısı

JAX, "pytrees" üzerinde çalışır. Liste, tuples, dicts ve arraylerin yuva içindeki kombinasyonları.

> JAX 操作"pytree"列表、元组、字典和数组的嵌套组合──你的模型参数就是一个 pytree:

```python
params = {
    'layer1': {'w': jnp.zeros((784, 256)), 'b': jnp.zeros(256)},
    'layer2': {'w': jnp.zeros((256, 128)), 'b': jnp.zeros(128)},
    'layer3': {'w': jnp.zeros((128, 10)),  'b': jnp.zeros(10)},
}
```

JAX ' in her dönüşümü ...`grad`- Evet .`jit`- Evet .`vmap`- Pytrees'i nasıl geçeceğini biliyor.`jax.tree.map(f, tree)`uygulanır .`f`Optimizeciler tüm parametreleri aynı anda bu şekilde güncelleyebilir:

> Her JAX 变换`grad`- Evet.`jit`- Evet.`vmap`都知道如何穿越Pytrie.`jax.tree.map(f, tree)`- Ben de .`f`应用到每个叶子──这是优化器一次更新所有参数的方法:

```python
params = jax.tree.map(lambda p, g: p - lr * g, params, grads)
```

Hayır .`.parameters()`Metod. Parametre kayıt yok. Ağaç yapısı model.

> Hiç .`.parameters()`方法──没有参数注册──树结构就是模型──

### Fonksiyonel vs. Nesne Dönemi

PyTorch depoları nesnelerin içinde şunları belirtir:

```python
class Model(nn.Module):
    def __init__(self):
        self.linear = nn.Linear(784, 10)

    def forward(self, x):
        return self.linear(x)
```

JAX açık durumlu saf fonksiyonları kullanır:

```python
def predict(params, x):
    return jnp.dot(x, params['w']) + params['b']
```

Parameler aktarılır. Hiçbir şey saklanmaz. Hiçbir şey mutasyonlanmaz. Bu her işlevi test edilebilir, yapılandırılabilir ve kompile edilebilir hale getirir. Bu aynı zamanda paramları kendiniz yönetmeniz anlamına gelir.

> 参数被传输──不存储任何东西──不修改任何东西──这使每个函数可测试、可组合、可编译──这也意味着你需要自己管理参数或使用 Flax或Equinox等库──

### JAX Ekosistemi JAX Ekosistemi

JAX size ilkellikler verir.

> JAX 提供原语──库提供便利性:

| Library | Role | Style |
|---------|------|-------|
| **Flax** (Google) | Neural network layers | `nn.Module` with explicit state |
| **Equinox** (Patrick Kidger) | Neural network layers | Pytree-based, Pythonic |
| **Optax** (DeepMind) | Optimizers + LR schedules | Composable gradient transforms |
| **Orbax** (Google) | Checkpointing | Save/restore pytrees |
| **CLU** (Google) | Metrics + logging | Training loop utilities |

Optax standart optimizer kütüphanesi. Bu, gradient dönüşümünü (Adam, SGD, kesim) parametreler güncelleme ile ayırır ve bunları oluşturmak önemsiz hale gelir:

> Optax standart optimizer kitlesidir. Bu, ılımlı ve kolay bir şekilde ayrılırken, parametrelerle yeni ayrılır.

```python
optimizer = optax.chain(
    optax.clip_by_global_norm(1.0),
    optax.adam(learning_rate=1e-3),
)
```

### JAX vs PyTorch ne zaman kullanılır ?

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

Dürüstçe cevap: JAX'i kullanmak için belirli bir nedeniniz yoksa PyTorch kullanın. Bu nedenler TPU erişim, örnek başına gradient gereksinimleri, çok cihazlı eğitim büyük ölçekte veya Google/DeepMind/Anthropic'te çalışmak.

> 诚实的答案:PyTorch kullanmak için belirli bir neden yoksa değilse.

### JAX'de rastgele sayılar JAX'de rastgele sayılar

JAX'in küresel bir rastgele durumu yoktur. Her rastgele işlem açık bir PRNG anahtarı gerektirir:

> JAX  hiçbir tüm devleti 随机状态 ⋅ Her 随机操作都需要显然的PRNG 密钥:

```python
key = jax.random.PRNGKey(42)
key1, key2 = jax.random.split(key)
w = jax.random.normal(key1, shape=(784, 256))
```

Bu ilk başta sinir bozucu ama PyTorch'un ürettiği bir özellik olan cihazlar ve komileler arasında yeniden üretilebilirliği garanti ediyor.`torch.manual_seed`Çoklu GPU ayarlarında garanti yapamaz.

> Birinci başta çok sorunlu bir durumdu. Ama bu PyTorch'in yapabildiği bir cihaz ve birleştirme yapabilme gücünü garanti etti.`torch.manual_seed`Çok fazla GPU'da garanti edilmez.
```figure
batchnorm-effect
```

## Yapın

## Yapın.

> **【中文解读】**JAX + Optax 訓練 MNIST 分类器──注意和 PyTorch 的关键区别: nn.Module、参数用嵌套字典(pytree) depo、訓練步骤是纯函数用 @jax.jit 编译、没有 .zero_grad() /.backward() /.step() 梯度计算和参数更新合并在一个函数中──

### Adım 1: Kurulum ve Veriler. Adım 1: Kurulum ve Veriler.

JAX ve Optax kullanarak MNIST'de 3 katlı bir MLP eğitime geçeceğiz. 784 giriş, 256 ve 128 nöronun iki gizli katmanı, 10 çıkış sınıfı.

> JAX ve Optax ile MNIST'de 3 katlı MLP, 784 giriş, 256 ve 128 sinirlerin gizli katlı 10 çıkış sınıfı eğitime başlayacağız.

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

### Adım 2: Parametreyi başlatın.

Bir sınıf yok, sadece bir Pytree'yi geri veren bir fonksiyon:

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

Bir tohumdan ayrı üç PRNG anahtarı, her ağırlık, bir yastık dikte bir değişmez dizidir.

> Hârşâli tamamlanmıştır O başlangıçlılık. Üç PRNG anahtarı bir tohumdan ayrılır. Her bir ağırlık, bir gömlek sözlüğünde değişmez bir dizi.

### Adım 3: Önceki Geçit.

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

Temiz fonksiyonlar, paramlar, tahminler.`self`, hiç depolama durumu yok. `loss_fn`sıfırdan çapraz entropi hesaplar -- softmax, log, negatif ortalama.

> 純函数──参数进,预测出──没有 `self`, depolama durumu yok.`loss_fn`softmax、log、负平均值──

### Adım 4: JIT-Compiled Training Step.

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

`jax.value_and_grad`Bir geçişle hem kayıp değerini hem de eğilimi geri verir.`@jax.jit`Bu programın ilk çağrısı sonrasında, her eğitim adımı Python'a dokunmadan çalışır.

> `jax.value_and_grad`Bir kez yayılmak sırasında aynı anda kaybı değer ve derecesi geri dönüştürmek.`@jax.jit`装饰器 iki işlevi XLA'ya özetleyecek. İlk kez kullanıldıktan sonra, her antrenman aşamasında Python'a dokunmaktan vazgeçmek zorunda kalacak.

### Adım 5: Eğitim Çember

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

10 dönem. ~ 97% test doğruluğu. İlk dönem yavaş (JIT kompili) Epochs 2-10 hızlı.

> 10 个时代──~97% 测试准确率──第一个时代 较慢(JIT 编译)──第 2-10 个时代 很快──

Ne eksik olduğunu fark et: hayır `.zero_grad()`Hayır .`.backward()`Hayır .`.step()`Tüm güncelleme bir fonksiyon çağrısıdır. Gradiyentler hesaplanır, Adam tarafından dönüştürülür ve parametrelere uygulanır.`train_step`- Evet .

> Dikkat et yok mu ?`.zero_grad()`- Hayır .`.backward()`- Hayır .`.step()`△ tüm yenilik bir yapılandırma fonksiyonu调用──梯度被计算、被亚当变换、被应用到参数上全部在`train_step`İçinde tamamlanıyorum.

> **【拓展：JAX 的分布式训练】**JAX'in pmapı otomatik olarak eğitimleri birden fazla cihaze dağıtabilir.`jax.pmap(train_step, axis_name='batch')`Bir seriyi otomatik olarak 4 parçaya ayırır, her GPU'yu bir tane işleyecek ve sonra geçecek.`jax.lax.pmean`Google'ın TPU Pod'u binlerce chip, JAX'in ağı ve shard_map'ı binlerce cihazda modelle yürütülebilir.

## Çerçeveyi kullanın.

> **【中文解读】**JAX 生态的核心库:Flax(Google'ın sinir ağı katmanı, nn.Module gibi) √Equinox(更 Pythonic 的替代) √Optax(可组合的优化器库) √Optax'ın tasarım felsefesi:优化器是梯度变化的链式组合剪 → Adam → 权重衰减,每一步都是独立的变化──

### Google Standartı: Google Standartı Kutusu

Flax, JAX sinir ağı kütüphanesi en yaygın kütüphanesi.`nn.Module`Geriye, ama açık bir devlet yönetimiyle:

> Flax en sık kullanılan JAX sinir ağı kitlesidir. Yeniden kullanıldı.`nn.Module`, ama açık durum yönetimi kullanmak:

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

PyTorch'la aynı yapı, ama `params`modelden ayrıdır. `model.init()`Param yaratıyor.`model.apply(params, x)`Model nesne durumsuz.

> 结构与 PyTorch 相同,但 `params`Modelden ayrılmış.`model.init()`创建参数──`model.apply(params, x)`运行前向传播──模型对象没有状态──

### Equinox: Pythonic Alternative.

Ekvinoks (Patrick Kidger tarafından) modeller pytrees olarak temsil edilir:

> Equinox ({{padleft:Equinox}}) ‡ by Patrick Kidger 开发) ‡模型表示为 pytree:

```python
import equinox as eqx

model = eqx.nn.MLP(
    in_size=784, out_size=10, width_size=256, depth=2,
    activation=jax.nn.relu, key=jax.random.PRNGKey(0)
)
logits = model(x)
```

Modelin kendisi bir pytree.`.apply()`Bu, JAX'in düşüncesine daha yakındır.

> Model kendisi bir ağaçtır.`.apply()`◊ parametre sadece modelin yapraklarıdır.

### Optax: Yapılandırılabilir Optimizer

Optax, gradient dönüşümünü güncelleme ile ayırır:

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

Gradient kesimi, öğrenme hızının yükselmesi, ağırlık kaybı - hepsi bir değişim zinciri olarak oluşur. Her değişim gradientleri görür, değiştirir ve bir sonrakiye aktarır. Monolit optimizer sınıfı yoktur.

> 梯度裁剪、学习率预热、权重衰减全部作为变换链组合──每个变换看梯度,修改它们,传递给下一个──没有巨大的优化器类──

## İndirin . Ürünler .

**Installation:**

```bash
pip install jax jaxlib optax flax
```

GPU desteği için:

```bash
pip install jax[cuda12]
```

TPU için (Google Cloud):

```bash
pip install jax[tpu] -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
```

**Performance gotchas:**

- İlk JIT çağrısı yavaş (tümlenme).
- JIT'in içindeki JAX dizinleri üzerinde Python döngüslerinden kaçının.`jax.lax.scan`veya `jax.lax.fori_loop`- Evet .
- `jax.debug.print()`JIT'de çalışmaktadır.`print()`- Hayır.
- Profil `jax.profiler`XLA komisyonu şişek boğazlarını saklayabilir.
- JAX, öntanımlı olarak GPU belleğinin %75'ini önceden ayırır.`XLA_PYTHON_CLIENT_PREALLOCATE=false`- İptal etmek için.

**Checkpointing:**

```python
import orbax.checkpoint as ocp
checkpointer = ocp.PyTreeCheckpointer()
checkpointer.save('/tmp/model', params)
restored = checkpointer.restore('/tmp/model')
```

**This lesson produces:**
- `outputs/prompt-jax-optimizer.md`-- doğru JAX optimizer yapılandırmasını seçmek için bir ipucu
- `outputs/skill-jax-patterns.md`-- JAX'de fonksiyonel kalıpları kapsayan bir beceri

## Egzersizler.

1. MLP'ye düşüş ekleyin. JAX'de düşüş bir PRNG anahtarı gerektirir. Bir anahtarı ileri geçişten geçerek her düşüş katman için bölün. Test doğruluğunu ile ve dışına karşılaştırın.

2. Kullanım`jax.vmap`32 MNIST görüntüler için örnek başına gradient hesaplamak için. Her örnek için gradient normunu hesaplayın. Hangi örneklerde en büyük gradient var ve neden?

3. Elci önleme fonksiyonunu genel bir fonksiyonla değiştirin `mlp_forward(params, x)`Bu, herhangi bir katman için çalışır.`jax.tree.leaves`derinliği otomatik olarak belirlemek için.

4. Eğitim adımını birlikte ve olmadan göster `@jax.jit`Her seferinde 100 adım yapın. Hardware'daki hızlanmanın ne kadarı var?

5. Yapıştırarak gradient kesimi uygulayın `optax.chain(optax.clip_by_global_norm(1.0), optax.adam(1e-3))`Eğitimle ve kesmeden, etkisini görmek için eğitiş üzerinde eğilime normunu çiz.

## Anahtar Şartlar .

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

## Daha fazla okumak

- JAX belgesi: https://jax.readthedocs.io/- ... resmi doktorlar, yüksek lisans, JIT ve Vmap hakkında mükemmel dersler.
  JAX 文档:https://jax.readthedocs.io/官方文档, Graduate jit 和 vmap 优秀教程
- "JAX: Python+NumPy programlarının yapılandırılabilir dönüşümleri" (Bradbury et al., 2018) - tasarım felsefesini açıklayan orijinal makale
  Bradbury 等人,JAX:Python+NumPy 程序的可组合变换(2018) 解释设计哲学学的原始论文
- İpek belgesi: https://flax.readthedocs.io/-- JAX için Google'ın sinir ağ kütüphanesi
  Flax 文档 Google JAX  geliştirmek için sinir ağı kütüphanesi
- Patrick Kidger, "Equinox: JAX'deki sinir ağları, çağrılabilir PyTrees ve filtreli dönüşümler aracılığıyla" (2021) -- Flax'in Pythonik alternatifidir
  Patrick Kidger,Equinox: PyTree ve Over变换实现 JAX 神经网络(2021)Flax'ın Pythonic 替代方案
- DeepMind, "Optax: Composable gradient transformation and optimization" -- standart optimizer kütüphanesi
  DeepMind,Optax:可组合的梯度变换和优化标准优化器库
- "You Don't Know JAX" (Colin Raffel, 2020) - T5 yazarlarından birinin JAX gotchas ve kalıplarına yönelik pratik bir rehber
  Colin Raffel,you still don't understand JAX(2020)JAX 陷和模式的实用指南,作者为 T5 论文作者之一
