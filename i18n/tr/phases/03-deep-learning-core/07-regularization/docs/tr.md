# Düzenleme. Düzenleme.

> Modeliniz %99'u eğitim verileri ve %60'ını test verileri ile elde eder. Öğrenmek yerine ezberler.

> **【中文解读】**模型訓練集 99% ama test集 sadece 60%                                                                                                                                                                                                                                                          

**Type:** Build
**Languages:** Python
**Prerequisites:** Lesson 03.06 (Optimizers)
**Time:** ~75 minutes

## Öğrenme hedefleri

- Ters ölçeklendirme, L2 ağırlık kaybı, parti normallendirme, katman normallendirme ve sıfırdan RMSNorm ile uygulama bırakma
- Tren testi doğruluk boşluğunu ölçmek ve düzenleme deneylerini kullanarak aşırı uygunluğu teşhis etmek
- Transformatörlerin BatchNorm yerine LayerNorm neden kullandığını ve modern LLM'lerin neden RMSNorm'ı tercih ettiğini açıklayın.
- Üstü uyumluğun şiddetine göre düzenleme tekniklerinin doğru kombinasyonunu uygulayın.

> **【中文解读】**Bu bölümde, yeni bir sistem oluşturmak için kullanılan beş temel araçlar:Dropout (Droput) L2 (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (Layer) Layer (L) Layer) Layer (L) Layer (Layer) Layer (Layer) Layer (Layer) Layer (L) Layer (L) Layer (L) Layer (L) Layer (L) Layer (L) Layer (L) (L) (L)

## Sorunlar. Sorunlar.

Yeterli parametreleri olan bir sinir ağı herhangi bir veri kümesini ezberleyebilir. Bu bir hipotezi değil - Zhang et al. (2017) bunu ImageNet'te rastgele etiketlerle standart ağları eğiterek kanıtladı. Ağlar tamamen rastgele etiket görevlerinde neredeyse sıfır eğitim kaybına ulaştı. Öğrenmek için bir patern olmadan bir milyon rastgele giriş-çıkanış çiftini ezberlediler. Eğitim kaybı mükemmeldi. Test doğruluğu sıfırdı.

> Zhang et al., (2017) bunu ImageNet'te rastgele etiketleme eğitim standartları ile kanıtladı. Ağ tam rastgele etiket dağıtımında neredeyse sıfırına yaklaşmış bir eğitim kaybına ulaşmıştır. Onlar bir milyon düzensiz akademik rastgele giriş-çıktırmalarını hatırlıyor.

Bu, aşırı uyumlu bir sorun ve modeller büyüdükçe daha da kötüleşir. GPT-3 175 milyar parametre sahiptir. Eğitim kümesi yaklaşık 500 milyar jetonu vardır. Bu sayısız parametre ile, model eğitim verilerinin önemli parçalarını kelimenin bir anlamında ezberleyebilecek kadar kapasiteye sahiptir. Düzenlendirme olmadan, genel hale getirülebilir kalıpları öğrenmek yerine sadece eğitim örneklerini tekrar tekrar üretecektir.

> Bu, bir çok uyumlu bir sorun. Modelin büyümesi ve daha da kötüleşmesiyle birlikte. GPT-3'de 1750 milyar parametre vardır.

Eğitim performansıyla test performansı arasındaki fark, aşırı uygunluk aralığıdır. Bu dersdeki her teknik farklı bir açıdan bu boşluğu vurur. İptal, ağın tek bir nörona güvenmemesini zorlar. Ağırlık kaybı, herhangi bir ağırlığın çok büyükleşmesini engeller. Satır normallendirme kayıp manzarasını düzeltir böylece optimizör daha düz, daha genel hale getirebilen minimumlar bulur. Katman normallaştırması aynı şeyi yapar ancak parti normallaştırması başarısız olduğunda çalışır (küçük partiler, değişken uzunluklı diziler). RMSNorm ortalama hesaplamayı düşürerek %10 daha hızlı yapar. Her teknik basit. Birlikte, ezberleyen ve genelleştiren bir model arasındaki farkı oluştururlar.

>  Eğitim performansı ile test performansı arasındaki fark, aşırı uygunluk farkıdır. Bu dersdeki her teknik farklı açıdan bu farkı saldırır.  Dropout  Zorlu ağlar herhangi bir tek sinirden bağımlı değildir.  Vücut kaybı herhangi bir tek ağırlığın aşırı büyümesini önler.  Bütü birleştirme düzlük kaybı eğri yüzeyini bulur, optimizasyon makinesi daha düz, daha değerli genelleştirilmiş küçük değerleri bulur.  Layer birleştirme aynı şeyi yapar, ancak grup birleştirme başarısız olduğu yerde geçerli küçük bitler  Bütü  Değişiklik dizisi)  RMSNorm  Provincial average calculation  10%                                                                                                                                                                            

