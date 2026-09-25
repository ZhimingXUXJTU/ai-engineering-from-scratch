# Sim-Real Transfer gerçekte gerçekte taşındı.

> Hardware'da başarısız olan bir simülatörde eğitilen bir politika, simülatörü ezberleyen bir politikadır.

> **【中文解读】**Taklit makinede eğitim stratejisi gerçek donanım üzerinde çalışamıyorsa, taklit makinesine "çok uygun" olduğunu gösterir.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 08 (PPO), Phase 2 · 10 (Bias/Variance) | **前置知识:** Phase 9 · 08 (PPO), Phase 2 · 10 (偏差/方差)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Gerçek bir robot eğitimi yavaş, tehlikeli ve pahalıdır. Bir iki ayaklı yürümeyi öğrenmek için milyonlarca eğitim bölümünü alır; gerçek bir iki ayaklı donanımı parçaladığında bile düşen gerçek bir robot. Simülasyon size sınırsız yeniden ayarlamalar, belirleyici yeniden üretilebilirlik, paralel ortamlar ve fiziksel hasar olmaması sağlar.

> 訓練真足機械人慢、危險而昂── 訓練真足機械人慢、危險而昂── 訓練真足機械人需要数百万的训练回合才能学会走; 訓練真足機械人即便摔倒一次也可能损坏硬件── 訓練真足機械人慢、危險而昂── 訓練真足機械人需要数百万的训练回合才能学会走; 訓練真足機械人即便摔倒一次也可能损坏硬件── 訓練真足機械人即便摔倒一次也可能损坏硬件── 訓練真足機械人即便摔倒一次也可能损坏硬件── 訓練真足機械人即便摔倒一次也可能损坏硬件── 訓練真足機械人即便摔倒一次也可能损坏硬件── 訓練真足機械人即便摔倒一次也可能损坏硬件── 訓練真足機械即可重置無限的重置、 確定性可重現、 復行環境與零物理傷──

Simülatörler yanlış. Doldurmalar MuJoCo modellerinden daha fazla sürtünme sahiptir. Kameralar lens çarpıtmasına sahiptir. Simülatör içermez. Motorlar gecikmeler, tepki ve doymuşluklara sahiptir. Sim modellerinin% 99'u atlıyor. Rüzgar, toz ve değişken aydınlatma steril renderiye eğitilmiş bir politika sabote eder.**reality gap**Sim dağıtım ve gerçek dağıtım arasındaki sistematik fark robotlar için yerleştirilen RL'nin merkezi sorunu.

> Ancak simülasyon makineleri yanlışlıktır. Başı MuJoCo modelinden daha fazla çizik taşıyor. Fotoğraf makineleri simülasyon makineleri de dahil değildir. Elektrik makineleri, geçici                                                                                                                                                                                                                                         **现实鸿沟** Simile gerçek dağılım ve gerçek dağılım arasındaki sistematik farklar  Deployment机器人 RL'nin temel sorunudır.

* Sim-real dağıtım değişikliğine dayanıklı bir politika ihtiyacınız var. Üç tarihsel yaklaşım: simülatörü rastgeleleştirmek (domain rastgeleleştirilmesi), politikayı biraz gerçek veriyle uyarlamak (domain uyarlanması / ince ayarlama), veya gerçek sistemin parametrelerini tanımlamak ve onlarla eşleştirmek (sistem tanımlaması). 2026'da baskın reçete, üçü de büyük paralel simülasyonla birleştirir (Isaac Sim, Isaac Lab, Mujoco MJX GPU'da).

> You need a strategy for simulating to real distribution shifting. ̋3 different historical methods: ̋随机化 ̋ (Historik yöntem: ̋随机化 ̋) ̋ (Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik yöntem: ̋Historik ̋Historik ̋ (Historik ̋) ̋ (Historik ̋) ̋ (Historik ̋) ̋ (Historik ̋) ̋ (Historik ̋) ̋) ̋ (Historik ̋) ̋ (Historik ̋) ̋ (Historik ̋) ̋ (Historik ̋) ̋) ̋ (Historik ̋) ̋ (Historik ̋) ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋ ̋

