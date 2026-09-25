# RL cho trò chơi  AlphaZero, MuZero, và thời đại lý luận LLM ∙ 游戏中的强化学习  AlphaZero、MuZero với LLM 推理时代

> 1992: TD-Gammon đánh bại các nhà vô địch người ở backgammon bằng TD tinh khiết. 2016: AlphaGo đánh bại Lee Sedol. 2017: AlphaZero thống trị cờ vua, shogi và Go từ đầu. 2024: DeepSeek-R1 chứng minh công thức tương tự, với GRPO thay thế PPO, hoạt động trên lý luận.

> **【中文解读】**游戏是RL 突破的试验场:TD-Gammon (1992) → AlphaGo (2016) → AlphaZero (2017) → DeepSeek-R1 (2025)。DeepSeek-R1 证明 AlphaZero's"self-browse+search+strategy improvement"循环 có thể trực tiếp được sử dụng cho các mô hình lớn của toán học suy luận token 就是动作,验证器就是"赢/输"信号──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (MARL) | **前置知识:** Phase 9 · 05 (DQN), Phase 9 · 08 (PPO), Phase 9 · 09 (RLHF), Phase 9 · 10 (多智能体 RL)
**Time:** ~120 minutes | **时间:** ~120 分钟

## Vấn đề  vấn đề giới thiệu

Trò chơi có tất cả những gì RL muốn. Giải thưởng sạch (trận thắng/ thua). Phiên bản vô hạn (đặt lại tự chơi). mô phỏng hoàn hảo (trò chơi * là * mô phỏng). Không gian hành động liên tục nhỏ hoặc nhỏ.

> 游戏拥有RL所需的一切──清晰的奖励(赢/输)──无限回合(自我博重置)──完美仿真(游戏*就是*仿真器)──离散或小型连续动作空间──迫使对抗鲁棒性的多智能体结构──

Và các trò chơi là cách để kiểm tra mọi bước đột phá lớn của RL. TD-Gammon (backgammon, 1992). Atari-DQN (2013). AlphaGo (2016). AlphaZero (2017). OpenAI Five (Dota 2, 2019). AlphaStar (StarCraft II, 2019). MuZero (tiếng học mô hình, 2019). AlphaTensor (tổ số ma trận, 2022). AlphaDev (chế thuật phân loại, 2023). DeepSeek-R1 (chủ nghĩa toán học, 2025)  minh chứng mới nhất rằng các kỹ thuật game-RL hoạt động trên văn bản.

> 游戏是每个 RL 重大突破的试验场. TD-Gammon(西洋双陆棋,1992) Atari-DQN(2013) 、AlphaGo(2016) 、AlphaZero(2017) 、OpenAI Five(Dota 2,2019) 、AlphaStar(星际争 II,2019) 、MuZero(学习模型,2019) 、AlphaTensor(矩阵乘法,2022) 、AlphaDev(排序算法,2023) 、DeepSeek-R1(数学推理,2025) 最新证明:游戏 RL 技术可用于文本.

Ngọc đá này khảo sát ba kiến trúc nổi bật  AlphaZero, MuZero và GRPO  thông qua một ống kính thống nhất: **self-play + search + policy improvement**. Mỗi một tổng quát trước đó; GRPO đặc biệt là công thức của AlphaZero được áp dụng cho lý luận LLM, với các token như các hành động và xác minh toán học như tín hiệu chiến thắng.

> Cái kết luận này qua một cái nhìn duy nhất**自我博弈+搜索+策略改进**审视三个里程碑架构:AlphaZero、MuZero 和 GRPO── mỗi là một sự quảng bá trước;GRPO đặc biệt sẽ sử dụng các bộ phận của AlphaZero để đưa ra các ý tưởng LLM, biểu tượng là động tác, kiểm tra toán là tín hiệu chiến thắng──

## Khái niệm cốt lõi

