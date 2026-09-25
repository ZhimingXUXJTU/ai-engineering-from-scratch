# Dynamic Programming  Policy Iteration & Value Iteration  动态规划  策略代与价值代

> Chương trình năng động là RL với gian lận. Bạn đã biết các chức năng chuyển đổi và phần thưởng; bạn chỉ cần lặp lại phương trình Bellman cho đến khi`V`hoặc `π`là chuẩn mực mà mọi phương pháp dựa trên lấy mẫu đều cố gắng tiếp cận.

> **【中文解读】**动态规划是强化学习的"作弊版"你已知环境的转移概率和奖励函数, chỉ cần lặp lại 代 Bellman 方程直到收──它是所有采样方法的"金标准" (Q-learning、PPO 等) 参照──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs) | **前置知识:** Phase 9 · 01 (MDP)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Bạn có một MDP với một mô hình được biết đến: bạn có thể truy vấn `P(s' | s, a)`và `R(s, a, s')`Một nhà quản lý hàng tồn kho biết phân phối nhu cầu. Một trò chơi bảng có chuyển đổi xác định. Một gridworld là bốn dòng Python. Bạn có một * mô hình *.

> Bạn có một mô hình đã biết MDP: bạn có thể truy vấn bất kỳ trạng thái- động tác đối với `P(s' | s, a)`和 `R(s, a, s')` Nhà quản lý kho biết nhu cầu phân bố  Game có xác định chuyển động  GridWorld là bốn dòng Python  Bạn có một mô hình 

RL không có mô hình (Q-learning, PPO, REINFORCE) được phát minh cho trường hợp bạn không có mô hình  bạn chỉ có thể lấy mẫu từ môi trường. Nhưng khi bạn có một, có các phương pháp nhanh hơn, tốt hơn: lập trình năng động. Bellman thiết kế chúng vào năm 1957.

> 无模型 RL(Q-learning、PPO、REINFORCE) là một cách phát triển cho tình huống không có mô hình. Bạn chỉ có thể lấy mẫu từ môi trường. Nhưng khi bạn có mô hình, có cách tốt hơn nhanh hơn: động thái lập kế hoạch. Bellman thiết kế chúng vào năm 1957. Chúng vẫn xác định tính chính xác: Khi mọi người nói "các chiến lược tốt nhất của MDP này", họ chỉ định là chiến lược trả lại của DP.

> **【中文解读】**Khi bạn biết mô hình môi trường (xác suất chuyển đổi và hàm thưởng) thì, động thái có thể xác định được giải pháp tối ưu nhất.

> **【拓展：AlphaZero/MCTS】**AlphaZero's Monte Carlo Tree Search (MCTS) bản chất là phiên bản khác biệt của Bellman 备份 trong search tree 代价函数──思想DP trải qua toàn bộ chuỗi từ game AI đến big model推理──

Bạn cần chúng vào năm 2026 vì ba lý do. Thứ nhất, mọi môi trường bảng tính trong nghiên cứu RL (GridWorld, FrozenLake, CliffWalking) được giải quyết với DP để tạo ra chính sách tiêu chuẩn vàng. thứ hai, các giá trị chính xác cho phép bạn *debug* phương pháp lấy mẫu: nếu ước tính của Q-learning cho `V*(s_0)`Không đồng ý với câu trả lời DP bằng 30%, Q-learning của bạn có một lỗi. Thứ ba, các phương pháp RL ngoại tuyến hiện đại và lập kế hoạch (MCTS, tìm kiếm của AlphaZero, RL dựa trên mô hình trong giai đoạn 9 · 10) tất cả lặp lại một bản sao Bellman trên một mô hình được học hoặc được đưa ra.

