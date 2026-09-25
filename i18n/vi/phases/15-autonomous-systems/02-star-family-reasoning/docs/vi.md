# STAR, V-STAR, Quiet-STAR  Tự học lý luận  STAR 系列 tự đoán phương pháp

> Loop tự cải thiện nhỏ nhất có thể nằm trong lý luận. Một mô hình tạo ra một chuỗi suy nghĩ, giữ những câu trả lời đúng, và tinh chỉnh những câu trả lời đó. Đó là STAR. V-STaR thêm một xác minh để lựa chọn thời gian suy luận là tốt hơn. Quiet-STaR đẩy lý do xuống mọi dấu hiệu. Cả ba đều làm việc. Không có một trong số đó là ma thuật  vòng lặp bảo tồn bất kỳ đường tắt nào xảy ra để đạt được câu trả lời đúng.

> **【中文解读】**Chuyện tự cải tiến nhỏ nhất ẩn trong quá trình suy luận: mô hình tạo ra chuỗi suy nghĩ, giữ lại quá trình suy luận của câu trả lời chính xác, điều chỉnh nhỏ trên dữ liệu này. Đây là STaR. V-STaR  thêm chứng minh cải thiện suy luận khi chọn.

> **【拓展：STaR → OpenAI o1/o3 的自我改进】**STaR 系列 là một mô hình tư tưởng cốt lõi của việc đào tạo "self-blowing" để tự đào tạo mình bằng tư duy của mình. OpenAI o1/o3 系列 系列 模型背后 của tập luyện hóa học mạnh mẽ đã sử dụng một cách tương tự như vậy: tạo ra nhiều con đường tư duy, chọn đúng, sử dụng chúng để cải thiện mô hình.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bootstrap-loop simulator) | **语言:** Python (标准库，bootstrap 循环模拟器)
**Prerequisites:** Phase 13 · 01-03 (Reasoning and CoT), Phase 15 · 01 (long-horizon framing) | **前置知识:** Phase 13 · 01-03（推理与 CoT），Phase 15 · 01（长程框架）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 13·01-03(CoT 思维链) Phase 11·08(SFT 监督微调) Phase 15·01(长程 Agent 框架) ・STaR là vòng kết thúc nhỏ nhất của "自蒸 + 推理增强"
>  **【类比】**STaR = "đánh giá tự học sinh"──普通学习 = 老师改作业学生订正(人工标注推理过程);STaR = 学生写推理→对答案→对对的推理保留并自我再练一遍(自我生成训练数据)── vấn đề là: đôi khi quá trình推理是错误的但答案巧合对对对对对对对,STaR sẽ tăng cường loại "蒙对" này推理V-STaR加一个法官验证器) 掉错推理
> ️ **【易错点】**STaR 训练时只看"答案是否正确"会强化"捷径推理"(错误过程但正确结果) ――修复:用过程奖励(PRM,Phase 13·03) thay thế kết quả奖励, từng bước推理都打分; hoặc sử dụng V-STaR 加验证器 检查推理质量──

## Vấn đề  vấn đề giới thiệu giới thiệu

Cách đơn giản để dạy một mô hình suy luận là thu thập những dấu vết suy luận được viết bởi con người.

> Cách trực tiếp của mô hình tư duy là thu thập các đường lối tư duy của văn bản con người.

STaR (Self-Teught Reasoner, Zelikman et al., 2022) hỏi: nếu mô hình viết racional của riêng mình và xếp hạng chúng so với các câu trả lời đã biết?

> STaR(self teaching推理器, Zelikman 等人,2022) đề xuất: Nếu mô hình tự viết quá trình推理并与已知答案对照评分会怎么样? vòng lặp là:


> **【中文解读】**Star 家族推理技术 (STAR、Quiet-STaR、ReST、ReST-EM) thông qua代式自我训练提升 LLM 推理能力──核心思想:让模型生成推理轨迹,过高质量轨迹,用这些轨迹微调模型,循环代──这是OpenAI o1/o3 系列和人类扩展思想的技术基础──

