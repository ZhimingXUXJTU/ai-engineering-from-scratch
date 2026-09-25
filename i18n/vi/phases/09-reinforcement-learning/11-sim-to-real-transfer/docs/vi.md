# Sim-to-Real Transfer 仿真到现实迁移

> Một chính sách được đào tạo trong một máy mô phỏng mà thất bại trên phần cứng là một chính sách ghi nhớ máy mô phỏng.

> **【中文解读】**Nếu không thể làm việc trên các thiết bị thực, hãy cho thấy nó "được phù hợp" với các thiết bị giả mạo.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 08 (PPO), Phase 2 · 10 (Bias/Variance) | **前置知识:** Phase 9 · 08 (PPO), Phase 2 · 10 (偏差/方差)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Trình luyện một robot thực sự là chậm, nguy hiểm và tốn kém. Một con đôi đạp phải mất hàng triệu tập tập để học cách đi bộ; một con đạp thực sự rơi xuống ngay cả khi phá vỡ phần cứng.

>  Trình máy thực sự chậm, nguy hiểm và đắt tiền.  Một máy đôi chân cần hàng triệu tập để học cách đi.  Một máy đôi chân thực ngay cả khi rơi một lần cũng có thể làm hỏng phần cứng. 

Nhưng máy mô phỏng sai. Các vòng đệm có độ chi phối nhiều hơn các mô hình MuJoCo. Các máy ảnh có độ biến dạng ống kính mà máy mô phỏng không bao gồm. Các động cơ có sự chậm trễ, phản ứng ngược và bão hòa mà 99% các mô hình sim bỏ qua. gió, bụi và ánh sáng biến đổi phá hoại một chính sách được đào tạo về rendering vô sinh.**reality gap** Sự khác biệt có hệ thống giữa phân phối sim và phân phối thực  là vấn đề trung tâm của RL được triển khai cho robot.

> Nhưng máy giả là sai lầm. 轴承 có nhiều xung hơn mô hình MuJoCo. 相机 có máy giả không bao gồm các thay đổi ống kính. 电机 có độ trì hoãn, khoảng cách và , 99% mô hình giả đã nhảy qua những điều này.**现实鸿沟**Sự khác biệt hệ thống giữa phân bố thực tế và phân bố thực tế là vấn đề cốt lõi của RL của triển khai máy tính.

Bạn cần một chính sách có khả năng chuyển đổi phân phối sim-to-real. Ba cách tiếp cận lịch sử: ngẫu nhiên mô phỏng (ngẫu nhiên phân phối miền), điều chỉnh chính sách với một chút dữ liệu thực (ngh thích ứng / điều chỉnh tinh tế miền), hoặc xác định các tham số của hệ thống thực và phù hợp với chúng (chẩn đoán hệ thống). Năm 2026, công thức thống trị kết hợp cả ba với mô phỏng song song lớn (Isaac Sim, Isaac Lab, Mujoco MJX trên GPU).

> Bạn cần một chiến lược để giả tạo cho phân bố thực sự chuyển hướng (ru棒) ⋅ 3 phương pháp lịch sử:随机化 (随机化) ⋅ sử dụng ít dữ liệu thực tế (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác nhau (transactional) ⋅ 3 phương pháp khác) ⋅ 3 phương pháp khác (transactional) ⋅ 3

> **【中文解读】**"现实沟" là vấn đề cốt lõi của RL của máy tính. Có 3 giải pháp: 1) Dòng tự động hóa trong quá trình đào tạo để làm cho chiến lược trở nên tốt hơn; 2) Dòng tự thích ứng với ít dữ liệu thực tế nhỏ hơn; 3) Hệ thống nhận thức đo các yếu tố thực sự sửa đổi các thiết bị giả lập.

> **【拓展：域随机化→大模型泛化】**域随机化思想在LLM 训练中也有应应:数据增强 (数据增强) (同义改写、噪声注入) là " phân bố tự động hóa 训练" để nâng cao khả năng phổ biến hóa.

## Khái niệm cốt lõi

![Three sim-to-real regimes: domain randomization, adaptation, system identification](../assets/sim-to-real.svg)

