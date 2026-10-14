# Tự tinh chỉnh và phê bình: cải thiện sản lượng lặp đi lặp lại .

> Self-Refine (Madaan et al., 2023) sử dụng một LLM trong ba vai trò  tạo, phản hồi, tinh chỉnh  trong vòng lặp. Lợi nhuận trung bình: +20 tuyệt đối trên 7 nhiệm vụ. CRITIC (Gou et al., 2023) làm cứng bước phản hồi bằng cách định tuyến xác minh thông qua các công cụ bên ngoài. Năm 2026, mô hình này được chuyển giao trong mọi khung như "đánh giá-tích cực" (Anthropic) hoặc vòng lặp guardrail (OpenAI Agents SDK).

> **【中文解读】**Bản thân tinh chỉnh 让一个 LLM 扮演三个角色:生成、反、精炼,循环改进――7 个任务平均提升 20 个百分点――Critic 将验证步骤通过外部工具 (搜索,代码解释器,计算器)进行强化――2026 年, nó đã trở thành một tiêu chuẩn của mỗi khung Anthropic được gọi là "评估器-优化器",OpenAI Agents SDK được gọi là "输出护"―

> **【拓展：CRITIC → Claude Code 的自我修复】**Claude Code trong việc viết code sẽ tự động chạy test test certificate đây là sự thực hiện của mô hình CRITIC  khi test thất bại, nó dựa trên lỗi phản  sửa đổi code, cho đến khi test thông qua

>  **【前置】**必须先过:Phase 14·01(Agent Loop) vàPhase 14·03(Reflection) ――Tự tinh tế là phiên bản của " đơn次任务内" của Reflection (Tự tinh tế là phiên bản của " đơn次任务内" của Reflection)

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Mục tiêu học tập

- Ba lời nhắc của State Self-Refine (tạo, phản hồi, tinh chỉnh) và giải thích tại sao lịch sử quan trọng đối với lời nhắc tinh chỉnh.
  Trung ngữ翻译:陈述自炼的三个提示 (từ: tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh chỉnh, tự tinh luyện)
- Giải thích quan điểm quan trọng của CRITIC: LLM không đáng tin cậy trong việc tự xác minh mà không có nền tảng bên ngoài.
  Trung ngữ翻译:解释Critic 的关键洞察:没有外部定,LLM 在自我验证上不可靠──
- Thực hiện một vòng tự lọc stdlib với lịch sử và một xác minh bên ngoài tùy chọn.
  Trung ngữ翻译: Sử dụng các tiêu chuẩn để thực hiện tự tinh chỉnh vòng lặp với các hồ sơ lịch sử và các chứng minh bên ngoài có thể chọn.
- Bản đồ mô hình này cho dòng công việc "học toán-tích toán" của Anthropic và cửa sổ bảo vệ đầu ra của OpenAI Agents SDK.
  Trung ngữ翻译:将此模式映射到人类的"评估器-优化器"工作流和 OpenAI Agents SDK 的输出护──

## Vấn đề  vấn đề giới thiệu

Một đại lý tạo ra một câu trả lời gần như đúng. Có thể một dòng mã có lỗi tổng hợp. Có thể một bản tóm tắt quá dài. Có thể một kế hoạch bỏ lỡ một trường hợp cạnh. Bạn muốn là: đại lý chỉ trích đầu ra của riêng mình, sau đó sửa chữa nó.

> Trưởng lý  tạo ra một câu trả lời gần như chính xác. Có lẽ một dòng mã có sai định ngữ pháp. Có lẽ bản tóm tắt quá dài. Có lẽ một kế hoạch bỏ qua tình huống bên cạnh. Bạn muốn: Trưởng lý  chỉ trích bản sản xuất của mình, sau đó sửa lại nó.

Self-Refine cho thấy điều này hoạt động với một mô hình duy nhất, không có dữ liệu đào tạo, không có RL. Nhưng có một câu đố: LLM không tốt trong việc tự xác minh trên thực tế cứng. CRITIC đặt tên cho sự cố định  đường dẫn bước xác minh thông qua các công cụ bên ngoài (bảo sát, phiên dịch mã, máy tính toán, chạy thử nghiệm).

