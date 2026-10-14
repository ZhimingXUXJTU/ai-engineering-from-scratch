# Sử dụng công cụ và chức năng gọi 工具使用与函调用

> Toolformer (Schick et al., 2023) bắt đầu tự giám sát ghi chú công cụ. Berkeley Function Calling Leaderboard V4 (Patil et al., 2025) đặt thanh 2026: 40% agentic, 30% multi-turn, 10% live, 10% non-live, 10% ảo giác.

> **【中文解读】**Toolformer  mở đầu tự giám sát công cụ nhãn.Berkley Function Calling Leaderboard V4 xác định tiêu chuẩn đánh giá năm 2026: 40% 智能体,30% 多轮,10% 实时,10% 非实时,10% 幻觉检测.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 13 · 01 (Function Calling Deep Dive) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 13 · 01 (函数调用深入)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Mục tiêu học tập

- Giải thích tín hiệu đào tạo tự giám sát của Toolformer: chỉ giữ ghi chú công cụ khi thực thi giảm mất token tiếp theo.
  Trung ngữ翻译:解释 Toolformer 的自监督训练信号: chỉ trong việc thực hiện giảm下一个代币 损失时保留工具标注。
- Hãy nêu tên năm loại đánh giá của BFCL V4 và mỗi loại đánh giá là gì.
  Trung ngữ翻译:说出 BFCL V4 的五个评估类别及每个衡量的内容──
- Thực hiện một danh sách công cụ stdlib với xác thực schema, buộc lập luận và sandboxing thực thi.
  Trung ngữ翻译:用标准库实现带模式验证、参数强制转换和执行沙箱的工具注册表
- Chẩn đoán ba vấn đề mở năm 2026: chuỗi công cụ đường dài, ra quyết định năng động và bộ nhớ.
  Trung ngữ翻译:诊断三个 2026年开放问题:长链工具编排、动态决策和记忆──

## Vấn đề  vấn đề giới thiệu

Sử dụng công cụ sớm được hỏi: mô hình có thể dự đoán một cuộc gọi chức năng chính xác không? Sử dụng công cụ hiện đại hỏi: có thể các công cụ chuỗi mô hình trên 40 bước, với bộ nhớ, với khả năng quan sát một phần, với sự phục hồi từ thất bại công cụ, mà không ảo giác các công cụ không tồn tại?

> Câu hỏi về việc sử dụng công cụ sớm là: mô hình có thể dự đoán đúng hàm调用 không? Câu hỏi về công cụ hiện đại là: mô hình có thể sử dụng công cụ trong 40 bước trong chuỗi không có bộ nhớ, xử lý phần có thể quan sát được, phục hồi từ thất bại của công cụ và không có vẻ như không có công cụ?

Toolformer đã thiết lập đường cơ sở: các mô hình có thể học được khi nào gọi công cụ với sự tự giám sát. BFCL V4 xác định mục tiêu đánh giá năm 2026 .

> Toolformer đã xây dựng một cơ sở: mô hình có thể thông qua tự giám sát để học cách sử dụng các công cụ. BFCL V4 đã xác định mục tiêu đánh giá năm 2026:

> **【中文解读】**Vấn đề sử dụng công cụ sớm là: mô hình có thể dự đoán được các hàm điều chỉnh đúng không? Vấn đề sử dụng công cụ hiện đại là: mô hình có thể sử dụng các công cụ điều chỉnh chuỗi trong 40 bước không? Có bộ nhớ, xử lý phần có thể quan sát được? Khôi phục từ thất bại của công cụ và không có vẻ như không tồn tại?

> **【拓展：BFCL V4 评估体系的演进】**Berkeley Function Calling Leaderboard V4 là tiêu chuẩn đánh giá thực tế năm 2026[6]. V3 đưa ra đánh giá dựa trên trạng thái( kiểm tra API  trạng thái thực tế chứ không phải phù hợp AST), V4 thêm Web  tìm kiếm、 nhớ và dạng nhạy hạng。 phát hiện quan trọng: đơn vòng hàm调用 đã gần như giải quyết, thất bại tập trung vào trí nhớ(跨轮次上下文传递)、 động thái quyết định( dựa trên kết quả trước lựa chọn công cụ) và长链漂移(20+ 后偏离任务)。

>  **【前置】**本节假设你已经能写 JSON Schema 并理解人类的 `input_schema`vs OpenAI của `function.parameters`区别;Phase 14·01(Agent Loop)  công cụ调用 được trong vòng lặp của Agent, rời vòng lặp một mình xem công cụ调用 sẽ mất trên bên dưới.

