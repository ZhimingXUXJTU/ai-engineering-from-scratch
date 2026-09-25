# CLIP ve Kontrast Görüş Dil Eğitimleri

> OpenAI'nin CLIP (2021) projesi, önümüzdeki beş yıl boyunca güç sağlayacak kadar büyük bir fikir olduğunu kanıtladı: Sadece gürültülü web görüntü başlık çiftlerini kullanarak bir görüntü kodleyicisi ve bir metin kodleyicisini aynı vektör alanına doğru birleştirmek ve kontrast kaybı. - Null denetim etiketi. 400 milyon çift. Sonuçta yerleştirme alanı sıfır çekim sınıflandırma, görüntü metni kurtarma ve görme kule olarak her 2026 VLM'ye bağlanır. SigLIP 2 (2025) softmax' ı sigmoid ile değiştirdi ve daha düşük maliyetle CLIP' i geçti. Bu ders, InfoNCE'den sigmoid çiftlik kaybına kadar matematik yürür ve stdlib Python'da eğitim adımını inşa eder.

> **【中文解读】**CLIP, 400 milyon net resim karşılığı ile, karşılaştırma kaybı ile resim ve metin aynı boyutlu alanına kodlandıracak.

> **【拓展：CLIP→多模态大模型】**CLIP'in resimleri karşılaştırma öğrenimi LLaVA、BLIP-2 ve diğer çok modoldaki büyük modellerin temelini oluşturur. CLIP'i anlamak, tüm çok modoldaki AI yaşamının başlangıcı noktasını anlamak demektir.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, InfoNCE + sigmoid loss implementations) | **语言:** Python（标准库，InfoNCE + sigmoid 损失实现）
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 7 (Transformers) | **前置知识:** Phase 12 · 01（ViT patch），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**学本节前 Lütfen önce bil:Fase 12·01(ViT Fotoğrafı Çıkarma Yapıştırma;Fase 11·04(Embeddings 向量空間概念);Fase 7(Transformer 自注意力)。本节核心数学是软max + 交叉,Fase 7·04 有详细推导──
>  **【类比】**CLIP 訓練 = "中外文词典配对游戏"── 32k için(şekil, açıklama), model öğrencilerinin her resmini ve kendi açıklamasını vektor alanının aynı yerine çekmesine izin versin, diğer 31999 张图片的描述推開── eğitimden sonra, model "bir kedi fotoğrafı" ve gerçek kedilerin resimlerini birlikte çekmesine izin verir.

## Öğrenme hedefleri

- Karşılıklı bilgi ile InfoNCE kaybını çıkarın ve sayısal olarak sabit vektörlü bir sürüm uygulayın.
  Çinçe çevirisi: 互信息推导 InfoNCE 损失,并实现数值稳定的向量化版本──
- Sigmoid çiftlik kaybının (SigLIP) toplam üst maliyetli softmax talepleri olmadan 32768+ partiye neden ölçeğini açıklayın.
  Çinçe Çevirimi: açıklama neden sigmoid 成对损失 (sigLIP) 32768+ 批次大小,而无需软max 所需的全部集成 开销――
- Metin şablonları oluşturarak sıfır çekim ImageNet sınıflandırmasını çalıştır (`a photo of a {class}`) ve argmax' ı cosine benzerliği yerine alıyor.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Ç Ç Ç Ç Ç Ç`a photo of a {class}`)并对余弦相似度取 argmax 来运行零样本 ImageNet 分类──
- CLIP / SigLIP öncesi eğitiminin size verdiği dört kaldırağı isimlendirin: parti boyutu, sıcaklık, istek şablonu, veri kalitesi.
  Çinçe Çevirimiçi:列举 CLIP / SigLIP 预训给你四杆:批次大小、温度、提示模板、数据质量──

## Sorunlar. Sorunlar.

Pre-CLIP vizyonu denetlendi. Etiketlenmiş veri kümelerini toplayın (ImageNet: 1.2M görüntüler, 1000 sınıf), bir CNN'yi eğitiniz, gönderin. Etiketler pahalı, etiketler etiketlercilerin anlaşabildiği şeylere kaygı duyulur ve etiketler ince ayarlama olmadan yeni görevlere aktarılmaz.

> CLIP 之前的视觉是监督式的──收集标签数据集(ImageNet:120万张图像,1000 个类别), CNN eğitimi,部署──标签昂贵,标标标偏向标标志者能达成共识的内容,而且标标不通过微调就无法迁移到新任务──标标标的偏向标志者能达成共识的内容,而且标标不通过微调就无法迁移到新任务──标标的偏向标志者能达成共识的内容,而且标标不通过微调就无法迁移到新任务──标标的偏向标标标的偏向标标标的偏向标标标的共识的内容,而且标不通过微调就无法迁移到新任务──标标的微调就无法迁移到新任务──标标的内容.

Resim başlıklı web, bir milyardan fazla serbest etiketli çiftleri ücretsiz olarak içerir. Alt metinde "köpeğim Max parkta" yazılı bir altın retriever resmi bir denetim sinyali taşır.

> İnternette ücretsiz olarak kullanılabilir olan 1 milyartan fazla yayılmış etiketleme resimleri bulunmaktadır. Bir altın mavi avcı köpeğinin fotoğrafı alt metin ile birlikte "My Dog Max in the Park" adlı bir izleme sinyali taşıyor.

CLIP'in cevabı: Resim-başlık çiftlerini eşleştirme görevi olarak ele alın. N resim ve N başlıklı bir parti verildiğinde, N-1 dikkat dağıtıcılarına karşı her resmini kendi başlıklarına eşleştirmeyi öğrenin. Gözetim "bu iki şey bir araya gelmektedir; bu N-1 yapmaz".

> CLIP'in cevabı: görsel uyumlu görevlere çizim yapmaktır. N-1 ıntılıksızlık programında öğrenilen N-1 ıntılıksızlık programında her bir resim kendi tanımına uyumlu olacaktır.

Sonuçta yerleştirme alanı CLIP'in eğitilmesinden daha fazlasını yapar. ImageNet sıfır çekim çalışmaktadır çünkü "bir kedinin fotoğrafı" açıkça kedilerle etiketlenmemiş kedilerin resimlerinin yanına yerleştirilmiştir.

> 得到的嵌入空间超越了CLIP'in eğitim hedefi──ImageNet 零样本分类有效,因为"bir kedinin fotoğrafı" hiç açıkça işaretlenmemiş bir kedinin kedinin resmini yakınında yerleştirilmiştir──

## Konsepten bir şey.

> **【中文解读】**CLIP(Tarif-İsmin karşılaştırmalı dil öncesi eğitim) karşılaştırma öğrenimi ile resim ve metin aynı boyutlu alanlara yerleştirilir: yakın mesafeye uygun resim, uzaktan uygun olmayan bir öne sürmek. CLIP 4 milyar resim üzerinde eğitimden sonra, sıfır çekim 画像分类, OpenAI çok modemlik kapasitesinin temel taşıdır.

> **【拓展：CLIP 的应用生态】**CLIP'in karşılaştırma öğrenme modeli büyük bir uygulama yaratmıştır:DALL-E 2/3 ile CLIP  yönlendirme görüntü üretimi,Stable Diffusion ile OpenCLIP  güvenli filtre olarak,LLaVA ile CLIP  görsel kodlayıcı bağlantı LLM 和图像理解──CLIP'in sıfır çekim 能力 on ImageNet                                                                                                                                                                                                                                                                                                                                                                                                                                               


> **【拓展：CLIP 的 zero-shot 能力】**CLIP'in en şaşırtıcı yeteneği sıfır çekim 分类 hiç aşağıya giden görevlerin eğitim verisi gerektirmez, sadece sınıf adı için bir görüntü ayırmak gerekir. ImageNet'te, CLIP ViT-L/14'in sıfır çekim 准确率ı ((76.2%) ResNet-50'in tüm denetim doğrulama oranına yakındır.


### Çift kodlayıcı

CLIP'in iki kulesi var:

> İki kule var.

- Resim kodlayıcı`f`: ViT veya ResNet, görüntü başına bir D-dim vektörü çıkarır.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`f`:ViT veya ResNet, her görüntü bir D 维向量
- Metin kodlayıcı`g`: küçük transformatör, başlık başına bir D-dim vektörü çıkarır.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`g`:小型 Transformer,每条描述输出一个 D 维向量──

İki kule de çıkışlarını birim uzunluğuna normalleştirir.`cos(f(x), g(y)) = f(x)^T g(y)`Her ikisi de birim normudur.

> İki tane çıkış birim olarak birleştirilmiştir.`cos(f(x), g(y)) = f(x)^T g(y)`Çünkü ikisi de birim ve boyut.

> ️ **【易错点】**忘归一化 (L2 normalize) on computation similarity → 向量模长大的样本天然有更大的点积,模型会偏向"长向量"而不是"语义匹配"──修复:每次前进 后必`f = f / ||f||`Sonra da hesapladım .`cos`- Evet.
> 🤔 **【困惑】**S: Neden 余弦 benzerliği 欧氏 mesafesini kullanmıyor? A: 余弦 sadece yönü görmez, "parlaklık farklı ama içerik aynı" resimleri için 鲁棒; 欧氏 mesafe yönlendirilir 量模长.

Bir parti için N (resim, başlık) çiftleri, benzerlik矩阵 oluşturun `S`şekli ile`(N, N)`- ...

> 对于一批 N 个图像,描述) 对,构建形状为 `(N, N)`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `S`- ...

