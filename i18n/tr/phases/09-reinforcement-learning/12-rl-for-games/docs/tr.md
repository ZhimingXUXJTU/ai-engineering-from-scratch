# Oyunlar için RL  AlphaZero, MuZero ve LLM-Düşünme Çağı  game içindeki güçlü bir kemik öğrenimi  AlphaZero、 MuZero ve LLM 推理时代

> 1992: TD-Gammon, saf TD ile backgammon'da insan şampiyonlarını yendi. 2016: AlphaGo Lee Sedol'u yendi. 2017: AlphaZero, satranç, shogi ve Go'yu sıfırdan baskın etti. 2024: DeepSeek-R1 aynı tarifleri kanıtladı.

> **【中文解读】**游戏是 RL 突破的试验场:TD-Gammon (1992) → AlphaGo (2016) → AlphaZero (2017) → DeepSeek-R1 (2025)。DeepSeek-R1 证明了 AlphaZero'nun"self-Blog+search+strategy Improvement" döngüsü doğrudan büyük modelin matematiksel düşüncelerine uygulanabilir.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (MARL) | **前置知识:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (多智能体 RL)
**Time:** ~120 minutes | **时间:** ~120 分钟

## Sorunlar. Sorunlar.

Oyunlar RL'nin istediği her şeye sahiptir. Temiz ödül ( Kazanç / Kaybetme). Sonsuz bölümler (kendini oynayan yeniden ayarlamalar). Mükemmel simülasyon (oyun * simülatördür). Diskret veya küçük sürekli eylem alanları. Karşılıklı dayanıklılığı zorlayan çoklu ajan yapısı.

> Oyun, RL gerektiren her şeyi vardır. Açık bir ödül.

Ve oyunlar, RL'nin her büyük keşfi test edildiği bir yöntem. TD-Gammon (Backgammon, 1992). Atari-DQN (2013). AlphaGo (2016). AlphaZero (2017). OpenAI Five (Dota 2, 2019) AlphaStar (StarCraft II, 2019). MuZero (bilimli model, 2019). AlphaTensor (matris çarpımı, 2022). AlphaDev (sortlama algoritmaları, 2023). DeepSeek-R1 (Matematika mantığı, 2025)  oyun-RL tekniklerinin metinde çalıştığını gösteren en son gösterim.

> 游戏是每个 RL重大突破的试验场──TD-Gammon(西洋双陆棋,1992)、Atari-DQN(2013)、AlphaGo(2016)、AlphaZero(2017)、OpenAI Five(Dota 2,2019)、AlphaStar(星际争 II,2019)、MuZero(学习模型,2019)、AlphaTensor(矩阵乘法,2022)、AlphaDev(排序算法,2023)、DeepSeek-R1(数学 önerileri,2025)最新证明:游戏 RL 技术可用于文本──

Bu baş taşı, üç önemli mimarisi  AlphaZero, MuZero ve GRPO 'yu tek birleştiren lensle araştırır: **self-play + search + policy improvement**Her biri öncekiyi genelleştirir; GRPO özellikle AlphaZero'nun, kazanç sinyalini simgelendiren işlemler ve matematiksel doğrulama olarak tokenlerle LLM mantıklılığına uygulanan bir reçetesidir.

> Bu, tek bir bakış açısı ile sonuçlandı.**自我博弈+搜索+策略改进**审视三个里程碑架构:AlphaZero、MuZero 和 GRPO──每个都是前一个的推广;GRPO 特别是将 AlphaZero 的配方应用于LLM 推理,代号是动作,数学验证是获胜信号──

## Konsepten bir şey.

![AlphaZero ↔ MuZero ↔ GRPO: same loop, different environments](../assets/rl-games.svg)

**The unifying loop.**

```
while True:
    trajectory = self_play(current_policy, search)     # play game against self
    policy_target = search.improved_policy(trajectory) # search improves raw policy
    policy_net.update(policy_target, value_target)     # supervised on search output
```

**AlphaZero (2017).**Silver et al. Bilinen kurallarla bir oyun (şah, shogi, Go) verildiğinde:

