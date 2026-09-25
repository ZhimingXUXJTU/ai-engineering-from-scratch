# Monte Carlo Metodları  Tam bölümlerden öğrenmek  Monte Carlo Metodları  Tam döngüden öğrenmek

> Dinamik programlama bir modeli gerektirir. Monte Carlo'nun sadece bölümlere ihtiyacı var. Politikayı çalıştırın, getiriyi izleyin, ortalama yapın. RL 'deki en basit fikir ve her şeyi aşağıdaki akıntıda açan bir fikir.

> **【中文解读】**动态规划需要已知环境模型,蒙特卡洛只需要完整的回合数据:执行策略、观测回报、取平均──; RL'deki en basit düşünce, tüm son algoritmaların temel taşıdır.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Dinamik programlama zarif ama sorular sorulabilir.`P(s' | s, a)`Bu, bir robotun kamera piksellerinin dağılımını analizle hesaplayamadığı anlamına gelir. Bir fiyatlandırma algoritması her olası müşteri tepkisine dahil edemez. Bir LLM bir token sonrası tüm olası devamları sayamaz.

> Hareket planı çok güzel ama her durumu ve hareketini soruyorsun diye varsayıyorum.`P(s' | s, a)`◊ gerçekte neredeyse hiçbir şey böyle bir iş yapmıyor. ◊ makineler, ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊     ◊ ◊    ◊ ◊    ◊ ◊     ◊   ◊                                                                                                                                                  

Sadece çevreye örnek alma yeteneğine ihtiyacınız var.`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`- Değerleri tahmin etmek için kullan.

> Bir yöntemin olması gerekir.`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`Bu Monte Carlo'nun değeri.

DP'den MC'ye geçiş felsefi açıdan önemlidir: * bilinmiş modelden + tam yedekleme*'den * örnekle atılan uygulamalardan + ortalama geri dönüşe* geçiyoruz.

> DP'den MC'ye dönüşüm felsefede önemli: biz * bilinen modelden + kesin rezervuar * dönüşümden * örnek dağıtım + ortalama geri dönüş *: √ fark artmıştır, ancak uygulanabilirlik kapsamı patlak vererek artmıştır.

> **【中文解读】**DP'den MC'ye çekirdek dönüşüm: "bilinen model+ kesin hesaplama"dan "şöyle bir rota + ortalama geri dönüş"e kadar.

> **【拓展：LLM中的MC】**ChatGPT'nin RLHF ı eğitiminde, her bir soruya  çok sayıda cevap ̇ hesaplama ortalama ödül ̇ bu MC ı düşüncelerinin büyük model eğitiminde doğrudan uygulanmasıdır―DeepSeek-R1'in GRPO'sı da grup içi değerlendirmelere dayanan MC ı tahminlerdir―

## Konsepten bir şey.

![Monte Carlo: rollout, compute returns, average; first-visit vs every-visit](../assets/monte-carlo.svg)

**The core idea, in one line:** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`nerede`G^{(i)}(s)` ziyaretlerden sonra yapılan ziyaretler`s`Politikası altında`π`- Evet .

> **核心思想，一行概括：** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`, içinden `G^{(i)}(s)`- Evet .`π`Aşağı ziyaret`s`时观测到的回报──

> **【中文解读】**MC  değerlendirmesinin merkezi: durum değer = bu durumdan geçiş sırasında gözlemlenen geri dönüşlerin ortalama değerı。 ilk ziyaret MC sadece her döngüde ilk ziyaret geri dönüşünü, her ziyaret MC 统计所有访问――增量式平均值更新`V_new = V_old + α(target - V_old)`MC'den TD'ye tüm modern RL algoritması için bir köprü.

**First-visit vs every-visit MC.**Bir bölümü göz önüne alarak , devletin ziyaretlerini yapıyorlar .`s`İlk ziyaret MC'si sadece ilk ziyaretten gelen geri dönüşü sayır; her ziyaret MC tüm ziyaretleri sayır. Her ikisi de sınırda tarafsızdır. İlk ziyaret analiz etmek daha kolaydır (iid örnekleri). Her ziyaret bölüm başına daha fazla veri kullanır ve genellikle uygulamada daha hızlı bir şekilde birleşti.

> **首次访问 vs 每次访问 MC。**给定一个多次访问状态 `s`Bu nedenle, bu süreçte, ilk ziyaretlerin özetleri, ilk ziyaretlerin özetleri, ilk ziyaretlerin özetleri, ilk ziyaretlerin özetleri, ilk ziyaretlerin özetleri ve özetleri, ilk ziyaretlerin özetleri ve özetleri, ilk ziyaretlerin özetleri ve özetleri, ilk ziyaretlerin özetleri ve özetleri, ilk ziyaretlerin özetleri ve özetleri, ilk ziyaretlerin özetleri ve özetleri, ilk ziyaretlerin özetleri ve özetleri, ilk ziyaretlerin özetleri ve özetleri, ilk ziyaretlerin özetleri ve özetleri, ilk ziyaretlerin özetleri ve özetleri, ilk ziyaretlerin özetleri ve özetleri, ilk ziyaretlerin özetleri ve özetleri, her ziyaretin özetleri ve özetleri, her ziyaretin özetleri ve özetleri, genellikle daha hızlı olarak kullanılır.

**Incremental mean.**Tüm gönderileri depolamak yerine, çalışkan ortalamayı güncelle:

`V_n(s) = V_{n-1}(s) + (1/n) [G_n - V_{n-1}(s)]`

Yeniden düzenlenir: `V_new = V_old + α · (target - V_old)`- Evet .`α = 1/n`- Değiş .`1/n`sabit bir adım boyutu için `α ∈ (0, 1)`ve bir istasyonel olmayan MC tahmincisi elde edersiniz ki değişimleri izler `π`Bu hareket, MC'den TD'ye ve modern RL algoritmasına kadar bir atlama.

> **增量均值。**Tüm değerleri depolamıyor, ama yeni bir çalışma ortalama değerini.`1/n`替换为常数步长 `α ∈ (0, 1)`Bir izlemeyi bulmuştum.`π`Değişikliklerin dengesiz MC  hesaplama makinesi. Bu adım MC'den TD'ye tüm modern RL algoritmalarına kadar atlama.

**Exploration is now a problem.**DP, her eyalete sayım yoluyla dokundu. MC sadece eyaletlerin politika ziyaretlerini görüyor.`π`Bu durum, bir devlet alanının tüm bölgelerinin asla örneklenmemesi ve değer tahminleri sonsuza kadar sıfırda kalması anlamına gelir.

> **探索现在成了问题。**DP 通過枚举触及每個州──MC sadece strateji ziyaret statusını görebilir──如果`π`Bu, tüm durum alanının bölgesi olarak asla örneklenmeyeceği kesin bir şekilde belirlenmiştir.

> **【中文解读】**探索问题:DP 能遍历所有状态,MC sadece strateji ziyaret过的状态──如果策略是确定性的,大量状态永远不会被访问──三种解决方案:探索起点 (不实) ̇ε-贪心 (最常用) ̇离策略 MC (MK) ̇通过重要性采样从行为策略学习目标策略) ̇

