# talimat-Aynlaşma sinyal olarak takip etmelerini göstermek için uyarı izlemek için uyarı

> RLHF'nin sonraki eleştirileri bu boru hattına karşı çıkıyor. Optimize basıncının bir vekili nasıl çarpıttığını incelemeden önce, vekili görmeniz gerekir. InstructGPT (Ouyang et al., 2022) referans mimarisini tanımladı: talimat- yanıt çiftlerinde denetimli ince ayarlama, çiftlik tercih sıralamaları üzerinde eğitilmiş bir ödül modeli ve SFT politikasına KL cezası ile ödül modeli karşı PPO. 1.3B InstructGPT, 175B GPT-3'e tercih edildi. Bu tek sonuç 2026 yılında her sınır laboratuvarının hala RLHF şeklinde bir eğitim sonrası boru hattı göndermesinin nedeni.

> **【中文解读】**InstructGPT(Ouyang 等人, 2022) birbiriyle ilgili bir referans yapı tanımladı: 1) SFT'yi denetleme; 2) ödüllendirme modeli, ödüllendirme sırasıyla eğitime hazırdır; 3) KL'yi cezalandırmakla birlikte ödüllendirme modeline karşı PPO'yu.

> **【拓展：RLHF → 现代 AI 对齐】**RLHF (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (RHF) (R) (RHF) (RHF) (R) (RHF) (R) (R) (RHF) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R)

>  **【前置】**学本节前 Lütfen önce bil:Fase 10·06(SFT 监督微调)、Fase 10·07(RLHF)、Fase 10·08(DPO)  anlamak Üç aşama 齐管线的技术细节──本节是Fase 18 开篇,工程视角审视对齐后续 29 节都基于此基础──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy three-stage pipeline) | **语言:** Python（标准库，玩具三阶段管线）
**Prerequisites:** Phase 10 · 06 (SFT), Phase 10 · 07 (RLHF), Phase 10 · 08 (DPO) | **前置知识:** Phase 10 · 06 (SFT), Phase 10 · 07 (RLHF), Phase 10 · 08 (DPO)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Öğrenme hedefleri

- InstructGPT borusunun üç aşamasını ve her birinde kullanılan kayıpları belirtin.
  Çinçe Çevirimi:                                                                                                                                                                                                                                                            
- 1.3B talimat uyarlanmış bir modelin insan tercih değerlendirmesinde çiğ 175B GPT-3'yi neden yendiğini açıklayın.
  Çinçe Çevirimi: 1.3B İnstrukçonu Modelle İnsan tercihleri değerlendirmesinde orijinal 175B GPT-3'yi neden yendiğini açıklayın.
- 3. aşamada KL cezasının neyden koruduğunu ve neden kaldırılması mod aramak davranışına neden düştüğünü açıklayın.
  Çinçe Çevirim: açıklama Üçüncü aşama KL  ceza korumak nedir, ve neden kaldırılması model çöküşe neden olur.
- Düzeltme vergisi ve PPO-ptx azaltma Ouyang et al.
  Çinçe Çevirimiçi: Description对齐税以及 Ouyang 等人使用的PPO-ptx 缓解方法──

## Sorunlar. Sorunlar.

Önceden eğitimli dil modelleri metni tamamlar. Sorulara cevap vermezler. GPT-3'e "listayı tersine çeviren bir Python fonksiyonu yaz" diye sorarsanız, genellikle bir başka istek alırsınız, çünkü eğitim dağıtımının çoğu daha fazla web metni ile devam eden web metni.

> 预训语言模型补充全文,而不是回答问题――让 GPT-3 "写一个反转列表的Python 函数",你经常会得到另一个提示词,因为训练分布中大多数是继续生成更多网页文的网页内容――模型在完成它的工作只是这个工作是错的――

Bu durumun çözülmesi için kullanılan bir vekil, insan tercihidir. İki tamamlama bir değerlendiriciye gidiyor; değerlendirici daha iyi birini seçer; ödül modeli değerlendiriciyi öğrenir.

