# Ngân sách hành động, giới hạn lặp lại, và quản trị chi phí 动作预算, 代上限与成本管理器

> Chi phí LLM hàng tháng của một đại lý thương mại điện tử vừa lớn đã tăng từ $1,200 to $4.800 sau khi nhóm của mình kích hoạt kỹ năng "điểm theo dõi đơn đặt hàng". Đó không phải là lỗi giá cả. Đó là một đại lý đã tìm thấy một vòng lặp mới và giữ chi tiêu bên trong nó.`max_tokens`, mỗi công việc mã thông báo và ngân sách đô la, mỗi ngày / tháng giới hạn, giới hạn lặp lại, định tuyến mô hình cấp bậc, lưu trữ cache nhanh, cửa sổ bối cảnh, các điểm kiểm soát HITL cho các hành động đắt tiền, tắt các chuyển đổi khi vi phạm ngân sách. SDK Claude Code Agent của Anthropic gửi các nguyên thủy tương tự dưới các tên khác nhau. giới hạn tốc độ tài chính  ví dụ cắt truy cập lên > $ 50 trong 10 phút  bắt vòng lặp nhanh hơn các giới hạn hàng tháng.

> **【中文解读】**Trung Typ Ecommerce Agent của tháng LLM Thành phần trong nhóm khởi động "để theo dõi đơn đặt hàng" kỹ năng từ$1,200 跳到 $4,800── đây không phải là lỗi định giá── đây là Agent tìm ra một vòng lặp mới và tiếp tục chi tiêu──Microsoft's Agent Governance Toolkit(4月2日) đã lập ra chống lại loại phòng thủ này: mỗi yêu cầu`max_tokens`、 mỗi nhiệm vụ token 和美元预算、 hàng ngày/ngày giới hạn trên 代 giới hạn trên 代 giới hạn trên  tầng mô hình đường路由、提示缓存、上下文窗口、昂贵动作上的 HITL 检查点、预算违反时的终止开关。Anthropic's Claude Code Agent SDK 以不同名称出货相同原语──金融速度限制例如10分钟内 >$50 切断访问比月度上限更快捕获循环──

> **【拓展：单一上限不够 → 分层栈】**失败模式和时间尺度需要应对:5秒重试的失控循环 (sự kiểm soát vòng lặp) 速度限制捕获) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏 (sự kiểm soát chậm) 工作的缓慢泄漏) 工作的缓慢性增长 (sự kiểm soát chậm) 缓慢性缓慢性) 缓慢性增长 (sự kiểm soát) 缓慢性缓慢性) 缓慢性增长) 缓慢性

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, layered cost-governor simulator) | **语言:** Python（标准库，分层成本治理器模拟器）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 12 (Durable execution) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 12（持久执行）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Học本节前请先掌握:Phase 15·10(权限模式) Phase 15·12(持久执行) 云成本管理基础──Cost Governors = 防"Denial of Wallet" (Của phủ nhận ví) 钱包拒绝服务攻击) 
>  **【类比】**Chi phí Thống đốc = "Công viên của tín dụng thẻ số"。普通 LLM 调用 = 刷卡(每次小钱);Công viên 进入死循环 = 盗刷(一夜烧光)。防御分层:(1) 速度限制10分钟 >$50 切断（防失控）；(2) 每日上限——$200/天(防慢泄漏);$3000/月（防坏发布）；(4) 单任务上限——$5/ nhiệm vụ (防单次任务爆炸)
> ️ **【易错点】**Chỉ định tháng độ lên giới hạn không định tốc độ giới hạn → 一夜烧完一个月预算才发现──修复: phải có "短周期速度限制"+"中周期日限制"+"长周期月限制"三层,越短越严,越早触发越好──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**成本控制器(Cost Governors) giám sát và hạn chế tiêu thụ tài nguyên của đại lý chủ yếu là API 调用费用和代币使用量。 không có kiểm soát chi phí đại lý có thể tạo ra một khoản chi phí khổng lồ trong chu kỳ hoặc hiệu quả thấp thực hiện。

