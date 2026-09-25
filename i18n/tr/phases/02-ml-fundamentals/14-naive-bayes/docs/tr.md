# Saçma Bayes
# 朴素贝叶斯


> "Sane" varsayımı yanlış ve yine de işe yarıyor.

> "Sadece" varsayımı yanlış ama hala kullanılabilir. Bu onun güzel yanı.

**Type:** Build | **类型：** 构建
**Language:**Python .**语言：**Python
**Prerequisites:** Phase 2, Lessons 01-07 (classification, Bayes' theorem) | **前置知识：** Phase 2 第 1-7 课（分类、贝叶斯定理）
**Time:** ~75 minutes | **时间：** 约 75 分钟

## Öğrenme hedefleri

- Metin sınıflandırması için Laplace düzeltmesi ile Multinomial Naive Bayes'i sıfırdan uygulayın
  Zülalım ile Laplace düz düz düz çoklu basit bir beyeş olarak kullanılır metin sınıfları
- Neden saf bağımsızlık varsayımının matematiksel olarak yanlış olduğunu, ancak pratikte doğru sınıf sıralamasını ürettiğini açıklayın
   açıklama neden basit bağımsızlık hipotezi matematiksel olarak yanlış ama pratikte doğru sınıf sınıflandırma oluşturur
- Multinomial, Bernoulli ve Gaussian Naive Bayes varianlarını karşılaştırın ve verilen bir özellik tipi için doğru olanı seçin
  Bir çok yönlü, Bernuli ve Yüksek Basit Bayles değişkenleri, doğru değişkenlerin seçimi için özellikler belirlemiştir.
- Yüksek boyutlu nadir veriler üzerinde mantıksal gerileme karşısında Naive Bayes'i değerlendirmek ve işyerindeki önyargı-varians pazarlamasını açıklamak
  Yüksek seviye nadirlik verileri üzerinde basit Bayes'i ve mantıksal geri dönüşü değerlendirmek, ayrım-arınma tartışmalarını açıklamak


> **【中文解读】**
> 朴素贝叶斯基于贝叶斯定理 +特征独立性假设──虽然假设很强,但在文本分类中出奇地好──sklearn 中的多边性NB/GaussianNB──

> **【拓展：朴素贝叶斯在垃圾邮件过滤和情感分析中的应用】**
> İlk spam filtreleri (SpamAssassin gibi) çok sayıda basit Bayes kullanıyordu, çünkü özellikli boyutlarda yüz binlerce kelime ifade edebiliyordu. Ancak eğitim örneği az bir sahada ortaya çıktı. Apple Mail'in spam testleri bugüne kadar basit Bayes değişiklerini kullanıyor. Duygu analizinde, basit Bayes+TF-IDF klasik bir temel hattıydı, doğru doğruluk oranı %85'e kadar yükseldi.

## Sorunlar. Sorunlar.

Metinleri sınıflandırmanız gerekir. E-postaları spam veya spam olmayan olarak. Müşteri incelemeleri olumlu veya negatif olarak. Destek biletleri kategorilere. Binlerce özelliğe (her kelime için bir tane) ve sınırlı eğitim verisine sahipsiniz.

> Metinleri sıralanmak gerekir. E-postalar da çöp posta veya çöp posta olarak bölünmelidir. Müşteri yorumları da olumlu veya olumsuz olarak bölünmelidir.

Çoğu sınıflandırıcı burada boğulur. Logistik geri dönüş binlerce ağırlığı güvenilir bir şekilde tahmin etmek için yeterli örneklere ihtiyaç duyar. Karar ağaçları bir seferde bir kelime üzerine bölünür ve vahşice aşırıya çarpar. 10.000 boyutta KNN anlamsızdır çünkü her nokta diğer noktalardan eşit derecede uzakta.

> Büyük çoğunluk burada kalıyor. Düzgün bir şekilde binlerce ağırlığı tahmin etmek gerekir. Karar ağaçları her seferinde bir kelime üzerinde bölünmüş ve ciddi şekilde uyumsuz.

Naif Bayes bu işi halleder. Matematik olarak yanlış bir varsayım yapar (her bir özelliğin sınıf verilmiş diğer tüm özelliğe bağımsız olması), ve özellikle küçük eğitim setleri ile metin sınıflandırması üzerindeki "akıllı" modellerden daha üstün bir performans sergiliyor. Verileri tek bir atışla geçirir. Milyonlarca özelliklere kadar ölçeklendiriyor. Bu, olasılık tahminlerini üretir (bağımsızlık varsayımından dolayı genellikle kötü kalibre edilse de).

> 朴素贝叶斯能处理这种情况――它做了一个数学错误的假设――它产生概率估算――尽管独立假设通常校准不佳)――它只需要一次经历数据就能训练――它扩展到数百万特征――它产生概率估算 (Bunlardaki her özellik birbirinden bağımsızdır),但文本分类上仍然优于"更聪明"的模型,特别是在小训集上――它只需要一次经历数据就能训练――它扩展到数百万特征――它产生概率估算 (Bunlarlıksızlık假设通常校准不良)

