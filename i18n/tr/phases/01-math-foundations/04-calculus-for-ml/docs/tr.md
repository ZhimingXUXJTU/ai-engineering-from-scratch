# Makine öğrenimi için hesaplama makineler öğrenmesindeki küçük noktalar.

> Derivatifler, aşağı doğru olan yönü söyler.

> Növrel ağ öğrenmek için gereken her şey budur.

**Type:** Learn | **类型:** 学习
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-03 | **前置知识:** Phase 1, Lessons 01-03
**Time:** ~60 minutes | **时间:** ~60 分钟

## Öğrenme hedefleri

- Ortak ML fonksiyonları için sayısal ve analitik türevleri hesaplayın (x^2, sigmoid, çapraz entropy)
  計算常见 ML 函数(x^2、sigmoid、交叉) 計算常见 ML 函数
- 1D ve 2D'de bir kayıp fonksiyonunu en aza indirmek için sıfırdan gradient düşüşü uygulayın
  0'dan gerçekleşen derecede düşüş, 1D ve 2D'de en az düşüş fonksiyonu
- Bir çizgisi gerileme modelinin gradiyentiyi çıkarın ve manuel ağırlık güncelleştirmeleri ile çalıştırın
  推导线性回归模型的梯度,并通过手动权重更新进行训练
- Hessian matrisini, Taylor serisi yaklaşımlarını ve optimizasyon yöntemleriyle bağlantısını açıklayın
  解释 Hessian 矩阵、Taylor 级数近似及其优化方法的联系

> **【中文解读】**
> 导数 size "gelirken hangi yönde yanlışlık yaratabilir" diyor. Nöral ağda milyonlarca parametredir, her bir parametresi bir "tüy"tir.

> **【拓展：微积分与神经网络】**
> - **梯度下降**: Nörolojik ağ eğitimi çekirdek algoritması  梯度 boyunca ters yönlü yenilemeler 
> - **SGD/Adam**Bu değişimlerin bir kısmı, Adam'ın da hareketlilik ve kendi kendine uyum sağlayan öğrenme oranına katılmasıdır.
> - **学习率**梯度下降的步长──太大则跳过最小值,太小则收太慢──

## Sorunlar. Sorunlar.

> **【中文解读】**Neural net'te milyonlarca ağırlık vardır. Dönüşüm, her dönmenin hangi yönde dönüşmesi gerektiğini bulmaktır.

## Konsepten bir şey.

> **【拓展：偏导数就是"只动一个旋钮看效果"]**Nörörel ağın kayıp işlevi L(w1, w2, ..., wn) 有百万个变量──偏导数 ∂L/∂w_i 告诉你"只改变 w_i 一重权,损失变化多少"──梯度就是把所有的偏导数组合成一个向量,指向"最的上坡方向",所以沿负梯度走就是最快的下坡路──

### Devirim nedir?

Bir türev değişim hızını ölçer. bir işlevi için y = f(x), türev f'(x) size söyler: x'yi küçük bir miktarda itirseniz, y ne kadar değişir?

> 导数量量变化率──对函数 y = f(x),导数 f'(x) 告诉你: x 微小变化, y 变化多少?

Geometrik olarak, türe bir noktada çelişkin çizginin eğimi.

> 几何上,导数, bir çizgiyi bir noktada eğilenliktir.

**f(x) = x^2:**

| x | f(x) | f'(x) (slope) |
|---|------|---------------|
| 0 | 0    | 0 (flat, at the bottom) |
| 1 | 1    | 2 |
| 2 | 4    | 4 (tangent line slope at this point) |
| 3 | 9    | 6 |

X=2'de eğim 4'dir. Eğer x'i biraz sağdan hareket ettirseniz, y bu miktarın yaklaşık 4 katına çıkar. x=0'da eğim 0'dur.

> X=2'de, eğrilik oranı 4'dir. Eğer x doğru hareket ederseniz, y yaklaşık olarak bu hareket miktarını 4 kat artırır.

Resmi tanım:

```
f'(x) = lim   f(x + h) - f(x)
        h->0  -----------------
                     h
```

Kodda, sınırı atlayıp çok küçük bir h kullanırız. Bu sayısal türevdir.

> Kodda, uç uç uçları, doğrudan çok küçük h ile yaklaşmak için.

### Bölümsel türevler: Bir seferde bir değişken

Gerçek fonksiyonlar birçok giriş vardır. Bir sinir ağı kaybı binlerce ağırlığa bağlıdır. Bir kısmi türev bir hariç tüm değişkenleri sabit tutar, sonra türevini o birine göre alır.

> Gerçek işlevi birçok giriş vardır. Nöral ağ kaybı işlevi binlerce ağırlığa bağlıdır.

```
f(x, y) = x^2 + 3xy + y^2

df/dx = 2x + 3y     (treat y as a constant)
df/dy = 3x + 2y     (treat x as a constant)
```

Her kısmi türeç cevap verir: Eğer sadece bu ağırlığı itirsem, kaybı nasıl değiştiriyor?

> Her yönlendirme sayısı cevap verir: Eğer sadece bu ağırlığı kullanırsam, kayıp değişimi ne kadar?

