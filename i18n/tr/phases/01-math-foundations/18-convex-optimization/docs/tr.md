# Konves Optimizasyon

> Konves sorunlarının tek bir vadisi var, sinir ağlarının milyonlarca.
> 凸 sorunları sadece bir çukurdadır.

**Type:** Build | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 04 (Calculus for ML), 08 (Optimization) | **前置知识:** Phase 1, 第 04 课（微积分）、第 08 课（优化）
**Time:** ~90 minutes | **时间:** ~90 分钟

## Öğrenme hedefleri

- Bir fonksiyonun tanım, ikinci türe ve Hessian kriterlerini kullanarak eğri olup olmadığını test edin
  kullanımı defini、二阶导数和 Hessian 判据测试函数
- Newton'un yöntemini uygulayın ve onun katraz dönüşümünü gradient düşüşü ile karşılaştırın
  Newton'un Metodu'nu gerçekleştirmek için, ikinci katkı oranı aşağıya düştü.
- Lagrange çarpıcıları kullanarak kısıtlı optimizasyon sorunlarını çözmek ve KKT koşullarını yorumlamak
  kullan 拉格朗日乘子(Lagrange Multipliers) 求解约束优化问题,解释 KKT 条件
- Neden sinir ağı kayıpları manzaraları konveks değil, SGD hala iyi çözümler bulduğunu açıkla
  Neden sinir ağının kaybı neden de belirgin değil, SGD'nin hala iyi bir çözüm bulması gerekiyor.


> **【中文解读】**
> 凸 işlevi sadece bir 山谷 (全局最优) dır, 线性归归归 (线性归归) 凸的, bu nedenle tüm 局最优 (全局最优) vardır.

## Sorunlar. Sorunlar.

Ders 08'de, gradient düşüşü, momentum ve Adam'ı öğrendiniz. Bu optimizörler herhangi bir yüzeyde aşağıya doğru yürürler. Ama hiçbir garanti yok. Konves olmayan bir manzarada gradient düşüşü kötü bir yerel minimumda düşebilir, bir sedil noktasına sıkışabilir veya sonsuza dek sallanabilir. Neural ağlar konvessi olmayan ve başka bir alternatif olmadığı için yine de kullandınız.

> 第8 课教你梯度下降、动量和亚当──这些优化器可以在任何表面下坡──但它们没有保证──在非凸表面上,梯度下降可能陷入差的局部最小值──卡在点 (点) 或永远振荡──你还是使用它,因为神经网络不凸,没有替代方案──

Ancak makine öğreniminde birçok sorun eğri. Düzgün gerileme, lojistik gerileme, SVM, LASSO, kıyı gerileme. Bunlar için daha güçlü bir şey var: matematiksel garantilerle optimize. eğri bir sorunun tam olarak bir vadisi vardır. Aşağıya doğru yürüyen herhangi bir algoritma küresel minimum'a ulaşır. Tekrar başlatma gerekmez. Öğrenme oranı programları yoktur. Dua yok.

> Ancak makineler öğrenmesindeki birçok sorun, ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒                                                                                                                                                                                                                               

Konvessiyet'i anlamak üç şey yapar. Birincisi, size sorununuz kolay (konves) ile sert (konvessi olmayan) olduğunda söyler. İkincisi, konves problemleri için Newton'un yöntemi gibi daha hızlı araçlar verir. Üçüncüsü, ML'de ortaya çıkan kavramları açıklar: düzenlenme bir kısıtlama, SVM'lerde çiftelik ve derin öğrenmenin neden her güzel konvessiyetin verilmesine rağmen çalışması.

> Kömfeti anlamak üç rolü vardır. Birincisi, sorunları size anlatır. Birincisi, Kömf problemini anlamak için Newton'un yasası gibi daha hızlı araçlar sunar. Üçincisi, ML'nin kavramını açıklar: normalleşme, SVM'de bir kısıtlama olarak rüntüdür ve neden derin öğrenme, tüm olumlu özelliklerin tersine Kömf ile uyumlu olarak hala geçerlidir.

## Konsepten bir şey.

> **【中文解读】**
> 凸 işlevi şekli bir kase gibi 凸 işlevi sadece en düşük noktayı ⋅ tüm局最优) ⋅ 线性归归、逻辑归归、SVM'in kaybı işlevi tümüyle 凸, bu yüzden eğitim kesinlikle tüm局最优に收 ⋅ 神经网络不凸, 连绵山脉 gibi, ancak SGD pratikte hala iyi bir çözüm bulabilir ⋅ 凸优化 anlaması "ne zaman emin olabiliriz" anlamaktır ⋅

> **【拓展：凸优化在工业中的实际规模】**
> Google'ın reklam sıralama sistemi, büyük çaplı mantıklı geri dönüşü (RPG) kullanıyor, günde milyarlarca kez yapılan istekleri işliyor. SVM, insan yüzü kontrolü (RPG) ve metin sınıflarında yaygın olarak kullanılıyor. Modern LP  çözücü (RPG) Gurobi CPLEX) birkaç dakikada milyonlarca değişkenin linear planlama sorunu çözülebilir. RPG, "en iyi çözümü sağlayacak" birkaç matematik araçtan biridir.

### Konves setleri