- Politika değerleri ağı: bir kule `f_θ(s) → (p, v)`- Evet .`p`- Hukuk hareketleri konusunda öncü.`v`Bu oyunun beklenen sonucu.
- Monte Carlo Ağacı Arama (MCTS): Her harekette, olası devamlar ağacını genişlet.`(p, v)`UCB (PUCT) tarafından düğümleri seçin: `a* = argmax Q(s, a) + c · p(a|s) · √N(s) / (1 + N(s, a))`- Evet .
- Kendi oyununu oynayın: ajan karşısına oyun oynayın.`t`, MCTS ziyaret dağıtımı `π_t`politika eğitim hedefi haline gelir.
- Kayıp:`L = (v - z)² - π · log p + c · ||θ||²`- Evet .`z`oyunun sonucu (+1 / 0 / -1).

İnsan bilgisi sıfır, el yapımı heuristik sıfır, tek bir tarif, her biri birkaç on milyon kendi oyunundan sonra satranç, shogi ve go ustası.

> 零人类知识――零手工启发式―― bir biçim binlerce milyonu kendi kendini geliştirdikten sonra International Chess, Deger Chess ve Go Chess'i ele geçirdi.

**MuZero (2019).**Schrittwieser et al. Kurallar bilinmesi gerekliliğini kaldırır.

- Sıkı bir ortam yerine *latent dinamik modeli öğrenin*`(h, g, f)`- ...
  - `h(s)`: gözlemleri gizli bir duruma kodlama.
  - `g(s_latent, a)`: bir sonraki gizli durumu + ödül öngör.
  - `f(s_latent)`: politika öncesi tahmin + değer.
- MCTS * öğrenilen gizli alanda* çalışır. Aynı arama, aynı eğitim döngüsü.
- Go, satranç, shogi ve Atari'de çalışır. Bir algoritma, kural bilgisine sahip değil.

> Bu algoritma, kural bilgisi gerekmez.

> **【中文解读】**AlphaZero ve MuZero'nun çekirdek döngüsü: Self-Blog → MCTS  arama geliştirme stratejisi → 监督学习更新网络──AlphaZero 需要已知游戏规则,MuZero 通过学习隐空间动力学模型消除了这个限制──这个"自我博+搜索+策略改进"循环直接启动了DeepSeek-R1 的推理训练使用可验证奖励替代游戏胜负信号──

> **【拓展：DeepSeek-R1 与 AlphaZero 范式】**DeepSeek-R1(2025) AlphaZero'nun paradigmasını LLM'de uygulayacak. 推理:token就是动作,推理过程就是"游戏",验证器(mathematics题对错、代码是否通过测试)就是"胜负信号"──GRPO 替代PPO,组内采样替代自我博──

**Stochastic MuZero (2022).**Stochastic dinamikleri ve şans düğümlerini ekler; backgammon sınıfı oyunlara uzanır.

> **随机 MuZero (2022)。**添加随机动力学和机会节点; ikili ülke oyunlarına yayıldı。

**Muesli, Gumbel MuZero (2022-2024).**Örnek verimliliği ve belirleyici arama konusunda gelişmeler.

> **Muesli、Gumbel MuZero (2022-2024)。**样本效率 ve kesinlik aramalarının gelişmesi

**GRPO (2024-2025).**DeepSeek-R1 tarifi, AlphaZero şeklinde aynı döngü, dil modeline uygulanır:

- "Game": bir matematik / kodlama / akıl yürütme sorunu cevaplayın. "Win" = doğrulayıcı (test vakaları geçiyor, sayısal cevap eşleşir) 1 gönderir.
- Politikası: LLM. Eylemler: tokenler. Devlet: hızlı + tepki-bkz.
- Hiçbir eleştirmen yok (PPO tarzı V_φ).`G`Politika'nın tamamlanması.**group-relative advantage** `A_i = (r_i - mean_r) / std_r`REINFORCE tarzında güncelleme için sinyal olarak.
- KL'nin geri çekilmeyi önlemek için referans politikasına yönelik ceza (RLHF gibi).
- Tam kaybı:

  `L_GRPO(θ) = -E_{q, {o_i}} [ (1/G) Σ_i A_i · log π_θ(o_i | q) ] + β · KL(π_θ || π_ref)`

Ödül modeli, eleştirmen, MCTS yoktur. Grup-sâlamlı temel üçü de değiştirir. Hesaplamaların bir kısmında akıl yürütme referansları üzerinde PPO-RLHF kalitesi ile eşleşir veya üstlenir.

