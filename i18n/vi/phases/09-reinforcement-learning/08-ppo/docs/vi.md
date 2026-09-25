# Tích cực chính sách gần (PPO) 

> A2C ném đi mỗi rollout sau một bản cập nhật. PPO gói gradient chính sách trong một tỷ lệ quan trọng bị cắt giảm để bạn có thể làm 10+ thời đại trên cùng một dữ liệu mà không bị chính sách nổ. Schulman et al. (2017).

> **【中文解读】**PPO sử dụng tỷ lệ cắt giảm tầm quan trọng gói gọn các thuật toán, để các dữ liệu tương tự có thể được làm 10 lần cập nhật hơn và các chiến lược sẽ không nổ. Năm 2017 được đề xuất, cho đến nay vẫn là thuật toán thuật toán tiêu chuẩn của năm 2026:

> **【拓展：PPO 与 ChatGPT】**PPO là thuật toán cốt lõi của ChatGPT RLHF  đào tạo.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic) | **前置知识:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

A2C (Dạy học 07) là chính sách: gradient `E_{π_θ}[A · ∇ log π_θ]`yêu cầu dữ liệu lấy mẫu từ *current* `π_θ`Hãy cập nhật một lần, và`π_θ`thay đổi; dữ liệu mà bạn đã sử dụng bây giờ là không chính sách. sử dụng lại nó và gradient của bạn là thiên vị.

> A2C(Dạy học 07) là trên đường chiến lược của:梯度 `E_{π_θ}[A · ∇ log π_θ]`要求从*当前* `π_θ`采样数据──一次更新后 `π_θ`改变; bạn đã sử dụng dữ liệu đã trở thành một chiến lược.

Các rollout là đắt tiền. trên Atari, một rollout trên 8 envs × 128 bước = 1024 chuyển đổi và một chục giây thời gian môi trường. Thả đi sau một bước gradient là lãng phí.

> Việc triển khai rất đắt tiền. Trong Atari, 8 môi trường x 128 bước = 1024 lần chuyển đổi và 10 giây thời gian môi trường.

Tích cực chính sách khu vực tin cậy (TRPO, Schulman 2015) là sự khắc phục đầu tiên: hạn chế mỗi bản cập nhật để sự khác biệt KL giữa chính sách cũ và mới vẫn ở dưới `δ`Về lý thuyết sạch, nhưng đòi hỏi phải giải quyết các hàm kết hợp mỗi lần cập nhật.

> 信赖域策略优化(TRPO,Schulman 2015) là lần đầu tiên sửa đổi:约束每次更新使新旧策略的 KL 散度保持在`δ`Theo lý thuyết, nhưng mỗi lần cập nhật cần có sự đồng cấp để giải quyết.

PPO (Schulman et al. 2017) thay thế hạn chế khu vực tin tưởng cứng bằng một mục tiêu đơn giản. Một dòng mã thêm. Mười thời đại mỗi triển khai. Không có gradient kết hợp. Đảm bảo lý thuyết đủ tốt. Chín năm sau nó vẫn là thuật toán chính sách-gradient mặc định cho mọi thứ từ MuJoCo đến RLHF.

> PPO(Schulman 等人 2017) sử dụng mục tiêu cắt ngắn đơn giản để thay thế HardTrust Domain约束──多一行代码── mỗi lần triển khai 十个时代──不需要共梯度──足够好的理论保证──九年后它 vẫn còn là từ MuJoCo đến RLHF 所有任务的默认策略梯度算法──

> **【中文解读】**Cốt lõi của PPO: sử dụng cắt mục tiêu thay thế TRPO của cứng约束―― tầm quan trọng tỷ lệ r_t(theta) = pi_theta / pi_old 被剪到 [1-epsilon, 1+epsilon] 范围内──当优势 A_t>0 时,不将好动作概率推得太高;当A_t<0 时,不将坏动作概率降低太低──需要一行代码,就能安全地多次复制同一批数据──

> **【拓展：PPO 之外的选择——DPO 与 GRPO】**Mặc dù PPO vẫn là lựa chọn mặc định năm 2026, nhưng các thay thế đang nổi lên.

## Khái niệm cốt lõi

![PPO clipped surrogate objective: ratio clipping at 1 ± ε](../assets/ppo.svg)

