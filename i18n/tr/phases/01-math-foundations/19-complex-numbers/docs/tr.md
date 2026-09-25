# AI için karmaşık sayılar.

> -1'in kare kökü hayal edici değil. Dönüşümlerin, frekansların ve sinyal işleme yarısının anahtarıdır.
> -1'in kare kökü "yalan" değil. Bu, dönüm, frekans ve yarım sinyal işleme alanının anahtarıdır.

**Type:** Learn | **类型:** 学习
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04 (linear algebra, calculus) | **前置知识:** Phase 1, 第 01-04 课（线性代数、微积分）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Öğrenme hedefleri

- Katı ve kutup şeklinde karmaşık aritmetik (ekle, kat, böl, birleştir) yapın
  执行复数运算(加、乘、除、共),直角坐标和极坐标形式 dahil
- Karmaşık eksponensialler ve trigonometrik fonksiyonlar arasında dönüştürmek için Euler'in formülünü uygulayın
  应用欧拉公式在复指数和三角函数之间转换
- Karmaşık birlik köklerini kullanarak Diskret Fourier Transform uygulamak
  İşe yarayan birim için ayrıntılı bir değişiklik yapın
- Transformatörlerde RoPE ve sinusoidal pozisyon kodlamalarının karmaşık dönümlerin nasıl altında olduğunu açıklayın.
  解释复数旋转 RoPE ve Transformer nasıl yapılandırılır 正弦位置编码的基础


> **【中文解读】**
> 虚数 i, dönüşüm ve frekans anahtarıdır. Transformer içindeki RoPE 位置编码 (Role)  LLaMA ve diğer modeller kullanımı) aslında dönüşümün bir parçasıdır.

## Sorunlar. Sorunlar.

Fourier dönüşümleri üzerine bir makale açarsanız , orada bir şey var .`i`Transformer konum kodlamalarına bakıp görebilirsiniz.`sin`ve `cos`karmaşık eksponensallerin gerçek ve hayalsel kısımları. Kuantum bilgisayarı hakkında okuyorsunuz ve karmaşık vektör alanlarında ifade edilen her şeyi bulursunuz.

> Bir makale açtınız.`i`◊You see Transformer 位置编码, see different frequency of `sin`和 `cos` bunlar, tekrar göstergelerinin gerçek ve gerçek bölümleridir.

Karmaşık sayılar soyut görünüyor. -1 kare kökü üzerine inşa edilmiş bir sayı sistemi bir matematik hilesi gibi hisseder. Ama bu bir hile değil. Bu dönüm ve titreşimlerin doğal dili. Bir şey her döndüğünde, titreştiğinde veya titreştiğinde, karmaşık sayılar doğru araçtır.

> 复数 çok soyut görünüyor. -1'in kare kökü üzerinde kurulan sayısal sistem, matematik oyunları gibi hissettirilir. Fakat oyun değildir.

Karmaşık sayıları anlamadan, Diskret Fourier Transform'u anlayamazsınız. FFT'yi anlayamazsınız. RoPE (Rotary Position Embedding) modern dil modellerinde nasıl çalışır anlamıyorsunuz.

> Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Çeviri Çeviri Çeviri Ç Çeviri Çeviri Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

Bu ders karmaşık aritmetikleri sıfırdan inşa eder, jeometriyle bağlar ve makine öğreniminde karmaşık sayılar tam olarak nerede göründüğünü gösterir.

> Bu ders, sıfırdan yapılandırma ve sayısal işlemlerle bağlantılıdır ve makine öğreniminde ortaya çıkan sayısal konumları doğru bir şekilde gösterir.

## Konsepten bir şey.

> **【中文解读】**
> 复数的核心洞察:i 不是"虚"的,它是一次回旋操作――乘一次 i 转 90 度,乘两次(i^2 = -1)转 180 度──复数 = 2D düzlemdeki nokta +自然支持旋转── bu, dönüş, titreşim, frekansla ilgili herhangi bir alanın doğal olarak çoklu tanımlamaya uygun olduğu anlamına gelir──

> **【拓展：复数在 AI 中的实际应用规模】**
> OpenAI'nın GPT-4、Meta'nın LLaMA 系列leri RoPE(Rotary Position Embedding) kullanıyor, aslında bu sayı dönüştürülüyor.