1. **Exploring starts.**Her bölümü rastgele bir çiftten başlatın.
   **探索起点。**Her bir dönüm, bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıçtan bir başlangıç.
2. **ε-greedy.**Açgözlü davranın.`ε`Tüm durum eylem çiftleri asimptotik olarak örneklenir.
   **ε-贪心。**Şimdiki Q 贪心行动 için, ama olasılıkla `ε`随机选动作──所有状态动作对渐近地采样──
3. **Off-policy MC.**Davranış politikası çerçevesinde veriler toplayın `μ`, hedef politika hakkında bilgi edinmek `π`Yüksek farklılık, ama DQN gibi tekrar oynatma tamponu yöntemlerine bir köprü.
   **离策略 MC。**Davranış stratejisi`μ`Aşağıdaki verileri toplamak, öğrenme hedef stratejileri için önemlilik göstermek.`π`❖ Yüksek bir fark, ama DQN'ye giden bir köprü.

**Monte Carlo Control.**Değerlendirme → geliştirme → değerlendirme, politika tekrarlaması gibi, ancak değerlendirme örnekleme tabanlı:

1. Çık .`π`Bir bölüm al.
2. Güncelleme`Q(s, a)`Görülen sonuçlardan.
3. Yap .`π`E-cinsel açgözlülük.`Q`- Evet .
4. Tekrar ediyorum.