> Bản chất tự tinh chỉnh chứng minh rằng nó có thể làm việc với một mô hình đơn lẻ, không cần đào tạo dữ liệu, không cần RL. Nhưng có một rào cản: LLM trên thực tế tự kiểm chứng rất kém.

Cùng với hai bài báo này xác định mặc định 2026 cho cải tiến lặp đi lặp lại: tạo, xác minh (trên bên ngoài khi có thể), tinh chỉnh, dừng khi xác minh vượt qua.

> Hai bài viết này cùng nhau xác định mô hình cố định của cải tiến 2026: tạo, kiểm chứng (từ bên ngoài càng tốt)

> **【中文解读】**Tư tưởng cốt lõi của tự tinh chỉnh: một mô hình đóng vai trò là người tạo ra, phê bình, tinh luyện người có ba vai trò. Nhưng LLM trong thực tế khó khăn, tự kiểm chứng không thể tin cậy.

## Khái niệm cốt lõi

### Tự tinh chỉnh (Madaan et al., NeurIPS 2023)

Một LLM, ba vai trò:

> Một LLM, ba vai trò:

```
generate(task)            -> output_0                          # 生成初始输出
feedback(task, output_0)  -> critique_0                        # 自我批评
refine(task, output_0, critique_0, history) -> output_1       # 根据批评精炼
feedback(task, output_1)  -> critique_1                        # 再次批评
refine(task, output_1, critique_1, history) -> output_2       # 再次精炼
...
stop when feedback says "no issues" or budget exhausted.       # 停止条件
```

Chi tiết chính:`refine`thấy lịch sử đầy đủ  tất cả các kết quả và chỉ trích trước đây  vì vậy nó không lặp lại sai lầm.

>  **【类比】**Bản chất tự tinh chỉnh 像写论文的"自改稿"流程:第一稿(generate)→ 通读找问题(反)→ 按问题改第二稿(精细,但要看第一稿和批注改,否则会重复同样错误)→ 再找问题→再改──**关键**Mỗi lần tinh chỉnh phải đưa bản lịch sử và các tập hợp cùng nhau cho mô hình, nếu không mô hình sẽ "nghoất quên vấn đề đã được chỉ ra trên", rơi vào vòng lặp.

> ️ **【易错点】**常见 bug: chỉ đưa "上一轮输出" 给精炼, không có phản hồi.**后果**:fine 后的输出重新引入反指出的问题,陷入"指出问题→改→再指出→再改"的死循环──**一行修复**- Có thể là:`refine_prompt = task + output_0 + critique_0 + output_1 + critique_1 + ... + output_n` lịch sử phải toàn lượng truyền vào.

> 关键细节:`refine`能看到完整历史所有前来的输出和批评因此不会重复错误──论文对此进行消融实验:删除历史记录后质量急剧下降──

Tiêu đề: +20 cải thiện tuyệt đối trung bình trong 7 nhiệm vụ ( toán học, mã, viết tắt, đối thoại) bao gồm GPT-4. Không có đào tạo, không có công cụ bên ngoài, mô hình đơn.

> 核心数据: trên 7 nhiệm vụ (mathematics, code, shorthand, dialog) trung bình tuyệt đối tăng 20 điểm phần trăm, bao gồm GPT-4── không cần đào tạo, không cần các công cụ bên ngoài, mô hình đơn lẻ──

### CRITIC (Gou et al., arXiv:2305.11738, v4 Feb 2024)

Điểm yếu của Self-Refine: bước phản hồi là một LLM tự ghi điểm. Đối với các tuyên bố thực tế, điều này không đáng tin cậy (một ảo giác thường trông thuyết phục cho mô hình đã tạo ra nó). CRITIC thay thế `feedback(task, output)`với `verify(task, output, tools)`nơi `tools`bao gồm:

> Phạm vi yếu của tự tinh chỉnh: phản bước là LLM 给自己评分── đối với tuyên bố thực tế, đây là không đáng tin cậy.`verify(task, output, tools)`替代 `feedback(task, output)`, trong số đó `tools`Bao gồm:

- Một công cụ tìm kiếm cho các tuyên bố thực tế.
  Trung ngữ翻译:用于事实性声明的搜索引擎.
- Một phiên dịch mã cho chính xác mã.
  Trung ngữ翻译:用于代码正确性的代码解释器──
- Máy tính toán toán.
  Trung ngữ翻译:用于算术的计算器──
- Các bộ xác minh cụ thể về miền (thử nghiệm đơn vị, kiểm tra loại, lăng).
  Trung文翻译: lĩnh vực xác định kiểm chứng器 (单元测试,类型检查器,代码检查器)

Người xác minh tạo ra một bài phê bình có cấu trúc dựa trên kết quả công cụ.

> 验证器 tạo ra đánh giá cấu trúc dựa trên kết quả của công cụ.

Tiêu đề: CRITIC vượt trội hơn Auto-Refine trong các nhiệm vụ thực tế vì sự chỉ trích được đặt nền.

> 🤔 **【困惑】**Q: 既然 CRITIC 比自精炼强,为什么不全部使用CritIC? A: Vì CRITIC phụ thuộc vào các công cụ bên ngoài(搜索、代码解释器、单元测试) 创意写作、邮件色**事实类用 CRITIC，创造类用 Self-Refine**

> 核心数据:CRITIC 在事实性任务上超越自我精炼,因为批评是有依据的──在没有外部验证器的任务上(创意写作、格式化),CRITIC 退化为自我精炼──

### Điều kiện dừng

Hai hình dạng phổ biến:

> 两种常见形式:

1. **Verifier passes.**Thử nghiệm bên ngoài trả lại thành công. Tích thích khi có (thử nghiệm đơn vị, kiểm tra kiểu, khẳng định tháp).
   Trung ngữ翻译:**验证器通过。**外部测试返回成功──在可用时优先单元测试、类型检查器、护断言)──
2. **No feedback issued.**Mô hình nói "tạo ra tốt". Thô hơn nhưng không đáng tin cậy; cặp với một nắp lặp tối đa.
   Trung ngữ翻译:**无反馈发出。**模型说"输出没问题"──更便宜但不可靠;配合最大代次数上限──

2026 mặc định: kết hợp chúng. "Hãy dừng nếu xác minh vượt qua OR mô hình nói OK AND lặp >= 2 hoặc lặp >= max_iterations".

> 2026 年默认做法:组合使用──"Nếu các thiết bị kiểm tra thông qua, hoặc mô hình nói không có vấn đề và số lần >= 2, hoặc số lần >= tối đa, thì dừng lại──"

### Tỷ lệ của các loại hình:

Bài đăng của Anthropic tháng 12 năm 2024 đề cập đến điều này như là một trong năm mô hình quy trình làm việc.

> Bài viết của Anthropic 2024 năm 12 tháng sẽ được đặt tên là một trong năm 5 phong trào làm việc.

- Đánh giá: đánh giá kết quả và tạo ra một lời chỉ trích.
  Trung文翻译:评估器:对输出评分并产生批评.
- Optimizer: sửa đổi sản xuất do sự chỉ trích.
  Trung文翻译:优化器:根据批评修改输出。

Loop cho đến khi đánh giá vượt qua. Đây là tự tinh chỉnh / CRITIC trong khung Anthropic. Chi tiết kỹ thuật quan trọng Anthropic thêm: các yêu cầu đánh giá và tối ưu hóa nên khác nhau đáng kể để mô hình không chỉ được dán bằng cao su.

> 循环直到评估器通过──这是人类 框架下的自我精炼/CRITIC──人类 添加的关键工程细节:评估器和优化器提示应该有实质性差异,免模型只是皮图章──

### Các cửa sổ bảo vệ đầu ra của OpenAI Agents SDK

OpenAI Agents SDK gửi mô hình này như là "các cửa sổ sản xuất".`OutputGuardrailTripwireTriggered`Các guardrails có thể gọi công cụ (như CRITIC) hoặc là các chức năng thuần túy (như tự tinh chế).

> OpenAI Agents SDK sẽ sử dụng mô hình này như "输出护" cung cấp.`OutputGuardrailTripwireTriggered`),输出被拒绝,Agent có thể thử lại.

