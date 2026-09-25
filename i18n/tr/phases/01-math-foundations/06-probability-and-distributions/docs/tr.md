# Muhtemelenlik ve dağılım 概率 ve dağılım

> Muhtemelenlik, AI'nin belirsizlikleri ifade etmek için kullandığı dildir.
> 概率 is AI (İÇ) belirsiz bir dil ifade etmektedir.

**Type:** Learn | **类型:** 学习
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~75 minutes | **时间:** ~75 分钟

## Öğrenme hedefleri

- Bernoulli, kategorik, Poisson, üniform ve normal dağılımlar için PMF ve PDF'leri sıfırdan uygulayın
- Beklenen değeri, varyansi hesaplayın ve Gaussians'ın neden egemen olduğunu açıklamak için Merkez Sınır Teoremi kullanın
- Sayısal istikrar hilesini kullanarak softmax ve log-softmax fonksiyonlarını oluştur (maksimum logit çıkar)
- Logitlerden çapraz entropik kaybı hesaplayın ve onu negatif log olasılığı ile bağlayın

> **【中文解读】**
> 概率, 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概率 概

> **【拓展：概率在 AI 中的位置】**
> - **Softmax**: Tüm sınıflardaki modellerin son adımı olan sinir ağının çıkışını olasılık dağılımına dönüştürmek.
> - **交叉熵损失**: 分类任务的标准损失函数, 负对数似然的等等.
> - **高斯分布**: Çevre ve AI'de neden yüksek dağılımın bu kadar yaygın olduğunu anlamak için çok sınırlı bir anlayış vardır.

## Sorunlar. Sorunlar.

> **【中文解读】**Çıkış ve çıkış`[0.03, 0.91, 0.06]`%91, %91, %91, %91, %91, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93, %93,%93,%93,%93,%93,%93,%93,%93,%93,%93,%93,%93,%93,%93,%93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,9

## Konsepten bir şey.

> **【拓展：概率分布是 AI 生成模型的基础】**生成模型 (VAE、GAN、扩散模型) nın çekirdeği olasılık dağılımıdır: bir veri dağılımını öğrenmek p(x), sonra orta örnekten yeni veri üretmek.

Bir modelin yaptığı her tahmin bir olasılık dağılımıdır. Her kayıp işlevi tahmin edilen dağılımın gerçek olanlardan ne kadar uzak olduğunu ölçer. Her eğitim adımında bir dağılımın diğerine daha çok benzeyebilmesi için parametreler ayarlanır.

> Modellerin her tahmininin bir olasılık dağılımıdır. Her kayıp işlevi, tahmin dağılımının gerçek dağılım arasındaki farkı ölçer. Her adım, bir dağılımın diğerine daha yakın hale gelmesini sağlayan ayarlama parametrelerinde bulunur.

## Konsepten bir şey.

### Olaylar, Örnek Alanlar ve Muhtemelenlik

Örnek alanı S, tüm olası sonuçların toplamıdır. Bir olay örnek alanının bir alt kümesidir. Muhtemelenlik olayları 0 ile 1 arasındaki rakamlara haritasıyor.

> 样本空间 S, tüm olası sonuçların bir toplamıdır. 事件は样本空间の小集である. 概率将事件映射到0〜1 arasındaki sayılardır.

```
Coin flip:
  S = {H, T}
  P(H) = 0.5,  P(T) = 0.5

Single die roll:
  S = {1, 2, 3, 4, 5, 6}
  P(even) = P({2, 4, 6}) = 3/6 = 0.5
```

Üç aksiom tüm olasılıkları tanımlar:
1. P(A) >= 0 herhangi bir olay için A
2. P(S) = 1 (her zaman bir şeyler olur)
3. P(A veya B) = P(A) + P(B) A ve B'nin ikisi de gerçekleşemediği zaman

> 概率论由三条公理定义:
> 1. 对于任意事件 A,P(A) >= 0
> 2. P(S) = 1( mutlaka bir sonuç olacak)
> 3. Bu durumun gerçekleşmesi için, P(A veya B) = P(A) + P(B)

