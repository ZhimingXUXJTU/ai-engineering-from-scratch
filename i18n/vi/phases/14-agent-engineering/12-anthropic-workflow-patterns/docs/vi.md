# Mô hình lưu lượng công việc của Anthropic: đơn giản hơn phức tạp  Antropic 流程工作模式:简单优于复杂

> Schluntz và Zhang (Anthropic, Dec 2024) phân biệt các dòng công việc (các con đường được xác định trước) với các đại lý (phương tiện sử dụng động lực). Năm mô hình dòng công việc bao gồm hầu hết các trường hợp. Bắt đầu với các cuộc gọi API trực tiếp. Chỉ thêm các đại lý khi không thể dự đoán các bước.

> **【中文解读】**Anthropic trong bài viết tháng 12 năm 2024 đã phân biệt giữa các dòng chảy làm việc (đường dẫn được xác định trước) và các loại hình sử dụng các công cụ động (Agent) 五种工作流模式覆盖大多数场景. Từ API trực tiếp 调用开始.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop) | **前置知识:** Phase 14 · 01 (Agent 循环)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Mục tiêu học tập

- Tên năm mô hình quy trình làm việc của Anthropic: chuỗi nhanh, định tuyến, song song, nhạc công-người làm việc, đánh giá-tích cực.
  Trung ngữ翻译:说出人类的五种工作流模式:提示链、路由、并行化、编排器-工作者、评估器-优化器──
- Giải thích sự khác biệt giữa người đại lý và dòng công việc và chi phí kỹ thuật của mỗi người.
  Trung ngữ翻译: giải thích Sự khác biệt giữa đại lý và dòng công việc và chi phí công việc riêng lẻ.
- Xác định khi nào nên chọn một dòng công việc thay vì một đại lý (và ngược lại).
  Trung文翻译:识别何时选择工作流而非 Agent (反之亦然)
- Thực hiện tất cả năm mô hình trong stdlib chống lại một LLM kịch bản.
  Trung ngữ翻译:用标准库针对脚本 LLM 实现所有五种模式──

## Vấn đề  vấn đề giới thiệu

Các nhóm tìm kiếm các khung đa đại lý cho các vấn đề cần một cuộc gọi chức năng duy nhất. Chi phí là thực: các khung thêm các lớp làm mờ các yêu cầu, che giấu dòng chảy kiểm soát và mời phức tạp sớm. Bài đăng của Schluntz và Zhang tháng 12 năm 2024 là sự đẩy lùi công nghiệp được trích dẫn nhiều nhất: bắt đầu đơn giản, thêm phức tạp chỉ khi nó kiếm được chi phí của nó.

> 团队 chỉ cần một lần điều chỉnh hàm vấn đề chọn nhiều Agent 框架──代价是真实的: framework thêm模糊提示、隐藏控制流、引入过早复杂性的层──Schluntz 和 Zhang năm 2024 tháng 12 bài viết được trích dẫn nhiều nhất trong ngành phản ánh: từ đơn giản bắt đầu, chỉ có giá trị trong sự phức tạp của nó khi chi phí được thêm vào──

> **【中文解读】**Anthropic trong tháng 12 năm 2024 Building Effective Agents đã xác định bốn loại mô hình: 1) Quả chuỗi chuỗi bước chuỗi; 2) Đường dẫn; 3) Phối hợp; 4) Nhà dàn nhạc-Người làm việc;

> **【拓展：Anthropic 的工作流模式分类已成为 Agent 工程的事实标准】**LangGraph sử dụng trạng thái để thực hiện các mô hình này, OpenAI Agents SDK sử dụng Handoffs  thực hiện đường dẫn và sắp xếp, CrewAI sử dụng Crew  thực hiện đồng hành hóa.

>  **【前置】**必须先过阶段14·01 (Agent Loop) 本节就是它的"模式提炼"──还需要看阶段14·02 (ReWOO) ‧阶段14·05 (Sự tinh chỉnh) ‧阶段14·10 (Skills) 五种工作流模式都对应前面学过的具体技术,没基础会感觉空洞──

## Khái niệm cốt lõi

### Phòng làm việc đối với các đại lý

- **Workflow.**LLM và công cụ được sắp xếp thông qua các con đường mã được xác định trước.
  Trung ngữ翻译:**工作流。**通过预定义代码路径编排的 LLM 和工具──工程师拥有图──
