# MARL  MADDPG, QMIX, MAPPO  MADDPG MAPPO MARL QMIX

> Di sản tăng cường học tập của phối hợp đa đại lý, vẫn còn thông báo cho các hệ thống LLM-agent vào năm 2026. **MADDPG**(Lowe et al., NeurIPS 2017, arXiv:1706.02275) giới thiệu Căn bộ tập trung, Thực hiện phi tập trung (CTDE): mỗi nhà phê bình nhìn thấy tất cả các trạng thái và hành động của các đại lý trong quá trình đào tạo; vào thời gian thử nghiệm chỉ có các diễn viên địa phương chạy.**QMIX**(Rashid et al., ICML 2018, arXiv:1803.11485) là sự phân hủy giá trị với một mạng hỗn hợp đơn giản; mỗi chất phản ứng Qs kết hợp thành chung Q so `argmax`phân phối sạch  thống trị trên StarCraft Multi-Agent Challenge (SMAC). **MAPPO**(Yu et al., NeurIPS 2022, arXiv:2103.01955) là PPO với chức năng giá trị tập trung; "sự hiệu quả đáng ngạc nhiên" trên thế giới hạt, SMAC, Google Research Football, Hanabi với điều chỉnh tối thiểu.**default 2026 cooperative-MARL baseline**Bài học này xây dựng mỗi từ một đồ chơi nhỏ của thế giới lưới và hạ cánh ba ý tưởng trong trí nhớ cơ trước khi chạm vào đào tạo đại lý LLM.

> **【中文解读】**Bài viết này giới thiệu nhiều Agent 强化学习MADDPG、QMIX、MAPPO 等多 Agent RL 算法。

> **【拓展：marl maddpg qmix mappo→具体应用】**Nhiều đại lý 强化学习(MARL) thuật toán:(1) MADDPG mỗi đại lý có độc lập Actor-Critic, nhưng các nhà phê bình có thể xem tất cả các động tác của đại lý;(2) QMIX tập trung đào tạo phân tán thực hiện, thông qua hỗn hợp mạng bảo đảm đơn调性;(3) MAPPOPPO's nhiều đại lý 扩展──2026 MARL đạt được tiến bộ trong trò chơi AI、机器人协作和交通控制, nhưng trong LLM Agent ứng dụng vẫn còn sớm.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, small NumPy-free implementations) | **语言:** Python（标准库，无 NumPy 的小型实现）
**Prerequisites:** Phase 09 (Reinforcement Learning), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 09（强化学习），Phase 16 · 09（并行群体网络）

>  **【前置】**学本节前请先掌握:Phase 09(RL 基础 PPO/Q-learning) 、Phase 16·09(Swarm) ・MARL = 多 Agent 强化学习,CTDE(集中训练分散执行) là mô hình cốt lõi。
>  **【类比】**MARL = "trenh tập đội bóng"──MADDPG = 教练看全场训练(集中评论),比赛时球员各自决策(分散演员);QMIX = Mỗi người một Q 值,单调混合保证最优解可分;MAPPO = PPO 多 Agent 版本──MAPPO 是 2026 合作 MARL 默认基线("lực kỳ hiệu quả"),SMAC、Google Football、Hanabi 都能少调参跑通──LLM Agent 训练也借鉴这套范式──
**Time:** ~90 minutes | **时间:** ~90 分钟

##                                                                                                                                                                                                                                                               

Các hệ thống đại lý LLM ngày càng đào tạo các chính sách phối hợp giữa các đại lý: khi nào trì hoãn, khi nào hành động, ai đồng nghiệp để gọi. Văn học cho bạn biết cách đào tạo các chính sách như vậy là Học tập tăng cường đa đại lý (MARL), vốn trước sóng LLM và có một bộ nhỏ các thuật toán thống trị.

