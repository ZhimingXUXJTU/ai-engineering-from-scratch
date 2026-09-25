# Chỉ thị theo dõi như tín hiệu sắp xếp

> Mỗi lời chỉ trích sau đó của RLHF tranh luận chống lại đường ống này. Trước khi bạn nghiên cứu cách áp lực tối ưu hóa làm sao biến dạng một proxy, bạn phải xem proxy. InstructGPT (Ouyang et al., 2022) đã xác định kiến trúc tham chiếu: điều chỉnh tinh tế được giám sát trên các cặp hướng dẫn-đáp ứng, mô hình phần thưởng được đào tạo trên bảng xếp hạng ưu tiên theo cặp, và PPO đối với mô hình phần thưởng với một hình phạt KL đối với chính sách SFT. Một 1.3B InstructGPT được ưa thích so với một 175B GPT-3. Kết quả duy nhất đó là lý do tại sao mỗi phòng thí nghiệm biên giới vào năm 2026 vẫn gửi một đường ống thuần đào tạo hình dạng RLHF.

> **【中文解读】**InstructGPT(Ouyang 等人, 2022) đã xác định cấu trúc tham khảo đối với tất cả: 1) giám sát điều chỉnh nhỏ của SFT) trong đào tạo trên lệnh đáp ứng; 2) mô hình thưởng được thực hiện trên đào tạo về sắp xếp ưu tiên; 3) mô hình thưởng đối với PPO, với KL  trừng phạt bảo vệ;. 1.3B của InstructGPT trên đánh giá ưu tiên của con người vượt quá 175B của GPT-3;; đó là lý do tại sao mỗi phòng thí nghiệm phía trước năm 2026 vẫn đang sử dụng các đường ống đào tạo sau dưới dạng RLHF;.

> **【拓展：RLHF → 现代 AI 对齐】**RLHF (RHF) là một trong những kỹ thuật quan trọng của ChatGPT thành công.

>  **【前置】**学本节前请先掌握:Phase 10·06(SFT 监督微调)、Phase 10·07(RLHF)、Phase 10·08(DPO) 理解三阶段对齐管线的技术细节──本节是Phase 18 的开篇,从工程视角审视对齐后续 29节都基于此基础──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy three-stage pipeline) | **语言:** Python（标准库，玩具三阶段管线）
**Prerequisites:** Phase 10 · 06 (SFT), Phase 10 · 07 (RLHF), Phase 10 · 08 (DPO) | **前置知识:** Phase 10 · 06 (SFT), Phase 10 · 07 (RLHF), Phase 10 · 08 (DPO)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Mục tiêu học tập

- Hãy nêu tên ba giai đoạn của đường ống dẫn InstructGPT và lỗ được sử dụng trong mỗi giai đoạn.
  Trung文翻译:说出 InstructGPT 管线的三个阶段及每个阶段使用的损失函数──
- Giải thích lý do tại sao mô hình điều chỉnh theo hướng dẫn 1.3B vượt qua GPT-3 thô 175B khi đánh giá sở thích của con người.
  Trung ngữ翻译:解释为什么 1.3B 指令微调模型在人类偏好评估上击败原始 175B GPT-3──
- Cần phải giải thích điều gì về hình phạt KL ở giai đoạn 3 và tại sao việc loại bỏ nó lại rơi vào hành vi tìm kiếm chế độ.
  Trung ngữ翻译:说明第三阶段 KL 惩罚保护的是什么,以及移除它为什么会导致模式塌行为──
- Mô tả thuế sắp xếp và giảm thiểu PPO-ptx Ouyang et al. được sử dụng chống lại nó.
  Trung ngữ翻译:描述对齐税以及 Ouyang 等人使用的PPO-ptx 缓解方法──

## Vấn đề  vấn đề giới thiệu

