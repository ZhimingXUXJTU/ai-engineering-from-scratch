# ReWOO và kế hoạch và thực hiện: Kế hoạch tách rời ư

> ReAct kết hợp suy nghĩ và hành động trong một dòng chảy. ReWOO tách chúng ra: một kế hoạch lớn trước, sau đó thực hiện. 5 lần ít hơn các token, độ chính xác +4% trên HotpotQA, và bạn có thể chưng cất kế hoạch thành một mô hình 7B. Plan-and-Execute tổng quát nó; Plan-and-Act quy mô nó đến định hướng web.

> **【中文解读】**ReAct trong một dòng chuyển đổi suy nghĩ và hành động。ReWOO sẽ phân chia chúng: trước tiên lập kế hoạch hoàn chỉnh, sau đó thực hiện。Token tiêu thụ giảm 5 lần,HotpotQA 准确率 tăng 4%, còn có thể biến lập trình viên biến mất thành 7B 模型。Plan-and-Execute là phiên bản phổ biến của nó,Plan-and-Act sẽ mở rộng nó đến webpages导航。

> **【拓展：ReWOO → 现代 Agent 架构】**Trong 5 mô hình hoạt động của Anthropic, mô hình kế hoạch thực hiện là một trong những mô hình trung tâm của các nhà sản xuất cấp độ năm 2026.

>  **【前置】**精通本节前请先掌握:Phase 14·01(Agent Loop / ReAct 循环) You must understand ReAct's"思考-行动-观察"交换模式, vì ReWOO là để hiểu được vấn đề tăng trưởng thứ hai của ReAct; cũng như khái niệm biểu đồ cơ bản của mình ((DAG、拓排序), không quen thuộc với DAG 会卡在"依赖解析"那一步.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop) | **前置知识:** Phase 14 · 01 (Agent 循环)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Mục tiêu học tập

- Giải thích tại sao chia kế hoạch / công nhân / giải pháp của ReWOO tiết kiệm token và cải thiện độ bền hơn vòng lặp liên kết của ReAct.
  Trung ngữ翻译:解释为什么 ReWOO 的规划器/工作器/求解器分离能节省代币并比 ReAct 的交换循环更强壮──
- Thực hiện một kế hoạch DAG, một trình thực hiện theo lệnh phụ thuộc, và một giải pháp tạo ra các sản xuất nhân viên  tất cả stdlib.
  Trung文翻译:实现计划 DAG、依赖顺序执行器和组合工作器输出求解器全部使用标准库──
- Quyết định khi nào một nhiệm vụ nên chạy như kế hoạch sau đó thực hiện vs ReAct liên kết, sử dụng khung năm 2026 "lên tục luồng công việc" (Anthropic).
  Trung ngữ翻译:使用 2026 年"五种工作流模式"框架 (Anthropic), quyết định nhiệm vụ là nên sử dụng kế hoạch thực hiện hoặc chuyển đổi ReAct.
- Nhận ra khi nào dữ liệu kế hoạch tổng hợp của Plan-and-Act cần thiết cho các công việc web hoặc di động dài hạn.
  Trung ngữ翻译:识别何时需要计划和行动的合成计划数据来处理长程网页或移动任务──

## Vấn đề  vấn đề giới thiệu

Loop suy nghĩ-cách-bản lý quan sát của ReAct là đơn giản và linh hoạt, nhưng mỗi cuộc gọi công cụ phải mang theo toàn bộ bối cảnh trước đó bao gồm cả mọi suy nghĩ trước đó. Việc sử dụng token tăng lên theo hình vuông với độ sâu.

> Chuyển đổi suy nghĩ- hành động- quan sát vòng lặp đơn giản, dễ dàng, nhưng mỗi lần công cụ được sử dụng đều cần mang theo một sự đặt trước hoàn chỉnh trên các bài viết dưới đây, bao gồm cả mỗi suy nghĩ trước đó.

ReWOO (Xu et al., arXiv:2305.18323, tháng 5 năm 2023) nhận thấy điều này và đặt cược: lên kế hoạch toàn bộ việc trước, lấy bằng chứng song song, soạn câu trả lời ở cuối. Một LLM gọi để lập kế hoạch, N công cụ gọi cho bằng chứng (có thể song song), một LLM gọi để giải quyết. Thương mại là ít linh hoạt hơn (kế hoạch là tĩnh) cho hiệu quả mã thông báo tốt hơn nhiều và các chế độ thất bại rõ ràng hơn.

