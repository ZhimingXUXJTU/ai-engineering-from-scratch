# Sayısal Kararlılık .

> Dalga geçiş noktası, sızdırıcı bir soyutlama.
> 浮点数 su dökülmesinin bir özelliğidir. Eğitim sırasında seni ısırır, ama sen görmezsin.

**Type:** Build | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~120 minutes | **时间:** ~120 分钟

## Öğrenme hedefleri

- Maksimum çıkarma hilesini kullanarak sayısal olarak stabil softmax ve log-sum-exp uygulamak
  En büyük değerleri azaltma tekniklerini kullanarak sayı değerini sabitleştirmek için softmax ve log-sum-exp
- Akış, akış ve felaket iptalinin yüzen nokta hesaplamalarında belirlenmesi
  识别浮点计算中的溢溢、下溢和灾难性抵消
- Merkezli sınırlı farkları kullanarak analitik gradientleri sayısal gradientlere karşı doğrula
  Uzcenter sınırlı farkı test çözünürlüğü
- Bfloat16'ın eğitim için float16'a neden tercih edildiğini ve kayıp ölçeklemesinin gradient akışının aşağı akışını nasıl engellediğini açıklayın.
  Neden float16 daha iyi uygulanabilir eğitim ve nasıl düşük dereceli bir kayıp önleyeceğini açıklayın.

> **【中文解读】**
> 浮点数是漏水的抽象──训练 3 小时后损失 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 NaN 变 N 变 N 变 N 变 N 变 N 变 N 变 N 变 N 变 N 变 N 变 N 变 N 变 N 变 N 变 N 变 N 变 N  变 N                                                                                                                                                                                                                                                                                                                        

## Sorunlar. Sorunlar.

> **【中文解读】**Üç tipik sayısal sabitlik felaketleri: 1) 3 saat sonra kaybı 变化 NaN某步计算溢出了; 2) 精度比论文差 2% float16 累积舍入差食掉准确率; 3) 自己写交叉 大逻辑时返回 infsoftmax 溢出── bunlar sayısal "漏水抽象", her türde standart bir düzeltme tekniği vardır──

Bir baskı açıklaması eklersin. 9.000'de kayıtlar iyi. 9.001'de ise.`inf`9.002 adımla her bir eğilimi `nan`Eğitim bitti.
> Bir yazı ekledin. 9.000 adımda kayıtlar normalleşti. 9.001 adım da normalleşti.`inf`9.002'ye kadar tüm seviyeler...`nan`Eğitim öldü.

Ya da: modeliniz tamamlanmaya hazır ama doğruluk kağıt iddialarından% 2 daha kötü. Her şeyi kontrol ediyorsunuz. Mimarlık eşleşir. Hiperparametre eşleşir. Veriler eşleşir. Sorun şu ki kağıt float32 kullanmış ve siz de doğru ölçeklendirme yapmadan float16 kullanmışsınız.
> Ya da: Model eğitim tamamlandı ama doğruluk teorinin oranı %2'dir. Her şeyi kontrol ettiniz. Yapılandırma uyumluluğu, süper parametre uyumluluğu, veri uyumluluğu.

Ya da: sıfırdan çapraz entropi kaybı uyguluyorsunuz. Küçük logitlerde çalışır.`inf`- Yumuşaklık aşırı aktı çünkü`exp(100)`Bu, bir iki satırlık numara ile işlenir.
> Ya da:You from head to implement交叉损失──小登录时正常──当登录时100 时返回 `inf`✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿`exp(100)`float32'nin gösterim alanını aşmıştır.

Sayısal istikrar teorik bir sorun değil. Başarılı bir eğitim koşusu ile sessiz bir şekilde başarısız olan bir eğitim koşusu arasındaki fark.
> Bilgi sabitliği teorik bir sorun değil. Bu, eğitim başarısı ile sessiz başarısızlık arasındaki farkı.

## Konsepten bir şey.