Các mô hình ngôn ngữ được đào tạo trước hoàn thành văn bản. Chúng không trả lời câu hỏi. Hãy hỏi GPT-3 "tập một hàm Python đảo ngược một danh sách" và bạn thường nhận được một lời nhắc lại khác, bởi vì hầu hết các phân phối đào tạo là văn bản web tiếp tục với nhiều văn bản web hơn. Mô hình đang làm công việc của nó  công việc sai.

> 预训语言模型补充全文, thay vì trả lời câu hỏi. Hãy để GPT-3 "tập một hàm Python  ngược chuyển trong danh sách", bạn thường sẽ nhận được một lời khuyên khác, bởi vì hầu hết các phân phối được đào tạo là tiếp tục tạo thêm nội dung trên các trang web.

Các nhà nghiên cứu chuyên nghiệp sử dụng để sửa chữa điều này là sự thích của con người. Hai hoàn thành đi đến một rater; rater chọn tốt hơn; một mô hình phần thưởng học được rater. Sau đó một vòng lặp RL chuyển chính sách hướng đến các kết quả mô hình phần thưởng điểm cao. Đó là luận án InstructGPT đầy đủ trong ba câu. phần còn lại của bài báo là kỹ thuật.

> Mỗi phòng thí nghiệm nghiêm ngặt được sử dụng để sửa chữa vấn đề này là đại diện cho sự thích của con người. Hai phần bổ sung cho các nhà đánh giá; các nhà đánh giá chọn tốt hơn; các nhà đánh giá học hỏi mô hình thưởng. Sau đó, vòng RL sẽ chuyển chiến lược sang các mô hình thưởng cao điểm xuất phát.

## Khái niệm cốt lõi

### Giai đoạn 1: điều chỉnh tinh tế được giám sát (SFT)

Thu thập các cặp phản ứng nhanh chóng nơi phản ứng là những gì một con người có ý định tốt sẽ viết. Ouyang et al. sử dụng 13k yêu cầu từ các nhãn và OpenAI API. Định chỉnh mô hình cơ sở trên dữ liệu này với mất lượng entropy chéo tiêu chuẩn.

> 收集提示-响应, trong đó响应 là một phần nội dung của một người đăng ký có ý chí tốt. Ouyang 等人 đã sử dụng từ 13k提示 từ người đăng ký và OpenAI API.

SFT cho bạn: mô hình bây giờ trả lời các câu hỏi thay vì tiếp tục chúng.

> SFT không cho bạn: khi nhiều câu trả lời đều hợp lý, người đánh giá thích hơn bất kỳ tín hiệu nào của câu trả lời nào.

> **【中文解读】**SFT 阶段使模型从"补全文本"转向"回答问题", nhưng không thể cung cấp về về nhiều câu trả lời hợp lý trong số đó là nào tốt hơn. RM 阶段 sử dụng Bradley-Terry 成对偏好损失 L_RM = -log sigmoid(r(x,y_w) - r(x,y_l)) Trong xếp hạng của các nhà chỉ định, RM thường bắt đầu và thay thế LM 标题, 6B là đủ để hướng dẫn 175B 模型。

### Giai đoạn 2: Mô hình phần thưởng (RM)

Đối với mỗi prompt, lấy mẫu hoàn thành K từ mô hình SFT. Một labeler xếp hạng chúng. Tập một mô hình phần thưởng ghi điểm bất kỳ cặp phản ứng prompt nào để, cho các cặp nơi `y_w`được `y_l`- Có thể là:

> Đối với mỗi gợi ý, từ SFT 模型采样 K 个补全――标注者对它们排序――训练一个奖励模型对任何提示-响应对打分,使对于`y_w`优于 `y_l`                                                                                                                                                                                                                                                              

```
L_RM = -log sigmoid(r(x, y_w) - r(x, y_l))
```

Đây là sự mất ưu tiên cặp Bradley-Terry. RM thường được khởi tạo từ mô hình SFT với đầu LM được thay thế bởi đầu scalar.