> Bu sorunun tam olarak çözülmesi için kullanılan her ciddi laboratuvar, insan tercihlerinin temsilcisi olarak kullanılır. İki tamamlayıcı değerlendiriciler; değerlendiriciler daha iyi seçerler; ödüllendirme model öğrenme değerlendiricileri olarak kullanılır.

## Konsepten bir şey.

### 1. aşama: denetim altında ince ayarlama (SFT)

İyi niyetli bir insan tarafından yazılacağı yanıtların yanıtlandığı çabuk cevap çiftlerini toplayın. Ouyang et al. etiketçilerden ve OpenAI API'den 13k çağrıları kullandı. Standart çapraz entropi kaybı ile bu verilere dayalı temel modelde ince ayarlama yapın.

> 收集提示-响应,其中响应是一个善意的标志者会写的内容──Ouyang 等人, bu verileri kullanarak 标志者和 OpenAI API's 13k 提示词──标准交叉损失在这个数据上微调基础模型──

SFT'nin size verdiği: model şimdi soruları devam etmek yerine cevaplar.

> SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT size: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: SFT: S: SFT: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S: S:

> **【中文解读】**SFT 阶段使模型 from"补全文本"转向"回答问题",but cannot provide about many rationale answers中哪个更好的信号──RM 阶段 use Bradley-Terry 成对偏好损失 L_RM = -log sigmoid(r(x,y_w) - r(x,y_l)) 标志者排序的补对上训奖励模型──RM genellikle SFT 模型初始化并替代 LM 头为标量头,6B 就足指导 175B 模型──

### İkinci aşama: Ödül modeli (RM)

SFT modelinden K tamamlamalarını örnekleyin. Bir etiketlemeci onları sıralar.`y_w`- Hayır .`y_l`- ...

> SFT modelinden K 个补全――标注者对它们排序――训练一个奖励模型对任何提示-响应对打分,使对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对对`y_w`优于                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `y_l`Çözüm:

```
L_RM = -log sigmoid(r(x, y_w) - r(x, y_l))
```

Bu Bradley-Terry çiftlik tercih kaybı. RM genellikle SFT modelinden başlangıç yapılır ve LM başı skalar başıyla değiştirilir.

> Bu Bradley-Terry'nin RM'de bir öne çıkmasıdır.

Ödül modelleri küçüktür: 175B InstructGPT için 6B yeterliydi.

> Ödül modelleri çok küçük: 6B'nin 175B'nin ÖnderlikGPT'sini yönlendirmek için yeterli.

> **【拓展：PPO 阶段 → RLHF 的核心工程】**PPO 阶段的目标函数 J(pi) = E[r(x,y) ] - beta * KL(pi de pi_SFT) Maksimum ödüllendirme aynı zamanda strateji SFT yakın tutmak için  KL 系数 beta en önemli RLHF 超参数太低导致奖励黑客,太高则 SFT 上无改进──没有 KL 项,优化器发现的是 RM 从未见过的对抗样本分数高不是因为人类真正偏好,而是因为 RM 从未评估过这些输入──

### 3. aşama: KL cezası ile PPO

Hedef tanımlanın:

```
J(pi) = E_{x~D, y~pi(.|x)} [ r(x, y) ] - beta * KL(pi(.|x) || pi_SFT(.|x))
```

PPO ile maksimum artırın.`pi`Bu nedenle, bu sistemin en iyi yönleri, SFT politikasından uzaklaşmaktan uzaklaşmaktır.

> PPO en fazla kullanmak KL 项保持 `pi`SFT 策略 çok uzak. Yoksa, optimizer RM'de karşı karşı örnekler  aşağı puan yüksek bir karakter satırı bulacaktır, çünkü RM onları hiç görmedi, insan gerçek tercihleri değil.

KL katılamı `beta`Bu, RLHF'nin en önemli hiperparametresidir. Çok düşük: ödül hackeri. Çok yüksek: SFT'ye karşı hiçbir gelişme yok.