>  **【类比】**ReWOO 像装修房子前先出施工图:设计师一次性画完全部工序 (设计师一次性画完全部工序) 工人按图并行施工互不打扰 (工程器) 工人按图并行施工互不打扰 (工程器) 工人按图并行施工互不打扰 (工程器) 工人按图并行施工互不打扰 (工程器) 工人按图并行施工互不打扰 (工程器) 验收时把所有工序结果拼拼到一起结算 (求解器) ⋅ ReAct 则像边施工边设计,每个工人可以翻阅前面所有工人的笔记动手,所以10步后笔记就堆成山──

> ReWOO(Xu 等人,arXiv:2305.18323,2023 年 5 月) lưu ý đến điều này và đề xuất một chương trình: trước tiên lập kế hoạch toàn bộ nhiệm vụ,并行 nhận chứng cứ,最后组合答案――一次 LLM 调用规划、N 次工具调用获取证据(可并行)、一次 LLM 调用求解──代价是灵活性降低(计划是静态的), nhưng thay vào đó là hiệu quả hiệu quả biểu tượng tốt hơn và mô hình thất bại rõ ràng hơn――

## Khái niệm cốt lõi

### Ba vai diễn

```
Planner:  user_question -> [plan_dag]        # 规划器：将用户问题转为计划 DAG
Workers:  [plan_dag]     -> [evidence]        # 工作器：执行工具调用获取证据（可并行）
Solver:   user_question, plan_dag, evidence -> final_answer  # 求解器：组合证据生成最终答案
```

Planner tạo ra một DAG. Mỗi nút đặt tên cho một công cụ, các lập luận của nó và các nút trước đó nó phụ thuộc vào (thông tin như `#E1`- `#E2`Người lao động thực hiện các nút theo thứ tự topological.

> 规划器 tạo ra một DAG. Mỗi node chỉ định một công cụ, các tham số của nó và các dependent trước đây của nó.`#E1``#E2`等引用) ・工作器按拓顺序执行节点――求解器将所有内容拼拼在一起――

### Tại sao 5x ít hơn các token

ReAct tăng chiều dài nhanh theo đường thẳng với số bước. Ở bước 10, prompt chứa suy nghĩ 1 cộng với hành động 1 cộng với quan sát 1 cộng với suy nghĩ 2 cộng với hành động 2 cộng với quan sát 2, v.v. Mỗi bước trung gian cũng có chứa prompt ban đầu.

> ReAct của các gợi ý độ dài theo từng bước số lượng đường dẫn tăng lên. Đến 10 bước, các gợi ý chứa đựng suy nghĩ 1 +  hành động 1 + 观察 1 + 思考 2 +  hành động 2 + 观察 2, theo các loại gợi ý. Mỗi bước trung gian còn còn có chỗ chứa các gợi ý ban đầu.

ReWOO trả một đơn giản lập kế hoạch (rất lớn), N đơn giản công nhân nhỏ (mỗi đơn giản là gọi công cụ, không có chuỗi), và một đơn giản giải quyết.

> ReWOO chỉ cần một lần lập trình viên gợi ý (n) 、N 个小工作器 gợi ý (n)  Mỗi chỉ chứa các công cụ调用, không có chuỗi lịch sử) và một lần gợi ý giải pháp (求解器提示──) trên HotpotQA trên bài viết đã giảm khoảng 5 lần token, đồng thời tỷ lệ xác thực tuyệt đối tăng 4%──

### Tại sao nó mạnh hơn

Nếu worker 3 thất bại trong ReAct, vòng lặp phải lý luận ra khỏi lỗi giữa dòng. Trong ReWOO, worker 3 trả lại một chuỗi lỗi; người giải quyết thấy nó trong bối cảnh với kế hoạch ban đầu và có thể hạ thấp một cách đẹp trai.

> Nếu Workstation 3 thất bại trong ReAct, vòng lặp phải được định hình trong quá trình giữa từ lỗi trong. Trong ReWOO, Workstation 3 trả lại một chuỗi sai trong kế hoạch ban đầu.