> Đó là Bradley-Terry 成 đối với sự mất tích ưu điểm. RM thường bắt đầu từ SFT 模型初始化, ngôn ngữ模型头换为标量头.

Các mô hình phần thưởng nhỏ: 6B là đủ cho 175B InstructGPT. Chúng cũng rất yếu  Phần 5 của bài báo chủ yếu là về hành vi tấn công phần thưởng xuất hiện ở quy mô nhỏ.

> 奖励模型很小:6B 就足以指导 175B's InstructGPT──但它们也很脆弱论文第5节主要讨论了小规模出现的奖励黑客行为──

> **【拓展：PPO 阶段 → RLHF 的核心工程】**Hàm mục tiêu của PPO 阶段 J(pi) = E[r(x,y) ] - beta * KL(pi khi được pi_SFT) tối đa hóa phần thưởng đồng thời giữ chiến lược gần SFT。KL 系数 beta là quan trọng nhất RLHF 超参数太低 dẫn đến phần thưởng黑客,太高则 SFT 上无改进。 không có KL 项,优化器 tìm thấy là RM từ chưa thấy đối kháng mẫu分数高 không phải vì sự ưa thích thực sự của con người, mà vì RM từ chưa đánh giá những đầu vào này。

### Giai đoạn 3: PPO với hình phạt KL

Định nghĩa mục tiêu:

```
J(pi) = E_{x~D, y~pi(.|x)} [ r(x, y) ] - beta * KL(pi(.|x) || pi_SFT(.|x))
```

Tăng tối đa bằng PPO.`pi`Nếu không có nó, người tối ưu hóa tìm thấy các ví dụ đối nghịch  chuỗi ghi điểm cao dưới RM vì RM chưa bao giờ thấy chúng, không phải vì con người thực sự thích chúng.

> Sử dụng PPO tối đa hóa.`pi`Không có nó, các máy tối ưu hóa sẽ tìm thấy các chuỗi đối kháng mẫu trong RM dưới điểm cao, bởi vì RM chưa từng thấy chúng, chứ không phải là sự thích hợp thực sự của con người.

Tỷ lệ KL `beta`là siêu tham số RLHF quan trọng nhất. quá thấp: reward hacking. quá cao: không có cải thiện so với SFT.

> KL là số`beta`là quan trọng nhất RLHF 超参数──太低:奖励黑客──太高:相比SFT 没有改进──

> **【中文解读】**Đối với thuế: RLHF 后模型在人类偏好上更好但在标准基准(SQuAD, HellaSwag, DROP) 上退步。Ouyang 等人称之为" đối với thuế"并使用PPO-ptx 修复将预训梯度混入RL 目标,使模型不忘从未获奖的下游任务──PPO-ptx 成为标准Anthropic、DeepMind和Meta 都使用某种变体──

### Thuế sắp xếp

Sau RLHF, mô hình được người thích nhưng giảm xuống trên các tiêu chuẩn chuẩn chuẩn (SQuAD, HellaSwag, DROP). Ouyang et al. gọi đây là thuế sắp xếp và sửa bằng PPO-ptx: trộn gradient trước đào tạo vào mục tiêu RL để mô hình không quên làm thế nào để thực hiện các nhiệm vụ dòng chảy sau đó nó không bao giờ được khen thưởng.

