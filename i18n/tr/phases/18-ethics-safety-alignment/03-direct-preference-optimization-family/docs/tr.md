# Doğrudan Tercihleri Optimizasyon Ailesi

> Rafailov et al. (2023) RLHF'nin optimumu tercih verileri açısından kapalı bir biçime sahip olduğunu gösterdi, bu nedenle açık ödül modelini atlayabilir ve politikayı doğrudan optimize edebilirsiniz. Bu anlayış bir aile doğurdu  IPO, KTO, SimPO, ORPO, BPO  her biri DPO'nun başarısızlık modunu düzeltti. 2026 yılında, doğrudan uyum algoritmaları, PPO'dan daha fazla sınır sonrası antrenman yolculuğu gönderir. Ama 2. Dersin aşırı optimize eğri hala geçerlidir: DAA'lar Goodhart'tan kaçmazlar, sadece ısırık olduğu yere hareket ederler.

> **【中文解读】**Bu bölüm doğrudan tercih optimizasyonu (DPO) ailesinin önerleme modelini doğrudan tercih veri eğitimi RLHF alternatif programından ￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼

> **【拓展：DPO 家族 → 现代 AI 训练】**2026 yılında, doğrudan bir algoritma ile karşılaştırıldığında PPO'nun daha fazla ön kenarlık sonrası eğitimde yerleştirilmesi. Ancak 2. Dersin aşırı optimize eğilimi hala uygulanmaktadır.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, six-variant preference-loss comparator) | **语言:** Python（标准库，六种变体偏好损失比较器）
**Prerequisites:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (Reward hacking), Phase 10 · 08 (DPO basics) | **前置知识:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (奖励黑客), Phase 10 · 08 (DPO 基础)

>  **【前置】**学本节前 Lütfen önce öğrenin:Fase 18·01-02(InstructGPT+古德哈特) 、Fase 10·08(DPO 基础) ・・・DPO 家族 = 绕过显式奖励模型直接从偏好数据训练――
>  **【类比】**DPO = "hakimiyet yargıçını ortadan kaldır"──RLHF = 訓練裁判(奖励模型) + 訓練选手优化裁判评分;DPO = 直接用比赛结果;;DPO = 直接用比赛结果;;DPO = 直接用比赛结果;;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO = 直接用比赛;DPO/KTO = 直接用比赛;PTO = 直接改进的投资;O/KTO/KTO/SimPO;OTO/ORPORP = ORPO = ORPO = ORPO = ORPO = ORPO = 改进修 DPO 不同缺陷;2026 DAA;D的算法) 直接对比 PPO: 直接对比 PPO 实施的策略; 更多;但古德的规则是对比 PPO 改改改改改;但古德的规则是改改改改改改;
**Time:** ~75 minutes | **时间:** ~75 分钟

## Öğrenme hedefleri

- DPO kapalı formunu RLHF-KL-optimum'dan çıkarın.
  Çin Çeviri: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışmalar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar: Çatışlar Çatışlar: Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatışlar Çatış
- DPO'daki her bir IPO, KTO, SimPO, ORPO, BPO düzeltmesinin başarısızlık modunu belirtin.
  Çinçe Çevirimi:说明 IPO、KTO、SimPO、ORPO、BPO 分別修复了 DPO'nun hangi başarısız modelini.
- "İplak ödül boşluğu" ile "Öncelik gücü" arasında fark yapın ve IPO'nun kimlik haritasının neden önemli olduğunu açıklayın.
  Çinçe çevirisi:区分"隐式奖励差"和"偏好强度", açıklamak neden IPO'nun恒等映射 çok önemli.
- Rafailov et al. (NeurIPS 2024) açık bir RM olmamasına rağmen DAAs'ın aşırı optimize olduğunu neden kanıtladığını açıklayın.
  Çeviri: Rafailov 等人(NeurIPS 2024) DAA'yı kanıtlıyor

## Sorunlar. Sorunlar.

RLHF amacı (Desin 1):

