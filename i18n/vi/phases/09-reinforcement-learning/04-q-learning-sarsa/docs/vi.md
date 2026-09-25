# Sự khác biệt thời gian  Q-Learning & SARSA  时序差分  Q学习与SARSA

> Monte Carlo chờ đợi cho đến khi tập phim kết thúc. TD cập nhật sau mỗi bước bằng cách khởi động ước tính giá trị tiếp theo. Q-learning là không chính sách và lạc quan; SARSA là chính sách và thận trọng. Cả hai đều là một dòng mã. Cả hai đều là nền tảng cho mọi phương pháp RL sâu trong giai đoạn này.

> **【中文解读】**MC phải chờ đến khi vòng kết thúc để cập nhật, TD(tỷ lệ thời gian khác nhau) Mỗi bước đều có thể cập nhật sử dụng `r + γ V(s')`作为目标来引导当前估计;;Q-learning是离策略的(学习最优策略),SARSA là在线策略的(学习当前行为策略);;`max`Nhưng đó là nền tảng của tất cả RL sâu.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming), Phase 9 · 03 (Monte Carlo) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划), Phase 9 · 03 (蒙特卡洛)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Monte Carlo hoạt động nhưng nó có hai yêu cầu đắt tiền. Nó cần các tập kết thúc, và nó chỉ cập nhật sau khi trở lại cuối cùng là. Nếu tập của bạn là 1.000 bước, MC chờ 1.000 bước để cập nhật bất cứ điều gì.

> 蒙特卡洛 có hiệu quả nhưng có hai yêu cầu đắt tiền. Nó cần kết thúc chu kỳ, và chỉ cần được cập nhật sau khi báo cáo cuối cùng xuất hiện. Nếu chu kỳ có 1.000 bước, MC phải chờ 1.000 bước để cập nhật bất cứ điều gì.

Quá trình lập trình năng động có hồ sơ ngược lại  sao lưu khởi động không biến động  nhưng yêu cầu một mô hình được biết đến.

> 动态规划 có những đặc điểm ngược lại 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零方差 零差 零差 零方差 零方差 零方差 零差 零差 零差 零方差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零差 零

Sự khác biệt thời gian (TD) học tập chia khác biệt.`(s, a, r, s')`, tạo ra một mục tiêu một bước `r + γ V(s')`và đẩy`V(s)`Không có mô hình, không có tập hoàn chỉnh, không có sự thiên vị khi sử dụng một mô hình`V`trên RHS, nhưng sự khác biệt thấp hơn đáng kể so với MC và cập nhật trực tuyến từ bước một.

> 时序差分(TD) Learning折中了两者──从单次转移 `(s, a, r, s')`构造单步目标 `r + γ V(s')`,将 `V(s)`Nằm gần nó. Không cần mô hình. Không cần hoàn chỉnh vòng quay.`V`Có sự khác biệt, nhưng sự khác biệt thấp hơn MC, và từ bước đầu tiên là có thể được cập nhật trực tuyến.

Đây là khoang xoay mà tất cả các RL  DQN, A2C, PPO, SAC  hiện đại quay. Phần còn lại của giai đoạn 9 là các lớp gần gũi chức năng và thủ thuật được xây dựng trên đỉnh cập nhật TD một bước bạn sẽ viết trong bài học này.

> Đây là tất cả các trung tâm của RLDQN A2C、PPO、SAC hiện đại. Phần còn lại của giai đoạn 9 là các hàm gần gũi và kỹ thuật của các lớp mà bạn sẽ viết trong bài học này.

> **【中文解读】**TD học là DP và MC 折中: dùng một bước chuyển đổi `(s,a,r,s')`构造目标 `r + γV(s')`, không cần mô hình, cũng không cần hoàn chỉnh vòng lặp. Có sự phân biệt (vì sử dụng gần như V), nhưng sự phân biệt thấp hơn MC, và có thể được cập nhật trực tuyến.

> **【拓展：游戏AI→LLM对齐】**Q-learning là cốt lõi của Atari DQN năm 2013, mở ra thời đại RL sâu hơn.PPO là thuật toán cốt lõi của đào tạo RLHF của ChatGPT.

## Khái niệm cốt lõi

![Q-learning vs SARSA: off-policy max vs on-policy Q(s', a')](../assets/td.svg)

**The TD(0) update for V:**

`V(s) ← V(s) + α [r + γ V(s') - V(s)]`

