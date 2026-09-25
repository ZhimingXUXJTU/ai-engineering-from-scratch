# Hội tâm trí và tranh luận đa đại lý .

> Thuyết năm 1986 của Minsky  trí thông minh là một xã hội của các chuyên gia  được khám phá lại mỗi thập kỷ. Năm 2023, Du et al. đã biến nó thành một thuật toán cụ thể: nhiều trường hợp LLM đề xuất câu trả lời, đọc câu trả lời của nhau, chỉ trích và cập nhật. Trong suốt N vòng họ tụ tụ tập về một sự đồng thuận vượt qua CoT không bắn và suy nghĩ về sáu nhiệm vụ lý luận và thực tế. Hai phát hiện quan trọng: cả hai **multiple agents**và **multiple rounds**xã hội đánh bại một đơn độc lập; trao đổi đa vòng đánh bại một lần bỏ phiếu.

> **【中文解读】**Bài viết này giới thiệu luận án xã hội tâm trí của Marvin Minsky về ứng dụng của lý thuyết xã hội tâm trí trong nhiều đại lý  hệ thống.

> **【拓展：society of mind debate→具体应用】**Marvin Minsky's心智社会 (được đề xuất năm 1986) đề xuất rằng trí thông minh là sản phẩm hợp tác của nhiều tâm trí đơn giản.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 16·04(原语模型)、Phase 13·01-03(CoT 推理)。Minsky 心智社会理论 + LLM 辩论算法。
>  **【类比】**多 Agent 辩论 = "学术同行评审"――单 Agent = 一个作者写论文(容易自但片面);多 Agent 辩论 = 多位审稿人 + 作者多轮回应,最终共识更稳健。Du et al. 2023 证明:多 Agent + 多轮独立贡献提升不是简单加法,是协同效应──3-5 个 Agent 最优(多多了反而成一团)。

##                                                                                                                                                                                                                                                               

Sự nhất quán tự nhiên  lấy nhiều lần một mẫu và lấy câu trả lời đa số  là cải tiến lý luận rẻ nhất bạn có thể bắt đầu. Nó hoạt động, nhưng nó bão hòa nhanh chóng. Bạn có thể tăng gấp đôi các mẫu của mình và không thấy một bước nhảy có ý nghĩa khác.

> Bản thân sự phù hợp với một mô hình nhiều lần lấy mẫu và nhận được đa số các câu trả lời là cải tiến lý thuyết rẻ nhất bạn có thể thêm vào. Nó hiệu quả, nhưng rất nhanh. Bạn có thể tăng gấp đôi lượng mẫu nhưng không có ý nghĩa tăng lên.

Sự bão hòa xuất phát từ các lỗi tương quan: mô hình tương tự có xu hướng thất bại theo cùng một cách. Việc lấy mẫu nhiều hơn không giúp ích nếu mỗi mẫu chia sẻ điểm mù tương tự. Vấn đề phá vỡ mối tương quan bằng cách buộc các nhân viên phải đối mặt với sự bất đồng.

> 和来自相关错误: cùng mô hình có xu hướng thất bại theo cùng một cách.

Cuộc tranh luận phá vỡ sự bão hòa. Thay vì các mẫu độc lập N từ một mô hình, các đại lý N đọc luận và sửa đổi của nhau.

> 辩论打破和── không phải lấy N个独立样本 từ một mô hình, mà là để N个代理阅读 lẫn nhau suy luận và sửa đổi── liên quan giữa các mô hình giảm đi (không còn độc lập và phân phối), điểm nhận thường là đúng, trong khi độc lập và phân phối bỏ phiếu thường tự tin phạm sai lầm──

Quan hệ kết hợp là cơ chế. Khi các đại lý thấy lý luận của các đại lý khác, họ không thể không tham gia với nó  hoặc để bảo vệ vị trí của họ hoặc cập nhật nó.

> Khi đại lý nhìn thấy những lời khuyên của đại lý khác, họ phải tham gia hoặc bảo vệ lập trường của mình, hoặc cập nhật nó.

## Khái niệm cốt lõi

### Du et al. 2023 thuật toán

Từ arXiv:2305.14325 (ICML 2024):

