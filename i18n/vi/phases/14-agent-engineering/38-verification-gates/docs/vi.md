# Chỗ kiểm tra cửa kiểm tra

> Người đại lý không được đánh dấu công việc của mình như đã hoàn thành. Một cổng xác minh đọc hợp đồng phạm vi, nhật ký phản hồi, báo cáo quy tắc và sự khác biệt, và trả lời một câu hỏi duy nhất: liệu nhiệm vụ này thực sự hoàn thành không? Nếu cổng nói không, nhiệm vụ không hoàn thành, bất kể trò chuyện nói gì.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 33 (Rules), Phase 14 · 36 (Scope), Phase 14 · 37 (Feedback) | **前置知识:** 见原文
**Time:** ~55 minutes | **时间:** 见原文

>  **【前置】**学本节前请先掌握:Phase 14·33(Rules) 、Phase 14·36(Scope) 、Phase 14·37(Feedback) 3 个前置都做完才能学验证门控。
>  **【类比】**Cổng kiểm tra: xuất厂质检.Agent స్వ言"我做完了"不算数gate 独立检查"测试是否通过、scope 是否守住、规则是否满足、diff 是否合理"──门控失败,任务不算完成──这是Phase 14·39(Reviewer Agent) 简体版gate 是脚本,reviewer 是 LLM──

## Mục tiêu học tập

- Định nghĩa một cổng xác minh như một chức năng xác định trên các đồ tạo tác bàn làm việc.
- Kết hợp báo cáo quy tắc, báo cáo phạm vi, hồ sơ phản hồi và phân biệt thành một phán quyết duy nhất.
- Gửi một `verification_report.json`Đại lý kiểm tra và thông tin cả hai đều có thể đọc.
- Từ chối tiến hành một nhiệm vụ về bất kỳ thất bại nghiêm trọng khối, mà không có ngoại lệ.

## Vấn đề  vấn đề giới thiệu

Các đại lý tuyên bố thành công quá dễ dàng.

> Trưởng lý:

> 验证门(Verification Gates) trong Agent 工作流的关键节点设置检查点──每个门验证前一步的输出是否满足要求,不满足则触发修复流──

- "Có vẻ tốt". Mô hình đọc ra sự khác biệt của nó và quyết định nó là đúng.
- "Các xét nghiệm đã qua". Ông nói với sự tự tin. Không có hồ sơ nào về việc xét nghiệm thực sự chạy.
- "Tình thức chấp nhận được đáp ứng". Các tiêu chí chấp nhận được giải thích đủ lỏng lẻo để có nghĩa là "bất cứ điều gì giống như đã được thực hiện".


> **【中文解读】**验证门在代理 执行的关键节点插入自动检查──常见验证门:(1) 编译检查代码修改后必须通过编译;(2) 测试检查提交前必须通过相关测试;(3) Lint 检查代码必须符合风格规范;(4) 安全检查必须引入已知漏洞──验证门防止错积――

Cổng kiểm soát phiên bản. Cổng được dây vào CI. Cổng không thể hối lộ nó. Cổng được kết nối với CI. Cổng kiểm soát phiên bản không thể hối lộ nó. Cổng kiểm soát phiên bản là một cổng kiểm soát. Cổng kiểm soát được kết nối với Cổng kiểm soát và không thể hối lộ.

> 工作台的修复是一个单一的验证门控,读取 代理 已产生的工件并做出判断.

> 验证门(Verification Gates) trong Agent 工作流的关键节点设置检查点──每个门验证前一步的输出是否满足要求,不满足则触发修复流──

## Khái niệm cốt lõi

```mermaid
flowchart TD
  Diff[Diff] --> Gate[verify_agent.py]
  Scope[scope_report.json] --> Gate
  Rules[rule_report.json] --> Gate
  Feedback[feedback_record.jsonl] --> Gate
  Gate --> Verdict[verification_report.json]
  Verdict --> Pass{passed?}
  Pass -- yes --> Review[Reviewer Agent]
  Pass -- no --> Refuse[refuse done + surface to human]
```


> **【中文解读】**验证门在代理 执行的关键节点插入自动检查──常见验证门:(1) 编译检查代码修改后必须通过编译;(2) 测试检查提交前必须通过相关测试;(3) Lint 检查代码必须符合风格规范;(4) 安全检查必须引入已知漏洞──验证门防止错积――

### Cái gì mà cổng kiểm tra

| Check | Source artifact | Severity |
|-------|-----------------|----------|
| All acceptance commands ran | `feedback_record.jsonl` | block |
| All acceptance commands exited zero | `feedback_record.jsonl` | block |
| Scope check has no forbidden writes | `scope_report.json` | block |
| Scope check has no off-scope writes | `scope_report.json` | block or warn |
| All block-severity rules pass | `rule_report.json` | block |
| No `null` exit codes in feedback | `feedback_record.jsonl` | block |
| Touched files match `scope.allowed_files` | both | warn |

A `warn`tìm kiếm ghi chú phán quyết; a `block`tìm kiếm ngăn cản `passed: true`- Tôi không biết.

