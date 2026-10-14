# Cây của suy nghĩ và LATS: Tìm kiếm cố ý

> Một đường đi chuỗi suy nghĩ duy nhất không có chỗ để quay trở lại. ToT (Yao et al., 2023) biến suy luận thành một cây với đánh giá tự trị trên mỗi nút. LATS (Zhou et al., 2024) thống nhất ToT với ReAct và Reflexion trong Monte Carlo Tree Search. Game of 24 tăng từ 4% (CoT) lên 74% (ToT); LATS đạt 92,7% pass@1 trên HumanEval.

> **【中文解读】**单条思维链没有回溯空间――TóT sẽ được đưa ra thay đổi cho cấu trúc cây có đánh giá tự trị,Túyển đổi từ 24 từ 4% 升级 lên 74%―LATS 统一了TóT、ReAct 和 Reflection, sử dụng tìm kiếm cây 蒙特卡洛实现,HumanEval 达到 92.7% pass@1──

> **【拓展：ToT/LATS → OpenAI o1/o3 的推理搜索】**"Thử suy nghĩ sâu sắc" của OpenAI o1/o3 系列 mô hình bản chất là tìm kiếm trong không gian suy nghĩ để khám phá nhiều đường, đánh giá và chọn tốt nhất.

>  **【前置】**本节硬核,前置必须扎实:Phase 14·01(ReAct) LATS 内部就是 ReAct;Phase 14·03(Reflection) LATS của Self-Reflector 复用 Reflection 机制;以及 MCTS(蒙特卡洛树搜索)基础知识`Q(s,a) + c*sqrt(lnN/N)`Hai phần khác nhau đại diện cho cái gì, trước tiên hãy xem AlphaGo bài báo hoặc bài giảng.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 03 (Reflexion) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 03 (Reflexion)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Lý luận khung như tìm kiếm: nút là "lưu ý", cạnh là "lớn rộng", giá trị là "cảm ơn".
  Trung ngữ翻译:将推理框架为搜索:节点是"思考",边是"扩展",值是"有多大前景"──
- Thực hiện tìm kiếm cây BFS kiểu stdlib ToT với điểm tự đánh giá.
  Trung文翻译:用标准库实现 ToT 风格的 BFS 树搜索,带自评估评分──
- Tăng đến một vòng lặp LATS MCTS đồ chơi với chọn / mở rộng / mô phỏng / đẩy ngược.
  Trung文翻译:扩展为玩具 LATS MCTS 循环,包含选择/扩展/模拟/反向传播──
- Quyết định khi nào tìm kiếm có giá trị nhân mã (Game of 24, code generation) và khi nào một quỹ đạo đơn giản là đủ (Question & Answer đơn giản).
  Trung文翻译:决定何时搜索值得付出代币 倍增成本(Lát bài 24、代码生成),何时单轨迹足够(简单问答) 』

## Vấn đề  vấn đề giới thiệu

Đường dây tư duy là một bước đi tuyến tính. Nếu bước đầu tiên sai, mỗi bước tiếp theo hoạt động trên một giả định xấu. Trong Game of 24 (tiêu dùng bốn chữ số với + − × ÷ để tạo ra 24), GPT-4 CoT đạt độ chính xác 4% . Mô hình chọn sự phản ánh sai sớm và không thể phục hồi.

> 思维链是线性推进的──如果第一步错了,后续每一步都基于错误假设── 在24的游戏中,GPT-4 CoT chỉ có 4% 准确率──模型在早期选错表达后无法恢复──

Điều cần thiết để suy luận là khả năng đề xuất nhiều ứng cử viên, đánh giá họ, chọn những ứng cử viên hứa hẹn và quay lại khi những kết cục chốt xuất hiện.

> Ưu điểm cần thiết là: đưa ra nhiều ứng cử viên, đánh giá chúng, chọn có triển vọng, cùng thời gian trở lại.

