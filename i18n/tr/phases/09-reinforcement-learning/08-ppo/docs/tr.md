# Yakınlık Politikası Optimize (PPO)

> A2C, her bir yüklenmenin bir güncelleştirmeden sonra atılmasını sağlar. PPO politika gradiyentiyi kesilmiş önem oranında sarar, böylece politika patlamadan aynı veriler üzerinde 10+ dönem yapabilirsiniz. Schulman et al. (2017).

> **【中文解读】**PPO, aynı veriyi 10+ kez güncelleyebilmesi için kesme önem oranını kullanarak strateji derecesi paketini paketledi.

> **【拓展：PPO 与 ChatGPT】**PPO, ChatGPT RLHF ıktırmanın temel algoritmasıdır. InstructGPT(2022) PPO'yu GPT-3'ye karşı insan tercihlerini gerçekleştirmek için kullanır.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic) | **前置知识:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

A2C (Desin 07) politikada: gradient `E_{π_θ}[A · ∇ log π_θ]`*kurrent*'den örnek alınan verileri gerektirir.`π_θ`Bir güncellemesi yapın ve`π_θ`Bu değişiklikler, kullandığınız veriler artık politika dışı.

> A2C(Düşünme 07)`E_{π_θ}[A · ∇ log π_θ]`要求从*当前* `π_θ`- Evet. - Evet.`π_θ`改变; you used data has become a strategy. ⇒ Uygulama seviyesi has biases.

Atari'de 8 envs × 128 adım boyunca bir rolü = 1024 geçiş ve bir düzine saniye çevre zamanı.

> Çıkarım çok pahalı. Atari'de 8 ̊ ortam × 128 ̊ adım = 1024 kez dönüşüm ve 10 saniyelik ortam süresi.

Güven Bölgesi Politikası Optimize edilmesi (TRPO, Schulman 2015) ilk çözümdür: her güncellemeyi kısıtlayın, böylece eski ve yeni politikalar arasındaki KL farklılığı aşağıda kalır `δ`Teorik olarak temiz ama her güncelleme için bir konjugat-gradyen çözümü gerektirir.

> TRPO, Schulman 2015) ilk modification:约束每次更新使新旧策略的 KL 散度保持在`δ`Aşağıda: teorik olarak iyi, ancak her güncelleme bir çözüm gerektirir.

PPO (Schulman et al. 2017) sert güven bölgesinin kısıtlamasını basit bir kesilmiş hedef ile değiştirir. Bir ekstra kod satırı. Her dağıtım için on dönem. Konjugat gradient yoktur. Yeterince iyi teorik garantiler.

> PPO(Schulman 等人 2017) basit bir kesim hedefiyle değiştirmek için bir kod satırı daha var. Her bir devreye 10 dönem gerek yok.

> **【中文解读】**PPO'nun temel yeniliği: TRPO'nun sert kısıtlamalarını değiştirmek için kesme hedefi kullanmak. Önemlilik oranı r_t(theta) = pi_theta / pi_old kesilmiş [1-epsilon, 1+epsilon] aralığında.

> **【拓展：PPO 之外的选择——DPO 与 GRPO】**PPO ⇒ 2026 yılının standart seçimi olmasına rağmen, alternatif programlar yükselmekte. DPO ⇒ Direct Preference Optimization (Direct Preference Optimization) doğrudan eğitim stratejisine tercihten atladı.

## Konsepten bir şey.

![PPO clipped surrogate objective: ratio clipping at 1 ± ε](../assets/ppo.svg)

**The importance ratio.**

`r_t(θ) = π_θ(a_t | s_t) / π_{θ_old}(a_t | s_t)`

Bu yeni politika ile verileri toplayan politika arasındaki olasılık oranıdır. `r_t = 1`Değişiklik yok demektir.`r_t = 2`Yeni politika iki kat daha fazla süre alacak.`a_t`Eski gibi.

