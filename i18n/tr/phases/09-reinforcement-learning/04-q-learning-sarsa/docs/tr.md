# Zaman Farkı  Q-Learning & SARSA  时序差分  Q öğrenmek ve SARSA

> Monte Carlo, bölümün sonunu bekliyor. TD, bir sonraki değer tahminini başlatarak her adımdan sonra güncelleyecek. Q-öğrenme politika dışı ve iyimser; SARSA politika içindedir ve dikkatlidir. Her ikisi de bir kod satırı. Her iki yöntemi bu aşamada derin-RL yönteminin temelini oluşturur.

> **【中文解读】**MC'nin yenilemesini beklemek için bir dönümün sonuna kadar beklemek zorundadır.`r + γ V(s')`作为目标来引导当前估计;;Q-learning is离策略的;;学习最佳策略的),SARSA is在线策略的;;学习当前行为策略的;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;`max`Ama tüm derinliklerin temeli bu.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming), Phase 9 · 03 (Monte Carlo) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划), Phase 9 · 03 (蒙特卡洛)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Monte Carlo çalışıyor ama iki pahalı talebe sahiptir. Son bölümlerin sona ermesi gerekiyor ve son dönüşün geldiği zaman güncelleştirilir. Eğer bölümünüz 1000 adım ise MC herhangi bir şeyi güncellemek için 1.000 adım bekler. Yüksek çeşitlilik, düşük önyargı ve pratikte yavaş.

> Monte Carlo geçerlidir ama iki pahalı gereksinim var. Son döngüye ihtiyaç vardır ve son döngü çıkışından sonra yenilebilir. Eğer döngü 1.000 adım varsa, MC herhangi bir şeyi yenilemek için 1.000 adım beklemek gerekir.

Dinamik programlamanın ters profilü vardır  sıfır varyasyonlı bootstrapped yedekleme  ancak bilinen bir modeli gerektirir.

> 动态规划 has opposite features 零方差的自举备份 但需要已知模型

Zaman farkı (TD) öğrenme farkı ayırır.`(s, a, r, s')`, tek adımlı bir hedef oluşturun .`r + γ V(s')`Ve itmek .`V(s)`- Model yok, episodlar yok, yaklaşık bir kısım kullanmaktan dolayı.`V`RHS'de, ancak MC ve çevrimiçi güncellemelerden çok daha düşük bir değişim.

> 时序差分(TD) öğrenme dönemi iki arasında.`(s, a, r, s')`构建单步目标 `r + γ V(s')`,将 `V(s)`Yakınlığa doğru, model gerektirmez, tam bir çevre gerektirmez, çünkü sağ tarafta yakınlık kullanılır.`V`Bu, bir diğer gelişme ve gelişme yoluyla gerçekleşir.

Bu modern RL  DQN, A2C, PPO, SAC 'nin dönüşü olan bir merkezdir. 9. Fase'nin geri kalanı bu dersde yazacağınız tek adımlı TD güncelleme üzerine inşa edilen fonksiyon yaklaşımını ve hilelerini oluşturur.

> Bu tüm modern RLDQN、A2C、PPO、SAC'un merkezidir. 9. aşamalın geri kalanı bu ders içinde yazacağınız tek aşamalı TD 更新 üzerinde inşa edilen işlev yaklaşım ve teknik katmanında bulunmaktadır.

> **【中文解读】**TD öğrenimi DP ve MC'nin bir parçasıdır: tek adımla dönüşüm`(s,a,r,s')`构建目标 `r + γV(s')`, model gerektirmez, tam bir çevrim gerektirmez.

> **【拓展：游戏AI→LLM对齐】**Q-öğrenme, 2013 yılında Atari DQN'in merkezinde, derinlik RL 时代'yi başlattı.PPO, ChatGPT RLHF öğrenme çekirdeği algoritmasıdır.

## Konsepten bir şey.

![Q-learning vs SARSA: off-policy max vs on-policy Q(s', a')](../assets/td.svg)

**The TD(0) update for V:**

`V(s) ← V(s) + α [r + γ V(s') - V(s)]`

Çekilen miktar TD hatasıdır `δ = r + γ V(s') - V(s)`Bu internet analogi .`G_t - V(s_t)`MC'de. Dönüşüm gerektirir.`α`Robbins-Monro'nun hoşnutluğunu`Σ α = ∞`- Evet .`Σ α² < ∞`) ve tüm eyaletler sonsuz sıklıkla ziyaret edildi.

> **V 的 TD(0) 更新：**括号中的量是 TD 误差 `δ = r + γ V(s') - V(s)`MC'de.`G_t - V(s_t)`Bu konuda bir çok şey var.`α`满足 Robbins-Monro 条件且所有状态被无限次访问──

**Q-learning.**Kontrol için politika dışı bir TD yöntemi:

`Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)]`

- Evet .`max`* açgözlülük* politikası takip edileceğini varsayır.`s'`Bu kopyalanma, Q öğrenmeyi öğrenir.`Q*`Mnih et al. (2015) bunu Atari'de derin Q öğrenimine dönüştürdü (Desin 05).

> **Q-learning。**Bir farklı strateji TD  kontrol yöntemi`max`假设从 `s'`開始將遵循*貪心*策略,無論智能體實際上采取什麼動作──這種解使Q-learning在通過 ε-貪心探索的同時學習`Q*`❖Mnih 等人 (2015) bunu Atari 上的深度 Q-learning olarak dönüştürecek.

**SARSA.**Politikada TD yöntemi:

`Q(s, a) ← Q(s, a) + α [r + γ Q(s', a') - Q(s, a)]`

Adı tuple .`(s, a, r, s', a')`SARSA bu eylemden yararlanıyor .`a'`*Agent* gerçekte* # # sonra alır, açgözlü değil.`argmax`- Dönüştüğü`Q^π`- Ne kadar açgözlüyse .`π`- Evet. - Evet.`ε → 0``Q*`- Evet .

> **SARSA。**Bir çeşit çevrimiçi strateji TD 方法──名称是元组 `(s, a, r, s', a')`◊SARSA 使用智能体*实际*采取的下一个动作 `a'`Ve açgözlülükten başka .`argmax`❖ 收到当前 ε-贪心 `π``Q^π`, `ε → 0`                                                                                                                                                                                                                                                              `Q*`- Evet.

**The cliff-walking difference.**Klasik uçurum yürüyüşü görevinde (kuşağın düşmesi = ödül -100), Q-öğrenme uçurum kenarında en iyi yolu öğrenir, ancak ara sıra keşif sırasında ceza alır. SARSA, keşif gürültüsünü Q değerine dahil ettiği için uçurumdan bir adım uzakta daha güvenli bir yol öğrenir.`ε → 0`. Pratikte önemli: keşif gerçekte yerleştirilmekteyken, SARSA'nın davranışları daha muhafazakârdır.

> **【中文解读】**Klasik tepesi yürüyüş deneyi, Q-öğrenme ve SARSA'nın önemli farkını ortaya koydu: Q-öğrenme, tepeden en iyi yolu öğrenmek için, ancak keşfetmek zaman düşer, SARSA, uçurumun güvenli yollarını öğrenmek için, çünkü gürültü keşfetmeyi düşünüyor.

**Expected SARSA.**Değiştir `Q(s', a')`Beklenen değeri `π`- ...

`Q(s, a) ← Q(s, a) + α [r + γ Σ_{a'} π(a'|s') Q(s', a') - Q(s, a)]`

SARSA' dan daha düşük bir varyansa (sırın `a'`Bu, modern ders kitaplarında genellikle standart olarak kullanılır.

> **期望 SARSA。**Kullan .`π`Aşağıdaki beklenmedik değer değişimi`Q(s', a')`◊ SARSA 方差更低 无需采样 `a'`), aynı online strateji hedefleri── her zaman modern öğretim kitaplarının belirlenmiş seçimi──

**n-step TD and TD(λ).**TD(0) ve MC arasında bekleme yoluyla aralaştır `n`Baştan çıkmadan önce adımlar atın. `n=1`TD'dir.`n=∞`MC. TD(λ) ortalamaları tüm `n`Geometri ağırlıkları ile `(1-λ)λ^{n-1}`En çok derin RL kullanımı`n`3 ila 20 arasında.

> **n 步 TD 和 TD(λ)。**TD(0) ve MC  arasındaki değer, bekleyin `n`步再自举──`n=1`Evet TD,`n=∞`Evet, her şeyi kontrol edeceğim.`n`取平均──大多数深度 RL 使用 `n`3 ila 20 arasında.

> **【拓展：TD 误差在 LLM RLHF 中的对应】**TD 误差 δ = r + γV(s') - V(s) LLM'de RLHF 訓練中直接对应:PPO'nun üstünlük işlevi A = r + γV(s') - V(s) İşte TD 误差の变体──每生成一个代币,计算当前代币的奖励──来自RM) 加上评论对未来价值的估计减算减算──理解 TD 误差是理解PPO 优势函数的关键──