**The importance ratio.**

`r_t(θ) = π_θ(a_t | s_t) / π_{θ_old}(a_t | s_t)`

Đây là tỷ lệ xác suất của chính sách mới so với chính sách thu thập dữ liệu. `r_t = 1`nghĩa là không có thay đổi.`r_t = 2`nghĩa là chính sách mới có khả năng gấp đôi`a_t`như cũ.

> **重要性比率。**Chiến lược mới và chiến lược thu thập dữ liệu tương tự như vậy.`r_t = 1`Không thay đổi.`r_t = 2`Tự động hóa`a_t`Có thể là gấp đôi chiến lược cũ.

**The clipped surrogate.**

`L^{CLIP}(θ) = E_t [ min( r_t(θ) A_t, clip(r_t(θ), 1-ε, 1+ε) A_t ) ]`

Hai điều khoản:

- Nếu lợi thế `A_t > 0`và tỷ lệ cố gắng tăng lên qua `1 + ε`, clip làm phẳng gradient  không đẩy một hành động tốt hơn `+ε`trên khả năng cũ.
- Nếu lợi thế `A_t < 0`và tỷ lệ cố gắng tăng lên qua `1 - ε`(có nghĩa là chúng ta sẽ làm cho một hành động xấu có khả năng hơn so với việc cắt giảm), clip                                                                                                                                                                                                                                                   `-ε`- Tôi không biết.

- `min`xử lý hướng khác: nếu tỷ lệ đã di chuyển theo hướng * hữu ích *, bạn vẫn nhận được độ nghiêng (không cắt trên mặt mà sẽ làm tổn thương bạn).

Thông thường`ε = 0.2`- Định hướng mục tiêu như một hàm của`r_t`: một chức năng tuyến tính theo mảnh với mái nhà phẳng trên "mặt tốt" và sàn phẳng trên "mặt xấu".

> **裁剪代理。**两项: Nếu lợi thế là đúng và tỷ lệ vượt quá `1 + ε`, cắt giảm làm cho độ cao thay đổi không làm cho động tác tốt hơn so với tỷ lệ cũ`+ε`更多── Nếu lợi thế là tiêu cực và tỷ lệ thấp hơn `1 - ε`, cắt giảm giới hạn mức độ không làm cho động tác xấu giảm xuống`-ε`更多──典型 `ε = 0.2`

