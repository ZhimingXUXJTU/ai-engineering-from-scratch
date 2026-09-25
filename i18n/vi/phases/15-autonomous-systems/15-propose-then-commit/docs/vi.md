# Người trong vòng: đề xuất-vậy-đề nghị.

> Sự đồng thuận năm 2026 về HITL là cụ thể. Nó không phải là "nhà đại lý hỏi, người dùng nhấp vào phê duyệt". Nó là đề xuất-sau đó cam kết: hành động được đề xuất được duy trì đến một cửa hàng bền vững với một khóa idempotency; xuất hiện trước một nhà phê duyệt với ý định, dòng dữ liệu, quyền được chạm vào, bán kính bùng nổ và kế hoạch quay lại; chỉ thực hiện sau sự xác nhận tích cực; xác minh sau khi thực hiện để xác nhận tác dụng phụ thực sự xảy ra. LangGraph's `interrupt()`cộng với PostgreSQL checkpointing, Microsoft Agent Framework của `RequestInfoEvent`, và Cloudflare `waitForApproval()`tất cả thực hiện cùng một hình dạng. chế độ thất bại theo quy luật là phê duyệt bằng dấu cao su: "T phê duyệt?" được nhấp mà không cần xem xét.

> **【中文解读】**2026 năm HITL 共识是具体的──不是"Agent 问, user点击 Approve"──是提出-then-commit:提议动作以等键持久化到持久存储;向审查员呈现意图、数据谱系、触及权限、爆炸半径、回滚计划;仅在正面确认后提交;执行后验证确认副作用实际发生──`interrupt()`加 PostgreSQL 检查点、Microsoft Agent Framework của `RequestInfoEvent`、Cloudflare của `waitForApproval()`                                                                                                                                                                                                                                                              

> **【拓展：四个状态机步骤】**đề xuất-sau-bắt buộc là bốn bước trạng thái机:(1) 提议Agent 产生动作,以等键持久化带意图/数据谱系/触及权限/爆炸半径/回滚计划;(2) 呈现审查员(人类,非代理自审) xem tất cả các dữ liệu;(3) 提交正面确认,动作执行;(4) 验证执行后回读副作用确认──这是数据库`RETURNING`子句、AWS `PutObject`后 `GetObject`、Stripe/AWS API 等键模式在代理审批上的复用──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, propose-then-commit state machine with idempotency) | **语言:** Python（标准库，带幂等的提议-提交状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 14 (Tripwires) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 14（触发器）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 15·12(Sự thực hiện bền vững) Phase 15·14(Kill Switches) Phase 14·15(HITL Agent 模式)  本节是HITL 的工程化标准四步状态机──
>  **【类比】**Propose-then-Commit = "Bank大额转账审批"──普通 LLM 调用 = 即时转账(错了找客服);Propose-then-Commit = 提交转账申请(含收款人、金额、用途、回滚预案)→ 审查员看元数据 → 批准 → 执行 → 验证到账──每一步都不能省──这是人类计算机使用、Claude Code Plan Mode、Stripe API 等的键统一模式──
> ️ **【易错点】**"Tính chấp?" 弹窗被用户惯性点"是" → 皮章失效──修复:(1) 多选清单(每个动作独立确认);(2) 强制延迟(3秒倒计时);(3) 关键动作双确认(输入金额数字);(4) 显示"爆炸半径"(影响 N 个文件、M 个用户) ・・・

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**Trước đề xuất sau khi nộp (được đề xuất sau đó thực hiện) mô hình yêu cầu Cơ quan tạo ra trước các sửa đổi nhưng không ngay lập tức thực hiện, mà chỉ trình bày cho người dùng hoặc Cơ quan khác kiểm tra, kiểm tra thông qua sau khi nộp. Đây là mô hình quan trọng của Cơ quan an toàn sẽ 'thử suy nghĩ' và 'hành động' tách biệt, cho con người hoặc hệ thống một cơ hội để thực hiện kiểm tra và sửa chữa trước khi thực hiện.

> **【拓展：propose then commit】**Mô hình gửi trước đề xuất là thực tiễn an ninh tiêu chuẩn của Cử nhân năm 2026 Claude Code 默认使用此模式生成修改建议并等用户确认──Git's PR/MR cơ chế cũng là ứng dụng của mô hình này代码修改先提出,经过审查才合并── Trong Agent 上下文, mô hình này đặc biệt quan trọng, vì lỗi của Cử nhân có thể gây tổn hại hơn so với lỗi của con người──

