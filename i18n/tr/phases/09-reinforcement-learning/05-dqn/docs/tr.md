# Deep Q-Networks (DQN)

> 2013: Mnih, çiğ pikseli üzerinde bir Q-öğrenme ağı eğitmiş, yedi Atari oyununda her klasik RL ajanını yenmiştir. 2015: 49 oyunlara kadar uzattı, Nature'de yayınlanmıştır, derin-RL çağını tetikledi. DQN, işlev yaklaşımını istikrarlı hale getiren üç numara ile birlikte Q-öğrenme.

> **【中文解读】**DQN = Q-öğrenme + Nörel Ağ + Üç stabilize teknikleri (s) ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞      ∞ ∞ ∞ 

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 04 (Q-learning, SARSA) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 04 (Q-learning, SARSA)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Tablolar Q öğrenme, her çift için ayrı bir Q değere ihtiyaç duyar. Bir satranç tahtasında ~1043 devlet vardır. Atari çerçevesinin 210 × 160 × 3 = 100,800 özellik vardır. Tablolar RL binlerce devlette ölür, milyarlarca bile olmaz.

> Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çiz

Çözüm, geriye bakıldığında açık: Q-tabloyu nöral ağla değiştirin.`Q(s, a; θ)`Ancak açık-görünen geriye bakış on yıllar sürdü. Saçma fonksiyon yaklaşımı ve Q öğrenimi "ölümlü üçlü"  fonksiyon yaklaşımı + başlangıç + politika dışı öğrenme altında ayrılır. Mnih et al. (2013, 2015) öğrenmeyi istikrarlandıran üç mühendislik hilesi tanımladı:

> İşlerin çözümü çok basit: sinir ağı kullanmak.`Q(s, a; θ)`√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√

1. **Experience replay**Decorrelates geçişler.
   **经验回放**打破转移的时间相关性──
2. **Target network**Başlangıç hedefini dondururur.
   **目标网络**结自举目标──
3. **Reward clipping**- Bu, gradient büyüleri normalleştirir.
   **奖励裁剪**归一化梯度级――

Atari'deki DQN, tek bir hiperparametre seti ile tek bir mimarinin ilk kez çiğ piksellerden düzinelerce kontrol sorunu çözmesiydi. DDQN, Rainbow, Dueling, Distributional, R2D2, Agent57 'den sonra inşa edilen her şey bu üç numara tabanının üzerine yığılmıştı.

> Atari'nin DQN'i ilk kez tek bir yapı ve tek bir süper parametre kümesi ile orijinal bir görüntüden onlarca kontrol sorunu çözüldü.

> **【中文解读】**"Fatal Three Elements": Fonktion近似 + 自举 + 离策略 → 训练不稳定甚至发散──DQN'in üç tekniği bu sorunu çözdü: 1) deney geri dönüşü ve zaman kırma ilişkisi; 2) 目标网络结自举目标; 3) 奖励裁剪归一化梯度──所有后续深度 RL 算法都建立在这些三技巧之上──

> **【拓展：经验回放→RLHF】**经验回放 (Experience Replay) düşüncesi LLM 训练中无处不在:PPO 训练时的缓冲、RLHF 内的偏好数据集、DPO 离线数据本质上都是"打破数据相关性、反复利用经验"

## Konsepten bir şey.

![DQN training loop: env, replay buffer, online net, target net, Bellman TD loss](../assets/dqn.svg)

**The objective.**DQN, sinirsel bir Q fonksiyonunda tek adımlı TD kaybını en aza indirgerir:

`L(θ) = E_{(s,a,r,s')~D} [ (r + γ max_{a'} Q(s', a'; θ^-) - Q(s, a; θ))² ]`

`θ`= çevrimiçi ağ, her adım gradient düşüşe göre güncellenir. `θ^-`= hedef ağ, düzenli olarak kopyalanır `θ`(Her ~ 10.000 adım).`D`= geçmiş geçişlerin yeniden oynatma tamponu.