### 2026 bẫy

- **Rubber-stamp loops.**Một mô hình tương tự làm việc tạo ra và phê bình với cùng một kiểu cách nhanh nhẹn hội tụ với "có vẻ tốt với tôi". Sử dụng các mô hình khác nhau về cấu trúc, hoặc một mô hình rẻ hơn cho phê bình.
  Trung ngữ翻译:**橡皮图章循环。**Một mô hình cũng sử dụng cùng một kiểu gợi ý để tạo ra và đánh giá nhận được đến "nhìn không sai"―― sử dụng các gợi ý khác nhau về cấu trúc, hoặc sử dụng mô hình nhỏ hơn để đánh giá lại.
- **Over-refinement.**Mỗi lần thông qua tinh chỉnh thêm độ trễ và token. Ngân sách 1-3 thông qua; sau đó, leo thang đến đánh giá của con người.
  Trung ngữ翻译:**过度精炼。**Mỗi lần luyện tập tăng trì hoãn và token  ngân sách 1-3 vòng; sau đó nâng cấp cho kiểm tra nhân tạo 
- **CRITIC on trivial tasks.**Nếu không có xác minh bên ngoài, CRITIC biến mất thành tự tinh chỉnh; đừng trả thời gian trễ cho xác minh stub.
  Trung ngữ翻译:**在简单任务上使用 CRITIC。**Nếu không có thiết bị kiểm tra bên ngoài, CRITIC 退化为自炼; đừng trả cho thiết bị kiểm tra trả giá muộn.

## Hãy xây dựng nó.
```figure
self-refine
```

## Hãy xây dựng nó

`code/main.py`thực hiện tự tinh chỉnh và CRITIC trên một nhiệm vụ đồ chơi: tạo ra một danh sách đạn ngắn cho một chủ đề.

> `code/main.py`Trong một nhiệm vụ chơi game thực hiện tự tinh chỉnh và CRITIC: cho các chủ đề tạo ra danh sách ngắn.

Các thành phần:

> 组件:

- `generate` Nhà sản xuất kịch bản.
  Trung ngữ翻译:`generate`脚本生成器──
- `feedback` Tự phê bình theo kiểu LLM.
  Trung ngữ翻译:`feedback`LLM 风格 tự phê bình.
- `verify_external` Kiểm tra cơ bản theo kiểu CRITIC.
  Trung ngữ翻译:`verify_external`CRITIC 风格 定验器──
- `refine` viết lại đầu ra với lịch sử.
  Trung ngữ翻译:`refine`根据历史重写输出──
- Điều kiện dừng  kiểm chứng vượt qua hoặc tối đa 4 lần lặp lại.
  Trung文翻译:停止条件验证器通过或最多 4 次代。

Đi đi.

> 运行:

```
python3 code/main.py
```

So sánh các tự tinh chỉnh so với CRITIC chạy. CRITIC bắt được một lỗi thực tế tự tinh chỉnh bị bỏ lỡ bởi vì kiểm tra bên ngoài đã đặt nền tự phê bình không.

> So sánh Tự tinh tế và Tầm quan trọng 运行。Tầm quan trọng  bắt được Tự tinh tế 遗漏 thực tế sai lầm, vì các chứng minh bên ngoài có tự phê bình không có 定依据。

## Hãy sử dụng nó để thực hiện

Phân tích đánh giá của Anthropic là mô hình này trong ngôn ngữ thân thiện với Claude. Các cửa sổ bảo vệ đầu ra của OpenAI Agents SDK có hình CRITIC (bên bảo vệ có thể gọi công cụ). LangGraph gửi một nút phản xạ đọc như tự tinh chỉnh. Sử dụng máy tính Gemini 2.5 của Google thêm một đánh giá an toàn từng bước là một biến thể CRITIC: mọi hành động được xác minh trước khi tham gia.

> Antropic's assessment-optimizer is using this model of Claude Friendly Language Expression.  Xuất khẩu của OpenAI Agents SDK                                                                                                                                                                                                                                              

## Chuyển nó đi.

