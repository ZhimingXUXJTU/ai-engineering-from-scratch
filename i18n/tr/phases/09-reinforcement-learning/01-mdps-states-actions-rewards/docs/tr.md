# MDP, Devletler, Eylemler ve Ödüller

> Markov Karar Süreci beş şeyden oluşur: durumlar, eylemler, geçişler, ödüller, indirim. RL  Q-öğrenme, PPO, DPO, GRPO 'daki her şey bu şekil üzerinde optimize eder. Bir kez öğrenin, kalan güçlendirme öğrenimini ücretsiz olarak okuyun.

> **【中文解读】**马尔可夫 karar alma süreci (MDP) beş unsur içerir: durum, hareket, dönüşüm olasılığı, ödül fonksiyonu, indirim faktörü, RL içindeki her şey, Q-öğrenme, PPO, DPO, GRPO  hepsi bu çerçeve üzerinde iyileştirilmiştir.

> **【拓展：MDP 是 AI 对齐的基础】**ChatGPT'nin RLHF  eğitimi doğasında da bir MDP: status= dialog上下文,动作=生成的代币,奖励=人类偏好评分――理解 MDP is understanding大模型对齐技术的起点――

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 1 · 06 (Probability & Distributions), Phase 2 · 01 (ML Taxonomy) | **前置知识:** Phase 1 · 06 (概率与分布), Phase 2 · 01 (ML 分类)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Bir satranç robotu ya da bir stok planlayıcısı ya da bir ticaret ajanı ya da bir mantık modeli eğitilen PPO döngüsü yazıyorsunuz.

> Bir dünya oyun makinesi ya da bir stok planlayıcı ya da bir ticaret temsilcisi ya da bir PPO modelini düşünmeyi öğrenen bir yazıyorsun.

Gözetimli öğrenme size verir .`(x, y)`Bu, bir çiftin bir fonksiyona uygun olmasını ve bir fonksiyona uygun olmanızi ister. Güçlendirme öğrenimi size etiket vermez. Sadece bir devlet akımı, yaptığınız eylemler ve bir skalar ödül.

> 监督学习给你 `(x, y)`Evet, size bir fonksiyona uygun olmanıza izin verin. Güçlendirme öğrenimi size etiketler vermez. Sadece durum akışı, aldığınız hareketi ve bir ölçüm ödülü.

Bu akıştan, bunu resmileştirmeden öğrenemezsiniz. "Ne gördüm", "ne yaptım", "ne oldu, "ne kadar iyiydi"  her biri mantık edebileceğiniz bir nesne haline gelmelidir. Bu resmileştirme Markov Karar Süreci'dir. Bu aşamada bulunan her RL algoritması, sonunda RLHF ve GRPO döngüleri de dahil olmak üzere, bu şekil üzerinde optimize eder.