> **目标。**DQN en küçük sinir Q  işlevi üzerinde tek adım TD  kaybı`θ`= 在线网络,每步通过梯度下降更新──`θ^-`= 目标网络,定期从 `θ`复制(約每 10,000 步)`D`= 过去转移的回放缓冲区──

**The three tricks, in order of importance:**

> **三个技巧，按重要性排序：**

**Experience replay.**Bir yüzük tamponu .`~10⁶`Bu, zamansal ilişkiyi kırar (sükseces çerçeveler neredeyse aynıdır), ağın nadir ödüllendirici geçişlerden birçok kez öğrenmesine izin verir ve ardıcıl gradient güncellemelerini dekorele eder.

> **经验回放。**Bir yaklaşık 106 kez dönüşümlü bir çevrelik buzağı bölgesi vardır. Her bir eğitim adımı küçük bir grup olarak düzenli olarak gerçekleşir. Bu da zaman ilişkisini kırar.

**Target network.**Aynı ağı kullanıyor `Q(·; θ)`Bellman denkleminin her iki tarafında hedef her güncelleme hareket eder  "kendin kuyruk peşinde".`Q(·; θ^-)`Dondurulmuş ağırlıklarla.`C`Adımlar, kopya `θ → θ^-`Bu, gerileme hedefini bir seferde binlerce gradient adımları için istikrarlı hale getirir.`θ^- ← τ θ + (1-τ) θ^-`(DDPG, SAC'da kullanılır) daha düzgün bir variandır.

> **目标网络。**Bellman denkleminin iki tarafında aynı ağ kullanılarak hedefler her güncelleştirilmek için hareket eder.`C`步复制 `θ → θ^-`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊                                                                                                                                                                                                                                                                

**Reward clipping.**Atari ödül büyüklükleri 1 ila 1000 + arasında değişir.`{-1, 0, +1}`Ödül büyüklüğü önemli olduğunda yanlış, sadece imza önemli olduğunda Atari için iyi.

> **奖励裁剪。**Atari  Ödül oranı 1 ila 1000+ arasında                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 `{-1, 0, +1}` herhangi bir oyun yönetimi seviyesini önlemek.

**Double DQN.**Hasselt (2016) maksimum önyargıyı düzeltir: eylem * seçmek için çevrimiçi ağ kullanın, hedef ağ * değerlendirmek için.

`target = r + γ Q(s', argmax_{a'} Q(s', a'; θ); θ^-)`

Değiştirme, sürekli daha iyi.

> **双重 DQN。**Hasselt (2016) 修复最大化偏差:用在线网络*选择*动作,用目标网络*评估*它──直接替换,始终更好──默认使用──

**Other improvements (Rainbow, 2017):**öncelikli tekrarlama (öntem yüksek TD hata geçişleri daha fazla), düello mimarisi (ayrı `V(s)`ve avantaj başları), gürültülü ağlar (öğrenmiş keşif), n-adım geri dönüşü, dağılımlı Q (C51/QR-DQN), çok adımlı başlangıç. Her biri birkaç yüzde ekler; kazançlar yaklaşık olarak eklenir.

> **其他改进（Rainbow, 2017）：**优先回放、决斗架构、噪声网络、n 步回报、分布式 Q、多步自举── her gelişme katkı birkaç yüz puan;收益大致可叠加──

> **【拓展：Rainbow DQN 与集成改进】**Rainbow DQN(2017) 6 çeşit DQN  geliştirme birleştirilmiştir: öncelikli deneyim    Dueling  yapı                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

## Yapın.
```figure
f3-dqn-stability
```

## Yapın

Burada kod sadece stdlib-numpy-free. küçük bir sürekli GridWorld'de elle yuvarlanan tek katmanlı MLP kullanıyoruz, bu yüzden her eğitim adımı mikrosekonda çalışır. Algoritm Atari DQN'e eşit ölçekte.

> Bu kod sadece standart kütüphanede kullanılır. GridWorld'da kullanılan tek gizli katman MLP'de kullanılır.

### Adım 1: Yeniden oynatma tamponu

```python
class ReplayBuffer:
    def __init__(self, capacity):
        self.buf = []
        self.capacity = capacity
    def push(self, s, a, r, s_next, done):
        if len(self.buf) == self.capacity:
            self.buf.pop(0)
        self.buf.append((s, a, r, s_next, done))
    def sample(self, batch, rng):
        return rng.sample(self.buf, batch)
```

~ Atari için 50.000 kapasite; bizim oyuncak ortamımız için 5.000 yeter.

> Atari'nin yaklaşık 50.000 kapasiteye ihtiyacı var. Oyuncaklarımız için 5.000 yeter.

### Adım 2: Küçük bir Q-ağı (elçi MLP)

```python
class QNet:
    def __init__(self, n_in, n_hidden, n_actions, rng):
        self.W1 = [[rng.gauss(0, 0.3) for _ in range(n_in)] for _ in range(n_hidden)]
        self.b1 = [0.0] * n_hidden
        self.W2 = [[rng.gauss(0, 0.3) for _ in range(n_hidden)] for _ in range(n_actions)]
        self.b2 = [0.0] * n_actions
    def forward(self, x):
        h = [max(0.0, sum(w * xi for w, xi in zip(row, x)) + b) for row, b in zip(self.W1, self.b1)]
        q = [sum(w * hi for w, hi in zip(row, h)) + b for row, b in zip(self.W2, self.b2)]
        return q, h
```

Ön geçit: doğrusal → ReLU → doğrusal.

> Önceki yazı: 线性 → ReLU → 线性──

### Adım 3: DQN güncelleme

```python
def train_step(online, target, batch, gamma, lr):
    grads = zeros_like(online)
    for s, a, r, s_next, done in batch:
        q, h = online.forward(s)
        if done:
            y = r
        else:
            q_next, _ = target.forward(s_next)
            y = r + gamma * max(q_next)
        td_error = q[a] - y
        accumulate_grads(grads, online, s, h, a, td_error)
    apply_sgd(online, grads, lr / len(batch))
```

Şekil, iki farklılık ile Ders 04'ten Q-öğrenme şeklidir: (a) farklılıklara sahip bir `Q(·; θ)`Bir tabloyu indeksilemek yerine, (b) hedef kullanımı `Q(·; θ^-)`- Evet .

> 形式与课04的Q-learning相似,但有两区别:`Q(·; θ)`Etkinlik ve gelişme için kullanılan yöntemler`Q(·; θ^-)`- Evet.

### Dördüncü adım: Dış döngü

Her bölümde, `Q(·; θ)`, tampona geçişleri itmek, minibatch örneğini almak, bir gradient adımını atmak, zaman zaman senkronize etmek`θ^- ← θ`- Şablon:

```python
for episode in range(N):
    s = env.reset()
    while not done:
        a = epsilon_greedy(online, s, epsilon)
        s_next, r, done = env.step(s, a)
        buffer.push(s, a, r, s_next, done)
        if len(buffer) >= batch:
            train_step(online, target, buffer.sample(batch), gamma, lr)
        if steps % sync_every == 0:
            target = copy(online)
        s = s_next
```

16 boyutlu bir sıcaktan ibaret küçük GridWorld'da, ajan yaklaşık 500 bölümde en iyi politika öğrenir. Atari'de bunu 200M çerçeveye kadar ölçeklendirin ve CNN özellikleri çıkarıcısı ekleyin.

> 16 boyutlı bir ısılı  durumu kullanırken, akıllı beden yaklaşık 500 kez en iyi stratejiyi öğrendi. Atari'de, 2 milyar dolarlık bir program oluşturdu ve CNN özellik çekicisi ekledi.

## Tuzaklar

- **Deadly triad.**Fonksiyon yaklaşımı + politika dışı + başlangıç kaydetimi farklı olabilir. DQN hedefi ağ + tekrar ile hafifletiyor; ikisini de kaldırmayın.
  **致命三要素。**函数近似+离策略+自举可能发散──DQN 通过目标网络+回放缓解; do not remove any one──
- **Exploration.**E-net, genellikle ilk %10 eğitim sırasında 1.0 ila 0.01 arasında bozulmalıdır.
  **探索。**E. ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞
- **Overestimation.** `max`Sesli Q'dan yukarı tarafsızdır.
  **过估计。**Sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesli bir sesliğidir.`max`Üst tarafa bağlılık. Üretim sırasında iki ağırlıklı DQN kullanımı sona erdi.
- **Reward scale.**Ödülleri kes veya normalleştir; gradient büyüklüğü ödül büyüklüğüne orantılıdır.
  **奖励尺度。**剪或归归化奖励; 梯度量级与奖励量级正比.
- **Replay buffer coldstart.**Buffer birkaç bin geçiş yapana kadar antrenman yapmayın.
  **回放缓冲区冷启动。**缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓冲区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 缓区 区 缓区 缓区 缓区 区 区 缓区 区 缓区 缓区 区 区 区 区 区 缓区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 区 
- **Target sync frequency.**Çok sık ≈ hedef ağı yok; çok nadir ≈ eskileri hedefler. Atari DQN 10.000 env adımları kullanır.
  **目标同步频率。**太频繁≈没有目标网络;太不频繁≈过时目标──体验法则: 每约1/100 训练视野同步一次──
- **Observation preprocessing.**Atari DQN, Markov durumu oluşturmak için 4 çerçeve yığar.
  **观测预处理。**Atari DQN 堆叠 4 使状态满足马尔可性──任何有速度信息的环境都需要堆叠或循环状态──

## Çerçeveyi kullanın.

2026 yılında DQN nadiren en son teknolojiye sahip ancak politika dışı referans algoritması olarak kalır:

> 2026 yılında, DQN  çok az gelişmiş, ama hala stratejik algoritma referans:

| Task | Method of choice | Why not DQN? |
|------|------------------|--------------|
| Task / 任务 | Method of choice / 首选方法 | Why not DQN? / 为什么不用 DQN？ |
| Discrete-action Atari-like / 离散动作类 Atari | Rainbow DQN or Muesli | Same framework, more tricks. / 相同框架，更多技巧。 |
| Continuous control / 连续控制 | SAC / TD3 (Phase 9 · 07) | DQN has no policy network. / DQN 没有策略网络。 |
| On-policy / high-throughput / 在线策略/高吞吐 | PPO (Phase 9 · 08) | No replay buffer; easier to scale. / 无回放缓冲区；更易扩展。 |
| Offline RL / 离线 RL | CQL / IQL / Decision Transformer | Conservative Q targets, no bootstrapping blowups. / 保守 Q 目标，无自举爆炸。 |
| Large discrete action spaces (recommender) / 大离散动作空间（推荐） | DQN with action embedding, or IMPALA | Fine; decoration matters. / 可行；细节很重要。 |
| LLM RL / LLM RL | PPO / GRPO | Sequence-level, not step-level; different loss. / 序列级而非步级；不同损失。 |

SAC, TD3, DDPG, SAC-X, AlphaZero'nun kendi kendine oynatma tamponu ve her çevrimdışı RL yöntemi boyunca tekrar oynatma ve hedef ağlar görünür. Ödüllü kesim PPO'da avantaj normallaşması olarak yaşar. Mimarlık bir tasarımdır.

> Bu deneyler hala geçerlidir. SAC, TD3, DDPG, SAC-X, AlphaZero'nun kendi kendini geliştirme alanı ve her bir çevrimiçi RL yöntemi.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-dqn-trainer.md`- ...

```markdown
---
name: dqn-trainer
description: Produce a DQN training config (buffer, target sync, ε schedule, reward clipping) for a discrete-action RL task.
version: 1.0.0
phase: 9
lesson: 5
tags: [rl, dqn, deep-rl]
---

Given a discrete-action environment (observation shape, action count, horizon, reward scale), output:

1. Network. Architecture (MLP / CNN / Transformer), feature dim, depth.
2. Replay buffer. Capacity, minibatch size, warmup size.
3. Target network. Sync strategy (hard every C steps or soft τ).
4. Exploration. ε start / end / schedule length.
5. Loss. Huber vs MSE, gradient clip value, reward clipping rule.
6. Double DQN. On by default unless explicit reason to disable.

Refuse to ship a DQN with no target network, no replay buffer, or ε held at 1. Refuse continuous-action tasks (route to SAC / TD3). Flag any reward range > 10× per-step mean as needing clipping or scale normalization.
```

## Egzersizler.

1. **Easy.**Çık .`code/main.py`-Episod başına geri dönüş eğriyi çiz.
2. **Medium.**Hedef ağını devre dışı bırakın (Bellman hedefinin her iki tarafı için çevrimiçi ağ kullanın).
3. **Hard.**Çift DQN ekle: seçmek için çevrimiçi ağ kullan `argmax a'`, hedef ağ değerlendirmek için.`Q(s_0, best_a)`Gerçek karşısında`V*(s_0)`1000 bölümden sonra gürültülü bir ödül GridWorld'da Double DQN'de karşı karşıya kalmadı.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| DQN | "Deep Q-learning" / 深度Q网络 | Q-learning with a neural Q-function, replay buffer, and target network. |
| Experience replay | "Shuffled transitions" / 经验回放 | Ring buffer sampled uniformly each gradient step; decorrelates data. |
| Target network | "Frozen bootstrap" / 目标网络 | Periodic copy of Q used in the Bellman target; stabilizes training. |
| Deadly triad | "Why RL diverges" / 致命三要素 | Function approximation + bootstrapping + off-policy = no convergence guarantee. |
| Double DQN | "Fix for maximization bias" / 双重DQN | Online net selects action, target net evaluates it. |
| Dueling DQN | "V and A heads" / 决斗DQN | Decompose Q = V + A - mean(A); same output, better gradient flow. |
| Rainbow | "All the tricks" / Rainbow | DDQN + PER + dueling + n-step + noisy + distributional in one. |
| PER | "Prioritized Replay" / 优先经验回放 | Sample transitions proportional to TD-error magnitude. |

## Daha fazla okumak

- [Mnih et al. (2013). Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602) Derin RL'ye başlayan 2013 NeurIPS atölyesi makalesi.
- [Mnih et al. (2015). Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236) Nature gazetesi, 49 oyun DQN.
- [Hasselt, Guez, Silver (2016). Deep Reinforcement Learning with Double Q-learning](https://arxiv.org/abs/1509.06461) DDQN.
- [Wang et al. (2016). Dueling Network Architectures](https://arxiv.org/abs/1511.06581)DQN'de dövüş.
- [Hessel et al. (2018). Rainbow: Combining Improvements in Deep RL](https://arxiv.org/abs/1710.02298)- Yapacakları kağıt.
- [OpenAI Spinning Up — DQN](https://spinningup.openai.com/en/latest/algorithms/dqn.html) Modern açıklama.
- [Sutton & Barto (2018). Ch. 9 — On-policy Prediction with Approximation](http://incompleteideas.net/book/RLbook2020.pdf) DQN'nin hedef ağının ve tekrarlama tamponu tarafından kontrol altına alınması için tasarlanmış olan "ölümlü üçlü" (fonksiyon yaklaşımı + başlatma + politika dışı) ders kitabı tedavisi.
- [CleanRL DQN implementation](https://docs.cleanrl.dev/rl-algorithms/dqn/) Ablation çalışmalarında kullanılan tek dosya DQN referansı; bu dersin sıfırdan versiyonu ile birlikte okumak iyi.