> **【中文解读】**模型参数越多,越容易过拟合――GPT-3 has 1750 亿参数、5000 亿 token no normalization, it only recites training data── her normalization means from different angles attack over suited:Dropout 强制冗余表示、权重衰减限制参数幅度、归化平滑损曲面──

> **【拓展：大模型的正则化策略】**GPT-4 ve Llama 3'ün düzeltmesi çok basit:AdamW 权重衰减 (wd=0.01) + Dropout (p=0.1) + RMSNorm。 karmaşık düzeltme teknikleri kullanılmıyor。关键洞察:

## Konsepten bir şey.

### - Üstünlük Spektrumu.

Her model bir spektrimde bir yerde oturur. (önümünü yakalamak için çok basit) aşırı uyumlu (gürültüyü yakalamak için çok karmaşık).

> Her model, uygunsuzluktan çok basit ve algılayamayan moduya kadar, uygunsuzluktan çok karmaşık olan gürültüyi algılamaya kadar bir dizi dizi dizi üzerinde bir konumdadır. En iyi noktası ortalarda, normalleşme modeli uygunsuzluktan en iyi noktaya doğru yönlendirir.

```mermaid
graph LR
    Under["Underfitting<br/>Train: 60%<br/>Test: 58%<br/>Model too simple"] --> Good["Good Fit<br/>Train: 95%<br/>Test: 92%<br/>Generalizes well"]
    Good --> Over["Overfitting<br/>Train: 99.9%<br/>Test: 65%<br/>Memorized noise"]

    Dropout["Dropout"] -->|"Pushes left"| Over
    WD["Weight Decay"] -->|"Pushes left"| Over
    BN["BatchNorm"] -->|"Pushes left"| Over
    Aug["Data Augmentation"] -->|"Pushes left"| Over
```

### İptal etmek.

Eğitim sırasında, her nöronun çıkışını rastgele olarak p olasılığı ile sıfıra ayarlayın.

> En basit ve en iyi normalleştirme tekniğini açıklamak için.

```
output = activation(z) * mask    where mask[i] ~ Bernoulli(1 - p)
```

P = 0.5'te, nöronların yarısı her ileri geçişte sıfırlanır. Ağ, neyronların hangi nöronların bulunacağını tahmin edemediği için fazladan temsilleri öğrenmelidir. Bu, uyumlu olmayı engeller - nöronlar belirli diğer nöronlara güvenmeyi öğrenir.

> P = 0.5'de, her ön yönlü yayımlama sırasında nöronların yarısı sıfırlaştırılır. Ağ, hangi nöronların kullanılabileceğini tahmin edemediği için reduktif ifadeyi öğrenmelidir. Bu, nöronların belirli diğer nöronlara bağımlı olmalarını önler.

Ensemsel yorum: N nöronu ve çıkışa sahip bir ağ 2^N olası alt ağlar (nöronların açılıp kapalı olduğu her kombinasyon) oluşturur. Eğitim, yaklaşık olarak her iki N alt ağını aynı anda, her biri farklı mini-batch'larda trenleştiriyor. Test sırasında tüm nöronları kullanır (bırakma) ve hazırlık sırasında beklenen değerle eşleşmek için çıkışları (1 - p) oranında ölçebilirsiniz. Bu, 2^N alt ağlarının tahminlerinin ortalamasına eşittir -- tek bir modelden oluşan büyük bir ansambl.

> 集成 açıklaması: bir n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n

Pratikte, test yerine eğitim sırasında ölçeklendirme uygulanır (i ters düşüş):

```
During training:  output = activation(z) * mask / (1 - p)
During testing:   output = activation(z)   (no change needed)
```

Bu daha temiz çünkü test kodu hiç de terk edilme hakkında bilgi sahibi olmamalı.

> Bu daha temiz çünkü test kodunun varlığını tamamen bilmemek gerekir.

Öntanımlı oranlar: transformörler için p = 0,1 , MLP için p = 0,5 , CNN'ler için p = 0,2 - 0,3 .

> 默认比率:Transformer 用 p = 0.1,MLP 用 p = 0.5,CNN 用 p = 0.2-0.3── dropout 越高 = 正则化越强 = 欠拟合风险越大──

> **【拓展：Dropout 在 BERT 和 GPT 中的不同用法】**BERT kullanımı Dropout p=0.1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

### Kilo kaybı (L2 düzenlenmesi) 权重减减 (L2 正则化)

Tüm ağırlıkların karede büyüklüğünü kaybına ekleyin:

> Mülkiyetin ağırlığındaki kareler kaybına kadar:

```
total_loss = task_loss + (lambda / 2) * sum(w_i^2)
```

Normalleştirme terimin gradiyenti lambda * w. Bu, her adımda her ağırlığın büyüklüğüne orantılı bir bölümle sıfıra doğru küçültüldüğü anlamına gelir. Büyük ağırlıklar daha fazla cezalandırılır.