`Q*`ve `π*`Hafif koşullarda 1 olasılıkla (her çiftin sonsuz sıklıkla ziyaret edildiği)`α`Robbins-Monro'yu tatmin eder.

> **蒙特卡洛控制。**评估 → 改进 → 评估,就像策略代,但评估基于采样──在温和条件下对被无限次访问,`α`满足 Robbins-Monro), 概率 1 收到`Q*`和 `π*`- Evet.

## Yapın.
```figure
epsilon-greedy
```

## Yapın

### Adım 1: başlat → listesi (s, a, r)

```python
def rollout(env, policy, max_steps=200):
    trajectory = []
    s = env.reset()
    for _ in range(max_steps):
        a = policy(s)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r))
        s = s_next
        if done:
            break
    return trajectory
```

- Model yok, sadece.`env.reset()`ve `env.step(s, a)`Spor ortamı gibi aynı arayüz ama soyulmuş.

> Model gerekmiyor, sadece gerek.`env.reset()`和 `env.step(s, a)`                                                                                                                                                                                                                                                              

### Adım 2: Hesaplama sonuçları (geri tarama)

```python
def returns_from(trajectory, gamma):
    returns = []
    G = 0.0
    for _, _, r in reversed(trajectory):
        G = r + gamma * G
        returns.append(G)
    return list(reversed(returns))
```

Bir geçiş.`O(T)`Geriye dönme .`G_t = r_{t+1} + γ G_{t+1}`Yeniden toplama yapmaktan kaçınır.

> Bir kere,`O(T)`❖ Geri dönüş`G_t = r_{t+1} + γ G_{t+1}`避免了重复求和──

### Adım 3: İlk ziyaret MC değerlendirme

```python
def mc_policy_evaluation(env, policy, episodes, gamma=0.99):
    V = defaultdict(float)
    counts = defaultdict(int)
    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for t, ((s, _, _), G) in enumerate(zip(trajectory, returns)):
            if s in seen:
                continue
            seen.add(s)
            counts[s] += 1
            V[s] += (G - V[s]) / counts[s]
    return V
```

İş üç satırla yapılır: ilk ziyarette görüldüğü gibi işaret durumunu, artış sayısını, güncelleme çalıştırma ortalamasını.

> Üç行代码完成工作:标记首次访问的状态,增加计数,更新运行平均值──

### Dördüncü adım: E-cinsel MC kontrolü (politikal)

```python
def mc_control(env, episodes, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    counts = defaultdict(lambda: {a: 0 for a in ACTIONS})

    def policy(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for (s, a, _), G in zip(trajectory, returns):
            if (s, a) in seen:
                continue
            seen.add((s, a))
            counts[s][a] += 1
            Q[s][a] += (G - Q[s][a]) / counts[s][a]
    return Q, policy
```

### Adım 5: DP altın standardı ile karşılaştır

MC tahmininiz`V^π`Ders 02'nin DP sonuçlarıyla aynı fikirde olmalısınız.`~0.1`DP cevabının.

> Sen de öyle .`V^π`∞ 时应 → ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞`~0.1`İçinde.

## Tuzaklar

- **Infinite episodes.**MC'nin bölümleri sona erdirmesi gerekiyor.`max_steps`GridWorld'in rastgele politikası normal olarak 'yi çıkartır.
  **无限回合。**MC 要求回合*终止*──如果策略可能永远循环,设置 `max_steps`Üst sınır ise, gizli bir başarısızlık olarak görülecek.
