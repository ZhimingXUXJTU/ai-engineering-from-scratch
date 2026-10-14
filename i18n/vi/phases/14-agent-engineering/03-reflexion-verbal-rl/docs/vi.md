# Tâm lý: Học tập tăng cường bằng lời nói ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi ơi

> RL dựa trên gradient cần hàng ngàn thử nghiệm và một cluster GPU để sửa đổi chế độ thất bại. Reflection (Shinn et al., NeurIPS 2023) làm điều đó bằng ngôn ngữ tự nhiên: sau mỗi thử nghiệm thất bại, đại lý viết một phản xạ, lưu trữ nó trong bộ nhớ tập thể, và điều kiện thử nghiệm tiếp theo trên bộ nhớ đó. Đây là mô hình đằng sau tính toán thời gian ngủ của Letta, học tập của Claude Code về CLAUDE.md, và quy tắc học tập của Pro-workflow.

> **【中文解读】**基于梯度的RL 需要数千次试验和GPU集群──Reflection Using Natural Language to realize self improvement: Mỗi lần thất bại,Agent 写一段反思存入情景记忆,次次尝试时参考这些记忆──Đây chính là mô hình đằng sau bộ máy tính thời gian ngủ của Letta──Claude Code của CLAUDE.md 学习机制──

> **【拓展：Reflexion → Claude Code 的自我学习】**Cơ chế của Claude Code là một biến thể của Reflection.Agent trong quá trình làm việc tích lũy kinh nghiệm, lưu trữ cho các tập tin quy tắc, tiếp tục tự động tải lên. Đây cũng là cách thực hiện phổ biến nhất trong môi trường sản xuất.

>  **【前置】**本节依赖:Phase 14·01(Agent Loop)你必须已经能够跑通一个 ReAct 循环,因为 Reflection 内部的 Actor 内部就是一个 ReAct loop;以及Phase 14·02(ReWOO) 理解"试验/轨迹"的概念──如果你分不清"一次试验"和"一个步骤",先回去补补 ReAct──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 02 (ReWOO) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 02 (ReWOO)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Mục tiêu học tập

- Hãy nêu tên ba thành phần của Nhận thức (Nhân viên, Thử nghiệm, Tự Nhận thức) và vai trò của trí nhớ tập thể.
  Trung文翻译:说出 Reflection 的三个组件 (Hành động viên, đánh giá, phản ánh bản thân)
- Thực hiện một vòng lặp phản xạ stdlib với đánh giá nhị phân, bộ đệm phản xạ và các nỗ lực tái tạo mới.
  Trung文翻译:用标准库实现反思循环,包含二元评估器、反思缓冲区和全新重试──
- Chọn giữa các nguồn phản hồi quy mô, heuristic và tự đánh giá cho một nhiệm vụ nhất định.
  Trung ngữ翻译:为给定任务选择标量、启发式或自评估反源──
- Giải thích tại sao việc tăng cường bằng lời nói bắt được những lỗi mà RL dựa trên gradient cần hàng ngàn thử nghiệm để sửa chữa.
  Trung ngữ翻译: giải thích tại sao ngôn ngữ tăng cường có thể bắt được RL dựa trên thang độ 需要数千次试验才能修复错误――

## Vấn đề  vấn đề giới thiệu

Một đại lý thất bại trong một nhiệm vụ. Trong RL tiêu chuẩn bạn sẽ chạy hàng ngàn thử nghiệm hơn, tính toán gradient, cập nhật trọng lượng.

> Trưởng lý không thành công trong một nhiệm vụ. Trong RL tiêu chuẩn, bạn cần phải chạy hàng ngàn lần thử nghiệm hơn, tính toán thang độ, nâng cấp trọng lượng, tốn kém, chậm, và hầu hết các công ty sản xuất không có ngân sách đào tạo dành cho mỗi lần thất bại.

Nhắc nhã (Shinn et al., arXiv:2303.11366) đặt ra một câu hỏi khác: nếu đại lý chỉ nghĩ về lý do tại sao nó thất bại và thử lại với ý tưởng đó trong lời nhắc nhở của nó? Không cập nhật trọng lượng. Không gradient. Chỉ là ngôn ngữ tự nhiên được lưu trữ giữa các thử nghiệm.