- **Agent.**LLM động hướng công cụ của riêng họ và thực hiện các bước của riêng họ.
  Trung ngữ翻译:**Agent。**LLM 动态 hướng dẫn các công cụ và bước của mình.

Cả hai đều có vị trí của mình. Dòng công việc rẻ hơn, nhanh hơn và dễ dàng để gỡ lỗi.

>  **【类比】**Workflow vs Agent 像地铁 vs 自驾:地铁(workflow)路线固定、便宜、可靠,但你只能去站点;自驾(agent)灵活、能去任何地方,但可能迷路、烧油、出车祸──日常通勤选地铁(workflow),探索未知地区选自驾(agent) ⋅ New手最常见的错误是" tất cả nhiệm vụ đều tự lái"其实 80% nhiệm vụ sản xuất là地铁能完成

> 两者都有其武之地――工作流更便宜、更快、更容易调试――Agent 解锁开放式问题但使失败模式更难推理――

### Các LLM tăng cường

Nền tảng cho tất cả năm mô hình: một LLM với ba khả năng được kết nối trong tìm kiếm (khám), công cụ (cách), bộ nhớ (căng cường).

> 所有五种模式的基础: Một LLM 配备三种能力搜索(检索) 、工具(行动) 、记忆(持久化) ✿ Bất kỳ API 调用都可以使用这些──

### 5 mô hình

1. **Prompt chaining.**Khả năng phát ra của cuộc gọi 1 là đầu vào vào cuộc gọi 2. Sử dụng khi một nhiệm vụ có sự phân hủy tuyến tính sạch. Cổng lập trình tùy chọn giữa các bước.
   Trung ngữ翻译:**提示链。**调用 1 的输出是调用 2 的输入. Khi nhiệm vụ có phân tích线性 rõ ràng, nó được sử dụng.
2. **Routing.**Một LLM phân loại chọn LLM hoặc công cụ nào để sử dụng. Sử dụng khi các đầu vào khác nhau cần xử lý khác nhau (Tiêu 1 hỗ trợ vs hoàn trả vs lỗi vs bán hàng).
   Trung ngữ翻译:**路由。**分类器 LLM 选择调用哪个下游 LLM 或工具── khi các loại nhập khác nhau cần xử lý khác nhau.
3. **Parallelization.**Run N LLM gọi đồng thời, kết quả tổng hợp. Hai hình dạng: phân đoạn (các mảnh khác nhau) và bỏ phiếu (những lần nhanh chóng, N chạy, đa số / tổng hợp).
   Trung ngữ翻译:**并行化。**并发运行 N 个 LLM 调用,聚合结果──两种形式:分段(不同块) 和投票(同提示,N 次运行,多数/综合)
4. **Orchestrator-workers.**Một tổ chức LLM động lực quyết định những người lao động (còn LLM) để chạy và tổng hợp sản lượng của họ.
   Trung ngữ翻译:**编排器-工作者。**编排器 LLM 动态决定运行哪些工作者(也是 LLM)并综合其输出──类似于代理循环但编排器不会无限循环──
5. **Evaluator-optimizer.**Một LLM đề xuất một câu trả lời, một LLM khác đánh giá nó. lặp lại cho đến khi người đánh giá vượt qua.
   Trung ngữ翻译:**评估器-优化器。**Một LLM  đưa ra câu trả lời, một LLM  đánh giá nó.

### Khi các dòng công việc đánh bại các nhân viên

> 工作流优于 Trình trường của đại lý:

- **Predictable tasks.**Nếu bạn có thể liệt kê các bước, bạn nên.
  Trung ngữ翻译:**可预测任务。**Nếu có thể đưa ra một bước, bạn nên đưa ra một bước.
- **Cost-bound tasks.**Các dòng công việc có số bước giới hạn; các đại lý có thể xoay quanh.
  Trung ngữ翻译:**成本受限任务。**工作流有有限步数;Công ty có thể bị mất kiểm soát.
- **Compliance-bound tasks.**Các kiểm toán viên muốn đọc biểu đồ, không suy luận nó từ quỹ đạo.
  Trung ngữ翻译:**合规受限任务。**审计员 muốn đọc bản đồ, chứ không phải theo dõi.

### Khi các nhân viên đánh bại các dòng công việc

> Trưởng 优于工作流的场景:

- **Open-ended research.**Khi nào bước tiếp theo phụ thuộc vào bước cuối cùng trở lại.
  Trung ngữ翻译:**开放式研究。**Khi bước tiếp theo quyết định bước tiếp theo là trở lại với cái gì.
- **Variable-length tasks.**Những phút đến giờ làm việc mà con số bước không được biết.
  Trung ngữ翻译:**可变长度任务。**Từ vài phút đến vài giờ làm việc, số bước không biết.
- **Novel domains.**Khi bạn chưa biết đúng quy trình làm việc  khám phá trước, lập mã sau đó.
  Trung ngữ翻译:**新领域。**Khi bạn còn không biết đúng dòng công việc thì hãy tìm hiểu trước, sau đó tìm hiểu.

### Các đồng hành kỹ thuật ngữ

"Kỹ thuật ngữ ngữ cảnh hiệu quả cho các đại lý AI" (Anthropic 2025) chính thức hóa ngành học liền kề: cửa sổ 200k là ngân sách, không phải là một thùng chứa. Những gì cần bao gồm, khi nào để nén, khi nào để cho ngữ cảnh phát triển. Được bao gồm chi tiết trong bài học giai đoạn 14 về nén ngữ cảnh.

> "AI Agent's有效上下文工程" (Anthropic 2025) đã hình thành các ngành tương ứng:

## Hãy xây dựng nó.

> ️ **【易错点】**团队 thường xuyên nhất bước trên: xem Anthropic 五种模式就直接全部上 LangGraph/CrewAI 框架──**后果**Có thể làm cho các hệ thống này có thể được sử dụng để tạo ra các hệ thống tự động.**先直接 API 调用，加复杂度只为换取能力**" Một chuỗi nhanh chóng sử dụng thông thường Python hàm liên kết lên là đủ, không cần bất kỳ khung nào".""**一行修复**Đánh giá mỗi nhiệm vụ có thể được thực hiện bằng các quy định khác, có thể được thực hiện trên một khung khác.
```figure
workflow-chain
```

## Hãy xây dựng nó

`code/main.py`thực hiện tất cả năm mô hình lưu lượng làm việc chống lại một `ScriptedLLM`- Có thể là:

> `code/main.py` đối với `ScriptedLLM`实现了所有五种工作流模式:

- `prompt_chain(input, steps)` theo trình tự.
- `route(input, classifier, handlers)` Định dạng + vận chuyển.
- `parallel_vote(prompt, n, aggregator)` N chạy, tổng hợp.
- `orchestrator_workers(task, workers)` Nhà dàn nhạc chọn công nhân.
- `evaluator_optimizer(task, proposer, evaluator, max_iter)` vòng lặp cho đến khi vượt qua.

Đi đi.

> 运行:

```
python3 code/main.py
```

Mỗi mô hình in dấu vết của nó. Tổng số các dòng mã cho mỗi mô hình là ~ 10-15; chi phí của một khung được đo bằng hàng ngàn.

> Mỗi mô hình in đường của nó. Số lượng mã của mỗi mô hình là khoảng 10-15; chi phí của khung là 1000.

> 🤔 **【困惑】**Q: 既然"workflow 优先" thì rõ ràng, tại sao LangGraph、CrewAI những khung này lại nóng như vậy?**持久化、可观测性、人在回路、监控**Những chức năng "运维级" này. Bạn sử dụng chuỗi nhanh chóng viết 30 行 stdlib  chạy 挂了, bạn đã tự nghĩ làm thế nào để phục hồi từ bước 17; sử dụng LangGraph 写的,框架免费给你检查点. Vì vậy kết luận là "phase nguyên mẫu sử dụng stdlib, sản xuất giai đoạn đánh giá liệu có trên khung" thay vì không có bộ não hoặc không có bộ não không trên.

## Hãy sử dụng nó để thực hiện

- API trực tiếp yêu cầu hầu hết các nhiệm vụ.
  Trung ngữ翻译: Hầu hết các nhiệm vụ sử dụng trực tiếp API 调用。
- Quadro chỉ khi mô hình thực sự cần trạng thái bền (LangGraph), đồng thời mô hình diễn viên (AutoGen v0.4), hoặc mô hình vai trò (CrewAI).
  Trung ngữ翻译:只在模式真正需要持久状态 (只在模式真正需要持久状态) 长图 (LangGraph) 演员 模型并发 (AutoGen v0.4) 或角色模板 (CrewAI) 时使用框架 (框架)
