# Örnekleme yöntemleri.

> Örnekleme, AI'nin olasılık alanını nasıl keşfettiğini gösterir.
> 采样是 AI 探索可能性空间的方式──

**Type:** Build | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 06-07 (Probability, Bayes' Theorem) | **前置知识:** Phase 1, 第 06-07 课（概率、贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Öğrenme hedefleri

- Teker teker rastgele sayılar kullanarak ters CDF, reddetme ve önem örneğini sıfırdan uygulayın
  % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
- Dil model simge üretimi için sıcaklık, üst-k ve üst-p (yüzey) örneklemesini oluştur
  构建用于语言模型代号 生成的温度、top-k 和 top-p(nukleus)采样
- Reparametreleme hilesini ve neden VAE'lerde örnekleme yoluyla geri yayılmayı mümkün kılanını açıklayın.
  解释重参数化技巧(Reparameterization Trick) ve neden VAE'de kullanılan örneğin tarama yöntemi destekleyebilmesi için
- Metropolis-Hastings MCMC'yi normalleşmemiş bir hedef dağıtımdan örnek almak için çalıştır
  运行 Metropolis-Hastings MCMC


> **【中文解读】**
> 采样是 AI 探索可能性的方法──LLM 温度/top-k/top-p 控制文本生成多样性──VAE 重参数化技巧让采样可微──扩散模型的前向过程是采样(加噪),反向过程是去噪(生成)──

## Sorunlar. Sorunlar.

Dil modeli, sorguyu işlemeyi bitirir ve 50.000 logitlik bir vektör üretir. Sözlükte bir simge için bir tane. Şimdi bir tane seçmelidir. Nasıl?

> 语言模型处理完毕后,生成一个包含50,000 逻辑的向量,应词汇表中的每个代币――现在它需要从中选一个――如何选?

Eğer her zaman en yüksek olasılık belirtiğini seçerse, her cevap aynıdır. Deterministik. Sıkıcı. Eğer rastgele olarak eşit seçerse, çıkış kayıp olur. Cevap bu aşırılıkların arasında bir yerde yaşar ve bir yerlerde örnekleme ile kontrol edilir.

> Eğer her seferinde en yüksek olasılık belirtiği seçilirse, her cevap aynı kesinlik ve 无聊的. Eğer her seferinde de 随机选取,输出就是胡言乱语.

Örnekleme metin üretimi ile sınırlı değildir. Güçlendirme öğrenimi, örnekleme rotaları ile politika gradiyentlerini tahmin eder. VAE'ler öğrenilen dağılımlardan örnek alarak ve rastgelelik yoluyla geri yayılarak gizli temsilleri öğrenir. Diffüzyon modelleri gürültü örneği ve tekrar tekrar denoizasyon yoluyla görüntüler üretir. Monte Carlo yöntemleri, kapalı biçimli çözüm olmayan bütünleri tahmin eder. MCMC algoritmaları, saymak imkansız olan yüksek boyutlu arka dağılımları araştırır.

> 采样不仅限于文本生成──强化学习通过采样轨迹(轨迹) 来估计策略梯度──VAE 通过从学习到分布中采样并反向传播来学习隐表示──扩散模型通过采样噪声并代去噪声来生成图像──蒙特卡洛方法估算没有解析的积分──MCMC algoritması探索无法枚举的高维后验分布──

Her üreticik AI sistemi bir örnekleme sistemidir. Örnekleme stratejisi çıkışın kalitesini, çeşitliliğini ve kontrol edilebilirliğini belirler. Bu ders, her büyük örnekleme yöntemini sıfırdan inşa eder, eşit rastgele sayılardan başlayarak modern LLM'leri ve üreticik modellerle güçlendiren tekniklerle sona erer.

> Her üretilen AI sistemi aslında bir örneklem sistemidir. Seçim stratejisi, çıkışın kalitesini, çeşitliliğini ve kontrol edilebilirliğini belirler.

## Konsepten bir şey.

> **【中文解读】**
> 采样问题无处不在:语言模型需要从50,000代币中选一个,VAE需要从隐空间采样,扩散模型需要从噪音逐步到噪音――核心挑战是你只能直接从简单分布(均分布、正态分布) 采样,复杂目标分布的样本才能才能才能通过巧妙变换――

### Örnek Almanın Önemli Olduğu Nedeni

Örnekleme, AI ve makine öğrenimi genelinde dört temel rolde ortaya çıkar:

> 采样 AI ve makinelerle öğrenmede dört temel rol oynar:

**Generation.**Dil modelleri, difüzyon modelleri ve GAN'lar tümüyle örnekleme yoluyla çıkış üretir. Örnekleme algoritması yaratıcılığı, tutarlılığı ve çeşitliliği doğrudan kontrol eder.

> **生成。**语言模型、扩散模型和 GAN 采样通过采样产生输出──采样算法直接控制创造力、连贯性和多样性──温度、top-k 和核采样是工程师的日常调节的"旋──采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样算法,采样,采样,采样,采样,采样,采样,采样,采样,采样,采样,采样,采样,采样,采样,采样,采样,采样,

**Training.**Stochastic gradient descent örnekleri mini-batch. Deaktivasyon için nöron örnekleri bırakın. Veri artırma örnekleri rastgele dönüşümler. Önemlilik örneklemesi güçlendirme öğreniminde gradient variansını azaltmak için örnekleri yeniden ağırlaştırır (PPO, TRPO).

> **训练。**随机梯度下降(SGD) 采样 mini-batch──Dropout 采样 采样 禁用神经元──数据增强采样随机变化──重要性采样重新加权样本以降低强化学习──PPO、TRPO) 中的梯度方差──

**Estimation.**ML'deki birçok miktarda kapalı bir çözüm yoktur. Veriler dağıtımında beklenen kayıp, enerji tabanlı bir modelin bölünme fonksiyonu, Bayesian sonuçlarındaki kanıtlar. Monte Carlo tahminleri tüm bunları örnekler üzerinde ortalama olarak yaklaştırır.

> **估计。**ML'deki birçok miktar çözülmedi. Verim dağılımında beklenen kayıplar, enerji modelinin dağılım fonksiyonları, Bayes'in tahminindeki kanıtlar, örneklere karşı ortalama bir tahminle tüm bu miktarlara yaklaşmak için Monte Carlo'nun tahminleri.

**Exploration.**MCMC algoritmaları Bayesian sonuçlarında arka dağılımları araştırır. Evrimsel stratejiler parametreler bozukluklarını örnekler. Thompson örneklemesi, suikastçılarda keşif ve sömürü dengeler.

