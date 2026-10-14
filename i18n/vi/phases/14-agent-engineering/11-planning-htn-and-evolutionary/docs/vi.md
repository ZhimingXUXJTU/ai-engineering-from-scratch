# Kế hoạch với HTN và Tìm kiếm tiến hóa ư

> Kế hoạch biểu tượng xử lý các trường hợp khi kế hoạch có thể chứng minh là chính xác. Tìm kiếm mã tiến hóa xử lý các trường hợp khi chức năng thể dục có thể kiểm tra bằng máy. ChatHTN (2025) và AlphaEvolve (2025) cho thấy mỗi khóa mở khi kết hợp với LLM.

> **【中文解读】**符号规划处理计划可证明正确的场景――进化代码搜索处理适应度函数可机器检查的场景――ChatHTN(2025) và AlphaEvolve(2025) đã cho thấy khả năng giải quyết hợp tác của riêng mình với LLM ──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 02 (ReWOO and Plan-and-Execute) | **前置知识:** Phase 14 · 02 (ReWOO 与计划-执行)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Giải thích mạng lưới nhiệm vụ cấp bậc: nhiệm vụ, phương pháp, nhà khai thác, điều kiện tiên quyết, hiệu ứng.
  Trung文翻译:解释分层任务网络:任务、方法、操作符、前置条件、效果──
- Mô tả vòng lặp lai của ChatHTN  tìm kiếm biểu tượng với phân hủy trở lại LLM.
  Trung文翻译:描述 ChatHTN 的混合循环带 LLM 回退分解的符号搜索──
- Giải thích vòng lặp tiến hóa của AlphaEvolve và tại sao nó chỉ hoạt động với một trình đánh giá chương trình.
  Trung ngữ翻译: giải thích vòng lặp tiến hóa của AlphaEvolve và tại sao nó chỉ có hiệu quả khi có trình độ đánh giá.
- Thực hiện một máy tính lên kế hoạch đồ chơi HTN cộng với một trò chơi tìm kiếm tiến hóa trong stdlib.
  Trung ngữ翻译:用标准库实现玩具 HTN 规划器和玩具进化搜索。

## Vấn đề  vấn đề giới thiệu

ReWOO (Dạy 02), Plan-and-Execute, và ReAct bao gồm hầu hết các kế hoạch của các đại lý.

> ReWOO(第 2 课) 、Plan-and-Execute 和 ReAct 覆盖大多数 Agent 规划──两种它们不能很好覆盖情况:

1. **Plans with provable correctness.**Lịch trình, đường bay, dòng công việc tuân thủ  kế hoạch phải được xây dựng đúng.
   Trung ngữ翻译:**可证明正确性的计划。**调度,航线规划,合规工作流计划必须在构建上是可靠的―― một bước phác thảo thường xuyên của流利 LLM 计划是不可接受的――
2. **Optimizations with a machine-checkable fitness function.**Sự nhân số tử liệu, lập trình tính toán học, biên dịch viên vượt qua  mục tiêu không phải là "một kế hoạch chính xác" mà là "kế hoạch tốt nhất".
   Trung ngữ翻译:**有机器可检查适应度函数的优化。**矩阵乘法、调度启发式、编译器 pass目标不是"một kế hoạch chính xác" mà là"最佳计划"──

> **【中文解读】**Các mô hình chính của Agent 规划: phân cấp nhiệm vụ mạng lưới (HTN) và tiến hóa quy hoạch.

HTN Planning và AlphaEvolve giải quyết hai vấn đề khác nhau. Cả hai đều sử dụng LLM như các bộ tăng cường, chứ không phải thay thế.

> HTN 规划和 AlphaEvolve 解决两个不同的问题──两者都将 LLM dùng như một máy mở rộng chứ không phải là một thay thế──

> **【拓展：2026 年 Agent 规划的前沿】**AlphaEvolve và Máy Darwin-Godel sẽ sử dụng thuật toán phát triển để tối ưu hóa chiến lược của chính Agent không chỉ là nhiệm vụ lập kế hoạch, mà còn là quy hoạch và quá trình lập kế hoạch chính nó.

