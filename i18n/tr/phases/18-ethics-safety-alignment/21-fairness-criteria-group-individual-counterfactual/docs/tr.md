# Adalet kriterleri  Grup, bireysel, sahte 

> Adalet edebiyatını üç aile düzenliyor. Grup adilliği: demografik eşitlik, eşit olasılıklar, koşullu kullanım doğruluğu eşitliği  korunan gruplar arasında ortalama eşit oranlar. Bireysel adillik (Dwork et al. 2012): benzer bireyler benzer kararlar alır; karar haritasında Lipschitz durumu. Gerçeklere karşı adillik (Kusner et al. 2017): Hissedici özellikler karşıt bir şekilde değiştirildiğinde değişmezse bir karar birey için adil olacaktır. 2024 teorik sonucu (NeurIPS 2024): CF vs. doğruluk içeren bir değişim vardır; bir model-agnostik yöntem, optimal ama haksız bir tahminciyi sınırlı doğruluk kaybı olan CF'ye dönüştürür. Geriye doğru geriye doğru doğrular (arXiv:2401.13935, Ocak 2024): yasal olarak korunan özellikler üzerinde müdahale gerekmesinden kaçınan yeni bir paradigma. Felsefi uzlaşma (ICLR Blogposts 2024): sebepli grafikler ile, belirli grup adalet önlemlerini tatmin etmek karşı gerçek adaleti içerir.

> **【中文解读】**Bu bölüm, eşitlik prensiplerini tanıtır.  Grup adilliği, bireysel adillik ve gerçek karşıtı adillik tanımları ve ölçümleri.

> **【拓展：不可能定理 → 公平性冲突】**Chouldechova / Kleinberg-Mullainathan-Raghavan (Kleinberg-Mullainathan-Raghavan, 2017): nüfusa eşitlik ̇ eşitsizliğin oranı ve koşulların kullanımı doğruluk oranı eşitsizliğin temel oranında aynı anda karşılanamaz. Bu bir matematik sonucu, bir tasarım sınırlaması değil.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-criteria comparison) | **语言:** Python（标准库，三标准比较）
**Prerequisites:** Phase 18 · 20 (bias), Phase 02 (classical ML) | **前置知识:** Phase 18 · 20 (偏见), Phase 02 (经典 ML)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Öğrenci bölümün öncesinde öğrenmek için:Fase 18·20(偏见) Fase 02(klasik ML) 、因果推断基础──公平性三大家族──
>  **【类比】**公平 = "AI'nin doğruluğu 天平"──群体公平(demografik eşitlik/eşitli oranlar) = 平均上各组别结果相等;个体公平(Durum 2012) = 相似个体得相似决策;反事实公平(Kusner 2017) = 改变敏感属性决策不变──三者不能同时满足选择是政策决定──
> NeurIPS 2024:CF-vs-Düzgünlük İçinde bir ağırlık var, ama bir sınır kaybı dönüşüm yöntemi var.

## Öğrenme hedefleri

- Grup adaletinin üç kriterini (demografik eşitlik, eşitliğe sahip oranlar, koşullu kullanım doğruluğunun eşitliği) ve bir imkansızlık sonucu belirtin.

> Açıklama üç grup eşit standartlar (population equality, median equalization, conditions of use, precision rate, median) ve bir imkansız sonuç.

- Dwork et al. 2012 Lipschitz formülü ile bireysel adalet tanımlayın.

> 描述通过 Dwork 等人 2012年 Lipschitz 公式定义的个体公平──

- Karşı gerçeklik adilliği ve nedensel grafik bağımlılığı anlatın.

> 描述反事实公平及其因果图依赖──

- Geriye doğru geriye doğru karşılıkları ve müdahale ile korunan özellik sorunu neden kaçınılması gerektiğini açıklayın.

> ☐ Antakyaların neden korunan özelliklere müdahale edilmesini engellediğini açıklamak

## Sorun . Sorun .

Ders 20 tarafsızlığı ölçmekle ilgiliydi. Ders 21 ölçüm hizmet etmesi gereken adillik standardını tanımlamakla ilgiliydi. Üç aile yapısal olarak farklı standartlar verir.

> Ders 20 ölçüm önyargısı hakkında. Ders 21 ölçüm hizmetlerinin adil standartlarını tanımlamakla ilgili.

## Konsep kavramı.

> **【中文解读】**群体公平三大标准: 群体公平三大标准: 群体平权P(Y=1 whereA=a) = P(Y=1 whereA=a) = P(Y=1 whereY*=y,A=a) = P(Y=1whereY*=y,A=a) = P(Y=1whereY*=y,A=a'), 群体真阳性率和假阳性率等等等; 条件使用准准率均等等P(Y*=yY=y,A=a) = P各Y(*=yY=y,A=a'),

### Grup adilliği

- **Demographic parity.**P\Y=1\A=a=P\Y=1\A=a') tüm gruplar için.
- **Equalized odds.**P  Y=1  Y*=y, A=a) = P  Y=1  Y*=y, A=a') gruplar arasında eşit TPR ve FPR.
- **Conditional use accuracy equality.**P\Y*=y\Y=y, A=a) = P\Y*=y\Y=y, A=a\') gruplar arasında eşit tahminsel değer.