## Khái niệm cốt lõi

### Toolformer (Schick et al., NeurIPS 2023)

Ý tưởng: để cho mô hình ghi chú bản thân trước khi tập với các cuộc gọi API ứng cử viên. Đối với mỗi ứng cử viên, thực hiện nó. Giữ ghi chú chỉ khi bao gồm kết quả công cụ làm giảm tổn thất trên token tiếp theo.

> 核心思想: Hãy để mô hình sử dụng bản thân mình trước khi được đào tạo 标签 ứng cử viên API 调用.

Các công cụ được bao gồm: máy tính, hệ thống kiểm tra chất lượng, công cụ tìm kiếm, dịch giả, lịch.

> 覆盖的工具:计算器、QA 系统、搜索引擎、翻译器、日历──自监督信号纯粹关于工具是否帮助预测文本不需要人工标签──

Kết quả quy mô: việc sử dụng công cụ xuất hiện trên quy mô. Các mô hình nhỏ hơn bị tổn thương bởi các chú thích công cụ; các mô hình lớn hơn tăng. Đây là lý do tại sao các mô hình biên giới 2026 có sử dụng công cụ mạnh mẽ được nấu trong khi hầu hết các mô hình 7B cần thiết thiết lập cụ thể sử dụng công cụ để được đáng tin cậy.

> 规模效应: dụng cụ sử dụng trên mô hình lớn nổi lên. 小模型反而被工具标注损害; 大模型则受益. Đó là lý do tại sao mô hình tiền tuyến năm 2026 được đặt vào khả năng sử dụng dụng dụng cụ mạnh mẽ, trong khi hầu hết các mô hình 7B cần các công cụ rõ ràng sử dụng các phương pháp nhỏ để có thể tin cậy.

> **【中文解读】**Ý tưởng cốt lõi của Toolformer: để mô hình sử dụng các ngôn ngữ dự kiến của mình để đánh dấu ứng cử viên API 调用. Đối với mỗi ứng cử viên, thực hiện nó. Chỉ khi kết quả có trong các công cụ có thể giảm thiểu tổn thất của một token tiếp theo mới có thể giữ lại các ngôn ngữ.

### Berkeley Function Calling Leaderboard V4 (Patil et al., ICML 2025)

BFCL là đánh giá thực tế năm 2026.

> BFCL là tiêu chuẩn đánh giá thực tế năm 2026:

- **Agentic (40%)** Các quỹ đạo đầy đủ: trí nhớ, nhiều vòng quay, quyết định năng động.
  Trung ngữ翻译:**智能体 (40%)**完整 Agent 轨迹: nhớ, quay, động thái quyết định
- **Multi-Turn (30%)** cuộc trò chuyện tương tác với chuỗi công cụ.
  Trung ngữ翻译:**多轮 (30%)**带工具链的交互式对话──
- **Live (10%)** Các yêu cầu thực được người dùng gửi (cải phân phối khó khăn hơn).
  Trung ngữ翻译:**实时 (10%)** người dùng gửi thực tế提示(更难的分布)
- **Non-Live (10%)** Các trường hợp thử nghiệm tổng hợp.
  Trung ngữ翻译:**非实时 (10%)**合成测试用例──
- **Hallucination (10%)** phát hiện khi không cần gọi công cụ.
  Trung ngữ翻译:**幻觉 (10%)**检测何时不应调用工具──

V3 giới thiệu đánh giá dựa trên trạng thái: sau một chuỗi công cụ, kiểm tra trạng thái thực tế của API (ví dụ: "tệp đã được tạo ra không?") thay vì phù hợp với AST của các cuộc gọi công cụ. V4 thêm các loại tìm kiếm web, bộ nhớ và độ nhạy định dạng.

> V3 giới thiệu đánh giá dựa trên trạng thái: sau khi thực hiện chuỗi công cụ, kiểm tra trạng thái thực tế của API như "file có đã được tạo không?") thay vì sử dụng các công cụ phù hợp AST。V4 đã thêm các loại Web  tìm kiếm、 ký ức và độ nhạy dạng。

Phát hiện quan trọng của năm 2026: gọi hàm một lượt gần như đã được giải quyết. Các lỗi tập trung trong bộ nhớ (tiếp tục mang bối cảnh qua các lượt), ra quyết định năng động (chọn các công cụ dựa trên kết quả trước đó), chuỗi đường chân trời dài (trở đi sau 20+ bước), và phát hiện ảo giác (đà từ chối gọi khi không có công cụ phù hợp).