Một đại lý thực hiện một hành động. Người dùng phải quyết định: chấp thuận hay không. Nếu quyết định là ngay lập tức, nó có lẽ không phải là một đánh giá lại.

> Người dùng phải quyết định: chấp thuận hay không chấp thuận. Nếu quyết định là ngay lập tức, thì có thể không phải là kiểm tra.

Nếu quyết định được cấu trúc, nó chậm nhưng đáng tin cậy.

> Nếu quyết định là cấu trúc, nó chậm nhưng đáng tin cậy.

Mô hình HITL thời kỳ 2023 là một lời nhắc đồng bộ: "Đại lý muốn gửi email đến X với cơ thể Y  chấp thuận?" Người dùng nhấp vào chấp thuận. Mọi người cảm thấy hệ thống an toàn. Trong thực tế, bề mặt này bị dán gốm nặng: người dùng chấp thuận nhanh, chấp thuận dự đoán ít, và khi đại lý sai, đường kiểm toán cho thấy một lịch sử lâu dài của sự chấp thuận người dùng không thể nhớ lại.

> 2023 时代 HITL 模式是同步提示:"Đội ngũ cần gửi thư cho X,正文 Y批准?" người dùng nhấp vào  phê duyệt。 mọi người cảm thấy hệ thống an toàn。 thực tế trong giao diện này bị nghiêm trọng皮章化: người dùng nhanh chóng phê duyệt, phê duyệt dự đoán性低, khi Trưởng xuất hiện  phê duyệt theo dõi cho thấy người dùng không thể nhớ được lịch sử phê duyệt dài。

> **【中文解读】**Bài này giới thiệu khái niệm và phương pháp thực hiện cốt lõi của AI Agent.

Mô hình 2026  đề xuất sau đó cam kết  di chuyển HITL lên một nền bền, gắn metadata có cấu trúc và yêu cầu cam kết tích cực.

> 2026 năm mô hình  đề xuất-sau-thói buộc sẽ chuyển HITL  lên持久基板上, thêm cấu trúc hóa元数据, yêu cầu phải nộp chính thức

Mỗi SDK quản lý đại lý gửi một phiên bản: LangGraph `interrupt()`, Microsoft Agent Framework `RequestInfoEvent`, Cloudflare `waitForApproval()`Tên API khác nhau; hình dạng không.

> Mỗi người quản lý đại lý SDK xuất khẩu`interrupt()`、Microsoft Agent Framework `RequestInfoEvent`、Cloudflare `waitForApproval()`△API 名称不同;形态不。

## Khái niệm cốt lõi

### Máy lập trường đề nghị sau đó thực hiện