```
S[i, j] = cos(f(x_i), g(y_j)) / tau
```

nerede`tau`öğrenilen bir sıcaklık (CLIP 0.07 olarak initializes; log- uzayda öğrenilen).

> İçlerinden `tau`Clip başlangıç 0.07 olarak öğrenilmektedir.

### InfoNCE Kayıpları

CLIP, satır ve sütunlar üzerinde simetrik çapraz entropi kullanır:

> CLIP için 列和列使用 için 交叉:

```
loss_i2t = CE(S, labels=identity)     # each image's positive is its own caption
loss_t2i = CE(S^T, labels=identity)   # each caption's positive is its own image
loss = (loss_i2t + loss_t2i) / 2
```

Bu InfoNCE. CE'deki yumuşak maksimum, her resmin batch'taki diğer tüm başlıklardan daha fazla başlıklarına uymasını zorlar. "Negatifler" diğer tüm batch öğeleri. Büyük batchlar = daha fazla negatif = daha güçlü sinyal. CLIP 32k batch'ta eğitilmiştir; ölçek önemlidir.

> İşte InfoNCE.CE'de yumuşak maksimum  Her bir görüntüyi kendi açıklamasıyla uyumlu olarak zorlamak, tüm diğer açıklamalardan daha yüksek bir şekilde negatif örnek olarak bütün diğer örnekleri batım tir.

