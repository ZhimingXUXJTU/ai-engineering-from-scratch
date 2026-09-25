# Swarm Optimization for LLM (PSO, ACO) 优化群体 PSO ACO LLM

> Bio-İnspire Optimizasyon, LLM'nin geri dönüşünü yapıyor. **LMPSO**(arXiv:2504.09247) her parçacığın hızının bir istek olduğu ve LLM'nin bir sonraki adayı oluşturduğu PSO kullanır; yapılandırılmış sıralama çıkışlarında (matematik ifadeler, programlar) iyi çalışır. **Model Swarms**(arXiv:2410.11163) her LLM uzmanını model ağırlığıyla bir çeşitlilik üzerinde bir PSO parçacığı olarak değerlendirir ve raporlar **13.3% average gain**Sadece 200 örnekle 9 veri kümesi üzerinde 12 temel çizgi. **SwarmPrompt**(ICAART 2025) hızlı optimizasyon için PSO + Grey Wolf hibridleştirir. **AMRO-S**(arXiv:2603.12933) çoklu ajan LLM yönlendirme için ACO-İnspire feromon uzmanları  **4.7x speedup**Bu ders, akıllıca parametre alanında PSO'yu ve ajan yönlendirme üzerinde ACO'yu uyguluyor, bu klasik algoritmaların LLM çağına neden ve ne zaman uymadığını ölçüyor.

> **【中文解读】**Bu bölüm, PSOparticle group ve ACOgroup gibi biyolojik particle group ve group group group optimization group optimization group optimization group optimization group optimization group group group group group group group group group group group group group group group group group group group group group group group group group group group group group group group gr  gr  gr   gr                                                                                                                             

> **【拓展：swarm optimization pso aco→具体应用】**群体优化算法在多代理中的应用:(1) 粒子群优化(PSO) Agent 根据自身最佳位置和全局最佳位置调整搜索方向;(2) 群优化(ACO) Agent 通过信息素标记好的路径,后者倾向于跟随强信息素路径──这些算法适合大规模搜索空间中的优化问题,如 Agent 任务分配和路径规划──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 09 (Parallel Swarm Networks), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 09（并行群体网络），Phase 16 · 14（共识与 BFT）

>  **【前置】**Öğrenci bölümünün ilk aşamasında:BİLİM'e uygulanmış olan biyolojik gelişme algoritması:BİLİM'in 16·09 aşamasında:Swarm 网络)
>  **【类比】**LLM + PSO/ACO = "群找最佳快点"──PSO = Her Bir Ajan parçacık, hız=sürekli, tüm bölgeye en iyi hareket;ACO = Ajan 在快点 空间留下信息素,后者跟随强信息素──LMPSO 适合结构化输出(数学表达式、代码);Model Swarms Her bir LLM 专家当粒子,比 12 个基线平均高13.3%;AMRO-S ACO kullanarak 路由,4.7 倍加速──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar sorunun giriş

Görev değerlendirmesinde %62 puan alan bir istekiniz var. Onu geliştirmek istiyorsunuz. Saçma hareket, kötü ölçeklendiren gradientsiz manuel ayarlama. Güçlendirme öğrenimine ödül sinyalleri ve eğitime yeterli dağıtımlar gerekmektedir. İstekler aracılığıyla geri dönüş gerçekten mümkün değildir  istek ayrı bir dizilerdir, farklılaştırılabilir bir parametredir.

> Görev değerlendirmesinde %62 puan aldığınız bir ipucu var. Bunu geliştirmek istediğiniz bir ipucu var. Basit bir yöntem ise, dereceli el ayarlama, genişleme ve genişleme farkı olmaktır.

Klasik biyolojik ilhamlı optimizasyon  Sürekli arama alanları için PSO, ACO yol seçimi  tam olarak bu rejim için tasarlandı: gradientsiz, nüfus tabanlı, değerlendirme başına ucuz.

> 经典的生物启发优化PSO,连续搜索空间,ACO,路径选择正是为这种场景设计的:无梯度,基于种群,每次评估成本低――它们与LLM 配合进行无梯度搜索步骤,你得到一个惊人实用优化器――

Aynı kalıplar, çoklu ajan sistemlerinde ajan * yönlendirme * için de geçerlidir. ACO tarzı feromon izini kaydeder. Hangi ajan hangi görev türünde en iyi çalıştı, yönlendirici izini kullanmasına izin verir ve feromonları bozarak rotaların yeniden keşfedilmesi mümkün olur.

> Aynı model çoklu ajan sistemindeki ajan * route*。ACO  стиles 信息素轨迹记录 hangi ajan hangi görev türünde en iyi performans gösterdi, yolcuların rotaları kullanmasına izin vererek, yolu yeniden keşfetmek için bilgi素ini azaltmasına izin vererek ︎

