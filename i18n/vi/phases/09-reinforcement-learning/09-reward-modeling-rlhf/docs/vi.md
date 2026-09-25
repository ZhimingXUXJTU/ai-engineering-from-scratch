# Giải thưởng mô hình hóa & RLHF  Giải thưởng xây dựng mô hình với RLHF

> Con người không thể viết một chức năng phần thưởng cho "đáp ứng trợ lý tốt", nhưng họ có thể so sánh hai phản ứng và chọn một tốt hơn. Đáp lại mô hình phần thưởng cho những so sánh đó, sau đó RL mô hình ngôn ngữ chống lại nó. Christiano 2017. InstructGPT 2022.

> **【中文解读】**Người ta không thể viết hàm thưởng cho "hỗ trợ tốt trả lời", nhưng có thể so sánh hai lần trả lời tốt hơn.

> **【拓展：RLHF 是大模型对齐的关键】**RLHF( dựa trên người phản của强化学习) là ChatGPT thành công của cốt lõi技术──三步流程:(1) 监督微调 SFT;(2) 训练奖励模型 RM;(3) 用 PPO 优化 LM──DPO 简化第 2-3步,但本质相同──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment), Phase 9 · 08 (PPO) | **前置知识:** Phase 5 · 05 (情感分析), Phase 9 · 08 (PPO)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Bạn đã đào tạo một mô hình ngôn ngữ về mục tiêu dự đoán mã thông báo tiếp theo. Nó viết tiếng Anh ngữ pháp. Nó cũng nói dối, rambles, và từ chối từ chối. Bạn không thể khắc phục điều này với nhiều hơn trước khi tập  văn bản web là vấn đề, không phải là phương thuốc.

> Bạn đã luyện tập mô hình ngôn ngữ trên mục tiêu dự đoán trong biểu tượng tiếp theo. Nó viết ra ngôn ngữ đúng tiếng Anh. Nhưng nó cũng sẽ nói dối, chạy câu hỏi, từ chối không từ chối. Bạn không thể vượt qua nhiều bài tập dự đoán để sửa chữa.

Bạn muốn một *scalar reward* nói "đáp ứng A tốt hơn phản ứng B cho hướng dẫn X". Việc viết chức năng thưởng bằng tay là không thể. "Helpfulness" không phải là một biểu hiện đóng cửa trên mã thông báo. Nhưng con người có thể so sánh hai đầu ra và đánh dấu một ưu tiên.

> Bạn muốn một * chỉ số thưởng*, cho biết" đối với chỉ dẫn X, trả lời A so với B tốt hơn"...... viết tay hàm thưởng này là không thể. " hữu ích" không phải là biểu tượng kết thúc trên biểu thức.

RLHF (Christiano et al. 2017; Ouyang et al. 2022) chuyển đổi sở thích thành mô hình phần thưởng, sau đó tối ưu hóa LM thông qua PPO so với phần thưởng đó. Trong ba bước: SFT → RM → PPO. Đó là công thức đã vận chuyển ChatGPT, Claude, Gemini và mọi LM khác được sắp xếp vào năm 20232025.

> RLHF sẽ chuyển thành mô hình thưởng, sau đó thông qua PPO đối với LM để tối ưu hóa.

Năm 2026, bước PPO chủ yếu được thay thế bởi DPO (Phase 10 · 08) vì nó rẻ hơn và gần như tốt cho việc điều chỉnh sự sắp xếp. Nhưng phần * mô hình phần thưởng * vẫn là nền tảng của mỗi mẫu Best-of-N, mỗi đường ống dẫn phần thưởng RL-from-verifiable, và mọi mô hình lý luận sử dụng mô hình phần thưởng quy trình.

> Năm 2026 PPO 步骤大多被DPO 替代,因为便宜 hơn và hiệu quả đối với齐几乎相同. Nhưng* mô hình thưởng* vẫn là tốt nhất của N 采样器、可验证奖励 RL 管道和过程奖励模型的基础.