Số lượng được xếp vào vòng đệm là lỗi TD `δ = r + γ V(s') - V(s)`Nó là analog trực tuyến của `G_t - V(s_t)`trong MC. Sự hội tụ đòi hỏi`α`làm hài lòng Robbins-Monro (`Σ α = ∞`- `Σ α² < ∞`) và tất cả các tiểu bang đã đến thăm vô hạn thường xuyên.

> **V 的 TD(0) 更新：**括号中的量是 TD 误差 `δ = r + γ V(s') - V(s)` Đó là MC `G_t - V(s_t)`                                                                                                                                                                                                                                                              `α`满足 Robbins-Monro 条件且所有状态被无限次访问.

**Q-learning.**Một phương pháp TD ngoài chính sách để kiểm soát:

`Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)]`

- `max`cho rằng chính sách tham lam sẽ được theo đuổi từ`s'`tiếp theo, bất kể tác nhân thực sự thực hiện hành động nào.`Q*`Mnih et al. (2015) đã chuyển đổi điều này thành deep Q-learning trên Atari (Dạy 05).

> **Q-learning。**Một cách khác biệt về phương pháp kiểm soát TD.`max`假设 từ `s'`开始将遵循*贪心*策略,无论智能体实际采取什么动作――这种解使 Q-learning 在通过 ε-贪心探索的同时学习`Q*`❖Mnih 等人 (2015) sẽ chuyển đổi thành Atari 上的深度 Q-learning (Dạy học 05):

**SARSA.**Một phương pháp TD trên chính sách:

`Q(s, a) ← Q(s, a) + α [r + γ Q(s', a') - Q(s, a)]`

Tên là tuple `(s, a, r, s', a')`SARSA sử dụng hành động này.`a'`- Không, không, không, không.`argmax`- Tương ứng với `Q^π`cho bất cứ điều gì `π`đang chạy, trong giới hạn `ε → 0`trở thành `Q*`- Tôi không biết.

> **SARSA。**Một种线上策略 TD 方法──名称是元组 `(s, a, r, s', a')`✿ SARSA 使用智能体* thực tế*采取的下一个动作 ✿`a'`, chứ không phải tham lam .`argmax`◊收到当前 ε-贪心 `π`của `Q^π`, trong `ε → 0`                `Q*`

**The cliff-walking difference.**Trong nhiệm vụ đi bộ vách đá cổ điển (đánh vách đá = phần thưởng -100), Q-learning học được con đường tối ưu dọc theo bờ vách đá nhưng đôi khi nhận được hình phạt trong quá trình khám phá. SARSA học được một con đường an toàn hơn một bước từ vách đá vì nó tạo ra tiếng ồn khám phá vào giá trị Q của nó.`ε → 0`Trong thực tế nó quan trọng: khi việc khám phá thực sự diễn ra tại triển khai, hành vi của SARSA là bảo thủ hơn.

> **【中文解读】**经典 dốc núi đi thử nghiệm cho thấy sự khác biệt quan trọng giữa Q-làm học và SARSA: Q-làm học học để gắn bó trên dốc núi tốt nhất nhưng tìm kiếm sẽ rơi xuống), SARSA học để tìm kiếm đường an toàn xa dốc núi vì nó xem xét tìm kiếm tiếng ồn)  Trong các triển khai trong nghiên cứu, SARSA bảo vệ an toàn hơn

**Expected SARSA.**Thay thế `Q(s', a')`với giá trị dự kiến của nó dưới `π`- Có thể là:

`Q(s, a) ← Q(s, a) + α [r + γ Σ_{a'} π(a'|s') Q(s', a') - Q(s, a)]`

Sự biến động thấp hơn SARSA (không có mẫu `a'`), cùng một mục tiêu chính sách.

> **期望 SARSA。**用 `π` 下的期望值替换 `Q(s', a')`◊ Than SARSA 方差低 hơn`a'`), cùng trong线策略目标──常作为现代教科书的默认选择──

**n-step TD and TD(λ).**Chuyển đổi giữa TD(0) và MC bằng cách chờ `n`bước trước khi khởi động. `n=1`là TD, `n=∞`là MC. TD(λ) trung bình trên tất cả `n`với trọng lượng hình học `(1-λ)λ^{n-1}`Hầu hết các sử dụng RL sâu `n`từ 3 đến 20.

> **n 步 TD 和 TD(λ)。**Trong TD(0) và MC  插值, chờ `n`步再自举──`n=1`là TD,`n=∞`- Đúng vậy. - Đúng vậy.`n`取平均──大多数深度 RL 使用 `n`Trong 3 đến 20...