> 验证门(Verification Gates) trong Agent 工作流的关键节点设置检查点──每个门验证前一步的输出是否满足要求,不满足则触发修复流──

### Định nghĩa, không xác suất

Cổng phải đưa ra cùng một phán quyết cho cùng một sản phẩm đặt mỗi lần. Không có thẩm phán LLM. thẩm phán LLM thuộc về phía nhà phê duyệt (Phase 14 · 39) nơi mục tiêu là đánh giá chất lượng, không phải là tình trạng.

> 验证门(Verification Gates) trong Agent 工作流的关键节点设置检查点──每个门验证前一步的输出是否满足要求,不满足则触发修复流──

### Một báo cáo, một con đường

Cổng phát ra một .`verification_report.json`mỗi nhiệm vụ kết thúc, được viết dưới `outputs/verification/<task_id>.json`CI tiêu thụ cùng một con đường, nhiều cổng với các con đường khác nhau làm cho nguồn của sự thật trở nên rõ ràng.

> 验证门(Verification Gates) trong Agent 工作流的关键节点设置检查点──每个门验证前一步的输出是否满足要求,不满足则触发修复流──

### Không có ngoại lệ

Các phát hiện về độ nghiêm trọng khối không thể bị bác bỏ bởi đại lý.`override_reason`và một `overridden_by`Đơn thay đổi là một sự thay đổi được ký kết, không phải là quyết định của đại lý.

> 验证门(Verification Gates) trong Agent 工作流的关键节点设置检查点──每个门验证前一步的输出是否满足要求,不满足则触发修复流──

## Hãy xây dựng nó.
```figure
wb-gate-sequence
```

## Hãy xây dựng nó

`code/main.py`thực hiện:

- Một bộ tải cho mỗi vật tạo ra, tất cả đều được đập vào địa phương để bài học tự nhiên.
- A `verify(task_id, artifacts) -> VerdictReport`chức năng thuần túy.
- Một máy in hiển thị kết quả kiểm tra và điểm vượt qua/không thành công cuối cùng.
- Một bản demo với ba kịch bản nhiệm vụ: thông qua sạch, phạm vi creep, mất chấp nhận.

Đi đi.

```
python3 code/main.py
```

Kết quả: ba bản báo cáo phán quyết, mỗi bản lưu bên cạnh kịch bản.

> 验证门(Verification Gates) trong Agent 工作流的关键节点设置检查点──每个门验证前一步的输出是否满足要求,不满足则触发修复流──

## Các mô hình sản xuất trong tự nhiên

Bốn mô hình nâng cổng từ "một công việc lông khác" lên "về quyết định".

> 验证门(Verification Gates) trong Agent 工作流的关键节点设置检查点──每个门验证前一步的输出是否满足要求,不满足则触发修复流──

**Defense-in-depth, not single gate.**Hook trước giao dịch → kiểm tra tình trạng CI → hook trước công cụ authz → cổng trước hợp nhất. Mỗi lớp là xác định, do đó một thất bại trong một lớp được bắt bởi lớp tiếp theo. sổ chơi tháng 3 năm 2026 của microservices.io là rõ ràng: hook trước giao dịch không thể vượt qua bởi vì, không giống như một kỹ năng bên mô hình, nó không phụ thuộc vào đại lý theo hướng dẫn. Cổng xác minh nằm ở lớp CI / pre-merge.

**Defense by deterministic check, model-judge only for nuance.**Các cặp chuẩn mực lai năm 2026 của Anthropic: phần thưởng có thể xác minh (thử nghiệm đơn vị, kiểm tra sơ đồ, mã thoát) trả lời "có mã giải quyết vấn đề không?"  Các quy tắc LLM trả lời "có mã có thể đọc được, an toàn, theo phong cách không?" Cổng chạy lớp đầu tiên; người xem xét (Phase 14 · 39) chạy thứ hai. Trộn chúng làm sụp đổ tín hiệu.

**Signed override log, not Slack threads.**Mỗi lần bỏ qua sẽ phát ra một hàng trong `outputs/verification/overrides.jsonl`với: timestamp, tìm kiếm mã, lý do, ký kết người dùng, hiện tại HEAD cam kết. thời gian chạy từ chối bất kỳ bỏ qua mà không có chữ ký; con đường kiểm toán là git-track. Đây là đường biên giữa một chính sách bỏ qua và một phim bỏ qua.

**Coverage floor as a first-class check.**A `coverage_report.json`cho ăn một `coverage_floor`(đánh giá mặc định 80%) Cổng thất bại nếu bảo hiểm đo lường giảm xuống dưới sàn hoặc dưới sàn hợp nhất trước đó hơn 1 điểm phần trăm. Không có kiểm tra này, các đại lý lặng lẽ xóa các thử nghiệm thất bại và báo cáo xác minh vẫn xanh lá cây.

**`--strict` mode promotes warns to blocks.**Đối với các chi nhánh giải phóng, PR chặn tàu, hoặc phân loại sau sự cố, `--strict`Lái cờ là chọn nhượng bộ theo chi nhánh, không phải là mặc định toàn cầu, bởi vì nghiêm ngặt đối với mọi thứ làm ăn mòn dòng chảy hàng ngày.