> Bạn cần chúng vào năm 2026 , vì có ba lý do. Thứ nhất,RL trong nghiên cứu mỗi biểu mẫu môi trường (GridWorld, FrozenLake, CliffWalking) đều sử dụng DP để tìm giải pháp để tạo ra các chiến lược tiêu chuẩn vàng.`V*(s_0)`Phân tích của các nghiên cứu về các phương pháp học tập và các phương pháp lập kế hoạch của các nhà nghiên cứu về các phương pháp học tập và các phương pháp học tập dựa trên các mô hình học tập (Phase 9 · 10 của các nghiên cứu trên các mô hình học tập) đều đang học tập hoặc được định nghĩa.

## Khái niệm cốt lõi

![Policy iteration and value iteration, side by side](../assets/dp.svg)

**Two algorithms, both fixed-point iteration on Bellman.**

> **两种算法，都是对 Bellman 方程做不动点迭代。**

> **【中文解读】**Hai loại thuật toán đều đối với phương pháp Bellman làm không động điểm代──策略代:交替执行"策略评估"和"策略改进"直到策略不变; giá trị代:将两者合并为一步,直接取 max──两者最终收到同一个优值函数 V*──

**Policy iteration.**Chuyển đổi hai bước cho đến khi chính sách ngừng thay đổi.

> **策略迭代。**交替执行两个步骤直到策略不再改变──

1. *Thêm đánh giá:* chính sách nhất định `π`, tính toán`V^π`bằng cách áp dụng nhiều lần `V(s) ← Σ_a π(a|s) Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`cho đến khi nó hội tụ.
   * đánh giá:* 给定策略 `π`, lặp lại ứng dụng Bellman 方程直到 `V^π`收──
2. *Cải thiện:* được đưa ra `V^π`, làm `π`Thằng tham lam.`V^π``π(s) ← argmax_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`- Tôi không biết.
   *改进:* 给定 `V^π`,让 `π`Đối với`V^π`贪心.

Sự hội tụ được đảm bảo bởi vì (a) mỗi bước cải tiến hoặc giữ `π`tương tự hoặc tăng chặt chẽ `V^π`cho một số trạng thái, (b) không gian của các chính sách xác định là hữu hạn. thường hội tụ trong ~ 520 lặp lại bên ngoài ngay cả cho không gian nhà nước lớn.

> 收性是有保证的,因为 (a) Mỗi lần cải tiến để giữ `π`Không thay đổi, phải nghiêm trọng tăng một trạng thái nào đó `V^π`,(b) Không gian định tính là giới hạn. Ngay cả đối với không gian trạng thái lớn, thường chỉ cần ~ 5-20 lần bên ngoài.

**Value iteration.**Phong trào đánh giá và cải tiến thành một lần phơi bày.

`V(s) ← max_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`

Lặp lại cho đến khi `max_s |V_{new}(s) - V(s)| < ε`. Tạo ra chính sách vào cuối bằng cách thực hiện hành động tham lam. Cụ thể nhanh hơn cho mỗi lặp  không có vòng đánh giá bên trong  nhưng thường cần nhiều lần lặp hơn để hội tụ.

> **值迭代。**Phân tích và cải tiến sẽ được kết hợp cho một lần quét. Ứng dụng Bellman * tối ưu nhất * phương pháp.

**Generalized policy iteration (GPI).**Các khung thống nhất. chức năng giá trị và chính sách được khóa trong một vòng cải thiện hai chiều; bất kỳ phương pháp nào thúc đẩy cả hai hướng đến sự nhất quán lẫn nhau (lần lặp lại giá trị không đồng bộ, lặp lại chính sách sửa đổi, Q-learning, diễn viên-chính trị, PPO) là một ví dụ của GPI.

> **【拓展：GPI→PPO/RLHF】**广义策略代 (GPI) là một khuôn khổ:Q-learning、Actor-Critic、PPO trên thực chất là một ví dụ về GPI── hiểu được GPI của DP, bạn đã hiểu được Triết lý thiết kế của vòng đào tạo RLHF  ChatGPT 背后──

**Why `γ < 1` matters.**Người vận hành Bellman là một `γ`-sự thu hẹp trong chuẩn sup: `||T V - T V'||_∞ ≤ γ ||V - V'||_∞`Sự thu hẹp liên quan đến điểm cố định và sự hội tụ hình học độc đáo.`γ < 1`và bạn mất bảo đảm  bạn cần một chân trời hữu hạn hoặc một trạng thái hấp thụ cuối cùng.