> ️ **【易错点】**batch_size 太小(如 64) 训不出好 CLIP负样本太少,模型学不到"什么算真正的相似"──CLIP 原文 batch_size=32768 才有效果──如果你只能跑批量=256,要么要么要么要么要么 SigLIP(不需要大批量),要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要么要要要要么要么要么要要么要么要要要要要要么要么要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要要
>  **【类比】**InfoNCE 像"找卧底游戏":32k 张图片对应 32k 个描述, her resim bir sürü açıklama içinde kendi gerçek eşleşmesi bulmak gerekir.

### Temperatür

`tau`Bu nedenle, bu testler, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer testin en yüksek seviyesinde, bir diğer seviyesinde, bir diğer seviyesinde, bir diğer seviyesinde, bir diğer seviye olarak, bir diğer seviye olarak, bir diğer seviye olarak, bir diğer seviye olarak, bir diğer seviye olarak, bir diğer seviye olarak, bir diğer seviye olarak, bir diğer seviye olarak, bir diğer seviye olarak, bir diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviye olarak, diğer seviyeye olarak, diğer seviyeyeyeyeyeyeyeyeyeyeyeyeyeyeye, diğer seviyeyeyeyeyeyeyeyeyeye, diğer seviyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeye

> `tau`控制 softmax 的度──低 tau → 尖分布,具有难负例挖掘效果──高 tau → 平滑,所有样本都有贡献──CLIP 学习 log(1/tau),并剪剪以防止崩──SigLIP 2 固定初始 tau 并使用可学习的偏置替──

