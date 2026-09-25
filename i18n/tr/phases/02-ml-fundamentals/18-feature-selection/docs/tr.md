# Özellik Seçimi
# Özellik Seçim


> Daha fazla özellik daha iyi değil, doğru özellikler daha iyidir.

> Özellikleri daha fazla değil.

**Type:** Build | **类型：** 构建
**Language:**Python .**语言：**Python
**Prerequisites:** Phase 2, Lessons 01-09, 08 (feature engineering) | **前置知识：** Phase 2 第 1-9 课、第 8 课（特征工程）
**Time:** ~75 minutes | **时间：** 约 75 分钟

## Öğrenme hedefleri

- Filtrleme yöntemlerini (varians eşiği, karşılıklı bilgi, chi-square) ve sarma yöntemlerini (RFE, ileriye seçme) sıfırdan uygulamak
  Bu, bir diğerinden daha fazla bilgi ve bilgi vermenin en iyi yolu.
- Karşılıklı bilgi neden bağlantıların eksik olduğu çizgisiz özellik-hedef ilişkileri yakalar?
   Neden birbirine ait bilgiler bağlantılılık ve yanlışlıkların bağlantılılığı ele alabilir 
- L1 düzenlenmesini (kişili seçimi) RFE ile (kalip seçimi) karşılaştırın ve hesaplama işlemleri karşılaştırın
  L1 正则化 (嵌入选择) ile RFE (包装选择) karşılaştırın, değerlendirme
- Çoklu yöntemleri birleştiren ve tutulan veriler üzerinde daha iyi genelleştirmeyi gösteren bir özellik seçimi boru hattı oluşturun
  Köşelmiş veriler üzerinde genel gelişmeler göstermek için çeşitli yöntemlerin özelliklerini seçme hattını oluşturmak


> **【中文解读】**
> Özellik Seçim, birçok özellikten en yararlı alt kümeleri seçmek için geçerlidir. Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özet

> **【拓展：特征选择在工业界的重要性】**
> Finansal rüzgar kontrol modelinde, düzenleme gereksinimleri modeli açıklanabilir ve her bir özelliğin neden seçildiğini açıklayabilmelidir. L1 düzenli düzenlenmesi (Lasso) otomatik olarak önemli olmayan özelliklerin ağırlığı sıfıra doğru sıkıştırılır. Aynı zamanda özellik seçimi ve model eğitimi gerçekleştirir.

## Sorunlar. Sorunlar.

500 özellikiniz var. Modeliniz yavaş yavaş tren alır, sürekli aşırı yüklenir ve kimse ne öğrendiklerini açıklayamaz. Performansı artırmak için daha fazla özellik eklersiniz.

> 500 özellik var. Modelle eğitim yavaş, sürekli, kimseyi anlatamaz.

Bu, eylemdeki boyutlulığın lanetidir. Özelliklerin sayısı arttıkça, özellik alanının hacmi patlar. Veri noktaları nadir hale gelir. Noktalar arasındaki mesafeler birleşti. Modelle gerçek kalıpları bulmak için eksponansiel olarak daha fazla veri gerekmektedir. Ses özellikleri sinyal özelliklerini boğar. Aşırı uyum öntanımlı hale gelir.

> Bu, boyut lanetinin gerçek işlevi. Özellik sayısı artışıyla birlikte, özellikler alanının büyüklüğü patlaması. Verim noktaları arasındaki mesafe giderek daha nadir hale geliyor.

Özellik seçimi, karşı ilacın bir parçasıdır. Gürültüyü ortadan kaldırın. Boşluğu ortadan kaldırın. Hedef hakkında gerçek bilgi taşıyan özellikleri koruyun. Sonuç: daha hızlı eğitim, daha iyi genelleştirme ve aslında açıklayabileceğiniz modeller.

> Özellik Seçim, bir çözümdür. Ses çıkarır. Boşluğu çıkarır. Gerçek hedef mesajı taşıyan özellikleri korur. Sonuç: Daha hızlı eğitim, daha iyi genelleşme ve gerçekten açıklayabileceğiniz modeller.

Amaç tüm mevcut bilgileri kullanmak değil, doğru bilgileri kullanmaktır.

> Amaç, tüm kullanılabilir bilgileri kullanmak değil, doğru bilgileri kullanmak.

> **【中文解读】**
> Özellik seçimi üç büyük yöntemin avantajları vardır: 过法 (farklılık 价值, karşılıklı bilgi, karşılıklı inceleme) en hızlı fakat özellikler arasındaki etkileşimi ihmal etme; paketleme yöntemleri (backlinking method)   dönüşümlü özellikler ortadan kaldırma RFE                                                                                                                                                                                                                                                                                                                                                                                                                                                         

