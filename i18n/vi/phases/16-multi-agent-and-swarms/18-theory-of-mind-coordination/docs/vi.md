# Lý thuyết về tâm trí và sự phối hợp mới nổi .

> Li et al. (arXiv:2310.10701) cho thấy rằng các đại lý LLM trong một triển lãm trò chơi văn bản hợp tác **emergent high-order Theory of Mind**(ToM)  lý luận về những gì một đại lý khác tin về niềm tin của một đại lý thứ ba  nhưng thất bại trong lập kế hoạch chân trời dài do quản lý bối cảnh và ảo giác. Riedl (arXiv:2510.05174) đo lường sự hợp tác thứ tự cao hơn trên một quần thể và phát hiện ra rằng **only**Điều kiện ToM-prompt tạo ra sự phân biệt liên quan đến danh tính và sự bổ sung hướng đến mục tiêu; LLM có khả năng thấp chỉ cho thấy sự xuất hiện giả mạo. Đó là sự xuất hiện của sự phối hợp là điều kiện ngay lập tức và phụ thuộc vào mô hình, không phải miễn phí. Bài học này thực hiện một nhân viên biết đến ToM tối thiểu, thực hiện một nhiệm vụ hợp tác với và mà không có sự thúc đẩy ToM, và đo lường delta phối hợp so với giao thức Riedl 2025.

> **【中文解读】**Bài viết này giới thiệu về cơ chế phối hợp của các tác nhân hiểu và dự đoán các tác nhân khác 意图.

> **【拓展：theory of mind coordination→具体应用】**心理理論 (心智理論) là khả năng hiểu và dự đoán tình trạng tâm lý của người khác. Trong nhiều hệ thống, một người có lý thuyết tâm trí có thể phối hợp tốt hơn với người khác.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 17 (Generative Agents) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 17（生成式 Agent）

>  **【前置】**学本节前请先掌握:Phase 16·07(辩论) 、Phase 16·17(生成式代理) 、认知科学 概念思想理论――ToM = Agent 推理"其他 Agent 在想什么"―
>  **【类比】**ToM = "Hội đồng lý tưởng của đại lý"。无 ToM Agent = tự nói tự话;有 ToM Agent = 站在对方角度思考"他认为我知道这个事吗?"高阶 ToM = 嵌套推理?
**Time:** ~75 minutes | **时间:** ~75 分钟

##                                                                                                                                                                                                                                                               

Sự phối hợp đa đại lý thường trông rất kỳ diệu: các đại lý chia lao động, dự đoán lẫn nhau, tránh việc tháo dỡ. Thông thường "sự xuất hiện" này là một tác phẩm của kỹ thuật nhanh chóng  ai đó nói với các đại lý "coordinate".

> Nhiều đại lý phối hợp thường trông rất kỳ lạ: đại lý phân công, đoán trước lẫn nhau, tránh thiếu sót.

Kết quả 2025 của Riedl là nghiêm ngặt hơn: trong các điều kiện được kiểm soát, sự phối hợp chỉ xuất hiện khi các đại lý được nhắc nhở để suy luận về **other agents' minds**(ToM). Không có sự phối hợp ToM, ngay cả các mô hình mạnh cũng cho thấy các mô hình phối hợp không tồn tại trong kiểm soát thống kê.

> Riedl 2025 phát hiện nghiêm ngặt hơn: trong điều kiện được kiểm soát, phối hợp chỉ với đại lý được khuyến cáo**其他 Agent 的心理**(ToM) khi xuất hiện. Không có ToM 提示, ngay cả mô hình mạnh cũng cho thấy một mô hình phối hợp không tồn tại dưới sự kiểm soát thống kê.

Bài học này xử lý ToM như một khả năng cụ thể (sự lý luận về niềm tin về niềm tin), xây dựng một đại lý ít ToM-thấu hiểu, và đo lường sự phối hợp thực sự trông như thế nào so với cách trang phục nhanh như thế nào.

> Bài học này sẽ xem ToM như một khả năng cụ thể để đưa ra suy luận về niềm tin), xây dựng một ToM ảm nhận nhỏ nhất, và đo lường sự khác biệt giữa sự phối hợp thực sự và sự trang trí gợi ý.

## Khái niệm cốt lõi

### ToM có nghĩa là gì