Bir S kümesi, S'deki herhangi iki noktaya göre, aralarındaki çizgi bölümü de tamamen S'de bulunursa, konveks olur.

> Eğer toplam S arasında herhangi iki nokta arasındaki çizgi bölümü tamamen S içinde yer alırsa, S ise凸集 (konveks Set) ⋅

| Convex sets | Not convex |
|---|---|
| **Rectangle**: any two points inside can be connected by a line segment that stays inside | **Star/crescent shape**: a line between two interior points can pass outside the set |
| **Triangle**: same property holds for all interior points | **Donut/annulus**: the hole means some line segments leave the set |
| The line segment between any two points stays within the set | The line segment between some pairs of points exits the set |

Formal test: S'deki herhangi bir x, y ve [0, 1]daki herhangi bir t için, tx + (1-t) y noktası da S'de bulunur.

> 形式化测试: S'nin içindeki herhangi bir noktaya x、y 和 [0, 1] arasında herhangi bir t, nokta tx + (1-t) y da S'de。

Konves setlerinin örnekleri:
- Bir çizgi, bir uçak, tüm R^n
  Bir düz çizgi, bir düzlem, tüm R^n
- Bir top (daire, küresi, hipersfer)
  Bir top (öğrenç)
- A yarı alan: {x: a^T x <= b}
  半空间: {x: a^T x <= b}
- Herhangi bir sayıda konveks setin kesişimi
  任意数凸集的交交集

Konveks olmayan kümelerin örnekleri:
- Bir çörek (annulus)
  Çember
- İki bölünmüş çevrenin birleşimi
  İki farklı yönlü bir birleşim
- "Dent" veya " delik" olan herhangi bir set
  "Hepsi bir "Şefer" veya "Döş" birimi

### Konves fonksiyonları

Bir fonksiyon f, domeni bir konveks kümesi ise ve domenindeki herhangi iki noktayı x, y ve [0, 1]'deki herhangi bir t için eğri:

> Eğer f fonksiyonun tanım alanı bir topluğun olduğu ve tanım alanındaki herhangi iki noktayı x、y 和 [0, 1] arasında herhangi bir t için:

```
f(tx + (1-t)y) <= t*f(x) + (1-t)*f(y)
```

Jeometrik olarak: grafikteki herhangi iki nokta arasındaki çizgi bölümü, grafikten yukarıda veya üzerinde bulunur.

> 几何上: çizgi üzerinde herhangi iki nokta arasındaki çizgi bölüm çizgi üzerinde veya çizgi üzerinde yer alır.

| Property | Convex function | Non-convex function |
|---|---|---|
| **Line segment test** | The line between any two points on the graph lies **above or on** the curve | The line between some points on the graph dips **below** the curve |
| **Shape** | Single bowl/valley curving upward | Multiple peaks and valleys with mixed curvature |
| **Local minima** | Every local minimum is the global minimum | Multiple local minima may exist at different heights |

Ortak konveks fonksiyonlar:
- f(x) = x^2 (parabola)
  抛物线
- f(x) = ↓ x (mükemmel değer)
   mutlak değer
- f(x) = e^x (gelişmiş)
  指数函数
- f(x) = max(0, x) (ReLU, parça şeklinde doğrusal olsa da)
  (Devamlı)
- f(x) = -log(x) için x > 0 (negatif log)
  负对数