## Konsepten bir şey.

### Özellik Seçimi Üç Kategoriyası

Her özellik seçimi yöntemi üç kategoriden birine ayrılır:

> Her özellik seçimi yönteminin aşağıdaki üç sınıfdan biri vardır:

```mermaid
flowchart TD
    A[Feature Selection Methods] --> B[Filter Methods]
    A --> C[Wrapper Methods]
    A --> D[Embedded Methods]

    B --> B1["Variance Threshold"]
    B --> B2["Mutual Information"]
    B --> B3["Chi-squared Test"]
    B --> B4["Correlation Filtering"]

    C --> C1["Recursive Feature Elimination"]
    C --> C2["Forward Selection"]
    C --> C3["Backward Elimination"]

    D --> D1["L1 / Lasso Regularization"]
    D --> D2["Tree-based Importance"]
    D --> D3["Elastic Net"]
```

**Filter methods**Bu, bir model kullanmamak için, bir özellik etkileşimini kaçırmak için.

> **过滤法**İstifadeden bağımsız olarak her özellik değerlendirmesi.

**Wrapper methods**Bu, bir modelin özellik alt kümelerini değerlendirmesi için eğitilmesini sağlar.

> **包装法**訓練模型, özellikleri değerlendirmek için 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練模型, 訓練

**Embedded methods**L1 düzenlenmesi ağırlıkları sıfıra çıkarır. karar ağaçları en yararlı özelliklere ayrılır. Seçim ayrı bir adım olarak değil, montaj sırasında gerçekleşir.

> **嵌入法**Model eğitim sürecinde özellik seçimi. L1 Düzenlenme, ağırlık yönlendirmesi olarak sıfırlanır.

### Değişiklik Eğitimi

Bir özellik örnekler arasında az değişirse, neredeyse hiçbir bilgi taşımıyor.

> En basit filtresi. Eğer bir özellik örnekler arasında neredeyse değişmezse, neredeyse bilgi taşımıyor.

1000 örnekten 999'un 0.0 oranında bir özelliği düşünün.

> 考虑一个1000 样本中999 值为0.0 的特征――它的方差接近零――没有模型能用它来区分类――移除它――

```
variance(x) = mean((x - mean(x))^2)
```

Bir eşiği (örneğin, 0.01) belirleyin. Onun altında varyansiyesi olan her özelliği bırakın. Bu, hedef değişkenine bakmadan sabit veya neredeyse sabit özellikleri çıkarır.

>  değerini ayarlayın.  değerini ayarlayın.  değerini kaldırmak için  değerini kaldırmak için  değerini kaldırmak için  değerini kaldırmak için  değerini kaldırın.                                                                                                                                                                                                                                       

Ne zaman kullanılır: diğer yöntemlerden önce bir önceden işleme adımı olarak.

> Hangi zaman kullanılır: Diğer yöntemlerden önce yapılan bir pre-processing step olarak, sıfır maliyetlere yakın bir şekilde kullanılmaz özellikler elde edilir.

Sınırlama: bir özellik yüksek bir değişikliğe sahip olabilir ve yine de saf bir gürültü olabilir.

>                                                                                                                                                                                                                                                               

### Karşılıklı Bilgi

Karşılıklı bilgi, X özelliğinin değerini bilmek ile Y hedefi hakkında belirsizliklerin ne kadar azaldığını ölçer.

> 互信息衡知道特征 X'in değeri, Y'nin belirsizliğine karşı belirsizliği ne ölçüde azaltabilir.

```
I(X; Y) = sum_x sum_y p(x, y) * log(p(x, y) / (p(x) * p(y)))
```

Eğer X ve Y bağımsız ise, p(x, y) = p(x) * p(y), yani log terimi sıfır ve I(X; Y) = 0. X size Y hakkında ne kadar çok şey söylerse, karşılıklı bilgi o kadar yüksek olur.

> Eğer X 和 Y 独立,p(x,y) = p(x) * p(y), bu nedenle sayısal konularda 0,I(X;Y) = 0──X 告诉你关于Y 的信息越多,互信息越高──

Bir özelliğin hedefe sıfır bir korelasyonu olabilir, ancak ilişki kare veya periyodik olduğu için yüksek karşılıklı bilgi olabilir.

> Bağlantılılık ile ilgili önemli avantajlar: İlişki ile ilgili bilgiyi kavramak, bağlantılı olmayan ilişkileri oluşturur.

