# Dinamik Programlama  Politika İterasyonu ve Değer İterasyonu  动态规划  策略代与价值代

> Dinamik programlama, aldatmacılık ile RL'dir.`V`veya `π`Bu, her örnekleme tabanlı yöntemin yaklaşmaya çalıştığı referans değeridir.

> **【中文解读】**动态规划是强化学习的"作弊版"你已知环境的转移概率和奖励函数, sadece karşılama olana kadar反复代 Bellman 方程.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs) | **前置知识:** Phase 9 · 01 (MDP)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Bilinen bir modelle bir MDP 'ye sahipsiniz: sorguya girebilirsiniz `P(s' | s, a)`ve `R(s, a, s')`Bu, bir envanter yöneticisi olarak talep dağılımını bilir. bir masa oyunu belirlenmiş geçişler vardır. bir gridworld Python'un dört satırı.

> Bilinen bir modelin var . Herhangi bir durum soruyabilirsiniz .`P(s' | s, a)`和 `R(s, a, s')` Depo yöneticisi ihtiyaç dağılımını bilir.  Çeviri dünyası işte Python'un dört safı.

Modelsiz RL (Q-learning, PPO, REINFORCE) bir modeliniz olmadığı durum için icat edildi.  Sadece çevreye örnek alabilirsiniz. Ama bir tane olduğunda, daha hızlı, daha iyi yöntemler vardır: dinamik programlama. Bellman onları 1957'de tasarladı.

> 无模型 RL(Q-learning、PPO、REINFORCE) modelsiz bir durum için ortaya çıkarılmış bir durumdur. Ancak modeliniz olduğunda daha hızlı ve daha iyi bir yöntem vardır:

> **【中文解读】**Eğer bildiğiniz çevresel modelde ([[Transfer Probability and Reward Function]]), hareket planlaması en iyi stratejileri belirleyebilir.

> **【拓展：AlphaZero/MCTS】**AlphaZero'nun Monte Carlo Tree Search (MCTS) özünde Bellman'ın farklı bir versiyonu.

2026'da üç nedenden dolayı ihtiyaç duyarsınız. Birincisi, RL araştırmalarında her tablo ortamı (GridWorld, FrozenLake, CliffWalking) altın standart politikasını üretmek için DP ile çözülür.`V*(s_0)`Üçüncü olarak, modern çevrimdışı RL ve planlama yöntemleri (MCTS, AlphaZero'nun arama, 9. · 10 aşamada model tabanlı RL) hepsi Bellman yedeklemeyi öğrenilen veya verilen bir model üzerinde tekrarlar.

> 2026 yılında ihtiyaç duyarsınız, neden var. 1.,RL araştırmasında her bir tablo ortamı (GridWorld, FrozenLake, CliffWalking) kullanmak için DP'yi kullanın.`V*(s_0)`%30'luk bir fark var. Q öğrenme konusunda bir hata var.

## Konsepten bir şey.

![Policy iteration and value iteration, side by side](../assets/dp.svg)

**Two algorithms, both fixed-point iteration on Bellman.**

> **两种算法，都是对 Bellman 方程做不动点迭代。**

> **【中文解读】**两种算法都是对贝尔曼方程做不动点代――策略代:交替执行"策略评估"和"策略改进"直到策略不变; 价值代:将两者合并为一步,直接取 max――两者最终收到同一个优值函数 V*──

**Policy iteration.**Politika değişmezken iki adım değiştiriyor.

> **策略迭代。**Bu iki adım yerine getirmek için, strateji değişmediği sürece.

1. *Değerlendirme:* belirli politika `π`, hesaplama`V^π`Tekrar tekrar uygulayarak `V(s) ← Σ_a π(a|s) Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`Bir araya gelene kadar.
   * değerlendirmek:* 给定策略 `π`Bellman'ın yöntemini tekrar tekrar uygula .`V^π`- Evet.
2. *Yenileştirme:* verildi `V^π`, yapın`π`Açgözlü bir hırsızlık .`V^π`- Evet .`π(s) ← argmax_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`- Evet .
   *改进:* 给定 `V^π`,让 `π`- Evet .`V^π`Kötü bir kalp.

Dönüşüm garanti edilir çünkü (a) her iyileştirme aşamasında ya `π`Aynı veya sıkı bir şekilde artıyor `V^π`Bazı devletler için (b) belirleyici politikaların alanı sınırlıdır. Genellikle büyük devlet alanları için bile ~520 dış iterasyonlarda birleşti.