> **【拓展：Softmax 的数值稳定技巧是面试必考题】**原始 Softmax:`softmax(x) = exp(x) / sum(exp(x))`, x arasında büyük değer olduğunda 溢出――解法: eksik en büyük değer `softmax(x) = exp(x - max(x)) / sum(exp(x - max(x)))`Matematik sonuç değişmez ama sayısal değer sabit.`F.cross_entropy`İçeride log-softmax kullanmak ve ayrı hesaplama yapmamak, işte bu yüzden.

### IEEE 754: Bilgisayarlar Gerçek Sayıları Nasıl Saklar?

Bilgisayarlar IEEE 754 standardına göre gerçek sayıları yüzen nokta değerleri olarak kaydetir.
> 计算机根据IEEE 754 标准将实数存储为浮点值──浮点数有三部分:符号位、指数和尾数──

```
Float32 layout (32 bits total):
[1 sign] [8 exponent] [23 mantissa]

Value = (-1)^sign * 2^(exponent - 127) * 1.mantissa
```

Mantissa, hassasiyet (ne kadar önemli rakam) belirler. Eksponent aralığı (bir sayı ne kadar büyük veya küçük olabileceğini) belirler.
> 尾数决定精度 (nüfusu belirleyici sayı)

```
Format     Bits   Exponent  Mantissa  Decimal digits  Range (approx)
float64    64     11        52        ~15-16          +/- 1.8e308
float32    32     8         23        ~7-8            +/- 3.4e38
float16    16     5         10        ~3-4            +/- 65,504
bfloat16   16     8         7         ~2-3            +/- 3.4e38
```

float32 size yaklaşık 7 onluk rakamlı kesinlik verir. float16 size yaklaşık 3 rakamlı kesinlik verir. bfloat16 Google'ın float16'ın aralığı sorusuna verdiği cevap. float32 ile aynı 8 bitli bir gösterge, ancak sadece 7 mantissa bit.
> float32  give you about 7 位十进制精度──float16 约 3 位──bfloat16 Google'ın float16                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

### Neden 0.1 + 0.2 != 0.3 .

0.1 sayı tam olarak ikili yüzen noktada temsil edilemez. 2. tabanda tekrarlayan bir kırıklık. Float32 bunu 23 bit mantissa'ya kısaltır.
> 0.1 2. döngüsel bir hareket noktasında belirlenemez.

```
In Python:
>>> 0.1 + 0.2
0.30000000000000004

>>> 0.1 + 0.2 == 0.3
False
```

ML için önemli olan bu durumdur: (1) Kayıp karşılaştırmaları gibi `if loss < threshold`2. çok küçük değerlerin toplanması gerçek toplamdan uzaklaşır. 3. Eğer akışları `==`- Düzene: asla yüzenleri karşılaştırma`==`Kullan .`abs(a - b) < epsilon`veya `math.isclose()`- Evet .
> Bu ML için çok önemlidir: 1) 损失比较可能出错──(2) 累积许多小值会偏离真相和──(3) 用`==`Bu yüzden, bu konuda bir şey yapmamalıyız.`==`-Büyük sayı ile karşılaştırıldığında.

### Katastrofal İptal.

İki neredeyse eşit yüzen nokta sayısını çıkarırsanız, önemli rakamlar iptal edilir ve yuvarlak gürültü ileri rakamlara yükseltilmiş kalır.
> Eğer iki yakın nokta sayısını azaltırsanız, geçerli sayı boşar, sesin ön yönlü sayı olarak yükseltilmesi gerekir.

```
a = 1.0000001    (stored as 1.00000011920929 in float32)
b = 1.0000000    (stored as 1.00000000000000 in float32)

True difference:  0.0000001
Computed:         0.00000011920929

Relative error: 19.2%
```

Düzeltme: büyük, neredeyse eşit sayıları çıkarmaktan kaçınmak için formülleri yeniden düzenleyin.
> 修复: Büyük yakınlıkların sayısını azaltmak için yeniden düzenleme formülü. Welford algoritması veya önceden merkezileştirilmiş veriler kullanılarak hesaplama.