Sürekli özellikler için önce kutulara ayırt edin (istogram tabanlı tahmin). kutuların sayısı tahmine etkiler - çok az kutu bilgiyi kaybeder, çok fazla kutu gürültü ekler.

> ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒    ⇒ ⇒   ⇒                                                                                                                                                 

```mermaid
flowchart LR
    A[Feature X] --> B[Discretize into Bins]
    B --> C["Compute Joint Distribution p(x,y)"]
    C --> D["Compute MI = sum p(x,y) * log(p(x,y) / p(x)p(y))"]
    D --> E["Rank Features by MI Score"]
    E --> F[Select Top K]
```

### Tekrarlı Özelliklerin Yok edilmesi (RFE)

RFE bir sarma yöntemidir. Bir modelin kendi özellik önemi ile tekrar tekrar kesim yapar:

> RFE bir paketleme yöntemidir. Modelin kendi özelliklerini kullanır.

1. Tüm özelliklerle model eğit
   Tüm özellikleri kullanın.
2. Önemliliklere göre sıralama özellikleri (lineer modeller için katılıklar, ağaçlar için kirlilik azaltımı)
   按重要性排列特征 (→ 线性模型用系数,树模型用不纯度减少)
3. En az önemli özelliği kaldırın
   移除最不重要特征
4. İstediğiniz özellik sayısı kalana kadar tekrarlayın
   重复 Geri kalan özellik sayısı

```mermaid
flowchart TD
    A["Start: All N Features"] --> B["Train Model"]
    B --> C["Rank Feature Importances"]
    C --> D["Remove Least Important"]
    D --> E{"Features == Target Count?"}
    E -->|No| B
    E -->|Yes| F["Return Selected Features"]
```

RFE, özellik etkileşimlerini göz önünde bulundurur çünkü model kalan tüm özellikleri bir araya getirir. Bir özellikten çıkarılması diğerlerinin önemini değiştirir. Bu, filtre yöntemlerinden daha kapsamlı hale getirir.

> RFE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

Masraf: model N - hedef zamanları eğitirsiniz. 500 özellik ve 10 hedef ile, yani 490 eğitim koşusu. Pahalı modeller için bu yavaş. Adım başına birden fazla özellik çıkararak hızlandırabilirsiniz (örneğin, her turda alt 10% çıkarın).

> 代价:You need to train model N - 目标 次数──500 个特征和目标 10 个,就是 490 个训练── 代价:You need to train model N - 目标 次数── 500 个特征和目标 10 个,就是 490 个训练── 代价:You need to train model N - 目标 次数── 目标 个特征和目标 10 个,就是 490 个训练── 代价:You need to train model N - 目标 次数── 目标 个特征和目标 10 个,就是 490 个训练── 代价:You need to train model N - 目标 次数── 500 个特征和目标 10 个特征和目标 10 个特征,就是 490 个次训练── 代价: 代价: 慢慢.

### L1 (Lasso) Düzenleme

L1 düzenlenmesi, kayıp fonksiyonuna ağırlıkların mutlak değerini ekler:

```
loss = prediction_error + alpha * sum(|w_i|)
```

Alfa parametri, özelliklerin ne kadar agresif olarak kesildiğini kontrol eder.

> Alfa parametr kontrol özellikleri kesilen dalların hızlandırılması derecesi. Daha yüksek alfa, daha fazla ağırlık değişimi anlamına gelir.

L1 cezası, ağırlık alanında elmas şeklinde bir kısıtlama bölgesini oluşturur. Optimal çözüm, bu elmasın bir veya daha fazla ağırlığın sıfır olduğu bir köşede yerleşebilir. L2 düzenlenmesi (kaş) ağırlıkların küçülmesi ancak nadiren sıfıra ulaşması için bir döngü kısıtlama oluşturur.

> Neden tam olarak sıfır?L1  ceza 形束区域を創造する形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束区域に形束を形成する形束を形成する形束を形成する形束を形成する形束を形成する形束を形成する形束を形成する形束を形成する形束を形成する形束を形成する形束を形成する形束を形成する形束を形成する形束を形成する形束を形成する形の形を形成する形の形を形成する形を形成する形の形を形成する形の形を形成する形を形成する形の形を形成する形の形を形成する形の形の形を形成する形を形成する形を形成する形の形の形を形成する形の形の形に形を形成する形の形を形成する形の形の形に形を形成する形の形を形成する形の形に形に形の形の形の形に形の形を形に形する形する形の形の形に形の形の形に形の形の形に形の形に形を形する形に形する形の形の形の形に形の形に形の形に形の形に形に形する形の形の形に形に形する形の形に形の形に形に形を形する形する形に形に形する形の形の形に形に