> **GRPO (2024-2025)。**DeepSeek-R1 配方── aynı AlphaZero 形状循环, 应用于语言模型推理:不需要奖励模型、Critic 或 MCTS──组相对基线替代了三者──在推理基准上匹配或超越 PPO-RLHF 质量,计算量仅为一小部分──

> **【中文解读】**GRPO, DeepSeek-R1'in temel yenilemidir: kritik 网络(省一半内存), grup içindeki ortalama değer ve standart fark yapılandırma avantajları. G 个回答, her soruya doğru cevapların avantajları doğru 增强概率), yanlışların olumsuz 降低概率 olarak kullanılır.

> **【拓展：GRPO→DeepSeek-R1→开源推理革命】**DeepSeek-R1'in dört aşamalı eğitim süreci: soğuk başlatma SFT → 推理导向 GRPO → 拒绝采样+SFT → 全谱 GRPO──R1-Zero(純 GRPO 无 SFT) LLM'yi 0 学会推理, ancak输出可读性差──蒸 deney gösterir: güçlü RL öğretmenlerinin推理轨迹 kullanılarak SFT yapın, küçük modellerden RL 效果ları daha iyi yapın.

**The R1 recipe in full.**DeepSeek-R1 (DeepSeek 2025) bir kağıtta iki modelden oluşur:

> **R1 完整配方。**DeepSeek-R1 bir makalede iki modelden oluşuyor:

- **R1-Zero.**DeepSeek-V3 temel modelinden başlayın. SFT yoktur. GRPO'yu doğrudan iki ödül bileşeniyle uygulayın: * doğruluk ödülü* (kurallara dayalı  son cevap doğru sayıya analiz etti / kod birim testlerini geçti mi) ve * format ödülü* (önüntüsü zincirini içine sarmış mı)`<think>…</think>`Etiketler). Binlerce adım boyunca, ortalama yanıt uzunluğu ~100'den ~10.000'e kadar büyür ve matematik referans puanları neredeyse o1 ön izleme seviyelerine tırmanır. Model sıfırdan mantık etmeyi öğrenir.
- **R1.**R1-Zero'nun okunma sorunlarını dört aşamalı bir boru hattıyla çözün:
  1. **Cold-start SFT.**Birkaç bin uzun CoT gösterisini temiz biçimlendirme ile toplayın.
  2. **Reasoning-oriented GRPO.**Kod değişimini önlemek için GRPO'yu doğruluk + biçim ödülleri ve *dilli tutarlılık* ödülü ile uygulayın.
  3. **Rejection sampling + SFT round 2.**RL kontrol noktasından ~ 600K mantık trajektörlerini örnekleyin, sadece doğru son cevapları ve okunur CoT'leri olanları tutun ve ~ 200K mantık dışı SFT örnekleriyle (yazma, sorgulama, kendi kendini tanımlama) birleştirin.
  4. **Full-spectrum GRPO.**Bir RL daha, hem akıl yürütme (kurallara dayalı ödüller) hem de genel uyum (karşılıklılık/hasırsızlık tercihlerine dayalı ödüller) kapsamaktadır.

Sonuç açık ağırlıklarda AIME ve MATH-500'de o1 ile eşleşir ve destille edilecek kadar küçüktür. Aynı makale aynı zamanda R1'nin akıl etmesi izlerine SFT'ye göre altı destille edilmiş yoğun model (Qwen-1.5B ile Llama-70B) serbest bırakır.

> 果da AIME 和 MATH-500 上匹配 o1,且足够小可以蒸──蒸强 RL Öğretmeninin düşünce tarzı öğrenci boyutundan daha iyi olmuştur RL──

**Why GRPO instead of PPO for reasoning.**DeepSeekMath makalesinde (Feb 2024) üç neden: (1) eğitmek için değer ağı yoktur, hafıza yarıya kısaltılır; (2) grup tabanı doğal olarak akıl yürütme görevlerinin ürettiği nadir bir yolculuğun son ödülünü ele alıyor; (3) anlık normalleşme, PPO'nun tek eleştirmeninin yapamayacağı çok farklı zorluklarla ilgili sorunlar arasında karşılaştırılabilir avantajları sağlar.