### Aşırı akış ve aşım.

Bir sonuç temsil etmek için çok büyük olduğunda aşırı akış oluşur.
> Sonuç çok büyük, sonuç çok küçük.

```
Float32 boundaries:
  Maximum:  3.4028235e+38
  Overflow:  anything > 3.4e38 becomes inf
  Underflow: anything < 1.4e-45 becomes 0.0

exp(88.7)  = 3.40e+38   (barely fits in float32)
exp(89.0)  = inf         (overflow)
```

ML'de, `exp()`softmax, sigmoid ve olasılık hesaplamalarında ortaya çıkar. `log()`Çelişkili entropi, log-eğilimler ve KL farklılıklarında ortaya çıkar.
> ML'de,`exp()`Şimdi yumuşaklık maksim,sigmoid ve olasılık hesaplamaları arasında.`log()`Şimdi ise, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu arada, bu da, bu arada, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da, bu da,

### Log-Sum-Exp Trick  Teknik

Bilgisayar `log(sum(exp(x_i)))`Bu numaralar, sayıca tehlikelidir.
> Doğrudan hesaplama`log(sum(exp(x_i)))`sayı değer tehlikeli: teknik: indeksleme öncesi en büyük değerini düşürmek

```
log(sum(exp(x_i))) = max(x) + log(sum(exp(x_i - max(x))))
```

Neden bu işe yarıyor: çıkarmadan sonra `max(x)`, en büyük gösterge `exp(0) = 1`. Üstü akış mümkün değildir. toplamda en az bir terim 1'dir, bu yüzden toplam en az 1'dir ve `log(1) = 0`- Akış yok .`-inf`- Bu mümkün.
> Neden geçerli: Kısaltma`max(x)`后,最大指数是 `exp(0) = 1`△ mümkün değil. △ en az 1'dir.`log(1) = 0`- Hayır, hayır.`-inf`- Evet.

Bu numara ML'de her yerde ortaya çıkar: softmax normallaşması, çapraz entropi kaybı, log- olasılık toplamı, Gaussians karışımı, varyasyon sonucu.
> Bu teknik ML'de mevcuttur:softmax 归化、交叉损失、对数概率求和、高斯混合、变分推断──

### Neden Softmax Max-Kürtme Trick'e ihtiyaç duyuyor ? Neden Softmax maksimum değer azaltma tekniklerine ihtiyaç duyuyor ?

Bu numarayı kullanmak için, [100, 101, 102] logitleri aşırı akışa neden olur.
> 没有技巧时,logits [100, 101, 102] 导致溢出──有技巧时,减去最大(x) = 102:

```
exp(100 - 102) = exp(-2) = 0.135
exp(101 - 102) = exp(-1) = 0.368
exp(102 - 102) = exp(0)  = 1.000
sum = 1.503

softmax = [0.090, 0.245, 0.665]
```

Muhtemelen aynıdır. Hesaplama güvenli. Bu bir optimizasyon değil. Doğru bir şart.
> 概率 tamamen aynıdır.

### NaN ve Inf: tespit ve önleme

`nan`ve `inf`Birinci, bilgisayar yoluyla virüs yoluyla yayılır.`nan`Bir gradient güncelleme ağırlığı yapar `nan`, bu da sonraki tüm çıkışları yapar .`nan`Eğitim bir adımdan sonra biter.
> `nan`和 `inf`通过计算病毒式传播――梯度更新中的一个 `nan`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `nan`,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `nan`❖ Trein Step'in ölmüş olması

Nasıl ?`nan`Görüntü: `0.0 / 0.0`- Evet .`inf - inf`- Evet .`inf * 0`- Evet .`sqrt()`negatif, `log()`Önleme: Klamp girişleri`exp()`, isimlendiriciye epsilon ekle, sabit uygulamalar kullan, gradient kesim.
> `nan`Nasıl ortaya çıkıyor:`0.0/0.0`- Evet.`inf-inf`- Evet.`inf*0`、负数 `sqrt()`、负数 `log()` Önleme: sınırlama`exp()`输入、给分母加 epsilon、使用稳定实现、梯度剪──