> **【中文解读】**"现实沟"机器人 RL'nin çekirdek sorunulardır. Üç büyük çözüm: 1) Domen asymonization training time asymonization 随机化仿真参数让策略更鲁棒; 2) Domen özelleşimi using a small amount of real data; 3) 系统识别测量真实参数修正仿真器──2026 yılının ana yöntemi üç kişilik birleştirme+ büyük ölçekli GPU ve imitator olarak ilerlemelidir.

> **【拓展：域随机化→大模型泛化】**Bölge ırkınlaşması düşüncesi LLM ırkınlaşmasında da karşı karşıya: DATA增强 (data增强) 同义改写、噪声注入) 就是"ırkınlaşmanın ırkınlaşması 分布"                                                                                                                                                                                                                               

## Konsepten bir şey.

![Three sim-to-real regimes: domain randomization, adaptation, system identification](../assets/sim-to-real.svg)

**Domain Randomization (DR).**Tobin et al. 2017, Peng et al. 2018'de. Eğitim sırasında gerçek robot üzerinde farklı olabilecek her sim parametresini rastgele yapın: kütleler, sürtünme katılıkları, motor PD kazançları, sensör gürültüsü, kamera pozisyonu, aydınlatma, dokular, temas modelleri. Politika "bugün hangi simde" bir koşullu dağılım öğrenir ve tüm alan boyunca genelleştirir. Eğer gerçek robot eğitim zarfına girerse, politika işe yarar.

> **域随机化（DR）。** eğitim sırasında, her olasılık, gerçek robotla farklı simülasyon parametreleri: kalitesi, ırmaklılıklılıklılıklılık,  makineler PD  artım  sensör gürültüsü, 相机位置, 光照纹理, kontakt modeli stratejisi  "bugün hangi simülasyonda" koşulları öğrenmek ve tüm kapsamda yaygınlaştırılmaktadır

- **Upside:**Gerçek verilere gerek yok.
  **优点：**Gerçek verilere gerek yok. Bir program, bir sürü makine.
- **Downside:**Çok rastgele eğitim "üneyet" ama çok dikkatli bir politika üretir.
  **缺点：** aşırı zamanlı eğitim "genel" ama aşırı koruyucu strateji oluşturur.  Çok fazla gürültü  Çok fazla normalleşme 

**System Identification (SI).**Simülatörün parametrelerini eğitimden önce gerçek dünya verilerine ayarlayın. Eğer gerçek robotta kol-kol sürtüşmesini ölçebilirseniz, onu simleme bağlayın. Sonra bu değerleri bekleyen bir politika eğitiniz. Gerçek sisteme erişime ihtiyaç duyar ama gerçeklik boşluğunu doğrudan azaltır.

> **系统辨识（SI）。**訓練前将仿真器参数适应到真世界数据──需要接触真实系统但直接缩小现实沟──

**Domain Adaptation.**Sim yaparak, az miktarda gerçek veriyle ince ayarlama yaparak.

> **域自适应。**Bu yüzden, gerçek veriyi kullanarak iki farklılık gösterir:

- **Real2Sim2Real:**Geri kalan simülatörü öğrenin .`f(s, a, z) - f_sim(s, a)`Gerçek devreye girişimleri kullanarak, düzeltilmiş simletimde çalıştırmak.
  **Real2Sim2Real：**Gerçek bir uygulama ile, düzeltme sonrası, gerçek bir uygulama içinde eğitim.
- **Observation adaptation:**Öğrenilmiş bir özellik çıkarıcı (örneğin, GAN pikselden piksel) aracılığıyla gerçek obs → sim benzeri obs haritasını yapan bir politika eğitmek.
  **观测自适应：**訓練将真实观测映射为仿真式观测的策略──

**Privileged learning / teacher-student.**Miki et al. 2022 (Yeni dörtlü). * öğretmen *'yi simülasyonda eğit, böylece özel bilgilere erişebilir (yerin gerçeği sürtünmesi, arazi yüksekliği, IMU sürüklenmesi). * Öğrenci *'yi sadece gerçek sensör gözlemlerini gören bir *isteden ayırın. Öğrenci, fiziksel parametreler arasında sağlam olan özel özellikleri tarihten çıkarmayı öğrenir.