Bu, yerleşik özellik seçimi: model eğitim sırasında hangi özellikleri görmezden gelmeyi öğrenir.

> Bu, yerleştirilmiş özellik seçimi: model eğitim sürecinde hangi özellikleri göz ardı etmeyi öğrenir.

Avantajlar: tek eğitim çalışması, ilişkili özellikleri ele alır (birini ve diğerlerini sıfırlar), çoğu doğrusal model uygulamasına yerleştirilmiştir.

> 优势:单次训练运行,处理相关特征(选择一个并将其他置零),内置在大多数线性模型实现中──

Sınırlama: Sadece doğrusal modeller için çalışır.

>  sınırlılık: sadece 線性モデルに適用します. 線性でない特性を重要性を把握できない.

### Ağaç Temelindeki Özelliklerin Önemi

Karar ağaçları ve onların ansamblları (hassasi ormanlar, gradient artışı) doğal olarak özellikleri sıralar. Her bölünme kirliliği azaltır (sınıflama için Gini veya entropy, geri dönüş için varians).

> 决策树及其集成 (随机森林、梯度升升) 自然地对特征排名──每次分分减少不纯度──分类用基尼或,归归用方差)──产生更大不纯度减少的特征更重要──

T ağaçları olan rastgele bir orman için:

```
importance(feature_j) = (1/T) * sum over all trees of
    sum over all nodes splitting on feature_j of
        (n_samples * impurity_decrease)
```

Bu, her özellik için normallaştırılmış bir önem puanı verir.

> Bu, her bir özelliğin birleştirilmesinin öneminin birincil değerini verir.

Dikkat: ağaç tabanlı önem birçok benzersiz değer (yüksek kardinallık) olan özelliklere karşı tarafsızdır.

> Dikkat: Şekil modelinin önemi çok sayıda benzersiz değerli özelliklere sahip olan bir eğilime sahiptir.

### Permutasyon Önemliliği

Model-agnostik bir yöntem:

> Modelle ilgili olmayan bir yöntem:

1. Model eğitimi ve doğrulama verileriyle başlangıç performansını kaydetmek
   訓練模型并记录验证数据 üzerinde temel çizgi performansı
2. Her özellik için: değerlerini rastgele karıştırın, performans düşüşünü ölçün
   Her özellik için: Asasansörde değer, ölçüm performansı düşüyor
3. Düşüş ne kadar büyükse, özellik o kadar önemli olur.
   Aşağıya düşen, özellikleri önemli olan

Bir özelliği karıştırmak performansına zarar vermezse, model buna bağlı değildir.

> Eğer bir özellik bozulursa, model buna bağlı değildir.

Permutasyon önemi ağaç tabanlı önemi kardinallik önyargısını önler. Ama yavaş: her özellik için bir tam değerlendirme, istikrar için çok kez tekrarlanır.

> 置換的重要性, ağaç modelinin öneminin temel sayısal kayıplarını önlemektedir.

### Karşılaştırma Tablosu

| Method | Type | Speed | Nonlinear | Feature Interactions |
|--------|------|-------|-----------|---------------------|
| Variance threshold | Filter | Very fast | No | No |
| Mutual information | Filter | Fast | Yes | No |
| Correlation filter | Filter | Fast | No | No |
| RFE | Wrapper | Slow | Depends on model | Yes |
| L1 / Lasso | Embedded | Fast | No (linear) | No |
| Tree importance | Embedded | Medium | Yes | Yes |
| Permutation importance | Model-agnostic | Slow | Yes | Yes |

### Karar Akış Çizelgesi

```mermaid
flowchart TD
    A[Start: Feature Selection] --> B{How many features?}
    B -->|"< 50"| C["Start with variance threshold + mutual information"]
    B -->|"50-500"| D["Variance threshold, then L1 or tree importance"]
    B -->|"> 500"| E["Variance threshold, then mutual info filter, then RFE on survivors"]

    C --> F{Using linear model?}
    D --> F
    E --> F

    F -->|Yes| G["L1 regularization for final selection"]
    F -->|No - trees| H["Tree importance + permutation importance"]
    F -->|No - other| I["RFE with your model"]

    G --> J[Validate: compare selected vs all features]
    H --> J
    I --> J

    J --> K{Performance improved?}
    K -->|Yes| L["Ship with selected features"]
    K -->|No| M["Try different method or keep all features"]
```

## Yapın.