> **【中文解读】**Các nhà nghiên cứu đã đưa ra một số ý tưởng về sự tiến bộ tuyến tính. Nếu bước đầu tiên đã sai, mỗi bước sau đều dựa trên giả định sai lầm.

## Khái niệm cốt lõi

### Cây của tư tưởng (Yao et al., NeurIPS 2023)

Mỗi nút là một bước trung gian liên kết ("một suy nghĩ"). Mỗi nút có thể mở rộng đến suy nghĩ của trẻ em K. LLM tự đánh giá mỗi nút với một lời nhắc điểm. Tìm kiếm khám phá cây  BFS, DFS hoặc chùm.

> Mỗi node là một bước trung gian liên tục (连贯的中间步骤) "一个思考")  Mỗi node có thể mở rộng thành K 个子思考──LLM 用评分提示自评每个节点──搜索探索这个树BFS、DFS 或梁 搜索──

```
                     (root: "find 24 from 4 6 4 1")
                    /               |            \
           ("6 - 4 = 2")    ("4 + 1 = 5")    ("4 * 6 = 24")  <- Score: HIGH
              /   \              |                  |
          ...    ...          ...                finish
```

Thử nghiệm tự đánh giá là một phần chịu tải.`sure / likely / impossible`phân loại, `1..10`Tất cả ba đều đánh bại CoT đáng kể trong Game of 24 (4% -> 74% với GPT-4).

>  **【类比】**ToT 像下象棋时时的"算路": mỗi bước trước trong bộ não tính toán 3-5 变化(扩展), tự đánh giá thay đổi nào thuận lợi hơn( tự đánh giá), cắt giảm thay đổi xấu rõ ràng(không thể), sâu vào tính toán thay đổi thuận lợi。CoT là "được trực tiếp tính toán bước tiếp" tính toán toàn bộ lỗ。Lời chơi của 24 từ 4% đến 74% tăng là chứng cứ trực tiếp nhất về giá trị "算路"".

> Bản đánh giá là phần chịu trách nhiệm cốt lõi.`sure / likely / impossible`- Định nghĩa`1..10`Số giá trị đánh giá và bầu cử ứng cử.

### LATS (Zhou et al., ICML 2024)

LATS thống nhất ToT, ReAct và Reflexion dưới MCTS. LLM đóng ba vai trò:

> LATS trong MCTS 下统一了 ToT, ReAct và Reflection.

- **Policy**: đề xuất ứng cử viên các hành động tiếp theo (tương tự như ReAct).
  Trung ngữ翻译:**策略**: đề xuất候选下一步行动(ReAct 风格)
- **Value function**: ghi một quỹ đạo một phần (Tô-T tự-tỷ lệ).
  Trung ngữ翻译:**价值函数**:对部分轨迹评分(ToT 风格自评)
- **Self-reflector**: khi thất bại, viết một phản ánh ngôn ngữ tự nhiên (tương tự như phản ánh) và sử dụng nó để xem xét lại các triển khai trong tương lai.
  Trung ngữ翻译:**自我反思器**失败时写自然语言反思 (Reflection 风格), được sử dụng để tái gieo trồng triển khai tương lai.

Phản hồi môi trường (sự quan sát) trộn vào hàm giá trị để tìm kiếm được thông báo bởi kết quả công cụ thực tế, không chỉ là ý kiến mô hình. Kết quả trong thời gian giấy: HumanEval pass@1 92.7% với GPT-4 (SOTA), WebShop trung bình 75.9 với GPT-3.5 (chấp cận điều chỉnh dựa trên gradient).

> 环境反(观察)混入价值函数,使搜索由真工具结果而不是仅仅模型观点驱动──论文发表时的结果:GPT-4 上 HumanEval pass@1 92.7%(SOTA),GPT-3.5 上 WebShop 平均 75.9(接近基于梯度的微调) ⋅

### MCTS, tối thiểu

Bốn giai đoạn cho mỗi lần lặp lại:

> Mỗi lần 代四阶段:

1. **Select** đi từ gốc đến lá bằng cách sử dụng UCT (tự tin trên kết nối với cây).
   Trung ngữ翻译:**选择** sử dụng UCT(nên trên cây) từ gốc đi đến các cột cây.
2. **Expand** sinh ra con K thông qua chính sách.
   Trung ngữ翻译:**扩展** sử dụng chiến lược tạo ra K 个子节点。
3. **Simulate** triển khai từ một đứa trẻ sử dụng chính sách, ghi điểm với hàm giá trị (hoặc phần thưởng môi trường).
   Trung ngữ翻译:**模拟**从子节点用策略展开,用价值函数 (或环境奖励) 评分叶节点──
4. **Backpropagate** cập nhật số lượng truy cập và ước tính giá trị trên con đường.
   Trung ngữ翻译:**反向传播** Thường xuyên cập nhật số lượng truy cập và ước tính giá trị.

Công thức UCT: `Q(s, a) + c * sqrt(ln N(s) / N(s, a))`Từ đầu tiên là khai thác; từ thứ hai là khám phá.`c`cho mỗi nhiệm vụ.

> UCT 公式:`Q(s, a) + c * sqrt(ln N(s) / N(s, a))`❖ thứ nhất là sử dụng; thứ hai là khám phá ❖ theo nhiệm vụ điều chỉnh `c`

### Thực tế chi phí

Tìm kiếm nổ token. ToT trên Game of 24 sử dụng 1001000x các token của CoT. LATS tương tự.

> ️ **【易错点】**Xem ToT trong Game of 24 上 +70 个点就以为是"银弹",套到所有任务上.**后果**Trong câu hỏi đơn giản, tiêu thụ 1000 lần token thay đổi 0% tăng, tài khoản nổ.**一行修复**Đầu tiên, sử dụng 10 mẫu đối với CoT vs ToT, tăng < 5 điểm về trở lại CoT tìm kiếm chỉ cho nhiệm vụ "một đường mòn rõ ràng thiếu hụt" có hiệu quả.

> 搜索会爆炸 token──TT 在 24 上消耗 CoT 100-1000倍的代币──LATS 类似──This is not free; will search leave to:

- Nhiệm vụ khi một quỹ đạo duy nhất là không đủ (Game of 24, mã phức tạp).
  Trung文翻译:单轨迹明显不足的任务(Lát bài 24、复杂代码)
- Nhiệm vụ mà thời gian tường ít quan trọng hơn sự chính xác.
  Trung ngữ翻译:正确性比耗时更重要任务──
- Nhiệm vụ với hàm giá rẻ, đáng tin cậy (thử nghiệm đơn vị cho mã, mục tiêu rõ ràng cho toán học).
  Trung ngữ翻译:有廉价可靠价值函数的任务(代码的单元测试、数学的明确目标) ⋅

Nếu nhiệm vụ của bạn có một câu trả lời đúng và một đánh giá ồn ào, tìm kiếm thường làm cho mọi thứ tồi tệ hơn  nó tìm thấy một câu trả lời sai "được điểm tốt".

> 🤔 **【困惑】**Q: LATS Đặt ToT/ReAct/Reflection 三个都"统一"了, đó là chưa học LATS就够了吗 A: 不够.LATS là "重型武器" một lần tìm kiếm đầy đủ cần mở trên trăm điểm, mã chỉ mục đích đơn 成本可达百万级.

> Nếu nhiệm vụ của bạn chỉ có một câu trả lời chính xác nhưng máy đánh giá có tiếng ồn, tìm kiếm thường làm cho tình hình tồi tệ hơn. Nó sẽ tìm thấy một câu trả lời "đặc biệt nhưng sai".

> **【中文解读】**搜尋会爆炸 TokenToT 在 24 游戏上消耗 CoT 100-1000倍―― chỉ trong các trường hợp sau đây sử dụng tìm kiếm: đơn轨迹明显不足、正确性比速度重要、有廉价可靠的价值函数―― nếu máy đánh giá có tiếng ồn, tìm kiếm có thể tìm thấy câu trả lời "高分但错误"――