> -Gülüşme garantilidir. Çünkü her gelişme yapılırsa yapılır.`π`Değişmez, ya da ciddi bir şekilde bir durum artırmak için.`V^π`,(b) 确定性策略空間有限── hatta büyük bir durum alanı için de genellikle sadece ~5-20 kez dış katman 代──

**Value iteration.**Değerlendirme ve iyileştirme bir süpürgeye çöküyor. Bellman * optimizasyon * denklemini uygulayın:

`V(s) ← max_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`

`max_s |V_{new}(s) - V(s)| < ε`. Açgözlü eylemleri yaparak son politika çıkar. Yeterlikçe daha hızlı  iç değerlendirme döngüsü  ama genellikle daha fazla iterasyon konverje gerekir.

> **值迭代。**Bu yöntemin uygulanması için Bellman * en iyi * yöntemini uygulayacağız.

**Generalized policy iteration (GPI).**Birleştiren çerçeveleme. Değer fonksiyonu ve politika iki yönlü bir geliştirme döngüsünde kilitlenir; her iki yönü de karşılıklı tutarlılığa (asynk değer iterasyonu, değiştirilmiş politika iterasyonu, Q-öğrenme, aktör eleştirmeni, PPO) yönlendiren herhangi bir yöntem GPI'nin bir örneğidir.

> **【拓展：GPI→PPO/RLHF】**广义策略代 (GPI) 统一框架:Q-learning、Actor-Critic、PPO aslında GPI'nin bir örneğilerdir. DP'nin GPI'sini anladın, ChatGPT'nin arkasındaki RLHF 訓練循环'nun tasarım felsefesini anladın.

**Why `γ < 1` matters.**Bellman operatörü bir `γ`-Sup-norm'daki kısıtlama: `||T V - T V'||_∞ ≤ γ ||V - V'||_∞`-Kısıtlama, benzersiz sabit nokta ve geometrik bir yakınlık anlamına gelir.`γ < 1`Ve garantiyi kaybedersen... ...bir sınırlı ufaklık veya absorber bir terminal durum gerekir.

> **为什么 `γ < 1` 很重要。**Bellman'ın hesapları çok düşük .`γ`- basınç haritası. basınç tek hareketsiz nokta ve geometrik bir değer anlamına gelir.`γ < 1`Sınırlı bir bakış ve akış açısı durumuna ihtiyacın var.

## Yapın.
```figure
value-iteration-gamma
```

## Yapın

### Adım 1: GridWorld MDP modeli oluştur

Ders 1'den aynı 4×4 GridWorld'u kullanın.`0.1`ajan rastgele dik yönde kayar.

> Ders 01'de aynı 4×4 GridWorld kullanalım.`0.1`智能体会滑向随机垂直方向──

```python
SLIP = 0.1

def transitions(state, action):
    if state == TERMINAL:
        return [(state, 0.0, 1.0)]
    outcomes = []
    for direction, prob in action_probs(action):
        outcomes.append((apply_move(state, direction), -1.0, prob))
    return outcomes
```

`transitions(s, a)` listesi gönderir`(s', r, p)`Bu tüm model.

> `transitions(s, a)`Geri dön .`(s', r, p)`Bu, tüm model.

### Adım 2: Politika değerlendirme

Bir politika göre .`π(s) = {action: prob}`, Bellman denklemini tekrarlayalım .`V`hareket etmeyi durdurur:

> 给定策略 `π(s) = {action: prob}`Bellman'ın yolundan.`V`İçeğişmez:

```python
def policy_evaluation(policy, gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = sum(pi_a * sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a))
                   for a, pi_a in policy(s).items())
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            return V
```

### Adım 3: Politikayı iyileştirmek

Değiştir `π`Açgözlü politika ile.`V`- Eğer ...`π`Değişmemiş, geri dönmüş  en iyisindeyiz.

> - Ben de .`π`替换为对 `V`Kötü bir yöntem.`π`Değişiklik yok, geri dönmek en iyisini elde etti.

```python
def policy_improvement(V, gamma=0.99):
    new_policy = {}
    for s in states():
        best_a = max(
            ACTIONS,
            key=lambda a: sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a)),
        )
        new_policy[s] = best_a
    return new_policy
```

### Dördüncü adım: Bir araya getirin