- Hãy tìm SDK của Claude Agent khi bạn muốn hình dạng của Claude Code mà không cần xây dựng lại nó.
  中文翻译:当你想要克劳德码 框架形态而不重建时选择克劳德代理 SDK。

## Chuyển nó đi.

`outputs/skill-workflow-picker.md`chọn mô hình phù hợp cho mô tả nhiệm vụ nhất định, bao gồm lý do lý luận quyết định và con đường chuyển đổi đến một đại lý nếu các dòng công việc không đạt được kết quả.

> `outputs/skill-workflow-picker.md`Để xác định nhiệm vụ mô tả lựa chọn mô hình đúng đắn, bao gồm lý do quyết định và cách thức xây dựng lại cho đại lý khi không có dòng chảy công việc.

## Tập luyện bài tập

1. Thực hiện định tuyến với ngưỡng độ tin cậy. dưới ngưỡng -> leo thang lên con người. Điểm ngưỡng cho trường hợp sử dụng hỗ trợ cấp 1 nằm ở đâu?
   Trung ngữ翻译:实现带信度值的路由.
2. Thêm thời gian nghỉ `parallel_vote`Điều gì xảy ra khi một cuộc gọi bị treo? Làm thế nào để tổng hợp với số phiếu bị bỏ phiếu?
   中文翻译:为 `parallel_vote`添加超时. Khi một调用挂起时怎么办? Làm thế nào để tập hợp bỏ phiếu thiếu sót?
3. Chuyển đi`evaluator_optimizer`trong một tên cướp: giữ cho đầu 2 đầu ra trên các lần lặp lại để kết quả tốt muộn không bị ghi lại bởi một kết quả xấu muộn.
   Trung ngữ翻译:将 `evaluator_optimizer`变成 bandit:跨代保留 top-2 输出,避免后期好结果被后期坏结果覆盖──
4. Kết hợp chuỗi nhanh với định tuyến: một router chọn một trong ba chuỗi. đo chi phí token so với một lựa chọn thay thế lớn.
   Trung ngữ翻译:组合提示链和路由:路由器选择三条链之一――对比单一大提示替代方案的代号 成本――
5. Chọn một trong những tính năng sản xuất của bạn vẽ biểu đồ quy trình làm việc đếm bước liệu một đại lý thực sự tốt hơn ở đây?
   Trung ngữ翻译:选择一个你的生产功能――画出工作流图――计算步骤――Agent 真的更好吗?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Workflow | "Predefined flow" / "预定义流程" | Engineer-owned graph of LLM and tool calls / 工程师拥有的 LLM 和工具调用图 |
| Agent | "Autonomous AI" / "自主 AI" | Model-owned graph; dynamic tool direction / 模型拥有的图；动态工具指导 |
| Augmented LLM | "LLM with tools" / "带工具的 LLM" | LLM + search + tools + memory; the atomic unit / LLM + 搜索 + 工具 + 记忆；原子单元 |
| Prompt chaining | "Sequential calls" / "串行调用" | Output of call N is input to call N+1 / 调用 N 的输出是调用 N+1 的输入 |
| Routing | "Classifier dispatch" / "分类分派" | Pick which chain/model handles the input / 选择哪个链/模型处理输入 |
| Parallelization | "Fan out" / "扇出" | N concurrent calls; aggregate by sectioning or voting / N 个并发调用；按分段或投票聚合 |
| Orchestrator-workers | "Dispatcher agent" / "分派 Agent" | Orchestrator LLM picks specialist LLMs dynamically / 编排器 LLM 动态选择专家 LLM |
| Evaluator-optimizer | "Proposer + judge" / "提议者 + 评判者" | Iterate until evaluator passes; Self-Refine generalized / 迭代直到评估器通过；Self-Refine 的泛化 |

## Xem thêm 延伸阅读

- [Anthropic, Building Effective Agents (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) 5 mô hình quy trình làm việc
  Trung ngữ翻译:Anthropic 关于构建有效代理的文章五种工作流模式──
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) kỷ luật đối tác
  Trung ngữ翻译:Anthropic 关于 AI Agent 有效上下文工程的文章伴随学科──
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) khi biểu đồ trạng thái kiếm được chi phí của họ
  Trung文翻译:LangGraph 概览有状态图何时值得其成本──
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) mô hình nhạc công-người lao động, sản xuất
  Trung文翻译:OpenAI Agents SDK编排器-工作者模式的产品化。
