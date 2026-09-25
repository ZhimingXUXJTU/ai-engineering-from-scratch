# Đạo diễn-Tác giả  A2C và A3C 演员-评论 viên  A2C và A3C

> Đăng lực là tiếng ồn.`V̂(s)`A2C chạy nó đồng bộ; A3C chạy nó qua các chuỗi. Cả hai đều là mô hình tâm lý cho mọi phương pháp RL sâu hiện đại.

> **【中文解读】**REINFORCE 方差太大──加入一个"评论家"(Critic)学习 V̂((s), sử dụng nó như một cơ sở xây dựng các hàm ưu thế A = G - V̂(s), kỳ vọng không thay đổi nhưng方差 giảm đáng kể── đây là Actor-CriticPPO、SAC 等 tất cả các mô hình nguyên bản của phương pháp RL độ sâu hiện đại──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 04 (TD Learning), Phase 9 · 06 (REINFORCE) | **前置知识:** Phase 9 · 04 (TD 学习), Phase 9 · 06 (REINFORCE)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Vanilla ReINFORCE có hiệu quả, nhưng sự khác biệt của nó là khủng khiếp.`G_t`có thể dao động qua một nhân tố 10 giữa các tập.`∇ log π`và trung bình tạo ra một ước tính gradient mất hàng ngàn tập để di chuyển chính sách cùng khoảng cách bạn có thể di chuyển nó với nhiều hơn cập nhật DQN.

> Động lực đầu tiên có hiệu quả, nhưng sự khác biệt rất tồi tệ.`G_t`Trong vòng hợp tác có thể biến động 10 lần.`∇ log π`Một lần nữa, các máy đánh giá độ cao được tạo ra cần hàng ngàn lần để di chuyển chiến lược với nhiều DQN hơn để đạt được hiệu quả tương tự.

Sự khác biệt xuất phát từ việc sử dụng các lợi nhuận nguyên liệu. Nếu bạn trừ một đường cơ bản `b(s_t)` bất kỳ hàm nào của trạng thái, bao gồm cả một giá trị được học  kỳ vọng không thay đổi và sự biến đổi giảm.`V̂(s_t)`Bây giờ số lượng nhân`∇ log π`là lợi thế:

`A(s, a) = G - V̂(s)`

> 方差来自使用原始回报──如果减基线 `b(s_t)` bất kỳ hàm trạng thái nào, bao gồm giá trị học  kỳ vọng không thay đổi nhưng tỷ lệ chênh lệch giảm.`V̂(s_t)`     `∇ log π`量就是优势

Một hành động là tốt nếu nó tạo ra lợi nhuận trên mức trung bình; xấu nếu dưới. REINFORCE với một nhà phê bình học tập là *actor-critic*. Nhà phê bình cho diễn viên một giáo viên biến thể thấp. Đây là mọi phương pháp chính sách sâu sắc sau năm 2015 (A2C, A3C, PPO, SAC, IMPALA).

> 动作好如果产生高于平均的回报;差如果低于──带学习批评的 REINFORCE就是 *Actor-Critic*──Critic 给 Actor一个低方差的老师──这是2015年后每个深度策略方法(A2C、A3C、PPO、SAC、IMPALA)──

## Khái niệm cốt lõi

![Actor-critic: policy net plus value net, TD residual as advantage](../assets/actor-critic.svg)

**Two networks, one shared loss:**

> **两个网络，一个共享损失：**

- **Actor** `π_θ(a | s)`Các nhà nghiên cứu đã được đào tạo để làm việc.
  **Actor** `π_θ(a | s)`: chiến lược. 采样以行动. 采用策略梯度训练.
- **Critic** `V_φ(s)`: ước tính dự kiến thu hồi từ nhà nước.`(V_φ(s) - target)²`- Tôi không biết.
  **Critic** `V_φ(s)`: ước tính xuất phát từ trạng thái kỳ vọng báo cáo.`(V_φ(s) - target)²`

**The advantage.**Hai mẫu tiêu chuẩn:

> **优势函数。**两种标准形式:

- *Lợi thế MC:* `A_t = G_t - V_φ(s_t)`Không thiên vị, sự khác biệt cao hơn.
  *MC 优势:* 无偏,方差较高──
- *Lợi thế TD:* `A_t = r_{t+1} + γ V_φ(s_{t+1}) - V_φ(s_t)`. Nhận định (sử dụng)`V_φ`), sự biến động thấp hơn nhiều.`δ_t`- Tôi không biết.
  *TD 优势:* 有偏差(使用 `V_φ`),方差远低──也称为 *TD残差* `δ_t`