> Sau RLHF, mô hình trên sở thích của con người tốt hơn nhưng trên tiêu chuẩn基准 ((SquAD, HellaSwag, DROP) trên退步。Ouyang 等人 gọi nó là "对齐税" và sử dụng PPO-ptx 修复将预训梯度混入RL 目标,使 mô hình không quên chưa bao giờ được thưởng dưới游任务。

```
J_ptx(pi) = J(pi) + gamma * E_{x~D_pretrain} [ log pi(x) ]
```

PPO-ptx trở thành tiêu chuẩn. Anthropic, DeepMind và Meta đều sử dụng một số biến thể.

> PPO-ptx  trở thành tiêu chuẩn.

> **【拓展：1.3B vs 175B → 对齐独立于能力】**1.3B InstructGPT trên sự lựa chọn của người tham khảo khoảng 70% thời gian vượt qua 175B GPT-3── khoảng cách trong dòng sản xuất ẩn trên các gợi ý thử nghiệm lớn hơn.

### Kết quả

Một 1.3B InstructGPT (SFT + RM + PPO-ptx) được các nhà nhãn thích hơn là 175B cơ sở GPT-3 khoảng 70% thời gian.

> 1.3B của hướng dẫnGPT(SFT + RM + PPO-ptx) trong khoảng 70% thời gian được đánh dấu ưu tiên tốt hơn 175B cơ sở GPT-3── khoảng cách trong các xu hướng sản xuất ẩn trên các chỉ số thử nghiệm lớn hơn. Từ số này có thể đọc hai điều:

1. Lòng xếp là một trục khác với khả năng. mô hình 175B có khả năng nhiều hơn; mô hình 1.3B có sự sắp xếp nhiều hơn; những người dán nhãn thích một loại sắp xếp.
   Trung ngữ翻译:对齐是与能力不同轴──175B 模型有更多能力;1.3B 模型有更多对齐;标注者偏好对齐的那个──
2. Mức độ khả năng được thiết lập bởi mô hình cơ bản. Bạn không thể RLHF mô hình cơ bản để biết các sự kiện nó chưa từng thấy.
   Trung ngữ翻译:能力下限由基础模型设定──你不能通过RLHF 让基础模型知道它从未见过的事实──

> **【拓展：Phase 18 后续课程 → 每个都在攻击此管线】**Mỗi bài phê bình của chương trình tiếp theo đều trong một phần của tấn công này: phần thưởng黑客 (đọc 2) giai đoạn tấn công 2,DPO (đọc 3) hợp并阶段 2 和 3,CAI (đọc 5) thay thế người đánh dấu, bài học 4) hiển thị người đánh dấu là có thiên vị, đối diện với giả mạo (đọc 9) chiến lược hiển thị có thể hoàn toàn vượt qua giai đoạn 3 (đọc 3) Nếu không có trong đầu của bạn một cái ống này, bạn sẽ không thể hiểu được những lời phê bình này.

### Tại sao đây là điểm tham chiếu cho giai đoạn 18

Mỗi lời chỉ trích trong các bài học sau đó  tấn công phần thưởng (Lớp 2), DPO (Lớp 3), ly (Lớp 4), CAI (Lớp 5), các đại lý ngủ (Lớp 7), giả mạo sự sắp xếp (Lớp 9)  tranh luận chống lại một phần của đường ống này. Chiến dịch tấn công phần thưởng giai đoạn 2. DPO bị sụp đổ giai đoạn 2 và 3. CAI thay thế máy dán nhãn của con người. Sycophancy cho thấy nhãn là một tín hiệu thiên vị. Sự giả mạo liên kết cho thấy chính sách có thể đi vòng quanh giai đoạn 3 hoàn toàn. Bạn không thể theo dõi bất kỳ lời chỉ trích nào mà không cần đầu tiên đưa vào đầu bạn.

> Mỗi bài học trong chương trình tiếp theo  khen thưởng黑客(Lớp 2)、DPO(Lớp 3)、(Lớp 4)、CAI(Lớp 5)、潜伏 Agent(Lớp 7)、对齐伪装(Lớp 9)都在攻击此管线的某部分── khen thưởng黑客攻击第二阶段──DPO 合并第二和第三阶段──CAI 替代人类标记者──展示标记者是有偏见信号──对齐伪装展示策略可以完全绕过第三阶段──如果没有先在脑中这个管线,就无法理解这些批评──

## Hãy sử dụng nó để thực hiện
```figure
al-instruct-pipeline
```

## Sử dụng nó