> **特权学习/教师-学生。**Bu nedenle, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrencilerin hakları hakkında bilgi edinmeleri için, öğrenciler tarafından kullanılarakiler tarafından kullanılarak kullanılarak kullanılarak,

**Massively parallel simulation.**20242026. Isaac Lab, Mujoco MJX, Brax hepsi binlerce paralel robotları tek bir GPU'da çalıştırabilir. 4.096 paralel humanoid olan PPO, saatler içinde yıllarca deneyim toplar. Eğitim dağıtımının genişleştiği gibi "gerçeklik boşluğu" azalır; DR, bu 4.096 envs'lerin her birinin farklı rastgele parametreleri olduğunda neredeyse serbest hale gelir.

> **大规模并行仿真。**2024-2026 yılları──Isaac Lab、Mujoco MJX、Brax, tek bir GPU üzerinde binlerce paralel robot çalıştırıyor──PPO  birlikte 4,096 paralel insan biçimindeki robot birkaç saat içinde yıllar süren deneyim topladı──

**The real-world 2026 recipe (quadruped walking example):**

1. Domen rastgele çekim, sürtünme, motor kazançları, yararlı yük ile büyük bir paralel sim.
2. Öğretmen politikaları ayrıcalıklı bilgilerle eğitilmiştir (yer haritası, vücut hızı, yer gerçeği).
3. Öğrenci politikası sadece proprioception (ayak eklem kodlayıcıları) kullanarak öğretmenden destillenmiştir.
4. Gerçek IMU'da otomatik kodlayıcı ile gözlem uyarlaması.
5. 10+ ortamda sıfır çekim yapın. Başarısız olursa, güvenlik kısıtlılığı olan PPO ile gerçek dünyadaki dakikalar boyunca ince ayarlama yapın.

> **真实世界 2026 年方案（四足行走示例）：**Büyük ölçekli并行仿真 + 域随机化 → Öğretmen kuralı(特权信息)→ Öğrenci kuralı蒸(仅本体感受)→ 可选观测自适应 → 部署。零样本迁移到10+ 环境。 Eğer başarısız olursak,做几分钟安全约束 PPO 真实世界微调。

## Yapın.
```figure
f3-reality-gap
```

## Yapın

Bu dersin kodu * gürültülü * geçişlerle bir GridWorld'de domen rastlantısının küçük bir göstergesidir. "sim"de rastgele kayma olasılıklarını deneyimleyen ve eğitim sırasında hiç görmediği kayma seviyesine sahip "gerçek" değerlendiren bir politika eğitiriyoruz. Şekil doğrudan MuJoCo'ya donanımlı aktarım için haritasını yapar.

> Bu dersin kodu, GridWorld'in üzerinde gelen sesle hareket eden küçük bir domen kasıtlılığının gösterisidir. Biz "imic" içinde deneyimlenen kasıtlı kayma olasılığı stratejisini eğittik ve eğitim sırasında hiç görülmemiş bir kayma seviyesinde değerlendirdiğimiz "gerçek" yapı, doğrudan MuJoCo'ya haritasın göçüne yerleştirilmiştir.

### Adım 1: parametre sim

```python
def step(state, action, slip):
    if rng.random() < slip:
        action = random_perpendicular(action)
    ...
```

`slip`Gerçek robotlarda, sürtünme, kütle, motor kazancı sim ve gerçek arasında değişen herhangi bir şey olabilir.

> `slip`Gerçek makineler arasında ise, gerçek makineler arasında herhangi bir değişimin miktarı olabilir.

### Adım 2: DR ile tren

Her bölümün başında, örnek`slip ~ Uniform[0.0, 0.4]`PPO / Q öğrenme / her şeyi eğit.

> Her seferinde başlayan zaman, örnek.`slip ~ Uniform[0.0, 0.4]` PPO/Q-learning/ herhangi bir algoritma eğitimi

### Adım 3: "gerçek" kartlarda sıfır atış değerlendirin

Değerlendirin `slip ∈ {0.0, 0.1, 0.2, 0.3, 0.5, 0.7}`İlk dört öğrenci eğitim desteği alanında bulunmaktadır.`0.5`ve `0.7`DR eğitimli bir politika, iç destekte neredeyse optimal kalmalı ve dışarıda zarif bir şekilde azalmalıdır.