> Nhắc nhã: Shinn et al., arXiv:2303.11366) đưa ra một vấn đề khác: Nếu Đại lý chỉ nghĩ về nguyên nhân thất bại, sau đó tham gia vào ý tưởng này trong lời khuyên của lần thử tiếp theo? Không có quyền tải trọng, không có thang, chỉ là thử nghiệm trong lưu trữ ngôn ngữ tự nhiên.

Kết quả: trên ALFWorld nó đánh bại ReAct và các đường cơ sở không được điều chỉnh tốt khác. trên HotpotQA nó cải thiện so với ReAct. Trên việc tạo mã (HumanEval / MBPP) nó thiết lập trạng thái nghệ thuật tại thời điểm đó. Tất cả mà không có một bước nghiêng duy nhất.

> Kết quả: trong ALFWorld 上 nó đánh bại ReAct 和其他非微调基线. Trong HotpotQA 上它 vượt qua ReAct. Trong mã tạo (HumanEval/MBPP) trên nó đạt được mức tốt nhất của thời điểm đó.

## Khái niệm cốt lõi

### Ba thành phần

```
Actor         : generates a trajectory (ReAct-style loop)     # 执行器：生成行动轨迹
Evaluator     : scores the trajectory — binary, heuristic, or self-eval  # 评估器：评分
Self-Reflector: writes a natural-language reflection on the failure      # 自我反思器：写反思
```

Thêm một cấu trúc dữ liệu:

```
Episodic memory: list of prior reflections, prepended to the next trial's prompt  # 情景记忆
```

Một thử nghiệm chạy cho diễn viên. Thử nghiệm đánh giá nó. Nếu điểm số thấp, Self-Reflector tạo ra một phản xạ ("Tôi chọn công cụ sai vì tôi đọc sai câu hỏi như hỏi về X khi nó hỏi về Y").

>  **【类比】**Nhận xét 像考试做错题后的"错题本"机制:你做错一道题(Actor 失败)→ 拿到对错信号(Evaluator 评分)→ 写下"我为什么错了"(Self-Reflector 写反思)→ 下次考前翻错题本(情景记忆前置到提示) ・・・ 下次重复同类题,错的概率就低了──关键是错题本(反思用自然语言写,不需要重训模型权──

> Một lần thử nghiệm chạy hành Đạo diễn. Một lần đánh giá được đánh giá. Nếu số lượng phân tích thấp, Người phản ánh bản thân sẽ tạo ra một đoạn phản chiếu. Tôi chọn một công cụ sai lầm, vì tôi đã hiểu sai vấn đề để hỏi X, thực sự hỏi là Y.

### Ba loại đánh giá

1. **Scalar** tín hiệu nhị phân bên ngoài. ALFWorld thành công hoặc thất bại. HumanEval thử nghiệm vượt qua hoặc thất bại. đơn giản nhất, tín hiệu cao nhất.
   Trung ngữ翻译:**标量** bên ngoài 2元 tín hiệu。ALFWorld thành công hoặc thất bại。HumanEval 测试通过或不通过。最简单,信号最强。
2. **Heuristic** dấu hiệu thất bại được xác định trước. "Nếu tác nhân tạo ra hành động tương tự hai lần liên tiếp, đánh dấu là bị mắc kẹt". "Nếu quỹ đạo vượt quá 50 bước, đánh dấu là không hiệu quả".
   Trung ngữ翻译:**启发式**预定义的失败签名──"Nếu đại lý 连续两次产生相同行动,标记为卡住──""Nếu轨迹超过50步,标记为低效──"
3. **Self-evaluated** LLM ghi điểm quỹ đạo của riêng mình. Cần khi không có sự thật cơ bản có sẵn. tín hiệu yếu hơn; kết hợp tốt với xác minh cơ bản bằng công cụ (Dạy 05  CRITIC).
   Trung ngữ翻译:**自评估**LLM đối với quỹ đạo của mình đánh giá.

Dự định 2026 là một hỗn hợp: scalar khi có sẵn, tự-eval khi không có, heuristics như đường ray an toàn.

> ️ **【易错点】**三种评估器选错会出大问题: Trong nhiệm vụ viết sáng tạo như "không có tiêu chuẩn trả lời" trên một đánh giá quy mô cứng lên như keyword匹配), sẽ tiếp tục tạo ra " failed signal "→ Đại lý 拼命反思 → Nhưng反思本身没有意义 → 浪费代币直到耗尽预算。**后果**: vòng quay chuyển đổi tiền đốt:**一行修复**: trước sử dụng 5 条 样本手工验证"失败信号是否能区分好坏",区分不开就降级为自衡 + 代上限──

