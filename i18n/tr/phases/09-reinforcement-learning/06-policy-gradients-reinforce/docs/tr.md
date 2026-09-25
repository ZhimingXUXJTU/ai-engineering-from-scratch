# Politika derecesi sıfırdan güçlendirme yöntemi sıfırdan güçlendirme yöntemi

> Bu nedenle, PPO, GRPO ve her LLM RL döngüsü var.

> **【中文解读】**Bu nedenle, bir değer değerinin yeniden değerlendirilmesi için bir değer değer değerinin yeniden değerlendirilmesi için bir değer değer değerinin yeniden değerlendirilmesi için bir değer değer değerinin yeniden değerlendirilmesi için bir değer değer değerinin yeniden değerlendirilmesi için bir değer değer değer değerinin yeniden değerlendirilmesi için bir değer değer değer değerinin yeniden değerlendirilmesi için bir değer değer değer değerinin yeniden değerlendirilmesi için bir değer değer değerinin yeniden değerlendirilmesi için bir değer değer değerlendirilmesi için bir değer değer değer değerinin yeniden değerlendirilmesi için bir değer değer değerlendirilmesi için bir değer değer değerlendirme için bir değer değer değerlendirme için bir değer değer değerlendirme için bir değer değer değerlendirme için bir değer değer değerlendirme için bir değer değer değerlendirme gereklidir.`∇J(θ) = E[G · ∇log π_θ(a|s)]`Bu PPO, GRPO ve tüm büyük model RL eğitim döngüsünün varlığının nedeni.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 03 (Monte Carlo), Phase 9 · 04 (TD Learning) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 03 (蒙特卡洛), Phase 9 · 04 (TD 学习)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Q-learning ve DQN *value* fonksiyonunu parametre eder.`argmax Q`Bu, ayrı eylemler ve ayrı durumlar için iyi.`argmax`10 boyutlu bir topu üzerinde?) veya stokast politikası istediğinizde (`argmax`Bu, yapısal olarak belirleyici bir yöntemdir.

> Q-öğrenme 和 DQN 参数化*值* işlevi`argmax Q`选择动作── This is a problem with the separated movement and the separated state. Bu bir sorun değil.`argmax`?) veya istekli bir strateji`argmax`Doğal olarak, bu kesin.

Politika gradiyentiler yerine *politik* parametrelidir. `π_θ(a | s)`Bu, bir işlem üzerinde bir dağılım üreten bir sinir ağıdır.`θ`- Yukarı çık.`argmax`Bellman'ın geri dönüşü yok, sadece gradient yükselme.`J(θ) = E_{π_θ}[G]`- Evet .

> 策略梯度改为参数化*策略*──`π_θ(a | s)`Bu, bir neörolojik ağın bir çıkış hareket dağılımıdır.`θ`梯度──往上走──不需要 `argmax`Bellman'ın ihtiyacı yok.`J(θ) = E_{π_θ}[G]`Yukarıdaki dereceleri yükseltmek.

REINFORCE teoremi (Williams 1992) size bu gradiyentin hesaplanabileceğini söylüyor:`∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`Bir bölüm çalıştır, geri dönüşü hesapla, çarpı ile çarpı.`∇ log π_θ(a | s)`Her adımda ortalama, derecelendirme, tamam.

> Bu düzeyin hesaplanabilir olduğunu söyleyin.`∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`◊运行一个回合――计算回报――每步乘以 `∇ log π_θ(a | s)`△取平均──梯度上升──完成──

2026'da LLM-RL algoritması olan her bir algoritma REINFORCE'nin bir gelişmesidir. Parmaklarınızla anlamak bu aşamanın geri kalanında ve 10 · 07 aşamasında (RLHF uygulaması) ve 10 · 08 aşamasında (DPO) ön koşuldur.

> 2026 yılında her LLM-RL 算法PPO、DPO、GRPO                                                                                                                                                                                                                                                     

> **【中文解读】**策略梯度的核心思想:直接优化策略参数 θ,让高回报的动作概率增加高回报的动作概率减少小──`∇log π`İşte "kurayetin yön yönü" G'yi çarpıp "iyi yönde yürü" demek.

> **【拓展：PPO→ChatGPT对齐】**ChatGPT'nin RLHF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     `loss = -advantage * log_prob`Bu bir kod satırı, 2026 yılının neredeyse tüm büyük model RL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

## Konsepten bir şey.

![Policy gradient: softmax policy, log-π gradient, return-weighted update](../assets/policy-gradient.svg)

**The policy gradient theorem.**Herhangi bir politika için .`π_θ`parametrelidir `θ`- ...

`∇J(θ) = E_{τ ~ π_θ}[ Σ_{t=0}^{T} G_t · ∇_θ log π_θ(a_t | s_t) ]`