> **探索。**MCMC Algoritmi, Bayes'in tahmininde keşfedilen ve yayılan yöntemleri geliştirme stratejileri, evrimsel stratejiler, örneklemeler ve sorunlar arasında araştırma ve kullanım biçimlerini geliştirmek için kullanılan algoritmalar.

Temel zorluk: sadece basit dağılımlardan (eşit, normal) doğrudan örnek alabilirsiniz. Diğer her şey için, basit örnekleri hedef dağılımınızdan örneklere dönüştürmek için bir yöntem gerekir.

> 核心挑战: You can only directly from simple distribution (Hazırlı dağılım, Normal dağılım) 中采样. Diğer dağılımlar için, basit örneği hedef dağılım örneğine dönüştüren bir yöntem gerekir.

> **【拓展：LLM 采样策略的工程实践】**
> GPT-4等 model düşünce zaman, sıcaklık genellikle 0.0-1.0, üst-p    0.9-1.0 olarak ayarlanır. OpenAI API 默认温度=1.0、top_p=1.0。 Araştırmalar üst-p (nukleus) 采样在大多数任务上优于上-k,因为它能根据模型置信度自适应调整候选集大小──对代生成,温度=0.2 + top_p=0.95 是常见配置──

### Eşsiz Rastgele Örnekleme

Her örnekleme yöntemi burada başlar. Bir benzer rastgele sayı jeneratörü, eşit uzunlukta her alt aralığın eşit olasılıkla olduğu [0, 1) değerlerini üretir.

> Tüm örnek yöntemler buradan başlar. Ortalama olarak, sayı üreticisi orta değerlerin [0, 1) oluşmasını sağlar.

```
U ~ Uniform(0, 1)

P(a <= U <= b) = b - a    for 0 <= a <= b <= 1

Properties:
  E[U] = 0.5
  Var(U) = 1/12
```

N öğelerin ayrı bir setinden benzer bir şekilde örnek almak için U oluşturun ve tekrar katı ((n * U).

> N 个元素的离散集合中均采样,生成 U 并返回 floor(n * U) 』;

Anahtar bir anlayış: tek bir eşsiz rastgele sayı herhangi bir dağılımdan bir örnek üretmek için tam olarak doğru miktarda rastgeleliği içerir.

> 关键洞察: Tek ortalama 随机数, herhangi bir dağılımdan bir örneği oluşturmak için yeterince 随机性 içerir.

> **【中文解读】**
> 均分布是所有采用基石──计算机中的伪随机数生成器 (Mersenne Twister gibi) oluşur, 均分布是 [0,1) 上的均分布──采用方法本质上是把均随机数"变换" into target distribution 样本,就像用一把万能钥匙打开不同的锁──

### Ters CDF Yöntem (Dönüştürülmüş Değişiklik Örnekleme)

Kumulatif dağılım fonksiyonu (CDF) değerleri olasılıklara haritası yapar:

```
F(x) = P(X <= x)

Properties:
  F is non-decreasing
  F(-inf) = 0
  F(+inf) = 1
  F maps the real line to [0, 1]
```

Ters CDF olasılıkları değerlere geri harfler. Eğer U ~ Uniform(0, 1), o zaman X = F_inverse(U) hedef dağılım takip eder.

> 逆 CDF 将概率映射回值──若 U ~ Uniform(0, 1),那么 X = F_inverse(U) 服从目标分布──

```
Algorithm:
  1. Generate u ~ Uniform(0, 1)
  2. Return F_inverse(u)

Why it works:
  P(X <= x) = P(F_inverse(U) <= x) = P(U <= F(x)) = F(x)
```

**Exponential distribution example:**

```
PDF: f(x) = lambda * exp(-lambda * x),   x >= 0
CDF: F(x) = 1 - exp(-lambda * x)

Solve F(x) = u for x:
  u = 1 - exp(-lambda * x)
  exp(-lambda * x) = 1 - u
  x = -ln(1 - u) / lambda

Since (1 - U) and U have the same distribution:
  x = -ln(u) / lambda
```

Bu, F_inverse'i kapalı biçimde yazabildiğinizde mükemmel bir şekilde çalışır. Normal dağılım için, kapalı biçimdeki ters CDF yoktur, bu yüzden diğer yöntemleri kullanıyoruz (Box-Muller veya sayısal yaklaşım).

> F_inverse'in çözünürlüğünü ifade ederken yazabilince, bu yöntem mükemmel bir şekilde kullanılır.

**Discrete version:**Diskre dağılımlar için CDF'yi kumülatîf bir toplam olarak oluşturun, U oluşturun ve kumülatîf toplamın U'yu aştığı ilk indeks bulun.`sample_categorical`6. Ders'te çalışmalar.

> **离散版本：**对于离散分布,将CDF 构建为累积和,生成 U,找到累积和首次超过 U 的索引――这是第06 课中`sample_categorical`Yapım biçimi:

> **【中文解读】**
> 逆 CDF 方法の核心思想:CDF 函数 F(x) 随机変数 değerini [0,1] 上の概率'a映射する, onun 逆関数 F_inverse 正好反过来把 [0,1] 上の均随机数を目標分布の値に映射する── bu yöntem kesin、高效, ancak önemi ise 逆関数の解析式 ifadeini yazabilmenizdir──

### Reddetme Örnekleme

CDF'yi tersine çeviremediğinizde ama hedef PDF'yi sabit bir şekilde değerlendirebildiğinizde, reddetme örneği çalışmaktadır.

> Eğer CDF'ye karşı talep edemezsen, ama hedefini hesaplayabilirsin PDF (Finanse)

```
Target distribution: p(x)  (can evaluate, possibly unnormalized)
Proposal distribution: q(x)  (can sample from)
Bound: M such that p(x) <= M * q(x) for all x

Algorithm:
  1. Sample x ~ q(x)
  2. Sample u ~ Uniform(0, 1)
  3. If u < p(x) / (M * q(x)), accept x
  4. Otherwise, reject and go to step 1

Acceptance rate = 1/M
```

M'nin bağlanması ne kadar sıkı olursa, kabul oranı o kadar yüksek olur. Düşük boyutlarda (1-3), reddetme örneği iyi çalışır. Yüksek boyutlarda, kabul oranı, önerinin büyük bir kısmı reddedildiği için eksponansal olarak düşer. Bu reddetme örneği için boyutluk lanetidir.

> 包络 M 越紧, kabul oranı越高──在低维空间 (低维空间) 1-3 维), kabul oranı çok iyi olmuştur──在高维空间 (高维空间) 接受率呈指数下降,因为大部分提议体积都被拒绝了──这是拒绝采采样的维数灾难──