> Từ arXiv:2305.14325 (ICML 2024):

Các thuật toán là cố ý đơn giản: không có vai trò đặc biệt, không có thẩm phán, không có người điều hành. Mỗi đại lý là đối xứng. Asymmetry duy nhất là thứ tự của ai nói đầu tiên, và thậm chí đó rửa ra qua nhiều vòng.

> 算法 có ý nghĩa đơn giản: không có vai trò đặc biệt, không có thẩm phán, không có chủ tịch. Mỗi đại lý là đối称.

1. Mỗi nhân viên N tạo ra câu trả lời ban đầu cho câu hỏi.
   Trung ngữ翻译:N 个代理 个别产生问题初始答案──
2. Đối với vòng r = 2..R: mỗi đại lý được hiển thị các câu trả lời vòng r-1 của các đại lý khác và được hỏi "Tuy nhiên, hãy đưa ra câu trả lời cập nhật của bạn".
   Đối với thứ hai.R: Mỗi đại lý nhìn thấy các đại lý khác.
3. Sau vòng R, đa số bỏ phiếu cho câu trả lời cuối cùng.
   Trung ngữ翻译:R 轮后, bỏ phiếu đa số cho câu trả lời cuối cùng.

Các bài kiểm tra trên giấy về MMLU, GSM8K, tiểu sử, MATH, và các điểm chuẩn thực tế.

> 论文在MMLU、GSM8K、传记、MATH 和事实性基准上测试──辩论持续优于CoT 和自我反思──

Bộ điểm chuẩn bao gồm cả lý luận (MATH, GSM8K  các vấn đề có câu trả lời chính xác có thể xác minh) và thực tế (tác phẩm tiểu sử  tuyên bố có thể kiểm tra với Wikipedia).

> 基准套件涵盖推理(MATH、GSM8K有可验证正确答案问题) 和事实性(传记可对照维基百科 检查的声明) ⋅ Sự gia tăng thực tế là kết quả tiêu đề:辩论是减少事实性问题幻觉的已知最便宜方法──

### Hai nút độc lập

Các bài viết từ cùng một giấy tờ:

> Đồng một bài báo của tiêu hủy kinh nghiệm:

- **Agent count alone**(1 vòng, đa số phiếu N) đánh bại đơn vị trong hầu hết các nhiệm vụ, nhưng cao nguyên.
  Trung ngữ翻译:**仅 Agent 数量**(1 vòng,N đa số bỏ phiếu) Trong hầu hết các nhiệm vụ tốt hơn một đại lý, nhưng sẽ đạt được nền tảng.
- **Round count alone**(1 nhân viên nhìn thấy lý luận trước đó của riêng mình) hầu như không giúp  yếu kém của phản xạ được biết đến.
  Trung ngữ翻译:**仅轮数**(1 个代理 见自己先前推理) hầu như không giúp gì  Đó là điểm yếu của phản ứng.
- **Both together**Sự trao đổi nhiều vòng giữa nhiều đại lý thúc đẩy lợi nhuận.
  Trung ngữ翻译:**两者结合**产生大幅提升.

### Tại sao nó hoạt động

Hai cơ chế:

> Hai cơ chế:

Hai cơ chế này hợp nhất: sự tiếp xúc với sự bất đồng cung cấp thông tin mới; sai lầm không liên quan ngăn chặn thông tin mới được trung bình vào câu trả lời sai.

> 两个机制复合:暴露于分歧提供新信息;去相关错误防止新信息被平均到错误答案中――单独任一比两者结合弱――

1. **Exposure to disagreement.**Khi một đại lý thấy chuỗi lý luận của đại lý khác với một kết luận khác, nó phải biện minh hoặc cập nhật.
   Trung ngữ翻译:**暴露于分歧。**Khi một đại lý nhìn thấy một đại lý khác với kết luận khác nhau, nó phải chứng minh hoặc cập nhật.