> Düzenlenme programının derecesi lambda * wdır. Bu, her adımda, her ağırlık, boyutuna göre oranla sıfıra küçülüyor.

Bu neden genelleşmeye yardımcı olur: Overfit modellerin eğitim verilerinde gürültüyi artırmak için büyük ağırlıklara sahip olma eğilimindedir.

> Neden bu genelleşmeye yardımcı olur: Uyumlu model genellikle çok büyük bir ağırlığa sahiptir, eğitim verilerindeki gürültüyü arttırır.

Lambda hiperparametri sertliği kontrol eder.

> lambda 超参数控制强度── tipik değer:

- AdamW için transformatörler için 0.01
  Çeviri: 0.01 Transformer 上的 AdamW için kullanılır
- 1e-4 için SGD CNN'de
  Çinçe Çevirimi: 1e-4
- 0.1 ağırlıklı olarak fazla uyumlu modeller için
  0.1 Çok uygun model kullan

Ders 06'da tartışıldığı gibi, kilo kaybı ve L2 düzenlenmesi SGD'de eşittir ama Adam'da değil.

> 6. Sınıfda tartışılan: Kilo düşüşü ve L2 normalleşmesi SGD ortalama fiyatlarda, ama Âdem ortalama fiyatlarda eşit değildir.

### Toplu Normalleşme.

Mini-batch'ın her katmanının çıkışını bir sonraki katmana geçmeden önce normalleştirin.

> Bu, mini-batch'a ilişkin birleştirme yapılması için yapılır.

Bir katman üzerinde mini seri aktivasyonlar için:

> 某一层的一个小型批量 激活值:

```
mu = (1/B) * sum(x_i)           (batch mean)
sigma^2 = (1/B) * sum((x_i - mu)^2)   (batch variance)
x_hat = (x_i - mu) / sqrt(sigma^2 + eps)   (normalize)
y = gamma * x_hat + beta        (scale and shift)
```

Gamma ve beta, ağın normalleşmeyi iptal etmesine izin veren öğrenilebilir parametrelerdir.

> Gamma ve beta, en iyi şekilde öğrenilebilir bir parametredir, eğer en iyi şekilde, ağın geri çekilmesini birleştirmek için kullanılabilir.

**Training vs inference split:**Eğitim sırasında, mu ve sigma mevcut mini-batch'ten gelir. Tahmin sırasında, eğitim sırasında birikmiş koşuş ortalamalarını kullanırsınız (eğlence = 0,1 ile esponansel hareketli ortalama, yani 90% eski + 10% yeni).

> **训练与推理的区别：**訓練時,mu 和 sigma 来自当前ミニ-batch──推理時,使用訓練期間累积的运行平均值(指数移动平均,动量 = 0.1,即90% 旧值 + 10% 新值)──

BatchNorm'un neden işe yaradığını tartışıyoruz. Orijinal makalede "içi kovariyet değişimi"ni (daha önceki katmanların güncelleşmesiyle değişen katman girişlerinin dağılımını) azaltıyor. Santurkar et al. (2018) bu açıklamanın yanlış olduğunu gösterdi. Gerçek neden: BatchNorm kayıpları daha da kolaylaştırıyor. Gradyentler daha öngörücüdür, Lipschitz sabitleri daha küçüktür ve optimizer daha büyük adımları güvenli bir şekilde atabilir. Bu yüzden BatchNorm daha yüksek öğrenme oranlarını kullanmanıza ve daha hızlı bir şekilde bir araya gelmenize izin verir.

> BatchNorm neden geçerli olduğu tartışmaya devam ediyor. İlk makale, "İçteki koesans değişim kayıplarını" azaltıyor, "üst kattaki girişlerin dağılımının ön kattaki yenilemlerle değişmesi" olduğunu iddia ediyor. Santurkar 等人 (2018) bu açıklamanın yanlış olduğunu kanıtlıyor. Gerçek neden: BatchNorm, kayıpların daha düz bir şekilde gerçekleşmesini sağlıyor.

BatchNorm'un temel bir sınırlaması vardır: seri istatistiklerine bağlıdır. 1 seri boyutu ile ortalama ve varyansa anlamsızdır. Küçük seri (< 32), istatistikler gürültülü ve zararlı performans gösterir. Bu, nesne tespit (hüye belleği seri boyutunu sınırlayan) ve dil modelleme (sequence uzunlukları değişen) gibi görevlerde önemlidir.

> BatchNet'in temel bir sınırı vardır: Satır statisine bağlıdır. Satır boyutu = 1 时, ortalama değer ve yön farkı anlamsızdır.

> **【中文解读】**BatchNorm'un temel sınırları: Batch_size=1 时平均值差无意;batch_size<32 时统计量噪声太大──这是变压器 用 LayerNorm'ın nedeni语言模型批小、序列长度不一──