> **为什么推理用 GRPO 而非 PPO。**Üç neden: 1) 无需训练值网络,内存减半; 2) 组基线自然处理推理任务产生的稀疏回合末奖励; 3) Her nokta birleşmesi, zorluklarda büyük farklarda avantaj yaratır.

**Search-free vs search-based.**Oyunlar şubelerle ayrılmıştır:

> **Search-free vs search-based.**

- *Uzun ufuklarla mükemmel bilgi oyunları* (Go, satranç): hala arama tabanlı. AlphaZero / MuZero hakim.
- *LLM mantıklılığı*: henüz üretimde MCTS yok; GRPO tam dağıtımlarda, sonuç hesaplama için en iyi N. Proses ödül modelleri (PRM) adım düzeyde arama eklenmeye işaret ediyor.

## Yapın.
```figure
f3-selfplay-ladder
```

## Yapın

Kodun içinde .`code/main.py`uygulamalar **GRPO in miniature** bir örnek grupları olan bir çeteci. Algoritm bir LLM ile aynıdır; sadece politika ve ortam daha basit. * kayıp * ve * grubun ilişkili avantajı * öğretir, bu da 2025 yeniliktir.

> `code/main.py`İç kod gerçekleştirildi**微型 GRPO**Bir çok grup örneği olan 博机── LLM'de algoritma aynıdır; sadece strateji ve ortam daha basit── bu profesör* kayb* ve* grup karşı avantajlar*, bu 2025 yılının yeniliktir──

### Adım 1: Küçük bir doğrulama ortamı

```python
QUESTIONS = [
    {"prompt": "q1", "correct": 3},
    {"prompt": "q2", "correct": 1},
]

def verify(prompt_idx, answer_token):
    return 1.0 if answer_token == QUESTIONS[prompt_idx]["correct"] else 0.0
```

Gerçek GRPO'da doğrulayıcı birim testleri yürütür veya matematiksel eşitliği kontrol eder.

> Gerçek GRPO 中验证器运行单元测试或检查数学等式──

### Adım 2: Politika: K cevap simgelerinden softmax / prompt

```python
def policy_probs(theta, p_idx):
    return softmax(theta[p_idx])
```

Bir HLM'nin en son katman çıkışına eşdeğer.

> LLM'nin son aşamasında verilen önerilerle sonuçlanmaktadır.

### Adım 3: Grup örneği ve gruplara göre avantaj

```python
def grpo_step(theta, p_idx, G=8, beta=0.01, lr=0.1, rng=None):
    probs = policy_probs(theta, p_idx)
    samples = [sample(probs, rng) for _ in range(G)]
    rewards = [verify(p_idx, s) for s in samples]
    mean_r = sum(rewards) / G
    std_r = stddev(rewards) + 1e-8
    advs = [(r - mean_r) / std_r for r in rewards]

    for a, A in zip(samples, advs):
        grad = onehot(a) - probs
        for i in range(len(probs)):
            theta[p_idx][i] += lr * A * grad[i]
    # KL penalty: pull theta toward reference
    for i in range(len(probs)):
        theta[p_idx][i] -= beta * (theta[p_idx][i] - reference[p_idx][i])
```

Grup-sare avantajı 2024 DeepSeek hilesi. Eleştirmen gerekmez. "Baş çizgi" grup ortalamasıdır ve normallaşım grup std kullanır.

> 组相对优势是 2024年DeepSeek'in teknikleri──无需批判──"基线"是组平均值,归结使用组标准差──

### Adım 4: REINFORCE'nin başlangıç seviyesine karşılaştır (değersiz)

Aynı ayar, aynı hesaplama, basit bir REINFORCE.

> Aynı ayar, aynı hesaplama, saf güçlendirme.

### Adım 5: Entropi ve KL'yi gözlemleyin

RLHF ile aynı teşhisler: referans için KL, politika entropi, ödül-over-time.

> RLHF ile benzer teşhis: ortalama KL'ye referans strateji, strateji, ödül zamanla değişir.

## Tuzaklar

- **Reward hacking via verifier gaming.**GRPO, RLHF'nin riskini miras alır: Eğer doğrulayıcı yanlış ya da sömürülebilirse, LLM sömürüyü bulacaktır.
  **通过验证器博弈的奖励黑客。**GRPO RLHF'nin riskini miras aldı: Eğer testçi yanlış veya kullanılabilirse, LLM bir hata bulacaktır.