**Domain Randomization (DR).**Tobin và các đồng nghiệp. 2017, Peng et al. Năm 2018. Trong quá trình đào tạo, ngẫu nhiên tất cả các tham số sim có thể khác nhau trên robot thực: khối lượng, hệ số soá, tăng PD động cơ, tiếng ồn cảm biến, vị trí máy ảnh, ánh sáng, kết cấu, mô hình tiếp xúc. Chính sách học được một phân phối điều kiện về "những sim nó là trong ngày hôm nay" và tổng quát trên toàn phạm vi. Nếu robot thực sự nằm trong bao bì huấn luyện, chính sách sẽ hoạt động.

> **域随机化（DR）。**Trong thời gian tập luyện, tự động hóa mỗi có thể và các tham số giả tạo khác nhau với máy tính thực: chất lượng, hệ số摩擦, điện thoại PD  tăng lợi, cảm biến tiếng ồn, vị trí ảnh, ánh sáng,纹理, mô hình tiếp xúc.

- **Upside:**Không cần dữ liệu thực sự. Một công thức, nhiều robot.
  **优点：**Không cần dữ liệu thực. Một cách thức, nhiều loại máy.
- **Downside:**Việc đào tạo vô tình tạo ra một chính sách "tối đa" nhưng quá thận trọng.
  **缺点：** Tập luyện tự nhiên quá nhiều tạo ra "chế tắc chung" nhưng quá bảo thủ.

**System Identification (SI).**Nếu bạn có thể đo lường độ soá cánh tay trên robot thực, hãy kết nối nó vào bộ mô phỏng. Sau đó tập một chính sách dự đoán các giá trị đó.

> **系统辨识（SI）。**训练前将仿真器参数适合真实世界数据――需要接触真实系统但直接缩小现实沟──

**Domain Adaptation.**Trình luyện trong bộ Sim, điều chỉnh tinh tế với một lượng nhỏ dữ liệu thực.

> **域自适应。**Trong thực tập, sử dụng một số lượng nhỏ dữ liệu thực tế.

- **Real2Sim2Real:**học một mô phỏng dư thừa `f(s, a, z) - f_sim(s, a)`sử dụng các bản triển khai thực, tập luyện trong bộ nhớ sim đã sửa chữa.
  **Real2Sim2Real：**Sử dụng thực sự triển khai học tập dư差仿真器, trong sửa đổi sau khi thực hiện thực hiện trong tập luyện.
- **Observation adaptation:**đào tạo một chính sách lập bản đồ thực obs → sim-like obs thông qua một bộ trích dẫn tính năng học (ví dụ, GAN pixel-to-pixel).
  **观测自适应：**训练将真实观测映射为仿真式观测的策略──

**Privileged learning / teacher-student.**Miki et al. 2022 (ANYmal quadruped). Trén một * giáo viên * trong mô phỏng có quyền truy cập vào thông tin đặc quyền (trận lưỡng lự chân lý mặt đất, độ cao địa hình, IMU drift). Chưa một * học sinh * chỉ nhìn thấy quan sát cảm biến thực. Học sinh học được suy luận các tính năng đặc quyền từ lịch sử, mạnh mẽ qua các tham số vật lý.

> **特权学习/教师-学生。**Trong thực tập thực tập có quyền truy cập đặc quyền thông tin của * giáo viên *。蒸 one only see real传感器观测的*学生*。学生从历史推断特权特征。

**Massively parallel simulation.**20242026. Isaac Lab, Mujoco MJX, Brax tất cả chạy hàng ngàn robot song song trên một GPU duy nhất. PPO với 4.096 nhân vật song song thu thập nhiều năm kinh nghiệm trong vài giờ. "các khoảng cách thực tế" thu hẹp khi phân phối đào tạo mở rộng; DR trở nên gần như miễn phí khi mỗi trong số 4.096 envs có các tham số ngẫu nhiên khác nhau.