## Konsept merkezi konsept

### PSO yenilenmesi (Kennedy & Eberhart 1995)

Partikel Swarm Optimization: sürekli bir arama alanında parçacıkların nüfusu.`x_i`ve hız.`v_i`Her tekrar:

```
v_i <- w * v_i + c1 * r1 * (p_best_i - x_i) + c2 * r2 * (g_best - x_i)
x_i <- x_i + v_i
evaluate fitness(x_i)
update p_best_i if improved
update g_best if global best
```

Nerede ?`p_best`Partikelin kendi en iyisi.`g_best`Swarm'ın en iyisi.`w, c1, c2`İnerti + bilişsel + sosyal ağırlıklar,`r1, r2`- Bu rastgele faktörler.

### LLM çıkışları için PSO  LMPSO

ArXiv:2504.09247 LLM tarafından oluşturulan yapılandırılmış çıkışlar (matematika ifadeleri, programlar) için PSO'yu uyarlar. Her parçacık bir aday çıkıştır. Hızlılık, mevcut çıkışın kişisel / küresel en iyi yönüne nasıl değiştirildiğini açıklayan bir * prompt * dır. LLM, hızlı çıkıştan yeni çıkış oluşturur. Hızlılığın "inertisi" "küçük artışlı değişiklikler yap" gibi bir istisna.

Bu iyi çalışır:
- Çıktıran yapılandırılmış (parse edilebilir, değerlendirilebilir).
  Çine dilinde:输出是结构化的 (输出是结构化的)
- Fitness otomatik (test çalışması, aritmetik değerlendirme).
  Çinçe Çevirimi:适应度是自动的测试运行、算术评估)
- Nüfusu küçüktür (~ 10-30 parçacık), bu nedenle toplam LLM çağrıları yönetilebilir kalır.
  Çinçe Çevirimiçi:种群小(約10-30 个粒子),总 LLM 调用可控。

Fitness'in insan tarafından incelemeye ihtiyacı olduğunda iyi çalışmaz.

> Yapay inceleme gerekirse, sonuç kötüdür.

### Model Swarms

ArXiv:2410.11163 PSO'yu çıkış katmanından *model* katmanına çıkarır. Her "partikel" bir uzman LLM (parametre) dir. Swarm, parametreleri gradientsiz bir güncelleme yoluyla toplu en iyi yönüne taşıyor.

Anahtar bir anlayış, LLM uzman modelleri zaten ortak bir parametre çeşitliliğinde (adapter ağırlıkları, LoRA deltas) yakınlarda bulunmaktadır.

### ACO yenilenmesi (Dorigo 1992)

Karınca Kolonisi Optimizasyon: Karıncalar bir grafik üzerinden geçer; her yolun feromon izleri vardır. Karıncalar olasılıkları feromon ağırlığı ile hareket eder. Görevyi tamamlayan karıncalar feromonları çözünürlük kalitesine orantılı olarak depolar. Feromonlar zamanla bozulur.

### AMRO-S  ACO ajan yönlendirme için

ArXiv:2603.12933 çoklu ajan yönlendirme için ACO kullanır. Her görev türü bir "yerleşme" dir; her ajan bir olası rota. Feromonlar iyi sonuçlar üreten yolları güçlendirir. Ana katkılar:

- **Interpretable routing evidence.**Feromon gücü insan tarafından okunur bir sinyaldir.
  Çeviri:**可解释的路由证据。**信息素强度, insan tarafından okunur.
- **Quality-gated asynchronous update.**Feromonlar sadece kalite kontrollerinin geçmesinden sonra güncellenir ve sonuçları öğrenimden ayırır.
  Çeviri:**质量门控异步更新。**信息素 sadece kalite kontrolü geçtikten sonra güncellenir, değerlendirilir ve öğrenilmektedir.
- **4.7x speedup**Çoklu ajan yönlendirme referans değerinde.
  Çin Çeviri:                                                                                                                                                                                                                                                            **4.7 倍加速**- Evet.

Kalite kapısı önemlidir: olmadan, hızlı ama yanlış ajanlar feromon biriktirir ve sistem kötü yollara kilitlenir.

> Kaliteti önemli: O olmadan, hızlı ama yanlış bir ajan, sistemin yanlış bir yolla kilitlendiği bilgi toplanır.

### LLM için PSO / ACO ne zaman kullanılır

**Use PSO when:**
- Arama alanı sürekli veya sürekli parametrelere (sürekli yerleşimler, LoRA ağırlıkları, sayısal jenerasyon parametreleri) haritalar.
  Çinçe Çevirimi: arama boşluğu is连续的或映射到连续参数(提示嵌入、LoRA 权重、数值生成参数) ⋅