> **【拓展：cost governors】**Kiểm soát thành phần là thách thức quan trọng của Agent 生产部署 năm 2025-2026  Các trường hợp công khai: nhiều người dùng báo cáo lập mã Agent trong vòng lặp sửa chữa tạo ra hàng ngàn đô la API  phí. Các giải pháp bao gồm: 1) giới hạn mã thông báo max_output_tokens của OpenAI; 2) API theo dõi sử dụng của nhân loại; 3) Kiểm soát chi phí của các công cụ thứ ba như Helicone và Braintrust.

Các nhân viên tự trị chi tiền thật cho mỗi lượt.

> Cảnh sát tự do trong mỗi vòng đều chi phí tiền thật.

Khả năng phát ra xấu của chatbot là một câu trả lời xấu; vòng lặp xấu của một đại lý là một hóa đơn. Thuật ngữ được công nghiệp ghi nhận cho chế độ thất bại là "Thà từ chối ví"

> 聊天机器人错误输出是一条错误回复; 代理的错误循环是一张账单――行业记录的失败模式术语是"Tước từ ví" 代理持续推理、持续调用工具、持续计费,没有什么阻止它,因为没有什么被设计为阻止──

Việc sửa chữa không phải là một số. Nó là một loạt các giới hạn ở các quy mô thời gian và độ phân mảnh khác nhau: theo yêu cầu, mỗi nhiệm vụ, mỗi giờ, mỗi ngày, mỗi tháng. Một loạt thiết kế tốt bắt được một vòng lặp chạy trong vòng vài phút, một rò rỉ chậm trong vòng vài giờ, và một giải phóng xấu trong vòng một ngày. cùng một loạt giữ một ngân sách ở tất cả khi đại lý là đường chân trời dài và tự trị.

> Phục hồi không phải là một con số. Nó là giới hạn về các quy mô và độ phân tích khác nhau trong thời gian: mỗi yêu cầu, mỗi nhiệm vụ, mỗi giờ, mỗi ngày, mỗi tháng. Được thiết kế tốt.

> **【中文解读】**Bài này giới thiệu khái niệm và phương pháp thực hiện cốt lõi của AI Agent.

Đây là một bài học kỹ thuật: toán học là tầm thường, kỷ luật là nơi mà các nhóm thất bại. Danh sách giới hạn dưới đây đều được đặt tên trong bộ công cụ quản lý đại lý Microsoft hoặc các tài liệu SDK của đại lý mã Anthropic Claude.

> Đây là một khóa học kỹ thuật: toán học bình thường, kỷ luật là nơi thất bại của đội.

## Khái niệm cốt lõi

### Các chi phí thống đốc xếp hàng.

1. **`max_tokens` per request.**Khả năng ngăn chặn bất kỳ cuộc gọi nào phát ra một kết thúc không giới hạn.
   Trung ngữ翻译:**每请求 `max_tokens`。**简单―― ngăn chặn đơn次调发无界补全――
2. **Per-task token budget.**Trong suốt cuộc chạy, đừng vượt quá N token.
   Trung ngữ翻译:**每任务 token 预算。**Toàn bộ hoạt động không vượt quá N 个 token.
3. **Per-task dollar budget.**Tương tự như tiền mã hóa nhưng bằng tiền tệ.`max_budget_usd`trong Claude Code.
   Trung ngữ翻译:**每任务美元预算。**Như biểu tượng tương tự nhưng như tiền tệ.`max_budget_usd`
4. **Per-tool call cap.**Không quá N `WebFetch`gọi, N `shell_exec`gọi điện, vv
   Trung ngữ翻译:**每工具调用上限。**Không quá N 个 `WebFetch`调用  个`shell_exec`调用等.
5. **Iteration cap (`max_turns`).**Tổng lặp vòng tròn đại lý; ngăn chặn vòng tròn lý luận vô hạn.
   Trung ngữ翻译:**迭代上限（`max_turns`）。**总 Agent 循环代数; ngăn chặn vòng lặp không giới hạn
6. **Per-minute / per-hour / per-day / per-month cap.**Đường kính tròn, bắt được rò rỉ ở các quy mô thời gian khác nhau.
   Trung ngữ翻译:**每分/时/日/月上限。**滚动窗口──在不同时间尺度捕获泄漏──