**Example: sampling from a truncated normal.**Kısaltılmış aralık üzerinde bir teklifte bulun. M zarf, bu aralığın normal PDF'lerinin maksimumıdır.

> **示例：从截断正态分布采样。**Kesinlik aralığında kullanım ortalama öneriler dağıtımı.

**Example: sampling from a semicircle.**Yönlü düzbuzda teker teker önerin. Nokta yarı döngü içinde düşerse kabul edin. Monte Carlo pi'yi böyle hesaplar: kabul oranı alan oranı pi/4'e eşittir.

> **示例：从半圆采样。**Dış düzlemde ortalama öneriler. Eğer nokta yarım döngü içinde düşerse kabul edilir. Bu Monte Carlo'da pi'yi hesaplama yöntemidir.

> **【拓展：拒绝采样在粒子滤波中的应用】**
> Particle波(Particle Filter) hedef takip ve makinelerin konumlandırılması için temel bir algoritmadır. Bu aslında bir grup "particle" ile örneklemeyi reddetmek için bir yöntemdir.

### Önemlilik Örnekleme

Bazen hedef dağılım p(x'den örneklere ihtiyacınız yoktur. Bir beklentiyi p(x altında tahmin etmek gerekir ve farklı bir dağılım q(x'den örnekler vardır.

> Bazen hedef dağılım p(x) arasında bir örnek almak zorunda değilsiniz, ama bir beklentiyi p(x) altında tahmin etmek gerekir, ve diğer dağılım q(x) üzerinde bir örnek var.

```
Goal: estimate E_p[f(x)] = integral of f(x) * p(x) dx

Rewrite:
  E_p[f(x)] = integral of f(x) * (p(x)/q(x)) * q(x) dx
            = E_q[f(x) * w(x)]

where w(x) = p(x) / q(x)  are the importance weights.

Estimator:
  E_p[f(x)] ~ (1/N) * sum(f(x_i) * w(x_i))    where x_i ~ q(x)
```

Bu, güçlendirme öğreniminde kritik bir önem taşır. PPO (Prosimal Policy Optimization) da eski bir politika pi_old altında yoldurları toplarsınız ancak yeni bir politika pi_new'i optimize etmek istiyorsunuz. Önemliyet ağırlığı pi_new'ler / pi_old'lar.

> Bu, güçlü bir bilimsel eğitimde çok önemlidir. PPO'da, eski stratejilerde, yeni stratejileri iyileştirmeyi düşünüyorsun.

> **【拓展：PPO 中的重要性采样】**
> PPO, ChatGPT RLHF ıktırmalarının temel algoritmasıdır. Yeni eski stratejilerin arasındaki dağılım farkını düzeltmek için önemlidir.

Önemlilik örnekleme tahminçisinin değişimi q'nın p'ye ne kadar benzer olduğuna bağlıdır. q p'den çok farklıysa, birkaç örnek büyük ağırlıklar alır ve tahminin baskısıdır.

> Önemlilik örneği değerlendiricisinin farkı q ile p arasındaki benzerlik derecesine bağlıdır. Eğer q ile p arasındaki fark büyükse, az sayıda örnek büyük bir ağırlık elde eder ve değerlendirmeyi yönlendirir.

```
E_p[f(x)] ~ sum(w_i * f(x_i)) / sum(w_i)
```

### Monte Carlo Tahmini

Monte Carlo tahminleri rastgele örneklerin ortalamasını kullanarak bütünlükleri yakındırır. Büyük sayılar kanunu, yakınlaşmayı garanti eder.

> Monte Carlo'nun tahminleri, rastlantı örneklerine karşı ortalama bir yaklaşımlılık göstermektedir.

```
Goal: estimate I = integral of g(x) dx over domain D

Method:
  1. Sample x_1, ..., x_N uniformly from D
  2. I ~ (Volume of D / N) * sum(g(x_i))

Error: O(1 / sqrt(N))   regardless of dimension
```

Hata oranı boyutlara bağlıdır. Bu nedenle Monte Carlo yöntemleri, ağ tabanlı entegrasyonun mümkün olmadığı yüksek boyutlarda baskındır.

> Bu nedenle Monte Carlo yöntemi yüksek boyutlu alanlarda üstünlük kazanıyor.

> **【中文解读】**
> Monte Carlo yönteminin özelliği: her zamanki örneklerin ortalama değerini kullanarak yaklaşım beklentilerini gerçekleştirmek için. Büyük sayı teorisi, kazançın, hata oranının O(1/sqrt(N) ile ölçüm ile ilgisi yoktur. Bu, yüksek boyutlu sorunlarda çok önemlidir.

**Estimating pi:**

```
Sample (x, y) uniformly from [-1, 1] x [-1, 1]
Count how many fall inside the unit circle: x^2 + y^2 <= 1
pi ~ 4 * (count inside) / (total count)
```

**Estimating expectations:**

```
E[f(X)] ~ (1/N) * sum(f(x_i))    where x_i ~ p(x)

The sample mean converges to the true expectation.
Variance of the estimator = Var(f(X)) / N
```

### Markov Chain Monte Carlo (MCMC): Metropolis-Hastings

MCMC, sabit dağılımının hedef dağılım p ((x) olan Markov zinciri oluşturur. Yeterli adımlardan sonra, zincirden örnekler (yaklaşık olarak) p ((x) örnekler olur.

> MCMC  yapılandırmak bir Markov zinciri , onun düz düz dağılımı  İstasyonel dağılımı                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

```
Target: p(x)  (known up to a normalizing constant)
Proposal: q(x'|x)  (how to propose the next state given the current state)

Metropolis-Hastings algorithm:
  1. Start at some x_0
  2. For t = 1, 2, ..., T:
     a. Propose x' ~ q(x'|x_t)
     b. Compute acceptance ratio:
        alpha = [p(x') * q(x_t|x')] / [p(x_t) * q(x'|x_t)]
     c. Accept with probability min(1, alpha):
        - If u < alpha (u ~ Uniform(0,1)): x_{t+1} = x'
        - Otherwise: x_{t+1} = x_t
  3. Discard first B samples (burn-in)
  4. Return remaining samples
```

Simetrik öneriler için (q(x'taitx) = q(x tık x') oranı p(x')/p(x'e basitleştirilir.

> 对于对称提议 (q) = q (x) ),比率简化为 p (x) /p (x)  (x) ).

**Why it works.**Kabul kuralı detaylı dengeyi sağlar: x'de bulunma ve x'ye taşınma olasılığı x'de bulunma ve x'ye taşınma olasılığına eşit olur. Detaylı denge p ((x) zincirin sabit dağılımını içerir.

> **为什么有效。**接受规则确保细致平衡条件 (Detailed Balance): x'de x'ye geçiş olasılığı x'de x'ye geçiş olasılığıyla eşittir.

> **【拓展：MCMC 在贝叶斯深度学习中的应用】**
> PyMC、NumPyro 等 Bayesian 推理框架ın merkezi MCMC¬¬TS (No-U-Turn Sampler) NUTS'tir, en gelişmiş MCMC 变体, otomatik olarak adım boyu ve yönü düzenler.

**Practical considerations:**
- Yanma: zincir dengeleme ulaşmadan önce erken örnekler atılır
  预热期(Burn-in): 抛弃链达到平衡前的早期样本
- İnceleme: Otokorelasyonu azaltmak için her k-te örnek tutun
  稀释(Tünleme): Her bölük k 个样本保留一个以减少自相关
- Teklif ölçeği: çok küçük ve zincir yavaş hareket eder (yüksek kabul, yavaş araştırmalar); çok büyük ve çoğu teklif reddedilmiştir ( düşük kabul, yerinde kalmıştır)
  提议尺度(Tasavvvu ölçeği): 太小则链移动缓慢(接受率高但探索慢); 太大则大多数提议被拒绝(接受率低,原地不动)
- Yüksek boyutlarda Gaussian önerisi için en iyi kabul oranı yaklaşık 0.234'dir.
  Yüksek Uzay Orta Yüksek Öneriler'in en iyi kabul oranı yaklaşık 0.234'dir.

### Gibbs Örnekleme

Gibbs örnekleme, çok değişken dağılımlar için MCMC'nin özel bir durumudur. Tüm boyutlarda bir seferde bir hareket önermek yerine, koşullu dağılımından bir değişkenyi bir seferde güncelleştirir.

> Gibbs'in örneği, MCMC'nin çok değişkenlik dağılımında bir örneğidir. Tüm boyutlarda aynı anda bir öneride hareket etmiyor, tersine koşul dağılımından her kez bir değişken yeniliyor.

```
Target: p(x_1, x_2, ..., x_d)

Algorithm:
  For each iteration t:
    Sample x_1^{t+1} ~ p(x_1 | x_2^t, x_3^t, ..., x_d^t)
    Sample x_2^{t+1} ~ p(x_2 | x_1^{t+1}, x_3^t, ..., x_d^t)
    ...
    Sample x_d^{t+1} ~ p(x_d | x_1^{t+1}, x_2^{t+1}, ..., x_{d-1}^{t+1})
```

Gibbs örneği, her koşullu dağılımdan örnek alabilmenizi gerektirir.
- Bayesian ağlar: grafik yapısından şartlar
  贝叶斯网络: koşullar dağılımı yapı tarafından belirlenir
- Gaussian karışımları: şartlar Gaussian
  Yüksek karışıklık modeli: koşulların dağılımı Yüksek
- İzin modelleri: her spin'in koşulları sadece komşularına bağlıdır
  Ising 模型: Her bir dönüm koşullarının dağılımı sadece komşusuna bağlıdır

Kabul oranı her zaman 1'dir (her teklif kabul edilir), çünkü tam şartlı örnekleme otomatik olarak ayrıntılı dengeni tatmin eder.

> 接受率永远是1 (Her önerme kabul edilir), çünkü belirli koşulların dağılımında örnekler otomatik olarak ince dengeleme koşullarını karşılar.

**Limitation.**Değişkenler yüksek bir korelasyonda olduğunda, Gibbs örnekleme yavaş karışır çünkü bir değişkenyi bir seferde güncelleme dağılım boyunca büyük çapraz hareketler yapamaz.

> **局限性。**Değişiklikler arasında yükseklik ilişkilendirilince, Gibbs'in ışığı çok yavaş karışır, çünkü her güncelleştirilen bir değişiklik dağılımda büyük bir karşı köşeler hareketini yapamaz.

> **【中文解读】**
> Gibbs'in örnekleri MCMC'nin bir özelliğidir: Her seferinde sadece bir değişken, koşul dağılımından yenileştirilir. Çünkü her örnek kesin koşul dağılımından gelir, bu yüzden kabul oranı her zaman %100'dir.

### Temperatür örneği (LLM'lerde kullanılır)

Dil modelleri sözcüklükteki her token için z_1, ..., z_V logitlerini çıkarır. Softmax bunları olasılıklara dönüştürür.

> 语言模型为词汇表中的每个代币 输出 logits z_1, ..., z_V──Softmax将它们转换为概率──温度(温度) 在软max 之前对 logits 进行缩放:

```
p_i = exp(z_i / T) / sum(exp(z_j / T))

T = 1.0: standard softmax (original distribution)
T -> 0:  argmax (deterministic, always picks highest logit)
T -> inf: uniform (all tokens equally likely)
T < 1.0: sharpens the distribution (more confident, less diverse)
T > 1.0: flattens the distribution (less confident, more diverse)
```

**Why it works.**Logitleri T < 1 ile bölmek logitler arasındaki farkları artırır. Z_1 = 2 ve z_2 = 1 ise, T = 0.5 ile bölmek z_1/T = 4 ve z_2/T = 2 verir.

> **为什么有效。**Eğer z_1 = 2、z_2 = 1, t = 0.5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

**In practice:**
- T = 0.0: açgözlülükle çözme, gerçekçi soru ve cevaplar için en iyisi
  贪心解码,最适合事实性问答
- T = 0.3-0.7: biraz yaratıcı, kod üretimi için iyi
  略有创意,适合代码生成
- T = 0,7-1,0: dengeli, genel konuşma için iyi
  均衡,适合一般对话
- T = 1.0-1.5: Yaratıcı yazma, beyin fırtınası
  创意写作、头脑风暴
- T > 1,5: giderek rastgele, nadiren kullanışlı
  Çok az işe yarıyor.

Temperatür, hangi tokenlerin mümkün olduğunu değiştirmez. Her token'a verilen olasılık kütlesini değiştirir.

> 温度 değişmez hangi token seçilebilir. ⇒ değişir.

> **【中文解读】**
> Sıcaklık ise LLM 输出多样性的"旋"──T < 1 让分布更尖(更像贪心),T > 1 让分布更平坦(更随机)──T → 0 退化为 argmax,T → ∞ 退化为均分布──实际中 T=0.7 常用平衡点──注意:温度不改变哪些符号有可能被选中,只改变概率分配──

### Top-k Örnekleme

Top-k örnekleme, aday seti en yüksek olasılıklara sahip k jetonlarına sınırlandırır, ardından bu sınırlı setten örnekleri yeniden normalleştirir ve gösterir.

> Top-k 采样将候选集限制至概率最高的 k 个代币,然后重新归归并从该受限集合中采样.

```
Algorithm:
  1. Compute softmax probabilities for all V tokens
  2. Sort tokens by probability (descending)
  3. Keep only the top k tokens
  4. Renormalize: p_i' = p_i / sum(p_j for j in top-k)
  5. Sample from the renormalized distribution

k = 1:  greedy decoding
k = V:  no filtering (standard sampling)
k = 40: typical setting, removes long tail of unlikely tokens
```

Top-k, sözlük dağılımının uzun kuyruğunda bulunan son derece olası olmayan jetonları (tipos, saçma) seçmekten modelin kaçınıyor. Sorun: k bağlamdan bağımsız olarak sabitlenir. Model güvenlidir (bir jeton 95% olasılıklara sahiptir), k = 40 hala 39 alternatif izin verir.

> Top-k 防止模型选择词汇分布长尾中极不可能的符号(错别字、无意义的词) ・・・ sorunun yanı sıra:k is fixed, does not follow up下文变化。当模型很有信心时(1 token 占据 95% 概率),k = 40 仍允许39 替代选项──当模型不确定时(概率分散在1000 个 token 上),k = 40 会截断的合理选项──

### Üst-p (Nucleus) Örnekleme

Top-p örneklemesi aday setinin boyutunu dinamik olarak ayarlar.

> Top-p 采样动态调整候选选集大小──它不保留固定数量的代币,而是保留累积概率超过p的最小代币集合──

```
Algorithm:
  1. Compute softmax probabilities for all V tokens
  2. Sort tokens by probability (descending)
  3. Find smallest k such that sum of top-k probabilities >= p
  4. Keep only those k tokens
  5. Renormalize and sample

p = 0.9:  keeps tokens covering 90% of probability mass
p = 1.0:  no filtering
p = 0.1:  very restrictive, nearly greedy
```

Modelle güven olduğu zaman, çekirdek örneklemesi birkaç simgeyi (belki 2-3) tutar.Modelle belirsiz olduğunda, birçok simgeyi (belki 200) tutar. Bu uyarlayıcı davranış, çekirdek örneklemesinin genellikle üst-k'den daha iyi metin üretmesinin nedeni.

> Model güvenli olduğunda, çekirdek ışığı sadece küçük miktarda token tutar. model belirsiz olduğunda, çok fazla ışığa sahip olur.

**Common combinations:**
- Temperatür 0,7 + üst-p 0,9: İyi genel amaçlı ayarlama
  İyi genel ayar
- Sıcaklık 0.0 (açık): Deterministik görevler için en iyi
  En uygun belirlenme görevleri
- Temperatür 1.0 + üst-k 50: Fan et al. (2018) orijinal kağıt ayarları
  Fan 等人 (2018) 原论文设置

Top-k ve top-p bir araya gelebilir.

> Top-k 和 top-p 组合使用──先应用 top-k,再在剩余集合上应用 top-p──

### Reparametreleme hilesi (AVE'lerde kullanılır)

Variasyonel otokodlayıcılar (VAE) girişleri gizli bir alanın bir dağılımına kodlayarak, bu dağılımdan örnek alarak ve örnekten geri kodlama yoluyla öğrenirler.

> 变分自编码器(VAE) tarafından gömülü alanın dağılımına kod ekleyecek, bu dağılımdan sonra örnek çözümü tekrar öğrenmek için gelmek için.

```
Standard sampling (not differentiable):
  z ~ N(mu, sigma^2)

  The randomness blocks gradient flow.
  d/d_mu [sample from N(mu, sigma^2)] = ???
```

Reparametreleme hilesi rastgeleliği parametrelerden ayırır:

> Çekilme teknikleri, parametrlerle rastlantılı olarak ayrılır:

```
Reparameterized sampling:
  epsilon ~ N(0, 1)          (fixed random noise, no parameters)
  z = mu + sigma * epsilon   (deterministic function of parameters)

  Now z is a deterministic, differentiable function of mu and sigma.
  d(z)/d(mu) = 1
  d(z)/d(sigma) = epsilon

  Gradients flow through mu and sigma.
```

Bu, N(mu, sigma^2) ile mu + sigma * N(0,1 arasındaki aynı dağılım nedeniyle çalışır. Anahtar anlayış: rastlantıyı bir parametre dışı kaynağa (epsilon) taşıyarak, sonra örneği parametrelerin farklılaştırılabilir bir dönüşümü olarak ifade edin.

> Bu nedenle geçerli, çünkü N(mu, sigma^2) ile mu + sigma * N(0, 1)  aynı dağılımlı olacaktır.

**In the VAE training loop:**
1. Kodlayıcı çıkışları mu ve log(sigma^2) her giriş için
2. Örnek epsilon ~ N(0, 1)
3. Z = mu + sigma * epsilon hesaplayın
4. Girişi yeniden yapılandırmak için z kodunu çöz
5. 4, 3, 2, 1 adımları üzerinden geriye yayılmak (mümkün çünkü adım 3 farklılaştırılabilir)

Reparametrizasyon hilesi olmadan, VAE'ler standart geri yayılma ile eğitilmez.

> ⇒                                                                                                                                                                                                                                                              

> **【拓展：重参数化技巧的广泛应用】**
> Heavy parameterization teknikleri VAE'ye sınırlı değildir. Yayınlama modeli (((Stable Diffusion、DALL-E) her adımında gürültü kullanılır. Heavy parameterization:z = mu + sigma * epsilon。

### Gumbel-Softmax (Farklı Kategorik Örnekleme)

Devamlı dağılımlar için (Gaussian) reparametreleme hilesi işe yarıyor. Ayrı kategorik dağılımlar için farklı bir yaklaşım gerekmektedir. Gumbel-Softmax kategorik örnekleme için farklılaştırılabilir bir yaklaşım sağlar.

> Ağırlama teknikleri sürekli dağılım için uygundur. Ayrılıklı dağılım için farklı yöntemler gerekmektedir.

**The Gumbel-Max trick (non-differentiable):**

```
To sample from a categorical distribution with log-probabilities log(p_1), ..., log(p_k):
  1. Sample g_i ~ Gumbel(0, 1) for each category
     (g = -log(-log(u)), where u ~ Uniform(0, 1))
  2. Return argmax(log(p_i) + g_i)

This produces exact categorical samples.
```

**Gumbel-Softmax (differentiable approximation):**

```
Replace the hard argmax with a soft softmax:
  y_i = exp((log(p_i) + g_i) / tau) / sum(exp((log(p_j) + g_j) / tau))

tau (temperature) controls the approximation:
  tau -> 0:  approaches a one-hot vector (hard categorical)
  tau -> inf: approaches uniform (1/k, 1/k, ..., 1/k)
  tau = 1.0: soft approximation
```

Gumbel-Softmax, ayrı bir örnekin sürekli gevşemesini sağlar. Çıktı sonuç sert bir sıcak yerine bir olasılık vektörü (yumuşak bir sıcak) olur. Gradiyentler yumuşak maksimum üzerinden akıyor. Eğitimde ileri geçiş sırasında, "doğru-önce" tahminçisini kullanabilirsiniz: ileri geçiş için sert argmax kullanın, ancak geri geçiş için yumuşak Gumbel-Softmax gradiyentleri kullanın.

> Gumbel-Softmax 产生离散样本的连续松(Continuous Relaxation) ・・・输出是一个概率向量(软一热) 而不是硬一热──梯度可以流过软max──在训练的前向传播中,你可以使用"直通估计器"(Straight-Through Estimator):前向传播使用硬 argmax,反向传播使用软 Gumbel-Softmax 梯度──

**Applications:**
- VAE'lerde gizli değişkenlerin ayrıntılı olması
  VAE'de ayrılma değişimi
- Nöral mimarlık araması (diskret işlemleri seçmek)
  神经架构搜索 (örnekle birlikte çalışmak)
- Zor dikkat mekanizmaları
  硬注意力機
- Ayrı hareketlerle güçlendirme öğrenimi
  离散动作强化学习 (Yekilen hareketlerin güçlendirilmesi)

### Katmanlı Örnekleme

Standart Monte Carlo örneklemesi, örnek alanında rastlantı sonucu boşluklar bırakabilir.

> 标准蒙特卡洛采样可能会偶然在样本空间中留下空隙──分层采样──Stratified Sampling) 通过将空间分为层──Strata) 并从每层中采样来强制均覆盖──

```
Standard Monte Carlo:
  Sample N points uniformly from [0, 1]
  Some regions may have clusters, others gaps

Stratified sampling:
  Divide [0, 1] into N equal strata: [0, 1/N), [1/N, 2/N), ..., [(N-1)/N, 1)
  Sample one point uniformly within each stratum
  x_i = (i + u_i) / N   where u_i ~ Uniform(0, 1),  i = 0, ..., N-1
```

Stratifikasyonlu örneklemenin her zaman standart Monte Carlo'ya kıyasla daha düşük veya eşit bir değişimi vardır:

> Bölümsel açıdan farklılıklar her zaman standart Monte Carlo'dan daha düşük veya eşit:

```
Var(stratified) <= Var(standard Monte Carlo)

The improvement is largest when f(x) varies smoothly.
For piecewise-constant functions, stratified sampling is exact.
```

**Applications:**
- Sayısal entegrasyon (quasi-Monte Carlo)
  Numara: (Hazırlık)
- Eğitim verileri bölünür (her kattaki sınıf dengesini sağlamak)
  训练数据划分(确保每折的类别平衡)
- Stratifikasyonla birlikte önemlilik örneği alımı (eki tekniği birleştirmek)
  结合分层的重要性采样
- Neural Radiance Fields (Neural Radiance Fields) kamera ışınları boyunca katlandırılmış örnekleme kullanır
  NeRF(nervous radiation field) boyunca kamera ışığı kullanımı

### Diffüzyon Modelleri ile Bağlantı

Diffusion modelleri örnekleme süreci aracılığıyla görüntüler üretir. Ön süreci saf gürültü haline gelene kadar bir görüntüye T adımları üzerinde Gaussian gürültüsü ekler. Ters süreci, adım adım orijinal görüntüyü geri kazanarak denosiyon yapmayı öğrenir.

> 扩散模型采样过程通过采样过程生成图像――前向过程在T 步骤内逐渐图像向增加高的噪音,直到变成纯噪音――反向过程学习去噪音,逐步恢复原始图像――

```
Forward process (known):
  x_t = sqrt(alpha_t) * x_{t-1} + sqrt(1 - alpha_t) * epsilon
  where epsilon ~ N(0, I)

  After T steps: x_T ~ N(0, I)  (pure noise)

Reverse process (learned):
  x_{t-1} = (1/sqrt(alpha_t)) * (x_t - (1 - alpha_t)/sqrt(1 - alpha_bar_t) * epsilon_theta(x_t, t)) + sigma_t * z
  where z ~ N(0, I)

  Each denoising step is a sampling step.
```

Bu dersdeki yöntemlerle bağlantı:
- Her denoizing adım reparameterizasyon hilesi kullanır (sample gürültüsü, deterministik dönüşüm uygula)
  Her ses çıkartma adımında yeniden parametreleme teknikleri kullanılır.
- Gürültü programı {alpha_t} bir tür sıcaklık kaydırma kontrolü sağlar.
  噪音调度 {alpha_t} 控制一种形式的温度退火(Hava sıcaklığı Anning)
- Eğitim, ELBO'yu (gösteriler alt sınır) yakınlaştırmak için Monte Carlo tahminini kullanıyor.
  訓練使用蒙特卡洛估算来近似ELBO(Evidence Lower Bound,证据下界)
- Diffüzyon modellerinde ata örneklemesi Markov zinciridir (her adım sadece mevcut durumdan bağlıdır)
  扩散模型中的祖先采样 (Ancestral Sampling) bir varlıklı zincirdir (Her adım sadece mevcut durumdan bağlıdır)

Tüm görüntü oluşturma süreci tekrarlayıcı örnekleme: gürültüden başlayarak, her adımda öğrenilen denoizing modeline bağlı olarak biraz daha az gürültülü bir versiyon örnekleyin.

> Tüm görüntü üretimi süreci generasyonal bir örnekle oluşur: gürültüden başlayarak, her aşamada, öğrenilen bir gürültü modeli biçimlendirerek, biraz daha karmaşık bir versiyon oluşturur.

## Yapın.
```figure
monte-carlo-pi
```

## Yapın

### Adım 1: Teker teker CDF örneği ve ters CDF örneği

```python
import math
import random

def sample_uniform(a, b):
    return a + (b - a) * random.random()  # 线性变换：把 [0,1) 映射到 [a,b)

def sample_exponential_inverse_cdf(lam):
    u = random.random()                   # 生成均匀随机数
    return -math.log(u) / lam             # 逆 CDF：x = -ln(u) / lambda
```

10.000 eksponensial örnek oluşturun ve ortalamanın 1/lambda olduğunu doğrulayın.

> 生成 10,000 个指数分布样本,验证平均值是否为1/lambda──

### Adım 2: Reddedilme örneği

```python
def rejection_sample(target_pdf, proposal_sample, proposal_pdf, M):
    while True:                           # 持续采样直到被接受
        x = proposal_sample()             # 从提议分布采样
        u = random.random()               # 均匀随机数用于决定接受/拒绝
        if u < target_pdf(x) / (M * proposal_pdf(x)):  # 接受条件
            return x
```

Kısaltılmış normal bir dağılımdan çekmek için reddedilme örneklemesini kullanın.

> Kullanım: Kısıtlı normal dağılımdaki örnekler.

### Adım 3: Önemlilik örneği

```python
def importance_sampling_estimate(f, target_pdf, proposal_pdf, proposal_sample, n):
    total = 0
    for _ in range(n):
        x = proposal_sample()
        w = target_pdf(x) / proposal_pdf(x)
        total += f(x) * w
    return total / n
```

E[X^2]'yi, bir teker teker öneride normal bir dağılım altında tahmin edin. Bilinen yanıtla karşılaştırın (mu^2 + sigma^2).

> Uygulamada kullanılan değerli değerler, değerlendirme ve değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değerleri, değerlendirme değer, değerlendirme değer, değer değer değer değer değer değer, değerlendirme değer, değer, değer değer değer değer değer değer değer değer değer değer değer değer değer değer değer

### Adım 4: Monte Carlo pi tahmin

```python
def monte_carlo_pi(n):
    inside = 0
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x*x + y*y <= 1:
            inside += 1
    return 4 * inside / n
```

### Adım 5: Metropolis-Hastings MCMC

```python
def metropolis_hastings(target_log_pdf, proposal_sample, proposal_log_pdf, x0, n_samples, burn_in):
    samples = []
    x = x0                                # 初始状态
    for i in range(n_samples + burn_in):
        x_new = proposal_sample(x)        # 从提议分布生成新候选
        log_alpha = (target_log_pdf(x_new) + proposal_log_pdf(x, x_new)  # 计算接受比的对数
                     - target_log_pdf(x) - proposal_log_pdf(x_new, x))
        if math.log(random.random()) < log_alpha:  # 以 min(1, alpha) 的概率接受
            x = x_new
        if i >= burn_in:                  # 丢弃 burn-in 阶段的样本
            samples.append(x)
    return samples
```

İki Gaussian karışımı olan bimodal dağılımdan örnek.

> İki yüksekliklerin karışımı arasında görülür.

### Adım 6: Gibbs örneği

```python
def gibbs_sampling_2d(conditional_x_given_y, conditional_y_given_x, x0, y0, n_samples, burn_in):
    x, y = x0, y0
    samples = []
    for i in range(n_samples + burn_in):
        x = conditional_x_given_y(y)
        y = conditional_y_given_x(x)
        if i >= burn_in:
            samples.append((x, y))
    return samples
```

### Adım 7: Temperatür örneği

```python
def softmax(logits):
    max_l = max(logits)
    exps = [math.exp(z - max_l) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def temperature_sample(logits, temperature):
    scaled = [z / temperature for z in logits]  # 温度缩放：除以 T
    probs = softmax(scaled)                      # 计算缩放后的概率分布
    return sample_from_probs(probs)
```

Bir dizi token logit için sıcaklık çıkış dağılımını nasıl değiştirdiğini göster.

> 展示温度如何改变一组代码日志的输出分布──

### Adım 8: Üst-k ve üst-p örnekleme

```python
def top_k_sample(logits, k):
    indexed = sorted(enumerate(logits), key=lambda x: -x[1])
    top = indexed[:k]
    top_logits = [l for _, l in top]
    probs = softmax(top_logits)
    idx = sample_from_probs(probs)
    return top[idx][0]

def top_p_sample(logits, p):
    probs = softmax(logits)
    indexed = sorted(enumerate(probs), key=lambda x: -x[1])
    cumsum = 0
    selected = []
    for token_idx, prob in indexed:
        cumsum += prob
        selected.append((token_idx, prob))
        if cumsum >= p:
            break
    sel_probs = [pr for _, pr in selected]
    total = sum(sel_probs)
    sel_probs = [pr / total for pr in sel_probs]
    idx = sample_from_probs(sel_probs)
    return selected[idx][0]
```

### Adım 9: Reparametreleme hilesi

```python
def reparam_sample(mu, sigma):
    epsilon = random.gauss(0, 1)          # 标准正态噪声，不含可学习参数
    return mu + sigma * epsilon            # 确定性变换，梯度可流过

def reparam_gradient(mu, sigma, epsilon):
    dz_dmu = 1.0                          # z 对 mu 的梯度恒为 1
    dz_dsigma = epsilon                   # z 对 sigma 的梯度是 epsilon
    return dz_dmu, dz_dsigma
```

Değişikliklerin yeniden ölçülmüş örnekten geçerken doğrudan örnekleme yoluyla geçer olmadığını göster.

> 演示梯度 ağır parametrizasyon örneği akıyor, ancak doğrudan örnek akıyor olamaz.

### Adım 10: Gumbel-Softmax

```python
def gumbel_sample():
    u = random.random()
    return -math.log(-math.log(u))

def gumbel_softmax(logits, temperature):
    gumbels = [math.log(p) + gumbel_sample() for p in logits]
    return softmax([g / temperature for g in gumbels])
```

Düşen sıcaklığın çıkışın bir sıcaktan uzak bir vektöre nasıl yaklaştığını göster.

> 展示降低温度 如何使输出趋近一热向量──

Tüm görsellemeler ile birlikte tam uygulamalar `code/sampling.py`- Evet .

> Tüm görülebilirliklerin tam gerçekleşmesi`code/sampling.py`İçeride.

## Çerçeveyi kullanın.

> **【拓展：扩散模型中的采样工程】**
> Stable Diffusion 2022 yılından beri, örnekleme yöntemi DDPM'nin 1000 adımlı gelişmesinden DDIM、DPM-Solver++'e kadar sadece 20-50 adımlı yöntemlere ihtiyaç duyar.

NumPy ve SciPy ile üretim sürümleri:

> NumPy ve SciPy'nin üretim sürümü:

```python
import numpy as np

rng = np.random.default_rng(42)

exponential_samples = rng.exponential(scale=2.0, size=10000)
print(f"Exponential mean: {exponential_samples.mean():.4f} (expected 2.0)")

from scipy import stats
normal = stats.norm(loc=0, scale=1)
print(f"CDF at 1.96: {normal.cdf(1.96):.4f}")
print(f"Inverse CDF at 0.975: {normal.ppf(0.975):.4f}")

logits = np.array([2.0, 1.0, 0.5, 0.1, -1.0])
temperature = 0.7
scaled = logits / temperature
probs = np.exp(scaled - scaled.max()) / np.exp(scaled - scaled.max()).sum()
token = rng.choice(len(logits), p=probs)
print(f"Sampled token index: {token}")
```

MCMC'nin ölçekli olması için özel kütüphaneler kullanın:
- PyMC: NUTS (adaptif HMC) ile tam Bayesian modelleme
  完整的贝叶斯建模, NUTS kullanmak
- emcee: MCMC örneği
  集成 MCMC 采样器
- NumPyro/JAX: GPU hızlandırılmış MCMC
  GPU hızlandırma MCMC

Şimdi kütüphane aramalarının ne yaptığını biliyorsun.

> Bu yöntemleri sıfırdan inşa ettin. Şimdi kutubu fonksiyonunun ne yaptığını biliyorsun.

## Egzersizler.

1. Cauchy dağılımında ters CDF örneklemesini uygulayın. CDF F(x) = 0.5 + arctan(x) / pi. 10.000 örnek oluşturun ve histogramı gerçek PDF ile çizin. Ağır kuyruğu (ekstrem değerler merkezden uzak) dikkat edin.
   实现柯西分布(Cauchy Distribution) 逆 CDF 采样──CDF 为 F(x) = 0.5 + arctan(x) / pi──生成 10,000 个样本并绘制直方图与真实 PDF 对比──注意重尾(远离中心的极端值)。

2. Bir Beta ((2, 5) dağıtımından örnekler oluşturmak için Uniform ((0, 1) önerisi kullanın. Kabul edilen örnekleri gerçek Beta PDF ile çizin.
   Use reject sample from Beta(2, 5) 分布中生成样本,提议分布使用Uniform(0, 1)─绘制接受样本与真实Beta PDF的对比图──理论接受率是多少?

3. Sin ((x) entegralını, Monte Carlo'dan 1000, 10.000 ve 100.000 örnekle 0'dan pi'ye kadar hesaplayın. Her seviyede hata ile karşılaştırın. Hata ölçeğinin O(1/sqrt(N) olduğunu kontrol edin.
   X) 0'dan pi'ye kadar olan 积分, ayrılığı olarak 1.000、10,000 ve 100.000 个样本を用いて, △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ 

4. Metropolis-Hastings'i uygulayın, 2D dağılımından örnek almak için p ((x, y) x^2 * y^2 + x^2 + y^2 - 8*x - 8*y) / 2).
   Metropolis-Hastings'in gerçekleşmesi 2D 分布 p(x, y) ~ exp(-(x^2*y^2 + x^2 + y^2 - 8x - 8y) /2) 中采样──绘制样本和链的轨迹──尝试不同的提议标准差──

5. Tam bir metin oluşturma demo oluşturun: logitlerle 10 kelimelik bir sözlük verildiğinde, (a) açgözlülük, (b) sıcaklık = 0,7, (c) üst-k = 3, (d) üst-p = 0,9 kullanarak 20 jetonlu bir dizi oluşturun.
   构建一个完整的文本生成演示:给定 10 个词的词汇表和logits,使用 (a) 贪心、(b) temperature=0.7、((c) top-k=3、((d) top-p=0.9 生成 20 个代币的序列──比较 5 次运行的输出多样性──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sampling | "Drawing random values" | Generating values according to a probability distribution. The mechanism behind all generative AI |
| Uniform distribution | "All equally likely" | Every value in [a, b] has equal probability density 1/(b-a). The starting point for all sampling methods |
| Inverse CDF | "Probability transform" | F_inverse(U) converts a uniform sample into a sample from any distribution with known CDF. Exact and efficient |
| Rejection sampling | "Propose and accept/reject" | Generate from a simple proposal, accept with probability proportional to target/proposal ratio. Exact but wastes samples |
| Importance sampling | "Reweight samples" | Estimate expectations under p(x) using samples from q(x) by weighting each sample by p(x)/q(x). Core to PPO in RL |
| Monte Carlo | "Average random samples" | Approximate integrals as sample averages. Error O(1/sqrt(N)) regardless of dimension |
| MCMC | "Random walk that converges" | Construct a Markov chain whose stationary distribution is the target. Metropolis-Hastings is the foundational algorithm |
| Metropolis-Hastings | "Accept uphill, sometimes downhill" | Propose moves, accept based on density ratio. Detailed balance ensures convergence to target distribution |
| Gibbs sampling | "One variable at a time" | Update each variable from its conditional distribution holding others fixed. 100% acceptance rate |
| Temperature | "Confidence knob" | Divides logits by T before softmax. T<1 sharpens (more confident), T>1 flattens (more diverse) |
| Top-k sampling | "Keep the k best" | Zero out all but the k highest-probability tokens, renormalize, sample. Fixed candidate set size |
| Nucleus sampling (top-p) | "Keep the probable ones" | Keep the smallest set of tokens whose cumulative probability exceeds p. Adaptive candidate set size |
| Reparameterization trick | "Move randomness outside" | Write z = mu + sigma * epsilon where epsilon ~ N(0,1). Makes sampling differentiable. Essential for VAE training |
| Gumbel-Softmax | "Soft categorical sampling" | Differentiable approximation to categorical sampling using Gumbel noise + softmax with temperature |
| Stratified sampling | "Forced coverage" | Divide sample space into strata, sample from each. Always lower variance than naive Monte Carlo |
| Burn-in | "Warm-up period" | Initial MCMC samples discarded before the chain reaches its stationary distribution |
| Detailed balance | "Reversibility condition" | p(x) * T(x->y) = p(y) * T(y->x). Sufficient condition for p to be the stationary distribution of a Markov chain |
| Diffusion sampling | "Iterative denoising" | Generate data by starting from noise and applying learned denoising steps. Each step is a conditional sampling operation |

## Daha fazla okumak

- [Holbrook (2023): The Metropolis-Hastings Algorithm](https://arxiv.org/abs/2304.07010)- MCMC temelleri hakkında ayrıntılı dersler
- [Jang, Gu, Poole (2017): Categorical Reparameterization with Gumbel-Softmax](https://arxiv.org/abs/1611.01144)- orijinal Gumbel-Softmax kağıdı
- [Holtzman et al. (2020): The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)- çekirdek (top-p) örnekleme kağıdı
- [Kingma & Welling (2014): Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)- VAE kağıdı, reparametreleme hilesini tanıtan
- [Ho, Jain, Abbeel (2020): Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)- DDPM örneklemeyi görüntü üretimi ile bağlar
