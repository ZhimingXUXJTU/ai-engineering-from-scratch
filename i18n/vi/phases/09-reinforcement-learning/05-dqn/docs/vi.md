# Deep Q-Networks (DQN)

> 2013: Mnih đào tạo một mạng học Q trên các pixel nguyên liệu, đánh bại mọi đại lý RL cổ điển trên bảy trò chơi Atari. 2015: mở rộng đến 49 trò chơi, được xuất bản trên Nature, đã kích hoạt thời đại RL sâu. DQN là học Q cộng với ba thủ thuật làm cho việc gần gũi chức năng ổn định.

> **【中文解读】**DQN = Q-learning + 神经网络 + 三个稳定化技巧 (Thử nghiệm tái放、目标网络、奖励剪裁) ⋅2013-2015 năm tại Atari 游戏击败 tất cả các phương pháp RL cổ điển, mở ra thời đại RL sâu.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 04 (Q-learning, SARSA) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 04 (Q-learning, SARSA)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Tablar Q-learning cần một giá trị Q riêng biệt cho mỗi cặp (thế độ, hành động). Một bảng cờ vua có ~1043 trạng thái. Một khung Atari là 210 × 160 × 3 = 100,800 tính năng. Tablar RL chết ở hàng ngàn trạng thái, chưa kể hàng tỷ.

> 表格 Q-learning 需要为每一个状态,动作) đối với một trạng thái riêng lẻ một giá trị Q. Một bàn cờ có khoảng 1043 trạng thái. Một Atari có 210×160×3 = 100,800 个特征. 表格 RL trong hàng ngàn trạng thái đã bị mất hiệu lực, không cần phải nói là hàng tỷ.

Sự khắc phục rõ ràng khi nhìn lại: thay thế bảng Q bằng một mạng lưới thần kinh,`Q(s, a; θ)`Nhưng việc gần gũi với hàm tính ngây thơ với việc học Q khác nhau dưới "triad chết người"  gần gũi với hàm tính + khởi động + học ngoài chính sách. Mnih et al. (2013, 2015) xác định ba thủ thuật kỹ thuật ổn định học tập:

> Việc sau đây giải pháp rất đơn giản: sử dụng mạng thần kinh.`Q(s, a; θ)`替换 Q 表――但这个"简单"花了几十年――简单的函数近似与Q-learning 在"致命三要素"下会发散函数近似 +自举 + 离策略学习――Mnih 等人(2013、2015) xác định ba kỹ thuật của việc học ổn định:

1. **Experience replay**decorreates chuyển đổi.
   **经验回放**打破转移的时间相关性.
2. **Target network**làm đông lạnh mục tiêu khởi động.
   **目标网络**结自举目标──
3. **Reward clipping**làm bình thường hóa độ vĩ đại gradient.
   **奖励裁剪**归一化梯度级级――

DQN trên Atari là lần đầu tiên một kiến trúc duy nhất với một bộ siêu tham số duy nhất giải quyết hàng chục vấn đề điều khiển từ các pixel thô. Mọi thứ "độ-RL" được xây dựng kể từ DDQN, Rainbow, Dueling, phân phối, R2D2, Agent57  được xếp chồng lên trên đỉnh của cơ sở ba trò chơi này.

> DQN trên Atari là lần đầu tiên sử dụng một cấu trúc đơn và một siêu số liệu tập hợp từ các mô hình gốc để giải quyết hàng chục vấn đề kiểm soát.

> **【中文解读】**"Thứ ba yếu tố chết người": hàm gần như + tự nâng + 离策略 → 训练不稳定甚至发散──DQN có ba kỹ thuật giải quyết vấn đề này: 1) kinh nghiệm quay lại và phá vỡ thời gian liên quan; 2) 目标网络结结自举目标; 3) 奖励 cắt giảm chuyển đổi 梯度──所有后续深度 RL 算法 đều dựa trên ba kỹ thuật này──

> **【拓展：经验回放→RLHF】**经验回放 (Experience Replay) là một ý tưởng không tồn tại trong các khóa đào tạo LLM: PPO  Buffer trong quá trình đào tạo RLHF DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET DATABET

## Khái niệm cốt lõi

![DQN training loop: env, replay buffer, online net, target net, Bellman TD loss](../assets/dqn.svg)

**The objective.**DQN giảm thiểu sự mất TD một bước trên chức năng Q thần kinh:

`L(θ) = E_{(s,a,r,s')~D} [ (r + γ max_{a'} Q(s', a'; θ^-) - Q(s, a; θ))² ]`

`θ`= mạng trực tuyến, cập nhật từng bước theo độ giảm gradient. `θ^-`= mạng mục tiêu, thường xuyên sao chép từ `θ`(mỗi ~ 10.000 bước). `D`= Buffer play của quá trình chuyển đổi trước đây.

> **目标。**DQN tối thiểu hóa thần kinh Q  hàm đơn bước TD  mất tích`θ`= 在线网络, từng bước qua thang độ xuống cập nhật.`θ^-`= 目标网络, thường xuyên từ `θ`复制(约每10,000 步)`D`= 过去转移的回放缓冲区──

**The three tricks, in order of importance:**

> **三个技巧，按重要性排序：**

**Experience replay.**Một bộ đệm vòng của `~10⁶`mỗi bước đào tạo lấy mẫu một bộ nhỏ một cách ngẫu nhiên. Điều này phá vỡ mối tương quan thời gian (chốt khung liên tiếp gần như giống nhau), cho phép mạng học hỏi từ những chuyển đổi rác mẻ nhiều lần, và gỡ liên tục cập nhật gradient.

> **经验回放。**Một vòng tròn chuyển động khoảng 106 lần. Mỗi bước tập trung đều được thực hiện theo một số lượng nhỏ.

**Target network.**Sử dụng mạng tương tự `Q(·; θ)`trên cả hai bên của phương trình Bellman làm cho mục tiêu di chuyển mỗi cập nhật  "cách đuôi của riêng bạn".`Q(·; θ^-)`Với trọng lượng đông lạnh.`C`bước, sao chép `θ → θ^-`Điều này ổn định mục tiêu hồi quy cho hàng ngàn bước gradient cùng một lúc.`θ^- ← τ θ + (1-τ) θ^-`(được sử dụng trong DDPG, SAC) là một biến thể mượt mà hơn.

> **目标网络。**Trong phương trình Bellman sử dụng cùng một mạng sẽ làm cho mục tiêu mỗi lần cập nhật đều di chuyển" theo đuổi尾巴 của mình"──修复方法: giữ một quyền重结的第二网络── mỗi `C`步复制 `θ → θ^-`◊软更新(DDPG、SAC 中使用) là biến thể dễ dàng hơn.

**Reward clipping.**Tầm thưởng của Atari dao động từ 1 đến 1000+.`{-1, 0, +1}`sai khi mức độ thưởng quan trọng, tốt cho Atari khi chỉ cần ký kết quan trọng.

> **奖励裁剪。**Atari                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            `{-1, 0, +1}`防止任何单个游戏主导梯度.

**Double DQN.**Hasselt (2016) khắc phục sự thiên vị tối đa hóa: sử dụng mạng trực tuyến để *chọn* hành động, mạng mục tiêu để *chánh giá* nó.

`target = r + γ Q(s', argmax_{a'} Q(s', a'; θ); θ^-)`

Đổi lại, luôn tốt hơn.

> **双重 DQN。**Hasselt (2016) 修复最大化偏差:用在线网络*选择*动作,用目标网络*评估*它──直接替换,始终更好──默认使用──

**Other improvements (Rainbow, 2017):**phát lại ưu tiên (ví dụ chuyển đổi lỗi TD cao hơn), kiến trúc đấu đôi (lỗi `V(s)`và đầu lợi thế), mạng ồn ào (khám phá học tập), n- bước trả về, phân phối Q (C51/QR-DQN), multi- bước khởi động.

> **其他改进（Rainbow, 2017）：**优先回放、决斗架构、噪声网络、n 步回报、分布式 Q、多步自举── mỗi cải tiến đóng góp vài trăm điểm;收益大致可叠加──

> **【拓展：Rainbow DQN 与集成改进】**Rainbow DQN(2017) sẽ tích hợp 6 loại DQN cải tiến cùng nhau: Priority Experience recharge, Dueling, Architcture, Noise Network Exploration, N 步回报, phân tán Q học, nhiều bước tự举举. Mỗi loại cải tiến góp phần tăng hiệu suất vài trăm điểm, kết hợp hiệu quả lên đáng kể.

## Hãy xây dựng nó.
```figure
f3-dqn-stability
```

## Hãy xây dựng nó