- **Group size too small.**Grup başlangıç çizgisinin değişimi şöyle `1/√G`Aşağıda .`G = 4`, avantaj sinyali gürültülü , standart seçenek `G = 8`- ...`64`- Evet .
  **组大小太小。**组基线的方差与 `1/√G`- Tamam.`G = 4`Aşağıdaki avantaj sinyaller gürültü; standart seçim `G = 8`- Ne ?`64`- Evet.
- **Length bias.**Farklı uzunluklarda LLM tamamlamaları farklı log- olasılıklara sahiptir. Token sayısına göre normalleştirin veya dizi düzeyde log-prob kullanın veya maksimum uzunlukta kesin.
  **长度偏差。**Farklı boyutlu LLM'nin tamamlanması farklı sayısal olasılıkla gerçekleşir.
- **Pure self-play cycles.**AlphaZero tarzı eğitim genel toplam oyunlarında egemenlik döngüsünde sıkışabilir.
  **纯自我博弈循环。**AlphaZero'nun genel ve genel olarak kontrol döngüsüne düşebileceği bir durumdur.
- **Search-policy mismatch.**AlphaZero, arama sonuçlarını taklit etmek için politikaları eğitir. Eğer politika ağı aramaların dağılımını temsil etmek için çok küçükse, eğitim stallları.
  **搜索-策略不匹配。**AlphaZero trenning strategy simulated search output── Eğer strateji ağı çok küçükse arama dağılımını gösteremezse, eğitim durur──