> Phương pháp cố định năm 2026 là sử dụng hỗn hợp: có tiêu chuẩn khi sử dụng tiêu chuẩn, không có thời gian tự đánh giá, bắt đầu như một bảo mật.

### Tại sao điều này nói chung

Reflection không phải là một thuật toán mới mà là một mô hình có tên.

> Nhận xét thay vì là một thuật toán mới, không giống như một mô hình đặt tên.

- Letta's sleep-time computation (Lớp 08): một đại lý riêng tư suy nghĩ về các cuộc trò chuyện trong quá khứ và viết cho các khối bộ nhớ.
  Trung ngữ翻译:Letta's sleep-time computation (第 8 课): Một đặc vụ độc lập phản chiếu quá khứ của cuộc đối thoại并写入记忆块。
- Claude Code `CLAUDE.md`/ " lưu trí nhớ" mô hình: phản ánh được ghi lại như những bài học, prepended cho các buổi tiếp theo.
  Trung ngữ翻译:Claude Code của `CLAUDE.md`/"保存记忆"模式:反思被捕获为学习经验,前置到未来会话.
- Pro-workflow `/learn-rule`lệnh: các sửa đổi được ghi lại như là các quy tắc rõ ràng.
  Trung ngữ翻译:pro-workflow của `/learn-rule`命令:纠正被捕为显式规则──
- Các nút phản xạ của LangGraph: một nút ghi điểm đầu ra và đường dẫn để tinh chỉnh nếu cần thiết.
  Trung ngữ翻译:LangGraph的反思节点:一个评分输出并在需要时路由到精炼的节点──

Tất cả đều bắt nguồn từ cùng một cái nhìn sâu sắc: ngôn ngữ tự nhiên là một phương tiện đủ phong phú để mang "những gì tôi đã học từ thất bại" giữa các cuộc chạy.

> Tất cả đều bắt nguồn từ cùng một ý kiến: ngôn ngữ tự nhiên là một phương tiện đủ phong phú, có thể truyền tải giữa các hành động"Tôi đã học được gì từ thất bại" (I learned from failure in the course of life).

> **【拓展：Reflexion → 生产环境的自我修复】**几乎所有生产环境的"自我修复"Agent 都使用 Reflexion 变体:Letta's sleep-time computation 异步反思、Claude Code 的 CLAUDE.md 存储学习经验、Langgraph 的反思节点──核心洞察相同:自然语言足够承载"从失败中学到了什么"──

### Khi nó hoạt động và khi nó không hoạt động

Nhận thức hoạt động khi:

> Nhận xét trong các trường hợp sau đây có hiệu lực:

- Có một tín hiệu thất bại rõ ràng (trình thử thất bại, lỗi công cụ, câu trả lời sai).
  Trung ngữ翻译:有明确的失败信号(测试失败、工具错误、错误答案)
- Nhóm nhiệm vụ có thể tái tạo (những câu hỏi tương tự có thể được đặt lại).
  Trung ngữ翻译:任务类别可重现(可以再次提出同类问题)。
- Sự suy nghĩ có chỗ để cải thiện quỹ đạo (khuế hoạch hành động đủ).
  Trung ngữ翻译:反思有改进轨迹的空间 (反思有改进轨迹的空间)

Nhắc nhã không giúp ích khi:

> Nhận xét trong các tình huống sau đây không giúp ích:

- Đặc vụ đã thành công trong lần thử đầu tiên.
  Trung文翻译:Công viên 首次尝试即成功。
- Sự cố là bên ngoài (mạng không hoạt động, công cụ bị hỏng)  phản ánh về "mạng đã bị hỏng" không giúp chạy trong tương lai.
  Trung ngữ翻译:失败是外部的网络中断、工具损坏) 对"网络中断"的反思对未来运行无助.