Yanlış bir varsaymanın neden iyi tahminlere yol açtığını anlamak, makine öğrenimi hakkında temel bir şey öğretir: En iyi model en doğru model değil, verileriniz için en iyi önyargı-varians pazarlaması olan model.

> Yanlış varsayımların neden iyi bir öngörüş yaratabileceğini anlamak, makinelerle öğrenme alanındaki bazı temel şeyleri öğretir: En iyi model en doğru model değil, en iyi model olarak verilerinizi ölçmek için en iyi modeldir.

> **【中文解读】**
> 朴素贝叶斯'in "sadece" ifadesi, tüm özelliklerin belirli sınıflar altında birbirinden bağımsız olduğunu varsaymakta bulunur. Bu gerçekte neredeyse geçerli değildir. Ancak neden kullanılabilir? Çünkü sınıflar sadece farklı sınıfların olasılıklarını doğru bir şekilde sıralamayı gerektirir, olasılık değerinin kesin olmasını gerektirmez.

## Konsepten bir şey.

### Bayes teoremi (Hızlı inceleme)

Bayes teoremi koşullu olasılıkları tersine çevirir:

> 贝叶斯定理翻转条件概率:

```
P(class | features) = P(features | class) * P(class) / P(features)
```

İstiyoruz .`P(class | features)`- bir belgenin içindeki kelimeleri göz önüne alarak bir sınıfın birine ait olma olasılığı.
- `P(features | class)`-- bu kelimeleri bu sınıfın belgelerinde görme olasılığı
  `P(features | class)`- Bu tür dosyalarda bu kelimelerin görünüşü
- `P(class)`-- sınıfın önceki olasılığı (spam genel olarak ne kadar yaygın?)
  `P(class)`- 类别的先验概率(垃圾邮件通常有多常见?)
- `P(features)`- kanıtlar, tüm sınıflar için aynı, böylece karşılaştırırken görmezden gelebiliriz
  `P(features)`-- 证据, tüm sınıflara eşit, karşılaştırma sırasında göz ardı edilebilir

En yüksek sınıfı .`P(class | features)`- Kazandı.

> `P(class | features)`En iyi sınıf kazanmak.

### Saf Bir Bağımsızlık Farkında

Bilgisayar `P(features | class)`Bu, tüm özelliklerin ortak olasılığını tahmin etmenizi gerektirir. 10.000 kelimelik bir kelime birikimi ile, 2^10.000 olası kombinasyonların dağılımını tahmin etmeniz gerekir.

> 精确计算 `P(features | class)`需要估计所有特征的联合概率──对10,000个词表,你需要估计2^10,000种可能组合上的分布──不可能──

Saf bir varsayım: her özellik sınıfı göz önüne alındığında koşullarla bağımsızdır.

> 朴素假设:给定类别下每个特征条件独立――

```
P(w1, w2, ..., wn | class) = P(w1 | class) * P(w2 | class) * ... * P(wn | class)
```

Bir imkansız ortak dağılım yerine, n basit özellik başına dağılım tahmin ediyorsunuz.

> Siz bir imkansız birleşik dağılım tahmin etmek zorunda değilsiniz, ama basit bir özellikli dağılım tahmin etmeniz gerekir.

Bu varsayım açıkça yanlış. "makine" ve "öğrenme" kelimeleri hiçbir belgede bağımsız değildir. Ama sınıflandırıcı doğru olasılık tahminlerine ihtiyaç duymaz. Doğru sıralamalara ihtiyaç duyar. Hangi sınıfın en yüksek olasılıkları vardır. Bağımsızlık varsayımı sistematik hatalar getiriyor, ancak bu hatalar tüm sınıfları benzer şekilde etkilemektedir, bu nedenle sıralama doğru kalır.

> Bu varsayım açıkça yanlışdır. "makine" ve "öğrenme" herhangi bir dosyada bağımsız değildir. Ancak sınıflandırma doğru olasılık tahminine ihtiyaç duymaz.

### Neden Hala Çalışıyor?

Üç neden:

> Üç neden:

1. **Ranking over calibration.**Sınıflandırma sadece en yüksek sıralamalı sınıfın doğru olması gerekir. Gerçek olasılık 0.7 olduğunda P(spam) = 0.99999 olsa bile, sınıflandırıcı hala spam'i doğru seçer. Doğru olasılıklara ihtiyacımız yok. Doğru kazananı ihtiyacımız var.
   **排名优于校准。**Klasörler sadece ilk sırada sıralanmak zorunda. Doğru %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %

2. **High bias, low variance.**Bağımsızlık varsayımı güçlü bir önlemdir. Modelli ağır bir şekilde kısıtlar ve bu da aşırı uyum sağlamayı önler. sınırlı eğitim verileri ile, hafif yanlış ama istikrarlı bir model teorik olarak doğru ama çok istikrarlı bir modelden daha üstün bir modeldir. Bu, aksiyonda önyargı-varians pazarlamasıdır.
   **高偏差、低方差。**独立性假设是一个强先验――它严重约束模型,防止过拟合――有限训练数据下,一个稍微错误但稳定的模型胜过理论上正确但极不稳定的模型――这是偏差差权衡的实际运作――