- **Compute floor.**MuZero / AlphaZero büyük hesaplamalara ihtiyaç duyar. Tek bir ablation genellikle yüzlerce GPU-saati tutar. Öğrenmek için miniatür demolar vardır (örneğin, Connect Four'da AlphaZero).
  **计算下限。**MuZero/AlphaZero  çok fazla hesaplama gerektirir.
- **Verifier coverage.**Bir hata çözümü için geçerli olan birim testleri, hatayı güçlendirir.
  **验证器覆盖。**通过有bug 解决方案的单元测试会强化 bug;;设计能捕获边缘情况的验证器;;

## Çerçeveyi kullanın.

2026 oyun-RL manzarası, alanlar doğrultusunda:

> 2026 yıl oyun RL 版图, Bölgeye göre:

| Domain | Dominant method |
|--------|-----------------|
| Domain / 领域 | Dominant method / 主导方法 |
| Two-player zero-sum board games (Go, chess, shogi) / 双人零和棋类 | AlphaZero / MuZero / KataGo |
| Imperfect info card games (poker) / 不完全信息纸牌 | CFR + deep learning (DeepStack, Libratus, Pluribus) / CFR + 深度学习 |
| Atari / pixel games / Atari/像素游戏 | Muesli / MuZero / IMPALA-PPO |
| Large multiplayer strategy (Dota, StarCraft) / 大型多人策略 | PPO + self-play + league (OpenAI Five, AlphaStar) |
| LLM math/code reasoning / LLM 数学/代码推理 | GRPO (DeepSeek-R1, Qwen-RL, open replications) |
| LLM alignment / LLM 对齐 | DPO / RLHF-PPO (not GRPO; verifier is preference not verifiable) / DPO/RLHF-PPO |
| Robotics / 机器人 | PPO + DR (not game-RL, but uses same policy-gradient tools) / PPO+DR |
| Combinatorial problems / 组合问题 | AlphaZero variants (AlphaTensor, AlphaDev) / AlphaZero 变体 |

*Recipe*  kendi kendine oynamak, arama artırılmış geliştirme, politika destilasyonu  metin, piksel ve fiziksel kontrolden uzanır. GRPO en genç örnektir; daha fazlası geliyor.

> Bu * biçim* öz-büyüklük, arama güçlendirme geliştirme, strateji, çap çapında metin, biçim ve fiziksel kontrol.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-game-rl-designer.md`- ...

```markdown
---
name: game-rl-designer
description: Design a game-RL or reasoning-RL training pipeline (AlphaZero / MuZero / GRPO) for a given domain.
version: 1.0.0
phase: 9
lesson: 12
tags: [rl, alphazero, muzero, grpo, self-play]
---

Given a target (perfect-info game / imperfect-info / Atari / LLM reasoning / combinatorial), output:

1. Environment fit. Known rules? Markov? Stochastic? Multi-agent? Informs AlphaZero vs MuZero vs GRPO.
2. Search strategy. MCTS (PUCT with learned prior), Gumbel-sampled, best-of-N, or none.
3. Self-play plan. Symmetric self-play / league / offline data / verifier-generated.
4. Target signal. Game outcome / verifier reward / preference / learned model. Include robustness plan.
5. Diagnostics. Win rate vs baseline, ELO curve, verifier pass rate, KL to reference.

Refuse AlphaZero on imperfect-info games (route to CFR). Refuse GRPO without a trusted verifier. Refuse any game-RL pipeline without a fixed baseline opponent set (self-play ELO is uncalibrated otherwise).
```

## Egzersizler.

1. **Easy.**GRPO ' yu kullanın .`code/main.py`. 2 çağrıda + 4 cevap simgesi her biri üzerinde çalış.`G=8`- Evet .
2. **Medium.**PPO ve vanilya REINFORCE'yi bağlayın.
3. **Hard.**Bir uzunluk-2 "düşünme zinciri"ne kadar uzan: ajan iki token gönderir ve doğrulayıcı çiftini ödüllendirir. GRPO'nun iki adımlı diziler boyunca kredi tahsisini nasıl ele aldığını ölç. (Tavsiye: * tam dizide hesap grup avantajı*, her iki token pozisyonuna yayıl.)

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| MCTS | "Tree search with learned net" / 蒙特卡洛树搜索 | Monte Carlo Tree Search; UCB1/PUCT selection with learned `(p, v)` priors. |
| AlphaZero | "Self-play + MCTS" / AlphaZero | Policy-value net trained to match MCTS visits and game outcome. |
| MuZero | "Learned-model AlphaZero" / MuZero | Same loop but in latent space via learned dynamics. |
| GRPO | "Critic-free PPO" / 组相对策略优化 | Group Relative Policy Optimization; REINFORCE with group-mean baseline + KL. |
| PUCT | "AlphaZero's UCB" / PUCT 选择公式 | `Q + c · p · √N / (1 + N_a)` — balances value estimate with prior. |
| Self-play | "Agent vs past self" / 自我博弈 | Standard for zero-sum; symmetric training signal. |
| League play | "Population-based self-play" / 联盟训练 | Past + current + exploiters sampled as opponents. |
| Verifier reward | "Verifiable RL" / 验证器奖励 | Reward comes from a deterministic checker (tests pass, answer matches). |
| Process reward | "PRM" / 过程奖励模型 | Scores each reasoning step, not just the final answer. |

## Daha fazla okumak

- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270)- Evet .
- [Silver et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play (AlphaZero)](https://www.science.org/doi/10.1126/science.aar6404)- Evet .
- [Schrittwieser et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model (MuZero)](https://www.nature.com/articles/s41586-020-03051-4)- Evet .
- [Vinyals et al. (2019). Grandmaster level in StarCraft II (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z)- Evet .
- [DeepSeek-AI (2024). DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO)](https://arxiv.org/abs/2402.03300) GRPO ve grup ilişkili temel değerleri tanıtan makale.
- [DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) R1 4 aşamalı resepti artı R1-Zero ablasyonu.
- [Brown et al. (2019). Superhuman AI for multiplayer poker (Pluribus)](https://www.science.org/doi/10.1126/science.aay2400) CFR + derin öğrenme ölçeğinde.
- [Tesauro (1995). Temporal Difference Learning and TD-Gammon](https://dl.acm.org/doi/10.1145/203330.203343)- Herşeye başlayan gazete.
- [Hugging Face TRL — GRPOTrainer](https://huggingface.co/docs/trl/main/en/grpo_trainer) GRO'yu özel ödül fonksiyonlarıyla uygulayacak üretim referansı.
- [Qwen Team (2024). Qwen2.5-Math — GRPO replication](https://github.com/QwenLM/Qwen2.5-Math) R1 tarifinin birden fazla ölçekte açık şekilde çoğaltılması.
- [Sutton & Barto (2018). Ch. 17 — Frontiers of Reinforcement Learning](http://incompleteideas.net/book/RLbook2020.pdf) R1'in LLM ölçeğinde oluşturduğu kendi oyun, arama ve "önemli ödül" için ders kitabı çerçevesini.
