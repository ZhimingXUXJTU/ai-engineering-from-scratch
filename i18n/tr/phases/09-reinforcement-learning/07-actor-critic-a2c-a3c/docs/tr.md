# Actor-Critic A2C ve A3C

> ReINFORCE gürültülü, öğrenen bir eleştirmen ekle.`V̂(s)`A2C, sinkron olarak çalışır, A3C ise ipler arasında çalışır. Her ikisi de modern derin-RL yönteminin zihinsel modelidir.

> **【中文解读】**REINFORCE 方差太大──加入一个"评论家"(Critic)学习 V̂(s), onu temel yapılandırma avantajlı işlevi olarak kullanın A = G - V̂(s), beklenti değişmez ama 方差 önemli ölçüde azalmıştır──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 04 (TD Learning), Phase 9 · 06 (REINFORCE) | **前置知识:** Phase 9 · 04 (TD 学习), Phase 9 · 06 (REINFORCE)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Vanilla REINFORCE işe yarıyor ama farkı korkunç.`G_t`Bu sesleri 10 katına çarparak çarpıyor.`∇ log π`ve ortalama bir gradient tahmincisi üretir. Bu politikaları daha az DQN güncellemeleri ile taşıyabileceğiniz mesafeyi taşımak için binlerce bölüm alıyor.

> İlk güçlenme, ama kötü bir yol.`G_t`Bu arada 10 kat daha fazla ses çıkıyor.`∇ log π`Yeniden ortalama olarak, oluşan dereceli tahminci, daha az DQN'yi kullanarak aynı etkiyi elde etmek için binlerce kez hareket etmek gerekir.

Değişiklik çiğ geri dönüş kullanılarak ortaya çıkar.`b(s_t)` öğrenilen bir değer de dahil olmak üzere herhangi bir durum fonksiyonu  beklenti değişmez ve varyansa düşer. En iyi ele alınan temel çizgi `V̂(s_t)`Şimdi miktar çarpı.`∇ log π`* avantaj*:

`A(s, a) = G - V̂(s)`

> 方差来自使用原始回报──如果减去基线 `b(s_t)` herhangi bir durum fonksiyonu, öğrenme değerini  beklenti değişmez ama fark azalır.`V̂(s_t)`Şimdi de.`∇ log π`量就是优势

Bir eylem ortalama üzerinde bir getiri üretirse iyi olur; aşağıda ise kötüdür. Öğrenmiş bir eleştirmen ile REINFORCE *actor-critic*. eleştirmen, aktörü düşük değişkenlik öğretmeni yapar. Bu 2015'ten sonra tüm derin politika yöntemleri (A2C, A3C, PPO, SAC, IMPALA).

> 动作好如果产生高于平均的回报;差如果低于──带学习批评的 REINFORCE 就是 *Actor-Critic*──Critic 给 Actor一个低方差的教师──这是2015年后每深度策略方法(A2C、A3C、PPO、SAC、IMPALA)──

## Konsepten bir şey.

![Actor-critic: policy net plus value net, TD residual as advantage](../assets/actor-critic.svg)

**Two networks, one shared loss:**

> **两个网络，一个共享损失：**

- **Actor** `π_θ(a | s)`Politikası. Yürümeye örneklenmiş. Politikası derecesi ile eğitilmiş.
  **Actor** `π_θ(a | s)`Taktiği:                                                                                                                                                                                                                                                             
- **Critic** `V_φ(s)`Bu nedenle, bu durumun en az bir şekilde azaltılması için eğitilmiştir.`(V_φ(s) - target)²`- Evet .
  **Critic** `V_φ(s)`: Durumdan çıkış beklentilerini tahmin etmek.`(V_φ(s) - target)²`- Evet.

**The advantage.**İki standart form:

> **优势函数。**两种标准形式:

- *MC avantajı:* `A_t = G_t - V_φ(s_t)`Tarafsız, daha yüksek bir değişim.
  *MC 优势:* 无偏,方差较高──