> **【中文解读】**
> Zıfadan gerçekleştirilen üç tip özellik seçme yöntemleri: 过法(方差值、互信息、卡方检查独立评估每个特征) 包装法(递归特征消除 RFE反复训练模型消除最不重要特征) 嵌入法(L1 正规化 Lasso训练时自动将不重要特征权重压缩为零) ⋅通过合成数据(已知哪些特征有用) 验证各方法的效果──

> **【拓展：特征选择在 LLM 时代的新意义】**
> ️Devide learning号称" otomatik öğrenme özellikleri", ancak özellik seçimi aşağıdaki durumlarda hala önemli: 1) 表格数据特征选择可提高 XGBoost/LightGBM'in performans ve eğitim hızı; 2) açıklanabilir gereksinimTapis ve finans alanlarında hangi özelliklerin kullanıldığını açıklamak gerekir; 3) 嵌入空间Tranformer bile 维度上做"特征选择" (Devide feature selection) ️Devide attention mechanism is a dynamic feature selection) ️OpenAI's GPT-4 技术报告提到, training time used data selection strategy based on importance.
```figure
f3-feature-prune
```

## Yapın

### Adım 1: Bilinen özellik yapısı ile sentetik verileri oluşturun

```python
import numpy as np


def make_feature_selection_data(n_samples=500, seed=42):
    rng = np.random.RandomState(seed)

    x1 = rng.randn(n_samples)
    x2 = rng.randn(n_samples)
    x3 = rng.randn(n_samples)
    x4 = x1 + 0.1 * rng.randn(n_samples)
    x5 = x2 + 0.1 * rng.randn(n_samples)

    informative = np.column_stack([x1, x2, x3, x4, x5])

    correlated = np.column_stack([
        x1 * 0.9 + 0.1 * rng.randn(n_samples),
        x2 * 0.8 + 0.2 * rng.randn(n_samples),
        x3 * 0.7 + 0.3 * rng.randn(n_samples),
        x1 * 0.5 + x2 * 0.5 + 0.1 * rng.randn(n_samples),
        x2 * 0.6 + x3 * 0.4 + 0.1 * rng.randn(n_samples),
    ])

    noise = rng.randn(n_samples, 10) * 0.5

    X = np.hstack([informative, correlated, noise])
    y = (2 * x1 - 1.5 * x2 + x3 + 0.5 * rng.randn(n_samples) > 0).astype(int)

    feature_names = (
        [f"info_{i}" for i in range(5)]
        + [f"corr_{i}" for i in range(5)]
        + [f"noise_{i}" for i in range(10)]
    )

    return X, y, feature_names
```