> **重要性比率。**Yeni strateji ve veri toplama stratejisi arasındaki benzerlik.`r_t = 1`Değişiklik göstermedi.`r_t = 2`Yeni strateji göstermek`a_t`Oldukça iki kat daha olası.

**The clipped surrogate.**

`L^{CLIP}(θ) = E_t [ min( r_t(θ) A_t, clip(r_t(θ), 1-ε, 1+ε) A_t ) ]`

İki dönem:

- Eğer avantajı `A_t > 0`ve oranın ötesine çıkmaya çalışması `1 + ε`, klipi eğilimi düzeltir  iyi bir eylem daha fazla itmemek `+ε`Eski olasılıkların üstünde.
- Eğer avantajı `A_t < 0`ve oranın ötesine çıkmaya çalışması `1 - ε`(yani kötü bir eylemin kesilmiş azaltılmasına kıyasla daha olası hale getirileceğini gösterir) Klip, gradiyenti kapatır  kötü bir eylemin aşağıya itirilmesini engellemez `-ε`- Evet .

- Evet .`min`Diğer yönü ele alır: oran * yararlı* yönde hareket ettiyse, hala eğilimi alırsınız (bölgeye bir kesim yapmamak sizi incitebilir).

Tipik `ε = 0.2`. Hedefi bir fonksiyon olarak çiz .`r_t`: "iyi tarafta" düz bir çatı ve "kötü tarafta" düz bir zemin ile parça-düzsel bir işlev.

> **裁剪代理。**两项: Eğer avantajlar % ten fazla doğru ve oranlı ise`1 + ε`Sıralama , seviyesini düzeltme , iyi hareketleri eski olasılıklardan daha yüksek bir şekilde sürükleme .`+ε`更多── Eğer avantaj olumsuz ve oran düşükse `1 - ε`Kısıtlama, kısıtlama, kısıtlama.`-ε`更多──典型 `ε = 0.2`- Evet.

> **【中文解读】**PPO  kesim mekanizmasının içgüdü:epsilon=0.2 stratejinin her güncelleme en fazla %20 değişmesini ifade eder. Eğer bir hareket iyiyse (A>0), en fazla olasılığı %20 artıracaktır. Eğer bir hareket çok kötüse (A<0), en fazla %20 düşecektir. Bu, "katastrofe unutulması"  stratejinin bir adım daha fazla değişmeyeceğini önler.

**The full PPO loss.**

`L(θ, φ) = L^{CLIP}(θ) - c_v · (V_φ(s_t) - V_t^{target})² + c_e · H(π_θ(·|s_t))`

Aynı aktör-kritik yapı A2C ile.`c_v = 0.5`- Evet .`c_e = 0.01`- Evet .`ε = 0.2`- Evet .

> **完整的 PPO 损失。**A2C ile benzer Aktor-Kritik 結構── üç系数, genellikle `c_v = 0.5`- Evet.`c_e = 0.01`- Evet.`ε = 0.2`- Evet.

**The training loop.**

1. Toplayın .`N × T``N`paralel ortamlar için`T`Her adım.
2. Gelirleri hesaplayın (GAE), onları sabit olarak dondurun.
3. Dondurma`π_{θ_old}``π_θ`- Evet .
4. - Evet .`K`                        `(s, a, A, V_target, log π_old(a|s))`- ...
   - Hesaplama`r_t(θ) = exp(log π_θ(a|s) - log π_old(a|s))`- Evet .
   - Uygula`L^{CLIP}`+ değer kaybı + entropi.
   - - İlerleyici adım.
5. Çıkarmayı atın ve adım 1'e dönün.

`K = 10`PPO güçlüdür: tam sayı nadiren ±50%'lik bir değer içerir.

> **训练循环。**收集 → 计算 GAE 优势 → 结旧策略 → K 轮更新 → 丢弃数据──`K = 10`Ve 64'in küçük grupları standart süper parametrelerdir.