3. **Feature redundancy cancels out.**İlişkili özellikler fazladan kanıt sağlar. sınıflandırıcı bu kanıtları iki kat sayır, ancak doğru sınıf için de iki kat sayır. "makine" ve "öğrenme" her zaman birlikte görünürse, her ikisi de "teknoloji" sınıfı için kanıt sağlar. NB onları iki kez sayır, ancak doğru sınıf için iki kez sayır.
   **特征冗余相互抵消。**相关特征提供冗余证据──分类重复计数这些证据,但正确类别的证据也被重复计数──如果"机器"和"学习"总是出现,两者都为"技术"类提供证据──简单贝叶斯数两次,但正确类别数两次──

Dördüncü, pratik bir neden: Naive Bayes son derece hızlıdır. Eğitim veri sayım frekansları üzerinden tek bir geçiştir. Tahmin bir matris çarpımıdır. Bir milyon belge üzerinde saniyeler içinde eğitim alabilirsiniz. Bu hız daha hızlı tekrarlayabileceğiniz, daha fazla özellik seti denemeyebileceğiniz ve daha yavaş modellere kıyasla daha fazla deney yapabileceğiniz anlamına gelir.

> Dördüncü gerçek neden: sade Bayes çok hızlıdır. Eğitim, tek kez geçen veri sayım frekansıdır. Tahmin, bir düzine çarpma. Birkaç saniye içinde milyonlarca dosya eğitimi alabilirsin. Bu hız, daha yavaş bir model kullanmaktan daha hızlı 代, daha fazla özellik toplamaya, daha fazla deney yapmaya çalışmaya yardımcı olur.

### Matematika Adım Adım

Şimdi, bir örnekle bir araya geliyoruz. Diyelim ki iki sınıfımız var: spam ve spam olmayan. Sözcüklerimiz üç kelimeye sahiptir: "bezgin", "para", "bir araya gelme".

Eğitim verileri:
- Spam e-postalarında "be bedava" 80 kez, "para" 60 kez, "bir araya gelme" 10 kez (150 kelimenin toplamı) bahsedildi.
- Spam olmayan e-postalarda "be bedava" 5 kez, "para" 10 kez, "bir araya gelme" 100 kez (115 kelimenin toplamı)
- E-postaların %40'ı spam, %60'ı spam değil.

Laplace düzeltmesi ile (alfa=1):

```
P(free | spam)    = (80 + 1) / (150 + 3) = 81/153 = 0.529
P(money | spam)   = (60 + 1) / (150 + 3) = 61/153 = 0.399
P(meeting | spam) = (10 + 1) / (150 + 3) = 11/153 = 0.072

P(free | not-spam)    = (5 + 1) / (115 + 3) = 6/118 = 0.051
P(money | not-spam)   = (10 + 1) / (115 + 3) = 11/118 = 0.093
P(meeting | not-spam) = (100 + 1) / (115 + 3) = 101/118 = 0.856
```

Yeni e-posta: "be bedava" (2 kez), "para" (1 kez), "bir toplantı" (0 kez).

```
log P(spam | email) = log(0.4) + 2*log(0.529) + 1*log(0.399) + 0*log(0.072)
                    = -0.916 + 2*(-0.637) + (-0.919) + 0
                    = -3.109

log P(not-spam | email) = log(0.6) + 2*log(0.051) + 1*log(0.093) + 0*log(0.856)
                        = -0.511 + 2*(-2.976) + (-2.375) + 0
                        = -8.838
```

Spam büyük bir farkla kazanır. "Özgür" kelimesi iki kez ortaya çıkmak spam için güçlü bir kanıtdır. "Dörüşme" görünmemesinin her iki log toplamına sıfır katkıda bulunduğunu unutmayın (0 * log(P)) - Multinomial NB'de, yok kelimelerin hiçbir etkisi yoktur.

### Üç Çeşit

Naive Bayes üç tadda gelir.`P(feature | class)`Farklı bir şekilde.

> Basitçe üç çeşit var.`P(feature | class)`Farklı bir yöntem.

#### Çoklu isimler Naif Bayes

Modeller her özelliği bir sayım olarak oluşturur. Özellikleri kelimeler sıklığı veya TF-IDF değerleri olan metin verileri için en iyisidir.

> Her bir özelliği sayı olarak oluşturmak için en uygun özelliği sözcük sıklığı veya TF-IDF değerinin metin verisi olarak oluşturmak için kullanın.

```
P(word_i | class) = (count of word_i in class + alpha) / (total words in class + alpha * vocab_size)
```

- Evet .`alpha`Bu variant metin sınıflandırması için iş atıdır.

> `alpha`Bu değişim, bir tür metin sınıfının başlıca gücüdür.

#### Gaussian Naive Bayes

Her bir özellik normal bir dağılım olarak modeller.

> Her bir özellikini doğru bir şekilde dağıtmak için en uygun özellikleri oluşturmak için.

