# Chính sách cấp độ  REINFORCE từ đầu  策略梯度  Từ zero thực hiệnREINFORCE

> Giữ các parameter chính sách trực tiếp, tính toán gradient của lợi nhuận dự kiến, bước lên. Williams (1992) đã viết nó trong một định lý. Đó là lý do tại sao PPO, GRPO và mỗi vòng LLM RL tồn tại.

> **【中文解读】**Không tái ước tính giá trị hàm, trực tiếp参数化策略 π_θ(a s), tính toán kỳ vọng trả giá từ thang và thang lên.`∇J(θ) = E[G · ∇log π_θ(a|s)]`Đây là lý do tại sao PPO, GRPO và tất cả các mô hình RL tập trung vòng lặp tồn tại.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 03 (Monte Carlo), Phase 9 · 04 (TD Learning) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 03 (蒙特卡洛), Phase 9 · 04 (TD 学习)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Q-learning và DQN tham số chức năng *value*. Bạn chọn các hành động bằng `argmax Q`Nó tốt cho các hành động riêng biệt và các trạng thái riêng biệt. nó phá vỡ khi các hành động liên tục (mà là`argmax`trên mô-men xoắn 10 chiều?) hoặc khi bạn muốn một chính sách stochastic (`argmax`là xác định theo cấu trúc).

> Q-learning 和 DQN 参数化*值* hàm──通过 `argmax Q`选择动作──这对离散动作和离散状态没有问题──但当动作连续时(10维力矩上取哪个 `argmax`?) hoặc cần theo chiến lược`argmax`Thiên nhiên là chắc chắn), đã sụp đổ.

Các gradient chính sách thay vào đó là các tham số của chính sách. `π_θ(a | s)`là một mạng thần kinh phát ra phân phối trên các hành động.`θ`- Đi lên đồi.`argmax`Không có sự tái phát Bellman, chỉ là tăng độ ở trên`J(θ) = E_{π_θ}[G]`- Tôi không biết.

> 策略梯度改为参数化*策略*`π_θ(a | s)`là một mạng lưới phân phối động tác xuất phát.`θ`                                                                                                                                                                                                                                                              `argmax`Không cần Bellman 递推.`J(θ) = E_{π_θ}[G]`Ưu làm thang lên Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu Ưu

Các định lý REINFORCE (Williams 1992) nói với bạn gradient này là tính toán: `∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`- Đánh ra một tập, tính toán lại, nhân bằng`∇ log π_θ(a | s)`- Tỷ lệ trung bình, tăng độ, xong rồi.

> (Williams 1992) cho chúng ta biết mức độ này có thể tính toán được:`∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`◊运行一个回合――计算回报――每步乘以 `∇ log π_θ(a | s)`取平均──梯度上升──完成──

Mỗi thuật toán LLM-RL vào năm 2026  PPO, DPO, GRPO  là một sự tinh tế của REINFORCE.

> 2026 mỗi LLM-RL 算法PPO、DPO、GRPO là sự tinh tế của REINFORCE.

> **【中文解读】**策略梯度的核心思想: trực tiếp tối ưu hóa các参数策略 θ,让高回报的动作概率增加大,低回报的动作概率减少小.`∇log π`Đó là "đường hướng của chiến lược", nhân bằng báo cáo G đó là "đối với hướng tốt".

> **【拓展：PPO→ChatGPT对齐】**ChatGPT của RLHF  luyện tập sử dụng PPO  thuật toán, bản chất là REINFORCE + phê bình 基线 + 信赖域剪.`loss = -advantage * log_prob`Đây là một dòng mã, xuất hiện gần như tất cả các mô hình lớn RL năm 2026 trong các bản thảo đào tạo.

## Khái niệm cốt lõi

![Policy gradient: softmax policy, log-π gradient, return-weighted update](../assets/policy-gradient.svg)

**The policy gradient theorem.**Đối với bất kỳ chính sách nào `π_θ`được định đo bởi `θ`- Có thể là:

`∇J(θ) = E_{τ ~ π_θ}[ Σ_{t=0}^{T} G_t · ∇_θ log π_θ(a_t | s_t) ]`