> LLM-Agent 系统越来越地训练 Agent 间协调策略:何时延迟、何时行动、调用哪个同伴──告诉你如何训练这些策略的文献是多 Agent 强化学习 ((MARL), nó sớm hơn LLM 潮潮, có một小组 dẫn đầu thuật toán──

Đọc các bài báo MARL mà không có từ vựng mẫu là đau đớn. Trình đào tạo tập trung với thực thi phi tập trung (CTDE), phân hủy giá trị và phê bình tập trung không phải là từ buzzword  họ là câu trả lời cụ thể cho các vấn đề cụ thể:

> 没有模式词汇表阅读 MARL 论文是痛苦的──集中训练分散执行(CTDE) 价值分解和集中式评论家不是流行词它们是特定问题的特定答案:

- RL độc lập (mỗi đại lý học một mình) là không tĩnh trong quan điểm của mỗi đại lý.
  Trung ngữ翻译:独立 RL(每个 Agent 独立学习) Từ góc nhìn của mỗi Agent 看不平稳的──不好──
- RL tập trung (một đại lý kiểm soát tất cả) không mở rộng và vi phạm các hạn chế thực hiện.
  Trung文翻译:集中式 RL(一个代理 控制所有) không thể mở rộng và vi phạm thực hiện约束。
- CTDE có được những lợi ích tốt nhất: đào tạo với thông tin toàn cầu, triển khai với các chính sách địa phương.
  Trung ngữ翻译:CTDE 兼得两者之长: dùng toàn局信息训练, dùng局部策略部署

## Khái niệm cốt lõi

### Ba môi trường sử dụng các giấy tờ

- **Particle World (multi-agent particle env).**Phí-siết 2D đơn giản với các nhiệm vụ hợp tác/ cạnh tranh.
- **StarCraft Multi-Agent Challenge (SMAC).**- Quản lý nhỏ hợp tác, quan sát một phần, thử nghiệm của QMIX, hành động riêng biệt, trạng thái liên tục.
- **Google Research Football, Hanabi, MPE.**MAPPO cơ sở.

Các môi trường khác nhau có các loại hành động / quan sát khác nhau.

### MADDPG (2017)  mô hình CTDE

Mỗi đại lý `i`có một diễn viên `mu_i(o_i)`Điều này có nghĩa là mỗi nhân viên cũng có một nhà phê bình.`Q_i(x, a_1, ..., a_n)`người diễn viên được cập nhật theo tỷ lệ chính sách so với đánh giá của nhà phê bình.

```
actor update:    grad_theta_i J = E[grad_theta mu_i(o_i) * grad_a_i Q_i(x, a_1..n) at a_i=mu_i(o_i)]
critic update:   TD on Q_i(x, a_1..n) given next-state joint estimate
```

Tại sao CTDE: trong thời gian đào tạo, chúng ta biết hành động của mọi người; chúng ta sử dụng điều đó để giảm sự khác biệt trong mỗi nhà phê bình.`o_i`và gọi điện`mu_i(o_i)`- Tôi không biết.

Chế độ thất bại: các nhà phê bình phát triển với các đại lý N (tài nhập bao gồm tất cả các hành động). Không mở rộng vượt quá ~ 10 đại lý mà không có các ước tính.

### QMIX (2018)  phân hủy giá trị

Chỉ hợp tác. Giải thưởng toàn cầu là tổng của một hàm đơn giản của các giá trị Q mỗi đại lý:

```
Q_tot(tau, a) = f(Q_1(tau_1, a_1), ..., Q_n(tau_n, a_n)),   df/dQ_i >= 0
```

Sự đơn thuần đảm bảo `argmax_a Q_tot`có thể được tính toán bởi mỗi đại lý chọn `argmax_{a_i} Q_i`độc lập.**exactly the decentralized execution property**Khi tập luyện, một mạng hỗn hợp tạo ra`Q_tot`từ các chất lượng Qs mỗi đại lý.

Tại sao QMIX thắng SMAC: quản lý nhỏ StarCraft hợp tác có các đại lý đồng nhất, công ty địa phương, phần thưởng toàn cầu  hoàn hảo phù hợp với sự phân hủy giá trị.

Chế độ thất bại: giới hạn đơn vị hạn chế; một số nhiệm vụ có cấu trúc phần thưởng không phân hủy đơn vị (một đại lý hy sinh cho nhóm).

### MAPPO (2022)  sự cố bị bỏ qua

Multi-Agent PPO: PPO với một chức năng giá trị tập trung. Mỗi đại lý có chính sách riêng của mình; tất cả các đại lý chia sẻ (hoặc có mỗi đại lý) các chức năng giá trị nhìn thấy trạng thái đầy đủ. Yu et al. 2022 so sánh MAPPO với MADDPG, QMIX, và các tiện ích của chúng trên năm tiêu chuẩn và tìm thấy:

- MAPPO phù hợp hoặc vượt qua các phương pháp MARL ngoài chính sách trên thế giới hạt, SMAC, Google Research Football, Hanabi, MPE.
- Mức độ điều chỉnh siêu tham số tối thiểu cần thiết.
- Trình luyện ổn định; có thể tái tạo qua các hạt giống.

Cộng đồng đã đánh giá thấp MARL về chính sách cho đến khi bài báo này. Năm 2026, MAPPO là cơ sở mặc định cho MARL hợp tác; bất kỳ phương pháp mới nào phải đánh bại nó.

### Tại sao các kỹ sư đại lý LLM nên quan tâm

Ba sử dụng trực tiếp:

1. **Router training.**Một siêu đại lý chọn bộ phận đại lý nào xử lý một nhiệm vụ. Đây là vấn đề MARL với N phân cấp đại lý và một bộ định tuyến tập trung. MAPPO phù hợp.
2. **Role emergence.**Trong các mô phỏng nhân tạo, các nhân viên đào tạo để chấp nhận vai trò bổ sung theo thời gian là một vấn đề MARL ẩn náu.
3. **Multi-agent tool use.**Khi các đại lý chia sẻ công cụ và cạnh tranh về ngân sách, đào tạo họ thông qua CTDE tạo ra các chính sách địa phương có thể triển khai được tôn trọng hạn chế nguồn lực.

Lưu ý thực tế: vào năm 2026, hầu hết các hệ thống đại lý LLM sản xuất thúc đẩy chính sách của họ thay vì đào tạo họ. MARL đến khi bạn có (a) rất nhiều dữ liệu tương tác, (b) một tín hiệu phần thưởng rõ ràng, và (c) sẵn sàng đầu tư vào cơ sở hạ tầng đào tạo.

### CTDE như một mô hình thiết kế ngoài RL

Ngay cả khi không có đào tạo, CTDE là một mô hình kiến trúc hữu ích:

- Trong quá trình thiết kế, đảm bảo toàn bộ khả năng nhìn thấy của nhóm.
- Tại * runtime*, thực thi thực thi phi tập trung: mỗi đại lý chỉ thấy `o_i`- Tôi không biết.

Các mô hình buộc bạn phải giữ cho trạng thái mỗi đại lý rõ ràng và suy nghĩ về khả năng quan sát một phần trước. Nhiều hệ thống sản xuất đa đại lý lặng lẽ giả định trạng thái chia sẻ ở khắp mọi nơi.

### Vấn đề không ổn định

Khi nhiều đại lý học cùng một lúc, môi trường của mỗi đại lý (bao gồm các chính sách của những người khác) là không tĩnh.

- MADDPG: Nhà phê bình toàn cầu nhìn thấy tất cả các hành động, vì vậy ước tính giá trị của nó là không ổn định.
- QMIX: phân hủy giá trị di chuyển học tập đến một không gian chung-Q nơi tối ưu được xác định rõ ràng.
- MAPPO: chức năng giá trị tập trung làm giảm sự khác biệt từ những thay đổi chính sách của người khác.

Trong hệ thống đại lý LLM, sự không ổn định biểu hiện như "nhà nhân của tôi đã làm việc tháng trước, bây giờ khi đại lý khác lên dòng thay đổi, mỏ có hành vi sai trái".

### Bài học này không bao gồm

Việc đào tạo các mạng thực tế là một chủ đề giai đoạn 9. Bài học này xây dựng các phiên bản chính sách kịch bản cho thấy CTDE, phân hủy giá trị và mô hình giá trị tập trung mà không cần cập nhật gradient. Mục tiêu là nội bộ hóa các mô hình trước khi bạn lấy một thư viện MARL đầy đủ (PyMARL, MARLlib, RLlib đa đại lý).

## Hãy xây dựng nó.
```figure
sw-ctde
```

## Hãy xây dựng nó

`code/main.py`thực hiện ba mô hình biểu hiện, tất cả trên một mạng lưới hợp tác 2 nhân viên nhỏ:

- Môi trường: 2 đại lý trên lưới 4x4, một viên thưởng.
  Trung ngữ翻译:环境:2 个代理 在 4x4 网格上,一个奖励颗粒──任何代理到达颗粒则奖励 = 1;任务结束──
- `IndependentAgents` mỗi tác nhân đối xử với những tác nhân khác như môi trường.
  Trung ngữ翻译:`IndependentAgents`Mỗi đại lý sẽ là đại lý khác theo môi trường.
- `MADDPGStyle` Nhà phê bình tập trung tính toán một giá trị chung; các chính sách của các diễn viên cập nhật từ đó.
  Trung ngữ翻译:`MADDPGStyle` 集中式评论家计算联合值;Actor 策略从中更新──脚本化策略改进──
- `QMIXStyle` phân hủy giá trị bằng máy trộn đơn tông.
  Trung ngữ翻译:`QMIXStyle` 带单调混合器的值分解──
- `MAPPOStyle` chức năng giá trị tập trung; chính sách cập nhật so với đường cơ sở chia sẻ.
  Trung ngữ翻译:`MAPPOStyle` 集中式值函数;策略对共享基线更新。

Cả bốn tập đều chạy cùng một tập và báo cáo trung bình các bước đến mục tiêu.

> Tất cả bốn hoạt động cùng vòng lặp và báo cáo đạt được số bước mục tiêu trung bình.

Đi chạy:

```
python3 code/main.py
```

Khả năng đầu ra dự kiến: các đại lý độc lập trung bình mất ~ 6 bước; các biến thể CTDE hội tụ đến ~ 3.5 bước (tối ưu cho lưới 4x4 là 3). Sự khác biệt mô hình xuất hiện mặc dù các chính sách kịch bản.

## Sử dụng nó.

`outputs/skill-marl-picker.md`là một kỹ năng chọn một thuật toán MARL cho một nhiệm vụ đa đại lý: hợp tác đối với cạnh tranh, đồng nhất đối với đa nhất, loại không gian hành động, quy mô, tín hiệu phần thưởng.

## Đưa nó lên mạng

MARL trong sản xuất là hiếm khi.

- **Start with MAPPO.**Bài báo năm 2022 đã thiết lập điều này như là đường cơ sở; tái tạo nó trước tiên tiết kiệm hàng tuần theo đuổi các phương pháp sang trọng hơn.
  Trung ngữ翻译:**从 MAPPO 开始。**Bài báo năm 2022 sẽ được thiết lập như một nền tảng; trước đó, nó có thể tiết kiệm nhiều tuần theo đuổi thời gian phong phú hơn.
- **Log every agent's observation and action stream.**Việc giải quyết lỗi MARL mà không có dấu vết của một nhân viên là vô vọng.
  Trung ngữ翻译:**记录每个 Agent 的观察和动作流。**Không có nhân viên nào làm việc trong MARL là không có gì.
- **Separate training code from execution code.**CTDE là một kỷ luật; để con đường thực hiện thực sự chỉ thấy `o_i`- Tôi không biết.
  Trung ngữ翻译:**分离训练代码和执行代码。**CTDE là một cách thức thực hiện; hãy thực hiện các đường thực sự chỉ nhìn thấy`o_i`
- **Reward shaping warning.**MARL rất nhạy cảm với việc thiết kế phần thưởng, một lỗi phối hợp trong việc hình thành và các đại lý học cách khai thác nó.
  Trung ngữ翻译:**奖励塑形警告。**MARL đối với thiết kế giải thưởng rất nhạy cảm. Một lỗi phối hợp trong hình dạng nhựa sẽ cho phép đại lý học sử dụng nó.
- **For LLM agents**Đầu tiên, hãy xem xét các chính sách cấp độ nhanh. Chỉ đầu tư vào đào tạo MARL khi dữ liệu tương tác + tín hiệu phần thưởng + cơ sở hạ tầng đều có mặt.
  Trung ngữ翻译:**对于 LLM Agent**, trước tiên xem xét các chiến lược cấp độ. Chỉ có trong giao tiếp dữ liệu +  báo cáo thưởng +  cơ sở hạ tầng đều có thời gian để đầu tư MARL  đào tạo.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- đo khoảng cách từ bước đến mục tiêu giữa các đại lý độc lập và các đại lý kiểu MAPPO.
2. Thực hiện một biến thể cạnh tranh: hai đại lý, một viên, chỉ người đầu tiên đạt được phần thưởng.
3. Đọc MADDPG (arXiv:1706.02275) Phần 3. Thực hiện chính xác điều chỉnh phê bình chính xác theo mã giả trong lời của bạn.
4. Đọc MAPPO (arXiv:2103.01955). Tại sao các tác giả lập luận giá trị tập trung + PPO đánh bại MARL ngoài chính sách trên các tiêu chuẩn của họ?
5. Sử dụng CTDE như một mô hình thiết kế cho một hệ thống đại lý LLM giả thuyết (ví dụ, đại lý nghiên cứu + tổng hợp + lập trình).

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MARL / 多 Agent 强化学习 | "Multi-Agent RL" / "多 Agent 强化学习" | Reinforcement learning for multi-agent systems. / 多 Agent 系统的强化学习。 |
| CTDE / 集中训练分散执行 | "Centralized Training, Decentralized Execution" / "集中训练分散执行" | Train with global info; deploy with local policies. / 用全局信息训练；用局部策略部署。 |
| MADDPG | "Multi-Agent DDPG" / "多 Agent DDPG" | CTDE with per-agent critic seeing all observations + actions. / CTDE，每个 Agent 的评论家看到所有观察 + 动作。 |
| QMIX / 值分解 | "Value decomposition" / "值分解" | Monotonic mixing of per-agent Qs. Cooperative. / 每 Agent Q 的单调混合。协作型。 |
| MAPPO / 多 Agent PPO | "Multi-Agent PPO" / "多 Agent PPO" | PPO with centralized value function. 2026 default baseline. / 带集中式值函数的 PPO。2026 默认基线。 |
| Value decomposition / 值分解 | "Sum of individual Qs" / "个体 Q 之和" | Joint Q represented as a monotone function of per-agent Qs. / 联合 Q 表示为每 Agent Q 的单调函数。 |
| Non-stationarity / 非平稳性 | "Moving targets" / "移动目标" | Each agent's env changes as others learn. The core MARL problem. / 每个 Agent 的环境随着其他 Agent 学习而变化。核心 MARL 问题。 |
| On-policy / off-policy / 同策略/离策略 | "Learn from current / replay" / "从当前/回放学习" | PPO is on-policy (MAPPO); DDPG and Q-learning are off-policy. / PPO 是同策略（MAPPO）；DDPG 和 Q-learning 是离策略。 |
| SMAC / 星际争霸多 Agent 挑战 | "StarCraft Multi-Agent Challenge" / "星际争霸多 Agent 挑战" | Cooperative micromanagement benchmark; QMIX's homegrown ground. / 协作微操基准；QMIX 的主战场。 |

## Xem thêm 延伸阅读

- [Lowe et al. — Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments](https://arxiv.org/abs/1706.02275) MADDPG; NeurIPS 2017
- [Rashid et al. — QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning](https://arxiv.org/abs/1803.11485) QMIX; ICML 2018
- [Yu et al. — The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games](https://arxiv.org/abs/2103.01955) MAPPO; NeurIPS 2022
- [BAIR blog post on MAPPO](https://bair.berkeley.edu/blog/2021/07/14/mappo/) Quá trình đọc được kết quả MAPPO
- [SMAC repository](https://github.com/oxwhirl/smac) StarCraft Multi-Agent Challenge