1. Mô tả một câu trả lời lý luận cộng với.
2. Nếu câu trả lời cuối cùng là đúng, hãy giữ dấu vết.
3. Định nghĩa kỹ lưỡng về những dấu vết được giữ.
4. Lặp lại.

Nó hoạt động. GSM8K và CommonsenseQA đều được cải thiện mà không cần ghi chú của con người mới. Nhưng vòng lặp có một thiên vị tích hợp: bất kỳ lý luận nào tạo ra câu trả lời đúng đắn vẫn được giữ lại, bất kể lý luận đó có hay không. V-STaR (Hosseini et al., 2024) sửa chữa điều này với một xác minh học tập; Quiet-STaR (Zelikman et al., 2024) tổng quát ý tưởng để tính racional nội bộ.

> Nó có hiệu lực. GSM8K và CommonsenseQA có sự nâng cao trong trường hợp không có dấu hiệu của con người mới. Nhưng vòng có một sự lệch trong nội bộ: bất kỳ quá trình suy luận nào tạo ra câu trả lời chính xác đều được giữ lại, bất kể suy luận có hợp lý hay không.

## Khái niệm cốt lõi

### STaR: bootstrap trên những gì đã làm việc

Bắt đầu từ một mô hình cơ bản với một số khả năng suy luận yếu. Đối với mỗi vấn đề đào tạo, lấy mẫu lý luận cộng với câu trả lời. Nếu câu trả lời phù hợp với nhãn, giữ cho (vấn đề, lý luận, câu trả lời) ba. Hoàn chỉnh mô hình trên bộ được giữ. Lặp lại.

> Bắt đầu từ một mô hình cơ bản có khả năng suy luận kém hơn. Trong mỗi câu hỏi đào tạo, lấy một quá trình suy luận thêm câu trả lời. Nếu câu trả lời phù hợp với nhãn, giữ lại câu hỏi.

Một vòng quay quan trọng. Nếu mô hình không bao giờ có thể làm cho một vấn đề đúng, vòng lặp không thể học được trên nó.**rationalization**: cho các vấn đề mô hình thất bại, tiêm câu trả lời chính xác như một gợi ý và nhắc lại mô hình để tạo ra một lý luận dẫn đến nó.

> Một sự chuyển đổi quan trọng. Nếu mô hình không thể trả lời một câu hỏi chính xác, vòng lặp sẽ không thể học được từ đó.**合理化**Đối với các vấn đề thất bại của mô hình, sẽ được đưa ra các câu trả lời chính xác như một lời khuyên, tái đưa ra các mô hình để tạo ra các quy trình suy luận hướng đến câu trả lời đó.

Kết quả trong bài báo ban đầu (Zelikman et al., 2022): mô hình cơ sở GPT-J cải thiện trên GSM8K từ 5.8% lên 10.7% thông qua các vòng STaR lặp đi lặp lại với hợp lý hóa  khoảng 5 điểm phần trăm tuyệt đối. Trên CommonsenseQA, GPT-J 6B được đào tạo bằng STaR đạt 72,5%, tương đương với một mô hình GPT-3 175B được điều chỉnh tốt (~ 73%)  mô hình lớn hơn khoảng 30 lần được đào tạo trên các hợp lý ghi chép bằng tay.

> Kết quả của nghiên cứu: GPT-J cơ bản mô hình thông qua hợp lý hóa lặp lại STaR 轮次, trên GSM8K tăng từ 5,8% lên 10,7%  khoảng 5 điểm phần trăm 绝对提升. trên CommonsenseQA, GPT-J 6B của STAR 训练 đạt 72,5%, có thể so sánh với GPT-3 175B 微调 (khoảng 73%) so với những mô hình sau đây là sử dụng các mô hình ghi nhận tay tay 

### V-STaR: đào tạo một kiểm chứng với DPO

STaR ném ra những lý luận sai lầm. Hosseini et al. (2024) quan sát rằng đó cũng là dữ liệu: mỗi cặp (rationale, "có đúng không") có thể đào tạo một xác minh. Họ sử dụng tối ưu hóa ưu tiên trực tiếp trên cả các giải pháp đúng và sai để xây dựng một trình xếp hạng.