2. **Correlated error reduction.**Trong tính nhất quán, tất cả các mẫu đều đến từ cùng một mô hình, vì vậy các lỗi tương quan với một câu trả lời sai lầm. Các mô hình khác nhau hoặc hạt giống khác nhau không liên quan. Các quan điểm tranh luận khác nhau không liên quan.
   Trung ngữ翻译:**相关错误减少。**Trong sự đồng nhất của bản thân, tất cả các mẫu đều xuất phát từ cùng một mô hình, vì vậy sai lầm liên quan  bạn trung bình nhận được một câu trả lời sai lầm tự tin                                                                                                                                                                                                                                          

### Cuộc tranh luận đa dạng

A-HMAD và các tiếp theo liên quan sử dụng * các mô hình cơ sở khác nhau* cho các tác nhân khác nhau. Llama + Claude + GPT tranh luận làm giảm sự sụp đổ của monoculture (Dạy 26) bởi vì các lỗi tương quan của một gia đình mô hình không được chia sẻ bởi những người khác.

> A-HMAD 和相关后续工作为不同 Agent 使用*不同的基础模型*──Llama + Claude + GPT 辩论减少单一文化崩(Lớp 26), vì một模型族的相关错误不被其他模型族共享──

Nguyên lý sai lầm-sự kết hợp là cùng một phía sau các phương pháp tập hợp trong ML cổ điển: các mô hình khác nhau thất bại khác nhau, vì vậy bỏ phiếu đáng tin cậy hơn.

> 错误去相关论点与经典 ML 集成方法背后的相同: đa dạng hóa mô hình thất bại theo cách khác nhau, do đó bỏ phiếu đáng tin cậy hơn.

Nhược điểm: mô hình yếu tham gia vào một cuộc tranh luận có thể kéo sự đồng thuận về phía câu trả lời sai (xem "Chúng ta nên trở nên điên rồ?", arXiv:2311.17371).

> 缺点: Một mô hình yếu của cuộc tranh luận tham gia có thể sẽ đồng ý kéo kéo đến câu trả lời sai lầm của mình.

Cuộc tranh luận đa dạng không phải là sự đa dạng tự do. Một mô hình yếu (ví dụ, một parameter Llama 7B) có thể bỏ phiếu hơn mô hình mạnh (GPT-4) nếu mô hình mạnh gia tăng quá mạnh mẽ đối với các câu trả lời sai lầm của mô hình yếu.

> 异构辩论不是免费多样性──弱模型(如 7B 参数 Llama) có thể否决强模型(GPT-4), nếu强模型 quá激进地向弱模型的自信错答案更新──校准哪些模型参与──

### NLSOM  mở rộng 129-agent

Zhuge et al. ("Mindstorms in Natural Language-Based Societies of Mind", arXiv:2305.17066) đã mở rộng ý tưởng này sang 129 xã hội thành viên. Kết quả: chuyên môn hóa và tự tổ chức xuất hiện với quy mô, và hệ thống vượt trội hơn một đại lý trong các nhiệm vụ như trả lời câu hỏi trực quan.

> Zhuge 等人("Based on Natural Language的心智社会中的思维风暴",arXiv:2305.17066) sẽ mở rộng ý tưởng này đến 129 thành viên xã hội── kết quả: chuyên nghiệp hóa và tự tổ chức theo quy mô, hệ thống trong các nhiệm vụ như hình ảnh câu trả lời, ưu việt hơn một đại lý──

Kết quả quy mô là đáng chú ý: sau ~ 50 đại lý, các vai trò cá nhân bắt đầu chuyên môn mà không được nói. Một số trở thành "nhà nghiên cứu", "một số khác" phê bình, "một số khác" tổng hợp.

> Kết quả mở rộng đáng chú ý: sau hơn 50 đại lý, vai trò cá nhân bắt đầu chuyên nghiệp hóa trong tình huống không được biết. Một số trở thành "nhà nghiên cứu"、 những người "chính trị"、 những người "chính trị" khác.

### Các chế độ thất bại

- **Sycophancy cascade.**Tất cả các đại lý đều trì hoãn cho bất kỳ đại lý nào có vẻ tự tin nhất. Cuộc tranh luận sụp đổ với giọng nói lớn nhất.
  Trung ngữ翻译:**谄媚级联。**所有 Agent 屈服于听起来最自信的 Agent──辩论崩为最大声音──对抗角色的提示──"Một Agent 必须论证反方立场") có ích──