`outputs/skill-refine-loop.md`cấu hình một vòng lặp đánh giá-optimizer cho hình dạng nhiệm vụ, tính sẵn có của xác minh và ngân sách lặp lại. Phát ra yêu cầu cho máy phát điện, đánh giá/ xác minh và tối ưu hóa, cộng với chính sách dừng.

> `outputs/skill-refine-loop.md`Theo hình dạng nhiệm vụ, tính khả dụng của bộ chứng nhận và quy trình định định kỳ định kỳ định kỳ ngân sách, vòng lặp tối ưu hóa.

## Tập luyện bài tập

1. Cứ chạy đồ chơi với max_iterations=1. CRITIC vẫn giúp không?
   中文翻译:用 max_iterations=1 运行――CRITIC  vẫn có ích không?
2. Thay thế xác minh bên ngoài bằng một xác minh ồn ào (những kết quả sai 30% ngẫu nhiên).
   Trung ngữ翻译:将外部验证器替换为杂的版本(30% 误报) ――循环会做什么?
3. Thực hiện một biến thể "tít xét máy phát trên các mô hình khác nhau": mô hình lớn tạo ra, mô hình nhỏ chỉ trích.
   Trung文翻译:实现"不同模型的生成-批评"变体:大模型生成,小模型批评――比同模型更好吗?
4. Đọc phần 3 CRITIC (arXiv:2305.11738 v4). Hãy nêu tên ba loại công cụ xác minh và đưa ra một ví dụ cho mỗi loại.
   Trung ngữ翻译:阅读CRITIC 第 3 节。说出三种验证工具类别并各举一例。
5. Bản đồ OpenAI Agents SDK `output_guardrails`Điều gì SDK sai và điều gì đúng?
   中文翻译:将 OpenAI Agents SDK 的 `output_guardrails`映射到Critic's verifier角色──SDK 哪里做得好,哪里不够?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Self-Refine | "LLM that fixes itself" / "自我修复的 LLM" | Generate -> feedback -> refine loop in one model, with history / 一个模型内的生成→反馈→精炼循环，带历史记录 |
| CRITIC | "Tool-grounded verification" / "工具锚定验证" | Replace feedback with an external verifier (search, code, calc, tests) / 用外部验证器替代反馈 |
| Evaluator-Optimizer | "Anthropic workflow pattern" / "Anthropic 工作流模式" | Two roles — evaluator scores, optimizer revises — looped to convergence / 两个角色——评估器评分、优化器修改——循环到收敛 |
| Output guardrail | "Post-hoc check" / "事后检查" | OpenAI Agents SDK validator that runs after an agent produces output / Agent 输出后运行的验证器 |
| Verify step | "Critique phase" / "批评阶段" | The load-bearing decision: grounded or self-rated / 核心决策：基于外部工具还是自我评价 |
| Refine history | "What the model already tried" / "模型已尝试的内容" | Prior outputs + critiques prepended to refine prompt; drop and quality collapses / 先前输出+批评前置到精炼提示；去掉则质量崩溃 |
| Rubber-stamp loop | "Self-agreement failure" / "自我认同失败" | Same-prompt critique returns "looks good"; fix with structurally different prompts / 相同提示批评返回"看起来不错"；用结构性不同的提示修复 |
| Stop condition | "Convergence test" / "收敛测试" | Verifier passes OR no feedback AND iteration cap; never single-condition / 验证器通过或无反馈且达到迭代上限；永不使用单一条件 |

## Xem thêm 延伸阅读

- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) giấy phép
  Trung văn翻译:Tự tinh chỉnh 经典论文自我精炼代改进。
- [Gou et al., CRITIC (arXiv:2305.11738)](https://arxiv.org/abs/2305.11738) Kiểm tra dựa trên công cụ
  Trung文翻译:CRITIC工具定验证──
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) mô hình lưu lượng công việc đánh giá- tối ưu hóa
  Trung ngữ翻译:Anthropic 关于构建有效代理的指导评估器-优化器工作流模式──
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) Vệ chắn đầu ra như các bộ xác minh hình CRITIC
  Trung文翻译:OpenAI Agents SDK 文档输出护作为Critic 形式的验证器──
