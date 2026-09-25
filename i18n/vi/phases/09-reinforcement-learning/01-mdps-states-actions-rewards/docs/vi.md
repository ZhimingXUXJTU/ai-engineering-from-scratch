# MDP, tiểu bang, hành động & phần thưởng

> Một Quá trình Quyết định Markov là năm thứ: trạng thái, hành động, chuyển đổi, phần thưởng, giảm giá. Mọi thứ trong RL  Q-learning, PPO, DPO, GRPO  tối ưu hóa trên hình dạng này. Học nó một lần, đọc phần còn lại của việc học tăng cường miễn phí.

> **【中文解读】**Málkoff quá trình quyết định (MDP) bao gồm năm yếu tố: trạng thái, động tác, chuyển đổi tỷ lệ, hàm thưởng, yếu tố giảm giá, RL mọi thứ trong đó Q-làm quen,PPO,DPO,GRPO đều được tối ưu hóa trong khuôn khổ này.

> **【拓展：MDP 是 AI 对齐的基础】**ChatGPT của RLHF  đào tạo bản chất cũng là một MDP: trạng thái = cuộc nói chuyện trên văn bản dưới đây,动作= tạo ra token,奖励= người thích đánh giá;.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 1 · 06 (Probability & Distributions), Phase 2 · 01 (ML Taxonomy) | **前置知识:** Phase 1 · 06 (概率与分布), Phase 2 · 01 (ML 分类)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Bạn đang viết một bot cờ vua, hoặc một nhà hoạch định hàng tồn kho, hoặc một đại lý giao dịch, hoặc vòng PPO đào tạo một mô hình lý luận, bốn lĩnh vực khác nhau, một sự thật đáng ngạc nhiên: tất cả bốn đều sụp đổ thành cùng một đối tượng toán học.

> Bạn đang viết một máy cờ quốc tế, hoặc một nhà lập kế hoạch kho lưu trữ, hoặc một đại lý giao dịch, hoặc một tập trung vào các mô hình PPO. Có bốn lĩnh vực khác nhau, một thực tế đáng ngạc nhiên: chúng có thể kết luận thành một đối tượng toán học.

Học tập được giám sát cho bạn `(x, y)`Đơn vị này có thể được sử dụng để tạo ra một số kết quả tốt hơn, nhưng bạn có thể không thể làm được điều đó.

> 监督学习给你 `(x, y)`Đúng vậy, để bạn phù hợp với một hàm. Tập luyện hóa học không cho bạn nhãn chỉ là trạng thái dòng chảy.

Bạn không thể học hỏi từ dòng này cho đến khi bạn chính thức hóa nó. "Những gì tôi đã thấy", "Những gì tôi đã làm, "Những gì đã xảy ra sau đó", "tốt như thế nào là"  mỗi phải trở thành một đối tượng bạn có thể suy luận về.

> Bạn không thể học được từ dòng dữ liệu này cho đến khi bạn hình thành nó. "Tôi thấy cái gì""",Tôi đã làm gì""",được xảy ra tiếp theo""",đó là tốt hơn" Mỗi thứ phải trở thành một đối tượng có thể suy luận.

## Khái niệm cốt lõi

![Markov decision process: states, actions, transitions, rewards, discount](../assets/mdp.svg)

**The five objects.**- **五个核心要素。**

- **States** `S`Trong GridWorld, tế bào, cờ vua, bảng, trong LLM, cửa sổ ngữ cảnh cộng với bất kỳ ký ức nào.
  **状态** `S` Thông tin cần thiết cho quyết định thông minh.  Trong GridWorld có thể ghi hình, trong International Chess là ghi hình, trong LLM có thể ghi hình trên cửa sổ bên dưới.
- **Actions** `A`Các lựa chọn, di chuyển lên/ xuống/ trái/ phải, chơi một động thái, phát hành một token.
  **动作** `A`△可选的操作──上/下/左/右移动──下一步棋──生成一个代币──
- **Transitions** `P(s' | s, a)`- Với tình trạng`s`và hành động`a`Định nghĩa trong cờ vua, stochastic trong hàng tồn kho, gần như quyết định trong giải mã LLM.
  **转移概率** `P(s' | s, a)`     `s`和动作 `a`, next state's distribution── trong cờ bạc là xác định, trong quản lý kho lưu trữ là ngẫu nhiên, trong LLM 解码 là gần như xác định──