> STaR  bỏ qua các lý thuyết sai lầm. Hosseini 等人 (Hosseini 等人) ]]2024) quan sát thấy những dữ liệu này: mỗi đối với quy trình sai lầm, "Đây là đúng hay không") có thể được đào tạo bằng chứng nhận.

Delta được báo cáo: +4 đến +17 điểm phần trăm so với các đường cơ sở tự cải thiện trước đây trên GSM8K và MATH, với phần lớn lợi nhuận đến từ việc sử dụng xác minh cho việc lựa chọn thời gian suy luận thay vì cho việc điều chỉnh kỹ lưỡng thêm máy phát.

> 报告的提升: trên GSM8K 和 MATH trên so với các bản cải tiến tự do trước đó nâng cao +4 đến +17 điểm trăm, phần lớn nâng cao đến từ các bộ xác minh lựa chọn khi suy đoán chứ không phải các bộ tạo thêm.

### Quiet-STaR: các tính toán nội bộ mỗi token

Zelikman et al. (2024) hỏi: nếu mô hình học được tạo ra một lý luận nội bộ ngắn ở mỗi vị trí token, không chỉ giữa vấn đề và câu trả lời? Quiet-STaR đào tạo mô hình để phát ra một "lời nghĩ" ẩn trước mỗi token dự đoán, sau đó trộn dự đoán ý thức với dự đoán đường cơ sở thông qua trọng lượng được học.

> Zelikman 等人 (pp. 2024) đề xuất: Nếu mô hình học tập tạo ra một lý luận nội bộ ngắn gọn ở mỗi vị trí của mỗi token, chứ không chỉ là giữa câu hỏi và câu trả lời?

Kết quả: Mistral 7B đạt được cải thiện tuyệt đối bằng không chụp trên GSM8K từ 5,9% đến 10,9% và CommonsenseQA từ 36,3% đến 47,2% mà không có điều chỉnh cụ thể về nhiệm vụ. Mô hình học "lúc nào để suy nghĩ"  mã thông báo cứng có được các hợp lý nội bộ dài hơn; những cái dễ dàng nhận được hầu như không có.

> Kết quả:Mistral 7B trên GSM8K trên 0 mẫu tuyệt đối tăng từ 5.9% đến 10.9%, trên CommonsenseQA từ 36.3% đến 47.2%, không cần các nhiệm vụ cụ thể.

### Tại sao cả ba đều có mối quan tâm chung về an toàn

Cả ba phương pháp đều sử dụng câu trả lời cuối cùng như tín hiệu gradient. Một lý luận đạt được câu trả lời đúng thông qua lý luận sai lầm  khai thác một đường tắt, đoán hoặc sử dụng một mô hình không tổng quát  được củng cố tích cực.

> Ba phương pháp đều sử dụng câu trả lời cuối cùng như một tín hiệu thang độ. Thông qua các suy luận có thiếu sót để đạt được câu trả lời chính xác.

V-STaR xác minh giảm thiểu bằng cách học cách xếp hạng lý lẽ, nhưng xác minh được đào tạo trên cùng một bộ nhãn. Nó có thể học cách thích lý luận sai lầm định dạng tốt hơn sự không chắc chắn trung thực. Thiết kế an toàn hơn là kết hợp dữ liệu kiểu STaR với (a) mô hình phần thưởng được giám sát bởi quy trình (bồi thường các bước trung gian, không chỉ trả lời) và (b) đánh giá OOD được thực hiện để phá vỡ các đường tắt đơn giản.

> V-STaR xác minh bằng cách học về các loại hình để giảm thiểu, nhưng các xác minh được đào tạo trên cùng một tập hợp nhãn. Nó có thể học được định dạng thích hợp nhưng không trung thực của các hình thức xác định sai trái.

### So sánh