> **【中文解读】**PPO  cắt cơ chế trực giác:epsilon=0.2 có nghĩa là chiến lược mỗi lần cập nhật thay đổi tối đa 20%── nếu một động tác tốt nhất ((A>0), tối đa sẽ tăng tỷ lệ 20%; nếu một động tác rất kém ((A<0), tối đa sẽ giảm 20%── điều này ngăn chặn "những thảm họa bị lãng quên" chiến lược sẽ không thay đổi quá lớn.

**The full PPO loss.**

`L(θ, φ) = L^{CLIP}(θ) - c_v · (V_φ(s_t) - V_t^{target})² + c_e · H(π_θ(·|s_t))`

Tương tự cấu trúc diễn viên-chính trị như A2C. Ba hệ số, thường `c_v = 0.5`- `c_e = 0.01`- `ε = 0.2`- Tôi không biết.

> **完整的 PPO 损失。**Hình cấu trúc-Critic Actor-Critic ∼3系数, thường `c_v = 0.5``c_e = 0.01``ε = 0.2`

**The training loop.**

1. Thu thập`N × T`chuyển đổi qua `N`các môi trường song song cho `T`từng bước.
2. Xét lợi thế (GAE), đóng băng chúng như là các định vị.
3. Đóng `π_{θ_old}`như một bức ảnh chụp của hiện tại `π_θ`- Tôi không biết.
4. Vì `K`các thời đại, cho mỗi mini batch của `(s, a, A, V_target, log π_old(a|s))`- Có thể là:
   - Lưu ý`r_t(θ) = exp(log π_θ(a|s) - log π_old(a|s))`- Tôi không biết.
   - Đơn `L^{CLIP}`+ mất giá trị + entropy.
   - Bước tiến.
5. Thả ra việc triển khai, quay lại bước 1.

`K = 10`và các bộ mini 64 là một bộ siêu tham số tiêu chuẩn. PPO là mạnh mẽ: các con số chính xác hiếm khi quan trọng trong ± 50%.

> **训练循环。**收集 → 计算 GAE 优势 → 结旧策略 → K 轮更新 → 丢弃数据──`K = 10`Và 64 của các lô nhỏ là tiêu chuẩn siêu参数──PPO  rất 鲁棒: giá trị cụ thể là ±50% trong thường không liên quan gì.

**KL-penalty variant.**Bài báo ban đầu đề xuất một lựa chọn thay thế bằng cách sử dụng một hình phạt KL thích nghi: `L = L^{PG} - β · KL(π_θ || π_old)`với `β`phiên bản cắt giảm trở nên thống trị; biến thể KL tồn tại trong RLHF (nơi KL đối với chính sách tham chiếu là một hạn chế riêng biệt bạn luôn muốn bất cứ lúc nào).

> **KL 惩罚变体。**Bài viết ban đầu đề xuất sử dụng tự thích ứng KL 惩罚 代替方案.

## Hãy xây dựng nó.
```figure
ppo-clip
```

## Hãy xây dựng nó

### Bước 1: bắt `log π_old(a | s)`tại thời điểm triển khai

```python
for step in range(T):
    probs = softmax(logits(theta, state_features(s)))
    a = sample(probs, rng)
    s_next, r, done = env.step(s, a)
    buffer.append({
        "s": s, "a": a, "r": r, "done": done,
        "v_old": value(w, state_features(s)),
        "log_pi_old": log(probs[a] + 1e-12),
    })
    s = s_next
```

Hình ảnh được chụp một lần, vào thời điểm triển khai. Nó không thay đổi trong thời gian cập nhật.

> 快照在 rollout 时拍摄一次──在更新时代 期间不变──

### Bước 2: tính toán lợi ích của GAE (Dạy học 07)

Tương tự như A2C. Thường hóa trên toàn bộ lô.

> Với A2C tương tự.

### Bước 3: Clip cập nhật thay thế

```python
for _ in range(K_EPOCHS):
    for mb in minibatches(buffer, size=64):
        for rec in mb:
            x = state_features(rec["s"])
            probs = softmax(logits(theta, x))
            logp = log(probs[rec["a"]] + 1e-12)
            ratio = exp(logp - rec["log_pi_old"])
            adv = rec["advantage"]
            surrogate = min(
                ratio * adv,
                clamp(ratio, 1 - EPS, 1 + EPS) * adv,
            )
            # backprop -surrogate, add value loss, subtract entropy
            grad_logpi = onehot(rec["a"]) - probs
            if (adv > 0 and ratio >= 1 + EPS) or (adv < 0 and ratio <= 1 - EPS):
                pg_grad = 0.0  # clipped
            else:
                pg_grad = ratio * adv
            for i in range(N_ACTIONS):
                for j in range(N_FEAT):
                    theta[i][j] += LR * pg_grad * grad_logpi[i] * x[j]
```

Mô hình "cắt → gradient không" là cốt lõi của PPO. Nếu chính sách mới đã trôi xa quá xa theo hướng có lợi, việc cập nhật sẽ dừng lại.

> Mô hình " cắt cắt → 零梯度" là cốt lõi của PPO. Nếu chiến lược mới đã chuyển sang hướng thuận lợi quá xa, việc cập nhật sẽ dừng lại.

### Bước 4: giá trị và entropy

Thêm MSE tiêu chuẩn vào mục tiêu phê bình và một phần thưởng entropy cho người chơi, giống như A2C.

> Đối với các nhà phê bình  mục tiêu thêm tiêu chuẩn MSE, đối với các diễn viên  thêm 奖励, tương tự như A2C.

### Bước 5: Chẩn đoán

Ba điều cần xem mỗi lần cập nhật:

> Mỗi lần cập nhật cần theo dõi ba điều:

- **Mean KL** `E[log π_old - log π_θ]`- Tôi nên ở lại.`[0, 0.02]`Nếu nó qua đi`0.1`, giảm `K_EPOCHS`hoặc `LR`- Tôi không biết.
  **平均 KL。**应 giữ ở `[0, 0.02]`Nếu quá`0.1`, giảm `K_EPOCHS`Hoặc`LR`
- **Clip fraction** phần mẫu có tỷ lệ nằm bên ngoài `[1-ε, 1+ε]`- Phải .`~0.1-0.3`Nếu`~0`, clip không bao giờ kích hoạt → tăng `LR`hoặc `K_EPOCHS`Nếu`~0.5+`, bạn đang quá phù hợp với việc triển khai → hạ thấp chúng.
  **裁剪比例。**tỷ lệ vượt quá`[1-ε, 1+ε]`                                                                                                                                                                                                                                                              `~0.1-0.3`
- **Explained variance** `1 - Var(V_target - V_pred) / Var(V_target)`- Đường đo chất lượng quan trọng. nên tăng lên 1 khi người phê bình học.
  **解释方差。**                                                                                                                                                                                                                                                              

## Những bẫy

- **Clip coefficient mistuned.** `ε = 0.2`là tiêu chuẩn thực tế.`0.1`làm cho các bản cập nhật quá nhút nhát; `0.3+`- Không ổn định.
  **裁剪系数调错。** `ε = 0.2`Đó là một tiêu chuẩn thực tế.`0.1`太保守;`0.3+`导致不稳定――
- **Too many epochs.** `K > 20`thường xuyên gây bất ổn vì chính sách di chuyển xa hơn `π_old`Thời đại giới hạn, đặc biệt là cho các mạng lớn.
  **太多 epoch。** `K > 20`常常不稳定,因为策略偏离`π_old`太远―― giới hạn thời đại, đặc biệt là mạng lưới lớn――
- **No reward normalization.**Tỷ lệ phần thưởng lớn ăn vào phạm vi clip.
  **没有奖励归一化。**Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh giá: Đánh
- **Forgetting advantage normalization.**Thường hợp bình thường hóa trung bình không/mức đơn vị là tiêu chuẩn.
  **忘记优势归一化。**Mỗi số lượng giá trị trung bình / đơn vị tiêu chuẩn phân biệt là tiêu chuẩn.
- **Learning rate not decayed.**PPO được hưởng lợi từ LR tuyến tính suy giảm đến không. LR liên tục thường tồi tệ hơn.
  **学习率未衰减。**PPO từ LR tuyến tính  giảm xuống 0 中受益──常数 LR thường hơn.
- **Importance ratio math errors.**Luôn luôn`exp(log_new - log_old)`cho sự ổn định số, không `new / old`- Tôi không biết.
  **重要性比率数学错误。**始终使用 `exp(log_new - log_old)`Bảo đảm giá trị số ổn định, chứ không phải `new / old`
- **Wrong gradient sign.**Tăng cường người thay thế = * giảm thiểu* `-L^{CLIP}`Một dấu hiệu đảo ngược là lỗi PPO phổ biến nhất.
  **梯度符号错误。**Đại diện tối đa hóa = * tối thiểu hóa * `-L^{CLIP}`▽符号反转为 PPO 最常见 bug──

## Hãy sử dụng nó để thực hiện

PPO là thuật toán RL mặc định của năm 2026 trên một số miền đáng ngạc nhiên:

> PPO là một thuật toán RL được chấp nhận trong nhiều lĩnh vực năm 2026:

| Use case | PPO variant |
|----------|-------------|
| Use case / 用例 | PPO variant / PPO 变体 |
| MuJoCo / robotics control / MuJoCo/机器人控制 | PPO with Gaussian policy, GAE(0.95) / 高斯策略的 PPO，GAE(0.95) |
| Atari / discrete games / Atari/离散游戏 | PPO with categorical policy, rolling 128-step rollouts / 分类策略的 PPO |
| RLHF for LLMs / LLM 的 RLHF | PPO with KL penalty to reference model, reward from RM at end of response / 带 KL 惩罚的 PPO |
| Large-scale game agents / 大规模游戏 Agent | IMPALA + PPO (AlphaStar, OpenAI Five) |
| Reasoning LLMs / 推理 LLM | GRPO (Lesson 12) — PPO variant without critic / 无 Critic 的 PPO 变体 |
| Preference-only data / 仅偏好数据 | DPO — closed-form collapsing of PPO+KL, no online sampling / 闭式 PPO+KL 折叠 |

PPO *hình dạng mất mát*  cắt thay thế + giá trị + entropy  là nền tảng cho DPO, GRPO và gần như mọi đường ống RLHF.

> PPO của* lỗ hình thức* cắt trung gian + 值 + 是 DPO、GRPO 和几乎所有 RLHF 流水线的脚手架──

## Chuyển nó đi.

Cứ như `outputs/skill-ppo-trainer.md`- Có thể là:

```markdown
---
name: ppo-trainer
description: Produce a PPO training config and a diagnostic plan for a given environment.
version: 1.0.0
phase: 9
lesson: 8
tags: [rl, ppo, policy-gradient]
---

Given an environment and training budget, output:

1. Rollout size. `N` envs × `T` steps.
2. Update schedule. `K` epochs, minibatch size, LR schedule.
3. Surrogate params. `ε` (clip), `c_v`, `c_e`, advantage normalization on.
4. Advantage. GAE(`λ`) with explicit `γ` and `λ`.
5. Diagnostics plan. KL, clip fraction, explained variance thresholds with alerts.

Refuse `K > 30` or `ε > 0.3` (unsafe trust region). Refuse any PPO run without advantage normalization or KL/clip monitoring. Flag clip fraction sustained above 0.4 as drift.
```

## Tập luyện bài tập

1. **Easy.**Tiếp tục PPO trên 4×4 GridWorld với `ε=0.2, K=4`So sánh hiệu quả mẫu với A2C (một thời đại mỗi lần triển khai) tại các bước môi trường phù hợp.
2. **Medium.**Tháo `K ∈ {1, 4, 10, 30}`- Trình quay lại vs bước env và theo dõi trung bình KL mỗi bản cập nhật.`K`KL sẽ nổ tung trong nhiệm vụ này?
3. **Hard.**Thay thế cho người thay thế bị cắt bằng một hình phạt KL thích ứng (`β`tăng gấp đôi nếu `KL > 2·target`, giảm một nửa nếu `KL < target/2`). So sánh lợi nhuận cuối cùng, ổn định và không clip.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Importance ratio | "r_t(θ)" | `π_θ(a\|s) / π_old(a\|s)`; deviation from the policy that collected the data. |
| Clipped surrogate | "PPO's main trick" | `min(r·A, clip(r, 1-ε, 1+ε)·A)`; flat gradient past the clip on beneficial side. |
| Trust region | "TRPO / PPO intent" | Limit each update's KL to guarantee monotone improvement. |
| KL penalty | "Soft trust region" | Alternative PPO: `L - β · KL(π_θ \|\| π_old)`. Adaptive `β`. |
| Clip fraction | "How often clipping triggers" | Diagnostic — should be 0.1-0.3; outside means mistuned. |
| Multi-epoch training | "Data reuse" | K epochs on each rollout; variance cost traded for sample efficiency. |
| On-policy-ish | "Mostly on-policy" | PPO is nominally on-policy but K>1 epochs uses slightly-off-policy data safely. |
| PPO-KL | "The other PPO" | KL-penalty variant; used in RLHF where KL-to-reference is already a constraint. |

## Xem thêm 延伸阅读

- [Schulman et al. (2017). Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)- Báo.
- [Schulman et al. (2015). Trust Region Policy Optimization](https://arxiv.org/abs/1502.05477)TRPO, người tiền nhiệm của PPO.
- [Andrychowicz et al. (2021). What Matters In On-Policy RL? A Large-Scale Empirical Study](https://arxiv.org/abs/2006.05990) mọi siêu tham số PPO bị loại bỏ.
- [Ouyang et al. (2022). Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) InstructGPT; công thức PPO-in-RLHF.
- [OpenAI Spinning Up — PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html) Khám phá hiện đại sạch sẽ với PyTorch.
- [CleanRL PPO implementation](https://github.com/vwxyzjn/cleanrl) chỉ dẫn PPO đơn tập tin được sử dụng bởi nhiều bài báo.
- [Hugging Face TRL — PPOTrainer](https://huggingface.co/docs/trl/main/en/ppo_trainer) công thức sản xuất cho PPO trên các mô hình ngôn ngữ; đọc cùng với Bài học 09 (RLHF).
- [Engstrom et al. (2020). Implementation Matters in Deep Policy Gradients](https://arxiv.org/abs/2005.12729) bài báo "37 tối ưu hóa cấp độ mã"; những thủ thuật PPO nào chịu tải và là câu chuyện dân gian.