Tâm lý phát triển: một đứa trẻ 3 tuổi nghĩ rằng thế giới bên trong của bất kỳ ai cũng phù hợp với thế giới của họ. Một đứa trẻ 5 tuổi hiểu rằng người khác có niềm tin khác nhau. Một đứa trẻ 7 tuổi lý do về niềm tin về niềm tin ("anh ấy nghĩ rằng tôi nghĩ rằng quả bóng đang nằm dưới cốc").

> 发展心理学: 3 岁的孩子认为任何人的内心世界都与自己相同―― 5 岁的孩子理解他人有不同的信仰―― 7 岁的孩子推推论关于信仰的信念――"她认为我认为球在杯子下面")――这些是零阶段,一阶段和二阶段 ToM――

Đối với các đại lý LLM, ToM yêu cầu bản đồ đến:

> Đối với đại lý LLM, ToM 阶次映射到:

- **Zeroth-order:**Không có mô hình của người khác.
  Trung ngữ翻译:**零阶：**Không có mô hình của người khác.
- **First-order:**"Alice tin X".
  Trung ngữ翻译:**一阶：**"Alice 相信 X" là một hình thức của niềm tin của một đại lý đối với mọi đại lý khác.
- **Second-order:**"Alice tin rằng Bob tin X".
  Trung ngữ翻译:**二阶：**"Alice 相信 Bob 相信 X".

Li et al. 2023 phát hiện ra rằng ToM thứ nhất và thứ hai xuất hiện trong các đại lý LLM trong các trò chơi hợp tác nhưng suy giảm với chân trời dài và giao tiếp không đáng tin cậy.

> Li 等人 năm 2023 phát hiện ra, giai đoạn một và giai đoạn hai ToM trong hợp tác trò chơi LLM đại lý xuất hiện, nhưng trong phạm vi thời gian dài và không thể tin cậy giao tiếp giảm dần.

### Thử nghiệm Sally-Anne, ngắn gọn

Một bài kiểm tra tin tưởng sai năm 1985: Sally đặt một viên đá cẩm thạch trong giỏ A, rời khỏi. Anne di chuyển nó đến giỏ B. Sally sẽ nhìn ra đâu khi cô trở lại?

> 1985 年的错误信念测试:Sally đặt viên ngọc vào hộp A, bỏ đi.Anne đặt nó vào hộp B.Sally quay lại sẽ đi tìm đâu? có một giai đoạn ToM của đứa trẻ nói hộp A.Sally's belief differs from reality.

Các LLM thời GPT-4 vượt qua các bài kiểm tra kiểu Sally-Anne khi được đặt ra một cách rõ ràng. Họ thất bại khi câu chuyện dài, cảnh quay thay đổi nhiều lần, hoặc câu hỏi được phrased gián tiếp. Đó là tình trạng thực tế của ToM năm 2026 trong LLM sản xuất.

> GPT-4 时代的LLM 在直接问时通过Sally-Anne 风格测试――当叙述很长,场景多次变化或问题间接表达时失败――这是2026年生产LLM 中 ToM的实际状态――

### Phân tích phối hợp của Riedl

Riedl (arXiv:2510.05174) đã xây dựng một thử nghiệm quy mô dân số: N đại lý, một mục tiêu hợp tác, điều kiện nhanh chóng biến đổi.

> Riedl(arXiv:2510.05174) xây dựng quy mô nhóm测试:N 个 Agent,合作目标,可变提示条件――测量:

1. **Identity-linked differentiation.**Các đại lý có phát triển sự phân biệt vai trò ổn định theo thời gian không?
   Trung ngữ翻译:**身份关联分化。**Trưởng phòng có vai trò ổn định không?
2. **Goal-directed complementarity.**Các hành động của các đại lý có bổ sung lẫn nhau (các nhiệm vụ phụ khác nhau) chứ không phải trùng lặp?
   Trung ngữ翻译:**目标导向互补性。**Hành vi của đại lý là bổ sung (đầu nhiệm khác nhau) chứ không phải lặp lại?
3. **Higher-order synergy.**Một thước đo thống kê về việc nhóm có đạt được những gì không có bộ phụ nào có thể đạt được.
   Trung ngữ翻译:**高阶协同。**群体是否达成任何子集都无法达成的统计量度.