### Sayısal Değer Aralık Kontrolü

Analizsel gradientler (geri yayılma) hatalara sahip olabilir. Sayısal gradient kontrolü onları sınırlı farklılıklara sahip gradientleri hesaplayarak doğruluyor.
> 解析梯度 (Bug) olabilir. 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析梯度 (Bug) 解析) 解析梯度 (Bug) 验证 (Bug) 验证) 验证 (Bug) 验证) 解析 (Bug) 解析) 解析梯度 (Bug) 解析) 解析 (Bug) 解析) 解析 (Bug) 解析 (Bug) 解析) 解析 (Bug) 解析)

```
df/dx ~= (f(x + h) - f(x - h)) / (2h)
```

Baskır kuralları: relative_error < 1e-7: perfect; < 1e-5: acceptable; > 1e-3: bir şey yanlış; > 1: tamamen yanlış.
> 经验法则:相对误差 < 1e-7:完美; < 1e-5:可接受;> 1e-3:有问题;> 1:完全错误──

### Karışık Precision Eğitimleri Karışık Precision Eğitimleri

Modern GPU'lar float16 matris çarpımlarını float32'den 2-8 kat daha hızlı hesaplayan Tensor Cores'e sahiptir.
> 现代 GPU has Tensor Core,float16 矩阵乘法比float32 快 2-8 倍──混合精度训练利用这一点──

```
1. Maintain float32 master copy of weights
2. Forward pass in float16 (fast)
3. Compute loss in float32 (prevents overflow)
4. Backward pass in float16 (fast)
5. Scale gradients to float32
6. Update float32 master weights
```

Float16 aşağı akışının düzeni kayıp ölçeklemesidir: kayıpı büyük ölçek faktörü ile çarpın, geriye geçiş daha büyük eğrilikleri hesaplar, ağırlıkları güncelleştirmeden önce ölçekle bölün.
> float16 下溢 の修复は損失縮小: kaybı büyük縮小因子, 逆向传播計算のより大きな梯度,更新权重前除以縮小因子にします.

### Bfloat16 vs. Float16: Neden Bfloat16 Eğitim için Kazanıyor

float16 daha fazla hassaslık (10 mantissa bit) ama sınırlı aralığı (maksimum 65,504). bfloat16 daha az hassaslık ama float32 ile aynı aralığı (maksimum 3,4e38).
> float16 精度更高(10 位尾数) 但范围有限(最大 ~65,504) ・bfloat16 精度较低但范围与 float32 相同(最大 ~3.4e38) ・训练时范围更重要──

### - Gradyent Kısaltma.

Patlama gradientleri gradientlerin eksponansal olarak büyüdüğünde meydana gelir. İki tür kesim: değerle klip (her elementle sıkıştır) ve normla klip (bütün vektörün bir eşiğiyle ölçülmesi için norm bir eşiği aşmaz).`torch.nn.utils.clip_grad_norm_()`- Evet.
> 梯度爆发生在梯度指数增长时――两种剪裁:按值剪裁 限制每个元素) 和按范数剪裁 缩放整个向量使范数不超过值)──按范数剪裁保留梯度方向──

Tipik değerler: `max_norm=1.0`transformatörler için, `max_norm=0.5`RL için, `max_norm=5.0`Daha basit ağlar için.
> 典型值:Transformer 用 `max_norm=1.0`- Ne?`max_norm=0.5`, basit ağ kullanımı `max_norm=5.0`- Evet.

### Genel ML Sayı Hataları  Genel ML Sayı Hataları

**Bug: Loss is NaN after a few epochs.**Sebep: çok büyük logitler, softmax aşırı akıyor.
> **Bug: 几个 epoch 后 loss 变 NaN。**原因:logits 太大,softmax 溢出──修复:使用稳定softmax,降低学习率,添加梯度剪──