> - Evet .`slip ∈ {0.0, 0.1, 0.2, 0.3, 0.5, 0.7}`Ünce değerlendirme.`0.5`和 `0.7`Dışarıda  DR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

### 4. adım: dar eğitimle karşılaştırın

İkinci bir politika oluşturmak için `slip = 0.0`Aynı şekilde değerlendirilir.`slip`Gerçek sıfırdan sonra felaket düşüşü görmelisiniz.

> Kullan .`slip = 0.0`訓練第二策略──在相同滑移范围上评估──当真实滑移 > 0 时应看到灾难性下降──

## Tuzaklar

- **Too much randomization.**Trene devam ediyor .`slip ∈ [0, 0.9]`* Beklenen* gerçek dünya dağılımına uygun, "Her şey olabilir" değil.
  **过度随机化。**- Evet .`slip ∈ [0, 0.9]`Üst eğitim, strateji en iyi yolu denemekten fazla kaçınmak ve en iyi yolu uygulamak.
- **Too little randomization.**Uygulama, ince bir parça üzerinde çalıştırılır ve politika genelleşemez.
  **过少随机化。**Bu nedenle, bu yöntemin uygulanması ve uygulanması için gerekli olan yöntemler de vardır.
- **Misidentified parameter space.**Yanlış şeyi rastgeleleştir (gerçek boşluk motor gecikmesi olduğunda kamera rengi) ve DR yardımcı olmaz.
  **错误识别参数空间。**随机化错误的东西,DR 无效――先分析真机器人――
- **Privileged info leakage.**Sadece gözlemler değil, küresel durumu eylemler için kullanan bir öğretmen, takip edemeyecek bir öğrenci üretebilir. Öğretmenin politikasının gözlem tarihini verilen öğrenci tarafından gerçekleştirilebilir olmasını sağlayın.
  **特权信息泄漏。**Tüm düzeyde hareket eden öğretmenler takip edemeyecek öğrencileri oluşturabilir.
- **Sim-to-sim transfer failure.**Eğer politikası daha zor bir sim varianti için sağlam değilse, gerçek dünyaya de sağlam olmayacaktır.
  **仿真到仿真迁移失败。**Eğer daha zor simülasyonlara karşı bir strateji çalışmazsa, gerçek dünyaya karşı da çalışmaz.
- **No real-world safety envelope.**Düşük düzeyde güvenlik kalkanı olmadan simde çalışan ve "gerçekte çalışan" bir politika hala donanımları kırabilir.
  **无真实世界安全包络。**低级安全屏蔽策略仍然可能损坏硬件──非学习控制器中加速度限制、扭矩限制、关节限制──

## Çerçeveyi kullanın.

2026 sim-real yığın:

> 2026 yıl仿真到真实技术:

| Domain | Stack |
|--------|-------|
| Domain / 领域 | Stack / 技术栈 |
| Legged locomotion (ANYmal, Spot, humanoid) / 腿式运动 | Isaac Lab + DR + privileged teacher / student |
| Manipulation (dexterous hands, pick-and-place) / 操作 | Isaac Lab + DR + DR-GAN for vision |
| Autonomous driving / 自动驾驶 | CARLA / NVIDIA DRIVE Sim + DR + real fine-tune |
| Drone racing / 无人机竞速 | RotorS / Flightmare + DR + online adaptation |
| Finger/in-hand manipulation / 手指/手内操作 | OpenAI Dactyl (DR at unprecedented scale) |
| Industrial arms / 工业机械臂 | MuJoCo-Warp + SI + small real fine-tune |

Tüm ölçeklerde kontrol için iş akışı tutarlıdır: simgeyi mümkün olduğunca uyumlu hale getirin, uyumlu olamadığınız şeyleri rastgele yapın, devasa politikalar uygulayın, destil edin, bir güvenlik kalkanıyla dağıtın.