- **Rewards** `R(s, a, s')`- Tín hiệu scalar. Win = +1, mất = -1. Thu nhập trừ chi phí.
  **奖励** `R(s, a, s')`                                                                                                                                                                                                                                                              
- **Discount** `γ ∈ [0, 1)`- Lương lai sẽ được thưởng bao nhiêu so với hiện tại.`γ = 0.99`mua một đường chân trời ~ 100 bước; `γ = 0.9`mua ~ 10.
  **折扣因子** `γ ∈ [0, 1)`: Thưởng tương lai so với trọng lượng của phần thưởng hiện tại`γ = 0.99`Đối với khoảng 100 bước quan sát hiệu quả;`γ = 0.9`Đối với khoảng 10 bước.

**The Markov property** `P(s_{t+1} | s_t, a_t) = P(s_{t+1} | s_0, a_0, …, s_t, a_t)`Tương lai chỉ phụ thuộc vào trạng thái hiện tại. Nếu không, đại diện của nhà nước là không đầy đủ không phải là một thất bại của phương pháp, một thất bại của nhà nước.

> **马尔可夫性质**Nếu không tồn tại, thì trạng thái biểu hiện không hoàn hảo không phải là thất bại của phương pháp, mà là thất bại của trạng thái.

**Policies and returns.**Một chính sách`π(a | s)`bản đồ các trạng thái để phân phối hành động.`G_t = r_t + γ r_{t+1} + γ² r_{t+2} + …`là tổng số tiền giảm giá của các phần thưởng trong tương lai.`V^π(s) = E[G_t | s_t = s]`là lợi nhuận dự kiến bắt đầu từ `s`trong chính sách`π`Giá trị Q`Q^π(s, a) = E[G_t | s_t = s, a_t = a]`là lợi nhuận dự kiến bắt đầu với một hành động cụ thể. Mỗi thuật toán RL ước tính một trong hai, sau đó cải thiện `π`Theo đó.

> **策略与回报。**策略 `π(a|s)`将状态映射到动作分布──回报 `G_t`là giá trị và giá trị của phần thưởng trong tương lai`V^π(s)``s`出发的期望回报──Q 值 `Q^π(s,a)`là từ động tác cụ thể được đưa ra kỳ vọng trả lại. Mỗi RL  thuật toán đều trong ước tính một trong hai số lượng này, sau đó theo đó cải tiến chiến lược.

**The Bellman equations.**Các phương trình điểm cố định mà mọi thứ trong giai đoạn này sử dụng:

`V^π(s) = Σ_a π(a|s) Σ_{s', r} P(s', r | s, a) [r + γ V^π(s')]`

> **【中文解读】**Phương trình Bellman là mối quan hệ chuyển tiếp cốt lõi của RL: giá trị của trạng thái hiện tại = phần thưởng tức thời + giá trị trạng thái sau khi giảm giá. Nó là cơ sở chung của lập kế hoạch, học tập Q-TD. Trong việc đào tạo RLHF của LLM, điều này tương ứng với "những đóng góp của token hiện tại = số điểm ưu tiên của con người + những đóng góp mong đợi của token tương lai".

> **【拓展：从 MDP 到 POMDP】**Trong thực tế, nhiều vấn đề không đáp ứng được khả năng của người dùng. Trong thực tế, nhiều vấn đề không đáp ứng được khả năng của người dùng.
`Q^π(s, a) = Σ_{s', r} P(s', r | s, a) [r + γ Σ_{a'} π(a'|s') Q^π(s', a')]`

Những chia dự kiến này trở lại vào "bước này phần thưởng" cộng với "đáng giá giảm giá của nơi bạn hạ cánh". Khôi phục. Mỗi thuật toán trong giai đoạn 9 hoặc lặp lại phương trình này để hội tụ (quá trình lập trình động), các mẫu từ nó (Monte Carlo), hoặc khởi động nó một bước (các biệt thời gian).

> Những phương pháp này sẽ được kỳ vọng để trả lại được phân chia thành "đánh giá của bước hiện tại" cộng với "đánh giá giảm giá của trạng thái đạt được"―递归―.

## Hãy xây dựng nó.
```figure
discount-horizon
```

## Hãy xây dựng nó

### Bước 1: một MDP xác định nhỏ

Một 4x4 GridWorld. Trưởng bắt đầu ở phía trên bên trái, cuối ở phía dưới bên phải, phần thưởng là -1 mỗi bước, hành động`{up, down, left, right}`- Nhìn xem .`code/main.py`- Tôi không biết.

