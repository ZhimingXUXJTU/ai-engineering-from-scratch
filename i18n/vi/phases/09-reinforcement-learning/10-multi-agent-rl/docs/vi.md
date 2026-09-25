# RL đa đại lý, nhiều cơ thể thông minh

> Một đại lý RL giả định môi trường không hoạt động. Đặt hai đại lý học tập trong cùng một thế giới và giả định đó phá vỡ: mỗi đại lý là một phần của môi trường của người khác, và cả hai đều thay đổi.

> **【中文解读】**单智能体 RL 假设环境是平稳的──但放入两个同时学习的智能体后, mỗi智能体都成为对方环境的一部分环境不再平稳,马尔可夫假设被打破──多智能体 RL就是处理"每个人都在变化"时的收收问题──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 04 (Q-learning), Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic) | **前置知识:** Phase 9 · 04 (Q-learning), Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Một robot học cách điều hướng một căn phòng là một vấn đề RL của một đại lý duy nhất. Một đội bóng không. AlphaStar vs StarCraft đối thủ không. Một thị trường của đại lý đấu giá không. Hai xe đàm phán một dừng bốn chiều không. Nhiều vấn đề trên nhiều thế giới thực không.

> 机器人学习在房间中导航是单智能体 RL 问题──足球队不是──AlphaStar对StarCraft对手不是──竞价代理的市场不是──两辆车协商四路停车不是──多对多现实世界问题都不是──

Trong mọi môi trường đa tác nhân, từ quan điểm của bất kỳ tác nhân nào, các tác nhân khác * là * một phần của môi trường. Khi chúng học và thay đổi hành vi của mình, môi trường trở nên không ổn định. Tài sản Markov "thị trạng tiếp theo chỉ phụ thuộc vào trạng thái hiện tại và hành động của tôi" bị vi phạm bởi vì trạng thái tiếp theo cũng phụ thuộc vào những gì các đại lý khác đã chọn, và chính sách của họ là chuyển mục tiêu.

> Trong mỗi môi trường đa năng thông minh, theo quan điểm của mỗi cơ thể thông minh, các cơ thể thông minh khác* là một phần của môi trường. Khi chúng học hỏi và thay đổi hành vi, môi trường trở nên không ổn định.

Điều này phá vỡ các bằng chứng hội tụ bảng (các bảo đảm của Q-learning giả định một môi trường tĩnh). Nó phá vỡ RL sâu sắc ngây thơ: các đại lý đuổi theo nhau trong vòng lặp, không bao giờ hội tụ với một chính sách ổn định. Bạn cần các kỹ thuật đa đại lý cụ thể: đào tạo tập trung / thực hiện phi tập trung, cơ sở đối thực, chơi giải đấu, tự chơi.