Temel gerçeği biliyoruz: 0-4 özellikleri bilgilendirici (daha 3 ve 4 0 ve 1'nin ilişkili kopyalarıdır), 5-9 özellikleri bilgilendirici özelliklerle ilişkili, 10-19 özellikleri saf gürültüdür. İyi bir seçim yöntemi 0-4 en yüksek ve 10-19 en düşük sırada yer almalıdır.

> Gerçek durum: 0-4 özellikleri bilgilidir (kaçak 3 ve 4 0 ve 1 ile ilgili kopyası), 5-9 özellikleri bilgi ile ilgili, 10-19 özellikleri saf gürültüdür. İyi seçim yöntemleri 0-4 排最高,10-19 排最低 olmalıdır.

### Adım 2: Değişiklik eşiği

```python
def variance_threshold(X, threshold=0.01):
    variances = np.var(X, axis=0)
    mask = variances > threshold
    return mask, variances
```

### Adım 3: Karşılıklı bilgi (diskret)

```python
def discretize(x, n_bins=10):
    min_val, max_val = x.min(), x.max()
    if max_val == min_val:
        return np.zeros_like(x, dtype=int)
    bin_edges = np.linspace(min_val, max_val, n_bins + 1)
    binned = np.digitize(x, bin_edges[1:-1])
    return binned


def mutual_information(X, y, n_bins=10):
    n_samples, n_features = X.shape
    mi_scores = np.zeros(n_features)

    y_vals, y_counts = np.unique(y, return_counts=True)
    p_y = y_counts / n_samples

    for f in range(n_features):
        x_binned = discretize(X[:, f], n_bins)
        x_vals, x_counts = np.unique(x_binned, return_counts=True)
        p_x = dict(zip(x_vals, x_counts / n_samples))

        mi = 0.0
        for xv in x_vals:
            for yi, yv in enumerate(y_vals):
                joint_mask = (x_binned == xv) & (y == yv)
                p_xy = np.sum(joint_mask) / n_samples
                if p_xy > 0:
                    mi += p_xy * np.log(p_xy / (p_x[xv] * p_y[yi]))
        mi_scores[f] = mi

    return mi_scores
```

### 4. Adım: Tekrarlı Özelliklerin Yok edilmesi

```python
def simple_logistic_importance(X, y, lr=0.1, epochs=100):
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    b = 0.0

    for _ in range(epochs):
        z = X @ w + b
        pred = 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
        error = pred - y
        w -= lr * (X.T @ error) / n_samples
        b -= lr * np.mean(error)

    return w, b


def rfe(X, y, n_features_to_select=5, lr=0.1, epochs=100):
    n_total = X.shape[1]
    remaining = list(range(n_total))
    rankings = np.ones(n_total, dtype=int)
    rank = n_total

    while len(remaining) > n_features_to_select:
        X_subset = X[:, remaining]
        w, _ = simple_logistic_importance(X_subset, y, lr, epochs)
        importances = np.abs(w)

        least_idx = np.argmin(importances)
        original_idx = remaining[least_idx]
        rankings[original_idx] = rank
        rank -= 1
        remaining.pop(least_idx)

    for idx in remaining:
        rankings[idx] = 1

    selected_mask = rankings == 1
    return selected_mask, rankings
```

### Adım 5: L1 özellik seçimi

```python
def soft_threshold(w, alpha):
    return np.sign(w) * np.maximum(np.abs(w) - alpha, 0)


def l1_feature_selection(X, y, alpha=0.1, lr=0.01, epochs=500):
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    b = 0.0

    for _ in range(epochs):
        z = X @ w + b
        pred = 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
        error = pred - y

        gradient_w = (X.T @ error) / n_samples
        gradient_b = np.mean(error)

        w -= lr * gradient_w
        w = soft_threshold(w, lr * alpha)
        b -= lr * gradient_b

    selected_mask = np.abs(w) > 1e-6
    return selected_mask, w
```

### Adım 6: Ağaç temelli önem (sadece karar ağacı)

```python
def gini_impurity(y):
    if len(y) == 0:
        return 0.0
    classes, counts = np.unique(y, return_counts=True)
    probs = counts / len(y)
    return 1.0 - np.sum(probs ** 2)


def best_split(X, y, feature_idx):
    values = np.unique(X[:, feature_idx])
    if len(values) <= 1:
        return None, -1.0

    best_threshold = None
    best_gain = -1.0
    parent_gini = gini_impurity(y)
    n = len(y)

    for i in range(len(values) - 1):
        threshold = (values[i] + values[i + 1]) / 2.0
        left_mask = X[:, feature_idx] <= threshold
        right_mask = ~left_mask

        n_left = np.sum(left_mask)
        n_right = np.sum(right_mask)

        if n_left == 0 or n_right == 0:
            continue

        gain = parent_gini - (n_left / n) * gini_impurity(y[left_mask]) - (n_right / n) * gini_impurity(y[right_mask])

        if gain > best_gain:
            best_gain = gain
            best_threshold = threshold

    return best_threshold, best_gain


def tree_importance(X, y, n_trees=50, max_depth=5, seed=42):
    rng = np.random.RandomState(seed)
    n_samples, n_features = X.shape
    importances = np.zeros(n_features)

    for _ in range(n_trees):
        sample_idx = rng.choice(n_samples, size=n_samples, replace=True)
        feature_subset = rng.choice(n_features, size=max(1, int(np.sqrt(n_features))), replace=False)

        X_boot = X[sample_idx]
        y_boot = y[sample_idx]

        tree_imp = _build_tree_importance(X_boot, y_boot, feature_subset, max_depth)
        importances += tree_imp

    total = importances.sum()
    if total > 0:
        importances /= total

    return importances


def _build_tree_importance(X, y, feature_subset, max_depth, depth=0):
    n_features = X.shape[1]
    importances = np.zeros(n_features)

    if depth >= max_depth or len(np.unique(y)) <= 1 or len(y) < 4:
        return importances

    best_feature = None
    best_threshold = None
    best_gain = -1.0

    for f in feature_subset:
        threshold, gain = best_split(X, y, f)
        if gain > best_gain:
            best_gain = gain
            best_feature = f
            best_threshold = threshold

    if best_feature is None or best_gain <= 0:
        return importances

    importances[best_feature] += best_gain * len(y)

    left_mask = X[:, best_feature] <= best_threshold
    right_mask = ~left_mask

    importances += _build_tree_importance(X[left_mask], y[left_mask], feature_subset, max_depth, depth + 1)
    importances += _build_tree_importance(X[right_mask], y[right_mask], feature_subset, max_depth, depth + 1)

    return importances
```

### Adım 7: Tüm yöntemleri çalıştır ve karşılaştır

Kod dosyası aynı sentetik veri kümesinde beş yöntemi de çalışır ve her yöntemi seçen özellikleri gösteren bir karşılaştırma tablosu basar.

> Kod dosyası aynı sentez veriler kümesinde çalıştırılan tüm beş yöntemden oluşur ve her yöntemin hangi özellikleri seçtiğini gösterir bir karşılaştırma tablosu basar.

## Çerçeveyi kullanın.

Scikit-learn ile, özellik seçimi boru hattına yerleştirilmiştir:

> Sikit-learn kullanın, 特征选择内置于管线中:

```python
from sklearn.feature_selection import (
    VarianceThreshold,
    mutual_info_classif,
    RFE,
    SelectFromModel,
)
from sklearn.linear_model import Lasso, LogisticRegression
from sklearn.ensemble import RandomForestClassifier

vt = VarianceThreshold(threshold=0.01)
X_filtered = vt.fit_transform(X)

mi_scores = mutual_info_classif(X, y)
top_k = np.argsort(mi_scores)[-10:]

rfe_selector = RFE(LogisticRegression(), n_features_to_select=10)
rfe_selector.fit(X, y)
X_rfe = rfe_selector.transform(X)

lasso_selector = SelectFromModel(Lasso(alpha=0.01))
lasso_selector.fit(X, y)
X_lasso = lasso_selector.transform(X)

rf = RandomForestClassifier(n_estimators=100)
rf.fit(X, y)
importances = rf.feature_importances_
```

Başlangıçtaki uygulamalar her yöntemin içinde ne olduğunu tam olarak gösterir.`var(X, axis=0)`RFE, bir tren, sıra ve kürek çizer bir döngüdür. L1 yumuşak bir sınırlı adımla gradient düşüşüdür. Ağaç önemi bölünmeler boyunca kirlilik azaltmalarını biriktirir. Sihir yok - sadece istatistik ve döngüler.

> Züre'den gerçekleştirilirken, her yöntemin içinde neler olduğunu gösterir.`var(X, axis=0)`Ve örtülü uygulamaktadır. Aramızdaki bilgi, hesaplama çizelgesindeki birleşik frekans ve sınır frekansıdır. RFE, bir eğitim, düzenleme ve kesim döngüsüdür. L1, hafif değer adımlarının derecesinin düşmesi ile oluşur.

sklearn sürümleri dayanıklılık (örneğin, mutual_info_classif, bin yerine k-NN yoğunluk tahminini kullanır), hız (C uygulamalar) ve boru hattı entegrasyonu.

> K-NN  yoğunluk tahminleri ve bölge değil) 速度 (C) 实现) 及管线集成──