> **大规模并行仿真。**2024-2026 năm。 Isaac Lab、Mujoco MJX、Brax trên một GPU chạy hàng ngàn máy tính đồng hành。PPO  cộng tác với 4.096 máy tính đồng hành hình con người người trong vài giờ thu thập nhiều năm kinh nghiệm。 Khi sự phân bố đào tạo ngày càng rộng, "现实沟" đã giảm đi。

**The real-world 2026 recipe (quadruped walking example):**

1. Sim song song lớn với trọng lực ngẫu nhiên, độ chà, tăng động cơ, tải trọng.
2. Chính sách giáo viên được đào tạo với thông tin đặc quyền (kìa đồ địa hình, tốc độ cơ thể thực tế mặt đất).
3. Chính sách học sinh được thu hút từ giáo viên chỉ sử dụng proprioception (code bộ phận ghép chân).
4. Chuẩn bị quan sát tùy chọn thông qua mã tự động trên IMU thực.
5. Đưa ra, không chụp trên 10 môi trường, nếu không, hãy điều chỉnh thực tế bằng cách sử dụng PPO.

> **真实世界 2026 年方案（四足行走示例）：**Đại quy mô并行仿真 + 域随机化 → 师策略(特权信息)→ 学生策略蒸(仅本体感受)→ 可选观测自适应 → 部署。零样本迁移到10+ 环境。 Nếu thất bại, làm vài phút an toàn约束 PPO 真实世界微调。

## Hãy xây dựng nó.
```figure
f3-reality-gap
```

## Hãy xây dựng nó

Mã bài học này là một minh họa nhỏ về sự ngẫu nhiên của miền trên một GridWorld với chuyển đổi * tiếng ồn *. Chúng tôi đào tạo một chính sách trải nghiệm xác suất trượt ngẫu nhiên trong "sim" và đánh giá trên "thực tế" với mức trượt mà nó chưa từng thấy trong quá trình đào tạo. Các hình dạng được vẽ trực tiếp đến chuyển đổi MuJoCo-to-hardware.

> Mã khóa này là một mô hình nhỏ về sự tự động hóa của GridWorld trên các lĩnh vực chuyển động với tiếng ồn. Chúng tôi tập một chiến lược về tỷ lệ chuyển động tự động trong "như thật" và đánh giá "thực tế" trên mức độ chuyển động chưa từng thấy trong đào tạo.

### Bước 1: Sim được tham số

```python
def step(state, action, slip):
    if rng.random() < slip:
        action = random_perpendicular(action)
    ...
```

`slip`trong robot thực sự nó có thể là trục trặc, khối lượng, tăng động lực bất cứ điều gì thay đổi giữa sim và thực.

> `slip`Trong thực tế, trong thực tế, có thể là độ 摩擦, chất lượng, điện tử tăng lợi ích.

### Bước 2: đào tạo với DR

Vào đầu mỗi tập, lấy mẫu `slip ~ Uniform[0.0, 0.4]`- Cụ thể, tập PPO/Q-learning/ bất cứ điều gì.

> Mỗi lần bắt đầu, như vậy.`slip ~ Uniform[0.0, 0.4]` đào tạo PPO/Q-learning/ bất kỳ thuật toán nào

### Bước 3: đánh giá điểm không bắn trên các tờ rơi "thực"

Đánh giá`slip ∈ {0.0, 0.1, 0.2, 0.3, 0.5, 0.7}`. Bốn chương trình đầu tiên được hỗ trợ trong việc đào tạo;`0.5`và `0.7`Một chính sách được đào tạo DR nên ở gần như tối ưu bên trong hỗ trợ và suy giảm đẹp đẽ bên ngoài.

> Trong `slip ∈ {0.0, 0.1, 0.2, 0.3, 0.5, 0.7}`上评估──前四在训练支内;`0.5`和 `0.7`Trong trường ngoài, các chiến lược tập luyện phải giữ được gần nhất trong trường, trong trường ngoài, những chiến lược tập luyện tập luyện tập luyện tập luyện tập luyện tập luyện tập luyện tập luyện tập luyện tập luyện tập luyện tập luyện tập luyện rất yếu.

### Bước 4: so sánh với đào tạo hẹp