nơi `G_t = Σ_{k=t}^{T} γ^{k-t} r_{k+1}`là lợi nhuận giảm giá từ bước `t`- Sự kỳ vọng đã vượt qua quỹ đạo đầy đủ.`τ`lấy mẫu từ `π_θ`- Tôi không biết.

> **策略梯度定理。**Đối với bất cứ điều gì`θ`Chiến lược số hóa`π_θ`, kỳ vọng về lợi nhuận bằng: giảm giá về lợi nhuận và nhân với kỳ vọng về lợi nhuận về các chiến lược số.`π_θ`采样完整轨迹上取──

**The proof is short.**Sự khác biệt `J(θ) = Σ_τ P(τ; θ) G(τ)`dưới sự mong đợi.`∇P(τ; θ) = P(τ; θ) ∇ log P(τ; θ)`(cánh chánh dẫn log).`log P(τ; θ) = Σ log π_θ(a_t | s_t) + environment terms that do not depend on θ`Hai dòng đại số cho bạn định lý.

> **证明很短。**Trong kỳ vọng`J(θ)`求导――使用对数导数技巧――将 `log P(τ; θ)`Các phân giải cho các chiến lược và môi trường.

**Variance reduction tricks.**Vanilla REINFORCE có sự khác biệt giết người  trả lại là tiếng ồn, `∇ log π`là tiếng ồn, sản phẩm của họ rất tiếng ồn. Hai sửa chữa tiêu chuẩn:

> **方差降低技巧。**Động lực đầu tiên có rất nhiều sự khác biệt.`∇ log π`Có tiếng ồn, số lượng tiếng ồn của chúng lớn hơn.

1. **Baseline subtraction.**Thay thế `G_t`với `G_t - b(s_t)`cho bất kỳ đường cơ sở nào `b(s_t)`không phụ thuộc vào `a_t`Không thiên vị bởi vì`E[b(s_t) · ∇ log π(a_t | s_t)] = 0`. Sự lựa chọn điển hình: `b(s_t) = V̂(s_t)`học được bởi một nhà phê bình → diễn viên-chính giả (Lớp 07).
   **基线减法。**用 `G_t - b(s_t)`替换 `G_t`❖ 典型选择:`b(s_t) = V̂(s_t)`由 phê bình 学习 → Đạo diễn-T phê bình (Lớp 07):
2. **Reward-to-go.**Thay thế `Σ_t G_t · ∇ log π_θ(a_t | s_t)`với `Σ_t G_t^{from t} · ∇ log π_θ(a_t | s_t)`Chỉ có lợi nhuận trong tương lai là quan trọng cho một hành động nhất định  phần thưởng trong quá khứ đóng góp tiếng ồn không trung bình.
   **未来回报。**Chỉ có những phản hồi trong tương lai về những động tác nhất định có ý nghĩa  đóng góp phần thưởng trong quá khứ 零 trung bình 

Kết hợp, bạn có được:

`∇J ≈ (1/N) Σ_{i=1}^{N} Σ_{t=0}^{T_i} [ G_t^{(i)} - V̂(s_t^{(i)}) ] · ∇_θ log π_θ(a_t^{(i)} | s_t^{(i)})`

là REINFORCE với một đường cơ sở  tổ tiên trực tiếp của A2C (Sự học 07) và PPO (Sự học 08).

**Softmax policy parameterization.**Đối với các hành động riêng biệt, lựa chọn tiêu chuẩn:

`π_θ(a | s) = exp(f_θ(s, a)) / Σ_{a'} exp(f_θ(s, a'))`

nơi `f_θ`là bất kỳ mạng thần kinh nào đưa ra điểm số cho mỗi hành động.

`∇_θ log π_θ(a | s) = ∇_θ f_θ(s, a) - Σ_{a'} π_θ(a' | s) ∇_θ f_θ(s, a')`

tức là điểm số của các hành động đã thực hiện trừ giá trị dự kiến của nó trong chính sách.

> **Softmax 策略参数化。**Đối với các động tác phân chia, gradiente forma简洁: số lượng động tác được thực hiện giảm giá trị dự kiến dưới các chiến lược trừ.