- **Topic drift.**Các cuộc tranh luận trong nhiều vòng trôi ra khỏi câu hỏi ban đầu.
  Trung ngữ翻译:**主题漂移。**Nhiều vòng tranh luận rời khỏi vấn đề ban đầu.
- **Compute blowup.**N đại lý x R vòng = N*R LLM cuộc gọi, mỗi cuộc gọi có một bối cảnh phát triển. Một cuộc tranh luận 5 đại lý, 5 vòng là 25 cuộc gọi trong bối cảnh phát triển. Chi phí cho mỗi câu hỏi có thể vượt quá 10 lần một cuộc gọi CoT duy nhất.
  Trung ngữ翻译:**计算爆炸。**N 个 Agent x R 轮 = N*R 次 LLM 调用, mỗi lần trên dưới văn bản đều đang tăng lên.

## Hãy xây dựng nó.
```figure
multi-agent-debate
```

## Hãy xây dựng nó

`code/main.py`chạy một cuộc tranh luận 3 đại lý x 3 vòng về một câu hỏi toán học nơi mỗi đại lý bắt đầu với một câu trả lời khác nhau (có thể sai).

> `code/main.py`Trong một vấn đề toán học, vận hành 3 Agent x 3 vòng tranh luận, mỗi Agent bắt đầu từ một câu trả lời khác nhau (có thể sai lầm).

Demo cho thấy hai hiệu ứng chính:

> 演示 đã cho thấy hai tác dụng quan trọng:

- Một vòng trao đổi duy nhất giúp các đại lý tiến gần hơn đến câu trả lời chính xác.
  Trung文翻译:单轮交流将 代理移向正确答案──
- Các vòng bổ sung sau vòng 2 cho thấy lợi nhuận giảm (cái khớp với cao nguyên của Du et al).
  Trung ngữ翻译: vượt quá số lượt 2 của số lượt 2 cho thấy thu nhập giảm ((匹配 Du 等人的平台) ]]

Đi chạy:

```
python3 code/main.py
```

## Hãy sử dụng nó để thực hiện

`outputs/skill-debate-configurator.md`cấu hình một cuộc tranh luận cho một nhiệm vụ mới: số lượng các đại lý, số lần ra mắt, tính đa dạng (những mô hình tương tự so với hỗn hợp), việc phân bổ vai trò (tương đối so với một đối thủ).

> `outputs/skill-debate-configurator.md`Đối với một đối thủ đối phương, nó cũng đang hoạt động trước khi đánh giá token 成本。

## Chuyển nó đi.

Nếu bạn vận chuyển tranh luận:

> Nếu bạn:

- **Cap rounds at 3.**Du et al. cho thấy 3 vòng chiếm phần lớn lợi nhuận.
  Trung ngữ翻译:**将轮数限制在 3。**Du 等人 cho thấy 3 vòng thu được phần lớn lợi ích.
- **Cap agents at 5.**Ngoài 5, tình trạng bùng nổ và chi phí chiếm ưu thế.
  Trung ngữ翻译:**将 Agent 限制在 5。**超过 5 个,上下文膨胀和成本占主导.
- **Heterogeneous by default.**Ít nhất là hai mẫu cơ sở khác nhau trong hồ bơi.
  Trung ngữ翻译:**默认异构。**Có ít nhất hai mô hình cơ bản khác nhau trong hồ.
- **Adversarial slot.**Một nhân viên đã khiến tôi bất đồng bất kể.
  Trung ngữ翻译:**对抗角色。**Một nhân viên được đề nghị bất cứ cách nào phải chống lại.
- **Log every round.**Các hệ thống tranh luận che giấu các vòng trung gian không thể được gỡ lỗi hoặc kiểm toán.
  Trung ngữ翻译:**记录每轮。**Hệ thống tranh luận trong vòng giữa không thể điều tra hoặc kiểm tra.

## Tập luyện bài tập

1. Đi chạy`code/main.py`, sau đó đặt số vòng lên 5 và xem lợi nhuận giảm.
   Trung ngữ翻译:运行 `code/main.py`, sau đó sẽ đặt số vòng lên 5 và quan sát lợi nhuận giảm.