>  **【前置】**必须先过阶段14·02 (ReWOO/Plan-and-Execute) HTN là phiên bản "nghắn định hình hóa" của nó;以及基本的经典 AI 规划知识 (Status, 预置条件, 效果) . Nếu bạn chưa nghe STRIPS hoặc PDDL, hãy đề nghị thêm một phần trước hai phần "Classical符号 AI"

## Khái niệm cốt lõi

### Các mạng lưới nhiệm vụ cấp bậc

Một HTN là:

> HTN là:

- **Tasks** hợp chất (để phân hủy) và nguyên thủy (được thực hiện trực tiếp).
  Trung ngữ翻译:**任务**复合(待分解)和原始(直接可执行)
- **Methods** cách phân hủy một nhiệm vụ hợp chất thành các nhiệm vụ phụ, với các điều kiện tiên quyết.
  Trung ngữ翻译:**方法**将复合任务分解为子任务的方式,带前置条件――
- **Operators** Các hành động ban đầu với các điều kiện và hiệu ứng.
  Trung ngữ翻译:**操作符**带前置条件和效果的原始动作──
- **State** một loạt các sự kiện.
  Trung ngữ翻译:**状态**一组事实──

Kế hoạch: với một nhiệm vụ mục tiêu và một trạng thái ban đầu, tìm ra sự phân hủy thành các nhà khai thác nguyên thủy mà các điều kiện tiên quyết được đáp ứng theo trình tự.

> 规划: cho được định mục tiêu nhiệm vụ và trạng thái đầu tiên, tìm một giải thể cho các trình điều hành đầu tiên, đặt trước điều kiện theo thứ tự đáp ứng.

HTN là lâu đời hơn LLM và vẫn là tham chiếu cho các kế hoạch có thể chứng minh là chính xác.

> HTN hơn LLM hơn, vẫn là một tài liệu có thể chứng minh đúng kế hoạch.

### ChatHTN (Gopalakrishnan et al., 2025)

ChatHTN (arXiv:2505.11814) kết nối HTN biểu tượng với các câu hỏi LLM:

> ChatHTN(arXiv:2505.11814)交替进行符号 HTN 和 LLM 查询:

1. Cố gắng phân hủy nhiệm vụ hợp chất hiện tại bằng các phương pháp hiện có.
   Trung文翻译:尝试用现有方法分解当前复合任务──
2. Nếu không có phương pháp áp dụng, hãy hỏi LLM: "chúng bạn sẽ phân hủy như thế nào `task`trong tiểu bang `s`"Điều gì?"
   Trung ngữ翻译: Nếu không có phương pháp thích hợp, hỏi LLM:"在状态 `s`Trung你会如何分解 `task`"Điều gì?"
3. Dịch câu trả lời LLM thành các nhiệm vụ phụ ứng cử viên.
   Trung văn翻译:将 LLM 响应翻译为候选子任务。
4. Thiết lập hợp lệ với các chương trình điều hành; từ chối phân hủy không hợp lệ.
   Trung文翻译:对照操作符模式验证;拒绝无效分解──
5. Lại tiếp.
   Trung文翻译:递归。

Lời tuyên bố chính của bài báo: mỗi kế hoạch được sản xuất đều có thể chứng minh là hợp lý bởi vì các đề xuất LLM chỉ được đưa vào như là phân hủy ứng cử viên, không bao giờ là chỉnh sửa kế hoạch trực tiếp.

>  **【类比】**ChatHTN 像严格的审计员 () 创意实习生 () ...................................................................................................................................................................................................................................................**结果**Tất cả các kế hoạch cuối cùng được chấp nhận đều được kiểm tra, độ tin cậy được đảm bảo.

> 论文的核心主张: Mỗi kế hoạch phát sinh đều có thể chứng minh là đáng tin cậy, bởi vì LLM 建议 chỉ như một ứng cử viên phân giải vào, từ không như một biên tập viên kế hoạch trực tiếp.

Học phương pháp trực tuyến (OpenReview `gwYEDY9j2x`, 2025 theo dõi) thêm một học viên tổng quát hóa phân hủy sản xuất LLM bằng cách lùi lại giảm tần suất truy vấn LLM lên đến 75%.