Kết quả: chỉ trong điều kiện ToM prompt thì cả ba métrics đều tạo ra tín hiệu trên đường gốc. Không có ToM prompt, métrics hơ gần khả năng cho các mô hình công suất vừa phải. Các mô hình lớn cho thấy một số sự phối hợp mà không có ToM prompt rõ ràng nhưng hiệu ứng nhỏ hơn so với với các prompt rõ ràng.

> Kết quả: Chỉ trong điều kiện ToM 提示, ba chỉ số chỉ tạo ra một tín hiệu cao hơn đường cốt lõi. Không có ToM 提示, chỉ số mô hình năng lực trung bình ở gần mức tự nhiên.

### Giảm giác phối hợp

Không có kiểm soát thống kê, "sự phối hợp cấp bách" trong các bản demo thường phản ánh:

> Không có kiểm soát thống kê, biểu hiện "涌现协调" thường phản ánh:

- Kỹ thuật nhanh chóng làm việc phối hợp (các lời nhắc hệ thống nói "hiện hợp tác").
  Trung ngữ翻译:嵌入协调的提示工程(系统提示说"一起工作")
- Bias quan sát viên (chúng ta thấy các mô hình chúng ta mong đợi).
  Trung文翻译:观察者偏差 (我们看到期望的模式)
- Việc lựa chọn sau khi chơi hoc của các chạy thành công.
  Trung文翻译:成功运行的事后选择──

Các hệ thống sản xuất mà tiếp thị "sự phối hợp mới" mà không có tín hiệu có thể đo lường nên được coi như tiếp thị.

> Không có tín hiệu có thể đo lường được về việc tuyên truyền "nghợp tác hiện nay" hệ thống sản xuất nên được xem như là tiếp thị.

### Một đặc vụ ít biết đến ToM

Cấu trúc:

```
agent state:
  own_beliefs:    {facts the agent believes}
  other_models:   {other_agent_id -> {beliefs_the_agent_attributes_to_them}}
  actions_last_N: [history of others' actions]

observation update:
  - update own_beliefs from direct observation
  - update other_models[agent_id] from their action + prior beliefs

action selection:
  - enumerate candidate actions
  - for each, predict what each other agent will do next given their modeled beliefs
  - pick action that maximizes joint outcome under those predictions
```

- `other_models`ToM thứ nhất giữ chỉ một cấp độ. thứ hai thêm`other_models[i][other_models_of_j]` Tôi nghĩ là đại lý tôi nghĩ là đại lý J tin.

### Tại sao đường chân trời dài lại đau

Li et al. tài liệu: giới hạn ngữ cảnh khiến các nhân viên quên đi niềm tin thuộc về ai. ảo giác thêm niềm tin sai vào các mô hình nhân viên khác. Cả hai đều tạo ra sai lầm "Tôi nghĩ anh ta nghĩ X" mà gia tăng theo thời gian.

Các biện pháp giảm thiểu được ghi lại trong báo cáo và theo dõi trong năm 2024-2026:

- **Explicit ToM state in the prompt.**Phương thức cấu trúc: `{agent_id: belief_list}`- Cần thu hồi để giữ lại sự ràng buộc về bản sắc và niềm tin.
- **Shorter reasoning chains.**Ít hơn các bản cập nhật ToM mỗi lượt làm giảm ảo giác hợp chất.
- **External ToM store.**Giữ mô hình bên ngoài bối cảnh LLM; chỉ tiêm các bộ phận liên quan mỗi lượt.

### Khi ToM thất bại trong sản xuất

- **Adversarial settings.**Các đại lý có ToM tốt dễ dàng hơn để thao túng (bạn có thể mô hình hóa những gì họ mô hình hóa bạn, sau đó khai thác).
- **Heterogeneous teams.**Khi các mô hình khác nhau, mô hình ToM hoạt động cho một đối thủ không phổ biến.
- **Ground-truth-dependent tasks.**ToM là về niềm tin; nếu sự chính xác phụ thuộc vào sự thật, ToM có thể là một sự phân tâm.

### Sự phối hợp mà bạn có thể đo lường

Ba tín hiệu thực tế sự sự phối hợp của một nhóm là thực hơn là ăn mặc nhanh chóng:

1. **Complementarity over time.**Trong một nhiệm vụ đa lượt, hành động của các đặc vụ bao gồm các nhiệm vụ phụ không liên quan?
2. **Anticipation.**Hành động của đại lý A ở lượt T+1 phụ thuộc vào một dự đoán về hành động của B ở T+2 đã kết quả chính xác?
3. **Correction.**Khi A đọc sai tin của B ở lượt T, A có sửa bằng lượt T + 2?

Chúng có thể đo lường trong một hệ thống đa đại lý được ghi lại. Chúng là phiên bản bản bản của câu chuyện "sự phối hợp".

## Hãy xây dựng nó.
```figure
sw-theory-of-mind
```

## Hãy xây dựng nó

`code/main.py`thực hiện:

- `ToMAgent` theo dõi niềm tin của riêng mình và các mô hình niềm tin của các đại lý khác.
  Trung ngữ翻译:`ToMAgent`Theo niềm tin của chính mình và mô hình niềm tin của mỗi nhân viên khác.
- Một nhiệm vụ hợp tác: ba đại lý phải thu thập ba token từ ba hộp; mỗi hộp có thể chứa một token.
  Trung ngữ翻译:合作任务:三个代理 必须从三个盒子中收集三个代币;每个盒子只能放一个代币――Agent 不能通信;它们从彼此的行为推断意图――
- Hai cấu hình: `zeroth_order`(không có ToM) và `first_order`(ToM với mô hình niềm tin một cấp).
  Trung ngữ翻译:两种配置:`zeroth_order`(无 ToM) và `first_order`(带一层信念模型的 ToM)
- Đánh giá trên 200 thử nghiệm ngẫu nhiên: tỷ lệ hoàn thành, tỷ lệ trùng lặp (hai đại lý nhắm vào cùng một hộp), trung bình quay đến hoàn thành.
  Trung文翻译:200 次随机试验的测量:完成率、重复率(两个代理 准同一个盒子) 、平均完成轮次。

Đi chạy:

```
python3 code/main.py
```

Tạo ra dự kiến: các đại lý thứ tự không lặp lại nỗ lực với tỷ lệ ~ 35% và hoàn thành ~ 60% các thử nghiệm trong 10 lượt.

> 预期输出: 0阶级代理以约 35% tỷ lệ重复工作完成约 60%试验,10轮内完成约 60%试验―― 1阶级TM Agent以约 5% tỷ lệ重复完成约 95%――差异就是可测量的协调效果――

## Sử dụng nó.

`outputs/skill-tom-auditor.md`là một kỹ năng kiểm tra tuyên bố của một hệ thống đa tác nhân về "sự phối hợp mới". kiểm tra việc trang bị nhanh chóng, ý nghĩa thống kê so với kiểm soát và đo sự bổ sung.

> `outputs/skill-tom-auditor.md`là một kiểm toán đa đại lý  hệ thống "nghợp tác hiện tại" tuyên bố kỹ năng  kiểm tra các ý kiến trang trí  tính quan trọng và tính bổ sung của các phép đo đối với nhóm kiểm soát 

## Đưa nó lên mạng

Danh sách kiểm tra yêu cầu phối hợp:

- **Control condition.**Một phiên bản của hệ thống của bạn mà không có thông báo phối hợp.
  Trung ngữ翻译:**对照条件。**Không có hệ thống để đo lường.
- **Statistical test.**Sự khác biệt giữa hệ thống và điều khiển có đáng kể không?`p < 0.05`trên số liệu của bạn?
  Trung ngữ翻译:**统计测试。** Sự khác biệt giữa hệ thống và ánh sáng trong chỉ số của bạn là `p < 0.05`- Đáng kể?
- **Complementarity measure.**Sự bất đồng hành động theo thời gian, không chỉ là thành công cuối cùng.
  Trung ngữ翻译:**互补性测量。**随时间的动作不交性, không chỉ là thành công cuối cùng.
- **Failure-case log.**Khi các nhân viên không phối hợp đúng, thì tiểu bang ToM trông như thế nào?
  Trung ngữ翻译:**失败案例日志。**Khi đại lý không thành công, tình trạng của anh như thế nào?
- **Model-capacity disclosure.**Nếu tác dụng biến mất trên các mô hình nhỏ hơn, hãy nói như vậy.
  Trung ngữ翻译:**模型能力披露。**Nếu hiệu quả biến mất trên mô hình nhỏ hơn, hãy giải thích điều này.