![AlphaZero ↔ MuZero ↔ GRPO: same loop, different environments](../assets/rl-games.svg)

**The unifying loop.**

```
while True:
    trajectory = self_play(current_policy, search)     # play game against self
    policy_target = search.improved_policy(trajectory) # search improves raw policy
    policy_net.update(policy_target, value_target)     # supervised on search output
```

**AlphaZero (2017).**Silver et al. Với một trò chơi (chess, shogi, Go) với các quy tắc được biết đến:

- Mạng lưới giá trị chính sách: một tháp `f_θ(s) → (p, v)`- `p`là một tiền nhiệm về các động thái pháp lý.`v`là kết quả trò chơi mong đợi.
- Monte Carlo Tree Search (MCTS): với mỗi chuyển động, mở rộng một cây có thể tiếp tục. Sử dụng `(p, v)`như trước + bootstrap. Chọn các nút theo UCB (PUCT): `a* = argmax Q(s, a) + c · p(a|s) · √N(s) / (1 + N(s, a))`- Tôi không biết.
- tự chơi: chơi trò chơi đại lý-về- đại lý.`t`, phân phối các chuyến thăm của MCTS `π_t`trở thành mục tiêu đào tạo chính sách.
- Lối mất:`L = (v - z)² - π · log p + c · ||θ||²`- `z`là kết quả trò chơi (+1 / 0 / -1).

Không có kiến thức con người, không có tính toán bằng tay, một công thức duy nhất làm chủ cờ vua, shogi và Go sau vài chục triệu trò chơi tự chơi.

> 零人类知识――零手工启发式―― một phương pháp sau hàng ngàn triệu tự hào đã nắm bắt国际象棋,棋牌 và围棋――

**MuZero (2019).**Schrittwieser et al. Tháo bỏ yêu cầu biết các quy tắc.

- Thay vì một môi trường cố định, học một mô hình động lực tiềm ẩn`(h, g, f)`- Có thể là:
  - `h(s)`: mã hóa quan sát vào trạng thái ẩn.
  - `g(s_latent, a)`: dự đoán trạng thái ẩn chứa tiếp theo + phần thưởng.
  - `f(s_latent)`: dự đoán chính sách trước + giá trị.
- MCTS chạy trong không gian ẩn học.
- Làm việc trên Go, cờ vua, shogi và Atari một thuật toán, không có luật lệ.

> Trong vòng tròn, cờ bạc, cờ vua và Atari 上都有效一个算法,无需规则知识.

> **【中文解读】**AlphaZero và MuZero's core cycle:自我博 → MCTS 搜索改进策略 → 监督学习更新网络;; AlphaZero 需要已知游戏规则,MuZero 通过学习隐空间动力学模型消除了这个限制;;

> **【拓展：DeepSeek-R1 与 AlphaZero 范式】**DeepSeek-R1(2025) sẽ áp dụng mô hình AlphaZero cho LLM 推理:token就是动作,推理过程就是"游戏",验证器(数学题对错、代码是否通过测试)就是"胜负信号"──GRPO 替代PPO,组内采样替代自我博──

**Stochastic MuZero (2022).**Thêm động lực stochastic và nút cơ hội; mở rộng đến các trò chơi lớp backgammon.

> **随机 MuZero (2022)。**添加随机动力学和机会节点; mở rộng sang chơi game bi-陆棋类.

**Muesli, Gumbel MuZero (2022-2024).**Cải thiện hiệu quả mẫu và tìm kiếm xác định.

> **Muesli、Gumbel MuZero (2022-2024)。** cải thiện hiệu quả và xác định tìm kiếm mẫu

**GRPO (2024-2025).**Công thức DeepSeek-R1. cùng một vòng lặp hình AlphaZero, áp dụng cho lí luận mô hình ngôn ngữ:

- "Game": trả lời một vấn đề toán học / mã hóa / lý luận. "Win" = xác minh (trình thử nghiệm vượt qua, số lượng trả lời phù hợp) trả lại 1.
- Chính sách: LLM. Các hành động: token.
- Không có nhà phê bình (v_φ kiểu PPO). thay vào đó, cho mỗi lời nhắc, mẫu `G`- Đánh giá tiền thưởng cho mỗi người.**group-relative advantage** `A_i = (r_i - mean_r) / std_r`như là tín hiệu cho việc cập nhật kiểu REINFORCE.
- KL phạt để chính sách tham chiếu để ngăn chặn trôi (như RLHF).
- Lối mất hoàn toàn:

  `L_GRPO(θ) = -E_{q, {o_i}} [ (1/G) Σ_i A_i · log π_θ(o_i | q) ] + β · KL(π_θ || π_ref)`

Không mô hình thưởng, không có nhà phê bình, không có MCTS. Tỷ lệ cơ sở liên quan đến nhóm thay thế cả ba.

> **GRPO (2024-2025)。**DeepSeek-R1 配方── tương tự AlphaZero 形状循环, được áp dụng cho mô hình ngôn ngữ推理:不需要奖励模型、Critic 或 MCTS──组相对基线替代了三者──在推理基准上匹配或超越PPO-RLHF质量,计算量仅为一小部分──

> **【中文解读】**GRPO là sáng tạo cốt lõi của DeepSeek-R1: không cần chỉ trích 网络(省一半内存), sử dụng trong nhóm trung bình và tiêu chuẩn khác biệt xây dựng ưu điểm.

> **【拓展：GRPO→DeepSeek-R1→开源推理革命】**DeepSeek-R1's four-phase training process: cold start SFT → 推理导向 GRPO → 拒采样+SFT → 全谱 GRPO──R1-Zero(纯 GRPO 无 SFT) chứng minh LLM có thể từ零学会推理, nhưng输出可读性差──蒸实验表明: sử dụng mạnh RL giáo viên's推理轨迹 làm SFT,比小模型从头做 RL效果更好──

**The R1 recipe in full.**DeepSeek-R1 (DeepSeek 2025) là hai mô hình trong một bài báo:

> **R1 完整配方。**DeepSeek-R1 là một trong hai mô hình trong bài luận:

- **R1-Zero.**Bắt đầu từ mô hình cơ bản DeepSeek-V3. Không có SFT. Sử dụng GRPO trực tiếp với hai thành phần phần thưởng: * thưởng chính xác * (tựa trên quy tắc  đã phân tích câu trả lời cuối cùng đến số chính xác / mã đã vượt qua các thử nghiệm đơn vị) và * thưởng định dạng * (có hoàn thành chuỗi suy nghĩ của nó trong `<think>…</think>`Trong hàng ngàn bước, độ dài phản ứng trung bình tăng từ ~100 đến ~10,000 token và điểm số chuẩn toán học leo lên gần o1 mức xem trước. Mô hình học cách lý luận từ đầu.
- **R1.**Xác định các vấn đề khả năng đọc của R1-Zero bằng một đường ống bốn giai đoạn:
  1. **Cold-start SFT.**Thu thập vài ngàn biểu hiện CoT dài với định dạng sạch. giám sát-finetune mô hình cơ bản trên chúng. Điều này cung cấp một điểm khởi đầu dễ đọc.
  2. **Reasoning-oriented GRPO.**Sử dụng GRPO với phần thưởng độ chính xác + định dạng cộng với phần thưởng phù hợp với ngôn ngữ để ngăn chặn chuyển đổi mã.
  3. **Rejection sampling + SFT round 2.**lấy mẫu ~ 600K quỹ đạo lý luận từ điểm kiểm soát RL, chỉ giữ những câu trả lời cuối cùng chính xác và CoT có thể đọc được, và kết hợp với ~ 200K ví dụ SFT không lý luận (sự viết, QA, nhận thức về bản thân).
  4. **Full-spectrum GRPO.**Một vòng RL nữa bao gồm cả lý luận (bước thưởng dựa trên quy tắc) và sự sắp xếp chung (bước thưởng dựa trên ưu tiên hữu ích/không hại).

Kết quả tương ứng với o1 trên AIME và MATH-500 ở trọng lượng mở, và đủ nhỏ để chưng cất. cùng một bài báo cũng phát hành sáu mô hình mật độ chưng cất (Qwen-1.5B thông qua Llama-70B) bằng cách SFT'ing trên dấu vết lý luận của R1  không có RL ở học sinh. Chưng cất của một giáo viên RL mạnh liên tục đánh bại RL từ đầu ở quy mô của học sinh.

> Kết quả là AIME và MATH-500 trên phù hợp với O1, và đủ nhỏ có thể蒸──蒸强 RL

**Why GRPO instead of PPO for reasoning.**Ba lý do trong bài báo DeepSeekMath (Từ tháng 2 năm 2024): (1) không có mạng giá trị để đào tạo, giảm bộ nhớ một nửa; (2) cơ sở nhóm tự nhiên xử lý phần thưởng cuối quỹ đạo hiếm khi mà các nhiệm vụ lý luận tạo ra; (3) bình thường hóa mỗi lần làm cho lợi ích tương đương trên các vấn đề khó khăn khác nhau, mà chỉ một nhà phê bình của PPO không thể.

> **为什么推理用 GRPO 而非 PPO。**三个原因: 1) 无需训练值网络,内存减半; 2) 组基线自然处理推理任务产生的稀疏回合末奖励; 3) Mỗi gợi ý tập hợp tạo lợi thế trong sự khác biệt khó khăn lớn trong vấn đề间可比较──

**Search-free vs search-based.**Các trò chơi đã được phân nhánh:

> **Search-free vs search-based.**

- *Các trò chơi thông tin hoàn hảo với chân trời dài * (Go, cờ vua): vẫn dựa trên tìm kiếm. AlphaZero / MuZero thống trị.
- *Làm lý luận LLM*: chưa có MCTS trong sản xuất; GRPO trên các triển khai đầy đủ, tốt nhất của N cho tính toán suy luận.

## Hãy xây dựng nó.
```figure
f3-selfplay-ladder
```

## Hãy xây dựng nó

Mã trong `code/main.py`thực hiện **GRPO in miniature** một tên cướp có nhiều nhóm mẫu. thuật toán giống như trên một LLM; chỉ chính sách và môi trường đơn giản hơn. Nó dạy về *kết quả* và *lợi thế liên quan đến nhóm*, đó là đổi mới năm 2025.

> `code/main.py`Trung 代码 đã thực hiện**微型 GRPO** Một 博机带有多组样本的博机――算法与LLM上相同; chỉ đơn giản hơn; nó giáo dục* mất mát* và*组 đối với lợi thế*, đây là một sáng tạo năm 2025―

### Bước 1: một môi trường xác minh nhỏ

```python
QUESTIONS = [
    {"prompt": "q1", "correct": 3},
    {"prompt": "q2", "correct": 1},
]

def verify(prompt_idx, answer_token):
    return 1.0 if answer_token == QUESTIONS[prompt_idx]["correct"] else 0.0
```

Trong GRPO thực sự, người xác minh chạy các bài kiểm tra đơn vị hoặc kiểm tra sự bình đẳng toán học.

> Thực sự GRPO 中验证器运行单元测试或检查数学等式──

### Bước 2: chính sách: softmax trên K trả lời token mỗi prompt

```python
def policy_probs(theta, p_idx):
    return softmax(theta[p_idx])
```

Tương đương với kết quả lớp cuối cùng của LLM theo điều kiện theo một prompt.

> Lớp giá của LLM trong các bước đầu tư cuối cùng.

### Bước 3: Tiểu mẫu nhóm và lợi thế liên quan đến nhóm