> KL'de bir sayı var .`beta`Bu, RLHF'nin en önemli 超参数──太低:奖励黑客──太高:相比 SFT 没有改进──

> **【中文解读】**ÖZÜTÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜNÜN

### Düzeltme vergisi

RLHF'den sonra, model insan tarafından tercih edilir, ancak standart referans değerlerinde (SQuAD, HellaSwag, DROP) geri döner. Ouyang ve diğerleri buna uyum vergisi derler ve bunu PPO-ptx ile düzeltirler: RL hedefine önceden eğitim gradiyentlerini karıştırın, böylece model, hiçbir zaman ödüllendirilmediği aşağıdaki görevleri nasıl yapacağını unutmaz.

> RLHF 后, model insan tercihlerinde daha iyi ama standart基准larda (SquAD, HellaSwag, DROP) 上退步。Ouyang 等人 olarak adlandırılan "对齐税" ve PPO-ptx 修复 will pre-training gradient mix into RL 目标, so model does not forget never been rewarded 下游任务。

```
J_ptx(pi) = J(pi) + gamma * E_{x~D_pretrain} [ log pi(x) ]
```

PPO-ptx standart haline geldi. Anthropic, DeepMind ve Meta hepsi bazı çeşitleri kullanıyor.

> PPO-ptx 成为标准──Antropik、DeepMind 和 Meta 都使用某种变体──

> **【拓展：1.3B vs 175B → 对齐独立于能力】**1.3B InstructGPT, işaretçinin tercihlerine yaklaşık %70'lik bir zaman kazanır. 175B GPT-3¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

### Sonuç

1.3B InstructGPT (SFT + RM + PPO-ptx) etiketleyiciler tarafından 175B taban GPT-3'e göre yaklaşık %70 tercih edilir.

> 1.3B'nin InstruktGPT(SFT + RM + PPO-ptx) %70'lik bir süre içinde etiketlenmiş tercihlerin 175B'nin temelinde GPT-3'den daha iyi olduğu belirtilmiştir.

1. Düzeltme, kapasiteye göre farklı bir eksendir. 175B modeli daha fazla kapasiteye sahipti; 1.3B modeli daha fazla düzeltme sahipti; etiketçiler düzeltmeyi tercih etti.
   Çinçe çevirisi: 齐是与能力不同轴──175B 模型有更多能力;1.3B 模型有更多对齐;标注者偏好对齐的那个──
2. Ürün modelinin kapasiteden kurduğu zemin, bir temel modelin görmediği gerçekleri bilmesine izin veremezsin.
   Çinçe Çevirisi:能力下限由基础模型设定──你不能通过RLHF 让基础模型知道它从未见过的事实──

> **【拓展：Phase 18 后续课程 → 每个都在攻击此管线】**Sonraki derslerin her eleştirisi bu hattın bir bölümünde bulunur: Ödüllendirme黑客(Dosma 2) saldırı aşaması 2,DPO(Dosma 3) birleşim aşaması 2 ve 3,CAI(Dosma 5) insan işaretleyicisini değiştirmek,(Dosma 4) gösterilen işaretleyicinin önyargılı olduğunu gösterir, hazırlıklı taklit ederek(Dosma 9) gösterim stratejisi tamamen aşılmasıdır 3.

### Bu neden 18 aşama için bir referans noktası?

Sonraki derslerdeki her eleştiris  ödül hackeri (Desin 2), DPO (Desin 3), sikofans (Desin 4), CAI (Desin 5), uyku ajanları (Desin 7), uyum sahteliği (Desin 9)  bu boru hattının bir kısmına karşı tartışmaktadır. Ödül hack saldırıları 2. aşama. DPO 2. ve 3. aşamaları çöküyor. CAI insan etiketleyicisini değiştirir. Sykophancy etiketlemeci taraflı bir sinyal olduğunu gösterir. Düzeltme sahteliği, politika'nın 3. aşamayı tamamen yönlendirebileceğini göstermektedir. Bu eleştirileri önce kafanın içine sokmadan takip edemezsin.