> Trong năm 2025, nghiên cứu tiếp theo đã tăng thêm các máy học phân hủy bằng cách tái phổ biến LLM.

### AlphaEvolve (Novikov et al., 2025)

AlphaEvolve (arXiv:2506.13131, DeepMind, tháng 6 năm 2025) là một con quái vật khác: tìm kiếm mã tiến hóa do bộ phận Flash / Pro Gemini 2.0 tổ chức.

> AlphaEvolve ((arXiv:2506.13131, DeepMind,2025 年 6 月) là một sự tồn tại khác: bởi Gemini 2.0 Flash/Pro 集群编排的进化代码搜索──

Lúp:

> Chuyển:

1. Bắt đầu với một chương trình hạt giống + một nhà đánh giá chương trình (giả lại điểm fitness).
   Trung ngữ翻译:从种子程序 + 程序化评估器(返回适应度分数) bắt đầu。
2. Nhóm LLM đề xuất đột biến.
   Trung文翻译:LLM 集群提出变异──
3. Thử các đột biến qua bộ đánh giá.
   Trung文翻译:通过评估器运行变异──
4. Hãy giữ những thứ tốt nhất, biến đổi lại.
   Trung文翻译: giữ giữ tốt nhất;再次变异──

Chiến thắng được công bố:

> 已发表成果:

- Sự cải thiện đầu tiên so với Strassen cho nhân số tử liệu phức tạp 4x4 trong 56 năm (48 nhân số scalar).
  Trung文翻译:56 年来首次改进 4x4 复矩阵乘法 Strassen 算法(48 次标量乘法) ⋅
- 0,7% đã phục hồi máy tính Google thông qua một hệ thống lập trình Borg.
  Trung ngữ翻译:通过 Borg 调度启发式回收 0.7% của Google 计算资源──
- FlashAttention tăng tốc 32% trên khối lượng công việc biên giới.
  Trung文翻译: 在前沿工作负载上 FlashAttention 加速 32%──

Khá hạn chế: chức năng thể dục phải được máy kiểm tra.

> ️ **【易错点】**Đưa AlphaEvolve 套到"创意写作优化"上让LLM sử dụng cải tiến thuật toán viết tiểu thuyết, sử dụng LLM 评分作为健身──**后果**: hoàn toàn không nhận được, vì chức năng fitness chính nó là LLM (随机+不稳定),**一行修复**: chỉ cho "có mục tiêu chỉ số nhiệm vụ lập trình" với AlphaEvolve ((cód hiệu suất, kiểm tra phủ sóng, điều chỉnh hiệu quả), sáng tạo loại nhiệm vụ trở lại tự tinh chỉnh / CRITIC。

> 硬约束: hàm ứng dụng phải là máy tính kiểm tra được.

### Khi nào sử dụng

| Problem class | Use | Why |
|---------------|-----|-----|
| 问题类别 | 使用 | 原因 |
| Scheduling with hard constraints | HTN + ChatHTN | Provable soundness / 可证明的可靠性 |
| Compiler optimization | AlphaEvolve | Machine-checkable fitness / 机器可检查的适应度 |
| Multi-step task execution | ReAct / ReWOO | LLM in the loop, no formal guarantees / LLM 在循环中，无形式化保证 |
| Code improvement with tests | AlphaEvolve | Tests are the evaluator / 测试即评估器 |
| Policy-bound automation | HTN | Preconditions encode policy / 前置条件编码策略 |

### Khi mô hình này đi sai

- **HTN without operators.**Nếu không có các quy trình điều kiện trước/sự ảnh hưởng thì tuyên bố tính hợp lý sẽ sụp đổ.
  Trung ngữ翻译:**没有操作符的 HTN。**Không có điều kiện trước/mô hình hiệu quả, tuyên bố đáng tin cậy đã sụp đổ.
- **AlphaEvolve without a real evaluator.**"Hãy hỏi LLM nếu mã là tốt hơn" không phải là một chức năng fitness.
  Trung ngữ翻译:**没有真正评估器的 AlphaEvolve。**"Hỏi LLM 代码 có tốt hơn" không phải là hàm thích ứng.
- **Over-engineering.**Hầu hết các nhiệm vụ của đại lý đều không cần thiết.
  Trung ngữ翻译:**过度工程。**Đại đa số đại lý nhiệm vụ không cần bất kỳ một.

> 🤔 **【困惑】**Q: ChatHTN 论文说"LLM chỉ đề nghị không trực tiếp vào kế hoạch"这跟LangChain Agent调用工具不是一回事吗? A: 不一样.普通 Agent 里 LLM quyết định调用哪个工具就直接执行了,没人验证"调用这个工具在当前状态是否合法"──ChatHTN 强制 LLM 提议经过符号层的先决条件 检查先决条件 满足才执行──这个"强制审计层"就是"可证明可靠性"的来源,普通 Agent 没有这个层──

## Hãy xây dựng nó.
```figure
htn-tree-expand
```

## Hãy xây dựng nó

`code/main.py`thực hiện hai đồ chơi:

> `code/main.py`实现了两个玩具:

- Một trình lập kế hoạch HTN có các nhà điều hành, phương pháp, điều kiện tiên quyết, hiệu ứng và một `LLMFallback`Làm này sẽ hoạt động khi không có phương pháp nào phù hợp với một nhiệm vụ hợp nhất.
  Trung ngữ翻译:一个标准库 HTN 规划器,带操作符、方法、前置条件、效果和当没有方法匹配复合任务时触发的`LLMFallback`"LLM" là một trình soạn thảo, lập trình viên có thể hoạt động trên mạng.
- Một cuộc tìm kiếm tiến hóa trên các chương trình toán học: tăng biểu thức mà sản lượng giảm thiểu `|f(x) - target|`Thử nghiệm là xác định.
  Trung ngữ翻译:一个标准库进化搜索, trong quá trình toán học:生长使 `|f(x) - target|`Trong tập hợp thử nghiệm, biểu hiện tối thiểu của .

Đi đi.

> 运行:

```
python3 code/main.py
```

Hướng dẫn cho thấy người lập kế hoạch HTN phân hủy một nhiệm vụ hợp chất (với một sự suy giảm LLM giữa kế hoạch) và vòng lặp tiến hóa hội tụ trên một biểu thức mục tiêu.

> 轨迹显示 HTN 规划器分解复合任务(带中途 LLM 回退) và chu trình tiến hóa tiếp nhận đến mục tiêu biểu hiện式。

## Hãy sử dụng nó để thực hiện

- **HTN planners** `pyhop`- `SHOP3`, hoặc xây dựng riêng của bạn cho việc thực thi chính sách cụ thể.
  Trung ngữ翻译:**HTN 规划器**`pyhop``SHOP3`, hoặc để thực hiện chiến lược cụ thể trong lĩnh vực tự xây dựng.
- **ChatHTN** mã nghiên cứu; mô hình (tình tượng + LLM fallback) được chuyển sang bất kỳ máy tính kế hoạch HTN nào.
  Trung ngữ翻译:**ChatHTN**研究代码;模式(符号 + LLM 回退) 可干净地移植到任何HTN 规划器──
- **AlphaEvolve** Tác phẩm DeepMind; mô hình (ensemble + evaluator) có thể tái tạo. OpenEvolve và các cổng mở nguồn tương tự đang xuất hiện.
  Trung ngữ翻译:**AlphaEvolve**DeepMind 论文;模式(集群 + 评估器) 可复现──OpenEvolve 和类似开源分支正在涌现──
- **Agent frameworks** không có tàu HTN hạng nhất hoặc AlphaEvolve.
  Trung ngữ翻译:**Agent 框架**Hiện tại không có HTN hoặc AlphaEvolve được xây dựng cho đại lý hay người làm việc sau đó.

## Chuyển nó đi.

`outputs/skill-hybrid-planner.md`tạo ra một sàn lập kế hoạch lai (HTN hoặc tiến hóa) với vai trò LLM được quy định rõ ràng.

> `outputs/skill-hybrid-planner.md`生成混合规划器脚手架(HTN 或进化),LLM 角色显式限定──

## Tập luyện bài tập

1. Tăng kế hoạch HTN với việc theo dõi ngược: khi điều kiện sau vận hành của một nhà điều hành thất bại trong thời gian chạy, quay lại và thử phương pháp tiếp theo.
   Trung ngữ翻译:为 HTN 规划器添加回溯: Khi điều kiện đặt sau của trình điều hành thất bại trong quá trình chạy, quay lại并尝试下一个方法──
2. Thêm một bộ nhớ cache của phương pháp LLM vào ChatHTN: khi LLM phân hủy nhiệm vụ `T`theo mô hình trạng thái `P`, lưu lại kết quả. kiểm tra lại thư viện phương pháp trước khi gọi tiếp theo.
   中文翻译:为 ChatHTN 添加 LLM 方法缓存:当 LLM 在状态模式 `P`中分解任务 `T`时, lưu trữ kết quả. 下次调用.
3. Thay đổi trình đánh giá tìm kiếm tiến hóa thành một bộ thử nghiệm thực tế. Phát triển một chức năng sắp xếp vượt qua 20 trường hợp thử nghiệm; báo cáo các thế hệ cho sự hội tụ.
   Trung ngữ翻译:将进化搜索评估器替换为真实测试套件──进化一个通过 20 个测试用例的排序函数;报告收代数──
4. Đọc các ghi chú thiết kế đánh giá của AlphaEvolve. Thiết kế một đánh giá cho một miền bạn quan tâm (tăng cường truy vấn SQL, giảm thiểu các tập hợp thử nghiệm, triển khai YAML).
   Trung ngữ翻译:阅读 AlphaEvolve's评估器设计笔记──为你关心的领域设计一个评估器(SQL 查询优化、测试套件最小化、部署 YAML)──
5. Kết hợp: sử dụng HTN để phân hủy một nhiệm vụ hợp chất thành các nhiệm vụ phụ, sau đó sử dụng tìm kiếm tiến hóa trên các nhà khai thác nguyên thủy của mỗi nhiệm vụ phụ.
   Trung ngữ翻译:组合使用: dùng HTN 分解复合任务为子任务, sau đó dùng cho các trình điều hành nguyên thủy của mỗi nhiệm vụ tiến hóa tìm kiếm.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| HTN | "Hierarchical planner" / "分层规划器" | Task decomposition with operators, preconditions, effects / 带操作符、前置条件、效果的任务分解 |
| Method | "Decomposition rule" / "分解规则" | Way to break a compound task into subtasks / 将复合任务分解为子任务的方式 |
| Operator | "Primitive action" / "原始动作" | Concrete step with precondition and effect / 带前置条件和效果的具体步骤 |
| ChatHTN | "LLM + HTN" / "LLM + HTN" | Symbolic planner asks LLM when no method matches / 符号规划器在没有方法匹配时询问 LLM |
| AlphaEvolve | "Evolutionary code search" / "进化代码搜索" | Ensemble LLMs mutate code; deterministic evaluator selects / LLM 集群变异代码；确定性评估器选择 |
| Fitness function | "Evaluator" / "评估器" | Deterministic, machine-checkable score over outputs / 输出上的确定性、机器可检查分数 |
| Online method learning | "Cached LLM decomposition" / "缓存的 LLM 分解" | Store + generalize LLM plans to cut query cost / 存储并泛化 LLM 计划以降低查询成本 |

## Xem thêm 延伸阅读

- [Gopalakrishnan et al., ChatHTN (arXiv:2505.11814)](https://arxiv.org/abs/2505.11814) biểu tượng + LLM lập kế hoạch lai
  Trung文翻译:ChatHTN 论文符号 + LLM 混合规划器。
- [Novikov et al., AlphaEvolve (arXiv:2506.13131)](https://arxiv.org/abs/2506.13131) Tìm kiếm mã tiến hóa với đột biến LLM
  Trung文翻译:AlphaEvolve 论文带 LLM 变异的进化代码搜索──
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) khi nào để tìm kiếm một kế hoạch cho so với một vòng lặp đơn giản
  Trung ngữ翻译:Anthropic 关于构建有效代理的指导 何时使用规划器而不是简单循环──
