# MARL  MADDPG, QMIX, MAPPO  MADDPG MAPPO MARL QMIX

> 2026'da hala LLM-agent sistemlerini bilgilendiren çoklu ajan koordinasyonunun güçlendirme-öğrenme mirası. **MADDPG**(Lowe et al., NeurIPS 2017, arXiv:1706.02275) Merkezi Eğitim, Merkezi İşlem (CTDE) başlattı: her eleştirmen eğitim sırasında tüm ajanların durumlarını ve eylemlerini görür; test zamanında sadece yerel aktörler çalışır. İşbirliği, rekabetçi ve karışık ortamlar için çalışır. **QMIX**(Rashid et al., ICML 2018, arXiv:1803.11485) bir monotonik karıştırma ağı ile değer-karıştırma; ajan başına Qs birleşik Q'lar böylece `argmax` StarCraft Multi-Agent Challenge (SMAC) üzerinde baskın bir şekilde dağıtılır. **MAPPO**(Yu et al., NeurIPS 2022, arXiv:2103.01955) merkezi bir değer fonksiyonu olan PPO'dur; parçacık dünyasında, SMAC, Google Araştırma Futbolu, Hanabi'de en az ayarlama ile "içik etkili".**default 2026 cooperative-MARL baseline**Bu ders, küçük bir çubuğuz dünyası oyuncağından her birini inşa eder ve üç fikri kas hafızasına yerleştirir.

> **【中文解读】**Bu bölümde bir çok ajanı tanıttım 强化学习MADDPG、QMIX、MAPPO 等多 ajanı RL 算法。

> **【拓展：marl maddpg qmix mappo→具体应用】**Çoğu Ajan 强化学习(MARL) algoritması:(1) MADDPG her Ajanın bağımsız bir Actor-Critic, ancak Eleştirmen tüm Ajanın hareketlerini görebilir;(2) QMIX yoğun bir eğitim dağılıp gerçekleştirir, karışık bir ağ güvenceye göre;(3) MAPPOPPO'nun çoklu Ajan 扩展──2026 yılında MARL oyunda AI 机器人协作与交通管制で進展取得, ancak LLM Ajanında uygulama henüz erken bir dönemde ise.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, small NumPy-free implementations) | **语言:** Python（标准库，无 NumPy 的小型实现）
**Prerequisites:** Phase 09 (Reinforcement Learning), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 09（强化学习），Phase 16 · 09（并行群体网络）

>  **【前置】**Önemli bir eğitim programı yaparak, öğrenci sınıfının öğrencileri ve öğrencileri için en iyi eğitim programı yaparak, öğrenci sınıfının öğrencileri için en iyi eğitim programı yaparak, öğrenci sınıfının öğrencileri için en iyi eğitim programı yaparak, öğrenci sınıfının öğrencileri için en iyi eğitim programı yaparak, öğrenci sınıfının öğrencileri için en iyi eğitim programı yaparak, öğrenci sınıfının öğrencileri için en iyi eğitim programı yaparak, öğrenci sınıfının öğrencileri için en iyi eğitim programı yaparak, öğrenci sınıfının öğrencileri için en iyi eğitim programı yaparak, öğrenci sınıfının öğrencileri için en iyi eğitim programı yaparak, öğrenci sınıfının öğrencileri için en iyi eğitim programı yaparak, öğrenci sınıfının öğrencileri için en iyi eğitim programı yaparak, öğrenci sınıfı geliştirmek için en iyi bir eğitim program yaparak, öğrenci sınıfı geliştirmek için en iyi bir eğitim program yaparak, öğrenci sınıflandırmak için en iyi bir eğitim program yaparak, öğrenci sınıflandırmak için en iyi bir eğitim program yaparak, öğrenci sınıflandırmak için.
>  **【类比】**MARL = "Bol takım eğitimi"──MADDPG = 教练看全场训练(集中批評),比赛时球员各自决策(分散演员);QMIX = Herkesin bir Q 值,单调混合保证最优解可分;MAPPO = PPO多 Agent 版本──MAPPO 是 2026 合作 MARL 默认基线(" şaşırtıcı derecede etkili"),SMAC、Google Football、Hanabi 都能少调参跑通──LLM Agent training也借鉴这套范式──
**Time:** ~90 minutes | **时间:** ~90 分钟