Mã ở đây là stdlib-only numpy-free  chúng tôi sử dụng một MLP một lớp ẩn được quét bằng tay trên một GridWorld liên tục nhỏ, vì vậy mỗi bước đào tạo chạy trong microsecond.

> Mã chỉ sử dụng các tiêu chuẩn trong một hệ thống nhỏ trên GridWorld trên sử dụng tay viết của một mảng ẩn MLP.

### Bước 1: Buffer play

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

~ 50.000 dung lượng cho Atari; 5.000 đủ cho môi trường đồ chơi của chúng tôi.

> Atari cần khoảng 50.000 dung lượng; môi trường chơi game của chúng tôi 5.000 đã đủ.

### Bước 2: một mạng Q nhỏ (MLP thủ công)

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

Chuyển đi phía trước: tuyến tính → ReLU → tuyến tính. Đó là toàn bộ lưới.

> 前向传播:线性 → ReLU → 线性──这就是整个网络──

### Bước 3: Cập nhật DQN

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

Hình dạng là Q-làm học từ Bài học 04 với hai khác biệt: (a) chúng ta backprop thông qua một phân biệt `Q(·; θ)`thay vì chỉ mục hóa một bảng, (b) mục tiêu sử dụng `Q(·; θ^-)`- Tôi không biết.

> 形式与课04的Q-学习相似, nhưng có hai sự khác biệt:`Q(·; θ)`反向传播而非索引表格,`Q(·; θ^-)`

### Bước 4: vòng ngoài

Đối với mỗi tập, hãy hành động khiêu dâm.`Q(·; θ)`, đẩy chuyển đổi vào bộ đệm, lấy mẫu một mini batch, thực hiện một bước nghiêng, theo thời gian đồng bộ `θ^- ← θ`- Mẫu:

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

Trên mạng lưới GridWorld nhỏ bé của chúng tôi với trạng thái 16 chiều, đại lý học được một chính sách gần như tối ưu trong khoảng 500 tập.

> Trong khi chúng tôi sử dụng 16 维 một-sự nóng  trạng thái GridWorld, smartbody trong khoảng 500 回合内学到接近最佳策略── trên Atari, mở rộng đến 2 tỷ并添加CNN特征提取器──

## Những bẫy

- **Deadly triad.**Phân tích chức năng + ngoại chính sách + bootstrapping có thể khác nhau. DQN giảm nhẹ với target net + replay; không loại bỏ cả hai.
  **致命三要素。**函数近似+离策略+自举可能发散──DQN 通过目标网络+回放缓解; đừng di chuyển bất kỳ một người nào──
- **Exploration.**ε phải phân hủy, thường từ 1.0 đến 0.01 trong ~ 10% đầu tiên của đào tạo.
  **探索。**ε 必须衰减, thường từ 1.0 đến 0.01, bao gồm khoảng 10% của các bài tập trước.
- **Overestimation.** `max`Over noise Q là thiên hướng lên. luôn sử dụng Double DQN trong sản xuất.
  **过估计。**Đối với tiếng ồn `max`会上偏倚──生产中始终使用双重 DQN──
- **Reward scale.**Clip hoặc bình thường hóa phần thưởng; độ lớn gradient tương xứng với độ lớn phần thưởng.
  **奖励尺度。** cắt giảm hoặc kết hợp phần thưởng; cấp độ và cấp độ phần thưởng được tương đương.
- **Replay buffer coldstart.**Đừng tập luyện cho đến khi bộ đệm có vài ngàn chuyển tiếp.
  **回放缓冲区冷启动。**缓冲区 có vài ngàn lần chuyển tiếp sau khi đào tạo lại.
- **Target sync frequency.**Thường xuyên quá ≈ không có lưới mục tiêu; quá hiếm ≈ mục tiêu lỗi thời. Atari DQN sử dụng 10.000 bước env. Quy tắc ngón tay: đồng bộ hóa mỗi ~1/100 chân trời huấn luyện.
  **目标同步频率。**太频繁≈没有目标网络;太不频繁≈过时目标――经验法则: 每约1/100 训练视野同步一次――
- **Observation preprocessing.**Atari DQN xếp 4 khung để làm cho trạng thái Markov. bất kỳ env với thông tin tốc độ cần khung xếp hoặc trạng thái lặp lại.
  **观测预处理。**Atari DQN 堆叠 4 使 trạng thái đáp ứng khả năng vận hành.