Diğer her şey (Bayes teoremi, beklentiler, dağılımlar) bu üç kuralı takip eder.

> 其他一切 (贝叶斯定理,期望,分布) bu üç kural tarafından yönlendirilir.

### Şartlı Muhtemelenlik ve Bağımsızlık

P ((A) B) A'nın B'nin gerçekleşmesi olasılığıdır.

> P (A) B) B ye ait koşullarda B ye ait olasılıktır.

```
P(A|B) = P(A and B) / P(B)

Example: deck of cards
  P(King | Face card) = P(King and Face card) / P(Face card)
                      = (4/52) / (12/52)
                      = 4/12 = 1/3
```

İki olay bağımsızdır. Birini bilmek diğerini anlatmaz.

> İki olayın bağımsızlığı, birinden diğerinden haber almadığını bilmek demektir.

```
Independent:   P(A|B) = P(A)
Equivalent to: P(A and B) = P(A) * P(B)
```

Para atmak bağımsızdır, değiştirilmeden çizmek de değil.

> Para bırakmak bağımsız değil.

### Muhtemelen Masa Fonksiyonları vs. Muhtemelen Sıklık Fonksiyonları

Diskret rastgele değişkenlerin olasılık kütle fonksiyonu (PMF) vardır. Her sonuç doğrudan okuyabileceğiniz belirli bir olasılığa sahiptir.

> 离散随机变量有概率质量函数 (PMF) ⋅ her sonuçta doğrudan okunur belirli bir olasılıkla sahiptir.

```
PMF: P(X = k)

Fair die:
  P(X = 1) = 1/6
  P(X = 2) = 1/6
  ...
  P(X = 6) = 1/6

  Sum of all probabilities = 1
```

Sürekli rastgele değişkenlerin olasılık yoğunluğu işlevi vardır. Tek bir noktada yoğunluk olasılık değildir.

> 连续随机变量有概率密度函数 (PDF) ⋅ tek bir noktadaki yoğunluk değeri olasılıkla değil, olasılıkla belirli bir bölgede yoğunluk işlevi karşısında bulunur.

```
PDF: f(x)

P(a <= X <= b) = integral of f(x) from a to b

f(x) can be greater than 1 (density, not probability)
integral from -inf to +inf of f(x) dx = 1
```

Bu ayrım ML'de önemlidir. Sınıflama çıkışları PMF'lerdir (diskret seçimler). VAE gizli alanları PDF'leri (daima) kullanır.

> Bu fark ML'de çok önemlidir.

### Genel dağıtımlar

**Bernoulli:**Bir deney, iki sonuç.

> **伯努利分布：**Bir deney, iki sonuç.

```
P(X = 1) = p
P(X = 0) = 1 - p
Mean = p,  Variance = p(1-p)
```

**Categorical:**Modeller çok sınıflı sınıflandırma (softmax çıkışı).

> **分类分布：**Bir deney, bir çeşit sonuç.

```
P(X = i) = p_i,  where sum of p_i = 1
Example: P(cat) = 0.7,  P(dog) = 0.2,  P(bird) = 0.1
```

**Uniform:**- Tüm sonuçlar eşit olasılıkla.

> **均匀分布：**Tüm sonuçlar ve olasılıklar ortaya çıkar.

```
Discrete: P(X = k) = 1/n for k in {1, ..., n}
Continuous: f(x) = 1/(b-a) for x in [a, b]
```

**Normal (Gaussian):**Çan eğri. ortalama (mu) ve varyansa (sigma^2) ile parametrelidir.

> **正态（高斯）分布：**钟形曲线──由均值 (mu) 和方差 (sigma^2) 参数化──

```
f(x) = (1 / sqrt(2*pi*sigma^2)) * exp(-(x - mu)^2 / (2*sigma^2))

Standard normal: mu = 0, sigma = 1
  68% of data within 1 sigma
  95% within 2 sigma
  99.7% within 3 sigma
```

**Poisson:**Sık rastlanan olayların belirli bir aralıkta sayılması.