```
P(x_i | class) = (1 / sqrt(2 * pi * var)) * exp(-(x_i - mean)^2 / (2 * var))
```

Her sınıfın özelliği ve farklılığı vardır. Bu, özellikler her sınıf içinde gerçekten bir çan eğrisini takip ettiğinde iyi çalışır.

> Her sınıfın her bir özelliğin kendi ortalama değer ve farkı vardır.

#### Bernoulli Naive Bayes

Modeller her özelliği ikili ( mevcut veya yok) olarak oluşturur. Kısa metin veya ikili özelliği vektörleri için en iyisi.

> Her bir özellikini ikinci değer olarak biçimlendirmek için, ortaya çıkmak veya ortaya çıkmamak için en uygun olan, kısa metin veya ikinci değerli özelliklerin bir parçasıdır.

```
P(word_i | class) = (docs in class containing word_i + alpha) / (total docs in class + 2 * alpha)
```

Multinomial'den farklı olarak, Bernoulli bir kelimenin yokluğuna açıkça cezalandırır. Eğer "belir" tipik olarak spam'de görünür ancak bu e-postada yoksa, Bernoulli bunu spam karşı bir kanıt olarak sayır.

> Birçok yöntemden farklı olarak, Bernuli'nin belirtilmiş cezalandırma kelimesinin ortaya çıkmaması. Eğer "özgür" genellikle çöp postalarında ortaya çıkarsa ama bu posta bulunmazsa, Bernuli bunu çöp postalarına karşı bir kanıt olarak görüyor.

### Her Bir Variantı Ne Zaman Kullanmalıyız?

| Variant | Feature Type | Best For | Example |
|---------|-------------|----------|---------|
| Multinomial | Counts or frequencies | Text classification, bag-of-words | Email spam, topic classification |
| Gaussian | Continuous values | Tabular data with normal-ish features | Iris classification, sensor data |
| Bernoulli | Binary (0/1) | Short text, binary feature vectors | SMS spam, presence/absence features |

| 变体 | 特征类型 | 最适合 | 示例 |
|------|---------|--------|------|
| Multinomial | 计数或频率 | 文本分类、词袋 | 邮件垃圾过滤、主题分类 |
| Gaussian | 连续值 | 近正态的表格数据 | 鸢尾花分类、传感器数据 |
| Bernoulli | 二值（0/1） | 短文本、二值特征向量 | 短信垃圾过滤、出现/缺失特征 |

### Laplace Düzeltme

Bir kelime test verilerinde görünse de belirli bir sınıf için eğitim verilerinde hiç görünmese ne olur?

> Eğer bir kelime test verilerinde ortaya çıkarsa, ama bir tür eğitim verilerinde hiç ortaya çıkmazsa, ne olur?

Düzeltmeden:`P(word | class) = 0/N = 0`. Tüm ürünün çarpıtıyla bir sıfır yapar `P(class | features) = 0`Tek bir görünmeyen sözcük tüm tahminleri yok eder, ne kadar başka kanıt desteklemesine rağmen.

> Çekilmez:`P(word | class) = 0/N = 0`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ `P(class | features) = 0`Diğer kanıtlar ne olursa olsun, bir sözcük tüm tahminleri yok eder.

Laplace düzeltmesi küçük bir sayıyı ekler .`alpha`(genellikle 1) her özellik sayısına:

> Her bir özellik için bir küçük hesaplama yap .`alpha`(genellikle 1):

```
P(word_i | class) = (count(word_i, class) + alpha) / (total_words_in_class + alpha * vocab_size)
```

Alpha = 1 ile her kelime en az küçük bir olasılık elde eder. Test e-postalarında görünen "discombobulate" kelimesi artık spam olasılığını öldürmez. Düzeltmenin Bayesian bir yorumuna sahiptir: kelime dağılımlarına bir benzer Dirichlet ön koymaya eşittir.

> Alpha=1 时, her kelime en az bir çok küçük olasılığı elde eder. Testing mail'de ortaya çıkan "discombobulate" artık çöpe gönderilen spam olasılığını yok etmeyi bırakır.

Daha yüksek alfa, daha güçlü bir düzeltme (daha benzer dağılımlar) anlamına gelir. Daha düşük alfa, modelin verilere daha fazla güvendiğini gösterir.

> Daha yüksek alfa daha güçlü düzlem anlamına gelir. Daha yakın ortalama dağılım. Daha düşük alfa daha fazla verilere inanmak anlamına gelir.

Alfa etkisi:

> alfa'nın etkisi:

| Alpha | Effect | When to use |
|-------|--------|-------------|
| 0.001 | Almost no smoothing, trust the data | Very large training set, no unseen features expected |
| 0.1 | Light smoothing | Large training set |
| 1.0 | Standard Laplace smoothing | Default starting point |
| 10.0 | Heavy smoothing, flattens distributions | Very small training set, many unseen features expected |

| Alpha | 效果 | 使用场景 |
|-------|------|---------|
| 0.001 | 几乎不平滑，相信数据 | 非常大的训练集，预期不会有未见特征 |
| 0.1 | 轻度平滑 | 大训练集 |
| 1.0 | 标准 Laplace 平滑 | 默认起点 |
| 10.0 | 重度平滑，拉平分布 | 非常小的训练集，预期有很多未见特征 |