7. **Financial velocity limit.**Ví dụ, "nếu chi tiêu vượt quá 50 đô la trong 10 phút, cắt lối vào".
   Trung ngữ翻译:**金融速度限制。**Ví dụ: "Nếu 10 phút trong thời gian chi phí hơn 50 đô la, cắt truy cập"
8. **Tiered model routing.**Theo mặc định cho một mô hình nhỏ hơn; leo thang lên một mô hình lớn hơn chỉ khi một nhà phân loại đánh giá nhiệm vụ cho phép nó.
   Trung ngữ翻译:**分层模型路由。**默认小模型; chỉ khi phân loại các nhiệm vụ đánh giá đáng khi nâng cấp lên mô hình lớn hơn.
9. **Prompt caching.**Hệ thống nhanh chóng và ổn định bối cảnh được lưu trữ trong bộ nhớ cache của nhà cung cấp; chi phí token của việc gửi lại gần bằng không.
   Trung ngữ翻译:**提示缓存。**系统提示和稳定上下文 lưu trữ tại nhà cung cấp lưu trữ; tái phát triển của token 成本接近零──
10. **Context windowing.**Compaction / summation để giữ cho bối cảnh hoạt động dưới ngưỡng; giảm chi phí token trực tiếp.
    Trung ngữ翻译:**上下文窗口。**压缩/摘要 để giữ hoạt động trên 下文低于值; biểu tượng trực tiếp 成本降低。
11. **HITL checkpoints on expensive actions.**Trước khi một hành động được biết là đắt tiền (câu hỏi công cụ dài, tải xuống lớn, nâng cấp mô hình tốn kém), cần một chạm của con người.
    Trung ngữ翻译:**昂贵动作上的 HITL 检查点。**Trong một động tác đã biết đắt tiền, người ta yêu cầu người ta click.
12. **Kill switch on budget breach.**Trò chơi bị phá hủy khi bất kỳ ngọn lửa nào.
    Trung ngữ翻译:**预算违反时终止开关。**任一上限触发时会话停止──上限被记录;需要单独重新启动路径──

### Tại sao lại đống, không phải một cái nắp. Tại sao lại là cái nắp mà không phải là giới hạn.

Một mức giới hạn hàng tháng duy nhất chỉ bắt được một đại lý chạy trốn sau khi ví mất. Một mức giới hạn duy nhất mỗi yêu cầu không bắt được gì ở cấp độ phiên. Các chế độ thất bại khác nhau đòi hỏi các quy mô thời gian khác nhau:

> 单一月度上限只在钱包空后抓失控 代理. 单一每请求上限在会话级上什么也没抓.

- **Runaway loop**(truyền viên bị mắc kẹt trong một lần thử lại 5 giây): bị bắt bởi giới hạn tốc độ.
  Trung ngữ翻译:**失控循环**(Agent 卡在 5 秒重试): tốc độ giới hạn bắt giữ
- **Slow leak**(trợ lý làm ~ 2 lần dự kiến công việc cho mỗi nhiệm vụ): bị bắt bởi giới hạn hàng ngày.
  Trung ngữ翻译:**缓慢泄漏**(Công viên mỗi nhiệm vụ làm khoảng 2x 预期工作): mỗi ngày lên giới hạn bắt giữ.
- **Bad release**(khả năng mới sử dụng token 5x): được bắt bởi giới hạn hàng tuần / hàng tháng.
  Trung ngữ翻译:**坏发布**(New Version Using 5x Token): 每周/月上限捕获──
- **Legitimate surge**(trực tế nhu cầu, không phải là lỗi): bị bắt bởi giới hạn giờ / ngày với hồ sơ rõ ràng.
  Trung ngữ翻译:**合法激增**(真实需求,非 bug):小时/日上限带清晰日志捕获──

### Bảng ngân sách của Claude Code
### Một bề mặt ngân sách của vòng xoáy

Các SDK Claude Code Agent tiết lộ (tác liệu công khai):

> Claude Code Agent SDK 暴露(公开文档):

- `max_turns` nắp lặp.
  Trung ngữ翻译:`max_turns`代上限──