> **泊松分布：**固定区内稀有事件の計り── inşaat için kullanılan olayların gerçekleşme oranı──

```
P(X = k) = (lambda^k * e^(-lambda)) / k!
Mean = lambda,  Variance = lambda
```

### Beklenen Değer ve Çeşitlilik

Beklenen değer, ağırlıklı ortalama sonuçtır.

> 期望值= 增权平均結果──

```
Discrete:   E[X] = sum of x_i * P(X = x_i)
Continuous: E[X] = integral of x * f(x) dx
```

Değişiklik ölçümleri ortalama etrafında yayılmış.

> 方差, ortalama değer etrafındaki dağılımın derecesini ölçer.

```
Var(X) = E[(X - E[X])^2] = E[X^2] - (E[X])^2
Standard deviation = sqrt(Var(X))
```

ML'de, beklenen değer kayıp işlevi (verilerin dağılımında ortalama kayıp) olarak görünür.

> ML'de, beklenmedik değerler kayıp işlevi olarak gösterilmektedir, bu da size model sabitliğini anlatır.

### Ortak ve Marjinal dağıtımlar

Bir ortak dağılım P ((X, Y) iki rastgele değişkenyi birlikte tanımlar.

> 联合分布 P(X, Y)  iki değişken değişkenin aynı anda meydana gelen durumları tanımlar.

Ortak PMF örneği (X = hava durumu, Y = şemsiye):
联合 PMF示例(X = 天气,Y = 是否带):

| | Y=0 (no umbrella / 不带伞) | Y=1 (umbrella / 带伞) | Marginal P(X) / 边缘 P(X) |
|---|---|---|---|
| X=0 (sun / 晴天) | 0.40 | 0.10 | P(X=0) = 0.50 |
| X=1 (rain / 下雨) | 0.05 | 0.45 | P(X=1) = 0.50 |
| **Marginal P(Y) / 边缘 P(Y)** | P(Y=0) = 0.45 | P(Y=1) = 0.55 | 1.00 |

Sınırsal dağılım diğer değişkenin toplamını içerir:

> 边缘分布通过对另一个变量求和得到:

```
P(X = x) = sum over all y of P(X = x, Y = y)
```

Yukarıdaki tabloda sırada ve sütunda toplamlar, kenarlıklardır.

> Yukarıdaki tabloda, sırayla dağılım ve sırayla dağılım vardır.

### Normal Değişiklik Neden Her Yerde Görülüyor?

Merkez Sınır Teoremi: birçok bağımsız rastgele değişkenin toplamı (veya ortalaması) orijinal dağılımdan bağımsız olarak normal bir dağılım için birleşti.

> Ortalama: birçok bağımsız değişken ve ortalama olarak normal dağılımlara ulaşır, ne olursa olsun orijinal dağılım neyi içerir.

```
Roll 1 die:  uniform distribution (flat)
Average of 2 dice:  triangular (peaked)
Average of 30 dice: nearly perfect bell curve

This works for ANY starting distribution.
```

İşte bu yüzden:
- Ölçüm hataları yaklaşık olarak normaldir (çok küçük bağımsız kaynaklar)
  Çinçe Çevirimi: ölçüm hataları yakın durumdur (由许多小的独立来源叠加)
- Nöral ağlarda ağırlık başlangıçları normal dağılımları kullanır
  Çinçe çevirisi: 神经网络的权重初始化正态分布使用
- SGD'deki gradient gürültüsü yaklaşık olarak normaldir (çok sayıda örnek gradientinin toplamı)
  Çinçe Çevirimi:SGD 中的梯度噪音近似正态(许多样本梯度的总和)
- Normal dağılım, verilen bir ortalama ve varyansa için en fazla entropi dağılımıdır.
  Çinçe çevirisi: Normal dağılım, belirli ortalama değer ve  en büyük dağılımdır.

### Kayıt olasılıkları

Çiğ olasılıklar sayısal sorunlara neden olur. Çok küçük olasılıkları bir araya getirmek hızla sıfıra düşer.

> İlk olasılık sayısal değer soruna yol açar.

```
P(sentence) = P(word1) * P(word2) * ... * P(word_n)
            = 0.01 * 0.003 * 0.02 * ...
            -> 0.0 (underflow after ~30 terms)
```

Log olasılıkları bunu düzeltir.

> Sayı olasılığı bu sorunu çözdü.

```
log P(sentence) = log P(word1) + log P(word2) + ... + log P(word_n)
                = -4.6 + -5.8 + -3.9 + ...
                -> finite number (no underflow)
```

Kurallar:
- log(a * b) = log(a) + log(b)
- log olasılığı her zaman <= 0'dur (Çünkü 0 < P <= 1)
- Daha negatif = daha az olası
- Çarpıcı entropik kaybı doğru sınıfın negatif log olasılığıdır

> 规则:
> - log(a * b) = log(a) + log(b)
> - Sayı olasılığı genellikle <= 0 ((Çünkü 0 < P <= 1)
> - 越负 = 越不可能
> - 交叉損失= doğru sınıfın negatif karşı sayı olasılığı

### Softmax, olasılık dağılımı olarak

Sinir ağları çiğ puanlar (logits) çıkarır. Softmax onları geçerli bir olasılık dağılımına dönüştürür.

> 神经网络输出原始分数(logits) ――Softmax onları geçerli olasılık dağılımına dönüştürecek──

```
softmax(z_i) = exp(z_i) / sum(exp(z_j) for all j)

Properties:
  - All outputs are in (0, 1)
  - All outputs sum to 1
  - Preserves relative ordering of inputs
  - exp() amplifies differences between logits
```

Softmax numarası: Aşırı akışın önlenmesi için, eksponansiyalandırmadan önce maksimum logit'i çıkarın.

> Softmax 技巧: 取指数'den önce maksimum logit'i azaltmak, aşırı çıkmayı önlemek

```
z = [100, 101, 102]
exp(102) = overflow

z_shifted = z - max(z) = [-2, -1, 0]
exp(0) = 1  (safe)

Same result, no overflow.
```

Log-softmax, sayısal istikrar için softmax ve log'u birleştirir. PyTorch bunu içsel olarak çapraz entropi kaybı için kullanır.

> Log-softmax, sayısal değer sabitliğini korumak için bir adım için softmax ve log 合并 eder.

### Örnekleme

Örnekleme, bir dağılımdan rastgele değerlerin çekilmesi anlamına gelir.
- Neuronu kimler sıfırlamak için rastgele örnekler bırakın
  Çinçe Çevirimi:Dropout 随机采样决定哪些神经元置零
- Veri artırma örnekleri rastgele dönüşümler
  Çinçe Çevirimi: Data增强采样随机变变
- Dil modelleri tahmin edilen dağılımdan bir sonraki simgeyi örnekler
  Çinçe Çevirimi:语言模型从预测分布中采样下一个词
- Diffüzyon modelleri gürültü örneğini ve ilerleyerek denosiyonunu gösterir
  Çinçe Çevirimi: yayılma modelleri ışığa giderek giderek ışığa gider

Kezleyici dağılımlardan örnek almak, ters dönüşüm örneği, reddetme örneği veya reparametreleme hilesi (VAE'lerde kullanılır) gibi teknikleri gerektirir.

> Bu yöntemler, farklı yöntemlerle kullanılır.

## Yapın.
```figure
gaussian-pdf
```

## Yapın

### Adım 1: Muhtemelenlik Temellikleri

```python
import math
import random

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def combinations(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def conditional_probability(p_a_and_b, p_b):
    return p_a_and_b / p_b

p_king_given_face = conditional_probability(4/52, 12/52)
print(f"P(King | Face card) = {p_king_given_face:.4f}")
```

### Adım 2: PMF ve PDF sıfırdan

```python
def bernoulli_pmf(k, p):
    return p if k == 1 else (1 - p)

def categorical_pmf(k, probs):
    return probs[k]

def poisson_pmf(k, lam):
    return (lam ** k) * math.exp(-lam) / factorial(k)

def uniform_pdf(x, a, b):
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0

def normal_pdf(x, mu, sigma):
    coeff = 1.0 / (sigma * math.sqrt(2 * math.pi))
    exponent = -0.5 * ((x - mu) / sigma) ** 2
    return coeff * math.exp(exponent)
```

### Adım 3: Beklenen değer ve değişim

```python
def expected_value(values, probabilities):
    return sum(v * p for v, p in zip(values, probabilities))

def variance(values, probabilities):
    mu = expected_value(values, probabilities)
    return sum(p * (v - mu) ** 2 for v, p in zip(values, probabilities))

die_values = [1, 2, 3, 4, 5, 6]
die_probs = [1/6] * 6
mu = expected_value(die_values, die_probs)
var = variance(die_values, die_probs)
print(f"Die: E[X] = {mu:.4f}, Var(X) = {var:.4f}, SD = {var**0.5:.4f}")
```

### 4. Adım: Distribüsiyonlardan örnek alınması

```python
def sample_bernoulli(p, n=1):
    return [1 if random.random() < p else 0 for _ in range(n)]

def sample_categorical(probs, n=1):
    cumulative = []
    total = 0
    for p in probs:
        total += p
        cumulative.append(total)
    samples = []
    for _ in range(n):
        r = random.random()
        for i, c in enumerate(cumulative):
            if r <= c:
                samples.append(i)
                break
    return samples

def sample_normal_box_muller(mu, sigma, n=1):
    samples = []
    for _ in range(n):
        u1 = random.random()
        u2 = random.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        samples.append(mu + sigma * z)
    return samples
```

### Adım 5: Softmax ve log olasılığı

```python
def softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    exps = [math.exp(z) for z in shifted]
    total = sum(exps)
    return [e / total for e in exps]

def log_softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = max_logit + math.log(sum(math.exp(z) for z in shifted))
    return [z - log_sum_exp for z in logits]

def cross_entropy_loss(logits, target_index):
    log_probs = log_softmax(logits)
    return -log_probs[target_index]
```

### Adım 6: Merkez Sınır Teoremi gösterimi

```python
def demonstrate_clt(dist_fn, n_samples, n_averages):
    averages = []
    for _ in range(n_averages):
        samples = [dist_fn() for _ in range(n_samples)]
        averages.append(sum(samples) / len(samples))
    return averages
```

### 7. Adım: Görüntüleme

```python
import matplotlib.pyplot as plt

xs = [mu + sigma * (i - 500) / 100 for i in range(1001)]
ys = [normal_pdf(x, mu, sigma) for x, mu, sigma in ...]
plt.plot(xs, ys)
```

Tüm görsellemeler ile birlikte tam uygulamalar `code/probability.py`- Evet .

> Tüm görülebilirliklerin tam gerçekleşmesi`code/probability.py`- Evet.

## Çerçeveyi kullanın.

NumPy ve SciPy ile yukarıda her şey tek satırlı:

> NumPy ve SciPy kullanın, yukarıdaki tüm özellikler sadece bir kod satırı gerektirir:

```python
import numpy as np
from scipy import stats

normal = stats.norm(loc=0, scale=1)
samples = normal.rvs(size=10000)
print(f"Mean: {np.mean(samples):.4f}, Std: {np.std(samples):.4f}")
print(f"P(X < 1.96) = {normal.cdf(1.96):.4f}")

logits = np.array([2.0, 1.0, 0.1])
from scipy.special import softmax, log_softmax
probs = softmax(logits)
log_probs = log_softmax(logits)
print(f"Softmax: {probs}")
print(f"Log-softmax: {log_probs}")
```

Şimdi kütüphane aramalarının ne yaptığını biliyorsun.

> Bu işlemi tamamen çözdün. Şimdi de kitlev fonksiyonunun ne yaptığını biliyorsun.

## Egzersizler.

1. Eksponansiyel dağılım için ters dönüşüm örneğini uygulayın. 10.000 değer örneği alıp histogramı gerçek PDF ile karşılaştırarak doğrulayın.

2. İki yüklü zar için ortak bir dağıtım masası oluşturun.

3. Logit çıkaran 5 sınıf sınıflandırıcı için çapraz entropik kaybı hesaplayın `[2.0, 0.5, -1.0, 3.0, 0.1]`Doğru sınıf indeks 3 olduğunda, sonra cevapınızı PyTorch'ın `nn.CrossEntropyLoss`- Evet .

4. Log olasılıklarının bir listesini alıp en olası sırayı, toplam log olasılığını ve eşdeğer çiğ olasılığı geri veren bir işlev yazın.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sample space | "All the possibilities" / "所有可能性" | The set S of every possible outcome of an experiment / 实验所有可能结果的集合 S |
| PMF | "The probability function" / "概率函数" | A function that gives the exact probability of each discrete outcome, summing to 1 / 给出每个离散结果精确概率的函数，总和为 1 |
| PDF | "The probability curve" / "概率曲线" | A density function for continuous variables. Integrate it over an interval to get probability / 连续变量的密度函数，在区间上积分得到概率 |
| Conditional probability | "Probability given something" / "条件概率" | P(A\|B) = P(A and B) / P(B). The foundation of Bayesian thinking and Bayes' theorem / 贝叶斯思维和贝叶斯定理的基础 |
| Independence | "They don't affect each other" / "互不影响" | P(A and B) = P(A) * P(B). Knowing one event tells you nothing about the other / 知道一个事件不影响另一个 |
| Expected value | "The average" / "平均值" | The probability-weighted sum of all outcomes. The loss function is an expected value / 所有结果的概率加权求和，损失函数就是一种期望值 |
| Variance | "How spread out" / "离散程度" | The expected squared deviation from the mean. High variance = noisy, unstable estimates / 偏离均值的平方的期望，方差大 = 噪声大、不稳定 |
| Normal distribution | "The bell curve" / "钟形曲线" | f(x) = (1/sqrt(2*pi*sigma^2)) * exp(-(x-mu)^2/(2*sigma^2)). Appears everywhere due to the CLT / 因中心极限定理而无处不在 |
| Central Limit Theorem | "Averages become normal" / "平均趋于正态" | The mean of many independent samples converges to a normal distribution regardless of the source / 许多独立样本的均值收敛到正态分布 |
| Joint distribution | "Two variables together" / "两个变量一起" | P(X, Y) describes the probability of every combination of X and Y outcomes / 描述 X 和 Y 每种组合的概率 |
| Marginal distribution | "Sum out the other variable" / "消去另一个变量" | P(X) = sum_y P(X, Y). Recovers one variable's distribution from the joint / 从联合分布中恢复单个变量的分布 |
| Log probability | "Log of the probability" / "概率的对数" | log P(x). Turns products into sums, preventing numerical underflow in long sequences / 将乘法变加法，防止长序列数值下溢 |
| Softmax | "Turn scores into probabilities" / "分数转概率" | softmax(z_i) = exp(z_i) / sum(exp(z_j)). Maps real-valued logits to a valid probability distribution / 将实数值 logits 映射为有效概率分布 |
| Cross-entropy | "The loss function" / "损失函数" | -sum(p_true * log(p_predicted)). Measures how different two distributions are. Lower is better / 衡量两个分布的差异，越小越好 |
| Logits | "Raw model outputs" / "模型原始输出" | Unnormalized scores before softmax. Named after the logistic function / softmax 之前的未归一化分数 |
| Sampling | "Drawing random values" / "随机取值" | Generating values according to a probability distribution. How models generate output / 按概率分布生成值，模型用它生成输出 |

## Daha fazla okumak

- [3Blue1Brown: But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo)- ortalamaların neden normal hale geldiğinin görsel bir kanıtı
- [Stanford CS229 Probability Review](https://cs229.stanford.edu/section/cs229-prob.pdf)- burada ve daha fazlasını kapsayan kısa bir referans
- [The Log-Sum-Exp Trick](https://gregorygundersen.com/blog/2020/02/09/log-sum-exp/)- Sayısal istikrar neden önemlidir ve nasıl elde edilebilir