1. **Propose.**Agent tạo ra một hành động được đề xuất. tiếp tục đến một kho lưu trữ bền (PostgreSQL, Redis, Durable Object). Bao gồm:
   Trung ngữ翻译:**提议。**Agent 产生提议动作──持久化到持久存储(PostgreSQL、Redis、Durable Object) ── bao gồm:
   - ý định (tại sao đại lý làm điều này)
     Trung ngữ翻译:意图(Agent 为什么做这个)
   - dòng dõi dữ liệu (nguồn dẫn đến đề xuất này)
     Trung文翻译:数据谱系 (What causes this proposal)
   - quyền được chạm vào (những phạm vi / tập tin / điểm cuối)
     Trung ngữ翻译:触及的权限(哪些范围/文件/端点)
   - Ánh sáng nổ (điều gì là trường hợp tồi tệ nhất)
     Trung ngữ翻译:爆炸半径 (Bùng nổ nửa đường)
   - kế hoạch quay trở lại (nếu đã thực hiện, chúng ta sẽ hủy bỏ nó như thế nào)
     中文翻译:回滚计划 (如提交,如何撤销)
   - Key idempotency (một số đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn đơn
     Trung ngữ翻译:等键(每提议唯一;重提交回归同一记录)
2. **Surface.**Người đánh giá thấy đề xuất với tất cả các siêu dữ liệu. Người đánh giá là một người (không phải là đại lý tự đánh giá).
   Trung ngữ翻译:**呈现。**审查员看带所有元数据的提议──审查员是个人(不是代理自审)──
3. **Commit.**Chứng nhận tích cực, hành động được thực hiện.
   Trung ngữ翻译:**提交。**正面确认――动作执行――
4. **Verify.**Sau khi thực hiện, tác dụng phụ được đọc lại và xác nhận. Nếu bước xác minh thất bại, hệ thống đang trong trạng thái xấu và báo động hoạt động.
   Trung ngữ翻译:**验证。**执行后副作用 được đọc lại xác nhận. Nếu các bước kiểm tra thất bại, hệ thống đang trong tình trạng xấu đã biết và khởi động báo động.

### Chìa khóa vô hiệu hóa

Không có chìa khóa vô hiệu, một lần thử lại sau khi thất bại tạm thời có thể thực hiện hai lần hành động được phê duyệt.

> Không có gì khác, ngay lập tức thất bại sau đó, thử lại có thể được thực hiện hai lần đã được phê duyệt.

Ví dụ cụ thể: người dùng chấp thuận "chạy chuyển $100 từ A sang B. " Các màn hình mạng. Giao dịch công việc được thử lại. Người dùng đã chấp thuận một lần nhưng chuyển giao được thực hiện hai lần.

> Ví dụ cụ thể: người dùng phê duyệt từ A 转 $100 đến B ⋅ mạng闪断――工作流重试―― người dùng phê duyệt một lần nhưng chuyển账执行两次――等键将批准绑定到单一唯一副作用;第二次执行是无-op──

Đây là mô hình idempotency tương tự như Stripe và AWS API sử dụng. Việc sử dụng lại cho sự chấp thuận của đại lý được rõ ràng trong tài liệu Microsoft Agent Framework.

> Đây là kiểu sử dụng của Stripe và AWS API tương tự.

### Đang bền: tại sao sự chấp thuận vượt quá quá quá trình

Phòng chờ phê duyệt là một phần của trạng thái mà đại lý không sở hữu.`interrupt()`với PostgreSQL kiểm tra điểm và không chỉ trong trạng thái trong bộ nhớ  một phê duyệt hai ngày sau vẫn tìm thấy dòng công việc nguyên vẹn.

> 批准等候室是代理 不拥有一片状态――工作流暂停――第 12 课)――批准到达时,工作流从该精确点恢复――这就是为什么 LangGraph将`interrupt()`Với PostgreSQL  kiểm tra điểm không chỉ là trạng thái trong trong trong 2 ngày sau đó phê duyệt vẫn tìm thấy toàn bộ dòng làm việc.

### 章 phê duyệt và đáp ứng thách thức 章 phê duyệt và đáp ứng thách thức

Các UI mặc định cho HITL ("Tính chấp" / "Từ chối" nút) tạo ra phê duyệt nhanh chóng mà không có đánh giá thực sự. Thuyên giảm tài liệu: một danh sách kiểm tra thách thức và phản ứng đòi hỏi câu trả lời tích cực cho các câu hỏi cụ thể trước khi nút phê duyệt được bật.

> HITL 默认 UI("Tính chấp"/"Tính phủ" 按)产生快速批准无真实审查──已记录缓解:在 批准按启动前要求对特定问题正面回答的挑战-响应清单──具体形状:

- "Bạn có hiểu nguồn tài nguyên nào mà điều này chạm vào không?"
  Trung ngữ翻译:"你了解这触及什么资源吗?[ ]"
- "Bạn đã xác minh được bán kính của vụ nổ là chấp nhận được không?"
  Trung ngữ翻译:"你验证了爆炸半径可接受吗?[ ]"
- "Bạn có kế hoạch quay lại nếu điều này thất bại không?"
  Trung ngữ翻译:"If失败你有回滚计划吗?[ ]"

Không phải là một chế độ quan chức vì lợi ích của chính nó. Một chức năng buộc. Người xem không thể đánh dấu các hộp hoặc yêu cầu giải thích (sự leo thang) hoặc từ chối (sự mặc định an toàn). Nghiên cứu anthropic về an toàn đại lý rõ ràng trích dẫn HITL dựa trên danh sách kiểm tra như là một biện pháp giảm thiểu cho các mẫu phê duyệt bằng dấu cao su.