- Sự phản ánh biến thành mê tín  lưu trữ một câu chuyện về một lần chạy ván.
  Trung ngữ翻译:反思变成迷信存储关于一次性不稳运行的叙述──

2026: mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ mớ m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m m

> 🤔 **【困惑】**Q: Reflection 真的能"等价于"RL 吗?RL 改是模型权重,Reflection 只改变快速,机制完全不同── A: 不能等价──论文标题"Verbal RL"是修辞而非数学等价──Reflection 的优势是**样本效率极高**Với 3-5 lần suy nghĩ, bạn có thể sửa chữa một mô hình thất bại, trong khi RL cần hàng ngàn lần nâng cấp;**反思不会持久**Đến trọng lượng mô hình, mỗi lần mới được học tập. Vì vậy, suy nghĩ phù hợp với "không có đào tạo ngân sách sản xuất trường hợp",RL phù hợp với "làm việc đào tạo ngoại tuyến có thể nản xuất mô hình nhỏ".

> Phạm cảnh năm 2026: kỷ niệm bị hư hỏng. 反思不断积累,部分已过时或错误.

## Hãy xây dựng nó.
```figure
react-trace
```

## Hãy xây dựng nó

`code/main.py`thực hiện Nhận thức trên một trò chơi: tạo ra một danh sách 3 yếu tố tổng cộng đến một mục tiêu.

> `code/main.py`Trong một trò chơi  Thử nghiệm: tạo ra một danh sách 3 nguyên tố và có giá trị mục tiêu  Đạo diễn  phát hành danh sách ứng cử viên  đánh giá  kiểm tra tổng cộng  Tự phản ánh  viết một dòng về việc chẩn đoán vấn đề xuất hiện 

Các thành phần:

> 组件:

- `Actor` một chính sách được viết kịch bản cải thiện khi nó thấy phản ánh.
  Trung ngữ翻译:`Actor` Xem phản hồi  sẽ cải thiện kịch bản chiến lược.
- `Evaluator.binary()` vượt qua/không đạt được số tiền mục tiêu.
  Trung ngữ翻译:`Evaluator.binary()` đối với mục tiêu tổng cộng của thông qua / thất bại phán quyết.
- `SelfReflector` tạo ra một chẩn đoán một dòng của sự thất bại.
  Trung ngữ翻译:`SelfReflector` tạo một dòng thất bại chẩn đoán.
- `EpisodicMemory` một danh sách giới hạn với ngữ nghĩa TTL.
  Trung ngữ翻译:`EpisodicMemory`带 TTL 语义的有界列表──

Đi đi.

> 运行:

```
python3 code/main.py
```

Các dấu vết cho thấy ba thử nghiệm. thử nghiệm 1 thất bại, một phản xạ được lưu trữ, thử nghiệm 2 thấy phản xạ và cải thiện nhưng vẫn thất bại, thử nghiệm 3 thành công. So sánh với một chạy cơ bản (không phản xạ)  nó vẫn bị mắc kẹt trong câu trả lời thử nghiệm 1.

> 轨迹显示三次试验──试验1 失败,存储反思,试验2 看到反思并改进但仍失败,试验3 成功──与基线运行(无反思) đối với它停留在试验1的答案──

## Hãy sử dụng nó để thực hiện

LangGraph đưa phản xạ như một mô hình nút.`/memory`lệnh và pro-workflow của `/learn-rule`Letta tính toán thời gian ngủ chạy Self-Reflector trong thời gian ngừng hoạt động để đại lý chính vẫn bị ràng buộc bởi độ trễ. OpenAI Agents SDK không gửi Reflexion trực tiếp; bạn xây dựng nó bằng Guardrail tùy chỉnh từ chối quỹ đạo theo điểm số và bộ nhớ`Session`là tồn tại qua các đường đua.

> LangGraph sẽ phản ánh như mô hình các nốt cung cấp.`/memory`命令和 pro-workflow của`/learn-rule`Để làm cho các hoạt động của mình phản xạ, làm cho chủ nhân giữ được độ chậm lại. OpenAI Agents SDK không trực tiếp cung cấp phản xạ. Bạn sử dụng tự xác định Guardrail (đơn tỷ lệ từ chối quỹ đạo) và trong quá trình vận hành.`Session`Để xây dựng nó.