Căn nuôi một chính sách thứ hai với `slip = 0.0`Chỉ đánh giá trên cùng một`slip`Bạn sẽ thấy một sự sụt giảm thảm khốc ngay khi trượt thực > 0.

> 用 `slip = 0.0`训练第二策略──在相同滑移范围上评估──当真实滑移 > 0 时应看到灾难性下降──

## Những bẫy

- **Too much randomization.**Đào tàu lên`slip ∈ [0, 0.9]`và chính sách của bạn rất không chấp nhận rủi ro mà nó không bao giờ cố gắng theo con đường tối ưu.
  **过度随机化。**Trong `slip ∈ [0, 0.9]`Ưu tiên, chiến lược vượt quá quy định và không cố gắng theo cách tốt nhất.
- **Too little randomization.**Căn luyện trên một mảnh mỏng và chính sách không thể tổng quát hóa. Sử dụng chương trình giảng dạy thích ứng (Tự động Tự nhiên phân phối miền) mở rộng phân phối khi chính sách cải thiện.
  **过少随机化。**Trong các bài tập trên các bài tập, các chiến lược hoàn toàn không thể phổ biến.
- **Misidentified parameter space.**Định dạng thứ sai (màu sắc của máy ảnh khi khoảng cách thực sự là chậm trễ động lực) và DR không giúp.
  **错误识别参数空间。**随机化错误的东西,DR 无效――先分析真机器人――
- **Privileged info leakage.**Một giáo viên sử dụng tình trạng toàn cầu để hành động, không chỉ quan sát, có thể tạo ra một học sinh không thể bắt kịp.
  **特权信息泄漏。**Các giáo viên sử dụng toàn cảnh làm động tác có thể tạo ra học sinh không thể theo đuổi.
- **Sim-to-sim transfer failure.**Nếu chính sách của bạn không vững chắc với một biến thể sim khó khăn hơn, nó cũng sẽ không vững chắc với thế giới thực.
  **仿真到仿真迁移失败。**Nếu chiến lược đối với những biến thể giả mạo khó hơn không hề tốt, đối với thế giới thực cũng không hề tốt.
- **No real-world safety envelope.**Một chính sách hoạt động trong sim và "sống thực tế" mà không có một tấm khiên an toàn cấp thấp vẫn có thể phá vỡ phần cứng.
  **无真实世界安全包络。**Không có chiến lược bảo vệ an toàn cấp thấp vẫn có thể làm hỏng phần cứng.

## Hãy sử dụng nó để thực hiện

Bộ sưu tập sim-to-real năm 2026:

> 2026 年仿真到真实技术:

| Domain | Stack |
|--------|-------|
| Domain / 领域 | Stack / 技术栈 |
| Legged locomotion (ANYmal, Spot, humanoid) / 腿式运动 | Isaac Lab + DR + privileged teacher / student |
| Manipulation (dexterous hands, pick-and-place) / 操作 | Isaac Lab + DR + DR-GAN for vision |
| Autonomous driving / 自动驾驶 | CARLA / NVIDIA DRIVE Sim + DR + real fine-tune |
| Drone racing / 无人机竞速 | RotorS / Flightmare + DR + online adaptation |
| Finger/in-hand manipulation / 手指/手内操作 | OpenAI Dactyl (DR at unprecedented scale) |
| Industrial arms / 工业机械臂 | MuJoCo-Warp + SI + small real fine-tune |

Để kiểm soát ở mọi quy mô, dòng công việc là nhất quán: phù hợp với bộ sim tốt nhất có thể, ngẫu nhiên những gì bạn không thể phù hợp, đào tạo các chính sách khổng lồ, chưng cất, triển khai với một tấm khiên an toàn.

> Đối với tất cả các quy mô kiểm soát, Workflow phù hợp: càng tốt phù hợp như thật,随机化无法适合部分,训练巨策略,蒸,部署时加安全屏蔽.

## Chuyển nó đi.

Cứ như `outputs/skill-sim2real-planner.md`- Có thể là:

```markdown
---
name: sim2real-planner
description: Plan a sim-to-real transfer pipeline for a given robot + task, covering DR, SI, and safety.
version: 1.0.0
phase: 9
lesson: 11
tags: [rl, sim2real, robotics, domain-randomization]
---

Given a robot platform, a task, and access to real hardware time, output:

1. Reality gap inventory. Suspected sources ranked by expected impact (contact, sensing, actuation delay, vision).
2. DR parameters. Exact list, ranges, distribution. Justify each range against real measurements.
3. SI steps. Which parameters to measure; measurement method.
4. Teacher/student split. What privileged info the teacher uses; what obs the student uses.
5. Safety envelope. Low-level limits, emergency stops, backup controller.

Refuse to deploy without (a) a zero-shot sim-variant test, (b) a safety shield, (c) a rollback plan. Flag any DR range wider than 3× measured real variability as likely over-randomized.
```

## Tập luyện bài tập

1. **Easy.**Trình luyện một đại lý học Q trên GridWorld (slip=0.0).
2. **Medium.**Trình luyện một nhân viên học tập DR Q lấy mẫu `slip ~ Uniform[0, 0.3]`- Đánh giá cùng một loại. DR mua bao nhiêu ở slip=0.5 (không phân phối)?
3. **Hard.**Thực hiện một chương trình giảng dạy: bắt đầu với slip=0.0, mở rộng phạm vi DR mỗi khi chính sách đạt 90% tối ưu. đo lường tổng bước môi trường để đạt slip=0.3 zero shot so với một đường cơ sở DR cố định.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Reality gap | "Sim-to-real difference" / 现实鸿沟 | Distribution shift between training and deployment physics/sensing. |
| Domain randomization (DR) | "Train across random sims" / 域随机化 | Randomize sim parameters during training so policy generalizes. |
| System identification (SI) | "Measure real and fit sim" / 系统辨识 | Estimate real physical parameters; set sim to match. |
| Domain adaptation | "Fine-tune on real data" / 域自适应 | Small real-world fine-tune after sim training; may adapt obs or dynamics. |
| Privileged info | "Ground truth for teacher" / 特权信息 | Information only the sim has; student must infer it from obs history. |
| Teacher/student | "Distill privileged -> observable" / 教师-学生蒸馏 | Teacher trained with shortcuts; student learns to mimic without them. |
| ADR | "Automatic Domain Randomization" / 自动域随机化 | Curriculum that widens DR ranges as the policy improves. |
| Real2Sim | "Close the gap with real data" / 现实到仿真 | Learn a residual to make the sim mimic real rollouts. |

## Xem thêm 延伸阅读

- [Tobin et al. (2017). Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World](https://arxiv.org/abs/1703.06907) giấy DR ban đầu (trầm nhìn cho robot).
- [Peng et al. (2018). Sim-to-Real Transfer of Robotic Control with Dynamics Randomization](https://arxiv.org/abs/1710.06537) DR cho động lực, động cơ bốn lần.
- [OpenAI et al. (2019). Solving Rubik's Cube with a Robot Hand](https://arxiv.org/abs/1910.07113) Dactyl, ADR ở quy mô.
- [Miki et al. (2022). Learning robust perceptive locomotion for quadrupedal robots in the wild](https://www.science.org/doi/10.1126/scirobotics.abk2822) giáo viên- học sinh cho ANYmal.
- [Makoviychuk et al. (2021). Isaac Gym: High Performance GPU Based Physics Simulation for Robot Learning](https://arxiv.org/abs/2108.10470) Sim song song lớn thúc đẩy việc triển khai 20252026
- [Akkaya et al. (2019). Automatic Domain Randomization](https://arxiv.org/abs/1910.07113) Phương pháp chương trình học ADR.
- [Sutton & Barto (2018). Ch. 8 — Planning and Learning with Tabular Methods](http://incompleteideas.net/book/RLbook2020.pdf) khung Dyna ( Sử dụng mô hình để lập kế hoạch + triển khai) hỗ trợ đường ống sim-to-real hiện đại.
- [Zhao, Queralta & Westerlund (2020). Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey](https://arxiv.org/abs/2009.13303) phân loại các phương pháp sim-to-real với kết quả tham chiếu.
