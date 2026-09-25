# Phương pháp Monte Carlo  Học từ các tập hoàn chỉnh  Phương pháp Monte Carlo  Học từ vòng hoàn chỉnh

> Phương pháp lập trình năng động cần một mô hình. Monte Carlo chỉ cần các tập.

> **【中文解读】**动态规划需要已知环境模型,蒙特卡洛只需要完整的回合数据:执行策略、观测回报、取平均── đây là ý tưởng đơn giản nhất trong RL, cũng là nền tảng của tất cả các thuật toán tiếp theo (TD、Q-learning、PPO、RLHF).

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Quá trình lập trình năng động là thanh lịch, nhưng nó cho rằng bạn có thể truy vấn `P(s' | s, a)`Một robot không thể tính toán phân phối trên các pixel máy ảnh theo một mô-men xoắn chung. Một thuật toán định giá không thể tích hợp trên mọi phản ứng khách hàng có thể. Một LLM không thể liệt kê tất cả các tiếp tục có thể sau một token.

> 动态规划 rất đẹp, nhưng nó cho rằng bạn có thể truy vấn mọi trạng thái và động tác `P(s' | s, a)`◊ thực tế hầu như không có gì làm việc như vậy ◊ máy tính không thể phân tích phân bố của các hình ảnh của các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh trong các hình ảnh.

Bạn cần một phương pháp mà chỉ cần khả năng *mặt mẫu* từ môi trường.`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`- Sử dụng nó để ước tính giá trị.

> Bạn cần một phương pháp chỉ cần lấy từ môi trường.`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`Hãy dùng nó để đánh giá giá trị. Đó là Monte Carlo.

Sự chuyển đổi từ DP sang MC là triết học quan trọng: chúng ta chuyển từ * mô hình được biết + sao lưu chính xác * sang * triển khai mẫu + lợi nhuận trung bình *. Sự khác biệt nhảy vọt, nhưng tính áp dụng nổ. Mỗi thuật toán RL sau bài học này  TD, Q-learning, REINFORCE, PPO, GRPO  là một ước tính Monte Carlo ở cốt lõi, đôi khi với bootstrapping được layered trên.

> Sự chuyển đổi từ DP đến MC rất quan trọng về triết học: chúng ta từ * mô hình đã biết + dự trữ chính xác * chuyển hướng * mẫu rollout + trung bình trả về *.

> **【中文解读】**Từ DP đến MC: Từ "định hình được biết+ tính toán chính xác" đến "định hình đường ray+ báo cáo trung bình"―― khoảng cách tăng lên, nhưng phạm vi áp dụng đã mở rộng một cách bùng nổ――PPO、RLHF về cơ bản là các biến thể của MC  ước tính――

> **【拓展：LLM中的MC】**Trong đào tạo RLHF của ChatGPT, cho mỗi yêu cầu 采样多个答案、计算平均奖励 đây là ứng dụng trực tiếp của ý tưởng MC trong đào tạo mô hình lớn。DeepSeek-R1's GRPO cũng dựa trên nhóm trong 采集的MC 估计──

## Khái niệm cốt lõi

![Monte Carlo: rollout, compute returns, average; first-visit vs every-visit](../assets/monte-carlo.svg)

**The core idea, in one line:** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`nơi `G^{(i)}(s)`được quan sát về những lần thăm `s`trong chính sách`π`- Tôi không biết.

> **核心思想，一行概括：** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`, trong số đó `G^{(i)}(s)`là trong chiến lược`π`下访问 `s`时观测到的回报──

> **【中文解读】**MC  đánh giá lõi: giá trị trạng thái = giá trị trung bình của các lần tham gia vào trạng thái này.`V_new = V_old + α(target - V_old)`Đó là một đường dây của các thuật toán RL hiện đại.