> **【中文解读】**RLHF 三阶段流程:(1) SFT trên dữ liệu biểu hiện của con người giám sát mô hình cơ bản;(2) RM sử dụng sự ưa thích của con người đối với đào tạo Bradley-Terry 奖励模型;(3) PPO sử dụng mô hình 奖励 signal optimization语言模型, đồng thời cộng với KL 惩罚 ngăn chặn sự偏离 SFT 太远.

> **【拓展：DPO 与 RLHF 的对比】**DPO(Direct Preference Optimization) sẽ làm RM+PPO của RLHF 两步合并为一步 trực tiếp từ sự ưu tiên đối với chiến lược đào tạo, không cần thiết cho mô hình thưởng đào tạo rõ ràng.

## Khái niệm cốt lõi

![Three-stage RLHF: SFT, RM training on pairwise prefs, PPO with KL penalty](../assets/rlhf.svg)

**Stage 1: Supervised Fine-Tuning (SFT).**Bắt đầu từ một mô hình cơ bản được đào tạo trước. Định chỉnh về các biểu hiện bằng văn bản của con người về hành vi mục tiêu (những phản ứng theo hướng dẫn, những câu trả lời hữu ích, v.v.). Kết quả: một mô hình `π_SFT`là *đối向 hành vi tốt* nhưng vẫn có không gian hành động không giới hạn.

> **阶段 1：监督微调（SFT）。**Từ mô hình cơ bản dự kiến tập luyện bắt đầu. mô hình hành vi mục tiêu của người viết được mô tả. Kết quả: một mô hình hướng đến hành vi tốt nhưng vẫn có không gian hoạt động không giới hạn.`π_SFT`

**Stage 2: Reward Model training.**

- Thu thập các cặp phản hồi `(y_+, y_-)`để được nhắc nhở `x`, được đánh dấu bởi con người như "y_+ được ưa thích so với y_-. "
- Trình hình thưởng`R_φ(x, y)`để gán điểm cao hơn cho `y_+`- Tôi không biết.
- Lối mất:**Bradley-Terry pairwise logistic**- Có thể là:

  `L(φ) = -E[ log σ(R_φ(x, y_+) - R_φ(x, y_-)) ]`

  BT đã là tiêu chuẩn từ năm 1952 (Bradley-Terry) và là lựa chọn thống trị trong RLHF hiện đại.

- `R_φ`thường được khởi tạo từ mô hình SFT với đầu scalar trên cùng.

> **阶段 2：奖励模型训练。** thu thập những ưu tiên của con người đối với `(y_+, y_-)`, tập luyện phần thưởng mô hình cho `y_+`Hơn nữa, mất mát là Bradley-Terry, và trở lại với logic.`R_φ`Thông thường từ SFT 模型初始化, thêm một mô hình đầu ra.

**Stage 3: PPO against the RM with KL penalty.**

- Tạo ra chính sách có thể đào tạo `π_θ`từ `π_SFT`- Giữ một cái băng lạnh`π_ref = π_SFT`- Tôi không biết.
- Giải thưởng sau khi trả lời `y`- Có thể là:

  `r_total(x, y) = R_φ(x, y) - β · KL(π_θ(·|x) || π_ref(·|x))`

  Lệnh phạt KL ngăn cản `π_θ`từ trôi dạt tùy ý từ `π_SFT` nó là một *regularizer*, không phải một vùng tin tưởng khó. `β`Thông thường `0.01`- Tôi không biết.`0.05`- Tôi không biết.
- Tiếp tục chạy PPO (Dạy 08) với phần thưởng này.

> **阶段 3：对 RM 做 PPO + KL 惩罚。**Từ `π_SFT`Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định hướng: Định định: Định định: Định định: Định định: Định định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Định: Đ

**Why the KL?**Nếu không có nó, PPO sẽ tìm ra chiến lược hack phần thưởng  RM chỉ được đào tạo về hoàn thành trong phân phối.`π_θ`gần các đa dạng nơi mà RM được đào tạo.

> **为什么需要 KL？**Không có nó, PPO sẽ tìm thấy chiến lược của người bị tấn công RM chỉ được đào tạo trên dữ liệu phân tán                                                                                                                                                                                                                                                 `π_θ`保持在 RM 训练的流形附近──这是 RLHF quan trọng nhất旋──