### Karmaşık bir sayı nedir?

Karmaşık bir sayı iki parçaya sahiptir: gerçek bir bölüm ve hayali bir bölüm.

> 复数有两部分:实部 (Gerçek Bölüm) 和虚部 (Yüce Bölüm)

```
z = a + bi

where:
  a is the real part
  b is the imaginary part
  i is the imaginary unit, defined by i^2 = -1
```

Bu sayılar, bir düzlemde, gerçek sayılar bir tarafa, hayal sayılar diğer tarafa, her karmaşık sayı bu düzlemde bir nokta.

> İşte böyle. Sayı aksideni bir düzine yayıyorsun. Gerçek sayı bir düzende.

### Karmaşık aritmetik

**Addition.**Gerçek parçaları bir araya getirin, hayali parçaları bir araya getirin.

> **加法。**Gerçek bir şey, gerçek bir şey.

```
(a + bi) + (c + di) = (a + c) + (b + d)i

Example: (3 + 2i) + (1 + 4i) = 4 + 6i
```

**Multiplication.**Paylaştırma yasasını kullanın ve i^2 = -1 olduğunu unutmayın.

> **乘法。**Uygulama kuralını kullan, i^2 = -1

```
(a + bi)(c + di) = ac + adi + bci + bdi^2
                 = ac + adi + bci - bd
                 = (ac - bd) + (ad + bc)i

Example: (3 + 2i)(1 + 4i) = 3 + 12i + 2i + 8i^2
                            = 3 + 14i - 8
                            = -5 + 14i
```

**Conjugate.**Hayal gücünün işaretini çevir.

> **共轭（Conjugate）。**翻转虚部的符号──

```
conjugate of (a + bi) = a - bi
```

Karmaşık bir sayının ve onun eşleşmesinin ürünü her zaman gerçek olur:

> 复数与其共的乘积总是实数:

```
(a + bi)(a - bi) = a^2 + b^2
```

**Division.**Sayıcı ve adlendiricini adlendiricinin birleşikliği ile çarpın.

> **除法。**分子 ve分母 aynı zamanda 分母'nin toplamını çarpıyor.

```
(a + bi) / (c + di) = (a + bi)(c - di) / (c^2 + d^2)
```

Bu, isimlendiriciden hayali kısmı ortadan kaldırır ve size temiz karmaşık bir sayı verir.

> Bu da, bölümlerin boş bölümlerini ortadan kaldırır ve net bir çift elde eder.

### Karmaşık düzlem

Karmaşık düzlem her karmaşık sayıyı 2 boyutlu bir noktaya haritası yapar. Düz ekseni gerçek ekseni, dikey ekseni hayal ekseni.

> 复平面将每复数映射为2D点──水平轴是实轴,垂直轴是虚轴──

```
z = 3 + 2i  corresponds to the point (3, 2)
z = -1 + 0i corresponds to the point (-1, 0) on the real axis
z = 0 + 4i  corresponds to the point (0, 4) on the imaginary axis
```

Karmaşık bir sayı aynı zamanda bir noktayı ve bir kaynağı olan vektördür. Bu çift yorumlama karmaşık sayıları jeometri için yararlı kılan şeydir.

> 复数 aynı zamanda bir noktayı ve bir başlangıç noktasından çıkan bir yayını oluşturur. Bu ikili açıklama, çok faydalı bir geometrik anlamda kullanılır.

### Kutup şekli

Düzende herhangi bir nokta, kökeninden uzaklığı ve pozitif gerçek eksiden açısı ile tanımlanabilir.

> Eklentide herhangi bir nokta, öz noktasından uzaklık ve gerçek aksanın açısından tanımlanabilir.

```
z = r * (cos(theta) + i*sin(theta))

where:
  r = |z| = sqrt(a^2 + b^2)     (magnitude, or modulus)
  theta = atan2(b, a)             (phase, or argument)
```

Dörtgenlik biçimi (a + bi) eklemek için iyidir. Polar biçimi (r, theta) çarpma için iyidir.

> 直角坐标形式 (a + bi) 适合加法。极坐标形式 (r, theta) 适合乘法。