> 后续课程中的每一个批评奖励黑客(Dos 2)、DPO(Dos 3)、(Dos 4)、CAI(Dos 5)、潜伏代理(Dos 7)、对齐伪装(Dos 9)都在攻击此管线的某部分中──奖励黑客攻击第二阶段──DPO 合并第二和第三阶段──CAI 替换人类标记者──展示标记者是有偏见信号──对齐伪装展示策略可以完全绕过第三阶段──如果没有先在脑内这个管线,就无法理解这些批评──

## Çerçeveyi kullanın.
```figure
al-instruct-pipeline
```

## Kullan

`code/main.py`Oyuncak tercih verileri üzerinde üç aşamayı simüle eder. Temel "politik" eylemlere karşı tarafsız bir maden. STAGE 1 SFT, 200 çağrıda etiketleme işlemini taklit eder. İkinci aşamada, 500 çiftlik sıralamadan bir Bradley-Terry ödül modeli uygulanıyor. 3. aşamada, SFT politikasına KL cezası ile basitleştirilmiş bir PPO güncelleme yapılır. Ödül artışını, KL farklılıklarının artışını ve politika sürümünü izleyebilirsiniz ve KL terimini kapatarak 50 güncelleme adımında ödül hackeri görünmesini görebilirsiniz.

> `code/main.py`Oyuncak tercihleri verilerinde üç aşama üzerinde simülasyon yapılır. Basis "taktiği" hareket {A, B, C} üzerinde olan bir partiyel para.[1] Aşama 1 SFT 模拟标志者 200 提示上の動作。 aşama 2 500 成成对排序中拟合布拉德利-テリー 奖励模型。 aşama 3 运行带有 KL 惩罚的简化PPO 更新。

Neye bakılır:

观察要点:

- Ödül yolculuğu `beta = 0.1`vs `beta = 0.0`- Evet .
  Çeviri:`beta = 0.1`vs `beta = 0.0`Ödül yolları:
- Bu nedenle, eğitim adımları hakkında bilgi almak için daha fazla bilgi edinmek gerekir.
  Çinçe Çevirisi: training步骤中 KL(pi  pi_SFT) 变化──