### Katman Normalleşmesi . Katman birleştirilmesi .

Bir numune için, parti yerine özellikler arasında normalleştirin:

> 跨特征维度归化,跨批量 değil:

```
mu = (1/D) * sum(x_j)           (feature mean)
sigma^2 = (1/D) * sum((x_j - mu)^2)   (feature variance)
x_hat = (x_j - mu) / sqrt(sigma^2 + eps)
y = gamma * x_hat + beta
```

D özellik boyutudur. Her örnek bağımsız olarak normallaştırılır - parti boyutundan bağımsız değildir. Bu nedenle transformatörler BatchNorm yerine LayerNorm kullanır. Sequence değişken uzunluklara sahiptir, parti boyutları genellikle küçüktür (veya 1 jenerasyon sırasında), ve hesaplama eğitim ve sonuçlama arasında aynıdır.

> D ise özellik boyutudur. Her örnek bağımsız olarak birleştirilmeye bağlı değildir. Bu yüzden Transformer BatchNorm yerine LayerNorm kullanır.

Transformatorlarda LayerNorm, her kendi dikkat blokunun ve her ileriye aktarma blokunun (Post-LN) ardından veya öncesinde (Evrim eğitimi için daha istikrarlı olan Pre-LN) uygulanır.

> Transformer Orta LayerNorm  应用于每个自注意力块和每个前块后 (post-LN),或之前 (pre-LN,训练更稳定) ⋅

### RMSNorm.

LayerNorm ortalama çıkarmadan. Zhang & Sennrich tarafından önerilen (2019).

> LayerNorm 去掉平均值减法── Zhang & Sennrich (2019) tarafından önerilmiştir──

```
rms = sqrt((1/D) * sum(x_j^2))
y = gamma * x / rms
```

Bu da. Ortalama hesaplama yok, beta parametri yok. gözlem: LayerNorm'daki yeniden merkeze (ortalama çıkarma) modelin performansına çok az katkıda bulunur, ancak hesaplama maliyetleri vardır.

> İşte böyle. Hiçbir ortalama değer hesaplanmıyor, hiçbir beta parametri yok.

LLaMA, LLaMA 2, LLaMA 3, Mistral ve çoğu modern LLM LayerNorm yerine RMSNorm kullanır.

> LLaMA、LLaMA 2、LLaMA 3、Mistral 和 çoğu modern LLM RMSNorm kullanır LayerNorm değil.

> **【拓展：RMSNorm 为什么能省 10%】**LayerNorm  hesaplama ortalama değer ve yön farkı iki adım,RMSNorm  sıçrayış ortalama değer sadece RMS olarak hesaplanır. Llama 3 405B  126 kat) üzerinde, her adım eğitim 252 RMSNorm  düzenli olarak düzenlenir.

### Normalleşme karşılaştırması

### Normalleşme karşılaştırması

```mermaid
graph TD
    subgraph "Batch Normalization"
        BN_D["Normalize across BATCH<br/>for each feature"]
        BN_S["Batch: [x1, x2, x3, x4]<br/>Feature 1: normalize [x1f1, x2f1, x3f1, x4f1]"]
        BN_P["Needs batch > 32<br/>Different train vs eval<br/>Used in CNNs"]
    end
    subgraph "Layer Normalization"
        LN_D["Normalize across FEATURES<br/>for each sample"]
        LN_S["Sample x1: normalize [f1, f2, f3, f4]"]
        LN_P["Batch-independent<br/>Same train vs eval<br/>Used in Transformers"]
    end
    subgraph "RMS Normalization"
        RN_D["Like LayerNorm<br/>but skip mean subtraction"]
        RN_S["Just divide by RMS<br/>No centering"]
        RN_P["10% faster than LayerNorm<br/>Same accuracy<br/>Used in LLaMA, Mistral"]
    end
```

### Veri artışı düzenlendirme olarak veri artışı normalleşme olarak

Model değiştirilmesi değil, veri değiştirilmesi. Etiketleri korurken eğitim girişlerini dönüştürün:

> Modelle değişim değil, veri değişimi. Etiket değişmezken değişim:

- Resimler: rastgele biçim, dönüş, dönüm, renk gerginliği, kesim
  Çinçe Çevirim: İzleme:随机剪转转转转转转色 动 遮
- Metin: eşya sözcükleri değiştirme, geri çevirme, rastgele silme
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Ses: zaman uzantısı, yüksek ses değişimi, gürültü eklenmesi
  Çinçe Çevirim:音频:时间拉伸、音调偏移、添加噪音

Bu, düzenlenme ile aynıdır: eğitim kümesinin etkin boyutunu arttırır ve modelin belirli örnekleri ezberlemesini zorlaştırır. Her resmini sadece orijinal biçiminde bir kez gören bir model onu ezberleyebilir. Her resmin 50 artırılmış versiyonunu gören bir model değişmez yapıyı öğrenmek zorunda kalır.