## Hãy sử dụng nó để thực hiện

Năm 2026, DQN hiếm khi là hiện đại nhưng vẫn là thuật toán tham chiếu ngoài chính sách:

> Năm 2026, DQN  ít khi là tiên tiến nhất, nhưng vẫn còn rời khỏi thuật toán chiến lược:

| Task | Method of choice | Why not DQN? |
|------|------------------|--------------|
| Task / 任务 | Method of choice / 首选方法 | Why not DQN? / 为什么不用 DQN？ |
| Discrete-action Atari-like / 离散动作类 Atari | Rainbow DQN or Muesli | Same framework, more tricks. / 相同框架，更多技巧。 |
| Continuous control / 连续控制 | SAC / TD3 (Phase 9 · 07) | DQN has no policy network. / DQN 没有策略网络。 |
| On-policy / high-throughput / 在线策略/高吞吐 | PPO (Phase 9 · 08) | No replay buffer; easier to scale. / 无回放缓冲区；更易扩展。 |
| Offline RL / 离线 RL | CQL / IQL / Decision Transformer | Conservative Q targets, no bootstrapping blowups. / 保守 Q 目标，无自举爆炸。 |
| Large discrete action spaces (recommender) / 大离散动作空间（推荐） | DQN with action embedding, or IMPALA | Fine; decoration matters. / 可行；细节很重要。 |
| LLM RL / LLM RL | PPO / GRPO | Sequence-level, not step-level; different loss. / 序列级而非步级；不同损失。 |

Các bài học vẫn đi lại. Phân hồi và các mạng mục tiêu xuất hiện trong SAC, TD3, DDPG, SAC-X, bộ đệm tự chơi của AlphaZero và mọi phương pháp RL ngoại tuyến.

> Những kinh nghiệm này vẫn còn hiệu quả. Các kết quả của SAC, TD3, DDPG, SAC-X và mỗi phương pháp RL của AlphaZero đã được phát hiện.

## Chuyển nó đi.

Cứ như `outputs/skill-dqn-trainer.md`- Có thể là:

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

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`- Bước quay trở lại mỗi tập. bao nhiêu tập cho đến khi trung bình chạy vượt quá -10?
2. **Medium.**Thiết lập mạng mục tiêu ( Sử dụng mạng trực tuyến cho cả hai bên của mục tiêu Bellman). đo sự bất ổn đào tạo  liệu trả lại dao động hay khác nhau?
3. **Hard.**Thêm DQN TP: sử dụng mạng trực tuyến để chọn `argmax a'`, mục tiêu lưới để đánh giá. So sánh thiên vị của `Q(s_0, best_a)`Vâng đúng `V*(s_0)`Sau 1.000 tập với vs không có Double DQN trên một GridWorld có phần thưởng lớn.

## Từ khóa  Từ khóa nhanh chóng

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

## Xem thêm 延伸阅读

- [Mnih et al. (2013). Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602) bài viết của hội thảo NeurIPS năm 2013 đã bắt đầu RL sâu.
- [Mnih et al. (2015). Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236) báo Nature, 49 game DQN.
- [Hasselt, Guez, Silver (2016). Deep Reinforcement Learning with Double Q-learning](https://arxiv.org/abs/1509.06461) DDQN.
- [Wang et al. (2016). Dueling Network Architectures](https://arxiv.org/abs/1511.06581) Đấu đấu DQN.
- [Hessel et al. (2018). Rainbow: Combining Improvements in Deep RL](https://arxiv.org/abs/1710.02298)- Báo đống thủ thuật.
- [OpenAI Spinning Up — DQN](https://spinningup.openai.com/en/latest/algorithms/dqn.html) trình bày hiện đại rõ ràng.
- [Sutton & Barto (2018). Ch. 9 — On-policy Prediction with Approximation](http://incompleteideas.net/book/RLbook2020.pdf) việc xử lý sách giáo khoa của "những phần ba chết người" (chấp gần chức năng + bootstrapping + ngoại lệ chính sách) mà mạng mục tiêu của DQN và bộ đệm lặp lại được thiết kế để làm đục.
- [CleanRL DQN implementation](https://docs.cleanrl.dev/rl-algorithms/dqn/) DQN tài liệu đơn tham khảo được sử dụng trong các nghiên cứu ablation; tốt để đọc cùng với phiên bản đầu tiên của bài học này.