### Định vị 2026

Hầu hết các đại lý sản xuất không chạy LATS. Họ chạy ReAct bằng cách xác minh dựa trên công cụ (CRITIC, Bài học 05).

> Đại đa số sản xuất Agent không vận hành LATS. Chúng vận hành với công cụ  xác định chứng nhận của ReAct.

- Các tác nhân mã hóa chạy các thử nghiệm như hàm giá trị (HumanEval-style).
  Trung文翻译:以测试作为价值函数的编码代理 (HumanEval 风格)
- Các đại lý nghiên cứu sâu khám phá nhiều con đường truy vấn.
  Trung ngữ翻译:探索多个查询路径的深度研究代理.
- Các dòng công việc có tính kế hoạch nặng trong các phụ hình LangGraph.
  Trung文翻译:LangGraph 子图内重规划工作流──

AlphaEvolve (Dạy 11) là cực đoan năm 2025: tìm kiếm tiến hóa về mã, tính năng phù hợp có thể kiểm tra bằng máy, tăng trưởng hàng rào (sự cải thiện đầu tiên của 4x4 trong 56 năm).

> AlphaEvolve (第 11 课) là một ví dụ cực cùng của năm 2025: tìm kiếm tiến hóa trên mã, máy tính có thể kiểm tra được độ thích ứng, bước đột phá trước mặt của máy tính.

## Hãy xây dựng nó.
```figure
tree-of-thoughts
```

## Hãy xây dựng nó

`code/main.py`thực hiện:

> `code/main.py`实现:

- Một ToT BFS nhỏ trên một nhiệm vụ "chọn toán học".
  Trung ngữ翻译: 在风格化"选算术运算"任务上的微型 ToT BFS。
- Một vòng lặp LATS MCTS đồ chơi trên cùng một nhiệm vụ (Hãy chọn / mở rộng / mô phỏng / đẩy ngược) với lựa chọn UCT.
  Trung văn翻译: cùng nhiệm vụ LATS MCTS 循环(选择/扩展/模拟/反向传播),带 UCT 选择。
- Một hàm giá trị tạo thành điểm tượng trưng cộng với điểm tự bằng.
  Trung ngữ翻译: một hàm giá trị của các điểm đánh giá và tự đánh giá.

Đi đi.

> 运行:

```
python3 code/main.py
```

Hướng dẫn cho thấy ToT mở rộng ba ứng cử viên cho mỗi nút với BFS, so với LATS hội tụ trên việc triển khai tốt nhất thông qua MCTS.

> 轨迹 hiển thị ToT sử dụng BFS Mỗi node mở rộng ba ứng cử viên, với LATS  thông qua MCTS 收 đến tốt nhất triển khai đối với.

## Hãy sử dụng nó để thực hiện

LangGraph cung cấp các mẫu mẫu ToT như các mẫu phụ; blog của nhóm LangChain trên LATS (Từ 2024) là hướng dẫn tham khảo. LlamaIndex cung cấp một `TreeOfThoughts`Đối với hầu hết các đại lý sản xuất năm 2026 mô hình này sống sau một`if task_complexity > threshold: use_search()`gate  xem mô hình đánh giá- tối ưu hóa trong Bài học 05.

> LangGraph sẽ tìm hiểu ToT 风格 như một mô hình hình cung cấp; LangChain 团队关于 LATS 的博客(2024 年 5 月) là một bài học tham khảo.`TreeOfThoughts`Đối với hầu hết các đại lý sản xuất năm 2026, mô hình này tồn tại trong`if task_complexity > threshold: use_search()`门控后参见第 5 课的评估器-优化器模式──

## Chuyển nó đi.

`outputs/skill-search-policy.md`chọn giữa ReAct tuyến tính, ToT, LATS và tìm kiếm tiến hóa do hình dạng nhiệm vụ, ngân sách và độ trung thành của người đánh giá.