## Chuyển nó đi.

`outputs/skill-reflexion-buffer.md`tạo và duy trì một bộ đệm tập thể với chụp phản xạ, TTL và giảm trùng lặp. Với một lớp công việc và thất bại, nó phát ra một phản xạ thực sự giúp thử nghiệm tiếp theo (không phải là một khái quát "sự cẩn thận hơn").

> `outputs/skill-reflexion-buffer.md`Tạo và duy trì một vùng chống lại phản ứng của việc bắt đầu, TTL và giảm cân.

## Tập luyện bài tập

1. Chuyển từ đánh giá nhị phân sang đánh giá thang đo trả lại một số lượng đường cách (cách nào xa từ mục tiêu).
   Trung ngữ翻译:将评估器将二元切换为返回距离量量标量评估器──收更快吗?
2. Thêm một TTL 10 thử nghiệm vào những suy nghĩ.
   Đưa lại phản ánh 10 lần thử nghiệm TTL.
3. Thực hiện đánh giá học học: đánh dấu thử nghiệm như bị mắc kẹt nếu cùng một hành động lặp lại.
   Trung ngữ翻译:实现启发式评估器:重复相同行动时标记为卡住.
4. Chạy Reflection với một diễn viên đối thủ mà bỏ qua phản xạ.
   Trung ngữ翻译:用忽略反思的对抗性 运行反思.
5. Đọc phần 4 của bài báo Reflexon trên AlfWorld. Tái tạo lại sự cải thiện tỷ lệ thành công 130% theo khái niệm: điểm chính là delta vs vanilla ReAct?
   Trung ngữ翻译:阅读 suy nghĩ 论文第4节关于AlfWorld的内容──概念重现 130% thành công率改进:相比原始 ReAct's key difference is what?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Reflexion | "Self-correction" / "自我纠错" | Shinn et al. 2023 — Actor, Evaluator, Self-Reflector plus episodic memory / Shinn 等人 2023——Actor、Evaluator、Self-Reflector 加情景记忆 |
| Verbal reinforcement | "Learning without gradients" / "无梯度学习" | Natural-language reflection prepended to the next trial's prompt / 自然语言反思前置到下一次试验的提示 |
| Episodic memory | "Per-task reflections" / "按任务的反思" | Bounded buffer of prior reflections for one task class / 一个任务类别的先前反思有界缓冲区 |
| Scalar evaluator | "Binary success signal" / "二元成功信号" | Pass/fail or numeric score from ground truth / 来自真值的通过/失败或数值评分 |
| Heuristic evaluator | "Pattern-based detector" / "基于模式的检测器" | Predefined failure signatures (e.g. stuck-loop, too-many-steps) / 预定义的失败签名（如卡住循环、步数过多） |
| Self-evaluator | "LLM-as-judge on own trace" / "LLM 评价自身轨迹" | Lower-signal fallback when no ground truth — pair with tool-grounded verification / 无真值时的低信号后备——与工具锚定验证配合 |
| Memory rot | "Stale reflections" / "过时反思" | Episodic buffer fills with obsolete entries; fix with compaction/TTL / 情景缓冲区填满过时条目；用压缩/TTL 修复 |
| Sleep-time reflection | "Async self-reflection" / "异步自我反思" | Run Self-Reflector off the hot path so primary agent stays fast / 在非关键路径上运行 Self-Reflector 使主 Agent 保持快速 |

## Xem thêm 延伸阅读

- [Shinn et al., Reflexion: Language Agents with Verbal Reinforcement Learning (arXiv:2303.11366)](https://arxiv.org/abs/2303.11366) giấy phép
  Trung文翻译:Reflection 经典论文语言 Agent 的语言强化学习。
- [Letta, Sleep-time Compute](https://www.letta.com/blog/sleep-time-compute) phản xạ không đồng bộ trong sản xuất
  Trung ngữ翻译:Letta 关于生产环境中异步反思的博客文章。
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) quản lý bộ đệm tập thể trong bối cảnh
  Trung văn翻译:Anthropic 关于 AI Agent 上下文工程的文章将情景缓冲区作为上下文的一部分管理──
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) mô hình nút phản xạ
  Trung文翻译:LangGraph 概览反思节点模式。