> 效果与正则化相同:它增加了训练集的有效大小,使模型更难记得特定样本――; 效果与正则化相同:它增加了训练集的有效大小,使模型更难记得特定样本――; 效果与正则化相同:它增加了训练集的有效大小,使模型更难记得特定样本――; 效果与正则化相同:它增加了训练集的有效大小,使模型更难记得特定样本――; 效果与正则化相同:它增加了训练集的有效大小,使模型更难记得特定样本――; 效果与正则化; 效果与正则化; 效果与正则化相同:它增加了训练集的有效大小,使模型更难记得特定样本的模型; 只有看到每张图像原形式的模型可以记得它; 看到每张图片每张图片50个增强版本的模型被迫学习不变结构――;

### Erken Durmak Erken Durmak

En basit düzenleyici: doğrulama kaybı artmaya başladığında eğitimden vazgeç. Model henüz o noktada fazla uyumlu değil.

> En basit düzenleme yöntemi: Test kaybı arttıkça eğitim durdurmak. Bu zaman model henüz uygun değil.

> **【拓展：Early Stopping 在大模型中的实践】**GPT 和 Llama 等大模型通常不使用早期停止训练在固定代币 数后结束──但在微调阶段 (如 LoRA 细调),早期停止 非常重要,因为小数据集上容易过拟合──HuggingFace's Trainer 默认使用早期停止(耐心=3),监控 eval_loss──

### Ne Zaman Kullanmalı Neyi ?

```mermaid
flowchart TD
    Gap{"Train-test<br/>accuracy gap?"} -->|"> 10%"| Heavy["Heavy regularization"]
    Gap -->|"5-10%"| Medium["Moderate regularization"]
    Gap -->|"< 5%"| Light["Light regularization"]

    Heavy --> D5["Dropout p=0.3-0.5"]
    Heavy --> WD2["Weight decay 0.01-0.1"]
    Heavy --> Aug["Aggressive data augmentation"]
    Heavy --> ES["Early stopping"]

    Medium --> D3["Dropout p=0.1-0.2"]
    Medium --> WD1["Weight decay 0.001-0.01"]
    Medium --> Norm["BatchNorm or LayerNorm"]

    Light --> D1["Dropout p=0.05-0.1"]
    Light --> WD0["Weight decay 1e-4"]
```

## Yapın.
```figure
l2-regularization
```

## Yapın

> **【中文解读】**Aşağıda ise ise ise, "Dropout"ın ters ölçeklendirilmesi, "Train Time Apart in (1-p), "Train Time Unchanged" ve "BatchNorm"ın iki modeli bulunmaktadır.

### Adım 1: Durdurma (Eval ve Tren Mode)

> İlk adım:Dropout 实现──关键是逆倒落训练时按概率 p 置零,余值除以 (1-p) 保持期望不变;推理时直接通过──这样推理代码不需要知道的存在──倒退也需要应用相同的面具(除以 (1-p))──

```python
import random
import math


class Dropout:
    def __init__(self, p=0.5):
        self.p = p
        self.training = True
        self.mask = None

    def forward(self, x):
        if not self.training:
            return list(x)
        self.mask = []
        output = []
        for val in x:
            if random.random() < self.p:
                self.mask.append(0)
                output.append(0.0)
            else:
                self.mask.append(1)
                output.append(val / (1 - self.p))
        return output

    def backward(self, grad_output):
        grads = []
        for g, m in zip(grad_output, self.mask):
            if m == 0:
                grads.append(0.0)
            else:
                grads.append(g / (1 - self.p))
        return grads
```

### Adım 2: L2 Ağırlık kaybı

> İkinci adım:L2 Doğruluk kaybı ve derecesi── kaybı项 = (lambda/2) × 平方和;梯度 = lambda × 权重── her bir ağırlık her adımda 往零方向拉一点点──Adam 中要用AdamW(解权重衰减)才等价──

```python
def l2_regularization(weights, lambda_reg):
    penalty = 0.0
    for w in weights:
        penalty += w * w
    return lambda_reg * 0.5 * penalty

def l2_gradient(weights, lambda_reg):
    return [lambda_reg * w for w in weights]
```

### Adım 3: Satır Normalleşmesi.

> Üçüncü adım: BatchNorm 实现── тренинг时: Using the average value of the current batch, simultaneously cumulative run average (BATCHNORM) ⋅ Suggestion时: Using cumulative run average ⋅ Gamma/beta is learning parameters make the network's "elimination" ability― dikkat eps  prevent de delimination ⋅ 0.