- Son eylem dağılımı etiketleme tercihine göre.
  Çinçe Çevirimiçi: Final动作分布与标注者偏好的比较──

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-instructgpt-explainer.md`RLHF boru hattı açıklaması veya kağıt özetini göz önüne alarak, üç aşamaldan hangisinin değiştirildiğini, her aşamada hangi kaybın kullanıldığını ve KL cezası veya eşdeğer düzenleyici olup olmadığını belirler.

> 本课产 出 `outputs/skill-instructgpt-explainer.md` RLHF 管线描述或论文摘要, üç aşamada hangisinin değiştirildiğini belirler, her aşamada hangi kaybı işlevi kullanılır ve KL 惩罚或等效正则化器是否存在──

## Egzersizler.

1. Çık .`code/main.py`- Yapılandır .`beta = 0.0`200 PPO adımından sonra eylem dağılımını rapor edin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Yapılandırma`beta = 0.0`Ve 200 adımlık PPO'nun ardından hareket dağılımını rapor etmektedir.

2. Ödül modelini değiştirerek, eylem B için +0.5 önyargısı (sümüle edilen ödül hatası) oluşturun.`beta = 0.1`KL cezası politikaların önyargıyı kullanmasını engeller mi?`beta`sömürü görülebilir mi?
   Çinçe Çevirim: Modify ödül modeli makes动作 B 有 +0.5 偏置(模拟奖励 bug) 』用 `beta = 0.1`运行 PPO──KL 惩罚能否阻止策略利用偏置?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `beta`- Değerli kullanımı görülebilir mi?

3. Ouyang et al. (arXiv:2203.02155) Resim 1. Etiketçi-Öncelik eğriyi 1, 5, 20, 100 adım boyunca PPO çalıştırarak ve SFT modeli ile karşılaştırarak öncelik ölçerek yeniden üretin.
   Çinçe Çevirimi:阅读 Ouyang 等人(arXiv:2203.02155)图 1──通过运行PPO 1、5、20、100 步并测量对SFT 模型的偏好来复现标志者偏好曲线──

4. Gazete'nin 4.3 Bölümü, 1.3B InstructGPT'nin 175B GPT-3'yi yaklaşık %70'i üzerinde geçirdiğini bildirir.
   Çinçe Çevirimi: Dergi Bölüm 4.3 Rapor 1.3B InstructGPT yaklaşık %70'te 175B GPT-3'yi yendi. Neden gizli üretim önerilerindeki oran, etiketleme yapanın kendi önerilerinden daha yüksek?

5. Aynı tercih verileri üzerine PPO kaybını DPO (Fase 10 · 08) ile değiştirin. Nihai politika sürekliliğini (KL ile SFT) ve nihai ödülü karşılaştırın. Hangi yöntem eşleşen ödülde daha fazla sürekliliği gösterir?
   Çin Çeviri: DPO'yu aynı tercih verileri üzerinde kullanmak için DPO'yu değiştirmek için 10 · 08) aşama.

## Anahtar Terimler

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| SFT | "instruction tuning" / "指令微调" | Stage 1: cross-entropy fine-tune on prompt-response pairs / 阶段 1：在提示-响应对上交叉熵微调 |
| Reward model | "the RM" / "奖励模型" | Scalar regressor over (prompt, response) trained with Bradley-Terry on pairwise labels / 用 Bradley-Terry 在成对标签上训练的标量回归器 |
| Bradley-Terry | "pairwise preference loss" / "成对偏好损失" | -log sigmoid(r_w - r_l); reduces pairwise ranking to binary classification / 将成对排序简化为二分类 |
| KL penalty | "the regularizer" / "正则化器" | `beta * KL(pi \|\| pi_SFT)` — keeps the RL policy near the SFT anchor / 保持 RL 策略接近 SFT 锚点 |
| PPO-ptx | "PPO with pretraining mix" / "带预训练混合的 PPO" | Adds a fraction of pre-training log-likelihood to the PPO objective to offset the alignment tax / 将部分预训练对数似然加入 PPO 目标以抵消对齐税 |
| Alignment tax | "the RLHF regression" / "RLHF 退步" | Post-RLHF drop on standard benchmarks that RLHF did not target / RLHF 后在未针对的标准基准上的性能下降 |
| Labeler preference | "the ground truth" / "地面真实" | Sample of human rankings; the RM is a statistical proxy for this, not for "human values" / 人类排序的样本；RM 是其统计代理，而非"人类价值观" |

## Daha fazla okumak

- [Ouyang et al. — Training language models to follow instructions with human feedback (arXiv:2203.02155)](https://arxiv.org/abs/2203.02155) ardından gelen her RLHF boru hattının temeli olan InstructGPT kağıdı
  Çinçe Çevirim:Ouyang  et al InstructGPT 论文, bundan sonra her RLHF 管线的基础
- [Stiennon et al. — Learning to summarize from human feedback (arXiv:2009.01325)](https://arxiv.org/abs/2009.01325) RLHF-for-summarization'ın öncesi
  Çevirim:Stiennon 等人RLHF
- [Christiano et al. — Deep reinforcement learning from human preferences (arXiv:1706.03741)](https://arxiv.org/abs/1706.03741) orijinal tercih tabanlı RL formülasyonu
  Çinçe Çevirimiçi:Christiano 等人                                                                                                                                                                                                                                                         
- [Bai et al. — Training a Helpful and Harmless Assistant with RLHF (arXiv:2204.05862)](https://arxiv.org/abs/2204.05862) Anthropic'in InstructGPT borusunun HH uzantısı
  Çinçe Çevirimi:Bai  et al  Antropik                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