## İndirin . Ürünler .

Bu ders şunları ortaya çıkarır:
- `outputs/skill-feature-selector.md`-- doğru özellik seçimi yöntemi seçmek için hızlı bir referans karar ağacı

## Egzersizler.

1. **Forward selection**RFE'nin tam tersini uygulayın. Zıfır özelliklerle başlayın. Her adımda model performansını en çok iyileştiren özelliği ekleyin. Özellikleri eklerken durun artık yardımcı olmaz. Seçilen özellikleri RFE sonuçlarıyla karşılaştırın. Hangisi daha hızlı? Hangisi daha iyi sonuçlar verir?
   1. 100 özellikli bir veri kümesi oluşturuldu. On tanesi hedef ile ilgili, 90 tanesi gürültü.

2. **Stability selection**L1 özellik seçimi: L1 özellik seçimini 50 kez, her seferinde, verilerin rastgele bir alt örnekinin %80'inde, hafif farklı alfa değerleri ile çalıştırın. Her özellik ne kadar sık seçilir.
   2. 实现后向消除 (→ tüm özelliklerden başlayarak, bire bire çıkarmak) ◊与前向选择比较效率和结果──

3. **Multicollinearity detection**: tüm özellikler için ilişki matrisi hesaplayın. Bir ilişki eşiği (örneğin 0,9) verildiğinde, her yüksek ilişkili çiftten bir özellik çıkarır (hedef ile daha yüksek karşılıklı bilgi olan bir çiftin korunması). Sentetik veri kümesi üzerinde test yapın ve onu doğrulayın.
   3. Aynı veri kümesi üzerinde L1 normalleşmesi ve RFE'nin seçim sonuçları karşılaştırıldığında, aynı özellikleri seçtiler mi?