### Sigmoid neden daha iyi ölçekler (SigLIP)

Softmax bütün benzerlik matrisini senkronize ederek kullanır. dağıtılmış eğitimde her gömleği her kopyasına toplayıp sonra softmax yapmalısınız.

> Softmax  tüm benzerlik matçının eşleşmesi gerekir.

SigLIP softmax ' i elementli sigmoid ile değiştirir: her çift için `(i, j)`, kaybı "bu eşleşen çift mi?" ikili sınıf sınıflandırmasıdır.

> SigLIP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `(i, j)`, kaybı "Onlar uyumlu mu?" için bir iki sınıf.

> 🤔 **【困惑】**S: Neden softmax  needs all-gather and sigmoid  不需要?A: softmax 的分母是" tüm N2 个配对的相似度之和", her GPU 必须看到全部;sigmoid 只有看每个 (i,j) 配对独立判断是/否匹配,不依赖全局信息──多 GPU 训练时 sigmoid 损失可以本地计算后减少──
>  **【类比】**InfoNCE = "32k 選 1 選題", yapmak için tam bir 張卷子看必須; SigLIP = "32k 个判断题 (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

```
L = -1/N sum over (i, j) [ y_ij log sigmoid(S[i,j]) + (1-y_ij) log sigmoid(-S[i,j]) ]
```

`y_ij = 1`Eğer`i == j`Her GPU'nun yerel blok ve toplamlarını hesaplaması gerekir. SigLIP 2 32k-512k'lık bir seri olarak ucuz bir şekilde ölçebilir. CLIP'in nispeten daha fazla iletişim gerekecektir.

> `y_ij = 1`Eğer `i == j`, yoksa 0 ⋅ her bir parçacık kaybı bağımsız ⋅ her GPU'nun kendi bloklarını hesaplaması gerekebilir ⋅ SigLIP 2 düşük maliyetle 32k-512k ⋅ paketlere kadar genişleyebilir, CLIP ise daha fazla iletişim gerekebilir ⋅

### sıfır atış sınıflandırması

N sınıf adları verildiğinde, her sınıf için bir metin şablonu oluşturun:

> 给定 N 个类名称,为每个类构建文模板:

```
"a photo of a {class}"
```

Her şablonun metin kodlayıcıyla yerleştirilmesi. Resminizi resim kodlayıcıyla yerleştirin. Argmax cosine benzerliği = tahmin sınıfı. Hedef sınıfları üzerinde eğitim yok.

> Metin kodlayıcıyı her moduleye yerleştirmek için kullanın.

> ️ **【易错点】**Doğrudan kullan .`"cat"`作为提示 → 比 `"a photo of a cat"`差 10+ 个百分点──CLIP 训练时文本端看的描述大多是完整句子,单词作为提示会让分布偏移──修复:始终使用模板 `"a photo of a {class}"`Daha iyi bir şekilde.
> 🤔 **【困惑】**S: ImageNet 1000 类全算一遍文嵌入 不是很慢吗?A: 只算一次然后缓存──1000 个提示 在文本编码器里跑一遍(毫秒级),后面每张新图片只需要1次图像嵌入+1000 次余弦相似度(向量化矩阵乘)──

Hızlı şablonlar önemlidir. CLIP'in orijinal kağıdı sınıf başına 80 şablon kullanıyordu (sırın, sanatsal, fotoğraf, resim vb.) ve yerleşimleri ortalama olarak ölçüyordu. +3 ImageNet puanları. Modern kullanım tipik olarak bir veya iki şablon seçer.

> 提示模板很重要──CLIP 原始文每类使用80个模板(普通、艺术、照片、绘画等)并对嵌入取平均──ImageNet 上提升 3个百分点──现代用法通常选择一个两个模板──