> Một 4×4 của mạng hình thế giới. Nhóm thông minh từ góc trên trái xuất phát, kết thúc trạng thái ở góc dưới phải, mỗi bước thưởng -1, động như `{上, 下, 左, 右}`

```python
GRID = 4
TERMINAL = (3, 3)
ACTIONS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

def step(state, action):
    if state == TERMINAL:
        return state, 0.0, True
    dr, dc = ACTIONS[action]
    r, c = state
    nr = min(max(r + dr, 0), GRID - 1)
    nc = min(max(c + dc, 0), GRID - 1)
    return (nr, nc), -1.0, (nr, nc) == TERMINAL
```

5 đường, đó là toàn bộ môi trường, chuyển đổi quyết định, hình phạt bước liên tục, hấp thụ trạng thái cuối cùng.

> 五行代码──这是整个环境──确定性转移──恒定步惩罚──吸收终止状态──

### Bước 2: triển khai chính sách

Một chính sách là một chức năng từ phân phối trạng thái đến hành động.

> 策略 là hàm phân phối từ trạng thái đến động tác.

```python
def uniform_policy(state):
    return {a: 0.25 for a in ACTIONS}

def rollout(policy, max_steps=200):
    s, total, steps = (0, 0), 0.0, 0
    for _ in range(max_steps):
        a = sample(policy(s))
        s, r, done = step(s, a)
        total += r
        steps += 1
        if done:
            break
    return total, steps
```

Lấy chính sách ngẫu nhiên 1000 lần. Phản hồi trung bình là khoảng -60 đến -80 cho bảng 4x4. Phản hồi tối ưu là -6 (cách đường thẳng xuống phải).

> 运行随机策略 1000次──这个4×4 棋盘的平均回报约为 -60到 -80──最优回报是 -6(直线路径向右下方)──缩小这个差距就是9阶段的全部目标──

### Bước 3: tính toán`V^π`chính xác qua phương trình Bellman

Đối với MDP nhỏ phương trình Bellman là một hệ thống tuyến tính.

> Đối với MDP nhỏ, phương trình Bellman là một hệ thống đường dẫn.

```python
def policy_evaluation(policy, gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in all_states()}
    while True:
        delta = 0.0
        for s in all_states():
            if s == TERMINAL:
                continue
            v = 0.0
            for a, pi_a in policy(s).items():
                s_next, r, _ = step(s, a)
                v += pi_a * (r + gamma * V[s_next])
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            return V
```

Đây là đánh giá chính sách lặp lại. Đây là thuật toán đầu tiên trong Sutton & Barto và nền tảng lý thuyết của mọi phương pháp RL tiếp theo.

> Đây là đánh giá chiến lược thế hệ. Đây là thuật toán đầu tiên trong sách giáo khoa của Sutton & Barto, cũng là cơ sở lý thuyết của tất cả các phương pháp RL sau đó.

### Bước 4: `γ`là một siêu tham số có ý nghĩa vật lý

Tầm nhìn hiệu quả là khoảng `1 / (1 - γ)`- `γ = 0.9`→ 10 bước. `γ = 0.99`→ 100 bước. `γ = 0.999`→ 1000 bước.

> Có hiệu quả cho thị trường`1 / (1 - γ)``γ = 0.9`Đối với 10 bước:`γ = 0.99`Đối với 100 bước.`γ = 0.999`Đối với 1000 bước.

quá thấp và đại lý hành động cận thị. quá cao và giao tín dụng trở nên ồn ào, bởi vì nhiều bước đầu chia sẻ trách nhiệm cho phần thưởng trong tương lai xa. LLM RLHF thường sử dụng `γ = 1`vì các tập phim ngắn và giới hạn.`0.95–0.99`. Trò chơi chiến lược đường dài sử dụng`0.999`- Tôi không biết.

> 折扣因子太低,智能体会目光短浅──太高, phân bổ tín dụng trở nên 杂, vì nhiều bước đầu tiên cùng nhau chịu trách nhiệm về phần thưởng dài hạn──LLM RLHF thường sử dụng `γ = 1`, vì 回合短且有界―― kiểm soát nhiệm vụ sử dụng `0.95-0.99`△长视野策略游戏使用 `0.999`

## Những bẫy