```python
def grpo_step(theta, p_idx, G=8, beta=0.01, lr=0.1, rng=None):
    probs = policy_probs(theta, p_idx)
    samples = [sample(probs, rng) for _ in range(G)]
    rewards = [verify(p_idx, s) for s in samples]
    mean_r = sum(rewards) / G
    std_r = stddev(rewards) + 1e-8
    advs = [(r - mean_r) / std_r for r in rewards]

    for a, A in zip(samples, advs):
        grad = onehot(a) - probs
        for i in range(len(probs)):
            theta[p_idx][i] += lr * A * grad[i]
    # KL penalty: pull theta toward reference
    for i in range(len(probs)):
        theta[p_idx][i] -= beta * (theta[p_idx][i] - reference[p_idx][i])
```

Lợi thế liên quan đến nhóm là thủ thuật DeepSeek 2024. Không cần người phê bình. "Baseline" là trung bình nhóm, và bình thường hóa sử dụng nhóm std.

> 组相对优势是2024年DeepSeek的技巧──无需批判──"基线"是组平均值,归结使用组标准差──

### Bước 4: so sánh với mức cơ sở REINFORCE (không có giá trị)

Tương tự thiết lập, tính toán, đơn giản là REINFORCE. GRPO hội tụ nhanh hơn và ổn định hơn.

> Tương tự như vậy, cùng tính toán, chỉ có REINFORCE.

### Bước 5: quan sát entropy và KL

Các chẩn đoán giống như RLHF: trung bình KL để tham chiếu, entropy chính sách, phần thưởng trên thời gian.

> Tiêu chuẩn chuẩn: KL trung bình đến hướng dẫn chiến lược, chiến lược, thưởng theo thời gian thay đổi.

## Những bẫy

- **Reward hacking via verifier gaming.**GRPO thừa hưởng rủi ro của RLHF: nếu người xác minh sai hoặc có thể khai thác, LLM sẽ tìm thấy lợi dụng.
  **通过验证器博弈的奖励黑客。**GRPO đã thừa hưởng rủi ro của RLHF: Nếu các máy kiểm tra sai hoặc có thể sử dụng, LLM sẽ tìm thấy lỗ hổng.
- **Group size too small.**Sự biến động của nhóm cơ sở là như `1/√G`- Ở dưới đây.`G = 4`, tín hiệu lợi thế là ồn ào; lựa chọn tiêu chuẩn là `G = 8`đến`64`- Tôi không biết.
  **组大小太小。**组基线的方差与 `1/√G`Đúng là vậy.`G = 4`Các tín hiệu có tiếng ồn:`G = 8`Đến`64`
- **Length bias.**LLM hoàn thành với độ dài khác nhau có khả năng log khác nhau. bình thường bằng số lượng token, hoặc sử dụng log-prob cấp độ chuỗi, hoặc cắt ngắn cho chiều dài tối đa.
  **长度偏差。**LLM khác nhau độ dài  hoàn thành có tỷ lệ đối số khác nhau  theo mã số kết hợp hoặc cắt ngang cho độ dài tối đa 
- **Pure self-play cycles.**Trình luyện theo kiểu AlphaZero có thể bị mắc kẹt trong vòng thống trị trong các trò chơi tổng cộng.
  **纯自我博弈循环。**AlphaZero 式训练在一般和博上可能陷入控制循环──通过多样化对手池缓解──
- **Search-policy mismatch.**AlphaZero đào tạo chính sách để bắt chước kết quả tìm kiếm. Nếu mạng lưới chính sách quá nhỏ để đại diện cho phân phối tìm kiếm, đào tạo sẽ dừng lại.
  **搜索-策略不匹配。**AlphaZero 训练策略模仿搜索输出── Nếu chiến lược mạng quá nhỏ không thể hiển thị phân bố tìm kiếm, đào tạo bị đình trệ──