### Log-Space Hesaplama

Yüzlerce olasılık (her biri 1'den daha az) çarpması, yüzen noktaların aşağı akışına neden olur. Gerçek değer çok küçük bir pozitif sayısıysa da ürün yüzen noktalarda sıfır olur.

> Yüzlerce olasılık koymak (her bir şey 1) aşama çarpması aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aşama aş

Çözüm: log alanında çalış. Muhtemelenlikleri çarpmak yerine, logaritmlerini ekleyin:

> Çözüm: sayısal alan hesaplamalarında                                                                                                                                                                                                                                                          

```
log P(class | x1, x2, ..., xn) = log P(class) + sum_i log P(xi | class)
```

Bu tahminleri nokta ürünü haline getirir:

> Bu tahmin bir nokta oluştu:

```
log_scores = X @ log_feature_probs.T + log_class_priors
prediction = argmax(log_scores)
```

Matrix çarpımı. Bu yüzden Naive Bayes tahminleri bu kadar hızlı -- tek katlı bir doğrusal modelle aynı işlemdir.

> 矩阵乘法── bu basit Bayes'in tahmininin bu kadar hızlı olmasının nedeni.

### Naif Bayes vs. Logistik Geri Dönüş

Her ikisi de metin için doğrusal sınıflandırıcılar. Fark, modellemelerindedir.

> Bu iki metin de birbiriyle bağlantılıdır.

| Aspect | Naive Bayes | Logistic Regression |
|--------|------------|-------------------|
| Type | Generative (models P(X\|Y)) | Discriminative (models P(Y\|X)) |
| Training | Count frequencies | Optimize loss function |
| Small data | Better (strong prior helps) | Worse (not enough to estimate weights) |
| Large data | Worse (wrong assumption hurts) | Better (flexible boundary) |
| Features | Assumes independence | Handles correlations |
| Speed | Single pass, very fast | Iterative optimization |
| Calibration | Poor probabilities | Better probabilities |

| 方面 | 朴素贝叶斯 | 逻辑回归 |
|------|----------|---------|
| 类型 | 生成式（建模 P(X\|Y)） | 判别式（建模 P(Y\|X)） |
| 训练 | 统计频率 | 优化损失函数 |
| 小数据 | 更好（强先验有帮助） | 更差（数据不足以估计权重） |
| 大数据 | 更差（错误假设有害） | 更好（灵活边界） |
| 特征 | 假设独立 | 能处理相关性 |
| 速度 | 单次遍历，极快 | 迭代优化 |
| 校准 | 概率校准差 | 概率校准更好 |

Basamak kural: Naive Bayes ile başlayın. Yeterince verileriniz ve NB platolarınız varsa, lojistik geri dönüşe geçin.

> 经验法则: önce basit bir şekilde kullanın. Eğer veri yeterli ise,

### Sınıflandırma boru hattı

```mermaid
flowchart LR
    A[Raw Text] --> B[Tokenize]
    B --> C[Build Vocabulary]
    C --> D[Count Word Frequencies]
    D --> E[Apply Smoothing]
    E --> F[Compute Log Probabilities]
    F --> G[Predict: argmax P class given words]

    style A fill:#f9f,stroke:#333
    style G fill:#9f9,stroke:#333
```

Bu nedenle, bu işlemler, bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha

```
log P(class | features) = log P(class) + sum_i log P(feature_i | class)
```

## Yapın.

> **【中文解读】**
> Zero uygulamasından çok sayıdaki basit bir karakter için kullanılır. Bu nedenle, çok sayıdaki karakterler, her bir kategoride her bir kelimenin ortaya çıkma sıklığı ile birlikte ortaya çıkmaktadır.

> **【拓展：朴素贝叶斯在现代 NLP 中的角色演变】**
> Transformer 模型(BERT、GPT) NLP  görevinde basit Bayes'i çok fazla aşsa da, basit Bayes'in hala bir kullanımı var:
```figure
naive-bayes
```

## Yapın

Kodun içinde .`code/naive_bayes.py`Hem MultinomialNB hem de GaussianNB'yi sıfırdan uyguluyor.

### Çoklu isimNB

Baştan başlayan uygulama:

1. **fit(X, y)**: Her sınıf için, her özelliğin sıklığını sayın. Laplace düzeltmesini ekleyin. Log olasılıklarını hesaplayın. Sınıf önceleri (sınıf frekanslarının logu)

2. **predict_log_proba(X)**: Her örnek için, hesap log P(sınıf) + tüm sınıflar için log P(kaynak_i sınıfı) toplamı. Bu bir matris çarpımı: X @ log_probs.T + log_priors.

3. **predict(X)**: En yüksek log olasılığı olan sınıfı geri gönderin.

```python
class MultinomialNB:
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        classes = np.unique(y)
        n_classes = len(classes)
        n_features = X.shape[1]

        self.classes_ = classes
        self.class_log_prior_ = np.zeros(n_classes)
        self.feature_log_prob_ = np.zeros((n_classes, n_features))

        for i, c in enumerate(classes):
            X_c = X[y == c]
            self.class_log_prior_[i] = np.log(X_c.shape[0] / X.shape[0])
            counts = X_c.sum(axis=0) + self.alpha
            self.feature_log_prob_[i] = np.log(counts / counts.sum())

        return self
```

Anahtar anlayış: uyumlandıktan sonra tahmin sadece matris çarpımı artı bir önyargı.

### GaussianNB

Sürekli özellikler için, sınıf başına ortalama ve varyasyonu bir özellik başına tahmin ediyoruz:

```python
class GaussianNB:
    def __init__(self):
        pass

    def fit(self, X, y):
        classes = np.unique(y)
        self.classes_ = classes
        self.means_ = np.zeros((len(classes), X.shape[1]))
        self.vars_ = np.zeros((len(classes), X.shape[1]))
        self.priors_ = np.zeros(len(classes))

        for i, c in enumerate(classes):
            X_c = X[y == c]
            self.means_[i] = X_c.mean(axis=0)
            self.vars_[i] = X_c.var(axis=0) + 1e-9
            self.priors_[i] = X_c.shape[0] / X.shape[0]

        return self
```

Tahmin, özellikler boyunca çarpılmış Gaussian PDF'yi kullanır (log alanında eklenir).

### Demo: Metin sınıflandırması

Kod iki sınıfı simüle eden sentetik sözcükler verisini oluşturur (teknoloji makaleleri vs. spor makaleleri). Her sınıfın farklı bir kelime frekans dağılımına sahiptir. MultinomialNB onları kelime sayılarını kullanarak sınıflandırır.

Sentetik veriler şöyle çalışır: 200 "söz" (kaynak sütunları) oluşturuyoruz. 0-39 kelimeleri teknik makalelerde yüksek frekanslı ve sporda düşük. 80-119 kelimeleri sporda yüksek frekanslı ve teknikte düşük. 40-79 kelimeleri her ikisinde orta frekanslı. Bu, bazı kelimelerin güçlü sınıf göstergeleri olduğu ve diğerlerinin gürültü olduğu gerçekçi bir senaryo yaratır.

### Demo: Sürekli Özellikler

Kod Iris benzeri verileri oluşturur (3 sınıf, 4 özellik, Gaussian kümeleri). GaussianNB sınıf başına ortalama ve varyansa kullanılarak sınıflandırır. Her sınıfın farklı bir merkezi (ortalama vektörü) ve farklı bir yayılması (varyansa) vardır. Ölçümlerin kategoriler arasında sistematik olarak farklı olduğu gerçek dünya verilerini taklit eder.

Kod ayrıca şunları gösterir:
- **Smoothing comparison:**Düzgünliğe yumuşaklık etkisini göstermek için farklı alfa değerleri ile MultinomialNB eğitimi.
- **Training size experiment:**NB'nin doğruluğu eğitim verileri 20'den 1600'e kadar arttıkça nasıl gelişiyor. NB çok az örnekle bile uygun doğruluğa ulaşır. Bu onun ana avantajıdır.
- **Confusion matrix:**Sınıf başına hassaslık, hatırlama ve F1 skorları NB'nin nerede hata yaptığını gösterir.

### Tahmin Hızı

Naive Bayes tahminleri bir matris çarpımıdır.
- MultinomialNB: bir matris çarpı (n x d) @ (d x k) = O(n * d * k)
- GaussianNB: n * k Gaussian PDF değerlendirmeleri, her biri d özellikler = O(n * d * k)

Her iki boyutda da doğrusaldır. Bunu KNN ile (bütün eğitim noktalarına uzaklık hesaplama gerektiren) veya RBF çekirdeği ile SVM ile (bütün destek vektörlerine karşı çekirdeği değerlendirme gerektiren) karşılaştırın. NB, tahmin zamanında büyüklük sıralamaları ile daha hızlıdır.

## Çerçeveyi kullanın.

sklearn ile, her iki varians da tek satırlı:

```python
from sklearn.naive_bayes import GaussianNB, MultinomialNB

gnb = GaussianNB()
gnb.fit(X_train, y_train)
print(f"GaussianNB accuracy: {gnb.score(X_test, y_test):.3f}")

mnb = MultinomialNB(alpha=1.0)
mnb.fit(X_train_counts, y_train)
print(f"MultinomialNB accuracy: {mnb.score(X_test_counts, y_test):.3f}")
```

Sklüarn ile metin sınıflandırması için:

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

text_clf = Pipeline([
    ("vectorizer", CountVectorizer()),
    ("classifier", MultinomialNB(alpha=1.0)),
])

text_clf.fit(train_texts, train_labels)
accuracy = text_clf.score(test_texts, test_labels)
```

Kodun içinde .`naive_bayes.py`Düzgünlüğü kontrol etmek için aynı verilere göre sıfırdan uygulanmaları sklearn ile karşılaştırır.

### TF-IDF, Naive Bayes ile

Çiğ kelimeler sayımı her kelimeyi olay başına eşit ağırlık verir. Ama "i" ve "i" gibi yaygın kelimeler her sınıfta sıkça görünür - hiçbir bilgi taşımıyorlar. TF-IDF (Term Frequency - Inverse Document Frequency) yaygın kelimeleri ağırlık altına alır ve nadir, ayrımcı kelimeleri ağırlık altına alır.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

text_clf = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB(alpha=0.1)),
])
```

TF-IDF değerleri negatif değildir, bu nedenle MultinomialNB ile çalışır. TF-IDF + MultinomialNB kombinasyonu metin sınıflandırması için en güçlü temel çizgilerden biridir.

### BernoulliNB kısa metin için

Kısa metinler için (tweetler, SMS, sohbet mesajları), BernoulliNB MultinomialNB'yi üstlenebilir. Kısa metinler düşük kelime sayısına sahiptir, bu nedenle MultinomialNB'nin güvendiği frekans bilgileri gürültülüdür. BernoulliNB sadece varlık veya yoklukla ilgilenir, bu da kısa metinle daha güvenilirdir.

```python
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer

text_clf = Pipeline([
    ("vectorizer", CountVectorizer(binary=True)),
    ("classifier", BernoulliNB(alpha=1.0)),
])
```

- Evet .`binary=True`CountVectorizer'deki bayrak tüm sayıları 0/1'ye dönüştürür.

### Kalibrasyon NB Muhtemelenlikler

NB olasılıkları kötü kalibrlenmiştir. NB'de P(spam) = 0.95 olduğu zaman, gerçek olasılık 0.7 olabilir.

```python
from sklearn.calibration import CalibratedClassifierCV

calibrated_nb = CalibratedClassifierCV(MultinomialNB(), cv=5, method="sigmoid")
calibrated_nb.fit(X_train, y_train)
proba = calibrated_nb.predict_proba(X_test)
```

Bu, NB'nin çiğ puanlarının üstündeki bir lojistik geri dönüşe karşılık gelir.

### Ortak Gotchas

1. **Negative feature values.**MultinomialNB negatif olmayan özellikleri gerektirir. Negatif değerleriniz varsa (bazı ayarlarla veya standart özelliklerle TF-IDF gibi), GaussianNB'yi kullanın veya özellikleri pozitif olarak değiştirin.

2. **Zero variance features.**GaussianNB, bir sınıf için sıfır bir değişikliğe sahipse (tüm değerler aynıdır), olasılık hesaplaması bozulur.

3. **Class imbalance.**Eğer e-postaların %99'u spam değilse, önceki P(not-spam) = 0.99 o kadar güçlüdür ki olasılık kanıtlarını aşıyor.

4. **Feature scaling.**MultinomialNB'nin ölçeklendirmeye ihtiyacı yoktur (sayılar üzerinde çalışır). GaussianNB'nin de ölçeklendirmeye ihtiyacı yoktur (sözümlü özellik istatistiklerini tahmin eder). Bu, özellik ölçeklerine duyarlı olan lojistik gerileme ve SVM'ye göre bir avantaj.

## İndirin . Ürünler .

Bu ders şunları ortaya çıkarır:
- `outputs/skill-naive-bayes-chooser.md`-- doğru NB varianti seçmek için karar verme becerisi
- `code/naive_bayes.py`-- MultinomialNB ve GaussianNB sıfırdan, sklearn karşılaştırması ile

### Naif Bayes Başarısız olduğunda

NB bağımsızlık varsayımının yanlış sıralamalara neden olduğu (sadece yanlış olasılıklar değil) durumlarda başarısız olur.

1. **Strong feature interactions.**Eğer sınıf iki özelliğin birleşmesine bağlıysa ancak tek başına (XOR benzeri desenler) değilse, NB onu tamamen kaçırır.

2. **Highly correlated features with opposing evidence.**Eğer A özelliği "spam" ve B özelliği "spam değil" diyor, ancak A ve B mükemmel bir şekilde ilişkili (gerçekte her zaman aynı fikirde) ise, NB hiçbir kanıt olmadığı yerde çelişkili kanıt görür.

3. **Very large training sets.**Yeterince veri ile, lojistik gerileme gibi ayrımcılık modelleri gerçek karar sınırını öğrenir ve NB'yi aşırır. Küçük verilerle yardımcı olan bağımsızlık varsayımı artık modeli geri tutuyor.

Bu tür hata modları metin sınıflandırması için nadirdir. Metin özellikleri sayısızdır, bireysel olarak zayıfdır ve bağımsızlık varsayımının hataları iptal edilme eğilimindedir.

## Egzersizler.

1. **Smoothing experiment.**MultinomialNB'yi 0.01, 0.1, 1.0, 10.0 ve 100.0 alfa değerleri olan metin verilerine çalıştır.
   1. **平滑实验。**Alfa değerinin 0.01 、0.1 、1.0 、10.0 、100.0 ile birlikte, çok sayıda değerli bir verinin üzerinde çalışmak.

2. **Feature independence test.**Gerçek bir metin veri kümesi alın. Açıkça ilişkili olan iki kelimeyi seçin ("makine" ve "öğrenme"). P  word1  class * P  word2  class) hesaplayın ve P  word1 AND word2  class ile karşılaştırın. Bağımsızlık varsayımı ne kadar yanlış?
   2. **特征独立性测试。**取一个真文本数据集. 取两个明显相关的词 (如机器和学习) 计算 P                                                                                                                                                                                                                                                  

