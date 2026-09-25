# Çoklu ajanlı RL.

> Tek ajan RL, ortamın sabit olduğunu varsayır. Aynı dünyada iki öğrenme ajanı koyun ve bu varsayım bozulur: her ajan diğerinin ortamının bir parçasıdır ve her ikisi de değişiyor.

> **【中文解读】**单智能体 RL 假设环境是平稳的──但放入两个同时学习的智能体后,每个智能体都成为对方环境的一部分环境不再平稳,马尔可夫假设被打破──多智能体 RL 就是处理"大家都在变化"时的收收问题──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 04 (Q-learning), Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic) | **前置知识:** Phase 9 · 04 (Q-learning), Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Bir robot bir odayı gezinmeyi öğrenir. Tek ajan RL problemi. Bir futbol takımı değil. AlphaStar vs StarCraft rakipleri değil. Teklif yapan ajanların pazarı değil. Dört yönli durak müzakere eden iki araba değil. Birçok gerçek dünya sorunları değil.

> 机器人学习在房间中导航是单智能体 RL 问题──足球队不是──AlphaStar对StarCraft对手不是──竞价代理的市场不是──两辆车协商四路停车不是──多对多现实世界问题都不是──

Her çoklu ajan ortamında, herhangi bir ajanın bakış açısından diğer ajanlar * çevrenin bir parçasıdır. Öğrenirken ve davranışlarını değiştirirken, çevre sabit değil hale gelir. Markov özelliği  "sonraki devlet sadece mevcut durum ve benim eylemden"  ihlal edilir çünkü sonraki devlet de * diğer* ajanların seçtiği şeye bağlıdır ve politikaları hedefleri hareket ettirir.

> Her çok zeki bir ortamda, diğer zeki birimin bakış açısından, diğer zeki birimin* ortamın* bir parçasıdır. Öğrenirken ve davranışlarını değiştirirken, ortam dengesiz hale gelir.