```python
class BatchNorm:
    def __init__(self, num_features, momentum=0.1, eps=1e-5):
        self.gamma = [1.0] * num_features
        self.beta = [0.0] * num_features
        self.eps = eps
        self.momentum = momentum
        self.running_mean = [0.0] * num_features
        self.running_var = [1.0] * num_features
        self.training = True
        self.num_features = num_features

    def forward(self, batch):
        batch_size = len(batch)
        if self.training:
            mean = [0.0] * self.num_features
            for sample in batch:
                for j in range(self.num_features):
                    mean[j] += sample[j]
            mean = [m / batch_size for m in mean]

            var = [0.0] * self.num_features
            for sample in batch:
                for j in range(self.num_features):
                    var[j] += (sample[j] - mean[j]) ** 2
            var = [v / batch_size for v in var]

            for j in range(self.num_features):
                self.running_mean[j] = (1 - self.momentum) * self.running_mean[j] + self.momentum * mean[j]
                self.running_var[j] = (1 - self.momentum) * self.running_var[j] + self.momentum * var[j]
        else:
            mean = list(self.running_mean)
            var = list(self.running_var)

        self.x_hat = []
        output = []
        for sample in batch:
            normalized = []
            out_sample = []
            for j in range(self.num_features):
                x_h = (sample[j] - mean[j]) / math.sqrt(var[j] + self.eps)
                normalized.append(x_h)
                out_sample.append(self.gamma[j] * x_h + self.beta[j])
            self.x_hat.append(normalized)
            output.append(out_sample)
        return output
```

### Adım 4: Katman Normalleşmesi.

```python
class LayerNorm:
    def __init__(self, num_features, eps=1e-5):
        self.gamma = [1.0] * num_features
        self.beta = [0.0] * num_features
        self.eps = eps
        self.num_features = num_features

    def forward(self, x):
        mean = sum(x) / len(x)
        var = sum((xi - mean) ** 2 for xi in x) / len(x)

        self.x_hat = []
        output = []
        for j in range(self.num_features):
            x_h = (x[j] - mean) / math.sqrt(var + self.eps)
            self.x_hat.append(x_h)
            output.append(self.gamma[j] * x_h + self.beta[j])
        return output
```

### Adım 5: RMSNorm Beşinci Adım: Orta kök birleştirme

> 第五步:RMSNorm LayerNorm'un basitleştirilmiş sürümüdür. Sadece RMS (RMS)  ortalama kök), hiç azaltılmamış ortalama değer, beta yok.

```python
class RMSNorm:
    def __init__(self, num_features, eps=1e-6):
        self.gamma = [1.0] * num_features
        self.eps = eps
        self.num_features = num_features

    def forward(self, x):
        rms = math.sqrt(sum(xi * xi for xi in x) / len(x) + self.eps)
        output = []
        for j in range(self.num_features):
            output.append(self.gamma[j] * x[j] / rms)
        return output
```

### Adım 6: Düzenlenme ile Düzenlenme olmadan Eğitim

> 6. adım: Eğitim/normalleşme oranı %100'e ulaşabilmek için düzensiz bir ağla yapılan eğitimler üzerinde %65'e ulaşabilmek için düzensiz bir ağla yapılan eğitimler üzerinde %65'e ulaşabilmek için düzensiz bir ağla yapılan eğitimler üzerinde %65'e ulaşabilmek için %65'e ulaşabilmek için düzensiz bir ağla yapılan eğitimler üzerinde %95'e düşebilir.