`code/main.py`mô phỏng ba giai đoạn trên dữ liệu sở thích đồ chơi. Chính sách cơ bản là một đồng xu thiên vị về các hành động {A, B, C}. Giai đoạn 1 SFT bắt chước các hành động của label trên 200 lời nhắc. Giai đoạn 2 phù hợp với mô hình giải thưởng Bradley-Terry từ 500 bảng xếp hạng cặp. Giai đoạn 3 thực hiện một bản cập nhật đơn giản về PPO với một hình phạt KL đối với chính sách SFT. Bạn có thể xem sự tăng trưởng của phần thưởng, sự khác biệt KL tăng lên, và sự trôi dạt chính sách và bạn có thể tắt thời gian KL để thấy sự tấn công phần thưởng xuất hiện trong vòng 50 bước cập nhật.

> `code/main.py`Trong dữ liệu sở thích đồ chơi mô phỏng ba giai đoạn. Cơ sở "cách" là động tác {A, B, C} trên có tiền tệ có sự偏偏. giai đoạn 1 SFT 模拟标注者 trên 200 提示 trên động tác. giai đoạn 2 từ 500 thành phần trong xếp hạng phù hợp với Bradley-Terry 奖励模型. giai đoạn 3 运行带有 KL 惩罚的简化 PPO 更新.

Những gì cần xem:

观察要点:

- Đường quỹ đạo thưởng với `beta = 0.1`vs `beta = 0.0`- Tôi không biết.
  Trung ngữ翻译:`beta = 0.1`vs `beta = 0.0`时的奖励轨迹──