- *TD avantajı:* `A_t = r_{t+1} + γ V_φ(s_{t+1}) - V_φ(s_t)`. Tarafsız (kullanımlar `V_φ`*TD geri kalanı* olarak da adlandırılır.`δ_t`- Evet .
  *TD 优势:* 有偏差(使用 `V_φ`),方差远低──也称为 *TD残差* `δ_t`- Evet.

**n-step advantage.**İkisi arasında bir arada dur:

`A_t^{(n)} = r_{t+1} + γ r_{t+2} + … + γ^{n-1} r_{t+n} + γ^n V_φ(s_{t+n}) - V_φ(s_t)`

`n = 1`saf TD.`n = ∞`MC'dir. Çoğu uygulamada kullanılır `n = 5`Atari için,`n = 2048`MuJoCo'da PPO için.

> **n 步优势。**Arasındaki değerler arasında bir fark var.`n = 1`Tam bir TD.`n = ∞`Evet, çoğu Atari kullanıyor.`n = 5`- MuJoCo'nun üstündeki PPO kullanıyor.`n = 2048`- Evet.

**Generalized Advantage Estimation (GAE).**Schulman et al. (2016) tüm n-adım avantajları üzerinde eksponensel olarak ağırlanan bir ortalama önerdi:

`A_t^{GAE} = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}`

- Evet .`λ ∈ [0, 1]`- Evet .`λ = 0`TD ( düşük değişkenlik, yüksek önyargı). `λ = 1`MC (yüksek farklılık, tarafsızlık)`λ = 0.95`2026'da, öntanımlı  ayarı, öntanımlı/varians diyalığı istediğiniz yere kadar.

> **【中文解读】**GAE( geniş anlamlı avantaj tahminleri) Actor-Critic'in anahtar gelişmesidir: indeksleme ile 步骤优势 arasındaki en iyi dengeni bulmak için 偏差 ve 方差 arasında 偏差 ve 方差 arasında 偏差 ve 偏差 arasında 偏差 ve 偏差 arasında 偏差 ve 偏差 arasında 偏差 ve 偏差 arasında 偏差 ve 偏差 arasında 偏差 ve 偏差 arasında 偏差 ve 偏差 arasında 偏差 ve 偏差 arasında 偏差 ve 偏差 arasında 偏差 ve 偏差 arasında 偏差 ve 偏差 arasında 偏差 arasında 偏差 ve 偏差 arasında 偏差 ve 偏差 arasında 偏差 arasında 偏差 ve 偏差 arasında 偏差 vardır.

> **【拓展：GAE 在 RLHF 中的应用】**ChatGPT'nin PPO eğitimi GAE  hesap avantaj fonksiyonu kullanılarak. LLM'de "stat" oluşturulan token 序列idir, "动作" oluşturulan token 序列idir, "öğüt" ödül modelinden gelir.

**A2C: synchronous advantage actor-critic.**Toplayın .`T`Dönüşümler `N`Paralel ortamlar. Her adım için avantajlar hesaplayın. Birleştirilmiş seri için aktör ve eleştirmeni güncelleyin. Tekrarla.

> **A2C：同步优势 Actor-Critic。**- Evet .`N`个并行环境中收集                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `T`步──计算每步优势──在合并批次上更新 Actor 和 Critic──重复──A3C'nin Daha basit、 Daha genişletilenebilir kardeş──

**A3C: asynchronous advantage actor-critic.**Mnih et al. (2016). Spawn `N`İşçi ipleri, her biri bir çevre çalıştırır. Her işçi kendi dağıtımında yerel olarak gradientleri hesaplar, sonra eşzamanlı olarak paylaşılan bir parametre sunucusuna uyguluyor. Hiçbir tekrarlama tamponu gerekmez  işçiler farklı yörüngeler çalıştırarak dekorrele. A3C ölçekte CPU'larda eğitim alabileceğini kanıtladı. 2026'da, GPU tabanlı A2C (batched parallel envs) baskın çünkü GPU'lar büyük partiler istiyor.

> **A3C：异步优势 Actor-Critic。**Mnih 等人 (2016) 启动`N`个工作线程,每个运行一个环境――每个工作线程在本地计算梯度,然后不同步应用到共享参数服务器――不需要回放缓冲区工作线程通过运行不同轨迹来相关――2026 yılında, GPU tabanlı A2C 占主导地位,因为 GPU 需要大量――

**The combined loss.**

`L(θ, φ) = -E[ A_t · log π_θ(a_t | s_t) ]  +  c_v · E[(V_φ(s_t) - G_t)²]  -  c_e · E[H(π_θ(·|s_t))]`

Üç şart: politika derecesi kaybı, değer gerileme, entropi bonusu. `c_v ~ 0.5`- Evet .`c_e ~ 0.01`Kanonik başlangıç noktalarıdır.

> **组合损失。**Üç: strateji derecesi kaybı, değer geri dönüşü, ödüller.`c_v ~ 0.5`- Evet.`c_e ~ 0.01`Tipik başlangıç değeri.

> **【中文解读】**Actor-Critic's Compound Loss = Strateji 梯度損失 + 值函数归归 + 正则化── These three distinct对应: İyi hareket olasılığını daha fazla artırın, eleştirmeni daha doğru hale getirin, stratejiyi çok erken kısaltmayı önleyin.

> **【拓展：GAE→PPO→RLHF】**GAE (广义优势估算) PPO'nun temel bileşeni, PPO ise ChatGPT RLHF 训练的标准算法──λ=0.95 2026 yılının standart değeri,偏差与方差 arasındaki dengeyi elde etmek için. GAE'yi anlamak, büyük modeller için hazırlıkta en önemli üstünlük tahmin yöntemini anlamak demektir.

## Yapın.
```figure
actor-critic
```

## Yapın

### Adım 1: eleştirmen

Düzsel eleştirmen`V_φ(s) = w · features(s)`MSE ile güncelleştirilmiştir:

```python
def critic_update(w, x, target, lr):
    v_hat = dot(w, x)
    err = target - v_hat
    for j in range(len(w)):
        w[j] += lr * err * x[j]
    return v_hat
```

Bir tablo ortamında eleştirmen birkaç yüz bölümde bir araya gelir. Atari'de, çizgisi eleştirmeni CNN'in paylaşılan bir çekirdek + değer başlığı ile değiştirin.

> 线性批評 `V_φ(s) = w · features(s)`Ül MSE 更新──在表格环境中几百回合就收──在 Atari 上, CNN 主干 + 值头──

### Adım 2: N-adım avantajı

Uzunluktan dolayı .`T`Ve bir de bir final.`V(s_T)`- ...

```python
def compute_advantages(rewards, values, gamma=0.99, lam=0.95, last_value=0.0):
    advantages = [0.0] * len(rewards)
    gae = 0.0
    for t in reversed(range(len(rewards))):
        next_v = values[t + 1] if t + 1 < len(values) else last_value
        delta = rewards[t] + gamma * next_v - values[t]
        gae = delta + gamma * lam * gae
        advantages[t] = gae
    returns = [a + v for a, v in zip(advantages, values)]
    return advantages, returns
```

`returns`eleştirmen hedef.`advantages`- Çokluyor.`∇ log π`- Evet .

> `returns`                                                                                                                                                                                                                                                              `advantages`Evet.`∇ log π`- Ne kadar?

### Adım 3: birleşik güncelleme

```python
for step_i, (x, a, _r, probs) in enumerate(traj):
    adv = advantages[step_i]
    target_v = returns[step_i]

    # critic
    critic_update(w, x, target_v, lr_v)

    # actor
    for i in range(N_ACTIONS):
        grad_logpi = (1.0 if i == a else 0.0) - probs[i]
        for j in range(N_FEAT):
            theta[i][j] += lr_a * adv * grad_logpi * x[j]
```

Politikada, her güncelleme için bir çıkış, aktör ve eleştirmen için ayrı öğrenme oranları.

> Online strateji, her gün yeni bir rol,Actor 和 Critic 使用不同学习率──

### Adım 4: paralellik (A3C vs. A2C)

- **A3C:**Çekil `N`Her biri kendi env ve kendi ileri geçişini yürütür. Periodik olarak gradient güncelleştirmeleri paylaşılmış bir usta.
- **A2C:**Çıkış`N`Tek bir süreçte örnekler oluşturmak, gözlemleri bir `[N, obs_dim]`Batch, batch forward pass, batch backward pass daha yüksek GPU kullanımı, belirleyici, akıl yürütmek daha kolay.

Oyuncak kodumuz netlik için tek iplik; A2C'ye yeniden yazmak üç satır numpy.

> Oyuncak kodumuz netliğe ulaşmak için tek bir satırdır.

## Tuzaklar

- **Critic bias before actor gradient.**Eğer eleştirmen rastgele ise, temel çizgisi bilgilendirici değil ve saf gürültü üzerinde eğitim veriyorsunuz.
  **Actor 梯度之前的 Critic 偏差。**Eğer eleştirmen kasıtlı ise, temel çizgiden bilgi miktarı yoksa, saf gürültü üzerinde eğitim alırsın.
- **Advantage normalization.**Parçaya sıfır ortalama/birlik std'ye avantajları normalleştirir.
  **优势归一化。**Her bir grup avantajı sıfır ortalama değer/birlik standart farkına dönüştürür.
- **Shared trunk.**Görüntü girişlerinde oyuncu ve eleştirmen için ortak bir özellik çıkarıcı kullanın. Ayrı başlar. Paylaşılan özellikler her iki kayıpta da serbest sürüş.
  **共享主干。**图像输入时使用共享特征提取器──分开的头──共享特征同时从两个损失中获益──
- **On-policy contract.**A2C, verileri tam bir güncelleme için tekrar kullanır. Daha fazla ve gradiyenti tarafsızdır (PPO'nun eklediği önemlilik örneği düzeltmesidir).
  **在线策略约束。**A2C 恰好用数据做一次更新.
- **Entropy collapse.**- Hayır .`c_e > 0`Bu politika birkaç yüz güncelleme ile neredeyse belirlenmiş hale gelir ve araştırmayı bırakır.
  **熵坍缩。**Hiç .`c_e > 0`, strateji birkaç yüz güncelleştirilmesinden sonra yakın belirsizlik için araştırmayı durdurdu.
- **Reward scale.**Avantaj büyüklükleri ödül ölçeğine bağlıdır. Görevler arasında tutarlı gradient büyüklükleri için ödülleri (örneğin, çalıştırma-std bölüşmesi) normallaştırın.
  **奖励尺度。**优势量级取决于奖励量级―― 归纳奖励以获得跨任务一致的梯度量级――

## Çerçeveyi kullanın.

A2C/A3C 2026'da nadiren son seçimdir ama sonraları en iyi yapılan mimarlıklardır:

> A2C/A3C 2026 yılında son seçimlerde çok azdır, ancak daha sonra tüm yöntemlerin daha iyi bir yapılandırmasıdır:

| Method | Relation to A2C |
|--------|----------------|
| Method / 方法 | Relation to A2C / 与 A2C 的关系 |
| PPO | A2C + clipped importance ratio for multi-epoch updates / A2C + 裁剪重要性比率用于多轮更新 |
| IMPALA | A3C + V-trace off-policy correction / A3C + V-trace 离策略修正 |
| SAC (Phase 9 · 07) | Off-policy A2C with a soft-value critic (next lesson) / 离策略 A2C + 软值 Critic |
| GRPO (Phase 9 · 12) | A2C without the critic — group-relative advantage / 无 Critic 的 A2C——组相对优势 |
| DPO | A2C collapsed into a preference-ranking loss, no sampling / 折叠为偏好排名损失的 A2C |
| AlphaStar / OpenAI Five | A2C with league training + imitation pre-training / A2C + 联盟训练 + 模仿预训练 |

2026'da bir makalede "kalah" görürseniz, oyuncu eleştirmeni düşünün.

> 2026'da "Güzen" ifadelerini görürsen, Aktris-Kritik'i düşün.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-actor-critic-trainer.md`- ...

```markdown
---
name: actor-critic-trainer
description: Produce an A2C / A3C / GAE configuration for a given environment, with advantage estimation and loss weights specified.
version: 1.0.0
phase: 9
lesson: 7
tags: [rl, actor-critic, gae]
---

Given an environment and compute budget, output:

1. Parallelism. A2C (GPU batched) vs A3C (CPU async) and the number of workers.
2. Rollout length T. Steps per env per update.
3. Advantage estimator. n-step or GAE(λ); specify λ.
4. Loss weights. `c_v` (value), `c_e` (entropy), gradient clip.
5. Learning rates. Actor and critic (separate if using).

Refuse single-worker A2C on environments with horizon > 1000 (too on-policy, too slow). Refuse to ship without advantage normalization. Flag any run with `c_e = 0` and observed entropy < 0.1 as entropy-collapsed.
```

## Egzersizler.

1. **Easy.**MC avantajı olan aktör-kritik tren (`G_t - V(s_t)`Örnek verimliliğini ders 06'tan REINFORCE-with-running-mean baseline ile karşılaştırın.
2. **Medium.**TD-salı avantajına geçiş (`r + γ V(s') - V(s)`En iyisi, avantaj partilerinin farkını ölçmek.
3. **Hard.**GAE'yi uygula.`λ ∈ {0, 0.5, 0.9, 0.95, 1.0}`Bu görevin önyargısı/varians tatlı noktası nerede?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Actor | "The policy net" / 演员（策略网络） | `π_θ(a\|s)`, updated by policy gradient. |
| Critic | "The value net" / 评论家（值网络） | `V_φ(s)`, updated by MSE regression to returns / TD targets. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = Q(s, a) - V(s)` or its estimators. Multiplier for `∇ log π`. |
| TD residual | "δ" / TD 残差 | `δ_t = r + γ V(s') - V(s)`; one-step advantage estimate. |
| GAE | "The interpolation knob" / 广义优势估计 | Exponentially weighted sum of n-step advantages, parameterized by `λ`. |
| A2C | "Synchronous actor-critic" / 同步演员-评论家 | Batched across envs; one gradient step per rollout. |
| A3C | "Async actor-critic" / 异步演员-评论家 | Worker threads push gradients to a shared param server. Original paper; less common in 2026. |
| Bootstrap | "Use V at the horizon" / 自举截断 | Truncate the rollout, add `γ^n V(s_{t+n})` to close the sum. |

## Daha fazla okumak

- [Mnih et al. (2016). Asynchronous Methods for Deep Reinforcement Learning](https://arxiv.org/abs/1602.01783) A3C, orijinal asynk aktör-kritik kağıdı.
- [Schulman et al. (2016). High-Dimensional Continuous Control Using Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438) GAE.
- [Sutton & Barto (2018). Ch. 13 — Actor-Critic Methods](http://incompleteideas.net/book/RLbook2020.pdf) Temeller; eleştirmen bir sinir ağı olduğunda fonksiyon yaklaşımıyla ilgili 9. bölüm ile eşleştirin.
- [Espeholt et al. (2018). IMPALA](https://arxiv.org/abs/1802.01561) V- izleme politika dışı düzeltme ile ölçeklenebilir dağıtılı aktör eleştirmen.
- [OpenAI Baselines / Stable-Baselines3](https://stable-baselines3.readthedocs.io/) üretim A2C/PPO uygulamaları okumaya değer.
- [Konda & Tsitsiklis (2000). Actor-Critic Algorithms](https://papers.nips.cc/paper/1786-actor-critic-algorithms) iki katlı aktör-kritik parçalanma için temel bir yakınlaşma sonucu.