| Method | Training signal | Inference cost | Data waste | Known failure mode |
|---|---|---|---|---|
| 方法 | 训练信号 | 推理成本 | 数据浪费 | 已知失败模式 |
| STaR | keep (rationale, answer) if correct | 1x | discards all incorrect rationales | shortcut rationales |
| STaR | 正确时保留（推理，答案） | 1x | 丢弃所有不正确的推理 | 捷径推理 |
| STaR + rationalization | above + correct-answer hinted retries | 1x | less | rationalized rationales may be implausible |
| STaR + 合理化 | 上述 + 正确答案提示重试 | 1x | 较少 | 合理化的推理可能不可信 |
| V-STaR | STaR + DPO verifier from both classes | Nx (best-of-N) | minimal | verifier can reinforce confident wrongness |
| V-STaR | STaR + 两类 DPO 验证器 | Nx（N 中选优） | 最少 | 验证器可能强化自信的错误 |
| Quiet-STaR | per-token rationale + mixing weight | 1.5-3x | minimal | still answer-conditioned gradient |
| Quiet-STaR | 每 token 推理 + 混合权重 | 1.5-3x | 最少 | 仍是答案条件梯度 |

### Ở đâu đây nằm trong đống 2026

STAR đã già rồi. Nhưng mô hình này xuất hiện lại ở khắp mọi nơi trong năm 2025-2026. RL trên các vấn đề toán học có thể xác minh (DeepSeek-R1, Kimi-k1.5, o1) là tín hiệu gradient đáp ứng điều kiện của STaR, mở rộng quy mô. Các mô hình phần thưởng quy trình (Lightman et al., 2023; "Hãy xác minh từng bước") của OpenAI là lựa chọn thay thế được giám sát bởi quy trình. AlphaEvolve (Dạy 3) là STaR cho mã, với một trình đánh giá chương trình thay vì một nhãn. Máy Darwin Godel (Học 4) là STaR cho chính sàn nhà đại lý.

> STaR  đã quá cũ. Nhưng mô hình này xuất hiện ở khắp nơi trong năm 2025-2026 RL trên các vấn đề toán học có thể xác minh được DeepSeek-R1、Kimi-k1.5、o1) là mô hình giải thưởng quy trình của STaR n bản mở rộng n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n 

Hiểu STaR làm cho tất cả các nhấp chuột này. Đó là vòng tự cải thiện tối thiểu khả thi.

> Nghĩ STaR 让所有这些都说通―― Đó là vòng tự cải thiện nhỏ nhất có thể làm.

## Hãy sử dụng nó để thực hiện
```figure
reflection-loop
```

## Sử dụng nó

`code/main.py`chạy một vòng lặp STaR mô phỏng trên một nhiệm vụ toán học đồ chơi.

- Sự chính xác vượt qua các đạn khởi động.
  Trung文翻译:准确率如何在bootstrap 轮次中升──
- Cách rút ngắn lẻn vào: máy mô phỏng bao gồm một lớp lý luận "lười biếng" có được câu trả lời đúng trong 40% thời gian nhưng tổng quát kém.
  Trung ngữ翻译:捷径如何潜入模拟器包含一个"惰"推理类,40% thời gian nhận được câu trả lời chính xác nhưng phổ biến rất kém.
- Làm thế nào một người xác minh (tương tự V-STaR) giúp suy luận nhưng không thể cắt hoàn toàn các đường tắt được đưa ra trong quá trình đào tạo.
  Trung ngữ翻译:验证器(V-STaR 风格) làm thế nào trong quá trình suy nghĩ giúp đỡ nhưng không thể hoàn toàn cắt cắt trong quá trình đào tạo.

## Chuyển nó đi.

`outputs/skill-star-loop-reviewer.md`giúp bạn kiểm tra một đường ống dẫn lý luận tự học được đề xuất trước khi bạn tập luyện trên nó.

> `outputs/skill-star-loop-reviewer.md` giúp bạn kiểm tra đề xuất của tự học trước khi đào tạo 

## Tập luyện bài tập