- (các bước đào tạo)
  Trung文翻译:训练步骤中 KL(pi                                                                                                                                                                                                                                                         
- Phân phối hành động cuối cùng so với ưu tiên nhãn.
  Trung ngữ翻译:最终动作分布与标注者的偏好比较──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-instructgpt-explainer.md`. Với mô tả đường ống RLHF hoặc bản tóm tắt trên giấy, nó xác định được hai giai đoạn nào đang được sửa đổi, mất mát nào đang được sử dụng ở mỗi giai đoạn, và liệu có một hình phạt KL hoặc một chất điều chỉnh tương đương có mặt hay không.

> 本课产 出 `outputs/skill-instructgpt-explainer.md` Đưa ra mô tả hoặc bản tóm tắt của RLHF, nó xác định được điều chỉnh trong ba giai đoạn, từng giai đoạn sử dụng hàm mất mát nào, cũng như liệu có KL 惩罚 hoặc hiệu quả bình thường hóa không.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đặt`beta = 0.0`và báo cáo phân phối hành động sau 200 bước PPO. Giải thích hành vi tìm kiếm chế độ trong một đoạn.
   Trung ngữ翻译:运行 `code/main.py`❖ thiết lập`beta = 0.0`Và báo cáo 200 bước PPO 后的动作分布――用一段话解释模式塌行为――

2. Thay đổi mô hình phần thưởng để có một thiên vị +0,5 cho hành động B (một lỗi phần thưởng mô phỏng).`beta = 0.1`- Hình phạt KL có ngăn cản chính sách khai thác sự thiên vị không?`beta`việc khai thác trở nên rõ ràng?
   Trung文翻译:修改奖励模型使动作 B 有 +0.5 偏置(模拟奖励 bug) 』用 `beta = 0.1`运行 PPO──KL 惩罚能否阻止策略利用偏置? 在什么`beta`Giá trị sử dụng trở nên hiển thị?

3. Đọc Ouyang et al. (arXiv:2203.02155) Hình 1. Tạo lại đường cong ưu tiên nhãn bằng cách chạy PPO trong 1, 5, 20, 100 bước và đo ưu tiên so với mô hình SFT.
   Trung文翻译:阅读 Ouyang 等人(arXiv:2203.02155)图 1──通过运行 PPO 1、5、20、100 步并测量对SFT 模型的偏好来复现标注者偏好曲线──

4. Phần 4.3 của báo cáo báo cáo một 1.3B InstructGPT vượt qua 175B GPT-3 khoảng 70% thời gian. Tại sao tỷ lệ này sẽ cao hơn trên các yêu cầu sản xuất ẩn hơn trên các yêu cầu của nhà dán nhãn?
   Bài luận Phần 4.3 báo cáo 1.3B InstructGPT trong khoảng 70% thời gian đánh bại 175B GPT-3── Tại sao tỷ lệ này trên các gợi ý sản xuất ẩn trên cao hơn các gợi ý của người tham gia?

5. Thay thế lỗ PPO bằng DPO (Phase 10 · 08) trên cùng dữ liệu ưu tiên. So sánh chi nhánh chính sách cuối cùng (KL đến SFT) và phần thưởng cuối cùng. Phương pháp nào chi nhánh hơn với phần thưởng phù hợp?
   Trung ngữ翻译: 在相同偏好数据上使用DPO(Phase 10 · 08) thay thế PPO 损失──比较最终策略漂移(KL到SFT) 和最终奖励── 在匹配奖励下哪种方法漂移更大?

## Từ khóa  Keyword

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| SFT | "instruction tuning" / "指令微调" | Stage 1: cross-entropy fine-tune on prompt-response pairs / 阶段 1：在提示-响应对上交叉熵微调 |
| Reward model | "the RM" / "奖励模型" | Scalar regressor over (prompt, response) trained with Bradley-Terry on pairwise labels / 用 Bradley-Terry 在成对标签上训练的标量回归器 |
| Bradley-Terry | "pairwise preference loss" / "成对偏好损失" | -log sigmoid(r_w - r_l); reduces pairwise ranking to binary classification / 将成对排序简化为二分类 |
| KL penalty | "the regularizer" / "正则化器" | `beta * KL(pi \|\| pi_SFT)` — keeps the RL policy near the SFT anchor / 保持 RL 策略接近 SFT 锚点 |
| PPO-ptx | "PPO with pretraining mix" / "带预训练混合的 PPO" | Adds a fraction of pre-training log-likelihood to the PPO objective to offset the alignment tax / 将部分预训练对数似然加入 PPO 目标以抵消对齐税 |
| Alignment tax | "the RLHF regression" / "RLHF 退步" | Post-RLHF drop on standard benchmarks that RLHF did not target / RLHF 后在未针对的标准基准上的性能下降 |
| Labeler preference | "the ground truth" / "地面真实" | Sample of human rankings; the RM is a statistical proxy for this, not for "human values" / 人类排序的样本；RM 是其统计代理，而非"人类价值观" |

## Xem thêm 延伸阅读

- [Ouyang et al. — Training language models to follow instructions with human feedback (arXiv:2203.02155)](https://arxiv.org/abs/2203.02155) giấy InstructGPT, nền tảng cho mỗi đường ống RLHF sau đó
  Trung ngữ翻译:Ouyang 等人InstructGPT 论文,此后每个RLHF 管线的基础
- [Stiennon et al. — Learning to summarize from human feedback (arXiv:2009.01325)](https://arxiv.org/abs/2009.01325) RLHF-for-summary tiền nhiệm
  Trung ngữ翻译:Stiennon 等人RLHF 用于摘要的前身
- [Christiano et al. — Deep reinforcement learning from human preferences (arXiv:1706.03741)](https://arxiv.org/abs/1706.03741) công thức RL dựa trên ưu tiên ban đầu
  Trung文翻译:Christiano 等人 dựa trên RL 偏好的 的原始公式
- [Bai et al. — Training a Helpful and Harmless Assistant with RLHF (arXiv:2204.05862)](https://arxiv.org/abs/2204.05862) Việc mở rộng HH của đường ống dẫn đường InstructGPT của Anthropic
  Trung文翻译:Bai 等人Anthropic đối với InstructGPT 管线的 HH 扩展