**n-step advantage.**Chuyển đổi giữa hai:

`A_t^{(n)} = r_{t+1} + γ r_{t+2} + … + γ^{n-1} r_{t+n} + γ^n V_φ(s_{t+n}) - V_φ(s_t)`

`n = 1`là TD tinh khiết. `n = ∞`là MC. Hầu hết các thực hiện sử dụng `n = 5`cho Atari, `n = 2048`cho PPO trên MuJoCo.

> **n 步优势。**Trong hai giá trị giữa hai.`n = 1`Đó là một TD.`n = ∞`Đó là MC. Phần lớn các ứng dụng được Atari sử dụng.`n = 5`, MuJoCo trên của PPO sử dụng `n = 2048`

**Generalized Advantage Estimation (GAE).**Schulman et al. (2016) đề xuất một trung bình cân nặng theo tỷ lệ theo số lượng lớn trên tất cả các lợi thế của n- bước:

`A_t^{GAE} = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}`

với `λ ∈ [0, 1]`- `λ = 0`là TD (varian thấp, thiên vị cao). `λ = 1`là MC (trang độ cao, không thiên vị). `λ = 0.95`là âm thanh mặc định 2026  cho đến khi số số bias / biến số là nơi bạn muốn nó.

> **【中文解读】**GAE(广义优势估算) là cải tiến quan trọng của Actor-Critic: thông qua chỉ số tăng权平均所有 n 步优势, tìm thấy sự cân bằng tốt nhất giữa偏差和方差.

> **【拓展：GAE 在 RLHF 中的应用】**ChatGPT của PPO  đào tạo sử dụng GAE 计算优势函数。 trong trường hợp LLM, " trạng thái " là chuỗi token đã được tạo ra, " động作" là token tiếp theo, "奖励" từ mô hình thưởng。GAE 让 PPO 能在长文本生成(100 token) trong đào tạo ổn định, cân bằng ngay lập tức thưởng và dài hạn回报。

**A2C: synchronous advantage actor-critic.**Thu thập`T`bước qua `N`Các môi trường song song tính lợi thế cho mỗi bước cập nhật diễn viên và nhà phê bình trên loạt kết hợp lặp lại.

> **A2C：同步优势 Actor-Critic。**Trong `N`个并行环境中收集 `T`步──计算每步优势──在合并批次上更新 Actor 和 Critic──重复──A3C 的更简单、更可扩展的兄弟──

**A3C: asynchronous advantage actor-critic.**Mnih et al. (2016). Spawn `N`Các work thread, mỗi người chạy một env. Mỗi worker tính toán gradient tại địa phương trên bản triển khai của riêng mình, sau đó áp dụng chúng theo cách không đồng bộ cho một máy chủ tham số chia sẻ. Không cần bộ đệm lặp lại  nhân viên giải khớp bằng cách chạy các quỹ đạo khác nhau. A3C chứng minh bạn có thể đào tạo trên CPU ở quy mô. Năm 2026, A2C dựa trên GPU (batched parallel envs) thống trị vì GPUs muốn các lô lớn.

> **A3C：异步优势 Actor-Critic。**Mnih 等人 (2016) 启动`N`个工作线程, mỗi运行一个环境―― mỗi work线程在本地计算梯度,然后分步应用到共享参数服务器――不需要回放缓冲区工作线程通过运行不同轨迹来相关――2026年, dựa trên GPU A2C chiếm ưu thế, vì GPU 需要大量――