1. Cứ chạy máy mô phỏng. Đặt tần số đường tắt là 0,4, sau đó là 0,4. Độ chính xác cuối cùng khác nhau giữa hai chạy, mặc dù cả hai đều đạt > 90% trên phân phối huấn luyện?
   Trung ngữ翻译: tỷ lệ phân chia cuối cùng giữa hai lần vận hành là bao nhiêu, ngay cả khi cả hai trong phân bố tập luyện đều đạt > 90%?

2. Thêm một thử nghiệm OOD kéo dài vào mô phỏng. Chụp các vấn đề từ một phân phối khác và đánh giá mô hình khởi động trên cả bộ phân phối và OOD.
   Trung ngữ翻译:量化差距──

3. Đọc bài báo Quiet-STaR (arXiv:2403.09629) Phần 3. Giải thích biểu tượng "sự kết thúc suy nghĩ" và đầu cân trộn trong ba câu mỗi câu.
   Trung文翻译:用三句话分别解释"思考结束"token 和混合权重头──

4. So sánh bộ lọc giữ nếu STaR là đúng với một lựa chọn thay thế được giám sát bởi quy trình mà thưởng cho từng bước hợp lý độc lập.
   Trung ngữ翻译:识别标注成本差异和质量差异.

5. Thiết kế một đánh giá sẽ bắt được các lý do tắt trong một mô hình được triển khai. Nó không phải là hoàn hảo  nó phải phá vỡ các đường tắt đơn giản nhất một vòng lặp STaR sẽ tăng cường.
   Trung ngữ翻译: nó chỉ cần phá vỡ đường lối đơn giản nhất của STaR 循环会强化.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| STaR | "Self-Taught Reasoner" | Fine-tune on model-generated rationales that land correct answers; repeat |
| STaR | "自我教学推理器" | 在模型生成的正确推理上微调；重复 |
| Rationalization | "Hinted retry" | Inject the correct answer and re-prompt for a rationale |
| 合理化 | "提示重试" | 注入正确答案重新提示推理 |
| V-STaR | "Verifier STaR" | DPO-train a verifier on both correct and incorrect rationales |
| V-STaR | "验证器 STaR" | DPO 训练验证器用于推理时选择 |
| Quiet-STaR | "Per-token rationales" | Generate hidden thoughts at every token position; mix with baseline |
| Quiet-STaR | "每 token 推理" | 在每个 token 位置生成隐藏思考；与基线预测混合 |
| Answer-conditioned gradient | "Outcome-based signal" | The training loop rewards final answers, not reasoning steps |
| 答案条件梯度 | "基于结果的信号" | 训练循环奖励最终答案，而非推理步骤 |
| Process reward model | "Step-level verifier" | Reward model trained on per-step correctness, not outcome |
| 过程奖励模型 | "步骤级验证器" | 在每步正确性上训练的奖励模型 |
| Shortcut rationale | "Right answer, wrong reasoning" | A rationale that reaches the label via a non-generalizing pattern |
| 捷径推理 | "正确答案，错误推理" | 通过不可泛化模式达到标签的推理 |

## Xem thêm 延伸阅读

- [Zelikman et al. (2022). STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465) giấy gốc.
  Trung ngữ翻译:原始论文。
- [Hosseini et al. (2024). V-STaR: Training Verifiers for Self-Taught Reasoners](https://arxiv.org/abs/2402.06457) thêm một DPO xác minh cho việc lựa chọn thời gian suy luận.
  Trung文翻译:添加 DPO 验证器用于推理时选择。
- [Zelikman et al. (2024). Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking](https://arxiv.org/abs/2403.09629) mỗi token racional nội bộ.
  Trung文翻译: 每 token 内部推理。
- [Lightman et al. (2023). Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) mô hình phần thưởng quá trình, tín hiệu gradient thay thế.
  Trung文翻译:过程奖励模型,替代梯度信号──
- [DeepSeek-R1 paper (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948) RL về các nhiệm vụ có thể kiểm tra, STaR mở rộng đến đào tạo biên giới.
  Trung文翻译: RL trên nhiệm vụ có thể xác nhận,STaR 扩展到前沿训练。