> `outputs/skill-search-policy.md`根据任务形状、预算和评估器保真度,在线性 ReAct、ToT、LATS 和进化搜索之间选择──

## Tập luyện bài tập

1. Lên đồ chơi LATS với UCT c=0.1 so với c=2.0.
   Trung ngữ翻译:用 UCT c=0.1 和 c=2.0 分别运行 LATS──轨迹有什么变化?
2. Thay đổi hàm giá trị cho một điểm số ồn ào hơn (đã thêm jitter ngẫu nhiên). MCTS vẫn tìm thấy lá tốt nhất?
   Trung ngữ翻译:将价值函数替换为更杂的评分器──MCTS còn tìm được điểm 叶节最佳吗? nó có thể chịu được âm thanh tối thiểu là bao nhiêu?
3. Thực hiện ToT (giữ top-k ở mỗi cấp độ) và so sánh với BFS.
   Trung文翻译:实现beam-search ToT(每层保留 top-k), so với BFS đối với Token 预算紧张时哪个更好?
4. Đọc LATS Phần 5.1. Tái tạo lại con số quỹ đạo HumanEval: cần bao nhiêu lần triển khai để đạt được thông qua được báo cáo@1?
   Trung ngữ翻译:阅读 LATS 第 5.1 节──重现 HumanEval 的轨迹数量:达到报告的 pass@1 需要多少次展开?
5. Đọc bài thảo luận của LATS về "lúc nào LATS giúp ít hơn".
   Trung ngữ翻译:阅读 LATS 论文关于"何时 LATS 帮助不大"的讨论──写一段决策规则映射任务形状到搜索策略──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Tree of Thoughts | "Branching CoT" / "分支思维链" | Yao et al. — tree of thought nodes with self-evaluation / Yao 等人——带自评估的思维节点树 |
| LATS | "MCTS for LLMs" / "LLM 的 MCTS" | Zhou et al. — unifies ToT + ReAct + Reflexion under MCTS / Zhou 等人——在 MCTS 下统一 ToT+ReAct+Reflexion |
| UCT | "Upper confidence bound" / "上置信界" | Select formula balancing exploitation (Q) and exploration (ln N / n) / 平衡利用(Q)和探索(ln N/n)的选择公式 |
| Value function | "How good is this state" / "状态有多好" | Prompted LLM score or environment reward; feeds backprop / 提示的 LLM 评分或环境奖励；驱动反向传播 |
| Policy | "Action proposer" / "行动提议器" | ReAct-style generator; emits candidate next thoughts/actions / ReAct 风格生成器；发出候选下一步思考/行动 |
| Rollout | "Simulated trajectory" / "模拟轨迹" | Walk from a node to a leaf using policy, score with value / 用策略从节点走到叶节点，用价值函数评分 |
| Backpropagate | "Update ancestors" / "更新祖先" | Push the leaf's reward up the path, updating visit counts and Q / 将叶节点的奖励沿路径上推，更新访问计数和 Q 值 |
| Search cost | "Token explosion" / "Token 爆炸" | 100-1000x CoT on Game of 24; budget before you adopt / Game of 24 上是 CoT 的 100-1000 倍；采用前先做预算 |

## Xem thêm 延伸阅读

- [Yao et al., Tree of Thoughts (arXiv:2305.10601)](https://arxiv.org/abs/2305.10601) giấy phép
  Trung ngữ翻译:思维树经典论文。
- [Zhou et al., LATS (arXiv:2310.04406)](https://arxiv.org/abs/2310.04406) MCTS với phản hồi phản xạ
  Trung文翻译:LATS带 Reflection 反的蒙特卡洛树搜索──
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) mẫu phụ hình cho tìm kiếm
  Trung文翻译:LangGraph 概览搜索的子图模式──
- [AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131) Tìm kiếm tiến hóa với các nhà đánh giá chương trình
  Trung ngữ翻译:AlphaEvolve带程序化评估器的进化搜索──
