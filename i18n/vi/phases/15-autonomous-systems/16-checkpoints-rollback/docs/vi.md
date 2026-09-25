# Các điểm kiểm tra và quay lại.

> Mỗi chuyển đổi trạng thái biểu đồ vẫn tồn tại. Khi một công nhân bị tai nạn, hợp đồng thuê của nó hết hạn và một công nhân khác nhận lại tại điểm kiểm soát mới nhất. Cloudflare Durable Objects giữ trạng thái trong nhiều giờ hoặc tuần. Đề xuất sau đó cam kết (Lớp 15) xác định một kế hoạch quay lại mỗi hành động. Việc xác minh sau hành động sẽ đóng lại vòng lặp. Điều 14 của EU AI Act buộc phải giám sát con người hiệu quả cho các hệ thống có nguy cơ cao  trong thực tế điều này có nghĩa là các trạm kiểm soát phải được truy vấn, các lần quay lại phải được thử nghiệm, và các đường mòn kiểm toán phải tồn tại sau khi triển khai. Phương thức thất bại cấp tính: mà không có các khóa bất khả năng và kiểm tra điều kiện trước, một lần thử lại sau khi thất bại tạm thời có thể thực hiện hai lần hành động đã được phê duyệt. Việc xác minh sau hành động là điều bắt được nó.

> **【中文解读】**Mỗi biểu đồ chuyển đổi trạng thái kéo dài; người lao động n khi hết hạn thuê, người lao động khác n điểm kiểm tra mới nhất n khi nhặt. Cloudflare Durable Objects 跨数小时或数周持有状态. Nề xuất-sau-commit (第15 课) cho mỗi động tác định nghĩa kế hoạch quay lại.  động tác sau khi kiểm tra kết thúc vòng lặp.  EU AI 法第14 条使 hệ thống quản lý người có nguy cơ cao có hiệu quả.  Thực tế có nghĩa là điểm kiểm tra phải được kiểm tra, quay lại phải được thực hiện, kiểm tra phải được theo dõi xuyên triển khai tồn tại. Mô hình thất bại: không có  khóa và điều kiện đặt trước, kiểm tra ngay lập tức có thể tái kiểm tra được hai lần thực hiện.  động tác sau khi kiểm tra đã được phê duyệt.

> **【拓展：幂等+前置条件+验证+回滚四件套】**仅等不够:考虑"当余额 > $1000 时从 A 转 $100 đến B" của phê duyệt động tác. Cải nghiệm trong quá trình tái tạo, chỉ có 1 lần kiểm tra sẽ được thông qua, nhưng nếu A  dư trong quá trình tái tạo và tái tạo trong quá trình tái tạo khác giảm xuống còn 500 USD, điều kiện kiểm tra trước thất bại.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, checkpoint and rollback state machine) | **语言:** Python（标准库，检查点和回滚状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 15 (Propose-then-commit) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 15（propose-then-commit）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 15·12(Sự thực hiện bền vững) Phase 15·15(Tề xuất-sau-Công dụng)  DATABASE事务(ACID)  本节把"持久执行"+"提议-提交"组合成完整安全网──
>  **【类比】**检查点回滚 = "game's archive与读档"――检查点 = tự động lưu trữ(每通过一关存一次);回滚 = 读档(这关打错了回到上关) ・・・后果性动作四件套 = 等键(防止重启两次执行) + 前置条件(重启后世界状态仍符合预期) + 动作后验证(确认真实副作用发生) + 失败回滚(恢复到动作前) ・・・
> ️ **【易错点】**Chỉ có 1 khóa không có điều kiện đặt trước kiểm tra → Thêm vào thời gian dư đã được các quy trình khác thay đổi vẫn được thực hiện →  thông qua支.

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**Cơ chế kiểm tra và quay lại cho phép Cơ quan trong quá trình thực hiện lưu giữ trạng thái nhanh ảnh, thoát lỗi thời phục hồi đến trạng thái tốt trước đây. Đây tương tự như kiểm soát các dữ liệu cơ sở dữ liệu và phiên bản Git.