## Yapın.
```figure
qlearning-gridworld
```

## Yapın

### Adım 1: Kıskançlık politikası üzerine SARSA

```python
def sarsa(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})

    def choose(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        s = env.reset()
        a = choose(s)
        while True:
            s_next, r, done = env.step(s, a)
            a_next = choose(s_next) if not done else None
            target = r + (gamma * Q[s_next][a_next] if not done else 0.0)
            Q[s][a] += alpha * (target - Q[s][a])
            if done:
                break
            s, a = s_next, a_next
    return Q
```

8 satır. Q öğrenme ile * tek* fark hedef satır.

> 八行代码── Q-öğrenme ile * tek* fark hedef行──

### Adım 2: Q öğrenme

```python
def q_learning(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    for _ in range(episodes):
        s = env.reset()
        while True:
            a = choose(s, Q, epsilon)
            s_next, r, done = env.step(s, a)
            target = r + (gamma * max(Q[s_next].values()) if not done else 0.0)
            Q[s][a] += alpha * (target - Q[s][a])
            if done:
                break
            s = s_next
    return Q
```

- Evet .`max`Bu bir sembol politika içi ve dışı politika arasındaki fark.

> `max`Bu bir simge, çevrimiçi stratejiler ve dış stratejiler arasındaki farkı ifade eder.