**Gaussian policy for continuous actions.** `π_θ(a | s) = N(μ_θ(s), σ_θ(s))`- `∇ log N(a; μ, σ)`có một hình thức đóng. Đó là tất cả các nhu cầu của SAC giai đoạn 9 · 07

> **连续动作的高斯策略。** `∇ log N(a; μ, σ)`Có giải pháp kết thúc. Đó là tất cả những gì cần thiết cho SAC trong giai đoạn 9 · 07.

## Hãy xây dựng nó.
```figure
policy-gradient-landscape
```

## Hãy xây dựng nó

### Bước 1: mạng chính sách softmax

```python
def policy_logits(theta, state_features):
    return [dot(theta[a], state_features) for a in range(N_ACTIONS)]

def softmax(logits):
    m = max(logits)
    exps = [exp(l - m) for l in logits]
    Z = sum(exps)
    return [e / Z for e in exps]
```

Sử dụng chính sách tuyến tính (một vector trọng lượng mỗi hành động) cho một bảng bao gồm. Đối với Atari, thay đổi trong một CNN và giữ đầu softmax.

> 表格环境使用线性策略(每个动作一个权重向量) ・・・ đối với Atari, chuyển vào CNN并保留软max 头――

### Bước 2: lấy mẫu và khả năng ghi chép

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

### Bước 3: triển khai với các log-probs được chụp

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

### Bước 4: Cập nhật REINFORCE

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

Tốc độ `∇ log π(a|s) = e_a - π(·|s)`(nhiều trong số đó là `a`- xác suất) là trung tâm của các gradient chính sách softmax.