> **【拓展：checkpoints rollback】**检查点-回滚是可靠的代理系统基础设施――实现选择:(1) 文件系统级使用 Git或快照保存文件状态;(2) 数据库级使用事务保证数据一致性;(3) 应用级 代理自管理检查点(如LangGraph) ――关键权衡是检查点粒度太细会增加开销,太粗会丢失更多工作──

Việc thực hiện lâu dài (Học 12) làm cho một đại lý bị hỏng có thể bắt đầu lại. đề xuất sau đó cam kết (Học 15) làm cho một hành động được phê duyệt có thể kiểm toán.

> 持久执行 (第 12 课)使崩 Agent 可恢复;; đề xuất sau đó cam kết;;第 15 课)使批准动作可审计;;

Bài học này kết hợp với họ: điều gì xảy ra khi một hành động được phê duyệt thực hiện một phần, bị hỏng và tiếp tục?

> Bài viết liên kết với chúng: Khi phê duyệt động tác phần thực hiện, sụp đổ, phục hồi sẽ xảy ra gì?

Hệ thống thực tế đưa ra điều này theo cách khác:

> Thực tế hệ thống kết nối khác nhau:

> **【中文解读】**Bài này giới thiệu khái niệm và phương pháp thực hiện cốt lõi của AI Agent.

- **LangGraph**Checkpoint mỗi chuyển đổi trạng thái đồ thị đến PostgreSQL. Khi nhân viên bị sụp đổ, hợp đồng thuê được phát hành và một nhân viên khác tiếp tục tại checkpoint mới nhất.`interrupt()`, mà chính nó vẫn tồn tại.
  Trung ngữ翻译:**LangGraph**Để chuyển đổi từng trạng thái kiểm tra đến PostgreSQL── nhân viên 崩时租约释放另一个工人在最新检查点恢复──工作流在`interrupt()`上暂停, tự nó kéo dài.
- **Cloudflare Durable Objects**giữ trạng thái mỗi khóa trong nhiều giờ hoặc vài tuần.
  Trung ngữ翻译:**Cloudflare Durable Objects**跨数小时或数周持有每键状态──将计算与已批准动作的存储同址──
- **Microsoft Agent Framework**- Tự động`Checkpoint`Primitive trong API workflow; play cộng với idempotency bao gồm các thử nghiệm lại.
  Trung ngữ翻译:**Microsoft Agent Framework**Trong API lưu lượng làm việc`Checkpoint`原语;重放加等覆盖重试──

Trong mọi trường hợp, sự kết hợp thực sự hoạt động là: khóa idempotency + kiểm tra điều kiện trước + xác minh sau hành động + quay lại khi xác minh-không thành công.

> Trong mỗi trường hợp thực tế hợp tác là: 等键 + 前置条件检查 + 动作后验证 + 验证失败时回滚──

## Khái niệm cốt lõi

### Mỗi chuyển đổi đều tồn tại

Một chuyển đổi trạng thái đồ thị là bất kỳ bước nào di chuyển dòng công việc từ một trạng thái có tên đến một trạng thái khác. Các thực hiện ngây thơ chỉ tồn tại tại tại các điểm tham gia cụ thể; thực hiện sản xuất tồn tại ở mọi chuyển đổi. Chi phí (một vài người viết thêm) là nhỏ so với lợi nhuận độ tin cậy (tái chơi đất ở bất cứ đâu, phục hồi thuê là chính xác).

> 图 trạng thái chuyển đổi là bất kỳ bước nào trong chuyển đổi từ một trạng thái đặt tên đến một trạng thái đặt tên khác.  đơn giản thực hiện chỉ ở một điểm gửi cụ thể duy trì; sản xuất thực hiện duy trì mỗi chuyển đổi.

### Thuê phục hồi.

Khi một công nhân bị hỏng, dòng công việc không bị mất; hợp đồng thuê (một tuyên bố ngắn ngủi rằng công nhân này đang thực hiện cuộc chạy này) chỉ đơn giản là hết hạn. Một công nhân khác nhận điểm kiểm soát mới nhất và tiếp tục. Cơ chế thuê là điều cho phép hệ thống sản xuất tồn tại trong việc triển khai không mất công việc trong chuyến bay.

> công nhân 崩时工作流不丢失;租约(这个工人在执行这个运行的短暂声明) chỉ là过期――另一员工 拾起最新检查点恢复――租约机制让生产系统在不丢失的情况下进行工作中存活滚部署――