## Hãy sử dụng nó để thực hiện

Các mô hình sản xuất:

- **CI step.**A `verify_agent`Job chạy cổng chống lại các đồ tạo vật cuối cùng của đại lý.`passed: true`- Tôi không biết.
- **Pre-handoff hook.**Đặc vụ chạy thời gian gọi cổng trước khi tạo ra tài liệu giao hàng.
- **Manual triage.**Các nhà điều hành đọc báo cáo khi một nhân viên tuyên bố thành công và một con người nghi ngờ nó.

Cổng là cạnh quyết định trong dòng chảy của bàn làm việc.

> 验证门(Verification Gates) trong Agent 工作流的关键节点设置检查点──每个门验证前一步的输出是否满足要求,不满足则触发修复流──

## Chuyển nó đi.

`outputs/skill-verification-gate.md`dây cổng vào một dự án cụ thể: những lệnh chấp nhận nào cung cấp cho nó, những quy tắc nào là nghiêm trọng khối, những gì ngoài phạm vi viết được dung nạp, cách ghi nhật ký kiểm toán qua lại được lưu trữ.

> 验证门(Verification Gates) trong Agent 工作流的关键节点设置检查点──每个门验证前一步的输出是否满足要求,不满足则触发修复流──

## Tập luyện bài tập

1. Thêm một `coverage_floor`kiểm tra: chỉ huy thử nghiệm phải đưa ra báo cáo bảo hiểm ít nhất 80%.
  Trung ngữ翻译:思考并实践此练习。
2. Cung cấp cho một `--strict`chế độ thúc đẩy mọi `warn`đến`block`. Tài liệu các trường hợp trong đó chế độ nghiêm ngặt là mặc định đúng.
  Trung ngữ翻译:思考并实践此练习。
3. Làm cho cổng tạo ra một bản tóm tắt Markdown ngoài JSON. Bảo vệ các trường thuộc về bản tóm tắt.
  Trung ngữ翻译:思考并实践此练习。
4. Thêm một `time_since_last_human_touch`kiểm tra: bất kỳ tập tin nào được chỉnh sửa trong vòng 60 giây sau khi nhấn phím của con người đều được miễn trừ các cờ ngoài phạm vi.
  Trung ngữ翻译:思考并实践此练习。
5. Hãy chạy cổng trên một chất thực khác với sản phẩm của bạn. bao nhiêu phát hiện là thực và bao nhiêu là tiếng ồn? Cổng cần phát triển ở đâu?
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Verification gate | "The check that stops things" | Deterministic function over workbench artifacts producing a pass/fail verdict |  |
| Block severity | "Hard fail" | A finding that prevents `passed: true` and requires a signed override |  |
| Override log | "Why we let it through" | Signed entries with reason and user id, audited by review |  |
| Acceptance command | "The proof" | A shell command whose zero exit is what `done` means |  |
| One report path | "Source of truth" | `outputs/verification/<task_id>.json`, consumed by CI and humans alike |  |

## Xem thêm 延伸阅读

- [Anthropic, Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
  Trung ngữ: 翻译:见原文.
- [OpenAI Agents SDK guardrails](https://platform.openai.com/docs/guides/agents-sdk/guardrails)
  Trung ngữ: 翻译:见原文.
- [OpenAI Agents SDK guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [microservices.io, GenAI dev platform: guardrails](https://microservices.io/post/architecture/2026/03/09/genai-development-platform-part-1-development-guardrails.html) phòng thủ sâu giữa dự án trước và CI
  Trung ngữ: 翻译:见原文.
- [ICMD, The 2026 Playbook for Agentic AI Ops](https://icmd.app/article/the-2026-playbook-for-agentic-ai-ops-guardrails-costs-and-reliability-at-scale-1776661990431) Thang cổng chấp thuận (mở → chấp thuận → tự động dưới ngưỡng)
  Trung ngữ: 翻译:见原文.
- [Type-Checked Compliance: Deterministic Guardrails (arXiv 2604.01483)](https://arxiv.org/pdf/2604.01483) Lean 4 như giới hạn trên của định nghĩa gào
  Trung ngữ: 翻译:见原文.
- [logi-cmd/agent-guardrails — merge gate spec](https://github.com/logi-cmd/agent-guardrails) phạm vi + cổng thử nghiệm đột biến
  Trung ngữ: 翻译:见原文.
- [Guardrails AI x MLflow](https://guardrailsai.com/blog/guardrails-mlflow) Các xác thực viên xác định như là điểm số CI
  Trung ngữ: 翻译:见原文.
- [Akira, Real-Time Guardrails for Agentic Systems](https://www.akira.ai/blog/real-time-guardrails-agentic-systems) Cổng trước/ sau công cụ
  Trung ngữ: 翻译:见原文.
- Giai đoạn 14 · 27  phòng thủ tiêm nhanh (cặp đối thủ của cổng)
- Giai đoạn 14 · 36  hợp đồng phạm vi này thực thi
- Giai đoạn 14 · 37  hồ sơ phản hồi này cửa điểm
- Giai đoạn 14 · 39  đại lý kiểm tra cánh cổng bàn tay ra