- **Non-Markovian state.**Nếu bạn cần ba quan sát cuối cùng để quyết định, "thế trạng" không chỉ là quan sát hiện tại.
  **非马尔可夫状态。**Nếu bạn cần gần đây ba quan sát để có thể đưa ra quyết định, " trạng thái "就不仅仅是当前观测──修复方法:堆叠(Atari 上的DQN 堆叠 4 ) hoặc sử dụng trạng thái vòng lặp(LSTM/GRU)。
- **Sparse rewards.**Những phần thưởng chỉ dành cho người chiến thắng làm cho việc học gần như không thể trong không gian lớn.
  **稀疏奖励。**仅获胜奖励使学习在大状态空间中的几乎不可能──塑形奖励 (中信号) 或用模仿学习引导──
- **Reward hacking.**Tối ưu hóa phần thưởng đại diện thường tạo ra hành vi bệnh lý. Đại diện đua thuyền của OpenAI xoay quanh vòng tròn thu thập sức mạnh mãi mãi thay vì kết thúc cuộc đua. Luôn xác định phần thưởng từ kết quả mục tiêu, chứ không phải đại diện.
  **奖励黑客。**优化代理奖励常产生病态行为――OpenAI的赛船代理原地转圈收集道具,永远不完成比赛――始终从目标结果定义奖励,而不是代理――
- **Discount mis-spec.** `γ = 1`trong một nhiệm vụ đường chân trời vô hạn làm cho mọi giá trị vô hạn.`γ < 1`- Tôi không biết.
  **折扣因子设定错误。**无限视野任务上 `γ = 1`会使所有值为无穷──始终使用有限视野或 `γ < 1`Đến đây.
- **Reward scale.**Các phần thưởng của {+100, -100} so với {+1, -1} cho các chính sách tối ưu giống nhau nhưng độ lớn gradient khác nhau.`[-1, 1]`- trước khi kết nối với PPO/DQN.
  **奖励尺度。**Các phần thưởng của {+100, -100} với {+1, -1} cho ra cùng một chiến lược tối ưu, nhưng mức độ khác biệt rất lớn.`[-1, 1]`左右──

## Hãy sử dụng nó để thực hiện

Dòng 2026 giảm mỗi đường ống RL thành MDP trước khi chạm vào mã:

> Trước khi viết mã hóa năm 2026, sẽ kết hợp mỗi dòng chảy RL thành một MDP:

| Situation | State | Action | Reward | γ |
|-----------|-------|--------|--------|---|
| Situation / 场景 | State / 状态 | Action / 动作 | Reward / 奖励 | γ |
| Control (locomotion, manipulation) / 控制（运动、操作） | Joint angles + velocities / 关节角度+速度 | Continuous torques / 连续力矩 | Task-specific shaped / 任务特定塑形 | 0.99 |
| Games (chess, Go, poker) / 游戏（象棋、围棋、扑克） | Board + history / 棋盘+历史 | Legal move / 合法走法 | Win=+1 / loss=-1 / 胜=+1/负=-1 | 1.0 (finite) |
| Inventory / pricing / 库存/定价 | Stock + demand / 库存+需求 | Order qty / 订购量 | Revenue - cost / 收入-成本 | 0.95 |
| RLHF for LLMs / LLM 的 RLHF | Context tokens / 上下文 token | Next token / 下一个 token | Reward-model score at end / 末尾奖励模型分数 | 1.0 (episode ~200 tokens) |
| GRPO for reasoning / 推理的 GRPO | Prompt + partial response / 提示+部分回复 | Next token / 下一个 token | Verifier 0/1 at end / 末尾验证器 0/1 | 1.0 |

Viết năm tuples trước khi viết bất kỳ vòng lặp đào tạo. Hầu hết các báo cáo lỗi "RL không hoạt động" bắt nguồn từ một công thức MDP đã bị phá vỡ trên giấy.

> Trong việc viết bất kỳ vòng tập luyện nào trước khi viết tốt 5元组. Hầu hết các báo cáo lỗi "RL không làm việc" đều có thể được bắt nguồn từ các định nghĩa MDP trên giấy.

## Chuyển nó đi.

Cứ như `outputs/skill-mdp-modeler.md`- Có thể là:

```markdown
---
name: mdp-modeler
description: Given a task description, produce a Markov Decision Process spec and flag formulation risks before training.
version: 1.0.0
phase: 9
lesson: 1
tags: [rl, mdp, modeling]
---

Given a task (control / game / recommendation / LLM fine-tuning), output:

1. State. Exact feature vector or tensor spec. Justify Markov property.
2. Action. Discrete set or continuous range. Dimensionality.
3. Transition. Deterministic, stochastic-with-known-model, or sample-only.
4. Reward. Function and source. Sparse vs shaped. Terminal vs per-step.
5. Discount. Value and horizon justification.

Refuse to ship any MDP where the state is non-Markovian without explicit mention of frame-stacking or recurrent state. Refuse any reward that was not defined in terms of the target outcome. Flag any `γ ≥ 1.0` on an infinite-horizon task. Flag any reward range >100x the typical step reward as a likely gradient-explosion source.
```

## Tập luyện bài tập

1. **Easy.**Thực hiện 4×4 GridWorld và triển khai chính sách ngẫu nhiên trong `code/main.py`- chạy 10.000 tập. báo cáo trung bình và std của lợi nhuận. so sánh với lợi nhuận tối ưu (-6).
   > **练习1（简单）：**实现 4×4 GridWorld 和随机策略 rollout──运行 10,000 回合──报告回报的平均值和标准差,与最优回报 (-6) 比较──
2. **Medium.**Đi chạy`policy_evaluation`với `γ ∈ {0.5, 0.9, 0.99}`cho chính sách đồng bộ ngẫu nhiên.`V`Giải thích tại sao các giá trị trạng thái gần ga kết thúc tăng nhanh hơn với lớn hơn `γ`- Tôi không biết.
   > **练习2（中等）：**用 `γ ∈ {0.5, 0.9, 0.99}`运行策略评估──印每 γ 的 4×4 值网格──解释为什么接近终止状态的状态值在更大的 γ 下增长更快──
3. **Hard.**Chuyển lại GridWorld stochastic: mỗi hành động trượt đến một hướng lân cận với xác suất `p = 0.1`- Đánh giá lại chính sách đồng phục.`V[start]`- Tốt hơn hay tồi tệ hơn?
   > **练习3（困难）：**sẽ GridWorld  đổi thành tùy ý: mỗi động tác theo tỷ lệ`p = 0.1`滑向相邻方向──重新评估均策略──`V[start]`变好还是变差? Tại sao?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
| MDP | "Reinforcement learning setup" | Tuple `(S, A, P, R, γ)` satisfying the Markov property. |
| State / 状态 | "What the agent sees" / "智能体看到什么" | Sufficient statistic for future dynamics under the chosen policy class. |
| Policy / 策略 | "Agent's behavior" / "智能体的行为" | Conditional distribution `π(a \| s)` or deterministic map `s → a`. |
| Return / 回报 | "Total reward" / "总奖励" | Discounted sum `Σ γ^t r_t` from the current step. |
| Value / 值函数 | "How good a state is" / "状态有多好" | Expected return under `π` starting from `s`. |
| Q-value / Q值 | "How good an action is" / "动作有多好" | Expected return under `π` starting from `s` with first action `a`. |
| Bellman equation / Bellman方程 | "Dynamic programming recursion" / "动态规划递推" | Fixed-point decomposition of value / Q into one-step reward plus discounted successor value. |
| Discount `γ` / 折扣因子 | "Future vs present" / "未来vs当前" | Geometric weight on far-future reward; effective horizon `~1/(1-γ)`. |

## Xem thêm 延伸阅读

- [Sutton & Barto (2018). Reinforcement Learning: An Introduction, 2nd ed.](http://incompleteideas.net/book/RLbook2020.pdf)Chương 3 bao gồm MDP và phương trình Bellman; Chương 1 thúc đẩy giả thuyết phần thưởng đặt nền tảng cho mỗi bài học tiếp theo.
- [Bellman (1957). Dynamic Programming](https://press.princeton.edu/books/paperback/9780691146683/dynamic-programming) nguồn gốc của phương trình Bellman.
- [OpenAI Spinning Up — Part 1: Key Concepts](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html) Nút đầu tiên MDP ngắn gọn từ góc RL sâu.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887) tham chiếu nghiên cứu hoạt động về MDP và phương pháp giải pháp chính xác.
- [Littman (1996). Algorithms for Sequential Decision Making (PhD thesis)](https://www.cs.rutgers.edu/~mlittman/papers/thesis-main.pdf) nguồn gốc sạch nhất của MDP như một chuyên môn lập trình động.