### Gradyent: tüm kısmi türevlerin vektörü

Gradient, her kısmi türevini bir vektörde toplar. f ((x, y, z) fonksiyonu için, gradient:

> 梯度把所有偏导数集成一个向量──对函数 f ((x, y, z),梯度为:

```
grad f = [ df/dx, df/dy, df/dz ]
```

Merdiven en dik tırmanış yönünde işaret eder.

> 梯度指向最上升方向──要最小化函数,就沿相反方向走──

**Contour plot of f(x,y) = x^2 + y^2:**

İşlev, kontur çizgiler olarak konsentrik döngülerle bir kase şeklinde oluşur.

> Bu işlevi bir kavanoz şeklinde oluşur, eğ高線=同心圆.

| Point | grad f | -grad f (descent direction) |
|-------|--------|----------------------------|
| (1, 1) | [2, 2] (points uphill, away from minimum) | [-2, -2] (points downhill, toward minimum) |
| (0, 0) | [0, 0] (flat, at the minimum) | [0, 0] |

> 梯度方向指向最上坡,负梯度方向指向最下坡 (minimum value) 〜在最小 value处梯度为零──

Bu bir resimde gradient düşüşü.

> İşte bu, ısınma ve düşüş şekli.

### Optimize bağlantısı

Bir sinir ağını eğitmek optimizasyon demektir. modelin ne kadar yanlış olduğunu ölçen bir kayb fonksiyonu L ((w1, w2, ..., wn) var. Onu en aza indirmek istiyorsunuz.

> 訓練神經網就是优化──損失函数 L(w1, w2, ..., wn) 衡量模型有多"错", you're gonna minimize it──

```
Gradient descent update rule:

  w_new = w_old - learning_rate * dL/dw

For every weight:
  1. Compute the partial derivative of loss with respect to that weight
  2. Subtract a small multiple of it from the weight
  3. Repeat
```

> 梯度下降规则: 新权重 = 旧权重 - 学习率 × 梯度──重复:1) her bir ağırlığın yönlendirme sayısını hesaplayın;2) ağırlıktan bir küçük katılık çıkarın;3) 代数百万次──

Öğrenme hızı adım boyutunu kontrol eder. Çok büyük ve sen aşır. Çok küçük ve sen sürüklenir.

> Öğrenme oranı kontrol etmektedir. Çok büyük, çok küçük, çok yavaş.

**Loss landscape (1D slice):**