### Phân lọc máy kế hoạch

Kết quả thứ hai của bài báo: vì người lập kế hoạch không thấy quan sát, bạn có thể tinh chỉnh mô hình 7B trên các sản phẩm lập kế hoạch từ một giáo viên 175B. mô hình nhỏ xử lý lập kế hoạch; mô hình lớn không cần thiết khi suy luận.

> Kết quả thứ hai của bài luận: Vì lập trình viên không thấy kết quả quan sát, bạn có thể trong 175B mô hình giáo viên lập trình xuất ra một mô hình 7B 模型──小模型处理规划;大模型在推理时不需要── đây là thực hành tiêu chuẩn许多2026年生产代理使用小规划器和大执行器,反之亦然──

> **【拓展：规划器蒸馏 → 成本优化】**Vì lập trình viên không cần kết quả quan sát, có thể đưa ra 175B mô hình giáo viên lập trình ra ngoài và phát triển đến 7B mô hình.

### Kế hoạch và thực hiện (LangChain, 2023)
### Kế hoạch và thực hiện (2023)

Bài đăng tháng 8 năm 2023 của nhóm LangChain đã tổng quát ReWOO thành một tên mẫu: Plan-and-Execute. Planner phía trước phát hành danh sách bước, trình thực hiện chạy mỗi bước, một nhà lập kế hoạch lại tùy chọn có thể sửa đổi sau khi quan sát kết quả. Điều này gần hơn với ReAct hơn ReWOO (những lập kế hoạch lại đưa quan sát trở lại kế hoạch) nhưng vẫn giữ lại tiết kiệm token.

> LangChain 团队 bài viết tháng 8 năm 2023 sẽ ReWOO 泛化为一个模式名称:Plan-and-Execute。前置规划器发出步骤列表,执行器运行每一步,可选的重新规划器可以在观察结果后修订──这比 ReWOO 更接近 ReAct(重新规划器将观察带回规划),但保留了代币节省──

### Kế hoạch và Đạo luật (Erdogan et al., arXiv:2503.09572, ICML 2025)

Plan-and-Act quy mô mô cho các đại lý web và di động tầm xa. Sự đóng góp chính là dữ liệu kế hoạch tổng hợp: một máy phát hành quỹ đạo có nhãn sản xuất dữ liệu đào tạo khi kế hoạch rõ ràng. Được sử dụng để điều chỉnh các mô hình lập kế hoạch tiếp tục làm việc sau 3050 bước trên các nhiệm vụ giống như WebArena nơi một quỹ đạo ReAct duy nhất mất tính nhất quán.

> Plan-and-Act sẽ mở rộng mô hình này đến các trang web và đại lý di động dài dài. Một đóng góp quan trọng là dữ liệu kế hoạch tổng hợp: máy tạo quỹ đạo đánh dấu tạo ra dữ liệu đào tạo, trong đó kế hoạch là rõ ràng.

### Khi nào để chọn

| Pattern | When | 适用场景 |
|---------|------|----------|
| ReAct | Short tasks, unknown environment, need reactive exception handling | 短任务、未知环境、需要响应式异常处理 |
| ReWOO | Structured tasks with known tools, token-sensitive, parallelizable evidence | 结构化任务、已知工具、Token 敏感、可并行 |
| Plan-and-Execute | Like ReWOO but with replanning after partial execution | 类似 ReWOO 但支持执行后重新规划 |
| Plan-and-Act | Long-horizon (>30 steps), web/mobile/computer-use | 长程任务(>30步)、网页/移动端/计算机使用 |
| Tree of Thoughts | Search is worth paying for (Lesson 04) | 值得付出搜索成本的场景 |

Chỉ dẫn của Anthropic tháng 12 năm 2024: bắt đầu với đơn giản nhất. Nếu nhiệm vụ là một cuộc gọi công cụ cộng với một bản tóm tắt, đừng xây dựng ReWOO. Nếu nhiệm vụ là một nhiệm vụ nghiên cứu 40 bước, đừng làm ReAct một mình.

> 🤔 **【困惑】**Q: 既然 ReWOO 省 5 倍代币还准确,为什么不全部使用 ReWOO? A: 因为 ReWOO 的计划是"静态"的一发发就不再根据观察调整.