> **为什么 `γ < 1` 很重要。**Bellman đang ở trong một số lượng lớn`γ`- compress 映射── compress nghĩa là điểm không động và quan điểm nhận ‖ bỏ ‖`γ < 1`Giảm bảo rằng bạn cần một thị trường hạn chế hoặc một trạng thái kết thúc hấp thụ.

## Hãy xây dựng nó.
```figure
value-iteration-gamma
```

## Hãy xây dựng nó

### Bước 1: xây dựng mô hình GridWorld MDP

Sử dụng cùng một 4x4 GridWorld từ Bài học 01. Chúng tôi thêm một biến thể stochastic: với xác suất `0.1`Máy bay trượt sang một hướng thẳng đứng ngẫu nhiên.

> Sử dụng Bài học 01 trong cùng 4×4 GridWorld. Chúng tôi thêm một biến thể tự nhiên:`0.1`智能体会滑向随机垂直方向──

```python
SLIP = 0.1

def transitions(state, action):
    if state == TERMINAL:
        return [(state, 0.0, 1.0)]
    outcomes = []
    for direction, prob in action_probs(action):
        outcomes.append((apply_move(state, direction), -1.0, prob))
    return outcomes
```

`transitions(s, a)`trả lại danh sách `(s', r, p)`Đây là toàn bộ mô hình.

> `transitions(s, a)` quay lại `(s', r, p)`列表──这是整个模型──

### Bước 2: Đánh giá chính sách

Với một chính sách `π(s) = {action: prob}`, lặp lại phương trình Bellman cho đến khi `V`dừng di chuyển:

> 给定策略 `π(s) = {action: prob}`, 代 Bellman 方程直到 `V`Không biến đổi:

```python
def policy_evaluation(policy, gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = sum(pi_a * sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a))
                   for a, pi_a in policy(s).items())
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            return V
```

### Bước 3: Cải thiện chính sách

Thay thế `π`với chính sách tham lam w.r.t.`V`Nếu`π`không thay đổi, trở lại  chúng ta ở mức tối ưu.

> sẽ`π`替换为对 `V`贪心的策略──如果 `π`Không thay đổi, trở lại chúng ta đã đạt được điểm tốt nhất.

```python
def policy_improvement(V, gamma=0.99):
    new_policy = {}
    for s in states():
        best_a = max(
            ACTIONS,
            key=lambda a: sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a)),
        )
        new_policy[s] = best_a
    return new_policy
```

### Bước 4: Thâu chúng lại với nhau

```python
def policy_iteration(gamma=0.99):
    policy = {s: "up" for s in states()}   # arbitrary start
    for _ in range(100):
        V = policy_evaluation(lambda s: {policy[s]: 1.0}, gamma)
        new_policy = policy_improvement(V, gamma)
        if new_policy == policy:
            return V, policy
        policy = new_policy
```

Sự hội tụ điển hình trên 4×4: 46 lặp lại bên ngoài.`V*(0,0) ≈ -6`và một chính sách cắt giảm nghiêm ngặt số bước.

> 4×4 上的典型收:4-6 次外层代──输出 `V*(0,0) ≈ -6`Và một chiến lược giảm số bước nghiêm ngặt.

### Bước 5: lặp lại giá trị (định dạng vòng một)

```python
def value_iteration(gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = max(sum(p * (r + gamma * V[s_prime])
                       for s_prime, r, p in transitions(s, a))
                   for a in ACTIONS)
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            break
    policy = policy_improvement(V, gamma)
    return V, policy
```

Điểm cố định giống nhau, ít dòng mã hơn.

> Tương tự không động điểm, ít hơn là số code.

## Những bẫy