**First-visit vs every-visit MC.**Với một tập phim đến thăm tiểu bang `s`nhiều lần, lần đầu tiên MC chỉ tính toán sự trở lại từ lần đầu tiên; mỗi lần truy cập MC tính tất cả các chuyến thăm. Cả hai đều không thiên vị trong giới hạn. lần đầu tiên dễ phân tích hơn (iid mẫu). Mỗi lần truy cập sử dụng nhiều dữ liệu hơn cho mỗi tập và thường hội tụ nhanh hơn trong thực tế.

> **首次访问 vs 每次访问 MC。**Định vị nhiều lần truy cập`s`Trong khi đó, lần đầu tiên truy cập MC chỉ tính lần đầu tiên truy cập của bạn; mỗi lần truy cập MC  tính tất cả truy cập.

**Incremental mean.**Thay vì lưu trữ tất cả các thông tin trả lại, cập nhật trung bình chạy:

`V_n(s) = V_{n-1}(s) + (1/n) [G_n - V_{n-1}(s)]`

Tái tổ chức: `V_new = V_old + α · (target - V_old)`với `α = 1/n`- Thay đổi`1/n`cho một bước kích thước liên tục `α ∈ (0, 1)`và bạn có một máy ước tính MC không tĩnh mà theo dõi thay đổi trong `π`Chuyển động đó là toàn bộ bước từ MC đến TD đến mọi thuật toán RL hiện đại.

> **增量均值。**Không lưu trữ tất cả các báo cáo, mà là cập nhật giá trị trung bình của hoạt động.`1/n`替换为常数步长 `α ∈ (0, 1)`Để tôi có được một dấu vết.`π` biến đổi không ổn định MC  đánh giá . Đây là bước nhảy vọt từ MC đến TD đến tất cả các thuật toán RL hiện đại.

**Exploration is now a problem.**DP đã chạm vào mọi tiểu bang bằng cách đếm. MC chỉ nhìn thấy các tiểu bang các chuyến thăm chính sách. Nếu`π`là xác định, toàn bộ khu vực trong không gian nhà nước không bao giờ được lấy mẫu, và ước tính giá trị của chúng vẫn ở mức không mãi mãi.

> **探索现在成了问题。**DP 通过枚举触及每个状态──MC chỉ có thể xem các chiến lược truy cập vào trạng thái──如果`π`Là chắc chắn, toàn bộ khu vực của không gian trạng thái sẽ không bao giờ được lấy mẫu, giá trị ước tính sẽ luôn là 0.

> **【中文解读】**探索问题:DP 能遍历所有状态,MC chỉ có thể nhìn thấy các chiến lược đã truy cập vào trạng thái.

1. **Exploring starts.**Bắt đầu mỗi tập từ một cặp ngẫu nhiên (s, a). Giảm bảo bảo hiểm; không thực tế trong thực tế (bạn không thể "đưa lại" một robot vào trạng thái tùy tiện).
   **探索起点。**Mỗi vòng quay từ bất cứ lúc nào, a) đối với bắt đầu.
2. **ε-greedy.**Tạo hành tham lam với Q hiện tại, nhưng với khả năng`ε`chọn một hành động ngẫu nhiên. tất cả các cặp hành động trạng thái được lấy mẫu theo cách không đồng nghĩa.
   **ε-贪心。**Đối với hiện tại Q 贪心行动, nhưng theo tỷ lệ`ε`随机选动作──所有状态动作对渐近地被采样──
3. **Off-policy MC.**Thu thập dữ liệu theo chính sách hành vi `μ`, tìm hiểu về chính sách mục tiêu `π`Sự khác biệt cao, nhưng nó là cầu nối với các phương pháp buffer như DQN.
   **离策略 MC。**Trong chiến lược hành vi`μ`下 thu thập dữ liệu, thông qua tầm quan trọng của các chiến lược học tập mục tiêu`π`高方差, nhưng nó là đường đi DQN 等回放缓冲方法的桥梁

**Monte Carlo Control.**Đánh giá → cải thiện → đánh giá, giống như lặp lại chính sách, nhưng đánh giá dựa trên mẫu:

1. Đi chạy`π`, lấy một tập phim.
2. Tới thiệu `Q(s, a)`từ những kết quả được quan sát.
3. Làm `π`ε-cái tham lam w.r.t. `Q`- Tôi không biết.
4. Lặp lại.

Tương ứng với `Q*`và `π*`với xác suất 1 trong điều kiện nhẹ (mỗi cặp được truy cập vô hạn thường xuyên,`α`làm hài lòng Robbins-Monro).

> **蒙特卡洛控制。**评估 → 改进 → 评估,就像策略代, nhưng đánh giá dựa trên mô hình.`α`满足 Robbins-Monro), với tỷ lệ 1 收到 `Q*`和 `π*`

## Hãy xây dựng nó.
```figure
epsilon-greedy
```

## Hãy xây dựng nó

### Bước 1: rollout → danh sách (s, a, r)

```python
def rollout(env, policy, max_steps=200):
    trajectory = []
    s = env.reset()
    for _ in range(max_steps):
        a = policy(s)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r))
        s = s_next
        if done:
            break
    return trajectory
```

Không có mô hình, chỉ là `env.reset()`và `env.step(s, a)`- Giống như môi trường tập thể dục nhưng không được trang bị.

> Không cần mô hình, chỉ cần`env.reset()`和 `env.step(s, a)`                                                                                                                                                                                                                                                              

### Bước 2: trả lại tính toán (tránh ngược)

```python
def returns_from(trajectory, gamma):
    returns = []
    G = 0.0
    for _, _, r in reversed(trajectory):
        G = r + gamma * G
        returns.append(G)
    return list(reversed(returns))
```

Một lần đi qua.`O(T)`Sự tái phát ngược lại`G_t = r_{t+1} + γ G_{t+1}`tránh tổng hợp lại.

> Một lần qua đời,`O(T)`        `G_t = r_{t+1} + γ G_{t+1}`避免了重复求和──

### Bước 3: đánh giá MC lần đầu tiên

```python
def mc_policy_evaluation(env, policy, episodes, gamma=0.99):
    V = defaultdict(float)
    counts = defaultdict(int)
    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for t, ((s, _, _), G) in enumerate(zip(trajectory, returns)):
            if s in seen:
                continue
            seen.add(s)
            counts[s] += 1
            V[s] += (G - V[s]) / counts[s]
    return V
```

Ba dòng làm việc: đánh dấu trạng thái như được nhìn thấy trong chuyến thăm đầu tiên, số lượng tăng, trung bình chạy cập nhật.

> 三行代码完成工作: 标记第一次访问的状态,增加计数,更新运行平均值──

### Bước 4: kiểm soát MC tham lam (trong chính sách)

```python
def mc_control(env, episodes, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    counts = defaultdict(lambda: {a: 0 for a in ACTIONS})

    def policy(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for (s, a, _), G in zip(trajectory, returns):
            if (s, a) in seen:
                continue
            seen.add((s, a))
            counts[s][a] += 1
            Q[s][a] += (G - Q[s][a]) / counts[s][a]
    return Q, policy
```

### Bước 5: so sánh với tiêu chuẩn vàng DP

Đánh giá của MC của bạn về`V^π`nên đồng ý với kết quả DP từ Bài học 02 như các tập → ∞. Trong thực tế: 50.000 tập trên 4×4 GridWorld đưa bạn trong `~0.1`của câu trả lời DP.

> Anh là `V^π`∞ 时应与课02的 DP 结果一致──实践中:4×4 GridWorld 上 50,000 回合可将错误控制在 ∞ 时应与课02的 DP 结果一致──实践中:4×4 GridWorld 上 50,000 回合可将错误控制在 ∞ ∞ 时应与课02 的 DP 结果一致──实践中:4×4 GridWorld 上 50,000 回合可将错误控制在 ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ `~0.1`Trong

## Những bẫy