> **【拓展：TD 误差在 LLM RLHF 中的对应】**TD 误差 δ = r + γV(s') - V(s) trong đào tạo RLHF của LLM trong một số đối ứng trực tiếp:

## Hãy xây dựng nó.
```figure
qlearning-gridworld
```

## Hãy xây dựng nó

### Bước 1: SARSA về chính sách tham lam

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

8 dòng. Sự khác biệt duy nhất với Q-learning là đường mục tiêu.

> 八行代码──与Q-learning *唯一*的区别是目标行──

### Bước 2: Học Q

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

- `max`Một biểu tượng đó là sự khác biệt giữa chính sách và ngoại chính sách.

> `max`Để giải quyết mục tiêu và hành vi.

### Bước 3: đường cong học tập

Track trung bình trở lại mỗi 100 tập. Q-learning hội tụ nhanh hơn trên đơn giản xác định GridWorld; SARSA là bảo thủ hơn trên đáy.`code/main.py`, cả hai đều gần như tối ưu sau khoảng 2.000 tập với `α=0.1, ε=0.1`- Tôi không biết.

> Theo dõi mỗi 100 lần quay lại trung bình. Q-learning trong một sự xác định đơn giản.`code/main.py`của 4×4 GridWorld 上, hai trong `α=0.1, ε=0.1`Khoảng 2.000 lần quay lại gần như là tốt nhất.

### Bước 4: so sánh với sự thật DP

Tiến trình lặp lại giá trị chạy (Dạy 02) để có được `Q*`- Đánh giá`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`Một chất tác dụng TD bảng hợp chất tốt sẽ rơi vào `~0.5`trên 4×4 GridWorld sau 10.000 tập.

> 运行值代(Dạy 02) 获得`Q*`❖ kiểm tra`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`❖ Một biểu đồ khỏe mạnh TD 智能体在10,000 回合后在4×4 GridWorld 上误差在`~0.5`Trong

## Những bẫy

- **Initial Q values matter.**Optimistic init (`Q = 0`(với một nhiệm vụ có phần thưởng tiêu cực) khuyến khích khám phá.
  **初始 Q 值很重要。**乐观初始化 负奖励任务中`Q = 0`(Bản phẩm:                                                                                                                                                                                                                                                             
- **α schedule.**- Không ngừng`α`Nó tốt cho các vấn đề không ổn định.`α_n = 1/n`cho sự hội tụ về mặt lý thuyết nhưng quá chậm trong thực tế  pin `α`trong `[0.05, 0.3]`và theo dõi đường cong học tập.
  **α 调度。**常数 `α`适用于 các vấn đề không bình thường `α_n = 1/n`Về lý thuyết thì nhận được nhưng thực tế thì quá chậm`α` cố định `[0.05, 0.3]`并监控学习曲线──
- **ε schedule.**Bắt đầu cao (`ε=1.0`), phân rã đến `ε=0.05`"GLIE" (cười tham lam trong giới hạn với khám phá vô hạn) là điều kiện hội tụ.
  **ε 调度。**Từ高值开始`ε=1.0`), giảm xuống`ε=0.05` "GLIE"极限贪心且无限探索) là điều kiện 
- **Max bias in Q-learning.**- `max`người vận hành bị thiên vị lên khi `Q`dẫn đến đánh giá quá mức  Hasselt's Double Q-learning (được DDQN sử dụng trong Bài học 05) khắc phục điều này bằng hai bảng Q.
  **Q-learning 的最大化偏差。** `max`算子在 `Q`Có tiếng ồn khi lên thiên vị. dẫn đến ước tính.
- **Non-terminating episodes.**TD có thể học mà không cần thiết bị kết thúc, nhưng bạn cần phải đóng cửa các bước hoặc xử lý bootstrap đúng ở đầu.
  **非终止回合。**TD có thể học trong trạng thái không kết thúc, nhưng cần thiết lập số bước trên giới hạn hoặc xử lý chính xác tự hành ở giới hạn trên.
- **State hashing.**Nếu các trạng thái là tuples/tensors, sử dụng một khóa có thể hash (tuple, không phải danh sách; tuple của floats tròn, không là nguyên liệu).
  **状态哈希。**Nếu trạng thái là khối/tỷ lệ, sử dụng các khóa có thể tính toán (tỷ lệ của khối)

## Hãy sử dụng nó để thực hiện

Tầm nhìn TD năm 2026:

> Bản đồ của TD 学习 năm 2026:

| Task | Method | Reason |
|------|--------|--------|
| Task / 任务 | Method / 方法 | Reason / 原因 |
| Small tabular environments / 小型表格环境 | Q-learning | Learns optimal policy directly. / 直接学习最优策略。 |
| On-policy safety-critical / 在线策略安全关键 | SARSA / Expected SARSA | Conservative during exploration. / 探索期间保守。 |
| High-dimensional state / 高维状态 | DQN (Phase 9 · 05) | Neural-net Q-function with replay and target net. / 神经网络 Q 函数+回放+目标网络。 |
| Continuous actions / 连续动作 | SAC / TD3 (Phase 9 · 07) | TD update on a Q-network; policy net emits actions. / Q 网络上的 TD 更新；策略网络输出动作。 |
| LLM RL (reward-model-based) / LLM RL（基于奖励模型） | PPO / GRPO (Phase 9 · 08, 12) | Actor-critic with TD-style advantage via GAE. / Actor-Critic + GAE 的 TD 式优势。 |
| Offline RL / 离线 RL | CQL / IQL (Phase 9 · 08) | Q-learning with conservative regularization. / 带保守正则化的 Q-learning。 |

90% số "RL" mà bạn đọc trong các bài báo 2026 là một số sự tinh chỉnh của Q-learning hoặc SARSA.

> Trong bài báo năm 2026 bạn đọc được "RL", 90% là một số biến thể của Q-làm học hoặc SARSA. Trước khi đọc sâu hơn, trước tiên hãy nâng cấp biểu đồ để nắm bắt bộ nhớ cơ thể.

## Chuyển nó đi.

Cứ như `outputs/skill-td-agent.md`- Có thể là:

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

## Tập luyện bài tập

1. **Easy.**Thực hiện Q-learning và SARSA trên 4×4 GridWorld. Lập đường cong học tập (tỷ lệ thu về mỗi 100 tập) cho 2.000 tập. Ai hội tụ nhanh hơn?
   > **练习1：**Trong GridWorld trên đối với Q-làm học và SARSA của học đường.
2. **Medium.**Xây dựng môi trường đi bộ vách đá (4x12, hàng cuối là vách đá với phần thưởng -100 và đặt lại để bắt đầu). So sánh các chính sách cuối cùng của Q-learning và SARSA.
   > **练习2：**实现悬崖行走环境,观察 Q-learning (tiếng Việt: Q-learning)
3. **Hard.**Thực hiện học Q đôi. Trên một GridWorld có phần thưởng tiếng ồn (giá tiếng Gaussian σ=5 thêm vào phần thưởng mỗi bước), cho thấy học Q đánh giá quá cao `V*(0,0)`bằng một số lượng có ý nghĩa trong khi học Double Q không.
   > **练习3：**Thực hiện việc học Q hai lần, chứng minh nó có thể loại bỏ sự phân biệt tối đa về học Q.

## Từ khóa  Từ khóa nhanh chóng

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

## Xem thêm 延伸阅读

- [Watkins & Dayan (1992). Q-learning](https://link.springer.com/article/10.1007/BF00992698) giấy gốc và bằng chứng hội tụ.
- [Sutton & Barto (2018). Ch. 6 — Temporal-Difference Learning](http://incompleteideas.net/book/RLbook2020.pdf) TD(0), SARSA, Q-learning, dự kiến SARSA.
- [Hasselt (2010). Double Q-learning](https://papers.nips.cc/paper_files/paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html) sửa chữa cho sự thiên vị tối đa hóa.
- [Seijen, Hasselt, Whiteson, Wiering (2009). A Theoretical and Empirical Analysis of Expected SARSA](https://ieeexplore.ieee.org/document/4927542) động lực SARSA dự kiến.
- [Rummery & Niranjan (1994). On-line Q-learning using connectionist systems](https://www.researchgate.net/publication/2500611_On-Line_Q-Learning_Using_Connectionist_Systems) bài báo đã tạo ra SARSA (sau đó được gọi là "sự học Q-thông tin kết nối sửa đổi").
- [Sutton & Barto (2018). Ch. 7 — n-step Bootstrapping](http://incompleteideas.net/book/RLbook2020.pdf) tổng hợp TD(0) đến TD(n), con đường từ Q-làm học đến các dấu vết đủ điều kiện và sau đó, GAE trong PPO.