**The combined loss.**

`L(θ, φ) = -E[ A_t · log π_θ(a_t | s_t) ]  +  c_v · E[(V_φ(s_t) - G_t)²]  -  c_e · E[H(π_θ(·|s_t))]`

Ba điều khoản: lỗ theo mức chính sách, sự lùi giá trị, tiền thưởng entropy. `c_v ~ 0.5`- `c_e ~ 0.01`là các điểm khởi đầu theo luật pháp.

> **组合损失。**3 mục: Chiến lược mất mát giá trị trở lại  Giải thưởng`c_v ~ 0.5``c_e ~ 0.01`Đó là giá trị khởi điểm điển hình.

> **【中文解读】**Khối thấu trúc của Actor-Critic = 策略梯度损失 + 值函数归归 + 正则化──Thês三分别对应:

> **【拓展：GAE→PPO→RLHF】**GAE (广义优势估算) là thành phần cốt lõi của PPO, còn PPO là thuật toán tiêu chuẩn của ChatGPT RLHF 训练――λ=0.95 là giá trị mặc định năm 2026, để đạt được sự cân bằng giữa sự phân biệt và sự phân biệt.

## Hãy xây dựng nó.
```figure
actor-critic
```

## Hãy xây dựng nó

### Bước 1: một nhà phê bình

Nhận xét tuyến tính`V_φ(s) = w · features(s)`được cập nhật với MSE:

```python
def critic_update(w, x, target, lr):
    v_hat = dot(w, x)
    err = target - v_hat
    for j in range(len(w)):
        w[j] += lr * err * x[j]
    return v_hat
```

Trên một bảng xếp hạng, nhà phê bình hội tụ trong vài trăm tập. trên Atari, thay thế nhà phê bình tuyến tính bằng một shared CNN trunk + value head.

> 线性批评 `V_φ(s) = w · features(s)`Sử dụng MSE 更新──在表格环境中几百回合就收──在 Atari 上, thay thế cho chia sẻ CNN 主干 + 值头──

### Bước 2: lợi thế n- bước

Với một sự triển khai dài `T`và một trận chung kết không được khởi động `V(s_T)`- Có thể là:

```python
def compute_advantages(rewards, values, gamma=0.99, lam=0.95, last_value=0.0):
    advantages = [0.0] * len(rewards)
    gae = 0.0
    for t in reversed(range(len(rewards))):
        next_v = values[t + 1] if t + 1 < len(values) else last_value
        delta = rewards[t] + gamma * next_v - values[t]
        gae = delta + gamma * lam * gae
        advantages[t] = gae
    returns = [a + v for a, v in zip(advantages, values)]
    return advantages, returns
```

`returns`là mục tiêu của những người phê bình.`advantages`là điều nhân lên.`∇ log π`- Tôi không biết.

> `returns`Là mục tiêu phê bình.`advantages`là乘以`∇ log π`

### Bước 3: cập nhật kết hợp

```python
for step_i, (x, a, _r, probs) in enumerate(traj):
    adv = advantages[step_i]
    target_v = returns[step_i]

    # critic
    critic_update(w, x, target_v, lr_v)

    # actor
    for i in range(N_ACTIONS):
        grad_logpi = (1.0 if i == a else 0.0) - probs[i]
        for j in range(N_FEAT):
            theta[i][j] += lr_a * adv * grad_logpi * x[j]
```

Chính sách, một lần phát hành mỗi bản cập nhật, tỷ lệ học tập riêng biệt cho diễn viên và nhà phê bình.

> Trong khi đó, các nhà diễn viên và nhà phê bình sử dụng tỷ lệ học khác nhau.

### Bước 4: Phối tương đồng (A3C vs A2C)

- **A3C:**quay lên `N`mỗi bộ chạy bản xoay của riêng mình và thông qua phía trước của riêng mình. định kỳ đẩy cập nhật gradient để một chủ shared. Không khóa trên chủ  đua là ok, họ chỉ thêm tiếng ồn.
- **A2C:**chạy`N`Env các trường hợp trong một quá trình, xếp các quan sát thành một `[N, obs_dim]`Lượng lớn hơn, tính toán xác định, dễ lý luận hơn.