nerede`G_t = Σ_{k=t}^{T} γ^{k-t} r_{k+1}`step'ten düşen düşüştür.`t`Beklentiler tam yollardan geçti .`τ``π_θ`- Evet .

> **策略梯度定理。**Herhangi bir şeye.`θ`参数化 stratejisi `π_θ`, geri dönüş beklentisi derecesi: geri dönüşün indirimleri ve sayısal strateji derecesinin beklentisi ile çarpılandırılmasıdır.`π_θ`采样完整轨迹上取──

**The proof is short.**Farklılaştır `J(θ) = Σ_τ P(τ; θ) G(τ)`- Kullanım.`∇P(τ; θ) = P(τ; θ) ∇ log P(τ; θ)`(log-derivat hilesi).`log P(τ; θ) = Σ log π_θ(a_t | s_t) + environment terms that do not depend on θ`İki cebir çizgisi teoremi verir.

> **证明很短。**Hızlı bir beklentide`J(θ)`求导──使用对数导数技巧──将 `log P(τ; θ)`Bu iki yöntemin birbiriyle çözülmesi için, birbiriyle ilgili bir diğer yöntem de belirlenmiştir.

**Variance reduction tricks.**Vanilla REINFORCE'nin cinayetçi bir değişikliği var.`∇ log π`Şiddetli bir sesli, ürünleri çok gürültülü.

> **方差降低技巧。**Çatışmalar çok büyük.`∇ log π`Bu sesler daha fazla.

1. **Baseline subtraction.**Değiştir `G_t`- Evet .`G_t - b(s_t)`herhangi bir başlangıç için `b(s_t)`Bu da `a_t`Tarafsızlık çünkü`E[b(s_t) · ∇ log π(a_t | s_t)] = 0`Tipik seçim:`b(s_t) = V̂(s_t)`Bir eleştirmen tarafından öğrenilen → aktör- eleştirmen (Denevi 07).
   **基线减法。**Kullan .`G_t - b(s_t)`替换 `G_t`❖ tipik seçim:`b(s_t) = V̂(s_t)`By eleştirmen 学习 → Aktör-Kritik(Düşünme 07)。
2. **Reward-to-go.**Değiştir `Σ_t G_t · ∇ log π_θ(a_t | s_t)`- Evet .`Σ_t G_t^{from t} · ∇ log π_θ(a_t | s_t)`. Sadece gelecekte elde edilen kazançlar belirli bir eylem için önemli  Geçmişteki ödüller sıfır ortalama gürültüye katkıda bulunur.
   **未来回报。**Sadece gelecekte verilen hareketlere değerli bir karşılık verilir.

Birleştirildiğinde:

`∇J ≈ (1/N) Σ_{i=1}^{N} Σ_{t=0}^{T_i} [ G_t^{(i)} - V̂(s_t^{(i)}) ] · ∇_θ log π_θ(a_t^{(i)} | s_t^{(i)})`

Bu, A2C (Desin 07) ve PPO (Desin 08) 'nin doğrudan ataları olan bir temel  ile REINFORCE'dir.

**Softmax policy parameterization.**Ayrı işlemler için standart seçim:

`π_θ(a | s) = exp(f_θ(s, a)) / Σ_{a'} exp(f_θ(s, a'))`

nerede`f_θ`Bu, her hareket için bir puan çıkaran herhangi bir sinir ağıdır.

`∇_θ log π_θ(a | s) = ∇_θ f_θ(s, a) - Σ_{a'} π_θ(a' | s) ∇_θ f_θ(s, a')`

Yani, alınan eylemlerin puanı, polisin altında beklenen değeri eksik.

> **Softmax 策略参数化。**Ayrı hareketler için, gradient form简洁:

**Gaussian policy for continuous actions.** `π_θ(a | s) = N(μ_θ(s), σ_θ(s))`- Evet .`∇ log N(a; μ, σ)`Bu, 9. · 07 aşamasının SAC ihtiyaçları.

> **连续动作的高斯策略。** `∇ log N(a; μ, σ)`Bu, SAC'nin 9. · 07 aşamasının tüm ihtiyaçlarıdır.

## Yapın.
```figure
policy-gradient-landscape
```

## Yapın

### Adım 1: softmax politika ağı

```python
def policy_logits(theta, state_features):
    return [dot(theta[a], state_features) for a in range(N_ACTIONS)]

def softmax(logits):
    m = max(logits)
    exps = [exp(l - m) for l in logits]
    Z = sum(exps)
    return [e / Z for e in exps]
```

Tablolar bir çerçeve için doğrusal bir politika (harekete bir ağırlık vektörü) kullanın. Atari için, CNN'e geçin ve softmax başını tutun.

> Çevreyi kullanmak için bir tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane

### Adım 2: Örnek alma ve kayıt olasılıkları

```python
def sample_action(probs, rng):
    x = rng.random()
    cum = 0
    for a, p in enumerate(probs):
        cum += p
        if x <= cum:
            return a
    return len(probs) - 1

def log_prob(probs, a):
    return log(probs[a] + 1e-12)
```

### Adım 3: Kayıtları yakalayarak devreye girme

```python
def rollout(theta, env, rng, gamma):
    trajectory = []
    s = env.reset()
    while not done:
        logits = policy_logits(theta, s)
        probs = softmax(logits)
        a = sample_action(probs, rng)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r, probs))
        s = s_next
    return trajectory
```

### 4. Adım: REINFORCE güncelleme

```python
def reinforce_step(theta, trajectory, gamma, lr, baseline=0.0):
    returns = compute_returns(trajectory, gamma)
    for (s, a, _, probs), G in zip(trajectory, returns):
        advantage = G - baseline
        grad_log_pi_a = [-p for p in probs]
        grad_log_pi_a[a] += 1.0
        for i in range(N_ACTIONS):
            for j in range(len(s)):
                theta[i][j] += lr * advantage * grad_log_pi_a[i] * s[j]
```

- Yolu `∇ log π(a|s) = e_a - π(·|s)`(birincisi `a`- olasılık) softmax politik gradientlerin kalbidir.