```python
def policy_iteration(gamma=0.99):
    policy = {s: "up" for s in states()}   # arbitrary start
    for _ in range(100):
        V = policy_evaluation(lambda s: {policy[s]: 1.0}, gamma)
        new_policy = policy_improvement(V, gamma)
        if new_policy == policy:
            return V, policy
        policy = new_policy
```

4×4: 46 dış iterasyonlarında tipik bir yakınlık.`V*(0,0) ≈ -6`Ve adım sayısını kesinlikle azaltan bir politika.

> 4×4 上的典型收:4-6 次外层代──输出 `V*(0,0) ≈ -6`Ve bir ciddi adım sayısını azaltma stratejisi.

### Adım 5: değer iterasyonu (bir döngü versiyonu)

```python
def value_iteration(gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = max(sum(p * (r + gamma * V[s_prime])
                       for s_prime, r, p in transitions(s, a))
                   for a in ACTIONS)
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            break
    policy = policy_improvement(V, gamma)
    return V, policy
```

Aynı sabit nokta, daha az kod satırı.

> Aynı hareket noktası, daha az kod numarası.

## Tuzaklar

- **Forgetting to handle terminals.**Bellman'ı emekçi bir duruma uyguladığınızda, hiçbir şey değiştirmeyen "en iyi eylem" alır.`if s == terminal: V[s] = 0`- Evet .
  **忘记处理终止状态。**Eğer Bellman'ın en iyi hareketini kullanırsa, hiçbir şey değişmez.`if s == terminal: V[s] = 0`保护。
- **Sup-norm vs L2 convergence.**Kullanım`max |V_new - V|`Teorik garanti sup-norma üzerinde.
  **Sup 范数 vs L2 收敛。**Kullanım`max |V_new - V|`, ve ortalama değeri değil.
- **In-place vs synchronous updates.**Güncelleme`V[s]`Yerde (Gauss-Seidel) ayrı bir `V_new`Üretim kodu yerinde kullanılıyor.
  **原地更新 vs 同步更新。**Yenilemeler`V[s]`(Gauss-Seidel) Tek başına kullanılır.`V_new`字典(Jacobi)收更快──生产代码使用原地更新──
- **Policy ties.**Eğer iki işlem aynı Q değeri varsa,`argmax`Her iterasyonda farklı şekilde bağları kırmak, "politik istikrarlı" kontrolünün oscilansına neden olabilir.
  **策略平局。**Eğer iki hareketin Q  değerleri ve benzeri`argmax`Her seferinde farklı bir şekilde düzeni kırmak mümkündür, bu da "taktiği sabit" kontrol dalgalanmasına neden olur.
- **State-space explosion.**DP `O(|S| · |A|)`Bu işlemler, 107. durumlara kadar çalışmaktadır.
  **状态空间爆炸。**DP her tarama için`O(|S| · |A|)`△ Yaklaşık 107 个 durum için uygulanmaktadır.

## Çerçeveyi kullanın.

2026 yılında DP, planlamacıların doğruluk başlangıç çizgisi ve iç döngüsüdür:

> 2026 yılında, DP, doğru bir temel ve planlayıcı iç döngüsüdür:

| Use case | Method |
|----------|--------|
| Use case / 用例 | Method / 方法 |
| Solve a small tabular MDP exactly / 精确求解小型表格 MDP | Value iteration (simpler) or policy iteration (fewer outer steps) / 值迭代（更简单）或策略迭代（更少外层步数） |
| Verify a Q-learning / PPO implementation / 验证 Q-learning/PPO 实现 | Compare to DP-optimal V* on a toy environment / 在玩具环境上与 DP 最优 V* 比较 |
| Model-based RL (Phase 9 · 10) / 基于模型的 RL | Bellman backup on a learned transition model / 在学习的转移模型上做 Bellman 备份 |
| Planning in AlphaZero / MuZero / AlphaZero/MuZero 中的规划 | Monte Carlo Tree Search = async Bellman backup / MCTS = 异步 Bellman 备份 |
| Offline RL (CQL, IQL) / 离线 RL | Conservative Q-iteration — DP with a penalty on OOD actions / 保守 Q 迭代——对 OOD 动作加惩罚的 DP |

Birisi "optimal değer fonksiyonu" dediğinde, "DP sabit noktası" demek istiyorlar.`V*`veya `Q*`Bir kağıtda, bu döngüyü hayal edin.