3. **Bernoulli implementation.**BernoulliNB sınıfıyla kodu genişlet. Sözcük çantalarını ikili ( mevcut/ yok) olarak dönüştürün ve metin verilerindeki MultinomialNB ile doğruluğu karşılaştırın. Bernoulli ne zaman kazanır?
   3. **伯努利实现。**扩展代码添加 BernoulliNB 类──将词袋转为二值(存在/不存在)并与多数式NB 在文本数据上比较准确率──伯努利何时赢?

4. **NB vs Logistic Regression.**Her ikisini de metin verileri üzerine eğit. 100 eğitim örneği ile başlayın ve 10.000'e yükseltsin. Her ikisinin de plan doğruluğu vs. eğitim setinin boyutu. Logistik Geri dönüş hangi noktada Naive Bayes'i geçiyor?
   4. **NB vs 逻辑回归。**Metin verilerinde eğitim ikili. 100 eğitim örneğinden 10.000'e yükselmeye başladı.

5. **Spam filter.**Tam bir spam sınıflandırıcısı oluşturun: çiğ e-posta metnini işaretleyin, kelime birikimi oluşturun, sözcük çanta özellikleri oluşturun, MultinomialNB'yi eğitiniz, doğru bir şekilde değerlendirin ve geri çağırın (sadece doğruluk değil - neden?).
   5. **垃圾邮件过滤器。**构建完整的垃圾邮件分类器:分词原始邮件文本、构建词汇表、创建词袋特征、训练 多数号NB、精确率和召回率评估──