> RLHF 目標(Lection 1):

```
max_pi E_{x,y~pi} [ r(x, y) ] - beta * KL(pi || pi_ref)
```

bilinen bir en iyisi vardır:

> En iyi çözüm var .

```
pi*(y|x) = (1/Z(x)) * pi_ref(y|x) * exp(r(x, y) / beta)
```

Yani ödül, optimum politika ile referans oranı ile bilinçli olarak tanımlanır:

> Bu nedenle ödül oranı en iyi strateji ile referans stratejisi tarafından tanımlanmıştır:

```
r(x, y) = beta * log(pi*(y|x) / pi_ref(y|x)) + beta * log Z(x)
```

Bunu Bradley-Terry tercih olasılığı ve partisyon fonksiyonuna değiştirin .`Z(x)`Sadece `x`. Geride kalan tek politika parametrelerinde bir kayıp  ödül modeli gerekmiyor.

> Bradley-Terry'nin bu işlevi için bir payı var.`Z(x)`Sadece buna bağlı.`x`Ve ödemesi. Geri kalanı ise saf strateji parametrelerinin kaybı işlevi.

Korkusu: Kökülme, en iyisini elde edilebilir olduğunu varsayır, tercih verileri dağıtım içindedir ve referans politikası gerçek mod ankeri. Bunlardan hiçbiri tam olarak geçerli değildir.

> 问题在于:推导假设最优可达,偏好数据分布内,参考策略是真正点. 问题在于:推导假设最优可达,偏好数据分布内,参考策略是真正点. 问题在于:推导假设最优可达,偏好数据分布内,参考策略是真正点.

## Konsepten bir şey.

> **【中文解读】**RPO'nun önerisi:RLF 目標有已知最优解 pi*((DH y y y y x) = (1(x)) * pi_ref(y y y y x) * exp((r(x,y) / beta)  ödül, en iyi strateji ile referans strateji oranı karşılığı için gösterilmiştir, Bradley-Terry 偏好,配分函数 Z(x) çünkü sadece x'e bağlıdır ve geriye kalanı sadece strateji parametrelerinin kayıp işlevi, gereksiz ödül modelilerdir.

### DPO (Rafailov et al., 2023)

```
L_DPO = -log sigmoid(
  beta * log(pi(y_w | x) / pi_ref(y_w | x))
  - beta * log(pi(y_l | x) / pi_ref(y_l | x))
)
```

Yanlış giden ne olabilir:

> Sorun olabilir:

- - Ödül boşluğu .`beta * (log(pi/pi_ref)_w - log(pi/pi_ref)_l)`Küçük bir tercih keyfiyle büyük bir boşluk oluşturabilir.
  Çinçe Çevirimiçi: Hid式奖励差无界──微小偏好可产生任意大的差──
- Kayıp sürücüler seçilen ve reddedilen log-probları karşı yönde hareket ettirir. Seçilen mutlak log-probı reddedilen daha hızlı düşerse aşağıya itirebilir. Bu, Degraded Chosen Response fenomeni.
  Çinçe çevirisi: Kalanın kaç sayısal olasılığı karşı yönde.
- Paylaştırılmamış tercihler (kuşkusuz nadir nadir çiftler vs. nadir nadir çiftler) keyfi anlamda bilinçli ödüller üretir.
  Çevre dışı tercihler herhangi bir gizli ödül elde eder.

> **【拓展：IPO → DPO 的边界控制】**IPO(Identity Preference Optimization) olarak log-sigmoid, preference farkı ile değiştirilen恒等 haritalama ile, preference farkı 1/(2*beta) 封顶 olarak çözülmüştür.

### Açıklama (Azar et al., 2024)

Kimlik Tercihi Optimizasyonu, log-sigmoid'i tercih olasılığı üzerindeki kimlik haritasıyla değiştirir. Kayıp sınırlı bir hedefte bir kare hatası haline gelir:

> IPO'nun bu şekilde bir log-sigmoid, bir öndelik farkı ile değiştirilmesi DPO'nun temel sorunu çözüldü.

```
L_IPO = (log(pi(y_w | x) / pi_ref(y_w | x)) - log(pi(y_l | x) / pi_ref(y_l | x)) - 1/(2 beta))^2
```

Marjinin sınırları `1/(2 beta)`-Prifesyon gücü ve içten ödül farkı orantılıdır.

> 边界被 `1/(2 beta)`封顶── 偏好强度与隐式奖励差成正比──不会爆炸──

> **【拓展：KTO → 无配对数据训练】**KTO (Kahneman-Tversky Optimization) anahtar yenilik, yapılara tamamen boyun eğmek, sadece "ideal" veya "ideal olmayan" bir çıkış için tek bir işaret gerektirir. Bu büyük ölçüde kullanılabilir eğitim verilerinin kapsamını genişletti.

### KTO (Ethayarajh et al., 2024)

Kahneman-Tversky Optimizasyon, çiftlik yapısını tamamen düşürür. Tek bir etiketlenmiş çıkış ve ikili bir "istiği" veya "istiği olmayan" sinyal verildiğinde, bir prospek teorisi kullanımı için haritası yapar:

> KTO  tamamen yapısal ilişkileri terk eder.

```
v(x, y) = sigma(beta * log(pi(y|x) / pi_ref(y|x)) - z_ref)
```

Fayda: çiftsiz verileri kullanabilirsiniz, bu çok daha boldur.

> Kâr ve Kayıp kullanımının farklılıkları vardır.

> **【中文解读】**SimPO, referans stratejisini kaldırdı, uzunluk birleştirme ile sayıları benzerliğiyle değiştirdi, ayrıca kenarlıklı gamma  sabitliği eğitimi yaptı. Bu doğrudan DPO'nun uzunluk birleştirme biçimini çözdü. Daha uzun bir y_w yapısal olarak daha büyük bir sayı olasılığı farkı oluşturdu. ORPO daha da yoğunlaştı: standart SFT'lerin NLL'lerine tercih edilen programları eklemek, tek aşamada temel modelden eğitimden tam bir model olarak BPO'nun "degradasyon seçim tepkisi" sorunu tespit etti.

### SimPO (Meng et al., 2024)

Basit Seçenek Optimizasyonu eğitim sinyali ile jenerasyonu uyumlu hale getirir. İpucu politikasını tamamen kaldırın ve uzunlukla log olasılığını normalleştirin:

> SimPO, sinyalleri eğitmek ve üretmek için tamamıyla kaldırmak için bir referans stratejisi, uzunluğu ile birleştirmek için bir dizi benzerliği:

```
L_SimPO = -log sigmoid(
  (beta / |y_w|) * log pi(y_w | x)
  - (beta / |y_l|) * log pi(y_l | x)
  - gamma
)
```

bir kenara sahip`gamma`Uzunluk normallendirme DPO'nun uzunluk-bias başarısızlık modunu kullanma teşvikini ortadan kaldırır (daha uzun `y_w`Yapım yoluyla daha büyük bir log-prob boşluğu verir).

> Üzerine`gamma`稳定训练――长度归结消除了利用 DPO 长度偏见失败模式的激励(更长的 长度归结消除了长度归结的激励的激励`y_w`构造性地产生较大的对数概率差)

### ORPO (Hong et al., 2024)

Odds-Ratio Preference Optimization, standart SFT negatif kayıt olasılığına bir tercih terimi ekler:

> ORPO, SFT 负 karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı

```
L_ORPO = L_NLL(y_w) + lambda * L_OR
L_OR = -log sigmoid(log(odds(y_w) / odds(y_l)))
```

Referans politikası yok  SFT terimi düzenleyici. Üssü modelden uyumlu modeline tek bir aşamada tren. Ayrı bir SFT kontrol noktası yoktur.

> 无参考策略SFT 项就是正则化器──单阶段从基础模型训练到对齐模型──无需单独的SFT 检查点──