- **Variance.**MC'nin tam geri dönüşleri kullanıyor. Uzun bölümlerde, fark büyük  bir şanssız ödül sonunda varyasyon `V(s_0)`TD yöntemleri (Leçon 04) bunu bootstrapping ile azaltıyor.
  **方差。**MC kullanın tam geri dönüş. Uzun geri dönüşler üzerinde büyük bir fark var. Son adımın uğursuzluk ödülleri de aynı derecede etkilidir.`V(s_0)`◊TD 方法(Desin 04) kendi kendine hareket ederek ◊
- **State coverage.**Açgözlü MC'ler, yeni bir Q'da bir kere bir şey yapmayı deneyecekler.
  **状态覆盖。**Yeni Q 上的贪心 MC Sadece bir hareket dener.
- **Non-stationary policies.**- Eğer`π`Bu durumlar, sürekli-α MC tarafından ele alınırken örnek ortalama MC tarafından ele alınmaz.
  **非平稳策略。**Eğer `π`变化(如 MC 控制中),旧回报来自不同策略──常数 α MC 处理此问题;样本平均 MC 不能──
- **Off-policy importance sampling.**Ağırlıkları .`π(a|s)/μ(a|s)`Bir yörüngede çarpma. Varians ufukta patlar. Kapı, karar başına ağırlıklı IS veya TD'ye geçiş.
  **离策略重要性采样。**权重 `π(a|s)/μ(a|s)`Yolda bir aralıklı bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir aralıkla bir saldırı ile bir saldırı ile bir saldırı ile bir saldırı ile bir saldırı ile karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı

## Çerçeveyi kullanın.

2026 Monte Carlo yöntemlerinin rolü:

> 2026 yılında Monte Carlo'nun rolü:

| Use case | Why MC |
|----------|--------|
| Use case / 用例 | Why MC / 为什么用 MC |
| Short-horizon games (blackjack, poker) / 短视野游戏（二十一点、扑克） | Episodes terminate naturally; returns are clean. / 回合自然终止；回报干净。 |
| Offline evaluation of a logged policy / 离线评估已记录的策略 | Average discounted returns over stored trajectories. / 对存储轨迹取折扣回报平均。 |
| Monte Carlo Tree Search (AlphaZero) / 蒙特卡洛树搜索 | MC rollouts from tree leaves guide selection. / 树叶的 MC rollout 指导选择。 |
| LLM RL evaluation / LLM RL 评估 | Compute average reward over sampled completions for a given policy. / 对给定策略的采样完成计算平均奖励。 |
| Baseline estimation in PPO / PPO 中的基线估计 | The advantage target `A_t = G_t - V(s_t)` uses an MC `G_t`. / 优势目标使用 MC 的 `G_t`。 |
| Teaching RL / 教学 RL | Simplest algorithm that actually works — strip bootstrapping to see the core. / 最简单且有效的算法——去掉自举看核心。 |

Modern derin-RL algoritmaları (PPO, SAC) saf MC (tam geri dönüş) ve saf TD (bir adımlı başlangıç) arasında aralar.`n`- step return veya GAE. Her iki uç noktası da aynı tahminçinin örnekleri.

> 现代深度 RL 算法(PPO、SAC) geçiş`n`步回报或 GAE 在纯 MC (M) 完整回报) 和纯 TD (TD) 单步自举) 间插值──两端点都是同一估计器的实例──

## İndirin . Ürünler .

- Kaydet .`outputs/skill-mc-evaluator.md`- ...