> Tüm büyüklükteki kontrol, çalışma akışı: mümkün olduğunca uygulanabilir, mümkün olduğunca uygulanabilir olmayan kısım, büyük stratejileri eğitmek, çalıştırmak, yerleştirmek, güvenlik koruma.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-sim2real-planner.md`- ...

```markdown
---
name: sim2real-planner
description: Plan a sim-to-real transfer pipeline for a given robot + task, covering DR, SI, and safety.
version: 1.0.0
phase: 9
lesson: 11
tags: [rl, sim2real, robotics, domain-randomization]
---

Given a robot platform, a task, and access to real hardware time, output:

1. Reality gap inventory. Suspected sources ranked by expected impact (contact, sensing, actuation delay, vision).
2. DR parameters. Exact list, ranges, distribution. Justify each range against real measurements.
3. SI steps. Which parameters to measure; measurement method.
4. Teacher/student split. What privileged info the teacher uses; what obs the student uses.
5. Safety envelope. Low-level limits, emergency stops, backup controller.

Refuse to deploy without (a) a zero-shot sim-variant test, (b) a safety shield, (c) a rollback plan. Flag any DR range wider than 3× measured real variability as likely over-randomized.
```

## Egzersizler.

1. **Easy.**Bir Q-öğrenme ajanını sabit kaydırma GridWorld'de eğit (slip=0.0).
2. **Medium.**DR Q öğrenme ajanı örneklemesini eğit `slip ~ Uniform[0, 0.3]`DR'nin dağıtım dışı fiyatı 0,5'dir.
3. **Hard.**Bir eğitim programı uygulayın: slip=0.0 ile başlayın, politikaların %90'a ulaştığında DR aralığını genişletin.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Reality gap | "Sim-to-real difference" / 现实鸿沟 | Distribution shift between training and deployment physics/sensing. |
| Domain randomization (DR) | "Train across random sims" / 域随机化 | Randomize sim parameters during training so policy generalizes. |
| System identification (SI) | "Measure real and fit sim" / 系统辨识 | Estimate real physical parameters; set sim to match. |
| Domain adaptation | "Fine-tune on real data" / 域自适应 | Small real-world fine-tune after sim training; may adapt obs or dynamics. |
| Privileged info | "Ground truth for teacher" / 特权信息 | Information only the sim has; student must infer it from obs history. |
| Teacher/student | "Distill privileged -> observable" / 教师-学生蒸馏 | Teacher trained with shortcuts; student learns to mimic without them. |
| ADR | "Automatic Domain Randomization" / 自动域随机化 | Curriculum that widens DR ranges as the policy improves. |
| Real2Sim | "Close the gap with real data" / 现实到仿真 | Learn a residual to make the sim mimic real rollouts. |

## Daha fazla okumak

- [Tobin et al. (2017). Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World](https://arxiv.org/abs/1703.06907) orijinal DR kağıdı (robotlar için vizyon).
- [Peng et al. (2018). Sim-to-Real Transfer of Robotic Control with Dynamics Randomization](https://arxiv.org/abs/1710.06537) D.R. dinamik, dörtlü hareket.
- [OpenAI et al. (2019). Solving Rubik's Cube with a Robot Hand](https://arxiv.org/abs/1910.07113) Dactyl, ölçekte ADR.
- [Miki et al. (2022). Learning robust perceptive locomotion for quadrupedal robots in the wild](https://www.science.org/doi/10.1126/scirobotics.abk2822) ANYmal için öğretmen-öğrenci.
- [Makoviychuk et al. (2021). Isaac Gym: High Performance GPU Based Physics Simulation for Robot Learning](https://arxiv.org/abs/2108.10470) 2025  2026 dağıtımlarını yönlendiren büyük paralel sim.
- [Akkaya et al. (2019). Automatic Domain Randomization](https://arxiv.org/abs/1910.07113) ADR eğitim programı yöntemi.
- [Sutton & Barto (2018). Ch. 8 — Planning and Learning with Tabular Methods](http://incompleteideas.net/book/RLbook2020.pdf) modern sim-real boru hattlarının temelini oluşturan Dyna çerçevesini (planlama + dağıtım için bir model kullanın).
- [Zhao, Queralta & Westerlund (2020). Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey](https://arxiv.org/abs/2009.13303) Benchmark sonuçları ile sim-to-real yöntemlerin taksonomisi.