### BPO (ICLR 2026 başvurusu, OpenReview id=b97EwMUWu7)

Degraded Selected Response sorunu belirler: DPO sıralamayı korur `y_w > y_l`Ama mutlak log-prob `y_w`BPO, seçilen cevapta aşağıya doğru hareketleri cezalandıran tek satırlı bir düzeltme ekler. Llama-3.1-8B-DPO'ya göre matematik akıl yürütme konusunda +10.1% doğruluk rapor edildi.

> BPO 识别了"退化选择响应" sorunu:DPO 保持 `y_w > y_l`排序但 `y_w`Bu nedenle, bu durumun daha da yaygınlaşması için, bu durumun daha da yaygınlaşması için, bu durumun daha da yaygınlaşması için, bu durumun daha da yaygınlaşması için, bu durumun daha da yaygınlaşması için, bu durumun daha da yaygınlaşması için, bu durumun daha da yaygınlaşması için, bu durumun daha da yaygınlaşması için, bu durumun daha da yaygınlaşması için, bu durumun daha da yaygınlaşması için, bu durumun daha da yaygınlaşması için, bu durumun daha da yaygınlaşması için, bu durumun daha da daha da yaygınlaşması için, bu durumun daha da daha da fazla bir neden olduğu durumun ortaya çıkması için, bu durumun daha da daha da fazla bir neden olduğu durumun ortaya çıkması için, bu durumun daha da daha da iyi bir nedenine sahip olduğu durumun daha da daha da daha da iyi hale geleceği için, bu durumun daha da daha da iyileşmesi için, bu durumun daha da daha da iyi bir nedenine göre, daha da daha da daha da iyi bir sonuç sağlanabilir.

> **【拓展：DAA 过度优化 → 通用防御】**Rafailov 等人(NeurIPS 2024) çok sayıda veri kümesi ve KL  bütçesinde DPO、IPO、SLiC  stratejisi eğitimi. Gerçek ödüller KL'nin eğilimi ile Gao  et alı gibi ön-üstün-üstün-üstün biçimlerde ortaya çıkmaktadır.

### Evrensel sonuç: DAA'lar hala aşırı optimize

Rafailov et al. "Direct Alignment Algorithms'te Ödül Modelinin Aşırı Optimizasyonu için Ölçekleme Kanunları" (NeurIPS 2024) DPO, IPO, KL bütçelerindeki birden fazla veri kümesi üzerine politika eğitimi aldı. Altın ödülleri vs. KL eğrilikleri aynı Gao et al. zirve ve çöküş şekline sahiptir.

> Raphailov  et al. birçok veri kümesi ve KL  bütçesinde DPO 、IPO 、SLiC  stratejisi üzerinde eğitim gördüler. Gerçek ödüller KL'nin eğilimi ile Gao  et al. ile aynı ileri ve aşağı biçimlerde ortaya çıktı.

DAAs Goodhart'tan kaçmaz. "Önemli olarak optimize edilen ödül modeli"nden "Önemli olarak optimize edilen referans politika oranı"na geçiyor.

> DAA'nın eski bir kuraldan kaçmadığı belirtilmiştir. Sadece " ödül modeli aşırı optimize edilmesinden" "reference strategy ratio over optimization" (reference strategy ratio over optimization) olarak yüzey saldırıları gerçekleşmektedir.