Bu, tablolar birleştirme kanıtlarını kırar (Q-learning'in garantisi sabit bir ortamı varsayır). Bu da saf derin RL'yi kırar: ajanlar birbirlerini döngülerde kovalar, asla sabit bir politikaya birleştiler. Çoklu ajan özel tekniklerine ihtiyacınız var: merkezi eğitim / merkezi olmayan yürütme, karşı gerçeklik tabanları, lig oyunu, kendiliğinden oyun.

> Bu, standartları bozuyor. Bu, basit bir RL'yi bozuyor. Zeki organların birbirlerine peşken döngüsü, asla sabit bir stratejiye ulaşmıyor.

2026 uygulamaları: robot sürüleri, trafik yönlendirme, otonom araç filosları, piyasa simülatörleri, çoklu ajanlı LLM sistemleri (Fase 16) ve birden fazla akıllı oyunculu olan herhangi bir oyun.

> 2026 yıl uygulaması:机器人集群、交通路由、自动驾驶车队、市场模拟器、多智能体 LLM 系统(16 . aşama), yanı sıra çok sayıda akıllı oyuncu olan herhangi bir oyun.

> **【中文解读】**Çoğu zekiyet RL'nin temel meydan okumaları: Asgariyetsizlik (非平稳性) 其他智能体也在学习) 信用分配 (信用分配) 联合动作空间爆炸、部分可观察性;;

> **【拓展：多智能体→LLM Agent系统】**2026 yılının en popüler MARL uygulaması çok zeki LLM sistemidir: çok büyük model Agent 协作完成复杂任务──Claude Code'un çoklu ajan 模式、AutoGen、CrewAI ve diğer çerçeveleri aslında MARL düşüncesinin dil Agent alanında bir uzantısıdır──

## Konsepten bir şey.

![Four MARL regimes: indep, centralized critic, self-play, league](../assets/marl.svg)

**Formalism: Markov Game.**MDP'nin genelleşmesi: devletler `S`, ortak bir eylemdir.`a = (a_1, …, a_n)`, geçiş`P(s' | s, a)`, ve ajan başına ödüller .`R_i(s, a, s')`Her ajan .`i`Kendi politikası altında kendi getiriyi en üst düzeye çıkarır.`π_i`Eğer ödüller aynı ise, o da aynı.**fully cooperative**Eğer sıfır toplamsa, o da **adversarial**Karışıksa, öyle.**general-sum**- Evet .

> **形式化：马尔可夫博弈。**MDP 的推广: durum`S`、 birleşik hareket `a = (a_1, …, a_n)`、                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            `P(s'|s,a)`、 Her akıllı bedenin ödülü `R_i` Eğer ödül aynı ise,**全合作**Eğer ≠ ≠**对抗** If mixed, yes**一般和**- Evet.

**Core challenges:**

- **Non-stationarity.** `P(s' | s, a_i)`Ajanın .`i`Görüşün değişeceğine .`π_{-i}`, değişen bir durum.
  **非平稳性。**Zekilikten`i`Bu, diğer akıllı bedenlerin değişen stratejilerine bağlıdır.
- **Credit assignment.**Paylaşılan bir ödülle, hangi ajanın nedeni buydu?
  **信用分配。**Paylaşım ödüllerinde hangi akıllı vücut sonuç verdi?
- **Exploration coordination.**Ajanlar, aynı durumu gereksiz yere araştırmak yerine, tamamlayıcı stratejileri keşfetmelidir.
  **探索协调。**Zekilik, birbirini tamamlama stratejisini keşfetmekle aynı durumu keşfetmekle kalmaz.
- **Scalability.**Ortak eylem alanı `n`- Evet .
  **可扩展性。**联合动作空间随 `n`İndeks artışı.
- **Partial observability.**Her ajan sadece kendi gözlemini görür; küresel durum gizlidir.
  **部分可观察性。**Her akıllı insan sadece kendi gözlemlerini görür; bütün dünya durumu gizlenir.

**Four dominant regimes:**

> **四种主导范式：**

**1. Independent Q-learning / independent PPO (IQL, IPPO).**Her ajan kendi Q veya politikasını öğrenir, diğerlerini çevrenin bir parçası olarak görüyor. Basit, bazen işe yarıyor (özellikle deneyim tekrarlamasıyla akıcı bir ajan modeli hilesi olarak hareket eder).

> **1. 独立 Q-learning / 独立 PPO。**Her akıllı vücut kendi Q veya stratejisini öğrenir, diğer akıllı vücutları çevrenin bir parçası olarak görür.

**2. Centralized training, decentralized execution (CTDE).**Modern paradigmaların en yaygını.`π_i`Yerel gözlem koşulları `o_i` standard merkezi olmayan uygulamalar dağıtım sırasında.`Q(s, a_1, …, a_n)`Dünya durumu ve ortak eylem konusunda koşullar.
- **MADDPG**(Lowe et al. 2017): DDPG, her ajan için merkezi bir eleştirmen ile.
- **COMA**(Foerster et al. 2017): karşı gerçekli bir başlangıç  sor "Eğer harekete geçseydim ödülüm ne olurdu `a'`Bunun yerine?"  katkılarımı bir kenara ayırır.
- **MAPPO**- Ne ?**IPPO**ortak eleştirmenle (Yu et al. 2022): Merkezi bir değer fonksiyonu olan PPO. 2026 yılında kooperatif MARL için baskın.
- **QMIX**(Rashid et al. 2018): değer parçalanması  `Q_tot(s, a) = f(Q_1(s, a_1), …, Q_n(s, a_n))`- Tek kelimeyle karıştır.

> **2. 集中训练，分布执行（CTDE）。**En yaygın modern paradigma. Her akıllı bedenin kendi stratejisi vardır.

**3. Self-play.**Aynı ajanın iki kopyası birbirini oynar. Rahatsız eden politika * geçmiş bir anlık fotoğrafımdan benim politikamdır. AlphaGo / AlphaZero / MuZero. OpenAI Beş.

> **3. 自我博弈。**Aynı akıllı bedenin iki kopyası karşı karşı yöntemi* benim geçmişimdeki hızlı resimde olan yöntemiymiş.

**4. League play.**Self-play'ın genel toplam / karşıma ortamlara genişletilmesi: geçmiş ve mevcut politikaların bir nüfusunu tutun, ligten bir rakibi örnekleyin, onlara karşı eğitiniz. İstifadeleri (sağlam en iyiyi yenmek için uzmanlaşmış) ve ana sömürücüleri (sömürücüleri yenmek için uzmanlaşmış) ekler. AlphaStar (StarCraft II).

> **4. 联盟训练。**Kendiliğinden genişleme: geçmişi ve mevcut stratejileri, birliğin içinden örnekler, el karşısında tutmak.

**Communication.**Ajanların öğrenilmiş mesajlar göndermesine izin verin .`m_i`Foerster et al. (2016) farklılaştırılabilir ajanlar arası iletişimin sonundan sona kadar eğitilebileceğini gösterdi. Bugünün LLM tabanlı çoklu ajan sistemleri (Fase 16) esasen doğal dilde iletişim kurar.

> **通信。**允许智能体相互发送学习的消息――在合作环境中有效―― bugünün LLM 多智能体系统本质上使用自然语言通信――

## Yapın.
```figure
f3-marl-orbit
```

## Yapın

Bu ders, iki işbirlikçi ajanla birlikte 6×6 GridWorld kullanır.`-1`Bir ajan hareket ederken,`+10`İkisi de geldiğinde.`code/main.py`- Evet .

> Bu ders 6×6 GridWorld ve iki ortak akıllı vücut kullanıyor. Onlar karşı köşeden çıkıyor, ortak hedefe ulaşmak zorundadır.

### Adım 1: Çoklu ajan ortamı

```python
class CoopGridWorld:
    def __init__(self):
        self.size = 6
        self.goal = (5, 5)

    def reset(self):
        return ((0, 0), (5, 0))  # two agents

    def step(self, state, actions):
        a1, a2 = state
        new1 = move(a1, actions[0])
        new2 = move(a2, actions[1])
        done = (new1 == self.goal) and (new2 == self.goal)
        reward = 10.0 if done else -1.0
        return (new1, new2), reward, done
```

* ortak * eylem alanı `|A|² = 16`Küresel durum iki pozisyondur.

> * Birleşmiş * hareketli alanı `|A|² = 16`Bütün bölge iki yerden oluşuyor.

### Adım 2: Bağımsız Q öğrenimi

Her ajan ortak durumdaki kendi Q-tablosunu çalıştırır. Her adımda: ikisinin de ε-cinsel eylemleri seçmesi, ortak geçiş toplaması, her biri kendi Q'sini paylaşılan ödülle güncelleştirir.

```python
def independent_q(env, episodes, alpha, gamma, epsilon):
    Q1, Q2 = defaultdict(default_q), defaultdict(default_q)
    for _ in range(episodes):
        s = env.reset()
        while not done:
            a1 = epsilon_greedy(Q1, s, epsilon)
            a2 = epsilon_greedy(Q2, s, epsilon)
            s_next, r, done = env.step(s, (a1, a2))
            target1 = r + gamma * max(Q1[s_next].values())
            target2 = r + gamma * max(Q2[s_next].values())
            Q1[s][a1] += alpha * (target1 - Q1[s][a1])
            Q2[s][a2] += alpha * (target2 - Q2[s][a2])
            s = s_next
```

Bu görevde çalışır çünkü ödüller yoğun ve uyumludur. Yakından ilişkili görevlerde başarısız olur (örneğin bir ajanın diğerini * beklemelidir).

> Bu görevde etkili, çünkü ödül yoğun ve karşı karşıya.

### Adım 3: Çürütülen değer güncelleme ile merkezi Q

Birlikte yapılan eylemlere bir Q kullanın `Q(s, a_1, a_2)`. Paylaşılan ödülden güncelleme.`π_i(s) = argmax_{a_i} max_{a_{-i}} Q(s, a_1, a_2)`* Doğru* küresel görüş için eksponensel ortak eylem alanı ticaret.

> Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uygulama: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: Uzo: U

### Adım 4: Basit kendi oyun (adversarial 2-agent)

Aynı ajan, iki rol.`K`A'nın ağırlıklarını B'ye kopyalayıp simetrik eğitim, sürekli ilerleme.

> Aynı akıllı vücut, iki rol.`K`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △

## Tuzaklar

- **Non-stationary replay.**Bağımsız ajanlarla deneyime tekrar yapmak tek ajanla oynayanlardan daha kötüdür çünkü eski geçişler artık eskileri tarafından oluşturuldu.
  **非平稳回放。**独立智能体的体验回放, 独立智能体的体验回放, 独立智能体的体验回放, 独立智能体的体验回放, 独立智能体的体验回放, 独立智能体的体验回放, 独立智能体的体验回放, 独立智能体的体验回放, 独立智能体的体验回放, 独立智能体的体验回放, 独立智能体的体验回放, 独立智能体的体验回放, 独立智能体的体验回放, 独立智能体的体体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立智能体回放, 独立回放, 独立智能体回放, 独立回放, 独立的回放, 独立的回放, 独立的回放, 独立的回放, 独立的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回放, 旧的回回放, 旧的回回放, 旧的回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回回
- **Credit assignment ambiguity.**Uzun bir bölümden sonra paylaşılan ödül; hangi ajanın katkıda bulunduğunu belirlemek için kesin bir yol yok.
  **信用分配模糊。**长回合后的共享奖励; hangi akıllı vücutların ne katkıda bulunduğunu belirleyemez.
- **Policy drift / chasing.**Her ajanın en iyi tepkisi diğerlerinin güncellemesiyle değişir.
  **策略漂移/追逐。**Her akıllı bedenin en iyi tepkisi diğer akıllı bedenlerin yenilemesi ve değişimiyle birlikte olacaktır.
- **Reward hacking via coordination.**Agentler tasarımcı tarafından öngörülmemiş koordine edilmiş başarılar bulurlar. Satış ajanları sıfır tekliflere doğru birleştiler.
  **协调奖励黑客。**智能体发现设计者未预期的协调漏洞──修复:仔细的奖励设计、行为约束──
- **Exploration redundancy.**Her iki ajan da aynı durum aksiyon çiftlerini araştırıyor.
  **探索冗余。**两个智能体探索相同状态-动作对──修复: 两个智能体探索相同状态-动作对──
- **League cycles.**Temiz kendi oyunları bir dominanç döngüsünde sıkışır.
  **联盟循环。**純自我博可能陷入支配循环──修复:多样化对手的联盟训练──
- **Sample explosion.** `n`Ajanlar × devlet alanı × ortak eylemler. Fonksiyon yakınlaması ile yaklaşır; faktörlü eylem alanları (her ajan için bir politika çıkış başı).
  **样本爆炸。**n 个智能体 × 状态空间 × 联合动作──用函数近似解决;因子化动作空间──

## Çerçeveyi kullanın.

2026 MARL başvuru haritası:

> 2026 yıl MARL 应用地图:

| Domain | Method | Notes |
|--------|--------|-------|
| Domain / 领域 | Method / 方法 | Notes / 备注 |
| Cooperative navigation / manipulation / 合作导航/操作 | MAPPO / QMIX | CTDE; shared critic + decentralized actors. / CTDE；共享 Critic + 分布式 Actor。 |
| Two-player games (chess, Go, poker) / 双人游戏 | Self-play with MCTS (AlphaZero) | Zero-sum; symmetric training. / 零和；对称训练。 |
| Complex multiplayer (Dota, StarCraft) / 复杂多人游戏 | League play + imitation pretraining | OpenAI Five, AlphaStar. |
| Autonomous-vehicle fleets / 自动驾驶车队 | CTDE MAPPO / PPO with attention | Partial obs; variable team sizes. / 部分可观察；可变团队大小。 |
| Auction markets / 拍卖市场 | Game-theoretic equilibrium + RL | Mean-field RL when `n` → ∞. / n→∞ 时用平均场 RL。 |
| LLM multi-agent systems (Phase 16) / LLM 多智能体系统 | Natural-language comm + role conditioning | RL loop at the agent-planning layer. / Agent 规划层的 RL 循环。 |

MARL'nin 2026 yılında en büyük büyüme alanı LLM tabanlı: dil modelleri ajanlarının sürüleri pazarlık, tartışma, yazılım oluşturma.

> 2026 MARL'nin en büyük büyüme alanı, LLM'nin: Language Model Smart Body Group discuss, debate, build software, ve RL'nin ortaya çıkması, belirtilmiş değil, *轨迹级* çıkış tercihleri optimize edilmesidir.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-marl-architect.md`- ...

```markdown
---
name: marl-architect
description: Pick the right multi-agent RL regime (IPPO, CTDE, self-play, league) for a given task.
version: 1.0.0
phase: 9
lesson: 10
tags: [rl, multi-agent, marl, self-play]
---

Given a task with `n` agents, output:

1. Regime classification. Cooperative / adversarial / general-sum. Justify.
2. Algorithm. IPPO / MAPPO / QMIX / self-play / league. Reason tied to coupling tightness and reward structure.
3. Information access. Centralized training (what global info goes to the critic)? Decentralized execution?
4. Credit assignment. Counterfactual baseline, value decomposition, or reward shaping.
5. Exploration plan. Per-agent entropy, population-based training, or league.

Refuse independent Q-learning on tightly-coupled cooperative tasks. Refuse to recommend self-play for general-sum with cycle risks. Flag any MARL pipeline without a fixed-opponent eval (cherry-picked self-play numbers are common).
```

## Egzersizler.

1. **Easy.**2. Ajanlı kooperatif GridWorld'de bağımsız Q-öğrenme eğitimi.
2. **Medium.**Bir "koordinasyon" görevi ekleyin: hedef ancak her iki ajan aynı virajda ona adım atınca ulaşılır.
3. **Hard.**MAPPO tarzı eğitim için merkezi bir eleştirmen uygulayın ve koordine görevi için bağımsız PPO ile konverjense hızını karşılaştırın.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Markov game | "Multi-agent MDP" / 马尔可夫博弈 | `(S, A_1, …, A_n, P, R_1, …, R_n)`; each agent has its own reward. |
| CTDE | "Centralized training, decentralized execution" / 集中训练分布执行 | Joint critic at training time; each agent's policy uses only local obs. |
| IPPO | "Independent PPO" / 独立 PPO | Each agent runs PPO separately. Simple baseline; often underrated. |
| MAPPO | "Multi-agent PPO" / 多智能体 PPO | PPO with a centralized value function conditioned on global state. |
| QMIX | "Monotonic value decomposition" / 单调值分解 | `Q_tot = f_monotone(Q_1, …, Q_n)` allows decentralized argmax. |
| COMA | "Counterfactual multi-agent" / 反事实多智能体 | Advantage = my Q minus expected Q marginalizing over my action. |
| Self-play | "Agent vs past self" / 自我博弈 | Single agent, two roles; standard for zero-sum games. |
| League play | "Population training" / 联盟训练 | Cache past policies, sample opponents from the pool; handles strategy cycles. |

## Daha fazla okumak

- [Lowe et al. (2017). Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments (MADDPG)](https://arxiv.org/abs/1706.02275) Merkezli bir eleştirmenle CTDE.
- [Foerster et al. (2017). Counterfactual Multi-Agent Policy Gradients (COMA)](https://arxiv.org/abs/1705.08926) kredi tahsisine karşı gerçeklik bazları.
- [Rashid et al. (2018). QMIX: Monotonic Value Function Factorisation](https://arxiv.org/abs/1803.11485) değer parçalanması monotonlukla.
- [Yu et al. (2022). The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games (MAPPO)](https://arxiv.org/abs/2103.01955)PPO MARL için şaşırtıcı derecede güçlü.
- [Vinyals et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z) Lig oynamak ölçekte.
- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270) sıfır toplam oyunlarında saf bir oyun.
- [Sutton & Barto (2018). Ch. 15 — Neuroscience & Ch. 17 — Frontiers](http://incompleteideas.net/book/RLbook2020.pdf) ders kitabının çoklu ajan ayarlarının kısa süreli olarak ele alınması ve CTDE'nin çözmesi için tasarlanmış olan istasyonarlık olmayan sorun içerir.
- [Zhang, Yang & Başar (2021). Multi-Agent Reinforcement Learning: A Selective Overview](https://arxiv.org/abs/1911.10635) Kooperatif, rekabetçi ve karışık MARL'yi kapsayan ve dönüşüm sonuçları ile sonuçlanan anket.