**KL-penalty variant.**Orijinal makalede adapte KL cezası kullanan bir alternatif önerildi: `L = L^{PG} - β · KL(π_θ || π_old)`- Evet .`β`KL'ye göre ayarlanmıştır. Klipleme sürümü baskın hale geldi; KL variansı RLHF'de hayatta kalıyor (RLHF'de KL'ye göre referans politikası her zaman istediğiniz ayrı bir kısıtlama olduğu).

> **KL 惩罚变体。**Orijinal makalede kendi kendine uyumlu KL  cezalarının alternatifleri önerilmiştir.

## Yapın.
```figure
ppo-clip
```

## Yapın

### Adım 1: Yakalama `log π_old(a | s)`Çıkarma zamanı

```python
for step in range(T):
    probs = softmax(logits(theta, state_features(s)))
    a = sample(probs, rng)
    s_next, r, done = env.step(s, a)
    buffer.append({
        "s": s, "a": a, "r": r, "done": done,
        "v_old": value(w, state_features(s)),
        "log_pi_old": log(probs[a] + 1e-12),
    })
    s = s_next
```

Fotoğraf bir kez çekilir, yayımlama sırasında.

> 快照在推出时拍摄一次──在更新时代 期间不变──

### Adım 2: GAE avantajlarını hesaplayın (Deneyim 07)

A2C'nin aynı şeyi.

> A2C ile aynı.

### Adım 3: Çıkarılmış yedek güncelleme

```python
for _ in range(K_EPOCHS):
    for mb in minibatches(buffer, size=64):
        for rec in mb:
            x = state_features(rec["s"])
            probs = softmax(logits(theta, x))
            logp = log(probs[rec["a"]] + 1e-12)
            ratio = exp(logp - rec["log_pi_old"])
            adv = rec["advantage"]
            surrogate = min(
                ratio * adv,
                clamp(ratio, 1 - EPS, 1 + EPS) * adv,
            )
            # backprop -surrogate, add value loss, subtract entropy
            grad_logpi = onehot(rec["a"]) - probs
            if (adv > 0 and ratio >= 1 + EPS) or (adv < 0 and ratio <= 1 - EPS):
                pg_grad = 0.0  # clipped
            else:
                pg_grad = ratio * adv
            for i in range(N_ACTIONS):
                for j in range(N_FEAT):
                    theta[i][j] += LR * pg_grad * grad_logpi[i] * x[j]
```

"Klip → sıfır gradient" modeli PPO'nun kalbidir. Yeni politika zaten yararlı yönde çok fazla ilerlediyse, güncelleme durur.

> "Kürt → 零梯度" modeli PPO'nun merkezinde yer alır. Yeni stratejiler olumlu yönde çok uzaklaşmışsa, yenilemeler durdurulur.

### Adım 4: Değer ve entropi

Kritik hedefe standart MSE ve A2C ile aynı şekilde aktörde entropi bonusu ekleyin.

> Kritiklere  hedef ekleme standartları MSE, aktörlere                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

### Adım 5: teşhis

Her güncellemeyi izlemek için üç şey:

> Her güncelleme için üç şey kontrol edilmeli:

- **Mean KL** `E[log π_old - log π_θ]`İçeride kalmalıydım .`[0, 0.02]`- Eğer geçmişte uçarsa .`0.1`, azaltmak`K_EPOCHS`veya `LR`- Evet .
  **平均 KL。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `[0, 0.02]` Eğer aşarsa `0.1`, reduk `K_EPOCHS`Ya da`LR`- Evet.
- **Clip fraction** oranı dışta bulunan örneklerin bölümü `[1-ε, 1+ε]`Olmalı .`~0.1-0.3`- Eğer ...`~0`, klipi asla                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `LR`veya `K_EPOCHS`- Eğer ...`~0.5+`- Bu yüzden, onları aşağı düşürmek için çok fazla ayarlıyorsun.
  **裁剪比例。**% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %`[1-ε, 1+ε]`                                                                                                                                                                                                                                                              `~0.1-0.3`- Evet.