> **【中文解读】**2026 yılının yöntem seçimi yöntemi: there is a large proportion of preference data → DPO(保守 beta) or SimpPO(((if there is a length bias); there is a non-pair of二元反 → KTO; wanting single-stage pipeline → ORPO;DPO 日志

### Seçimler (2026)

- Büyük çiftli tercih verileriniz varsa: DPO, koruyucu beta ile, SimPO uzunluk kayıtsızlığı belirginse.
  Çinçe çevirisi: There is a large proportion of preference data → DPO(保守 beta), if there is a lengthitude bias using SimPO。
- Eğer çiftsiz ikili geri bildiriminiz varsa: KTO.
  Çinçe Çevirimiçi:有非配对二元反 → KTO。
- Eğer bir basamak modelesinden tek aşamalı bir boru hattı istiyorsanız: ORPO.
  Çinçe Çevirimiçi: want from基础模型的单阶段管线 → ORPO。
- Eğer DPO kayıtlarında seçilmiş kayıt araştırmalarının bozulduğunu görürseniz: BPO.
  Çinçe Çevirim:DPO 日志中看选择概率下降 → BPO。
- Eğer tercih güçleri çok farklı ve DPO doymuşsa: IPO.
  Çin dilinde: 偏好强度变化大且 DPO 和 → IPO。

Her laboratuvar beş tane de bir pille çalışır ve her görev için kazananı seçer.

> Her laboratuvar her yöntemle aynı yöntemin en iyi olduğunu düşünmeye gerek yok.

> **【拓展：DPO 家族实践 → 方法选择】**2026 yılında her ön kenar laboratuvarı tüm yöntemlerde tekrar görev seçimi ile sonuçlandı. Matematik düşünce ve güvence için en iyi yöntemin aynı olduğunu düşünmeye gerek yoktur.

## Çerçeveyi kullanın.
```figure
dpo-margin
```

## Kullan

`code/main.py`Oyuncak tercih verisi, gerçek tercih gücü çiftlere göre değişir. Her kayıp, küçük bir softmax politikası ile aynı 500 çift örneğine göre optimize edilir.

> `code/main.py`Seçim ve güçlüğe değişen oyuncaklar verileri üzerinde altı kayıp karşılaştırın.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-preference-loss-selector.md`. Verita set istatistikleri (bir çiftle eşleşmemiş, değişkenle eşleşmiş tercih gücü, uzunluk dağılımı) ve bir hedef (tek aşama veya SFT-den sonra tercih) göz önüne alındığında, tercih kaybını önerin ve bu durumun önüne geçirilmesi gereken başarısızlık modunu bildirin.

> 本课产 出 `outputs/skill-preference-loss-selector.md`◊ belirlenmiş veri kümesi statistiği (department vs. nonpartment, variable vs. average preference strength, length distribution) ve hedef (sadece bir aşama veya SFT-sonra preference), tercih kaybını öneriyor ve koruma başarısızlık modelini rapor ediyor.

## Egzersizler.

1. Çık .`code/main.py`. DPO ve BPO için son seçilen kayıt sorgu düşüşünü bildirin. BPO seçilen mutlak olasılıkları daha yüksek tutmalıdır  bunu doğrulayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ Rapor DPO ve BPO'nun son seçim oranı oran oranı düştü.

2. Bu nedenle, bu iki yöntemin en güçlü olanı ve en düşük dereceli olanını belirtmek için, bir çiftin aynı kuvvetli olmasını sağlayan bir preferans verisini değiştirin.
   Çinçe Çevirisi: Değişiklik tercih verileri tüm görevi güç seviyesini etmektedir.

3. Yönülmüş yanıtları seçileninden ortalama 2 kat daha uzun yapın.
   Çinçe çevirisi:使拒绝响应平均比选择响应长 2倍──不改变其他东西,数值显示 DPO的长度利用和 SimPO的修复──

4. Rafailov et al. (NeurIPS 2024) DAAs'ın aşırı optimize olduğunu iddia ediyor. Tek nokta bir versiyonu üretmek: plan seçilen-minus reddedilen KL farklılığı ve büyük beta'da DPO'da aşırı optimize gözlemlemek.
   NeurIPS 2024) DAA 过度优化──复现单点版本:绘制选择减拒的 KL 散度,观察 DPO 在大贝塔时的过度优化──

5. BPO kağıdı özetini okuyun (OpenReview b97EwMUWu7).`code/main.py`- Evet .
   Çeviri: BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BPO'nun BLOCK'unun BLOCK'unun BLOCK'unun BLOCK'unun BLOCK'unun BLOCK'unun BLOCK'unun BLOCK'unun BLOCK'unun BLOCK'unun BLOCK'unun BLOCK'unun BLOCK'unun BLOCK'unun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'nun BLOCK'N BLOCK'N BLOCK BLOCK'N BLOCK'N BLOCK BLOCK'N BLOCK BLOCK'N BLOCK`code/main.py`İçinde gerçekleştirilen doğrulama:

## Anahtar Terimler

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| DPO | "RLHF without a reward model" / "没有奖励模型的 RLHF" | Loss derived from the closed-form RLHF optimum; policy parameters only / 从闭式 RLHF 最优解推导的损失；仅策略参数 |
| Implicit reward | "the log-ratio" / "对数比率" | `beta * log(pi(y\|x) / pi_ref(y\|x))` — the DPO-implied reward / DPO 隐含的奖励 |
| IPO | "bounded DPO" / "有界 DPO" | Replaces log-sigmoid with identity; implicit reward gap capped by `1/(2 beta)` / 用恒等映射替换 log-sigmoid；隐式奖励差距被 `1/(2 beta)` 封顶 |
| KTO | "unpaired DPO" / "非配对 DPO" | Prospect-theory utility over single labels with loss aversion / 带损失厌恶的单标签前景理论效用 |
| SimPO | "reference-free DPO" / "无参考 DPO" | Length-normalized log-likelihood + margin; no reference policy / 长度归一化对数似然 + 边际；无参考策略 |
| ORPO | "one-stage DPO" / "单阶段 DPO" | NLL + odds-ratio preference term; trains from base model in one pass / NLL + 胜率比偏好项；单阶段从基础模型训练 |
| BPO | "chosen-preserving DPO" / "保留选择的 DPO" | DPO plus a penalty for decreasing the chosen response's absolute log-prob / DPO 加上降低选择响应绝对对数概率的惩罚 |
| Degraded Chosen | "chosen goes down" / "选择概率下降" | DPO decreases chosen log-prob so long as rejected falls faster / DPO 降低选择对数概率只要拒绝下降更快 |
| DAA | "direct alignment algorithm" / "直接对齐算法" | Any preference-loss method that skips an explicit RM / 任何跳过显式 RM 的偏好损失方法 |

## Daha fazla okumak

- [Rafailov et al. — Direct Preference Optimization (NeurIPS 2023, arXiv:2305.18290)](https://arxiv.org/abs/2305.18290)
  Çeviri:Rafailov 等人DPO 原始论文
- [Azar et al. — A General Theoretical Paradigm to Understand Learning from Human Preferences (AISTATS 2024, arXiv:2310.12036)](https://arxiv.org/abs/2310.12036) Açıklama
  Çeviri:Azar 等人IPO 论文
- [Ethayarajh et al. — KTO: Model Alignment as Prospect Theoretic Optimization (arXiv:2402.01306)](https://arxiv.org/abs/2402.01306)
  Çeviri:Ethayarajh 等人KTO 论文
- [Meng, Xia, Chen — SimPO (NeurIPS 2024, arXiv:2405.14734)](https://arxiv.org/abs/2405.14734)
  Çeviri:Meng 等人 SimPO 论文
- [Hong, Lee, Thorne — ORPO (EMNLP 2024, arXiv:2403.07691)](https://arxiv.org/abs/2403.07691)
  Çeviri:Hong 等人 ORPO 论文
- [BPO — Behavior Preservation Optimization (ICLR 2026 OpenReview b97EwMUWu7)](https://openreview.net/forum?id=b97EwMUWu7)
  Çin Çeviri:BPO   davranışlarını iyileştirmek
- [Rafailov et al. — Scaling Laws for RM Overoptimization in DAAs (NeurIPS 2024, arXiv:2406.02900)](https://arxiv.org/abs/2406.02900)
  Çeviri:Rafailov 等人 DAA 过度优化缩放定律