**Bug: Validation accuracy is lower by 1-3%.**Sebep: uygun bir kayıp ölçeklemesi olmadan karışık hassasiyet. Düzelt: dinamik kayıp ölçeklemesini etkinleştirin veya bfloat16'a geçin.
> **Bug: 验证精度低 1-3%。**原因:混合精度没有正确的损失缩放──修复:启动动态损失缩放,或切换到 bfloat16──

**Bug: `exp()` returns `inf` in loss computation.**Düzeltme: kullan `torch.nn.functional.log_softmax()`Bu da log-sum-exp'i içtenlikle uyguluyor.
> **Bug: 损失计算中 `exp()` 返回 `inf`。**修复: kullan `torch.nn.functional.log_softmax()`- Evet.

## Yapın.

### Adım 1: Sürükleyici nokta kesinliği sınırlarını gösterin.
**Bug: Validation accuracy is lower than expected by 1-3%.**
Sebep: uygun bir kayıp ölçeklemesi olmadan karışık hassasiyet.
Düzeltme: dinamik kayıp ölçeklemesini etkinleştir veya bfloat16'a geçin.

**Bug: Gradient norms are 0.0 for some layers.**
Sebep: ölü ReLU nöronları (tüm girişler negatif) veya float16 akış altındaki akış.
Düzeltme: LeakyReLU veya GELU kullanın, gradient ölçeklemesini kullanın, ağırlık başlangıçını kontrol edin.

**Bug: Model works on one GPU but gives different results on another.**
Sebep: belirlenmez yüzen nokta birikimi sırası. GPU paralel azaltmaları farklı donanımlarda farklı sırada toplamlanır ve yüzen nokta eklenmesi ilişkili değildir.
Düzeltme: küçük farkları kabul edin (1e-6), veya ayarlayın `torch.use_deterministic_algorithms(True)`Ve hız cezasını kabul et.

**Bug: `exp()` returns `inf` in loss computation.**
Sebep: Hızlı malzeme `exp()`Maksimum çıkarma hilesi olmadan.
Düzeltme: kullan `torch.nn.functional.log_softmax()`Bu da log-sum-exp'i içtenlikle uyguluyor.

**Bug: Training diverges after switching from float32 to float16.**
Sebep: float16 6e-8'den aşağıdaki gradient büyüklüklerini veya 65,504'ten yüksek aktivasyonları temsil edemez.
Düzeltme: Kayıp ölçeklemesi (AMP) ile karışık hassaslık kullanın veya bunun yerine bfloat16 kullanın.

```figure
logsumexp-stability
```

## Yapın

### Adım 1: Sürükleyici noktaların doğruluk sınırlarını göster

```python
print("=== Floating Point Precision ===")
print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}")
print(f"Difference: {(0.1 + 0.2) - 0.3:.2e}")
```

### Adım 2: Naif vs. Stabil Softmax uygulamak.

```python
import math

def softmax_naive(logits):
    exps = [math.exp(z) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def softmax_stable(logits):
    max_logit = max(logits)
    exps = [math.exp(z - max_logit) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

safe_logits = [2.0, 1.0, 0.1]
print(f"Naive:  {softmax_naive(safe_logits)}")
print(f"Stable: {softmax_stable(safe_logits)}")

dangerous_logits = [100.0, 101.0, 102.0]
print(f"Stable: {softmax_stable(dangerous_logits)}")
# softmax_naive(dangerous_logits) would return [nan, nan, nan]
```

### Adım 3: Durgan log-sum-exp uygulamak.

```python
def logsumexp_stable(values):
    c = max(values)
    return c + math.log(sum(math.exp(v - c) for v in values))
```

### Dördüncü adım: Dönüştürücü bir bağlantı gerçekleştirmek.

```python
def cross_entropy_stable(true_class, logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = math.log(sum(math.exp(s) for s in shifted))
    log_prob = shifted[true_class] - log_sum_exp
    return -log_prob
```