### Thất lực cộng với điều kiện tiên quyết

Chỉ cần tính năng tự do không đủ.$100 from A to B when balance > $1000. " Phòng lưu lượng công việc được thực hiện, bị hỏng giữa thực hiện, và tiếp tục. Nếu chỉ cần kiểm tra khóa idempotency, và thực hiện tiếp tục, chuyển nhượng chạy một lần (có chính xác). Nhưng hãy xem xét rằng giữa hỏng và tiếp tục, cân bằng của A giảm xuống 500 đô la thông qua một workflow khác.

> 仅等不够――考虑: 工作流被批准"当余额 > $1000 时从 A 转 $100 đến B"── 工作流提交、执行中崩、恢复──若仅检查等关键执行恢复,转账运行一次(正确) 但考虑崩和恢复间 A 余额通过另一工作流降至$500──等检查仍通过;前置条件不──没有前置条件检查,我们发透支──

Mỗi hành động có hậu quả cần cả hai:

> Mỗi động tác hậu quả cần hai điều:

- **Idempotency key**: ngăn chặn việc thực hiện hai lần.
  Trung ngữ翻译:**幂等键**: ngăn chặn hai lần thực hiện.
- **Precondition check**: xác nhận rằng nhà nước vẫn phù hợp với những gì đã được phê duyệt.
  Trung ngữ翻译:**前置条件检查**: xác nhận trạng thái vẫn có sự đồng thuận với phê duyệt

### Tiêu chuẩn sau hành động

"Công cụ trả lại 200" không phải xác minh. xác minh thực sự đọc lại trạng thái mục tiêu và xác nhận tác dụng phụ thực sự xảy ra.

> "工具返回 200" không xác nhận.

- Tái cập nhật cơ sở dữ liệu: `UPDATE ... RETURNING *`sau đó khẳng định trạng thái phù hợp hàng quay trở lại.
  Trung ngữ翻译:数据库更新:`UPDATE ... RETURNING *`Sau đó, tôi nói rằng tôi sẽ quay lại trạng thái dự kiến phù hợp.
- Gửi email: kiểm tra thư mục gửi cho ID tin nhắn sau khi gửi.
  Trung文翻译:邮件发送:提交后检查发送文件 中的消息 ID──
- Tác tập tin: đọc lại tập tin và phân phối nó.
  Trung ngữ翻译:文件写:回读文件并哈希──
- Lệnh API: theo dõi `GET`về nguồn tài nguyên mục tiêu.
  Trung文翻译:API 调用:对目标资源的后续 `GET`

Nếu xác minh thất bại, dòng công việc sẽ ở trạng thái xấu.

> 验证失败时工作流处于已知坏状态――回滚启动――

### Kế hoạch quay lại

Mỗi hành động liên quan trong đề xuất sau đó cam kết (Dạy học 15) mang theo một kế hoạch quay trở lại.

> đề xuất sau đó cam kết (第 15 课) 中每个后果性动作带回滚计划──类型:

- **In-band rollback**: làm đảo ngược tác dụng phụ trực tiếp (`DELETE`sau đó`INSERT`- `Send-correction-email`sau khi gửi).
  Trung ngữ翻译:**带内回滚**: direct反转副作用`INSERT`后 `DELETE`、发送后发送更正邮件) ⋅
- **Compensating transaction**: một hành động mới làm trung hòa nguyên bản (chương trình SAGA tiêu chuẩn).
  Trung ngữ翻译:**补偿事务**:抵消原始动作的新动作 (Sự động động thái của người dùng)
- **Out-of-band rollback**: cảnh báo một con người, tạm dừng quá trình làm việc, để lại tình trạng xấu để điều tra.
  Trung ngữ翻译:**带外回滚**: cảnh báo nhân loại, tạm dừng công việc, để lại tình trạng xấu để điều tra.

Không có sự phục hồi (no-op rollback) ("chúng ta không thể đảo ngược điều này") phải được nêu trong đề xuất.