> 梯度 `∇ log π(a|s) = e_a - π(·|s)`(`a`Bu, birer sıcak                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

### Adım 5: Temel çizgiler

Bir ortalama `G`Son bölümler üzerinde 4×4 GridWorld çalıştırmak için yeterli varyansa azaltılması; bir araya gelmek için ~500 bölüm gerekir.`V̂(s)`Ve sen aktör eleştirmenini alıyorsun.

> Son görüşmeler`G`4×4 GridWorld  çalışma için yeterli; yaklaşık 500 回合收──将基线升级为学习的 `V̂(s)`- Aktor-Kritik Alıyorum.

## Tuzaklar

- **Exploding gradients.**Geri dönüşler büyük olabilir.`G`- ...`~N(0, 1)``∇ log π`- Evet .
  **梯度爆炸。**Bir haber büyük olabilir.`∇ log π`Önceden sona erecek .`G`归一化到 `~N(0, 1)`- Evet.
- **Entropy collapse.**Politikası çok erken bir kararlılık eylemine dönüşür, keşif yapmayı bırakır, sıkışır.`β · H(π(·|s))`Amaca ulaşmak için.
  **熵坍缩。**策略过早收到近确定性动作,停止探索,陷入困境──修复:向目标添加奖励 `β · H(π(·|s))`- Evet.
- **High variance.**Vanilla REINFORCE binlerce bölüm gerektirir. Kritik bir temel (Denevi 07) veya TRPO/PPO'nun güven bölgesini (Denevi 08) standart düzeltme.
  **高方差。**Önemli bir temel oluşturmak için, bu konuda çok fazla bilgi almak gerekir.
- **Sample inefficiency.**Politika üzerindeki değişiklikler, bir güncelleme sonrasında her geçişi atmak anlamına gelir.Polis dışındaki düzeltmeler, önemi örneği ile veriyi geri getirir, değişikliğin bedeliyle (PPO'nun oranı, bir kısaltılmış IS ağırlığıdır).
  **样本效率低。**Online strateji, her güncelleme sonrası tüm taşınmayı bırakmak anlamına gelir.
- **Non-stationary gradients.**100 bölüm önceki aynı gradient eski kullanıyor .`π`Bu nedenle politika yöntemleri her birkaç çıkışta güncelleştirilir.
  **非平稳梯度。**100 回合前的梯度使用旧的 `π`                                                                                                                                                                                                                                                              
- **Credit assignment.**Ödüller olmadan, geçmiş ödüller gürültüye katkıda bulunur.
  **信用分配。**没有未来回报,过去的奖励贡献噪声──始终使用未来回报──

## Çerçeveyi kullanın.

2026 yılında REINFORCE nadiren doğrudan çalıştırılır ancak gradient formülü her yerde bulunur:

> 2026 yıl, REINFORCE  çok az doğrudan çalıştırılır, ancak 梯度公式 bulunmuyor:

| Use case | Derived method |
|----------|---------------|
| Use case / 用例 | Derived method / 派生方法 |
| Continuous control / 连续控制 | PPO / SAC with Gaussian policy / 高斯策略的 PPO/SAC |
| LLM RLHF / LLM RLHF | PPO with KL penalty, running on token-level policy / 带 KL 惩罚的 PPO，token 级策略 |
| LLM reasoning (DeepSeek) / LLM 推理 | GRPO — REINFORCE with group-relative baseline, no critic / 组相对基线的 REINFORCE，无 critic |
| Multi-agent / 多智能体 | Centralized-critic REINFORCE (MADDPG, COMA) / 集中 critic 的 REINFORCE |
| Discrete action robotics / 离散动作机器人 | A2C, A3C, PPO |
| Preference-only settings / 仅偏好设置 | DPO — REINFORCE rewritten as a preference-likelihood loss, no sampling / 重写为偏好似然损失的 REINFORCE |

Okuduğunda .`loss = -advantage * log_prob`Bu bir çizgi üzerine tüm makaleler (DPO, GRPO, RLOO) varyansa azaltma hileleridir.

> 2026 yılı için eğitim kitabında okuduğunuz zaman.`loss = -advantage * log_prob`Bu yüzden, bu kod üzerinde farklılık düşürme teknikleri vardır.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-policy-gradient-trainer.md`- ...

```markdown
---
name: policy-gradient-trainer
description: Produce a REINFORCE / actor-critic / PPO training config for a given task and diagnose variance issues.
version: 1.0.0
phase: 9
lesson: 6
tags: [rl, policy-gradient, reinforce]
---

Given an environment (discrete / continuous actions, horizon, reward stats), output:

1. Policy head. Softmax (discrete) or Gaussian (continuous) with parameter counts.
2. Baseline. None (vanilla), running mean, learned `V̂(s)`, or A2C critic.
3. Variance controls. Reward-to-go on by default, return normalization, gradient clip value.
4. Entropy bonus. Coefficient β and decay schedule.
5. Batch size. Episodes per update; on-policy data freshness contract.

Refuse REINFORCE-no-baseline on horizons > 500 steps. Refuse continuous-action control with a softmax head. Flag any run with `β = 0` and observed policy entropy < 0.1 as entropy-collapsed.
```

## Egzersizler.

1. **Easy.**4×4 GridWorld'de lineer softmax politikası ile REINFORCE uygulamak. Temel çizgi olmadan 1.000 bölüm için eğit. Öğrenme eğriyi çiz; varyans ölç (sd of returns).
2. **Medium.**Baseline'i bir daha çalıştırın. Yeniden çalıştırın. Örnek verimliliğini ve varyansiyonunu vanilya çalıştırması ile karşılaştırın. Baseline, dönüşüm adımlarını ne kadar azaltır?
3. **Hard.**Bir entropi bonusu ekleyin `β · H(π)`- Arama .`β ∈ {0, 0.01, 0.1, 1.0}`Bu işin en iyi noktası nerede?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy gradient | "Train the policy directly" / 策略梯度 | `∇J(θ) = E[G · ∇ log π_θ(a\|s)]`; derived from the log-derivative trick. |
| REINFORCE | "The original PG algorithm" / REINFORCE算法 | Williams (1992); Monte Carlo returns multiplied by log-policy gradient. |
| Log-derivative trick | "Score function estimator" / 对数导数技巧 | `∇P(τ;θ) = P(τ;θ) · ∇ log P(τ;θ)`; makes gradients of expectations tractable. |
| Baseline | "Variance reduction" / 基线 | Any `b(s)` subtracted from `G`; unbiased because `E[b · ∇ log π] = 0`. |
| Reward-to-go | "Only future returns count" / 未来回报 | `G_t^{from t}` instead of the full `G_0`; correct and lower-variance. |
| Entropy bonus | "Encourage exploration" / 熵正则化 | `+β · H(π(·\|s))` term keeps the policy from collapsing. |
| On-policy | "Train on what you just saw" / 在线策略 | Gradient expectation is w.r.t. the current policy — cannot reuse old data directly. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = G(s, a) - V(s)`; the signed quantity REINFORCE-with-baseline multiplies. |

## Daha fazla okumak

- [Williams (1992). Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning](https://link.springer.com/article/10.1007/BF00992696) orijinal REINFORCE kağıdı.
- [Sutton et al. (2000). Policy Gradient Methods for Reinforcement Learning with Function Approximation](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html) fonksiyon yaklaşımı ile modern politika-gradyen teoremi.
- [Sutton & Barto (2018). Ch. 13 — Policy Gradient Methods](http://incompleteideas.net/book/RLbook2020.pdf) Ders kitabı sunum.
- [OpenAI Spinning Up — VPG / REINFORCE](https://spinningup.openai.com/en/latest/algorithms/vpg.html) PyTorch kodu ile açık bir pedagojik açıklama.
- [Peters & Schaal (2008). Reinforcement Learning of Motor Skills with Policy Gradients](https://homes.cs.washington.edu/~todorov/courses/amath579/reading/PolicyGradient.pdf) Değişiklik azaltma ve REINFORCE'yi güven bölgesine (TRPO, PPO) bağlayan doğal-gradyen görüşü.