```python
def sigmoid(x):
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))


def make_circle_data(n=200, seed=42):
    random.seed(seed)
    data = []
    for _ in range(n):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        label = 1.0 if x * x + y * y < 1.5 else 0.0
        data.append(([x, y], label))
    return data


class RegularizedNetwork:
    def __init__(self, hidden_size=16, lr=0.05, dropout_p=0.0, weight_decay=0.0):
        random.seed(0)
        self.hidden_size = hidden_size
        self.lr = lr
        self.dropout_p = dropout_p
        self.weight_decay = weight_decay
        self.dropout = Dropout(p=dropout_p) if dropout_p > 0 else None

        self.w1 = [[random.gauss(0, 0.5) for _ in range(2)] for _ in range(hidden_size)]
        self.b1 = [0.0] * hidden_size
        self.w2 = [random.gauss(0, 0.5) for _ in range(hidden_size)]
        self.b2 = 0.0

    def forward(self, x, training=True):
        self.x = x
        self.z1 = []
        self.h = []
        for i in range(self.hidden_size):
            z = self.w1[i][0] * x[0] + self.w1[i][1] * x[1] + self.b1[i]
            self.z1.append(z)
            self.h.append(max(0.0, z))

        if self.dropout and training:
            self.dropout.training = True
            self.h = self.dropout.forward(self.h)
        elif self.dropout:
            self.dropout.training = False
            self.h = self.dropout.forward(self.h)

        self.z2 = sum(self.w2[i] * self.h[i] for i in range(self.hidden_size)) + self.b2
        self.out = sigmoid(self.z2)
        return self.out

    def backward(self, target):
        eps = 1e-15
        p = max(eps, min(1 - eps, self.out))
        d_loss = -(target / p) + (1 - target) / (1 - p)
        d_sigmoid = self.out * (1 - self.out)
        d_out = d_loss * d_sigmoid

        for i in range(self.hidden_size):
            d_relu = 1.0 if self.z1[i] > 0 else 0.0
            d_h = d_out * self.w2[i] * d_relu
            self.w2[i] -= self.lr * (d_out * self.h[i] + self.weight_decay * self.w2[i])
            for j in range(2):
                self.w1[i][j] -= self.lr * (d_h * self.x[j] + self.weight_decay * self.w1[i][j])
            self.b1[i] -= self.lr * d_h
        self.b2 -= self.lr * d_out

    def evaluate(self, data):
        correct = 0
        total_loss = 0.0
        for x, y in data:
            pred = self.forward(x, training=False)
            eps = 1e-15
            p = max(eps, min(1 - eps, pred))
            total_loss += -(y * math.log(p) + (1 - y) * math.log(1 - p))
            if (pred >= 0.5) == (y >= 0.5):
                correct += 1
        return total_loss / len(data), correct / len(data) * 100

    def train_model(self, train_data, test_data, epochs=300):
        history = []
        for epoch in range(epochs):
            total_loss = 0.0
            correct = 0
            for x, y in train_data:
                pred = self.forward(x, training=True)
                self.backward(y)
                eps = 1e-15
                p = max(eps, min(1 - eps, pred))
                total_loss += -(y * math.log(p) + (1 - y) * math.log(1 - p))
                if (pred >= 0.5) == (y >= 0.5):
                    correct += 1
            train_loss = total_loss / len(train_data)
            train_acc = correct / len(train_data) * 100
            test_loss, test_acc = self.evaluate(test_data)
            history.append((train_loss, train_acc, test_loss, test_acc))
            if epoch % 75 == 0 or epoch == epochs - 1:
                gap = train_acc - test_acc
                print(f"    Epoch {epoch:3d}: train_acc={train_acc:.1f}%, test_acc={test_acc:.1f}%, gap={gap:.1f}%")
        return history
```

## Çerçeveyi kullanın.

> **【中文解读】**PyTorch 中使用正则化关键:model.train()/model.eval() 切换 Dropout 和 BatchNorm 的行为──在Transformer 中,LayerNorm + Dropout p=0.1 是标配──忘记模型.eval() 是最常见的深度学习 bug 之一──

PyTorch tüm normallaşmayı ve düzenlendirmeyi modüller olarak sağlar:

> PyTorch, tüm özelleştirme ve düzenleme işlevlerini bir modül olarak sunacak:

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(784, 256),
    nn.BatchNorm1d(256),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(256, 128),
    nn.BatchNorm1d(128),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(128, 10),
)

model.train()
out_train = model(torch.randn(32, 784))

model.eval()
out_test = model(torch.randn(1, 784))
```

- Evet .`model.train()`- Ne ?`model.eval()`Çıkış kritik. Açılış/kesinliği açar ve BatchNorm'a seri istatistiklerini çalıştırma istatistikleriyle karşılaştırmak için söyler.`model.eval()`Bu nedenle, bu testlerin doğruluğu rastgele değişecek çünkü çıkış durumları hala aktif ve BatchNorm mini-batch istatistiklerini kullanıyor.

> `model.train()`- Ne ?`model.eval()`切换至关重要──它开关 dropout 并告诉BatchNorm  使用批量统计量还是运行统计量──推理前忘记 `model.eval()`Bu nedenle, bu testlerin doğrulaması oranı, kayıplar için geçerlidir.

Transformatörler için, örneği farklıdır:

> Transformer için farklı modular:

```python
class TransformerBlock(nn.Module):
    def __init__(self, d_model=512, nhead=8, dropout=0.1):
        super().__init__()
        self.attention = nn.MultiheadAttention(d_model, nhead, dropout=dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(),
            nn.Linear(d_model * 4, d_model),
            nn.Dropout(dropout),
        )
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        attended, _ = self.attention(x, x, x)
        x = self.norm1(x + self.dropout(attended))
        x = self.norm2(x + self.ff(x))
        return x