### Düzsel araştırma ve ince ayarlama

ZERO-shot bir temel çizgidir. Bir çizgi zond (ziyaret sınıflarınız için dondurulmuş CLIP özelliklerinin üzerine bir çizgi katmanı hazırlayın) alan içindeki görevlerde sıfır çekimi yener. Tam ince ayarlama alan içindeki çizgi zondayı yener ancak sıfır çekim transferini etkileyebilir. Üç değişikliğe sahip üç rejim.

> 零样本是基线──线性探测;;在结的 CLIP特征之上为目标类训练一线性层) 域内任务上超越零样本──全量微调在域内超越线性探测,但可能损害零样本迁移──三种模式,三种权衡──

### SigLIP 2: NaFlex ve yoğun özellikler

SigLIP 2 (2025) şunları ekliyor:

> Siglip 2 ((2025) Ekle:

- NaFlex: tek model değişken boyut oranlarını ve çözünürlüklerini ele alır.
  Çinçe Çevirimi:NaFlex:单一模型处理可变宽高比和分辨率──
- Segmanlama ve derinlik tahminleri için daha iyi yoğun özellikler, VLM'lerde donmuş omurgan olarak kullanımı hedeflemiştir.
  Çinçe Çevirimiçi: daha iyi yoğun özellikler bölünme ve derinlik tahminleri için kullanılır, hedef VLM'de bir 结干主网络 olarak kullanılır.
- Çok dilli: CLIP'nin sadece İngilizce olduğu 100'den fazla dilde eğitim görmüştür.
  ÇINÇAN TRÜBLÜK:多语言: 在 100+种语言上训练,而 CLIP 仅限英文──
- 1B param ölçeğinde CLIP 400M'de en üst düzeye çıktı.
  Çinçe Çevirisi: 10 milyar parameter, CLIP en yüksek 4 milyar.

2026 açık VLM'lerde, SigLIP 2 SO400m/14 varsayılan görme kulesi olarak kalır. CLIP, belirli LAION-2B eğitim dağılımının sorgu örneğinize eşleştiği saf görüntü metin kurtarma için varsayılan olarak kalır.

> 2026 yılında açılan VLM'de, SigLIP 2 SO400m/14 öntanımlı görme kulesi. CLIP, özellikle belirli LAION-2B ı öğrenme modeline uygun şekilde dağıtma eğitimi aldığında, sadece inceleme sırasında öntanımlı bir seçimdir.

### ALIGN, BASIC, OpenCLIP, EVA-CLIP

ALIGN (Google, 2021): CLIP ile aynı fikir, 1.8B çift ölçek, 90% gürültülü. Sıkı gürültülü veri ölçekleri kanıtlanmıştır. OpenCLIP (LAION): CLIP'in açık yeniden üretimi LAION-400M / 2B, birden fazla ölçek, açılış kontrol noktası. EVA-CLIP: maskeli görüntü modelleme ile başlatır; VLM'ler için güçlü omurgan. BASIC: Google'ın CLIP+ALIGN hibrid. Hepsi aynı aile, farklı veriler ve ayarlama.

> ALIGN(Google,2021): CLIP ile aynı fikir,18 milyar büyüklüğüne,90% 噪音数据―― kanıtladı gürültü verileri genişletilebilir。OpenCLIP(LAION): LAION-400M / 2B'de CLIP 开放复现,多种规模,首选的开放检查点──EVA-CLIP:从掩码图像建模初始化;VLM'in强主干网络──BASIC:Google's CLIP+ALIGN 混合──都属于同一家族,不同的数据和调优──

### - Çatı sıfır çekim

CLIP sınıfı modeller, ImageNet sıfır çekiminin (CLIP-G, OpenCLIP-G) yaklaşık %76'sini kaplıyor. Bunun ötesinde çok daha büyük veri (SigLIP 2 %80'e ulaşır) veya mimari değişiklikleri (genergeleştirilmiş başlar, daha fazla parametreler) gerekmektedir.

> ImageNet 零样本分类上限76%dir.Bu seviyeye aşan CLIP 类模型, daha fazla veri gerektirir.