- **Forgetting to handle terminals.**Nếu bạn áp dụng Bellman vào trạng thái hấp thụ, nó vẫn nhận được "các hành động tốt nhất" mà không thay đổi gì.`if s == terminal: V[s] = 0`- Tôi không biết.
  **忘记处理终止状态。**Nếu áp dụng Bellman cho tình trạng hấp thụ, nó vẫn sẽ chọn một động tác tốt nhất nhưng không có gì thay đổi.`if s == terminal: V[s] = 0`Bảo vệ
- **Sup-norm vs L2 convergence.**Sử dụng `max |V_new - V|`Chứng chỉ lý thuyết là trên chuẩn sup.
  **Sup 范数 vs L2 收敛。**Sử dụng `max |V_new - V|`, thay vì giá trị trung bình.
- **In-place vs synchronous updates.**Tới hạn `V[s]`trong chỗ (Gauss-Seidel) hội tụ nhanh hơn một tách biệt `V_new`Định nghĩa (Jacobi). mã sản xuất sử dụng tại chỗ.
  **原地更新 vs 同步更新。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `V[s]`(Gauss-Seidel) So với một đơn vị.`V_new`字典(Jacobi)收更快──生产代码使用原地更新──
- **Policy ties.**Nếu hai hành động có giá trị Q bằng nhau,`argmax`có thể phá vỡ các liên kết khác nhau mỗi lần lặp lại, khiến kiểm tra "chính sách ổn định" dao động. Sử dụng một liên kết ổn định (phản ứng đầu tiên theo thứ tự cố định).
  **策略平局。**Nếu hai động tác có giá trị Q 相等,`argmax`Mỗi lần có thể phá vỡ trục hình bằng cách khác nhau, dẫn đến "cách lược ổn định" kiểm tra振荡.
- **State-space explosion.**DP là `O(|S| · |A|)`Phương pháp này có thể được sử dụng cho các hoạt động khác nhau.
  **状态空间爆炸。**DP mỗi lần quét là`O(|S| · |A|)`△ được áp dụng cho khoảng 107 trạng thái.

## Hãy sử dụng nó để thực hiện

Năm 2026, DP là đường cơ sở chính xác và vòng lặp bên trong của các nhà hoạch định:

> Năm 2026, DP là một vòng tròn trong cơ sở chính xác và lập kế hoạch:

| Use case | Method |
|----------|--------|
| Use case / 用例 | Method / 方法 |
| Solve a small tabular MDP exactly / 精确求解小型表格 MDP | Value iteration (simpler) or policy iteration (fewer outer steps) / 值迭代（更简单）或策略迭代（更少外层步数） |
| Verify a Q-learning / PPO implementation / 验证 Q-learning/PPO 实现 | Compare to DP-optimal V* on a toy environment / 在玩具环境上与 DP 最优 V* 比较 |
| Model-based RL (Phase 9 · 10) / 基于模型的 RL | Bellman backup on a learned transition model / 在学习的转移模型上做 Bellman 备份 |
| Planning in AlphaZero / MuZero / AlphaZero/MuZero 中的规划 | Monte Carlo Tree Search = async Bellman backup / MCTS = 异步 Bellman 备份 |
| Offline RL (CQL, IQL) / 离线 RL | Conservative Q-iteration — DP with a penalty on OOD actions / 保守 Q 迭代——对 OOD 动作加惩罚的 DP |

Mỗi khi ai đó nói "động lực giá trị tối ưu", họ có nghĩa là "điểm cố định DP".`V*`hoặc `Q*`trong một tờ báo, hình dung vòng lặp này.

> Mỗi khi ai đó nói "động lực tối ưu nhất", họ chỉ ra "DP không động điểm"── khi bạn thấy trong bài luận `V*`Hoặc`Q*`时, tưởng tượng vòng lặp này

## Chuyển nó đi.

Cứ như `outputs/skill-dp-solver.md`- Có thể là:

```markdown
---
name: dp-solver
description: Solve a small tabular MDP exactly via policy iteration or value iteration. Report convergence behavior.
version: 1.0.0
phase: 9
lesson: 2
tags: [rl, dynamic-programming, bellman]
---

Given an MDP with a known model, output:

1. Choice. Policy iteration vs value iteration. Reason tied to |S|, |A|, γ.
2. Initialization. V_0, starting policy. Convergence sensitivity.
3. Stopping. Sup-norm tolerance ε. Expected number of sweeps.
4. Verification. V*(s_0) computed exactly. Greedy policy extracted.
5. Use. How this baseline will be used to debug/evaluate sampling-based methods.

Refuse to run DP on state spaces > 10⁷. Refuse to claim convergence without a sup-norm check. Flag any γ ≥ 1 on an infinite-horizon task as a guarantee violation.
```

## Tập luyện bài tập

1. **Easy.**Tiến đổi giá trị chạy trên GridWorld 4×4 với `γ ∈ {0.9, 0.99}`- Bao nhiêu lần quét cho đến khi`max |ΔV| < 1e-6`?`V*`như một lưới 4x4.
   > **练习1：**Sử dụng các yếu tố giảm giá khác nhau, xem tốc độ nhận thay đổi như thế nào.
2. **Medium.**So sánh lặp lại chính sách so với lặp lại giá trị trên GridWorld (slip probability `0.1` Số: quét, giờ tường, cuối cùng `V*(0,0)`- Cái nào hội tụ nhanh hơn trong các lần lặp lại?
   > **练习2：**So sánh chiến lược 代和值 代在随机网格世界中的收速度 ((代次数和运行时间) 
3. **Hard.**Xây dựng lặp lại chính sách sửa đổi: trong bước đánh giá, chỉ chạy `k`Trải qua thay vì hội tụ.`V*(0,0)`lỗi vs `k`cho `k ∈ {1, 2, 5, 10, 50}`- Hẻo cong cho bạn biết gì về sự đổi giá/ cải thiện?
   > **练习3：**Thực hiện các chiến lược sửa đổi (代) 评估步只代 k 次), tìm kiếm đánh giá chính xác và hiệu quả cải tiến.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy iteration | "DP algorithm" / 策略迭代 | Alternating evaluation (`V^π`) and improvement (greedy `π` w.r.t. `V^π`) until the policy stops changing. |
| Value iteration | "Faster DP" / 值迭代 | Bellman optimality backup applied in one sweep; converges to `V*` geometrically. |
| Bellman operator | "The recursion" / Bellman 算子 | `(T V)(s) = max_a Σ P (r + γ V(s'))`; a `γ`-contraction in sup-norm. |
| Contraction | "Why DP converges" / 压缩映射 | Any operator `T` with `\|\|T x - T y\|\| ≤ γ \|\|x - y\|\|` has a unique fixed point. |
| GPI | "Everything is DP" / 广义策略迭代 | Generalized Policy Iteration: any method driving `V` and `π` to mutual consistency. |
| Synchronous update | "Jacobi-style" / 同步更新 | Use old `V` throughout a sweep; cleanly analyzable but slower. |
| In-place update | "Gauss-Seidel-style" / 原地更新 | Use `V` as it's being updated; converges faster in practice. |

## Xem thêm 延伸阅读

- [Sutton & Barto (2018). Ch. 4 — Dynamic Programming](http://incompleteideas.net/book/RLbook2020.pdf) trình bày theo quy định của sự lặp lại chính sách và sự lặp lại giá trị.
- [Bertsekas (2019). Reinforcement Learning and Optimal Control](http://www.athenasc.com/rlbook.html) xử lý nghiêm ngặt các lập luận lập bản đồ thu hẹp.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887) Phác thảo chính sách đã được sửa đổi và phân tích sự hội tụ của nó.
- [Howard (1960). Dynamic Programming and Markov Processes](https://mitpress.mit.edu/9780262582300/dynamic-programming-and-markov-processes/) giấy lặp lại chính sách ban đầu.
- [Bertsekas & Tsitsiklis (1996). Neuro-Dynamic Programming](http://www.athenasc.com/ndpbook.html) cầu từ DP đến khoảng-DP / RL sâu được sử dụng trong mỗi bài học tiếp theo.