- **Compute floor.**MuZero / AlphaZero cần tính toán lớn. Một lần bỏ thường là hàng trăm giờ GPU.
  **计算下限。**MuZero/AlphaZero 需要大量计算.
- **Verifier coverage.**Các thử nghiệm đơn vị vượt qua cho một giải pháp lỗi tăng cường lỗi. Thiết kế xác minh để bắt được các trường hợp cạnh.
  **验证器覆盖。**通过有 bug 解决方案的单元测试会强化 bug;;设计能捕获边缘情况的验证器;;

## Hãy sử dụng nó để thực hiện

Khảo cảnh game-RL năm 2026, theo lĩnh vực:

> 2026 年游戏 RL 版图, theo lĩnh vực:

| Domain | Dominant method |
|--------|-----------------|
| Domain / 领域 | Dominant method / 主导方法 |
| Two-player zero-sum board games (Go, chess, shogi) / 双人零和棋类 | AlphaZero / MuZero / KataGo |
| Imperfect info card games (poker) / 不完全信息纸牌 | CFR + deep learning (DeepStack, Libratus, Pluribus) / CFR + 深度学习 |
| Atari / pixel games / Atari/像素游戏 | Muesli / MuZero / IMPALA-PPO |
| Large multiplayer strategy (Dota, StarCraft) / 大型多人策略 | PPO + self-play + league (OpenAI Five, AlphaStar) |
| LLM math/code reasoning / LLM 数学/代码推理 | GRPO (DeepSeek-R1, Qwen-RL, open replications) |
| LLM alignment / LLM 对齐 | DPO / RLHF-PPO (not GRPO; verifier is preference not verifiable) / DPO/RLHF-PPO |
| Robotics / 机器人 | PPO + DR (not game-RL, but uses same policy-gradient tools) / PPO+DR |
| Combinatorial problems / 组合问题 | AlphaZero variants (AlphaTensor, AlphaDev) / AlphaZero 变体 |

* Công thức *  tự chơi, cải thiện tìm kiếm, phân giải chính sách  trải dài trên văn bản, pixel và kiểm soát vật lý. GRPO là phiên bản trẻ nhất; nhiều hơn nữa đang đến.

> Đây là một trong những cách thức mới nhất của việc tìm kiếm bản thân, tìm kiếm cải tiến, tìm kiếm cải tiến, tìm kiếm kỹ thuật, tìm kiếm kỹ thuật và kiểm soát vật lý.

## Chuyển nó đi.

Cứ như `outputs/skill-game-rl-designer.md`- Có thể là:

```markdown
---
name: game-rl-designer
description: Design a game-RL or reasoning-RL training pipeline (AlphaZero / MuZero / GRPO) for a given domain.
version: 1.0.0
phase: 9
lesson: 12
tags: [rl, alphazero, muzero, grpo, self-play]
---

Given a target (perfect-info game / imperfect-info / Atari / LLM reasoning / combinatorial), output:

1. Environment fit. Known rules? Markov? Stochastic? Multi-agent? Informs AlphaZero vs MuZero vs GRPO.
2. Search strategy. MCTS (PUCT with learned prior), Gumbel-sampled, best-of-N, or none.
3. Self-play plan. Symmetric self-play / league / offline data / verifier-generated.
4. Target signal. Game outcome / verifier reward / preference / learned model. Include robustness plan.
5. Diagnostics. Win rate vs baseline, ELO curve, verifier pass rate, KL to reference.

Refuse AlphaZero on imperfect-info games (route to CFR). Refuse GRPO without a trusted verifier. Refuse any game-RL pipeline without a fixed baseline opponent set (self-play ELO is uncalibrated otherwise).
```

## Tập luyện bài tập