> Halk oranı  grupların kabul oranı  grupların eşitlik oranı  grupların gerçek                                                                                                                                                                                                                                                   

İmkansızlık (Chouldechova, Kleinberg-Mullainathan-Raghavan 2017): Bu üçü eşit olmayan temel oranlarda aynı anda tatmin edilemez.

> İmkansız bir karar: eşitsizlik temelli oranı altında bu üçü aynı anda karşılanamaz.

### Kişisel adalet

Dwork et al. 2012. Bir karar haritası f, belirli bir Lipschitz sabit L için bireysel olarak adil bir görev-spesifik benzerlik metrikine d if (f(x) - f(x') <= L * d(x, x') göre benzer kararlar alır.

> Dwork 等人 2012──decision mapping f Eğer bir Lipschitz 常数 L 满足 f  x) - f  x') da <= L * d  x, x'), ise görev için belirli benzerlik ölçüsü d  bireysel adil── benzer bireysel benzerlik kararları elde eder

D. Politik soru, istatistik değil.

> 需要定义 d.Bu bir politika sorunu, istatistik bir sorudur.

> **【拓展：反事实公平 → 因果图依赖】**Kusner 等人(2017) 's anti-facts fairness: Input modelinde, bireyin hassas özellikleri anti-facts değişmesi sonrası karar değişmezse, karar bu birey için adil olacaktır.

### Gerçeklere karşı adillik

Kusner et al. 2017. Bir karar birey için karşıt olarak adil olur i eğer, nüfusun nedensel bir modeli altında, karar değişmez i hassas özellikler karşıt olarak değiştirildiğinde.

> Kusner  et al. 2017 ⋅ Enfo modelinde, bireyin hassas özellikleri gerçeklere karşı değişirken karar değişmezse, karar bu birey için gerçeklere karşı adil olacaktır.

Bir sebepçi DAG gerektirir. DAG bir model seçeneği. Karşıt gerçeklik adillik sadece DAG kadar haklı.

> 需要因果 DAG──DAG 是建模选择──反事实公平的合理性取决于DAG的合理性──

### CF vs. Düzgünlik karşılığı

NeurIPS 2024 teorik: karşıt gerçeklik ve tahminsel doğruluk arasında doğuştan bir değişim vardır. Bir model-agnostik yöntem, sınırlı bir doğruluk maliyetinde, optimal ama haksız bir tahminciyi CF'ye dönüştürebilir.

> NeurIPS 2024  teorik sonuç: Antfakta açıklığı ve tahmin doğruluğu arasında sabit bir ağırlık vardır.

### Geriye dönme karşı faktörleri

ArXiv:2401.13935 (Ocak 2024): Geleneksel karşı faktörler hassas özelliğe müdahale gerektirir  "Bu kişi farklı bir cinsiyet olsaydı karar değişir miydi". Hukuki olarak, bu sorunlu: korunan özelliğe sınıflandırma yasasında müdahale edilmez.

> 傳統反事實需要在敏感属性上干預法律上有問題──反事實反反轉方向: 傳統反事實需要在敏感属性上干預法律上有問題──反事實反轉方向: 傳統反事實反事實反事實反干預: 傳統反事實反事實反事實反干預,而不是屬性干預,而非結果反推理──法律异议──

Geriye doğru karşı faktörler yönünü tersine çeviriyor: özelliğe müdahale etmek yerine, bireyin gerçek özelliklerinin hangi kombinasyonunun karşı faktör sonuçları doğurduğunu sorun. Bu yasal itirazın önüne geçiyor.

> Geriye dönmek gerçeklere karşı bir özellik değildir, tersine bireyin gerçek özelliklerinin hangi birleşimleri gerçeklere karşı bir sonuç doğuracağını sormakla ilgilidir.

> **【中文解读】**哲学调和(ICLR Blogposts 2024): 因果图后,满足某些群体公平度就含反事实公平──三家族不是正交的,而是相同的底层因果结构的不同面向──这是没有解决不可能的定理──不平等基础率仍阻止同时群体公平), ancak "grup" ve "个体/反事实" arasındaki yüzey karşılığı kısımlarının, belirgin bir neden modeli oluşturduğu varsayım olmadığından ortaya çıkmıştır──

### Felsefi uzlaşma

ICLR Blogposts 2024. Bir sebep grafikini elinde tutarak, belirli grup adalet önlemlerini tatmin etmek karşı gerçek adalet gerektirir.

> ICLR 2024: Sonuç çizgisinden sonra, bazı grupların eşitliğinin ölçümünü yerine getirmek, gerçek adilliği içerir.

Bu, imkansızlık teoremlerini çözmez (eşitsiz temel oranlar hala aynı anda grup adilliğini engeller). Ancak "grup" ve " bireysel / kontrafaktal" arasındaki görünen muhalefetin kısmen sebep model hakkında açık olmayan bir eser olduğunu gösterir.