**Multiplication in polar form.**Büyüklükleri çarpıp açıları ekleyin.

> **极坐标形式的乘法。**模相乘,角相加──

```
z1 = r1 * e^(i*theta1)
z2 = r2 * e^(i*theta2)

z1 * z2 = (r1 * r2) * e^(i*(theta1 + theta2))
```

Bu yüzden karmaşık sayılar dönümler için mükemmel. 1 büyüklüğü ile karmaşık sayılarla çarpmak saf bir dönümdür.

> Bu yüzden bir çarpı tam olarak dönmeye uygun bir çarpıdır.

### Euler'in formülü

Karmaşık eksponensal ve trigonometri arasındaki köprü:

> 复指数 ile 三角函数 arasındaki köprü:

```
e^(i*theta) = cos(theta) + i*sin(theta)
```

Bu dersdeki en önemli formül.

> Bu, dersinin en önemli formülü.

```
e^(i*pi) = cos(pi) + i*sin(pi) = -1 + 0i = -1

Therefore: e^(i*pi) + 1 = 0
```

Beş temel sabit (e, i, pi, 1, 0) bir denklemde birbirine bağlanmıştır.

> 五个基本常数 ((e、i、pi、1、0) 统一在一个方程中──

### Euler'ın formülü ML için neden önemlidir

Euler'in formülü bunu söylüyor.`e^(i*theta)`Theta = 0, teta = pi/2, teta = pi = 0, teta = 1, teta = 2, teta = 1, teta = 3, teta = 3, teta = 0, teta = 2, teta = 2, teta = 2, teta = 2, teta = 2, teta = 2, teta = 2, teta = 2, teta = 2, teta = 2, teta = 1, teta = 2, teta = 1, teta = 2, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 1, teta = 2, teta = 1, teta = 1, teta = 2, teta = 1, teta = 1, teta = 2, teta = 1, teta = 1, teta = 2, teta = 1, teta = 2, teta = 1, teta = 2, teta = 2, teta = 1, teta = 2, t = 1, teta = 2, t = 1, t = 2, t = 1, t = 2, t = 2, t = 1, t = 2, t = 2, t = 1, t = 2, t = 2, t = 2, t = 2, t = 1, t = 2, t = 1, t = 2, t = 2, t = 1, t = 2, t = 1, t = 2, t = 1, t = 2, t = 2, t = 2, t = 2, t = 1, t = 2, t = = 1, t = 2, t = = 2, t = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

> 欧拉公式说 `e^(i*theta)`随着thea 变化描绘单位圆――theta = 0 时在 (1, 0) ・・・theta = pi/2 时在 (0, 1) ・・・theta = pi 时在 (-1, 0) ・・・theta = 3*pi/2 时在 (0, -1) ・・・完整旋转是thea = 2*pi。

Bu karmaşık eksponensialler Dönüştürücüdür ve sinyal işleme ve ML'de her yerde dönüştür.

> Bu da, tekrar gösterge dönüşümdür.

> **【中文解读】**
> 欧拉公式 e^(i*theta) = cos(theta) + i*sin(theta) bu sınıfın en önemli formülüdür. Bu da indeks işlevi ve üçgen işlevi bir arada getirir, ayrıca tekrarlama ve dönüşüm bir arada getirir.

### 2D dönüşümlere bağlanmak

Karmaşık sayıyı (x + yi) e^(i*theta ile çarpırsak, noktayı (x, y) köşe theta tarafından köken etrafında döndürür.

> 将复数 (x + yi) 乘以 e^(i*theta) 将点 (x, y) 绕原点旋转角 theta。

```
Rotation via complex multiplication:
  (x + yi) * (cos(theta) + i*sin(theta))
  = (x*cos(theta) - y*sin(theta)) + (x*sin(theta) + y*cos(theta))i

Rotation via matrix multiplication:
  [cos(theta)  -sin(theta)] [x]   [x*cos(theta) - y*sin(theta)]
  [sin(theta)   cos(theta)] [y] = [x*sin(theta) + y*cos(theta)]
```

Bu iki metrekal bir dönüştürücü matrisin bir matris notasyonunda yazılmış karmaşık çarpma.

> 它们产生完全相同的结果──复数乘法就是2D 旋转──旋矩阵只是用矩阵符号写出的复数乘法──

```mermaid
graph TD
    subgraph "Complex Multiplication = 2D Rotation"
        A["z = x + yi<br/>Point (x, y)"] -->|"multiply by e^(i*theta)"| B["z' = z * e^(i*theta)<br/>Point rotated by theta"]
    end
    subgraph "Equivalent Matrix Form"
        C["vector [x, y]"] -->|"multiply by rotation matrix"| D["[x cos theta - y sin theta,<br/> x sin theta + y cos theta]"]
    end
    B -.->|"same result"| D
```

### Fasorlar ve dönük sinyaller

Karmaşık bir eksponensal e^(i*omega*t) açı frekansı omega'da birim döngüsünün etrafında dönen bir noktayır. t arttıkça nokta döngüyü izler.

> 复指数 e^(i*omega*t) 角频 omega 绕单位圆旋转的点──随着t 增加,点描绘出圆──

Bu dönüm noktasının gerçek kısmı cos(omega*t) imajür kısmı sin(omega*t) sinusoidal bir sinyal dönümlü bir karmaşık sayının gölgesidir.

> Bu dönüm noktasının gerçek kısmı cosmososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososososos

```
e^(i*omega*t) = cos(omega*t) + i*sin(omega*t)

Real part:      cos(omega*t)    -- a cosine wave
Imaginary part: sin(omega*t)    -- a sine wave
```

Bu fazör temsilidir. Bir sinüs dalgasını izlemek yerine, düzgün bir şekilde dönen bir ok izlersiniz. Faz değişimleri açı bozuklukları haline gelir. Amplitude değişiklikleri büyüklük değişimleri haline gelir. Sinyal eklemesi vektör eklemesi haline gelir.

> İşte fazometre f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f.s. f. f.s. f. f.s. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f. f.

### Birliğin Temelleri

Birlik köklerinin N-th kökü, birlik dairesinde eşit derecede uzanan N noktalardır:

> N 次单位根(Birliğin Kökleri) n 个点分布的单位圆上等间间间分布的 N 个点:

```
w_k = e^(2*pi*i*k/N)    for k = 0, 1, 2, ..., N-1
```

N = 4 için kökler şunlardır: 1, i, -1, -i (dört pusula noktası).
N = 8 için dört pusula noktasını artı dört diyagonalı elde edersiniz.

Birlik kökleri Diskret Fourier Transform'un temelidir. DFT, bir sinyali bu N eşit alanlı frekanslarda bileşenlere parçalayır.

> 单位根是离散里叶变换的基础――DFT, sinyalleri bu N 个等间隔频率 bölümü olarak parçalacaktır―

> **【中文解读】**
> 单位根是N 个等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等等

### DFT'ye Bağlantı

Bir sinyalin x[0], x[1], ..., x[N-1] Diskret Fourier Transform'u:

> 信号 x[0], x[1], ..., x[N-1] 离散里叶变换为:

```
X[k] = sum_{n=0}^{N-1} x[n] * e^(-2*pi*i*k*n/N)
```

Her X[k] sinyalin birliğin k-inci kökü ile ne kadar ilişkili olduğunu ölçer. Bu karmaşık sinusoid bir frekans k. DFT bir sinyalü N dönümlü fazörlere ayırır ve her birinin amplitudu ve fazını söyler.

> Her X[k]  ölçüm sinyalinin k                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

### Neden ben hayali değilim?

"Fantastik" kelimesi tarihi bir tesadüf. Descartes onu reddeterek kullandı. Ama i negatif sayılar ilk defa reddedildiğinde olduğu kadar daha hayali değildir.

> "Yedi" ifadesi tarihsel tesadüflerdir. Descartes onu kullanırken aşağıda yer aldı. Ama ben olumsuz sayıdan daha fazla değilim.

Daha da kullanışlı: i 90 derecelik bir dönüm operatörüdür. Gerçek bir sayıyı bir kez i ile çarpırsak, hayalsel eksine 90 derece döndürürüz. tekrar i ile çarpırsak (i^2) bir başka 90 derece döndürürsünüz - şimdi negatif gerçek yönde işaret ediyorsunuz.

> Daha yararlı anlamak: i is a 90 ° rotation calculator。 real number multiplied i once, you rotate 90 ° to虚轴── re-fold i(i^2), re-rotate 90 ° now pointing towards negative real direction── işte bu yüzden i^2 = -1── bu gizemli değil── bu iki çeyrevinin dönüşü şeklinde dönüştürülmesinin yarısıdır──

Bu yüzden mühendislikte karmaşık sayılar her yerde var. Dönen her şey - elektromanyetik dalgalar, kuantum durumları, sinyal titreşimleri, konum kodlamaları - doğal olarak karmaşık sayılarla tanımlanır.

> Bu yüzden karmaşıklık, mühendislikte hiçbir yerde yoktur. Her türlü dönüşümlü bir şeyin  elektromanyetik dalga, kuantum hali, sinyal titreşim, konum kodlaması  hepsi doğal olarak karmaşıklık ile tanımlanır.

### Karmaşık eksponensaller vs. trigonometrik fonksiyonlar

Euler'in formülünden önce mühendisler sinyalleri A*cos(omega*t + phi) olarak yazdılar. - amplitud A, frekans omega, faz phi. Bu çalışır ama aritmetik ağrılı hale getirir.

> Bu işlemden önce mühendisler A*cos olarak sinyal yazacaklar.

Karmaşık eksponensallerle aynı sinyal A*e^(i*(omega*t + phi)). İki sinyal eklemek sadece iki karmaşık sayı eklemektir. Karşılaştırmak (modülasyon) sadece büyüklükleri çarpıtmak ve açı eklemektir. Faz değişikliği açı eklemelerine dönüşür. Frekans değişikliği fazörlerle çarpıtım olur.

> İki sinyal birleştirilmesi iki sayı birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirilmesi, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme, birleştirme

Tüm sinyal işleme alanı karmaşık eksponensel notasyona geçmiştir çünkü matematik daha temizdir. "gerçek sinyal" her zaman karmaşık temsilin gerçek bir parçasıdır. Hayali kısım da hesaplama olarak taşınır ve tüm cebir doğal olarak çalışır.

> Tüm sinyal işleme alanı, matematik daha basit olduğu için, "gerçek sinyal" genellikle sayısal ifadelerin gerçek bölümünü oluşturur.

> **【拓展：复数在量子计算中的角色】**
> 量子計算的基础态是复数向量──一个量子比特的状态是阿尔法                                                                                                                                                                                                                                                   

### Transformatörlere bağlama

**Sinusoidal positional encodings**(Orijinal Transformer kağıdı):

```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

Günah ve cos çiftleri, karmaşık eksponensallerin gerçek ve hayalsel parçalarıdır. Her frekans kodlama pozisyonu için farklı bir " çözünürlük " sağlar. Düşük frekanslar yavaşça (kaşlı pozisyon) değişir. Yüksek frekanslar hızlıca (sık pozisyon) değişir. Birlikte her pozisyonu benzersiz bir frekans parmak izi verirler.

> ve çünkü farklı frekanslı bir dizi indeksin gerçek ve gerçek bölümlerine karşıdır. Her frekanslı bir konum kodlaması farklı bir çözünürlük sağlar.

**RoPE (Rotary Position Embedding)**Bu, sorgu ve anahtar vektörlerini karmaşık döngü matrisleri ile açıkça çoğaltır. İki simge arasındaki göreceli konum bir döngü açısına dönüşür. Dikkat bu döngü vektörleri kullanarak hesaplanır.

> **RoPE（旋转位置编码）**Daha da ileri¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

> **【拓展：RoPE 在 LLaMA 和 GPT-NeoX 中的实现】**
> RoPE, bir sorgu ve anahtar yönlendirmeyi bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir diziye göre bir bir diziye göre bir bir bir diziye göre bir bir bir bir olarak bir bir bir bir bir olarak bir bir olarak bir bir olarak bir bir olarak bir olarak bir bir olarak bir olarak bir olarak bir bir olarak bir olarak bir olarak bir olarak bir bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak diğerine bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak bir olarak diğer olarak bir olarak bir olarak diğer olarak diğer olarak bir olarak bir olarak bir olarak diğer diğer olarak bir olarak diğer olarak bir olarak bir olarak bir olarak diğer diğer diğer olarak diğer olarak bir olarak diğer olarak diğer olarak bir olarak bir olarak bir olarak diğer olarak bir olarak bir olarak bir olarak bir olarak bir olarak diğer olarak diğer olarak diğer olarak diğer olarak bir olarak bir olarak diğer olarak diğer olarak bir olarak bir olarak diğer olarak diğer olarak bir olarak diğer olarak diğer olarak bir olarak diğer olarak diğer olarak diğer

| Operation | Algebraic Form | Geometric Meaning |
|-----------|---------------|-------------------|
| Addition | (a+c) + (b+d)i | Vector addition in the plane |
| Multiplication | (ac-bd) + (ad+bc)i | Rotate and scale |
| Conjugate | a - bi | Reflect over real axis |
| Magnitude | sqrt(a^2 + b^2) | Distance from origin |
| Phase | atan2(b, a) | Angle from positive real axis |
| Division | multiply by conjugate | Reverse rotation and rescale |
| Power | r^n * e^(i*n*theta) | Rotate n times, scale by r^n |

```mermaid
graph LR
    subgraph "Unit Circle"
        direction TB
        U1["e^(i*0) = 1"] -.-> U2["e^(i*pi/2) = i"]
        U2 -.-> U3["e^(i*pi) = -1"]
        U3 -.-> U4["e^(i*3pi/2) = -i"]
        U4 -.-> U1
    end
    subgraph "Applications"
        A1["Euler's formula:<br/>e^(i*theta) = cos + i*sin"]
        A2["DFT uses roots of unity:<br/>e^(2*pi*i*k/N)"]
        A3["RoPE uses rotation:<br/>q * e^(i*m*theta)"]
    end
    U1 --> A1
    U1 --> A2
    U1 --> A3
```

## Yapın.
```figure
roots-of-unity
```

## Yapın

### Adım 1: Karmaşık sınıf

Dörtgen ve kutup şekiller arasındaki aritmetik, büyüklük, faz ve dönüşümü destekleyen karmaşık bir sayı sınıfı oluşturun.

> 复数类 oluşturmak, 算术运算、模、相位 ve直角坐标 ve极坐标 arasındaki dönüşümü desteklemek

```python
import math

class Complex:
    def __init__(self, real, imag=0.0):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def __mul__(self, other):
        r = self.real * other.real - self.imag * other.imag  # 实部：(ac - bd)
        i = self.real * other.imag + self.imag * other.real  # 虚部：(ad + bc)
        return Complex(r, i)

    def __truediv__(self, other):
        denom = other.real ** 2 + other.imag ** 2            # 分母：c^2 + d^2
        r = (self.real * other.real + self.imag * other.imag) / denom  # 乘以共轭后的实部
        i = (self.imag * other.real - self.real * other.imag) / denom  # 乘以共轭后的虚部
        return Complex(r, i)

    def magnitude(self):
        return math.sqrt(self.real ** 2 + self.imag ** 2)

    def phase(self):
        return math.atan2(self.imag, self.real)

    def conjugate(self):
        return Complex(self.real, -self.imag)
```

### Adım 2: Kutup dönüşümü ve Euler formülü

```python
def to_polar(z):
    return z.magnitude(), z.phase()

def from_polar(r, theta):
    return Complex(r * math.cos(theta), r * math.sin(theta))

def euler(theta):
    return Complex(math.cos(theta), math.sin(theta))
```

Kontrol edin:`euler(theta).magnitude()`Her zaman 1.0 olmalı.`euler(0)`vermesi gerekir (1, 0). `euler(pi)`(-1, 0) vermeli.

> 验证:`euler(theta).magnitude()`应始终为 1.0──`euler(0)`应给出 (1, 0)`euler(pi)`应给出 (-1, 0)

### Adım 3: Dönüşüm

Bir noktayı (x, y) açı ile teta döndürmek bir karmaşık çarpma:

> 将点 (x, y) 旋转角度 theta 只有一次复数乘法:

```python
point = Complex(3, 4)
rotated = point * euler(math.pi / 4)
```

Büyüklük aynı kalır. Sadece açı değişir.

> 模保持不变──只有角度改变──

### Adım 4: Karmaşık aritmetikten DFT

```python
def dft(signal):
    N = len(signal)                               # 信号长度
    result = []
    for k in range(N):
        total = Complex(0, 0)
        for n in range(N):
            angle = -2 * math.pi * k * n / N      # 第 k 个单位根的角度
            total = total + Complex(signal[n], 0) * euler(angle)  # 累加：信号与旋转相量的相关
        result.append(total)
    return result
```

Bu O(N^2) DFT. Her çıkış X[k] sinyal örneklerinin toplamı birliğin kökleri ile çarpılmıştır.

> Bu O(N^2)'nin DFT¬idir. Her çıkış X[k] is sinyal örneği çarpı birim kökünü ve¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

### Adım 5: Ters DFT

Ters DFT, orijinal sinyali spektrumundan yeniden oluşturur. Ön DFT'den gelen tek değişiklikler: işaretini katılamada çevir ve N ile bölün.

> 逆 DFT 频谱重建原始信号──与正向 DFT 的唯一区别:翻转指数符号并除以 N──

```python
def idft(spectrum):
    N = len(spectrum)
    result = []
    for n in range(N):
        total = Complex(0, 0)
        for k in range(N):
            angle = 2 * math.pi * k * n / N
            total = total + spectrum[k] * euler(angle)
        result.append(Complex(total.real / N, total.imag / N))
    return result
```

Bu size mükemmel bir yeniden yapılandırma sağlar. DFT uygulayın, sonra IDFT, ve orijinal sinyal makine hassaslığına geri gelir. Hiçbir bilgi kaybolmaz.

> Bu size mükemmel bir şekilde yeniden inşa eder. DFT uygulamak, IDFT uygulamak, makine hassasiyetle orijinal sinyalleri geri kazanmak.

### 6 . Adım: Birliğin Temelleri

```python
def roots_of_unity(N):
    return [euler(2 * math.pi * k / N) for k in range(N)]
```

İki özellik doğrulanıyor:
- Her kökenin büyüklüğü tam olarak 1'dir.
  Her kökün tam olarak bir tane olması lazım.
- Tüm N köklerinin toplamı sıfırdır (simetri ile iptal edilirler).
  Ürünler ve kökler,

Bu özellikler DFT'yi dönüştürülebilir yapanlardır. Birlik kökleri frekans alanı için ortogonal bir temel oluşturur.

> Bu özellikler DFT'yi tersine yapar.

## Çerçeveyi kullanın.

Python'da karmaşık sayı desteği yer alıyor.`j`Hayal birimi temsil eder.

> Python 内置复数支持──字面量 `j`Göstermek için birim.

```python
z = 3 + 2j
w = 1 + 4j

print(z + w)
print(z * w)
print(abs(z))

import cmath
print(cmath.phase(z))
print(cmath.exp(1j * cmath.pi))
```

Arraylar için, numpy karmaşık sayıları doğuştan ele alır:

> 对于数组,numpy 原生处理复数:

```python
import numpy as np

z = np.array([1+2j, 3+4j, 5+6j])
print(np.abs(z))
print(np.angle(z))
print(np.conj(z))
print(np.real(z))
print(np.imag(z))

signal = np.sin(2 * np.pi * 5 * np.linspace(0, 1, 128))
spectrum = np.fft.fft(signal)
freqs = np.fft.fftfreq(128, d=1/128)
```

## İndirin . Ürünler .

Çık .`code/complex_numbers.py`üretmek için`outputs/skill-complex-arithmetic.md`- Evet .

> 运行  İşlem`code/complex_numbers.py`Ürün`outputs/skill-complex-arithmetic.md`(复数运算技能文档)

## Egzersizler.

1. **Complex arithmetic by hand.**Hesaplayın (2 + 3i) * (4 - i) ve kod ile doğrulayın. Sonra hesaplayın (5 + 2i) / (1 - 3i). Her iki sonucu da karmaşık düzlemde çizin ve çarpımın ilk sayıyı döndüğünü ve ölçeklediğini kontrol edin.

2. **Rotation sequence.**Bu sayede, e^(i*pi/6) ile on iki kez çarpın. 12 çarpımdan sonra (1, 0) 'ye döndüğünüzü kontrol edin.

3. **DFT of a known signal.**32 noktada örneklenen sin ((2*pi*3*t) ve 0.5*sin ((2*pi*7*t) toplamı olan bir sinyal oluşturun. DFT'ni çalıştırın. Büyüklük spektrumun 3 ve 7 frekanslarında zirvelerinin olup olmadığını kontrol edin.

4. **Roots of unity visualization.**Birliğin 8. kökü hesaplayın. Onların sıfıra kadar toplamını kontrol edin. Bir kökü ilk kökü e^(2*pi*i/8) ile çarpmanın bir sonraki kökü verdiğini kontrol edin.

5. **Rotation matrix equivalence.**10 rastgele açı ve 10 rastgele nokta için, karmaşık çarpımın 2x2 döngü matrisinde matris-vektor çarpımı ile aynı sonucu verdiğini kontrol edin.

## Anahtar Şartlar .

| Term | What it means |
|------|---------------|
| Complex number | A number a + bi where a is the real part, b is the imaginary part, and i^2 = -1 |
| Imaginary unit | The number i, defined by i^2 = -1. Not imaginary in the philosophical sense -- it is a rotation operator |
| Complex plane | The 2D plane where the x-axis is real and the y-axis is imaginary. Also called the Argand plane |
| Magnitude (modulus) | The distance from the origin: sqrt(a^2 + b^2). Written as \|z\| |
| Phase (argument) | The angle from the positive real axis: atan2(b, a). Written as arg(z) |
| Conjugate | The mirror image across the real axis: conjugate of a + bi is a - bi |
| Polar form | Expressing z as r * e^(i*theta) instead of a + bi. Makes multiplication easy |
| Euler's formula | e^(i*theta) = cos(theta) + i*sin(theta). Connects exponentials to trigonometry |
| Phasor | A rotating complex number e^(i*omega*t) representing a sinusoidal signal |
| Roots of unity | The N complex numbers e^(2*pi*i*k/N) for k = 0 to N-1. N equally spaced points on the unit circle |
| DFT | Discrete Fourier Transform. Decomposes a signal into complex sinusoidal components using roots of unity |
| RoPE | Rotary Position Embedding. Uses complex multiplication to encode relative position in transformer attention |

> 术语速查:Sıcak sayı(复数 a+bi)、Tüze birim(虚数单位 i,旋算子)、Sıcak düzlem(复平面)、Büyüklük/modül(模 √(a2+b2))、Fase/argument(相位 atan2(b,a))、Konküge(共 a-bi)、Polar biçim(极坐标 r·e^(iθ、Euler formülü欧拉公式 e^(iθ)=θ+i·sinθ)、Phasor(旋相量)、Birlik biriminin kökleri ((N 个均分单位圆点)、DFT散离里叶变换)、Rocosmode转转位置编码,L(Laosmode 等使用)

## Daha fazla okumak

- [Visual Introduction to Euler's Formula](https://betterexplained.com/articles/intuitive-understanding-of-eulers-formula/)- ağır notasyon olmadan geometrik algı oluşturur
- [Su et al.: RoFormer (2021)](https://arxiv.org/abs/2104.09864)- karmaşık dönümleri kullanarak Rotary Position Embedding'i tanıtan kağıt
- [Vaswani et al.: Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762)- Sinusoidal pozisyon kodlamaları olan orijinal Transformer kağıdı
- [3Blue1Brown: Euler's formula with introductory group theory](https://www.youtube.com/watch?v=mvmuCPvRoWQ)- e^(i*pi) = -1 nedeninin görsel açıklaması
- [Needham: Visual Complex Analysis](https://global.oup.com/academic/product/visual-complex-analysis-9780198534464)- karmaşık sayılar için en iyi görsel tedavi, geometrik anlayışla dolu
- [Strang: Introduction to Linear Algebra, Ch. 10](https://math.mit.edu/~gs/linearalgebra/)- Düzsel cebir ve öz değerler bağlamında karmaşık sayılar