Mã đồ chơi của chúng tôi là một sợi đơn cho sự rõ ràng; viết lại cho A2C đúc là ba dòng numpy.

> Mã đồ chơi của chúng tôi là một đường để giữ độ rõ ràng; viết lại cho số lượng A2C chỉ cần ba dòng numpy.

## Những bẫy

- **Critic bias before actor gradient.**Nếu nhà phê bình là ngẫu nhiên, cơ sở của nó là không thông tin và bạn đang tập luyện trên tiếng ồn thuần túy. Đáp ấm nhà phê bình trong vài trăm bước trước khi bật gradient chính sách, hoặc sử dụng tốc độ học tập diễn viên chậm.
  **Actor 梯度之前的 Critic 偏差。**Nếu chỉ trích là tự nhiên, không có thông tin, bạn tập luyện trên tiếng ồn thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh thanh
- **Advantage normalization.**Tiêu chuẩn hóa lợi thế cho số trung bình / đơn vị / std mỗi lô.
  **优势归一化。**Mỗi lô sẽ được phân tích thành 0 trung bình/ đơn vị tiêu chuẩn khác biệt.
- **Shared trunk.**Sử dụng bộ thu thập tính năng chung cho diễn viên và nhà phê bình trên đầu vào hình ảnh. Đầu tách biệt. Các tính năng chung tự lái trên cả hai lỗ.
  **共享主干。**图像输入时使用共享特征提取器──分开的头──共享特征同时从两个损失中获益──
- **On-policy contract.**A2C sử dụng lại dữ liệu cho chính xác một bản cập nhật. Nhiều hơn và gradient của bạn bị thiên vị (chính xác lấy mẫu quan trọng là điều PPO thêm vào).
  **在线策略约束。**A2C 恰好用数据做一次更新.
- **Entropy collapse.**Không có`c_e > 0`, chính sách trở nên gần như quyết định trong vài trăm cập nhật và ngừng khám phá.
  **熵坍缩。**Không có gì`c_e > 0`, chiến lược sau vài trăm lần cập nhật biến đổi gần như xác định và ngừng khám phá.
- **Reward scale.**Tầm quan trọng lợi thế phụ thuộc vào quy mô phần thưởng. bình thường hóa phần thưởng (ví dụ, chia run-std) cho độ lớn gradient phù hợp giữa các nhiệm vụ.
  **奖励尺度。**Ưu điểm của cấp độ phụ thuộc vào mức độ thưởng                                                                                                                                                                                                                                                         

## Hãy sử dụng nó để thực hiện

A2C/A3C hiếm khi là lựa chọn cuối cùng vào năm 2026 nhưng chúng là kiến trúc mọi thứ sau đó tinh chỉnh:

> A2C/A3C trong năm 2026 ít khi là lựa chọn cuối cùng, nhưng chúng sau đó là cấu trúc tinh tế của tất cả các phương pháp:

| Method | Relation to A2C |
|--------|----------------|
| Method / 方法 | Relation to A2C / 与 A2C 的关系 |
| PPO | A2C + clipped importance ratio for multi-epoch updates / A2C + 裁剪重要性比率用于多轮更新 |
| IMPALA | A3C + V-trace off-policy correction / A3C + V-trace 离策略修正 |
| SAC (Phase 9 · 07) | Off-policy A2C with a soft-value critic (next lesson) / 离策略 A2C + 软值 Critic |
| GRPO (Phase 9 · 12) | A2C without the critic — group-relative advantage / 无 Critic 的 A2C——组相对优势 |
| DPO | A2C collapsed into a preference-ranking loss, no sampling / 折叠为偏好排名损失的 A2C |
| AlphaStar / OpenAI Five | A2C with league training + imitation pre-training / A2C + 联盟训练 + 模仿预训练 |

Nếu bạn thấy "lợi thế" trong một bài báo năm 2026, hãy nghĩ đến nhà phê bình diễn viên.