### Adım 5: Devamlı kontrol.

```python
def numerical_gradient(f, x, h=1e-5):
    grad = []
    for i in range(len(x)):
        x_plus = x[:]
        x_minus = x[:]
        x_plus[i] += h
        x_minus[i] -= h
        grad.append((f(x_plus) - f(x_minus)) / (2 * h))
    return grad

def check_gradient(analytical, numerical, tolerance=1e-5):
    for i, (a, n) in enumerate(zip(analytical, numerical)):
        denom = max(abs(a), abs(n), 1e-8)
        rel_error = abs(a - n) / denom
        status = "OK" if rel_error < tolerance else "FAIL"
        print(f"  param {i}: analytical={a:.8f} numerical={n:.8f} "
              f"rel_error={rel_error:.2e} [{status}]")
```

## Çerçeveyi kullanın.

Bakın .`code/numerical.py`Tüm kenar durumları gösterilen tam uygulamalar için.
> 完整实现见 `code/numerical.py`- Evet.

```python
# 梯度裁剪
def clip_by_norm(gradients, max_norm):
    total_norm = math.sqrt(sum(g**2 for g in gradients))
    if total_norm > max_norm:
        scale = max_norm / total_norm
        return [g * scale for g in gradients]
    return gradients

# NaN/Inf 检测
def check_tensor(name, values):
    has_nan = any(math.isnan(v) for v in values)
    has_inf = any(math.isinf(v) for v in values)
    if has_nan or has_inf:
        print(f"WARNING {name}: nan={has_nan} inf={has_inf}")
        return False
    return True
```

## İndirin . Ürünler .

Bu ders şunları ortaya çıkarır:
> 本课程产出:

- `code/numerical.py`Kalıcı softmax, log-sum-exp, çapraz entropi, gradient kontrolü ve karışık hassaslık simülasyonu ile
  包含稳定软max、log-sum-exp、交叉、梯度检查和混合精度模拟
- `outputs/prompt-numerical-debugger.md`eğitimde NaN/Inf ve sayısal sorunların teşhis edilmesi için
  Diagnostik eğitimde NaN/Inf ve sayısal değer sorunu kullanılır

## Egzersizler.

1. **Catastrophic cancellation.**Naif formülü kullanarak [1000000.0, 1000001.0, 1000002.0] değişikliğini hesaplayın `E[x^2] - E[x]^2`Sonra Welford'un çevrimiçi algoritmasını kullanarak hesaplayın.
   **灾难性抵消。**Uzdön basit formül ve Welford 算法 hesaplama [1000000.0, 1000001.0, 1000002.0] ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′s ′ ′s ′s ′s ′s ′s ′ ′s ′ ′ ′s ′s ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′   ′ ′     ′       ′                                                                                                              

2. **Precision hunt.**En küçük pozitif float32 değerini bul `x`Bu kadar .`1.0 + x == 1.0`- Düzleşmesini kontrol et .`numpy.finfo(numpy.float32).eps`- Evet .
   **精度搜索。**找到使 `1.0 + x == 1.0`En az normal float32 değerı

3. **Log-sum-exp edge cases.**Testini yap .`logsumexp_stable`Bu fonksiyon: (a) tüm değerler eşit, (b) bir değer diğerlerinden çok daha büyük, (c) tüm değerler çok negatif (-1000).
   **Log-sum-exp 边界情况。**测试稳定 log-sum-exp 在极端输入下表现──

4. **Gradient checking a neural network layer.**Tek bir çizgi katmanı uygula `y = Wx + b`ve 3x2 ağırlık matrisinin doğruluğunu kontrol et.
   **梯度检查神经网络层。**实现单层线性层并验证正确性──

5. **Loss scaling experiment.**Float16 ile eğitim simülasyonu: gradientlerin hangi bölümü sıfır haline geldiğini ölç.
   **损失缩放实验。**模拟 float16 训练,测量梯度变为零的比例, sonra kaybı küçültmek için yeniden ölçmek için uygulayın