```markdown
---
name: mc-evaluator
description: Evaluate a policy via Monte Carlo rollouts and produce a convergence report with DP-comparison if available.
version: 1.0.0
phase: 9
lesson: 3
tags: [rl, monte-carlo, evaluation]
---

Given an environment (episodic, with reset+step API) and a policy, output:

1. Method. First-visit vs every-visit MC. Reason.
2. Episode budget. Target number, variance diagnostic, expected standard error.
3. Exploration plan. ε schedule (if needed) or exploring starts.
4. Gold-standard comparison. DP-optimal V* if tabular; otherwise a bound from a Q-learning / PPO baseline.
5. Termination check. Max-step cap, timeouts, handling of non-terminating trajectories.

Refuse to run MC on non-episodic tasks without a finite horizon cap. Refuse to report V^π estimates from fewer than 100 episodes per state for tabular tasks. Flag any policy with zero-variance actions as an exploration risk.
```

## Egzersizler.

1. **Easy.**4×4 GridWorld'da ilk ziyaret MC değerlendirmesini uygulayın. 10.000 bölüm çalıştırın.`V(0,0)`Bölüm sayısının DP cevabına göre bir fonksiyonu olarak.
   > **练习1：**实现 MC 评估,将 V(0,0) 随回合数的收曲线与 DP 基准对比──
2. **Medium.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `ε ∈ {0.01, 0.1, 0.3}`20.000 bölümden sonra ortalama geri dönüşü karşılaştırın.
   > **练习2：**Ül farklı ε  değer yapmak MC  kontrol, observar explorar-utilizer权衡。
3. **Hard.***Politik dışı* MC'yi önemli örnekleme ile uygula: Teker teker rastgele politika çerçevesinde veriler toplamak `μ`, tahmin`V^π`Determinizm en iyi politika için `π`- Basit IS vs. Kararlama IS vs. Ağır IS. En düşük varyansa hangisi?
   > **练习3：**实现离策略 MC 重要性采样), karşılaştırmak farklı 方差的差异──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Monte Carlo | "Random sampling" / 蒙特卡洛 | Estimate expectations by averaging over iid samples from the distribution. |
| Return `G_t` | "Future reward" / 回报 | Sum of discounted rewards from step `t` to episode end: `Σ_{k≥0} γ^k r_{t+k+1}`. |
| First-visit MC | "Count each state once" / 首次访问 MC | Only the first visit in an episode contributes to the value estimate. |
| Every-visit MC | "Use all visits" / 每次访问 MC | Every visit contributes; slightly biased but more sample-efficient. |
| ε-greedy | "Exploration noise" / ε-贪心 | Pick greedy action with prob `1-ε`; random action with prob `ε`. |
| Importance sampling | "Correcting for sampling from the wrong distribution" / 重要性采样 | Reweight returns by `π(a\|s)/μ(a\|s)` products to estimate `V^π` from `μ` data. |
| On-policy | "Learn from my own data" / 在线策略 | Target policy = behavior policy. Vanilla MC, PPO, SARSA. |
| Off-policy | "Learn from someone else's data" / 离线策略 | Target policy ≠ behavior policy. Importance-sampled MC, Q-learning, DQN. |

## Daha fazla okumak

- [Sutton & Barto (2018). Ch. 5 — Monte Carlo Methods](http://incompleteideas.net/book/RLbook2020.pdf) Kanonik tedavi.
- [Singh & Sutton (1996). Reinforcement Learning with Replacing Eligibility Traces](https://link.springer.com/article/10.1007/BF00114726) İlk ziyaret vs. her ziyaret analizleri.
- [Precup, Sutton, Singh (2000). Eligibility Traces for Off-Policy Policy Evaluation](http://incompleteideas.net/papers/PSS-00.pdf) politika dışı MC ve varyansa kontrolü.
- [Mahmood et al. (2014). Weighted Importance Sampling for Off-Policy Learning](https://arxiv.org/abs/1404.6362) Modern düşük varyasyonlı IS tahmincileri.
- [Tesauro (1995). TD-Gammon, A Self-Teaching Backgammon Program](https://dl.acm.org/doi/10.1145/203330.203343) MC/TD kendi oyununun insanüstü oyunlara doğru yaklaşıp ilk büyük ölçekli deneyimli gösterimi; bu aşamanın ikinci yarısında her dersin kavramsal öncüsü.