- Herhangi bir doğrusal fonksiyon f ((x) = a^T x + b (hem konveks hem de konkav)
  任何线性函数 ((既是凸的也是的)

### Çelişkinlik için test

En kolaytan en zorluya kadar üç pratik test.

> Üç çeşit pratik test, en basitten en sertine kadar.

**Test 1: Second derivative test (1D).**Eğer f'(x) >= 0 tüm x için ise f eğri.

> **测试 1：二阶导数测试（一维）。**Eğer tüm x'lere f'(x) >= 0, o zaman f'ın üzerinde bir etkisi vardır.

- f''((x) = x^2: f''(x) = 2 >= 0.
- f'(x) = x^3: f'(x) = 6x. X < 0 için negatif.
- f'(x) = e^x: f'(x) = e^x > 0.

**Test 2: Hessian test (multivariate).**Eğer Hessian matrisi H ((x) tüm x için pozitif yarı belirlenmiş ise, f sarıdır. Hessian ikinci kısmi türevlerin matrisidir.

> **测试 2：Hessian 测试（多变量）。**Eğer Hessian 矩阵 H(x) tüm x için yarımsalı ise, f 凸的──Hessian 矩阵二阶偏导数──

**Test 3: Definition test.**Doğrudan f ((tx + (1-t) y) <= t*f ((x) + (1-t) * f ((y) eşitsizliğini kontrol edin.

> **测试 3：定义测试。**直接检查不等式 f(tx + (1-t) y) <= t*f(x) + (1-t) *f(y)。适用于导数难以计算的函数。

### Neden konveksi önemli

Konves optimizasyonunun merkezi teoremi:

**For a convex function, every local minimum is a global minimum.**

> **对于凸函数，每个局部最小值都是全局最小值。**

Bu da gradient düşüşü tuzağa düşebileceğinden, herhangi bir aşağı yamaç yolu aynı cevaba yol açar.

> Bu, aşağıdaki derecenin sıkışmayacağı anlamına gelir.

> **【中文解读】**
> Bu, kemalizasyonun temel teorisi: kemal işlevinin her bir bölgesel en az değeri tüm bir bölgesel en az değerdir. Bu, derecede düşüşün asla "eşit" bölgesel en iyi yerlerde kalmayacağını gösterir.

```mermaid
graph LR
    subgraph "Convex: ONE answer"
        direction TB
        C1["Loss surface has a single valley"] --> C2["Gradient descent ALWAYS finds the global minimum"]
    end
    subgraph "Non-convex: MANY traps"
        direction TB
        N1["Loss surface has multiple valleys and peaks"] --> N2["Gradient descent may get stuck in a local minimum"]
        N2 --> N3["Global minimum might be missed"]
    end
```

Sonuçlar:
- - İhtiyacın yok .
  Tekrar başlatmak zorunda değilsiniz.
- Gelişmiş öğrenme oranı programlarına gerek yok
  karmaşık öğrenme oranı düzenlemesi gerekmez
- Dönüşüm kanıtları mümkündür (süreklilik fonksiyon özelliklerine bağlıdır)
  % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
- Çözüm benzersiz (taze bölgelerden)
  解是唯一的 (sadece düz bölge dışında)

### ML'de konveks vs konveks olmayan

| Problem | Convex? | Why |
|---------|---------|-----|
| Linear regression (MSE) | Yes | Loss is quadratic in weights |
| Logistic regression | Yes | Log-loss is convex in weights |
| SVM (hinge loss) | Yes | Maximum of linear functions |
| LASSO (L1 regression) | Yes | Sum of convex functions is convex |
| Ridge regression (L2) | Yes | Quadratic + quadratic = convex |
| Neural network (any loss) | No | Nonlinear activations create non-convex landscape |
| k-means clustering | No | Discrete assignment step |
| Matrix factorization | No | Product of unknowns |

Sınırlı kayıplarla çizgi modeller sarıdır.

> 凸损性的线性模型是凸的── eğer 凸损性 aktif olmayan 凸的隐藏层 (associated layer) i eklersen, 凸性 凸的就被破裂──

### Hessian Matrix

Bir fonksiyonun Hessian H'si f: R^n -> R ikinci kısmi türevlerin n x n matrisidir.

> 函数 f: R^n -> R'ın Hessian 矩阵 H 是 n x n'in ikinci aşamasındaki yönlendirme sayı矩阵。

```
H[i][j] = d^2 f / (dx_i dx_j)
```

f ((x, y) = x^2 + 3xy + y^2:

```
df/dx = 2x + 3y       d^2f/dx^2 = 2      d^2f/dxdy = 3
df/dy = 3x + 2y       d^2f/dydx = 3      d^2f/dy^2 = 2

H = [ 2  3 ]
    [ 3  2 ]
```

Hessian, eğrilik hakkında şöyle diyor:
- Eigenvalue'ler tüm pozitif: fonksiyon her yönde yukarı eğrilir (o noktada sarı)
  Özellik değerleri tamamı için doğru: işlevi her yönde tüm yukarı 曲 (→)
- Tüm öz değerleri negatif: her yönde aşağıya eğri (konkaf, yerel maksimum)
  Özellik değerleri: Her yönde tüm aşağı doğru (~)
- Karışık işaretler: otlak noktası (bazı yönlerde yukarı eğri, diğerlerinde aşağı eğri)
  混合符号:点(某些方向上曲,其他方向向下)
- 0 öz değeri: bu yönde düz (degenerasyon)
  零特征值:该方向平坦(退化)

Konvesisite için, Hessian sadece bir noktada değil her yerde pozitif yarı belirlenmiş (tüm öz değerleri >= 0) olmalıdır.

> √√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√

### Newton'un yöntemi

Gradyent inme birinci sıra bilgilerini (gradient) kullanır. Newton'un yöntemi ikinci sıra bilgilerini (Hessian) kullanır.

> 梯度下降使用一阶信息(梯度) ・・・牛顿法使用二阶信息(Hessian) ・・・ bu, mevcut noktada ikinci yaklaşım için uygun olur, sonra doğrudan bu ikinci işlevinin en az değerine atlar.

```
Update rule:
  x_new = x - H^(-1) * gradient

Compare to gradient descent:
  x_new = x - lr * gradient
```

Newton'un yöntemi, skalar öğrenme hızını ters Hessian ile değiştirir. Bu otomatik olarak yerel eğriliği temelinde adım boyutunu ve yönünü ayarlar.

> 牛顿法用逆ヘッシアン 替代标量学习率──これは局部曲率自动调整步长和方向──

> **【拓展：牛顿法在现代 ML 中的实际使用】**
> Newton'un uygulaması derin öğrenimde uygulanmasa da klasik ML'de hâlâ önemli güçtür. XGBoost ve LightGBM her ağacı inşa ederken kayıp işlevi için ikinci aşamada bir çalışma yapılır.

```mermaid
graph TD
    subgraph "Gradient Descent"
        GD1["Start"] --> GD2["Step 1"]
        GD2 --> GD3["Step 2"]
        GD3 --> GD4["..."]
        GD4 --> GD5["Step ~500: Converged"]
        GD_note["Follows gradient blindly — many small steps"]
    end
    subgraph "Newton's Method"
        NM1["Start"] --> NM2["Step 1"]
        NM2 --> NM3["..."]
        NM3 --> NM4["Step ~5: Converged"]
        NM_note["Uses curvature for optimal steps"]
    end
```

Avantajlar:
- En az yakın olan kare dönüşüm (her adımdaki hata kare)
  En az değer yakınında ikinci katlama (Hızlı bir hata)
- Düzenleme için öğrenme oranı yok
  无需调节学习率
- Ölçek değişkenliği (problemi nasıl parametrelediğine bakılmaksızın çalışır)
  尺度不变 (sadece bir iş yapabilmek için)

Eksiklikler:
- Hessian hesaplama O  n ^ 2) hafıza ve O  n ^ 3) tersine maliyet
  計算 Hessian 需要 O(n^2) 内存和 O(n^3) 求逆
- 1 milyon ağırlıklı bir sinir ağı için, yani 10^12 giriş ve 10^18 işlem
  Bir milyon ağırlıklı sinir ağı için 10^12 element ve 10^18 kez hesaplanır.
- Derin öğrenme için pratik değil
  derin öğrenme için uygun değil

### Sınırlı optimizasyon

Sınırsız optimizasyon: tüm x üzerinde f ((x) 'yi en aza indir.
Sınırlı optimizasyon: sınırlara tabi f ((x) 'yi en aza indir.

> 无约束优化: 在所有 x 上最小化 f(x) ・・・约束优化: 在约束条件下最小化 f(x) ・・・

Gerçek sorunların kısıtlamaları vardır. Masrafları en aza indirmek istiyorsunuz ama bütçeniz sınırlıdır. Hataları en aza indirmek istiyorsunuz ama model karmaşıklığınız sınırlıdır.

> Gerçek sorunlar kısıtlılıklara sahiptir. Masrafları en aza indirmek istersin ama bütçe sınırlıdır. Hataları en aza indirmek istersin ama model karmaşıklığı sınırlıdır.

```mermaid
graph LR
    subgraph "Unconstrained"
        U1["Loss function"] --> U2["Free minimum: lowest point of the loss surface"]
    end
    subgraph "Constrained"
        C1["Loss function"] --> C2["Constrained minimum: lowest point within the feasible region"]
        C3["Constraint boundary limits the search space"]
    end
```

### Lagrange çarpıcıları

Lagrange çarpıcıları yöntemi, kısıtlı bir sorunu kısıtlı olmayan bir soruna dönüştürür.

> 拉格朗日乘子法将束问题转化为无束问题.

Sorun: g(x) = 0 ile f ((x) ı en aza indirmek.

Çözüm: yeni bir değişken (Lagrange çarpıcı lambda) ekle ve kısıtlama olmayan sorunu çöz:

```
L(x, lambda) = f(x) + lambda * g(x)
```

Çözümde L'nin gradiyenti sıfırdır:

```
dL/dx = df/dx + lambda * dg/dx = 0
dL/dlambda = g(x) = 0
```

Geometrik algı: kısıtlı minimumda, f'nin gradiyenti kısıtlama g'nin gradiyenti ile paralel olmalıdır. Eğer paralel değillerse, kısıtlama yüzeyi boyunca hareket edip f'yi daha da azaltabilirsiniz.

> 几何直觉:                                                                                                                                                                                                                                                            

```mermaid
graph LR
    A["Contours of f(x,y): concentric ellipses"] --- S["Solution point"]
    B["Constraint curve g(x,y) = 0"] --- S
    S --- C["At the solution, gradient of f is parallel to gradient of g"]
```

Örnek: f ((x,y) = x^2 + y^2'yi x + y = 1'e tabi olarak en aza indir.

```
L = x^2 + y^2 + lambda(x + y - 1)

dL/dx = 2x + lambda = 0  =>  x = -lambda/2
dL/dy = 2y + lambda = 0  =>  y = -lambda/2
dL/dlambda = x + y - 1 = 0

From first two: x = y
Substituting: 2x = 1, so x = y = 0.5, lambda = -1
```

X + y = 1 çizgisindeki en yakın nokta (0,5, 0,5)

> Doğrudan x + y = 1 yukarıdaki ilk nokta (0.5, 0.5)

### KKT koşulları

Karush-Kuhn-Tucker koşulları Lagrange çarpıcılarını eşitsizlik kısıtlamalarına kadar uzattır.

> KKT 条件(Karush-Kuhn-Tucker Şartları) will拉格朗日乘子推广到不等式约束──

Sorun: i = 1, ..., m için g_i(x) <= 0 ile sınırlı f ((x) en az azaltmak.

KKT koşulları (optimallık için gerekli):

```
1. Stationarity:    df/dx + sum(lambda_i * dg_i/dx) = 0
2. Primal feasibility:  g_i(x) <= 0  for all i
3. Dual feasibility:    lambda_i >= 0  for all i
4. Complementary slackness:  lambda_i * g_i(x) = 0  for all i
```

Eklemci gevşeklik anahtar bir anlayıştır: ya kısıtlama aktifdir (g_i = 0, çözünürlük sınır üzerinde oturur) veya katılatıcı sıfırdır (sıkıntı önemi yoktur).

> 互补松性(Complementary Slackness) ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒    ⇒ ⇒  ⇒                                                                                                                                                  

KKT koşulları SVM'lerin merkezi konumdadır. Destek vektörleri kısıtlamanın aktif olduğu veri noktalarıdır (lambda > 0). Diğer tüm veri noktalarının lambda = 0'u vardır ve karar sınırını etkilemez.

> KKT 条件是 SVM'nin merkezi. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持向量. 支持. 支持向量. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持. 支持.

> **【中文解读】**
> KKT 条件は拉格朗日乘子の推广版,处理不等式约束──互补松性 en精妙洞察: her bir kısım için, ister "aktif" olur, isterse çözüme etkisi olmayan bir çözüm için geçerlidir.

### Düzenlendirme kısıtlı optimizasyon olarak

L1 ve L2 düzenlenmesi keyfi hileler değil, maskeli kısıtlı optimizasyon problemleri.

> L1 ve L2 düzenleme isteksiz teknikler değildir.

**L2 regularization (Ridge):**

```
minimize  Loss(w)  subject to  ||w||^2 <= t

Equivalent unconstrained form:
minimize  Loss(w) + lambda * ||w||^2
```

Bu kısıtlama bir topu tanımlar (dörtlü 2D, küre 3D).

> 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约  约 约                                                                                                                                                             

**L1 regularization (LASSO):**

```
minimize  Loss(w)  subject to  ||w||_1 <= t

Equivalent unconstrained form:
minimize  Loss(w) + lambda * ||w||_1
```

Sınırlılık çiçekler bir elmas (dört boyutlu bir dönüm) tanımlar.

> 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约束 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 约 

| Property | L2 constraint (circle) | L1 constraint (diamond) |
|---|---|---|
| **Constraint shape** | Circle (sphere in higher dims) | Diamond (rotated square in 2D) |
| **Where loss contour touches** | Smooth boundary — any point on the circle | Corner — aligned with an axis |
| **Solution behavior** | Weights are small but nonzero | Some weights are exactly zero (sparse) |
| **Result** | Weight shrinkage | Feature selection |

Bu, L1'nin neden nadir modeller ürettiğini (önümlük seçimi) açıklarken L2'nin sadece ağırlıkları azaltmasının nedenini açıklar. Elmasın ekselerle uyumlu köşeleri vardır. Kayıp konturların bir köşe dokunma olasılığı daha yüksektir, bir veya daha fazla ağırlığı tam olarak sıfıra ayarlar.

> Bu neden L1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

> **【拓展：L1 正则化与 L2 正则化的几何直觉】**
> L1 束 şekli 形(2D'de dönerken düz kare şeklidir), L2 束 şekli yuvarlaktır. 形角yi 形ün köşe üzerinde yerleştirir. Bu nedenle, 高線 daha kolay bir köşede çarpılır. Bu da belirli ağırlıkların kesin olarak sıfır olarak belirlenmesi anlamına gelir.  Özellik seçimi.

### İkiliğe

Her kısıtlı optimizasyon sorunu (birincil) bir eş sorunu (ikili) vardır. Konves problemler için, birincil ve ikili aynı optimal değere sahiptir. Bu güçlü bir ikili.

> Her kısım optimizasyon sorusu ([[original problem]]) bir yanlısı sorunu vardır.

Lagrangian çift fonksiyonu:

```
Primal: minimize f(x) subject to g(x) <= 0
Lagrangian: L(x, lambda) = f(x) + lambda * g(x)
Dual function: d(lambda) = min_x L(x, lambda)
Dual problem: maximize d(lambda) subject to lambda >= 0
```

İkiliğin neden önemli olduğu:
- İkilem problemini çözmek bazen ilk problemden daha kolay.
  Bir çift sorunun çözümü bazen orijinal sorunun çözümü için daha kolaydır.
- SVM'ler ikili şeklinde çözülür, burada sorun veri noktaları arasındaki nokta ürünlerine bağlıdır (kernel hilesini etkinleştirir)
  SVM, sorunların çözümü için bir arada bir şekil kullanılır.
- Dual, çözünürlük kalitesini kontrol etmek için yararlı olan ilk optimum'un alt sınırını sağlar.
  İlk en iyi değer için aşağı sınırı sağlanarak, test çözülmesi için kullanılır.

Özellikle SVM için:

```
Primal: find w, b that maximize the margin 2/||w|| subject to
        y_i(w^T x_i + b) >= 1 for all i

Dual:   maximize sum(alpha_i) - 0.5 * sum_ij(alpha_i * alpha_j * y_i * y_j * x_i^T x_j)
        subject to alpha_i >= 0 and sum(alpha_i * y_i) = 0

The dual only involves dot products x_i^T x_j.
Replace x_i^T x_j with K(x_i, x_j) to get the kernel trick.
```

### Derin öğrenmenin neden konveksiyetsiz olmasına rağmen işe yarıyor

Neural ağ kaybı fonksiyonları oldukça konveks değildir. Her klasik ölçümle, onları optimize etmek başarısız olmalıdır.

> Neural net kaybı işlevi son derece belirsiz. Klasik teorilere göre, optimize edilmesi gerekenler başarısızdır.

**Most local minima are good enough.**Yüksek boyutlu alanlarda, rastgele kritik noktalar (gelişme sıfır olduğu yerlerde) yerel minimumlar değil, büyük ölçüde otlak noktalarıdır. Var olan birkaç yerel minimum, küresel minimumın yakınında kayıp değerlerine sahip olma eğilimindedir. Parametre alanının milyonlarca boyutunda olduğu zaman korkunç bir yerel minimumda sıkışmak son derece muhtemel değildir.

> **大多数局部最小值都足够好。**Yüksek seviye alanında, as机临界点 (梯度为零的点) büyük çoğunluğu 点, yerel en az değerdir.

**Saddle points, not local minima, are the real obstacle.**N parametre olan bir fonksiyonda, bir sedil noktası pozitif ve negatif eğrilik yönlerinin bir karışımına sahiptir. Yüksek boyutlarda rastgele bir kritik noktada, tüm n öz değerlerinin pozitif olma olasılığı (yerel minimum) yaklaşık 2 ^ - n'dir.

> **鞍点而非局部最小值才是真正的障碍。**Bu nedenle, bu değerlerin birbiriyle birlikte olması için, bu değerlerin birbiriyle birlikte olması gerekir. Bu değerlerin birbiriyle birlikte olması için, bu değerlerin birbiriyle birlikte olması gerekir.

**Overparameterization smooths the landscape.**Eğitim örneklerinden daha fazla parametreye sahip ağlar daha düzgün, daha bağlantılı kayıp yüzeylerine sahiptir. Daha geniş ağlar daha az kötü yerel minimumlara sahiptir. Bu, mantık dışı ancak empiri olarak tutarlıdır.

> **过参数化（Overparameterization）使损失面更平滑。**参数 daha fazla olan eğitim örneği ağ daha düz, daha bağlantılı kayıp yüzü vardır.  Daha geniş ağ daha az kötü yerlerin en az değerine sahiptir.

**Loss landscape structure:**

| Property | Low-dimensional space | High-dimensional space |
|---|---|---|
| **Landscape** | Many isolated peaks and valleys | Smoothly connected valleys |
| **Minima** | Many isolated local minima | Few bad local minima; most are near-optimal |
| **Navigation** | Hard to find global minimum | Many paths lead to good solutions |
| **Critical points** | Mix of local minima and saddle points | Overwhelmingly saddle points, not local minima |

**Stochastic noise acts as implicit regularization.**Mini-batch SGD, keskin minimumlara yerleşmeyi engelleyen gürültü ekler. Keskin minimumlar aşırı uyum sağlar; düz minimumlar genelleştirir. Gürültü kayıp manzarasının düz bölgelerine yönelik optimize etmeyi engeller.

> **随机噪声充当隐式正则化。**Mini-batch SGD                                                                                                                                                                                                                                                            

> **【中文解读】**
> Derin öğrenme başarısı, kam optimizasyon teorisine aykırı görünüyor: Kımsız işlevi çok zor optimizasyon yapmalıdır, ancak SGD çok iyi çalışıyor. Sebep üçtür: Birincisi, yüksek seviye alanındaki neredeyse tüm kritik noktalar yeral minimum değeri değil, noktalardır; ikincisi, aşırı parametreleme kayıpların yüzeyi daha düz hale getirir; üçüncü olarak, SGD'nin gürültüsü gizli düzeltme olarak yüklenir, en küçük değerlerden kaçmaya yardımcı olur, daha düzeltme                                                                                                                                                                                                    

### İkinci sırada uygulanan yöntemler

Pure Newton'un yöntemi büyük modeller için pratik değildir.

> 純牛頓法對大模型不實用──二段信息可用── birkaç yaklaşımlı yöntem kullanılabilir hale getirir.

**L-BFGS (Limited-memory BFGS):**Son m gradient farklarını kullanarak ters Hessian'ı yaklaştırır. O(n^2 yerine O(mn) belleği gerektirir. ~ 10,000 parametre kadar olan sorunlar için iyi çalışır. Klasik ML (logistik geri dönüş, CRF) ama derin öğrenme için kullanılır.

> **L-BFGS：**O'n'n'n'2) değil O'n'n'den daha fazla 10.000 个参数 sorusu için kullanılır.

**Natural gradient:**Standart Hessian yerine Fisher bilgi matrisini (log- olasılık beklenen Hessian) kullanır. Bu olasılık dağılımlarının jeometri için hesap verir. K-FAC (Kronecker-Faktörlü Yaklaşım Kürürümesi) Fisher matrisini Kronecker ürünü olarak yaklaştırır ve sinir ağları için pratik hale getirir.

> **自然梯度（Natural Gradient）：**Fisher 信息矩阵 (Hessian) Hessian standartının yerine Hessian 信息矩阵 (Hessian) kullanın. Bu, olasılık dağılımının geometrik yapısını göz önünde bulundurur.

**Hessian-free optimization:**Hx = g'yi hiçbir zaman H oluşturmadan çözmek için konjugat gradiyenti kullanır. Sadece otomatik farklılaşma yoluyla O ((n) zamanında hesaplanabilen Hessian vektör ürünlerini gerektirir.

> **无 Hessian 优化：**Hx = g ve H. oluşumunu kullanmak için H. Hessian-向量乘积, otomatik olarak O (n) 时间内计算.

**Diagonal approximations:**Adam'ın ikinci anı, Hessian'ın diyagonalının diyagonal yaklaşımıdır. AdaHessian bunu Hutchinson'un tahmincisi aracılığıyla gerçek Hessian diyagonal unsurlarını kullanarak genişletiyor.

> **对角近似：**Adam'ın ikinci aşaması Hessian'ın köşelerin köşelerine yaklaşımıdır. AdaHessian Hutchinson tarafından gerçek Hessian köşelerine yaklaşımını genişletmek için değerlendirme cihazı kullanıyor.

| Method | Memory | Per-step cost | When to use |
|--------|--------|--------------|-------------|
| Gradient descent | O(n) | O(n) | Baseline, large models |
| Newton's method | O(n^2) | O(n^3) | Small convex problems |
| L-BFGS | O(mn) | O(mn) | Medium convex problems |
| Adam | O(n) | O(n) | Deep learning default |
| K-FAC | O(n) | O(n) per layer | Research, large-batch training |

## Yapın.
```figure
convex-vs-nonconvex
```

## Yapın

### Adım 1: Konvesitlik kontrolü

Örnek noktaları ve tanımı kontrol ederek konvessiyetini empiri olarak test eden bir fonksiyon oluşturun.

>  bir işlevi oluşturmak, örnek noktayı ve kontrol tanımını kullanarak deneysel olarak test etmektedir.

```python
import random
import math

def check_convexity(f, dim, bounds=(-5, 5), samples=1000):
    violations = 0
    for _ in range(samples):
        x = [random.uniform(*bounds) for _ in range(dim)]  # 随机采样点 x
        y = [random.uniform(*bounds) for _ in range(dim)]  # 随机采样点 y
        t = random.uniform(0, 1)                            # 随机混合系数
        mid = [t * xi + (1 - t) * yi for xi, yi in zip(x, y)]  # 凸组合 tx + (1-t)y
        lhs = f(mid)                                        # f(凸组合)
        rhs = t * f(x) + (1 - t) * f(y)                    # tf(x) + (1-t)f(y)
        if lhs > rhs + 1e-10:                               # 违反凸性不等式
            violations += 1
    return violations == 0, violations
```

### Adım 2: 2D için Newton'un yöntemi

Newton'un yöntemini açık bir Hessian kullanarak uygulayın.

> Newton'un yöntemini gerçekleştirmek için açık Hessian kullanılmıştır.

```python
def newtons_method(f, grad_f, hessian_f, x0, steps=50, tol=1e-12):
    x = list(x0)
    history = [x[:]]
    for _ in range(steps):
        g = grad_f(x)
        H = hessian_f(x)
        det = H[0][0] * H[1][1] - H[0][1] * H[1][0]
        if abs(det) < 1e-15:
            break
        H_inv = [
            [H[1][1] / det, -H[0][1] / det],
            [-H[1][0] / det, H[0][0] / det],
        ]
        dx = [
            H_inv[0][0] * g[0] + H_inv[0][1] * g[1],
            H_inv[1][0] * g[0] + H_inv[1][1] * g[1],
        ]
        x = [x[0] - dx[0], x[1] - dx[1]]
        history.append(x[:])
        if sum(gi ** 2 for gi in g) < tol:
            break
    return history
```

### Adım 3: Lagrange çarpıcı çözücü

Lagrangian'daki gradient düşüşünü kullanarak kısıtlı optimizasyonu çözün.

> LaGlang gün işlevi üzerinde gradient aşağı aşağı

```python
def lagrange_solve(f_grad, g_val, g_grad, x0, lr=0.01,
                   lr_lambda=0.01, steps=5000):
    x = list(x0)
    lam = 0.0
    history = []
    for _ in range(steps):
        fg = f_grad(x)
        gv = g_val(x)
        gg = g_grad(x)
        x = [
            xi - lr * (fgi + lam * ggi)
            for xi, fgi, ggi in zip(x, fg, gg)
        ]
        lam = lam + lr_lambda * gv
        history.append((x[:], lam, gv))
    return history
```

### Adım 4: Birinci sırayı ikincisi sıraya karşı karşılaştır

Aynı kare işlevi üzerinde gradient düşüşünü ve Newton'un yöntemini çalıştırın.

```python
def quadratic(x):
    return 5 * x[0] ** 2 + x[1] ** 2

def quadratic_grad(x):
    return [10 * x[0], 2 * x[1]]

def quadratic_hessian(x):
    return [[10, 0], [0, 2]]
```

Newton'un yöntemi 1 adımla (kvadratik için tamdır) birleştiğinde, derecelendirme yüzlerce adım sürecek çünkü Hessian'ın öz değerleri 5 katı farklılık göstererek uzanan bir vadide oluşur.

> Newton'un kuralları, ikinci işlevi için bir adım içinde alınması gereken bir adımdır.

## Çerçeveyi kullanın.

Çelişkililik analizi, ML modellerini ve çözücüleri seçerken doğrudan uygulanır.

> 凸性分析在选择ML 模型和求解器当中直接适用──

Konves sorunlar için (logistik gerileme, SVM, LASSO):
- Özel çözücüler kullanın (liblinear, CVXPY, scipy.optimize.minimize method='L-BFGS-B')
  Özel arama makinesi kullanın
- Eşsiz bir küresel çözüm bekleyin
  期望唯一的全局解
- İkinci sırada uygulanabilir ve hızlı yöntemler
  İkinci aşama yöntem uygundur ve hızlı

Konveks olmayan problemler için (nervüler ağlar):
- İlk sıradaki yöntemleri kullanın (SGD, Adam)
  Bir aşama yöntem kullan
- Çözümün başlangıç ve rastlantıya bağlı olduğunu kabul edin
  接受解依赖于初始化和随机性
- İstifadeden dolayı düzenlenme olarak aşırı parametreleştirme, gürültü ve öğrenme hızı programlarını kullanın
  Sıcaklık, gürültü ve öğrenme oranı düzenlemesini bir normalleştirme olarak kullanmak
- Yerel minimum için zaman harcamayın.
  Zamanınızı boşa harcamayın. İyi bir yerin en az değeri yeter.

```python
from scipy.optimize import minimize

result = minimize(
    fun=lambda w: sum((y - X @ w) ** 2) + 0.1 * sum(w ** 2),
    x0=np.zeros(d),
    method='L-BFGS-B',
    jac=lambda w: -2 * X.T @ (y - X @ w) + 0.2 * w,
)
```

SVM için, çift formülasyon çekirdek hilesini kullanmanıza olanak tanır:

> -SVM için, bazı durumlarda nükleer teknikler kullanmanızı sağlayın.

```python
from sklearn.svm import SVC

svm = SVC(kernel='rbf', C=1.0)
svm.fit(X_train, y_train)
print(f"Support vectors: {svm.n_support_}")
```

## Egzersizler.

1. **Convexity gallery.**Bu fonksiyonları şıklık için kontrolci kullanarak test edin: f(x) = x^4, f(x) = sin(x), f(x,y) = x^2 + y^2, f(x,y) = x*y, f(x) = max(x, 0).

2. **Newton vs gradient descent race.**Her iki yöntemi de f ((x,y) = 50*x^2 + y^2 olarak başlatın (10,10).

3. **Lagrange multiplier geometry.**f ((x,y) = (x-3)^2 + (y-3)^2 x + 2y = 4 ile sınırlı olarak en azı azaltın.

4. **Regularization constraint.**L1 kısıtlı optimizasyonu uygulayın: (x-3)^2 + (y-2)^2'yi azaltın, bu sayede \x \x \y \y \ \y \ <= 1. Çözümün sıfır eşit bir koordinat olduğunu gösterin (erlinç kısıtlamasından uzaklık).

5. **Hessian eigenvalue analysis.**Rosenbrock fonksiyonunun Hessian'ı (1,1) ve (-1,1) ile hesaplayın.

## Anahtar Şartlar .

| Term | What it means |
|------|---------------|
| Convex set | A set where the line segment between any two points in the set stays inside the set |
| Convex function | A function where the line between any two points on its graph lies above or on the graph. Equivalently, Hessian is positive semidefinite everywhere |
| Local minimum | A point lower than all nearby points. For convex functions, every local minimum is the global minimum |
| Global minimum | The lowest point of a function over its entire domain |
| Hessian matrix | The matrix of all second partial derivatives. Encodes curvature information |
| Positive semidefinite | A matrix whose eigenvalues are all non-negative. The multidimensional analogue of "second derivative >= 0" |
| Condition number | Ratio of largest to smallest eigenvalue of the Hessian. High condition number means elongated valleys and slow gradient descent |
| Newton's method | Second-order optimizer that uses the inverse Hessian to determine step direction and size. Quadratic convergence near the minimum |
| Lagrange multiplier | A variable introduced to convert a constrained optimization problem into an unconstrained one |
| KKT conditions | Necessary conditions for optimality with inequality constraints. Generalize Lagrange multipliers |
| Complementary slackness | At the solution, either a constraint is active or its multiplier is zero. Never both nonzero |
| Duality | Every constrained problem has a companion dual problem. For convex problems, both have the same optimal value |
| Strong duality | Primal and dual optimal values are equal. Holds for convex problems satisfying Slater's condition |
| L-BFGS | Approximate second-order method that stores the last m gradient differences instead of the full Hessian |
| Saddle point | A point where the gradient is zero but it is a minimum in some directions and a maximum in others |
| Overparameterization | Using more parameters than training examples. Smooths the loss landscape and reduces bad local minima |

## Daha fazla okumak

- [Boyd & Vandenberghe: Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/)- standart ders kitabı, internette ücretsiz olarak kullanılabilir
- [Bottou, Curtis, Nocedal: Optimization Methods for Large-Scale Machine Learning (2018)](https://arxiv.org/abs/1606.04838)- Köprüler, konveks optimizasyon teorisi ve derin öğrenme uygulaması
- [Choromanska et al.: The Loss Surfaces of Multilayer Networks (2015)](https://arxiv.org/abs/1412.0233)- neden konveks olmayan sinir ağları manzaraları görünüşleri kadar kötü değil
- [Nocedal & Wright: Numerical Optimization](https://link.springer.com/book/10.1007/978-0-387-40065-5)- Newton'un yöntemi, L-BFGS ve kısıtlı optimizasyon için kapsamlı bir referans