### Adım 3: Öğrenme eğri

100 bölüm başına geri dönüş ortalaması. Q-öğrenme basit belirleyici GridWorld'da daha hızlı bir şekilde birleşti. SARSA, uçurum yürüyüşünde daha muhafazakardır.`code/main.py`Her ikisi de yaklaşık 2000 bölümden sonra en iyi şekilde yapılıyor .`α=0.1, ε=0.1`- Evet .

> Bu, bir dizi farklı yöntemi oluşturur.`code/main.py`4×4 GridWorld'ın üstü, ikisi arasında.`α=0.1, ε=0.1`Yaklaşık 2.000 kez en iyi şekilde.

### Dördüncü adım: DP gerçeği ile karşılaştır

Çalışma değerinin tekrarlanması (Denevi 02) elde etmek için `Q*`- Kontrol et .`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`Sağlıklı bir tablolar TD ajanı `~0.5`4×4 GridWorld'da 10.000 bölümden sonra.

> 运行值代(Düşünme 02) 获得`Q*`❖ Kontrol`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`❖ Sağlıklı bir tablo TD  Akıllı vücut 10.000 kere birleştirildi sonra 4×4 GridWorld `~0.5`İçinde.

## Tuzaklar

- **Initial Q values matter.**Optimistik başlangıç (`Q = 0`Bu nedenle, bu durumun bir sonucu olarak, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir kişinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerinin, bir diğerine, bir diğerine, bir diğerine, bir diğerine, bir diğerine, bir diğerine, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir diğer, bir, bir, bir diğer, bir, bir, bir diğer, bir, bir, bir diğer, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir
  **初始 Q 值很重要。**乐观初始化 负奖励任务中   负奖励任务中    负奖励任务中`Q = 0`* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
- **α schedule.**Sürekli .`α`-Sitasyonel olmayan sorunlar için iyi.`α_n = 1/n`teoride bir uyum sağlar ama pratikte çok yavaş  pin `α`İçeride`[0.05, 0.3]`Öğrenme eğrisini izle.
  **α 调度。**常数 `α`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `α_n = 1/n`Teorik olarak kabul edilir ama pratikte çok yavaş olur.`α`Düzgün`[0.05, 0.3]`Ve öğrenme eğilimi izlemektedir.
- **ε schedule.**Yüksek başlayın (`ε=1.0`), ıkışmaya`ε=0.05`"GLIE" (sonsuz keşifle sınırda açgözlülük) bir yakınlık şartıdır.
  **ε 调度。**# Başlamak için yüksek değeri #`ε=1.0`), düşüşe kadar `ε=0.05` "GLIE" (极限贪心且无限探索)  条件
- **Max bias in Q-learning.**- Evet .`max`Operatör yukarı tarafa eğilimi gösterir.`Q`Hasselt'in Çift Q öğrenimi (DDDQN tarafından Ders 05) bunu iki Q tablosu ile düzeltir.
  **Q-learning 的最大化偏差。** `max`- Evet .`Q`Hay hayati bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli birli bir sesli bir sesli birli bir sesli bir sesli
- **Non-terminating episodes.**TD, terminal olmadan öğrenebilir, ancak ya adımları kapalı tutmanız veya başlatma çubuğunu başlatmanız gerekir. Standart: başlatmayı terminal olmayan olarak değerlendirin, başlatmayı sürdürün.
  **非终止回合。**TD, sonsuz bir durumda öğrenebilir, ancak adım sayısının sınırına veya doğru şekilde işleme sınırının kendiliğinden hareket etmesi gerekir.
- **State hashing.**Eğer durumlar tuples/tenzorlar ise, bir hashable anahtar kullanın (toplo, listesi değil; toplu, çiğ değil yuvarlanmış yüzenler).
  **状态哈希。**Eğer durum buyum/张量 ise, kullanılabilir olan anahtarı kullanın.

## Çerçeveyi kullanın.

2026 TD manzarası:

> 2026 yıl TD 学习的版图:

| Task | Method | Reason |
|------|--------|--------|
| Task / 任务 | Method / 方法 | Reason / 原因 |
| Small tabular environments / 小型表格环境 | Q-learning | Learns optimal policy directly. / 直接学习最优策略。 |
| On-policy safety-critical / 在线策略安全关键 | SARSA / Expected SARSA | Conservative during exploration. / 探索期间保守。 |
| High-dimensional state / 高维状态 | DQN (Phase 9 · 05) | Neural-net Q-function with replay and target net. / 神经网络 Q 函数+回放+目标网络。 |
| Continuous actions / 连续动作 | SAC / TD3 (Phase 9 · 07) | TD update on a Q-network; policy net emits actions. / Q 网络上的 TD 更新；策略网络输出动作。 |
| LLM RL (reward-model-based) / LLM RL（基于奖励模型） | PPO / GRPO (Phase 9 · 08, 12) | Actor-critic with TD-style advantage via GAE. / Actor-Critic + GAE 的 TD 式优势。 |
| Offline RL / 离线 RL | CQL / IQL (Phase 9 · 08) | Q-learning with conservative regularization. / 带保守正则化的 Q-learning。 |

2026 makalelerinde okuduğunuz "RL"lerin yüzde 90'ı, Q-öğrenme veya SARSA'nın bir çeşit geliştirmesidir.

> 2026 yılında okuduğunuz makalede "RL" nin %90'ı Q öğrenme veya SARSA'nın bir çeşit değişikliği olmuştur.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-td-agent.md`- ...

```markdown
---
name: td-agent
description: Pick between Q-learning, SARSA, Expected SARSA for a tabular or small-feature RL task.
version: 1.0.0
phase: 9
lesson: 4
tags: [rl, td-learning, q-learning, sarsa]
---

Given a tabular or small-feature environment, output:

1. Algorithm. Q-learning / SARSA / Expected SARSA / n-step variant. One-sentence reason tied to on-policy vs off-policy and variance.
2. Hyperparameters. α, γ, ε, decay schedule.
3. Initialization. Q_0 value (optimistic vs zero) and justification.
4. Convergence diagnostic. Target learning curve, `|Q - Q*|` check if DP is possible.
5. Deployment caveat. How will exploration behave at inference? Is SARSA's conservatism needed?

Refuse to apply tabular TD to state spaces > 10⁶. Refuse to ship a Q-learning agent without a max-bias caveat. Flag any agent trained with ε held at 1.0 throughout (no exploitation phase).
```

## Egzersizler.

1. **Easy.**4×4 GridWorld'de Q-öğrenme ve SARSA uygulaması. 2000 bölüm için plan öğrenme eğri (100 bölüm başına ortalama dönüş) uygulayın.
   > **练习1：**Bu nedenle, bu programın en önemli yönü, bu programın en önemli yönüdür.
2. **Medium.**Klip yürüyüş ortamı oluşturun (4×12, son satır ödül -100 ile klip ve başlangıç için yeniden ayarlayın). Q-öğrenme ve SARSA son politikalarını karşılaştırın. Her birinin aldığı yolları ekran görüntüsü. Klipten hangisi daha yakın?
   > **练习2：**悬崖行走环境,观察 Q-learning (Q-learning) 贴崖边) vs SARSA (SARSA) 远离崖边) 策略差异──
3. **Hard.**Çift Q öğrenimi uygulayın. Gürültülü ödül GridWorld'da (Gaussian gürültüsü σ=5 adım ödülüne eklenir) Q öğrenimi aşırı derecede değerlendirilmiş olduğunu gösterin `V*(0,0)`İki kez öğrenmek, iki kez öğrenmek değil.
   > **练习3：**İkiz Q-öğrenme gerçekleştirmek, Q-öğrenme maksimum farkı ortadan kaldırabileceğini kanıtlamak.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| TD error | "The update signal" / TD 误差 | `δ = r + γ V(s') - V(s)`, the bootstrapped residual. |
| TD(0) | "One-step TD" / 单步 TD | Update after every transition using only the next state's estimate. |
| Q-learning | "Off-policy RL 101" / Q 学习 | TD update with `max` over next-state actions; learns `Q*` regardless of behavior policy. |
| SARSA | "On-policy Q-learning" / SARSA | TD update using the actual next action; learns `Q^π` for current ε-greedy π. |
| Expected SARSA | "The low-variance SARSA" / 期望 SARSA | Replace sampled `a'` with its expectation under π. |
| GLIE | "Correct exploration schedule" / 无限探索极限贪心 | Greedy in the Limit with Infinite Exploration; needed for Q-learning convergence. |
| Bootstrapping | "Using current estimate in the target" / 自举 | What distinguishes TD from MC. Source of bias but massive variance reduction. |
| Maximization bias | "Q-learning overestimates" / 最大化偏差 | `max` over noisy estimates is upward-biased; fixed by Double Q-learning. |

## Daha fazla okumak

- [Watkins & Dayan (1992). Q-learning](https://link.springer.com/article/10.1007/BF00992698) orijinal kağıt ve yakınlık kanıtı.
- [Sutton & Barto (2018). Ch. 6 — Temporal-Difference Learning](http://incompleteideas.net/book/RLbook2020.pdf) TD(0), SARSA, Q-öğrenme, Beklenen SARSA.
- [Hasselt (2010). Double Q-learning](https://papers.nips.cc/paper_files/paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html) Maksimumlama tercihleri için düzeltme.
- [Seijen, Hasselt, Whiteson, Wiering (2009). A Theoretical and Empirical Analysis of Expected SARSA](https://ieeexplore.ieee.org/document/4927542) beklenen SARSA motivasyonu.
- [Rummery & Niranjan (1994). On-line Q-learning using connectionist systems](https://www.researchgate.net/publication/2500611_On-Line_Q-Learning_Using_Connectionist_Systems) SARSA'yı (o zaman "değiştirilmiş bağlantılı Q-öğrenme" olarak adlandırılan) ortaya koyan kağıt.
- [Sutton & Barto (2018). Ch. 7 — n-step Bootstrapping](http://incompleteideas.net/book/RLbook2020.pdf) TD(0) ile TD(n'e genelleştirir.