2. Thêm một nhân viên thứ tư với vai trò đối lập: luôn không đồng ý với đa số hiện tại.
   Trung ngữ: Ước tính thứ tư có chống đối vai trò của Agent:总是不同意与当前多数.
3. Trình (phác) điểm thỏa thuận cho mỗi vòng (phân số các đại lý trên câu trả lời đa số). Khi nào nó đạt 1,0 và đó tương đương với "sự đúng"?
   Trung ngữ翻译:绘制 (打印) mỗi vòng một致性分数 () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () () ()
4. Đọc Du et al. Phần 4 Ablations. sao chép "chỉ đại lý" vs "chỉ vòng" vs "cả hai" kết quả bằng cách sử dụng mã này.
   Trung ngữ翻译:阅读 Du 等人第 4节消融实验──使用此代码复现"仅代理"vs"仅轮数"vs"两者结合"的结果──
5. Đọc "Chúng ta nên điên lên?" (arXiv:2311.17371) và liệt kê hai biến thể tranh luận ngoài vòng tròn  ví dụ, do thẩm phán dẫn đầu, chuỗi tranh luận, đối thủ.
   Trung ngữ翻译:阅读" Should we go towards MAD ?" (ArXiv:2311.17371)并列出两种轮询之外辩论变体例如,裁判主导、辩论链、对抗式──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Society of Mind / 心智社会 | "Minsky's idea" / "Minsky 的想法" | Intelligence as interacting specialists; 1986 framing now operationalized via LLM debate. / 智能作为交互的专家；1986 年的框架现在通过 LLM 辩论实现。 |
| Multi-agent debate / 多 Agent 辩论 | "Agents argue" / "Agent 争论" | N agents propose, critique each other, revise over R rounds, majority-vote. / N 个 Agent 提议、批评彼此、在 R 轮中修改、多数投票。 |
| Consensus / 共识 | "They agree" / "他们一致" | Not epistemic truth — just fraction-on-majority-answer. Can be confidently wrong. / 不是认识论真理——只是多数答案上的比例。可能自信地犯错。 |
| Rounds / 轮次 | "Exchange steps" / "交换步骤" | One round = each agent reads the others and updates once. / 一轮 = 每个 Agent 阅读其他 Agent 并更新一次。 |
| Heterogeneous debate / 异构辩论 | "Mix model families" / "混合模型族" | Using different base models to decorrelate errors. / 使用不同的基础模型来去相关错误。 |
| Sycophancy cascade / 谄媚级联 | "Everyone agrees with the loud one" / "每个人都同意最大声的" | Debate failure where agents defer to the most confident agent regardless of correctness. / 辩论失败，Agent 不顾正确性屈从于最自信的 Agent。 |
| NLSOM | "129-agent society" / "129 Agent 社会" | Natural-language society of mind; Zhuge et al.'s scaled version. / 自然语言心智社会；Zhuge 等人的扩展版本。 |
| Correlated error / 相关错误 | "Same model, same bug" / "相同模型，相同 bug" | Why self-consistency saturates; debate across different views decorrelates. / 自我一致性为什么饱和；不同观点的辩论去相关。 |

## Xem thêm 延伸阅读

- [Du et al. — Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325) giấy tham chiếu, ICML 2024
  Trung văn翻译:Du 等人  通过多 Agent 辩论改进语言模型的事实性和推理  参考论文, ICML 2024
- [Zhuge et al. — Mindstorms in Natural Language-Based Societies of Mind](https://arxiv.org/abs/2305.17066) 129-agent NLSOM
  Trung文翻译:Zhuge 等人  基于自然语言的心智社会中的思维风暴  129 Đại diện NLSOM
- [Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs](https://arxiv.org/abs/2311.17371) Các biến thể tranh luận tham chiếu
  Trung文翻译: 我们应该走向 MAD 吗?多 代理辩论策略研究 辩论变体基准测试
- [Debate project page](https://composable-models.github.io/llm_debate/) Mã của Du et al., chi tiết về demo và việc bỏ
  Trung文翻译:辩论项目页面  Du 等人的代码、演示和消融细节