> Điều này phá vỡ biểu đồ nhận thức chứng minh (((Q-learning's assurance assumption is plain stable environment) ⋅ Nó cũng phá vỡ một vòng lặp đơn giản sâu sắc RL: các cơ thể thông minh theo đuổi lẫn nhau, không bao giờ nhận được đến chiến lược ổn định.

2026 ứng dụng: robot swarms, giao thông định tuyến, hạm đội xe tự động, mô phỏng thị trường, hệ thống LLM đa đại lý (Phase 16), và bất kỳ trò chơi nào với nhiều người chơi thông minh hơn một.

> 2026 năm ứng dụng: 机器人集群、交通路由、自动驾驶车队、市场模拟器、多智能体 LLM 系统(Phase 16), cũng như bất kỳ trò chơi nào có nhiều người chơi thông minh.

> **【中文解读】**Ưu tiên của nhiều cơ thể thông minh RL: không ổn định (非平稳性) 其他智能体也在学习) 信用分配 (谁应获得奖励?) 联合动作空间爆炸、部分可观察性──四种主要范式:独立学习 (独立学习) 简单但不保证收)  CTDE (训练时集中、执行时分布) 自我博 (AlphaZero) 联盟训练 (AlphaStar) 

> **【拓展：多智能体→LLM Agent系统】**Các mô hình MARL được sử dụng nhiều năm 2026 là nhiều mô hình lớn của các mô hình LLM: nhiều mô hình đại lý hợp tác hoàn thành các nhiệm vụ phức tạp.

## Khái niệm cốt lõi

![Four MARL regimes: indep, centralized critic, self-play, league](../assets/marl.svg)

**Formalism: Markov Game.**Một khái quát hóa của MDP: các tiểu bang `S`, một hành động chung `a = (a_1, …, a_n)`, chuyển tiếp `P(s' | s, a)`, và phần thưởng cho mỗi đại lý `R_i(s, a, s')`Mỗi đại lý`i`tối đa hóa lợi nhuận của riêng mình theo chính sách của riêng mình `π_i`Nếu phần thưởng giống nhau, thì đó là**fully cooperative**Nếu số tiền bằng không, thì nó là**adversarial**Nếu trộn, thì nó là **general-sum**- Tôi không biết.

> **形式化：马尔可夫博弈。**MDP 的推广: trạng thái `S`、 hợp tác động`a = (a_1, …, a_n)`、 chuyển`P(s'|s,a)`、 Giải thưởng cho mỗi người thông minh `R_i`Nếu phần thưởng giống nhau,**全合作**Nếu là零和, thì là**对抗**Nếu trộn, thì**一般和**

**Core challenges:**

- **Non-stationarity.** `P(s' | s, a_i)`từ đại lý `i`Quan điểm của anh phụ thuộc vào`π_{-i}`, mà đang thay đổi.
  **非平稳性。**Từ智能体`i`Quan điểm của chuyển động phụ thuộc vào các chiến lược đang thay đổi của các cơ thể thông minh khác.
- **Credit assignment.**Với phần thưởng chia sẻ, đại lý nào gây ra nó?
  **信用分配。**Khi chia sẻ phần thưởng, cái gì dẫn đến?
- **Exploration coordination.**Các đại lý phải khám phá các chiến lược bổ sung, không phải khám phá một trạng thái tương tự.
  **探索协调。**智能体 phải khám phá các chiến lược bổ sung lẫn nhau, chứ không phải khám phá quá mức về trạng thái tương tự.
- **Scalability.**Không gian hành động chung tăng trưởng theo cấp sốt `n`- Tôi không biết.
  **可扩展性。**联合动作空间随 `n`Số lượng tăng trưởng.
- **Partial observability.**Mỗi nhân viên chỉ thấy quan sát của riêng mình; tình trạng toàn cầu được che giấu.
  **部分可观察性。**Mỗi thể thông minh chỉ nhìn thấy quan sát của mình; toàn cảnh trạng thái ẩn.

**Four dominant regimes:**

> **四种主导范式：**

**1. Independent Q-learning / independent PPO (IQL, IPPO).**Mỗi đại lý học được Q hoặc chính sách của riêng mình, đối xử với những người khác như là một phần của môi trường. đơn giản, đôi khi nó hoạt động (đặc biệt là với trải nghiệm lặp lại hoạt động như một thủ thuật mô hình hóa đại lý làm mượt mà).

> **1. 独立 Q-learning / 独立 PPO。**Mỗi cơ thể thông minh học hỏi Q hoặc chiến lược của riêng mình, sẽ coi các cơ thể thông minh khác là một phần của môi trường.

**2. Centralized training, decentralized execution (CTDE).**Phương pháp hiện đại phổ biến nhất.`π_i`Điều kiện về quan sát địa phương `o_i` thực hiện phân cấp tiêu chuẩn khi triển khai.`Q(s, a_1, …, a_n)`Điều kiện về tình trạng toàn cầu và hành động chung.
- **MADDPG**(Lowe et al. 2017): DDPG với một nhà phê bình tập trung cho mỗi đại lý.
- **COMA**(Foerster et al. 2017): cơ sở phản thực  hỏi "bảo thưởng của tôi sẽ là gì nếu tôi đã hành động `a'`thay vì đó?"  cô lập sự đóng góp của tôi.
- **MAPPO**- **IPPO**với nhà phê bình chung (Yu et al. 2022): PPO với chức năng giá trị tập trung.
- **QMIX**(Rashid et al. 2018): phân hủy giá trị  `Q_tot(s, a) = f(Q_1(s, a_1), …, Q_n(s, a_n))`với sự trộn lẫn đơn điệu.

> **2. 集中训练，分布执行（CTDE）。**Trong khi đó, các nhà khoa học đã phát triển các phương pháp học tập tập trung để phân tích các phương pháp học tập và các phương pháp học tập tập.

**3. Self-play.**Hai bản sao của cùng một đại lý chơi với nhau. Chính sách của đối thủ * là chính sách của tôi từ một snapshot trước đây. AlphaGo / AlphaZero / MuZero. OpenAI Năm.

> **3. 自我博弈。**Cùng với 2 bản sao của cùng một cơ thể thông minh đối với ── phương pháp đối với ── là phương pháp của quá khứ ── phù hợp nhất với 零和博; training signal is对称的──

**4. League play.**Một sự mở rộng của tự chơi đến môi trường tổng / đối đầu: giữ một dân số của chính sách quá khứ và hiện tại, lấy mẫu đối thủ từ giải đấu, tập luyện chống lại họ. Thêm khai thác (khóa học chuyên đánh bại những người giỏi nhất hiện tại) và khai thác chính (khóa học chuyên đánh bại các khai thác). AlphaStar (StarCraft II).

> **4. 联盟训练。**Bản thân mình đã mở rộng: giữ cho quá khứ và hiện tại của các chiến lược, từ liên minh trong các mô hình đối thủ.

**Communication.**Cho phép các nhân viên gửi tin nhắn học hỏi `m_i`Các hệ thống đa đại lý dựa trên LLM ngày nay (Phase 16) về cơ bản giao tiếp bằng ngôn ngữ tự nhiên.

> **通信。**允许智能体相互发送学习的消息――有效在合作环境中―― ngày nay LLM 多智能体系统本质上使用自然语言通信――

## Hãy xây dựng nó.
```figure
f3-marl-orbit
```

## Hãy xây dựng nó

Bài học này sử dụng một GridWorld 6×6 với hai đại lý hợp tác.`-1`mỗi bước trong khi bất kỳ đại lý nào vẫn đang di chuyển,`+10`Khi cả hai đến.`code/main.py`- Tôi không biết.

> Bài học này sử dụng một 6×6 GridWorld và hai hệ thống thông minh hợp tác. Chúng bắt đầu từ góc độ đối đầu, phải đạt được mục tiêu chia sẻ.

### Bước 1: môi trường đa đại lý

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

Không gian hành động chung là`|A|² = 16`- Tình trạng toàn cầu là hai vị trí.

> *联合*动作空间是 `|A|² = 16` toàn cảnh trạng thái là hai vị trí

### Bước 2: Học Q độc lập

Mỗi đại lý chạy bảng Q riêng của mình được khóa vào trạng thái chung. Ở mỗi bước: cả hai chọn các hành động tham lam, thu thập chuyển đổi chung, mỗi người cập nhật Q của riêng mình với phần thưởng chia sẻ.

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

Làm việc trên nhiệm vụ này bởi vì phần thưởng dày đặc và phù hợp. Không thành công trong các nhiệm vụ gắn liền chặt chẽ (ví dụ, nơi một đại lý phải *ngợi * cho người khác).

> Trong nhiệm vụ này có hiệu quả, vì phần thưởng rất cồng kề và rất tập trung. Trong nhiệm vụ chặt chẽ, một cơ thể thông minh phải chờ đợi một cơ thể khác.

### Bước 3: Q tập trung với cập nhật giá trị phân hủy

Sử dụng một Q thay vì các hành động chung `Q(s, a_1, a_2)`. Cập nhật từ phần thưởng chia sẻ. Phân tâm hóa khi thực hiện bằng cách bìa: `π_i(s) = argmax_{a_i} max_{a_{-i}} Q(s, a_1, a_2)`. Giao dịch không gian hành động chung theo tỷ lệ thoáng để có một cái nhìn toàn cầu * đúng * .

> Sử dụng một Q trên tập hợp động tác. Từ chia sẻ phần thưởng cập nhật.

### Bước 4: tự chơi đơn giản (nhân 2 đối thủ)

- Cảnh sát A chống lại Cảnh sát B.`K`tập, sao chép trọng lượng của A thành B. Tập luyện đối xứng, tiến bộ liên tục.

> Cùng một thể trí thông minh, hai vai trò.`K`回合后将 A's权重复复到B──对称训练,持续进步──AlphaZero 配方的缩影──

## Những bẫy

- **Non-stationary replay.**Lại chơi kinh nghiệm với các đại lý độc lập là tồi tệ hơn so với một đại lý đơn bởi vì những chuyển đổi cũ được tạo ra bởi các đối thủ đã lỗi thời.
  **非平稳回放。**Chuyên nghiệm của một cơ thể thông minh độc lập trở lại tồi tệ hơn so với một cơ thể thông minh đơn lẻ, vì chuyển đổi cũ được tạo ra bởi đối thủ đã qua.
- **Credit assignment ambiguity.**Giải thưởng chia sẻ sau một tập dài; không có cách rõ ràng để nói là đại lý nào đóng góp.
  **信用分配模糊。**长回合后的共享奖励; không thể xác định được những gì mà các nhà khoa học đã đóng góp.
- **Policy drift / chasing.**Phản ứng tốt nhất của mỗi đại lý thay đổi với cập nhật của nhau.
  **策略漂移/追逐。**Phản ứng tốt nhất của mỗi cơ thể thông minh với sự đổi mới và thay đổi của các cơ thể thông minh khác.
- **Reward hacking via coordination.**Các đại lý tìm thấy những hoạt động phối hợp mà nhà thiết kế không dự đoán. Các đại lý đấu giá hội tụ để đặt giá không.
  **协调奖励黑客。**智能体发现设计者未预期的协调漏洞──修复:仔细的奖励设计、行为约束──
- **Exploration redundancy.**Cả hai đại lý đều khám phá các cặp hành động trạng thái tương tự.
  **探索冗余。**2 thể trí thông minh khám phá cùng một trạng thái- động tác đối với.
- **League cycles.**Chơi tự chơi tinh khiết có thể bị mắc kẹt trong chu kỳ thống trị.
  **联盟循环。**纯自我博可能陷入控制循环──修复:多样化对手的联盟训练──
- **Sample explosion.** `n`Các nhân viên × không gian trạng thái × hành động chung. Phân tích với sự gần gũi chức năng; không gian hành động nhân tố (một đầu sản xuất chính sách cho mỗi nhân viên).
  **样本爆炸。**n 个智能体 × 状态空间 × 联合动作──用函数近似解决;因子化动作空间──

## Hãy sử dụng nó để thực hiện

Bản đồ ứng dụng MARL 2026:

> 2026 年 MARL 应用地图:

| Domain | Method | Notes |
|--------|--------|-------|
| Domain / 领域 | Method / 方法 | Notes / 备注 |
| Cooperative navigation / manipulation / 合作导航/操作 | MAPPO / QMIX | CTDE; shared critic + decentralized actors. / CTDE；共享 Critic + 分布式 Actor。 |
| Two-player games (chess, Go, poker) / 双人游戏 | Self-play with MCTS (AlphaZero) | Zero-sum; symmetric training. / 零和；对称训练。 |
| Complex multiplayer (Dota, StarCraft) / 复杂多人游戏 | League play + imitation pretraining | OpenAI Five, AlphaStar. |
| Autonomous-vehicle fleets / 自动驾驶车队 | CTDE MAPPO / PPO with attention | Partial obs; variable team sizes. / 部分可观察；可变团队大小。 |
| Auction markets / 拍卖市场 | Game-theoretic equilibrium + RL | Mean-field RL when `n` → ∞. / n→∞ 时用平均场 RL。 |
| LLM multi-agent systems (Phase 16) / LLM 多智能体系统 | Natural-language comm + role conditioning | RL loop at the agent-planning layer. / Agent 规划层的 RL 循环。 |

Năm 2026, lĩnh vực tăng trưởng lớn nhất của MARL là dựa trên LLM: những đám đại lý mô hình ngôn ngữ đàm phán, tranh luận, xây dựng phần mềm.

> 2026 MARL tăng trưởng lớn nhất lĩnh vực là dựa trên LLM của: ngôn ngữ mô hình智能体群体协商、辩论、构建软件──RL xuất hiện trên *轨迹级* xuất khẩu ưu tiên tối ưu hóa, chứ không phải token 级──

## Chuyển nó đi.

Cứ như `outputs/skill-marl-architect.md`- Có thể là:

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

## Tập luyện bài tập

1. **Easy.**Trình luyện học Q độc lập trên hợp tác cộng tác GridWorld 2 đại lý. Bao nhiêu tập cho đến khi trung bình trở lại > 0?
2. **Medium.**Thêm một nhiệm vụ "sự phối hợp": mục tiêu chỉ đạt được khi cả hai đại lý bước lên nó trên cùng một lượt.
3. **Hard.**Thực hiện một nhà phê bình tập trung cho đào tạo theo kiểu MAPPO và so sánh tốc độ hội tụ với PPO độc lập trong nhiệm vụ phối hợp.

## Từ khóa  Từ khóa nhanh chóng

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

## Xem thêm 延伸阅读

- [Lowe et al. (2017). Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments (MADDPG)](https://arxiv.org/abs/1706.02275) CTDE với một nhà phê bình tập trung.
- [Foerster et al. (2017). Counterfactual Multi-Agent Policy Gradients (COMA)](https://arxiv.org/abs/1705.08926) Các đường cơ sở đối lập cho việc phân bổ tín dụng.
- [Rashid et al. (2018). QMIX: Monotonic Value Function Factorisation](https://arxiv.org/abs/1803.11485) phân hủy giá trị với sự đơn điệu.
- [Yu et al. (2022). The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games (MAPPO)](https://arxiv.org/abs/2103.01955)PPO rất mạnh với MARL.
- [Vinyals et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z) chơi giải đấu ở quy mô.
- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270) tự chơi tự chơi trong các trò chơi số không.
- [Sutton & Barto (2018). Ch. 15 — Neuroscience & Ch. 17 — Frontiers](http://incompleteideas.net/book/RLbook2020.pdf) bao gồm việc xử lý ngắn của sách giáo khoa về các thiết lập đa đại lý và vấn đề không ổn định mà CTDE được thiết kế để giải quyết.
- [Zhang, Yang & Başar (2021). Multi-Agent Reinforcement Learning: A Selective Overview](https://arxiv.org/abs/1911.10635) khảo sát bao gồm các MARL hợp tác, cạnh tranh và hỗn hợp với kết quả hội tụ.