## Sorunlar sorunun giriş

LLM-agent sistemleri, giderek daha fazla ajanlar arası koordinasyon politikalarını eğitmektedir: ne zaman ertelenmek, ne zaman harekete geçmek, hangi kişiyi çağrmak. Bu politikaları nasıl eğitileceğini söyleyen literatür, LLM dalgasından önceki ve küçük bir baskın algoritma kümesine sahip olan Multi-Agent Reinforcement Learning (MARL) dır.

> LLM-Agent 系统越来越地训练 Agent 间协调策略:何时延迟、何时行动、调用哪个同伴──告诉你如何训练这些策略的文献是多 Agent 强化学习 ((MARL), bu LLM 浪潮, 一小组主导算法, 早期的.

MARL makaleleri, örneği kelimeforusu olmadan okumak acı verici. Merkezsiz yürütme (CTDE), değer parçalanması ve merkezi eleştirmenlerle merkezileştirilmiş eğitim, birer konu hakkında konuşan bir kelime değildir.

> 没有模式词汇表阅读 MARL 论文是痛苦的──集中训练分散执行(CTDE)、值分解和集中式评论家流行词它们是特定问题的特定答案:

- Bağımsız RL (her ajan tek başına öğrenir) her ajanın bakış açısından istasyonel değil.
  Çinçe Çevirimi: bağımsız RL( her Agent 独立学习)
- Merkezi RL (tek ajan hepsini kontrol eder) ölçeklendirme yapmaz ve yürütme kısıtlamalarını ihlal etmez.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- CTDE her ikisinden de en iyisini elde eder: küresel bilgi ile eğitilmek, yerel politikalarla çalıştırmak.
  Çinçe Çevirimi:CTDE 兼得两者之长: 全局信息训练,用局部策略部署。

## Konsept merkezi konsept

### Kağıtlar üç ortamda kullanıyor

- **Particle World (multi-agent particle env).**MADDPG'nin orijinal test yatağı.
- **StarCraft Multi-Agent Challenge (SMAC).**İşbirliği mikro yönetimi, kısmi gözlem, QMIX'in test yatağı, ayrıntılı eylemler, sürekli durumlar.
- **Google Research Football, Hanabi, MPE.**Mappo Temel Hatları.

Farklı ortamlar farklı eylem/ gözlem türlerine sahiptir.

### MADDPG (2017)  CTDE örneği

Her ajan .`i`Bir aktörü var.`mu_i(o_i)`Bu, kendi gözlemlerini eylemlere yerleştirir.`Q_i(x, a_1, ..., a_n)`Bu, eğitim sırasında tüm gözlemleri ve tüm eylemleri görüyor.

```
actor update:    grad_theta_i J = E[grad_theta mu_i(o_i) * grad_a_i Q_i(x, a_1..n) at a_i=mu_i(o_i)]
critic update:   TD on Q_i(x, a_1..n) given next-state joint estimate
```

Neden CTDE: eğitim sırasında, herkesin eylemlerini biliyoruz; bunu her eleştirmende farklılık azaltmak için kullanıyoruz.`o_i`ve aramalar`mu_i(o_i)`- Evet .

Başarısızlık modu: eleştirmenler N ajanlarla büyür (gönüllülük tüm eylemleri içerir). Yaklaşım olmadan ~ 10 ajanın ötesine ölçeklendirmeyi engellemez.

### QMIX (2018)  değer parçalanması

Toplam ödül, bir ajan başına Q değerlerinin monoton fonksiyonunun toplamıdır:

```
Q_tot(tau, a) = f(Q_1(tau_1, a_1), ..., Q_n(tau_n, a_n)),   df/dQ_i >= 0
```

Tek kelimelilik garanti eder `argmax_a Q_tot`Her seçen ajan tarafından hesaplanabilir.`argmax_{a_i} Q_i`- Bağımsız olarak.**exactly the decentralized execution property**Eğitim sırasında, bir karıştırma ağı üretir.`Q_tot`- Bir ajan için Qs'ten.

Neden QMIX SMAC'da kazanıyor: StarCraft mikro yönetimi kooperatifine eşdeğer ajanlar, yerel iş, küresel ödül  değer parçalanması için mükemmel bir uyum sağlar.

Başarısızlık modu: monotonluk kısıtlaması kısıtlayıcıdır; bazı görevlerde monoton bozulmayan ödül yapıları vardır (kişiler için bir ajan feda edilir).

### MAPPO (2022)  göz ardı edilen misilleme

Çoklu Ajan PPO: Merkezi bir değer fonksiyonu olan PPO. Her ajanın kendi politikası vardır; tüm ajanlar tam durumu gören değer fonksiyonlarını paylaşıyor (veya var). Yu ve diğerleri 2022'de MAPPO'yu MADDPG, QMIX ve uzantıları ile beş referans değerine göre karşılaştırdılar ve buldular:

- MAPPO, PARTICLE-WORLD, SMAC, Google Research Football, Hanabi, MPE'deki politikası dışı MARL yöntemlerine eşlik ediyor veya yener.
- En az hiperparametre ayarlaması gereklidir.
- Dayanıklı eğitim; tohumlar arasında yeniden üretilebilir.

Toplum bu makaleye kadar politika MARL'i küçümsüyordu. 2026'da MAPPO kooperatif MARL için varsayılan temel çizgidir; herhangi bir yeni yöntem onu yenmelidir.

### LLM mühendislerinin neden ilgilenmesi gerekiyor

Üç doğrudan kullanım:

1. **Router training.**Meta-agent bir görevi hangi alt-agent ile hallediyor seçer. Bu bir MARL sorunu N merkezi olmayan alt-agent ve bir merkezi yönlendirici.
2. **Role emergence.**Geliştirici ajan simülasyonlarında, zaman içinde tamamlayıcı roller benimsemek için eğitim ajanları, bir MARL sorunu olarak gizlenir.
3. **Multi-agent tool use.**Ajanlar araçları paylaşırken ve bütçe için rekabet ederken, CTDE aracılığıyla eğitilmeleri kaynak kısıtlamalarını saygılı olarak uygulanabilir yerel politikalar üretir.

Pratik bir uyarı: 2026 yılında, çoğu üretim LLM-ajen sistemi, politikalarını eğitmek yerine uyarır. MARL (a) çok sayıda etkileşim verisi, (b) net bir ödül sinyali ve (c) eğitim altyapısına yatırım yapmaya istekli olduğunuzda gelir.

### CTDE, RL'den öte bir tasarım örneği olarak

Eğitim olmadan bile CTDE yararlı bir mimari örneğidir:

- * tasarım* sırasında, tüm ekibin görünürlüğünü düşünün.
- * Runtime*'de merkezi olmayan yürütme uygulanması: her ajan sadece `o_i`- Evet .

Bu model, ajan başına açık bir durum tutmanıza ve öncesinde kısmi gözlemlenebilirliği düşünmenize zorlar. Birçok üretim çok ajanlı sistemi sessizce her yerde paylaşılan durumun varlığını varsaymaktadır.

### Yerleşimsizlik sorunu

Birden fazla ajan aynı anda öğrendiğinde, her ajanın ortamı (başkalarının politikalarını da içeren) sabit değildir.

- MADDPG: Küresel eleştirmen tüm eylemleri görür, bu yüzden değer tahminleri sabit.
- QMIX: değer parçalanması, öğrenmenin iyi tanımlanmış olan en iyi şekilde tanımlanmış olan bir ortak-Q alanına taşınır.
- MAPPO: merkezi değer fonksiyonu, başkalarının politika değişikliklerinden farklılıkları azaltır.

LLM-agent sistemlerinde, istasyonarlık "benim ajanım geçen ay çalıştı, şimdi diğer ajanın akıntıda değişmesi, maden yanlış davranışı" olarak ortaya çıkar.

### Bu ders neyi kapsamıyor

Gerçek ağları eğitmek, 9. aşamada bir konu. Bu ders, CTDE, değer parçalanması ve gradient güncellemeleri olmadan merkezileştirilmiş değer kalıplarını gösteren senaryolı politika sürümlerini oluşturur.

## Yapın.
```figure
sw-ctde
```

## Yapın

`code/main.py`Üç örnek gösterisi uyguluyor, hepsi küçük bir iki ajanlı kooperatif şebekesi dünyasında:

- Çevre: 4×4 şebekede 2 ajan, bir ödül pellet.
  Çinçe Çevirim: Çevre: 2 个 代理 在 4x4 网格上,一个奖励颗粒──任何代理到达颗粒则奖励 = 1;任务结束──
- `IndependentAgents` her ajan diğerlerini çevre olarak görüyor.
  Çeviri:`IndependentAgents` Her ajan diğer ajanı görür.
- `MADDPGStyle` Merkezli eleştirmen ortak bir değer hesaplar; aktör politikaları ondan güncelleştirir.
  Çeviri:`MADDPGStyle` 集中式评论家计算联合值;Actor 策略从中更新──脚本化策略改进──
- `QMIXStyle` değer parçalanması monoton bir karıştırıcı ile.
  Çeviri:`QMIXStyle` 带单调混合器的值分解──
- `MAPPOStyle` Merkezi değer fonksiyonu; politikalar paylaşılan temel çizgiye göre güncellenir.
  Çeviri:`MAPPOStyle` 集中式值函数; 策略对共享基线更新。

Dörtü de aynı bölümleri yürütür ve ortalama adımlar ile hedefe rapor eder. CTDE varianları bağımsız başlangıç çizgisinden daha kısa yollara doğru birleşti.

> Tüm dört çalışmanın aynı döngüsü ve raporları hedef adım sayısına ulaşmak için ortalama bir yol oluşturur.

Çık:

```
python3 code/main.py
```

Beklenen çıkış: bağımsız ajanlar ortalama ~ 6 adım atarlar; CTDE varyantları ~ 3.5 adımlara doğru birleşti (optimal 4x4 şebekesi için 3'dir).

## Kullanın Kullanın

`outputs/skill-marl-picker.md`verilen bir çok ajanlı görev için MARL algoritmasını seçen bir beceri: işbirliği vs rekabetçi, homogen vs heterogen, eylem alanı tipi, ölçek, ödül sinyali.

## Gönderin.

Üretimdeki MARL nadirdir.

- **Start with MAPPO.**2022 makalesi bunu temel çizgi olarak belirledi; ilk olarak yeniden üretmek, daha süslü yöntemlerin peşinden koşmak için haftalar kurtarır.
  Çeviri:**从 MAPPO 开始。**2022'de baskı kurulacak; daha fazla kullanışlı yöntemin süresi için haftalarca tasarruf edilebilir.
- **Log every agent's observation and action stream.**Ajanın izleri olmadan MARL'i düzeltmek umutsuz.
  Çeviri:**记录每个 Agent 的观察和动作流。**Her bir ajanın yolculuğu, MARL'de bir hayal kırıklığı var.
- **Separate training code from execution code.**CTDE bir disiplin; sadece yürütme yolunun görmesine izin verin`o_i`- Evet .
  Çeviri:**分离训练代码和执行代码。**CTDE bir kural; gerçekleştirme yollarını gerçekten sadece görme.`o_i`- Evet.
- **Reward shaping warning.**MARL, ödül tasarımına çok hassas bir koordinasyon hatası şekillendirme ve ajanlar bunu kullanmayı öğrenir.
  Çeviri:**奖励塑形警告。**MARL, ödül tasarımına karşı çok hassas bir koordinasyon hatası vardır.
- **For LLM agents**MARL eğitimine yalnızca etkileşim verileri + ödül sinyali + altyapı mevcut olduğunda yatırım yapın.
  Çeviri:**对于 LLM Agent**, önce öneriler ve stratejileri düşünün. Sadece iletişim verileri + ödül sinyalleri + altyapı için hazırlıklı olan MARL eğitimlerini yatırım yapın.

## Egzersizler.

1. Çık .`code/main.py`- bağımsız ve MAPPO tarzı ajanlar arasındaki adım-amaca farkı ölçmek. 6x6 şebekede fark büyüyor mu yoksa küçülüyor mu?
2. Rekabetçi bir variant uygulayın: iki ajan, bir pellet, sadece ilk ulaşan ödül alır. Hangi model rekabeti temiz şekilde ele alır?
3. MADDPG'yi okuyun (arXiv:1706.02275) Bölüm 3. Tam eleştirmen güncelleme kuralını kendi kelimelerinizle, sembolik olarak pseudokodla uygulayın.
4. MAPPO'yu okuyun (arXiv:2103.01955). Yazarlar neden merkezi değer + PPO'nun politika dışı MARL'yi yendiğini iddia ediyorlar?
5. CTDE'yi bir hipotetik LLM-ağent sistemi için tasarım örneği olarak uygulayın (örneğin, araştırma ajanı + özetleyici + kodlayıcı).

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MARL / 多 Agent 强化学习 | "Multi-Agent RL" / "多 Agent 强化学习" | Reinforcement learning for multi-agent systems. / 多 Agent 系统的强化学习。 |
| CTDE / 集中训练分散执行 | "Centralized Training, Decentralized Execution" / "集中训练分散执行" | Train with global info; deploy with local policies. / 用全局信息训练；用局部策略部署。 |
| MADDPG | "Multi-Agent DDPG" / "多 Agent DDPG" | CTDE with per-agent critic seeing all observations + actions. / CTDE，每个 Agent 的评论家看到所有观察 + 动作。 |
| QMIX / 值分解 | "Value decomposition" / "值分解" | Monotonic mixing of per-agent Qs. Cooperative. / 每 Agent Q 的单调混合。协作型。 |
| MAPPO / 多 Agent PPO | "Multi-Agent PPO" / "多 Agent PPO" | PPO with centralized value function. 2026 default baseline. / 带集中式值函数的 PPO。2026 默认基线。 |
| Value decomposition / 值分解 | "Sum of individual Qs" / "个体 Q 之和" | Joint Q represented as a monotone function of per-agent Qs. / 联合 Q 表示为每 Agent Q 的单调函数。 |
| Non-stationarity / 非平稳性 | "Moving targets" / "移动目标" | Each agent's env changes as others learn. The core MARL problem. / 每个 Agent 的环境随着其他 Agent 学习而变化。核心 MARL 问题。 |
| On-policy / off-policy / 同策略/离策略 | "Learn from current / replay" / "从当前/回放学习" | PPO is on-policy (MAPPO); DDPG and Q-learning are off-policy. / PPO 是同策略（MAPPO）；DDPG 和 Q-learning 是离策略。 |
| SMAC / 星际争霸多 Agent 挑战 | "StarCraft Multi-Agent Challenge" / "星际争霸多 Agent 挑战" | Cooperative micromanagement benchmark; QMIX's homegrown ground. / 协作微操基准；QMIX 的主战场。 |

## Daha fazla okumak

- [Lowe et al. — Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments](https://arxiv.org/abs/1706.02275) MADDPG; NeurIPS 2017
- [Rashid et al. — QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning](https://arxiv.org/abs/1803.11485) QMIX; ICML 2018
- [Yu et al. — The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games](https://arxiv.org/abs/2103.01955) MAPPO; NeurIPS 2022
- [BAIR blog post on MAPPO](https://bair.berkeley.edu/blog/2021/07/14/mappo/) MAPPO sonuçlarının okunur çerçevesinde
- [SMAC repository](https://github.com/oxwhirl/smac) StarCraft Çoklu Ajan Çabası