**2026 status:**

- **DPO**(Rafailov 2023): đại số hình thức đóng sụp đổ giai đoạn 2 + 3 thành một lỗ duy nhất được giám sát trên dữ liệu ưu tiên. Không RM, không PPO.
- **GRPO**(DeepSeek 20242025): PPO với cơ sở tương quan nhóm thay vì một nhà phê bình, phần thưởng từ một *verifier* (công trình mã / kết hợp câu trả lời toán học) thay vì một người đào tạo RM. Quyền thống cho các mô hình lý luận. Được bao gồm trong giai đoạn 9 · 12.
- **Process reward models (PRMs):**giải pháp phân tích điểm (mỗi bước lý luận), được sử dụng trong cả RLHF và các biến thể GRPO để lý luận.
- **Constitutional AI / RLAIF:**sử dụng một LLM phù hợp để tạo ra ưu tiên thay vì con người.

> **2026 年状态：**DPO 将阶段 2+3 折叠为单一监督损失──GRPO 用组对基线替代评论,用验证器替代人类训练的 RM──PRM 评分部分解决方案──宪法 AI / RLAIF 用对齐的 LLM 生成偏好──

## Hãy xây dựng nó.
```figure
reward-model
```

## Hãy xây dựng nó

Bài học này sử dụng "phản ứng" và "câu trả lời" tổng hợp nhỏ được đại diện như chuỗi. RM là một điểm số tuyến tính trên một đại diện túi mã thông báo. Không có LLM thực sự  hình dạng * của đường ống quan trọng, không phải quy mô. Xem `code/main.py`- Tôi không biết.

> Bài học này sử dụng các chuỗi chữ nhỏ "提示" và "回复" được tổng hợp.

### Bước 1: dữ liệu ưu tiên tổng hợp

```python
PROMPTS = ["help me", "answer me", "explain this"]
GOOD_WORDS = {"clear", "specific", "kind", "thorough"}
BAD_WORDS = {"vague", "rude", "wrong", "short"}

def make_pair(rng):
    x = rng.choice(PROMPTS)
    y_good = rng.choice(list(GOOD_WORDS)) + " " + rng.choice(list(GOOD_WORDS))
    y_bad = rng.choice(list(BAD_WORDS)) + " " + rng.choice(list(BAD_WORDS))
    return (x, y_good, y_bad)
```

Trong RLHF thực sự, nó được thay thế bởi các nhãn nhân.`(prompt, preferred_response, rejected_response)` giống nhau.

> Thực sự RLHF 中由人类标注者替代──形状`(提示, 偏好回复, 拒绝回复)` hoàn toàn giống nhau.

### Bước 2: Mô hình phần thưởng Bradley-Terry

Điểm số tuyến tính: `R(x, y) = w · bag(y)`- Đào tạo để giảm thiểu lỗ log BT theo cặp:

```python
def rm_train_step(w, x, y_pos, y_neg, lr):
    r_pos = dot(w, bag(y_pos))
    r_neg = dot(w, bag(y_neg))
    p = sigmoid(r_pos - r_neg)
    for tok, cnt in bag(y_pos).items():
        w[tok] += lr * (1 - p) * cnt
    for tok, cnt in bag(y_neg).items():
        w[tok] -= lr * (1 - p) * cnt
```

Sau vài trăm bản cập nhật,`w`Đưa trọng lượng tích cực cho các biểu tượng từ tốt và tiêu cực cho xấu.

> Sau vài trăm lần cập nhật,`w`给好词 token 分配正权重,坏词 分配负权重──

### Bước 3: Chính sách giống như PPO trên RM

Chính sách đồ chơi của chúng tôi tạo ra một token từ một từ vựng.`log π_θ(token | prompt)`, thêm một hình phạt KL-to-reference, và áp dụng các cắt giảm PPO thay thế.

> Chiến lược đồ chơi của chúng tôi tạo ra một token từ một biểu đồ.`log π_θ(token | prompt)`, thêm KL để tham khảo chiến lược trừng phạt, và áp dụng cắt giảm PPO 代理