4. **Feature selection pipeline**: zincir varyansa eşiği, karşılıklı bilgi filtresi ve RFE tek bir boru hattına. Önce sıfır yakın varyansa özelliklerini kaldırın, sonra üst 50%'i karşılıklı bilgi ile tutun, sonra hayatta kalanlar üzerinde RFE çalıştırın. Bu boru hattını tüm özelliklerde RFE'yi tek başına çalıştırmaya karşılaştırın. Boru hattı daha hızlı mıdır?
   4. 构建完整的特征选择管线:方差值 -> 相关性过 -> 互信息 -> L1──展示每步移除多少特征以及模型性能的变化──

5. **Permutation importance from scratch**F1 puanının ortalama düşüşünü ölçerek, her özellik için değerlerini 10 kez karıştırın. Rangoyu ağaç tabanlı önemle karşılaştırın. Anlaşmazlıkların olduğu durumları bul ve nedenini açıklayın (söyleme: ilişkili özellikler).

> **【中文解读】**
> Özellik Seçimi'nin gerçek savaş stratejisi: 1) Önceden kullanılan yön farkı  değerini düzenli özelliklerden çıkarmak   差接近零 anlamına gelir hiçbir bilgi yoktur; 2) birbirine bilgi ile                                                                                                                                                                                                                                       

> **【拓展：递归特征消除（RFE）的工业应用】**
> RFE, genoloji alanında geniş çapta kullanılıyor. 20.000 gen ifadeinden en öngörücü 50-100 gen seçilir, sadece model performansını artırmakla kalmaz, aynı zamanda hastalık belirtici bulguları için de adaylar sunar. Finansal rüzgar kontrolünde, RFE, yüzlerce aday özellikinden son giriş özelliklerini seçmek için yardımcı olur.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Filter method | "Score features independently" | A feature selection approach that ranks features using a statistical measure without training a model, evaluating each feature in isolation |
| Wrapper method | "Use the model to pick features" | A feature selection approach that evaluates feature subsets by training a model and using its performance as the selection criterion |
| Embedded method | "The model selects features during training" | Feature selection that happens as part of model fitting, such as L1 regularization driving weights to zero |
| Mutual information | "How much one variable tells you about another" | A measure of the reduction in uncertainty about Y given knowledge of X, capturing both linear and nonlinear dependencies |
| Recursive Feature Elimination | "Train, rank, prune, repeat" | An iterative wrapper method that trains a model, removes the least important feature(s), and repeats until a target count is reached |
| L1 / Lasso regularization | "Penalty that kills features" | Adding the sum of absolute weight values to the loss function, which drives unimportant feature weights to exactly zero |
| Variance threshold | "Remove constant features" | Dropping features whose variance across samples falls below a specified threshold, filtering out features that carry no information |
| Feature importance | "Which features matter most" | A score indicating how much each feature contributes to model predictions, computed from split gains (trees) or coefficient magnitudes (linear) |
| Permutation importance | "Shuffle and measure the damage" | Evaluating feature importance by randomly shuffling each feature's values and measuring the resulting drop in model performance |
| Curse of dimensionality | "Too many features, not enough data" | The phenomenon where adding features increases the volume of the feature space exponentially, making data sparse and distances meaningless |

## Daha fazla okumak

- [An Introduction to Variable and Feature Selection (Guyon & Elisseeff, 2003)](https://jmlr.org/papers/v3/guyon03a.html)-- Özellik seçimi yöntemleri üzerine temel araştırmaya, hala yaygın olarak atıfta bulunmaktadır
  [Guyon & Elisseeff: An Introduction to Variable and Feature Selection (2003)](https://jmlr.org/papers/v3/guyon03a.html)- Özellik Seçim Genel
- [scikit-learn Feature Selection Guide](https://scikit-learn.org/stable/modules/feature_selection.html)-- Filtr, ambalaj ve kod örnekleri ile gömülü yöntemler için pratik referans
  [scikit-learn 特征选择文档](https://scikit-learn.org/stable/modules/feature_selection.html)
- [Stability Selection (Meinshausen & Buhlmann, 2010)](https://arxiv.org/abs/0809.2932)-- güçlü, tekrarlanabilir sonuçlar için alt örnekleme ile özellik seçimi birleştirir
  [Feature Engineering and Selection](http://www.feat.engineering/)- 免费在线书籍
- [Beware Default Random Forest Importances (Strobl et al., 2007)](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-8-25)-- ağaç temelli önemdeki kardinallik önyargısını gösterir ve alternatif olarak koşullu önem önerir