> Giới thiệu về giải pháp nghiên cứu của Anthropic 2024: Từ đầu tiên đơn giản nhất. Nếu nhiệm vụ là một công cụ, hãy thêm một bản tóm tắt, đừng xây dựng ReWOO. Nếu nhiệm vụ là nhiệm vụ nghiên cứu 40 bước, đừng chỉ sử dụng ReAct.

## Hãy xây dựng nó.

> ️ **【易错点】**实现 ReWOO 时新手最常踩的坑: quên đi kế hoạch DAG làm vòng kiểm tra.`#E1`Tùy vào`#E2`Và `#E2`Và phụ thuộc vào`#E1`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,**后果**:Tình điều hành 挂起或溢出──**一行修复**: To xếp hạng sau kiểm tra đã xếp hạng số điểm liệu bằng với tổng số điểm, không giống như như bỏ`CycleDetectedError`
```figure
rewoo-plan
```

## Hãy xây dựng nó

`code/main.py`thực hiện một đồ chơi ReWOO:

> `code/main.py`实现一个玩具 ReWOO:

- `Planner` một chính sách kịch bản phát hành một kế hoạch DAG từ một lời nhắc.
  Trung ngữ翻译:`Planner` Từ lời khuyên tạo kế hoạch DAG
- `Worker` gửi các nút của các công cụ gọi qua registry.
  Trung ngữ翻译:`Worker` thông qua đăng ký phân chia mỗi phần của công cụ调用
- `Solver` thành phần kịch bản đọc bằng chứng và tạo ra câu trả lời cuối cùng.
  Trung ngữ翻译:`Solver`读取证据并生成最终答案的脚本组合器──
- Giải quyết phụ thuộc  tham chiếu như `#E1`được thay thế bằng sản lượng lao động trước đó.
  Trung ngữ翻译:依赖解析如`#E1`引用被替换为前前的工作器输出──

Phản ứng biểu diễn là "Thế số dân số của thủ đô Pháp là bao nhiêu, được tròn xuống hàng triệu?" bằng cách sử dụng một kế hoạch hai bước: (1) tìm ra thủ đô, (2) tìm kiếm dân số, sau đó giải quyết.

> 演讲回答"Quân số người ở thủ đô Pháp là bao nhiêu,四舍五入到百万?" sử dụng hai bước kế hoạch: 1) Tìm kiếm thủ đô, 2) Tìm kiếm dân số, rồi tìm giải pháp.

Đi đi.

> 运行:

```
python3 code/main.py
```

Các dấu vết cho thấy toàn bộ kế hoạch trước, sau đó kết quả công nhân, sau đó thành phần giải pháp. So sánh số lượng mã thông báo (chúng tôi in một số chữ xấp xỉ) với một kiểu ReAct chạy được giao nhau  ReWOO thắng trên loại nhiệm vụ có cấu trúc này.

> 轨迹 đầu tiên hiển thị kế hoạch hoàn chỉnh, sau đó là kết quả của máy, cuối cùng là kết quả của bộ máy.

## Hãy sử dụng nó để thực hiện

LangGraph tàu kế hoạch và thực hiện như một công thức (`create_react_agent`cho ReAct, đồ thị tùy chỉnh cho thực hiện kế hoạch). dòng chảy của CrewAI mã hóa mô hình trực tiếp: bạn xác định các nhiệm vụ trước và Flow DAG thực hiện chúng. Phương pháp dữ liệu tổng hợp của Plan-and-Act vẫn chủ yếu là nghiên cứu; mô hình thời gian chạy (plan DAG rõ ràng) được sản xuất thông qua LangGraph và CrewAI Flow.

> LangGraph sẽ lập kế hoạch và thực hiện như một phụ kiện cung cấp`create_react_agent`Sử dụng để ReAct, tự định hình sử dụng để lập kế hoạch- thực hiện) ――CrewAI's Flow  trực tiếp mã hóa mô hình này: bạn đã xác định trước nhiệm vụ, Flow DAG  thực hiện chúng。Phương pháp tổng hợp dữ liệu của Plan-and-Act vẫn chủ yếu trong giai đoạn nghiên cứu;

## Chuyển nó đi.