> 梯度 `∇ log π(a|s) = e_a - π(·|s)`(`a`(được gọi là "đối đa" trong các mô hình khác nhau, nhưng không phải là "đối đa" trong các mô hình khác nhau.

### Bước 5: đường cơ sở

Một con số chạy của `G`hơn các tập gần đây là giảm độ biến số đủ để có được một 4 × 4 GridWorld chạy; nó mất ~ 500 tập để hội tụ. nâng cấp đường cơ sở đến một học `V̂(s)`và bạn có một nhà phê bình diễn viên.

> Gần đây `G`Giá trị trung bình hoạt động đủ để 4x4 GridWorld làm việc; khoảng 500 回合收──将基线升级为学习的`V̂(s)`Được nhận được bởi các nhà phê bình.

## Những bẫy

- **Exploding gradients.**Lợi nhuận có thể rất lớn.`G`đến`~N(0, 1)`qua lô trước khi nhân bằng `∇ log π`- Tôi không biết.
  **梯度爆炸。**Câu chuyện có thể rất lớn.`∇ log π`之前始终将 `G`归一化到 `~N(0, 1)`
- **Entropy collapse.**Chính sách hội tụ với một hành động gần như quyết định quá sớm, ngừng khám phá, bị mắc kẹt.`β · H(π(·|s))`đến mục tiêu.
  **熵坍缩。**策略过早收到近确定性动作,停止探索,陷入困境──修复:向目标添加奖励 `β · H(π(·|s))`
- **High variance.**Vanilla REINFORCE cần hàng ngàn tập phim. Một điểm cơ bản phê bình (Lớp 07) hoặc khu vực tin tưởng của TRPO/PPO (Lớp 08) là sự cố chuẩn.
  **高方差。**Định nghĩa của TRPO/PPO: Định nghĩa của TRPO/PPO: Định nghĩa của TRPO/PPO: Định nghĩa của TRPO
- **Sample inefficiency.**On-policy có nghĩa là bạn bỏ đi mọi chuyển đổi sau một cập nhật.
  **样本效率低。**Lưu ý trực tuyến có nghĩa là bỏ tất cả chuyển đổi sau mỗi lần cập nhật.
- **Non-stationary gradients.**Tương tự như 100 tập trước, dùng cũ.`π`Các phương pháp chính sách cập nhật mỗi vài lần triển khai vì lý do này.
  **非平稳梯度。**100 回合前的梯度使用旧的 `π`                                                                                                                                                                                                                                                              
- **Credit assignment.**Không có phần thưởng, phần thưởng trước đây sẽ gây tiếng ồn.
  **信用分配。**没有未来回报,过去的奖励贡献噪声──始终使用未来回报──

## Hãy sử dụng nó để thực hiện

Năm 2026, REINFORCE hiếm khi được chạy trực tiếp nhưng công thức gradient của nó là khắp nơi:

> Năm 2026, REINFORCE  rất ít hoạt động trực tiếp, nhưng các công thức của nó không có ở đâu cả:

| Use case | Derived method |
|----------|---------------|
| Use case / 用例 | Derived method / 派生方法 |
| Continuous control / 连续控制 | PPO / SAC with Gaussian policy / 高斯策略的 PPO/SAC |
| LLM RLHF / LLM RLHF | PPO with KL penalty, running on token-level policy / 带 KL 惩罚的 PPO，token 级策略 |
| LLM reasoning (DeepSeek) / LLM 推理 | GRPO — REINFORCE with group-relative baseline, no critic / 组相对基线的 REINFORCE，无 critic |
| Multi-agent / 多智能体 | Centralized-critic REINFORCE (MADDPG, COMA) / 集中 critic 的 REINFORCE |
| Discrete action robotics / 离散动作机器人 | A2C, A3C, PPO |
| Preference-only settings / 仅偏好设置 | DPO — REINFORCE rewritten as a preference-likelihood loss, no sampling / 重写为偏好似然损失的 REINFORCE |

Khi đọc`loss = -advantage * log_prob`trong một kịch bản đào tạo 2026 đó là REINFORCE với một đường cơ sở. Các bài báo toàn bộ (DPO, GRPO, RLOO) là thủ thuật giảm biến số trên đầu một dòng này.

> Khi bạn đọc trong bài tập năm 2026`loss = -advantage * log_prob`, đó là REINFORCE của带基线. 整篇论文 ((DPO、GRPO、RLOO) đều là những kỹ thuật giảm chênh lệch trên các mã này.

## Chuyển nó đi.

Cứ như `outputs/skill-policy-gradient-trainer.md`- Có thể là:

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

## Tập luyện bài tập

1. **Easy.**Thực hiện REINFORCE trên 4×4 GridWorld với chính sách mềm tối đa tuyến tính. Đào tạo cho 1.000 tập mà không có đường cơ sở. Chụp đường cong học tập; đo sự khác biệt (std của lợi nhuận).
2. **Medium.**Thêm một đường cơ sở trung bình chạy. Tập luyện lại. So sánh hiệu quả mẫu và sự khác biệt với đường chạy vani. đường cơ sở làm giảm bao nhiêu bước tiến sang hội tụ?
3. **Hard.**Thêm thêm một phần thưởng entropy `β · H(π)`- Tháo ra .`β ∈ {0, 0.01, 0.1, 1.0}`- Đâu là điểm tốt nhất trong nhiệm vụ này?

## Từ khóa  Từ khóa nhanh chóng

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

## Xem thêm 延伸阅读

- [Williams (1992). Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning](https://link.springer.com/article/10.1007/BF00992696) giấy REINFORCE ban đầu.
- [Sutton et al. (2000). Policy Gradient Methods for Reinforcement Learning with Function Approximation](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html) định lý chính sách-độ cấp hiện đại với sự gần gũi chức năng.
- [Sutton & Barto (2018). Ch. 13 — Policy Gradient Methods](http://incompleteideas.net/book/RLbook2020.pdf) trình bày sách giáo khoa.
- [OpenAI Spinning Up — VPG / REINFORCE](https://spinningup.openai.com/en/latest/algorithms/vpg.html) trình bày giáo dục rõ ràng với mã PyTorch.
- [Peters & Schaal (2008). Reinforcement Learning of Motor Skills with Policy Gradients](https://homes.cs.washington.edu/~todorov/courses/amath579/reading/PolicyGradient.pdf) Giảm biến số và quan điểm tự nhiên-đường độ kết nối REINFORCE với gia đình vùng tín thác (TRPO, PPO).