Kayıp işlevi L ((w) ağırlık w değişirken zirve ve vadilerle bir eğri oluşturur.

> 损失函数 L(w) 随权重 w 变化形成带峰和谷的曲线──

| Feature | Description |
|---------|-------------|
| Global minimum | The lowest point on the entire curve -- the best solution |
| Local minimum | A valley that is lower than its neighbors but not the lowest overall |
| Slope | Gradient descent follows the slope downhill from any starting point |

> Toplam en düşük değeri tüm ırmakların en düşük noktasıdır; Toplam en düşük değeri komşuların en düşük ama tümlük en düşük olmayan dağlık vadisidir; Düzeni herhangi bir başlangıç noktasından aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru aşağıya doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru doğru

Gradyent düşüş, yamaçın aşağıya doğru ilerler. Yerel minimumlarda sıkışabilir, ancak yüksek boyutlu alanlarda (milyonlarca ağırlık) bu nadiren pratik bir problemdir.

> 梯度下降沿坡下行──可能陷入局部最小值,但在高维空间中 (Million-level权重), bu çok az gerçek bir sorun haline gelir──

### Sayısal ve analitik türevler

Bir türevini hesaplamanın iki yolu vardır.

> 計算導數: İki yöntem vardır.

Analiz: hesap kurallarını el ile uygulayın. f'(x) = x^2, türev f'(x) = 2x. Tam.

> 解析法:手动应用微积分规则──如 f(x) = x^2 的导数是 f'(x) = 2x──精确且快速──

Sayısal: tanımı kullanarak tahmini. F ((x+h) ve f ((x-h) küçük bir h için hesaplayın, sonra farkı kullanın.

> 数值法:用定义近似──计算 f(x+h) 和 f(x-h),用差值除以 2h──

```
Numerical (central difference):

f'(x) ~= f(x + h) - f(x - h)
          -----------------------
                  2h

h = 0.0001 works well in practice
```

Sayısal türevler daha yavaş ama herhangi bir fonksiyon için çalışır. Analitik türevler hızlıdır ancak formülü çıkarmanızı gerektirir. Nöral ağ çerçeveleri üçüncü bir yaklaşımı kullanır: otomatik farklılaşma, tam türevleri mekanik olarak hesaplar.

> Bilgi değerleri, herhangi bir işlevi için daha yavaş ama uygundur.

### Basit fonksiyonlar için elden üretilen türevler

Bunlar ML'de tekrar tekrar göreceğiniz türevler.

> Bunlar ML'de tekrar tekrar göreceğiniz yönlendirmeler.

```
Function        Derivative       Used in
--------        ----------       -------
f(x) = x^2     f'(x) = 2x      Loss functions (MSE)
f(x) = wx + b  f'(w) = x        Linear layer (gradient w.r.t. weight)
                f'(b) = 1        Linear layer (gradient w.r.t. bias)
                f'(x) = w        Linear layer (gradient w.r.t. input)
f(x) = e^x     f'(x) = e^x     Softmax, attention
f(x) = ln(x)   f'(x) = 1/x     Cross-entropy loss
f(x) = 1/(1+e^-x)  f'(x) = f(x)(1-f(x))   Sigmoid activation
```

f ((x) = x^2:

```
f(x) = x^2    f'(x) = 2x

  x    f(x)   f'(x)   meaning
  -2    4      -4      slope tilts left (decreasing)
  -1    1      -2      slope tilts left (decreasing)
   0    0       0      flat (minimum!)
   1    1       2      slope tilts right (increasing)
   2    4       4      slope tilts right (increasing)
```

> X = 0 时导数为负 (x = 0 时导数为零) = 0 时导数为零 (x = 0 时导数为正 (x = 0) = 0 时导数为正 (x = 0) = 0 时导数为正 (x = 0) = 0 时导数为正 (x = 0) = 0 时导数为零 (x = 0) = 0 时导数为正 (x = 0) = 0 时导数为正 (x = 0) = 0 时导数为正 (x = 0) = 0 时导数为正 (x = 0) = 0 时导数为正 (x = 0) = 0 时导数为正 (x = 0) = 0 时导数为正 (x = 0) = 0) = 0 时导数为正 (x = 0) = 0) = 0

f(w) = wx + b için x=3, b=1:

```
f(w) = 3w + 1    f'(w) = 3

The derivative with respect to w is just x.
If x is big, a small change in w causes a big change in output.
```

> Eğer x  çok büyükse, w'nin küçük değişiklikleri çıkışın büyük değişmesine neden olursa, bu yüzden giriş birleştirme antrenman kararlılığı için bu kadar önemli.

### Zincir kuralı

İşlevler bir araya geldiğinde, zincir kuralı size nasıl farklılık göstereceğinizi söyler.

> Bir fonksiyon karmaşık olduğunda, bir zincir kuralı nasıl yönlendirilirse söyler.

```
If y = f(g(x)), then dy/dx = f'(g(x)) * g'(x)

Example: y = (3x + 1)^2
  outer: f(u) = u^2       f'(u) = 2u
  inner: g(x) = 3x + 1    g'(x) = 3
  dy/dx = 2(3x + 1) * 3 = 6(3x + 1)
```

Nöral ağlar fonksiyon zincirleri: giriş -> doğrusal -> etkinleştirme -> doğrusal -> etkinleştirme -> kayb. Geri yayılma, çıkıştan girişe tekrar tekrar uygulanan zincir kuraldır. Tüm algoritma budur.

> 神经网络是函数链:输入 -> 线性 -> 激活 -> 线性 -> 激活 -> 损失──反向传播就是从输出到输入反复应用链式法则──这是整个算法──

### Hessian Matrix

Merdiven, eğimden, Hessian'dan eğrilikten bahseder.

> 梯度 size eğrilik gösteriyor, Hessian 矩阵 size eğrilik gösteriyor.

Hessian, ikinci sıradaki kısmi türevlerin matrisidir. f ((x1, x2, ..., xn) fonksiyonu için, Hessian'ın giriş (i, j) şudur:

> Hessian'ın ikinci aşaması ise ∂2f/∂x_i ∂x_j) ⋅

```
H[i][j] = d^2f / (dx_i * dx_j)
```

2 değişken fonksiyon için f ((x, y):

```
H = | d^2f/dx^2    d^2f/dxdy |
    | d^2f/dydx    d^2f/dy^2 |
```

**What the Hessian tells you at a critical point (where gradient = 0):**

> Hessian 在临界点 (梯度为0处) size: local minimum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local maximum value, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, local level, or local level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, level, or level, level, level, level, level, level, level, level,

| Hessian property | Meaning | Example surface |
|-----------------|---------|-----------------|
| Positive definite (all eigenvalues > 0) | Local minimum | Bowl pointing up |
| Negative definite (all eigenvalues < 0) | Local maximum | Bowl pointing down |
| Indefinite (mixed eigenvalues) | Saddle point | Horse saddle shape |

> 正定(所有特征值 > 0) = 局部最小值;负定(所有特征值 < 0) = 局部最大值;不定(特征值有正有负) = 点。

**Example:**f(x, y) = x^2 - y^2 (bir otlak fonksiyonu)

```
df/dx = 2x       df/dy = -2y
d^2f/dx^2 = 2    d^2f/dy^2 = -2    d^2f/dxdy = 0

H = | 2   0 |
    | 0  -2 |

Eigenvalues: 2 and -2 (one positive, one negative)
--> Saddle point at (0, 0)
```

f ((x, y) = x^2 + y^2 (bir kase) ile karşılaştırın:

```
H = | 2  0 |
    | 0  2 |

Eigenvalues: 2 and 2 (both positive)
--> Local minimum at (0, 0)
```

**Why the Hessian matters in ML:**

> Hessian ML'de neden önemlidir: Newton'un Hessian 修正梯度方向, make 方向走小步、平坦方向走大步,从而比梯度下降更快收──

Newton'un yöntemi, gradient düşüşünden daha iyi optimizasyon adımlarını almak için Hessian'ı kullanır.

```
Newton's update:    w_new = w_old - H^(-1) * gradient
Gradient descent:   w_new = w_old - lr * gradient
```

> Newton 更新:w_new = w_old - H−1 × gradient。

Newton'un yöntemi daha hızlı bir şekilde yaklaşır çünkü Hessian'ın "daha" kaymaları - dik yönler daha küçük adımlar alır, düz yönler daha büyük adımlar alır.

> Newton daha hızlı kazanıyor, çünkü Hessian " yeniden küçültülmüş " gradient  direction 走小步,平坦方向 走大步.

N parametre olan bir sinir ağı için Hessian N x N. 1 milyon parametre olan bir model 1 trilyon giriş matrisine ihtiyaç duyar.

> 问题在:N 个参数的网络,Hessian 是N×N──百万参数模型需要万亿规模矩阵

| Method | What it uses | Cost | Convergence |
|--------|-------------|------|-------------|
| Gradient descent | First derivatives only | O(N) per step | Slow (linear) |
| Newton's method | Full Hessian | O(N^3) per step | Fast (quadratic) |
| L-BFGS | Approximate Hessian from gradient history | O(N) per step | Medium (superlinear) |
| Adam | Per-parameter adaptive rates (diagonal Hessian approx) | O(N) per step | Medium |
| Natural gradient | Fisher information matrix (statistical Hessian) | O(N^2) per step | Fast |

> Önemli olmayan bir optimizasyon karşılaştırması: gradience downdown only with a single step guide number (O(N),慢); Newton 法 with a complete Hessian (O(N3), fast but too expensive); L-BFGS with gradience history approximate Hessian; Adam using gradience against corner Hessian 近似做每参数自适应; Natural gradience with Fisher 信息矩阵。

Adam, derin öğrenme için varsayılan optimizerdir. Parametre başına gradientlerin çalışkan ortalamasını ve değişimini takip ederek ikinci sıradaki bilgileri ucuz bir şekilde yaklaştırır.

> 实际上,Adam is a deep learning default optimizer―― it tracks the average value and the square difference of each parameter gradient, cheaply approximate second-stage information―

### Taylor Serisi Yaklaşımları

Herhangi bir düz fonksiyon yerel olarak bir polinom ile yaklaşılabilir:

> Herhangi bir düzleme işlevi, yerel olarak çoklu bir yaklaşım olarak kullanılabilir.

```
f(x + h) = f(x) + f'(x)*h + (1/2)*f''(x)*h^2 + (1/6)*f'''(x)*h^3 + ...
```

Ne kadar çok terimi eklerseniz, yaklaşım daha iyi olur -- ama sadece x noktasına yakın.

> 包含的项越多,近似越好但只在x 附近有效──一阶泰勒 = 梯度下降,二阶泰勒 = Newton 法──

**Why Taylor series matter for ML:**

- **First-order Taylor = gradient descent.**f(x + h) ~ f(x) + f'(x) *h kullanırken, bir çizgi yaklaşım yapıyorsunuz.

- **Second-order Taylor = Newton's method.**f(x + h) ~ f(x) + f'(x) *h + (1/2) *f'(x) *h^2, bir kare modeli elde edersiniz.

- **Loss function design.**MSE ve çapraz entropi, düzgün bir şekilde hareket eder, yani Taylor genişlemeleri iyi davranır.

> Taylor 级数在 ML 中的意义:一阶 Taylor = 线性近似 = 梯度下降;二阶 Taylor = 二次近似 = Newton 法;MSE 和交叉的平滑性不是巧合平滑损失让优化可预测──

```
Approximation order    What it captures    Optimization method
-------------------    -----------------   -------------------
0th order (constant)   Just the value      Random search
1st order (linear)     Slope               Gradient descent
2nd order (quadratic)  Curvature           Newton's method
Higher orders          Finer structure     Rarely used in ML
```

> Yakınlık seviyeler ve optimize yöntemleri: 0 阶只用值(随机搜索); 1 阶用斜率(梯度下降); 2 阶用曲率(Newton 法);更高阶在 ML 中很少使用──

Anahtar anlayış: tüm gradient tabanlı optimizasyon aslında kayıp fonksiyonunu yerel olarak yaklaştırmak ve bu yaklaşımın en azına doğru adım atmakla ilgilidir.

> 关键洞见: Tüm dereceli optimizasyonlar özünde yerel yakın kaybı işlevi ile, sonra bu yakın en küçük değer noktasına gider.

### ML'deki bütünler

Devireler değişim oranlarını söyler. Integraller bir eğri altında alanı hesaplar.

> 导数告诉你变化率,积分计算累积(曲线下面积) ⋅

ML'de, entegralları el ile hesaplamak nadiren mümkündür, ama kavram her yerde:

> ML'de çok az kişi hesaplama yapar, fakat hesaplama kavramı yok:

**Probability.**Sıklık p ((x) olan sürekli rastgele değişken için:
```
P(a < X < b) = integral from a to b of p(x) dx
```
A ve b arasındaki olasılık yoğunluk eğrisinin altındaki alan, bu aralıkta iniş olasılığıdır.

> **概率**: için sürekli olarak değişken, yoğunluk işlevi p(x) içinde [a, b] 区间 积分就是落在此区间的概率──

**Expected value.**Muhtemelen ağırlanan ortalama sonuç:
```
E[f(X)] = integral of f(x) * p(x) dx
```
Verilerin dağıtımına karşı beklenen kayıp bir ayrılmaz bir unsurdur.

> **期望**:加权平均──数据分布上的期望损失就是一个积分,训练最小化它的经验近似──

**KL divergence.**İki dağılımın ne kadar farklı olduğunu ölçer:
```
KL(p || q) = integral of p(x) * log(p(x) / q(x)) dx
```
VAE'lerde, bilgi destillasyonunda ve Bayesian sonuçlandırmada kullanılır.

> **KL 散度**: iki dağılımsal farkı ölçmek.

**Normalization constants.**Bayesian sonucu:
```
p(w | data) = p(data | w) * p(w) / integral of p(data | w) * p(w) dw
```
Adınlayıcı, tüm olası parametreler değerlerinin bir bütünüdür. Genellikle çözülemezdir, bu nedenle MCMC ve varyasyonsal çıkarım gibi yaklaşımları kullanıyoruz.

> **归一化常数**Bayes'in teorisi: bölme, tüm olası parametreler değerinin bir bölümünü oluşturur.

| Integral concept | Where it appears in ML |
|-----------------|----------------------|
| Area under curve | Probability from density functions |
| Expected value | Loss functions, risk minimization |
| KL divergence | VAEs, policy optimization, distillation |
| Normalization | Bayesian posteriors, softmax denominator |
| Marginal likelihood | Model comparison, evidence lower bound (ELBO) |

> 积分概念在 ML 中体现:曲线下面积(密度函数求概率) 期望(损失函数) 、KL 散度(VAE/蒸) 归结(贝叶斯后验/softmax 分母) 边际似然(模型比较/ELBO) ⋅

### Bilgisayar Grafikinde Çok Değişken Zincir Kuralı

Zincir kuralı sadece bir çizgide skalar fonksiyonlara uygulanmaz. Bir nöral ağda değişkenler yayılır ve birleşir.

> Çok değişkenlik zinciri kuralları sadece liniyel ölçüm fonksiyonlarına uygulanmaz.

```mermaid
graph LR
    x["x (input)"] -->|"*w"| z1["z1 = w*x"]
    z1 -->|"+b"| z2["z2 = w*x + b"]
    z2 -->|"sigmoid"| a["a = sigmoid(z2)"]
    a -->|"loss fn"| L["L = -(y*log(a) + (1-y)*log(1-a))"]
```

Geriye geçiş sağdan sola dereceleri hesaplar:

```mermaid
graph RL
    dL["dL/dL = 1"] -->|"dL/da"| da["dL/da = -y/a + (1-y)/(1-a)"]
    da -->|"da/dz2 = a(1-a)"| dz2["dL/dz2 = dL/da * a(1-a)"]
    dz2 -->|"dz2/dw = x"| dw["dL/dw = dL/dz2 * x"]
    dz2 -->|"dz2/db = 1"| db["dL/db = dL/dz2 * 1"]
```

Her ok yerel türevle çarpılır. Her bir parametrenin gradiyenti kayıptan bu parametre giden yol boyunca tüm yerel türevlerin ürünüdür. Yollar dalınca ve birleşince katkıları toplamlanır (çok değişken zincir kuralı).

> Her bir ok, yerel yönlendirmelerin katılamasına göre çarpılır.

Bu, geri yayılma: bir hesaplama grafiği ile sistematik olarak uygulanan zincir kuralı, çıkıştan girişlere kadar.

> Karşı yönlü yayılmaların tamamı: hesaplama çizelgesinde çıkıştan giriş sistemleştirilmiş olarak uygulama zinciri kurallarıdır.

### Jacobian Matrix

Bir fonksiyon bir vektörü bir vektöre (örneğin bir nöral ağ katmanı gibi) haritasında bulduğunda, onun türevisi bir matrisdir. Jacobian, her çıkışın her girişe ilişkin her kısmi türevini içerir.

> Bir işlevin yön yönü yönü olarak gösterildiğinde, yön yönü bir yön yön yönü olarak belirlenir.

F: R^n -> R^m için, Jacobian J bir m x n matrisidir:

> 对于 f: R^n → R^m,Jacobian J 是一个m × n矩阵:

| | x1 | x2 | ... | xn |
|---|---|---|---|---|
| f1 | df1/dx1 | df1/dx2 | ... | df1/dxn |
| f2 | df2/dx1 | df2/dx2 | ... | df2/dxn |
| ... | ... | ... | ... | ... |
| fm | dfm/dx1 | dfm/dx2 | ... | dfm/dxn |

PyTorch onu işletiyor. Ama varlığını bilmek size geri yayılma şekilleri anlamanıza yardımcı olur: bir katman R^n'i R^m'e haritası yaparsa, onun Jacobian'ı m x n'dir.

> Nevron ağının JacobianPyTorch otomatik işlemini hesaplamayacaksınız. Ama bunun varlığını bilmek, geri dönüştürülmüş bir şekilde yayılmakta olan şekilleri anlamanıza yardımcı olacaktır.

### Neden bu sinir ağları için önemlidir

Bir sinir ağındaki her ağırlık bir gradient alır.

> Sinir ağındaki her bir ağırlığın bir derecesi vardır. Kayıpları azaltmak için bu ağırlığı nasıl ayarlayacağınızı söyler.

```mermaid
graph LR
    subgraph Forward["Forward Pass"]
        I["input"] --> W1["W1"] --> R["relu"] --> W2["W2"] --> S["softmax"] --> L["loss"]
    end
```

```mermaid
graph RL
    subgraph Backward["Backward Pass"]
        dL["dL/dloss"] --> dW2["dL/dW2"] --> d2["..."] --> dW1["dL/dW1"]
    end
```

Her kilo güncelleme:
- `W1 = W1 - lr * dL/dW1`
- `W2 = W2 - lr * dL/dW2`

> Her bir ağırlık değişikliği:W = W - lr × dL/dW──前向计算预测和损失,反向计算每一个权重的梯度,每一个权重沿梯度负方向走一小步──

Önceki geçiş tahmin ve kayıp hesaplar. Geriye geçiş her ağırlığa göre kayıp dikme hesaplar. Sonra her ağırlık bir adım aşağı doğru gider. Milyonlarca adım için tekrarlayın. Bu derin öğrenme.

> Ön yönlü yayımlama hesaplama tahmin ve kaybı, karşı yönlü yayımlama hesaplama her ağırlığın derecesini, sonra her ağırlığın üzerinde bir adım adım adım adım adım adım adım adım yapılır.

## Yapın.
```figure
derivative-tangent
```

## Yapın

### Adım 1: Sayısal türev sıfırdan

```python
def numerical_derivative(f, x, h=1e-7):
    return (f(x + h) - f(x - h)) / (2 * h)

def f(x):
    return x ** 2

for x in [-2, -1, 0, 1, 2]:
    numerical = numerical_derivative(f, x)
    analytical = 2 * x
    print(f"x={x:2d}  f'(x) numerical={numerical:.6f}  analytical={analytical:.1f}")
```

> Use center differential method to realize numeric value. H=1e-7 genellikle yeterince doğru.

Sayı türeği analitik bir ile birçok onluk yerine eşleşir.

> Sayı değer yönlendirmesi ve çözüm yönlendirmesi, küçük bir sayı sonra birçok yerde uyumlu kalırken merkez fark formülünün doğruluğunu doğruladı.

### Adım 2: Ayrı ögeleri ve gradientler

```python
def numerical_gradient(f, point, h=1e-7):
    gradient = []
    for i in range(len(point)):
        point_plus = list(point)
        point_minus = list(point)
        point_plus[i] += h
        point_minus[i] -= h
        partial = (f(point_plus) - f(point_minus)) / (2 * h)
        gradient.append(partial)
    return gradient

def f_multi(point):
    x, y = point
    return x**2 + 3*x*y + y**2

grad = numerical_gradient(f_multi, [1.0, 2.0])
print(f"Numerical gradient at (1,2): {[f'{g:.4f}' for g in grad]}")
print(f"Analytical gradient at (1,2): [2*1+3*2, 3*1+2*2] = [{2*1+3*2}, {3*1+2*2}]")
```

> sayı değer seviyesine: her seviyesinde bağımsız bir merkez farkı için yönlendirme, 组合成梯度向量──验证 f(x,y) = x2+3xy+y2 在 (1,2) 处的梯度为 [8, 7]──

### Adım 3: F ((x) = x^2'nin minimumunu bulmak için dereceli düşüş

```python
x = 5.0
lr = 0.1
for step in range(20):
    grad = 2 * x
    x = x - lr * grad
    print(f"step {step:2d}  x={x:8.4f}  f(x)={x**2:10.6f}")
```

X=5'den başlayarak her adım x=0'ye (minimum) daha yakınlaşır.

> X = 5'den çıkış, her adım daha yakın x = 0 ((minimum value) ◦ öğrenme oranı 0.1 让 x 逐步缩小到接近0──

### Adım 4: 2 boyutlu bir fonksiyonda dereceli düşüş

```python
def f_2d(point):
    x, y = point
    return x**2 + y**2

point = [4.0, 3.0]
lr = 0.1
for step in range(30):
    grad = numerical_gradient(f_2d, point)
    point = [p - lr * g for p, g in zip(point, grad)]
    loss = f_2d(point)
    if step % 5 == 0 or step == 29:
        print(f"step {step:2d}  point=({point[0]:7.4f}, {point[1]:7.4f})  f={loss:.6f}")
```

> 2D 梯度下降: (4, 3) 出发,每步更新点 -= lr × grad,逐步收到 (0, 0) 』

### Adım 5: Sayısal ve analitik türevleri karşılaştırmak

```python
import math

test_functions = [
    ("x^2",      lambda x: x**2,          lambda x: 2*x),
    ("x^3",      lambda x: x**3,          lambda x: 3*x**2),
    ("sin(x)",   lambda x: math.sin(x),   lambda x: math.cos(x)),
    ("e^x",      lambda x: math.exp(x),   lambda x: math.exp(x)),
    ("1/x",      lambda x: 1/x,           lambda x: -1/x**2),
]

x = 2.0
print(f"{'Function':<12} {'Numerical':>12} {'Analytical':>12} {'Error':>12}")
print("-" * 50)
for name, f, df in test_functions:
    num = numerical_derivative(f, x)
    ana = df(x)
    err = abs(num - ana)
    print(f"{name:<12} {num:12.6f} {ana:12.6f} {err:12.2e}")
```

> X=2'de 5 adet normal işlevi ile x2、x3、sin(x)、e^x、1/x。 hataları genellikle 1e-10'luk bir boyut seviyesinde, test sayısal değer yöntemi doğruluğu vardır.

### Adım 6: Hesyon'u sayısal olarak hesaplamak

```python
def hessian_2d(f, x, y, h=1e-5):
    fxx = (f(x + h, y) - 2 * f(x, y) + f(x - h, y)) / (h ** 2)
    fyy = (f(x, y + h) - 2 * f(x, y) + f(x, y - h)) / (h ** 2)
    fxy = (f(x + h, y + h) - f(x + h, y - h) - f(x - h, y + h) + f(x - h, y - h)) / (4 * h ** 2)
    return [[fxx, fxy], [fxy, fyy]]

def saddle(x, y):
    return x ** 2 - y ** 2

def bowl(x, y):
    return x ** 2 + y ** 2

H_saddle = hessian_2d(saddle, 0.0, 0.0)
H_bowl = hessian_2d(bowl, 0.0, 0.0)
print(f"Saddle Hessian: {H_saddle}")  # [[2, 0], [0, -2]] -- mixed signs
print(f"Bowl Hessian:   {H_bowl}")    # [[2, 0], [0, 2]]  -- both positive
```

> Hessian 矩阵:fxx、fyy 是二阶偏导,fxy 是混合偏导。点函数 x2-y2 的 Hessian 是 [[2,0],[0,-2]](一正一负=点),碗形 x2+y2 是 [[2,0],[0,2]](均正=最小值)。

Saddle fonksiyonunun Hessian öz değerleri 2 ve -2 (bir saddle noktasını doğrulayan karıştırılmış işaretler) vardır.

> 点 işlevi Hessian özellik değeri 2 和 -2(一正一负, 点 olarak belirlenir); bow shape işlevi Hessian özellik değeri 2 ((均正, 最小值 olarak belirlenir)。

### Adım 7: Taylor yaklaşımı

```python
import math

def taylor_approx(f, f_prime, f_double_prime, x0, h, order=2):
    result = f(x0)
    if order >= 1:
        result += f_prime(x0) * h
    if order >= 2:
        result += 0.5 * f_double_prime(x0) * h ** 2
    return result

x0 = 0.0
for h in [0.1, 0.5, 1.0, 2.0]:
    true_val = math.sin(h)
    t1 = taylor_approx(math.sin, math.cos, lambda x: -math.sin(x), x0, h, order=1)
    t2 = taylor_approx(math.sin, math.cos, lambda x: -math.sin(x), x0, h, order=2)
    print(f"h={h:.1f}  sin(h)={true_val:.4f}  order1={t1:.4f}  order2={t2:.4f}")
```

> Taylor 近似实战:在 x0=0 处使用一阶和二阶 Taylor 近似 sin(h) ・h=0.1 时近似精度极高,h=2 时偏差很大──这是梯度下降需要小学习率的数学根源──

X0 = 0 yakınında, sin(x) ~ x (birinci sıradaki Taylor). Yaklaşım küçük h için mükemmel ama büyük h için ayrılır. Bu nedenle gradient düşüşü küçük öğrenme oranları ile en iyi çalışır - her adım çizgisi yaklaşımın doğru olduğunu varsayır.

> Bu nedenle, bu aşamada küçük öğrenme oranı gerekecek.

### Adım 8: Neden bu bir nöral ağ için önemlidir

```python
import random

random.seed(42)

w = random.gauss(0, 1)
b = random.gauss(0, 1)
lr = 0.01

xs = [1.0, 2.0, 3.0, 4.0, 5.0]
ys = [3.0, 5.0, 7.0, 9.0, 11.0]

for epoch in range(200):
    total_loss = 0
    dw = 0
    db = 0
    for x, y in zip(xs, ys):
        pred = w * x + b
        error = pred - y
        total_loss += error ** 2
        dw += 2 * error * x
        db += 2 * error
    dw /= len(xs)
    db /= len(xs)
    total_loss /= len(xs)
    w -= lr * dw
    b -= lr * db
    if epoch % 40 == 0 or epoch == 199:
        print(f"epoch {epoch:3d}  w={w:.4f}  b={b:.4f}  loss={total_loss:.6f}")

print(f"\nLearned: y = {w:.2f}x + {b:.2f}")
print(f"Actual:  y = 2x + 1")
```

> 完整的线性回归训练循环:随机权重 w、b 出发, her örnek için hesaplama tahmin、误差、梯度 dw 和 db, sonra parametreyi güncelleme.

Her gradient tabanlı eğitim döngüsü bu örneği izler: tahmin, hesap kaybı, hesap gradientleri, güncelleme ağırlıkları.

> Her dereceli eğitim döngüsü şu moduya uyar: tahmin →  hesap kaybı →  hesap derecesi →  yenileme ağırlığı. Bu ders, 线性归归 y=2x+1'in antrenmanını gerçekleştirdi.

## Çerçeveyi kullanın.

NumPy ile aynı işlemler daha hızlı ve daha kısa:

> Uzd NumPy 重写: 同样运算更简洁更快──矢量化 Python 循环 避免,让梯度计算更高效──

```python
import numpy as np

x = np.array([1, 2, 3, 4, 5], dtype=float)
y = np.array([3, 5, 7, 9, 11], dtype=float)

w, b = np.random.randn(), np.random.randn()
lr = 0.01

for epoch in range(200):
    pred = w * x + b
    error = pred - y
    loss = np.mean(error ** 2)
    dw = np.mean(2 * error * x)
    db = np.mean(2 * error)
    w -= lr * dw
    b -= lr * db

print(f"Learned: y = {w:.2f}x + {b:.2f}")
```

> NumPy 向量化版: 用 `np.mean`Python'u değiştirmek için ortalama, daha hızlı, daha basit bir döngü kullanmak için kullanılır.

PyTorch gradient hesaplamasını otomatikleştirir ama güncelleme döngüsü aynı.

> Siz sadece sıfırdan aşağı dereceli işlemler gerçekleştirmişsiniz. PyTorch, dereceli işlemleri otomatikleştirmiş, ancak yeni döngü tamamen aynıdır.`w -= lr * dw`Bu bir yol asla değişmeyecek.

## Egzersizler.

1. Uygulama`numerical_second_derivative(f, x)`kullanmak`numerical_derivative`x^3'ün ikinci türevinin x=2'de 12 olduğunu kontrol edin.
    gerçekleştirmek `numerical_second_derivative(f, x)`,调用两次 `numerical_derivative` Test x^3 = 2'de ikinci aşama 12'dir.
2. F ((x, y) = (x - 3) ^ 2 + (y + 1) ^ 2'nin en azını bulmak için gradient düşüşünü kullanın. (0, 0) 'den başlayın. Cevap (3, -1) 'e yakın olmalıdır.
   Use梯度下降找 f(x, y) = (x - 3)2 + (y + 1)2'nin en düşük değeri, (0, 0) çıkıştan,应收到 (3, -1)。
3. Gradyent düşüş döngüsüne momentum ekleyin: Geçmiş gradientleri toplayan bir hız vektörünü koruyun.
   给梯度下降循环加动量:维护一个累积过去梯度的速度向量──比较有无动量在 f(x) = x4 - 3x2 上的收速度──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Derivative | "The slope" | The rate of change of a function at a point. Tells you how much the output changes per unit change in input. |
| Partial derivative | "Derivative of one variable" | The derivative with respect to one variable while all others are held constant. |
| Gradient | "Direction of steepest ascent" | A vector of all partial derivatives. Points in the direction that increases the function fastest. |
| Gradient descent | "Go downhill" | Subtract the gradient (times a learning rate) from the parameters to reduce the loss. The core of neural network training. |
| Learning rate | "Step size" | A scalar that controls how big each gradient descent step is. Too large: diverge. Too small: converge slowly. |
| Chain rule | "Multiply the derivatives" | The rule for differentiating composed functions: df/dx = df/dg * dg/dx. The mathematical basis of backpropagation. |
| Jacobian | "Matrix of derivatives" | When a function maps vectors to vectors, the Jacobian is the matrix of all partial derivatives of outputs with respect to inputs. |
| Numerical derivative | "Finite differences" | Approximating a derivative by evaluating the function at two nearby points and computing the slope between them. |
| Backpropagation | "Reverse-mode autodiff" | Computing gradients layer by layer from output to input using the chain rule. How neural networks learn. |
| Hessian | "Matrix of second derivatives" | The matrix of all second-order partial derivatives. Describes the curvature of a function. Positive definite Hessian at a critical point means local minimum. |
| Taylor series | "Polynomial approximation" | Approximating a function near a point using its derivatives: f(x+h) ~ f(x) + f'(x)h + (1/2)f''(x)h^2 + ... The basis for understanding why gradient descent and Newton's method work. |
| Integral | "Area under the curve" | The accumulation of a quantity over a range. In ML, integrals define probabilities, expected values, and KL divergence. |

> 术语速查:Derivative (导数/斜率) ‧Partial derivative (偏导数, fixed other variables) ‧Gradient (梯度), tüm偏导数 oluşan △, en 上方方向) ‧Gradient descent (梯度下降,沿梯度负方向更新) ‧Learning rate (öğrenme oranı, adım atma) ‧Chain rule (cadı kural, △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ 

## Daha fazla okumak

- [3Blue1Brown: Essence of Calculus](https://www.3blue1brown.com/topics/calculus)- Derivatifler, entegrallar ve zincir kuralları için görsel sezgisellik
- [Stanford CS231n: Backpropagation](https://cs231n.github.io/optimization-2/)- gradientlerin sinir ağları katmanları üzerinden nasıl akıştığı