> Bu çözüm imkansız teorik değildir, ancak "grup" ve "şehit/karşı gerçek" arasındaki yüzey karşılığı bir bölümün belirgin bir neden modeli oluşturduğu varsayımlar olmadığından ortaya çıkarılmıştır.

### Bu 18 fazaya uygun.

Ders 20 tarafsızlık ölçümü. Ders 21 adillik tanımlaması. Ders 22 gizlilik (farklı gizlilik). Ders 23 su işaretlemesi. Bunlar, aldatma ile bitişik dersleri tamamlayan tahsisle ilgili dersler 7-11.

> Ders 20 is bias见测量──Lesson 21 is fair definition──Lesson 22 is privacy──Lesson 23 is waterprint── bunlar dağıtım ile ilgili derslerdir, dolandırıcılık ile ilgili derslerdir──

> **【拓展：CF vs 准确性权衡 → 实际影响】**NeurIPS 2024  teorik sonuç: Antista fact open ve prediction accuracy arasında sabit bir ağırlık vardır. Model inkognition yöntemleri en iyi ama adil olmayan bir tahminciyi CF  adil olarak dönüştürebilir, ancak doğruluk kaybı, adil olmayan bir tahminci içinde hassas özellikler fektörünün büyüklüğüne bağlıdır. Bu, adil standartların seçilmesi anlamına gelir.

## Kullanın Kullanın
```figure
an-fairness-trilemma
```

## Kullan

`code/main.py`Bu, bir oyuncakın duyarlı bir özelliği ve eşit olmayan temel oranları olan ikili sınıflandırma verileri oluşturur. Demografik eşitliği, eşitliğe sahip oranları ve koşullı kullanım doğruluğu eşitliğini basit bir sınıflandırıcıda hesaplayın. Üç ölçüyü birbirinden farklı olarak gözlemleyin. Demografik eşitlik için yeniden ağırlık uygulayın ve diğer iki maliyetini gözlemleyin.

> `code/main.py` Duygusal özellikler ve eşitsizlik oranı temelinde oyuncaklar iki sınıfı veri kümesi oluşturdu.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-fairness-criterion.md`. Adalet iddiası veya politikası göz önüne alındığında, hangi kriterin talep edildiğini, modelin iddia edilen eşitsiz temel oranlar altında kalan kriterleri karşılayabileceğini ve iddia hangi sebepli DAG'den bağlı olduğunu belirler.

> 本课产 出 `outputs/skill-fairness-criterion.md` Düzgünlük ifadeleri veya politikaları belirlemek, hangi standartları belirlemek, eşitsizlik temelli oranında diğer standartları karşılamak ve belirlenen sonuçları belirlemek.

## Egzersizler.

1. Çık .`code/main.py`. Öntanımlı veriler üzerinde üç grup ölçüsünü rapor edin. Demografik eşitlik hedefli yeniden ağırlama ve yeniden raporlama uygulayın.

2. Hissetisiz özellikler üzerinde L2 kullanarak Dwork et al. 2012 bireysel adillik ölçüsünü uygulayın. Lipschitz'i sürekli L=1 ile kaç çift ihlal ettiğini bildirin.

3. Kusner et al. 2017'yi okuyun. Başlangıç notları için basit iki özellikli bir sebepli DAG oluşturun ve içerdiği karşı gerçeklik-eğenlik koşulunu belirleyin.

4. 2024'te geriye doğru geriye doğru karşı faktörler makalesi korunan özelliklere müdahaleden kaçınır.

5. ICLR 2024 uzlaşması, grup ve karşı gerçek adilliği aynı yapının yönleri olduğunu savunuyor.`code/main.py`ve onları eşdeğer kılan sebepçi varsayımı belirtin.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Demographic parity | "equal rates" | P(Y=1 | A=a) equal across groups |
| Equalized odds | "equal TPR/FPR" | Equal true-positive and false-positive rates across groups |
| Conditional use accuracy | "equal PPV/NPV" | Equal predictive values across groups |
| Individual fairness | "Lipschitz condition" | Similar individuals get similar decisions |
| Counterfactual fairness | "causal alteration invariance" | Decision unchanged under counterfactual attribute alteration |
| Backtracking counterfactual | "explain via actuals" | Counterfactual reasoned backward from outcome, not forward from attribute |
| Impossibility theorem | "the three conflict" | Chouldechova / KMR 2017: group criteria mutually exclusive under unequal base rates |

## Daha fazla okumak

- [Dwork et al. — Fairness through Awareness (arXiv:1104.3913)](https://arxiv.org/abs/1104.3913) bireysel adalet
- [Kusner, Loftus, Russell, Silva — Counterfactual Fairness (arXiv:1703.06856)](https://arxiv.org/abs/1703.06856) karşı gerçek adillik
- [Chouldechova — Fair prediction with disparate impact (arXiv:1703.00056)](https://arxiv.org/abs/1703.00056) imkansızlık
- [Backtracking Counterfactuals (arXiv:2401.13935)](https://arxiv.org/abs/2401.13935) Korunmuş özellikler ile ilgili yeni bir paradigma