1. **Easy.**Thực hiện hành vi của GRPO trong `code/main.py`. Đào tạo trên 2 lời nhắc × 4 mã thông báo trả lời mỗi.`G=8`- Tôi không biết.
2. **Medium.**Chuẩn bị PPO (cắt) và vanilla REINFORCE. So sánh hiệu quả mẫu và sự khác biệt phần thưởng với GRPO trên cùng một tên cướp.
3. **Hard.**Tăng đến một "sợi dây chuyền lý luận" dài-2: đại lý phát ra hai token và người xác minh thưởng cho cặp. đo lường cách GRPO xử lý giao tín dụng qua chuỗi hai bước. (Công dẫn: tính toán lợi thế nhóm cho mỗi * chuỗi đầy đủ*, lan rộng đến cả hai vị trí token.)

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| MCTS | "Tree search with learned net" / 蒙特卡洛树搜索 | Monte Carlo Tree Search; UCB1/PUCT selection with learned `(p, v)` priors. |
| AlphaZero | "Self-play + MCTS" / AlphaZero | Policy-value net trained to match MCTS visits and game outcome. |
| MuZero | "Learned-model AlphaZero" / MuZero | Same loop but in latent space via learned dynamics. |
| GRPO | "Critic-free PPO" / 组相对策略优化 | Group Relative Policy Optimization; REINFORCE with group-mean baseline + KL. |
| PUCT | "AlphaZero's UCB" / PUCT 选择公式 | `Q + c · p · √N / (1 + N_a)` — balances value estimate with prior. |
| Self-play | "Agent vs past self" / 自我博弈 | Standard for zero-sum; symmetric training signal. |
| League play | "Population-based self-play" / 联盟训练 | Past + current + exploiters sampled as opponents. |
| Verifier reward | "Verifiable RL" / 验证器奖励 | Reward comes from a deterministic checker (tests pass, answer matches). |
| Process reward | "PRM" / 过程奖励模型 | Scores each reasoning step, not just the final answer. |

## Xem thêm 延伸阅读

- [Silver et al. (2017). Mastering the game of Go without human knowledge (AlphaGo Zero)](https://www.nature.com/articles/nature24270)- Tôi không biết.
- [Silver et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play (AlphaZero)](https://www.science.org/doi/10.1126/science.aar6404)- Tôi không biết.
- [Schrittwieser et al. (2020). Mastering Atari, Go, chess and shogi by planning with a learned model (MuZero)](https://www.nature.com/articles/s41586-020-03051-4)- Tôi không biết.
- [Vinyals et al. (2019). Grandmaster level in StarCraft II (AlphaStar)](https://www.nature.com/articles/s41586-019-1724-z)- Tôi không biết.
- [DeepSeek-AI (2024). DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO)](https://arxiv.org/abs/2402.03300) bài báo giới thiệu GRPO và cơ sở liên quan đến nhóm.
- [DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) công thức R1 đầy đủ bốn giai đoạn cộng với R1-Zero ablation.
- [Brown et al. (2019). Superhuman AI for multiplayer poker (Pluribus)](https://www.science.org/doi/10.1126/science.aay2400) CFR + học sâu quy mô.
- [Tesauro (1995). Temporal Difference Learning and TD-Gammon](https://dl.acm.org/doi/10.1145/203330.203343)- Báo bắt đầu mọi chuyện.
- [Hugging Face TRL — GRPOTrainer](https://huggingface.co/docs/trl/main/en/grpo_trainer) tham chiếu sản xuất để áp dụng GRPO với các chức năng thưởng tùy chỉnh.
- [Qwen Team (2024). Qwen2.5-Math — GRPO replication](https://github.com/QwenLM/Qwen2.5-Math) sao chép mở của công thức R1 ở nhiều quy mô.
- [Sutton & Barto (2018). Ch. 17 — Frontiers of Reinforcement Learning](http://incompleteideas.net/book/RLbook2020.pdf) khung sách giáo khoa cho tự chơi, tìm kiếm và "bảo quy định phần thưởng" mà R1 trình bày ở quy mô LLM.