> Không phải vì quan chức và quan chức là hàm bắt buộc Không thể勾选框的审查者要么要求澄清升级拒绝安全默认 Anthropic Agent 安全研究明确引用清单驱动HITL 作为皮章批准模式的缓解

### Điều gì là quan trọng là hậu quả của nó.

Không phải mọi hành động đều cần đề xuất sau đó cam kết.

> Không phải mỗi động tác đều cần đề xuất-sau-thành động.

- **Consequential actions**(hằng ngày HITL): ghi chép không thể đảo ngược, giao dịch tài chính, giao tiếp ra ngoài, thay đổi cơ sở dữ liệu sản xuất, hoạt động hệ thống tập tin phá hủy.
  Trung ngữ翻译:**后果性动作**(总 HITL): không thể đảo ngược, giao dịch tài chính, ngoại phát giao, sản xuất cơ sở dữ liệu, thay đổi, phá hoại hệ thống tài liệu, hoạt động.
- **Reversible actions**(đôi khi là HITL): chỉnh sửa các tệp địa phương, thay đổi trình độ, viết đảo ngược với sự quay lại rõ ràng.
  Trung ngữ翻译:**可逆动作**(有时 HITL):本地文件编辑、舞台化 环境变更、带清晰回滚的可逆写──
- **Reads and inspections**(không bao giờ HITL): đọc một tập tin, liệt kê tài nguyên, gọi một API chỉ đọc.
  Trung ngữ翻译:**读和检查**(从不HITL):读文件列资源调用只读API。

### Tiêu chuẩn sau hành động

"Commit run" không giống như "the side effect happened". Các điều kiện phân vùng mạng và chạy đua có thể tạo ra một workflow nghĩ rằng nó đã thành công trong khi backend không tồn tại. Bước xác minh đọc lại tài nguyên mục tiêu sau khi cam kết xác nhận. Đây là mô hình tương tự như các giao dịch cơ sở dữ liệu với `RETURNING`Điều khoản hoặc AWS `GetObject`sau đó`PutObject`- Tôi không biết.

> "đầu đã chạy" không bằng "được dụng xảy ra"                                                                                                                                                                                                                                                        `RETURNING`Các vấn đề cơ sở dữ liệu`PutObject`后 `GetObject`AWS tương tự mô hình.

### Điều 14 của Luật AI của EU

Điều 14 yêu cầu giám sát nhân lực hiệu quả cho các hệ thống AI có nguy cơ cao trong EU. "Hiệu quả" không phải là trang trí. Ngôn ngữ quy định đặc biệt loại trừ các mô hình dấu cao su. đề xuất sau đó thực hiện với thách thức và phản ứng là hình dạng tồn tại trong kiểm tra Điều 14 trong tài liệu tuân thủ của Bộ Công cụ Quản trị Trưởng lý Microsoft.

> Điều 14 条强制 EU 高风险 AI 系统的有效人类监督――"有效" không phải là trang trí――监管语言明确排除皮章模式――带挑战-响应的建议-然后-承诺 是在微软代理治理工具包 合规文档中通过第 14 条审查的形式――

## Hãy sử dụng nó để thực hiện
```figure
mx-propose-then-commit
```

## Sử dụng nó

`code/main.py`Dryer thực hiện một máy tính propose-then-commit trong stdlib Python. Durable store là một tệp JSON. Idempotency key là một hash của (thread_id, action_signature). Driver mô phỏng ba trường hợp: một dòng phê duyệt sạch, một lần thử lại sau khi thất bại tạm thời (không được thực hiện hai lần), và một dấu cao su mặc định so với một dòng thách thức và phản ứng.

> `code/main.py`Sử dụng Python 实现 propose-then-commit 状态机──持久存储是 JSON 文件──等键是 (thread_id, action_signature) 的哈希──驱动器模拟三例:干净批准流、瞬态失败后重试(必须不双执行)

## Chuyển nó đi.

`outputs/skill-hitl-design.md`xem xét một quy trình làm việc HITL được đề xuất cho hình dạng đề xuất sau đó cam kết và đánh dấu các lớp metadata, idempotency, xác minh hoặc thách thức và phản ứng thiếu.