## Anahtar Şartlar .

| Term / 术语 | What people say | What it actually means / 实际含义 |
|------|----------------|----------------------|
| IEEE 754 | "The float standard" | International standard defining binary floating point formats. / 定义二进制浮点格式的国际标准。 |
| Machine epsilon / 机器精度 | "The precision limit" | The smallest value e such that 1.0 + e != 1.0. For float32, ~1.19e-7. / 使 1.0 + e != 1.0 的最小值。float32 约 1.19e-7。 |
| Catastrophic cancellation / 灾难性抵消 | "Precision loss from subtraction" | Significant digits cancel when subtracting nearly equal numbers. / 相减近似相等数时有效数字抵消。 |
| Overflow / 溢出 | "Number too big" | A result exceeds the maximum representable value and becomes inf. / 结果超过最大可表示值变为 inf。 |
| Underflow / 下溢 | "Number too small" | A result is closer to zero than the smallest representable positive number. / 结果比最小可表示正数更接近零。 |
| Log-sum-exp trick / Log-sum-exp 技巧 | "Subtract the max first" | Computing log(sum(exp(x))) by factoring out exp(max(x)). / 通过提取 exp(max(x)) 计算 log(sum(exp(x)))。 |
| Stable softmax / 稳定 softmax | "Softmax that does not explode" | Subtracting max(logits) before exponentiating. / 指数化前减去最大 logit。 |
| Gradient checking / 梯度检查 | "Verify your backprop" | Comparing analytical vs numerical gradients to catch bugs. / 比较解析和数值梯度以捕获 bug。 |
| Mixed precision / 混合精度 | "Float16 forward, float32 backward" | Using lower-precision for speed, higher-precision for accuracy. / 低精度加速，高精度保准确。 |
| Loss scaling / 损失缩放 | "Prevent gradient underflow" | Multiplying loss by a large constant to keep gradients in float16 range. / 将损失乘以大常数使梯度保持在 float16 范围内。 |
| bfloat16 | "Brain floating point" | Google's 16-bit format with 8 exponent bits. Preferred for training. / Google 的 16 位格式，8 位指数。训练首选。 |
| Gradient clipping / 梯度裁剪 | "Cap the gradient norm" | Scaling the gradient vector so its norm does not exceed a threshold. / 缩放梯度向量使范数不超过阈值。 |
| NaN | "Not a Number" | Special float value from undefined operations. Propagates through all arithmetic. / 未定义操作的特殊浮点值。通过所有算术传播。 |
| Inf | "Infinity" | Special float value from overflow or division by zero. / 溢出或除零产生的特殊浮点值。 |
| Numerical gradient / 数值梯度 | "Brute force derivative" | Approximating a derivative by evaluating f(x+h) and f(x-h). / 通过求 f(x+h) 和 f(x-h) 近似导数。 |

## Daha fazla okumak

- [What Every Computer Scientist Should Know About Floating-Point Arithmetic (Goldberg 1991)](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)-- Son referans
  浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算术 浮点算算
- [Mixed Precision Training (Micikevicius et al., 2018)](https://arxiv.org/abs/1710.03740)- NVIDIA'nın kayıp ölçeklemesi makalesinde
  NVIDIA 损失缩放论文
- [AMP: Automatic Mixed Precision (PyTorch docs)](https://pytorch.org/docs/stable/amp.html)-- pratik rehber
  PyTorch 混合精度实践指南
- [bfloat16 format (Google Cloud TPU docs)](https://cloud.google.com/tpu/docs/bfloat16)-- Google neden bu biçimi seçti
  Google 选择 bfloat16 的原因
- [Kahan Summation (Wikipedia)](https://en.wikipedia.org/wiki/Kahan_summation_algorithm)-- yuvarlama hatasını azaltmak için algoritma
  減舍入差的 Kahan 求和算法