- **Infinite episodes.**MC cần các tập phim để chấm dứt. Nếu chính sách của bạn có thể lặp mãi mãi, cap `max_steps`và coi nắp như thất bại ngầm. GridWorld với một chính sách ngẫu nhiên thường xuyên thời gian ra  đó là bình thường, chỉ cần đảm bảo bạn đếm nó đúng.
  **无限回合。**MC 要求回合*终止*──如果策略可能永远循环,设置 `max_steps`Ưu điểm sẽ được xem là thất bại ẩn dụ.
- **Variance.**MC sử dụng hoàn toàn trả lại. Trong các tập dài, sự khác biệt là rất lớn  một phần thưởng không may ở cuối các phiên `V(s_0)`Các phương pháp TD (Lớp 04) cắt giảm điều này bằng cách khởi động.
  **方差。**MC sử dụng toàn bộ báo cáo.`V(s_0)`◊TD 方法(Lớp 04) thông qua tự động để giảm tỷ lệ khác biệt.
- **State coverage.**MC tham lam trên một Q mới với dây xích sẽ chỉ thử một hành động.
  **状态覆盖。**Ơn của tôi là một sự thật.
- **Non-stationary policies.**Nếu`π`(như trong kiểm soát MC), các khoản trả lại cũ là từ một chính sách khác.
  **非平稳策略。**Nếu `π`变化(如 MC 控制中),旧回报来自不同策略──常数 α MC 处理此问题;样本平均 MC 不能──
- **Off-policy importance sampling.**Những trọng lượng `π(a|s)/μ(a|s)`Tăng bằng đường đi, biến động nổ với chân trời, giới hạn với IS/phát quyết hoặc chuyển sang TD.
  **离策略重要性采样。**权重 `π(a|s)/μ(a|s)`Trong quỹ đạo tích lũy số lần.

## Hãy sử dụng nó để thực hiện

Vai trò của phương pháp Monte Carlo năm 2026:

> 2026  Монт卡洛方法的角色:

| Use case | Why MC |
|----------|--------|
| Use case / 用例 | Why MC / 为什么用 MC |
| Short-horizon games (blackjack, poker) / 短视野游戏（二十一点、扑克） | Episodes terminate naturally; returns are clean. / 回合自然终止；回报干净。 |
| Offline evaluation of a logged policy / 离线评估已记录的策略 | Average discounted returns over stored trajectories. / 对存储轨迹取折扣回报平均。 |
| Monte Carlo Tree Search (AlphaZero) / 蒙特卡洛树搜索 | MC rollouts from tree leaves guide selection. / 树叶的 MC rollout 指导选择。 |
| LLM RL evaluation / LLM RL 评估 | Compute average reward over sampled completions for a given policy. / 对给定策略的采样完成计算平均奖励。 |
| Baseline estimation in PPO / PPO 中的基线估计 | The advantage target `A_t = G_t - V(s_t)` uses an MC `G_t`. / 优势目标使用 MC 的 `G_t`。 |
| Teaching RL / 教学 RL | Simplest algorithm that actually works — strip bootstrapping to see the core. / 最简单且有效的算法——去掉自举看核心。 |

Các thuật toán sâu-RL hiện đại (PPO, SAC) liên kết giữa MC tinh khiết (cũng trả lại) và TD tinh khiết (một bước khởi động) thông qua `n`- bước trở lại hoặc GAE. Cả hai điểm cuối là các trường hợp của ước tính tương tự.

> 现代深度 RL 算法(PPO、SAC) thông qua `n`步回报或 GAE 在纯 MC (cũng hoàn toàn回报) 和纯 TD (单步自举) 间插值.

## Chuyển nó đi.

Cứ như `outputs/skill-mc-evaluator.md`- Có thể là:

```markdown
---
name: mc-evaluator
description: Evaluate a policy via Monte Carlo rollouts and produce a convergence report with DP-comparison if available.
version: 1.0.0
phase: 9
lesson: 3
tags: [rl, monte-carlo, evaluation]
---

Given an environment (episodic, with reset+step API) and a policy, output:

1. Method. First-visit vs every-visit MC. Reason.
2. Episode budget. Target number, variance diagnostic, expected standard error.
3. Exploration plan. ε schedule (if needed) or exploring starts.
4. Gold-standard comparison. DP-optimal V* if tabular; otherwise a bound from a Q-learning / PPO baseline.
5. Termination check. Max-step cap, timeouts, handling of non-terminating trajectories.

Refuse to run MC on non-episodic tasks without a finite horizon cap. Refuse to report V^π estimates from fewer than 100 episodes per state for tabular tasks. Flag any policy with zero-variance actions as an exploration risk.
```

## Tập luyện bài tập

1. **Easy.**Thực hiện đánh giá MC lần đầu tiên về chính sách đồng bộ ngẫu nhiên trên 4×4 GridWorld.`V(0,0)`như một hàm số tập so với câu trả lời DP.
   > **练习1：**实现 MC 评估,将 V(0,0) 随回合数收曲线与 DP 基准对比──
2. **Medium.**Thực hiện kiểm soát MC tham lam với `ε ∈ {0.01, 0.1, 0.3}`So sánh mức thu hồi trung bình sau 20.000 tập.
   > **练习2：**用不同 ε 值做 MC 控制,观察探索-利用权衡──
3. **Hard.**Thực hiện các MC ngoài chính sách với việc lấy mẫu quan trọng: thu thập dữ liệu theo chính sách ngẫu nhiên đồng nhất `μ`, ước tính`V^π`cho chính sách tối ưu định nghĩa `π`So sánh IS đơn giản so với IS theo quyết định so với IS trọng lượng.
   > **练习3：**实现离策略 MC 重要性采样), so sánh khác nhau IS 方差的差异──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Monte Carlo | "Random sampling" / 蒙特卡洛 | Estimate expectations by averaging over iid samples from the distribution. |
| Return `G_t` | "Future reward" / 回报 | Sum of discounted rewards from step `t` to episode end: `Σ_{k≥0} γ^k r_{t+k+1}`. |
| First-visit MC | "Count each state once" / 首次访问 MC | Only the first visit in an episode contributes to the value estimate. |
| Every-visit MC | "Use all visits" / 每次访问 MC | Every visit contributes; slightly biased but more sample-efficient. |
| ε-greedy | "Exploration noise" / ε-贪心 | Pick greedy action with prob `1-ε`; random action with prob `ε`. |
| Importance sampling | "Correcting for sampling from the wrong distribution" / 重要性采样 | Reweight returns by `π(a\|s)/μ(a\|s)` products to estimate `V^π` from `μ` data. |
| On-policy | "Learn from my own data" / 在线策略 | Target policy = behavior policy. Vanilla MC, PPO, SARSA. |
| Off-policy | "Learn from someone else's data" / 离线策略 | Target policy ≠ behavior policy. Importance-sampled MC, Q-learning, DQN. |

## Xem thêm 延伸阅读

- [Sutton & Barto (2018). Ch. 5 — Monte Carlo Methods](http://incompleteideas.net/book/RLbook2020.pdf) điều trị theo luật pháp.
- [Singh & Sutton (1996). Reinforcement Learning with Replacing Eligibility Traces](https://link.springer.com/article/10.1007/BF00114726) lần đầu tiên và mỗi lần thăm.
- [Precup, Sutton, Singh (2000). Eligibility Traces for Off-Policy Policy Evaluation](http://incompleteideas.net/papers/PSS-00.pdf) MC và kiểm soát biến động ngoài chính sách.
- [Mahmood et al. (2014). Weighted Importance Sampling for Off-Policy Learning](https://arxiv.org/abs/1404.6362) Máy ước tính IS hiện đại có biến thể thấp.
- [Tesauro (1995). TD-Gammon, A Self-Teaching Backgammon Program](https://dl.acm.org/doi/10.1145/203330.203343) sự chứng minh thực nghiệm quy mô lớn đầu tiên của MC/TD tự chơi hội tụ với trò chơi siêu nhân; tiền thân khái niệm cho mỗi bài học trong nửa sau của giai đoạn này.