```python
def rlhf_step(theta, ref, w, prompt, rng, eps=0.2, beta=0.1, lr=0.05):
    logits_theta = policy_logits(theta, prompt)
    probs = softmax(logits_theta)
    token = sample(probs, rng)
    logits_ref = policy_logits(ref, prompt)
    probs_ref = softmax(logits_ref)
    reward = dot(w, bag([token])) - beta * kl(probs, probs_ref)
    # ppo-style update on theta, treating reward as the return
    ...
```

> 关键: phần thưởng = RM 分数 - β × KL(π_θ 1920 π_ref) ――β là kiểm soát chiến lược漂移程度的关键超参数太大策略几乎不变,太小则奖励黑客开始──

### Bước 4: Kiểm tra KL

Đường trung bình đường`KL(π_θ || π_ref)`Nếu nó trượt qua`~5-10`Chính sách đã trôi dạt xa khỏi `π_SFT` thấp hơn `β`Đây là chẩn đoán hàng đầu trong RLHF thực.

> Mỗi lần cập nhật theo dõi trung bình`KL(π_θ || π_ref)`Nếu quá`~5-10`, Chiến lược đã xa `π_SFT`可能 β đang đang giảm hoặc thưởng黑客 đang bắt đầu. Đây là sự khám phá quan trọng nhất trong thực tế RLHF.

### Bước 5: công thức sản xuất với TRL