> 🤔 **【困惑】**Öğrenmek için bir bölümde soru sorulur: 1) CLIP'in sıfır çekimi neden GPT-4 gibi "Şekilde iki kişi ne yapıyor" anlamıyor?

## Çerçeveyi kullanın.
```figure
multimodal-fusion
```

## Kullan

`code/main.py`Uygulamaları:

> `code/main.py`实现了:

1. Oyuncak çift kodlayıcı (hash tabanlı görüntü özellikleri, metin grafik özellikleri) böylece InfoNCE şeklini numpy olmadan görebilirsiniz.
   Çinçe Çevirimiçi: bir oyunça iki kodlayıcı (Hashi'nin resim özelliklerine dayanarak), numpy gerekmiyor, hatta InfoNCE'nin biçimini görebilirsiniz.
2. Saf Python'da InfoNCE kaybı (log-sum-exp yoluyla sayısal istikrar).
   Çinçe çeviri: Pure Python 实现的 InfoNCE 损失((通过日志-总数-exp 实现数值稳定性)
3. Karşılaştırma için Sigmoid çiftlik kaybı.
   Çıxma: Sigmoid 成对损失用于对比.
4. sıfır çekim sınıflandırma rutin: bir dizi metin isteklerine karşı kosinus benzerliğini hesaplayın, tahmin için argmax.
   Çinçe Çevirimi:零样本分类例程:计算与一组文本提示的余弦相似度,argmax 得出预测──

Bu sayılar oyuncak, şekli gerçek bir CLIP eğitmeninin yaydığı ile eşleşir.

> 运行它并观察损失曲线──绝对数值是玩具级的;但形状与真实CLIP 训练机的输出匹配──

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-clip-zero-shot.md`. Bir görüntü kümesi (yol yoluyla) ve hedef sınıflar listesini göz önüne alarak, CLIP şablonu ile metin isteklerini oluşturur, her iki tarafı belirtilen bir kontrol noktasıyla yerleştirir (örneğin, `openai/clip-vit-large-patch14`), ve benzerlik puanları ile ilk-1 / ilk-5 tahminlerini gönderir.

> 本课产 出 `outputs/skill-clip-zero-shot.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                                        `openai/clip-vit-large-patch14`) iki tarafta yerleştirilmiş,并返回带有相似度分数的 top-1 / top-5 预测──该技能 绝对拒绝在提示列表中的类别做判断──

## Egzersizler.

1. 4 çiftli bir parti için InfoNCE'yi el ile uygulayın. 4x4 benzerlik matrisini oluşturun, softmax çalıştırın, diyagonalı seçin, çapraz entropi hesaplayın. Python uygulamasını bu el hesaplama ile doğrulayın.
   Çinçe çevirisi: 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 4 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書

2. SigLIP bir önyargı parametre kullanır `b`sıcaklıktan başka: `S'[i,j] = S[i,j]/tau + b`- Ne rolü var ?`b`Bir seri için olumlulardan çok olumsuz olan büyük bir sınıf dengesizliği olduğunda oynayın. SigLIP Bölümü 3'ü okuyun (arXiv:2303.15343).
   Çinçe Çevirimi:SigLIP temperature dışında de kullanılır`b`- ...`S'[i,j] = S[i,j]/tau + b`◊ büyük bir grupta büyük bir sınıf dengesizliği varsa,`b`起什么作用?阅读 SigLIP 第3节(arXiv:2303.15343)

3. Kediler ve köpekler için sıfır atış sınıflandırıcısı oluşturun.`a photo of a {class}`ve `a picture of a {class}`Test görüntülerinin 100'ü üzerinde doğruluğu ölçün. Şablonların ansamblının tek bir çarpması var mı?
   Çinçe Çevirisi: 构建猫狗零样本分类器──尝试两种提示模板:`a photo of a {class}`和 `a picture of a {class}`◊ 100 张测试图上测量准确率──模板集成单模板ten daha iyi midir?

4. 512-GPU çalıştırma için 32k partide softmax InfoNCE vs sigmoid iletişim maliyetini hesaplayın. Hangi ölçekler O(N), hangi O(N ^ 2) olarak? SigLIP Bölümü 4.
   Çin dilinde:计算 512 GPU、批次 32k 下softmax InfoNCE 与 sigmoid 成对损失的通信成本──哪个是 O(N),哪个是 O(N^2)?引用 SigLIP 第 4 节──

5. OpenCLIP ölçekleme yasaları kağıdını okuyun (arXiv:2212.07143, Cherti et al.). Verilerin ölçeklenmesi için sonuçlarını rakamlardan üretin: sabit model boyutunda, ImageNet sıfır çekim doğruluğu ile eğitim verileri boyutu arasındaki log-lineer ilişki nedir?
   Çinçe çevirisi: OpenCLIP 缩放定律论文 ({{lang-en:OpenCLIP}}) 阅读 arXiv:2212.07143,Cherti 等人) ⋅ Şekillerden alınan resimler, verilerin genişletilmesi hakkında şunları gösteriyor:

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| InfoNCE | "Contrastive loss" | Cross-entropy over a batch's similarity matrix; each item's positive is its paired item, negatives are everything else | 批次相似度矩阵上的交叉熵；每项的正样本是其配对项，负样本是所有其他项 |
| Sigmoid loss | "SigLIP loss" | Per-pair binary cross-entropy; no softmax, no all-gather, scales cheaply in distributed training | 逐对二分类交叉熵；无 softmax，无 all-gather，分布式训练中扩展成本低 |
| Temperature | "tau" | Scalar that scales logits before softmax/sigmoid; controls sharpness of the distribution | softmax/sigmoid 前缩放 logits 的标量；控制分布的锐度 |
| Zero-shot | "no-finetune classification" | Use text prompts to construct class embeddings and classify by cosine similarity; no training on target classes | 用文本提示构建类别嵌入，通过余弦相似度分类；无需在目标类别上训练 |
| Prompt template | "a photo of a ..." | Text scaffold around a class name; affects zero-shot accuracy by 1-5 points | 类别名周围的文本支架；影响零样本准确率 1-5 个百分点 |
| Dual encoder | "Two-tower" | One image encoder + one text encoder, outputs in shared D-dim space | 一个图像编码器 + 一个文本编码器，输出在共享的 D 维空间 |
| Hard negative | "Tough distractor" | A negative similar enough to the positive that the model has to work to separate them | 与正样本足够相似的负样本，模型需要努力区分它们 |
| Linear probe | "Frozen + one layer" | Train only a linear classifier on top of frozen features; measures feature quality | 仅在冻结特征之上训练线性分类器；衡量特征质量 |
| NaFlex | "Native flexible resolution" | SigLIP 2 capability to ingest images at any aspect ratio and resolution without resizing | SigLIP 2 以任意宽高比和分辨率输入图像的能力，无需调整大小 |
| Temperature scaling | "log-parametrized tau" | CLIP parametrizes `log(1/tau)` so gradients behave; clips to prevent collapse to near-zero tau | CLIP 参数化 `log(1/tau)` 使梯度行为正常；裁剪防止 tau 崩溃到接近零 |

## Daha fazla okumak

- [Radford et al. — Learning Transferable Visual Models From Natural Language Supervision (arXiv:2103.00020)](https://arxiv.org/abs/2103.00020)- CLIP kağıdı.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Zhai et al. — Sigmoid Loss for Language Image Pre-Training (arXiv:2303.15343)](https://arxiv.org/abs/2303.15343)Siglip.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) çok dilli + NaFlex.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Jia et al. — ALIGN (arXiv:2102.05918)](https://arxiv.org/abs/2102.05918) gürültülü web verileri ile ölçeklendirme.
  Çinçe Çevirisi: Using noise network data expand.
- [Cherti et al. — Reproducible scaling laws for contrastive language-image learning (arXiv:2212.07143)](https://arxiv.org/abs/2212.07143) OpenCLIP ölçekleme yasaları.
  Çeviri: OpenCLIP 缩放定律──