`outputs/skill-rewoo-planner.md`tạo ra một kế hoạch ReWOO DAG từ yêu cầu của người dùng, được cung cấp một danh mục công cụ. Nó xác nhận kế hoạch (acyclic, mọi tham chiếu được giải quyết, mọi công cụ tồn tại) trước khi giao cho một người thực thi.

> `outputs/skill-rewoo-planner.md`根据用户请求和工具目录生成 ReWOO 计划 DAG──它在移交给执行器之前验证计划(无环、每个引用已解析、每个工具存在)。

## Tập luyện bài tập

1. Lấy các nút kế hoạch độc lập để thực hiện công việc song song.
   Trung ngữ翻译:将独立计划节点的工作器并行化.
2. Thêm một nút tái lập kế hoạch sẽ khởi động nếu bất kỳ công nhân nào trả về một lỗi.
   Trung ngữ翻译: 添加一个在工作器返回错误时触发的重新规划节点──ReWOO 变成计划执行的最小改动是什么?
3. Thay thế `Planner`với mô hình nhỏ (tầng 7B) và giữ `Solver`So sánh chất lượng đầu đến cuối  nơi phân chia thất bại?
   Trung文翻译:用小模型(7B 级) thay thế lập kế hoạch, giữ trước bờ模型 như tìm giải pháp.
4. Đọc phần 4 của bài báo của ReWOO về chưng cất kế hoạch.
   Trung ngữ翻译:阅读 ReWOO论文第4节关于规划器蒸的内容──概念上重现 175B→7B 结果:需要什么训练数据?如何评估计划质量?
5. Đưa đồ chơi vào hình dạng quỹ đạo của Plan-and-Act: kế hoạch là một chuỗi, không phải là DAG. Những sự đổi thay nào?
   Trung ngữ翻译:将玩具系统移植为 Plan-and-Act的轨迹形式:计划是序列而不是DAG.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| ReWOO | "Reasoning without observations" / "无观察推理" | Plan, then fetch evidence in parallel, then solve — no observations in the planning prompt / 先规划，再并行获取证据，最后求解——规划提示中不包含观察 |
| Plan-and-Execute | "LangChain's plan-execute pattern" / "LangChain 的计划-执行模式" | ReWOO with an optional replanner node after execution / 带可选重新规划节点的 ReWOO |
| Plan-and-Act | "Scaled plan-execute" / "扩展版计划-执行" | Explicit planner/executor split with synthetic plan training data for long-horizon tasks / 使用合成计划训练数据的长程任务显式规划器/执行器分离 |
| Evidence reference | "#E1, #E2, ..." / "证据引用" | Plan-node placeholder substituted with prior worker output at dispatch time / 计划节点占位符，在分派时替换为工作器输出 |
| Planner distillation | "Small planner, big executor" / "小规划器，大执行器" | Fine-tune a small model on planner traces from a large teacher / 用大模型的规划轨迹微调小模型 |
| Token efficiency | "Fewer round trips" / "更少往返" | 5x fewer tokens on HotpotQA vs ReAct in the paper / 论文中 HotpotQA 上比 ReAct 减少 5 倍 token |
| DAG executor | "Topological dispatcher" / "拓扑分派器" | Runs plan nodes in dependency order; parallel at each level / 按依赖顺序运行计划节点；每层可并行 |

## Xem thêm 延伸阅读

- [Xu et al., ReWOO: Decoupling Reasoning from Observations (arXiv:2305.18323)](https://arxiv.org/abs/2305.18323) giấy phép
  Trung ngữ翻译:ReWOO 经典论文将推理与观察解──
- [Erdogan et al., Plan-and-Act (arXiv:2503.09572)](https://arxiv.org/abs/2503.09572) Kiểu kế hoạch-hành động viên có kế hoạch tổng hợp
  Trung文翻译:Plan-and-Act使用合成计划的扩展版规划器-执行器──
- [LangGraph Plan-and-Execute tutorial](https://docs.langchain.com/oss/python/langgraph/overview) Công thức khung
  Trung文翻译:LangGraph Plan-and-Execute 教程框架配方──
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) chọn mô hình đơn giản nhất có hiệu quả
  Trung ngữ翻译:Anthropic 关于构建有效代理的指导选择最简单的可行模式──