Khi bạn hiểu được đường ống đồ chơi, đây là vòng lặp giống như người dùng thư viện thực sự viết nó.[TRL](https://huggingface.co/docs/trl)là thực hiện tham chiếu  `RewardTrainer`cho giai đoạn 2 và `PPOTrainer`(với một KL-to-reference tích hợp) cho giai đoạn 3.

> Một khi bạn hiểu được dòng chảy đồ chơi, đây là cách người dùng thực tế viết cùng một vòng lặp.`RewardTrainer`, giai đoạn 3`PPOTrainer`

```python
# Stage 2: reward model from pairwise preferences
from trl import RewardTrainer, RewardConfig
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
rm = AutoModelForSequenceClassification.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct", num_labels=1
)

# dataset rows: {"prompt", "chosen", "rejected"} — Bradley-Terry format
trainer = RewardTrainer(
    model=rm,
    tokenizer=tok,
    train_dataset=preference_data,
    args=RewardConfig(output_dir="./rm", num_train_epochs=1, learning_rate=1e-5),
)
trainer.train()
```

```python
# Stage 3: PPO against the RM with KL penalty to the SFT reference
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead

policy = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")
ref    = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")  # frozen

ppo = PPOTrainer(
    config=PPOConfig(learning_rate=1.41e-5, batch_size=64, init_kl_coef=0.05,
                     target_kl=6.0, adap_kl_ctrl=True),
    model=policy, ref_model=ref, tokenizer=tok,
)

for batch in dataloader:
    responses = ppo.generate(batch["query_ids"], max_new_tokens=128)
    rewards   = rm(torch.cat([batch["query_ids"], responses], dim=-1)).logits[:, 0]
    stats     = ppo.step(batch["query_ids"], responses, rewards)
    # stats includes: mean_kl, clip_frac, value_loss — the three PPO diagnostics
```

Ba điều thư viện làm cho bạn.`adap_kl_ctrl=True`thực hiện lịch trình thích ứng-β: nếu quan sát thấy KL vượt quá `target_kl`, β gấp đôi; nếu dưới một nửa, β phân nửa. Mô hình tham chiếu được đóng băng theo quy ước  bạn không được ngẫu nhiên chia sẻ các tham số với `policy`Và giá trị đầu sống trên cùng xương sống như chính sách (`AutoModelForCausalLMWithValueHead`gắn đầu MLP scalar), đó là lý do tại sao TRL báo cáo `policy/kl`và `value/loss`riêng biệt.

> Tôi có 3 việc làm cho anh.`adap_kl_ctrl=True`实现自适应 β 调度: Nếu KL 超过目标则 β 翻倍, nếu thấp hơn một nửa则 β 减半.

## Những bẫy

- **Over-optimization / reward hacking.**RM là không hoàn hảo.`π_θ`tìm thấy kết quả đối kháng có điểm số cao nhưng xấu. Các triệu chứng: phần thưởng leo lên vô hạn trong khi điểm đánh giá của con người cao cấp hoặc giảm.`β`, mở rộng dữ liệu đào tạo RM.
  **过度优化/奖励黑客。**RM 不完美;`π_θ`找到抗性补全分高但质量差──症状:奖励持续升但人类评估分数停滞或下降──修复:早停、提高 β、扩展 RM 训练数据──
- **Length hacking.**RM được đào tạo về các phản ứng hữu ích thường vô nghĩa thưởng dài. Chính sách học cách đệm các phản ứng. Phong trào khắc phục: phần thưởng bình thường hóa chiều dài, hoặc RLAIF với một RM nhận thức về chiều dài.
  **长度黑客。**Trong bài tập có ích, bạn có thể tìm hiểu về các bài học khác về các bài học khác.
- **Too-small RM.**RM cần phải lớn bằng chính sách. một RM nhỏ không thể ghi điểm chính xác về sản phẩm chính sách.
  **RM 太小。**RM ít nhất phải lớn như chiến lược.
- **KL tuning.**quá thấp β → drift và phần thưởng hack. quá cao β → chính sách hầu như không thay đổi. thủ thuật tiêu chuẩn là một * thích nghi * β nhắm mục tiêu một KL cố định mỗi bước.
  **KL 调优。**β 太低→漂移和奖励黑客──β 太高→ chiến lược gần như không thay đổi──标准技巧是*自适应* β 目标为固定 KL──
- **Preference-data noise.**~ 30% nhãn của con người là tiếng ồn hoặc mơ hồ.
  **偏好数据噪声。**Khoảng 30%  nhãn nhân loại có tiếng ồn hoặc mờ.
- **Off-policy problems.**Dữ liệu PPO là một chút ngoài chính sách sau thời kỳ đầu tiên.
  **离策略问题。**PPO số liệu trong thời đại thứ nhất 后略离策略──像课08 那样监控裁剪比例──

## Hãy sử dụng nó để thực hiện

RLHF vào năm 2026 được xếp lớp:

> RLHF năm 2026 là:

| Layer | Target | Method |
|-------|--------|--------|
| Layer / 层级 | Target / 目标 | Method / 方法 |
| Instruction following, helpfulness, harmlessness / 指令遵循、有用性、无害性 | Alignment / 对齐 | DPO (Phase 10 · 08) preferred over RLHF-PPO. |
| Reasoning correctness (math, code) / 推理正确性（数学、代码） | Capability / 能力 | GRPO with verifier reward (Phase 9 · 12). |
| Long-horizon multi-step tasks / 长视野多步任务 | Agentic / 代理 | PPO / GRPO with process reward models over steps. |
| Safety / refusal behavior / 安全/拒绝行为 | Safety / 安全 | RLHF-PPO with separate safety RM, or Constitutional AI. |
| Best-of-N at inference / 推理时 Best-of-N | Fast alignment / 快速对齐 | Use RM at decode time; no policy training needed. |
| Reward distillation / 奖励蒸馏 | Inference compute / 推理计算 | Train a small "reward head" on top of a frozen LM. |

RLHF là phương pháp * trong năm 2022-2024. Năm 2026, đường ống sắp xếp sản xuất là DPO-thì, chỉ là PPO-cho các bước cao RM hoặc quan trọng về an toàn.

> RLHF trong năm 2022-2024 là phương pháp cốt lõi. Năm 2026, sản xuất cho dòng nước cục bộ với mục đích DPO, PPO chỉ được sử dụng cho các bước quan trọng về an ninh.

## Chuyển nó đi.

Cứ như `outputs/skill-rlhf-architect.md`- Có thể là:

```markdown
---
name: rlhf-architect
description: Design an RLHF / DPO / GRPO alignment pipeline for a language model, including RM, KL, and data strategy.
version: 1.0.0
phase: 9
lesson: 9
tags: [rl, rlhf, alignment, llm]
---

Given a base LM, a target behavior (alignment / reasoning / refusal / agent), and a preference or verifier budget, output:

1. Stage. SFT? RM? DPO? GRPO? With justification.
2. Preference or verifier source. Humans, AI feedback, rule-based, unit-test-pass, or reward distillation.
3. KL strategy. Fixed β, adaptive β, or DPO (implicit KL).
4. Diagnostics. Mean KL, reward stability, over-optimization guard (holdout human eval).
5. Safety gate. Red-team set, refusal rate, safety RM separate from helpfulness RM.

Refuse to ship RLHF-PPO without a KL monitor. Refuse to use an RM smaller than the target policy. Refuse length-only rewards. Flag any pipeline that does not hold back a blind human-eval set as lacking over-optimization protection.
```

## Tập luyện bài tập

1. **Easy.**Đào tạo mô hình giải thưởng Bradley-Terry vào `code/main.py`trên 500 cặp ưu tiên tổng hợp. đo độ chính xác đôi trên 100 cặp được giữ.
2. **Medium.**Động hành vòng đồ chơi PPO-RLHF với `β ∈ {0.0, 0.1, 1.0}`Đối với mỗi người, ghi điểm RM so với KL-to-reference trên các bản cập nhật.
3. **Hard.**Thực hiện DPO (các định giá trị ưu tiên trong dạng đóng) trên cùng một dữ liệu ưu tiên và so sánh với đường ống RLHF-PPO trong tính toán được sử dụng và điểm RM cuối cùng đạt được.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| RLHF | "Alignment RL" | Three-stage SFT + RM + PPO pipeline (Christiano 2017, Ouyang 2022). |
| Reward Model (RM) | "The scoring net" | Learned scalar function fit to pairwise preferences via Bradley-Terry. |
| Bradley-Terry | "Pairwise logistic loss" | `P(y_+ ≻ y_-) = σ(R(y_+) - R(y_-))`; the standard RM objective. |
| KL penalty | "Stay near the reference" | `β · KL(π_θ \|\| π_ref)` in the reward; the anti-reward-hacking regularizer. |
| Reward hacking | "Goodhart's law" | Policy exploits RM flaws; symptoms: reward up, human eval flat. |
| RLAIF | "AI-labeled preferences" | RLHF where labels come from another LM instead of humans. |
| PRM | "Process Reward Model" | Scores partial reasoning steps; used in reasoning pipelines. |
| Constitutional AI | "Anthropic's method" | AI-generated preferences guided by explicit rules. |

## Xem thêm 延伸阅读

- [Christiano et al. (2017). Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741) tờ báo bắt đầu RLHF.
- [Ouyang et al. (2022). InstructGPT — Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) công thức đằng sau ChatGPT.
- [Stiennon et al. (2020). Learning to summarize with human feedback](https://arxiv.org/abs/2009.01325) RLHF trước đây để tóm tắt.
- [Rafailov et al. (2023). Direct Preference Optimization](https://arxiv.org/abs/2305.18290) DPO; sự cố sau RLHF vào năm 2026.
- [Bai et al. (2022). Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) RLAIF và tự phê bình vòng lặp.
- [Anthropic RLHF paper (Bai et al. 2022). Training a Helpful and Harmless Assistant](https://arxiv.org/abs/2204.05862) tờ HH.
- [Hugging Face TRL library](https://huggingface.co/docs/trl) sản xuất `RewardTrainer`và `PPOTrainer`Đọc nguồn huấn luyện viên cho thông tin về KL thích ứng và giá trị đầu.
- [Hugging Face — Illustrating Reinforcement Learning from Human Feedback](https://huggingface.co/blog/rlhf)bởi Lambert, Castricato, von Werra, Havrilla  bước đi thông qua của đường ống ba giai đoạn với sơ đồ.
- [von Werra et al. (2020). TRL: Transformer Reinforcement Learning](https://github.com/huggingface/trl) thư viện; `examples/`có các kịch bản RLHF cuối đến cuối cho Llama, Mistral và Qwen.
- [Sutton & Barto (2018). Ch. 17.4 — Designing Reward Signals](http://incompleteideas.net/book/RLbook2020.pdf) quan điểm giả thuyết phần thưởng; điều kiện tiên quyết thiết yếu để suy nghĩ về việc hack phần thưởng.