> Nếu bạn thấy "Lợi thế" trong bài viết năm 2026, hãy nghĩ đến Nhà phê bình diễn viên.

## Chuyển nó đi.

Cứ như `outputs/skill-actor-critic-trainer.md`- Có thể là:

```markdown
---
name: actor-critic-trainer
description: Produce an A2C / A3C / GAE configuration for a given environment, with advantage estimation and loss weights specified.
version: 1.0.0
phase: 9
lesson: 7
tags: [rl, actor-critic, gae]
---

Given an environment and compute budget, output:

1. Parallelism. A2C (GPU batched) vs A3C (CPU async) and the number of workers.
2. Rollout length T. Steps per env per update.
3. Advantage estimator. n-step or GAE(λ); specify λ.
4. Loss weights. `c_v` (value), `c_e` (entropy), gradient clip.
5. Learning rates. Actor and critic (separate if using).

Refuse single-worker A2C on environments with horizon > 1000 (too on-policy, too slow). Refuse to ship without advantage normalization. Flag any run with `c_e = 0` and observed entropy < 0.1 as entropy-collapsed.
```

## Tập luyện bài tập

1. **Easy.**Đào tạo diễn viên-chính trị với lợi thế MC (`G_t - V(s_t)`So sánh hiệu quả mẫu với REINFORCE-with-running-median-baseline từ bài học 06.
2. **Medium.**Chuyển sang lợi thế TD-`r + γ V(s') - V(s)`(Điều 1 - 2): đo sự khác biệt của các lô lợi thế.
3. **Hard.**Thực hiện GAE ((λ).`λ ∈ {0, 0.5, 0.9, 0.95, 1.0}`Phản hồi cuối cùng của bản đồ so với hiệu quả mẫu.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Actor | "The policy net" / 演员（策略网络） | `π_θ(a\|s)`, updated by policy gradient. |
| Critic | "The value net" / 评论家（值网络） | `V_φ(s)`, updated by MSE regression to returns / TD targets. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = Q(s, a) - V(s)` or its estimators. Multiplier for `∇ log π`. |
| TD residual | "δ" / TD 残差 | `δ_t = r + γ V(s') - V(s)`; one-step advantage estimate. |
| GAE | "The interpolation knob" / 广义优势估计 | Exponentially weighted sum of n-step advantages, parameterized by `λ`. |
| A2C | "Synchronous actor-critic" / 同步演员-评论家 | Batched across envs; one gradient step per rollout. |
| A3C | "Async actor-critic" / 异步演员-评论家 | Worker threads push gradients to a shared param server. Original paper; less common in 2026. |
| Bootstrap | "Use V at the horizon" / 自举截断 | Truncate the rollout, add `γ^n V(s_{t+n})` to close the sum. |

## Xem thêm 延伸阅读

- [Mnih et al. (2016). Asynchronous Methods for Deep Reinforcement Learning](https://arxiv.org/abs/1602.01783) A3C, bài báo phê bình diễn viên đồng bộ ban đầu.
- [Schulman et al. (2016). High-Dimensional Continuous Control Using Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438) GAE.
- [Sutton & Barto (2018). Ch. 13 — Actor-Critic Methods](http://incompleteideas.net/book/RLbook2020.pdf) nền tảng; kết hợp điều này với chương 9 về việc gần gũi chức năng khi người phê bình là một mạng thần kinh.
- [Espeholt et al. (2018). IMPALA](https://arxiv.org/abs/1802.01561) có thể mở rộng phân phối các nhà phê bình diễn viên với sự sửa đổi ngoài chính sách theo dấu vết V.
- [OpenAI Baselines / Stable-Baselines3](https://stable-baselines3.readthedocs.io/) thực hiện A2C/PPO đáng đọc.
- [Konda & Tsitsiklis (2000). Actor-Critic Algorithms](https://papers.nips.cc/paper/1786-actor-critic-algorithms) kết quả hội tụ cơ bản cho sự phân hủy hai thang điểm diễn viên-nhân trọng.