- **Explained variance** `1 - Var(V_target - V_pred) / Var(V_target)`Eleştirmen öğrendiği gibi 1'e doğru tırmanmalı.
  **解释方差。**Kritik kalite göstergesi: 1.

## Tuzaklar

- **Clip coefficient mistuned.** `ε = 0.2`Bu gerçek standart.`0.1`güncellemeleri çok çekingen kılar .`0.3+`- Durum dengesizliği.
  **裁剪系数调错。** `ε = 0.2`Bu gerçek bir standart.`0.1`太保守;`0.3+`导致不稳定――
- **Too many epochs.** `K > 20`politikası uzaklaşır.`π_old`Özellikle büyük ağlar için sınırlama dönemleri.
  **太多 epoch。** `K > 20`- Sürekli olarak sabit değil.`π_old`太远―― sınırlı çağ, özellikle büyük ağ―
- **No reward normalization.**Büyük ödül ölçekleri, video aralığında yer alır.
  **没有奖励归一化。**Büyük ödül ölçüsü ısınma oranı ∞
- **Forgetting advantage normalization.**Satır başına sıfır ortalama/birlik std normallaştırma standarttır.
  **忘记优势归一化。**Her bir grupda sıfır ortalama değer/birlik standartı birleştirilmesidir.
- **Learning rate not decayed.**PPO, doğrusal LR'nin sıfıra düşmesinden yararlanır.
  **学习率未衰减。**PPO  線性 LR 衰减到零中受益──常数 LR 通常更差──
- **Importance ratio math errors.**Her zaman .`exp(log_new - log_old)`sayısal istikrar için değil `new / old`- Evet .
  **重要性比率数学错误。**始终使用 `exp(log_new - log_old)`Güvenli sayısal değeri sabitlik, değil `new / old`- Evet.
- **Wrong gradient sign.**Yeraltı anneni en üst seviyeye çıkar = *minimize* `-L^{CLIP}`- Dönüştürülmüş bir işaret en yaygın PPO virüsüdür.
  **梯度符号错误。**Maksimalleştirme temsilcisi = * minimize* `-L^{CLIP}`▽符号反转为 PPO 最常见 bug──

## Çerçeveyi kullanın.

PPO, 2026'ın şaşırtıcı sayıda alan üzerinde varsayılan RL algoritmasıdır:

> PPO 2026 yılının birçok alanında belirlenmiş RL algoritmasıdır:

| Use case | PPO variant |
|----------|-------------|
| Use case / 用例 | PPO variant / PPO 变体 |
| MuJoCo / robotics control / MuJoCo/机器人控制 | PPO with Gaussian policy, GAE(0.95) / 高斯策略的 PPO，GAE(0.95) |
| Atari / discrete games / Atari/离散游戏 | PPO with categorical policy, rolling 128-step rollouts / 分类策略的 PPO |
| RLHF for LLMs / LLM 的 RLHF | PPO with KL penalty to reference model, reward from RM at end of response / 带 KL 惩罚的 PPO |
| Large-scale game agents / 大规模游戏 Agent | IMPALA + PPO (AlphaStar, OpenAI Five) |
| Reasoning LLMs / 推理 LLM | GRPO (Lesson 12) — PPO variant without critic / 无 Critic 的 PPO 变体 |
| Preference-only data / 仅偏好数据 | DPO — closed-form collapsing of PPO+KL, no online sampling / 闭式 PPO+KL 折叠 |

PPO * kayb şekli*  kesilmiş alternatif + değer + entropi  DPO, GRPO ve neredeyse her RLHF boru hattı için asfalt.

> PPO'nun* kaybı biçimi* 剪代理 + 值 + 是 DPO、GRPO 和几乎所有RLHF 流水线的脚手架──

## İndirin . Ürünler .

- Kaydet .`outputs/skill-ppo-trainer.md`- ...