- Fitness ucuz ve otomatik.
  Çinçe Çevirimi:适应度评估廉价且自动──
- Nüfusu küçük olabilir (10-30).
  Çeviri: 种群可以很小 ((10-30) ⋅

**Use ACO when:**
- Yol seçimi veya yönlendirme sorunu var.
  Çinçe Çevirisi: 你有路由或路径选择问题──
- Kararlar zamanla güçlenir (aynı görev türleri tekrarlanır).
  Çinçe Çevirimi: karar zamanla güçlenir (shame task type will come back)
- Yol kararları için yorumlanabilir kanıtlara ihtiyacın var.
  Çin Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çev

**Do not use either when:**
- Fitness insan incelemesini gerektirir (her tekrar için çok pahalı).
  Çinçe Çevirimi:适应度需要人工审查 (Yönetici)
- Arama alanı, PSO'nun kapsamadığı bir şekilde ayrı ve kombinatördür (genetik algoritmalar kullanın).
  Çinçe Çevirimiçi:搜索空间是离散组合的,PSO 无法覆盖 (PDO)
- Gerçek zamanlı kararlar sıkı gecikme süresi gerektirir (PSO/ACO tek geçiş heuristiklerine göre yavaşça birleşti).
  Çinçe Çevirisi:实时决策需要严格延迟(PSO/ACO 相对单次启发式收慢)

### Neden biyo-İnspire hala kazanıyor

Gradyent tabanlı yöntemler farklılaşabilen sinyallere ihtiyaç duyar. LLM çıkışları ve yönlendirme kararları önemsiz olarak farklılaşamaz.

PSO ve ACO'nun sadece *evaluator* fonksiyonu gerekir. Eğer bir aday çıkışı veya yönlendirme kararı puanlayabilirseniz, boşluğu optimize edebilirsiniz. Bu da uygulanabilirlik çubuğunu çok daha düşük yapar.

### Pratik sınırlamalar

- **Population budget.**N parçacık × T tekrarlama × her değerden maliyet.$0.02 / call, a 20-particle PSO running 50 iterations costs ~$20. Buna göre plan yapın.
- **Exploration vs exploitation.**Feromon bozulma oranı ve PSO inersiyası değişikliği; çok hızlı bozulma → çözümleri unutmak; çok yavaş → erken yerel optimuma sıkıştı.
- **Catastrophic drift.**Her iki algoritma da fitness manzarası değişirse bir araya gelebilir ve sonra farklılaşabilir (yeni veri dağıtım).

## Yapın.
```figure
swarm-stigmergy
```

## Yapın

`code/main.py`Uygulamaları:

- `LMPSO` PSO sayısal önlem parametreleri ( sıcaklık, top_k ağırlıklar) üzerinde. Her parçacığın "LLM nesli" bir scriptli fitness fonksiyonu olarak simüle edilir. Algoritmi 30 iterasyon için çalıştırır ve g_best konverjensi gösterir.
- `AMRO_S` ACO tarzı yönlendirme. 3 ajan, 4 görev türü, feromon matrisi, 100 yönlendirilmiş görev.
- Benzer bir görev akışında rastgele yönlendirme ile ACO yönlendirme karşılaştırması. Kaliteli ve gecikmeyi ölçer.

Çık:

```
python3 code/main.py
```

Beklenen üretim:
- LMPSO: g_best fitness 30 tekrar üzerinde rastgeleden neredeyse optimal'e kadar iyileşir.
- AMRO-S: feromon tablosu görev türüne göre doğru ajan üzerinde istikrar kazanır; ACO yönlendirme kalitede rastgele %30-40'a kadar çarpır ve aynı zamanda gecikmeyi (sadece tekrar deneme) azaltır.

## Kullanın Kullanın

`outputs/skill-swarm-optimizer.md`LLM / ajan optimizasyonu sorunları için PSO, ACO, genetik algoritmalar ve gradient tabanlı optimizörler arasında seçim yapma konusunda yardımcı olur.

## Gönderin.

- **Start small.**10-20 parçacık, 20-50 iterasyon.
  Çeviri:**从小开始。**10-20 parçacık, 20-50 kez 代── sadece kapsam eğriğinde belirgin artışlar gösterir.
- **Log pheromones or g_best per iteration.**İzlemeden sürü optimizörlerini düzeltmek acı verici.
  Çeviri:**每次迭代记录信息素或 g_best。**没有轨迹调试群体优化器 çok acı verici.
- **Quality-gate updates.**Özellikle ACO yönlendirme için: hızlı ve yanlış ajanlar feromon biriktirmemelidir.
  Çeviri:**质量门控更新。**Özellikle de ACO yolları: hızlı ama yanlış ajanı
- **Reset decay on distribution shift.**Evalü dağılımınız değişirken, yaşlı feromonlar eskisine kalmaz; bozulma oranını geçici olarak yeniden ayarlayın veya ikiye katlayın.
  Çeviri:**分布偏移时重置衰减。**Değişikliklerin değerlendirilmesi sırasında, yaşlanma bilgisi geçmiştir; yeniden yerleştirilme veya geçici olarak artış oranı azalmıştır.
- **Cap the per-iteration cost.**İterasyon başına 500 dolarlık ve % 0,5 kazançlı bir PSO gönderilmez.
  Çeviri:**限制每次迭代成本。**发发每次代成本指标──每次代花费$500 且只增加0.5% 的PSO不可发行──

## Egzersizler.

1. Çık .`code/main.py`LMPSO'nun yakınlaşmasını gözlemleyin. 5, 10, 20, 50 farklı nüfus boyutu.
2. "Kazadılı sürüş" deneyini uygulayın: 30'dan sonra fitness fonksiyonunu değiştirin. PSO ne kadar hızlı uyar?`p_best`Yardım mı?
3. AMRO-S'e bir kalite kapısı ekleyin: Feromon depozitosu sadece eval puanı > 0.7 olan çalışmalar için. Bu, kapalı olmayan sürümle karşılaştırıldığında nasıl dönüşüm değişir?
4. LMPSO'yu okuyun (arXiv:2504.09247). Kağıtın "hızlılığı bir istek olarak" sayısız hızınıza geri gönderin.
5. AMRO-S'i okuyun (arXiv:2603.12933). Asinkron feromon güncelleme ile koparılmamış "inference fast-path" uygulamasını uygulayın. Bu, sürekli yük altında sistem gecikmesini nasıl değiştirir?

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| PSO / 粒子群优化 | "Particle Swarm Optimization" / "粒子群优化" | Kennedy-Eberhart 1995. Population-based gradient-free optimizer. / Kennedy-Eberhart 1995。基于种群的无梯度优化器。 |
| ACO / 蚁群优化 | "Ant Colony Optimization" / "蚁群优化" | Dorigo 1992. Path/route optimization via pheromone trails. / Dorigo 1992。通过信息素轨迹的路径/路由优化。 |
| LMPSO / LLM 粒子群 | "PSO with LLM generation" / "LLM 生成的 PSO" | arXiv:2504.09247. Velocity is a prompt; LLM produces candidates. / arXiv:2504.09247。速度是提示；LLM 生成候选。 |
| Model Swarms / 模型群体 | "PSO on expert weights" / "专家权重的 PSO" | arXiv:2410.11163. Gradient-free update on model parameter subspace. / arXiv:2410.11163。模型参数子空间上的无梯度更新。 |
| AMRO-S / ACO Agent 路由 | "ACO for agent routing" / "Agent 路由的 ACO" | arXiv:2603.12933. Pheromone matrix over task-type × agent. / arXiv:2603.12933。任务类型 × Agent 的信息素矩阵。 |
| p_best / g_best / 个体最优/全局最优 | "Personal / global best" / "个人/全局最优" | Per-particle and swarm-wide best solutions found so far. / 每个粒子和群体目前找到的最优解。 |
| Pheromone / 信息素 | "Routing memory" / "路由记忆" | Strength on an edge; decays over time; deposits on quality. / 边上的强度；随时间衰减；按质量沉积。 |
| Quality-gated update / 质量门控更新 | "Only learn from good runs" / "只从好的运行学习" | Pheromone deposit conditioned on quality check. / 以质量检查为条件的信息素沉积。 |
| Catastrophic drift / 灾难性漂移 | "Distribution shift" / "分布偏移" | Fitness landscape changes; old p_best and pheromones become stale. / 适应度景观变化；旧的 p_best 和信息素变得过时。 |

## Daha fazla okumak

- [Kennedy & Eberhart — Particle Swarm Optimization](https://ieeexplore.ieee.org/document/488968) 1995 PSO kağıdı
- [Dorigo — Ant Colony Optimization](https://www.aco-metaheuristic.org/about.html)1992 ACO Vakfları
- [LMPSO — Language Model Particle Swarm Optimization](https://arxiv.org/abs/2504.09247) Struktürlü LLM çıkışları için PSO
- [Model Swarms — gradient-free LLM expert optimization](https://arxiv.org/abs/2410.11163) Model ağırlığı alt alanındaki PSO
- [AMRO-S — ant-colony multi-agent routing](https://arxiv.org/abs/2603.12933) Kalite kapısı ile feromon yönlendirme