> **【中文解读】**
> 朴素贝叶斯的三种变体:(1) 多项式朴素贝叶斯(MultinomialNB) 适用于词频/TF-IDF特征文本分类;(2) 伯努利朴素贝叶斯(BernoulliNB) 适用于二值特征(词是否出现);(3) 高斯朴素贝叶斯(GaussianNB) 适用于连续特征,假设每类内特征服从正态分布;;Laplace 平滑加

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Naive Bayes | "Simple probabilistic classifier" | A classifier that applies Bayes' theorem with the assumption that features are conditionally independent given the class |
| Conditional independence | "Features don't affect each other" | P(A, B \| C) = P(A \| C) * P(B \| C) -- knowing B tells you nothing new about A once you know C |
| Laplace smoothing | "Add-one smoothing" | Adding a small count to every feature to prevent zero probabilities from dominating the prediction |
| Prior | "What you believed before seeing data" | P(class) -- the probability of each class before observing any features |
| Likelihood | "How well the data fits" | P(features \| class) -- the probability of observing these features if the class is known |
| Posterior | "What you believe after seeing data" | P(class \| features) -- the updated probability of the class after observing the features |
| Generative model | "Models how data is generated" | A model that learns P(X \| Y) and P(Y), then uses Bayes' theorem to get P(Y \| X) |
| Discriminative model | "Models the decision boundary" | A model that directly learns P(Y \| X) without modeling how X is generated |
| Log probability | "Avoid underflow" | Working with log P instead of P to prevent the product of many small numbers from becoming zero in floating point |