- `max_budget_usd` mức giới hạn đô la; phá thai phiên khi vi phạm.
  Trung ngữ翻译:`max_budget_usd`美元上限;违反时会话中止──
- `allowed_tools`- `disallowed_tools` công cụ allowlist và denylist.
  Trung ngữ翻译:`allowed_tools`- `disallowed_tools` công cụ cho phép danh sách và từ chối danh sách.
- Điểm nếp trước khi sử dụng công cụ để tính toán chi phí tùy chỉnh.
  Trung ngữ翻译:工具使用前的子点用于自定义成本核算──

Kết hợp với thang chế độ cho phép (Dạy 10.`autoMode`phiên mà không có `max_budget_usd`Anthropic rõ ràng định nghĩa chế độ tự động như yêu cầu kiểm soát ngân sách; phân loại là orthogonal với chi phí.

> Với quyền hạn mô hình阶梯 (第 10 课)结合──无`max_budget_usd`của `autoMode`会话是未治理的自主──Anthropic 明确将 Auto Mode 框定为需要预算控制; 分类器与成本正交──

### EU AI Act, OWASP Agent Top 10

Công cụ quản lý đại lý của Microsoft bao gồm các yêu cầu của Top 10 đại lý OWASP và Điều 14 của Đạo luật AI của EU (chống chế con người).

> Microsoft's Agent Governance Toolkit  bao gồm OWASP Agentic Top 10 và EU AI 法案第 14 条(Control nhân sự) yêu cầu.

### Những gì đã được quan sát$1,200 → $4.800 vụ được quan sát.$1,200 → $4.800 trường hợp

Trường hợp thực sự trong tài liệu Microsoft: một đại lý thương mại điện tử mà chi phí hàng tháng tăng gấp ba lần sau khi một công cụ mới được thêm vào.

> Ví dụ thực tế trong tài liệu Microsoft: Một đại lý điện tử trong việc thêm công cụ mới sau tháng chi phí tăng gấp ba lần.

Công cụ cho phép đại lý thăm dò tình trạng đặt hàng trong mỗi phiên. Không phát hiện vòng lặp. Không giới hạn mỗi công cụ. Không cảnh báo về tăng trưởng tuần qua tuần. Việc sửa chữa là một giới hạn mỗi công cụ cộng với một cảnh báo tăng trưởng hàng ngày. Đây là một mẫu: mỗi bề mặt công cụ mới là một vòng lặp tiềm năng mới; mỗi công cụ mới cần giới hạn riêng của nó và cảnh báo riêng của nó.

> Công cụ này cho phép Trưởng trong mỗi cuộc họp kiểm tra tình trạng đơn hàng vòng. Không kiểm tra vòng lặp. Không giới hạn hàng công cụ. Không giới hạn hàng vòng so với cảnh báo tăng trưởng.

## Hãy sử dụng nó để thực hiện
```figure
cost-governor-stack
```

## Sử dụng nó

`code/main.py`mô phỏng một đại lý chạy với và không có một đống quản lý chi phí lớp. Đại lý mô phỏng di chuyển vào vòng thăm dò sau một số lượt; đống đống lớp bắt nó trong cửa sổ tốc độ trong khi một nắp hàng tháng duy nhất sẽ không nổ ra cho đến vài ngày sau đó.

> `code/main.py`模拟有和没有分层成本管理的代理运行;模拟代理在某些轮次后漂移到轮询循环;分层在速度窗口内捕获它,而单一级上限直到几天后才触发;

## Chuyển nó đi.

`outputs/skill-agent-budget-audit.md`kiểm toán các khoản chi phí của một đại lý được đề xuất triển khai và đánh dấu các lớp thiếu sót.

> `outputs/skill-agent-budget-audit.md`审计提议 署 署 署 成本管理 并标记缺层──

## Tập luyện bài tập

1. Đi chạy`code/main.py`. xác nhận giới hạn tốc độ phát ra trước khi giới hạn lặp lại trên một quỹ đạo vòng thăm dò. Bây giờ vô hiệu hóa giới hạn tốc độ và đo lường bao nhiêu đại lý "gài" trước khi giới hạn lặp lại bắt nó.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận tốc độ giới hạn trong vòng lặp đường mòn 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 

2. Thiết kế một bộ nắp mỗi công cụ cho một đại lý trình duyệt (Dạy 11) Công cụ nào cần nắp chặt nhất? Công cụ nào có thể chạy không giới hạn mà không có rủi ro?
   Trung ngữ翻译:为浏览器 Agent ((第 11 课) 设计每工具上限集──哪个工具需要最紧上限?哪个工具可无限运行无风险?

3. Đọc các tài liệu của Microsoft Agent Governance Toolkit. Đăng danh sách từng loại nắp tên của bộ công cụ. Định dạng mỗi một trong các chế độ thất bại (số chạy, rò rỉ chậm, phát hành xấu, tăng).
   Trung文翻译:阅读Microsoft Agent Governance Toolkit 文档。列出工具包命名的每个上限类型──将各映射到失败模式之一(失控循环、缓慢泄漏、坏发布、激增)。

4. Giá một lần chạy không giám sát qua đêm cho một nhiệm vụ thực tế (ví dụ: "triangle 50 issues in a repo").`max_budget_usd`2x ước tính điểm của bạn.
   Trung文翻译:为真实任务 ((例如"分类 50 个仓库问题")定价隔夜无人值守运行――设置 `max_budget_usd`Vì bạn đánh giá điểm 2x.

5. Claude Code `max_budget_usd`thiết kế một giới hạn tốc độ bổ sung bạn sẽ áp dụng bên ngoài.
   Trung ngữ翻译:Claude Code của `max_budget_usd`Trong cuộc họp tổng chi phí. Thiết kế bạn sẽ hạn chế tốc độ bổ sung của bên ngoài bắt buộc.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Denial of Wallet | "Runaway bill" | Agent loop generating spend with no cap to stop it |
| Denial of Wallet | "失控账单" | 无上限阻止的 Agent 循环产生花费 |
| max_tokens | "Per-request cap" | Ceiling on a single completion's size |
| max_tokens | "每请求上限" | 单次补全大小上限 |
| max_turns | "Iteration cap" | Ceiling on agent loop iterations in a session |
| max_turns | "迭代上限" | 会话中 Agent 循环迭代数上限 |
| max_budget_usd | "Dollar kill switch" | Session cost cap; aborts on breach |
| max_budget_usd | "美元终止开关" | 会话成本上限；违反时中止 |
| Velocity limit | "Rate cap" | Limit on spend per short window (e.g., $50 / 10 min) |
| 速度限制 | "速率上限" | 短窗口花费限制（例如 $50/10 分钟） |
| Tiered routing | "Small model first" | Cheap model default; escalate only when classifier warrants |
| 分层路由 | "小模型优先" | 默认廉价模型；仅当分类器批准时升级 |
| Prompt caching | "Cached system prompt" | Provider-side cache reduces re-send token cost to near zero |
| 提示缓存 | "缓存系统提示" | 提供商侧缓存将重发 token 成本降至接近零 |
| HITL checkpoint | "Human approval gate" | Human tap required before expensive action |
| HITL 检查点 | "人类批准门" | 昂贵动作前需人类点击 |

## Xem thêm 延伸阅读

- [Anthropic Claude Code Agent SDK — agent loop and budgets](https://code.claude.com/docs/en/agent-sdk/agent-loop) `max_turns`- `max_budget_usd`, các công cụ cho phép.
  Trung ngữ翻译:`max_turns``max_budget_usd`、工具允许列表──
- [Microsoft Agent Framework — human-in-the-loop and governance](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) Các trạm kiểm soát chi phí của chính phủ.
  Trung文翻译:成本治理器检查点──
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) kiểm soát chi phí bên cung cấp.
  Trung ngữ翻译:提供商侧成本控制。
- [Anthropic — Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/prompt-caching) Cơ khí lưu trữ cache.
  Trung ngữ翻译:缓存机械──
- [Anthropic — Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) Cơ khí lưu trữ cache.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Mô hình chi phí cho các đại lý đường dài.
  Trung ngữ翻译:长程 Agent 的成本档案──