```

LayerNorm, BatchNorm değil. Kaldırma p=0.1, p=0.5. Bunlar dönüştürücü öntanımlıları.

> LayerNorm kullanıyor, BatchNorm değil.

## İndirin . Ürünler .

Bu ders şunları ortaya çıkarır:
- `outputs/prompt-regularization-advisor.md`-- aşırı uygunluk teşhis eden ve doğru düzenleme stratejisini öneren bir istek.

> 本课产 出:`outputs/prompt-regularization-advisor.md`- Bir teşhis yaparak doğru düzgün bir strateji önerisi

## Egzersizler.

1. 2 boyutlu veriler için uzaylı düşüş uygulayın: bireysel nöronları düşürmek yerine, tüm özellik kanallarını düşürün. Bunu ardılı özellik gruplarını kanal olarak değerlendirerek ve tüm grupları düşürerek simüle edin.

2. 5. Dersin 5. bölümünden etiket düzeltmesini uygulayın ve bu dersden çıkma ile birlikte. Dört yapılandırma ile çalışın: hiçbirisi, sadece çıkma, sadece etiket düzeltmesi, her ikisi de. Her biri için son tren testi doğruluk boşluğu ölçün. Hangi kombinasyon en küçük boşluğu verir?

3. Gizli katman ve çevrim- veri kümesi ağınızdaki etkinleştirme arasında BatchNorm katmanı ekleyin. BatchNorm ile ve olmadan 0.01, 0.05 ve 0.1 öğrenme oranlarında çalışın. BatchNorm, vanilya ağının farklı olduğu yüksek öğrenme oranlarında istikrarlı eğitim sağlaması gerekir.

4. Erken durdurma uygulayın: her dönem deneme kaybını takip edin, en iyi ağırlıkları koruyun ve test kaybı 20 dönem boyunca iyileşmediyse durdurun. 1000 dönem için düzenli ağ çalıştırın. Hangi dönem en iyi test doğruluğu olduğunu ve kaç hesaplama dönemini kurtardığınızı bildirin.

5. LayerNorm vs RMSNorm'ı 4 katlı ağda karşılaştırın (sadece 2 değil). Her ikisini de aynı ağırlıklarla başlatın. 200 dönem boyunca çalıştırın ve ilk katlıktaki son doğruluk, eğitim hızı (zaman başına) ve gradient büyüklüklerini karşılaştırın. RMSNorm'un aynı doğrulukla daha hızlı olduğunu kontrol edin.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Overfitting | "Model memorized the data" | When a model's training performance significantly exceeds its test performance, indicating it learned noise rather than signal |
| Regularization | "Preventing overfitting" | Any technique that constrains model complexity to improve generalization: dropout, weight decay, normalization, augmentation |
| Dropout | "Random neuron deletion" | Zeroing random neurons during training with probability p, forcing redundant representations; equivalent to training an ensemble |
| Weight decay | "L2 penalty" | Shrinking all weights toward zero by subtracting lambda * w at each step; penalizes complexity through weight magnitude |
| Batch normalization | "Normalize per batch" | Normalizing layer outputs across the batch dimension using batch statistics during training and running averages during inference |
| Layer normalization | "Normalize per sample" | Normalizing across features within each sample; batch-independent, used in transformers where batch size varies |
| RMSNorm | "LayerNorm without the mean" | Root mean square normalization; drops the mean subtraction from LayerNorm for 10% speedup with equal accuracy |
| Early stopping | "Stop before overfit" | Halting training when validation loss stops improving; the simplest regularizer, often used alongside others |
| Data augmentation | "More data from less" | Transforming training inputs (flip, crop, noise) to increase effective dataset size and force invariance learning |
| Generalization gap | "Train-test split" | The difference between training and test performance; regularization aims to minimize this gap |

## Daha fazla okumak

- Srivastava et al., "Dropout: Neural Networks'in Aşırı Uygunluktan Korunması İçin Basit Bir Yolu" (2014) -- Ensemble interpretasyonu ve kapsamlı deneyler ile orijinal bırakma kağıdı
  Srivastava 等人,Dropout: a way to prevent neural network overadaptation (2014) 原始 dropout 论文,包含集成解释和大量实验
- Ioffe & Szegedy, "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift" (2015) -- BatchNorm ve eğitim prosedürünü, en çok alıntılanan derin öğrenme makaleleri arasında bir tanesi olarak tanıttı
  Ioffe & Szegedy, 批归归一化:通过减少内部协变量偏移加速深度网络训练(2015) 引入BatchNorm 及其训练过程,深度学习中最引用的论文之一
- Zhang & Sennrich, "Root Mean Square Layer Normalization" (2019) -- RMSNorm'un LayerNorm doğruluğuna az hesaplama ile eşleştiğini gösterdi; LLaMA ve Mistral tarafından kabul edildi
  Zhang & Sennrich,                                                                                                                                                                                                                                                            
- Zhang et al., "Deep Learning Understanding Requires Rethinking Generalization" (2017) - nöral ağların rastgele etiketleri ezberleyebileceğini gösteren önemli bir makale, genelleşme hakkında geleneksel görüşlere meydan okuyarak
  Zhang 等人, anlamak derin öğrenme yeniden düşünme ihtiyacı 2017里程碑论文,证明神经网络可以记忆随机标签,挑战传统泛化观点