> Không-op 回滚 (("我们不能撤销此") phải được đặt tên trong đề nghị.

### Luật AI của EU Điều 14 đọc hoạt động .

Điều 14 yêu cầu "sự giám sát nhân lực hiệu quả" cho các hệ thống có nguy cơ cao.

> 第 14 条要求高风险系统的有效人类监督"──运营术语中,实现者读为:

- Các điểm kiểm soát có thể được kiểm tra bởi một kiểm toán viên.
  Trung ngữ翻译:检查点可被审计者查询──
- Rollback được thử nghiệm (được thử nghiệm hết cuối đến cuối ít nhất một lần).
  Trung文翻译:回滚演练 ((至少端到端测试一次) ⋅
- Các đường mòn kiểm toán tồn tại sau khi triển khai (checkpoint backend không là tạm thời).
  Trung文翻译:审计追踪跨部署存活(检查点后端非临时)
- Các xác minh thất bại được báo động, không được ghi âm.
  Trung ngữ翻译:失败验证被警报而非静默记录。

Một dòng công việc bị hỏng giữa thời gian thực hiện, tiếp tục và hoàn thành tác dụng phụ mà không có đường kiểm tra + quay trở lại không tồn tại trong bài kiểm tra Điều 14.

> 提交中崩、恢复、无验证+回滚路完成副作用工作流不通过第 14条测试──

### Phương thức thất bại mạnh: thực hiện hai lần

Sự cố sản xuất phổ biến nhất trong không gian này: hành động được phê duyệt, bắt đầu tham gia, trả lại 200, luồng công việc bị hỏng trước khi duy trì trạng thái, tiếp tục và thực hiện lại.

> Các tai nạn sản xuất phổ biến nhất trong lĩnh vực này: động作批准、提交开始、返回 200、工作流在持久化状态前崩、恢复并重新执行──

1. Động thái được phê duyệt, khóa miễn trừ k.
   Trung文翻译:动作批准,等键 k。
2. Commit bắt đầu, thực hiện, trả lại 200.
   中文翻译:提交开始、执行、返回 200。
3. Workflow bị hỏng trước khi duy trì trạng thái "được cam kết".
   Trung文翻译:工作流在持久化"已提交" trạng thái trước sự sụp đổ.
4. Workflow tiếp tục; thấy "được chấp thuận nhưng không được cam kết"; thực hiện lại.
   中文翻译:工作流恢复;看到"批准但未提交";重新执行──
5. Tác dụng phụ nổ hai lần.
   Trung文翻译: phụ tác触发两次.

Giảm thiểu: duy trì một ý định "trong chuyến bay" trước khi thực hiện, thực hiện với một khóa idempotency, sau đó đánh dấu "được thực hiện" chỉ sau khi xác minh sau hành động thành công. Nếu các hoạt động bắn và viết trạng thái thất bại, bạn biết để xác minh và (nếu cần thiết) tái bắn. Nếu viết trạng thái thành công và hành động thất bại, bạn xác minh và bắn chính xác một lần thông qua con đường phục hồi.

> 缓解:执行前持久化"in-flight"意图,用等键执行,仅在动作后验证成功后标记"已提交"──如动作触发而状态写失败,你知道要验证(如必要) 重触发──如状态写成功而动作失败,你验证并通过恢复路径精确触发一次──

## Hãy sử dụng nó để thực hiện
```figure
checkpoint-replay
```

## Sử dụng nó

`code/main.py`thực hiện một dòng công việc kiểm soát được đặt theo điểm với idempotency, điều kiện trước, xác minh và quay trở lại. Người lái xe mô phỏng bốn kịch bản: chạy sạch, thử lại sau khi bị tai nạn (đấu bắt idempotency), thất bại trong điều kiện trước (lái bỏ dòng công việc mà không bắn), xác minh thất bại (cửa lửa quay trở lại).

> `code/main.py`实现带等等、前置条件、验证和回滚的检查点工作流──驱动器模拟四场景:干净运行、崩后重试(等捕获)、前置条件失败(工作流停止不触发)、验证失败(回滚触发)。

## Chuyển nó đi.

`outputs/skill-rollback-rehearsal.md`thiết kế một thử nghiệm thử nghiệm quay trở lại cho một dòng công việc được đề xuất và kiểm toán hậu quả của điểm kiểm tra để xác định sự bền vững của đường audit.

> `outputs/skill-rollback-rehearsal.md`Để đề xuất quy trình làm việc thiết kế quay lại tập luyện kiểm tra và kiểm tra kiểm tra điểm sau cuối kiểm tra theo dõi lâu dài.

## Tập luyện bài tập

1. Đi chạy`code/main.py`Để xác minh bốn kịch bản, trong trường hợp xảy ra tai nạn, xác nhận các vụ nổ chính xác là một lần trong các lần thử lại.
   Trung ngữ翻译:运行 `code/main.py`❖ kiểm chứng bốn trường hợp ❖ đối với trường hợp nộp trong vụ sụp đổ, xác nhận động tác trong thử nghiệm lần nữa

2. Thay đổi mô hình "đánh dấu như đã làm trước, sau đó làm nó" để trạng thái viết cháy sau khi hành động. Lặp lại kịch bản tai nạn. đo số lượng các hành động trùng lặp bắn.
   Trung ngữ翻译:修改"先标记完成再做"模式使状态写在动作后触发──重跑崩场景──测量多少重动作触发──

3. Thiết kế kế kế hoạch quay lại cho một hành động sản xuất cụ thể (ví dụ: "đưa vào một kênh Slack").
   Trung ngữ翻译:为特定生产动作 (例如"发到Slack频道") 设计回滚计划──分类为带内、补偿或带外──论证选择──

4. Hãy lấy một dòng công việc bạn biết. xác định từng chuyển đổi trạng thái. Đánh dấu mỗi điều kiện với yêu cầu độ bền (đằng sau / không tồn tại). Đếm những điều mà bạn hiện không tồn tại.
   Trung ngữ翻译:取一个你了解的工作流――识别每个状态转换――标记各个持久性要求(持久化/不持久化) ――计数你当前不持久化的――

5. Thử nghiệm quay trở lại lặp lại: thiết kế một thử nghiệm kết thúc đến kết thúc chạy một dòng công việc thực sự, làm sụp đổ nó, và xác nhận các vụ cháy đường quay trở lại.
   Trung ngữ翻译:演练回滚测试:设计端到端测试运行真实工作流、崩、确认回滚路径触发──测试断言什么?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Checkpoint | "Save point" | Every graph-state transition persists to a durable store |
| 检查点 | "保存点" | 每个图状态转换持久化到持久存储 |
| Lease | "Worker claim" | Short-lived claim that a worker is executing a run; expires on crash |
| 租约 | "Worker 声明" | worker 正在执行运行的短暂声明；崩溃时过期 |
| Precondition | "State gate" | Assertion that the state is still consistent with the approved action |
| 前置条件 | "状态门" | 状态仍与批准动作一致的断言 |
| Post-action verify | "Re-read check" | Confirm the side effect actually happened in the target system |
| 动作后验证 | "回读检查" | 确认副作用在目标系统中实际发生 |
| In-band rollback | "Direct undo" | Reverse the side effect with the inverse operation |
| 带内回滚 | "直接撤销" | 用逆操作反转副作用 |
| Compensating transaction | "SAGA undo" | A new action that neutralizes the original |
| 补偿事务 | "SAGA 撤销" | 抵消原始动作的新动作 |
| Mark-as-done-first | "Status write order" | Persist the committed status before returning from commit |
| 先标记完成 | "状态写顺序" | 从提交返回前持久化已提交状态 |
| Article 14 | "EU AI Act human oversight" | Operational: queryable checkpoints, rehearsed rollbacks, auditable trail |
| 第 14 条 | "EU AI 法案人类监督" | 运营：可查询检查点、演练回滚、可审计追踪 |

## Xem thêm 延伸阅读

- [Microsoft Agent Framework — Checkpointing and HITL](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) Đường kiểm soát nguyên thủy và thu hồi thuê.
  Trung ngữ翻译:检查点原语和租约恢复。
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) Các đối tượng bền như một nền trạng thái.
  中文翻译:Thể vật bền 作为状态基板。
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/) cơ sở quy định.
  Trung ngữ翻译:监管基线。
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) khung độ tin cậy cho các dòng công việc dài hạn.
  Trung ngữ翻译:长程工作流的可靠性框架──
- [Anthropic — Claude Code Agent SDK: agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) hình dạng luồng làm việc cho Claude Code Routines.
  Trung文翻译:Claude Code Routines 的工作流形态──