## Daha fazla okumak

- [scikit-learn Naive Bayes docs](https://scikit-learn.org/stable/modules/naive_bayes.html)- Matematik detaylarla birlikte üç farklılık
  [scikit-learn 朴素贝叶斯文档](https://scikit-learn.org/stable/modules/naive_bayes.html)- Üç çeşit değişim ve matematik ayrıntıları
- [McCallum and Nigam, A Comparison of Event Models for Naive Bayes Text Classification (1998)](https://www.cs.cmu.edu/~knigam/papers/multinomial-aaaiws98.pdf)-- metin için Multinomial vs Bernoulli'nin klasik karşılaştırması
  [McCallum and Nigam (1998)](https://www.cs.cmu.edu/~knigam/papers/multinomial-aaaiws98.pdf)- Çokluk vs 伯努利文本分类的经典比较
- [Rennie et al., Tackling the Poor Assumptions of Naive Bayes Text Classifiers (2003)](https://people.csail.mit.edu/jrennie/papers/icml03-nb.pdf)-- metin için NB'de gelişmeler
  [Ng and Jordan (2001)](https://ai.stanford.edu/~ang/papers/nips01-discriminativegenerative.pdf)- 证明 NB 在少数据时收快于 LR
- [Ng and Jordan, On Discriminative vs. Generative Classifiers (2001)](https://ai.stanford.edu/~ang/papers/nips01-discriminativegenerative.pdf)-- daha az veri ile NB'nin LR'den daha hızlı bir şekilde yakınlaştığını kanıtlar