> Her zaman birisi "en iyi değerli işlevi" diyor, onlar "DP hareket noktası" anlamına gelir.`V*`Ya da`Q*`Bu döngüyü düşün.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-dp-solver.md`- ...

```markdown
---
name: dp-solver
description: Solve a small tabular MDP exactly via policy iteration or value iteration. Report convergence behavior.
version: 1.0.0
phase: 9
lesson: 2
tags: [rl, dynamic-programming, bellman]
---

Given an MDP with a known model, output:

1. Choice. Policy iteration vs value iteration. Reason tied to |S|, |A|, γ.
2. Initialization. V_0, starting policy. Convergence sensitivity.
3. Stopping. Sup-norm tolerance ε. Expected number of sweeps.
4. Verification. V*(s_0) computed exactly. Greedy policy extracted.
5. Use. How this baseline will be used to debug/evaluate sampling-based methods.

Refuse to run DP on state spaces > 10⁷. Refuse to claim convergence without a sup-norm check. Flag any γ ≥ 1 on an infinite-horizon task as a guarantee violation.
```

## Egzersizler.

1. **Easy.**4×4 GridWorld'de değer iterasyonunu  ile çalıştır`γ ∈ {0.9, 0.99}`- Ne kadar süpürür ?`max |ΔV| < 1e-6`- Baskı`V*`4×4 şebekesi olarak.
   > **练习1：**Farklı indirim faktörleri ile, nasıl değişeceğini gözlemleyin.
2. **Medium.*** Stochastic* GridWorld'de politika iterasyonu vs değer iterasyonu karşılaştırın (slip olasılığı `0.1`Sayım: süpürmeler, duvar saati, son `V*(0,0)`- Hangi süreler daha hızlı bir şekilde dönüşüyor?
   > **练习2：**代数和运行时间) 代数和运行时间) 代数和运行时间) 代数和运行时间) 代数和运行时间 (代数和运行时间) 代数和运行时间 (代数和运行时间) 代数和运行时间 (代数和运行时间) 代数和运行速度) 代数和运行时间 (代数和运行时间) 代数和运行速度 (代数和运行时间) 代数和运行时间) 代数
3. **Hard.**Değiştirilmiş politika tekrarını oluştur: değerlendirme aşamasında sadece çalıştır `k`- Birleştirilmek yerine tarar.`V*(0,0)`hata vs `k`için`k ∈ {1, 2, 5, 10, 50}`Bu eğrilik değerlendirme/iyileştirme karşılığı hakkında size ne söylüyor?
   > **练习3：**                                                                                                                                                                                                                                                              

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy iteration | "DP algorithm" / 策略迭代 | Alternating evaluation (`V^π`) and improvement (greedy `π` w.r.t. `V^π`) until the policy stops changing. |
| Value iteration | "Faster DP" / 值迭代 | Bellman optimality backup applied in one sweep; converges to `V*` geometrically. |
| Bellman operator | "The recursion" / Bellman 算子 | `(T V)(s) = max_a Σ P (r + γ V(s'))`; a `γ`-contraction in sup-norm. |
| Contraction | "Why DP converges" / 压缩映射 | Any operator `T` with `\|\|T x - T y\|\| ≤ γ \|\|x - y\|\|` has a unique fixed point. |
| GPI | "Everything is DP" / 广义策略迭代 | Generalized Policy Iteration: any method driving `V` and `π` to mutual consistency. |
| Synchronous update | "Jacobi-style" / 同步更新 | Use old `V` throughout a sweep; cleanly analyzable but slower. |
| In-place update | "Gauss-Seidel-style" / 原地更新 | Use `V` as it's being updated; converges faster in practice. |

## Daha fazla okumak

- [Sutton & Barto (2018). Ch. 4 — Dynamic Programming](http://incompleteideas.net/book/RLbook2020.pdf) politika iterasyonunun ve değer iterasyonunun kanonik sunumu.
- [Bertsekas (2019). Reinforcement Learning and Optimal Control](http://www.athenasc.com/rlbook.html) Kısalaşma haritası argümanlarının sıkı şekilde ele alınması.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887) modifi politikayı tekrarlama ve onun yakınlaştırma analizi.
- [Howard (1960). Dynamic Programming and Markov Processes](https://mitpress.mit.edu/9780262582300/dynamic-programming-and-markov-processes/) orijinal politika tekrarlama kağıdı.
- [Bertsekas & Tsitsiklis (1996). Neuro-Dynamic Programming](http://www.athenasc.com/ndpbook.html) DP'den yaklaşık DP/ derin RL'ye kadar her sonraki dersde kullanılan köprü.