> Bu veriler akışından, formüle edene kadar öğrenemezsiniz. "Ne gördüm""",Ne yaptım""",Ne oldu""",Ne oldu""",Ne oldu""",Ne oldu"""Bu çok iyi" Her biri düşünülebilir bir nesne olmalıdır. Bu formüle edilme, Markov'un karar verme süreci olarak görülmektedir. Bu aşamada RL algoritmasının her biri, son RLHF ve GRPO döngüsü dahil olmak üzere, tüm bu yapı üzerinde optimize edilmektedir.

## Konsepten bir şey.

![Markov decision process: states, actions, transitions, rewards, discount](../assets/mdp.svg)

**The five objects.**- Ne ?**五个核心要素。**

- **States** `S`Agentin karar vermesi gereken her şey. GridWorld'da hücre, satrançta tahta, LLM'de bağlam penceresi ve herhangi bir hafıza.
  **状态** `S`△ Akıllı vücut karar verme için gerekli tüm bilgiler── GridWorld'de kart, International Chess'de kart, LLM'de üst penceresinde hatırlamalar ∼
- **Actions** `A`Seçenekler, yukarı/ aşağı/ sola/ sağa hareket et.
  **动作** `A`△可选的操作──上/下/左/右移动──下一步棋──生成一个标志──
- **Transitions** `P(s' | s, a)`- Durum verildiğinde .`s`ve eylemler`a`Satrançta belirgin, stokastik envanterde, LLM'de neredeyse belirgin.
  **转移概率** `P(s' | s, a)`❖ belirlenmiş durum`s`Hızlı hareketler`a`, bir sonraki durum dağılımı, uluslararası şoklarda kesinlik, stok yönetimlerinde rastlantı, LLM çözümü, yakın kesinliktir.
- **Rewards** `R(s, a, s')`- Skalaar sinyal. Kazanç = +1, Kayıp = -1. Gelir eksi maliyet.
  **奖励** `R(s, a, s')`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △          △                                       
- **Discount** `γ ∈ [0, 1)`Gelecekteki ödülün ne kadarı var ?`γ = 0.99`~ 100 adımlık ufuk alır; `γ = 0.9`- 10'u alır.
  **折扣因子** `γ ∈ [0, 1)`Gelecek ödülleri, mevcut ödüllerin ağırlığı ile karşılaştırıldığında.`γ = 0.99`100 adımlık etkin bir görüş alanı;`γ = 0.9`10 adım daha fazla.

**The Markov property** `P(s_{t+1} | s_t, a_t) = P(s_{t+1} | s_0, a_0, …, s_t, a_t)`Gelecek sadece mevcut durumdan bağlıdır. Eğer öyle değilse, devlet temsilcisi eksiktir.

> **马尔可夫性质**Gelecek sadece mevcut durumdan asılıdır. Eğer oluşmazsa, durumun eksikliği, yöntemin başarısızlığı değil, durumun başarısızlığı anlamına gelir.

**Policies and returns.**Bir politika`π(a | s)`Haritalar, hareket dağılımlarına ilişkin durumları gösterir.`G_t = r_t + γ r_{t+1} + γ² r_{t+2} + …`gelecek ödüllerin indirimli toplamıdır.`V^π(s) = E[G_t | s_t = s]``s`Politikası altında`π`- Q değerini .`Q^π(s, a) = E[G_t | s_t = s, a_t = a]`Bu iki işlemden birini tahmin eden her RL algoritması, daha sonra iyileştirir.`π`Bu yüzden.

> **策略与回报。**策略 `π(a|s)`                                                                                                                                                                                                                                                              `G_t`Bu, gelecek ödüllerin indirimleri ve değer fonksiyonlarıdır.`V^π(s)`Durumdan`s`Çıkışın beklentileri`Q^π(s,a)`Bu iki rakamdan biri olarak değerlendirilmiş ve sonra bu stratejiyi geliştirilmiştir.

**The Bellman equations.**Bu aşamada her şeyin kullandığı sabit nokta denklemleri:

`V^π(s) = Σ_a π(a|s) Σ_{s', r} P(s', r | s, a) [r + γ V^π(s')]`

> **【中文解读】**Bellman denklemi RL'nin temel öne sürme ilişkisidir: mevcut durum değer = 即時獎勵 + 折扣後下一状態価値── bu, hareketli planlama、Q-öğrenme、TD öğrenme ortak temelidir── LLM'nin RLHF eğitiminde, bu " mevcut token katkı = insan tercihleri oranı + 未来 token'un beklenen katkı"ya karşılık gelir.

> **【拓展：从 MDP 到 POMDP】**现实中很多问题不满足马尔可夫性 (现状不能完全决定未来), POMDP (POMDP) 部分可观察 MDP) 建模――对话系统就是 POMDP (POMDP) 模型只能看到上下文窗口内的内容,而非完整的用户意图――LLM'的长上下文能力本质上缓解 POMDP'in信息不完整的问题――
`Q^π(s, a) = Σ_{s', r} P(s', r | s, a) [r + γ Σ_{a'} π(a'|s') Q^π(s', a')]`

Bu bölünme beklenen "bu adım ödül" artı "hiç yere düştüğünüz yerin indirim değeri" olarak geri döner. Tekrarlı. 9. aşamada her algoritma bu denklemi ya bir yaklaşım (dinamik programlama), ondan örnekler (Monte Carlo) veya bir adım (zaman farkı) ile yeniden başlatır.

> Bu işlemlerin geri dönüşü "hazırdaki adımların ödüllerine" ekleyerek "devlete ulaşma indirim değeri" olarak ayrılır.

## Yapın.
```figure
discount-horizon
```

## Yapın

### Adım 1: Küçük bir deterministik MDP

Agent yukarıdan sola, terminal aşağıdan sağ, ödül adım başına -1'dir, eylemler.`{up, down, left, right}`Bakın .`code/main.py`- Evet .

> Bir 4×4'ün ağ biçimi dünyası. Akıllı vücut sol üst köşeden çıkıyor, son durum sağ alt köşede, her adım ödüllendirildi -1, hareket edildi `{上, 下, 左, 右}`- Evet.

```python
GRID = 4
TERMINAL = (3, 3)
ACTIONS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

def step(state, action):
    if state == TERMINAL:
        return state, 0.0, True
    dr, dc = ACTIONS[action]
    r, c = state
    nr = min(max(r + dr, 0), GRID - 1)
    nc = min(max(c + dc, 0), GRID - 1)
    return (nr, nc), -1.0, (nr, nc) == TERMINAL
```

Beş çizgi, tüm çevre bu. Deterministik geçişler, sürekli adım cezaları, terminal durumu absorbe etmek.

> 五行代码──这是整个环境──确定性转移、恒定步惩罚、吸收终止状态──

### İkinci adım: Bir politika oluşturmak

Bir politika, devletten eylemlere dağılım fonksiyonudur. En basit: eşsiz rastgele.

> 策略は状態から動作分布の関数です.

```python
def uniform_policy(state):
    return {a: 0.25 for a in ACTIONS}

def rollout(policy, max_steps=200):
    s, total, steps = (0, 0), 0.0, 0
    for _ in range(max_steps):
        a = sample(policy(s))
        s, r, done = step(s, a)
        total += r
        steps += 1
        if done:
            break
    return total, steps
```

Bu 4×4 tablo için ortalama geri dönüş -60 ila -80 civarındadır. Optimal geri dönüş -6 (sürekli çizgi yolu aşağı doğru) dir. Bu boşluğu kapatmak 9. aşamada her şey.

> 运行随机策略 1000 次── bu 4×4 棋盘'ın ortalama dönüşü yaklaşık -60 ila -80── en iyi dönüşü -6(直线路径向右下方)── bu farkın azaltılması 9. aşamada tüm hedeflerdir──

### Adım 3: hesaplama`V^π`Tam olarak Bellman denkleminden

Küçük MDP'ler için Bellman denkleminin bir çizgisi vardır. Sayım durumları, beklentiyi uygulayın, değerlerin değişmesini durdurana kadar tekrarlayın.

> Küçük MDP için, Bellman denklemi bir 線性系である.

```python
def policy_evaluation(policy, gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in all_states()}
    while True:
        delta = 0.0
        for s in all_states():
            if s == TERMINAL:
                continue
            v = 0.0
            for a, pi_a in policy(s).items():
                s_next, r, _ = step(s, a)
                v += pi_a * (r + gamma * V[s_next])
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            return V
```

Bu, Sutton & Barto'daki ilk algoritmadır ve ardından gelen her RL yöntemi için teorik temeldir.

> Bu, Sutton & Barto öğretim kitabındaki ilk algoritmadır ve tüm RL yöntemlerinin teorik temelidir.

### Dördüncü adım:`γ`fiziksel anlamı olan bir hiperparametre

Etkili ufuk yaklaşık olarak `1 / (1 - γ)`- Evet .`γ = 0.9`→ 10 adım. `γ = 0.99`→ 100 adım. `γ = 0.999`→ 1000 adım.

> Etkili bir görüntü.`1 / (1 - γ)`- Evet.`γ = 0.9`10 adım.`γ = 0.99`100 adım.`γ = 0.999`1000 adım karşısında.

Çok düşük ve ajan kısa görüşlü davranır. Çok yüksek ve kredi tahsis gürültülü hale gelir, çünkü birçok erken adım uzun vadeli ödül için sorumluluk paylaşır. LLM RLHF tipik olarak kullanır `γ = 1`Çünkü bölümler kısa ve sınırlı.`0.95–0.99`Uzun üfüre strateji oyunları kullanıyor`0.999`- Evet .

> 折扣因子太低,智能体会目光短浅──太高,信用分配会变杂, çünkü birçok erken adım uzun vadeli ödül sorumluluğunu ortak olarak üstlenir──LLM RLHF genellikle kullanılır `γ = 1`, çünkü 回合短且有界──控制任务使用 `0.95-0.99`△长视野策略游戏使用 `0.999`- Evet.

## Tuzaklar

- **Non-Markovian state.**Eğer son üç gözlemden karar vermek istiyorsanız, "devlet" sadece mevcut gözlem değildir.
  **非马尔可夫状态。**Eğer son üç gözlem için bir karar gerekiyorsa, "stat" sadece şu anki gözlem değil.
- **Sparse rewards.**Sadece kazançlı ödüller, büyük devlet alanlarında öğrenmeyi neredeyse imkansız hale getirir.
  **稀疏奖励。**                                                                                                                                                                                                                                                              
- **Reward hacking.**Bir vekil ödülünü optimize etmek genellikle patolojik bir davranış üretir. OpenAI'nin tekne yarışları ajanı yarışı bitirmek yerine sonsuza dek güç toplayarak çevrelerde döner.
  **奖励黑客。**优化代理奖励常产生病态行为──OpenAI'nin yarışçı代理原地转圈收集道具,永远不完成比赛──始终从目标结果定义奖励,而非代理──
- **Discount mis-spec.** `γ = 1`Sonsuz ufuklı bir görevin her değerini sonsuz yapar.`γ < 1`- Evet .
  **折扣因子设定错误。**无限视野任务上  sınırsız görsel görevler`γ = 1`Bütün değerleri sonsuzluk için kullanır.`γ < 1`- Gelin.
- **Reward scale.**{+100, -100} vs {+1, -1} ödülleri aynı optimum politikaları verir ama büyük ölçüde farklı gradient büyüklükleri.`[-1, 1]`-PPO/DQN'e bağlanmadan önce.
  **奖励尺度。**{+100, -100} ile {+1, -1} ödülleri aynı en iyi stratejiyi verir, ancak seviye seviyesinin farkı büyüktür.`[-1, 1]`- Evet.

## Çerçeveyi kullanın.

2026 yığın, her RL borusunu kodla temas etmeden önce bir MDP'ye düşürür:

> 2026 yılında teknik  written code olmadan önce, her RL 流水线 bir MDP'ye dönüşecek:

| Situation | State | Action | Reward | γ |
|-----------|-------|--------|--------|---|
| Situation / 场景 | State / 状态 | Action / 动作 | Reward / 奖励 | γ |
| Control (locomotion, manipulation) / 控制（运动、操作） | Joint angles + velocities / 关节角度+速度 | Continuous torques / 连续力矩 | Task-specific shaped / 任务特定塑形 | 0.99 |
| Games (chess, Go, poker) / 游戏（象棋、围棋、扑克） | Board + history / 棋盘+历史 | Legal move / 合法走法 | Win=+1 / loss=-1 / 胜=+1/负=-1 | 1.0 (finite) |
| Inventory / pricing / 库存/定价 | Stock + demand / 库存+需求 | Order qty / 订购量 | Revenue - cost / 收入-成本 | 0.95 |
| RLHF for LLMs / LLM 的 RLHF | Context tokens / 上下文 token | Next token / 下一个 token | Reward-model score at end / 末尾奖励模型分数 | 1.0 (episode ~200 tokens) |
| GRPO for reasoning / 推理的 GRPO | Prompt + partial response / 提示+部分回复 | Next token / 下一个 token | Verifier 0/1 at end / 末尾验证器 0/1 | 1.0 |

Bir eğitim döngüsünü yazmadan önce beş tupleyi yazın. "RL çalışmıyor" hata raporlarının çoğu kağıt üzerinde kırılmış bir MDP formülasyonuna kadar uzanır.

> Herhangi bir eğitim döngüsünü yazmadan önce iyi bir beşlik oluşturmak için yazın.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-mdp-modeler.md`- ...

```markdown
---
name: mdp-modeler
description: Given a task description, produce a Markov Decision Process spec and flag formulation risks before training.
version: 1.0.0
phase: 9
lesson: 1
tags: [rl, mdp, modeling]
---

Given a task (control / game / recommendation / LLM fine-tuning), output:

1. State. Exact feature vector or tensor spec. Justify Markov property.
2. Action. Discrete set or continuous range. Dimensionality.
3. Transition. Deterministic, stochastic-with-known-model, or sample-only.
4. Reward. Function and source. Sparse vs shaped. Terminal vs per-step.
5. Discount. Value and horizon justification.

Refuse to ship any MDP where the state is non-Markovian without explicit mention of frame-stacking or recurrent state. Refuse any reward that was not defined in terms of the target outcome. Flag any `γ ≥ 1.0` on an infinite-horizon task. Flag any reward range >100x the typical step reward as a likely gradient-explosion source.
```

## Egzersizler.

1. **Easy.**4×4 GridWorld ve rastgele politika uygulaması uygulamak `code/main.py`- 10.000 bölüm çalıştırın. Geri dönüş ortalaması ve STD rapor edin.
   > **练习1（简单）：**实现 4×4 GridWorld 和随机策略 rollout──运行 10,000 回合──报告回报的平均值和标准差,与最优回报 (-6) 比较──
2. **Medium.**Çık .`policy_evaluation`- Evet .`γ ∈ {0.5, 0.9, 0.99}`- Üniformal rastgelelik politikası için.`V`Her biri için 4×4 şebekesi olarak. Terminal yakınındaki durum değerlerinin neden daha büyük olan daha hızlı büyüdüğünü açıklayın.`γ`- Evet .
   > **练习2（中等）：**Kullan .`γ ∈ {0.5, 0.9, 0.99}`运行策略评估──印每 γ'in 4×4 值网格──解释为什么接近终止状态的状态值在更大的 γ下增长更快──
3. **Hard.**GridWorld ' i stohastik çevir: her eylem olasılık ile bitişik bir yöne kayar `p = 0.1`- Üniforma politikasını yeniden değerlendirmek.`V[start]`- Daha iyi mi kötü mi?
   > **练习3（困难）：**GridWorld'ı her hareketin olasılığı için değiştirmek .`p = 0.1`滑向相邻方向── yeniden değerlendirme stratejisi──`V[start]`- İyi mi yoksa kötü mi?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
| MDP | "Reinforcement learning setup" | Tuple `(S, A, P, R, γ)` satisfying the Markov property. |
| State / 状态 | "What the agent sees" / "智能体看到什么" | Sufficient statistic for future dynamics under the chosen policy class. |
| Policy / 策略 | "Agent's behavior" / "智能体的行为" | Conditional distribution `π(a \| s)` or deterministic map `s → a`. |
| Return / 回报 | "Total reward" / "总奖励" | Discounted sum `Σ γ^t r_t` from the current step. |
| Value / 值函数 | "How good a state is" / "状态有多好" | Expected return under `π` starting from `s`. |
| Q-value / Q值 | "How good an action is" / "动作有多好" | Expected return under `π` starting from `s` with first action `a`. |
| Bellman equation / Bellman方程 | "Dynamic programming recursion" / "动态规划递推" | Fixed-point decomposition of value / Q into one-step reward plus discounted successor value. |
| Discount `γ` / 折扣因子 | "Future vs present" / "未来vs当前" | Geometric weight on far-future reward; effective horizon `~1/(1-γ)`. |

## Daha fazla okumak

- [Sutton & Barto (2018). Reinforcement Learning: An Introduction, 2nd ed.](http://incompleteideas.net/book/RLbook2020.pdf)3. bölüm MDP'leri ve Bellman denklemlerini kapsar; 1. bölüm her sonraki derslerin altında bulunan ödül hipotezini motive eder.
- [Bellman (1957). Dynamic Programming](https://press.princeton.edu/books/paperback/9780691146683/dynamic-programming) Bellman denkleminin kökeni.
- [OpenAI Spinning Up — Part 1: Key Concepts](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html) derin bir RL açısından kısa bir MDP primer.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887) MDP'ler ve tam çözüm yöntemleri ile ilgili operasyon-kağıt araştırma referansı.
- [Littman (1996). Algorithms for Sequential Decision Making (PhD thesis)](https://www.cs.rutgers.edu/~mlittman/papers/thesis-main.pdf) dinamik programlama uzmanlığı olarak MDP'lerin en temiz türü.