> Phát hiện quan trọng năm 2026: đơn vòng hàm调用已接近解决;;失败集中在记忆(跨轮次传递上下文) 动态决策(基于先前结果选择工具) 长链漂移(20+ 步后偏离) 和幻觉检测 ((在不合适工具时拒绝调用) 

### Chế hoạch công cụ

Mỗi nhà cung cấp đều có một kế hoạch.

> Mỗi nhà cung cấp có mô hình riêng của họ.

```
name: string
description: string (what it does, when to use it)
input_schema: JSON Schema (properties, required, types, enums)
```

Sử dụng nhân loại `input_schema`trực tiếp. OpenAI sử dụng `function.parameters`. Cả hai đều chấp nhận JSON Schema. mô tả chịu tải  mô hình đọc chúng để chọn công cụ đúng. mô tả công cụ xấu là nguyên nhân gốc số 1 của sự thất bại trong việc chọn công cụ sai.

>  **【类比】**工具描述就像给实习生写的"使用说明书"――模型从未见过你的工具,它唯一能依赖的就是描述――如果你写`name: get_user, description: "gets user"`, mô hình không biết là theo ID hoặc theo hộp thư, trả lại là đối tượng hoàn chỉnh hoặc chỉ có tên.**好描述包含三要素**Làm gì + 何時用 + 输入输出语义──

> ️ **【易错点】**                                                                                                                                                                                                                                                              `"5"`(字符串) trở lại `int`của kế hoạch.**后果**:你的工具函数 `TypeError` , toàn bộ vòng tròn của đại lý 中断**一行修复**: trong công cụ thực hiện nhập khẩu thống nhất làm `pydantic.BaseModel.parse_obj`Hoặc giống như thử nghiệm, thử nghiệm thất bại khi trả về cấu trúc sai lầm như`{"error": "expected int, got str"}`Hãy thử lại.

> Nhân văn 直接使用 `input_schema`❖ OpenAI 使用 `function.parameters`◊ Cả hai đều chấp nhận JSON Schema。 mô tả là trọng tâm của mô hình  thông qua đọc mô tả để chọn đúng công cụ。 mô tả của công cụ xấu là chọn sai công cụ thất bại 

### Định giá lý lẽ

Không tin vào công cụ gọi.

> Đừng tin bất cứ công cụ nào.

1. **Type coercion.**Mô hình có thể trả lại chuỗi "5" nơi schema nói int. Cố gắng nếu không rõ ràng; từ chối nếu không.
   Trung ngữ翻译:**类型强制转换。**模型可能返回字符串 "5" Nhưng模式要求 int──如果无歧义则强制转换;否则拒绝──
2. **Enum validation.**Nếu kế hoạch nói `status in {"open", "closed"}`và các loại phát thải mô hình `"in_progress"`, từ chối với một lỗi mô tả.
   Trung ngữ翻译:**枚举验证。**Nếu mô hình được xác định`status in {"open", "closed"}`Và mô hình xuất khẩu`"in_progress"`, dùng để mô tả sai lầm từ chối.
3. **Required fields.**Thiếu trường yêu cầu -> quan sát lỗi ngay lập tức trở lại mô hình, không phải là một vụ tai nạn.
   Trung ngữ翻译:**必填字段。**缺少必填字段 -> 立即返回错误观察给模型, thay vì bị phá hủy.
4. **Format validation.**Ngày, email, URL  xác nhận bằng các parsers bê tông, không phải regex.
   Trung ngữ翻译:**格式验证。**Ngày期、邮箱、URL sử dụng các máy phân tích cụ thể, thay vì biểu hiện chính thức.

Mỗi thất bại xác nhận nên trả lại một quan sát có cấu trúc để mô hình có thể thử lại với hình dạng chính xác.

> Mỗi lần thử nghiệm thất bại đều phải quay lại quan sát cấu trúc, để mô hình có thể được thử lại theo định dạng chính xác.

### Các cuộc gọi công cụ song song

Các nhà cung cấp hiện đại hỗ trợ các cuộc gọi công cụ song song trong một lượt trợ lý.

> 现代提供商支持在一个助手轮次中并行调用工具──循环:

1. Mô hình phát ra 3 tool call với các điểm khác nhau `tool_use_id`S.
   Trung ngữ翻译:模型发出 3 个带有不同 `tool_use_id`                                                                                                                                                                                                                                                              
2. Runtime thực hiện chúng (trong song nếu độc lập).
   Trung文翻译:运行时执行它们 (如果独立则并行)
3. Mỗi kết quả đều trở lại như một`tool_result`khối liên quan đến `tool_use_id`- Tôi không biết.
   中文翻译: mỗi kết quả như `tool_result`块返回, qua `tool_use_id`关联:

Quy tắc kỹ thuật: coi ID tương quan như là chịu tải, thay đổi chúng và bạn có được đường dẫn từ công cụ sai đến kết quả sai.

> 🤔 **【困惑】**Q: 40% trong BFCL V4 là đại lý, có phải chỉ ra rằng một vòng đã không quan trọng? A: Không. 40% là đại lý để phản ánh sản xuất thực tế, nhưng tỷ lệ xác thực đơn vẫn là cơ sở.

> Quy tắc kỹ thuật: 将关联 ID 视为核心承载──交换它们会导致错误的工具-结果路由──

### Sandboxing

Việc thực hiện công cụ là ranh giới hộp cát. Xem Bài học 09 để biết chi tiết. Phiên bản ngắn: mỗi công cụ nên chỉ định bề mặt đọc/tập, truy cập mạng, thời gian, memory cap.`run_shell(cmd)`là một lá cờ đỏ; cụ thể `git_status()`an toàn hơn.

> 工具执行是沙箱边界──详见第 9 课――简短版: Mỗi công cụ đều được chỉ định phạm vi đọc, truy cập mạng, thời gian và ký 存.`run_shell(cmd)`                                                                                                                                                                                                                                                              `git_status()`Thêm an toàn hơn.

## Hãy xây dựng nó.
```figure
tool-routing
```

## Hãy xây dựng nó

`code/main.py`thực hiện một sổ đăng ký công cụ hình dạng sản xuất:

> `code/main.py`实现一个生产级工具注册表:

- JSON Schema subset validator (stdlib chỉ).
  中文翻译:JSON Schema 子集验证器 (JSON Schema 子集验证器)
- Đăng ký công cụ với mô tả, sơ đồ nhập, thời gian nghỉ và trình thực hiện.
  Trung ngữ翻译:带描述、输入模式、超时和执行器的工具注册。
- Sự buộc buộc và xác nhận bằng chứng.
  Trung ngữ翻译:参数强制转换和枚举验证。
- Chuyển dụng đồng bộ với các thẻ xác định tương quan.
  Trung ngữ翻译:带关联 ID 的并行工具分派──
- Các quan sát lỗi như chuỗi cấu trúc.
  Trung文翻译:错误观察作为结构化字符串──

Đi đi.

> 运行:

```
python3 code/main.py
```

Hình ảnh này cho thấy một đại lý nhỏ gọi ba công cụ cùng một lượt, với một cuộc gọi cố ý bị sai lệch mà bị từ chối với một lỗi mô hình mô tả có thể hành động.

> 轨迹 cho thấy một đặc vụ mê trong một vòng gọi trong ba công cụ, trong đó một trong số đó cố ý định dạng sai lầm của gọi được mô tả sai lầm từ chối, mô hình có thể theo hành động này.

## Hãy sử dụng nó để thực hiện

Mỗi nhà cung cấp có kế hoạch công cụ riêng của mình  Anthropic, OpenAI, Gemini, Bedrock. Sử dụng một lớp dịch (OpenAI Agents SDK, Vercel AI SDK, LangChain tool adapter) nếu bạn cần nhiều nhà cung cấp. BFCL là điểm tham khảo  chạy nó chống lại đại lý của bạn trước khi vận chuyển nếu việc sử dụng công cụ là trung tâm của sản phẩm.

> Mỗi nhà cung cấp có mô hình công cụ riêng của mình Anthropic、OpenAI、Gemini、Bedrock。 nếu cần nhiều nhà cung cấp, sử dụng phiên dịch层(OpenAI Agents SDK、Vercel AI SDK、LangChain 工具适配器) BFCL là cơ sở tham khảo Nếu công cụ sử dụng là cốt lõi sản phẩm, hãy phát hành trước sử dụng nó để thử nghiệm Agent của bạn。

## Chuyển nó đi.

`outputs/skill-tool-registry.md`tạo ra danh mục công cụ, sơ đồ và đăng ký cho một tên miền nhiệm vụ nhất định. Bao gồm kiểm tra chất lượng mô tả (có mô tả của mỗi công cụ cho mô hình biết khi nào sử dụng nó?).

> `outputs/skill-tool-registry.md`Để tạo danh mục công cụ trong lĩnh vực nhiệm vụ nhất định, mô hình và đăng ký.

## Tập luyện bài tập

1. Thêm một công cụ "không có" cho phép mô hình rõ ràng từ chối sử dụng bất kỳ công cụ nào khác.
   Trung ngữ翻译:添加一个"无操作"工具,让模型显然拒绝使用任何其他工具──在类 BFCL 幻觉测试上测量──
2. Thực hiện buộc buộc tranh luận cho int-as-string và float-as-string.
   Trung文翻译:实现字符串到 int 和字符串到浮动 的参数强制转换──强制转换何时开始隐藏真实 bug?
3. Thêm một thời gian nghỉ mỗi công cụ và một bộ cắt mạch (đánh bỏ công cụ trong 60s sau 3 thất bại liên tiếp). Điều này thay đổi gì về cách mô hình phục hồi?
   Trung ngữ翻译:添加每个工具的超时和断器(连续 3次失败后拒绝工具 60秒) ⋅ Điều này làm thế nào để thay đổi cách phục hồi mô hình?
4. Đọc mô tả BFCL V4. Chọn một danh mục (ví dụ: "multi-turn") và chạy 10 ví dụ yêu cầu thông qua đại lý của bạn.
   Trung ngữ翻译:阅读 BFCL V4 描述──选择一个类别(如"多轮")并通过你的代理 运行 10 个示例提示──报告通过率──
5. Đưa xác nhận STDlib vào Pydantic hoặc Zod.
   Trung文翻译:将标准库验证器移植到Pydantic 或 Zod──Pydantic/Zod 捕获了玩具版本遗漏的什么?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Function calling | "Tool use" / "工具使用" | Structured-output tool invocation with validated schema / 带验证模式的结构化输出工具调用 |
| Toolformer | "Self-supervised tool annotation" / "自监督工具标注" | Schick 2023 — keep tool calls whose results reduce next-token loss / Schick 2023——保留减少下一个 token 损失的工具调用 |
| BFCL | "Berkeley Function Calling Leaderboard" / "Berkeley 函数调用排行榜" | 2026 benchmark: 40% agentic, 30% multi-turn, 10% live, 10% non-live, 10% hallucination / 2026 基准：40% 智能体、30% 多轮、10% 实时、10% 非实时、10% 幻觉 |
| Tool schema | "Function signature for the model" / "模型的函数签名" | name, description, JSON Schema of arguments / 名称、描述、参数的 JSON Schema |
| tool_use_id | "Correlation ID" / "关联 ID" | Ties a tool call to its result; essential for parallel dispatch / 将工具调用与其结果关联；并行分派必需 |
| Hallucination detection | "Know when not to call" / "知道何时不调用" | V4 category: refuse to call when no tool fits / V4 类别：无合适工具时拒绝调用 |
| Argument coercion | "String-to-int repair" / "字符串到整数的修复" | Narrow fixes for predictable schema-mismatch; reject if ambiguous / 可预测模式不匹配的窄修复；如果歧义则拒绝 |
| Sandboxing | "Tool execution boundary" / "工具执行边界" | Per-tool read/write surface, network, timeout, memory cap / 每个工具的读写范围、网络、超时、内存上限 |

## Xem thêm 延伸阅读

- [Schick et al., Toolformer (arXiv:2302.04761)](https://arxiv.org/abs/2302.04761) Nhận xét công cụ tự giám sát
  Trung文翻译:Toolformer 经典论文自监督工具标注。
- [Berkeley Function Calling Leaderboard (V4)](https://gorilla.cs.berkeley.edu/leaderboard.html) Định nghĩa chuẩn đánh giá năm 2026
  Trung文翻译:Berkeley 函数调用排行榜 V42026 年评估基准──
- [Anthropic, Tool use documentation](https://platform.claude.com/docs/en/agent-sdk/overview) Sơ đồ công cụ sản xuất trong SDK Claude Agent
  Trung文翻译:Anthropic 工具使用文档Claude Agent SDK 中的生产级工具模式──
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) loại công cụ chức năng và Guardrails
  中文翻译:OpenAI Agents SDK 文档函数工具类型和护。