```markdown
---
name: ppo-trainer
description: Produce a PPO training config and a diagnostic plan for a given environment.
version: 1.0.0
phase: 9
lesson: 8
tags: [rl, ppo, policy-gradient]
---

Given an environment and training budget, output:

1. Rollout size. `N` envs × `T` steps.
2. Update schedule. `K` epochs, minibatch size, LR schedule.
3. Surrogate params. `ε` (clip), `c_v`, `c_e`, advantage normalization on.
4. Advantage. GAE(`λ`) with explicit `γ` and `λ`.
5. Diagnostics plan. KL, clip fraction, explained variance thresholds with alerts.

Refuse `K > 30` or `ε > 0.3` (unsafe trust region). Refuse any PPO run without advantage normalization or KL/clip monitoring. Flag clip fraction sustained above 0.4 as drift.
```

## Egzersizler.

1. **Easy.**4×4 GridWorld ' da PPO çalıştır `ε=0.2, K=4`. Örnek verimliliğini A2C ile (her bir atılım için bir dönem) eşleşen çevre adımlarında karşılaştırın.
2. **Medium.**Tarama`K ∈ {1, 4, 10, 30}`- Plan geri dönüşü vs. çevre adımları ve takip ortalaması KL güncelleme başına.`K`KL bu görevde patlayacak mı?
3. **Hard.**Kısaltılan yer değiştiricisini uyarlayıcı bir KL cezası ile değiştirin (`β`iki katına çıkarılır.`KL > 2·target`, yarıya düştü`KL < target/2`) Son dönüşü, istikrarı ve çubuksuzluğu karşılaştırın.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Importance ratio | "r_t(θ)" | `π_θ(a\|s) / π_old(a\|s)`; deviation from the policy that collected the data. |
| Clipped surrogate | "PPO's main trick" | `min(r·A, clip(r, 1-ε, 1+ε)·A)`; flat gradient past the clip on beneficial side. |
| Trust region | "TRPO / PPO intent" | Limit each update's KL to guarantee monotone improvement. |
| KL penalty | "Soft trust region" | Alternative PPO: `L - β · KL(π_θ \|\| π_old)`. Adaptive `β`. |
| Clip fraction | "How often clipping triggers" | Diagnostic — should be 0.1-0.3; outside means mistuned. |
| Multi-epoch training | "Data reuse" | K epochs on each rollout; variance cost traded for sample efficiency. |
| On-policy-ish | "Mostly on-policy" | PPO is nominally on-policy but K>1 epochs uses slightly-off-policy data safely. |
| PPO-KL | "The other PPO" | KL-penalty variant; used in RLHF where KL-to-reference is already a constraint. |

## Daha fazla okumak

- [Schulman et al. (2017). Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)- Gazete.
- [Schulman et al. (2015). Trust Region Policy Optimization](https://arxiv.org/abs/1502.05477)TRPO, PPO'nun öncüsü.
- [Andrychowicz et al. (2021). What Matters In On-Policy RL? A Large-Scale Empirical Study](https://arxiv.org/abs/2006.05990) her PPO hiperparametre silinmiş.
- [Ouyang et al. (2022). Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) InstructGPT; PPO-in-RLHF tarifi.
- [OpenAI Spinning Up — PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html)PyTorch ile temiz modern bir sergileme.
- [CleanRL PPO implementation](https://github.com/vwxyzjn/cleanrl) Referans bir dosya PPO birçok makalede kullanılır.
- [Hugging Face TRL — PPOTrainer](https://huggingface.co/docs/trl/main/en/ppo_trainer) dil modellerinde PPO için üretim tarifi; Ders 09 (RLHF) ile birlikte okuyun.
- [Engstrom et al. (2020). Implementation Matters in Deep Policy Gradients](https://arxiv.org/abs/2005.12729) "37 kod seviyesinde optimizasyon" makalesi; hangi PPO numaraları yük taşıyor ve hangiları folklor.