> `outputs/skill-hitl-design.md`审查提议 HITL 工作流的建议-然后-承诺 形态并标记缺失的元数据、等、验证或挑战-响应层──

## Tập luyện bài tập

1. Đi chạy`code/main.py`- xác nhận rằng một lần thử lại một đề xuất được phê duyệt sử dụng hồ sơ lâu dài và không thực hiện lại. Bây giờ thay đổi khóa idempotency để bao gồm một dấu thời gian và hiển thị các lần thử lại.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận đã phê duyệt đề xuất sử dụng thử lại ghi chép lâu dài và không được thực hiện lại.

2. Cải dài hồ sơ đề xuất bằng một `rollback`Field. mô phỏng một hành động mà bước xác minh thất bại. hiển thị việc quay lại tự động.
   中文翻译:用 `rollback`字段扩展提议记录──模拟验证步骤失败的执行──展示回滚自动触发──

3. Đọc Microsoft Agent Framework `RequestInfoEvent`Docs. xác định một trường siêu dữ liệu API bao gồm rằng động cơ đồ chơi bị thiếu.
   Trung ngữ翻译:阅读 Microsoft Agent Framework của `RequestInfoEvent`文档――识别 API 包含而玩具引擎缺失的一个元数据字段――添加它并解释它防止什么――

4. Thiết kế danh sách kiểm tra thách thức và phản ứng cho một hành động cụ thể (ví dụ: "thông vào tài khoản Twitter công cộng").
   Trung ngữ翻译:为特定动作 (ví dụ: "发到公共Twitter账号") thiết kế thách thức-响应清单――审查 viên phải trả lời ba câu hỏi nào? Tại sao ba câu hỏi này?

5. Chọn một trường hợp mà một lời nhắc đồng thời "Thỏa thuận?" sẽ đủ (không cần phải lưu trữ lâu dài).
   Trung ngữ翻译:选一个同步"Từu"提示就足够(不需要持久存储) 案例──解释为什么,并命名你接受的风险类──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Propose-then-commit | "Two-phase approval" | Persisted proposal + positive commit + verify |
| Propose-then-commit | "两阶段批准" | 持久提议 + 正面提交 + 验证 |
| Idempotency key | "Retry-safe token" | Unique per proposal; second execution no-ops |
| 幂等键 | "重试安全 token" | 每提议唯一；第二次执行 no-op |
| Data lineage | "Where it came from" | The specific source content that led to the proposal |
| 数据谱系 | "它从哪来" | 导致提议的特定源内容 |
| Blast radius | "Worst case" | Scope of effect if the action goes wrong |
| 爆炸半径 | "最坏情况" | 动作出错时的影响范围 |
| Rubber-stamp | "Fast approval" | "Approve" clicked without genuine review |
| 橡皮章 | "快速批准" | 无真实审查地点击"Approve" |
| Challenge-and-response | "Forcing checklist" | Reviewer must positively acknowledge specific questions |
| 挑战-响应 | "强制清单" | 审查者必须正面确认特定问题 |
| RequestInfoEvent | "MS Agent Framework primitive" | Durable HITL request with structured metadata |
| RequestInfoEvent | "MS Agent Framework 原语" | 带结构化元数据的持久 HITL 请求 |
| `interrupt()` / `waitForApproval()` | "Framework primitives" | LangGraph / Cloudflare equivalents of the same shape |
| `interrupt()` / `waitForApproval()` | "框架原语" | 相同形态的 LangGraph / Cloudflare 等价物 |

## Xem thêm 延伸阅读

- [Microsoft Agent Framework — Human in the loop](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) `RequestInfoEvent`, chấp thuận lâu dài.
  Trung ngữ翻译:`RequestInfoEvent`、được phê duyệt lâu dài.
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) `waitForApproval()`và các vật thể bền.
  Trung ngữ翻译:`waitForApproval()`和 Các vật thể bền vững
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) HITL như một biện pháp giảm thiểu rủi ro về đường dài.
  Trung文翻译:HITL 作为长程风险缓解──
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/) Nguyên tắc cơ bản về các hệ thống có nguy cơ cao.
  Trung ngữ翻译:高风险系统的监管基线──
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) quy định hiến pháp xung quanh giám sát.
  Trung ngữ翻译:监督的宪法框架──