## Tập luyện bài tập

1. Đi chạy`code/main.py`. xác nhận thứ tự đầu tiên ToM giảm tỷ lệ trùng lặp khoảng 7x. Sự chênh lệch vẫn tồn tại khi bạn mở rộng lên 5 đại lý và 5 hộp?
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận 1 giai đoạn ToM sẽ giảm tỷ lệ lặp lại khoảng 7 lần.
2. Thực hiện ToM thứ hai (các nhân A mô hình những gì B nghĩ về C).
   Trung ngữ翻译:实现二阶 ToM(Agent A 建模 B 对 C 的想法) ―― nó đã cải tiến hơn một阶段 chưa?
3. Tiêm **hallucination**trong trạng thái ToM: ngẫu nhiên đảo ngược một niềm tin mỗi lượt.
   中文翻译:向 ToM 状态注入**幻觉**Mỗi vòng có thể thay đổi một niềm tin.
4. Đọc Li et al. (arXiv:2310.10701). Tái tạo lại phát hiện "sự suy giảm đường chân trời dài": khi lượt tăng từ 10 đến 30, hiệu suất ToM thứ nhất của bạn thay đổi như thế nào?
   Trung văn翻译:阅读 Li 等人(arXiv:2310.10701)。复现"长期退化"发现:当轮次从10 增长到30 时,你的一阶 ToM 性能如何变化?
5. Đọc Riedl 2025 (arXiv:2510.05174). Thực hiện các thống kê tương tác thứ tự cao hơn trên nhật ký mô phỏng của bạn.
   Trung ngữ翻译:阅读 Riedl 2025(arXiv:2510.05174)。 在你的模拟日志上实现高阶协同统计──没有ToM 提示条件下效果存在吗?

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Theory of Mind / 心智理论 | "Understanding others' minds" / "理解他人的心理" | The capacity to model another agent's beliefs. Graded by order (0, 1, 2+). / 建模另一个 Agent 信念的能力。按阶次分级（0, 1, 2+）。 |
| Sally-Anne test / Sally-Anne 测试 | "The false-belief test" / "错误信念测试" | 1985 developmental psychology; LLMs pass plain versions, fail complex ones. / 1985 年发展心理学；LLM 通过简单版本，复杂版本失败。 |
| First-order ToM / 一阶 ToM | "A believes X" / "A 相信 X" | Modeling one other's beliefs about facts. / 建模另一个关于事实的信念。 |
| Second-order ToM / 二阶 ToM | "A believes B believes X" / "A 相信 B 相信 X" | Recursive modeling one level deeper. / 递归建模更深一层。 |
| Identity-linked differentiation / 身份关联分化 | "Stable roles over time" / "稳定的角色" | Riedl's metric: roles persist, not random. / Riedl 的指标：角色持续而非随机。 |
| Goal-directed complementarity / 目标导向互补性 | "Disjoint actions" / "不交动作" | Agents target different subtasks, not the same one. / Agent 瞄准不同子任务，不是同一个。 |
| Higher-order synergy / 高阶协同 | "Group exceeds any subset" / "群体超越任何子集" | Riedl's statistical measure for real coordination. / Riedl 对真正协调的统计度量。 |
| Coordination illusion / 协调幻觉 | "It looks coordinated" / "看起来协调" | Prompt-dressed appearance of coordination without measurable signal. / 没有可测量信号的提示装饰的协调外观。 |

## Xem thêm 延伸阅读

- [Li et al. — Theory of Mind for Multi-Agent Collaboration via Large Language Models](https://arxiv.org/abs/2310.10701) ToM mới nổi trong các trò chơi hợp tác; các chế độ thất bại theo đường chân trời dài
- [Riedl — Emergent Coordination in Multi-Agent Language Models](https://arxiv.org/abs/2510.05174) đo lường quy mô dân số; ToM prompt là điều kiện chịu tải
- [Premack & Woodruff — Does the chimpanzee have a theory of mind?](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/does-the-chimpanzee-have-a-theory-of-mind/1E96B02CD9850E69AF20F81FA7EB3595) nguồn gốc năm 1978 của khái niệm ToM
- [Baron-Cohen, Leslie, Frith — Does the autistic child have a theory of mind?](https://doi.org/10.1016/0010-0277(85)90022-8)  bài báo Sally-Anne (1985)
